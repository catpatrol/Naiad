"""F-B25 -- the volume layer: VA nesting and LVN detection (Amendment 2 §3-§4).

Run: python -m pytest tests/test_brief2_volume.py

F-B25 is the fixture the amendment names: on synthetic profiles with KNOWN
geometry, `state`, `overlap_frac`, consensus and gap bands are computed
correctly for all five states.  Synthetic and not sampled from the estate on
purpose -- the point is to pin the arithmetic against geometry whose answer is
known by construction, so a regression is unambiguous rather than a judgement
call about real data.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import analytics                                                    # noqa: E402
from analytics import nesting as N                                  # noqa: E402
from analytics import profile as P                                  # noqa: E402


# --------------------------------------------------------------- F-B25

def test_f_b25_all_five_states_by_construction():
    """Every state in §4.1, on geometry whose answer is known by construction."""
    cases = [
        # (short VAL, short VAH, long VAL, long VAH, expected state)
        (100.0, 110.0, 90.0, 120.0, "nested_inside"),
        (90.0, 120.0, 100.0, 110.0, "nested_outside"),
        (100.0, 120.0, 110.0, 130.0, "overlapping"),
        (140.0, 150.0, 100.0, 120.0, "disjoint_above"),
        (80.0, 90.0, 100.0, 120.0, "disjoint_below"),
    ]
    seen = set()
    for a_lo, a_hi, b_lo, b_hi, want in cases:
        n = N.va_nesting(a_lo, a_hi, b_lo, b_hi)
        assert n["state"] == want, f"{(a_lo, a_hi, b_lo, b_hi)} -> {n['state']}, want {want}"
        seen.add(want)
    assert seen == set(N.STATES), f"not all five states exercised: {seen}"


def test_f_b25_overlap_frac_is_a_fraction_of_the_SHORTER_va():
    """overlap_frac answers 'how much of short-term value has long-term backing'."""
    # short 100-110 entirely inside long 90-120: total backing
    assert N.va_nesting(100, 110, 90, 120)["overlap_frac"] == 1.0
    # short 100-120 vs long 110-130: intersection 110-120 = 10 of the short 20
    assert N.va_nesting(100, 120, 110, 130)["overlap_frac"] == pytest.approx(0.5)
    # short 90-120 CONTAINS long 100-110: intersection is the long VA, 10 of 30
    assert N.va_nesting(90, 120, 100, 110)["overlap_frac"] == pytest.approx(1 / 3)
    # disjoint: zero, not nan
    assert N.va_nesting(140, 150, 100, 120)["overlap_frac"] == 0.0
    # a zero-width short VA touching the long VA is TOTAL agreement, not 0/0
    assert N.va_nesting(105, 105, 100, 110)["overlap_frac"] == 1.0


def test_f_b25_consensus_and_gap_bands():
    """consensus = [max(VAL), min(VAH)]; gap = the unclaimed space between."""
    assert N.va_nesting(100, 120, 110, 130)["consensus_band"] == [110.0, 120.0]
    assert N.va_nesting(100, 110, 90, 120)["consensus_band"] == [100.0, 110.0]

    above = N.va_nesting(140, 150, 100, 120)
    assert above["gap_band"] == [120.0, 140.0] and above["consensus_band"] is None
    below = N.va_nesting(80, 90, 100, 120)
    assert below["gap_band"] == [90.0, 100.0] and below["consensus_band"] is None

    # intersecting pairs have no gap
    assert N.va_nesting(100, 120, 110, 130)["gap_band"] is None


def test_f_b25_facing_edges_are_the_edges_price_meets_first():
    """§4.2 names BOTH facing edges; they must be the inner pair, not the outer."""
    above = N.va_nesting(140, 150, 100, 120)
    assert above["facing_edges"]["short"] == {"edge": "VAL", "level": 140.0}
    assert above["facing_edges"]["long"] == {"edge": "VAH", "level": 120.0}

    below = N.va_nesting(80, 90, 100, 120)
    assert below["facing_edges"]["short"] == {"edge": "VAH", "level": 90.0}
    assert below["facing_edges"]["long"] == {"edge": "VAL", "level": 100.0}


def test_f_b25_prose_names_the_gap_and_both_edges():
    """§4.2: a table alone does not satisfy §4 -- the sentence is a deliverable."""
    text = N.describe_nesting(("7d", "30d"), N.va_nesting(64250, 66000, 61000, 63100))
    assert "entirely above" in text
    assert "63,100.00-64,250.00" in text, f"gap not named in prose: {text}"
    assert "7d VAL at 64,250.00" in text and "30d VAH at 63,100.00" in text, text

    nested = N.describe_nesting(("7d", "30d"), N.va_nesting(100, 110, 90, 120))
    assert "entirely inside" in nested and "100.00 and 110.00" in nested


def test_f_b25_warming_window_yields_no_state_and_no_levels():
    """A warming window has no VA; inventing one is the §3.2 mislabelling."""
    for bad in (np.nan, None):
        n = N.va_nesting(100, 110, bad, 120)
        assert n["state"] is None
        assert N.nesting_levels(("90d", "365d"), n) == []
        assert N.price_location(105, n) is None
        assert "warming" in N.describe_nesting(("90d", "365d"), n)


def test_f_b25_price_location():
    inter = N.va_nesting(100, 120, 110, 130)
    assert N.price_location(115, inter) == "inside_consensus"
    assert N.price_location(105, inter) == "inside_short_only"
    assert N.price_location(125, inter) == "inside_long_only"
    assert N.price_location(200, inter) == "outside_all"

    gap = N.va_nesting(140, 150, 100, 120)
    assert N.price_location(130, gap) == "in_gap"
    assert N.price_location(145, gap) == "inside_short_only"
    assert N.price_location(110, gap) == "inside_long_only"


def test_f_b25_levels_emitted_carry_family_and_facing_flag():
    """Consensus and gap edges emit as levels; gap edges are flagged facing."""
    lv = N.nesting_levels(("7d", "30d"), N.va_nesting(100, 120, 110, 130))
    assert [x["level"] for x in lv] == [110.0, 120.0]
    assert all(x["family"] == "profile_windowed" for x in lv)
    assert all(x["facing_edge"] is False for x in lv)

    gap = N.nesting_levels(("7d", "30d"), N.va_nesting(140, 150, 100, 120))
    assert sorted(x["level"] for x in gap) == [120.0, 140.0]
    assert all(x["facing_edge"] is True for x in gap)
    assert all(x["timeframe"] == "7d<->30d" for x in gap)


def test_f_b25_pairs_are_adjacent_scales_only():
    assert N.ADJACENT_PAIRS == (("7d", "30d"), ("30d", "90d"), ("90d", "365d"))


# --------------------------------------------------------------- LVN (§3.4)

def _hist(vals):
    v = np.asarray(vals, float)
    return np.arange(len(v) + 1, dtype=float), v


def test_lvn_finds_an_interior_shelf_and_reports_its_midpoint():
    edges, hist = _hist([10, 10, 10, 0, 0, 0, 10, 10, 10])
    got = P.low_volume_nodes(edges, hist)
    assert len(got) == 1
    n = got[0]
    assert n["low"] == 3.0 and n["high"] == 6.0 and n["mid"] == 4.5
    assert n["rows"] == 3
    assert n["approximation"] == P.APPROXIMATION


def test_lvn_min_rows_and_threshold_are_enforced():
    # a 2-row hole is below LVN_MIN_ROWS
    edges, hist = _hist([10, 10, 0, 0, 10, 10, 10])
    assert P.low_volume_nodes(edges, hist) == []
    # ...and is found when min_rows is relaxed
    assert len(P.low_volume_nodes(edges, hist, min_rows=2)) == 1

    # rows at 30% of the median are NOT thin at threshold 0.25
    edges, hist = _hist([10, 10, 3, 3, 3, 10, 10])
    assert P.low_volume_nodes(edges, hist) == []
    assert len(P.low_volume_nodes(edges, hist, threshold=0.5)) == 1


def test_lvn_ignores_the_extremes():
    """Rows at a window's edges are always thin -- calling them LVNs would emit
    two guaranteed, meaningless levels per window per asset."""
    edges, hist = _hist([0, 0, 0, 10, 10, 10, 0, 0, 0])
    assert P.low_volume_nodes(edges, hist) == [], \
        "runs touching either extreme must be discarded"

    # an all-empty profile must not yield one enormous node
    edges, hist = _hist([0, 0, 0, 0, 0, 0])
    assert P.low_volume_nodes(edges, hist) == []


def test_lvn_threshold_is_relative_to_the_MEDIAN_not_the_mean():
    """A profile peaked at the POC drags the mean up; a mean-relative threshold
    would classify ordinary rows as low-volume on any well-formed profile."""
    hist = np.array([10., 10., 10., 900., 10., 10., 10.])
    edges = np.arange(len(hist) + 1, dtype=float)
    assert float(np.median(hist)) == 10.0
    assert float(np.mean(hist)) > 100.0
    # nothing is below 0.25 x median = 2.5, so there is no LVN here
    assert P.low_volume_nodes(edges, hist) == []


def test_lvn_defaults_match_the_amendment():
    assert P.LVN_THRESHOLD == 0.25 and P.LVN_MIN_ROWS == 3
    assert P.PROFILE_ROWS == 120 and P.VALUE_AREA == 0.70


def test_substrate_tiers_match_amendment_3_3():
    """The substrate actually used must be printed in every capture, and 15m is
    stored for all ten assets, so nothing is silently resampled."""
    assert P.WINDOW_SUBSTRATE["7d"] == "1m"
    assert P.WINDOW_SUBSTRATE["30d"] == "5m"
    assert P.WINDOW_SUBSTRATE["90d"] == "15m"
    assert P.WINDOW_SUBSTRATE["365d"] == "15m"


def test_volume_profile_honours_120_rows_and_70pct():
    rng = np.random.default_rng(11)
    n = 500
    close = 100 + np.cumsum(rng.normal(0, 1, n))
    high, low = close + 0.5, close - 0.5
    vol = np.abs(rng.normal(100, 20, n))
    vp = P.volume_profile(high, low, vol, bins=P.PROFILE_ROWS, value_area=P.VALUE_AREA)
    assert len(vp["hist"]) == 120 and len(vp["edges"]) == 121
    assert vp["val"] <= vp["poc"] <= vp["vah"]
    inside = vp["hist"][(vp["edges"][:-1] >= vp["val"]) & (vp["edges"][1:] <= vp["vah"])]
    assert inside.sum() / vp["hist"].sum() >= 0.60
    assert vp["approximation"] == P.APPROXIMATION


# ------------------------------------------- windowed profiles (§3.1/§3.2/§3.3)

def _bars(days, step_min=15, start_ms=1_700_000_000_000, seed=5):
    rng = np.random.default_rng(seed)
    n = int(days * 24 * 60 / step_min)
    t = np.arange(n, dtype="int64") * step_min * 60_000 + start_ms
    close = 100 + np.cumsum(rng.normal(0, 0.3, n))
    return t, close + 0.4, close - 0.4, np.abs(rng.normal(500, 80, n))


def test_windowed_profile_is_trailing_and_records_its_substrate():
    t, h, l, v = _bars(120)
    as_of = int(t[-1])
    wp = P.windowed_profile(t, h, l, v, 30, as_of, substrate="5m")
    assert wp["warming"] is False
    assert wp["substrate"] == "5m", "the substrate actually used must be carried"
    assert wp["window_start_ms"] == as_of - 30 * 86_400_000
    assert wp["bins"] == 120 and wp["value_area"] == 0.70
    assert wp["val"] <= wp["poc"] <= wp["vah"]
    assert wp["approximation"] == P.APPROXIMATION

    # trailing: a 7d window must use strictly fewer bars than a 30d one
    assert P.windowed_profile(t, h, l, v, 7, as_of)["bars"] < wp["bars"]

    # bars after as_of are excluded outright
    mid = int(t[len(t) // 2])
    assert P.windowed_profile(t, h, l, v, 365, mid)["as_of_ms"] == mid


def test_f_b30_warming_window_prints_no_number():
    """F-B30 mechanism: under 365d of history -> `warming` chip and NO number.

    This is the LITUSDT case measured in probe 0.4: 222.4 days of history, so
    its 365d window can never be honest today.  A 365d VWAP computed on 200 days
    is a 200-day VWAP wearing the wrong label (§3.2).
    """
    t, h, l, v = _bars(222)                       # LITUSDT-shaped history
    as_of = int(t[-1])

    warm = P.windowed_profile(t, h, l, v, 365, as_of, substrate="15m")
    assert warm["warming"] is True, "365d on 222 days of data must be warming"
    assert np.isnan(warm["poc"]) and np.isnan(warm["vah"]) and np.isnan(warm["val"]), \
        "a warming window must print NO number, not a mislabelled one"
    assert warm["lvns"] == []
    assert warm["substrate"] == "15m", "provenance survives the warming path"

    # ...while the windows it DOES cover are honest
    for wd in (7, 30, 90):
        ok = P.windowed_profile(t, h, l, v, wd, as_of)
        assert ok["warming"] is False and np.isfinite(ok["poc"]), f"{wd}d"

    # a warming VA feeds through to nesting as "no state", not as a fake pair
    nest = N.va_nesting(100, 110, warm["val"], warm["vah"])
    assert nest["state"] is None


def test_windowed_profile_warming_is_about_COVERAGE_not_bar_count():
    """An asset listed inside the window has plenty of bars and still cannot
    honestly claim the window."""
    t, h, l, v = _bars(40, step_min=1)            # 40 days at 1m = 57,600 bars
    as_of = int(t[-1])
    wp = P.windowed_profile(t, h, l, v, 90, as_of)
    assert wp["bars"] > 10_000, "the fixture must actually have many bars"
    assert wp["warming"] is True, "many bars must not buy an uncovered window"


def test_lockbox_overlap_is_disclosed_on_every_window():
    """OPERATOR RULING 2026-08-03, and the CONDITION attached to it.

    The seal governs scored outcome evidence, not raw price in a display-only
    trailing window -- granted on condition the overlap is DISCLOSED.  A brief
    that silently read across the holdout is what the condition forbids, so the
    disclosure is asserted here rather than left to the report layer.

    Measured 2026-08-03: only the 365d window reaches the holdout, by 64 days,
    self-clearing 2026-10-06.
    """
    LB0, LB1 = analytics.LOCKBOX_START_MS, analytics.LOCKBOX_END_MS
    DAY = 86_400_000

    clear = analytics.lockbox_overlap(LB1, LB1 + 90 * DAY)
    assert clear["intersects"] is False and clear["overlap_days"] == 0.0

    over = analytics.lockbox_overlap(LB1 - 64 * DAY, LB1 + 300 * DAY)
    assert over["intersects"] is True and over["overlap_days"] == 64.0

    inside = analytics.lockbox_overlap(LB0 + DAY, LB0 + 11 * DAY)
    assert inside["overlap_days"] == 10.0

    before = analytics.lockbox_overlap(LB0 - 30 * DAY, LB0)
    assert before["intersects"] is False

    # every windowed profile carries the record, warming or not
    t, h, l, v = _bars(120)
    for wd in (7, 30, 90, 365):
        wp = P.windowed_profile(t, h, l, v, wd, int(t[-1]))
        assert "lockbox_overlap" in wp, f"{wd}d window has no disclosure"
        assert set(wp["lockbox_overlap"]) >= {"intersects", "overlap_days", "basis"}


def test_nesting_module_is_in_the_analytics_sha():
    """A new module that is not hashed makes analytics_sha a lie."""
    assert "nesting.py" in analytics._MODULES
    assert analytics.analytics_sha() == analytics.analytics_sha()
