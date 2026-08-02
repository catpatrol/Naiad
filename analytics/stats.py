"""Small statistical helpers. Rolling forms only, so every one stays causal."""

import numpy as np

__all__ = ["zscore", "correlation", "beta"]


def _arr(x):
    return np.asarray(x, dtype=float)


def zscore(x, length):
    """Rolling z-score over a trailing window of `length`.  CAUSAL.

    Population standard deviation, consistent with the VWAP band convention in
    §I.4 -- mixing sample and population forms across one toolbox is how two
    numbers that should agree quietly stop agreeing.
    """
    v = _arr(x)
    n = len(v)
    out = np.full(n, np.nan)
    for i in range(n):
        lo = i - length + 1
        if lo < 0:
            continue
        w = v[lo:i + 1]
        if np.isnan(w).any():
            continue
        sd = float(np.std(w))
        out[i] = 0.0 if sd == 0 else (v[i] - float(np.mean(w))) / sd
    return out


def correlation(a, b, length):
    """Rolling Pearson correlation over a trailing window.  CAUSAL."""
    x, y = _arr(a), _arr(b)
    n = min(len(x), len(y))
    out = np.full(n, np.nan)
    for i in range(n):
        lo = i - length + 1
        if lo < 0:
            continue
        wx, wy = x[lo:i + 1], y[lo:i + 1]
        if np.isnan(wx).any() or np.isnan(wy).any():
            continue
        sx, sy = float(np.std(wx)), float(np.std(wy))
        if sx == 0 or sy == 0:
            continue
        out[i] = float(np.mean((wx - wx.mean()) * (wy - wy.mean()))) / (sx * sy)
    return out


def beta(asset_returns, market_returns, length):
    """Rolling beta of asset against market over a trailing window.  CAUSAL."""
    a, m = _arr(asset_returns), _arr(market_returns)
    n = min(len(a), len(m))
    out = np.full(n, np.nan)
    for i in range(n):
        lo = i - length + 1
        if lo < 0:
            continue
        wa, wm = a[lo:i + 1], m[lo:i + 1]
        if np.isnan(wa).any() or np.isnan(wm).any():
            continue
        var = float(np.var(wm))
        if var == 0:
            continue
        out[i] = float(np.mean((wa - wa.mean()) * (wm - wm.mean()))) / var
    return out
