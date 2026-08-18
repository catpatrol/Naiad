"""L-WEAVE pass 1 — TIER-E SIGNAL QUALITY FOR D-R3/D-R4.  DISPLAY-ONLY, GATES
NOTHING, REGISTERS NOTHING.

════════════════════════════════════════════════════════════════════════════
THIS IS A COUNTERFACTUAL ABOUT A RULE THAT DID NOT FIRE.  SAY IT FIRST.
════════════════════════════════════════════════════════════════════════════
Every number in this module is measured on the **BASE BOOK** — `run_cell` with
`RC.CARD_V6_CONTROL`, in which `card.weave is False` and the weave therefore
**never fires and never exits anything**.  What this module does is walk each
of those 196 campaigns bar by bar and ask `RC.weave_fires` on the campaign's own
direction: *had the weave been armed, would it have fired here?*  Then, because
the campaign was allowed to run, the tape already contains the answer to the
commission's question — "what would the campaign have done had it been allowed
to run" — and that answer is the campaign's ACTUAL outcome.

So: THE EVENTS ARE COUNTERFACTUAL, THE OUTCOMES ARE ACTUAL.  Every table
carries `counterfactual = True` and a `counterfactual_note` column, and the
event rows carry `is_the_arms_counterfactual` to separate the ONE event per
campaign the weave arm would really have faced from the later ones that occur
inside a campaign the weave arm had already exited (a hypothetical inside a
hypothetical, printed because it is part of the whole grid, and flagged).

THIS IS NOT THE REGISTRATION.  P-WEV-1 is scored in `tierc7.score_registrations7`
and its verdict stands: paired per-campaign delta **-0.0027 R**, asset-cluster
90% CI **[-0.0084, +0.0029]**, **NOT SUPPORTED**, **LOAO 0/5**.  Nothing here
may be read as re-scoring it, and every table prints those four numbers as
riding columns so a reader cannot lose them.

════════════════════════════════════════════════════════════════════════════
THE HEADLINE, AND IT DISSOLVES THE COMMISSION'S PREMISE
════════════════════════════════════════════════════════════════════════════
The commission asks for "the too-early cost quantified: when the weave exits a
campaign that was in profit, what would the campaign have done had it been
allowed to run?"  Measured on the full corridor (2,535 days, 196 campaigns):

    42 weave events fire inside open campaigns.  ONE of them is in profit.

    79.47% of the 3,960 open campaign bars are in profit at their close.
     2.38% of the 42 weave-event bars are  (1 of 42).

AND THE POOLED 33.4x IS TWO EFFECTS MULTIPLIED, NOT ONE — SAY WHICH IS THE
RULE'S.  The 42 events live in only 15 of the 196 campaigns, and those 15 are
the WORSE ones: 55.35% of their open bars are in profit against 82.84% of the
other 181's.  So the pooled ratio is a campaign-selection effect times the
rule's bar-selection effect, and only the second is a statement about D-R3.
HOLDING THE CAMPAIGN FIXED the ratio is **23.2x** (25.4x against those same
campaigns' non-event bars).  The finding survives — the rule really does pick
the losing bars — but it is 23x, not 33x, and `weave_quality` now prints both
denominators with `selection_decomposition_note` saying which claim each
carries.  Quoting the pooled number as the rule effect would have credited
D-R3 with choosing the campaigns as well as the bars.

The weave is not a profit-taking rule on this book — it is a **loss-side
detector**.  Its two clauses require the M-ribbon to be contracting with its
median slope AGAINST the trade AND the fast ribbon to have come back to the M
band AGAINST the trade; by the time both hold, the position is almost always
already underwater.  The mean unit move at a weave-event bar is **-0.5630 R**.
Under the harvest-inclusive mark (card v6 banks half at the band, and the band
harvest had ALREADY fired on all 42 events because `harvest_min_unit_r = -inf`),
**ZERO of 42** events sit in profit.

THE PREMISE IS THEREFORE NOT DENIED, IT IS EMPTY — n = 1 — AND THE TABLE SAYS
SO RATHER THAN QUIETLY REPORTING A MEAN OVER ONE ROW.  The in-profit cut is
printed whole with `provisional = True` and its n on the face of the row.

════════════════════════════════════════════════════════════════════════════
AND THAT IS EXACTLY WHY P-WEV-1 IS NOT SUPPORTED — THE RECONCILIATION
════════════════════════════════════════════════════════════════════════════
A reader could suspect this table of contradicting P-WEV-1: it reports a
too-early cost of **+0.5695 R gross** while the registration reports a paired
delta of only **-0.5198 R net**.  It does not contradict it; it explains it,
and the arithmetic closes to machine zero:

    too-early cost (gross R forgone)          +0.5695
    fee + funding saved by exiting earlier    -0.0496
    ─────────────────────────────────────────────────
    the weave arm's realised paired delta     -0.5198     [== the ablation's
                                                            "weave ALONE is
                                                            worth -0.5198 R"]

    spread over 196 paired campaigns          -0.002652 R per campaign
                                                        [== P-WEV-1's point]

Both sides are derived INDEPENDENTLY — the cost from the base book's price path
and harvest state, the delta from a separately-run `CARD_WEAVE_ONLY` book — and
the per-campaign residual is `1.2e-16` across all 15.  This is NOT a
re-derivation of a value the way the program derived it: the program never
computes a "cost", and this module never computes an accounting `net_r`.

TWO CARDINALITY ASSERTIONS, NOT TWO EXAMPLES, TIE THE TWO OBJECTS TOGETHER:
  * the 15 campaigns holding a FIRST weave event are EXACTLY the 15 campaigns
    whose `net_r` differs between the base book and the weave arm (`n = 15`,
    both ways, no exceptions);
  * every one of those 15 weave-arm campaigns exits with `exit_reason ==
    "weave"` on EXACTLY the bar index of its first event (15 of 15).
Both are checked on every call and reported in `weave_quality`'s
`reconciliation_*` columns; a failure sets `pwev1_consistent = False` rather
than raising, because a lab that gates nothing must not halt the estate.

════════════════════════════════════════════════════════════════════════════
FOUR READINGS THIS MODULE HAD TO SETTLE, AND THE ALTERNATIVE EACH TIME
════════════════════════════════════════════════════════════════════════════
(1) WHICH BARS ARE WEAVE-ELIGIBLE.  In `T7._ride_leg` the weave sits at step 6,
    AFTER stop / bell / time-stop / abort.  A campaign that exits on bar `x`
    for any of those reasons broke out of the loop BEFORE the weave test ran on
    `x`, so bar `x` is NOT weave-eligible; a campaign that ends on
    `corridor_end` never broke out, so its final bar IS.  Eligibility is
    therefore `entry_i+1 .. exit_i-1`, or `.. exit_i` for `corridor_end`.
    THE ALTERNATIVE — scanning through `exit_i` unconditionally — is NOT taken:
    it would manufacture events on bars the armed rule provably cannot see, and
    it would break the 15-of-15 bar-exact reconciliation above.

(2) "IN PROFIT" IS THE OPEN POSITION'S MARK AT THE EVENT BAR'S CLOSE, because
    the close is the price a weave exit would FILL at [D-R4 exits the remainder
    at that close].  `unit_move_r_at_event = (close - entry) * direction /
    r_dist`.  A SECOND, STRICTER reading is printed beside it and not instead of
    it — `campaign_mtm_r_at_event`, which adds the half already banked by the
    band harvest, because that half is realised money and a campaign holding
    +0.9 R of booked harvest against a -0.1 R open remainder is not "losing".
    Both are columns; neither is a filter.  A THIRD — "was EVER in profit" —
    rides as `peak_unit_move_r_to_event`, and it is 100% of events by
    construction (every campaign's high exceeds its entry on some bar), which
    is precisely why it is not used as the profit test.

(3) THE FORWARD MOVE IS A PRICE FACT, NOT A CAMPAIGN FACT, AND IS LABELLED AS
    ONE.  `fwd_{6,24,100}_bars_r` is `(close[j+h] - close[j]) * direction /
    r_dist`: it ignores the card's stop, the bell and the corridor.  A campaign
    stopped out 4 bars after the event still shows its 100-bar forward move,
    and three of them here run +2.2 to +2.6 R that the card could never have
    collected.  So `fwd_is_price_path_not_campaign_outcome = True` rides every
    row, `fwd_{h}_bars_outlives_campaign` flags the horizons that do, and the
    ONLY number used for cost is `too_early_cost_r`, which is bounded by the
    campaign's real exit.  THE ALTERNATIVE — quoting the 100-bar forward move as
    the "cost of exiting early" — is NOT taken, and would have inflated the
    too-early cost of this book by roughly an order of magnitude.

(4) THE COST IS HARVEST-AWARE, BECAUSE D-R4 EXITS "THE REMAINDER".  If the band
    harvest has already banked `q` at the event bar, the weave can only forgo
    the remaining `(1-q)` of the campaign's forward move; if the harvest would
    have come LATER, a weave exit cancels it entirely and the whole unit is
    re-priced.  All three cases are coded and named in `_forgone_gross_r`.
    THE ALTERNATIVE — a flat `held_unit_r - event_unit_r` on one whole unit —
    is printed as `unit_give_up_r` for readability but is NOT the cost column;
    on this book it is exactly 2x the truth for every event, because the
    harvest had fired on all 42.

════════════════════════════════════════════════════════════════════════════
HOUSE LAW OBSERVED
════════════════════════════════════════════════════════════════════════════
* D15 columns ride the aggregate rows of `weave_quality` and `too_early_cost`
  and GATE NOTHING.
* Every grid is reported WHOLE: all 8 corridor years including the two with no
  events, all 5 panel assets including the two with one, every verdict cell
  including the empty one.
* NOT A SELECTION SURFACE — `selection_surface = False` on every table, and it
  is false because nothing here is chosen FROM: `weave_k` is PINNED at 6 by the
  register and this module builds NO grid over it.
* `provisional = True` wherever n < `RC.PROVISIONAL_MIN_N` (= 30), which is
  every row of the in-profit cut and the whole first-event population (n = 15).
* No writes at import time.  `tierc7.py` must never import this module.

Drafted for the TIER-C7 commission, pass 1.  Seed inherited: `T7.SEED`.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import tierc7 as T7                                                   # noqa: E402
import tierc7_rules as RC                                             # noqa: E402

SEED = T7.SEED
FWD_HORIZONS: tuple[int, ...] = (6, 24, 100)

COUNTERFACTUAL_NOTE = (
    "COUNTERFACTUAL. Measured on the BASE BOOK (card v6, weave OFF), where the "
    "weave never fired and exited nothing. The events are what the armed rule "
    "WOULD have done; the outcomes are what the campaign ACTUALLY did. This is "
    "Tier-E measurement, it gates nothing, and it is NOT the registration — "
    "P-WEV-1 is scored in tierc7.score_registrations7 and is NOT SUPPORTED.")

PWEV1_OF_RECORD = {
    "pwev1_paired_delta_expectancy_r_of_record": -0.0027,
    "pwev1_ci_lo_of_record": -0.0084,
    "pwev1_ci_hi_of_record": 0.0029,
    "pwev1_verdict_of_record": "NOT SUPPORTED",
    "pwev1_loao_of_record": "0/5",
}

_SCAN: dict[tuple, tuple[pd.DataFrame, pd.DataFrame, dict]] = {}

# THE EVENT FRAME'S SCHEMA, DECLARED, so an event-free window returns an EMPTY
# frame WITH ITS COLUMNS rather than a 0x0 one.  A 0x0 frame is not a smaller
# answer, it is a different TYPE of answer: a caller doing
# `weave_events(...)[d["is_first_in_campaign"]]` gets a KeyError instead of an
# empty selection, so the module would fail loudest exactly on the windows where
# it has nothing to say.  The list is duplicated from the row builder and
# `_selftest` asserts the two agree EXACTLY, in order, so the duplication cannot
# drift in silence.
EVENT_COLUMNS: tuple[str, ...] = (
    "symbol", "lane", "direction", "dir_word",
    "campaign_entry_i", "campaign_entry_ms", "campaign_entry_iso",
    "campaign_r_dist", "event_i", "event_ms", "event_iso", "event_year",
    "bars_since_entry", "event_seq_in_campaign", "is_first_in_campaign",
    "is_the_arms_counterfactual", "weave_k",
    "unit_move_r_at_event", "in_profit_at_event", "campaign_mtm_r_at_event",
    "in_profit_mtm_at_event", "peak_unit_move_r_to_event",
    "ever_in_profit_before_event", "peak_reached_1r_before_event",
    "harvest_state_at_event", "open_fraction_at_event",
    "campaign_exit_i", "campaign_exit_ms", "campaign_exit_iso",
    "campaign_exit_reason", "campaign_bars_held",
    "campaign_unit_move_r_at_exit", "campaign_net_r", "campaign_mfe_r",
    "campaign_reached_1r", "campaign_harvested", "campaign_has_adds",
    "bars_from_event_to_campaign_exit", "bars_from_event_to_corridor_end",
    "unit_give_up_r", "too_early_cost_r", "verdict", "counterfactual",
    "cost_model_assumes_no_adds", "counterfactual_note",
) + tuple(c for h in FWD_HORIZONS
          for c in (f"fwd_{h}_bars_r",
                    f"fwd_{h}_bars_truncated_at_corridor_end",
                    f"fwd_{h}_bars_outlives_campaign")) + (
    "fwd_is_price_path_not_campaign_outcome",
    "arm_realized_delta_r", "arm_exit_reason", "arm_exit_i",
    "arm_exit_matches_event_bar", "fee_funding_saved_r_from_books",
    "reconciliation_residual_r",
)


# ═══════════════════════════════════════════════════════════════════ HELPERS
def _eligible_last_bar(t) -> int:
    """The LAST bar on which the armed weave could have been tested in `t`.

    `T7._ride_leg` puts the weave at step 6, after the stop, the bell, the time
    stop and the abort.  A campaign that exits on bar `x` for one of those
    reasons `break`s before the weave test runs on `x`; a `corridor_end`
    campaign never breaks, so its last bar did run every test.

    WHAT WOULD MAKE THIS WRONG: returning `t.exit_i` for a stop or bell exit —
    that manufactures events on bars the armed rule cannot see, and it would
    break the bar-exact 15-of-15 reconciliation against the weave arm.  Also
    wrong: returning `t.exit_i - 1` for `corridor_end`, which would silently
    drop a real event at the end of the tape.
    """
    return t.exit_i if t.exit_reason == "corridor_end" else t.exit_i - 1


def _forgone_gross_r(t, j: int, close_j: float, harvest_frac: float) -> float:
    """THE TOO-EARLY COST OF ONE EVENT, in GROSS R, harvest-aware.

    What the campaign's gross R would have been had the weave exited it at bar
    `j`'s close, subtracted FROM what it actually booked.  Positive means the
    weave would have given R up — "exit was early".  Negative means the
    campaign went on to give back more than the weave would have held — "exit
    was right".

    Three cases, because D-R4 exits "the REMAINDER" and the remainder depends on
    whether card v6's band harvest has already fired:

      harvest never fired      : one whole unit is re-priced from exit to close.
      harvest fired at or before j : `q` is already banked and untouchable; only
                                 `(1-q)` is re-priced.
      harvest would fire AFTER j : a weave exit cancels it, so the actual book's
                                 TWO fractions are both replaced by one whole
                                 unit marked at `close_j`.

    Fees and funding are deliberately EXCLUDED: they are not a signal-quality
    fact, they differ between the two books only because one holds fewer bars,
    and `weave_quality` reports them separately as the residual that closes the
    reconciliation to the weave arm's realised delta.

    WHAT WOULD MAKE THIS WRONG: pricing the whole unit when the harvest had
    already banked half (that doubles the cost of every event on this book);
    using the campaign's `net_r` instead of its gross unit moves (that would
    double-count the fees this function excludes by construction); or ignoring
    the third case, which would let a cancelled harvest vanish from the
    arithmetic.  It is also wrong if the card ever carries adds — this model
    prices no adds, and `weave_events` flags `cost_model_assumes_no_adds` and
    `campaign_has_adds` so a future card cannot break it in silence.
    """
    d, R, e = t.direction, t.r_dist, t.entry_px
    q = float(harvest_frac)
    unit_j = (float(close_j) - e) * d / R
    unit_x = (t.exit_px - e) * d / R
    hj = t.harvest_i
    if hj is None:
        return unit_x - unit_j
    unit_h = (t.harvest_px - e) * d / R
    held = q * unit_h + (1.0 - q) * unit_x
    if hj <= j:
        return held - (q * unit_h + (1.0 - q) * unit_j)
    return held - unit_j


def _scan(lo_ms: int, hi_ms: int, k: int) -> tuple[pd.DataFrame, pd.DataFrame,
                                                   dict]:
    """ONE PASS OVER THE BASE BOOK'S OPEN BARS.  Returns (bars, events, recon).

    Both the event table and the base rate it must be compared against come out
    of the SAME walk, so the denominator can never drift from the numerator.
    `bars` is every weave-eligible open campaign bar (3,960 of them on the full
    corridor); `events` is the subset on which `RC.weave_fires` returns True,
    enriched with the counterfactual cost and the forward moves.

    THE BASE RATE IS THE POINT OF THE `bars` FRAME.  "The weave fires on losers"
    is not a finding if campaigns are usually losing at the bar in question;
    it becomes one only against the share of open bars that are in profit.
    Measured here: 79.47% of ALL open bars, 55.35% of the open bars of the 15
    campaigns that actually carry an event, and 2.38% of the event bars.  The
    frame therefore carries `lane` and `campaign_entry_ms` so `weave_quality`
    can cut it BOTH ways: the pooled rate answers "what would a reader see
    unconditionally", the within-campaign rate answers "what does the RULE
    select", and they are 33.4x and 23.2x respectively.  Reporting only the
    first credits the rule with choosing the campaigns too.

    WHAT WOULD MAKE THIS WRONG: scanning bars the armed rule cannot reach (see
    `_eligible_last_bar`); measuring the forward move past the corridor's own
    last index rather than clipping to it (that reads bars the corridor
    excludes); computing the base rate over a different bar set from the events;
    or caching across a changed `k` or a changed corridor, which the cache key
    prevents.
    """
    key = (int(lo_ms), int(hi_ms), int(k))
    if key in _SCAN:
        return _SCAN[key]

    card = RC.CARD_V6_CONTROL
    base = T7.run_cell(card, lo_ms, hi_ms)
    arm = T7.run_cell(RC.CARD_WEAVE_ONLY, lo_ms, hi_ms)
    amap = {(t.symbol, t.lane, t.entry_ms): t for t in arm}
    q = float(card.harvest_frac)

    bar_rows: list[dict] = []
    ev_rows: list[dict] = []
    for t in base:
        st = T7.frame(t.symbol)
        f = st["f"]
        w = T7.weave_of(t.symbol)
        d, R, e = t.direction, t.r_dist, t.entry_px
        corr_lo_i, corr_hi_i = T7._idx_range(f.open_ms, lo_ms, hi_ms)
        last = _eligible_last_bar(t)
        at = amap.get((t.symbol, t.lane, t.entry_ms))
        seq = 0
        # THE RUNNING PEAK IS NOT FLOORED AT ZERO.  Seeding it at 0.0 makes the
        # column `max(0, MFE)` rather than MFE: a campaign that never traded
        # above its entry would publish a peak of exactly 0.0000, and
        # `_stats`'s `peak_unit_move_r_mean` would be a CENSORED mean biased
        # upward — the same warm-up-floor family of defect this estate has
        # repaired four times, in the shape of a floor that is silently WRONG
        # rather than silently absent. It binds on 0 of the 42 events on this
        # corridor (the smallest true MFE-to-event is +0.0148 R), so seeding at
        # -inf changes no published number today and stops the column lying on
        # the first book where a weave event precedes any favourable move.
        # `ever_in_profit_before_event` (peak > 0) and
        # `peak_reached_1r_before_event` (peak >= 1) are unaffected either way.
        peak = float("-inf")
        for j in range(t.entry_i + 1, last + 1):
            cj = float(f.c[j])
            unit = (cj - e) * d / R
            fav = float(f.h[j]) if d == 1 else float(f.l[j])
            peak = max(peak, (fav - e) * d / R)
            fires = bool(RC.weave_fires(w, j, d, k))
            year = int(T7.iso(int(f.open_ms[j]))[:4])
            bar_rows.append({"symbol": t.symbol, "lane": t.lane, "year": year,
                             "direction": d,
                             "campaign_entry_ms": t.entry_ms,
                             "unit_move_r": unit, "in_profit": bool(unit > 0.0),
                             "is_weave_event": fires})
            if not fires:
                continue
            seq += 1
            hj = t.harvest_i
            harv_state = ("never" if hj is None else
                          "banked_before_event" if hj <= j else
                          "comes_after_event")
            open_frac = 1.0 if (hj is None or hj > j) else (1.0 - q)
            mtm = (unit if (hj is None or hj > j)
                   else q * (t.harvest_px - e) * d / R + (1.0 - q) * unit)
            cost = _forgone_gross_r(t, j, cj, q)
            held_unit = (t.exit_px - e) * d / R
            row = {
                # ── identity
                "symbol": t.symbol, "lane": t.lane, "direction": d,
                "dir_word": "long" if d == 1 else "short",
                "campaign_entry_i": t.entry_i,
                "campaign_entry_ms": t.entry_ms,
                "campaign_entry_iso": T7.iso(t.entry_ms),
                "campaign_r_dist": T7.r6(R),
                "event_i": j, "event_ms": int(f.open_ms[j]),
                "event_iso": T7.iso(int(f.open_ms[j])),
                "event_year": year,
                "bars_since_entry": j - t.entry_i,
                "event_seq_in_campaign": seq,
                "is_first_in_campaign": bool(seq == 1),
                "is_the_arms_counterfactual": bool(seq == 1),
                "weave_k": int(k),
                # ── was the campaign in profit?  three readings, no filter
                "unit_move_r_at_event": T7.r6(unit),
                "in_profit_at_event": bool(unit > 0.0),
                "campaign_mtm_r_at_event": T7.r6(mtm),
                "in_profit_mtm_at_event": bool(mtm > 0.0),
                "peak_unit_move_r_to_event": T7.r6(peak),
                "ever_in_profit_before_event": bool(peak > 0.0),
                "peak_reached_1r_before_event": bool(peak >= 1.0),
                "harvest_state_at_event": harv_state,
                "open_fraction_at_event": T7.r4(open_frac),
                # ── the campaign's ACTUAL outcome — it did NOT exit here
                "campaign_exit_i": t.exit_i,
                "campaign_exit_ms": t.exit_ms,
                "campaign_exit_iso": T7.iso(t.exit_ms),
                "campaign_exit_reason": t.exit_reason,
                "campaign_bars_held": t.bars_held,
                "campaign_unit_move_r_at_exit": T7.r6(held_unit),
                "campaign_net_r": T7.r6(t.net_r),
                "campaign_mfe_r": T7.r6(t.mfe_r),
                "campaign_reached_1r": bool(t.reached_1r),
                "campaign_harvested": bool(t.harvested),
                "campaign_has_adds": bool(len(t.adds) > 0),
                "bars_from_event_to_campaign_exit": t.exit_i - j,
                "bars_from_event_to_corridor_end": corr_hi_i - j,
                # ── the counterfactual cost
                "unit_give_up_r": T7.r6(held_unit - unit),
                "too_early_cost_r": T7.r6(cost),
                "verdict": ("exit-was-early" if cost > 1e-9 else
                            "exit-was-right" if cost < -1e-9 else
                            "exit-was-neutral"),
                "counterfactual": True,
                "cost_model_assumes_no_adds": True,
                "counterfactual_note": COUNTERFACTUAL_NOTE,
            }
            for h in FWD_HORIZONS:
                kk = min(j + h, corr_hi_i)
                row[f"fwd_{h}_bars_r"] = T7.r6((float(f.c[kk]) - cj) * d / R)
                row[f"fwd_{h}_bars_truncated_at_corridor_end"] = bool(
                    j + h > corr_hi_i)
                row[f"fwd_{h}_bars_outlives_campaign"] = bool(j + h > t.exit_i)
            row["fwd_is_price_path_not_campaign_outcome"] = True
            # ── the arm's REALISED delta, read from a separately-run book
            if seq == 1 and at is not None:
                arm_delta = at.net_r - t.net_r
                ff_books = (t.fee_r + t.funding_r) - (at.fee_r + at.funding_r)
                row["arm_realized_delta_r"] = T7.r6(arm_delta)
                row["arm_exit_reason"] = at.exit_reason
                row["arm_exit_i"] = at.exit_i
                row["arm_exit_matches_event_bar"] = bool(
                    at.exit_reason == "weave" and at.exit_i == j)
                row["fee_funding_saved_r_from_books"] = T7.r6(ff_books)
                row["reconciliation_residual_r"] = T7.r6(
                    (arm_delta + cost) - ff_books)
            else:
                row["arm_realized_delta_r"] = None
                row["arm_exit_reason"] = None
                row["arm_exit_i"] = None
                row["arm_exit_matches_event_bar"] = None
                row["fee_funding_saved_r_from_books"] = None
                row["reconciliation_residual_r"] = None
            ev_rows.append(row)

    bars = pd.DataFrame(bar_rows)
    # AN EVENT-FREE WINDOW STILL RETURNS THE SCHEMA — see `EVENT_COLUMNS`.
    events = (pd.DataFrame(ev_rows) if ev_rows
              else pd.DataFrame(columns=list(EVENT_COLUMNS)))

    firsts = events[events["is_first_in_campaign"].astype(bool)]
    # THE CAMPAIGN KEY CARRIES THE LANE.  `amap` below needs all three fields
    # to be unique, which is the module's own statement that (symbol, entry_ms)
    # is NOT a campaign identity: two lanes can enter one asset on one bar. The
    # panel runs a single lane today, so dropping it was inert — but an inert
    # wrong key is still a wrong key, and it would have mis-paired the D15 cell
    # and the differing-set the moment a second lane was admitted.
    ev_keys = {(r.symbol, r.lane, r.campaign_entry_ms)
               for r in firsts.itertuples()}
    differ = {(t.symbol, t.lane, t.entry_ms) for t in base
              if (t.symbol, t.lane, t.entry_ms) in amap
              and abs(amap[(t.symbol, t.lane, t.entry_ms)].net_r
                      - t.net_r) > 1e-12}
    resid = [abs(v) for v in firsts["reconciliation_residual_r"].tolist()
             if v is not None]
    recon = {
        "base_n_campaigns": len(base),
        "arm_n_campaigns": len(arm),
        "n_campaigns_with_event": len(ev_keys),
        "n_campaigns_book_differs": len(differ),
        "event_set_equals_differing_set": bool(ev_keys == differ),
        "n_first_events_matching_arm_exit_bar": int(
            sum(1 for v in firsts["arm_exit_matches_event_bar"].tolist()
                if v is True)),
        "n_arm_weave_exits": sum(1 for t in arm if t.exit_reason == "weave"),
        "max_abs_reconciliation_residual_r": (max(resid) if resid else None),
        # HOW MANY FIRST EVENTS THE RESIDUAL WAS ACTUALLY TAKEN OVER.  The max
        # above silently skips any first event whose arm campaign is missing,
        # so a max over ONE survivor and a max over all fifteen are the same
        # number to a reader — and "the residual is < 1e-9 for EVERY first
        # event" would then be a claim about one example. The count is
        # published so the assertion can be a CARDINALITY one, and
        # `_riders`/`_selftest` both require it to equal the event population.
        "n_first_events_reconciled": len(resid),
        # `_forgone_gross_r` prices no adds. Card v6 carries `adds_max = 0`, so
        # this is 0 and the model is exact — but a future card could turn adds
        # on and silently invalidate every cost in this file, so the count is
        # published rather than assumed.
        "n_base_campaigns_with_adds": sum(1 for t in base if t.adds),
        "base": base, "arm": arm, "amap": amap, "ev_keys": ev_keys,
    }
    _SCAN[key] = (bars, events, recon)
    return _SCAN[key]


def _riders(recon: dict, k: int) -> dict:
    """THE COLUMNS THAT MUST RIDE EVERY TABLE THIS MODULE EMITS.

    P-WEV-1's verdict of record, the reconciliation that ties this lab to it,
    and the four booleans that say what class of object the table is.  They are
    constant across the rows on purpose: the estate's own idiom (see
    `tierc7.ablation`'s `interaction_note`) is that a caveat a reader must not
    lose rides the frame rather than living in prose that can be cropped.

    WHAT WOULD MAKE THIS WRONG: dropping `pwev1_*` so the table reads as an
    effect claim; printing `scored = True` for anything in this file; or
    reporting `pwev1_consistent` as True while a reconciliation check failed.
    """
    n_ev_c = recon["n_campaigns_with_event"]
    mr = recon["max_abs_reconciliation_residual_r"]
    # THE RESIDUAL CHECK MUST HAVE RUN OVER EVERY FIRST EVENT BEFORE IT MAY
    # REPORT CONSISTENT.  The previous form read `mr is None or mr < 1e-6`,
    # which returns True when the residual was never computed at all — exactly
    # the failure `weave_quality`'s docstring forbids ("letting
    # pwev1_consistent read True when the residual check did not run"). A
    # window with no events is consistent by vacuity and says so via
    # `reconciliation_ran`; a window WITH events must have reconciled all of
    # them.
    ran = bool(n_ev_c and recon["n_first_events_reconciled"] == n_ev_c)
    consistent = bool(
        recon["event_set_equals_differing_set"]
        and recon["n_first_events_matching_arm_exit_bar"]
        == n_ev_c
        == recon["n_arm_weave_exits"]
        and (ran and mr is not None and mr < 1e-6
             if n_ev_c else mr is None))
    # THE ARM IS PINNED AT THE REGISTER'S k, NOT AT THE CALLER'S.  `arm` is
    # always `RC.CARD_WEAVE_ONLY`, whose `weave_k` is `RC.WEAVE_K` — so on a
    # call with any other k the events are the caller's and every arm,
    # reconciliation, D15 and LOAO column still describes the k = RC.WEAVE_K
    # book. These two riders used to be the literal True/False regardless of
    # the call, i.e. a table swept over k asserted on its own face that it had
    # not been swept. They are now derived from the k in hand.
    pinned = bool(int(k) == int(RC.WEAVE_K))
    return {
        "weave_k": int(k),
        "weave_k_pinned_not_swept": pinned,
        "weave_k_of_register": int(RC.WEAVE_K),
        "arm_book_weave_k": int(RC.CARD_WEAVE_ONLY.weave_k),
        "reconciliation_ran": ran,
        "reconciliation_n_first_events_reconciled": recon[
            "n_first_events_reconciled"],
        "counterfactual": True,
        "counterfactual_note": COUNTERFACTUAL_NOTE,
        "scored": False,
        "gates_nothing": True,
        "selection_surface": False,
        "selection_surface_note": (
            "NOT a selection surface — nothing is chosen FROM this table. "
            f"weave_k is PINNED at {RC.WEAVE_K} by the register and NO grid is "
            "built over it here."
            if pinned else
            f"OFF-REGISTER CALL: weave_k = {int(k)}, the register pins "
            f"{RC.WEAVE_K}. The EVENTS in this table are the caller's k, but "
            f"the arm book is CARD_WEAVE_ONLY at weave_k = {RC.WEAVE_K}, so "
            "arm_realized_delta_r, every reconciliation_* column, the D15 "
            "block and the LOAO block still describe the k = "
            f"{RC.WEAVE_K} arm and DO NOT correspond to these events. This row "
            "is not comparable with a pinned row and must not be tabulated "
            "beside one."),
        "tier": "TIER-E signal quality — measurement, UNSCORED, gates nothing",
        "d15_note": (
            "The D15 columns ride THIS ROW'S CELL — the weave-arm campaigns "
            "behind the events in this row — paired against the full base "
            "book. `n_paired` is therefore the CELL's, never the "
            "registration's: P-WEV-1 is scored over 196 paired campaigns and "
            "its point estimate is the pwev1_* columns. D15 GATES NOTHING."),
        **PWEV1_OF_RECORD,
        "reconciliation_event_set_equals_differing_set": recon[
            "event_set_equals_differing_set"],
        "reconciliation_first_events_matching_arm_exit_bar": recon[
            "n_first_events_matching_arm_exit_bar"],
        "reconciliation_arm_weave_exits": recon["n_arm_weave_exits"],
        "reconciliation_max_abs_residual_r": recon[
            "max_abs_reconciliation_residual_r"],
        "pwev1_consistent": consistent,
        "n_base_campaigns_with_adds": recon["n_base_campaigns_with_adds"],
        "cost_model_valid_no_adds": bool(
            recon["n_base_campaigns_with_adds"] == 0),
    }


def _cell(recon: dict, keys) -> list:
    """The weave-arm campaigns behind a set of (symbol, lane, entry_ms) keys,
    so the D15 columns have a book to ride.

    WHAT WOULD MAKE THIS WRONG: keying on the symbol alone, or on
    (symbol, entry_ms) — two LANES can enter one asset on one bar, which is
    exactly why `_scan`'s `amap` needs all three fields, so a two-field key
    would pull a second lane's campaign into a cell that never held it. Or
    returning BASE campaigns — D15's `cell` argument is the CHANGED book and
    returning the unchanged one would print a paired delta of exactly zero on
    every row.
    """
    out = []
    for t in recon["arm"]:
        if (t.symbol, t.lane, t.entry_ms) in keys:
            out.append(t)
    return out


def _stats(sub: pd.DataFrame, prefix: str = "") -> dict:
    """Count-and-cost summary of one cut of the event frame.

    WHAT WOULD MAKE THIS WRONG: reporting a mean without its n beside it (a mean
    over one row is not a mean), or summing `too_early_cost_r` across BOTH
    first and later events — a later event lives inside a campaign the armed
    weave had already exited, and adding the two double-counts the same
    campaign's forward path.  The caller passes ONE scope; this function does
    not mix them.
    """
    n = len(sub)
    if not n:
        return {f"{prefix}n_events": 0, f"{prefix}n_campaigns": 0,
                f"{prefix}n_in_profit": 0, f"{prefix}pct_in_profit": None,
                f"{prefix}n_exit_was_early": 0, f"{prefix}n_exit_was_right": 0,
                f"{prefix}n_exit_was_neutral": 0,
                f"{prefix}too_early_cost_r_total": None,
                f"{prefix}too_early_cost_r_mean": None,
                f"{prefix}too_early_cost_r_median": None,
                f"{prefix}cost_r_from_early_events": None,
                f"{prefix}cost_r_from_right_events": None,
                f"{prefix}unit_move_r_at_event_mean": None,
                f"{prefix}peak_unit_move_r_mean": None,
                **{f"{prefix}fwd_{h}_bars_r_mean": None for h in FWD_HORIZONS},
                f"{prefix}provisional": True}
    c = sub["too_early_cost_r"].astype(float)
    early = c[c > 1e-9]
    right = c[c < -1e-9]
    return {
        f"{prefix}n_events": n,
        f"{prefix}n_campaigns": int(sub.groupby(
            ["symbol", "lane", "campaign_entry_ms"]).ngroups),
        f"{prefix}n_in_profit": int(sub["in_profit_at_event"].sum()),
        f"{prefix}pct_in_profit": T7.pct(int(sub["in_profit_at_event"].sum()),
                                         n),
        f"{prefix}n_exit_was_early": int(len(early)),
        f"{prefix}n_exit_was_right": int(len(right)),
        f"{prefix}n_exit_was_neutral": int(n - len(early) - len(right)),
        f"{prefix}too_early_cost_r_total": T7.r4(float(c.sum())),
        f"{prefix}too_early_cost_r_mean": T7.r6(float(c.mean())),
        f"{prefix}too_early_cost_r_median": T7.r6(float(c.median())),
        f"{prefix}cost_r_from_early_events": T7.r4(float(early.sum())),
        f"{prefix}cost_r_from_right_events": T7.r4(float(right.sum())),
        f"{prefix}unit_move_r_at_event_mean": T7.r6(
            float(sub["unit_move_r_at_event"].astype(float).mean())),
        f"{prefix}peak_unit_move_r_mean": T7.r6(
            float(sub["peak_unit_move_r_to_event"].astype(float).mean())),
        **{f"{prefix}fwd_{h}_bars_r_mean": T7.r6(
            float(sub[f"fwd_{h}_bars_r"].astype(float).mean()))
           for h in FWD_HORIZONS},
        f"{prefix}provisional": bool(n < RC.PROVISIONAL_MIN_N),
    }


# ════════════════════════════════════════════════════════════════ THE TABLES
def weave_events(lo_ms: int, hi_ms: int, k: int = RC.WEAVE_K) -> pd.DataFrame:
    """EVERY WEAVE EVENT IN THE v6 BOOK, ONE ROW EACH, WHOLE — the per-event
    too-early cost.

    The base book is run with `RC.CARD_V6_CONTROL` (weave OFF, so nothing here
    ever fired), each campaign's weave-eligible bars are walked, and
    `RC.weave_fires` is asked on the CAMPAIGN's direction.  For each event the
    row carries: the bar, the unit move at that bar and whether the campaign was
    in profit (three readings, all printed, none used as a filter), the
    campaign's ACTUAL eventual outcome — it did not exit, this is the base book
    — the forward price move over the next 6, 24 and 100 bars in R, and the
    harvest-aware counterfactual cost with its verdict.

    `is_first_in_campaign` / `is_the_arms_counterfactual` marks the ONE event
    per campaign the armed weave would really have faced.  Later events are kept
    and flagged, not dropped: they are hypotheticals inside a campaign the armed
    weave had already exited, and deleting them would hide that the signal
    repeats 2.8x per campaign it touches.

    ON THIS CORRIDOR: 42 events, 15 campaigns, 15 first events.  ONE event of
    the 42 is in profit at its bar; ZERO are in profit on the harvest-inclusive
    mark.  The commission's "too-early cost on profitable campaigns" therefore
    has n = 1 and the row says so on its face.

    WHAT WOULD MAKE THIS WRONG: scanning bars the armed weave cannot reach
    (`_eligible_last_bar`); asking `weave_fires` on a fixed direction rather
    than the campaign's — the slope clause is read `slope * direction <= 0` and
    a fixed sign would fire on winning shorts; filtering to the in-profit events
    and reporting a mean over the survivors; treating the 100-bar forward move
    as recoverable P&L when the card's stop had already closed the campaign; or
    summing the cost across first AND later events of the same campaign, which
    double-counts one forward path.
    """
    _, events, _ = _scan(lo_ms, hi_ms, k)
    return events.copy()


def weave_quality(lo_ms: int, hi_ms: int, k: int = RC.WEAVE_K) -> pd.DataFrame:
    """THE CLASSIFICATION GRID — exit-was-right vs exit-was-early — REPORTED
    WHOLE, with the selection base rate and the P-WEV-1 reconciliation riding
    every row.

    Two SCOPES, each cut three ways and every cell printed even when empty:

      scope "FIRST event in campaign"  — the 15 decisions the armed weave would
                                         really have faced.  THE arm's
                                         counterfactual.
      scope "EVERY event"              — all 42, including the 27 that sit
                                         inside a campaign the armed weave had
                                         already exited.  Hypothetical inside a
                                         hypothetical; kept because the grid is
                                         reported whole, flagged because it is.

      cut "all"          — one row.
      cut "profit state" — in profit at the event bar / NOT in profit.  These
                           two partition the scope.
      cut "verdict"      — exit-was-early / exit-was-right / exit-was-neutral.
                           These three partition the scope.
      Rows WITHIN a cut partition; rows ACROSS cuts do not, and the `cut`
      column is there so no one adds them up.

    THE SELECTION COLUMNS ARE THE FINDING, AND THEY COME IN TWO DENOMINATORS
    BECAUSE THE POOLED ONE IS NOT A PURE RULE EFFECT.
    `open_bars_in_profit_pct` (79.47% of 3,960 open campaign bars) against
    `event_bars_in_profit_pct` (2.38% of 42) is 33.4x — but the events sit in
    only 15 campaigns and those 15 are worse than the other 181 (55.35% of
    their bars in profit against 82.84%), so 33.4x multiplies a
    CAMPAIGN-selection effect by the rule's BAR-selection effect.
    `selection_ratio_open_over_event_within_event_campaigns` holds the campaign
    fixed and is **23.2x**; that is the number that says "the weave fires on
    losing bars", and it is the one to quote about the RULE.  Both are printed
    from the same walk with `selection_decomposition_note` naming which claim
    each supports.  "The weave fires on losers" is not a claim about the book
    being bad; it is a claim about the RULE, and only the WITHIN-campaign ratio
    can make it.

    THE RECONCILIATION COLUMNS TIE THIS TABLE TO A REGISTRATION IT MUST NOT
    CONTRADICT.  `+0.5695 R` of gross cost minus `0.0496 R` of fee and funding
    saved is the weave arm's realised `-0.5198 R`, which over 196 paired
    campaigns is P-WEV-1's `-0.002652 R` point estimate.  Both sides are derived
    independently — cost from the base book's prices, delta from a separately
    run `CARD_WEAVE_ONLY` book — and the residual is 1.2e-16 per campaign.
    `pwev1_consistent` is the boolean; it is False if any check fails, and this
    module never raises, because a lab that gates nothing must not halt.

    D15 rides the aggregate rows and GATES NOTHING.  F-KEY is `["cut", "key"]`
    — `tierc7.run` writes this table under that key, and the scope is folded
    into `key` because `("verdict", "exit-was-early")` names a row in BOTH
    scopes and would not be unique on its own.

    WHAT WOULD MAKE THIS WRONG: dropping the empty verdict cell (the grid stops
    being whole); comparing the event in-profit rate against the population of
    CAMPAIGNS rather than of open BARS (a different denominator and a different
    claim); reading the cost total as a refutation of P-WEV-1's -0.0027 without
    dividing by the 196 paired campaigns the registration is scored over; or
    letting `pwev1_consistent` read True when the residual check did not run.
    """
    bars, events, recon = _scan(lo_ms, hi_ms, k)
    rid = _riders(recon, k)
    n_bars = len(bars)
    n_bars_profit = int(bars["in_profit"].sum()) if n_bars else 0
    n_ev = len(events)
    n_ev_profit = int(events["in_profit_at_event"].sum()) if n_ev else 0
    base_rate = (n_bars_profit / n_bars) if n_bars else None
    ev_rate = (n_ev_profit / n_ev) if n_ev else None

    # ── THE SELECTION EFFECT HAS TWO PARTS AND THE POOLED RATIO HIDES ONE.
    # `open_bars_in_profit_pct` is taken over ALL 196 campaigns, but the events
    # live in only 15 of them, and those 15 are the WORSE campaigns: 55.35% of
    # their open bars are in profit against 82.84% of the other 181's. So the
    # pooled 33.4x is a product of two effects —
    #     (A) WHICH CAMPAIGNS the weave fires in  (a campaign-selection effect)
    #     (B) WHICH BARS it fires on inside them  (the RULE effect)
    # — and only (B) is a statement about the rule. Holding the campaign fixed,
    # the ratio is 23.2x (25.4x against the non-event bars of the same
    # campaigns): the rule effect is real and large, but it is NOT the pooled
    # number, and the pooled number alone would have credited the rule with the
    # campaign selection too. Both denominators are therefore printed, from the
    # SAME walk, and the note says which claim each supports.
    if n_bars:
        in_ev = bars.apply(
            lambda r: (r["symbol"], r["lane"], r["campaign_entry_ms"])
            in recon["ev_keys"], axis=1)
        b_ev = bars[in_ev]
        b_ev_nonev = b_ev[~b_ev["is_weave_event"].astype(bool)]
    else:
        b_ev = b_ev_nonev = bars
    r_ev = (float(b_ev["in_profit"].mean()) if len(b_ev) else None)
    r_ev_ne = (float(b_ev_nonev["in_profit"].mean())
               if len(b_ev_nonev) else None)
    decomp = {
        "open_bars_in_event_campaigns": len(b_ev),
        "open_bars_in_event_campaigns_in_profit_pct": T7.pct(
            int(b_ev["in_profit"].sum()) if len(b_ev) else 0, len(b_ev)),
        "open_bars_in_event_campaigns_excl_event_bars": len(b_ev_nonev),
        "open_bars_in_event_campaigns_excl_event_bars_in_profit_pct": T7.pct(
            int(b_ev_nonev["in_profit"].sum()) if len(b_ev_nonev) else 0,
            len(b_ev_nonev)),
        "selection_ratio_open_over_event_pooled": (
            T7.r4(base_rate / ev_rate)
            if (ev_rate not in (None, 0) and base_rate is not None) else None),
        "selection_ratio_open_over_event_within_event_campaigns": (
            T7.r4(r_ev / ev_rate)
            if (ev_rate not in (None, 0) and r_ev is not None) else None),
        "selection_ratio_open_over_event_vs_nonevent_bars_same_campaigns": (
            T7.r4(r_ev_ne / ev_rate)
            if (ev_rate not in (None, 0) and r_ev_ne is not None) else None),
        "selection_decomposition_note": (
            "THE POOLED RATIO IS NOT A PURE RULE EFFECT. The events sit in a "
            "MINORITY of campaigns and those campaigns are worse than the rest, "
            "so selection_ratio_open_over_event_pooled multiplies a "
            "campaign-selection effect by the rule's bar-selection effect. The "
            "claim 'the weave fires on losing BARS' is carried ONLY by "
            "selection_ratio_open_over_event_within_event_campaigns, which "
            "holds the campaign fixed. Quote the within-campaign ratio for the "
            "rule; quote the pooled one only as the unconditional rate a reader "
            "would see, and say which is which."),
    }
    sel = {
        "open_campaign_bars_scanned": n_bars,
        "open_campaign_bars_in_profit": n_bars_profit,
        "open_bars_in_profit_pct": T7.pct(n_bars_profit, n_bars),
        "weave_event_bars": n_ev,
        "weave_event_bars_in_profit": n_ev_profit,
        "event_bars_in_profit_pct": T7.pct(n_ev_profit, n_ev),
        "selection_ratio_event_over_open": (
            T7.r4(ev_rate / base_rate)
            if (base_rate not in (None, 0) and ev_rate is not None) else None),
        "campaigns_scanned": recon["base_n_campaigns"],
        "campaigns_with_at_least_one_event": recon["n_campaigns_with_event"],
        "campaigns_with_no_event": (recon["base_n_campaigns"]
                                    - recon["n_campaigns_with_event"]),
        "n_in_profit_on_harvest_inclusive_mark": (
            int(events["in_profit_mtm_at_event"].sum()) if n_ev else 0),
        "selection_ratio_open_over_event": (
            T7.r4(base_rate / ev_rate)
            if (ev_rate not in (None, 0) and base_rate is not None) else None),
        **decomp,
    }

    scopes = [
        ("first-event", "FIRST event in campaign — THE arm's counterfactual",
         events[events["is_first_in_campaign"]] if n_ev else events),
        ("every-event",
         "EVERY event — later ones sit inside a campaign the arm had exited",
         events),
    ]
    rows = []
    for tag, scope, sub in scopes:
        cuts = [("all", "ALL", sub)]
        cuts += [("profit state", "in profit at the event bar",
                  sub[sub["in_profit_at_event"]] if len(sub) else sub),
                 ("profit state", "NOT in profit at the event bar",
                  sub[~sub["in_profit_at_event"]] if len(sub) else sub)]
        for v in ("exit-was-early", "exit-was-right", "exit-was-neutral"):
            cuts.append(("verdict", v,
                         sub[sub["verdict"] == v] if len(sub) else sub))
        for cut, cell, ss in cuts:
            keys = {(r.symbol, r.lane, r.campaign_entry_ms)
                    for r in ss.itertuples()}
            rows.append({
                # `cut` + `key` is this table's F-KEY, and the SCOPE is folded
                # into `key` because the same cell name appears in both scopes:
                # ("verdict", "exit-was-early") alone is NOT unique and
                # `assert_key` would halt the estate's driver on it.
                "cut": cut, "key": f"{tag} · {cell}",
                "scope": scope, "scope_tag": tag, "cell": cell,
                "share_of_scope_pct": T7.pct(len(ss), len(sub)),
                **_stats(ss),
                # THE ARM'S REALISED DELTA EXISTS ONLY ON FIRST EVENTS — a
                # later event is a decision the arm never reached, so it has no
                # realised anything. In the EVERY-event scope this total is
                # therefore over the FIRST events inside the cell and not over
                # all of them, and the count beside it says how many that is so
                # the two can never be read as the same denominator.
                "n_first_events_in_cell": (
                    int(ss["is_first_in_campaign"].sum()) if len(ss) else 0),
                "arm_realized_delta_r_over_first_events_in_cell": (
                    T7.r4(float(ss["arm_realized_delta_r"].dropna()
                                .astype(float).sum()))
                    if len(ss) and ss["arm_realized_delta_r"].notna().any()
                    else None),
                "fee_funding_saved_r_total": (
                    T7.r4(float(ss["fee_funding_saved_r_from_books"].dropna()
                                .astype(float).sum()))
                    if len(ss)
                    and ss["fee_funding_saved_r_from_books"].notna().any()
                    else None),
                **sel, **rid,
                **T7.d15(_cell(recon, keys), recon["base"]),
            })
    d = pd.DataFrame(rows)
    lo_ = T7.loao(recon["arm"], recon["base"], "L-WEAVE (mirrors P-WEV-1)")
    for kk, vv in lo_.items():
        if not kk.startswith("_"):
            d[kk] = vv
    d["loao_note"] = (
        "LOAO printed because this table is registration-SHAPED even though it "
        "registers nothing. It is the weave arm's own leave-one-asset-out line "
        "and it reproduces P-WEV-1's 0/5 exactly — the effect does not survive "
        "dropping any single asset, which is the same fact the CI already "
        "reports and is not a second test.")
    d["in_sample"] = True
    return d


def too_early_cost(lo_ms: int, hi_ms: int,
                   k: int = RC.WEAVE_K) -> pd.DataFrame:
    """THE TOO-EARLY COST IN R, AGGREGATED — overall, BY YEAR and BY ASSET,
    every grid WHOLE.

    Five cuts, each reported entire: `ALL`; every year in the corridor
    including the two with no events at all; every asset in `RC.UNIVERSE`
    including the two with a single event; both directions; and the profit
    state the commission actually asked about.

    TWO SCOPES SIT SIDE BY SIDE IN COLUMNS RATHER THAN IN ROWS, so they can
    never be added.  `first_*` is the arm's real counterfactual — the ONE event
    per campaign the armed weave would have faced, and the only column whose
    total reconciles to the weave arm.  `all_*` prices every event as if the
    weave had been ignored until then; it is a hypothetical inside a
    hypothetical and its name says so.

    ON THIS CORRIDOR, first-event scope: **+0.5695 R** of gross cost over 15
    events, 4 of which were early and 11 of which were right.  The entire
    positive mass is three campaigns that recovered from a deep drawdown the
    weave would have cut — ETHUSDT 2021 (+1.0732 R), SOLUSDT 2025 (+0.5223 R),
    BTCUSDT 2020 (+0.5179 R).  The cost of the ONE in-profit event is
    **-0.0727 R** — i.e. on the single occasion the weave would have exited a
    campaign that was actually in profit, exiting was RIGHT.

    D15 rides every row against the base book and GATES NOTHING.  Rows with
    n < RC.PROVISIONAL_MIN_N carry `first_provisional` / `all_provisional`,
    which on this corridor is every row of every cut.  F-KEY is
    `["cut", "key"]`, with `cut` mirroring `group` so both L-WEAVE tables carry
    the one key `tierc7.run` writes them under.

    WHAT WOULD MAKE THIS WRONG: adding `first_too_early_cost_r_total` to
    `all_too_early_cost_r_total` (the same campaign's forward path, counted
    twice); omitting the zero-event years or assets so the reader cannot see how
    thin the grid is; attributing the cost to the year of the campaign's ENTRY
    rather than of the EVENT (the cost accrues at the event bar); or reading the
    +0.5695 R total as an effect size — it is 0.29% of the base book's
    +39.7819 R and P-WEV-1's CI already covers zero.
    """
    _, events, recon = _scan(lo_ms, hi_ms, k)
    rid = _riders(recon, k)
    firsts = (events[events["is_first_in_campaign"]] if len(events)
              else events)

    y0, y1 = int(T7.iso(lo_ms)[:4]), int(T7.iso(hi_ms)[:4])
    cuts: list[tuple[str, str, pd.Series | None]] = [("ALL", "ALL", None)]
    for y in range(y0, y1 + 1):
        cuts.append(("year", str(y),
                     (events["event_year"] == y) if len(events) else None))
    for s in sorted(RC.UNIVERSE):
        cuts.append(("asset", s,
                     (events["symbol"] == s) if len(events) else None))
    for dd, word in ((1, "long"), (-1, "short")):
        cuts.append(("direction", word,
                     (events["direction"] == dd) if len(events) else None))
    for flag, word in ((True, "in profit at the event bar"),
                       (False, "NOT in profit at the event bar")):
        cuts.append(("profit_state", word,
                     (events["in_profit_at_event"] == flag) if len(events)
                     else None))

    rows = []
    for group, key, mask in cuts:
        if mask is None:
            sub_all, sub_first = events, firsts
        else:
            sub_all = events[mask]
            sub_first = firsts[mask.reindex(firsts.index)] if len(firsts) \
                else firsts
        keys = {(r.symbol, r.lane, r.campaign_entry_ms)
                for r in sub_first.itertuples()}
        rows.append({
            # `cut` mirrors `group` so this table carries the same F-KEY
            # (`cut`, `key`) that `tierc7.run` writes both L-WEAVE tables with.
            "cut": group, "key": key, "group": group,
            **_stats(sub_first, "first_"),
            **_stats(sub_all, "all_"),
            "first_arm_realized_delta_r_total": (
                T7.r4(float(sub_first["arm_realized_delta_r"].dropna()
                            .astype(float).sum())) if len(sub_first) else None),
            "first_fee_funding_saved_r_total": (
                T7.r4(float(sub_first["fee_funding_saved_r_from_books"]
                            .dropna().astype(float).sum()))
                if len(sub_first) else None),
            "scope_note": (
                "first_* is the arm's real counterfactual (one decision per "
                "campaign) and is the ONLY total that reconciles to the weave "
                "arm. all_* prices later events too — a hypothetical inside a "
                "hypothetical. THE TWO MUST NEVER BE ADDED."),
            **rid,
            **T7.d15(_cell(recon, keys), recon["base"]),
        })
    d = pd.DataFrame(rows)
    d["in_sample"] = True
    return d


# ═════════════════════════════════════════════════════════════════════ SELF-TEST
def _selftest(lo_ms: int | None = None, hi_ms: int | None = None) -> dict:
    """CARDINALITY ASSERTIONS, NOT EXAMPLES.  Returns a dict; raises on failure.

    Every check is a count or a bound over the WHOLE population:
      0  (symbol, lane, entry_ms) is a campaign identity in the base book —
         asserted, because every key in this module rests on it;
      1  every event's bar lies inside the range the RIDE allows, stated from
         `exit_i` / `exit_reason` and NOT by re-calling `_eligible_last_bar`;
         plus the count of events sitting on a bar the ride broke out of is 0;
      1b the live event frame's columns EQUAL `EVENT_COLUMNS`, in order, so the
         declared schema an event-free window returns cannot drift from the
         schema a populated one returns;
      2  the set of campaigns holding a first event EQUALS the set of campaigns
         whose net_r differs between the base book and the weave arm;
      3  every first event's bar EQUALS its weave-arm campaign's exit bar, and
         that campaign's exit reason is "weave" — 15 of 15, no exceptions;
      4  the residual was taken over EVERY first event (the count is asserted
         first, so the bound is cardinality and not existence) and is < 1e-9;
      5  the first-event cost total plus the arm's realised delta equals the fee
         and funding saved, read from the two books, to a tolerance that SCALES
         with n because the three columns are stored rounded;
      6  no base campaign carries adds, which is what makes `_forgone_gross_r`
         exact rather than approximate;
      7  the whole grids are whole — one row per corridor year and one per
         panel asset in `too_early_cost`, six cells per scope in
         `weave_quality`, and both F-KEYs unique.

    WHAT WOULD MAKE THIS WRONG: asserting any of these on a single row (the
    house rule: a check satisfied by ONE example is not a check) — which is why
    check 4 asserts its POPULATION before its bound; or comparing a value to a
    re-derivation of itself — which is why check 1 no longer calls the helper
    that produced the events it is checking, and why checks 2 to 5 compare THIS
    module's price-path model against a separately-run `CARD_WEAVE_ONLY` book,
    a different derivation by a different code path.
    """
    if lo_ms is None or hi_ms is None:
        lo_ms, hi_ms, _ = T7.corridor()
    bars, ev, recon = _scan(lo_ms, hi_ms, RC.WEAVE_K)
    bmap = {(t.symbol, t.lane, t.entry_ms): t for t in recon["base"]}
    assert len(bmap) == len(recon["base"]), (
        "(symbol, lane, entry_ms) is not a campaign identity in the base book")

    # 1 · ELIGIBILITY, CHECKED AGAINST THE CAMPAIGN'S OWN FIELDS AND NOT
    # AGAINST `_eligible_last_bar`.  The previous form re-called
    # `_eligible_last_bar` on the same campaign object that had just produced
    # the loop bound `range(entry_i + 1, _eligible_last_bar(t) + 1)`, so `bad`
    # was empty by construction and the check had NO detection power: swapping
    # in the alternative the function's docstring explicitly refuses
    # (`lambda t: t.exit_i`) left this assertion passing. It now states the
    # rule from `exit_i` / `exit_reason` directly — a campaign that exits for
    # any reason other than `corridor_end` broke out of `_ride_leg`'s loop
    # BEFORE step 6, so no event may sit on its exit bar — which is a fact
    # about the ride, not about this module's helper, and which the wrong
    # helper does violate.
    bad = []
    for r in ev.itertuples():
        t = bmap[(r.symbol, r.lane, r.campaign_entry_ms)]
        cap = t.exit_i if t.exit_reason == "corridor_end" else t.exit_i - 1
        if not (t.entry_i < r.event_i <= cap):
            bad.append((r.symbol, r.event_i, t.exit_reason, t.exit_i))
    assert not bad, (f"{len(bad)} events outside the weave-eligible range "
                     f"{bad[:5]}")
    # and the bar the ride provably cannot test is empty of events, stated as a
    # count over the whole book rather than as a range on each row
    n_on_break_bar = sum(
        1 for r in ev.itertuples()
        if bmap[(r.symbol, r.lane, r.campaign_entry_ms)].exit_reason
        != "corridor_end"
        and r.event_i == bmap[(r.symbol, r.lane, r.campaign_entry_ms)].exit_i)
    assert n_on_break_bar == 0, (
        f"{n_on_break_bar} events on a bar the ride broke out of before the "
        f"weave test could run")

    assert list(ev.columns) == list(EVENT_COLUMNS), (
        "EVENT_COLUMNS has drifted from the row builder: "
        f"{set(ev.columns) ^ set(EVENT_COLUMNS)}")

    assert recon["event_set_equals_differing_set"], (
        f"campaigns with a first event ({recon['n_campaigns_with_event']}) != "
        f"campaigns whose book differs ({recon['n_campaigns_book_differs']})")

    firsts = ev[ev["is_first_in_campaign"]]
    n_match = int(firsts["arm_exit_matches_event_bar"].sum())
    assert n_match == len(firsts) == recon["n_arm_weave_exits"], (
        f"bar-exact match {n_match} / {len(firsts)} first events, "
        f"{recon['n_arm_weave_exits']} arm weave exits")

    # 4 · THE RESIDUAL, AND THE POPULATION IT WAS TAKEN OVER.  `max(resid)`
    # skips any first event whose arm campaign is missing, so the bound alone
    # cannot tell a max over fifteen from a max over one — which would make
    # "the residual is < 1e-9 for EVERY first event" a claim satisfied by a
    # single example. The count is asserted first, so the bound is a
    # cardinality statement and not an existence one.
    assert recon["n_first_events_reconciled"] == len(
        ev[ev["is_first_in_campaign"].astype(bool)]) == recon[
        "n_campaigns_with_event"], (
        f"residual taken over {recon['n_first_events_reconciled']} of "
        f"{recon['n_campaigns_with_event']} first events")
    mr = recon["max_abs_reconciliation_residual_r"]
    assert mr is not None and mr < 1e-9, f"residual {mr}"

    assert recon["n_base_campaigns_with_adds"] == 0, (
        f"{recon['n_base_campaigns_with_adds']} base campaigns carry adds — "
        f"_forgone_gross_r prices no adds and every cost in this file is void")

    cost = float(firsts["too_early_cost_r"].astype(float).sum())
    delta = float(firsts["arm_realized_delta_r"].astype(float).sum())
    ff = float(firsts["fee_funding_saved_r_from_books"].astype(float).sum())
    # THE TOLERANCE MUST SCALE WITH n.  Each of these three columns is stored
    # through `T7.r6`, so every row carries up to 5e-7 of rounding and the sum
    # of 15 rows carries up to 7.5e-6 — MORE than the flat 1e-6 this used to
    # assert. The check was therefore one lucky book away from failing for a
    # reason that is not a defect. The per-row residual is check 4's business
    # and is exact; this one is the aggregate and is given the aggregate's
    # error bar.
    tol = 1e-9 + 5e-7 * 3 * max(1, len(firsts))
    assert abs((cost + delta) - ff) < tol, (cost, delta, ff, tol)

    q = weave_quality(lo_ms, hi_ms)
    tec = too_early_cost(lo_ms, hi_ms)
    y0, y1 = int(T7.iso(lo_ms)[:4]), int(T7.iso(hi_ms)[:4])
    assert int((tec["group"] == "year").sum()) == (y1 - y0 + 1)
    assert int((tec["group"] == "asset").sum()) == len(RC.UNIVERSE)
    assert q.groupby("scope").size().tolist() == [6, 6]

    # F-KEY — both tables are written by `tierc7.run` with key ["cut", "key"],
    # and `assert_key` HALTS the estate on a duplicate. Checked here so the
    # halt cannot first happen inside somebody else's build.
    for nm, d in (("weave_quality", q), ("too_early_cost", tec)):
        assert not int(d.duplicated(subset=["cut", "key"]).sum()), (
            f"{nm} key ['cut','key'] is not unique")

    ev_cols = set(ev.columns)
    assert {"counterfactual", "is_the_arms_counterfactual", "too_early_cost_r",
            "verdict", "in_profit_at_event"} <= ev_cols
    for d in (q, tec):
        assert bool(d["counterfactual"].all()) and not bool(d["scored"].any())

    return {
        "n_events": len(ev), "n_first_events": len(firsts),
        "n_campaigns_with_event": recon["n_campaigns_with_event"],
        "open_bars": len(bars),
        "open_bars_in_profit_pct": T7.pct(int(bars["in_profit"].sum()),
                                          len(bars)),
        "event_bars_in_profit_pct": T7.pct(int(ev["in_profit_at_event"].sum()),
                                           len(ev)),
        "too_early_cost_r_first_total": T7.r4(cost),
        "arm_realized_delta_r_total": T7.r4(delta),
        "fee_funding_saved_r_total": T7.r4(ff),
        "max_abs_residual_r": mr,
        "weave_quality_rows": len(q), "too_early_cost_rows": len(tec),
        "pwev1_consistent": bool(q["pwev1_consistent"].all()),
    }


if __name__ == "__main__":                                # pragma: no cover
    import json
    print(json.dumps(_selftest(), indent=2, default=str))
