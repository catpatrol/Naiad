"""S-2b — Architecture Decomposition Addendum (Tier A: journals only).

Contract: S2b_Decomposition_Addendum_Builder_Contract.md. Read-only
arithmetic over research_outputs/s2/journal_s2 (engine 1.0.10, PASS at
6fdab03), joined to fills in the same journal. No engine execution, no
config change, no network, no evidence spend.

Every cross-architecture table STATES ITS DENOMINATOR: baseline and
corrected-fold-in R are baseline-denominated (native `one_r`); the F4
struct books are denominated in the wider structural `one_r`. Standing
caveats: in-sample · first-order (rail/halt/equity feedback ignored,
entries fixed) · 1x-proxy costs · flatten-reason split is the disclosed
proxy · JTO/TAO 1d never enters the level anchors here (F4 uses exec/30m/1h
only).

Usage: python scripts/s2b_decompose.py
"""
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
S2J = ROOT / "research_outputs" / "s2" / "journal_s2" / "scored"

CAND = "ema200_gov_b0.5"          # the ratified TC-1 fold-in form
TL_CANDS = ["ema200_gov_b0.5", "ema200_gov_b0.0", "ema89_gov_b0.0"]
MANDATES = ["swing", "intraday", "position"]
SLIP = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
        "ZECUSDT": 5.0, "JTOUSDT": 5.0, "TAOUSDT": 5.0}
DEATH_REASONS = {"failure_x", "opposite_cross", "v_reversal",
                 "campaign_died", "equity_floor"}
# fixture references — the in-session scan of 2026-07-19
F1_REF = (-1796.9930, 275.9924, 2599, 10.8503)
F2_REF = {"30m": (4493, 9, 15, 1755, 7, 363.5363),
          "1h": (3997, 8, 15, 2259, 0, 565.5794)}
F3_REF = {"30m": 742.94, "1h": 606.99, "baseline": 2072.98,
          "1h_ident": 1466.0, "1h_gross": 896.6}
F4_REF = (506.279, 384.2388)
BASELINE_COST_STACK = 2072.9854


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def med(vals):
    vals = [v for v in vals if v is not None]
    return r4(float(np.median(vals))) if vals else None


def toll(asset):
    return 2.0 * (5.0 + SLIP[asset])          # roundtrip cost bps, per tier


def load():
    cells = sorted(p.name for p in S2J.iterdir() if p.is_dir())
    tr = []
    for cell in cells:
        asset = cell.rpartition("_")[0]
        mand = cell.rpartition("_")[2]
        fills = {}
        exits = []
        for p in sorted((S2J / cell).glob("*.jsonl")):
            for line in open(p, encoding="utf-8"):
                if not line.strip():
                    continue
                r = json.loads(line)
                if r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
                    fills[r["tranche_id"]] = r
                elif r["evt"] == "EXIT":
                    exits.append(r)
        # campaign baseline flatten reasons (for the ride-to-death split)
        camp_flat = {}
        for r in exits:
            if r["exit_reason"] not in ("stop", "stop_gap"):
                camp = int(r["tranche_id"][1:].split("t")[0])
                camp_flat[camp] = r["exit_reason"]
        for r in exits:
            f = fills[r["tranche_id"]]
            camp = int(r["tranche_id"][1:].split("t")[0])
            cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + \
                (r["slippage"] or 0)
            unit0 = abs(f["px_fill"] - f["stop"])
            one_r = unit0 * f["qty"] / f["size_r"]
            base_bps = unit0 / f["px_fill"] * 1e4
            tr.append({
                "cell": cell, "asset": asset, "mandate": mand,
                "camp": (cell, camp), "tid": r["tranche_id"],
                "size": f["size_r"], "px": f["px_fill"],
                "cost_r": cost / one_r,
                "realized_r": r["realized_r"],
                "base_off": None,               # filled in main() via _off
                "reason": r["exit_reason"],
                "base_bps": base_bps, "toll": toll(asset),
                "f4": r["s2"]["f4"], "tl": r["s2"]["tl"],
                "camp_flat": camp_flat.get(camp),
                "exit_ts": r["ts_open"], "fill_ts": f["ts_open"],
            })
    return cells, tr


def _off(fill_ts, exit_ts, mandate):
    from datetime import datetime
    step = {"intraday": 60_000, "swing": 300_000,
            "position": 900_000}[mandate]
    def ms(s):
        return int(datetime.fromisoformat(s.replace("Z", "+00:00"))
                   .timestamp() * 1000)
    return (ms(exit_ts) - ms(fill_ts)) // step


# ── per-architecture per-tranche view ───────────────────────────────────
def arch_row(t, arch):
    """Return (r1x, r0x, holding_off, reason, denom) or None to skip.
    denom in {'baseline-R', 'struct-R'}."""
    if arch == "baseline":
        return (t["realized_r"], t["realized_r"] + t["cost_r"],
                t["base_off"], t["reason"], "baseline-R")
    if arch == "fold":
        rec = t["tl"][CAND]
        g = rec["fold_exit_r"] * t["size"]
        return (g - t["cost_r"], g, rec["fold_off"], rec["fold_kind"],
                "baseline-R")
    tf = "30m" if arch == "struct30" else "1h"
    v = t["f4"][tf]
    if v.get("void"):
        return (t["realized_r"], t["realized_r"] + t["cost_r"],
                t["base_off"], "void_baseline_kept", "struct-R")
    ratio = t["base_bps"] / v["stop_dist_bps"]
    g = v["exit_r_struct"] * t["size"]
    reason = v["exit_kind"]
    if reason == "flatten":
        reason = ("flatten_ride_to_death" if t["camp_flat"] is None
                  else "flatten_baseline_death")
    return (g - t["cost_r"] * ratio, g, v["exit_i_offset"], reason,
            "struct-R")


def book(tr, arch, sel=None):
    rows = [arch_row(t, arch) for t in tr
            if sel is None or sel(t)]
    s1 = sum(r[0] for r in rows)
    s0 = sum(r[1] for r in rows)
    camp = defaultdict(float)
    for t, r in zip([t for t in tr if sel is None or sel(t)], rows):
        camp[t["camp"]] += r[0]
    vals = list(camp.values())
    best = max(vals) if vals else 0.0
    top10 = sum(sorted(vals, reverse=True)[:10])
    return {
        "sum_0x": r4(s0), "sum_1x_proxy": r4(s1),
        "cost_stack": r4(s0 - s1),
        "campaigns": len(vals), "tranches": len(rows),
        "win_rate_pct": pct(sum(1 for v in vals if v > 0), len(vals)),
        "strip_best_1x": r4(s1 - best),
        "top10_share_of_sum_wins_pct":
            pct(top10, sum(v for v in vals if v > 0))
            if any(v > 0 for v in vals) else None,
        "sign_flip_on_strip": bool((s1 > 0) != (s1 - best > 0)),
    }


def main() -> int:
    cells, tr = load()
    for t in tr:
        t["base_off"] = _off(t["fill_ts"], t["exit_ts"], t["mandate"])

    fx, ok = {}, 0
    # F1
    camp_r = defaultdict(float)
    for t in tr:
        camp_r[t["camp"]] += t["realized_r"]
    s1 = sum(camp_r.values())
    s0 = sum(t["realized_r"] + t["cost_r"] for t in tr)
    win = sum(1 for v in camp_r.values() if v > 0)
    fx["F1"] = {"sum_1x": r4(s1), "sum_0x": r4(s0),
                "campaigns": len(camp_r), "win_pct": pct(win, len(camp_r)),
                "match": abs(s1 - F1_REF[0]) < 1e-3
                and abs(s0 - F1_REF[1]) < 1e-3 and len(camp_r) == F1_REF[2]}
    # F2 — F4 census
    f2 = {}
    for tf, arch in (("30m", "struct30"), ("1h", "struct1h")):
        cen = Counter()
        bk = book(tr, arch)
        for t in tr:
            r = arch_row(t, arch)
            cen[r[3]] += 1
        stop = cen["stop"]
        gap = cen["gap"]
        death = cen["flatten_baseline_death"]
        ride = cen["flatten_ride_to_death"]
        void = cen["void_baseline_kept"]
        exp = F2_REF[tf]
        f2[tf] = {"stop": stop, "gap": gap, "baseline_death": death,
                  "ride_to_death": ride, "void": void,
                  "book_1x": bk["sum_1x_proxy"],
                  "match": (stop, gap, death, ride, void) ==
                  exp[:5] and abs(bk["sum_1x_proxy"] - exp[5]) < 5e-3}
    fx["F2"] = {**f2, "match": f2["30m"]["match"] and f2["1h"]["match"]}
    # F3 — cost stacks + 1h decomposition
    b30 = book(tr, "struct30")
    b1h = book(tr, "struct1h")
    base_cost = s0 - s1
    swing_1h = b1h["sum_1x_proxy"] - s1
    ident = base_cost - b1h["cost_stack"]
    gross = b1h["sum_0x"] - s0
    fx["F3"] = {"cost_30m": b30["cost_stack"], "cost_1h": b1h["cost_stack"],
                "baseline_cost": r4(base_cost),
                "1h_swing": r4(swing_1h),
                "1h_cost_identity": r4(ident),
                "1h_gross": r4(gross),
                "1h_ident_pct": pct(ident, swing_1h),
                "match": abs(b30["cost_stack"] - F3_REF["30m"]) < 5e-2
                and abs(b1h["cost_stack"] - F3_REF["1h"]) < 5e-2
                and abs(base_cost - F3_REF["baseline"]) < 5e-2
                and abs(ident - F3_REF["1h_ident"]) < 1.0
                and abs(gross - F3_REF["1h_gross"]) < 1.0}
    # F4 — corrected fold-in
    fold0 = sum(t["tl"][CAND]["fold_exit_r"] * t["size"] for t in tr)
    posfold1 = sum(t["tl"][CAND]["fold_exit_r"] * t["size"] - t["cost_r"]
                   for t in tr if t["mandate"] == "position")
    fx["F4"] = {"fold_grid_0x": r4(fold0),
                "fold_position_1x_proxy": r4(posfold1),
                "match": abs(fold0 - F4_REF[0]) < 5e-3
                and abs(posfold1 - F4_REF[1]) < 5e-3}

    print("== S-2b fixtures ==")
    for k in ("F1", "F2", "F3", "F4"):
        m = fx[k]["match"]
        ok += m
        brief = {kk: vv for kk, vv in fx[k].items() if kk != "match"}
        print(f"{k:<3} {'MATCH' if m else '*** MISMATCH ***'} "
              f"{json.dumps(brief, default=str)[:180]}")
    if ok < 4:
        print("\n*** HALT: fixture mismatch — computed vs expected above. "
              "Nothing downstream. ***")
        return 1

    ARCHS = [("baseline", "baseline-R"), ("fold", "baseline-R"),
             ("struct30", "struct-R"), ("struct1h", "struct-R")]
    res = {"fixtures": fx,
           "caveat": ("in-sample; first-order (rail/halt/equity feedback "
                      "ignored, entries fixed); 1x-proxy costs; struct "
                      "books denominated in the wider structural one_r; "
                      "flatten-reason split is the disclosed proxy")}

    # ── D1 decision table ──
    d1 = {}
    for arch, denom in ARCHS:
        row = {"denominator": denom, "GRID": book(tr, arch)}
        for m in MANDATES:
            row[m] = book(tr, arch, lambda t, m=m: t["mandate"] == m)
        d1[arch] = row
    d1["struct_ratcheting"] = {"denominator": "struct-R",
                               "status": "NAMED-UNMEASURED (blank by "
                               "design): re-anchors the structural stop to "
                               "each newer confirmed pivot; not priced this "
                               "phase — TC-1's cell"}
    res["D1_decision_table"] = d1

    # ── D2 concentration ──
    d2 = {}
    for arch, _ in ARCHS:
        d2[arch] = {"GRID": {k: d1[arch]["GRID"][k] for k in
                             ("sum_1x_proxy", "strip_best_1x",
                              "top10_share_of_sum_wins_pct",
                              "sign_flip_on_strip")}}
        for m in MANDATES:
            d2[arch][m] = {k: d1[arch][m][k] for k in
                           ("sum_1x_proxy", "strip_best_1x",
                            "top10_share_of_sum_wins_pct",
                            "sign_flip_on_strip")}
    res["D2_concentration"] = d2

    # ── D3 distributions ──
    d3 = {"holding_bars_median": {}, "win_rate_by_exit_reason": {},
          "denominator_ratio_bps": {}}
    for arch, _ in ARCHS:
        d3["holding_bars_median"][arch] = {
            m: med([arch_row(t, arch)[2] for t in tr
                    if t["mandate"] == m]) for m in MANDATES}
        by = defaultdict(lambda: [0, 0])
        for t in tr:
            r = arch_row(t, arch)
            by[r[3]][0] += 1
            by[r[3]][1] += 1 if r[0] > 0 else 0
        d3["win_rate_by_exit_reason"][arch] = {
            k: {"n": v[0], "win_pct": pct(v[1], v[0])}
            for k, v in sorted(by.items())}
    for tf, arch in (("30m", "struct30"), ("1h", "struct1h")):
        d3["denominator_ratio_bps"][tf] = {}
        for m in MANDATES:
            ratios = [t["f4"][tf]["stop_dist_bps"] / t["base_bps"]
                      for t in tr if t["mandate"] == m
                      and not t["f4"][tf].get("void")]
            d3["denominator_ratio_bps"][tf][m] = {
                "n": len(ratios),
                "p25_50_75": [r4(float(np.percentile(ratios, q)))
                              for q in (25, 50, 75)] if ratios else None}
    res["D3_distributions"] = d3

    # ── D4 fold-in mirror ──
    fold_cen = Counter()
    for t in tr:
        k = t["tl"][CAND]["fold_kind"]
        eng = t["tl"][CAND]["engaged_off"]
        off = t["tl"][CAND]["fold_off"]
        if k == "flatten":
            fold_cen["flatten"] += 1
        elif eng is not None and off >= eng:
            fold_cen["trail_exit_post_engage"] += 1
        else:
            fold_cen["native_stop_pre_engage"] += 1
    fold_cost = sum(t["cost_r"] for t in tr)
    fold0 = d1["fold"]["GRID"]["sum_0x"]
    fold_swing = d1["fold"]["GRID"]["sum_1x_proxy"] - s1
    res["D4_fold_mirror"] = {
        "exit_census": dict(fold_cen),
        "cost_stack": r4(fold_cost),
        "baseline_cost_stack": r4(base_cost),
        "cost_identity_component": r4(fold_cost - base_cost),
        "gross_component": r4(fold0 - s0),
        "swing_vs_baseline": r4(fold_swing),
        "note": "cost-identity component should be ~0 (same entries, same "
                "baseline denominator, cost_r unchanged) — the "
                "decomposition-method sanity check; nonzero would mean the "
                "cost split is mis-derived"}

    # ── D5 m=2 overlap ──
    flagged = [t for t in tr if t["base_bps"] < 2.0 * t["toll"]]
    d5 = {"m2_flagged_fills": len(flagged),
          "denominator": "baseline stop_bps < 2xtoll; struct clears iff "
          "struct stop_dist_bps >= 2xtoll"}
    for tf in ("30m", "1h"):
        clears = sum(1 for t in flagged
                     if not t["f4"][tf].get("void")
                     and t["f4"][tf]["stop_dist_bps"] >= 2.0 * t["toll"])
        voidn = sum(1 for t in flagged if t["f4"][tf].get("void"))
        d5[f"clears_2xtoll_under_{tf}"] = {
            "n": clears, "pct": pct(clears, len(flagged)),
            "still_under_or_void": len(flagged) - clears,
            "void_in_flagged": voidn}
    # complement: floor passes but struct still under 2xtoll
    passed = [t for t in tr if t["base_bps"] >= 2.0 * t["toll"]]
    for tf in ("30m", "1h"):
        under = sum(1 for t in passed
                    if not t["f4"][tf].get("void")
                    and t["f4"][tf]["stop_dist_bps"] < 2.0 * t["toll"])
        d5[f"floor_passes_but_{tf}_under"] = under
    res["D5_m2_overlap"] = d5

    # ── D6 PARTIAL ──
    interact = sum(
        1 for t in tr
        if t["tl"][CAND]["engaged_off"] is not None
        and t["tl"][CAND]["fold_kind"] in ("stop", "gap")
        and t["tl"][CAND]["fold_off"] >= t["tl"][CAND]["engaged_off"]
        and not t["f4"]["1h"].get("void")
        and t["tl"][CAND]["fold_off"] < t["f4"]["1h"]["exit_i_offset"])
    res["D6_joint"] = {
        "status": "PARTIAL",
        "missing_field": "the gov-e200 trail re-seeded/re-walked under the "
        "STRUCTURAL stop as phase-1 floor. Journals carry the "
        "native-seeded trail (fold book) and the fixed structural stop "
        "(struct book) but NOT their interaction: the joint's trail would "
        "seed at the wider structural stop, so the native-seeded fold "
        "trail is not a faithful substitute. A naive first-touch min() "
        "over the two journaled books would misprice exactly the "
        "pre-engagement region (fold native-stop exits the joint replaces "
        "with the wider structural floor). No joint R priced.",
        "diagnostic_interaction_region_1h": interact,
        "diagnostic_note": "tranches where the post-engagement fold trail "
        "exits strictly before the 1h structural stop — the region where "
        "the two lines genuinely interact and TC-1's re-simulation is "
        "required. Descriptive only.",
        "reviewer_ruling": "the real interaction is TC-1's fourth cell "
        "either way (contract 4.D6)"}

    # ── D7 ride-to-death anatomy ──
    d7 = {}
    for tf, arch in (("30m", "struct30"), ("1h", "struct1h")):
        per = {}
        for m in MANDATES:
            sel = [t for t in tr if t["mandate"] == m
                   and not t["f4"][tf].get("void")
                   and t["f4"][tf]["exit_kind"] == "flatten"
                   and t["camp_flat"] is None]
            cellr = [arch_row(t, arch)[0] for t in sel]
            bars = [t["f4"][tf]["exit_i_offset"] for t in sel]
            per[m] = {"n": len(sel), "mean_cell_r": r4(np.mean(cellr))
                      if cellr else None,
                      "mean_bars": r4(np.mean(bars)) if bars else None}
        d7[tf] = per
    res["D7_ride_to_death"] = {
        "denominator": "struct-R", "per_mandate": d7,
        "note": "the shape of what the doctrine actually buys: baseline "
                "stopped these out, the structural stop rode them to "
                "campaign death"}

    # ── predictions ──
    P = {}
    intr_1h = d1["struct1h"]["intraday"]["sum_1x_proxy"]
    P["P-S2b-1"] = {"prior": 60, "f4_1h_intraday_1x": intr_1h,
                    "denominator": "struct-R",
                    "verdict": "CONFIRMED" if intr_1h > 0 else "FALSIFIED"}
    sb = d1["struct1h"]["GRID"]["strip_best_1x"]
    P["P-S2b-2"] = {"prior": 65, "f4_1h_grid_strip_best": sb,
                    "verdict": "CONFIRMED" if sb > 0 else "FALSIFIED"}
    dev = abs(fold_cost - BASELINE_COST_STACK) / BASELINE_COST_STACK * 100
    P["P-S2b-3"] = {"prior": 70, "fold_cost_stack": r4(fold_cost),
                    "deviation_pct": r4(dev),
                    "verdict": "CONFIRMED" if dev <= 15 else "FALSIFIED"}
    share = d5["clears_2xtoll_under_1h"]["pct"]
    P["P-S2b-4"] = {"prior": 60, "clears_1h_pct": share,
                    "verdict": "CONFIRMED" if (share or 0) >= 70
                    else "FALSIFIED"}
    hold = d3["holding_bars_median"]
    ratios = {m: (hold["struct1h"][m] / hold["baseline"][m]
                  if hold["baseline"][m] else None) for m in MANDATES}
    all3 = all(v is not None and v >= 3.0 for v in ratios.values())
    P["P-S2b-5"] = {"prior": 60,
                    "hold_ratio_1h_vs_baseline":
                        {m: r4(v) for m, v in ratios.items()},
                    "verdict": "CONFIRMED" if all3 else "FALSIFIED"}
    res["predictions"] = P
    print("\n== predictions ==")
    for k, v in P.items():
        print(f"{k:<9} {v['verdict']}")

    blob = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"
    (ROOT / "s2b_results.json").write_text(blob, encoding="utf-8",
                                           newline="\n")
    (ROOT / "S2B_DECOMPOSITION.md").write_text(render_md(res),
                                               encoding="utf-8",
                                               newline="\n")
    print("\nOUTPUT_HASH json:",
          hashlib.sha256(blob.encode()).hexdigest())
    print("OUTPUT_HASH md:  ", hashlib.sha256(
        (ROOT / "S2B_DECOMPOSITION.md").read_bytes()).hexdigest())
    return 0


def _brow(name, r):
    if "status" in r:
        return f"| {name} | *{r['status']}* | | | | | | |"
    g = r["GRID"]
    return (f"| {name} ({r['denominator']}) | {g['sum_0x']} | "
            f"{g['sum_1x_proxy']} | {g['strip_best_1x']} | "
            f"{g['win_rate_pct']}% | {g['campaigns']}/{g['tranches']} | "
            f"{g['cost_stack']} |")


def render_md(res):
    L = ["# S-2b — Architecture Decomposition (Tier A, journals only)", "",
         f"> **{res['caveat']}**", "",
         "Every table states its denominator. baseline & fold-in = "
         "baseline-R (native one_r); F4 struct books = struct-R (wider "
         "structural one_r). Not comparable across denominators without "
         "that note.", "",
         "## Fixtures", ""]
    for k in ("F1", "F2", "F3", "F4"):
        v = res["fixtures"][k]
        L.append(f"- **{k}**: MATCH — `" + json.dumps(
            {kk: vv for kk, vv in v.items() if kk != "match"},
            default=str)[:150] + "`")
    L += ["", "## D1 — Architecture decision table (GRID)", "",
          "| architecture (denom) | 0x | 1x-proxy | strip-best 1x | win | "
          "camps/tr | cost stack |", "|---|---|---|---|---|---|---|"]
    for arch in ("baseline", "fold", "struct30", "struct1h",
                 "struct_ratcheting"):
        L.append(_brow(arch, res["D1_decision_table"][arch]))
    L += ["", "### D1 per-mandate 1x-proxy (denominators as above)", "",
          "| architecture | swing | intraday | position |",
          "|---|---|---|---|"]
    for arch in ("baseline", "fold", "struct30", "struct1h"):
        r = res["D1_decision_table"][arch]
        L.append(f"| {arch} | {r['swing']['sum_1x_proxy']} | "
                 f"{r['intraday']['sum_1x_proxy']} | "
                 f"{r['position']['sum_1x_proxy']} |")
    for key, title in (("D2_concentration", "D2 — Concentration"),
                       ("D3_distributions", "D3 — Distributions"),
                       ("D4_fold_mirror", "D4 — Fold-in mirror "
                        "decomposition"),
                       ("D5_m2_overlap", "D5 — m=2 overlap"),
                       ("D6_joint", "D6 — Joint first-passage (PARTIAL)"),
                       ("D7_ride_to_death", "D7 — Ride-to-death anatomy")):
        L += ["", f"## {title}", "",
              f"`{json.dumps(res[key], default=str)[:2400]}`"]
    L += ["", "## Prediction scorecard", "",
          "| # | verdict | measured |", "|---|---|---|"]
    for k, v in res["predictions"].items():
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("verdict", "prior")}
        L.append(f"| {k} | **{v['verdict']}** | "
                 f"`{json.dumps(keep, default=str)[:150]}` |")
    L += ["", "*scripts/s2b_decompose.py; raw journal bytes; read-only.*",
          ""]
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
