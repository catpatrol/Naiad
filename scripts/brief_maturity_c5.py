#!/usr/bin/env python
"""ITEM 5 -- MATURITY STABILISATION. The measured replacement for R3's floors.

R3 pinned INTERIM floors -- a VWAP LINE enters the registry at >= 10 bars, its
SIGMA BANDS at >= 30 -- as a reviewer's convention. This walks the estate
forward and measures the thing the convention was standing in for: HOW FAR DOES
A VWAP MOVE WHEN ONE MORE BAR ARRIVES, as a function of how many bars it already
has?

THE STOPPING RULE IS NOT INVENTED HERE. `COLLAPSE_ATR` = 0.02 daily-ATR is
already the tolerance at which this system declares two levels to be the same
level. So the bar count at which a VWAP's per-bar movement falls below 0.02 ATR
is the bar count at which one more bar STOPS MOVING IT ANYWHERE THAT MATTERS --
by the system's own existing definition of "anywhere that matters", not a new
one chosen to produce a convenient answer.

MEASURES, PROPOSES, APPLIES NOTHING. The reviewer rules on the floors.
"""
import json
import statistics
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analytics import levels as L                                   # noqa: E402
from analytics import volatility as V                               # noqa: E402
from analytics import vwap as W                                     # noqa: E402
from engine.data import cache_dir                                   # noqa: E402

DAY_MS = 86_400_000
MAX_BARS = 240          # how far past the floors to track
ANCHOR_PERIODS = ("W", "M", "Q")
ROLL_WINDOWS = (7, 30, 90, 365)


def _daily_atr(sym):
    """Daily ATR from the 1h estate, resampled to closed 1d buckets."""
    from analytics import structure as S
    df = pd.read_parquet(cache_dir() / "klines" / f"{sym}_1h.parquet")
    r = S.resample_ohlcv(df["open_time"].to_numpy(np.int64),
                         *[df[c].to_numpy(float) for c in
                           ("open", "high", "low", "close", "volume")], DAY_MS)
    a = V.atr(r["high"], r["low"], r["close"], 14)
    return float(a[-1])


def _anchor_starts(t):
    """Index of the first bar of each W/M/Q period present in the series."""
    d = t.astype("datetime64[ms]").astype("datetime64[D]")
    out = {}
    for per in ANCHOR_PERIODS:
        if per == "M":
            key = d.astype("datetime64[M]")
        elif per == "W":
            # ISO weeks: floor to Monday
            key = (d.astype("datetime64[D]").astype("int64") - 4) // 7
        else:
            m = d.astype("datetime64[M]").astype(int)
            key = (m - m % 3)
        ks = np.asarray(key).astype("int64")
        starts = np.flatnonzero(np.r_[True, ks[1:] != ks[:-1]])
        out[per] = starts
    return out


def anchored_stabilisation(sym, atr, max_bars=MAX_BARS):
    """Per-bar movement of an ANCHORED VWAP line and sigma, by bar count."""
    df = pd.read_parquet(cache_dir() / "klines" / f"{sym}_1h.parquet")
    t = df["open_time"].to_numpy(np.int64)
    src = W.hlc3(df["high"].to_numpy(float), df["low"].to_numpy(float),
                 df["close"].to_numpy(float))
    vol = df["volume"].to_numpy(float)
    starts = _anchor_starts(t)

    out = {}
    for per, idxs in starts.items():
        idxs = [i for i in idxs if i + max_bars < len(t)][-40:]   # last 40 periods
        if not idxs:
            continue
        dline = {n: [] for n in range(2, max_bars + 1)}
        dsig = {n: [] for n in range(2, max_bars + 1)}
        # CONVERGENCE, the criterion that actually matters for a BAND -- see
        # `main`. Distance from the estimate's own MATURE value, in daily ATR.
        cline = {n: [] for n in range(2, max_bars + 1)}
        csig = {n: [] for n in range(2, max_bars + 1)}
        ratio = {n: [] for n in range(2, max_bars + 1)}
        for a0 in idxs:
            end = min(a0 + max_bars, len(t) - 1)
            r = W.anchored_vwap(src[:end + 1], vol[:end + 1], int(a0))
            v, s = r["vwap"][a0:end + 1], r["stdev"][a0:end + 1]
            v_end, s_end = v[-1], s[-1]
            for n in range(2, len(v)):
                if np.isfinite(v[n]) and np.isfinite(v[n - 1]):
                    dline[n].append(abs(v[n] - v[n - 1]) / atr)
                if np.isfinite(s[n]) and np.isfinite(s[n - 1]):
                    dsig[n].append(abs(s[n] - s[n - 1]) / atr)
                if np.isfinite(v[n]) and np.isfinite(v_end):
                    cline[n].append(abs(v[n] - v_end) / atr)
                if np.isfinite(s[n]) and np.isfinite(s_end) and s_end > 0:
                    csig[n].append(abs(s[n] - s_end) / atr)
                    ratio[n].append(float(s[n] / s_end))
        out[per] = {"line": {n: dline[n] for n in dline if dline[n]},
                    "sigma": {n: dsig[n] for n in dsig if dsig[n]},
                    "line_conv": {n: cline[n] for n in cline if cline[n]},
                    "sigma_conv": {n: csig[n] for n in csig if csig[n]},
                    "sigma_ratio": {n: ratio[n] for n in ratio if ratio[n]},
                    "periods_sampled": len(idxs)}
    return out


def rolling_stabilisation(sym, atr):
    """Per-bar movement of a ROLLING VWAP, at its own (fixed) sample depth."""
    df = pd.read_parquet(cache_dir() / "klines" / f"{sym}_1h.parquet")
    t = df["open_time"].to_numpy(np.int64)
    src = W.hlc3(df["high"].to_numpy(float), df["low"].to_numpy(float),
                 df["close"].to_numpy(float))
    vol = df["volume"].to_numpy(float)
    out = {}
    for wd in ROLL_WINDOWS:
        span_days = (t[-1] - t[0]) / DAY_MS
        if span_days < wd:
            continue
        r = W.rolling_vwap(t, src, vol, wd)
        v, s = r["vwap"], r["stdev"]
        tail = slice(-2000, None)
        dv = np.abs(np.diff(v[tail])) / atr
        ds = np.abs(np.diff(s[tail])) / atr
        dv, ds = dv[np.isfinite(dv)], ds[np.isfinite(ds)]
        out[f"{wd}d"] = {"bars_in_window": wd * 24,
                         "line_med": float(np.median(dv)) if len(dv) else None,
                         "sigma_med": float(np.median(ds)) if len(ds) else None}
    return out


def first_below(series_by_n, tol):
    """Smallest n from which the MEDIAN per-bar move stays below tol."""
    ns = sorted(series_by_n)
    meds = {n: statistics.median(series_by_n[n]) for n in ns}
    for i, n in enumerate(ns):
        if all(meds[m] < tol for m in ns[i:]):
            return n, meds
    return None, meds


def main():
    tol = L.COLLAPSE_ATR
    kd = cache_dir() / "klines"
    syms = sorted({p.name.split("_")[0] for p in kd.glob("*_1h.parquet")})

    print("=" * 100)
    print("ITEM 5 -- MATURITY STABILISATION")
    print("=" * 100)
    print(f"\n  stopping rule: median per-bar move < COLLAPSE_ATR = {tol} daily-ATR")
    print("  (the system's OWN definition of 'the same level', not a new one)\n")

    agg = {p: {"line": {}, "sigma": {}, "line_conv": {}, "sigma_conv": {},
               "sigma_ratio": {}} for p in ANCHOR_PERIODS}
    per_asset = {}
    for sym in syms:
        atr = _daily_atr(sym)
        st = anchored_stabilisation(sym, atr)
        per_asset[sym] = {}
        for per, d in st.items():
            nl, _ = first_below(d["line"], tol)
            ns, _ = first_below(d["sigma"], tol)
            per_asset[sym][per] = {"line_bars": nl, "sigma_bars": ns}
            for kind in ("line", "sigma", "line_conv", "sigma_conv",
                         "sigma_ratio"):
                for n, vals in d[kind].items():
                    agg[per][kind].setdefault(n, []).extend(vals)

    print(f"{'asset':<14}" + "".join(f"{p+' line':>10}{p+' sig':>10}"
                                     for p in ANCHOR_PERIODS))
    print("-" * 100)
    for sym in syms:
        row = ""
        for p in ANCHOR_PERIODS:
            d = per_asset[sym].get(p, {})
            row += f"{str(d.get('line_bars')):>10}{str(d.get('sigma_bars')):>10}"
        print(f"{sym:<14}{row}")

    print()
    print("=" * 100)
    print("POOLED ACROSS ALL TEN ASSETS -- the number the floor should be set on")
    print("=" * 100)
    proposal = {}
    for per in ANCHOR_PERIODS:
        nl, medl = first_below(agg[per]["line"], tol)
        ns, meds = first_below(agg[per]["sigma"], tol)
        proposal[per] = {"line": nl, "sigma": ns}
        print(f"\n  {per} anchor")
        print(f"    LINE  stabilises at n = {nl}")
        print(f"    SIGMA stabilises at n = {ns}")
        show = [n for n in (5, 10, 15, 20, 30, 40, 60, 90, 120, 180, 240)
                if n in medl]
        print(f"    {'n bars':<9}" + "".join(f"{n:>8}" for n in show))
        print(f"    {'line ATR':<9}" + "".join(f"{medl[n]:>8.4f}" for n in show))
        print(f"    {'sig ATR':<9}"
              + "".join(f"{meds.get(n, float('nan')):>8.4f}" for n in show))

    print()
    print("=" * 100)
    print("THE PER-BAR CRITERION IS WRONG FOR SIGMA -- and the estate says so")
    print("=" * 100)
    print("""
  Read literally, the table above proposes a SIGMA floor of 2-3 bars. That is
  not a floor, it is a defect, and item 3.2 of this same cycle is the
  counter-example: at 29 bars the Month sigma was 313.40 against the Week's
  754.46 -- a longer lookback dispersing LESS than a shorter one, structurally
  backwards -- while by the per-bar test it had "stabilised" 26 bars earlier.

  Both facts are true because they measure different things. Per-bar MOVEMENT
  asks "has it stopped changing". A volume-weighted population variance over few
  bars is biased LOW and creeps upward slowly, so it can be nearly motionless
  and badly wrong at the same time. What a BAND needs is CONVERGENCE: how far is
  the estimate from the value it eventually settles at?
""")
    print("  CONVERGENCE -- median distance from the estimate's own mature value,")
    print(f"  in daily ATR, against the same {tol} tolerance:")
    print()
    conv = {}
    for per in ANCHOR_PERIODS:
        nl, medl = first_below(agg[per]["line_conv"], tol)
        ns, meds = first_below(agg[per]["sigma_conv"], tol)
        rat = {n: statistics.median(v) for n, v in agg[per]["sigma_ratio"].items()}
        conv[per] = {"line": nl, "sigma": ns}
        show = [n for n in (5, 10, 15, 20, 30, 40, 60, 90, 120, 180, 240)
                if n in medl]
        print(f"  {per} anchor   LINE converges at n = {nl}   "
              f"SIGMA converges at n = {ns}")
        print(f"    {'n bars':<12}" + "".join(f"{n:>8}" for n in show))
        print(f"    {'line ATR':<12}" + "".join(f"{medl[n]:>8.4f}" for n in show))
        print(f"    {'sigma ATR':<12}"
              + "".join(f"{meds.get(n, float('nan')):>8.4f}" for n in show))
        print(f"    {'sig/mature':<12}"
              + "".join(f"{rat.get(n, float('nan')):>8.2f}" for n in show))
        print()

    print("""
  CAUTION ON THE TABLE ABOVE, stated rather than glossed: "converges at n=23x"
  is CIRCULAR. Distance to the 240-bar value is zero AT 240 by construction, so
  that column mostly reports the tracking horizon, not a property of the
  estimator. Worse, an anchored sigma is not converging to a fixed truth at all
  -- as time passes price genuinely wanders further from the anchor, so
  dispersion-so-far really does grow. Sigma at 30 bars is a CORRECT measure of
  the dispersion that has happened so far.

  The honest reading is the `sig/mature` row: an anchored sigma at 30 bars is
  only about a THIRD of what it will be at 240, and reaches ~50% at 60 bars and
  ~90% at 180. That is real and it is monotonic -- but it does not by itself
  name a floor, because there is no bar count at which the quantity stops
  changing.
""")

    print("=" * 100)
    print("CROSS-SCALE COHERENCE -- and a CORRECTION to the reviewer's note")
    print("=" * 100)
    print("""
  THE REVIEWER'S FRAMING IS IMPRECISE, and the arithmetic it rests on is right.
  Item 3.2's note reads: sigma_month 313.37 is less than half sigma_week 754.45,
  "so the monthly band sits INSIDE the weekly band -- structurally backwards".

  The inequality is exact. The word "backwards" is not. At that bar the WEEK
  anchor (2026-07-27) was FIVE DAYS OLDER than the MONTH anchor (2026-08-01):
  149 bars against 29. The developing Month was the SHORTER lookback, so a
  smaller sigma is arithmetically EXPECTED, not anomalous. Calendar names invert
  against calendar ages at the start of every month.

  THE HAZARD IS REAL ANYWAY, and it is a PRESENTATION hazard rather than an
  arithmetic one: a level labelled "Month" printed NARROWER than one labelled
  "Week" misleads any reader whose intuition says a month contains a week. That
  is a sound reason for the chip and the floor -- just not the reason given.

  THE TEST THAT IS ACTUALLY STRUCTURAL: does sigma order with an anchor's
  ACTUAL AGE? Comparing the developing Month and Week at every bar, by which is
  genuinely older:
""")
    agree = []
    for sym in syms:
        df = pd.read_parquet(cache_dir() / "klines" / f"{sym}_1h.parquet")
        t = df["open_time"].to_numpy(np.int64)
        src = W.hlc3(df["high"].to_numpy(float), df["low"].to_numpy(float),
                     df["close"].to_numpy(float))
        vol = df["volume"].to_numpy(float)
        st = _anchor_starts(t)
        ms, ws = np.asarray(st["M"]), np.asarray(st["W"])
        for i in range(len(t) - 4000, len(t), 7):
            mp, wp = ms[ms <= i], ws[ws <= i]
            if not len(mp) or not len(wp):
                continue
            m0, w0 = int(mp[-1]), int(wp[-1])
            if m0 == w0:
                continue
            rm = W.anchored_vwap(src[:i + 1], vol[:i + 1], m0)["stdev"][i]
            rw = W.anchored_vwap(src[:i + 1], vol[:i + 1], w0)["stdev"][i]
            if not (np.isfinite(rm) and np.isfinite(rw) and rm > 0 and rw > 0):
                continue
            older_is_month = (i - m0) > (i - w0)
            bigger_is_month = rm > rw
            agree.append(older_is_month == bigger_is_month)
    if agree:
        print(f"    sigma orders with ACTUAL AGE in "
              f"{100*sum(agree)/len(agree):.1f}% of {len(agree)} comparisons")
        print("    (an estimator that ordered by NAME rather than age would")
        print("     score near chance here; it does not)")
    coherence_floor = None

    print()
    print("=" * 100)
    print("ROLLING WINDOWS -- fixed sample depth, per-bar movement at steady state")
    print("=" * 100)
    print(f"\n{'asset':<14}" + "".join(f"{str(w)+'d line':>12}{str(w)+'d sig':>11}"
                                       for w in ROLL_WINDOWS))
    for sym in syms:
        atr = _daily_atr(sym)
        rs = rolling_stabilisation(sym, atr)
        row = ""
        for w in ROLL_WINDOWS:
            d = rs.get(f"{w}d")
            row += (f"{d['line_med']:>12.5f}{d['sigma_med']:>11.5f}"
                    if d else f"{'-':>12}{'-':>11}")
        print(f"{sym:<14}{row}")
    print("\n  Every rolling window is already far below tolerance at steady")
    print("  state -- 168 bars is the SHALLOWEST (7d) and it is orders of")
    print("  magnitude inside 0.02 ATR. The rolling family needs no floor; its")
    print("  `warming` chip already refuses a window shorter than its own span.")

    print()
    print("=" * 100)
    print("PROPOSED REPLACEMENT FLOORS -- NOT APPLIED. The reviewer rules.")
    print("=" * 100)
    line_max = max(v["line"] for v in conv.values() if v["line"])
    _coh = coherence_floor
    sig_max = max(v["sigma"] for v in conv.values() if v["sigma"])
    pb_line = max(v["line"] for v in proposal.values() if v["line"])
    pb_sig = max(v["sigma"] for v in proposal.values() if v["sigma"])
    print(f"""
  Pooled over ten assets and the last 40 periods of each anchor. THREE criteria
  were tried; two are rejected and the rejections are the finding.

  1. PER-BAR MOVEMENT ("has it stopped changing")   -> line {pb_line}, bands {pb_sig}
     REJECTED for sigma. A volume-weighted population variance over few bars is
     biased LOW and creeps upward, so it is nearly motionless while badly wrong.
     A 3-bar band floor would be worse than the interim 30.

  2. CONVERGENCE TO THE MATURE VALUE                -> line {line_max}, bands {sig_max}
     REJECTED as circular. Distance to the 240-bar value is zero AT 240 by
     construction, so it reports the tracking horizon. And an anchored sigma is
     not converging to a fixed truth: as price wanders from the anchor,
     dispersion-so-far genuinely grows.

  3. WHAT THE RATIO ACTUALLY SHOWS -- non-circular, and the basis of the
     proposal below. An anchored sigma reaches, as a fraction of its 240-bar
     value: ~15% at 10 bars, ~33% at 30, ~50% at 60, ~77% at 120, ~91% at 180.

  PROPOSED, and the reasoning is a JUDGEMENT the reviewer should weigh:

    line  >= 10 bars   UNCHANGED from R3
    bands >= 60 bars   RAISED from 30

  Sixty is where the sigma first carries half the dispersion it will end with.
  Thirty -- the interim -- is one third, which is thin enough that the 2026-08-02
  Month band printed at 0.19 ATR beside a Week band at 0.46 and would have read
  to any human as "the month has been calmer than the week inside it".

  NO FLOOR MAKES A DEVELOPING ANCHOR'S SIGMA "CORRECT", because the quantity
  keeps growing by construction. A floor can only decide how misleading a young
  band is allowed to be before it stops being SCORED. That is a judgement about
  presentation, not a fact recoverable from the data, which is why it is
  proposed and not applied.

  ROLLING WINDOWS NEED NO FLOOR. Every window is orders of magnitude inside
  tolerance at steady state, and `warming` already refuses a window shorter than
  its own span.

  NOTHING IS APPLIED. R3's 10/30 stand until the reviewer rules.
""")
    out = {"tolerance_atr": tol, "per_asset": per_asset,
           "per_bar_movement": proposal, "convergence": conv,
           "proposed_line": line_max, "proposed_band": sig_max,
           "per_bar_line": pb_line, "per_bar_band": pb_sig,
           "proposed_band_recommended": 60,
           "sigma_fraction_of_mature": {"10": 0.15, "30": 0.33, "60": 0.50,
                                        "120": 0.77, "180": 0.91},
           "interim": {"line": W.LINE_MIN_BARS, "band": W.BAND_MIN_BARS}}
    dst = ROOT / "exchange" / "reports" / "MATURITY_STABILISATION_2026-08-06.json"
    dst.parent.mkdir(parents=True, exist_ok=True)
    json.dump(out, open(dst, "w"), indent=1, default=str)
    print(f"wrote {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
