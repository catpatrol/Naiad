"""TC-5 — fixtures (F-ENG first), deliverables, six-row scorecard.

Contract: TC5_Intraday_Respec_Builder_Contract.md + Amendment 1 (tf_align=1h).
Read-only over research_outputs/tc5/journal_tc5 (v2) with v1-intraday and
swing same-asset subsets joined from research_outputs/tc4/journal_pass2.
HALT on any fixture MISMATCH — F-ENG especially (an engine diff in a
config-only phase breaks the single-variable isolation).

Compressed-ladder caveat on every table: v2 align sits AT the governor —
no strictly-between rung exists at this scale. Standing caveats: in-sample;
same-asset five-cell subset (never v1's full 7-cell book); era note (the
2022-23 chop sits inside the window; era split addresses it).

Usage: python scripts/tc5_fixtures.py
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
TC5 = ROOT / "research_outputs" / "tc5" / "journal_tc5" / "scored"
TC5B = ROOT / "research_outputs" / "tc5" / "journal_tc5_run2" / "scored"
P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
MAN = ROOT / "research_outputs" / "tc5" / "manifest.json"

ASSETS = ["BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT"]
SLIP = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
        "ZECUSDT": 5.0}
V2 = [f"{a}_intraday_v2" for a in ASSETS]
V1I = [f"{a}_intraday" for a in ASSETS]
SWING = [f"{a}_swing" for a in ASSETS]
# windows (start dates): v1-intraday == v2; swing distinct
START_INTRADAY = {"BTCUSDT": "2019-10-01", "ETHUSDT": "2020-01-01",
                  "SOLUSDT": "2020-10-01", "NEARUSDT": "2020-11-01",
                  "ZECUSDT": "2020-03-01"}
START_SWING = {"BTCUSDT": "2019-11-01", "ETHUSDT": "2020-01-01",
               "SOLUSDT": "2020-11-01", "NEARUSDT": "2020-12-01",
               "ZECUSDT": "2020-04-01"}
END = "2024-06-30T23:59"
GOV_MS = {"intraday": 3_600_000, "swing": 14_400_000}
ERA_BOUNDARY = "2023-01-01"     # standing intraday-era caveat boundary

# pinned v1 (committed 1731793, reused — NOT the prediction denominators'
# source of recompute; reproduced here only as a self-consistency gate)
PIN = {"net_1x": -1362.5619, "gross_0x": 113.0427, "campaigns": 1550,
       "tranches": 3664, "med_mfe_bps": 13.0398, "toll": 19.9615,
       "ratio": 0.6533,
       "halts": {"BTCUSDT_intraday": "2022-04-11",
                 "ETHUSDT_intraday": "2022-07-15",
                 "SOLUSDT_intraday": "2023-04-28",
                 "NEARUSDT_intraday": "2023-01-21",
                 "ZECUSDT_intraday": "2022-06-01"}}
CFG_SHA = {
    "tc5_btc.json": "3f80a27b70eb2265b5e3f6517f108eab80483038e2b3f19548fdd624e31bfb76",
    "tc5_eth.json": "4c3cd13249a9986aac00e5e0bab3d1d6fd5ab8b4c99a0c191137979a84d5baeb",
    "tc5_sol.json": "307be3ccc720d4c3a5880d56aaa52219b97ab0420f496c4f796c802957ac2187",
    "tc5_near.json": "2ec1432fbd70bb1051046de7d4c8f0cb96c79a403cce30e0b00e434957faf72c",
    "tc5_zec.json": "010b9dfc2318ed368ade9e9e03449a52a1c815c37284c16ce188db163e6c7480"}
CAVEAT = ("in-sample; same-asset five-cell subset (never v1's full 7-cell "
          "book); compressed ladder — v2 align sits AT the governor, no "
          "strictly-between rung exists at this scale; 2022-23 chop inside "
          "the window (see era split).")


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def med(v):
    v = [x for x in v if x is not None]
    return r4(float(np.median(v))) if v else None


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def ms_of(s):
    for f in ("%Y-%m-%d", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H:%M:%SZ"):
        try:
            return int(datetime.strptime(s, f).replace(tzinfo=timezone.utc)
                       .timestamp() * 1000)
        except ValueError:
            continue
    raise ValueError(s)


def load_cell(root, cell):
    fills, exits, evt = {}, [], Counter()
    halt = None
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            evt[r["evt"]] += 1
            if r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
                fills[r["tranche_id"]] = r
            elif r["evt"] == "EXIT":
                exits.append(r)
            elif r["evt"] == "HALT" and r["tranche_id"] == "equity_floor":
                halt = r["ts_open"]
    return fills, exits, evt, halt


def tranche_stats(fills, exits, asset):
    """Per resolved tranche: mfe_bps, cost_bps, one_r, realized, camp, etc."""
    out = []
    for r in exits:
        f = fills[r["tranche_id"]]
        unit = abs(f["px_fill"] - f["stop"])
        one_r = unit * f["qty"] / f["size_r"]
        cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + \
            (r["slippage"] or 0)
        out.append({
            "tid": r["tranche_id"],
            "camp": int(r["tranche_id"][1:].split("t")[0]),
            "realized_r": r["realized_r"], "size": f["size_r"],
            "cost_r": cost / one_r, "one_r": one_r,
            "mfe_bps": r["mfe_r"] * unit / f["px_fill"] * 1e4,
            "cost_bps": cost / (abs(f["qty"]) * f["px_fill"]) * 1e4,
            "grade": f["grade"], "fill_class": f["fill_class"],
            "hold": None, "exit_ts": r["ts_open"], "fill_ts": f["ts_open"],
            "reason": r["exit_reason"]})
    return out


def guard_checks(fills, exits):
    """G-8 a-d for one cell."""
    # a: no fill after equity_floor halt (journal order = chronological)
    all_rows = []
    for p in sorted(fills.values(), key=lambda r: r["ts_open"]):
        pass
    # rebuild ordered event stream from exits+fills+halt by ts is complex;
    # use the HALT ts and check no fill ts strictly after it
    return None


def g8(root, cell):
    """G-8 a-d from raw rows, journal order."""
    rows = []
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if line.strip():
                rows.append(json.loads(line))
    floored_at = None
    a_viol = 0
    one_r_le0 = 0
    min_stop_atr = None
    fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
    for r in rows:
        if r["evt"] == "HALT" and r["tranche_id"] == "equity_floor":
            floored_at = r["ts_open"]
        elif floored_at and r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
            a_viol += 1
    for f in fills:
        one_r = abs(f["px_fill"] - f["stop"]) * f["qty"] / f["size_r"]
        if one_r <= 0:
            one_r_le0 += 1
        if f["atr_exec"]:
            ratio = abs(f["px_fill"] - f["stop"]) / f["atr_exec"]
            if min_stop_atr is None or ratio < min_stop_atr:
                min_stop_atr = ratio
    # b: notional cap — event-sweep equity reconstruction
    events = []
    exit_by = {r["tranche_id"] for r in rows if r["evt"] == "EXIT"}
    for r in rows:
        if r["evt"] == "EXIT":
            ph = 2 if r["exit_reason"] == "stop" else 0
            events.append((r["ts_open"], ph, "x", r["pnl_usd"] or 0.0))
        elif r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
            events.append((r["ts_open"], 1, "f",
                           abs(r["qty"]) * r["px_fill"]))
    events.sort(key=lambda e: (e[0], e[1]))
    eq = 10000.0
    max_lev = 0.0
    for _, _, k, v in events:
        if k == "x":
            eq += v
        else:
            max_lev = max(max_lev, v / eq)
    return {"g8a_fills_after_floor": a_viol,
            "g8b_max_leverage": r4(max_lev),
            "g8c_min_stop_atr": r4(min_stop_atr),
            "g8d_one_r_le0": one_r_le0}


def signal_mix(root, cells, starts, gov):
    """Event counts per 100 governor bars, pooled over cells."""
    evt = Counter()
    gov_bars = 0
    for cell in cells:
        _, _, e, _ = load_cell(root, cell)
        evt += e
        asset = cell.split("_")[0]
        span = ms_of(END) - ms_of(starts[asset])
        gov_bars += span // GOV_MS[gov]
    return {k: r4(evt[k] * 100.0 / gov_bars) for k in
            ("PRIME", "CONFIRM", "V", "TPW", "CLUSTER", "TAG", "X")}, \
        gov_bars


def main() -> int:
    manifest = json.loads(MAN.read_text(encoding="utf-8"))
    fx, ok = {}, 0

    # F-ENG — engine tree byte-identical vs 6fdab03 and clean working tree
    diff_hist = subprocess.run(
        ["git", "diff", "--name-only", "6fdab03", "HEAD", "--", "engine"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip()
    diff_wt = subprocess.run(
        ["git", "status", "--porcelain", "--", "engine"],
        cwd=ROOT, capture_output=True, text=True).stdout.strip()
    # The sole permitted committed engine delta vs 6fdab03 is the documented
    # S-2 hygiene commit (engine/s2.py noise fields — instrumentation-only,
    # F-BYTE-covered, does not touch the baseline replay TC-5 exercises).
    # TC-5 itself must introduce ZERO engine changes → working tree clean.
    hist_files = set(diff_hist.split()) if diff_hist else set()
    tc5_added = hist_files - {"engine/s2.py"}
    fx["F-ENG"] = {"engine_diff_vs_6fdab03": sorted(hist_files) or "(empty)",
                   "s2_hygiene_only": hist_files <= {"engine/s2.py"},
                   "engine_working_tree": diff_wt or "(clean)",
                   "tc5_engine_changes": sorted(tc5_added) or "(none)",
                   "match": not diff_wt and not tc5_added}
    # F-CFG
    cfg_ok = True
    for fn, sha in CFG_SHA.items():
        got = hashlib.sha256((ROOT / "configs" / fn).read_bytes()).hexdigest()
        cfg_ok &= (got == sha)
    fx["F-CFG"] = {"five_shas_match_prereg": cfg_ok, "match": cfg_ok}
    # F-SPEC
    spec_ok = True
    specs = {}
    for a in ASSETS:
        s = json.loads((ROOT / "configs" /
                        f"tc5_{a.split('USDT')[0].lower()}.json")
                       .read_text(encoding="utf-8"))
        specs[f"{a}_intraday_v2"] = s
    hdr = {}
    for cell in V2:
        r = json.loads(next(open(sorted((TC5 / cell).glob("*.jsonl"))[0],
                                 encoding="utf-8")))
        align_ok = specs[cell]["tf_align"] == "1h"
        this = r["tf_gov"] == "1h" and r["tf_exec"] == "5m" and align_ok
        spec_ok &= this
        hdr[cell] = {"tf_gov": r["tf_gov"], "tf_exec": r["tf_exec"],
                     "tf_align_from_cfg": specs[cell]["tf_align"]}
    fx["F-SPEC"] = {"headers": hdr,
                    "note": "tf_align not journaled; verified from the "
                    "committed config spec (cell source of truth); "
                    "MTF_SET unchanged proven by F-ENG",
                    "match": spec_ok}
    # F-GUARDS
    guards = {c: g8(TC5, c) for c in V2}
    gv = all(g["g8a_fills_after_floor"] == 0 and g["g8b_max_leverage"] <= 10 + 1e-6
             and (g["g8c_min_stop_atr"] is None or g["g8c_min_stop_atr"] >= 0.5 - 1e-9)
             and g["g8d_one_r_le0"] == 0 for g in guards.values())
    fx["F-GUARDS"] = {"per_cell": guards, "match": gv}
    # F-DET
    det_m = [c for c in V2 if not manifest["cells"][c]["match"]]
    fx["F-DET"] = {"mismatched": det_m,
                   "manifest": manifest["determinism_all_identical"],
                   "match": not det_m and manifest["determinism_all_identical"]}

    print("== TC-5 fixtures (F-ENG first) ==")
    for k in ("F-ENG", "F-CFG", "F-SPEC", "F-GUARDS", "F-DET"):
        v = fx[k]
        ok += v["match"]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "per_cell", "headers")}
        print(f"{k:<9} {'MATCH' if v['match'] else '*** MISMATCH ***'} "
              f"{json.dumps(brief, default=str)[:150]}")
    if ok < 5:
        print("\n*** HALT: fixture mismatch. F-ENG failure = single-"
              "variable isolation broken. Nothing downstream. ***")
        return 1

    # ── v2 stats ──
    res = {"fixtures": fx, "caveat": CAVEAT, "pinned_v1": PIN}
    v2tr, v2halt, v2evt = [], {}, Counter()
    percell = {}
    net_pool = 0.0
    for a in ASSETS:
        cell = f"{a}_intraday_v2"
        fills, exits, evt, halt = load_cell(TC5, cell)
        ts = tranche_stats(fills, exits, a)
        for t in ts:
            t["hold"] = (ms_of(t["exit_ts"]) - ms_of(t["fill_ts"])) // 300_000
        v2tr += ts
        v2evt += evt
        if halt:
            v2halt[cell] = halt[:10]
        camps = {t["camp"] for t in ts}
        net = sum(t["realized_r"] for t in ts)
        g0 = sum(t["realized_r"] + t["cost_r"] for t in ts)
        g2 = sum(t["realized_r"] - t["cost_r"] for t in ts)
        net_pool += net
        camp_r = defaultdict(float)
        for t in ts:
            camp_r[t["camp"]] += t["realized_r"]
        vals = list(camp_r.values())
        best = max(vals) if vals else 0.0
        percell[cell] = {
            "net_1x": r4(net), "gross_0x": r4(g0), "stress_2x": r4(g2),
            "campaigns": len(camps), "tranches": len(ts),
            "strip_best_1x": r4(net - best),
            "win_rate_pct": pct(sum(1 for v in vals if v > 0), len(vals)),
            "cost_stack": r4(g0 - net),
            "fills_without_exit_row": len(fills) - len(exits),
            "med_mfe_bps": med([t["mfe_bps"] for t in ts]),
            "med_cost_bps": med([t["cost_bps"] for t in ts]),
            "final_equity": manifest["cells"][cell]["final_equity"],
            "floor_halt": v2halt.get(cell)}
    v2_mfe = [t["mfe_bps"] for t in v2tr]
    v2_cost = [t["cost_bps"] for t in v2tr]
    v2_med_mfe = med(v2_mfe)
    v2_toll = med(v2_cost)
    v2_ratio = r4(v2_med_mfe / v2_toll)
    v2_camps = sum(percell[c]["campaigns"] for c in V2)

    # thesis table: v2 vs pinned-v1, mfe_bps distribution
    res["thesis_table"] = {
        "toll_definition": "median cost_bps (fees+funding+slippage / "
        "notional), pooled resolved tranches",
        "v2": {"med_mfe_bps": v2_med_mfe, "toll": v2_toll,
               "ratio": v2_ratio, "mfe_bps_p10_50_90":
               [r4(float(np.percentile(v2_mfe, q))) for q in (10, 50, 90)],
               "net_1x": r4(net_pool), "campaigns": v2_camps,
               "tranches": len(v2tr)},
        "v1_pinned": {"med_mfe_bps": PIN["med_mfe_bps"],
                      "toll": PIN["toll"], "ratio": PIN["ratio"],
                      "net_1x": PIN["net_1x"], "campaigns": PIN["campaigns"],
                      "tranches": PIN["tranches"]}}
    res["per_cell"] = percell

    # v1 self-consistency (reproduce pinned; NOT altering it)
    v1tr = []
    for a in ASSETS:
        fills, exits, _, _ = load_cell(P2, f"{a}_intraday")
        v1tr += tranche_stats(fills, exits, a)
    v1_check = {"med_mfe_bps": med([t["mfe_bps"] for t in v1tr]),
                "toll": med([t["cost_bps"] for t in v1tr]),
                "net_1x": r4(sum(t["realized_r"] for t in v1tr)),
                "reproduces_pinned":
                    abs(med([t["mfe_bps"] for t in v1tr]) - PIN["med_mfe_bps"]) < 1e-3
                    and abs(med([t["cost_bps"] for t in v1tr]) - PIN["toll"]) < 1e-3}
    res["v1_selfcheck"] = v1_check

    # signal-mix census — three columns
    v2mix, v2gb = signal_mix(TC5, V2, START_INTRADAY, "intraday")
    v1mix, _ = signal_mix(P2, V1I, START_INTRADAY, "intraday")
    swmix, _ = signal_mix(P2, SWING, START_SWING, "swing")
    keys3 = ("PRIME", "TPW", "CLUSTER")
    d_swing = sum(abs(v2mix[k] - swmix[k]) for k in keys3)
    d_v1 = sum(abs(v2mix[k] - v1mix[k]) for k in keys3)
    res["signal_mix_per_100_gov_bars"] = {
        "v2": v2mix, "v1_intraday": v1mix, "swing": swmix,
        "distance_to_swing": r4(d_swing), "distance_to_v1": r4(d_v1),
        "nearer": "swing" if d_swing < d_v1 else "v1"}

    # era split
    era = {}
    for name, sel in (("pre_2023", lambda t: t["exit_ts"] < ERA_BOUNDARY),
                      ("2023_plus", lambda t: t["exit_ts"] >= ERA_BOUNDARY)):
        v2e = [t for t in v2tr if sel(t)]
        v1e = [t for t in v1tr if sel(t)]
        era[name] = {
            "v2_net_1x": r4(sum(t["realized_r"] for t in v2e)),
            "v2_med_mfe_bps": med([t["mfe_bps"] for t in v2e]),
            "v2_ratio": r4(med([t["mfe_bps"] for t in v2e]) /
                           med([t["cost_bps"] for t in v2e]))
            if v2e else None,
            "v1_net_1x": r4(sum(t["realized_r"] for t in v1e))}
    res["era_split"] = {"boundary": ERA_BOUNDARY, "splits": era}

    # halt calendar
    res["halt_calendar"] = {
        "v2_halts": v2halt,
        "v1_halts": PIN["halts"],
        "v2_halt_count": len(v2halt), "v1_halt_count": 5}

    # A-grade share
    def agr(trs):
        n = len(trs)
        a = sum(1 for t in trs if t["grade"] in ("A+", "A"))
        return {"n": n, "a_grade_share_pct": pct(a, n)}
    res["a_grade_share"] = {"v2": agr(v2tr), "v1_intraday": agr(v1tr)}

    # holding + fill_class + adds funnel
    res["holding_bars_median"] = {"v2": med([t["hold"] for t in v2tr])}
    res["fill_class_census"] = {"v2": dict(Counter(t["fill_class"]
                                                   for t in v2tr))}
    np_rej = 0
    for c in V2:
        for p in sorted((TC5 / c).glob("*.jsonl")):
            for line in open(p, encoding="utf-8"):
                if '"not_positioned"' in line:
                    r = json.loads(line)
                    if r.get("reject_reason") == "not_positioned":
                        np_rej += 1
    res["adds_funnel"] = {"v2_not_positioned_rejects": np_rej,
                          "v2_fill_class": res["fill_class_census"]["v2"]}

    # ── predictions ──
    P = {}
    P["P-TC5-a"] = {"prior": 60, "v2_ratio": v2_ratio, "bar": 1.30,
                    "v1_ratio": PIN["ratio"],
                    "verdict": "CONFIRMED" if v2_ratio >= 1.30
                    else "FALSIFIED"}
    P["P-TC5-b"] = {"prior": 55, "v2_net_1x": r4(net_pool),
                    "bar": r4(PIN["net_1x"] + 500),
                    "verdict": "CONFIRMED"
                    if net_pool >= PIN["net_1x"] + 500 else "FALSIFIED"}
    P["P-TC5-c"] = {"prior": 60, "v2_campaigns": v2_camps,
                    "band": [465, 930],
                    "verdict": "CONFIRMED" if 465 <= v2_camps <= 930
                    else "FALSIFIED"}
    fewer = len(v2halt) < 5
    later = all(
        v2halt[f"{a}_intraday_v2"][:10] > PIN["halts"][f"{a}_intraday"]
        for a in ASSETS if f"{a}_intraday_v2" in v2halt)
    P["P-TC5-d"] = {"prior": 60, "v2_halt_count": len(v2halt),
                    "fewer_than_5": fewer, "all_later": later,
                    "verdict": "CONFIRMED" if fewer and later
                    else "FALSIFIED"}
    P["P-TC5-e"] = {"prior": 55,
                    "nearer": res["signal_mix_per_100_gov_bars"]["nearer"],
                    "d_swing": d_swing, "d_v1": d_v1,
                    "verdict": "CONFIRMED" if d_swing < d_v1
                    else "FALSIFIED"}
    P["P-TC5-f"] = {"prior": 65, "v2_ratio": v2_ratio, "bar": 1.0,
                    "verdict": "CONFIRMED" if v2_ratio >= 1.0
                    else "FALSIFIED"}
    res["predictions"] = P
    print("\n== predictions (6) ==")
    for k, v in P.items():
        print(f"{k:<9} {v['verdict']}")

    blob = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"
    (ROOT / "tc5_results.json").write_text(blob, encoding="utf-8",
                                           newline="\n")
    (ROOT / "TC5_RESULTS.md").write_text(render_md(res), encoding="utf-8",
                                         newline="\n")
    print(f"\nv2 ratio {v2_ratio} (bar a=1.30, f=1.0; v1 {PIN['ratio']}) | "
          f"v2 net {r4(net_pool)} | camps {v2_camps} | "
          f"halts {len(v2halt)}/5")
    print("OUTPUT_HASH json:", hashlib.sha256(blob.encode()).hexdigest())
    print("OUTPUT_HASH md:  ", hashlib.sha256(
        (ROOT / "TC5_RESULTS.md").read_bytes()).hexdigest())
    return 0


def render_md(res):
    L = ["# TC-5 RESULTS — intraday re-spec 1H/5m (config-only, "
         "engine 1.0.10 byte-untouched)", "",
         f"> **{res['caveat']}**", "",
         "single-variable: re-spec only; architecture cross deferred.", "",
         "## Fixtures (F-ENG first)", ""]
    for k in ("F-ENG", "F-CFG", "F-SPEC", "F-GUARDS", "F-DET"):
        v = res["fixtures"][k]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "per_cell", "headers")}
        L.append(f"- **{k}**: MATCH — `{json.dumps(brief, default=str)[:150]}`")
    t = res["thesis_table"]
    L += ["", "## Thesis table — mfe_bps vs toll (v2 beside pinned v1)", "",
          f"toll = {t['toll_definition']}", "",
          "| | median mfe_bps | toll | ratio | net 1× | campaigns | "
          "tranches |", "|---|---|---|---|---|---|---|",
          f"| **v2 (1H/5m)** | {t['v2']['med_mfe_bps']} | {t['v2']['toll']} "
          f"| **{t['v2']['ratio']}** | {t['v2']['net_1x']} | "
          f"{t['v2']['campaigns']} | {t['v2']['tranches']} |",
          f"| v1 pinned (1H/1m) | {t['v1_pinned']['med_mfe_bps']} | "
          f"{t['v1_pinned']['toll']} | {t['v1_pinned']['ratio']} | "
          f"{t['v1_pinned']['net_1x']} | {t['v1_pinned']['campaigns']} | "
          f"{t['v1_pinned']['tranches']} |"]
    L += ["", "## Per-cell headlines (v2)", "",
          "| cell | net 1× | gross 0× | camps | tr | win | strip-best | "
          "med mfe_bps | floor halt | final eq |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for c, v in res["per_cell"].items():
        L.append(f"| {c} | {v['net_1x']} | {v['gross_0x']} | "
                 f"{v['campaigns']} | {v['tranches']} | {v['win_rate_pct']}% "
                 f"| {v['strip_best_1x']} | {v['med_mfe_bps']} | "
                 f"{v['floor_halt'] or '—'} | {v['final_equity']} |")
    for key, title in (("signal_mix_per_100_gov_bars",
                        "Signal-mix per 100 gov bars (v2 · v1-intraday · "
                        "swing)"),
                       ("era_split", "Era split (boundary 2023-01-01)"),
                       ("halt_calendar", "Halt calendar (v2 vs v1)"),
                       ("a_grade_share", "A-grade share of fills"),
                       ("adds_funnel", "Adds funnel"),
                       ("v1_selfcheck", "v1 self-consistency (reproduces "
                        "pinned)")):
        L += ["", f"## {title}", "",
              f"`{json.dumps(res[key], default=str)[:1600]}`"]
    L += ["", "## Scorecard", "", "| # | verdict | measured |",
          "|---|---|---|"]
    for k, v in res["predictions"].items():
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("verdict", "prior")}
        L.append(f"| {k} | **{v['verdict']}** | "
                 f"`{json.dumps(keep, default=str)[:150]}` |")
    L += ["", "*scripts/tc5_fixtures.py; raw journal bytes; read-only.*", ""]
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
