"""L-REGIME [E3] — TIER-C7 pre-named lab.  DISPLAY-ONLY, GATES NOTHING.

TWO REGIME DIMENSIONS, BOTH CUT FROM THE PANEL'S OWN TAPE, AND THE v6 CARD AND
THE FULL HYBRID SLICED BY EACH.  Then — and this is the deliverable the
commission actually asked for — A NAMED LIST OF CONDITIONING CANDIDATES FOR
CENSUS-3.  A named list is not a filter.  Nothing in this module gates anything,
no card is changed, no campaign is dropped, and every grid is printed whole
including the cells that separate on nothing and the cells too small to read.

────────────────────────────────────────────────────────────────────────────
1 · REALIZED VOL, DEFINED, AND THE ONE SENTENCE THAT DEFENDS IT
────────────────────────────────────────────────────────────────────────────
    r[j]      = log(close[j] / close[j-1])                      4h log return
    rv[j]     = stdev(r[j-29 .. j], ddof=1)                     30 bars = 5 days
    med[j]    = median(rv[j-499 .. j])                          500 bars ~ 83 d
    rv_rel[j] = rv[j] / med[j]                                  THE REGIME VALUE

THE DEFENCE, IN ONE SENTENCE: `rv_rel` is each asset's current 5-day realized
vol divided by its OWN trailing 83-day median of that same quantity, because the
un-normalised quantity is not a regime at all — it is an asset name, and this
module MEASURES that rather than asserting it.

THE MEASUREMENT THAT FORCED THE NORMALISATION.  Cut on the pooled RAW rv, the
bottom tercile of panel bars is 45.3% BTCUSDT (panel share 21.8%) and 6.5%
NEARUSDT (panel share 18.2%); the top tercile is 30.1% NEARUSDT and 5.2%
BTCUSDT.  "High vol" would have meant "NEAR", "low vol" would have meant "BTC",
and a CENSUS-3 candidate written off that cut would be a per-asset card wearing
a regime's clothes.  Cut on `rv_rel` the largest asset-share excess over the
whole panel falls to under one percentage point.  Both cuts are printed in
`vol_terciles`, side by side, so a reader sees the contrast and not the claim.

BOTH WINDOW LENGTHS ARE PINNED HERE AND NEITHER IS SWEPT — an assumption, not a
comparison, in the same sense WEAVE_K is one.  30 bars is five days: enough
observations that the stdev is an estimate rather than a coin-flip, short enough
that it still describes the regime the campaign is ENTERING rather than the
quarter it sits in.  500 bars is the normaliser, deliberately an order of
magnitude longer than the numerator, so `rv_rel` moves because the numerator
moved.  THE ALTERNATIVE — normalising by the asset's FULL-HISTORY median — is
NOT taken: it is look-ahead, and a conditioning candidate that cannot be
computed at the entry bar is not a candidate for anything.

THE ANNUALISATION IS COSMETIC AND IS NAMED AS SUCH.  `rv_ann_pct` multiplies by
sqrt(6 * 365) for readability only.  A monotone constant cannot move a quantile,
so no cut in this module depends on it.

────────────────────────────────────────────────────────────────────────────
2 · TIDE STREAK, DEFINED
────────────────────────────────────────────────────────────────────────────
The tide state at bar j is sign(e89[j] - e316[j]) — the card's own 89/316 tide,
read off `T7.frame(sym)["f"]`.  The STREAK is the number of consecutive bars
ending at j on which that sign has not changed.  A campaign's band is the streak
at its ENTRY bar.

MEASURED, NOT ASSUMED: all 196 v6 campaigns and all 189 hybrid campaigns enter
WITH the tide (state == direction), so the streak is unambiguously "how long the
trend this campaign is joining has already been running" and never "how long the
trend it is fighting has run".  The cardinality is asserted in `_tag_book`.

THE EMA WARM-UP FLOOR IS EXPLICIT, BECAUSE `engine.indicators.ema` SEEDS AT THE
SERIES START AND NEVER RETURNS NaN.  This estate has repaired that defect four
times.  The tide state is treated as UNDEFINED for j < RC.WARMUP_BARS (316, the
slow tide's own length) and streaks are counted only from there.

AND THE FIRST STREAK OF EVERY ASSET IS LEFT-CENSORED, WHICH IS PRINTED.  A
streak already in progress at the warm floor has an unknown true age; its
measured length is a LOWER BOUND.  4 of 196 v6 campaigns sit in such a streak.
They are NOT dropped — dropping them would be a silent filter — they are banded
on the lower bound and counted in `n_left_censored` on their band's row.

────────────────────────────────────────────────────────────────────────────
3 · WHERE THE CUTS ARE TAKEN — PANEL POOLED BARS, NOT PER ASSET, NOT ENTRIES
────────────────────────────────────────────────────────────────────────────
Terciles and bands are cut on the PANEL POOLED distribution over BARS in the
corridor — every warm 4h bar of all five assets, one pot.  Two alternatives were
available and each is named:

  PER-ASSET CUTS are NOT taken.  Per-asset quantiles would force every asset to
  contribute exactly one third of each tercile by construction, which hides the
  very question the composition columns exist to answer.  `rv_rel` already does
  the per-asset work INSIDE the value; doing it again in the cut would be
  double-normalising.

  CUTTING ON THE CAMPAIGN ENTRIES is NOT taken, and this one is the tempting
  mistake.  It would make the three cells equal-sized by construction — 65/65/66
  — which is convenient and destroys a real finding: the card enters 76 / 66 / 52
  campaigns across LOW / MID / HIGH relative vol, so it is already, without
  anyone asking it to, a low-relative-vol entry engine.  A cut that equalises the
  cells cannot see that.  The cut is a property of the TAPE; the campaign counts
  are a property of the CARD; keeping them separate is the whole point.

Terciles for vol (3 cells), quartiles for the streak (4 cells).  Both are the
panel's own quantiles and no threshold in this module is an outside number.

THE STREAK'S BAR-POOLED QUANTILES ARE LENGTH-BIASED AND THE BIAS IS PRINTED.
Sampling streak length by BAR gives a 400-bar streak 400 votes and a 40-bar
streak 40.  The bar-pooled quartiles are the ones USED — a campaign is sampled
at a bar, so the bar distribution is the right reference for "where does this
entry sit" — and the EPISODE-pooled quartiles (each streak one vote, 226 streaks
on this panel) are printed beside them in `tide_streak_bands` so a reader can
see how far apart the two readings are.

────────────────────────────────────────────────────────────────────────────
4 · THE CANDIDATE SCREEN, WRITTEN DOWN BEFORE THE LOOK
────────────────────────────────────────────────────────────────────────────
A cell is a CANDIDATE for a statement when BOTH hold:

  (a) the cell's own asset-cluster 90% CI on the statement's quantity EXCLUDES
      ZERO; and
  (b) the asset-cluster 90% CI on the CONTRAST — the cell's mean minus its
      COMPLEMENT's mean, the same asset draw resampled into both — EXCLUDES ZERO.

CLAUSE (b) IS THE ONE THAT MAKES THE WORD "SEPARATES" MEAN ANYTHING.  Without
it every cell of a profitable book qualifies, and the table would name eight
candidates that are all just "the book is positive".  A regime cell earns the
word only by differing from the rest of the book.

AND NEITHER CLAUSE IS EVALUATED BELOW A THREE-ASSET CLUSTER FLOOR.  An
asset-cluster bootstrap over K clusters has C(2K-1, K) distinct resamples — 3 at
K=2 — so a two-asset cell's "90% interval" is the span of three numbers and
excludes zero whenever those three share a sign.  Measured here before the floor
went in: the 2-campaign `unbanded` cell reported [1.4896, 4.4971] and passed the
screen on both statements.  Such cells are still PRINTED, with no interval and
`degenerate_why` on the row; refusing to publish a number is not the same as
dropping a cell, and the multiplicity must keep its denominator.

TWO STATEMENTS ARE RUN PER CELL, AND THEY ARE DIFFERENT QUESTIONS:
  A · CARD-CONDITIONING — v6's per-campaign net R in the cell.  "Should the card
      enter here at all?"
  B · ARM-CONDITIONING  — the PAIRED hybrid-minus-v6 delta in the cell.  "Should
      the hybrid's machinery be switched on here?"

EVERY CELL IS PRINTED WHETHER IT PASSES OR NOT, and `candidates()` says on its
own face, in a column, that it IS A SELECTION SURFACE.  `is_candidate` is a
label, not a gate; `provisional` (n < 30), `rests_on_one_asset` (LOAO under 3/5),
`max_single_campaign_share` and `degenerate` ride beside it so no candidate can
be read without its caveats.

NO FDR CORRECTION IS APPLIED AND THAT IS DELIBERATE.  24 cells x 2 statements =
48 looks and NOT ONE OF THEM IS AN ACCEPTANCE TEST.  Correcting would dress an
unscored list as a scored one; the honest move is to print the number of looks
on every row (`n_looks_taken`) and let CENSUS-3 pre-register whichever candidate
it chooses to actually test.  A candidate here is a HYPOTHESIS TO BE REGISTERED
ELSEWHERE, and it is in-sample by construction.

────────────────────────────────────────────────────────────────────────────
5 · D15 RIDES, D15 GATES NOTHING
────────────────────────────────────────────────────────────────────────────
`T7.d15(cell, base)` columns ride every aggregate row of `regime_table`, and the
base for a cell is the v6 book RESTRICTED TO THE SAME BAND — so
`tail_exit_ratio` is a within-regime comparison and not a comparison against a
book made mostly of other regimes.  The v6 rows are therefore self-paired, which
gives this module a free cardinality assertion: EVERY v6 row must show a paired
delta of exactly 0 and a tail ratio of exactly 1.0, and `regime_table` HALTs if
any one of them does not.
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

iso, r4, r6, pct = T7.iso, T7.r4, T7.r6, T7.pct
PROVISIONAL_MIN_N = RC.PROVISIONAL_MIN_N
SEED = T7.SEED

# ═══════════════════════════════ THE REGISTER — pinned here, before the look
RV_WINDOW_BARS: int = 30          # 5 days of 4h bars; the numerator's window
RV_NORM_WINDOW_BARS: int = 500    # ~83 days; the asset's own trailing median
RV_ANN = float(np.sqrt(6 * 365))  # cosmetic only — monotone, moves no quantile
TIDE_WARM_BARS: int = RC.WARMUP_BARS          # 316 == TIDE_SLOW, the slow tide
VOL_TERCILE_QUANTILES = (1.0 / 3.0, 2.0 / 3.0)
STREAK_BAND_QUANTILES = (0.25, 0.50, 0.75)
CI_PCT = 90                       # the estate's asset-cluster interval
CLUSTER_FLOOR: int = 3            # min distinct assets before an interval is
#                                   published — see `_stat` for the arithmetic


def _n_resamples(k: int) -> int:
    """DISTINCT asset-cluster bootstrap resamples available at k clusters.

    Multisets of size k drawn from k labels: C(2k-1, k).  1, 3, 10, 35, 126 for
    k = 1..5.  This is the number `CLUSTER_FLOOR` is set from, and it is
    computed rather than quoted so the floor cannot drift away from its reason.

    WHAT WOULD MAKE THIS WRONG: counting ORDERED draws (k**k), which would say a
    two-cluster bootstrap has four resamples when the mean of {A,B} and {B,A}
    is the same number.
    """
    if k < 1:
        return 0
    from math import comb
    return int(comb(2 * k - 1, k))

REGISTER: dict[str, dict] = {
    "RV_WINDOW_BARS": {
        "value": RV_WINDOW_BARS,
        "text": "realized vol is the stdev (ddof=1) of 4h log returns over 30 "
                "bars = five days. Enough observations to be an estimate; short "
                "enough to describe the regime the campaign is ENTERING. PINNED "
                "AND NOT SWEPT — an assumption, not a comparison."},
    "RV_NORM_WINDOW_BARS": {
        "value": RV_NORM_WINDOW_BARS,
        "text": "rv is divided by the asset's OWN TRAILING median rv over 500 "
                "bars (~83 days), inclusive of the current bar, hence causal. "
                "An order of magnitude longer than the numerator so rv_rel moves "
                "because the numerator moved. A full-history median would be "
                "look-ahead and is NOT taken."},
    "CUT_BASIS": {
        "value": "panel pooled BARS in the corridor",
        "text": "terciles/bands are quantiles of the pooled bar distribution "
                "across all five assets. NOT per asset (rv_rel already carries "
                "the per-asset work) and NOT on campaign entries (that would "
                "equalise the cells by construction and hide that the card "
                "enters 76/66/52 across LOW/MID/HIGH relative vol)."},
    "TIDE_WARM_BARS": {
        "value": TIDE_WARM_BARS,
        "text": "engine.indicators.ema SEEDS at the series start and NEVER "
                "returns NaN. The tide state is treated as UNDEFINED below this "
                "bar index and streaks are counted only from it. The first "
                "streak of each asset is LEFT-CENSORED and is counted, banded "
                "on its lower bound, and never dropped."},
    "STREAK_SAMPLING": {
        "value": "bar-pooled quartiles USED; episode-pooled PRINTED",
        "text": "bar sampling is length-biased (a 400-bar streak votes 400 "
                "times). It is the basis USED because a campaign is sampled at "
                "a bar. The episode-pooled quartiles ride the same table so the "
                "size of the bias is visible."},
    "CANDIDATE_SCREEN": {
        "value": "own CI excludes zero AND cell-vs-complement CI excludes zero",
        "text": "clause two is what makes 'separates' mean anything: without it "
                "every cell of a profitable book qualifies. Both intervals are "
                "asset-cluster bootstraps at 90%."},
}


def register_rows() -> pd.DataFrame:
    """The pinned choices of this lab, as a table.

    WHAT WOULD MAKE THIS WRONG: a value here disagreeing with the constant the
    code actually uses — every row reads the module constant, it does not
    restate it.
    """
    return pd.DataFrame([{"key": k, "value": str(v["value"]), "text": v["text"]}
                         for k, v in sorted(REGISTER.items())])


# ═══════════════════════════════════════════════════════ THE SERIES, CACHED
_RV: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
_TIDE: dict[str, tuple[np.ndarray, np.ndarray, np.ndarray]] = {}
_CUTS: dict[tuple[int, int], dict] = {}
_BOOKS: dict[tuple[int, int], dict] = {}


def realized_vol(sym: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(rv_bar, rv_ann_pct, rv_rel) for one asset, over its FULL history.

    Computed over the whole loaded series and only then restricted by the
    caller, exactly as `T7.frame` computes its indicators, so a corridor edge
    can never move a rolling window.

    rv_bar[j]  stdev of the 30 most recent 4h log returns, ddof=1
    rv_ann_pct cosmetic: rv_bar * sqrt(6*365) * 100
    rv_rel[j]  rv_bar[j] / median(rv_bar[j-499 .. j])

    THE WARM-UP IS EXPLICIT AND IS NOT INHERITED FROM ANY EMA. Bar 0 has no
    return, so rv_bar is NaN below index RV_WINDOW_BARS, and rv_rel is NaN below
    index RV_WINDOW_BARS + RV_NORM_WINDOW_BARS - 1 (= 529 on this panel).
    `min_periods` equals the window on both rollings, so no partial window is
    ever reported as a full one.

    WHAT WOULD MAKE THIS WRONG: a trailing median that includes bars after j
    (look-ahead); min_periods below the window, which would publish a 3-sample
    stdev as a 30-sample one; using close-to-close returns across a gap in the
    series without saying so (the 4h cache is contiguous per asset and the
    corridor is one unbroken window); or normalising by a full-history median,
    which is the look-ahead this function refuses.
    """
    if sym in _RV:
        return _RV[sym]
    c = np.asarray(T7.frame(sym)["f"].c, float)
    r = np.full(len(c), np.nan)
    with np.errstate(divide="ignore", invalid="ignore"):
        r[1:] = np.log(c[1:] / c[:-1])
    r[~np.isfinite(r)] = np.nan
    rv = (pd.Series(r).rolling(RV_WINDOW_BARS, min_periods=RV_WINDOW_BARS)
          .std(ddof=1).to_numpy())
    med = (pd.Series(rv).rolling(RV_NORM_WINDOW_BARS,
                                 min_periods=RV_NORM_WINDOW_BARS)
           .median().to_numpy())
    with np.errstate(divide="ignore", invalid="ignore"):
        rel = rv / np.where(np.isfinite(med) & (med > 0), med, np.nan)
    rel = np.where(np.isfinite(rel), rel, np.nan)
    _RV[sym] = (rv, rv * RV_ANN * 100.0, rel)
    return _RV[sym]


def tide_streak(sym: str) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """(state, run, start) for one asset — the 89/316 tide and its run length.

    state[j]  +1 when e89[j] > e316[j], -1 otherwise; 0 below the warm floor
    run[j]    consecutive bars ending at j on which `state` has not changed;
              -1 below the warm floor, i.e. "not a number of bars"
    start[j]  the index at which the current streak began; -1 below the floor

    THE WARM FLOOR IS THE POINT OF THIS FUNCTION. `engine.indicators.ema` seeds
    at the series start and never returns NaN, so `e89 > e316` is answerable —
    and meaningless — from bar 0. Counting from bar 0 would hand every asset a
    fictitious 300-bar streak built out of seed values. Counting starts at
    TIDE_WARM_BARS and `start[TIDE_WARM_BARS] == TIDE_WARM_BARS` marks the one
    streak per asset whose true age is unknown.

    WHAT WOULD MAKE THIS WRONG: counting below the warm floor; resetting `run`
    to 0 rather than 1 on a flip (the flip bar IS one bar of the new state);
    treating the left-censored streak as if its length were known; or reading
    the state from anything other than the frame's own e89/e316, which are the
    same arrays the card's tide gate reads.
    """
    if sym in _TIDE:
        return _TIDE[sym]
    f = T7.frame(sym)["f"]
    e89 = np.asarray(f.e89, float)
    e316 = np.asarray(f.e316, float)
    n = len(e89)
    state = np.zeros(n, int)
    run = np.full(n, -1, int)
    start = np.full(n, -1, int)
    w = int(TIDE_WARM_BARS)
    if n > w:
        st = np.where(e89[w:] > e316[w:], 1, -1).astype(int)
        state[w:] = st
        # a flip is a change of sign; the flip bar is bar 1 of the new streak
        flip = np.empty(len(st), bool)
        flip[0] = True
        flip[1:] = st[1:] != st[:-1]
        seg_start = np.where(flip, np.arange(len(st)), 0)
        seg_start = np.maximum.accumulate(seg_start)
        run[w:] = np.arange(len(st)) - seg_start + 1
        start[w:] = seg_start + w
    _TIDE[sym] = (state, run, start)
    return _TIDE[sym]


# ═════════════════════════════════════════════════════════ POOLED PANEL BARS
def _corr(lo_ms: int | None, hi_ms: int | None) -> tuple[int, int]:
    if lo_ms is None or hi_ms is None:
        lo, hi, _ = T7.corridor()
        return (lo if lo_ms is None else lo_ms, hi if hi_ms is None else hi_ms)
    return int(lo_ms), int(hi_ms)


def _panel_pool(lo_ms: int, hi_ms: int) -> dict:
    """Every warm 4h bar of all five assets inside the corridor, pooled.

    Returns the pooled `rv_raw`, `rv_rel`, `streak` and `episode` arrays with a
    parallel symbol array for each, plus each asset's share of the panel's bars.

    THE FOUR POOLS HAVE DIFFERENT LENGTHS ON PURPOSE. `rv_rel` is warm 529 bars
    into an asset and the tide is warm at 316, so a single mask would silently
    impose the stricter warm-up on the looser dimension and shift the streak
    quartiles. Each dimension carries its own warm-up and its own pool.

    WHAT WOULD MAKE THIS WRONG: one shared warm-up mask; including bars outside
    the corridor in a cut that is then applied to campaigns inside it; or
    weighting assets equally rather than by bar count, which would make the
    quantile a property of a re-weighting nobody asked for.
    """
    rv_v, rv_s, rl_v, rl_s, sk_v, sk_s, ep_v, ep_s = ([] for _ in range(8))
    bars_by_sym: dict[str, int] = {}
    for s in RC.UNIVERSE:
        f = T7.frame(s)["f"]
        a, b = T7._idx_range(f.open_ms, lo_ms, hi_ms)
        if b < a:
            bars_by_sym[s] = 0
            continue
        idx = np.arange(len(f.c))
        inwin = (idx >= a) & (idx <= b)
        bars_by_sym[s] = int(inwin.sum())
        rv, _ann, rel = realized_vol(s)
        m = inwin & np.isfinite(rv) & np.isfinite(rel)
        rv_v.append(rv[m]); rv_s.append(np.full(int(m.sum()), s))
        rl_v.append(rel[m]); rl_s.append(np.full(int(m.sum()), s))
        _state, run, _start = tide_streak(s)
        ms = inwin & (run > 0)
        sk_v.append(run[ms]); sk_s.append(np.full(int(ms.sum()), s))
        # ONE VOTE PER STREAK: a streak's final length is its length at the bar
        # before the next flip, i.e. wherever run drops back to 1.
        # THE LAST STREAK OF EACH ASSET IS RIGHT-CENSORED — it has not flipped
        # by the corridor edge, so it has no final length and contributes NO
        # episode. Five streaks on this panel, one per asset. Inventing a
        # length for them would bias the episode quartiles DOWN, which is the
        # opposite of the truth about a streak still running.
        ends = np.flatnonzero((run[1:] == 1) & (run[:-1] > 0))
        ends = ends[inwin[ends]]
        ep_v.append(run[ends]); ep_s.append(np.full(len(ends), s))
    cat = lambda xs, dt: (np.concatenate(xs) if xs else np.array([], dt))  # noqa: E731
    tot = float(sum(bars_by_sym.values())) or 1.0
    return {
        "rv_raw": cat(rv_v, float), "rv_raw_sym": cat(rv_s, object),
        "rv_rel": cat(rl_v, float), "rv_rel_sym": cat(rl_s, object),
        "streak": cat(sk_v, int), "streak_sym": cat(sk_s, object),
        "episode": cat(ep_v, int), "episode_sym": cat(ep_s, object),
        "bars_by_sym": bars_by_sym,
        "panel_share": {s: bars_by_sym[s] / tot for s in RC.UNIVERSE},
    }


def cuts(lo_ms: int | None = None, hi_ms: int | None = None) -> dict:
    """The panel's own quantiles — the only thresholds in this module.

    `vol_rel`, `vol_raw` (tercile edges), `streak_bar` and `streak_episode`
    (quartile edges).  Cached per corridor.

    WHAT WOULD MAKE THIS WRONG: a hard-coded edge anywhere else in the file; a
    cut taken on campaign entries rather than panel bars (it would equalise the
    cells by construction); or reusing one corridor's cuts on another's book.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    key = (lo_ms, hi_ms)
    if key in _CUTS:
        return _CUTS[key]
    p = _panel_pool(lo_ms, hi_ms)
    q = lambda a, qs: [float(x) for x in np.quantile(a, qs)]           # noqa: E731
    _CUTS[key] = {
        "pool": p,
        "vol_rel": q(p["rv_rel"], VOL_TERCILE_QUANTILES),
        "vol_raw": q(p["rv_raw"], VOL_TERCILE_QUANTILES),
        "streak_bar": q(p["streak"], STREAK_BAND_QUANTILES),
        "streak_episode": (q(p["episode"], STREAK_BAND_QUANTILES)
                           if len(p["episode"]) else [None, None, None]),
    }
    return _CUTS[key]


VOL_LABELS = ("T1 LOW rel-vol", "T2 MID rel-vol", "T3 HIGH rel-vol")
VOL_RAW_LABELS = ("T1 LOW raw vol", "T2 MID raw vol", "T3 HIGH raw vol")
VOL_UNBANDED = "unbanded (rv warm-up)"
STREAK_LABELS = ("B1 YOUNG tide", "B2 EARLY tide", "B3 MATURE tide",
                 "B4 OLD tide")


def _vol_band(v: float, edges) -> int | None:
    if v is None or not np.isfinite(v):
        return None
    return int(np.digitize(float(v), edges))


def _streak_band(run: int, edges) -> int | None:
    if run is None or run <= 0:
        return None
    return int(np.digitize(float(run), edges))


# ══════════════════════════════════════════════════════════════ THE BOOKS
def books(lo_ms: int | None = None, hi_ms: int | None = None) -> dict:
    """{'v6': [...], 'hybrid': [...]} — the two books this lab slices, cached.

    Both are `T7.run_cell` on the estate's own cards, so nothing here is a
    second implementation of the ride.

    WHAT WOULD MAKE THIS WRONG: a locally-defined card; reusing a book across
    corridors; or mutating the returned lists (callers slice, they do not edit).
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    key = (lo_ms, hi_ms)
    if key not in _BOOKS:
        _BOOKS[key] = {"v6": T7.run_cell(RC.CARD_V6_CONTROL, lo_ms, hi_ms),
                       "hybrid": T7.run_cell(RC.CARD_HYBRID, lo_ms, hi_ms)}
    return _BOOKS[key]


def _tag_book(bk: list, cu: dict) -> pd.DataFrame:
    """One row per campaign: its regime coordinates at ENTRY.

    Columns: symbol, lane, entry_ms, direction, net_r, n_reentries, rv_rel,
    rv_ann_pct, vol_band, streak, streak_band, tide_state, left_censored.

    THE CARDINALITY ASSERTIONS LIVE HERE, and they are assertions about ALL
    campaigns rather than about one example:
      * every campaign has a streak band (the tide is warm at every entry bar,
        because the card's own WARMUP_BARS equals the tide warm floor);
      * every campaign enters WITH the tide, `tide_state == direction`. This is
        the fact that makes "streak" mean "the age of the trend being joined";
        were it ever false the streak would mix two opposite meanings in one
        band and every band's reading would be uninterpretable.

    WHAT WOULD MAKE THIS WRONG: reading rv_rel or the streak at the EXIT bar
    (regime at entry is the only regime a conditioning rule could act on);
    dropping the campaigns whose rv_rel is unwarm instead of banding them
    'unbanded'; or silently coercing a left-censored streak to a known one.
    """
    rows = []
    for t in bk:
        _rv, ann, rel = realized_vol(t.symbol)
        state, run, start = tide_streak(t.symbol)
        i = int(t.entry_i)
        v = float(rel[i]) if np.isfinite(rel[i]) else None
        vb = _vol_band(v, cu["vol_rel"])
        sb = _streak_band(int(run[i]), cu["streak_bar"])
        rows.append({
            "symbol": t.symbol, "lane": t.lane, "entry_ms": int(t.entry_ms),
            "entry_iso": iso(t.entry_ms), "direction": int(t.direction),
            "net_r": float(t.net_r),
            "n_reentries": int(getattr(t, "n_reentries", 0)),
            "rv_rel": r6(v), "rv_ann_pct": r4(float(ann[i]))
            if np.isfinite(ann[i]) else None,
            "vol_band": vb,
            "vol_band_label": VOL_LABELS[vb] if vb is not None else VOL_UNBANDED,
            "streak_bars": int(run[i]), "streak_band": sb,
            "streak_band_label": STREAK_LABELS[sb] if sb is not None else "—",
            "tide_state": int(state[i]),
            "left_censored": bool(int(start[i]) == int(TIDE_WARM_BARS)),
        })
    d = pd.DataFrame(rows)
    if len(d):
        if int(d["streak_band"].isna().sum()):
            raise SystemExit(
                "HALT: %d campaigns have no tide streak band. The card's "
                "WARMUP_BARS and the tide warm floor have diverged."
                % int(d["streak_band"].isna().sum()))
        off = int((d["tide_state"] != d["direction"]).sum())
        if off:
            raise SystemExit(
                "HALT: %d of %d campaigns enter AGAINST the 89/316 tide. The "
                "streak bands would mix 'age of the trend joined' with 'age of "
                "the trend fought' and no band would be readable."
                % (off, len(d)))
    return d


# ═══════════════════════════════════════════════ DIMENSION 1 · VOL TERCILES
def vol_terciles(lo_ms: int | None = None,
                 hi_ms: int | None = None) -> pd.DataFrame:
    """THE VOL TERCILES, BOTH BASES, WHOLE — the cut and the case for the cut.

    Eight rows: four cells (T1, T2, T3, unbanded) on each of two bases.

      basis 'rv_rel — USED'  the asset-normalised value this lab conditions on
      basis 'rv_raw — NOT USED'  the un-normalised value, printed ONLY so the
                                 asset-composition contrast is visible

    The composition columns are the argument. `share_<ASSET>` is the asset's
    share of the cell's bars, `panel_share_<ASSET>` its share of the corridor's
    bars, and `max_asset_share_excess_pp` the largest gap between them in
    percentage points — the single number that says whether a tercile is a
    regime or an asset name.

    WHAT WOULD MAKE THIS WRONG: printing only the basis that was used (the
    contrast IS the defence); computing shares over campaigns rather than bars
    (the cut is a property of the tape); or letting the rows fail to sum — every
    basis's cell bar-counts must total the pooled bar count, and its campaign
    counts must total the book, which is asserted below.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    cu = cuts(lo_ms, hi_ms)
    pool = cu["pool"]
    bk = books(lo_ms, hi_ms)
    tags = {k: _tag_book(v, cu) for k, v in bk.items()}
    rows = []
    for basis, key, edges, used, labels in (
            ("rv_rel — USED", "rv_rel", cu["vol_rel"], True, VOL_LABELS),
            ("rv_raw — NOT USED (composition contrast only)", "rv_raw",
             cu["vol_raw"], False, VOL_RAW_LABELS)):
        vals = pool[key]
        syms = pool[key + "_sym"]
        lab = np.digitize(vals, edges)
        for b in range(3):
            m = lab == b
            sub = syms[m]
            share = {s: (float((sub == s).sum()) / float(m.sum())
                         if m.sum() else None) for s in RC.UNIVERSE}
            exc = max(abs((share[s] or 0.0) - pool["panel_share"][s])
                      for s in RC.UNIVERSE)
            # campaign counts are only meaningful for the basis actually used
            nv6 = nhy = None
            if used:
                nv6 = int((tags["v6"]["vol_band"] == b).sum())
                nhy = int((tags["hybrid"]["vol_band"] == b).sum())
            rows.append({
                "basis": basis, "basis_used": used, "band": b,
                "band_label": labels[b],
                "edge_lo": r6(None if b == 0 else edges[b - 1]),
                "edge_hi": r6(None if b == 2 else edges[b]),
                "n_panel_bars": int(m.sum()),
                "bar_share_pct": pct(int(m.sum()), len(vals)),
                "median_value": r6(float(np.median(vals[m])) if m.sum() else None),
                "median_rv_ann_pct": None,
                "n_campaigns_v6": nv6, "n_campaigns_hybrid": nhy,
                "max_asset_share_excess_pp": r4(100.0 * exc),
                **{f"share_{s}": r4(100.0 * share[s]) if share[s] is not None
                   else None for s in RC.UNIVERSE},
                **{f"panel_share_{s}": r4(100.0 * pool["panel_share"][s])
                   for s in RC.UNIVERSE},
                "provisional": bool(used and nv6 is not None
                                    and nv6 < PROVISIONAL_MIN_N),
            })
        rows.append({
            "basis": basis, "basis_used": used, "band": None,
            "band_label": VOL_UNBANDED,
            "edge_lo": None, "edge_hi": None,
            "n_panel_bars": 0, "bar_share_pct": 0.0, "median_value": None,
            "median_rv_ann_pct": None,
            "n_campaigns_v6": (int(tags["v6"]["vol_band"].isna().sum())
                               if used else None),
            "n_campaigns_hybrid": (int(tags["hybrid"]["vol_band"].isna().sum())
                                   if used else None),
            "max_asset_share_excess_pp": None,
            **{f"share_{s}": None for s in RC.UNIVERSE},
            **{f"panel_share_{s}": r4(100.0 * pool["panel_share"][s])
               for s in RC.UNIVERSE},
            "provisional": bool(used),
        })
    d = pd.DataFrame(rows)
    # the annualised median, for readability, on the RAW basis only (rv_rel is
    # a ratio and has no percent reading)
    raw = ~d["basis_used"].astype(bool)
    d.loc[raw, "median_rv_ann_pct"] = [
        r4(v * RV_ANN * 100.0) if v is not None else None
        for v in d.loc[raw, "median_value"]]
    # ═══ CARDINALITY, NOT AN EXAMPLE
    for basis, grp in d.groupby("basis"):
        nb = int(grp["n_panel_bars"].sum())
        want = len(pool["rv_rel" if grp["basis_used"].iloc[0] else "rv_raw"])
        if nb != want:
            raise SystemExit(f"HALT: vol basis {basis!r} bars {nb} != pooled "
                             f"{want}. A tercile has lost or double-counted "
                             f"bars.")
    for name, tg in tags.items():
        got = int(d.loc[d["basis_used"], f"n_campaigns_{'v6' if name == 'v6' else 'hybrid'}"].sum())
        if got != len(tg):
            raise SystemExit(f"HALT: vol terciles hold {got} {name} campaigns "
                             f"but the book has {len(tg)}.")
    d["gates"] = "NOTHING — a cut definition, printed whole"
    d["in_sample"] = True
    d["corridor"] = f"{iso(lo_ms)} → {iso(hi_ms)}"
    return d


# ══════════════════════════════════════════ DIMENSION 2 · TIDE STREAK BANDS
def tide_streak_bands(lo_ms: int | None = None,
                      hi_ms: int | None = None) -> pd.DataFrame:
    """THE TIDE-STREAK BANDS, BOTH SAMPLINGS, WHOLE.

    Eight rows: four bands on each of two samplings of the SAME streaks.

      basis 'bar-pooled — USED'      each panel bar votes; length-biased, and
                                     the right reference because a campaign is
                                     sampled at a bar
      basis 'episode-pooled — NOT USED'  each streak votes once; printed so the
                                     size of the length bias is a number

    `n_left_censored` counts the campaigns sitting in the one streak per asset
    that was already running at the EMA warm floor. Their streak length is a
    LOWER bound, so a left-censored campaign can only ever be banded too YOUNG,
    never too old — the direction of the error is stated because it is knowable.

    WHAT WOULD MAKE THIS WRONG: quoting the episode quartiles as the ones in
    force; dropping left-censored campaigns instead of counting them; counting
    streaks below the warm floor; or letting a band's campaign counts fail to
    total the book — asserted below.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    cu = cuts(lo_ms, hi_ms)
    pool = cu["pool"]
    bk = books(lo_ms, hi_ms)
    tags = {k: _tag_book(v, cu) for k, v in bk.items()}
    rows = []
    for basis, key, edges, used in (
            ("bar-pooled — USED", "streak", cu["streak_bar"], True),
            ("episode-pooled — NOT USED (length-bias contrast)", "episode",
             cu["streak_episode"], False)):
        vals = pool[key]
        syms = pool[key + "_sym"]
        lab = np.digitize(vals.astype(float), edges)
        for b in range(4):
            m = lab == b
            sub = syms[m]
            share = {s: (float((sub == s).sum()) / float(m.sum())
                         if m.sum() else None) for s in RC.UNIVERSE}
            nv6 = nhy = ncens = None
            if used:
                sel6 = tags["v6"]["streak_band"] == b
                nv6 = int(sel6.sum())
                nhy = int((tags["hybrid"]["streak_band"] == b).sum())
                ncens = int(tags["v6"].loc[sel6, "left_censored"].sum())
            rows.append({
                "basis": basis, "basis_used": used, "band": b,
                "band_label": STREAK_LABELS[b],
                "edge_lo_bars": (None if b == 0 else
                                 r4(edges[b - 1]) if edges[b - 1] is not None
                                 else None),
                "edge_hi_bars": (None if b == 3 else
                                 r4(edges[b]) if edges[b] is not None else None),
                "n_units": int(m.sum()),
                "unit": "panel 4h bars" if used else "streak episodes",
                "unit_share_pct": pct(int(m.sum()), len(vals)),
                "median_streak_bars": r4(float(np.median(vals[m]))
                                         if m.sum() else None),
                "median_streak_days": r4(float(np.median(vals[m])) / 6.0
                                         if m.sum() else None),
                "n_campaigns_v6": nv6, "n_campaigns_hybrid": nhy,
                "n_left_censored": ncens,
                **{f"share_{s}": r4(100.0 * share[s]) if share[s] is not None
                   else None for s in RC.UNIVERSE},
                "provisional": bool(used and nv6 is not None
                                    and nv6 < PROVISIONAL_MIN_N),
            })
    d = pd.DataFrame(rows)
    used = d["basis_used"]
    for name, col in (("v6", "n_campaigns_v6"), ("hybrid", "n_campaigns_hybrid")):
        got = int(d.loc[used, col].sum())
        if got != len(tags[name]):
            raise SystemExit(f"HALT: streak bands hold {got} {name} campaigns "
                             f"but the book has {len(tags[name])}.")
    for basis, grp in d.groupby("basis"):
        nb = int(grp["n_units"].sum())
        want = len(pool["streak" if grp["basis_used"].iloc[0] else "episode"])
        if nb != want:
            raise SystemExit(f"HALT: streak basis {basis!r} holds {nb} units "
                             f"!= pooled {want}.")
    d["bar_vs_episode_note"] = (
        f"bar-pooled quartiles {[r4(x) for x in cu['streak_bar']]} against "
        f"episode-pooled {[r4(x) for x in cu['streak_episode']]}. The bar "
        f"sampling gives a long streak one vote per bar; the episode sampling "
        f"gives it one. The bar basis is the one USED.")
    d["gates"] = "NOTHING — a cut definition, printed whole"
    d["in_sample"] = True
    d["corridor"] = f"{iso(lo_ms)} → {iso(hi_ms)}"
    return d


# ══════════════════════════════════════════════════════════ THE CROSS TABLE
def _band_key(b) -> str:
    """A TOTAL, SORTABLE STRING KEY for a band.

    `band` carries three kinds of value — an integer band, None for the
    unbanded cell, and the literal "ALL" — and a column holding all three
    cannot be sorted, which is precisely what `TB.write_table` does to it
    before hashing.  The key is a string in every row: "01".."04" for the
    bands, "98-unbanded", "99-ALL", so the sort is total, the ordering is the
    reading order, and the aggregate rows land last.  The integer survives
    beside it as `band_index` and the prose as `band_label`.

    WHAT WOULD MAKE THIS WRONG: a mixed-type key column (it raises under
    `sort_values` on some pandas builds and orders arbitrarily on others); or a
    key that is not unique per (book, dimension), which would trip F-KEY.
    """
    if isinstance(b, int):
        return f"{b + 1:02d}"
    return "99-ALL" if b == "ALL" else "98-unbanded"


def _cell(bk: list, tg: pd.DataFrame, dim: str, band) -> list:
    """The campaigns of one book inside one regime cell, order preserved."""
    if band == "ALL":
        return list(bk)
    col = "vol_band" if dim == "vol_tercile" else "streak_band"
    if band is None:
        m = tg[col].isna().to_numpy()
    else:
        m = (tg[col] == band).to_numpy()
    return [t for t, keep in zip(bk, m) if keep]


def regime_table(lo_ms: int | None = None,
                 hi_ms: int | None = None) -> pd.DataFrame:
    """v6 AND THE FULL HYBRID, CROSSED BY EACH REGIME DIMENSION, WHOLE.

    One row per (dimension, band, card).  Each dimension prints every band, the
    unbanded cell where one exists, and an ALL row whose n is the book — so the
    reader can add the bands up and see that nothing left the table.

    Headline columns are `T7.agg`'s: n, net_r, expectancy_r, win_rate_pct, plus
    max_dd_r / best_r / strip_best_net_r / top_decile_share_pct, which are the
    concentration reading a regime cell most needs.  `n_reentries` rides the
    hybrid rows because "does the chain fire more in some regimes?" is a
    question this table can answer and nothing else in the estate asks.

    THE D15 TRIO RIDES EVERY ROW AND GATES NOTHING.  The base for a cell is the
    v6 book RESTRICTED TO THE SAME BAND, so `tail_exit_ratio` compares like with
    like instead of comparing one regime's tail against a book made mostly of
    other regimes.  That choice makes every v6 row self-paired, which is a free
    cardinality assertion and it is taken: EVERY v6 row must show
    paired_delta_expectancy_r == 0 and, where a top decile exists,
    tail_exit_ratio == 1.0.  The table HALTs otherwise.

    WHAT WOULD MAKE THIS WRONG: banding a campaign by its EXIT regime; dropping
    the unbanded cell; pairing the hybrid against the whole v6 book while
    calling the result a within-regime delta; or reading any column here as a
    filter — the deliverable is `candidates`, and even that names rather than
    selects.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    cu = cuts(lo_ms, hi_ms)
    bk = books(lo_ms, hi_ms)
    tags = {k: _tag_book(v, cu) for k, v in bk.items()}
    tot = {k: sum(t.net_r for t in v) for k, v in bk.items()}
    rows = []
    dims = (("vol_tercile", [0, 1, 2, None, "ALL"],
             lambda b: VOL_LABELS[b] if isinstance(b, int) else
             (VOL_UNBANDED if b is None else "ALL (the whole book)")),
            ("tide_streak_band", [0, 1, 2, 3, "ALL"],
             lambda b: STREAK_LABELS[b] if isinstance(b, int) else
             "ALL (the whole book)"))
    for dim, bands, lab in dims:
        for b in bands:
            v6c = _cell(bk["v6"], tags["v6"], dim, b)
            for card in ("v6", "hybrid"):
                cell = _cell(bk[card], tags[card], dim, b)
                row = T7.agg(cell, label=dim, key=str(lab(b)))
                row.update({
                    "dimension": dim, "band": _band_key(b),
                    "band_index": b if isinstance(b, int) else None,
                    "band_label": lab(b),
                    "card": card, "book": card,
                    "share_of_card_net_r_pct": (
                        pct(sum(t.net_r for t in cell), tot[card])
                        if tot[card] else None),
                    "n_reentries": sum(getattr(t, "n_reentries", 0)
                                       for t in cell),
                    "n_assets": len({t.symbol for t in cell}),
                    "d15_base": "the v6 book RESTRICTED TO THIS BAND",
                    "d15_gates": "NOTHING [house law]",
                })
                row.update(T7.d15(cell, v6c))
                rows.append(row)
    d = pd.DataFrame(rows)
    # ═══ CARDINALITY, NOT AN EXAMPLE — every v6 row is self-paired
    v6r = d[d["card"] == "v6"]
    bad = v6r[(v6r["n"] > 0)
              & (v6r["paired_delta_expectancy_r"].fillna(1.0).abs() > 1e-12)]
    if len(bad):
        raise SystemExit(f"HALT: {len(bad)} v6 rows are not self-paired. The "
                         f"cell/base banding has diverged.")
    bad2 = v6r[(v6r["n"] >= 10)
               & ((v6r["tail_exit_ratio"] - 1.0).abs() > 1e-9)]
    if len(bad2):
        raise SystemExit(f"HALT: {len(bad2)} v6 rows have tail_exit_ratio != 1 "
                         f"against themselves.")
    for dim, _bands, _lab in dims:
        for card in ("v6", "hybrid"):
            g = d[(d["dimension"] == dim) & (d["card"] == card)]
            parts = int(g.loc[g["band"] != "99-ALL", "n"].sum())
            whole = int(g.loc[g["band"] == "99-ALL", "n"].iloc[0])
            if parts != whole:
                raise SystemExit(f"HALT: {dim}/{card} bands hold {parts} "
                                 f"campaigns, the ALL row holds {whole}.")
    d["provisional"] = d["n"] < PROVISIONAL_MIN_N
    d["gates"] = "NOTHING — a slice surface, printed whole"
    d["in_sample"] = True
    d["corridor"] = f"{iso(lo_ms)} → {iso(hi_ms)}"
    front = ["dimension", "band", "band_label", "book", "card", "n", "net_r",
             "expectancy_r", "win_rate_pct", "paired_delta_expectancy_r",
             "tail_exit_ratio", "max_single_trade_delta_share", "provisional"]
    return d[front + [c for c in d.columns if c not in front]]


# ═══════════════════════════════════════════ THE NAMED LIST FOR CENSUS-3
def _loao_line_mean(values, clusters) -> dict:
    """LEAVE-ONE-ASSET-OUT on a SINGLE-BOOK mean — the same 3-of-5 bar.

    `T7.loao` is the estate's object and it is used unchanged for the PAIRED
    statement below, where a base book exists to pair against.  Statement A has
    no base book — it is v6's own expectancy inside a cell — so its five panels
    are built here.  Same bar, same 90% asset-cluster interval, same "k/5" line.

    ITS TWO-CLUSTER MINIMUM MIRRORS `T7.loao`'s AND DELIBERATELY DIFFERS FROM
    `CLUSTER_FLOOR`.  Forking the estate's threshold here would put two
    incomparable numbers in one column.  The weakness it leaves — a 3-asset cell
    whose every LOAO panel drops to 2 clusters — is not hidden, it is FLAGGED on
    the row instead, which keeps the estate's object unforked and the caveat
    visible.

    WHAT WOULD MAKE THIS WRONG: a different interval or a different bar from
    T7.loao's, which would make the two statements' lines incomparable while
    they sit in the same column; or treating 3/5 as a significance threshold —
    it is a robustness line printed beside a verdict, never instead of one.
    """
    v = np.asarray(values, float)
    c = np.asarray(clusters)
    per = []
    for drop in sorted(RC.UNIVERSE):
        m = c != drop
        vv, cc = v[m], c[m]
        if len(vv) < 2 or len(set(cc.tolist())) < 2:
            per.append({"dropped": drop, "excludes_zero": False,
                        "lo": None, "hi": None})
            continue
        ci = T7._ci_from(T7.cluster_boot(vv, cc), float(np.mean(vv)))
        per.append({"dropped": drop,
                    "lo": ci["lo"], "hi": ci["hi"],
                    "excludes_zero": bool(ci["lo"] is not None
                                          and (ci["lo"] > 0 or ci["hi"] < 0))})
    n_ex = sum(1 for p in per if p["excludes_zero"])
    return {"loao_line": f"{n_ex}/{len(per)}",
            "loao_clears_3_of_5": bool(n_ex >= 3),
            "loao_detail": "; ".join(
                f"-{p['dropped']}: [{r4(p['lo'])}, {r4(p['hi'])}]"
                f"{'*' if p['excludes_zero'] else ''}" for p in per)}


def _stat(values, clusters, comp_values, comp_clusters) -> dict:
    """One cell's two intervals: its own mean, and its mean minus its complement.

    Both are asset-cluster bootstraps at 90%; the contrast resamples the SAME
    asset draw into both arms (`T7.cluster_boot_diff`), which is the only way
    "this cell differs from the rest of the book" survives a panel where one
    asset is 82% of the net R.

    THE CLUSTER FLOOR IS THREE ASSETS, AND THE ARITHMETIC IS WHY.  An
    asset-cluster bootstrap over K clusters has only C(2K-1, K) distinct
    resamples: ONE at K=1, THREE at K=2, ten at K=3, 126 at the full panel's
    K=5.  Four thousand draws from three distinct values is not a 90% interval,
    it is the span of three numbers wearing a percentile's clothes — and it
    excludes zero whenever all three happen to share a sign, which is exactly
    what a two-asset cell does.  Measured on this build before the floor was
    raised: the 2-campaign `unbanded` cell reported [1.4896, 4.4971] and passed
    the candidate screen on both statements.  So a cell with under three
    distinct assets (or under two campaigns) returns `degenerate=True` and NO
    interval.  IT IS STILL PRINTED — this refuses to publish a number, it does
    not drop a cell, and `degenerate_why` carries the reason onto the row.

    WHAT WOULD MAKE THIS WRONG: bootstrapping over campaigns rather than assets;
    an independent draw for the two arms of the contrast; emitting an interval
    below the cluster floor; or dropping the cells that fall below it, which
    would delete part of the multiplicity the table exists to show.
    """
    v = np.asarray(values, float)
    c = np.asarray(clusters)
    w = np.asarray(comp_values, float)
    k = np.asarray(comp_clusters)
    out = {"n": len(v), "n_assets": len(set(c.tolist())),
           "complement_n": len(w),
           "point": r6(float(np.mean(v))) if len(v) else None,
           "complement_point": r6(float(np.mean(w))) if len(w) else None,
           "ci_lo": None, "ci_hi": None, "ci_excludes_zero": False,
           "contrast_point": None, "contrast_ci_lo": None,
           "contrast_ci_hi": None, "contrast_excludes_zero": False,
           "degenerate": False, "degenerate_why": ""}
    if len(v) < 2 or out["n_assets"] < CLUSTER_FLOOR:
        out["degenerate"] = True
        out["degenerate_why"] = (
            f"{len(v)} campaigns across {out['n_assets']} assets — below the "
            f"cluster floor of {CLUSTER_FLOOR}. An asset-cluster bootstrap over "
            f"{out['n_assets']} clusters has only "
            f"{_n_resamples(out['n_assets'])} distinct resamples, so no "
            f"interval is published for this cell")
        return out
    ci = T7._ci_from(T7.cluster_boot(v, c), float(np.mean(v)))
    out["ci_lo"], out["ci_hi"] = r6(ci["lo"]), r6(ci["hi"])
    out["ci_excludes_zero"] = bool(ci["lo"] is not None
                                   and (ci["lo"] > 0 or ci["hi"] < 0))
    if len(w) < 2 or len(set(k.tolist())) < CLUSTER_FLOOR:
        out["degenerate_why"] = (f"the complement holds {len(w)} campaigns "
                                 f"across {len(set(k.tolist()))} assets, below "
                                 f"the cluster floor — no contrast is "
                                 f"computable")
        return out
    dr = T7.cluster_boot_diff(v, c, w, k)
    dci = T7._ci_from(dr, float(np.mean(v)) - float(np.mean(w)))
    out["contrast_point"] = r6(dci["point"])
    out["contrast_ci_lo"], out["contrast_ci_hi"] = r6(dci["lo"]), r6(dci["hi"])
    out["contrast_excludes_zero"] = bool(
        dci["lo"] is not None and (dci["lo"] > 0 or dci["hi"] < 0))
    return out


def _conc(values) -> dict:
    """TWO CONCENTRATION READINGS, BECAUSE THE FAMILIAR ONE IS UNBOUNDED.

    `max_single_campaign_share` is D15's shape — the largest |campaign| over
    |the cell's NET| — kept for parity with `T7.d15`.  IT IS NOT A PERCENTAGE
    AND IT ROUTINELY EXCEEDS 1: a cell whose campaigns nearly cancel has a
    near-zero denominator, and this build measured 95.61 on one joint cell.
    That is not a broken number, it is the strongest possible warning — a cell
    whose net is a near-cancellation has no net to speak of — but it must not be
    printed with a percent sign, and `concentration_reading` says which regime
    the number is in.

    `max_abs_share_of_gross` is the bounded companion: the largest |campaign|
    over the SUM of |campaigns|, which lives in (0, 1] and answers "how much of
    the cell's total movement is one campaign" without a denominator that can
    vanish.  Both are printed because neither alone is honest.

    WHAT WOULD MAKE THIS WRONG: rendering the unbounded ratio as a percentage;
    dropping it in favour of the bounded one (it is the estate's own D15 shape
    and a reader comparing tables needs it); or reporting either on an empty
    cell.
    """
    v = np.asarray(values, float)
    if not len(v):
        return {"max_single_campaign_share": None,
                "max_abs_share_of_gross": None,
                "concentration_reading": "empty cell"}
    tot = float(np.sum(v))
    gross = float(np.sum(np.abs(v)))
    share = (r4(float(np.max(np.abs(v))) / abs(tot))
             if abs(tot) > 1e-12 else None)
    bounded = r4(float(np.max(np.abs(v))) / gross) if gross > 1e-12 else None
    if share is None:
        reading = ("the cell's net is zero to within 1e-12 — the ratio to net "
                   "is undefined; read max_abs_share_of_gross")
    elif share > 1.0:
        reading = (f"the cell's net is a NEAR-CANCELLATION: its largest single "
                   f"campaign is {share:.2f}x the whole cell's net. The net is "
                   f"a residue, not a result.")
    else:
        reading = (f"the largest single campaign is {100.0 * share:.1f}% of "
                   f"the cell's net")
    return {"max_single_campaign_share": share,
            "max_abs_share_of_gross": bounded,
            "concentration_reading": reading}


def candidates(lo_ms: int | None = None,
               hi_ms: int | None = None) -> pd.DataFrame:
    """THE DELIVERABLE — CONDITIONING CANDIDATES FOR CENSUS-3, NAMED, NOT USED.

    THIS TABLE IS A SELECTION SURFACE AND SAYS SO IN A COLUMN.  It ranks regime
    cells by whether they look like they separate.  It changes no card, gates no
    campaign and is in-sample by construction.  What it produces is a list of
    HYPOTHESES for CENSUS-3 to pre-register and test out of sample.

    ONE ROW PER (cell, statement).  24 cells — 4 vol, 4 tide-streak, 16 joint —
    times two statements:

      A · CARD-CONDITIONING  quantity = v6's per-campaign net R in the cell.
          "Does the card itself work differently here?"
      B · ARM-CONDITIONING   quantity = the PAIRED hybrid-minus-v6 delta over
          the campaigns in the cell.  "Does the hybrid's machinery pay here?"

    THE SCREEN, PRE-STATED IN THE MODULE DOCSTRING: `is_candidate` requires the
    cell's own 90% asset-cluster CI to exclude zero AND the cell-versus-
    complement contrast CI to exclude zero.  The second clause is what stops the
    table naming every cell of a profitable book.

    EVERY CELL IS PRINTED WHETHER IT PASSES OR NOT, with `provisional`
    (n_effective < PROVISIONAL_MIN_N), `rests_on_one_asset` (LOAO under 3/5),
    both concentration readings and `degenerate` beside the verdict.  A candidate
    with a 0.9 concentration share and a 1/5 LOAO line is one campaign wearing a
    regime's name, and the columns say so on the same line as the word
    "candidate".  `census3_statement` renders each row as a sentence CENSUS-3
    could pre-register verbatim — with its caveats attached, and with the reason
    a non-candidate failed, because the failures ARE the multiplicity.

    NO FDR CORRECTION IS APPLIED, DELIBERATELY.  `n_looks_taken` rides every row
    so the multiplicity is a printed number.  Correcting an unscored list would
    dress it as a scored one; CENSUS-3 corrects what CENSUS-3 registers.

    WHAT WOULD MAKE THIS WRONG: dropping the cells that fail (the failures are
    the multiplicity); using `is_candidate` as a filter anywhere in the estate;
    scoring statement B against zero without pairing (Tier-C5 shipped that
    mistake and the review reversed its verdict); an FDR bar quoted here as if
    these were tests; or reading any of it out of sample, which it is not.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    cu = cuts(lo_ms, hi_ms)
    bk = books(lo_ms, hi_ms)
    tags = {k: _tag_book(v, cu) for k, v in bk.items()}
    v6, hyb = bk["v6"], bk["hybrid"]
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in v6}

    def masks(card: str):
        tg = tags[card]
        vb = tg["vol_band"].to_numpy()
        sb = tg["streak_band"].to_numpy()
        return vb, sb

    cells: list[tuple[str, str, dict]] = []
    vlab = list(VOL_LABELS) + [VOL_UNBANDED]
    vkey = [0, 1, 2, None]
    for b, lb in zip(vkey, vlab):
        cells.append(("vol_tercile", lb, {"vol": b}))
    for b, lb in zip([0, 1, 2, 3], STREAK_LABELS):
        cells.append(("tide_streak_band", lb, {"streak": b}))
    for vb_, vl in zip(vkey, vlab):
        for sb_, sl in zip([0, 1, 2, 3], STREAK_LABELS):
            cells.append(("vol_tercile x tide_streak_band",
                          f"{vl} & {sl}", {"vol": vb_, "streak": sb_}))

    def select(card: str, spec: dict) -> np.ndarray:
        vb, sb = masks(card)
        m = np.ones(len(vb), bool)
        if "vol" in spec:
            m &= (pd.isna(vb) if spec["vol"] is None else (vb == spec["vol"]))
        if "streak" in spec:
            m &= (sb == spec["streak"])
        return m

    n_looks = len(cells) * 2
    rows = []
    for dim, label, spec in cells:
        m6 = select("v6", spec)
        mh = select("hybrid", spec)
        # ── STATEMENT A · the card itself, in the cell against everywhere else
        va = np.array([t.net_r for t, k in zip(v6, m6) if k], float)
        ca = np.array([t.symbol for t, k in zip(v6, m6) if k], object)
        vb_ = np.array([t.net_r for t, k in zip(v6, m6) if not k], float)
        cb_ = np.array([t.symbol for t, k in zip(v6, m6) if not k], object)
        st = _stat(va, ca, vb_, cb_)
        lo_ = (_loao_line_mean(va, ca) if not st["degenerate"]
               else {"loao_line": "—", "loao_clears_3_of_5": False,
                     "loao_detail": "not computed — degenerate cell"})
        rows.append(_row(dim, label, spec, "A · CARD-CONDITIONING",
                         "v6 per-campaign net R in the cell",
                         "v6 campaigns in the cell vs v6 campaigns elsewhere",
                         st, lo_, va, n_looks))
        # ── STATEMENT B · the hybrid's marginal, PAIRED, in the cell
        cellh = [t for t, k in zip(hyb, mh) if k]
        outh = [t for t, k in zip(hyb, mh) if not k]
        pv, pc = [], []
        for t in cellh:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                pv.append(t.net_r - bu[k]); pc.append(t.symbol)
        qv, qc = [], []
        for t in outh:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                qv.append(t.net_r - bu[k]); qc.append(t.symbol)
        stb = _stat(np.array(pv, float), np.array(pc, object),
                    np.array(qv, float), np.array(qc, object))
        # `n` is the cell's hybrid campaign count; the INTERVAL rests on the
        # PAIRED subset, which is `n_paired` and which `provisional` reads.
        stb["n"] = len(cellh)
        lob = (T7.loao(cellh, v6, label) if len(pv) >= 2
               and len(set(pc)) >= 2 else
               {"loao_line": "—", "loao_clears_3_of_5": False,
                "loao_detail": "not computed — degenerate cell"})
        rows.append(_row(dim, label, spec, "B · ARM-CONDITIONING",
                         "PAIRED hybrid − v6 per-campaign delta in the cell",
                         "paired delta in the cell vs paired delta elsewhere",
                         stb, lob, np.array(pv, float), n_looks,
                         n_paired=len(pv), n_reentries=sum(
                             getattr(t, "n_reentries", 0) for t in cellh)))
    d = pd.DataFrame(rows)
    if len(d) != n_looks:
        raise SystemExit(f"HALT: {len(d)} rows for {n_looks} looks.")
    # ═══ CARDINALITY — the marginal cells of each dimension must hold the book
    for dim, col in (("vol_tercile", "n"), ("tide_streak_band", "n")):
        g = d[(d["dimension"] == dim) & (d["statement"].str.startswith("A"))]
        if int(g[col].sum()) != len(v6):
            raise SystemExit(f"HALT: {dim} statement-A cells hold "
                             f"{int(g[col].sum())} v6 campaigns, book has "
                             f"{len(v6)}.")
    d = d.sort_values(
        ["is_candidate", "n_effective"],
        ascending=[False, False], kind="mergesort").reset_index(drop=True)
    d["selection_surface"] = True
    d["selection_surface_note"] = (
        "THIS TABLE IS A SELECTION SURFACE. It ranks regime cells by how much "
        "they look like they separate and NAMES candidates for CENSUS-3 to "
        "pre-register. It gates nothing, changes no card, and is in-sample by "
        "construction. `is_candidate` is a LABEL, never a filter.")
    d["n_looks_taken"] = n_looks
    d["fdr_applied"] = False
    d["fdr_note"] = (
        f"{n_looks} looks and not one acceptance test. No FDR correction is "
        f"applied because correcting an unscored list would dress it as a "
        f"scored one; the look count is printed instead and CENSUS-3 corrects "
        f"what CENSUS-3 registers.")
    d["in_sample"] = True
    d["corridor"] = f"{iso(lo_ms)} → {iso(hi_ms)}"
    front = ["is_candidate", "candidate", "dimension", "cell", "statement",
             "n", "n_effective", "point", "ci_lo", "ci_hi", "contrast_point",
             "contrast_ci_lo", "contrast_ci_hi", "provisional",
             "rests_on_one_asset", "max_abs_share_of_gross",
             "max_single_campaign_share", "flags"]
    return d[front + [c for c in d.columns if c not in front]]


def _row(dim, label, spec, statement, quantity, contrast_is, st, lo_, vals,
         n_looks, n_paired=None, n_reentries=None) -> dict:
    """ONE (cell, statement) LINE — the verdict and every caveat it must carry.

    `n_effective` IS THE n THE INTERVAL ACTUALLY RESTS ON, and it is what
    `provisional` reads.  For statement B the cell may hold 64 hybrid campaigns
    while the paired delta rests on however many of them have a v6 twin; calling
    that cell non-provisional on the 64 would be claiming an n the CI never had.

    `census3_statement` is the row rendered as a sentence CENSUS-3 could
    pre-register verbatim, caveats attached.  Non-candidates render the reason
    they are not, because the reasons are the multiplicity and deleting them
    would leave a list of winners with no denominator.

    WHAT WOULD MAKE THIS WRONG: provisional read off the unpaired n; a flag
    computed from a different quantity than the interval; or a
    `census3_statement` that omits a flag the row carries.
    """
    n_eff = int(n_paired) if n_paired is not None else int(st["n"])
    prov = bool(n_eff < PROVISIONAL_MIN_N)
    one_asset = not bool(lo_["loao_clears_3_of_5"])
    conc = _conc(vals)
    cand = bool(st["ci_excludes_zero"] and st["contrast_excludes_zero"])
    flags = []
    if prov:
        flags.append(f"PROVISIONAL n_effective={n_eff} < {PROVISIONAL_MIN_N}")
    if st["degenerate"]:
        flags.append("DEGENERATE — no interval")
    if one_asset and not st["degenerate"]:
        flags.append(f"RESTS ON ONE ASSET (LOAO {lo_['loao_line']})")
    b = conc["max_abs_share_of_gross"]
    if b is not None and b >= 0.5:
        flags.append(f"ONE CAMPAIGN IS {100.0 * b:.0f}% OF THE CELL'S TOTAL "
                     f"ABSOLUTE MOVEMENT")
    s = conc["max_single_campaign_share"]
    if s is not None and s > 1.0:
        flags.append(f"NET IS A NEAR-CANCELLATION ({s:.2f}x)")
    if st["n_assets"] < CLUSTER_FLOOR:
        flags.append(f"only {st['n_assets']} assets in the cell — below the "
                     f"cluster floor of {CLUSTER_FLOOR}")
    elif st["n_assets"] == CLUSTER_FLOOR:
        flags.append(f"{CLUSTER_FLOOR} assets in the cell — EVERY LOAO panel "
                     f"drops to {CLUSTER_FLOOR - 1} clusters "
                     f"({_n_resamples(CLUSTER_FLOOR - 1)} distinct resamples), "
                     f"so the LOAO line is not readable here")
    fl = "; ".join(flags) if flags else ""
    if cand:
        sent = (f"CENSUS-3 MAY PRE-REGISTER: inside {dim} = {label} "
                f"(n={st['n']}, n_effective={n_eff}, assets={st['n_assets']}), "
                f"{quantity} is {st['point']} "
                f"[90% CI {st['ci_lo']}, {st['ci_hi']}] and SEPARATES from the "
                f"rest of the book by {st['contrast_point']} "
                f"[{st['contrast_ci_lo']}, {st['contrast_ci_hi']}]. "
                f"CAVEATS: {fl or 'none recorded'}.")
    else:
        why = ("no interval — degenerate cell" if st["degenerate"] else
               "its own CI includes zero" if not st["ci_excludes_zero"] else
               "it does not separate from the rest of the book — the "
               "cell-vs-complement CI includes zero")
        sent = (f"NOT A CANDIDATE: inside {dim} = {label} (n={st['n']}), "
                f"{quantity} is {st['point']}, and the screen fails because "
                f"{why}." + (f" ALSO: {fl}." if fl else ""))
    return {
        # `candidate` IS THE ROW'S NAME AND ITS JOIN KEY. One row per
        # (dimension, cell, statement), so the triple is the identity and
        # F-KEY can assert it. A key of `cell` alone would collide across the
        # two statements and silently drop half the table on a join.
        "candidate": f"{dim} | {label} | {statement.split(' · ')[0]}",
        "dimension": dim, "cell": label, "statement": statement,
        "quantity": quantity, "contrast_is": contrast_is,
        "n": st["n"], "n_paired": n_paired, "n_effective": n_eff,
        "n_assets": st["n_assets"], "complement_n": st["complement_n"],
        "point": st["point"], "ci_lo": st["ci_lo"], "ci_hi": st["ci_hi"],
        "ci_excludes_zero": st["ci_excludes_zero"],
        "complement_point": st["complement_point"],
        "contrast_point": st["contrast_point"],
        "contrast_ci_lo": st["contrast_ci_lo"],
        "contrast_ci_hi": st["contrast_ci_hi"],
        "contrast_excludes_zero": st["contrast_excludes_zero"],
        "is_candidate": cand,
        "provisional": prov,
        "rests_on_one_asset": one_asset,
        **conc,
        "loao_line": lo_["loao_line"],
        "loao_clears_3_of_5": bool(lo_["loao_clears_3_of_5"]),
        "loao_detail": lo_["loao_detail"],
        "degenerate": st["degenerate"], "degenerate_why": st["degenerate_why"],
        "n_reentries": n_reentries,
        "flags": fl,
        "census3_statement": sent,
        "screen": "own 90% asset-cluster CI excludes zero AND cell-vs-"
                  "complement CI excludes zero",
        "gates": "NOTHING — a named candidate for CENSUS-3 to pre-register",
    }


def all_tables(lo_ms: int | None = None,
               hi_ms: int | None = None) -> dict[str, pd.DataFrame]:
    """The lab's five tables, by name.  No writes — the caller decides.

    WHAT WOULD MAKE THIS WRONG: writing at import time or from here; or
    returning a table this module has not asserted the cardinality of.
    """
    lo_ms, hi_ms = _corr(lo_ms, hi_ms)
    return {"lregime_register": register_rows(),
            "lregime_vol_terciles": vol_terciles(lo_ms, hi_ms),
            "lregime_tide_streak_bands": tide_streak_bands(lo_ms, hi_ms),
            "lregime_cross": regime_table(lo_ms, hi_ms),
            "lregime_candidates": candidates(lo_ms, hi_ms)}
