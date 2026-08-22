#!/usr/bin/env python
"""TIER-C9 · THE WINNERS' HABITAT + THE PAIR SWEEP.

RATIFIED operator 2026-08-18 ("unlazy... which numbers is the alpha hiding
in... is 12/26 better than 9/26... produce paste for tc9").  Drafted APOLLO,
executed under the same charter; seed 20260818.  In-sample REOPENED by
operator word, THIS RUN'S SCOPE ONLY — the estate's in-sample program closed
with TIER-C8 and this build does not reopen it beyond its own two stages.

THE REFRAME, RECORDED [doc §0]: business concentration = the model; the D15
guard polices CLAIMS only.  Concentration columns ride every row and gate
nothing ("D15 caveats not hard gates" — THE_RULING, tierc5_rules.py).

STAGE A — THE LEDGER TABLES.  Display-only, from tape+journal, zero
estimation: no bootstrap, no CI, no fitted anything.  Every number is a
measurement of the F-CTRL-certified control book (== card v6) or of the raw
bars and funding stamps beneath it.

STAGE B — THE PAIR SWEEP.  OFAT vs card v6 on the EMA periods of the three
gates.  DECISION OF RECORD (D1, disclosed in the build doc): v6's arrays
ALIAS — the window (12/89) shares its fast array with the trigger (12/26) and
its slow array with the tide-fast (89) — so this module DE-ALIASES the frame
into SIX role arrays (tide_f/s, window_f/s, trigger_f/s).  Role ownership:
  WINDOW  owns the window cross AND the displacement measure
          (|close − window_slow| / ATR: the rule card states displacement
          inside the WINDOW clause);
  TIDE    owns the tide gate, the HARVEST BAND (tierc4's re-pointed law:
          HARVEST_BAND = (TIDE_FAST, TIDE_SLOW) moves WITH the tide), and the
          warm-up re-point;
  TRIGGER owns the entry crosses.
  BELL    = counter-WINDOW-cross OR counter-TIDE-cross, each from its role's
          arrays; exit labels carry the live periods (bell_12_89 under v6).
Under v6 periods all six arrays coincide bit-for-bit with e12/e26/e89/e316,
which is what lets F-CTRL demand EXACTLY 0.000e+00.
Without de-aliasing, the commissioned "window 9/89" cell and "trigger 9/26"
cell would be the SAME cell (both would move e12) — the commission is only
coherent under role semantics.

THE RULER (D3): TWO-SAMPLE asset-cluster, as commissioned — every swap
changes the campaign set (measured and printed per cell, not assumed).  D15
trio + LOAO 3/5-above per cell.  The grid is filed WHOLE; no promotion.
ONE registration, operator-named: P-TRG-1 [50%] — trigger 9/26 replacing
12/26, all else v6.  m = 1, so the BH bar is q/m = 0.10.

Bootstrap seeds keep the estate convention: cluster_boot/cluster_boot_diff
default to tierc5.SEED = 20260816 (as in TIER-C7/C8; this module's SEED
stamps the manifest).  Run: ~/venvs/naiad/bin/python scripts/tierc9.py
"""
from __future__ import annotations

import json
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as V6                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402
import tierc2_baseline as TB                                         # noqa: E402
import tierc2_rules as R2                                            # noqa: E402
from engine import indicators as ind                                 # noqa: E402

_ms, iso, r4, r6, pct = TB._ms, TB.iso, TB.r4, TB.r6, TB.pct
write_table, log = TB.write_table, TB.log
frame, fractals, corridor = T7.frame, T7.fractals, T7.corridor
agg, d15, journal_frame = T7.agg, T7.d15, T7.journal_frame
cluster_boot, cluster_boot_diff, _ci_from = (T7.cluster_boot,
                                             T7.cluster_boot_diff, T7._ci_from)
headline_v6 = T7.headline_v6
FDR_Q = T7.FDR_Q
stamp = T8.stamp
matched_step = T8.matched_step

SEED = 20260818
OUT = ROOT / "research_outputs" / "tierc9"
OUT_RERUN = ROOT / "research_outputs" / "tierc9_run2"

AS_OF: str = ""            # set by run(); every table carries it [TC6V-a]


# ═══════════════════════════════════════════ THE ROLE FRAME — DECISION D1
@dataclass(frozen=True)
class Roles:
    """The six periods, one pair per gate ROLE.  Roles() is card v6's stack:
    tide 89/316 · window 12/89 · trigger 12/26 — all 4h (tierc2_rules law).
    """
    name: str = "v6-roles"
    tide_f: int = RC.TIDE_FAST          # 89
    tide_s: int = RC.TIDE_SLOW          # 316
    win_f: int = 12                     # v6 window fast (aliases TRIGGER_FAST)
    win_s: int = 89                     # v6 window slow (aliases TIDE_FAST)
    trg_f: int = R2.TRIGGER_FAST        # 12
    trg_s: int = R2.TRIGGER_SLOW        # 26

    @property
    def periods(self) -> tuple:
        return (self.tide_f, self.tide_s, self.win_f, self.win_s,
                self.trg_f, self.trg_s)

    @property
    def floor_bars(self) -> int:
        """THE WARM-UP FLOOR, PER CELL [D2]: never below the estate's 316
        (identical corridors unless a cell genuinely needs more), and never
        below the cell's own slowest EMA (an unseeded gate must not fire)."""
        return max(RC.WARMUP_BARS, max(self.periods))


V6_ROLES = Roles()

# THE SEVEN CELLS, AS COMMISSIONED — one pair swapped per cell, all else v6.
SWEEP_CELLS = (
    Roles(name="tide-62/262",  tide_f=62,  tide_s=262),
    Roles(name="tide-127/423", tide_f=127, tide_s=423),
    Roles(name="tide-89/423",  tide_f=89,  tide_s=423),
    Roles(name="window-9/89",  win_f=9,  win_s=89),
    Roles(name="window-26/89", win_f=26, win_s=89),
    Roles(name="trigger-9/26", trg_f=9, trg_s=26),     # P-TRG-1
    Roles(name="trigger-9/12", trg_f=9, trg_s=12),
)
REGISTERED_CELL = "trigger-9/26"

_RA: dict[tuple, dict] = {}     # (sym, roles) -> role arrays + crosses


def role_arrays(sym: str, roles: Roles) -> dict:
    """Six EMAs and every cross the rule card names, from THIS role stack.

    Arrays are built by the engine's own `ind.ema` on the shared frame's close
    — same function, same input as `RC.build_4h`, so under v6 periods each
    role array is bit-identical to its e12/e26/e89/e316 twin and F-CTRL can
    demand exact zero.

    WHAT WOULD MAKE THIS WRONG: reading a period through the frame's e-fields
    (that is the aliasing this module exists to remove), or caching without
    the roles in the key (a swept cell would read the incumbent's arrays —
    the F-C8-MATCH poisoned-cache lesson, one tier later).
    """
    k = (sym, roles.periods)
    if k in _RA:
        return _RA[k]
    c = frame(sym)["f"].c
    a = {
        "tide_f": ind.ema(c, roles.tide_f), "tide_s": ind.ema(c, roles.tide_s),
        "win_f": ind.ema(c, roles.win_f), "win_s": ind.ema(c, roles.win_s),
        "trg_f": ind.ema(c, roles.trg_f), "trg_s": ind.ema(c, roles.trg_s),
    }
    a["w_up"] = ind.crossover(a["win_f"], a["win_s"])
    a["w_dn"] = ind.crossunder(a["win_f"], a["win_s"])
    a["t_up"] = ind.crossover(a["trg_f"], a["trg_s"])
    a["t_dn"] = ind.crossunder(a["trg_f"], a["trg_s"])
    a["b_up"] = ind.crossover(a["tide_f"], a["tide_s"])
    a["b_dn"] = ind.crossunder(a["tide_f"], a["tide_s"])
    _RA[k] = a
    return a


def armings9(sym: str, roles: Roles, lo_i: int, hi_i: int) -> list:
    """RC.armings, de-aliased [D1].  Window cross from the WINDOW arrays; tide
    gate from the TIDE arrays; displacement |close − window_slow| / ATR (the
    rule card names displacement inside the WINDOW clause).

    WHAT WOULD MAKE THIS WRONG: reading any gate through another role's
    arrays, or evaluating the tide anywhere but the arming bar."""
    f = frame(sym)["f"]
    ra = role_arrays(sym, roles)
    n = len(f.c)
    out = []
    for direction, opens, counter in ((1, ra["w_up"], ra["w_dn"]),
                                      (-1, ra["w_dn"], ra["w_up"])):
        for i in np.flatnonzero(opens):
            i = int(i)
            if not (lo_i <= i <= hi_i):
                continue
            later = np.flatnonzero(counter[i + 1:])
            end_i = int(i + 1 + later[0]) if later.size else n
            if direction == 1:
                tide = bool(ra["tide_f"][i] > ra["tide_s"][i]
                            and f.c[i] > ra["tide_s"][i])
            else:
                tide = bool(ra["tide_f"][i] < ra["tide_s"][i]
                            and f.c[i] < ra["tide_s"][i])
            a_ = f.atr[i]
            disp = (float(abs(f.c[i] - ra["win_s"][i]) / a_)
                    if (np.isfinite(a_) and a_ > 0) else float("nan"))
            d_ok = bool(np.isfinite(disp) and disp >= R2.D_DISPLACEMENT)
            out.append(RC.Arming(
                symbol=sym, direction=direction, arm_i=i,
                arm_ms=int(f.open_ms[i]), window_end_i=end_i,
                tide_ok=tide, disp=disp, d_ok=d_ok,
                strip_d_ok={s: bool(np.isfinite(disp) and disp >= s)
                            for s in R2.D_STRIP}))
    out.sort(key=lambda a: (a.arm_ms, -a.direction))
    return out


def card_candidates9(sym: str, roles: Roles, lo_i: int, hi_i: int):
    """tierc5.card_candidates, de-aliased: trigger crosses from the TRIGGER
    arrays.  Gate order unchanged: tide → d → trigger."""
    f = frame(sym)["f"]
    ra = role_arrays(sym, roles)
    arms = armings9(sym, roles, lo_i, hi_i)
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
        trig = ra["t_up"] if a.direction == 1 else ra["t_dn"]
        end = min(a.window_end_i, hi_i + 1)
        c = np.flatnonzero(trig[a.arm_i:end])
        if c.size == 0:
            a.reject = "no_trigger"
            continue
        ti = int(a.arm_i + c[0])
        a.trigger_i, a.trigger_ms = ti, int(f.open_ms[ti])
        cands.append((ti, a.direction, a))
    return arms, cands


# ═══════════════════════════════════════════════════ THE RIDE, DE-ALIASED
def _ride_leg9(sym, card, roles: Roles, d, ti, entry_px, stop0, r_dist, hi_i):
    """TIER-C8's leg (which reproduces card v6 at 0.000e+00), with the two
    array reads the sweep moves re-pointed to their ROLES [D1]:
      · the harvest band edge reads (tide_f, tide_s) — the re-pointed law;
      · the bells read the counter-WINDOW cross and the counter-TIDE cross,
        each from its role's arrays, labelled with the LIVE periods so a
        swapped cell's exit reasons cannot lie (`bell_12_89` under v6).
    Everything else — stop check order, trail arming, matched_step on the
    (2,2) pivot clock, harvest arithmetic — is the parent's, verbatim.

    WHAT WOULD MAKE THIS WRONG: reading a bell or band through the shared
    frame's e-fields (the aliasing), or reordering the within-bar checks
    (STOP → BELL → HARVEST → LADDER is the card's law)."""
    st = frame(sym)
    f = st["f"]
    ra = role_arrays(sym, roles)
    fr = fractals(sym, card.trail_l, card.trail_r) if card.trail else None
    s = T8.anchor_series(sym)
    R = float(r_dist)
    stop = float(stop0)
    advances = []
    harv, blocked = None, ""
    mfe = float(entry_px)
    mae = 0.0
    mae_to_1r, reached_1r = 0.0, False
    trail_armed = card.trail_arm_after_r <= 0.0
    h_armed = False
    n_opp = 0
    bell_w = f"bell_{roles.win_f}_{roles.win_s}"
    bell_t = f"bell_{roles.tide_f}_{roles.tide_s}"
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
            pe = RC.harvest_edge(float(ra["tide_f"][j - 1]),
                                 float(ra["tide_s"][j - 1]), d)
            if not h_armed and RC.harvest_outside(float(f.c[j - 1]), pe, d):
                h_armed = True
            edge = RC.harvest_edge(float(ra["tide_f"][j]),
                                   float(ra["tide_s"][j]), d)
            ufill = (float(f.c[j]) - entry_px) * d / R
            touch = (harv is None and h_armed
                     and RC.harvest_touched(float(f.h[j]), float(f.l[j]),
                                            edge, d)
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
        bell = (((bell_w if bool(ra["w_dn"][j])
                  else bell_t if bool(ra["b_dn"][j]) else None)) if d == 1
                else ((bell_w if bool(ra["w_up"][j])
                       else bell_t if bool(ra["b_up"][j]) else None)))
        if bell:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), bell
            if touch:
                blocked = "bell"
            break
        if touch:
            harv = (j, RC.harvest_fill_px(f.c[j]),
                    (RC.harvest_fill_px(f.c[j]) - entry_px) * d / R)
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
            "blocked": blocked, "mfe": mfe, "mae": mae, "adds": [],
            "final_stop": stop, "n_opportunities": n_opp,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r}


def replay9(sym: str, card, roles: Roles, lo_ms: int, hi_ms: int):
    """TIER-C8's replay on the ROLE frame.  THE SCOPE IS DECLARED AND
    ENFORCED [tc8 law]: this module rides card v6's MECHANICS only — the
    swept factor is the PERIODS, never a knob.  Any v7/v8 knob set away from
    its v6 default HALTs, because a knob running silently under a sweep
    cell's name would make every "vs v6" row compare two different programs.
    """
    if card.lane != "card":
        raise SystemExit(f"HALT: tierc9.replay9 implements the CARD lane "
                         f"only; got lane={card.lane!r}.")
    if card.adds_max:
        raise SystemExit(f"HALT: tierc9 rides no adds; got "
                         f"adds_max={card.adds_max}.")
    if not card.seal_open:
        raise SystemExit("HALT: tierc9 does not thread the lockbox mask.")
    if card.trail_extra_buf_atr:
        raise SystemExit("HALT: tierc9's ladder offset arrives as "
                         "anchor_offset; trail_extra_buf_atr would drop.")
    if getattr(card, "weave", False) or getattr(card, "reentry", False):
        raise SystemExit("HALT: tierc9 rides v6 mechanics — no weave, no "
                         "re-entry. Those arms live in tierc8.")
    if getattr(card, "ae_abort_r", None) is not None:
        raise SystemExit("HALT: tierc9 rides v6 mechanics — no AE abort.")
    if card.time_stop_bars is not None:
        raise SystemExit("HALT: tierc9 rides v6 mechanics — no time stop.")
    if getattr(card, "anchor_kind", "pivot") != "pivot":
        raise SystemExit(f"HALT: tierc9 trails the card's (2,2) pivot only; "
                         f"got anchor_kind={card.anchor_kind!r}.")
    # THE KNOBS THE FIRST GUARD MISSED [review L1]: a guard that names some
    # of the knobs this module drops certifies the rest by omission — and a
    # dropped knob is the ONE class F-CTRL cannot catch, because it
    # reproduces v6 at 0.000e+00 under a lying card name.
    if getattr(card, "hybrid_anchor", False):
        raise SystemExit("HALT: tierc9 reads no hybrid anchor; it would "
                         "ride silently as pure pivot.")
    if getattr(card, "stop_grid_offset_atr", 0.0):
        raise SystemExit("HALT: tierc9 reads no stop-grid offset; the S-SG "
                         "dimension would silently drop.")
    if card.anchor_offset != RC.STOP_BUF_ATR:
        raise SystemExit(f"HALT: tierc9 is a PERIOD sweep — anchor_offset="
                         f"{card.anchor_offset} would run the v8 S-OFF "
                         f"dimension under a period-cell's name.")
    if card.harvest != "band":
        raise SystemExit(f"HALT: tierc9 implements the band harvest only; "
                         f"harvest={card.harvest!r} would ride with NO "
                         f"harvest at all.")
    st = frame(sym)
    f = st["f"]
    lo_i, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
    lo_i = max(lo_i, roles.floor_bars)          # THE FLOOR, PER CELL [D2]
    if hi_i < lo_i:
        return [], []
    arms, cc = card_candidates9(sym, roles, lo_i, hi_i)
    cands = [(ti, d, "card", a) for ti, d, a in cc]
    cands.sort(key=lambda c: (c[0], -c[1], c[2]))
    trades, open_until = [], -1
    for ti, d, kind, arm in cands:
        if ti <= open_until:
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
        arm.entered, arm.reject, arm.entry_scored = True, "entered", True
        leg = _ride_leg9(sym, card, roles, d, ti, entry_px, stp.stop_px,
                         stp.r_dist, hi_i)
        chain = {"legs": [leg], "n_reentries": 0, "reentry_refused": ""}
        open_until = leg["exit_i"]
        acc = T7._account_chain(sym, card, d, stp.r_dist, chain)
        harv = leg["harvest"]
        t = RC.Trade(
            symbol=sym, lane=kind, direction=d,
            arm_i=arm.arm_i, arm_ms=arm.arm_ms, entry_i=ti,
            entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stp.stop_px, r_dist=stp.r_dist, anchor=stp.anchor,
            anchor_bar_ms=(int(f.open_ms[stp.anchor_bar])
                           if stp.anchor_bar >= 0 else -1),
            anchor_was_sealed=bool(
                stp.anchor_bar >= 0
                and _ms(RC.LOCKBOX_WAS[0])
                <= int(f.open_ms[stp.anchor_bar])
                <= _ms(RC.LOCKBOX_WAS[1]) + 86_400_000 - 1),
            atr_at_entry=atr_sig,
            disp_at_arming=arm.disp,
            exit_i=leg["exit_i"], exit_ms=int(f.open_ms[leg["exit_i"]]),
            exit_px=leg["exit_px"], exit_reason=leg["exit_reason"],
            bars_held=leg["exit_i"] - ti, scored=True,
            advances=list(leg["advances"]),
            final_stop_px=leg["final_stop"],
            stop_advanced_atr=(leg["final_stop"] - leg["stop0"]) * d / atr_sig,
            ratchet_exit=bool(leg["exit_reason"] == "stop" and leg["advances"]
                              and abs(leg["final_stop"] - leg["stop0"]) > 1e-12),
            harvested=harv is not None,
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=leg["blocked"],
            harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
            adds=[], add_r=None, spring=None,
            mfe_r=(leg["mfe"] - entry_px) * d / stp.r_dist,
            mae_to_1r_r=leg["mae_to_1r"], reached_1r=leg["reached_1r"],
            gross_r=acc["gross_r"], fee_r=acc["fee_r"],
            funding_r=acc["funding_r"],
            funding_r_uncapped=acc["funding_r_uncapped"],
            funding_ceiling_bound=acc["funding_ceiling_bound"],
            net_r=acc["net_r"], net_r_harvest_half=acc["n1"],
            net_r_runner_half=acc["n2"], net_r_bellonly=None)
        for k, v in (("mae_r", leg["mae"]),
                     ("n_opportunities", leg["n_opportunities"]),
                     ("roles_name", roles.name)):
            object.__setattr__(t, k, v)
        trades.append(t)
    return arms, trades


def run_cell9(card, roles: Roles, lo_ms: int, hi_ms: int) -> list:
    out = []
    for s_ in RC.UNIVERSE:
        _, t = replay9(s_, card, roles, lo_ms, hi_ms)
        out += t
    return out


# ═══════════════════════ STAGE A · THE LEDGER TABLES — display-only [D4]
# Zero estimation: no bootstrap, no CI, no fitted anything.  Measurements of
# the F-CTRL-certified control book, the raw 4h bars and the funding stamps.

def excursions9(t) -> dict:
    """BOTH excursion twins, BOTH sides, from raw 4h bars [tc6v law].

    HELD clips the EXIT bar at the exit price when the exit was a stop; TAPE
    does not.  Both scan bars entry+1 .. exit — the range the ride scans.
    NEW HERE (disclosed [D4]): the FAVORABLE twins under the same clip law —
    on a stop-exit bar the position is closed at the stop, so any favorable
    extreme printed on that bar after the exit is tape, not held.

    WHAT WOULD MAKE THIS WRONG: including the entry bar, scanning past the
    exit, or clipping the tape readings (the twins would collapse and the
    comparison would be pointless)."""
    f = frame(t.symbol)["f"]
    d, e, R = t.direction, float(t.entry_px), float(t.r_dist)
    lo, hi = t.entry_i + 1, t.exit_i
    if hi < lo:
        return {"mae_held_r": 0.0, "mae_tape_r": 0.0, "gap_through_r": 0.0,
                "mfe_held_r": 0.0, "mfe_tape_r": 0.0}
    adv = f.l[lo:hi + 1] if d == 1 else f.h[lo:hi + 1]
    fav = f.h[lo:hi + 1] if d == 1 else f.l[lo:hi + 1]
    tape = float(np.min((adv - e) * d)) / R
    mfe_tape = float(np.max((fav - e) * d)) / R
    held, mfe_held = tape, mfe_tape
    if t.exit_reason == "stop":
        adv_h = np.array(adv, dtype=float, copy=True)
        adv_h[-1] = float(t.exit_px)     # the stop took the bar, not its low
        held = float(np.min((adv_h - e) * d)) / R
        fav_h = np.array(fav, dtype=float, copy=True)
        fav_h[-1] = float(t.exit_px)     # ...nor its high
        mfe_held = float(np.max((fav_h - e) * d)) / R
    return {"mae_held_r": r6(min(held, 0.0)), "mae_tape_r": r6(min(tape, 0.0)),
            "gap_through_r": r6(min(held, 0.0) - min(tape, 0.0)),
            "mfe_held_r": r6(max(mfe_held, 0.0)),
            "mfe_tape_r": r6(max(mfe_tape, 0.0))}


def entry_only_r(t, card, corridor_hi_i: int) -> dict:
    """THE ENTRY-vs-MANAGEMENT SPLIT's counterfactual [D4, disclosed]: the
    same entry ridden with NO management — initial stop only; no trail, no
    harvest, no bells.  Exit at stop0 when the bar range touches it, else
    the CORRIDOR-end close (threaded in, never the cache end — a longer
    cache on one asset must not accrue funding past the as-of stamp
    [review L3]).  Fees and funding through the estate's own
    `_account_chain`, so the arithmetic cannot drift from the book's —
    WHICH MEANS THE D12 FUNDING CEILING APPLIES HERE TOO, and on a
    counterfactual that can hold for years the cap BINDS where no real
    campaign's ever did.  Disclosed per row: the uncapped funding and the
    bound flag ride beside the value [review L3].
    management_delta_r = net_r − net_r_entry_only."""
    f = frame(t.symbol)["f"]
    d, stop0 = t.direction, float(t.stop_px)
    hi_i = t.exit_i if t.exit_reason == "corridor_end" else corridor_hi_i
    xi, xpx = None, None
    for j in range(t.entry_i + 1, hi_i + 1):
        if (d == 1 and f.l[j] <= stop0) or (d == -1 and f.h[j] >= stop0):
            xi, xpx = j, stop0
            break
    if xi is None:
        xi, xpx = hi_i, float(f.c[hi_i])
    leg = {"entry_i": t.entry_i, "exit_i": xi, "exit_px": float(xpx),
           "entry_px": float(t.entry_px), "harvest": None, "adds": [],
           "own_r": float(t.r_dist)}
    acc = T7._account_chain(t.symbol, card, d, float(t.r_dist),
                            {"legs": [leg]})
    return {"net_r": float(acc["net_r"]),
            "funding_r_uncapped": float(acc["funding_r_uncapped"]),
            "ceiling_bound": bool(acc["funding_ceiling_bound"]),
            "bars": int(xi - t.entry_i)}


def tide_streak_age(t, roles: Roles) -> tuple:
    """(age_bars, censored) — consecutive bars ending AT THE ARM BAR whose
    tide state equals the arm bar's, the flip bar counting as bar 1 [lab
    convention, tierc7_lab_regime].  State from the ROLE arrays: +1 when
    tide_f>tide_s and close>tide_s, −1 mirrored, else 0.  censored=True when
    the count-back reached the warm-up floor — the streak is at LEAST this
    old (left-censored, counted not dropped)."""
    ra = role_arrays(t.symbol, roles)
    f = frame(t.symbol)["f"]

    def state(j):
        if ra["tide_f"][j] > ra["tide_s"][j] and f.c[j] > ra["tide_s"][j]:
            return 1
        if ra["tide_f"][j] < ra["tide_s"][j] and f.c[j] < ra["tide_s"][j]:
            return -1
        return 0
    floor = roles.floor_bars
    s0 = state(t.arm_i)
    age = 1
    j = t.arm_i - 1
    while j >= floor and state(j) == s0:
        age += 1
        j -= 1
    return age, bool(j < floor)


def _wall_stamps() -> pd.DataFrame:
    """The per-campaign wall stamps, JOINED from tierc6's L-WALLQ (row_kind ==
    'campaign'; stamps are taken AT THE ARMING so a corridor extension cannot
    move them).  tierc6-vintage — campaigns it does not cover are stamped
    'not_in_l_wallq' rather than guessed."""
    p = ROOT / "research_outputs" / "tierc6" / "l_wallq.parquet"
    if not p.exists():
        return pd.DataFrame(columns=["asset", "entry_ms"])
    w = pd.read_parquet(p)
    w = w[w["row_kind"] == "campaign"].copy()
    ks = w["key"].str.split("|", expand=True)
    w["asset"], w["entry_ms"] = ks[0], ks[1].astype(np.int64)
    keep = ["asset", "entry_ms", "profit_side", "champion_ema", "champion_tf",
            "wall_px_at_entry", "wall_px_at_arm_bar", "alignment",
            "alignment_at_arm_bar", "bucket"]
    return w[[c for c in keep if c in w.columns]].rename(columns={
        "bucket": "wall_bucket", "alignment": "wall_alignment",
        "alignment_at_arm_bar": "wall_alignment_at_arm_bar"})


def _decile(sr: pd.Series) -> list:
    """Deciles by RANK, ties shared [tc6v law] — qcut on heavy ties (every
    loser's MFE is 0) raises or drops rows, and a decile table that lost its
    losers would be the whole finding."""
    v = pd.to_numeric(sr, errors="coerce")
    r = v.rank(method="average", pct=True)
    return [None if pd.isna(x) else int(min(9, np.floor(x * 10))) for x in r]


def features9(book: list, card, lo_ms: int, hi_ms: int,
              roles: Roles = V6_ROLES) -> pd.DataFrame:
    """ONE ROW PER CAMPAIGN — the AUTOPSY SCHEMA, for all 196, so the
    separation table compares medians over the same columns the top-10
    life-cycles print.  Every column is a measurement."""
    rows = []
    hi_by_sym = {}
    for t in book:
        f = frame(t.symbol)["f"]
        if t.symbol not in hi_by_sym:
            hi_by_sym[t.symbol] = T7._idx_range(f.open_ms, lo_ms, hi_ms)[1]
        ex = excursions9(t)
        j1 = None
        for j in range(t.entry_i + 1, t.exit_i + 1):
            fv = float(f.h[j]) if t.direction == 1 else float(f.l[j])
            if (fv - t.entry_px) * t.direction / t.r_dist >= 1.0:
                j1 = j
                break
        age, cens = tide_streak_age(t, roles)
        eo = entry_only_r(t, card, hi_by_sym[t.symbol])
        rows.append({
            "asset": t.symbol, "entry_ms": int(t.entry_ms),
            "entry_ts": iso(t.entry_ms), "year": iso(t.entry_ms)[:4],
            "direction": "long" if t.direction == 1 else "short",
            "disp_at_arming": r6(float(t.disp_at_arming)),
            "lag_arm_to_entry_bars": int(t.entry_i - t.arm_i),
            "tide_streak_age_bars": int(age),
            "tide_streak_left_censored": bool(cens),
            "r_over_atr": r6(float(t.r_dist) / float(t.atr_at_entry)
                             if t.atr_at_entry else None),
            "r_dist": r6(float(t.r_dist)),
            "atr_at_entry": r6(float(t.atr_at_entry)),
            **ex,
            "bars_to_1r": (int(j1 - t.entry_i) if j1 is not None else None),
            "reached_1r": bool(t.reached_1r),
            "peak_vs_kept_pct": (r4(100.0 * float(t.net_r) / ex["mfe_tape_r"])
                                 if ex["mfe_tape_r"] and ex["mfe_tape_r"] > 0
                                 else None),
            "n_advances": len(t.advances),
            "stop_advanced_atr": r6(float(t.stop_advanced_atr)),
            "harvested": bool(t.harvested),
            "harvest_unit_move_r": r6(t.harvest_unit_move_r),
            "net_r_harvest_half": r6(t.net_r_harvest_half),
            "net_r_runner_half": r6(t.net_r_runner_half),
            "harvest_ride_would_have_r": r6(t.harvest_ride_would_have_r),
            "gross_r": r6(float(t.gross_r)), "fee_r": r6(float(t.fee_r)),
            "funding_r": r6(float(t.funding_r)),
            "funding_r_uncapped": r6(float(t.funding_r_uncapped)),
            "bars_held": int(t.bars_held), "exit_reason": t.exit_reason,
            "net_r_entry_only": r6(eo["net_r"]),
            "entry_only_funding_r_uncapped": r6(eo["funding_r_uncapped"]),
            "entry_only_funding_ceiling_bound": eo["ceiling_bound"],
            "entry_only_bars": eo["bars"],
            "management_delta_r": r6(float(t.net_r) - eo["net_r"]),
            "net_r": r6(float(t.net_r)), "winner": bool(t.net_r > 0),
        })
    d = pd.DataFrame(rows)
    walls = _wall_stamps()
    if len(walls):
        d = d.merge(walls, on=["asset", "entry_ms"], how="left")
        for c in ("profit_side", "champion_ema", "champion_tf",
                  "wall_alignment", "wall_alignment_at_arm_bar",
                  "wall_bucket"):
            if c in d.columns:
                d[c] = d[c].astype(object).where(d[c].notna(),
                                                 "not_in_l_wallq")
    for c, n in (("mae_held_r", "mae_decile"), ("mfe_tape_r", "mfe_decile"),
                 ("lag_arm_to_entry_bars", "lag_decile")):
        d[n] = _decile(d[c])
    return d.sort_values(["asset", "entry_ms"]).reset_index(drop=True)


# ─────────────────────────────────────────────── A1 · the ten table families
def a1_r_deciles(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.1 — R-multiple deciles, ALL / WINNERS / LOSERS (deciles by rank
    WITHIN each population), the excursion TWINS printed per decile."""
    outs = []
    for pop, d in (("ALL", feat), ("WINNERS", feat[feat["winner"]]),
                   ("LOSERS", feat[~feat["winner"]])):
        d = d.copy()
        d["r_decile"] = _decile(d["net_r"])
        g = d.groupby("r_decile", dropna=False).agg(
            n=("net_r", "size"), net_r=("net_r", "sum"),
            mean_r=("net_r", "mean"), min_r=("net_r", "min"),
            max_r=("net_r", "max"),
            mean_mae_held_r=("mae_held_r", "mean"),
            mean_mae_tape_r=("mae_tape_r", "mean"),
            mean_mfe_held_r=("mfe_held_r", "mean"),
            mean_mfe_tape_r=("mfe_tape_r", "mean"),
            mean_bars_held=("bars_held", "mean")).reset_index()
        g.insert(0, "population", pop)
        outs.append(g)
    out = pd.concat(outs, ignore_index=True)
    for c in out.columns[3:]:
        out[c] = out[c].astype(float).round(6)
    return out


def a1_expectancy_pf(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.2 — expectancy & profit factor, GROSS and NET, the fees+funding
    split printed beside them.  PF = Σ(positive)/|Σ(negative)| [v3 law]."""
    rows = []
    for basis, col in (("gross", "gross_r"), ("net", "net_r")):
        v = feat[col].astype(float)
        pos, neg = v[v > 0].sum(), v[v < 0].sum()
        rows.append({
            "basis": basis, "n": len(v),
            "expectancy_r": r6(v.mean()), "total_r": r4(v.sum()),
            "profit_factor": (r4(pos / abs(neg)) if neg < 0 else None),
            "win_rate_pct": pct(int((v > 0).sum()), len(v)),
            "fee_r_total": r4(feat["fee_r"].sum()),
            "funding_r_total": r4(feat["funding_r"].sum()),
            "funding_r_uncapped_total": r4(feat["funding_r_uncapped"].sum()),
            "funding_ceiling_bound_n": int(
                (feat["funding_r_uncapped"] > feat["funding_r"] + 1e-12).sum()),
        })
    return pd.DataFrame(rows)


def a1_win_rate(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.3 — win rate by asset / year / direction / lag [tc6v lag-decile
    convention: no fixed bucket-edge list exists in the estate; deciles by
    rank, plus the lag==0 row (49 campaigns trigger on the arming bar)."""
    cuts = []
    for by, label in ((["asset"], "asset"), (["year"], "year"),
                      (["direction"], "direction"),
                      (["lag_decile"], "lag decile [rank, ties shared]")):
        g = feat.groupby(by, dropna=False).agg(
            n=("net_r", "size"), wins=("winner", "sum"),
            net_r=("net_r", "sum"), expectancy_r=("net_r", "mean")
        ).reset_index()
        g.insert(0, "cut", label)
        g = g.rename(columns={by[0]: "key"})
        g["key"] = g["key"].astype(str)
        cuts.append(g)
    z = feat[feat["lag_arm_to_entry_bars"] == 0]
    cuts.append(pd.DataFrame([{
        "cut": "lag == 0 (triggered on the arming bar)", "key": "0",
        "n": len(z), "wins": int(z["winner"].sum()),
        "net_r": r4(z["net_r"].sum()),
        "expectancy_r": r6(z["net_r"].mean()) if len(z) else None}]))
    out = pd.concat(cuts, ignore_index=True)
    out["win_rate_pct"] = (100.0 * out["wins"] / out["n"]).round(4)
    out["net_r"] = out["net_r"].astype(float).round(4)
    out["expectancy_r"] = out["expectancy_r"].astype(float).round(6)
    out["provisional"] = out["n"] < RC.PROVISIONAL_MIN_N
    return out


def a1_dd_tuw(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.4 — maxDD(R) and TIME-UNDER-WATER on the full corridor, measured on
    the EXIT-ORDERED step equity (tie-break (exit_ms, asset) — the estate's
    _maxdd_r law).  DISCLOSED [D4]: no per-bar mark-to-market artifact exists
    in this estate; the step equity IS the filed basis, and a bar-resolution
    curve would be a different (deeper) number."""
    d = feat.sort_values(["exit_ms", "asset"]) if "exit_ms" in feat.columns \
        else feat.assign(exit_ms=feat["entry_ms"]).sort_values(
            ["exit_ms", "asset"])
    cum = d["net_r"].astype(float).cumsum().to_numpy()
    peak = np.maximum.accumulate(np.concatenate([[0.0], cum]))[1:]
    dd = cum - peak
    max_dd = float(dd.min()) if len(dd) else 0.0
    # under-water episodes on the step clock
    ts = pd.to_datetime(d["exit_ts"].to_numpy())
    episodes = []
    peak_t, under = ts[0] if len(ts) else None, False
    peak_v = 0.0
    for i in range(len(cum)):
        if cum[i] >= peak_v - 1e-12:
            if under:
                episodes.append((peak_t, ts[i]))
                under = False
            peak_v = max(peak_v, cum[i])
            peak_t = ts[i]
        else:
            under = True
    open_days = None
    if under and len(ts):
        open_days = (ts[len(ts) - 1] - peak_t).days
    durs = [(b - a).days for a, b in episodes]
    return pd.DataFrame([{
        "basis": "exit-ordered step equity, tie (exit_ms, asset); no per-bar "
                 "mark-to-market artifact exists in this estate [D4]",
        "max_dd_r": r4(max_dd),
        "n_underwater_episodes_closed": len(durs),
        "max_tuw_days_closed": max(durs) if durs else 0,
        "total_tuw_days_closed": int(sum(durs)),
        "open_underwater_days_at_corridor_end": open_days,
        "final_equity_r": r4(float(cum[-1])) if len(cum) else 0.0,
        "peak_equity_r": r4(float(peak[-1])) if len(peak) else 0.0,
    }])


def a1_streaks(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.5 — losing/winning streaks, exit-ordered, MEASURED (no independence
    model, no expectation — that would be estimation)."""
    d = feat.sort_values(["exit_ms", "asset"])
    w = (d["net_r"] > 0).to_numpy()
    best = {"W": 0, "L": 0}
    runs = {"W": [], "L": []}
    cur, n = None, 0
    for x in w:
        k = "W" if x else "L"
        if k == cur:
            n += 1
        else:
            if cur:
                runs[cur].append(n)
            cur, n = k, 1
    if cur:
        runs[cur].append(n)
    rows = []
    for k, label in (("L", "losing"), ("W", "winning")):
        rr = runs[k] or [0]
        rows.append({"streak": label, "max_len": int(max(rr)),
                     "n_streaks": len(runs[k]),
                     "mean_len": r4(float(np.mean(rr))) if runs[k] else 0.0})
    return pd.DataFrame(rows)


def a1_r_in_atr(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.6 — the R-in-ATR spread: the distribution of r_over_atr (initial
    risk in ATR units), overall and per asset.  The rail is 1.0 ATR, so the
    minimum states whether the rail binds."""
    outs = []
    for key, d in [("ALL", feat)] + [(a, feat[feat["asset"] == a])
                                     for a in sorted(feat["asset"].unique())]:
        v = d["r_over_atr"].astype(float)
        outs.append({
            "key": key, "n": len(v), "min": r4(v.min()),
            "p10": r4(v.quantile(0.10)), "median": r4(v.median()),
            "p90": r4(v.quantile(0.90)), "max": r4(v.max()),
            "at_rail_n": int((v <= 1.0 + 1e-9).sum()),
        })
    return pd.DataFrame(outs)


def a1_hold(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.7 — hold distribution, winners vs losers, and by exit mechanism."""
    outs = []
    for key, d in (("WINNERS", feat[feat["winner"]]),
                   ("LOSERS", feat[~feat["winner"]]),
                   ("ALL", feat)):
        v = d["bars_held"].astype(float)
        outs.append({"cut": "population", "key": key, "n": len(v),
                     "mean_bars": r4(v.mean()), "median_bars": r4(v.median()),
                     "p10_bars": r4(v.quantile(0.10)),
                     "p90_bars": r4(v.quantile(0.90)),
                     "max_bars": int(v.max()) if len(v) else 0})
    for xr, d in feat.groupby("exit_reason"):
        v = d["bars_held"].astype(float)
        outs.append({"cut": "exit mechanism", "key": xr, "n": len(v),
                     "mean_bars": r4(v.mean()), "median_bars": r4(v.median()),
                     "p10_bars": r4(v.quantile(0.10)),
                     "p90_bars": r4(v.quantile(0.90)),
                     "max_bars": int(v.max())})
    return pd.DataFrame(outs)


def a1_funding(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.8 — funding as % of gross, and fees beside it, by asset/year/book.
    Sign law: fee_r and funding_r are COSTS (net = gross − fee − funding);
    a negative funding_r is a credit."""
    outs = []
    for cut, key, d in ([("book", "ALL", feat)]
                        + [("asset", a, feat[feat["asset"] == a])
                           for a in sorted(feat["asset"].unique())]
                        + [("year", y, feat[feat["year"] == y])
                           for y in sorted(feat["year"].unique())]):
        g = d["gross_r"].sum()
        outs.append({
            "cut": cut, "key": key, "n": len(d),
            "gross_r": r4(g), "fee_r": r4(d["fee_r"].sum()),
            "funding_r": r4(d["funding_r"].sum()),
            "funding_r_uncapped": r4(d["funding_r_uncapped"].sum()),
            "funding_pct_of_gross": (r4(100.0 * d["funding_r"].sum() / abs(g))
                                     if abs(g) > 1e-9 else None),
            "fee_pct_of_gross": (r4(100.0 * d["fee_r"].sum() / abs(g))
                                 if abs(g) > 1e-9 else None),
            "funding_credit_campaigns_n": int((d["funding_r"] < 0).sum()),
        })
    return pd.DataFrame(outs)


def a1_serial(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.9 — serial correlation of consecutive outcomes, MEASURED, no
    inference (a p-value would be estimation).  Exit-ordered; the book
    interleaves five assets on one clock, so the per-asset entry-ordered
    reading is printed beside the book reading."""
    rows = []

    def one(d, key):
        v = d["net_r"].astype(float).to_numpy()
        w = (v > 0).astype(float)
        if len(v) < 3:
            return {"key": key, "n_pairs": max(len(v) - 1, 0),
                    "lag1_pearson_net_r": None, "lag1_pearson_win": None,
                    "p_win_after_win_pct": None, "p_win_after_loss_pct": None}
        r_ = float(np.corrcoef(v[:-1], v[1:])[0, 1])
        rw = float(np.corrcoef(w[:-1], w[1:])[0, 1])
        aw = w[1:][w[:-1] == 1]
        al = w[1:][w[:-1] == 0]
        return {"key": key, "n_pairs": len(v) - 1,
                "lag1_pearson_net_r": r6(r_), "lag1_pearson_win": r6(rw),
                "p_win_after_win_pct": (r4(100 * aw.mean()) if len(aw) else None),
                "p_win_after_loss_pct": (r4(100 * al.mean()) if len(al) else None)}
    rows.append({"cut": "book, exit-ordered",
                 **one(feat.sort_values(["exit_ms", "asset"]), "ALL")})
    for a in sorted(feat["asset"].unique()):
        rows.append({"cut": "asset, entry-ordered",
                     **one(feat[feat["asset"] == a]
                           .sort_values("entry_ms"), a)})
    return pd.DataFrame(rows)


def a1_mae_mfe_xtab(feat: pd.DataFrame) -> pd.DataFrame:
    """A1.10 — THE TC6-COMMISSIONED SUPPLEMENT, SUPERSET: MAE-decile ×
    MFE-decile × exit mechanism, BOTH excursion bases, winners never merged
    away — one tidy long table (basis × exit × cell), n and net R per cell."""
    outs = []
    for basis, mcol, fcol in (("held", "mae_held_r", "mfe_held_r"),
                              ("tape", "mae_tape_r", "mfe_tape_r")):
        d = feat.copy()
        d["mae_dec"] = _decile(d[mcol])
        d["mfe_dec"] = _decile(d[fcol])
        for xr, dd in [("ALL", d)] + list(d.groupby("exit_reason")):
            g = dd.groupby(["mae_dec", "mfe_dec"], dropna=False).agg(
                n=("net_r", "size"), net_r=("net_r", "sum"),
                expectancy_r=("net_r", "mean"),
                winners_n=("winner", "sum")).reset_index()
            g.insert(0, "exit_mechanism", xr)
            g.insert(0, "basis", basis)
            outs.append(g)
    out = pd.concat(outs, ignore_index=True)
    out["net_r"] = out["net_r"].astype(float).round(4)
    out["expectancy_r"] = out["expectancy_r"].astype(float).round(6)
    out["provisional"] = out["n"] < RC.PROVISIONAL_MIN_N
    return out


A1_BUILDERS = (
    ("a1_r_deciles", a1_r_deciles, ["population", "r_decile"]),
    ("a1_expectancy_pf", a1_expectancy_pf, ["basis"]),
    ("a1_win_rate", a1_win_rate, ["cut", "key"]),
    ("a1_dd_tuw", a1_dd_tuw, ["basis"]),
    ("a1_streaks", a1_streaks, ["streak"]),
    ("a1_r_in_atr", a1_r_in_atr, ["key"]),
    ("a1_hold", a1_hold, ["cut", "key"]),
    ("a1_funding", a1_funding, ["cut", "key"]),
    ("a1_serial", a1_serial, ["cut", "key"]),
    ("a1_mae_mfe_xtab", a1_mae_mfe_xtab,
     ["basis", "exit_mechanism", "mae_dec", "mfe_dec"]),
)


# ─────────────────────────── A2 · the top-10 autopsy + the separation table
SELECTION_NOTE = ("a SELECTION, not a result — the top-10 are the book's own "
                  "argmax rows; every gap in the separation table is "
                  "conditioned on having selected winners, GATES NOTHING, "
                  "and no registration rests on it")


def a2_top10(feat: pd.DataFrame) -> pd.DataFrame:
    """A2.1 — the ten best by net R, full life-cycle schema, collared."""
    d = feat.sort_values("net_r", ascending=False).head(10).copy()
    d.insert(0, "rank_by_net_r", range(1, len(d) + 1))
    d["selection_not_a_result"] = SELECTION_NOTE
    d["gates_nothing"] = True
    return d.reset_index(drop=True)


def a2_separation(feat: pd.DataFrame) -> pd.DataFrame:
    """A2.2 — THE SEPARATION TABLE: every numeric autopsy column, median of
    the top-10 vs median of the other-186, gap ranked by ROBUST z
    (gap / (1.4826·MAD of the others)) — 'where the alpha hides', as ONE
    sortable table, SELECTION-collared on every row [D5].

    WHAT WOULD MAKE THIS WRONG: ranking raw gaps (columns have incomparable
    units), or dropping the collar (a reader would read a conditioned gap as
    a tradable signal)."""
    top = feat.sort_values("net_r", ascending=False).head(10)
    rest = feat.sort_values("net_r", ascending=False).iloc[10:]
    # ROSTER HYGIENE [review L3]: timestamps and booleans are not habitat
    # features — exit_ms is an epoch, `winner` IS the selection predicate.
    drop = {"entry_ms", "exit_ms"}
    num = [c for c in feat.columns
           if pd.api.types.is_numeric_dtype(feat[c])
           and not pd.api.types.is_bool_dtype(feat[c])
           and c not in drop and not c.endswith("_decile")
           and c not in ("mae_decile", "mfe_decile", "lag_decile")]
    # THE TAUTOLOGY COLLAR, NAMED PER COLUMN [review L3]: the top-10 are the
    # argmax of net_r, so every column DERIVED from net_r by identity ranks
    # by construction — management_delta_r = net_r − net_r_entry_only chief
    # among them (pushing net_r's own gap through its MAD yields z = 22.3,
    # MORE than the observed 20.9; the genuine entry-only gap is +0.31 R).
    DERIVED = {"net_r": "the selection variable itself",
               "gross_r": "net_r before costs — the selection re-labelled",
               "management_delta_r": "net_r − net_r_entry_only BY IDENTITY; "
                                     "its z is delivered by the selection "
                                     "(mechanical z 22.3 > observed 20.9)",
               "mfe_tape_r": "the selection's own favorable excursion",
               "mfe_held_r": "the selection's own favorable excursion",
               "net_r_harvest_half": "a component of net_r",
               "net_r_runner_half": "a component of net_r",
               "peak_vs_kept_pct": "net_r / mfe — a ratio of two selection "
                                   "columns"}
    MAD_NOTE = {"net_r_entry_only": "MAD of the others is 0.020 (nearly "
                "every non-top campaign stops near −1R), so a +0.31 R "
                "median gap prints z = 10.2 — read the GAP, not the z"}
    rows = []
    for c in num:
        tv = pd.to_numeric(top[c], errors="coerce").dropna()
        rv = pd.to_numeric(rest[c], errors="coerce").dropna()
        if not len(tv) or not len(rv):
            continue
        mt, mr = float(tv.median()), float(rv.median())
        mad = float((rv - mr).abs().median())
        z = (mt - mr) / (1.4826 * mad) if mad > 1e-12 else None
        rows.append({"column": c, "median_top10": r6(mt),
                     "median_other": r6(mr), "gap": r6(mt - mr),
                     "robust_z": r4(z) if z is not None else None,
                     "abs_z": abs(r4(z)) if z is not None else None,
                     "derived_from_selection": c in DERIVED,
                     "tautology_note": DERIVED.get(c, MAD_NOTE.get(c)),
                     "n_top": len(tv), "n_other": len(rv)})
    d = pd.DataFrame(rows).sort_values("abs_z", ascending=False,
                                       na_position="last")
    d.insert(0, "rank", range(1, len(d) + 1))
    d["selection_not_a_result"] = SELECTION_NOTE
    d["gates_nothing"] = True
    # m counts columns with a COMPUTABLE z — a NaN-z row is not a comparison
    d["m_columns_compared"] = int(d["robust_z"].notna().sum())
    return d.reset_index(drop=True)


# ═══════════════ STAGE B · THE PAIR SWEEP — the grid WHOLE, no promotion
NO_PROMOTION = ("CONTEXT ONLY [D-R7 lineage]. No cell of this grid may be "
                "promoted. P-TRG-1 was named before the look and is scored "
                "whatever this table says; the other six cells decide "
                "nothing and their best number is the best number in a grid "
                "of seven.")


def _role_desc(roles: Roles) -> tuple:
    """(swapped_role, from, to) vs v6 — exactly one pair differs by
    construction of SWEEP_CELLS; HALT if not, because a two-factor cell under
    an OFAT name would poison every 'vs v6' row."""
    diffs = []
    if (roles.tide_f, roles.tide_s) != (V6_ROLES.tide_f, V6_ROLES.tide_s):
        diffs.append(("tide", f"{V6_ROLES.tide_f}/{V6_ROLES.tide_s}",
                      f"{roles.tide_f}/{roles.tide_s}"))
    if (roles.win_f, roles.win_s) != (V6_ROLES.win_f, V6_ROLES.win_s):
        diffs.append(("window", f"{V6_ROLES.win_f}/{V6_ROLES.win_s}",
                      f"{roles.win_f}/{roles.win_s}"))
    if (roles.trg_f, roles.trg_s) != (V6_ROLES.trg_f, V6_ROLES.trg_s):
        diffs.append(("trigger", f"{V6_ROLES.trg_f}/{V6_ROLES.trg_s}",
                      f"{roles.trg_f}/{roles.trg_s}"))
    if len(diffs) != 1:
        raise SystemExit(f"HALT: cell {roles.name!r} swaps {len(diffs)} "
                         f"role pairs; the sweep is OFAT.")
    return diffs[0]


def sweep_grid(base: list, cell_books: dict, card) -> pd.DataFrame:
    """THE GRID, WHOLE — seven cells, TWO-SAMPLE ruler, D15 trio + LOAO on
    every row, NO PROMOTION.  `changes` is measured, never assumed; both
    rulers are printed [estate law: the one that decides and the one that
    does not]."""
    bnet = [t.net_r for t in base]
    bcl = [t.symbol for t in base]
    bu = {(t.symbol, t.lane, t.entry_ms): t.net_r for t in base}
    rows = []
    for roles in SWEEP_CELLS:
        book = cell_books[roles.name]
        role, r_from, r_to = _role_desc(roles)
        pv, pc = [], []
        for t in book:
            k = (t.symbol, t.lane, t.entry_ms)
            if k in bu:
                pv.append(t.net_r - bu[k])
                pc.append(t.symbol)
        changes = (len(base) - len(pv)) > 0 or (len(book) - len(pv)) > 0
        if not changes:
            raise SystemExit(f"HALT: cell {roles.name!r} shares the whole "
                             f"campaign set; the commissioned two-sample "
                             f"ruler's premise failed and a paired fallback "
                             f"would be a different commission.")
        rs = [t.net_r for t in book]
        ac = [t.symbol for t in book]
        pt2 = (float(np.mean(rs)) if rs else 0.0) - float(np.mean(bnet))
        ci_2 = _ci_from(cluster_boot_diff(rs, ac, bnet, bcl), pt2)
        ci_p = _ci_from(cluster_boot(pv, pc),
                        float(np.mean(pv)) if pv else None)
        lo_ = T7.loao(book, base, roles.name, two_sample=True)
        n_before = sum(1 for t in base if t.arm_i < roles.floor_bars)
        r_before = sum(t.net_r for t in base
                       if t.arm_i < roles.floor_bars)
        row = agg(book, label="pair-sweep", key=roles.name)
        row.update({
            "cell": roles.name, "swapped_role": role,
            "swapped_from": r_from, "swapped_to": r_to,
            "floor_bars": roles.floor_bars,
            "base_armings_before_cell_floor_n": n_before,
            "base_armings_before_cell_floor_net_r": r4(r_before),
            "set_changes": bool(changes),
            "n_shared": len(pv), "n_cell_only": len(book) - len(pv),
            "n_base_only": len(base) - len(pv),
            "ruler": "TWO-SAMPLE asset-cluster (commissioned; the swap "
                     "changes the campaign set — measured on the row)",
            "two_sample_ci_point": r6(ci_2["point"]),
            "two_sample_ci_lo": r6(ci_2["lo"]),
            "two_sample_ci_hi": r6(ci_2["hi"]),
            "p_one_sided": r6(ci_2["p_one_sided"]),
            "paired_ci_point": r6(ci_p["point"]),
            "paired_ci_lo": r6(ci_p["lo"]), "paired_ci_hi": r6(ci_p["hi"]),
            "whole_book_difference_r": r4(sum(rs) - sum(bnet)),
            "is_the_registered_cell": bool(roles.name == REGISTERED_CELL),
            "promotable": False, "no_promotion": NO_PROMOTION,
            "d15_gates": "NOTHING [house law: D15 caveats not hard gates]",
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            **d15(book, base)})
        rows.append(row)
    return pd.DataFrame(rows)


def registration_text9() -> pd.DataFrame:
    return pd.DataFrame([{
        "registration": "P-TRG-1", "prior_pct": 50,
        "claim": "the 4h trigger cross 9/26 replacing 12/26 — all else card "
                 "v6, roles de-aliased so the window STAYS 12/89 [D1] — "
                 "beats card v6",
        "ruler": "TWO-SAMPLE asset-cluster — the swap CHANGES the campaign "
                 "set (measured: the two books share fewer than half their "
                 "campaigns)",
        "named_caveat": "OPERATOR-NAMED ('is 12/26 better than 9/26'), m = 1 "
                        "— the six other sweep cells are DIAGNOSTIC and take "
                        "no slot; naming one cell before the look is what "
                        "keeps the BH bar at q/m = 0.10 honest. The window "
                        "cross still reads the period-12 array; without "
                        "de-aliasing this cell would also move the window "
                        "and the claim would be two swaps wearing one name."}])


def score9(base: list, trg_book: list) -> pd.DataFrame:
    """ONE REGISTRATION, m = 1 [TC7-c law: m counts independently-failable
    hypotheses; the grid's other cells are diagnostics and take no slot]."""
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
                 "verdict": ("SUPPORTED" if (ref["lo"] or 0) > 0
                             else "NOT SUPPORTED"),
                 "loao_line": "—", "scored_in_family": False,
                 "note": "not an acceptance test; excluded from m"})
    book = trg_book
    pv, pc = [], []
    for t in book:
        k = (t.symbol, t.lane, t.entry_ms)
        if k in bu:
            pv.append(t.net_r - bu[k])
            pc.append(t.symbol)
    changes = (len(base) - len(pv)) > 0 or (len(book) - len(pv)) > 0
    if not changes:
        raise SystemExit("HALT: P-TRG-1's book shares the whole campaign "
                         "set; the commissioned two-sample ruler's premise "
                         "failed.")
    rs = [t.net_r for t in book]
    ac = [t.symbol for t in book]
    ci_p = _ci_from(cluster_boot(pv, pc), float(np.mean(pv)) if pv else None)
    pt2 = float(np.mean(rs)) - float(np.mean(bnet))
    ci_2 = _ci_from(cluster_boot_diff(rs, ac, bnet, bcl), pt2)
    ci = ci_2                       # commissioned TWO-SAMPLE; changes printed
    lo_ = T7.loao(book, base, "P-TRG-1", two_sample=True)
    good = bool(ci["lo"] is not None and ci["lo"] > 0)
    rows.append({
        "registration": "P-TRG-1", "arm": "trigger 9/26 vs card v6",
        "prior_pct": 50, "n": len(book),
        "expectancy_r": r6(float(np.mean(rs))), "net_r": r4(sum(rs)),
        "ruler": "TWO-SAMPLE (commissioned; set change measured on the row)",
        "ruler_is_two_sample": True, "set_changes_measured": bool(changes),
        "ci_point": r6(ci["point"]), "ci_lo": r6(ci["lo"]),
        "ci_hi": r6(ci["hi"]), "p_one_sided": r6(ci["p_one_sided"]),
        "verdict": "SUPPORTED" if good else "NOT SUPPORTED",
        "paired_ci_point": r6(ci_p["point"]), "paired_ci_lo": r6(ci_p["lo"]),
        "paired_ci_hi": r6(ci_p["hi"]),
        "two_sample_ci_point": r6(ci_2["point"]),
        "two_sample_ci_lo": r6(ci_2["lo"]),
        "two_sample_ci_hi": r6(ci_2["hi"]),
        "paired_n": len(pv), "unpaired_base_n_lane_keyed": len(base) - len(pv),
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
        f"m = {m}, counting INDEPENDENTLY-FAILABLE HYPOTHESES [TC7-c]. The "
        f"six unregistered sweep cells are DIAGNOSTIC (no promotion) and "
        f"take no slot. q = {FDR_Q}, bar = q/m = {bar:.5f}.")
    return d


# ═══════════════════ TC7-f · THE LABS' FRAMES, FILED, WITH PROVE-RAN DATA
def tc7f_frames(lo_ms: int, hi_ms: int, base: list) -> tuple[dict, dict]:
    """EVERY frame each TIER-C7 lab's own registry enumerates, built and
    returned for filing [TC7-f].  The commission says '17 frames'; the
    on-disk registries total 18 (chain 7 + regime 5 + stopgrid 3 + weave 3,
    counting weave's _selftest as a frame once rendered) — the discrepancy is
    STATED, not reconciled: no file on disk enumerates 17.

    The prove-ran evidence per lab is its VERIFICATION frame — chain
    `self_check`, stopgrid `selfcheck`, weave `_selftest` (rendered to one
    row per leg), regime's cardinality-asserting tables — filed non-empty
    with every row passed.  `F-C9-LABS` asserts exactly that."""
    import tierc7_lab_chain as LC
    import tierc7_lab_regime as LR
    import tierc7_lab_stopgrid as LS
    import tierc7_lab_weave as LW
    frames: dict[str, pd.DataFrame] = {}
    prove: dict[str, dict] = {}

    ch = LC.build(lo_ms, hi_ms)
    for k, v in ch.items():
        frames[f"tc7f_chain_{k}"] = v
    sc = ch["self_check"]
    # `passes` is None on DISCLOSURE rows (their `failures` is a COUNT being
    # disclosed, e.g. "chains whose D12 ceiling binds: 1 of 79") — only rows
    # where `passes` is not null are checks, and those must all hold.
    checks = sc[sc["passes"].notna()]
    prove["L-RE (chain)"] = {
        "frames_expected": len(ch), "frames_built": len(ch),
        "selfcheck_rows": len(sc), "selfcheck_check_rows": len(checks),
        "selfcheck_disclosure_rows": int(sc["passes"].isna().sum()),
        "selfcheck_all_passed": bool(
            checks["passes"].astype(bool).all()
            and (checks["failures"].astype(int) == 0).all())}

    rg = LR.all_tables(lo_ms, hi_ms)
    for k, v in rg.items():
        frames[f"tc7f_regime_{k}"] = v
    prove["L-REGIME"] = {
        "frames_expected": len(rg), "frames_built": len(rg),
        "selfcheck_rows": int(sum(len(v) for v in rg.values())),
        "selfcheck_all_passed": True,   # the lab HALTs on cardinality breach
        "note": "regime's checks are in-band SystemExit HALTs "
                "(self-paired v6 rows, bands sum to whole); reaching this "
                "line means they ran and held"}

    sg = LS.stopgrid_table(lo_ms, hi_ms, base)
    ab = LS.anchor_bakeoff(lo_ms, hi_ms, base)
    sk = LS.selfcheck()
    frames["tc7f_stopgrid_stopgrid_table"] = sg
    frames["tc7f_stopgrid_anchor_bakeoff"] = ab
    frames["tc7f_stopgrid_selfcheck"] = sk
    pcol = [c for c in ("passed", "pass", "ok") if c in sk.columns]
    prove["S-STOPGRID/L-ANCHOR"] = {
        "frames_expected": 3, "frames_built": 3,
        "selfcheck_rows": len(sk),
        "selfcheck_all_passed": bool(sk[pcol[0]].all()) if pcol else None}

    we = LW.weave_events(lo_ms, hi_ms)
    wq = LW.weave_quality(lo_ms, hi_ms)
    wc = LW.too_early_cost(lo_ms, hi_ms)
    st_ = LW._selftest(lo_ms, hi_ms)     # raises on failure [lab law]
    frames["tc7f_weave_weave_events"] = we
    frames["tc7f_weave_weave_quality"] = wq
    frames["tc7f_weave_too_early_cost"] = wc
    frames["tc7f_weave_selftest"] = pd.DataFrame(
        [{"leg": str(k), "value": str(v), "passed": True}
         for k, v in st_.items()])
    prove["L-WEAVE"] = {
        "frames_expected": 4, "frames_built": 4,
        "selfcheck_rows": len(st_),
        "selfcheck_all_passed": True,   # _selftest raises on failure
        "note": "_selftest returns a dict and RAISES on failure; a rendered "
                "row set with passed=True is the surviving evidence"}
    return frames, prove


# ══════════ TC7-g · L-REGIME RE-EMITTED WITH TRAILING BAND EDGES [D7]
def _trailing_pool(lo_ms: int, hi_ms: int) -> dict:
    """The regime lab's panel pools, WITH TIMES — so an edge can be taken on
    the prefix of bars at or before a campaign's entry (causal, inclusive:
    the register's own trailing-median precedent includes the current bar).
    """
    import tierc7_lab_regime as LR
    rl_v, rl_t, sk_v, sk_t = [], [], [], []
    for s_ in RC.UNIVERSE:
        f = frame(s_)["f"]
        a, b = T7._idx_range(f.open_ms, lo_ms, hi_ms)
        if b < a:
            continue
        idx = np.arange(len(f.c))
        inwin = (idx >= a) & (idx <= b)
        _rv, _ann, rel = LR.realized_vol(s_)
        m = inwin & np.isfinite(rel)
        rl_v.append(rel[m]); rl_t.append(f.open_ms[m])
        _st, run, _sa = LR.tide_streak(s_)
        ms_ = inwin & (run > 0)
        sk_v.append(run[ms_]); sk_t.append(f.open_ms[ms_])
    rl_v, rl_t = np.concatenate(rl_v), np.concatenate(rl_t)
    sk_v, sk_t = np.concatenate(sk_v), np.concatenate(sk_t)
    o1, o2 = np.argsort(rl_t, kind="mergesort"), np.argsort(sk_t,
                                                            kind="mergesort")
    return {"rl_v": rl_v[o1], "rl_t": rl_t[o1],
            "sk_v": sk_v[o2], "sk_t": sk_t[o2]}


def _trailing_edges(pool: dict, at_ms: int) -> dict:
    """Edges from the pooled prefix open_ms <= at_ms.  None while the prefix
    is empty (a campaign this early is 'unbanded (trailing warm-up)')."""
    import tierc7_lab_regime as LR
    i1 = int(np.searchsorted(pool["rl_t"], at_ms, side="right"))
    i2 = int(np.searchsorted(pool["sk_t"], at_ms, side="right"))
    v = (list(np.quantile(pool["rl_v"][:i1], LR.VOL_TERCILE_QUANTILES))
         if i1 >= RC.PROVISIONAL_MIN_N else None)
    s_ = (list(np.quantile(pool["sk_v"][:i2], LR.STREAK_BAND_QUANTILES))
          if i2 >= RC.PROVISIONAL_MIN_N else None)
    return {"vol_rel": v, "streak_bar": s_}


def tc7g_tables(lo_ms: int, hi_ms: int) -> tuple[dict, dict]:
    """THE RE-EMISSION [TC7-g]: the lab's campaign-banded tables —
    lregime_cross and lregime_candidates — re-run through the lab's OWN
    machinery with `_tag_book` surgically replaced by a TRAILING tagger:
    each campaign banded by expanding panel-pooled quantile edges over bars
    at or before its OWN entry.  The lab's cardinality HALTs (self-paired
    v6 rows, bands sum to whole) run unmodified and still bind.

    The two BAR-DISTRIBUTION tables (vol_terciles, tide_streak_bands)
    describe the corridor's pooled distribution and are not campaign-banded;
    the look-ahead critique does not touch them, so they re-emit unchanged
    beside an EDGE-EVOLUTION table that quantifies how far the trailing
    edges sit from the whole-corridor ones at each year boundary — the
    measured size of the look-ahead this fix removes."""
    import tierc7_lab_regime as LR
    pool = _trailing_pool(lo_ms, hi_ms)
    cu_fixed = LR.cuts(lo_ms, hi_ms)

    def _tag_trailing(bk, cu):
        rows = []
        for t in bk:
            _rv, ann, rel = LR.realized_vol(t.symbol)
            state, run, start = LR.tide_streak(t.symbol)
            i = int(t.entry_i)
            f = frame(t.symbol)["f"]
            ed = _trailing_edges(pool, int(f.open_ms[i]))
            v = float(rel[i]) if np.isfinite(rel[i]) else None
            vb = (LR._vol_band(v, ed["vol_rel"])
                  if ed["vol_rel"] is not None else None)
            sb = (LR._streak_band(int(run[i]), ed["streak_bar"])
                  if ed["streak_bar"] is not None else None)
            # the lab's no-null-streak HALT survives the patch [review L5]:
            # with warm edges a campaign must band (WARMUP_BARS == the tide
            # warm floor); only a cold PREFIX may leave it unbanded, and
            # that gets its own label rather than the lab's rv one.
            if sb is None and ed["streak_bar"] is not None:
                raise SystemExit("HALT: a campaign has no tide streak band "
                                 "under warm trailing edges — the floors "
                                 "have diverged.")
            rows.append({
                "symbol": t.symbol, "lane": t.lane,
                "entry_ms": int(t.entry_ms), "entry_iso": iso(t.entry_ms),
                "direction": int(t.direction), "net_r": float(t.net_r),
                "n_reentries": int(getattr(t, "n_reentries", 0)),
                "rv_rel": r6(v),
                "rv_ann_pct": (r4(float(ann[i]))
                               if np.isfinite(ann[i]) else None),
                "vol_band": vb,
                "vol_band_label": (LR.VOL_LABELS[vb] if vb is not None
                                   else ("unbanded (trailing warm-up)"
                                         if ed["vol_rel"] is None
                                         else LR.VOL_UNBANDED)),
                "streak_bars": int(run[i]), "streak_band": sb,
                "streak_band_label": (LR.STREAK_LABELS[sb]
                                      if sb is not None else "—"),
                "tide_state": int(state[i]),
                "left_censored": bool(int(start[i])
                                      == int(LR.TIDE_WARM_BARS)),
            })
        d = pd.DataFrame(rows)
        if len(d):
            off = int((d["tide_state"] != d["direction"]).sum())
            if off:
                raise SystemExit(f"HALT: {off} campaigns against the tide "
                                 f"under the trailing tagger.")
        return d

    old_tag = LR._tag_book
    LR._tag_book = _tag_trailing
    try:
        cross = LR.regime_table(lo_ms, hi_ms)
        cands = LR.candidates(lo_ms, hi_ms)
    finally:
        LR._tag_book = old_tag
    for d in (cross, cands):
        d["banding"] = ("TRAILING expanding panel quantiles, causal "
                        "inclusive [TC7-g]; edges as of each campaign's own "
                        "entry bar")
    # the measured look-ahead: trailing vs whole-corridor edges at year ends
    ev = []
    for y in range(2020, 2027):
        at = _ms(f"{y}-01-01")
        ed = _trailing_edges(pool, at)
        ev.append({"as_of": f"{y}-01-01",
                   "vol_rel_edges_trailing": (
                       [r6(x) for x in ed["vol_rel"]]
                       if ed["vol_rel"] else None),
                   "streak_edges_trailing": (
                       [r4(x) for x in ed["streak_bar"]]
                       if ed["streak_bar"] else None),
                   "vol_rel_edges_whole_corridor": [
                       r6(x) for x in cu_fixed["vol_rel"]],
                   "streak_edges_whole_corridor": [
                       r4(x) for x in cu_fixed["streak_bar"]]})
    edges = pd.DataFrame(ev)
    reg = pd.DataFrame([{
        "key": "TC7-g",
        "what": "L-REGIME campaign banding re-emitted with TRAILING edges",
        "method": "expanding panel-pooled quantiles over bars with open_ms "
                  "<= the campaign's entry bar, inclusive (the register's "
                  "own trailing-median precedent); n>=30 prefix floor, "
                  "else 'unbanded (trailing warm-up)'",
        "replaces": "whole-corridor quantiles — look-ahead of the kind the "
                    "register rejects by name [BUILD_2026-08-17 §A row 28]",
        "bar_distribution_tables": "vol_terciles / tide_streak_bands "
                                   "describe the pooled corridor and are "
                                   "not campaign-banded; re-emitted "
                                   "unchanged beside the edge-evolution "
                                   "table",
    }])
    frames = {"tc7g_regime_cross_trailing": cross,
              "tc7g_regime_candidates_trailing": cands,
              "tc7g_edge_evolution": edges,
              "tc7g_register": reg,
              "tc7g_vol_terciles": LR.vol_terciles(lo_ms, hi_ms),
              "tc7g_tide_streak_bands": LR.tide_streak_bands(lo_ms, hi_ms)}
    meta_ = {"method": "trailing expanding panel quantiles (causal, "
                       "inclusive), prefix floor n>=30",
             "tables": sorted(frames)}
    return frames, meta_


# ═══════════════════════════════════════════════════════════ THE BUILD
def run(root: Path) -> dict:
    t0 = time.time()
    root.mkdir(parents=True, exist_ok=True)
    lo, hi, cmeta = corridor()
    global AS_OF
    AS_OF = cmeta["last_closed_4h_close"]
    log(f"TIER-C9 · corridor {cmeta['panel_start']} → {AS_OF} "
        f"({cmeta['span_days']}d)")
    card = T8.Card(name="v6-control")

    # ═══ F-CTRL PRECONDITION — BEFORE ANYTHING [commissioned order].
    # The de-aliased role pipeline at v6 periods must BE card v6, exactly.
    base = run_cell9(card, V6_ROLES, lo, hi)
    want = T6.run_cell(V6.CARD_V6, lo, hi)
    gj = journal_frame(base).sort_values(["asset", "entry_ms"]).reset_index(drop=True)
    wj = journal_frame(want).sort_values(["asset", "entry_ms"]).reset_index(drop=True)
    ctrl_cols = ["entry_ms", "exit_ms", "entry_px", "exit_px", "stop_px",
                 "r_dist", "net_r", "gross_r", "fee_r", "funding_r", "mfe_r",
                 "n_advances"]
    if len(gj) != len(wj):
        raise SystemExit(f"HALT: F-CTRL precondition — {len(gj)} vs "
                         f"{len(wj)} campaigns. Nothing downstream runs.")
    worst = max(float(np.max(np.abs(gj[c].to_numpy(dtype=float)
                                    - wj[c].to_numpy(dtype=float))))
                for c in ctrl_cols)
    if worst != 0.0 or list(gj["exit_reason"]) != list(wj["exit_reason"]):
        raise SystemExit(f"HALT: F-CTRL precondition — worst abs diff "
                         f"{worst:.3e} != 0.000e+00. Nothing downstream runs.")
    log(f"  F-CTRL precondition: n={len(base)} worst=0.000e+00  [HELD]")

    W: dict[str, str] = {}
    K: dict[str, list] = {}
    SK: list[str] = []

    def put(df: pd.DataFrame, name: str, key: list):
        if df is None or not len(df):
            SK.append(name)
            log(f"    (skipped empty: {name})")
            return
        d = df.copy()
        if "as_of_last_closed_4h" not in d.columns:
            d = stamp(d, cmeta)
        d.attrs = {}
        d.columns = [str(c) for c in d.columns]
        W[name] = write_table(d, name, key, root)
        K[name] = key

    # ═══ STAGE A — the ledger tables, display-only, zero estimation
    log("  STAGE A · the ledger tables")
    feat = features9(base, card, lo, hi)
    put(gj, "trade_journal_control", ["asset", "entry_ms"])
    fx = feat.merge(gj[["asset", "entry_ms", "exit_ms", "exit_ts"]],
                    on=["asset", "entry_ms"], how="left")
    put(fx, "a2_campaign_features", ["asset", "entry_ms"])
    for name, fn, key in A1_BUILDERS:
        put(fn(fx), name, key)
    put(a2_top10(fx), "a2_top10_autopsy", ["rank_by_net_r"])
    put(a2_separation(fx), "a2_separation", ["column"])
    put(headline_v6(base, "TIER-C9 control (== card v6)", lo, hi),
        "headline", ["group", "key", "aggregation"])

    # ═══ STAGE B — the pair sweep + P-TRG-1
    log("  STAGE B · the pair sweep (7 cells, OFAT, two-sample)")
    cell_books = {}
    for roles in SWEEP_CELLS:
        cell_books[roles.name] = run_cell9(card, roles, lo, hi)
        b = cell_books[roles.name]
        log(f"    {roles.name:<14} n={len(b):3d} net={sum(t.net_r for t in b):+9.4f}")
    put(sweep_grid(base, cell_books, card), "sweep_grid", ["cell"])
    put(registration_text9(), "registration_text", ["registration"])
    put(score9(base, cell_books[REGISTERED_CELL]), "registrations",
        ["registration", "arm"])
    put(journal_frame(cell_books[REGISTERED_CELL]),
        "trade_journal_p_trg_1", ["asset", "entry_ms"])

    # ═══ TC7-f — the labs' frames, filed, prove-ran
    log("  TC7-f · filing every lab frame")
    fr7, prove7 = tc7f_frames(lo, hi, base)
    for name, df in sorted(fr7.items()):
        d = df.copy() if df is not None else df
        if d is not None and len(d):
            d.insert(0, "row_id", range(len(d)))
        put(d, name, ["row_id"])

    # ═══ TC7-g — L-REGIME re-emitted, trailing edges
    log("  TC7-g · L-REGIME trailing re-emission")
    fr7g, meta7g = tc7g_tables(lo, hi)
    for name, df in sorted(fr7g.items()):
        d = df.copy() if df is not None else df
        if d is not None and len(d):
            d.insert(0, "row_id", range(len(d)))
        put(d, name, ["row_id"])

    # ═══ THE MANIFEST
    man = {
        "seed": SEED, "stage": "TIER-C9",
        "as_of": AS_OF,
        "corridor": {k: v for k, v in cmeta.items()
                     if k not in ("wall_clock_at_run", "cache_lag_hours")},
        "corridor_warranty": "every table carries as-of columns [TC6V-a]",
        "cache_drift_note": (
            "TIER-C8 filed AS-OF 2026-08-17T16:00Z, book n=196 net +39.7819; "
            "this corridor runs to " + str(AS_OF) + " on the same cache "
            "convention (not snapshotted [TC6V-b]). The tc8 corridor_end "
            "campaign has since resolved as a stop; no new campaigns "
            "entered. F-CTRL is live-vs-live and certifies THIS corridor."),
        "reframe_of_record": (
            "business concentration = the model; the D15 guard polices "
            "CLAIMS only [operator, ratified 2026-08-18; lineage: "
            "'D15 caveats not hard gates' (THE_RULING), TC8-e]"),
        "registration": {
            "P-TRG-1": {"prior_pct": 50, "m": 1,
                        "cell": REGISTERED_CELL,
                        "ruler": "two-sample (commissioned)"}},
        "role_semantics": (
            "D1: six de-aliased role arrays; window owns displacement; tide "
            "owns harvest band + warm-up re-point; bells split by role; "
            "under v6 periods arrays are bit-identical to e12/e26/e89/e316"),
        "bootstrap_seed_note": (
            "cluster_boot/cluster_boot_diff run on tierc5.SEED=20260816 "
            "(estate convention since TIER-C5; this module's SEED stamps "
            "the manifest, as in TIER-C7/C8)"),
        "counts": {
            "control_n": len(base),
            "control_net_r": r4(sum(t.net_r for t in base)),
            **{f"cell_{r_.name}_n": len(cell_books[r_.name])
               for r_ in SWEEP_CELLS},
            **{f"cell_{r_.name}_net_r": r4(sum(t.net_r
                                               for t in cell_books[r_.name]))
               for r_ in SWEEP_CELLS}},
        "a1_table_count": len(A1_BUILDERS),
        "tc7f": prove7,
        "tc7f_count_note": (
            "the commission says '17 frames'; the on-disk registries name "
            "18 (chain 7 + regime 5 + stopgrid 3 + weave 3), and 19 frames "
            "are FILED — the weave _selftest, a dict in the lab, rendered "
            "as the 19th. Stated, not reconciled — no file on disk "
            "enumerates 17."),
        "tc7g": meta7g,
        "labs": {k: "BUILT" for k in prove7},
        "labs_missing": [],
        "sha": W, "keys": K, "skipped_empty": SK,
        "elapsed_s": round(time.time() - t0, 1),
    }
    (root / "build_manifest.json").write_text(
        json.dumps(man, indent=2, sort_keys=True, default=str))
    log(f"  manifest → {root / 'build_manifest.json'}  ({man['elapsed_s']}s)")
    return man


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--rerun", action="store_true")
    a = ap.parse_args()
    run(OUT_RERUN if a.rerun else OUT)
