"""L-ZEC — WHY ZEC.  TIER-C6 rev B, pre-named lab.  DISPLAY-ONLY, GATES NOTHING.

THE QUESTION THE OPERATOR ASKED: *understand WHY ZEC*.  ZEC is 81.7% of the v6
panel's entire net R (32.5680 of 39.8443) and 83.9% of the v5 control's
(28.2027 of 33.6149).  Five hypotheses were named before the look — trend
persistence, relative toll, swing-scale match, whipsaw scarcity, era
concentration — and this module computes every one of them on ALL FIVE panel
assets, ranks how far ZEC sits outside the other four, and prints the answer
whatever the answer turns out to be.

────────────────────────────────────────────────────────────────────────────
THE THREE DESIGN DECISIONS THAT MAKE THIS TABLE READABLE
────────────────────────────────────────────────────────────────────────────

1 · ONE CLOCK: ATR-TIME.  A duration in bars is not comparable across a panel
    whose per-bar volatility differs by 2.2x (median ATR/close is 1.56% on
    BTCUSDT and 3.41% on NEARUSDT).  ATR-time of a half-open bar span [a,b) is
    `sum over its bars of ATR14(4h)[i] / close[i]` — the SAME currency the
    card's own risk unit is denominated in (`r_dist = max(pivot_dist,
    1.0 x ATR)`), so "a long trend" means "long relative to what this asset
    moves" rather than "long on a wall clock".  ALTERNATIVE NAMED AND NOT
    TAKEN: scaling a bar count by a single ATR/close read at the span's first
    bar.  Rejected because tide streaks reach p90 ~ 165 bars and the ATR regime
    drifts materially inside one, so a point scalar mismeasures exactly the
    long streaks the hypothesis is about.

2 · A MATERIALITY GATE STANDS BESIDE THE STATISTICAL ONE, ON THE FACE OF THE
    TABLE.  `sep_gap` and `sep_robust_z` both divide by the other four assets'
    OWN dispersion.  When those four are tightly clustered the denominator
    collapses and an economically trivial difference is reported as a large
    separation.  THE MEASURED INSTANCE FROM THIS ESTATE, and the reason this
    column exists: on `ctr_trig_per_100_window_bars` the other four span
    2.0447 -> 2.1578 and ZEC is 2.0057 — `sep_robust_z = -3.63` on a difference
    of 6% from the pack median.  The statistic is real and the finding is
    nothing.  So `MATERIALITY_FLOOR_PCT = 20.0` is pinned [VETO] before the
    look, `material` is a printed boolean, `verdict` says it in words, and no
    immaterial metric may enter the suitability card however large its gap.

3 · OUTCOME METRICS ARE SEGREGATED FROM EXPLANATORY ONES AND SORT BELOW THEM.
    `net_r`, `expectancy_r` and every era-concentration statistic are computed
    FROM the result.  They cannot explain ZEC — they ARE ZEC.  Every row
    carries `metric_class in {'outcome','explanatory'}`, the ranking sorts
    explanatory first, and no outcome metric can ever be `card_eligible`
    (their `direction_favours` is pinned "none", which forces
    `sign_agrees = False`).  Without this the table's top two rows would be
    `net_r` (sep_gap +1.37) and `expectancy_r` (+1.34) and it would answer
    "why ZEC" with "because ZEC".

────────────────────────────────────────────────────────────────────────────
H-Z4 IS RE-WORDED, AND THE RE-WORDING IS NAMED HERE AND IN A COLUMN
────────────────────────────────────────────────────────────────────────────
H-Z4 AS ORIGINALLY WORDED — "counter-ARMINGS per open window" — IS IDENTICALLY
ZERO BY CONSTRUCTION, for every asset and every arming, and is therefore not a
measurement of anything.  `RC.armings` defines `window_end_i` AS the first
counter 12/89 cross (`scripts/tierc2_rules.py:313-315`), so a counter arming
inside an open window is impossible.  It is computed anyway and printed as
`ctr_arm_12_89_per_window` with `sep_degenerate = "ZERO_BY_CONSTRUCTION"`,
because a degenerate zero IS the finding and deleting it would hide it.

THE RE-WORDING, USED FOR THE SCORED METRIC:
    `ctr_trig_per_100_window_bars` = 100 x (count of AGAINST-DIRECTION 12/26
    TRIGGER crosses inside [arm_i, min(window_end_i, hi_i+1))) / (total open
    window bars).  12/26 is the card's own TRIGGER pair, so this counts
    precisely the churn a trigger-based entry has to survive while its window
    is open.
THE ALTERNATIVE NOT TAKEN: counting counter 12/89 crosses inside the window.
Not taken because that is the event which CLOSES the window and would return
exactly 1.000 per window by definition — a constant, not a measurement.

────────────────────────────────────────────────────────────────────────────
FIVE MORE THINGS THAT CANNOT BE BUILT AS ORIGINALLY SPECIFIED
────────────────────────────────────────────────────────────────────────────
* NO 4h FAN-EPISODE TABLE EXISTS.  `research_outputs/census2b/transitions/`
  covers 5m/15m/30m/1h only (`LENSES_A3`).  4h fans are REBUILT here from
  `ribbons/<ASSET>/4h.parquet` `<FAM>_orient` with `census2b_parta.runs_of`
  plus the two-fans-without-passing-through-mixed split.  The 1h table is NOT
  substituted: it answers a different lens.
* VH AND UH NEVER WARM ON 4h.  `UH_orient` is OR_NA on 100% of bars on all five
  assets; `VH_orient` on 82-98%.  Scored fan families are FAST/M/MH; H is
  printed with its warm share; VH and UH are printed as rows with n_fans = 0
  and a note.  Reported whole, never omitted.
* THE RIBBON PARQUETS DO NOT ALIGN POSITIONALLY with `Frame4h` (15,184 vs
  14,888 rows on BTC).  Every join here is on `open_time`.
* PIVOT SPACING IN BARS HAS ZERO VARIANCE ACROSS THE PANEL — median (5,5) gap
  is 7.0 bars and 200/7 = 28.5714 on all five assets.  MAD = 0 and range = 0,
  so both separation statistics are UNDEFINED, not small.  Printed with
  `sep_degenerate = "OTHERS_IDENTICAL"`; the ATR-time version, where the metric
  does vary, is printed beside it.
* "% OF TOTAL" FOR ERA CONCENTRATION IS UNDEFINED FOR BTC AND NEAR (negative
  net R denominators) and returns 397% for ETH.  Replaced by an HHI on POSITIVE
  MASS (defined and in [0,1] for every asset) plus `net_r_ex_best_*` printed in
  R rather than as a share.

────────────────────────────────────────────────────────────────────────────
WHAT THIS MODULE IS NOT
────────────────────────────────────────────────────────────────────────────
It is a MEASUREMENT and a SELECTION SURFACE, and it says so in a column on
every table it emits.  It touches no `Card` field, no `_ride` branch, no
`card_candidates` gate.  It is imported by nothing in the decision path;
`tierc6.py` must never import it.  `SUITABILITY_CARD` gates nothing and is not
in the FDR family.  n = 5 assets with one positive case: `sep_gap` has NO
sampling distribution and NO p-value, and this table carries no CI column
precisely so that absence is visible rather than filled with something that
looks like one.

HONEST DISCLOSURE ABOUT `direction_favours`: the pins below are declared before
the values are read BY THIS MODULE, but the recon spec that preceded this build
already published measured values for most of these metrics.  The pins are
therefore DECLARED, NOT BLIND, and every fingerprint row carries
`direction_pinned_blind = False` so no reader can mistake the one for the other.
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc6 as T6                                                   # noqa: E402
import tierc6_rules as RC                                             # noqa: E402
import census2b_parta as CP                                           # noqa: E402
import census2b_program as C2B                                        # noqa: E402

r4, r6, iso, log = T6.r4, T6.r6, T6.iso, T6.log
write_table = T6.write_table
UNIVERSE = list(RC.UNIVERSE)
ZEC = "ZECUSDT"

CEN2B = ROOT / "research_outputs" / "census2b"

# ═════════════════════════════════════════ CONSTANTS — [VETO], PINNED BY NAME
# Nothing below is tuned, swept, or chosen after a look at the fingerprint.
MATERIALITY_FLOOR_PCT: float = 20.0     # [VETO] sep_rel_pct floor for the card
SUITABILITY_TOP_K: int = 3              # [VETO] how many screens the card may hold
FAN_FAMILIES_SCORED = ("FAST", "M", "MH")            # [VETO] warm on 4h
FAN_FAMILIES_REPORTED = ("FAST", "M", "MH", "H", "VH", "UH")   # reported whole
REACH_BARS: int = RC.V5.PIVOT_LOOKBACK_4H            # 200 x 4h = 800h
LEG_TOL_INDICATOR_PCT: float = 8.0      # [VETO] analytics-vs-engine EMA tolerance
LEG_TOL_ATR_PCT: float = 5.0            # [VETO] analytics-vs-engine ATR tolerance
LEG_TOL_EXACT: float = 1e-5             # [VETO] same-arithmetic legs are exact

SELECTION_SURFACE_NOTE = (
    "L-ZEC fingerprint metrics — every metric in METRIC_REGISTRY is one cell of "
    "a selection surface whose m was written down BEFORE the look.  Promoting "
    "any row out of this table starts from that m, not from 1.")

DISCLAIMER = (
    "THIS CARD IS NOT A REGISTRATION. It was fitted in-sample on five assets "
    "with one positive case; its thresholds are the other four assets' own "
    "boundary and nothing else; no arm of it was scored against a bar declared "
    "before the result. It gates nothing — it cannot move an entry, an exit, a "
    "stop or a fill, and it is not in the FDR family. Its only correct use is "
    "to say which asset to LOOK at next. Any use of it to decide is a "
    "promotion out of a table that wrote down its m before the look and has "
    "not paid it.")

H_Z4_REWORDING = (
    "RE-WORDED: 'counter-armings per open window' is identically 0 by "
    "construction (armings defines window_end AS the first counter 12/89 "
    "cross), so the scored metric counts AGAINST-DIRECTION 12/26 TRIGGER "
    "crosses inside the open window instead. ALTERNATIVE NOT TAKEN: counting "
    "counter 12/89 crosses — that is the event that CLOSES the window and "
    "would return 1.000 per window by definition.")


# ═══════════════════════════════════════════════════════════════ THE CLOCK
_TAU: dict[str, np.ndarray] = {}


def tau(sym: str) -> np.ndarray:
    """The ATR-clock increment per 4h bar: ATR(14) as a fraction of that bar's
    close, over the FULL loaded history.

    WHAT WOULD MAKE THIS WRONG: reading `atr` or `close` off a restricted
    slice.  `tierc5.frame` builds both over the whole loaded history precisely
    so a corridor edge cannot move them; this returns the FULL-LENGTH array and
    every caller slices it, never the other way round.  Also wrong: letting a
    non-positive or non-finite ratio through as 0.0 — it would silently shorten
    every span that crosses the warm-up.
    """
    if sym not in _TAU:
        f = T6.frame(sym)["f"]
        with np.errstate(invalid="ignore", divide="ignore"):
            t = np.asarray(f.atr, float) / np.asarray(f.c, float)
        _TAU[sym] = np.where(np.isfinite(t) & (t > 0), t, np.nan)
    return _TAU[sym]


def atr_time(sym: str, a: int, b: int) -> float:
    """ATR-time of the HALF-OPEN bar span [a, b) — units: ATR-widths of price.

    WHAT WOULD MAKE THIS WRONG: an inclusive upper bound (every span would
    double-count its final bar and the streak/gap distributions would inflate
    by one bar's worth of ATR), or a negative-width span silently returning 0.0
    instead of NaN.
    """
    if b <= a:
        return float("nan")
    return float(np.nansum(tau(sym)[int(a):int(b)]))


def _corr(sym: str, lo_ms: int, hi_ms: int) -> tuple[int, int]:
    """This asset's inclusive corridor index range, WARM-UP FLOOR APPLIED.

    WHAT WOULD MAKE THIS WRONG: omitting the WARMUP_BARS floor.  `build_4h`
    seeds its EMAs, so at bar 0 e12 == e89 == e316 == close and every tide mask
    is True — a streak measured across the warm-up is an artefact of the seed,
    not a property of the asset.
    """
    f = T6.frame(sym)["f"]
    a, b = T6._idx_range(f.open_ms, lo_ms, hi_ms)
    return max(int(a), int(RC.WARMUP_BARS)), int(b)


# ══════════════════════════════════════════════════════════════ THE BOOKS
_BOOKS: dict[str, list] = {}
BOOK_CARDS = {"v6": RC.CARD_V6, "v5-control": RC.CARD_V5_CONTROL}


def book(name: str = "v6") -> list:
    """The campaign book, ridden through TIER-C6's own code path, cached.

    TWO BOOKS ARE AVAILABLE AND BOTH ARE REPORTED.  'v6' is the card of record
    for this tier (armed trail + minimum advance).  'v5-control' is the same
    code path with every v6 knob off, and it is the book the recon spec's prior
    was measured on — carrying it lets the answer paragraph say whether the
    ZEC finding is a property of the ASSET or of the CARD REVISION.

    WHAT WOULD MAKE THIS WRONG: caching a book against the wrong corridor.  The
    corridor is full water and derived inside, so a caller cannot hand in a
    narrower window and get a cached wider book back.
    """
    if name not in BOOK_CARDS:
        raise SystemExit(f"HALT: unknown book {name!r}; have {sorted(BOOK_CARDS)}")
    if name not in _BOOKS:
        lo, hi, _ = T6.corridor()
        _BOOKS[name] = T6.run_cell(BOOK_CARDS[name], lo, hi)
    return _BOOKS[name]


def _of(bk: list, sym: str) -> list:
    """This asset's campaigns out of a book.

    WHAT WOULD MAKE THIS WRONG: matching on a prefix rather than the exact
    symbol — the panel has no overlapping tickers today, and a prefix match
    would silently start pooling the day it does.
    """
    return [t for t in bk if t.symbol == sym]


def _med(v) -> float:
    """Median over the FINITE values only.

    WHAT WOULD MAKE THIS WRONG: letting NaN through (numpy's median poisons the
    whole answer with one), or returning 0.0 for an empty population — an empty
    population has no median and must say NaN so `provisional` and the n column
    are what the reader looks at.
    """
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return float(np.median(v)) if v.size else float("nan")


def _q(v, p: float) -> float:
    """Percentile over the FINITE values only.  Same failure modes as `_med`."""
    v = np.asarray(v, float)
    v = v[np.isfinite(v)]
    return float(np.percentile(v, p)) if v.size else float("nan")


def _ranks(x: np.ndarray) -> np.ndarray:
    """Average ranks, ties shared — the only ranking used in this module.

    WHAT WOULD MAKE THIS WRONG: breaking ties by position instead of sharing
    the rank.  On a five-point panel two identical values are common (the pivot
    metrics are identical on all five) and a positional tie-break would invent
    an ordering the data does not contain.
    """
    x = np.asarray(x, float)
    order = np.argsort(x, kind="mergesort")
    r = np.empty(len(x), float)
    r[order] = np.arange(1, len(x) + 1, dtype=float)
    for v in np.unique(x):
        m = x == v
        if m.sum() > 1:
            r[m] = r[m].mean()
    return r


def _spearman(x, y) -> float:
    """Spearman rho on n = 5 (or 4) points.  DESCRIPTIVE ONLY — no p-value.

    WHAT WOULD MAKE THIS WRONG: quoting it as a test.  With five assets and one
    of them the hypothesis, a rank correlation is a picture of five points; the
    version that is worth anything is the EX-ZEC one, because a metric that
    orders the other four by their outcome is explaining something and a metric
    that only puts ZEC at the top is restating ZEC.
    """
    x, y = np.asarray(x, float), np.asarray(y, float)
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return float("nan")
    rx, ry = _ranks(x[ok]), _ranks(y[ok])
    sx, sy = rx.std(), ry.std()
    if sx == 0 or sy == 0:
        return float("nan")
    return float(np.mean((rx - rx.mean()) * (ry - ry.mean())) / (sx * sy))


# ═══════════════════════════════════════════════ SEPARATION — AN ACTUAL STAT
def separation(x_z: float, others) -> dict:
    """How far ZEC sits outside the other four, in units of THEIR OWN SPREAD.

    THE RANKING STATISTIC IS `sep_gap`, and it is EXACTLY ZERO when ZEC is
    interior — which is the honest reading of "does not separate", not a small
    number that still sorts above other small numbers.  A z-score is never
    zero, so "ZEC is third of five" would sort above "ZEC is off the end of the
    range"; the robust z is reported alongside as a second opinion and is never
    ranked on.

    WHAT WOULD MAKE THIS WRONG: returning a finite gap when the four others are
    identical (rng == 0 — there is no scale to divide by, so the answer is
    UNDEFINED and must print as such); dividing `sep_rel_pct` by a median of
    zero; or dropping a degenerate row instead of flagging it.  And the
    standing failure mode, which is why `sep_rel_pct` is carried at all: both
    statistics divide by the others' dispersion, so a tightly clustered pack
    turns a 6% difference into a -3.6 z.
    """
    o = np.asarray(others, float)
    o = o[np.isfinite(o)]
    if o.size == 0 or not np.isfinite(x_z):
        return {"others_min": None, "others_max": None, "others_median": None,
                "others_mad": None, "sep_gap": None, "sep_robust_z": None,
                "sep_rel_pct": None, "sep_degenerate": "NO_COMPARATORS",
                "interior": None}
    lo, hi, med = float(o.min()), float(o.max()), float(np.median(o))
    rng = hi - lo
    mad = 1.4826 * float(np.median(np.abs(o - med)))
    interior = bool(lo <= x_z <= hi)
    if interior:
        gap = 0.0
    elif rng > 0:
        gap = ((x_z - hi) if x_z > hi else (x_z - lo)) / rng
    else:
        gap = None
    return {
        "others_min": lo, "others_max": hi, "others_median": med,
        "others_mad": mad,
        "sep_gap": gap,
        "sep_robust_z": ((x_z - med) / mad) if mad > 0 else None,
        "sep_rel_pct": (100.0 * abs(x_z - med) / abs(med)) if med != 0 else None,
        "sep_degenerate": ("" if (rng > 0 and mad > 0 and med != 0)
                           else "OTHERS_IDENTICAL" if rng == 0
                           else "SIGNED_DENOMINATOR"),
        "interior": interior,
    }


# ═══════════════════════════════════════════════════════════════════ H-Z1
def _fan_spans(sym: str, fam: str, a: int, b: int) -> tuple[np.ndarray, np.ndarray, float]:
    """4h fan episodes for one ribbon family, REBUILT (no 4h fan table exists).

    Joined on `open_time`, never positionally — the ribbon parquet carries up
    to 296 more rows than the Frame4h and a positional read would slide every
    orientation against the wrong bar.  A full-order run is split wherever the
    orientation flips without passing through `mixed`, exactly the rule at
    `census2b_parta.py:1068-1073`, so a bull run that becomes a bear run is TWO
    fans and not one long one.

    WHAT WOULD MAKE THIS WRONG: treating OR_NA (-9, not warm) as an
    orientation — UH is OR_NA on 100% of 4h bars and would otherwise report one
    fan spanning the whole corridor; or reading the ribbon positionally.
    """
    p = CEN2B / "ribbons" / sym / "4h.parquet"
    if not p.exists():
        return np.zeros(0), np.zeros(0), float("nan")
    rb = pd.read_parquet(p, columns=["open_time", f"{fam}_orient"])
    f = T6.frame(sym)["f"]
    om = np.asarray(f.open_ms[a:b + 1], np.int64)
    s = pd.Series(rb[f"{fam}_orient"].to_numpy(),
                  index=rb["open_time"].to_numpy(np.int64))
    s = s[~s.index.duplicated(keep="last")]
    orient = s.reindex(om).to_numpy(dtype=float)
    orient = np.where(np.isfinite(orient), orient, float(C2B.OR_NA))
    warm_pct = 100.0 * float(np.mean(orient != C2B.OR_NA))
    ordered = (orient == C2B.OR_BULL) | (orient == C2B.OR_BEAR)
    ats, bars = [], []
    for s0, e0 in CP.runs_of(ordered):
        sub = orient[s0:e0]
        brk = list(np.flatnonzero(np.diff(sub) != 0) + 1)
        for a0, a1 in zip([0] + brk, brk + [e0 - s0]):
            ats.append(atr_time(sym, a + s0 + a0, a + s0 + a1))
            bars.append(a1 - a0)
    return np.array(ats, float), np.array(bars, float), warm_pct


def hz1_scope_table(lo_ms: int | None = None, hi_ms: int | None = None
                    ) -> pd.DataFrame:
    """H-Z1 LONG FORM — tide-streak and fan-duration distributions in ATR-time,
    one row per (asset, scope), EVERY SCOPE REPORTED WHOLE.

    WHAT WOULD MAKE THIS WRONG: a streak measured across the warm-up floor (the
    EMAs are seeded, so bar 0 has e89 == e316 and every mask is True); a fan
    read positionally off the ribbon parquet; or omitting the VH/UH rows
    because they are empty — an empty row that says "not warm on 4h" is a
    finding and a missing row is a silence.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    rows = []
    for sym in UNIVERSE:
        f = T6.frame(sym)["f"]
        a, b = _corr(sym, lo_ms, hi_ms)
        nbars = b - a + 1
        c, e89, e316 = f.c[a:b + 1], f.e89[a:b + 1], f.e316[a:b + 1]
        up = (e89 > e316) & (c > e316)
        dn = (e89 < e316) & (c < e316)
        segs = CP.runs_of(up) + CP.runs_of(dn)
        ats = np.array([atr_time(sym, a + i, a + j) for i, j in segs], float)
        bars = np.array([j - i for i, j in segs], float)
        rows.append(_dist_row(sym, "tide", ats, bars, nbars, 100.0, ""))
        for fam in FAN_FAMILIES_REPORTED:
            fa, fb, warm = _fan_spans(sym, fam, a, b)
            note = ("not warm on 4h" if fa.size == 0 else
                    "warm share printed — interpret with n" if warm < 95.0 else "")
            rows.append(_dist_row(sym, f"fan_{fam}", fa, fb, nbars, warm, note))
    df = pd.DataFrame(rows)
    df["display_only"] = True
    df["gates_nothing"] = True
    return df


def _dist_row(sym: str, scope: str, ats: np.ndarray, bars: np.ndarray,
              nbars: int, warm_pct: float, note: str) -> dict:
    """One distribution row, in bars AND in ATR-time, both reported.

    WHAT WOULD MAKE THIS WRONG: emitting only the ATR-time columns.  ATR-time
    accrues faster on a volatile asset, so a separation that exists in ATR-time
    and not in bars is a volatility restatement — and the reader can only see
    that if both live on the same row.  Also wrong: reporting a median over
    fewer than PROVISIONAL_MIN_N segments without the provisional flag.
    """
    return {
        "asset": sym, "scope": scope, "n_segments": int(bars.size),
        "med_bars": r4(_med(bars)), "p75_bars": r4(_q(bars, 75)),
        "p90_bars": r4(_q(bars, 90)),
        "med_atr_time": r6(_med(ats)), "p75_atr_time": r6(_q(ats, 75)),
        "p90_atr_time": r6(_q(ats, 90)),
        "mean_atr_time": r6(float(np.nanmean(ats)) if ats.size else float("nan")),
        "segments_per_1k_bars": r4(1000.0 * bars.size / nbars) if nbars else None,
        "corridor_bars": int(nbars), "warm_pct": r4(warm_pct), "note": note,
        "provisional": bool(bars.size < RC.PROVISIONAL_MIN_N),
    }


def hz1_table(lo_ms: int | None = None, hi_ms: int | None = None) -> pd.DataFrame:
    """H-Z1 · TREND PERSISTENCE — ONE ROW PER ASSET.

    The hypothesis: ZEC trends persist longer, so a trail-and-ride card gets
    more out of it.  Measured as tide-streak duration (the card's own regime
    predicate, `e89 > e316 and close > e316`, mirrored short) and as 4h ribbon
    fan duration, BOTH in bars and in ATR-time.

    WHAT WOULD MAKE THIS WRONG: reporting only the bar-count version.  Bars and
    ATR-time disagree on this hypothesis — that disagreement IS the H-Z1
    finding — and a table carrying one of them would have answered the question
    with a unit choice.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    lg = hz1_scope_table(lo_ms, hi_ms)
    rows = []
    for sym in UNIVERSE:
        g = lg[lg["asset"] == sym].set_index("scope")
        t = g.loc["tide"]
        row = {
            "asset": sym,
            "corridor_bars": int(t["corridor_bars"]),
            "n_tide_segments": int(t["n_segments"]),
            "tide_med_streak_bars": t["med_bars"],
            "tide_p90_streak_bars": t["p90_bars"],
            "tide_med_streak_atr_time": t["med_atr_time"],
            "tide_p90_streak_atr_time": t["p90_atr_time"],
            "tide_mean_streak_atr_time": t["mean_atr_time"],
            "tide_flips_per_1k_bars": t["segments_per_1k_bars"],
        }
        f = T6.frame(sym)["f"]
        a, b = _corr(sym, lo_ms, hi_ms)
        c, e89, e316 = f.c[a:b + 1], f.e89[a:b + 1], f.e316[a:b + 1]
        up = (e89 > e316) & (c > e316)
        dn = (e89 < e316) & (c < e316)
        n = b - a + 1
        row["asset_up_tide_pct"] = r4(100.0 * float(up.sum()) / n)
        row["asset_down_tide_pct"] = r4(100.0 * float(dn.sum()) / n)
        row["asset_no_tide_pct"] = r4(100.0 * float((~up & ~dn).sum()) / n)
        # THE CONFOUND CONTROL.  ATR-time is a duration in ATR-widths of price,
        # so a high-volatility asset accumulates it faster PER BAR.  Any
        # separation in ATR-time that is absent in bars is a restatement of
        # this column, not a persistence finding — and the reader can only see
        # that if this column is on the same row.
        row["median_atr_pct_of_close"] = r6(100.0 * float(np.nanmedian(tau(sym)[a:b + 1])))
        for fam in FAN_FAMILIES_REPORTED:
            fr = g.loc[f"fan_{fam}"]
            row[f"fan_{fam}_n"] = int(fr["n_segments"])
            row[f"fan_{fam}_warm_pct"] = fr["warm_pct"]
            row[f"fan_{fam}_med_bars"] = fr["med_bars"]
            row[f"fan_{fam}_med_atr_time"] = fr["med_atr_time"]
            row[f"fan_{fam}_p90_atr_time"] = fr["p90_atr_time"]
        row["fan_families_scored"] = ",".join(FAN_FAMILIES_SCORED)
        row["fan_families_not_warm_on_4h"] = "VH,UH"
        row["provisional"] = bool(row["n_tide_segments"] < RC.PROVISIONAL_MIN_N)
        row["display_only"] = True
        row["gates_nothing"] = True
        rows.append(row)
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════ H-Z2
def hz2_table(book_name: str = "v6", lo_ms: int | None = None,
              hi_ms: int | None = None) -> pd.DataFrame:
    """H-Z2 · RELATIVE TOLL — what the card pays to be in the trade, in ATR and
    against the trade's own reach.  ONE ROW PER ASSET.

    `toll_atr` is measured ON THE EVENT POPULATION — this asset's own card
    entries — not over every corridor bar.  That is census2a note m8's
    requirement and the whole reason the number is not a whole-series average:
    entries cluster at compressed ATR, so a whole-series figure UNDERSTATES the
    toll.  Both figures are printed side by side so the reader can see the gap.

    WHAT WOULD MAKE THIS WRONG: dividing a MEDIAN toll by a MEAN MFE (the MFE
    distribution has a heavy right tail and the two are not the same population
    statistic); charging funding at a stamp the corridor does not contain; or
    quoting the capped `funding_r` without the uncapped one beside it, which
    would hide whether the ceiling ever bound.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    bk = book(book_name)
    rows = []
    for sym in UNIVERSE:
        f = T6.frame(sym)["f"]
        a, b = _corr(sym, lo_ms, hi_ms)
        ts = _of(bk, sym)
        idx = np.array([t.entry_i for t in ts], np.int64)
        om = np.asarray(f.open_ms[a:b + 1], np.int64)
        fund = T6.frame(sym)["fund"]
        rate = np.array([fund.get(int(x), 0.0) for x in om], float)
        nz = rate != 0
        cl, av = np.asarray(f.c[a:b + 1], float), np.asarray(f.atr[a:b + 1], float)
        ok = nz & np.isfinite(cl) & np.isfinite(av) & (av > 0)
        toll_evt = CP.toll_atr_for(np.asarray(f.c, float),
                                   np.asarray(f.atr, float), idx)
        toll_all = CP.toll_atr_for(np.asarray(f.c, float),
                                   np.asarray(f.atr, float),
                                   np.arange(a, b + 1, dtype=np.int64))
        med_fee = _med([t.fee_r for t in ts])
        med_fund = _med([t.funding_r for t in ts])
        med_mfe = _med([t.mfe_r for t in ts])
        rows.append({
            "asset": sym, "book": book_name, "n_campaigns": len(ts),
            "toll_atr": r6(toll_evt),
            "toll_atr_whole_corridor": r6(toll_all),
            "toll_event_minus_corridor_atr": r6(toll_evt - toll_all),
            "funding_stamps_n": int(ok.sum()),
            "funding_atr_per_stamp": r6(_med(np.abs(rate[ok]) * cl[ok] / av[ok])),
            "med_fee_r": r6(med_fee), "med_funding_r": r6(med_fund),
            "med_funding_r_uncapped": r6(_med([t.funding_r_uncapped for t in ts])),
            "max_funding_r_uncapped": r6(max((t.funding_r_uncapped for t in ts),
                                             default=float("nan"))),
            "funding_ceiling_bound_n": int(sum(1 for t in ts
                                               if t.funding_ceiling_bound)),
            "med_mfe_r": r6(med_mfe),
            "toll_pct_of_med_mfe": r4(100.0 * (med_fee + med_fund) / med_mfe
                                      if np.isfinite(med_mfe) and med_mfe != 0
                                      else float("nan")),
            "toll_pct_of_med_atr_move": r4(100.0 * toll_evt),
            "provisional": bool(len(ts) < RC.PROVISIONAL_MIN_N),
            "display_only": True, "gates_nothing": True,
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════ H-Z3
def hz3_table(book_name: str = "v6", lo_ms: int | None = None,
              hi_ms: int | None = None) -> pd.DataFrame:
    """H-Z3 · SWING-SCALE MATCH — 4h (5,5) pivot spacing against the card's
    800h anchor reach, plus trail cadence.  ONE ROW PER ASSET.

    THE BAR-COUNT VERSION IS DEGENERATE AND IS PRINTED ANYWAY.  A strict (5,5)
    fractal on any price series gives a median gap of 7.0 bars, so
    `200 / 7 = 28.5714` on all five assets: MAD = 0, range = 0, and the
    separation statistic is UNDEFINED rather than small.  That is a property of
    the pivot kernel, not of any asset, and the degenerate row is the finding.
    The ATR-time version, where the metric does vary, is printed beside it.

    WHAT WOULD MAKE THIS WRONG: reading `low_conf` instead of `low_bar` (the
    confirmation index is the pivot bar plus R, so every gap would be right but
    every REACH would start 5 bars late); measuring the reach forward instead
    of backward (the anchor lookback reaches BACK from the entry bar); or
    computing trail cadence over campaigns from a different book than the one
    named in `book`.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    bk = book(book_name)
    rows = []
    for sym in UNIVERSE:
        f = T6.frame(sym)["f"]
        a, b = _corr(sym, lo_ms, hi_ms)
        pv = T6.frame(sym)["pv4"]
        bars = np.unique(np.concatenate([np.asarray(pv.low_bar, np.int64),
                                         np.asarray(pv.high_bar, np.int64)]))
        bars = bars[(bars >= a) & (bars <= b)]
        gaps = np.diff(bars).astype(float) if bars.size > 1 else np.zeros(0)
        gaps_at = np.array([atr_time(sym, int(bars[k]), int(bars[k + 1]))
                            for k in range(len(bars) - 1)], float)
        reach = np.array([atr_time(sym, max(a, int(i) - REACH_BARS), int(i))
                          for i in bars], float)
        ts = _of(bk, sym)
        nadv = np.array([len(t.advances) for t in ts], float)
        adv_atr, first_bars, rail = [], [], []
        for t in ts:
            for k, adv in enumerate(t.advances):
                adv_atr.append(abs(float(adv.new_stop) - float(adv.prev_stop))
                               / float(adv.atr))
                rail.append(bool(adv.rail_binding))
                if k == 0:
                    first_bars.append(adv.conf_i - t.entry_i)
        med_gap_b, med_gap_at = _med(gaps), _med(gaps_at)
        med_reach = _med(reach)
        rows.append({
            "asset": sym, "book": book_name,
            "n_pivots": int(bars.size),
            "piv_med_gap_bars": r4(med_gap_b),
            "piv_p75_gap_bars": r4(_q(gaps, 75)),
            "piv_p90_gap_bars": r4(_q(gaps, 90)),
            "piv_med_gap_atr_time": r6(med_gap_at),
            "piv_p90_gap_atr_time": r6(_q(gaps_at, 90)),
            "reach_bars": int(REACH_BARS),
            "reach_med_atr_time": r6(med_reach),
            "pivots_per_reach_bars": r4(REACH_BARS / med_gap_b
                                        if med_gap_b else float("nan")),
            "pivots_per_reach_atr_time": r4(med_reach / med_gap_at
                                            if med_gap_at else float("nan")),
            "n_campaigns": len(ts),
            "adv_per_campaign": r4(float(np.mean(nadv)) if nadv.size else float("nan")),
            "n_advances": int(nadv.sum()),
            "adv_med_atr": r6(_med(adv_atr)),
            "med_bars_to_first_advance": r4(_med(first_bars)),
            "pct_campaigns_zero_advance": r4(100.0 * float((nadv == 0).mean())
                                             if nadv.size else float("nan")),
            "rail_binding_pct": r4(100.0 * float(np.mean(rail)) if rail
                                   else float("nan")),
            "provisional": bool(len(ts) < RC.PROVISIONAL_MIN_N),
            "display_only": True, "gates_nothing": True,
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════════ H-Z4
def hz4_table(lo_ms: int | None = None, hi_ms: int | None = None) -> pd.DataFrame:
    """H-Z4 · WHIPSAW SCARCITY — RE-WORDED.  ONE ROW PER ASSET.

    THE RE-WORDING IS A COLUMN (`rewording`), not a footnote, because a caption
    does not survive a copy of the row into somebody else's spreadsheet.  See
    `H_Z4_REWORDING`.  The degenerate original is computed and printed as
    `ctr_arm_12_89_per_window`, which is 0.0 for every asset BY CONSTRUCTION.

    Cross-check columns are lifted from `research_outputs/census2b/windows/
    <ASSET>/4h.parquet` — an INDEPENDENTLY BUILT census of the same object,
    with its own arming detector and its own window closer.  They are a second
    opinion, not a re-derivation of this table by the same route.

    WHAT WOULD MAKE THIS WRONG: counting the PRO-direction trigger as churn
    (that is the entry, not the whipsaw); letting a window run past the
    corridor edge (`end` is clipped to `hi_i + 1`); or dividing the counter
    count by the number of windows instead of by open-window BARS, which would
    make a long window look quiet merely for being long.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    rows = []
    for sym in UNIVERSE:
        f = T6.frame(sym)["f"]
        x = T6.frame(sym)["x"]
        a, b = _corr(sym, lo_ms, hi_ms)
        arms = RC.armings(sym, f, a, b)
        ctr, ctr89, sbars, sat, reach_trig = [], [], [], [], []
        for A in arms:
            end = min(int(A.window_end_i), b + 1)
            if end <= A.arm_i:
                end = A.arm_i + 1
            anti = x["t_dn"] if A.direction == 1 else x["t_up"]
            pro = x["t_up"] if A.direction == 1 else x["t_dn"]
            opp = x["w_dn"] if A.direction == 1 else x["w_up"]
            ctr.append(int(np.asarray(anti[A.arm_i:end]).sum()))
            ctr89.append(int(np.asarray(opp[A.arm_i + 1:end]).sum()))
            sbars.append(end - A.arm_i)
            sat.append(atr_time(sym, A.arm_i, end))
            reach_trig.append(bool(np.asarray(pro[A.arm_i:end]).any()))
        n = len(arms)
        sb = np.array(sbars, float)
        c2b = _c2b_windows(sym)
        rows.append({
            "asset": sym, "n_armings": n,
            "rewording": H_Z4_REWORDING,
            "ctr_trig_per_window": r6(float(np.mean(ctr)) if ctr else float("nan")),
            "ctr_trig_per_100_window_bars": r6(100.0 * float(np.sum(ctr))
                                               / float(sb.sum()) if sb.sum() else
                                               float("nan")),
            "ctr_arm_12_89_per_window": r6(float(np.mean(ctr89)) if ctr89
                                           else float("nan")),
            "ctr_arm_12_89_total": int(np.sum(ctr89)) if ctr89 else 0,
            "win_med_bars": r4(_med(sb)), "win_p90_bars": r4(_q(sb, 90)),
            "win_med_atr_time": r6(_med(sat)), "win_p90_atr_time": r6(_q(sat, 90)),
            "pct_windows_reaching_trigger": r4(100.0 * float(np.mean(reach_trig))
                                               if reach_trig else float("nan")),
            "pct_windows_passing_tide": r4(100.0 * float(np.mean(
                [A.tide_ok for A in arms])) if n else float("nan")),
            "pct_windows_passing_d": r4(100.0 * float(np.mean(
                [A.d_ok for A in arms])) if n else float("nan")),
            "n_windows_c2b": c2b["n"],
            "med_window_width_bars_c2b": c2b["med_width"],
            "pct_has_trigger_c2b": c2b["pct_trig"],
            "med_refusal_per_1k_bars_24h": c2b["med_refusal"],
            "med_MH_fan_age_c2b": c2b["med_mh_age"],
            "degenerate_note": ("ctr_arm_12_89_per_window is 0.0 BY "
                                "CONSTRUCTION — armings defines window_end AS "
                                "the first counter 12/89 cross"),
            "provisional": bool(n < RC.PROVISIONAL_MIN_N),
            "display_only": True, "gates_nothing": True,
        })
    return pd.DataFrame(rows)


def _c2b_windows(sym: str) -> dict:
    """The independently-filed census2b 4h window census, as a second opinion.

    WHAT WOULD MAKE THIS WRONG: treating a difference between this and the
    program's own arming count as an error.  census2b arms on its own detector
    over its own corridor; the columns are a SECOND OPINION on the shape of the
    object, and the row count is printed so the reader can see they are not the
    same population.
    """
    p = CEN2B / "windows" / sym / "4h.parquet"
    if not p.exists():
        return {"n": 0, "med_width": None, "pct_trig": None,
                "med_refusal": None, "med_mh_age": None}
    d = pd.read_parquet(p)
    return {
        "n": int(len(d)),
        "med_width": r4(_med(d["window_width_bars"].to_numpy(float))),
        "pct_trig": r4(100.0 * float(d["has_trigger"].astype(bool).mean())),
        "med_refusal": r4(_med(d["refusal_per_1k_bars_24h"].to_numpy(float))),
        "med_mh_age": r4(_med(d["MH_fan_age"].to_numpy(float))),
    }


# ═══════════════════════════════════════════════════════════════════ H-Z5
def hz5_slice_table(book_name: str = "v6", base_name: str = "v5-control",
                    lo_ms: int | None = None, hi_ms: int | None = None
                    ) -> pd.DataFrame:
    """H-Z5 LONG FORM — one row per (asset, slice_group, slice_key), REPORTED
    WHOLE including every slice in which an asset has n = 0.

    THE D15 COLUMNS RIDE THESE ROWS AND GATE NOTHING.  They are paired against
    the `base_name` book (the v5 control) rather than against the panel, because
    pairing a subset against its own superset gives a delta of exactly zero and
    would be a column that cannot be wrong.

    WHAT WOULD MAKE THIS WRONG: dropping the n = 0 slices (a book that vanishes
    in an era is the era finding), or letting a slice row be read without its
    window label — every row carries `slice_group`/`slice_key`/`slice_from`/
    `slice_to` for exactly that reason [F-C5-a].
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    bk, base = book(book_name), book(base_name)
    spans = [(g, k, a, b) for g, k, a, b in T6.slices_of(lo_ms, hi_ms)]
    rows = []
    for sym in UNIVERSE:
        ba = _of(bk, sym)
        bb = _of(base, sym)
        for g, k, a, b in spans:
            cell = [t for t in ba if a <= t.entry_ms <= b]
            bcell = [t for t in bb if a <= t.entry_ms <= b]
            row = dict(T6.agg(cell, "asset_slice", k))
            row.update(T6.d15(cell, bcell))
            row.update({"asset": sym, "book": book_name, "d15_base": base_name,
                        "slice_group": g, "slice_key": k,
                        "slice_from": iso(a), "slice_to": iso(b)})
            row.update(_asset_tide_mix(sym, a, b))
            rows.append(row)
    df = pd.DataFrame(rows)
    df["in_sample"] = True
    df["display_only"] = True
    df["gates_nothing"] = True
    front = ["asset", "book", "slice_group", "slice_key", "slice_from", "slice_to"]
    return df[front + [c for c in df.columns if c not in front]]


def _asset_tide_mix(sym: str, lo_ms: int, hi_ms: int) -> dict:
    """PER-ASSET tide mix over a span.  `tierc5.tide_mix` is PANEL-wide; a
    per-asset slice row needs its own asset's regime, not the panel's.

    WHAT WOULD MAKE THIS WRONG: quoting the panel mix on an asset row — a
    9-of-11-shorts ZEC book in a ZEC down-tide is a different object from the
    same book in a panel-average one.
    """
    f = T6.frame(sym)["f"]
    a, b = _corr(sym, lo_ms, hi_ms)
    if b < a:
        return {"asset_up_tide_pct": None, "asset_down_tide_pct": None,
                "asset_no_tide_pct": None, "asset_slice_bars": 0}
    c, e89, e316 = f.c[a:b + 1], f.e89[a:b + 1], f.e316[a:b + 1]
    up = (e89 > e316) & (c > e316)
    dn = (e89 < e316) & (c < e316)
    n = b - a + 1
    return {"asset_up_tide_pct": r4(100.0 * float(up.sum()) / n),
            "asset_down_tide_pct": r4(100.0 * float(dn.sum()) / n),
            "asset_no_tide_pct": r4(100.0 * float((~up & ~dn).sum()) / n),
            "asset_slice_bars": int(n)}


def hz5_table(book_name: str = "v6", base_name: str = "v5-control",
              lo_ms: int | None = None, hi_ms: int | None = None) -> pd.DataFrame:
    """H-Z5 · ERA CONCENTRATION — ONE ROW PER ASSET.  EVERY METRIC HERE IS AN
    OUTCOME METRIC AND CANNOT EXPLAIN ANYTHING.

    "% of total" is UNDEFINED for two of five assets: BTC and NEAR book NEGATIVE
    net R, so `best_year / total` is a share of a negative denominator, and ETH
    returns 397% for the same reason.  The concentration statistic is therefore
    a HERFINDAHL ON POSITIVE MASS — `sum over years of (max(0, net_r_y) / sum
    of max(0, net_r_y))^2` — which is defined and in [0,1] for every asset, and
    `net_r_ex_best_*` is printed IN R rather than as a share, because a share is
    what breaks.

    WHAT WOULD MAKE THIS WRONG: an HHI computed over a year set that differs
    per asset (it does — assets list at different dates — so the denominator is
    that asset's own positive mass and `years_present` is printed beside it), or
    quoting `best_campaign_pos_share_pct` without the campaign's own timestamp,
    which is what makes the number checkable against the journal.
    """
    if lo_ms is None:
        lo_ms, hi_ms, _ = T6.corridor()
    bk, base = book(book_name), book(base_name)
    rows = []
    for sym in UNIVERSE:
        ts = _of(bk, sym)
        r = np.array([float(t.net_r) for t in ts], float)
        years = sorted(set(iso(t.entry_ms)[:4] for t in ts))
        by_year = {y: float(sum(t.net_r for t in ts if iso(t.entry_ms)[:4] == y))
                   for y in years}
        pos = {y: max(0.0, v) for y, v in by_year.items()}
        spos = sum(pos.values())
        hhi = (sum((v / spos) ** 2 for v in pos.values()) if spos > 0 else None)
        best_y = max(pos, key=lambda y: pos[y]) if pos else None
        pos_camp = float(np.sum(np.maximum(r, 0.0))) if r.size else 0.0
        jbest = int(np.argmax(r)) if r.size else -1
        base_a = _of(base, sym)
        ex_best_year = [t for t in ts if iso(t.entry_ms)[:4] != best_y]
        row = {
            "asset": sym, "book": book_name,
            "n_campaigns": len(ts),
            "net_r": r4(float(r.sum())) if r.size else None,
            "expectancy_r": r4(float(r.mean())) if r.size else None,
            "win_rate_pct": r4(100.0 * float((r > 0).mean())) if r.size else None,
            "years_present": len(years),
            "years_with_positive_net_r": int(sum(1 for v in by_year.values() if v > 0)),
            "hhi_of_positive_mass": r6(hhi),
            "best_year": best_y,
            "best_year_net_r": r4(by_year.get(best_y)) if best_y else None,
            "best_year_pos_share_pct": r4(100.0 * pos[best_y] / spos)
            if (best_y and spos > 0) else None,
            "best_campaign_net_r": r4(float(r[jbest])) if jbest >= 0 else None,
            "best_campaign_entry_ts": iso(ts[jbest].entry_ms) if jbest >= 0 else None,
            "best_campaign_exit_ts": iso(ts[jbest].exit_ms) if jbest >= 0 else None,
            "best_campaign_pos_share_pct": r4(100.0 * float(r[jbest]) / pos_camp)
            if pos_camp > 0 else None,
            # THE FAMILIAR "% OF TOTAL" — AND WHY IT IS NOT THE RANKED METRIC.
            # It is None wherever net R is not strictly positive, which on this
            # panel is BTCUSDT and NEARUSDT, and on ETHUSDT it can exceed 100%.
            # Printed so the reader can see the hole the HHI was built to fill.
            "best_campaign_share_of_net_r_pct": (
                r4(100.0 * float(r[jbest]) / float(r.sum()))
                if r.size and float(r.sum()) > 0 else None),
            "share_of_net_r_undefined_reason": (
                "" if (r.size and float(r.sum()) > 0)
                else "net_r <= 0 — a share of a non-positive denominator is "
                     "not a share"),
            "net_r_ex_best_campaign": r4(float(r.sum() - r[jbest])) if r.size else None,
            "net_r_ex_best_year": r4(float(sum(t.net_r for t in ex_best_year))),
            "expectancy_ex_best_year": r4(float(np.mean([t.net_r for t in ex_best_year]))
                                          if ex_best_year else float("nan")),
            "n_ex_best_year": len(ex_best_year),
            "share_of_panel_net_r_pct": None,     # filled below
            "provisional": bool(len(ts) < RC.PROVISIONAL_MIN_N),
            "in_sample": True, "display_only": True, "gates_nothing": True,
            "metric_class_note": "EVERY column on this row is an OUTCOME of the "
                                 "card; none of it can explain ZEC",
        }
        row.update(T6.d15(ts, base_a))
        rows.append(row)
    df = pd.DataFrame(rows)
    tot = float(sum(t.net_r for t in bk))
    df["share_of_panel_net_r_pct"] = [
        r4(100.0 * v / tot) if tot else None for v in df["net_r"].astype(float)]
    df["panel_net_r"] = r4(tot)
    return df


# ════════════════════════════════════════════════════ THE METRIC REGISTRY
# PINNED BEFORE THE LOOK BY THIS MODULE.  `direction_favours` says which way a
# value must move for the hypothesis to be SUPPORTED, and it is pinned here so
# that a metric which separates in the WRONG direction cannot be read as
# evidence for the hypothesis it belongs to.  `metric_class = 'outcome'` marks
# every quantity computed FROM the result; those are pinned `direction_favours
# = "none"` which makes `sign_agrees` False and `card_eligible` impossible.
METRIC_REGISTRY: tuple[dict, ...] = (
    # ── H-Z1 · persistence ────────────────────────────────────────────────
    dict(metric="tide_med_streak_bars", hypothesis="H-Z1", family="persistence",
         units="bars", favours="high", cls="explanatory", table="hz1",
         col="tide_med_streak_bars", n_col="n_tide_segments",
         why="a trail-and-ride card wants long regimes; longer median streak "
             "supports H-Z1"),
    dict(metric="tide_med_streak_atr_time", hypothesis="H-Z1",
         family="persistence", units="atr_time", favours="high",
         cls="explanatory", table="hz1", col="tide_med_streak_atr_time",
         n_col="n_tide_segments",
         why="the same claim in the currency the card's risk is denominated in"),
    dict(metric="tide_p90_streak_atr_time", hypothesis="H-Z1",
         family="persistence", units="atr_time", favours="high",
         cls="explanatory", table="hz1", col="tide_p90_streak_atr_time",
         n_col="n_tide_segments",
         why="the card is paid by the tail of the streak distribution, not its "
             "middle"),
    dict(metric="tide_flips_per_1k_bars", hypothesis="H-Z1",
         family="persistence", units="count", favours="low", cls="explanatory",
         table="hz1", col="tide_flips_per_1k_bars", n_col="n_tide_segments",
         why="fewer regime flips is the same claim from the other side"),
    dict(metric="fan_FAST_med_atr_time", hypothesis="H-Z1", family="persistence",
         units="atr_time", favours="high", cls="explanatory", table="hz1",
         col="fan_FAST_med_atr_time", n_col="fan_FAST_n",
         why="ordered-ribbon episodes are the estate's independent read of "
             "'trending'"),
    dict(metric="fan_M_med_atr_time", hypothesis="H-Z1", family="persistence",
         units="atr_time", favours="high", cls="explanatory", table="hz1",
         col="fan_M_med_atr_time", n_col="fan_M_n", why="as FAST, mid ribbon"),
    dict(metric="fan_MH_med_atr_time", hypothesis="H-Z1", family="persistence",
         units="atr_time", favours="high", cls="explanatory", table="hz1",
         col="fan_MH_med_atr_time", n_col="fan_MH_n",
         why="as FAST, the slowest family that warms on 4h at >88%"),
    # THE SAME THREE IN BARS.  Carried so that an ATR-time separation which is
    # absent in bars is visible as a VOLATILITY restatement rather than a
    # persistence finding.  Bars and ATR-time disagreeing IS the H-Z1 result.
    dict(metric="fan_FAST_med_bars", hypothesis="H-Z1", family="persistence",
         units="bars", favours="high", cls="explanatory", table="hz1",
         col="fan_FAST_med_bars", n_col="fan_FAST_n",
         why="the bar-count companion to fan_FAST_med_atr_time"),
    dict(metric="fan_M_med_bars", hypothesis="H-Z1", family="persistence",
         units="bars", favours="high", cls="explanatory", table="hz1",
         col="fan_M_med_bars", n_col="fan_M_n",
         why="the bar-count companion to fan_M_med_atr_time"),
    dict(metric="fan_MH_med_bars", hypothesis="H-Z1", family="persistence",
         units="bars", favours="high", cls="explanatory", table="hz1",
         col="fan_MH_med_bars", n_col="fan_MH_n",
         why="the bar-count companion to fan_MH_med_atr_time"),
    dict(metric="median_atr_pct_of_close", hypothesis="H-Z1",
         family="persistence", units="pct", favours="none", cls="explanatory",
         table="hz1", col="median_atr_pct_of_close", n_col="corridor_bars",
         confound=True,
         why="CONFOUND CONTROL, not a hypothesis metric. ATR-time accrues "
             "faster on a more volatile asset, so every atr_time row must be "
             "read against this one. Pinned direction 'none' — it can never be "
             "card-eligible, because 'ZEC is volatile' is not an explanation "
             "of why the card wins on it"),
    # ── H-Z2 · toll ───────────────────────────────────────────────────────
    dict(metric="toll_atr", hypothesis="H-Z2", family="toll", units="atr",
         favours="low", cls="explanatory", table="hz2", col="toll_atr",
         n_col="n_campaigns",
         why="a cheaper round trip relative to the asset's own ATR leaves more "
             "of the move for the card"),
    dict(metric="funding_atr_per_stamp", hypothesis="H-Z2", family="toll",
         units="atr", favours="low", cls="explanatory", table="hz2",
         col="funding_atr_per_stamp", n_col="funding_stamps_n",
         why="the carry cost of holding a multi-day campaign, in ATR"),
    dict(metric="toll_pct_of_med_mfe", hypothesis="H-Z2", family="toll",
         units="pct", favours="low", cls="explanatory", table="hz2",
         col="toll_pct_of_med_mfe", n_col="n_campaigns", denom_outcome=True,
         why="cost measured against the reach the campaign actually got"),
    dict(metric="med_fee_r", hypothesis="H-Z2", family="toll", units="R",
         favours="low", cls="explanatory", table="hz2", col="med_fee_r",
         n_col="n_campaigns",
         why="the fee in the card's own risk unit — small R means the stop is "
             "wide relative to price"),
    dict(metric="med_funding_r", hypothesis="H-Z2", family="toll", units="R",
         favours="low", cls="explanatory", table="hz2", col="med_funding_r",
         n_col="n_campaigns", why="the carry in the card's own risk unit"),
    # ── H-Z3 · swing scale ────────────────────────────────────────────────
    dict(metric="piv_med_gap_bars", hypothesis="H-Z3", family="swing_scale",
         units="bars", favours="high", cls="explanatory", table="hz3",
         col="piv_med_gap_bars", n_col="n_pivots",
         why="wider swings mean the 800h anchor window spans fewer, cleaner "
             "structures"),
    dict(metric="piv_med_gap_atr_time", hypothesis="H-Z3", family="swing_scale",
         units="atr_time", favours="high", cls="explanatory", table="hz3",
         col="piv_med_gap_atr_time", n_col="n_pivots",
         why="the same claim in ATR-time, where the bar-count version is "
             "degenerate"),
    dict(metric="pivots_per_reach_bars", hypothesis="H-Z3", family="swing_scale",
         units="ratio", favours="low", cls="explanatory", table="hz3",
         col="pivots_per_reach_bars", n_col="n_pivots",
         why="how many swings the anchor lookback must choose among"),
    dict(metric="pivots_per_reach_atr_time", hypothesis="H-Z3",
         family="swing_scale", units="ratio", favours="low", cls="explanatory",
         table="hz3", col="pivots_per_reach_atr_time", n_col="n_pivots",
         why="THE swing-scale-match number: swings per anchor window in the "
             "asset's own volatility currency"),
    dict(metric="adv_per_campaign", hypothesis="H-Z3", family="swing_scale",
         units="count", favours="high", cls="explanatory", table="hz3",
         col="adv_per_campaign", n_col="n_campaigns", denom_outcome=True,
         why="trail cadence — a well-matched asset lets the ratchet advance "
             "repeatedly"),
    dict(metric="pct_campaigns_zero_advance", hypothesis="H-Z3",
         family="swing_scale", units="pct", favours="low", cls="explanatory",
         table="hz3", col="pct_campaigns_zero_advance", n_col="n_campaigns",
         denom_outcome=True,
         why="the share of campaigns the trail never touched at all"),
    # ── H-Z4 · whipsaw ────────────────────────────────────────────────────
    dict(metric="ctr_trig_per_100_window_bars", hypothesis="H-Z4",
         family="whipsaw", units="count", favours="low", cls="explanatory",
         table="hz4", col="ctr_trig_per_100_window_bars", n_col="n_armings",
         why="RE-WORDED metric: against-direction 12/26 trigger crosses per 100 "
             "open-window bars — the churn a trigger entry must survive"),
    dict(metric="ctr_arm_12_89_per_window", hypothesis="H-Z4", family="whipsaw",
         units="count", favours="low", cls="explanatory", table="hz4",
         col="ctr_arm_12_89_per_window", n_col="n_armings",
         why="THE ORIGINAL WORDING, printed to show it is 0.0 by construction"),
    dict(metric="win_med_atr_time", hypothesis="H-Z4", family="whipsaw",
         units="atr_time", favours="high", cls="explanatory", table="hz4",
         col="win_med_atr_time", n_col="n_armings",
         why="a window that survives longer gives the trigger more room"),
    dict(metric="win_med_bars", hypothesis="H-Z4", family="whipsaw",
         units="bars", favours="high", cls="explanatory", table="hz4",
         col="win_med_bars", n_col="n_armings",
         why="the same in bars, so the unit choice is visible"),
    dict(metric="pct_windows_reaching_trigger", hypothesis="H-Z4",
         family="whipsaw", units="pct", favours="high", cls="explanatory",
         table="hz4", col="pct_windows_reaching_trigger", n_col="n_armings",
         why="how often an open window produces the entry event at all"),
    # ── H-Z5 · era · EVERY ROW IS AN OUTCOME METRIC ───────────────────────
    dict(metric="net_r", hypothesis="H-Z5", family="era", units="R",
         favours="none", cls="outcome", table="hz5", col="net_r",
         n_col="n_campaigns", why="THIS IS THE THING BEING EXPLAINED"),
    dict(metric="expectancy_r", hypothesis="H-Z5", family="era", units="R",
         favours="none", cls="outcome", table="hz5", col="expectancy_r",
         n_col="n_campaigns", why="THIS IS THE THING BEING EXPLAINED, per trade"),
    dict(metric="win_rate_pct", hypothesis="H-Z5", family="era", units="pct",
         favours="none", cls="outcome", table="hz5", col="win_rate_pct",
         n_col="n_campaigns", why="outcome"),
    dict(metric="hhi_of_positive_mass", hypothesis="H-Z5", family="era",
         units="ratio", favours="none", cls="outcome", table="hz5",
         col="hhi_of_positive_mass", n_col="n_campaigns",
         why="Herfindahl on positive yearly mass — defined where '% of total' "
             "is not"),
    dict(metric="best_year_pos_share_pct", hypothesis="H-Z5", family="era",
         units="pct", favours="none", cls="outcome", table="hz5",
         col="best_year_pos_share_pct", n_col="n_campaigns", why="outcome"),
    dict(metric="best_campaign_pos_share_pct", hypothesis="H-Z5", family="era",
         units="pct", favours="none", cls="outcome", table="hz5",
         col="best_campaign_pos_share_pct", n_col="n_campaigns",
         why="THE headline concentration number, and an outcome of the ride"),
    dict(metric="net_r_ex_best_campaign", hypothesis="H-Z5", family="era",
         units="R", favours="none", cls="outcome", table="hz5",
         col="net_r_ex_best_campaign", n_col="n_campaigns",
         why="printed in R because the share version breaks on a negative "
             "denominator"),
    dict(metric="expectancy_ex_best_year", hypothesis="H-Z5", family="era",
         units="R", favours="none", cls="outcome", table="hz5",
         col="expectancy_ex_best_year", n_col="n_ex_best_year", why="outcome"),
)


# METRICS MEASURED ON REALISED CAMPAIGNS — i.e. conditioned on the trades the
# card actually took.  These are NOT outcome metrics (they do not contain the
# P&L), but they are not free of the card either: change the entry rule and the
# population changes.  Listed by name, pinned here, printed as a column.
REALISED_METRICS = frozenset({
    "toll_atr", "toll_pct_of_med_mfe", "med_fee_r", "med_funding_r",
    "adv_per_campaign", "pct_campaigns_zero_advance",
    "net_r", "expectancy_r", "win_rate_pct", "hhi_of_positive_mass",
    "best_year_pos_share_pct", "best_campaign_pos_share_pct",
    "net_r_ex_best_campaign", "expectancy_ex_best_year",
})


def _norm_tables(tables: dict) -> dict[str, pd.DataFrame]:
    """Accept the driver's table dict in either shape it is written in.

    `tierc6.run` builds `{h: hz{h}_table() for h in (1,2,3,4,5)}` — INTEGER
    keys — and hands that straight to `fingerprint` and `answer_paragraph`;
    `all_tables` here builds string keys and carries two extra long-form
    tables.  Both are legal inputs and both are normalised to `hz1`..`hz5`.

    WHAT WOULD MAKE THIS WRONG: silently inventing a missing table.  A key this
    module needs and cannot find HALTs with the key it wanted, because a lab
    that quietly returns a short fingerprint is the failure mode the whole
    reported-whole discipline exists to prevent.
    """
    out: dict[str, pd.DataFrame] = {}
    for k, v in tables.items():
        key = str(k)
        if not key.startswith("hz"):
            key = f"hz{key}"
        out[key] = v
    need = sorted({spec["table"] for spec in METRIC_REGISTRY} | {"hz1", "hz2",
                                                                 "hz5"})
    missing = [k for k in need if k not in out]
    if missing:
        raise SystemExit(f"HALT: L-ZEC was handed a table dict missing {missing}; "
                         f"got keys {sorted(map(str, tables))}")
    return out


def all_tables(book_name: str = "v6") -> dict[str, pd.DataFrame]:
    """Every hypothesis table, keyed by the name the registry points at.

    WHAT WOULD MAKE THIS WRONG: building two of these on different books.  One
    `book_name` threads through all of them and is printed as a column on each,
    so a fingerprint row cannot mix a v6 outcome with a v5 structure.
    """
    lo, hi, _ = T6.corridor()
    return {
        "hz1": hz1_table(lo, hi),
        "hz2": hz2_table(book_name, lo, hi),
        "hz3": hz3_table(book_name, lo, hi),
        "hz4": hz4_table(lo, hi),
        "hz5": hz5_table(book_name, lo_ms=lo, hi_ms=hi),
        "hz1_scope": hz1_scope_table(lo, hi),
        "hz5_slice": hz5_slice_table(book_name, lo_ms=lo, hi_ms=hi),
    }


# ═══════════════════════════════════════════════════ THE FINGERPRINT TABLE
def fingerprint(tables: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """THE DELIVERABLE — every metric x every asset, with ZEC's separation
    RANKED, its MATERIALITY beside it, and outcome metrics segregated.

    REPORTED WHOLE: exactly one row per METRIC_REGISTRY entry, including every
    `sep_gap == 0.0` row (ZEC interior — the honest "does not separate") and
    every degenerate row.  `len(fingerprint) == len(METRIC_REGISTRY)` is
    asserted before return, as a CARDINALITY check: a filter that silently
    dropped 60% of the rows would leave every spot-check green.

    THE RANKING RULE, total and deterministic:
        card_eligible DESC, is_outcome_metric ASC, |sep_gap| DESC,
        sep_rel_pct DESC, metric ASC
    `is_outcome_metric ASC` is load-bearing.  The two largest separations in the
    estate are `net_r` and `expectancy_r`; if they sorted first the table would
    answer "why ZEC" with "because ZEC".

    THIS IS A SELECTION SURFACE AND SAYS SO IN A COLUMN.

    WHAT WOULD MAKE THIS WRONG: ranking on `sep_robust_z` (never zero, so an
    interior asset outranks an exterior one); letting an immaterial row be
    `card_eligible` (a 6% pack difference with a collapsed denominator is the
    estate's own worst false separator); dropping the degenerate rows; or
    reading a metric column off a table built on a different book.
    """
    tables = _norm_tables(tables)
    net_by_asset = tables["hz5"].set_index("asset")["net_r"].astype(float)
    rows = []
    for spec in METRIC_REGISTRY:
        df = tables[spec["table"]]
        if spec["col"] not in df.columns:
            raise SystemExit(f"HALT: metric {spec['metric']!r} names column "
                             f"{spec['col']!r} absent from table {spec['table']!r}")
        v = df.set_index("asset")[spec["col"]]
        vals = {s: (float(v[s]) if v.get(s) is not None
                    and np.isfinite(float(v[s] if v[s] is not None else np.nan))
                    else float("nan")) for s in UNIVERSE}
        x_z = vals[ZEC]
        sep = separation(x_z, [vals[s] for s in UNIVERSE if s != ZEC])
        n_zec = df.set_index("asset")[spec["n_col"]].get(ZEC)
        n_zec = int(n_zec) if n_zec is not None and np.isfinite(float(n_zec)) else 0
        is_out = spec["cls"] == "outcome"
        # ZEC's rank among the five values, DESCENDING (1 = the largest).
        finite = {s: x for s, x in vals.items() if np.isfinite(x)}
        rank = (1 + sum(1 for s, x in finite.items() if x > x_z)
                if np.isfinite(x_z) else None)
        material = bool(sep["sep_rel_pct"] is not None
                        and sep["sep_rel_pct"] >= MATERIALITY_FLOOR_PCT)
        fav = spec["favours"]
        med = sep["others_median"]
        if fav == "none" or med is None or not np.isfinite(x_z):
            sign_ok = False
        elif fav == "high":
            sign_ok = bool(x_z > med)
        else:
            sign_ok = bool(x_z < med)
        gap = sep["sep_gap"]
        eligible = bool(material and sign_ok and gap not in (None, 0.0)
                        and sep["sep_degenerate"] == "" and not is_out)
        degen = sep["sep_degenerate"]
        if spec["metric"] == "ctr_arm_12_89_per_window":
            degen = "ZERO_BY_CONSTRUCTION"
        # THE BOUNDARY AND THE EXCEEDANCE — the SECOND materiality axis, and it
        # is a different one from `sep_rel_pct`.  `sep_rel_pct` measures the
        # distance from the pack MEDIAN, so a widely spread pack can make a
        # value that only just clears the pack MAXIMUM look far away.  This
        # pair says how far past the other four's own edge ZEC actually is, in
        # the metric's own units and as a percentage OF THAT EDGE.  It is
        # PRINTED AND NOT GATED: a second floor pinned after this table was
        # first read would be a knob fitted on the answer, which is exactly the
        # move MATERIALITY_FLOOR_PCT exists to forbid.
        omin, omax = sep["others_min"], sep["others_max"]
        if omin is None or not np.isfinite(x_z) or sep["interior"]:
            bound, exc_abs, exc_pct = None, (0.0 if sep["interior"] else None), \
                (0.0 if sep["interior"] else None)
        else:
            bound = omax if x_z > omax else omin
            exc_abs = x_z - bound
            exc_pct = (100.0 * abs(exc_abs) / abs(bound)) if bound != 0 else None
        ov = np.array([vals[s] for s in UNIVERSE], float)
        nv = np.array([float(net_by_asset.get(s, np.nan)) for s in UNIVERSE], float)
        orient = 1.0 if fav != "low" else -1.0
        exz = [i for i, s in enumerate(UNIVERSE) if s != ZEC]
        row = {
            "hypothesis": spec["hypothesis"], "metric": spec["metric"],
            "metric_family": spec["family"], "units": spec["units"],
            "metric_class": spec["cls"],
            "is_outcome_metric": is_out,
            "is_confound_control": bool(spec.get("confound", False)),
            "measured_on_realised_campaigns": spec["metric"] in REALISED_METRICS,
            "direction_favours": fav,
            "direction_pinned_blind": False,
            "denominator_is_outcome": bool(spec.get("denom_outcome", False)),
            "why_this_direction": spec["why"],
        }
        for s in UNIVERSE:
            row[s] = r6(vals[s])
        row.update({
            "others_min": r6(sep["others_min"]), "others_max": r6(sep["others_max"]),
            "others_median": r6(sep["others_median"]),
            "others_mad": r6(sep["others_mad"]),
            "zec_interior": sep["interior"],
            "sep_gap": r6(gap) if gap is not None else None,
            "sep_robust_z": r6(sep["sep_robust_z"]),
            "sep_rel_pct": r4(sep["sep_rel_pct"]),
            "sep_rank": rank,
            "sep_degenerate": degen,
            "boundary_of_the_other_four": r6(bound),
            "exceedance_abs": r6(exc_abs),
            "exceedance_pct_of_boundary": r4(exc_pct),
            "outcome_rank_corr": r4(_spearman(orient * ov, nv)),
            "outcome_rank_corr_ex_zec": r4(_spearman(orient * ov[exz], nv[exz])),
            "outcome_rank_corr_note":
                "Spearman rho across assets between this metric (oriented by "
                "direction_favours) and net R. n = 5 / n = 4: DESCRIPTIVE, no "
                "p-value. The EX-ZEC column is the one worth reading — a "
                "metric that orders the other four by their outcome is "
                "explaining something; one that only puts ZEC on top is "
                "restating ZEC.",
            "materiality_floor_pct": MATERIALITY_FLOOR_PCT,
            "material": material,
            "sign_agrees": sign_ok,
            "card_eligible": eligible,
            "verdict": _verdict(sep, degen, material, sign_ok, is_out, eligible,
                                bool(spec.get("confound", False))),
            "n_zec": n_zec,
            "provisional": bool(n_zec < RC.PROVISIONAL_MIN_N),
            "has_p_value": False,
            "ci_note": "NO CI AND NO P-VALUE. n = 5 assets, one value each, no "
                       "within-asset uncertainty; cluster_ci's unit of "
                       "replication IS the asset and one of the five is the "
                       "hypothesis.",
            "is_selection_surface": True,
            "display_only": True, "gates_nothing": True,
        })
        rows.append(row)
    fp = pd.DataFrame(rows)
    if len(fp) != len(METRIC_REGISTRY):
        raise SystemExit(f"HALT: fingerprint has {len(fp)} rows for "
                         f"{len(METRIC_REGISTRY)} registry metrics — a metric "
                         f"was dropped or duplicated")
    # `metric` ALONE must be a total key: the TIER-C6 driver files this table
    # with `put(fp, "lzec_fingerprint", ["metric"])`, and `assert_key` HALTs on
    # a duplicate.  Asserted here, where the registry is, rather than discovered
    # at write time in another module.
    if fp["metric"].duplicated().any():
        dup = sorted(fp.loc[fp["metric"].duplicated(), "metric"])
        raise SystemExit(f"HALT: METRIC_REGISTRY has duplicate metric names "
                         f"{dup}; `metric` must be unique on its own because "
                         f"tierc6.run keys this table on it alone")
    fp["_absgap"] = fp["sep_gap"].apply(
        lambda g: abs(float(g)) if g is not None and np.isfinite(float(g)) else -1.0)
    fp["_rel"] = fp["sep_rel_pct"].apply(
        lambda g: float(g) if g is not None and np.isfinite(float(g)) else -1.0)
    fp = fp.sort_values(
        by=["card_eligible", "is_outcome_metric", "_absgap", "_rel", "metric"],
        ascending=[False, True, False, False, True],
        kind="mergesort").reset_index(drop=True)
    fp.insert(0, "fp_rank", np.arange(1, len(fp) + 1))
    fp = fp.drop(columns=["_absgap", "_rel"])
    fp["selection_surface_cells"] = len(METRIC_REGISTRY)
    fp["selection_surface_note"] = SELECTION_SURFACE_NOTE
    return fp


def _verdict(sep: dict, degen: str, material: bool, sign_ok: bool,
             is_out: bool, eligible: bool, confound: bool = False) -> str:
    """The row's reading, IN WORDS, so the table cannot be skimmed wrong.

    WHAT WOULD MAKE THIS WRONG: a verdict that says SEPARATOR for a row whose
    separation is real but immaterial — that is precisely the failure the
    materiality floor exists to prevent, and the word for it is not "separator".
    """
    if is_out:
        return "OUTCOME — cannot explain, IS the thing explained"
    if confound:
        return ("CONFOUND CONTROL — read every atr_time row against this one; "
                "it is not a hypothesis metric and can never screen")
    if degen:
        return f"DEGENERATE ({degen}) — separation undefined, not small"
    if sep["interior"]:
        return "INTERIOR — ZEC sits inside the other four; does not separate"
    if not material:
        return (f"EXTERIOR BUT IMMATERIAL — {sep['sep_rel_pct']:.2f}% from the "
                f"pack median, below the {MATERIALITY_FLOOR_PCT:.0f}% floor")
    if not sign_ok:
        return "EXTERIOR, MATERIAL, WRONG DIRECTION — separates AGAINST its own hypothesis"
    return "SEPARATOR — exterior, material, and in the direction the hypothesis needs" \
        if eligible else "EXTERIOR AND MATERIAL — but not card-eligible"


# ═══════════════════════════════════════════════════════ THE SUITABILITY CARD
def suitability_card(fp: pd.DataFrame) -> pd.DataFrame:
    """THE SCREENING THRESHOLDS — [VETO]-tagged, DISPLAY-ONLY UNTIL REGISTERED.

    HOW A TOP SEPARATOR BECOMES A THRESHOLD, with no free parameter: the
    threshold is the OTHER FOUR ASSETS' OWN BOUNDARY.  `direction_favours ==
    "high"` -> `threshold = others_max`, screen `metric > threshold`; `"low"` ->
    `threshold = others_min`, screen `metric < threshold`.  Any offset,
    percentile or midpoint would be a knob fitted on five points — one degree of
    freedom per observation — and would make this a curve fit rather than a
    boundary.

    IF FEWER THAN `SUITABILITY_TOP_K` ROWS ARE ELIGIBLE THE CARD IS SHORT AND
    SAYS SO.  Relaxing the materiality floor to fill it would be exactly the
    move the floor was pinned to prevent, and the temptation to do it is itself
    a finding.  `k_actual` is a column.

    WHAT WOULD MAKE THIS WRONG: a threshold set at ZEC's own value (the screen
    would admit ZEC by construction and nothing else, which is a tautology, not
    a boundary); admitting an immaterial or outcome metric; or omitting the
    disclaimer, which is the only thing standing between this table and a
    promotion nobody paid for.
    """
    el = fp[fp["card_eligible"]].head(SUITABILITY_TOP_K)
    rows = []
    for k, (_, r) in enumerate(el.iterrows(), start=1):
        hi_side = r["direction_favours"] == "high"
        thr = float(r["others_max"] if hi_side else r["others_min"])
        op = ">" if hi_side else "<"
        admitted = [s for s in UNIVERSE
                    if r[s] is not None and np.isfinite(float(r[s]))
                    and ((float(r[s]) > thr) if hi_side else (float(r[s]) < thr))]
        rows.append({
            "rank": k, "hypothesis": r["hypothesis"], "metric": r["metric"],
            "units": r["units"], "direction_favours": r["direction_favours"],
            "threshold": r6(thr),
            "screen_expression": f"{r['metric']} {op} {r6(thr)}",
            "others_min": r["others_min"], "others_max": r["others_max"],
            "zec_value": r[ZEC], "sep_gap": r["sep_gap"],
            "sep_rel_pct": r["sep_rel_pct"],
            "materiality_floor_pct": MATERIALITY_FLOOR_PCT,
            "exceedance_abs": r["exceedance_abs"],
            "exceedance_pct_of_boundary": r["exceedance_pct_of_boundary"],
            "outcome_rank_corr_ex_zec": r["outcome_rank_corr_ex_zec"],
            "measured_on_realised_campaigns": r["measured_on_realised_campaigns"],
            "n_zec": r["n_zec"], "provisional": r["provisional"],
            "assets_admitted": ",".join(admitted),
            "n_assets_admitted": len(admitted),
            "veto_tag": "[VETO]",
            "k_requested": SUITABILITY_TOP_K, "k_actual": len(el),
            "note": (
                f"CLEARS BOTH PINNED GATES. Read it with the two printed "
                f"caveats: ZEC clears the other four's own boundary by "
                f"{r['exceedance_pct_of_boundary']}% of that boundary "
                f"({r['exceedance_abs']} {r['units']}), and this metric's "
                f"rank correlation with net R across the OTHER FOUR assets is "
                f"{r['outcome_rank_corr_ex_zec']} on n = 4, which has no "
                f"p-value and never will. A SECOND materiality floor on "
                f"exceedance was considered and NOT applied: pinning a gate "
                f"after reading this table is the move the first floor exists "
                f"to forbid."),
        })
    if not rows:
        rows.append({
            "rank": 0, "hypothesis": "(none)", "metric": "(none)",
            "units": "", "direction_favours": "none", "threshold": None,
            "screen_expression": "(no screen — no metric survived the gates)",
            "others_min": None, "others_max": None, "zec_value": None,
            "sep_gap": None, "sep_rel_pct": None,
            "materiality_floor_pct": MATERIALITY_FLOOR_PCT,
            "exceedance_abs": None, "exceedance_pct_of_boundary": None,
            "outcome_rank_corr_ex_zec": None,
            "measured_on_realised_campaigns": False,
            "n_zec": 0, "provisional": True,
            "assets_admitted": "", "n_assets_admitted": 0, "veto_tag": "[VETO]",
            "k_requested": SUITABILITY_TOP_K, "k_actual": 0,
            "note": "NO METRIC IS CARD-ELIGIBLE. Of "
                    f"{int((~fp['is_outcome_metric']).sum())} explanatory "
                    "metrics none is simultaneously exterior to the other four, "
                    f"material at the {MATERIALITY_FLOOR_PCT:.0f}% floor, and "
                    "pointing in the direction its own hypothesis needs. The "
                    "card is EMPTY and the floor was NOT relaxed to fill it.",
        })
    card = pd.DataFrame(rows)
    card["in_sample_note"] = _in_sample_note()
    card["disclaimer"] = DISCLAIMER
    card["display_only"] = True
    card["gates_nothing"] = True
    card["is_registration"] = False
    card["in_fdr_family"] = False
    # THIS TABLE IS A SELECTION SURFACE AND SAYS SO ON ITS FACE, IN A COLUMN.
    card["is_selection_surface"] = True
    card["selection_surface_cells"] = len(METRIC_REGISTRY)
    card["selection_surface_note"] = SELECTION_SURFACE_NOTE
    return card


_IN_SAMPLE_NOTE_CACHE: dict[str, str] = {}


def _in_sample_note() -> str:
    """IN-SAMPLE RISK, NAMED — measured live, never transcribed.

    WHAT WOULD MAKE THIS WRONG: hard-coding the numbers.  The sentence's whole
    job is to say how much of the ZEC book is one campaign, and a transcribed
    figure would keep saying it after the book moved.
    """
    if "note" in _IN_SAMPLE_NOTE_CACHE:
        return _IN_SAMPLE_NOTE_CACHE["note"]
    parts = []
    for name in ("v6", "v5-control"):
        z = _of(book(name), ZEC)
        r = np.array([float(t.net_r) for t in z], float)
        j = int(np.argmax(r))
        pos = float(np.sum(np.maximum(r, 0.0)))
        ex26 = [t for t in z if iso(t.entry_ms)[:4] != "2026"]
        order = sorted(((s, float(np.mean(
            [t.net_r for t in _of(book(name), s)
             if iso(t.entry_ms)[:4] != "2026"] or [np.nan]))) for s in UNIVERSE),
            key=lambda kv: -kv[1])
        pos26 = 1 + [s for s, _ in order].index(ZEC)
        parts.append(
            f"[{name}] +{r.sum():.4f} R over {len(z)} campaigns, of which "
            f"+{r[j]:.4f} R — {100.0 * r[j] / r.sum():.2f}% of ZEC's NET R and "
            f"{100.0 * r[j] / pos:.2f}% of its positive mass — is ONE campaign "
            f"entered {iso(z[j].entry_ms)} and exited {iso(z[j].exit_ms)}; strip "
            f"it and ZEC books {r.sum() - r[j]:+.4f} R over {len(z) - 1}. "
            f"Ex-2026 entirely, ZEC's expectancy is "
            f"{np.mean([t.net_r for t in ex26]):+.4f} R over {len(ex26)} "
            f"campaigns — rank {pos26} of 5, behind "
            f"{', '.join(f'{s} ({v:+.4f})' for s, v in order[:pos26 - 1]) or 'nobody'}.")
    note = ("IN-SAMPLE RISK, NAMED. " + "  ".join(parts) +
            "  At the limit this card is fitted on one trade, and every "
            "threshold on it inherits that.")
    _IN_SAMPLE_NOTE_CACHE["note"] = note
    return note


# ═══════════════════════════════════════════════════════════ THE ANSWER
def answer_paragraph(fp: pd.DataFrame, tables: dict[str, pd.DataFrame]) -> str:
    """ONE PARAGRAPH stating the WHY-ZEC answer, whatever it is.

    Quoted VERBATIM by the build document and the ledger, so every number in it
    is read out of the live tables at call time rather than transcribed.  If the
    book moves, the sentence moves with it.

    WHAT WOULD MAKE THIS WRONG: reporting the fingerprint's top row as "the
    reason" without checking whether that row is an outcome metric, an
    immaterial separator, or a separation that exists in ATR-time and vanishes
    in bars — which are the three ways this table can be misread and the three
    the columns were built to expose.
    """
    tables = _norm_tables(tables)
    exp = fp[~fp["is_outcome_metric"]]
    n_exp = len(exp)
    n_out = int(fp["is_outcome_metric"].sum())
    degen = exp[exp["sep_degenerate"] != ""]
    live = exp[exp["sep_degenerate"] == ""]
    interior = live[live["zec_interior"].fillna(False).astype(bool)]
    ext = live[~live["zec_interior"].fillna(False).astype(bool)]
    ext_immat = ext[~ext["material"]]
    ext_mat = ext[ext["material"]]
    ext_wrong = ext_mat[~ext_mat["sign_agrees"]]
    elig = fp[fp["card_eligible"]]

    def _g(metric, col):
        """One cell of the fingerprint by name.  WRONG IF it returned a default
        for an absent metric — a silently missing metric would make the
        paragraph quietly stop mentioning it."""
        s = fp[fp["metric"] == metric]
        return None if s.empty else s.iloc[0][col]

    # the two gates' own worked examples, measured rather than remembered
    z4_rel = _g("ctr_trig_per_100_window_bars", "sep_rel_pct")
    z4_z = _g("ctr_trig_per_100_window_bars", "sep_robust_z")
    arms_total = int(tables["hz4"]["n_armings"].sum())
    hz2 = tables["hz2"].set_index("asset")
    hz5 = tables["hz5"].set_index("asset")
    hz1 = tables["hz1"].set_index("asset")

    # H-Z1's COUNTER-EVIDENCE, MEASURED.  An earlier build set `hz1` up here and
    # then never read it, writing "the SHORTEST median tide streak of the five,
    # 7 bars against ETH's 12, and the MOST regime flips" into the sentence by
    # hand.  Those three numbers happen to be right today and would have gone on
    # being printed after the book moved, which is the failure this docstring
    # promises the paragraph does not have.
    tb_bars = hz1["tide_med_streak_bars"].astype(float)
    tb_flips = hz1["tide_flips_per_1k_bars"].astype(float)
    tb_hi_sym = tb_bars.idxmax()
    n_shorter = int((tb_bars < tb_bars[ZEC]).sum())
    n_flippier = int((tb_flips > tb_flips[ZEC]).sum())
    streak_rank = ("the SHORTEST of the five" if n_shorter == 0
                   else f"{n_shorter} of the other four are shorter still")
    flip_rank = ("the MOST of the five" if n_flippier == 0
                 else f"exceeded by {n_flippier} of the other four")
    streak_txt = (f"its median tide streak is {tb_bars[ZEC]:.0f} bars against "
                  f"{tb_hi_sym}'s {tb_bars[tb_hi_sym]:.0f} — {streak_rank} — "
                  f"and at {tb_flips[ZEC]:.2f} regime flips per 1k bars it is "
                  f"{flip_rank}")

    # H-Z3's OWN ROWS, COUNTED.  The transcribed clause said ZEC was "interior
    # on every version" of the swing-scale metric, and the fingerprint's THIRD
    # row contradicts it: `pct_campaigns_zero_advance` is H-Z3 and ZEC is
    # EXTERIOR on it.  Counted from the table so the sentence cannot disagree
    # with the rows underneath it again.
    z3 = exp[exp["hypothesis"] == "H-Z3"]
    z3_deg = int((z3["sep_degenerate"] != "").sum())
    z3_live = z3[z3["sep_degenerate"] == ""]
    z3_in = z3_live[z3_live["zec_interior"].fillna(False).astype(bool)]
    z3_out = z3_live[~z3_live["zec_interior"].fillna(False).astype(bool)]
    z3_out_txt = ("" if z3_out.empty else " and EXTERIOR on " + ", ".join(
        f"{r.metric} ({str(r.verdict).split(' — ')[0]})"
        for r in z3_out.itertuples()))
    z3_txt = (f"ZEC rank {_g('piv_med_gap_atr_time', 'sep_rank')} of 5 on "
              f"median pivot gap in ATR-time, DEGENERATE on {z3_deg} of its "
              f"{len(z3)} metrics, INTERIOR on {len(z3_in)}{z3_out_txt}")

    # the eligible rows, each with the caveat that its own columns carry
    bits = []
    for r in elig.itertuples():
        comp = {"fan_M_med_atr_time": "fan_M_med_bars",
                "fan_FAST_med_atr_time": "fan_FAST_med_bars",
                "fan_MH_med_atr_time": "fan_MH_med_bars"}.get(r.metric)
        tail = ""
        if comp is not None:
            ci = _g(comp, "zec_interior")
            tail = (f", but in BARS rather than ATR-time ZEC is "
                    f"{'INTERIOR' if ci else 'still exterior'} on the same "
                    f"family ({_g(comp, 'ZECUSDT')} against a pack range "
                    f"{_g(comp, 'others_min')}–{_g(comp, 'others_max')}), so "
                    f"the separation lives in the volatility normalisation and "
                    f"not in the trend")
        if r.units == "R":
            tail += (f", and the absolute difference is {abs(float(r.exceedance_abs)):.6f} R "
                     f"per campaign against a ZEC expectancy of "
                     f"{float(hz5.loc[ZEC, 'expectancy_r']):+.4f} R — "
                     f"statistically clean and economically nil")
        bits.append(f"{r.metric} (ZEC {r.ZECUSDT}, past the other four's own "
                    f"edge by {r.exceedance_pct_of_boundary}% of it, rank "
                    f"correlation with net R across the OTHER four = "
                    f"{r.outcome_rank_corr_ex_zec} on n = 4{tail})")
    elig_txt = "; ".join(bits) if bits else "none"

    # the sharpest single piece of counter-evidence the table contains
    tb_rho = _g("tide_med_streak_bars", "outcome_rank_corr_ex_zec")

    z6 = _of(book("v6"), ZEC)
    r_v6 = np.array([float(t.net_r) for t in z6], float)
    j = int(np.argmax(r_v6))
    best = z6[j]
    share_pos = 100.0 * float(r_v6[j]) / float(np.sum(np.maximum(r_v6, 0.0)))
    share_net = 100.0 * float(r_v6[j]) / float(r_v6.sum())
    panel6 = float(sum(t.net_r for t in book("v6")))
    z5 = _of(book("v5-control"), ZEC)
    r_v5 = np.array([float(t.net_r) for t in z5], float)
    panel5 = float(sum(t.net_r for t in book("v5-control")))
    ex26 = [t for t in z6 if iso(t.entry_ms)[:4] != "2026"]
    exp26 = float(np.mean([t.net_r for t in ex26])) if ex26 else float("nan")
    order26 = sorted(
        ((s, float(np.mean([t.net_r for t in _of(book("v6"), s)
                            if iso(t.entry_ms)[:4] != "2026"] or [np.nan])))
         for s in UNIVERSE), key=lambda kv: -kv[1])
    pos26 = 1 + [s for s, _ in order26].index(ZEC)
    ordn = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth"}[pos26]
    days = (best.exit_ms - best.entry_ms) / 86_400_000.0

    return (
        f"WHY ZEC — on the evidence in this lab, none of the five named "
        f"hypotheses explains it, and the thing that does is one trade. Of the "
        f"{n_exp} EXPLANATORY metrics on the fingerprint ({n_out} further "
        f"metrics are OUTCOME metrics and are excluded from this count by "
        f"construction: net R, expectancy and era concentration are computed "
        f"FROM the result, so they cannot explain ZEC — they ARE ZEC), ZEC sits "
        f"INTERIOR to the other four panel assets on {len(interior)}, is "
        f"DEGENERATE on {len(degen)} (the strict "
        f"({RC.V5.PIVOT_L},{RC.V5.PIVOT_R}) pivot gap is "
        f"{float(_g('piv_med_gap_bars', ZEC)):.1f} bars and {REACH_BARS}/"
        f"{float(_g('piv_med_gap_bars', ZEC)):.0f} = "
        f"{float(_g('pivots_per_reach_bars', ZEC)):.4f} on all five assets — "
        f"selfcheck asserts the EQUALITY across the panel, and these are the "
        f"values it equals — so the separation statistic is "
        f"undefined rather than small; and counter-armings inside an open window "
        f"are exactly 0 across all {arms_total:,} armings because the window is "
        f"DEFINED to end at the first one), and lies outside the pack on only "
        f"{len(ext)} — of which {len(ext_immat)} fail the "
        f"{MATERIALITY_FLOOR_PCT:.0f}% materiality floor, "
        f"{len(ext_wrong)} separates in the direction that should make ZEC "
        f"WORSE ({streak_txt}), leaving "
        f"{len(elig)} that clear every pinned gate: {elig_txt}. Hypothesis by "
        f"hypothesis: H-Z1 trend persistence is not merely unsupported but "
        f"INVERTED — and the sharpest single line in the table is that median "
        f"tide streak in bars orders the OTHER four assets by their net R at "
        f"rho = {tb_rho} on n = 4, and ZEC sits at the wrong end of that "
        f"ordering entirely, which is what an exception looks like rather than "
        f"an explanation; H-Z2 relative toll is a real finding but it is BTC's, "
        f"not ZEC's (BTC pays "
        f"{float(hz2.loc['BTCUSDT', 'toll_pct_of_med_mfe']):.2f}% of its median "
        f"campaign reach in toll against ZEC's "
        f"{float(hz2.loc[ZEC, 'toll_pct_of_med_mfe']):.2f}%, but NEARUSDT is "
        f"cheaper still at {float(hz2.loc['NEARUSDT', 'toll_pct_of_med_mfe']):.2f}% "
        f"and books negative R, and the funding ceiling bound 0 campaigns on all "
        f"five assets); H-Z3 swing-scale match is degenerate in bars and null in "
        f"ATR-time — {z3_txt}; H-Z4 "
        f"whipsaw scarcity is degenerate as worded and, re-worded to "
        f"against-direction 12/26 trigger crosses inside the open window, "
        f"produces this estate's cleanest FALSE separator — a robust z of "
        f"{float(z4_z):.2f} on a difference of {float(z4_rel):.2f}% from the "
        f"pack median, which is exactly why the materiality floor is a printed "
        f"column and not a footnote; and H-Z5 era concentration is overwhelming "
        f"and circular, because a concentration computed from net R is the "
        f"result wearing a different hat. What IS true is arithmetic. ZEC books "
        f"{float(r_v6.sum()):+.4f} R of the v6 panel's {panel6:+.4f} R "
        f"({float(hz5.loc[ZEC, 'share_of_panel_net_r_pct']):.1f}%; on the v5 "
        f"control book it is {float(r_v5.sum()):+.4f} of {panel5:+.4f}, so this "
        f"is a property of the ASSET's history and not of the card revision), "
        f"and {float(r_v6[j]):+.4f} R of that — {share_net:.2f}% of ZEC's net "
        f"and {share_pos:.2f}% of its entire positive mass — is a SINGLE "
        f"campaign entered {iso(best.entry_ms)} and exited {iso(best.exit_ms)}, "
        f"{best.bars_held} bars and {len(best.advances)} ratchet advances on a "
        f"move of {(best.exit_px / best.entry_px):.2f}x in {days:.0f} days; "
        f"strip that one trade and ZEC books {float(r_v6.sum() - r_v6[j]):+.4f} "
        f"R, and strip 2026 entirely and ZEC's expectancy is {exp26:+.4f} R over "
        f"{len(ex26)} campaigns — {ordn} of five, behind "
        f"{', '.join(f'{s} ({v:+.4f})' for s, v in order26[:pos26 - 1]) or 'nobody'}"
        f". So the question 'why ZEC' "
        f"presupposes a DISTRIBUTION of ZEC campaigns that beats the panel, and "
        f"there is no such distribution: there are {len(z6) - 1} ordinary ZEC "
        f"campaigns and one extraordinary one that the trail held through. The "
        f"suitability card below is therefore short by design, DISPLAY-ONLY, and "
        f"fitted in-sample on five assets with one positive case; it gates "
        f"nothing, and the correct next question is not 'what makes ZEC "
        f"suitable' but 'how often does this card catch a move like that on ANY "
        f"asset, and did it catch this one because ZEC is special or because the "
        f"MOVE was' — which is answerable, and is not one of the five "
        f"hypotheses.")

# ══════════════════════════════════════════ F-C6-ZEC · CROSS-CHECK BY ANOTHER PATH
def crosscheck(book_name: str = "v6") -> pd.DataFrame:
    """FIVE LEGS, ONE PER HYPOTHESIS, EACH BY AN INDEPENDENT PATH.

    THE HOUSE RULE THIS OBEYS: never re-derive a value the way the program
    derived it and compare it to itself.  Every leg below reaches the quantity
    through DIFFERENT code — `analytics`' SMA-seeded NaN-before-warm-up EMA
    instead of the engine's Pine-parity one, a naive O(n·L) pivot scan instead
    of `engine.s1._pivots`, hand-walked windows instead of `RC.armings`, raw
    funding stamps instead of `_account.fund_leg` — and the only shared input is
    `load_klines`.

    AND THE LEGS ARE CARDINALITY CHECKS WHERE THEY CAN BE.  A leg satisfied by
    one example is not a leg: LEG 3 and LEG 4 assert across ALL FIVE assets,
    because this estate has already watched a book lose 64% of its rows with
    every single-example fixture staying green.

    WHAT WOULD MAKE THIS WHOLE FUNCTION WRONG: a leg that reaches its quantity
    through the same helper the table used.  That is not a cross-check, it is
    the program agreeing with itself, and this estate lost 6 of 16 TC5 repairs
    to exactly that.  Each leg names its independent path in its own `detail`
    string, and the tolerances are stated rather than tuned: exact equality is
    the WRONG bar wherever an indicator recipe differs between the two paths,
    and the RIGHT bar wherever it does not (LEG 5 is exact at 1e-05).
    """
    from analytics import momentum as AM, volatility as AV
    import tierc2_baseline as TB
    rows: list[dict] = []
    bk = book(book_name)
    lo_ms, hi_ms, _ = T6.corridor()

    def leg(name, metric, hand, prog, tol_pct, extra="", ok_override=None):
        """Record one leg.  WRONG IF a leg with a non-comparable program value
        (zero or non-finite) were scored PASS by default — it answers None for
        the difference and only an explicit `ok_override` can pass it."""
        d = (abs(hand - prog) / abs(prog) * 100.0) if (prog not in (0, None)
                                                       and np.isfinite(prog)
                                                       and np.isfinite(hand)) else None
        ok = (ok_override if ok_override is not None
              else bool(d is not None and d <= tol_pct))
        rows.append({"leg": name, "metric": metric, "hand_path_value": r6(hand),
                     "program_value": r6(prog), "abs_rel_diff_pct": r4(d),
                     "tolerance_pct": tol_pct, "passed": ok, "detail": extra})

    # ── LEG 1 · H-Z1 tide_med_streak_atr_time, ZEC, analytics EMAs + a loop ──
    k = TB.load_klines(ZEC, "4h")
    ot = k["open_time"].to_numpy(np.int64)
    hi_a, lo_a, cl = (k["high"].to_numpy(float), k["low"].to_numpy(float),
                      k["close"].to_numpy(float))
    e89 = AM.ema(cl, 89)
    e316 = AM.ema(cl, 316)
    at = AV.atr(hi_a, lo_a, cl, 14)
    a0 = int(np.searchsorted(ot, lo_ms, "left"))
    b0 = int(np.searchsorted(ot, hi_ms, "right")) - 1
    a0 = max(a0, RC.WARMUP_BARS)
    segs, cur, acc, sign = [], 0, 0.0, 0
    for i in range(a0, b0 + 1):
        s = 0
        if np.isfinite(e89[i]) and np.isfinite(e316[i]):
            if e89[i] > e316[i] and cl[i] > e316[i]:
                s = 1
            elif e89[i] < e316[i] and cl[i] < e316[i]:
                s = -1
        if s != 0 and s == sign:
            cur += 1
            acc += (at[i] / cl[i]) if (np.isfinite(at[i]) and cl[i]) else 0.0
        else:
            if sign != 0 and cur > 0:
                segs.append(acc)
            sign, cur = s, (1 if s != 0 else 0)
            acc = ((at[i] / cl[i]) if (s != 0 and np.isfinite(at[i]) and cl[i])
                   else 0.0)
    if sign != 0 and cur > 0:
        segs.append(acc)
    prog1 = float(hz1_table(lo_ms, hi_ms).set_index("asset")
                  .loc[ZEC, "tide_med_streak_atr_time"])
    leg("LEG 1 · H-Z1", "tide_med_streak_atr_time(ZECUSDT)",
        float(np.median(segs)), prog1, LEG_TOL_INDICATOR_PCT,
        f"analytics SMA-seeded EMA + pure-python loop; n_segments hand="
        f"{len(segs)}. FAILS IF the two medians differ by more than "
        f"{LEG_TOL_INDICATOR_PCT}% — exact equality is the WRONG bar because "
        f"analytics.ema warms differently from engine.indicators.ema.")

    # ── LEG 2 · H-Z2 toll_atr, ZEC, census2b's own toll constant ─────────────
    zt = _of(bk, ZEC)
    ent = np.array([t.entry_ms for t in zt], np.int64)
    pos = np.searchsorted(ot, ent)
    tolls = (C2B.TOLL_BPS_ROUND_TRIP / 10_000.0) * cl[pos] / at[pos]
    hand2 = float(np.median(tolls[np.isfinite(tolls)]))
    corr_tolls = (C2B.TOLL_BPS_ROUND_TRIP / 10_000.0) * cl[a0:b0 + 1] / at[a0:b0 + 1]
    corr_med = float(np.nanmedian(corr_tolls))
    prog2 = float(hz2_table(book_name, lo_ms, hi_ms).set_index("asset")
                  .loc[ZEC, "toll_atr"])
    const_ok = (float(RC.FEE_BPS_SIDE) * 2.0 == 10.0
                and float(C2B.TOLL_BPS_ROUND_TRIP) == 10.0)
    m8_ok = hand2 > corr_med
    h2 = hz2_table(book_name, lo_ms, hi_ms).set_index("asset")
    m8_panel = {s: r6(float(h2.loc[s, "toll_event_minus_corridor_atr"]))
                for s in UNIVERSE}
    m8_exceptions = [s for s, v in m8_panel.items() if v is not None and v <= 0]
    leg("LEG 2 · H-Z2", "toll_atr(ZECUSDT)", hand2, prog2, LEG_TOL_ATR_PCT,
        f"census2b_program.TOLL_BPS_ROUND_TRIP={C2B.TOLL_BPS_ROUND_TRIP} and "
        f"2xRC.FEE_BPS_SIDE={2 * RC.FEE_BPS_SIDE} both 10.0: {const_ok}. "
        f"m8 (entry population > whole corridor) on ZEC: {m8_ok} "
        f"({hand2:.6f} vs {corr_med:.6f}). DISCLOSED, NOT SWEPT UNDER: m8's "
        f"direction holds on 4 of 5 assets but NOT on {m8_exceptions} — "
        f"per-asset event-minus-corridor toll {m8_panel}. The leg's bar is ZEC, "
        f"which is the asset it is about, and the exception is printed rather "
        f"than allowed to fail silently. NOTE ALSO that the recon spec's own "
        f"§6 prior quotes the WHOLE-CORRIDOR toll figures (BTC 0.0640 … ZEC "
        f"0.0322) while its §1 H-Z2(b) specifies the ENTRY population; this "
        f"table uses the entry population, which is what m8 requires, and "
        f"prints both. FAILS IF the constants are not both 10.0, m8's "
        f"direction fails on ZEC, or the figures differ by more than "
        f"{LEG_TOL_ATR_PCT}%.",
        ok_override=bool(const_ok and m8_ok
                         and abs(hand2 - prog2) / abs(prog2) * 100.0
                         <= LEG_TOL_ATR_PCT))

    # ── LEG 3 · H-Z3 pivots, naive O(n·L) scan, ALL FIVE ASSETS ──────────────
    # THE HAND MEDIAN IS TAKEN FROM THE HAND-SCANNED SET, AND THAT IS THE WHOLE
    # POINT OF THE LEG.  An earlier build computed it from `T6.frame(sym)["pv4"]`
    # — the very object `hz3_table` reads — with the same `np.diff`/median and
    # the same `_corr` bounds, and compared that to `hz3_table`.  That is the
    # program agreeing with itself: it could not have failed for any defect in
    # the pivot path, which is exactly the failure this leg exists to catch.
    # The corridor bounds here are likewise a bare searchsorted over the raw
    # kline open times, never `_corr` / `T6._idx_range`.
    L, R = int(RC.V5.PIVOT_L), int(RC.V5.PIVOT_R)
    set_ok, med_vals, counts = True, [], {}
    h3 = hz3_table(book_name, lo_ms, hi_ms).set_index("asset")
    for sym in UNIVERSE:
        kk = TB.load_klines(sym, "4h")
        H, Lo = kk["high"].to_numpy(float), kk["low"].to_numpy(float)
        o3 = kk["open_time"].to_numpy(np.int64)
        n = len(H)
        piv = []
        for i in range(L, n - R):
            if Lo[i] < Lo[i - L:i].min() and Lo[i] < Lo[i + 1:i + R + 1].min():
                piv.append(i)
            elif H[i] > H[i - L:i].max() and H[i] > H[i + 1:i + R + 1].max():
                piv.append(i)
        pv = T6.frame(sym)["pv4"]
        prog_set = set(int(v) for v in np.concatenate(
            [np.asarray(pv.low_bar, np.int64), np.asarray(pv.high_bar, np.int64)]))
        hand_set = set(piv)
        # a bar can be BOTH a high and a low pivot; the naive scan takes the low
        # branch first, so compare against the union restricted to the same
        # scannable span.  EQUALITY, NOT CONTAINMENT: a subset test stays green
        # if the engine's pivot set doubles, and equality is the bar this estate
        # can actually meet — the two sets agree bar for bar on all five.
        span = set(range(L, n - R))
        set_ok &= (hand_set == (prog_set & span))
        a1 = max(int(np.searchsorted(o3, lo_ms, "left")), int(RC.WARMUP_BARS))
        b1 = int(np.searchsorted(o3, hi_ms, "right")) - 1
        hb = np.array(sorted(x for x in hand_set if a1 <= x <= b1))
        counts[sym] = int(hb.size)
        med_vals.append(float(np.median(np.diff(hb))) if hb.size > 1
                        else float("nan"))
    all_same = len(set(med_vals)) == 1
    hand3 = med_vals[UNIVERSE.index(ZEC)]      # BY NAME — not med_vals[-1]
    prog3 = float(h3.loc[ZEC, "piv_med_gap_bars"])
    prog_same = len(set(h3["piv_med_gap_bars"].astype(float))) == 1
    leg("LEG 3 · H-Z3", "piv_med_gap_bars(ALL FIVE)", hand3, prog3, 0.0,
        f"naive O(n·L) triple-loop scan over the RAW klines — never "
        f"engine.s1._pivots, never T6.frame()['pv4'], never _corr. The hand "
        f"median is taken from the HAND set and the corridor bounds from a "
        f"bare searchsorted, so no part of this leg reaches the quantity by "
        f"the table's own route. Hand median gap per asset "
        f"{dict(zip(UNIVERSE, med_vals))} over hand pivot counts {counts}; "
        f"identical on all five, HAND path: {all_same}; identical on all five, "
        f"PROGRAM path: {prog_same}; hand pivot set EQUALS the program's "
        f"(restricted to the scannable span) on all five: {set_ok}. FAILS IF "
        f"the medians are not exactly equal across all five assets (the "
        f"degeneracy IS the H-Z3 finding), the two paths disagree on ZEC, or "
        f"any asset's two pivot sets differ by a single bar.",
        ok_override=bool(all_same and prog_same and set_ok and hand3 == prog3))

    # ── LEG 4 · H-Z4 hand-walked windows, ALL FIVE ASSETS ────────────────────
    zeros_ok, ratios = True, {}
    for sym in UNIVERSE:
        kk = TB.load_klines(sym, "4h")
        c2 = kk["close"].to_numpy(float)
        o2 = kk["open_time"].to_numpy(np.int64)
        E12, E26, E89 = AM.ema(c2, 12), AM.ema(c2, 26), AM.ema(c2, 89)

        def xover(a, b):
            """`a` crosses above `b` — a direct sign-change test, deliberately
            NOT engine.indicators.crossover.  WRONG IF it fired on a bar where
            either series is NaN: an unwarm EMA is not a level and cannot
            cross."""
            out = np.zeros(len(a), bool)
            out[1:] = (a[1:] > b[1:]) & (a[:-1] <= b[:-1])
            return out & np.isfinite(a) & np.isfinite(b)

        wu, wd = xover(E12, E89), xover(E89, E12)
        tu, td = xover(E12, E26), xover(E26, E12)
        aa = max(int(np.searchsorted(o2, lo_ms, "left")), RC.WARMUP_BARS)
        bb = int(np.searchsorted(o2, hi_ms, "right")) - 1
        tot_ctr = tot_bars = 0
        for dirn, opens, counter, anti in ((1, wu, wd, td), (-1, wd, wu, tu)):
            for i in np.flatnonzero(opens):
                i = int(i)
                if not (aa <= i <= bb):
                    continue
                later = np.flatnonzero(counter[i + 1:])
                end = min(int(i + 1 + later[0]) if later.size else len(c2), bb + 1)
                if end <= i:
                    end = i + 1
                tot_ctr += int(anti[i:end].sum())
                tot_bars += end - i
                if int(counter[i + 1:end].sum()) != 0:
                    zeros_ok = False
        ratios[sym] = 100.0 * tot_ctr / tot_bars if tot_bars else float("nan")
    h4 = hz4_table(lo_ms, hi_ms).set_index("asset")
    prog4 = float(h4.loc[ZEC, "ctr_trig_per_100_window_bars"])
    prog_zero_total = int(h4["ctr_arm_12_89_total"].sum())
    d4 = abs(ratios[ZEC] - prog4) / abs(prog4) * 100.0
    leg("LEG 4 · H-Z4", "ctr_trig_per_100_window_bars(ZECUSDT)", ratios[ZEC],
        prog4, LEG_TOL_INDICATOR_PCT,
        f"hand-walked 12/89 windows from analytics EMAs with a sign-change "
        f"cross test, never RC.armings / RC._crosses. Counter 12/89 crosses "
        f"strictly inside an open window, re-derived independently on ALL FIVE "
        f"assets: {zeros_ok} (program total {prog_zero_total}). Per-asset "
        f"ratios {({k2: round(v, 4) for k2, v in ratios.items()})}. FAILS IF "
        f"the zero is not independently confirmed on every asset or the ratio "
        f"differs by more than {LEG_TOL_INDICATOR_PCT}%.",
        ok_override=bool(zeros_ok and prog_zero_total == 0
                         and d4 <= LEG_TOL_INDICATOR_PCT))

    # ── LEG 5 · H-Z5 best ZEC campaign net R, from raw bars + raw funding ────
    zr = np.array([float(t.net_r) for t in zt], float)
    j = int(np.argmax(zr))
    t = zt[j]
    fp_ = TB.FUNDING / f"{ZEC}.parquet"
    fd = pd.read_parquet(fp_)
    fms = fd["funding_time"].to_numpy(np.int64)
    frt = fd["funding_rate"].to_numpy(float)
    bar_of = np.searchsorted(ot, fms, "right") - 1
    d = t.direction
    gross = (t.exit_px - t.entry_px) * d / t.r_dist
    fee = (RC.FEE_BPS_SIDE / 10_000.0) * (t.entry_px + t.exit_px) / t.r_dist
    fund = 0.0
    for jj, rate in zip(bar_of, frt):
        if t.entry_i < jj <= t.exit_i and rate:
            fund += rate * float(cl[jj - 1]) * d
    hand5 = gross - fee - fund / t.r_dist
    clean = (not t.harvested) and (not t.adds) and (not t.funding_ceiling_bound)
    pos5 = float(np.sum(np.maximum(zr, 0.0)))
    share_pos = 100.0 * float(zr[j]) / pos5
    share_net = 100.0 * float(zr[j]) / float(zr.sum())
    leg("LEG 5 · H-Z5", "best_campaign_net_r(ZECUSDT)", hand5, float(t.net_r),
        0.0,
        f"raw 4h bars + raw funding parquet, never _account/fund_leg/_ride. "
        f"abs diff {abs(hand5 - float(t.net_r)):.3e} (bar {LEG_TOL_EXACT:g} — "
        f"this leg IS exact: same prices, same arithmetic, no indicator in the "
        f"path). Campaign is unharvested/no-adds/uncapped: {clean} — if it were "
        f"harvested the two-half accounting at tierc5.py:366-381 would be in "
        f"the path and this arithmetic would be the wrong arithmetic. FAILS IF "
        f"the hand figure differs by more than {LEG_TOL_EXACT:g} R or the "
        f"campaign is not clean. The DOMINANCE bar is a separate leg (5b) "
        f"because it tests the card's premise, not this module's arithmetic.",
        ok_override=bool(abs(hand5 - float(t.net_r)) <= LEG_TOL_EXACT and clean))

    # ── LEG 5b · THE PREMISE — and a bar the recon spec attached to the wrong
    #    quantity.  The spec pins "share >= 80%" but DEFINES share on POSITIVE
    #    MASS, while the 88.86% figure it quotes is share of NET R.  The two are
    #    different numbers (on this book, 49.79% and 76.95%), so the bar is
    #    applied to the quantity it was written against — share of NET R — and
    #    measured on the v5 control book, which is the book the spec measured.
    #    The v6 figure is printed beside it: the armed trail lifts ZEC's OTHER
    #    campaigns and DILUTES the best one's dominance, which is a finding
    #    about the card revision and not a broken fixture.
    z5 = _of(book("v5-control"), ZEC)
    r5 = np.array([float(x.net_r) for x in z5], float)
    j5 = int(np.argmax(r5))
    share_net_v5 = 100.0 * float(r5[j5]) / float(r5.sum())
    share_pos_v5 = 100.0 * float(r5[j5]) / float(np.sum(np.maximum(r5, 0.0)))
    rows.append({
        "leg": "LEG 5b · H-Z5 premise", "metric": "best_campaign dominance",
        "hand_path_value": r6(share_net_v5), "program_value": 80.0,
        "abs_rel_diff_pct": None, "tolerance_pct": None,
        "passed": bool(share_net_v5 >= 80.0),
        "detail": (
            f"THE PREMISE: one ZEC campaign dominates the ZEC book. On the "
            f"v5-control book (the book the recon spec measured) the best "
            f"campaign is {share_net_v5:.2f}% of ZEC's NET R and "
            f"{share_pos_v5:.2f}% of its positive mass; the spec's bar of 80% "
            f"is met by the first and not the second, and the spec quotes "
            f"88.86% — the share-of-net figure — while DEFINING share on "
            f"positive mass. The bar is therefore applied to share of NET R and "
            f"that is said out loud rather than adjusted quietly. ON THE v6 "
            f"BOOK the same campaign is {share_net:.2f}% of net and "
            f"{share_pos:.2f}% of positive mass: the armed trail improved ZEC's "
            f"OTHER {len(z5) - 1} campaigns "
            f"({float(r5.sum() - r5[j5]):+.4f} R -> "
            f"{float(zr.sum() - zr[j]):+.4f} R ex-best) and diluted the "
            f"dominance. FAILS IF the v5 share of net falls below 80%, which "
            f"would mean the filed book moved and the card's premise changed."),
    })

    df = pd.DataFrame(rows)
    df["book"] = book_name
    df["display_only"] = True
    return df


# ═══════════════════════════════════════════ CARDINALITY ASSERTIONS, PRINTED
def selfcheck(tables: dict[str, pd.DataFrame], fp: pd.DataFrame,
              card: pd.DataFrame) -> pd.DataFrame:
    """CARDINALITY CHECKS — because a check satisfied by one example is not a
    check.

    This estate has already lost a book that shed 64% of its rows while every
    fixture stayed green.  Each row below asserts a COUNT, not a value, so a
    silent filter has nowhere to hide.

    WHAT WOULD MAKE THIS WRONG: asserting `>= 1` anywhere.  Every bar here is an
    equality against a number derived from the panel or the registry, not from
    the table being checked.
    """
    rows = []

    def chk(name, got, want, why):
        """Record one cardinality assertion.  WRONG IF `passed` were computed
        from the stringified values — `"5" == "5"` would also be True for two
        different objects that both render as 5."""
        # STRINGIFIED ON PURPOSE: the checks compare ints, bools and lists, and
        # a parquet column cannot hold all three.  The comparison happens on the
        # live objects; only the record of it is text.
        rows.append({"check": name, "got": str(got), "want": str(want),
                     "passed": bool(got == want), "why_this_bar": why})

    nU = len(UNIVERSE)
    for k in ("hz1", "hz2", "hz3", "hz4", "hz5"):
        chk(f"{k}_rows_is_one_per_asset", len(tables[k]), nU,
            "every hypothesis table is one row per panel asset, reported whole")
        chk(f"{k}_assets_complete", sorted(tables[k]["asset"]), sorted(UNIVERSE),
            "no asset silently dropped")
    chk("hz1_scope_rows", len(tables["hz1_scope"]),
        nU * (1 + len(FAN_FAMILIES_REPORTED)),
        "5 assets x (tide + 6 ribbon families) — VH/UH included with n=0")
    nsl = len(T6.slices_of(*T6.corridor()[:2]))
    chk("hz5_slice_rows", len(tables["hz5_slice"]), nU * nsl,
        "every asset x every slice, including the n=0 ones")
    chk("fingerprint_rows", len(fp), len(METRIC_REGISTRY),
        "one row per registry metric — reported WHOLE")
    chk("fingerprint_key_unique", int(fp.duplicated(["hypothesis", "metric"]).sum()),
        0, "the declared key must be unique before anything joins on it")
    chk("fingerprint_all_display_only", int(fp["display_only"].sum()), len(fp),
        "no row of a selection surface may be anything but display-only")
    chk("outcome_metrics_never_eligible",
        int((fp["is_outcome_metric"] & fp["card_eligible"]).sum()), 0,
        "an outcome metric cannot explain the outcome, so it can never screen")
    chk("immaterial_never_eligible",
        int(((~fp["material"]) & fp["card_eligible"]).sum()), 0,
        f"the {MATERIALITY_FLOOR_PCT:.0f}% floor is [VETO] and binds absolutely")
    chk("outcome_metrics_sort_below_explanatory",
        int((fp["is_outcome_metric"].astype(int).diff().dropna() < 0).sum()), 0,
        "the ranking must never put an outcome metric above an explanatory one "
        "of equal eligibility")
    # THE EXACT ROW COUNT, NOT AN UPPER BOUND.  `len(card) <= K` was the earlier
    # bar and it is satisfied by a card that silently dropped an eligible row —
    # a 1-row card passes `<= 3` just as happily as the 2-row card that is
    # correct.  The count is derived from the FINGERPRINT, not from the card.
    n_elig = int(fp["card_eligible"].sum())
    chk("card_rows_exactly_min_k_and_eligible", len(card),
        max(1, min(SUITABILITY_TOP_K, n_elig)),
        "the card holds exactly min(K, eligible) rows — or the single '(none)' "
        "row when nothing is eligible; an inequality here would pass a card "
        "that quietly lost a screen")
    chk("card_k_actual_matches", int(card["k_actual"].iloc[0]), n_elig,
        "k_actual is the count of eligible rows, not a target that was filled")
    # THE BOOK THE TABLES WERE ACTUALLY BUILT ON, read off the table rather than
    # pinned to "v6".  `run(book_name=...)` and `all_tables(book_name=...)` are
    # real parameters, and v5-control books the SAME 195 campaigns as v6 (the
    # two share the entry rule and differ only in exit management) — so a
    # hardcoded "v6" here was green by coincidence, not by agreement, and would
    # have stayed green against a book it was not checking.
    tb_book = str(tables["hz5"]["book"].iloc[0])
    bk = book(tb_book)
    chk("hz5_campaign_total_matches_book",
        int(tables["hz5"]["n_campaigns"].sum()), len(bk),
        f"the per-asset campaign counts must partition the {tb_book} book "
        f"exactly — the book the tables name, not a pinned one")
    chk("hz2_campaign_total_matches_book",
        int(tables["hz2"]["n_campaigns"].sum()), len(bk),
        "same partition, reached by a different table")
    chk("corridor_bars_match_raw_klines",
        int(tables["hz1"]["corridor_bars"].sum()), _corridor_bars_from_raw(),
        "the corridor bar count is re-derived by COUNTING A BOOLEAN MASK over "
        "the raw kline open times — no searchsorted, no index subtraction, "
        "which is what the table's own path uses. A warm-up floor applied on "
        "one path and not the other, a wrong searchsorted side, or a "
        "duplicated timestamp all show up here as a count mismatch")
    chk("fan_UH_empty_on_all_five", int(tables["hz1"]["fan_UH_n"].sum()), 0,
        "UH_orient is OR_NA on 100% of 4h bars on EVERY asset; one asset "
        "proving it is not a check")
    chk("funding_ceiling_never_bound_on_all_five",
        int(tables["hz2"]["funding_ceiling_bound_n"].sum()), 0,
        "FUNDING_CEILING_R = 1.0 binds on no campaign of any asset; asserted "
        "across the whole panel, not sampled")
    chk("counter_armings_in_window_zero_on_all_five",
        int(tables["hz4"]["ctr_arm_12_89_total"].sum()), 0,
        "H-Z4 as originally worded is 0 by construction on EVERY asset — the "
        "reason the metric was re-worded, asserted panel-wide")
    chk("pivot_gap_degenerate_on_all_five",
        len(set(tables["hz3"]["piv_med_gap_bars"].astype(float))), 1,
        "the strict (5,5) median gap is the SAME number on all five assets; a "
        "check that looked at one asset would call it a fact about that asset")
    df = pd.DataFrame(rows)
    df["display_only"] = True
    return df


def _corridor_bars_from_raw() -> int:
    """Corridor bar count re-derived by COUNTING A BOOLEAN MASK.

    A DIFFERENT ARITHMETIC ON PURPOSE, and the earlier version did not have
    one.  `Frame4h.open_ms` is byte-identical to the raw kline `open_time` on
    all five assets, so counting the corridor with `searchsorted(lo,'left')` /
    `searchsorted(hi,'right') - 1` and `b - a + 1` here — which is precisely
    what `_corr` -> `T6._idx_range` does — was the same two searchsorteds over
    the same array subtracted the same way, and could not have disagreed for
    any reason whatever.  This counts instead: a mask over `open_time` with the
    warm-up floor expressed as a position predicate, no searchsorted and no
    index subtraction anywhere in it.

    THAT MAKES THE CHECK ABLE TO FAIL: a wrong searchsorted side, an off-by-one
    on either corridor edge, a duplicated timestamp, or an out-of-order
    timestamp all move the index arithmetic and NOT the mask count.

    WHAT WOULD MAKE THIS WRONG: calling `_corr`, `T6._idx_range` or
    `searchsorted` here.  The whole value of this number is that it does not.
    """
    import tierc2_baseline as TB
    lo, hi, _ = T6.corridor()
    n = 0
    for sym in UNIVERSE:
        ot = TB.load_klines(sym, "4h")["open_time"].to_numpy(np.int64)
        keep = ((ot >= lo) & (ot <= hi)
                & (np.arange(len(ot)) >= int(RC.WARMUP_BARS)))
        n += int(keep.sum())
    return n


# ═════════════════════════════════════════════════════════════════ THE RUN
def run(root: Path | None = None, book_name: str = "v6") -> dict:
    """Build every table, cross-check it, and file it.  Returns a manifest dict.

    WHAT WOULD MAKE THIS WRONG: writing the fingerprint without asserting its
    cardinality first (a dropped metric would file silently), or writing the
    suitability card without the disclaimer column, which is the only thing
    between this table and an unpaid promotion.
    """
    root = Path(root) if root is not None else T6.OUT
    tb = all_tables(book_name)
    fp = fingerprint(tb)
    card = suitability_card(fp)
    cc = crosscheck(book_name)
    sc = selfcheck(tb, fp, card)
    ans = answer_paragraph(fp, tb)
    shas = {}
    for name, df, keys in (
            ("lzec_hz1", tb["hz1"], ["asset"]),
            ("lzec_hz1_scope", tb["hz1_scope"], ["asset", "scope"]),
            ("lzec_hz2", tb["hz2"], ["asset"]),
            ("lzec_hz3", tb["hz3"], ["asset"]),
            ("lzec_hz4", tb["hz4"], ["asset"]),
            ("lzec_hz5", tb["hz5"], ["asset"]),
            ("lzec_hz5_slice", tb["hz5_slice"],
             ["asset", "slice_group", "slice_key"]),
            ("lzec_fingerprint", fp, ["hypothesis", "metric"]),
            ("lzec_suitability_card", card, ["rank"]),
            ("lzec_crosscheck", cc, ["leg"]),
            ("lzec_selfcheck", sc, ["check"])):
        shas[name] = write_table(df, name, keys, root)
    log("")
    log("  L-ZEC ANSWER (quoted verbatim by the build document):")
    log(f"  {ans}")
    log("")
    log(f"  {DISCLAIMER}")
    return {"shas": shas, "answer_paragraph": ans, "disclaimer": DISCLAIMER,
            "in_sample_note": _in_sample_note(),
            "selection_surface": {"L-ZEC fingerprint metrics": len(METRIC_REGISTRY)},
            "crosscheck_all_passed": bool(cc["passed"].all()),
            "selfcheck_all_passed": bool(sc["passed"].all()),
            "book": book_name}


if __name__ == "__main__":                                  # pragma: no cover
    import json
    m = run()
    print(json.dumps({k: v for k, v in m.items() if k != "shas"}, indent=2)[:4000])
