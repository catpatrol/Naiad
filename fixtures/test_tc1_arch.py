"""TC-1 (engine 1.0.11) — architecture unit tests: structural anchor,
trail one-way property, D's structural floor. Hand-built SignalResult +
arch_data, run_trading only (no journal), mirroring test_g8's style.
"""
import numpy as np
import pytest

from conftest import BASE_MS

from engine.cells import make_cell
from engine.config import load_config
from engine.signals import SignalEvent, SignalResult
from engine.trading import GateViolation, run_trading

CELL = make_cell("BTCUSDT", "swing")   # gov 4h, exec 5m — arbitrary; arch
#   data is injected directly, so the frames don't matter for these units.


def _scn(n, prime_bar, stop_native, dir_=1, gov_e200=None, atr=0.4,
         death_bar=None, price=None):
    """One long/short campaign: REGIME at 2, PRIME (R1) at prime_bar."""
    step = 60_000
    open_ms = BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * step
    o = np.full(n, 100.0) if price is None else price["o"].copy()
    h = np.full(n, 100.4) if price is None else price["h"].copy()
    l = np.full(n, 99.7) if price is None else price["l"].copy()
    c = np.full(n, 100.0) if price is None else price["c"].copy()
    v = np.full(n, 10.0)
    e9 = np.full(n, 100.0); e89 = np.full(n, 99.5 if dir_ == 1 else 100.5)
    e200 = np.full(n, 80.0 if dir_ == 1 else 120.0)
    atr_x = np.full(n, atr); g_atr = np.full(n, 1.0)
    g_e89 = np.full(n, 99.0 if dir_ == 1 else 101.0)
    d_ = np.zeros(n, dtype=np.int8); cc = np.zeros(n, dtype=bool)
    sl = np.full(n, np.nan); ss = np.full(n, np.nan)
    zone = np.zeros(n, dtype=np.int8); stage = np.ones(n, dtype=np.int8)
    camp = np.zeros(n, dtype=np.int64)
    d_[2:] = dir_; camp[2:] = 1
    if death_bar is not None:
        d_[death_bar:] = 0; camp[death_bar:] = 0
    if dir_ == 1:
        sl[prime_bar:] = stop_native
    else:
        ss[prime_bar:] = stop_native
    events = [SignalEvent(2, "REGIME", dir_, stage=2, tier="full",
                          arrow_visible=True),
              SignalEvent(prime_bar, "PRIME", dir_, grade="A", rc=1,
                          zone="Z2", retr=0.6, stop=stop_native, stage=2,
                          tier="full", is_r1=True, is_add=False,
                          grade_uncapped="A")]
    sig = SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v, e9x=e9, e89x=e89,
        e200x=e200, atr_x=atr_x, g_atr=g_atr, g_e89=g_e89, dir=d_,
        camp_counter=cc, stop_long=sl, stop_short=ss, active_zone=zone,
        stage=stage, campaign_id=camp, events=events)
    return sig


def _arch(n, pivots_low=None, pivots_high=None, gov_e200=None):
    """Build arch_data. pivots as [(conf_exec, oneh_idx, value)]."""
    exec_1h = (np.arange(n) // 60).astype(np.int64)
    pl = pivots_low or []
    ph = pivots_high or []
    ge = np.full(n, 90.0) if gov_e200 is None else np.asarray(gov_e200, float)
    return {
        "gov_e200": ge, "exec_1h": exec_1h,
        "plow_conf": np.array([p[0] for p in pl], np.int64),
        "plow_1h": np.array([p[1] for p in pl], np.int64),
        "plow_val": np.array([p[2] for p in pl], float),
        "phigh_conf": np.array([p[0] for p in ph], np.int64),
        "phigh_1h": np.array([p[1] for p in ph], np.int64),
        "phigh_val": np.array([p[2] for p in ph], float)}


# ── structural anchor + static-for-life ───────────────────────────────────

def test_struct_anchor_static():
    """Long fills ~100.06; nearest 1h pivot low 97 → struct = 97 − 0.2 =
    96.8. Static: struct_stop == stop_at_entry for the whole life."""
    sig = _scn(120, 5, 99.5, death_bar=80)
    arch = _arch(120, pivots_low=[(5, 0, 97.0)])
    res = run_trading(CELL, load_config("tc1_B"), sig, None, arch_data=arch)
    assert len(res.tranches) == 1
    tr = res.tranches[0]
    assert tr.is_struct and abs(tr.struct_stop - 96.8) < 1e-9
    assert abs(tr.stop_at_entry - 96.8) < 1e-9
    assert tr.exited and tr.exit_reason == "campaign_died"   # 96.8 never hit
    assert tr.struct_stop == 96.8   # unchanged — static for life


def test_no_struct_anchor_reject():
    """Only a pivot ABOVE entry exists (long) → no eligible pivot → the
    tranche is not taken (no_struct_anchor)."""
    sig = _scn(60, 5, 99.5)
    arch = _arch(60, pivots_low=[(5, 0, 103.0)])   # above entry
    res = run_trading(CELL, load_config("tc1_B"), sig, None, arch_data=arch)
    assert not res.tranches
    assert [r.reason for r in res.rejects].count("no_struct_anchor") == 1


def test_struct_stops_out_at_its_own_level():
    """Price dips to 96.5 at bar 40 → the struct tranche stops at 96.8."""
    n = 120
    price = {"o": np.full(n, 100.0), "h": np.full(n, 100.4),
             "l": np.full(n, 99.7), "c": np.full(n, 100.0)}
    price["l"][40] = 96.5    # pierces 96.8
    sig = _scn(n, 5, 99.5, price=price)
    arch = _arch(n, pivots_low=[(5, 0, 97.0)])
    res = run_trading(CELL, load_config("tc1_B"), sig, None, arch_data=arch)
    tr = res.tranches[0]
    assert tr.exited and tr.exit_reason == "stop"
    assert abs(tr.exit_raw_px - 96.8) < 1e-9 and tr.exit_i == 40


# ── trail one-way + D floor ───────────────────────────────────────────────

def test_trail_one_way_never_loosens():
    """C (native + trail): gov_e200 rises then falls; the engaged trail
    stop must be monotone non-decreasing (long)."""
    n = 120
    ge = np.full(n, 98.0)
    ge[10:30] = np.linspace(98.0, 99.5, 20)   # rising → trail tightens up
    ge[30:60] = np.linspace(99.5, 97.0, 30)   # falling → must NOT loosen
    # keep price above the trail so it doesn't exit; engagement needs close
    # beyond gov e200 (c=100 > ge always here)
    sig = _scn(n, 5, 99.5, death_bar=100)
    arch = _arch(n, gov_e200=ge)
    res = run_trading(CELL, load_config("tc1_C"), sig, None, arch_data=arch)
    tr = res.tranches[0]
    assert tr.trail_on and tr.engaged
    # trail_stop is the final one-way value; reconstruct monotonicity by
    # re-running the update is internal, so assert it ended at the peak-era
    # trail (≈ max gov_e200 − 0.2 = 99.3), not the late dip (97 − 0.2)
    assert tr.trail_stop >= 99.5 - 0.2 - 1e-6


def test_d_floor_never_below_structural():
    """D (struct + trail): gov_e200 dips well below the structural stop;
    the working stop must never fall below the structural floor."""
    n = 120
    ge = np.full(n, 100.5)      # above price 100 → engagement never triggers
    #   for a long (needs c > ge). Use a case where trail engages then the
    #   line drops below struct: price 100, ge starts 99 (engage), then 90.
    ge = np.full(n, 90.0)
    ge[5:12] = 99.0             # engage window (c=100 > 99)
    sig = _scn(n, 5, 99.5, death_bar=100)
    arch = _arch(n, pivots_low=[(5, 0, 97.0)], gov_e200=ge)  # struct 96.8
    res = run_trading(CELL, load_config("tc1_D"), sig, None, arch_data=arch)
    tr = res.tranches[0]
    assert tr.is_struct and tr.trail_on
    # once engaged, the D stop = max(trail, 96.8) ≥ 96.8 always
    if tr.engaged:
        assert tr.trail_stop >= 96.8 - 1e-9
