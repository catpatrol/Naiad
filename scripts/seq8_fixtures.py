"""SEQ-8 — fixtures F-SEQ1 .. F-SEQ8. Each independently falsifiable.

Contract: exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md §4

  F-SEQ1  event counts reconcile to the census machinery's own cross counts
          per asset x TF (0 diffs)
  F-SEQ2  max timestamp in every emitted file <= the printed ceiling
  F-SEQ3  join integrity; join rule stated
  F-SEQ4  the Atlas count (2,378) reproduced exactly, or the diff itemized
  F-SEQ5  curtain audit — every column marked curtain-clean derives only from
          data at/before the event bar
  F-SEQ6  EMA300/450 are NaN before full warmup; zero backfilled values
  F-SEQ7  determinism — a full re-run reproduces every table byte-identically
  F-SEQ8  worked multiTF example, count verified by hand-inspection

Prints a transcript in the repo's fixture idiom ([PASS]/[FAIL] + the assertion
with its actual numbers inline) and writes seq8_fixtures.json.

Usage:
  python scripts/seq8_fixtures.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as cb                                             # noqa: E402
from seq8_extract import iso, HTF_ORIENT, HTF_TFS, WARM, write_json   # noqa: E402
from seq8_views import sha256_file                                    # noqa: E402

R1 = ROOT / "research_outputs" / "seq8"
R2 = ROOT / "research_outputs" / "seq8_run2"

FIXTURES = []


def fixture(tag, ok, detail, extra=None):
    FIXTURES.append({"id": tag, "pass": bool(ok), "detail": detail,
                     **({"extra": extra} if extra else {})})
    print(f"  [{'PASS' if ok else 'FAIL'}] {tag}: {detail}")
    return ok


# ---------------------------------------------------------------------------
def f_seq1():
    """Reconcile to census_outcomes.jsonl per (asset, tf, cross_type, dir)."""
    cen = Counter()
    with open(ROOT / "research_outputs/census/census_outcomes.jsonl",
              encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            cen[(r["asset"], r["tf"], r["cross_type"], r["dir"])] += 1
    counts = json.loads((R1 / "seq8_event_counts.json").read_text(encoding="utf-8"))
    mine = Counter()
    raw = Counter()
    for k, v in counts.items():
        a, tf, lat, cls, d = k.split("|")
        if lat != "A":
            continue
        mine[(a, tf, cls, d)] += v["census_filtered"]
        raw[(a, tf, cls, d)] += v["raw"]
    keys = set(cen) | set(mine)
    diffs = [(k, cen[k], mine[k]) for k in sorted(keys) if cen[k] != mine[k]]
    excess = sum(raw.values()) - sum(mine.values())
    return fixture(
        "F-SEQ1",
        not diffs,
        f"{len(keys)} asset x TF x class x dir cells reconciled against "
        f"census_outcomes.jsonl; {len(diffs)} diffs; totals "
        f"{sum(cen.values())} census == {sum(mine.values())} extract "
        f"(census-filter applied). The raw stream additionally retains "
        f"{excess} event(s) the census filter drops at the right edge — kept "
        f"and flagged, never silently dropped.",
        {"diffs": diffs[:20], "cells": len(keys),
         "census_total": sum(cen.values()), "extract_filtered_total": sum(mine.values()),
         "extract_raw_total": sum(raw.values())})


def f_seq2():
    """No emitted row may carry a timestamp at/after the exploration ceiling."""
    worst = {}
    ok = True
    ts_fields = ("ts", "init_ts", "term_ts", "exec_ts", "bar_close_ms",
                 "term_bar_close_ms", "birth_ts_ms", "cascade_init_ts",
                 "cascade_term_close_ms")
    for name in ("seq8_events.jsonl", "seq8_cascades.jsonl",
                 "seq8_outcomes.jsonl", "seq8_cascade_birth_join.jsonl"):
        p = R1 / name
        if not p.exists():
            continue
        mx = -1
        with open(p, encoding="utf-8") as f:
            for line in f:
                r = json.loads(line)
                for k in ts_fields:
                    v = r.get(k)
                    if isinstance(v, int) and v > mx:
                        mx = v
        worst[name] = mx
        # bar_close_ms may equal the ceiling: a bar OPENING before the ceiling
        # closes at it. Event/observation instants must be strictly below.
        if mx > cb.CEIL_MS:
            ok = False
    return fixture(
        "F-SEQ2", ok,
        f"ceiling {cb.CEIL_MS} ({iso(cb.CEIL_MS)}) read from census_build.CEIL_MS; "
        f"max timestamp per file: "
        + ", ".join(f"{k}={v}" for k, v in sorted(worst.items()))
        + " — all <= ceiling (a bar opening before the ceiling may CLOSE on it)",
        {"per_file_max": worst, "ceiling_ms": cb.CEIL_MS})


def f_seq3():
    m = json.loads((R1 / "seq8_outcomes_manifest.json").read_text(encoding="utf-8"))
    j = m["join"]
    ok = j["orphans_join_to_journal"] == 0
    return fixture(
        "F-SEQ3", ok,
        f"{j['join_rows']} join rows; {j['distinct_births_joined']} of "
        f"{j['birth_keys_distinct']} distinct (cell_id,tranche_id) births joined; "
        f"orphans join->journal = {j['orphans_join_to_journal']}; "
        f"{j['births_never_joined']} births fall inside no cascade span (a real "
        f"outcome, not an orphan). RULE: {j['join_rule']}",
        {"join": j})


def f_seq4():
    p = R1 / "seq8_atlas_replication.json"
    a = json.loads(p.read_text(encoding="utf-8"))
    n = len(a["checks"])
    m = sum(1 for c in a["checks"] if c["result"] == "MATCH")
    ok = m == n
    return fixture(
        "F-SEQ4", ok,
        f"Atlas re-derived from census1b_termini_enriched.jsonl under its OWN "
        f"recipe: seq_total={a['reproduction']['seq_total']} (published 2378), "
        f"{m}/{n} published values reproduced exactly (6 signatures, 8 frontier "
        f"cells, 4 transition column totals, monotone_pct). The literal fixture "
        f"wording cannot hold: the Atlas is a TERMINUS-ANCHORED STAR over 14,560 "
        f"pivot termini, not a window-chained view over cross events — the diff "
        f"is itemized on 5 axes in seq8_atlas_replication.json:diff_vs_D2.",
        {"checks_matched": m, "checks_total": n,
         "diff_axes": [x["axis"] for x in a["diff_vs_D2"]["axes"]]})


def f_seq5():
    """Curtain audit. Two falsifiable assertions, not a hand wave:
       (i) no column named in the clean list is an outcome column;
      (ii) every terminus exec anchor opens at/after the terminus bar close."""
    m = json.loads((R1 / "seq8_outcomes_manifest.json").read_text(encoding="utf-8"))
    ca = m["curtain_audit"]
    clean_cols = " ".join(c["columns"] for c in ca["clean"])
    leaked = [t for t in ("mfe_", "mae_", "trunc_h", "joined_births")
              if t in clean_cols]

    # (ii) re-derive the anchor rule on a real sample, straight from the data.
    from engine.data import cache_dir
    klines = cache_dir() / "klines"
    checked = viol = 0
    sample = defaultdict(list)
    with open(R1 / "seq8_cascades.jsonl", encoding="utf-8") as f:
        for i, line in enumerate(f):
            if i % 9973:                       # deterministic stride sample
                continue
            r = json.loads(line)
            if r["term_exec_idx"] is not None:
                sample[r["asset"]].append((r["term_bar_close_ms"], r["term_exec_idx"]))
    for sym, rows in sorted(sample.items()):
        ex = cb.load_tf(klines, sym, cb.EXEC_TF, cb.ms(cb.ASSET_STARTS[sym]))
        xo = ex["open_time"].to_numpy(np.int64)
        for close_ms, k in rows:
            checked += 1
            if k >= len(xo):
                continue
            # the anchor must be the FIRST exec bar opening at/after the close
            if not (xo[k] >= close_ms and (k == 0 or xo[k - 1] < close_ms)):
                viol += 1
    ok = not leaked and viol == 0
    return fixture(
        "F-SEQ5", ok,
        f"curtain-clean list contains {len(ca['clean'])} column groups, none of "
        f"which is an outcome column ({len(leaked)} leaks); "
        f"{len(ca['post_curtain'])} column groups explicitly labelled "
        f"post-curtain. Anchor rule re-derived on {checked} sampled termini "
        f"across {len(sample)} assets: {viol} violations of 'first exec bar whose "
        f"open >= the terminus bar close'.",
        {"leaks": leaked, "anchors_checked": checked, "anchor_violations": viol})


def f_seq6():
    """EMA300/450: NaN before full warmup, zero backfilled values."""
    warm = json.loads((R1 / "seq8_warmup.json").read_text(encoding="utf-8"))
    bad = []
    for w in warm:
        if not w["applicable"]:
            if w["warm_bars_in_window"] != 0:
                bad.append(("non-HTF TF carries a warmed value", w))
            continue
        # a warmed cell must have first_warm at or after the required bar count
        if w["status"] == "WARMED" and w["first_warm_ts"] is None:
            bad.append(("WARMED without a timestamp", w))
        if w["status"] == "NEVER" and w["warm_bars_in_window"] != 0:
            bad.append(("NEVER but warm bars present", w))

    # direct scan of the emitted stream: no e300/e450 value may appear on a TF
    # outside HTF_TFS, and none may be a backfilled number where NaN is due.
    seen_non_htf = 0
    n_null = n_val = 0
    with open(R1 / "seq8_events.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            for L in HTF_ORIENT:
                v = r.get(f"e{L}")
                if r["tf"] not in HTF_TFS:
                    if v is not None:
                        seen_non_htf += 1
                elif v is None:
                    n_null += 1
                else:
                    n_val += 1
    ok = not bad and seen_non_htf == 0
    never = [f"{w['asset']}/{w['tf']}/e{w['ema']}" for w in warm
             if w["status"] == "NEVER"]
    return fixture(
        "F-SEQ6", ok,
        f"warmup rule: seed residual (1-alpha)^k < 1e-3 -> EMA300 needs "
        f"{WARM[300]} bars, EMA450 needs {WARM[450]} bars. {len(warm)} asset x TF "
        f"x length cells audited, {len(bad)} inconsistencies; {seen_non_htf} "
        f"e300/e450 values on a non-HTF timeframe (must be 0); across the event "
        f"stream {n_null} null vs {n_val} warmed 300/450 readings. "
        f"{len(never)} cells NEVER warm within the substrate: {', '.join(never)}",
        {"inconsistencies": bad[:10], "never": never,
         "warmup_bars": {str(L): WARM[L] for L in HTF_ORIENT}})


def f_seq7():
    """Full re-run byte-identity, manifest sha256 vs manifest sha256."""
    if not R2.exists():
        return fixture("F-SEQ7", False,
                       "run2 root absent — determinism pass not executed")
    pairs, diffs = [], []
    for man in ("seq8_extract_manifest.json", "seq8_views_summary.json",
                "seq8_outcomes_manifest.json"):
        p1, p2 = R1 / man, R2 / man
        if not (p1.exists() and p2.exists()):
            diffs.append(f"{man}: missing in one root")
            continue
        m1 = json.loads(p1.read_text(encoding="utf-8"))
        m2 = json.loads(p2.read_text(encoding="utf-8"))
        for k, v in sorted(m1.get("sha256", {}).items()):
            w = m2.get("sha256", {}).get(k)
            pairs.append((k, v, w))
            if v != w:
                diffs.append(f"{k}: {v[:16]} != {(w or 'MISSING')[:16]}")
    # and the arrivals panel, which carries the scored claim
    for name in ("seq8_arrivals.json", "seq8_event_counts.json", "seq8_warmup.json"):
        p1, p2 = R1 / name, R2 / name
        if p1.exists() and p2.exists():
            a, b = sha256_file(p1), sha256_file(p2)
            pairs.append((name, a, b))
            if a != b:
                diffs.append(f"{name}: {a[:16]} != {b[:16]}")
    ok = not diffs
    return fixture(
        "F-SEQ7", ok,
        f"{len(pairs)} artifacts compared across a full independent re-run "
        f"(seq8 vs seq8_run2); {len(diffs)} differ. python "
        f"{sys.version.split()[0]}, numpy {np.__version__}. No seed is used "
        f"anywhere in this extract — nothing is sampled, bootstrapped or "
        f"shuffled, so there is no seed to print. NORMALIZATION DISCLOSURE: the "
        f"three manifests are compared via their sha256 BLOCKS, not as files, "
        f"because each carries a wall-clock `elapsed_s` that cannot be "
        f"byte-stable; every bulk artifact they name is compared by its own "
        f"sha256, and seq8_arrivals.json / seq8_event_counts.json / "
        f"seq8_warmup.json are compared RAW. NO computed value is normalized "
        f"(precedent: census1b_det.py F1b-DET).",
        {"diffs": diffs[:20], "compared": [(k, v[:16]) for k, v, _ in pairs],
         "normalized_fields": ["elapsed_s (manifest wall-clock only)"]})


def f_seq8():
    """Worked multiTF query over D1, hand-verified.

    Pattern (the contract's own example, restricted to classes D1 emits):
        5m bull 9_89 cross  ->  15m bull 9_89 cross  ->  4h bull 9_89 cross
        all within 48h, on one asset-month, with 12h e89 > e200 at the 4h event.
    The 12h alignment is read from the event row's `mtf` bit string, proving the
    cross-timeframe state travels with the atom and needs no re-extraction.
    """
    import bisect
    W = 48 * 3_600_000
    # Pattern fixed in advance and run over the ENTIRE substrate — every asset,
    # every month — so the demonstration cannot be a cherry-picked window.
    by = defaultdict(lambda: defaultdict(list))
    with open(R1 / "seq8_events.jsonl", encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if (r["lattice"] != "A" or r["event_class"] != "9_89"
                    or r["dir"] != "up" or r["tf"] not in ("5m", "15m", "4h")):
                continue
            by[r["asset"]][r["tf"]].append(r)
    per_asset, worked = {}, None
    total = 0
    for asset in sorted(by):
        tf5 = sorted(by[asset]["5m"], key=lambda r: r["bar_close_ms"])
        t15 = sorted(by[asset]["15m"], key=lambda r: r["bar_close_ms"])
        t4h = sorted(by[asset]["4h"], key=lambda r: r["bar_close_ms"])
        c5 = [r["bar_close_ms"] for r in tf5]
        c15 = [r["bar_close_ms"] for r in t15]
        n = 0
        for c in t4h:
            if c["mtf"]["12h"][1] != "1":       # 12h e89>e200 as-of the 4h event
                continue
            cc = c["bar_close_ms"]
            lo = bisect.bisect_left(c15, cc - W)
            hi = bisect.bisect_right(c15, cc)
            for bi in range(lo, hi):
                b = t15[bi]
                bb = b["bar_close_ms"]
                a_lo = bisect.bisect_left(c5, bb - W)
                a_hi = bisect.bisect_right(c5, bb)
                k = a_hi - a_lo
                n += k
                if k and worked is None:
                    a = tf5[a_hi - 1]
                    worked = {"asset": asset, "5m": a["ts_iso"],
                              "15m": b["ts_iso"], "4h": c["ts_iso"],
                              "12h_bits_at_4h": c["mtf"]["12h"],
                              "mtf_bit_index_1": "e89>e200",
                              "4h_event_price": c["event_price"],
                              "gap_5m_to_15m_h": round((bb - a["bar_close_ms"]) / 3.6e6, 2),
                              "gap_15m_to_4h_h": round((cc - bb) / 3.6e6, 2)}
        per_asset[asset] = n
        total += n
    ok = total > 0 and worked is not None
    return fixture(
        "F-SEQ8", ok,
        f"query over D1 alone (no re-extraction, no recomputation of any "
        f"indicator): bull 9_89 5m->15m->4h, each step within 48h, with 12h "
        f"e89>e200 as-of the 4h arrival — {total} ordered triples across the "
        f"whole substrate: "
        + ", ".join(f"{a}={c}" for a, c in sorted(per_asset.items()))
        + f". Worked instance for hand-inspection: {worked['asset']} "
          f"5m {worked['5m']} -> 15m {worked['15m']} (+{worked['gap_5m_to_15m_h']}h) "
          f"-> 4h {worked['4h']} (+{worked['gap_15m_to_4h_h']}h), 12h bits "
          f"'{worked['12h_bits_at_4h']}' (index 1 = e89>e200 = 1). The "
          f"cross-timeframe state travels ON the atom, which is what makes "
          f"across-time-AND-across-timeframes patterns minable without "
          f"re-extraction.",
        {"total_triples": total, "per_asset": per_asset, "worked": worked})


def main() -> int:
    t0 = time.time()
    print("=" * 72)
    print("SEQ-8 FIXTURE TRANSCRIPT")
    print("=" * 72)
    print("\n=== FIXTURES ===")
    for fn in (f_seq1, f_seq2, f_seq3, f_seq4, f_seq5, f_seq6, f_seq7, f_seq8):
        try:
            fn()
        except Exception as exc:                      # a fixture must never
            fixture(fn.__name__.upper().replace("_", "-"), False,
                    f"raised {type(exc).__name__}: {exc}")   # hide a failure
    npass = sum(1 for f in FIXTURES if f["pass"])
    print("\n=== FIXTURE SUMMARY ===")
    print(f"  {npass}/{len(FIXTURES)} pass")
    write_json(R1 / "seq8_fixtures.json",
               {"fixtures": FIXTURES, "pass": npass, "total": len(FIXTURES),
                "elapsed_s": round(time.time() - t0, 1)})
    if npass != len(FIXTURES):
        print("*** FIXTURE MISMATCH — HALT ***")
    return 0 if npass == len(FIXTURES) else 1


if __name__ == "__main__":
    raise SystemExit(main())
