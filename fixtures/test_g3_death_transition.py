"""G-3 (engine 1.0.4) — stop-guarantee vs the campaign-death transition bar.

The signals layer clears the dying side's ratchet ON the death bar (opposite
governor cross / X / V-reversal); the real book flattens at the NEXT open
(wake step 3a). Engine 1.0.3's step-1 stop-guarantee assert ran before the
queued flatten and read the now-NaN ratchet -> spurious GateViolation on any
death arriving while a tranche is still open (first observed BTCUSDT_swing
bar 31418, 2019-12-26 20:05Z, V3 anchor-run pre-flight).

test_flatten_not_gate_violation: MUST FAIL on 1.0.3 and PASS on 1.0.4 —
the regression net for the fix.
test_orphan_still_hard_fails: pins the exemption's bound (G-3 ruling): a NaN
stop with NO queued flatten remains a hard GateViolation on both versions.
"""

import numpy as np
import pytest

from conftest import BASE_MS

from engine.cells import make_cell
from engine.config import load_config
from engine.signals import SignalEvent, SignalResult
from engine.trading import GateViolation, run_trading


def death_scenario(orphan: bool = False) -> SignalResult:
    """One long campaign, one filled tranche whose stop (90) is never touched.

    Default: an opposite REGIME cross at bar 30 kills the campaign — signals
    clear stop_long on the cross bar (mirroring signals.py), the flatten is
    queued for bar 31's open. The engine must flatten there, not raise.

    orphan=True: no death event — the ratchet just vanishes at bar 41 while
    dir stays long. That position is genuinely unprotected and the
    stop-guarantee MUST still raise.
    """
    n = 60
    open_ms = BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * 60_000
    o = np.full(n, 100.0)
    h = np.full(n, 100.4)
    l = np.full(n, 99.8)
    c = np.full(n, 100.0)
    v = np.full(n, 10.0)
    e9 = np.full(n, 100.0)
    e89 = np.full(n, 99.5)
    e200 = np.full(n, 120.0)
    atr = np.full(n, 0.4)
    g_atr = np.full(n, 1.0)
    g_e89 = np.full(n, 99.0)
    dir_ = np.zeros(n, dtype=np.int8)
    cc = np.zeros(n, dtype=bool)
    sl = np.full(n, np.nan)
    ss = np.full(n, np.nan)
    zone = np.zeros(n, dtype=np.int8)
    stage = np.ones(n, dtype=np.int8)
    camp = np.zeros(n, dtype=np.int64)
    events: list[SignalEvent] = []

    events.append(SignalEvent(2, "REGIME", 1, stage=2, tier="full",
                              arrow_visible=True))
    events.append(SignalEvent(5, "PRIME", 1, grade="A", rc=1, zone="Z2",
                              retr=0.6, stop=90.0, stage=2, tier="full",
                              is_r1=True, is_add=False, grade_uncapped="A"))
    if orphan:
        dir_[2:] = 1
        camp[2:] = 1
        sl[5:41] = 90.0            # ratchet vanishes at 41, dir still long:
        # no death event, no queued flatten -> hard GateViolation at wake 42
    else:
        dir_[2:30] = 1
        dir_[30:] = -1
        camp[2:30] = 1
        camp[30:] = 2
        sl[5:30] = 90.0            # cleared ON the cross bar (signals.py)
        events.append(SignalEvent(30, "REGIME", -1, stage=1, tier="full",
                                  arrow_visible=True))

    return SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v,
        e9x=e9, e89x=e89, e200x=e200, atr_x=atr, g_atr=g_atr, g_e89=g_e89,
        dir=dir_, camp_counter=cc, stop_long=sl, stop_short=ss,
        active_zone=zone, stage=stage, campaign_id=camp, events=events)


def test_flatten_not_gate_violation():
    """Opposite cross with an open tranche: flatten at the next open — the
    queued-flatten wake is exempt from the stop-guarantee (fails on 1.0.3)."""
    sig = death_scenario()
    cell = make_cell("BTCUSDT", "intraday")
    cfg = load_config("naiad_v0")
    res = run_trading(cell, cfg, sig, None)   # 1.0.3: GateViolation here
    assert len(res.tranches) == 1, "the PRIME fill went missing"
    tr = res.tranches[0]
    assert tr.exited, "tranche never exited despite campaign death"
    assert tr.exit_reason == "opposite_cross"
    assert tr.exit_i == 31, "flatten must fill at the bar after the cross"
    assert tr.exit_raw_px == 100.0, "flatten must fill at that bar's open"


def test_orphan_still_hard_fails():
    """The exemption's bound: NaN stop with NO queued flatten is still a
    hard failure — the guarantee is narrowed by one bar, not weakened."""
    sig = death_scenario(orphan=True)
    cell = make_cell("BTCUSDT", "intraday")
    cfg = load_config("naiad_v0")
    with pytest.raises(GateViolation, match="no working stop"):
        run_trading(cell, cfg, sig, None)
