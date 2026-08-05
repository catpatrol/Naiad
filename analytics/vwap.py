"""VWAP recipes -- rolling and anchored -- with volume-weighted sigma bands.

The rolling form is PINNED FROM SOURCE: TradingView's published Rolling VWAP
(RVWAP) Pine v5, MPL-2.0, supplied by the operator.  Three things here look
like defects and are not.  Read §I.4 of the contract before changing any of
them:

1.  The variance is the volume-weighted POPULATION variance via the one-pass
    identity E[x^2] - E[x]^2.  There is NO (n-1) correction.  An unweighted
    standard deviation of typical price, or a sample-form correction, produces
    plausible numbers that never match the operator's chart.

2.  The clamp at zero is ALGORITHMIC, not defensive padding.  The one-pass
    identity can go slightly negative through floating-point cancellation at
    high price with low dispersion -- precisely the BTC-at-65,000 case.

3.  The window is a trailing W MILLISECONDS, not a bar count, floored at the 10
    most recent bars even when they fall outside W.  On gapless 24/7 perpetuals
    the two coincide; they diverge only across gaps, which is why the time form
    is implemented.

Window membership: bars with bar_open_time > current_bar_open_time - W,
inclusive of the current bar.  If parity fails by a small amount, test this
boundary FIRST and the min-bars floor at gaps SECOND.
"""

import numpy as np

__all__ = ["hlc3", "rolling_vwap", "anchored_vwap", "vw_sigma_bands",
           "two_pass_vw_variance", "MIN_BARS", "DAY_MS",
           "VWAP_SUBSTRATE", "VWAP_SOURCE", "SUBSTRATE_REASONING",
           "SOURCE_REASONING", "LINE_MIN_BARS", "BAND_MIN_BARS",
           "maturity"]

MIN_BARS = 10
DAY_MS = 86_400_000

# --------------------------------------------------------------------------
# THE PINNED SUBSTRATE AND SOURCE -- operator rulings R1 and R2, 2026-08-05.
#
# These are ratified conventions, not implementation details.  The code already
# did both before the ruling; pinning them is what stops the coincidence from
# drifting.  Every VWAP layer in the instrument must PRINT these two strings on
# itself, so a value that differs from the operator's daily chart explains
# itself on sight rather than becoming a parity incident.
# --------------------------------------------------------------------------

VWAP_SUBSTRATE = "1h"
VWAP_SOURCE = "hlc3"

SUBSTRATE_REASONING = (
    "R1: the 1h computation is the operator's discretionary observation of "
    "which substrate is most faithful. Parity stays checkable BECAUSE "
    "TradingView computes rolling VWAP from CHART bars -- so a 1H chart uses "
    "the same 168 hourly bars we do, and a reading taken there is a direct "
    "test of the path the instrument actually runs on."
)

# R2 REVERSES the addendum's ohlc4 recommendation.  The reversal is on NEW
# INFORMATION, not a change of mind: the operator's ohlc4 chart setting was
# ACCIDENTAL, so the addendum had been reasoning from a mis-set control.
SOURCE_REASONING = (
    "(a) In a 24/7 perpetual market a bar's OPEN IS THE PRIOR BAR'S CLOSE. "
    "ohlc4 therefore partly DOUBLE-COUNTS the prior bar and smears content "
    "across bar boundaries; hlc3 uses only what happened INSIDE the bar. "
    "(b) hlc3 is the standard 'typical price' VWAP definition and is "
    "TradingView's own Rolling VWAP default. "
    "(c) ONE price definition across the whole vwap family, so a disagreement "
    "between two VWAP levels is a MARKET FACT and not a definitional artifact "
    "-- the entire confluence design rests on levels being comparable. "
    "(d) At hourly resolution the ohlc4/hlc3 difference is small and largely "
    "averages out, so the cost of choosing correctly is near zero and the cost "
    "of choosing by accident is a permanent unexplained offset."
)

# --------------------------------------------------------------------------
# MATURITY FLOORS -- operator ruling R3, 2026-08-05.  INTERIM, on the 1h
# substrate; stage 7's MATURITY STABILISATION measurement replaces them with a
# measured rule.
#
# A VWAP over very few bars is arithmetically exact and informationally empty.
# The LINE is a weighted average and stabilises fast; the SIGMA is a dispersion
# estimate over the same handful of points and stabilises far more slowly --
# which is why the two carry DIFFERENT floors rather than one shared one.
#
# BELOW THE FLOOR THE VALUE STILL PRINTS, carrying a `thin_sample` chip.  It is
# NOT emitted as a registry level.  That asymmetry is the whole point: hiding it
# would conceal market state the operator asked to see, while scoring it would
# let a two-bar-old anchor cast a confluence vote with the same weight as a
# year of business.
# --------------------------------------------------------------------------

LINE_MIN_BARS = 10
BAND_MIN_BARS = 30


def maturity(bars, line_min=LINE_MIN_BARS, band_min=BAND_MIN_BARS):
    """Classify a windowed estimator's sample depth against the R3 floors.

    Returns a dict with `bars`, `line_ok`, `band_ok` and `thin_sample`.
    `thin_sample` is True whenever the BANDS are below their floor, because
    that is the flag a reader needs: a mature line with an immature sigma is
    exactly the case that looks trustworthy and is not.

    `bars is None` means the caller could not count -- treated as immature in
    both directions rather than waved through, since an uncountable sample is
    not evidence of a deep one.
    """
    n = None if bars is None else int(bars)
    line_ok = n is not None and n >= line_min
    band_ok = n is not None and n >= band_min
    return {"bars": n, "line_ok": line_ok, "band_ok": band_ok,
            "thin_sample": not band_ok,
            "line_min_bars": line_min, "band_min_bars": band_min}


def _arr(x):
    return np.asarray(x, dtype=float)


def hlc3(high, low, close):
    """The pinned source for every VWAP here."""
    return (_arr(high) + _arr(low) + _arr(close)) / 3.0


def _vw_moments(src, vol):
    """Volume-weighted mean and one-pass population variance over a whole slice."""
    sv = float(np.sum(vol))
    if sv <= 0:
        return np.nan, np.nan
    mean = float(np.sum(src * vol)) / sv
    ex2 = float(np.sum(vol * src * src)) / sv
    return mean, max(ex2 - mean * mean, 0.0)      # clamp is algorithmic


def two_pass_vw_variance(src, vol):
    """Volume-weighted population variance computed the numerically stable way.

    Not used by the pinned recipe -- matching TradingView requires the one-pass
    form.  Knowing that form's fragility at our price scales is a separate
    necessary fact, which is what F-AN-11 measures.
    """
    src, vol = _arr(src), _arr(vol)
    sv = float(np.sum(vol))
    if sv <= 0:
        return np.nan
    mean = float(np.sum(src * vol)) / sv
    return float(np.sum(vol * (src - mean) ** 2)) / sv


def rolling_vwap(open_time_ms, src, volume, window_days, sigmas=(1, 2, 3)):
    """Rolling VWAP over a trailing time window, TradingView RVWAP semantics.

    CAUSAL: the value at index i uses only bars [0..i].

    Returns dict with 'vwap', 'stdev', and 'band_up_k'/'band_dn_k' arrays.
    Positions with no volume in the window are NaN.
    """
    t, s, v = _arr(open_time_ms), _arr(src), _arr(volume)
    n = len(t)
    W = float(window_days) * DAY_MS
    vwap = np.full(n, np.nan)
    stdev = np.full(n, np.nan)

    lo = 0
    for i in range(n):
        # membership: bar_open_time > current_bar_open_time - W, current included
        while lo < i and t[lo] <= t[i] - W:
            lo += 1
        # ...floored at the MIN_BARS most recent bars even if they fall outside W
        start = min(lo, max(0, i - MIN_BARS + 1))
        m, var = _vw_moments(s[start:i + 1], v[start:i + 1])
        vwap[i], stdev[i] = m, (np.sqrt(var) if var == var else np.nan)

    out = {"vwap": vwap, "stdev": stdev}
    for k in sigmas:
        out[f"band_up_{k}"] = vwap + k * stdev
        out[f"band_dn_{k}"] = vwap - k * stdev
    return out


def anchored_vwap(src, volume, anchor_index, sigmas=(1, 2, 3)):
    """VWAP accumulated from `anchor_index` forward.  CAUSAL.

    Bands use the same volume-weighted population variance as the rolling form.
    That is a REASONED INFERENCE from shared TradingView band machinery, NOT read
    from source -- the parity worksheet flags it 'to be confirmed by reading'
    and it must never be asserted as pinned.
    """
    s, v = _arr(src), _arr(volume)
    n = len(s)
    vwap = np.full(n, np.nan)
    stdev = np.full(n, np.nan)
    if not 0 <= anchor_index < n:
        raise ValueError(f"anchor_index {anchor_index} outside series of length {n}")

    csv_ = cv = csv2 = 0.0
    for i in range(anchor_index, n):
        csv_ += s[i] * v[i]
        cv += v[i]
        csv2 += v[i] * s[i] * s[i]
        if cv > 0:
            m = csv_ / cv
            vwap[i] = m
            stdev[i] = np.sqrt(max(csv2 / cv - m * m, 0.0))

    out = {"vwap": vwap, "stdev": stdev}
    for k in sigmas:
        out[f"band_up_{k}"] = vwap + k * stdev
        out[f"band_dn_{k}"] = vwap - k * stdev
    return out


def vw_sigma_bands(vwap, stdev, sigmas=(1, 2, 3)):
    """Bands from an already-computed VWAP and its volume-weighted stdev."""
    vwap, stdev = _arr(vwap), _arr(stdev)
    out = {}
    for k in sigmas:
        out[f"band_up_{k}"] = vwap + k * stdev
        out[f"band_dn_{k}"] = vwap - k * stdev
    return out
