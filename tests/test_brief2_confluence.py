"""F-B26 / F-B27 / F-B28 -- the confluence engine (Amendment 2 §5, §7.4).

Run: C:\\venvs\\naiad\\Scripts\\python.exe -m pytest tests/test_brief2_confluence.py -q

F-B26  scale confirmation merges, badges, and does NOT increase score (B-10a).
F-B27  both scored sets present; the excluded set holds zero volume-family members.
F-B28  no weight vector, coefficient array or fitted parameter in the scoring path.
"""

import ast
import inspect
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from analytics import levels as L                                   # noqa: E402

ATR = 100.0


def _lv(family, label, level, timeframe=None, layer="test"):
    return {"family": family, "label": label, "level": float(level),
            "source_layer": layer, "timeframe": timeframe}


# --------------------------------------------------------------- F-B26

def test_f_b26_coincident_window_edges_merge_and_badge():
    """Two windows' VA edges inside the collapse tolerance become ONE member."""
    # 0.02 x 100 = 2.0 wide, so 64000 and 64001 collapse.
    got = L.collapse_same_family(
        [_lv("profile_windowed", "7d VAH", 64000, "7d"),
         _lv("profile_windowed", "30d VAH", 64001, "30d")], ATR)
    assert len(got) == 1, "coincident edges must merge, not double-count"
    m = got[0]
    assert m["collapsed_count"] == 2
    assert m["scale_confirmed"] == ["7d", "30d"], m
    assert m["level"] == pytest.approx(64000.5)


def test_f_b26_scale_confirmation_does_NOT_increase_score():
    """B-10a on the record: it merges and badges, it does not add score.

    Nested windows share data -- the 30d window CONTAINS the 7d window -- so they
    are partially dependent voices, and counted-never-weighted forbids the
    fractional credit partial dependence would deserve.
    """
    one_window = [_lv("profile_windowed", "7d VAH", 64000, "7d")]
    two_windows = [_lv("profile_windowed", "7d VAH", 64000, "7d"),
                   _lv("profile_windowed", "30d VAH", 64001, "30d")]

    s1 = L.score(L.collapse_same_family(one_window, ATR))
    s2 = L.score(L.collapse_same_family(two_windows, ATR))
    assert s2 == s1, (
        f"scale confirmation added score ({s1} -> {s2}) -- B-10a forbids it")

    # and the badge is visibly present on the scored member
    assert "scale_confirmed" in L.collapse_same_family(two_windows, ATR)[0]

    # three windows agreeing is still one voice
    three = two_windows + [_lv("profile_windowed", "90d VAH", 63999, "90d")]
    merged = L.collapse_same_family(three, ATR)
    assert len(merged) == 1 and L.score(merged) == s1
    assert merged[0]["scale_confirmed"] == ["7d", "30d", "90d"]


def test_f_b26_badge_only_where_scales_actually_differ():
    """One window firing twice is not two timescales agreeing."""
    same_window = L.collapse_same_family(
        [_lv("profile_windowed", "7d VAH", 64000, "7d"),
         _lv("profile_windowed", "7d LVN mid", 64001, "7d")], ATR)
    assert "scale_confirmed" not in same_window[0], \
        "one window firing twice must not be badged as scale confirmation"

    # non-scale families are never badged, even with differing timeframes
    structure = L.collapse_same_family(
        [_lv("structure", "prior D high", 64000, "1d"),
         _lv("structure", "prior W high", 64001, "1w")], ATR)
    assert "scale_confirmed" not in structure[0]


def test_f_b26_windows_further_apart_than_tolerance_do_not_merge():
    """ANTI-VACUITY: the merge must be the tolerance doing work, not everything
    collapsing regardless."""
    apart = L.collapse_same_family(
        [_lv("profile_windowed", "7d VAH", 64000, "7d"),
         _lv("profile_windowed", "30d VAH", 64500, "30d")], ATR)
    assert len(apart) == 2, "levels 5 ATR-hundredths apart must stay separate"
    assert all("scale_confirmed" not in m for m in apart)


def test_f_b26_scale_confirmed_windows_are_in_scale_order():
    merged = L.collapse_same_family(
        [_lv("profile_windowed", "365d VAL", 64000, "365d"),
         _lv("profile_windowed", "7d VAL", 64001, "7d"),
         _lv("profile_windowed", "90d VAL", 63999.5, "90d")], ATR)
    assert merged[0]["scale_confirmed"] == ["7d", "90d", "365d"], \
        "badge must read in scale order, not alphabetical"


# --------------------------------------------------------------- F-B27

def _mixed_registry():
    return [
        _lv("vwap_anchored", "M anchor", 63900, "1M"),
        _lv("vwap_anchored", "Q anchor 1s", 64400, "1Q"),
        _lv("vwap_rolling", "7d RVWAP", 63910, "7d"),
        _lv("vwap_rolling", "30d RVWAP 1s", 64380, "30d"),
        _lv("profile_windowed", "30d POC", 63905, "30d"),
        _lv("profile_windowed", "90d VAH", 64420, "90d"),
        _lv("structure", "prior D high", 64405, "1d"),
        _lv("structure", "prior W low", 63180, "1w"),
        _lv("ss", "Z2 upper", 64395, "4h"),
    ]


def test_f_b27_both_scored_sets_are_present():
    out = L.dual_score(_mixed_registry(), ATR, price=64100)
    assert set(out) >= {"with_volume", "without_volume", "differ"}
    for view in ("with_volume", "without_volume"):
        v = out[view]
        assert {"clusters", "lines", "member_count", "sensitivity",
                "by_family"} <= set(v)
        assert v["clusters"], f"{view} produced no clusters"


def test_f_b27_collapsed_registry_is_stored_once_only():
    """D-1: every member lands in exactly one cluster, so a flat `members` list
    beside `clusters[].members` stored the registry TWICE -- 18.12% of the
    2026-08-03 capture. The nested form is the single source."""
    out = L.dual_score(_mixed_registry(), ATR, price=64100)
    for view in ("with_volume", "without_volume"):
        v = out[view]
        assert "members" not in v, \
            "the flat members list is back -- the registry is stored twice again"
        nested = [m for cl in v["clusters"] for m in cl["members"]]
        assert len(nested) == v["member_count"], \
            "member_count must equal the members actually held in clusters"

    # ANTI-VACUITY: the nested form must genuinely still be there and populated
    wv = out["with_volume"]
    assert wv["member_count"] > 0
    assert all("family" in m and "level" in m
               for cl in wv["clusters"] for m in cl["members"])


def test_f_b27_excluded_set_contains_zero_volume_family_members():
    """The assertion the amendment names: the excluded set holds none of them."""
    out = L.dual_score(_mixed_registry(), ATR, price=64100)
    without = out["without_volume"]

    for fam in L.VOLUME_FAMILIES:
        assert without["by_family"][fam] == 0, f"{fam} leaked into without_volume"

    for cl in without["clusters"]:
        for m in cl["members"]:
            assert m["family"] not in L.VOLUME_FAMILIES, \
                f"{m['family']} member {m['label']} leaked into a cluster"
        assert not (set(cl["families"]) & set(L.VOLUME_FAMILIES))

    # ANTI-VACUITY: the with_volume view must actually contain them, or the
    # assertion above is satisfied by an empty registry.
    assert sum(out["with_volume"]["by_family"][f] for f in L.VOLUME_FAMILIES) == 4
    assert without["levels_in"] < out["with_volume"]["levels_in"]


def test_f_b27_exclusion_happens_before_collapse():
    """Dropping volume levels after clustering would leave cluster means already
    pulled by them -- a relabelled with-volume answer, not the without one."""
    reg = [_lv("vwap_anchored", "M anchor", 64000, "1M"),
           _lv("vwap_rolling", "7d RVWAP", 64001, "7d")]
    out = L.dual_score(reg, ATR, price=64000)
    wv = out["with_volume"]["clusters"][0]["mean"]
    nv = out["without_volume"]["clusters"][0]["mean"]
    assert wv == pytest.approx(64000.5)
    assert nv == pytest.approx(64000.0), \
        "the without-volume mean is still pulled by a volume level"


def test_f_b27_dual_scoring_records_whether_the_lines_moved():
    """Calibration §9.2 item 6 -- the comparison must be computed, not eyeballed."""
    out = L.dual_score(_mixed_registry(), ATR, price=64100)
    d = out["differ"]
    assert set(d) >= {"above", "below", "any_changed"}
    for side in ("above", "below"):
        assert set(d[side]) >= {"changed", "with_volume", "without_volume"}
    assert isinstance(d["any_changed"], bool)

    # a registry where volume levels are the ONLY thing above price must move
    reg = [_lv("structure", "prior W low", 63000, "1w"),
           _lv("vwap_rolling", "7d RVWAP", 64500, "7d"),
           _lv("profile_windowed", "30d VAH", 64505, "30d")]
    moved = L.dual_score(reg, ATR, price=64000)["differ"]
    assert moved["above"]["changed"] is True
    assert moved["above"]["without_volume"] is None


def test_f_b27_families_are_the_revised_five():
    assert L.FAMILIES == ("vwap_anchored", "vwap_rolling", "profile_windowed",
                          "structure", "ss")
    assert L.VOLUME_FAMILIES == ("vwap_rolling", "profile_windowed")
    with pytest.raises(ValueError):
        L.LevelRegistry().add("profile", "old name", 1.0, "x")


def test_f_b27_thresholds_are_unchanged_by_the_amendment():
    """§5.2: the rules are unchanged and printed in every capture."""
    assert (L.COLLAPSE_ATR, L.CLUSTER_ATR, L.LIS_ATR, L.FAMILY_CAP) == \
        (0.02, 0.15, 1.5, 3)


# --------------------------------------------------------------- F-B28

SCORING_PATH = ("levels.py", "nesting.py")

# Words that would indicate a fitted model. `weight` catches weight/weights/
# weighted; `volume-weighted` is the one legitimate use and is excluded by name
# because it describes an ARITHMETIC MEAN of price by volume, not a fitted
# parameter -- see vwap.py's pinned TradingView recipe.
BANNED = ("weight", "coef", "coeff", "intercept", "beta_hat", "fitted",
          "regress", "logit", "sigmoid", "learn", "train", "gradient",
          "optimi", "calibrat_", "param_vector", "theta")

ALLOWED_SUBSTRINGS = ("volume-weighted", "volume_weighted", "counted-never-weighted",
                      "never-weighted", "counted, never weighted", "equal weights",
                      "half-weight", "weighed", "weigh")


def test_f_b28_no_weight_vector_in_the_scoring_path():
    """§7.4: a live display instrument that ships fitted weights is a machine
    flattering itself with its own history.  Nothing here may implement rung 3.
    """
    for name in SCORING_PATH:
        src = (ROOT / "analytics" / name).read_text(encoding="utf-8")
        low = src.lower()
        for token in BANNED:
            idx = 0
            while True:
                i = low.find(token, idx)
                if i < 0:
                    break
                ctx = low[max(0, i - 40):i + 40]
                assert any(a in ctx for a in ALLOWED_SUBSTRINGS), (
                    f"{name}: banned token {token!r} in the scoring path -- "
                    f"...{ctx.strip()}...")
                idx = i + 1


def test_f_b28_score_is_pure_counting():
    """The score function must contain no multiplication by a constant table."""
    src = inspect.getsource(L.score)
    tree = ast.parse(src.lstrip())
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Mult):
            pytest.fail(f"score() multiplies -- counting never scales: {src}")
        if isinstance(node, ast.Constant) and isinstance(node.value, float):
            pytest.fail(f"score() holds a float constant: {node.value}")


def test_f_b28_score_is_count_based_and_capped():
    """Equal weights, count-based: N members of one family score min(N, cap)."""
    fam = [_lv("structure", f"s{i}", 64000 + i * 1000, None) for i in range(6)]
    assert L.score(fam) == L.FAMILY_CAP + 1        # capped members + 1 family

    mixed = [_lv("structure", "a", 1, None), _lv("ss", "b", 2, None),
             _lv("vwap_anchored", "c", 3, None)]
    assert L.score(mixed) == 3 + 3                # 3 members + 3 families

    # doubling every family's membership cannot double the score
    doubled = mixed + [_lv("structure", "d", 4, None), _lv("ss", "e", 5, None),
                       _lv("vwap_anchored", "f", 6, None)]
    assert L.score(doubled) == 6 + 3


def test_f_b28_scores_are_integers():
    """A fitted model produces floats; counting produces integers."""
    out = L.dual_score(_mixed_registry(), ATR, price=64100)
    for view in ("with_volume", "without_volume"):
        for cl in out[view]["clusters"]:
            assert isinstance(cl["score"], int), \
                f"non-integer score {cl['score']!r} -- counting produces integers"


# ------------------------------------------------- F-B35 registry completion

def test_f_b35_prior_anchors_and_confirmed_pivots_reach_the_registry():
    """Stage B, cycle 3. Two reviewer findings, fixtured so they cannot recur.

    (1) D2-3(a): prior M/Q/Y anchored VWAPs are ratified at D-B11 and appear by
        name in the operator's manual reviews. They were absent.
    (2) F-3R-A: `structure` reported EXACTLY 13 levels for all ten assets,
        because the registry was fed by daily_brief's `last_pivots(..., n=3)` --
        a DISPLAY cap -- while `analytics.confirmed_pivots` was never emitted at
        all. Ten instruments cannot share a pivot count.
    """
    import sys as _sys
    from pathlib import Path as _P
    _sys.path.insert(0, str(_P(__file__).resolve().parent.parent / "scripts"))
    import brief2 as B2

    # `bars` is a MATURE month on the 1h substrate (~720). It is supplied
    # explicitly because R3's floors gate on sample depth, and an anchor with no
    # countable depth is treated as immature rather than waved through.
    prior = {"prior_M": {"warming": False, "vwap": 100.0, "sigma": 2.0, "bars": 720,
                         "bands": {f"{s}{k}s": 100.0 + (1 if s == "+" else -1) * k * 2.0
                                   for k in (1, 2, 3) for s in ("+", "-")}},
             "prior_Q": {"warming": True, "reason": "no completed prior period"}}
    pivots = {"lookback_days": 180,
              "highs": [{"level": 120.0, "index": 5}, {"level": 130.0, "index": 9}],
              "lows": [{"level": 80.0, "index": 7}]}
    a = {"vwap": {}, "structure": {"pivot_highs": [{"level": 999.0, "day": "x"}]},
         "sessions": {}, "radar": []}
    reg = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                            prior_anchors=prior, pivots=pivots)
    labels = [x["label"] for x in reg.as_list()]

    # prior anchors: 1 vwap + 6 bands for the armed period; warming one emits none
    assert sum(1 for x in reg.as_list() if x["source_layer"] == "prior_anchor") == 7
    assert any("prior_M VWAP" in s for s in labels)
    assert not any("prior_Q" in s for s in labels), "a warming prior anchor emitted levels"

    # confirmed pivots replace the display-capped list, and vary in count
    cp = [x for x in reg.as_list() if x["source_layer"] == "confirmed_pivots"]
    assert len(cp) == 3, "confirmed pivots did not reach the registry"
    assert not any("999" in str(x["level"]) for x in reg.as_list()), \
        "daily_brief's display-capped pivot leaked in alongside the confirmed ones"

    # ANTI-VACUITY: without pivots the builder must fall back, not emit nothing
    reg2 = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                             prior_anchors=None, pivots=None)
    assert any(x["source_layer"] == "structure_layer" for x in reg2.as_list())


def test_f_b37_r3_maturity_floors_withhold_immature_vwap_levels():
    """F-B37 -- operator ruling R3, 2026-08-05.

    A VWAP over a handful of bars is arithmetically exact and informationally
    empty. The LINE enters the registry at >= 10 bars, the SIGMA BANDS at >= 30.
    Below the floor the value still PRINTS with a `thin_sample` chip and is
    excluded from SCORING only -- so this asserts three separable things:

      1. the floors BIND (an immature anchor contributes no scored levels),
      2. they bind SEPARATELY (line and bands have different floors, so the
         band-only case must exist and be reachable),
      3. every withholding is AUDITABLE (recorded with bar count and floor),
         because a filter nobody can inspect is indistinguishable from a bug.
    """
    import sys as _sys
    from pathlib import Path as _P
    _sys.path.insert(0, str(_P(__file__).resolve().parent.parent / "scripts"))
    import brief2 as B2
    from analytics import vwap as W

    assert (W.LINE_MIN_BARS, W.BAND_MIN_BARS) == (10, 30), \
        "R3's interim floors moved without the fixture moving with them"

    def _prior(bars):
        return {"prior_M": {"warming": False, "vwap": 100.0, "sigma": 2.0,
                            "bars": bars,
                            "bands": {f"{s}{k}s": 100.0 + (1 if s == "+" else -1) * k * 2.0
                                      for k in (1, 2, 3) for s in ("+", "-")}}}

    a = {"vwap": {}, "structure": {}, "sessions": {}, "radar": []}
    lvls = lambda reg: [x for x in reg.as_list() if x["source_layer"] == "prior_anchor"]

    # 3 bars -- below BOTH floors: nothing scored, 7 rows withheld.
    r3 = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                           prior_anchors=_prior(3))
    assert lvls(r3) == [], "a 3-bar anchor cast confluence votes"
    assert len(r3.withheld) == 7 and r3.withheld[0]["bars"] == 3

    # 15 bars -- ABOVE the line floor, BELOW the band floor. This is the case
    # the two-floor design exists for: a mature mean whose dispersion estimate
    # is not yet meaningful. One line scored, six bands withheld.
    r15 = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                            prior_anchors=_prior(15))
    assert len(lvls(r15)) == 1 and lvls(r15)[0]["label"] == "prior_M VWAP"
    assert len(r15.withheld) == 6
    assert {w["level"] for w in r15.withheld} == {"band"}, \
        "the line was withheld at 15 bars, above its own floor of 10"

    # 720 bars -- a full month on 1h: everything admitted, nothing withheld.
    r720 = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                             prior_anchors=_prior(720))
    assert len(lvls(r720)) == 7 and r720.withheld == []

    # UNCOUNTABLE depth is treated as immature, not waved through.
    rnone = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [],
                              prior_anchors=_prior(None))
    assert lvls(rnone) == [], "an anchor with no countable sample was scored anyway"

    # AUDITABILITY: every withheld row names what failed and against what floor.
    for w in r3.withheld:
        assert w["level"] in ("line", "band") and w["floor"] in (10, 30)
        assert w["label"] and w["what"] and w["reason"]


def test_f_b35_confirmed_pivots_use_a_lookback_not_a_count_cap():
    """A count cap is what produced the uniform 13. A trailing lookback is
    self-limiting and varies per asset, as pivot counts must."""
    import sys as _sys
    from pathlib import Path as _P
    _sys.path.insert(0, str(_P(__file__).resolve().parent.parent / "scripts"))
    import brief2 as B2
    import ast
    import inspect
    src = inspect.getsource(B2.confirmed_pivot_levels)
    assert "lookback_days" in src
    assert "confirmed_pivots" in src, "must use the causality-disciplined entry point"

    # Scan CODE, not prose: this function's docstring QUOTES the defect it
    # replaced ("last_pivots(..., n=3)"), and a naive substring scan flags the
    # sentence that explains the fix as if it were the fix's absence. Same false
    # positive as F-F3's prohibition text.
    tree = ast.parse(src.lstrip())
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)):
                node.body[0].value.value = ""
    code = ast.unparse(tree)
    assert "n=3" not in code and "[:3]" not in code, "a count cap has come back"
    assert "lookback_days" in code, "the stripper ate the code, not just the prose"


# The F-B41 block below uses brief2 at module scope. Earlier tests in this file
# import it lazily inside each function; both work, and this keeps the new block
# readable rather than repeating four lines of path juggling seven times.
sys.path.insert(0, str(ROOT / "scripts"))
import brief2 as B2                                                 # noqa: E402
from analytics import vwap as W                                     # noqa: E402


# ------------------------------- F-B41  stage 5.2/5.3/5.4 REVERSION archetype

def _stretch_for(name, mean, sigma, price, atr, bars=200, kind="rolling"):
    return {"rows": [B2._stretch_row(name, kind, mean, sigma, price, atr, bars=bars)]}


def test_f_b41_reversion_rr_is_a_constant_of_the_geometry():
    """5.3's PREMISE, asserted rather than assumed.

    Entry at sigma2 targeting the mean earns 2 sigma against a 1-sigma stop at
    sigma3: exactly 2:1. At sigma3 it is exactly 3:1. This holds for every
    anchor, every window, every asset and every price -- which is precisely why
    R:R cannot rank reversion drafts and something else must.
    """
    mean, sigma, atr = 1000.0, 50.0, 25.0
    for k, want in ((2, 2.0), (3, 3.0)):
        for direction in (+1, -1):
            px = mean + direction * (k + 0.05) * sigma        # just past the band
            st = _stretch_for("RVWAP 30d", mean, sigma, px, atr)
            rd = B2.reversion_drafts(st, {}, px, atr)
            assert rd["count"] == 1, (k, direction)
            d = rd["drafts"][0]
            assert d["rr"] == pytest.approx(want), \
                f"sigma{k} reversion must be exactly {want}:1, got {d['rr']}"
            assert d["entry_band"] == f"{'+' if direction > 0 else '-'}{k}s"
            assert d["side"] == ("short" if direction > 0 else "long")
            assert d["target"] == pytest.approx(mean), "the target IS the mean"
            # invalidation is exactly one band further out than the entry
            assert abs(d["invalidation"] - mean) == pytest.approx((k + 1) * sigma)
            assert d["rr_is_constant"] is True


def test_f_b41_ranking_is_by_band_confluence_score_not_by_rr():
    """5.3 -- the reviewer's design decision, made falsifiable.

    Two drafts with IDENTICAL R:R and different band scores must order by score.
    If this test can be made to pass by sorting on R:R, it guards nothing.
    """
    atr = 10.0
    price = 1300.0
    # BOTH means sit at +2.2 sigma from price, so both drafts enter at sigma2 and
    # both therefore carry R:R exactly 2.0. Only the sigma WIDTH differs, which
    # puts their entry bands at different prices and lets them land in different
    # clusters. Anything that ranks these by R:R cannot order them at all.
    st = {"rows": [
        B2._stretch_row("anchored M", "anchored", 1080.0, 100.0, price, atr, bars=200),
        B2._stretch_row("anchored Q", "anchored", 1190.0, 50.0, price, atr, bars=200),
    ]}
    # entries: M -> 1080 + 2*100 = 1280 ; Q -> 1190 + 2*50 = 1290
    conf = {"with_volume": {"clusters": [
        {"mean": 1280.0, "score": 3, "families": ["vwap_anchored"], "members": []},
        {"mean": 1290.0, "score": 11, "families": ["vwap_anchored", "structure"],
         "members": []},
    ]}}
    rd = B2.reversion_drafts(st, conf, price, atr)
    assert rd["count"] == 2
    first, second = rd["drafts"]
    assert first["rr"] == pytest.approx(second["rr"]), \
        "the two drafts must have EQUAL R:R or this test proves nothing"
    assert first["band_confluence_score"] == 11 and second["band_confluence_score"] == 3
    assert first["name"] == "anchored Q" and first["rank"] == 1
    assert "confluence score of the BAND" in rd["ranked_by"]


def test_f_b41_entry_requires_price_to_have_actually_reached_the_band():
    """The entry is an OBSERVATION, never a forecast. No draft exists until
    price is past the band at the close."""
    mean, sigma, atr = 1000.0, 50.0, 25.0

    # inside sigma2 -- nothing, however close
    for px in (mean + 1.99 * sigma, mean - 1.99 * sigma, mean):
        st = _stretch_for("RVWAP 7d", mean, sigma, px, atr)
        assert B2.reversion_drafts(st, {}, px, atr)["count"] == 0, \
            "a draft appeared for a band price has not reached"

    # exactly at sigma2 -- reached
    px = mean + 2.0 * sigma
    st = _stretch_for("RVWAP 7d", mean, sigma, px, atr)
    assert B2.reversion_drafts(st, {}, px, atr)["count"] == 1

    # sigma1 alone never produces a reversion draft
    px = mean + 1.5 * sigma
    st = _stretch_for("RVWAP 7d", mean, sigma, px, atr)
    assert B2.reversion_drafts(st, {}, px, atr)["count"] == 0
    assert B2.REVERSION_ENTRY_SIGMAS == (2, 3)


def test_f_b41_thin_sample_cannot_manufacture_a_draft():
    """D4-2 -- a freshly-opened anchor must not turn a two-bar sigma into a
    setup. The skip is RECORDED, not silent."""
    mean, sigma, atr = 1000.0, 50.0, 25.0
    px = mean + 2.5 * sigma
    st = _stretch_for("anchored W", mean, sigma, px, atr, bars=2, kind="anchored")
    rd = B2.reversion_drafts(st, {}, px, atr)
    assert rd["count"] == 0, "a 2-bar sigma produced a tradeable draft"
    assert len(rd["skipped_thin_sample"]) == 1
    assert rd["skipped_thin_sample"][0]["bars"] == 2
    assert "thin_sample" in rd["skipped_thin_sample"][0]["reason"]

    # and the same geometry with a mature sample DOES produce one, or the gate
    # is indistinguishable from the feature being broken
    st2 = _stretch_for("anchored W", mean, sigma, px, atr, bars=200, kind="anchored")
    assert B2.reversion_drafts(st2, {}, px, atr)["count"] == 1


def test_f_b41_sigma_width_in_atr_distinguishes_identical_geometry():
    """5.4 -- identical R:R, wildly different trades. A board printing only the
    ratio would present a day trade and a multi-month position as the same."""
    atr = 1628.44005908                      # BTC daily ATR, 2026-08-05
    fast_sigma, slow_sigma = 0.4 * atr, 11.4 * atr

    out = []
    for name, sigma in (("RVWAP 7d", fast_sigma), ("RVWAP 365d", slow_sigma)):
        mean = 60000.0
        # 2.05 sigma, not exactly 2.0: at an irrational sigma the round-trip
        # (mean + 2*sigma - mean) / sigma can land a half-ulp under 2.0 and the
        # `>=` boundary would then correctly refuse the draft. The boundary is
        # right; pinning a fixture to a float coincidence would not be.
        px = mean + 2.05 * sigma
        d = B2.reversion_drafts(_stretch_for(name, mean, sigma, px, atr),
                                {}, px, atr)["drafts"][0]
        out.append(d)

    fast, slow = out
    assert fast["rr"] == pytest.approx(slow["rr"]) == pytest.approx(2.0), \
        "the two setups must be geometrically identical for this to mean anything"
    assert fast["sigma_atr"] == pytest.approx(0.4, abs=0.01)
    assert slow["sigma_atr"] == pytest.approx(11.4, abs=0.01)
    assert fast["target_distance_atr"] == pytest.approx(0.8, abs=0.02)
    assert slow["target_distance_atr"] == pytest.approx(22.8, abs=0.05)
    assert slow["target_distance_atr"] > 6.0 > fast["target_distance_atr"], \
        "these must land in different distance buckets (5.5)"


def test_f_b41_reversion_claims_no_probability_and_prescribes_no_size():
    """The permanent constraints. R:R is GEOMETRY; whether a reversion pays is
    H-VBR, census work under G-7."""
    mean, sigma, atr = 1000.0, 50.0, 25.0
    px = mean + 2.5 * sigma
    rd = B2.reversion_drafts(_stretch_for("RVWAP 30d", mean, sigma, px, atr),
                             {}, px, atr)
    d = rd["drafts"][0]
    assert d["no_sizing"] is True and d["contains_no_probability_claim"] is True
    assert "H-VBR" in rd["claims_nothing"] and "G-7" in rd["claims_nothing"]

    # SEVENTH INSTANCE of the same false positive, and this time the fixture was
    # the one carrying it: `contains_no_probability_claim` and `no_sizing` are
    # DISCLAIMERS, and a scan that reads them flags the promise as the offence.
    # Strip the disclaimer keys, then scan the payload -- scan what the layer
    # SAYS ABOUT THE MARKET, never the flags that say what it refuses to say.
    DISCLAIMERS = ("contains_no_probability_claim", "no_sizing", "rr_is_constant")
    payload = [{k: v for k, v in d.items() if k not in DISCLAIMERS}
               for d in rd["drafts"]]
    assert payload and all(len(p) > 10 for p in payload), \
        "stripping the disclaimers emptied the payload -- the scan is vacuous"

    blob = repr(payload).lower()
    for banned in ("probability", "likely", "expectancy", "win_rate", "size",
                   "qty", "leverage", "forecast", "predict"):
        assert banned not in blob, f"predictive or sizing language in a DRAFT: {banned}"

    # and the disclaimers must still actually be set on every draft
    assert all(d["no_sizing"] and d["contains_no_probability_claim"]
               for d in rd["drafts"])


def test_f_b41_reversion_populates_the_far_buckets_continuation_cannot():
    """WHY THIS ARCHETYPE EXISTS. Cycle 4 measured all 40 continuation targets in
    NEAR (<2 ATR) and MID/FAR both EMPTY, because the next opposing cluster is
    always close in a 148-level registry. Reversion targets the MEAN, which for
    the far anchors is where the long distance lives."""
    import brief_render as BR
    atr = 1000.0
    mean, sigma = 60000.0, 8.0 * atr          # a far anchor
    px = mean - 2.2 * sigma
    d = B2.reversion_drafts(_stretch_for("prior Y", mean, sigma, px, atr),
                            {}, px, atr)["drafts"][0]
    assert BR.target_bucket(d["target_distance_atr"]) == "FAR"
    assert d["side"] == "long" and d["target"] == pytest.approx(mean)


# ============================= F-B42  cycle 5 item 3.1 -- G7 ANCHOR DEGENERACY
#
# BUILT ON A REAL OPERATOR CAPTURE, not synthetic geometry. BINANCE:BTCUSDT.P,
# 1H, hlc3, closed bar 2026-07-26T20:00Z. July opens Q3, so the Month and
# Quarter anchors are BOTH 2026-07-01 -- the same bar -- and our computed levels
# came out byte-identical to the last decimal, sigma included.

# The real values, from scripts/parity_c5_worksheet.py against the live estate.
C5_A_DEGENERATE_VWAP = 63334.048643
C5_A_DEGENERATE_SIGMA = 1729.988691
C5_A_ATR = 1628.44005908


def _c5_capture_a(anchored_only=True):
    return {"vwap": {"anchored": {
        "W": {"vwap": 65190.810716, "sigma": 798.4663, "bars": 165,
              "anchor_utc": "2026-07-20T00:00:00Z"},
        "M": {"vwap": C5_A_DEGENERATE_VWAP, "sigma": C5_A_DEGENERATE_SIGMA,
              "bars": 621, "anchor_utc": "2026-07-01T00:00:00Z"},
        "Q": {"vwap": C5_A_DEGENERATE_VWAP, "sigma": C5_A_DEGENERATE_SIGMA,
              "bars": 621, "anchor_utc": "2026-07-01T00:00:00Z"},
    }}, "structure": {}, "sessions": {}, "radar": []}


def test_f_b42_july_month_and_quarter_anchors_are_identical_by_construction():
    """The identity itself, on the real capture. If these ever differ, either
    the anchor arithmetic or the calendar assumption has broken."""
    a = _c5_capture_a()
    m, q = a["vwap"]["anchored"]["M"], a["vwap"]["anchored"]["Q"]
    assert m["anchor_utc"] == q["anchor_utc"] == "2026-07-01T00:00:00Z"
    assert m["vwap"] == q["vwap"] and m["sigma"] == q["sigma"]
    assert m["bars"] == q["bars"] == 621


def test_f_b42_degenerate_anchors_collapse_to_seven_not_fourteen():
    """THE FAILURE THIS PREVENTS: fourteen identical levels entering the
    registry uncollapsed would count ONE tool as TWO agreeing voices, at every
    one of the seven prices, in the family that already contributes the most
    members."""
    # THE DEGENERACY IN ISOLATION. The Week anchor is deliberately left out
    # here -- see the next assertion block for why keeping it in would test two
    # things at once and prove neither.
    a = _c5_capture_a()
    del a["vwap"]["anchored"]["W"]
    reg = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [])
    raw = [x for x in reg.as_list() if x["source_layer"] == "vwap_complex"]
    assert len(raw) == 14, "the degenerate pair did not produce 14 raw levels"

    merged = L.collapse_same_family(reg.as_list(), C5_A_ATR)
    assert len(merged) == 7, \
        f"14 identical levels collapsed to {len(merged)}, expected 7 -- one " \
        f"tool would be counted as two agreeing voices"

    deg_prices = [C5_A_DEGENERATE_VWAP + k * C5_A_DEGENERATE_SIGMA
                  for k in (-3, -2, -1, 0, 1, 2, 3)]
    for p in deg_prices:
        hits = [m for m in merged if abs(m["level"] - p) < 1e-6]
        assert len(hits) == 1, f"price {p} did not collapse to one member"
        assert hits[0]["collapsed_count"] == 2, \
            f"price {p} merged {hits[0]['collapsed_count']} members, expected 2"
        # AUDITABLE: the merged member must still name BOTH contributors, or
        # the collapse is indistinguishable from silently dropping one.
        lab = str(hits[0].get("labels") or hits[0].get("label"))
        assert "M" in lab and "Q" in lab, f"merged member lost a contributor: {lab}"


def test_f_b42_the_real_capture_also_merges_the_week_anchor_at_two_sigma():
    """A SECOND, GENUINE merge in the same capture -- recorded because it looks
    like the degeneracy and is not.

    On this bar Week +2sigma is 66,787.75 and Month/Quarter +2sigma is
    66,794.03: 6.28 apart, inside the 32.57 collapse width (0.02 x 1,628.44
    daily ATR). So the full capture collapses those THREE into one member, not
    two.

    That is not calendar degeneracy -- the Week anchor is a genuinely different
    anchor that happens to land nearby -- but the scoring consequence is the
    same and correct either way: `vwap_anchored` contributes ONE voice at that
    price, not three. Asserting 'exactly 2' on the full capture would have been
    wrong, and the first version of this fixture made exactly that error.
    """
    reg = B2.build_registry(_c5_capture_a(), {"windows": {}}, {"windows": {}}, [])
    merged = L.collapse_same_family(reg.as_list(), C5_A_ATR)
    two_sig = [m for m in merged if abs(m["level"] - 66790.9) < 20.0]
    assert len(two_sig) == 1, "Week and Month/Quarter +2s did not merge"
    assert two_sig[0]["collapsed_count"] == 3, \
        f"expected a 3-way merge, got {two_sig[0]['collapsed_count']}"
    lab = str(two_sig[0].get("labels") or two_sig[0].get("label"))
    assert "W" in lab and "M" in lab and "Q" in lab

    # ANTI-VACUITY: the collapse must be the TOLERANCE doing work. The Week and
    # Month MEANS are 1,856 apart and must NOT merge.
    means = [m for m in merged if abs(m["level"] - 65190.81) < 1.0]
    assert means and means[0]["collapsed_count"] == 1, \
        "the Week mean merged with something it is 1,856 away from"


def test_f_b42_degeneracy_note_fires_and_names_the_calendar():
    """A reader seeing a 2-member cluster must be able to tell whether two tools
    agreed or one tool was counted twice. Those are opposite facts wearing the
    same shape, so the collapse has to be VISIBLE, not merely correct."""
    deg = B2.anchor_degeneracy(_c5_capture_a())
    assert len(deg) == 1, "the M=Q degeneracy was not reported"
    g = deg[0]
    assert set(g["anchors"]) == {"M", "Q"}
    assert g["anchor"] == "2026-07-01T00:00:00Z"
    assert g["duplicate_levels"] == 14 and g["collapses_to"] == 7
    assert g["adds_no_score"] is True
    assert "calendar" in g["why"].lower()

    # ANTI-VACUITY: a normal capture with distinct anchors reports NOTHING.
    clean = {"vwap": {"anchored": {
        "W": {"vwap": 1.0, "sigma": 1.0, "bars": 100,
              "anchor_utc": "2026-08-03T00:00:00Z"},
        "M": {"vwap": 2.0, "sigma": 1.0, "bars": 100,
              "anchor_utc": "2026-08-01T00:00:00Z"},
        "Q": {"vwap": 3.0, "sigma": 1.0, "bars": 100,
              "anchor_utc": "2026-07-01T00:00:00Z"}}}}
    assert B2.anchor_degeneracy(clean) == [], \
        "the note fires on non-degenerate anchors -- it would flag everything"


# ============================= F-B43  cycle 5 item 3.2 -- MATURITY FLOOR, REAL
#
# Capture (B), BINANCE:BTCUSDT.P 1H hlc3, closed bar 2026-08-02T04:00Z. The
# Month anchor opened 2026-08-01T00:00Z, so it carries 29 hourly bars -- one
# short of R3's 30-bar BAND floor. This is the floor's justifying case, found in
# real data rather than argued for.

C5_B_MONTH_BARS = 29
C5_B_SIGMA_WEEK = 754.4595
C5_B_SIGMA_MONTH = 313.3966
C5_B_SIGMA_QUARTER = 1608.6236


def test_f_b43_immature_month_withholds_bands_but_prints_the_line():
    a = {"vwap": {"anchored": {
        "M": {"vwap": 62926.056254, "sigma": C5_B_SIGMA_MONTH,
              "bars": C5_B_MONTH_BARS, "anchor_utc": "2026-08-01T00:00:00Z"}}},
         "structure": {}, "sessions": {}, "radar": []}
    reg = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [])
    lv = [x for x in reg.as_list() if x["source_layer"] == "vwap_complex"]

    assert C5_B_MONTH_BARS < W.BAND_MIN_BARS, "the case is no longer immature"
    assert C5_B_MONTH_BARS >= W.LINE_MIN_BARS, "the line floor should still pass"

    assert len(lv) == 1, f"expected the LINE alone, got {len(lv)} levels"
    assert lv[0]["label"] == "M anchored VWAP"
    assert len(reg.withheld) == 6, "the six band levels were not withheld"
    assert {w["level"] for w in reg.withheld} == {"band"}
    assert all(w["bars"] == C5_B_MONTH_BARS and w["floor"] == W.BAND_MIN_BARS
               for w in reg.withheld)

    # ONE MORE BAR admits everything -- proving the floor, not a broken layer.
    a["vwap"]["anchored"]["M"]["bars"] = W.BAND_MIN_BARS
    reg2 = B2.build_registry(a, {"windows": {}}, {"windows": {}}, [])
    assert len(reg2.as_list()) == 7 and reg2.withheld == []


def test_f_b43_immaturity_inverts_the_scale_ladder():
    """THE CONCRETE JUSTIFICATION FOR THE FLOOR.

    A longer lookback must not disperse LESS than a shorter one. On this real
    bar the 29-bar Month sigma is 313.40 against the 149-bar Week's 754.46 --
    41.5%, well under half. The monthly band is therefore NARROWER than the
    weekly one, which is structurally backwards and is caused purely by
    immaturity, not by the market.
    """
    assert C5_B_SIGMA_MONTH < C5_B_SIGMA_WEEK / 2.0, \
        "the inversion this fixture documents has gone away"
    assert C5_B_SIGMA_WEEK < C5_B_SIGMA_QUARTER, \
        "week vs quarter should be correctly ordered -- only Month is immature"

    # The ladder is monotonic in lookback ONCE the immature rung is removed.
    mature = [C5_B_SIGMA_WEEK, C5_B_SIGMA_QUARTER]
    assert mature == sorted(mature), "the mature rungs are themselves inverted"

    # Width, in daily ATR -- the units a reader acts in.
    atr = C5_A_ATR
    assert round(C5_B_SIGMA_MONTH / atr, 3) == 0.192
    assert round(C5_B_SIGMA_WEEK / atr, 3) == 0.463
    assert round(C5_B_SIGMA_QUARTER / atr, 3) == 0.988
