"""TIER-C8 · STAGE N · AN-2 — OSCILLATOR COINCIDENCE.

TIER-E MEASUREMENT ONLY.  EVERY TABLE IN THIS MODULE GATES NOTHING, NO
REGISTRATION RESTS ON IT, AND NONE MAY BE IMPLIED.  Every row carries the
literal string "a SELECTION, not a result" in `selection_not_a_result`, its
table's `m_selections_this_table`, and the module's `m_an2_total_selections`.
A number here is a description of a cut of the book; it is not a claim that the
cut is a rule, and no cell of any grid in this file has been, or may be,
promoted.

────────────────────────────────────────────────────────────────────────────
THE PIVOT-PAIR RULE — PINNED, SO THE BUILD DOCUMENT CAN QUOTE IT VERBATIM
────────────────────────────────────────────────────────────────────────────
A divergence at as-of bar `j` on clock `X` is decided by exactly this rule and
by nothing else:

  1. PIVOTS ARE (2,2) FRACTALS ON THE CLOCK'S OWN BARS.  Bar `i` is a pivot HIGH
     iff `high[i]` is the STRICT and UNIQUE maximum of `high[i-2 : i+3]`; bar `i`
     is a pivot LOW iff `low[i]` is the strict and unique minimum of
     `low[i-2 : i+3]`.  This is `analytics.structure.pivots(..., left=2,
     right=2)`, the estate's own object, not a reimplementation.  A consequence
     used as a cardinality assertion in `an2_selfcheck`: two pivots on the same
     side can never be closer than 3 bars apart.

  2. THE CONFIRMATION LAG IS 2 BARS, AND IT BINDS.  A pivot at bar `i` is
     CONFIRMED at bar `i + 2` and is INVISIBLE before then.  A pivot confirmed at
     `j + 2` MAY NOT BE USED AT BAR `j`, and is not: the pivot set read at `j` is
     filtered to `confirmed_at <= j`, which is precisely
     `analytics.structure.confirmed_pivots(values, as_of_index=j, 2, 2, kind)`.
     `F-AN-2` leg 8 proves the filter is honest by RECOMPUTING every flag from
     arrays TRUNCATED at bar `j` and asserting the flag set is identical.

  3. THE LOOKBACK IS 60 BARS OF THAT CLOCK, AND IT IS PINNED, NOT SWEPT.  Only
     pivots with `pivot_index >= j - 60` are eligible.  On 1h that is 2.5 days,
     on 4h 10 days, on 12h 30 days.  60 is an ASSUMPTION, not a comparison: it
     was named before the look and no other value was tried, so no reader may
     read "60 won" out of this file, because nothing raced.

  4. THE PAIR IS THE TWO MOST RECENT ELIGIBLE PIVOTS ON THE SAME SIDE.  Call
     them `(i0, p0)` then `(i1, p1)` with `i0 < i1 <= j - 2`.  Both must lie
     inside the lookback.  If fewer than two eligible pivots exist on that side,
     THERE IS NO FLAG — which is recorded as `flag = "none"`, not dropped.

  5. THE OSCILLATOR IS READ AT THE PRICE PIVOT'S OWN BAR — `rsi[i0]`, `rsi[i1]` —
     AND THE RSI IS NOT SEPARATELY PIVOTED.  The alternative (pivot the RSI too,
     then pair its pivots with price's) is NOT taken, and the reason is stated
     rather than left to inference: two independently pivoted series produce
     pairs at DIFFERENT bars, so the comparison stops being "what did momentum do
     at the two moments price made this shape" and becomes a comparison of two
     unrelated moments.  This is also what `analytics.momentum.divergences`
     documents as its own intended use ("the oscillator's pivots at the same
     indices"), and that estate function is the flag engine here.

  6. THE FOUR CLASSES, IN FULL:
         on HIGHS   p1 > p0  and  rsi1 < rsi0   ->  REGULAR BEARISH
         on HIGHS   p1 < p0  and  rsi1 > rsi0   ->  HIDDEN  BEARISH
         on LOWS    p1 < p0  and  rsi1 > rsi0   ->  REGULAR BULLISH
         on LOWS    p1 > p0  and  rsi1 < rsi0   ->  HIDDEN  BULLISH
     Agreement (`price_up == rsi_up`) is not a divergence and emits nothing.

  7. TIES ARE NOT DIVERGENCES AND ARE COUNTED.  The comparisons are STRICT `>`,
     so `p1 == p0` or `rsi1 == rsi0` falls out as "no divergence" on one branch
     and could otherwise be silently classed.  `an2_selfcheck` counts every
     exactly-tied pair over the whole panel and PRINTS the count, so the reader
     sees the exposure instead of trusting that floats never repeat.

WHAT WOULD MAKE THIS RULE WRONG — the failure modes it is built against:
  · using a pivot before its confirmation bar (look-ahead; leg 8 refutes it);
  · reading RSI at the as-of bar instead of at the pivot bar (that measures
    "momentum now vs price then", which is not a divergence);
  · letting the pair straddle the lookback edge, so a 300-bar-old pivot pairs
    with a fresh one and the "divergence" is an artefact of the gap;
  · pivoting on CLOSE instead of HIGH/LOW (a different object; the shape a
    trader reads is the wick's);
  · a warm-up-seeded RSI, which would put a fabricated number at the older
    pivot of every early pair.

────────────────────────────────────────────────────────────────────────────
THE THREE CLOCKS, AND WHY THE 12h ONE IS RESAMPLED
────────────────────────────────────────────────────────────────────────────
RSI(14) is computed on 1h, 4h and 12h CLOSES, EACH ON ITS OWN CLOCK, and read
AS OF THE LAST BAR OF THAT CLOCK THAT HAD ALREADY CLOSED at the moment of the
campaign event.  The moment of a campaign event at 4h bar `i` is that bar's
CLOSE, `open_ms[i] + 4h` — not its open, because the card's decision is taken on
the close.  The as-of index is `searchsorted(bar_close_ms, event_close_ms,
"right") - 1`, so for the 4h clock it returns bar `i` itself; `F-AN-2` leg 7
asserts that identity over all 588 campaign events rather than on an example.

  1h   the cache's own `*_1h.parquet`, via `tierc2_baseline.load_klines` — the
       estate loader `tierc5._tf_frame` also uses.  It cannot be derived from 4h.
  4h   `tierc7.frame(sym)["f"]` — the DECISION frame itself, so the oscillator
       is read on exactly the bars the campaigns live on.
  12h  RESAMPLED FROM THE 4h DECISION FRAME through
       `analytics.structure.resample_ohlcv`, which drops the forming bucket
       unconditionally (AMENDMENT FAN8).  THIS IS A COMPUTE, AND HERE IS WHY:
       the cache's own `*_12h.parquet` ends 2026-08-15T00:00Z while the 4h
       corridor ends 2026-08-17T16:00Z, so the native file is FOUR WHOLE 12h
       BUCKETS STALE and every late campaign would silently read a two-and-a-half
       day old oscillator.  Resampling from 4h also guarantees the 12h clock is
       built from the same bars the book is, which the separate file does not.
       4h buckets 3-into-1 exactly (00/04/08 and 12/16/20 UTC), the 4h series is
       gapless on all five assets (asserted), and `an2_selfcheck` PRINTS the
       measured staleness of the native file so the choice is auditable rather
       than asserted.  Precedent: `tierc6_rules.wall_series_12h` builds its 12h
       clock from 4h bars for the same class of reason.

WARM-UP: `analytics.momentum.rsi` is NaN for exactly its first `length`
positions and never seeds.  That is NOT taken on trust.  `engine.indicators.ema`
SEEDS AT THE SERIES START AND NEVER RETURNS NaN — a defect this estate has
repaired FOUR times — so an EXPLICIT floor `idx >= RSI_LEN` is applied on top,
and `an2_selfcheck` asserts by CARDINALITY that the count of finite RSI values
before the floor is exactly ZERO on every (asset × clock) pair.  If anyone ever
swaps the momentum source for a seeding one, that assertion fails immediately.

────────────────────────────────────────────────────────────────────────────
WHAT IS MEASURED
────────────────────────────────────────────────────────────────────────────
(a) ENTRY      divergence PRESENT vs ABSENT at the ARMING bar and at the TRIGGER
               bar -> net R, win rate, reached-1R rate, per direction, with the
               D15 trio against the WHOLE BOOK.
(b) EXIT       divergence PRESENT vs ABSENT at the EXIT bar -> what the tape did
               over the next {6, 24, 100} 4h bars, in R of the campaign's own
               `r_dist`, signed by the campaign's direction.  THIS IS A
               COUNTERFACTUAL ABOUT A RULE THAT DID NOT FIRE.  The campaign
               exited; nobody held; no account earned or lost any part of these
               numbers.  It is what the tape did next, and it is reported as
               that and as nothing else.
(c) D15        `tierc7.d15(subset, whole_book)` on every aggregate row, printed,
               gating nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
import analytics as AN                                               # noqa: E402
from analytics import structure as AS                                # noqa: E402
from analytics import momentum as AM                                 # noqa: E402

iso, r4, r6, pct = TB.iso, TB.r4, TB.r6, TB.pct
log = TB.log
MS_1H, MS_4H = TB.MS_1H, TB.MS_4H
MS_12H = RC.MS_12H

SEED = 20260818

# ═══════════════════════════════════════════════════ THE PINNED CONSTANTS
# Every one of these was named BEFORE the look and NONE of them was swept.
# They are assumptions, not comparisons, and the tables say so in a column.
RSI_LEN = 14
CLOCKS = ("1h", "4h", "12h")
CLOCK_MS = {"1h": MS_1H, "4h": MS_4H, "12h": MS_12H}
PIVOT_L = 2
PIVOT_R = 2                       # == the confirmation lag, in bars
DIV_LOOKBACK_BARS = 60
WINDOW_BARS = 12                  # the +/- window, in the SAMPLING CLOCK's bars
FOLLOW_HORIZONS = (6, 24, 100)    # 4h bars, the campaign's own clock
EVENTS = ("arming", "trigger", "exit")
ENTRY_EVENTS = ("arming", "trigger")
FAMILIES = ("any", "regular", "hidden", "with_trade", "against_trade")
PRESENCE = ("present", "absent")
DIRECTIONS = ("long", "short", "both")
MIN_PIVOTS_FOR_PAIR = 2

# A divergence is only READ once the whole lookback window is itself warm, so
# that "the two most recent eligible pivots" can never quietly reach past a
# NaN-RSI pivot to an older one.  74 = 14 + 60.
DIV_MIN_ASOF_BAR = RSI_LEN + DIV_LOOKBACK_BARS

PINNED_NOT_SWEPT = (f"RSI_LEN={RSI_LEN}, pivot=({PIVOT_L},{PIVOT_R}), "
                    f"confirmation_lag={PIVOT_R} bars, "
                    f"lookback={DIV_LOOKBACK_BARS} bars of the clock, "
                    f"window=+/-{WINDOW_BARS} bars, "
                    f"horizons={FOLLOW_HORIZONS} 4h bars — ALL PINNED BEFORE "
                    f"THE LOOK AND NONE SWEPT; nothing raced, so nothing won")

# ═══════════════════════════════════════════════════ THE SELECTION SURFACE
M_ENTRY = len(ENTRY_EVENTS) * len(CLOCKS) * len(FAMILIES) * len(DIRECTIONS)
M_EXIT = len(CLOCKS) * len(FAMILIES) * len(DIRECTIONS) * len(FOLLOW_HORIZONS)
M_AN2_TOTAL = M_ENTRY + M_EXIT

GATES = ("NOTHING — TIER-E MEASUREMENT ONLY. No registration rests on this "
         "row, none is implied, and no cell of this grid may be promoted.")
SELECTION = "a SELECTION, not a result"


def _m_note(m_here: int, surface: str) -> str:
    """The m sentence carried on every row of every table.

    WHAT WOULD MAKE THIS WRONG: quoting a smaller m than the number of cuts
    actually taken (a reader who later promotes a cell needs the true count of
    looks, not the count of looks this table happens to print), or implying that
    an uncorrected m is acceptable because a correction was applied — none is,
    and none is needed, because nothing here is a test.
    """
    return (f"m = {m_here} SELECTIONS in this table; m = {M_AN2_TOTAL} across "
            f"AN-2 ({M_ENTRY} entry + {M_EXIT} exit). Surface: {surface}. NO "
            f"multiplicity correction is applied and none is needed, because "
            f"NOTHING HERE IS A TEST — there is no acceptance bar, no verdict "
            f"column and no registration downstream. m is logged so that a "
            f"reader who later wants to turn any of these cells into a claim "
            f"can see how many ways the book was cut first.")


def _tier_e(df: pd.DataFrame, m_here: int, surface: str) -> pd.DataFrame:
    """THE TIER-E COLLAR — the columns that make a table unusable as a gate.

    WHAT WOULD MAKE THIS WRONG: putting any of these in a caption instead of a
    column (a caption does not survive a copy of the row into a spreadsheet,
    which is the whole lesson of [TC6V-a]), or emitting a table from this module
    that has not been through it.
    """
    d = df.copy()
    d["selection_not_a_result"] = SELECTION
    d["m_selections_this_table"] = int(m_here)
    d["m_an2_total_selections"] = int(M_AN2_TOTAL)
    d["m_note"] = _m_note(m_here, surface)
    d["gates"] = GATES
    d["pinned_not_swept"] = PINNED_NOT_SWEPT
    d["tier"] = "TIER-E MEASUREMENT — UNSCORED, GATES NOTHING"
    d["in_sample"] = True
    return d


# ═══════════════════════════════════════════════════════════ THE CLOCKS
_CLOCK: dict[tuple[str, str], dict] = {}
_BOOK: dict[tuple[int, int], list] = {}
_META: dict = {}


def _meta(lo_ms: int, hi_ms: int) -> dict:
    """The corridor meta — BOUND to the corridor the caller actually asked for.

    THE WARRANTY MUST DESCRIBE THE BARS THE NUMBERS WERE BUILT FROM, AND THIS IS
    WHERE THAT CAN GO WRONG.  `T7.corridor()` takes no arguments and always
    returns the WHOLE corridor, but every table function in this module takes
    `(lo_ms, hi_ms)` and builds its book from THOSE.  Stamping the whole
    corridor's meta onto a narrowed book hands that table a warranty for bars it
    never saw — exactly the [TC6V-a] falsification the stamp exists to prevent,
    and silent, because the columns are all present and all look right.

    MEASURED BEFORE THIS GUARD, by the Stage-N self-check:
        entry_outcome(lo, lo + 30 days)  ->  180 rows over a ZERO-campaign book,
        stamped `as_of_last_closed_4h = 2026-08-17T16:00:00Z` and
        `as_of_span_days = 2535.0`.  Every number in it was true of 30 days and
        the row said 2535.
    The two keys `_lo_ms`/`_hi_ms` were already being stored here and never
    compared against anything; this completes that intent.

    A mismatch REFUSES rather than mis-stamps.  A narrowed corridor is not
    forbidden in principle — it is forbidden until someone writes the meta that
    honestly describes it, because there is no way to derive `panel_start`,
    `last_closed_4h_close` and `span_days` for an arbitrary window out of a
    function that only ever reports the whole one.

    WHAT WOULD MAKE THIS WRONG: caching it across a cache refresh, so a table
    built on new bars carries the old corridor's warranty. This module is
    single-run; a long-lived process would have to clear `_META`.
    """
    if not _META:
        lo, hi, m = T7.corridor()
        _META.update(m)
        _META["_lo_ms"], _META["_hi_ms"] = int(lo), int(hi)
    if (int(lo_ms), int(hi_ms)) != (_META["_lo_ms"], _META["_hi_ms"]):
        raise SystemExit(
            f"HALT: a table was requested for corridor [{int(lo_ms)}, "
            f"{int(hi_ms)}], but the only warranty this module can honestly "
            f"stamp is [{_META['_lo_ms']}, {_META['_hi_ms']}] "
            f"({_META['panel_start']} -> {_META['last_closed_4h_close']}, "
            f"{_META['span_days']} d). Stamping the whole corridor's as-of onto "
            f"a narrowed book is the [TC6V-a] falsification; refusing instead.")
    return _META


def _book(lo_ms: int, hi_ms: int) -> list:
    """THE WHOLE BOOK — card v6 control, the 196-campaign book of record.

    WHAT WOULD MAKE THIS WRONG: scoring AN-2 against a book that is not the one
    the estate calls the control, or rebuilding it per table so two tables in the
    same document could disagree about how many campaigns exist.
    """
    k = (int(lo_ms), int(hi_ms))
    if k not in _BOOK:
        _BOOK[k] = T7.run_cell(RC.CARD_V6_CONTROL, lo_ms, hi_ms)
    return _BOOK[k]


def clock(sym: str, tf: str) -> dict:
    """ONE ASSET ON ONE CLOCK: bars, bar-close stamps, floored RSI(14), pivots.

    The 4h clock IS the decision frame.  The 1h clock is the cache's own file.
    The 12h clock is resampled from the 4h decision frame — see the module
    docstring for the measured reason (the native 12h file is four buckets stale
    against the corridor).

    THE WARM-UP FLOOR IS APPLIED EXPLICITLY AND THEN ASSERTED.
    `analytics.momentum.rsi` already returns NaN for its first `RSI_LEN`
    positions, but `engine.indicators.ema` does NOT (it seeds at the series start
    and has been repaired four times in this estate for exactly that), so the
    floor is written down here rather than inherited by trust, and
    `an2_selfcheck` asserts the pre-floor finite count is ZERO by cardinality.

    WHAT WOULD MAKE THIS WRONG: stamping a bar by its OPEN and then treating that
    as the moment it is readable (that reads a bar from inside itself); building
    the 12h clock with the forming bucket kept, so the newest "12h bar" is a
    fraction of a period; or pivoting on CLOSE rather than HIGH/LOW.
    """
    key = (sym, tf)
    if key in _CLOCK:
        return _CLOCK[key]
    if tf == "4h":
        f = T7.frame(sym)["f"]
        t = np.asarray(f.open_ms, dtype=np.int64)
        h, l_, c = (np.asarray(f.h, float), np.asarray(f.l, float),
                    np.asarray(f.c, float))
        src = "tierc7.frame(sym)['f'] — the DECISION frame itself"
    elif tf == "1h":
        k1 = TB.load_klines(sym, "1h")
        t = k1["open_time"].to_numpy(np.int64)
        h = k1["high"].to_numpy(float)
        l_ = k1["low"].to_numpy(float)
        c = k1["close"].to_numpy(float)
        src = "cache *_1h.parquet via tierc2_baseline.load_klines"
    elif tf == "12h":
        f = T7.frame(sym)["f"]
        k4 = T7.frame(sym)["k4"]
        om4 = np.asarray(f.open_ms, np.int64)
        d = AS.resample_ohlcv(
            om4, k4["open"].to_numpy(float),
            np.asarray(f.h, float), np.asarray(f.l, float),
            np.asarray(f.c, float), k4["volume"].to_numpy(float), MS_12H)
        t = np.asarray(d["open_time"], np.int64)
        h, l_, c = (np.asarray(d["high"], float), np.asarray(d["low"], float),
                    np.asarray(d["close"], float))
        # ═══ THE HEAD BUCKET IS INCOMPLETE AND IS DROPPED. FOUND BY F-AN-2.
        #
        # `resample_ohlcv` drops the FORMING bucket at the tail (AMENDMENT
        # FAN8) and its docstring gives the reason in full: "a 1d 'bar' built
        # from a single 1h bar reads as a day". THE HEAD HAS THE SAME DEFECT
        # AND IS NOT COVERED, because a bucket at the head is not forming — it
        # is finished, and merely missing the slots that fall before the panel
        # starts. Measured on all five assets, every one of them:
        #     BTC   2019-09-08T12:00Z 12h bar built from 2 of its 3 4h bars
        #     ETH   2019-11-27T00:00Z                    2 of 3
        #     SOL   2020-09-14T00:00Z                    2 of 3
        #     NEAR  2020-10-15T00:00Z                    1 of 3
        #     ZEC   2020-02-05T00:00Z                    1 of 3
        # A 12h "bar" whose HIGH is the maximum of one 4h bar is a bar whose
        # range is understated by construction, and it is a legitimate pivot
        # candidate — so the defect is a fabricated extreme, not a cosmetic.
        #
        # THE FILTER IS COMPLETENESS, NOT POSITION: a bucket survives iff it
        # holds ALL THREE of its 4h slots. That is necessary and sufficient
        # for a closed 12h bar given gapless 4h data (asserted in F-AN-2 leg
        # 11b), it is symmetric between head and tail, and it is what the
        # fixture's independent arithmetic bucketing reproduces.
        #
        # NOT ruled by dropping index 0 unconditionally: an asset whose 4h
        # history happened to start on a 12h boundary would then lose a GOOD
        # bar, and the rule would be about position rather than about whether
        # the bar exists.
        uniq, ucnt = np.unique(om4 // MS_12H, return_counts=True)
        cmap = dict(zip(uniq.tolist(), ucnt.tolist()))
        cnt = np.array([cmap.get(int(b), 0) for b in (t // MS_12H)], dtype=int)
        full = cnt == 3
        if not full.any():
            raise SystemExit(f"HALT: {sym} has no complete 12h bucket")
        n_dropped_head = int(np.argmax(full))
        # AN INTERIOR HOLE IS REFUSED, NOT SILENTLY SKIPPED. Dropping an
        # incomplete bucket from the middle would shift every later index and
        # leave a clock that looks continuous and is not.
        if not full[n_dropped_head:].all():
            bad = int((~full[n_dropped_head:]).sum())
            raise SystemExit(
                f"HALT: {sym} has {bad} INTERIOR 12h bucket(s) missing a 4h "
                f"slot — the 4h series is not gapless and this clock cannot be "
                f"built by bucketing without inventing a bar")
        t, h, l_, c = (t[n_dropped_head:], h[n_dropped_head:],
                       l_[n_dropped_head:], c[n_dropped_head:])
        src = ("RESAMPLED 4h -> 12h via analytics.structure.resample_ohlcv "
               "(forming tail bucket dropped, AMENDMENT FAN8) THEN filtered to "
               f"buckets holding all three 4h slots ({n_dropped_head} partial "
               f"head bucket(s) dropped — see clock() for the finding)")
    else:
        raise SystemExit(f"HALT: unknown clock {tf!r}")

    step = CLOCK_MS[tf]
    rsi = AM.rsi(c, RSI_LEN)
    warm = np.arange(len(c)) >= RSI_LEN                    # THE EXPLICIT FLOOR
    rsi = np.where(warm, rsi, np.nan)
    piv = {}
    for side, series in (("high", h), ("low", l_)):
        i, lv, cf = AS.pivots(series, PIVOT_L, PIVOT_R, side)
        piv[side] = (np.asarray(i, np.int64), np.asarray(lv, float),
                     np.asarray(cf, np.int64))
    _CLOCK[key] = {"tf": tf, "sym": sym, "t": t, "close_ms": t + step,
                   "h": h, "l": l_, "c": c, "rsi": rsi, "piv": piv,
                   "step_ms": int(step), "n": len(c), "source": src}
    return _CLOCK[key]


def asof_index(sym: str, tf: str, event_close_ms: int) -> int:
    """The index of the last bar of `tf` that had CLOSED at `event_close_ms`.

    WHAT WOULD MAKE THIS WRONG: `side="left"`, which would admit a bar closing at
    exactly the event instant on the wrong side of the boundary; comparing OPEN
    stamps, which admits the bar the event is inside; or clipping a negative
    result to 0, which would publish bar 0 as "the last closed bar" for an event
    before the series starts instead of refusing.
    """
    cl = clock(sym, tf)
    k = int(np.searchsorted(cl["close_ms"], int(event_close_ms), "right")) - 1
    return k


# ═══════════════════════════════════════════════════ THE DIVERGENCE ENGINE
def divergences_at(sym: str, tf: str, j: int) -> list[dict]:
    """EVERY DIVERGENCE VISIBLE AT AS-OF BAR `j` ON CLOCK `tf`.

    The rule is the module docstring's, in full, and the flag engine is
    `analytics.momentum.divergences` with `max_pairs=1` — which pairs
    `usable[-2]` with `usable[-1]`, i.e. THE TWO MOST RECENT eligible pivots.

    `analytics.structure.confirmed_pivots` recomputes the whole pivot scan on
    every call, which is O(n) inside a loop that runs 588 x 3 times; the pivot
    scan is therefore CACHED once per (asset, clock, side) and the SAME
    `confirmed_at <= j` filter is applied here.  `an2_selfcheck` leg 6b asserts
    the hoisted filter returns byte-identical arrays to `confirmed_pivots` on a
    sample, so the optimisation cannot silently become a different rule.

    WHAT WOULD MAKE THIS WRONG: dropping the `conf <= j` filter (instant
    look-ahead); applying the lookback AFTER choosing the pair, so a pair could
    be chosen and then discarded leaving a stale older pair unexamined; or
    reading RSI at `j` instead of at the pivot bars.
    """
    cl = clock(sym, tf)
    out: list[dict] = []
    if j < DIV_MIN_ASOF_BAR or j >= cl["n"]:
        return out
    rsi = cl["rsi"]
    for side in ("high", "low"):
        pi, pl, pc = cl["piv"][side]
        keep = (pc <= j) & (pi >= j - DIV_LOOKBACK_BARS)
        i_k, l_k, c_k = pi[keep], pl[keep], pc[keep]
        if len(i_k) < MIN_PIVOTS_FOR_PAIR:
            continue
        ov = rsi[i_k]
        fin = np.isfinite(ov)
        if not fin.all():                    # cannot happen above DIV_MIN_ASOF_BAR
            i_k, l_k, c_k, ov = i_k[fin], l_k[fin], c_k[fin], ov[fin]
            if len(i_k) < MIN_PIVOTS_FOR_PAIR:
                continue
        conf_of = {int(a): int(b) for a, b in zip(i_k, c_k)}
        for kind in ("regular", "hidden"):
            for f in AM.divergences(i_k, l_k, i_k, ov, pivot_kind=side,
                                    kind=kind, max_pairs=1):
                f = dict(f)
                f["conf_from"] = conf_of[int(f["from_index"])]
                f["conf_to"] = conf_of[int(f["to_index"])]
                f["asof_index"] = int(j)
                f["clock"] = tf
                f["rsi_from"] = float(f.pop("osc_from"))
                f["rsi_to"] = float(f.pop("osc_to"))
                f["bars_between_pivots"] = int(f["to_index"] - f["from_index"])
                f["bars_since_pivot"] = int(j - f["to_index"])
                out.append(f)
    return out


def _agrees(div_direction: str, trade_direction: int) -> bool:
    """A bullish divergence agrees with a LONG; a bearish one with a SHORT.

    WHAT WOULD MAKE THIS WRONG: mapping agreement to the divergence's CLASS
    rather than its DIRECTION. A hidden bullish and a regular bullish are
    opposite readings of the tape but BOTH point up, and both therefore agree
    with a long — collapsing that into "regular agrees, hidden opposes" would
    silently relabel half the census.
    """
    return bool((trade_direction == 1 and div_direction == "bullish")
                or (trade_direction == -1 and div_direction == "bearish"))


def _families_of(flags: list[dict], trade_direction: int) -> dict[str, bool]:
    """Which of the five FAMILIES fire at one (campaign, event, clock) cell.

    WHAT WOULD MAKE THIS WRONG: making the families mutually exclusive.  They are
    OVERLAPPING BY DESIGN — a single regular-bullish flag on a long campaign sets
    `any`, `regular` and `with_trade` at once — which is exactly why the table's
    m counts each family as its own selection instead of pretending the five are
    one look.
    """
    agree = [f for f in flags if _agrees(f["direction"], trade_direction)]
    return {
        "any": bool(flags),
        "regular": any(f["kind"] == "regular" for f in flags),
        "hidden": any(f["kind"] == "hidden" for f in flags),
        "with_trade": bool(agree),
        "against_trade": bool([f for f in flags
                               if not _agrees(f["direction"], trade_direction)]),
    }


def _event_bars(t) -> list[tuple[str, int]]:
    """(event name, 4h bar index) for one campaign: arming, trigger, exit.

    ARMING AND TRIGGER COINCIDE ON 49 OF THE 196 CAMPAIGNS (`arm_i == entry_i`),
    and those campaigns therefore contribute the SAME sample twice — once to
    each event's rows. That is correct (both events happened on that bar) and it
    is why the two events are never pooled into one row.

    WHAT WOULD MAKE THIS WRONG: taking `arm_ms`/`entry_ms` and re-deriving the
    bar index by searching, which would drift from the index the replay actually
    used; or reading a chain's leg-2 entry as the trigger — the control card has
    no re-entry, and a card that did would need the leg named on the row.
    """
    return [("arming", int(t.arm_i)), ("trigger", int(t.entry_i)),
            ("exit", int(t.exit_i))]


# ═══════════════════════════════════════════════════════════ TABLE 1 · RSI
def rsi_panel(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """RSI(14) ON 1h / 4h / 12h AT EVERY CAMPAIGN'S ARMING, TRIGGER AND EXIT,
    PLUS +/-12 BARS OF THAT CLOCK AROUND EACH.

    One row per (campaign x event x clock x offset), offset in [-12, +12], so a
    complete cell is 25 rows and the panel is n_campaigns x 3 x 3 x 25.

    THE OFFSETS ARE IN THE SAMPLING CLOCK'S OWN BARS, not in 4h bars — "each on
    its own clock" is taken literally, so the 1h window is +/-12 hours and the
    12h window is +/-6 days.  The column `offset_clock_bars_of` names it on every
    row so the two can never be confused after a copy.

    POSITIVE OFFSETS ARE THE FUTURE AND ARE FLAGGED AS SUCH.  `offset_bars > 0`
    reads bars the campaign event could not see; the column
    `uses_bars_after_the_event` is True on exactly those rows.  They are here
    because this is a DESCRIPTIVE panel of what the oscillator did around the
    event, which is a legitimate Tier-E question — but they are not available at
    decision time and NOTHING in `entry_outcome` reads them: every entry
    classification is taken at `offset_bars == 0` and `an2_selfcheck` leg 9
    asserts the offset-0 RSI equals the as-of RSI on every cell.

    WHAT WOULD MAKE THIS WRONG: a warm-up-seeded RSI (a fabricated number would
    ride the whole panel); an as-of taken at the bar's OPEN, which would read a
    12h bar the event sits inside; an offset window measured in 4h bars while
    labelled as the clock's; or letting a positive offset leak into a
    classification.
    """
    book = _book(lo_ms, hi_ms)
    rows = []
    for t in book:
        f = T7.frame(t.symbol)["f"]
        for ev, bi in _event_bars(t):
            ev_open = int(f.open_ms[bi])
            ev_close = ev_open + MS_4H
            for tf in CLOCKS:
                cl = clock(t.symbol, tf)
                k = asof_index(t.symbol, tf, ev_close)
                for off in range(-WINDOW_BARS, WINDOW_BARS + 1):
                    b = k + off
                    ok = 0 <= b < cl["n"]
                    v = float(cl["rsi"][b]) if ok else float("nan")
                    rows.append({
                        "asset": t.symbol, "lane": t.lane,
                        "entry_ms": int(t.entry_ms),
                        "entry_ts": iso(int(t.entry_ms)),
                        "direction": int(t.direction),
                        "side": "long" if t.direction == 1 else "short",
                        "event": ev,
                        "event_bar_4h_index": int(bi),
                        "event_bar_4h_open_ts": iso(ev_open),
                        "event_decision_ts": iso(ev_close),
                        "clock": tf,
                        "asof_index": int(k),
                        "asof_bar_open_ts": (iso(int(cl["t"][k]))
                                             if 0 <= k < cl["n"] else None),
                        "asof_bar_close_ts": (iso(int(cl["close_ms"][k]))
                                              if 0 <= k < cl["n"] else None),
                        "offset_bars": int(off),
                        "offset_clock_bars_of": tf,
                        "bar_index": int(b),
                        "bar_open_ts": (iso(int(cl["t"][b])) if ok else None),
                        "in_series": bool(ok),
                        "rsi14": r4(v) if np.isfinite(v) else None,
                        "rsi_is_warm": bool(ok and b >= RSI_LEN
                                            and np.isfinite(v)),
                        "uses_bars_after_the_event": bool(off > 0),
                        "readable_at_decision_time": bool(off <= 0),
                        "clock_source": cl["source"],
                        "net_r": r6(t.net_r), "reached_1r": bool(t.reached_1r),
                        "exit_reason": t.exit_reason,
                    })
    d = pd.DataFrame(rows)
    d = _tier_e(d, len(CLOCKS) * len(EVENTS),
                "campaign x {arming,trigger,exit} x {1h,4h,12h} x offset "
                "[-12,+12] — a DESCRIPTIVE panel, no cell of which is a cut "
                "anything is scored on")
    return T8.stamp(d, _meta(lo_ms, hi_ms))


# ═══════════════════════════════════════════════════ TABLE 2 · THE FLAGS
def divergence_flags(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """EVERY DIVERGENCE — REGULAR AND HIDDEN — VISIBLE AT EVERY CAMPAIGN EVENT.

    A COMPLETE CENSUS, NOT A LIST OF HITS.  A (campaign, event, clock) cell where
    nothing fired emits a row with `flag_kind = "none"`, because absence is the
    denominator of every rate in `entry_outcome` and a table of hits alone cannot
    be counted against anything.

    The rule that decides each row is pinned in the module docstring and is
    quoted onto the row itself in `pivot_pair_rule`, so a copied row still
    carries its own definition.

    WHAT WOULD MAKE THIS WRONG: emitting only the fired rows (the rates lose
    their denominator); an `asof_index` that is not the last CLOSED bar of the
    clock; or a flag whose pivot confirmation index exceeds its as-of bar —
    `an2_selfcheck` leg 6 asserts that count is ZERO over the whole census, not
    on an example.
    """
    book = _book(lo_ms, hi_ms)
    rule = ("(2,2) price pivots on HIGH/LOW; confirmation lag 2 bars, "
            f"confirmed_at <= asof; lookback {DIV_LOOKBACK_BARS} bars of the "
            "clock; the TWO MOST RECENT eligible pivots on one side; RSI(14) "
            "read AT THOSE SAME BARS; regular bearish = higher price high with "
            "lower RSI high, hidden bullish = higher price low with lower RSI "
            "low, and the mirrors")
    rows = []
    for t in book:
        f = T7.frame(t.symbol)["f"]
        for ev, bi in _event_bars(t):
            ev_close = int(f.open_ms[bi]) + MS_4H
            for tf in CLOCKS:
                cl = clock(t.symbol, tf)
                k = asof_index(t.symbol, tf, ev_close)
                flags = divergences_at(t.symbol, tf, k)
                base = {
                    "asset": t.symbol, "entry_ms": int(t.entry_ms),
                    "entry_ts": iso(int(t.entry_ms)),
                    "direction": int(t.direction),
                    "side": "long" if t.direction == 1 else "short",
                    "event": ev, "event_bar_4h_index": int(bi),
                    "event_decision_ts": iso(ev_close),
                    "clock": tf, "asof_index": int(k),
                    "asof_bar_close_ts": (iso(int(cl["close_ms"][k]))
                                          if 0 <= k < cl["n"] else None),
                    "readable": bool(k >= DIV_MIN_ASOF_BAR),
                    "lookback_bars": DIV_LOOKBACK_BARS,
                    "confirmation_lag_bars": PIVOT_R,
                    "pivot_pair_rule": rule,
                    "net_r": r6(t.net_r), "reached_1r": bool(t.reached_1r),
                    "exit_reason": t.exit_reason,
                    "n_flags_at_this_cell": len(flags),
                }
                if not flags:
                    rows.append(base | {
                        "flag_kind": "none", "flag_pivot_side": None,
                        "flag_direction": None, "agrees_with_trade": None,
                        "from_index": None, "to_index": None,
                        "from_ts": None, "to_ts": None,
                        "conf_from": None, "conf_to": None,
                        "price_from": None, "price_to": None,
                        "rsi_from": None, "rsi_to": None,
                        "bars_between_pivots": None, "bars_since_pivot": None,
                        "price_leg_up": None, "rsi_leg_up": None})
                    continue
                for fl in flags:
                    rows.append(base | {
                        "flag_kind": fl["kind"],
                        "flag_pivot_side": fl["pivot_kind"],
                        "flag_direction": fl["direction"],
                        "agrees_with_trade": _agrees(fl["direction"],
                                                     t.direction),
                        "from_index": int(fl["from_index"]),
                        "to_index": int(fl["to_index"]),
                        "from_ts": iso(int(cl["t"][int(fl["from_index"])])),
                        "to_ts": iso(int(cl["t"][int(fl["to_index"])])),
                        "conf_from": int(fl["conf_from"]),
                        "conf_to": int(fl["conf_to"]),
                        "price_from": r6(fl["price_from"]),
                        "price_to": r6(fl["price_to"]),
                        "rsi_from": r4(fl["rsi_from"]),
                        "rsi_to": r4(fl["rsi_to"]),
                        "bars_between_pivots": int(fl["bars_between_pivots"]),
                        "bars_since_pivot": int(fl["bars_since_pivot"]),
                        "price_leg_up": bool(fl["price_to"] > fl["price_from"]),
                        "rsi_leg_up": bool(fl["rsi_to"] > fl["rsi_from"])})
    d = pd.DataFrame(rows)
    d = _tier_e(d, len(CLOCKS) * len(EVENTS),
                "campaign x {arming,trigger,exit} x {1h,4h,12h} — a CENSUS of "
                "the flag, including its absence")
    return T8.stamp(d, _meta(lo_ms, hi_ms))


# ═════════════════════════════════════════════════ THE CELL CLASSIFICATION
def _cells(book: list) -> dict:
    """(campaign, event, clock) -> the five family booleans.  Computed once.

    WHAT WOULD MAKE THIS WRONG: keying on (asset, entry_ms) alone, which would
    collide if two lanes ever entered the same asset on the same bar; or
    computing it per table, so `entry_outcome` and `exit_followthrough` could
    disagree about which campaigns carry a flag.
    """
    out = {}
    for t in book:
        f = T7.frame(t.symbol)["f"]
        for ev, bi in _event_bars(t):
            ev_close = int(f.open_ms[bi]) + MS_4H
            for tf in CLOCKS:
                k = asof_index(t.symbol, tf, ev_close)
                flags = divergences_at(t.symbol, tf, k)
                out[(t.symbol, int(t.entry_ms), ev, tf)] = _families_of(
                    flags, t.direction)
    return out


def _outcome_row(sub: list, book: list, extra: dict) -> dict:
    """ONE AGGREGATE ROW: outcome, the D15 trio, and an asset-cluster interval.

    `n` is always printed and anything under `RC.PROVISIONAL_MIN_N` carries
    `provisional=True` — the house line, applied here to descriptive rows too,
    because a 4-campaign cell reads exactly like a 90-campaign one once it is a
    row in a table.

    THE INTERVAL IS PRINTED AND IS NOT A TEST.  There is no bar to clear and no
    verdict column; it is here so a reader can see the width, and with FIVE
    asset clusters in the whole universe that width is large by construction.

    WHAT WOULD MAKE THIS WRONG: reporting an expectancy without n; treating the
    interval's exclusion of zero as a verdict; or pairing D15 against the SUBSET
    instead of the whole book, which would compare the cut to itself.
    """
    rs = [t.net_r for t in sub]
    row = dict(extra)
    row["n"] = len(sub)
    row["n_assets"] = len(set(t.symbol for t in sub))
    row["net_r"] = r4(sum(rs)) if rs else None
    row["expectancy_r"] = r6(float(np.mean(rs))) if rs else None
    row["median_r"] = r6(float(np.median(rs))) if rs else None
    row["win_rate_pct"] = pct(sum(1 for v in rs if v > 0), len(rs)) if rs else None
    row["reached_1r_pct"] = (pct(sum(1 for t in sub if t.reached_1r), len(sub))
                             if sub else None)
    row["best_r"] = r4(max(rs)) if rs else None
    row["worst_r"] = r4(min(rs)) if rs else None
    row["provisional"] = bool(len(sub) < RC.PROVISIONAL_MIN_N)
    row["provisional_note"] = (
        f"n < {RC.PROVISIONAL_MIN_N}" if len(sub) < RC.PROVISIONAL_MIN_N else "")
    if len(rs) >= 2 and len(set(t.symbol for t in sub)) >= 2:
        ci = T7._ci_from(T7.cluster_boot(rs, [t.symbol for t in sub]),
                         float(np.mean(rs)))
        row["ci_lo_expectancy_r"] = r6(ci["lo"])
        row["ci_hi_expectancy_r"] = r6(ci["hi"])
    else:
        row["ci_lo_expectancy_r"] = None
        row["ci_hi_expectancy_r"] = None
    row["ci_note"] = ("asset-cluster 90% interval on the cell's own expectancy, "
                      "PRINTED not tested; 5 clusters is the entire universe so "
                      "the interval is wide by construction")
    row.update(T7.d15(sub, book))
    row["d15_note"] = ("the D15 trio — paired_delta_expectancy_r, "
                       "tail_exit_ratio, max_single_trade_delta_share — taken "
                       "against the WHOLE 196-campaign book. Diagnostics, "
                       "printed, gating nothing.")
    # ═══ TWO THIRDS OF THE D15 TRIO ARE DEGENERATE HERE, AND SAYING SO IS THE
    # ═══ POINT OF PRINTING THEM AT ALL.
    #
    # D15 was built to score an ARM against a CONTROL over the same campaigns:
    # the same trade, ridden by a different rule, differenced. AN-2's cells are
    # not arms. They are SUBSETS of the control book — the same campaigns,
    # ridden by the same card, merely selected. So the per-campaign delta is
    # EXACTLY ZERO for every campaign in every cell, `paired_delta_expectancy_r`
    # is 0.0 by construction and not by measurement, and
    # `max_single_trade_delta_share` is None because its denominator is zero.
    #
    # They are kept because the commission asks for the trio on every aggregate
    # row and because a silently missing column invites the reader to assume it
    # was inconvenient. But a 0.0 that means "identical by construction" reads
    # exactly like a 0.0 that means "no effect was found", so the honest
    # analogues are printed beside them:
    #
    #   subset_minus_book_expectancy_r   the cell's expectancy minus the whole
    #                                    book's. UNPAIRED, and labelled so —
    #                                    the cell is a sub-population, not a
    #                                    re-ride, and no pairing can exist.
    #   max_single_campaign_share        the D15 concentration question asked of
    #                                    the quantity that actually varies here:
    #                                    the largest |net_r| in the cell over
    #                                    |sum net_r| in the cell. Near 1.0 means
    #                                    ONE CAMPAIGN IS THE CELL. IT CAN EXCEED
    #                                    1.0, and that is the signal at its
    #                                    loudest rather than a bug: when winners
    #                                    and losers nearly cancel, the cell's
    #                                    whole net is SMALLER than one of its
    #                                    campaigns, and its expectancy is a
    #                                    statement about that one campaign.
    #
    # `tail_exit_ratio` is the one member of the trio that is NOT degenerate: it
    # compares the cell's top-decile winning mass to the book's and answers a
    # real question about the cut.
    row["d15_degenerate_by_construction"] = (
        "paired_delta_expectancy_r is 0.0 and max_single_trade_delta_share is "
        "None BY CONSTRUCTION, not by measurement: an AN-2 cell is a SUBSET of "
        "the control book, not an arm ridden through it, so every paired delta "
        "is identically zero. tail_exit_ratio is the member of the trio that "
        "still measures something. Read subset_minus_book_expectancy_r and "
        "max_single_campaign_share instead.")
    book_rs = [t.net_r for t in book]
    row["book_expectancy_r"] = r6(float(np.mean(book_rs)))
    row["subset_minus_book_expectancy_r"] = (
        r6(float(np.mean(rs)) - float(np.mean(book_rs))) if rs else None)
    row["subset_minus_book_is_unpaired"] = True
    row["max_single_campaign_share"] = (
        r4(max(abs(v) for v in rs) / abs(sum(rs)))
        if rs and abs(sum(rs)) > 1e-12 else None)
    return row


# ═══════════════════════════════════════════════════ TABLE 3 · (a) ENTRY
def entry_outcome(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """(a) DIVERGENCE PRESENT vs ABSENT AT THE ARMING / TRIGGER -> OUTCOME.

    Rows: {arming, trigger} x {1h,4h,12h} x {any, regular, hidden, with_trade,
    against_trade} x {present, absent} x {long, short, both}.  Present and absent
    partition the book on every (event, clock, family, direction) line, so the
    two n's on a line sum to that direction's whole-book n — asserted in
    `an2_selfcheck` leg 12 by cardinality rather than eyeballed.

    THE CLASSIFICATION IS TAKEN AT OFFSET 0 — the last bar of the clock that had
    closed when the card made its decision — so every cut here is one a rule
    COULD have taken.  That does not make any of them a rule, and none is
    proposed.  The families OVERLAP by construction (a regular bullish flag on a
    long sets `any`, `regular` and `with_trade`), which is why m counts 90
    selections here and not 6.

    WHAT WOULD MAKE THIS WRONG: classifying on a bar the event could not see;
    letting the present/absent split lose campaigns (a cell where the clock's
    as-of index is below DIV_MIN_ASOF_BAR must still land in `absent`, and it
    does — no divergence was readable, so none was present); or reading these
    numbers as an entry filter, which this module forbids in a column.
    """
    book = _book(lo_ms, hi_ms)
    cells = _cells(book)
    rows = []
    for ev in ENTRY_EVENTS:
        for tf in CLOCKS:
            for fam in FAMILIES:
                for dl in DIRECTIONS:
                    pool = [t for t in book
                            if dl == "both"
                            or (dl == "long" and t.direction == 1)
                            or (dl == "short" and t.direction == -1)]
                    for pres in PRESENCE:
                        want = (pres == "present")
                        sub = [t for t in pool
                               if cells[(t.symbol, int(t.entry_ms), ev,
                                         tf)][fam] is want]
                        rows.append(_outcome_row(sub, book, {
                            "measure": "(a) ENTRY",
                            "event": ev, "clock": tf, "family": fam,
                            "presence": pres, "direction_group": dl,
                            "classified_at": "offset 0 — the last bar of this "
                                             "clock closed at the event's "
                                             "decision instant",
                            "counterfactual": False,
                            "pool_n": len(pool)}))
    d = pd.DataFrame(rows)
    d = _tier_e(d, M_ENTRY,
                "{arming,trigger} x {1h,4h,12h} x {any,regular,hidden,"
                "with_trade,against_trade} x {long,short,both}")
    return T8.stamp(d, _meta(lo_ms, hi_ms))


# ═══════════════════════════════════════════════ TABLE 4 · (b) EXIT
def _followthrough(t, h: int) -> dict:
    """WHAT THE TAPE DID FOR `h` 4h BARS AFTER ONE CAMPAIGN'S EXIT, IN ITS R.

    Signed by the campaign's own direction, so POSITIVE means the trade's
    direction kept going after the exit — i.e. the exit left money on the table —
    and negative means the exit was ahead of a reversal.  The unit is the
    campaign's own `r_dist`, the same R its `net_r` is in.

    CENSORING IS REPORTED, NOT IMPUTED.  A campaign whose exit sits within `h`
    bars of the corridor edge has no `h`-bar future in the cache; it returns
    `censored=True` and is EXCLUDED from that horizon's mean and COUNTED on the
    row.  Filling it with the shortest available window would mix horizons.

    A HORIZON BELOW ONE BAR IS REFUSED, NOT ANSWERED.  Found by the Stage-N
    self-check: `h <= 0` makes `[exit_i + 1, exit_i + h]` an EMPTY slice, and
    `np.max` on a zero-size array raises `ValueError: zero-size array to
    reduction operation maximum which has no identity` — an opaque numpy error
    from three frames down, where this module's own refusal belongs.  It must
    NOT be answered with `censored=True`: censoring is a COUNTED quantity
    (F-AN-2 leg 14) that means "the corridor ran out before the window closed",
    and folding a malformed horizon into that count would inflate a published
    number with a caller's typo.  `FOLLOW_HORIZONS` is (6, 24, 100), so no
    shipped row goes near this; the guard exists because the horizon is a free
    parameter and the next hand asking for a zero-bar baseline should be told
    why, not shown a traceback.

    WHAT WOULD MAKE THIS WRONG: measuring from a bar close instead of the actual
    exit FILL (a stop exit fills at the stop, not at that bar's close); counting
    bar `exit_i` itself, which the campaign already booked; dividing by anything
    other than the campaign's own R; or silently truncating a censored window and
    calling it an `h`-bar result.
    """
    if int(h) < 1:
        raise SystemExit(
            f"HALT: follow-through horizon must be at least 1 bar, got {h}. "
            f"A horizon of {h} slices an EMPTY window and is a malformed "
            f"question, not a censored campaign — see _followthrough().")
    f = T7.frame(t.symbol)["f"]
    n = len(f.c)
    d, R, px = int(t.direction), float(t.r_dist), float(t.exit_px)
    lo_j, hi_j = int(t.exit_i) + 1, int(t.exit_i) + h
    if hi_j > n - 1:
        return {"censored": True, "close_r": None, "mfe_r": None,
                "mae_r": None, "bars_available": max(0, n - 1 - int(t.exit_i))}
    seg_h = np.asarray(f.h[lo_j:hi_j + 1], float)
    seg_l = np.asarray(f.l[lo_j:hi_j + 1], float)
    fav = float(np.max(seg_h)) if d == 1 else float(np.min(seg_l))
    adv = float(np.min(seg_l)) if d == 1 else float(np.max(seg_h))
    return {"censored": False,
            "close_r": (float(f.c[hi_j]) - px) * d / R,
            "mfe_r": (fav - px) * d / R,
            "mae_r": (adv - px) * d / R,
            "bars_available": h}


def exit_followthrough(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """(b) DIVERGENCE PRESENT vs ABSENT AT THE EXIT -> WHAT THE TAPE DID NEXT.

    SAID PLAINLY, AND SAID IN A COLUMN: THIS IS A COUNTERFACTUAL ABOUT A RULE
    THAT DID NOT FIRE.  Every campaign in this table EXITED.  Nobody held.  No
    account earned or lost one cent of the follow-through R printed here.  These
    numbers describe what the tape did after the exit, and they would only become
    a P&L if some rule had held the position — no such rule exists, none is
    proposed, and turning any cell of this grid into one would be a fresh
    registration with its own prior and its own ruler, not a promotion of this
    row.  `counterfactual = True` is on every row for exactly that reason.

    Rows: {1h,4h,12h} x {5 families} x {long,short,both} x {6,24,100} bars, and
    present/absent are two columns on each so the pair sits side by side.

    THE HORIZON IS 4h BARS — THE CAMPAIGN'S OWN CLOCK — while the CLASSIFICATION
    is on the named clock.  Those are two different clocks in one row on purpose,
    and both are named in columns (`horizon_clock`, `clock`), because reading the
    100 as 100 twelve-hour bars would be a fifty-day claim instead of a
    sixteen-day one.

    WHAT WOULD MAKE THIS WRONG: presenting the follow-through as a return; using
    the whole book's R instead of each campaign's own; or averaging censored and
    uncensored windows together.
    """
    book = _book(lo_ms, hi_ms)
    cells = _cells(book)
    ft = {(t.symbol, int(t.entry_ms), h): _followthrough(t, h)
          for t in book for h in FOLLOW_HORIZONS}
    rows = []
    for tf in CLOCKS:
        for fam in FAMILIES:
            for dl in DIRECTIONS:
                pool = [t for t in book
                        if dl == "both"
                        or (dl == "long" and t.direction == 1)
                        or (dl == "short" and t.direction == -1)]
                for h in FOLLOW_HORIZONS:
                    for pres in PRESENCE:
                        want = (pres == "present")
                        sub = [t for t in pool
                               if cells[(t.symbol, int(t.entry_ms), "exit",
                                         tf)][fam] is want]
                        vals = [ft[(t.symbol, int(t.entry_ms), h)] for t in sub]
                        live = [v for v in vals if not v["censored"]]
                        cens = len(vals) - len(live)
                        cl_r = [v["close_r"] for v in live]
                        mf_r = [v["mfe_r"] for v in live]
                        ma_r = [v["mae_r"] for v in live]
                        row = _outcome_row(sub, book, {
                            "measure": "(b) EXIT FOLLOW-THROUGH",
                            "event": "exit", "clock": tf, "family": fam,
                            "presence": pres, "direction_group": dl,
                            "horizon_bars": h, "horizon_clock": "4h",
                            "counterfactual": True,
                            "counterfactual_note": (
                                "A COUNTERFACTUAL ABOUT A RULE THAT DID NOT "
                                "FIRE. The campaign exited; nobody held. No "
                                "account earned or lost any part of this "
                                "follow-through. It is what the tape did next "
                                "and it is nothing else."),
                            "pool_n": len(pool)})
                        row["n_followthrough"] = len(live)
                        row["n_censored_at_corridor_edge"] = cens
                        row["followthrough_close_r_mean"] = (
                            r6(float(np.mean(cl_r))) if cl_r else None)
                        row["followthrough_close_r_median"] = (
                            r6(float(np.median(cl_r))) if cl_r else None)
                        row["followthrough_mfe_r_mean"] = (
                            r6(float(np.mean(mf_r))) if mf_r else None)
                        row["followthrough_mae_r_mean"] = (
                            r6(float(np.mean(ma_r))) if ma_r else None)
                        row["followthrough_continued_pct"] = (
                            pct(sum(1 for v in cl_r if v > 0), len(cl_r))
                            if cl_r else None)
                        row["followthrough_sign_note"] = (
                            "POSITIVE = the trade's own direction kept going "
                            "after the exit (the exit left tape behind); "
                            "NEGATIVE = the tape turned against the trade's "
                            "direction after the exit.")
                        rows.append(row)
    d = pd.DataFrame(rows)
    d = _tier_e(d, M_EXIT,
                "{1h,4h,12h} x {any,regular,hidden,with_trade,against_trade} x "
                "{long,short,both} x {6,24,100} 4h bars")
    return T8.stamp(d, _meta(lo_ms, hi_ms))


# ═══════════════════════════════════════════════════ F-AN-2 · THE FIXTURE
def _hand_rsi(closes: np.ndarray, length: int = RSI_LEN) -> np.ndarray:
    """WILDER RSI BY A PATH THAT TOUCHES NONE OF THIS MODULE'S HELPERS.

    A scalar Python loop, not a vectorised `rma`, and the ALGEBRAIC ALTERNATE
    FORM `100 * AG / (AG + AL)` rather than `100 - 100/(1+RS)` — two expressions
    of the same definition that agree only if the definition is what both
    implement.  It calls neither `analytics.momentum.rsi`, nor
    `analytics.momentum.rma`, nor `clock()`.

    WHAT WOULD MAKE THIS A FAKE CHECK: computing it the way the program does and
    comparing it to itself — which is why the smoothing is a hand loop and the
    final expression is the other one.
    """
    c = [float(v) for v in closes]
    n = len(c)
    out = [float("nan")] * n
    if n <= length:
        return np.asarray(out, float)
    gains, losses = [], []
    for i in range(1, n):
        ch = c[i] - c[i - 1]
        gains.append(ch if ch > 0 else 0.0)
        losses.append(-ch if ch < 0 else 0.0)
    ag = sum(gains[:length]) / length
    al = sum(losses[:length]) / length
    out[length] = (50.0 if (ag + al) == 0.0 else 100.0 * ag / (ag + al))
    for i in range(length, len(gains)):
        ag = ag + (gains[i] - ag) / length
        al = al + (losses[i] - al) / length
        out[i + 1] = (50.0 if (ag + al) == 0.0 else 100.0 * ag / (ag + al))
    return np.asarray(out, float)


def _raw_closes(sym: str, tf: str) -> tuple[np.ndarray, np.ndarray,
                                            np.ndarray, np.ndarray]:
    """RAW BARS OFF DISK — (open_ms, high, low, close) — for the fixture only.

    1h and 4h are read straight from the parquet with `pandas.read_parquet`, not
    through `clock()`.  12h is bucketed by ARITHMETIC here (`open_ms // MS_12H`,
    three 4h bars, incomplete final bucket dropped by counting) rather than
    through `analytics.structure.resample_ohlcv`, so the fixture's 12h clock is
    an independent construction of the one under test.

    WHAT WOULD MAKE THIS WRONG: calling `clock()` or `load_klines` here, which
    would make the "independent" path the same path.
    """
    p = TB.KLINES / f"{sym}_{'4h' if tf == '12h' else tf}.parquet"
    raw = pd.read_parquet(p).sort_values("open_time")
    t = raw["open_time"].to_numpy(np.int64)
    h = raw["high"].to_numpy(float)
    l_ = raw["low"].to_numpy(float)
    c = raw["close"].to_numpy(float)
    if tf != "12h":
        return t, h, l_, c
    b = t // MS_12H
    ts, hs, ls, cs = [], [], [], []
    i = 0
    while i < len(t):
        j = i
        while j + 1 < len(t) and b[j + 1] == b[i]:
            j += 1
        # A 12h BUCKET COUNTS ONLY IF ALL THREE 4h SLOTS ARE PRESENT — the same
        # completeness rule `clock()` applies, reached here by counting bars
        # rather than by calling `resample_ohlcv`. Head and tail alike.
        if j - i + 1 == 3:
            ts.append(int(b[i]) * MS_12H)
            hs.append(float(np.max(h[i:j + 1])))
            ls.append(float(np.min(l_[i:j + 1])))
            cs.append(float(c[j]))
        i = j + 1
    return (np.asarray(ts, np.int64), np.asarray(hs, float),
            np.asarray(ls, float), np.asarray(cs, float))


def _hand_is_pivot(series: np.ndarray, i: int, side: str) -> bool:
    """(2,2) pivot, checked by four explicit STRICT scalar comparisons.

    STRICT on every neighbour, which is what `analytics.structure.pivots`'
    "unique extreme" clause means — it takes the max AND asserts the max occurs
    exactly once in the window.

    WHAT WOULD MAKE THIS WRONG: `>=` instead of `>`, which admits a flat double
    top as two pivots and would let the fixture bless a scan the module would
    reject; or an asymmetric window.
    """
    if i < PIVOT_L or i + PIVOT_R >= len(series):
        return False
    w = [float(series[i + k]) for k in range(-PIVOT_L, PIVOT_R + 1)]
    c = float(series[i])
    if side == "high":
        return all(c > v for k, v in enumerate(w) if k != PIVOT_L)
    return all(c < v for k, v in enumerate(w) if k != PIVOT_L)


def _leg(name: str, passed: bool, n_checked, detail: str, fails: str) -> dict:
    """One fixture row.  `what_would_make_this_fail` is REQUIRED, not optional.

    WHAT WOULD MAKE THIS WRONG: a leg whose failure condition is blank or
    unfalsifiable — the estate's `F-AN-13` lesson, where a NaN-equals-NaN branch
    made an all-NaN series pass at every k. A leg that cannot fail is decoration.
    """
    return {"fixture": "F-AN-2", "leg": name, "passed": bool(passed),
            "n_checked": n_checked, "detail": detail,
            "what_would_make_this_fail": fails}


def an2_selfcheck() -> pd.DataFrame:
    """F-AN-2 — THREE HAND-VERIFICATIONS FROM RAW BARS, PLUS THE CARDINALITIES.

    Legs 1-3 are the commissioned hand-verifications: one RSI value, one REGULAR
    divergence, one HIDDEN divergence, each recomputed by a path that calls none
    of this module's helpers — raw parquet, a scalar Wilder loop, the alternate
    algebraic RSI form, and five explicit comparisons per pivot.

    Legs 4-13 are CARDINALITY assertions, because a check satisfied by one
    example is not a check.  They count over the whole census: zero finite RSI
    below the warm-up floor, zero pivot pairs closer than 3 bars, zero flags
    using an unconfirmed pivot, 588 of 588 4h as-of indices equal to the event
    bar, a truncation re-derivation on a seeded sample, the present/absent
    partition summing to the book, and the exactly-tied pairs counted rather than
    assumed away.

    WHAT WOULD MAKE THIS FIXTURE WORTHLESS: a leg that cannot fail (the estate's
    own `F-AN-13` lesson — an all-NaN series satisfied a NaN-equals-NaN
    assertion at every k); a hand path that imports the helper it is checking; or
    a single-example leg standing in for a population claim.
    """
    lo_ms, hi_ms, meta = T7.corridor()
    book = _book(lo_ms, hi_ms)
    legs: list[dict] = []
    rng = np.random.default_rng(SEED)

    # ── LEG 1 · ONE RSI VALUE PER CLOCK, HAND-COMPUTED FROM RAW BARS ──────
    picks = [("BTCUSDT", "1h"), ("ETHUSDT", "4h"), ("ZECUSDT", "12h")]
    det, ok1, n1 = [], True, 0
    for sym, tf in picks:
        cl = clock(sym, tf)
        t_raw, _, _, c_raw = _raw_closes(sym, tf)
        # THE TWO PATHS MUST AGREE BAR FOR BAR. On 12h they are two independent
        # bucketings, and `resample_ohlcv` is allowed to be at most ONE bucket
        # more conservative at the tail (it additionally requires a bar in a
        # strictly later bucket to prove closure); anything else is a real
        # disagreement and fails.
        m = min(len(t_raw), cl["n"])
        if not np.array_equal(t_raw[:m], cl["t"][:m]) or not (
                0 <= len(t_raw) - cl["n"] <= 1):
            ok1 = False
            det.append(f"{sym}/{tf}: RAW BAR STAMPS DISAGREE with clock() "
                       f"(fixture {len(t_raw)} bars, module {cl['n']})")
            continue
        j = m - 5                                     # a late, deterministic bar
        hand = _hand_rsi(c_raw[:j + 1], RSI_LEN)[j]
        got = float(cl["rsi"][j])
        d = abs(hand - got)
        n1 += 1
        ok1 = ok1 and (d < 1e-9)
        det.append(f"{sym}/{tf} bar {j} ({iso(int(cl['t'][j]))}): "
                   f"hand {hand:.10f} vs module {got:.10f}  |d|={d:.3e}")
    legs.append(_leg(
        "1 · RSI(14) HAND-VERIFIED FROM RAW BARS, one per clock", ok1, n1,
        " ; ".join(det),
        "a seeded RSI, a wrong smoothing constant, a source other than close, "
        "or a 12h clock whose bars are not three 4h bars"))

    # ── the census, built once for the remaining legs ─────────────────────
    census = []
    for t in book:
        f = T7.frame(t.symbol)["f"]
        for ev, bi in _event_bars(t):
            ev_close = int(f.open_ms[bi]) + MS_4H
            for tf in CLOCKS:
                k = asof_index(t.symbol, tf, ev_close)
                census.append((t, ev, bi, tf, k,
                               divergences_at(t.symbol, tf, k)))
    all_flags = [(t, ev, tf, k, fl) for t, ev, _, tf, k, fs in census
                 for fl in fs]

    # ── LEG 2/3 · ONE REGULAR AND ONE HIDDEN DIVERGENCE, HAND-VERIFIED ────
    def _hand_verify(fl_row) -> tuple[bool, str]:
        """ONE FLAG, RE-DERIVED FROM RAW PARQUET BARS AND A SCALAR RSI LOOP.

        Seven independent checks, each named on the row: pivot-ness by explicit
        comparison, the confirmation lag, the lookback on BOTH pivots, the price
        levels against the raw bars, the RSI at both pivot bars against the hand
        loop, that the two legs actually disagree, and that the class follows
        the pinned table.

        WHAT WOULD MAKE THIS A FAKE CHECK: calling `clock()`, `divergences_at()`
        or `analytics.momentum.rsi` from inside it — the whole value of the leg
        is that it shares no code with the thing it checks. It reads the parquet
        itself and smooths by hand.
        """
        t, ev, tf, k, fl = fl_row
        sym = t.symbol
        cl = clock(sym, tf)
        t_raw, h_raw, l_raw, c_raw = _raw_closes(sym, tf)
        m = min(len(t_raw), cl["n"])
        if not np.array_equal(t_raw[:m], cl["t"][:m]) or not (
                0 <= len(t_raw) - cl["n"] <= 1):
            return False, (f"raw bar stamps disagree with clock() "
                           f"(fixture {len(t_raw)}, module {cl['n']})")
        i0, i1 = int(fl["from_index"]), int(fl["to_index"])
        side = fl["pivot_kind"]
        series = h_raw if side == "high" else l_raw
        checks = []
        # (i) both bars really are (2,2) pivots, by explicit comparison
        p0 = _hand_is_pivot(series, i0, side)
        p1 = _hand_is_pivot(series, i1, side)
        checks.append(("both bars are strict (2,2) pivots", p0 and p1))
        # (ii) the confirmation lag binds — both confirmed at or before the
        #      as-of bar, and NEITHER confirmed after it
        checks.append(("confirmed_at <= asof (no look-ahead)",
                       (i0 + PIVOT_R) <= k and (i1 + PIVOT_R) <= k))
        # (iii) the lookback holds for BOTH pivots
        checks.append((f"both pivots within {DIV_LOOKBACK_BARS} bars of asof",
                       i0 >= k - DIV_LOOKBACK_BARS
                       and i1 >= k - DIV_LOOKBACK_BARS))
        # (iv) the price levels are the raw bars' own
        checks.append(("price levels are the raw bars'",
                       abs(float(series[i0]) - float(fl["price_from"])) < 1e-9
                       and abs(float(series[i1])
                               - float(fl["price_to"])) < 1e-9))
        # (v) the RSI at both pivot bars, hand-computed from raw closes
        hr = _hand_rsi(c_raw[:i1 + 1], RSI_LEN)
        r0, r1 = float(hr[i0]), float(hr[i1])
        checks.append(("RSI at both pivot bars matches the hand loop",
                       abs(r0 - float(fl["rsi_from"])) < 1e-9
                       and abs(r1 - float(fl["rsi_to"])) < 1e-9))
        # (vi) the class follows from the two legs, by the pinned table
        pu, ru = float(series[i1]) > float(series[i0]), r1 > r0
        if side == "high":
            want_kind = "regular" if pu else "hidden"
            want_dir = "bearish"
        else:
            want_kind = "regular" if not pu else "hidden"
            want_dir = "bullish"
        checks.append(("price and RSI legs disagree (it is a divergence)",
                       pu != ru))
        checks.append(("the class follows the pinned table",
                       want_kind == fl["kind"] and want_dir == fl["direction"]))
        allok = all(v for _, v in checks)
        txt = (f"{sym}/{tf} {ev} asof {k} ({iso(int(cl['close_ms'][k]))}) "
               f"{fl['kind']} {fl['direction']} on {side}s: "
               f"pivots {i0}->{i1} price {float(series[i0]):.6f}->"
               f"{float(series[i1]):.6f} rsi {r0:.4f}->{r1:.4f} | "
               + " ; ".join(f"{nm}={v}" for nm, v in checks))
        return allok, txt

    for leg_no, want in ((2, "regular"), (3, "hidden")):
        cand = sorted(
            [fr for fr in all_flags if fr[4]["kind"] == want],
            key=lambda fr: (fr[0].symbol, int(fr[0].entry_ms), fr[2],
                            int(fr[4]["to_index"])))
        if not cand:
            legs.append(_leg(
                f"{leg_no} · {want.upper()} DIVERGENCE HAND-VERIFIED", False, 0,
                f"NO {want} divergence exists in the whole census — which is "
                f"itself a finding, and a fixture that cannot find its subject "
                f"FAILS rather than passes vacuously",
                "an engine that never fires"))
            continue
        okd, txt = _hand_verify(cand[0])
        legs.append(_leg(
            f"{leg_no} · {want.upper()} DIVERGENCE HAND-VERIFIED FROM RAW BARS",
            okd, 1, txt,
            "a pivot that is not a strict (2,2) extreme; a pivot used before "
            "its confirmation bar; an RSI read at the as-of bar instead of the "
            "pivot bar; or a class that does not follow the pinned table"))

    # ── LEG 4 · THE WARM-UP FLOOR, BY CARDINALITY ────────────────────────
    bad, tot = [], 0
    for sym in RC.UNIVERSE:
        for tf in CLOCKS:
            r = clock(sym, tf)["rsi"]
            tot += 1
            nfin = int(np.isfinite(r[:RSI_LEN]).sum())
            if nfin:
                bad.append(f"{sym}/{tf}: {nfin} finite RSI before bar {RSI_LEN}")
            if not np.isfinite(r[RSI_LEN]):
                bad.append(f"{sym}/{tf}: RSI still NaN AT the floor bar "
                           f"{RSI_LEN} — the floor is too high")
    legs.append(_leg(
        "4 · WARM-UP FLOOR — zero finite RSI below the floor, finite AT it",
        not bad, tot,
        "; ".join(bad) if bad else
        f"{tot} (asset x clock) series: 0 finite RSI values at indices "
        f"[0,{RSI_LEN}) and a finite value at index {RSI_LEN} on every one",
        "a seeding EMA/RMA (engine.indicators.ema seeds at the series start and "
        "NEVER returns NaN — repaired four times in this estate), or a floor "
        "set one bar wrong in either direction"))

    # ── LEG 5 · PIVOT SEPARATION, BY CARDINALITY OVER EVERY PAIR USED ────
    gaps = [int(fl["to_index"]) - int(fl["from_index"]) for _, _, _, _, fl
            in all_flags]
    bad5 = [g for g in gaps if g < PIVOT_L + PIVOT_R - 1]
    legs.append(_leg(
        "5 · (2,2) PIVOT SEPARATION — every pair used is >= 3 bars apart",
        not bad5, len(gaps),
        f"{len(gaps)} pairs used across the census; min gap "
        f"{min(gaps) if gaps else None}, max {max(gaps) if gaps else None}; "
        f"{len(bad5)} below 3. A strict-unique (2,2) extreme makes gaps of 1 "
        f"and 2 arithmetically impossible, so any is a broken pivot scan.",
        "a pivot scan that admits equal extremes, or a window off by one"))

    # ── LEG 6 · NO LOOK-AHEAD, BY CARDINALITY OVER EVERY FLAG ────────────
    viol = [(t.symbol, tf, k, int(fl["conf_to"]))
            for t, ev, tf, k, fl in all_flags
            if max(int(fl["conf_from"]), int(fl["conf_to"])) > k]
    legs.append(_leg(
        "6 · NO LOOK-AHEAD — every pivot confirmed at or before its as-of bar",
        not viol, len(all_flags),
        f"{len(all_flags)} flags; {len(viol)} whose confirmation index exceeds "
        f"the as-of bar. A pivot confirmed at j+2 may not be used at bar j.",
        "dropping the confirmed_at <= j filter, or filtering on the pivot index "
        "instead of the confirmation index"))

    # ── LEG 6b · THE HOISTED FILTER == analytics.confirmed_pivots ────────
    same, ncmp = True, 0
    for _ in range(25):
        t = book[int(rng.integers(len(book)))]
        tf = CLOCKS[int(rng.integers(len(CLOCKS)))]
        side = ("high", "low")[int(rng.integers(2))]
        f = T7.frame(t.symbol)["f"]
        k = asof_index(t.symbol, tf, int(f.open_ms[int(t.exit_i)]) + MS_4H)
        cl = clock(t.symbol, tf)
        pi, pl, pc = cl["piv"][side]
        mine = pi[pc <= k]
        ref, _, _ = AS.confirmed_pivots(
            cl["h"] if side == "high" else cl["l"], k, PIVOT_L, PIVOT_R, side)
        ncmp += 1
        same = same and np.array_equal(np.asarray(mine, np.int64),
                                       np.asarray(ref, np.int64))
    legs.append(_leg(
        "6b · THE CACHED PIVOT FILTER IS analytics.structure.confirmed_pivots",
        same, ncmp,
        f"{ncmp} seeded (campaign, clock, side) draws: the hoisted "
        f"`conf <= j` filter returns index arrays identical to "
        f"`AS.confirmed_pivots(values, j, 2, 2, side)`",
        "an optimisation that quietly became a different rule"))

    # ── LEG 7 · THE 4h AS-OF IS THE EVENT BAR ITSELF, ON EVERY EVENT ─────
    n7, bad7 = 0, 0
    for t, ev, bi, tf, k, _ in census:
        if tf != "4h":
            continue
        n7 += 1
        if k != bi:
            bad7 += 1
    legs.append(_leg(
        "7 · AS-OF IDENTITY — the 4h as-of index IS the event's own 4h bar",
        bad7 == 0, n7,
        f"{n7} campaign events on the 4h clock; {bad7} where the as-of index "
        f"differs from the event bar. The event instant is the bar's CLOSE, so "
        f"the last 4h bar closed at that instant is the bar itself — an "
        f"identity, and a broken as-of would break it immediately.",
        "an as-of taken on OPEN stamps, or a `side='left'` searchsorted"))

    # ── LEG 8 · TRUNCATION RE-DERIVATION — CAUSALITY, THE HARD WAY ───────
    idxs = rng.choice(len(census), size=min(60, len(census)), replace=False)
    n8, bad8, ex8 = 0, 0, []
    for ii in idxs:
        t, ev, bi, tf, k, flags = census[int(ii)]
        cl = clock(t.symbol, tf)
        if k < DIV_MIN_ASOF_BAR or k >= cl["n"]:
            continue
        n8 += 1
        # rebuild the whole engine from arrays that STOP at bar k
        c_t = cl["c"][:k + 1]
        h_t = cl["h"][:k + 1]
        l_t = cl["l"][:k + 1]
        r_t = AM.rsi(c_t, RSI_LEN)
        r_t = np.where(np.arange(len(c_t)) >= RSI_LEN, r_t, np.nan)
        got = []
        for side, ser in (("high", h_t), ("low", l_t)):
            pi, pl, pc = AS.pivots(ser, PIVOT_L, PIVOT_R, side)
            keep = (pc <= k) & (pi >= k - DIV_LOOKBACK_BARS)
            i_k, l_k = np.asarray(pi)[keep], np.asarray(pl)[keep]
            if len(i_k) < MIN_PIVOTS_FOR_PAIR:
                continue
            ov = r_t[i_k]
            for kind in ("regular", "hidden"):
                for fl in AM.divergences(i_k, l_k, i_k, ov, pivot_kind=side,
                                         kind=kind, max_pairs=1):
                    got.append((fl["kind"], fl["pivot_kind"], fl["direction"],
                                int(fl["from_index"]), int(fl["to_index"])))
        want = sorted((fl["kind"], fl["pivot_kind"], fl["direction"],
                       int(fl["from_index"]), int(fl["to_index"]))
                      for fl in flags)
        if sorted(got) != want:
            bad8 += 1
            if len(ex8) < 3:
                ex8.append(f"{t.symbol}/{tf}@{k}: truncated {sorted(got)} vs "
                           f"as-of {want}")
    legs.append(_leg(
        "8 · TRUNCATION RE-DERIVATION — the flag set is identical when the "
        "arrays literally stop at the as-of bar", bad8 == 0, n8,
        f"{n8} seeded (campaign, event, clock) cells recomputed from series "
        f"TRUNCATED at bar k — RSI, pivots and divergences all rebuilt on the "
        f"short arrays; {bad8} disagreements. "
        + ("; ".join(ex8) if ex8 else "no disagreement"),
        "any path that lets a bar after k reach a value at k — this is the leg "
        "that would catch a look-ahead the confirmed_at filter missed"))

    # ── LEG 9 · THE +/- WINDOW IS 25 OFFSETS AND OFFSET 0 IS THE AS-OF ──
    pan = rsi_panel(lo_ms, hi_ms)
    cnt = pan.groupby(["asset", "entry_ms", "event", "clock"]).size()
    bad9a = int((cnt != 2 * WINDOW_BARS + 1).sum())
    z = pan[pan["offset_bars"] == 0]
    bad9b = 0
    for _, r_ in z.iterrows():
        cl = clock(r_["asset"], r_["clock"])
        k = int(r_["asof_index"])
        v = float(cl["rsi"][k]) if 0 <= k < cl["n"] else float("nan")
        got = r_["rsi14"]
        if (got is None) != (not np.isfinite(v)):
            bad9b += 1
        elif got is not None and abs(float(got) - r4(v)) > 1e-9:
            bad9b += 1
    legs.append(_leg(
        "9 · THE WINDOW — 25 offsets per cell, and offset 0 IS the as-of RSI",
        bad9a == 0 and bad9b == 0, len(cnt),
        f"{len(cnt)} (campaign, event, clock) cells; {bad9a} without exactly "
        f"{2 * WINDOW_BARS + 1} offset rows; {len(z)} offset-0 rows checked, "
        f"{bad9b} whose RSI is not the as-of RSI. Positive offsets are "
        f"future bars and are flagged `uses_bars_after_the_event`: "
        f"{int(pan['uses_bars_after_the_event'].sum())} of {len(pan)} rows.",
        "a window measured in 4h bars while labelled as the clock's, or an "
        "offset-0 row that is not the classification bar"))

    # ── LEG 10 · THE AS-OF NEVER OVERRUNS THE EVENT, ON ANY CLOCK ───────
    bad10, n10 = 0, 0
    for t, ev, bi, tf, k, _ in census:
        f = T7.frame(t.symbol)["f"]
        ev_close = int(f.open_ms[bi]) + MS_4H
        cl = clock(t.symbol, tf)
        n10 += 1
        if not (0 <= k < cl["n"]) or int(cl["close_ms"][k]) > ev_close:
            bad10 += 1
        elif k + 1 < cl["n"] and int(cl["close_ms"][k + 1]) <= ev_close:
            bad10 += 1                      # not the LAST closed bar
    legs.append(_leg(
        "10 · AS-OF IS THE LAST CLOSED BAR — not a later one, not an earlier "
        "one", bad10 == 0, n10,
        f"{n10} (campaign event x clock) as-of reads; {bad10} where the chosen "
        f"bar closed AFTER the event or where a later bar had also already "
        f"closed",
        "an off-by-one in searchsorted, or a stale clock silently returning an "
        "older bar as 'the last closed one'"))

    # ── LEG 11 · THE 12h STALENESS THAT MOTIVATED THE RESAMPLE ──────────
    st = []
    for sym in RC.UNIVERSE:
        native = TB.load_klines(sym, "12h")
        nt = int(native["open_time"].iloc[-1])
        rt = int(clock(sym, "12h")["t"][-1])
        st.append(f"{sym}: native file last 12h open {iso(nt)}, resampled "
                  f"{iso(rt)}, {(rt - nt) // MS_12H} buckets fresher")
    legs.append(_leg(
        "11 · THE 12h SOURCE CHOICE IS AUDITABLE (measurement, always passes)",
        True, len(RC.UNIVERSE), "; ".join(st),
        "nothing — this leg REPORTS the staleness that motivated resampling "
        "12h from the 4h decision frame, so the choice is a measured number in "
        "the fixture rather than a claim in a docstring"))

    # ── LEG 11b · EVERY 12h BAR HOLDS ALL THREE 4h SLOTS ───────────────
    #    The cardinality assertion behind the head-bucket repair F-AN-2 found.
    bad11, det11 = 0, []
    for sym in RC.UNIVERSE:
        cl = clock(sym, "12h")
        om4 = np.asarray(T7.frame(sym)["f"].open_ms, np.int64)
        uq, uc = np.unique(om4 // MS_12H, return_counts=True)
        cm = dict(zip(uq.tolist(), uc.tolist()))
        cnts = np.array([cm.get(int(b), 0) for b in (cl["t"] // MS_12H)])
        short = int((cnts != 3).sum())
        bad11 += short
        det11.append(f"{sym}: {len(cnts)} 12h bars, {short} not built from "
                     f"exactly 3 four-hour bars")
    legs.append(_leg(
        "11b · 12h COMPLETENESS — every published 12h bar is three 4h bars",
        bad11 == 0, sum(clock(s, "12h")["n"] for s in RC.UNIVERSE),
        "; ".join(det11) + ". THIS LEG FOUND A DEFECT ON ITS FIRST RUN: "
        "`analytics.structure.resample_ohlcv` drops the FORMING bucket at the "
        "tail (AMENDMENT FAN8) but PUBLISHES a partial bucket at the HEAD, and "
        "all five assets' first 12h bar was built from 1 or 2 four-hour bars — "
        "a bar whose HIGH and LOW are understated by construction and which is "
        "a legitimate pivot candidate. `clock()` now filters on completeness.",
        "a resampler that publishes a period built from a fraction of it — the "
        "exact defect FAN8 names at the tail, unhandled at the head"))

    # ── LEG 12 · PRESENT + ABSENT PARTITION THE BOOK, EVERY LINE ────────
    eo = entry_outcome(lo_ms, hi_ms)
    g = eo.groupby(["event", "clock", "family", "direction_group"])
    bad12 = 0
    for _, sub in g:
        if int(sub["n"].sum()) != int(sub["pool_n"].iloc[0]):
            bad12 += 1
    legs.append(_leg(
        "12 · THE PARTITION — present + absent = the direction's whole book",
        bad12 == 0, g.ngroups,
        f"{g.ngroups} (event, clock, family, direction) lines; {bad12} where "
        f"the two n's do not sum to that direction's pool. A campaign whose "
        f"clock is not yet readable lands in ABSENT, which is correct — no "
        f"divergence was readable, so none was present — and it is counted, "
        f"not dropped.",
        "a filter that drops campaigns instead of classifying them, which "
        "would make every rate in the table rest on a silent denominator"))

    # ── LEG 13 · EXACT TIES, COUNTED RATHER THAN ASSUMED AWAY ──────────
    ties_p = sum(1 for _, _, _, _, fl in all_flags
                 if float(fl["price_from"]) == float(fl["price_to"]))
    ties_r = sum(1 for _, _, _, _, fl in all_flags
                 if float(fl["rsi_from"]) == float(fl["rsi_to"]))
    # and the ties the STRICT comparison silently classed as "not up"
    near = 0
    for t, ev, bi, tf, k, _ in census:
        cl = clock(t.symbol, tf)
        if k < DIV_MIN_ASOF_BAR or k >= cl["n"]:
            continue
        for side in ("high", "low"):
            pi, pl, pc = cl["piv"][side]
            keep = (pc <= k) & (pi >= k - DIV_LOOKBACK_BARS)
            i_k, l_k = pi[keep], pl[keep]
            if len(i_k) < 2:
                continue
            if float(l_k[-1]) == float(l_k[-2]):
                near += 1
            elif float(cl["rsi"][i_k[-1]]) == float(cl["rsi"][i_k[-2]]):
                near += 1
    legs.append(_leg(
        "13 · EXACT TIES — counted, printed, not assumed impossible", True,
        len(all_flags),
        f"{ties_p} flags with an exactly equal price pair, {ties_r} with an "
        f"exactly equal RSI pair, and {near} eligible pairs across the whole "
        f"census where price or RSI repeated to the last bit. The comparisons "
        f"are STRICT `>`, so a tie is 'not up' and can only ever SUPPRESS a "
        f"flag, never invent one — this leg exists so that claim rests on a "
        f"count instead of on faith in floats.",
        "nothing — a measurement leg. It becomes load-bearing if the tie count "
        "is ever large, at which point the strict comparison needs a ruling"))

    # ── LEG 14 · CENSORING IN THE FOLLOW-THROUGH ───────────────────────
    ftc = {h: sum(1 for t in book if _followthrough(t, h)["censored"])
           for h in FOLLOW_HORIZONS}
    legs.append(_leg(
        "14 · FOLLOW-THROUGH CENSORING — counted per horizon", True,
        len(book) * len(FOLLOW_HORIZONS),
        "; ".join(f"h={h}: {v} of {len(book)} campaigns have no full "
                  f"{h}-bar future in the corridor and are EXCLUDED from that "
                  f"horizon's mean" for h, v in ftc.items()),
        "nothing — a measurement leg; it fails the READER, not the code, if a "
        "horizon's censored count is ever a large share of its n"))

    # ── LEG 15 · THE COLLAR IS ON EVERY TABLE THIS MODULE EMITS ────────
    need = {"selection_not_a_result", "m_selections_this_table", "gates",
            "as_of_last_closed_4h", "warranty"}
    tabs = {"rsi_panel": pan, "divergence_flags": divergence_flags(lo_ms, hi_ms),
            "entry_outcome": eo,
            "exit_followthrough": exit_followthrough(lo_ms, hi_ms)}
    miss = {k: sorted(need - set(v.columns)) for k, v in tabs.items()
            if need - set(v.columns)}
    badsel = {k: int((v["selection_not_a_result"] != SELECTION).sum())
              for k, v in tabs.items() if "selection_not_a_result" in v.columns}
    legs.append(_leg(
        "15 · THE TIER-E COLLAR — every emitted table carries it in COLUMNS",
        not miss and not any(badsel.values()), len(tabs),
        f"tables {sorted(tabs)}; missing columns {miss or 'none'}; rows whose "
        f"`selection_not_a_result` is not the literal string {badsel}; "
        f"row counts "
        + ", ".join(f"{k}={len(v)}" for k, v in tabs.items()),
        "a table emitted without the collar, which is the only way a Tier-E "
        "number can end up read as a gate"))

    d = pd.DataFrame(legs)
    d["all_legs_passed"] = bool(d["passed"].all())
    d["analytics_version"] = AN.ANALYTICS_VERSION
    d["seed"] = SEED
    d = _tier_e(d, 0, "the fixture itself — no cut of the book is taken here")
    return T8.stamp(d, meta)


# ═══════════════════════════════════════════════════════════════ THE DRIVER
def build(lo_ms: int | None = None, hi_ms: int | None = None) -> dict:
    """Every AN-2 table, in one dict.  NO WRITES — the caller writes.

    WHAT WOULD MAKE THIS WRONG: writing from here (no writes at import time and
    none from a builder; the run script owns the filesystem), or returning a
    table that has not been through `_tier_e` and `T8.stamp` — F-AN-2 leg 15
    asserts every one of them has.
    """
    if lo_ms is None or hi_ms is None:
        lo_ms, hi_ms, _ = T7.corridor()
    return {"an2_rsi_panel": rsi_panel(lo_ms, hi_ms),
            "an2_divergence_flags": divergence_flags(lo_ms, hi_ms),
            "an2_entry_outcome": entry_outcome(lo_ms, hi_ms),
            "an2_exit_followthrough": exit_followthrough(lo_ms, hi_ms),
            "an2_selfcheck": an2_selfcheck()}


if __name__ == "__main__":
    lo, hi, mt = T7.corridor()
    log("=" * 78)
    log("AN-2 · OSCILLATOR COINCIDENCE — TIER-E MEASUREMENT, GATES NOTHING")
    log("=" * 78)
    log(f"  corridor {mt['panel_start']} -> {mt['last_closed_4h_close']} "
        f"({mt['span_days']} d)  m = {M_AN2_TOTAL} selections")
    for nm, df in build(lo, hi).items():
        log(f"  {nm:26} {len(df):7d} rows x {len(df.columns)} cols")
    sc = an2_selfcheck()
    for _, r in sc.iterrows():
        log(f"  {'PASS' if r['passed'] else 'FAIL'}  {r['leg']}")
