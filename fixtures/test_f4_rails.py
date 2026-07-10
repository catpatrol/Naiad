"""F4 — risk rails: a constructed scenario breaches -2R intraday and the
engine halts, in the replay path AND the tick.py path. The journal shows a
HALT row; no further entries fill that UTC day.
"""

import json
import sys
from pathlib import Path

import pytest

from conftest import halt_scenario

import engine.replay as replay_mod
from engine.cells import make_cell
from engine.config import load_config
from engine.journal import read_journal
from engine.trading import run_trading


def test_day_breaker_direct():
    """run_trading on the hand-built five-loss scenario."""
    sig = halt_scenario()
    cell = make_cell("BTCUSDT", "intraday")
    cfg = load_config("naiad_v0")
    res = run_trading(cell, cfg, sig, None)
    day_halts = [h for h in res.halts if h.scope == "day"]
    assert day_halts, "-2R day never tripped the breaker"
    halt_bar = day_halts[0].i
    assert day_halts[0].r_total <= -2.0
    # exactly the four pre-halt tranches filled; the fifth was blocked
    assert len(res.tranches) == 4
    assert all(tr.fill_i <= halt_bar for tr in res.tranches)
    assert any(r.reason == "halted_day" for r in res.rejects)


@pytest.fixture()
def injected_signals(monkeypatch):
    """Make run_replay compute the hand-built scenario regardless of data."""
    sig = halt_scenario()
    monkeypatch.setattr(replay_mod, "compute_signals",
                        lambda *a, **k: sig)
    return sig


def test_day_breaker_replay_path(synth_env, synth_cell, injected_signals, tmp_path):
    summary = replay_mod.run_replay("naiad_v0", synth_cell.cell_id,
                                    "2024-01-15", "2024-01-16",
                                    tmp_path / "j", log=lambda *_: None)
    rows = read_journal(tmp_path / "j", synth_cell.cell_id)
    halts = [r for r in rows if r["evt"] == "HALT" and r["tranche_id"] == "day"]
    assert halts, "no HALT row in the journal"
    halt_ts = halts[0]["ts_open"]
    fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
    assert fills, "scenario produced no fills at all"
    day = halt_ts[:10]
    for r in fills:
        if r["ts_open"][:10] == day:
            assert r["ts_open"] <= halt_ts, \
                "an entry filled after the day halt tripped"
    assert any(r["evt"] == "REJECT" and r["reject_reason"] == "halted_day"
               for r in rows)


def test_day_breaker_tick_path(synth_env, synth_cell, injected_signals,
                               tmp_path, monkeypatch):
    """The same breach must halt via scripts/tick.py (F4: replay AND paper
    path). Network calls are stubbed to the local synthetic cache."""
    import engine.data as dl
    monkeypatch.setattr(dl, "backfill_klines",
                        lambda sym, iv, s, e, log=print: dl.load_klines(sym, iv, s, e))
    monkeypatch.setattr(dl, "backfill_funding",
                        lambda sym, s, e, log=print: dl.load_funding(sym, s, e))
    # freeze "now" inside the synthetic data span
    import time as _time
    monkeypatch.setattr(_time, "time", lambda: 1_705_600_000.0)  # 2024-01-18

    sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
    import tick
    # pre-seed state so the epoch falls inside the synthetic span
    state_root = tmp_path / "state"
    state_root.mkdir()
    (state_root / f"{synth_cell.cell_id}.json").write_text(json.dumps(
        {"cell_id": synth_cell.cell_id, "paper_epoch": "2024-01-15"}))
    monkeypatch.setattr(sys, "argv", [
        "tick.py", "--config", "naiad_v0", "--cells", synth_cell.cell_id,
        "--journal-root", str(tmp_path / "j"), "--state-root", str(state_root)])
    assert tick.main() == 0

    state = json.loads((state_root / f"{synth_cell.cell_id}.json").read_text())
    assert state["error"] is None, f"tick failed: {state['error']}"
    assert state["halts"] >= 1, "tick path did not record the halt"
    rows = read_journal(tmp_path / "j", synth_cell.cell_id)
    assert any(r["evt"] == "HALT" for r in rows)
