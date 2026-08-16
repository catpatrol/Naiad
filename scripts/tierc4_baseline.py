"""TIER-C4 · THE MEAN CARD — v3 + the LPS-trail ratchet + the creek/ice harvest.

RATIFIED operator 2026-08-16 ("run tc4 with just the anchor 4H trade; ratchet
and harvest per your lean; a mean for the average trade we can tune later").
Drafted APOLLO · Executor HEPHAESTUS · Seed 20260816.

CLASS: MEASUREMENT, NOT REGISTRATION.  m = 0.  ONE pre-named card — no grid, no
sweep.  The estate's selection guard is LOADED and CALLED, and it IDLES with
m = 0 because there is nothing to select; the call and its verdict are in the
manifest so "no sweep happened" is a record and not a claim.  NO lockbox read
for outcomes.  No estate write.  No live orders.

────────────────────────────────────────────────────────────────────────────
THIS FILE IS A FORK OF `tierc3_baseline.py`, AND THE FORK IS AN IMPORT
────────────────────────────────────────────────────────────────────────────
`import tierc3_baseline as T3` — and through it `tierc2_baseline as TB`.  Every
unchanged part of the program is USED, not copied: the loaders, the atomic
table writer, F-KEY, the funnel, the lead-in census and table, the headline
aggregation, the monthly equity, the d-strip, the anchor-lookback disclosure,
and the WHOLE Amendment-B1 analytics tape.  `F-C4-INHERIT` asserts those
identities with `is`, and asserts that this module redefines none of them.

BUT NOT ALL OF IT IS AN IMPORT, AND THE HONEST STATEMENT SAYS SO.  The two
amendments live inside the ride, and the loop around the ride had to be
rewritten to carry them — so the ENTRY half of `replay_asset` (the arming walk,
the tide and displacement gates, the trigger selection, the occupancy gate, the
reject naming, the anchor call and the scored test) is a HAND TRANSCRIPTION of
Tier-C3's, not a binding.  `is` cannot reach transcribed code.  The claim is
therefore made where it CAN be falsified: every table the ride cannot touch —
`funnel`, `lead_in_census`, `lead_in_trades`, `strip_d_unscored`,
`anchor_lookback_disclosure` — must come out CONTENT-HASH-IDENTICAL to
Tier-C3's filed one, and F-C4-INHERIT asserts all five.  A single drifted
arming, gate, trigger, occupancy decision, anchor or entry stop would move one
of those hashes.

WHAT IS REDEFINED HERE, AND WHY — the decision-path diffs, and nothing else:

    replay_asset    THE RIDE, and only the ride: the RATCHET advances the stop
                    on a confirmed favourable (2,2) fractal; the HARVEST takes
                    50% off at the first opposing-band touch. Entry, anchor,
                    entry rail, tide, window, trigger, bell and toll are
                    untouched — the amendments cannot move an entry.
    journal_frame   the two amendments' arithmetic, per trade, plus the halves.
    stop_geometry   the advanced stop beside the entry stop.
    ratchet_ledger  NEW. One row per stop ADVANCE, with its full provenance.
    harvest_ledger  NEW. One row per harvest FILL, with the band edge it met.
    delta_v3_v4     NEW. v3 vs v4 per arming, with the GIVE-BACK accounted:
                    what the amendments captured and what they surrendered.
    ablation_unscored  NEW. Five cells through this one code path — four
                    for the amendments, one for the seal floor 'printed
                    both ways'.
    headline_triptych  NEW. v4 beside v3 beside v1, all three read or built
                    under their own filed cards.

The retired 1H anchor lens is NOT reachable from this program at all.  v1's
number is READ from Tier-C2's filed headline and never recomputed, so this
build cannot move a predecessor's figure while comparing itself to it.

────────────────────────────────────────────────────────────────────────────
THE SEAL — INHERITED, AND EXTENDED TO THE SECOND PUBLISHED PRICE
────────────────────────────────────────────────────────────────────────────
F-C3-a semantics are inherited byte-for-byte: sealed bars are masked out of
ENTRY-anchor eligibility and a tranche with no admissible anchor is NOT TAKEN.
The RATCHET publishes a SECOND price quoted from a named bar — the trailing
pivot — which is paid out when the advanced stop fires, so it is the same class
of object and takes the same mask.

THE MASK DID NOT BIND ON THIS CORRIDOR, AND THAT IS MEASURED, NOT INFERRED.
The tempting argument — "every ratchet pivot confirms after an entry that is
itself after the seal closes" — DOES NOT FOLLOW, because a fractal's PIVOT BAR
precedes its confirmation by RATCHET_PIVOT_R bars and could in principle sit
before the entry.  So F-C4-SEAL resolves every advance's pivot back to its own
raw bar and checks THAT bar: 0 of 21 sealed, earliest 2025-10-18.  The
measured margin is wider still — the earliest advance confirms 5 bars after its
entry, so no pivot bar in this book is even at the entry, let alone before it.
See also finding F-C4-i: the "new pivot" gate is on the CONFIRMATION bar, which
is a named reading and did not bind here.

USAGE
    ~/venvs/naiad/bin/python scripts/tierc4_baseline.py --stage all
    ~/venvs/naiad/bin/python scripts/tierc4_baseline.py --stage all --rerun
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

# THE FORK, AS AN IMPORT.  Tier-C3's program, used rather than transcribed.
import tierc3_baseline as T3                                        # noqa: E402
import tierc2_baseline as TB                                        # noqa: E402
import tierc4_rules as RC                                           # noqa: E402
import analytics as AN                                              # noqa: E402

# ── byte-inherited helpers, bound so the call sites read like the original ──
_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, assert_key = TB.write_table, TB.assert_key
load_klines, load_funding = TB.load_klines, TB.load_funding
_idx_range = TB._idx_range
MS_4H, MS_1H, MS_1D = TB.MS_4H, TB.MS_1H, TB.MS_1D
KLINES = TB.KLINES
CENSUS_RIDE_ONLY = TB.CENSUS_RIDE_ONLY
DISPLAY_ONLY_HEADER = TB.DISPLAY_ONLY_HEADER
log, LOG_LINES = TB.log, TB.LOG_LINES

# ── byte-inherited PROGRAM PARTS.  These are Tier-C3's own functions, bound.
sealed_mask = T3.sealed_mask
funnel_table = T3.funnel_table
lead_in_census = T3.lead_in_census
lead_in_table = T3.lead_in_table
anchor_lookback_disclosure = T3.anchor_lookback_disclosure

INHERITED_FROM_TIERC3 = (
    "sealed_mask", "funnel_table", "lead_in_census", "lead_in_table",
    "anchor_lookback_disclosure", "SCORED", "LOCKBOX", "CENSUS_ERA",
    "PINNING", "WINDOWS",
)
INHERITED_FROM_TIERC2 = (
    "_ms", "iso", "r4", "r6", "pct", "_content_sha", "_round_floats",
    "write_table", "assert_key", "load_klines", "load_funding", "_idx_range",
    "headline_rows", "monthly_equity", "_maxdd_r", "_top_decile_share",
    "strip_d_table", "daily_spine", "build_level_series", "tape_rows",
    "ribbon_state", "tape_inventory", "_daily_atr_map", "_ribbon_bands",
    "_single_wall",
)

SEED = 20260816                 # printed and unused — no stochastic step exists
OUT = ROOT / "research_outputs" / "tierc4"
OUT_RERUN = ROOT / "research_outputs" / "tierc4_run2"
V1_TABLES = ROOT / "research_outputs" / "tierc2"
V3_TABLES = ROOT / "research_outputs" / "tierc3"

# ── the windows, as ruled — HELD IDENTICAL to v3, which held them identical to
#    v1.  The v3<->v4 delta is a delta in the RIDE and in nothing else.
SCORED = T3.SCORED                              # 2025-10-06 -> 2026-01-31
LOCKBOX = T3.LOCKBOX                            # NOT COMPUTED — sealed
CENSUS_ERA = T3.CENSUS_ERA                      # display-only
PINNING = T3.PINNING                            # display-only, F-7 truncated
WINDOWS = T3.WINDOWS                            # the SAME dict object

YARDSTICK_LABEL = "YARDSTICK v4 — PROVISIONAL (one regime, n small)"


# ═══════════════════════════════════════════════════════ STAGE A · replay v4
def replay_asset(sym: str, win_name: str, k4: pd.DataFrame, k1: pd.DataFrame,
                 funding: dict[int, float], *,
                 ratchet: bool = True, harvest: bool = True,
                 seal_floor: bool = True) -> tuple[list, list]:
    """The v4 rule card, ridden bar by bar.  Returns (armings, trades).

    Tier-C3's `replay_asset` with exactly two changes, BOTH INSIDE THE RIDE:

      [ratchet]  when a favourable (2,2) fractal CONFIRMS on bar j, the stop
                 advances to beyond it, railed 1.0 x ATR from bar j's close,
                 monotone.  The new stop is applied AFTER bar j finishes, so it
                 governs bar j+1 onward — a stop derived from a bar's close is
                 never tested against that same bar's low.
      [harvest]  the FIRST bar whose extreme reaches the opposing 89/316 band
                 takes 50% off AT THAT BAR'S CLOSE.  Once per campaign.

    WITHIN-BAR ORDER is the card's, and it is adverse-first throughout:
    STOP -> BELL -> HARVEST -> RATCHET.  A stop takes the whole remainder at
    the stop [F-4].  A bell takes the whole remainder at the close, which makes
    a same-bar harvest economically identical — so it is NOT recorded, and the
    campaign is stamped `harvest_blocked_by` instead of silently losing the
    fact.  The ratchet is last because its result governs the NEXT bar.

    Everything else is Tier-C3's, unchanged: EMAs, ATR, the (5,5) anchor grid
    and the fractal grid are computed over the FULL loaded history and only
    then restricted to the window, so a window edge can never move an indicator,
    an anchor or a trail.

    `ratchet` / `harvest` / `seal_floor` are keyword arguments ONLY so the
    ablation can re-ask this same question with one amendment switched off at a
    time, through this one code path rather than a second copy.  Their defaults
    ARE the ratified card plus the CLASS line's seal floor.
    """
    span = WINDOWS[win_name]["span"]
    win_lo, win_hi = _ms(span[0]), _ms(span[1]) + MS_1D - 1
    lead_lo = win_lo - RC.LEAD_IN_DAYS * MS_1D

    f = RC.build_4h(k4["open_time"].to_numpy(np.int64),
                    k4["open"].to_numpy(float), k4["high"].to_numpy(float),
                    k4["low"].to_numpy(float), k4["close"].to_numpy(float))
    pv4 = RC.build_pivots_4h(k4["high"].to_numpy(float),
                             k4["low"].to_numpy(float))
    fr4 = RC.build_fractals_4h(k4["high"].to_numpy(float),
                               k4["low"].to_numpy(float))
    forbid4 = sealed_mask(f.open_ms) if seal_floor else None
    sealed = sealed_mask(f.open_ms)

    lead_i, hi_i = _idx_range(f.open_ms, lead_lo, win_hi)
    if hi_i < lead_i:
        return [], []

    arms = RC.armings(sym, f, lead_i, hi_i)
    trades: list[RC.Trade] = []
    open_until = -1              # 4h index the open position releases at
    x = RC._crosses(f)
    bps = RC.FEE_BPS_SIDE / 10_000.0

    for a in arms:
        a.in_window = bool(a.arm_ms >= win_lo)          # F-5 bookkeeping
        a.entry_scored = False
        if not a.tide_ok:
            a.reject = "tide"
            continue
        if not a.d_ok:
            a.reject = "d"
            continue

        trig_flags = x["t_up"] if a.direction == 1 else x["t_dn"]
        end = min(a.window_end_i, hi_i + 1)
        cand = np.flatnonzero(trig_flags[a.arm_i:end])
        if cand.size == 0:
            a.reject = "no_trigger"
            continue
        ti = int(a.arm_i + cand[0])
        a.trigger_i, a.trigger_ms = ti, int(f.open_ms[ti])

        # ONE POSITION PER ASSET.  Under v4 the ride can end EARLIER (a ratchet
        # stop) or on the same bar, never later — so occupancy can free sooner
        # and admit an arming v3 refused.  That is a real population difference
        # and the delta table joins OUTER because of it.
        if ti <= open_until:
            a.reject = "position_open"
            continue

        entry_px = float(f.c[ti])
        atr_sig = float(f.atr[ti])
        st = RC.struct_stop_4h(pv4, ti, entry_px, a.direction, atr_sig,
                               forbidden=forbid4)
        if st is None:
            a.reject = "no_struct_anchor"
            if seal_floor and RC.struct_stop_4h(
                    pv4, ti, entry_px, a.direction, atr_sig,
                    forbidden=None) is not None:
                a.reject = "anchor_sealed"
            continue
        if not (np.isfinite(st.r_dist) and st.r_dist > 0):
            a.reject = "degenerate_R"
            continue
        stop_px, r_dist = st.stop_px, st.r_dist

        a.entered = True
        a.reject = "entered"
        scored = bool(f.open_ms[ti] >= win_lo)
        a.entry_scored = scored

        # ── THE RIDE.  [F-4] stop first, every bar, at its CURRENT level. ──
        def ride(honour_stop: bool, use_ratchet: bool, use_harvest: bool):
            stop = float(stop_px)
            advances: list = []
            harv = None                       # (bar, fill px, band edge)
            n_harv = 0                        # against HARVEST_MAX_PER_CAMPAIGN
            blocked = ""
            mfe = float(entry_px)
            # THE "FROM BELOW" PRECONDITION, carried as state. A touch is a
            # CROSSING: the campaign must have been on its own side of the
            # band's near edge on the LAST CLOSED bar. Evaluated on closes so
            # it is unambiguous and causal — at bar ti+1 the last closed bar is
            # the entry bar, so this is "did the trade start outside the band".
            h_armed = False
            for j in range(ti + 1, hi_i + 1):
                prev_edge = RC.harvest_edge(float(f.e89[j - 1]),
                                            float(f.e316[j - 1]), a.direction)
                if not h_armed and RC.harvest_outside(float(f.c[j - 1]),
                                                      prev_edge, a.direction):
                    h_armed = True
                edge = RC.harvest_edge(float(f.e89[j]), float(f.e316[j]),
                                       a.direction)
                touch = (use_harvest and h_armed
                         and n_harv < RC.HARVEST_MAX_PER_CAMPAIGN
                         and RC.harvest_touched(float(f.h[j]), float(f.l[j]),
                                                edge, a.direction))
                # 1 · ADVERSE FIRST — the stop takes the whole remainder
                if honour_stop and ((a.direction == 1 and f.l[j] <= stop)
                                    or (a.direction == -1 and f.h[j] >= stop)):
                    return (j, stop, "stop", advances, harv,
                            "stop" if touch else blocked, mfe)
                # ── MFE, AND WHY IT IS UPDATED *HERE* AND NOT AT THE TOP ──
                # The favourable extreme is credited only for bars the position
                # was held THROUGH. On a stop bar the campaign closed at the
                # stop, and F-4 models no intrabar path — so crediting that same
                # bar's favourable extreme would assume the good half of the bar
                # happened before the bad half, which is exactly the assumption
                # adverse-first refuses. A bell or corridor_end exits at the
                # CLOSE, so its bar WAS held through and is credited.
                # (Found by the post-build adversarial review. It changed one
                # campaign's give-back — a 1-bar NEAR long whose entire MFE was
                # its own stop bar — and no headline figure.)
                ex = float(f.h[j]) if a.direction == 1 else float(f.l[j])
                if (ex - entry_px) * a.direction > (mfe - entry_px) * a.direction:
                    mfe = ex
                # 2 · the bell takes the whole remainder at the close
                if a.direction == 1:
                    bell = ("bell_12_89" if bool(x["w_dn"][j])
                            else "bell_89_316" if bool(x["b_dn"][j]) else None)
                else:
                    bell = ("bell_12_89" if bool(x["w_up"][j])
                            else "bell_89_316" if bool(x["b_up"][j]) else None)
                if bell:
                    return (j, float(f.c[j]), bell, advances, harv,
                            "bell" if touch else blocked, mfe)
                # 3 · the harvest — HARVEST_FRACTION off at the fill price the
                #     register's HARVEST_FILL rule names, counted against
                #     HARVEST_MAX_PER_CAMPAIGN rather than against a literal.
                if touch:
                    harv = (j, RC.harvest_fill_px(f.c[j]), float(edge))
                    n_harv += 1
                # 4 · the ratchet — governs bar j + 1 onward
                if use_ratchet:
                    adv = RC.ratchet_step(fr4, j, a.direction, stop,
                                          float(f.c[j]), float(f.atr[j]),
                                          f.open_ms, forbidden=forbid4)
                    if adv is not None:
                        advances.append(adv)
                        stop = float(adv.new_stop)
            return (hi_i, float(f.c[hi_i]), "corridor_end", advances, harv,
                    blocked, mfe)

        xi, xpx, xreason, advs, harv, blocked, mfe = ride(True, ratchet, harvest)
        open_until = xi
        final_stop = float(advs[-1].new_stop) if advs else float(stop_px)

        def _fund(lo_j: int, hi_j: int, qty: float) -> float:
            """Funding in PRICE units over bars (lo_j, hi_j], on `qty` units.

            Convention byte-inherited from Tier-C2: the stamp is keyed to the
            bar's OPEN and charged on the LAST CLOSED price.  The size charged
            is the size held INTO that bar, which is the full unit up to and
            including the harvest bar (the reduction happens at its CLOSE) and
            the runner thereafter.
            """
            s = 0.0
            for j in range(lo_j + 1, hi_j + 1):
                rate = funding.get(int(f.open_ms[j]))
                if rate:
                    s += rate * float(f.c[j - 1]) * a.direction * qty
            return s

        def account(exit_i: int, exit_px: float, hv):
            """(gross_r, fee_r, funding_r, net_r, net_half1, net_half2).

            With no harvest this is Tier-C3's arithmetic exactly — one unit in,
            one unit out.  With a harvest the unit is split and EACH HALF BOOKS
            ITS OWN R: the entry fee splits 50/50, each half pays its own exit
            fee, and funding accrues on the size actually held.  The two halves
            sum to the campaign identically, which F-C4-HARV asserts to 1e-9.
            """
            if hv is None:
                gross = (exit_px - entry_px) * a.direction
                fee = bps * (entry_px + exit_px)
                fund = _fund(ti, exit_i, 1.0)
                return (gross / r_dist, fee / r_dist, fund / r_dist,
                        (gross - fee - fund) / r_dist, None, None)
            hj, hpx, _edge = hv
            q = RC.HARVEST_FRACTION
            g1 = q * (hpx - entry_px) * a.direction
            f1 = bps * q * (entry_px + hpx)
            u1 = _fund(ti, hj, q)
            g2 = (1.0 - q) * (exit_px - entry_px) * a.direction
            f2 = bps * (1.0 - q) * (entry_px + exit_px)
            u2 = _fund(ti, exit_i, 1.0 - q)
            gross, fee, fund = g1 + g2, f1 + f2, u1 + u2
            n1, n2 = (g1 - f1 - u1) / r_dist, (g2 - f2 - u2) / r_dist
            net = (gross - fee - fund) / r_dist
            # THE HALVES ARE THE CAMPAIGN, AT FULL PRECISION, OR THE BUILD
            # HALTS.  The written columns are rounded to 6 dp, so the fixture
            # can only ever assert this to the arithmetic bound of three
            # independently-rounded values (2e-6). The exact identity is
            # asserted HERE, before any rounding, because "the halves book
            # their own R" is a card sentence and not a display convention.
            if abs((n1 + n2) - net) > 1e-9:
                raise SystemExit(
                    f"HALT: the halves do not book the campaign. "
                    f"{sym} entry {int(f.open_ms[ti])}: "
                    f"{n1!r} + {n2!r} != {net!r} "
                    f"(|diff| = {abs((n1 + n2) - net):.3e})")
            return (gross / r_dist, fee / r_dist, fund / r_dist, net, n1, n2)

        tr = RC.Trade(
            symbol=sym, direction=a.direction, arm_i=a.arm_i, arm_ms=a.arm_ms,
            entry_i=ti, entry_ms=int(f.open_ms[ti]),
            entry_px=entry_px if scored else float("nan"),
            stop_px=stop_px if scored else float("nan"),
            r_dist=r_dist if scored else float("nan"),
            pivot_anchor=st.anchor if scored else float("nan"),
            anchor_bar_ms=(int(f.open_ms[st.anchor_bar])
                           if st.anchor_bar >= 0 else -1),
            anchor_in_lockbox=bool(st.anchor_bar >= 0 and sealed[st.anchor_bar]),
            n_eligible_anchors=st.n_eligible,
            atr_at_entry=atr_sig if scored else float("nan"),
            disp_at_arming=a.disp,
            exit_i=xi, exit_ms=int(f.open_ms[xi]),
            exit_px=xpx if scored else float("nan"),
            exit_reason=xreason, bars_held=xi - ti,
            scored=scored, armed_in_lead_in=not a.in_window,
            pivot_stop_px=st.pivot_stop_px if scored else float("nan"),
            pivot_dist=st.pivot_dist if scored else float("nan"),
            rail_dist=st.rail_dist if scored else float("nan"),
            rail_binding=st.rail_binding,
            advances=advs,
            final_stop_px=final_stop if scored else float("nan"),
            stop_advanced_atr=(((final_stop - stop_px) * a.direction / atr_sig)
                               if (scored and atr_sig) else float("nan")),
            ratchet_exit=bool(xreason == "stop" and advs
                              and abs(final_stop - stop_px) > 1e-12),
            harvested=bool(harv is not None),
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if (harv and scored) else None),
            harvest_edge_px=(harv[2] if (harv and scored) else None),
            harvest_bars_after_entry=((harv[0] - ti) if harv else None),
            harvest_blocked_by=blocked,
            entered_outside_band=RC.harvest_outside(
                entry_px, RC.harvest_edge(float(f.e89[ti]), float(f.e316[ti]),
                                          a.direction), a.direction),
            mfe_px=mfe if scored else float("nan"),
            mfe_r=(((mfe - entry_px) * a.direction / r_dist)
                   if scored else float("nan")),
        )

        # THE SEAL.  An unscored lead-in trade is ridden for occupancy and is
        # accounted for NOTHING — no gross, no net, no bell-only, no prices.
        if scored:
            # THE BELL-ONLY COUNTERFACTUAL keeps its v3 MEANING exactly: ride to
            # the bell honouring no stop and managing nothing. Same object, same
            # definition, comparable across all three card versions.
            bi, bpx, _br, _ba, _bh, _bb, _bm = ride(False, False, False)
            g_r, fee_r, fund_r, net, n1, n2 = account(xi, xpx, harv)
            gb_r, feeb_r, fundb_r, netb, _, _ = account(bi, bpx, None)
            tr.gross_r, tr.fee_r, tr.funding_r, tr.net_r = g_r, fee_r, fund_r, net
            tr.net_r_harvest_half, tr.net_r_runner_half = n1, n2
            tr.gross_r_bellonly = gb_r
            tr.net_r_bellonly = netb
            tr.exit_reason_bellonly = _br
            tr.exit_ms_bellonly = int(f.open_ms[bi])
        trades.append(tr)

    return arms, trades


# ═══════════════════════════════════════════════════════ the v4 record
def journal_frame(trades: list) -> pd.DataFrame:
    """Tier-C3's journal, plus the two amendments' arithmetic per trade."""
    rows = []
    for t in trades:
        if not t.scored:
            continue
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "arm_ms": t.arm_ms, "arm_ts": iso(t.arm_ms),
            "armed_in_lead_in": bool(t.armed_in_lead_in),
            "disp_at_arming": r6(t.disp_at_arming),
            "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
            "pivot_anchor": r6(t.pivot_anchor),
            "anchor_bar_ms": int(t.anchor_bar_ms),
            "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
            "anchor_in_lockbox": bool(t.anchor_in_lockbox),
            "n_eligible_anchors": int(t.n_eligible_anchors),
            "pivot_stop_px": r6(t.pivot_stop_px),
            "pivot_dist": r6(t.pivot_dist), "rail_dist": r6(t.rail_dist),
            "rail_binding": bool(t.rail_binding),
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(t.atr_at_entry),
            "r_over_atr": r6(t.r_dist / t.atr_at_entry if t.atr_at_entry else None),
            # ── THE RATCHET ──────────────────────────────────────────────
            "n_advances": len(t.advances),
            "final_stop_px": r6(t.final_stop_px),
            "stop_advanced_atr": r6(t.stop_advanced_atr),
            "ratchet_exit": bool(t.ratchet_exit),
            "first_advance_ts": (iso(t.advances[0].conf_ms) if t.advances
                                 else None),
            "last_advance_ts": (iso(t.advances[-1].conf_ms) if t.advances
                                else None),
            # ── THE HARVEST ──────────────────────────────────────────────
            "harvested": bool(t.harvested),
            "harvest_ts": iso(t.harvest_ms) if t.harvest_ms else None,
            "harvest_px": r6(t.harvest_px),
            "harvest_edge_px": r6(t.harvest_edge_px),
            "harvest_bars_after_entry": t.harvest_bars_after_entry,
            "harvest_blocked_by": t.harvest_blocked_by or None,
            "entered_outside_band": bool(t.entered_outside_band),
            "net_r_harvest_half": r6(t.net_r_harvest_half),
            "net_r_runner_half": r6(t.net_r_runner_half),
            # ── the ride ─────────────────────────────────────────────────
            "mfe_px": r6(t.mfe_px), "mfe_r": r6(t.mfe_r),
            "exit_ms": t.exit_ms, "exit_ts": iso(t.exit_ms),
            "exit_px": r6(t.exit_px), "exit_reason": t.exit_reason,
            "bars_held": t.bars_held,
            "gross_r": r6(t.gross_r), "fee_r": r6(t.fee_r),
            "funding_r": r6(t.funding_r), "net_r": r6(t.net_r),
            "net_r_bellonly": r6(t.net_r_bellonly),
            "exit_reason_bellonly": t.exit_reason_bellonly,
            # ── Amendment B1 · RECORDED ONLY.  Nothing reads these back. ──
            "wall_family_at_arming": None, "dist_atr_at_arming": None,
            "dist_atr_at_trigger": None, "coloc_n": None,
        })
    return pd.DataFrame(rows)


def ratchet_ledger(trades: list) -> pd.DataFrame:
    """ONE ROW PER STOP ADVANCE, with the whole arithmetic that produced it.

    A trailing stop is a price that gets paid out.  Under F-C3-a's own logic
    that makes it the same class of object as the entry anchor, so it gets the
    same treatment: the bar it was quoted from is named, the seal is checked,
    and the rail leg is re-derivable from this table alone.
    """
    rows = []
    for t in trades:
        if not t.scored:
            continue
        for k, adv in enumerate(t.advances):
            rows.append({
                "asset": t.symbol, "entry_ms": t.entry_ms,
                "advance_seq": k + 1,
                "direction": "long" if t.direction == 1 else "short",
                "conf_ms": adv.conf_ms, "conf_ts": iso(adv.conf_ms),
                "governs_from_ts": iso(adv.conf_ms + MS_4H),
                "pivot_val": r6(adv.pivot_val),
                "pivot_bar_ms": adv.pivot_bar_ms,
                "pivot_bar_ts": iso(adv.pivot_bar_ms),
                "pivot_bar_in_lockbox": bool(
                    _ms(LOCKBOX[0]) <= adv.pivot_bar_ms
                    <= _ms(LOCKBOX[1]) + MS_1D - 1),
                "atr_at_conf": r6(adv.atr), "close_at_conf": r6(adv.close),
                "cand_px": r6(adv.cand_px), "rail_px": r6(adv.rail_px),
                "prev_stop_px": r6(adv.prev_stop),
                "new_stop_px": r6(adv.new_stop),
                "advance_atr": r6(abs(adv.new_stop - adv.prev_stop) / adv.atr),
                "rail_binding": bool(adv.rail_binding),
                "buffer_binding": bool(not adv.rail_binding),
                "dist_from_close_atr": r6(adv.dist_from_close_over_atr),
                "bars_after_entry": adv.conf_i - t.entry_i,
                "is_final_stop": bool(k == len(t.advances) - 1),
                "paid_out": bool(k == len(t.advances) - 1
                                 and t.exit_reason == "stop"),
            })
    return pd.DataFrame(rows)


def harvest_ledger(trades: list) -> pd.DataFrame:
    """ONE ROW PER HARVEST FILL — the touch, the edge it met, and the half's
    own R.  A campaign that touched the band on its exit bar appears here only
    as a `blocked_by` row on the journal, never as a fill."""
    rows = []
    for t in trades:
        if not t.scored or not t.harvested:
            continue
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "harvest_ms": int(t.harvest_ms), "harvest_ts": iso(t.harvest_ms),
            "bars_after_entry": int(t.harvest_bars_after_entry),
            "band_edge_px": r6(t.harvest_edge_px),
            "fill_px": r6(t.harvest_px),
            "entry_px": r6(t.entry_px),
            "fraction": RC.HARVEST_FRACTION,
            # THE PRICE MOVE AT THE FILL, EXPRESSED IN R ON A FULL UNIT.
            # Named `unit_move_at_harvest_r` and NOT `half_move_r`: the half's
            # own booked R is `net_r_harvest_half` beside it, and the two differ
            # by the fraction plus costs. The first draft called this
            # `half_move_r`, sitting between `fraction = 0.5` and two genuine
            # half quantities, where a reader could only tell them apart by
            # reading the source. Found by the post-build adversarial review.
            "unit_move_at_harvest_r": r6((t.harvest_px - t.entry_px)
                                         * t.direction / t.r_dist),
            "net_r_harvest_half": r6(t.net_r_harvest_half),
            "net_r_runner_half": r6(t.net_r_runner_half),
            "net_r_campaign": r6(t.net_r),
            "runner_exit_ts": iso(t.exit_ms),
            "runner_exit_reason": t.exit_reason,
        })
    return pd.DataFrame(rows)


def stop_geometry(trades: list) -> pd.DataFrame:
    """R in ATR, the toll in R, and the advanced stop beside the entry stop.

    `r_over_atr` still has a floor of MIN_STOP_ATR by construction — R is the
    ENTRY stop distance and the ratchet does NOT re-denominate it.  The new
    columns say how far the trail actually travelled and whether it was the
    thing that ended the campaign.
    """
    rows = []
    for t in trades:
        if not t.scored:
            continue
        atr = t.atr_at_entry
        rows.append({
            "asset": t.symbol, "entry_ms": t.entry_ms,
            "entry_ts": iso(t.entry_ms),
            "direction": "long" if t.direction == 1 else "short",
            "r_dist": r6(t.r_dist), "atr_at_entry": r6(atr),
            "r_over_atr": r6(t.r_dist / atr if atr else None),
            "anchor_bar_ts": iso(t.anchor_bar_ms) if t.anchor_bar_ms > 0 else None,
            "anchor_in_lockbox": bool(t.anchor_in_lockbox),
            "pivot_dist_over_atr": r6(t.pivot_dist / atr if atr else None),
            "rail_binding": bool(t.rail_binding),
            "widening_atr": r6((t.r_dist - t.pivot_dist) / atr if atr else None),
            "under_g8c_rail": bool(atr and t.r_dist < 0.5 * atr),
            "under_c3_rail": bool(atr and t.r_dist < RC.MIN_STOP_ATR * atr - 1e-12),
            "n_advances": len(t.advances),
            "final_stop_px": r6(t.final_stop_px),
            "stop_advanced_atr": r6(t.stop_advanced_atr),
            "ratchet_exit": bool(t.ratchet_exit),
            "harvested": bool(t.harvested),
            "toll_share_of_r_pct": r4(100.0 * t.fee_r),
            "bars_held": t.bars_held, "exit_reason": t.exit_reason,
            "mfe_r": r6(t.mfe_r),
            "net_r": r6(t.net_r), "net_r_bellonly": r6(t.net_r_bellonly),
            "stop_cost_r": r6(t.net_r_bellonly - t.net_r),
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════ THE DELTA TABLE · v3 vs v4
def delta_table(trades: list, v3_trades: list) -> pd.DataFrame:
    """v3 vs v4, PER ARMING, with THE GIVE-BACK ACCOUNTED.

    Join key `(asset, direction, arm_ms)`, OUTER — the two card versions need
    not agree on which armings become trades, because a ratchet stop can free
    the one-position-per-asset slot earlier than v3's bell would have.  A row on
    one side only is the finding, not an error.

    v3's FILED journal (`research_outputs/tierc3/trade_journal.parquet`) is the
    authority for v3's NUMBERS and is never recomputed.  The v3 ABLATION CELL
    is used for exactly one thing the filed table does not carry — the maximum
    favourable excursion — and the two are RECONCILED here on net R before that
    column is trusted, so the borrowed quantity cannot smuggle in a different
    v3.

    THE GIVE-BACK, defined once and used everywhere downstream:
        mfe_r_v3            the campaign's best unrealised R UNDER THE v3 RIDE,
                            counting only bars the v3 position was held through
        giveback_v3_r       mfe_r_v3 - net_r_v3, what v3 handed back
        captured_r          net_r_v4 - net_r_v3, what the two amendments took
        surrendered_r       mfe_r_v3 - net_r_v4, how far the v4 result sits
                            below the v3 ride's own peak

    READ THOSE THREE HONESTLY, BECAUSE TWO OF THEM ARE EASY TO OVER-READ.

    `captured_r + surrendered_r == giveback_v3_r` is an ALGEBRAIC IDENTITY —
    net_r_v4 cancels — so it is arithmetic self-consistency and NOT evidence
    about the amendments.  It is asserted downstream to catch a wiring error,
    and it is named as a tautology wherever it is printed.  The only one of the
    three that carries information about v4 is `captured_r`.

    And `surrendered_r` is NOT "what v4 left on the table".  On the campaigns
    the ratchet closed early the v4 position was already flat while the v3 ride
    was still running, so `mfe_r_v3` reaches past v4's exit: the number is a
    COMPARISON AGAINST A COUNTERFACTUAL PEAK, not an unrealised opportunity
    that v4 could have taken.  (ETH is the clearest case: the v3 peak lands
    2025-11-21, a fortnight after v4 exited on 11-07.)
    """
    p = V3_TABLES / "trade_journal.parquet"
    if not p.exists():
        raise SystemExit(f"HALT: v3 journal absent at {p} — the DELTA TABLE is "
                         f"a deliverable and may not be faked. Re-run "
                         f"scripts/tierc3_baseline.py --stage all first.")
    v3 = pd.read_parquet(p)
    keep = ["asset", "direction", "arm_ms", "arm_ts", "r_over_atr", "entry_ts",
            "entry_px", "stop_px", "r_dist", "exit_ts", "exit_reason", "net_r",
            "net_r_bellonly"]
    v3 = v3[keep].add_prefix("v3_").rename(
        columns={"v3_asset": "asset", "v3_direction": "direction",
                 "v3_arm_ms": "arm_ms"})

    # the v3 ABLATION CELL, for MFE only — reconciled against the filed table
    mfe3 = pd.DataFrame([{
        "asset": t.symbol,
        "direction": "long" if t.direction == 1 else "short",
        "arm_ms": t.arm_ms, "v3_mfe_r": r6(t.mfe_r),
        "v3_cell_net_r": r6(t.net_r)}
        for t in v3_trades if t.scored])
    # THE BORROWED COLUMN'S LICENCE, CHECKED PER ROW AND IN BOTH DIRECTIONS.
    # The cell is not an independent reproduction of Tier-C3 — it runs THIS
    # program's transcribed entry code — so this reconciliation is the only
    # thing standing between the ablation and a silent fork, and it is an
    # OUTER merge on purpose: a LEFT merge would drop a cell row the filed
    # journal does not have, and a row the cell failed to produce would arrive
    # as NaN and be quietly excused. Both are HALTs.
    assert_key(mfe3, ["asset", "direction", "arm_ms"], "delta.v3_mfe")
    v3 = v3.merge(mfe3, on=["asset", "direction", "arm_ms"], how="outer",
                  validate="1:1", indicator="_cell")
    one_sided = v3[v3["_cell"] != "both"]
    if len(one_sided):
        raise SystemExit(
            "HALT: the v3 ABLATION CELL and Tier-C3's FILED journal do not "
            f"cover the same armings — {len(one_sided)} one-sided row(s): "
            f"{one_sided[['asset', 'direction', 'arm_ms', '_cell']].to_dict('records')}")
    if v3["v3_cell_net_r"].isna().any() or v3["v3_mfe_r"].isna().any():
        raise SystemExit("HALT: the v3 ABLATION CELL produced a NULL net R or "
                         "MFE. A missing number may not be excused into a NaN.")
    gap = (v3["v3_cell_net_r"].astype(float)
           - v3["v3_net_r"].astype(float)).abs()
    if float(gap.max()) > 1e-4:
        raise SystemExit(
            "HALT: the v3 ABLATION CELL disagrees with Tier-C3's FILED journal "
            f"PER TRADE (max |diff| = {float(gap.max()):.3e} over {len(v3)} "
            "rows). The MFE column may only be borrowed from a cell that "
            "reproduces the filed number trade by trade, or it is a different "
            "v3 wearing the label.")
    v3 = v3.drop(columns=["_cell"])

    v4 = journal_frame([t for t in trades if t.scored])
    v4cols = ["asset", "direction", "arm_ms", "arm_ts", "r_over_atr",
              "entry_ts", "entry_px", "stop_px", "r_dist", "exit_ts",
              "exit_reason", "net_r", "net_r_bellonly", "mfe_r", "n_advances",
              "stop_advanced_atr", "ratchet_exit", "harvested", "harvest_ts",
              "harvest_bars_after_entry", "net_r_harvest_half",
              "net_r_runner_half", "armed_in_lead_in"]
    if len(v4):
        v4 = v4[v4cols].add_prefix("v4_").rename(
            columns={"v4_asset": "asset", "v4_direction": "direction",
                     "v4_arm_ms": "arm_ms"})
    else:
        v4 = pd.DataFrame(columns=["asset", "direction", "arm_ms"])

    assert_key(v3, ["asset", "direction", "arm_ms"], "delta.v3")
    assert_key(v4, ["asset", "direction", "arm_ms"], "delta.v4")
    d = v3.merge(v4, on=["asset", "direction", "arm_ms"], how="outer",
                 indicator=True, validate="1:1")
    d["present"] = d["_merge"].map({"both": "both", "left_only": "v3_only",
                                    "right_only": "v4_only"})
    d = d.drop(columns=["_merge"])
    d["arm_ts"] = d["arm_ms"].map(lambda m: iso(int(m)))

    def _sub(b, a):
        return [None if (pd.isna(u) or pd.isna(v)) else r6(float(v) - float(u))
                for u, v in zip(a, b)]

    d["delta_net_r"] = _sub(d["v4_net_r"], d["v3_net_r"])
    d["captured_r"] = d["delta_net_r"]
    d["giveback_v3_r"] = _sub(d["v3_mfe_r"], d["v3_net_r"])
    d["surrendered_r"] = _sub(d["v3_mfe_r"], d["v4_net_r"])
    # THE ENTRY IS UNTOUCHED BY BOTH AMENDMENTS — so on every shared arming the
    # R denominator must be IDENTICAL. Asserted here rather than assumed,
    # because every R figure in the delta is a ratio to it.
    both = d[d["present"] == "both"]
    if len(both):
        gap = (both["v4_r_dist"].astype(float)
               - both["v3_r_dist"].astype(float)).abs().max()
        if gap > 1e-9:
            raise SystemExit(
                f"HALT: R denominator moved between v3 and v4 on a shared "
                f"arming (max |diff| = {gap:.3e}). The TC-4 amendments are "
                f"ride-only and MAY NOT touch the entry stop.")
    for c in ("v3_r_over_atr", "v3_net_r", "v3_net_r_bellonly", "v3_entry_px",
              "v3_stop_px", "v3_r_dist", "v3_mfe_r"):
        d[c] = d[c].map(r6)
    return d


# ══════════════════════════════════════ THE ABLATION — UNSCORED, four cells
def ablation_table() -> tuple[pd.DataFrame, dict]:
    """UNSCORED ABLATION — the "tune later" substrate, F-C4-ABLATE.

    Five cells, each the SAME `replay_asset` with different keywords — one code
    path, not five copies:

        V3          ratchet OFF, harvest OFF -> must REPRODUCE Tier-C3's filed
                                                net R, TRADE BY TRADE, or every
                                                marginal below is measuring the
                                                fork rather than the amendment
        RATCHET     ratchet ON,  harvest OFF
        HARVEST     ratchet OFF, harvest ON
        BOTH        ratchet ON,  harvest ON  = THE SHIPPED CARD
        BOTH_NOSEAL the shipped card with the CLASS line's seal floor OFF —
                    the card LITERALLY. This is the "printed both ways" the
                    SEAL FLOOR line and the inherited SEAL_FLOOR_ON_ANCHOR
                    register row promise, discharged for THIS card rather than
                    borrowed from Tier-C3's cell A0, which was computed under a
                    different ride. NOT a card diff: the CLASS line enacted,
                    and overturnable by the operator in one line (F-C3-a).

    THIS IS NOT A SWEEP AND NOTHING HERE IS SCORED.  A sweep searches a space
    for the best cell and reports it; this decomposes ONE ratified result into
    the contributions of its OWN ratified parts, every cell printed, the
    ratified card already chosen before the table existed.  m = 0 is unaffected:
    no cell may be promoted, and picking one out of this table on its R is a new
    probe that declares its own m BEFORE the look.

    The operator's words were "a mean for the average trade we can tune later".
    THIS TABLE IS THAT SUBSTRATE, and the sentence that must ride with it is:
    tuning later means declaring m first.
    """
    cells = [("V3", False, False, True,
              "the v3 card, re-ridden here — the control"),
             ("RATCHET", True, False, True, "the LPS-trail alone"),
             ("HARVEST", False, True, True, "the creek/ice touch alone"),
             ("BOTH", True, True, True, "THE SHIPPED CARD"),
             # PRINTED BOTH WAYS. The card's SEAL FLOOR line ends "Printed both
             # ways" and the inherited register row promises the operator can
             # overturn the floor in one line. Tier-C3 discharged that with its
             # attribution cell A0; v4 must discharge it for ITS OWN card, not
             # borrow a predecessor's number computed under a different ride.
             # The mask is not inert here — it refuses 2 armings.
             ("BOTH_NOSEAL", True, True, False,
              "the card LITERALLY — no seal floor; F-C3-a, printed both ways")]
    rows, kept = [], {}
    for cell, rt, hv, floor, note in cells:
        ts: list = []
        for sym in RC.UNIVERSE:
            k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
            _, t = replay_asset(sym, "SCORED", k4, k1, load_funding(sym),
                                ratchet=rt, harvest=hv, seal_floor=floor)
            ts += [t2 for t2 in t if t2.scored]
        kept[cell] = ts
        rs = [t2.net_r for t2 in ts]
        rows.append({
            "cell": cell, "ratchet": rt, "harvest": hv, "seal_floor": floor,
            "n": len(ts),
            "net_r": r4(sum(rs)) if rs else None,
            "expectancy_r": r4(float(np.mean(rs))) if rs else None,
            "win_rate_pct": pct(sum(1 for v in rs if v > 0), len(rs)),
            "max_dd_r": r4(TB._maxdd_r([(t2.exit_ms, t2.symbol, t2.net_r)
                                        for t2 in ts])) if rs else None,
            "top_decile_share_pct": TB._top_decile_share(rs) if rs else None,
            "best_r": r4(max(rs)) if rs else None,
            "strip_best_net_r": r4(sum(rs) - max(rs)) if rs else None,
            "n_advances": sum(len(t2.advances) for t2 in ts),
            "n_ratchet_exits": sum(1 for t2 in ts if t2.ratchet_exit),
            "n_harvests": sum(1 for t2 in ts if t2.harvested),
            # WHERE A HARVEST FIRED, RELATIVE TO ENTRY. Printed because the
            # HARVEST cell's marginal is otherwise unreadable: the fills
            # themselves make money on this corridor, and the amendment still
            # costs R. The cost is in the half that was NOT allowed to run,
            # which is a different quantity from the half that was taken, and
            # only these columns separate them.
            "harvest_half_net_r": r4(sum(t2.net_r_harvest_half for t2 in ts
                                         if t2.harvested)) if ts else None,
            # FULL-UNIT move in R at the fill, mean over the cell's fills.
            # `harvest_half_net_r` above IS a half quantity; this is not, and
            # the names now say so.
            "harvest_unit_move_r_mean": r4(float(np.mean(
                [(t2.harvest_px - t2.entry_px) * t2.direction / t2.r_dist
                 for t2 in ts if t2.harvested]))) if any(
                t2.harvested for t2 in ts) else None,
            "harvest_adverse_n": sum(
                1 for t2 in ts if t2.harvested
                and (t2.harvest_px - t2.entry_px) * t2.direction < 0),
            # THE SEAL READ, PER CELL. The BOTH_NOSEAL cell exists to show what
            # the card does WITHOUT the CLASS line's mask, so it necessarily
            # quotes a sealed bar — and a table with no timestamp column is
            # invisible to a min/max era scan, which is exactly the class of
            # blindness F-C3-a was found by. So the read is COUNTED here, in
            # the same row as the outcome it produced.
            "anchors_in_lockbox": sum(1 for t2 in ts if t2.anchor_in_lockbox),
            "harvest_median_bars_after_entry": r4(float(np.median(
                [t2.harvest_bars_after_entry for t2 in ts if t2.harvested])))
                if any(t2.harvested for t2 in ts) else None,
            "n_stop_exits": sum(1 for t2 in ts if t2.exit_reason == "stop"),
            "n_bell_exits": sum(1 for t2 in ts
                                if t2.exit_reason.startswith("bell")),
            "median_bars_held": r4(float(np.median([t2.bars_held for t2 in ts])))
                                if ts else None,
            "note": note,
        })
    d = pd.DataFrame(rows)
    g = {r["cell"]: r["net_r"] for _, r in d.iterrows()}
    d["marginal_vs"] = ["", "V3", "V3", "V3", "BOTH"]
    d["marginal_net_r"] = [None, r4(g["RATCHET"] - g["V3"]),
                           r4(g["HARVEST"] - g["V3"]), r4(g["BOTH"] - g["V3"]),
                           r4(g["BOTH_NOSEAL"] - g["BOTH"])]
    # NOT ADDITIVE, AND SAID SO IN THE TABLE. The two amendments interact
    # through the same ride: a harvest changes nothing about where the trail
    # goes, but a ratchet stop can end the campaign BEFORE the band is touched.
    d["interaction_net_r"] = [None, None, None,
                              r4(g["BOTH"] - g["RATCHET"] - g["HARVEST"]
                                 + g["V3"]), None]
    return d, kept


def headline_triptych(v4_head: pd.DataFrame) -> pd.DataFrame:
    """v4 BESIDE v3 BESIDE v1 — the deliverable, and the only honest way to
    read any of the three.

    v1's and v3's rows are READ from their own FILED `headline.parquet` and are
    never recomputed here.  A build that can move its predecessor's number while
    comparing itself to it is not comparing anything.
    """
    rows = []
    for label, root, card in (
            ("v1", V1_TABLES, "TIER-C2 · 1H anchor, no rail, no lead-in"),
            ("v3", V3_TABLES, "TIER-C3 · 4h anchor + 1.0 ATR rail + 30d lead-in"),
            ("v4", None, "TIER-C4 · v3 + LPS-trail ratchet + creek/ice harvest")):
        if root is None:
            a = v4_head[(v4_head["group"] == "ALL")
                        & (v4_head["key"] == "ALL")].iloc[0]
            src = "this build"
        else:
            p = root / "headline.parquet"
            if not p.exists():
                raise SystemExit(f"HALT: {label} headline absent at {p} — the "
                                 f"TRIPTYCH is a deliverable and may not be "
                                 f"faked.")
            h = pd.read_parquet(p)
            a = h[(h["group"] == "ALL") & (h["key"] == "ALL")].iloc[0]
            src = str(p.relative_to(ROOT))
        rows.append({
            "version": label, "card": card, "source": src,
            "n": int(a["n"]), "net_r": r4(a["net_r"]),
            "expectancy_r": r4(a["expectancy_r"]),
            "win_rate_pct": r4(a["win_rate_pct"]),
            "max_dd_r": r4(a["max_dd_r"]),
            "top_decile_share_pct": r4(a["top_decile_share_pct"]),
            "best_r": r4(a["best_r"]),
            "strip_best_net_r": r4(a["strip_best_net_r"]),
            "net_r_bellonly": r4(a["net_r_bellonly"]),
            "corridor": f"{SCORED[0]} -> {SCORED[1]}",
        })
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════ the driver
def run(root: Path, do_tape: bool = True) -> dict:
    t0 = time.time()
    man: dict = {"seed": SEED, "windows": {}, "sha": {}, "counts": {},
                 "card": "TIER-C4 · THE MEAN CARD",
                 "yardstick_label": YARDSTICK_LABEL}

    log("=" * 78)
    log("TIER-C4 · THE MEAN CARD — v3 + LPS-trail ratchet + creek/ice harvest")
    log("=" * 78)
    log(f"  analytics {AN.ANALYTICS_VERSION}  sha {AN.analytics_sha()[:16]}…")
    log(f"  seed {SEED} · universe {', '.join(RC.UNIVERSE)} · lens {RC.LENS}")
    log(f"  klines {KLINES}")
    log(f"  AMENDMENTS: ratchet = ({RC.RATCHET_PIVOT_L},{RC.RATCHET_PIVOT_R}) "
        f"fractal, beyond {RC.RATCHET_BUF_ATR} x ATR, railed "
        f"{RC.RATCHET_RAIL_ATR} x ATR from close, monotone "
        f"{RC.RATCHET_MONOTONE} · harvest = {RC.HARVEST_FRACTION:.0%} at the "
        f"first {RC.HARVEST_BAND[0]}/{RC.HARVEST_BAND[1]} band touch, "
        f"max {RC.HARVEST_MAX_PER_CAMPAIGN} per campaign, fill "
        f"{RC.REGISTER['HARVEST_FILL']['value']}")
    log(f"  UNCHANGED: anchor 4h ({RC.PIVOT_L},{RC.PIVOT_R}) lookback "
        f"{RC.PIVOT_LOOKBACK_4H} bars · entry rail {RC.MIN_STOP_ATR} x ATR · "
        f"lead-in {RC.LEAD_IN_DAYS}d · d {RC.D_DISPLACEMENT} · toll "
        f"{RC.FEE_BPS_ROUND_TRIP} bps round trip")
    log("")

    # ── THE GUARD, LOADED AND IDLE ────────────────────────────────────────
    # CLASS says ONE pre-named card, no grid, no sweep. The estate's selection
    # guard is the object that would have to be satisfied if that were false,
    # so it is imported and CALLED — with the empty candidate list this build
    # actually has. Its verdict, m = 0, goes in the manifest. A guard that is
    # only mentioned is a guard nobody ran.
    from census2a_program import selection_guard                  # noqa: E402
    guard = selection_guard([])
    man["selection_guard"] = {
        "loaded": True, "called": True, "candidates": 0, "verdict": guard,
        "why": "CLASS: ONE pre-named card, m = 0. No grid, no sweep, nothing "
               "promoted. The guard idles because there is no selection to "
               "correct — the ABLATION decomposes a card already chosen, and "
               "picking a cell out of it on its R is a NEW probe that declares "
               "its own m before the look."}
    log(f"  SELECTION GUARD loaded and called with 0 candidates -> "
        f"m={guard['m']} · {guard.get('reason', '')} (IDLE, as classed)")
    log("")

    log("  WINDOWS")
    for n, w in WINDOWS.items():
        lead = _ms(w["span"][0]) - RC.LEAD_IN_DAYS * MS_1D
        log(f"    {n:12} {w['span'][0]} -> {w['span'][1]}   "
            f"{'SCORED' if w['scored'] else 'DISPLAY-ONLY'}  "
            f"(armings from {iso(lead)[:10]}; {w['note']})")
    read_lo = _ms(SCORED[0]) - RC.LEAD_IN_DAYS * MS_1D
    lo = AN.lockbox_overlap(read_lo, _ms(SCORED[1]) + MS_1D - 1)
    log(f"    {'LOCKBOX':12} {LOCKBOX[0]} -> {LOCKBOX[1]}   NOT COMPUTED (sealed)")
    log(f"    {'':12} the span this build READS for armings, "
        f"{iso(read_lo)[:10]} -> {SCORED[1]}, overlaps the seal by "
        f"{lo['overlap_days']:.3f} d  [F-5, disclosed]")
    log(f"    {'':12} SEAL FLOOR: {RC.SEAL_FLOOR_ON_ANCHOR} on the ENTRY "
        f"ANCHOR *and* on every RATCHET PIVOT — both are published prices paid "
        f"out on a stop (CLASS line, not a card diff)")
    log("")

    all_arms: dict[str, list] = {}
    all_trades: dict[str, list] = {}
    tape_frames: list[pd.DataFrame] = []

    for win_name in WINDOWS:
        span = WINDOWS[win_name]["span"]
        win_lo, win_hi = _ms(span[0]), _ms(span[1]) + MS_1D - 1
        log(f"  ── {win_name} {span[0]} -> {span[1]} "
            f"{'(SCORED)' if WINDOWS[win_name]['scored'] else '(DISPLAY-ONLY)'}")
        arms_w, trades_w = [], []
        for sym in RC.UNIVERSE:
            k4, k1 = load_klines(sym, "4h"), load_klines(sym, "1h")
            fund = load_funding(sym)
            a, t = replay_asset(sym, win_name, k4, k1, fund)
            arms_w += a
            trades_w += t
            sc = sum(1 for y in t if y.scored)
            log(f"    {sym:9} armings={len(a):5d} "
                f"(in-window {sum(1 for y in a if y.in_window):5d} / lead-in "
                f"{sum(1 for y in a if not y.in_window):3d})  "
                f"trades={sc:4d} (+{len(t) - sc} unscored lead-in)  "
                f"advances={sum(len(y.advances) for y in t if y.scored):4d}  "
                f"harvests={sum(1 for y in t if y.scored and y.harvested):3d}")

            if do_tape and WINDOWS[win_name]["scored"]:
                # THE SEAL: no tape instant precedes the corridor. A trade armed
                # in the lead-in therefore has NULL arming-instant tape columns,
                # by construction — disclosed, never back-filled.
                inst: list[tuple[int, str]] = []
                for xa in a:
                    if xa.arm_ms >= win_lo:
                        inst.append((xa.arm_ms, "arming"))
                    if xa.trigger_ms is not None and xa.trigger_ms >= win_lo:
                        inst.append((xa.trigger_ms, "trigger"))
                for tr in t:
                    if tr.scored:
                        inst.append((tr.exit_ms, "exit"))
                        if tr.harvested:
                            inst.append((int(tr.harvest_ms), "harvest"))
                for dsp in TB.daily_spine(k4, win_lo, win_hi):
                    inst.append((dsp, "spine"))
                order = {"arming": 0, "trigger": 1, "exit": 2, "harvest": 3,
                         "spine": 4}
                seen: dict[int, str] = {}
                for ts, kind in sorted(inst, key=lambda p: (p[0], order[p[1]])):
                    seen.setdefault(int(ts), kind)
                tp = TB.tape_rows(sym, k4, k1, sorted(seen.items()), win_name)
                if len(tp):
                    rs = TB.ribbon_state(sym)
                    if len(rs):
                        assert_key(rs, ["ts"], f"ribbon_state[{sym}]")
                        tp = tp.merge(rs, on="ts", how="left", validate="1:1")
                    tape_frames.append(tp)
        all_arms[win_name] = arms_w
        all_trades[win_name] = trades_w
        man["windows"][win_name] = {
            "span": list(span), "scored": WINDOWS[win_name]["scored"],
            "lead_in_from": iso(_ms(span[0]) - RC.LEAD_IN_DAYS * MS_1D)[:10],
            "armings": len(arms_w),
            "armings_in_window": sum(1 for y in arms_w if y.in_window),
            "armings_lead_in": sum(1 for y in arms_w if not y.in_window),
            "trades_scored": sum(1 for y in trades_w if y.scored),
            "trades_lead_in_unscored": sum(1 for y in trades_w if not y.scored)}
        sc_w = [y for y in trades_w if y.scored]
        if sc_w:
            man["windows"][win_name]["trade_ts_bounds"] = {
                "min_entry": iso(min(y.entry_ms for y in sc_w)),
                "max_entry": iso(max(y.entry_ms for y in sc_w)),
                "min_exit": iso(min(y.exit_ms for y in sc_w)),
                "max_exit": iso(max(y.exit_ms for y in sc_w)),
                "max_exit_ms": int(max(y.exit_ms for y in sc_w))}
        log("")

    # ── tables ────────────────────────────────────────────────────────────
    log("  ── TABLES")
    scored_arms = all_arms["SCORED"]
    all_scored_win_trades = all_trades["SCORED"]
    scored_trades = [t for t in all_scored_win_trades if t.scored]

    man["sha"]["funnel"] = write_table(funnel_table(scored_arms), "funnel",
                                       ["asset", "direction"], root)
    man["sha"]["lead_in_census"] = write_table(
        lead_in_census(scored_arms, all_scored_win_trades), "lead_in_census",
        [], root)
    li = lead_in_table(all_scored_win_trades)
    man["sha"]["lead_in_trades"] = write_table(
        li, "lead_in_trades", ["asset", "entry_ms"] if len(li) else [], root)

    sd = []
    for pop, subset in (("in_window", [a for a in scored_arms if a.in_window]),
                        ("in_window+lead_in", scored_arms)):
        s = TB.strip_d_table(subset)
        s.insert(0, "population", pop)
        sd.append(s)
    man["sha"]["strip_d"] = write_table(pd.concat(sd, ignore_index=True),
                                        "strip_d_unscored",
                                        ["population", "d"], root)

    head = pd.concat([TB.headline_rows(scored_trades, g)
                      for g in ("ALL", "asset", "direction", "exit_reason")],
                     ignore_index=True)
    head.insert(0, "label", YARDSTICK_LABEL)
    man["sha"]["headline"] = write_table(head, "headline", ["group", "key"],
                                         root)
    man["sha"]["triptych"] = write_table(headline_triptych(head),
                                         "headline_triptych", ["version"], root)
    man["sha"]["monthly"] = write_table(TB.monthly_equity(scored_trades),
                                        "monthly_equity", ["month"], root)
    sg = stop_geometry(scored_trades)
    man["sha"]["stop_geometry"] = write_table(
        sg, "stop_geometry", ["asset", "entry_ms"] if len(sg) else [], root)
    rl = ratchet_ledger(scored_trades)
    man["sha"]["ratchet_ledger"] = write_table(
        rl, "ratchet_ledger",
        ["asset", "entry_ms", "advance_seq"] if len(rl) else [], root)
    hl = harvest_ledger(scored_trades)
    man["sha"]["harvest_ledger"] = write_table(
        hl, "harvest_ledger", ["asset", "entry_ms"] if len(hl) else [], root)

    ab, cells = ablation_table()
    man["sha"]["ablation"] = write_table(ab, "ablation_unscored", ["cell"], root)
    dl = delta_table(scored_trades, cells["V3"])
    man["sha"]["delta"] = write_table(
        dl, "delta_v3_v4", ["asset", "direction", "arm_ms"] if len(dl) else [],
        root)

    al = anchor_lookback_disclosure(scored_trades)
    man["sha"]["anchor_lookback"] = write_table(
        al, "anchor_lookback_disclosure",
        ["asset", "entry_ms"] if len(al) else [], root)
    if len(al):
        man["counts"]["anchor_same_under_time_equiv_lookback"] = int(
            al["same_anchor"].sum())
        man["counts"]["anchor_rows"] = len(al)

    jr = journal_frame(scored_trades)
    if len(jr):
        tp = pd.concat(tape_frames, ignore_index=True) if tape_frames else pd.DataFrame()
        if len(tp):
            am = tp.set_index(["asset", "ts"])
            for i, row in jr.iterrows():
                ka = (row["asset"], row["arm_ms"])
                kt = (row["asset"], row["entry_ms"])
                if ka in am.index:
                    jr.at[i, "wall_family_at_arming"] = am.loc[ka, "wall_family"]
                    jr.at[i, "dist_atr_at_arming"] = am.loc[ka, "nearest_dist_atr"]
                    jr.at[i, "coloc_n"] = am.loc[ka, "coloc_n"]
                if kt in am.index:
                    jr.at[i, "dist_atr_at_trigger"] = am.loc[kt, "nearest_dist_atr"]
    man["sha"]["journal"] = write_table(jr, "trade_journal",
                                        ["asset", "entry_ms"] if len(jr) else [],
                                        root)

    ds = []
    for win_name in ("CENSUS_ERA", "PINNING"):
        h = TB.headline_rows([t for t in all_trades[win_name] if t.scored], "ALL")
        h["window"] = win_name
        h["span"] = f"{WINDOWS[win_name]['span'][0]} -> {WINDOWS[win_name]['span'][1]}"
        h["class"] = DISPLAY_ONLY_HEADER
        ds.append(h)
    man["sha"]["display_only"] = write_table(pd.concat(ds, ignore_index=True),
                                             "display_only_strips",
                                             ["window", "group", "key"], root)

    if tape_frames:
        tape = pd.concat(tape_frames, ignore_index=True)
        man["sha"]["tape"] = write_table(tape, "analytics_tape",
                                         ["asset", "ts"], root)
        man["counts"]["tape_rows"] = len(tape)
        man["counts"]["tape_instants"] = tape["instant"].value_counts().to_dict()
        man["sha"]["tape_inventory"] = write_table(
            TB.tape_inventory(tape), "tape_inventory", ["instant", "column"],
            root)

    man["counts"]["scored_trades"] = len(scored_trades)
    man["counts"]["scored_armings"] = sum(1 for a in scored_arms if a.in_window)
    man["counts"]["lead_in_armings"] = sum(1 for a in scored_arms
                                           if not a.in_window)
    man["counts"]["lead_in_trades_unscored"] = sum(
        1 for t in all_scored_win_trades if not t.scored)
    man["counts"]["scored_trades_armed_in_lead_in"] = sum(
        1 for t in scored_trades if t.armed_in_lead_in)
    man["counts"]["rail_binding"] = sum(1 for t in scored_trades if t.rail_binding)
    man["counts"]["anchors_in_lockbox"] = sum(
        1 for t in scored_trades if t.anchor_in_lockbox)
    man["counts"]["armings_refused_anchor_sealed"] = sum(
        1 for a in scored_arms if a.reject == "anchor_sealed")
    man["counts"]["advances_total"] = int(len(rl))
    man["counts"]["trades_with_advance"] = sum(1 for t in scored_trades
                                               if t.advances)
    man["counts"]["ratchet_exits"] = sum(1 for t in scored_trades
                                         if t.ratchet_exit)
    man["counts"]["advance_pivots_in_lockbox"] = (
        int(rl["pivot_bar_in_lockbox"].sum()) if len(rl) else 0)
    man["counts"]["harvests"] = int(len(hl))
    man["counts"]["harvest_blocked_by_stop"] = sum(
        1 for t in scored_trades if t.harvest_blocked_by == "stop")
    man["counts"]["harvest_blocked_by_bell"] = sum(
        1 for t in scored_trades if t.harvest_blocked_by == "bell")
    man["counts"]["never_touched_band"] = sum(
        1 for t in scored_trades if not t.harvested and not t.harvest_blocked_by)
    # THE "FROM BELOW" PRECONDITION, disclosed as a count. A campaign whose
    # ENTRY closed inside the 89/316 band cannot have a first touch "from
    # below" and is not armed until it leaves. Zero on this corridor; the
    # number is printed so that stays a measurement rather than an assumption.
    man["counts"]["entries_inside_band"] = sum(
        1 for t in scored_trades if not t.entered_outside_band)
    man["seal_floor_on_anchor"] = bool(RC.SEAL_FLOOR_ON_ANCHOR)
    man["seal_floor_on_ratchet_pivot"] = True
    # THE ONE DELIBERATE SEAL READ IN THIS BUILD, NAMED AND BOUNDED.
    # `anchors_in_lockbox = 0` above is computed over the SHIPPED trades only.
    # The ablation's BOTH_NOSEAL cell runs the card WITHOUT the mask — that is
    # its entire purpose, it is the "printed both ways" the card promises — and
    # it therefore quotes a sealed bar. Saying "no outcome in this build comes
    # from a sealed bar" without this line would be false, and false in the
    # exact way F-C3-a was: invisible to any timestamp test, because the table
    # that carries it has no timestamps.
    man["seal_read"] = {
        "shipped_card": {"cells": ["V3", "RATCHET", "HARVEST", "BOTH"],
                         "seal_floor": True, "anchors_in_lockbox": 0},
        "deliberately_unmasked": {
            "cells": ["BOTH_NOSEAL"], "seal_floor": False,
            "anchors_in_lockbox": int(
                ab.loc[ab["cell"] == "BOTH_NOSEAL", "anchors_in_lockbox"].iloc[0]),
            "why": "the CLASS line's seal floor PRINTED BOTH WAYS (F-C3-a). The "
                   "operator can overturn the floor in one line and this cell "
                   "is the number if they do. UNSCORED, and the only place in "
                   "this build where an outcome descends from a sealed bar."}}
    man["elapsed_s"] = round(time.time() - t0, 1)

    root.mkdir(parents=True, exist_ok=True)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}   ({man['elapsed_s']}s)")
    return man


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all", choices=["all", "replay", "tape"])
    ap.add_argument("--rerun", action="store_true",
                    help="write to research_outputs/tierc4_run2 (F-C4-DET)")
    a = ap.parse_args()
    root = OUT_RERUN if a.rerun else OUT
    run(root, do_tape=(a.stage in ("all", "tape")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
