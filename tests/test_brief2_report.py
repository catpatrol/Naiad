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


# ------------------------------------------- F-B36 stretch + band excursions

def test_f_b36_worked_example_from_the_operators_capture():
    """D.5, the operator's own numbers at price 63,522.7.

    Month VWAP 63,112.3 sigma 319.9   -> +1.28 sigma
    RVWAP365   83,686.7 sigma 18,868.6 -> -1.07 sigma

    Price is simultaneously ABOVE the monthly sigma-1 upper and BELOW the yearly
    sigma-1 lower: overextended up against the month and down against the year,
    both true at the same instant. That is the object of interest, not a
    contradiction.
    """
    px, atr = 63522.7, 1649.58
    m = B2._stretch_row("anchored M", "anchored", 63112.3, 319.9, px, atr, bars=69)
    y = B2._stretch_row("RVWAP 365d", "rolling", 83686.7, 18868.6, px, atr)

    assert m["sigma_position"] == pytest.approx(1.28, abs=0.005)
    assert y["sigma_position"] == pytest.approx(-1.07, abs=0.005)
    assert m["band_reached"] == 1, "price is past the monthly +1 sigma"
    assert y["band_reached"] == -1, "price is past the yearly -1 sigma"
    assert m["thin_sample"] is False and 69 >= B2.THIN_SAMPLE_BARS

    # the three units answer different questions and must all be present
    for r in (m, y):
        assert r["sigma_position"] is not None
        assert r["bps"] is not None and r["atr"] is not None


def test_f_b36_multiscale_disagreement_is_recorded():
    """D.5.1 -- max and min sigma-position, and WHICH TWO disagree most."""
    a = {"vwap": {"anchored": {
        "M": {"vwap": 63112.3, "sigma": 319.9, "bars": 69},
        "W": {"vwap": None, "sigma": None, "bars": 0}}}}
    rv = {"windows": {"365d": {"warming": False, "vwap": 83686.7, "stdev": 18868.6},
                      "7d": {"warming": True}}}
    st = B2.stretch_layer(a, rv, {}, 63522.7, 1649.58)

    d = st["disagreement"]
    assert d["max"]["name"] == "anchored M"
    assert d["min"]["name"] == "RVWAP 365d"
    assert d["spread_sigma"] == pytest.approx(1.28 + 1.07, abs=0.01)
    assert d["straddles_one_sigma"] is True, \
        "above one +1 sigma AND below another -1 sigma must be flagged"
    assert set(d["most_disagreeing_pair"]) == {"anchored M", "RVWAP 365d"}

    # warming entries are carried but contribute no sigma position
    warm = [r for r in st["rows"] if r["warming"]]
    assert warm, "warming anchors/windows must still appear, not vanish"
    assert all(r["sigma_position"] is None for r in warm)
    assert st["n_live"] == 2


def test_f_b36_thin_sample_is_flagged_not_suppressed():
    """A sigma over 2 bars is the spread between two numbers -- arithmetically
    exact, informationally empty. It is FLAGGED, not silently trusted."""
    thin = B2._stretch_row("anchored M", "anchored", 63112.3, 319.9,
                           63522.7, 1649.58, bars=2)
    assert thin["thin_sample"] is True
    assert thin["sigma_position"] is not None, "flagged, not suppressed"
    assert B2.THIN_SAMPLE_BARS == 30


def test_f_b36_zero_and_missing_sigma_never_divide():
    for sig in (0.0, None):
        r = B2._stretch_row("x", "anchored", 100.0, sig, 110.0, 10.0, bars=50)
        assert r["sigma_position"] is None
        assert r["bps"] is not None, "bps does not need sigma and must survive"
    warm = B2._stretch_row("x", "anchored", None, None, 110.0, 10.0, warming=True)
    assert warm["sigma_position"] is None and warm["bps"] is None


def test_f_b36_excursions_record_and_claim_nothing():
    """D.6 -- recording is OPS; whether a touch pays is census work."""
    a = {"vwap": {"anchored": {"M": {"vwap": 63112.3, "sigma": 319.9, "bars": 69}}}}
    rv = {"windows": {"365d": {"warming": False, "vwap": 83686.7, "stdev": 18868.6}}}
    st = B2.stretch_layer(a, rv, {}, 63522.7, 1649.58)
    ex = B2.excursion_layer(st, 1649.58)

    assert len(ex["events"]) == 2
    by = {e["name"]: e for e in ex["events"]}
    assert by["anchored M"]["side"] == "above" and by["anchored M"]["band_reached"] == 1
    assert by["RVWAP 365d"]["side"] == "below"
    for e in ex["events"]:
        assert e["recording_only"] is True
        assert e["distance_to_mean_sigma"] > 0
        assert e["distance_to_mean_atr"] is not None
    assert ex["census_candidate"] == "H-VBR"

    # Scan the EVENTS, not the metadata. `claims_nothing` and `census_candidate`
    # mention paying and expectancy in order to DENY them -- the fourth time this
    # project has hit the same false positive (F-F3's prohibition text, F-B29's
    # "not probability", F-B35's quoted `n=3`). The rule that keeps emerging:
    # scan the DATA a layer emits, never the prose that disclaims it.
    blob = repr(ex["events"]).lower()
    for banned in ("expectancy", "probability", "likely", "edge", "pays",
                   "win_rate", "forecast", "predict"):
        assert banned not in blob, f"predictive language in an excursion EVENT: {banned}"

    # and the disclaimers must actually be there
    assert "census work under g-7" in ex["claims_nothing"].lower()
    assert "derived" in ex["since_last_touch"].lower()
    assert "captures alone" in ex["since_last_touch"]


def test_f_b36_no_touch_means_no_event():
    """ANTI-VACUITY: an event list that fires on everything records nothing."""
    a = {"vwap": {"anchored": {"M": {"vwap": 63112.3, "sigma": 319.9, "bars": 69}}}}
    st = B2.stretch_layer(a, {"windows": {}}, {}, 63150.0, 1649.58)   # +0.12 sigma
    ex = B2.excursion_layer(st, 1649.58)
    assert ex["events"] == [], "price inside sigma-1 must produce no excursion"
    assert ex["n_live_vwaps"] == 1


# ------------------------------- F-B38  stage 3.4 EXCURSION FIREWALL
#
# The line the operator drew: RECORDING band-excursion events is market-state
# observation and is OPS. AGGREGATING them -- "band touches revert N% of the
# time", hit rates, expectancy, any statistic over the event HISTORY -- is the
# answer to his thesis and is CENSUS work under G-7. Same line as the trade
# diary: recording is diary-keeping, aggregating is a statistic.

def _code_only(path):
    """Source with docstrings and comments removed -- scan CODE, never prose.

    This project has now hit the same false positive six times (F-F3's
    prohibition text, F-B29's "not probability", F-B35's quoted n=3, F-B36's
    claims_nothing, cycle 4's stoch_rsi_k). The excursion layer's own
    docstrings QUOTE the prohibition they enforce. The standing rule, written
    into the fixtures: scan what the code DOES, never what it mentions, and
    never the prose that disclaims a thing.
    """
    import ast
    import io
    import tokenize

    src = Path(path).read_text(encoding="utf-8")
    toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline)
            if t.type != tokenize.COMMENT]
    tree = ast.parse(tokenize.untokenize(toks))
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body[0].value.value = ""
    return ast.unparse(tree).lower()


def _func_code(fn):
    """Just one function's body, prose stripped."""
    import ast
    import inspect
    import textwrap
    tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if (node.body and isinstance(node.body[0], ast.Expr)
                    and isinstance(node.body[0].value, ast.Constant)
                    and isinstance(node.body[0].value.value, str)):
                node.body[0].value.value = ""
    return ast.unparse(tree).lower()


# Statistics over OUTCOMES. Deliberately does NOT ban groupby/idxmax: selecting
# the most recent touch is a LOOKUP, not a statistic, and stage 3.3 explicitly
# commissions "captures since the last touch".
BANNED_EXCURSION_STATS = (
    "expectancy", "win_rate", "winrate", "hit_rate", "hitrate", "revert_rate",
    "reversion_rate", "success", "profit", "pnl", "r_multiple", "sharpe",
    "drawdown", "probability", "frequency", "np.mean", "np.std", "np.median",
    "mean(", "median(", "average(", "describe(", "value_counts", "pct_",
    "ratio_of", "how_often",
)


def test_f_b38_no_aggregation_is_applied_to_the_excursion_event_history():
    """Stage 3.4 -- the firewall, enforced on CODE rather than promised in prose."""
    code = _func_code(B2.excursion_layer)
    for token in BANNED_EXCURSION_STATS:
        assert token not in code, (
            f"excursion_layer CODE contains {token!r} -- aggregating the event "
            f"history is H-VBR, census work under G-7, not OPS")

    # ANTI-VACUITY: the stripper must not have eaten the code with the prose.
    assert "events.append" in code and "band_reached" in code

    # And the prohibition must still be STATED in the prose it was stripped from.
    import inspect
    assert "census work under g-7" in inspect.getsource(B2.excursion_layer).lower()


def test_f_b38_panel_derivation_counts_recency_and_computes_no_rate():
    """since_last_touch may say WHEN a band was last touched, never HOW OFTEN
    a touch works. The first is a diary fact; the second answers the thesis."""
    import brief_panel as BP

    code = _func_code(BP.since_last_touch)
    for token in BANNED_EXCURSION_STATS:
        assert token not in code, (
            f"since_last_touch CODE contains {token!r} -- that is a statistic "
            f"over the event history, not a recency counter")

    # It must actually derive recency, or the fixture guards nothing.
    assert "captures_since_last_touch" in code and "idxmax" in code

    # The stored table carries per-capture OBSERVATIONS only: no column may be
    # derived from other captures, or the partition stops rebuilding from
    # captures alone (F-B19/F-B32).
    rowcode = _func_code(BP.excursion_rows)
    for token in ("since_last_touch", "captures_since", "streak", "count_of"):
        assert token not in rowcode, (
            f"excursion_rows stores {token!r} -- a cross-capture derivation in "
            f"a write-once partition breaks rebuildable-from-captures-alone")


def test_f_b38_excursion_partition_is_a_table_and_round_trips():
    """The table promised by D.6 exists and carries the event grain."""
    import brief_panel as BP
    assert "excursions" in BP.TABLES, \
        "the excursions table was documented for a cycle and never built"

    doc = {"date": "2026-08-05", "slot": "post_ny", "assets": {"BTCUSDT": {
        "band_excursions": {"events": [
            {"name": "RVWAP 7d", "kind": "rolling", "side": "above",
             "band_reached": 1, "sigma_position": 1.51,
             "distance_to_mean_sigma": 1.51, "distance_to_mean_atr": 0.61,
             "bars": 168, "thin_sample": False, "returned_to_mean": False}]}}}}
    rows = BP.excursion_rows(doc)
    assert len(rows) == 1
    r = rows[0]
    assert (r["asset"], r["name"], r["side"], r["band_reached"]) == \
           ("BTCUSDT", "RVWAP 7d", "above", 1)
    assert r["date"] == "2026-08-05" and r["slot"] == "post_ny"

    # ANTI-VACUITY: no events -> no rows, so the table cannot fire on everything.
    empty = {"date": "2026-08-05", "slot": "post_ny",
             "assets": {"BTCUSDT": {"band_excursions": {"events": []}}}}
    assert BP.excursion_rows(empty) == []


# ------------------------------- F-B39  stage 3.1 stretch, LIVE capture numbers

def test_f_b39_stretch_reproduces_the_2026_08_05_ruled_substrate_capture():
    """Stage 3.1 -- the operator's worked example on the 1h parity bar.

    Price 64,733.6 at 2026-08-05T17:00Z against the four rolling means, all of
    which passed parity on the ruled 1h substrate the same run:

        RVWAP   7d  63,737.7323  sigma    658.9130  ->  +1.51
        RVWAP  30d  64,026.4740  sigma  1,014.3754  ->  +0.70
        RVWAP  90d  66,248.8393  sigma  6,288.7101  ->  -0.24
        RVWAP 365d  83,430.7716  sigma 18,858.6356  ->  -0.99

    Price is ABOVE the 7d sigma-1 upper: a LIVE excursion, which is what makes
    this capture the right one to pin the fixture to.
    """
    px, atr = 64733.6, 1628.44005908
    want = {"7d": 1.51, "30d": 0.70, "90d": -0.24, "365d": -0.99}
    means = {"7d": (63737.732321, 658.9130), "30d": (64026.474, 1014.3754),
             "90d": (66248.839326, 6288.7101), "365d": (83430.771601, 18858.6356)}

    for w, (mean, sigma) in means.items():
        r = B2._stretch_row(f"RVWAP {w}", "rolling", mean, sigma, px, atr)
        assert r["sigma_position"] == pytest.approx(want[w], abs=0.005), w
        # all three units answer different questions and must all be present
        assert r["bps"] is not None and r["atr"] is not None

    seven = B2._stretch_row("RVWAP 7d", "rolling", means["7d"][0],
                            means["7d"][1], px, atr)
    assert seven["band_reached"] == 1, \
        "price above the 7d +1 sigma must register a live excursion"

    # NON-MONOTONIC ACROSS SCALES, and that is the information: stretched UP
    # against the week, pulled DOWN against the year, at the same instant.
    rv = {"windows": {w: {"warming": False, "vwap": m, "stdev": s}
                      for w, (m, s) in means.items()}}
    st = B2.stretch_layer({"vwap": {}}, rv, {}, px, atr)
    d = st["disagreement"]
    assert d["max"]["name"] == "RVWAP 7d" and d["min"]["name"] == "RVWAP 365d"
    assert d["spread_sigma"] == pytest.approx(1.51 + 0.99, abs=0.02)


# ------------------------------- F-B40  stage 3.5 RVOL (ruling B-7)

def test_f_b40_rvol_compares_like_with_like_and_excludes_itself():
    """RVOL is current volume against the trailing 20-day SAME-TIME-OF-DAY mean.

    The time-of-day bucket is the whole point. Crypto volume has a hard diurnal
    shape, so a flat 20-day mean scores every US-open bar high and every Asian
    bar low -- a clock reading, not a market reading.
    """
    from analytics import profile as P

    # 40 days of hourly bars. Volume depends ONLY on hour-of-day, so a
    # like-for-like comparison must return exactly 1.0 and a flat-mean
    # comparison cannot.
    n = 40 * 24
    t = np.arange(n, dtype="int64") * HOUR_MS
    hour = (t // HOUR_MS) % 24
    v = np.where(hour == 13, 1000.0, 100.0)          # one loud hour a day

    at_13 = int(np.flatnonzero(hour == 13)[-1])
    r = P.relative_volume(t, v, as_of_index=at_13)
    assert r["rvol"] == pytest.approx(1.0), \
        "a US-open bar of typical US-open size must read 1.0, not 10.0"
    assert r["samples"] == P.RVOL_LOOKBACK_DAYS and r["warming"] is False
    assert r["average_volume"] == pytest.approx(1000.0)

    at_03 = int(np.flatnonzero(hour == 3)[-1])
    assert P.relative_volume(t, v, as_of_index=at_03)["rvol"] == pytest.approx(1.0)

    # A GENUINE spike is still caught: same hour, ten times the usual size.
    v2 = v.copy()
    v2[at_13] = 10000.0
    assert P.relative_volume(t, v2, as_of_index=at_13)["rvol"] == pytest.approx(10.0)

    # SELF-EXCLUSION: the current bar must not enter its own baseline, or every
    # reading is dragged toward 1.0 exactly when the measure matters most.
    assert P.relative_volume(t, v2, as_of_index=at_13)["average_volume"] == \
        pytest.approx(1000.0), "the spike leaked into its own baseline"

    # WARMING is honest rather than silently thin.
    early = P.relative_volume(t, v, as_of_index=int(np.flatnonzero(hour == 13)[2]))
    assert early["warming"] is True and early["samples"] == 2

    # A zero baseline reports None, never inf -- inf would rank first on any
    # board that sorts by RVOL.
    z = P.relative_volume(t, np.zeros(n), as_of_index=at_13)
    assert z["rvol"] is None and z["average_volume"] == 0.0


def test_f_b40_rvol_layer_is_observation_only_and_casts_no_vote():
    """B-7 commissions RVOL as CONTEXT. It describes participation, not price,
    so it contributes no level and must never reach the scoring registry."""
    kl = _klines(days=40, step_ms=HOUR_MS)
    lay = B2.rvol_layer(kl)
    assert lay["observation_only"] is True
    assert lay["tf"] == "1h" and lay["lookback_days"] == 20

    # It must not have leaked into the registry under any label.
    reg = B2.build_registry({"vwap": {}, "structure": {}, "sessions": {},
                             "radar": []},
                            {"windows": {}}, {"windows": {}}, [])
    labels = " ".join(x["label"] for x in reg.as_list()).lower()
    assert "rvol" not in labels and "relative volume" not in labels, \
        "RVOL reached the scoring registry -- it locates no price"


# ------------------- F-B38d  cycle 5 item 4.3 -- the EPISODE view is covered
#
# The firewall does not get a new boundary because a new view exists. Locating
# and measuring runs beyond a band is market-state observation and is OPS.
# Computing what fraction of them RETURN to the mean -- or any hit count or
# expectancy over the run history -- is H-VBR, census work under G-7.

def test_f_b38_episode_view_computes_no_statistic_over_outcomes():
    """Stage 3.4's firewall, extended to cover C5's episode view."""
    import brief_panel as BP

    code = _func_code(BP.episode_runs)
    for token in BANNED_EXCURSION_STATS:
        assert token not in code, (
            f"episode_runs CODE contains {token!r} -- a statistic over the run "
            f"history is H-VBR, census work under G-7, not OPS")

    # It must genuinely locate runs, or the scan guards nothing.
    assert "length_bars" in code and "max_abs_z" in code

    # The prohibition must still be STATED in the prose the scan strips.
    # Whitespace-normalised: the phrase legitimately wraps across lines, and a
    # fixture that breaks on a line break tests formatting, not content.
    import inspect
    import re as _re
    doc = _re.sub(r"\s+", " ", inspect.getsource(BP.episode_runs).lower())
    assert "census work under g-7" in doc and "h-vbr" in doc

    # And it must NOT look at what happened after a run ended -- no forward
    # index, no return-to-mean flag, no outcome column of any kind.
    for token in ("returned", "revert", "after", "outcome", "target", "exit"):
        assert token not in code, \
            f"episode_runs CODE mentions {token!r} -- it may not look past the run"


def test_f_b38_episode_runs_is_correct_on_hand_built_geometry():
    """ANTI-VACUITY for the scan above: the function must actually work, or a
    firewall test over a broken primitive proves nothing."""
    import brief_panel as BP

    # two runs beyond 2: indices 1-3 (len 3) and 6-6 (len 1)
    z = [0.0, 2.5, 3.1, 2.0, 1.9, 0.5, -2.2, 0.0]
    eps = BP.episode_runs(z, 2)
    assert len(eps) == 2
    assert eps[0] == {"start_index": 1, "length_bars": 3, "max_abs_z": 3.1}
    assert eps[1] == {"start_index": 6, "length_bars": 1, "max_abs_z": 2.2}

    # SIGN-BLIND: a run below -k is an excursion just as one above +k is.
    assert BP.episode_runs([-2.5, -2.6], 2)[0]["length_bars"] == 2

    # the boundary is INCLUSIVE, matching |z| >= k
    assert len(BP.episode_runs([2.0], 2)) == 1
    assert BP.episode_runs([1.999], 2) == []

    # a series never beyond the band yields NO episodes -- it cannot fire on
    # everything.
    assert BP.episode_runs([0.0, 1.0, -1.5, 0.2], 2) == []

    # a run open at the END of the series is still closed and counted, not
    # silently dropped for lacking a return.
    tail = BP.episode_runs([0.0, 2.1, 2.2], 2)
    assert len(tail) == 1 and tail[0]["length_bars"] == 2


def test_f_b38_the_c4_normal_comparison_is_gone_from_the_interface():
    """C5 item 4.1 -- the category error must be REMOVED, not merely annotated.

    Price relative to a VWAP is a persistent, autocorrelated series; comparing
    its time-fractions to a normal distribution's independent-draw tail
    probabilities licenses a conclusion about tail fatness that does not follow.
    """
    iface = (ROOT / "analytics" / "INTERFACE.md").read_text(encoding="utf-8")
    low = iface.lower()
    for banned in ("31.7", "roughly double", "wrong by a factor of two"):
        assert banned not in low, (
            f"INTERFACE.md still carries the withdrawn normal-distribution "
            f"comparison ({banned!r}) -- C5 item 4.1 removes it")

    # and the replacement framing must be present, or the removal left a hole
    assert "episode" in low and "autocorrelated" in low


# ============================== F-B46  cycle 6 item 4 -- CERTIFICATION FLIP
#
# F-B33 already asserts the BANNER appears while uncertified and clears when
# certified. This asserts what REPLACES it, because certification is not
# silence: with the warning gone, the recipes that were NOT chart-certified are
# the ones most likely to be mistaken for verified.

def test_f_b46_certified_capture_swaps_banner_for_provenance():
    import brief2 as _B2
    unc = _B2.capture_envelope("2026-08-06", "post_ny", parity_certified=False)
    assert unc["banner"] == _B2.PARITY_BANNER
    assert unc["parity_provenance"] is None
    assert unc["parity_provenance_line"] is None

    cert = _B2.capture_envelope("2026-08-06", "post_ny", parity_certified=True)
    assert cert["banner"] is None, "the banner survived certification"
    assert cert["parity_provenance_line"], "certification left an empty slot"
    assert cert["parity_provenance"] is not None


def test_f_b46_provenance_names_what_was_NOT_chart_certified():
    """The half that matters. Volume profile, value area and LVN are excluded
    from the gate BY DESIGN and must say so where the reader sees the numbers."""
    import brief2 as _B2
    cert = _B2.capture_envelope("2026-08-06", "post_ny", parity_certified=True)
    pv = cert["parity_provenance"]

    not_cert = " ".join(pv["fixture_verified_not_chart_certified"]).lower()
    for must in ("profile", "lvn", "nesting"):
        assert must in not_cert, f"{must} is not disclosed as un-certified"

    # the REASON must be stated, not merely the fact -- otherwise a later cycle
    # reads the exclusion as an oversight and "fixes" it by comparing two
    # approximations to each other.
    why = pv["why_excluded"].lower()
    assert "approximation" in why and "certifies nothing" in why

    line = cert["parity_provenance_line"].lower()
    assert "not" in line and "chart-certified" in line
    assert "approximation" in line

    # and the certified list must actually name the families that passed
    cert_txt = " ".join(pv["certified"]).lower()
    for must in ("rolling_vwap", "anchored_vwap", "oscillator", "resample"):
        assert must in cert_txt, f"{must} missing from the certified list"

    # ANTI-VACUITY: the two lists must be disjoint. A recipe cannot be both.
    assert not (set(pv["certified"]) & set(pv["fixture_verified_not_chart_certified"]))


def test_f_b46_instrument_and_substrate_travel_with_the_certification():
    """A certification is only meaningful attached to WHAT was certified."""
    import brief2 as _B2
    pv = _B2.capture_envelope("2026-08-06", "post_ny",
                              parity_certified=True)["parity_provenance"]
    assert "BINANCE" in pv["instrument"]
    assert "1h" in pv["substrate"] and "hlc3" in pv["substrate"]
