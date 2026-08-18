"""TIER-C7-C + TIER-C8 · THE CLEAN CHAINS AND THE HONEST ANCHOR.

RATIFIED operator 2026-08-17 — "tc7c and tc8, then we set SAIL".  THE LAST
IN-SAMPLE RUN.

RULINGS ENACTED AS DEFAULTS, each a [VETO]:
    TC6V-a  CORRIDORS ARE WARRANTIES.  Every written table carries an `as_of`
            stamp naming the last closed 4h bar it is true of.  A number
            without its corridor is a number with no shelf life.
    TC6V-b  CACHE DRIFT IS DOCUMENTED, NOT FROZEN.  The manifest carries a
            drift note; the cache is not snapshotted.
    TC6V-d  the sixteen cosmetics, fixed as one batch and listed.
    TC7-c   AN FDR FAMILY COUNTS INDEPENDENTLY-FAILABLE HYPOTHESES.  m = 3.

────────────────────────────────────────────────────────────────────────────
PHASE C — THE CHAIN IS A TWO-POSITION OBJECT, BY SCHEMA
────────────────────────────────────────────────────────────────────────────
TIER-C7 filed a chain as ONE row of a single-campaign journal and four columns
lied about it: `mfe_r` divided leg 2's excursion by the chain's R without its
size, `stop_advanced_atr` measured leg 2's final stop against leg 1's entry
anchor, `ratchet_exit` read the wrong leg, and `harvested` read leg 1 only.
Each was repaired individually.  THE CLASS IS RETIRED HERE BY SCHEMA: the
journal is per-leg rows PLUS a chain rollup, so there is no single slot left to
put a two-position answer into.  `F-C7C-JRN` hand-walks three chains through it.

────────────────────────────────────────────────────────────────────────────
PHASE 8 — THE ANCHOR BAKE-OFF, RATE-MATCHED
────────────────────────────────────────────────────────────────────────────
TIER-C7's L-ANCHOR named M-band-edge @0.50 the winner at +118.75 R, ~3x the
prior — and its own builder flagged the confound: the smooth-series anchors
ratchet on nearly every confirming pivot (696 advances against the pivot's 228),
so the gain was partly a looser, later-moving stop rather than a better anchor.

THE DESIGN SEPARATES TIMING FROM VALUE.  Advance TIMING is the incumbent pivot
clock — a (2,2) confirmation is the ONLY moment any anchor may advance.  Advance
VALUE is that anchor's level at that moment.  Cadence is then equal BY
CONSTRUCTION, not by adjustment, and `F-C8-MATCH` asserts identical
advance-OPPORTUNITY counts per campaign across every cell.
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

import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
import analytics as AN                                               # noqa: E402
from engine import indicators as ind                                 # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, log = TB.write_table, TB.log
frame, fractals, corridor = T7.frame, T7.fractals, T7.corridor
card_candidates, _idx_range = T7.card_candidates, T7._idx_range
agg, d15, journal_frame = T7.agg, T7.d15, T7.journal_frame
cluster_boot, cluster_boot_diff, _ci_from = (T7.cluster_boot,
                                             T7.cluster_boot_diff, T7._ci_from)
headline_v6 = T7.headline_v6
FDR_Q = T7.FDR_Q

SEED = 20260818
OUT = ROOT / "research_outputs" / "tierc8"
OUT_RERUN = ROOT / "research_outputs" / "tierc8_run2"

# ═════════════════════════════════ THE FROZEN THRESHOLD — P-AE-2, STEP 1
# THE NAMING RULE IS THE PRE-REGISTRATION; THE VALUE IS PRINTED THE MOMENT IT
# IS FIXED.  "the smallest x with P(win | MAE_tape >= x) <= 10% on the
# UNCENSORED, tape-side hazard curve, over a population of at least 30."
# Computed in step 1 of this phase, before any arm was scored, and frozen here.
AE2_RULE = ("smallest x on the UNCENSORED tape-side hazard curve with "
            "P(win | MAE_tape >= x) <= 10% and n >= 30")
AE2_THRESHOLD_R = 0.60
AE2_MEASURED = {"x_r": 0.60, "n_at_or_beyond": 134, "p_win_pct": 9.7015,
                "curve": "tape-side (uncensored)"}
# AND THE HONEST CONSEQUENCE, STATED BEFORE THE SCORE: the rule re-derives the
# SAME 0.60R that P-AE-1 was given from the CENSORED curve (where it read
# 7.03%). P-AE-2 therefore rides the identical card and produces the identical
# book. It is not an independent second look at the question; it is P-AE-1 with
# its threshold now honestly sourced. Said here rather than discovered later.
AE2_IS_AE1 = True

AS_OF: str = ""            # set by run(); every table carries it [TC6V-a]


def stamp(df: pd.DataFrame, meta: dict) -> pd.DataFrame:
    """THE WARRANTY [TC6V-a].  Every written table says which corridor it is
    true of, in a COLUMN — a caption does not survive a copy of the row.

    WHAT WOULD MAKE THIS WRONG: stamping the wall clock instead of the last
    closed bar (the run time is not the data's), or stamping only the manifest,
    which is the thing a reader least often has in front of them.
    """
    d = df.copy()
    d["as_of_last_closed_4h"] = meta["last_closed_4h_close"]
    d["as_of_panel_start"] = meta["panel_start"]
    d["as_of_span_days"] = meta["span_days"]
    d["warranty"] = ("these numbers are true AS OF the corridor named in this "
                     "row and of no other; the corridor advances with the "
                     "cache [TC6V-a]")
    return d


# ══════════════════════════════════════════════ TC7-i · BOTH TIDE CLAUSES
def tide_ok(f, j: int, d: int) -> bool:
    """THE CARD'S TIDE, BOTH CLAUSES [TC7-i].

    The card's own gate (`tierc2_rules.armings`) is TWO conditions:
        long   e89 > e316  AND  close > e316
        short  e89 < e316  AND  close < e316
    TIER-C7's re-entry implemented only the first, while its docstring claimed
    it used "the card's tide gate" — a claim the code did not meet. The second
    clause is the one that refuses a re-entry where the ribbons have crossed
    back but price has not.

    WHAT WOULD MAKE THIS WRONG: re-deriving the tide from a different pair of
    EMAs, or keeping one clause and calling it the card's.
    """
    e89, e316, c = float(f.e89[j]), float(f.e316[j]), float(f.c[j])
    if not all(np.isfinite(v) for v in (e89, e316, c)):
        return False
    return bool((e89 - e316) * d > 0 and (c - e316) * d > 0)


# ══════════════════════════════════ PHASE 8 · THE RATE-MATCHED ANCHOR
ANCHORS = ("pivot", "e26", "e89", "m_edge", "max_pivot_e89")
OFFSETS = (0.25, 0.50)
_SERIES: dict[str, dict] = {}


def anchor_series(sym: str) -> dict:
    """The anchor levels, warm-up floored, one pass per asset.

    EVERY SERIES IS FLOORED. `ind.ema` seeds at the series start and never
    returns NaN; this estate has repaired that defect FOUR times and the fifth
    is prevented here. The M band is floored at its LONGEST member, because a
    band is not defined while only some of its members are warm.
    """
    if sym in _SERIES:
        return _SERIES[sym]
    c = frame(sym)["f"].c
    n = len(c)
    idx = np.arange(n)
    e26 = np.where(idx >= 26, ind.ema(c, 26), np.nan)
    e89 = np.where(idx >= 89, ind.ema(c, 89), np.nan)
    m_lo, m_hi = RC.ribbon_band(c, "M")
    warm = idx >= max(RC.RIBBONS["M"])
    m_lo = np.where(warm, m_lo, np.nan)
    m_hi = np.where(warm, m_hi, np.nan)
    _SERIES[sym] = {"e26": e26, "e89": e89, "m_lo": m_lo, "m_hi": m_hi}
    return _SERIES[sym]


def anchor_level(kind: str, s: dict, j: int, pivot_val: float,
                 d: int) -> float:
    """The anchor's LEVEL at the confirming bar — value only, never timing.

    The trade-side edge is the one that can be a stop: the M band's LOW for a
    long, its HIGH for a short. `max_pivot_e89` is the TIGHTER of the two for a
    long and the mirror for a short, which is what `max` means when the stop
    sits below price.

    WHAT WOULD MAKE THIS WRONG: taking the far edge of the band (it would sit
    on the wrong side of price), or using `max` for both directions.
    """
    if kind == "pivot":
        return float(pivot_val)
    if kind == "e26":
        return float(s["e26"][j])
    if kind == "e89":
        return float(s["e89"][j])
    if kind == "m_edge":
        return float(s["m_lo"][j] if d == 1 else s["m_hi"][j])
    if kind == "max_pivot_e89":
        e = float(s["e89"][j])
        if not np.isfinite(e):
            return float("nan")
        return max(float(pivot_val), e) if d == 1 else min(float(pivot_val), e)
    raise SystemExit(f"HALT: unknown anchor {kind!r}")


def matched_step(fr, j: int, d: int, cur_stop: float, close: float, atr: float,
                 s: dict, kind: str, offset: float, open_ms,
                 min_advance_atr: float = 0.05,
                 rail_atr: float = RC.MIN_STOP_ATR):
    """ONE ADVANCE, RATE-MATCHED.  Returns (Advance | None, opportunity: bool).

    TIMING IS THE INCUMBENT PIVOT CLOCK.  A (2,2) confirmation is the ONLY
    moment any anchor may advance — the same bars, in the same order, for every
    cell of the grid.  `opportunity` is True on exactly those bars, whatever the
    anchor does with them, and `F-C8-MATCH` asserts the counts are identical
    across cells.  That is what makes the bake-off a comparison of ANCHORS
    rather than of cadences: TIER-C7's table gave M-band-edge 696 advances
    against the pivot's 228 and then compared the results.

    VALUE IS THE ANCHOR'S LEVEL AT THAT MOMENT, offset into the trade, railed
    from the confirming close, advance-only, minimum advance 0.05 ATR measured
    on the STOP movement — the quantity the ledger publishes.

    WHAT WOULD MAKE THIS WRONG: letting a smooth anchor advance on a bar with no
    confirming pivot (that is the confound, restored); measuring the minimum
    advance on the ANCHOR move rather than the stop's; or counting an
    opportunity only when the anchor happened to produce one.
    """
    src = fr.low_by_conf if d == 1 else fr.high_by_conf
    hit = src.get(int(j))
    if hit is None:
        return None, False
    pv, pbar = hit
    if not (np.isfinite(atr) and atr > 0 and np.isfinite(close)):
        return None, True
    lvl = anchor_level(kind, s, j, pv, d)
    if not np.isfinite(lvl):
        return None, True
    if d == 1:
        cand = lvl - offset * atr
        rail = close - rail_atr * atr
        admitted = min(cand, rail)
        rail_bound = rail < cand
        if not (admitted > cur_stop):
            return None, True
    else:
        cand = lvl + offset * atr
        rail = close + rail_atr * atr
        admitted = max(cand, rail)
        rail_bound = rail > cand
        if not (admitted < cur_stop):
            return None, True
    if min_advance_atr > 0.0 and abs(admitted - cur_stop) / atr < min_advance_atr:
        return None, True
    return RC.Advance(
        conf_i=int(j), conf_ms=int(open_ms[j]), pivot_val=float(lvl),
        pivot_bar=int(pbar), pivot_bar_ms=int(open_ms[pbar]),
        atr=float(atr), close=float(close), cand_px=float(cand),
        rail_px=float(rail), new_stop=float(admitted),
        prev_stop=float(cur_stop), rail_binding=bool(rail_bound),
        dist_from_close_over_atr=float(abs(close - admitted) / atr)), True


# ═══════════════════════════════════════════════════════════════ THE CARD, v8
from dataclasses import dataclass                                  # noqa: E402


@dataclass(frozen=True)
class Card(RC.Card):
    """v7's card, two fields wider — and both default to the incumbent.

    `Card()` with no arguments is card v6, exactly as `RC.Card()` is, which is
    what makes `F-CTRL` a control: the whole v8 code path must reproduce card
    v6 at 0.000e+00 before any arm is scored.
    """
    name: str = "v8-default(=v6)"
    anchor_kind: str = "pivot"          # PHASE 8 — the rate-matched anchor
    anchor_offset: float = RC.STOP_BUF_ATR


CARD_V6_CONTROL = Card(name="v6-control")
CARD_CHAIN2 = Card(name="v8-chain2", weave=True, reentry=True)
CARD_AE2 = Card(name="v8-ae2", ae_abort_r=AE2_THRESHOLD_R)
CARD_ANC1 = Card(name="v8-anchor-M-edge-0.50", anchor_kind="m_edge",
                 anchor_offset=0.50)
CARD_WEV = Card(name="v8-weave-only", weave=True)


def _ride_leg(sym, card, d, ti, entry_px, stop0, r_dist, hi_i, chain_r=None):
    """TIER-C7's leg, with the anchor rate-matched and the opportunity counted.

    The ONLY diffs from `T7._ride_leg` are (a) the ladder call goes through
    `matched_step`, so a smooth anchor advances only on a confirming pivot, and
    (b) `n_opportunities` is returned — the count of confirming-pivot bars,
    which is identical across every cell of the grid by construction and is
    what `F-C8-MATCH` asserts.

    WHAT WOULD MAKE THIS WRONG: counting an opportunity only when the anchor
    produced an advance (that would make the match tautological), or letting the
    anchor advance off-clock (that is the confound this phase exists to remove).
    """
    st = frame(sym)
    f, x = st["f"], st["x"]
    fr = fractals(sym, card.trail_l, card.trail_r) if card.trail else None
    wv = T7.weave_of(sym) if (card.weave or card.reentry) else None
    s = anchor_series(sym)
    R = float(chain_r if chain_r is not None else r_dist)
    stop = float(stop0)
    advances, adds = [], []
    harv, blocked = None, ""
    mfe = float(entry_px)
    mae = 0.0
    mae_to_1r, reached_1r = 0.0, False
    trail_armed = card.trail_arm_after_r <= 0.0
    h_armed = False
    n_opp = 0
    exit_i, exit_px, exit_reason = hi_i, float(f.c[hi_i]), "corridor_end"

    for j in range(ti + 1, hi_i + 1):
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        ufav = (fav - entry_px) * d / R
        uadv = (adverse - entry_px) * d / R
        mae = min(mae, uadv)
        if not reached_1r:
            mae_to_1r = min(mae_to_1r, uadv)
            if ufav >= 1.0:
                reached_1r = True
        if not trail_armed and ufav >= card.trail_arm_after_r:
            trail_armed = True

        if card.harvest == "band":
            pe = RC.harvest_edge(float(f.e89[j - 1]), float(f.e316[j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(f.e89[j]), float(f.e316[j]), d)
            ufill = (float(f.c[j]) - entry_px) * d / R
            touch = (harv is None and h_armed
                     and RC.harvest_touched(float(f.h[j]), float(f.l[j]), edge, d)
                     and ufill >= card.harvest_min_unit_r)
        else:
            edge, touch = float("nan"), False

        if (d == 1 and f.l[j] <= stop) or (d == -1 and f.h[j] >= stop):
            exit_i, exit_px, exit_reason = j, stop, "stop"
            if touch:
                blocked = "stop"
            break
        if (fav - entry_px) * d > (mfe - entry_px) * d:
            mfe = fav
        bell = ((("bell_12_89" if bool(x["w_dn"][j])
                  else "bell_89_316" if bool(x["b_dn"][j]) else None)) if d == 1
                else (("bell_12_89" if bool(x["w_up"][j])
                       else "bell_89_316" if bool(x["b_up"][j]) else None)))
        if bell:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), bell
            break
        if card.time_stop_bars is not None and (j - ti) >= card.time_stop_bars:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "time_stop"
            break
        if card.ae_abort_r is not None and uadv <= -abs(card.ae_abort_r):
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "ae_abort"
            break
        if touch:
            harv = (j, RC.harvest_fill_px(f.c[j]),
                    (RC.harvest_fill_px(f.c[j]) - entry_px) * d / R)
        if card.weave and wv is not None and RC.weave_fires(wv, j, d,
                                                            card.weave_k):
            exit_i, exit_px, exit_reason = j, float(f.c[j]), "weave"
            break
        if card.trail and trail_armed:
            adv, opp = matched_step(fr, j, d, stop, float(f.c[j]),
                                    float(f.atr[j]), s, card.anchor_kind,
                                    card.anchor_offset, f.open_ms,
                                    min_advance_atr=card.trail_min_advance_atr)
            n_opp += int(opp)
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)
    return {"own_r": abs(float(entry_px) - float(stop0)), "entry_i": ti,
            "entry_px": float(entry_px), "stop0": float(stop0),
            "exit_i": exit_i, "exit_px": float(exit_px),
            "exit_reason": exit_reason, "advances": advances, "harvest": harv,
            "blocked": blocked, "mfe": mfe, "mae": mae, "adds": adds,
            "final_stop": stop, "n_opportunities": n_opp,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r}


def _ride_chain(sym, card, d, ti, entry_px, stop0, r_dist, hi_i):
    """TIER-C7's chain, with the re-entry gate now implementing BOTH tide
    clauses [TC7-i].  A weave-exit or ladder-out, then the first close beyond
    the fast ribbon in the trend direction within 24 bars with the tide — BOTH
    clauses — still agreeing."""
    st = frame(sym)
    f = st["f"]
    legs = [_ride_leg(sym, card, d, ti, entry_px, stop0, r_dist, hi_i)]
    if not card.reentry:
        return {"legs": legs, "n_reentries": 0, "reentry_refused": ""}
    leg1 = legs[0]
    laddered_out = bool(leg1["exit_reason"] == "stop" and leg1["advances"]
                        and abs(leg1["final_stop"] - stop0) > 1e-12)
    if leg1["exit_reason"] != "weave" and not laddered_out:
        return {"legs": legs, "n_reentries": 0,
                "reentry_refused": f"exit_reason={leg1['exit_reason']}"}
    wv = T7.weave_of(sym)
    x0 = leg1["exit_i"]
    for j in range(x0 + 1, min(x0 + RC.REENTRY_WINDOW_BARS, hi_i) + 1):
        ok_tide = tide_ok(f, j, d)                     # BOTH CLAUSES [TC7-i]
        if not RC.reentry_close(wv, j, d, float(f.c[j]), ok_tide):
            continue
        atr_j = float(f.atr[j])
        if not (np.isfinite(atr_j) and atr_j > 0):
            continue
        stp = RC.struct_stop_4h(st["pv4"], j, float(f.c[j]), d, atr_j,
                                min_stop_atr=card.entry_rail_atr,
                                forbidden=None)
        if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            return {"legs": legs, "n_reentries": 0,
                    "reentry_refused": "no structural anchor at re-entry"}
        legs.append(_ride_leg(sym, card, d, j, float(f.c[j]), stp.stop_px,
                              stp.r_dist, hi_i, chain_r=r_dist))
        return {"legs": legs, "n_reentries": 1, "reentry_refused": ""}
    return {"legs": legs, "n_reentries": 0,
            "reentry_refused": f"no qualifying close within "
                               f"{RC.REENTRY_WINDOW_BARS} bars (BOTH tide "
                               f"clauses required)"}


def replay(sym, card, lo_ms, hi_ms):
    """TIER-C7's replay on this module's chain, and the CHAIN IS A TWO-POSITION
    OBJECT: the Trade carries the rollup, the LEGS ride as a list, and no
    single-campaign column is asked to describe two positions."""
    st = frame(sym)
    f = st["f"]
    # THE SCOPE IS DECLARED AND ENFORCED, NOT ASSUMED.
    # This module implements the CARD lane only and no adds — which is exactly
    # card v6's own configuration, so F-CTRL is a fair control. But `replay`
    # silently ignoring `card.lane` and `card.adds_max` would mean a union card
    # or an adds card ran as a card-only book under its own name, and the
    # control would then compare two different programs while reporting
    # 0.000e+00. It HALTs instead.
    if card.lane != "card":
        raise SystemExit(
            f"HALT: tierc8.replay implements the CARD lane only; got "
            f"lane={card.lane!r}. The spring/union lanes live in tierc7 and "
            f"running them here would silently drop half the book.")
    if card.adds_max:
        raise SystemExit(
            f"HALT: tierc8.replay implements no adds; got "
            f"adds_max={card.adds_max}. P-CASC-1's cascade lives in tierc5.")
    lo_i, hi_i = _idx_range(f.open_ms, lo_ms, hi_ms)
    lo_i = max(lo_i, RC.WARMUP_BARS)
    if hi_i < lo_i:
        return [], []
    arms, cc = card_candidates(sym, lo_i, hi_i)
    cands = [(ti, d, "card", a, None) for ti, d, a in cc]
    cands.sort(key=lambda c: (c[0], -c[1], c[2]))
    trades, open_until = [], -1
    for ti, d, kind, arm, sp in cands:
        if ti <= open_until:
            if arm is not None:
                arm.reject = "position_open"
            continue
        entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])
        if not (np.isfinite(atr_sig) and atr_sig > 0):
            continue
        stp = RC.struct_stop_4h(st["pv4"], ti, entry_px, d, atr_sig,
                                min_stop_atr=card.entry_rail_atr,
                                forbidden=None)
        if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            continue
        if arm is not None:
            arm.entered, arm.reject, arm.entry_scored = True, "entered", True
        chain = _ride_chain(sym, card, d, ti, entry_px, stp.stop_px,
                            stp.r_dist, hi_i)
        last, first = chain["legs"][-1], chain["legs"][0]
        open_until = last["exit_i"]
        acc = T7._account_chain(sym, card, d, stp.r_dist, chain)
        sizes = acc["leg_sizes"]
        harv_legs = [k for k, lg in enumerate(chain["legs"]) if lg["harvest"]]
        harv = next((lg["harvest"] for lg in chain["legs"] if lg["harvest"]),
                    None)
        # SIZE-WEIGHTED, ACROSS LEGS — the TC7-a class, retired by schema.
        mfe_r = max(sz * (lg["mfe"] - lg["entry_px"]) * d / stp.r_dist
                    for sz, lg in zip(sizes, chain["legs"]))
        mae_r = min(sz * lg["mae"] for sz, lg in zip(sizes, chain["legs"]))
        last_ratchet = bool(last["exit_reason"] == "stop" and last["advances"]
                            and abs(last["final_stop"] - last["stop0"]) > 1e-12)
        t = RC.Trade(
            symbol=sym, lane=kind, direction=d,
            arm_i=arm.arm_i, arm_ms=arm.arm_ms, entry_i=ti,
            entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stp.stop_px, r_dist=stp.r_dist, anchor=stp.anchor,
            anchor_bar_ms=int(f.open_ms[stp.anchor_bar]) if stp.anchor_bar >= 0 else -1,
            anchor_was_sealed=False, atr_at_entry=atr_sig,
            disp_at_arming=arm.disp,
            exit_i=last["exit_i"], exit_ms=int(f.open_ms[last["exit_i"]]),
            exit_px=last["exit_px"], exit_reason=last["exit_reason"],
            bars_held=last["exit_i"] - ti, scored=True,
            advances=[a for lg in chain["legs"] for a in lg["advances"]],
            final_stop_px=last["final_stop"],
            stop_advanced_atr=(last["final_stop"] - last["stop0"]) * d / atr_sig,
            ratchet_exit=last_ratchet,
            harvested=bool(harv_legs),
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=first["blocked"],
            harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
            adds=[], add_r=None, spring=None, mfe_r=mfe_r,
            mae_to_1r_r=first["mae_to_1r"], reached_1r=first["reached_1r"],
            gross_r=acc["gross_r"], fee_r=acc["fee_r"],
            funding_r=acc["funding_r"],
            funding_r_uncapped=acc["funding_r_uncapped"],
            funding_ceiling_bound=acc["funding_ceiling_bound"],
            net_r=acc["net_r"], net_r_harvest_half=acc["n1"],
            net_r_runner_half=acc["n2"], net_r_bellonly=None)
        for k, v in (("chain", chain), ("n_reentries", chain["n_reentries"]),
                     ("leg_sizes", tuple(sizes)),
                     ("n_harvests", len(harv_legs)),
                     ("mae_r", mae_r),
                     ("n_opportunities", sum(lg["n_opportunities"]
                                             for lg in chain["legs"])),
                     ("reentry_refused", chain.get("reentry_refused", ""))):
            object.__setattr__(t, k, v)
        trades.append(t)
    return arms, trades


def run_cell(card, lo_ms, hi_ms):
    out = []
    for s in RC.UNIVERSE:
        _, t = replay(s, card, lo_ms, hi_ms)
        out += t
    return out


# ═══════════════════════════════════════════ THE REGISTRATIONS — m = 3
def registration_text() -> pd.DataFrame:
    return pd.DataFrame([
        {"registration": "P-CHAIN-2", "prior_pct": 45,
         "claim": "weave-exit + ONE re-entry (BOTH tide clauses, <=24 bars, "
                  "fresh railed stop; the chain is one campaign including its "
                  "funding) beats card v6",
         "ruler": "TWO-SAMPLE asset-cluster — the arm CHANGES the campaign set",
         "named_caveat": "TIER-C7's P-CHAIN-1 cleared on a PAIRED ruler and was "
                         "reversed: a chain holds its slot longer, so control "
                         "campaigns never open and the arm is credited for "
                         "moves it captured inside a surviving twin while the "
                         "control campaign that captured them is deleted from "
                         "the comparison. The set-change law is why this arm is "
                         "two-sample."},
        {"registration": "P-AE-2", "prior_pct": 40,
         "claim": f"exiting any campaign whose adverse excursion reaches "
                  f"{AE2_THRESHOLD_R}R beats card v6",
         "ruler": "PAIRED per-campaign delta — the arm rides inside the set",
         "named_caveat": f"CARD-CONDITIONAL by operator ruling. The threshold "
                         f"was FROZEN IN STEP 1 by a NAMING RULE fixed before "
                         f"any scoring: {AE2_RULE}. It resolved to "
                         f"{AE2_THRESHOLD_R}R at n={AE2_MEASURED['n_at_or_beyond']}, "
                         f"P(win)={AE2_MEASURED['p_win_pct']}%. THE RULE "
                         f"RE-DERIVED THE SAME 0.60R P-AE-1 WAS GIVEN FROM THE "
                         f"CENSORED CURVE, so this arm rides the identical card "
                         f"and produces the identical book. It is not a second "
                         f"independent look; it is P-AE-1 with its threshold "
                         f"honestly sourced."},
        {"registration": "P-ANC-1", "prior_pct": 45,
         "claim": "the ladder anchored on the M-band edge at 0.50 ATR, under "
                  "MATCHED TIMING, beats card v6",
         "ruler": "the set-change law decides; reported on the row",
         "named_caveat": "TIER-C7's bake-off named this anchor the winner at "
                         "+118.75 R — with 696 advances against the pivot's "
                         "228. The cadence, not the anchor, may have been the "
                         "edge. Under matched timing a (2,2) confirmation is "
                         "the only moment ANY anchor may advance, so this is "
                         "the de-confounded question."},
    ])


def score(base: list, arms: dict) -> pd.DataFrame:
    """THREE ARMS, THE RULER CHOSEN BY THE SET-CHANGE LAW, m = 3.

    m COUNTS INDEPENDENTLY-FAILABLE HYPOTHESES [TC7-c].  TIER-C7 filed P-HYB-1
    and P-CHAIN-1 as two slots when they differed by an anchor worth +0.0369 R
    — one hypothesis reported twice, making the correction looser than the
    evidence warranted.  Three genuinely separable questions are filed here:
    does the round trip pay, does early invalidation pay, does the anchor pay.

    P-WEV RIDES AS A REPORT-ONLY LINE and takes no slot: TIER-C7 already
    answered it (-0.0027, CI [-0.008, +0.003], LOAO 0/5) and re-filing it would
    buy a second bite at a question already settled.
    """
    rows = []
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    ref = _ci_from(cluster_boot(bnet, bcl), float(np.mean(bnet)))
    rows.append({"registration": "(reference)", "arm": "CARD v6 vs zero",
                 "prior_pct": None, "n": len(base),
                 "expectancy_r": r6(float(np.mean(bnet))),
                 "net_r": r4(sum(bnet)), "ruler": "vs zero",
                 "ci_point": r6(ref["point"]), "ci_lo": r6(ref["lo"]),
                 "ci_hi": r6(ref["hi"]),
                 "p_one_sided": r6(ref["p_one_sided"]),
                 "verdict": "SUPPORTED" if (ref["lo"] or 0) > 0
                            else "NOT SUPPORTED",
                 "loao_line": "—", "scored_in_family": False,
                 "note": "not an acceptance test; excluded from m"})
    for reg, prior, key in (("P-CHAIN-2", 45, "chain"), ("P-AE-2", 40, "ae"),
                            ("P-ANC-1", 45, "anchor")):
        book = arms[key]
        pv, pc = [], []
        for t in book:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                pv.append(t.net_r - bu[k])
                pc.append(t.symbol)
        changes = (len(base) - len(pv)) > 0 or (len(book) - len(pv)) > 0
        rs = [t.net_r for t in book]
        ac = [t.symbol for t in book]
        ci_p = _ci_from(cluster_boot(pv, pc), float(np.mean(pv)) if pv else None)
        pt2 = float(np.mean(rs)) - float(np.mean(bnet))
        ci_2 = _ci_from(cluster_boot_diff(rs, ac, bnet, bcl), pt2)
        ci = ci_2 if changes else ci_p
        lo_ = T7.loao(book, base, reg, two_sample=changes)
        good = bool(ci["lo"] is not None and ci["lo"] > 0)
        rows.append({
            "registration": reg, "arm": f"{reg} vs card v6", "prior_pct": prior,
            "n": len(book), "expectancy_r": r6(float(np.mean(rs))),
            "net_r": r4(sum(rs)),
            "ruler": ("TWO-SAMPLE (the arm CHANGES the campaign set)"
                      if changes else "PAIRED (the arm rides inside the set)"),
            "ruler_is_two_sample": bool(changes),
            "ci_point": r6(ci["point"]), "ci_lo": r6(ci["lo"]),
            "ci_hi": r6(ci["hi"]), "p_one_sided": r6(ci["p_one_sided"]),
            "verdict": "SUPPORTED" if good else "NOT SUPPORTED",
            "paired_ci_point": r6(ci_p["point"]), "paired_ci_lo": r6(ci_p["lo"]),
            "paired_ci_hi": r6(ci_p["hi"]),
            "two_sample_ci_point": r6(ci_2["point"]),
            "two_sample_ci_lo": r6(ci_2["lo"]),
            "two_sample_ci_hi": r6(ci_2["hi"]),
            "paired_n": len(pv), "unpaired_base_n": len(base) - len(pv),
            "unpaired_base_net_r": r4(sum(
                v for k, v in bu.items()
                if k not in {(t.symbol, t.lane, t.entry_ms) for t in book})),
            "whole_book_difference_r": r4(sum(rs) - sum(bnet)),
            "scored_in_family": True,
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            **d15(book, base)})
    d = pd.DataFrame(rows)
    m = int(d["scored_in_family"].sum())
    bar = FDR_Q / m
    d["fdr_m_tests_actually_run"] = m
    d["fdr_bar_q_over_m"] = r6(bar)
    d["clears_bh_bar"] = [
        (None if not r_["scored_in_family"]
         else bool(r_["p_one_sided"] is not None and r_["p_one_sided"] <= bar))
        for _, r_ in d.iterrows()]
    d["fdr_note"] = (
        f"m = {m}, counting INDEPENDENTLY-FAILABLE HYPOTHESES [TC7-c]. "
        f"P-WEV rides report-only and takes no slot; TIER-C7 already settled "
        f"it. q = {FDR_Q}, bar = q/m = {bar:.5f}.")
    return d


def anchor_grid(base: list, lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """THE GRID, WHOLE — ten cells, no promotion, ADVANCE COUNTS PRINTED.

    The advance counts are the column TIER-C7's table did not have, and they are
    why this one can be read: under matched timing every cell gets the SAME
    opportunities, so a difference in advances taken is the anchor's doing and
    not the clock's.
    """
    rows = []
    for kind in ANCHORS:
        for off in OFFSETS:
            bk = run_cell(Card(name=f"{kind}@{off}", anchor_kind=kind,
                               anchor_offset=off), lo_ms, hi_ms)
            rs = [t.net_r for t in bk]
            rows.append({
                "cell": f"{kind} @ {off:.2f} ATR", "anchor": kind,
                "offset_atr": off, "n": len(bk), "net_r": r4(sum(rs)),
                "expectancy_r": r6(float(np.mean(rs))),
                "advances_taken": sum(len(t.advances) for t in bk),
                "advance_opportunities": sum(t.n_opportunities for t in bk),
                "is_the_pre_named_prior": bool(kind == "max_pivot_e89"
                                               and abs(off - 0.50) < 1e-9),
                "is_the_registered_anchor": bool(kind == "m_edge"
                                                 and abs(off - 0.50) < 1e-9),
                "promotable": False,
                "no_promotion": ("CONTEXT ONLY. No cell of this grid may be "
                                 "promoted. P-ANC-1 was named before the look "
                                 "and is scored whatever this table says."),
                **d15(bk, base)})
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════════════════════════ THE DRIVER
def chain_journal(book: list, meta: dict) -> tuple:
    """THE TWO-POSITION JOURNAL — per-leg rows AND a chain rollup [PHASE C].

    The TC7-a class is retired by SCHEMA rather than by four repairs: there is
    no single-campaign slot left for a two-position answer, because the legs
    have their own rows and the rollup says how many there are.
    """
    legs, roll = [], []
    for t in book:
        f = frame(t.symbol)["f"]
        for k, lg in enumerate(t.chain["legs"]):
            legs.append({
                "asset": t.symbol, "entry_ms": int(t.entry_ms), "leg": k,
                "chain_entry_ts": iso(t.entry_ms),
                "leg_entry_ts": iso(int(f.open_ms[lg["entry_i"]])),
                "leg_entry_px": r6(lg["entry_px"]),
                "leg_stop0_px": r6(lg["stop0"]), "leg_own_r": r6(lg["own_r"]),
                "chain_r": r6(t.r_dist), "leg_size": r6(t.leg_sizes[k]),
                "leg_exit_ts": iso(int(f.open_ms[lg["exit_i"]])),
                "leg_exit_px": r6(lg["exit_px"]),
                "leg_exit_reason": lg["exit_reason"],
                "leg_advances": len(lg["advances"]),
                "leg_opportunities": lg["n_opportunities"],
                "leg_harvested": bool(lg["harvest"]),
                "leg_mfe_r_sized": r6(t.leg_sizes[k]
                                      * (lg["mfe"] - lg["entry_px"])
                                      * t.direction / t.r_dist),
                "leg_mae_r_sized": r6(t.leg_sizes[k] * lg["mae"])})
        roll.append({
            "asset": t.symbol, "entry_ms": int(t.entry_ms),
            "entry_ts": iso(t.entry_ms), "n_legs": len(t.chain["legs"]),
            "n_reentries": t.n_reentries, "n_harvests": t.n_harvests,
            "chain_net_r": r6(t.net_r), "chain_mfe_r": r6(t.mfe_r),
            "chain_mae_r": r6(t.mae_r),
            "advances_all_legs": len(t.advances),
            "opportunities_all_legs": t.n_opportunities,
            "ratchet_exit_last_leg": bool(t.ratchet_exit),
            "harvested_any_leg": bool(t.harvested),
            "reentry_refused": t.reentry_refused,
            "funding_ceiling_bound_chain": bool(t.funding_ceiling_bound)})
    return (stamp(pd.DataFrame(legs), meta), stamp(pd.DataFrame(roll), meta))


def run(root: Path) -> dict:
    global AS_OF
    t0 = time.time()
    lo, hi, meta = corridor()
    AS_OF = meta["last_closed_4h_close"]
    man = {"seed": SEED, "stage": "TIER-C7-C + TIER-C8", "sha": {},
           "keys": {}, "counts": {}, "as_of": AS_OF,
           "corridor": {k: v for k, v in meta.items()
                        if k not in ("wall_clock_at_run", "cache_lag_hours")},
           "corridor_warranty": ("TC6V-a: every table carries an as_of stamp; "
                                 "these numbers are true of this corridor and "
                                 "of no other"),
           "cache_drift_note": (
               "TC6V-b: the offline cache is NOT frozen. It gains boundary bars "
               "between builds, so a filed table is not bit-reproducible across "
               "a refresh — measured in TC6-V at +1 approach on 30 of 313 "
               "league rows even pinned to the parent's corridor end. Drift is "
               "DOCUMENTED here, not eliminated."),
           "ae2_preregistration": {"rule": AE2_RULE, "frozen_value_r": AE2_THRESHOLD_R,
                                   "measured": AE2_MEASURED,
                                   "is_identical_to_p_ae_1": AE2_IS_AE1}}
    log("=" * 78)
    log("TIER-C7-C + TIER-C8 · THE CLEAN CHAINS AND THE HONEST ANCHOR")
    log("=" * 78)
    log(f"  AS OF {AS_OF} · corridor {meta['span_days']} d")
    log(f"  P-AE-2 THRESHOLD FROZEN IN STEP 1: {AE2_THRESHOLD_R}R "
        f"(n={AE2_MEASURED['n_at_or_beyond']}, "
        f"P(win)={AE2_MEASURED['p_win_pct']}%, uncensored tape side)")

    base = run_cell(CARD_V6_CONTROL, lo, hi)
    arms = {"chain": run_cell(CARD_CHAIN2, lo, hi),
            "ae": run_cell(CARD_AE2, lo, hi),
            "anchor": run_cell(CARD_ANC1, lo, hi),
            "wev": run_cell(CARD_WEV, lo, hi)}
    for k, b in [("v6", base)] + list(arms.items()):
        log(f"  {k:7} n={len(b):4d} net={sum(t.net_r for t in b):+9.4f}")

    root.mkdir(parents=True, exist_ok=True)
    W, K, SK = {}, {}, []

    def put(df, name, key):
        if df is None or not len(df):
            log(f"    (skip {name} — empty)")
            SK.append(name)
            return
        df = stamp(df, meta) if "as_of_last_closed_4h" not in df.columns else df
        df = df.copy()
        df.attrs = {}
        df.columns = [str(c) for c in df.columns]
        W[name] = write_table(df, name, key, root)
        K[name] = list(key)

    put(pd.concat([headline_v6(base, "CARD v6 (control)", lo, hi),
                   headline_v6(arms["chain"], "v8 CHAIN-2", lo, hi),
                   headline_v6(arms["anchor"], "v8 ANCHOR M-edge", lo, hi)],
                  ignore_index=True),
        "headline", ["label", "aggregation", "universe", "group", "key"])
    put(registration_text(), "registration_text", ["registration"])
    put(score(base, arms), "registrations", ["registration"])
    put(anchor_grid(base, lo, hi), "anchor_grid", ["cell"])
    lg, roll = chain_journal(arms["chain"], meta)
    put(lg, "chain_legs", ["asset", "entry_ms", "leg"])
    put(roll, "chain_rollup", ["asset", "entry_ms"])
    put(journal_frame(base), "trade_journal_control", ["asset", "entry_ms"])
    # P-WEV, REPORT-ONLY — no slot in the family
    wv = arms["wev"]
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    pv = [t.net_r - bu[(t.symbol, t.lane, t.entry_ms)] for t in wv
          if (t.symbol, t.lane, t.entry_ms) in bu]
    ci = _ci_from(cluster_boot(pv, [t.symbol for t in wv
                                    if (t.symbol, t.lane, t.entry_ms) in bu]),
                  float(np.mean(pv)))
    put(pd.DataFrame([{
        "line": "P-WEV re-check", "scored_in_family": False,
        "n": len(wv), "net_r": r4(sum(t.net_r for t in wv)),
        "paired_delta_total_r": r4(sum(pv)),
        "ci_point": r6(ci["point"]), "ci_lo": r6(ci["lo"]),
        "ci_hi": r6(ci["hi"]),
        "weave_firings_all_legs": sum(1 for t in wv
                                      if t.exit_reason == "weave"),
        "note": ("REPORT-ONLY under the corrected counts [TC7-h]. Takes no "
                 "slot in the m=3 family: TIER-C7 already settled it and "
                 "re-filing would buy a second bite at a decided question.")}]),
        "p_wev_recheck", ["line"])

    man["sha"], man["keys"], man["skipped_empty"] = W, K, SK
    man["counts"] = {f"{k}_n": len(b) for k, b in
                     [("v6", base)] + list(arms.items())}
    man["counts"].update({f"{k}_net_r": r4(sum(t.net_r for t in b))
                          for k, b in [("v6", base)] + list(arms.items())})
    # TC7-h: EVERY firing, not only the ones that ended a chain
    man["counts"]["weave_firings_any_leg"] = sum(
        1 for t in arms["chain"] for lg in t.chain["legs"]
        if lg["exit_reason"] == "weave")
    man["counts"]["weave_firings_final_leg_only"] = sum(
        1 for t in arms["chain"] if t.exit_reason == "weave")
    man["elapsed_s"] = round(time.time() - t0, 1)
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"\n  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    run(OUT_RERUN if ap.parse_args().rerun else OUT)
