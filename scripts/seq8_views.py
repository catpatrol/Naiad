"""SEQ-8 — D2 cascade views (derived, never baked) + D5 arrivals panel.

Contract: exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md
Reads:  research_outputs/seq8/seq8_events.jsonl   (D1, produced by seq8_extract.py)
Emits:  research_outputs/seq8/seq8_cascades.jsonl (D2 rows, all 8 views)
        research_outputs/seq8/seq8_views_summary.json (per-view summary +
                                                       cross-view agreement)
        research_outputs/seq8/seq8_arrivals.json (D5 panel, scores P-SEQ-ii)

WHY THIS FILE IS SEPARATE FROM THE OUTCOME SUBSTRATE
  I6 embargoes analysis of the outcome-bearing tables (D3, D4) but requires
  P-SEQ-ii (D5) be SCORED this run. D5 is pure counts and touches no outcome
  column, so keeping it in a file that never opens an MFE/MAE array makes the
  embargo structural rather than a promise.

THE EIGHT VIEWS (D2) — chaining is a PARAMETER, never a property of the data
  windows {24h, 48h, 72h, 1W} x rules {window-chained, direction-consistent}.
  A cascade is built from D1 atoms at read time; D1 itself carries no chain.
  That is the SEQ-1 ruling's whole point: any future definition of "a cascade"
  recomputes from D1 without re-extraction.

  window-chained      : consecutive same-direction events on NEW timeframes,
                        each within `window` of the previously admitted rung.
  direction-consistent: identical, but a counter-direction event of the same
                        class ENDS the cascade where it occurs.

  Chaining is on `bar_close_ms` — the instant a cross becomes knowable — never
  on bar open. Using open would chain on information not yet available (F-SEQ5).

RUNG FRAMES (SEQ-2 ruling D: all three counted, none primary)
  absolute       "5m>15m>4h"                — the operator's reading preference
  gov_relative   "0>+1>+4"                  — steps on the 7-TF ladder from the
                                              initiating rung (the transferable
                                              frame; LEDGER C-2 dual coordinates)
  tier           "FAST>FAST>SLOW"           — see TIER_GRAMMAR below

TIER GRAMMAR IS DEFINED HERE BECAUSE NOTHING IN THE REPO DEFINES IT.
  Searched: no "tier grammar" definition, no named tiers, no mapping in any
  script, contract or ledger entry. It is therefore constructed from the only
  authority that exists — the operator's own named regions in the SEQ-2 ruling
  ("30m-chop · 1H-stair · 4h-12h-slow", SESSION_SUMMARY_DIONYSUS_2026-08-04)
  plus Q1c's trend tier (memory Entry 19: "trend tier 1D/1W/1M, build tier
  12H-5m"). Reported as a builder definition, not presented as inherited.
  It is also exactly what makes "leap" mean what the Atlas says it means:
  FAST -> SLOW skipping STAIR.

D5 / P-SEQ-ii USES THE ATLAS'S OWN ARRIVAL VOCABULARY, recovered verbatim from
`Cascade Rewire.html` drawArrivals(): an ARRIVAL is a transition read at its
destination; ADJACENT is `TFS.index(src) == TFS.index(dest) - 1`; a LEAP is a
source two or more ladder positions below. Redefining them would have made the
replication vacuous.

Usage:
  python scripts/seq8_views.py
  python scripts/seq8_views.py --run2
"""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as cb                                   # noqa: E402
from seq8_extract import iso, write_json                    # noqa: E402

H = 3_600_000
WINDOWS = {"24h": 24 * H, "48h": 48 * H, "72h": 72 * H, "1W": 168 * H}
RULES = ["window_chained", "direction_consistent"]
VIEWS = [f"{w}|{r}" for w in WINDOWS for r in RULES]        # 8 views

TFI = {tf: i for i, tf in enumerate(cb.TFS)}                # 5m=0 … 1d=6

# See module docstring — constructed, not inherited. Provenance in the report.
TIER_GRAMMAR = {"5m": "FAST", "15m": "FAST", "30m": "FAST",
                "1h": "STAIR", "4h": "SLOW", "12h": "SLOW", "1d": "TREND"}

ARRIVAL_LENSES = ["1h", "4h", "12h", "1d"]
# P-SEQ-ii, verbatim from the contract §3 D5:
#   "the leap (arrival at 4h directly from <=30m) is the dominant 4h activation
#    mode, and 1h arrivals are predominantly adjacent"
P_SEQ_II_PRIOR = 0.75
REPLICATION_BAR = 5          # sign-consistent on >= 5 of the 7 census assets
FAST_TIER = {"5m", "15m", "30m"}


def sha256_file(p: Path) -> str:
    """Chunked — these artifacts run to hundreds of MB and read_bytes() fails
    outright on Windows past a certain size (census1b_det.sha256_file pattern)."""
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def sig_first3(rungs: list) -> str:
    return ">".join(rungs[:3])


def family(rungs: list) -> str:
    """Rewire famOf(), on the first-3-rung signature only (offset 222906):
    leap iff monotone and seq[2] in {4h,12h}; drift iff monotone and seq[2]=1d;
    grind iff monotone and both steps adjacent; skip iff otherwise monotone;
    shuffle iff not monotone."""
    if len(rungs) < 3:
        return "under3"
    a, b, c = (TFI[t] for t in rungs[:3])
    mono = a < b < c
    if not mono:
        return "shuffle"
    if rungs[2] in ("4h", "12h"):
        return "leap"
    if rungs[2] == "1d":
        return "drift"
    if b - a == 1 and c - b == 1:
        return "grind"
    return "skip"


def build_cascades(evs: list, window_ms: int, rule: str) -> list:
    """Greedy, deterministic, non-overlapping chaining over one (asset, class)
    event sequence already sorted by (bar_close_ms, tf_idx, dir).

    Each admitted rung must be a NEW timeframe: a cascade is a ladder across
    timeframes, one rung per TF (max depth 7). Re-firings on a TF already in the
    chain do not extend it and remain available to start their own cascade.
    """
    n = len(evs)
    used = [False] * n
    out = []
    for i in range(n):
        if used[i]:
            continue
        e0 = evs[i]
        members = [i]
        tfs = {e0["tf"]}
        last = e0["bar_close_ms"]
        ended_by = None
        j = i + 1
        while j < n:
            f = evs[j]
            if f["bar_close_ms"] - last > window_ms:
                break
            if rule == "direction_consistent" and f["dir"] != e0["dir"]:
                ended_by = j                      # counter-direction terminator
                break
            if f["dir"] == e0["dir"] and f["tf"] not in tfs:
                members.append(j)
                tfs.add(f["tf"])
                last = f["bar_close_ms"]
            j += 1
        for m in members:
            used[m] = True
        out.append((members, ended_by))
    return out


def cascade_row(asset, lattice, klass, view, members, ended_by, evs) -> dict:
    ms_ = [evs[m] for m in members]
    rungs = [e["tf"] for e in ms_]
    idxs = [TFI[t] for t in rungs]
    init = idxs[0]
    closes = [e["bar_close_ms"] for e in ms_]
    sojourn_ms = [closes[k + 1] - closes[k] for k in range(len(closes) - 1)]
    monotone = all(idxs[k] < idxs[k + 1] for k in range(len(idxs) - 1))
    row = {
        "asset": asset, "lattice": lattice, "event_class": klass, "view": view,
        "dir": ms_[0]["dir"],
        "depth": len(ms_),
        "init_tf": rungs[0], "init_ts": ms_[0]["ts"],
        "init_ts_iso": iso(ms_[0]["ts"]),
        "term_tf": rungs[-1], "term_ts": ms_[-1]["ts"],
        "term_bar_close_ms": closes[-1],
        "term_exec_idx": ms_[-1]["exec_idx"],
        "span_ms": closes[-1] - closes[0],
        # all three frames, depth-complete — no 3-rung truncation (D2)
        "rungs_absolute": ">".join(rungs),
        "rungs_gov_relative": ">".join(
            ("0" if d == 0 else f"{d:+d}") for d in (i - init for i in idxs)),
        "rungs_tier": ">".join(TIER_GRAMMAR[t] for t in rungs),
        "monotone": monotone,
        "shuffle": not monotone,
        "family_first3": family(rungs),
        "sig_first3": sig_first3(rungs),
        "sojourn_ms": sojourn_ms,
        "sojourn_exec_bars": [s // cb.TF_MS["5m"] for s in sojourn_ms],
        "ended_by_counter_dir": ended_by is not None,
        "event_ts": [e["ts"] for e in ms_],
    }
    # leap latency — time from the initiating rung to the first arrival at each
    # governor lens, when the cascade reaches it at all.
    for lens in ARRIVAL_LENSES:
        if lens in rungs:
            k = rungs.index(lens)
            row[f"latency_to_{lens}_ms"] = closes[k] - closes[0]
            row[f"source_into_{lens}"] = rungs[k - 1] if k > 0 else None
        else:
            row[f"latency_to_{lens}_ms"] = None
            row[f"source_into_{lens}"] = None
    return row


def classify_arrival(src: str | None, dest: str) -> str:
    """Rewire drawArrivals() vocabulary, unchanged."""
    if src is None:
        return "initiating"
    ds, dd = TFI[src], TFI[dest]
    if ds == dd - 1:
        return "adjacent"
    if ds < dd - 1:
        return "leap"
    return "from_above"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--run2", action="store_true")
    args = ap.parse_args()
    tag = "seq8_run2" if args.run2 else "seq8"
    root = ROOT / "research_outputs" / tag
    src = root / "seq8_events.jsonl"
    if not src.exists():
        print(f"MISSING: {src} — run seq8_extract.py first")
        return 2

    t0 = time.time()
    print("SEQ-8 VIEWS — D2 cascade views + D5 arrivals panel")
    print(f"  reading  : {src}")
    print(f"  views    : {len(VIEWS)} = {list(WINDOWS)} x {RULES}")
    print(f"  tiers    : {TIER_GRAMMAR}")

    # ---- load D1 atoms (only the fields chaining needs) ----
    groups = defaultdict(list)
    n_ev = 0
    with open(src, encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            n_ev += 1
            groups[(r["asset"], r["lattice"], r["event_class"])].append({
                "tf": r["tf"], "dir": r["dir"], "ts": r["ts"],
                "bar_close_ms": r["bar_close_ms"], "exec_idx": r["exec_idx"],
            })
    for k in groups:
        groups[k].sort(key=lambda e: (e["bar_close_ms"], TFI[e["tf"]], e["dir"]))
    print(f"  atoms    : {n_ev} events in {len(groups)} (asset,lattice,class) groups")

    # ---- D2 ----
    rows = []
    singletons = Counter()
    per_view = defaultdict(lambda: {"n_cascades": 0, "n_singletons": 0,
                                    "depth_hist": Counter(), "monotone": 0,
                                    "family": Counter()})
    # event -> depth/rung-string per view, for the cross-view agreement table
    membership = {v: {} for v in VIEWS}

    for (asset, lattice, klass), evs in sorted(groups.items()):
        for w, wms in WINDOWS.items():
            for rule in RULES:
                view = f"{w}|{rule}"
                for members, ended_by in build_cascades(evs, wms, rule):
                    key0 = (asset, lattice, klass)
                    if len(members) < 2:
                        # A 1-rung cascade adds nothing over the D1 atom it
                        # contains. Counted here and reported in the summary —
                        # NOT silently dropped (no silent caps).
                        singletons[(view,) + key0] += 1
                        per_view[view]["n_singletons"] += 1
                        e = evs[members[0]]
                        membership[view][(asset, lattice, klass, e["ts"], e["tf"])] = (1, e["tf"])
                        continue
                    row = cascade_row(asset, lattice, klass, view,
                                      members, ended_by, evs)
                    rows.append(row)
                    pv = per_view[view]
                    pv["n_cascades"] += 1
                    pv["depth_hist"][row["depth"]] += 1
                    pv["monotone"] += int(row["monotone"])
                    pv["family"][row["family_first3"]] += 1
                    for m in members:
                        e = evs[m]
                        membership[view][(asset, lattice, klass, e["ts"], e["tf"])] = (
                            row["depth"], row["rungs_absolute"])

    print(f"  D2       : {len(rows)} cascades (depth>=2) across {len(VIEWS)} views; "
          f"{sum(singletons.values())} singletons counted, not emitted")

    # ---- cross-view agreement (D2: "how much do the 8 definitions disagree") --
    agreement = []
    for a, b in itertools.combinations(VIEWS, 2):
        ma, mb = membership[a], membership[b]
        common = ma.keys() & mb.keys()
        same_depth = sum(1 for k in common if ma[k][0] == mb[k][0])
        same_str = sum(1 for k in common if ma[k][1] == mb[k][1])
        agreement.append({
            "view_a": a, "view_b": b, "events_compared": len(common),
            "same_depth_pct": round(100.0 * same_depth / len(common), 3) if common else None,
            "same_rung_string_pct": round(100.0 * same_str / len(common), 3) if common else None,
        })

    # ---- D5 arrivals panel + P-SEQ-ii ----
    # counts only: no outcome column is opened anywhere in this file.
    #
    # TWO FRAMES, and the distinction is the finding.
    #   trunc3        — the Atlas's own frame: the arrival source is read off the
    #                   first THREE rungs only. P-SEQ-ii is a REPLICATION claim
    #                   about a finding made in this frame, so this is the frame
    #                   that scores it. Scoring only the other frame would test a
    #                   different proposition and call it a replication.
    #   depth_complete— the contract's D2 requirement (no 3-rung truncation).
    #                   Reported beside it because the two disagree, and the
    #                   disagreement is what the operator asked D2 to expose.
    FRAMES = ["trunc3", "depth_complete"]
    arrivals = defaultdict(Counter)
    for r in rows:
        rungs = r["rungs_absolute"].split(">")
        for frame in FRAMES:
            rr = rungs[:3] if frame == "trunc3" else rungs
            for lens in ARRIVAL_LENSES:
                if lens not in rr:
                    continue
                k = rr.index(lens)
                s = rr[k - 1] if k > 0 else None
                key = (frame, r["view"], r["lattice"], r["event_class"],
                       r["asset"], lens)
                arrivals[key][classify_arrival(s, lens)] += 1
                if lens == "4h" and s is not None:
                    arrivals[key]["leap_from_fast" if s in FAST_TIER
                                  else "not_leap_from_fast"] += 1

    panel = []
    for key, c in sorted(arrivals.items(), key=lambda kv: [str(x) for x in kv[0]]):
        frame, view, lattice, klass, asset, lens = key
        tot = c["adjacent"] + c["leap"] + c["from_above"] + c["initiating"]
        panel.append({
            "frame": frame, "view": view, "lattice": lattice,
            "event_class": klass, "asset": asset, "lens": lens,
            "n_arrivals": tot,
            "adjacent": c["adjacent"], "leap": c["leap"],
            "from_above": c["from_above"], "initiating": c["initiating"],
            "leap_from_fast": c["leap_from_fast"] or None,
            "not_leap_from_fast": c["not_leap_from_fast"] or None,
            "adjacent_pct": round(100.0 * c["adjacent"] / tot, 3) if tot else None,
            "leap_pct": round(100.0 * c["leap"] / tot, 3) if tot else None,
        })

    # Scoring. Two limbs, both pure counts, both scored per view x lattice x class.
    #   limb A (4h)  : leap is the DOMINANT 4h activation mode  -> leap > adjacent
    #                  and leap is the largest single category.
    #   limb B (1h)  : 1h arrivals are PREDOMINANTLY adjacent   -> adjacent is the
    #                  largest single category.
    # An asset counts toward replication only if it has arrivals to score; assets
    # with n=0 are reported as unscorable rather than silently counted as failures.
    scores = []
    for (frame, view, lattice, klass) in sorted(
            {(p["frame"], p["view"], p["lattice"], p["event_class"]) for p in panel}):
        limb = {}
        for lens, test in (("4h", "leap"), ("1h", "adjacent")):
            rowsl = [p for p in panel if p["frame"] == frame and p["view"] == view
                     and p["lattice"] == lattice
                     and p["event_class"] == klass and p["lens"] == lens]
            scorable, agree, detail = 0, 0, {}
            for p in rowsl:
                cats = {"adjacent": p["adjacent"], "leap": p["leap"],
                        "from_above": p["from_above"], "initiating": p["initiating"]}
                # 'initiating' is not an activation ROUTE — a cascade that starts
                # at the lens arrived from nowhere. Excluded from the mode test,
                # reported separately.
                cats.pop("initiating")
                n = sum(cats.values())
                if n == 0:
                    detail[p["asset"]] = "unscorable(n=0)"
                    continue
                scorable += 1
                top = max(cats, key=lambda k: (cats[k], k))
                ok = (top == test)
                agree += int(ok)
                detail[p["asset"]] = f"{'YES' if ok else 'no'} ({test}={cats[test]}/{n})"
            limb[lens] = {"test": f"{test} is the largest arrival category at {lens}",
                          "assets_scorable": scorable, "assets_agreeing": agree,
                          "bar": REPLICATION_BAR, "per_asset": detail,
                          "replicates": bool(agree >= REPLICATION_BAR)}
        scores.append({
            "frame": frame,
            "view": view, "lattice": lattice, "event_class": klass,
            "limb_A_4h_leap_dominant": limb["4h"],
            "limb_B_1h_adjacent_dominant": limb["1h"],
            "P_SEQ_ii_replicates": bool(limb["4h"]["replicates"]
                                        and limb["1h"]["replicates"]),
        })

    # ---- emit ----
    rows.sort(key=lambda r: (r["view"], r["asset"], r["lattice"], r["event_class"],
                             r["init_ts"], r["init_tf"]))
    p_casc = root / "seq8_cascades.jsonl"
    with open(p_casc, "w", encoding="utf-8", newline="\n") as f:
        for r in rows:
            f.write(json.dumps(r, sort_keys=True, separators=(",", ":")) + "\n")
    sha_casc = sha256_file(p_casc)

    summary = {
        "views": VIEWS,
        "windows_ms": WINDOWS,
        "rules": RULES,
        "tier_grammar": TIER_GRAMMAR,
        "tier_grammar_provenance":
            "CONSTRUCTED BY THE BUILDER — no tier-grammar definition exists in "
            "the repo. Built from the operator's named regions in the SEQ-2 "
            "ruling (30m-chop / 1H-stair / 4h-12h-slow, "
            "SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md) plus Q1c's "
            "trend tier (memory Entry 19). Reported, not inherited.",
        "chaining_clock": "bar_close_ms (the instant a cross becomes knowable)",
        "per_view": {v: {"n_cascades": d["n_cascades"],
                         "n_singletons": d["n_singletons"],
                         "monotone_pct": (round(100.0 * d["monotone"] / d["n_cascades"], 3)
                                          if d["n_cascades"] else None),
                         "depth_hist": {str(k): v2 for k, v2 in sorted(d["depth_hist"].items())},
                         "family_first3": dict(sorted(d["family"].items()))}
                     for v, d in sorted(per_view.items())},
        "cross_view_agreement": agreement,
        "row_counts": {"cascades_depth_ge_2": len(rows),
                       "singletons_counted_not_emitted": sum(singletons.values())},
        "sha256": {"seq8_cascades.jsonl": sha_casc},
        "elapsed_s": round(time.time() - t0, 1),
    }
    write_json(root / "seq8_views_summary.json", summary)

    write_json(root / "seq8_arrivals.json", {
        "claim_id": "P-SEQ-ii",
        "claim": "the leap (arrival at 4h directly from <=30m) is the dominant 4h "
                 "activation mode, and 1h arrivals are predominantly adjacent",
        "proposed_prior": P_SEQ_II_PRIOR,
        "replication_bar": f">= {REPLICATION_BAR} of the 7 census assets, per lens",
        "definitions_source":
            "Cascade Rewire.html drawArrivals(): arrival read at destination; "
            "adjacent iff TFS.index(src) == TFS.index(dest)-1; leap iff src is "
            ">=2 ladder positions below.",
        "frames": {
            "trunc3": "Atlas frame — arrival source read off the first 3 rungs "
                      "only. THIS FRAME SCORES THE REPLICATION, because the "
                      "finding P-SEQ-ii replicates was made in it.",
            "depth_complete": "Contract D2 frame — full rung string, no "
                              "truncation. Reported beside trunc3; where the two "
                              "disagree, the disagreement is the finding.",
        },
        "scoring_frame": "trunc3",
        "outcome_free": True,
        "panel": panel,
        "scores": scores,
    })

    print(f"\nVIEWS done -> {tag} in {time.time() - t0:.1f}s")
    print(f"  cascades {len(rows)}   panel rows {len(panel)}   "
          f"agreement pairs {len(agreement)}")
    ref = "48h|window_chained"
    pv = summary["per_view"].get(ref)
    if pv:
        print(f"  reference view {ref}: n={pv['n_cascades']} "
              f"monotone={pv['monotone_pct']}%")
    for s in scores:
        if s["lattice"] == "A" and s["event_class"] == "9_89" and s["view"] == ref:
            print(f"  P-SEQ-ii @ {ref} A/9_89 [{s['frame']:14}]: "
                  f"4h-leap {s['limb_A_4h_leap_dominant']['assets_agreeing']}"
                  f"/{s['limb_A_4h_leap_dominant']['assets_scorable']}  "
                  f"1h-adjacent {s['limb_B_1h_adjacent_dominant']['assets_agreeing']}"
                  f"/{s['limb_B_1h_adjacent_dominant']['assets_scorable']}  "
                  f"-> {'REPLICATES' if s['P_SEQ_ii_replicates'] else 'DOES NOT REPLICATE'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
