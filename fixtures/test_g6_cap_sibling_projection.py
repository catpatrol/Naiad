"""G-6 (engine 1.0.7) — gate tranche-cap sibling projection.

The third and FINAL sibling-blind enforcement point (family enumeration in
CHANGELOG 1.0.7): a campaign standing at 2 fills receives same-wake
PRIME+CONFIRM adds; the gate's cap check evaluated each sibling individually
against the signal-time count (2 < 3, both queued); the first fill made it 3
and the second sibling's fill-time assert refused fill #4 — correctly: the
3-tranche cap is a hard charter rail. First observed: NEARUSDT_intraday bar
91950 (2020-12-18 04:30Z), V3 anchor run.

Semantics note of record (operator, 2026-07-13): no new trading-rule fork —
last-slot allocation follows the ratified PRIME-then-CONFIRM order; the gate
now counts queued same-campaign siblings toward the cap and the over-cap
sibling lands as a graceful max_tranches REJECT row.

test_cap_sibling_rejected: GateViolation on 1.0.6, graceful REJECT on 1.0.7.
test_cap_floor_forced_overfill_still_fails: floor retained both versions
  (sanctioned admit_entry double rewrites a fresh campaign-2 entry into the
  capped campaign 1 — the fill-time assert must raise).
"""

import numpy as np
import pytest

from conftest import BASE_MS

import engine.trading as trading
from engine.cells import make_cell
from engine.config import load_config
from engine.signals import SignalEvent, SignalResult
from engine.trading import GateViolation, run_trading


def g6_scenario(confirm_sibling: bool, second_campaign: bool) -> SignalResult:
    """Campaign 1 reaches 2 protected fills (R1 @5->6, ADD @22->23), the
    ratchet hand-raised behind each fill (99 -> 101 @20 -> 103.8 @26) so
    every prior tranche is breakeven-protected and no stop is ever touched.
    Bar 30 emits a PRIME add (+ optionally a same-wake CONFIRM add sibling).
    Optionally a same-direction re-arm opens campaign 2 with a fresh R1
    (used by the floor test's evil double)."""
    n = 60
    close = np.concatenate([np.full(10, 100.0), np.linspace(100, 104, 15),
                            np.full(35, 104.0)])
    a = dict(
        exec_open_ms=BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * 60_000,
        o=close.copy(), h=close + 0.2, l=close - 0.1, c=close,
        v=np.full(n, 10.0),
        e9x=close - 1, e89x=close - 2, e200x=np.full(n, 80.0),
        atr_x=np.full(n, 0.4), g_atr=np.full(n, 1.0), g_e89=np.full(n, 99.0),
        camp_counter=np.zeros(n, dtype=bool),
        stop_short=np.full(n, np.nan),
        active_zone=np.zeros(n, dtype=np.int8), stage=np.ones(n, dtype=np.int8),
    )
    dir_ = np.zeros(n, dtype=np.int8); dir_[2:] = 1
    camp = np.zeros(n, dtype=np.int64)
    camp[2:] = 1
    sl = np.full(n, np.nan)
    sl[5:20] = 99.0; sl[20:26] = 101.0; sl[26:] = 103.8

    events = [
        SignalEvent(2, "REGIME", 1, stage=2, tier="full", arrow_visible=True),
        SignalEvent(5, "PRIME", 1, grade="A", rc=1, zone="Z2", retr=0.6,
                    stop=99.0, stage=2, tier="full", is_r1=True,
                    is_add=False, grade_uncapped="A"),
        SignalEvent(22, "PRIME", 1, grade="A", rc=2, zone="Z2", retr=0.5,
                    stop=101.0, stage=2, tier="full", is_r1=False,
                    is_add=True, grade_uncapped="A"),
        SignalEvent(30, "PRIME", 1, grade="A", rc=3, zone="Z2", retr=0.5,
                    stop=103.8, stage=2, tier="full", is_r1=False,
                    is_add=True, grade_uncapped="A"),
    ]
    if confirm_sibling:
        events.append(SignalEvent(30, "CONFIRM", 1, grade="-", rc=3, zone="Z2",
                                  stop=103.8, stage=2, tier="full",
                                  is_r1=False, is_add=True, grade_uncapped="-"))
    if second_campaign:
        camp[40:] = 2   # same-direction re-arm: campaign id increments,
        # dir unchanged, book persists (ruled semantics, shadows.py span note)
        events.append(SignalEvent(40, "REGIME", 1, stage=2, tier="full",
                                  arrow_visible=True))
        events.append(SignalEvent(45, "PRIME", 1, grade="A", rc=1, zone="Z2",
                                  retr=0.6, stop=103.8, stage=2, tier="full",
                                  is_r1=True, is_add=False, grade_uncapped="A"))
    return SignalResult(dir=dir_, campaign_id=camp, stop_long=sl,
                        events=events, **a)


def _cfg_cell():
    return make_cell("BTCUSDT", "intraday"), load_config("naiad_v0")


def test_cap_sibling_rejected():
    """Production shape: campaign at 2 fills + same-wake PRIME+CONFIRM.
    On 1.0.7 the PRIME sibling takes the last slot (count 3) and the CONFIRM
    sibling lands as one max_tranches REJECT row at the signal bar — no
    raise, in-path cap assert passes. (1.0.6 crashed at the CONFIRM fill.)"""
    cell, cfg = _cfg_cell()
    res = run_trading(cell, cfg, g6_scenario(confirm_sibling=True,
                                             second_campaign=False), None)
    assert len(res.tranches) == 3, "R1 + ADD + the PRIME sibling (last slot)"
    assert [tr.kind for tr in res.tranches] == ["R1", "ADD", "ADD"]
    rc = [r for r in res.rejects if r.reason == "max_tranches"]
    assert len(rc) == 1, f"expected one max_tranches reject, got {res.rejects}"
    assert rc[0].kind == "ADD" and rc[0].family == "confirm" and rc[0].i == 30


def test_cap_floor_forced_overfill_still_fails(monkeypatch):
    """Floor: a genuinely over-cap FILL still raises on both versions. The
    gate legally admits a fresh campaign-2 R1; the sanctioned F5 double
    rewrites it into capped campaign 1 post-admission — the independent
    fill-time assert must refuse fill #4."""
    def evil(pe):
        pe.campaign = 1
        return pe

    monkeypatch.setattr(trading, "admit_entry", evil)
    cell, cfg = _cfg_cell()
    with pytest.raises(GateViolation, match="tranche cap"):
        run_trading(cell, cfg, g6_scenario(confirm_sibling=False,
                                           second_campaign=True), None)
