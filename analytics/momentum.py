"""Momentum recipes. Pure arithmetic on arrays.

Every function here is CAUSAL: the value at index i depends only on x[0..i].
That is asserted by F-AN-13, not merely intended -- see analytics/__init__.py
CONVENTIONS for the causality class of each.

Warm-up policy (I-D): a function returns NaN for exactly the documented number
of leading positions and a finite value immediately after. It never seeds a
number into the warm-up region to make a chart look continuous.
"""

import numpy as np

__all__ = ["sma", "ema", "rma", "rsi", "stoch_rsi", "macd",
           "awesome_oscillator", "divergences"]


def _arr(x):
    return np.asarray(x, dtype=float)


def sma(x, length):
    """Simple moving average. NaN for the first length-1 positions."""
    x = _arr(x)
    out = np.full(x.shape, np.nan)
    if length <= 0 or len(x) < length:
        return out
    c = np.cumsum(np.insert(x, 0, 0.0))
    out[length - 1:] = (c[length:] - c[:-length]) / length
    return out


def ema(x, length):
    """Exponential moving average, alpha = 2/(length+1), seeded with the SMA of
    the first `length` values at index length-1.  NaN before that."""
    x = _arr(x)
    out = np.full(x.shape, np.nan)
    if length <= 0 or len(x) < length:
        return out
    alpha = 2.0 / (length + 1.0)
    prev = float(np.mean(x[:length]))
    out[length - 1] = prev
    for i in range(length, len(x)):
        prev = prev + alpha * (x[i] - prev)
        out[i] = prev
    return out


def rma(x, length):
    """Wilder's smoothing (alpha = 1/length), seeded with the mean of the first
    `length` values.  This is the smoothing RSI and ATR use."""
    x = _arr(x)
    out = np.full(x.shape, np.nan)
    if length <= 0 or len(x) < length:
        return out
    alpha = 1.0 / length
    prev = float(np.mean(x[:length]))
    out[length - 1] = prev
    for i in range(length, len(x)):
        prev = prev + alpha * (x[i] - prev)
        out[i] = prev
    return out


def rsi(close, length=14):
    """RSI, Wilder/RMA smoothing, source close.  NaN for the first `length`
    positions (one more than RMA, because the difference loses a bar)."""
    c = _arr(close)
    out = np.full(c.shape, np.nan)
    if len(c) < length + 1:
        return out
    d = np.diff(c)
    gain, loss = np.clip(d, 0, None), np.clip(-d, 0, None)
    ag, al = rma(gain, length), rma(loss, length)
    with np.errstate(divide="ignore", invalid="ignore"):
        rs = np.where(al == 0, np.inf, ag / np.where(al == 0, 1.0, al))
        r = 100.0 - 100.0 / (1.0 + rs)
    r = np.where(al == 0, np.where(ag == 0, 50.0, 100.0), r)
    out[1:] = np.where(np.isnan(ag), np.nan, r)
    return out


def _sma_after_warmup(x, length):
    """SMA applied from the first finite value onward.

    FINDING F-2R-A (2026-08-03).  `sma` is cumsum-based, so a SINGLE leading NaN
    poisons every later value.  `stoch_rsi`'s raw stochastic always has a NaN
    prefix (RSI's own warm-up plus the stochastic window), so `sma(raw, k)`
    returned ALL NaN -- and therefore StochRSI never produced a number, on any
    input, ever.  Measured before the fix: 100% of stoch_rsi values in the
    2026-08-03 capture were null, across all ten assets and all five timeframes.

    F-AN-13 did not catch it because the truncation assertion compares
    `got[k-1] == ref[k-1]` with a NaN-equals-NaN branch, and an all-NaN series
    satisfies that at every k.  A fixture that cannot fail is not a guard, which
    is why F-AN-6b now asserts the output is FINITE after warm-up.

    Fixed HERE rather than in `sma` deliberately: making `sma` NaN-tolerant would
    change every other consumer, including `awesome_oscillator`, whose input has
    no NaNs and whose published numbers must not move.

    Interior NaNs are NOT papered over.  A gap inside the finite region is a real
    discontinuity, and smoothing across it would invent data; the result stays
    NaN and the caller sees the gap.
    """
    x = _arr(x)
    out = np.full(x.shape, np.nan)
    fin = np.isfinite(x)
    if not fin.any():
        return out
    first = int(np.argmax(fin))
    seg = x[first:]
    if np.isnan(seg).any():
        return out
    out[first:] = sma(seg, length)
    return out


def stoch_rsi(close, rsi_length=14, stoch_length=14, k=3, d=3):
    """StochRSI: RSI(14) -> stochastic(14) -> %K smoothed 3 -> %D smoothed 3.

    Returns (k_line, d_line), both 0-100.  Warm-up is
    rsi_length + stoch_length + k + d - 3 for %D, exactly as CONVENTIONS records.
    """
    r = rsi(close, rsi_length)
    n = len(r)
    raw = np.full(n, np.nan)
    for i in range(n):
        lo_i = i - stoch_length + 1
        if lo_i < 0:
            continue
        w = r[lo_i:i + 1]
        if np.isnan(w).any():
            continue
        lo, hi = float(np.min(w)), float(np.max(w))
        raw[i] = 50.0 if hi == lo else 100.0 * (r[i] - lo) / (hi - lo)
    k_line = _sma_after_warmup(raw, k)
    d_line = _sma_after_warmup(k_line, d)
    return k_line, d_line


def macd(close, fast=12, slow=26, signal=9):
    """MACD line, signal line, histogram.  Source close."""
    c = _arr(close)
    line = ema(c, fast) - ema(c, slow)
    sig = ema(np.nan_to_num(line, nan=0.0), signal)
    sig = np.where(np.isnan(line), np.nan, sig)
    # the signal EMA is only meaningful once the MACD line itself is defined
    first = int(np.argmax(~np.isnan(line))) if (~np.isnan(line)).any() else len(c)
    sig[:min(first + signal - 1, len(c))] = np.nan
    return line, sig, line - sig


def awesome_oscillator(high, low, fast=5, slow=34):
    """AO = SMA(5) - SMA(34) of the bar midpoint (H+L)/2."""
    mid = (_arr(high) + _arr(low)) / 2.0
    return sma(mid, fast) - sma(mid, slow)


def divergences(price_pivot_idx, price_pivot_val,
                osc_pivot_idx, osc_pivot_val, pivot_kind,
                kind="regular", max_pairs=2):
    """Compare the last `max_pairs` confirmed pivot pairs on price against the
    oscillator's pivots at the same indices.

    `pivot_kind` ("high" or "low") is required, not optional, because BOTH
    divergence classes are cases of `price_up != osc_up` and only the pivot type
    separates them:

        on LOWS   price lower-low  + osc higher-low   -> REGULAR bullish
                  price higher-low + osc lower-low    -> HIDDEN  bullish
        on HIGHS  price higher-high+ osc lower-high   -> REGULAR bearish
                  price lower-high + osc higher-high  -> HIDDEN  bearish

    Inputs are CONFIRMED pivots only -- the caller applies `structure.pivots`'
    confirmation lag.  Each result carries the price level of its pivot, which
    is what lets a divergence be matched to the confluence area containing it.
    """
    if pivot_kind not in ("high", "low"):
        raise ValueError(f"pivot_kind must be 'high' or 'low', got {pivot_kind!r}")
    if kind not in ("regular", "hidden"):
        raise ValueError(f"kind must be 'regular' or 'hidden', got {kind!r}")

    oi = dict(zip(osc_pivot_idx, osc_pivot_val))
    usable = [(i, v) for i, v in zip(price_pivot_idx, price_pivot_val) if i in oi]

    out = []
    for (i0, p0), (i1, p1) in zip(usable[-(max_pairs + 1):-1], usable[-max_pairs:]):
        o0, o1 = oi[i0], oi[i1]
        price_up, osc_up = p1 > p0, o1 > o0
        if price_up == osc_up:
            continue                       # agreement is not a divergence
        if pivot_kind == "low":
            this = "regular" if not price_up else "hidden"
            direction = "bullish"
        else:
            this = "regular" if price_up else "hidden"
            direction = "bearish"
        if this != kind:
            continue
        out.append({"kind": kind, "pivot_kind": pivot_kind, "direction": direction,
                    "from_index": int(i0), "to_index": int(i1),
                    "price_from": float(p0), "price_to": float(p1),
                    "osc_from": float(o0), "osc_to": float(o1),
                    "price_level": float(p1)})
    return out
