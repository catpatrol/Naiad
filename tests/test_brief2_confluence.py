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
