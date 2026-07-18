"""G-8 (engine 1.0.8) — four hard guards, each breached by a synthetic cell.

TC-4 contract §3 (operator-ratified values): G-8a equity floor 25% of initial
(breach = permanent cell halt), G-8b notional cap (REJECT at 10x equity,
never resize), G-8c minimum stop distance (0.5 x signal-bar exec ATR,
extending the unit_risk<=0 rejection), G-8d one_r>0 unit sanity assert.

G-8a/b/c sit behind config keys (absent key = guard off, so pre-G8 configs
replay byte-identically); G-8d is an unconditional in-path assert of the F5
family. The synthetic scenarios mirror test_g4/test_g5: hand-built
SignalResult, run_trading only, no journal.
"""

import numpy as np
import pytest

from conftest import BASE_MS

from engine.cells import make_cell
from engine.config import load_config
from engine.journal import make_row
from engine.signals import SignalEvent, SignalResult
from engine.trading import GateViolation, run_trading


def _scenario(n, primes, gap_bar=None, gap_to=None, atr=0.4):
    """Long-only tape at price 100; `primes` = [(bar, campaign_id, stop)];
    optional gap to `gap_to` at gap_bar's open (gap-through-stop exit of
    whatever is open). Lows are held above every pre-gap stop so nothing
    stops out intra-bar before the gap."""
    open_ms = BASE_MS + 14 * 86_400_000 + np.arange(n, dtype=np.int64) * 60_000
    pre_stops = [s for b, _, s in primes if gap_bar is None or b < gap_bar]
    o = np.full(n, 100.0)
    h = np.full(n, 100.4 + max(0.0, max(pre_stops) - 100.0))
    l = np.full(n, max(pre_stops) + 0.01)
    c = np.full(n, 100.0)
    v = np.full(n, 10.0)
    e9 = np.full(n, 100.0)
    e89 = np.full(n, 99.5)
    e200 = np.full(n, 80.0)
    atr_x = np.full(n, atr)
    g_atr = np.full(n, 1.0)
    g_e89 = np.full(n, 99.0)
    dir_ = np.zeros(n, dtype=np.int8)
    cc = np.zeros(n, dtype=bool)
    sl = np.full(n, np.nan)
    ss = np.full(n, np.nan)
    zone = np.zeros(n, dtype=np.int8)
    stage = np.ones(n, dtype=np.int8)
    camp = np.zeros(n, dtype=np.int64)

    if gap_bar is not None:
        o[gap_bar:] = gap_to
        h[gap_bar:] = gap_to + 0.1
        l[gap_bar:] = gap_to - 0.1
        c[gap_bar:] = gap_to

    dir_[2:] = 1
    camp[2:] = primes[0][1]
    events = [SignalEvent(2, "REGIME", 1, stage=2, tier="full",
                          arrow_visible=True)]
    for b, cid, stop in primes:
        camp[b:] = cid
        sl[b:] = stop         # ratchet from the signal bar on (never loosened)
        events.append(SignalEvent(b, "PRIME", 1, grade="A", rc=1, zone="Z2",
                                  retr=0.6, stop=stop, stage=2, tier="full",
                                  is_r1=True, is_add=False,
                                  grade_uncapped="A"))
    return SignalResult(
        exec_open_ms=open_ms, o=o, h=h, l=l, c=c, v=v,
        e9x=e9, e89x=e89, e200x=e200, atr_x=atr_x, g_atr=g_atr, g_e89=g_e89,
        dir=dir_, camp_counter=cc, stop_long=sl, stop_short=ss,
        active_zone=zone, stage=stage, campaign_id=camp, events=events)


CELL = make_cell("BTCUSDT", "intraday")   # tier A: 2 bps slip -> fill 100.02
LATE = 10 + 11 * 1440   # a PRIME 11 days later: outside any day/week halt


def _rejects(res, reason):
    return [r for r in res.rejects if r.reason == reason]


# ── G-8c — minimum stop distance ──────────────────────────────────────────

def test_g8c_stop_too_tight_rejected():
    """Stop 0.12 under fill with 0.5 x ATR = 0.20 floor: fill refused,
    reject_reason=stop_too_tight, no tranche minted."""
    sig = _scenario(60, [(5, 1, 99.9)], atr=0.4)
    res = run_trading(CELL, load_config("v12_anchor_g8"), sig, None)
    assert not res.tranches, "a too-tight stop reached a fill"
    assert len(_rejects(res, "stop_too_tight")) == 1


def test_g8c_off_without_key():
    """Same tape under naiad_v0 (no min_stop_atr key): the fill happens —
    the guard is config-gated, pre-G8 configs replay unchanged."""
    sig = _scenario(60, [(5, 1, 99.9)], atr=0.4)
    res = run_trading(CELL, load_config("naiad_v0"), sig, None)
    assert len(res.tranches) == 1
    assert not _rejects(res, "stop_too_tight")


# ── G-8b — notional cap ───────────────────────────────────────────────────

def test_g8b_notional_cap_rejects_not_resizes():
    """Stop ~0.022 under fill (>= 0.5 x ATR 0.04 = 0.02, so G-8c passes):
    qty ~ 25/0.022 ~ 1,136, notional ~ 113.7k > 10 x 10k equity — REJECT,
    and no downsized tranche exists anywhere."""
    sig = _scenario(60, [(5, 1, 99.998)], atr=0.04)
    res = run_trading(CELL, load_config("v12_anchor_g8"), sig, None)
    assert not res.tranches, "notional-capped entry was resized into a fill"
    assert len(_rejects(res, "notional_cap")) == 1


def test_g8b_under_cap_fills():
    """Stop 0.25 under fill: qty 100, notional ~10k << 100k — fills."""
    sig = _scenario(60, [(5, 1, 99.77)], atr=0.4)
    res = run_trading(CELL, load_config("v12_anchor_g8"), sig, None)
    assert len(res.tranches) == 1
    assert not _rejects(res, "notional_cap")


# ── G-8a — equity floor ───────────────────────────────────────────────────

def _floor_breach():
    """PRIME fills ~100 units at bar 6 (stop 0.25 under fill), price gaps to
    10 at bar 8 -> gap-through loss ~ -9,008 -> equity ~992 < 2,500 floor.
    A second campaign PRIMEs 11 days later (stop 9.75, clean of the day/week
    halts tripped by the -180R loss), so the ONLY blocker is the floor."""
    return _scenario(LATE + 200, [(5, 1, 99.77), (LATE, 2, 9.75)],
                     gap_bar=8, gap_to=10.0)


def test_g8a_floor_halts_cell_permanently():
    res = run_trading(CELL, load_config("v12_anchor_g8"), _floor_breach(), None)
    assert len(res.tranches) == 1, "expected exactly the pre-breach fill"
    tr = res.tranches[0]
    assert tr.exited and tr.exit_reason == "stop_gap"
    assert tr.equity_after < 2500.0
    fl = [h for h in res.halts if h.scope == "equity_floor"]
    assert len(fl) == 1, "breach must record exactly one equity_floor HALT"
    assert fl[0].i == 8 and fl[0].r_total == tr.equity_after
    # the day-11 PRIME lands as a permanent-floor reject, not a fill
    assert len(_rejects(res, "equity_floor")) == 1
    assert not [t for t in res.tranches if t.fill_i > 8], \
        "a fill occurred after the equity_floor halt"


def test_g8a_off_without_key():
    """naiad_v0 (no equity_floor_frac): same crash, no floor halt, and the
    later PRIME trades again — pre-G8 behavior preserved under old configs."""
    res = run_trading(CELL, load_config("naiad_v0"), _floor_breach(), None)
    assert not [h for h in res.halts if h.scope == "equity_floor"]
    assert len(res.tranches) == 2, "old configs must keep trading (no floor)"


# ── G-8d — unit sanity assert ─────────────────────────────────────────────

def test_g8d_negative_one_r_raises():
    """naiad_v0, all G-8 keys absent: a 0.022-stop entry mints qty ~1,190 and
    a gap to 50 realizes ~ -59.6k (equity ~ -49.6k, the ZEC pathology's
    shape). The next sizing attempt 11 days later must raise GateViolation —
    a bankrupt cell can no longer mint negative-R tranches."""
    sig = _scenario(LATE + 200, [(5, 1, 99.999), (LATE, 2, 49.999)],
                    gap_bar=8, gap_to=50.0)
    with pytest.raises(GateViolation, match="G-8d"):
        run_trading(CELL, load_config("naiad_v0"), sig, None)


def test_g8d_unreachable_with_floor():
    """Same tape under v12_anchor_g8: G-8c rejects both too-tight stops, the
    crash never fills, equity never moves — no GateViolation reachable."""
    sig = _scenario(LATE + 200, [(5, 1, 99.999), (LATE, 2, 49.999)],
                    gap_bar=8, gap_to=50.0)
    res = run_trading(CELL, load_config("v12_anchor_g8"), sig, None)
    assert not res.tranches
    assert len(_rejects(res, "stop_too_tight")) == 2


# ── schema additions — additive only ──────────────────────────────────────

def test_fill_only_fields_additive():
    """make_row accepts the two 1.0.8 fill fields only when passed (absent
    otherwise, so non-fill rows keep the exact pre-1.0.8 key set) and still
    refuses unknown keys."""
    plain = make_row(evt="PRIME")
    assert "concurrent_open_at_fill" not in plain and "fill_class" not in plain
    fill = make_row(evt="ADD_FILL", concurrent_open_at_fill=1,
                    fill_class="true_add")
    assert fill["concurrent_open_at_fill"] == 1
    assert fill["fill_class"] == "true_add"
    with pytest.raises(KeyError):
        make_row(evt="EXIT", bogus_field=1)
