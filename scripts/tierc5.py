"""TIER-C5 · FULL-WATER TUNING RUN — seal open, shadow fleet, two registrations,
three labs.

RATIFIED operator 2026-08-16.  THE RULING, VERBATIM:

    "open the sealed box, we lose continuity otherwise… we will put it to paper
     trade the Prometheus route… another data stream"
    "D15 caveats not hard gates"

Drafted APOLLO · Executor HEPHAESTUS · Seed 20260816.

CLASS: measurement + PRE-REGISTERED CLAIMS + PRE-NAMED SHADOW GRIDS.  Every grid
reported WHOLE.  The guard is LOADED and IDLES.  THE SELECTION SURFACE IS LOGGED
— m per grid and m in total — because with a fleet on the table the honest thing
is not "we did not sweep", it is "here is exactly how many cells were available
to pick from, written down before anyone picked".

────────────────────────────────────────────────────────────────────────────
THE FORK IS AN IMPORT — FOUR GENERATIONS
────────────────────────────────────────────────────────────────────────────
`import tierc4_baseline as T4` (→ tierc3 → tierc2) for the loaders, the atomic
table writer, F-KEY, the headline aggregation, the monthly equity and the whole
Amendment-B1 tape.  `import tierc5_rules as RC` for the decision path.

THE CARD NAMED ONE FILE, `scripts/tierc5.py`, AND THIS BUILD SHIPS THREE.  The
reason is F-C5-6: the decision path must import no `analytics` member, and this
program must import several (resampling for the 12h/1d league, the tape).  One
file could not be both, so `tierc5_rules.py` holds the decision path and
`tierc5_fixtures.py` the transcript.  Named, not taken quietly.

────────────────────────────────────────────────────────────────────────────
WHAT IS IN-SAMPLE HERE, WHICH IS EVERYTHING
────────────────────────────────────────────────────────────────────────────
With the box open there is no held-out span left in the cache.  Every number in
this build — the card, both registrations, every shadow cell, all three labs —
is IN-SAMPLE BY CONSTRUCTION.  The out-of-sample role transfers FORWARD to live
paper on the Prometheus route (Stage-B interim).  Every headline row says so.

USAGE
    ~/venvs/naiad/bin/python scripts/tierc5.py
    ~/venvs/naiad/bin/python scripts/tierc5.py --rerun
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc4_baseline as T4                                        # noqa: E402
import tierc4_rules as V4                                           # noqa: E402
import tierc3_baseline as T3                                        # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import tierc5_rules as RC                                           # noqa: E402
import analytics as AN                                              # noqa: E402
from analytics import structure as AS                               # noqa: E402
from analytics import momentum as AM                                # noqa: E402
from analytics import volatility as AV                              # noqa: E402
from engine import indicators as ind                                # noqa: E402

# ── byte-inherited helpers ────────────────────────────────────────────────
_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key = TB.write_table, TB.assert_key
load_klines, load_funding = TB.load_klines, TB.load_funding
_idx_range = TB._idx_range
_maxdd_r, _top_decile_share = TB._maxdd_r, TB._top_decile_share
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D
KLINES = TB.KLINES
log, LOG_LINES = TB.log, TB.LOG_LINES

INHERITED_FROM_PARENTS = (
    "_ms", "iso", "r4", "r6", "pct", "write_table", "assert_key",
    "load_klines", "load_funding", "_idx_range", "_maxdd_r",
    "_top_decile_share", "daily_spine", "tape_rows", "ribbon_state",
    "tape_inventory", "build_level_series",
)

SEED = 20260816
OUT = ROOT / "research_outputs" / "tierc5"
OUT_RERUN = ROOT / "research_outputs" / "tierc5_run2"
V1_T, V3_T, V4_T = (ROOT / "research_outputs" / n
                    for n in ("tierc2", "tierc3", "tierc4"))

YARDSTICK_LABEL = ("YARDSTICK v5 — IN-SAMPLE BY CONSTRUCTION (the box is open; "
                   "out-of-sample transfers forward to live paper)")

# THE RESISTANCE LEAGUE and MID-BAND CONFLUENCE are Tier-E, and their window is
# the operator's, not the card's.
TIER_E_FROM = "2025-10-01"
LEAGUE_EMAS = (89, 127, 200, 300, 316, 423, 450, 500, 616, 889, 1272, 2618,
               3618, 4618, 5000)
LEAGUE_TFS = ("1h", "4h", "12h", "1d")
LEAGUE_APPROACH_ATR = 0.25      # "within 0.25 ATR from below"
LEAGUE_RESOLVE_BARS = 3         # "fails to close above within 3 bars"
LEAGUE_MIN_APPROACHES = 20      # a champion needs a population; pinned before the look
MIDBAND_CROSSES = (("89_127", 89, 127), ("127_316", 127, 316),
                   ("316_423", 316, 423))
MIDBAND_LEVELS = (127, 200, 300, 316, 423, 450)
MIDBAND_TFS = ("1h", "4h")
MIDBAND_H = (20, 100)
MIDBAND_NEAR_BARS = 6           # "co-occurrence within ±6 bars of v5 exits"


# ═══════════════════════════════════════════════════ frames, cached per asset
_FRAMES: dict[str, dict] = {}


def frame(sym: str) -> dict:
    """Everything the decision path reads for one asset, built once.

    Indicators are computed over the FULL loaded history and only then
    restricted, so a corridor edge can never move an EMA, an anchor or a trail.
    """
    if sym in _FRAMES:
        return _FRAMES[sym]
    k4 = load_klines(sym, "4h")
    f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                    k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                    k4["low"].to_numpy(float), k4["close"].to_numpy(float))
    _FRAMES[sym] = {
        "k4": k4, "f": f, "x": RC._crosses(f),
        "pv4": RC.build_pivots_4h(k4["high"].to_numpy(float),
                                  k4["low"].to_numpy(float)),
        "fund": load_funding(sym),
        "fractals": {}, "addctx": None,
    }
    return _FRAMES[sym]


def fractals(sym: str, L: int, R: int):
    st = frame(sym)
    key = (L, R)
    if key not in st["fractals"]:
        k4 = st["k4"]
        st["fractals"][key] = RC.build_fractals(
            k4["high"].to_numpy(float), k4["low"].to_numpy(float), L, R)
    return st["fractals"][key]


def addctx(sym: str):
    st = frame(sym)
    if st["addctx"] is None:
        st["addctx"] = RC.add_context(st["f"])
    return st["addctx"]


# ═══════════════════════════════════════════════════════════ THE CORRIDOR
def corridor() -> tuple[int, int, dict]:
    """Panel start → latest CLOSED 4h bar, one unbroken window.

    THE EDGE IS THE CACHE'S, AND THAT IS SAID OUT LOUD.  "Latest closed 4h bar
    at run time" is bounded by what the offline estate holds; this build makes
    no network call.  The manifest records both the corridor edge and the wall
    clock so the lag is a measured number rather than an impression.
    """
    lo = min(int(frame(s)["f"].open_ms[0]) for s in RC.UNIVERSE)
    hi_open = min(int(frame(s)["f"].open_ms[-1]) for s in RC.UNIVERSE)
    now = int(time.time() * 1000)
    meta = {
        "panel_start": iso(lo),
        "last_closed_4h_open": iso(hi_open),
        "last_closed_4h_close": iso(hi_open + MS_4H),
        "wall_clock_at_run": iso(now),
        "cache_lag_hours": round((now - (hi_open + MS_4H)) / 3_600_000.0, 2),
        "span_days": round((hi_open + MS_4H - lo) / MS_1D, 1),
        "per_asset_first_4h": {s: iso(int(frame(s)["f"].open_ms[0]))
                               for s in RC.UNIVERSE},
        "note": "the corridor END is the latest closed 4h bar PRESENT IN THE "
                "OFFLINE CACHE; this build makes no network call, so the lag "
                "against wall clock is disclosed rather than closed.",
    }
    return lo, hi_open + MS_4H - 1, meta


# ═══════════════════════════════════════════════════════════ THE RIDE
def _ride(sym: str, card: RC.Card, direction: int, ti: int, entry_px: float,
          stop0: float, r_dist: float, hi_i: int,
          test_stop_on_entry_bar: bool = False) -> dict:
    """ONE CODE PATH FOR EVERY CELL IN THE FLEET.

    Within-bar order, inherited from the card and adverse-first throughout:
        STOP → BELL → TIME STOP → HARVEST → ADDS → TRAIL
    The trail is last because its result governs the NEXT bar; the time stop is
    after the bell so a bell keeps the label when both would fire, which means a
    shadow clock only ever acts where the card would not have.

    WHAT WOULD MAKE THIS WRONG: a stop tested against the bar that created it, a
    harvest booked on a bar the stop already closed, an add entered after the
    exit, or a trail advance applied to its own bar.  F-C5-CTRL rides the v4
    settings through this same function and must reproduce Tier-C4's book
    trade-by-trade; a reordering here would break it.
    """
    st = frame(sym)
    f, x = st["f"], st["x"]
    fr = fractals(sym, card.trail_l, card.trail_r) if card.trail else None
    ctx = addctx(sym) if card.adds_max else None
    d = direction
    stop = float(stop0)
    advances: list = []
    harv = None
    blocked = ""
    mfe = float(entry_px)
    mae_to_1r = 0.0
    reached_1r = False
    trail_armed = card.trail_arm_after_r <= 0.0
    h_armed = False
    adds: list = []
    retraced = False
    exit_i, exit_px, exit_reason = hi_i, float(f.c[hi_i]), "corridor_end"

    # THE ENTRY BAR IS ONLY DEAD TIME WHEN THE ENTRY IS A CLOSE.
    # The card enters at a bar CLOSE, so after it there is no bar left and the
    # scan rightly starts at ti+1. A LIMIT fills mid-bar, and the remainder of
    # that bar is real tradeable time — discarding it silently gave every
    # S-LIMIT cell a free bar of immunity. Adverse-first [F-4] applies: if the
    # fill bar's own adverse extreme reached the new stop, the stop is taken on
    # that bar. Found by the post-build adversarial review.
    if test_stop_on_entry_bar:
        adv0 = float(f.l[ti]) if d == 1 else float(f.h[ti])
        if (d == 1 and adv0 <= stop) or (d == -1 and adv0 >= stop):
            return {"exit_i": ti, "exit_px": stop, "exit_reason": "stop",
                    "advances": [], "harvest": None, "blocked": "",
                    "mfe": float(entry_px), "adds": [], "final_stop": stop,
                    "mae_to_1r": None, "reached_1r": False}

    for j in range(ti + 1, hi_i + 1):
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        unit_fav_r = (fav - entry_px) * d / r_dist
        unit_adv_r = (adverse - entry_px) * d / r_dist

        # THE AE STUDY — deepest adverse from entry UNTIL +1R is first reached.
        if not reached_1r:
            mae_to_1r = min(mae_to_1r, unit_adv_r)
            if unit_fav_r >= 1.0:
                reached_1r = True
        if unit_fav_r >= card.trail_arm_after_r:
            trail_armed = True

        # harvest arming: the "from below" precondition, on the LAST CLOSED bar
        if card.harvest == "band":
            pe = RC.harvest_edge(float(f.e89[j - 1]), float(f.e316[j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(f.e89[j]), float(f.e316[j]), d)
            # THE IN-PROFIT GATE IS MEASURED AT THE FILL, NOT AT THE EXTREME.
            # The band harvest fills at the bar's CLOSE, so "fire only if the
            # unit move is >= X at the touch" has to be read at the close or it
            # is asking about a price the half never got. The card's own gate is
            # -inf (no minimum), which is v4 exactly; S-HARV sets +1R.
            unit_fill_r = (float(f.c[j]) - entry_px) * d / r_dist
            touch = (harv is None and h_armed
                     and RC.harvest_touched(float(f.h[j]), float(f.l[j]), edge, d)
                     and unit_fill_r >= card.harvest_min_unit_r)
        elif card.harvest == "fixed_r":
            edge = entry_px + d * card.harvest_fixed_r * r_dist
            touch = harv is None and unit_fav_r >= card.harvest_fixed_r
        else:
            edge, touch = float("nan"), False

        # 1 · ADVERSE FIRST — the stop takes the whole remainder
        if (d == 1 and f.l[j] <= stop) or (d == -1 and f.h[j] >= stop):
            exit_i, exit_px, exit_reason = j, stop, "stop"
            if touch:
                blocked = "stop"
            break
        if (fav - entry_px) * d > (mfe - entry_px) * d:
            mfe = fav                      # credited only for bars held THROUGH

        # 2 · the bell
        if d == 1:
            bell = ("bell_12_89" if bool(x["w_dn"][j])
                    else "bell_89_316" if bool(x["b_dn"][j]) else None)
        else:
            bell = ("bell_12_89" if bool(x["w_up"][j])
                    else "bell_89_316" if bool(x["b_up"][j]) else None)
        if bell:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), bell
            if touch:
                blocked = "bell"
            break

        # 3 · the shadow clock
        if card.time_stop_bars is not None and (j - ti) >= card.time_stop_bars:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "time_stop"
            if touch:
                blocked = "time_stop"
            break

        # 4 · the harvest
        if touch:
            fill = (RC.harvest_fill_px(f.c[j]) if card.harvest == "band"
                    else float(edge))          # a resting target fills AT target
            harv = (j, fill, (fill - entry_px) * d / r_dist)

        # 5 · the adds
        if ctx is not None and len(adds) < card.adds_max:
            if not retraced and RC.add_retraced(ctx, j, d, float(f.h[j]),
                                                float(f.l[j])):
                retraced = True
                retrace_i = j
            if retraced and RC.add_reclaimed(ctx, j, d, float(f.c[j])):
                adds.append(RC.Add(i=j, ms=int(f.open_ms[j]), px=float(f.c[j]),
                                   size=card.add_size, retrace_i=retrace_i,
                                   retrace_ms=int(f.open_ms[retrace_i])))
                retraced = False

        # 6 · the trail — governs bar j + 1
        if card.trail and trail_armed:
            adv = RC.trail_step(fr, j, d, stop, float(f.c[j]), float(f.atr[j]),
                                f.open_ms,
                                buf_atr=RC.RATCHET_BUF_ATR + card.trail_extra_buf_atr,
                                rail_atr=RC.RATCHET_RAIL_ATR,
                                forbidden=(None if card.seal_open
                                           else T3.sealed_mask(f.open_ms)))
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)

    return {"exit_i": exit_i, "exit_px": exit_px, "exit_reason": exit_reason,
            "advances": advances, "harvest": harv, "blocked": blocked,
            "mfe": mfe, "adds": adds, "final_stop": stop,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r}


def _account(sym: str, card: RC.Card, direction: int, ti: int, entry_px: float,
             r_dist: float, ride: dict) -> dict:
    """R accounting for a campaign: the base unit, its two halves, every add,
    and the D12 funding ceiling.

    WHAT WOULD MAKE THIS WRONG: halves that do not sum to the base leg, an add
    charged funding before it existed, or a ceiling applied to a funding CREDIT.
    The first is asserted at full precision below (it HALTs); the second and
    third are asserted by F-C5-ACCOUNT from raw funding stamps.
    """
    st = frame(sym)
    f, funding = st["f"], st["fund"]
    d, bps = direction, RC.FEE_BPS_SIDE / 10_000.0
    xi, xpx = ride["exit_i"], ride["exit_px"]
    harv = ride["harvest"]

    def fund_leg(lo_j: int, hi_j: int, qty: float) -> float:
        s = 0.0
        for j in range(lo_j + 1, hi_j + 1):
            rate = funding.get(int(f.open_ms[j]))
            if rate:
                s += rate * float(f.c[j - 1]) * d * qty
        return s

    q = RC.HARVEST_FRACTION
    if harv is None:
        g_base = (xpx - entry_px) * d
        f_base = bps * (entry_px + xpx)
        u_base = fund_leg(ti, xi, 1.0)
        n1 = n2 = None
        would_have = None
    else:
        hj, hpx, _ = harv
        g1 = q * (hpx - entry_px) * d
        fe1 = bps * q * (entry_px + hpx)
        u1 = fund_leg(ti, hj, q)
        g2 = (1.0 - q) * (xpx - entry_px) * d
        fe2 = bps * (1.0 - q) * (entry_px + xpx)
        u2 = fund_leg(ti, xi, 1.0 - q)
        g_base, f_base, u_base = g1 + g2, fe1 + fe2, u1 + u2
        n1, n2 = (g1 - fe1 - u1) / r_dist, (g2 - fe2 - u2) / r_dist
        # THE HARVEST-LAB's counterfactual: what the harvested half would have
        # booked had it ridden with the runner instead of being taken.
        gw = q * (xpx - entry_px) * d
        fw = bps * q * (entry_px + xpx)
        uw = fund_leg(ti, xi, q)
        would_have = (gw - fw - uw) / r_dist

    g_add = fe_add = u_add = 0.0
    for a in ride["adds"]:
        g_add += a.size * (xpx - a.px) * d
        fe_add += bps * a.size * (a.px + xpx)
        u_add += fund_leg(a.i, xi, a.size)

    gross = (g_base + g_add) / r_dist
    fee = (f_base + fe_add) / r_dist
    fund_raw = (u_base + u_add) / r_dist
    # ── D12 · THE FUNDING CEILING.  Cost only; a credit is never capped.
    cap = card.funding_ceiling_r
    fund_eff = min(fund_raw, cap) if (cap is not None and fund_raw > cap) else fund_raw
    net = gross - fee - fund_eff

    if n1 is not None and cap is None:
        base_net = (g_base - f_base - u_base) / r_dist
        if abs((n1 + n2) - base_net) > 1e-9:
            raise SystemExit(
                f"HALT: the halves do not book the base leg. {sym} {ti}: "
                f"{n1!r} + {n2!r} != {base_net!r}")
    return {"gross_r": gross, "fee_r": fee, "funding_r": fund_eff,
            "funding_r_uncapped": fund_raw,
            "funding_ceiling_bound": bool(cap is not None and fund_raw > cap),
            "net_r": net, "n1": n1, "n2": n2,
            "add_r": (g_add - fe_add - u_add) / r_dist if ride["adds"] else None,
            "harvest_ride_would_have_r": would_have}


# ═══════════════════════════════════════════════ THE LANES · card and spring
def card_candidates(sym: str, lo_i: int, hi_i: int) -> tuple[list, list]:
    """The v4 gate stack, unchanged — armings, tide, d, trigger.  Returns
    (armings, candidates) where a candidate is (trigger_bar, direction, arming)."""
    st = frame(sym)
    f, x = st["f"], st["x"]
    arms = RC.armings(sym, f, lo_i, hi_i)
    cands = []
    for a in arms:
        a.in_window = True
        a.entry_scored = False
        if not a.tide_ok:
            a.reject = "tide"
            continue
        if not a.d_ok:
            a.reject = "d"
            continue
        trig = x["t_up"] if a.direction == 1 else x["t_dn"]
        end = min(a.window_end_i, hi_i + 1)
        c = np.flatnonzero(trig[a.arm_i:end])
        if c.size == 0:
            a.reject = "no_trigger"
            continue
        ti = int(a.arm_i + c[0])
        a.trigger_i, a.trigger_ms = ti, int(f.open_ms[ti])
        cands.append((ti, a.direction, a))
    return arms, cands


def replay(sym: str, card: RC.Card, lo_ms: int, hi_ms: int,
           avg_ae_r: float | None = None) -> tuple[list, list]:
    """Ride one asset through one cell of the fleet.  Returns (armings, trades).

    ONE POSITION PER ASSET, across lanes.  For the union lane the card and the
    spring compete for the same slot in time order, which is the only reading
    under which "one position per asset" survives adding a second lane.
    """
    st = frame(sym)
    f = st["f"]
    lo_i, hi_i = _idx_range(f.open_ms, lo_ms, hi_ms)
    # THE WARM-UP FLOOR. `engine.indicators.ema` SEEDS at the series start, so
    # at bar 1 every EMA equals the first close and the tide/window gates are
    # evaluable and meaningless. Every parent corridor was warm by traversal;
    # the full-water one starts at bar 0 and is not. No arming before bar 316.
    lo_i = max(lo_i, RC.WARMUP_BARS)
    if hi_i < lo_i:
        return [], []

    arms, cands = ([], [])
    if card.lane in ("card", "union"):
        arms, cc = card_candidates(sym, lo_i, hi_i)
        cands += [(ti, d, "card", a, None) for ti, d, a in cc]
    if card.lane in ("spring", "union"):
        for sp in RC.spring_signals(f, lo_i, hi_i):
            cands.append((sp.reclaim_i, sp.direction, "spring", None, sp))
    cands.sort(key=lambda c: (c[0], -c[1], c[2]))

    trades: list = []
    open_until = -1
    for ti, d, kind, arm, sp in cands:
        if ti <= open_until:
            if arm is not None:
                arm.reject = "position_open"
            continue
        entry_px = float(f.c[ti])
        atr_sig = float(f.atr[ti])
        if not (np.isfinite(atr_sig) and atr_sig > 0):
            if arm is not None:
                arm.reject = "degenerate_R"
            continue
        if kind == "card":
            # THE SEAL, ANSWERED AT THE CALL SITE. The box is open, so the mask
            # is None — but the ARGUMENT is still here and `seal_open=False`
            # puts the old lockbox back, because F-C5-CTRL has to ride the v4
            # card exactly and a removed argument cannot be un-removed.
            forbid = None if card.seal_open else T3.sealed_mask(f.open_ms)
            stp = RC.struct_stop_4h(st["pv4"], ti, entry_px, d, atr_sig,
                                    min_stop_atr=card.entry_rail_atr,
                                    forbidden=forbid)
        else:
            stp = RC.spring_stop(sp, entry_px, atr_sig, card.entry_rail_atr)
        if stp is None:
            if arm is not None:
                arm.reject = "no_struct_anchor"
            continue
        if not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            if arm is not None:
                arm.reject = "degenerate_R"
            continue
        if arm is not None:
            arm.entered = True
            arm.reject = "entered"
            arm.entry_scored = True

        ride = _ride(sym, card, d, ti, entry_px, stp.stop_px, stp.r_dist, hi_i)
        open_until = ride["exit_i"]
        acc = _account(sym, card, d, ti, entry_px, stp.r_dist, ride)
        harv = ride["harvest"]
        anchor_ms = int(f.open_ms[stp.anchor_bar]) if stp.anchor_bar >= 0 else -1
        lb0, lb1 = _ms(RC.LOCKBOX_WAS[0]), _ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1
        trades.append(RC.Trade(
            symbol=sym, lane=kind, direction=d,
            arm_i=(arm.arm_i if arm is not None else sp.sweep_i),
            arm_ms=(arm.arm_ms if arm is not None else sp.sweep_ms),
            entry_i=ti, entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stp.stop_px, r_dist=stp.r_dist, anchor=stp.anchor,
            anchor_bar_ms=anchor_ms,
            anchor_was_sealed=bool(anchor_ms > 0 and lb0 <= anchor_ms <= lb1),
            atr_at_entry=atr_sig,
            disp_at_arming=(arm.disp if arm is not None else float("nan")),
            exit_i=ride["exit_i"], exit_ms=int(f.open_ms[ride["exit_i"]]),
            exit_px=ride["exit_px"], exit_reason=ride["exit_reason"],
            bars_held=ride["exit_i"] - ti, scored=True,
            advances=ride["advances"], final_stop_px=ride["final_stop"],
            stop_advanced_atr=((ride["final_stop"] - stp.stop_px) * d / atr_sig),
            ratchet_exit=bool(ride["exit_reason"] == "stop" and ride["advances"]
                              and abs(ride["final_stop"] - stp.stop_px) > 1e-12),
            harvested=harv is not None,
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=ride["blocked"],
            harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
            adds=ride["adds"], add_r=acc["add_r"], spring=sp,
            mfe_r=(ride["mfe"] - entry_px) * d / stp.r_dist,
            mae_to_1r_r=ride["mae_to_1r"], reached_1r=ride["reached_1r"],
            gross_r=acc["gross_r"], fee_r=acc["fee_r"],
            funding_r=acc["funding_r"],
            funding_r_uncapped=acc["funding_r_uncapped"],
            funding_ceiling_bound=acc["funding_ceiling_bound"],
            net_r=acc["net_r"], net_r_harvest_half=acc["n1"],
            net_r_runner_half=acc["n2"], net_r_bellonly=None))
    return arms, trades


def run_cell(card: RC.Card, lo_ms: int, hi_ms: int) -> list:
    """One cell of the fleet over the whole panel."""
    out = []
    for s in RC.UNIVERSE:
        _, t = replay(s, card, lo_ms, hi_ms)
        out += t
    return out


# ═══════════════════════════════════════════════════ headline + D15 columns
def agg(trades: list, label: str, key: str = "ALL", extra: dict | None = None
        ) -> dict:
    rs = [t.net_r for t in trades]
    row = {"group": label, "key": key, "n": len(rs),
           "net_r": r4(sum(rs)) if rs else None,
           "expectancy_r": r4(float(np.mean(rs))) if rs else None,
           "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
           "max_dd_r": r4(_maxdd_r([(t.exit_ms, t.symbol, t.net_r)
                                    for t in trades])) if rs else None,
           "top_decile_share_pct": _top_decile_share(rs) if rs else None,
           "best_r": r4(max(rs)) if rs else None,
           "strip_best_net_r": r4(sum(rs) - max(rs)) if rs else None,
           "gross_r": r4(sum(t.gross_r for t in trades)) if rs else None,
           "fee_r": r4(sum(t.fee_r for t in trades)) if rs else None,
           "funding_r": r4(sum(t.funding_r for t in trades)) if rs else None,
           "provisional": bool(len(rs) < RC.PROVISIONAL_MIN_N),
           "in_sample": True}
    if extra:
        row.update(extra)
    return row


def d15(cell: list, base: list) -> dict:
    """THE D15 DIAGNOSTIC COLUMNS — printed on every scored and shadow line,
    and NOT GATES.  The operator's word of record: "D15 caveats not hard gates".

    paired_delta_expectancy_r  mean over PAIRED campaigns (same asset+entry bar)
                               of cell − base.  Paired, because an unpaired
                               difference of means confounds the change with the
                               population it changed.
    tail_exit_ratio            cell top-decile winning mass ÷ base's.  A4-TRG's
                               shape for an ALTERNATIVE-EXIT arm: unbounded, no
                               pass bar, printed not judged.
    max_single_trade_delta_share  the largest |per-campaign Δ| as a share of
                               |Σ Δ|.  Near 1.0 means one trade IS the result.
    provisional                n < PROVISIONAL_MIN_N on this line.
    """
    bk = {(t.symbol, t.entry_ms): t.net_r for t in base}
    pairs = [(t.net_r, bk[(t.symbol, t.entry_ms)]) for t in cell
             if (t.symbol, t.entry_ms) in bk]
    deltas = [a - b for a, b in pairs]
    tot = sum(deltas)

    def decile_mass(ts):
        """MEAN of the top decile, not the SUM.

        A sum scales with the decile's COUNT, which is 0.1n — so a ratio of two
        sums over books of different size measures the trade count, not the
        tail. Harmless across the fleet (every cell has n = 199) and
        load-bearing on exactly the two rows where it is not: the registration
        arms. Found by the post-build adversarial review.
        """
        rs = sorted([t.net_r for t in ts], reverse=True)
        k = int(np.floor(0.10 * len(rs)))
        return (sum(rs[:k]) / k) if k >= 1 else None
    cm, bm = decile_mass(cell), decile_mass(base)
    return {
        "n_paired": len(pairs),
        "paired_delta_expectancy_r": r6(float(np.mean(deltas))) if deltas else None,
        "tail_exit_ratio": (r4(cm / bm) if (cm is not None and bm not in
                                            (None, 0)) else None),
        "max_single_trade_delta_share": (
            r4(max(abs(x) for x in deltas) / abs(tot))
            if deltas and abs(tot) > 1e-12 else None),
        "unpaired_cell_n": len(cell) - len(pairs),
        "unpaired_base_n": len(base) - len(pairs),
    }


# ═══════════════════════════════════════════════════════════════ THE SLICES
def slices_of(lo_ms: int, hi_ms: int) -> list[tuple[str, str, int, int]]:
    """Reported, never gated.  Per-year · pre/post 2024-07-01 · the operator's
    post-lockbox market-open read."""
    out = []
    y0 = int(iso(lo_ms)[:4])
    y1 = int(iso(hi_ms)[:4])
    for y in range(y0, y1 + 1):
        a, b = max(lo_ms, _ms(f"{y}-01-01")), min(hi_ms, _ms(f"{y+1}-01-01") - 1)
        if b > a:
            out.append(("year", str(y), a, b))
    wall = _ms("2024-07-01")
    out.append(("era", "pre-2024-07-01", lo_ms, min(hi_ms, wall - 1)))
    out.append(("era", "post-2024-07-01", max(lo_ms, wall), hi_ms))
    out.append(("operator", "post-lockbox refresh (2025-10-06→latest)",
                max(lo_ms, _ms("2025-10-06")), hi_ms))
    out.append(("operator", "the formerly SEALED span (2024-07-01→2025-10-05)",
                max(lo_ms, wall), min(hi_ms, _ms("2025-10-05") + MS_1D - 1)))
    return out


def tide_mix(lo_ms: int, hi_ms: int) -> dict:
    """Tide-regime mix over a slice: the share of panel 4h bars in an up-tide,
    a down-tide, or neither.  A slice's result is not readable without it — a
    9-of-11-shorts book in a down-tide era is a different object from the same
    book in a mixed one."""
    up = dn = neither = 0
    for s in RC.UNIVERSE:
        f = frame(s)["f"]
        a, b = _idx_range(f.open_ms, lo_ms, hi_ms)
        if b < a:
            continue
        e89, e316, c = f.e89[a:b + 1], f.e316[a:b + 1], f.c[a:b + 1]
        u = (e89 > e316) & (c > e316)
        d_ = (e89 < e316) & (c < e316)
        up += int(np.nansum(u))
        dn += int(np.nansum(d_))
        neither += int(len(c) - np.nansum(u) - np.nansum(d_))
    tot = up + dn + neither
    return {"bars": tot, "up_tide_pct": pct(up, tot),
            "down_tide_pct": pct(dn, tot), "no_tide_pct": pct(neither, tot)}


# ═══════════════════════════════════════════════════════════ THE AE STUDY
def ae_study(book: list, lo_ms: int, hi_ms: int) -> tuple[pd.DataFrame, float]:
    """S-LIMIT's first half: per WINNER, the deepest adverse excursion (in R)
    from entry until +1R is first reached.

    TWO POPULATIONS, SEPARATELY LABELLED, as commissioned:
      TC-BOOK       every winner in this build's v5 book on the full corridor
      CENSUS-ERA    the winners inside the census-scored era (panel start →
                    2024-06-30) — the era CENSUS-2A scored
    A NAMED READING: "census winners" is taken as THIS CARD's winners in that
    ERA, not CENSUS-2A's filed ride-only book, which rode a different card, a
    different ruler and a size-free denominator and is not comparable. The
    alternative reading is stated in the build document and not taken.
    """
    ceil_census = _ms("2024-07-01")
    rows = []
    for pop, sel in (("TC-BOOK", lambda t: True),
                     ("CENSUS-ERA", lambda t: t.entry_ms < ceil_census)):
        w = [t for t in book if t.net_r > 0 and sel(t) and t.reached_1r
             and t.mae_to_1r_r is not None]
        allw = [t for t in book if t.net_r > 0 and sel(t)]
        rows.append({
            "population": pop, "winners": len(allw),
            "winners_reaching_1r": len(w),
            "never_reached_1r": len(allw) - len(w),
            "mean_ae_r": r6(float(np.mean([-t.mae_to_1r_r for t in w]))) if w else None,
            "median_ae_r": r6(float(np.median([-t.mae_to_1r_r for t in w]))) if w else None,
            "p90_ae_r": r6(float(np.percentile([-t.mae_to_1r_r for t in w], 90))) if w else None,
            "max_ae_r": r6(float(np.max([-t.mae_to_1r_r for t in w]))) if w else None,
            "note": ("deepest adverse from entry until +1R first reached, in R; "
                     "winners that never reach +1R have no AE and are counted "
                     "apart, never imputed"),
        })
    d = pd.DataFrame(rows)
    avg = d.loc[d["population"] == "TC-BOOK", "mean_ae_r"].iloc[0]
    return d, float(avg if avg is not None else 0.0)


def limit_grid(book: list, avg_ae: float, levels=(0.5, 0.75, 1.0, 1.5, 2.0)
               ) -> pd.DataFrame:
    """S-LIMIT's second half: a limit `k × avg-AE` BEYOND the trigger close,
    stop 1R beyond the limit, per level.

    AN OVERLAY, NOT A RE-RUN, AND SAID SO.  Each level rides the MEAN CARD'S OWN
    campaign set: the limit is live from the bar after the trigger until the
    mean card's own exit instant, and a level that never fills books a MISS
    rather than freeing the slot for someone else.  Re-running occupancy would
    change the population and a miss rate over a population that moved is not a
    miss rate.

    THE SELECTION SURFACE IS ON THE FACE: `avg-AE` is fitted on the SAME BOOK
    these levels are then scored against.  That is in-sample twice over, it is
    logged in `selection_surface`, and no level may be promoted out of here
    without declaring its own m first.
    """
    rows = []
    for k in levels:
        filled, missed, ts = [], 0, []
        for t in book:
            st = frame(t.symbol)
            f = st["f"]
            d, ti = t.direction, t.entry_i
            lim = t.entry_px - d * k * avg_ae * t.r_dist
            fill_i = None
            for j in range(ti + 1, t.exit_i + 1):
                if (d == 1 and f.l[j] <= lim) or (d == -1 and f.h[j] >= lim):
                    fill_i = j
                    break
            if fill_i is None:
                missed += 1
                continue
            new_stop = lim - d * t.r_dist
            card = RC.Card(name=f"S-LIMIT {k}", grid="S-LIMIT")
            ride = _ride(t.symbol, card, d, fill_i, lim, new_stop, t.r_dist,
                         int(np.searchsorted(f.open_ms, f.open_ms[-1])),
                         test_stop_on_entry_bar=True)
            acc = _account(t.symbol, card, d, fill_i, lim, t.r_dist, ride)
            filled.append(acc["net_r"])
            ts.append((int(f.open_ms[ride["exit_i"]]), t.symbol, acc["net_r"]))
        n = len(filled)
        rows.append({
            "level_x_avg_ae": k,
            "limit_offset_r": r6(k * avg_ae),
            "campaigns_offered": len(book), "filled": n, "missed": missed,
            "miss_rate_pct": pct(missed, len(book)),
            "net_r": r4(sum(filled)) if n else None,
            "expectancy_r": r4(float(np.mean(filled))) if n else None,
            "win_rate_pct": pct(sum(1 for v in filled if v > 0), n),
            "max_dd_r": r4(_maxdd_r(ts)) if n else None,
            "best_r": r4(max(filled)) if n else None,
            "provisional": bool(n < RC.PROVISIONAL_MIN_N),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════ THE HARVEST-LAB
def harvest_lab(book: list, sl: list) -> pd.DataFrame:
    """Per campaign: what the harvest TOOK, what riding WOULD HAVE booked, and
    the delta — then aggregated by regime slice.  THE H1 EVIDENCE."""
    rows = []
    for t in book:
        if not t.harvested:
            continue
        took = float(t.net_r_harvest_half)
        would = float(t.harvest_ride_would_have_r)
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms, "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "harvest_ts": iso(int(t.harvest_ms)),
            "bars_after_entry": int(t.harvest_i - t.entry_i),
            "unit_move_at_harvest_r": r6(t.harvest_unit_move_r),
            "took_r": r6(took), "would_have_r": r6(would),
            "delta_r": r6(took - would),
            "harvest_helped": bool(took > would),
            "runner_half_r": r6(t.net_r_runner_half),
            "campaign_net_r": r6(t.net_r),
            "exit_reason": t.exit_reason,
        })
    per = pd.DataFrame(rows)
    if not len(per):
        return per
    agg_rows = []
    for kind, name, a, b in sl:
        m = per[(per["entry_ms"] >= a) & (per["entry_ms"] <= b)]
        if not len(m):
            continue
        agg_rows.append({
            "asset": "__SLICE__", "entry_ms": a, "entry_ts": f"{kind}:{name}",
            "direction": "", "harvest_ts": "",
            "bars_after_entry": len(m),
            "unit_move_at_harvest_r": r6(float(m["unit_move_at_harvest_r"].mean())),
            "took_r": r6(float(m["took_r"].sum())),
            "would_have_r": r6(float(m["would_have_r"].sum())),
            "delta_r": r6(float(m["delta_r"].sum())),
            "harvest_helped": bool(m["delta_r"].sum() > 0),
            "runner_half_r": r6(float(m["runner_half_r"].sum())),
            "campaign_net_r": r6(float(m["campaign_net_r"].sum())),
            "exit_reason": f"{int(m['harvest_helped'].sum())} of {len(m)} helped",
        })
    return pd.concat([per, pd.DataFrame(agg_rows)], ignore_index=True)


# ═══════════════════════════════════════════════ TIER-E · RESISTANCE LEAGUE
def _tf_frame(sym: str, tf: str) -> dict:
    """OHLC on a timeframe.  1h/4h/12h come from the cache as their own files;
    1d is RESAMPLED through `analytics.structure.resample_ohlcv`, which drops
    the forming bucket unconditionally (AMENDMENT FAN8) — so the last row is a
    finished day, never a fraction of one."""
    if tf == "1d":
        k = load_klines(sym, "1h")
        d = AS.resample_ohlcv(k["open_time"].to_numpy(np.int64),
                              k["open"].to_numpy(float), k["high"].to_numpy(float),
                              k["low"].to_numpy(float), k["close"].to_numpy(float),
                              k["volume"].to_numpy(float), MS_1D)
        return {"t": d["open_time"], "h": d["high"], "l": d["low"],
                "c": d["close"]}
    k = load_klines(sym, tf)
    return {"t": k["open_time"].to_numpy(np.int64), "h": k["high"].to_numpy(float),
            "l": k["low"].to_numpy(float), "c": k["close"].to_numpy(float)}


def resistance_league(hi_ms: int) -> pd.DataFrame:
    """THE LEAGUE TABLE.  Every EMA × every TF × every panel asset over
    2025-10-01 → latest.

    APPROACH   the bar's HIGH comes within LEAGUE_APPROACH_ATR of the EMA FROM
               BELOW (the previous bar closed below it), and the EMA is warm.
    REJECTION  no close above the EMA within LEAGUE_RESOLVE_BARS bars.
    PENETRATION the deepest close-above within that window, in ATR; 0 when none.
    STREAK     the longest run of consecutive approaches that were all rejected.

    WHAT WOULD MAKE THIS WRONG: an approach counted from above (it would measure
    support, not resistance), a rejection window that reads a bar the approach
    could not see, or an EMA read before it is warm.  F-C5-LEAGUE re-derives one
    row per timeframe from raw bars.
    """
    lo = _ms(TIER_E_FROM)
    rows = []
    for sym in RC.UNIVERSE:
        for tf in LEAGUE_TFS:
            d = _tf_frame(sym, tf)
            t, h, l_, c = d["t"], d["h"], d["l"], d["c"]
            a = ind.atr(h, l_, c, RC.ATR_LEN)
            m = (t >= lo) & (t <= hi_ms)
            if not m.any():
                continue
            i0, i1 = int(np.argmax(m)), int(len(t) - 1 - np.argmax(m[::-1]))
            for L in LEAGUE_EMAS:
                if len(c) < L + 5:
                    continue
                e = ind.ema(c, L)
                n_app = n_rej = 0
                pens, streak, best_streak = [], 0, 0
                for i in range(max(i0, L + 1), i1 + 1):
                    if not (np.isfinite(e[i]) and np.isfinite(a[i]) and a[i] > 0):
                        continue
                    if not (c[i - 1] < e[i - 1]):          # must come FROM BELOW
                        continue
                    if h[i] < e[i] - LEAGUE_APPROACH_ATR * a[i]:
                        continue                            # never got close
                    n_app += 1
                    w = slice(i, min(i + LEAGUE_RESOLVE_BARS + 1, i1 + 1))
                    above = c[w] > e[w]
                    pen = float(np.max((c[w] - e[w]) / a[i])) if len(c[w]) else 0.0
                    pens.append(max(pen, 0.0))
                    if not above.any():
                        n_rej += 1
                        streak += 1
                        best_streak = max(best_streak, streak)
                    else:
                        streak = 0
                if n_app:
                    rows.append({
                        "asset": sym, "tf": tf, "ema": L,
                        "approaches": n_app, "rejections": n_rej,
                        "rejection_rate_pct": pct(n_rej, n_app),
                        "mean_penetration_atr": r6(float(np.mean(pens))),
                        "longest_rejection_streak": int(best_streak),
                    })
    d = pd.DataFrame(rows)
    if not len(d):
        return d
    # THE PANEL ROW POOLS APPROACHES AND REJECTIONS, so its penetration must be
    # APPROACH-WEIGHTED too. An unweighted mean of five per-asset means sitting
    # beside a pooled count is two populations on one row. Found by the
    # post-build adversarial review.
    d["_pen_w"] = d["mean_penetration_atr"].astype(float) * d["approaches"]
    panel = (d.groupby(["tf", "ema"], as_index=False)
             .agg(approaches=("approaches", "sum"),
                  rejections=("rejections", "sum"),
                  _pen_w=("_pen_w", "sum"),
                  longest_rejection_streak=("longest_rejection_streak", "max")))
    panel["asset"] = "__PANEL__"
    panel["rejection_rate_pct"] = [pct(r_, a_) for r_, a_ in
                                   zip(panel["rejections"], panel["approaches"])]
    panel["mean_penetration_atr"] = [
        r6(w / a) if a else None
        for w, a in zip(panel["_pen_w"], panel["approaches"])]
    d = d.drop(columns=["_pen_w"])
    panel = panel.drop(columns=["_pen_w"])
    out = pd.concat([d, panel[d.columns]], ignore_index=True)
    out["eligible_for_champion"] = (
        (out["asset"] == "__PANEL__")
        & (out["approaches"] >= LEAGUE_MIN_APPROACHES))
    ch = out[out["eligible_for_champion"]]
    champs = {}
    for tf in LEAGUE_TFS:
        m = ch[ch["tf"] == tf]
        if len(m):
            champs[tf] = int(m.sort_values(
                ["rejection_rate_pct", "approaches"],
                ascending=[False, False]).iloc[0]["ema"])
    out["is_champion_wall"] = [
        bool(r_["asset"] == "__PANEL__" and champs.get(r_["tf"]) == r_["ema"])
        for _, r_ in out.iterrows()]
    # A NAMED MAXIMUM, NOT A PROMOTION, AND THE DISTINCTION IS ON THE ROW.
    # `is_champion_wall` is an argmax over the eligible panel cells for its
    # timeframe. It carries NO acceptance bar, NO interval and NO correction,
    # and the number of cells it was chosen from is stated so the selection
    # surface it implies is visible rather than implied. Found by the post-build
    # adversarial review, which pointed out that 54 eligible league cells were
    # absent from the logged surface while a champion was being named from them.
    out["champion_chosen_from_n_cells"] = [
        int(((out["asset"] == "__PANEL__") & out["eligible_for_champion"]
             & (out["tf"] == r_["tf"])).sum()) if r_["is_champion_wall"] else None
        for _, r_ in out.iterrows()]
    out["champion_is_a_named_maximum_not_a_promotion"] = [
        ("argmax of rejection_rate over the eligible panel cells for this TF; "
         "no acceptance bar, no CI, no multiplicity correction — it is the "
         "biggest number in a column, and that is all it is")
        if r_["is_champion_wall"] else None for _, r_ in out.iterrows()]
    return out


# ═══════════════════════════════════════════ TIER-E · MID-BAND CONFLUENCE
def midband(book: list, hi_ms: int) -> pd.DataFrame:
    """Crosses {89_127, 127_316, 316_423} and price↔{127,200,300,316,423,450}
    on {1h, 4h}: n, forward H20/H100 net of toll, and co-occurrence within ±6
    bars of a v5 EXIT ranked by that exit's quality.

    FORWARD RETURNS ARE DIRECTIONAL AND NET OF THE CARD'S OWN TOLL, so a number
    here is on the same footing as a card number: `(c[i+H] − c[i]) / c[i] × dir`
    minus the 10 bps round trip, expressed in bps.  No R denominator exists for
    an event that never became a trade, and inventing one would make these
    comparable to the book when they are not.
    """
    lo = _ms(TIER_E_FROM)
    exits = {}
    for t in book:
        exits.setdefault(t.symbol, []).append((t.exit_ms, t.net_r))
    rows = []
    toll_bps = RC.FEE_BPS_ROUND_TRIP
    for sym in RC.UNIVERSE:
        ex = sorted(exits.get(sym, []))
        ex_ms = np.array([e[0] for e in ex], np.int64)
        ex_r = np.array([e[1] for e in ex], float)
        for tf in MIDBAND_TFS:
            d = _tf_frame(sym, tf)
            t, c = d["t"], d["c"]
            step = MS_1H if tf == "1h" else MS_4H
            m = (t >= lo) & (t <= hi_ms)
            if not m.any():
                continue
            i0, i1 = int(np.argmax(m)), int(len(t) - 1 - np.argmax(m[::-1]))
            emas = {L: ind.ema(c, L) for L in
                    sorted(set([x for _, a, b in MIDBAND_CROSSES for x in (a, b)]
                               + list(MIDBAND_LEVELS)))}
            events: dict[str, list[tuple[int, int]]] = {}
            for name, a, b in MIDBAND_CROSSES:
                up = ind.crossover(emas[a], emas[b])
                dn = ind.crossunder(emas[a], emas[b])
                events[f"cross_{name}"] = (
                    [(int(i), 1) for i in np.flatnonzero(up) if i0 <= i <= i1]
                    + [(int(i), -1) for i in np.flatnonzero(dn) if i0 <= i <= i1])
            for L in MIDBAND_LEVELS:
                up = ind.crossover(c, emas[L])
                dn = ind.crossunder(c, emas[L])
                events[f"price_x_{L}"] = (
                    [(int(i), 1) for i in np.flatnonzero(up) if i0 <= i <= i1]
                    + [(int(i), -1) for i in np.flatnonzero(dn) if i0 <= i <= i1])
            for name, ev in events.items():
                if not ev:
                    continue
                fwd = {H: [] for H in MIDBAND_H}
                near, hit_idx = 0, set()
                for i, dirn in ev:
                    for H in MIDBAND_H:
                        if i + H <= i1:
                            fwd[H].append(
                                1e4 * (c[i + H] - c[i]) / c[i] * dirn - toll_bps)
                    if len(ex_ms):
                        w = MIDBAND_NEAR_BARS * step
                        k = np.flatnonzero(np.abs(ex_ms - int(t[i])) <= w)
                        if len(k):
                            near += 1
                            # DISTINCT EXITS, NOT EVENT-HITS. The first draft
                            # appended a per-event MEAN and then averaged over
                            # events and then over assets — a triple
                            # mean-of-means over a recycled handful of exits,
                            # published under a column name that claims a
                            # statistic over EXITS. Found by the post-build
                            # adversarial review. The set is the fix and the
                            # count is now a column, so the recycling is
                            # visible instead of invisible.
                            hit_idx.update(int(z) for z in k)
                near_r = [float(ex_r[z]) for z in sorted(hit_idx)]
                rows.append({
                    "asset": sym, "tf": tf, "event": name, "n": len(ev),
                    "h20_net_bps": r4(float(np.mean(fwd[20]))) if fwd[20] else None,
                    "h100_net_bps": r4(float(np.mean(fwd[100]))) if fwd[100] else None,
                    "h20_win_pct": pct(sum(1 for v in fwd[20] if v > 0), len(fwd[20])),
                    "h100_win_pct": pct(sum(1 for v in fwd[100] if v > 0), len(fwd[100])),
                    "coincident_event_hits": near,
                    "coincident_pct": pct(near, len(ev)),
                    "distinct_v5_exits_touched": len(near_r),
                    "mean_net_r_of_those_exits": r6(float(np.mean(near_r))) if near_r else None,
                })
    d = pd.DataFrame(rows)
    if not len(d):
        return d
    # THE PANEL ROW IS n-WEIGHTED. A pooled `n` beside an UNWEIGHTED mean of
    # per-asset means is two different populations on one row. Found by the
    # post-build adversarial review; the same defect is fixed in the league.
    def _wmean(g, col):
        v = g[col].astype(float)
        w = g["n"].astype(float)
        m = v.notna()
        return float((v[m] * w[m]).sum() / w[m].sum()) if m.any() and w[m].sum() else None

    panel = (d.groupby(["tf", "event"], as_index=False)
             .agg(n=("n", "sum"),
                  coincident_event_hits=("coincident_event_hits", "sum"),
                  distinct_v5_exits_touched=("distinct_v5_exits_touched", "sum")))
    for col in ("h20_net_bps", "h100_net_bps", "mean_net_r_of_those_exits"):
        panel[col] = [
            _wmean(d[(d["tf"] == r_["tf"]) & (d["event"] == r_["event"])], col)
            for _, r_ in panel.iterrows()]
    panel["asset"] = "__PANEL__"
    panel["h20_win_pct"] = None
    panel["h100_win_pct"] = None
    panel["coincident_pct"] = [pct(a, b) for a, b in
                               zip(panel["coincident_event_hits"], panel["n"])]
    for col in ("h20_net_bps", "h100_net_bps"):
        panel[col] = panel[col].map(r4)
    panel["mean_net_r_of_those_exits"] = panel["mean_net_r_of_those_exits"].map(r6)
    return pd.concat([d, panel[d.columns]], ignore_index=True)


# ═══════════════════════════════════════════════════════════ journal frames
def journal_frame(book: list) -> pd.DataFrame:
    rows = []
    for t in book:
        rows.append({
            "asset": t.symbol, "lane": t.lane, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
            "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
            "anchor": r6(t.anchor),
            "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
            "anchor_was_sealed_under_the_old_lockbox": bool(t.anchor_was_sealed),
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(t.atr_at_entry),
            "r_over_atr": r6(t.r_dist / t.atr_at_entry if t.atr_at_entry else None),
            "n_advances": len(t.advances),
            "final_stop_px": r6(t.final_stop_px),
            "stop_advanced_atr": r6(t.stop_advanced_atr),
            "ratchet_exit": bool(t.ratchet_exit),
            "harvested": bool(t.harvested),
            "harvest_ts": iso(int(t.harvest_ms)) if t.harvest_ms else None,
            "harvest_unit_move_r": r6(t.harvest_unit_move_r),
            "harvest_blocked_by": t.harvest_blocked_by or None,
            "net_r_harvest_half": r6(t.net_r_harvest_half),
            "net_r_runner_half": r6(t.net_r_runner_half),
            "harvest_ride_would_have_r": r6(t.harvest_ride_would_have_r),
            "n_adds": len(t.adds), "add_r": r6(t.add_r),
            "spring_sweep_ts": (iso(t.spring.sweep_ms) if t.spring else None),
            "spring_bars_to_reclaim": (t.spring.bars_to_reclaim if t.spring else None),
            "mfe_r": r6(t.mfe_r), "mae_to_1r_r": r6(t.mae_to_1r_r),
            "reached_1r": bool(t.reached_1r),
            "exit_ms": t.exit_ms, "exit_ts": iso(t.exit_ms),
            "exit_px": r6(t.exit_px), "exit_reason": t.exit_reason,
            "bars_held": t.bars_held,
            "gross_r": r6(t.gross_r), "fee_r": r6(t.fee_r),
            "funding_r": r6(t.funding_r),
            "funding_r_uncapped": r6(t.funding_r_uncapped),
            "funding_ceiling_bound": bool(t.funding_ceiling_bound),
            "net_r": r6(t.net_r),
        })
    return pd.DataFrame(rows)


def ratchet_ledger(book: list) -> pd.DataFrame:
    rows = []
    for t in book:
        for k, a in enumerate(t.advances):
            rows.append({
                "asset": t.symbol, "entry_ms": t.entry_ms, "advance_seq": k + 1,
                "direction": "long" if t.direction == 1 else "short",
                "conf_ts": iso(a.conf_ms), "governs_from_ts": iso(a.conf_ms + MS_4H),
                "pivot_val": r6(a.pivot_val), "pivot_bar_ts": iso(a.pivot_bar_ms),
                "atr_at_conf": r6(a.atr), "close_at_conf": r6(a.close),
                "cand_px": r6(a.cand_px), "rail_px": r6(a.rail_px),
                "prev_stop_px": r6(a.prev_stop), "new_stop_px": r6(a.new_stop),
                "advance_atr": r6(abs(a.new_stop - a.prev_stop) / a.atr),
                "rail_binding": bool(a.rail_binding),
                "dist_from_close_atr": r6(a.dist_from_close_over_atr),
                "bars_after_entry": a.conf_i - t.entry_i,
                "is_final_stop": bool(k == len(t.advances) - 1),
                "paid_out": bool(k == len(t.advances) - 1
                                 and t.exit_reason == "stop"),
            })
    return pd.DataFrame(rows)


# ═══════════════════════════════ THE REGISTRATIONS · text before result
REGISTRATIONS = {
    "P-SPR-1": {
        "prior_pct": 55,
        "text": ("THE SPRING LANE — sweep of prior 96x4h-bar extreme closing "
                 "back inside <=3 bars, tide-aligned, entry at reclaim close, "
                 "stop beyond sweep extreme railed 1.0, same trail/harvest/bell. "
                 "Scored standalone AND as card+spring union."),
        "ruler": ("THE REGISTRATION TEXT NAMES NO ACCEPTANCE BAR. The estate's "
                  "standing ruler for a panel claim is adopted and DECLARED "
                  "BEFORE THE RESULT: asset-cluster 90% bootstrap CI on the "
                  "expectancy (census2a_program.cluster_ci, the unit of "
                  "replication is the ASSET) excluding zero on the correct "
                  "side. BUILDER'S READING — the operator should confirm or "
                  "replace the bar; the builder will not word a bar it is also "
                  "scoring against and then call the wording ratified."),
        "arms": ("standalone = the spring lane alone; union = card+spring "
                 "competing for one position per asset"),
    },
    "P-CASC-1": {
        "prior_pct": 50,
        "text": ("CASCADE ADDS — retrace into MH-or-heavier band THEN close "
                 "back beyond the fast ribbon; <=2 adds/campaign; each add "
                 "stops with the campaign stop; 4h account. Scored as card+adds "
                 "vs card."),
        "ruler": ("Same adopted ruler, same disclosure: asset-cluster 90% CI on "
                  "the PAIRED per-campaign delta (card+adds minus card on the "
                  "same campaign) excluding zero above. Paired because the adds "
                  "cannot change which campaigns exist — they ride inside one."),
        "arms": "card+adds vs card, paired on (asset, entry bar)",
    },
}
FDR_FAMILY_M = len(REGISTRATIONS)
FDR_Q = 0.10


def cluster_ci(values, clusters, n_boot=4000, seed=SEED, stat="mean"):
    """The estate's asset-cluster bootstrap, imported rather than reimplemented.
    R-2: the unit of replication is the ASSET, not the row.

    stat="mean" IS DELIBERATE AND IS DECLARED BEFORE THE RESULT. The estate's
    default is "median" for returns, and its own note says why: a median on a
    0/1 indicator is degenerate. But BOTH registrations are worded about
    EXPECTANCY, and expectancy is a mean. Scoring an expectancy claim on a
    median would answer a question nobody registered — and on the union arm,
    whose paired deltas are mostly exactly zero by construction, a median CI
    collapses to [0, 0] and reports "NOT SUPPORTED" for an arithmetic reason
    rather than an evidential one. Mean it is, with the wider interval that
    heavy tails earn.
    """
    from census2a_program import cluster_ci as _cc
    return _cc(np.asarray(values, float), np.asarray(clusters),
               n_boot=n_boot, seed=seed, stat=stat)


def cluster_boot(values, clusters, seed=SEED, n_boot=4000):
    """Asset-cluster bootstrap draws of the MEAN — the raw draws, not a summary.

    `census2a_program.cluster_ci` returns an interval; the registrations need
    the interval AND the one-sided tail, and the tail is available from the very
    same draws. Returning them lets this build BH-correct a CI-scored
    registration instead of declaring the correction impossible — which the
    first draft of this file did, wrongly (finding F-C5-n).
    """
    v = np.asarray(values, float)
    c = np.asarray(clusters)
    uniq = np.unique(c)
    idx = {u: np.flatnonzero(c == u) for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        take = np.concatenate([idx[u] for u in pick])
        out[b] = float(np.mean(v[take])) if len(take) else np.nan
    return out


def cluster_boot_diff(va, ca, vb, cb, seed=SEED, n_boot=4000):
    """Two-sample asset-cluster bootstrap of (mean A − mean B), resampling the
    SAME asset draw into both arms.

    THIS IS THE RULER THE UNION ARM ALWAYS NEEDED. An arm named "vs card" must
    be tested against the card. The first draft tested the union's expectancy
    against ZERO, which is a different claim and — because the union's n is
    2.2x the card's — one the union can pass while being per-campaign WORSE
    than the thing it is named against. Found by the post-build adversarial
    review, twice, independently.
    """
    va, vb = np.asarray(va, float), np.asarray(vb, float)
    ca, cb = np.asarray(ca), np.asarray(cb)
    uniq = np.unique(np.concatenate([ca, cb]))
    ia = {u: np.flatnonzero(ca == u) for u in uniq}
    ib = {u: np.flatnonzero(cb == u) for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(n_boot)
    for b in range(n_boot):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        ta = np.concatenate([ia[u] for u in pick]) if len(pick) else np.array([], int)
        tb = np.concatenate([ib[u] for u in pick]) if len(pick) else np.array([], int)
        out[b] = ((float(np.mean(va[ta])) if len(ta) else np.nan)
                  - (float(np.mean(vb[tb])) if len(tb) else np.nan))
    return out


def _ci_from(draws, point):
    d = draws[np.isfinite(draws)]
    if not len(d):
        return {"point": None, "lo": None, "hi": None, "p_one_sided": None}
    return {"point": point, "lo": float(np.percentile(d, 5)),
            "hi": float(np.percentile(d, 95)),
            # one-sided bootstrap tail: P(draw <= 0), the probability the
            # effect is not positive. Directly comparable to a BH bar.
            "p_one_sided": float((np.sum(d <= 0) + 1) / (len(d) + 1))}


def score_registrations(base: list, spring: list, union: list, adds: list
                        ) -> pd.DataFrame:
    """FOUR ROWS, FOUR NAMED RULERS, AND THE CARD SCORED THROUGH THE SAME BAR.

    THE RULER IS NOT THE SAME FOR ALL, AND EVERY ROW SAYS WHICH IT USED.
      - a lane with its OWN campaigns and no twin is scored on its own
        expectancy against zero;
      - an arm named "vs card" is scored AGAINST THE CARD, by a two-sample
        asset-cluster bootstrap that resamples the same asset draw into both
        books — because "the union beats zero" and "the union beats the card"
        are different claims and the union can pass one while failing the other;
      - an arm that rides INSIDE the card's campaigns is scored on the PAIRED
        per-campaign delta.
    THE CARD ITSELF IS SCORED THROUGH THE FIRST RULER AND PRINTED AS A ROW, so
    a reader can see what the bar is worth before reading who cleared it.
    """
    rows = []

    def _row(reg, arm, prior, book, draws, point, ci_on, extra=None):
        ci = _ci_from(draws, point)
        rs = [t.net_r for t in book]
        good = bool(ci["lo"] is not None and ci["lo"] > 0)
        r = {"registration": reg, "arm": arm, "prior_pct": prior,
             "n": len(book),
             "expectancy_r": r6(float(np.mean(rs))) if rs else None,
             "net_r": r4(sum(rs)) if rs else None,
             "win_rate_pct": pct(sum(1 for x in rs if x > 0), len(rs)),
             "ci_on": ci_on, "ci_point": r6(ci["point"]),
             "ci_lo": r6(ci["lo"]), "ci_hi": r6(ci["hi"]),
             "p_one_sided": r6(ci["p_one_sided"]),
             "excludes_zero_above": good,
             "verdict": "SUPPORTED" if good else "NOT SUPPORTED",
             **d15(book, base),
             "provisional": bool(len(book) < RC.PROVISIONAL_MIN_N)}
        if extra:
            r.update(extra)
        rows.append(r)

    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]

    # ── ROW 0 · THE CARD, THROUGH THE SAME BAR ────────────────────────────
    _row("(reference)", "THE CARD v5, scored through the same ruler", 0, base,
         cluster_boot(bnet, bcl), float(np.mean(bnet)),
         "the card's OWN expectancy vs zero (asset-cluster 90% CI, mean). "
         "PRINTED FIRST ON PURPOSE: the bar every arm below is held to is one "
         "the CARD ITSELF does not clear, and a reader who does not know that "
         "cannot read the rest of this table")

    # ── P-SPR-1 (a) the spring lane alone, vs zero ────────────────────────
    sv = [t.net_r for t in spring]
    sc = [t.symbol for t in spring]
    _row("P-SPR-1", "standalone spring lane", 55, spring,
         cluster_boot(sv, sc), float(np.mean(sv)) if sv else None,
         "the lane's OWN expectancy vs zero — unpaired, because the spring "
         "lane's campaigns are not the card's and there is nothing to pair")

    # ── P-SPR-1 (b) the union, AGAINST THE CARD ───────────────────────────
    uv = [t.net_r for t in union]
    uc = [t.symbol for t in union]
    pt = float(np.mean(uv)) - float(np.mean(bnet))
    _row("P-SPR-1", "card+spring UNION vs card", 55, union,
         cluster_boot_diff(uv, uc, bnet, bcl), pt,
         "UNION EXPECTANCY MINUS CARD EXPECTANCY, two-sample asset-cluster 90% "
         "CI resampling the same asset draw into both books. The arm is named "
         "'vs card' so it is tested against the card. Scoring it against ZERO "
         "instead — as this build's first draft did — lets a book with 2.2x the "
         "campaigns pass on a narrower interval while being per-campaign WORSE "
         "than the thing it is named against",
         extra={"card_net_r_for_comparison": r4(sum(bnet)),
                "union_minus_card_net_r": r4(sum(uv) - sum(bnet)),
                "union_n_minus_card_n": len(union) - len(base),
                "union_minus_card_expectancy_r": r6(pt),
                "also_vs_zero_ci_lo": r6(_ci_from(cluster_boot(uv, uc),
                                                  float(np.mean(uv)))["lo"]),
                "also_vs_zero_verdict": (
                    "SUPPORTED against ZERO — and that is the WRONG BAR for an "
                    "arm named 'vs card'; printed so the two readings are on "
                    "one row and nobody has to take the builder's word for "
                    "which was used")})

    # ── P-CASC-1 · PAIRED ─────────────────────────────────────────────────
    bu = {(t.symbol, t.entry_ms): t.net_r for t in base}
    pairs = [(t, t.net_r - bu[(t.symbol, t.entry_ms)]) for t in adds
             if (t.symbol, t.entry_ms) in bu]
    pv = [d_ for _, d_ in pairs]
    pc = [t.symbol for t, _ in pairs]
    _row("P-CASC-1", "card+adds vs card (PAIRED)", 50, adds,
         cluster_boot(pv, pc), float(np.mean(pv)) if pv else None,
         "the PAIRED per-campaign delta vs zero (asset-cluster 90% CI, mean). "
         "Paired is correct here and only here: an add cannot create or destroy "
         "a campaign, it rides inside one, so every adds-campaign has exactly "
         "one card twin",
         extra={"paired_n": len(pairs),
                "paired_delta_r_total": r4(sum(pv)),
                "paired_delta_expectancy": r6(float(np.mean(pv))) if pv else None,
                "campaigns_with_at_least_one_add": sum(1 for t in adds if t.adds),
                "adds_total": sum(len(t.adds) for t in adds)})

    d = pd.DataFrame(rows)
    # ── BH, APPLIED — because the tail IS available from the same draws ───
    tested = d[d["registration"] != "(reference)"].copy()
    m = len(tested)
    bar = FDR_Q / m
    d["fdr_m_tests_actually_run"] = m
    d["fdr_q"] = FDR_Q
    d["fdr_bar_q_over_m"] = r6(bar)
    d["clears_bh_bar"] = [
        (None if r_["registration"] == "(reference)"
         else bool(r_["p_one_sided"] is not None and r_["p_one_sided"] <= bar))
        for _, r_ in d.iterrows()]
    d["fdr_note"] = (
        f"m = {m} — the number of ACCEPTANCE TESTS ACTUALLY RUN, not the number "
        f"of registrations filed. Two registrations produced three tests "
        f"(P-SPR-1 was scored twice), and a family that counts filings rather "
        f"than tests gives the second bite of the same apple a free pass. "
        f"q = {FDR_Q}, bar = q/m = {bar:.5f}. THE CORRECTION IS APPLIED, NOT "
        f"MERELY RECORDED: the same asset-cluster bootstrap that produces the "
        f"interval also produces the one-sided tail, so no p had to be "
        f"invented. This build's first draft claimed the opposite and was "
        f"wrong — finding F-C5-n.")
    d["in_sample"] = True
    return d


def registration_robustness(base: list, spring: list, union: list,
                            adds: list) -> pd.DataFrame:
    """THE THREE CHECKS A VERDICT ON AN INTERVAL HAS TO SURVIVE, RUN ON EVERY
    ARM WHETHER IT PASSED OR NOT — AND RUN THROUGH THE ARM'S OWN RULER.

    That last clause is not decoration.  The first draft of this block scored
    the union arm against ZERO while the verdict scored it against the CARD, so
    the robustness table and the verdict were answering different questions and
    the table would have "confirmed" a verdict it had never tested.  Each arm
    here is stressed with exactly the ruler its row was decided by.

    LEAVE-ONE-ASSET-OUT — a panel claim is a claim about REPLICATION.  Precedent:
      A4-WITCORR found P-REL-1b's "LOAO 4 of 5" overstated its replication.
    DROP THE LARGEST CAMPAIGN — a tail-heavy book can carry an interval on one
      trade.
    SEED SENSITIVITY — the ruler is a 4,000-draw bootstrap; a verdict on its
      fourth decimal could be a verdict about a seed.

    NONE IS A GATE. They are D15-class diagnostics — "caveats not hard gates" —
    printed beside the verdict, never in front of it.
    """
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    bu = {(t.symbol, t.entry_ms): t.net_r for t in base}
    pairs = [(t.symbol, t.net_r - bu[(t.symbol, t.entry_ms)]) for t in adds
             if (t.symbol, t.entry_ms) in bu]

    def _one_sample(vals, cls, keep=None, seed=SEED):
        if keep is not None:
            vals = [v for c, v in zip(cls, vals) if c in keep]
            cls = [c for c in cls if c in keep]
        if len(vals) < 8:
            return {}
        return _ci_from(cluster_boot(vals, cls, seed=seed), float(np.mean(vals)))

    def _two_sample(keep=None, seed=SEED):
        uv = [t.net_r for t in union]
        uc = [t.symbol for t in union]
        av, ac, bv, bc = uv, uc, bnet, bcl
        if keep is not None:
            av = [v for c, v in zip(uc, uv) if c in keep]
            ac = [c for c in uc if c in keep]
            bv = [v for c, v in zip(bcl, bnet) if c in keep]
            bc = [c for c in bcl if c in keep]
        if len(av) < 8 or len(bv) < 8:
            return {}
        return _ci_from(cluster_boot_diff(av, ac, bv, bc, seed=seed),
                        float(np.mean(av)) - float(np.mean(bv)))

    arms = [
        ("P-SPR-1", "standalone spring lane", "own expectancy vs zero",
         [t.symbol for t in spring], [t.net_r for t in spring], None),
        ("P-SPR-1", "card+spring UNION vs card",
         "UNION minus CARD expectancy (two-sample)", None, None, _two_sample),
        ("P-CASC-1", "card+adds vs card (PAIRED)", "paired delta vs zero",
         [c for c, _ in pairs], [v for _, v in pairs], None),
    ]
    rows = []
    for reg, arm, ruler, cls, vals, two in arms:
        def score(keep=None, seed=SEED):
            return two(keep, seed) if two else _one_sample(vals, cls, keep, seed)

        full = score()
        rows.append({"registration": reg, "arm": arm, "ruler": ruler,
                     "check": "FULL PANEL", "variant": "all 5 assets",
                     "n": (len(union) if two else len(vals)),
                     "point": r6(full.get("point")), "ci_lo": r6(full.get("lo")),
                     "ci_hi": r6(full.get("hi")),
                     "excludes_zero_above": bool(full.get("lo") is not None
                                                 and full["lo"] > 0)})
        n_excl = 0
        for drop in RC.UNIVERSE:
            keep = tuple(a for a in RC.UNIVERSE if a != drop)
            ci = score(keep)
            ex = bool(ci.get("lo") is not None and ci["lo"] > 0)
            n_excl += int(ex)
            rows.append({"registration": reg, "arm": arm, "ruler": ruler,
                         "check": "LEAVE-ONE-ASSET-OUT", "variant": f"drop {drop}",
                         "n": None, "point": r6(ci.get("point")),
                         "ci_lo": r6(ci.get("lo")), "ci_hi": r6(ci.get("hi")),
                         "excludes_zero_above": ex})
        rows.append({"registration": reg, "arm": arm, "ruler": ruler,
                     "check": "LEAVE-ONE-ASSET-OUT", "variant": "SUMMARY",
                     "n": None, "point": None, "ci_lo": None, "ci_hi": None,
                     "excludes_zero_above": None,
                     "loao_excluding_zero": f"{n_excl} of {len(RC.UNIVERSE)}"})
        if not two and vals is not None and len(vals) >= 9:
            k = int(np.argmax(np.abs(np.asarray(vals, float))))
            vv = [v for i_, v in enumerate(vals) if i_ != k]
            cc = [c for i_, c in enumerate(cls) if i_ != k]
            ci = _ci_from(cluster_boot(vv, cc), float(np.mean(vv)))
            rows.append({"registration": reg, "arm": arm, "ruler": ruler,
                         "check": "DROP THE LARGEST CAMPAIGN",
                         "variant": f"drop {vals[k]:+.4f} on {cls[k]}",
                         "n": len(vv), "point": r6(ci.get("point")),
                         "ci_lo": r6(ci.get("lo")), "ci_hi": r6(ci.get("hi")),
                         "excludes_zero_above": bool(ci.get("lo") is not None
                                                     and ci["lo"] > 0)})
        for sd in (SEED, 1, 42, 999, 123456):
            ci = score(seed=sd)
            rows.append({"registration": reg, "arm": arm, "ruler": ruler,
                         "check": "SEED SENSITIVITY", "variant": f"seed {sd}",
                         "n": None, "point": r6(ci.get("point")),
                         "ci_lo": r6(ci.get("lo")), "ci_hi": r6(ci.get("hi")),
                         "excludes_zero_above": bool(ci.get("lo") is not None
                                                     and ci["lo"] > 0)})
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════ THE SHADOW FLEET
# THE GRID SIZES, DECLARED AS A LITERAL AND INDEPENDENT OF THE CODE THAT BUILDS
# THE CELLS.  F-C5-GRID's first draft counted `fleet_cards()` on the declared
# side and `fleet_unscored` (written from the same list) on the written side —
# the same object counted twice, which is the pattern this build's own fixture
# preamble bans.  Now there are three independent things to agree: this literal,
# the cards the code builds, and the rows the table holds.
GRID_SIZES = {"card": 1, "S-RAIL": 2, "S-HARV": 2, "S-CLOCK": 2, "S-TRAIL": 3,
              "S-SIZE": 4, "S-ADDSIZE": 4, "S-LIMIT": 5, "registration arms": 3}


def fleet_cards() -> list[RC.Card]:
    """EVERY CELL, PRE-NAMED, BEFORE ANY OF THEM RAN.  Grids are declared here
    and their sizes are the SELECTION SURFACE that gets logged."""
    C = RC.Card
    out = [C(name="v5 (the card)", grid="card")]
    out += [C(name=f"S-RAIL {r}", grid="S-RAIL", entry_rail_atr=r)
            for r in (1.25, 1.5)]
    out += [C(name="S-HARV fixed +2R", grid="S-HARV", harvest="fixed_r",
              harvest_fixed_r=2.0),
            C(name="S-HARV in-profit-only (>=+1R)", grid="S-HARV",
              harvest_min_unit_r=1.0)]
    out += [C(name="S-CLOCK 60-bar time stop", grid="S-CLOCK",
              time_stop_bars=60),
            C(name="S-CLOCK no funding ceiling", grid="S-CLOCK",
              funding_ceiling_r=None)]
    out += [C(name="S-TRAIL (3,3) pivots", grid="S-TRAIL", trail_l=3, trail_r=3),
            C(name="S-TRAIL +0.25 ATR buffer", grid="S-TRAIL",
              trail_extra_buf_atr=0.25),
            C(name="S-TRAIL arms after +1R", grid="S-TRAIL",
              trail_arm_after_r=1.0)]
    return out


def size_grid(book: list, sizes=(1.0, 1.5, 2.0, 3.0), span_days: float = 1.0,
              funding_cap: float | None = RC.FUNDING_CEILING_R) -> pd.DataFrame:
    """S-SIZE.  RE-CAPPED PER SIZE, NOT SCALED FROM THE UNIT-1 BOOK.

    The first draft multiplied the unit-1 result by `s` and asserted exact
    linearity on the table's face.  That claim was FALSE IN GENERAL and the
    reason is v5's own new rule: **D12 caps a campaign's funding COST at an
    absolute 1R.**  Funding in R scales with the unit; the cap does not.  So
    multiplying a cap-applied book silently converts a 1R ceiling into an s×1R
    ceiling.  Found by the post-build adversarial review.  Each size is now
    re-accounted per campaign from `gross`, `fee` and the UNCAPPED funding.

    THE LINEAR-SCALING CAVEAT REMAINS ON THE TABLE'S FACE, and it is now a
    measured claim rather than an assumed one: the `ceiling_bound_n` column says
    how many campaigns the cap actually caught at each size, so a reader can see
    for themselves whether linearity held.  What is genuinely NOT linear is
    `max_concurrent_campaigns` — a property of the calendar. A real book with
    margin, liquidation and compounding would not scale linearly either, and
    this table does not claim it would.
    """
    iv = sorted([(t.entry_ms, t.exit_ms) for t in book])
    pts = sorted([(a, 1) for a, _ in iv] + [(b, -1) for _, b in iv])
    cur = mx = 0
    for _, delta in pts:
        cur += delta
        mx = max(mx, cur)
        cur = max(cur, 0)
    years = span_days / 365.25
    rows = []
    for s in sizes:
        nets, bound = [], 0
        for t in book:
            raw = float(t.funding_r_uncapped) * s
            capped = (min(raw, funding_cap) if (funding_cap is not None
                                                and raw > funding_cap) else raw)
            bound += int(funding_cap is not None and raw > funding_cap)
            nets.append((t.gross_r - t.fee_r) * s - capped)
        net = sum(nets)
        dd = _maxdd_r([(t.exit_ms, t.symbol, n_)
                       for t, n_ in zip(book, nets)])
        rows.append({
            "unit": s, "n": len(book),
            "net_r": r4(net), "max_dd_r": r4(dd),
            "expectancy_r": r4(net / len(book)) if book else None,
            "ceiling_bound_n": bound,
            "max_concurrent_campaigns": mx,
            "max_concurrent_exposure_units": r4(mx * s),
            "net_r_per_year": r4(net / years) if years else None,
            "return_over_maxdd": r4(net / dd) if dd else None,
            "linear_scaling_caveat": (
                "RE-CAPPED PER SIZE, not scaled: D12 caps funding COST at an "
                "absolute 1R, which does NOT scale with the unit, so a scaled "
                "book would have silently carried an s x 1R ceiling. "
                "`ceiling_bound_n` says how often the cap actually caught. No "
                "equity feedback, no margin, no liquidation, no compounding — "
                "this is not a leverage study."),
        })
    return pd.DataFrame(rows)


def addsize_grid(lo_ms: int, hi_ms: int, base: list,
                 sizes=(1.0, 1.5, 2.0, 3.0)) -> pd.DataFrame:
    """S-ADDSIZE — the add tranche, on the P-CASC line, ridden for real (an add
    changes the ride's accounting, so unlike S-SIZE it cannot be scaled on
    paper)."""
    rows = []
    for s in sizes:
        card = RC.Card(name=f"S-ADDSIZE {s}x", grid="S-ADDSIZE",
                       adds_max=RC.ADDS_MAX, add_size=s)
        bk = run_cell(card, lo_ms, hi_ms)
        rs = [t.net_r for t in bk]
        rows.append({
            "add_tranche_x_base": s, "n": len(bk),
            "campaigns_with_adds": sum(1 for t in bk if t.adds),
            "adds_total": sum(len(t.adds) for t in bk),
            "net_r": r4(sum(rs)) if rs else None,
            "expectancy_r": r4(float(np.mean(rs))) if rs else None,
            "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
            "max_dd_r": r4(_maxdd_r([(t.exit_ms, t.symbol, t.net_r) for t in bk])),
            "add_r_total": r4(sum(t.add_r for t in bk if t.add_r is not None)),
            **d15(bk, base),
            "provisional": bool(len(bk) < RC.PROVISIONAL_MIN_N),
        })
    return pd.DataFrame(rows)


def control_v4() -> list:
    """F-C5-CTRL — the v4 card, ridden through the v5 code path.

    Everything v4 had and v5 changed is put back: the SEAL is closed, the
    FUNDING CEILING is off, the corridor is v4's 118 days, and armings are
    admitted from 30 days before it (v4's F-5 lead-in) while only in-window
    ENTRIES are scored.  What comes out must be Tier-C4's filed book, campaign
    for campaign.

    WHAT WOULD MAKE THIS FAIL: any reordering inside `_ride`, any change to the
    entry gates, the anchor, the rail, the trail, the harvest or the accounting.
    It is the single test that the fork did not drift, and every fleet number in
    this build is worth exactly what it is worth.
    """
    lo, hi = _ms("2025-10-06"), _ms("2026-01-31") + MS_1D - 1
    card = RC.Card(name="F-C5-CTRL (v4)", grid="control",
                   funding_ceiling_r=None, seal_open=False)
    out = []
    for s in RC.UNIVERSE:
        _, t = replay(s, card, lo - 30 * MS_1D, hi)
        out += [x for x in t if x.entry_ms >= lo]
    out.sort(key=lambda t: (t.symbol, t.entry_ms))
    return out


# ═══════════════════════════════════════════════════════════════ the driver
def run(root: Path) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "card": "TIER-C5 · FULL-WATER",
                 "yardstick_label": YARDSTICK_LABEL, "sha": {}, "counts": {},
                 "ruling_verbatim": RC.THE_RULING}
    log("=" * 78)
    log("TIER-C5 · FULL-WATER TUNING RUN — the box is open")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")
    log(f"  seed {SEED} · universe {', '.join(RC.UNIVERSE)}")
    log(f"  RULING: {RC.THE_RULING}")

    lo_ms, hi_ms, cmeta = corridor()
    man["corridor"] = cmeta
    log(f"  CORRIDOR {cmeta['panel_start']} -> {cmeta['last_closed_4h_close']} "
        f"({cmeta['span_days']} d) · cache lag {cmeta['cache_lag_hours']} h")

    # ── THE SEAL, OPENED AND RECORDED ─────────────────────────────────────
    lb0, lb1 = _ms(RC.LOCKBOX_WAS[0]), _ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1
    n_bars_freed = 0
    first_freed = None
    for s in RC.UNIVERSE:
        ot = frame(s)["f"].open_ms
        m = (ot >= lb0) & (ot <= lb1)
        n_bars_freed += int(m.sum())
        if m.any():
            b = int(ot[m][0])
            first_freed = b if first_freed is None else min(first_freed, b)
    man["seal"] = {
        "state": "OPEN", "ruling": RC.THE_RULING,
        "was": {"from": RC.LOCKBOX_WAS[0], "to": RC.LOCKBOX_WAS[1]},
        "mask_returns_true_anywhere": bool(
            any(RC.sealed_mask(frame(s)["f"].open_ms).any() for s in RC.UNIVERSE)),
        "formerly_sealed_4h_bars_now_readable": n_bars_freed,
        "earliest_formerly_sealed_bar": iso(first_freed) if first_freed else None,
    }
    log(f"  SEAL OPEN — {n_bars_freed:,} formerly-sealed 4h bars now readable, "
        f"earliest {man['seal']['earliest_formerly_sealed_bar']}")

    # ── THE GUARD, LOADED AND IDLE; THE SELECTION SURFACE, LOGGED ─────────
    from census2a_program import selection_guard
    guard = selection_guard([])
    cards = fleet_cards()
    built = {}
    for c in cards:
        built[c.grid] = built.get(c.grid, 0) + 1
    for g, n_ in built.items():
        if GRID_SIZES.get(g) != n_:
            raise SystemExit(
                f"HALT: grid '{g}' declares {GRID_SIZES.get(g)} cells in "
                f"GRID_SIZES and fleet_cards() built {n_}. The declaration and "
                f"the construction must agree BEFORE anything runs, or the "
                f"selection surface is a number the code derived from itself.")
    surface = dict(GRID_SIZES)
    total_m = sum(v for k, v in surface.items() if k != "card")
    man["selection_guard"] = {
        "loaded": True, "called": True, "candidates": 0, "verdict": guard,
        "why": "no cell is promoted; the guard has nothing to correct."}
    man["selection_surface"] = {
        "per_grid": surface, "total_cells_excluding_the_card": total_m,
        "fdr_family_for_the_two_registrations": FDR_FAMILY_M,
        "statement": ("EVERY GRID WAS NAMED BEFORE IT RAN AND EVERY CELL IS "
                      "REPORTED. Nothing here is promoted. This number is "
                      "written down so that a future promotion out of these "
                      "tables starts from an m that existed BEFORE the look — "
                      "which is the only thing that makes a later correction "
                      "meaningful."),
    }
    log(f"  GUARD idle (m={guard['m']}) · SELECTION SURFACE "
        f"{total_m} shadow cells across {len(surface)-1} pre-named grids")
    log("")

    # ── THE CARD ──────────────────────────────────────────────────────────
    arms_all, base = [], []
    for s in RC.UNIVERSE:
        a, t = replay(s, RC.V5, lo_ms, hi_ms)
        arms_all += a
        base += t
        log(f"    {s:9} armings={len(a):5d}  campaigns={len(t):5d}  "
            f"advances={sum(len(x.advances) for x in t):6d}  "
            f"harvests={sum(1 for x in t if x.harvested):5d}")
    base.sort(key=lambda t: (t.entry_ms, t.symbol))
    log(f"  v5 BOOK: {len(base)} campaigns, net R "
        f"{sum(t.net_r for t in base):+.4f}")
    log("")

    # ── tables ────────────────────────────────────────────────────────────
    root.mkdir(parents=True, exist_ok=True)
    # THE WALL CLOCK STAYS OUT OF THE WRITTEN TABLE. `wall_clock_at_run` and
    # `cache_lag_hours` are true and useful and belong in the manifest, where
    # F-C5-DET normalises them by name — but a table that carries them can
    # never be hash-identical across two runs, and determinism that has to be
    # excused is not determinism. The corridor's own EDGES are in the table and
    # are compared.
    cstruct = {k: v for k, v in cmeta.items()
               if k not in ("wall_clock_at_run", "cache_lag_hours")}
    man["sha"]["corridor"] = write_table(
        pd.DataFrame([{**cstruct, **man["seal"], "label": YARDSTICK_LABEL}]),
        "corridor_and_seal", [], root)

    fn = T3.funnel_table(arms_all)
    man["sha"]["funnel"] = write_table(fn, "funnel", ["asset", "direction"], root)

    head = pd.DataFrame([agg(base, "ALL", "ALL")]
                        + [agg([t for t in base if t.symbol == s], "asset", s)
                           for s in RC.UNIVERSE]
                        + [agg([t for t in base if t.direction == d], "direction", n)
                           for d, n in ((1, "long"), (-1, "short"))]
                        + [agg([t for t in base if t.exit_reason == r],
                               "exit_reason", r)
                           for r in ("stop", "bell_12_89", "bell_89_316",
                                     "time_stop", "corridor_end")])
    head.insert(0, "label", YARDSTICK_LABEL)
    man["sha"]["headline"] = write_table(head, "headline", ["group", "key"], root)

    sl = slices_of(lo_ms, hi_ms)
    srows, lrows = [], []
    for kind, name, a, b in sl:
        inn = [t for t in base if a <= t.entry_ms <= b]
        across = [t for t in base if t.entry_ms < a <= t.exit_ms]
        mix = tide_mix(a, b)
        srows.append({**agg(inn, kind, name), "slice_from": iso(a),
                      "slice_to": iso(b), "days": round((b - a) / MS_1D, 1),
                      **mix,
                      "counted_open_across_left_edge": len(across),
                      "d13c": ("campaigns open across this slice's left edge are "
                               "COUNTED here and SCORED only in the slice they "
                               "ENTERED in — both books printed")})
        for t in across:
            lrows.append({"slice": f"{kind}:{name}", "asset": t.symbol,
                          "entry_ts": iso(t.entry_ms), "exit_ts": iso(t.exit_ms),
                          "direction": "long" if t.direction == 1 else "short",
                          "bars_held": t.bars_held,
                          "outcome": "NOT SCORED IN THIS SLICE [D13(c)] — "
                                     "counted as occupancy only"})
    man["sha"]["by_slice"] = write_table(pd.DataFrame(srows), "headline_by_slice",
                                         ["group", "key"], root)
    man["sha"]["d13c"] = write_table(
        pd.DataFrame(lrows), "d13c_counted_not_scored",
        ["slice", "asset", "entry_ts"] if lrows else [], root)

    jr = journal_frame(base)
    man["sha"]["journal"] = write_table(jr, "trade_journal",
                                        ["asset", "entry_ms"], root)
    rl = ratchet_ledger(base)
    man["sha"]["ratchet"] = write_table(
        rl, "ratchet_ledger", ["asset", "entry_ms", "advance_seq"] if len(rl) else [],
        root)

    # ── the registrations ─────────────────────────────────────────────────
    log("  ── REGISTRATIONS")
    spring = run_cell(RC.Card(name="spring", grid="P-SPR-1", lane="spring"),
                      lo_ms, hi_ms)
    # THE NAMED READING, COUNTED ACROSS THE WHOLE PANEL. `spring_signals`
    # records the refusals of its LAST call; summing per asset here is what
    # makes the number a panel fact rather than ZEC's fact.
    spring_tide_refused = 0
    for s_ in RC.UNIVERSE:
        f_ = frame(s_)["f"]
        a_, b_ = _idx_range(f_.open_ms, lo_ms, hi_ms)
        RC.spring_signals(f_, a_, b_)
        spring_tide_refused += int(getattr(RC.spring_signals,
                                           "last_tide_rejected", 0))
    union = run_cell(RC.Card(name="union", grid="P-SPR-1", lane="union"),
                     lo_ms, hi_ms)
    adds = run_cell(RC.Card(name="adds", grid="P-CASC-1", adds_max=RC.ADDS_MAX),
                    lo_ms, hi_ms)
    reg = score_registrations(base, spring, union, adds)
    for _, r in reg.iterrows():
        log(f"    {r['registration']:10} {r['arm']:34} n={r['n']:5d} "
            f"exp={r['expectancy_r']} CI=[{r['ci_lo']},{r['ci_hi']}] "
            f"-> {r['verdict']}")
    man["sha"]["registrations"] = write_table(reg, "registrations",
                                              ["registration", "arm"], root)
    rb = registration_robustness(base, spring, union, adds)
    man["sha"]["reg_robust"] = write_table(
        rb, "registration_robustness", ["registration", "arm", "check", "variant"],
        root)
    for reg, arm in rb[["registration", "arm"]].drop_duplicates().itertuples(index=False):
        m_ = rb[(rb["registration"] == reg) & (rb["arm"] == arm)
                & (rb["variant"] == "SUMMARY")]
        if len(m_):
            log(f"    LOAO {reg:10} {arm:34} "
                f"{m_.iloc[0]['loao_excluding_zero']} panels exclude zero")
    man["sha"]["reg_text"] = write_table(
        pd.DataFrame([{"registration": k, **v} for k, v in REGISTRATIONS.items()]),
        "registration_text", ["registration"], root)

    # ── the fleet ─────────────────────────────────────────────────────────
    log("  ── THE SHADOW FLEET")
    frows = []
    for c in cards:
        bk = base if c.grid == "card" else run_cell(c, lo_ms, hi_ms)
        rs = [t.net_r for t in bk]
        frows.append({
            "grid": c.grid, "cell": c.name, "diff_from_v5": c.diff_from_v5(),
            "n": len(bk), "net_r": r4(sum(rs)) if rs else None,
            "expectancy_r": r4(float(np.mean(rs))) if rs else None,
            "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
            "max_dd_r": r4(_maxdd_r([(t.exit_ms, t.symbol, t.net_r) for t in bk])),
            "top_decile_share_pct": _top_decile_share(rs) if rs else None,
            "best_r": r4(max(rs)) if rs else None,
            "strip_best_net_r": r4(sum(rs) - max(rs)) if rs else None,
            "median_bars_held": r4(float(np.median([t.bars_held for t in bk]))) if bk else None,
            "advances": sum(len(t.advances) for t in bk),
            "harvests": sum(1 for t in bk if t.harvested),
            "funding_ceiling_bound_n": sum(1 for t in bk if t.funding_ceiling_bound),
            **d15(bk, base),
            "provisional": bool(len(bk) < RC.PROVISIONAL_MIN_N),
            "in_sample": True,
        })
        log(f"    {c.grid:10} {c.name:32} n={len(bk):5d} "
            f"netR={sum(rs):+10.4f} exp={np.mean(rs) if rs else 0:+.4f}")
    man["sha"]["fleet"] = write_table(pd.DataFrame(frows), "fleet_unscored",
                                      ["grid", "cell"], root)

    # ── the labs ──────────────────────────────────────────────────────────
    log("  ── THE LABS")
    hl = harvest_lab(base, sl)
    man["sha"]["harvest_lab"] = write_table(
        hl, "harvest_lab",
        ["asset", "entry_ms", "entry_ts"] if len(hl) else [], root)

    ae, avg_ae = ae_study(base, lo_ms, hi_ms)
    man["sha"]["ae"] = write_table(ae, "ae_study", ["population"], root)
    log(f"    AE study: mean adverse-to-+1R on the TC book = {avg_ae:.6f} R")
    lg = limit_grid(base, avg_ae)
    man["sha"]["limit"] = write_table(lg, "limit_grid", ["level_x_avg_ae"], root)

    man["sha"]["size"] = write_table(
        size_grid(base, span_days=cmeta["span_days"]), "size_grid", ["unit"], root)
    man["sha"]["addsize"] = write_table(
        addsize_grid(lo_ms, hi_ms, base), "addsize_grid",
        ["add_tranche_x_base"], root)

    league = resistance_league(hi_ms)
    man["sha"]["league"] = write_table(league, "resistance_league",
                                       ["asset", "tf", "ema"], root)
    # THE LEAGUE'S OWN SELECTION SURFACE, ADDED TO THE LOG.
    # A champion wall is an argmax, and an argmax over cells that are not in the
    # surface is a promotion nobody counted. The eligible cells go in the log.
    n_elig = int(((league["asset"] == "__PANEL__")
                  & league["eligible_for_champion"]).sum())
    man["selection_surface"]["per_grid"]["LEAGUE eligible panel cells"] = n_elig
    man["selection_surface"]["total_cells_excluding_the_card"] += n_elig
    man["selection_surface"]["league_note"] = (
        f"{n_elig} eligible panel cells across {len(LEAGUE_TFS)} timeframes. "
        f"The champion wall named per timeframe is an ARGMAX over these, with "
        f"no acceptance bar, no interval and no multiplicity correction. It is "
        f"the biggest number in a column and the build says so on the row.")
    mb = midband(base, hi_ms)
    man["sha"]["midband"] = write_table(mb, "midband_confluence",
                                        ["asset", "tf", "event"], root)

    # ── the tape ──────────────────────────────────────────────────────────
    tape_frames = []
    for s in RC.UNIVERSE:
        st = frame(s)
        k4 = st["k4"]
        inst = []
        for a in arms_all:
            if a.symbol != s:
                continue
            inst.append((a.arm_ms, "arming"))
            if a.trigger_ms is not None:
                inst.append((a.trigger_ms, "trigger"))
        for t in base:
            if t.symbol != s:
                continue
            inst.append((t.exit_ms, "exit"))
            if t.harvested:
                inst.append((int(t.harvest_ms), "harvest"))
        ot = st["f"].open_ms
        # WEEKLY spine, not daily: the corridor is ~21x longer than Tier-C4's,
        # and a daily spine would put ~63k rows on a table nothing reads back.
        # The change is one rule and it is stated rather than tuned.
        wk = [int(v) for v in ot if lo_ms <= v <= hi_ms and v % (7 * MS_1D) == 0]
        inst += [(v, "spine") for v in wk]
        order = {"arming": 0, "trigger": 1, "exit": 2, "harvest": 3, "spine": 4}
        seen: dict[int, str] = {}
        for ts, kind in sorted(inst, key=lambda p: (p[0], order[p[1]])):
            seen.setdefault(int(ts), kind)
        tp = TB.tape_rows(s, k4, load_klines(s, "1h"), sorted(seen.items()),
                          "FULL_WATER")
        if len(tp):
            tape_frames.append(tp)
    if tape_frames:
        tape = pd.concat(tape_frames, ignore_index=True)
        man["sha"]["tape"] = write_table(tape, "analytics_tape",
                                         ["asset", "ts"], root)
        man["sha"]["tape_inventory"] = write_table(
            TB.tape_inventory(tape), "tape_inventory", ["instant", "column"], root)
        man["counts"]["tape_rows"] = len(tape)
        man["counts"]["tape_instants"] = tape["instant"].value_counts().to_dict()

    # ── the lineage ───────────────────────────────────────────────────────
    lin = []
    for label, rt, card in (("v1", V1_T, "TIER-C2 · 1H anchor, no rail"),
                            ("v3", V3_T, "TIER-C3 · 4h anchor + 1.0 rail + lead-in"),
                            ("v4", V4_T, "TIER-C4 · v3 + trail + harvest")):
        p = rt / "headline.parquet"
        if p.exists():
            h = pd.read_parquet(p)
            a = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
            lin.append({"version": label, "card": card,
                        "corridor": "2025-10-06 -> 2026-01-31 (118 d, SEALED box)",
                        "n": int(a["n"]), "net_r": r4(a["net_r"]),
                        "expectancy_r": r4(a["expectancy_r"]),
                        "win_rate_pct": r4(a["win_rate_pct"]),
                        "max_dd_r": r4(a["max_dd_r"]),
                        "source": str(p.relative_to(ROOT))})
    a5 = head[(head["group"] == "ALL") & (head["key"] == "ALL")].iloc[0]
    lin.append({"version": "v5", "card": "TIER-C5 · v4 + funding ceiling 1R",
                "corridor": f"{cmeta['panel_start'][:10]} -> "
                            f"{cmeta['last_closed_4h_close'][:10]} "
                            f"({cmeta['span_days']} d, BOX OPEN)",
                "n": int(a5["n"]), "net_r": r4(a5["net_r"]),
                "expectancy_r": r4(a5["expectancy_r"]),
                "win_rate_pct": r4(a5["win_rate_pct"]),
                "max_dd_r": r4(a5["max_dd_r"]), "source": "this build"})
    man["sha"]["lineage"] = write_table(pd.DataFrame(lin), "lineage", ["version"],
                                        root)

    # ── counts ────────────────────────────────────────────────────────────
    lb0s, lb1s = RC.LOCKBOX_WAS[0], iso(_ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1)
    if len(rl):
        sm = (rl["pivot_bar_ts"] >= lb0s) & (rl["pivot_bar_ts"] <= lb1s)
        n_sealed_piv = int(sm.sum())
        pc = rl[sm][["asset", "entry_ms"]].drop_duplicates()
        n_sealed_piv_camp = len(pc)
        n_sealed_paid = int((sm & rl["paid_out"]).sum())
        anch = set(map(tuple, jr[jr["anchor_was_sealed_under_the_old_lockbox"]]
                       [["asset", "entry_ms"]].values))
        n_sealed_any = len(anch | set(map(tuple, pc.values)))
    else:
        n_sealed_piv = n_sealed_piv_camp = n_sealed_paid = 0
        n_sealed_any = int(jr["anchor_was_sealed_under_the_old_lockbox"].sum())
    man["counts"].update({
        "armings": len(arms_all), "campaigns": len(base),
        "advances": len(rl), "harvests": int(jr["harvested"].sum()),
        "funding_ceiling_bound": int(jr["funding_ceiling_bound"].sum()),
        "anchors_from_formerly_sealed_bars": int(
            jr["anchor_was_sealed_under_the_old_lockbox"].sum()),
        # THE SECOND PUBLISHED PRICE, COUNTED TOO.
        # An anchor is not the only price this card quotes from a named bar and
        # pays out: so is a RATCHET PIVOT. Counting only anchors understated the
        # box read — 60 advances across 24 campaigns take a pivot from a
        # formerly-sealed bar, and on every one of those 24 that advance is the
        # FINAL stop, i.e. the EXIT PRICE came out of the old lockbox. Found by
        # the post-build adversarial review.
        "advances_from_formerly_sealed_pivot_bars": int(n_sealed_piv),
        "campaigns_with_a_sealed_ratchet_pivot": int(n_sealed_piv_camp),
        "campaigns_whose_EXIT_PRICE_came_from_a_sealed_bar": int(n_sealed_paid),
        "campaigns_quoting_ANY_formerly_sealed_price": int(n_sealed_any),
        "spring_campaigns": len(spring), "union_campaigns": len(union),
        "spring_sweeps_refused_on_tide_at_first_reclaim": spring_tide_refused,
        "adds_campaigns_with_adds": sum(1 for t in adds if t.adds),
        "adds_total": sum(len(t.adds) for t in adds),
        "league_rows": len(league), "midband_rows": len(mb),
        "avg_ae_r": r6(avg_ae),
    })
    man["elapsed_s"] = round(time.time() - t0, 1)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    a = ap.parse_args()
    run(OUT_RERUN if a.rerun else OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
