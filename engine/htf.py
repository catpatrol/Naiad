"""Confirmed-HTF visibility mapping (build prompt §2 invariant 2).

The governor/MTF value visible to an exec bar is the value at the most recent
higher-timeframe bar whose CLOSE time is <= that exec bar's OPEN time. This
replicates Pine's `expr[1] + lookahead_on` idiom exactly, including the fact
that an HTF event flag (e.g. a governor cross) stays visible to every exec bar
of the following HTF period. No exceptions, including display/journal fields.
"""

import numpy as np

from engine.cells import INTERVAL_MS


def map_htf_to_exec(exec_open_ms: np.ndarray, htf_open_ms: np.ndarray,
                    htf_interval: str) -> np.ndarray:
    """Return, per exec bar, the index into the HTF arrays of the most recent
    HTF bar with close_time <= exec open_time; -1 where none exists yet.

    HTF close time = open_time + interval (exact boundary). An HTF bar whose
    close coincides with the exec bar's open IS visible (it just closed).
    """
    htf_close_ms = htf_open_ms + INTERVAL_MS[htf_interval]
    idx = np.searchsorted(htf_close_ms, exec_open_ms, side="right") - 1
    return idx


def take(series: np.ndarray, idx: np.ndarray, fill=np.nan) -> np.ndarray:
    """Gather `series[idx]` with -1 mapped to `fill`."""
    out = np.asarray(series, dtype=float)[np.clip(idx, 0, None)]
    out = out.copy()
    out[idx < 0] = fill
    return out


def take_bool(series: np.ndarray, idx: np.ndarray) -> np.ndarray:
    """Gather a boolean series; -1 maps to False."""
    out = np.asarray(series, dtype=bool)[np.clip(idx, 0, None)].copy()
    out[idx < 0] = False
    return out
