"""Volume profile and the naked-POC registry.

APPROXIMATION, declared not hidden: volume-at-price is built by spreading each
bar's volume uniformly across its high-low range.  Real tick data would move
POC/VAH/VAL somewhat.  Every consumer must carry an `approximation` provenance
chip -- §II.10 G10 keeps those chips on the profile layers.
"""

import numpy as np

__all__ = ["volume_profile", "windowed_profile", "naked_poc_registry",
           "low_volume_nodes", "relative_volume",
           "APPROXIMATION", "PROFILE_ROWS", "VALUE_AREA",
           "LVN_THRESHOLD", "LVN_MIN_ROWS", "WINDOW_SUBSTRATE",
           "RVOL_LOOKBACK_DAYS"]

APPROXIMATION = "volume spread uniformly across each bar's range (not tick data)"

# Amendment 2 §3.3, all v1 PLACEHOLDERS to be re-ratified against the calibration
# report and roughly a week of live use.  Printed in every capture.
PROFILE_ROWS = 120          # rows across each window's range
VALUE_AREA = 0.70           # fraction of window volume

# §3.4.  An LVN is a price shelf where the histogram is near-empty -- the market
# moved through without doing business, and such gaps tend to be revisited.
LVN_THRESHOLD = 0.25        # x the window's MEDIAN row volume
LVN_MIN_ROWS = 3            # contiguous rows

# §3.3 substrate tiers: precision where short-window levels need it, broad
# structure elsewhere without ballooning compute.  Probed and confirmed present
# in the estate for all ten assets (2026-08-03): 1m/5m/15m are all stored, so
# nothing here is silently resampled from a coarser interval.  prior-day is not
# named in the §3.3 table; it is shorter than 7d and takes the finest substrate.
WINDOW_SUBSTRATE = {"prior-day": "1m", "7d": "1m", "30d": "5m",
                    "90d": "15m", "365d": "15m"}


# §3.6 RVOL (ratified B-7).  Twenty trading days of the SAME time-of-day bucket.
RVOL_LOOKBACK_DAYS = 20
_DAY_MS = 86_400_000


def _arr(x):
    return np.asarray(x, dtype=float)


def relative_volume(open_time_ms, volume, as_of_index=None,
                    lookback_days=RVOL_LOOKBACK_DAYS):
    """RVOL -- this bar's volume against the trailing same-time-of-day average.

    Ruling B-7, Amendment 2 §3.6: "current volume against the trailing 20-day
    average for the same time-of-day bucket".  Computable from the single volume
    column the estate stores; CVD/delta remain parked behind an estate-column
    addition (ARGUS_REPRIME §D-AR-9 REVISED).

    WHY TIME-OF-DAY AND NOT A FLAT AVERAGE.  Crypto volume has a hard diurnal
    shape -- the 13:00Z US open hour trades multiples of the 03:00Z hour.  A flat
    20-day mean would score every US-session bar as "high volume" and every Asian
    bar as "low", which is a clock reading, not a market reading.  Comparing a
    bar only against the SAME HOUR on prior days removes that shape.

    CAUSAL, and the current bar is EXCLUDED from its own baseline.  Including it
    would pull the average toward the observation and bias every reading toward
    1.0 -- most visibly on exactly the volume spikes the measure exists to find.

    Returns a dict rather than a bare float: an RVOL of 3.2 computed from four
    samples and one computed from twenty are different claims, so `samples` and
    `warming` travel with the number.
    """
    t = np.asarray(open_time_ms, dtype="int64")
    v = _arr(volume)
    n = len(t)
    i = (n - 1) if as_of_index is None else int(as_of_index)
    out = {"rvol": None, "current_volume": None, "average_volume": None,
           "samples": 0, "lookback_days": int(lookback_days),
           "bucket_ms": None, "warming": True,
           "basis": "same time-of-day bucket, current bar excluded"}
    if n == 0 or not 0 <= i < n:
        return out

    cur = float(v[i])
    bucket = int(t[i] % _DAY_MS)
    out["current_volume"] = cur
    out["bucket_ms"] = bucket

    # The LAST `lookback_days` occurrences of this bucket, strictly earlier than
    # the current bar -- not a time-window filter.  Both agree on gapless data;
    # they diverge across an exchange outage, where a time filter silently
    # returns fewer samples while the intent ("the last 20 of this hour") is
    # still satisfiable.  `oldest_sample_utc_ms` travels with the number so a
    # baseline that had to reach unusually far back is visible rather than
    # implied.
    prior = t[:i]                                   # strictly earlier bars only
    sel = np.flatnonzero(prior % _DAY_MS == bucket)
    if not len(sel):
        return out
    sel = sel[np.isfinite(v[sel])][-int(lookback_days):]
    if not len(sel):
        return out

    sample = v[sel]
    avg = float(np.mean(sample))
    out["samples"] = int(len(sample))
    out["average_volume"] = avg
    out["oldest_sample_utc_ms"] = int(t[sel[0]])
    out["warming"] = bool(len(sample) < lookback_days)
    # A zero baseline cannot be divided into.  Report the state rather than
    # emitting inf, which would rank first on any board that sorts by RVOL.
    out["rvol"] = float(cur / avg) if avg > 0 else None
    return out


def volume_profile(high, low, volume, bins=100, value_area=0.70):
    """Volume-at-price over the supplied slice.

    The slice IS the window -- this function has no opinion about which bars it
    was handed, so as-of correctness is the caller's to establish by slicing to
    the decision bar.  Returns POC/VAH/VAL plus the histogram.
    """
    h, l, v = _arr(high), _arr(low), _arr(volume)
    if len(h) == 0 or not np.isfinite(h).any():
        return {"poc": np.nan, "vah": np.nan, "val": np.nan,
                "edges": np.array([]), "hist": np.array([]),
                "approximation": APPROXIMATION}

    lo, hi = float(np.nanmin(l)), float(np.nanmax(h))
    if not np.isfinite(lo) or not np.isfinite(hi) or hi <= lo:
        return {"poc": lo if np.isfinite(lo) else np.nan, "vah": np.nan, "val": np.nan,
                "edges": np.array([]), "hist": np.array([]),
                "approximation": APPROXIMATION}

    edges = np.linspace(lo, hi, bins + 1)
    centers = (edges[:-1] + edges[1:]) / 2.0
    hist = np.zeros(bins)

    for i in range(len(h)):
        if not (np.isfinite(h[i]) and np.isfinite(l[i]) and np.isfinite(v[i])):
            continue
        if v[i] <= 0:
            continue
        a, b = min(l[i], h[i]), max(l[i], h[i])
        if b == a:
            hist[min(int((a - lo) / (hi - lo) * bins), bins - 1)] += v[i]
            continue
        overlap = np.clip(np.minimum(edges[1:], b) - np.maximum(edges[:-1], a), 0, None)
        tot = overlap.sum()
        if tot > 0:
            hist += v[i] * overlap / tot

    if hist.sum() <= 0:
        return {"poc": np.nan, "vah": np.nan, "val": np.nan,
                "edges": edges, "hist": hist, "approximation": APPROXIMATION}

    poc_i = int(np.argmax(hist))
    target = hist.sum() * value_area
    lo_i = hi_i = poc_i
    acc = hist[poc_i]
    while acc < target and (lo_i > 0 or hi_i < bins - 1):
        down = hist[lo_i - 1] if lo_i > 0 else -1.0
        up = hist[hi_i + 1] if hi_i < bins - 1 else -1.0
        if up >= down:
            hi_i += 1
            acc += hist[hi_i]
        else:
            lo_i -= 1
            acc += hist[lo_i]

    return {"poc": float(centers[poc_i]),
            "vah": float(centers[hi_i]),
            "val": float(centers[lo_i]),
            "edges": edges, "hist": hist,
            "approximation": APPROXIMATION}


def windowed_profile(open_time_ms, high, low, volume, window_days, as_of_ms,
                     bins=PROFILE_ROWS, value_area=VALUE_AREA,
                     substrate=None, min_bars=2):
    """A TRAILING windowed volume profile (§3.1, §3.3).

    Trailing, not anchored: the last N days as of `as_of_ms`, recomputed each
    capture, sliding forward with the clock.  THESE ARE NOT the parked
    judgment-merged composites of D-B12 -- a composite encodes a decision about
    which balance areas belong together; a trailing window encodes a clock.

    Window membership matches the RVWAP convention in `vwap.rolling_vwap` so the
    two layers describe the same span: bar_open_time > as_of_ms - W, and bars
    after `as_of_ms` are excluded outright.  Sharing the convention is the point
    -- a 30d VWAP and a 30d profile disagreeing about which bars are "the last
    30 days" would be an invisible and permanent source of level drift.

    `substrate` is carried through untouched and returned, because §3.3 requires
    the substrate ACTUALLY USED to be printed in every capture.  It is not used
    in any computation; passing it here is what stops the printed provenance and
    the real one from drifting apart.

    Returns the volume_profile dict plus window provenance, with `warming=True`
    and NO numbers when the supplied data does not span the window -- a 365d
    profile computed on 200 days is a 200-day profile wearing the wrong label
    (§3.2).
    """
    t = np.asarray(open_time_ms, dtype="int64")
    h, l, v = _arr(high), _arr(low), _arr(volume)
    W = int(round(float(window_days) * 86_400_000))
    as_of = int(as_of_ms)
    start = as_of - W

    from analytics import lockbox_overlap          # disclosure, not enforcement

    prov = {"window_days": float(window_days), "window_start_ms": start,
            "as_of_ms": as_of, "bins": int(bins), "value_area": float(value_area),
            "substrate": substrate, "approximation": APPROXIMATION,
            "lockbox_overlap": lockbox_overlap(start, as_of)}

    sel = (t > start) & (t <= as_of)
    n_sel = int(np.count_nonzero(sel))

    # Warm-up honesty (§3.2), and it is not optional: the check is whether the
    # DATA reaches back to the window start, not whether enough bars were
    # selected.  An asset listed inside the window has plenty of bars and still
    # cannot honestly claim the window.
    covered = bool(t.size) and int(t[0]) <= start
    if not covered or n_sel < min_bars:
        return {"poc": np.nan, "vah": np.nan, "val": np.nan,
                "edges": np.array([]), "hist": np.array([]),
                "lvns": [], "warming": True, "bars": n_sel,
                "history_start_ms": int(t[0]) if t.size else None, **prov}

    vp = volume_profile(h[sel], l[sel], v[sel], bins=bins, value_area=value_area)
    vp["lvns"] = low_volume_nodes(vp["edges"], vp["hist"])
    vp["warming"] = False
    vp["bars"] = n_sel
    vp["history_start_ms"] = int(t[0])
    vp.update(prov)
    return vp


def low_volume_nodes(edges, hist, threshold=LVN_THRESHOLD, min_rows=LVN_MIN_ROWS):
    """Low-volume nodes: near-empty shelves INSIDE the traded range (§3.4).

    A contiguous run of profile rows whose volume is below `threshold` x the
    window's MEDIAN row volume, at least `min_rows` wide, lying inside the
    window's traded range -- not at its extremes.  Each node emits its midpoint
    as a level and its edges as a band.

    WHY THE MEDIAN AND NOT THE MEAN.  A volume profile is strongly peaked at the
    POC; the mean is dragged up by that peak, so a mean-relative threshold would
    classify ordinary rows as "low volume" on any well-formed profile.  The
    median is the typical row, which is what "near-empty" is meant to be
    relative to.

    WHY INTERIOR ONLY.  The rows at a window's extremes are always thin -- price
    visited them briefly by construction.  Calling those LVNs would emit two
    guaranteed levels per window per asset that carry no information, and with
    five windows that is ten manufactured levels inflating every score.  A run
    touching either end of the histogram is therefore discarded, which is also
    why an all-empty profile yields nothing rather than one enormous node.

    This is the mechanical equivalent of the "single print from April 13th"
    class of level the operator's manual reviews lean on.  TPO single prints and
    judgment-composites remain parked.
    """
    e = _arr(edges)
    v = _arr(hist)
    out = []
    if v.size == 0 or e.size != v.size + 1:
        return out
    live = v[np.isfinite(v)]
    if live.size == 0:
        return out
    med = float(np.median(live))
    if not np.isfinite(med) or med <= 0:
        return out

    cut = threshold * med
    thin = np.isfinite(v) & (v < cut)
    n = len(v)
    i = 0
    while i < n:
        if not thin[i]:
            i += 1
            continue
        j = i
        while j + 1 < n and thin[j + 1]:
            j += 1
        # interior only -- a run touching either extreme is discarded
        if i > 0 and j < n - 1 and (j - i + 1) >= min_rows:
            lo, hi = float(e[i]), float(e[j + 1])
            out.append({"low": lo, "high": hi, "mid": (lo + hi) / 2.0,
                        "rows": int(j - i + 1),
                        "row_volume_median": med,
                        "threshold_volume": float(cut),
                        "approximation": APPROXIMATION})
        i = j + 1
    return out


def naked_poc_registry(period_pocs, high, low, as_of_index):
    """POCs not yet revisited by price as of `as_of_index`.

    "Untested" is a statement about the FUTURE of a level, so it is only
    well-defined relative to a decision bar.  Testing is evaluated strictly over
    bars (poc_index, as_of_index] -- never beyond -- which is what keeps this
    usable in an as-of historical walk rather than only live.
    """
    h, l = _arr(high), _arr(low)
    out = []
    for poc_index, level in period_pocs:
        if poc_index > as_of_index:
            continue
        seg_h = h[poc_index + 1:as_of_index + 1]
        seg_l = l[poc_index + 1:as_of_index + 1]
        touched = bool(np.any((seg_l <= level) & (seg_h >= level))) if len(seg_h) else False
        if not touched:
            out.append({"index": int(poc_index), "level": float(level),
                        "naked": True, "approximation": APPROXIMATION})
    return out
