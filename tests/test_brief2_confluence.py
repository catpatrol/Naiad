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
        assert {"clusters", "lines", "members", "sensitivity", "by_family"} <= set(v)
        assert v["clusters"], f"{view} produced no clusters"


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
