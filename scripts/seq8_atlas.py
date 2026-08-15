"""SEQ-8 — F-SEQ4 Atlas replication + the third P-SEQ-ii scoring frame.

Contract: exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md §4
  F-SEQ4  "The {48h, window-chained, 3-rung-truncated} view reproduces the Atlas
           count (2,378 on the same asset/lens set) exactly, or the diff is
           itemized."

WHY THIS FILE EXISTS, AND WHY F-SEQ4 CANNOT PASS AS LITERALLY WORDED
  The fixture presumes the Atlas 2,378 is a window-chained view over cross
  events. It is not. Recovered by reproduction, the Atlas number is a
  TERMINUS-ANCHORED STAR over a different population:

    population   14,560 confirmed (5,5) pullback termini, lenses {1h,4h,12h,1d}
                 (census1b_termini_enriched.jsonl, written by
                 scripts/census1b_analyze.py::d5b_enrich)
    per terminus take the FIRST forward 9_89 cross on EACH of the 7 TFs
    filter       aligned direction only; lag_exec_bars <= 576 (48h of 5m bars),
                 measured from exec_idx_confirm — NOT from the pivot low
    order        ascending by lag; the "sequence" is that order truncated to 3
    count        termini whose order has >= 3 rungs  ->  2,378

  A cascade chained from D1 cross atoms is a different object with a different
  population, so the two counts cannot be equal and equality would in fact
  indicate a bug. This file therefore does what F-SEQ4's escape clause requires:
  reproduces the Atlas number EXACTLY under the Atlas's own recipe, then
  itemizes the diff against the D2 view axis by axis.

  No generator for the Atlas `const D` blob exists in the repo (grep for
  seq_total/transitions/sequences/interrung hits only the two Atlas HTMLs and
  the two design-contract copies) — it is a hand-carried JSON. This is a
  re-derivation from the substrate, not a port.

SECOND PURPOSE — the honest scoring frame for P-SEQ-ii.
  P-SEQ-ii is a REPLICATION claim about a finding made on THIS object. Scoring
  it only on the D2 cascade views would test a different proposition. So the
  arrivals panel is computed here too, in the Atlas's own frame, and reported
  beside the D2 frames in seq8_views.py.

Usage:
  python scripts/seq8_atlas.py
"""
from __future__ import annotations

import json
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import census_build as cb                                   # noqa: E402
from seq8_extract import write_json                         # noqa: E402
from seq8_views import TFI, classify_arrival, FAST_TIER, REPLICATION_BAR  # noqa: E402

SRC = ROOT / "census1b_termini_enriched.jsonl"
W48_EXEC_BARS = 576          # 48h of 5m exec bars, per census1b_analyze.py:762
CROSS = "9_89"               # the Atlas counts this pair ONLY
ARRIVAL_LENSES = ["1h", "4h", "12h", "1d"]

# Published Atlas values, transcribed for validation. Sources:
#   seq_total          Cascade_Atlas_CENSUS_1b.html:236 / _v2_1.html:374
#   frontier (depth)   D.depth.pooled.w48h
#   arrival shares     Cascade Rewire.html drawArrivals() dests[] prose
PUBLISHED = {
    "seq_total": 2378,
    "top_sig": {"5m>15m>30m": 1441, "5m>30m>15m": 180, "15m>30m>1h": 151,
                "5m>15m>1h": 141, "5m>15m>4h": 55, "5m>15m>12h": 46},
    "frontier": {"none": 6378, "5m": 1527, "15m": 1609, "30m": 1860,
                 "1h": 1150, "4h": 1029, "12h": 624, "1d": 383},
    "transition_col_totals": {"1h": 1111, "4h": 434, "12h": 281, "1d": 179},
    "monotone_pct_ge2rungs": 83.6,
}


def order_for(rec: dict) -> list:
    """The Atlas's per-terminus ordering: first forward aligned 9_89 cross on
    each TF, within 48h of the CONFIRM bar, ascending by lag. One rung per TF."""
    fwd = rec.get("forward") or {}
    hits = []
    for tf in cb.TFS:
        c = (fwd.get(tf) or {}).get(CROSS)
        if not c:
            continue
        if c.get("dir") != rec["dir"]:
            continue                       # aligned-direction only
        lag = c.get("lag_exec_bars")
        if lag is None or lag > W48_EXEC_BARS:
            continue
        hits.append((int(lag), tf))
    # Tie-break is ALPHABETICAL on the TF name, not by ladder position. The
    # substrate is written with sort_keys=True, so `forward`'s keys arrive as
    # 12h,15m,1d,1h,30m,4h,5m; the Atlas blob was built by a stable sort over
    # that iteration order, which preserves it whenever lags are equal.
    # Recovered empirically: ladder-order tie-breaking moves ~60 termini from
    # 5m>15m>1h into 5m>15m>30m and misses the published signature counts.
    hits.sort()
    return [t for _, t in hits]


def main() -> int:
    if not SRC.exists():
        print(f"MISSING: {SRC}")
        return 2
    t0 = time.time()
    print("SEQ-8 ATLAS REPLICATION (F-SEQ4)")
    print(f"  substrate : {SRC.name}")
    print(f"  recipe    : terminus-anchored star, {CROSS} only, aligned dir, "
          f"lag <= {W48_EXEC_BARS} exec bars from exec_idx_confirm")

    rows = [json.loads(l) for l in open(SRC, encoding="utf-8")]
    print(f"  termini   : {len(rows)}")

    sigs = Counter()
    frontier = Counter()
    transitions = defaultdict(Counter)          # transitions[src][dest]
    arrivals = defaultdict(Counter)             # (asset, lens) -> kind
    depths = Counter()
    n_ge3 = 0
    mono_ge2, n_ge2 = 0, 0
    assets = set()

    for r in rows:
        assets.add(r["asset"])
        o = order_for(r)
        depths[len(o)] += 1
        frontier[max(o, key=lambda t: TFI[t]) if o else "none"] += 1
        if len(o) >= 3:
            n_ge3 += 1
            sigs[">".join(o[:3])] += 1
        if len(o) >= 2:
            n_ge2 += 1
            if all(TFI[o[k]] < TFI[o[k + 1]] for k in range(len(o) - 1)):
                mono_ge2 += 1
        # transitions are consecutive pairs of the FULL ordering (not the
        # 3-rung signature) — this is what drawArrivals() reads column-wise.
        for k in range(len(o) - 1):
            transitions[o[k]][o[k + 1]] += 1
        for k, tf in enumerate(o):
            if tf in ARRIVAL_LENSES and k > 0:
                src = o[k - 1]
                arrivals[(r["asset"], tf)][classify_arrival(src, tf)] += 1
                if tf == "4h":
                    arrivals[(r["asset"], tf)][
                        "leap_from_fast" if src in FAST_TIER
                        else "not_leap_from_fast"] += 1

    col_tot = {d: sum(transitions[s][d] for s in cb.TFS) for d in ARRIVAL_LENSES}
    mono_pct = round(100.0 * mono_ge2 / n_ge2, 2) if n_ge2 else None

    # ---- validation against the published blob ----
    checks = []

    def chk(name, got, want):
        ok = got == want
        checks.append({"check": name, "got": got, "want": want,
                       "result": "MATCH" if ok else "MISMATCH"})
        return ok

    chk("seq_total (termini with >=3 rungs)", n_ge3, PUBLISHED["seq_total"])
    for s, want in PUBLISHED["top_sig"].items():
        chk(f"signature {s}", sigs.get(s, 0), want)
    for tf, want in PUBLISHED["frontier"].items():
        chk(f"frontier {tf}", frontier.get(tf, 0), want)
    for tf, want in PUBLISHED["transition_col_totals"].items():
        chk(f"transition column total {tf}", col_tot[tf], want)
    chk("monotone_pct (>=2 rungs)", mono_pct, PUBLISHED["monotone_pct_ge2rungs"])

    n_match = sum(1 for c in checks if c["result"] == "MATCH")
    print(f"\n  validation: {n_match}/{len(checks)} MATCH")
    for c in checks:
        if c["result"] != "MATCH":
            print(f"    MISMATCH {c['check']}: got {c['got']} want {c['want']}")

    # ---- pooled arrival shares (the published prose) ----
    pooled = {}
    for lens in ARRIVAL_LENSES:
        c = Counter()
        for (a, l), cc in arrivals.items():
            if l == lens:
                c.update(cc)
        tot = c["adjacent"] + c["leap"] + c["from_above"]
        pooled[lens] = {
            "n": tot, "adjacent": c["adjacent"], "leap": c["leap"],
            "from_above": c["from_above"],
            "adjacent_pct": round(100.0 * c["adjacent"] / tot, 1) if tot else None,
            "leap_pct": round(100.0 * c["leap"] / tot, 1) if tot else None,
        }
    print("  pooled arrivals (Atlas frame):")
    for lens in ARRIVAL_LENSES:
        p = pooled[lens]
        print(f"    {lens:3} n={p['n']:5}  adjacent {p['adjacent_pct']}%  "
              f"leap {p['leap_pct']}%")

    # ---- P-SEQ-ii in the Atlas frame, per asset ----
    panel, scores = [], {}
    for lens, test in (("4h", "leap"), ("1h", "adjacent")):
        scorable, agree, detail = 0, 0, {}
        for a in sorted(assets):
            c = arrivals.get((a, lens), Counter())
            cats = {"adjacent": c["adjacent"], "leap": c["leap"],
                    "from_above": c["from_above"]}
            n = sum(cats.values())
            panel.append({"frame": "atlas_star", "asset": a, "lens": lens,
                          "n_arrivals": n, **cats,
                          "leap_from_fast": c["leap_from_fast"] or None,
                          "adjacent_pct": round(100.0 * cats["adjacent"] / n, 3) if n else None,
                          "leap_pct": round(100.0 * cats["leap"] / n, 3) if n else None})
            if n == 0:
                detail[a] = "unscorable(n=0)"
                continue
            scorable += 1
            top = max(cats, key=lambda k: (cats[k], k))
            ok = top == test
            agree += int(ok)
            detail[a] = f"{'YES' if ok else 'no'} ({test}={cats[test]}/{n})"
        scores[lens] = {"test": f"{test} is the largest arrival category at {lens}",
                        "assets_scorable": scorable, "assets_agreeing": agree,
                        "bar": REPLICATION_BAR, "per_asset": detail,
                        "replicates": bool(agree >= REPLICATION_BAR)}

    replicates = scores["4h"]["replicates"] and scores["1h"]["replicates"]
    print(f"\n  P-SEQ-ii [atlas_star]: 4h-leap "
          f"{scores['4h']['assets_agreeing']}/{scores['4h']['assets_scorable']}  "
          f"1h-adjacent {scores['1h']['assets_agreeing']}/{scores['1h']['assets_scorable']}"
          f"  -> {'REPLICATES' if replicates else 'DOES NOT REPLICATE'}")

    out = {
        "fixture": "F-SEQ4",
        "status": "MATCH" if n_match == len(checks) else "MISMATCH",
        "atlas_recipe": {
            "population": "census1b_termini_enriched.jsonl real termini",
            "n_termini": len(rows),
            "cross_type": CROSS,
            "direction": "aligned with the terminus regime only",
            "window_exec_bars": W48_EXEC_BARS,
            "window_measured_from": "exec_idx_confirm (NOT the pivot low — the "
                                    "Atlas prose label '48 hours after the low' "
                                    "is wrong by PIVOT_R=5 lens bars)",
            "rungs": "first forward cross per TF, one per TF, ascending by lag",
            "truncation": "sequence = order[:3]; transitions use the FULL order",
            "assets": sorted(assets),
        },
        "reproduction": {
            "seq_total": n_ge3, "n_ge2_rungs": n_ge2,
            "monotone_pct_ge2rungs": mono_pct,
            "depth_hist": {str(k): v for k, v in sorted(depths.items())},
            "frontier": dict(frontier),
            "top_signatures": dict(sigs.most_common(12)),
            "transition_col_totals": col_tot,
            "pooled_arrivals": pooled,
        },
        "checks": checks,
        "p_seq_ii_atlas_frame": {
            "limb_A_4h_leap_dominant": scores["4h"],
            "limb_B_1h_adjacent_dominant": scores["1h"],
            "replicates": bool(replicates),
        },
        "panel": panel,
        "diff_vs_D2": {
            "verdict": "NOT COMPARABLE BY CONSTRUCTION — itemized per F-SEQ4's "
                       "escape clause; the chained view does not and cannot "
                       "reproduce 2,378.",
            "axes": [
                {"axis": "anchor", "atlas": "a confirmed (5,5) pullback terminus",
                 "d2": "a cross event (D1 atom)",
                 "consequence": "different populations: 14,560 termini vs "
                                "288,711 cross events"},
                {"axis": "rung admission", "atlas": "first forward cross per TF, "
                 "measured from the terminus", "d2": "next same-direction cross "
                 "on a new TF within `window` of the PREVIOUS admitted rung",
                 "consequence": "the Atlas window is a fixed radius around one "
                                "anchor; D2's window slides with the chain, so "
                                "D2 cascades can span far more than 48h"},
                {"axis": "pair set", "atlas": "9_89 only",
                 "d2": "9_89, 89_200, 9_200, 12_25",
                 "consequence": "D2 counts 4 event classes; the Atlas counts 1"},
                {"axis": "direction", "atlas": "aligned with terminus regime; a "
                 "counter-direction cross is invisible",
                 "d2": "direction is a rule parameter — invisible under "
                       "window-chained, a TERMINATOR under direction-consistent",
                 "consequence": "the Atlas has no counterpart to the "
                                "direction-consistent challenger"},
                {"axis": "TF whose cross precedes the anchor",
                 "atlas": "absent from the ladder entirely (only FORWARD crosses "
                          "count), so a lens that fired before the terminus "
                          "leaves a hole",
                 "d2": "present — chaining walks the event stream and admits it",
                 "consequence": "THIS is the mechanism behind the leap: a 4h "
                                "arrival looks like a jump from the fast tier "
                                "whenever 1h's cross fell before the terminus. "
                                "Depth-complete chaining fills that hole and the "
                                "same arrival reads as adjacent."},
            ],
        },
        "elapsed_s": round(time.time() - t0, 1),
    }
    write_json(ROOT / "research_outputs" / "seq8" / "seq8_atlas_replication.json", out)
    print(f"\nATLAS done in {time.time() - t0:.1f}s -> "
          f"research_outputs/seq8/seq8_atlas_replication.json")
    return 0 if n_match == len(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())
