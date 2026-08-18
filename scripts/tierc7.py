"""TIER-C7 · THE HYBRID R&H PROGRAM — the program.

RATIFIED operator 2026-08-17, resume word "TC7 GO", with P-AE-1 ruled
CARD-CONDITIONAL and the arm KEPT.

CLASS: measurement + FOUR pre-registered claims + pre-named labs.  D15 columns
everywhere, GATES NOWHERE.  LOAO-3/5 on every registration table [E1 law].
Every grid reported WHOLE.

────────────────────────────────────────────────────────────────────────────
THE CHAIN IS ONE CAMPAIGN, AND THAT DECIDES THE DENOMINATOR [D-R6]
────────────────────────────────────────────────────────────────────────────
A chain is a weave-exit or ladder-out followed by ONE re-entry.  D-R6 rules it
is a single campaign "for all accounting", and the sharpest consequence is the
one the pin does not spell out: **which R?**

THE CHAIN HAS ONE R, SET AT ITS FIRST ENTRY, AND THE RE-ENTRY IS **SIZED** TO
RISK IT.  The estate's accounting rule is "R = ENTRY stop distance", and a
campaign has one entry.  Leg 2 gets a FRESH structural stop at a DIFFERENT
distance, so holding one unit on both legs would hold the QUANTITY constant and
let the RISK float — which is not what "one campaign, one R" means.  Leg 2's
size is therefore `chain_R / leg2_own_R`: a stopped-out re-entry loses exactly
1.0 chain-R whatever its stop distance, and a winning one books its move in the
risk it actually took.

THIS WAS FOUND BY DISBELIEVING A GOOD NUMBER, AND IT IS THE LARGEST REPAIR IN
THE BUILD.  The first draft held one unit per leg.  SOLUSDT 2023-10-16
re-entered with an own-R of 1.5264 against a chain R of 0.4391 — **3.5x the
risk** — and booked its 17.89-point run as **+40.74 chain-R** when the move was
worth **11.72 R** against the risk actually taken.  That single campaign was
**75% of the entire chain arm's delta** and would have carried P-CHAIN-1 on its
own.  With sizing, the campaign books +12.24 R, the arm falls from +68.17 to
+59.62, and its max single-trade delta share falls from 0.7473 to 0.5462.

THE ALTERNATIVE — one unit per leg — is NOT taken, and the number above is why.
A wide re-entry stop must not be a free multiplier.

AND THE D12 CEILING IS APPLIED ONCE, TO THE CHAIN.  Funding accumulates across
both legs and the 1R cap is taken on the total — never per leg, which would
silently convert a 1R ceiling into a 2R one.  That is the same defect
`size_grid` names for S-SIZE and it is inert today only because the ceiling
binds on nothing at unit size.

────────────────────────────────────────────────────────────────────────────
THE FORK
────────────────────────────────────────────────────────────────────────────
Everything that does not change is BOUND from `tierc6` by identity.  What is
FORKED is the ride — because a ride that can exit to flat, re-enter, and abort
on excursion is a different loop — and the accounting, because a chain sums.
`F-C7-CTRL` is what makes the fork checkable: card v7 with every v7 knob at its
default IS card v6, and must reproduce the v6 book trade-for-trade before any
arm is scored.
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

import tierc6 as T6                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc3_baseline as T3                                         # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
import analytics as AN                                               # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key, log = TB.write_table, TB.assert_key, TB.log
MS_4H, MS_1D = TB.MS_4H, TB.MS_1D

frame, fractals, addctx = T6.frame, T6.fractals, T6.addctx
corridor, card_candidates, _idx_range = (T6.corridor, T6.card_candidates,
                                         T6._idx_range)
agg, d15, slices_of = T6.agg, T6.d15, T6.slices_of
agg_both, headline_v6, ear_weights = T6.agg_both, T6.headline_v6, T6.ear_weights
journal_frame = T6.journal_frame
cluster_boot, cluster_boot_diff, _ci_from = (T6.cluster_boot,
                                             T6.cluster_boot_diff, T6._ci_from)
FDR_Q = T6.FDR_Q

SEED = 20260817
OUT = ROOT / "research_outputs" / "tierc7"
OUT_RERUN = ROOT / "research_outputs" / "tierc7_run2"
TC6 = ROOT / "research_outputs" / "tierc6"

_WEAVE: dict[str, RC.Weave] = {}


def weave_of(sym: str) -> RC.Weave:
    if sym not in _WEAVE:
        _WEAVE[sym] = RC.Weave(frame(sym)["f"].c)
    return _WEAVE[sym]


# ═══════════════════════════════════════════════════════════ ONE LEG OF A RIDE
def _ride_leg(sym: str, card: RC.Card, direction: int, ti: int, entry_px: float,
              stop0: float, r_dist: float, hi_i: int,
              chain_r: float | None = None) -> dict:
    """ONE LEG.  Tier-C6's ride, plus the hybrid anchor, the weave and the abort.

    Within-bar order, adverse-first throughout:

        STOP -> BELL -> TIME STOP -> AE ABORT -> HARVEST -> WEAVE -> ADDS -> LADDER

    THE ABORT SITS BEFORE THE HARVEST AND THE WEAVE, AND THAT IS ITS SEMANTICS.
    P-AE-1 exits a campaign that has gone 0.60R against it.  A campaign at
    -0.60R is not a campaign that should first be allowed to book a harvest —
    the harvest fires on a band touch that can happen on the same bar as a deep
    adverse extreme, and letting it book first would credit the abort arm with
    a de-risk it only got because it was about to quit.  Placed before, the
    abort takes the whole remainder at that bar's close.

    THE WEAVE SITS AFTER THE HARVEST, for the mirror of the reason P-WALL-1's
    exit did in Tier-C6: the weave exits "the REMAINDER" [D-R4], so a harvest
    that fires on the same bar books its fraction at that close and the weave
    takes what is left at the SAME close.  The two together are a full exit at
    the close and the fractions still sum.

    THE ABORT IS MEASURED ON THE BAR'S ADVERSE EXTREME, NOT ITS CLOSE — a
    campaign that traded 0.60R against you reached 0.60R against you — and it
    FILLS at the close, because the rule is a decision taken on seeing the
    excursion, not a resting order at -0.60R. Naming both halves because a
    reader could reasonably assume either.

    WHAT WOULD MAKE THIS WRONG: a stop tested against the bar that created it,
    an abort that fills at the extreme it was measured on (that would be a
    resting order and a better fill than the rule earns), a weave on a bar the
    stop already closed, or a ladder advance applied to its own bar.
    """
    st = frame(sym)
    f, x = st["f"], st["x"]
    fr = fractals(sym, card.trail_l, card.trail_r) if card.trail else None
    ctx = addctx(sym) if card.adds_max else None
    wv = weave_of(sym) if (card.weave or card.reentry) else None
    d = direction
    R = float(chain_r if chain_r is not None else r_dist)
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

    for j in range(ti + 1, hi_i + 1):
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        unit_fav_r = (fav - entry_px) * d / R
        unit_adv_r = (adverse - entry_px) * d / R

        if not reached_1r:
            mae_to_1r = min(mae_to_1r, unit_adv_r)
            if unit_fav_r >= 1.0:
                reached_1r = True
        if not trail_armed and unit_fav_r >= card.trail_arm_after_r:
            trail_armed = True

        if card.harvest == "band":
            pe = RC.harvest_edge(float(f.e89[j - 1]), float(f.e316[j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(f.e89[j]), float(f.e316[j]), d)
            unit_fill_r = (float(f.c[j]) - entry_px) * d / R
            touch = (harv is None and h_armed
                     and RC.harvest_touched(float(f.h[j]), float(f.l[j]), edge, d)
                     and unit_fill_r >= card.harvest_min_unit_r)
        elif card.harvest == "fixed_r":
            edge = entry_px + d * card.harvest_fixed_r * R
            touch = harv is None and unit_fav_r >= card.harvest_fixed_r
        else:
            edge, touch = float("nan"), False

        # 1 · ADVERSE FIRST
        if (d == 1 and f.l[j] <= stop) or (d == -1 and f.h[j] >= stop):
            exit_i, exit_px, exit_reason = j, stop, "stop"
            if touch:
                blocked = "stop"
            break
        if (fav - entry_px) * d > (mfe - entry_px) * d:
            mfe = fav

        # 2 · the bell — the backstop [F-C4-c / F-C5-e]
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
            break

        # 4 · P-AE-1 · THE ABORT — measured on the extreme, filled at the close
        if card.ae_abort_r is not None and unit_adv_r <= -abs(card.ae_abort_r):
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "ae_abort"
            if touch:
                blocked = "ae_abort"
            break

        # 5 · the harvest
        if touch:
            fill = (RC.harvest_fill_px(f.c[j]) if card.harvest == "band"
                    else float(edge))
            harv = (j, fill, (fill - entry_px) * d / R)

        # 6 · D-R3/D-R4 · THE WEAVE — exit the remainder to FLAT
        if card.weave and wv is not None and RC.weave_fires(wv, j, d,
                                                            card.weave_k):
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "weave"
            break

        # 7 · the adds
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

        # 8 · the ladder — governs bar j + 1
        if card.trail and trail_armed:
            if card.hybrid_anchor:
                adv = RC.ladder_step(
                    fr, j, d, stop, float(f.c[j]), float(f.atr[j]),
                    float(f.e89[j]), f.open_ms,
                    buf_atr=RC.STOP_BUF_ATR + card.trail_extra_buf_atr,
                    rail_atr=RC.MIN_STOP_ATR,
                    min_advance_atr=card.trail_min_advance_atr,
                    forbidden=(None if card.seal_open
                               else T3.sealed_mask(f.open_ms)))
            else:
                adv = RC.trail_step(
                    fr, j, d, stop, float(f.c[j]), float(f.atr[j]), f.open_ms,
                    buf_atr=RC.RATCHET_BUF_ATR + card.trail_extra_buf_atr,
                    rail_atr=RC.RATCHET_RAIL_ATR,
                    forbidden=(None if card.seal_open
                               else T3.sealed_mask(f.open_ms)),
                    min_advance_atr=card.trail_min_advance_atr)
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)

    return {"own_r": abs(float(entry_px) - float(stop0)),
            "entry_i": ti, "entry_px": float(entry_px), "stop0": float(stop0),
            "exit_i": exit_i, "exit_px": float(exit_px),
            "exit_reason": exit_reason, "advances": advances, "harvest": harv,
            "blocked": blocked, "mfe": mfe, "adds": adds,
            "final_stop": stop,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r}


# ══════════════════════════════════════════════ D-R5/D-R6 · THE CHAIN
def _ride_chain(sym: str, card: RC.Card, direction: int, ti: int,
                entry_px: float, stop0: float, r_dist: float,
                hi_i: int) -> dict:
    """ONE CAMPAIGN, WHICH MAY HAVE TWO LEGS.

    After a WEAVE exit or a LADDER-OUT, D-R5 looks forward up to 24 bars for the
    first close back beyond the fast ribbon in the trend direction with the tide
    still agreeing, and re-enters with a FRESH structural stop.  Max one
    re-entry.

    "LADDER-OUT" IS DEFINED, BECAUSE THE PIN DOES NOT DEFINE IT.  It is a stop
    exit on a stop the ladder had ADVANCED — i.e. the campaign was taken out of
    a position it had already made money in, not stopped on its entry anchor.
    A plain entry-stop loss is NOT a ladder-out and does not earn a re-entry;
    reading it as one would re-enter every loser and make D-R5 a martingale.
    Stated because the two readings differ on most of the book.

    THE RE-ENTRY'S STOP IS STRUCTURAL AND FRESH — `struct_stop_4h` at the
    re-entry bar, railed — which is the card's own entry-anchor object, not a
    reuse of the first leg's stop.  If no structural anchor exists there, the
    chain simply does not re-enter: a re-entry without an anchor would have to
    invent a stop.

    WHAT WOULD MAKE THIS WRONG: re-entering after a plain entry-stop; more than
    one re-entry; a re-entry outside the 24-bar window or against the tide;
    scanning for the re-entry from the wrong bar (it starts the bar AFTER the
    exit — the exit bar is spent); or re-using leg 1's R for sizing while
    calling it a fresh stop.
    """
    st = frame(sym)
    f = st["f"]
    legs = [_ride_leg(sym, card, direction, ti, entry_px, stop0, r_dist, hi_i)]
    if not card.reentry:
        return {"legs": legs, "n_reentries": 0, "reentry_refused": ""}

    leg1 = legs[0]
    laddered_out = bool(leg1["exit_reason"] == "stop" and leg1["advances"]
                        and abs(leg1["final_stop"] - stop0) > 1e-12)
    if leg1["exit_reason"] not in ("weave",) and not laddered_out:
        return {"legs": legs, "n_reentries": 0,
                "reentry_refused": f"exit_reason={leg1['exit_reason']}"
                                   f"{' (entry-stop, not a ladder-out)' if leg1['exit_reason'] == 'stop' else ''}"}

    wv = weave_of(sym)
    d = direction
    x0 = leg1["exit_i"]
    hi_scan = min(x0 + RC.REENTRY_WINDOW_BARS, hi_i)
    for j in range(x0 + 1, hi_scan + 1):
        tide_ok = bool((float(f.e89[j]) - float(f.e316[j])) * d > 0.0)
        if not RC.reentry_close(wv, j, d, float(f.c[j]), tide_ok):
            continue
        atr_j = float(f.atr[j])
        if not (np.isfinite(atr_j) and atr_j > 0):
            continue
        stp = RC.struct_stop_4h(st["pv4"], j, float(f.c[j]), d, atr_j,
                                min_stop_atr=card.entry_rail_atr,
                                forbidden=(None if card.seal_open
                                           else T3.sealed_mask(f.open_ms)))
        if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            return {"legs": legs, "n_reentries": 0,
                    "reentry_refused": "no structural anchor at the re-entry bar"}
        # THE CHAIN'S R IS THE FIRST LEG'S — see the module docstring.
        legs.append(_ride_leg(sym, card, d, j, float(f.c[j]), stp.stop_px,
                              stp.r_dist, hi_i, chain_r=r_dist))
        return {"legs": legs, "n_reentries": 1, "reentry_refused": "",
                "reentry_stop_px": float(stp.stop_px),
                "reentry_r_dist_own": float(stp.r_dist)}
    return {"legs": legs, "n_reentries": 0,
            "reentry_refused": f"no qualifying close within "
                               f"{RC.REENTRY_WINDOW_BARS} bars"}


def _account_chain(sym: str, card: RC.Card, direction: int, r_dist: float,
                   chain: dict) -> dict:
    """ONE CAMPAIGN'S ACCOUNTING, ACROSS EVERY LEG [D-R6].

    Gross, fees and funding are summed over the legs and divided by the CHAIN's
    single `r_dist`.  The D12 ceiling is taken ONCE, on the chain's total
    funding — never per leg.

    THE FRACTION INVARIANT IS ASSERTED PER LEG AND THE CHAIN SUM IS ASSERTED
    TOO.  A harvest splits one leg into two fractions that must book that leg;
    the legs must then book the chain.  Two levels, both checked, because a
    chain that summed wrongly would look exactly like a card that performed
    differently.
    """
    st = frame(sym)
    f, funding = st["f"], st["fund"]
    d, bps = direction, RC.FEE_BPS_SIDE / 10_000.0
    q = float(card.harvest_frac)
    R = float(r_dist)

    def fund_leg(lo_j: int, hi_j: int, qty: float) -> float:
        s = 0.0
        for j in range(lo_j + 1, hi_j + 1):
            rate = funding.get(int(f.open_ms[j]))
            if rate:
                s += rate * float(f.c[j - 1]) * d * qty
        return s

    g_tot = fe_tot = u_tot = 0.0
    n1s: list = []
    n2s: list = []
    would_have = None
    add_r_tot = 0.0
    sizes: list = []
    for k, lg in enumerate(chain["legs"]):
        ti, xi, xpx = lg["entry_i"], lg["exit_i"], lg["exit_px"]
        e = lg["entry_px"]
        harv = lg["harvest"]
        # ═══ THE RE-ENTRY IS SIZED TO RISK THE CHAIN'S 1R, NOT TO HOLD ONE
        # ═══ UNIT.  This is the repair that matters most in this build.
        #
        # A chain has ONE R (leg 1's stop distance) and a re-entry gets a FRESH
        # structural stop, which is a DIFFERENT distance. Holding one unit on
        # both legs therefore does not hold the risk constant — it holds the
        # QUANTITY constant, which is not the same thing and is not what "one
        # campaign, one R" means.
        #
        # Measured on the first draft, which held one unit: SOLUSDT
        # 2023-10-16 re-entered with an own-R of 1.5264 against a chain R of
        # 0.4391 — 3.5x the risk — and booked its 17.89-point run as
        # **+40.74 chain-R** when the move was worth **11.72 R** against the
        # risk actually taken. That one campaign was 75% of the whole chain
        # arm's delta and would have carried the registration.
        #
        # So leg k > 0 is sized `chain_R / own_R`. A stopped-out re-entry then
        # loses exactly 1.0 chain-R, whatever its stop distance, and a winning
        # one books its move in the risk it actually took. The book stays
        # additive and a wide re-entry stop stops being a free multiplier.
        #
        # THE ALTERNATIVE — one unit per leg — is NOT taken, and the number
        # above is why.
        size = 1.0 if k == 0 else (R / float(lg["own_r"]) if lg["own_r"] else 0.0)
        sizes.append(size)
        if harv is None:
            g = size * (xpx - e) * d
            fe = bps * size * (e + xpx)
            u = fund_leg(ti, xi, size)
            n1 = n2 = None
        else:
            hj, hpx, _ = harv
            g1 = size * q * (hpx - e) * d
            fe1 = bps * size * q * (e + hpx)
            u1 = fund_leg(ti, hj, size * q)
            g2 = size * (1.0 - q) * (xpx - e) * d
            fe2 = bps * size * (1.0 - q) * (e + xpx)
            u2 = fund_leg(ti, xi, size * (1.0 - q))
            g, fe, u = g1 + g2, fe1 + fe2, u1 + u2
            n1, n2 = (g1 - fe1 - u1) / R, (g2 - fe2 - u2) / R
            if k == 0:
                gw = size * q * (xpx - e) * d
                fw = bps * size * q * (e + xpx)
                uw = fund_leg(ti, xi, size * q)
                would_have = (gw - fw - uw) / R
            # THE FRACTIONS MUST BOOK THEIR OWN LEG — exact, per leg.
            if abs((n1 + n2) - (g - fe - u) / R) > 1e-9:
                raise SystemExit(
                    f"HALT: the fractions do not book leg {k}. {sym} {ti}")
        n1s.append(n1)
        n2s.append(n2)
        for a in lg["adds"]:
            # adds ride at the LEG's size, for the same reason the leg does
            g += size * a.size * (xpx - a.px) * d
            fe += bps * size * a.size * (a.px + xpx)
            u += fund_leg(a.i, xi, size * a.size)
            add_r_tot += (size * a.size * (xpx - a.px) * d
                          - bps * size * a.size * (a.px + xpx)
                          - fund_leg(a.i, xi, size * a.size)) / R
        g_tot += g
        fe_tot += fe
        u_tot += u

    gross = g_tot / R
    fee = fe_tot / R
    fund_raw = u_tot / R
    cap = card.funding_ceiling_r
    fund_eff = (min(fund_raw, cap) if (cap is not None and fund_raw > cap)
                else fund_raw)
    net = gross - fee - fund_eff
    return {"leg_sizes": sizes, "gross_r": gross, "fee_r": fee,
            "funding_r": fund_eff,
            "funding_r_uncapped": fund_raw,
            "funding_ceiling_bound": bool(cap is not None and fund_raw > cap),
            "net_r": net, "n1": n1s[0], "n2": n2s[0],
            "add_r": add_r_tot if add_r_tot else None,
            "harvest_ride_would_have_r": would_have}


def replay(sym: str, card: RC.Card, lo_ms: int, hi_ms: int) -> tuple[list, list]:
    """Tier-C6's `replay`, re-pointed at the chain ride and chain accounting.

    ONE POSITION PER ASSET STILL HOLDS, and a chain occupies the slot until its
    LAST leg exits — `open_until` is the chain's final exit, not leg 1's.
    Reading it as leg 1's would let a second campaign open inside a chain and
    the book would hold two positions in one asset, which is the one thing this
    loop has always refused.
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
        # S-STOPGRID [D-R7] — the initial stop offset, rail respected.
        stop_px = float(stp.stop_px)
        if card.stop_grid_offset_atr:
            cand = stop_px - d * card.stop_grid_offset_atr * atr_sig
            rail = entry_px - d * card.entry_rail_atr * atr_sig
            stop_px = min(cand, rail) if d == 1 else max(cand, rail)
        r_dist = abs(entry_px - stop_px)
        if not (np.isfinite(r_dist) and r_dist > 0):
            if arm is not None:
                arm.reject = "degenerate_R"
            continue
        if arm is not None:
            arm.entered = True
            arm.reject = "entered"
            arm.entry_scored = True

        chain = _ride_chain(sym, card, d, ti, entry_px, stop_px, r_dist, hi_i)
        last = chain["legs"][-1]
        first = chain["legs"][0]
        open_until = last["exit_i"]
        acc = _account_chain(sym, card, d, r_dist, chain)
        anchor_ms = int(f.open_ms[stp.anchor_bar]) if stp.anchor_bar >= 0 else -1
        lb0, lb1 = _ms(RC.LOCKBOX_WAS[0]), _ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1
        all_adv = [a for lg in chain["legs"] for a in lg["advances"]]
        # ── THE JOURNAL'S CROSS-LEG COLUMNS, EACH FIXED ──────────────────
        # `mfe_r` MUST CARRY THE LEG'S SIZE. Leg 2 is held at
        # `chain_R/own_R`, so its favourable excursion in CHAIN-R is
        # `size * (mfe - entry) * d / chain_R`. Dividing by the chain's R
        # without the size published 57.31 R of "favourable excursion" on a
        # campaign whose risk-adjusted reach was a fraction of that — a
        # number no position ever had.
        mfe_r = max(sz * (lg["mfe"] - lg["entry_px"]) * d / r_dist
                    for sz, lg in zip(acc["leg_sizes"], chain["legs"]))
        # `stop_advanced_atr` AND `ratchet_exit` ARE THE LAST LEG'S, MEASURED
        # FROM THE LAST LEG'S OWN ENTRY STOP. Measuring the final stop of leg
        # 2 against the entry anchor of leg 1 splices two different positions
        # into one distance: 26 of 79 chains filed as ratchet exits had not
        # trailed at all on the leg that actually exited, and 8 published a
        # NEGATIVE advance.
        last_stop0 = float(last["stop0"])
        stop_adv_atr = (last["final_stop"] - last_stop0) * d / atr_sig
        ratchet_exit = bool(last["exit_reason"] == "stop" and last["advances"]
                            and abs(last["final_stop"] - last_stop0) > 1e-12)
        # A HARVEST ON LEG 2 IS NOT INVISIBLE. `harvested` is true if ANY leg
        # harvested; the `harvest_*` price fields carry the FIRST harvest,
        # because the Trade record has one slot and inventing a second would
        # change an inherited dataclass. `n_harvests` and the chain ledger
        # carry the rest.
        harv_legs = [k for k, lg in enumerate(chain["legs"]) if lg["harvest"]]
        harv = next((lg["harvest"] for lg in chain["legs"] if lg["harvest"]),
                    None)
        t = RC.Trade(
            symbol=sym, lane=kind, direction=d,
            arm_i=(arm.arm_i if arm is not None else sp.sweep_i),
            arm_ms=(arm.arm_ms if arm is not None else sp.sweep_ms),
            entry_i=ti, entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stop_px, r_dist=r_dist, anchor=stp.anchor,
            anchor_bar_ms=anchor_ms,
            anchor_was_sealed=bool(anchor_ms > 0 and lb0 <= anchor_ms <= lb1),
            atr_at_entry=atr_sig,
            disp_at_arming=(arm.disp if arm is not None else float("nan")),
            exit_i=last["exit_i"], exit_ms=int(f.open_ms[last["exit_i"]]),
            exit_px=last["exit_px"], exit_reason=last["exit_reason"],
            bars_held=last["exit_i"] - ti, scored=True,
            advances=all_adv, final_stop_px=last["final_stop"],
            stop_advanced_atr=stop_adv_atr,
            ratchet_exit=ratchet_exit,
            harvested=harv is not None,
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=first["blocked"],
            harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
            adds=[a for lg in chain["legs"] for a in lg["adds"]],
            add_r=acc["add_r"], spring=sp,
            mfe_r=mfe_r,
            mae_to_1r_r=first["mae_to_1r"], reached_1r=first["reached_1r"],
            gross_r=acc["gross_r"], fee_r=acc["fee_r"],
            funding_r=acc["funding_r"],
            funding_r_uncapped=acc["funding_r_uncapped"],
            funding_ceiling_bound=acc["funding_ceiling_bound"],
            net_r=acc["net_r"], net_r_harvest_half=acc["n1"],
            net_r_runner_half=acc["n2"], net_r_bellonly=None)
        object.__setattr__(t, "chain", chain)
        object.__setattr__(t, "n_harvests", len(harv_legs))
        object.__setattr__(t, "harvest_legs", tuple(harv_legs))
        object.__setattr__(t, "leg_sizes", tuple(acc["leg_sizes"]))
        object.__setattr__(t, "n_reentries", chain["n_reentries"])
        object.__setattr__(t, "leg1_exit_reason", first["exit_reason"])
        object.__setattr__(t, "reentry_refused", chain.get("reentry_refused", ""))
        trades.append(t)
    return arms, trades


def run_cell(card: RC.Card, lo_ms: int, hi_ms: int) -> list:
    out = []
    for s in RC.UNIVERSE:
        _, t = replay(s, card, lo_ms, hi_ms)
        out += t
    return out


# ═══════════════════════════════════════════════ E1 · THE LOAO-3/5 LINE
def loao(new: list, base: list, label: str, two_sample: bool = False) -> dict:
    """LEAVE-ONE-ASSET-OUT, ON EVERY REGISTRATION TABLE [E1 law].

    The estate's own lesson: ZEC is 82% of the book and dropping it flips every
    arm.  So an arm's headline is not enough — the question is how many of the
    five leave-one-out panels still exclude zero.

    THE BAR IS 3 OF 5 AND IT IS NAMED BEFORE THE LOOK.  It is not a
    significance threshold and is not treated as one; it is a robustness line
    printed beside the verdict so a reader can see whether an arm survives its
    own panel.  An arm that clears its CI and fails 3/5 has not been refuted —
    it has been shown to rest on one asset, which is a different fact and is
    reported as one.
    """
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    per = []
    for drop in sorted(RC.UNIVERSE):
        pv, pc = [], []
        for t in new:
            if t.symbol == drop:
                continue
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                pv.append(t.net_r - bu[k])
                pc.append(t.symbol)
        if two_sample:
            # THE PANEL MUST BE SCORED BY THE SAME RULER AS THE HEADLINE.
            # A paired LOAO on an arm that changes the campaign set carries the
            # headline's own bias into all five panels — which is how "5/5,
            # does not rest on ZEC" was published for an arm that clears ONLY
            # when ZEC is removed.
            av = [t.net_r for t in new if t.symbol != drop]
            ac = [t.symbol for t in new if t.symbol != drop]
            bv = [t.net_r for t in base if t.symbol != drop]
            bc = [t.symbol for t in base if t.symbol != drop]
            if len(av) < 2 or len(bv) < 2 or len(set(ac)) < 2:
                per.append({"dropped": drop, "n": len(av), "ci_lo": None,
                            "ci_hi": None, "excludes_zero": False,
                            "excludes_above": False, "excludes_below": False,
                            "note": "too few clusters"})
                continue
            pt = float(np.mean(av)) - float(np.mean(bv))
            ci = _ci_from(cluster_boot_diff(av, ac, bv, bc), pt)
            above = bool(ci["lo"] is not None and ci["lo"] > 0)
            below = bool(ci["hi"] is not None and ci["hi"] < 0)
            per.append({"dropped": drop, "n": len(av), "point": r6(pt),
                        "ci_lo": r6(ci["lo"]), "ci_hi": r6(ci["hi"]),
                        "excludes_zero": bool(above or below),
                        "excludes_above": above, "excludes_below": below,
                        "note": ""})
            continue
        if len(pv) < 2 or len(set(pc)) < 2:
            per.append({"dropped": drop, "n": len(pv), "ci_lo": None,
                        "ci_hi": None, "excludes_zero": False,
                        "note": "too few clusters to bootstrap"})
            continue
        ci = _ci_from(cluster_boot(pv, pc), float(np.mean(pv)))
        above = bool(ci["lo"] is not None and ci["lo"] > 0)
        below = bool(ci["hi"] is not None and ci["hi"] < 0)
        per.append({"dropped": drop, "n": len(pv),
                    "point": r6(float(np.mean(pv))),
                    "ci_lo": r6(ci["lo"]), "ci_hi": r6(ci["hi"]),
                    "excludes_zero": bool(above or below),
                    "excludes_above": above, "excludes_below": below,
                    "note": ""})
    n_ex = sum(1 for p in per if p["excludes_zero"])
    n_ab = sum(1 for p in per if p.get("excludes_above"))
    n_be = sum(1 for p in per if p.get("excludes_below"))
    # THE DIRECTION IS PUBLISHED, BECAUSE "5/5" IS NOT A VERDICT ON ITS OWN.
    # `excludes_zero` is true when a panel's interval clears zero in EITHER
    # direction, so a cell that is robustly WORSE than the control scores a
    # perfect 5/5 exactly as a cell that is robustly better does. The
    # S-STOPGRID lab hit this first: its +0.25 and +0.50 ATR cells read 5/5
    # while being reliably worse than the card. The halves are split out and
    # the 3/5 line is taken on the ABOVE half only, which is the direction an
    # arm is registered in.
    return {"loao_panels": len(per), "loao_excluding_zero": n_ex,
            "loao_excluding_above": n_ab, "loao_excluding_below": n_be,
            "loao_line": f"{n_ab}/{len(per)} above"
                         + (f", {n_be}/{len(per)} BELOW" if n_be else ""),
            "loao_clears_3_of_5": bool(n_ab >= 3),
            "loao_sign_note": (
                "the 3/5 line is taken on panels excluding zero ABOVE. A panel "
                "excluding zero BELOW is robust evidence the arm is WORSE, and "
                "counting it toward robustness would read a reliable loss as a "
                "reliable gain."),
            "loao_detail": "; ".join(
                f"-{p['dropped']}: [{p['ci_lo']}, {p['ci_hi']}]"
                f"{'*' if p['excludes_zero'] else ''}" for p in per),
            "loao_worst_drop": (min(
                (p for p in per if p["ci_lo"] is not None),
                key=lambda p: p.get("point", 0.0), default={"dropped": None}
            )["dropped"]),
            "_per": per}


# ═══════════════════════════════════════════════════════ THE REGISTRATIONS
def registration_text() -> pd.DataFrame:
    """THE TEXT BEFORE THE RESULT — four claims, their priors, their rulers and
    the caveat each one carries."""
    return pd.DataFrame([
        {"registration": "P-HYB-1", "prior_pct": 50,
         "claim": "the full hybrid card (v6 + the armed hybrid ladder + the "
                  "weave + one re-entry) beats card v6 on PAIRED per-campaign "
                  "expectancy",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "named_caveat": "the hybrid turns three knobs at once; the ablation "
                         "ladder is what says which one did the work, and it is "
                         "unscored by construction."},
        {"registration": "P-WEV-1", "prior_pct": 45,
         "claim": "the weave-exit ALONE, with no re-entry, beats card v6",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "named_caveat": "the weave's k-window is PINNED at 6 bars and NOT "
                         "SWEPT. It is an assumption, not a comparison."},
        {"registration": "P-CHAIN-1", "prior_pct": 50,
         "claim": "weave-exit PLUS one re-entry — the round-trip thesis itself "
                  "— beats card v6",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "named_caveat": "the re-entry is SIZED to risk the chain's 1R. Held "
                         "at one unit instead, one campaign was 75% of this "
                         "arm's delta. The sizing is the rule, not a "
                         "post-hoc adjustment, and it is stated because the "
                         "unsized number would have carried the arm."},
        {"registration": "P-AE-1", "prior_pct": 40,
         "claim": "exiting any campaign whose adverse excursion reaches 0.60R "
                  "beats card v6",
         "ruler": "the PAIRED per-campaign delta vs zero, asset-cluster 90% CI",
         "named_caveat": "RULED CARD-CONDITIONAL by the operator 2026-08-17. "
                         "The 0.60R threshold was pre-named from Tier-C6's "
                         "hazard curve, and the TC6-V audit then established "
                         "that the held-excursion distribution is CENSORED AT "
                         "THE CARD'S OWN 1R RAIL — 110 of 196 campaigns sit at "
                         "exactly -1.0R while the uncensored tape reaches "
                         "-4.59R. P(win | MAE >= 0.60R) = 7.03% is therefore a "
                         "fact about campaigns UNDER THIS CARD, not about the "
                         "market, and this arm is scored and read on that "
                         "reading alone."},
    ])


def score_registrations7(base: list, arms: dict[str, list]) -> pd.DataFrame:
    """FOUR ARMS, ALL PAIRED AGAINST CARD v6, EACH WITH ITS LOAO-3/5 LINE.

    THE RULER DEPENDS ON WHETHER THE ARM CHANGES THE CAMPAIGN SET, and this was
    the blocker of this build's own review.

    An arm that rides INSIDE the card's campaigns is scored on the PAIRED
    per-campaign delta — Tier-C5's law, and the reason its P-CASC-1 was paired.
    An arm that CHANGES WHICH CAMPAIGNS EXIST must be scored by the TWO-SAMPLE
    asset-cluster bootstrap, because a paired ruler cannot see the campaigns
    that stopped existing.

    THE CHAIN ARMS CHANGE THE SET. A chain holds its asset's slot until its last
    leg exits, so 7 campaigns the control took never open — and the bias is not
    neutral. When a chain's re-entry captures the very move the control booked
    as a SEPARATE campaign, the arm is CREDITED for it inside the surviving twin
    while the control's campaign that captured the same move is DELETED from the
    comparison and never debited.

    Measured, on ZECUSDT: the control takes two campaigns over 2026-04-23 ->
    2026-05-10 worth +25.5692 R; the hybrid takes one chain worth +25.3148 R.
    On that tape the hybrid is 0.2544 R WORSE — and the paired ruler credits it
    +24.8061 R, which is 54.6% of the entire +45.4748 paired delta. Across all
    7 blocked slots the paired ruler credits +29.3562 R where the account earned
    +3.7723 R.

    So `cluster_boot_diff` — imported by this module and, in the first draft,
    called ZERO times — is now the PRIMARY ruler wherever `unpaired_base_n > 0`.
    The paired number is kept, printed, and labelled as conditional on the
    shared set. It is not deleted, because it is a true statement about the
    campaigns both books took; it is simply not the claim.

    THE PAIRING KEY CARRIES THE LANE, because two lanes can enter the same asset
    on the same bar.  UNPAIRED CAMPAIGNS ARE COUNTED AND PRINTED, not dropped in
    silence: a chain occupies its asset's slot for longer, so the chain arms
    legitimately hold FEWER campaigns than the base, and a reader must be able
    to see how many comparisons the delta actually rests on.
    """
    rows = []
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    ref = _ci_from(cluster_boot(bnet, bcl), float(np.mean(bnet)))
    rows.append({
        "registration": "(reference)", "arm": "CARD v6 vs zero",
        "prior_pct": None, "n": len(base),
        "expectancy_r": r6(float(np.mean(bnet))), "net_r": r4(sum(bnet)),
        "ci_on": "the card's own expectancy vs zero — the bar, scored through "
                 "the same ruler as everything asked to clear it",
        "ci_point": r6(ref["point"]), "ci_lo": r6(ref["lo"]),
        "ci_hi": r6(ref["hi"]), "p_one_sided": r6(ref["p_one_sided"]),
        "verdict": ("SUPPORTED" if (ref["lo"] or 0) > 0 else "NOT SUPPORTED"),
        "note": "not an acceptance test; excluded from m",
        "loao_line": "—", "loao_clears_3_of_5": None})

    for reg, prior, book in (("P-HYB-1", 50, arms["hybrid"]),
                             ("P-WEV-1", 45, arms["weave"]),
                             ("P-CHAIN-1", 50, arms["chain"]),
                             ("P-AE-1", 40, arms["ae"])):
        pv, pc = [], []
        for t in book:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                pv.append(t.net_r - bu[k])
                pc.append(t.symbol)
        ci_paired = _ci_from(cluster_boot(pv, pc),
                             float(np.mean(pv)) if pv else None)
        rs = [t.net_r for t in book]
        # THE TWO-SAMPLE RULER — the same asset draw resampled into both books.
        av, ac = [t.net_r for t in book], [t.symbol for t in book]
        pt2 = float(np.mean(av)) - float(np.mean(bnet))
        ci_two = _ci_from(cluster_boot_diff(av, ac, bnet, bcl), pt2)
        changes_set = (len(base) - len(pv)) > 0 or (len(book) - len(pv)) > 0
        ci = ci_two if changes_set else ci_paired
        ruler = ("TWO-SAMPLE asset-cluster (the arm CHANGES the campaign set)"
                 if changes_set else
                 "PAIRED per-campaign delta (the arm rides inside the set)")
        lo_ = loao(book, base, reg, two_sample=changes_set)
        good = bool(ci["lo"] is not None and ci["lo"] > 0)
        rows.append({
            "registration": reg, "arm": f"{reg} vs card v6 (PAIRED)",
            "prior_pct": prior, "n": len(book),
            "expectancy_r": r6(float(np.mean(rs))), "net_r": r4(sum(rs)),
            "ci_on": ruler,
            "ci_point": r6(ci["point"]), "ci_lo": r6(ci["lo"]),
            "ci_hi": r6(ci["hi"]), "p_one_sided": r6(ci["p_one_sided"]),
            "verdict": "SUPPORTED" if good else "NOT SUPPORTED",
            "ruler_is_two_sample": bool(changes_set),
            # BOTH RULERS PRINTED, ALWAYS — the one that decides and the one
            # that does not, so a reader can see the gap rather than infer it.
            "paired_ci_point": r6(ci_paired["point"]),
            "paired_ci_lo": r6(ci_paired["lo"]),
            "paired_ci_hi": r6(ci_paired["hi"]),
            "paired_p_one_sided": r6(ci_paired["p_one_sided"]),
            "paired_verdict_would_be": (
                "SUPPORTED" if (ci_paired["lo"] or 0) > 0 else "NOT SUPPORTED"),
            "two_sample_ci_point": r6(ci_two["point"]),
            "two_sample_ci_lo": r6(ci_two["lo"]),
            "two_sample_ci_hi": r6(ci_two["hi"]),
            "two_sample_p_one_sided": r6(ci_two["p_one_sided"]),
            "ruler_note": (
                "an arm that rides INSIDE the campaign set is scored PAIRED; an "
                "arm that CHANGES which campaigns exist is scored TWO-SAMPLE, "
                "because a paired ruler credits the arm for moves it captured "
                "inside a surviving twin while the control campaign that "
                "captured the same move is deleted from the comparison and "
                "never debited."),
            "paired_n": len(pv),
            "paired_delta_r_total": r4(sum(pv)) if pv else None,
            "unpaired_arm_n": len(book) - len(pv),
            "unpaired_base_n": len(base) - len(pv),
            # ═══ THE CROWD-OUT, PRICED — and it is the largest caveat on the
            # ═══ two arms that clear.
            #
            # A paired test is the right ruler for a rule that rides INSIDE a
            # campaign. The chain arms are not purely inside-campaign: a chain
            # holds its asset's slot until its LAST leg exits, so campaigns the
            # base took never open in the arm at all. The paired delta cannot
            # see them, because they have no counterpart to pair with.
            #
            # Measured: the base book holds 7 campaigns the hybrid never takes,
            # and they are worth +25.58 R to the base. So the arm's paired
            # delta of +45.47 R and its WHOLE-BOOK advantage of +19.89 R are
            # both true and they differ by exactly that crowd-out.
            #
            # Neither number is the answer on its own. The paired delta is the
            # registered claim and is what the CI is computed on; the whole-book
            # difference is what an account would actually have earned. Both are
            # published on the row, and the arm that forgoes campaigns is not
            # allowed to bank the ones it never took.
            "unpaired_base_net_r": r4(sum(
                v for k, v in bu.items()
                if k not in {(t.symbol, t.lane, t.entry_ms) for t in book})),
            "whole_book_difference_r": r4(sum(rs) - sum(bnet)),
            "paired_minus_wholebook_r": r4((sum(pv) if pv else 0.0)
                                           - (sum(rs) - sum(bnet))),
            "crowd_out_note": (
                "the PAIRED delta scores only campaigns BOTH books took. A "
                "chain holds its asset's slot longer, so campaigns the control "
                "took may never open in this arm — they are counted in "
                "`unpaired_base_n` and PRICED in `unpaired_base_net_r`. Where "
                "those differ from zero, the paired delta and the whole-book "
                "difference are different questions and both are printed."),
            "note": "",
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            **d15(book, base)})

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
        f"m = {m} ACCEPTANCE TESTS ACTUALLY RUN. P-LAG-1 was CONDITIONAL and "
        f"its condition was evaluated in TC6-V and NOT MET — the top-vs-bottom "
        f"lag-group delta was +0.0616 with CI [-0.7819, +0.9566] — so it is "
        f"report-only, is not a test, and m is unchanged at {m}. "
        f"q = {FDR_Q}, bar = q/m = {bar:.5f}.")
    d["in_sample"] = True
    return d


def ablation(base: list, arms: dict[str, list], lo_ms: int,
             hi_ms: int) -> pd.DataFrame:
    """THE ABLATION LADDER — UNSCORED ATTRIBUTION, ONE CODE PATH.

    Every cell is the same `run_cell` with a different card, so a difference
    between cells is a difference between RULES and not between programs.

    THE INTERACTION COLUMN IS PRINTED, and Tier-C4 is why: there the ratchet
    and the harvest each looked negative alone while the pair was worth +3.45 R
    of interaction, so "the harvest costs 3.18 R" was a sentence the ablation
    table made available and the shipped card made false. The same column is
    here so the same sentence cannot be written about the weave.

    THE STOP GRID IS EXCLUDED BY CONSTRUCTION [D-R7]: it is a diagnostic, its
    best cell is not a rung, and putting it on this ladder would invite exactly
    the promotion the commission forbids.

    ONE RUNG IS ADDED TO THE COMMISSIONED LADDER, AND IT IS THE ONE THAT
    ANSWERS THE TABLE'S OWN QUESTION.  The commission lists v6 / ladder-only /
    weave-only / weave+re-entry / FULL HYBRID — which cannot separate the weave
    from the re-entry, because the only cell containing a re-entry also
    contains the weave.  Measured: the weave ALONE is worth -0.5198 R, and
    RE-ENTRY ALONE (no weave) is worth +38.1513 R of the +45.4175 that
    weave+re-entry earns.  Of the 79 re-entries in the chain arm, 67 follow a
    plain LADDER-OUT and only 12 follow a weave.  **The round-trip thesis is
    carried by the re-entry, not by the weave**, and a ladder without this rung
    would have attributed it to the pair.  Added as UNSCORED attribution, which
    is what this whole table is.
    """
    b0 = sum(t.net_r for t in base)
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    rows = []
    for name, book in (("v6 (control)", base),
                       ("ladder-only", arms["ladder"]),
                       ("weave-only", arms["weave"]),
                       ("RE-ENTRY ONLY (no weave)", arms["reonly"]),
                       ("weave + re-entry", arms["chain"]),
                       ("FULL HYBRID", arms["hybrid"])):
        net = sum(t.net_r for t in book)
        # THE MARGINAL IS PAIRED, AND THE RAW DIFFERENCE IS PRINTED BESIDE IT.
        # A chain occupies its asset's slot for longer, so the chain cells hold
        # 189 campaigns against the control's 196 — and a raw total difference
        # across different campaign COUNTS is not an attribution, it is two
        # books of different sizes subtracted. The paired sum compares the same
        # campaigns to themselves. The first draft printed only the raw
        # difference and it overstated the chain rungs.
        pv = [t.net_r - bu[(t.symbol, t.lane, t.entry_ms)] for t in book
              if (t.symbol, t.lane, t.entry_ms) in bu]
        rows.append({"cell": name, "n": len(book), "net_r": r4(net),
                     "expectancy_r": r6(net / len(book)) if book else None,
                     "paired_marginal_r": r4(sum(pv)) if pv else None,
                     "paired_n": len(pv),
                     "raw_total_difference_r": r4(net - b0),
                     "raw_difference_is_not_an_attribution": bool(
                         len(book) != len(base)),
                     "n_reentries": sum(getattr(t, "n_reentries", 0)
                                        for t in book),
                     **d15(book, base)})
    d = pd.DataFrame(rows)
    # THE INTERACTION: the full hybrid against the sum of its parts' marginals.
    parts = float(d.loc[d["cell"].isin(["ladder-only", "weave + re-entry"]),
                        "paired_marginal_r"].sum())
    full = float(d.loc[d["cell"] == "FULL HYBRID",
                       "paired_marginal_r"].iloc[0])
    d["interaction_r"] = None
    d.loc[d["cell"] == "FULL HYBRID", "interaction_r"] = r4(full - parts)
    d["interaction_note"] = (
        f"FULL HYBRID's marginal {full:+.4f} R against the sum of "
        f"ladder-only and weave+re-entry marginals {parts:+.4f} R = "
        f"interaction {full - parts:+.4f} R. Any sentence of the form 'the "
        f"weave is worth X' that ignores this column is false about the "
        f"shipped card [the Tier-C4 lesson].")
    d["scored"] = False
    d["tier"] = "attribution — UNSCORED, gates nothing"
    return d


# ═══════════════════════════════════════════════════════════════ THE DRIVER
ARM_CARDS = {
    "control": RC.CARD_V6_CONTROL, "ladder": RC.CARD_LADDER_ONLY,
    "weave": RC.CARD_WEAVE_ONLY, "chain": RC.CARD_WEAVE_RE,
    "hybrid": RC.CARD_HYBRID, "ae": RC.CARD_AE,
    "reonly": RC.Card(name="v7-reentry-only", reentry=True),
}


LABS_EXPECTED = {"stopgrid": "tierc7_lab_stopgrid",
                 "weave": "tierc7_lab_weave",
                 "chain": "tierc7_lab_chain",
                 "regime": "tierc7_lab_regime"}


def _labs():
    """The four labs, imported individually — and a MISSING lab is LOUD.

    THE FIRST DRAFT SWALLOWED THE ImportError AND LOGGED "NOT AVAILABLE".
    A full TIER-C7 run then completed GREEN with THREE OF FOUR LABS ABSENT, and
    both filed manifests recorded it in a field nobody was asserting on. That is
    the same defect class as a `put()` that returns silently on an empty frame:
    "this lab produced nothing" and "this lab was never written" became the same
    observation.

    The import is still individual — one broken lab must not take the other
    three down, and a build that loses all four to one syntax error would report
    "no labs" when the truth is "one lab is broken". But the failure is now
    RECORDED PER LAB with its exception, the manifest carries a
    `labs_missing` list, and `F-C7-LABS` asserts that list is EMPTY. A lab that
    is absent will fail the suite instead of decorating the log.
    """
    mods, missing = {}, []
    for k, name in LABS_EXPECTED.items():
        try:
            mods[k] = __import__(name)
        except Exception as e:                                # noqa: BLE001
            mods[k] = None
            missing.append(f"{k} ({name}): {type(e).__name__}: {e}")
            log(f"    LAB {k}: NOT AVAILABLE — {type(e).__name__}: {e}")
    mods["__missing__"] = missing
    return mods


def run(root: Path) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "stage": "TIER-C7 hybrid R&H", "sha": {},
                 "counts": {}}
    KEYS: dict[str, list] = {}
    SKIPPED: list[str] = []
    log("=" * 78)
    log("TIER-C7 · THE HYBRID R&H PROGRAM")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")

    lo_ms, hi_ms, cmeta = corridor()
    man["corridor"] = {k: v for k, v in cmeta.items()
                       if k not in ("wall_clock_at_run", "cache_lag_hours")}
    log(f"  CORRIDOR {cmeta['panel_start']} -> {cmeta['last_closed_4h_close']} "
        f"({cmeta['span_days']} d)")

    books = {k: run_cell(c, lo_ms, hi_ms) for k, c in ARM_CARDS.items()}
    base = books["control"]
    for k, b in books.items():
        log(f"  {k:9} n={len(b):4d} net={sum(t.net_r for t in b):+9.4f} "
            f"reentries={sum(getattr(t, 'n_reentries', 0) for t in b)}")

    root.mkdir(parents=True, exist_ok=True)
    W = {}

    def put(df, name, key):
        if df is None or not len(df):
            log(f"    (skip {name} — empty)")
            SKIPPED.append(name)
            return
        df = df.copy()
        df.attrs = {}
        df.columns = [str(c) for c in df.columns]
        W[name] = write_table(df, name, key, root)
        KEYS[name] = list(key)

    head = pd.concat(
        [headline_v6(books[k], nm, lo_ms, hi_ms)
         for k, nm in (("control", "CARD v6 (control)"),
                       ("hybrid", "v7 FULL HYBRID"))] +
        [headline_v6(books[k], nm, lo_ms, hi_ms, echo=True)
         for k, nm in (("control", "CARD v6 (control)"),
                       ("hybrid", "v7 FULL HYBRID"))],
        ignore_index=True)
    put(head, "headline", ["label", "aggregation", "universe", "group", "key"])
    put(registration_text(), "registration_text", ["registration"])
    put(score_registrations7(base, books), "registrations",
        ["registration", "arm"])
    put(ablation(base, books, lo_ms, hi_ms), "ablation", ["cell"])
    put(pd.DataFrame(RC.register_rows()), "register", ["key"])
    put(journal_frame(books["hybrid"]), "trade_journal_hybrid",
        ["asset", "entry_ms"])
    put(journal_frame(base), "trade_journal_control", ["asset", "entry_ms"])

    # the chain ledger the journal cannot hold — two legs on one row
    ch_rows = []
    for t in books["hybrid"]:
        acc = _account_chain(t.symbol, RC.CARD_HYBRID, t.direction, t.r_dist,
                             t.chain)
        for k, lg in enumerate(t.chain["legs"]):
            f = frame(t.symbol)["f"]
            ch_rows.append({
                "asset": t.symbol, "entry_ms": int(t.entry_ms),
                "entry_ts": iso(t.entry_ms), "leg": k,
                "leg_entry_ts": iso(int(f.open_ms[lg["entry_i"]])),
                "leg_entry_px": r6(lg["entry_px"]),
                "leg_stop0_px": r6(lg["stop0"]),
                "leg_own_r": r6(lg["own_r"]),
                "chain_r": r6(t.r_dist),
                "leg_size": r6(acc["leg_sizes"][k]),
                "leg_exit_ts": iso(int(f.open_ms[lg["exit_i"]])),
                "leg_exit_px": r6(lg["exit_px"]),
                "leg_exit_reason": lg["exit_reason"],
                "leg_advances": len(lg["advances"]),
                "n_reentries": t.n_reentries,
                "reentry_refused": t.reentry_refused,
                "chain_net_r": r6(t.net_r)})
    put(pd.DataFrame(ch_rows), "chain_ledger", ["asset", "entry_ms", "leg"])

    L = _labs()
    lab_state = {}
    if L["stopgrid"]:
        S = L["stopgrid"]
        put(S.stopgrid_table(lo_ms, hi_ms, base), "s_stopgrid", ["cell"])
        put(S.anchor_bakeoff(lo_ms, hi_ms, base), "l_anchor", ["cell"])
        lab_state["S-STOPGRID/L-ANCHOR"] = "BUILT"
    else:
        lab_state["S-STOPGRID/L-ANCHOR"] = "NOT AVAILABLE"
    if L["weave"]:
        Wv = L["weave"]
        put(Wv.weave_quality(lo_ms, hi_ms), "l_weave_quality", ["key"])
        put(Wv.too_early_cost(lo_ms, hi_ms), "l_weave_cost", ["key"])
        lab_state["L-WEAVE"] = "BUILT"
    else:
        lab_state["L-WEAVE"] = "NOT AVAILABLE"
    if L["chain"]:
        C = L["chain"]
        put(C.chain_ledger(lo_ms, hi_ms), "l_re_chains", ["asset", "entry_ms"])
        put(C.sizing_sensitivity(lo_ms, hi_ms), "l_re_sizing", ["reading"])
        lab_state["L-RE"] = "BUILT"
    else:
        lab_state["L-RE"] = "NOT AVAILABLE"
    if L["regime"]:
        G = L["regime"]
        put(G.regime_table(lo_ms, hi_ms), "l_regime", ["book", "dimension", "band_label"])
        put(G.candidates(lo_ms, hi_ms), "l_regime_candidates", ["candidate"])
        lab_state["L-REGIME"] = "BUILT"
    else:
        lab_state["L-REGIME"] = "NOT AVAILABLE"

    man["labs"] = lab_state
    man["labs_missing"] = L["__missing__"]
    if L["__missing__"]:
        log(f"    *** {len(L['__missing__'])} LAB(S) MISSING — "
            f"F-C7-LABS will fail: {L['__missing__']}")
    man["keys"] = KEYS
    man["skipped_empty"] = SKIPPED
    man["sha"] = W
    man["counts"] = {
        f"{k}_n": len(b) for k, b in books.items()} | {
        f"{k}_net_r": r4(sum(t.net_r for t in b)) for k, b in books.items()} | {
        "reentries_hybrid": sum(t.n_reentries for t in books["hybrid"]),
        "weave_exits_hybrid": sum(1 for t in books["hybrid"]
                                  if t.exit_reason == "weave"),
        "ae_aborts": sum(1 for t in books["ae"] if t.exit_reason == "ae_abort"),
        "corridor_days": cmeta["span_days"]}
    man["elapsed_s"] = round(time.time() - t0, 1)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    a = ap.parse_args()
    run(OUT_RERUN if a.rerun else OUT)
