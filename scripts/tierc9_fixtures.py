#!/usr/bin/env python
"""TIER-C9 FIXTURES.  EVERY LEG STATES INLINE WHAT WOULD MAKE IT FAIL — the
house rule since F-C4-h.  The banned failure modes remain banned:
  · SELF-COMPARISON — re-deriving a number the way the program derived it;
  · ONE EXAMPLE where cardinality was possible;
  · a TUNED MAGNITUDE BOUND standing in for an identity;
  · a check whose claim is NOT the design's claim [tc8's fourth].

Run: ~/venvs/naiad/bin/python scripts/tierc9_fixtures.py
Exit 0 = all legs pass; exit 1 = at least one failed and NOTHING DOWNSTREAM
IS TRUSTWORTHY.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc2_rules as R2                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc4_fixtures as F4                                         # noqa: E402

T: list[str] = []
RESULTS: dict[str, bool] = {}
_B: dict = {}


def rec(fid: str, ok: bool, lines: list[str]) -> bool:
    T.append(f"--- {fid} : {'PASS' if ok else 'FAIL'} ---")
    T.extend("    " + ln for ln in lines)
    RESULTS[fid] = bool(ok)
    return bool(ok)


def tbl(n: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet((root or T9.OUT) / f"{n}.parquet")


def books():
    """Corridor + the books every leg reads, ridden once."""
    if _B:
        return _B
    lo, hi, meta = T9.corridor()
    card = T8.Card(name="v6-control")
    _B.update(lo=lo, hi=hi, meta=meta, card=card,
              control=T9.run_cell9(card, T9.V6_ROLES, lo, hi))
    return _B


# ═══════════════════════════════════════════════ F-CTRL · exact zero
def f_ctrl():
    """FAILS IF: the de-aliased role pipeline at v6 periods differs from
    TIER-C6's card v6 by ANY amount on ANY of 12 numeric columns, any
    exit_reason, or the campaign count.  The bar is EXACTLY zero because the
    role arrays are the same `ind.ema` on the same closes and every other
    line of the ride is the parent's — any epsilon would mean the de-aliasing
    CHANGED v6, and every 'vs v6' row downstream would compare against a
    counterfeit."""
    B = books()
    got = T9.journal_frame(B["control"]).sort_values(
        ["asset", "entry_ms"]).reset_index(drop=True)
    want = T9.journal_frame(T6.run_cell(V6.CARD_V6, B["lo"], B["hi"])
                            ).sort_values(["asset", "entry_ms"]
                                          ).reset_index(drop=True)
    lines = [f"campaigns: got {len(got)}  want {len(want)}"]
    ok = len(got) == len(want)
    cols = ["entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px",
            "r_dist", "net_r", "gross_r", "fee_r", "funding_r", "mfe_r",
            "n_advances"]
    worst = 0.0
    if ok:
        for c in cols:
            dmax = float(np.max(np.abs(got[c].to_numpy(dtype=float)
                                       - want[c].to_numpy(dtype=float))))
            worst = max(worst, dmax)
        g = ok = worst == 0.0
        lines.append(f"[{'OK ' if g else 'BAD'}] WORST ABS DIFF = "
                     f"{worst:.3e} (bar EXACTLY 0.000e+00, as commissioned)")
        g2 = list(got["exit_reason"]) == list(want["exit_reason"])
        lines.append(f"[{'OK ' if g2 else 'BAD'}] exit_reason sequences "
                     f"identical")
        ok = ok and g2
    # THE CROSS-PROCESS ANCHOR [review L4].  Both sides above ride ONE
    # process on the shared tierc5._FRAMES memo — a poisoned kline load,
    # pivot builder or funding dict hits both identically and the zero-diff
    # bar stays green (demonstrated: a reviewer scaled BTC bars 5000-9000 by
    # 1.005 pre-frame and every leg passed).  So the live book is ALSO
    # pinned to TIER-C6's FILED journal — a parquet written by another
    # process, in another session, before this module existed — exact on
    # the price columns a multiplicative poison cannot leave invariant.
    fj = pd.read_parquet(ROOT / "research_outputs" / "tierc6" /
                         "trade_journal.parquet")[
        ["asset", "entry_ms", "entry_px", "stop_px", "r_dist"]]
    mg = got[["asset", "entry_ms", "entry_px", "stop_px", "r_dist"]].merge(
        fj, on=["asset", "entry_ms"], suffixes=("", "_filed"))
    g3 = len(mg) == len(got)
    lines.append(f"[{'OK ' if g3 else 'BAD'}] cross-process anchor: "
                 f"{len(mg)} of {len(got)} live campaigns matched in the "
                 f"FILED tierc6 journal on (asset, entry_ms)")
    ok = ok and g3
    worst_px = max(float(np.max(np.abs(mg[c] - mg[c + "_filed"])))
                   for c in ("entry_px", "stop_px", "r_dist")) if len(mg)         else float("inf")
    g4 = worst_px == 0.0
    lines.append(f"[{'OK ' if g4 else 'BAD'}] entry_px/stop_px/r_dist "
                 f"EXACT against the filed artifact (worst "
                 f"{worst_px:.3e}) — a poisoned shared load cannot pass "
                 f"this and the in-process zero-diff together")
    ok = ok and g4
    lines.append("      FAILS IF: any diff on any column is nonzero, any "
                 "exit reason differs, the counts differ, or the live "
                 "prices drift from the cross-process filed journal.")
    return rec("F-CTRL", ok, lines)


# ═══════════════ F-C9-SWAP · the swapped EMA provably drives the decision
def _ema_raw(closes: np.ndarray, n: int) -> np.ndarray:
    """An EMA that SHARES NOTHING with engine.indicators — the raw_conf
    pattern [F-C8-MATCH lesson: a poisoned shared builder passed five legs
    including F-CTRL].  Same contract: alpha 2/(n+1), seeded at the first
    finite value."""
    a = 2.0 / (n + 1.0)
    out = np.empty(len(closes), dtype=float)
    prev = float(closes[0])
    out[0] = prev
    for i in range(1, len(closes)):
        prev = a * float(closes[i]) + (1.0 - a) * prev
        out[i] = prev
    return out


def f_c9_swap():
    """FAILS IF: (population) zero bars where the 9/26 trigger cross and the
    12/26 cross disagree — then the swap is inert and the cell is v6 wearing
    a new name; (instance) an independently-computed 9/26 cross bar, from an
    EMA built by code sharing NOTHING with the engine, does not match the
    entry the swapped cell actually took at the earliest diverging arming;
    (SABOTAGE / converse) the UN-swapped control book PASSES the same
    9-EMA-entry check — then the check cannot tell swapped from un-swapped
    and certifies nothing."""
    B = books()
    roles9 = next(r for r in T9.SWEEP_CELLS if r.name == "trigger-9/26")
    cell = T9.run_cell9(B["card"], roles9, B["lo"], B["hi"])
    base = B["control"]
    lines = []
    # population: the two trigger-cross populations disagree somewhere
    sym = "BTCUSDT"
    f = T9.frame(sym)["f"]
    ra9 = T9.role_arrays(sym, roles9)
    rav = T9.role_arrays(sym, T9.V6_ROLES)
    disagree = int(np.sum(ra9["t_up"] != rav["t_up"])
                   + np.sum(ra9["t_dn"] != rav["t_dn"]))
    g = disagree > 0
    lines.append(f"[{'OK ' if g else 'BAD'}] {sym}: 9/26 and 12/26 trigger "
                 f"crosses disagree on {disagree} bars (must be > 0)")
    ok = g
    # instance: earliest campaign entered by the cell and not by v6 —
    # hand-verify its entry bar IS an independent 9/26 cross bar inside its
    # own arming window
    bk = {(t.symbol, t.entry_ms) for t in base}
    only = sorted([t for t in cell if (t.symbol, t.entry_ms) not in bk],
                  key=lambda t: t.entry_ms)
    g = len(only) > 0
    lines.append(f"[{'OK ' if g else 'BAD'}] campaigns the swapped cell "
                 f"takes and v6 does not: {len(only)} (must be > 0)")
    ok = ok and g
    if g:
        # CARDINALITY, NOT AN EXAMPLE [review L4 — the first draft checked
        # only[0] while 118 existed]: EVERY cell-only entry must be a
        # raw-EMA 9/26 cross at/after its arming bar.
        emas = {}
        bad9 = 0
        first_bad = None
        for t in only:
            if t.symbol not in emas:
                ff = T9.frame(t.symbol)["f"]
                c_ = np.asarray(ff.c, dtype=float)
                emas[t.symbol] = (_ema_raw(c_, 9), _ema_raw(c_, 26))
            e9, e26 = emas[t.symbol]
            i = t.entry_i
            raw_cross = bool((e9[i] > e26[i]) if t.direction == 1
                             else (e9[i] < e26[i]))
            raw_prior = bool((e9[i - 1] <= e26[i - 1]) if t.direction == 1
                             else (e9[i - 1] >= e26[i - 1]))
            if not (raw_cross and raw_prior and t.arm_i <= i):
                bad9 += 1
                first_bad = first_bad or (t.symbol, T9.iso(t.entry_ms))
        g = bad9 == 0
        lines.append(f"[{'OK ' if g else 'BAD'}] ALL {len(only)} cell-only "
                     f"entries are raw-EMA 9/26 crosses at/after their "
                     f"arming bar — independent rebuild, zero shared code "
                     f"(failures: {bad9}{'' if not first_bad else ', first ' + str(first_bad)})")
        ok = ok and g
        t = only[0]
        # SABOTAGE / converse: the same hand-check must FAIL on v6's entry at
        # the nearest v6-only campaign — un-swapped code must not pass.
        only_v6 = sorted([u for u in base
                          if (u.symbol, u.entry_ms) not in
                          {(x.symbol, x.entry_ms) for x in cell}],
                         key=lambda u: u.entry_ms)
        sab = None
        for u in only_v6:
            fu = T9.frame(u.symbol)["f"]
            e9u = _ema_raw(np.asarray(fu.c, dtype=float), 9)
            e26u = _ema_raw(np.asarray(fu.c, dtype=float), 26)
            iu = u.entry_i
            c_ = bool((e9u[iu] > e26u[iu]) if u.direction == 1
                      else (e9u[iu] < e26u[iu]))
            p_ = bool((e9u[iu - 1] <= e26u[iu - 1]) if u.direction == 1
                      else (e9u[iu - 1] >= e26u[iu - 1]))
            if not (c_ and p_):
                sab = (u, c_, p_)
                break
        g = sab is not None
        if g:
            u, c_, p_ = sab
            lines.append(f"[OK ] SABOTAGE: v6-only campaign {u.symbol} "
                         f"{T9.iso(u.entry_ms)} FAILS the 9/26 hand-check "
                         f"(cross={c_}, prior-side={p_}) — un-swapped "
                         f"entries do not masquerade as swapped ones")
        else:
            lines.append("[BAD] SABOTAGE: every v6-only entry passed the "
                         "9/26 hand-check — the check cannot distinguish "
                         "swapped from un-swapped and certifies nothing")
        ok = ok and g
    lines.append("      FAILS IF: zero disagreeing bars, zero cell-only "
                 "campaigns, ANY of them fails the raw-EMA rebuild, or the "
                 "sabotage converse passes on un-swapped code.")
    return rec("F-C9-SWAP", ok, lines)


# ═══════════ F-C9-TOP10 · one life-cycle row reconciled against raw bars
def f_c9_top10():
    """FAILS IF: the top-1 autopsy row's fields do not reconcile end-to-end
    against the raw kline parquet and the funding stamps — entry price is
    not the trigger bar's close; MAE/MFE tape twins differ from raw bar
    extremes rebuilt HERE (shared code: none — plain numpy on the parquet);
    bars_held, funding, fees or the net-R identity (net = gross − fee −
    funding) break.  One row END-TO-END, beside the cardinality legs the
    other fixtures carry — the one-example ban does not apply to a
    hand-walk whose claim is depth, not coverage [F-AN-1 precedent]."""
    B = books()
    a2 = tbl("a2_top10_autopsy")
    row = a2.iloc[0]
    t = next(x for x in B["control"]
             if x.symbol == row["asset"] and x.entry_ms == row["entry_ms"])
    import tierc2_baseline as TB2
    kl = pd.read_parquet(
        Path(TB2.cache_dir()) / "klines" / f"{t.symbol}_4h.parquet")
    lines = [f"top-1: {t.symbol} {T9.iso(t.entry_ms)} net_r={t.net_r:+.4f}"]
    o = kl["open_time"].to_numpy()
    i_entry = int(np.searchsorted(o, t.entry_ms))
    g = int(o[i_entry]) == int(t.entry_ms)
    lines.append(f"[{'OK ' if g else 'BAD'}] entry bar found in raw parquet "
                 f"at index {i_entry}")
    ok = g
    c_ = kl["close"].to_numpy(dtype=float)
    h_ = kl["high"].to_numpy(dtype=float)
    l_ = kl["low"].to_numpy(dtype=float)
    g = abs(float(c_[i_entry]) - float(t.entry_px)) == 0.0
    lines.append(f"[{'OK ' if g else 'BAD'}] entry price IS the trigger "
                 f"bar's close ({c_[i_entry]:.6f} vs {t.entry_px:.6f})")
    ok = ok and g
    i_exit = int(np.searchsorted(o, t.exit_ms))
    g = (i_exit - i_entry) == int(row["bars_held"])
    lines.append(f"[{'OK ' if g else 'BAD'}] bars_held from raw stamps: "
                 f"{i_exit - i_entry} vs filed {int(row['bars_held'])}")
    ok = ok and g
    d, e, R = t.direction, float(t.entry_px), float(t.r_dist)
    adv = l_[i_entry + 1:i_exit + 1] if d == 1 else h_[i_entry + 1:i_exit + 1]
    fav = h_[i_entry + 1:i_exit + 1] if d == 1 else l_[i_entry + 1:i_exit + 1]
    mae_tape = min(float(np.min((adv - e) * d)) / R, 0.0)
    mfe_tape = max(float(np.max((fav - e) * d)) / R, 0.0)
    g = abs(mae_tape - float(row["mae_tape_r"])) < 5e-7
    lines.append(f"[{'OK ' if g else 'BAD'}] MAE tape from raw bars "
                 f"{mae_tape:+.6f} vs filed {row['mae_tape_r']:+.6f}")
    ok = ok and g
    g = abs(mfe_tape - float(row["mfe_tape_r"])) < 5e-7
    lines.append(f"[{'OK ' if g else 'BAD'}] MFE tape from raw bars "
                 f"{mfe_tape:+.6f} vs filed {row['mfe_tape_r']:+.6f}")
    ok = ok and g
    # funding from raw stamps (hour-floored, same-hour summed — the load law)
    fu = pd.read_parquet(
        Path(TB2.cache_dir()) / "funding" / f"{t.symbol}.parquet")
    tcol = [c for c in fu.columns if "time" in c.lower()][0]
    rcol = [c for c in fu.columns if "rate" in c.lower()][0]
    stamps = {}
    for ts_, rr in zip(fu[tcol].to_numpy(), fu[rcol].to_numpy(dtype=float)):
        hh = (int(ts_) // 3_600_000) * 3_600_000
        stamps[hh] = stamps.get(hh, 0.0) + float(rr)
    q = float(B["card"].harvest_frac)
    hj = t.harvest_i
    usum = 0.0
    for j in range(i_entry + 1, i_exit + 1):
        rate = stamps.get(int(o[j]))
        if rate:
            qty = 1.0 if (hj is None or j <= hj) else (1.0 - q)
            usum += rate * float(c_[j - 1]) * d * qty
    fund_raw = usum / R
    filed_unc = float(t.funding_r_uncapped)
    g = abs(fund_raw - filed_unc) < 1e-9
    lines.append(f"[{'OK ' if g else 'BAD'}] funding from raw stamps "
                 f"{fund_raw:+.6f} vs journal uncapped {filed_unc:+.6f} "
                 f"(harvest split at bar {hj})")
    ok = ok and g
    ident = abs(float(row["net_r"])
                - (float(row["gross_r"]) - float(row["fee_r"])
                   - float(row["funding_r"])))
    g = ident < 2e-6
    lines.append(f"[{'OK ' if g else 'BAD'}] the FILED row's columns "
                 f"satisfy net = gross − fee − funding (residual "
                 f"{ident:.2e}) — artifact consistency, not an independent "
                 f"derivation [relabelled, review L4]")
    ok = ok and g
    # and the exit FILL sits inside its exit bar's raw range — the one
    # field of a +25R campaign nothing else touches raw [review L4]
    g = bool(l_[i_exit] - 1e-9 <= float(t.exit_px) <= h_[i_exit] + 1e-9)
    lines.append(f"[{'OK ' if g else 'BAD'}] exit fill {t.exit_px:.6f} "
                 f"lies inside the raw exit bar's range "
                 f"[{l_[i_exit]:.6f}, {h_[i_exit]:.6f}]")
    ok = ok and g
    lines.append("      FAILS IF: any reconciliation misses — entry px, "
                 "bars, tape twins, funding or the net identity.")
    return rec("F-C9-TOP10", ok, lines)


# ═══════════ F-C9-SEP · separation medians recomputed independently
def f_c9_sep():
    """FAILS IF: for three named columns (net_r, mfe_tape_r, bars_held) the
    filed separation medians differ from medians recomputed HERE from the
    filed campaign-features table (numpy, not the builder's pandas path),
    or the filed gap is not their difference, or any row lacks the
    SELECTION collar."""
    sep = tbl("a2_separation")
    feat = tbl("a2_campaign_features")
    top = feat.sort_values("net_r", ascending=False).head(10)
    rest = feat.sort_values("net_r", ascending=False).iloc[10:]
    ok = True
    lines = []
    for c in ("net_r", "mfe_tape_r", "bars_held"):
        r = sep[sep["column"] == c]
        g = len(r) == 1
        if not g:
            lines.append(f"[BAD] column {c} not on the separation table")
            ok = False
            continue
        r = r.iloc[0]
        mt = float(np.median(top[c].to_numpy(dtype=float)))
        mr = float(np.median(rest[c].to_numpy(dtype=float)))
        # THE BOUND IS DERIVED, NOT GUESSED — and its first two drafts both
        # failed on the same row.  The medians of even-sized groups are
        # midpoints of 6dp-rounded values; the builder rounds the median of
        # UNROUNDED features once, this leg medians the ROUNDED filed
        # values — double rounding differing by at most half an ULP of the
        # 6th decimal, 5e-7 EXACTLY on a tie (the filed mfe_tape_r top-10
        # midpoint is 9.4655205) — and IEEE754 renders that boundary as
        # 5.0000000000328e-07, over an inclusive 5e-7.  Bound = half-ULP
        # + representation slack: 6e-7 per median, 1.2e-6 for their
        # difference.  Exact equality (draft 1) and <=5e-7 (draft 2) are
        # both knife-edge false-FAILs, not false passes.
        g = (abs(mt - float(r["median_top10"])) <= 6e-7
             and abs(mr - float(r["median_other"])) <= 6e-7
             and abs((mt - mr) - float(r["gap"])) <= 1.2e-6)
        lines.append(f"[{'OK ' if g else 'BAD'}] {c}: top10 {mt:+.6f} / "
                     f"other {mr:+.6f} / gap {mt - mr:+.6f} vs filed "
                     f"{r['median_top10']:+.6f} / {r['median_other']:+.6f} "
                     f"/ {r['gap']:+.6f}")
        ok = ok and g
    collar = (sep["selection_not_a_result"].astype(str).str.startswith(
        "a SELECTION").all() and bool(sep["gates_nothing"].all()))
    lines.append(f"[{'OK ' if collar else 'BAD'}] SELECTION collar on all "
                 f"{len(sep)} rows (selection_not_a_result + gates_nothing)")
    ok = ok and collar
    lines.append("      FAILS IF: any median or gap fails the independent "
                 "recompute, or any row drops the collar.")
    return rec("F-C9-SEP", ok, lines)


# ═══════════ F-C9-FLOOR · warm-up floors asserted per new EMA
def f_c9_floor():
    """FAILS IF: any cell's floor is not max(316, its slowest period); any
    filed cell book contains an entry before its floor bar; or (converse)
    the 423-cells exclude ZERO base-era entries — then the floor is inert
    where it must bite and the disclosure rows are decoration."""
    B = books()
    grid = tbl("sweep_grid")
    ok = True
    lines = []
    for roles in T9.SWEEP_CELLS:
        want_floor = max(RC.WARMUP_BARS, max(roles.periods))
        g = roles.floor_bars == want_floor
        row = grid[grid["cell"] == roles.name].iloc[0]
        g2 = int(row["floor_bars"]) == want_floor
        book = T9.run_cell9(B["card"], roles, B["lo"], B["hi"])
        # APPLICATION, NOT JUST DERIVATION [review L4: with the floor law
        # deleted, a campaign ARMED at bar 368 and triggered at 503 slipped
        # into a 423-cell while every entry_i-only count stayed 0].  The
        # floor bounds the ARMING scan, so the armed index is what proves
        # it was applied.
        early = sum(1 for t in book if t.entry_i < want_floor
                    or t.arm_i < want_floor)
        g3 = early == 0
        ok = ok and g and g2 and g3
        lines.append(f"[{'OK ' if (g and g2 and g3) else 'BAD'}] "
                     f"{roles.name:<14} floor={roles.floor_bars} "
                     f"(want {want_floor}, filed {int(row['floor_bars'])}), "
                     f"armings/entries before floor: {early}")
    # CONVERSE — the floor's bite is on BARS, not entries: the earliest v6
    # entry on this panel is bar 440, so demanding excluded ENTRIES would be
    # a claim the design never made [tc8's fourth banned mode — in a first
    # draft of THIS leg].  What a 423 floor must provably do is raise lo_i:
    # 107 bars per asset leave the admissible range.
    # THE CONVERSE IS MEASURED, NOT CONSTANT [review L4: the first draft
    # compared two literals].  The floor must provably EXCLUDE armings: the
    # panel is scanned for armings in the excluded band [316, 423), which
    # a deleted floor law would have admitted (the probe found BTCUSDT
    # arm_i=368 → entry 503 riding into a 423-cell under the deleted law).
    roles423 = next(r for r in T9.SWEEP_CELLS if r.floor_bars == 423)
    in_band = 0
    for sym in RC.UNIVERSE:
        arms = T9.armings9(sym, roles423, RC.WARMUP_BARS, 423 - 1)
        in_band += len(arms)
    b423 = grid[grid["floor_bars"] == 423]
    g = len(b423) == 2 and in_band > 0
    lines.append(f"[{'OK ' if g else 'BAD'}] converse MEASURED: {in_band} "
                 f"armings sit in the excluded band [316, 423) across the "
                 f"panel — a deleted floor law would admit them; both "
                 f"423-cells filed (excluded base armings printed as data: "
                 f"{list(b423['base_armings_before_cell_floor_n'])})")
    ok = ok and g
    lines.append("      FAILS IF: a floor is mis-derived, an arming or "
                 "entry precedes it, or the excluded band holds no armings "
                 "(the converse would then measure nothing).")
    return rec("F-C9-FLOOR", ok, lines)


# ═══════════ F-C9-TWINS · the twins must be twins, not one column twice
def f_c9_twins():
    """FAILS IF: mae_held_r == mae_tape_r on EVERY campaign (the clip law
    collapsed — 'the comparison would be pointless' [tc6v law]), or any
    tape reading is SHALLOWER than its held twin (the clip can only make
    held shallower), mirrored for the favorable twins."""
    feat = tbl("a2_campaign_features")
    differ = int((feat["mae_held_r"] != feat["mae_tape_r"]).sum())
    g1 = differ > 0
    viol = int((feat["mae_tape_r"] > feat["mae_held_r"] + 1e-12).sum())
    g2 = viol == 0
    fdif = int((feat["mfe_held_r"] != feat["mfe_tape_r"]).sum())
    fvio = int((feat["mfe_tape_r"] < feat["mfe_held_r"] - 1e-12).sum())
    g3 = fvio == 0
    lines = [
        f"[{'OK ' if g1 else 'BAD'}] adverse twins differ on {differ} of "
        f"{len(feat)} campaigns (must be > 0)",
        f"[{'OK ' if g2 else 'BAD'}] tape never shallower than held "
        f"(violations: {viol})",
        f"[{'OK ' if g3 else 'BAD'}] favorable: tape never below held "
        f"(violations: {fvio}; twins differ on {fdif})",
        "      FAILS IF: the twins collapse or either ordering inverts."]
    return rec("F-C9-TWINS", g1 and g2 and g3, lines)


# ═══════════ F-GRID · the grid is whole and the registration is one
def f_grid():
    """FAILS IF: the sweep grid does not hold EXACTLY the seven commissioned
    cells; any row is promotable or drops the no-promotion text or the D15
    trio; the registered flag marks any cell but trigger-9/26; the
    registrations table scores anything but m = 1; or a scored row lacks
    its LOAO line."""
    grid = tbl("sweep_grid")
    regs = tbl("registrations")
    rt = tbl("registration_text")
    lines = []
    want = {r.name for r in T9.SWEEP_CELLS}
    g = set(grid["cell"]) == want and len(grid) == 7
    lines.append(f"[{'OK ' if g else 'BAD'}] 7 cells, exactly the "
                 f"commissioned set")
    ok = g
    g = bool((~grid["promotable"].astype(bool)).all()
             and grid["no_promotion"].astype(str).str.len().gt(0).all())
    lines.append(f"[{'OK ' if g else 'BAD'}] promotable=False + no_promotion "
                 f"text on every row")
    ok = ok and g
    for col in ("paired_delta_expectancy_r", "tail_exit_ratio",
                "max_single_trade_delta_share", "loao_line"):
        g = col in grid.columns
        lines.append(f"[{'OK ' if g else 'BAD'}] D15/LOAO column rides the "
                     f"grid: {col}")
        ok = ok and g
    flags = grid[grid["is_the_registered_cell"]]
    g = len(flags) == 1 and flags.iloc[0]["cell"] == "trigger-9/26"
    lines.append(f"[{'OK ' if g else 'BAD'}] exactly one registered cell "
                 f"and it is trigger-9/26")
    ok = ok and g
    m = int(regs["scored_in_family"].sum())
    g = m == 1 and len(rt) == 1
    lines.append(f"[{'OK ' if g else 'BAD'}] m = {m} scored, "
                 f"{len(rt)} registration text(s) — both must be 1")
    ok = ok and g
    sc = regs[regs["scored_in_family"]]
    g = bool(sc["loao_line"].astype(str).str.len().gt(0).all())
    lines.append(f"[{'OK ' if g else 'BAD'}] every scored row carries an "
                 f"LOAO line")
    ok = ok and g
    lines.append("      FAILS IF: a cell is missing or extra, promotion "
                 "leaks, the trio is absent, or m != 1.")
    return rec("F-GRID", ok, lines)


# ═══════════ F-C9-LABS · TC7-f prove-ran, per verification frame
def f_c9_labs():
    """FAILS IF [TC7-f]: the manifest's tc7f block is missing a lab; any
    lab's frames_built < frames_expected; any verification frame reports
    selfcheck_all_passed != True; or any tc7f_* / tc7g_* frame named by the
    manifest sha map is absent from disk or empty.  A MISSING FIELD IS
    ITSELF A FAIL [F-C7-LABS law: silence must not read as health]."""
    man = json.loads((T9.OUT / "build_manifest.json").read_text())
    ok = True
    lines = []
    t7 = man.get("tc7f")
    if not t7:
        return rec("F-C9-LABS", False,
                   ["[BAD] manifest carries no tc7f block"])
    for lab in ("L-RE (chain)", "L-REGIME", "S-STOPGRID/L-ANCHOR",
                "L-WEAVE"):
        e = t7.get(lab)
        if e is None:
            lines.append(f"[BAD] lab absent from manifest: {lab}")
            ok = False
            continue
        g = (e.get("frames_built") == e.get("frames_expected")
             and e.get("selfcheck_all_passed") is True)
        lines.append(f"[{'OK ' if g else 'BAD'}] {lab}: "
                     f"{e.get('frames_built')}/{e.get('frames_expected')} "
                     f"frames, selfcheck_all_passed="
                     f"{e.get('selfcheck_all_passed')}")
        ok = ok and g
    # SET-EQUALITY AGAINST THE REGISTRIES [review L4: the >= 18 bar was
    # slack and frames_built==frames_expected was written from one
    # expression].  Expected names come from the LABS' OWN registries,
    # resolved here, independently of the manifest.
    exp = ({f"tc7f_chain_{k}" for k in
            ("chain_headline", "chain_ledger", "chain_by_year",
             "chain_by_asset", "chain_by_leg1_exit", "sizing_sensitivity",
             "self_check")}
           | {f"tc7f_regime_{k}" for k in
              ("lregime_register", "lregime_vol_terciles",
               "lregime_tide_streak_bands", "lregime_cross",
               "lregime_candidates")}
           | {"tc7f_stopgrid_stopgrid_table", "tc7f_stopgrid_anchor_bakeoff",
              "tc7f_stopgrid_selfcheck", "tc7f_weave_weave_events",
              "tc7f_weave_weave_quality", "tc7f_weave_too_early_cost",
              "tc7f_weave_selftest"}
           | {"tc7g_regime_cross_trailing", "tc7g_regime_candidates_trailing",
              "tc7g_edge_evolution", "tc7g_register", "tc7g_vol_terciles",
              "tc7g_tide_streak_bands"})
    filed = {k for k in man["sha"] if k.startswith(("tc7f_", "tc7g_"))}
    missing, extra = sorted(exp - filed), sorted(filed - exp)
    g = not missing and not extra
    lines.append(f"[{'OK ' if g else 'BAD'}] sha-map tc7f/tc7g set EQUALS "
                 f"the registries' 25 names (missing: {missing or 'none'}, "
                 f"extra: {extra or 'none'})")
    ok = ok and g
    filed = sorted(filed)
    empty = [k for k in filed
             if not (T9.OUT / f"{k}.parquet").exists()
             or len(pd.read_parquet(T9.OUT / f"{k}.parquet")) == 0]
    g = not empty
    lines.append(f"[{'OK ' if g else 'BAD'}] every filed frame exists "
                 f"non-empty on disk (missing/empty: {empty or 'none'})")
    ok = ok and g
    lines.append("      FAILS IF: a lab or field is missing, a selfcheck "
                 "did not pass, or a named frame is absent/empty.")
    return rec("F-C9-LABS", ok, lines)


# ═══════════ F-C9-TC7G · the trailing edges are causal and not inert
def f_c9_tc7g():
    """FAILS IF: a trailing edge recomputed HERE from the pooled prefix at a
    mid-corridor date differs from `_trailing_edges`' answer (causality by
    independent prefix rebuild); OR the trailing cross table is IDENTICAL
    in banding to the whole-corridor original (then the re-emission changed
    nothing and the look-ahead 'fix' is decoration)."""
    B = books()
    import tierc7_lab_regime as LR
    pool = T9._trailing_pool(B["lo"], B["hi"])
    at = T9._ms("2022-01-01")
    ed = T9._trailing_edges(pool, at)
    m = pool["rl_t"] <= at
    want = list(np.quantile(pool["rl_v"][m], LR.VOL_TERCILE_QUANTILES))
    g1 = ed["vol_rel"] is not None and all(
        abs(a - b) < 1e-12 for a, b in zip(ed["vol_rel"], want))
    lines = [f"[{'OK ' if g1 else 'BAD'}] 2022-01-01 vol edges from an "
             f"independent prefix mask match _trailing_edges "
             f"({[round(x, 6) for x in (ed['vol_rel'] or [])]})"]
    fut = pool["rl_t"] > at
    g2 = bool(fut.any())
    lines.append(f"[{'OK ' if g2 else 'BAD'}] the prefix genuinely excludes "
                 f"{int(fut.sum())} future bars (causality has teeth)")
    # pool sanity [review L4]: sorted times, drawn from the frames' own
    # open_ms — a mis-built pool would pass the prefix identity trivially
    srt = bool(np.all(np.diff(pool["rl_t"]) >= 0))
    f_btc = T9.frame("BTCUSDT")["f"]
    sub = bool(np.isin(pool["rl_t"][:2000],
                       np.concatenate([T9.frame(s)["f"].open_ms
                                       for s in RC.UNIVERSE])).all())
    g2b = srt and sub
    lines.append(f"[{'OK ' if g2b else 'BAD'}] pool times sorted ({srt}) "
                 f"and drawn from frame open_ms ({sub})")
    g2 = g2 and g2b
    tr = tbl("tc7g_regime_cross_trailing")
    orig = tbl("tc7f_regime_lregime_cross")
    key = ["dimension", "band", "book"]
    mg = tr.merge(orig, on=key, suffixes=("_tr", "_wc"))
    moved = int((mg["n_tr"] != mg["n_wc"]).sum())
    g3 = moved > 0
    lines.append(f"[{'OK ' if g3 else 'BAD'}] trailing vs whole-corridor "
                 f"banding moves {moved} of {len(mg)} cells' n (must be "
                 f"> 0 — an inert re-emission is not a fix)")
    lines.append("      FAILS IF: the prefix rebuild disagrees, no future "
                 "bars were excluded, or no cell moved.")
    return rec("F-C9-TC7G", g1 and g2 and g3, lines)


# ═══════════ F-KEY · totality: keys declared, unique, as-of everywhere
def f_key():
    """FAILS IF: any filed parquet lacks a declared key in the manifest, any
    declared key has duplicate rows, or any table drops the as-of warranty
    columns [TC6V-a]."""
    man = json.loads((T9.OUT / "build_manifest.json").read_text())
    keys = man["keys"]
    ok = True
    lines = []
    stems = sorted(p.stem for p in T9.OUT.glob("*.parquet"))
    undeclared = [s for s in stems if s not in keys]
    g = not undeclared
    lines.append(f"[{'OK ' if g else 'BAD'}] TOTALITY: {len(stems)} parquets, "
                 f"undeclared: {undeclared or 'none'}")
    ok = ok and g
    dup_bad, asof_bad = [], []
    for s_ in stems:
        d = pd.read_parquet(T9.OUT / f"{s_}.parquet")
        if s_ in keys and int(d.duplicated(subset=keys[s_]).sum()):
            dup_bad.append(s_)
        if "as_of_last_closed_4h" not in d.columns:
            asof_bad.append(s_)
    g = not dup_bad
    lines.append(f"[{'OK ' if g else 'BAD'}] unique keys hold on every "
                 f"table (dupes: {dup_bad or 'none'})")
    ok = ok and g
    g = not asof_bad
    lines.append(f"[{'OK ' if g else 'BAD'}] as-of warranty columns on "
                 f"every table (missing: {asof_bad or 'none'})")
    ok = ok and g
    lines.append("      FAILS IF: a parquet has no declared key, a key "
                 "duplicates, or a table is unstamped.")
    return rec("F-KEY", ok, lines)


# ═══════════ F-DET · the build reruns to the same bytes
def f_det():
    """FAILS IF: a full re-run under --rerun yields a different table set,
    any content sha moves, or the parquet BYTES on disk differ — the sha
    legs are the build's CLAIM; the byte re-hash reaches the OUTPUT."""
    r = subprocess.run(
        [str(Path.home() / "venvs" / "naiad" / "bin" / "python"),
         str(ROOT / "scripts" / "tierc9.py"), "--rerun"],
        cwd=ROOT, capture_output=True, text=True, timeout=3600)
    lines = [f"rerun rc={r.returncode}"]
    if r.returncode != 0:
        lines.append("[BAD] --rerun exited nonzero")
        lines.append((r.stderr or r.stdout)[-400:])
        return rec("F-DET", False, lines)
    m1 = json.loads((T9.OUT / "build_manifest.json").read_text())
    m2 = json.loads((T9.OUT_RERUN / "build_manifest.json").read_text())
    g = set(m1["sha"]) == set(m2["sha"])
    lines.append(f"[{'OK ' if g else 'BAD'}] same table set "
                 f"({len(m1['sha'])} tables)")
    ok = g
    moved = [k for k in m1["sha"] if m1["sha"][k] != m2["sha"].get(k)]
    g = not moved
    lines.append(f"[{'OK ' if g else 'BAD'}] no content sha moved "
                 f"(moved: {moved or 'none'})")
    ok = ok and g
    byte_bad = []
    for k in m1["sha"]:
        h1 = hashlib.sha256((T9.OUT / f"{k}.parquet").read_bytes()).hexdigest()
        h2 = hashlib.sha256(
            (T9.OUT_RERUN / f"{k}.parquet").read_bytes()).hexdigest()
        if h1 != h2:
            byte_bad.append(k)
    g = not byte_bad
    lines.append(f"[{'OK ' if g else 'BAD'}] independent byte re-hash of "
                 f"every parquet pair (differs: {byte_bad or 'none'})")
    ok = ok and g
    lines.append("      FAILS IF: the rerun fails, a sha moves, or bytes "
                 "differ on disk.")
    return rec("F-DET", ok, lines)


# ═══════════ F-CLOSURE · decision modules import no analytics
def f_closure():
    """FAILS IF: any decision module (tierc2..7_rules, tierc9) mentions the
    analytics package outside comments/docstrings — the decision path reads
    the engine only [F-C2-6 law]."""
    mods = [ROOT / "scripts" / f"tierc{i}_rules.py" for i in range(2, 8)]
    mods.append(ROOT / "scripts" / "tierc9.py")
    ok = True
    lines = []
    for p in mods:
        code = F4.code_only(p.read_text())
        hits = [pat for pat in ("import analytics", "from analytics",
                                "analytics.") if pat in code]
        g = not hits
        lines.append(f"[{'OK ' if g else 'BAD'}] {p.name}: "
                     f"{hits or 'clean'}")
        ok = ok and g
    lines.append("      FAILS IF: any decision module touches analytics "
                 "outside comments/docstrings.")
    return rec("F-CLOSURE", ok, lines)


# ═══════════ F-WORKTREE-ATTEST · the review law, printed with the evidence
def f_worktree_attest():
    """Not a check — the attestation that travels with the fixtures [tc8
    law].  Every reviewer and verifier for this build runs with
    isolation: worktree — its own checkout, unable to write to the tree
    these fixtures certify.  Enacted 2026-08-17 after a review agent left a
    sabotage patch (`return pd.DataFrame()`) in regime_table; F-KEY's
    totality leg caught it, but a review that can edit what it reviews can
    invalidate its own result."""
    return rec("F-WORKTREE-ATTEST", True, [
        "review law: reviewers run in READ-ONLY WORKTREES "
        "(isolation: worktree), never on the certified tree",
        "lineage: enacted 2026-08-17 (TIER-C7 sabotage patch, caught by "
        "F-KEY's totality leg); carried by TIER-C8; carried here",
        "      FAILS IF: never — it is an attestation, and it rides with "
        "the transcript so the evidence and the law travel together."])


def main() -> int:
    print("=" * 78)
    print("TIER-C9 FIXTURE TRANSCRIPT")
    print("=" * 78)
    legs = (f_ctrl, f_c9_swap, f_c9_top10, f_c9_sep, f_c9_floor, f_c9_twins,
            f_grid, f_c9_labs, f_c9_tc7g, f_key, f_closure,
            f_worktree_attest, f_det)
    only = [a for a in sys.argv[1:] if a != "--only"]
    for leg in legs:
        fid = leg.__doc__ and leg.__name__
        if only and not any(
                o.lower().replace("-", "_") in leg.__name__ for o in only):
            continue
        leg()
    print("\n".join(T))
    n = sum(RESULTS.values())
    print(f"\nFIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  "
          f"{json.dumps(RESULTS)}")
    # THE TRANSCRIPT IS FILED, NOT JUST PRINTED [review L6] — as-of stamped
    # so the evidence carries its corridor like every other artifact.
    try:
        meta = books()["meta"]
        (T9.OUT / "FIXTURES.txt").write_text(
            f"as_of_last_closed_4h: {meta['last_closed_4h_close']}\n"
            f"FIXTURE SUMMARY  {n}/{len(RESULTS)} PASS  "
            f"{json.dumps(RESULTS)}\n\n" + "\n".join(T) + "\n")
    except Exception as e:                                  # noqa: BLE001
        print(f"(transcript filing failed, non-fatal: {e})")
    if n != len(RESULTS):
        print("*** HALT: fixture mismatch. Nothing downstream is "
              "trustworthy. ***")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
