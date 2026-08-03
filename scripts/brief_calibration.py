#!/usr/bin/env python
"""brief_calibration.py -- the §9.2 calibration report.

    C:\\venvs\\naiad\\Scripts\\python.exe scripts/brief_calibration.py --date 2026-08-03

Emits `exchange/reports/BRIEF2_CALIBRATION_<date>.json` plus a markdown summary.

WHAT THIS IS FOR.  Amendment §5.3: every threshold in the contract was calibrated
against a registry roughly a third the size the volume layers produce, and
"no threshold is defended on intuition once measured numbers exist."  This report
is the measurement that replaces intuition.

IT DOES NOT RE-RATIFY ANYTHING.  Reviewer ruling D-2 is explicit that no
threshold is re-ratified against a registry that is not yet the real one.  This
prints distributions; the operator and reviewer rule on them.

ITEM 6 LEADS the markdown because the amendment calls it "the single most
interesting number the build will produce": how often the volume-included and
volume-excluded lines in the sand DIFFER, and by how much.
"""

import argparse
import json
import statistics
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import brief2 as B2                                                 # noqa: E402
from analytics import levels as L                                   # noqa: E402

BRIEFS = ROOT / "briefs"
OUT_DIR = ROOT / "exchange" / "reports"

# §5.3 states v1.1 ran 46-62 levels per asset.  Cited from the contract, NOT
# recomputed here: the v1.1 registry no longer exists to measure, and inventing a
# reconstruction would be a worse number than an honestly-attributed one.
V11_LEVELS_PER_ASSET = "46-62 (contract §5.3, not recomputed)"


def _pct(xs, q):
    if not xs:
        return None
    s = sorted(xs)
    i = min(int(round(q / 100 * (len(s) - 1))), len(s) - 1)
    return s[i]


def _load(date, slot=None):
    pats = f"brief_{date}_{slot}.json" if slot else f"brief_{date}_*.json"
    caps = sorted(BRIEFS.glob(pats))
    if not caps:
        raise SystemExit(f"no capture for {date} in {BRIEFS}")
    with caps[-1].open(encoding="utf-8") as fh:
        return caps[-1], json.load(fh)


def calibrate(date, slot=None):
    path, doc = _load(date, slot)
    assets = doc["assets"]
    out = {"date": doc["date"], "slot": doc["slot"],
           "capture": path.name,
           "schema_version": doc.get("schema_version"),
           "rules_version": doc.get("rules_version"),
           "analytics_version": doc.get("analytics_version"),
           "analytics_sha": doc.get("analytics_sha"),
           "parity_certified": doc.get("parity_certified"),
           "not_a_ratification": "reviewer ruling D-2: distributions are printed, "
                                 "no threshold is re-ratified here"}

    # ---- item 1: level count per asset, by family
    item1 = {"v1_1_reference": V11_LEVELS_PER_ASSET, "per_asset": {}}
    for sym, a in assets.items():
        c = a["confluence"]
        item1["per_asset"][sym] = {"total": c["level_count"],
                                   "by_family": c["level_count_by_family"]}
    totals = [v["total"] for v in item1["per_asset"].values()]
    item1["summary"] = {"min": min(totals), "median": statistics.median(totals),
                        "max": max(totals),
                        "contract_expectation": "~180-200 (§5.3)"}
    out["item1_level_count"] = item1

    # ---- item 2: score distribution + how often the family cap binds
    scores, cap_binds, cap_total = [], 0, 0
    for a in assets.values():
        for cl in a["confluence"]["with_volume"]["clusters"]:
            scores.append(cl["score"])
            per = Counter(m["family"] for m in cl["members"])
            for n in per.values():
                cap_total += 1
                if n > L.FAMILY_CAP:
                    cap_binds += 1
    out["item2_score_distribution"] = {
        "min": min(scores), "median": statistics.median(scores),
        "p90": _pct(scores, 90), "max": max(scores), "n_clusters": len(scores),
        "family_cap": L.FAMILY_CAP,
        "cap_binds_count": cap_binds, "cap_opportunities": cap_total,
        "cap_binds_pct": round(100 * cap_binds / cap_total, 2) if cap_total else None,
        "note": "the cap binds whenever one family contributes more members than "
                "FAMILY_CAP to a single cluster -- that is it doing its job, "
                "stopping one prolific tool manufacturing agreement with itself"}

    # ---- item 3: line stability across tolerances
    item3 = {}
    for sym, a in assets.items():
        conf = a["confluence"]
        members = [m for cl in conf["with_volume"]["clusters"] for m in cl["members"]]
        atr, price = a["daily_atr"], a["price"]
        per_tol = {}
        for tol in (0.10, L.CLUSTER_ATR, 0.20):
            cl = L.cluster(members, atr, tol=tol)
            lines = L.lines_in_sand(cl, price, atr)
            per_tol[str(tol)] = {
                "above": (lines["above"] or {}).get("mean"),
                "below": (lines["below"] or {}).get("mean"),
                "clusters": len(cl)}
        aboves = [v["above"] for v in per_tol.values() if v["above"] is not None]
        belows = [v["below"] for v in per_tol.values() if v["below"] is not None]
        item3[sym] = {"by_tolerance": per_tol,
                      "above_spread": (max(aboves) - min(aboves)) if len(aboves) > 1 else 0.0,
                      "below_spread": (max(belows) - min(belows)) if len(belows) > 1 else 0.0,
                      "stable": (len(set(aboves)) <= 1 and len(set(belows)) <= 1)}
    out["item3_line_stability"] = item3

    # ---- item 4: family composition of the top-3 areas
    item4, dom = {}, Counter()
    for sym, a in assets.items():
        top = sorted(a["confluence"]["with_volume"]["clusters"],
                     key=lambda c: -c["score"])[:3]
        rows = []
        for cl in top:
            per = Counter(m["family"] for m in cl["members"])
            lead = per.most_common(1)[0][0] if per else None
            dom[lead] += 1
            rows.append({"mean": cl["mean"], "score": cl["score"],
                         "families": dict(per), "largest_family": lead})
        item4[sym] = rows
    out["item4_top3_composition"] = {
        "per_asset": item4,
        "largest_family_tally": dict(dom),
        "question": "does vwap_rolling or profile_windowed DOMINATE the top areas? "
                    "if so the family split did not go far enough (§9.2 item 4)"}

    # ---- item 5: VA nesting state distribution
    states = Counter()
    per_pair = {}
    for a in assets.values():
        for pair, blob in (a["va_nesting"]["pairs"] or {}).items():
            st = blob.get("state") or "unavailable(warming)"
            states[st] += 1
            per_pair.setdefault(pair, Counter())[st] += 1
    out["item5_nesting_states"] = {
        "overall": dict(states),
        "by_pair": {k: dict(v) for k, v in per_pair.items()},
        "n_assets": len(assets)}

    # ---- item 6: THE HEADLINE -- dual-scoring divergence
    diffs, changed, both_sides = [], 0, 0
    per_asset6 = {}
    for sym, a in assets.items():
        d = a["confluence"]["differ"]
        atr = a["daily_atr"]
        sides = {}
        for side in ("above", "below"):
            s = d[side]
            sides[side] = {"changed": s["changed"], "delta": s.get("delta"),
                           "delta_atr": s.get("delta_atr"),
                           "with_volume": s.get("with_volume"),
                           "without_volume": s.get("without_volume"),
                           "note": s.get("note")}
            if s["changed"]:
                changed += 1
                if s.get("delta_atr") is not None:
                    diffs.append(s["delta_atr"])
        if d["any_changed"]:
            both_sides += 1
        per_asset6[sym] = sides
    out["item6_dual_scoring_divergence"] = {
        "assets_where_a_line_moved": both_sides,
        "of_assets": len(assets),
        "sides_changed": changed, "of_sides": 2 * len(assets),
        "delta_atr": {"n": len(diffs),
                      "min": min(diffs) if diffs else None,
                      "median": statistics.median(diffs) if diffs else None,
                      "p90": _pct(diffs, 90), "max": max(diffs) if diffs else None},
        "per_asset": per_asset6,
        "what_this_measures": "whether volume evidence MOVES THE OPERATOR'S "
                              "LINES. It is display-only; whether the move helps "
                              "is census work under G-7."}

    # ---- item 7: measured storage
    cap_bytes = path.stat().st_size
    parts = {}
    for t in ("snapshots", "levels", "areas"):
        p = BRIEFS / "panel" / t / f"{doc['date']}.parquet"
        parts[t] = p.stat().st_size if p.exists() else None
    part_total = sum(v for v in parts.values() if v)
    out["item7_storage"] = {
        "capture_bytes": cap_bytes,
        "partition_bytes": parts, "partitions_per_day": part_total,
        "slots_per_day": 3,
        "projected_annual_mb": {
            "captures": round(cap_bytes * 3 * 365 / 1e6, 1),
            "partitions": round(part_total * 365 / 1e6, 1),
            "total": round((cap_bytes * 3 + part_total) * 365 / 1e6, 1)},
        "contract_estimate_mb": "150-250 (§8.2)"}

    # ---- extra (stage C.4): inval_atr distribution
    inval, ranked, excluded = [], 0, 0
    for a in assets.values():
        rr = a["decision_instrument"]["rr_ranking"]
        ranked += len(rr["board"])
        excluded += len(rr["excluded_too_tight"])
        for r in rr["board"] + rr["excluded_too_tight"]:
            if r.get("inval_atr") is not None:
                inval.append(r["inval_atr"])
    out["extra_inval_atr_distribution"] = {
        "floor": B2.MIN_INVAL_ATR, "n": len(inval),
        "min": min(inval) if inval else None,
        "p25": _pct(inval, 25), "median": statistics.median(inval) if inval else None,
        "p75": _pct(inval, 75), "max": max(inval) if inval else None,
        "rows_ranked": ranked, "rows_excluded": excluded,
        "purpose": "R-1 stage C.4 -- the floor is a v1 PLACEHOLDER and is "
                   "re-ratified against this distribution, not against a guess"}

    # ---- runtime
    out["runtime"] = {"total_seconds": doc.get("runtime_seconds"),
                      "by_layer": doc.get("runtime_by_layer"),
                      "budget_note": "one capture must stay well under ~15 min; "
                                     "three slots per day"}
    return out


def to_markdown(c):
    L_ = []
    a = L_.append
    a(f"# BRIEF-2 CALIBRATION — {c['date']} ({c['slot']})")
    a("")
    a(f"`{c['capture']}` · schema {c['schema_version']} · rules {c['rules_version']} "
      f"· analytics {c['analytics_version']}")
    a("")
    a("> **PARITY NOT CERTIFIED.** Nothing here is adopted. "
      "**No threshold is re-ratified in this report** (reviewer ruling D-2) — "
      "it prints distributions so the operator and reviewer can rule on them.")
    a("")

    i6 = c["item6_dual_scoring_divergence"]
    a("## ITEM 6 — does volume evidence move the lines? *(the headline)*")
    a("")
    a(f"**A line in the sand moved on {i6['assets_where_a_line_moved']} of "
      f"{i6['of_assets']} assets** "
      f"({i6['sides_changed']} of {i6['of_sides']} individual sides).")
    a("")
    d = i6["delta_atr"]
    if d["n"]:
        a(f"Where a line moved and both views had one, the move was "
          f"**{d['median']:.3f} daily-ATR at the median** "
          f"(min {d['min']:.3f}, p90 {d['p90']:.3f}, max {d['max']:.3f}, n={d['n']}).")
    else:
        a("No side had a measurable delta: every change was a line existing in "
          "one view only, which is itself the strongest form of the result.")
    a("")
    a("| asset | side | with volume | without volume | Δ ATR |")
    a("|---|---|---|---|---|")
    for sym, sides in i6["per_asset"].items():
        for side, s in sides.items():
            if not s["changed"]:
                continue
            wv = f"{s['with_volume']:,.2f}" if s["with_volume"] is not None else "—"
            nv = f"{s['without_volume']:,.2f}" if s["without_volume"] is not None else "—"
            da = f"{s['delta_atr']:.3f}" if s.get("delta_atr") is not None else "n/a"
            a(f"| {sym} | {side} | {wv} | {nv} | {da} |")
    a("")
    a(f"*{i6['what_this_measures']}*")
    a("")

    i1 = c["item1_level_count"]
    a("## Item 1 — registry size by family")
    a("")
    a(f"v1.1 reference: {i1['v1_1_reference']} · contract expectation "
      f"{i1['summary']['contract_expectation']} · "
      f"measured min {i1['summary']['min']} / median {i1['summary']['median']} / "
      f"max {i1['summary']['max']}")
    a("")
    a("| asset | total | anchored | rolling | profile | structure | ss |")
    a("|---|---|---|---|---|---|---|")
    for sym, v in i1["per_asset"].items():
        f = v["by_family"]
        a(f"| {sym} | {v['total']} | {f['vwap_anchored']} | {f['vwap_rolling']} | "
          f"{f['profile_windowed']} | {f['structure']} | {f['ss']} |")
    a("")

    i2 = c["item2_score_distribution"]
    a("## Item 2 — score distribution and the family cap")
    a("")
    a(f"min {i2['min']} · median {i2['median']} · p90 {i2['p90']} · max {i2['max']} "
      f"over {i2['n_clusters']} clusters.")
    a("")
    a(f"The cap (={i2['family_cap']}) binds in **{i2['cap_binds_count']} of "
      f"{i2['cap_opportunities']}** family-in-cluster opportunities "
      f"({i2['cap_binds_pct']}%). {i2['note']}")
    a("")

    a("## Item 3 — line-in-the-sand stability across tolerance")
    a("")
    a("| asset | stable? | above spread | below spread |")
    a("|---|---|---|---|")
    for sym, v in c["item3_line_stability"].items():
        a(f"| {sym} | {'yes' if v['stable'] else 'NO'} | "
          f"{v['above_spread']:,.2f} | {v['below_spread']:,.2f} |")
    a("")

    i4 = c["item4_top3_composition"]
    a("## Item 4 — family composition of the top-3 areas")
    a("")
    a(f"Largest-family tally across all top-3 areas: `{i4['largest_family_tally']}`")
    a("")
    a(f"*{i4['question']}*")
    a("")

    i5 = c["item5_nesting_states"]
    a("## Item 5 — VA nesting state distribution")
    a("")
    a(f"Overall: `{i5['overall']}`")
    a("")
    for pair, v in i5["by_pair"].items():
        a(f"- `{pair}` → {v}")
    a("")

    i7 = c["item7_storage"]
    p = i7["projected_annual_mb"]
    a("## Item 7 — measured storage")
    a("")
    a(f"| | bytes |")
    a(f"|---|---|")
    a(f"| capture (one slot) | {i7['capture_bytes']:,} |")
    for k, v in i7["partition_bytes"].items():
        a(f"| partition `{k}` | {v:,} |")
    a(f"| partitions per day | {i7['partitions_per_day']:,} |")
    a("")
    a(f"Projected annual at 3 slots/day: **captures {p['captures']} MB + "
      f"partitions {p['partitions']} MB = {p['total']} MB/yr** "
      f"against a contract estimate of {i7['contract_estimate_mb']} MB.")
    a("")

    e = c["extra_inval_atr_distribution"]
    a("## Extra — invalidation distance distribution (R-1, stage C.4)")
    a("")
    if e["n"]:
        a(f"floor **{e['floor']}** · min {e['min']:.3f} · p25 {e['p25']:.3f} · "
          f"median {e['median']:.3f} · p75 {e['p75']:.3f} · max {e['max']:.3f} "
          f"(n={e['n']})")
        a("")
        a(f"{e['rows_ranked']} rows ranked, {e['rows_excluded']} excluded as too "
          f"tight. {e['purpose']}")
    else:
        a("No R:R rows produced.")
    a("")

    r = c["runtime"]
    a("## Runtime")
    a("")
    a(f"One full capture: **{r['total_seconds']}s** ({r['budget_note']}).")
    a("")
    a("---")
    a("")
    a("Confluence scores measure **agreement between tools**, not edge. "
      "R:R measures **geometry**, not probability. Whether any of it predicts "
      "anything is census work under G-7.")
    return "\n".join(L_)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--slot")
    args = ap.parse_args()

    c = calibrate(args.date, args.slot)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    jp = OUT_DIR / f"BRIEF2_CALIBRATION_{args.date}.json"
    mp = OUT_DIR / f"BRIEF2_CALIBRATION_{args.date}.md"
    jp.write_text(json.dumps(c, indent=1, sort_keys=True, default=str),
                  encoding="utf-8", newline="\n")
    mp.write_text(to_markdown(c), encoding="utf-8", newline="\n")
    print(f"wrote {jp.relative_to(ROOT)}  ({jp.stat().st_size:,} B)")
    print(f"wrote {mp.relative_to(ROOT)}  ({mp.stat().st_size:,} B)")
    i6 = c["item6_dual_scoring_divergence"]
    print(f"\nITEM 6: a line moved on {i6['assets_where_a_line_moved']}/"
          f"{i6['of_assets']} assets, {i6['sides_changed']}/{i6['of_sides']} sides")


if __name__ == "__main__":
    main()
