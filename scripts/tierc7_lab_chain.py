"""TIER-C7 · L-RE — THE CHAIN LEDGER.  DID THE ROUND TRIP BEAT THE HOLD?

CLASS: measurement.  Nothing here is scored, nothing here gates.  D15 columns
ride every aggregate row and GATE NOTHING; every grid is reported WHOLE; every
public function's docstring says WHAT WOULD MAKE IT WRONG.

This module builds ON `tierc7` — it does not fork it.  `tierc7.py` must never
import this file, and does not: the dependency runs one way only.

════════════════════════════════════════════════════════════════════════════
THE QUESTION, AND THE ONE THING THAT MAKES IT ANSWERABLE
════════════════════════════════════════════════════════════════════════════
D-R5 lets a campaign exit and come back.  D-R6 rules the pair ONE campaign.
The question this ledger exists to answer is the one the arm's headline cannot:
for the campaigns that actually did the round trip, would simply HOLDING have
done better?

THE COUNTERFACTUAL IS NOT RE-RIDDEN.  IT IS ALREADY IN THE BOOK.
`RC.CARD_V6_CONTROL` differs from `RC.CARD_WEAVE_RE` in exactly two fields —
`weave` and `reentry` — and in NOTHING that touches candidate selection, the
entry price, the initial stop or R.  So the v6 control campaign that shares a
chain's (asset, lane, entry bar) IS that chain's single ride: same tape, same
entry, same stop, same R, held to whatever the v6 ride ended on.  Re-riding it
here would be a SECOND implementation of a ride that already exists, and the
estate's own rule forbids re-deriving a value the way the program derived it
and then comparing it to itself.  `self_check` asserts the identity that makes
the substitution legitimate — entry price, stop price and R equal on all 79
pairs — rather than assuming it.

CONSEQUENCE: for the 67 chains whose leg 1 ended on a LADDER-OUT, the weave
never fired, so leg 1 and the single ride are the SAME RIDE — same bars, same
exit bar, same exit price, same exit reason — and their net R agrees to the
last bit on all 67.

AND THAT AGREEMENT IS NOT WHAT EARNS THE SUBSTITUTION.  An earlier draft of
this docstring said it was, and called the two rides "two independent code
paths".  They are not independent: both are `T7._ride_leg` with one `if`
differing on `card.weave`, and both are booked by `T7._account_chain`, which
`T7.replay` also calls.  On a ladder-out chain the weave provably never fired —
had it fired, leg 1's exit reason would be "weave" — so the agreement is a
CONSTRUCTION and cannot fail.  It is kept as a regression guard against state
leaking through the `_WEAVE`/`frame` caches, and `self_check` labels it as one.

WHAT ACTUALLY EARNS THE SUBSTITUTION is `self_check`'s FIRST row: two books,
run over the same tape from two different cards, agree on entry price, stop
price and R on all 79 pairs.  That is an agreement between two rides rather
than a restatement of one, and it is a cardinality assertion, not an example.

════════════════════════════════════════════════════════════════════════════
HOW A LEG'S R CONTRIBUTION IS OBTAINED — BY CALLING THE PROGRAM, NOT COPYING IT
════════════════════════════════════════════════════════════════════════════
`T7._account_chain` sums gross, fees and funding over a chain's legs and takes
the D12 ceiling ONCE on the total.  It exposes no per-leg net.  Rather than
re-implement its arithmetic — which would be the forbidden self-comparison —
this module calls it twice on the SAME campaign:

    leg1_r = _account_chain(sym, card, d, R, {"legs": [leg1]})["net_r"]
    leg2_r = t.net_r - leg1_r

Leg 1 is index 0 in both calls, so it is sized 1.0 in both, and gross/fee/
funding are per-leg sums — the subtraction is therefore EXACT, with one named
exception: when the chain's D12 funding ceiling BINDS, the ceiling's credit is
taken on the chain total and lands entirely in the residual.  That happens on
ONE of the 79 chains (ETHUSDT 2020-11-04) and the row carries a flag saying so.

THE REJECTED READING IS OBTAINED THE SAME WAY — BY CALLING THE PROGRAM.
`_account_chain` computes leg k>0's size as `R / leg["own_r"]`.  Handing it a
leg 2 whose `own_r` has been SET TO THE CHAIN'S R therefore yields size exactly
1.0 — the one-unit-per-leg book — computed by the shipped accounting function
with no fork, no copy and no second implementation.

════════════════════════════════════════════════════════════════════════════
THE SIZING IS THE RULE.  THE UNSIZED NUMBER IS PRINTED, AND IT IS NOT A RESULT.
════════════════════════════════════════════════════════════════════════════
A chain has ONE R, set at its first entry.  Leg 2 gets a FRESH structural stop
at a DIFFERENT distance, so one unit on both legs holds the QUANTITY constant
and lets the RISK float.  Leg 2 is therefore sized `chain_R / own_R`.

Every chain's one-unit number is printed as `unsized_chain_net_r`, LABELLED THE
REJECTED READING on the face of the frame, so a reader can see the size of the
accounting choice instead of taking it on trust.  Measured on the full arm:

    max_single_trade_delta_share    0.5462 sized  ·  0.7473 one-unit
    arm net R                      +59.6155 sized ·  +68.1650 one-unit

The one-unit reading is 8.55 R richer and rests 75% of the chain arm's delta on
a single campaign — SOLUSDT 2023-10-16, which re-entered at 3.48x the chain's
risk.  It is printed BECAUSE it is richer.  It is not offered as an alternative
result and no row of this module treats it as one.

════════════════════════════════════════════════════════════════════════════
THE HONEST DENOMINATOR
════════════════════════════════════════════════════════════════════════════
The round trip LOST on 51 of 79 chains.  It won +45.3481 R anyway, because the
28 wins are much larger than the 51 losses — the median chain is a small loser
and the mean chain is a large winner.  Both numbers are on every aggregate row
and neither is allowed to appear without the other.

NOTHING IN THIS FILE IS A SELECTION SURFACE.  No cell is picked, no best group
is promoted, and every frame carries `selection_surface = False` to say so on
its face.
"""
from __future__ import annotations

import copy
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc7 as T7                                                   # noqa: E402
import tierc7_rules as RC                                             # noqa: E402

# ═════════════════════════════════════════════════════════════════ THE CARDS
# The chain book, and the book that IS its single-ride counterfactual.
CHAIN_CARD = RC.CARD_WEAVE_RE          # weave + one re-entry
BASE_CARD = RC.CARD_V6_CONTROL         # card v6 — the hold
PROVISIONAL_MIN_N = RC.PROVISIONAL_MIN_N

# The two fields that separate the chain card from the control.  Asserted at
# import so a future edit to either card cannot silently make the control stop
# being the counterfactual.
_FORK_FIELDS = ("weave", "reentry")
for _f in RC.Card.__dataclass_fields__:
    if _f in ("name",) or _f in _FORK_FIELDS:
        continue
    if getattr(CHAIN_CARD, _f) != getattr(BASE_CARD, _f):
        raise SystemExit(
            f"HALT: L-RE's counterfactual is not a counterfactual — the chain "
            f"card and the v6 control differ on '{_f}', which is not one of "
            f"{_FORK_FIELDS}. The base book is no longer the single ride.")

_BOOKS: dict[tuple[int, int], tuple[list, list]] = {}
_PARTS: dict[tuple[int, int], dict] = {}


def _key(t) -> tuple:
    """The pairing key, LANE INCLUDED.

    Two lanes can enter the same asset on the same bar, so (asset, bar) is not
    a key.  `T7.score_registrations7` and `T7.loao` use this same triple;
    `T7.d15` uses (asset, bar) only, which is why d15's `n_paired` can differ
    from this module's and why both are printed rather than reconciled away.
    """
    return (t.symbol, t.lane, int(t.entry_ms))


def books(lo_ms: int, hi_ms: int) -> tuple[list, list]:
    """(base, chain-arm) over the window, run once per window and cached.

    WHAT WOULD MAKE THIS WRONG: caching across a corridor that moved (the cache
    key is the window, so it cannot); returning the arm as the base or vice
    versa; or running the arm on a different window than the base, which would
    pair campaigns that never faced the same tape.
    """
    k = (int(lo_ms), int(hi_ms))
    if k not in _BOOKS:
        _BOOKS[k] = (T7.run_cell(BASE_CARD, lo_ms, hi_ms),
                     T7.run_cell(CHAIN_CARD, lo_ms, hi_ms))
    return _BOOKS[k]


# ══════════════════════════════════════════════════════ ONE CHAIN, DECOMPOSED
def _decompose(t) -> dict:
    """ONE CHAIN'S LEG SPLIT AND ITS ONE-UNIT COUNTERPART, BOTH FROM T7.

    Three calls into `T7._account_chain`, all on the SAME campaign object:

      full      the chain exactly as the book rode it — read for `leg_sizes`
                only.  Its net is `t.net_r` by construction and is NOT compared
                to `t.net_r` as though that were a check; it is the same call
                with the same arguments and would prove nothing.
      leg-1     the same first leg, alone.  Index 0 in both calls, so size 1.0
                in both, so this IS leg 1's contribution to the chain.
      one-unit  the same two legs with leg 2's `own_r` set to the chain's R,
                which is the only quantity `_account_chain` reads from it and
                which makes its size exactly R/R = 1.0.

    WHAT WOULD MAKE THIS WRONG: accounting leg 2 alone (it would be index 0 and
    would silently be sized 1.0, which is the rejected reading wearing the
    rule's name); treating `leg2_r` as exact when the chain's funding ceiling
    binds — the ceiling is taken once on the chain total and its credit lands
    wholly in the residual, which is why the flag exists; or reading `own_r` as
    anything other than leg 2's own stop distance.
    """
    legs = t.chain["legs"]
    sym, d, R = t.symbol, t.direction, float(t.r_dist)
    full = T7._account_chain(sym, CHAIN_CARD, d, R, t.chain)
    l1 = T7._account_chain(sym, CHAIN_CARD, d, R, {"legs": [legs[0]]})
    one_unit = T7._account_chain(
        sym, CHAIN_CARD, d, R,
        {"legs": [legs[0], {**legs[1], "own_r": R}]})
    leg1_r = float(l1["net_r"])
    return {"leg_sizes": full["leg_sizes"],
            "leg1_r": leg1_r,
            "leg2_r": float(t.net_r) - leg1_r,
            "unsized_net_r": float(one_unit["net_r"]),
            # THE MECHANISM, RETURNED SO IT CAN BE ASSERTED RATHER THAN TRUSTED.
            # The whole rejected-reading column rests on `own_r = R` making
            # `_account_chain` size leg 2 at exactly R/R = 1.0. That is a claim
            # about a line of code in another module, and `_account_chain` has a
            # silent `else 0.0` branch for a falsy `own_r` — so a leg 2 sized
            # ZERO would masquerade as a one-unit leg with no flag anywhere.
            # `self_check` asserts it over the whole chain population.
            "unsized_leg2_size": float(one_unit["leg_sizes"][1]),
            "ceiling_bound_chain": bool(full["funding_ceiling_bound"]),
            "ceiling_bound_leg1": bool(l1["funding_ceiling_bound"]),
            "ceiling_credit_r": float(full["funding_r_uncapped"]
                                      - full["funding_r"])}


def _parts(lo_ms: int, hi_ms: int) -> dict:
    """Everything the three public frames share, built once per window."""
    k = (int(lo_ms), int(hi_ms))
    if k in _PARTS:
        return _PARTS[k]
    base, arm = books(lo_ms, hi_ms)
    bu = {_key(t): t for t in base}
    chains = sorted([t for t in arm if getattr(t, "n_reentries", 0) == 1],
                    key=lambda t: (t.entry_ms, t.symbol))
    dec = {_key(t): _decompose(t) for t in chains}
    _PARTS[k] = {"base": base, "arm": arm, "base_by_key": bu,
                 "chains": chains, "dec": dec}
    return _PARTS[k]


def _unsized_book(lo_ms: int, hi_ms: int) -> list:
    """The chain arm with every chain re-booked AT ONE UNIT PER LEG.

    THE REJECTED READING AS A BOOK, so the D15 trio can be measured on it the
    same way it is measured on the shipped arm.  Non-chain campaigns are the
    SAME OBJECTS — they have no re-entry and the sizing rule cannot touch them.
    Chain campaigns are shallow copies with `net_r` overwritten, which keeps the
    `chain`/`n_reentries` attributes `T7.replay` attached with
    `object.__setattr__` and which a `dataclasses.replace` would have dropped.

    WHAT WOULD MAKE THIS WRONG: mutating the arm's own trades (later callers
    would read the rejected reading as the result); rebuilding non-chain
    campaigns and letting float noise separate two books that must agree
    exactly off the chains; or letting this book anywhere near a scored line.
    """
    p = _parts(lo_ms, hi_ms)
    out = []
    for t in p["arm"]:
        k = _key(t)
        if k in p["dec"]:
            c = copy.copy(t)
            object.__setattr__(c, "net_r", p["dec"][k]["unsized_net_r"])
            out.append(c)
        else:
            out.append(t)
    return out


# ═══════════════════════════════════════════════════════════ THE PER-CHAIN LEDGER
def chain_ledger(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """ONE ROW PER CHAIN — the round trip beside the hold, on the same tape.

    `single_ride_net_r` IS the v6 control campaign's net R.  It is not a replay
    and not an estimate: it is the same entry, the same stop, the same R, held.

    `delta_r = chain_net_r - single_ride_net_r`, and `did_the_round_trip_win`
    is that delta being positive.  Both are None on the (currently zero) chains
    that have no control twin — a chain holds its asset's slot longer than the
    control does, so the arm can legitimately hold a campaign the control never
    opened.  Those rows are KEPT and flagged, never dropped: dropping them would
    silently improve the denominator.

    `unsized_chain_net_r` is THE REJECTED READING — one unit per leg — and the
    frame says so in `unsized_is_the_rejected_reading`.  It is printed so the
    accounting choice is visible, and it is never the answer to the column
    beside it.

    WHAT WOULD MAKE THIS WRONG: pairing on (asset, bar) without the lane;
    reading `leg2_r` as exact on the row where the chain's funding ceiling
    binds; calling a chain a win because `chain_net_r > 0` rather than because
    it beat the hold; presenting `unsized_chain_net_r` as a result; or letting
    a chain with no control twin score as a loss by defaulting its counterfactual
    to zero.
    """
    p = _parts(lo_ms, hi_ms)
    rows = []
    for t in p["chains"]:
        k = _key(t)
        d = p["dec"][k]
        legs = t.chain["legs"]
        l1, l2 = legs[0], legs[1]
        f = T7.frame(t.symbol)["f"]
        b = p["base_by_key"].get(k)
        single = float(b.net_r) if b is not None else None
        delta = (float(t.net_r) - single) if single is not None else None
        # ── THE PROGRAM OWNS THE DEFINITION OF "LADDER-OUT". THIS DOES NOT. ──
        # `T7._ride_chain` admits a re-entry through exactly TWO doors: a weave
        # exit, or a stop exit on a stop the ladder had ADVANCED. It refuses a
        # plain entry-stop BY NAME, because re-entering one would re-enter every
        # loser and make D-R5 a martingale. So on THIS population — chains, and
        # only chains — "did not weave out" IS "laddered out", by the program's
        # own gate rather than by a second reading of it.
        #
        # Reading it instead as `exit_reason == "stop"` would be a one-clause
        # copy of a three-clause rule. It agrees here only because the gate ran
        # first: across the whole 189-campaign arm the two readings disagree on
        # 96 campaigns, exactly as tierc7's docstring warns ("the two readings
        # differ on most of the book"). `self_check` asserts the gate's alphabet
        # and the advanced-stop property cardinally, so a future third door
        # halts instead of being silently filed as a ladder-out.
        ladder_out = bool(l1["exit_reason"] != "weave")
        rows.append({
            "asset": t.symbol,
            "lane": t.lane,
            "direction": "long" if t.direction == 1 else "short",
            "entry_ts": T7.iso(t.entry_ms),
            "entry_ms": int(t.entry_ms),
            "chain_r_dist": T7.r6(t.r_dist),
            "n_reentries": int(t.n_reentries),
            # ── leg 1 ────────────────────────────────────────────────────
            "leg1_exit_reason": l1["exit_reason"],
            "leg1_exit_ts": T7.iso(int(f.open_ms[l1["exit_i"]])),
            "leg1_bars": int(l1["exit_i"] - l1["entry_i"]),
            "leg1_was_a_ladder_out": ladder_out,
            "leg1_size": T7.r6(d["leg_sizes"][0]),
            "leg1_r": T7.r6(d["leg1_r"]),
            # ── leg 2 ────────────────────────────────────────────────────
            "leg2_entry_ts": T7.iso(int(f.open_ms[l2["entry_i"]])),
            "leg2_entry_ms": int(f.open_ms[l2["entry_i"]]),
            "leg2_bars_after_leg1_exit": int(l2["entry_i"] - l1["exit_i"]),
            "leg2_own_r": T7.r6(l2["own_r"]),
            "leg2_own_r_over_chain_r": T7.r6(float(l2["own_r"]) / float(t.r_dist)),
            "leg2_size_chain_r_over_own_r": T7.r6(d["leg_sizes"][1]),
            "leg2_exit_reason": l2["exit_reason"],
            "leg2_exit_ts": T7.iso(int(f.open_ms[l2["exit_i"]])),
            "leg2_bars": int(l2["exit_i"] - l2["entry_i"]),
            "leg2_r": T7.r6(d["leg2_r"]),
            # ── the chain, the hold, and the difference ──────────────────
            "chain_net_r": T7.r6(t.net_r),
            "single_ride_net_r": T7.r6(single),
            "single_ride_exit_reason": (b.exit_reason if b is not None else None),
            "single_ride_exit_ts": (T7.iso(b.exit_ms) if b is not None else None),
            "single_ride_bars_held": (int(b.bars_held) if b is not None else None),
            "delta_r": T7.r6(delta),
            "did_the_round_trip_win": (None if delta is None else bool(delta > 0)),
            "paired_to_the_control": bool(b is not None),
            # ── the rejected reading, printed and labelled ───────────────
            "unsized_chain_net_r": T7.r6(d["unsized_net_r"]),
            "unsized_delta_r": (None if single is None
                                else T7.r6(d["unsized_net_r"] - single)),
            "sizing_gap_r": T7.r6(float(t.net_r) - d["unsized_net_r"]),
            "unsized_is_the_rejected_reading": True,
            # ── the arithmetic's own disclosures ─────────────────────────
            "chain_funding_ceiling_bound": d["ceiling_bound_chain"],
            "chain_funding_ceiling_credit_r": T7.r6(d["ceiling_credit_r"]),
            "leg2_r_is_leg2_alone": not d["ceiling_bound_chain"],
            "single_ride_equals_leg1_exactly": (
                None if single is None
                else bool(abs(single - d["leg1_r"]) < 1e-9)),
            "selection_surface": False,
        })
    df = pd.DataFrame(rows)
    if len(df):
        df["reading"] = "SIZED — leg 2 risks the chain's 1R [D-R6]"
        df["counterfactual_source"] = (
            "RC.CARD_V6_CONTROL's own campaign at the same (asset, lane, entry "
            "bar) — the identical tape, entry, stop and R, held. Not re-ridden.")
    return df


# ══════════════════════════════════════════════════════════════ THE AGGREGATES
_DIMS = {
    "year": ("year", lambda t: T7.iso(t.entry_ms)[:4]),
    "asset": ("asset", lambda t: t.symbol),
    "leg1_exit": ("leg1 exit reason",
                  lambda t: ("ladder-out" if t.leg1_exit_reason == "stop"
                             else t.leg1_exit_reason)),
}


def chain_by(lo_ms: int, hi_ms: int, dim: str) -> pd.DataFrame:
    """THE CHAIN LEDGER AGGREGATED — WHOLE, with the D15 trio and a LOAO line.

    `dim` is "year", "asset" or "leg1_exit".  The grid is reported whole: every
    group that has a chain gets a row, plus an ALL row, and no row is dropped
    for being small — small rows carry `provisional` instead.

    THE D15 BASE IS THIS GROUP'S OWN TWINS, and the frame says so in
    `d15_measured_against`.  `tail_exit_ratio` compares a top-decile MEAN to a
    top-decile MEAN, so handing it the whole 196-campaign control while the cell
    is eight chains from 2023 would compare a group to a population rather than
    to its counterfactual.  D15 rides these rows and GATES NOTHING.

    THE LOAO LINE IS DEGENERATE ON THE ASSET TABLE AND THAT IS PRINTED, NOT
    HIDDEN.  A single-asset group has one cluster, so every leave-one-asset-out
    panel is either empty or the whole group and none can be bootstrapped:
    the line reads 0/5 for an arithmetic reason, not an evidential one, and
    `loao_degenerate_single_asset` says which rows those are.  Reading 0/5 there
    as a refutation would be reading the panel structure, not the result.

    BOTH DENOMINATORS RIDE EVERY ROW.  `n_round_trip_lost` sits beside
    `delta_r_total` because on this book they point opposite ways: the round
    trip loses more often than it wins and makes money anyway.

    WHAT WOULD MAKE THIS WRONG: dropping a group for being small; ranking the
    rows and promoting one (this is not a selection surface and no cell here is
    a candidate for anything); measuring D15 against a population rather than
    the group's own twins without saying so; or reporting the total without the
    loss count.
    """
    if dim not in _DIMS:
        raise SystemExit(f"HALT: chain_by dim must be one of "
                         f"{sorted(_DIMS)}, got {dim!r}")
    label, keyfn = _DIMS[dim]
    p = _parts(lo_ms, hi_ms)
    groups: dict[str, list] = {}
    for t in p["chains"]:
        groups.setdefault(str(keyfn(t)), []).append(t)

    rows = []
    for g in sorted(groups) + ["ALL"]:
        cell = p["chains"] if g == "ALL" else groups[g]
        twins = [p["base_by_key"][_key(t)] for t in cell
                 if _key(t) in p["base_by_key"]]
        deltas = [float(t.net_r) - float(p["base_by_key"][_key(t)].net_r)
                  for t in cell if _key(t) in p["base_by_key"]]
        uns = [p["dec"][_key(t)]["unsized_net_r"] - float(p["base_by_key"][_key(t)].net_r)
               for t in cell if _key(t) in p["base_by_key"]]
        won = sum(1 for x in deltas if x > 0)
        lost = sum(1 for x in deltas if x < 0)
        assets = {t.symbol for t in cell}
        lo_ = T7.loao(cell, p["base"], f"L-RE {label}={g}")
        rows.append({
            "dim": label, "group": g,
            "n_chains": len(cell),
            "n_paired_to_the_control": len(deltas),
            "n_unpaired": len(cell) - len(deltas),
            "assets_in_group": len(assets),
            "chain_net_r": T7.r4(sum(float(t.net_r) for t in cell)),
            "single_ride_net_r": T7.r4(sum(float(b.net_r) for b in twins)),
            "delta_r_total": T7.r4(sum(deltas)) if deltas else None,
            "delta_r_mean": T7.r6(float(np.mean(deltas))) if deltas else None,
            "delta_r_median": T7.r6(float(np.median(deltas))) if deltas else None,
            "n_round_trip_won": won,
            "n_round_trip_lost": lost,
            "round_trip_win_rate_pct": T7.pct(won, len(deltas)),
            "best_delta_r": T7.r4(max(deltas)) if deltas else None,
            "worst_delta_r": T7.r4(min(deltas)) if deltas else None,
            "leg1_r_total": T7.r4(sum(p["dec"][_key(t)]["leg1_r"] for t in cell)),
            "leg2_r_total": T7.r4(sum(p["dec"][_key(t)]["leg2_r"] for t in cell)),
            "n_leg1_ladder_out": sum(1 for t in cell
                                     if t.leg1_exit_reason == "stop"),
            "n_leg1_weave": sum(1 for t in cell
                                if t.leg1_exit_reason == "weave"),
            "REJECTED_unsized_delta_r_total": T7.r4(sum(uns)) if uns else None,
            "unsized_is_the_rejected_reading": True,
            # ── D15, riding the row, gating nothing ──────────────────────
            **T7.d15(cell, twins),
            "d15_measured_against": ("this group's OWN single-ride twins "
                                     "(the paired v6 control campaigns)"),
            "d15_gates_nothing": True,
            # ── the LOAO line ────────────────────────────────────────────
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            "loao_degenerate_single_asset": bool(len(assets) < 2),
            "provisional": bool(len(cell) < PROVISIONAL_MIN_N),
            "provisional_min_n": PROVISIONAL_MIN_N,
            "selection_surface": False,
            "grid_reported_whole": True,
            "scored": False,
        })
    return pd.DataFrame(rows)


def chain_headline(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """THE HONEST DENOMINATOR AS ITS OWN FRAME — four rows, whole.

    Row 1  the chain population and how often the round trip beat the hold.
    Row 2  where the chain arm's paired delta actually comes from: the chains,
           and the non-chain campaigns the weave changed without a re-entry.
    Row 3  the leg split — how much of the round trip's edge is leg 2.
    Row 4  the rejected reading, on the same three columns, LABELLED.

    THE SECOND ROW EXISTS BECAUSE THE FIRST IS NOT THE ARM.  79 chains are not
    189 campaigns, and the arm's paired delta contains campaigns whose weave
    fired and whose re-entry never qualified.  Quoting the chain total as the
    arm's total would attribute the weave-only campaigns to the round trip.

    AND THE SECOND ROW'S DENOMINATOR IS MOSTLY TIES, WHICH IS WHY `n_tied` IS ON
    THE FRAME.  108 of the arm's 189 paired campaigns have a delta of EXACTLY
    zero — the weave never fired and no re-entry qualified, so the arm rode the
    control's own campaign.  A win rate of 29/189 = 15.34% therefore counts 108
    campaigns that were never a comparison as though they were losses, and sits
    in the same column as row 1's 35.44%, whose 79 chains contain NO ties.  The
    two numbers are not comparable and a reader could not tell from the frame.
    Both denominators now ride the row: `win_rate_pct` over everything paired,
    `win_rate_of_decided_pct` over the campaigns that actually differ (29/81 =
    35.80%, which is row 1's number, and that is the finding — the arm's
    non-tied win rate IS the chain win rate).

    WHAT WOULD MAKE THIS WRONG: quoting the win count without the loss count or
    the total without either; quoting a win rate over a denominator padded with
    ties, or dropping the ties instead of counting them; folding the non-chain
    remainder into the chain line; or reading row 4 as a result.
    """
    p = _parts(lo_ms, hi_ms)
    bu = p["base_by_key"]
    deltas = [float(t.net_r) - float(bu[_key(t)].net_r)
              for t in p["chains"] if _key(t) in bu]
    arm_pairs = [float(t.net_r) - float(bu[_key(t)].net_r)
                 for t in p["arm"] if _key(t) in bu]
    non_chain = [float(t.net_r) - float(bu[_key(t)].net_r)
                 for t in p["arm"]
                 if _key(t) in bu and getattr(t, "n_reentries", 0) == 0]
    uns = [p["dec"][_key(t)]["unsized_net_r"] - float(bu[_key(t)].net_r)
           for t in p["chains"] if _key(t) in bu]
    l1 = [p["dec"][_key(t)]["leg1_r"] for t in p["chains"]]
    l2 = [p["dec"][_key(t)]["leg2_r"] for t in p["chains"]]
    tot = [a + b for a, b in zip(l1, l2)]

    def _tally(xs: list) -> dict:
        """WON, LOST, TIED AND BOTH WIN RATES — never one without the others.

        A tie is a campaign the arm rode identically to the control.  It is not
        a loss and it is not a win, and a win rate that puts it in the
        denominator measures how OFTEN the rule fired, not how often it was
        right.  Both denominators are printed because on this book they differ
        by a factor of two on one row and not at all on another.
        """
        w = sum(1 for x in xs if x > 0)
        ls = sum(1 for x in xs if x < 0)
        return {"n_won": w, "n_lost": ls, "n_tied": len(xs) - w - ls,
                "win_rate_pct": T7.pct(w, len(xs)),
                "win_rate_of_decided_pct": T7.pct(w, w + ls)}

    rows = [
        {"line": f"THE ROUND TRIP vs THE HOLD ({len(p['chains'])} chains)",
         "n": len(deltas),
         "value_r": T7.r4(sum(deltas)),
         "mean_r": T7.r6(float(np.mean(deltas))) if deltas else None,
         "median_r": T7.r6(float(np.median(deltas))) if deltas else None,
         **_tally(deltas),
         "is_the_rejected_reading": False,
         "note": "the round trip LOSES more often than it wins and makes money "
                 "anyway — the wins are much larger than the losses. Neither "
                 "number is readable without the other."},
        {"line": "the chain arm's WHOLE paired delta, for context",
         "n": len(arm_pairs),
         "value_r": T7.r4(sum(arm_pairs)),
         "mean_r": T7.r6(float(np.mean(arm_pairs))) if arm_pairs else None,
         "median_r": T7.r6(float(np.median(arm_pairs))) if arm_pairs else None,
         **_tally(arm_pairs),
         "is_the_rejected_reading": False,
         "note": f"of which {T7.r4(sum(non_chain))} R comes from "
                 f"{len(non_chain)} NON-CHAIN campaigns — the weave fired and "
                 f"no re-entry qualified. Not the round trip's. MOST OF THIS "
                 f"ROW IS TIES: read win_rate_of_decided_pct, not "
                 f"win_rate_pct, if you mean to compare it to row 1."},
        {"line": f"the leg split across the {len(l1)} chains",
         "n": len(l1),
         "value_r": T7.r4(sum(l1) + sum(l2)),
         "mean_r": T7.r6(float(np.mean(tot))) if tot else None,
         "median_r": None,
         "n_won": None, "n_lost": None, "n_tied": None,
         "win_rate_pct": None, "win_rate_of_decided_pct": None,
         "is_the_rejected_reading": False,
         "note": f"leg 1 booked {T7.r4(sum(l1))} R and leg 2 booked "
                 f"{T7.r4(sum(l2))} R. Leg 2 is the re-entry, sized to risk "
                 f"the chain's 1R."},
        {"line": "THE REJECTED READING — one unit per leg (NOT A RESULT)",
         "n": len(uns),
         "value_r": T7.r4(sum(uns)),
         "mean_r": T7.r6(float(np.mean(uns))) if uns else None,
         "median_r": T7.r6(float(np.median(uns))) if uns else None,
         **_tally(uns),
         "is_the_rejected_reading": True,
         "note": "printed so the size of the accounting choice is visible. A "
                 "wide re-entry stop must not be a free multiplier — see "
                 "sizing_sensitivity for what it buys and what it costs."},
    ]
    d = pd.DataFrame(rows)
    d["selection_surface"] = False
    d["scored"] = False
    return d


# ═══════════════════════════════════════ THE SIZING CHOICE, MADE VISIBLE
def sizing_sensitivity(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """THE TWO READINGS OF ONE RULE, SIDE BY SIDE, ONE OF THEM REJECTED.

    Row 1 is the shipped rule: leg 2 sized `chain_R / own_R`, so a stopped-out
    re-entry loses exactly 1.0 chain-R whatever its stop distance.
    Row 2 is ONE UNIT PER LEG — the reading the build did NOT take.
    Row 3 is the difference, and it is the size of the accounting choice.

    Both rows are measured on the WHOLE ARM through the SAME rulers the
    registration uses — `T7.d15` and `T7.loao` — because the point is not that
    the two totals differ but that the rejected reading's total is CARRIED BY
    ONE CAMPAIGN.  `max_single_trade_delta_share` is 0.7473 unsized against
    0.5462 sized: the largest single campaign's delta is three quarters of the
    whole arm's delta under the reading that was not taken.

    ROW 2 IS NOT AN ALTERNATIVE RESULT AND NOTHING MAY QUOTE IT AS ONE.  It is
    richer by 8.55 R and that is exactly why it is printed — a reader who is
    told only the sized number cannot check whether the sizing rule was chosen
    for being right or for being convenient.  It was chosen before this ledger
    existed, it makes the arm SMALLER, and `is_the_rejected_reading` says so on
    every column of its row.

    WHAT WOULD MAKE THIS WRONG: dropping row 2 (the choice would become
    invisible); presenting row 2 without its label; measuring the two rows
    through different rulers or on different campaign sets; or computing the
    one-unit book by a second implementation of the accounting rather than by
    handing `T7._account_chain` a leg whose own_r IS the chain's R.
    """
    p = _parts(lo_ms, hi_ms)
    base, bu = p["base"], p["base_by_key"]
    sized_book = p["arm"]
    uns_book = _unsized_book(lo_ms, hi_ms)

    def _line(name: str, book: list, rejected: bool) -> dict:
        pv = [float(t.net_r) - float(bu[_key(t)].net_r) for t in book
              if _key(t) in bu]
        ch = [t for t in book if getattr(t, "n_reentries", 0) == 1]
        cd = [(t, float(t.net_r) - float(bu[_key(t)].net_r)) for t in ch
              if _key(t) in bu]
        top = max(cd, key=lambda x: abs(x[1])) if cd else (None, None)
        lo_ = T7.loao(book, base, name)
        risk_mult = [float(t.chain["legs"][1]["own_r"]) / float(t.r_dist)
                     for t in ch]
        return {
            "reading": name,
            "is_the_rule": not rejected,
            "is_the_rejected_reading": rejected,
            "leg2_size_rule": ("chain_R / leg2_own_R  [D-R6]" if not rejected
                               else "1.0 per leg  [NOT TAKEN]"),
            "arm_n": len(book),
            "arm_net_r": T7.r4(sum(float(t.net_r) for t in book)),
            # GUARDED: an empty book is a legitimate window, and np.mean([])
            # is a RuntimeWarning and a NaN, not an expectancy.
            "arm_expectancy_r": (T7.r6(float(np.mean([t.net_r for t in book])))
                                 if book else None),
            "paired_n": len(pv),
            "paired_delta_r_total": T7.r4(sum(pv)),
            "n_chains": len(ch),
            "chain_net_r_total": T7.r4(sum(float(t.net_r) for t in ch)),
            "chain_delta_r_total": T7.r4(sum(x for _, x in cd)),
            "largest_single_chain": (f"{top[0].symbol} {T7.iso(top[0].entry_ms)}"
                                     if top[0] is not None else None),
            "largest_single_chain_net_r": (T7.r4(top[0].net_r)
                                           if top[0] is not None else None),
            "largest_single_chain_delta_r": (T7.r4(top[1])
                                             if top[1] is not None else None),
            "largest_chain_share_of_chain_delta": (
                T7.r4(abs(top[1]) / abs(sum(x for _, x in cd)))
                if cd and abs(sum(x for _, x in cd)) > 1e-12 else None),
            "max_leg2_risk_multiple": T7.r4(max(risk_mult)) if risk_mult else None,
            "n_chains_leg2_riskier_than_chain_r": sum(1 for m in risk_mult
                                                      if m > 1.0),
            **T7.d15(book, base),
            "d15_measured_against": "the v6 control book (the arm's own ruler)",
            "d15_gates_nothing": True,
            **{k: v for k, v in lo_.items() if not k.startswith("_")},
            "provisional": bool(len(book) < PROVISIONAL_MIN_N),
            "selection_surface": False,
            "scored": False,
        }

    a = _line("SIZED — leg 2 risks the chain's 1R [THE RULE, D-R6]",
              sized_book, False)
    b = _line("ONE UNIT PER LEG [THE REJECTED READING — NOT A RESULT]",
              uns_book, True)

    def _sub(x, y, nd=4):
        """THE DIFFERENCE OF TWO CELLS THAT MAY NOT EXIST.

        Every cell subtracted here is None-able: `arm_expectancy_r` is None on
        an empty book (`r6` maps NaN to None) and `max_single_trade_delta_share`
        is None whenever the paired delta sums to zero.  A window with no
        campaigns is a legitimate argument to a public function — the corridor
        is a parameter, not a constant — and `None - None` raised TypeError on
        one.  An absent difference is None, which is what every other
        inapplicable cell on this row already is.
        """
        if x is None or y is None:
            return None
        return (T7.r4 if nd == 4 else T7.r6)(float(x) - float(y))

    diff = {k: None for k in a}
    diff.update({
        "reading": "DIFFERENCE (the rule − the rejected reading)",
        "is_the_rule": None, "is_the_rejected_reading": None,
        "leg2_size_rule": "what the accounting choice is worth",
        "arm_n": a["arm_n"] - b["arm_n"],
        "arm_net_r": _sub(a["arm_net_r"], b["arm_net_r"]),
        "arm_expectancy_r": _sub(a["arm_expectancy_r"], b["arm_expectancy_r"], 6),
        "paired_delta_r_total": _sub(a["paired_delta_r_total"],
                                     b["paired_delta_r_total"]),
        "chain_delta_r_total": _sub(a["chain_delta_r_total"],
                                    b["chain_delta_r_total"]),
        "max_single_trade_delta_share": _sub(a["max_single_trade_delta_share"],
                                             b["max_single_trade_delta_share"]),
        "d15_gates_nothing": True,
        "selection_surface": False,
        "scored": False,
    })
    d = pd.DataFrame([a, b, diff])
    gap = diff["arm_net_r"]
    d["ruling"] = (
        "D-R6 + the module docstring of tierc7.py. The sizing was ruled BEFORE "
        "this ledger existed and it makes the arm SMALLER by "
        + (f"{abs(float(gap)):.4f} R" if gap is not None else "an amount this "
           "window is too empty to measure") + ". The "
        "rejected reading is printed because it is the richer one.")
    return d


# ═══════════════════════════════════════════════ THE CHECKS, AS CARDINALITIES
def self_check(lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """WHAT THIS LEDGER ASSERTS, OVER POPULATIONS AND NOT OVER EXAMPLES.

    Every row states a claim, the SIZE of the population it is checked on, and
    the number of failures.  A row whose population is 1 is marked
    `is_a_population_check = False` and is a disclosure, not a check — the
    estate's rule is that one example is not a check.

    ROW 1 IS THE ROW THAT LICENSES THE SUBSTITUTION, AND IT IS THE ONLY ONE
    THAT DOES.  Two books were run over the same tape from two different cards,
    and on all 79 pairs the entry price, the stop price and R came out equal.
    That is a genuine agreement between two rides, and it is what makes the v6
    campaign the chain's single ride rather than an approximation of one.

    ROW 2 IS NOT A SECOND, INDEPENDENT DERIVATION, AND AN EARLIER DRAFT OF THIS
    DOCSTRING SAID IT WAS.  It claimed the control book and `leg1_r` come down
    "two INDEPENDENT code paths… two programs that were never told about each
    other".  They do not.  Both rides are the SAME `T7._ride_leg`, differing
    only in the `card.weave` flag on one `if`; both books are accounted by the
    SAME `T7._account_chain`, which `T7.replay` also calls.  And on a LADDER-OUT
    chain the weave provably never fired — had it fired, leg 1's exit reason
    would be "weave" and the chain would not be in that population at all — so
    the two rides are bar-for-bar identical BY CONSTRUCTION and their nets
    CANNOT differ.  Measured: all 67 agree on exit bar, exit price and exit
    reason, not merely on net R.

    So row 2 is a REGRESSION GUARD, not evidence.  What it can still catch is
    real and is why it is kept: state leaking between the two runs through the
    `_WEAVE` / `frame` caches, or a future card-conditional branch added to
    `_ride_leg` that perturbs a leg the weave never touched.  What it must NOT
    be read as is an independent confirmation of the counterfactual.  Calling a
    construction a check is how a table comes to show seven passes and hold
    fewer than seven facts.

    ROWS 3 AND 4 ARE THE SAME FACT AS ROW 2, RESTATED.  Row 3 reduces
    algebraically to row 2 (delta − leg2_r ≡ leg1_r − twin_net) and adds no
    information; row 4 is row 2 plus its converse over the weave chains, and
    that converse IS new.  Both say so in their notes.  Of the seven passing
    rows, four are independent claims.

    WHAT WOULD MAKE THIS WRONG: a row whose `n` is 0 (it asserts nothing and
    must not read as a pass — `is_a_population_check` is False there too); a
    check that compares a value to the same computation of itself; a row that
    cannot fail being counted as a pass without saying so; or treating the
    ceiling-bound disclosure as a failure — it is a named consequence of
    taking the D12 ceiling once on the chain, exactly as D-R6 requires.
    """
    p = _parts(lo_ms, hi_ms)
    bu, dec = p["base_by_key"], p["dec"]
    ch = p["chains"]
    paired = [t for t in ch if _key(t) in bu]
    ladder = [t for t in paired if t.leg1_exit_reason == "stop"]
    weave = [t for t in paired if t.leg1_exit_reason == "weave"]
    rows = []

    def _row(claim, n, fails, extra="", independent=True, can_fail=True):
        rows.append({"claim": claim, "population_n": n, "failures": int(fails),
                     "passes": bool(fails == 0 and n > 0),
                     "is_a_population_check": bool(n > 1),
                     # WHAT THE ROW IS WORTH, ON THE FACE OF THE ROW.  A row
                     # that restates another, or that asserts something the
                     # program's own control flow already guarantees, is still
                     # worth printing and is NOT worth counting as a seventh
                     # independent fact.
                     "is_independent_of_the_rows_above": bool(independent),
                     "could_fail_on_this_population": bool(can_fail),
                     "note": extra})

    _row("every chain's entry price, stop price and R are IDENTICAL to its v6 "
         "control twin's — this is what makes the control book the single-ride "
         "counterfactual rather than an approximation of one",
         len(paired),
         sum(1 for t in paired
             if not (abs(t.entry_px - bu[_key(t)].entry_px) < 1e-12
                     and abs(t.stop_px - bu[_key(t)].stop_px) < 1e-12
                     and abs(t.r_dist - bu[_key(t)].r_dist) < 1e-12)),
         "two books, two rides, one tape")
    _row("every LADDER-OUT chain's leg-1 contribution equals its control twin's "
         "whole net R, exactly — a REGRESSION GUARD, not independent evidence: "
         "the weave provably never fired on these legs, so the same _ride_leg "
         "rode the same bars and the same _account_chain booked them",
         len(ladder),
         sum(1 for t in ladder
             if abs(float(bu[_key(t)].net_r) - dec[_key(t)]["leg1_r"]) > 1e-9),
         "SAME ride function (weave branch inert) and SAME accounting function "
         "— it cannot fail unless state leaks between the two runs, which is "
         "the only thing it is here to catch",
         independent=True, can_fail=False)
    _row("every LADDER-OUT chain's delta against the hold IS its leg-2 "
         "contribution — nothing else can have moved",
         len(ladder),
         sum(1 for t in ladder
             if abs((float(t.net_r) - float(bu[_key(t)].net_r))
                    - dec[_key(t)]["leg2_r"]) > 1e-9),
         "ALGEBRAICALLY IDENTICAL to the row above — delta − leg2_r reduces to "
         "leg1_r − twin_net. Stated because it is the reading; it ADDS NO "
         "INDEPENDENT INFORMATION and must not be counted as a second fact",
         independent=False, can_fail=False)
    _row("the WEAVE-EXIT chains are the only chains whose leg 1 differs from "
         "the hold",
         len(paired),
         sum(1 for t in paired
             if (abs(float(bu[_key(t)].net_r) - dec[_key(t)]["leg1_r"]) > 1e-9)
             != (t.leg1_exit_reason == "weave")),
         f"{len(weave)} weave-exit chains, {len(ladder)} ladder-outs")
    _row("every chain carries exactly one re-entry [D-R5's cap]",
         len(ch), sum(1 for t in ch if t.n_reentries != 1), "")
    _row("D-R5 LEFT EXACTLY TWO DOORS OPEN — every chain's leg 1 exited on "
         "'stop' or 'weave' and on nothing else. If a third exit reason ever "
         "earns a re-entry, `leg1_was_a_ladder_out` (which reads 'not a weave') "
         "would file it as a ladder-out, so this row must fail loudly first",
         len(ch),
         sum(1 for t in ch
             if t.chain["legs"][0]["exit_reason"] not in ("stop", "weave")),
         "the alphabet the gate in T7._ride_chain leaves behind")
    _row("NO CHAIN RE-ENTERED A PLAIN ENTRY-STOP — every stop-exit leg 1 was "
         "taken out of a stop the ladder had ADVANCED, checked from the leg's "
         "own record (it has advances AND its final stop moved off its entry "
         "anchor). Re-entering a plain entry-stop would re-enter every loser "
         "and make D-R5 a martingale",
         sum(1 for t in ch if t.chain["legs"][0]["exit_reason"] == "stop"),
         sum(1 for t in ch
             if t.chain["legs"][0]["exit_reason"] == "stop"
             and not (t.chain["legs"][0]["advances"]
                      and abs(t.chain["legs"][0]["final_stop"]
                              - t.chain["legs"][0]["stop0"]) > 1e-12)),
         "across the WHOLE 189-campaign arm, 'exit_reason==stop' and "
         "'laddered out' disagree on 96 campaigns — this row is what makes the "
         "ledger's one-word reading safe on the chain population")
    _row("THE REJECTED READING IS ACTUALLY ONE UNIT — handing _account_chain a "
         "leg 2 whose own_r IS the chain's R sized it at EXACTLY 1.0 on every "
         "chain. This is the mechanism the entire unsized column rests on, and "
         "_account_chain's sizing line falls back to 0.0 on a falsy own_r, "
         "which would book a ZERO-SIZE leg 2 as though it were one unit",
         len(ch),
         sum(1 for t in ch if abs(dec[_key(t)]["unsized_leg2_size"] - 1.0)
             > 1e-12),
         "the claim is about a line of code in another module, so it is "
         "asserted over the population rather than trusted or spot-checked")
    _row("every chain pairs to a control twin — an unpaired chain would have no "
         "counterfactual and is KEPT and flagged, never dropped",
         len(ch), len(ch) - len(paired), "")
    _row("leg-1-alone's funding ceiling never binds where the chain's does not "
         "— if it did, the leg split would be inexact in the other direction "
         "and the residual would be silently wrong",
         len(ch),
         sum(1 for t in ch if dec[_key(t)]["ceiling_bound_leg1"]
             and not dec[_key(t)]["ceiling_bound_chain"]), "")
    nb = sum(1 for t in ch if dec[_key(t)]["ceiling_bound_chain"])
    rows.append({
        "claim": "chains whose D12 funding ceiling BINDS — a DISCLOSURE, not a "
                 "failure. The ceiling is taken once on the chain [D-R6], so "
                 "its credit lands wholly in leg 2's residual and "
                 "leg2_r_is_leg2_alone is False on those rows",
        "population_n": len(ch), "failures": nb, "passes": None,
        "is_a_population_check": False,
        "is_independent_of_the_rows_above": True,
        "could_fail_on_this_population": True,
        "note": f"{nb} of {len(ch)} chains"})
    d = pd.DataFrame(rows)
    d["selection_surface"] = False
    d["scored"] = False
    return d


# ═════════════════════════════════════════════════════════════════ THE BUILD
def build(lo_ms: int | None = None, hi_ms: int | None = None) -> dict:
    """Every frame L-RE ships, keyed by table name.  NO WRITES — the caller
    decides where anything lands.

    WHAT WOULD MAKE THIS WRONG: writing at import or from here (this module
    must be importable with no side effects); or defaulting the window to
    anything other than the estate's own corridor.
    """
    if lo_ms is None or hi_ms is None:
        lo_ms, hi_ms, _ = T7.corridor()
    return {
        "chain_headline": chain_headline(lo_ms, hi_ms),
        "chain_ledger": chain_ledger(lo_ms, hi_ms),
        "chain_by_year": chain_by(lo_ms, hi_ms, "year"),
        "chain_by_asset": chain_by(lo_ms, hi_ms, "asset"),
        "chain_by_leg1_exit": chain_by(lo_ms, hi_ms, "leg1_exit"),
        "sizing_sensitivity": sizing_sensitivity(lo_ms, hi_ms),
        "self_check": self_check(lo_ms, hi_ms),
    }


if __name__ == "__main__":                                   # pragma: no cover
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", 40)
    _lo, _hi, _ = T7.corridor()
    for _name, _df in build(_lo, _hi).items():
        print(f"\n══ {_name}  ({len(_df)} rows x {len(_df.columns)} cols)")
        print(_df.head(12).to_string())
