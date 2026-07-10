"""F7 — warm-up: every replay refuses to emit signals until >= 2000 exec bars
AND >= 200 governor bars of history precede the window."""

import pytest

from conftest import SYNTH_END

from engine.replay import WarmupError, run_replay


def test_insufficient_warmup_refused(synth_env, synth_cell, tmp_path):
    # synthetic data starts 2024-01-01; one day of history is far too little
    with pytest.raises(WarmupError, match="2000"):
        run_replay("naiad_v0", synth_cell.cell_id, "2024-01-02", SYNTH_END,
                   tmp_path / "j", log=lambda *_: None)


def test_governor_floor_binds_independently(synth_env, tmp_path):
    # position mandate: 12h governor -> 20 days hold only ~28 governor bars,
    # while 15m exec bars exceed 2000 — the governor floor must still refuse
    from engine.cells import make_cell
    cell = make_cell("BTCUSDT", "position")
    with pytest.raises(WarmupError):
        run_replay("naiad_v0", cell.cell_id, "2024-01-19", "2024-01-20",
                   tmp_path / "j", log=lambda *_: None)


def test_sufficient_warmup_accepted(synth_env, synth_cell, tmp_path):
    summary = run_replay("naiad_v0", synth_cell.cell_id, "2024-01-15",
                         SYNTH_END, tmp_path / "j", log=lambda *_: None)
    assert summary["rows"] > 0
