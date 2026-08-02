"""Volume profile and the naked-POC registry.

APPROXIMATION, declared not hidden: volume-at-price is built by spreading each
bar's volume uniformly across its high-low range.  Real tick data would move
POC/VAH/VAL somewhat.  Every consumer must carry an `approximation` provenance
chip -- §II.10 G10 keeps those chips on the profile layers.
"""

import numpy as np

__all__ = ["volume_profile", "naked_poc_registry", "APPROXIMATION"]

APPROXIMATION = "volume spread uniformly across each bar's range (not tick data)"


def _arr(x):
    return np.asarray(x, dtype=float)


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
