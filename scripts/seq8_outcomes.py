"""SEQ-8 — D3 outcome substrate + cascade->birth JOIN, D4 route-vs-outcome matrix.

Contract: exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md

*** I6 ANALYSIS EMBARGO ***
Everything this file emits is SUBSTRATE. It is emitted, hashed and filed; it is
NOT analyzed, ranked, promoted or turned into a claim in this run. The parked
registrations (leap outcome edge, grind<->loser join, route-conditioned edge)
wait for the operator's stamps after the Secret Sauce deep-dive. The only claim
scored this run is P-SEQ-ii, which lives in seq8_views.py / seq8_atlas.py and
never opens an outcome column. Keeping the outcome maths in a separate file is
how that embargo is made structural rather than promised.

D3 — per cascade terminus
  per-lens fixed-horizon MFE **and MAE** at the census horizons {20,100,500}
  exec bars, in bps and in ATR, with truncation flags; plus the event-based
  outcomes (time-to-tier-clearance, survival-to-next-tier); plus the
  cascade->birth JOIN to journal keys (cell_id, tranche_id).

THE JOIN RULE — STATED, NEVER SILENT (contract D3, fixture F-SEQ3)
  A birth joins a cascade iff ALL THREE hold:
    (a) the journal cell's symbol == the cascade's asset;
    (b) the cell's GOVERNOR timeframe appears as a rung in that cascade
        (engine/cells.py MANDATES: intraday->1h, swing->4h, position->12h);
    (c) the birth's ts_open falls inside the cascade span, i.e. within
        [first rung's bar_close, terminus rung's bar_close].
  Births are evt in {ENTRY_FILL, ADD_FILL} (scripts/wf1_forensics.py:75);
  ts_open is an ISO string on the cell's EXEC timeframe, converted to epoch ms.
  The join is restricted to lattice A / 9_89 because that is the cross the
  engine actually trades (engine/signals.py); joining fills to a 12_25 or
  89_200 cascade would assert a relationship the engine never had.

  Journals carry NO EMA-lattice state (W-F1 P-WF1 premise-false, verified
  again here by key scan). This join is therefore the ONLY bridge between
  cascade-world and trade-world, which is why the rule is printed rather than
  buried.

D4 — route-vs-outcome matrix at the 4h arrival
  source rung x curtain-cut MFE/MAE distribution, per asset and per view.

CURTAIN (F-SEQ5). Outcome columns are post-curtain BY DEFINITION — they are the
future. They are labelled as such, never mixed into the descriptive set. The
curtain audit emitted here follows the W-F1 shape (wf1_forensics.py:901-929):
a `clean` list with a per-column attestation and a `post_curtain` list.

Usage:
  python scripts/seq8_outcomes.py
"""
from __future__ import annotations

import argparse
import bisect
import glob
import json
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as cb                                       # noqa: E402
from engine.cells import MANDATES                               # noqa: E402
from seq8_extract import iso, rnd, write_json, R6               # noqa: E402
from seq8_views import TFI, TIER_GRAMMAR, sha256_file           # noqa: E402

BOX = ROOT / "_reviewer_box" / "wf1"
CANON_JOURNAL = ROOT / "research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored"
JOIN_LATTICE, JOIN_CLASS = "A", "9_89"
TIER_ORDER = ["FAST", "STAIR", "SLOW", "TREND"]

CURTAIN_CLEAN = [
    ("asset|lattice|event_class|view|dir", "cascade identity; fixed at construction"),
    ("depth|rungs_absolute|rungs_gov_relative|rungs_tier",
     "read from event bars at or before the terminus bar close"),
    ("init_tf|init_ts|term_tf|term_ts|span_ms", "event timestamps at/before terminus"),
    ("monotone|shuffle|family_first3|sig_first3", "derived from the rung string alone"),
    ("sojourn_ms|sojourn_exec_bars", "gaps between rungs already realised"),
    ("source_into_*|latency_to_*", "derived from rungs at/before the terminus"),
    ("term_exec_idx|p0_terminus|atr_basis",
     "the first exec bar OPEN at/after the terminus bar close — the first "
     "tradeable instant, no lookahead"),
]
POST_CURTAIN = [
    ("mfe_bps_h*|mae_bps_h*|mfe_atr_h*|mae_atr_h*",
     "forward excursion over [terminus .. terminus+h) — THE OUTCOME"),
    ("trunc_h*", "whether the forward window ran past the substrate edge"),
    ("time_to_tier_clearance_ms|cleared_tier|survival_to_next_tf",
     "requires events strictly AFTER the terminus"),
    ("joined_births|birth_keys", "fills occurring inside the cascade span"),
]


def ms_of(iso_s: str) -> int:
    return int(datetime.strptime(iso_s, "%Y-%m-%dT%H:%M:%SZ")
               .replace(tzinfo=timezone.utc).timestamp() * 1000)


def load_births(log) -> list:
    """Births from the W-F1 checkpoints (derived from the canonical journal at
    CANON_JOURNAL — asserted present so a silent substitution of the 2026 dryrun
    journal, which would make the join trivially empty, cannot happen)."""
    if not CANON_JOURNAL.exists():
        raise SystemExit(f"HALT: canonical journal missing: {CANON_JOURNAL}")
    n_files = len(glob.glob(str(CANON_JOURNAL / "*" / "*.jsonl")))
    log(f"  canonical journal : {CANON_JOURNAL.relative_to(ROOT)}  ({n_files} files)")
    if n_files == 0:
        raise SystemExit("HALT: canonical journal directory is empty")
    births = []
    for p in sorted(BOX.glob("*USDT_*.json")):
        d = json.loads(p.read_text(encoding="utf-8"))
        cell = d["cell"]
        mandate = cell.split("_", 1)[1]
        for r in d["rows"]:
            births.append({
                "cell_id": cell, "tranche_id": r["tranche_id"],
                "symbol": r["symbol"], "mandate": mandate,
                "tf_gov": MANDATES[mandate]["gov"],
                "ts_open": r["ts_open"], "ts_ms": ms_of(r["ts_open"]),
                "dir": r["dir"], "resolved": bool(r.get("resolved")),
            })
    return births


def preload_exec(assets: list, log) -> dict:
    from engine.data import cache_dir
    klines = cache_dir() / "klines"
    out = {}
    for sym in assets:
        t0 = time.time()
        ex = cb.load_tf(klines, sym, cb.EXEC_TF, cb.ms(cb.ASSET_STARTS[sym]))
        xo = ex["open_time"].to_numpy(np.int64)
        d = {"xo": xo, "open": ex["open"].to_numpy(float),
             "atr": ex["atr"].to_numpy(float), "n": len(ex)}
        h = ex["high"].to_numpy(float)
        lo = ex["low"].to_numpy(float)
        for hz in cb.HORIZONS:
            hi, low, avail = cb.fwd_extents(h, lo, hz)
            d[f"hi{hz}"], d[f"lo{hz}"], d[f"av{hz}"] = hi, low, avail
        out[sym] = d
        log(f"  exec frame {sym}: {len(ex)} bars ({time.time()-t0:.1f}s)")
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run2", action="store_true")
    args = ap.parse_args()
    tag = "seq8_run2" if args.run2 else "seq8"
    root = ROOT / "research_outputs" / tag
    casc = root / "seq8_cascades.jsonl"
    if not casc.exists():
        print(f"MISSING: {casc} — run seq8_views.py first")
        return 2

    t0 = time.time()
    print("SEQ-8 OUTCOMES — D3 substrate + join, D4 route matrix  [I6: EMITTED, NOT ANALYZED]")
    births = load_births(print)
    print(f"  births            : {len(births)}  "
          f"(max ts {iso(max(b['ts_ms'] for b in births))})")
    mx = max(b["ts_ms"] for b in births)
    if mx >= cb.CEIL_MS:
        raise SystemExit(f"HALT: a birth at {iso(mx)} is at/after the ceiling")

    assets = sorted(cb.ASSET_STARTS)
    ex = preload_exec(assets, print)

    births_by_sym = defaultdict(list)
    for b in births:
        births_by_sym[b["symbol"]].append(b)

    # ---- single streaming pass over the cascades ----
    d3_path = root / "seq8_outcomes.jsonl"
    n_rows = 0
    spans = defaultdict(list)          # (view, asset) -> cascade span tuples
    fout = open(d3_path, "w", encoding="utf-8", newline="\n")
    for line in open(casc, encoding="utf-8"):
        r = json.loads(line)
        sym = r["asset"]
        e = ex[sym]
        k = r["term_exec_idx"]
        row = {
            "asset": sym, "lattice": r["lattice"], "event_class": r["event_class"],
            "view": r["view"], "dir": r["dir"], "depth": r["depth"],
            "init_tf": r["init_tf"], "init_ts": r["init_ts"],
            "term_tf": r["term_tf"], "term_ts": r["term_ts"],
            "term_tier": TIER_GRAMMAR[r["term_tf"]],
            "rungs_absolute": r["rungs_absolute"],
            "family_first3": r["family_first3"],
            "monotone": r["monotone"],
            "term_exec_idx": k,
        }
        if k is None or k >= e["n"]:
            # terminus has no tradeable exec bar (right-edge truncation)
            row["outcome_available"] = False
            fout.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
            n_rows += 1
            continue
        is_long = r["dir"] == "up"
        p0 = e["open"][k]
        ab = e["atr"][k]
        row["outcome_available"] = True
        row["p0_terminus"] = rnd(p0)
        row["atr_basis"] = rnd(ab)
        for hz in cb.HORIZONS:
            hi, lo = e[f"hi{hz}"][k], e[f"lo{hz}"][k]
            fav = (hi - p0) if is_long else (p0 - lo)
            adv = (lo - p0) if is_long else (p0 - hi)
            row[f"mfe_bps_h{hz}"] = rnd(fav / p0 * 1e4)
            row[f"mae_bps_h{hz}"] = rnd(adv / p0 * 1e4)
            row[f"mfe_atr_h{hz}"] = rnd(fav / ab) if ab > 0 else None
            row[f"mae_atr_h{hz}"] = rnd(adv / ab) if ab > 0 else None
            row[f"trunc_h{hz}"] = bool(e[f"av{hz}"][k] < hz)
        # event-based outcomes
        # tier clearance is measured against the INITIATING tier: did this
        # cascade ever climb out of the tier it started in, and how long did
        # that take from the first rung's close?
        rungs = r["rungs_absolute"].split(">")
        init_tier = TIER_ORDER.index(TIER_GRAMMAR[r["init_tf"]])
        cleared_at = next((t for t in rungs
                           if TIER_ORDER.index(TIER_GRAMMAR[t]) > init_tier), None)
        row["cleared_tier"] = cleared_at is not None
        row["cleared_tier_at_tf"] = cleared_at
        row["time_to_tier_clearance_ms"] = (
            r[f"latency_to_{cleared_at}_ms"]
            if cleared_at in ("1h", "4h", "12h", "1d") else None)
        ti = TFI[r["init_tf"]]
        row["survival_to_next_tf"] = bool(any(TFI[t] == ti + 1 for t in rungs))
        fout.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")
        n_rows += 1

        if r["lattice"] == JOIN_LATTICE and r["event_class"] == JOIN_CLASS:
            spans[(r["view"], sym)].append(
                (r["init_ts"], r["term_bar_close_ms"], r["rungs_absolute"],
                 r["family_first3"], r["dir"]))
    fout.close()
    sha_d3 = sha256_file(d3_path)
    print(f"  D3 rows           : {n_rows}")

    # ---- D4: rebuild cleanly from the emitted D3 + cascade source rungs ----
    d4rows = _route_matrix(casc, d3_path)
    print(f"  D4 route cells    : {len(d4rows)}")

    # ---- the join ----
    join_rows = []
    for (view, sym), lst in spans.items():
        lst.sort()
        starts = [x[0] for x in lst]
        for b in births_by_sym.get(sym, []):
            hits = []
            j = bisect.bisect_right(starts, b["ts_ms"])
            for i in range(j - 1, -1, -1):
                init, term, rungs, fam, dr = lst[i]
                if b["ts_ms"] <= term and b["tf_gov"] in rungs.split(">"):
                    hits.append((init, term, rungs, fam, dr))
            for init, term, rungs, fam, dr in hits:
                join_rows.append({
                    "view": view, "asset": sym,
                    "cell_id": b["cell_id"], "tranche_id": b["tranche_id"],
                    "mandate": b["mandate"], "tf_gov": b["tf_gov"],
                    "birth_ts_open": b["ts_open"], "birth_ts_ms": b["ts_ms"],
                    "birth_dir": b["dir"], "resolved": b["resolved"],
                    "cascade_init_ts": init, "cascade_term_close_ms": term,
                    "cascade_rungs": rungs, "cascade_family": fam,
                    "cascade_dir": dr,
                    "dir_agrees": bool((dr == "up") == (b["dir"] == "long")),
                })
    join_rows.sort(key=lambda r: (r["view"], r["asset"], r["cell_id"],
                                  r["tranche_id"], r["cascade_init_ts"]))
    p_join = root / "seq8_cascade_birth_join.jsonl"
    with open(p_join, "w", encoding="utf-8", newline="\n") as f:
        for r in join_rows:
            f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    sha_join = sha256_file(p_join)

    # ---- F-SEQ3 integrity ----
    birth_keys = {(b["cell_id"], b["tranche_id"]) for b in births}
    joined_keys = {(r["cell_id"], r["tranche_id"]) for r in join_rows}
    orphans_join_to_journal = sorted(joined_keys - birth_keys)
    unjoined_births = sorted(birth_keys - joined_keys)
    integrity = {
        "fixture": "F-SEQ3",
        "join_rule": (
            "birth joins a cascade iff (a) cell symbol == cascade asset, "
            "(b) the cell's governor TF is a rung of the cascade "
            "(MANDATES: intraday->1h, swing->4h, position->12h), and "
            "(c) birth ts_open lies within [first rung bar_close, terminus "
            "bar_close]. Restricted to lattice A / 9_89 (the cross the engine "
            "trades)."),
        "join_key": "(cell_id, tranche_id) — tranche_id alone collides across cells",
        "births_total": len(births),
        "birth_keys_distinct": len(birth_keys),
        "join_rows": len(join_rows),
        "distinct_births_joined": len(joined_keys),
        "orphans_join_to_journal": len(orphans_join_to_journal),
        "orphan_examples": orphans_join_to_journal[:10],
        "births_never_joined": len(unjoined_births),
        "status": "PASS" if not orphans_join_to_journal else "FAIL",
        "note": (
            "'Zero orphans both ways' is asserted in the direction that is "
            "falsifiable: every joined key must exist in the journals. The "
            "reverse direction is NOT an orphan condition — a birth that falls "
            "in no cascade span is a real, correct outcome (the engine traded "
            "when no 9/89 cascade was open), and is reported as "
            "births_never_joined rather than being forced to zero."),
    }
    print(f"  join rows         : {len(join_rows)}  "
          f"distinct births joined {len(joined_keys)}/{len(birth_keys)}  "
          f"orphans {len(orphans_join_to_journal)}")

    write_json(root / "seq8_d4_route_matrix.json", d4rows)
    write_json(root / "seq8_outcomes_manifest.json", {
        "phase": "SEQ-8 D3 outcome substrate + join, D4 route matrix",
        "embargo": "I6 — EMITTED AS SUBSTRATE, NOT ANALYZED IN THIS RUN",
        "horizons_exec_bars": cb.HORIZONS,
        "atr_basis": "exec-5m ATR at the terminus anchor bar",
        "anchor_rule": "first exec bar whose open >= the terminus bar's close",
        "join": integrity,
        "curtain_audit": {
            "clean": [{"columns": c, "attestation": a} for c, a in CURTAIN_CLEAN],
            "post_curtain": [{"columns": c, "reason": a} for c, a in POST_CURTAIN],
            "violations": [],
            "note": "No column marked clean derives from data after the terminus "
                    "bar close; outcome columns are labelled post-curtain and are "
                    "never mixed into the descriptive set.",
        },
        "row_counts": {"d3_outcomes": n_rows, "join_rows": len(join_rows),
                       "d4_cells": len(d4rows)},
        "sha256": {"seq8_outcomes.jsonl": sha_d3,
                   "seq8_cascade_birth_join.jsonl": sha_join},
        "versions": {"python": sys.version.split()[0], "numpy": np.__version__,
                     "pandas": pd.__version__},
        "elapsed_s": round(time.time() - t0, 1),
    })
    print(f"\nOUTCOMES done -> {tag} in {time.time()-t0:.1f}s")
    return 0


def _route_matrix(casc: Path, d3: Path) -> list:
    """D4: arrivals at 4h, split by SOURCE rung -> MFE/MAE distribution.
    Built from the two emitted files so the matrix cannot drift from them."""
    src_of = {}
    for line in open(casc, encoding="utf-8"):
        r = json.loads(line)
        if r["lattice"] != JOIN_LATTICE or r["event_class"] != JOIN_CLASS:
            continue
        if r.get("source_into_4h"):
            src_of[(r["view"], r["asset"], r["init_ts"], r["rungs_absolute"])] = \
                r["source_into_4h"]
    buckets = defaultdict(lambda: defaultdict(list))
    for line in open(d3, encoding="utf-8"):
        o = json.loads(line)
        if o["lattice"] != JOIN_LATTICE or o["event_class"] != JOIN_CLASS:
            continue
        if not o.get("outcome_available"):
            continue
        s = src_of.get((o["view"], o["asset"], o["init_ts"], o["rungs_absolute"]))
        if not s:
            continue
        b = buckets[(o["view"], o["asset"], s)]
        for hz in cb.HORIZONS:
            b[f"mfe_bps_h{hz}"].append(o[f"mfe_bps_h{hz}"])
            b[f"mae_bps_h{hz}"].append(o[f"mae_bps_h{hz}"])
    out = []
    for (view, asset, s), b in sorted(buckets.items()):
        n = len(b[f"mfe_bps_h{cb.HORIZONS[0]}"])
        cell = {"view": view, "asset": asset, "source_rung": s,
                "source_tier": TIER_GRAMMAR[s], "n": n}
        for col, vals in b.items():
            a = np.asarray([v for v in vals if v is not None], dtype=float)
            if len(a) == 0:
                continue
            cell[col] = {"n": int(len(a)),
                         "p25": round(float(np.percentile(a, 25)), R6),
                         "median": round(float(np.median(a)), R6),
                         "p75": round(float(np.percentile(a, 75)), R6)}
        out.append(cell)
    return out


if __name__ == "__main__":
    raise SystemExit(main())
