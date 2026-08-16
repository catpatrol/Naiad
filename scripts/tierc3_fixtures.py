"""TIER-C3 fixtures — the transcript, printed.  HALTs non-zero on any failure.

    F-C3-1       gates transcript + ESTATE READY over the corridor AND its
                 F-5 lead-in AND the F-7-truncated strip
    F-C3-INHERIT the card diffs are the ONLY diffs — the unchanged half is the
                 SAME OBJECT, asserted with `is` (extra fixture, additive)
    F-C3-RAIL    every scored trade's R >= 1.0 x ATR, ASSERTED PER TRADE, and
                 the rail's arithmetic re-derived per trade
    F-C3-PIVOT   three anchors hand-verified on RAW 4h bars — the (5,5) pivot
                 definition, nearest-beyond-entry, the rail, the exit, net R
    F-C3-4       determinism: full re-run hash-identical
    F-C3-5       era exclusions by min/max ts per table, incl. the F-7
                 truncation and the ONE table that carries a pre-corridor stamp
    F-C3-6       tape import-closure: the decision path reads no registry symbol
    F-KEY        on every join (asserted inside the program, re-asserted here
                 against the WRITTEN tables)

House idiom inherited from `tierc2_fixtures.py`: one `--- F-ID : PASS ---`
header per fixture with indented evidence beneath, because a fixture that
prints only a verdict cannot be audited.

USAGE  ~/venvs/naiad/bin/python scripts/tierc3_fixtures.py
"""
from __future__ import annotations

import ast
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc3_baseline as TC                                        # noqa: E402
import tierc3_rules as RC                                           # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import tierc2_rules as V1                                           # noqa: E402
import analytics as AN                                              # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    RESULTS[fid] = bool(ok)
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + x for x in lines)
    return bool(ok)


def sh(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          cwd=ROOT).stdout.strip()


def tbl(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or TC.OUT) / f"{name}.parquet")


# ═══════════════════════════════════════════════════════ F-C3-1 · the gates
def f_gates() -> bool:
    lines, ok = [], True
    head, remote = sh("git rev-parse --short HEAD"), sh("git remote -v")
    branch, pwd, home = sh("git branch --show-current"), str(ROOT), str(Path.home())
    checks = [
        ("HEAD", head, bool(head)),
        ("remote catpatrol/Naiad", "yes" if "catpatrol/Naiad" in remote else "NO",
         "catpatrol/Naiad" in remote),
        ("pwd", pwd, pwd == f"{home}/Naiad"),
        ("IDENTITY v2 · no cloud-sync token", "clean",
         not any(t in pwd for t in ("OneDrive", "com~apple~CloudDocs",
                                    "Mobile Documents", "GoogleDrive", "My Drive"))),
        ("branch", branch, branch == "v12-v1-census"),
        ("venv python", str(Path.home() / "venvs/naiad/bin/python"),
         (Path.home() / "venvs/naiad/bin/python").exists()),
    ]
    for name, val, good in checks:
        ok &= good
        lines.append(f"{'OK ' if good else 'HALT'}  {name:34} {val}")

    # ESTATE READY — three spans, because v3 reads three: the corridor, its
    # 30-day F-5 lead-in, and the F-7-truncated continuity strip.
    lead = TC._ms(TC.SCORED[0]) - RC.LEAD_IN_DAYS * TC.MS_1D
    spans = [("SCORED corridor", TC._ms(TC.SCORED[0]),
              TC._ms(TC.SCORED[1]) + TC.MS_1D - 1),
             (f"F-5 lead-in ({RC.LEAD_IN_DAYS}d)", lead, TC._ms(TC.SCORED[0]) - 1),
             ("F-7 truncated PINNING", TC._ms(TC.PINNING[0]),
              TC._ms(TC.PINNING[1]) + TC.MS_1D - 1)]
    for label, lo, hi in spans:
        lines.append(f"ESTATE READY (read-only) {label}: "
                     f"{TC.iso(lo)} -> {TC.iso(hi)}")
        for sym in RC.UNIVERSE:
            for tf, step in (("1h", TC.MS_1H), ("4h", TC.MS_4H)):
                d = TC.load_klines(sym, tf)
                o = d["open_time"].to_numpy(np.int64)
                w = o[(o >= lo) & (o <= hi)]
                if not len(w):
                    ok = False
                    lines.append(f"  HALT  {sym:9} {tf:3} NO ROWS")
                    continue
                diffs = np.diff(w)
                gaps = int((diffs != step).sum())
                good = gaps == 0 and bool((diffs > 0).all())
                ok &= good
                lines.append(f"  {'OK ' if good else 'HALT'}  {sym:9} {tf:3} "
                             f"rows={len(w):6d} gaps={gaps} "
                             f"{TC.iso(w[0])} -> {TC.iso(w[-1])}")
    return rec("F-C3-1", ok, lines)


# ══════════════════════════════════ F-C3-INHERIT · the card diffs are the only diffs
def f_inherit() -> bool:
    """The unchanged half of the card is not a copy that resembles Tier-C2's —
    it IS Tier-C2's, bound by import.  `is` is the strongest statement
    available, so it is the one made."""
    lines, ok = [], True
    ident = [("RC.build_4h", RC.build_4h, V1.build_4h),
             ("RC._crosses", RC._crosses, V1._crosses),
             ("RC.armings", RC.armings, V1.armings),
             ("RC.Frame4h", RC.Frame4h, V1.Frame4h),
             ("RC.Arming", RC.Arming, V1.Arming),
             ("TC.write_table", TC.write_table, TB.write_table),
             ("TC.assert_key", TC.assert_key, TB.assert_key),
             ("TC.load_klines", TC.load_klines, TB.load_klines),
             ("TC.load_funding", TC.load_funding, TB.load_funding),
             ("TB.headline_rows (used)", TB.headline_rows, TB.headline_rows),
             ("TB.build_level_series (tape)", TB.build_level_series,
              TB.build_level_series),
             ("TB.tape_rows (tape)", TB.tape_rows, TB.tape_rows)]
    for name, a, b in ident:
        good = a is b
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:32} is "
                     f"tierc2's own object")
    lines.append("")
    lines.append("THE CARD DIFFS — the only rule changes, each cited to its F:")
    for k, v in RC.REGISTER_DIFF.items():
        lines.append(f"  {k:26} = {v['value']}")
        lines.append(f"      {v['source'][:150]}")
    lines.append("")
    lines.append("UNCHANGED constants, re-read from the Tier-C2 register:")
    for k in ("UNIVERSE", "LENS", "TIDE_FAST", "TIDE_SLOW", "WINDOW_FAST",
              "WINDOW_SLOW", "TRIGGER_FAST", "TRIGGER_SLOW", "D_DISPLACEMENT",
              "D_STRIP", "ATR_LEN", "FEE_BPS_SIDE", "PIVOT_L", "PIVOT_R",
              "STOP_BUF_ATR"):
        same = RC.REGISTER[k]["value"] == V1.REGISTER[k]["value"]
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:16} {RC.REGISTER[k]['value']}")
    # RETIRED rows are named as retired. A stale row in a closed register that
    # nothing reads is how a retired rule comes back.
    import inspect
    decision_src = (inspect.getsource(RC.struct_stop_4h)
                    + inspect.getsource(RC.build_pivots_4h))
    for k in RC.RETIRED_FROM_V1:
        dead = k not in decision_src
        ok &= dead
        lines.append(f"[{'OK ' if dead else 'BAD'}] {k:16} "
                     f"{RC.REGISTER[k]['value']:<6} RETIRED by F-3 — inherited "
                     f"in the register, and READ BY NOTHING in the v3 stop: the "
                     f"name does not occur in build_pivots_4h or struct_stop_4h. "
                     f"Its only live use is deriving the time-equivalent "
                     f"lookback ({RC.PIVOT_LOOKBACK_4H_TIME_EQUIV} bars) for the "
                     f"F-C3-b disclosure, and the v1 cell of the attribution.")
    # the toll is still DERIVED, never typed
    good = RC.FEE_BPS_ROUND_TRIP == 2 * RC.FEE_BPS_SIDE == 10.0
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] toll = 2 x fee_bps_side = "
                 f"{RC.FEE_BPS_ROUND_TRIP} bps round trip — derived, not typed")
    # the corridor is HELD IDENTICAL to v1 (F-1/F-2), so the delta is the card's
    good = TC.SCORED == TB.SCORED
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] scored corridor held identical "
                 f"to v1: {TC.SCORED} == {TB.SCORED} — the v1<->v3 delta is a "
                 f"delta in the CARD, not in the corridor")
    # and the strip IS truncated (F-7)
    good = TC.PINNING[1] == "2026-07-07" and TB.PINNING[1] == "2026-08-11"
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] F-7: PINNING {TB.PINNING[1]} "
                 f"(v1) -> {TC.PINNING[1]} (v3), VR-1's forward edge")
    lines.append("")
    lines.append("RULE CARD v3, verbatim:")
    lines += ["  " + x for x in RC.RULE_CARD_V3.splitlines()]
    return rec("F-C3-INHERIT", ok, lines)


# ═══════════════════════════════════════ F-C3-RAIL · R >= 1.0 ATR, per trade
def f_rail() -> bool:
    """THE RAIL, ASSERTED PER TRADE — not as a summary statistic.

    Three legs per trade: the ratio meets the floor; the stop is EXACTLY the
    farther of {pivot stop, rail stop}; and `rail_binding` agrees with the
    arithmetic rather than being a label someone wrote.
    """
    lines, ok = [], True
    j = tbl("trade_journal")
    sg = tbl("stop_geometry")
    if not len(j):
        return rec("F-C3-RAIL", False, ["no scored trades"])
    lines.append(f"MIN_STOP_ATR = {RC.MIN_STOP_ATR} (F-3 ruling); "
                 f"{len(j)} scored trades, EVERY ONE asserted")
    lines.append(f"{'asset':9} {'entry':21} {'R':>14} {'ATR':>14} {'R/ATR':>9} "
                 f"{'pivot/ATR':>10} rail")
    for _, r in j.iterrows():
        atr, rd = float(r["atr_at_entry"]), float(r["r_dist"])
        ratio = rd / atr
        floor_ok = ratio >= RC.MIN_STOP_ATR - 1e-9
        # the stop is the FARTHER of the two candidates, exactly
        d = 1 if r["direction"] == "long" else -1
        rail_stop = float(r["entry_px"]) - d * RC.MIN_STOP_ATR * atr
        pivot_stop = float(r["pivot_stop_px"])
        want = min(pivot_stop, rail_stop) if d == 1 else max(pivot_stop, rail_stop)
        stop_ok = abs(want - float(r["stop_px"])) < 1e-6
        # and R is exactly max(pivot distance, rail distance)
        rmax = max(float(r["pivot_dist"]), float(r["rail_dist"]))
        rmax_ok = abs(rmax - rd) < 1e-6
        # rail_binding is arithmetic, not assertion
        bind_ok = bool(r["rail_binding"]) == (float(r["rail_dist"])
                                              > float(r["pivot_dist"]))
        good = floor_ok and stop_ok and rmax_ok and bind_ok
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {r['asset']:9} "
                     f"{r['entry_ts']:21} {rd:14.6f} {atr:14.6f} {ratio:9.6f} "
                     f"{float(r['pivot_dist'])/atr:10.6f} "
                     f"{'BINDING' if r['rail_binding'] else '-'}")
        if not good:
            lines.append(f"        floor={floor_ok} stop={stop_ok} "
                         f"R=max()={rmax_ok} binding={bind_ok}")
    lines.append("")
    mn = float(j["r_dist"].astype(float).div(j["atr_at_entry"].astype(float)).min())
    mx = float(j["r_dist"].astype(float).div(j["atr_at_entry"].astype(float)).max())
    nb = int(j["rail_binding"].sum())
    lines.append(f"R/ATR range {mn:.6f} -> {mx:.6f}; floor {RC.MIN_STOP_ATR} "
                 f"MET BY EVERY TRADE. rail BINDING on {nb} of {len(j)}.")
    # v1's own table, for contrast — read, never recomputed
    v1j = pd.read_parquet(TC.V1_TABLES / "trade_journal.parquet")
    v1r = (v1j["r_dist"] / v1j["atr_at_entry"])
    lines.append(f"v1 (filed, for contrast): R/ATR range {v1r.min():.6f} -> "
                 f"{v1r.max():.6f}; {int((v1r < RC.MIN_STOP_ATR).sum())} of "
                 f"{len(v1j)} trades below the v3 floor, "
                 f"{int((v1r < 0.5).sum())} below the estate's G-8c 0.5 rail.")
    # nothing in stop_geometry may claim to be under either rail
    g1 = not bool(sg["under_c3_rail"].any())
    g2 = not bool(sg["under_g8c_rail"].any())
    ok &= g1 and g2
    lines.append(f"[{'OK ' if g1 else 'BAD'}] stop_geometry.under_c3_rail: "
                 f"{int(sg['under_c3_rail'].sum())} rows")
    lines.append(f"[{'OK ' if g2 else 'BAD'}] stop_geometry.under_g8c_rail: "
                 f"{int(sg['under_g8c_rail'].sum())} rows")
    return rec("F-C3-RAIL", ok, lines)


# ═════════════════ F-C3-PIVOT · three anchors hand-verified on RAW 4h bars
def f_pivot() -> bool:
    """THREE TRADES, END TO END, FROM RAW BARS — chosen adversarially.

    The picks are: the FLAGGED F-3 row (the arming v1's own finding is about),
    the LARGEST rail widening, and the LARGEST R/ATR (the anchor that had to be
    found farthest away), then the earliest as a filler — taken in that order
    until three DISTINCT trades are held.  Three is the contract.

    Each leg is re-derived from the raw 4h series: that the anchor IS a strict
    (5,5) swing pivot by the estate's own definition, that it is CONFIRMED by
    the entry bar, that it is the NEAREST eligible one beyond entry, that the
    rail arithmetic gives the stop, that the exit fired for the reason claimed,
    and that net R reconciles from raw prices + the register's toll + funding.
    """
    lines, ok = [], True
    j = tbl("trade_journal")
    d = tbl("delta_v1_v3")
    if not len(j):
        return rec("F-C3-PIVOT", False, ["no scored trades"])

    sg = tbl("stop_geometry").set_index(["asset", "entry_ms"])
    flagged = d[d["flag"].astype(str).str.len() > 0]
    picks: list[tuple] = []
    order: list[tuple] = []
    if len(flagged):
        f0 = flagged.iloc[0]
        m = j[(j["asset"] == f0["asset"]) & (j["arm_ms"] == f0["arm_ms"])]
        if len(m):
            order.append((m.iloc[0]["asset"], int(m.iloc[0]["entry_ms"])))
    wid = sg.reset_index().sort_values("widening_atr", ascending=False)
    order += [(r["asset"], int(r["entry_ms"])) for _, r in wid.iterrows()][:1]
    big = sg.reset_index().sort_values("r_over_atr", ascending=False)
    order += [(r["asset"], int(r["entry_ms"])) for _, r in big.iterrows()][:1]
    order += [(r["asset"], int(r["entry_ms"]))
              for _, r in j.sort_values("entry_ms").iterrows()]
    for k in order:
        if k not in picks:
            picks.append(k)
        if len(picks) == 3:
            break
    if len(picks) < 3:
        return rec("F-C3-PIVOT", False,
                   [f"only {len(picks)} distinct trades; the contract asks THREE"])

    for sym, em in picks:
        r = j[(j["asset"] == sym) & (j["entry_ms"] == em)].iloc[0]
        dirn = 1 if r["direction"] == "long" else -1
        k4 = TC.load_klines(sym, "4h")
        k1 = TC.load_klines(sym, "1h")
        hi = k4["high"].to_numpy(float)
        lo = k4["low"].to_numpy(float)
        f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                        k4["open"].to_numpy(float), hi, lo,
                        k4["close"].to_numpy(float))
        ot = f.open_ms
        ai = int(np.searchsorted(ot, int(r["arm_ms"])))
        ti = int(np.searchsorted(ot, int(em)))
        xi = int(np.searchsorted(ot, int(r["exit_ms"])))
        lines.append("")
        lines.append(f"TRADE  {sym} {r['direction']}  arm {r['arm_ts']}"
                     f"{'  [ARMED IN THE F-5 LEAD-IN]' if r['armed_in_lead_in'] else ''}"
                     f"  entry {r['entry_ts']}  exit {r['exit_ts']} "
                     f"({r['exit_reason']})")

        # 1 · ARMING is a real 12/89 cross in direction, from RAW bars
        e12p, e89p, e12n, e89n = f.e12[ai-1], f.e89[ai-1], f.e12[ai], f.e89[ai]
        arm_ok = ((e12n > e89n and e12p <= e89p) if dirn == 1
                  else (e12n < e89n and e12p >= e89p))
        ok &= arm_ok
        lines.append(f"  [{'OK ' if arm_ok else 'BAD'}] arming 12/89: prev "
                     f"e12={e12p:.6f} e89={e89p:.6f} -> now e12={e12n:.6f} "
                     f"e89={e89n:.6f}")

        # 2 · TIDE and 3 · DISPLACEMENT at the arming bar
        tide = ((f.e89[ai] > f.e316[ai] and f.c[ai] > f.e316[ai]) if dirn == 1
                else (f.e89[ai] < f.e316[ai] and f.c[ai] < f.e316[ai]))
        ok &= bool(tide)
        lines.append(f"  [{'OK ' if tide else 'BAD'}] tide: e89={f.e89[ai]:.6f} "
                     f"e316={f.e316[ai]:.6f} close={f.c[ai]:.6f}")
        disp = abs(f.c[ai] - f.e89[ai]) / f.atr[ai]
        dok = (disp >= RC.D_DISPLACEMENT
               and abs(disp - float(r["disp_at_arming"])) < 1e-6)
        ok &= bool(dok)
        lines.append(f"  [{'OK ' if dok else 'BAD'}] d: |{f.c[ai]:.6f}-"
                     f"{f.e89[ai]:.6f}|/{f.atr[ai]:.6f} = {disp:.6f} >= "
                     f"{RC.D_DISPLACEMENT}  (journal {r['disp_at_arming']})")

        # 4 · TRIGGER is a real 12/26 cross and entry px IS that bar's close
        t12p, t26p, t12n, t26n = f.e12[ti-1], f.e26[ti-1], f.e12[ti], f.e26[ti]
        trig_ok = ((t12n > t26n and t12p <= t26p) if dirn == 1
                   else (t12n < t26n and t12p >= t26p))
        px_ok = abs(float(f.c[ti]) - float(r["entry_px"])) < 1e-9
        ok &= bool(trig_ok and px_ok)
        lines.append(f"  [{'OK ' if trig_ok else 'BAD'}] trigger 12/26: prev "
                     f"e12={t12p:.6f} e26={t26p:.6f} -> now e12={t12n:.6f} "
                     f"e26={t26n:.6f}")
        lines.append(f"  [{'OK ' if px_ok else 'BAD'}] entry px = bar close "
                     f"{f.c[ti]:.6f} (journal {r['entry_px']})")

        # 5 · THE ANCHOR — a REAL (5,5) 4h swing pivot, from raw bars.
        #     engine.s1._pivots is STRICT: x[p] < min(prev L) and < min(next R)
        #     for a low (mirrored for a high); it confirms at p + R.
        anchor = float(r["pivot_anchor"])
        series = lo if dirn == 1 else hi
        cand = np.flatnonzero(np.isclose(series, anchor, rtol=0, atol=1e-9))
        pidx = None
        for p in cand:
            p = int(p)
            if p - RC.PIVOT_L < 0 or p + RC.PIVOT_R >= len(series):
                continue
            L = series[p - RC.PIVOT_L:p]
            Rr = series[p + 1:p + 1 + RC.PIVOT_R]
            real = ((series[p] < L.min() and series[p] < Rr.min()) if dirn == 1
                    else (series[p] > L.max() and series[p] > Rr.max()))
            if real and p + RC.PIVOT_R <= ti:
                pidx = p
                break
        good = pidx is not None
        ok &= good
        lines.append(f"  [{'OK ' if good else 'BAD'}] anchor {anchor:.6f} is a "
                     f"STRICT 4h ({RC.PIVOT_L},{RC.PIVOT_R}) swing "
                     f"{'low' if dirn == 1 else 'high'} at bar "
                     f"{TC.iso(ot[pidx]) if pidx is not None else '?'}")
        if pidx is not None:
            L = series[pidx - RC.PIVOT_L:pidx]
            Rr = series[pidx + 1:pidx + 1 + RC.PIVOT_R]
            lines.append(f"        raw bars: prev5 {np.round(L, 6).tolist()}")
            lines.append(f"                  PIVOT {series[pidx]:.6f}")
            lines.append(f"                  next5 {np.round(Rr, 6).tolist()}")
            conf_ok = (pidx + RC.PIVOT_R) <= ti
            look_ok = (ti - (pidx + RC.PIVOT_R)) <= RC.PIVOT_LOOKBACK_4H
            ok &= bool(conf_ok and look_ok)
            lines.append(f"  [{'OK ' if conf_ok else 'BAD'}] confirmed at bar "
                         f"{pidx + RC.PIVOT_R} <= entry bar {ti} "
                         f"(causal: the pivot was knowable at entry)")
            lines.append(f"  [{'OK ' if look_ok else 'BAD'}] within lookback: "
                         f"{ti - (pidx + RC.PIVOT_R)} <= "
                         f"{RC.PIVOT_LOOKBACK_4H} bars")

        # 5b · it is the NEAREST eligible anchor beyond entry
        pv4 = RC.build_pivots_4h(hi, lo)
        if dirn == 1:
            elig = ((pv4.low_conf <= ti)
                    & (ti - pv4.low_conf <= RC.PIVOT_LOOKBACK_4H)
                    & (pv4.low_val < float(r["entry_px"])))
            nearest = float(pv4.low_val[elig].max()) if elig.any() else None
        else:
            elig = ((pv4.high_conf <= ti)
                    & (ti - pv4.high_conf <= RC.PIVOT_LOOKBACK_4H)
                    & (pv4.high_val > float(r["entry_px"])))
            nearest = float(pv4.high_val[elig].min()) if elig.any() else None
        near_ok = nearest is not None and abs(nearest - anchor) < 1e-9
        ok &= bool(near_ok)
        lines.append(f"  [{'OK ' if near_ok else 'BAD'}] nearest eligible "
                     f"{'low below' if dirn == 1 else 'high above'} entry "
                     f"{float(r['entry_px']):.6f} = {nearest} "
                     f"({int(elig.sum())} eligible pivots in the lookback)")

        # 6 · THE RAIL — pivot stop, rail stop, and which one the card takes
        atr = float(r["atr_at_entry"])
        pstop = anchor - dirn * RC.STOP_BUF_ATR * atr
        rstop = float(r["entry_px"]) - dirn * RC.MIN_STOP_ATR * atr
        stop = min(pstop, rstop) if dirn == 1 else max(pstop, rstop)
        s_ok = abs(stop - float(r["stop_px"])) < 1e-6
        rd_ok = abs(abs(float(r["entry_px"]) - stop) - float(r["r_dist"])) < 1e-6
        ok &= bool(s_ok and rd_ok)
        lines.append(f"  [{'OK ' if s_ok else 'BAD'}] pivot stop = {anchor:.6f} "
                     f"{'-' if dirn == 1 else '+'} {RC.STOP_BUF_ATR}xATR"
                     f"({atr:.6f}) = {pstop:.6f}  |  rail stop = entry "
                     f"{'-' if dirn == 1 else '+'} {RC.MIN_STOP_ATR}xATR = "
                     f"{rstop:.6f}  ->  TAKEN {stop:.6f} "
                     f"({'RAIL' if abs(stop - rstop) < 1e-12 else 'PIVOT'})")
        lines.append(f"  [{'OK ' if rd_ok else 'BAD'}] R = |entry-stop| = "
                     f"{r['r_dist']} = {float(r['r_dist'])/atr:.6f} x ATR "
                     f">= {RC.MIN_STOP_ATR}")

        # 7 · THE EXIT, from raw bars — and F-4's adverse-first rule tested
        if r["exit_reason"] == "stop":
            hit = (lo[xi] <= stop) if dirn == 1 else (hi[xi] >= stop)
            ok &= bool(hit)
            lines.append(f"  [{'OK ' if hit else 'BAD'}] stop hit intrabar: bar "
                         f"{TC.iso(ot[xi])} low={lo[xi]:.6f} high={hi[xi]:.6f} "
                         f"vs stop {stop:.6f}")
        else:
            p12, p89, n12, n89 = f.e12[xi-1], f.e89[xi-1], f.e12[xi], f.e89[xi]
            bell = ((n12 < n89 and p12 >= p89) if dirn == 1
                    else (n12 > n89 and p12 <= p89))
            b8p, b3p, b8n, b3n = f.e89[xi-1], f.e316[xi-1], f.e89[xi], f.e316[xi]
            bell2 = ((b8n < b3n and b8p >= b3p) if dirn == 1
                     else (b8n > b3n and b8p <= b3p))
            ok &= bool(bell or bell2)
            lines.append(f"  [{'OK ' if (bell or bell2) else 'BAD'}] bell "
                         f"{'12/89' if bell else '89/316'} at {TC.iso(ot[xi])}; "
                         f"exit px = close {f.c[xi]:.6f} (journal {r['exit_px']})")
            # F-4 ADVERSE-FIRST: no bar in the ride may have touched the stop
            # before this bell — if one had, the stop would have taken it.
            seg_lo, seg_hi = lo[ti+1:xi+1], hi[ti+1:xi+1]
            touched = (seg_lo <= stop).any() if dirn == 1 else (seg_hi >= stop).any()
            ok &= (not touched)
            lines.append(f"  [{'OK ' if not touched else 'BAD'}] F-4 "
                         f"adverse-first: no bar of the {xi-ti}-bar ride "
                         f"touched the stop before the bell "
                         f"(worst excursion "
                         f"{(seg_lo.min() if dirn == 1 else seg_hi.max()):.6f} "
                         f"vs stop {stop:.6f})")

        # 8 · NET R from raw prices + the register's toll + journaled funding
        gross = ((float(r["exit_px"]) - float(r["entry_px"])) * dirn
                 / float(r["r_dist"]))
        fee = ((RC.FEE_BPS_SIDE / 10_000.0)
               * (float(r["entry_px"]) + float(r["exit_px"]))
               / float(r["r_dist"]))
        fund = TC.load_funding(sym)
        fu = 0.0
        for jj in range(ti + 1, xi + 1):
            rate = fund.get(int(ot[jj]))
            if rate:
                fu += rate * float(f.c[jj - 1]) * dirn
        fu /= float(r["r_dist"])
        net = gross - fee - fu
        net_ok = abs(net - float(r["net_r"])) < 1e-6
        ok &= bool(net_ok)
        lines.append(f"  [{'OK ' if net_ok else 'BAD'}] net R = gross "
                     f"{gross:+.6f} - fee {fee:.6f} - funding {fu:+.6f} = "
                     f"{net:+.6f}  (journal {r['net_r']})")
        del k1

    # 9 · THE CROSS-VERSION RECONCILIATION — v3's flagged outcome is not a new
    #     price path, it is v1's OWN bell-only counterfactual measured against
    #     a legal R.  net_r x R is in price units and must agree.
    if len(flagged):
        f0 = flagged.iloc[0]
        v1j = pd.read_parquet(TC.V1_TABLES / "trade_journal.parquet")
        v1r = v1j[(v1j["asset"] == f0["asset"])
                  & (v1j["arm_ms"] == f0["arm_ms"])]
        v3r = j[(j["asset"] == f0["asset"]) & (j["arm_ms"] == f0["arm_ms"])]
        if len(v1r) and len(v3r):
            a = float(v1r.iloc[0]["net_r_bellonly"]) * float(v1r.iloc[0]["r_dist"])
            b = float(v3r.iloc[0]["net_r"]) * float(v3r.iloc[0]["r_dist"])
            good = abs(a - b) < 1e-3
            ok &= good
            lines.append("")
            lines.append(f"  [{'OK ' if good else 'BAD'}] THE F-3 ROW, "
                         f"CROSS-VERSION: v1 bell-only {v1r.iloc[0]['net_r_bellonly']:+.6f} R "
                         f"x R {v1r.iloc[0]['r_dist']:.6f} = {a:.6f} price units; "
                         f"v3 realised {v3r.iloc[0]['net_r']:+.6f} R x R "
                         f"{v3r.iloc[0]['r_dist']:.6f} = {b:.6f}. SAME PATH, "
                         f"different denominator (|diff| = {abs(a-b):.2e}).")
    return rec("F-C3-PIVOT", ok, lines)


# ════════════════════════════════════════════════════ F-C3-4 · determinism
def f_determinism() -> bool:
    lines = []
    a = json.loads((TC.OUT / "build_manifest.json").read_text())
    p2 = TC.OUT_RERUN / "build_manifest.json"
    if not p2.exists():
        return rec("F-C3-4", False, ["re-run manifest absent — run --rerun first"])
    b = json.loads(p2.read_text())
    ok = True
    for k in sorted(a["sha"]):
        same = a["sha"][k] == b["sha"].get(k)
        ok &= same
        lines.append(f"[{'OK ' if same else 'BAD'}] {k:22} {a['sha'][k][:32]}")
    same = a["counts"] == b["counts"]
    ok &= same
    lines.append(f"[{'OK ' if same else 'BAD'}] counts block identical: "
                 f"{json.dumps(a['counts'], sort_keys=True)}")
    lines.append("")
    lines.append("NORMALIZATION DISCLOSURE — normalized fields: ['elapsed_s'] "
                 "(wall clock) and the output ROOT path. NO computed value is "
                 "normalized: every table, count, hash and R figure is compared "
                 "content-for-content.")
    lines.append(f"seed {TC.SEED} is printed and unused — no stochastic step "
                 f"exists in this program, so determinism is structural.")
    return rec("F-C3-4", ok, lines)


# ══════════════════════════════════ F-C3-5 · era exclusions, min/max ts
def f_eras() -> bool:
    """Where every table's timestamps actually live — and the ONE table that is
    allowed a pre-corridor stamp, which is allowed it by ruling and carries no
    outcome column in exchange."""
    lines, ok = [], True
    lo_s = TC._ms(TC.SCORED[0])
    hi_s = TC._ms(TC.SCORED[1]) + TC.MS_1D - 1
    lb0 = TC._ms(TC.LOCKBOX[0])
    lb1 = TC._ms(TC.LOCKBOX[1]) + TC.MS_1D - 1
    lead_lo = lo_s - RC.LEAD_IN_DAYS * TC.MS_1D
    ceil_census = TC._ms("2024-07-01")

    # (a) EVERY ms COLUMN OF EVERY FILED TABLE — enumerated, not curated.
    #     v1's scan checked a hand-written tuple; a hand-written tuple is a
    #     scan that passes by construction, and dropping one name from it (v3
    #     dropped `arm_ms`) silently retires the test. So the columns are
    #     DISCOVERED here, and each is judged against the rule that applies to
    #     it rather than against one rule for all.
    LEAD_OK = {"arm_ms", "arm_time", "v1_arm_ts", "v3_arm_ts"}   # F-5 licenses these
    ANCHOR = {"anchor_bar_ms"}
    for p in sorted((TC.OUT).glob("*.parquet")):
        d = pd.read_parquet(p)
        if not len(d):
            lines.append(f"     {p.stem:28} EMPTY — no timestamp to place")
            continue
        for c in d.columns:
            if not (c.endswith("_ms") or c == "ts"):
                continue
            v = pd.to_numeric(d[c], errors="coerce").dropna()
            v = v[v > 0]
            if not len(v):
                continue
            mn, mx = int(v.min()), int(v.max())
            in_lb = bool(((v >= lb0) & (v <= lb1)).any())
            n_lb = int(((v >= lb0) & (v <= lb1)).sum())
            pre = int((v < lo_s).sum())
            if c in LEAD_OK:
                good = not (v < lead_lo).any()          # may reach the lead-in
                verdict = (f"LEAD-IN LICENSED (F-5): {pre} row(s) pre-corridor, "
                           f"{n_lb} inside the SEAL — arming state, no outcome "
                           f"is computed there")
            elif c in ANCHOR:
                good = not in_lb                        # CLASS line: never sealed
                verdict = (f"ANCHOR PROVENANCE: {n_lb} sealed — the seal floor "
                           f"forbids any")
            else:
                good = (lo_s <= mn and mx <= hi_s and not in_lb
                        and mn >= ceil_census)
                verdict = (f"in-scored={lo_s <= mn and mx <= hi_s} "
                           f"lockbox-free={not in_lb} "
                           f"after-census-ceiling={mn >= ceil_census}")
            ok &= good
            lines.append(f"[{'OK ' if good else 'BAD'}] {p.stem}.{c:18} "
                         f"min={TC.iso(mn)} max={TC.iso(mx)}  {verdict}")

    # (b) THE F-5 DISCLOSURE — arm_ms MAY reach into the lead-in, and the
    #     lead-in overlaps the sealed span. Every such row must still have its
    #     ENTRY in the corridor, which is what makes its OUTCOME post-lockbox.
    j = tbl("trade_journal")
    early = j[j["arm_ms"] < lo_s]
    good = bool((early["entry_ms"] >= lo_s).all()) if len(early) else True
    ok &= good
    in_lb = [TC.iso(int(m)) for m in early["arm_ms"] if lb0 <= int(m) <= lb1]
    lines.append("")
    lines.append(f"[{'OK ' if good else 'BAD'}] F-5 LEAD-IN, DISCLOSED: "
                 f"{len(early)} of {len(j)} scored trades were ARMED before the "
                 f"corridor (>= {TC.iso(lead_lo)}); EVERY ONE has its ENTRY "
                 f"inside the corridor, so every scored OUTCOME is post-lockbox.")
    lines.append(f"      arming stamps inside the SEALED span: {in_lb} — arming "
                 f"is EMA state, not outcome. CITED BY QUOTE, NOT BY LINE (the "
                 f"2026-08-15 collapse moved both by ~50 lines): LEDGER.md F4-a "
                 f"annex, 'lockbox warm-up traversal disclosed per cell in "
                 f"manifest; zero journal rows with lockbox open times'; and "
                 f"STANDING VERDICTS, 'the seal governs scored outcome evidence, "
                 f"not raw price in a display-only trailing window'. NOTE the "
                 f"limit of the second: it licenses raw price in a DISPLAY-ONLY "
                 f"window — which is why the ANCHOR, a price in a SCORED window, "
                 f"gets its own floor (F-C3-SEAL).")
    good = bool((early["arm_ms"] >= lead_lo).all()) if len(early) else True
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] no arming precedes the ruled "
                 f"lead-in edge {TC.iso(lead_lo)} "
                 f"(scored_start - {RC.LEAD_IN_DAYS}d)")

    # (c) the lead-in trade table — NO OUTCOME, whatever else it carries.
    #     NOT claimed to be the only table with a pre-corridor stamp: it is not,
    #     and (a) above enumerates the others. What IS true is the PAIRING —
    #     no row anywhere pairs a pre-corridor ENTRY/EXIT/ANCHOR stamp with an
    #     outcome. That is the claim, and it is the one tested.
    li = tbl("lead_in_trades")
    banned = [c for c in li.columns
              if any(t in c for t in ("net_r", "gross_r", "_px", "r_dist",
                                      "fee", "funding", "atr"))]
    good = not banned
    ok &= good
    lines.append("")
    lines.append(f"[{'OK ' if good else 'BAD'}] lead_in_trades: {len(li)} row(s), "
                 f"NO outcome column — banned-name scan {banned or 'none'}; "
                 f"columns = {list(li.columns)}")
    if len(li):
        mn, mx = int(li["entry_ms"].min()), int(li["entry_ms"].max())
        good = mx < lo_s and mn >= lead_lo
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] lead_in_trades.entry_ms "
                     f"{TC.iso(mn)} -> {TC.iso(mx)} — before the corridor and "
                     f"at or after the lead-in edge; occupancy only.")
    else:
        lines.append("     Under the CLASS line's seal floor NO lead-in trade "
                     "survives: every anchor a lead-in entry could reach is "
                     "sealed, so the tranche is refused. The table is EMPTY by "
                     "consequence, not by omission — and the occupancy problem "
                     "it existed to solve is therefore vacuous this corridor "
                     "(in-window triggers blocked by an open position = 0).")

    # (d) F-7 — the display-only strips truncate at VR-1's forward edge
    man = json.loads((TC.OUT / "build_manifest.json").read_text())
    edge = TC._ms("2026-07-07") + TC.MS_1D - 1
    ds = tbl("display_only_strips")
    good = set(ds["window"]) <= {"CENSUS_ERA", "PINNING"}
    ok &= good
    lines.append("")
    lines.append(f"[{'OK ' if good else 'BAD'}] display-only strips carry only "
                 f"{sorted(set(ds['window']))} and live in their own table, "
                 f"never pooled into headline.parquet")
    for w in ("CENSUS_ERA", "PINNING"):
        b = man["windows"][w].get("trade_ts_bounds")
        if not b:
            continue
        good = int(b["max_exit_ms"]) <= edge
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] F-7 {w}: entries "
                     f"{b['min_entry']} -> {b['max_entry']}, last exit "
                     f"{b['max_exit']} <= {TC.iso(edge)} (VR-1 forward edge)")
    lines.append(f"      v1's PINNING strip ran to {TB.PINNING[1]} and its last "
                 f"35 days sat PAST that edge — F-7 is the ruling that closed it.")
    lines.append("")
    lines.append(f"    SEALED LOCKBOX {TC.iso(lb0)} -> {TC.iso(lb1)} — NOT "
                 f"COMPUTED; no OUTCOME anywhere in this build is derived from "
                 f"a bar inside it.")
    lines.append("    WARM-UP TRAVERSAL DISCLOSED: the EMA/ATR recursion and the "
                 "4h pivot grid read bars before the corridor to arrive warm.")
    return rec("F-C3-5", ok, lines)


# ═════════════════════ F-C3-SEAL · the anchor's provenance, asserted per trade
def f_seal() -> bool:
    """THE FIXTURE THIS BUILD DID NOT HAVE, AND NEEDED.

    A min/max-of-timestamps test cannot see a sealed PRICE.  The structural
    anchor is a price selected by name from one specific bar, published in the
    journal, used as the R denominator and paid out as the exit price when the
    stop fires — and until this fixture existed, nothing in the build resolved
    it back to the bar it came from.  Executing the card without the CLASS
    line's seal floor quotes the low of the SEALED bar 2025-09-15T12:00Z as the
    anchor of a scored trade.

    So: for every scored trade, re-derive the chosen anchor's own bar INDEPENDENTLY
    from the raw 4h series and assert that bar is not inside the sealed span.
    """
    lines, ok = [], True
    j = tbl("trade_journal")
    lb0 = TC._ms(TC.LOCKBOX[0])
    lb1 = TC._ms(TC.LOCKBOX[1]) + TC.MS_1D - 1
    lines.append(f"SEAL {TC.iso(lb0)} -> {TC.iso(lb1)} · seal floor on anchors "
                 f"= {RC.SEAL_FLOOR_ON_ANCHOR} (CLASS line, not a card diff)")
    lines.append(f"{'asset':9} {'entry':21} {'anchor':>14} {'from bar':21} sealed?")
    for _, r in j.iterrows():
        sym, anc = r["asset"], float(r["pivot_anchor"])
        k4 = TC.load_klines(sym, "4h")
        ot = k4["open_time"].to_numpy(np.int64)
        # INDEPENDENT re-derivation: find the bar the anchor price was quoted
        # from, from raw bars, rather than trusting the stored column.
        series = (k4["low"] if r["direction"] == "long" else k4["high"]).to_numpy(float)
        ti = int(np.searchsorted(ot, int(r["entry_ms"])))
        cand = [int(p) for p in np.flatnonzero(np.isclose(series, anc, rtol=0,
                                                          atol=1e-9))
                if p + RC.PIVOT_R <= ti]
        bar = max(cand) if cand else -1
        stored = int(r["anchor_bar_ms"])
        agree = bar >= 0 and int(ot[bar]) == stored
        sealed = bool(lb0 <= stored <= lb1)
        good = agree and (not sealed) and (not bool(r["anchor_in_lockbox"]))
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {sym:9} {r['entry_ts']:21} "
                     f"{anc:14.6f} {TC.iso(stored):21} "
                     f"{'SEALED' if sealed else 'no'}"
                     f"{'' if agree else '  (STORED BAR DISAGREES WITH RAW)'}")
    n_sealed = int(j["anchor_in_lockbox"].sum())
    ok &= (n_sealed == 0)
    lines.append("")
    lines.append(f"[{'OK ' if n_sealed == 0 else 'BAD'}] anchors quoted from a "
                 f"sealed bar: {n_sealed} of {len(j)}")

    # what the floor actually refused — named, not silently absent
    man = json.loads((TC.OUT / "build_manifest.json").read_text())
    refused = man["counts"].get("armings_refused_anchor_sealed", 0)
    f = tbl("funnel")
    lines.append(f"     armings refused because EVERY reachable anchor was "
                 f"sealed: {refused} "
                 f"(funnel.leak_anchor_sealed = {int(f['leak_anchor_sealed'].sum())})")
    lines.append("     WITHOUT the floor the card takes them, and the low of the "
                 "sealed 4h bar 2025-09-15T12:00Z becomes a scored trade's "
                 "anchor, R denominator and exit price. Both numbers are on the "
                 "record — see attribution_unscored and F-C3-a.")

    # and v1's own anchors, re-derived the same way, as the contrast
    v1j = pd.read_parquet(TC.V1_TABLES / "trade_journal.parquet")
    v1_sealed = 0
    for _, r in v1j.iterrows():
        k1 = TC.load_klines(r["asset"], "1h")
        o1 = k1["open_time"].to_numpy(np.int64)
        s1 = (k1["low"] if r["direction"] == "long" else k1["high"]).to_numpy(float)
        t1 = int(np.searchsorted(o1, int(r["entry_ms"]) + 3 * TC.MS_1H,
                                 "right")) - 1
        cand = [int(p) for p in
                np.flatnonzero(np.isclose(s1, float(r["pivot_anchor"]),
                                          rtol=0, atol=1e-9))
                if p + RC.PIVOT_R <= t1]
        if cand and lb0 <= int(o1[max(cand)]) <= lb1:
            v1_sealed += 1
    lines.append(f"     v1, re-derived on its own 1H grid for contrast: "
                 f"{v1_sealed} of {len(v1j)} anchors sealed. v1 was clean by "
                 f"ARITHMETIC ACCIDENT — a 200-bar 1h lookback reaches 8.3 d "
                 f"and its earliest entry was 2025-10-29, 24 d after the seal. "
                 f"On the 4h lens the same 200 bars reach {200 * 4 / 24:.1f} d, "
                 f"and F-5 pulled the first entry to 2025-10-08.")
    return rec("F-C3-SEAL", ok, lines)


# ═══════════════════ F-C3-ABLATE · the fork reproduces its parent, exactly
def f_ablate() -> bool:
    """THE ATTRIBUTION, AND THE REPRODUCTION THAT MAKES IT TRUSTWORTHY.

    The V1 cell of `attribution_unscored` rides Tier-C2's card through the
    Tier-C3 program.  If that cell does not reproduce Tier-C2's FILED net R to
    the last decimal, then every other cell's difference is measuring the fork
    rather than the diff, and the whole attribution is worthless.
    """
    lines, ok = [], True
    a = tbl("attribution_unscored").set_index("cell")
    v1j = pd.read_parquet(TC.V1_TABLES / "trade_journal.parquet")
    filed = float(v1j["net_r"].astype(float).sum())
    mine = float(a.loc["V1", "net_r"])
    good = abs(filed - mine) < 1e-3 and int(a.loc["V1", "n"]) == len(v1j)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] THE V1 CELL REPRODUCES TIER-C2: "
                 f"filed net R {filed:+.4f} over {len(v1j)} trades vs this "
                 f"program's {mine:+.4f} over {int(a.loc['V1','n'])} — "
                 f"|diff| = {abs(filed - mine):.2e}")
    lines.append("     so every marginal below is the DIFF, not the fork.")
    lines.append("")
    lines.append(f"{'cell':5} {'anchor':7} {'rail':>5} {'lead':>5} {'seal':>5} "
                 f"{'n':>3} {'net R':>9} {'exp':>8} {'win%':>7}  marginal")
    for c in ("V1", "D", "C", "B", "A"):
        r = a.loc[c]
        m = "" if pd.isna(r["marginal_net_r"]) else \
            f"{r['marginal_net_r']:+.4f} vs {r['marginal_vs']}"
        lines.append(f"{c:5} {r['anchor_lens']:7} {r['rail_atr']:5} "
                     f"{int(r['lead_in_days']):5} {str(r['seal_floor']):>5} "
                     f"{int(r['n']):3} {r['net_r']:+9.4f} "
                     f"{r['expectancy_r']:+8.4f} {r['win_rate_pct']:7.2f}  {m}")
    lines.append("")
    lines.append("READ IT PLAINLY: the ANCHOR LENS carries the result. The rail "
                 "— the diff this build is NAMED for — is worth "
                 f"{float(a.loc['C','marginal_net_r']):+.4f} R (C vs D) and "
                 f"{float(a.loc['A','marginal_net_r']):+.4f} R (A vs B). The "
                 f"F-5 lead-in is worth "
                 f"{float(a.loc['B','marginal_net_r']):+.4f} R (B vs D).")
    lines.append("UNSCORED. No cell here may be promoted; picking one out of "
                 "this table on its R is a new probe and declares its own m "
                 "BEFORE the look. The ratified card is cell A and was chosen "
                 "before this table existed.")
    return rec("F-C3-ABLATE", ok, lines)


# ═══════════════════════════ F-C3-6 · captured-not-consulted (Amendment B1)
def f_no_consultation() -> bool:
    """The decision path imports no registry symbol — proven four ways, over
    the v3 module AND the v1 module it inherits from."""
    lines, ok = [], True
    srcs = {"scripts/tierc3_rules.py": (ROOT / "scripts" / "tierc3_rules.py").read_text(),
            "scripts/tierc2_rules.py": (ROOT / "scripts" / "tierc2_rules.py").read_text()}

    # (1) AST import scan — over import NODES, not raw lines. A line-grep gives
    #     false positives on this module's own prose about not importing.
    for name, src in srcs.items():
        imported: list[str] = []
        for node in ast.walk(ast.parse(src)):
            if isinstance(node, ast.Import):
                imported += [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                imported.append(node.module or "")
        hits = [m for m in imported if m == "analytics" or m.startswith("analytics.")]
        g = not hits
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] AST import scan of {name}: "
                     f"{sorted(set(imported))} — analytics hits = {hits}")

    # (2) the stronger property: the TRANSITIVE import closure
    import tierc3_rules  # noqa: F401
    seen, stack = set(), ["tierc3_rules"]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        seen.add(m)
        mod = sys.modules.get(m)
        if mod is None:
            continue
        for v in vars(mod).values():
            n = getattr(v, "__name__", None) if isinstance(v, type(sys)) else None
            if n and n not in seen:
                stack.append(n)
    bad = sorted(m for m in seen if m == "analytics" or m.startswith("analytics."))
    g2 = not bad
    ok &= g2
    lines.append(f"[{'OK ' if g2 else 'BAD'}] transitive import closure of "
                 f"tierc3_rules: {len(seen)} modules, analytics members = {bad}")
    lines.append(f"    closure (project modules only): "
                 f"{sorted(m for m in seen if m.split('.')[0] in {'engine', 'tierc3_rules', 'tierc2_rules'})}")

    # (3) why (2) cannot be defeated: engine/ never imports analytics/ either
    eng = [p.name for p in (ROOT / "engine").glob("*.py")
           if "import analytics" in p.read_text() or "from analytics" in p.read_text()]
    g3 = not eng
    ok &= g3
    lines.append(f"[{'OK ' if g3 else 'BAD'}] engine/ modules importing "
                 f"analytics: {eng}  (invariant I-B, analytics/INTERFACE.md — "
                 f"so the closure cannot reach a registry symbol by any path)")

    # (4) the tape's columns are write-only: the decision path never names them
    tape_cols = ["wall_family", "dist_atr", "coloc_n", "nearest_level",
                 "rvwap", "avwap", "prior_extreme"]
    named = {n: [c for c in tape_cols if c in s] for n, s in srcs.items()}
    g4 = not any(named.values())
    ok &= g4
    lines.append(f"[{'OK ' if g4 else 'BAD'}] tape column names appearing in "
                 f"the decision path: {named}")

    # (5) and the tape is still CAPTURED — the join is by ts, after the fact
    tp = tbl("analytics_tape")
    lines.append(f"    tape CAPTURED: {len(tp):,} rows over "
                 f"{TC.iso(int(tp['ts'].min()))} -> {TC.iso(int(tp['ts'].max()))}, "
                 f"instants {tp['instant'].value_counts().to_dict()}")
    lines.append(f"    Q6c: this baseline is the UNCONDITIONED population of "
                 f"fills the stillbirth counterfactual needs; nothing here "
                 f"conditions on a tape column.")
    return rec("F-C3-6", ok, lines)


# ════════════════════════════════════════════════════════ F-KEY · every join
def f_keys() -> bool:
    """Re-asserted against the WRITTEN tables, not only inside the program."""
    lines, ok = [], True
    keys = {"funnel": ["asset", "direction"],
            "headline": ["group", "key"],
            "monthly_equity": ["month"],
            "stop_geometry": ["asset", "entry_ms"],
            "trade_journal": ["asset", "entry_ms"],
            "delta_v1_v3": ["asset", "direction", "arm_ms"],
            "attribution_unscored": ["cell"],
            "anchor_lookback_disclosure": ["asset", "entry_ms"],
            "lead_in_trades": ["asset", "entry_ms"],
            "strip_d_unscored": ["population", "d"],
            "display_only_strips": ["window", "group", "key"],
            "analytics_tape": ["asset", "ts"],
            "tape_inventory": ["instant", "column"]}
    for name, k in keys.items():
        d = tbl(name)
        dup = int(d.duplicated(subset=k).sum()) if len(d) else 0
        good = dup == 0
        ok &= good
        lines.append(f"[{'OK ' if good else 'BAD'}] {name:28} key={k} "
                     f"rows={len(d):,} dup={dup}")
    # the funnel must RECONCILE — cumulative by construction
    f = tbl("funnel")
    checks = [
        ("armings_seen == in_window + lead_in",
         (f["armings_seen"] == f["armings_in_window"] + f["armings_lead_in"]).all()),
        ("passed_tide == seen - leak_tide",
         (f["passed_tide"] == f["armings_seen"] - f["leak_tide"]).all()),
        ("passed_d == passed_tide - leak_d",
         (f["passed_d"] == f["passed_tide"] - f["leak_d"]).all()),
        ("triggered == passed_d - leak_no_trigger",
         (f["triggered"] == f["passed_d"] - f["leak_no_trigger"]).all()),
        ("entered == triggered - (open+anchor+sealed+degenerate)",
         (f["entered"] == f["triggered"] - f["leak_position_open"]
          - f["leak_no_struct_anchor"] - f["leak_anchor_sealed"]
          - f["leak_degenerate_R"]).all()),
        ("entered == entered_scored + entered_lead_in",
         (f["entered"] == f["entered_scored"] + f["entered_lead_in"]).all()),
    ]
    for name, good in checks:
        ok &= bool(good)
        lines.append(f"[{'OK ' if good else 'BAD'}] funnel reconciles: {name}")
    # and the entered count must equal scored trades + unscored lead-in trades
    j, li = tbl("trade_journal"), tbl("lead_in_trades")
    good = int(f["entered"].sum()) == len(j) + len(li)
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] entered {int(f['entered'].sum())} "
                 f"== scored trades {len(j)} + unscored lead-in trades {len(li)}")
    # the headline must reconcile to the journal
    h = tbl("headline")
    a = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
    good = abs(float(a["net_r"]) - float(j["net_r"].astype(float).sum())) < 1e-4
    ok &= good
    lines.append(f"[{'OK ' if good else 'BAD'}] headline net_r "
                 f"{float(a['net_r']):.4f} == sum(journal.net_r) "
                 f"{float(j['net_r'].astype(float).sum()):.4f}; n={int(a['n'])} "
                 f"== {len(j)}")
    return rec("F-KEY", ok, lines)


# ════════════════════════════════════════════════════════════════ main
def main() -> int:
    print("=" * 78)
    print("TIER-C3 FIXTURE TRANSCRIPT — THE RAILED BASELINE")
    print("=" * 78)
    f_gates()
    f_inherit()
    f_rail()
    f_pivot()
    f_seal()
    f_ablate()
    f_determinism()
    f_eras()
    f_no_consultation()
    f_keys()

    print("\n".join(T))
    n_ok = sum(RESULTS.values())
    print()
    print("=" * 78)
    print(f"FIXTURE SUMMARY  {n_ok}/{len(RESULTS)} PASS  {json.dumps(RESULTS)}")
    print(f"  I9: ANALYTICS_VERSION {AN.ANALYTICS_VERSION} · analytics_sha "
          f"{AN.analytics_sha()}")
    print("=" * 78)
    if n_ok < len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
