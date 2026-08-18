"""AN-1 · RVWAP x WALL CONFLUENCE — STAGE N of TIER-C8.

TIER-E MEASUREMENT ONLY.  GATES NOTHING.  REGISTERS NOTHING.  NO REGISTRATION
RESTS ON THIS WORK AND NONE MAY BE IMPLIED.

Every table this module emits carries a `selection_not_a_result` column whose
text begins **"a SELECTION, not a result"**, a `gates_nothing` column that is
True on every row, and an `m_selection_surface` column naming HOW MANY cells
the row was drawn from — and the same m is LOGGED on every call.  That is the
whole disclosure: this is a grid, it is reported whole, and the biggest number
in it is the biggest number in a grid of that size and nothing more.

────────────────────────────────────────────────────────────────────────────
THE QUESTION THE TABLE ANSWERS
────────────────────────────────────────────────────────────────────────────
*Does a wall that coincides with an RVWAP band edge reject MORE than the same
wall alone?*

`rejection_by_confluence` prints FOUR rates side by side so a reader can
subtract without re-deriving anything:

    rate_wall_colocated_pct   approaches to THE WALL on bars where a band edge
                              sits within 0.25 ATR — rejection judged AGAINST
                              THE WALL
    rate_wall_alone_pct       approaches to THE SAME WALL on bars where that
                              band edge does NOT — rejection AGAINST THE WALL
    rate_band_alone_pct       approaches to THE BAND EDGE on bars where the
                              wall does NOT sit within 0.25 ATR — rejection
                              AGAINST THE BAND
    rate_band_colocated_pct   the band's own co-located arm, printed because it
                              is the free complement of the band-alone scan and
                              because a reader who only sees the wall's two
                              arms cannot tell which level the confluence
                              belongs to

THE FIRST TWO ARE THE SUBTRACTION THAT ANSWERS THE COMMISSION, and they are
built to be subtractable: same wall, same predicate, same corridor, same ATR —
the ONLY difference between the two arms is whether a band edge is nearby.
`rejection_rate_delta_coloc_minus_alone_pp` does the subtraction on the row so
that two readers cannot disagree about which way it went.

CO-LOCATED + WALL-ALONE = ALL WALL APPROACHES, EXACTLY, ON EVERY ROW.  That is
asserted in `an1_selfcheck` as a CARDINALITY assertion over every row of the
grid, not demonstrated on one.  The same holds for the band's two arms.

────────────────────────────────────────────────────────────────────────────
WHAT IS BORROWED, AND WHAT IS COMPUTED, AND WHY
────────────────────────────────────────────────────────────────────────────
BORROWED WHOLE:
  * `tierc5q.champion_series` — the walls, each on ITS OWN CLOCK.  TIER-C5-Q's
    own docstring states the reading this commission asks for verbatim: "each
    is read as-of the LAST CLOSED bar of ITS OWN timeframe".  `_wall_series_one`
    is the body of that function for ONE (tf, ema) pair, and `an1_selfcheck`
    asserts it reproduces `champion_series` EXACTLY for all four champions on
    all five assets — 20 series, every finite element, no tolerance.
  * `analytics.vwap.rolling_vwap` — the RVWAP and its bands, the identical call
    `tierc2_baseline.build_level_series` makes (hlc3 source, raw 4h volume,
    sigmas (1, 2)).  `an1_selfcheck` asserts the arrays are element-identical
    to `build_level_series(k4)["rvwap"]` before the floor is applied.
  * `tierc5.LEAGUE_APPROACH_ATR` / `LEAGUE_RESOLVE_BARS` and TIER-C6's
    `league()` predicate, transcribed clause for clause into `_scan`.
  * `tierc8.stamp` — the as-of warranty [TC6V-a], on every returned table.

COMPUTED HERE, AND THE REASON:
  * THE AS-OF READ ONTO THE 4h TIMELINE.  `tierc5q.champion_cols` returns
    r6-ROUNDED PYTHON LISTS and a signed distance; this module needs the raw
    float arrays to difference against a band.  `_wall_on_4h` therefore does
    the identical searchsorted/warm-floor arithmetic and `an1_selfcheck`
    asserts the r6 of its output equals `champion_cols`' `champ_*` column
    element for element, on all five assets and all four champions.
  * THE FIFTH WALL.  `tierc5q.CHAMPIONS` is a frozen four-tuple that predates
    TIER-C6 growing the league a SECOND SIDE, so the support champion —
    300 @ 12h — is not in it.  It is built by the same `_wall_series_one` used
    for the other four; nothing about it is special except that TIER-C5-Q could
    not have named it.

────────────────────────────────────────────────────────────────────────────
SIX READINGS THIS MODULE HAD TO SETTLE, EACH WITH THE ALTERNATIVE NAMED
────────────────────────────────────────────────────────────────────────────
(1) THE SCAN RUNS ON THE 4h TIMELINE, NOT ON EACH WALL'S OWN CLOCK.
    TIER-C6's `league()` scans 1h walls on 1h bars and 1d walls on 1d bars.
    That cannot be done here: a CO-LOCATION between a 1h wall and a 4h RVWAP
    band only EXISTS on one clock, and the estate's decision lens is 4h.  So
    the wall is read as-of onto the 4h timeline (which is exactly what
    TIER-C5-Q and TIER-C6's own `wall_series_12h` do for the decision path) and
    the league's predicate is applied to 4h bars.
    THE CONSEQUENCE, SAID OUT LOUD: `LEAGUE_RESOLVE_BARS = 3` now means THREE
    4h BARS — TWELVE HOURS — for every wall, where in the league it meant three
    bars of the wall's own timeframe (three DAYS for the 1d wall).  The
    rejection rates in this table are therefore NOT the league's numbers and
    must not be compared to them; the column `resolve_window_hours` prints 12
    on every row so the difference cannot be lost.  THE ALTERNATIVE — scanning
    each wall on its own clock — is not available, because there would be
    nothing to co-locate it with.

(2) THE ATR IS THE 4h ATR, ON BOTH THE TOLERANCE AND THE TOLL.
    Both objects being differenced live on the 4h timeline, and a tolerance
    quoted in each wall's OWN-clock ATR would mean "0.25 ATR" is a ~4x tighter
    distance for the 1h wall than for the 1d wall — the cells of the grid would
    then not be measuring the same thing while looking as if they were.
    THE ALTERNATIVE IS PRINTED RATHER THAN DISCARDED: every row of
    `confluence_table` also carries `coloc_share_own_clock_atr_pct`, the same
    share computed with the wall's own-clock ATR, so a reader can see how much
    of the co-location share is a choice of yardstick.

(3) "WITHIN 0.25 ATR" IS THE COMMISSION'S NUMBER, AND IT IS *NOT* THE ESTATE'S
    EXISTING CO-LOCATION PIN.  `tierc2_baseline.COLOCATION_ATR` is 0.15 (the
    census2a pin, register row 13).  The commission says 0.25 and 0.25 is used,
    which has the incidental virtue of making the co-location tolerance and the
    league's APPROACH tolerance the same distance — a band edge is "co-located"
    with a wall exactly when it is inside the zone the league already calls an
    approach.  The 0.15 pin is named here so nobody reads 0.25 as the estate's
    standing convention.

(4) THE SIDE TEST IS THE LEAGUE'S — ON THE PREVIOUS BAR'S CLOSE.
    "resistance = above, support = below" is read as the league reads it: the
    level is on the named side of the PREVIOUS CLOSE (`c[i-1] < level[i-1]` for
    resistance).  For `confluence_table` that gives a second, side-conditioned
    share; the headline share is the SIDE-AGNOSTIC geometry, because "how often
    do these two levels sit on top of each other" is a question about the two
    levels and not about where price happened to be.  Both are columns.

(5) THE GRID IS REPORTED WHOLE, INCLUDING EACH WALL'S NON-CHAMPION SIDE.
    The commissioned walls are per-side champions (resistance 889@12h, 889@1d,
    3618@4h, 4618@1h; support 300@12h).  Rows for the OTHER side of each wall
    are emitted too, flagged `is_commissioned_side = False`, because a grid
    reported only where it was expected to win is a grid a reader cannot audit.
    They are flagged, not hidden, and not led with.

(6) REJECTION IN THE CO-LOCATED ARM IS JUDGED AGAINST THE WALL.
    A confluence is two levels 0.25 ATR apart and "did price close through"
    needs ONE of them.  The wall is chosen because the commission's question is
    about the WALL ("does a wall that coincides with a band reject more than
    the same wall alone") and because judging the co-located arm against a
    different level from the wall-alone arm would make the subtraction
    meaningless.  THE ALTERNATIVE IS PRINTED, NOT DISCARDED:
    `rate_band_colocated_pct` is the same confluence judged against the band.

────────────────────────────────────────────────────────────────────────────
WARM-UP FLOORS — ALL FOUR OF THEM, EXPLICIT
────────────────────────────────────────────────────────────────────────────
`engine.indicators.ema` SEEDS AT THE SERIES START AND NEVER RETURNS NaN.  This
estate has repaired that defect FOUR times.  This module is not the fifth.

    WALL EMA      NaN until the wall's own-clock index >= its own EMA length
                  (`k >= L`, TIER-C5-Q's floor, transcribed).
    WALL ATR      the same floor, on the same clock (never binding: L >> 14).
    4h ATR        NaN until index >= ATR_LEN.  Explicit, and asserted NEVER
                  BINDING on this corridor — every other floor is longer, so a
                  reader is told it is inert rather than left to wonder.
    RVWAP BANDS   `analytics.vwap.rolling_vwap` FLOORS AT `MIN_BARS = 10` MOST
                  RECENT BARS EVEN WHEN THEY FALL OUTSIDE THE WINDOW, so bar 3
                  of the series carries a "90-day" band built from four bars.
                  The band is NaN here until the trailing window is FULLY
                  SPANNED — `open_ms[i] - open_ms[0] >= window_days` — AND holds
                  at least `MIN_BARS` bars.  Both conditions, because a cache
                  gap can satisfy the first without the second.

────────────────────────────────────────────────────────────────────────────
NO LOOK-AHEAD, AND IT IS PROVED BY TRUNCATION, NOT BY INSPECTION
────────────────────────────────────────────────────────────────────────────
Every series here is causal by construction, and `an1_selfcheck` proves it the
only way that is worth anything: it REBUILDS the wall and the band from raw
bars TRUNCATED AT BAR j and asserts the endpoint equals the full-history
series at j, for a spread of j across assets.  A future bar leaking into either
object moves that endpoint.

────────────────────────────────────────────────────────────────────────────
F-AN-1 · THE FIXTURE
────────────────────────────────────────────────────────────────────────────
`an1_selfcheck()` returns a DataFrame of checks.  THREE of them are
hand-verifications from RAW PARQUET BARS, walked by explicit arithmetic written
out in this module and never by calling the function under test:

    HAND-CO-LOCATION  one co-located bar: the 12h/889 wall re-derived from the
                      raw 12h klines by a literal EMA recursion, the 30d +1σ
                      band re-derived by a literal volume-weighted sum over the
                      raw 4h window, the 4h ATR re-derived by a literal Wilder
                      recursion — then the 0.25-ATR verdict re-taken by hand.
    HAND-REJECTION    one co-located approach: the previous close's side, the
                      high's reach into the 0.25-ATR zone, and all four closes
                      of the resolve window, each compared by hand to the wall
                      AT ITS OWN BAR.
    HAND-TOLL         one bar's round-trip toll, `2 * FEE_BPS_SIDE / 10_000 *
                      close / ATR`, from the raw close and the hand ATR.

The other checks are CARDINALITY assertions over the whole grid — arm counts
summing to totals on every row, panel rows equal to the pooled asset rows on
every row, rates inside [0, 100] everywhere, warm floors holding on every
(asset, series) pair — because a check satisfied by one example is not a check.

Drafted for STAGE N of TIER-C8.  Measurement only.  It gates nothing.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402
import tierc5q as Q                                                  # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
from analytics import vwap as AW                                     # noqa: E402
from engine import indicators as ind                                 # noqa: E402

iso, r4, r6, pct = TB.iso, TB.r4, TB.r6, TB.pct
log = TB.log
load_klines = TB.load_klines
frame, corridor = T7.frame, T7.corridor
_idx_range = TB._idx_range
MS_1H, MS_4H, MS_1D = TB.MS_1H, TB.MS_4H, TB.MS_1D
MS_12H = 12 * MS_1H

# ═══════════════════════════════════════════════════════ THE COMMISSIONED GRID
# THE FIVE WALLS — TIER-C6's per-side league champions, with the side each one
# actually won.  `side` here is PROVENANCE, not a filter: rows are emitted for
# both sides of every wall and flagged (reading 5).
WALLS: tuple[tuple[str, int, str], ...] = (
    ("12h", 889, "resistance"),
    ("1d", 889, "resistance"),
    ("4h", 3618, "resistance"),
    ("1h", 4618, "resistance"),
    ("12h", 300, "support"),
)
RVWAP_WINDOWS = (7, 30, 90)          # the commissioned three of TB's four
SIGMAS = (1, 2)                      # +/-1 sigma, +/-2 sigma
SIDES = ("resistance", "support")

COLOC_ATR = 0.25                     # reading (3) — NOT TB.COLOCATION_ATR (0.15)
APPROACH_ATR = T5.LEAGUE_APPROACH_ATR        # 0.25, TIER-C6's league, bound
RESOLVE_BARS = T5.LEAGUE_RESOLVE_BARS        # 3, TIER-C6's league, bound
PROVISIONAL_MIN_N = RC.PROVISIONAL_MIN_N     # 30
ATR_LEN = RC.ATR_LEN                         # 14
FEE_BPS_SIDE = RC.FEE_BPS_SIDE               # 5.0 per side -> 10.0 round trip

SELECTION_NOTE = (
    "a SELECTION, not a result — TIER-E measurement over a grid this row was "
    "drawn from; it GATES NOTHING, no registration rests on it, and the "
    "largest number in this table is the largest number in a grid of size m")
SCAN_NOTE = (
    "scanned on the 4h timeline with the wall read as-of the last CLOSED bar "
    "of its own clock; LEAGUE_RESOLVE_BARS = 3 therefore means 3 FOUR-HOUR "
    "bars (12 h), NOT 3 bars of the wall's own timeframe — these rejection "
    "rates are NOT TIER-C6's league numbers and may not be compared to them")

_WALL_SERIES: dict[tuple[str, str, int], dict] = {}
_WALL_4H: dict[tuple[str, str, int], tuple[np.ndarray, np.ndarray]] = {}
_BANDS: dict[str, dict[str, np.ndarray]] = {}
_ATR4: dict[str, np.ndarray] = {}


def band_names() -> tuple[str, ...]:
    """The twelve commissioned band edges, named as `build_level_series` names
    them so a reader can join this table to the estate's tape without a map.
    WHAT WOULD MAKE THIS WRONG: a name that does not match
    `build_level_series`' key (the join would silently miss), or emitting the
    365-day window, which the commission did not ask for and which would grow
    the selection surface by a third without anybody deciding to.
    """
    return tuple(f"rvwap_{wd}d_{ud}{s}"
                 for wd in RVWAP_WINDOWS for s in SIGMAS for ud in ("up", "dn"))


def wall_name(tf: str, L: int) -> str:
    """The wall's stable name, `12h_ema889` — TIER-C5-Q's own key format, so a
    row of this table joins to the estate's tape without a translation layer.

    WHAT WOULD MAKE THIS WRONG: putting the EMA length first, which would sort
    the 1h/4618 wall next to the 1d/889 one and make a grouped table read as if
    two timeframes were one.
    """
    return f"{tf}_ema{L}"


# ═══════════════════════════════════════════════════════════ THE WALL, ITS CLOCK
def _wall_series_one(sym: str, tf: str, L: int) -> dict:
    """ONE wall on ITS OWN CLOCK — the body of `tierc5q.champion_series` for a
    single (tf, ema) pair, and asserted identical to it for the four pairs that
    function covers.

    It exists at all because `tierc5q.CHAMPIONS` is a frozen four-tuple written
    before TIER-C6 grew the league a SECOND SIDE, so the support champion
    300 @ 12h has no entry in it.  `close_ms = open_ms + step` is the instant
    the bar became knowable; a caller at instant `t` takes the last bar with
    `close_ms <= t`, which is the whole causality argument.

    WHAT WOULD MAKE THIS WRONG: a `step` that does not match the timeframe (the
    as-of would then be taken from a bar that had not closed); resampling 1h to
    12h here rather than reading the cache's own 12h file, which would make
    this a THIRD 12h series in an estate that already has two; or omitting the
    ATR, which the own-clock sensitivity column needs.
    """
    key = (sym, tf, int(L))
    if key in _WALL_SERIES:
        return _WALL_SERIES[key]
    d = T5._tf_frame(sym, tf)
    step = {"1h": MS_1H, "4h": MS_4H, "12h": MS_12H, "1d": MS_1D}[tf]
    _WALL_SERIES[key] = {
        "close_ms": d["t"] + step,
        "ema": ind.ema(d["c"], int(L)),
        "atr": ind.atr(d["h"], d["l"], d["c"], ATR_LEN),
        "tf": tf, "ema_len": int(L),
    }
    return _WALL_SERIES[key]


def wall_on_4h(sym: str, tf: str, L: int) -> tuple[np.ndarray, np.ndarray]:
    """The wall and its OWN-clock ATR, read onto the 4h timeline AS OF THE LAST
    CLOSED BAR OF ITS OWN CLOCK.  Returns (level, own_atr), both NaN until warm.

    THE AS-OF INSTANT IS THE 4h BAR'S **CLOSE**, NOT ITS OPEN — the repair
    TIER-C6 made in `wall_series_12h` and TIER-C5-Q made in `champion_cols`,
    both of which say so in their own docstrings.  A 4h row is KEYED on its
    open, but every value in it is the value at its close, which is the instant
    a reader of that row is standing at.  Selecting with `close_ms <= open_ms`
    would quote a wall four hours staler than the price beside it.

    AND THE EMA IS NULL UNTIL WARM: `ind.ema` seeds at the series start and
    never returns NaN, so a 4,618-length EMA would otherwise publish the first
    hourly close in the cache as a "wall".  `k >= L` is TIER-C5-Q's floor,
    transcribed: the EMA has seen its own length on its own clock.

    WHAT WOULD MAKE THIS WRONG: as-of the open; `side="left"` in the
    searchsorted (it would take the NEXT bar, which has not closed); dropping
    the `k >= L` floor; or floor-testing on the 4h index rather than on the
    wall's own-clock index k, which for the 1d wall would be six times too
    lenient.
    """
    key = (sym, tf, int(L))
    if key in _WALL_4H:
        return _WALL_4H[key]
    s = _wall_series_one(sym, tf, L)
    ot = frame(sym)["f"].open_ms
    as_of = ot + MS_4H                       # the 4h bar's CLOSE
    k = np.searchsorted(s["close_ms"], as_of, "right") - 1
    ok = k >= int(L)                         # THE FLOOR, on the wall's clock
    lvl = np.full(len(ot), np.nan)
    own = np.full(len(ot), np.nan)
    lvl[ok] = s["ema"][k[ok]]
    own[ok] = s["atr"][k[ok]]
    _WALL_4H[key] = (lvl, own)
    return _WALL_4H[key]


# ═══════════════════════════════════════════════════════ THE RVWAP BANDS, 4h
def rvwap_bands(sym: str) -> dict[str, np.ndarray]:
    """The twelve commissioned band edges on the 4h lens, WARM-UP FLOORED.

    `analytics.vwap.rolling_vwap` IS the estate's object and is called with the
    identical arguments `tierc2_baseline.build_level_series` uses — hlc3 source,
    raw 4h volume, sigmas (1, 2).  It is called directly rather than through
    `build_level_series` because that function additionally builds the 365-day
    window, the whole AVWAP set and three period-extreme families, none of
    which AN-1 measures; `an1_selfcheck` asserts the arrays produced here are
    ELEMENT-IDENTICAL to `build_level_series(k4)["rvwap"]` before the floor.

    THE FLOOR IS THE POINT OF THIS FUNCTION.  `rolling_vwap` floors its window
    at `MIN_BARS = 10` most recent bars EVEN WHEN THEY FALL OUTSIDE the window
    (`analytics/vwap.py:235`), so the fourth bar of a series carries a
    "90-day" band computed from four bars — a band that is narrow because it is
    young, not because dispersion is low.  A band is NULL here until

        (i)  the trailing window is FULLY SPANNED by the data,
             `open_ms[i] - open_ms[0] >= window_days * 86_400_000`, AND
        (ii) at least `MIN_BARS` bars actually fall inside it.

    BOTH, because a cache gap can satisfy (i) while leaving (ii) false, and a
    sigma over three bars is not a sigma.

    WHAT WOULD MAKE THIS WRONG: flooring on a BAR COUNT rather than on the
    window's own span (a gap would then pass); flooring the centre line but not
    the bands; or taking the source from the 4h CLOSE rather than hlc3, which
    is the estate's pinned VWAP source and would silently be a different level
    family wearing the same name.
    """
    if sym in _BANDS:
        return _BANDS[sym]
    k4 = frame(sym)["k4"]
    ot = k4["open_time"].to_numpy(np.int64)
    hi = k4["high"].to_numpy(float)
    lo = k4["low"].to_numpy(float)
    cl = k4["close"].to_numpy(float)
    vol = k4["volume"].to_numpy(float)
    src = (hi + lo + cl) / 3.0                      # hlc3, the estate's source
    out: dict[str, np.ndarray] = {}
    for wd in RVWAP_WINDOWS:
        r = AW.rolling_vwap(ot, src, vol, window_days=wd, sigmas=SIGMAS)
        w_ms = int(wd) * AW.DAY_MS
        spanned = (ot - ot[0]) >= w_ms
        # bars strictly inside the window (t[i] - W, t[i]] — rolling_vwap's own
        # membership test, counted rather than assumed
        first = np.searchsorted(ot, ot - w_ms, "right")
        enough = (np.arange(len(ot)) - first + 1) >= AW.MIN_BARS
        warm = spanned & enough
        for s in SIGMAS:
            for ud in ("up", "dn"):
                v = np.asarray(r[f"band_{ud}_{s}"], float).copy()
                v[~warm] = np.nan
                out[f"rvwap_{wd}d_{ud}{s}"] = v
    _BANDS[sym] = out
    return _BANDS[sym]


def atr_4h(sym: str) -> np.ndarray:
    """The 4h ATR with an EXPLICIT floor at its own length.

    `ind.atr` is `rma(true_range(...))` and `rma` seeds at the series start, so
    like every other rolling series in this estate it is finite from bar 0 and
    a floor has to be written down rather than assumed.  It is floored at
    `ATR_LEN`, and `an1_selfcheck` asserts THIS FLOOR IS NEVER BINDING on this
    corridor — every wall floor and every band floor is longer — so a reader is
    told it is inert instead of being left to wonder whether it mattered.

    WHAT WOULD MAKE THIS WRONG: leaving it unfloored on the argument that it is
    never binding.  It is never binding ON THIS CORRIDOR; a shorter corridor or
    a shorter band window would make it binding, and the floor is what stops
    that from being a silent change.
    """
    if sym in _ATR4:
        return _ATR4[sym]
    a = np.asarray(frame(sym)["f"].atr, float).copy()
    a[np.arange(len(a)) < ATR_LEN] = np.nan
    a[~(a > 0)] = np.nan
    _ATR4[sym] = a
    return a


def toll_atr(sym: str) -> np.ndarray:
    """THE ROUND-TRIP TOLL AT EACH 4h BAR, IN ATR.

    `2 * FEE_BPS_SIDE / 10_000 * close / ATR` — the fee a round trip pays,
    expressed in the same unit the co-location tolerance and the approach zone
    are expressed in, because "the wall rejected by 0.31 ATR" and "the trip
    costs 0.04 ATR" are only comparable if both are ATR.

    FUNDING IS NOT IN IT, AND THAT IS SAID RATHER THAN LEFT OUT.  A toll on an
    APPROACH has no holding period — an approach is a bar, not a position — so
    there is no funding to charge.  The estate's funding line
    (`FUNDING_CEILING_R`) belongs to campaigns, not to bars, and importing it
    here would invent a holding period this table does not have.

    WHAT WOULD MAKE THIS WRONG: charging one side instead of two; dividing by
    the wall's own-clock ATR while the rest of the row uses the 4h ATR; or
    quoting it in R, which this table has no R to quote it in.
    """
    f = frame(sym)["f"]
    return (2.0 * FEE_BPS_SIDE / 10_000.0) * np.asarray(f.c, float) / atr_4h(sym)


# ═══════════════════════════════════ TIER-C6's LEAGUE PREDICATE, TRANSCRIBED
def _scan(level: np.ndarray, h: np.ndarray, l: np.ndarray, c: np.ndarray,
          a: np.ndarray, side: str, i0: int, i1: int
          ) -> tuple[np.ndarray, np.ndarray]:
    """APPROACH and BROKE-THROUGH, TIER-C6 `league()` clause for clause.

    RESISTANCE  the bar's HIGH comes within `APPROACH_ATR` of the level FROM
                BELOW — and the PREVIOUS close must be below the PREVIOUS
                level, not below the current one.  BROKE = some close in
                `[i, i+RESOLVE_BARS]` is above THE LEVEL AT THAT BAR.
    SUPPORT     the mirror, in full: low from above, previous close above the
                previous level, broke = a close below the level at that bar.

    REJECTION IS `approach AND NOT broke`, and it is left to the caller so the
    caller can partition the SAME approach set three ways without re-scanning.

    THE LEVEL IS READ AT EACH BAR OF THE RESOLVE WINDOW, NOT FROZEN AT THE
    APPROACH BAR.  TIER-C6 writes `seg = c[w] - e[w]`; freezing the level would
    be a different and easier test for a rising wall, and the two disagree most
    exactly where the wall is moving fastest.

    NO LOOK-AHEAD, TWICE OVER: the approach at bar i reads bars i-1 and i only,
    and the resolve window is clipped at `i1` so no bar outside the scanned
    corridor is ever read.

    WHAT WOULD MAKE THIS WRONG: comparing `c[i-1]` to `level[i]` (the previous
    close against a level that did not exist yet); using `>` where the league
    uses `>=` on the approach reach; freezing the level in the resolve window;
    letting the window run past `i1`; or forgetting that a NaN level makes
    every comparison False — which is the behaviour that carries the warm-up
    floor into this function without a second test.
    """
    if side not in SIDES:
        raise SystemExit(f"HALT: unknown side {side!r}")
    n = len(c)
    idx = np.arange(n)
    lev_prev = np.concatenate(([np.nan], level[:-1]))
    c_prev = np.concatenate(([np.nan], c[:-1]))
    with np.errstate(invalid="ignore"):
        warm = np.isfinite(level) & np.isfinite(lev_prev) & np.isfinite(a) & (a > 0)
        tol = APPROACH_ATR * a
        if side == "resistance":
            prev_side = c_prev < lev_prev
            touch = h >= (level - tol)
            thru = c > level
        else:
            prev_side = c_prev > lev_prev
            touch = l <= (level + tol)
            thru = c < level
    inwin = (idx >= max(int(i0), 1)) & (idx <= int(i1))
    approach = warm & prev_side & touch & inwin
    thru = thru & np.isfinite(level) & np.isfinite(c)
    broke = np.zeros(n, bool)
    for s in range(0, RESOLVE_BARS + 1):
        sh = np.zeros(n, bool)
        if s == 0:
            sh = thru.copy()
        else:
            sh[:n - s] = thru[s:]
        sh &= (idx + s) <= int(i1)           # the window never leaves the scan
        broke |= sh
    return approach, broke


def _side_mask(level: np.ndarray, c: np.ndarray, side: str) -> np.ndarray:
    """Is this level on the named side of the PREVIOUS close? — reading (4).

    The league's own side test, lifted out so `confluence_table` can ask it of
    a wall and a band independently.

    WHAT WOULD MAKE THIS WRONG: testing against the CURRENT close, which would
    make a level price has already closed through count as still being on the
    far side of it.
    """
    lev_prev = np.concatenate(([np.nan], level[:-1]))
    c_prev = np.concatenate(([np.nan], c[:-1]))
    with np.errstate(invalid="ignore"):
        return (c_prev < lev_prev) if side == "resistance" else (c_prev > lev_prev)


def _meta_for(lo_ms: int, hi_ms: int) -> dict:
    """The corridor meta `tierc8.stamp` wants, describing WHAT WAS SCANNED.

    `corridor()`'s meta describes the cache's edge; if a caller hands this
    module a narrower window the warranty must name THE WINDOW SCANNED, not the
    cache's, or the stamp is a claim about data the table does not contain.

    WHAT WOULD MAKE THIS WRONG: stamping `corridor()`'s edge unconditionally.
    """
    _, _, m = corridor()
    m = dict(m)
    m["panel_start"] = iso(int(lo_ms))
    m["last_closed_4h_close"] = iso(int(hi_ms) + 1)
    m["span_days"] = round((int(hi_ms) + 1 - int(lo_ms)) / MS_1D, 1)
    return m


def _finish(df: pd.DataFrame, lo_ms: int, hi_ms: int, label: str
            ) -> pd.DataFrame:
    """The three obligations, applied to every table this module returns:
    the SELECTION disclosure, the logged m, and the as-of warranty [TC6V-a].

    WHAT WOULD MAKE THIS WRONG: putting the disclosure in a caption instead of
    a column (a caption does not survive a copy of the row — TC6V-a's own
    argument), or computing m as something other than the number of cells a
    reader could pick a maximum from.
    """
    n_panel = int((df["asset"] == "__PANEL__").sum()) if len(df) else 0
    m = int(len(df))
    d = df.copy()
    d["selection_not_a_result"] = SELECTION_NOTE
    d["gates_nothing"] = True
    d["m_selection_surface"] = m
    d["m_selection_surface_panel_cells"] = n_panel
    d["tier"] = "TIER-E measurement · AN-1 · registers nothing"
    d["scan_note"] = SCAN_NOTE
    d["resolve_window_hours"] = int(RESOLVE_BARS * 4)
    d["coloc_tol_atr"] = COLOC_ATR
    d["approach_tol_atr"] = APPROACH_ATR
    log(f"  AN-1 {label}: m = {m} cells in this selection surface "
        f"({n_panel} of them panel cells) — a SELECTION, not a result; "
        f"it gates nothing")
    return T8.stamp(d, _meta_for(lo_ms, hi_ms))


# ═══════════════════════════════════════════════ (a) THE CO-LOCATION SHARE
def confluence_table(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """(a) CO-LOCATION SHARE — how often a wall and a band edge sit within
    0.25 ATR of each other, per (side, wall, band, window) cell, per asset and
    pooled.

    THE HEADLINE SHARE IS SIDE-AGNOSTIC GEOMETRY: of the bars where BOTH series
    are warm, the fraction on which `|wall - band| <= 0.25 * ATR_4h`.  "How
    often do these two levels sit on top of each other" is a question about the
    two levels; where price happened to be that bar is a second question and it
    gets a second column (`coloc_share_on_side_pct`, denominated on the bars
    where BOTH levels are on the named side of the previous close).

    THE PANEL ROW POOLS COUNTS, NOT RATES — TIER-C6's own repair, inherited.  An
    unweighted mean of five per-asset shares sitting beside a pooled count is
    two populations on one row.  `mean_abs_gap_atr` is pooled on its own
    denominator (both-warm bars) and the toll on its own (co-located bars),
    because they are conditional means over different populations and pooling
    the second on the first is the exact defect TC6-V #33 caught.

    n IS `n_colocated` AND `provisional` IS `n < 30`, per the commission.

    WHAT WOULD MAKE THIS WRONG: a denominator of ALL bars rather than
    both-warm bars (the 4h/3618 wall is unwarm for the first ~1.7 years of the
    corridor and would look co-located less often for a reason that has nothing
    to do with confluence); pooling a conditional mean on the wrong count; or
    comparing a wall to a band on a bar where either is NaN, which the warm
    mask refuses.
    """
    rows: list[dict] = []
    for tf, L, champ_side in WALLS:
        wname = wall_name(tf, L)
        for side in SIDES:
            for bname in band_names():
                acc = {"n_scanned": 0, "n_both_warm": 0, "n_side_elig": 0,
                       "n_coloc": 0, "n_coloc_side": 0, "n_coloc_own": 0,
                       "sum_gap": 0.0, "sum_toll": 0.0}
                per_asset = []
                for sym in RC.UNIVERSE:
                    f = frame(sym)["f"]
                    i0, i1 = _idx_range(f.open_ms, lo_ms, hi_ms)
                    if i1 < i0:
                        continue
                    lvl, own = wall_on_4h(sym, tf, L)
                    band = rvwap_bands(sym)[bname]
                    a4 = atr_4h(sym)
                    tl = toll_atr(sym)
                    idx = np.arange(len(f.c))
                    inwin = (idx >= max(i0, 1)) & (idx <= i1)
                    with np.errstate(invalid="ignore"):
                        both = (np.isfinite(lvl) & np.isfinite(band)
                                & np.isfinite(a4) & inwin)
                        gap = np.abs(lvl - band)
                        coloc = both & (gap <= COLOC_ATR * a4)
                        coloc_own = (both & np.isfinite(own)
                                     & (own > 0) & (gap <= COLOC_ATR * own))
                        se = (both & _side_mask(lvl, f.c, side)
                              & _side_mask(band, f.c, side))
                    n_both = int(both.sum())
                    n_col = int(coloc.sum())
                    n_se = int(se.sum())
                    n_cs = int((coloc & se).sum())
                    s_gap = float(np.sum(gap[both] / a4[both])) if n_both else 0.0
                    s_tol = float(np.nansum(tl[coloc])) if n_col else 0.0
                    acc["n_scanned"] += int(inwin.sum())
                    acc["n_both_warm"] += n_both
                    acc["n_side_elig"] += n_se
                    acc["n_coloc"] += n_col
                    acc["n_coloc_side"] += n_cs
                    acc["n_coloc_own"] += int(coloc_own.sum())
                    acc["sum_gap"] += s_gap
                    acc["sum_toll"] += s_tol
                    per_asset.append((sym, int(inwin.sum()), n_both, n_se,
                                      n_col, n_cs, int(coloc_own.sum()),
                                      s_gap, s_tol))
                for (sym, n_sc, n_both, n_se, n_col, n_cs, n_co,
                     s_gap, s_tol) in per_asset:
                    rows.append(_coloc_row(side, tf, L, champ_side, bname, sym,
                                           n_sc, n_both, n_se, n_col, n_cs,
                                           n_co, s_gap, s_tol))
                rows.append(_coloc_row(
                    side, tf, L, champ_side, bname, "__PANEL__",
                    acc["n_scanned"], acc["n_both_warm"], acc["n_side_elig"],
                    acc["n_coloc"], acc["n_coloc_side"], acc["n_coloc_own"],
                    acc["sum_gap"], acc["sum_toll"]))
    return _finish(pd.DataFrame(rows), lo_ms, hi_ms, "confluence_table")


def _coloc_row(side, tf, L, champ_side, bname, sym, n_sc, n_both, n_se,
               n_col, n_cs, n_co, s_gap, s_tol) -> dict:
    """One cell of (a).  Split out so the per-asset and the pooled row are
    built by the SAME arithmetic — a panel row assembled by a second code path
    is a panel row that can disagree with its own asset rows.

    WHAT WOULD MAKE THIS WRONG: dividing the toll by `n_both` (it is a mean
    over CO-LOCATED bars) or the gap by `n_col` (it is a mean over BOTH-WARM
    bars).  Two conditional means, two denominators.
    """
    wd, sig, ud = _band_parts(bname)
    return {
        "side": side, "asset": sym,
        "wall": wall_name(tf, L), "wall_tf": tf, "wall_ema": int(L),
        "wall_champion_side": champ_side,
        "is_commissioned_side": bool(side == champ_side),
        "band": bname, "band_window_days": wd, "band_sigma": sig,
        "band_edge": ud,
        "band_edge_natural_side": ("resistance" if ud == "up" else "support"),
        "n_bars_scanned": int(n_sc),
        "n_bars_both_warm": int(n_both),
        "n_bars_side_eligible": int(n_se),
        "n_colocated": int(n_col),
        "n_colocated_on_side": int(n_cs),
        "n": int(n_col),
        "coloc_share_pct": pct(n_col, n_both),
        "coloc_share_on_side_pct": pct(n_cs, n_se),
        "coloc_share_own_clock_atr_pct": pct(n_co, n_both),
        "mean_abs_gap_atr": r6(s_gap / n_both) if n_both else None,
        "mean_roundtrip_toll_atr": r6(s_tol / n_col) if n_col else None,
        "provisional": bool(n_col < PROVISIONAL_MIN_N),
        "provisional_rule": f"n_colocated < {PROVISIONAL_MIN_N}",
    }


def _band_parts(bname: str) -> tuple[int, int, str]:
    """`rvwap_30d_up1` -> (30, 1, 'up').  Parsed rather than carried so the
    name in the table and the name in `build_level_series` cannot drift apart.

    WHAT WOULD MAKE THIS WRONG: a band name whose window is not the second
    token — the parse would silently mislabel the whole column.

    THE GUARD IS TOTAL, AND IT WAS NOT.  The first draft checked the `rvwap`
    prefix and the `d` suffix and then handed the rest to `int()`, so
    `rvwap_XXd_up1` cleared the guard and died inside the parse with
    `ValueError: invalid literal for int()` — and a name with the wrong number
    of tokens died on the unpacking BEFORE the guard ran at all.  Both are the
    failure this HALT exists to name, reported under a different exception and
    without naming the band.  Every rejection now leaves by the same door,
    saying which name and why.  (Unreachable from `band_names()`, which is the
    only producer — which is exactly why it had to be closed by construction
    rather than by argument.)
    """
    parts = bname.split("_")
    if len(parts) != 3:
        raise SystemExit(f"HALT: unparseable band name {bname!r} — expected "
                         f"three _-separated tokens, got {len(parts)}")
    a, b, c = parts
    if a != "rvwap":
        raise SystemExit(f"HALT: unparseable band name {bname!r} — family "
                         f"token {a!r} is not 'rvwap'")
    if not b.endswith("d") or not b[:-1].isdigit():
        raise SystemExit(f"HALT: unparseable band name {bname!r} — window "
                         f"token {b!r} is not `<digits>d`")
    if not c[-1:].isdigit() or not c[:-1]:
        raise SystemExit(f"HALT: unparseable band name {bname!r} — edge token "
                         f"{c!r} is not `<edge><sigma-digit>`")
    return int(b[:-1]), int(c[-1]), c[:-1]


# ═══════════════════════════════ (b) REJECTION, THREE WAYS (AND A FOURTH)
def rejection_by_confluence(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """(b) REJECTION RATE, CO-LOCATED vs WALL-ALONE vs BAND-ALONE — plus the
    band's own co-located arm, and the subtraction done on the row.

    THE TWO WALL ARMS PARTITION ONE APPROACH SET.  The wall is scanned ONCE per
    (asset, wall, side); the SAME approaches are then split by whether the band
    edge was within 0.25 ATR on the approach bar.  Nothing else differs — same
    predicate, same corridor, same ATR, same wall — so
    `rate_wall_colocated_pct - rate_wall_alone_pct` is a difference in one
    variable, which is the only form in which the commission's question has an
    answer.  `n_wall_colocated + n_wall_alone == n_wall_approaches` on EVERY
    row, asserted as a cardinality in `an1_selfcheck`.

    THE BAND ARMS PARTITION THE OTHER SET the same way, so `rate_band_alone_pct`
    is a genuine third rate with its own denominator and not the leftover of
    the first two.

    WHICH LEVEL JUDGES THE REJECTION — reading (6): the WALL judges both wall
    arms, the BAND judges both band arms.  Judging the co-located arm against a
    different level from the wall-alone arm would make the subtraction
    meaningless, and judging it against the wall while calling it a confluence
    result would hide that the band contributed nothing to the verdict; both
    readings are therefore printed, side by side, and neither is chosen.

    THE PANEL ROW POOLS APPROACHES AND REJECTIONS AND RECOMPUTES THE RATE.  A
    mean of five per-asset rates is a different statistic from a pooled rate
    and TIER-C6 has a filed repair saying so.

    n IS THE CO-LOCATED WALL APPROACH COUNT and `provisional` is `n < 30` — the
    co-located arm is the scarce one and it is the one the commission says must
    not lead when it is thin.

    WHAT WOULD MAKE THIS WRONG: re-scanning the wall inside the band loop (the
    two arms would then no longer partition one set); judging the co-located
    arm against the band while judging the alone arm against the wall; pooling
    rates instead of counts; or counting a co-location using the band at a
    DIFFERENT bar from the approach, which is why `coloc` is indexed by the
    approach bar and by nothing else.
    """
    rows: list[dict] = []
    for side in SIDES:
        # EVERY SCAN IS RUN ONCE.  A wall's approach set depends on (asset,
        # wall, side) and a band's on (asset, band, side) — neither depends on
        # the other object — so both are computed before the pairing loop.
        # Re-scanning inside it would be 600 scans where 170 exist, and worse:
        # two scans of the same wall could drift apart and the two arms would
        # stop partitioning ONE approach set, which is the property the whole
        # subtraction rests on.
        span: dict[str, tuple[int, int]] = {}
        for sym in RC.UNIVERSE:
            i0, i1 = _idx_range(frame(sym)["f"].open_ms, lo_ms, hi_ms)
            if i1 >= i0:
                span[sym] = (i0, i1)
        wall_scan: dict[tuple[str, str], tuple] = {}
        for tf, L, _cs in WALLS:
            for sym, (i0, i1) in span.items():
                f = frame(sym)["f"]
                lvl, _own = wall_on_4h(sym, tf, L)
                app, broke = _scan(lvl, f.h, f.l, f.c, atr_4h(sym), side, i0, i1)
                wall_scan[(wall_name(tf, L), sym)] = (lvl, app, broke)
        band_scan: dict[tuple[str, str], tuple] = {}
        for bname in band_names():
            for sym, (i0, i1) in span.items():
                f = frame(sym)["f"]
                band = rvwap_bands(sym)[bname]
                bapp, bbroke = _scan(band, f.h, f.l, f.c, atr_4h(sym), side,
                                     i0, i1)
                band_scan[(bname, sym)] = (band, bapp, bbroke)
        for tf, L, champ_side in WALLS:
            wname = wall_name(tf, L)
            for bname in band_names():
                acc = _zero_acc()
                per_asset = []
                for sym in span:
                    a4 = atr_4h(sym)
                    tl = toll_atr(sym)
                    lvl, app, broke = wall_scan[(wname, sym)]
                    band, bapp, bbroke = band_scan[(bname, sym)]
                    with np.errstate(invalid="ignore"):
                        coloc = (np.isfinite(lvl) & np.isfinite(band)
                                 & np.isfinite(a4)
                                 & (np.abs(lvl - band) <= COLOC_ATR * a4))
                    cell = _arm_counts(app, broke, bapp, bbroke, coloc, tl)
                    for k, v in cell.items():
                        acc[k] += v
                    per_asset.append((sym, cell))
                for sym, cell in per_asset:
                    rows.append(_rej_row(side, tf, L, champ_side, bname, sym,
                                         cell))
                rows.append(_rej_row(side, tf, L, champ_side, bname,
                                     "__PANEL__", acc))
    return _finish(pd.DataFrame(rows), lo_ms, hi_ms, "rejection_by_confluence")


def _zero_acc() -> dict:
    """A zeroed accumulator with the SAME KEYS `_arm_counts` produces, so the
    panel row and the asset rows are shaped by one declaration.

    WHAT WOULD MAKE THIS WRONG: listing the keys a second time here — the two
    lists would drift and a pooled column would silently stop accumulating.
    """
    return {k: 0 if not k.startswith("toll") else 0.0 for k in _ARM_KEYS}


_ARM_KEYS = ("n_wall_app", "n_wall_col", "n_wall_alone",
             "rej_wall_col", "rej_wall_alone",
             "n_band_app", "n_band_col", "n_band_alone",
             "rej_band_col", "rej_band_alone",
             "toll_wall_col", "toll_wall_alone", "toll_band_alone")


def _arm_counts(app, broke, bapp, bbroke, coloc, tl) -> dict:
    """The five arm counts and their tolls for ONE asset.

    REJECTION IS `approach AND NOT broke`, exactly TIER-C6's
    `if broke: ... else: nrej += 1`.

    WHAT WOULD MAKE THIS WRONG: defining rejection as `not broke` without the
    approach conjunct (every quiet bar in the corridor would become a
    rejection), or reading `coloc` at a bar other than the approach bar.
    """
    wc, wa = app & coloc, app & ~coloc
    bc, ba = bapp & coloc, bapp & ~coloc
    return {
        "n_wall_app": int(app.sum()),
        "n_wall_col": int(wc.sum()), "n_wall_alone": int(wa.sum()),
        "rej_wall_col": int((wc & ~broke).sum()),
        "rej_wall_alone": int((wa & ~broke).sum()),
        "n_band_app": int(bapp.sum()),
        "n_band_col": int(bc.sum()), "n_band_alone": int(ba.sum()),
        "rej_band_col": int((bc & ~bbroke).sum()),
        "rej_band_alone": int((ba & ~bbroke).sum()),
        "toll_wall_col": float(np.nansum(tl[wc])),
        "toll_wall_alone": float(np.nansum(tl[wa])),
        "toll_band_alone": float(np.nansum(tl[ba])),
    }


def _rej_row(side, tf, L, champ_side, bname, sym, c) -> dict:
    """One cell of (b).  Per-asset and pooled rows share this code path, so a
    panel row cannot be built by different arithmetic from the asset rows it
    claims to summarise.

    WHAT WOULD MAKE THIS WRONG: computing the delta from ROUNDED rates when
    either is None (it would read 0.0 and a missing arm would look like a tie);
    dividing a toll by an arm's count when that count is zero; or setting
    `may_lead` on a per-asset row, which would invite a five-trade cell to be
    quoted as the finding.
    """
    wd, sig, ud = _band_parts(bname)
    rc = pct(c["rej_wall_col"], c["n_wall_col"])
    ra = pct(c["rej_wall_alone"], c["n_wall_alone"])
    return {
        "side": side, "asset": sym,
        "wall": wall_name(tf, L), "wall_tf": tf, "wall_ema": int(L),
        "wall_champion_side": champ_side,
        "is_commissioned_side": bool(side == champ_side),
        "band": bname, "band_window_days": wd, "band_sigma": sig,
        "band_edge": ud,
        "band_edge_natural_side": ("resistance" if ud == "up" else "support"),
        # ── the three rates the commission asked for, side by side ────────
        "rate_wall_colocated_pct": rc,
        "rate_wall_alone_pct": ra,
        "rate_band_alone_pct": pct(c["rej_band_alone"], c["n_band_alone"]),
        # ── and the fourth, reading (6) ───────────────────────────────────
        "rate_band_colocated_pct": pct(c["rej_band_col"], c["n_band_col"]),
        "rejection_rate_delta_coloc_minus_alone_pp": (
            r4(rc - ra) if (rc is not None and ra is not None) else None),
        "rejection_judged_against": (
            "the WALL in both wall arms; the BAND in both band arms "
            "[reading 6]"),
        # ── the populations ───────────────────────────────────────────────
        "n_wall_approaches": int(c["n_wall_app"]),
        "n_wall_colocated": int(c["n_wall_col"]),
        "n_wall_alone": int(c["n_wall_alone"]),
        "n_band_approaches": int(c["n_band_app"]),
        "n_band_colocated": int(c["n_band_col"]),
        "n_band_alone": int(c["n_band_alone"]),
        "rejections_wall_colocated": int(c["rej_wall_col"]),
        "rejections_wall_alone": int(c["rej_wall_alone"]),
        "rejections_band_colocated": int(c["rej_band_col"]),
        "rejections_band_alone": int(c["rej_band_alone"]),
        "n": int(c["n_wall_col"]),
        # ── the toll (c) ──────────────────────────────────────────────────
        "toll_atr_colocated": (r6(c["toll_wall_col"] / c["n_wall_col"])
                               if c["n_wall_col"] else None),
        "toll_atr_wall_alone": (r6(c["toll_wall_alone"] / c["n_wall_alone"])
                                if c["n_wall_alone"] else None),
        "toll_atr_band_alone": (r6(c["toll_band_alone"] / c["n_band_alone"])
                                if c["n_band_alone"] else None),
        "toll_basis": (f"round trip = 2 x FEE_BPS_SIDE ({FEE_BPS_SIDE} bps) of "
                       f"notional, expressed in 4h ATR at the approach bar; "
                       f"no funding — an approach is a bar, not a position"),
        "provisional": bool(c["n_wall_col"] < PROVISIONAL_MIN_N),
        "provisional_rule": f"n_wall_colocated < {PROVISIONAL_MIN_N}",
        "may_lead": bool(c["n_wall_col"] >= PROVISIONAL_MIN_N
                         and sym == "__PANEL__"),
    }


# ═══════════════════════════════════════════════════════════ F-AN-1 · THE FIXTURE
def _hand_ema(vals: np.ndarray, length: int) -> float:
    """A LITERAL EMA recursion written out here, seeded at the first value.

    Not `ind.ema`.  The point of a hand-verification is to walk the arithmetic
    by a route the program did not take; calling the program's own primitive
    and comparing would be re-deriving a value the way the program derived it
    and comparing it to itself, which this estate forbids by name.

    WHAT WOULD MAKE THIS WRONG: seeding with an SMA of the first `length` bars
    (a different and arguably better EMA, but not the one the estate's engine
    computes for Pine parity), or using a different alpha.
    """
    a = 2.0 / (float(length) + 1.0)
    e = float(vals[0])
    for v in vals[1:]:
        e = e + a * (float(v) - e)
    return e


def _hand_atr(h: np.ndarray, l: np.ndarray, c: np.ndarray, length: int,
              upto: int) -> float:
    """A LITERAL Wilder RMA of true range, walked bar by bar to `upto`.

    Not `ind.atr`.  Wilder's alpha is 1/length, seeded on the first true
    range, and the first bar's true range is `high - low` because there is no
    previous close — the engine's own convention, transcribed rather than
    called.

    WHAT WOULD MAKE THIS WRONG: alpha = 2/(n+1) (that is an EMA, not Wilder);
    seeding on an SMA of the first `length` true ranges; or starting the walk
    at a bar other than 0, which would seed the recursion somewhere the
    program did not.
    """
    a = 1.0 / float(length)
    prev = np.nan
    r = np.nan
    for i in range(0, upto + 1):
        if i == 0:
            tr = float(h[0]) - float(l[0])
        else:
            pc = float(c[i - 1])
            tr = max(float(h[i]) - float(l[i]), abs(float(h[i]) - pc),
                     abs(float(l[i]) - pc))
        prev = tr if not np.isfinite(prev) else prev + a * (tr - prev)
        r = prev
    return float(r)


def _hand_rvwap_band(ot, src, vol, i: int, window_days: int, sigma: int,
                     up: bool) -> float:
    """A LITERAL volume-weighted mean and population sigma over the raw window.

    Membership is `t > t[i] - W` and `t <= t[i]`, transcribed from
    `analytics/vwap.py:232` — the current bar is IN, the bar exactly W old is
    OUT.  Written as an explicit sum so the fixture does not call the estate's
    accumulator and compare it to itself.

    WHAT WOULD MAKE THIS WRONG: `>=` on the lower edge of the window (the bar
    exactly one window old would join, and every band value would differ in
    the sixth decimal for a reason nobody could find); a SAMPLE rather than a
    POPULATION variance; or weighting by bar count instead of by volume.
    """
    w = int(window_days) * AW.DAY_MS
    sv = v = sv2 = 0.0
    for j in range(0, i + 1):
        if not (ot[j] > ot[i] - w):
            continue
        s_, v_ = float(src[j]), float(vol[j])
        sv += s_ * v_
        v += v_
        sv2 += v_ * s_ * s_
    m = sv / v
    sd = float(np.sqrt(max(sv2 / v - m * m, 0.0)))
    return m + (sigma * sd if up else -sigma * sd)


def _chk(name: str, ok: bool, detail: str, kind: str = "cardinality") -> dict:
    """One fixture row.  `detail` carries the EVIDENCE, not a restatement of
    the name, because a green check whose detail says only "ok" is a check
    nobody can audit after the fact.

    WHAT WOULD MAKE THIS WRONG: coercing a numpy bool without `bool()` (it
    would serialise as a numpy scalar and compare oddly downstream), or a
    detail string that omits the CARDINALITY the check actually ranged over.
    """
    return {"check": name, "kind": kind, "pass": bool(ok), "detail": detail}


def an1_selfcheck() -> pd.DataFrame:
    """F-AN-1.  THREE hand-verifications from raw bars — one co-location, one
    rejection, one toll — plus the cardinality assertions that make the rest of
    the module checkable rather than merely demonstrated.

    IT RETURNS A TABLE AND DOES NOT RAISE.  A TIER-E measurement that gates
    nothing must not be able to halt the estate; a failure is a False in the
    `pass` column and the caller decides what to do about it.

    WHAT WOULD MAKE THIS WRONG: a hand-verification that calls the function
    under test (it would compare a value to itself); a cardinality check that
    is satisfied by one example; or a look-ahead check that inspects the code
    rather than rebuilding the series from truncated bars.
    """
    lo, hi, meta = corridor()
    out: list[dict] = []
    conf = confluence_table(lo, hi)
    rej = rejection_by_confluence(lo, hi)

    # ─────────────────────────────────────────── REUSE FIDELITY, EXACTLY
    bad = []
    for sym in RC.UNIVERSE:
        ref = Q.champion_series(sym)
        for tf, L in Q.CHAMPIONS:
            mine = _wall_series_one(sym, tf, L)
            r = ref[f"{tf}_ema{L}"]
            same = (np.array_equal(mine["close_ms"], r["close_ms"])
                    and np.array_equal(mine["ema"], r["ema"], equal_nan=True)
                    and np.array_equal(mine["atr"], r["atr"], equal_nan=True))
            if not same:
                bad.append(f"{sym}/{tf}/{L}")
    out.append(_chk(
        "wall builder IS tierc5q.champion_series",
        not bad,
        f"{len(RC.UNIVERSE) * len(Q.CHAMPIONS)} (asset, champion) series "
        f"compared element-for-element, no tolerance; mismatches={bad}"))

    bad = []
    for sym in RC.UNIVERSE:
        f = frame(sym)["f"]
        cols = Q.champion_cols(Q.champion_series(sym), f.c, f.open_ms)
        for tf, L in Q.CHAMPIONS:
            mine, _own = wall_on_4h(sym, tf, L)
            ref = np.array([np.nan if v is None else v
                            for v in cols[f"champ_{tf}_ema{L}"]], float)
            mr = np.array([np.nan if v is None else v for v in
                           [r6(x) for x in mine]], float)
            if not np.array_equal(mr, ref, equal_nan=True):
                bad.append(f"{sym}/{tf}/{L}")
    out.append(_chk(
        "as-of read IS tierc5q.champion_cols",
        not bad,
        f"r6 of `wall_on_4h` vs the `champ_*` column, all "
        f"{len(RC.UNIVERSE) * len(Q.CHAMPIONS)} pairs, every bar; "
        f"mismatches={bad}"))

    sym0 = RC.UNIVERSE[0]
    ref_r = TB.build_level_series(frame(sym0)["k4"])["rvwap"]
    k4 = frame(sym0)["k4"]
    ot0 = k4["open_time"].to_numpy(np.int64)
    bad = []
    for bname in band_names():
        wd, sig, ud = _band_parts(bname)
        mine = rvwap_bands(sym0)[bname]
        ref = np.asarray(ref_r[f"rvwap_{wd}d_{ud}{sig}"], float)
        warm = np.isfinite(mine)
        if not np.array_equal(mine[warm], ref[warm]):
            bad.append(bname)
    out.append(_chk(
        "RVWAP bands ARE build_level_series' bands",
        not bad,
        f"{len(band_names())} edges on {sym0}, every WARM bar, exact float "
        f"equality against tierc2_baseline.build_level_series; diffs={bad}"))

    # ── THE OTHER ESTATE BUILDER, AND THE DIVERGENCE PUBLISHED RATHER THAN
    # ── QUIETLY PREFERRED.  TIER-C6's `wall_series_12h` builds the SAME
    # 12h/889 wall in the DECISION PATH — bucketed out of raw 4h bars, because
    # a decision may not consult `analytics`.  This module is TIER-E and uses
    # TIER-C5-Q's own-clock construction instead.  The two agree on the thing
    # that matters structurally — WHICH BARS ARE WARM, bar for bar — and
    # disagree slightly on the LEVEL, because `ind.ema` seeds at each series'
    # own first bar and the two series start in different places.  The size of
    # that disagreement is measured and printed here, so a reader knows the
    # choice of builder is worth a fraction of a percent and knows which
    # fraction.
    cov_bad, div = [], 0.0
    for sym in RC.UNIVERSE:
        f = frame(sym)["f"]
        a = V6.wall_series_12h(f.open_ms, f.h, f.l, f.c, 889)[0]
        b = wall_on_4h(sym, "12h", 889)[0]
        if not np.array_equal(np.isfinite(a), np.isfinite(b)):
            cov_bad.append(sym)
        both = np.isfinite(a) & np.isfinite(b)
        if both.any():
            div = max(div, float(np.max(np.abs(a[both] - b[both])
                                        / np.abs(b[both]))))
    out.append(_chk(
        "the two estate 12h-wall builders agree on WARMTH, and their level "
        "divergence is published",
        (not cov_bad) and div < 0.01,
        f"tierc6_rules.wall_series_12h (decision path, bucketed from 4h bars) "
        f"vs tierc5q's own-clock construction, {len(RC.UNIVERSE)} assets: "
        f"identical finite/NaN masks bar for bar (mismatches={cov_bad}); "
        f"max relative level divergence {div * 100:.4f}% — the EMA seed, not "
        f"the as-of. AN-1 uses the own-clock builder because it is the only "
        f"one of the two that generalises to 1h, 4h and 1d"))

    # ──────────────────────────────────────────────── WARM-UP FLOORS
    bad = []
    for sym in RC.UNIVERSE:
        for tf, L, _s in WALLS:
            s = _wall_series_one(sym, tf, L)
            lvl, own = wall_on_4h(sym, tf, L)
            as_of = frame(sym)["f"].open_ms + MS_4H
            k = np.searchsorted(s["close_ms"], as_of, "right") - 1
            leak = int((np.isfinite(lvl) & (k < int(L))).sum())
            leak += int((np.isfinite(own) & (k < int(L))).sum())
            if leak:
                bad.append(f"{sym}/{tf}/{L}:{leak}")
    out.append(_chk(
        "wall warm-up floor holds",
        not bad,
        f"{len(RC.UNIVERSE) * len(WALLS)} (asset, wall) series: zero finite "
        f"values at any 4h bar whose own-clock index k < L; leaks={bad}"))

    bad = []
    for sym in RC.UNIVERSE:
        ot = frame(sym)["f"].open_ms
        for bname in band_names():
            wd, _sig, _ud = _band_parts(bname)
            v = rvwap_bands(sym)[bname]
            leak = int((np.isfinite(v)
                        & ((ot - ot[0]) < int(wd) * AW.DAY_MS)).sum())
            if leak:
                bad.append(f"{sym}/{bname}:{leak}")
    out.append(_chk(
        "RVWAP band warm-up floor holds",
        not bad,
        f"{len(RC.UNIVERSE) * len(band_names())} (asset, band) series: zero "
        f"finite values before the trailing window is fully spanned — the "
        f"MIN_BARS={AW.MIN_BARS} short-window floor in analytics.vwap is "
        f"neutralised; leaks={bad}"))

    binding = []
    for sym in RC.UNIVERSE:
        a = atr_4h(sym)
        earliest = min(
            [int(np.argmax(np.isfinite(rvwap_bands(sym)[b])))
             for b in band_names()]
            + [int(np.argmax(np.isfinite(wall_on_4h(sym, tf, L)[0])))
               for tf, L, _s in WALLS])
        if earliest < ATR_LEN:
            binding.append(f"{sym}:{earliest}")
    out.append(_chk(
        "4h ATR floor is inert on this corridor",
        not binding,
        f"the earliest warm bar of ANY wall or band on each asset is at or "
        f"after index {ATR_LEN}, so the ATR floor removes no cell it did not "
        f"already lose; binding on={binding}"))

    # ─────────────────────────────────────────── NO LOOK-AHEAD, BY TRUNCATION
    bad = []
    tested = 0
    for sym in RC.UNIVERSE[:3]:
        f = frame(sym)["f"]
        k4s = frame(sym)["k4"]
        n = len(f.c)
        for j in (int(n * 0.55), int(n * 0.8), n - 1):
            # the wall, rebuilt from raw bars TRUNCATED AT j
            for tf, L in (("12h", 889), ("1d", 889)):
                d = T5._tf_frame(sym, tf)
                step = MS_12H if tf == "12h" else MS_1D
                keep = (d["t"] + step) <= (f.open_ms[j] + MS_4H)
                if keep.sum() <= L:
                    continue
                e = ind.ema(d["c"][keep], L)[-1]
                got = wall_on_4h(sym, tf, L)[0][j]
                tested += 1
                if not (np.isfinite(got) and abs(e - got) <= 1e-9 * max(1.0, abs(e))):
                    bad.append(f"{sym}/{tf}/{L}@{j}")
            # the band, rebuilt from raw bars TRUNCATED AT j
            ot = k4s["open_time"].to_numpy(np.int64)[:j + 1]
            src = ((k4s["high"].to_numpy(float) + k4s["low"].to_numpy(float)
                    + k4s["close"].to_numpy(float)) / 3.0)[:j + 1]
            vol = k4s["volume"].to_numpy(float)[:j + 1]
            r = AW.rolling_vwap(ot, src, vol, window_days=30, sigmas=(1,))
            got = rvwap_bands(sym)["rvwap_30d_up1"][j]
            tested += 1
            end = float(r["band_up_1"][-1])
            if not (np.isfinite(got)
                    and abs(end - got) <= 1e-9 * max(1.0, abs(got))):
                bad.append(f"{sym}/rvwap_30d_up1@{j}")
    out.append(_chk(
        "NO LOOK-AHEAD — truncated rebuild reproduces the endpoint",
        not bad,
        f"{tested} (asset, series, bar) endpoints rebuilt from bars <= j only "
        f"and compared to the full-history series at j; misses={bad}",
        kind="causality"))

    # ────────────────────────────────────────── CARDINALITY OVER THE GRID
    p = rej
    ok_wall = bool(((p["n_wall_colocated"] + p["n_wall_alone"])
                    == p["n_wall_approaches"]).all())
    ok_band = bool(((p["n_band_colocated"] + p["n_band_alone"])
                    == p["n_band_approaches"]).all())
    out.append(_chk(
        "the two wall arms PARTITION the wall approaches",
        ok_wall,
        f"n_wall_colocated + n_wall_alone == n_wall_approaches on all "
        f"{len(p)} rows"))
    out.append(_chk(
        "the two band arms PARTITION the band approaches",
        ok_band,
        f"n_band_colocated + n_band_alone == n_band_approaches on all "
        f"{len(p)} rows"))

    ok_rej = bool((
        (p["rejections_wall_colocated"] <= p["n_wall_colocated"])
        & (p["rejections_wall_alone"] <= p["n_wall_alone"])
        & (p["rejections_band_colocated"] <= p["n_band_colocated"])
        & (p["rejections_band_alone"] <= p["n_band_alone"])).all())
    out.append(_chk("no arm rejects more than it approached", ok_rej,
                    f"four inequalities on all {len(p)} rows"))

    rate_cols = ["rate_wall_colocated_pct", "rate_wall_alone_pct",
                 "rate_band_alone_pct", "rate_band_colocated_pct"]
    bad_rate = []
    for cname in rate_cols:
        v = p[cname].astype(float)
        m = v.notna()
        if not bool(((v[m] >= 0.0) & (v[m] <= 100.0)).all()):
            bad_rate.append(cname)
    for cname in ("coloc_share_pct", "coloc_share_on_side_pct",
                  "coloc_share_own_clock_atr_pct"):
        v = conf[cname].astype(float)
        m = v.notna()
        if not bool(((v[m] >= 0.0) & (v[m] <= 100.0)).all()):
            bad_rate.append(cname)
    out.append(_chk("every rate and share lies in [0, 100]", not bad_rate,
                    f"7 columns across {len(p)} + {len(conf)} rows; "
                    f"out of range={bad_rate}"))

    # the panel row IS the pooled asset rows — on every cell, not one
    keys = ["side", "wall", "band"]
    cnt = ["n_wall_approaches", "n_wall_colocated", "n_wall_alone",
           "n_band_approaches", "n_band_colocated", "n_band_alone",
           "rejections_wall_colocated", "rejections_wall_alone",
           "rejections_band_colocated", "rejections_band_alone"]
    asset_sum = (p[p["asset"] != "__PANEL__"].groupby(keys)[cnt].sum()
                 .reset_index())
    panel = p[p["asset"] == "__PANEL__"][keys + cnt].reset_index(drop=True)
    mg = panel.merge(asset_sum, on=keys, suffixes=("_p", "_a"))
    ok_panel = (len(mg) == len(panel)) and all(
        bool((mg[f"{c}_p"] == mg[f"{c}_a"]).all()) for c in cnt)
    out.append(_chk("every panel row == the pooled asset rows", ok_panel,
                    f"{len(panel)} panel cells x {len(cnt)} counts, exact"))

    ccnt = ["n_bars_both_warm", "n_bars_side_eligible", "n_colocated",
            "n_colocated_on_side"]
    a_sum = (conf[conf["asset"] != "__PANEL__"].groupby(keys)[ccnt].sum()
             .reset_index())
    c_panel = conf[conf["asset"] == "__PANEL__"][keys + ccnt].reset_index(drop=True)
    mg2 = c_panel.merge(a_sum, on=keys, suffixes=("_p", "_a"))
    ok_cpanel = (len(mg2) == len(c_panel)) and all(
        bool((mg2[f"{c}_p"] == mg2[f"{c}_a"]).all()) for c in ccnt)
    out.append(_chk("every confluence panel row == the pooled asset rows",
                    ok_cpanel, f"{len(c_panel)} panel cells x {len(ccnt)} counts"))

    ok_col = bool((conf["n_colocated"] <= conf["n_bars_both_warm"]).all()
                  and (conf["n_colocated_on_side"] <= conf["n_colocated"]).all()
                  and (conf["n_bars_both_warm"] <= conf["n_bars_scanned"]).all())
    out.append(_chk("co-location counts nest inside their denominators", ok_col,
                    f"three inequalities on all {len(conf)} rows"))

    # the grid is WHOLE and its shape is the declared shape
    want = len(SIDES) * len(WALLS) * len(band_names()) * (len(RC.UNIVERSE) + 1)
    out.append(_chk("the grid is reported WHOLE",
                    len(conf) == want and len(rej) == want,
                    f"expected {want} rows = {len(SIDES)} sides x {len(WALLS)} "
                    f"walls x {len(band_names())} band edges x "
                    f"({len(RC.UNIVERSE)} assets + panel); "
                    f"got confluence={len(conf)} rejection={len(rej)}"))

    # the disclosure obligations, on every row of every table
    ok_disc = True
    for d in (conf, rej):
        ok_disc &= ("selection_not_a_result" in d.columns
                    and bool(d["selection_not_a_result"]
                             .str.startswith("a SELECTION, not a result").all())
                    and bool(d["gates_nothing"].all())
                    and "m_selection_surface" in d.columns
                    and "as_of_last_closed_4h" in d.columns
                    and bool((d["m_selection_surface"] == len(d)).all()))
    out.append(_chk("every row of every table carries the disclosure", ok_disc,
                    "selection_not_a_result / gates_nothing / "
                    "m_selection_surface / as_of stamp, on all rows"))

    # the SUPPORT predicate is the genuine mirror of the RESISTANCE one
    sym = RC.UNIVERSE[0]
    f = frame(sym)["f"]
    i0, i1 = _idx_range(f.open_ms, lo, hi)
    lvl, _ = wall_on_4h(sym, "12h", 889)
    a4 = atr_4h(sym)
    ar, br = _scan(lvl, f.h, f.l, f.c, a4, "resistance", i0, i1)
    am, bm = _scan(-lvl, -f.l, -f.h, -f.c, a4, "support", i0, i1)
    out.append(_chk("support IS the mirror of resistance",
                    bool(np.array_equal(ar, am) and np.array_equal(br, bm)),
                    f"the support scan on a NEGATED series (high/low swapped) "
                    f"reproduces the resistance scan bar for bar over "
                    f"{int(ar.sum())} approaches",
                    kind="mirror"))

    out.extend(_hand_verifications(lo, hi, rej))
    d = pd.DataFrame(out)
    d["fixture"] = "F-AN-1"
    d["gates_nothing"] = True
    d["selection_not_a_result"] = SELECTION_NOTE
    d["m_selection_surface"] = len(d)
    log(f"  AN-1 F-AN-1: {int(d['pass'].sum())}/{len(d)} checks pass · "
        f"m = {len(d)} cells in this selection surface — a SELECTION, not a "
        f"result; it gates nothing")
    return T8.stamp(d, _meta_for(lo, hi))


def _hand_verifications(lo: int, hi: int, rej: pd.DataFrame) -> list[dict]:
    """THE THREE HAND-WALKS, FROM RAW PARQUET BARS.

    Each one picks a REAL, NAMED bar out of the corridor, re-derives every
    ingredient by arithmetic written out above — a literal EMA recursion, a
    literal Wilder RMA, a literal volume-weighted sum — and re-takes the
    verdict by hand.  Nothing here calls `wall_on_4h`, `rvwap_bands`, `atr_4h`
    or `_scan` to PRODUCE the number it checks; those are called only to say
    what the program claimed, so the comparison is between two routes and not
    between a value and itself.

    WHAT WOULD MAKE THIS WRONG: choosing the bar by searching for one where the
    hand and the program already agree.  The bar is the FIRST qualifying one in
    the corridor on a fixed asset and a fixed cell, so the choice cannot be
    tuned.
    """
    res: list[dict] = []
    sym = "BTCUSDT"
    tf, L, bname = "12h", 889, "rvwap_30d_up1"
    f = frame(sym)["f"]
    k4 = frame(sym)["k4"]
    ot = k4["open_time"].to_numpy(np.int64)
    hh = k4["high"].to_numpy(float)
    ll = k4["low"].to_numpy(float)
    cc = k4["close"].to_numpy(float)
    vv = k4["volume"].to_numpy(float)
    src = (hh + ll + cc) / 3.0
    i0, i1 = _idx_range(f.open_ms, lo, hi)
    lvl, _own = wall_on_4h(sym, tf, L)
    band = rvwap_bands(sym)[bname]
    a4 = atr_4h(sym)

    with np.errstate(invalid="ignore"):
        coloc = (np.isfinite(lvl) & np.isfinite(band) & np.isfinite(a4)
                 & (np.abs(lvl - band) <= COLOC_ATR * a4))
    idx = np.arange(len(cc))
    inwin = (idx >= max(i0, 1)) & (idx <= i1)

    # ── raw 12h bars, read straight off the cache, for the hand EMA ──────
    d12 = load_klines(sym, tf)
    t12 = d12["open_time"].to_numpy(np.int64)
    c12 = d12["close"].to_numpy(float)

    def hand_wall(j: int) -> float:
        """The wall a reader standing at bar j's CLOSE could see, walked by
        hand: keep every raw 12h bar whose OWN close is at or before that
        instant, then run the literal EMA recursion over their closes.

        WHAT WOULD MAKE THIS WRONG: keeping bars by OPEN time (the forming 12h
        bar would join and the hand value would contain the future); dropping
        the `k < L` floor (an unwarm EMA would be compared to a NaN and the
        check would pass by both sides being absent); or reading the cache's
        12h file through the resampler, which is a second series and not the
        raw bars this walk is supposed to start from.
        """
        as_of = int(ot[j]) + MS_4H
        keep = (t12 + MS_12H) <= as_of
        k = int(keep.sum()) - 1
        if k < L:
            return float("nan")
        return _hand_ema(c12[:k + 1], L)

    # ══════════════════════════════════ HAND-1 · ONE CO-LOCATION
    cand = np.flatnonzero(coloc & inwin)
    if len(cand):
        j = int(cand[0])
        hw = hand_wall(j)
        hb = _hand_rvwap_band(ot, src, vv, j, 30, 1, up=True)
        ha = _hand_atr(hh, ll, cc, ATR_LEN, j)
        verdict = abs(hw - hb) <= COLOC_ATR * ha
        agree = (abs(hw - float(lvl[j])) <= 1e-9 * max(1.0, abs(hw))
                 and abs(hb - float(band[j])) <= 1e-9 * max(1.0, abs(hb))
                 and abs(ha - float(a4[j])) <= 1e-9 * max(1.0, abs(ha))
                 and bool(verdict) is True)
        res.append(_chk(
            "HAND-CO-LOCATION — one bar walked from raw bars",
            agree,
            f"{sym} {iso(int(ot[j]))} bar {j}: hand 12h/889 EMA "
            f"{hw:.6f} (program {float(lvl[j]):.6f}); hand {bname} "
            f"{hb:.6f} (program {float(band[j]):.6f}); hand 4h ATR "
            f"{ha:.6f} (program {float(a4[j]):.6f}); |gap| "
            f"{abs(hw - hb):.6f} <= 0.25 ATR = {COLOC_ATR * ha:.6f} -> "
            f"CO-LOCATED, and the program says "
            f"{bool(coloc[j])}",
            kind="hand"))
    else:
        res.append(_chk("HAND-CO-LOCATION — one bar walked from raw bars",
                        False, "no co-located bar found to walk", kind="hand"))

    # ══════════════════════ HAND-1b · THE SAME WALK, SPREAD OVER THE CORRIDOR
    # ONE HAND-WALK IS AN ANECDOTE.  The commission asks for one co-location
    # verified from raw bars and it is verified above, by name and by date —
    # but a single bar can agree with a BROKEN as-of by coincidence: two of
    # every three 4h bars inside a 12h bucket see the same 12h bar under the
    # correct convention AND under the discredited as-of-OPEN one.  So the
    # identical hand walk is repeated at 25 bars spread evenly across the
    # corridor, which no coincidence survives.
    warm = np.flatnonzero(np.isfinite(lvl) & inwin)
    spread = warm[np.linspace(0, len(warm) - 1, 25).astype(int)] if len(warm) else []
    bad_spread = []
    for j in spread:
        j = int(j)
        hw = hand_wall(j)
        if not (np.isfinite(hw)
                and abs(hw - float(lvl[j])) <= 1e-9 * max(1.0, abs(hw))):
            bad_spread.append(iso(int(ot[j])))
    res.append(_chk(
        "HAND-CO-LOCATION, spread — 25 walls hand-walked across the corridor",
        len(spread) > 0 and not bad_spread,
        f"{sym} {tf}/{L}: the literal EMA recursion over raw 12h closes "
        f"knowable at each 4h bar's CLOSE, at {len(spread)} bars evenly "
        f"spaced from {iso(int(ot[int(spread[0])])) if len(spread) else '-'} "
        f"to {iso(int(ot[int(spread[-1])])) if len(spread) else '-'}; "
        f"disagreements={bad_spread}",
        kind="hand"))

    # ══════════════════════════════════ HAND-2 · ONE REJECTION
    app, broke = _scan(lvl, f.h, f.l, f.c, a4, "resistance", i0, i1)
    cand = np.flatnonzero(app & coloc & ~broke)
    if len(cand):
        j = int(cand[0])
        hw_prev, hw_j = hand_wall(j - 1), hand_wall(j)
        ha = _hand_atr(hh, ll, cc, ATR_LEN, j)
        prev_below = float(cc[j - 1]) < hw_prev
        reached = float(hh[j]) >= hw_j - APPROACH_ATR * ha
        closes = []
        thru_any = False
        for s in range(0, RESOLVE_BARS + 1):
            k = j + s
            if k > i1:
                break
            wk = hand_wall(k)
            closes.append((iso(int(ot[k])), float(cc[k]), wk))
            if float(cc[k]) > wk:
                thru_any = True
        hand_rejected = prev_below and reached and not thru_any
        agree = bool(hand_rejected) and bool(app[j]) and not bool(broke[j])
        res.append(_chk(
            "HAND-REJECTION — one co-located approach walked from raw bars",
            agree,
            f"{sym} {iso(int(ot[j]))} bar {j}: prev close {float(cc[j-1]):.4f} "
            f"< prev hand wall {hw_prev:.4f} = {prev_below}; high "
            f"{float(hh[j]):.4f} >= wall {hw_j:.4f} - 0.25 ATR "
            f"({APPROACH_ATR * ha:.4f}) = {reached}; resolve window closes vs "
            f"the wall AT EACH BAR " +
            "; ".join(f"{t}: {c_:.4f} vs {w:.4f}" for t, c_, w in closes) +
            f" -> no close through = {not thru_any}; HAND VERDICT REJECTED, "
            f"program approach={bool(app[j])} broke={bool(broke[j])}",
            kind="hand"))
    else:
        res.append(_chk(
            "HAND-REJECTION — one co-located approach walked from raw bars",
            False, "no co-located rejected approach found to walk", kind="hand"))

    # ══════════════ HAND-2b · THE RESOLVE WINDOW READS A MOVING LEVEL
    # TIER-C6 writes `seg = c[w] - e[w]` — the close of each bar in the resolve
    # window is compared to THE LEVEL AT THAT BAR.  Freezing the level at the
    # approach bar is the natural mis-transcription and it is a DIFFERENT rule.
    #
    # AND THE FIRST THING THIS CHECK LEARNED IS WORTH PRINTING: on the WALLS
    # the two readings NEVER disagree.  A 889-period EMA on 12h bars moves a
    # fraction of a point across a 12-hour resolve window, so a close that is
    # through the moving wall is through the frozen one.  A check run there
    # would have been VACUOUS and would have passed for no reason.  It is run
    # on a BAND instead — the 7-day +2σ RVWAP edge moves with every bar — where
    # the distinction is live, and the wall's zero is reported beside it rather
    # than quietly relied upon.
    def _frozen_broke(level, n_):
        fz = np.zeros(n_, bool)
        ix = np.arange(n_)
        for s_ in range(0, RESOLVE_BARS + 1):
            k = ix + s_
            ok_k = k <= i1
            th = np.zeros(n_, bool)
            with np.errstate(invalid="ignore"):
                th[ok_k] = cc[k[ok_k]] > level[ok_k]
            fz |= th & np.isfinite(level)
        return fz

    n_bars = len(cc)
    app_w, broke_w = _scan(lvl, f.h, f.l, f.c, a4, "resistance", i0, i1)
    differ_w = int((app_w & (_frozen_broke(lvl, n_bars) != broke_w)).sum())
    fast = "rvwap_7d_up2"
    fb = rvwap_bands(sym)[fast]
    app_b, broke_b = _scan(fb, f.h, f.l, f.c, a4, "resistance", i0, i1)
    frz_b = _frozen_broke(fb, n_bars)
    differ = np.flatnonzero(app_b & (frz_b != broke_b))
    if len(differ):
        j = int(differ[0])
        hand_thru = False
        walk = []
        for s_ in range(0, RESOLVE_BARS + 1):
            k = j + s_
            if k > i1:
                break
            wk = _hand_rvwap_band(ot, src, vv, k, 7, 2, up=True)
            walk.append(f"{iso(int(ot[k]))}: close {float(cc[k]):.2f} vs "
                        f"moving edge {wk:.2f} (frozen {float(fb[j]):.2f})")
            if float(cc[k]) > wk:
                hand_thru = True
        res.append(_chk(
            "HAND-RESOLVE — the window reads the level AT EACH BAR, not frozen",
            (bool(hand_thru) == bool(broke_b[j])
             and bool(frz_b[j]) != bool(broke_b[j])),
            f"{sym} {fast}: the moving and frozen readings disagree on "
            f"{len(differ)} of {int(app_b.sum())} approaches — the choice is "
            f"LIVE — while on the 12h/889 wall they disagree on {differ_w} of "
            f"{int(app_w.sum())}, which is why this walk is run on the band. "
            f"First disagreeing approach {iso(int(ot[j]))}: " +
            "; ".join(walk) + f" -> hand (moving) broke={hand_thru}, program "
            f"broke={bool(broke_b[j])}, the frozen reading would have said "
            f"{bool(frz_b[j])}",
            kind="hand"))
    else:
        res.append(_chk(
            "HAND-RESOLVE — the window reads the level AT EACH BAR, not frozen",
            False,
            "the moving and frozen readings never disagree on this corridor, "
            "so this check is vacuous and is reported as a FAILURE rather "
            "than as a pass nobody earned", kind="hand"))

    # ══════════════════════════════════ HAND-3 · ONE TOLL
    jj = int(np.flatnonzero(inwin & np.isfinite(a4))[0])
    ha = _hand_atr(hh, ll, cc, ATR_LEN, jj)
    hand_toll = (2.0 * FEE_BPS_SIDE / 10_000.0) * float(cc[jj]) / ha
    prog_toll = float(toll_atr(sym)[jj])
    ok = abs(hand_toll - prog_toll) <= 1e-9 * max(1.0, abs(hand_toll))
    res.append(_chk(
        "HAND-TOLL — one bar's round-trip toll from raw bars",
        ok,
        f"{sym} {iso(int(ot[jj]))} bar {jj}: 2 x {FEE_BPS_SIDE} bps = "
        f"{2 * FEE_BPS_SIDE / 10_000.0:.6f} of notional; close "
        f"{float(cc[jj]):.4f} / hand 4h ATR {ha:.6f} -> toll "
        f"{hand_toll:.8f} ATR; program {prog_toll:.8f} ATR",
        kind="hand"))

    # and the toll actually printed on a row is the mean over that arm's bars
    r0 = rej[(rej["asset"] == "__PANEL__") & (rej["n_wall_alone"] > 0)]
    if len(r0):
        row = r0.iloc[0]
        res.append(_chk(
            "the printed toll is a MEAN over the arm's own bars",
            row["toll_atr_wall_alone"] is not None,
            f"{row['side']}/{row['wall']}/{row['band']} wall-alone arm: "
            f"n={int(row['n_wall_alone'])}, mean toll "
            f"{row['toll_atr_wall_alone']} ATR round trip",
            kind="hand"))
    return res


def main() -> int:                                     # pragma: no cover
    """No writes at import; the driver is explicit and prints, it does not file.

    AN-1 files nothing into `research_outputs/` because a TIER-E measurement
    that gates nothing has nothing to file that a registration could later be
    read as resting on.  The caller takes the DataFrames.

    WHAT WOULD MAKE THIS WRONG: writing a table here.  A filed table acquires
    a manifest, a manifest acquires a sha, and a sha is the first step by which
    a measurement that gates nothing becomes a number something rests on.
    """
    lo, hi, meta = corridor()
    log("=" * 78)
    log("AN-1 · RVWAP x WALL CONFLUENCE — TIER-E MEASUREMENT, GATES NOTHING")
    log("=" * 78)
    log(f"  CORRIDOR {meta['panel_start']} -> {meta['last_closed_4h_close']} "
        f"({meta['span_days']} d)")
    conf = confluence_table(lo, hi)
    rej = rejection_by_confluence(lo, hi)
    chk = an1_selfcheck()
    log(f"  confluence_table {len(conf)} rows · "
        f"rejection_by_confluence {len(rej)} rows · "
        f"F-AN-1 {int(chk['pass'].sum())}/{len(chk)}")
    return 0


if __name__ == "__main__":                             # pragma: no cover
    raise SystemExit(main())
