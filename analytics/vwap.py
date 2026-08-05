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
           "VWAP_SUBSTRATE", "VWAP_SOURCE", "SUBSTRATE_REASONING", "FLOOR_BASIS",
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
# MATURITY FLOORS -- RULED 2026-08-06 (cycle 6 item 1), replacing R3's interim
# 10/30 convention with the cycle-5 measurement.
#
# A VWAP over very few bars is arithmetically exact and informationally empty.
# The LINE is a weighted average and stabilises fast; the SIGMA is a dispersion
# estimate over the same handful of points and stabilises far more slowly --
# which is why the two carry DIFFERENT floors rather than one shared one.
#
# LINE 16 -- MEASURED, not conventional.  At 16 bars the median per-bar move of
# an anchored VWAP line falls below COLLAPSE_ATR (0.02 daily-ATR), which is this
# system's own definition of "the same level".  Per-bar stability is the RIGHT
# test for a converging mean; cycle 5 rejected it only for SIGMA, and that
# rejection does not carry over to the line.
#
# BAND 60 -- MEASURED.  Sixty bars is where an anchored sigma first carries half
# the dispersion it eventually reports (~33% at 30, ~50% at 60, ~91% at 180).
# It guards SAMPLING NOISE, which is the one genuine small-sample defect here.
#
# BELOW THE FLOOR THE VALUE STILL PRINTS, carrying a `thin_sample` chip.  It is
# NOT emitted as a registry level.  That asymmetry is the whole point: hiding it
# would conceal market state the operator asked to see, while scoring it would
# let a two-bar-old anchor cast a confluence vote with the same weight as a
# year of business.
#
# ROLLING WINDOWS TAKE NO FLOOR.  Measured at steady state, every rolling window
# moves orders of magnitude inside tolerance per bar, and the `warming` chip
# already refuses a window shorter than its own span.  A floor there would be
# a second guard on a problem the first one has already solved.
# --------------------------------------------------------------------------

LINE_MIN_BARS = 16
BAND_MIN_BARS = 60

# --------------------------------------------------------------------------
# THE WITHDRAWN PERIOD-RELATIVE FLOOR, and why the reasoning was wrong.
#
# The reviewer proposed scaling the floor to the anchor's period (period/4) on
# the grounds that a YOUNG SIGMA INFLATES THE SIGMA-LABEL and so manufactures
# false reversion signals -- a narrow early band would put price at "sigma 2"
# when a mature band would not.
#
# THAT REASONING IS WRONG, and the correction is worth more than the ruling.
#
# An anchored sigma grows roughly as sqrt(t).  But price's DISPLACEMENT from the
# anchored mean grows as sqrt(t) as well -- both are accumulations of the same
# random walk from the same anchor.  The ratio of the two is therefore
# APPROXIMATELY SCALE-FREE IN TIME: the Z-SCORE a young anchor reports is not
# systematically inflated, even though its band is narrow.
#
# MEASURED ON THE OPERATOR'S OWN CAPTURES, same asset, same Month anchor:
#
#     bar                 bars    sigma       z
#     2026-08-02T04:00Z     29   313.3966   +2.0136
#     2026-08-05T17:00Z    114   583.3876   +1.9389
#
#     sigma grew +86.1%   (sqrt(114/29) = 1.983 predicted, 1.861 observed)
#     z moved     -3.7%
#
# A young band's WIDTH is age-dependent.  Its READING is not.  So the defect a
# period-relative floor was aimed at does not exist, and the floors that remain
# are justified by SAMPLING NOISE alone -- which is exactly what BAND_MIN_BARS
# guards and why it is the larger of the two.
#
# CONSEQUENCE, enforced in the report: comparing one anchor's band WIDTH to
# another's is valid ONLY AT COMPARABLE AGES.  Every place widths appear
# together must print each anchor's AGE IN BARS beside its width.
# --------------------------------------------------------------------------

FLOOR_BASIS = {
    "line": "per-bar move below COLLAPSE_ATR at 16 bars (measured, cycle 5)",
    "band": "sigma carries half its eventual dispersion at 60 bars (measured)",
    "rolling": "no floor; `warming` already refuses a short span",
    "withdrawn": "period-relative (period/4) floor, proposed to stop a young "
                 "sigma inflating the sigma-label. WITHDRAWN: anchored sigma "
                 "and displacement from the anchored mean BOTH grow as sqrt(t), "
                 "so the z-score is approximately scale-free in time. Measured "
                 "on the same Month anchor: sigma +86.1% (29->114 bars) while z "
                 "moved -3.7% (+2.0136 -> +1.9389). A young band's WIDTH is "
                 "age-dependent; its READING is not.",
    "width_comparison_caveat": "band WIDTHS are comparable only at comparable "
                               "ages; print age in bars beside every width",
}


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
