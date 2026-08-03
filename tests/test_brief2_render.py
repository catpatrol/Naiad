"""F-B10 / F-B20 / D.7 -- the render layer (Amendment 2 §2, §3.5, §4.2, §7).

F-B10  render fidelity: byte-identical modulo the render timestamp, and the
       render RECOMPUTES NOTHING.
F-B20  a Tier-2 fetch failure still renders, with degradation chips.
D.7.1  the R:R board is bucketed by target distance and ranked WITHIN buckets.
"""

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import brief_note as BN                                             # noqa: E402
import brief_render as BR                                           # noqa: E402

BRIEFS = ROOT / "briefs"


def _capture():
    caps = sorted(BRIEFS.glob("brief_*_*.json"))
    if not caps:
        pytest.skip("no capture in briefs/")
    return json.loads(caps[-1].read_text(encoding="utf-8"))


# --------------------------------------------------------------- F-B10

def test_f_b10_render_is_byte_identical_modulo_the_timestamp():
    doc = _capture()
    a = BR.render(doc, generated_utc="2026-01-01T00:00:00Z")
    b = BR.render(doc, generated_utc="2026-01-01T00:00:00Z")
    assert a == b, "the render is not deterministic for a fixed timestamp"

    c = BR.render(doc, generated_utc="2099-12-31T23:59:59Z")
    assert c != a, "the timestamp must actually appear in the output"
    assert c.replace("2099-12-31T23:59:59Z", "2026-01-01T00:00:00Z") == a, \
        "the render differs by more than the timestamp"


def test_f_b10_render_recomputes_nothing():
    """A render that recomputed would be a second source of truth, and the drift
    would be invisible because the page would still look right."""
    src = (ROOT / "scripts" / "brief_render.py").read_text(encoding="utf-8")

    # Test for CALLS and IMPORTS, not bare names. `stoch_rsi_k` is a capture KEY
    # the render legitimately READS; `stoch_rsi(` would be a recomputation.
    # (Fifth instance of the same fixture bug in this project: scan what the
    # code DOES, not what it mentions.)
    for fn in ("rolling_vwap", "anchored_vwap", "windowed_profile",
               "volume_profile", "dual_score", "collapse_same_family",
               "cluster", "resample_ohlcv", "confirmed_pivots", "stoch_rsi",
               "rsi", "macd", "atr", "low_volume_nodes", "va_nesting"):
        assert f"{fn}(" not in src, (
            f"brief_render.py CALLS {fn}() -- it must READ the capture, "
            f"not recompute")

    import ast
    tree = ast.parse(src)
    for node in ast.walk(tree):
        mod = (node.module if isinstance(node, ast.ImportFrom) else None)
        names = ([a.name for a in node.names]
                 if isinstance(node, (ast.Import, ast.ImportFrom)) else [])
        for n in ([mod] if mod else []) + names:
            assert not str(n).startswith("analytics"), (
                f"brief_render.py imports {n!r} -- the render must not reach "
                f"the computation layer at all")

    # ...and it must actually print numbers straight out of the capture
    doc = _capture()
    sym, a = next(iter(doc["assets"].items()))
    html = BR.part1_html(sym, a)
    st = a.get("stretch") or {}
    live = [r for r in st.get("rows") or [] if r.get("sigma_position") is not None]
    assert live, "no live stretch rows -- the assertion would be vacuous"
    for r in live[:3]:
        assert f"{r['sigma_position']:+,.2f}" in html, (
            f"{r['name']} sigma position is not printed verbatim from the capture")


def test_f_b10_parity_banner_prints_and_clears():
    doc = _capture()
    on = BR.render(dict(doc, banner="PARITY NOT CERTIFIED - test"),
                   generated_utc="x")
    assert "PARITY NOT CERTIFIED" in on
    off = BR.render(dict(doc, banner=None, parity_certified=True),
                    generated_utc="x")
    assert "PARITY NOT CERTIFIED" not in off, (
        "the banner must clear when the flag is set, or it asserts nothing")


def test_f_b10_prose_requirement_is_rendered():
    """4.2 -- a table alone does not satisfy the nesting section."""
    doc = _capture()
    sym, a = next(iter(doc["assets"].items()))
    nest = a.get("va_nesting") or {}
    if not nest.get("prose"):
        pytest.skip("no nesting prose in this capture")
    html = BR.part1_html(sym, a)
    for sentence in nest["prose"]:
        head = sentence.split(".")[0][:40]
        assert head in html, "a prose sentence did not reach the page"


def test_f_b10_forming_candle_is_drawn_and_labelled():
    doc = _capture()
    sym, a = next(iter(doc["assets"].items()))
    planes = (a.get("chart_planes") or {}).get("planes") or {}
    html = BR.part1_html(sym, a)
    if any((p.get("forming") or {}).get("available") for p in planes.values()):
        assert "forming" in html and "greyed" in html
    assert "NO computed value" in html or "appears in NO" in html


# --------------------------------------------------------------- F-B20

def test_f_b20_tier2_failure_still_renders_with_chips():
    doc = _capture()
    broken = json.loads(json.dumps(doc))
    for a in broken["assets"].values():
        a["tier2"] = {"provenance": "degraded", "error": "fetch failed",
                      "oi": None, "oi_change_pct": None}
    html = BR.render(broken, generated_utc="x")
    assert len(html) > 5000, "the render collapsed on a degraded Tier-2 block"
    assert "Part I" in html and "Part II" in html


def test_f_b20_missing_layers_never_crash_the_render():
    """Every layer is optional at render time; absence is not an exception."""
    doc = _capture()
    for drop in ("stretch", "band_excursions", "va_nesting", "oscillators",
                 "chart_planes", "lattice_12_25", "volume_windows",
                 "decision_instrument", "confluence", "bias"):
        broken = json.loads(json.dumps(doc))
        for a in broken["assets"].values():
            a.pop(drop, None)
        html = BR.render(broken, generated_utc="x")
        assert "Part I" in html and "Part II" in html, (
            f"dropping {drop} broke the render")

    empty = dict(doc, assets={})
    assert "Part I" in BR.render(empty, generated_utc="x")


# --------------------------------------------------------------- D.7

def test_d71_target_buckets_rank_within_not_globally():
    """The mirror of R-1: a distant TARGET inflates R:R exactly as a knife-edge
    STOP does. A 47-ATR target on a 0.25-ATR stop reads 188:1 and means nothing."""
    rows = [{"rr": 188.0, "target_atr": 47.0, "side": "long"},
            {"rr": 2.1, "target_atr": 1.2, "side": "long"},
            {"rr": 3.4, "target_atr": 4.0, "side": "short"},
            {"rr": 1.1, "target_atr": 0.8, "side": "short"}]
    b = BR.bucket_board(rows)
    assert [r["rr"] for r in b["NEAR"]] == [2.1, 1.1]
    assert [r["rr"] for r in b["MID"]] == [3.4]
    assert [r["rr"] for r in b["FAR"]] == [188.0]
    assert b["NEAR"][0]["rr"] < b["FAR"][0]["rr"], (
        "the 188:1 row must NOT be able to outrank a near-target row")

    assert BR.target_bucket(0.5) == "NEAR"
    assert BR.target_bucket(2.0) == "MID"
    assert BR.target_bucket(6.0) == "FAR"
    assert BR.target_bucket(None) is None


def test_d72_target_clusters_are_not_distance_filtered():
    """D.4 WITHDRAWN: no admission filter by distance. One sigma of BTC's 365d
    RVWAP is 11.4 daily ATR -- the far bands are structure, not ballast."""
    conf = {"with_volume": {"clusters": [
        {"mean": 100.0, "score": 5, "families": ["ss"], "member_count": 2},
        {"mean": 900.0, "score": 9,
         "families": ["vwap_rolling", "profile_windowed", "ss"],
         "member_count": 6},
        {"mean": 10.0, "score": 7, "families": ["structure"], "member_count": 3}]}}
    tc = BR.target_clusters(conf, price=50.0, atr=10.0)
    means = [c["mean"] for c in tc["above"]]
    assert 900.0 in means, "a far cluster was filtered out -- D.4 is withdrawn"
    assert tc["above"][0]["score"] == 9, "ranked by SCORE, not by proximity"
    assert tc["above"][0]["atr_away"] == pytest.approx(85.0)
    assert [c["mean"] for c in tc["below"]] == [10.0]


def test_d73_render_carries_no_sizing_or_probability():
    doc = _capture()
    html = BR.render(doc, generated_utc="x").lower()
    for banned in ("position size", "risk %", "leverage", "notional",
                   "win rate", "expectancy", "probability of"):
        assert banned not in html, f"forbidden language in the render: {banned}"
    assert "not probability" in html, "the geometry disclaimer must be printed"
    assert "no sizing" in html


# --------------------------------------------------------------- brief_note

def test_brief_note_refuses_outcome_and_sizing_language():
    """The firewall at the one place a human types free text into the record."""
    for bad in ("that trade won", "closed for a 2R profit", "pnl was good",
                "half size next time", "our win rate is improving"):
        assert BN.check_note(bad), f"outcome/sizing language not caught: {bad!r}"
    for ok in ("the 30d VAL held on the retest",
               "price rejected the 90d VAH twice",
               "monthly anchor is still above the quarterly"):
        assert BN.check_note(ok) == [], f"a legitimate observation was refused: {ok!r}"


def test_brief_note_appends_and_never_rewrites(tmp_path):
    import brief2 as B2
    import brief_capture as BC
    d = tmp_path
    doc = B2.capture_envelope("2026-08-03", "post_ny")
    doc["generated_utc"] = "2026-08-03T20:30:00Z"
    doc["assets"] = {}
    BC.write_capture(doc, briefs_dir=d)
    before = json.loads((d / "brief_2026-08-03_post_ny.json").read_text(encoding="utf-8"))

    BN.append_note("2026-08-03", "post_ny",
                   "the 30d VAL held on the retest", briefs_dir=d)
    after = json.loads((d / "brief_2026-08-03_post_ny.json").read_text(encoding="utf-8"))
    assert len(after["operator_notes"]) == 1
    assert after["operator_notes"][0]["observation_only"] is True
    assert after["date"] == before["date"], "the capture body changed"

    BN.append_note("2026-08-03", "post_ny", "and again on the second test",
                   briefs_dir=d)
    after2 = json.loads((d / "brief_2026-08-03_post_ny.json").read_text(encoding="utf-8"))
    assert len(after2["operator_notes"]) == 2, "notes must APPEND, not replace"

    idx = (d / "index.jsonl").read_text(encoding="utf-8").strip().splitlines()
    assert len(idx) == 3, "the index is append-only: 1 write + 2 amendments"

    with pytest.raises(SystemExit) as e:
        BN.append_note("2026-08-03", "post_ny", "that one won big", briefs_dir=d)
    assert "REFUSED" in str(e.value) and "census work under G-7" in str(e.value)
