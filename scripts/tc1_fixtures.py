"""TC-1 — fixtures (F-A-BYTE first), per-cell headlines, factorial
interaction table, eight-row scorecard.

Contract: TC1_Factorial_Builder_Contract.md + TC1_DEFINITIONS.md. Read-only
over research_outputs/tc1/{A, B_run1, C_run1, D_run1} with journal_pass2 as
the A reference; the 1h frame is reloaded per B/D cell (offline) to
independently recompute the structural stop. HALT on any fixture MISMATCH;
F-A-BYTE / F-SIG-ALL failure = the config gating is broken.

Denominators: A and C are baseline-R (native one_r); B and D are struct-R
(the engine sizes qty on the structural distance, so realized_r is natively
risk-normalized to the wider stop). Stated on every B/D table.

Usage: python scripts/tc1_fixtures.py
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
sys.path.insert(0, str(ROOT))
TC1 = ROOT / "research_outputs" / "tc1"
PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"
MAN = TC1 / "manifest.json"

CELLS = {
    "BTCUSDT_intraday": "2019-10-01", "BTCUSDT_position": "2020-01-01",
    "BTCUSDT_swing": "2019-11-01", "ETHUSDT_intraday": "2020-01-01",
    "ETHUSDT_position": "2020-04-01", "ETHUSDT_swing": "2020-01-01",
    "JTOUSDT_intraday": "2024-01-01", "JTOUSDT_position": "2024-04-01",
    "JTOUSDT_swing": "2024-02-01", "NEARUSDT_intraday": "2020-11-01",
    "NEARUSDT_position": "2021-02-01", "NEARUSDT_swing": "2020-12-01",
    "SOLUSDT_intraday": "2020-10-01", "SOLUSDT_position": "2021-01-01",
    "SOLUSDT_swing": "2020-11-01", "TAOUSDT_intraday": "2024-05-01",
    "TAOUSDT_swing": "2024-06-01", "ZECUSDT_intraday": "2020-03-01",
    "ZECUSDT_position": "2020-06-01", "ZECUSDT_swing": "2020-04-01"}
END = "2024-06-30T23:59"
ARMS = {"A": "A", "B": "B_run1", "C": "C_run1", "D": "D_run1"}
DENOM = {"A": "baseline-R", "B": "struct-R", "C": "baseline-R",
         "D": "struct-R"}
A_TRANCHES = 6304
CFG_REF = {  # from pre-registration c9d9821
    "tc1_A": "311a1cd3d1e950e3bb8b8c54eefe305b8c56f9a5517c4520076cf9c4fa76edc0",
    "tc1_B": "3e99401d427fedd96842cc4df15c329220b8ec43e93bd6543c62de7acb3f636b",
    "tc1_C": "462c4e46f1501386b66dd67bccf099e0223d1bd1ee098372cace84b65a8bf4fa",
    "tc1_D": "37f6869631db2b831ea9413fa91799cdfd78bd8e6bbac01330af2e1574bef6c0"}
SIG_EVTS = {"REGIME", "STAGE", "TAG", "PRIME", "CONFIRM", "V", "TPW",
            "CLUSTER", "X"}
CAVEAT = ("in-sample; REAL runs (path effects — re-entry suppression, "
          "concurrency, funding, rail/halt feedback — are measured, not "
          "noise); B/D denominated in struct-R, A/C in baseline-R; "
          "prediction basis s2b D1 (the 38% gross, not the +2360 headline).")


def r4(x):
    return None if x is None else round(float(x) + 0.0, 4)


def med(v):
    v = [x for x in v if x is not None]
    return r4(float(np.median(v))) if v else None


def pct(x, d):
    return None if not d else r4(100.0 * x / d)


def mand(cell):
    return cell.rpartition("_")[2]


def ms_of(s):
    return int(datetime.fromisoformat(s.replace("Z", "+00:00"))
               .timestamp() * 1000)


def root_of(arm):
    return TC1 / ARMS[arm] / "scored"


def _norm(line):
    r = json.loads(line)
    r.pop("s1", None); r.pop("s2", None)
    r["run_id"] = r["engine_version"] = r["config_id"] = "-"
    return json.dumps(r, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False)


def sig_lines(root, cell):
    out = []
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if not line.strip():
                continue
            r = json.loads(line)
            if r["evt"] in SIG_EVTS or (r["evt"] == "REJECT"
                                        and not (r["tranche_id"] or "")
                                        .startswith("trade_")):
                out.append(_norm(line))
    return out


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


def tstats(fills, exits):
    out = []
    for r in exits:
        f = fills[r["tranche_id"]]
        cost = (r["fees"] or 0) + (r["funding_cum"] or 0) + (r["slippage"] or 0)
        unit = abs(f["px_fill"] - f["stop"])
        one_r = unit * f["qty"] / f["size_r"]
        out.append({
            "tid": r["tranche_id"], "mandate": mand(f["cell_id"]),
            "camp": int(r["tranche_id"][1:].split("t")[0]),
            "realized_r": r["realized_r"], "size": f["size_r"],
            "cost_r": cost / one_r, "dir": 1 if f["dir"] == "long" else -1,
            "entry_stop": f["stop"], "px_fill": f["px_fill"],
            "atr_exec": f["atr_exec"], "fill_ts": f["ts_open"],
            "exit_raw": r["stop"], "reason": r["exit_reason"],
            "fill_class": f["fill_class"], "grade": f["grade"],
            "hold": None})
    return out


def book(trs, sel=None):
    ts = [t for t in trs if sel is None or sel(t)]
    s1 = sum(t["realized_r"] for t in ts)
    s0 = sum(t["realized_r"] + t["cost_r"] for t in ts)
    s2 = sum(t["realized_r"] - t["cost_r"] for t in ts)
    camp = defaultdict(float)
    for t in ts:
        camp[(t["mandate"], t["camp"])] += t["realized_r"]
    vals = list(camp.values())
    best = max(vals) if vals else 0.0
    return {"sum_1x": r4(s1), "sum_0x": r4(s0), "sum_2x": r4(s2),
            "tranches": len(ts), "campaigns": len(vals),
            "win_rate_pct": pct(sum(1 for v in vals if v > 0), len(vals)),
            "strip_best_1x": r4(s1 - best), "cost_stack": r4(s0 - s1)}


def g8(root, cell):
    rows = []
    for p in sorted((root / cell).glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            if line.strip():
                rows.append(json.loads(line))
    floored, a_viol, one_r_le0, min_sa = None, 0, 0, None
    fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
    for r in rows:
        if r["evt"] == "HALT" and r["tranche_id"] == "equity_floor":
            floored = True
        elif floored and r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
            a_viol += 1
    for f in fills:
        one_r = abs(f["px_fill"] - f["stop"]) * f["qty"] / f["size_r"]
        if one_r <= 0:
            one_r_le0 += 1
        if f["atr_exec"]:
            ratio = abs(f["px_fill"] - f["stop"]) / f["atr_exec"]
            if min_sa is None or ratio < min_sa:
                min_sa = ratio
    events, eq, max_lev = [], 10000.0, 0.0
    for r in rows:
        if r["evt"] == "EXIT":
            events.append((r["ts_open"], 2 if r["exit_reason"] == "stop"
                           else 0, "x", r["pnl_usd"] or 0.0))
        elif r["evt"] in ("ENTRY_FILL", "ADD_FILL"):
            events.append((r["ts_open"], 1, "f", abs(r["qty"]) * r["px_fill"]))
    events.sort(key=lambda e: (e[0], e[1]))
    for _, _, k, v in events:
        if k == "x":
            eq += v
        else:
            max_lev = max(max_lev, v / eq)
    return {"g8a": a_viol, "g8b_max_lev": r4(max_lev),
            "g8c_min_stop_atr": r4(min_sa), "g8d_one_r_le0": one_r_le0}


def struct_recompute_viol(cell, trs):
    """Independently recompute the structural stop for each fill from the
    1h frame and compare to the journaled entry stop. Returns violations."""
    from engine import data as dl
    from engine.replay import warmup_anchor_ms
    from engine.cells import cell_by_id
    from engine.s1 import _pivots
    c = cell_by_id(cell)
    anchor = warmup_anchor_ms(c, ms_of(CELLS[cell]))
    oneh = dl.load_klines(c.symbol, "1h", anchor, ms_of(END))
    ot = oneh["open_time"].to_numpy(np.int64)
    close1h = ot + 3_600_000
    lc, lv = _pivots(oneh["low"].to_numpy(float), 5, 5, low=True)
    hc, hv = _pivots(oneh["high"].to_numpy(float), 5, 5, low=False)
    lconf_close = close1h[lc]      # confirmation 1h bar's close time
    hconf_close = close1h[hc]
    lp1h, hp1h = lc - 5, hc - 5    # pivot's own 1h index
    viol = 0
    for t in trs:
        fts = ms_of(t["fill_ts"])
        cur1h = int(np.searchsorted(close1h, fts, side="right")) - 1
        a = t["atr_exec"]
        if a is None:
            continue
        if t["dir"] == 1:
            elig = (lconf_close <= fts) & (cur1h - lp1h <= 200) & \
                (lv < t["px_fill"])
            if not elig.any():
                viol += 1
                continue
            pv = float(lv[elig].max())
            exp = pv - 0.5 * a
        else:
            elig = (hconf_close <= fts) & (cur1h - hp1h <= 200) & \
                (hv > t["px_fill"])
            if not elig.any():
                viol += 1
                continue
            pv = float(hv[elig].min())
            exp = pv + 0.5 * a
        if abs(exp - t["entry_stop"]) > 1e-4:
            viol += 1
    return viol


def main() -> int:
    manifest = json.loads(MAN.read_text(encoding="utf-8"))
    fx, ok = {}, 0

    # cache per-arm tranche stats
    data = {}
    for arm in "ABCD":
        allt, halts, evt, fwe = [], {}, Counter(), {}
        for cell in sorted(CELLS):
            fills, exits, e, halt = load_cell(root_of(arm), cell)
            ts = tstats(fills, exits)
            for t in ts:
                # holding in exec bars from ts is approximate; use exit-fill
                pass
            allt += ts
            evt += e
            if halt:
                halts[cell] = halt[:10]
            fwe[cell] = len(fills) - len(exits)
        data[arm] = {"tr": allt, "halts": halts, "evt": evt, "fwe": fwe}

    # F-A-BYTE
    mism = []
    for cell in sorted(CELLS):
        a = [_norm(l) for p in sorted((root_of("A") / cell).glob("*.jsonl"))
             for l in open(p, encoding="utf-8") if l.strip()]
        b = [_norm(l) for p in sorted((PASS2 / cell).glob("*.jsonl"))
             for l in open(p, encoding="utf-8") if l.strip()]
        if a != b:
            mism.append(cell)
    fx["F-A-BYTE"] = {"mismatched_cells": mism, "match": not mism}
    # F-SIG-ALL
    sig_mism = []
    for cell in sorted(CELLS):
        sa = sig_lines(root_of("A"), cell)
        for arm in ("B", "C", "D"):
            if sig_lines(root_of(arm), cell) != sa:
                sig_mism.append((cell, arm))
    fx["F-SIG-ALL"] = {"mismatched": sig_mism, "match": not sig_mism}
    # F-ARCH-B — recompute the structural stop per B/D fill from the 1h
    # frame and compare to the journaled entry stop; B static.
    # The static/one-way property lives on intra-bar `stop` exits (fill AT
    # the stop level). `stop_gap` fills at the bar OPEN (invariant 3) — a
    # gap-down through a static/one-way stop fills below it, which is the gap
    # model, not a stop-level move; checked separately for consistency.
    b_static = 0        # B intra-bar stop-exit fill != entry stop
    b_gap_bad = 0       # B stop_gap not through the static stop
    struct_viol = 0
    for cell in sorted(CELLS):
        for arm in ("B", "D"):
            fills, exits, _, _ = load_cell(root_of(arm), cell)
            trs = tstats(fills, exits)
            struct_viol += struct_recompute_viol(cell, trs)
            if arm == "B":
                for t in trs:
                    if t["exit_raw"] is None:
                        continue
                    if t["reason"] == "stop" and \
                            abs(t["exit_raw"] - t["entry_stop"]) > 1e-6:
                        b_static += 1
                    elif t["reason"] == "stop_gap" and \
                            (t["exit_raw"] - t["entry_stop"]) * t["dir"] > 1e-6:
                        b_gap_bad += 1   # gap must be on the losing side
    fx["F-ARCH-B"] = {"struct_recompute_violations": struct_viol,
                      "B_nonstatic_intrabar_exits": b_static,
                      "B_stopgap_wrong_side": b_gap_bad,
                      "note": "static verified on intra-bar `stop` exits; "
                      "`stop_gap` fills at the open (invariant 3), checked "
                      "on the losing side of the static stop",
                      "match": struct_viol == 0 and b_static == 0
                      and b_gap_bad == 0}
    # F-TRAIL (one-way): C/D intra-bar stop-exits fill AT a level never below
    # the entry stop; strict per-bar monotonicity + D floor unit-tested
    # (test_tc1_arch). stop_gap fills at the open, excluded (invariant 3).
    trail_viol = 0
    gap_n = 0
    for arm in ("C", "D"):
        for t in data[arm]["tr"]:
            if t["exit_raw"] is None:
                continue
            if t["reason"] == "stop" and \
                    (t["exit_raw"] - t["entry_stop"]) * t["dir"] < -1e-6:
                trail_viol += 1
            elif t["reason"] == "stop_gap":
                gap_n += 1
    fx["F-TRAIL"] = {"loosening_violations": trail_viol,
                     "stop_gap_exits_excluded": gap_n,
                     "note": "C/D intra-bar stop-exits never below the entry "
                     "stop (one-way); strict per-bar monotonicity + D floor "
                     "unit-tested (test_tc1_arch); stop_gap fills at the "
                     "open per invariant 3", "match": trail_viol == 0}
    # F-GUARDS
    guards = {}
    gv = True
    for arm in "ABCD":
        for cell in sorted(CELLS):
            g = g8(root_of(arm), cell)
            guards[f"{arm}:{cell}"] = g
            gv &= (g["g8a"] == 0 and g["g8b_max_lev"] <= 10 + 1e-6
                   and (g["g8c_min_stop_atr"] is None
                        or g["g8c_min_stop_atr"] >= 0.5 - 1e-9)
                   and g["g8d_one_r_le0"] == 0)
    fx["F-GUARDS"] = {"all_hold": gv, "match": gv}
    # F-CFG
    cfg_ok = all(hashlib.sha256((ROOT / "configs" / f"{k}.yaml")
                                .read_bytes()).hexdigest() == v
                 for k, v in CFG_REF.items())
    fx["F-CFG"] = {"match": cfg_ok}
    # F-DET
    det_m = [f"{arm}:{c}" for arm in ("B", "C", "D")
             for c in sorted(CELLS)
             if not manifest["cells"][arm][c]["match"]]
    fx["F-DET"] = {"mismatched": det_m,
                   "manifest": manifest["determinism_all_identical"],
                   "match": not det_m and manifest["determinism_all_identical"]}

    print("== TC-1 fixtures (F-A-BYTE first) ==")
    order = ["F-A-BYTE", "F-SIG-ALL", "F-ARCH-B", "F-TRAIL", "F-GUARDS",
             "F-CFG", "F-DET"]
    for k in order:
        v = fx[k]
        ok += v["match"]
        brief = {kk: vv for kk, vv in v.items()
                 if kk not in ("match", "note")}
        print(f"{k:<10} {'MATCH' if v['match'] else '*** MISMATCH ***'} "
              f"{json.dumps(brief, default=str)[:130]}")
    if ok < 7:
        print("\n*** HALT: fixture mismatch. F-A-BYTE/F-SIG-ALL failure = "
              "config gating broken; nothing downstream. ***")
        return 1

    # ── deliverables ──
    res = {"fixtures": fx, "caveat": CAVEAT, "denominators": DENOM}
    headline = {}
    for arm in "ABCD":
        row = {"denominator": DENOM[arm], "GRID": book(data[arm]["tr"])}
        for m in ("swing", "intraday", "position"):
            row[m] = book(data[arm]["tr"], lambda t, m=m: t["mandate"] == m)
        row["fills_without_exit_row"] = sum(data[arm]["fwe"].values())
        row["halts"] = data[arm]["halts"]
        row["fill_class"] = dict(Counter(t["fill_class"]
                                         for t in data[arm]["tr"]))
        # adds funnel: BE-gate passes ~ true_add fills; add_ineligible count
        row["add_ineligible_rejects"] = None
        headline[arm] = row
    res["per_cell_arm_headlines"] = headline

    # factorial interaction (grid + per-mandate): stop effect = B−A,
    # trail effect = C−A, interaction = D−B−C+A. NOTE denominators differ
    # (B/D struct-R, A/C baseline-R) — the interaction mixes denominators;
    # reported with that caveat, per contract §7.
    fac = {}
    for scope in ("GRID", "swing", "intraday", "position"):
        def g1(arm):
            return (headline[arm][scope]["sum_1x"] if scope == "GRID"
                    else headline[arm][scope]["sum_1x"])
        A1, B1, C1, D1 = (g1("A"), g1("B"), g1("C"), g1("D"))
        fac[scope] = {"A": A1, "B": B1, "C": C1, "D": D1,
                      "stop_effect_B_minus_A": r4(B1 - A1),
                      "trail_effect_C_minus_A": r4(C1 - A1),
                      "interaction_D_B_C_A": r4(D1 - B1 - C1 + A1)}
    res["factorial"] = {"table": fac,
                        "caveat": "B/D are struct-R, A/C baseline-R; the "
                        "interaction mixes denominators — read directional, "
                        "not additive-exact (contract §7)."}

    # ── predictions ──
    P = {}
    P["P-A"] = {"prior": 90, "byte_identical": fx["F-A-BYTE"]["match"],
                "verdict": "CONFIRMED" if fx["F-A-BYTE"]["match"]
                else "FALSIFIED"}
    Bg = headline["B"]["GRID"]["sum_1x"]
    P["P-B-1"] = {"prior": 55, "B_grid_1x": Bg, "band": [100, 900],
                  "verdict": "CONFIRMED" if 100 <= Bg <= 900 else "FALSIFIED"}
    Bsw = headline["B"]["swing"]["sum_1x"]
    P["P-B-2"] = {"prior": 65, "B_swing_1x": Bsw,
                  "verdict": "CONFIRMED" if Bsw > 0 else "FALSIFIED"}
    Bin = headline["B"]["intraday"]["sum_1x"]
    P["P-B-3"] = {"prior": 70, "B_intraday_1x": Bin,
                  "verdict": "CONFIRMED" if Bin < 0 else "FALSIFIED"}
    Cg = headline["C"]["GRID"]["sum_1x"]
    P["P-C-1"] = {"prior": 55, "C_grid_1x": Cg, "band": [-1900, -1300],
                  "verdict": "CONFIRMED" if -1900 <= Cg <= -1300
                  else "FALSIFIED"}
    Cpo = headline["C"]["position"]["sum_1x"]
    P["P-C-2"] = {"prior": 60, "C_position_1x": Cpo,
                  "verdict": "CONFIRMED" if Cpo >= 250 else "FALSIFIED"}
    Dg = headline["D"]["GRID"]["sum_1x"]
    P["P-D"] = {"prior": 50, "D_grid_1x": Dg, "B_grid_1x": Bg,
                "verdict": "CONFIRMED" if Dg >= Bg else "FALSIFIED"}
    Bt = headline["B"]["GRID"]["tranches"]
    Dt = headline["D"]["GRID"]["tranches"]
    P["P-CNT"] = {"prior": 60, "B_tranches": Bt, "D_tranches": Dt,
                  "cap": r4(0.70 * A_TRANCHES), "A_tranches": A_TRANCHES,
                  "verdict": "CONFIRMED"
                  if Bt <= 0.70 * A_TRANCHES and Dt <= 0.70 * A_TRANCHES
                  else "FALSIFIED"}
    res["predictions"] = P
    print("\n== predictions (8) ==")
    for k, v in P.items():
        print(f"{k:<8} {v['verdict']}")

    blob = json.dumps(res, indent=1, sort_keys=True, default=str) + "\n"
    (ROOT / "tc1_results.json").write_text(blob, encoding="utf-8",
                                           newline="\n")
    (ROOT / "TC1_RESULTS.md").write_text(render_md(res), encoding="utf-8",
                                         newline="\n")
    print(f"\nA {headline['A']['GRID']['sum_1x']} · B {Bg} · C {Cg} · D {Dg}"
          f" | interaction(GRID) {fac['GRID']['interaction_D_B_C_A']}")
    print("OUTPUT_HASH json:", hashlib.sha256(blob.encode()).hexdigest())
    print("OUTPUT_HASH md:  ", hashlib.sha256(
        (ROOT / "TC1_RESULTS.md").read_bytes()).hexdigest())
    return 0


def render_md(res):
    L = ["# TC-1 RESULTS — Stop × Exit Architecture Factorial "
         "(engine 1.0.11)", "", f"> **{res['caveat']}**", "",
         "prediction basis: s2b D1 — registered against the 38%, not the "
         "headline.", "", "## Fixtures (F-A-BYTE first)", ""]
    for k in ("F-A-BYTE", "F-SIG-ALL", "F-ARCH-B", "F-TRAIL", "F-GUARDS",
              "F-CFG", "F-DET"):
        v = res["fixtures"][k]
        b = {kk: vv for kk, vv in v.items() if kk not in ("match", "note")}
        L.append(f"- **{k}**: MATCH — `{json.dumps(b, default=str)[:130]}`")
    L += ["", "## Per-arm headlines (GRID; denominator noted)", "",
          "| arm | denom | 0× | 1× | 2× | camps | tr | win | strip-best | "
          "cost stack | fills_no_exit |", "|---|---|---|---|---|---|---|---|"
          "---|---|---|"]
    for arm in "ABCD":
        h = res["per_cell_arm_headlines"][arm]; g = h["GRID"]
        L.append(f"| {arm} | {h['denominator']} | {g['sum_0x']} | "
                 f"{g['sum_1x']} | {g['sum_2x']} | {g['campaigns']} | "
                 f"{g['tranches']} | {g['win_rate_pct']}% | "
                 f"{g['strip_best_1x']} | {g['cost_stack']} | "
                 f"{h['fills_without_exit_row']} |")
    L += ["", "### Per-mandate 1× (denominators as above)", "",
          "| arm | swing | intraday | position |", "|---|---|---|---|"]
    for arm in "ABCD":
        h = res["per_cell_arm_headlines"][arm]
        L.append(f"| {arm} | {h['swing']['sum_1x']} | "
                 f"{h['intraday']['sum_1x']} | {h['position']['sum_1x']} |")
    L += ["", "## Factorial main-effects + interaction", "",
          f"> {res['factorial']['caveat']}", "",
          "| scope | A | B | C | D | stop(B−A) | trail(C−A) | "
          "interaction(D−B−C+A) |", "|---|---|---|---|---|---|---|---|"]
    for scope, v in res["factorial"]["table"].items():
        L.append(f"| {scope} | {v['A']} | {v['B']} | {v['C']} | {v['D']} | "
                 f"{v['stop_effect_B_minus_A']} | "
                 f"{v['trail_effect_C_minus_A']} | "
                 f"{v['interaction_D_B_C_A']} |")
    L += ["", "## Scorecard", "", "| # | verdict | measured |",
          "|---|---|---|"]
    for k, v in res["predictions"].items():
        keep = {kk: vv for kk, vv in v.items()
                if kk not in ("verdict", "prior")}
        L.append(f"| {k} | **{v['verdict']}** | "
                 f"`{json.dumps(keep, default=str)[:150]}` |")
    L += ["", "## Halt calendars + fill_class", ""]
    for arm in "ABCD":
        h = res["per_cell_arm_headlines"][arm]
        L.append(f"- **{arm}**: halts `{json.dumps(h['halts'])}` · "
                 f"fill_class `{json.dumps(h['fill_class'])}`")
    L += ["", "*scripts/tc1_fixtures.py; raw journal bytes; 1h frame "
          "reloaded per B/D cell to recompute the structural stop.*", ""]
    return "\n".join(L)


if __name__ == "__main__":
    raise SystemExit(main())
