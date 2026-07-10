"""Indicator primitives matching the build prompt §5 semantics exactly.

- EMA: standard recursive, alpha = 2/(len+1), seeded at series start.
  (Seed effects are made negligible by the F7 warm-up floor; parity tolerance
  for EMA/ATR values is 0.05% after warm-up.)
- ATR: Wilder smoothing (RMA, alpha = 1/len) of true range — not SMA, not EMA.
- Volume MA: SMA.
- Cross semantics: crossover(a,b) <=> a>b now AND a<=b on the prior bar.

All computations are single-threaded, vectorized where associative, and
deterministic: same inputs -> bit-identical outputs.
"""

import numpy as np


def ema(values: np.ndarray, length: int) -> np.ndarray:
    """Recursive EMA seeded at the series start (first finite value)."""
    alpha = 2.0 / (length + 1.0)
    out = np.full(len(values), np.nan)
    prev = np.nan
    for i, v in enumerate(values):
        if np.isnan(v):
            out[i] = prev
            continue
        prev = v if np.isnan(prev) else prev + alpha * (v - prev)
        out[i] = prev
    return out


def rma(values: np.ndarray, length: int) -> np.ndarray:
    """Wilder smoothing, alpha = 1/len, seeded at the series start."""
    alpha = 1.0 / length
    out = np.full(len(values), np.nan)
    prev = np.nan
    for i, v in enumerate(values):
        if np.isnan(v):
            out[i] = prev
            continue
        prev = v if np.isnan(prev) else prev + alpha * (v - prev)
        out[i] = prev
    return out


def true_range(high: np.ndarray, low: np.ndarray, close: np.ndarray) -> np.ndarray:
    prev_close = np.concatenate(([np.nan], close[:-1]))
    tr = np.maximum(high - low,
                    np.maximum(np.abs(high - prev_close), np.abs(low - prev_close)))
    tr[0] = high[0] - low[0]
    return tr


def atr(high: np.ndarray, low: np.ndarray, close: np.ndarray, length: int) -> np.ndarray:
    return rma(true_range(high, low, close), length)


def sma(values: np.ndarray, length: int) -> np.ndarray:
    out = np.full(len(values), np.nan)
    if len(values) >= length:
        c = np.cumsum(values, dtype=np.float64)
        out[length - 1] = c[length - 1] / length
        out[length:] = (c[length:] - c[:-length]) / length
    return out


def crossover(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """a > b now AND a <= b on the prior bar. NaN comparisons are False."""
    a_prev = np.concatenate(([np.nan], a[:-1]))
    b_prev = np.concatenate(([np.nan], b[:-1]))
    with np.errstate(invalid="ignore"):
        return (a > b) & (a_prev <= b_prev)


def crossunder(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    a_prev = np.concatenate(([np.nan], a[:-1]))
    b_prev = np.concatenate(([np.nan], b[:-1]))
    with np.errstate(invalid="ignore"):
        return (a < b) & (a_prev >= b_prev)


def rolling_min(values: np.ndarray, length: int) -> np.ndarray:
    """ta.lowest equivalent: NaN until `length` bars exist."""
    import pandas as pd
    return pd.Series(values).rolling(length, min_periods=length).min().to_numpy()


def rolling_max(values: np.ndarray, length: int) -> np.ndarray:
    import pandas as pd
    return pd.Series(values).rolling(length, min_periods=length).max().to_numpy()
