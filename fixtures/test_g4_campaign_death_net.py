"""G-4 (engine 1.0.5) — wake-time campaign-death net.

Campaign death WITHOUT a death event: the signals arming block re-arms on
every exec bar of the cross-visibility window (Pine-literal, parity-signed),
so a counter-window V campaign is silently overwritten one bar after birth —
dir flips, campaign id increments, the dying side's stop clears, and NO
X / REGIME / V event is journaled. The trading layer's flatten triggers were
all event-based, stranding the position (first observed: BTCUSDT_swing bar
52115, 2020-03-07 16:50Z — V short at 52113 killed by the standing bull
re-arm at 52114; the step-1 stop-guarantee then fired as a TRUE positive).

Design ruling of record (operator, 2026-07-13): the book follows the
campaign — a silently-killed campaign exits at the NEXT open via
exit_reason="campaign_died", uniform with the three event-based death modes
(one bar of exposure, same fill model). The signal layer is untouched.

This test MUST raise GateViolation on 1.0.4 and PASS on 1.0.5. The
stop-guarantee floor is unweakened: test_orphan_still_hard_fails
(test_g3_death_transition.py) keeps pinning NaN-stop + no-flatten +
NO-direction-mismatch as a hard failure.
"""

import numpy as np

from conftest import BASE_MS

from engine.cells import make_cell
from engine.config import load_config
from engine.signals import SignalEvent, SignalResult
from engine.trading import run_trading


def silent_rearm_scenario() -> SignalResult:
    """One short campaign, one filled tranche whose stop (110) is never
    touched; at bar 30 the campaign silently re-arms long — dir flips to +1,
    campaign id increments, stop_short clears — with NO event journaled
    (mirroring signals.py's visibility-window re-arm)."""
    n = 60
    open_ms = BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * 60_000
    o = np.full(n, 100.0)
    h = np.full(n, 100.4)
    l = np.full(n, 99.8)
    c = np.full(n, 100.0)
    v = np.full(n, 10.0)
    e9 = np.full(n, 100.0)
    e89 = np.full(n, 100.5)
    e200 = np.full(n, 80.0)
    atr = np.full(n, 0.4)
    g_atr = np.full(n, 1.0)
    g_e89 = np.full(n, 101.0)
    dir_ = np.zeros(n, dtype=np.int8)
    cc = np.zeros(n, dtype=bool)
    sl = np.full(n, np.nan)
    ss = np.full(n, np.nan)
    zone = np.zeros(n, dtype=np.int8)
    stage = np.ones(n, dtype=np.int8)
    camp = np.zeros(n, dtype=np.int64)

    dir_[2:30] = -1
    dir_[30:] = 1                  # silent re-arm: NO event at bar 30
    camp[2:30] = 1
    camp[30:] = 2
    ss[5:30] = 110.0               # cleared by the re-arm (signals.py:275)

    events = [
        SignalEvent(2, "REGIME", -1, stage=2, tier="full", arrow_visible=True),
        SignalEvent(5, "PRIME", -1, grade="A", rc=1, zone="Z2", retr=0.6,
                    stop=110.0, stage=2, tier="full", is_r1=True,
                    is_add=False, grade_uncapped="A"),
    ]
    return SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v,
        e9x=e9, e89x=e89, e200x=e200, atr_x=atr, g_atr=g_atr, g_e89=g_e89,
        dir=dir_, camp_counter=cc, stop_long=sl, stop_short=ss,
        active_zone=zone, stage=stage, campaign_id=camp, events=events)


def test_silent_rearm_flattens_campaign_died():
    """Silently-killed campaign: the stranded tranche must flatten at the
    open after the flip bar, exit_reason='campaign_died' — no GateViolation.
    (1.0.4 raises here: no event ever queues a flatten.)"""
    sig = silent_rearm_scenario()
    cell = make_cell("BTCUSDT", "intraday")
    cfg = load_config("naiad_v0")
    res = run_trading(cell, cfg, sig, None)   # 1.0.4: GateViolation here
    assert len(res.tranches) == 1, "the PRIME fill went missing"
    tr = res.tranches[0]
    assert tr.exited, "stranded tranche never exited"
    assert tr.exit_reason == "campaign_died"
    assert tr.exit_i == 31, "net must flatten at the bar after the flip"
    assert tr.exit_raw_px == 100.0, "flatten must fill at that bar's open"
