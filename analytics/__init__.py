"""analytics -- Naiad's versioned, pure-computation toolbox.

Deliberately OUTSIDE `engine/`.  Engine files are frozen and hash-cited; ops
iteration must never share a blast radius with them.  Nothing here imports
engine, touches the network, or reads market data.

WHY A SHARED TOOLBOX.  The brief reads these numbers every morning.  A bug
hides comfortably inside a batch aggregate; it does not survive a week of a
human looking at the same number and saying "that's wrong."  Daily use is the
stress test that earns the right to point these functions at study data later.

VERSIONING (I-F).  Any change to a returned NUMBER bumps at least the minor
version.  Archive comparability depends on it: a capture from last week and one
from today are only comparable if the recipe that produced them is identifiable.

A NOTE ON `analytics_sha` AND THE NO-I/O INVARIANT.  I-A forbids I/O and F-AN-4
scans the sources for `open(`.  F-AN-5 nevertheless requires `analytics_sha()`
to hash the package's own sources.  These are reconciled deliberately, not
accidentally: the self-hash is a PROVENANCE function, not a computation
function, and it uses `pathlib.Path.read_bytes()` rather than the builtin.  No
function that returns a number reads anything.
"""

import hashlib
from pathlib import Path

# 1.1.0 -- Amendment FAN8 (2026-08-02): resample_ohlcv drops the unclosed
# bucket.  Returned NUMBERS change on every resampled layer, and I-F requires at
# least a minor bump whenever that happens, precisely so an archived capture can
# be told apart from a current one.
#
# 1.2.0 -- Amendment 2 §1.2 as extended (2026-08-03).  resample_ohlcv now RAISES
# on an undecidable source step, and emits only buckets PROVED closed by a bar in
# a strictly later bucket.  MEASURED ON THE ESTATE, NO PUBLISHED NUMBER MOVES:
# 1h->4h and 1h->1d across all ten assets give identical bucket counts, because
# live data always carries a forming final bucket that both rules drop.  The
# minor bump is taken anyway -- the CONTRACT changed and a returned number CAN
# change (a series ending exactly on a period boundary now drops that period),
# and I-F is about identifying the recipe, not about whether today's data happens
# to exercise the difference.
ANALYTICS_VERSION = "1.2.0"

_PKG = Path(__file__).resolve().parent
_MODULES = ("__init__.py", "momentum.py", "vwap.py", "volatility.py",
            "profile.py", "structure.py", "levels.py", "stats.py", "parity.py")


def analytics_sha() -> str:
    """sha256 over the package sources, in a fixed order, binary reads.

    Printed by every artifact that consumes this toolbox, beside
    ANALYTICS_VERSION, so a stored capture can always name the exact code that
    produced its numbers.
    """
    h = hashlib.sha256()
    for name in _MODULES:
        p = _PKG / name
        if p.exists():
            h.update(name.encode("utf-8"))
            h.update(p.read_bytes())
    return h.hexdigest()


# --------------------------------------------------------------------------
# CONVENTIONS -- the exact variant of every recipe AND its causality class.
#
#   causal        output at i depends only on input [0..i]        (F-AN-13)
#   lag:N         output at i is knowable only at i+N             (F-AN-13 at lag)
#   endpoint_only valid only at the end of the supplied array;
#                 MUST raise if asked for a mid-array value       (exempt)
# --------------------------------------------------------------------------

CONVENTIONS = {
    # momentum
    "sma": {"recipe": "simple moving average", "causality": "causal",
            "warmup": "length-1"},
    "ema": {"recipe": "alpha=2/(length+1), seeded with SMA(length) at index length-1",
            "causality": "causal", "warmup": "length-1"},
    "rma": {"recipe": "Wilder smoothing, alpha=1/length, seeded with mean(first length)",
            "causality": "causal", "warmup": "length-1"},
    "rsi": {"recipe": "length 14, Wilder/RMA smoothing, source close",
            "causality": "causal", "warmup": "length"},
    "stoch_rsi": {"recipe": "RSI 14, Stoch 14, %K smooth 3, %D smooth 3, source close",
                  "causality": "causal", "warmup": "rsi + stoch + k + d - 3"},
    "macd": {"recipe": "EMA(12)-EMA(26), signal EMA(9), hist = MACD - signal, source close",
             "causality": "causal", "warmup": "slow-1, signal defined slow+signal-2"},
    "awesome_oscillator": {"recipe": "SMA(5)-SMA(34) of bar midpoint (H+L)/2",
                           "causality": "causal", "warmup": "slow-1"},
    "divergences": {"recipe": "pivots(5,5) on price and oscillator; last 2 pivot pairs; "
                              "regular = price extreme extends while oscillator does not; "
                              "hidden = the converse; pivot_kind selects which",
                    "causality": "lag:5", "warmup": "n/a (pivot driven)"},
    # vwap
    "rolling_vwap": {"recipe": "TradingView RVWAP: trailing W-millisecond window floored at "
                               "10 bars, src hlc3, volume-weighted POPULATION variance via "
                               "one-pass max(E[x^2]-E[x]^2, 0), no (n-1) correction",
                     "causality": "causal", "warmup": "first bar with volume"},
    "anchored_vwap": {"recipe": "accumulated from the anchor bar, src hlc3, same variance "
                                "definition (INFERRED from shared band machinery, not read "
                                "from source -- flagged in the parity worksheet)",
                      "causality": "causal", "warmup": "anchor index"},
    "vw_sigma_bands": {"recipe": "vwap +/- k*stdev, k in {1,2,3}",
                       "causality": "causal", "warmup": "inherits"},
    # volatility
    "true_range": {"recipe": "max(H-L, abs(H-C_prev), abs(L-C_prev)); index 0 = H-L",
                   "causality": "causal", "warmup": "0"},
    "atr": {"recipe": "length 14, Wilder smoothing of true range",
            "causality": "causal", "warmup": "length-1"},
    "realised_vol": {"recipe": "close-to-close log returns, population sd, 7d vs 30d ratio, "
                               "NOT annualised",
                     "causality": "causal", "warmup": "slow"},
    "percentile_rank": {"recipe": "rank among trailing sample, 0-100, sample size returned",
                        "causality": "endpoint_only",
                        "warmup": "n/a -- raises if as_of_index is not the sample end"},
    # profile
    "volume_profile": {"recipe": "volume spread uniformly across each bar's range, "
                                 "POC/VAH/VAL at 70% value area (APPROXIMATION)",
                       "causality": "endpoint_only",
                       "warmup": "n/a -- describes the slice it is handed"},
    "naked_poc_registry": {"recipe": "POCs untested over (poc_index, as_of_index]",
                           "causality": "causal", "warmup": "n/a"},
    # structure
    "pivots": {"recipe": "pivot(5,5), strict extreme, unique within the window",
               "causality": "lag:5", "warmup": "left"},
    "confirmed_pivots": {"recipe": "pivots filtered to confirmation_lag <= as_of_index",
                         "causality": "causal", "warmup": "left+right"},
    "period_opens": {"recipe": "opening price of each D/W/M/Q/Y bucket, fixed at its first bar",
                     "causality": "causal", "warmup": "0"},
    "prior_period_extremes": {"recipe": "high/low of the previous COMPLETED period",
                              "causality": "causal", "warmup": "one full period"},
    "resample_ohlcv": {"recipe": "key = open_time // step * step, then "
                                 "first/max/min/last/sum; only buckets PROVED "
                                 "closed by a bar in a strictly later bucket are "
                                 "emitted, so the FINAL bucket is always dropped "
                                 "(Amendment FAN8 2026-08-02, extended by "
                                 "Amendment 2 §1.2 2026-08-03) -- the last row is "
                                 "the last FINISHED period, never the forming "
                                 "one; RAISES UndecidableStepError when the "
                                 "source spacing cannot be inferred at all",
                       "causality": "causal", "warmup": "0",
                       "raises": "UndecidableStepError on undecidable source step",
                       "precondition": "none -- closure is proved from the data, "
                                       "not inferred from median spacing, so "
                                       "safety no longer rests on the caller"},
    # stats
    "zscore": {"recipe": "rolling, population sd", "causality": "causal", "warmup": "length-1"},
    "correlation": {"recipe": "rolling Pearson", "causality": "causal", "warmup": "length-1"},
    "beta": {"recipe": "rolling cov/var against market", "causality": "causal",
             "warmup": "length-1"},
}

# Functions returning a series, which F-AN-13 must exercise.
SERIES_FUNCTIONS = (
    "sma", "ema", "rma", "rsi", "stoch_rsi", "macd", "awesome_oscillator",
    "true_range", "atr", "realised_vol", "rolling_vwap", "anchored_vwap",
    "zscore", "correlation", "beta", "period_opens", "prior_period_extremes",
)

__all__ = ["ANALYTICS_VERSION", "CONVENTIONS", "SERIES_FUNCTIONS", "analytics_sha"]
