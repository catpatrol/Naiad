"""TIER-C6 rev B · ARMED TRAIL + WALLS + ZEC FORENSICS + THE LIMIT FRONTIER.

RATIFIED operator 2026-08-16.  CLASS: measurement + registrations + pre-named
labs.  D15 columns everywhere, GATES NOWHERE.  Every grid reported WHOLE.  Every
fixture leg states its failure condition.

THE CORRIDOR IS FULL WATER — panel start to the latest closed 4h bar, one
unbroken window, WARMUP_BARS = 316.

────────────────────────────────────────────────────────────────────────────
F-C5-a IS RULED, AND IT CHANGES EVERY TABLE IN THIS DOCUMENT
────────────────────────────────────────────────────────────────────────────
THE YARDSTICK IS THE CURRENT CARD'S FULL-CORRIDOR EXPECTANCY.  Not the 118
sealed days (+0.6907), not the operator's 29-campaign refresh (+1.1964) — the
whole corridor, whatever it says.  Three candidates seven times apart are now
one, and EVERY SLICE NUMBER IN THIS BUILD CARRIES ITS WINDOW LABEL so that no
reader can lift a quarter out of a table and call it the book.  The label is a
COLUMN (`window`), not a caption, because a caption does not survive a copy of
the row into someone else's spreadsheet.

────────────────────────────────────────────────────────────────────────────
THE FORK: WHAT IS BOUND, AND WHAT IS COPIED, AND WHY THE COPIES ARE SAFE
────────────────────────────────────────────────────────────────────────────
Everything that does not change is BOUND from `tierc5` by identity — `frame`,
`fractals`, `addctx`, `corridor`, `card_candidates`, `agg`, `d15`, `slices_of`,
`tide_mix`, `journal_frame`, `ratchet_ledger`, the bootstrap block, `_tf_frame`
and the constants.  F-C6-INHERIT asserts it with `is`.

THREE FUNCTIONS ARE FORKED, NOT BOUND: `_ride`, `_account` and `replay`.  They
are forked because their BODIES change, and a body that changes cannot be
inherited by import however much one would like it to.  `_ride` gains the
minimum advance and the wall exit; `_account` reads the harvest fraction off the
card instead of off a module constant; `replay` differs from its parent in
exactly two call sites — the two above.

AND THAT IS EXACTLY WHY F-C6-CTRL EXISTS.  A copied function is a function that
can drift, so the v5 CARD is ridden through THIS module's forked code path and
must reproduce Tier-C5's FILED book trade-for-trade to 1e-05.  The estate's own
verdict on the parent of this fixture: F-C5-CTRL was "the single most productive
fixture" of the TC5 build.  It is carried forward and tightened.

────────────────────────────────────────────────────────────────────────────
THE PROMOTION IS DISCLOSED, BECAUSE IT WAS A CELL BEFORE IT WAS A CARD
────────────────────────────────────────────────────────────────────────────
`trail_arm_after_r = 1.0` was NOT invented for v6.  It was `S-TRAIL arms after
+1R`, a scored shadow cell of the TC5 fleet (`tierc5.py:1502`), and its numbers
were looked at: n = 195, net +39.9201, expectancy +0.2047, Δexp +0.0323, and the
session report called it "the only S-TRAIL cell whose diagnostics do not
immediately disqualify its headline".  It is promoted to the card BY RULING H5,
by the operator, and NOT by that number — but the number existed first and the
selection surface it came out of is logged (S-TRAIL contributed 3 cells to a
total m the TC5 build wrote down before the look).

A builder who promotes a cell it also scored, without saying so, is running the
exact failure the idling selection guard exists to make visible.  So it is said
here, in the module that does it, and again on the headline table's face.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc5 as T5                                                  # noqa: E402
import tierc6_rules as RC                                            # noqa: E402
import tierc5_rules as V5                                            # noqa: E402
import tierc3_baseline as T3                                         # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
import analytics as AN                                               # noqa: E402
from engine import indicators as ind                                 # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key, log = TB.write_table, TB.assert_key, TB.log
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D

# ═══════════════════════════════════════════ BOUND, NOT COPIED — asserted `is`
frame, fractals, addctx = T5.frame, T5.fractals, T5.addctx
corridor, card_candidates = T5.corridor, T5.card_candidates
_idx_range = T5._idx_range
agg, d15, slices_of, tide_mix = T5.agg, T5.d15, T5.slices_of, T5.tide_mix
journal_frame, ratchet_ledger = T5.journal_frame, T5.ratchet_ledger
cluster_boot, cluster_boot_diff, _ci_from = (T5.cluster_boot, T5.cluster_boot_diff,
                                             T5._ci_from)
_tf_frame = T5._tf_frame
harvest_lab, midband = T5.harvest_lab, T5.midband
LEAGUE_EMAS, LEAGUE_TFS = T5.LEAGUE_EMAS, T5.LEAGUE_TFS
LEAGUE_APPROACH_ATR, LEAGUE_RESOLVE_BARS = (T5.LEAGUE_APPROACH_ATR,
                                            T5.LEAGUE_RESOLVE_BARS)
LEAGUE_MIN_APPROACHES, TIER_E_FROM = T5.LEAGUE_MIN_APPROACHES, T5.TIER_E_FROM

SEED = 20260816
OUT = ROOT / "research_outputs" / "tierc6"
OUT_RERUN = ROOT / "research_outputs" / "tierc6_run2"
TC5 = ROOT / "research_outputs" / "tierc5"

SIDES = ("resistance", "support")


# ══════════════════════════════════════════ THE WALL, CACHED PER (SYM, LEN)
_WALL: dict[tuple[str, int, str], np.ndarray] = {}


def wall(sym: str, length: int, tf: str = "12h") -> np.ndarray:
    """The champion wall series on the 4h clock — 2 x N (ema, atr), cached.

    Built by `RC.wall_series_12h` IN THE DECISION PATH out of raw 4h bars, not
    by the league's analytics resampler.  The league names the LENGTH; it does
    not supply the series.  See `tierc6_rules.wall_series_12h` for why.
    """
    k = (sym, int(length), tf)
    if k not in _WALL:
        f = frame(sym)["f"]
        _WALL[k] = RC.wall_series_12h(f.open_ms, f.h, f.l, f.c, int(length))
    return _WALL[k]


# ═══════════════════════════════════════════════════════════ THE RIDE, v6
def _ride(sym: str, card: RC.Card, direction: int, ti: int, entry_px: float,
          stop0: float, r_dist: float, hi_i: int,
          test_stop_on_entry_bar: bool = False,
          wall_lens: dict[int, int] | None = None) -> dict:
    """ONE CODE PATH FOR EVERY CELL IN THE FLEET — Tier-C5's, plus two rules.

    Within-bar order, adverse-first throughout, INHERITED AND EXTENDED:

        STOP -> BELL -> TIME STOP -> HARVEST -> WALL -> ADDS -> TRAIL

    THE WALL SITS AFTER THE HARVEST, AND THAT IS THE WHOLE OF ITS SEMANTICS.
    P-WALL-1 exits "the REMAINDER".  If the wall fired before the harvest, then
    on a bar where both trigger the harvest would never book and the campaign
    would exit whole — a different rule.  Placed after, the harvest takes its
    fraction at that bar's close and the wall takes what is left at the SAME
    close, so the two together are a full exit at the close and the halves still
    sum.  The alternative order is named here because the two readings differ on
    exactly the bars where both fire, and only one of them is in the code.

    THE TRAIL IS STILL LAST because its result governs the NEXT bar, and the
    minimum advance [F-C4-d] is applied inside `RC.trail_step`, not here, so the
    quantity gated is the quantity the ledger publishes.

    THE ARMING IS A HIGH-WATER LATCH, INHERITED UNCHANGED.  `trail_armed` is set
    the first bar whose FAVOURABLE extreme reaches `card.trail_arm_after_r` and
    is never cleared.  A campaign that touches +1R and falls back keeps its
    armed trail, because the ruling asks whether the campaign has proved itself
    and a campaign does not un-prove itself.

    WHAT WOULD MAKE THIS WRONG: a stop tested against the bar that created it, a
    harvest booked on a bar the stop already closed, a wall exit on a bar the
    stop already closed, an add entered after the exit, or a trail advance
    applied to its own bar.  F-C6-CTRL rides the v5 card through this exact
    function and must reproduce Tier-C5's filed book trade-by-trade; any
    reordering here breaks it, which is the point of having it.
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
    armed_at_i = ti if trail_armed else None
    h_armed = False
    adds: list = []
    retraced = False
    exit_i, exit_px, exit_reason = hi_i, float(f.c[hi_i]), "corridor_end"
    wall_hit = None

    # THE WALL SERIES IS FETCHED ONCE, AND ONLY WHEN THE CARD ASKS FOR IT.
    # A cell with `wall_exit_atr = None` must not pay for a 12h EMA it will
    # never read, and — more importantly — must not be able to differ from v5
    # because of one.
    we, wa = (None, None)
    if card.wall_exit_atr is not None and wall_lens:
        # THE WALL IS CHOSEN BY DIRECTION, NOT BY THE BOOK.  A long is scored
        # against the RESISTANCE champion and a short against the SUPPORT one —
        # see `profit_side`.  One length for both sides would measure, for half
        # the book, the wall behind the position.
        wl = wall_lens.get(int(d))
        if wl:
            w = wall(sym, int(wl), card.wall_tf)
            we, wa = w[0], w[1]

    if test_stop_on_entry_bar:
        adv0 = float(f.l[ti]) if d == 1 else float(f.h[ti])
        if (d == 1 and adv0 <= stop) or (d == -1 and adv0 >= stop):
            return {"exit_i": ti, "exit_px": stop, "exit_reason": "stop",
                    "advances": [], "harvest": None, "blocked": "",
                    "mfe": float(entry_px), "adds": [], "final_stop": stop,
                    "mae_to_1r": None, "reached_1r": False,
                    "armed_at_i": armed_at_i, "wall_hit": None}

    for j in range(ti + 1, hi_i + 1):
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        unit_fav_r = (fav - entry_px) * d / r_dist
        unit_adv_r = (adverse - entry_px) * d / r_dist

        if not reached_1r:
            mae_to_1r = min(mae_to_1r, unit_adv_r)
            if unit_fav_r >= 1.0:
                reached_1r = True
        if not trail_armed and unit_fav_r >= card.trail_arm_after_r:
            trail_armed = True
            armed_at_i = j

        if card.harvest == "band":
            pe = RC.harvest_edge(float(f.e89[j - 1]), float(f.e316[j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(f.e89[j]), float(f.e316[j]), d)
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
            mfe = fav

        # 2 · the bell — KEPT AS A BACKSTOP [F-C4-c / F-C5-e], expected never
        #     to fire. It fired once in seven years under v5 and its silence is
        #     not evidence that it works.
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
                    else float(edge))
            harv = (j, fill, (fill - entry_px) * d / r_dist)

        # 5 · THE WALL [P-WALL-1] — the remainder exits on a close within
        #     `wall_exit_atr` ATR of the profit-side champion. Registered, NOT
        #     carded: the card v6 leaves `wall_exit_atr = None` and this branch
        #     is dead on every scored card row.
        if we is not None and np.isfinite(we[j]):
            if RC.wall_touch(float(f.c[j]), float(we[j]), float(wa[j]),
                             card.wall_exit_atr):
                exit_i, exit_px, exit_reason = j, float(f.c[j]), "wall"
                wall_hit = (j, float(we[j]), float(wa[j]))
                break

        # 6 · the adds
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

        # 7 · the trail — governs bar j + 1
        if card.trail and trail_armed:
            adv = RC.trail_step(fr, j, d, stop, float(f.c[j]), float(f.atr[j]),
                                f.open_ms,
                                buf_atr=RC.RATCHET_BUF_ATR + card.trail_extra_buf_atr,
                                rail_atr=RC.RATCHET_RAIL_ATR,
                                forbidden=(None if card.seal_open
                                           else T3.sealed_mask(f.open_ms)),
                                min_advance_atr=card.trail_min_advance_atr)
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)

    return {"exit_i": exit_i, "exit_px": exit_px, "exit_reason": exit_reason,
            "advances": advances, "harvest": harv, "blocked": blocked,
            "mfe": mfe, "adds": adds, "final_stop": stop,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r, "armed_at_i": armed_at_i,
            "wall_hit": wall_hit}


def _account(sym: str, card: RC.Card, direction: int, ti: int, entry_px: float,
             r_dist: float, ride: dict) -> dict:
    """Tier-C5's accounting, with the harvest FRACTION read off the card.

    THE ONLY DIFF IS `q`.  v5 read `RC.HARVEST_FRACTION`, a module constant, so
    S-HFRAC could not be a grid: a shadow that cannot vary is a shadow that
    cannot be compared.  It is now `card.harvest_frac`, whose default IS
    `HARVEST_FRACTION` (0.5, the ruled value under H3), so the card is
    unchanged and the grid becomes possible.

    THE HALVES INVARIANT SURVIVES THE GENERALISATION.  It was never about
    halves — `q` and `1-q` sum to 1 for any fraction — and the exact HALT at
    1e-9 is kept rather than loosened, because the arithmetic bound does not
    depend on q.

    WHAT WOULD MAKE THIS WRONG: fractions that do not book the base leg, an add
    charged funding before it existed, or a ceiling applied to a funding CREDIT.
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

    q = float(card.harvest_frac)                 # THE ONE DIFF FROM v5
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
    cap = card.funding_ceiling_r
    fund_eff = min(fund_raw, cap) if (cap is not None and fund_raw > cap) else fund_raw
    net = gross - fee - fund_eff

    if n1 is not None and cap is None:
        base_net = (g_base - f_base - u_base) / r_dist
        if abs((n1 + n2) - base_net) > 1e-9:
            raise SystemExit(
                f"HALT: the fractions do not book the base leg. {sym} {ti}: "
                f"{n1!r} + {n2!r} != {base_net!r}  (q={q})")
    return {"gross_r": gross, "fee_r": fee, "funding_r": fund_eff,
            "funding_r_uncapped": fund_raw,
            "funding_ceiling_bound": bool(cap is not None and fund_raw > cap),
            "net_r": net, "n1": n1, "n2": n2,
            "add_r": (g_add - fe_add - u_add) / r_dist if ride["adds"] else None,
            "harvest_ride_would_have_r": would_have}


def replay(sym: str, card: RC.Card, lo_ms: int, hi_ms: int,
           wall_lens: dict[int, int] | None = None) -> tuple[list, list]:
    """Tier-C5's `replay`, re-pointed at this module's `_ride` and `_account`.

    THE DIFF IS TWO CALL SITES AND ONE THREADED ARGUMENT.  Everything else —
    the warm-up floor, the lane merge, one-position-per-asset across lanes, the
    seal argument, the rejection labels, the Trade construction — is Tier-C5's,
    line for line.  F-C6-CTRL is what makes that claim checkable rather than
    asserted: it rides the v5 card through this function and demands Tier-C5's
    FILED journal back, trade for trade.
    """
    st = frame(sym)
    f = st["f"]
    lo_i, hi_i = _idx_range(f.open_ms, lo_ms, hi_ms)
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

        ride = _ride(sym, card, d, ti, entry_px, stp.stop_px, stp.r_dist, hi_i,
                     wall_lens=wall_lens)
        open_until = ride["exit_i"]
        acc = _account(sym, card, d, ti, entry_px, stp.r_dist, ride)
        harv = ride["harvest"]
        anchor_ms = int(f.open_ms[stp.anchor_bar]) if stp.anchor_bar >= 0 else -1
        lb0, lb1 = _ms(RC.LOCKBOX_WAS[0]), _ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1
        t = RC.Trade(
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
            net_r_runner_half=acc["n2"], net_r_bellonly=None)
        # THE TWO v6 DIAGNOSTICS, CARRIED ON THE OBJECT BUT NOT IN `Trade`.
        # `RC.Trade` is Tier-C5's frozen dataclass bound by identity; adding a
        # field to it would break the `is` inheritance leg and every parent's
        # book. These ride as attributes and are read only by this module's
        # own tables.
        object.__setattr__(t, "armed_at_i", ride["armed_at_i"])
        object.__setattr__(t, "wall_hit", ride["wall_hit"])
        trades.append(t)
    return arms, trades


def run_cell(card: RC.Card, lo_ms: int, hi_ms: int,
             wall_lens: dict[int, int] | None = None) -> list:
    """One cell of the fleet over the whole panel."""
    out = []
    for s in RC.UNIVERSE:
        _, t = replay(s, card, lo_ms, hi_ms, wall_lens=wall_lens)
        out += t
    return out


# ═══════════════════════════════════ THE TWO AGGREGATIONS · raw + equal-asset
def ear_weights(trades: list) -> np.ndarray:
    """EQUAL-ASSET-RISK weights.  w_i = (N/K) / n_{a(i)},  sum(w) = N exactly.

    THE DENOMINATOR IS THE ASSETS PRESENT IN THIS BOOK, not `len(UNIVERSE)`.
    An echo that drops ZEC has K = 4, and dividing by 5 there would quietly
    scale every number in the echo by 4/5 — a weighting bug that looks like a
    result.

    WHY `N/K` AND NOT `1/n_a`: it makes sum(w) = N, so `n` is the SAME INTEGER
    under both aggregations, `expectancy = sum(w r)/N` is directly comparable to
    the raw one, and `net_r` stays denominated in R rather than in "mean R per
    asset".  A reader can put the two rows side by side without a conversion.
    """
    if not trades:
        return np.zeros(0)
    syms = np.array([t.symbol for t in trades])
    uniq, counts = np.unique(syms, return_counts=True)
    n_by = dict(zip(uniq, counts))
    N, K = len(trades), len(uniq)
    return np.array([(N / K) / n_by[s] for s in syms], dtype=float)


def agg_ear(trades: list, label: str, key: str = "ALL",
            extra: dict | None = None) -> dict:
    """`agg`, re-weighted so every asset carries the same risk.

    WHAT DOES NOT GET WEIGHTED, AND WHY.  `best_r` names a REAL TRADE — the
    biggest single result in the book — and a weighted "best" is not a trade
    anybody took.  It stays raw, and `best_contrib_r` (the largest WEIGHTED
    contribution) is added beside it, because under equal-asset-risk the trade
    that dominates the total need not be the trade with the largest R.

    WHAT WOULD MAKE THIS WRONG: weighting `best_r`; using `len(UNIVERSE)` as K;
    or computing max drawdown on unweighted contributions, which would report a
    drawdown the equal-risk book never had.
    """
    if not trades:
        return dict(agg(trades, label, key, extra), aggregation="equal_asset_risk")
    w = ear_weights(trades)
    r = np.array([float(t.net_r) for t in trades])
    N = len(trades)
    wr = w * r
    base = agg(trades, label, key, extra)
    contrib = sorted(zip([int(t.exit_ms) for t in trades],
                         [t.symbol for t in trades], wr))
    run = 0.0
    peak = 0.0
    dd = 0.0
    for _, _, v in contrib:
        run += v
        peak = max(peak, run)
        dd = max(dd, peak - run)
    jbest = int(np.argmax(wr))
    k = max(int(np.floor(0.10 * N)), 1)
    top = np.sort(wr)[::-1][:k]
    tot = float(wr.sum())
    out = dict(base)
    out.update({
        "aggregation": "equal_asset_risk",
        "n": N,
        "net_r": r4(tot),
        "expectancy_r": r4(tot / N),
        "win_rate_pct": r4(100.0 * float(w[r > 0].sum()) / N),
        "max_dd_r": r4(dd),
        # ADVERSARIAL REPAIR C6-4. `top_decile_share_pct` is a SHARE OF THE
        # TOTAL, and under equal-asset-risk the total is the WEIGHTED total —
        # which is small whenever the rest of the book is negative. The first
        # draft published 260% and 302% in the same column, on the same table,
        # beside the raw rows' 72.6% and 77.1%, so two numbers on two different
        # denominators wore one name. Above 100% the quantity is arithmetically
        # correct and semantically not a share, so it is published with its
        # BASIS on the row and a flag that says when it may be compared across
        # aggregations. Nothing is hidden and nothing is silently rescaled.
        "top_decile_share_pct": (r4(100.0 * float(top.sum()) / tot)
                                 if abs(tot) > 1e-12 else None),
        "top_decile_share_basis": "weighted net R total (equal-asset-risk)",
        "top_decile_share_comparable_to_raw": bool(
            abs(tot) > 1e-12 and 0.0 <= 100.0 * float(top.sum()) / tot <= 100.0),
        "best_r": r4(float(r.max())),          # UNWEIGHTED — it names a trade
        "best_contrib_r": r4(float(wr[jbest])),
        "strip_best_net_r": r4(tot - float(wr[jbest])),
        "gross_r": r4(float((w * np.array([t.gross_r for t in trades])).sum())),
        "fee_r": r4(float((w * np.array([t.fee_r for t in trades])).sum())),
        "funding_r": r4(float((w * np.array([t.funding_r for t in trades])).sum())),
        "assets_present": len(set(t.symbol for t in trades)),
    })
    return out


def agg_both(trades: list, label: str, key: str = "ALL",
             group: str = "ALL", window: str = "full_corridor",
             extra: dict | None = None) -> list[dict]:
    """Both rulers, one table, one row each — and the WINDOW LABEL on every row.

    F-C5-a ruled that the yardstick is the full-corridor expectancy.  A slice
    row that does not say which window it is a slice OF is exactly the object
    that made three numbers seven times apart look like one number, so `window`
    is a column here and it is never optional.
    """
    # `agg`'s `label` argument becomes its `group` COLUMN — it is a grouping
    # name, not a book name. TC6 needs both (the same group appears under the
    # v6 book and the v5 control), so the book label is its own column and the
    # grouping dimension is set explicitly. Writing `label` into `group` and
    # then overwriting `group` — which the first draft did — silently dropped
    # the book name and made the headline key non-unique.
    a = dict(agg(trades, group, key, extra), aggregation="raw_panel",
             top_decile_share_basis="raw net R total",
             top_decile_share_comparable_to_raw=True)
    b = agg_ear(trades, group, key, extra)
    rows = []
    for x in (a, b):
        x = dict(x)
        x["label"] = label
        x["group"], x["key"], x["window"] = group, key, window
        x.setdefault("best_contrib_r", x.get("best_r"))
        x.setdefault("assets_present", len(set(t.symbol for t in trades)))
        rows.append(x)
    return rows


def headline_v6(book: list, label: str, lo_ms: int, hi_ms: int,
                echo: bool = False) -> pd.DataFrame:
    """THE HEADLINE — both aggregations x {ALL, per-asset, per-direction,
    per-exit-reason}, every row carrying its window.

    And the ZEC-EXCLUDED ECHO, when asked for: the SAME table re-scored over a
    universe of four.  It is a re-score, not a filter of the rows above — the
    equal-asset-risk weights change when K changes, and a filtered table would
    carry weights computed for five assets while claiming to describe four.
    """
    rows: list[dict] = []
    uni = "panel_minus_ZEC" if echo else "panel"
    b = [t for t in book if t.symbol != "ZECUSDT"] if echo else book
    rows += agg_both(b, label, "ALL", "ALL", window="full_corridor")
    for s in sorted(set(t.symbol for t in b)):
        rows += agg_both([t for t in b if t.symbol == s], label, s, "asset",
                         window="full_corridor")
    for dn, dv in (("long", 1), ("short", -1)):
        rows += agg_both([t for t in b if t.direction == dv], label, dn,
                         "direction", window="full_corridor")
    for er in sorted(set(t.exit_reason for t in b)):
        rows += agg_both([t for t in b if t.exit_reason == er], label, er,
                         "exit_reason", window="full_corridor")
    df = pd.DataFrame(rows)
    df["universe"] = uni
    return df


def slice_table(book: list, label: str, lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """Every slice, both rulers, EACH CARRYING ITS OWN WINDOW LABEL [F-C5-a]."""
    # `slices_of` yields (GROUP, KEY, lo, hi) — the group first. Unpacking it
    # the other way round, as the first draft did, collapsed all eight years
    # onto one key and F-KEY caught it at 36 duplicate rows. The years are
    # already IN `slices_of`; a second per-year loop would double them.
    rows = []
    for grp, key, a, b in slices_of(lo_ms, hi_ms):
        sl = [t for t in book if a <= t.entry_ms <= b]
        rows += agg_both(sl, label, key, grp, window=key)
    df = pd.DataFrame(rows)
    df["provisional"] = df["n"].astype(int) < RC.PROVISIONAL_MIN_N
    return df


# ═══════════════════════════════════════════ STAGE W · THE LEAGUE, BOTH SIDES
def league(hi_ms: int, side: str) -> pd.DataFrame:
    """THE LEAGUE TABLE, PARAMETERISED BY SIDE.  Tier-C5's resistance league is
    `side="resistance"` exactly; `side="support"` is its mirror.

    RESISTANCE  the bar's HIGH comes within LEAGUE_APPROACH_ATR of the EMA FROM
                BELOW (the previous bar closed BELOW it).  REJECTION = no close
                ABOVE the EMA within LEAGUE_RESOLVE_BARS bars.
    SUPPORT     the bar's LOW comes within LEAGUE_APPROACH_ATR of the EMA FROM
                ABOVE (the previous bar closed ABOVE it).  REJECTION = no close
                BELOW the EMA within the same window.

    PENETRATION NEVER FLIPS SIGN.  It is a DEPTH — how far past the wall the
    deepest close got, in ATR — and a depth is a magnitude on both sides.  A
    mirrored sign here would make the two sides' columns incomparable while
    looking fine.

    THE CHAMPION IS A NAMED MAXIMUM, NOT A PROMOTION.  It is an argmax over the
    eligible cells of one side, with no bar, no interval and no correction, and
    the cells it is chosen from are in the logged selection surface.  P-WALL-1
    then USES that argmax as a decision input, which is a selection surface
    feeding a registration — disclosed on the registration's own row, because
    it is the single largest caveat on that claim.

    WHAT WOULD MAKE THIS WRONG: an approach counted from the wrong side (it
    would measure the opposite wall), a rejection window that reads a bar the
    approach could not see, an EMA read before it is warm, or a penetration
    that changes sign with the side.  F-C6-LEAGUE re-derives one row per
    (timeframe, side) from raw bars AND proves the two predicates are genuine
    mirrors by running the support scan on a negated series.
    """
    if side not in SIDES:
        raise SystemExit(f"HALT: unknown league side {side!r}")
    up = side == "resistance"
    lo = _ms(TIER_E_FROM)
    rows = []
    for sym in RC.UNIVERSE:
        for tf in LEAGUE_TFS:
            fr = _tf_frame(sym, tf)
            t, h, l, c = fr["t"], fr["h"], fr["l"], fr["c"]
            a = ind.atr(h, l, c, RC.ATR_LEN)
            m = (t >= lo) & (t <= hi_ms)
            if not m.any():
                continue
            i0, i1 = int(np.argmax(m)), int(len(t) - 1 - np.argmax(m[::-1]))
            for L in LEAGUE_EMAS:
                if len(c) < L + 5:
                    continue
                e = ind.ema(c, L)
                warm = L      # THE FLOOR — ind.ema seeds and never returns NaN
                napp = nrej = 0
                pens: list[float] = []
                depths: list[float] = []
                streak = best_streak = 0
                for i in range(max(i0, warm + 1), i1 + 1):
                    if not (np.isfinite(e[i]) and np.isfinite(a[i]) and a[i] > 0):
                        continue
                    # THE APPROACH — from the correct side, and the previous
                    # close must be on that side too.
                    if up:
                        if not (c[i - 1] < e[i - 1]):
                            continue
                        if h[i] < e[i] - LEAGUE_APPROACH_ATR * a[i]:
                            continue
                    else:
                        if not (c[i - 1] > e[i - 1]):
                            continue
                        if l[i] > e[i] + LEAGUE_APPROACH_ATR * a[i]:
                            continue
                    napp += 1
                    w = slice(i, min(i + LEAGUE_RESOLVE_BARS + 1, i1 + 1))
                    seg = c[w] - e[w]
                    broke = bool(np.any(seg > 0)) if up else bool(np.any(seg < 0))
                    # PENETRATION IS THE PARENT'S STATISTIC, UNCHANGED —
                    # ADVERSARIAL REPAIR C6-2. Tier-C5 appends
                    # `max(pen, 0.0)` for EVERY approach, rejected ones
                    # included, where `pen` is the deepest signed excursion in
                    # the window over ATR. The first draft of this fork
                    # appended only on a break-through and called the result by
                    # the parent's name, which SILENTLY REDEFINED the column:
                    # 290 of 313 rows differed and the build claimed "zero
                    # differences" because leg (a) compared only approaches,
                    # rejections and champion flags. A statistic renamed by
                    # accident under a reproduction claim is the same defect
                    # class as `dist_atr` and `prior_extreme` — a name that is
                    # almost right. The parent's definition is restored here
                    # and the broke-only depth, which IS the more useful
                    # number, is published beside it UNDER ITS OWN NAME.
                    pen = (float(np.max(seg)) if up else float(-np.min(seg)))
                    pens.append(max(pen / float(a[i]), 0.0))
                    if broke:
                        depths.append(abs(pen) / float(a[i]))
                        streak = 0
                    else:
                        nrej += 1
                        streak += 1
                        best_streak = max(best_streak, streak)
                rows.append({
                    "side": side, "asset": sym, "tf": tf, "ema": int(L),
                    "approaches": napp, "rejections": nrej,
                    "rejection_rate_pct": (r4(100.0 * nrej / napp) if napp else None),
                    "mean_penetration_atr": (r6(float(np.mean(pens))) if pens
                                             else None),
                    "mean_breakthrough_depth_atr": (r6(float(np.mean(depths)))
                                                    if depths else None),
                    "longest_rejection_streak": int(best_streak),
                })
    d = pd.DataFrame(rows)
    if not len(d):
        return d
    # THE PANEL ROW POOLS APPROACHES AND REJECTIONS, so its penetration is
    # APPROACH-WEIGHTED — Tier-C5's own post-build repair, inherited verbatim
    # rather than re-derived, because an unweighted mean of five per-asset means
    # sitting beside a pooled count is two populations on one row.
    #
    # AND THE CHAMPION IS CHOSEN FROM THE PANEL ROW, NOT FROM A MEAN OF THE
    # PER-ASSET RATES.  The first draft of this function took the argmax of the
    # mean per-asset rejection rate and named EMA 127 the 1d resistance champion
    # on 29 approaches, where the parent's pooled rule names EMA 889 on 42.  The
    # two rules disagree, the parent's is filed, and a fork that quietly picks
    # the other one is a fork that has changed a published number while claiming
    # to mirror.  Caught by comparing against the filed table, which is the only
    # reason it was caught at all.
    d["_pen_w"] = d["mean_penetration_atr"].astype(float) * d["approaches"]
    d["_dep_w"] = d["mean_breakthrough_depth_atr"].astype(float) * d["approaches"]
    panel = (d.groupby(["tf", "ema"], as_index=False)
             .agg(approaches=("approaches", "sum"),
                  rejections=("rejections", "sum"),
                  _pen_w=("_pen_w", "sum"),
                  _dep_w=("_dep_w", "sum"),
                  longest_rejection_streak=("longest_rejection_streak", "max")))
    panel["asset"] = "__PANEL__"
    panel["side"] = side
    panel["rejection_rate_pct"] = [pct(r_, a_) for r_, a_ in
                                   zip(panel["rejections"], panel["approaches"])]
    panel["mean_penetration_atr"] = [
        r6(w / a) if a else None
        for w, a in zip(panel["_pen_w"], panel["approaches"])]
    panel["mean_breakthrough_depth_atr"] = [
        r6(w / a) if a else None
        for w, a in zip(panel["_dep_w"], panel["approaches"])]
    d = d.drop(columns=["_pen_w", "_dep_w"])
    panel = panel.drop(columns=["_pen_w", "_dep_w"])
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
    out["champion_chosen_from_n_cells"] = [
        int(((out["asset"] == "__PANEL__") & out["eligible_for_champion"]
             & (out["tf"] == r_["tf"])).sum()) if r_["is_champion_wall"] else None
        for _, r_ in out.iterrows()]
    out["champion_is_a_named_maximum_not_a_promotion"] = [
        ("argmax of rejection_rate over the eligible panel cells for this TF "
         "and SIDE; no acceptance bar, no CI, no multiplicity correction — it "
         "is the biggest number in a column, and that is all it is. P-WALL-1 "
         "then USES it as a decision input, which makes it a selection surface "
         "feeding a registration and is disclosed on that registration's row.")
        if r_["is_champion_wall"] else None for _, r_ in out.iterrows()]
    return out


def champions(lg: pd.DataFrame) -> dict[tuple[str, str], int]:
    """(side, tf) -> the champion EMA length.  One dict, read by P-WALL-1."""
    out = {}
    for (side, tf), g in lg[lg["is_champion_wall"]].groupby(["side", "tf"]):
        out[(side, tf)] = int(g["ema"].iloc[0])
    return out


def profit_side(direction: int) -> str:
    """A LONG makes money UPWARD, so the wall in its way is RESISTANCE.
    A SHORT makes money DOWNWARD, so its wall is SUPPORT.

    This is why the league had to grow a second side before P-WALL-1 could be
    written at all: scoring a short against a resistance champion measures the
    wall BEHIND it, which is not a wall, it is a floor it has already left.
    """
    return "resistance" if direction == 1 else "support"


def main() -> int:                                     # pragma: no cover
    raise SystemExit("tierc6.run(root) is driven by the build driver below")


# ═══════════════════════════════════════════════════════ THE REGISTRATIONS
FDR_Q = T5.FDR_Q


def registration_text() -> pd.DataFrame:
    """THE TEXT BEFORE THE RESULT.  Both claims, their priors, their rulers and
    their named caveats, written as a table so the wording cannot drift between
    the commission and the score."""
    return pd.DataFrame([
        {"registration": "P-TRAIL-1", "prior_pct": 65,
         "claim": "the v6 trail (arms after +1R, minimum advance 0.05 ATR) "
                  "beats the v5 trail on PAIRED per-campaign expectancy",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "why_paired": "the trail cannot create or destroy a campaign — it "
                       "rides inside one — so every v6 campaign has exactly one "
                       "v5 twin at the same (asset, entry bar)",
         "named_caveat": "THE ARMING WAS A SCORED SHADOW CELL BEFORE IT WAS A "
                         "CARD. S-TRAIL 'arms after +1R' posted +0.2047 in the "
                         "TC5 fleet and was looked at. It is carded by ruling "
                         "H5, not by that number, but the number came first."},
        {"registration": "P-WALL-1", "prior_pct": 55,
         "claim": "exiting the remainder on a close within 0.25 ATR of the "
                  "PROFIT-SIDE 12h champion wall beats card v6",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "why_paired": "the wall exit rides inside a v6 campaign and changes "
                       "only where it ends; the campaign set is identical",
         "named_caveat": "THE CHAMPION LENGTH IS AN IN-SAMPLE ARGMAX. The 12h "
                         "champions (resistance 889, support 300) are the "
                         "biggest number in a league column, chosen from the "
                         "eligible panel cells with no bar, no interval and no "
                         "correction — and this registration then USES that "
                         "argmax as a decision input. That is a selection "
                         "surface feeding a registration and it is the single "
                         "largest caveat on this claim."},
    ])


def score_registrations6(base: list, trail_ctrl: list, wallbook: list
                         ) -> pd.DataFrame:
    """P-TRAIL-1 and P-WALL-1 — both PAIRED, both against the same bar.

    THE PAIRING IS THE POINT, AND IT IS WHY THIS IS NOT TC5's FUNCTION.
    Tier-C5's P-SPR-1 was scored against ZERO under a name that said "vs card",
    and the post-build review reversed its verdict for exactly that.  Both arms
    here ride INSIDE the same campaign set, so the paired delta is available and
    it is the only honest ruler: a campaign's v6 result minus the SAME
    campaign's v5 result, clustered on the asset.

    THE CARD IS PRINTED AS A REFERENCE ROW so a reader can see what the bar is
    worth before reading who cleared it — and the reference row is EXCLUDED from
    m, because it is not an acceptance test.

    WHAT WOULD MAKE THIS WRONG: pairing on entry time alone (two lanes can enter
    the same bar), scoring an arm named "vs X" against zero, or counting
    registrations filed instead of tests run in m.
    """
    rows = []

    def _row(reg, arm, prior, book, draws, point, ci_on, extra=None,
             d15_base=None, d15_base_name="card v6"):
        """One registration row.

        `d15_base` IS SEPARATE FROM `book` AND THAT IS ADVERSARIAL REPAIR C6-3.
        The first draft passed `**d15(book, base)` for every arm, so P-TRAIL-1 —
        whose `book` IS `base`, the v6 book — published `d15(v6, v6)`: a
        self-comparison reporting paired delta 0.0000, tail ratio 1.0000 and a
        NaN single-trade share, under column names that a reader takes to mean
        "the diagnostics of this arm". The D15 columns exist to say what the arm
        did TO the thing it is measured against, so the base is now named at
        every call site and P-TRAIL-1's is the v5 CONTROL.
        """
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
             **d15(book, base if d15_base is None else d15_base),
             "d15_measured_against": d15_base_name}
        r.update(extra or {})
        rows.append(r)

    # THE REFERENCE ROW — the card itself, through the first ruler.
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    _row("(reference)", "CARD v6 vs zero", None, base,
         cluster_boot(bnet, bcl), float(np.mean(bnet)),
         "the card's OWN expectancy vs zero, asset-cluster 90% CI — the bar, "
         "scored through the same ruler as everything that is asked to clear it",
         extra={"note": "not an acceptance test; excluded from m"})

    def paired(newbook, oldbook):
        """(deltas, clusters, n_pairs) keyed on (asset, lane, entry_ms).

        THE KEY CARRIES THE LANE.  Two lanes can enter the same asset on the
        same bar, and a key of (asset, entry_ms) would silently pair a spring
        with a card and call the difference a trail effect.
        """
        old = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in oldbook}
        pv, pc = [], []
        for t in newbook:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in old:
                pv.append(t.net_r - old[k])
                pc.append(t.symbol)
        return pv, pc, len(pv)

    # ── P-TRAIL-1 ────────────────────────────────────────────────────────
    pv, pc, npair = paired(base, trail_ctrl)
    _row("P-TRAIL-1", "v6 trail vs v5 trail (PAIRED)", 65, base,
         cluster_boot(pv, pc), float(np.mean(pv)) if pv else None,
         "the PAIRED per-campaign delta vs zero (asset-cluster 90% CI, mean)",
         d15_base=trail_ctrl, d15_base_name="v5 control",
         extra={"paired_n": npair,
                "paired_delta_r_total": r4(sum(pv)) if pv else None,
                "paired_delta_expectancy": r6(float(np.mean(pv))) if pv else None,
                "control_net_r": r4(sum(t.net_r for t in trail_ctrl)),
                "control_expectancy_r": r6(float(np.mean(
                    [t.net_r for t in trail_ctrl]))),
                "unpaired_new": len(base) - npair,
                "unpaired_old": len(trail_ctrl) - npair})

    # ── P-WALL-1 ─────────────────────────────────────────────────────────
    wv, wc, wpair = paired(wallbook, base)
    _row("P-WALL-1", "v6+wall exit vs v6 (PAIRED)", 55, wallbook,
         cluster_boot(wv, wc), float(np.mean(wv)) if wv else None,
         "the PAIRED per-campaign delta vs zero (asset-cluster 90% CI, mean)",
         extra={"paired_n": wpair,
                "paired_delta_r_total": r4(sum(wv)) if wv else None,
                "paired_delta_expectancy": r6(float(np.mean(wv))) if wv else None,
                "wall_exits": sum(1 for t in wallbook
                                  if t.exit_reason == "wall"),
                "unpaired_new": len(wallbook) - wpair,
                "unpaired_old": len(base) - wpair})

    d = pd.DataFrame(rows)
    tested = d[d["registration"] != "(reference)"]
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
        f"m = {m} — ACCEPTANCE TESTS ACTUALLY RUN, not registrations filed. "
        f"The reference row is not a test and is excluded. q = {FDR_Q}, "
        f"bar = q/m = {bar:.5f}. The correction is APPLIED, not merely "
        f"recorded: the same asset-cluster bootstrap that produces the interval "
        f"produces the one-sided tail, so no p was invented.")
    d["in_sample"] = True
    return d


# ═══════════════════════════════════════════════════════════════ THE DRIVER
def _labs():
    """The three lab modules, imported LAZILY and INDIVIDUALLY.

    Lazily because a lab is a Tier-E measurement and the decision path must be
    runnable without one.  Individually because a build that loses all three
    labs to one import error reports "no labs" when the truth is "one lab is
    broken" — and the disposition table has to be able to tell those apart.
    """
    mods = {}
    for k, name in (("zec", "tierc6_lab_zec"), ("limit", "tierc6_lab_limit"),
                    ("misc", "tierc6_lab_misc")):
        try:
            mods[k] = __import__(name)
        except Exception as e:                    # noqa: BLE001
            mods[k] = None
            log(f"    LAB {k}: NOT AVAILABLE — {type(e).__name__}: {e}")
    return mods


def run(root: Path) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "stage": "TIER-C6 rev B", "sha": {}, "counts": {}}
    log("=" * 78)
    log("TIER-C6 rev B · ARMED TRAIL + WALLS + ZEC FORENSICS + THE LIMIT FRONTIER")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")

    lo_ms, hi_ms, cmeta = corridor()
    man["corridor"] = {k: v for k, v in cmeta.items()
                       if k not in ("wall_clock_at_run", "cache_lag_hours")}
    log(f"  CORRIDOR {cmeta['panel_start']} -> {cmeta['last_closed_4h_close']} "
        f"({cmeta['span_days']} d = {cmeta['span_days']/365.25:.2f} y)")

    # ── the books ────────────────────────────────────────────────────────
    v6 = run_cell(RC.CARD_V6, lo_ms, hi_ms)
    v5 = run_cell(RC.CARD_V5_CONTROL, lo_ms, hi_ms)
    union = run_cell(RC.Card(name="union", grid="P-SPR-1", lane="union"),
                     lo_ms, hi_ms)
    log(f"  BOOKS  v6 {len(v6)} · v5-control {len(v5)} · union {len(union)}")

    # ── STAGE W · the league, both sides ─────────────────────────────────
    lg = pd.concat([league(hi_ms, s) for s in SIDES], ignore_index=True)
    ch = champions(lg)
    wl = {1: ch[("resistance", "12h")], -1: ch[("support", "12h")]}
    log(f"  LEAGUE {len(lg)} rows · champions "
        f"{ {f'{k[0]}/{k[1]}': v for k, v in sorted(ch.items())} }")

    wcard = RC.Card(name="v6+wall", grid="P-WALL-1", wall_exit_atr=0.25)
    wallbook = run_cell(wcard, lo_ms, hi_ms, wall_lens=wl)
    log(f"  WALL BOOK {len(wallbook)} · wall exits "
        f"{sum(1 for t in wallbook if t.exit_reason == 'wall')}")

    root.mkdir(parents=True, exist_ok=True)
    W = {}
    KEYS: dict[str, list] = {}
    SKIPPED: list[str] = []

    def put(df, name, key):
        if df is None or not len(df):
            # AN EMPTY TABLE IS RECORDED, NOT SWALLOWED — ADVERSARIAL REPAIR
            # C6-7. `put` returning silently meant a lab could produce nothing
            # and the manifest would look identical to a build where that lab
            # was never asked. The skip is now in the manifest, so "this table
            # is absent" and "this table was never attempted" are different
            # facts on the record.
            log(f"    (skip {name} — empty)")
            SKIPPED.append(name)
            return
        # A WRITTEN TABLE CARRIES DATA, NEVER LIVE OBJECTS.
        # pandas serialises `DataFrame.attrs` into the parquet metadata as
        # JSON, so a lab that stashes its source `Trade` objects on the frame —
        # convenient in memory, invisible on screen — kills the write with
        # "Object of type Trade is not JSON serializable". Cleared here rather
        # than in each lab, because the invariant belongs to the WRITE: whatever
        # a table needs to be understood must be a COLUMN, where a reader can
        # see it, not an attribute that only survives inside one process.
        df = df.copy()
        df.attrs = {}
        W[name] = write_table(df, name, key, root)
        KEYS[name] = list(key)

    # ── the headline, BOTH AGGREGATIONS, + per-asset + the ZEC echo ──────
    head = pd.concat([headline_v6(v6, "CARD v6", lo_ms, hi_ms),
                      headline_v6(v5, "v5 control", lo_ms, hi_ms)],
                     ignore_index=True)
    echo = pd.concat([headline_v6(v6, "CARD v6", lo_ms, hi_ms, echo=True),
                      headline_v6(v5, "v5 control", lo_ms, hi_ms, echo=True)],
                     ignore_index=True)
    head = pd.concat([head, echo], ignore_index=True)
    head["yardstick_note"] = (
        "F-C5-a RULED: the yardstick is the CURRENT CARD's FULL-CORRIDOR "
        "expectancy. Every row carries its own `window`. The arming rule was a "
        "SCORED SHADOW CELL of the TC5 fleet before it was carded — promoted by "
        "ruling H5, not by its number, but the number came first.")
    put(head, "headline", ["label", "aggregation", "universe", "group", "key"])

    put(pd.concat([slice_table(v6, "CARD v6", lo_ms, hi_ms),
                   slice_table(v5, "v5 control", lo_ms, hi_ms)],
                  ignore_index=True),
        "headline_by_slice", ["label", "aggregation", "group", "key"])

    put(lg, "league", ["side", "asset", "tf", "ema"])
    put(registration_text(), "registration_text", ["registration"])
    put(score_registrations6(v6, v5, wallbook), "registrations",
        ["registration", "arm"])
    put(journal_frame(v6), "trade_journal", ["asset", "entry_ms"])
    put(journal_frame(wallbook), "trade_journal_wall", ["asset", "entry_ms"])
    put(ratchet_ledger(v6), "ratchet_ledger", ["asset", "entry_ms", "advance_seq"])
    put(pd.DataFrame(RC.register_rows()), "register", ["key"])
    put(harvest_lab(v6, slices_of(lo_ms, hi_ms)), "harvest_lab",
        ["asset", "entry_ms", "entry_ts"])

    # ── the labs ─────────────────────────────────────────────────────────
    L = _labs()
    lab_state = {}
    if L["zec"]:
        Z = L["zec"]
        tabs = {h: getattr(Z, f"hz{h}_table")() for h in (1, 2, 3, 4, 5)}
        for h, t in tabs.items():
            put(t, f"lzec_hz{h}", ["asset"])
        fp = Z.fingerprint(tabs)
        put(fp, "lzec_fingerprint", ["metric"])
        put(Z.suitability_card(fp), "lzec_suitability_card", ["metric"])
        put(Z.crosscheck(), "lzec_crosscheck", ["leg"])
        man["why_zec"] = Z.answer_paragraph(fp, tabs)
        lab_state["L-ZEC"] = "BUILT"
    else:
        lab_state["L-ZEC"] = "NOT AVAILABLE"
    if L["limit"]:
        M = L["limit"]
        put(M.ae_deciles(v6, lo_ms, hi_ms), "l_ae_deciles", ["bucket", "key"])
        put(M.hazard_curve(v6), "l_ae_hazard", ["x_r"])
        put(M.ae_by_context(v6, ch), "l_ae_by_context", ["context", "bucket"])
        # THE CARD IS THREADED, NOT DEFAULTED. The split arm caps funding at
        # the campaign level and must read the ceiling off the card that is
        # being scored, not off a module global — the lab's own self-check
        # found that divergence and it is invisible while both are 1.0.
        put(M.frontier(v6, lo_ms, hi_ms, card=RC.CARD_V6), "l_limit_frontier",
            ["k_atr", "arm"])
        man["limit_prereg"] = M.prereg_text()
        man["limit_prereg_sha256"] = M.prereg_sha256()
        lab_state["L-LIMIT-2"] = "BUILT"
    else:
        lab_state["L-LIMIT-2"] = "NOT AVAILABLE"
    if L["misc"]:
        X = L["misc"]
        # `fmh_tables` runs BOTH books — the card book's zeros are themselves
        # the finding (194 of 195 card exits are stops, so the winner cells are
        # empty) and must be printed beside the union book, not suppressed.
        put(X.fmh_tables(lo_ms, hi_ms), "l_fmh",
            ["book", "arm", "asset", "entry_ms"])
        put(X.shadow_identity_checks(lo_ms, hi_ms), "shadow_identity", ["leg"])
        put(X.wallq_lab(v6, ch), "l_wallq", ["bucket", "key"])
        put(X.sprnt_lab(lo_ms, hi_ms), "l_spr_nt", ["population", "direction"])
        put(X.shadow_table(lo_ms, hi_ms, v6), "fleet_unscored", ["cell"])
        man["grid_sizes"] = X.GRID_SIZES6
        lab_state["L-FMH/L-WALLQ/L-SPR-NT/SHADOWS"] = "BUILT"
    else:
        lab_state["L-FMH/L-WALLQ/L-SPR-NT/SHADOWS"] = "NOT AVAILABLE"

    man["labs"] = lab_state
    man["champions"] = {f"{k[0]}/{k[1]}": v for k, v in sorted(ch.items())}
    man["counts"].update({
        "v6_campaigns": len(v6), "v5_control_campaigns": len(v5),
        "union_campaigns": len(union), "wall_campaigns": len(wallbook),
        "wall_exits": sum(1 for t in wallbook if t.exit_reason == "wall"),
        "v6_net_r": r4(sum(t.net_r for t in v6)),
        "v6_expectancy_r": r6(float(np.mean([t.net_r for t in v6]))),
        "v5_net_r": r4(sum(t.net_r for t in v5)),
        "v5_expectancy_r": r6(float(np.mean([t.net_r for t in v5]))),
        "v6_advances": sum(len(t.advances) for t in v6),
        "v5_advances": sum(len(t.advances) for t in v5),
        "league_rows": len(lg),
        "corridor_years": r4(cmeta["span_days"] / 365.25),
    })
    man["sha"] = W
    # EVERY TABLE'S KEY, ON THE RECORD — so F-KEY can re-check ALL of them on
    # disk instead of the nine somebody remembered to type into the fixture.
    man["keys"] = KEYS
    man["skipped_empty"] = SKIPPED
    man["elapsed_s"] = round(time.time() - t0, 1)
    (root / "build_manifest.json").write_text(json.dumps(man, indent=2,
                                                         sort_keys=True,
                                                         default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


if __name__ == "__main__":                                  # pragma: no cover
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true",
                    help="write to tierc6_run2/ for the determinism fixture")
    a = ap.parse_args()
    run(OUT_RERUN if a.rerun else OUT)
