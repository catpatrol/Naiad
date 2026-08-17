"""TIER-C6 rev B · L-FMH · L-WALLQ · L-SPR-NT · THE SHADOW FLEET.

CLASS: measurement + pre-named labs + pre-named shadow grids.  D15 columns ride
every aggregate row and GATE NOTHING.  Every grid is reported WHOLE.  Every
public function's docstring says WHAT WOULD MAKE IT WRONG.

This module builds ON `tierc6` — it does not fork it.  `tierc6.py` must never
import this file, and does not: the dependency runs one way only.

────────────────────────────────────────────────────────────────────────────
WHAT IS HERE, AND WHAT EACH ONE COST TO BUILD
────────────────────────────────────────────────────────────────────────────
L-FMH   [H1]  fast x MH winner-protection.  COMMISSIONED ON THE CARD BOOK AND
              NOT BUILDABLE THERE — the v6 card exits `stop` 191 of 195 times
              and the three commissioned predicates fire on 3, 13 and 36
              campaigns with 0, 1 and 0 winners between them.  It is ridden on
              the UNION book as well (414 campaigns, 147 winners), and the card
              book's zeros are PRINTED BESIDE IT because the zeros are the
              finding.  Also: the commissioned outcome triple
              {winner-saved, winner-killed, loser-unchanged} IS NOT A PARTITION
              — three of its six cells have no name.  The 7-class exhaustive
              partition is shipped and three of its classes carry the
              commissioned names.

L-WALLQ [H2]  entries by wall alignment x outcome.  P-SIZE-W's evidence.  A LONG
              is scored against the RESISTANCE champion and a SHORT against
              SUPPORT (`T6.profit_side`), because scoring a short against a
              resistance wall measures the floor it has already left.

L-SPR-NT [F-C5-i]  the tide-neutral spring line, Tier-E, FULL CORRIDOR.  The
              estate's filed "3,526 refused sweeps" is defective in three ways
              and all three are quantified on the table's face:
                (1) NO WARM-UP FLOOR on the counting call.  Floored it is 3,470.
                    56 refusals live entirely inside the first 316 bars, where
                    `ind.ema` is seeded and the tide gate is evaluable and
                    WRONG.  (The same unfloored call also inflates the ADMITTED
                    signal count from 363 to 367 — measured here, and not in the
                    manifest at all.)
                (2) THE COMPARATOR IS THE WRONG POPULATION.  241 is CAMPAIGNS,
                    after one-position-per-asset drops candidates.  The
                    signal-level admitted count is 363.  241 is published as a
                    third column, never as a denominator.
                (3) A THIRD POPULATION IS COUNTED NOWHERE — sweeps that
                    penetrated and never closed back inside within 3 bars.
                    Without it the sweep population does not close.
              A fourth fate the spec did not name is also published:
              penetrations whose reclaim window runs off the end of the
              corridor and therefore have no fate at all.  Silently folding
              them into "unreclaimed" would be a truncated window quietly
              relabelled.

SHADOWS      S-OFFSET {0.25,0.50,0.75} x S-MINADV {0.00,0.05,0.10} as a 3x3
              CROSS reported WHOLE · S-BUF {0.15,0.25,0.35} + a wall-aware cell
              [H4] · S-HFRAC {33,67}.  Plus Tier-C5's four fleet families
              carried forward so the grid-size literal is checkable whole.

────────────────────────────────────────────────────────────────────────────
THE KNOB-ASSIGNMENT RULING — SURFACED, AND THE DEFENSIBLE DEFAULT PICKED
────────────────────────────────────────────────────────────────────────────
`RATCHET_BUF_ATR is STOP_BUF_ATR` (both 0.5) and `RATCHET_RAIL_ATR is
MIN_STOP_ATR` (both 1.0) — asserted at import in `tierc4_rules`.  So "offset"
and "buffer" name THE SAME NUMBER IN TWO PLACES and the two shadow families
must be bound to different SITES or they are the same grid twice.

PICKED (and this is the operator-visible ruling, see `KNOB_RULING`):
  S-OFFSET -> the ENTRY anchor's "beyond" (`STOP_BUF_ATR`, read by
              `struct_stop_4h` and `spring_stop`).  The card is 0.50, so the
              cross's middle column IS the card.
  S-BUF    -> the RATCHET's "beyond" (`RATCHET_BUF_ATR`, threaded by
              `tierc6._ride` as `RC.RATCHET_BUF_ATR + card.trail_extra_buf_atr`).
              The card is 0.50, OUTSIDE the set — the same shape as S-RAIL
              {1.25, 1.5} excluding the card's 1.0.

THE ALTERNATIVE, NAMED AND REJECTED: bind S-OFFSET to the ratchet buffer
instead.  Then S-OFFSET 0.50 duplicates the card and S-OFFSET 0.75 duplicates
the EXISTING `S-TRAIL +0.25 ATR buffer` cell exactly — two of three cells
already on the books, double-counted in the selection surface.

A CORRECTION TO THE COMMISSION, MEASURED HERE: the spec says the cross cell
(0.50, 0.00) "IS the ratified card".  That was true of the v5 card.  It is NOT
true of v6 — F-C4-d ratified `TRAIL_MIN_ADVANCE_ATR = 0.05`, so the cell that
is the v6 card is (0.50, 0.05), and (0.50, 0.00) is the v5-TRAIL control.  Both
are marked on the table's face and both identity claims are CHECKED trade for
trade rather than asserted.

────────────────────────────────────────────────────────────────────────────
HOW A SHADOW CELL IS RIDDEN — ONE CODE PATH, NO FORK
────────────────────────────────────────────────────────────────────────────
Three of the new knobs (`entry_buf_atr`, `trail_buf_atr`, `wall_aware_stop`) do
not exist on `RC.Card` and `tierc6._ride`/`tierc6.replay` therefore cannot read
them.  There were two ways to ride them and only one of them is honest:

  FORK `_ride` and `replay` into this file  — ~290 lines of copied decision path
  that can drift from the parent silently.  This estate has already paid for
  that mistake once.  NOT TAKEN.

  BIND THE KNOB AT ITS SITE for the duration of one cell — `_knobs()`, a
  single-entry context manager that rebinds the module attributes the parent
  reads (`RC.RATCHET_BUF_ATR`, `RC.struct_stop_4h`, `RC.spring_stop`,
  `RC.trail_step`), rides the cell through `tierc6.run_cell` UNCHANGED, and
  restores every name in a `finally`.  TAKEN, because it keeps ONE code path
  for every cell in the fleet — which is the property that makes a grid a
  comparison rather than a display.

It is only defensible because it is CHECKED, not asserted: at card values the
harness is proven INERT (the (0.50, 0.05) cell reproduces `T6.run_cell(CARD_V6)`
trade for trade), `restop` is proven to reproduce the parent's own Stop on every
eligible anchor in the corridor, and every rebound name is asserted back to its
original object BY IDENTITY on the way out.

Drafted for TIER-C6 rev B.  Seed 20260816.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, replace
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc6 as T6                                                  # noqa: E402
import tierc6_rules as RC                                            # noqa: E402
from engine import indicators as ind                                 # noqa: E402

iso, r4, r6, pct = T6.iso, T6.r4, T6.r6, T6.pct
SEED = T6.SEED

# ── the objects the harness rebinds, captured ONCE, before anything can move ──
_ORIG_STRUCT_STOP = RC.struct_stop_4h
_ORIG_SPRING_STOP = RC.spring_stop
_ORIG_TRAIL_STEP = RC.trail_step
_ORIG_RATCHET_BUF = RC.RATCHET_BUF_ATR

# `tierc6_rules` does not re-export `ribbon_band` (it binds the lanes and the
# stops, not the cascade's band helper), so it is reached through the parent it
# inherits from — the SAME OBJECT, not a copy.  Asserted below rather than
# assumed, because "the same object" is the entire claim.
ribbon_band = RC.V5.ribbon_band
assert ribbon_band is RC.V5.ribbon_band and RC.V5.MH_OR_HEAVIER is not None

# ── constants pinned HERE, before the look ───────────────────────────────────
EPS_DELTA = 1e-9        # in-memory tolerance, matching `_account`'s HALT bound.
                        # 2e-6 is the FILED-parquet bound (F-C5-HARV, three
                        # 6-dp columns x half an ulp); nothing here is scored
                        # off a parquet, so the tighter number is correct.

# H20/H100 — THE ESTATE HOLDS TWO INCOMPATIBLE READINGS AND THEY ARE NOT MERGED.
# census-2B's `HORIZONS_MS` is DURATION-fixed and on a 4h lens H20 resolves to
# ZERO BARS -> INFEASIBLE -> NaN.  `tierc5.MIDBAND_H` is a BAR COUNT and that is
# the reading adopted here, named as a deviation from R-1, with the durations
# printed on the table's face so no reader confuses the two.
H_BARS: tuple[int, ...] = (20, 100)
H_HOURS: dict[int, int] = {20: 80, 100: 400}

FDR_FAMILY_M_SPRNT = 8          # 2 horizons x 2 directions x 2 populations
FDR_Q = 0.10

MH_OR_HEAVIER: tuple[str, ...] = RC.V5.MH_OR_HEAVIER

SELECTION_SURFACE_NOTE = (
    "SELECTION SURFACE — every cell in this table was named before it ran; "
    "nothing here is promoted in-sample")

KNOB_RULING: dict[str, dict] = {
    "S-OFFSET": {
        "bound_to": "STOP_BUF_ATR — the ENTRY anchor's 'beyond'",
        "read_by": "tierc3_rules.struct_stop_4h · tierc5_rules.spring_stop",
        "card_value": RC.STOP_BUF_ATR,
        "card_is_a_cell": True,
        "mechanism": "restop() re-places the parent's OWN anchor at a different "
                     "buffer; the anchor CHOICE is buffer-free so this is exact",
        "alternative_rejected": "binding S-OFFSET to RATCHET_BUF_ATR instead — "
                                "then 0.50 duplicates the card and 0.75 "
                                "duplicates the existing S-TRAIL +0.25 cell, "
                                "double-counting two cells in the surface",
    },
    "S-BUF": {
        "bound_to": "RATCHET_BUF_ATR — the TRAIL's 'beyond'",
        "read_by": "tierc6._ride, as RC.RATCHET_BUF_ATR + card.trail_extra_buf_atr",
        "card_value": _ORIG_RATCHET_BUF,
        "card_is_a_cell": False,
        "mechanism": "the module attribute the parent reads is rebound for the "
                     "duration of the cell and restored by identity",
        "alternative_rejected": "adding a NEGATIVE trail_extra_buf_atr to reach "
                                "0.15/0.25/0.35 — arithmetically equal but it "
                                "prints the wrong knob on the cell's own face",
    },
    "S-MINADV": {
        "bound_to": "Card.trail_min_advance_atr — ALREADY ON THE v6 CARD",
        "read_by": "tierc6_rules.trail_step, gating abs(new-prev)/atr",
        "card_value": RC.TRAIL_MIN_ADVANCE_ATR,
        "card_is_a_cell": True,
        "mechanism": "no rebinding — the knob exists and the parent honours it",
        "alternative_rejected": "editing tierc4_rules.ratchet_step's monotone "
                                "gate — a parent edit, and not taken",
    },
    "S-HFRAC": {
        "bound_to": "Card.harvest_frac — ALREADY ON THE v6 CARD",
        "read_by": "tierc6._account, as q",
        "card_value": RC.HARVEST_FRACTION,
        "card_is_a_cell": False,
        "mechanism": "no rebinding; 50% is the RULED default [H3] and is the "
                     "card row, not a cell of this grid",
        "alternative_rejected": "renormalising R per leg — the denominator is "
                                "the ENTRY stop distance and the legs book "
                                "their own R against it",
    },
}


# ═════════════════════════════════════════════════════════════════ tiny helpers
def _win(t) -> bool:
    """`net_r > 0` — the estate's operative definition of a winner, confirmed.

    It is POST-fee, POST-funding and POST-ceiling, so a campaign that is a gross
    winner and a funding loser is a loser here.  That is the right ruler for a
    PROTECTION study (you are protecting BOOKED R) and it is said on the face of
    every table that uses it.

    WHAT WOULD MAKE THIS WRONG: switching to `gross_r > 0`, which would count
    campaigns the account never made money on.
    """
    return float(t.net_r) > 0.0


def _provisional(n: int) -> bool:
    return int(n) < RC.PROVISIONAL_MIN_N


def reached_1r_bar(t) -> int | None:
    """The FIRST bar in (entry_i, exit_i] whose favourable extreme reached +1R.

    `tierc6._ride` computes `reached_1r` and DISCARDS the index, which arm A3
    needs.  Rather than patch the parent, the bar is recovered here with the
    parent's own predicate and its own bar range — including the EXIT bar, because
    `_ride` updates `reached_1r` BEFORE it tests the stop, so a campaign stopped
    on the bar it first touched +1R is `reached_1r = True` in the parent.

    CROSS-CHECKED BY CARDINALITY, NOT BY EXAMPLE: `fmh_lab` asserts
    `(reached_1r_bar(t) is not None) == t.reached_1r` on EVERY campaign of every
    book it rides, and reports the count.  One agreeing example would prove
    nothing.

    WHAT WOULD MAKE THIS WRONG: excluding the exit bar (it would disagree with
    the parent on exactly the campaigns stopped at +1R), scanning from `entry_i`
    instead of `entry_i + 1`, or using the CLOSE where the parent uses the
    favourable EXTREME.
    """
    f = T6.frame(t.symbol)["f"]
    d = t.direction
    ext = f.h if d == 1 else f.l
    for j in range(t.entry_i + 1, t.exit_i + 1):
        if (float(ext[j]) - t.entry_px) * d / t.r_dist >= 1.0:
            return j
    return None


def _first_fire(mask: np.ndarray, lo_j: int, hi_j: int,
                before: int | None = None) -> int | None:
    """First index in [lo_j, hi_j] where `mask` is True, optionally < `before`."""
    hi_j = min(int(hi_j), len(mask) - 1)
    for j in range(int(lo_j), hi_j + 1):
        if before is not None and j >= before:
            return None
        if bool(mask[j]):
            return j
    return None


# ═══════════════════════════════════════════════════════════════════════ L-FMH
# THE THREE COMMISSIONED PREDICATES, PLUS THE TWO ALTERNATIVE READINGS THAT THE
# COMMISSION'S OWN VOCABULARY ALSO ADMITS.  All five are ridden; none is chosen
# after the look.
FMH_ARMS: tuple[tuple[str, str, str], ...] = (
    ("A1_fast_median_back_through_89", "named",
     "counter 12/89 cross inside the campaign — THE CARD'S OWN BELL "
     "(tierc6._ride labels this exact event `bell_12_89` and EXITS on it), so "
     "on the card lane A1 cannot save what it terminates"),
    ("A1b_FASTmid_back_through_89", "alternative",
     "census-2B's other 'fast-median': the FAST band's MID line (e9+e26)/2 "
     "crossing e89 against the campaign"),
    ("A2_fast_ribbon_inside_M_band", "named",
     "strict containment of the FAST band inside the M band, both taken as "
     "V5.ribbon_band (3-member min/max)"),
    ("A2b_fast_ribbon_intersects_M_band", "alternative",
     "the two bands merely INTERSECT — the weaker reading of 'inside'"),
    ("A3_12_26_counter_pre_1R", "named",
     "counter 12/26 cross strictly BEFORE the campaign first reaches +1R"),
)

FMH_CLASSES = ("winner_saved", "winner_killed", "winner_neutral",
               "loser_rescued", "loser_deepened", "loser_unchanged", "no_signal")

_FMH_CACHE: dict[tuple[str, int], dict[str, np.ndarray]] = {}


def fmh_arm_masks(sym: str, direction: int) -> dict[str, np.ndarray]:
    """The five arm predicates as per-bar boolean arrays, cached per (asset, dir).

    THE BAND DEFINITION IS PICKED BY NAME, because the estate holds two.
    `V5.ribbon_band` takes min/max over ALL THREE members of a family; census-2B's
    `ribbon(a, z)` takes the EXTREME PAIR only, and the two disagree on ~14% of
    FAST bars and ~8-9% of M bars.  THE DECISION PATH OWNS `V5.ribbon_band` and
    imports no analytics, so it is the object used here; the filed
    `census2b/ribbons/*.parquet` `FAST_upper/FAST_lower` columns are THE OTHER
    OBJECT and are not joined.  (They also end 2026-08-13T04:00Z, 17 4h bars
    short of this corridor — a join would have silently truncated the book.)

    WHAT WOULD MAKE THIS WRONG: mixing the two band definitions between the FAST
    and M legs of one predicate; taking the cross in the campaign's own direction
    rather than AGAINST it (that is a continuation signal, not a protection one);
    or reading the filed parquet bands under the name `V5.ribbon_band`.
    """
    key = (sym, int(direction))
    if key in _FMH_CACHE:
        return _FMH_CACHE[key]
    st = T6.frame(sym)
    f, x = st["f"], st["x"]
    c = f.c
    d = int(direction)
    flo, fhi = ribbon_band(c, "FAST")
    mlo, mhi = ribbon_band(c, "M")
    fmid = (ind.ema(c, 9) + ind.ema(c, 26)) / 2.0
    a1b = (ind.crossunder(fmid, f.e89) if d == 1
           else ind.crossover(fmid, f.e89))
    out = {
        "A1_fast_median_back_through_89": (x["w_dn"] if d == 1 else x["w_up"]),
        "A1b_FASTmid_back_through_89": np.asarray(a1b, bool),
        "A2_fast_ribbon_inside_M_band": (flo >= mlo) & (fhi <= mhi),
        "A2b_fast_ribbon_intersects_M_band": (flo <= mhi) & (fhi >= mlo),
        "A3_12_26_counter_pre_1R": (x["t_dn"] if d == 1 else x["t_up"]),
    }
    _FMH_CACHE[key] = out
    return out


def net_r_if_exited_at(t, s_i: int, card: RC.Card | None = None) -> float:
    """Net R had the campaign closed at the CLOSE of bar `s_i` instead of its
    realised exit.

    NO SECOND REPLAY, AND THAT IS A STRUCTURAL FACT, NOT AN OPTIMISATION.
    `(entry_i, s_i]` with `s_i <= t.exit_i` is a STRICT PREFIX of a path the
    realised ride already walked WITHOUT the stop, the bell or the clock firing.
    Every gate that could have terminated the campaign before `s_i` is already
    known not to have.  So only the exit instant moves and `tierc6._account` does
    the rest.  (This is strictly cheaper than the S-LIMIT overlay, which DOES
    re-ride, because a limit fill moves the ENTRY and therefore the prefix.)

    The exit price is the CLOSE of `s_i` because that is the card's own exit
    instant for every close-based exit it has — `bell`, `time_stop` and
    `corridor_end` all fill at `f.c[j]`.

    WHAT WOULD MAKE THIS WRONG: `s_i` outside (entry_i, exit_i] (asserted); a
    harvest booked that had not happened by `s_i` (filtered); an add charged that
    had not been entered by `s_i` (filtered); or a `card` whose `harvest_frac` or
    `funding_ceiling_r` differs from the card the book was ridden on, which would
    re-account the counterfactual under a different accounting than the realised
    leg it is subtracted from.
    """
    assert t.entry_i < s_i <= t.exit_i, (
        f"counterfactual outside the realised path: {t.symbol} "
        f"{t.entry_i} < {s_i} <= {t.exit_i}")
    f = T6.frame(t.symbol)["f"]
    if card is None:
        card = RC.Card(name="L-FMH counterfactual", grid="L-FMH")
    harv = ((t.harvest_i, t.harvest_px, t.harvest_unit_move_r)
            if (t.harvested and t.harvest_i is not None and t.harvest_i <= s_i)
            else None)
    ride = {"exit_i": int(s_i), "exit_px": float(f.c[s_i]),
            "exit_reason": "L-FMH", "advances": [], "harvest": harv,
            "blocked": "", "mfe": t.entry_px,
            "adds": [a for a in t.adds if a.i <= s_i],
            "final_stop": t.stop_px, "mae_to_1r": None, "reached_1r": False}
    return float(T6._account(t.symbol, card, t.direction, t.entry_i, t.entry_px,
                             t.r_dist, ride)["net_r"])


def fmh_classify(win: bool, delta: float | None) -> str:
    """The SEVEN-class outcome partition — exhaustive and disjoint.

    THE COMMISSIONED TRIPLE IS NOT A PARTITION.  {winner-saved, winner-killed,
    loser-unchanged} leaves three of the six signal-bearing cells UNNAMED, which
    violates *report the grid WHOLE*: a winner the signal left exactly alone and
    a loser the signal rescued or deepened would each have had to be filed under
    a label that does not describe them.  Three of these seven carry the
    commissioned names; the other four exist so nothing has to be mis-filed, and
    `loser_unchanged` becomes a MEASURED claim rather than an assumption.

    WHAT WOULD MAKE THIS WRONG: a tolerance so loose that real deltas land in the
    `*_neutral`/`unchanged` classes, or so tight that float noise on an
    arithmetically identical re-accounting does not.  EPS_DELTA is the
    in-memory HALT tolerance of `_account` itself (1e-9), not a number chosen to
    make a cell look full.
    """
    if delta is None:
        return "no_signal"
    if win:
        return ("winner_saved" if delta > EPS_DELTA else
                "winner_killed" if delta < -EPS_DELTA else "winner_neutral")
    return ("loser_rescued" if delta > EPS_DELTA else
            "loser_deepened" if delta < -EPS_DELTA else "loser_unchanged")


def fmh_lab(book: list, base: list, label: str,
            card: RC.Card | None = None) -> pd.DataFrame:
    """L-FMH: one row per (campaign x arm), plus one `__ARM__` aggregate per arm.

    THE COUNTERFACTUAL BOOK IS RE-ACCOUNTED, NOT RE-REPLAYED, and the aggregate
    rows say so in a column.  Exiting a campaign early would free the asset
    earlier and `one position per asset` could then admit campaigns the realised
    book never took.  Those campaigns are NOT modelled: the acted book is the
    realised book with the signalled campaigns' outcomes replaced.  This is the
    right object for "did the signal protect THIS campaign" and the wrong one for
    "what would the book have been" — and the distinction is printed rather than
    left for a reader to discover.

    THE ACTED BOOK IS PAIRED WITH THE BASE BY CONSTRUCTION (campaigns with no
    signal carry their realised outcome through), so `n_paired` on the D15 block
    equals the base's n whenever `book is base`.  When it does not — the union
    book against the card base — the unpaired counts carry it, as they are meant
    to.

    WHAT WOULD MAKE THIS WRONG: acting on a signal bar OUTSIDE (entry_i, exit_i]
    (asserted in `net_r_if_exited_at`); scoring A3 without the pre-+1R condition;
    taking the LAST firing rather than the FIRST (you act when the signal fires,
    not when it stops firing); or letting the arm masks be read in the campaign's
    own direction.
    """
    if card is None:
        card = RC.Card(name="L-FMH counterfactual", grid="L-FMH")

    # ── CARDINALITY CHECK, BY A DIFFERENT PATH, ON EVERY CAMPAIGN ────────────
    # `reached_1r` is the parent's published boolean; `reached_1r_bar` re-derives
    # the INDEX from raw bars.  The two must agree on all n, not on one example.
    r1 = {}
    dis = 0
    for t in book:
        j = reached_1r_bar(t)
        r1[(t.symbol, t.entry_ms)] = j
        if (j is not None) != bool(t.reached_1r):
            dis += 1
    if dis:
        raise SystemExit(
            f"HALT: reached_1r disagrees with its own bar index on {dis} of "
            f"{len(book)} campaigns in book {label!r} — one of the two readings "
            f"is not the parent's.")

    # ── the close-exit re-accounting control, also a cardinality check ────────
    # For every campaign whose realised exit was AT A CLOSE, re-accounting the
    # realised exit bar must reproduce the realised net exactly.  Stop exits are
    # excluded because they fill at the STOP, not the close — which is the whole
    # reason this control exists.
    n_close_exit = n_close_ok = 0
    for t in book:
        if t.exit_reason in ("bell_12_89", "bell_89_316", "time_stop",
                             "corridor_end") and t.exit_i > t.entry_i:
            n_close_exit += 1
            if abs(net_r_if_exited_at(t, t.exit_i, card) - float(t.net_r)) <= 1e-9:
                n_close_ok += 1
    if n_close_exit and n_close_ok != n_close_exit:
        raise SystemExit(
            f"HALT: the L-FMH re-accounting does not reproduce the realised net "
            f"on {n_close_exit - n_close_ok} of {n_close_exit} close-filled "
            f"exits in book {label!r}.")
    # THE LEG'S OWN CARDINALITY IS PUBLISHED, because it CAN be zero honestly.
    # The v6 card exits `stop` on 191 of 195, so a book could hold no
    # close-filled exit at all and this control would then pass having compared
    # NOTHING. That is a real possibility, not a defect — but a reader must be
    # able to see it, so the count rides the aggregate rows rather than dying in
    # a local variable.
    n_reacct_checked = n_close_exit

    rows: list[dict] = []
    per_arm: dict[str, list] = {a: [] for a, _, _ in FMH_ARMS}
    for t in book:
        masks = fmh_arm_masks(t.symbol, t.direction)
        f = T6.frame(t.symbol)["f"]
        r1_i = r1[(t.symbol, t.entry_ms)]
        win = _win(t)
        for arm, reading, why in FMH_ARMS:
            before = r1_i if arm == "A3_12_26_counter_pre_1R" else None
            s_i = _first_fire(masks[arm], t.entry_i + 1, t.exit_i, before=before)
            if s_i is None:
                acted, delta, sig_ts = float(t.net_r), None, ""
                bars_after = bars_before = None
                hstate = ""
                pre1r = None
            else:
                acted = net_r_if_exited_at(t, s_i, card)
                delta = acted - float(t.net_r)
                sig_ts = iso(int(f.open_ms[s_i]))
                bars_after = int(s_i - t.entry_i)
                bars_before = int(t.exit_i - s_i)
                hstate = ("harvested_before_signal"
                          if (t.harvested and t.harvest_i is not None
                              and t.harvest_i <= s_i)
                          else "harvest_after_signal_dropped"
                          if t.harvested else "never_harvested")
                pre1r = bool(r1_i is not None and r1_i < s_i)
            cls = fmh_classify(win, delta)
            per_arm[arm].append((t, acted))
            rows.append({
                "asset": t.symbol, "entry_ms": int(t.entry_ms),
                "entry_ts": iso(int(t.entry_ms)), "book": label, "arm": arm,
                "arm_reading": reading, "arm_note": why,
                "lane": t.lane,
                "direction": "long" if t.direction == 1 else "short",
                "signal_ts": sig_ts, "bars_after_entry": bars_after,
                "bars_before_exit": bars_before,
                "realised_net_r": r6(float(t.net_r)), "acted_net_r": r6(acted),
                "delta_r": (r6(delta) if delta is not None else None),
                "winner": win, "winner_rule": "net_r > 0 (post-fee, post-funding, "
                                              "post-ceiling)",
                "outcome_class": cls, "exit_reason": t.exit_reason,
                "harvest_state_at_signal": hstate,
                "reached_1r_before_signal": pre1r,
                "row_kind": "campaign",
            })

    # ── the __ARM__ aggregates, with D15 riding them and gating nothing ──────
    for arm, reading, why in FMH_ARMS:
        pairs = per_arm[arm]
        acted_book = [replace(t, net_r=a) for t, a in pairs]
        sub = [r for r in rows if r["arm"] == arm and r["row_kind"] == "campaign"]
        fired = [r for r in sub if r["signal_ts"]]
        n_fired = len(fired)
        row = {
            "asset": "__ARM__", "entry_ms": 0, "entry_ts": "", "book": label,
            "arm": arm, "arm_reading": reading, "arm_note": why, "lane": "",
            "direction": "", "signal_ts": "",
            "bars_after_entry": None, "bars_before_exit": None,
            "realised_net_r": r6(sum(float(t.net_r) for t, _ in pairs)),
            "acted_net_r": r6(sum(a for _, a in pairs)),
            "delta_r": r6(sum(a - float(t.net_r) for t, a in pairs)),
            "winner": None, "winner_rule": "net_r > 0 (post-fee, post-funding, "
                                           "post-ceiling)",
            "outcome_class": "__ALL__", "exit_reason": "",
            "harvest_state_at_signal": "", "reached_1r_before_signal": None,
            "row_kind": "arm_aggregate",
            "n_campaigns": len(pairs), "n_fired": n_fired,
            "n_fired_winners": sum(1 for r in fired if r["winner"]),
            "n_book_winners": sum(1 for r in sub if r["winner"]),
            "book_is_reaccounted_not_rereplayed": True,
            "n_reaccounting_control_checked": n_reacct_checked,
            "reaccounting_control_is_vacuous": bool(n_reacct_checked == 0),
            "n_reached_1r_bar_agrees": len(book) - dis,
            "provisional_on_fired_n": _provisional(n_fired),
            "provisional_on_fired_winners": _provisional(
                sum(1 for r in fired if r["winner"])),
        }
        for c in FMH_CLASSES:
            row[f"n_{c}"] = sum(1 for r in sub if r["outcome_class"] == c)
        row.update(T6.d15(acted_book, base))
        rows.append(row)
    df = pd.DataFrame(rows)
    # COUNTS PRINT AS COUNTS.  The campaign rows carry NaN in the aggregate-only
    # columns, which upcasts them to float; a table that prints "n = 195.0" for a
    # number of campaigns is a table that invites a reader to wonder what the
    # fraction means.  Nullable Int64 keeps the NaN and the integer.
    for c in (["n_campaigns", "n_fired", "n_fired_winners", "n_book_winners",
               "bars_after_entry", "bars_before_exit", "n_paired",
               "unpaired_cell_n", "unpaired_base_n",
               "n_reaccounting_control_checked", "n_reached_1r_bar_agrees"]
              + [f"n_{k}" for k in FMH_CLASSES]):
        if c in df.columns:
            df[c] = df[c].astype("Int64")
    df["window"] = "full_corridor"
    df["tier"] = "E (measurement — gates nothing, moves no fill)"
    df["selection_surface"] = (
        f"SELECTION SURFACE — {len(FMH_ARMS)} arms declared before the look: "
        "3 carry the commission's own names and 2 are the alternative readings "
        "the commission's vocabulary also admits. All are printed; none is "
        "chosen after the look")
    df["d15_gates_nothing"] = True
    return df


def fmh_tables(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """L-FMH on all three books at once — CARD, v5-CONTROL and UNION.

    THE CARD BOOK'S ZEROS ARE THE FINDING AND ARE PRINTED, NOT SUPPRESSED.
    L-FMH was commissioned on the card book and its winner cells there are empty:
    the card exits `stop` on 191 of 195 campaigns, so the 12/89 counter-cross
    almost never happens inside a live campaign — and when it does, it IS the
    exit.  The union book (414 campaigns, 147 winners) is the buildable
    substitute, ridden with the SAME predicates and the SAME counterfactual, and
    both are in this one frame so no reader can quote one without the other.

    WHAT WOULD MAKE THIS WRONG: dropping the card rows because they are empty;
    or riding the union book through a different card, which would make the two
    halves of the table incomparable — every book here is ridden through
    `tierc6.run_cell` with the SAME v6 knobs, differing only in `lane`.
    """
    books = [
        ("card_v6", RC.CARD_V6),
        ("card_v5_control", RC.CARD_V5_CONTROL),
        ("union_v6", RC.Card(name="union", grid="P-SPR-1", lane="union")),
    ]
    base = T6.run_cell(RC.CARD_V6, lo_ms, hi_ms)
    out = []
    for lbl, cd in books:
        bk = base if lbl == "card_v6" else T6.run_cell(cd, lo_ms, hi_ms)
        out.append(fmh_lab(bk, base, lbl, card=cd))
    return pd.concat(out, ignore_index=True)


# ═════════════════════════════════════════════════════════════════════ L-WALLQ
_CHAMP_CACHE: dict[int, dict] = {}


def wall_champs(hi_ms: int) -> dict[tuple[str, str], int]:
    """Both leagues' champions, `(side, tf) -> ema length`, cached per corridor end.

    WHAT WOULD MAKE THIS WRONG: scoring both directions against ONE side's
    champion.  The league had to grow a support side before P-WALL-1 or L-WALLQ
    could be written at all — a short scored against the resistance champion is
    measured against the floor it has already left.
    """
    k = int(hi_ms)
    if k not in _CHAMP_CACHE:
        lg = pd.concat([T6.league(hi_ms, s) for s in T6.SIDES], ignore_index=True)
        _CHAMP_CACHE[k] = T6.champions(lg)
    return _CHAMP_CACHE[k]


def wallq_lab(book: list, champs: dict, tf: str = "12h") -> pd.DataFrame:
    """L-WALLQ [H2] — entries bucketed by WALL ALIGNMENT x outcome.  P-SIZE-W's
    evidence.

    THE WALL IS READ AS OF THE ENTRY BAR, and the reason is that the alignment is
    defined against `entry_px`, `stop_px` and the first +2R — none of which
    exists until the entry bar.  `RC.wall_alignment`'s docstring says "read at the
    arming"; that reading is ALSO published here as `alignment_at_arm_bar` (same
    entry/stop geometry, wall as of `arm_i`), because the two differ and only one
    of them can be the primary.  NEITHER LOOKS AHEAD: `arm_i <= entry_i` and the
    wall series is already as-of each 4h bar's own close.

    THE FIVE BUCKETS ARE REPORTED WHOLE, `no_wall` INCLUDED.  A 12h EMA of length
    889 (the resistance champion) is not warm for the first 889 12h bars, and
    `wall_series_12h` returns NaN there rather than publishing a seeded value as a
    level.  Those campaigns are `no_wall` — a real bucket with a real cause, not
    a dropped row.

    THE TABLE CARRIES THE JOIN KEY ITS CALLER DECLARES.  `tierc6.run` files this
    frame with `write_table(..., ["bucket", "key"])`, and F-KEY reads those two
    column NAMES off the frame before it will write anything.  Publishing only
    `alignment`/`direction` made that call a `KeyError` inside `assert_key` — the
    TIER-C6 build died at `l_wallq` and never reached the manifest.  So `bucket`
    (the alignment) and `key` (the row's own discriminator) are emitted here, and
    `alignment` is KEPT beside them because it is the column the analysis reads.
    The pair is unique by construction: a campaign's `key` is `asset|entry_ms`,
    which a campaign holds exactly once, and an aggregate's `key` is its
    direction, which cannot collide with a symbol-bearing string.

    WHAT WOULD MAKE THIS WRONG: computing the alignment from the EXIT (it would
    be an outcome, not a context); using the resistance champion for shorts;
    treating a NaN wall as "neither" (it would fill an evidential bucket with
    campaigns that had no evidence); reading the 12h wall as of the 4h bar's
    OPEN, which would quote a level built partly from that bar itself; or
    dropping `bucket`/`key` and leaving the caller's declared key undefined.
    """
    rows = []
    for t in book:
        side = T6.profit_side(t.direction)
        L = champs.get((side, tf))
        if L is None:
            raise SystemExit(f"HALT: no champion for ({side!r}, {tf!r})")
        we = T6.wall(t.symbol, int(L), tf)[0]
        w_entry = float(we[t.entry_i])
        w_arm = float(we[t.arm_i]) if 0 <= t.arm_i < len(we) else float("nan")
        al = RC.wall_alignment(t.entry_px, t.stop_px, t.r_dist, w_entry,
                               t.direction)
        al_arm = RC.wall_alignment(t.entry_px, t.stop_px, t.r_dist, w_arm,
                                   t.direction)
        rows.append({
            "asset": t.symbol, "entry_ms": int(t.entry_ms),
            "entry_ts": iso(int(t.entry_ms)), "lane": t.lane,
            "direction": "long" if t.direction == 1 else "short",
            "profit_side": side, "champion_ema": int(L), "champion_tf": tf,
            "wall_px_at_entry": (r6(w_entry) if np.isfinite(w_entry) else None),
            "wall_px_at_arm_bar": (r6(w_arm) if np.isfinite(w_arm) else None),
            "entry_px": r6(t.entry_px), "stop_px": r6(t.stop_px),
            "target_2r_px": r6(t.entry_px + t.direction * 2.0 * t.r_dist),
            "alignment": al, "alignment_at_arm_bar": al_arm,
            "bucket": al, "key": f"{t.symbol}|{int(t.entry_ms)}",
            "alignment_agrees_across_bars": bool(al == al_arm),
            "net_r": r6(float(t.net_r)), "winner": _win(t),
            "mfe_r": r6(float(t.mfe_r)), "reached_1r": bool(t.reached_1r),
            "exit_reason": t.exit_reason, "bars_held": int(t.bars_held),
            "row_kind": "campaign",
        })
    per = pd.DataFrame(rows)
    if not len(per):
        return per

    agg_rows = []
    order = ["beyond_stop", "blocks_2r", "both", "neither", "no_wall"]
    for bucket in order:                       # EVERY bucket, whether or not
        for dname in ("ALL", "long", "short"):  # it is populated
            m = per[per["alignment"] == bucket]
            if dname != "ALL":
                m = m[m["direction"] == dname]
            n = len(m)
            agg_rows.append({
                "asset": "__BUCKET__", "entry_ms": 0, "entry_ts": "",
                "lane": "", "direction": dname, "profit_side": "",
                "champion_ema": None, "champion_tf": tf,
                "alignment": bucket, "alignment_at_arm_bar": "",
                "bucket": bucket, "key": dname,
                "row_kind": "bucket_aggregate",
                "n": int(n),
                "n_winners": int(m["winner"].sum()) if n else 0,
                "win_rate_pct": (pct(int(m["winner"].sum()), n) if n else None),
                "net_r": (r4(float(m["net_r"].sum())) if n else None),
                "expectancy_r": (r4(float(m["net_r"].mean())) if n else None),
                "mean_mfe_r": (r4(float(m["mfe_r"].mean())) if n else None),
                "reached_1r_pct": (pct(int(m["reached_1r"].sum()), n) if n else None),
                "provisional": _provisional(n),
                "arm_bar_reading_agrees_pct": (
                    pct(int(m["alignment_agrees_across_bars"].sum()), n)
                    if n else None),
            })
    out = pd.concat([per, pd.DataFrame(agg_rows)], ignore_index=True)
    for c in ("n", "n_winners", "champion_ema", "bars_held"):
        if c in out.columns:
            out[c] = out[c].astype("Int64")
    out["window"] = "full_corridor"
    out["tier"] = "E (measurement — gates nothing, moves no fill)"
    out["selection_surface"] = (
        "the champion EMA is an ARGMAX over the league's eligible cells — a "
        "selection surface feeding this table, disclosed here")
    # THE CALLER'S DECLARED KEY IS CHECKED HERE, NOT ONLY AT WRITE TIME.
    # `tierc6.run` files this frame under ["bucket", "key"]; F-KEY would catch a
    # duplicate, but only after the whole build had been paid for. Checking it
    # at the source makes the failure land on the function that owns the key.
    dup = int(out.duplicated(subset=["bucket", "key"]).sum())
    if dup:
        raise SystemExit(
            f"HALT: L-WALLQ's declared join key ['bucket','key'] is not unique "
            f"— {dup} duplicate row(s). tierc6.run files this frame on that key "
            "and a join on a non-unique key silently drops or multiplies rows.")
    return out


# ════════════════════════════════════════════════════════════════════ L-SPR-NT
@dataclass
class Sweep:
    """One penetration of the prior `lookback` extreme, and its FATE.

    `fate` is one of {"admitted", "refused_on_tide", "unreclaimed",
    "truncated_at_corridor_end"} and the four are an EXHAUSTIVE, DISJOINT
    partition of every penetration in the scanned corridor.

    THE FOURTH FATE IS NOT IN THE COMMISSION AND IS NOT OPTIONAL.  A penetration
    whose 3-bar reclaim window runs off the end of the corridor has NO fate: it
    neither reclaimed nor failed to, it was not observed long enough.  Folding it
    into `unreclaimed` would be a truncated window quietly relabelled as a result.
    """
    direction: int
    sweep_i: int
    sweep_ms: int
    sweep_extreme: float
    swept_level: float
    reclaim_i: int | None
    reclaim_ms: int | None
    bars_to_reclaim: int | None
    fate: str


def spring_scan(f, lo_i: int, hi_i: int,
                lookback: int = RC.SPRING_LOOKBACK_BARS,
                reclaim_bars: int = RC.SPRING_RECLAIM_BARS
                ) -> tuple[list, list[Sweep]]:
    """The v5 spring scan, emitting BOTH legs from ONE traversal.

    The `list[Spring]` returned MUST equal `RC.spring_signals(f, lo_i, hi_i)`
    element for element; `sprnt_lab` asserts it on every asset and reports the
    count.  That leg is the whole reason this generalisation is safe: it is the
    `build_fractals` / F-C5-INHERIT pattern — a widened function that must still
    reproduce the narrow one it widened.

    WHAT WOULD MAKE THIS WRONG: an admitted leg that differs from the parent by
    one signal; a sweep whose fate is unset; a prior extreme computed INCLUSIVE
    of the sweep bar (nothing could then ever penetrate); or
    |admitted| + |refused| + |unreclaimed| + |truncated| != the penetration count
    re-derived from bars by a DIFFERENT path (`penetration_count`, which uses a
    vectorised rolling window and never walks this loop).
    """
    n = len(f.c)
    hi_i = min(int(hi_i), n - 1)
    out: list = []
    sweeps: list[Sweep] = []
    lows, highs, closes = f.l, f.h, f.c
    for i in range(max(int(lo_i), lookback), hi_i + 1):
        prior_lo = float(np.min(lows[i - lookback:i]))
        prior_hi = float(np.max(highs[i - lookback:i]))
        for direction in (1, -1):
            swept = (lows[i] < prior_lo) if direction == 1 else (highs[i] > prior_hi)
            if not swept:
                continue
            level = prior_lo if direction == 1 else prior_hi
            ext = float(lows[i]) if direction == 1 else float(highs[i])
            fate_set = False
            truncated = False
            for k in range(0, reclaim_bars + 1):
                j = i + k
                if j > hi_i:
                    truncated = True
                    break
                inside = (closes[j] > level) if direction == 1 else (closes[j] < level)
                if not inside:
                    ext = (min(ext, float(lows[j])) if direction == 1
                           else max(ext, float(highs[j])))
                    continue
                ext = (min(ext, float(lows[j])) if direction == 1
                       else max(ext, float(highs[j])))
                tide = ((f.e89[j] > f.e316[j] and closes[j] > f.e316[j])
                        if direction == 1 else
                        (f.e89[j] < f.e316[j] and closes[j] < f.e316[j]))
                sweeps.append(Sweep(
                    direction=direction, sweep_i=i, sweep_ms=int(f.open_ms[i]),
                    sweep_extreme=ext, swept_level=level, reclaim_i=j,
                    reclaim_ms=int(f.open_ms[j]), bars_to_reclaim=k,
                    fate=("admitted" if tide else "refused_on_tide")))
                fate_set = True
                if tide:
                    out.append(RC.Spring(
                        direction=direction, sweep_i=i,
                        sweep_ms=int(f.open_ms[i]), sweep_extreme=ext,
                        swept_level=level, reclaim_i=j,
                        reclaim_ms=int(f.open_ms[j]), bars_to_reclaim=k))
                break
            if not fate_set:
                sweeps.append(Sweep(
                    direction=direction, sweep_i=i, sweep_ms=int(f.open_ms[i]),
                    sweep_extreme=ext, swept_level=level, reclaim_i=None,
                    reclaim_ms=None, bars_to_reclaim=None,
                    fate=("truncated_at_corridor_end" if truncated
                          else "unreclaimed")))
    out.sort(key=lambda s: (s.reclaim_ms, -s.direction))
    return out, sweeps


def penetration_count(f, lo_i: int, hi_i: int,
                      lookback: int = RC.SPRING_LOOKBACK_BARS) -> dict:
    """How many penetrations exist in [lo_i, hi_i], BY A DIFFERENT PATH.

    `spring_scan` walks bars in a Python loop and calls `np.min`/`np.max` over a
    slice per bar.  This counts the same events with a VECTORISED rolling
    window built by pandas and a single boolean comparison — no loop, no slice,
    no shared code with the scan it checks.  Comparing the scan's own count to
    itself would prove nothing; this is the closure test that makes the four-fate
    partition a claim rather than a definition.

    `both_directions_same_bar` IS MEASURED, NOT ASSUMED ZERO.  An OUTSIDE bar can
    take out the prior 96-bar low AND the prior 96-bar high, and `spring_scan`
    emits TWO Sweeps for it (its direction loop tests the two legs
    independently), so `total` must be `long + short` and not a count of bars.
    Today the corridor holds one such bar (ETHUSDT); a hardcoded 0 here would
    have been a published number that the data contradicts.

    WHAT WOULD MAKE THIS WRONG: a rolling window that includes the current bar
    (`shift(1)` is what excludes it), a `min_periods` that lets a partial window
    produce a level, an index range that differs from the scan's by one bar, or
    reporting `total` as a count of BARS rather than of penetrations.
    """
    lo_i = max(int(lo_i), lookback)
    hi_i = min(int(hi_i), len(f.c) - 1)
    lo_s = pd.Series(np.asarray(f.l, float))
    hi_s = pd.Series(np.asarray(f.h, float))
    prior_lo = lo_s.rolling(lookback, min_periods=lookback).min().shift(1).to_numpy()
    prior_hi = hi_s.rolling(lookback, min_periods=lookback).max().shift(1).to_numpy()
    sl = slice(lo_i, hi_i + 1)
    m_lo = np.asarray(f.l, float)[sl] < prior_lo[sl]
    m_hi = np.asarray(f.h, float)[sl] > prior_hi[sl]
    nl, ns = int(m_lo.sum()), int(m_hi.sum())
    return {"long": nl, "short": ns,
            "both_directions_same_bar": int(np.sum(m_lo & m_hi)),
            "bars_with_a_penetration": int(np.sum(m_lo | m_hi)),
            "total": nl + ns}


def collapse_episodes(sweeps: list[Sweep]) -> list[Sweep]:
    """Greedy, NON-OVERLAPPING episodes, per direction — census-2B's A-4 rule.

    `RC.spring_signals` emits ONCE PER SWEEP BAR with no non-overlap guard, so
    three consecutive bars re-sweeping one level emit three times.  census-2B's
    `springs_for_cell` is explicit that "episodes are emitted GREEDILY and
    non-overlapping per side: once a spring fires at i and reclaims at j, the scan
    resumes at j+1", and that emitting every qualifying bar "would triple-count a
    single three-bar spring".  This applies that discipline WITHOUT touching the
    lane — the raw count and the collapsed count are both published.

    An UNRECLAIMED sweep sets no guard (census-2B `continue`s past it), because
    it has no episode to absorb anything into.

    WHAT WOULD MAKE THIS WRONG: collapsing across directions (a long sweep and a
    short sweep are different events); resuming the scan at the SWEEP bar rather
    than the RECLAIM bar; or letting an unreclaimed penetration absorb later ones.
    """
    out: list[Sweep] = []
    for d in (1, -1):
        guard = -1
        for sw in sorted([s for s in sweeps if s.direction == d],
                         key=lambda s: s.sweep_i):
            if sw.sweep_i <= guard:
                continue
            out.append(sw)
            if sw.reclaim_i is not None:
                guard = int(sw.reclaim_i)
    return out


def sweep_forward(sw: Sweep, f, H: tuple[int, ...] = H_BARS,
                  last_i: int | None = None) -> dict:
    """Forward net per horizon, IN THE R THE ADMITTED LANE WOULD HAVE USED.

    ANCHOR: the RECLAIM bar's CLOSE.  Two reasons, both the estate's own: it is
    the exact price the 363 admitted signals enter at (`entry_px = f.c[reclaim_i]`
    in `replay`), and census-2B's R-1 ruling is that the reclaim bar "is the bar
    the event completes and the first bar at which it is knowable".  REFUSED
    SWEEPS HAVE A RECLAIM BAR — the tide refused, the reclaim did not.

    UNIT: an EXACT R, not an ATR proxy.  `RC.spring_stop` is a pure function of
    (Spring, entry_px, atr_sig, rail_atr) and needs no replay, so the refused
    population is denominated in THE SAME R the admitted lane would have used on
    that very sweep.  That is what makes "beside the admitted line" a comparison
    rather than a juxtaposition.  ATR is taken at the RECLAIM bar, not the sweep
    bar, because that is the ATR `replay` feeds `spring_stop`; ATR-at-sweep would
    denominate the two populations differently.

    THE TOLL IS CHARGED AND ALSO PUBLISHED AS ITS OWN COLUMN, because the admitted
    side is net of one and census-2B's note m8 is that "the toll must be measured
    where the returns are normalised".  Both faces are printed.

    NO CLAMPING.  A horizon that runs off the corridor is NaN, never a truncated
    window relabelled H100.  `last_i` IS THE CORRIDOR'S LAST BAR AND IS PASSED
    IN, not taken as `len(f.c) - 1`: today the two coincide on every asset, and a
    study whose forward window silently widens the day one asset's cache runs a
    bar longer than the panel's is a study that reads bars its own corridor
    excludes.

    WHAT WOULD MAKE THIS WRONG: an anchor other than the reclaim close; ATR at the
    sweep bar; a clamped horizon; a toll charged on one population and not the
    other; or an R re-derived from the ATR instead of taken from `spring_stop`.
    """
    j = sw.reclaim_i
    empty = {"r_dist": None, "toll_r": None}
    for h in H:
        empty[f"h{h}_gross_r"] = None
        empty[f"h{h}_net_r"] = None
    if j is None:
        return empty
    entry = float(f.c[j])
    atr = float(f.atr[j])
    stp = _ORIG_SPRING_STOP(
        RC.Spring(direction=sw.direction, sweep_i=sw.sweep_i,
                  sweep_ms=sw.sweep_ms, sweep_extreme=sw.sweep_extreme,
                  swept_level=sw.swept_level, reclaim_i=j,
                  reclaim_ms=int(sw.reclaim_ms), bars_to_reclaim=int(sw.bars_to_reclaim)),
        entry, atr, RC.MIN_STOP_ATR)
    if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
        return empty
    toll = (RC.V5.FEE_BPS_ROUND_TRIP / 1e4) * entry          # price, one round trip
    out = {"r_dist": float(stp.r_dist), "toll_r": float(toll / stp.r_dist)}
    last = (len(f.c) - 1) if last_i is None else min(int(last_i), len(f.c) - 1)
    for h in H:
        k = j + h
        if k > last:
            out[f"h{h}_gross_r"] = None
            out[f"h{h}_net_r"] = None
        else:
            g = (float(f.c[k]) - entry) * sw.direction
            out[f"h{h}_gross_r"] = float(g / stp.r_dist)
            out[f"h{h}_net_r"] = float((g - toll) / stp.r_dist)
    return out


def sprnt_sweeps(lo_ms: int, hi_ms: int) -> tuple[pd.DataFrame, dict]:
    """Every penetration in the corridor, with its fate and its forward returns.

    THE CORRIDOR IS WARM-UP FLOORED — `lo_i = max(lo_i, RC.WARMUP_BARS)`, exactly
    as `tierc6.replay` floors the lane.  That single line is DEFECT (1) of the
    filed 3,526: the manifest's counting call has no floor, so 56 refusals live
    entirely inside the first 316 bars where `ind.ema` is seeded and the tide gate
    is evaluable and WRONG.  Measuring the refused population on a corridor the
    admitted population never traded would compare two different windows.

    BOTH LEGS OF THE PARENT ARE CHECKED, NOT JUST THE ADMITTED ONE.  DEFECT-1's
    number is a SUBTRACTION across two code paths — the parent's unfloored
    `spring_signals.last_tide_rejected` minus this scan's floored
    `refused_on_tide` count — and that subtraction is only a measurement of the
    FLOOR if the two paths agree on a common corridor.  So the refused leg is
    checked here by cardinality, on the floored corridor, exactly as the
    admitted leg is: `parent_refused == scan_refused` or HALT.  Without it the
    56 could be a floor effect, a scan defect, or any mixture of the two, and
    nothing in the table would say which.

    WHAT WOULD MAKE THIS WRONG: dropping the floor; running the scan over a
    corridor different from `replay`'s; letting the parent-equality assertion
    pass vacuously on an empty asset; or checking the admitted leg alone and
    then subtracting on the refused one.
    """
    rows = []
    checks = {"assets": 0, "parent_signals": 0, "scan_admitted": 0,
              "elementwise_equal": 0, "penetrations_vectorised": 0,
              "penetrations_partitioned": 0, "assets_with_zero_signals": 0,
              "parent_refused": 0, "scan_refused": 0,
              "both_directions_same_bar": 0}
    for sym in RC.UNIVERSE:
        f = T6.frame(sym)["f"]
        a, b = T6._idx_range(f.open_ms, lo_ms, hi_ms)
        a = max(a, RC.WARMUP_BARS)
        if b < a:
            continue
        checks["assets"] += 1
        parent = _parent_springs(f, a, b)
        mine, sweeps = spring_scan(f, a, b)
        checks["parent_signals"] += len(parent)
        checks["scan_admitted"] += len(mine)
        checks["parent_refused"] += int(_parent_springs.last_tide_rejected)
        checks["scan_refused"] += sum(1 for z in sweeps
                                      if z.fate == "refused_on_tide")
        if len(parent) == 0:
            checks["assets_with_zero_signals"] += 1
        if len(parent) == len(mine) and all(
                (p.direction, p.sweep_i, p.reclaim_i, p.bars_to_reclaim,
                 float(p.sweep_extreme), float(p.swept_level))
                == (q.direction, q.sweep_i, q.reclaim_i, q.bars_to_reclaim,
                    float(q.sweep_extreme), float(q.swept_level))
                for p, q in zip(parent, mine)):
            checks["elementwise_equal"] += len(mine)
        pc = penetration_count(f, a, b)
        checks["penetrations_vectorised"] += pc["total"]
        checks["penetrations_partitioned"] += len(sweeps)
        checks["both_directions_same_bar"] += pc["both_directions_same_bar"]
        # EPISODE HEADS ARE KEYED BY (fate, direction, sweep_i), NOT BY OBJECT
        # IDENTITY.  `sweep_i` is unique within a (fate, direction) leg on one
        # asset, and a key that survives a copy of the record is a key a reader
        # can reproduce from the written table.
        keep: set[tuple] = set()
        for fate in ("admitted", "refused_on_tide", "unreclaimed",
                     "truncated_at_corridor_end"):
            for s in collapse_episodes([z for z in sweeps if z.fate == fate]):
                keep.add((fate, s.direction, s.sweep_i))
        for sw in sweeps:
            fw = sweep_forward(sw, f, last_i=b)
            rows.append({
                "asset": sym, "fate": sw.fate,
                "direction": "long" if sw.direction == 1 else "short",
                "direction_i": sw.direction,
                "sweep_ts": iso(sw.sweep_ms), "sweep_ms": sw.sweep_ms,
                "reclaim_ts": (iso(int(sw.reclaim_ms))
                               if sw.reclaim_ms is not None else ""),
                "bars_to_reclaim": sw.bars_to_reclaim,
                "swept_level": r6(sw.swept_level),
                "sweep_extreme": r6(sw.sweep_extreme),
                # A SWEEP WITH NO RECLAIM BAR HAS NO ANCHOR, AND THAT IS A
                # DIFFERENT KIND OF MISSING from a horizon that ran off the end
                # of the corridor.  The two are counted in separate columns
                # downstream; merging them would report "no forward return
                # available" for two incomparable reasons under one number.
                "has_anchor": bool(sw.reclaim_i is not None),
                "is_episode_head": bool((sw.fate, sw.direction, sw.sweep_i)
                                        in keep),
                **{k: (r6(v) if isinstance(v, float) else v)
                   for k, v in fw.items()},
            })
    if checks["elementwise_equal"] != checks["parent_signals"]:
        raise SystemExit(
            "HALT: spring_scan's admitted leg is not the parent's. parent="
            f"{checks['parent_signals']} scan={checks['scan_admitted']} "
            f"elementwise-equal={checks['elementwise_equal']}")
    if checks["scan_refused"] != checks["parent_refused"]:
        raise SystemExit(
            "HALT: spring_scan's REFUSED leg is not the parent's on the floored "
            f"corridor. parent={checks['parent_refused']} "
            f"scan={checks['scan_refused']} — DEFECT-1's figure subtracts these "
            "two paths and is only a floor measurement while they agree.")
    if checks["penetrations_vectorised"] != checks["penetrations_partitioned"]:
        raise SystemExit(
            "HALT: the four-fate partition does not close against a vectorised "
            f"re-count. vectorised={checks['penetrations_vectorised']} "
            f"partitioned={checks['penetrations_partitioned']}")
    if checks["assets"] == 0 or checks["parent_signals"] == 0:
        raise SystemExit("HALT: the parent-equality leg passed vacuously.")
    if checks["parent_refused"] == 0:
        raise SystemExit("HALT: the refused-leg equality passed vacuously.")
    return pd.DataFrame(rows), checks


def _parent_springs(f, lo_i: int, hi_i: int) -> list:
    """`RC.spring_signals` plus its function-attribute refusal count, captured
    together so the two can never be read from different calls."""
    sig = RC.spring_signals(f, lo_i, hi_i)
    _parent_springs.last_tide_rejected = RC.spring_signals.last_tide_rejected
    return sig


_parent_springs.last_tide_rejected = 0


def sprnt_lab(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """L-SPR-NT [F-C5-i] — the tide-neutral spring line.  TIER-E, FULL CORRIDOR.

    CLASS: Tier-E.  It gates nothing, changes no card knob, moves no
    entry/exit/stop/fill and produces no `Card` and no fleet row — exactly the
    class of the league and the midband.

    WINDOW: NOT the league's `TIER_E_FROM`.  The 3,470/363 counts are
    full-corridor and cutting the refusals to 2025-10-01 would compare a
    truncated refusal set against a full admitted set.  `tier` and `window` are
    separate columns on every row so the two meanings can never be conflated
    again.

    WHAT THIS TABLE PUBLISHES, AND WHY EACH COLUMN IS THERE:
      · all FOUR sweep fates, per direction and pooled — the partition does not
        close without the never-reclaimed leg, and it does not close honestly
        without the truncated one;
      · `became_a_campaign` = 241, published as a COLUMN, never as a denominator
        — it is CAMPAIGNS, after one-position-per-asset drops candidates, and the
        comparable population is the 363 SIGNALS;
      · the raw count AND the episode-collapsed count, because `spring_signals`
        emits once per sweep bar with no non-overlap guard;
      · forward H20/H100 in the EXACT R the admitted lane would have used, gross
        and net, with the toll as its own column and the horizon DURATIONS
        printed (80h / 400h) so nobody reads them as census-2B's duration-fixed
        R-1 horizons, which are INFEASIBLE on a 4h lens;
      · an asset-cluster bootstrap CI per scored cell, `m = 8` for BH.

    WHAT WOULD MAKE THIS WRONG: an unfloored corridor; 241 used as a denominator;
    the never-reclaimed leg omitted; a horizon clamped rather than NaN'd; a toll
    charged on one population and not the other; or scoring the bootstrap on rows
    rather than on ASSET clusters (the unit of replication is the asset).
    """
    sw, checks = sprnt_sweeps(lo_ms, hi_ms)
    # THE FILED COMPARATOR, MEASURED UNDER BOTH CARDS.  241 is the manifest's
    # number and it is reproduced here EXACTLY by the v5 control; the same lane
    # under the v6 card is 236.  That drift is the second half of DEFECT-2 and
    # is the reason a campaign count can never be the denominator of a
    # signal-level study: it MOVES WITH THE CARD, while the 363 signals do not.
    became_v6 = len(T6.run_cell(
        RC.Card(name="spring v6", grid="P-SPR-1", lane="spring"), lo_ms, hi_ms))
    became_v5 = len(T6.run_cell(
        replace(RC.CARD_V5_CONTROL, name="spring v5", grid="P-SPR-1",
                lane="spring"), lo_ms, hi_ms))

    # the filed, UNFLOORED numbers — re-measured here so the defect is a
    # measurement and not a quotation
    unf_sig = unf_ref = 0
    for s in RC.UNIVERSE:
        f = T6.frame(s)["f"]
        a, b = T6._idx_range(f.open_ms, lo_ms, hi_ms)
        if b < a:
            continue
        unf_sig += len(_parent_springs(f, a, b))
        unf_ref += int(_parent_springs.last_tide_rejected)

    rows: list[dict] = []
    fates = ("admitted", "refused_on_tide", "unreclaimed",
             "truncated_at_corridor_end")
    for fate in fates:
        for dname in ("ALL", "long", "short"):
            m = sw[sw["fate"] == fate]
            if dname != "ALL":
                m = m[m["direction"] == dname]
            n = len(m)
            row = {
                "row_kind": "population",
                "population": fate, "direction": dname, "n": int(n),
                "n_episodes": int(m["is_episode_head"].sum()) if n else 0,
                "n_with_anchor": int(m["has_anchor"].sum()) if n else 0,
                "became_a_campaign_v5_filed": (became_v5 if fate == "admitted"
                                               and dname == "ALL" else None),
                "became_a_campaign_v6": (became_v6 if fate == "admitted" and
                                         dname == "ALL" else None),
                "became_a_campaign_note":
                    ("the manifest's 241 — CAMPAIGNS, after "
                     "one-position-per-asset drops candidates. Reproduced here "
                     "by the v5 control; the v6 card gives a DIFFERENT number "
                     "on the same signals. NEVER a denominator."
                     if fate == "admitted" and dname == "ALL" else ""),
                "provisional": _provisional(n),
            }
            anch = m[m["has_anchor"]] if n else m
            for h in H_BARS:
                gc, nc = f"h{h}_gross_r", f"h{h}_net_r"
                ok = anch[anch[nc].notna()] if len(anch) else anch
                vals = ok[nc].to_numpy(float) if len(ok) else np.zeros(0)
                clus = ok["asset"].to_numpy() if len(ok) else np.zeros(0)
                row[f"h{h}_hours"] = H_HOURS[h]
                row[f"h{h}_n_scored"] = int(len(vals))
                # THE TWO KINDS OF MISSING, COUNTED APART.  `no_anchor` is a
                # sweep that never reclaimed and therefore has no entry price to
                # measure forward from; `offcorridor` is an anchored sweep whose
                # horizon runs past the last closed bar and is NaN'd rather than
                # clamped.  One number for both would hide which is which.
                row[f"h{h}_n_no_anchor"] = int(n - len(anch))
                row[f"h{h}_n_offcorridor_nan"] = int(len(anch) - len(vals))
                row[f"h{h}_mean_gross_r"] = (
                    r6(float(ok[gc].dropna().mean()))
                    if len(ok) and ok[gc].notna().any() else None)
                row[f"h{h}_mean_net_r"] = (
                    r6(float(vals.mean())) if len(vals) else None)
                row[f"h{h}_median_net_r"] = (
                    r6(float(np.median(vals))) if len(vals) else None)
                row[f"h{h}_pos_pct"] = (pct(int((vals > 0).sum()), len(vals))
                                        if len(vals) else None)
                if len(vals) >= RC.PROVISIONAL_MIN_N and len(set(clus)) > 1:
                    draws = T6.cluster_boot(vals, clus, seed=SEED, n_boot=4000)
                    ci = T6._ci_from(draws, float(vals.mean()))
                    row[f"h{h}_ci_lo"] = r6(ci["lo"])
                    row[f"h{h}_ci_hi"] = r6(ci["hi"])
                    row[f"h{h}_p_one_sided"] = r6(ci["p_one_sided"])
                else:
                    row[f"h{h}_ci_lo"] = row[f"h{h}_ci_hi"] = None
                    row[f"h{h}_p_one_sided"] = None
            row["mean_toll_r"] = (r6(float(m["toll_r"].dropna().mean()))
                                  if n and m["toll_r"].notna().any() else None)
            rows.append(row)

    tot_ref = int((sw["fate"] == "refused_on_tide").sum())
    tot_adm = int((sw["fate"] == "admitted").sum())
    tot_unr = int((sw["fate"] == "unreclaimed").sum())
    tot_trunc = int((sw["fate"] == "truncated_at_corridor_end").sum())
    ref_eps = int(sw[sw["fate"] == "refused_on_tide"]["is_episode_head"].sum())
    rows += [
        {"row_kind": "defect", "population": "DEFECT-1 no warm-up floor",
         "direction": "ALL", "n": tot_ref,
         "filed_value": unf_ref, "measured_value": tot_ref,
         "defect": "the manifest's counting call passes _idx_range straight in "
                   "with NO warm-up floor, where `replay` floors the lane at "
                   f"WARMUP_BARS={RC.WARMUP_BARS}. "
                   f"{unf_ref - tot_ref} refusals live entirely inside the "
                   "warm-up, where ind.ema is SEEDED and the tide gate is "
                   "evaluable and WRONG. The same unfloored call also inflates "
                   f"the ADMITTED signal count, {unf_sig} vs {tot_adm} — a "
                   "second face of the same defect, not in the manifest at all."},
        {"row_kind": "defect", "population": "DEFECT-2 wrong comparator",
         "direction": "ALL", "n": tot_adm,
         "filed_value": became_v5, "measured_value": tot_adm,
         "defect": "the filed comparator is CAMPAIGNS (the spring lane's book), "
                   "not SIGNALS. A forward-return study anchored at the reclaim "
                   "close must compare refusals against admitted SIGNALS; the "
                   "campaign count is published as a column and never as a "
                   f"denominator. It is also CARD-DEPENDENT — {became_v5} under "
                   f"the v5 control, {became_v6} under the v6 card, on the same "
                   f"{tot_adm} signals — so it cannot denominate anything at "
                   "the signal level even in principle."},
        {"row_kind": "defect", "population": "DEFECT-3 population counted nowhere",
         "direction": "ALL", "n": tot_unr,
         "filed_value": 0, "measured_value": tot_unr,
         "defect": "sweeps that penetrated and never closed back inside within "
                   "reclaim_bars fall through spring_signals' inner loop and are "
                   "counted nowhere in the estate. census-2B tracks exactly this "
                   "as n_unreclaimed. Without it the sweep population does not "
                   f"close: {tot_adm} + {tot_ref} + {tot_unr} + {tot_trunc} = "
                   f"{tot_adm + tot_ref + tot_unr + tot_trunc} penetrations."},
        {"row_kind": "defect", "population": "DEFECT-4 no non-overlap guard",
         "direction": "ALL", "n": tot_ref,
         "filed_value": tot_ref, "measured_value": ref_eps,
         "defect": "spring_signals emits ONCE PER SWEEP BAR with no greedy "
                   "non-overlap guard, unlike census-2B's springs_for_cell. "
                   f"Episode-collapsed the refused line is {ref_eps}, not "
                   f"{tot_ref}. Both are published; cluster on assets, score on "
                   "episodes."},
        {"row_kind": "closure", "population": "PARTITION CLOSES",
         "direction": "ALL", "n": tot_adm + tot_ref + tot_unr + tot_trunc,
         "filed_value": checks["penetrations_vectorised"],
         "measured_value": checks["penetrations_partitioned"],
         "defect": "penetration count re-derived by a VECTORISED rolling window "
                   "(no shared code with the scan) equals the sum of the four "
                   "fates. A check satisfied by one example is not a check; this "
                   "one is a cardinality identity over every asset. "
                   f"{checks['both_directions_same_bar']} bar(s) in the corridor "
                   "penetrate in BOTH directions and count as two penetrations "
                   "each, which is why the total is long+short and not a count "
                   "of bars."},
        {"row_kind": "closure", "population": "REFUSED LEG IS THE PARENT'S",
         "direction": "ALL", "n": tot_ref,
         "filed_value": checks["parent_refused"],
         "measured_value": checks["scan_refused"],
         "defect": "DEFECT-1's figure is a SUBTRACTION across two code paths — "
                   "the parent's unfloored last_tide_rejected minus this scan's "
                   "floored refused_on_tide. It measures the FLOOR only while "
                   "the two paths agree on a COMMON corridor, so that equality "
                   "is asserted by cardinality here (HALT on one disagreement), "
                   "exactly as the admitted leg already was. Without this row "
                   f"the {unf_ref - tot_ref} could be a floor effect, a scan "
                   "defect, or any mixture."},
    ]
    df = pd.DataFrame(rows)
    df["tier"] = "E (measurement — gates nothing, moves no fill)"
    df["window"] = "full corridor (panel start -> latest closed 4h)"
    df["anchor"] = "the RECLAIM bar's CLOSE — the admitted lane's own entry price"
    df["unit"] = ("exact R from RC.spring_stop(sweep_extreme, ATR at the RECLAIM "
                  "bar, rail=MIN_STOP_ATR) — the R the admitted lane would have "
                  "used on this very sweep")
    df["horizon_reading"] = ("BAR COUNTS (tierc5.MIDBAND_H), NOT census-2B's "
                             "duration-fixed R-1 horizons, which resolve to 0 "
                             "bars on a 4h lens and are INFEASIBLE. H20 = 80h, "
                             "H100 = 400h.")
    df["bh_family_m"] = FDR_FAMILY_M_SPRNT
    df["bh_q"] = FDR_Q
    return df


# ══════════════════════════════════════════════════════════════════ THE SHADOWS
@dataclass(frozen=True)
class Card6(RC.Card):
    """`RC.Card`, three shadow knobs wider.  `isinstance(c, RC.Card)` HOLDS.

    THE THREE KNOBS DO NOT EXIST ON `RC.Card` AND THE PARENT CANNOT READ THEM.
    They are bound at their SITES by `_knobs()` for the duration of one cell —
    see the module docstring for why that beats forking `_ride` and `replay`.

    `diff_from_v5` (inherited) CANNOT SEE THESE FIELDS, which is precisely the
    trap the spec flags: a cell whose difference is invisible prints "(the
    ratified card)" on the table's own face.  `diff_from_card` below is the
    method the tables use, and it compares against the v6 CARD over the full
    field set including these three.
    """
    entry_buf_atr: float = RC.STOP_BUF_ATR          # S-OFFSET {0.25,0.50,0.75}
    trail_buf_atr: float = _ORIG_RATCHET_BUF        # S-BUF   {0.15,0.25,0.35}
    wall_aware_stop: bool = False                   # S-BUF wall-aware cell [H4]

    def diff_from_card(self) -> str:
        """What this cell changes against the RATIFIED v6 CARD, in words.

        WHAT WOULD MAKE THIS WRONG: omitting a field from the tuple below. A knob
        that moves and is not listed here is a cell that lies about itself on the
        table's face — the exact failure `diff_from_v5` has for the three fields
        this class adds.
        """
        base = Card6()
        out = []
        for f_ in ("entry_rail_atr", "lane", "limit_ae_mult", "trail", "trail_l",
                   "trail_r", "trail_extra_buf_atr", "trail_arm_after_r",
                   "harvest", "harvest_fixed_r", "harvest_min_unit_r",
                   "time_stop_bars", "funding_ceiling_r", "adds_max", "add_size",
                   "seal_open", "trail_min_advance_atr", "harvest_frac",
                   "wall_exit_atr", "wall_tf", "entry_buf_atr", "trail_buf_atr",
                   "wall_aware_stop"):
            a, b = getattr(base, f_), getattr(self, f_)
            if a != b:
                out.append(f"{f_}={b}")
        return " · ".join(out) or "(the ratified v6 card)"


# THE GRID SIZES, DECLARED AS A LITERAL AND INDEPENDENT OF THE CODE THAT BUILDS
# THE CELLS.  Three independent things must agree: this literal, the cards
# `fleet_cards6()` builds, and the rows `shadow_table` writes.  Counting the
# builder on both sides is the same object counted twice and is banned.
GRID_SIZES6: dict[str, int] = {
    "card": 1, "S-RAIL": 2, "S-HARV": 2, "S-CLOCK": 2, "S-TRAIL": 3,
    "S-OFFSETxMINADV": 9, "S-BUF": 4, "S-HFRAC": 2,
    "S-SIZE": 4, "S-ADDSIZE": 4, "S-LIMIT": 5, "registration arms": 3,
}

# The grids `fleet_cards6()` actually builds CARDS for.  S-SIZE, S-ADDSIZE,
# S-LIMIT and the registration arms are declared in the literal because they are
# part of the SELECTION SURFACE, but they are built by their own overlays
# (`size_grid`, `addsize_grid`, `limit_grid`, `score_registrations`) and not by a
# `Card`.  Saying which is which is the difference between a literal that can be
# checked and a literal that cannot.
GRIDS_BUILT_HERE: tuple[str, ...] = ("card", "S-RAIL", "S-HARV", "S-CLOCK",
                                     "S-TRAIL", "S-OFFSETxMINADV", "S-BUF",
                                     "S-HFRAC")
# THE FLEET'S OWN SURFACE ONLY.  Tier-C5's `total_cells_excluding_the_card`
# also folds in the league's eligible panel cells, which are counted where they
# are built (`tierc6.league`) and are NOT in this literal.  Adding a number this
# module cannot check to a literal this module HALTs on would make the HALT
# unenforceable — so the two surfaces are kept apart and both are published.
FLEET_CELLS_EXCLUDING_THE_CARD = sum(v for k, v in GRID_SIZES6.items()
                                     if k != "card")
NEW_IN_C6 = ("S-OFFSETxMINADV", "S-BUF", "S-HFRAC")
CELLS_ADDED_BY_C6 = sum(GRID_SIZES6[g] for g in NEW_IN_C6)   # 15, 1 of them the card


def fleet_cards6() -> list[RC.Card]:
    """EVERY CELL, PRE-NAMED, BEFORE ANY OF THEM RAN.

    Tier-C5's four families are carried forward VERBATIM so the grid-size literal
    is checkable whole, and the three new families are added.  Note that Tier-C5's
    `S-TRAIL arms after +1R` cell IS the v6 card — `trail_arm_after_r = 1.0` was
    promoted from that shadow by ruling H5 — and the cell is ridden anyway with
    `identical_to_card` marked on its row.  A promoted cell that quietly vanishes
    from the surface it was selected out of is the exact disclosure failure the
    idling guard exists to make visible.

    WHAT WOULD MAKE THIS WRONG: a grid whose built count differs from
    `GRID_SIZES6` (HALTed in `shadow_table`); a cell that differs from the card in
    more ways than its name says; or a cell added after the look.
    """
    C = Card6
    out: list[RC.Card] = [C(name="v6 (the card)", grid="card")]
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
    # S-OFFSET x S-MINADV — a 3x3 CROSS, REPORTED WHOLE.  Nothing is
    # marginalised to a 3 + 3.  Under v6 the cell that IS the ratified card is
    # (0.50, 0.05), NOT (0.50, 0.00): F-C4-d ratified a 0.05 minimum advance, so
    # (0.50, 0.00) is the v5-TRAIL control.  Both identities are CHECKED.
    out += [C(name=f"S-OFFSET {o:.2f} x S-MINADV {a:.2f}",
              grid="S-OFFSETxMINADV", entry_buf_atr=o, trail_min_advance_atr=a)
            for o in (0.25, 0.50, 0.75) for a in (0.00, 0.05, 0.10)]
    # S-BUF — the RATCHET's 'beyond', tighter than the card's 0.50 in all three
    # cells, plus the wall-aware cell that makes the buffer CONDITIONAL.
    out += [C(name=f"S-BUF {b:.2f}", grid="S-BUF", trail_buf_atr=b)
            for b in (0.15, 0.25, 0.35)]
    out += [C(name="S-BUF wall-aware (0.25, cleared past a heavy band)",
              grid="S-BUF", trail_buf_atr=0.25, wall_aware_stop=True)]
    # S-HFRAC — 50% is the RULED default [H3] and is NOT a cell here: it is the
    # card, already on the first row of this table.
    out += [C(name="S-HFRAC 33%", grid="S-HFRAC", harvest_frac=0.33),
            C(name="S-HFRAC 67%", grid="S-HFRAC", harvest_frac=0.67)]
    return out


def restop(stp, entry_px: float, atr_sig: float, direction: int,
           buf_atr: float, rail_atr: float):
    """Re-place the parent's OWN anchor at a different 'beyond'.

    EXACT, NOT APPROXIMATE, AND NOT A COPY OF THE PARENT'S SELECTION LOGIC.
    `struct_stop_4h` chooses its anchor with an eligibility test that reads only
    `val < entry_px` (mirrored for a short) and an argmax over VALUES — the
    buffer appears nowhere in the choice.  So the parent's chosen anchor can be
    re-buffered afterwards and the result is the stop the parent would have
    returned had `STOP_BUF_ATR` been the new value.  `spring_stop` has the same
    shape with `anchor = sweep_extreme`, so one function serves both.

    WHAT WOULD MAKE THIS FAIL: called with the card's own buf/rail it must return
    the parent's Stop BIT FOR BIT.  `restop_identity` asserts that over every
    eligible anchor in the corridor and reports the count — not one example.
    """
    d = int(direction)
    pivot = float(stp.anchor) - d * float(buf_atr) * float(atr_sig)
    rail = float(entry_px) - d * float(rail_atr) * float(atr_sig)
    px = min(pivot, rail) if d == 1 else max(pivot, rail)
    pdist = abs(float(entry_px) - pivot)
    rdist = float(rail_atr) * float(atr_sig)
    return replace(stp, stop_px=float(px), pivot_stop_px=float(pivot),
                   pivot_dist=float(pdist), rail_dist=float(rdist),
                   r_dist=float(abs(float(entry_px) - px)),
                   rail_binding=bool(rdist > pdist))


def restop_identity(lo_ms: int, hi_ms: int) -> dict:
    """`restop` at the card's own buffer must reproduce the parent Stop exactly.

    Walks EVERY bar of the floored corridor on EVERY asset in BOTH directions,
    asks the parent for its Stop, re-places it at the card's own buffer, and
    compares all seven arithmetic fields.  A cardinality result, not an example:
    the number compared and the number matched are both returned and a single
    mismatch HALTs.

    WHAT WOULD MAKE THIS WRONG: comparing only `stop_px` (the rail could bind and
    hide a wrong pivot); skipping the short side; or running it on a corridor the
    fleet does not trade.
    """
    n_cmp = n_ok = 0
    for sym in RC.UNIVERSE:
        st = T6.frame(sym)
        f, pv = st["f"], st["pv4"]
        a, b = T6._idx_range(f.open_ms, lo_ms, hi_ms)
        a = max(a, RC.WARMUP_BARS)
        for i in range(a, b + 1):
            entry = float(f.c[i])
            atr = float(f.atr[i])
            if not (np.isfinite(atr) and atr > 0):
                continue
            for d in (1, -1):
                p = _ORIG_STRUCT_STOP(pv, i, entry, d, atr,
                                      min_stop_atr=RC.MIN_STOP_ATR,
                                      forbidden=None)
                if p is None:
                    continue
                q = restop(p, entry, atr, d, RC.STOP_BUF_ATR, RC.MIN_STOP_ATR)
                n_cmp += 1
                if all(abs(getattr(p, k) - getattr(q, k)) <= 0.0
                       for k in ("stop_px", "pivot_stop_px", "pivot_dist",
                                 "rail_dist", "r_dist", "anchor")) and \
                        p.rail_binding == q.rail_binding and \
                        p.anchor_bar == q.anchor_bar and \
                        p.n_eligible == q.n_eligible:
                    n_ok += 1
    if n_cmp == 0 or n_ok != n_cmp:
        raise SystemExit(f"HALT: restop is not the parent. {n_ok}/{n_cmp}")
    return {"anchors_compared": n_cmp, "anchors_identical": n_ok}


# ── the wall-aware cell [H4] ─────────────────────────────────────────────────
_BANDS: dict[str, dict[str, tuple[np.ndarray, np.ndarray]]] = {}
_BANDS_BY_CLOCK: dict[tuple, dict] = {}


def band_context(sym: str) -> dict[str, tuple[np.ndarray, np.ndarray]]:
    """The MH-or-heavier bands, RETAINED SEPARATELY — not collapsed to an envelope.

    `RC.add_context` cannot be reused: it collapses the four families into a
    single `heavy_lo/heavy_hi` ENVELOPE that also contains the GAPS between them.
    Against the envelope the card's stop lands "inside a heavy band" far more
    often than it does against any real band, and the extra hits are gaps.  The
    per-band disjunction is the right predicate and it needs the bands apart.

    Everything read here is already in the decision path: `V5.ribbon_band` uses
    `engine.indicators.ema` and imports no analytics.  The estate's canonical
    wall (`_single_wall`) is NOT usable in a decision cell — it lives in a module
    that imports analytics transitively and it measures in DAILY ATR resampled
    through the analytics estate.

    WHAT WOULD MAKE THIS WRONG: using the envelope; using the filed census-2B
    2-member ribbon envelope under the name `ribbon_band`; or naming a field with
    a banned tape substring (`wall_family`, anything containing `dist_atr`).
    """
    if sym not in _BANDS:
        c = T6.frame(sym)["f"].c
        _BANDS[sym] = {nm: ribbon_band(c, nm) for nm in MH_OR_HEAVIER}
    return _BANDS[sym]


def _clock_key(open_ms: np.ndarray) -> tuple:
    return (len(open_ms), int(open_ms[0]), int(open_ms[-1]))


def _band_lookup(open_ms: np.ndarray) -> dict:
    """Bands for the asset whose 4h clock is `open_ms` — keyed, and the key is
    PROVEN INJECTIVE rather than assumed.

    THE KEY IS A SUMMARY, SO IT MUST BE CHECKED FOR COLLISIONS.  `_clock_key` is
    `(len, first_open, last_open)`; two assets sharing all three would map to one
    slot and the SECOND would silently be served the FIRST's bands — every band
    test in the wall-aware cell then run against the wrong asset's prices, with
    no error anywhere.  The map is therefore built with a cardinality assertion
    (`len(map) == len(UNIVERSE)`) instead of a lookup on one asset, which is the
    check that was actually available.

    WHAT WOULD MAKE THIS WRONG: building the map without the injectivity
    assertion; or warming it against a single asset's clock and calling that a
    validation of the map.
    """
    if not _BANDS_BY_CLOCK:
        for s in RC.UNIVERSE:
            _BANDS_BY_CLOCK[_clock_key(T6.frame(s)["f"].open_ms)] = band_context(s)
        if len(_BANDS_BY_CLOCK) != len(RC.UNIVERSE):
            raise SystemExit(
                f"HALT: _clock_key is not injective over the universe — "
                f"{len(RC.UNIVERSE)} assets collapsed to {len(_BANDS_BY_CLOCK)} "
                "keys, so at least one asset would be served another's bands.")
    k = _clock_key(open_ms)
    if k not in _BANDS_BY_CLOCK:
        raise SystemExit("HALT: the wall-aware cell was handed a clock it has no "
                         "bands for — the frame cache and the band cache have "
                         "diverged.")
    return _BANDS_BY_CLOCK[k]


def wall_aware_trail_step(fr, j: int, direction: int, cur_stop: float,
                          close: float, atr: float, open_ms: np.ndarray,
                          buf_atr: float, rail_atr: float,
                          forbidden: np.ndarray | None = None,
                          min_advance_atr: float = 0.0):
    """S-BUF's wall-aware cell [H4] — ONE exact predicate, on top of the parent.

        WALL-AWARE(j, direction, cand) == exists nm in {MH,H,VH,UH} with
                                         lo_nm[j] <= cand <= hi_nm[j]

    where `cand` is the BUFFERED CANDIDATE STOP the parent already computed
    (`Advance.cand_px`).  When it holds the cell places the stop BEYOND THE
    BAND'S FAR EDGE instead — `lo_nm[j] - buf*ATR[j]` for a long, `hi_nm[j] +
    buf*ATR[j]` for a short, ties broken by the WIDEST band so the result is
    unique.  When it does not hold the cell IS the `S-BUF 0.25` cell exactly,
    which is what makes it a CELL OF S-BUF and not a fourth family.

    THE PARENT DOES THE SELECTION.  The pivot lookup, the seal mask, the rail and
    the monotone test are the parent's objects running the parent's code; this
    wrapper only re-places the candidate and re-rails it.  The minimum-advance
    gate is applied AFTER the re-placement (the parent is called with the gate
    off), because widening a stop can shrink the movement below the threshold and
    a gate measured before the last thing that moves the stop is a gate that
    reports on a quantity it did not test.

    THE CELL CAN ONLY EVER BE A SUBSET OF ITS PARENT, and that is provable rather
    than hoped: for a long `cand' < cand` (the band's low edge minus a buffer is
    below a point inside the band), so `admitted' <= admitted`, so any bar on
    which the parent refused to advance is a bar on which this cell also refuses.

    WHAT WOULD MAKE THIS WRONG: testing the predicate against the ENVELOPE of the
    four bands rather than each band separately (the gaps would fire it);
    applying it to the RAILED stop rather than the candidate (the rail is not a
    band); dropping the monotone re-test after re-placement (the stop could move
    backwards); or applying the minimum advance before the re-placement.
    """
    adv = _ORIG_TRAIL_STEP(fr, j, direction, cur_stop, close, atr, open_ms,
                           buf_atr=buf_atr, rail_atr=rail_atr,
                           forbidden=forbidden, min_advance_atr=0.0)
    if adv is None:
        return None
    d = int(direction)
    bands = _band_lookup(open_ms)
    cand = float(adv.cand_px)
    hits = []
    for nm, (blo, bhi) in bands.items():
        lo_j, hi_j = float(blo[j]), float(bhi[j])
        if np.isfinite(lo_j) and np.isfinite(hi_j) and lo_j <= cand <= hi_j:
            hits.append((hi_j - lo_j, nm, lo_j, hi_j))
    if hits:
        _w, _nm, lo_j, hi_j = max(hits, key=lambda z: z[0])
        cand2 = (lo_j - buf_atr * atr) if d == 1 else (hi_j + buf_atr * atr)
        rail = float(adv.rail_px)
        admitted = min(cand2, rail) if d == 1 else max(cand2, rail)
        rail_bound = (rail < cand2) if d == 1 else (rail > cand2)
        if RC.RATCHET_MONOTONE:
            if d == 1 and not (admitted > cur_stop):
                return None
            if d == -1 and not (admitted < cur_stop):
                return None
        adv = replace(adv, cand_px=float(cand2), new_stop=float(admitted),
                      rail_binding=bool(rail_bound),
                      dist_from_close_over_atr=float(abs(close - admitted) / atr))
    if min_advance_atr > 0.0:
        if not (np.isfinite(atr) and atr > 0):
            return None
        if abs(float(adv.new_stop) - float(adv.prev_stop)) / float(atr) \
                < float(min_advance_atr):
            return None
    return adv


# ── the knob harness ─────────────────────────────────────────────────────────
class _knobs:
    """Bind a shadow cell's knobs AT THEIR SITES for the duration of one ride.

    SINGLE-ENTRY, RESTORED BY IDENTITY, AND PROVEN INERT AT CARD VALUES.  Nesting
    HALTs (two cells' knobs live at the same addresses and the second would
    inherit the first's).  Every rebound name is restored in a `finally` and then
    asserted back to its ORIGINAL OBJECT with `is`, so a partially-restored
    harness cannot leak into the next cell and look like a result.

    THE STOP HARNESS IS BOUND UNCONDITIONALLY, EVEN AT THE CARD'S OWN BUFFER,
    AND THAT IS THE POINT.  The obvious optimisation — bind only when the knob
    differs from the card — would make the identity control WORTHLESS: the cell
    that reproduces the card book would be the one cell that never went through
    the harness, so "the harness is inert" would be a claim tested on a path it
    does not take.  Bound always, `S-OFFSET 0.50 x S-MINADV 0.05` reproducing
    `T6.run_cell(CARD_V6)` trade for trade IS a test of `restop`.

    The WALL-AWARE wrapper is the one binding that stays conditional, because it
    is not inert at any value: it re-places every candidate that lands in a heavy
    band, which is the whole of what the cell does.

    WHAT WOULD MAKE THIS WRONG: rebinding a name the parent reads at IMPORT time
    rather than at CALL time (the rebinding would do nothing and the cell would
    silently be the card); binding only when the knob differs (the control would
    then never exercise the harness); restoring by value rather than by identity;
    or letting an exception inside the ride skip the restore.
    """
    _active = False

    def __init__(self, card):
        self.card = card
        self.saved: dict[str, object] = {}

    def __enter__(self):
        if _knobs._active:
            raise SystemExit("HALT: the knob harness is not re-entrant.")
        _knobs._active = True
        c = self.card
        eb = float(getattr(c, "entry_buf_atr", RC.STOP_BUF_ATR))
        tb = float(getattr(c, "trail_buf_atr", _ORIG_RATCHET_BUF))
        wa = bool(getattr(c, "wall_aware_stop", False))
        try:
            # ALWAYS BOUND — see the class docstring. At the card's own buffer
            # `restop` is a no-op proven bit-for-bit by F-C6-RESTOP, so binding
            # it unconditionally costs nothing and buys a control that actually
            # walks the path it certifies.
            self.saved["struct_stop_4h"] = RC.struct_stop_4h
            self.saved["spring_stop"] = RC.spring_stop

            def _ss(pv, cur_i, entry_px, direction, atr_sig,
                    lookback=None, min_stop_atr=RC.MIN_STOP_ATR,
                    forbidden=None, _eb=eb):
                kw = {} if lookback is None else {"lookback": lookback}
                p = _ORIG_STRUCT_STOP(pv, cur_i, entry_px, direction,
                                      atr_sig, min_stop_atr=min_stop_atr,
                                      forbidden=forbidden, **kw)
                if p is None:
                    return None
                return restop(p, entry_px, atr_sig, direction, _eb,
                              min_stop_atr)

            def _sp(sp, entry_px, atr_sig, rail_atr=RC.MIN_STOP_ATR, _eb=eb):
                p = _ORIG_SPRING_STOP(sp, entry_px, atr_sig, rail_atr)
                if p is None:
                    return None
                return restop(p, entry_px, atr_sig, sp.direction, _eb,
                              rail_atr)

            RC.struct_stop_4h = _ss
            RC.spring_stop = _sp
            self.saved["RATCHET_BUF_ATR"] = RC.RATCHET_BUF_ATR
            RC.RATCHET_BUF_ATR = tb
            if wa:
                self.saved["trail_step"] = RC.trail_step
                RC.trail_step = wall_aware_trail_step
                # WARM AND VALIDATE EVERY ASSET, NOT ONE.  Resolving a single
                # asset's clock would prove only that ONE key is present; the
                # loop below asserts the map answers for the whole universe
                # before a single bar is ridden, and `_band_lookup` HALTs if the
                # key is not injective.
                for _s in RC.UNIVERSE:
                    _band_lookup(T6.frame(_s)["f"].open_ms)
        except BaseException:
            self.__exit__(None, None, None)
            raise
        return self

    def __exit__(self, *exc):
        try:
            for k, v in self.saved.items():
                setattr(RC, k, v)
        finally:
            _knobs._active = False
        for name, orig in (("struct_stop_4h", _ORIG_STRUCT_STOP),
                           ("spring_stop", _ORIG_SPRING_STOP),
                           ("trail_step", _ORIG_TRAIL_STEP)):
            if getattr(RC, name) is not orig:
                raise SystemExit(f"HALT: the knob harness leaked {name}.")
        if RC.RATCHET_BUF_ATR != _ORIG_RATCHET_BUF:
            raise SystemExit("HALT: the knob harness leaked RATCHET_BUF_ATR.")
        return False


def run_shadow_cell(card, lo_ms: int, hi_ms: int) -> list:
    """Ride one shadow cell through `tierc6.run_cell` — THE SAME CODE PATH the
    card rides, with the cell's knobs bound at their sites.

    WHAT WOULD MAKE THIS WRONG: a knob left bound after the call (asserted on the
    way out by identity), or a cell whose knobs the harness does not know about —
    which is why `Card6` declares exactly three and `_knobs` binds exactly three.
    """
    with _knobs(card):
        return T6.run_cell(card, lo_ms, hi_ms)


def _same_book(a: list, b: list) -> bool:
    """Trade-for-trade identity of two books, on the quantities that would move
    if a knob had leaked."""
    if len(a) != len(b):
        return False
    ka = sorted((t.symbol, t.entry_ms, t.exit_ms, r6(t.stop_px), r6(t.r_dist),
                 r6(t.net_r), t.exit_reason) for t in a)
    kb = sorted((t.symbol, t.entry_ms, t.exit_ms, r6(t.stop_px), r6(t.r_dist),
                 r6(t.net_r), t.exit_reason) for t in b)
    return ka == kb


def hfrac_enactment(cells: dict[str, list]) -> pd.DataFrame:
    """Was the DECLARED harvest fraction actually ENACTED in the arithmetic?

    THE SUM INVARIANT PROVABLY CANNOT ANSWER THIS.  `n1 + n2 == net` is an
    ALGEBRAIC IDENTITY in `q` for every q in (0,1) — the 0.5 never appears — so a
    cell that declares 0.33 on its row and books 0.5 in its arithmetic passes the
    sum test with room to spare.  A second leg is needed and this is it.

    THE LEG, BY A PATH THAT DOES NOT RE-DERIVE THE ACCOUNTING: on a campaign that
    is IDENTICAL across two S-HFRAC cells (same entry, same exit, same harvest
    bar and price — which is the case, because the fraction changes ACCOUNTING
    ONLY and never the ride), every term of the taken leg is linear in q:
    `g1, fe1, u1` all carry a factor q exactly.  Therefore

        n1(q_a) / q_a  ==  n1(q_b) / q_b

    to floating tolerance, for every shared harvested campaign.  This tests the
    SPLIT, which the sum cannot, and it does so without recomputing `g1` the way
    `_account` computed it.

    THE HALVES SUM IS ALSO CHECKED, at the in-memory 1e-9 — and ONLY where the
    funding ceiling did not bind, because under a bound ceiling `net != n1 + n2`
    by construction regardless of q.

    WHAT WOULD MAKE THIS WRONG: comparing `took_r` across cells as if it were
    like-for-like (at q=0.33 the taken leg is a third of a unit and at q=0.67 two
    thirds — the two are different-sized objects and `harvest_lab`'s `delta_r` is
    comparable WITHIN a cell only); or running the linearity leg on campaigns
    whose rides differ.
    """
    rows = []
    names = list(cells)
    idx = {nm: {(t.symbol, t.entry_ms): t for t in cells[nm]} for nm in names}
    for nm in names:
        bk = cells[nm]
        harvested = [t for t in bk if t.harvested and t.net_r_harvest_half is not None]
        worst_sum = 0.0
        n_sum = 0
        for t in harvested:
            if t.funding_ceiling_bound:
                continue
            n_sum += 1
            worst_sum = max(worst_sum, abs((float(t.net_r_harvest_half)
                                            + float(t.net_r_runner_half))
                                           - float(t.net_r)))
        rows.append({"cell": nm, "n_harvested": len(harvested),
                     "n_sum_checked": n_sum,
                     "worst_halves_sum_abs_err": (r6(worst_sum) if n_sum else None),
                     "halves_sum_tolerance": 1e-9,
                     "halves_sum_passes": bool(n_sum and worst_sum <= 1e-9),
                     "leg": "sum identity (CANNOT detect a wrong split)"})
    # THE LINEARITY LEG MAY NOT BE SKIPPED SILENTLY.  `_CELL_Q` is populated by
    # `shadow_table`; called with a cell it has no `q` for, the old code
    # `continue`d — and the table then printed nothing but sum rows, every one
    # of them "passes", having run ZERO of the checks that can detect a wrong
    # split.  A table that reports all-pass on a leg it never ran is worse than
    # no table, so this HALTs instead.
    missing = [nm for nm in names if _CELL_Q.get(nm) is None]
    if missing:
        raise SystemExit(
            f"HALT: no declared harvest fraction for {missing!r} — the SPLIT "
            "linearity leg cannot run, and the sum identity provably cannot "
            "detect a wrong split. Call shadow_table() first, which declares q "
            "for every S-HFRAC and card cell it rides.")
    if len(names) < 2:
        raise SystemExit(
            f"HALT: the split-linearity leg needs at least two cells at "
            f"DIFFERENT q; {len(names)} given. One cell cannot check a split.")
    n_lin = 0
    # the linearity leg, pairwise
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            qa = _CELL_Q.get(a)
            qb = _CELL_Q.get(b)
            if qa is None or qb is None or qa == qb:
                continue
            n_lin += 1
            shared = 0
            worst = 0.0
            for k, ta in idx[a].items():
                tb = idx[b].get(k)
                if tb is None or not (ta.harvested and tb.harvested):
                    continue
                if (ta.exit_i, ta.harvest_i) != (tb.exit_i, tb.harvest_i):
                    continue
                shared += 1
                worst = max(worst, abs(float(ta.net_r_harvest_half) / qa
                                       - float(tb.net_r_harvest_half) / qb))
            rows.append({
                "cell": f"{a}  vs  {b}", "n_harvested": shared,
                "n_sum_checked": shared,
                "worst_halves_sum_abs_err": (r6(worst) if shared else None),
                "halves_sum_tolerance": 1e-9,
                "halves_sum_passes": bool(shared and worst <= 1e-9),
                "leg": f"SPLIT linearity  n1/q equal across cells (q={qa} vs "
                       f"{qb}) — the leg the sum identity provably cannot do"})
    if n_lin == 0:
        raise SystemExit(
            "HALT: every cell handed to hfrac_enactment declares the SAME q, so "
            "the split-linearity leg has nothing to compare and the table would "
            "report all-pass having tested only the sum identity.")
    return pd.DataFrame(rows)


_CELL_Q: dict[str, float] = {}


def shadow_table(lo_ms: int, hi_ms: int, base: list) -> pd.DataFrame:
    """THE SHADOW FLEET — every declared cell, ridden whole, D15 on every row.

    THE TABLE IS A SELECTION SURFACE AND SAYS SO IN A COLUMN.  Nothing here is
    promoted; the whole grid is printed including the cells that are the card and
    the cells that lose.

    THE POPULATION CAVEAT, CARRIED RATHER THAN HIDDEN: S-OFFSET moves `r_dist`,
    which moves the stop, which moves the exit bar, which moves `open_until`
    occupancy — so its cells are NOT perfectly paired with the base book.
    S-MINADV and S-BUF have the same property through the trail.  S-HFRAC is the
    only one of the three that changes ACCOUNTING ONLY and is therefore fully
    paired.  `n_paired` / `unpaired_cell_n` / `unpaired_base_n` are on every row.

    THE D12 CEILING DOES NOT SCALE WITH THE HARVEST FRACTION and that movement is
    a RESULT, not an artefact: `funding_ceiling_r` is an absolute 1R, so at
    q = 0.33 the runner carries 0.67 of a unit for the whole hold and accrues MORE
    funding than at q = 0.5.  `funding_ceiling_bound_n` is on every row and the
    cap's absoluteness is stated on the face.

    WHAT WOULD MAKE THIS WRONG: a built grid whose size differs from the declared
    literal (HALTed); a cell whose knobs leaked into the next (asserted by
    identity in `_knobs`); D15 columns used as gates; or the identity cells
    asserted rather than checked — both are checked trade for trade here.
    """
    cards = fleet_cards6()
    built: dict[str, int] = {}
    for c in cards:
        built[c.grid] = built.get(c.grid, 0) + 1
        if not isinstance(c, RC.Card):
            raise SystemExit(f"HALT: {c.name!r} is not an RC.Card.")
    for g in GRIDS_BUILT_HERE:
        if built.get(g, 0) != GRID_SIZES6[g]:
            raise SystemExit(
                f"HALT: grid {g!r} declares {GRID_SIZES6[g]} cells and "
                f"{built.get(g, 0)} were built.")
    if set(built) - set(GRIDS_BUILT_HERE):
        raise SystemExit(f"HALT: undeclared grids built: "
                         f"{sorted(set(built) - set(GRIDS_BUILT_HERE))}")

    card_book = T6.run_cell(RC.CARD_V6, lo_ms, hi_ms)
    rows = []
    hf_cells: dict[str, list] = {}
    _CELL_Q.clear()
    for c in cards:
        bk = run_shadow_cell(c, lo_ms, hi_ms)
        row = dict(T6.agg(bk, c.name, c.grid))
        row.update(T6.d15(bk, base))
        ex = {}
        for t in bk:
            ex[t.exit_reason] = ex.get(t.exit_reason, 0) + 1
        row.update({
            "cell": c.name, "grid": c.grid,
            "diff_from_card": c.diff_from_card(),
            "declared_identical_to_card": (c.diff_from_card()
                                           == "(the ratified v6 card)"),
            "reproduces_card_book": _same_book(bk, card_book),
            "selection_surface": SELECTION_SURFACE_NOTE,
            "grid_declared_size": GRID_SIZES6[c.grid],
            "entry_buf_atr": c.entry_buf_atr,
            "trail_buf_atr": c.trail_buf_atr,
            "trail_min_advance_atr": c.trail_min_advance_atr,
            "trail_extra_buf_atr": c.trail_extra_buf_atr,
            "trail_arm_after_r": c.trail_arm_after_r,
            "harvest_frac": c.harvest_frac,
            "wall_aware_stop": c.wall_aware_stop,
            "harvested_n": sum(1 for t in bk if t.harvested),
            "funding_ceiling_bound_n": sum(1 for t in bk
                                           if t.funding_ceiling_bound),
            "funding_ceiling_is_absolute_1R": True,
            "exits_stop": ex.get("stop", 0),
            "exits_bell": ex.get("bell_12_89", 0) + ex.get("bell_89_316", 0),
            "exits_time_stop": ex.get("time_stop", 0),
            "exits_corridor_end": ex.get("corridor_end", 0),
            "exits_wall": ex.get("wall", 0),
            "window": "full_corridor",
            "d15_gates_nothing": True,
        })
        rows.append(row)
        if c.grid in ("S-HFRAC", "card"):
            hf_cells[c.name] = bk
            _CELL_Q[c.name] = float(c.harvest_frac)
    df = pd.DataFrame(rows)
    # TWO INDEPENDENT READINGS OF "IS THIS THE CARD", RECONCILED BY CARDINALITY
    # OVER EVERY ROW.  `declared_identical_to_card` is a FIELD COMPARISON on the
    # Card; `reproduces_card_book` is a TRADE-FOR-TRADE comparison of two ridden
    # books, the right-hand one of which rides no harness.  A cell that declares
    # itself the card and does NOT reproduce it is either a knob that leaked
    # through `_knobs` or a field missing from `diff_from_card`'s tuple — which
    # is the exact failure that docstring names, and it was going unchecked.
    #
    # THE IMPLICATION IS ONE-WAY AND ONLY THE SOUND DIRECTION IS ASSERTED. The
    # converse is FALSE by construction: `S-CLOCK no funding ceiling` differs on
    # a knob and still reproduces the card book, because the ceiling never binds
    # in this corridor. Asserting it both ways would HALT on a true result.
    bad = df[df["declared_identical_to_card"] & ~df["reproduces_card_book"]]
    if len(bad):
        raise SystemExit(
            "HALT: cells declare themselves the ratified v6 card but do not "
            f"reproduce its book trade for trade: {list(bad['cell'])} — either "
            "a knob leaked or diff_from_card() is missing a field.")
    if not bool(df["declared_identical_to_card"].any()):
        raise SystemExit(
            "HALT: no cell declares itself the card, so the identity leg above "
            "passed vacuously — the fleet must contain the card row.")
    front = ["cell", "grid", "diff_from_card", "selection_surface", "n", "net_r",
             "expectancy_r", "win_rate_pct", "provisional"]
    cols = front + [c for c in df.columns if c not in front]
    df = df[cols]
    df.attrs["hfrac_cells"] = hf_cells
    df.attrs["fleet_cells_excluding_the_card"] = FLEET_CELLS_EXCLUDING_THE_CARD
    df.attrs["cells_added_by_c6"] = CELLS_ADDED_BY_C6
    return df


def shadow_identity_checks(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """THE IDENTITY LEGS — checked trade for trade, never asserted.

    Three claims this build makes about the cross, each of which is free to check
    because the two books must be the SAME OBJECT if the claim is true:
      1. `S-OFFSET 0.50 x S-MINADV 0.05` IS the ratified v6 card;
      2. `S-OFFSET 0.50 x S-MINADV 0.00` is the v5-TRAIL control (the v6 card
         with F-C4-d's minimum advance switched off) — a claim the spec got
         wrong, having been drafted against the v5 baseline;
      3. `restop` at the card's own buffer reproduces the parent's Stop on every
         eligible anchor in the corridor.

    WHAT WOULD MAKE THIS WRONG: comparing only the headline `net_r` (two
    different books can sum to the same total); or comparing books that were both
    produced by the harness, which would compare a copy to itself — leg 1's
    right-hand side is `T6.run_cell(RC.CARD_V6, ...)` with NO harness at all.
    """
    card_book = T6.run_cell(RC.CARD_V6, lo_ms, hi_ms)
    ctrl_card = RC.Card(name="v6 minus the minimum advance",
                        trail_min_advance_atr=0.0)
    ctrl_book = T6.run_cell(ctrl_card, lo_ms, hi_ms)
    cross = {c.name: c for c in fleet_cards6() if c.grid == "S-OFFSETxMINADV"}
    a = run_shadow_cell(cross["S-OFFSET 0.50 x S-MINADV 0.05"], lo_ms, hi_ms)
    b = run_shadow_cell(cross["S-OFFSET 0.50 x S-MINADV 0.00"], lo_ms, hi_ms)
    ri = restop_identity(lo_ms, hi_ms)
    rows = [
        {"leg": "F-C6-CROSS-a", "claim": "S-OFFSET 0.50 x S-MINADV 0.05 IS the "
                                         "ratified v6 card",
         "n_left": len(a), "n_right": len(card_book),
         "identical": _same_book(a, card_book),
         "compared_by": "trade-for-trade on (asset, entry, exit, stop, R, net, "
                        "exit_reason); the right-hand book rides NO harness"},
        {"leg": "F-C6-CROSS-b", "claim": "S-OFFSET 0.50 x S-MINADV 0.00 is the "
                                         "v5-TRAIL control, NOT the card — the "
                                         "commission says otherwise and the "
                                         "commission was drafted against v5",
         "n_left": len(b), "n_right": len(ctrl_book),
         "identical": _same_book(b, ctrl_book),
         "compared_by": "trade-for-trade against T6.run_cell(v6 card with "
                        "trail_min_advance_atr=0.0)"},
        {"leg": "F-C6-CROSS-c", "claim": "and it is NOT the card book",
         "n_left": len(b), "n_right": len(card_book),
         "identical": not _same_book(b, card_book),
         "compared_by": "the same comparison, negated — a control that "
                        "reproduces the card is not a control"},
        {"leg": "F-C6-RESTOP", "claim": "restop at the card's own buffer "
                                        "reproduces the parent Stop exactly",
         "n_left": ri["anchors_identical"], "n_right": ri["anchors_compared"],
         "identical": ri["anchors_identical"] == ri["anchors_compared"],
         "compared_by": "all seven arithmetic fields + anchor_bar + n_eligible, "
                        "over every eligible anchor in the floored corridor, "
                        "both directions"},
    ]
    return pd.DataFrame(rows)


def wall_aware_population(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """How big is the wall-aware cell's population — so it is not born provisional.

    TWO COUNTS, AND THEY ARE DIFFERENT OBJECTS:
      · `entry_stop_inside_a_single_band` — the ENTRY stop of a card campaign
        landing inside ONE MH-or-heavier band, per family.  This is the spec's
        47/195 figure and it describes the CONDITION the cell responds to.
      · `campaigns_with_a_replaced_advance` — campaigns on which the cell
        actually MOVED a trail candidate.  This is what the cell DOES, and it is
        the number that decides whether the cell is scoreable.
    Publishing only the first would describe a condition and call it an effect.

    THE ENVELOPE READING IS PRINTED BESIDE THE PER-BAND ONE, because it is the
    reading `add_context` would have given and it is INFLATED by the inter-band
    gaps — which is the whole reason `band_context` keeps the four bands apart.

    WHAT WOULD MAKE THIS WRONG: counting the envelope as if it were the
    predicate; or counting bars instead of campaigns and calling the result a
    population of campaigns.
    """
    base = T6.run_cell(RC.CARD_V6, lo_ms, hi_ms)
    per_family = {nm: 0 for nm in MH_OR_HEAVIER}
    n_any = n_single = n_env = 0
    for t in base:
        bands = band_context(t.symbol)
        i = t.entry_i
        hit = [nm for nm in MH_OR_HEAVIER
               if np.isfinite(bands[nm][0][i]) and
               bands[nm][0][i] <= t.stop_px <= bands[nm][1][i]]
        for nm in hit:
            per_family[nm] += 1
        if len(hit) >= 1:
            n_any += 1
        if len(hit) == 1:
            n_single += 1
        elo = min(float(bands[nm][0][i]) for nm in MH_OR_HEAVIER)
        ehi = max(float(bands[nm][1][i]) for nm in MH_OR_HEAVIER)
        if elo <= t.stop_px <= ehi:
            n_env += 1

    # THE CELL AND ITS CONTROL ARE SELECTED BY CARDINALITY, NOT BY `next(iter)`.
    # Both dicts must hold EXACTLY ONE card: a second wall-aware cell, or a
    # second S-BUF 0.25, would have been picked arbitrarily by dict order and
    # the comparison below would silently be against the wrong control.
    cell = {c.name: c for c in fleet_cards6() if c.wall_aware_stop}
    if len(cell) != 1:
        raise SystemExit(f"HALT: expected exactly one wall-aware cell in the "
                         f"fleet, found {len(cell)}: {sorted(cell)}")
    name = next(iter(cell))
    bk = run_shadow_cell(cell[name], lo_ms, hi_ms)
    plain = {c.name: c for c in fleet_cards6()
             if c.grid == "S-BUF" and not c.wall_aware_stop
             and abs(c.trail_buf_atr - 0.25) < 1e-12}
    if len(plain) != 1:
        raise SystemExit(f"HALT: expected exactly one plain S-BUF 0.25 control, "
                         f"found {len(plain)}: {sorted(plain)}")
    plain_name = next(iter(plain))
    bk_plain = run_shadow_cell(plain[plain_name], lo_ms, hi_ms)
    idx = {(t.symbol, t.entry_ms): t for t in bk_plain}
    moved = sum(1 for t in bk
                if (t.symbol, t.entry_ms) in idx
                and abs(float(t.final_stop_px)
                        - float(idx[(t.symbol, t.entry_ms)].final_stop_px)) > 1e-12)
    rows = [{"measure": "entry_stop_inside_AT_LEAST_ONE_MH_or_heavier_band",
             "n": n_any, "of": len(base), "provisional": _provisional(n_any),
             "note": "THE PREDICATE — it is a DISJUNCTION over the four bands, "
                     "so 'at least one' is the count that matches it"},
            {"measure": "entry_stop_inside_EXACTLY_ONE_band",
             "n": n_single, "of": len(base),
             "provisional": _provisional(n_single),
             "note": "the stricter reading; the difference from the row above "
                     "is the campaigns whose stop sits in overlapping bands"},
            {"measure": "entry_stop_inside_the_ENVELOPE_of_the_four",
             "n": n_env, "of": len(base), "provisional": _provisional(n_env),
             "note": "the reading add_context would give — INFLATED by the "
                     "inter-band gaps, printed to show why it is not used"},
            {"measure": "campaigns_whose_final_stop_the_cell_moved",
             "n": moved, "of": len(bk), "provisional": _provisional(moved),
             "note": f"what the cell DOES, against `{plain_name}`"}]
    rows += [{"measure": f"entry_stop_inside_band_{nm}", "n": per_family[nm],
              "of": len(base), "provisional": _provisional(per_family[nm]),
              "note": "per family; a stop may sit in more than one"}
             for nm in MH_OR_HEAVIER]
    return pd.DataFrame(rows)


def knob_ruling_rows() -> pd.DataFrame:
    """The knob-assignment ruling, as a table, so the build document quotes the
    code rather than a transcription of it.

    WHAT WOULD MAKE THIS WRONG: a ruling recorded here that no code consults —
    the F-C3-e defect in miniature.  Every `bound_to` below names a site that
    `_knobs` actually binds or a `Card` field the parent actually reads.
    """
    return pd.DataFrame([{"grid": k, **v} for k, v in sorted(KNOB_RULING.items())])


# ═══════════════════════════════════════════════════════════════ THE SELF-TEST
def main() -> int:                                          # pragma: no cover
    """Run every table against live data and print what it measured."""
    lo, hi, meta = T6.corridor()
    print(f"corridor  {meta['panel_start']} -> {meta['last_closed_4h_open']}  "
          f"{meta['span_days']} d")

    print("\n── knob ruling ──")
    kr = knob_ruling_rows()
    print(kr[["grid", "bound_to", "card_is_a_cell"]].to_string(index=False))

    print("\n── L-FMH ──")
    fm = fmh_tables(lo, hi)
    ag = fm[fm["row_kind"] == "arm_aggregate"]
    print(ag[["book", "arm", "n_campaigns", "n_fired", "n_fired_winners",
              "n_winner_saved", "n_winner_killed", "n_loser_unchanged",
              "delta_r", "paired_delta_expectancy_r"]].to_string(index=False))
    print(f"fmh rows={len(fm)} cols={len(fm.columns)}")

    print("\n── L-WALLQ ──")
    ch = wall_champs(hi)
    print("champions:", {k: v for k, v in ch.items() if k[1] == "12h"})
    wq = wallq_lab(T6.run_cell(RC.CARD_V6, lo, hi), ch)
    print(wq[wq["row_kind"] == "bucket_aggregate"][
        ["alignment", "direction", "n", "n_winners", "win_rate_pct",
         "expectancy_r", "provisional"]].to_string(index=False))
    print(f"wallq rows={len(wq)} cols={len(wq.columns)}")

    print("\n── L-SPR-NT ──")
    sp = sprnt_lab(lo, hi)
    print(sp[sp["row_kind"] == "population"][
        ["population", "direction", "n", "n_episodes", "h20_mean_net_r",
         "h100_mean_net_r", "h20_n_offcorridor_nan", "provisional"]
    ].to_string(index=False))
    print(sp[sp["row_kind"] != "population"][
        ["population", "n", "filed_value", "measured_value"]].to_string(index=False))
    print(f"sprnt rows={len(sp)} cols={len(sp.columns)}")

    print("\n── SHADOW FLEET ──")
    base = T6.run_cell(RC.CARD_V6, lo, hi)
    sh = shadow_table(lo, hi, base)
    print(sh[["cell", "grid", "n", "net_r", "expectancy_r", "win_rate_pct",
              "n_paired", "paired_delta_expectancy_r",
              "funding_ceiling_bound_n", "reproduces_card_book"]
             ].to_string(index=False))
    print(f"shadow rows={len(sh)} cols={len(sh.columns)}")

    print("\n── the wall-aware cell's population [H4] ──")
    print(wall_aware_population(lo, hi).to_string(index=False))

    print("\n── identity legs ──")
    idf = shadow_identity_checks(lo, hi)
    print(idf.to_string(index=False))

    print("\n── S-HFRAC enactment ──")
    print(hfrac_enactment(sh.attrs["hfrac_cells"]).to_string(index=False))
    return 0


if __name__ == "__main__":                                  # pragma: no cover
    raise SystemExit(main())
