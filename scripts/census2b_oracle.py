#!/usr/bin/env python3
"""CENSUS-2B ORACLE -- Mac-native rev C.  Tier-E + instrument re-pins.

RATIFIED operator 2026-08-14/15.  Drafted APOLLO, executed HEPHAESTUS.
Seed 20260814.  NO REGISTRATIONS.  F-KEY on every table.

  STAGE R   instrument-scale re-pins
            R-1  kiss-scale   per-pair delta = min(0.75, 0.6 x p95 spread ATR)
            R-2  knot-scale   KNOT = per-SR (width < 0.5 x ATR); BR = column
            R-3  state-scale  k = max(20, round(median_len/8)) per SR, _v2

  STAGE O   the complete m=0 partition, toll-honest, per lens x class,
            per direction, conditioned on VH/UH orientation.

Everything is READ from the pinned census-2B substrate and the ratified
helpers are IMPORTED, not restated: census2b_program supplies the grammar,
the crossover rule and the ribbon/state machinery; census2b_parta supplies
the R-1 ruler (r1_block / attach_r1), the duration-fixed horizon law and the
toll line.  This program adds no new constant that is not printed below.
"""
from __future__ import annotations

import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import census2b_program as P                                  # noqa: E402
import census2b_parta as A                                    # noqa: E402
from engine.indicators import crossover, crossunder           # noqa: E402

SEED = 20260814
OUT = P.OUT
ORC = OUT / "oracle"
REPORTS = ROOT / "exchange" / "reports"

LENSES = ["5m", "15m", "30m", "1h", "4h"]
PANEL = P.PANEL

# ---- the 11 pinned pairs: 6 pared-within-SR + 5 SR-median.
PAIRS_11 = [("within_sr", p) for p in A.PARED_WITHIN_SR] + \
           [("sr_median", p) for p in A.SR_MEDIAN_PAIRS]

# ---- R-1 scale law
D_CAP, D_FRAC, EPS_DIV, P95 = 0.75, 0.6, 3.0, 95.0
# ---- R-2 scale law
KNOT_C = P.RIBBON_C                      # 0.5, per-SR, unchanged by rev C
# ---- R-3 scale law
K_FLOOR, K_DIV = 20, 8

_T0 = time.time()


def hr(ch="-", n=100):
    print(ch * n)


def banner(t):
    print()
    hr("=")
    print(t)
    hr("=")


def q(x, p):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    return float(np.percentile(x, p)) if x.size else float("nan")


def med_iqr(v):
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return float("nan"), float("nan"), float("nan")
    return (float(np.median(v)), float(np.percentile(v, 25)),
            float(np.percentile(v, 75)))


def fmt(x, w=7, d=3):
    return f"{'--':>{w}s}" if not np.isfinite(x) else f"{x:>{w}.{d}f}"


def k_for(fam: str) -> int:
    """R-3: state window per SR from that family's MIDDLE (median) member."""
    return max(K_FLOOR, int(round(P.RIBBONS[fam][1] / K_DIV)))


# =====================================================================  R-1
def stage_r1(fm) -> tuple[pd.DataFrame, pd.DataFrame]:
    banner("STAGE R-1  [VETO 'kiss-scale']  per-pair delta = "
           "min(0.75, 0.6 x p95 pair-spread ATR),  eps = delta/3")
    print("The ratified grammar (approach<=eps*ATR -> veer>=delta*ATR within k=10,")
    print("no sign change) is UNTOUCHED.  Only its two SCALE arguments are re-pinned,")
    print("per pair, from that pair's own spread distribution.  k stays 10.")
    print()

    # pooled spread distribution per pair over panel x the 5 lenses
    spreads: dict[str, list[np.ndarray]] = {}
    per_cell: list[dict] = []
    for sym in PANEL:
        for tf in LENSES:
            e, _ = A.load_cell(sym, tf)
            av = e["atr"].to_numpy(np.float64)
            feas = set(P.feasible_lengths(fm, sym, tf))
            for _cls, (p_, q_) in PAIRS_11:
                tag = f"{p_}_{q_}"
                if p_ not in feas or q_ not in feas:
                    per_cell.append({"asset": sym, "tf": tf, "pair": tag,
                                     "feasible": False, "p95_spread_atr": np.nan})
                    continue
                d = e[f"e{p_}"].to_numpy(np.float64) - e[f"e{q_}"].to_numpy(np.float64)
                with np.errstate(invalid="ignore", divide="ignore"):
                    ok = np.isfinite(d) & np.isfinite(av) & (av > 0)
                    s = np.abs(d[ok]) / av[ok]
                spreads.setdefault(tag, []).append(s)
                per_cell.append({"asset": sym, "tf": tf, "pair": tag,
                                 "feasible": True, "p95_spread_atr": q(s, P95)})

    rows = []
    for cls, (p_, q_) in PAIRS_11:
        tag = f"{p_}_{q_}"
        pool = np.concatenate(spreads[tag]) if tag in spreads else np.array([])
        p95 = q(pool, P95)
        delta = min(D_CAP, D_FRAC * p95) if np.isfinite(p95) else np.nan
        rows.append({"pair_class": cls, "pair": tag, "fast_len": p_,
                     "slow_len": q_, "n_bars_pooled": int(pool.size),
                     "med_spread_atr": q(pool, 50), "p95_spread_atr": p95,
                     "delta_v2": delta, "eps_v2": delta / EPS_DIV,
                     "delta_v1": P.KISS_DELTA, "eps_v1": P.KISS_EPS,
                     "rescaled": bool(np.isfinite(delta) and delta < D_CAP - 1e-12)})
    pin = pd.DataFrame(rows)

    print(f"{'class':10s} {'pair':11s} {'bars pooled':>12s} {'med|s|/ATR':>11s} "
          f"{'p95|s|/ATR':>11s} {'delta v1':>9s} {'delta v2':>9s} "
          f"{'eps v2':>8s} {'rescaled':>9s}")
    hr()
    for r in pin.itertuples():
        print(f"{r.pair_class:10s} {r.pair:11s} {r.n_bars_pooled:>12,d} "
              f"{fmt(r.med_spread_atr, 11, 4)} {fmt(r.p95_spread_atr, 11, 4)} "
              f"{r.delta_v1:>9.3f} {fmt(r.delta_v2, 9, 4)} "
              f"{fmt(r.eps_v2, 8, 4)} {'YES' if r.rescaled else 'no':>9s}")
    hr()
    print(f"11 rows pinned.  {int(pin.rescaled.sum())} pair(s) rescale below the "
          f"0.75 cap; the rest keep the ratified 0.75/0.25.")

    # ---- which pairs were INERT under v1, and the re-run on those only
    inert = []
    for cls, (p_, q_) in PAIRS_11:
        tag = f"{p_}_{q_}"
        n = 0
        for sym in PANEL:
            for tf in LENSES:
                f = OUT / "refusals" / sym / f"{tf}.parquet"
                if f.exists():
                    d = pd.read_parquet(f, columns=["pair"])
                    n += int((d["pair"] == tag).sum())
        if n == 0:
            inert.append(tag)
    print(f"\nPREVIOUSLY INERT under v1 (0 refusals across panel x 5 lenses): "
          f"{inert if inert else 'none'}")
    print("The grammar is re-run ON THESE ONLY.  Live pairs are NOT re-run: their")
    print("v1 rows stand as filed, so nothing already published moves.\n")

    out = []
    for tag in inert:
        p_, q_ = (int(x) for x in tag.split("_"))
        d2 = float(pin.loc[pin.pair == tag, "delta_v2"].iloc[0])
        e2 = d2 / EPS_DIV
        for sym in PANEL:
            for tf in LENSES:
                e, _ = A.load_cell(sym, tf)
                feas = set(P.feasible_lengths(fm, sym, tf))
                if p_ not in feas or q_ not in feas:
                    continue
                av = e["atr"].to_numpy(np.float64)
                sp = e[f"e{p_}"].to_numpy(np.float64)
                sl = e[f"e{q_}"].to_numpy(np.float64)
                flag, _conf = P.refusal_events(sp, sl, av, eps=e2, delta=d2,
                                               k=P.KISS_K)
                spread = sp - sl
                with np.errstate(invalid="ignore", divide="ignore"):
                    ok = np.isfinite(spread) & np.isfinite(av) & (av > 0)
                    a_atr = np.where(ok, np.abs(spread) / av, np.nan)
                    touch = ok & (np.abs(spread) <= e2 * av)
                # the VEER limb, measured: best |spread|/ATR reachable within
                # k bars OF A TOUCH.  This is the quantity delta thresholds.
                ti = np.flatnonzero(touch)
                reach = np.zeros(ti.size)
                for step in range(1, P.KISS_K + 1):
                    j = np.minimum(ti + step, len(spread) - 1)
                    reach = np.maximum(reach, np.nan_to_num(a_atr[j]))
                out.append({"pair": tag, "asset": sym, "tf": tf,
                            "delta_v2": d2, "eps_v2": e2,
                            "n_touch_v2": int(ti.size),
                            "n_refusals_v2": int(flag.sum()),
                            "n_refusals_v1": 0,
                            "reach_p50": q(reach, 50), "reach_p95": q(reach, 95),
                            "reach_max": float(reach.max()) if ti.size else np.nan})
    rerun = pd.DataFrame(out)

    print(f"{'pair':11s} {'cells':>6s} {'delta v2':>9s} {'eps v2':>8s} "
          f"{'n_touch v2':>12s} {'refusals v1':>12s} {'refusals v2':>12s} "
          f"{'delta':>1s}")
    hr()
    for tag in inert:
        s = rerun[rerun.pair == tag]
        print(f"{tag:11s} {len(s):>6d} {s.delta_v2.iloc[0]:>9.4f} "
              f"{s.eps_v2.iloc[0]:>8.4f} {int(s.n_touch_v2.sum()):>12,d} "
              f"{0:>12,d} {int(s.n_refusals_v2.sum()):>12,d} "
              f"{int(s.n_refusals_v2.sum()):>+d}")
    hr()
    tot = int(rerun.n_refusals_v2.sum()) if len(rerun) else 0
    woke = rerun[rerun.n_refusals_v2 > 0].pair.nunique() if len(rerun) else 0
    print(f"RE-RUN TOTAL: {tot:,} refusals recovered; {woke} of {len(inert)} "
          f"previously-inert pair(s) now emit.")

    if tot == 0:
        print("\n*** THE RE-PIN IS INERT.  This is a FINDING, not a failure. ***")
        print("The law delta = min(0.75, 0.6 x p95) can only LOWER delta, and only")
        print("for a pair whose p95 spread is under 1.25 ATR.  Every inert pair is")
        print("inert because it is WIDE, so the cap binds and nothing moves.  The")
        print("diagnostic below shows the limb that actually fails: the approach")
        print("limb is not the problem -- touches are abundant -- the VEER limb is.")
        print()
        print("VEER-REACH DIAGNOSTIC  (MEASURED, NOT APPLIED -- no constant here is")
        print("pinned by this pass; it is what a working re-pin would have to size)")
        print(f"  {'pair':11s} {'touches':>12s} {'reach p50':>10s} "
              f"{'reach p95':>10s} {'reach max':>10s} {'delta ratified':>15s} "
              f"{'clears?':>8s}")
        hr()
        for tag in inert:
            s = rerun[rerun.pair == tag]
            if not len(s):
                continue
            r95 = float(np.nanmax(s.reach_p95)) if s.reach_p95.notna().any() else np.nan
            rmx = float(np.nanmax(s.reach_max)) if s.reach_max.notna().any() else np.nan
            r50 = float(np.nanmedian(s.reach_p50))
            print(f"  {tag:11s} {int(s.n_touch_v2.sum()):>12,d} "
                  f"{fmt(r50, 10, 4)} {fmt(r95, 10, 4)} {fmt(rmx, 10, 4)} "
                  f"{s.delta_v2.iloc[0]:>15.4f} "
                  f"{('yes' if rmx >= s.delta_v2.iloc[0] else 'NEVER'):>8s}")
        hr()
    return pin, rerun


# =====================================================================  R-2
def stage_r2(fm) -> pd.DataFrame:
    banner("STAGE R-2  [VETO 'knot-scale']  KNOT = per-SR (width < 0.5 x ATR); "
           "BR-dispersion = COLUMN ONLY")
    print("Verified against the filed substrate rather than re-derived: the pinned")
    print("<SR>_knot column already thresholds THAT family's own <SR>_width_atr at")
    print("0.5, so the per-SR reading is the filed reading.  F-R2 proves it.")
    print("The Big-Ribbon envelope becomes a REPORTED COLUMN (br_disp_atr) and is")
    print("never a knot definition.\n")

    rows, viol = [], 0
    for sym in PANEL:
        for tf in LENSES:
            e, rb = A.load_cell(sym, tf)
            av = e["atr"].to_numpy(np.float64)
            los, his = [], []
            for fam in P.FAMILIES:
                if f"{fam}_knot" not in rb.columns:
                    continue
                w = rb[f"{fam}_width_atr"].to_numpy(np.float64)
                k = rb[f"{fam}_knot"].to_numpy(np.int8)
                ok = np.isfinite(w) & (k != P.KN_NA)
                if ok.any():
                    viol += int((k[ok].astype(bool) != (w[ok] < KNOT_C)).sum())
                rows.append({"asset": sym, "tf": tf, "sr": fam,
                             "n_bars": int(ok.sum()),
                             "knot_occupancy": float(k[ok].mean()) if ok.any() else np.nan,
                             "med_width_atr": float(np.nanmedian(w[ok])) if ok.any() else np.nan})
                los.append(rb[f"{fam}_lower"].to_numpy(np.float64))
                his.append(rb[f"{fam}_upper"].to_numpy(np.float64))
            if los:
                lo = np.nanmin(np.vstack(los), axis=0)
                hi = np.nanmax(np.vstack(his), axis=0)
                with np.errstate(invalid="ignore", divide="ignore"):
                    br = np.where(np.isfinite(av) & (av > 0), (hi - lo) / av, np.nan)
                rows.append({"asset": sym, "tf": tf, "sr": "BR(column)",
                             "n_bars": int(np.isfinite(br).sum()),
                             "knot_occupancy": np.nan,
                             "med_width_atr": float(np.nanmedian(br))})
    occ = pd.DataFrame(rows)

    print(f"F-R2  <SR>_knot == (<SR>_width_atr < {KNOT_C}) element-for-element: "
          f"{viol} violation(s) -> {'PASS' if viol == 0 else 'HALT'}")
    if viol:
        raise SystemExit(2)
    print()
    piv = occ[occ.sr != "BR(column)"].pivot_table(
        index="sr", columns="tf", values="knot_occupancy", aggfunc="mean")
    piv = piv.reindex(index=[f for f in P.FAMILIES if f in piv.index],
                      columns=[t for t in LENSES if t in piv.columns])
    print("KNOT OCCUPANCY (share of warm bars with width < 0.5 ATR), panel mean")
    print(f"  {'SR':6s} " + "".join(f"{t:>9s}" for t in piv.columns))
    for sr in piv.index:
        print(f"  {sr:6s} " + "".join(fmt(piv.loc[sr, t], 9, 4) for t in piv.columns))
    br = occ[occ.sr == "BR(column)"].pivot_table(
        index="sr", columns="tf", values="med_width_atr", aggfunc="mean")
    br = br.reindex(columns=[t for t in LENSES if t in br.columns])
    print("\nBR-DISPERSION (median (max upper - min lower)/ATR over all 6 SRs) "
          "-- COLUMN ONLY, no threshold")
    print(f"  {'BR':6s} " + "".join(f"{t:>9s}" for t in br.columns))
    print(f"  {'disp':6s} " + "".join(fmt(br.iloc[0][t], 9, 3) for t in br.columns))
    return occ


# =====================================================================  R-3
def stage_r3(fm) -> pd.DataFrame:
    banner("STAGE R-3  [VETO 'state-scale']  k = max(20, round(median_len/8)) "
           "per SR;  _v2 columns BESIDE the originals")
    print(f"{'SR':6s} {'lengths (fast,median,slow)':>28s} {'median_len':>11s} "
          f"{'k_v1':>6s} {'k_v2':>6s} {'changed':>8s}")
    hr()
    kmap = {}
    for fam in P.FAMILIES:
        a, m, z = P.RIBBONS[fam]
        kmap[fam] = k_for(fam)
        print(f"{fam:6s} {str((a, m, z)):>28s} {m:>11d} {P.K_WINDOW:>6d} "
              f"{kmap[fam]:>6d} {'YES' if kmap[fam] != P.K_WINDOW else 'no':>8s}")
    hr()
    print("k is the width-delta lookback ONLY.  eps stays 0.05 ATR; the three state")
    print("codes and their meanings are unchanged.  Originals are not overwritten.\n")

    rows = []
    for sym in PANEL:
        for tf in LENSES:
            e, rb = A.load_cell(sym, tf)
            av = e["atr"].to_numpy(np.float64)
            n = len(rb)
            keep = {"open_time": e["open_time"].to_numpy(np.int64)}
            for fam in P.FAMILIES:
                col = f"{fam}_width_atr"
                if col not in rb.columns:
                    continue
                up = rb[f"{fam}_upper"].to_numpy(np.float64)
                lo = rb[f"{fam}_lower"].to_numpy(np.float64)
                raw = up - lo
                k = kmap[fam]
                prev = np.full(n, np.nan)
                if n > k:
                    prev[k:] = raw[:-k]
                warm = np.isfinite(raw) & np.isfinite(av) & (av > 0)
                with np.errstate(invalid="ignore", divide="ignore"):
                    dk = np.where(warm & np.isfinite(prev), (raw - prev) / av, np.nan)
                st = np.full(n, P.ST_NA, dtype=np.int8)
                fin = np.isfinite(dk)
                st[fin] = P.ST_FLAT
                st[fin & (dk < -P.STATE_EPS)] = P.ST_COMPRESS
                st[fin & (dk > P.STATE_EPS)] = P.ST_EXPAND
                keep[f"{fam}_width_delta_k_v2"] = dk.astype(np.float32)
                keep[f"{fam}_state_v2"] = st
                o1 = rb[f"{fam}_state"].to_numpy(np.int8)
                for label, code in (("compressing", P.ST_COMPRESS),
                                    ("flat", P.ST_FLAT), ("expanding", P.ST_EXPAND)):
                    rows.append({"asset": sym, "tf": tf, "sr": fam, "k_v2": k,
                                 "state": label,
                                 "occ_v1": float((o1 == code).mean()),
                                 "occ_v2": float((st == code).mean())})
            d = ORC / "state_v2" / sym
            d.mkdir(parents=True, exist_ok=True)
            P.to_parquet_atomic(pd.DataFrame(keep), d / f"{tf}.parquet")
    occ = pd.DataFrame(rows)

    for tf in LENSES:
        s = occ[occ.tf == tf]
        if not len(s):
            continue
        print(f"OCCUPANCY -- lens {tf}   (panel mean; v1 = k20 global, "
              f"v2 = per-SR k)")
        print(f"  {'SR':6s} {'k_v2':>5s} " +
              "".join(f"{lab:>24s}" for lab in ("compressing", "flat", "expanding")))
        for fam in P.FAMILIES:
            f = s[s.sr == fam]
            if not len(f):
                continue
            cells = []
            for lab in ("compressing", "flat", "expanding"):
                r = f[f.state == lab]
                if len(r):
                    cells.append(f"{r.occ_v1.mean():.4f} -> {r.occ_v2.mean():.4f}".rjust(24))
                else:
                    cells.append(" " * 24)
            print(f"  {fam:6s} {int(f.k_v2.iloc[0]):>5d} " + "".join(cells))
        print()
    return occ


# ===================================================================== STAGE O
CLASSES = [
    ("12_26 IN-WINDOW", "crosses"), ("12_26 bare", "crosses"),
    ("26_89", "derived"), ("12_89", "crosses"), ("89_127", "crosses"),
    ("89_316", "crosses"), ("316_423", "crosses"), ("316_889", "crosses"),
    ("889_2618", "crosses"), ("2618_4618", "crosses"),
    ("knot->fan transition", "transitions"), ("spring", "springs"),
]


def orient_cond(rb: pd.DataFrame, idx: np.ndarray, sgn: np.ndarray) -> np.ndarray:
    """VH/UH-orientation conditioning at the anchor bar.

    orient codes: 1 bull-fanned, -1 bear-fanned, 0 mixed, -9 n/a.
    with    = BOTH VH and UH fanned the way the event points
    against = BOTH fanned the opposite way
    mixed   = anything else, INCLUDING any mixed(0) or n/a(-9) limb -- a
              not-yet-warm ultra-high ribbon is not evidence of agreement.
    """
    n = len(idx)
    out = np.full(n, "mixed", dtype=object)
    vh = rb["VH_orient"].to_numpy(np.int8)[idx]
    uh = rb["UH_orient"].to_numpy(np.int8)[idx]
    s = np.sign(sgn).astype(np.int8)
    live = (vh != P.OR_NA) & (uh != P.OR_NA) & (vh != P.OR_MIXED) & \
           (uh != P.OR_MIXED) & (s != 0)
    out[live & (vh == s) & (uh == s)] = "with"
    out[live & (vh == -s) & (uh == -s)] = "against"
    return out


def _events_for_cell(sym: str, tf: str, fm, e, rb) -> pd.DataFrame:
    """Every ORACLE anchor for one cell: (class, anchor bar, direction sign)."""
    feas = set(P.feasible_lengths(fm, sym, tf))
    n = len(e)
    frames = []

    def add(cls, idx, sgn, src):
        if len(idx) == 0:
            return
        frames.append(pd.DataFrame({"cls": cls, "bar_index": np.asarray(idx, np.int64),
                                    "dir_sign": np.asarray(sgn, np.float64),
                                    "source": src}))

    # ---- native cross classes, READ from the filed crosses inventory
    cf = OUT / "crosses" / sym / f"{tf}.parquet"
    cx = pd.read_parquet(cf) if cf.exists() else pd.DataFrame()
    NATIVE = ["12_89", "89_127", "89_316", "316_423", "316_889",
              "889_2618", "2618_4618"]
    if len(cx):
        for tag in NATIVE:
            s = cx[(cx.pair == tag) & cx.event.isin(["cross_up", "cross_down"])]
            add(tag, s.bar_index.to_numpy(np.int64),
                np.where(s.event.to_numpy() == "cross_up", 1.0, -1.0), "crosses")

        # ---- 12_26 split IN-WINDOW vs bare against the filed windows table
        s = cx[(cx.pair == "12_26") & cx.event.isin(["cross_up", "cross_down"])]
        wf = OUT / "windows" / sym / f"{tf}.parquet"
        inwin = np.zeros(len(s), dtype=bool)
        if wf.exists() and len(s):
            w = pd.read_parquet(wf, columns=["arming_ts_ms", "window_close_ts_ms"])
            ts = s.ts_ms.to_numpy(np.int64)
            a = np.sort(w.arming_ts_ms.to_numpy(np.int64))
            order = np.argsort(w.arming_ts_ms.to_numpy(np.int64))
            c = w.window_close_ts_ms.to_numpy(np.int64)[order]
            cmax = np.maximum.accumulate(c)          # windows may nest/overlap
            j = np.searchsorted(a, ts, "right") - 1
            ok = j >= 0
            inwin[ok] = ts[ok] <= cmax[j[ok]]
        sg = np.where(s.event.to_numpy() == "cross_up", 1.0, -1.0)
        bi = s.bar_index.to_numpy(np.int64)
        add("12_26 IN-WINDOW", bi[inwin], sg[inwin], "crosses x windows")
        add("12_26 bare", bi[~inwin], sg[~inwin], "crosses x windows")

    # ---- 26_89: NOT in the filed crosses taxonomy (18 within-family + 5
    #      midline; 26_89 is a cross-FAMILY adjacency nobody emitted).  It is
    #      derived HERE from the pinned emas substrate with the SAME crossover
    #      rule and the SAME feasibility gate, and is flagged 'derived'.
    if 26 in feas and 89 in feas:
        a26 = e["e26"].to_numpy(np.float64)
        a89 = e["e89"].to_numpy(np.float64)
        u = np.flatnonzero(crossover(a26, a89))
        d = np.flatnonzero(crossunder(a26, a89))
        add("26_89", u, np.ones(len(u)), "derived<emas>")
        add("26_89", d, -np.ones(len(d)), "derived<emas>")

    # ---- knot -> fan transition: a knot episode whose separation is followed
    #      by a fan onset.  Anchor = the fan ONSET bar (the transition itself),
    #      direction = the fan's dir_sign.  Joined per SR, nearest fan at or
    #      after the knot exit.
    kp = OUT / "transitions" / sym / f"{tf}_knots.parquet"
    fp = OUT / "transitions" / sym / f"{tf}_fans.parquet"
    if kp.exists() and fp.exists():
        kn = pd.read_parquet(kp)
        fa = pd.read_parquet(fp)
        for sr in sorted(set(kn.sr) & set(fa.sr)):
            k = kn[kn.sr == sr].sort_values("exit_bar_index")
            f = fa[fa.sr == sr].sort_values("onset_bar_index")
            if not len(k) or not len(f):
                continue
            on = f.onset_bar_index.to_numpy(np.int64)
            ex = k.exit_bar_index.to_numpy(np.int64)
            j = np.searchsorted(on, ex, "left")
            j = j[j < len(on)]
            # one fan may only close one knot: unique() keeps each fan once
            uj = np.unique(j)
            add("knot->fan transition", on[uj],
                f.dir_sign.to_numpy(np.float64)[uj], "transitions(knots x fans)")

    # ---- spring / upthrust: anchor = reclaim bar, dir_sign as filed
    sp = OUT / "springs" / sym / f"{tf}.parquet"
    if sp.exists():
        s = pd.read_parquet(sp)
        if len(s):
            add("spring", s.reclaim_bar_index.to_numpy(np.int64),
                s.dir_sign.to_numpy(np.float64), "springs")

    if not frames:
        return pd.DataFrame(columns=["cls", "bar_index", "dir_sign", "source"])
    out = pd.concat(frames, ignore_index=True)
    return out[(out.bar_index >= 0) & (out.bar_index < n)].reset_index(drop=True)


def window_tiling() -> pd.DataFrame:
    """Why '12_26 bare' is nearly empty, measured rather than asserted.

    A window is armed by a 12_89 cross and CLOSED BY THE COUNTER 12_89 cross --
    the same cross that arms the next one.  So the windows TILE the armed span
    by construction and 'bare' can only be the pre-first-arming head.  This is
    a property of the filed windows table, not of the split.
    """
    print("WINDOW TILING  (why '12_26 bare' is a head, not a population)")
    print(f"  {'asset':9s} {'tf':4s} {'windows':>8s} {'closed_by counter':>18s} "
          f"{'union cover of armed span':>27s} {'pre-arm head bars':>18s}")
    rows = []
    for sym in PANEL:
        for tf in LENSES:
            f = OUT / "windows" / sym / f"{tf}.parquet"
            if not f.exists():
                continue
            w = pd.read_parquet(f, columns=["arming_ts_ms", "window_close_ts_ms",
                                            "closed_by"])
            if not len(w):
                continue
            o = np.argsort(w.arming_ts_ms.to_numpy(np.int64))
            a = w.arming_ts_ms.to_numpy(np.int64)[o]
            c = w.window_close_ts_ms.to_numpy(np.int64)[o]
            cov, cs, ce = 0, a[0], c[0]
            for i in range(1, len(a)):
                if a[i] <= ce:
                    ce = max(ce, c[i])
                else:
                    cov += ce - cs
                    cs, ce = a[i], c[i]
            cov += ce - cs
            span = int(c.max() - a.min())
            e, _ = A.load_cell(sym, tf)
            ot = e["open_time"].to_numpy(np.int64)
            head = int((ot < a.min()).sum())
            frac = cov / span if span else float("nan")
            rows.append({"asset": sym, "tf": tf, "n_windows": len(w),
                         "cover": frac, "head_bars": head})
            print(f"  {sym:9s} {tf:4s} {len(w):>8,d} "
                  f"{int((w.closed_by == 'counter-12_89').sum()):>18,d} "
                  f"{frac:>26.4%} {head:>18,d}")
    d = pd.DataFrame(rows)
    if len(d):
        print(f"  panel: union cover min={d.cover.min():.4%} "
              f"max={d.cover.max():.4%}.  The armed span is TILED; 'bare' is the "
              f"warm-up head only.")
    print()
    return d


def stage_o(fm) -> pd.DataFrame:
    banner("STAGE O  --  THE ORACLE TABLE   (complete partition, m=0, "
           "toll-honest)")
    A.print_horizon_realisation(LENSES)
    print()
    print("RULER  R-1: signed TERMINAL return over the duration-fixed horizon,")
    print("       ATR-normalised AT THE ANCHOR.  MFE/MAE window is [i+1, i+bars].")
    print("TOLL   10 bps round trip, in ATR units, measured on EACH CELL'S OWN")
    print("       anchor population (census2a note m8).  NET = median - toll.")
    print("ORIENT with/against/mixed on VH AND UH at the anchor bar; any mixed(0)")
    print("       or n/a(-9) limb falls to 'mixed'.")
    print()
    window_tiling()

    all_rows = []
    for sym in PANEL:
        for tf in LENSES:
            e, rb = A.load_cell(sym, tf)
            ev = _events_for_cell(sym, tf, fm, e, rb)
            if not len(ev):
                continue
            close = e["close"].to_numpy(np.float64)
            high = e["high"].to_numpy(np.float64)
            low = e["low"].to_numpy(np.float64)
            av = e["atr"].to_numpy(np.float64)
            idx = ev.bar_index.to_numpy(np.int64)
            sgn = ev.dir_sign.to_numpy(np.float64)
            blk = A.r1_block(close, high, low, av, idx, sgn, tf)
            for k, v in blk.items():
                ev[k] = v.astype(np.float32)
            ev["orient"] = orient_cond(rb, idx, sgn)
            ev["dir"] = np.where(sgn > 0, "up", "down")
            ev["asset"] = sym
            ev["tf"] = tf
            # toll per (cls) on that class's own anchors, this cell
            ev["toll_atr"] = np.nan
            for c in ev.cls.unique():
                m = ev.cls == c
                ev.loc[m, "toll_atr"] = A.toll_atr_for(close, av, idx[m.to_numpy()])
            all_rows.append(ev)

    ledger = pd.concat(all_rows, ignore_index=True) if all_rows else pd.DataFrame()
    ORC.mkdir(parents=True, exist_ok=True)
    P.to_parquet_atomic(ledger, ORC / "oracle_ledger.parquet")
    print(f"ORACLE LEDGER: {len(ledger):,} anchors  ->  "
          f"{ORC / 'oracle_ledger.parquet'}\n")
    return ledger


def oracle_grid(ledger: pd.DataFrame) -> pd.DataFrame:
    """The one grid, printed whole: lens x class x {ALL, up, down, orient}."""
    names = [c for c, _ in CLASSES]
    rows = []
    for tf in LENSES:
        L = ledger[ledger.tf == tf]
        for cls in names:
            C = L[L.cls == cls]
            toll = float(C.toll_atr.median()) if len(C) else float("nan")
            cuts = [("ALL", C)] + \
                   [(f"dir={d}", C[C["dir"] == d]) for d in ("up", "down")] + \
                   [(f"orient={o}", C[C.orient == o])
                    for o in ("with", "against", "mixed")]
            for label, S in cuts:
                r = {"tf": tf, "cls": cls, "cut": label, "n": len(S),
                     "toll_atr": toll}
                for h in ("H20", "H100"):
                    m, lo, hi = med_iqr(S.get(f"term_{h}", pd.Series(dtype=float)))
                    r[f"{h}_med"] = m
                    r[f"{h}_q25"] = lo
                    r[f"{h}_q75"] = hi
                    r[f"{h}_net"] = m - toll if np.isfinite(m) else np.nan
                    mf, _, _ = med_iqr(S.get(f"mfe_{h}", pd.Series(dtype=float)))
                    ma, _, _ = med_iqr(S.get(f"mae_{h}", pd.Series(dtype=float)))
                    r[f"{h}_mfe"] = mf
                    r[f"{h}_mae"] = ma
                rows.append(r)
    g = pd.DataFrame(rows)
    P.to_parquet_atomic(g, ORC / "oracle_grid.parquet")

    for tf in LENSES:
        banner(f"THE ORACLE GRID  --  LENS {tf}   "
               f"(median [IQR] terminal ATR-R; NET = median - toll)")
        S = g[g.tf == tf]
        toll_by = S.groupby("cls").toll_atr.first()
        print(f"{'class':22s} {'cut':16s} {'n':>8s} "
              f"{'H20 med':>9s} {'H20 IQR':>17s} {'H20 NET':>9s} "
              f"{'H100 med':>9s} {'H100 IQR':>17s} {'H100 NET':>9s} {'toll':>7s}")
        hr("-", 132)
        for cls in [c for c, _ in CLASSES]:
            C = S[S.cls == cls]
            if not len(C) or int(C[C.cut == "ALL"].n.iloc[0]) == 0:
                print(f"{cls:22s} {'--':16s} {0:>8d}   NO EVENTS AT THIS LENS")
                continue
            for r in C.itertuples():
                if r.n == 0:
                    continue
                iqr20 = f"[{fmt(r.H20_q25, 6, 3)},{fmt(r.H20_q75, 6, 3)}]"
                iqr100 = f"[{fmt(r.H100_q25, 6, 3)},{fmt(r.H100_q75, 6, 3)}]"
                print(f"{cls if r.cut == 'ALL' else '':22s} {r.cut:16s} "
                      f"{r.n:>8,d} {fmt(r.H20_med, 9)} {iqr20:>17s} "
                      f"{fmt(r.H20_net, 9)} {fmt(r.H100_med, 9)} "
                      f"{iqr100:>17s} {fmt(r.H100_net, 9)} "
                      f"{fmt(toll_by.get(cls, np.nan), 7, 4)}")
            hr("-", 132)
    return g


# ===================================================================== F-O1
def f_o1(ledger: pd.DataFrame) -> bool:
    banner("F-O1  ORACLE counts reconcile to the filed inventories")
    ok = True
    NATIVE = ["12_89", "89_127", "89_316", "316_423", "316_889",
              "889_2618", "2618_4618"]
    print(f"{'class':22s} {'oracle n':>10s} {'inventory n':>12s} {'delta':>8s}  verdict")
    hr()

    def line(cls, o, inv):
        nonlocal ok
        good = (o == inv)
        ok &= good
        print(f"{cls:22s} {o:>10,d} {inv:>12,d} {o - inv:>8,d}  "
              f"{'PASS' if good else 'FAIL'}")

    for tag in NATIVE:
        inv = 0
        for sym in PANEL:
            for tf in LENSES:
                f = OUT / "crosses" / sym / f"{tf}.parquet"
                if f.exists():
                    d = pd.read_parquet(f, columns=["pair", "event"])
                    inv += int(((d.pair == tag) &
                                d.event.isin(["cross_up", "cross_down"])).sum())
        line(tag, int((ledger.cls == tag).sum()), inv)

    inv = 0
    for sym in PANEL:
        for tf in LENSES:
            f = OUT / "crosses" / sym / f"{tf}.parquet"
            if f.exists():
                d = pd.read_parquet(f, columns=["pair", "event"])
                inv += int(((d.pair == "12_26") &
                            d.event.isin(["cross_up", "cross_down"])).sum())
    o = int(ledger.cls.isin(["12_26 IN-WINDOW", "12_26 bare"]).sum())
    line("12_26 (both halves)", o, inv)

    inv = 0
    for sym in PANEL:
        for tf in LENSES:
            f = OUT / "springs" / sym / f"{tf}.parquet"
            if f.exists():
                inv += P.parquet_rows(f) or 0
    line("spring", int((ledger.cls == "spring").sum()), inv)

    # knot->fan is a JOIN, so it is bounded by both parents, not equal to either
    nk = nf = 0
    for sym in PANEL:
        for tf in LENSES:
            for suf, acc in (("_knots", "k"), ("_fans", "f")):
                f = OUT / "transitions" / sym / f"{tf}{suf}.parquet"
                if f.exists():
                    n = P.parquet_rows(f) or 0
                    if acc == "k":
                        nk += n
                    else:
                        nf += n
    nt = int((ledger.cls == "knot->fan transition").sum())
    bounded = nt <= min(nk, nf)
    ok &= bounded
    print(f"{'knot->fan transition':22s} {nt:>10,d} "
          f"{'k=' + format(nk, ',') + ' f=' + format(nf, ','):>12s} "
          f"{'':>8s}  {'PASS (join <= min(parents))' if bounded else 'FAIL'}")

    nd = int((ledger.cls == "26_89").sum())
    print(f"{'26_89':22s} {nd:>10,d} {'(none)':>12s} {'':>8s}  "
          f"DERIVED THIS PASS -- not in the filed crosses taxonomy; "
          f"excluded from reconciliation by construction")
    hr()
    print(f"F-O1 VERDICT: {'PASS' if ok else 'HALT'}")
    return ok


def f_o1b(fm) -> bool:
    """The derivation rule that produced 26_89 must reproduce a FILED pair."""
    banner("F-O1b  the 26_89 derivation rule reproduces a FILED cross class")
    print("If crossover(e26,e89) is to count as a cross, the same expression must")
    print("reproduce a pair the substrate already filed.  12_26 is re-derived from")
    print("emas and compared to the crosses inventory, cell by cell.\n")
    bad = 0
    tot_d = tot_f = 0
    for sym in PANEL:
        for tf in LENSES:
            e, _ = A.load_cell(sym, tf)
            feas = set(P.feasible_lengths(fm, sym, tf))
            if 12 not in feas or 26 not in feas:
                continue
            a, b = e["e12"].to_numpy(np.float64), e["e26"].to_numpy(np.float64)
            d = int(crossover(a, b).sum() + crossunder(a, b).sum())
            f = OUT / "crosses" / sym / f"{tf}.parquet"
            x = pd.read_parquet(f, columns=["pair", "event"])
            n = int(((x.pair == "12_26") &
                     x.event.isin(["cross_up", "cross_down"])).sum())
            tot_d += d
            tot_f += n
            if d != n:
                bad += 1
                print(f"  MISMATCH {sym} {tf}: derived={d:,} filed={n:,}")
    print(f"  re-derived total = {tot_d:,}   filed total = {tot_f:,}   "
          f"mismatched cells = {bad}")
    print(f"F-O1b VERDICT: {'PASS' if bad == 0 else 'HALT'}")
    return bad == 0


# ===================================================================== W-E+
CARDS = ["ETHUSDT_swing|c61t75", "ETHUSDT_intraday|c554t720",
         "ETHUSDT_intraday|c186t225"]


def stage_we(cards=CARDS) -> list[dict]:
    banner("STAGE W-E+  --  TOP-3 FULL CARDS  (straight from the campaign rows; "
           "NO recomputation)")
    box = ROOT / "_reviewer_box" / "wf1"
    want = set(cards)
    raw: dict[str, dict] = {}
    for f in sorted(box.glob("*USDT_*.json")):
        for r in json.loads(f.read_text(encoding="utf-8")).get("rows", []):
            tid = f"{r.get('cell')}|{r.get('tranche_id')}"
            if tid in want:
                raw[tid] = {"_src": str(f.relative_to(ROOT)), **r}
    cen = pd.read_parquet(OUT.parent / "census2a" / "cen5" / "cen5_campaigns.parquet")
    cen = cen.set_index("tranche_id")

    out = []
    FIELDS = [("entry px_fill", "px_fill"), ("stop", "stop"),
              ("exit px", "exit_px_fill"), ("exit ts", "ts_close"),
              ("exit_reason", "exit_reason"), ("realized_r", "realized_r"),
              ("mfe_r", "mfe_r"), ("mae_r", "mae_r"),
              ("give_back_r", "give_back_r"), ("funding_cum", "funding_cum"),
              ("hold", "hold_s")]
    for tid in cards:
        r = raw.get(tid)
        print()
        hr("=")
        print(f"CARD  {tid}")
        hr("=")
        if r is None:
            print("  ABSENT from _reviewer_box/wf1 -- NOT FABRICATED")
            out.append({"tranche_id": tid, "present": False})
            continue
        rec = {"tranche_id": tid, "present": True, "source": r["_src"],
               "symbol": r.get("symbol"), "mandate": r.get("mandate"),
               "dir": r.get("dir"), "size_r": r.get("size_r"),
               "ts_open": r.get("ts_open"), "grade": r.get("grade"),
               "zone": r.get("zone"), "stage": r.get("stage"),
               "fill_class": r.get("fill_class"), "tier": r.get("tier")}
        print(f"  {'source':16s} {r['_src']}")
        print(f"  {'symbol/mandate':16s} {r.get('symbol')} / {r.get('mandate')}"
              f"   dir={r.get('dir')}  size_r={r.get('size_r')}"
              f"  grade={r.get('grade')}  zone={r.get('zone')}")
        print(f"  {'entry ts':16s} {r.get('ts_open')}")
        for label, key in FIELDS:
            v = r.get(key)
            rec[key] = v
            unit = " s" if key == "hold_s" else ""
            print(f"  {label:16s} {v}{unit}")
        # gross_R is the STORED ride_R from cen5 -- read, not recomputed
        if tid in cen.index:
            g = float(cen.loc[tid, "ride_R"])
            rec["gross_R"] = g
            print(f"  {'gross_R':16s} {g:.6f}   "
                  f"[cen5_campaigns.ride_R, stored]")
        else:
            rec["gross_R"] = None
            print(f"  {'gross_R':16s} ABSENT from cen5_campaigns")
        out.append(rec)
    print()
    return out


# ===================================================================== main
def main() -> int:
    banner(f"CENSUS-2B ORACLE  (Mac-native rev C)   seed={SEED}   "
           f"{datetime.now(timezone.utc).isoformat(timespec='seconds')}")
    print(f"panel  = {PANEL}")
    print(f"lenses = {LENSES}")
    print(f"substrate = {OUT}")
    print("class  = Tier-E + instrument re-pins; NO REGISTRATIONS; m=0")

    fm = A.load_feasibility()
    ORC.mkdir(parents=True, exist_ok=True)

    pin, rerun = stage_r1(fm)
    occ2 = stage_r2(fm)
    occ3 = stage_r3(fm)
    ledger = stage_o(fm)
    grid = oracle_grid(ledger)
    ok = f_o1(ledger)
    ok &= f_o1b(fm)
    cards = stage_we()

    for name, df in [("r1_pinned_scales", pin), ("r1_rerun_inert", rerun),
                     ("r2_knot_occupancy", occ2), ("r3_state_occupancy", occ3)]:
        P.to_parquet_atomic(df, ORC / f"{name}.parquet")

    man = {"program": "scripts/census2b_oracle.py", "module": "ORACLE rev C",
           "seed": SEED, "class": "Tier-E + instrument re-pins; m=0",
           "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "lenses": LENSES, "panel": PANEL,
           "pins": {"kiss_v2_law": "delta = min(0.75, 0.6 x p95 |spread|/ATR) per pair; eps = delta/3; k = 10",
                    "knot_law": f"per-SR width_atr < {KNOT_C}",
                    "state_k_law": "k = max(20, round(median_len/8)) per SR",
                    "state_k": {f: k_for(f) for f in P.FAMILIES},
                    "toll_bps_round_trip": P.TOLL_BPS_ROUND_TRIP,
                    "horizons_ms": A.HORIZONS_MS},
           "artifacts": {}}
    for p in sorted(ORC.rglob("*.parquet")):
        man["artifacts"][str(p.relative_to(ORC))] = {
            "rows": P.parquet_rows(p), "bytes": p.stat().st_size,
            "sha256": P.sha256_file(p)}
    (ORC / "oracle_manifest.json").write_text(json.dumps(man, indent=1) + "\n")
    with open(ORC / "cards.json", "w") as f:
        json.dump(cards, f, indent=1, default=str)

    banner("PROBE LEDGER  --  m = 0")
    print("  module      : CENSUS-2B ORACLE rev C")
    print("  motif surface m = 0.  Nothing here is a registration.  The grid is a")
    print("  COMPLETE partition of the filed event substrate under one ruler; no")
    print("  cell was selected, ranked, or promoted, so there is no family to")
    print("  correct over.  Any future selection FROM this grid is a new probe")
    print("  and must declare its own m BEFORE it looks.")
    print(f"  seed        : {SEED}")
    print(f"  artifacts   : {ORC}")

    hr("=")
    print(f"ORACLE COMPLETE  verdict={'PASS' if ok else 'HALT'}  "
          f"elapsed={time.time() - _T0:.0f}s")
    hr("=")
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
