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
    +1R print THEN dip-to-entry         -> the floor FILLS inside the bar, at
                                           the EFFECTIVE stop
                                           max(ratchet, entry) — which IS
                                           entry wherever the ratchet still
                                           sits below it [`be_latch_fill`];
    both inside ONE 5m child            -> adverse-first, and COUNTED;
    the +1R print and NO dip at all     -> the OLD stop stands TOO, and the
                                           parent's stop test runs on it.
The last two lines are not decoration, and BOTH were written wrong once.
Once the ratchet has carried the stop ABOVE entry, a latch bar can pierce
that stop without ever reaching entry, and a branch that tested only
"dip_first / tie / mismatch" left that bar with NO stop decision [review
2026-09-21, BLOCKING; `be_latch_decision`].  And a latch bar that DOES reach
entry over such a ratchet must have crossed the ratchet on the way, so a fill
priced at `entry_px` unconditionally paid a price the tape had taken away
[review 2026-09-21 / R0 2026-09-22, BLOCKING; `be_latch_fill`, measured at
-0.411957 R long / -0.412369 R short on one campaign].
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
tuning-era bar and be refused afterwards.  Unfiled, amended or stale-pinned
it HALTs [F-LANES-GATE, post-371123f].  The one book that rides unfiled is the
KNOWN CONTROL (card v6, every knob at its default, every new knob OFF, roles
v6, a non-empty subset of CLASSIC5) — the contract's own exception.

`replay10` ITSELF IS UNGATED, BY DESIGN — the door is `run_lane`, exactly as
`tierc9.replay9`'s door is `run_cell_n`.  Called directly it rides, and no
code in this file can stop it; what stops it is that STAGE B's driver must
show `require_arm(` above every replay, and a reviewer greps for that.  Said
here so nobody mistakes the gate for a property of the replay.

LAW 4, IN THIS FILE.  Nothing here computes a P-GEN-1 / P-SPR-2 / P-BE-1 /
P-TRG-2 / P-BRK-S1 / P-BRK-I1 number.  `main()` prints the lane spec and
files nothing.  Fixture real bars: the control + P-BE-1 A1's latch census.

Run:  NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921 \\
      ~/venvs/naiad/bin/python scripts/tierc10_lanes.py
"""
from __future__ import annotations

import dataclasses
import hashlib
import json
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
    "L-be-latch-fill": ("THE CONTRACT DOES NOT PIN THIS AND CANNOT REACH IT "
                        "AT THE REGISTERED PIN.  Its words for the latch bar "
                        "are 'BE exit AT ENTRY inside the bar'; they are "
                        "silent on a latch bar reached when the RATCHET "
                        "already stands past entry, because at "
                        "be_floor_after_r = 1.0 (== v6's trail_arm_after_r) "
                        "no advance can precede the latch.  Above 1.0 it is "
                        "reachable, and the tape coming down from the latch "
                        "print to entry MUST cross that ratchet first.  SO: "
                        "the latch bar's fill is the EFFECTIVE stop "
                        "max(ratchet, entry) for a long, min for a short "
                        "[`be_latch_fill`], labelled `be_floor` only when it "
                        "IS entry and `stop` otherwise.  At the registered "
                        "pin this is BYTE-IDENTICAL to a bare entry fill and "
                        "F-BE-IDENT proves it; above it the two differ and "
                        "F-BE-IDENT proves THAT too"),
    "L-be-mfe-ratchet": ("a RATCHET-BOUND latch-bar fill advances no MFE.  "
                         "[L-be-mfe] runs the held extreme to the child that "
                         "DIPPED to entry; a ratchet-bound fill exits at an "
                         "EARLIER child than that, so crediting the held "
                         "extreme would credit tape after the exit and "
                         "breach the lineage's HELD law.  It also makes the "
                         "latch bar agree, field for field, with the same "
                         "bar reached through the OLD_STOP branch — which is "
                         "the honest answer, since on such a bar the tape "
                         "forces the same exit whichever order the 5m walk "
                         "reports"),
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


def be_latch_fill(stop: float, entry_px: float, d: int) -> tuple:
    """WHAT THE LATCH BAR'S FILL PAYS — the EFFECTIVE stop, never `entry_px`
    unconditionally [review 2026-09-21 / R0 2026-09-22, BLOCKING, REPAIRED].

    THE DEFECT THIS REPLACES.  The fill branch used to read

        exit_i, exit_px, exit_reason = j, float(entry_px), BE_REASON

    and `break`.  `stop` was never consulted, and because the branch broke out
    of the loop the parent's stop test never ran on that bar either — so a
    `plus1r_first` WITH a dip ALWAYS filled at entry, even when the ratchet
    had already carried `stop` PAST entry.  The tape cannot get from the latch
    print down to entry without crossing a stop that sits between them, so
    that fill paid a price the tape had already taken away.  MEASURED on the
    synthetic latch tape at `be_floor_after_r = 2.0`: floor OFF exits
    (369, 'stop') at +0.412163 R; floor ON exited (369, 'be_floor') at
    +0.000000 R while its OWN `stop_path` ended at +0.412163 R — a fabricated
    -0.411957 R long / -0.412369 R short on ONE campaign.

    THE REPAIR, IN ONE LINE.  The fill is `apply_floor(stop, entry_px, d)` —
    max(ratchet, floor) for a long, min for a short — and it is labelled
    `be_floor` only when it IS the floor.  Above the floor it is an ordinary
    `stop`, which is the contract's own words for every bar after the latch,
    applied to the latch bar itself.

    THE SAFETY PROPERTY, AND IT IS PROVEN NOT ASSERTED [F-BE-IDENT].  At the
    REGISTERED pin `be_floor_after_r = 1.0` — which equals v6's
    `trail_arm_after_r` — no advance can precede the latch, so `stop` is still
    `stop0` (adverse), `apply_floor` returns `entry_px`, and the ride is
    BYTE-IDENTICAL to the pre-repair ride.  F-BE-IDENT digests the whole
    scenario set both ways and requires equality at 1.0 and INEQUALITY at 2.0.

    WHAT WOULD MAKE THIS WRONG: returning `entry_px` unconditionally (the
    defect); labelling a fill above the floor `be_floor` (it would then count
    as a breakeven exit and `be_bound_at_exit` would lie); or letting the fill
    be WORSE for the position than the stop already on the record, which is
    the cheap invariant F-BE-NOWORSE drives.
    """
    fill = apply_floor(float(stop), float(entry_px), int(d))
    return float(fill), (BE_REASON if fill == float(entry_px) else "stop")


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
        `fill` (the floor fills inside the bar, PRICED BY `be_latch_fill` at
        the EFFECTIVE stop max(ratchet, entry) and labelled `be_floor` only
        when that is entry) or `old_stop` (the OLD stop stands and the
        parent's stop test runs unchanged), and a decision this leg does not
        know HALTs rather than skipping the stop slot [review 2026-09-21,
        BLOCKING — see `be_latch_decision` and `be_latch_fill`];
      · at the END of every bar from the latch bar on, `stop` is floored at
        entry, so bar j+1's stop test, and `matched_step`'s advance-only
        comparison, both see `max(floor, ratchet)`.

    WHAT WOULD MAKE THIS WRONG: flooring the stop BEFORE the latch bar's own
    stop test (the floor would exit a bar it was not yet armed on); taking
    the BE fill after the bell (a stop is not a close); letting the floor
    LOWER a ratchet that had already passed it; pricing the latch bar's fill
    at `entry_px` without consulting `stop` (the repaired defect); or
    answering the latch bar on 4h extremes, which is the question the 5m walk
    exists to answer.
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
                # THE EFFECTIVE STOP, never entry unconditionally.  Below the
                # floor this IS entry and the ride is unmoved; above it the
                # ratchet is what the tape crossed on the way down, and the
                # ratchet is what the campaign is paid [be_latch_fill].
                fill, reason = be_latch_fill(stop, entry_px, d)
                exit_i, exit_px, exit_reason = j, float(fill), reason
                if touch:
                    blocked = reason
                if reason == BE_REASON:
                    # [LEAN L-be-mfe] applies to a BE fill AT ENTRY only: the
                    # held extreme runs to the child that DIPPED, and on a
                    # ratchet-bound fill the exit is an EARLIER child than
                    # that, so crediting it would credit tape after the exit.
                    # A ratchet-bound latch bar therefore advances no MFE —
                    # exactly as the OLD_STOP branch below does not, which is
                    # what makes the two orders agree on that bar.
                    held = float(seq["mfe_held"])
                    if np.isfinite(held) \
                            and (held - entry_px) * d > (mfe - entry_px) * d:
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
# P-BE-1 IS FILED (371123f), AND ITS FILED TEXT GOVERNS THIS LEG.  Until the
# filing this block said the three campaigns "are not named yet and cannot
# be", and that was true: they come from P-BE-1's own book, which could not
# exist before the text.  The text now exists, and its §9 prescribes what
# happens when the book cannot supply the three orders the contract names:
#
#   "if P-BE-1's filed book contains no tie and no 4h/5m mismatch latch bar,
#    the leg must report NOT RUN with that reason. It must NOT substitute a
#    synthetic bar or relabel a dip_first case to reach three."
#
# So the rows are never TYPED here.  They are DERIVED, by the rule in
# `be_c10_decision`, from the LATCH CENSUS of the filed book
# (`be_latch_census`, filed by the fixture suite as
# research_outputs/tierc10/lanes/BE_LATCH_CENSUS.json).  `BE_CAMPAIGNS` stays
# an EMPTY tuple on purpose: a hand-typed row is exactly the substitution §9
# forbids, and the fixture suite asserts it stays empty.
BE_CAMPAIGNS: tuple = ()
BE_CAMPAIGNS_NOTE = (
    "P-BE-1 is FILED (371123f) and its filed text §9 governs F-C10-BE: 'if "
    "P-BE-1's filed book contains no tie and no 4h/5m mismatch latch bar, "
    "the leg must report NOT RUN with that reason. It must NOT substitute a "
    "synthetic bar or relabel a dip_first case to reach three.' The three "
    "rows (one dip-before, one dip-after, one tie-or-mismatch, each with its "
    "converse) are DERIVED by rule from the latch census of the filed book "
    "(BE_LATCH_CENSUS.json, built by `be_latch_census` from P-BE-1's scored "
    "arm ridden through the filed door) and are never typed here. "
    "BE_CAMPAIGNS stays EMPTY: a hand-typed row is the substitution §9 "
    "forbids. The leg is never reported PASS unless the census supplies all "
    "three classes.")

# ── THE FILED DOOR, READ FROM THE RECORD [371123f] ─────────────────────────
# The text of record and the pinned head are read from the TRACKED files
# Stage B filed them into — never typed, never read back out of the
# registration file itself (offering the door the bytes it holds would be
# comparing it with itself).  json only: this module's import closure stays
# range-free [F-LANES-CLOSURE].
REGISTRY_PIN_PATH = TP.OUT / "REGISTRY_PIN.json"
REGISTRATION_TEXTS_PATH = TP.OUT / "REGISTRATION_TEXTS.json"
BE1_REG, SPR2_REG = "P-BE-1", "P-SPR-2"
LANE_REGS = (BE1_REG, SPR2_REG)
BE1_SCORED_ARM = "be-floor-1R vs card-v6 (CLASSIC5, full)"
BE1_SCORED_ERA = "full"


def filed_text(reg_id: str, path: Path | None = None) -> str:
    """THE TEXT OF RECORD for a filed registration, from
    REGISTRATION_TEXTS.json — the drafted file it was filed FROM."""
    p = Path(path) if path else REGISTRATION_TEXTS_PATH
    if not p.is_file():
        raise SystemExit(f"HALT: no texts of record at {p}.")
    t = (json.loads(p.read_text(encoding="utf-8")).get(reg_id)
         or {}).get("text")
    if not isinstance(t, str) or not t.strip():
        raise SystemExit(f"HALT: {p.name} carries no text for {reg_id!r}.")
    return t


def filed_head(reg_id: str, path: Path | None = None) -> tuple:
    """(registry_len, registry_head) as PINNED for `reg_id` in
    REGISTRY_PIN.json — the witness the door holds the chain against."""
    p = Path(path) if path else REGISTRY_PIN_PATH
    if not p.is_file():
        raise SystemExit(f"HALT: no registry pin at {p}.")
    r = (json.loads(p.read_text(encoding="utf-8")).get("registrations")
         or {}).get(reg_id)
    if not r or not r.get("already_filed"):
        raise SystemExit(f"HALT: {p.name} pins no FILED head for {reg_id!r}.")
    return (int(r["registry_len"]), str(r["registry_head"]))


# ── THE CLASSES OF A LATCH BAR, AND THE THREE THE CONTRACT REQUIRES ─────────
# `order` alone cannot carry the contract's classes: `plus1r_first` is BOTH
# the dip-after bar (the floor FILLS) and the print-with-no-dip bar (the old
# stop stands), and a closing check written on `order` counted the second
# as the first.  The class reads the order AND whether a dip happened.
BE_CLASSES = ("dip_before", "dip_after", "print_no_dip", "tie", "mismatch")
BE_REQUIRED = ("dip_before", "dip_after", "tie_or_mismatch")
BE_REQUIRED_QUOTE = "dip-before, dip-after, and a tie or a 4h/5m mismatch"
BE_SECTION9 = (
    "if P-BE-1's filed book contains no tie and no 4h/5m mismatch latch bar, "
    "the leg must report NOT RUN with that reason. It must NOT substitute a "
    "synthetic bar or relabel a dip_first case to reach three.")


def be_class(order: str, dip: bool) -> str:
    """The latch bar's CLASS from a walk's `order` and whether it dipped."""
    if order == "dip_first":
        return "dip_before"
    if order == "plus1r_first":
        return "dip_after" if dip else "print_no_dip"
    if order in ("tie", "mismatch"):
        return order
    return f"unknown:{order}"


def be_required_class(cls: str) -> str:
    """The contract's slot a class fills: a tie and a mismatch share one."""
    return "tie_or_mismatch" if cls in ("tie", "mismatch") else cls


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


def hand_parent_check(t5, h5, l5, bar_open_ms: int, bar_hi: float,
                      bar_lo: float) -> dict:
    """THE HAND'S OWN MISMATCH DETECTOR — so `agree` can hold on a GENUINE
    4h/5m mismatch campaign instead of failing it by construction.

    `hand_walk_5m` cannot see the parent bar, so on a mismatch campaign it
    answers the children's order while the module answers `mismatch`; an
    `agree` written as "the two orders are equal" could therefore NEVER hold
    on the very class the contract requires one of.  This walks, in plain
    python loops sharing nothing with `be_sequence`: 48 children
    ((4 * 60) // 5, recomputed here), each opening exactly 5 minutes after
    the one before from the parent's own open, and the children's extremes
    EQUAL to the parent's — EXACT float equality, because both come from
    the venue's decimal strings and a genuine agreement is bit-equal (the
    module's 1e-9 REPR_TOL is not borrowed; a bar inside that window would
    surface as a disagreement, which is the honest answer).

    WHAT WOULD MAKE THIS WRONG: borrowing `_same_px` or `N_5M_PER_4H`
    (self-comparison), or passing a bar whose children do not reproduce it.
    """
    n = int(len(t5))
    want_n, step = (4 * 60) // 5, 5 * 60 * 1000
    grid = n == want_n
    for k in range(n):
        if int(t5[k]) != int(bar_open_ms) + k * step:
            grid = False
    hi = lo = None
    for k in range(n):
        hk, lk = float(h5[k]), float(l5[k])
        hi = hk if hi is None or hk > hi else hi
        lo = lk if lo is None or lk < lo else lo
    same_hi = hi is not None and hi == float(bar_hi)
    same_lo = lo is not None and lo == float(bar_lo)
    return {"ok": bool(grid and same_hi and same_lo), "n_children": n,
            "grid": bool(grid), "same_high": bool(same_hi),
            "same_low": bool(same_lo)}


def converse_children(t5, h5, l5, c5) -> tuple:
    """THE CONVERSE OF A LATCH BAR: the same 48 children with their PRICES
    (high, low, close) in reverse tape order and their TIMESTAMPS KEPT.

    THE DEFECT THIS REPLACES.  The converse used to reverse all four arrays,
    timestamps included, and a reversed timestamp array is not the 5m grid —
    so `be_sequence` answered `mismatch` for EVERY campaign and "the
    converse moved the order" held by construction, whatever the tape said.
    Keeping the stamps keeps the grid, keeps the extremes (the same set of
    prices), and asks the sequencer the one real question: this bar's prices
    in the other order.  Reversal maps the FIRST child that printed or
    dipped onto the LAST one, so the converse's answer is predictable from
    the original children, and the fixtures predict it independently."""
    return (t5, np.asarray(h5)[::-1].copy(), np.asarray(l5)[::-1].copy(),
            np.asarray(c5)[::-1].copy())


# Which rows are EXEMPT from "the converse flips the order": the ones whose
# order cannot matter.  A tie is read inside ONE child, so the 5m tape holds
# no order to flip.  A print with NO dip and a 4h/5m mismatch are INVARIANT
# under the converse (no child dips in either order; the extremes, the count
# and the grid are unchanged), and that invariance is ASSERTED, not assumed.
BE_CONVERSE_EXEMPT = ("tie",)
BE_CONVERSE_INVARIANT = ("print_no_dip", "mismatch")


def be_converse_ok(cls: str, rev_cls: str) -> bool:
    """Does the converse behave as the class says it must?
      dip_before / dip_after -> the converse is the OTHER of the two (it
                                must flip, and it may not land on a mismatch,
                                which would prove nothing about order);
      print_no_dip / mismatch -> the converse is the SAME class (invariance);
      tie                     -> exempt: no order inside one child."""
    if cls in ("dip_before", "dip_after"):
        return rev_cls in ("dip_before", "dip_after") and rev_cls != cls
    if cls in BE_CONVERSE_INVARIANT:
        return rev_cls == cls
    return cls in BE_CONVERSE_EXEMPT


def be_campaign_evidence(sym: str, bar_open_ms: int, d: int, entry_px: float,
                         r_dist: float, bar_hi: float, bar_lo: float,
                         be_r: float = 1.0, converse: bool = False) -> dict:
    """One real campaign's latch bar, read BOTH ways: the module's sequencer
    and the hand walk (+ the hand's own parent check), side by side.  With
    `converse=True` the same bar is read with its prices reversed and its
    stamps kept [`converse_children`].

    `bar_hi` / `bar_lo` are the PARENT 4h bar's own extremes and must come
    from the 4h frame, never from the children — feeding the children's own
    aggregate back in would make the mismatch check tautological.

    `agree` IS CLASS AGREEMENT PLUS CHILD-INDEX AGREEMENT: the module's class
    (`be_class` of its order and dip) equals the hand's (`mismatch` when the
    hand's parent check fails, else `be_class` of the hand walk), and both
    walks name the same first print child and first dip child.  It used to
    be ORDER equality, which a genuine mismatch campaign could never meet.

    The sequencer is asked about exactly these children by rebinding this
    module's `children_5m` for the one call and restoring it in `finally` —
    `be_sequence` itself, the registered mechanism, is not touched."""
    kids = children_5m(sym, int(bar_open_ms))
    if converse:
        kids = converse_children(*kids)
    t5, h5, l5, c5 = kids
    trig = entry_px + d * float(be_r) * float(r_dist)
    g = globals()
    held = g["children_5m"]
    g["children_5m"] = lambda _s, _b, _k=kids: _k
    try:
        mine = be_sequence(sym, int(bar_open_ms), d, entry_px, trig,
                           float(bar_hi), float(bar_lo))
    finally:
        g["children_5m"] = held
    hand = hand_walk_5m(t5, h5, l5, c5, d, entry_px, trig)
    parent = hand_parent_check(t5, h5, l5, int(bar_open_ms), float(bar_hi),
                               float(bar_lo))
    m_cls = be_class(mine["order"], bool(mine["dip"]))
    h_cls = ("mismatch" if not parent["ok"]
             else be_class(hand["order"], hand["i_dip"] is not None))
    return {"symbol": sym, "bar_open_ms": int(bar_open_ms),
            "bar_open": iso(int(bar_open_ms)), "direction": int(d),
            "entry_px": float(entry_px), "trigger_px": float(trig),
            "converse": bool(converse),
            "module": mine, "hand": hand, "parent": parent,
            "module_class": m_cls, "hand_class": h_cls,
            "agree": bool(m_cls == h_cls
                          and mine["i_up"] == hand["i_up"]
                          and mine["i_dip"] == hand["i_dip"])}


# ── THE LATCH CENSUS OF THE FILED BOOK — OUTCOME-FREE ──────────────────────
# Every field a census row carries is IDENTITY (which campaign, which latch
# bar), ENTRY GEOMETRY fixed at the entry bar's close, or a SEQUENCING FACT
# about the latch bar's 48 children (the three answers, the class, the
# agreement flags, the converse).  NO exit, price-after-entry, excursion or
# outcome field is read into a row or written out, and the fixture suite
# holds every row's key set against its own whitelist and an outcome
# denylist [F-C10-BE-CENSUS].
BE_CENSUS_ROW_FIELDS = (
    "symbol", "direction", "entry_ms", "entry_px", "r_dist",
    "latch_bar_open_ms", "latch_bar_open", "trigger_px",
    "journal_order", "module_order", "hand_order", "parent_reproduced",
    "i_up", "i_dip", "class", "hand_class",
    "module_eq_journal", "module_eq_hand", "three_way",
    "converse_module_class", "converse_hand_class", "converse_agree",
    "converse_ok")
BE_CENSUS_RULE = (
    "Every campaign of P-BE-1's SCORED arm A1 'be-floor-1R vs card-v6 "
    "(CLASSIC5, full)', ridden by tierc10_lanes.run_lane through "
    "tierc10_panel.require_arm (the text of record from "
    "REGISTRATION_TEXTS.json, the head pinned in REGISTRY_PIN.json) and "
    "tierc10_panel.external_book on CLASSIC5 over corridor_era(CLASSIC5, "
    "'full'), card CARD_BE1 (be_floor_after_r 1.0), roles v6. A campaign is "
    "in the census iff its journal says be_reached; its LATCH BAR is the "
    "journal's be_bar on the ride's own 4h frame. Each latch bar is read "
    "THREE WAYS: the ride's own answer (journal be_order), the module's "
    "be_sequence re-run on the bar, and the plain-loop hand_walk_5m with "
    "the hand's own parent check (48 children, the 5m grid, EXACT "
    "extremes). CLASS: dip_before = dip_first; dip_after = plus1r_first "
    "WITH a dip; print_no_dip = plus1r_first with NO dip; tie; mismatch. "
    "The contract's three required classes are dip_before, dip_after and "
    "tie_or_mismatch. THE CONVERSE re-reads the bar with its prices "
    "reversed and its timestamps kept. Rows are ordered by panel position, "
    "then entry_ms. No exit, price-after-entry, excursion or outcome field "
    "is read or written, and nothing here is scored.")


def be_latch_census(book, be_r: float = 1.0) -> dict:
    """THE LATCH CENSUS of one ridden Book: per latch bar, identity + class +
    agreement flags, and the counts.  Pure over the Book and the tapes; it
    rides nothing and files nothing (the fixture suite files it).

    WHAT WOULD MAKE THIS WRONG: reading the latch bar's extremes from its
    children (the mismatch check would be tautological); classifying on
    `order` alone (a print with no dip would count as dip-after); letting
    one exit or outcome field into a row; or relabelling a class to fill a
    slot — the census reports what the walks say, and nothing else."""
    spec = dict(getattr(book, "spec", None) or {})
    panel = list(spec.get("panel") or [])
    pos = {s: k for k, s in enumerate(panel)}
    rows: list = []
    for t in book:
        if not bool(getattr(t, "be_reached", False)):
            continue
        f = T9.frame(t.symbol)["f"]
        j, d = int(t.be_bar), int(t.direction)
        om = int(f.open_ms[j])
        args = (t.symbol, om, d, float(t.entry_px), float(t.r_dist),
                float(f.h[j]), float(f.l[j]), float(be_r))
        ev = be_campaign_evidence(*args)
        rv = be_campaign_evidence(*args, converse=True)
        m = ev["module"]
        full = {
            "symbol": str(t.symbol), "direction": d,
            "entry_ms": int(t.entry_ms), "entry_px": float(t.entry_px),
            "r_dist": float(t.r_dist),
            "latch_bar_open_ms": om, "latch_bar_open": iso(om),
            "trigger_px": float(ev["trigger_px"]),
            "journal_order": str(t.be_order), "module_order": m["order"],
            "hand_order": ev["hand"]["order"],
            "parent_reproduced": bool(ev["parent"]["ok"]),
            "i_up": m["i_up"], "i_dip": m["i_dip"],
            "class": ev["module_class"], "hand_class": ev["hand_class"],
            "module_eq_journal": bool(m["order"] == str(t.be_order)),
            "module_eq_hand": bool(ev["agree"]),
            "converse_module_class": rv["module_class"],
            "converse_hand_class": rv["hand_class"],
            "converse_agree": bool(rv["agree"]),
            "converse_ok": bool(rv["agree"] and be_converse_ok(
                ev["module_class"], rv["module_class"]))}
        full["three_way"] = bool(full["module_eq_journal"]
                                 and full["module_eq_hand"])
        rows.append({k: (full[k] if k in full else getattr(t, k))
                     for k in BE_CENSUS_ROW_FIELDS})
    rows.sort(key=lambda r: (pos.get(r.get("symbol"), len(pos)),
                             int(r.get("entry_ms", 0)),
                             int(r.get("direction", 0))))
    by = {c: 0 for c in BE_CLASSES}
    for r in rows:
        by[r["class"]] = by.get(r["class"], 0) + 1
    per_sym = {s: sum(1 for r in rows if r["symbol"] == s) for s in panel}
    counts = {
        "n_campaigns": len(book), "n_latch": len(rows), "by_class": by,
        "tie_or_mismatch": int(by.get("tie", 0) + by.get("mismatch", 0)),
        "by_symbol": per_sym,
        "n_module_eq_journal": sum(bool(r["module_eq_journal"])
                                   for r in rows),
        "n_module_eq_hand": sum(bool(r["module_eq_hand"]) for r in rows),
        "n_three_way": sum(bool(r["three_way"]) for r in rows),
        "n_converse_agree": sum(bool(r["converse_agree"]) for r in rows),
        "n_converse_ok": sum(bool(r["converse_ok"]) for r in rows)}
    return {"artifact": "BE_LATCH_CENSUS", "tier": "TIER-C10",
            "registration": spec.get("registration"), "arm": spec.get("arm"),
            "era": spec.get("era"), "panel": panel,
            "registration_sha256": spec.get("registration_sha256"),
            "window_lo": (None if spec.get("lo_ms") is None
                          else iso(int(spec["lo_ms"]))),
            "window_hi": (None if spec.get("hi_ms") is None
                          else iso(int(spec["hi_ms"]) + 1)),
            "be_floor_after_r": float(be_r), "rule": BE_CENSUS_RULE,
            "classes": list(BE_CLASSES), "required": list(BE_REQUIRED),
            "converse_exempt": list(BE_CONVERSE_EXEMPT),
            "converse_invariant": list(BE_CONVERSE_INVARIANT),
            "row_fields": list(BE_CENSUS_ROW_FIELDS),
            "withheld": ("every exit, price-after-entry, excursion and "
                         "outcome field of the Book; nothing is scored"),
            "section9": BE_SECTION9, "counts": counts,
            "f_c10_be": be_c10_decision_of(rows, counts), "rows": rows}


def be_census_json(census: dict) -> str:
    """The census's bytes of record: sorted keys, indent 2, trailing newline,
    no wall clock — so two runs give one sha."""
    return json.dumps(census, indent=2, sort_keys=True, default=str) + "\n"


def be_c10_decision_of(rows: list, counts: dict) -> dict:
    """THE RULE THAT DECIDES F-C10-BE FROM THE CENSUS — and the only source
    of its rows.  Per required class, in BE_REQUIRED order, the FIRST census
    row (census order) of that class whose three answers agree and whose
    converse behaves [`be_converse_ok`].  Nothing is chosen by outcome (no
    outcome is in reach) and nothing is typed.

      · no tie AND no mismatch in the book -> NOT RUN, with P-BE-1 §9's own
        reason (the filed text prescribes this case);
      · another required class absent -> NOT RUN, and it is an OPERATOR
        QUESTION: §9 forbids substitution but prescribes nothing for it;
      · all three present -> RUN on exactly those three rows."""
    by = dict(counts.get("by_class") or {})
    pick, missing = {}, []
    for req in BE_REQUIRED:
        ok = [r for r in rows if be_required_class(r["class"]) == req
              and r["three_way"] and r["converse_ok"]]
        if ok:
            pick[req] = ok[0]
        else:
            missing.append(req)
    tally = (f"{counts.get('n_latch')} latch bars of "
             f"{counts.get('n_campaigns')} campaigns: dip-before "
             f"{by.get('dip_before', 0)}, dip-after {by.get('dip_after', 0)}, "
             f"print-no-dip {by.get('print_no_dip', 0)}, tie "
             f"{by.get('tie', 0)}, 4h/5m mismatch {by.get('mismatch', 0)}; "
             f"three-way agreement {counts.get('n_three_way')}/"
             f"{counts.get('n_latch')}")
    if int(by.get("tie", 0)) + int(by.get("mismatch", 0)) == 0:
        return {"decision": "NOT RUN", "governed_by": "P-BE-1 §9",
                "operator_question": False, "missing": missing, "rows": [],
                "reason": (f"P-BE-1 §9 (filed text): \"{BE_SECTION9}\" — "
                           f"P-BE-1's filed book (scored arm A1) contains "
                           f"NO tie and NO 4h/5m mismatch latch bar: "
                           f"{tally}. Required classes absent: {missing}. "
                           f"No synthetic bar is substituted and no "
                           f"dip_first case is relabelled; BE_CAMPAIGNS "
                           f"stays empty.")}
    if missing:
        return {"decision": "NOT RUN", "governed_by": "OPERATOR",
                "operator_question": True, "missing": missing, "rows": [],
                "reason": (f"the filed book lacks required class(es) "
                           f"{missing} ({tally}); §9 forbids substitution "
                           f"and prescribes nothing for this case — an "
                           f"OPERATOR QUESTION, not a PASS.")}
    return {"decision": "RUN", "governed_by": "the census rule",
            "operator_question": False, "missing": [],
            "rows": [pick[r] for r in BE_REQUIRED],
            "reason": f"all three required classes present: {tally}"}


# ═════════════════ THE LATCH BAR'S WORDS — NARROWED TO WHAT THE LEGS PROVE
# THE CLAIM THAT STOOD HERE UNTIL 2026-09-22 WAS FALSE AS WRITTEN, and a
# builder DECLINED a reviewer's protective HALT on the strength of it.  It
# said F-BE-LATCH "proves the ride at be_floor_after_r = 2.0 ... exits exactly
# where the floor-OFF ride does — so a sensitivity run off the registered 1.0
# is proven, not assumed".  F-BE-LATCH's A_ROWS authors the latch bar as
# (high +2.05 R, low +0.15 R, close +1.20 R): the low NEVER reaches entry, so
# `be_latch_decision` answered `old_stop` and only the OLD_STOP half of the
# branch was ever driven.  The FILL half — the half that carried the blocking
# defect — was untested, and the words covered for it.
#
# The prose below is PINNED BY SHA (`LATCH_TOTALITY_SHA`) and every claim it
# makes is listed in `LATCH_TOTALITY_CLAIMS` against the fixture that drives
# it.  F-BE-SPEC checks all three together, so the words cannot be
# STRENGTHENED without either re-pinning the sha beside a new leg, or going
# RED.  That is the whole mechanism: a sentence here is a promise about a leg
# somewhere else, and nothing but a fixture can keep the two honest.
LATCH_TOTALITY = (
    "the latch bar's stop slot is TOTAL: `be_latch_decision` maps every 5m "
    "answer onto a fill or the old stop, and a third answer HALTs. The fill "
    "is PRICED by `be_latch_fill` at the EFFECTIVE stop — max(ratchet, "
    "entry) for a long, min for a short — and labelled `be_floor` only when "
    "that IS entry, so a latch bar the tape could only reach by crossing a "
    "ratcheted stop exits at that stop [repaired 2026-09-22; the branch used "
    "to pay `entry_px` unconditionally]. AT be_floor_after_r = 2.0 (ABOVE "
    "v6's trail_arm_after_r 1.0, where the ratchet CAN precede the latch) "
    "F-BE-LATCH drives TWO hand-authored latch bars over a ratchet standing "
    "above entry — `plus1r_first` with NO dip, and `plus1r_first` WITH a dip "
    "— in both directions, and in every one of the four the floor-ON ride "
    "exits on the same bar, at the same price, for the same reason as the "
    "floor-OFF ride. THAT IS ALL IT PROVES: four hand-authored bars, NOT a "
    "sensitivity run, and nothing here says the 2.0 book equals the 1.0 book "
    "on real bars. At the REGISTERED pin 1.0 the repair is BYTE-IDENTICAL to "
    "the pre-repair ride and F-BE-IDENT digests the whole scenario set both "
    "ways to prove it, and proves the two DIFFER at 2.0 so the identity is "
    "not vacuous. F-BE-NOWORSE carries the cheap invariant underneath all of "
    "it: a stop-class exit is never worse for the position than the stop "
    "already on its own `stop_path`."
)

# Each claim is (a phrase that must appear VERBATIM in LATCH_TOTALITY, the
# fixture that drives it).  F-BE-SPEC requires the phrase to occur EXACTLY
# ONCE and the fixture to have PASSED in the same run.
LATCH_TOTALITY_CLAIMS = (
    ("a third answer HALTs", "F-BE-LATCH"),
    ("`plus1r_first` with NO dip", "F-BE-LATCH"),
    ("`plus1r_first` WITH a dip", "F-BE-LATCH"),
    ("in both directions", "F-BE-LATCH"),
    ("BYTE-IDENTICAL to the pre-repair ride", "F-BE-IDENT"),
    ("proves the two DIFFER at 2.0", "F-BE-IDENT"),
    ("never worse for the position than the stop already on its own "
     "`stop_path`", "F-BE-NOWORSE"),
)

# The exact sentence that was RETRACTED on 2026-09-22.  It is kept verbatim so
# the retraction is checkable: F-BE-SPEC refuses to find it anywhere in
# LANE_SPEC again.
LATCH_TOTALITY_RETRACTED = (
    "F-BE-LATCH proves the ride at be_floor_after_r = 2.0 (ABOVE v6's "
    "trail_arm_after_r 1.0, where the ratchet can precede the latch) exits "
    "exactly where the floor-OFF ride does",
    "so a sensitivity run off the registered 1.0 is proven, not assumed",
)

# sha256 of LATCH_TOTALITY.  Re-pinning it is the deliberate, greppable act a
# reviewer looks for when the words change [F-BE-SPEC].
LATCH_TOTALITY_SHA = ("54867daf9101ae14da90f5c38ceefbe345329669"
                      "b700fb319e0d46f1b97a23c4")


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
        "latch_bar_totality": LATCH_TOTALITY,
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


# ═══════════════════════════ THE STAGE MANIFEST — LAW 1(b)'s ON-DISK RECORD
# R0 (2026-09-22) found `lanes/` one of only two stage directories with no
# `build_manifest.json`, so clause (b) of the LAW OF RESUMPTION — "its
# manifest shas verify" — had NOTHING to verify against: the transcript was
# self-consistent and unattested.  This is that record, in the shape
# `census/`, `panel/` and `stamps/` already use.
#
# IT CARRIES NO WALL CLOCK.  A manifest with a timestamp in it cannot be
# re-derived, and LAW 1(b) is a RE-DERIVATION law: a second run must produce
# this file byte for byte [F-DET's own law, applied to the evidence].
LANES_WARRANTY = (
    "these mechanics are true AS OF the bar named in `as_of_last_closed_4h` "
    "and of no other; the corridor advances with the cache [TC6V-a, carried "
    "by TIER-C10]. The 5m children the BE sequencer walks are read through "
    "`tierc10_data.load_asof`, which CLOSES them at the same pin — the 5m "
    "parquet files hold rows past it and a sequencer that read one would be "
    "judging a campaign on a bar stamped after it."
)
LANES_GATES = (
    "NOTHING. This stage is MECHANICS, and no P-* number is computed. Since "
    "371123f P-BE-1 and P-SPR-2 are FILED (with the other four; the registry "
    "of record is the six lines pinned in REGISTRY_PIN.json), and they open "
    "ONLY through the filed door — the text of record and the pinned head "
    "[F-LANES-GATE]. Real bars enter this suite two ways: the KNOWN CONTROL "
    "(card v6, every new knob OFF, CLASSIC5), ridden to prove it is "
    "UNCHANGED [LAW 4, F-LANES-OFF]; and P-BE-1's scored arm A1, ridden "
    "through that door for its LATCH CENSUS alone (BE_LATCH_CENSUS.json: "
    "identity, class and agreement flags, no exit or outcome field) "
    "[F-C10-BE-CENSUS]. TP.score is never called and no .scored.json is "
    "written. F-C10-BE is DECIDED BY P-BE-1 §9 from that census and is "
    "never reported PASS unless the census supplies all three classes."
)
LANES_COMMISSION = {
    "P-BE-1": (
        "the BREAKEVEN FLOOR mechanism for the 4h card lane: "
        "`Card.be_floor_after_r` (registered pin 1.0, default None = OFF), "
        "the latch bar SEQUENCED on its 48 native 5m children, and from bar "
        "j+1 stop = max(floor, ratchet). Mechanism only — no arm, no book, "
        "no number."),
    "P-SPR-2": (
        "the SPRING / UPTHRUST lane for the 4h card: signals handed in as a "
        "PRECOMPUTED LIST and verified against the raw tape, entry at the "
        "harden bar's close, stop on the RAW sweep extreme. Mechanism only."),
    "P-SPR-2_population_of_record": (
        "OPERATOR RULING R3 (2026-09-21, verbatim): 'Full corridor, "
        "standalone vs zero, top side in, we trade both ways' — RATIFIED by "
        "ruling R9 (2026-09-22): 'R3 governs — full corridor, both ways', "
        "which supersedes the contract's frozen text '4h, 5-asset "
        "exploration-classic, vs card/standalone'. NOTE that "
        "'exploration-classic' is an ERA (<= 2024-06-30), not a panel: the "
        "superseded reading kept the CLASSIC5 panel and added an era collar, "
        "and R3/R9 drop the collar and keep the panel. THIS MODULE SERVES "
        "EITHER: the era is a WINDOW argument (`replay10(lo_ms, hi_ms)` / "
        "`run_lane`) and the signal list is built per-window "
        "(`spring_signals_from_census(lo_i, hi_i)`), so no code changes when "
        "a registration names one. TODAY IT SERVES R3/R9 — LANE_SPEC's "
        "`population` reads 'CLASSIC5 x full corridor x 4h [R3]' and no era "
        "collar exists anywhere in this file."),
    "not_commissioned": (
        "a registration text, a scored row, an arm, a verdict, or any "
        "P-BE-1 / P-SPR-2 number. TEXT BEFORE RESULT."),
}


def file_sha256(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def code_sha() -> str:
    return file_sha256(Path(__file__))


def lanes_input_sha(panel=None) -> dict:
    """sha256 of every input file a LANE reads.

    `tierc10_panel.input_sha` names the 4h klines and the funding tapes.  It
    does NOT name the native 5m tapes, and the BE sequencer walks those on
    every latch bar — a 5m parquet that moved would move a latch-bar answer
    with nothing in any manifest to attribute it to.  So they are added here,
    by the same path function the loader uses (`tierc10_data.kline_path`),
    never by a hand-built string."""
    panel = tuple(panel or TP.CLASSIC5)
    out = dict(TP.input_sha(panel))
    for sym in panel:
        q = D.kline_path(sym, "5m")
        out[f"{q.parent.name}/{q.name}"] = (file_sha256(q) if q.exists()
                                            else "ABSENT")
    return out


def build_manifest(fixture_results=None, not_run=None, panel=None) -> dict:
    """The stage record: code shas, the as-of, the seed, the commission, and
    the content sha of EVERY artifact in `research_outputs/tierc10/lanes/`.

    `build_manifest.json` itself is excluded — a file cannot carry its own
    sha — and every other file in the directory is listed, WHOLE: no
    filtering, no "the ones I wrote".  A stray artifact is recorded, not
    hidden, because the point of the record is to make the directory
    checkable by someone who did not build it."""
    panel = tuple(panel or TP.CLASSIC5)
    meta = TP.corridor_n(panel)[2]
    arts, shas = {}, {}
    if OUT.exists():
        for q in sorted(OUT.iterdir()):
            if not q.is_file() or q.name == "build_manifest.json":
                continue
            arts[q.name] = {"bytes": q.stat().st_size, "sha256": file_sha256(q)}
            shas[q.name] = arts[q.name]["sha256"]
    fx = dict(fixture_results or {})
    return {
        "tier": "TIER-C10",
        "stage": "TIER-C10 · STAGE B MECHANICS · LANES (P-BE-1, P-SPR-2)",
        "seed": SEED,
        "seed_lineage": getattr(TP, "SEED_LINEAGE", None),
        "substrate": TP.substrate()["substrate"],
        "as_of_last_closed_4h": meta["last_closed_4h_close"],
        "as_of_source": "Stage D AS_OF_PIN.json, via tierc10_panel.corridor_n",
        "panel_name": "CLASSIC5",
        "panel": list(panel),
        "book": ("card v6 · V6_ROLES · CLASSIC5 — the KNOWN CONTROL, ridden "
                 "unregistered by run_lane's own gate to prove it is "
                 "UNCHANGED; and, since 371123f, P-BE-1's scored arm A1 "
                 f"{BE1_SCORED_ARM!r} ridden THROUGH THE FILED DOOR for its "
                 "outcome-free latch census (BE_LATCH_CENSUS.json) and "
                 "nothing else — no outcome is summed, printed or filed"),
        "commission": LANES_COMMISSION,
        "gates": LANES_GATES,
        "warranty": LANES_WARRANTY,
        "code_sha": code_sha(),
        "fixtures_code_sha": file_sha256(ROOT / "scripts"
                                         / "tierc10_lanes_fixtures.py"),
        "panel_code_sha": file_sha256(ROOT / "scripts" / "tierc10_panel.py"),
        "data_code_sha": file_sha256(ROOT / "scripts" / "tierc10_data.py"),
        "census_code_sha": file_sha256(ROOT / "scripts"
                                       / "tierc10_census.py"),
        "input_sha": lanes_input_sha(panel),
        "artifacts": arts,
        "sha": shas,
        "new_knobs": {k: repr(_KNOB_OFF[k]) for k in NEW_KNOBS},
        "pins": {"FROZEN_SCALE_MULT": float(FROZEN_SCALE),
                 "DEV_RETURN_BARS": 7,
                 "N_5M_PER_4H": int(N_5M_PER_4H),
                 "REPR_TOL": float(REPR_TOL),
                 "BE_REASON": BE_REASON,
                 "be_floor_after_r_registered": 1.0,
                 "lanes": list(LANES)},
        "lane_spec": {k: dict(v) for k, v in LANE_SPEC.items()},
        "latch_bar_totality_sha": LATCH_TOTALITY_SHA,
        "latch_bar_totality_claims": [list(c) for c in LATCH_TOTALITY_CLAIMS],
        "latch_bar_totality_retracted": list(LATCH_TOTALITY_RETRACTED),
        "leans": dict(LEANS),
        "lean_tag": LEAN_TAG,
        "fixtures": {"results": fx, "not_run": dict(not_run or {}),
                     "n_pass": sum(1 for v in fx.values() if v),
                     "n_total": len(fx)},
        "be_campaigns": list(BE_CAMPAIGNS),
        "be_campaigns_note": BE_CAMPAIGNS_NOTE,
        "registry_of_record": str(TP.REG_DIR),
        "registry_present": bool(TP.REG_DIR.exists()),
        "registry_pin_of_lanes": _lane_pins(),
    }


def _lane_pins() -> dict:
    """The head each lane registration is held against, AS PINNED — or the
    reason it could not be read.  Printed, so the manifest names the door."""
    out = {}
    for reg in LANE_REGS:
        try:
            n, h = filed_head(reg)
            out[reg] = f"{n}:{h}"
        except SystemExit as e:
            out[reg] = f"UNREADABLE: {e}"
    return out


def write_manifest(fixture_results=None, not_run=None, panel=None) -> Path:
    """File it.  Sorted keys, indent 2, trailing newline — the estate's own
    shape, so two runs give one sha."""
    OUT.mkdir(parents=True, exist_ok=True)
    q = OUT / "build_manifest.json"
    q.write_text(json.dumps(build_manifest(fixture_results, not_run, panel),
                            indent=2, sort_keys=True, default=str) + "\n")
    return q


def main() -> int:
    """Print the lane spec and file NOTHING.  This module files no
    registration (the six of record were filed at 371123f, by Stage B) and
    main() rides nothing; the fixture suite files the transcript, the latch
    census and the manifest [LAW 4]."""
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
    print("LAW 4: this module files no registration and computes no P-* "
          "number; main() rides nothing. The door `run_lane` opens a FILED "
          "arm only with the text of record and the pinned head.")
    print(f"F-C10-BE campaigns: {BE_CAMPAIGNS or 'NOT NAMED'} — "
          f"{BE_CAMPAIGNS_NOTE}")
    q = OUT / "build_manifest.json"
    print(f"stage manifest {q}: "
          + (f"PRESENT, sha {file_sha256(q)[:16]}…" if q.exists()
             else "ABSENT — run tierc10_lanes_fixtures.py WHOLE; it files "
                  "the manifest after the transcript, and this function "
                  "files nothing [LAW 4]"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
