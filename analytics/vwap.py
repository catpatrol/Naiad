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
           "two_pass_vw_variance", "MIN_BARS", "DAY_MS"]

MIN_BARS = 10
DAY_MS = 86_400_000


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
