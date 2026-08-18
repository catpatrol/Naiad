"""TIER-C7 · S-STOPGRID [D-R7] AND L-ANCHOR — THE TWO STOP LABS.

CLASS: measurement.  NOTHING HERE IS SCORED AND NOTHING HERE GATES.  D15
columns ride every aggregate row and gate nothing; every grid is reported
WHOLE; every public function's docstring says WHAT WOULD MAKE IT WRONG.

This module builds ON `tierc7` — it does not fork it.  `tierc7.py` imports this
file through `_labs()` and this file must never be imported by `tierc7_rules`;
the dependency runs one way only.  Nothing is written at import time.

════════════════════════════════════════════════════════════════════════════
DELIVERABLE 1 · S-STOPGRID [D-R7] — THE INITIAL STOP, FOUR OFFSETS, RAIL KEPT
════════════════════════════════════════════════════════════════════════════
The grid is the INITIAL stop at `pivot + {-0.25, 0, +0.25, +0.50} ATR`, and the
offset is applied by the SHIPPED PROGRAM, not by this lab.  `T7.replay` already
carries it:

    stop_px = float(stp.stop_px)
    if card.stop_grid_offset_atr:
        cand = stop_px - d * card.stop_grid_offset_atr * atr_sig
        rail = entry_px - d * card.entry_rail_atr * atr_sig
        stop_px = min(cand, rail) if d == 1 else max(cand, rail)
    r_dist = abs(entry_px - stop_px)

READ IT IN THAT ORDER, BECAUSE THE ORDER IS THE WHOLE RULE.  The card's own
`struct_stop_4h` has ALREADY railed its stop at `entry_rail_atr` before this
block sees it.  The offset then moves that railed stop by `offset x ATR` IN THE
TRADE DIRECTION'S SIGN — for a long `- d * offset` means a POSITIVE offset
pushes the stop DOWN (wider) and a NEGATIVE offset pulls it UP (tighter) — and
the rail is then RE-IMPOSED on the result: `min(cand, rail)` for a long takes
whichever stop is FARTHER BELOW price, `max` mirrors it for a short.  So the
rail is a FLOOR ON DISTANCE applied AFTER the offset, and the consequence is
asymmetric and worth saying plainly:

    a POSITIVE offset always moves the stop, because a wider stop can never
    breach a floor on width;
    a NEGATIVE offset moves the stop ONLY where the card's stop was already
    wider than the rail, and is CLIPPED to exactly the rail everywhere else.

Measured on the corridor: at -0.25 ATR the rail binds on 71 of 196 campaigns
against 48 at offset 0, and the 48 campaigns whose net R is unchanged at -0.25
are EXACTLY the 48 that were already rail-bound at offset 0.  That is the
assertion this lab makes about the rail — a set identity over the book, not one
example — and it is what makes "RAIL RESPECTED" a checked claim rather than a
restatement of the code.

`offset = 0.0` is FALSY, so the block is skipped entirely and the cell is card
v6 by construction, not by arithmetic that happens to cancel.  F-SG-CTRL
asserts it campaign-for-campaign anyway.

THE GRID TOUCHES THE INITIAL STOP AND NOTHING ELSE.  The cards are card v6 with
one knob turned, so the ladder is still v6's `trail_step`, there is no weave, no
re-entry and no abort.  A cell's delta is therefore attributable to the entry
anchor alone.

IT IS A DIAGNOSTIC.  NO CELL MAY BE PROMOTED, and every row of
`stopgrid_table` carries a column saying so, because a four-cell grid whose best
cell is +4.5 R richer than the shipped card is exactly the object that gets
promoted by a reader who never saw the word "diagnostic".

════════════════════════════════════════════════════════════════════════════
DELIVERABLE 2 · L-ANCHOR — THE BAKE-OFF, AND WHAT IT IS NOT ALLOWED TO DECIDE
════════════════════════════════════════════════════════════════════════════
Five ladder anchors x two offsets = ten cells.  THIS INFORMS FUTURE TUNING
ONLY.  The scored hybrid uses the pre-named prior `max(pivot, e89)` at 0.5 ATR
and NEVER this table's winner — that sentence is a COLUMN on every row of
`anchor_bakeoff`, not a line in a document nobody reads next to the number.

THE LADDER IS PARAMETERISED HERE, IN THIS MODULE, AND `tierc7_rules` IS NOT
TOUCHED.  `_anchored_ladder_step` builds a drop-in replacement for
`RC.ladder_step` with the anchor opened up, and `_ladder_patched` binds it onto
`RC` for the duration of ONE `T7.replay` call and restores the original in a
`finally`.  The alternative — copying `T7._ride_leg`, `T7._ride_chain`,
`T7._account_chain` and `T7.replay` into this file so they could take a ladder
argument — is NOT taken, and it is not taken because a second copy of the ride
would make every cell of this table a claim about a different program.  Every
cell here is the SHIPPED ride, the SHIPPED accounting and the SHIPPED
bookkeeping, with one function swapped for the duration of one call.

THE OFFSET IS NOT PATCHED — IT IS CARDED.  `T7._ride_leg` passes
`buf_atr = RC.STOP_BUF_ATR + card.trail_extra_buf_atr` into the ladder, so a
cell at 0.25 ATR is `trail_extra_buf_atr = -0.25` and a cell at 0.50 ATR is
`trail_extra_buf_atr = 0.0`.  The 0.50 cells therefore ride a card that is
FIELD-IDENTICAL to `RC.CARD_LADDER_ONLY` apart from its name, and the patched
function receives the buffer the shipped code computed.

THE IDENTITY IS THE CONTROL, AND IT IS ASSERTED THREE WAYS.
`max(pivot, e89)` at 0.50 ATR IS `RC.ladder_step`, so that cell must reproduce
the unpatched ladder-only book EXACTLY.  Asserted:

  F-AN-ID    the patched book against the UNPATCHED `RC.CARD_LADDER_ONLY`
             book — 196 campaigns, every entry/stop/exit/net-R equal, and all
             229 `Advance` objects equal FIELD BY FIELD across all 13 fields.
  F-AN-CALL  a call-level sweep that does not depend on which bars the book
             happened to visit: EVERY confirming (2,2) fractal on the whole
             panel, both directions, four standing-stop levels drawn from the
             tape — 80,000-odd calls — patched against `RC.ladder_step`, every
             field equal and every refusal a refusal in both.
  F-AN-CLEAN `RC.ladder_step is` the original object after every table build.

F-AN-CALL exists because F-AN-ID alone is a check the ANCHOR could pass while
the REFUSAL paths differed: the book only ever visits the monotone-passing
branch on the bars it advanced.  The sweep drives all four standing-stop levels
through both functions, so the monotone refusal and the minimum-advance refusal
are exercised on the whole panel and not merely assumed to agree.

THE PIVOT GATE STAYS THE LADDER'S CLOCK IN EVERY CELL, AND THAT IS A READING.
`RC.ladder_step` only forms an anchor on a bar where a FAVOURABLE (2,2) fractal
confirms — e89 exists on every bar, the pivot does not.  Every cell of this
bake-off keeps that gate, including the cells whose anchor never mentions a
pivot.  THE ALTERNATIVE — letting an `e26` or `e89` anchor advance the stop on
EVERY bar — is NOT taken, because it changes the ladder's CADENCE as well as
its LEVEL, and a table that moved both could not say which one moved the
number.  The cost of the reading is stated too: an `e89` cell here is "the e89
level, sampled on pivot confirmations", not "an e89 trailing stop".

THE BAKE-OFF RIDES LADDER-ONLY, NOT THE FULL HYBRID.  The question is which
anchor the LADDER should use; running it inside the full hybrid would confound
the anchor with the weave and the re-entry, and would pair against a base whose
campaign set the chain has already changed.  THE ALTERNATIVE — riding the full
hybrid — is not taken for that reason, and it is named because a future reader
tuning the shipped card will want the hybrid number and must know this is not
it.

════════════════════════════════════════════════════════════════════════════
EVERY EMA CARRIES AN EXPLICIT WARM-UP FLOOR
════════════════════════════════════════════════════════════════════════════
`engine.indicators.ema` SEEDS AT THE SERIES START AND NEVER RETURNS NaN.  This
estate has repaired that defect four times.  Every series this module reads —
e26, e89 and both edges of the M band — is NULLED below its own length, and the
M band is nulled below its LONGEST member (127), because a band is not defined
while only some of its members are warm.

The floors are applied to a COPY (`np.where`), never in place: `f.e26` and
`f.e89` are the program's own arrays and a lab that NaN'd them would poison the
decision path for every later caller in the process.

The floors are also PROVED INERT rather than assumed so: F-AN-WARM asserts each
floor is present and F-AN-FLOOR asserts the earliest ladder call anywhere in
the ten cells sits at a bar far beyond the deepest floor.  A warm-up floor that
silently changed a shipped number would be a repair that broke the thing it
repaired.
"""
from __future__ import annotations

import dataclasses
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc7 as T7                                                   # noqa: E402
import tierc7_rules as RC                                             # noqa: E402

# THE ORIGINAL, CAPTURED AT IMPORT.  A READ, not a write — and the object every
# restore and every `is` check compares against.
_RC_LADDER_STEP = RC.ladder_step

# ═══════════════════════════════════════════════ THE TWO GRIDS, NAMED UP FRONT
STOP_OFFSETS: tuple[float, ...] = (-0.25, 0.0, 0.25, 0.50)
ANCHORS: tuple[str, ...] = ("pivot(2,2)", "e26", "e89", "M-band-edge",
                            "max(pivot,e89)")
ANCHOR_OFFSETS: tuple[float, ...] = (0.25, 0.50)

# D-R2's pre-named prior — the cell that IS the shipped ladder.
PRIOR_ANCHOR: str = "max(pivot,e89)"
PRIOR_OFFSET: float = 0.50

NO_PROMOTION = (
    "DIAGNOSTIC [D-R7] — NO CELL MAY BE PROMOTED. The scored card's initial "
    "stop is the card's own railed structural stop (offset 0.00 ATR). This "
    "grid measures what the other offsets would have done and decides "
    "nothing; its best cell is not a rung and is not a candidate.")

NEVER_THE_WINNER = (
    "INFORMS FUTURE TUNING ONLY. The scored hybrid uses the pre-named prior "
    "max(pivot,e89) at 0.5 ATR and NEVER this table's winner.")

# EMA WARM-UP FLOORS, one per series this module reads.  `ind.ema` never
# returns NaN, so a floor that is not written here does not exist.
WARMUP_FLOOR: dict[str, int] = {
    "e26": 26,                          # f.e26 IS ind.ema(f.c, 26)
    "e89": int(RC.TIDE_FAST),           # f.e89 IS ind.ema(f.c, 89)
    "M": int(max(RC.RIBBONS["M"])),     # the band's LONGEST member, 127
}

_TOL = 1e-9                    # price tolerance for a rail comparison
_ADV_FIELDS: tuple[str, ...] = tuple(f.name
                                     for f in dataclasses.fields(RC.Advance))

_SERIES: dict[str, dict] = {}
_BOOKS: dict[tuple, list] = {}


# ═══════════════════════════════════════════════════ THE SERIES, FLOORED, ONCE
def anchor_series(sym: str) -> dict:
    """The four anchor levels for one asset, each with an EXPLICIT WARM-UP
    FLOOR, computed once and cached.

    `e26` and `e89` are TAKEN FROM THE FRAME, not recomputed: `RC.build_4h`
    builds them as `ind.ema(c, 26)` and `ind.ema(c, 89)` on exactly
    `frame(sym)["f"].c`, so the frame's arrays ARE those calls' output and a
    second call here would be a second implementation of one number.  The M
    band comes from `RC.ribbon_band(c, "M")`, which is the estate's own band
    object (`V5.ribbon_band`), and is floored at the band's LONGEST member.

    THE FLOOR IS APPLIED TO A COPY.  `np.where` returns a new array; writing
    `arr[idx < n] = np.nan` would NaN the program's own `f.e26`/`f.e89` for
    every later caller in the process.

    WHAT WOULD MAKE THIS WRONG: trusting `ind.ema` to return NaN while unwarm
    (it seeds at the series start and never does — the defect this estate has
    repaired four times); flooring the M band at its SHORTEST member, which
    would publish a band two of whose three EMAs are still seeded; mutating the
    frame's arrays in place; or floors deep enough to bite a bar the ladder can
    actually be called on, which F-AN-FLOOR refuses.
    """
    if sym in _SERIES:
        return _SERIES[sym]
    f = T7.frame(sym)["f"]
    idx = np.arange(len(f.c))
    m_lo_raw, m_hi_raw = RC.ribbon_band(f.c, "M")
    _SERIES[sym] = {
        "e26": np.where(idx >= WARMUP_FLOOR["e26"], f.e26, np.nan),
        "e89": np.where(idx >= WARMUP_FLOOR["e89"], f.e89, np.nan),
        "m_lo": np.where(idx >= WARMUP_FLOOR["M"], m_lo_raw, np.nan),
        "m_hi": np.where(idx >= WARMUP_FLOOR["M"], m_hi_raw, np.nan),
    }
    return _SERIES[sym]


def _anchor_px(anchor: str, sr: dict, j: int, direction: int,
               pivot_val: float) -> float:
    """ONE CELL'S ANCHOR LEVEL AT BAR j.  NaN means 'no anchor' and the caller
    refuses the advance.

    "MAX" IS DIRECTIONAL AND THAT IS THE WHOLE OF D-R2's MIRROR.  For a long
    the HIGHER of pivot and e89 is the TIGHTER — the one closer to price — so
    `max` tracks whichever of structure and tide is doing more work; for a
    short the mirror is `min`.  Writing `max` for both would take the anchor
    FARTHER from price on every short, which is the opposite rule.

    THE M-BAND EDGE IS THE TRADE-SIDE EDGE: the band's LOW for a long (the
    support the position leans on) and its HIGH for a short.  The far edge
    would put the stop on the wrong side of the band's own width.

    NON-FINITE INPUTS ARE REFUSED BEFORE THE ARITHMETIC, because Python's
    builtin `max(1.0, nan)` returns 1.0 — a NaN anchor would silently become a
    pivot anchor instead of a refusal.

    WHAT WOULD MAKE THIS WRONG: `max` on both sides; the far band edge; letting
    a NaN through `max`/`min`; or reading the series at a bar other than the
    confirming bar j.
    """
    if anchor == "pivot(2,2)":
        return float(pivot_val)
    if anchor == "e26":
        return float(sr["e26"][j])
    if anchor == "e89":
        return float(sr["e89"][j])
    if anchor == "M-band-edge":
        return float(sr["m_lo"][j] if direction == 1 else sr["m_hi"][j])
    if anchor == "max(pivot,e89)":
        e = float(sr["e89"][j])
        if not (np.isfinite(e) and np.isfinite(pivot_val)):
            return float("nan")
        return (max(float(pivot_val), e) if direction == 1
                else min(float(pivot_val), e))
    raise SystemExit(f"HALT: unknown ladder anchor {anchor!r}")


# ══════════════════════════════════ THE LOCAL LADDER — RC.ladder_step, OPENED
def _anchored_ladder_step(anchor: str, sr: dict):
    """Build a drop-in replacement for `RC.ladder_step` with the anchor opened.

    THE SIGNATURE, THE GATE ORDER AND THE RETURNED RECORD ARE `RC.ladder_step`'s
    — deliberately, because that is what makes the reduction checkable: with
    `anchor = "max(pivot,e89)"` and the shipped buffer this function must be
    the shipped function, field for field, on every call.  `T7._ride_leg` looks
    `RC.ladder_step` up on the module at call time, so binding this in place of
    it puts the whole SHIPPED ride and the SHIPPED accounting behind every cell
    of the bake-off.

    THE PIVOT GATE IS KEPT IN EVERY CELL.  An anchor is formed only on a bar
    where a favourable (2,2) fractal confirms, even for anchors that never
    mention a pivot — see the module docstring: opening the cadence as well as
    the level would make the table unreadable.

    Then, unchanged from the shipped ladder: the seal mask on the pivot's own
    bar, railed at `rail_atr` from the CONFIRMING CLOSE, ADVANCE-ONLY, and
    refused if the STOP would move less than `min_advance_atr` — measured on
    `abs(new_stop - prev_stop) / atr`, which is the quantity the ratchet ledger
    publishes as `advance_atr`.

    `pivot_val` ON THE RETURNED `Advance` CARRIES THE ANCHOR, NOT THE FRACTAL,
    exactly as `RC.ladder_step` does — the field is the level the stop was
    derived from, and on the identity cell the two definitions agree by
    construction.  `pivot_bar` still carries the confirming fractal's own bar,
    because that is the bar the seal mask was tested against.

    WHAT WOULD MAKE THIS WRONG: advancing on a bar with no confirming pivot;
    dropping the seal mask (`forbidden`) that the shipped ladder threads;
    measuring the minimum advance on the ANCHOR move rather than the STOP move
    (a large anchor move can leave a railed stop unchanged); letting the stop
    retreat; or reordering the gates, which would make the reduction to
    `RC.ladder_step` a coincidence of the tape rather than an identity.
    """

    def step(fr, j: int, direction: int, cur_stop: float, close: float,
             atr: float, e89: float, open_ms: np.ndarray,
             buf_atr: float = RC.STOP_BUF_ATR,
             rail_atr: float = RC.MIN_STOP_ATR,
             min_advance_atr: float = 0.05,
             forbidden: np.ndarray | None = None):
        """ONE BAR OF THE ANCHORED LADDER.  Returns the Advance, or None.

        WHAT WOULD MAKE THIS WRONG: any divergence from `RC.ladder_step`'s gate
        ORDER or returned record — see the factory's docstring. The `e89`
        argument is accepted and deliberately unused: this function reads e89
        from its own WARM-FLOORED series, because `f.e89` as the shipped ladder
        receives it is seeded at the series start and never NaN.
        """
        src = fr.low_by_conf if direction == 1 else fr.high_by_conf
        hit = src.get(int(j))
        if hit is None:
            return None
        pv, pbar = hit
        if forbidden is not None and bool(forbidden[pbar]):
            return None
        if not (np.isfinite(atr) and atr > 0 and np.isfinite(close)):
            return None
        a = _anchor_px(anchor, sr, int(j), direction, float(pv))
        if not np.isfinite(a):
            return None
        if direction == 1:
            cand = a - buf_atr * atr
            rail = close - rail_atr * atr
            admitted = min(cand, rail)               # the FARTHER stop below
            rail_bound = rail < cand
            if RC.RATCHET_MONOTONE and not (admitted > cur_stop):
                return None
        else:
            cand = a + buf_atr * atr
            rail = close + rail_atr * atr
            admitted = max(cand, rail)               # the FARTHER stop above
            rail_bound = rail > cand
            if RC.RATCHET_MONOTONE and not (admitted < cur_stop):
                return None
        if min_advance_atr > 0.0:
            if abs(admitted - cur_stop) / atr < min_advance_atr:
                return None
        return RC.Advance(
            conf_i=int(j), conf_ms=int(open_ms[j]), pivot_val=float(a),
            pivot_bar=int(pbar), pivot_bar_ms=int(open_ms[pbar]),
            atr=float(atr), close=float(close), cand_px=float(cand),
            rail_px=float(rail), new_stop=float(admitted),
            prev_stop=float(cur_stop), rail_binding=bool(rail_bound),
            dist_from_close_over_atr=float(abs(close - admitted) / atr))

    return step


@contextmanager
def _ladder_patched(step):
    """Bind `step` onto `RC.ladder_step` for the duration of ONE replay and put
    the original back, whatever happens.

    THE PATCH IS SCOPED, RESTORED IN A `finally`, AND CHECKED AFTERWARDS.
    `tierc7_rules.py` is NOT edited and no file is written; what is swapped is a
    module attribute for the length of one call, which is the only way to put
    an alternative anchor behind the SHIPPED ride without forking it.
    F-AN-CLEAN asserts `RC.ladder_step is` the original after every table this
    module builds, so a leaked patch is a reported failure and not a silent one.

    WHAT WOULD MAKE THIS WRONG: restoring to whatever was bound at entry rather
    than to the object captured at import (a nested patch would then restore a
    patch); leaving the swap in place across a call this lab does not own; or
    patching around `T7.run_cell`, which rides the whole universe and would put
    one asset's anchor series behind every asset's ride.
    """
    RC.ladder_step = step
    try:
        yield
    finally:
        RC.ladder_step = _RC_LADDER_STEP


# ═══════════════════════════════════════════════════════════════ THE BOOKS
def _stopgrid_card(offset: float) -> RC.Card:
    """Card v6 with the initial-stop offset turned, and NOTHING else.

    WHAT WOULD MAKE THIS WRONG: turning a second knob (the cell's delta would
    stop being the entry anchor's), or building on a card other than the v6
    default — `RC.Card()` with no arguments IS card v6, which is what makes the
    0.00 cell a control rather than a coincidence.
    """
    return RC.Card(name=f"S-STOPGRID offset {offset:+.2f} ATR",
                   stop_grid_offset_atr=float(offset))


def _anchor_card(anchor: str, offset: float) -> RC.Card:
    """The ladder-only card at one bake-off offset.

    The offset rides `trail_extra_buf_atr` because `T7._ride_leg` passes
    `RC.STOP_BUF_ATR + card.trail_extra_buf_atr` into the ladder — so at 0.50
    ATR the card is field-identical to `RC.CARD_LADDER_ONLY` apart from `name`,
    which is what F-AN-CARD asserts.

    WHAT WOULD MAKE THIS WRONG: setting `trail_extra_buf_atr` to the offset
    itself rather than to `offset - RC.STOP_BUF_ATR` (every cell's buffer would
    be 0.5 too wide and the 0.50 cell would silently stop being the shipped
    card); or turning `weave`/`reentry` on, which would confound the anchor
    with rules the bake-off is not about.
    """
    return RC.Card(name=f"L-ANCHOR {anchor} @ {offset:.2f} ATR",
                   hybrid_anchor=True,
                   trail_extra_buf_atr=float(offset) - RC.STOP_BUF_ATR)


def stopgrid_book(offset: float, lo_ms: int, hi_ms: int) -> list:
    """One S-STOPGRID cell's campaigns, from the SHIPPED `T7.run_cell`.

    WHAT WOULD MAKE THIS WRONG: applying the offset here instead of letting
    `T7.replay` apply it (this lab would then be measuring its own arithmetic);
    or caching across corridors — the key carries `lo_ms`/`hi_ms` so it cannot.
    """
    key = ("sg", float(offset), int(lo_ms), int(hi_ms))
    if key not in _BOOKS:
        _BOOKS[key] = T7.run_cell(_stopgrid_card(offset), lo_ms, hi_ms)
    return _BOOKS[key]


def anchor_book(anchor: str, offset: float, lo_ms: int, hi_ms: int) -> list:
    """One L-ANCHOR cell's campaigns: the SHIPPED ride, one function swapped.

    The patch is applied PER ASSET, around a single `T7.replay`, because the
    anchor series are per-asset: patching around `T7.run_cell` would put one
    asset's arrays behind every asset's ride.

    WHAT WOULD MAKE THIS WRONG: patching around the whole universe; forgetting
    that `T7.replay` is what `run_cell` calls (a fork here would be a second
    program); or leaving the patch bound after the call, which `_ladder_patched`
    refuses and F-AN-CLEAN checks.
    """
    key = ("an", str(anchor), float(offset), int(lo_ms), int(hi_ms))
    if key in _BOOKS:
        return _BOOKS[key]
    card = _anchor_card(anchor, offset)
    out: list = []
    for sym in RC.UNIVERSE:
        step = _anchored_ladder_step(anchor, anchor_series(sym))
        with _ladder_patched(step):
            _, tr = T7.replay(sym, card, lo_ms, hi_ms)
        out += tr
    _BOOKS[key] = out
    return out


def ladder_only_book(lo_ms: int, hi_ms: int) -> list:
    """The UNPATCHED `RC.CARD_LADDER_ONLY` book — the identity's control.

    WHAT WOULD MAKE THIS WRONG: building it while a patch is bound (the control
    would be the thing it is meant to check), or reaching it through
    `anchor_book`, which patches by construction. It goes through
    `T7.run_cell` on the shipped card and nothing else.
    """
    key = ("ctrl-ladder", int(lo_ms), int(hi_ms))
    if key not in _BOOKS:
        _BOOKS[key] = T7.run_cell(RC.CARD_LADDER_ONLY, lo_ms, hi_ms)
    return _BOOKS[key]


# ═════════════════════════════════════════════════════════ THE RAIL, AUDITED
def rail_audit(book: list, rail_atr: float) -> dict:
    """DID THE RAIL HOLD ON EVERY CAMPAIGN OF THIS CELL?

    The claim is `|entry - stop| >= entry_rail_atr x ATR(entry bar)` for EVERY
    campaign, and it is reported as a COUNT over the whole cell — violations
    out of campaigns checked — because a rail check satisfied by one campaign
    is not a check.

    `n_rail_bound` counts the campaigns sitting EXACTLY on the rail, and it is
    published beside the violation count for a reason: a rail that never binds
    is a rail nothing has tested, and a cell reporting "0 violations, 0 bound"
    has proved only that its offset never pushed anything against the floor.

    THE QUANTITY IS THE PROGRAM'S OWN.  `t.r_dist` is what `T7.replay` divided
    by to make every R in the book, and `t.atr_at_entry` is the ATR it used to
    build the rail; re-deriving either from the tape here would compare the
    program to a second copy of itself.

    WHAT WOULD MAKE THIS WRONG: reporting a share instead of a count; running
    on an empty book (a vacuous pass, refused below); comparing against a rail
    built from a different bar's ATR; or a tolerance loose enough to swallow a
    real breach — `_TOL` is 1e-9 in PRICE units against distances of order 1e2.
    """
    n = len(book)
    if n == 0:
        return {"campaigns_checked": 0, "rail_violations": 0,
                "rail_respected": False, "n_rail_bound": 0,
                "min_stop_dist_over_atr": None,
                "rail_note": "EMPTY CELL — a rail claim over no campaigns is "
                             "vacuous and is reported as NOT RESPECTED."}
    dist = np.array([float(t.r_dist) for t in book])
    atr = np.array([float(t.atr_at_entry) for t in book])
    rail = float(rail_atr) * atr
    viol = int(np.sum(dist < rail - _TOL))
    bound = int(np.sum(np.abs(dist - rail) <= _TOL))
    return {"campaigns_checked": n, "rail_violations": viol,
            "rail_respected": bool(viol == 0),
            "n_rail_bound": bound,
            "min_stop_dist_over_atr": T7.r6(float(np.min(dist / atr))),
            "rail_note": (f"|entry-stop| >= {rail_atr:.2f} x ATR(entry) on "
                          f"{n - viol}/{n} campaigns; {bound} sit exactly on "
                          f"the rail.")}


def _rail_bound_keys(book: list, rail_atr: float) -> set:
    """The keys of the campaigns whose stop sits EXACTLY on the rail.

    WHAT WOULD MAKE THIS WRONG: an inequality instead of an equality (every
    campaign is at least on the rail, so `>=` would return the whole book and
    F-SG-CLIP's set identity would pass on nothing); or a tolerance loose
    enough to sweep in campaigns the pivot placed just beyond it.
    """
    return {_key(t) for t in book
            if abs(float(t.r_dist) - rail_atr * float(t.atr_at_entry)) <= _TOL}


def _key(t) -> tuple:
    """The pairing key: asset, LANE and entry bar.

    WHAT WOULD MAKE THIS WRONG: dropping the lane. Two lanes can enter the same
    asset on the same bar, and a key that collided them would silently pair one
    campaign against another.
    """
    return (t.symbol, t.lane, int(t.entry_ms))


# ═════════════════════════════════════════════════ THE IDENTITY, FIELD BY FIELD
def _adv_mismatch(a, b) -> list[str]:
    """Which of `Advance`'s fields differ between two advances, EXACTLY.

    Equality is EXACT, not tolerant: both functions run the same arithmetic in
    the same order on the same floats, so the results are bit-identical or the
    reduction claim is false.  NaN is treated as equal to NaN so a field that
    is legitimately absent in both does not read as a difference.

    WHAT WOULD MAKE THIS WRONG: a tolerance (it would hide a real divergence in
    the anchor); comparing a hand-written field list instead of
    `dataclasses.fields(RC.Advance)`, which would silently stop checking any
    field a future tier adds.
    """
    out = []
    for fld in _ADV_FIELDS:
        x, y = getattr(a, fld), getattr(b, fld)
        if isinstance(x, float) and isinstance(y, float):
            if np.isnan(x) and np.isnan(y):
                continue
        if x != y:
            out.append(fld)
    return out


def identity_book(lo_ms: int, hi_ms: int) -> dict:
    """F-AN-ID · THE PATCHED PRIOR CELL AGAINST THE UNPATCHED SHIPPED LADDER.

    Two books over the same corridor: `anchor_book(max(pivot,e89), 0.50)` and
    the unpatched `RC.CARD_LADDER_ONLY`.  Compared: the campaign KEY SET, then
    per campaign the entry price, the initial stop, R, the exit bar, the exit
    price, the exit reason and net R, then EVERY `Advance` field by field.

    THE ADVANCE COUNT IS PUBLISHED, because "0 mismatches" over 0 advances is
    not an identity.  If the two books disagree on which campaigns they hold,
    that is reported as an unpaired count rather than silently intersected.

    WHAT WOULD MAKE THIS WRONG: comparing only the headline net R (two ladders
    can reach the same total by different advances); intersecting the key sets
    and calling the result a match; or comparing advances positionally without
    first asserting the two lists are the same length.
    """
    new = anchor_book(PRIOR_ANCHOR, PRIOR_OFFSET, lo_ms, hi_ms)
    ref = ladder_only_book(lo_ms, hi_ms)
    kn = {_key(t): t for t in new}
    kr = {_key(t): t for t in ref}
    bad: list[str] = []
    n_adv = 0
    n_fields = 0
    for k in sorted(set(kn) | set(kr)):
        a, b = kn.get(k), kr.get(k)
        if a is None or b is None:
            bad.append(f"{k}: present in only one book")
            continue
        for fld in ("entry_px", "stop_px", "r_dist", "exit_i", "exit_ms",
                    "exit_px", "exit_reason", "net_r", "final_stop_px"):
            if getattr(a, fld) != getattr(b, fld):
                bad.append(f"{k}: {fld} {getattr(a, fld)!r} != "
                           f"{getattr(b, fld)!r}")
        if len(a.advances) != len(b.advances):
            bad.append(f"{k}: {len(a.advances)} advances != {len(b.advances)}")
            continue
        for x, y in zip(a.advances, b.advances):
            n_adv += 1
            n_fields += len(_ADV_FIELDS)
            for fld in _adv_mismatch(x, y):
                bad.append(f"{k}: Advance.{fld} {getattr(x, fld)!r} != "
                           f"{getattr(y, fld)!r}")
    return {"campaigns_compared": len(set(kn) | set(kr)),
            "campaigns_in_both": len(set(kn) & set(kr)),
            "advances_compared": n_adv,
            "advance_fields_compared": n_fields,
            "advance_field_names": list(_ADV_FIELDS),
            "mismatches": len(bad),
            "identical": bool(not bad and n_adv > 0 and len(kn) == len(kr)
                              and len(kn) > 0),
            "examples": bad[:5]}


def identity_calls(lo_ms: int, hi_ms: int) -> dict:
    """F-AN-CALL · THE SAME IDENTITY, DRIVEN OFF THE BOOK'S CHOICES.

    F-AN-ID only ever exercises the bars the ladder-only book actually rode,
    and only the branch on which the advance was TAKEN.  This leg calls both
    functions directly on EVERY confirming (2,2) fractal on the whole panel, in
    BOTH directions, at FOUR standing-stop levels drawn from the tape
    (`close - k x ATR` for a long, mirrored for a short) — so the monotone
    refusal and the minimum-advance refusal are exercised too, and a refusal in
    one function is required to be a refusal in the other.

    THE SWEEP STARTS AT `WARMUP_BARS + 1` BECAUSE THAT IS THE FIRST BAR THE
    PROGRAM CAN EVER CALL THE LADDER ON: `T7.replay` floors its entry index at
    `RC.WARMUP_BARS` (316) and the ladder governs bar j+1 of a campaign that
    began no earlier than there.  The floors in `WARMUP_FLOOR` are all far
    shallower than 316 — F-AN-FLOOR asserts exactly that — so the restriction
    cannot be hiding a bar where this module's floors and the shipped
    function's unfloored e89 would disagree.

    WHAT WOULD MAKE THIS WRONG: sweeping only the bars the book visited (that
    is F-AN-ID and it is a different, weaker leg); one standing-stop level
    (which would exercise one branch); counting a both-None call as a
    comparison without counting how many were not None, which would let an
    all-refusing patch pass.
    """
    step_by_sym = {s: _anchored_ladder_step(PRIOR_ANCHOR, anchor_series(s))
                   for s in RC.UNIVERSE}
    n_calls = n_adv = n_both_none = n_fields = 0
    bad: list[str] = []
    j0 = int(RC.WARMUP_BARS) + 1
    for sym in RC.UNIVERSE:
        st = T7.frame(sym)
        f = st["f"]
        fr = T7.fractals(sym, RC.RATCHET_PIVOT_L, RC.RATCHET_PIVOT_R)
        step = step_by_sym[sym]
        for direction in (1, -1):
            src = fr.low_by_conf if direction == 1 else fr.high_by_conf
            for j in sorted(int(x) for x in src):
                if j < j0 or j >= len(f.c):
                    continue
                close, atr = float(f.c[j]), float(f.atr[j])
                e89 = float(f.e89[j])
                if not (np.isfinite(atr) and atr > 0):
                    continue
                for k in (0.5, 1.0, 1.5, 3.0):
                    cur = close - direction * k * atr
                    got = step(fr, j, direction, cur, close, atr, e89,
                               f.open_ms, buf_atr=RC.STOP_BUF_ATR,
                               rail_atr=RC.MIN_STOP_ATR,
                               min_advance_atr=0.05, forbidden=None)
                    want = _RC_LADDER_STEP(fr, j, direction, cur, close, atr,
                                           e89, f.open_ms,
                                           buf_atr=RC.STOP_BUF_ATR,
                                           rail_atr=RC.MIN_STOP_ATR,
                                           min_advance_atr=0.05,
                                           forbidden=None)
                    n_calls += 1
                    if got is None and want is None:
                        n_both_none += 1
                        continue
                    if (got is None) != (want is None):
                        bad.append(f"{sym} j={j} d={direction} k={k}: "
                                   f"{'patched' if got is None else 'shipped'}"
                                   f" refused, the other did not")
                        continue
                    n_adv += 1
                    n_fields += len(_ADV_FIELDS)
                    for fld in _adv_mismatch(got, want):
                        bad.append(f"{sym} j={j} d={direction} k={k}: "
                                   f"Advance.{fld}")
    return {"calls": n_calls, "advances_returned": n_adv,
            "both_refused": n_both_none, "advance_fields_compared": n_fields,
            "mismatches": len(bad),
            "identical": bool(not bad and n_calls > 0 and n_adv > 0
                              and n_both_none > 0),
            "examples": bad[:5]}


# ══════════════════════════════════════════════════════ ONE ROW OF EITHER GRID
def _cell_row(book: list, base: list, label: str) -> dict:
    """The aggregate, the D15 trio and the LOAO-3/5 line for one cell.

    D15 RIDES THE ROW AND GATES NOTHING — the operator's word of record. The
    LOAO line comes from `T7.loao`, which is the estate's own 5-panel object;
    computing a leave-one-asset-out here would be a second implementation of
    the E1 law.

    THE LOAO LINE IS SPLIT BY SIGN, AND THAT IS A READING REPAIR.  `T7.loao`
    counts a panel as excluding zero when `ci_lo > 0 OR ci_hi < 0` — the E1 law
    is about ROBUSTNESS, not direction, and on a registration arm the two are
    the same thing because the arm is only ever proposed as an improvement.  On
    a DIAGNOSTIC GRID they are not: the +0.25 and +0.50 cells here clear 5 of 5
    panels BELOW zero, and "5/5" printed alone is a line a reader will take for
    a pass.  `loao_excludes_zero_below` and `loao_sign_note` are added so the
    direction cannot be lost, and the panels themselves are the shipped
    function's — nothing is recomputed.

    WHAT WOULD MAKE THIS WRONG: reading any D15 column as a threshold; reading
    `loao_line` without its sign on a grid that contains losing cells; dropping
    the provisional flag on a thin cell; or pairing on (asset, entry_ms) while
    the book holds two lanes, which would collide two campaigns onto one key.
    """
    row = T7.agg(book, label)
    # `agg` names its label `group` and stamps a constant `key = "ALL"`. Both
    # are dropped: `cell` IS this table's declared key, and shipping a column
    # literally called `key` that is NOT the key is a trap for the next reader.
    row.pop("group", None)
    row.pop("key", None)
    row["cell"] = label
    row.update(T7.d15(book, base))
    lo_ = T7.loao(book, base, label)
    row.update({k: v for k, v in lo_.items() if not k.startswith("_")})
    above = sum(1 for p in lo_["_per"]
                if p["ci_lo"] is not None and p["ci_lo"] > 0)
    below = sum(1 for p in lo_["_per"]
                if p["ci_hi"] is not None and p["ci_hi"] < 0)
    row["loao_excludes_zero_above"] = above
    row["loao_excludes_zero_below"] = below
    row["loao_sign_note"] = (
        f"{lo_['loao_line']} panels exclude zero: {above} ABOVE it, {below} "
        f"BELOW it. A cell whose panels exclude zero BELOW it is robustly "
        f"WORSE than card v6 — the LOAO line is a robustness count, not a "
        f"verdict, and on a diagnostic grid it must be read with its sign.")
    row["provisional"] = bool(len(book) < RC.PROVISIONAL_MIN_N)
    row["d15_gates_nothing"] = True
    return row


# ══════════════════════════════════════════════════════════════ DELIVERABLE 1
def stopgrid_table(lo_ms: int, hi_ms: int, base: list) -> pd.DataFrame:
    """S-STOPGRID [D-R7] — FOUR CELLS, REPORTED WHOLE, PROMOTED NEVER.

    One row per offset in {-0.25, 0, +0.25, +0.50} ATR, each with the D15 trio
    (`paired_delta_expectancy_r`, `tail_exit_ratio`,
    `max_single_trade_delta_share`), the LOAO-3/5 line from `T7.loao`, and the
    rail audit — `rail_violations`, `n_rail_bound`, `min_stop_dist_over_atr`.

    THE RAIL IS ASSERTED, NOT DESCRIBED.  Every campaign of every cell must
    satisfy `|entry - stop| >= entry_rail_atr x ATR(entry bar)`; a single
    violation HALTS this build rather than printing a table with a column that
    says so quietly.  The counts are published anyway, so a reader sees how
    many campaigns the claim rests on and how many actually sat on the floor.

    NO CELL MAY BE PROMOTED.  `promotable` is False on every row and
    `promotion_rule` carries the sentence.

    WHAT WOULD MAKE THIS WRONG: dropping a cell (the grid is reported WHOLE —
    the negative cells are the point); gating on any D15 column; letting the
    rail assertion pass on an empty cell; or reporting the 0.00 cell as
    anything other than card v6, which F-SG-CTRL checks campaign for campaign.
    """
    rail_atr = float(RC.Card().entry_rail_atr)
    rows = []
    for off in STOP_OFFSETS:
        book = stopgrid_book(off, lo_ms, hi_ms)
        au = rail_audit(book, rail_atr)
        if not au["rail_respected"]:
            raise SystemExit(
                f"HALT (S-STOPGRID): the entry rail was BREACHED in cell "
                f"{off:+.2f} ATR — {au['rail_violations']} of "
                f"{au['campaigns_checked']} campaigns hold "
                f"|entry-stop| < {rail_atr} x ATR. The offset must never "
                f"produce a stop tighter than the card's own floor.")
        row = _cell_row(book, base, f"offset {off:+.2f} ATR")
        row.update({
            "offset_atr": float(off),
            "entry_rail_atr": rail_atr,
            "is_the_scored_card": bool(off == 0.0),
            **au,
        })
        rows.append(row)
    d = pd.DataFrame(rows)
    d["scored"] = False
    d["promotable"] = False
    d["promotion_rule"] = NO_PROMOTION
    d["tier"] = "diagnostic — UNSCORED, gates nothing, promotes nothing"
    d["grid_reported_whole"] = True
    d["selection_surface"] = False
    d["offset_applied_by"] = ("tierc7.replay — card.stop_grid_offset_atr, "
                              "rail re-imposed after the offset")
    d["in_sample"] = True
    front = ["cell", "offset_atr", "n", "net_r", "expectancy_r",
             "win_rate_pct", "rail_respected", "rail_violations",
             "n_rail_bound", "min_stop_dist_over_atr", "promotable"]
    return d[front + [c for c in d.columns if c not in front]]


# ══════════════════════════════════════════════════════════════ DELIVERABLE 2
def anchor_bakeoff(lo_ms: int, hi_ms: int, base: list) -> pd.DataFrame:
    """L-ANCHOR — TEN CELLS, AND A SENTENCE ON EVERY ONE OF THEM.

    Anchors {pivot(2,2), e26, e89, M-band-edge, max(pivot,e89)} x offsets
    {0.25, 0.50} ATR, each ridden by the SHIPPED ride with the local
    anchor-parameterised ladder bound in place of `RC.ladder_step`.

    THE IDENTITY IS ASSERTED BEFORE ANY CELL IS REPORTED.  `max(pivot,e89)` at
    0.50 ATR must reproduce the unpatched `RC.CARD_LADDER_ONLY` book exactly —
    every campaign, every `Advance`, field by field — and a mismatch HALTS.
    Without that control this table would be ten numbers from an unverified
    ladder, and its `pivot(2,2)` cell would look like a v6 comparison it had
    not earned.

    EVERY ROW CARRIES `informs_future_tuning_only`.  The scored hybrid uses the
    pre-named prior `max(pivot,e89)` at 0.5 ATR and NEVER this table's winner.

    WHAT WOULD MAKE THIS WRONG: reporting fewer than ten cells; ranking the
    cells or emitting a "best" row (there is none, by construction); scoring
    any cell against zero; letting the identity be assumed rather than
    asserted; or comparing these cells against the FULL HYBRID's base — they
    ride ladder-only, and the row says so.
    """
    ident = identity_book(lo_ms, hi_ms)
    if not ident["identical"]:
        raise SystemExit(
            f"HALT (L-ANCHOR): the local ladder does NOT reduce to "
            f"RC.ladder_step on the {PRIOR_ANCHOR} / {PRIOR_OFFSET} cell — "
            f"{ident['mismatches']} mismatch(es) over "
            f"{ident['advances_compared']} advances. e.g. {ident['examples']}")
    rows = []
    for anchor in ANCHORS:
        for off in ANCHOR_OFFSETS:
            book = anchor_book(anchor, off, lo_ms, hi_ms)
            label = f"{anchor} @ {off:.2f} ATR"
            row = _cell_row(book, base, label)
            is_prior = bool(anchor == PRIOR_ANCHOR and off == PRIOR_OFFSET)
            row.update({
                "anchor": anchor,
                "offset_atr": float(off),
                "is_the_pre_named_prior": is_prior,
                "reduces_to_rc_ladder_step": is_prior,
                "identity_campaigns_compared": (
                    int(ident["campaigns_compared"]) if is_prior else None),
                "identity_advances_compared": (
                    int(ident["advances_compared"]) if is_prior else None),
                "identity_advance_fields_compared": (
                    int(ident["advance_fields_compared"]) if is_prior
                    else None),
                "identity_mismatches": (int(ident["mismatches"]) if is_prior
                                        else None),
                "n_advances": sum(len(t.advances) for t in book),
                "n_advances_rail_bound": sum(
                    1 for t in book for a in t.advances if a.rail_binding),
                "n_ratchet_exits": sum(1 for t in book if t.ratchet_exit),
            })
            rows.append(row)
    d = pd.DataFrame(rows)
    d["informs_future_tuning_only"] = NEVER_THE_WINNER
    d["scored"] = False
    d["promotable"] = False
    d["selection_surface"] = False
    d["grid_reported_whole"] = True
    d["rides"] = ("ladder-only (card v6 + hybrid_anchor) — NOT the full "
                  "hybrid; the weave and the re-entry are OFF so a cell's "
                  "delta is the anchor's")
    d["pivot_gate_kept"] = ("every cell advances only on a confirming (2,2) "
                            "fractal — the anchor's LEVEL is swept, its "
                            "CADENCE is not")
    d["in_sample"] = True
    front = ["cell", "anchor", "offset_atr", "n", "net_r", "expectancy_r",
             "win_rate_pct", "is_the_pre_named_prior",
             "reduces_to_rc_ladder_step", "informs_future_tuning_only"]
    return d[front + [c for c in d.columns if c not in front]]


# ═══════════════════════════════════════════ THE CHECKS, AS CARDINALITIES
def _leg(name: str, claim: str, ok: bool, cardinality: str,
         detail: str = "") -> dict:
    """One self-check row: the claim, the COUNT it rests on, and pass/fail.

    WHAT WOULD MAKE THIS WRONG: a `cardinality` that is prose rather than a
    count — the whole point of the column is that a reader can see how many
    objects the claim was checked against, so "the rail held" without
    "784/784" is a leg that could be passing on one campaign.
    """
    return {"leg": name, "claim": claim, "cardinality": cardinality,
            "detail": detail, "passed": bool(ok)}


def selfcheck() -> pd.DataFrame:
    """EVERY LEG THIS MODULE RESTS ON, RUN AND REPORTED — pass or fail.

    The table builders HALT on a broken invariant; this function REPORTS every
    leg's status instead, so a reader sees the whole board rather than the
    first failure.  It takes no arguments and fetches its own corridor and its
    own v6 control book, because a self-check that depended on the caller's
    inputs could be handed the inputs that make it pass.

    EVERY LEG IS A CARDINALITY, NOT AN EXAMPLE.  "The rail held" is 784 of 784
    campaigns across four cells; "the ladder reduces" is 229 advances x 13
    fields plus 80,000-odd direct calls; "the offset tightened only where the
    rail allowed" is a SET IDENTITY between two cells' rail-bound campaigns.

    WHAT WOULD MAKE THIS WRONG: a leg that passes on an empty collection (each
    one below asserts its own count is non-zero); a leg that catches its own
    exception and reports a pass; reporting a pass for a leg that did not run;
    or checking the offset by re-applying it here, which would compare the
    program to a second copy of itself.
    """
    lo_ms, hi_ms, cmeta = T7.corridor()
    base = T7.run_cell(RC.CARD_V6_CONTROL, lo_ms, hi_ms)
    rail_atr = float(RC.Card().entry_rail_atr)
    legs: list[dict] = []

    # ── F-SG-CTRL · the 0.00 cell IS card v6, campaign for campaign ─────────
    zero = stopgrid_book(0.0, lo_ms, hi_ms)
    bz, bb = {_key(t): t for t in zero}, {_key(t): t for t in base}
    same = sum(1 for k in bb if k in bz and all(
        getattr(bz[k], f) == getattr(bb[k], f)
        for f in ("entry_px", "stop_px", "r_dist", "exit_ms", "exit_px",
                  "exit_reason", "net_r")))
    legs.append(_leg(
        "F-SG-CTRL",
        "the offset-0.00 cell reproduces card v6 trade-for-trade (the "
        "`if card.stop_grid_offset_atr:` guard is falsy, so the block never "
        "runs) — entry, stop, R, exit and net R all equal",
        ok=(same == len(base) == len(zero) and len(base) > 0),
        cardinality=f"{same}/{len(base)} campaigns identical; cell n={len(zero)}"))

    # ── F-SG-RAIL · the rail held in EVERY cell ─────────────────────────────
    tot = viol = 0
    per = []
    for off in STOP_OFFSETS:
        au = rail_audit(stopgrid_book(off, lo_ms, hi_ms), rail_atr)
        tot += au["campaigns_checked"]
        viol += au["rail_violations"]
        per.append(f"{off:+.2f}:{au['n_rail_bound']}bound")
    legs.append(_leg(
        "F-SG-RAIL",
        f"|entry - stop| >= {rail_atr} x ATR(entry bar) on EVERY campaign of "
        f"EVERY cell — the rail is re-imposed after the offset",
        ok=(viol == 0 and tot == len(STOP_OFFSETS) * len(base) and tot > 0),
        cardinality=f"{tot - viol}/{tot} campaigns over "
                    f"{len(STOP_OFFSETS)} cells; {viol} violations",
        detail="rail-bound per cell — " + ", ".join(per)))

    # ── F-SG-CLIP · the tightening offset moved everything the rail allowed ─
    tight = stopgrid_book(-0.25, lo_ms, hi_ms)
    bound_zero = _rail_bound_keys(zero, rail_atr)
    bound_tight = _rail_bound_keys(tight, rail_atr)
    bt = {_key(t): t for t in tight}
    unchanged = {k for k in bz if k in bt
                 and bt[k].stop_px == bz[k].stop_px}
    legs.append(_leg(
        "F-SG-CLIP",
        "a NEGATIVE offset tightens every campaign EXCEPT those already on the "
        "rail, and clips those to exactly the rail — so the set of campaigns "
        "whose stop is unchanged at -0.25 ATR IS the set that was rail-bound "
        "at 0.00 ATR, and the rail-bound set can only grow",
        ok=(unchanged == bound_zero and bound_zero <= bound_tight
            and len(bound_zero) > 0 and len(bound_tight) > len(bound_zero)),
        cardinality=f"unchanged={len(unchanged)} rail_bound(0.00)="
                    f"{len(bound_zero)} rail_bound(-0.25)={len(bound_tight)}; "
                    f"sets equal={unchanged == bound_zero}"))

    # ── F-SG-WIDE · a positive offset widens EVERY campaign, exactly ────────
    wide_ok, wide_n = True, 0
    for off in (0.25, 0.50):
        bo = {_key(t): t for t in stopgrid_book(off, lo_ms, hi_ms)}
        for k, t in bo.items():
            if k not in bz:
                wide_ok = False
                continue
            wide_n += 1
            if not (float(t.r_dist) > float(bz[k].r_dist) - _TOL
                    and float(t.r_dist) >= rail_atr * float(t.atr_at_entry)
                    - _TOL):
                wide_ok = False
    legs.append(_leg(
        "F-SG-WIDE",
        "a POSITIVE offset can never breach a floor on WIDTH, so every "
        "campaign in the +0.25 and +0.50 cells is at least as far from entry "
        "as the same campaign at 0.00 and still beyond the rail",
        ok=(wide_ok and wide_n == 2 * len(base) and wide_n > 0),
        cardinality=f"{wide_n} campaign comparisons over 2 cells"))

    # ── F-SG-LIVE · the knob is not inert ───────────────────────────────────
    nets = [round(sum(t.net_r for t in stopgrid_book(o, lo_ms, hi_ms)), 9)
            for o in STOP_OFFSETS]
    legs.append(_leg(
        "F-SG-LIVE",
        "the four cells are four DIFFERENT books — a grid whose cells all "
        "agree would mean the knob never reached the decision path",
        ok=(len(set(nets)) == len(STOP_OFFSETS)),
        cardinality=f"{len(set(nets))}/{len(STOP_OFFSETS)} distinct net R",
        detail=", ".join(f"{o:+.2f}:{n:+.4f}" for o, n in
                         zip(STOP_OFFSETS, nets))))

    # ── F-SG-NOPROMO · the diagnostic says so on every row ──────────────────
    sg = stopgrid_table(lo_ms, hi_ms, base)
    legs.append(_leg(
        "F-SG-NOPROMO",
        "every row of stopgrid_table carries promotable=False and the "
        "no-promotion sentence [D-R7]",
        ok=(len(sg) == len(STOP_OFFSETS)
            and not sg["promotable"].any()
            and bool((sg["promotion_rule"] == NO_PROMOTION).all())
            and not sg["scored"].any()),
        cardinality=f"{int((~sg['promotable']).sum())}/{len(sg)} rows "
                    f"promotable=False"))

    # ── F-AN-CARD · the 0.50 cards ARE the shipped ladder-only card ─────────
    fields = [f.name for f in dataclasses.fields(RC.Card) if f.name != "name"]
    c050 = _anchor_card(PRIOR_ANCHOR, PRIOR_OFFSET)
    diff = [f for f in fields
            if getattr(c050, f) != getattr(RC.CARD_LADDER_ONLY, f)]
    legs.append(_leg(
        "F-AN-CARD",
        "the 0.50 ATR bake-off card is field-identical to RC.CARD_LADDER_ONLY "
        "apart from its name — the offset rides trail_extra_buf_atr, which "
        "T7._ride_leg adds to RC.STOP_BUF_ATR",
        ok=(not diff and len(fields) > 0),
        cardinality=f"{len(fields) - len(diff)}/{len(fields)} fields equal",
        detail=f"differing: {diff}" if diff else ""))

    # ── F-AN-ID · the reduction, over the whole book ────────────────────────
    ident = identity_book(lo_ms, hi_ms)
    legs.append(_leg(
        "F-AN-ID",
        "the local ladder at max(pivot,e89) / 0.50 ATR reproduces the "
        "UNPATCHED RC.CARD_LADDER_ONLY book exactly — every campaign's entry, "
        "stop, R, exit and net R, and every Advance FIELD BY FIELD",
        ok=bool(ident["identical"]),
        cardinality=f"{ident['campaigns_compared']} campaigns, "
                    f"{ident['advances_compared']} advances x "
                    f"{len(_ADV_FIELDS)} fields = "
                    f"{ident['advance_fields_compared']} field comparisons, "
                    f"{ident['mismatches']} mismatches",
        detail=str(ident["examples"]) if ident["examples"] else ""))

    # ── F-AN-CALL · the reduction, off the book's own choices ───────────────
    ic = identity_calls(lo_ms, hi_ms)
    legs.append(_leg(
        "F-AN-CALL",
        "the same reduction driven on EVERY confirming (2,2) fractal of the "
        "panel, both directions, four standing-stop levels — so the monotone "
        "refusal and the minimum-advance refusal are exercised, not assumed",
        ok=bool(ic["identical"]),
        cardinality=f"{ic['calls']:,} calls: {ic['advances_returned']:,} "
                    f"advances x {len(_ADV_FIELDS)} fields, "
                    f"{ic['both_refused']:,} refused by BOTH, "
                    f"{ic['mismatches']} mismatches",
        detail=str(ic["examples"]) if ic["examples"] else ""))

    # ── F-AN-V6 · and it reduces to the v6 RATCHET too, which is not the ────
    # ── function it was modelled on — an independent implementation ─────────
    pv050 = anchor_book("pivot(2,2)", 0.50, lo_ms, hi_ms)
    bp = {_key(t): t for t in pv050}
    v6_same = sum(1 for k in bb if k in bp and all(
        getattr(bp[k], f) == getattr(bb[k], f)
        for f in ("entry_px", "stop_px", "r_dist", "exit_ms", "exit_px",
                  "exit_reason", "net_r", "final_stop_px")))
    v6_adv = sum(len(t.advances) for t in pv050)
    v6_adv_bad = 0
    for k, t in bp.items():
        o = bb.get(k)
        if o is None or len(t.advances) != len(o.advances):
            v6_adv_bad += 1
            continue
        v6_adv_bad += sum(1 for x, y in zip(t.advances, o.advances)
                          if _adv_mismatch(x, y))
    legs.append(_leg(
        "F-AN-V6",
        "the local ladder at pivot(2,2) / 0.50 ATR — the card's own buffer and "
        "rail — reproduces CARD v6 trade-for-trade and advance-for-advance. "
        "v6's ladder is V5.trail_step -> V4.ratchet_step, a DIFFERENT function "
        "from the RC.ladder_step this module was modelled on, so this is an "
        "agreement between two implementations and not a restatement of one",
        ok=(v6_same == len(base) == len(pv050) and v6_adv_bad == 0
            and v6_adv > 0),
        cardinality=f"{v6_same}/{len(base)} campaigns identical, {v6_adv} "
                    f"advances, {v6_adv_bad} campaigns with a differing "
                    f"advance"))

    # ── F-AN-RAIL · every advance in every cell is beyond the ladder rail ───
    adv_n = adv_bad = 0
    for anchor in ANCHORS:
        for off in ANCHOR_OFFSETS:
            for t in anchor_book(anchor, off, lo_ms, hi_ms):
                for a in t.advances:
                    adv_n += 1
                    if (abs(a.close - a.new_stop) / a.atr
                            < RC.MIN_STOP_ATR - 1e-12):
                        adv_bad += 1
    legs.append(_leg(
        "F-AN-RAIL",
        f"the LADDER's rail holds on every advance of every cell: "
        f"|confirming close - new stop| >= {RC.MIN_STOP_ATR} x ATR. The rail "
        f"is a floor on DISTANCE taken after the anchor, so no anchor — "
        f"however close to price the sweep puts it — can place a stop inside "
        f"it",
        ok=(adv_bad == 0 and adv_n > 0),
        cardinality=f"{adv_n - adv_bad}/{adv_n} advances over "
                    f"{len(ANCHORS) * len(ANCHOR_OFFSETS)} cells"))

    # ── F-AN-LIVE · the anchor knob reaches the decision path in every cell ─
    anets = [round(sum(t.net_r for t in anchor_book(a, o, lo_ms, hi_ms)), 9)
             for a in ANCHORS for o in ANCHOR_OFFSETS]
    legs.append(_leg(
        "F-AN-LIVE",
        "the ten cells are ten DIFFERENT books — a bake-off whose cells agreed "
        "would mean the anchor never reached the ride",
        ok=(len(set(anets)) == len(anets)),
        cardinality=f"{len(set(anets))}/{len(anets)} distinct net R"))

    # ── F-AN-WARM · every EMA carries its floor, and the floor is real ──────
    warm_ok, warm_n = True, 0
    for sym in RC.UNIVERSE:
        sr = anchor_series(sym)
        for nm, fl in (("e26", WARMUP_FLOOR["e26"]), ("e89", WARMUP_FLOOR["e89"]),
                       ("m_lo", WARMUP_FLOOR["M"]), ("m_hi", WARMUP_FLOOR["M"])):
            arr = sr[nm]
            warm_n += 1
            if not (bool(np.all(np.isnan(arr[:fl])))
                    and bool(np.isfinite(arr[fl]))):
                warm_ok = False
    legs.append(_leg(
        "F-AN-WARM",
        "every series this module reads is NULL below its own warm-up floor "
        "and finite at it — engine.indicators.ema seeds at the series start "
        "and NEVER returns NaN, so a floor that is not written does not exist",
        ok=(warm_ok and warm_n == 4 * len(RC.UNIVERSE)),
        cardinality=f"{warm_n}/{4 * len(RC.UNIVERSE)} series x assets checked",
        detail=f"floors {WARMUP_FLOOR}"))

    # ── F-AN-FLOOR · and the floors never bit a bar the ladder could use ────
    conf = []
    for anchor in ANCHORS:
        for off in ANCHOR_OFFSETS:
            conf += [a.conf_i for t in anchor_book(anchor, off, lo_ms, hi_ms)
                     for a in t.advances]
    deepest = max(WARMUP_FLOOR.values())
    legs.append(_leg(
        "F-AN-FLOOR",
        "no ladder advance anywhere in the ten cells sits at a bar the "
        "deepest warm-up floor could have touched — the floors are PRESENT "
        "and PROVABLY INERT, which is what makes them a repair rather than a "
        "change to a shipped number",
        ok=(bool(conf) and min(conf) > deepest
            and deepest < int(RC.WARMUP_BARS) + 1),
        cardinality=f"{len(conf):,} advances, earliest at bar {min(conf)} "
                    f"vs deepest floor {deepest} and WARMUP_BARS "
                    f"{RC.WARMUP_BARS}" if conf else "0 advances"))

    # ── F-AN-CELLS · ten cells, the prior present once, the sentence on all ─
    an = anchor_bakeoff(lo_ms, hi_ms, base)
    legs.append(_leg(
        "F-AN-CELLS",
        "the bake-off is 5 anchors x 2 offsets = 10 distinct cells, the "
        "pre-named prior appears exactly once, and the "
        "informs-future-tuning-only sentence rides EVERY row",
        ok=(len(an) == len(ANCHORS) * len(ANCHOR_OFFSETS)
            and an["cell"].nunique() == len(an)
            and int(an["is_the_pre_named_prior"].sum()) == 1
            and bool((an["informs_future_tuning_only"]
                      == NEVER_THE_WINNER).all())
            and not an["promotable"].any()),
        cardinality=f"{len(an)} rows, {an['cell'].nunique()} distinct cells, "
                    f"{int(an['is_the_pre_named_prior'].sum())} prior row, "
                    f"{int((an['informs_future_tuning_only'] == NEVER_THE_WINNER).sum())}"
                    f"/{len(an)} carry the sentence"))

    # ── F-AN-CLEAN · nothing leaked ─────────────────────────────────────────
    legs.append(_leg(
        "F-AN-CLEAN",
        "RC.ladder_step IS the object captured at import after every book and "
        "every table this module built — the patch is scoped and restored",
        ok=(RC.ladder_step is _RC_LADDER_STEP),
        cardinality="1/1 identity check on the live module attribute"))

    # ── F-LAB-PROV · the provisional flag tracks the count, both ways ───────
    cols = ["cell", "n", "provisional", "loao_excluding_zero",
            "loao_excludes_zero_above", "loao_excludes_zero_below"]
    both = pd.concat([sg[cols], an[cols]], ignore_index=True)
    agree = int((both["provisional"]
                 == (both["n"] < RC.PROVISIONAL_MIN_N)).sum())
    legs.append(_leg(
        "F-LAB-PROV",
        f"every row of both tables flags provisional iff n < "
        f"{RC.PROVISIONAL_MIN_N}",
        ok=(agree == len(both) and len(both) > 0),
        cardinality=f"{agree}/{len(both)} rows agree; "
                    f"min n = {int(both['n'].min())}"))

    # ── F-LAB-LOAO · the sign split is faithful to the shipped panel count ──
    lo_ok = int((both["loao_excludes_zero_above"]
                 + both["loao_excludes_zero_below"]
                 == both["loao_excluding_zero"]).sum())
    legs.append(_leg(
        "F-LAB-LOAO",
        "every row's ABOVE-zero and BELOW-zero panel counts sum to T7.loao's "
        "own excluding-zero count — the sign split re-reads the shipped "
        "panels, it does not recompute them, and a row whose halves did not "
        "sum would mean this lab had invented a panel",
        ok=(lo_ok == len(both) and len(both) > 0),
        cardinality=f"{lo_ok}/{len(both)} rows sum; "
                    f"{int(both['loao_excludes_zero_below'].sum())} "
                    f"panel-clearances across both tables are BELOW zero"))

    d = pd.DataFrame(legs)
    d["corridor"] = f"{cmeta['panel_start']} -> {cmeta['last_closed_4h_close']}"
    d["seed"] = T7.SEED
    d["gates"] = False
    return d


# ═════════════════════════════════════════════════════════════════ THE BUILD
def main() -> int:                                        # pragma: no cover
    """Run both tables and the self-check to stdout.  No file is written.

    WHAT WOULD MAKE THIS WRONG: writing anything (the driver owns every path
    this estate writes to), or returning 0 while a self-check leg failed — the
    exit code IS the module's own verdict on itself.
    """
    lo_ms, hi_ms, cmeta = T7.corridor()
    base = T7.run_cell(RC.CARD_V6_CONTROL, lo_ms, hi_ms)
    T7.log(f"CORRIDOR {cmeta['panel_start']} -> "
           f"{cmeta['last_closed_4h_close']} ({cmeta['span_days']} d)")
    T7.log(f"BASE card v6: n={len(base)} "
           f"net={sum(t.net_r for t in base):+.4f}")
    with pd.option_context("display.width", 200,
                           "display.max_columns", 60):
        sg = stopgrid_table(lo_ms, hi_ms, base)
        T7.log("\nS-STOPGRID [D-R7]\n" + sg[[
            "cell", "n", "net_r", "expectancy_r", "win_rate_pct",
            "rail_respected", "rail_violations", "n_rail_bound",
            "min_stop_dist_over_atr", "paired_delta_expectancy_r",
            "tail_exit_ratio", "max_single_trade_delta_share", "loao_line",
            "promotable"]].to_string(index=False))
        an = anchor_bakeoff(lo_ms, hi_ms, base)
        T7.log("\nL-ANCHOR\n" + an[[
            "cell", "n", "net_r", "expectancy_r", "n_advances",
            "paired_delta_expectancy_r", "tail_exit_ratio",
            "max_single_trade_delta_share", "loao_line",
            "is_the_pre_named_prior", "reduces_to_rc_ladder_step"]]
            .to_string(index=False))
        sc = selfcheck()
        T7.log("\nSELFCHECK\n" + sc[["leg", "passed", "cardinality"]]
               .to_string(index=False))
    return 0 if bool(sc["passed"].all()) else 1


if __name__ == "__main__":                                # pragma: no cover
    raise SystemExit(main())
