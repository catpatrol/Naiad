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
# 1.3.0 -- FINDING F-2R-A (2026-08-03).  `stoch_rsi` returned ALL NaN on every
# input: `sma` is cumsum-based, so the NaN prefix of the raw stochastic poisoned
# every later value.  StochRSI -- one of the four oscillators §6.1 commissions --
# had never produced a number, and 100% of its values in the 2026-08-03 capture
# were null.  F-AN-13 passed it because an all-NaN series satisfies the
# NaN-equals-NaN branch at every truncation point; F-AN-6b now asserts each
# series function is FINITE after warm-up, which is the property F-AN-13
# silently assumed.  Returned NUMBERS change, so I-F requires the bump.
#
# 1.4.0 -- OPERATOR RULINGS R1/R2/R4 (2026-08-05, ARGUS cycle 4 consolidated).
# The CONTRACT changed on three counts and NO PUBLISHED NUMBER MOVES, which is
# itself the finding:
#
#   R1/R2 -- the 1h substrate and the hlc3 source are now PINNED BY RULING for
#   rolling AND anchored VWAP.  They were already what the code did
#   (`daily_brief.vwap_series` A1.6(d), `brief2.rvwap_layer(tf="1h")`,
#   `brief2.prior_anchored_vwaps`), so this bump records a promotion from
#   implementation detail to ratified convention, not a recomputation.  The
#   distinction matters: an unpinned coincidence can drift, a pinned one cannot.
#
#   R4 -- the anchored variance definition moves INFERRED -> VERIFIED.  It was
#   flagged for four cycles as a reasoned inference from shared band machinery.
#   It is now read off a discriminating measurement rather than assumed.
#
# The 1.2.0 precedent governs: the minor bump is taken when the CONTRACT
# changes, because I-F is about identifying the recipe an archived capture was
# produced by, not about whether today's data happens to exercise a difference.
# 1.5.0 -- MATURITY FLOORS RULED (2026-08-06, cycle 6 item 1).  R3's interim
# 10/30 convention is replaced by the cycle-5 measurement: LINE 10 -> 16, BANDS
# 30 -> 60.  REGISTRY MEMBERSHIP CHANGES -- levels admitted under 10/30 are
# withheld under 16/60 -- so returned numbers move and I-F requires the bump.
# The reviewer's period-relative alternative was WITHDRAWN on evidence; see
# `vwap.FLOOR_BASIS` for the sqrt(t) argument that killed it.
ANALYTICS_VERSION = "1.5.0"

# --------------------------------------------------------------------------
# THE SEALED LOCKBOX -- disclosure, not enforcement.
#
# [2024-07-01, 2025-10-06) is the study holdout.  OPERATOR RULING 2026-08-03:
# the seal governs SCORED OUTCOME EVIDENCE -- replay journals, outcome
# statistics, anything the census may later grade -- and not raw price inside a
# display-only trailing indicator window.  The G-1 code guard sits on the replay
# path (LEDGER §220) and is untouched by anything here.
#
# The ruling was granted ON CONDITION that the overlap is DISCLOSED, so this is
# a disclosure utility and deliberately not a refusal: a brief that silently
# read across the holdout would be exactly what the condition forbids.
#
# It bites in one place only.  Measured 2026-08-03: of {7, 30, 90, 365}d, only
# the 365d window reaches back into the holdout, by 64 days, and that overlap
# self-clears on 2026-10-06.  7/30/90d are clear by construction and will stay
# clear.
# --------------------------------------------------------------------------

LOCKBOX_START_MS = 1_719_792_000_000        # 2024-07-01T00:00:00Z
LOCKBOX_END_MS = 1_759_708_800_000          # 2025-10-06T00:00:00Z, exclusive


def lockbox_overlap(start_ms, end_ms):
    """Disclosure record for a window spanning [start_ms, end_ms].

    Returned by every windowed layer and printed in every capture.  `days` is 0
    when the window is clear, which is the case that must stay boring.
    """
    lo = max(int(start_ms), LOCKBOX_START_MS)
    hi = min(int(end_ms), LOCKBOX_END_MS)
    ms = max(hi - lo, 0)
    return {"intersects": ms > 0,
            "overlap_ms": ms,
            "overlap_days": round(ms / 86_400_000, 3),
            "lockbox": [LOCKBOX_START_MS, LOCKBOX_END_MS],
            "basis": "operator ruling 2026-08-03: the seal governs scored "
                     "outcome evidence, not raw price in a display-only "
                     "trailing window; disclosed, never silent"}


_PKG = Path(__file__).resolve().parent
_MODULES = ("__init__.py", "momentum.py", "vwap.py", "volatility.py",
            "profile.py", "structure.py", "levels.py", "stats.py", "parity.py",
            "nesting.py")


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
    # vwap -- substrate and source PINNED BY OPERATOR RULING, see VWAP_SUBSTRATE
    # and VWAP_SOURCE below for the reasoning that is not compressible into a
    # recipe string.
    "rolling_vwap": {"recipe": "TradingView RVWAP: trailing W-millisecond window floored at "
                               "10 bars, src hlc3, volume-weighted POPULATION variance via "
                               "one-pass max(E[x^2]-E[x]^2, 0), no (n-1) correction",
                     "substrate": "1h (R1)", "source": "hlc3 (R2)",
                     "causality": "causal", "warmup": "first bar with volume",
                     "certification": "CERTIFIED -- 1D/hlc3 (2026-08-03, 14/14) and "
                                      "1h/hlc3 (2026-08-05, the ruled substrate)"},
    "anchored_vwap": {"recipe": "accumulated from the anchor bar, src hlc3, volume-weighted "
                                "POPULATION variance, one-pass, no (n-1) correction",
                      "substrate": "1h (R1)", "source": "hlc3 (R2)",
                      "causality": "causal", "warmup": "anchor index",
                      "variance_status": "VERIFIED (R4) -- was INFERRED for four cycles",
                      "variance_evidence":
                          "The 2026-08-01 Month anchor was TWO BARS wide, which is the "
                          "smallest sample that discriminates: population and sample "
                          "(n-1) forms differ by sqrt(n/(n-1)) = sqrt(2) = 41.4% there, "
                          "against a collapse tolerance of 0.02 ATR. The POPULATION form "
                          "landed within 0.003% of the operator's observed band-1 "
                          "distance; the sample form would have missed by 41%. The "
                          "definition is therefore READ OFF A MEASUREMENT that could only "
                          "come out one way, not inferred from shared band machinery. "
                          "True volume weights on the two bars: 0.394428 / 0.605572.",
                      "certification": "CERTIFIED on both substrates. 1D 14/14 "
                                       "(2026-08-03); 1h 42/42 (2026-08-06, two closed "
                                       "bars x W/M/Q x 7 levels, worst |delta| 0.0495)",
                      "maturity_floors": "line >= 16 bars, bands >= 60 bars (RULED "
                                         "2026-08-06); see vwap.FLOOR_BASIS",
                      "withdrawn_period_relative_floor":
                          "A period-relative floor (period/4) was proposed on the "
                          "grounds that a YOUNG SIGMA INFLATES THE SIGMA-LABEL and so "
                          "manufactures false reversion signals. THE REASONING IS WRONG "
                          "and the correction matters more than the ruling: anchored "
                          "sigma grows as sqrt(t), but price's DISPLACEMENT from the "
                          "anchored mean grows as sqrt(t) too -- both accumulate the "
                          "same walk from the same anchor -- so their RATIO, the "
                          "z-score, is approximately SCALE-FREE IN TIME. Measured on "
                          "the operator's captures, same asset, same Month anchor: at "
                          "29 bars sigma 313.3966 and z +2.0136; at 114 bars sigma "
                          "583.3876 and z +1.9389. Sigma grew 86.1%, the reading moved "
                          "3.7%. A young band's WIDTH is age-dependent; its READING is "
                          "not. The remaining floors are justified by SAMPLING NOISE "
                          "alone. CONSEQUENCE: band WIDTHS are comparable only at "
                          "comparable AGES, so every place widths appear together must "
                          "print each anchor's age in bars."},
    "vw_sigma_bands": {"recipe": "vwap +/- k*stdev, k in {1,2,3}",
                       "causality": "causal", "warmup": "inherits",
                       "certification": "GEOMETRY VERIFIED -- 36 triples across 3 captures, "
                                        "2 instruments, 2 timeframes; every triple exactly "
                                        "symmetric at exact integer multiples of sigma"},
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
    "relative_volume": {"recipe": "RVOL (B-7): bar volume / mean volume of the SAME "
                                  "time-of-day bucket over the trailing 20 days, "
                                  "current bar EXCLUDED from its own baseline; "
                                  "None rather than inf when the baseline is zero",
                        "causality": "causal",
                        "warmup": "warming until 20 same-bucket samples exist",
                        "why_time_of_day": "crypto volume has a hard diurnal shape; a "
                                           "flat 20-day mean would score every US-open "
                                           "bar high and every Asian bar low, which is a "
                                           "clock reading and not a market reading"},
    "low_volume_nodes": {"recipe": "contiguous runs of profile rows below "
                                   "lvn_threshold x the window's MEDIAN row "
                                   "volume, >= lvn_min_rows wide, INTERIOR only "
                                   "(a run touching either extreme is discarded); "
                                   "emits midpoint as a level and edges as a band "
                                   "(Amendment 2 §3.4)",
                         "causality": "endpoint_only",
                         "warmup": "n/a -- describes the histogram it is handed"},
    # nesting -- Amendment 2 §4
    "va_nesting": {"recipe": "per adjacent window pair: state in {nested_inside, "
                             "nested_outside, overlapping, disjoint_above, "
                             "disjoint_below}; overlap_frac = |intersection| / "
                             "|SHORTER VA|; consensus_band = [max(VAL), min(VAH)] "
                             "when they intersect; gap_band when disjoint, edges "
                             "flagged facing_edge",
                   "causality": "endpoint_only",
                   "warmup": "n/a -- describes the two value areas it is handed"},
    "price_location": {"recipe": "inside_consensus | inside_short_only | "
                                 "inside_long_only | in_gap | outside_all",
                       "causality": "endpoint_only", "warmup": "n/a"},
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
