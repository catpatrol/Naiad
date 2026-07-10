"""F5 — gate integrity: the traded set equals the eligible set, enforced by
in-path assertions independent of the admission logic. A deliberately broken
gate (test double on trading.admit_entry) must fail loudly (GateViolation).
"""

import numpy as np
import pytest

from conftest import SYNTH_END, SYNTH_START, halt_scenario

import engine.trading as trading
from engine.cells import make_cell
from engine.config import load_config
from engine.journal import read_journal
from engine.replay import run_replay
from engine.signals import SignalEvent
from engine.trading import GateViolation, run_trading


def test_traded_set_equals_eligible_set(synth_env, synth_cell, tmp_path):
    """Offline re-derivation from the journal: every fill obeys the sizing
    table, the C-ban, and the tranche cap; C events stay journal-only."""
    run_replay("naiad_v0", synth_cell.cell_id, SYNTH_START, SYNTH_END,
               tmp_path / "j", log=lambda *_: None)
    rows = read_journal(tmp_path / "j", synth_cell.cell_id)
    t = load_config("naiad_v0")["trading"]

    fills = [r for r in rows if r["evt"] in ("ENTRY_FILL", "ADD_FILL")]
    assert fills, "no fills to audit"
    per_campaign = {}
    for r in fills:
        assert r["grade"] != "C", "a C-grade signal traded"
        if r["evt"] == "ADD_FILL":
            expected = t["size_add"]
        elif r["grade"] == "V":
            expected = t["size_v"]
        elif r["tier"] == "provisional":
            expected = t["size_r1_provisional"]
        elif r["grade"] in ("A+", "A"):
            expected = t["size_r1_a_full"]
        else:
            expected = t["size_r1_b_full"]
        assert r["size_r"] == expected, \
            f"sizing table violated at {r['ts_open']}: {r['size_r']} != {expected}"
        camp = r["tranche_id"].split("t")[0]
        per_campaign[camp] = per_campaign.get(camp, 0) + 1
    assert max(per_campaign.values()) <= t["max_tranches"]

    c_events = [r for r in rows if r["evt"] == "CONFIRM" and r["grade"] == "C"]
    fill_keys = {(r["ts_open"], r["dir"]) for r in fills}
    for r in c_events:
        assert (r["ts_open"], r["dir"]) not in fill_keys


def _cfg_cell():
    return make_cell("BTCUSDT", "intraday"), load_config("naiad_v0")


def test_broken_gate_c_grade_fails_loudly(monkeypatch):
    def evil(pe):
        pe.grade = "C"
        return pe

    monkeypatch.setattr(trading, "admit_entry", evil)
    cell, cfg = _cfg_cell()
    with pytest.raises(GateViolation, match="C-grade"):
        run_trading(cell, cfg, halt_scenario(), None)


def test_broken_gate_oversize_fails_loudly(monkeypatch):
    def evil(pe):
        pe.size_r = 5.0
        return pe

    monkeypatch.setattr(trading, "admit_entry", evil)
    cell, cfg = _cfg_cell()
    with pytest.raises(GateViolation, match="1R"):
        run_trading(cell, cfg, halt_scenario(), None)


def _rising_scenario():
    """Three legitimately-filled tranches in campaign 1 (price rises, every
    add's priors sit at/beyond breakeven, no stop ever hit), then a fresh
    campaign 2 with one more R1 signal."""
    from conftest import BASE_MS
    from engine.signals import SignalResult

    n = 400
    open_ms = BASE_MS + np.arange(n, dtype=np.int64) * 60_000
    c = np.concatenate([np.linspace(100, 102, 60), np.linspace(102, 104, 50),
                        np.linspace(104, 106, 290)])
    o = c.copy()
    h = c + 0.2
    l = c - 0.1
    v = np.full(n, 10.0)
    sl = np.full(n, np.nan)
    dir_ = np.zeros(n, dtype=np.int8)
    dir_[2:] = 1
    camp = np.zeros(n, dtype=np.int64)
    camp[2:200] = 1
    camp[200:] = 2

    events = [SignalEvent(2, "REGIME", 1, stage=2, tier="full", arrow_visible=True),
              SignalEvent(200, "REGIME", 1, stage=2, tier="full", arrow_visible=True)]
    stops = {10: 99.0, 60: 101.5, 110: 103.5, 210: 104.5}
    for b, s in stops.items():
        sl[b:] = s
        is_r1 = b in (10, 210)
        events.append(SignalEvent(b, "PRIME", 1, grade="A",
                                  rc=1 if is_r1 else (2 if b == 60 else 3),
                                  zone="Z2", stop=s, stage=2, tier="full",
                                  is_r1=is_r1, is_add=not is_r1,
                                  grade_uncapped="A"))
    return SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v,
        e9x=c - 1, e89x=c - 2, e200x=np.full(n, 200.0),
        atr_x=np.full(n, 0.4), g_atr=np.full(n, 1.0), g_e89=np.full(n, 99.0),
        dir=dir_, camp_counter=np.zeros(n, dtype=bool),
        stop_long=sl, stop_short=np.full(n, np.nan),
        active_zone=np.zeros(n, dtype=np.int8), stage=np.ones(n, dtype=np.int8),
        campaign_id=camp, events=events)


def test_broken_gate_tranche_cap_fails_loudly(monkeypatch):
    """Sanity first: honest gates fill 3+1 tranches across two campaigns.
    Then the double rewrites campaign 2's entry into campaign 1 (which is
    already at the 3-tranche cap) — the independent fill assertion raises."""
    cell, cfg = _cfg_cell()
    res = run_trading(cell, cfg, _rising_scenario(), None)
    assert len(res.tranches) == 4
    assert [tr.campaign for tr in res.tranches] == [1, 1, 1, 2]

    def evil(pe):
        pe.campaign = 1
        return pe

    monkeypatch.setattr(trading, "admit_entry", evil)
    with pytest.raises(GateViolation, match="tranche cap"):
        run_trading(cell, cfg, _rising_scenario(), None)
