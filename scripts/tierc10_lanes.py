#!/usr/bin/env python
"""TIER-C10 · THE 4h LANE MECHANICS — P-BE-1 (BREAKEVEN) and P-SPR-2 (SPRING).

RATIFIED operator 2026-09-21 (TIER-C10; Q1-Q5 on lean, Q7 = CENSUS-R as Stage
0).  Drafted APOLLO, executed under the same charter; seed 20260921.  This
module holds the two 4h lane MECHANISMS the contract's Stage B registers, and
nothing else: it files no registration, rides no registered book, and prints
no P-* number.  TEXT BEFORE RESULT is enforced at the door (`run_lane`), not
promised in a docstring.

WHY A TC10 RIDE AT ALL [A].  `tierc9.replay9` declares its scope and HALTs on
every knob it does not read — which is the right law, and which is exactly
why a BREAKEVEN FLOOR cannot ride through it: a knob `replay9` has never
heard of would either HALT or, worse, drop silently under a cell's name.
`scripts/tierc9.py` may not be edited (it carries the estate's filed TC9
book).  So `_ride_leg10` is derived from `tierc9._ride_leg9` — itself
`tierc8._ride_leg`, itself `tierc6._ride` — with the within-bar order
unchanged and ONE new branch, and `F-LANES-OFF` is what makes the derivation
checkable rather than asserted: with every new knob OFF the whole CLASSIC5
control book must come back 0.000e+00 identical to `tierc10_panel`'s control,
campaign for campaign, column for column.  That control is the ONLY real-data
book this module rides (LAW 4).

THE WITHIN-BAR ORDER IS THE CARD'S, UNCHANGED:  STOP -> BELL -> HARVEST ->
TRAIL, adverse-first throughout, with the +1R latch taken at the TOP of the
bar BEFORE the stop test (`tierc9.py:270-283` — `mae_to_1r` deliberately
counts the +1R bar's adverse extreme as "before").  The breakeven floor is a
STOP, so it enters that order in the stop slot and nowhere else.

P-BE-1 · THE BREAKEVEN FLOOR [B].  `Card.be_floor_after_r` (default None =
OFF).  Once the campaign's favourable excursion FIRST prints the threshold in
R, the stop is floored at the entry price.  On the LATCH BAR the answer is
not a 4h question at all — a 4h bar that both printed +1R and dipped back to
entry is two different campaigns depending on the ORDER — so the latch bar is
SEQUENCED by walking its 48 native 5m children in tape order:
    dip-to-entry BEFORE the +1R print   -> the OLD stop stands for that bar;
    +1R print THEN dip-to-entry         -> BE exit AT ENTRY inside the bar;
    both inside ONE 5m child            -> adverse-first, and COUNTED;
    the +1R print and NO dip at all     -> the OLD stop stands TOO, and the
                                           parent's stop test runs on it.
The last line is not decoration: once the ratchet has carried the stop ABOVE
entry, a latch bar can pierce that stop without ever reaching entry, and a
branch that tested only "dip_first / tie / mismatch" left that bar with NO
stop decision [review 2026-09-21, BLOCKING; `be_latch_decision`].
From bar j+1 the floor is an ordinary stop: `stop = max(floor, ratchet)` for
a long (min for a short), monotone, so the ratchet may pass the floor but
never fall back through it.

THE TRAP, NAMED AND COUNTED [map_critic §4.10 x data §4.1(b)].  Native 4h
bars and 5m aggregates DISAGREE on incident bars (BTC: 4 of 15,419 4h bars;
2024-10-28T20:00Z native low 69480.3 vs aggregated 69389.0).  A 4h bar can
therefore say "+1R touched" or "dipped to entry" when no 5m child does, or
the reverse.  `be_sequence` DETECTS that — the children must number 48, sit
on the 5m grid inside the bar, and reproduce the 4h bar's high AND low — and
on a mismatch it COUNTS the bar and falls back to adverse-first.  It never
silently picks a side.

P-SPR-2 · THE SPRING / UPTHRUST LANE [C, OPERATOR RULING R3].  The runner
takes a PRECOMPUTED SIGNAL LIST as an argument.  The decision path imports no
range code at all: `replay10` reads `direction / sweep_i / sweep_ms /
sweep_extreme / swept_level / reclaim_i / bars_to_reclaim` off objects that
are `tierc5_rules.Spring`-shaped and verifies their SHAPE against the raw
tape (`check_signals`).  The list is built by a separate harness function
(`spring_signals_from_census`) which is the only thing here that imports the
census, and it imports it LAZILY, inside the function body, so the module's
own import closure stays range-free [F-LANES-CLOSURE].

  signal law (R3):  macro `harden` at the FROZEN pins (SCALE 3.0,
  DEV_RETURN_BARS 7 — the P-RNG slate's K=4 is SUPERSEDED by the frozen pin
  and the registration text must say 7).  bottom-side harden -> LONG spring;
  top-side harden -> SHORT upthrust.  `sweep_i` = the same-side breach-open
  that the harden closes; `sweep_extreme` = the raw tape's extreme over
  [sweep_i, reclaim_i] (never the 2-dp event field); `swept_level` = the
  AS-OF boundary at the breach bar; `reclaim_i` = the harden bar and
  `known_at` = that same bar, so the earliest legal entry is that bar's
  CLOSE.  Stop = `tierc5_rules.spring_stop` on the sweep extreme, railed.

THE GATE [D].  Every runner in this file calls `tierc10_panel.require_arm`
BEFORE one real bar is replayed or one frame built — `run_lane` does it as
its first statement, above every other check — and then the FILED ERA is
checked at the same door, so an arm filed for the holdout era cannot read a
tuning-era bar and be refused afterwards.  With no registration filed it
HALTs, and `F-LANES-GATE` proves it.  The one book that rides unfiled is the
KNOWN CONTROL (card v6, every knob at its default, every new knob OFF, roles
v6, a non-empty subset of CLASSIC5) — the contract's own exception.

`replay10` ITSELF IS UNGATED, BY DESIGN — the door is `run_lane`, exactly as
`tierc9.replay9`'s door is `run_cell_n`.  Called directly it rides, and no
code in this file can stop it; what stops it is that STAGE B's driver must
show `require_arm(` above every replay, and a reviewer greps for that.  Said
here so nobody mistakes the gate for a property of the replay.

LAW 4, IN THIS FILE.  Nothing here computes a P-GEN-1 / P-SPR-2 / P-BE-1 /
P-TRG-2 / P-BRK-S1 / P-BRK-I1 number.  `main()` prints the lane spec and
files nothing.  The fixtures ride synthetic tapes and the known control only.

Run:  NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
      ~/venvs/naiad/bin/python scripts/tierc10_lanes.py
"""
from __future__ import annotations

import dataclasses
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc10_panel as TP                                           # noqa: E402
import tierc10_data as D                                            # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
import tierc5 as T5                                                  # noqa: E402

# Read through TIERC9/TIERC5, not through the panel module: those two are
# FROZEN lineage files, and a helper taken from a module still under repair
# is a dependency on a moving target.
iso, _ms = T9.iso, T9._ms
MS_4H, MS_1D = T5.MS_4H, T5.MS_1D
MS_5M = 300_000
N_5M_PER_4H = MS_4H // MS_5M            # 48 — an identity, not a pin

SEED = TP.SEED                          # 20260921, by OBJECT
FROZEN_SCALE = 3.0                      # [LEAN-HEPHAESTUS L2] registered lanes
OUT = TP.OUT / "lanes"
LEAN_TAG = TP.LEAN_TAG

# ─────────────────────────────────────────── the leans this module rides on
LEANS = {
    "L2-scale": ("registered lanes and Stage-A stamps use the FROZEN "
                 "SCALE_MULT 3.0; the census prints the calibrated scale "
                 "beside, report-only"),
    "L-be-mfe": ("on a BE exit the campaign's MFE is advanced to the "
                 "favourable extreme of the 5m children up to and including "
                 "the child that filled the floor — the lineage's HELD law "
                 "(`tierc9.excursions9`: after the exit the tape is tape), "
                 "applied at 5m because that is the resolution the exit was "
                 "decided at"),
    "L-be-reason": ("the latch bar's BE fill is labelled `be_floor`; from "
                    "bar j+1 the floor is an ORDINARY stop and its exits are "
                    "labelled `stop`, with `be_bound_at_exit` printed beside "
                    "— the contract's own words, 'from bar j+1 the floor is "
                    "an ordinary stop'"),
    "L-spr-floor": ("the spring lane's warm-up floor is `roles.floor_bars` "
                    "(316 under v6) — the same floor the card lane rides, so "
                    "a standalone-vs-card comparison is over one window"),
}


# ═══════════════════════════════════════════════ THE CARD, TC10 · ONE KNOB
NEW_KNOBS = ("be_floor_after_r",)
_KNOB_OFF = {"be_floor_after_r": None}


@dataclass(frozen=True)
class Card(T8.Card):
    """v8's card, ONE field wider — and it defaults to the incumbent.

    `Card()` with no arguments is card v6, exactly as `T8.Card()` is and
    `RC.Card()` before it.  That is what makes `F-LANES-OFF` a control: this
    whole code path must reproduce the panel module's card-v6 book at
    0.000e+00 before any arm is scored.

    `be_floor_after_r` is the R threshold at which the stop is floored at
    entry.  None = OFF.  P-BE-1 registers 1.0.
    """

    name: str = "tc10-default(=v6)"
    be_floor_after_r: float | None = None


CARD_TC10_CONTROL = Card(name="tc10-control(=v6)")
CARD_BE1 = Card(name="tc10-be-floor-1R", be_floor_after_r=1.0)
CARD_SPR2 = Card(name="tc10-spring-standalone", lane="spring")

LANES = ("card", "spring", "union")
BE_REASON = "be_floor"


def knobs_off(card) -> bool:
    """True iff every knob this module ADDS is at its OFF default."""
    return all(getattr(card, k, _KNOB_OFF[k]) == _KNOB_OFF[k]
               for k in NEW_KNOBS)


# ═══════════════════════════════════════ THE 5m CHILDREN — AS-OF, MEMOISED
_FIVE: dict[str, tuple] = {}


def five_from_stage_d(sym: str) -> tuple:
    """(open_ms, high, low, close) of the asset's native 5m tape, CLOSED at
    Stage D's write-once as-of.

    `tierc10_data.load_asof` is used and NOT `tierc2_baseline.load_klines`:
    the 5m parquet files hold rows PAST the pin (Stage D's manifest counts
    them and its warranty says they are never read), and a sequencer that
    read one would be reading a bar stamped after the campaign it judges.

    WHAT WOULD MAKE THIS WRONG: storing this tape in the lineage's
    bare-symbol frame memo (the poisoned-memo hazard `tierc10_panel.frame_n`
    exists to catch), or reading the live cache instead of the snapshot.
    """
    if sym in _FIVE:
        return _FIVE[sym]
    df = D.load_asof(sym, "5m")
    t = (df["open_time"].to_numpy(np.int64), df["high"].to_numpy(float),
         df["low"].to_numpy(float), df["close"].to_numpy(float))
    _FIVE[sym] = t
    return t


# THE HOOK A FIXTURE REPLACES.  A synthetic tape pair is the only way to give
# the sequencer a KNOWN answer, and a synthetic tape must never enter the
# lineage's memos.  Replacing this name is a deliberate, greppable act.
_FIVE_SOURCE = five_from_stage_d


def children_5m(sym: str, bar_open_ms: int) -> tuple:
    """The 5m bars whose OPEN falls inside one 4h bar, in TAPE ORDER."""
    t0, h5, l5, c5 = _FIVE_SOURCE(sym)
    a = int(np.searchsorted(t0, bar_open_ms, "left"))
    b = int(np.searchsorted(t0, bar_open_ms + MS_4H, "left"))
    return t0[a:b], h5[a:b], l5[a:b], c5[a:b]


# The children must REPRODUCE the parent bar's extremes.  The comparison is
# EXACT up to a float-representation tolerance: both numbers are parsed from
# the venue's own decimal strings, so a genuine agreement is bit-equal.  1e-9
# relative is nine orders of magnitude below the measured disagreement on the
# known incident bar (BTC 2024-10-28T20:00Z: 69480.3 vs 69389.0 = 1.3e-3
# relative).  It is a REPRESENTATION tolerance, never a tuned bound.
REPR_TOL = 1e-9


def _same_px(a: float, b: float) -> bool:
    return bool(abs(float(a) - float(b))
                <= REPR_TOL * max(1.0, abs(float(a)), abs(float(b))))


def apply_floor(stop: float, floor_px: float, d: int) -> float:
    """`stop = max(floor, ratchet)` for a long, `min` for a short.

    THE FLOOR MAY RAISE THE STOP AND MAY NEVER LOWER IT.  Once the ratchet has
    carried the stop past entry the floor is spent, and a floor written as a
    plain assignment (`stop = entry_px`) would UNDO the ratchet — which is why
    this is one named function the fixture can plant a wrong into, rather than
    two characters buried in a loop [F-BE-MONO]."""
    return (max(float(stop), float(floor_px)) if d == 1
            else min(float(stop), float(floor_px)))


def be_sequence(sym: str, bar_open_ms: int, d: int, entry_px: float,
                trigger_px: float, bar_hi: float, bar_lo: float) -> dict:
    """WHICH CAME FIRST INSIDE THE 4h BAR — the +1R print, or the dip back to
    entry.  Answered on the bar's own 5m children, in tape order.

    Returns `order` in {plus1r_first, dip_first, tie, mismatch}, the two child
    indices, whether each event happened at all, the count of children, and
    `mfe_held` — the favourable extreme up to and including the child that
    filled the floor [LEAN L-be-mfe].

    THE MISMATCH LEG IS THE POINT.  `mismatch` is returned when the children
    do not number 48, do not sit on the 5m grid inside the bar, or do not
    reproduce the parent's high AND low — and ALSO when the children's own
    answer to "did it dip / did it print" disagrees with the parent bar's.
    A mismatch is COUNTED and falls back to adverse-first.  It is never
    silently resolved in either direction.

    THAT LAST CLAUSE IS DEFENSIVE, NOT LIVE MACHINERY [review 2026-09-21].
    Once the extremes are proven equal to a REPRESENTATION tolerance, child
    and parent answer "did it print / did it dip" with the SAME float
    comparison against the SAME extreme, so they can only disagree inside the
    1e-9 `REPR_TOL` window.  It is kept because a later edit to `_same_px`
    would widen that window silently, and it is named here so no reader
    mistakes it for the incident-bar detector — that is the extreme check
    three lines above it.

    WHAT WOULD MAKE THIS WRONG: reading the children out of tape order;
    comparing the parent's extremes against a rounded aggregate; resolving a
    tie in the FAVOURABLE direction (that would pay the campaign for an
    ordering the tape does not record); or treating an absent 5m file as
    "no dip" rather than as a mismatch.
    """
    t5, h5, l5, c5 = children_5m(sym, bar_open_ms)
    n5 = int(len(t5))
    # the parent's own answers, in the ride's own arithmetic
    fav4 = float(bar_hi) if d == 1 else float(bar_lo)
    adv4 = float(bar_lo) if d == 1 else float(bar_hi)
    up4 = bool((fav4 - entry_px) * d >= (trigger_px - entry_px) * d)
    dip4 = bool((adv4 - entry_px) * d <= 0.0)

    why = ""
    if n5 != N_5M_PER_4H:
        why = f"{n5} 5m children, expected {N_5M_PER_4H}"
    elif int(t5[0]) != int(bar_open_ms) \
            or int(t5[-1]) != int(bar_open_ms) + MS_4H - MS_5M \
            or not np.array_equal(np.diff(t5), np.full(n5 - 1, MS_5M,
                                                       dtype=np.int64)):
        why = "the children are not the 5m grid inside the parent bar"
    elif not _same_px(float(h5.max()), float(bar_hi)):
        why = (f"4h high {float(bar_hi):.8g} not reproduced by its 5m "
               f"children (max {float(h5.max()):.8g})")
    elif not _same_px(float(l5.min()), float(bar_lo)):
        why = (f"4h low {float(bar_lo):.8g} not reproduced by its 5m "
               f"children (min {float(l5.min()):.8g})")

    fav5 = h5 if d == 1 else l5
    adv5 = l5 if d == 1 else h5
    up_hits = np.flatnonzero((fav5 - entry_px) * d
                             >= (trigger_px - entry_px) * d)
    dip_hits = np.flatnonzero((adv5 - entry_px) * d <= 0.0)
    i_up = int(up_hits[0]) if up_hits.size else None
    i_dip = int(dip_hits[0]) if dip_hits.size else None

    if not why and (bool(i_up is not None) != up4
                    or bool(i_dip is not None) != dip4):
        why = (f"the children disagree with the parent: print "
               f"{bool(i_up is not None)} vs {up4}, dip "
               f"{bool(i_dip is not None)} vs {dip4}")

    if why:
        order = "mismatch"
    elif i_up is None:
        # the ride only calls this on the bar the LATCH printed; the parent
        # says it printed, the children agree, so this branch is unreachable
        # unless the two checks above are removed.  Named, not assumed.
        order = "mismatch"
        why = "no 5m child reached the latch threshold"
    elif i_dip is None:
        order = "plus1r_first"
    elif i_dip < i_up:
        order = "dip_first"
    elif i_up < i_dip:
        order = "plus1r_first"
    else:
        order = "tie"

    if i_dip is not None and not why:
        held = fav5[:i_dip + 1]
    else:
        held = fav5
    mfe_held = (float(held.max()) if d == 1 else float(held.min())) \
        if len(held) else float("nan")

    return {"order": order, "i_up": i_up, "i_dip": i_dip,
            "print": bool(i_up is not None), "dip": bool(i_dip is not None),
            "n_children": n5, "mismatch": bool(order == "mismatch"),
            "why": why, "mfe_held": mfe_held,
            "parent_print": up4, "parent_dip": dip4}


# ══════════════════════════════════ THE LATCH BAR'S STOP SLOT — TOTAL, NAMED
BE_LATCH_FILL, BE_LATCH_OLD_STOP = "fill", "old_stop"
BE_LATCH_DECISIONS = (BE_LATCH_FILL, BE_LATCH_OLD_STOP)


def be_latch_decision(seq: dict) -> str:
    """WHAT THE LATCH BAR'S 5m WALK DECIDES — and it decides one of TWO
    things, so the latch bar always gets a stop decision.

      `fill`      the +1R print came FIRST and a dip to entry followed inside
                  the same 4h bar: the floor fills AT ENTRY inside the bar.
      `old_stop`  EVERYTHING ELSE — `dip_first`, `tie`, `mismatch`, AND a
                  `plus1r_first` that never dipped at all: the OLD stop
                  stands for that bar and the parent's own stop test decides
                  it, unchanged.

    THE SECOND CLAUSE IS THE ONE A REVIEWER FOUND MISSING [review 2026-09-21,
    BLOCKING].  The branch was written as two POSITIVE tests — `order ==
    plus1r_first and dip` for the fill, `order != plus1r_first` for the
    parent's test — and `plus1r_first` with NO dip satisfies neither, so that
    bar got no stop test at all.  Where the stop still sits BELOW entry that
    is invisible (a low at or below the stop is necessarily a dip to entry,
    which routes to the fill branch), but once the ratchet has carried the
    stop ABOVE entry the bar can pierce the stop without ever reaching entry:
    on a synthetic tape at `be_floor_after_r=2.0` the floor-OFF ride exits
    (369, 'stop') at +0.4122 R and the floor-ON ride rode straight through
    the breached stop to (372, 'corridor_end') at +1.2000 R.  It was NOT
    reachable at the registered pin (1.0 == v6's `trail_arm_after_r`, so no
    advance can precede the latch), but nothing in the module enforced that
    coincidence, and a sensitivity run above 1.0 R would have mis-ridden.

    The function exists so the decision is ONE named thing a fixture can
    plant a wrong into, and so `_ride_leg10` can HALT on a decision it does
    not know rather than fall through the stop slot in silence.

    WHAT WOULD MAKE THIS WRONG: calling a `plus1r_first` with no dip a fill
    (the floor would pay a campaign that never came back to entry); or
    returning a third value, which the ride refuses.
    """
    return (BE_LATCH_FILL if (seq["order"] == "plus1r_first" and seq["dip"])
            else BE_LATCH_OLD_STOP)


# ═══════════════════════════════════════════════════ THE RIDE, TC10 · ONE LEG
def _ride_leg10(sym, card, roles, d, ti, entry_px, stop0, r_dist, hi_i):
    """`tierc9._ride_leg9`, with ONE new branch: the breakeven floor.

    Everything else is the parent's, line for line — the harvest arming and
    band edges off the TIDE arrays, the bells off the WINDOW and TIDE arrays
    labelled with the live periods, `matched_step` on the (2,2) pivot clock,
    the +1R latch at the top of the bar before the stop test, the within-bar
    order STOP -> BELL -> HARVEST -> TRAIL.  With `be_floor_after_r=None` the
    new branch is dead code and the leg IS `_ride_leg9` (F-LANES-OFF).

    THE NEW BRANCH, EXACTLY:
      · the BE latch is its own latch at `card.be_floor_after_r`, taken at the
        top of the bar like the diagnostic +1R latch and never reusing it —
        the threshold is a knob and the diagnostic is hardwired at 1.0;
      · on the LATCH BAR the 5m sequencer decides, and it decides in the STOP
        slot, TOTALLY: `be_latch_decision` maps every sequencer answer onto
        `fill` (BE fill at entry, inside the bar) or `old_stop` (the OLD stop
        stands and the parent's stop test runs unchanged), and a decision
        this leg does not know HALTs rather than skipping the stop slot
        [review 2026-09-21, BLOCKING — see `be_latch_decision`];
      · at the END of every bar from the latch bar on, `stop` is floored at
        entry, so bar j+1's stop test, and `matched_step`'s advance-only
        comparison, both see `max(floor, ratchet)`.

    WHAT WOULD MAKE THIS WRONG: flooring the stop BEFORE the latch bar's own
    stop test (the floor would exit a bar it was not yet armed on); taking
    the BE fill after the bell (a stop is not a close); letting the floor
    LOWER a ratchet that had already passed it; or answering the latch bar
    on 4h extremes, which is the question the 5m walk exists to answer.
    """
    st = T9.frame(sym)
    f = st["f"]
    ra = T9.role_arrays(sym, roles)
    fr = T9.fractals(sym, card.trail_l, card.trail_r) if card.trail else None
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

    # ── the breakeven floor's own state ─────────────────────────────────
    be_r = getattr(card, "be_floor_after_r", None)
    be_on = be_r is not None
    be_trigger_px = entry_px + d * float(be_r) * R if be_on else float("nan")
    be_reached, be_bar, be_order, be_why = False, None, "", ""
    n_be_tie, n_be_mismatch = 0, 0
    stop_hist = [float(stop0)]

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
        be_latch_now = bool(be_on and not be_reached and ufav >= float(be_r))
        if be_latch_now:
            be_reached, be_bar = True, j
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

        # ═══ THE STOP SLOT.  On the latch bar the 5m walk owns it; on every
        # ═══ other bar it is the parent's test, verbatim.
        if be_latch_now:
            seq = be_sequence(sym, int(f.open_ms[j]), d, entry_px,
                              be_trigger_px, float(f.h[j]), float(f.l[j]))
            be_order, be_why = seq["order"], seq["why"]
            n_be_tie += int(seq["order"] == "tie")
            n_be_mismatch += int(seq["order"] == "mismatch")
            decision = be_latch_decision(seq)
            if decision == BE_LATCH_FILL:
                exit_i, exit_px, exit_reason = j, float(entry_px), BE_REASON
                if touch:
                    blocked = BE_REASON
                held = float(seq["mfe_held"])
                if np.isfinite(held) and (held - entry_px) * d > (mfe - entry_px) * d:
                    mfe = held
                break
            elif decision == BE_LATCH_OLD_STOP:
                # dip_first / tie / mismatch / a plus1r_first that never
                # dipped -> the OLD stop stands for this bar, and the
                # parent's own test decides it, verbatim.
                if (d == 1 and f.l[j] <= stop) or (d == -1 and f.h[j] >= stop):
                    exit_i, exit_px, exit_reason = j, stop, "stop"
                    if touch:
                        blocked = "stop"
                    break
            else:
                raise SystemExit(
                    f"HALT: {sym} campaign at bar {ti} — the latch bar {j} "
                    f"came back with decision {decision!r}, which is not one "
                    f"of {BE_LATCH_DECISIONS}. The latch bar's stop slot is "
                    f"TOTAL: every 5m answer is a fill or the old stop, and "
                    f"a bar with no stop decision would ride through a "
                    f"breached stop.")
        else:
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
        # ═══ THE FLOOR, ARMED FOR THE NEXT BAR.  max(floor, ratchet) for a
        # ═══ long, min for a short — monotone, and asserted as such.
        if be_on and be_reached:
            pre_floor = float(stop)
            stop = apply_floor(stop, entry_px, d)
            if (stop - pre_floor) * d < -1e-12:
                raise SystemExit(
                    f"HALT: {sym} campaign at bar {ti} — the breakeven floor "
                    f"LOWERED the stop at bar {j} ({pre_floor} -> {stop}). "
                    f"The floor is max(floor, ratchet), not an assignment.")
        if (stop - stop_hist[-1]) * d < -1e-12:
            raise SystemExit(
                f"HALT: {sym} campaign at bar {ti} — the stop moved AGAINST "
                f"the position ({stop_hist[-1]} -> {stop}) at bar {j}. The "
                f"ratchet is advance-only and the floor may only raise it.")
        stop_hist.append(float(stop))

    return {"own_r": abs(float(entry_px) - float(stop0)), "entry_i": ti,
            "entry_px": float(entry_px), "stop0": float(stop0),
            "exit_i": exit_i, "exit_px": float(exit_px),
            "exit_reason": exit_reason, "advances": advances, "harvest": harv,
            "blocked": blocked, "mfe": mfe, "mae": mae, "adds": [],
            "final_stop": stop, "n_opportunities": n_opp,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r,
            # ── the BE diagnostics, printed and never silent ──────────────
            "be_on": be_on, "be_reached": be_reached, "be_bar": be_bar,
            "be_order": be_order, "be_why": be_why,
            "be_exit": bool(exit_reason == BE_REASON),
            "n_be_tie": n_be_tie, "n_be_mismatch": n_be_mismatch,
            "be_bound_at_exit": bool(
                be_on and be_reached and exit_reason == "stop"
                and abs(float(exit_px) - float(entry_px)) <= 1e-12),
            "stop_path": list(stop_hist)}


matched_step = T8.matched_step


def ratchet_exit_flag(leg: dict) -> bool:
    """True iff the campaign exited on a stop THE RATCHET carried there.

    `tierc9`'s own expression with ONE clause added: a stop exit the FLOOR
    carried is not a ratchet exit [review 2026-09-21].  At the registered pin
    the two cannot be confused — `be_floor_after_r` 1.0 equals v6's
    `trail_arm_after_r`, so no advance can precede the latch and a floor-bound
    exit has an EMPTY `advances` — but above it an advance may sit below entry
    while the floor lifts the stop TO entry, and the campaign then exits at
    the floor with advances on its record.  `stop_advanced_atr` still counts
    both lifts (it is the lineage's published quantity); `be_bound_at_exit`
    and `stop_path` print beside it and say which lift was binding.

    With the floor OFF `be_bound_at_exit` is always False and this IS the
    parent's expression, 0.000e+00 [F-LANES-OFF].
    """
    return bool(leg["exit_reason"] == "stop" and leg["advances"]
                and abs(leg["final_stop"] - leg["stop0"]) > 1e-12
                and not leg["be_bound_at_exit"])


# ═══════════════════════════════════ THE SPRING SIGNAL — SHAPE, NOT MACHINE
@dataclass
class SpringSignal(RC.Spring):
    """`tierc5_rules.Spring`, plus its provenance and its as-of stamp.

    It SUBCLASSES the lineage's Spring so `RC.spring_stop` and `RC.Trade`
    take it unchanged — the stop geometry is re-pointed, never re-chosen.
    `known_at` is the bar at whose CLOSE the signal becomes knowable; for a
    macro harden that is the harden bar itself, so `known_at == reclaim_i`
    and the earliest legal entry is that bar's close.
    """

    known_at: int = -1
    rid: int = -1
    side: str = ""
    source: str = ""


def check_signals(f, springs, lo_i: int = 0, hi_i: int | None = None) -> dict:
    """THE AS-OF AND SHAPE WARRANTY ON AN INJECTED SIGNAL LIST — read off the
    RAW TAPE, with no range code anywhere in reach.

    Every claim a signal makes about the tape is re-derived here and must hold
    EXACTLY:
      (i)   0 <= sweep_i <= reclaim_i < n, and both inside the window;
      (ii)  bars_to_reclaim == reclaim_i - sweep_i;
      (iii) known_at == reclaim_i — a signal knowable only at its harden bar
            may not carry an earlier stamp, and `replay10` enters at
            `reclaim_i`'s close, so an early stamp would BE look-ahead;
      (iv)  sweep_ms == open_ms[sweep_i] and reclaim_ms == open_ms[reclaim_i];
      (v)   sweep_extreme == min(low[sweep_i:reclaim_i+1]) for a long
            (max(high[...]) for a short) — the RAW extreme, never the
            machine's 2-dp event field;
      (vi)  THE DEVIATION-CONFIRM SHAPE: the sweep extreme is BEYOND the
            swept level and the reclaim bar CLOSES BACK INSIDE it.  This is
            what makes the class a deviation-confirm and it is definitional
            (the census measures it at 34/34 and 27/27 on BTC 4h), so a
            signal that fails it is not one;
      (vii) the list is sorted by (reclaim_ms, -direction), the lineage's own
            candidate order.

    A signal stamped ONE BAR EARLY fails (vi): the harden is by construction
    the FIRST bar that closes back inside, so the bar before it does not.
    That is the sabotage leg F-SPR-SYN plants.

    WHAT IT CANNOT CHECK, SAID PLAINLY [review 2026-09-21].  Nothing here can
    verify that `swept_level` is the AS-OF boundary rather than a redrawn one:
    the raw tape does not know what a boundary is, and a range module in this
    function's reach is exactly what F-LANES-CLOSURE forbids.  (vi) tests the
    deviation-confirm SHAPE against whatever level the signal carries, and
    AS-OF-NESS is delegated to `springs_from_episodes` (which reads
    `bot_asof[a]` / `top_asof[a]` AT THE BREACH BAR) and thence to the census
    module's own F-RNG-ASOF.  A leaked level could therefore only change
    signal ADMISSION, never a price: the level never enters the stop
    (`tierc5_rules.spring_stop` reads `sweep_extreme` alone).  P-SPR-2's
    as-of warranty rests on the census's fixture, not on this file's — and
    the BUILD doc must say so.

    WHAT WOULD MAKE THIS WRONG: checking the signal against the machine that
    produced it (self-comparison), loosening (v) to a tolerance, or letting a
    signal outside the window pass because it will be skipped later.
    """
    n = int(len(f.c))
    hi_i = (n - 1) if hi_i is None else int(hi_i)
    h, l, c, om = f.h, f.l, f.c, f.open_ms
    bad: list[str] = []
    prev = None
    for k, sp in enumerate(springs):
        tag = f"signal[{k}] {getattr(sp, 'source', '')!r}"
        d, a, i = int(sp.direction), int(sp.sweep_i), int(sp.reclaim_i)
        if d not in (1, -1):
            bad.append(f"{tag}: direction {d}")
            continue
        if not (0 <= a <= i < n):
            bad.append(f"{tag}: indices sweep {a} reclaim {i} outside [0,{n})")
            continue
        if not (lo_i <= i <= hi_i):
            bad.append(f"{tag}: reclaim bar {i} outside the window "
                       f"[{lo_i},{hi_i}]")
            continue
        if int(sp.bars_to_reclaim) != i - a:
            bad.append(f"{tag}: bars_to_reclaim {sp.bars_to_reclaim} != "
                       f"{i - a}")
        ka = int(getattr(sp, "known_at", -1))
        if ka != i:
            bad.append(f"{tag}: known_at {ka} != reclaim_i {i} — a signal "
                       f"stamped at a bar other than the one it becomes "
                       f"knowable at")
        if int(sp.sweep_ms) != int(om[a]):
            bad.append(f"{tag}: sweep_ms {sp.sweep_ms} != open_ms[{a}] "
                       f"{int(om[a])}")
        if int(getattr(sp, "reclaim_ms", om[i])) != int(om[i]):
            bad.append(f"{tag}: reclaim_ms {sp.reclaim_ms} != open_ms[{i}]")
        raw = (float(l[a:i + 1].min()) if d == 1
               else float(h[a:i + 1].max()))
        if float(sp.sweep_extreme) != raw:
            bad.append(f"{tag}: sweep_extreme {sp.sweep_extreme!r} != the raw "
                       f"tape's {raw!r} over [{a},{i}]")
        lvl = float(sp.swept_level)
        if not np.isfinite(lvl):
            bad.append(f"{tag}: swept_level is not finite")
        elif d == 1 and not (raw < lvl and float(c[i]) >= lvl):
            bad.append(f"{tag}: not a bottom deviation-confirm — extreme "
                       f"{raw} vs level {lvl}, reclaim close {float(c[i])}")
        elif d == -1 and not (raw > lvl and float(c[i]) <= lvl):
            bad.append(f"{tag}: not a top deviation-confirm — extreme {raw} "
                       f"vs level {lvl}, reclaim close {float(c[i])}")
        key = (int(sp.reclaim_ms), -d)
        if prev is not None and key < prev:
            bad.append(f"{tag}: out of candidate order {key} after {prev}")
        prev = key
    if bad:
        raise SystemExit("HALT: the injected spring signal list does not "
                         "survive the raw tape:\n  " + "\n  ".join(bad[:8])
                         + (f"\n  ... {len(bad) - 8} more" if len(bad) > 8
                            else ""))
    return {"n_signals": len(springs),
            "n_long": sum(1 for s in springs if s.direction == 1),
            "n_short": sum(1 for s in springs if s.direction == -1)}


# ═════════════════════════════════════════════════════ THE REPLAY, TC10
_SCOPE_DEFAULTS = {f.name: getattr(T8.Card(), f.name)
                   for f in dataclasses.fields(T8.Card) if f.name != "name"}


def replay10(sym: str, card, roles: T9.Roles, lo_ms: int, hi_ms: int,
             springs=None) -> tuple[list, list]:
    """`tierc9.replay9`, with the scope re-declared for TC10's two lanes.

    THE SCOPE IS DECLARED AND ENFORCED [tc8 law, tc9's own words].  Every knob
    `replay9` HALTs on, this HALTs on, for the same reason: a knob running
    silently under a lane's name would make every "vs v6" row compare two
    different programs.  TWO things are added:
      · `be_floor_after_r` is READ (that is what this module exists for);
      · TOTALITY — the offered card's field set must be EXACTLY `tierc8.Card`'s
        plus this module's named knobs.  A guard that names some of the knobs
        it drops certifies the rest by omission, and a DROPPED knob is the one
        class F-LANES-OFF cannot catch, because it reproduces v6 at 0.000e+00
        under a lying card name [tc9 review L1, one tier later].

    THE SPRING LANE takes its signals as an ARGUMENT.  Nothing in this
    function, or anything it calls, imports a line of range code; the signals
    are verified against the RAW TAPE by `check_signals` before one candidate
    is built.
    """
    if card.lane not in LANES:
        raise SystemExit(f"HALT: tierc10_lanes rides {LANES}; got "
                         f"lane={card.lane!r}.")
    want = set(_SCOPE_DEFAULTS) | set(NEW_KNOBS) | {"name"}
    got = {f.name for f in dataclasses.fields(card)}
    if got != want:
        raise SystemExit(
            f"HALT: tierc10_lanes reads a KNOWN card. Fields it does not "
            f"know: {sorted(got - want)}; fields it expects and did not get: "
            f"{sorted(want - got)}. An unread knob would ride silently.")
    if card.adds_max:
        raise SystemExit(f"HALT: tierc10_lanes rides no adds; got "
                         f"adds_max={card.adds_max}.")
    if not card.seal_open:
        raise SystemExit("HALT: tierc10_lanes does not thread the lockbox "
                         "mask.")
    if card.trail_extra_buf_atr:
        raise SystemExit("HALT: tierc10_lanes' ladder offset arrives as "
                         "anchor_offset; trail_extra_buf_atr would drop.")
    if getattr(card, "weave", False) or getattr(card, "reentry", False):
        raise SystemExit("HALT: tierc10_lanes rides v6 mechanics — no weave, "
                         "no re-entry. Those arms live in tierc8.")
    if getattr(card, "ae_abort_r", None) is not None:
        raise SystemExit("HALT: tierc10_lanes rides v6 mechanics — no AE "
                         "abort.")
    if card.time_stop_bars is not None:
        raise SystemExit("HALT: tierc10_lanes rides v6 mechanics — no time "
                         "stop.")
    if getattr(card, "anchor_kind", "pivot") != "pivot":
        raise SystemExit(f"HALT: tierc10_lanes trails the card's (2,2) pivot "
                         f"only; got anchor_kind={card.anchor_kind!r}.")
    if getattr(card, "hybrid_anchor", False):
        raise SystemExit("HALT: tierc10_lanes reads no hybrid anchor; it "
                         "would ride silently as pure pivot.")
    if getattr(card, "stop_grid_offset_atr", 0.0):
        raise SystemExit("HALT: tierc10_lanes reads no stop-grid offset; the "
                         "S-SG dimension would silently drop.")
    if card.anchor_offset != RC.STOP_BUF_ATR:
        raise SystemExit(f"HALT: tierc10_lanes is a LANE study — "
                         f"anchor_offset={card.anchor_offset} would run the "
                         f"v8 S-OFF dimension under a lane's name.")
    if card.harvest != "band":
        raise SystemExit(f"HALT: tierc10_lanes implements the band harvest "
                         f"only; harvest={card.harvest!r} would ride with NO "
                         f"harvest at all.")
    be_r = getattr(card, "be_floor_after_r", None)
    if be_r is not None and not (isinstance(be_r, (int, float))
                                 and np.isfinite(be_r) and be_r > 0):
        raise SystemExit(f"HALT: be_floor_after_r={be_r!r} — the floor arms "
                         f"at a FAVOURABLE excursion, so the threshold is a "
                         f"finite positive number of R, or None for OFF.")
    if card.lane in ("spring", "union") and springs is None:
        raise SystemExit(
            f"HALT: lane={card.lane!r} takes its signal list as an ARGUMENT "
            f"and was given none. The runner never builds signals; the "
            f"harness does, and hands them in.")
    if card.lane == "card" and springs:
        raise SystemExit("HALT: lane='card' was handed a spring signal list; "
                         "a signal that cannot be ridden must not be passed.")

    st = T9.frame(sym)
    f = st["f"]
    lo_i, hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
    lo_i = max(lo_i, roles.floor_bars)          # THE FLOOR, PER CELL [tc9 D2]
    if hi_i < lo_i:
        return [], []

    arms: list = []
    cands: list = []
    if card.lane in ("card", "union"):
        arms, cc = T9.card_candidates9(sym, roles, lo_i, hi_i)
        cands += [(ti, d_, "card", a, None) for ti, d_, a in cc]
    if card.lane in ("spring", "union"):
        # the list handed in is THIS asset's; the runner slices it per symbol
        # and the shape warranty is re-run here, against THIS frame's tape.
        mine = list(springs or [])
        check_signals(f, mine, lo_i, hi_i)
        cands += [(int(sp.reclaim_i), int(sp.direction), "spring", None, sp)
                  for sp in mine]
    cands.sort(key=lambda c: (c[0], -c[1], c[2]))

    trades: list = []
    open_until = -1
    for ti, d, kind, arm, sp in cands:
        if ti <= open_until:
            if arm is not None:
                arm.reject = "position_open"
            continue
        entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])
        if not (np.isfinite(atr_sig) and atr_sig > 0):
            if arm is not None:
                arm.reject = "degenerate_R"
            continue
        if kind == "card":
            stp = RC.struct_stop_4h(st["pv4"], ti, entry_px, d, atr_sig,
                                    min_stop_atr=card.entry_rail_atr,
                                    forbidden=None)
        else:
            stp = RC.spring_stop(sp, entry_px, atr_sig, card.entry_rail_atr)
        if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            if arm is not None:
                arm.reject = "no_struct_anchor"
            continue
        if arm is not None:
            arm.entered, arm.reject, arm.entry_scored = True, "entered", True
        leg = _ride_leg10(sym, card, roles, d, ti, entry_px, stp.stop_px,
                          stp.r_dist, hi_i)
        chain = {"legs": [leg], "n_reentries": 0, "reentry_refused": ""}
        open_until = leg["exit_i"]
        acc = T7._account_chain(sym, card, d, stp.r_dist, chain)
        harv = leg["harvest"]
        anchor_ms = (int(f.open_ms[stp.anchor_bar]) if stp.anchor_bar >= 0
                     else -1)
        lb0 = _ms(RC.LOCKBOX_WAS[0])
        lb1 = _ms(RC.LOCKBOX_WAS[1]) + MS_1D - 1
        t = RC.Trade(
            symbol=sym, lane=kind, direction=d,
            arm_i=(arm.arm_i if arm is not None else int(sp.sweep_i)),
            arm_ms=(arm.arm_ms if arm is not None else int(sp.sweep_ms)),
            entry_i=ti, entry_ms=int(f.open_ms[ti]), entry_px=entry_px,
            stop_px=stp.stop_px, r_dist=stp.r_dist, anchor=stp.anchor,
            anchor_bar_ms=anchor_ms,
            anchor_was_sealed=bool(anchor_ms > 0 and lb0 <= anchor_ms <= lb1),
            atr_at_entry=atr_sig,
            disp_at_arming=(arm.disp if arm is not None else float("nan")),
            exit_i=leg["exit_i"], exit_ms=int(f.open_ms[leg["exit_i"]]),
            exit_px=leg["exit_px"], exit_reason=leg["exit_reason"],
            bars_held=leg["exit_i"] - ti, scored=True,
            advances=list(leg["advances"]),
            final_stop_px=leg["final_stop"],
            stop_advanced_atr=(leg["final_stop"] - leg["stop0"]) * d / atr_sig,
            ratchet_exit=ratchet_exit_flag(leg),
            harvested=harv is not None,
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(f.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=leg["blocked"],
            harvest_ride_would_have_r=acc["harvest_ride_would_have_r"],
            adds=[], add_r=None, spring=sp,
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
                     ("roles_name", roles.name),
                     ("card_name", card.name),
                     ("be_on", leg["be_on"]), ("be_reached", leg["be_reached"]),
                     ("be_bar", leg["be_bar"]), ("be_order", leg["be_order"]),
                     ("be_why", leg["be_why"]), ("be_exit", leg["be_exit"]),
                     ("n_be_tie", leg["n_be_tie"]),
                     ("n_be_mismatch", leg["n_be_mismatch"]),
                     ("be_bound_at_exit", leg["be_bound_at_exit"]),
                     ("stop_path", list(leg["stop_path"]))):
            object.__setattr__(t, k, v)
        trades.append(t)
    return arms, trades


_REPLAY10_AT_IMPORT = replay10      # a fixture stubs the NAME; this holds the
#                                     real function, and the gate compares


# ═════════════════════════════════════ THE DOOR — TEXT BEFORE RESULT [LAW 4]
def is_control_ride(card, roles, panel, lane: str = "card",
                    springs=None) -> bool:
    """True iff this is THE KNOWN CONTROL: THIS module's card with every
    inherited v8 field at its default AND every new knob OFF, the v6 roles,
    the card lane, no injected signals, and a non-empty subset of CLASSIC5.

    Both classes are checked EXACTLY and every field is compared FIELD BY
    FIELD from the dataclass fields — a subclass overriding a property cannot
    pass for v6 [tierc10_panel.is_control_book's law, re-pointed]."""
    if type(card) is not Card or type(roles) is not T9.Roles:
        return False
    if lane != "card" or card.lane != "card" or springs:
        return False
    if not knobs_off(card):
        return False
    for k, v in _SCOPE_DEFAULTS.items():
        if repr(getattr(card, k, object())) != repr(v):
            return False
    if TP.ride_spec(T8.Card(), roles) != TP.CONTROL_RIDE:
        return False
    panel = tuple(panel)
    return bool(panel and len(set(panel)) == len(panel)
                and set(panel) <= set(TP.CLASSIC5))


def _check_window(panel, lo_ms: int, hi_ms: int) -> tuple:
    """`run_cell_n`'s window law, re-pointed: the end must be a 4h bar CLOSE
    no later than the panel's own corridor end under Stage D's as-of pin."""
    lo_c, hi_c, meta = TP.corridor_n(panel)
    if hi_ms > hi_c or (int(hi_ms) + 1) % MS_4H or lo_ms > hi_ms:
        raise SystemExit(
            f"HALT: run_lane window [{iso(int(lo_ms))}, "
            f"{iso(int(hi_ms) + 1)}) — the end must be a 4h bar CLOSE no "
            f"later than the panel's corridor end {iso(hi_c + 1)} (the "
            f"as-of); a later end would read bars stamped after it.")
    return lo_c, hi_c, meta


def run_lane(card, roles: T9.Roles, panel, lo_ms: int, hi_ms: int,
             lane: str | None = None, springs_by_sym: dict | None = None,
             reg_id: str | None = None, text: str | None = None,
             arm: str | None = None, lanes=None, head_of_record=None,
             reg_root: Path | None = None):
    """THE ONLY WAY A TC10 LANE RIDES REAL BARS — and the gate is the FIRST
    statement, above every other check.

    Exactly one book rides without paperwork: the known control
    (`is_control_ride`), which the contract names as ALLOWED.  EVERY other
    book — the breakeven floor ON, any spring lane, any unseen asset — walks
    through `tierc10_panel.require_arm`: a registration ALREADY FILED, its
    text in the caller's hand, the hash-chained registry pinned by a head
    held OUTSIDE the registry directory, and the NAMED ARM filed for an
    EXTERNAL runner on exactly this panel with exactly these lanes.  The
    journal comes back as a `tierc10_panel.Book` wearing that gate, which is
    what `score()` reads back — so no hand-built Book exists anywhere in this
    file.

    Returns a plain `list` for the control (it is not a registered book and
    must not wear provenance it does not have) and a `Book` for a gated lane.

    WHAT WOULD MAKE THIS WRONG: calling the gate after the frames are built
    (the bars would already be in memory); widening the control exception by
    one field; or letting a throwaway registry open the gate onto the REAL
    replay — which is why a non-canonical root demands a stubbed `replay10`,
    exactly as `run_cell_n` demands a stubbed `replay9`.
    """
    lane = lane or card.lane
    panel = tuple(panel)
    gate = None
    if is_control_ride(card, roles, panel, lane, springs_by_sym):
        via = TP.CONTROL_ARM
    else:
        if reg_id is None or text is None or arm is None:
            raise SystemExit(
                f"HALT: run_lane refuses — card={card.name!r} lane={lane!r} "
                f"roles={roles.name!r} panel={TP.panel_name(panel)} is not "
                f"the known control, and reg_id/text/arm were not ALL given. "
                f"TEXT BEFORE RESULT: file it with tierc10_panel.register() "
                f"first, then name the arm this runner rides.")
        root = Path(reg_root) if reg_root else TP.REG_DIR
        gate = TP.require_arm(reg_id, text, arm, panel,
                              lanes=(lanes if lanes is not None
                                     else (lane,)),
                              head_of_record=head_of_record, root=root)
        if root.resolve() != TP.REG_DIR.resolve() \
                and replay10 is _REPLAY10_AT_IMPORT:
            raise SystemExit(
                f"HALT: run_lane refuses — {root} is not the canonical "
                f"registry {TP.REG_DIR}; a throwaway registry opens the gate "
                f"onto a STUBBED replay only (fixtures). Real bars need the "
                f"registry of record.")
        via = gate["arm"]
        # THE FILED ERA, BEFORE A BAR IS READ [review 2026-09-21].
        # `tierc10_panel.external_book` refuses a journal whose campaigns
        # ENTER outside the arm's era — but that is after the bars have been
        # replayed, and an arm filed for the holdout era handed the full
        # corridor would have READ the tuning era first.  `run_cell_n` checks
        # it at the door (panel:1164-1172) and so does this door.
        e_lo, e_hi = TP.era_window(gate["era"])
        if (e_lo is not None and int(lo_ms) < e_lo) \
                or (e_hi is not None and int(hi_ms) > e_hi):
            raise SystemExit(
                f"HALT: run_lane refuses — arm {via!r} is filed for the "
                f"{gate['era']!r} era ({TP.era_note(gate['era'])}), and the "
                f"offered window [{iso(int(lo_ms))}, {iso(int(hi_ms) + 1)}) "
                f"leaves it. Ride tierc10_panel.corridor_era(panel, "
                f"{gate['era']!r}).")
    _check_window(panel, lo_ms, hi_ms)
    for s in panel:
        TP.frame_n(s)               # substrate · funding · memo safety
    trades: list = []
    for s in panel:
        _, t = replay10(s, card, roles, lo_ms, hi_ms,
                        springs=(None if springs_by_sym is None
                                 else list(springs_by_sym.get(s, ()))))
        trades += t
    if gate is None:
        return trades
    return TP.external_book(trades, gate, lo_ms, hi_ms)


def run_cell10(card, roles: T9.Roles, panel, lo_ms: int, hi_ms: int, **kw):
    """`tierc9.run_cell9` over a declared panel, through this module's door.
    A thin alias kept because that is the lineage's name for it."""
    return run_lane(card, roles, panel, lo_ms, hi_ms, **kw)


# ═══════════════════════════ THE SIGNAL HARNESS — the only census reader
def harden_episodes(events) -> list[tuple]:
    """(rid, side, breach_i, harden_i) for every macro deviation episode.

    PURE over the event list — it is handed the events and imports nothing.
    A harden closes the LAST same-side breach-open of its range, which is the
    census as-of layer's own episode law (`tierc10_census:664-672`).

    TWO HARDENS, ONE OPEN [review 2026-09-21].  When two hardens fire on the
    same (rid, side) with no breach-open between them, the SECOND pairs with
    the SAME (now stale) open — the open is not consumed.  That is not this
    port's invention: `tierc10_census`'s own pairing behaves identically, and
    a port that "fixed" it here would make the spring lane's episodes
    disagree with the census tables printed beside them.  The duplicate case
    is fixtured next to the orphan case (F-SPR-BUILD) so the behaviour is
    recorded rather than assumed.

    WHAT WOULD MAKE THIS WRONG: pairing a harden with a breach of the other
    side or of another range, or letting a harden with no open pass silently.
    """
    opens: dict = {}
    out: list[tuple] = []
    for e in events:
        kind = e.get("event")
        if kind not in ("breach-open", "harden"):
            continue                    # pivots, seeds, redraws carry no rid
        k = (e["rid"], e["side"])
        if kind == "breach-open":
            opens[k] = int(e["i"])
        else:
            if k not in opens:
                raise SystemExit(
                    f"HALT: harden at bar {e['i']} on rid {e['rid']} side "
                    f"{e['side']} has no same-side breach-open before it; "
                    f"the episode law is broken.")
            out.append((int(e["rid"]), str(e["side"]), int(opens[k]),
                        int(e["i"])))
    out.sort(key=lambda r: (r[3], r[2]))
    return out


def springs_from_episodes(h, l, c, open_ms, episodes, top_asof, bot_asof,
                          lo_i: int = 0, hi_i: int | None = None,
                          source: str = "") -> list:
    """The deviation-confirm signal list, from episodes + the AS-OF boundary
    arrays.  PURE over arrays: it is handed `top_asof` / `bot_asof` and never
    asks a machine for them.

    bottom-side harden -> LONG spring; top-side harden -> SHORT upthrust
    [R3: "top side in, we trade both ways"].  `sweep_extreme` is the RAW
    tape's extreme over [breach, harden]; `swept_level` is the AS-OF boundary
    AT THE BREACH BAR, which is the boundary the deviation actually swept —
    never the redrawn one the harden itself produces.
    """
    n = int(len(c))
    hi_i = (n - 1) if hi_i is None else int(hi_i)
    out: list = []
    for rid, side, a, i in episodes:
        if not (lo_i <= i <= hi_i) or not (0 <= a <= i < n):
            continue
        if side == "bottom":
            d, lvl = 1, float(bot_asof[a])
            ext = float(np.min(l[a:i + 1]))
        else:
            d, lvl = -1, float(top_asof[a])
            ext = float(np.max(h[a:i + 1]))
        if not np.isfinite(lvl):
            continue
        out.append(SpringSignal(
            direction=d, sweep_i=int(a), sweep_ms=int(open_ms[a]),
            sweep_extreme=ext, swept_level=lvl, reclaim_i=int(i),
            reclaim_ms=int(open_ms[i]), bars_to_reclaim=int(i - a),
            known_at=int(i), rid=int(rid), side=str(side), source=source))
    out.sort(key=lambda s: (s.reclaim_ms, -s.direction))
    return out


def spring_signals_from_census(sym: str, lens: str = "4h",
                               scale_mult: float = FROZEN_SCALE,
                               tape=None, lo_i: int = 0,
                               hi_i: int | None = None) -> list:
    """THE ONE FUNCTION HERE THAT READS THE RANGE CENSUS — and it imports it
    INSIDE ITS OWN BODY, so this module's import closure stays range-free
    [F-LANES-CLOSURE; map_critic §4.9's wiring].

    Frozen pins, by object: SCALE_MULT comes in as `FROZEN_SCALE` = 3.0
    [LEAN L2] and DEV_RETURN_BARS is the machine's own frozen 7 — the P-RNG
    slate's K = 4 is SUPERSEDED, and the registration text must say 7.

    The signals come back indexed in the CENSUS TAPE's index space; hand them
    to `signals_on_frame` before they touch a 4h ride.
    """
    import tierc10_census as C                              # noqa: PLC0415
    tp = tape if tape is not None else C.load_tape(sym, lens)
    m = C.run_scale(tp, float(scale_mult))
    view = C.asof_view(tp, m["macro"], m["leash"])
    eps = harden_episodes(m["macro"]["events"])
    return springs_from_episodes(
        tp.h, tp.l, tp.c, tp.t0, eps, view["top"], view["bot"],
        lo_i=lo_i, hi_i=hi_i,
        source=f"census/{sym}/{lens}/scale{float(scale_mult)}")


def signals_on_frame(f, springs) -> list:
    """Re-index a signal list from the census tape onto the RIDE's 4h frame,
    by MILLISECOND STAMP and never by position, and re-derive every price
    from the frame's own raw tape.

    The two tapes hold the same bars for the 4h lens, but the ride's frame may
    carry bars the census tape cut at the as-of; a positional carry-over would
    be a silent one-bar shift, which is precisely the class F-SPR-SYN's
    sabotage leg plants by hand.

    IT RE-DERIVES, AND IT ALSO REFUSES [review 2026-09-21].  The extreme and
    the as-of stamp are re-derived on the RIDE's own tape — that tape is the
    tape of record for the ride — but a signal whose own claims DISAGREE with
    what this frame says is a CORRUPTED signal, and a corrupted signal is
    surfaced here rather than quietly repaired into a good one:
      · `known_at != reclaim_i` (an index-space invariant that survives
        re-indexing, so it can be checked before anything is re-derived);
      · `bars_to_reclaim != reclaim_i - sweep_i`;
      · a `sweep_extreme` that is not the RIDE tape's extreme over the same
        MILLISECOND window.  Both tapes read the same Stage D parquet for the
        4h lens (`tierc10_census.load_tape` -> `klines/{sym}_4h.parquet`), so
        a genuine agreement is bit-equal and a disagreement is either a
        corrupted signal or two different substrates — neither of which may
        ride under a repaired stamp.
    """
    om = f.open_ms
    out: list = []
    for sp in springs:
        a = int(np.searchsorted(om, int(sp.sweep_ms), "left"))
        i = int(np.searchsorted(om, int(sp.reclaim_ms), "left"))
        if not (0 <= a < len(om) and 0 <= i < len(om)) \
                or int(om[a]) != int(sp.sweep_ms) \
                or int(om[i]) != int(sp.reclaim_ms):
            raise SystemExit(
                f"HALT: signal {sp.source!r} stamps sweep {sp.sweep_ms} / "
                f"reclaim {sp.reclaim_ms}, and the ride's frame holds no bar "
                f"opening at one of them.")
        if int(getattr(sp, "known_at", -1)) != int(sp.reclaim_i):
            raise SystemExit(
                f"HALT: signal {sp.source!r} carries known_at "
                f"{getattr(sp, 'known_at', None)!r} against reclaim_i "
                f"{int(sp.reclaim_i)} — a signal knowable only at its harden "
                f"bar may not arrive stamped at another, and re-indexing "
                f"REPOINTS a stamp, it does not repair one.")
        if int(sp.bars_to_reclaim) != int(sp.reclaim_i) - int(sp.sweep_i):
            raise SystemExit(
                f"HALT: signal {sp.source!r} carries bars_to_reclaim "
                f"{int(sp.bars_to_reclaim)} against reclaim_i - sweep_i = "
                f"{int(sp.reclaim_i) - int(sp.sweep_i)}.")
        d = int(sp.direction)
        ext = (float(np.min(f.l[a:i + 1])) if d == 1
               else float(np.max(f.h[a:i + 1])))
        if float(sp.sweep_extreme) != ext:
            raise SystemExit(
                f"HALT: signal {sp.source!r} carries sweep_extreme "
                f"{float(sp.sweep_extreme)!r}; the ride's own tape says "
                f"{ext!r} over [{iso(int(sp.sweep_ms))}, "
                f"{iso(int(sp.reclaim_ms))}]. Both tapes read the same Stage "
                f"D 4h parquet, so this is a corrupted signal or a second "
                f"substrate — it is not re-derived away.")
        out.append(SpringSignal(
            direction=d, sweep_i=a, sweep_ms=int(sp.sweep_ms),
            sweep_extreme=ext, swept_level=float(sp.swept_level),
            reclaim_i=i, reclaim_ms=int(sp.reclaim_ms),
            bars_to_reclaim=int(i - a), known_at=i, rid=int(sp.rid),
            side=str(sp.side), source=str(sp.source)))
    out.sort(key=lambda s: (s.reclaim_ms, -s.direction))
    return out


# ═══════════════════════════════════ F-C10-BE · THE REAL-CAMPAIGN HARNESS
# THE THREE CAMPAIGNS ARE NOT NAMED YET AND CANNOT BE.  They must come from
# P-BE-1's own book, which does not exist until the registration is FILED
# (LAW 4).  Filling this tuple with (symbol, entry_ms) triples is the whole
# of what the fixture needs after filing; the hand-walk below is already
# written and already proven against the module on synthetic tapes.
BE_CAMPAIGNS: tuple = ()
BE_CAMPAIGNS_NOTE = (
    "F-C10-BE needs THREE REAL campaigns with one of each 5m order "
    "(dip-before, dip-after, and a tie or a 4h/5m mismatch) plus the "
    "converse of each. Their ids come from P-BE-1's filed book; until the "
    "registration is filed, naming them would be running the lane. The leg "
    "reports NOT RUN with this reason and never PASS.")


def hand_walk_5m(t5, h5, l5, c5, d: int, entry_px: float,
                 trigger_px: float) -> dict:
    """AN INDEPENDENT ANSWER TO THE SAME QUESTION, in plain numpy, written so
    it shares no code path with `be_sequence` [F-C9-TOP10's template].

    It walks the children one at a time in a python loop — no vectorised
    `flatnonzero`, no shared helper — and reports the first child that printed
    the trigger, the first that dipped to entry, and the resulting order.
    `be_sequence`'s answer must equal it on every campaign.

    WHAT WOULD MAKE THIS WRONG: importing `be_sequence`'s helpers, or
    re-deriving the answer the way the module derived it (self-comparison).
    """
    i_up = i_dip = None
    for k in range(len(t5)):
        fav = float(h5[k]) if d == 1 else float(l5[k])
        adv = float(l5[k]) if d == 1 else float(h5[k])
        if i_up is None and (fav - entry_px) * d >= (trigger_px - entry_px) * d:
            i_up = k
        if i_dip is None and (adv - entry_px) * d <= 0.0:
            i_dip = k
    if i_up is None:
        order = "no_print"
    elif i_dip is None:
        order = "plus1r_first"
    elif i_dip < i_up:
        order = "dip_first"
    elif i_up < i_dip:
        order = "plus1r_first"
    else:
        order = "tie"
    return {"order": order, "i_up": i_up, "i_dip": i_dip,
            "n_children": int(len(t5))}


def be_campaign_evidence(sym: str, bar_open_ms: int, d: int, entry_px: float,
                         r_dist: float, bar_hi: float, bar_lo: float,
                         be_r: float = 1.0) -> dict:
    """One real campaign's latch bar, read BOTH ways: the module's sequencer
    and the hand walk, side by side.  Used by F-C10-BE once the ids exist.

    `bar_hi` / `bar_lo` are the PARENT 4h bar's own extremes and must come
    from the 4h frame, never from the children — feeding the children's own
    aggregate back in would make the mismatch check tautological."""
    t5, h5, l5, c5 = children_5m(sym, int(bar_open_ms))
    trig = entry_px + d * float(be_r) * float(r_dist)
    mine = be_sequence(sym, int(bar_open_ms), d, entry_px, trig,
                       float(bar_hi), float(bar_lo))
    hand = hand_walk_5m(t5, h5, l5, c5, d, entry_px, trig)
    return {"symbol": sym, "bar_open_ms": int(bar_open_ms),
            "bar_open": iso(int(bar_open_ms)), "direction": int(d),
            "entry_px": float(entry_px), "trigger_px": float(trig),
            "module": mine, "hand": hand,
            "agree": bool(mine["order"] == hand["order"]
                          and mine["i_up"] == hand["i_up"]
                          and mine["i_dip"] == hand["i_dip"])}


# ═══════════════════════════════════════════════════════════ THE LANE SPEC
LANE_SPEC = {
    "P-BE-1": {
        "prior_pct": 40,
        "runner": "external",
        "lanes": ("card",),
        "ruler": "two_sample",
        "base": "card-v6",
        "knob": "be_floor_after_r = 1.0",
        "sequencing": ("the +1R bar is SEQUENCED on its 48 native 5m "
                       "children in tape order; dip-before -> the old stop "
                       "stands, dip-after -> BE fill at entry inside the "
                       "bar, same child -> adverse-first and counted, 4h/5m "
                       "extreme mismatch -> counted and adverse-first, and a "
                       "print with NO dip at all -> the old stop stands too"),
        "after_the_latch_bar": ("stop = max(floor, ratchet) for a long, min "
                                "for a short; monotone; exits labelled "
                                "`stop` with be_bound_at_exit beside"),
        "latch_bar_totality": ("the latch bar's stop slot is TOTAL: "
                               "`be_latch_decision` maps every 5m answer "
                               "onto a fill or the old stop, a third answer "
                               "HALTs, and F-BE-LATCH proves the ride at "
                               "be_floor_after_r = 2.0 (ABOVE v6's "
                               "trail_arm_after_r 1.0, where the ratchet can "
                               "precede the latch) exits exactly where the "
                               "floor-OFF ride does — so a sensitivity run "
                               "off the registered 1.0 is proven, not "
                               "assumed [review 2026-09-21]"),
        "ratchet_vs_floor": ("`ratchet_exit` excludes a floor-bound stop "
                             "exit; `stop_advanced_atr` counts both lifts "
                             "and `be_bound_at_exit` / `stop_path` say "
                             "which"),
    },
    "P-SPR-2": {
        "prior_pct": 45,
        "runner": "external",
        "lanes": ("spring",),
        "ruler": "vs_zero",
        "base": "zero",
        "signal": ("macro `harden` (deviation-confirm at a CONFIRMED macro "
                   "boundary) at the FROZEN pins SCALE_MULT 3.0 and "
                   "DEV_RETURN_BARS 7 (the P-RNG slate's K=4 is SUPERSEDED "
                   "by the frozen pin); bottom-side -> long spring, "
                   "top-side -> short upthrust"),
        "entry": "the harden bar's CLOSE (known_at = that bar)",
        "stop": ("tierc5_rules.spring_stop on the RAW-tape sweep extreme, "
                 "railed at the card's entry_rail_atr"),
        "population": "CLASSIC5 x full corridor x 4h [R3]",
        "scored_arm": ("the STANDALONE book's expectancy vs zero; the "
                       "union-with-card view is printed beside, "
                       "scored_in_family=False"),
        "as_of_warranty": ("`check_signals` tests the deviation-confirm "
                           "SHAPE on the raw tape; that `swept_level` is the "
                           "AS-OF boundary is delegated to "
                           "`springs_from_episodes` (bot_asof/top_asof READ "
                           "AT THE BREACH BAR) and thence to the census "
                           "module's F-RNG-ASOF — a leaked level could "
                           "change signal ADMISSION only, never a price, "
                           "since spring_stop reads sweep_extreme alone. "
                           "The BUILD doc must name F-RNG-ASOF as this "
                           "lane's as-of witness [review 2026-09-21]"),
    },
}


def main() -> int:
    """Print the lane spec and file NOTHING.  No registration may be filed in
    this workflow and no registered lane may ride, so there is nothing for a
    build driver to build [LAW 4]."""
    print("=" * 78)
    print("TIER-C10 · 4h LANE MECHANICS — P-BE-1 (breakeven) + P-SPR-2 "
          "(spring/upthrust)")
    print("=" * 78)
    print(f"substrate {TP.substrate()['substrate']} · seed {SEED} · frozen "
          f"SCALE_MULT {FROZEN_SCALE} · 5m children per 4h bar "
          f"{N_5M_PER_4H}")
    print(f"registry of record: {TP.REG_DIR} — "
          f"{'PRESENT' if TP.REG_DIR.exists() else 'ABSENT (nothing filed)'}")
    print()
    for k, v in LEANS.items():
        print(f"{LEAN_TAG} {k}: {v}")
    print()
    for reg, spec in LANE_SPEC.items():
        print(f"--- {reg}")
        for kk, vv in spec.items():
            print(f"    {kk}: {vv}")
    print()
    print("card knobs added by this module: "
          + ", ".join(f"{k} (OFF = {_KNOB_OFF[k]!r})" for k in NEW_KNOBS))
    print("LAW 4: this module files no registration, computes no P-* number, "
          "and rides no real book but the known control.")
    print(f"F-C10-BE campaigns: {BE_CAMPAIGNS or 'NOT NAMED'} — "
          f"{BE_CAMPAIGNS_NOTE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
