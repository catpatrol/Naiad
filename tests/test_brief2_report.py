"""F-B29 / F-B31 / F-B33 -- the report layer (Amendment 2 §2, §3.5, §4.2, §7).

Run: C:\\venvs\\naiad\\Scripts\\python.exe -m pytest tests/test_brief2_report.py -q

F-B29  R:R integrity -- every printed ratio recomputes from its own printed
       components, and no ratio prints without entry, invalidation and target.
F-B31  forming-candle isolation -- drawn on 1W/1M, present in NO computed value.
F-B33  the PARITY NOT CERTIFIED banner prints while the flag is unset.
Plus §4.2's prose requirement and §2.2's sequencing rule.
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import brief2 as B2                                                 # noqa: E402
from analytics import levels as L                                   # noqa: E402

DAY_MS = 86_400_000
HOUR_MS = 3_600_000


def _klines(days=420, step_ms=HOUR_MS, seed=3, end_ms=None):
    """A synthetic OHLCV frame long enough to arm every window."""
    n = int(days * DAY_MS / step_ms)
    rng = np.random.default_rng(seed)
    end = end_ms if end_ms is not None else 1_760_000_000_000
    start = ((end - n * step_ms) // step_ms) * step_ms
    t = np.arange(n, dtype="int64") * step_ms + start
    close = 60000 + np.cumsum(rng.normal(0, 40, n))
    high = close + np.abs(rng.normal(0, 25, n))
    low = close - np.abs(rng.normal(0, 25, n))
    open_ = close + rng.normal(0, 12, n)
    vol = np.abs(rng.normal(1000, 180, n))
    return pd.DataFrame({"open_time": t, "open": open_, "high": high,
                         "low": low, "close": close, "volume": vol})


def _bundle(days=420):
    k1h = _klines(days, HOUR_MS)
    end = int(k1h["open_time"].iloc[-1])
    return {"1h": k1h,
            "15m": _klines(min(days, 200), 15 * 60_000, seed=4, end_ms=end),
            "5m": _klines(min(days, 60), 5 * 60_000, seed=5, end_ms=end),
            "1m": _klines(min(days, 12), 60_000, seed=6, end_ms=end)}


# --------------------------------------------------------------- F-B29

def _conf_from(klines, now_ms, price, atr=250.0):
    vol = B2.volume_layer(klines, now_ms)
    rv = B2.rvwap_layer(klines, now_ms)
    nest = B2.nesting_layer(vol, price)
    reg = B2.build_registry({"vwap": {}, "structure": {}, "sessions": {},
                             "radar": []}, vol, rv, nest["levels"])
    return B2.confluence(reg, price, atr), vol, nest


def test_f_b29_every_ratio_recomputes_from_its_own_printed_components():
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    conf, _, _ = _conf_from(k, now, price)
    rr = B2.rr_board(conf, price, 250.0)
    board = rr["board"] + rr["excluded_too_tight"]
    assert board, "no R:R rows produced -- F-B29 would be vacuous"

    for row in board:
        for field in ("entry", "invalidation", "target", "rr", "reward", "risk"):
            assert field in row and row[field] is not None, \
                f"a ratio printed without {field}: {row}"
            assert np.isfinite(row[field]), f"{field} is not finite: {row}"
        assert row["risk"] > 0, "a zero-risk ratio is not a ratio"
        assert row["risk"] == pytest.approx(abs(row["entry"] - row["invalidation"]))
        assert row["reward"] == pytest.approx(abs(row["target"] - row["entry"]))
        assert row["rr"] == pytest.approx(row["reward"] / row["risk"]), \
            "printed R:R does not recompute from its own printed components"


def test_f_b29_no_ratio_without_all_three_components():
    """A row missing any component must not exist at all, rather than print a
    ratio the operator cannot recompute."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    conf, _, _ = _conf_from(k, now, price)
    for view in ("with_volume", "without_volume"):
        v = B2.rr_board(conf, price, 250.0, view=view)
        for row in v["board"] + v["excluded_too_tight"]:
            assert {"entry", "invalidation", "target"} <= set(row)

    # a degenerate cluster (entry == invalidation) yields NO row, not inf
    fake = {"with_volume": {"clusters": [
        {"cluster_id": 0, "mean": 100.0, "member_count": 1, "score": 5,
         "families": ["structure"], "members": [{"level": 100.0}]},
        {"cluster_id": 1, "mean": 90.0, "member_count": 1, "score": 5,
         "families": ["ss"], "members": [{"level": 90.0}]}],
        "lines": {"above": {"mean": 100.0, "score": 5, "families": ["structure"],
                            "members": [{"level": 100.0}], "source": "primary"},
                  "below": None}}}
    out = B2.rr_board(fake, 95.0, 10.0)["board"]
    assert all(np.isfinite(r["rr"]) for r in out)


def test_f_b29_ranking_claims_geometry_not_probability():
    """§7.2 and §11: R:R measures GEOMETRY, not probability."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    conf, _, _ = _conf_from(k, now, price)
    rr = B2.rr_board(conf, price, 250.0)
    assert "structural quality, not probability" in rr["ranking_is"]
    assert rr["contains_no_probability_claim"] is True

    # Scan the ROWS, not the metadata: `ranking_is` and
    # `contains_no_probability_claim` mention probability in order to DENY it,
    # which is the opposite of the defect and must not be flagged.
    rows = rr["board"] + rr["excluded_too_tight"]
    assert rows, "no rows to scan -- the assertion would be vacuous"
    blob = repr(rows).lower()
    # "edge" alone is GEOMETRY vocabulary here -- invalidation_source reads
    # "far edge of the next cluster". Ban the PREDICTIVE senses explicitly
    # rather than the word, or the fixture flags the geometry it exists to
    # protect. Same class as "not probability" in the metadata.
    for banned in ("probability", "likely", "expected value", "win rate",
                   "forecast", "predict", "has edge", "an edge", "our edge",
                   "trading edge"):
        assert banned not in blob, f"predictive language in an R:R row: {banned}"
    import re as _re
    for m in _re.finditer(r"edge", blob):
        ctx = blob[max(0, m.start() - 12):m.start()]
        assert ctx.endswith(("far ", "cluster ", "facing ", "near ")),             f"'edge' used outside geometry vocabulary: ...{blob[max(0,m.start()-30):m.start()+20]}..."


def test_f_b29_drafts_carry_no_sizing():
    """§7.1: NO SIZING, EVER."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    conf, _, _ = _conf_from(k, now, price)
    drafts = B2.hypothesis_drafts(conf, price)
    assert drafts, "no drafts produced -- the assertion would be vacuous"
    for d in drafts:
        assert d["draft"] is True and d["no_sizing"] is True
        assert {"if", "then", "invalidated_if"} <= set(d)
        blob = repr(d).lower()
        for banned in ("size", "risk %", "leverage", "contracts", "position size",
                       "% of account", "notional"):
            assert banned not in blob, f"sizing language in a draft: {banned}"


# --------------------------------------------------------------- F-B34

def _tight_conf(entry=100.0, far=100.5, opposite=50.0, score=7):
    """A cluster whose far edge is a hair from its mean -- the R-1 shape.

    Geometry: price sits BELOW `entry`, so the line is genuinely 'above', and the
    opposing cluster sits below `entry` so it can serve as a target.
    """
    return {"with_volume": {
        "clusters": [
            {"cluster_id": 0, "mean": entry, "member_count": 2, "score": score,
             "families": ["structure", "ss"],
             "members": [{"level": entry}, {"level": far}]},
            {"cluster_id": 1, "mean": opposite, "member_count": 2, "score": score,
             "families": ["structure", "ss"],
             "members": [{"level": opposite}, {"level": opposite + 1}]}],
        "lines": {
            "above": {"mean": entry, "score": score,
                      "families": ["structure", "ss"],
                      "members": [{"level": entry}, {"level": far}],
                      "source": "primary"},
            "below": None}}}


def test_f_b34_tight_invalidation_is_CHIPPED_not_excluded():
    """R-1 DEMOTED (ruling D2-2). The §7.2 fix made a knife-edge stop
    geometrically impossible, and measured inval_atr spanned only 0.03 ATR, so
    excluding on it was an arbitrary cut wearing the appearance of a principle.
    A tight stop now carries a CAUTION CHIP and stays on the ranked board."""
    atr = 100.0
    # a cluster just BEYOND the entry, so the invalidation is genuinely tight
    # (0.21 ATR) rather than absent -- absence is C.3's path, tested separately.
    conf = _tight_conf()
    conf["with_volume"]["clusters"].append(
        {"cluster_id": 2, "mean": 120.0, "member_count": 2, "score": 6,
         "families": ["structure", "ss"],
         "members": [{"level": 120.0}, {"level": 121.0}]})
    rr = B2.rr_board(conf, 90.0, atr)
    assert rr["min_inval_atr"] == B2.MIN_INVAL_ATR == 0.25
    assert rr["excluded_too_tight"] == [], "the floor is no longer an exclusion gate"
    assert rr["board"], "a tight row must still be RANKED, carrying a chip"
    for row in rr["board"]:
        assert row["rankable"] is True
        if row["inval_atr"] < B2.MIN_INVAL_ATR:
            assert row["caution"] is True
            assert "caution" in row["flag"]
    assert "CAUTION CHIP" in rr["why_a_floor"] or "caution chip" in rr["why_a_floor"].lower()


def test_f_b34_invalidation_is_structure_derived_not_width_derived():
    """C.2: invalidation is the far edge of the NEXT CLUSTER beyond the entry
    cluster. Dense structure gives a tight stop, a void gives a wide one, and
    both are true information -- which a width-derived stop could not express."""
    atr = 100.0
    conf = _tight_conf(entry=100.0, far=100.5, opposite=50.0)
    conf["with_volume"]["clusters"].append(
        {"cluster_id": 2, "mean": 130.0, "member_count": 2, "score": 6,
         "families": ["structure", "ss"],
         "members": [{"level": 129.0}, {"level": 131.0}]})
    rr = B2.rr_board(conf, 90.0, atr)
    assert rr["board"]
    row = rr["board"][0]
    # the next cluster beyond 100 is the one at 130; its far edge is 131
    assert row["invalidation"] == pytest.approx(131.0),         "invalidation must be the next cluster's far edge, not a width multiple"
    assert "next cluster" in row["invalidation_source"]
    assert "structure" in rr["invalidation_rule"]

    # a draft must agree with its ranked row about where the level failed
    d = B2.hypothesis_drafts(conf, 90.0, atr_d=atr)
    assert d[0]["inval_atr"] == pytest.approx(row["inval_atr"])


def test_f_b34_no_structure_beyond_means_no_rr_not_a_fabricated_stop():
    """C.3: never invent a stop to complete a ratio."""
    atr = 100.0
    lonely = {"with_volume": {
        "clusters": [{"cluster_id": 0, "mean": 100.0, "member_count": 2, "score": 7,
                      "families": ["structure", "ss"],
                      "members": [{"level": 100.0}, {"level": 100.5}]},
                     {"cluster_id": 1, "mean": 50.0, "member_count": 2, "score": 7,
                      "families": ["structure", "ss"],
                      "members": [{"level": 50.0}, {"level": 51.0}]}],
        "lines": {"above": {"mean": 100.0, "score": 7,
                            "families": ["structure", "ss"],
                            "members": [{"level": 100.0}, {"level": 100.5}],
                            "source": "primary"}, "below": None}}}
    rr = B2.rr_board(lonely, 90.0, atr)
    assert rr["board"] == [], "no structure beyond -> no ranked row"
    assert rr["no_rr"], "the draft must be reported, with a reason"
    n = rr["no_rr"][0]
    assert n["rr"] is None and n["invalidation"] is None
    assert "no cluster beyond" in n["reason"]
    assert "fabricated" in n["reason"]


def test_f_b34_inval_atr_is_printed_on_every_row():
    """C.1: the reader must see the stop distance in ATR terms."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    conf, _, _ = _conf_from(k, now, price)
    rr = B2.rr_board(conf, price, 250.0)
    rows = rr["board"] + rr["excluded_too_tight"]
    assert rows, "no rows at all -- the assertion would be vacuous"
    for row in rows:
        assert "inval_atr" in row and row["inval_atr"] is not None
        assert row["inval_atr"] == pytest.approx(row["risk"] / 250.0)


def test_f_b34_floor_is_declared_a_placeholder():
    """C.4: re-ratified from the calibration distribution, not defended."""
    rr = B2.rr_board(_tight_conf(), 90.0, 100.0)
    assert "placeholder" in rr["min_inval_atr_is"]
    assert "calibration" in rr["min_inval_atr_is"]


# --------------------------------------------------------------- F-B31

def test_f_b31_forming_candle_is_drawn_but_in_no_computed_value():
    """§3.5: the forming candle is DRAWN and GREYED; every computed number uses
    closed candles only.  Mid-week, the weekly RSI is last week's."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    vol = B2.volume_layer(k, now)
    planes = B2.chart_planes(k, vol)

    weekly = planes["planes"]["1W"]["forming"]
    assert weekly["draw_only"] is True
    if not weekly.get("available"):
        pytest.skip("the fixture span ended exactly on a week boundary")
    assert weekly["greyed"] is True and weekly["label"] == "forming"
    assert weekly["excluded_from_computation"] is True

    # the forming bar's own numbers must appear in NO computed layer
    osc = B2.oscillator_layer(k)
    wk = osc["timeframes"].get("1w") or {}
    assert wk, "no weekly oscillator computed -- the assertion would be vacuous"
    assert wk["last_bar_utc_ms"] < weekly["open_time_ms"], (
        "a computed weekly value is stamped at or after the forming bar -- the "
        "forming candle reached a computed number")

    forming_values = {round(weekly[k_], 6) for k_ in ("open", "high", "low", "close")
                      if weekly.get(k_) is not None}
    computed = {round(v, 6) for v in
                (wk.get("rsi"), wk.get("macd"), wk.get("ao"), wk.get("macd_hist"))
                if v is not None}
    assert not (forming_values & computed)


def test_f_b31_closed_resample_never_includes_the_forming_bucket():
    """The computed path routes through analytics.resample_ohlcv, which emits
    only buckets PROVED closed -- so this holds by construction, not by luck."""
    k = _bundle()
    t = k["1h"]["open_time"].to_numpy().astype("int64")
    got = B2._resampled(k, "1w")
    assert got is not None
    wt = got[0]
    last_closed_end = int(wt[-1]) + 7 * DAY_MS
    assert last_closed_end <= int(t[-1]) + HOUR_MS, (
        "the last emitted weekly bucket extends past the data that proves it closed")


def test_f_b31_1m_plane_carries_no_oscillator():
    """§6.1: a closed-bar monthly oscillator in late July is June's number."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    planes = B2.chart_planes(k, B2.volume_layer(k, now))
    assert planes["planes"]["1M"]["oscillators"] is None
    assert "1M" not in B2.OSC_TFS


# --------------------------------------------------------------- F-B33

def test_f_b33_parity_banner_is_present_while_uncertified():
    """Until the operator's parity readings are returned and matched, EVERY
    render prints the banner.  Build and trust are separate gates."""
    assert "PARITY NOT CERTIFIED" in B2.PARITY_BANNER
    assert "not yet adopted" in B2.PARITY_BANNER
    doc = B2.capture_envelope("2026-08-03", "ny_am", parity_certified=False)
    assert doc["parity_certified"] is False
    assert doc["banner"] == B2.PARITY_BANNER
    assert "PARITY NOT CERTIFIED" in doc["banner"]


def test_f_b33_banner_clears_only_when_the_flag_is_set():
    """ANTI-VACUITY: the banner must be a function of the flag, not a constant."""
    on = B2.capture_envelope("2026-08-03", "ny_am", parity_certified=True)
    assert on["parity_certified"] is True
    assert on.get("banner") in (None, ""), \
        "the banner must clear once parity is certified, or it asserts nothing"


def test_f_b33_rules_version_is_2_0_0():
    """§8.1 ratified A-6: the closed-bar correction plus the volume filter move
    published numbers, and archive-comparability law requires a major bump."""
    import analytics
    doc = B2.capture_envelope("2026-08-03", "london")
    assert doc["rules_version"] == "2.0.0"
    assert doc["slot"] == "london"
    # Read from the package, never pinned to a literal: analytics is versioned
    # independently of rules_version, and a defect fix that moves a number is
    # REQUIRED to bump it (I-F). A hardcoded literal here turns every honest
    # bump into a spurious failure.
    assert doc["analytics_version"] == analytics.ANALYTICS_VERSION
    assert len(doc["analytics_sha"]) == 64


# --------------------------------------------------- §4.2 prose requirement

def test_prose_is_emitted_for_every_pair_and_names_disjoint_gaps():
    """§4.2: when disjoint, the report states it IN WORDS, naming the gap and
    both facing edges.  A table alone does not satisfy §4."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    vol = B2.volume_layer(k, now)
    nest = B2.nesting_layer(vol, price)

    assert len(nest["prose"]) == 3, "one sentence per adjacent pair"
    assert len(nest["pairs"]) == 3
    for key, pair in nest["pairs"].items():
        assert pair["state"] in (None,) + L.__dict__.get("_", ()) or \
            pair["state"] in ("nested_inside", "nested_outside", "overlapping",
                              "disjoint_above", "disjoint_below")

    # a constructed disjoint pair must produce the required sentence shape
    from analytics import nesting as N
    text = N.describe_nesting(("7d", "30d"), N.va_nesting(64250, 66000, 61000, 63100))
    assert "unclaimed gap" in text and "facing edges" in text


# --------------------------------------------------- §2.2 sequencing rule

def test_part_two_is_built_only_from_printed_part_one_numbers():
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    a = {"vwap": {}, "structure": {}, "sessions": {}, "radar": [],
         "governor": {}, "funding": {}, "volatility": {}}
    part1, part2 = B2.brief2_asset(a, k, now, price, 250.0)

    assert set(part1) >= {"volume_windows", "rvwap", "va_nesting", "oscillators",
                          "cross_state", "lattice_12_25", "chart_planes",
                          "confluence"}
    assert set(part2) >= {"confluence_area_map", "lines_in_sand", "lines_differ",
                          "hypothesis_drafts", "rr_ranking", "composite_bias"}
    assert "no hidden inputs" in part2["sequencing_rule"]

    # every area-map mean must exist as a cluster mean in Part I's confluence
    for view, rows in part2["confluence_area_map"].items():
        means = {round(c["mean"], 8)
                 for c in part1["confluence"][view]["clusters"]}
        for r in rows:
            assert round(r["mean"], 8) in means, \
                "Part II names an area Part I never printed"


def test_composite_bias_is_counted_and_names_dissent():
    """§7.3: 'N of 5 agree, dissenting: <names>', equal weights, never fitted."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    a = {"vwap": {}, "structure": {}, "sessions": {}, "radar": [],
         "governor": {"1h": {"direction": "long"}, "4h": {"direction": "long"},
                      "12h": {"direction": "short"}},
         "funding": {"percentile": 95.0}, "volatility": {"compression_flag": False}}
    _, part2 = B2.brief2_asset(a, k, now, price, 250.0)
    cb = part2["composite_bias"]

    assert set(cb["votes"]) == {"trend", "momentum", "location",
                                "volume_location", "crowding"}
    assert all(v in (-1, 0, 1) for v in cb["votes"].values()), \
        "a vote that is not in {-1,0,+1} is a weight"
    assert cb["of"] == 5 and "agree" in cb["print"]
    assert cb["votes"]["trend"] == 1, "2 long vs 1 short is a long majority"
    assert cb["votes"]["crowding"] == -1, "funding p95 votes against"
    assert cb["band"] in ["Short", "Lean-short", "Neutral-mixed",
                          "Lean-long", "Long"]
    assert "never fitted" in cb["weights"]

    # Dissent is asserted as an INVARIANT, not as a specific family: which side
    # wins depends on the data, and pinning the winner would make this a test of
    # the fixture's randomness rather than of the counting rule.
    total = sum(cb["votes"].values())
    majority = 1 if total > 0 else (-1 if total < 0 else 0)
    expected = sorted(k for k, v in cb["votes"].items()
                      if v != majority and v != 0)
    assert cb["dissenting"] == expected, "dissent must name exactly the minority"
    assert cb["agree"] == sum(1 for v in cb["votes"].values()
                              if v == majority and v != 0)
    assert all(f in cb["votes"] for f in cb["dissenting"])
    # abstentions (0) are never dissent -- they declared no side
    assert not any(cb["votes"][f] == 0 for f in cb["dissenting"])
    if cb["dissenting"]:
        assert f"dissenting: {', '.join(cb['dissenting'])}" in cb["print"]
    else:
        assert "no dissent" in cb["print"]
    assert cb["disagreement_chip"] is bool(cb["dissenting"])


def test_compression_demotes_one_band_toward_neutral_without_reweighting():
    """§7.3: the compression flag demotes the band one step; it does NOT
    half-weight votes, which would contradict count-based purity."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    base = {"vwap": {}, "structure": {}, "sessions": {}, "radar": [],
            "governor": {l: {"direction": "long"} for l in ("1h", "4h", "12h")},
            "funding": {"percentile": 5.0}}
    plain = B2.brief2_asset({**base, "volatility": {"compression_flag": False}},
                            k, now, price, 250.0)[1]["composite_bias"]
    comp = B2.brief2_asset({**base, "volatility": {"compression_flag": True}},
                           k, now, price, 250.0)[1]["composite_bias"]

    assert plain["votes"] == comp["votes"], \
        "compression changed a VOTE -- it may only demote the final band"
    assert comp["compression_demoted"] is True
    bands = ["Short", "Lean-short", "Neutral-mixed", "Lean-long", "Long"]
    assert abs(bands.index(comp["band"]) - bands.index(plain["band"])) <= 1
    if plain["band"] != "Neutral-mixed":
        assert abs(bands.index(comp["band"]) - 2) < abs(bands.index(plain["band"]) - 2)


def test_lattice_and_cross_state_are_display_only():
    """§3.7 and §6.2: no signal, no vote, no score contribution."""
    k = _bundle()
    lat = B2.lattice_layer(k)
    assert lat["display_only"] and lat["no_vote"] and lat["no_score"]
    cross = B2.cross_state_layer(k, 250.0)
    assert cross["display_only"] is True
    assert set(cross["census_candidates"]) == {"H-RVX", "H-M1X"}

    # neither may reach the confluence registry
    now = int(k["1h"]["open_time"].iloc[-1])
    price = float(k["1h"]["close"].iloc[-1])
    vol = B2.volume_layer(k, now)
    rv = B2.rvwap_layer(k, now)
    nest = B2.nesting_layer(vol, price)
    reg = B2.build_registry({"vwap": {}, "structure": {}, "sessions": {},
                             "radar": []}, vol, rv, nest["levels"])
    labels = " ".join(x["label"] for x in reg.as_list()).lower()
    assert "ema12" not in labels and "ema25" not in labels, \
        "the {12,25} lattice leaked into the scoring registry"


def test_substrate_actually_used_is_recorded_per_window():
    """§3.3: the substrate actually used must be printed in every capture."""
    k = _bundle()
    now = int(k["1h"]["open_time"].iloc[-1])
    vol = B2.volume_layer(k, now)
    assert vol["substrate_used"]["7d"] == "1m"
    assert vol["substrate_used"]["30d"] == "5m"
    assert vol["substrate_used"]["90d"] == "15m"
    assert vol["rows"] == 120 and vol["value_area"] == 0.70
    assert vol["retired_windows"] == ["5d", "20d"]

    # a missing tier must be DISCLOSED, never silently substituted
    thin = {"1h": k["1h"]}
    v2 = B2.volume_layer(thin, now)
    assert "substrate_substitutions" in v2
    assert v2["substrate_substitutions"]["7d"]["wanted"] == "1m"
    assert v2["substrate_substitutions"]["7d"]["used"] == "1h"
