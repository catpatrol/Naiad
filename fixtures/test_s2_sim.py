"""S-2 (engine 1.0.10) — corrected-simulator wake-order tests.

The permanent regression tranche (Amendment 2 §3.2): BTCUSDT_intraday
c141t213 — the V-short filled 2020-07-18T19:50Z whose campaign died the
same wake. The corrected simulator must price its ema89_gov_b0.0 fold-in
exit as the campaign_died open-flatten at +0.0739R gross, forever. This
test runs on the real estate (like F6's real-data validations) and MUST
pass before any grid run.

Synthetic legs pin the two wake-order fixes independently: fill-bar
coverage (an intra-bar touch on the fill bar exits at offset 0) and
death-bar flatten precedence (the open-flatten at camp_end+1 beats an
intra-bar touch on that bar).
"""

import numpy as np
import pytest

from engine.s2 import sim_corrected, two_line_walk


class _Sig:
    def __init__(self, o, h, l, c):
        self.o, self.h, self.l, self.c = (np.asarray(x, float)
                                          for x in (o, h, l, c))


def test_fill_bar_coverage():
    """Long fill at bar 2 open=100, entry stop 99, bar-2 low 98.5: the
    corrected walk exits ON the fill bar at the stop (offset 0); the legacy
    walk could not represent this."""
    sig = _Sig(o=[100, 100, 100, 100, 100], h=[101] * 5,
               l=[99.5, 99.5, 98.5, 99.5, 99.5], c=[100] * 5)
    path = np.full(3, 99.0)
    px, bar, kind = sim_corrected(sig, 1, 2, 4, 99.0, path)
    assert (px, bar, kind) == (99.0, 2, "stop")


def test_death_bar_flatten_precedence():
    """camp_end=2: at bar 3 the open-flatten executes even though the bar's
    low would have touched the stop intra-bar."""
    sig = _Sig(o=[100, 100, 100, 100.5], h=[101] * 4,
               l=[99.9, 99.9, 99.9, 98.0], c=[100, 100, 100, 100.4])
    path = np.full(3, 99.5)
    px, bar, kind = sim_corrected(sig, 1, 0, 2, 99.5, path)
    assert (px, bar, kind) == (100.5, 3, "flatten")


def test_two_line_tighter_line_wins():
    """Native at 99, candidate trailed to 99.8: bar low 99.5 touches only
    the candidate — two-line exits there, source cand."""
    sig = _Sig(o=[100, 100, 100, 100], h=[101] * 4,
               l=[99.9, 99.9, 99.5, 99.9], c=[100] * 4)
    native = np.full(4, 99.0)
    cand = np.array([99.0, 99.8, 99.8, 99.8])
    px, bar, kind, src = two_line_walk(sig, 1, 0, 3, 99.0, native, cand)
    assert (px, bar, kind, src) == (99.8, 2, "stop", "cand")


@pytest.mark.slow
def test_c141t213_regression(tmp_path):
    """The tranche that taught the simulator what order a bar happens in."""
    from engine.replay import run_replay
    from pathlib import Path
    import json
    s = run_replay("v12_anchor_g8", "BTCUSDT_intraday",
                   "2020-07-01", "2020-08-01",
                   tmp_path / "j", s2_sidecar_root=tmp_path / "e",
                   s2_resampled_dir=Path("research_outputs/s1/resampled"))
    hit = None
    for p in sorted((tmp_path / "j" / "BTCUSDT_intraday").glob("*.jsonl")):
        for line in open(p, encoding="utf-8"):
            r = json.loads(line)
            if r["evt"] == "EXIT" and r.get("s2") and \
                    r["exit_reason"] == "campaign_died":
                fills = r  # EXIT row; need matching fill ts 19:50
                if r["ts_open"] == "2020-07-18T19:51:00Z":
                    hit = r
    assert hit is not None, "regression tranche not found in the window"
    rec = hit["s2"]["tl"]["ema89_gov_b0.0"]
    assert rec["fold_kind"] == "flatten"
    assert abs(rec["fold_exit_r"] - 0.0739) < 5e-4, rec
    assert rec["two_exit_r"] == rec["fold_exit_r"], \
        "zero-advance identity must hold on the regression tranche"
