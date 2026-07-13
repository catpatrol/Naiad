"""G-5 / G-5b (engine 1.0.6) — same-wake sibling-add semantics.

Design rulings of record (operator, 2026-07-13, charter §3):
- Same-bar sibling adds are FILLABLE: the breakeven doctrine sequences adds
  across signal events; within-wake siblings do not breakeven-test each other.
  The assert keeps full force against all earlier-bar tranches
  (tr.fill_i < i, tolerance 1e-9).
- G-5b: the gate's pending-creation risk projection counts queued same-wake
  siblings; an over-cap later sibling produces a graceful risk_cap REJECT
  row, not a fill-time crash. Same-wake fill order is PRIME then CONFIRM.
- Variant seed logged: one-add-per-signal-bar dedupe (PRIME precedence).

Production instance: SOLUSDT_intraday bar 739466 (2022-02-09 19:26Z) — same-
bar PRIME+CONFIRM adds over a breakeven-protected R1; the second sibling's
fill tripped the assert against the first (a just-filled tranche sits above
the standing ratchet by construction; the ratchet only catches up on later
signal bars).

test_same_bar_sibling_adds_fill: GateViolation on 1.0.5, passes on 1.0.6.
test_breakeven_floor_earlier_tranche_still_fails: floor retained both versions.
test_overcap_sibling_rejected_risk_cap: crash on 1.0.5 (counterfactual
  established empirically), graceful risk_cap REJECT on 1.0.6.
"""

import numpy as np
import pytest

from conftest import BASE_MS

import engine.trading as trading
from engine.cells import make_cell
from engine.config import load_config
from engine.signals import SignalEvent, SignalResult
from engine.trading import GateViolation, run_trading


def _arrays(n, close):
    return dict(
        exec_open_ms=BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * 60_000,
        o=close.copy(), h=close + 0.2, l=close - 0.1, c=close,
        v=np.full(n, 10.0),
        e9x=close - 1, e89x=close - 2, e200x=np.full(n, 80.0),
        atr_x=np.full(n, 0.4), g_atr=np.full(n, 1.0), g_e89=np.full(n, 99.0),
        camp_counter=np.zeros(n, dtype=bool),
        stop_short=np.full(n, np.nan),
        active_zone=np.zeros(n, dtype=np.int8), stage=np.ones(n, dtype=np.int8),
    )


def sibling_scenario(n_confirm_adds: int) -> SignalResult:
    """Protected-R1 base + same-bar sibling adds (production shape).

    R1 fills at bar 6 (~100), ratchet 99; price rises to 104; the ratchet is
    hand-raised to 101 at bar 20 — ABOVE the R1 fill, so the R1 is breakeven-
    protected and adds are gate-eligible. Bar 30 emits one PRIME add plus
    n_confirm_adds CONFIRM adds (events in ruled fill order: PRIME first).
    Stops are never touched (l >= ~101.9 after the raise)."""
    n = 60
    close = np.concatenate([np.full(15, 100.0), np.linspace(100, 104, 15),
                            np.full(30, 104.0)])
    a = _arrays(n, close)
    dir_ = np.zeros(n, dtype=np.int8); dir_[2:] = 1
    camp = np.zeros(n, dtype=np.int64); camp[2:] = 1
    sl = np.full(n, np.nan); sl[5:20] = 99.0; sl[20:] = 101.0

    events = [
        SignalEvent(2, "REGIME", 1, stage=2, tier="full", arrow_visible=True),
        SignalEvent(5, "PRIME", 1, grade="A", rc=1, zone="Z2", retr=0.6,
                    stop=99.0, stage=2, tier="full", is_r1=True,
                    is_add=False, grade_uncapped="A"),
        SignalEvent(30, "PRIME", 1, grade="A", rc=2, zone="Z2", retr=0.5,
                    stop=101.0, stage=2, tier="full", is_r1=False,
                    is_add=True, grade_uncapped="A"),
    ]
    for _ in range(n_confirm_adds):
        events.append(SignalEvent(30, "CONFIRM", 1, grade="-", rc=2, zone="Z2",
                                  stop=101.0, stage=2, tier="full",
                                  is_r1=False, is_add=True, grade_uncapped="-"))
    return SignalResult(dir=dir_, campaign_id=camp, stop_long=sl,
                        events=events, **a)


def unprotected_r1_scenario() -> SignalResult:
    """R1 below breakeven (fill ~100, ratchet stays 99) + a second same-
    campaign R1 signal at bar 30 — gate-legal as an R1 (no breakeven test),
    used by the floor test's evil double."""
    n = 60
    close = np.full(n, 100.0)
    a = _arrays(n, close)
    dir_ = np.zeros(n, dtype=np.int8); dir_[2:] = 1
    camp = np.zeros(n, dtype=np.int64); camp[2:] = 1
    sl = np.full(n, np.nan); sl[5:] = 99.0
    events = [
        SignalEvent(2, "REGIME", 1, stage=2, tier="full", arrow_visible=True),
        SignalEvent(5, "PRIME", 1, grade="A", rc=1, zone="Z2", retr=0.6,
                    stop=99.0, stage=2, tier="full", is_r1=True,
                    is_add=False, grade_uncapped="A"),
        SignalEvent(30, "PRIME", 1, grade="A", rc=1, zone="Z2", retr=0.5,
                    stop=99.0, stage=2, tier="full", is_r1=True,
                    is_add=False, grade_uncapped="A"),
    ]
    return SignalResult(dir=dir_, campaign_id=camp, stop_long=sl,
                        events=events, **a)


def _cfg_cell():
    return make_cell("BTCUSDT", "intraday"), load_config("naiad_v0")


def test_same_bar_sibling_adds_fill():
    """3a — production shape: PRIME+CONFIRM adds on one bar over a protected
    R1. Both must fill sequentially at the next open (PRIME then CONFIRM),
    3 tranches, open campaign risk <= 1R, no raise. (1.0.5 raised the
    breakeven GateViolation on the second sibling.)"""
    cell, cfg = _cfg_cell()
    res = run_trading(cell, cfg, sibling_scenario(n_confirm_adds=1), None)
    assert len(res.tranches) == 3, "expected R1 + both sibling adds"
    r1, add1, add2 = res.tranches
    assert (add1.kind, add2.kind) == ("ADD", "ADD")
    assert add1.fill_i == add2.fill_i == 31, "siblings fill at the same open"
    assert not res.rejects, f"unexpected rejects: {res.rejects}"
    # rails: combined fresh risk vs the standing stop is exactly 1R
    open_risk = sum(max(0.0, (tr.fill_px - 101.0) * tr.dir) * tr.qty / tr.one_r_usd
                    for tr in res.tranches)
    assert open_risk <= 1.0 + 1e-9


def test_breakeven_floor_earlier_tranche_still_fails(monkeypatch):
    """3b — the assert floor: an ADD filling while a genuinely EARLIER-bar
    tranche sits below breakeven must still raise, on 1.0.5 and 1.0.6 alike.
    An honest gate cannot produce this state (gate and assert read the same
    ratchet), so the sanctioned F5 test double flips a gate-legal R1 into an
    ADD after admission."""
    def evil(pe):
        pe.kind = "ADD"
        return pe

    monkeypatch.setattr(trading, "admit_entry", evil)
    cell, cfg = _cfg_cell()
    with pytest.raises(GateViolation, match="below breakeven"):
        run_trading(cell, cfg, unprotected_r1_scenario(), None)


def flat_campaign_triple_prime() -> SignalResult:
    """Risk-projection isolate (1.0.7 rescope): a flat campaign (count 0 —
    the tranche cap cannot bind on three queued siblings) emits THREE
    synthetic same-wake PRIME adds of 0.5R each. Only the risk projection
    can reject the third. ADDs while flat are vacuously breakeven-eligible
    (charter: an R2+ PRIME while flat mid-campaign trades as an ADD)."""
    n = 60
    close = np.full(n, 100.0)
    a = _arrays(n, close)
    dir_ = np.zeros(n, dtype=np.int8); dir_[2:] = 1
    camp = np.zeros(n, dtype=np.int64); camp[2:] = 1
    sl = np.full(n, np.nan); sl[5:] = 99.0
    events = [SignalEvent(2, "REGIME", 1, stage=2, tier="full",
                          arrow_visible=True)]
    for _ in range(3):
        events.append(SignalEvent(30, "PRIME", 1, grade="A", rc=2, zone="Z2",
                                  retr=0.5, stop=99.0, stage=2, tier="full",
                                  is_r1=False, is_add=True, grade_uncapped="A"))
    return SignalResult(dir=dir_, campaign_id=camp, stop_long=sl,
                        events=events, **a)


def test_overcap_sibling_rejected_risk_cap():
    """3c — G-5b, rescoped at 1.0.7 (the original 3-siblings-over-R1
    scenario was doubly-illegal — cap AND risk — and the sibling-aware cap
    now correctly rejects it first; both halves pinned here).

    (i) risk projection isolate: flat campaign, three 0.5R PRIME siblings —
        cap cannot bind (0+2 < 3); the third rejects risk_cap; two fill;
        the in-path 1R assert passes.
    (ii) funnel order: the original R1 + PRIME + 2xCONFIRM scenario now
        lands the third sibling as max_tranches (cap projection fires before
        risk in the gate order); same graceful shape, ruled reason."""
    cell, cfg = _cfg_cell()

    res = run_trading(cell, cfg, flat_campaign_triple_prime(), None)
    assert len(res.tranches) == 2, "exactly two 0.5R siblings fill"
    rc = [r for r in res.rejects if r.reason == "risk_cap"]
    assert len(rc) == 1, f"expected one risk_cap reject, got {res.rejects}"
    assert rc[0].kind == "ADD" and rc[0].family == "prime" and rc[0].i == 30
    open_risk = sum(max(0.0, (tr.fill_px - 99.0) * tr.dir) * tr.qty / tr.one_r_usd
                    for tr in res.tranches)
    assert open_risk <= 1.0 + 1e-9

    res2 = run_trading(cell, cfg, sibling_scenario(n_confirm_adds=2), None)
    assert len(res2.tranches) == 3, "R1 + exactly two sibling adds fill"
    rc2 = [r for r in res2.rejects if r.reason == "max_tranches"]
    assert len(rc2) == 1, f"expected one max_tranches reject, got {res2.rejects}"
    assert rc2[0].kind == "ADD" and rc2[0].family == "confirm" and rc2[0].i == 30
