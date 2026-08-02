"""Volatility recipes.

`percentile_rank` is the package's only `endpoint_only` function: a rank against
a trailing sample is meaningful at the tip of the array and nowhere else.  Per
§I.5 it is exempt from F-AN-13 but MUST raise when misused, so a caller contract
that used to live in a human's head becomes a property asserted in code.
"""

import numpy as np

from analytics.momentum import rma

__all__ = ["true_range", "atr", "realised_vol", "percentile_rank"]


def _arr(x):
    return np.asarray(x, dtype=float)


def true_range(high, low, close):
    """TR = max(H-L, |H - C_prev|, |L - C_prev|).  NaN at index 0."""
    h, l, c = _arr(high), _arr(low), _arr(close)
    out = np.full(h.shape, np.nan)
    if len(h) == 0:
        return out
    pc = np.concatenate([[np.nan], c[:-1]])
    out = np.maximum(h - l, np.maximum(np.abs(h - pc), np.abs(l - pc)))
    out[0] = h[0] - l[0]
    return out


def atr(high, low, close, length=14):
    """ATR, Wilder smoothing of true range."""
    return rma(true_range(high, low, close), length)


def realised_vol(close, fast=7, slow=30):
    """Close-to-close log-return stdev over trailing windows, reported as the
    fast/slow ratio.  NOT annualised.  Returns (fast_sd, slow_sd, ratio)."""
    c = _arr(close)
    n = len(c)
    r = np.full(n, np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        r[1:] = np.log(c[1:] / c[:-1])

    def _sd(win):
        out = np.full(n, np.nan)
        for i in range(n):
            lo = i - win + 1
            if lo < 1:
                continue
            w = r[lo:i + 1]
            if np.isnan(w).any():
                continue
            out[i] = float(np.std(w))        # population form, consistent with §I.4
        return out

    f, s = _sd(fast), _sd(slow)
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = np.where(s > 0, f / s, np.nan)
    return f, s, ratio


def percentile_rank(sample, value=None, as_of_index=None):
    """Rank of `value` within `sample`, 0-100, plus the sample size.

    ENDPOINT_ONLY.  `as_of_index`, when given, must point at the last element of
    `sample`; anything else raises.  A percentile computed against a trailing
    sample is a statement about the tip of that sample, and silently honouring a
    mid-array index would produce a number that looks fine and means nothing.
    """
    s = _arr(sample)
    s = s[~np.isnan(s)]
    if as_of_index is not None and as_of_index != len(sample) - 1:
        raise ValueError(
            f"percentile_rank is endpoint_only: as_of_index={as_of_index} but the "
            f"sample ends at {len(sample) - 1}. Slice the sample to the decision "
            f"bar and call again.")
    if value is None:
        if len(s) == 0:
            return np.nan, 0
        value = float(s[-1])
    if len(s) == 0:
        return np.nan, 0
    return 100.0 * float(np.sum(s < value)) / len(s), int(len(s))
