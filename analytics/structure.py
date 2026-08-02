"""Structure recipes: pivots, period opens, prior-period extremes.

`pivots` is the package's `lag:N` case and the reason CONFIRMATION_LAG is a
module constant rather than a comment.  A pivot(5,5) at bar i is only KNOWABLE
at bar i+5, because five subsequent bars are required to confirm it.  A level
registry that consumes unconfirmed pivots is reading the future -- which is
exactly the class of defect F-AN-13 exists to catch.
"""

import numpy as np

__all__ = ["CONFIRMATION_LAG", "pivots", "confirmed_pivots",
           "period_opens", "prior_period_extremes", "resample_ohlcv",
           "infer_step_ms"]

CONFIRMATION_LAG = 5


def infer_step_ms(open_time_ms):
    """Median positive spacing of a timestamp array, or None if undecidable.

    Used to tell a CLOSED aggregation bucket from a still-forming one.  The
    median rather than the last gap: a single missing bar must not redefine the
    source interval.
    """
    t = np.asarray(open_time_ms, dtype="int64")
    if t.size < 2:
        return None
    d = np.diff(t)
    d = d[d > 0]
    if d.size == 0:
        return None
    return int(np.median(d))


def _bucket_is_closed(last_key, step_ms, last_open_time, src_step_ms):
    """Does the source data reach the end of the bucket beginning at last_key?

    A bucket is CLOSED when the bar that completes it is present.  The last
    source bar covers [last_open_time, last_open_time + src_step_ms), so the
    bucket is closed exactly when that reach lands on or past its end.
    """
    if src_step_ms is None:
        return None                      # undecidable -- never guess
    return (int(last_open_time) + int(src_step_ms)) >= (int(last_key) + int(step_ms))


def resample_ohlcv(open_time_ms, open_, high, low, close, volume, step_ms,
                   drop_unclosed=True):
    """OHLCV aggregation onto a UTC floor-division grid.  CLOSED BUCKETS ONLY.

    Aggregation convention is byte-identical to `scripts/s1_resample.aggregate()`
    -- key = open_time // step_ms * step_ms, then first/max/min/last/sum.
    F-AN-14 asserts that equivalence from the test file rather than here, so
    `analytics/` keeps invariant I-B (no engine or script imports).

    Basis: `engine/s1.py:70-73` already extends 30m and 1d outside the frozen
    INTERVAL_MS/MTF_SET map and is F-RESAMPLE PASS, so daily ATR is an existing
    fixtured capability. Match that convention; do not invent one.

    AMENDMENT FAN8 (2026-08-02, operator-ratified).  The final bucket is DROPPED
    when the source data does not reach its end.  Rationale on record: keeping
    the in-progress bucket published a number computed from a fraction of a
    period -- a 1d "bar" built from a single 1h bar reads as a day.  Preserving
    it would enshrine a known defect to protect a number now known to be wrong,
    and it is not reproducible: re-run an hour later and it changes.

    The disclosed cost is real and is the operator's ruling to have taken: the
    last row is now the last FINISHED period, not the forming one a chart shows
    mid-candle.

    `drop_unclosed=False` reinstates the old behaviour.  It exists so a fixture
    can PROVE the dropped bar is the only difference (F-AN-8b) and so F-AN-14 can
    still assert the aggregation convention itself is untouched.  It is not part
    of the public contract -- see `_resample_ohlcv_legacy`.

    When the source spacing cannot be inferred (fewer than two bars), closure is
    undecidable and nothing is dropped: guessing would be worse than keeping.
    """
    # WHY PANDAS HERE, in an otherwise numpy-pure package: F-AN-14 requires
    # BYTE-IDENTICAL agreement with scripts/s1_resample.aggregate(), which is a
    # pandas groupby. Summation order is not an implementation detail at that
    # standard -- a numpy pairwise sum differs from pandas' accumulation by 1 ULP
    # on real volume data (measured: max abs 3.6e-12, max 1 ULP). Matching the
    # reference exactly is the only way to satisfy the fixture as written; a
    # tolerance would have quietly lowered the bar the project sets everywhere
    # else with its byte-identity fixtures. No I/O is introduced -- read_parquet
    # and friends remain banned and F-AN-4 still scans for them.
    import pandas as pd

    t = np.asarray(open_time_ms, dtype="int64")
    src = pd.DataFrame({
        "open_time": t,
        "open": _arr(open_), "high": _arr(high), "low": _arr(low),
        "close": _arr(close), "volume": _arr(volume),
    })
    key = src["open_time"].to_numpy(np.int64) // int(step_ms) * int(step_ms)
    g = src.groupby(key, sort=True)
    out = {
        "open_time": np.asarray(sorted(set(key)), dtype=np.int64),
        "open": g["open"].first().to_numpy(float),
        "high": g["high"].max().to_numpy(float),
        "low": g["low"].min().to_numpy(float),
        "close": g["close"].last().to_numpy(float),
        "volume": g["volume"].sum().to_numpy(float),
    }

    if not drop_unclosed or out["open_time"].size == 0 or t.size == 0:
        return out
    closed = _bucket_is_closed(out["open_time"][-1], step_ms, t[-1],
                               infer_step_ms(t))
    if closed is False:
        out = {k: v[:-1] for k, v in out.items()}
    return out


def _resample_ohlcv_legacy(open_time_ms, open_, high, low, close, volume, step_ms):
    """TEST-ONLY.  Pre-Amendment-FAN8 behaviour: keeps the forming bucket.

    Deliberately NOT in `__all__` and deliberately underscore-prefixed.  Its only
    purpose is to let F-AN-8b reinstate the in-progress bucket and demonstrate
    that reinstating it reproduces the v1.1 published numbers EXACTLY -- which is
    what proves the dropped bar is the ONLY thing that moved.  A fixture asserts
    that `scripts/daily_brief.py` contains no reference to this name, so it
    cannot leak into production by drift.
    """
    return resample_ohlcv(open_time_ms, open_, high, low, close, volume,
                          step_ms, drop_unclosed=False)


def _arr(x):
    return np.asarray(x, dtype=float)


def pivots(values, left=5, right=5, kind="high"):
    """Pivot indices in `values`.

    Returns (indices, levels, confirmed_at) where confirmed_at = index + right.
    A caller working as-of bar k must filter to `confirmed_at <= k`; the helper
    `confirmed_pivots` does exactly that and should be preferred.
    """
    v = _arr(values)
    n = len(v)
    idx, lvl, conf = [], [], []
    for i in range(left, n - right):
        w = v[i - left:i + right + 1]
        if np.isnan(w).any():
            continue
        c = v[i]
        if kind == "high":
            ok = c == np.max(w) and np.sum(w == c) == 1
        else:
            ok = c == np.min(w) and np.sum(w == c) == 1
        if ok:
            idx.append(i)
            lvl.append(float(c))
            conf.append(i + right)
    return np.array(idx, dtype=int), np.array(lvl, dtype=float), np.array(conf, dtype=int)


def confirmed_pivots(values, as_of_index, left=5, right=5, kind="high"):
    """Pivots knowable at `as_of_index`.  This is the as-of-safe entry point."""
    idx, lvl, conf = pivots(values, left, right, kind)
    keep = conf <= as_of_index
    return idx[keep], lvl[keep], conf[keep]


def period_opens(open_time_ms, open_, period="D"):
    """Opening price of each calendar period, and the running current-period open.

    `period` in {'D','W','M','Q','Y'}.  Returns (bucket_key, period_open) arrays;
    period_open[i] is the open of the period bar i belongs to -- causal, because
    it is fixed at the first bar of the period.
    """
    t = np.asarray(open_time_ms, dtype="int64")
    o = _arr(open_)
    d = t.astype("datetime64[ms]").astype("datetime64[D]")
    if period == "D":
        key = d
    elif period == "W":
        key = d - (d.astype("datetime64[D]").astype(int) + 4) % 7   # ISO Monday
    elif period == "M":
        key = d.astype("datetime64[M]")
    elif period == "Y":
        key = d.astype("datetime64[Y]")
    elif period == "Q":
        m = d.astype("datetime64[M]").astype(int)
        key = (m - m % 3).astype("datetime64[M]")
    else:
        raise ValueError(f"unknown period {period!r}")

    key = np.asarray(key)
    out = np.full(len(o), np.nan)
    seen = {}
    for i in range(len(o)):
        k = key[i]
        kk = k.astype("datetime64[ms]").astype("int64").item()
        if kk not in seen:
            seen[kk] = float(o[i])
        out[i] = seen[kk]
    return key, out


def prior_period_extremes(open_time_ms, high, low, period="D"):
    """High and low of the PREVIOUS completed period, as-of each bar.

    Causal by construction: a bar only ever sees periods that closed before its
    own period began.
    """
    key, _ = period_opens(open_time_ms, high, period)
    h, l = _arr(high), _arr(low)
    n = len(h)
    ph = np.full(n, np.nan)
    pl = np.full(n, np.nan)

    order, agg = [], {}
    for i in range(n):
        kk = key[i].astype("datetime64[ms]").astype("int64").item()
        if kk not in agg:
            agg[kk] = [h[i], l[i]]
            order.append(kk)
        else:
            agg[kk][0] = max(agg[kk][0], h[i])
            agg[kk][1] = min(agg[kk][1], l[i])
        pos = len(order) - 1
        if pos > 0:
            prev = agg[order[pos - 1]]
            ph[i], pl[i] = prev[0], prev[1]
    return ph, pl
