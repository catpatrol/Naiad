"""TIER-C6 rev B · L-AE and L-LIMIT-2 — THE LIMIT FRONTIER.

Commissioned by the operator, in his words: *"better/tighter limit entries, find
the n x ATR sweet spot"*.  It cures open ruling **F-C5-g**.

────────────────────────────────────────────────────────────────────────────
WHAT F-C5-g SAID, AND WHAT THIS MODULE DOES ABOUT IT
────────────────────────────────────────────────────────────────────────────
Tier-C5's `limit_grid` priced every S-LIMIT level at `k x AVG-AE x r_dist`,
where AVG-AE was the mean adverse excursion of the WINNERS of the very
195-campaign book those levels were then scored on.  The offset was a statistic
of its own outcome variable.  Five expectancies, no held-out anything.

**THE FITTED QUANTITY IS GONE.**  Here `k` multiplies `t.atr_at_entry` — the
ATR(14) the card already computed at its own trigger bar, before any outcome
existed.  Nothing derived from `net_r`, from `mae_to_1r_r`, or from any winner
sub-population enters the fill rule.  Grep this file: the Tier-C5 scalar is read
exactly once, inside `legacy_ae_study`, which REPRODUCES the old table as the
durable S-LIMIT statistic and hands its scalar to nobody.

────────────────────────────────────────────────────────────────────────────
**THE SELECTION SURFACE IS NOT GONE.  ALL FIVE RESIDUALS, NAMED.**
────────────────────────────────────────────────────────────────────────────
Asked to state honestly whether ANY residual in-sample fitting survives — it
does, and here is the whole of it:

1. **THE k GRID ITSELF.**  5 levels x 2 arms = **10 cells**.  An argmax over 10
   cells is a selection whether or not it is called one.  m = 10 is declared in
   `LIM2_PREREG` — a module constant, defined above every function that could
   look at a result — and is carried on every frontier row.
2. **THE CORRIDOR.**  Panel start -> latest closed 4h bar, box open.  Everything
   in TIER-C5 and TIER-C6 was measured here.  The frontier is *conditionally*
   out-of-sample given the card and *in-sample* with respect to the corridor.
   F-C5-b is not cured by anything in this file.
3. **THE CARD'S OWN KNOBS** — d = 0.75, rail 1.0 ATR, trail (3,3) armed after
   +1R, band harvest, WARMUP_BARS = 316.  The arms inherit them; they do not
   re-fit them, and they do not launder them either.
4. **ATR_LEN = 14 AND `atr_at_entry`.**  Inherited from v1.  Not re-chosen here,
   but it is the scale the offset is denominated in, and a different ATR length
   would move every fill on the frontier.
5. **THE OFFERED SET.**  The frontier rides THE CARD'S OWN campaigns.  The
   population was produced by the card, so `miss_pct` is a statement about the
   card's triggers, not about limit orders in general.

Verdict, printed on the table's face:
**"THE FITTED QUANTITY IS GONE.  THE SELECTION SURFACE IS NOT.  m = 10,
declared before the look; the corridor is the same one everything else was
built on."**

ONE CLAUSE WAS ADDED TO THE COMMISSIONED PRE-REGISTRATION WORDING, AND IT IS
DISCLOSED: the draft said *"argmax of expectancy_r"* without naming the
denominator.  "Expectancy" over the FILLED set and over the OFFERED set rank the
k grid differently, and an ambiguous pre-registration is not a pre-registration.
The denominator is fixed here as **the OFFERED set (all campaigns the card
took, misses included at their true value)** — because a limit that never fills
earns nothing and no one can spend a per-fill expectancy.  Both are printed;
only the offered one is the form's argument.

────────────────────────────────────────────────────────────────────────────
THE SPLIT-ENTRY RESOLUTION: (A) TWO STOPS, ONE R
────────────────────────────────────────────────────────────────────────────
*"Stop 1R beyond each fill"* admitted two readings.  Taken: **TWO STOPS**.  The
market half stops at `entry_px - d*r_dist` (which IS `t.stop_px`, exactly — the
identity holds to 0.0 on all 195 campaigns of the v6 book, verified in
`selfcheck`); the limit half stops 1R beyond ITS OWN fill.  Rejected: one
blended stop at the mid, because between the trigger and the fill that half
would be carried with its stop BEYOND the card's structural anchor, which is
look-ahead — it is only justifiable if you already know the limit will fill, and
the miss rate here runs 2%-16%.

**R IS NOT RE-DERIVED PER FILL.**  Both halves use the campaign's `t.r_dist`.
Two stops, one denominator; without that, R stops being additive and the book
stops summing.  Campaign worst case is exactly 1.0R either way.

────────────────────────────────────────────────────────────────────────────
HOUSE RULES OBSERVED
────────────────────────────────────────────────────────────────────────────
* D15 columns ride every frontier row and **GATE NOTHING**.
* Every grid is reported WHOLE — 10 cells built, 10 cells printed, nothing
  dropped and nothing promoted in-sample.
* The frontier is a SELECTION SURFACE and says so IN A COLUMN, on every row.
* Every function's docstring states WHAT WOULD MAKE IT WRONG.
* Cross-checks go by a DIFFERENT PATH where one exists, and `selfcheck` marks
  each leg `INDEPENDENT` or `REPLICATION` so a replication can never be mistaken
  for evidence.
* Anything under `PROVISIONAL_MIN_N = 30` carries `provisional`.

────────────────────────────────────────────────────────────────────────────
TWO THINGS THE TABLE SAYS THAT THE COMMISSION DID NOT ANTICIPATE
────────────────────────────────────────────────────────────────────────────
**1. THE FORM IS FALSIFIED IN-SAMPLE BY ITS OWN CLAUSE (c).**  `k* = 0.40` on
both arms, and that cell's `max_single_trade_delta_share` is 41.4 — the paired
improvement over the card is +0.0013 R/campaign while a single campaign's delta
is forty times the whole sum.  F-C5-f's defect exactly: the number is real and
the mechanism is one trade.  `frontier` EVALUATES the pre-registered
falsification clauses against the table it just built and prints the verdict on
every row, because a falsification clause that is written and never run is
decoration.

**2. THE SPLIT ARM IS NOT A SECOND SEARCH.**  Under resolution (A) with the D12
ceiling inert, `net_r_split = 0.5*net_r_card + 0.5*net_r_limit` EXACTLY, so
`expectancy_split(k)` is an affine increasing transform of `expectancy_full(k)`
and `k*(SPLIT) == k*(FULL)` by construction.  Pre-registration clause (b) —
"k* differing between the two arms" — therefore CANNOT FIRE, and the effective
selection surface for the argmax is **5 cells, not 10**.  The declared m stays
10 (a declaration is not revised by its own result); the observation is printed
beside it and proved in `selfcheck` as F-C6-LIM-6.

WHAT COULD NOT BE BUILT: the SAIL validation.  "SAIL" appears NOWHERE in this
estate (zero grep hits).  This module emits the FORM and the frontier; the
validation clause is unbound and `LIM2_PREREG["the_instrument"]` says so on
every row.  See `prereg_text()`.
"""
from __future__ import annotations

import dataclasses
import hashlib
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

import tierc6 as T6                                                   # noqa: E402
import tierc6_rules as RC                                             # noqa: E402

# ── bound from the core, never copied ────────────────────────────────────────
frame, corridor, agg, d15 = T6.frame, T6.corridor, T6.agg, T6.d15
slices_of, tide_mix, wall = T6.slices_of, T6.tide_mix, T6.wall
champions, league, profit_side = T6.champions, T6.league, T6.profit_side
cluster_boot, _ci_from = T6.cluster_boot, T6._ci_from
_idx_range, _ride, _account = T6._idx_range, T6._ride, T6._account
iso, r4, r6, pct, _ms = T6.iso, T6.r4, T6.r6, T6.pct, T6._ms
_maxdd_r = T6.T5._maxdd_r
SEED = T6.SEED

# ═════════════════════════════════════════════ THE GRIDS, PINNED BEFORE A LOOK
K_GRID: tuple[float, ...] = (0.10, 0.20, 0.30, 0.40, 0.50)
FRONTIER_ARMS: tuple[str, ...] = ("FULL-LIMIT", "SPLIT-ENTRY")
LIM2_M: int = len(K_GRID) * len(FRONTIER_ARMS)          # = 10

AE_DECILES: tuple[float, ...] = tuple(round(0.1 * i, 1) for i in range(1, 10))
HAZARD_STEPS_R: tuple[float, ...] = tuple(round(0.05 * i, 2) for i in range(1, 21))
HAZARD_STEPS_ATR: tuple[float, ...] = tuple(round(0.10 * i, 2) for i in range(1, 21))

# multiples of the REGISTERED displacement gate, not in-sample quartiles —
# a quartile cut would be a fitted quantity and would reopen F-C5-g on a
# second axis.
DISP_EDGES: tuple[float, ...] = (RC.V5.D_DISPLACEMENT, 1.0, 1.5, 2.0, float("inf"))
DISP_LABELS: tuple[str, ...] = ("[0.75,1.0)", "[1.0,1.5)", "[1.5,2.0)", "[2.0,inf)")

WALL_TF: str = "12h"

OFFSET_BASIS: str = (
    "ABSOLUTE x ATR(14) at the trigger bar — NOT a multiple of avg-AE. "
    "F-C5-g's fitted quantity does not enter the fill rule.")

K_PROMOTED: str = "NO — NOTHING IS PROMOTED IN-SAMPLE"

SELECTION_SURFACE: str = (
    "SELECTION SURFACE. P-LIM-2 declares m = 10 frontier cells (5 k x 2 arms) "
    "and 0 in-sample tests, written down before the run. THE FITTED QUANTITY IS "
    "GONE. THE SELECTION SURFACE IS NOT. The corridor is the same one "
    "everything else was built on (F-C5-b uncured).")

MISS_SEMANTICS: dict[str, str] = {
    "FULL-LIMIT": ("FULL-LIMIT: no position taken. The forgone R is the whole "
                   "card's net_r on that trigger."),
    "SPLIT-ENTRY": ("SPLIT-ENTRY: half a card WAS taken; a 'miss' forgoes only "
                    "the limit half, so the forgone R is 0.5 x the card."),
}

D15_DISPOSITION: str = "D15 columns ride this row and GATE NOTHING."

CI_STAMP: str = ("INTERVAL, NOT A TEST — asset-cluster bootstrap of the PAIRED "
                 "per-campaign delta, 4000 draws, seed 20260816, unit of "
                 "replication = ASSET. Diagnostic only; no bar is applied here.")

WINDOW: str = "full_corridor"

# THE PUBLISHED TABLE LIST, in one place. `build` HALTs if what it returns
# differs from this, and F-C6-KEY enumerates its key coverage against it — so a
# table added to `build` cannot slip past the key check while the leg goes on
# claiming it covers "every published table".
BUILD_TABLES: tuple[str, ...] = (
    "ae_deciles", "legacy_ae_study", "hazard_curve", "hazard_curve_atr",
    "ae_by_context", "frontier", "selfcheck")

AE_POPULATION_NOTE: str = (
    "AE = -mae_held_r over ALL scored campaigns, winners and losers, "
    "recomputed post hoc from 4h bars. NOT mae_to_1r_r, which exists only on "
    "campaigns that reached +1R and cannot carry deciles by year.")


# ═════════════════════════════════════════════════ THE PRE-REGISTRATION (c)
LIM2_PREREG: dict = {
    "probe": "P-LIM-2",
    "declared_before_the_look": True,
    "m_in_sample_tests_run": 0,
    "m_cells_on_the_frontier": LIM2_M,
    "the_form": (
        "k* := argmax over k in {0.10,0.20,0.30,0.40,0.50} of expectancy_r, "
        "taken SEPARATELY within each arm A in {FULL-LIMIT, SPLIT-ENTRY}, on "
        "the TIER-C6 full-water book (panel start -> latest closed 4h bar). "
        "expectancy_r IS DENOMINATED IN THE OFFERED SET — every campaign the "
        "card took, misses included at their true value (0.0 for FULL-LIMIT, "
        "half a card for SPLIT-ENTRY) — because a limit that never fills earns "
        "nothing and no one can spend a per-fill expectancy. Ties are broken by "
        "the SMALLER k. THE FRONTIER IS A FORM, NOT A NUMBER: k*(A) is whatever "
        "the table says it is, and this text is fixed before the table exists."),
    "the_claim_to_be_tested_out_of_sample": (
        "H-LIM-2: on the out-of-sample instrument, arm A entered at offset "
        "k*(A) x ATR(14) at the trigger bar posts a per-campaign expectancy in "
        "R strictly greater than the same instrument's market-trigger card, "
        "measured by the asset-cluster bootstrap of the PAIRED per-campaign "
        "delta (cluster_boot / cluster_boot_diff, 4000 draws, seed 20260816, "
        "stat='mean', unit of replication = ASSET), 90% two-sided interval "
        "excluding zero above, BH-corrected at m = the number of tests actually "
        "run in that family. PAIRED, because the arm cannot change which "
        "campaigns exist — it rides inside the card's own offered set."),
    "the_instrument": (
        "*** UNBOUND AT DRAFTING. The commission names 'SAIL'; SAIL appears "
        "NOWHERE in this estate (zero grep hits over .py/.md/.json/.html). THIS "
        "TABLE MAY NOT BE PUBLISHED WITH A VALIDATION CLAUSE until the operator "
        "names the instrument, its corridor edges and its card version. The "
        "estate's only forward reserve today is the Prometheus paper route, and "
        "F-C5-k records that it is running v1, three card generations behind "
        "the book this form was measured on — so binding SAIL to it without a "
        "ruling would validate v6's entry rule on v1's entries. ***"),
    "what_is_promoted_in_sample": "NOTHING. No k is promoted here. Not one.",
    "what_would_falsify_the_form": (
        "expectancy_r non-monotonic in k with no interior maximum on EITHER arm "
        "(the 'frontier' would be noise and argmax would be picking the biggest "
        "of ten draws); or k* differing between the two arms by more than one "
        "grid step (the two arms would not be measuring one quantity); or a k* "
        "whose max_single_trade_delta_share >= 1.0 (F-C5-f's defect: the number "
        "is real and the mechanism is one trade)."),
    "sample_size_the_instrument_must_supply": (
        "PROVISIONAL_MIN_N = 30 scored campaigns on the instrument before "
        "H-LIM-2 is read at all; below that the row prints and the verdict does "
        "not."),
    "the_offset_basis": OFFSET_BASIS,
    "the_residual_in_sample_fitting": (
        "FIVE, ALL NAMED: (1) the k grid, m = 10; (2) the corridor, the same "
        "one everything else was built on — F-C5-b uncured; (3) the card's own "
        "knobs, inherited not re-fitted and not laundered; (4) ATR_LEN = 14, "
        "the scale the offset is denominated in; (5) the offered set, produced "
        "by the card, so miss_pct describes the card's triggers and not limit "
        "orders in general."),
}


def prereg_text() -> str:
    """THE PRE-REGISTRATION, as one string, for the table's face and the manifest.

    It is assembled from `LIM2_PREREG`, a module constant defined ABOVE every
    function in this file that can compute a result — so the text cannot have
    been written after the look without the diff showing it.

    WHAT WOULD MAKE THIS WRONG: editing `LIM2_PREREG` after a frontier has been
    read; dropping the instrument clause (the SAIL warning is the single largest
    caveat on the claim and it must not be separable from the numbers); or
    letting `m_cells_on_the_frontier` drift from `len(K_GRID)*len(FRONTIER_ARMS)`
    — `frontier` HALTs if the declared m and the constructed m disagree.
    """
    order = ("probe", "declared_before_the_look", "m_in_sample_tests_run",
             "m_cells_on_the_frontier", "the_form", "the_offset_basis",
             "the_claim_to_be_tested_out_of_sample", "the_instrument",
             "what_is_promoted_in_sample", "what_would_falsify_the_form",
             "sample_size_the_instrument_must_supply",
             "the_residual_in_sample_fitting")
    return "\n\n".join(f"{k.upper().replace('_', ' ')}:\n{LIM2_PREREG[k]}"
                       for k in order)


def prereg_sha256() -> str:
    """A stable digest of the pre-registration, carried on every frontier row.

    WHAT WOULD MAKE THIS WRONG: hashing a dict whose key order can vary (json
    with sort_keys=True fixes it), or hashing a rendering that omits a clause —
    the digest must cover the instrument warning too, or a published table could
    carry a matching hash with the warning stripped.
    """
    blob = json.dumps(LIM2_PREREG, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def write_prereg(path: str | Path) -> dict:
    """Write the pre-registration to disk BEFORE any frontier row exists.

    Returns the stamp `frontier(prereg_path=...)` verifies.  This is the
    F-C6-LIM-5 leg made operable: the text is on disk with an mtime, and the
    frontier refuses to run against a file whose sha does not match the constant
    it claims to be.

    WHAT WOULD MAKE THIS WRONG: writing it from inside `frontier` (the ordering
    claim would then be circular), or writing a summary rather than the whole
    dict — a pre-registration that omits the falsification clause pre-registers
    nothing.
    """
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    stamp = {"sha256": prereg_sha256(), "written_at": iso(int(time.time() * 1000)),
             "m_cells_on_the_frontier": LIM2_M, "prereg": LIM2_PREREG}
    p.write_text(json.dumps(stamp, indent=2, sort_keys=True, ensure_ascii=False))
    return {"path": str(p), "sha256": stamp["sha256"],
            "mtime_ms": int(p.stat().st_mtime * 1000)}


# ═══════════════════════════════════════════════ L-AE · THE ADVERSE EXCURSION
def campaign_mae(t) -> tuple[float, float]:
    """(mae_held_r, mae_tape_r) — the deepest adverse excursion of ONE campaign,
    in R.  Both are negative-or-zero.  THIS IS THE ONLY NEW MEASUREMENT IN THE
    AREA; everything else in this module is a lookup or an arithmetic
    combination.

    WHY IT EXISTS AT ALL.  `RC.Trade.mae_to_1r_r` is `None` on 94 of the v6
    book's 195 campaigns, because `_ride` only accumulates it while
    `not reached_1r` and discards it otherwise.  A curve conditioned on "max
    adverse >= x" needs the adverse excursion of EVERY campaign, winners and
    losers, so it is recomputed post hoc from the frame.  `RC.Trade` is not
    touched, `_ride` is not touched, and no filed book is re-run.

    HELD  what the campaign actually ENDURED: bars ti+1..exit_i, with the EXIT
          bar clipped to `exit_px` when the exit was a STOP — once the stop is
          taken you are OUT and the rest of that bar is not your excursion.
    TAPE  the raw bar extremes over the same bars, unclipped.  Printed BESIDE
          held so the gap-through is visible rather than absorbed, and NEVER
          used as a conditioning variable: on this book `mae_tape_r` differs
          from `mae_held_r` on 124 of 195 campaigns and runs to -4.589R, which
          is post-exit tape, not risk anybody carried.

    WHAT WOULD MAKE THIS WRONG: including bar `ti` (the card enters at a bar
    CLOSE, so the trigger bar has no tradeable remainder and its wick is not the
    campaign's excursion); running past `exit_i`; failing to clip the exit bar
    on a stop (held would then absorb the whole stop-bar wick and could print
    excursions deeper than the campaign's own stop); or clipping on a NON-stop
    exit (a bell or corridor-end exit prints at the close and the bar's adverse
    extreme before it was genuinely endured).
    """
    f, d, E, R = frame(t.symbol)["f"], t.direction, t.entry_px, t.r_dist
    a, b = t.entry_i + 1, t.exit_i + 1
    if b <= a:
        return 0.0, 0.0
    seg = (f.l[a:b] if d == 1 else f.h[a:b]).astype(float)
    adv = (seg - E) * d / R
    tape = float(min(0.0, adv.min()))
    held = adv.copy()
    if t.exit_reason == "stop":
        held[-1] = (float(t.exit_px) - E) * d / R
    return float(min(0.0, held.min())), tape


def _mae_to_1r_replicated(t) -> float | None:
    """`_ride`'s AE-to-first-+1R accumulator, replicated bar for bar.

    THIS IS A REPLICATION, NOT AN INDEPENDENT PATH, AND `selfcheck` LABELS IT SO.
    It re-walks the same bars with the same predicate the program used, so it
    can only catch INDEXING drift (an off-by-one in the scan window, a
    swapped high/low, a wrong R denominator) — it cannot corroborate the
    quantity's meaning.  The estate lost 6 of 16 TC5 repairs to checks that were
    exactly this and were reported as if they were more.  The independent leg is
    `_ledger_identity_rows`, which reaches `mae_held_r` through the trail ledger
    and the exit reason instead of through the bars.

    WHAT WOULD MAKE THIS WRONG: being read as corroboration; or drifting from
    `tierc6._ride` (the trigger bar excluded, the +1R test on the FAVOURABLE
    extreme, the `min` taken BEFORE the latch flips, the scan stopping at the
    campaign's own exit).
    """
    f, d, E, R = frame(t.symbol)["f"], t.direction, t.entry_px, t.r_dist
    m, reached = 0.0, False
    for j in range(t.entry_i + 1, t.exit_i + 1):
        fav = float(f.h[j]) if d == 1 else float(f.l[j])
        adverse = float(f.l[j]) if d == 1 else float(f.h[j])
        if reached:
            break
        m = min(m, (adverse - E) * d / R)
        if (fav - E) * d / R >= 1.0:
            reached = True
    return m if reached else None


def _regime_year(t) -> str:
    return iso(t.entry_ms)[:4]


def _r_over_atr(t) -> float:
    return float(t.r_dist) / float(t.atr_at_entry)


def _quantile_block(vals_r: np.ndarray, vals_atr: np.ndarray) -> dict:
    row: dict = {
        "mean_ae_r": r6(float(vals_r.mean())),
        "median_ae_r": r6(float(np.median(vals_r))),
        "mean_ae_atr": r6(float(vals_atr.mean())),
        "median_ae_atr": r6(float(np.median(vals_atr))),
        "p90_ae_r": r6(float(np.percentile(vals_r, 90))),
        "p90_ae_atr": r6(float(np.percentile(vals_atr, 90))),
        "max_ae_r": r6(float(vals_r.max())),
        "max_ae_atr": r6(float(vals_atr.max())),
    }
    for q in AE_DECILES:
        row[f"ae_r_d{int(round(q * 10))}"] = r6(float(np.quantile(vals_r, q)))
        row[f"ae_atr_d{int(round(q * 10))}"] = r6(float(np.quantile(vals_atr, q)))
    return row


def ae_deciles(book: list, lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """L-AE · AE DECILES, IN R **AND** IN ATR, by REGIME-YEAR and by ASSET.

    THREE GROUPINGS IN ONE FRAME, EACH ROW SAYING WHICH IT IS: `__PANEL__`
    (1 row), `asset` (one per asset present), `regime_year` (one per calendar
    year present).  Every year row carries `tide_mix`'s up/down/no-tide shares
    over that year's corridor slice, so "regime-year" is a REGIME and not just a
    calendar label — a 2022 book in a down-tide is a different object from a
    2022 book in a mixed one.

    ASSET x YEAR IS NOT REPORTED.  5 x 7 = 35 cells over 195 campaigns, median
    cell ~5.  The commission's "by regime-year AND by asset" is read as TWO
    MARGINS, and the cross is named as refused rather than printed at n = 5.

    R AND ATR WILL NOT RANK THE GROUPS THE SAME WAY, AND THAT IS THE POINT.
    `ae_atr = ae_r * r_over_atr`, exact — the same trigger-bar ATR the card
    used, never re-derived — and `r_over_atr` varies from 1.00 to 7.47 across
    this book, so a group with deep R-excursions can be a shallow-ATR group.
    Both are printed side by side.

    WHAT WOULD MAKE THIS WRONG: printing a group with n < PROVISIONAL_MIN_N
    without `provisional` (four of seven years are provisional on this book);
    recomputing the ATR column from an ATR other than the trigger bar's
    (`t.atr_at_entry`), which would silently re-scale every decile; conditioning
    the population on winners (the deciles would then be `ae_study`'s 58-winner
    statistic wearing a decile's name); or dropping the window label, which is
    what let three numbers seven times apart look like one number (F-C5-a).
    """
    groups: list[tuple[str, str, list]] = [("__PANEL__", "ALL", list(book))]
    for s in sorted({t.symbol for t in book}):
        groups.append(("asset", s, [t for t in book if t.symbol == s]))
    year_bounds = {k: (a, b) for g, k, a, b in slices_of(lo_ms, hi_ms) if g == "year"}
    for y in sorted({_regime_year(t) for t in book}):
        groups.append(("regime_year", y, [t for t in book if _regime_year(t) == y]))

    rows = []
    for by, key, ts in groups:
        if not ts:
            continue
        r = np.array([-campaign_mae(t)[0] for t in ts], dtype=float)
        oa = np.array([_r_over_atr(t) for t in ts], dtype=float)
        a = r * oa
        row = {"grouping": by, "bucket": by, "key": key, "n": len(ts),
               "f_key": "(bucket, key)",
               "provisional": bool(len(ts) < RC.PROVISIONAL_MIN_N),
               "window": WINDOW, "in_sample": True,
               "mean_r_over_atr": r6(float(oa.mean())),
               "winners_n": int(sum(1 for t in ts if t.net_r > 0)),
               "reached_1r_n": int(sum(1 for t in ts if t.reached_1r)),
               "population": AE_POPULATION_NOTE,
               "selection_surface": "NO — descriptive margins. Nothing is "
                                    "chosen, ranked or promoted on this table.",
               "asset_x_year_cross": "REFUSED: 5 assets x 7 years = 35 cells "
                                     "over 195 campaigns, median cell ~5. Two "
                                     "margins are reported; the cross is not.",
               }
        row.update(_quantile_block(r, a))
        if by == "regime_year" and key in year_bounds:
            a0, b0 = year_bounds[key]
            row.update({f"tide_{k}": v for k, v in tide_mix(a0, b0).items()})
            row["window"] = f"year_{key}"
        rows.append(row)
    return pd.DataFrame(rows)


def legacy_ae_study(book: list, lo_ms: int, hi_ms: int) -> pd.DataFrame:
    """S-LIMIT's OWN AE TABLE, reproduced beside the new one, unchanged.

    F-C5-g's finding was that *the AE study itself is the durable output* — what
    failed was pricing a grid with its mean.  So the two legacy rows (TC-BOOK,
    CENSUS-ERA; winner-conditioned, `mae_to_1r_r`) are reproduced by CALLING
    Tier-C5's own function rather than restating it, and its scalar return —
    the quantity F-C5-g convicted — is **discarded at the call site and reaches
    nothing in this module.**

    WHAT WOULD MAKE THIS WRONG: threading the returned scalar into any offset,
    bucket edge or decision anywhere in this file; or presenting these rows as
    comparable with `ae_deciles` (they are a different population — winners
    only, and truncated at the first +1R).
    """
    df, _discarded_fitted_scalar = T6.T5.ae_study(book, lo_ms, hi_ms)
    out = df.copy()
    out["statistic"] = "mae_to_1r_r, WINNERS ONLY — the S-LIMIT legacy"
    out["comparable_with_ae_deciles"] = False
    out["why_not_comparable"] = (
        "winner-conditioned and truncated at the first +1R; ae_deciles runs "
        "mae_held_r over ALL campaigns to the campaign's own exit.")
    out["the_mean_here_priced_nothing_in_this_module"] = True
    return out


# ═══════════════════════════════════════════════════════════ THE HAZARD CURVE
def _hazard_block(book: list, basis: str, steps: tuple[float, ...],
                  xs: np.ndarray, wins_mask: np.ndarray,
                  assets: np.ndarray) -> list[dict]:
    rows = []
    for x in steps:
        sel = xs >= x - 1e-12
        n = int(sel.sum())
        w = int(wins_mask[sel].sum())
        ci = {"lo": None, "hi": None, "p_one_sided": None}
        if n:
            draws = cluster_boot(wins_mask[sel].astype(float), assets[sel],
                                 seed=SEED, n_boot=4000)
            ci = _ci_from(draws, w / n)
        degen, approaching = "", False
        if basis == "R" and abs(x - 1.00) < 1e-12:
            degen = (f"IDENTITY, NOT EVIDENCE: -1.00R held == the initial, "
                     f"un-advanced stop was taken == the campaign ended at "
                     f"-1R. p_win = 0 is arithmetic, not a measurement. "
                     f"{n} campaigns.")
        if basis == "R" and x >= 0.95 - 1e-12:
            approaching = True
        if n == 0:
            printed = ("NOTHING TO READ: the conditioning set is EMPTY. n and "
                       "wins are printed as 0 and p_win is None — never 0.0, "
                       "which would read as a measured zero.")
        elif n < RC.PROVISIONAL_MIN_N:
            printed = (f"n = {n} < PROVISIONAL_MIN_N = 30. p_win and wins are "
                       f"PRINTED, NOT SUPPRESSED, with provisional=True; the "
                       f"rate may not be quoted as a rate.")
        elif w < 5:
            printed = (f"wins = {w} < 5. The ratio is defined; its interval is "
                       f"uninformative. p_win, wins and the interval all print, "
                       f"stamped WIDE — n_wins < 5.")
        else:
            printed = "REPORTABLE: n >= 30 and wins >= 5."
        rows.append({
            "basis": basis,
            "x": r4(float(x)),
            # F-KEY aliases: within ONE basis the threshold is a unique key, and
            # each basis publishes under its own name. Across bases it is NOT —
            # 0.50R and 0.50 ATR are different thresholds of different
            # quantities — which is why `basis="both"` must be keyed on
            # (basis, x) and never on a bare threshold column.
            "x_r": (r4(float(x)) if basis == "R" else None),
            "x_atr": (r4(float(x)) if basis == "ATR" else None),
            "x_units": "R (multiples of the campaign's own entry-stop distance)"
                       if basis == "R" else
                       "ATR(14) at the trigger bar",
            "n_at_or_beyond": n,
            "wins": w,
            "losses": n - w,
            "p_win": (r6(w / n) if n else None),
            "ci_lo": (r6(ci["lo"]) if ci["lo"] is not None else None),
            "ci_hi": (r6(ci["hi"]) if ci["hi"] is not None else None),
            "ci_stamp": CI_STAMP.replace("PAIRED per-campaign delta",
                                         "win indicator"),
            "provisional": bool(n < RC.PROVISIONAL_MIN_N),
            "sparse_numerator": bool(0 < n and w < 5),
            "reportable": bool(n >= RC.PROVISIONAL_MIN_N and w >= 5),
            "printed_instead": printed,
            "degenerate": degen,
            "approaching_the_identity": approaching,
            "n_at_or_beyond_is_a_shrinking_set": (
                "the conditioning set is NESTED and shrinks monotonically in x; "
                "cells at large x are SUBSETS of cells at small x and their "
                "p_win values are not independent observations."),
            "win_definition": "net_r > 0 — strictly NET R, after 10 bps round "
                              "trip and funding under the D12 ceiling. Not "
                              "gross, not 'reached +1R', not 'exited above "
                              "entry'.",
            "conditioning_variable": "mae_held_r (exit-bar clipped on a stop). "
                                     "NEVER mae_tape_r, which is contaminated "
                                     "by post-exit tape.",
            "window": WINDOW, "in_sample": True,
        })
    return rows


def hazard_curve(book: list, basis: str = "R") -> pd.DataFrame:
    """THE HAZARD CURVE — P(win | max adverse >= x), with n on every step.

    **P(win | max adverse >= x) = #{t : -mae_held_r(t) >= x AND net_r(t) > 0}
    / #{t : -mae_held_r(t) >= x}**, "win" being `net_r > 0` — the same
    definition `agg.win_rate_pct` uses, so this curve and the headline mean the
    same word.

    TWO BLOCKS, NOT TWO CURVES ON ONE AXIS.  `basis="R"` (THE DEFAULT, and what
    the commission asked for) runs x in 0.05R steps to 1.00R — 20 steps, keyed
    uniquely by `x_r`.  `basis="ATR"` runs the ATR-denominated twin, x in 0.10
    ATR steps to 2.00 ATR, conditioning on `-mae_held_r * r_over_atr`, keyed by
    `x_atr`.  `basis="both"` stacks them and MUST then be keyed on `(basis, x)`:
    they are separate blocks because `r_over_atr` varies 1.00-7.47 across this
    book, so one campaign's 0.5R is another's 3.7 ATR, 0.50R and 0.50 ATR are
    thresholds of DIFFERENT quantities, and a single bare threshold column
    across both would be a non-unique key on a table that looks joinable.

    **WHERE n GETS TOO SMALL, AND WHAT IS PRINTED THERE INSTEAD — three regimes,
    all on the row, none suppressed:**

    1. `n_at_or_beyond < PROVISIONAL_MIN_N = 30` -> `provisional = True`.  n and
       wins and p_win all still print; `printed_instead` says the rate may not
       be quoted as a rate.  On the panel curve this never fires (n bottoms out
       in the low hundreds) — the guard is kept because it fires the instant the
       curve is cut by asset or by year.
    2. `wins < 5` -> `sparse_numerator = True`.  The ratio is defined; the
       interval is not informative.  Everything prints, stamped WIDE, rather
       than being blanked — a blank cell is indistinguishable from a zero.
    3. **x = 1.00R IS DEGENERATE BY CONSTRUCTION.**  Under `mae_held_r`,
       reaching -1.00R held IS the initial un-advanced stop being taken, which
       IS the campaign ending at -1R.  So `p_win = 0` there is an IDENTITY, not
       a measurement, and the `degenerate` column says so in words on the row.
       Steps at x >= 0.95R are within a rounding tick of the same identity and
       carry `approaching_the_identity = True`.  The ATR block has no such
       identity, because the -1R stop maps to a DIFFERENT ATR distance on every
       campaign.

    WHAT WOULD MAKE THIS WRONG: conditioning on `mae_tape_r` (115 of 195
    campaigns show tape beyond -1.0R, to -4.589R, all of it post-exit); a
    conditioning set that is not nested (n or wins rising in x); printing the
    x = 1.00R cell as evidence; reading the bootstrap interval as a test — it is
    a diagnostic and is stamped as one; or publishing `basis="both"` under a
    single-column key.
    """
    if basis not in ("R", "ATR", "both"):
        raise SystemExit(f"HALT: unknown hazard basis {basis!r}")
    held = np.array([-campaign_mae(t)[0] for t in book], dtype=float)
    oa = np.array([_r_over_atr(t) for t in book], dtype=float)
    wins = np.array([bool(t.net_r > 0) for t in book])
    assets = np.array([t.symbol for t in book])
    rows: list[dict] = []
    if basis in ("R", "both"):
        rows += _hazard_block(book, "R", HAZARD_STEPS_R, held, wins, assets)
    if basis in ("ATR", "both"):
        rows += _hazard_block(book, "ATR", HAZARD_STEPS_ATR, held * oa, wins,
                              assets)
    df = pd.DataFrame(rows)
    df["f_key"] = ("x_r" if basis == "R" else
                   "x_atr" if basis == "ATR" else "(basis, x)")
    return df


# ═══════════════════════════════════ L-LIMIT-2 (a) · AE DECILES BY CONTEXT
def disp_bucket(t) -> str:
    """The displacement bucket, in MULTIPLES OF THE REGISTERED GATE.

    Edges are `RC.V5.D_DISPLACEMENT = 0.75`, 1.0, 1.5, 2.0, inf — pinned by the
    card's own gate, NOT by this book's quartiles.  A quartile cut would be a
    fitted quantity and would reopen F-C5-g on a second axis after this module
    spent its whole design closing it on the first.

    WHAT WOULD MAKE THIS WRONG: quartile edges; edges that do not start at the
    gate (a campaign below 0.75 cannot exist on the card lane, so a first bucket
    starting anywhere else would be reporting an empty region as if it were a
    measurement); or applying it to a lane where `disp_at_arming` is NaN (the
    spring and union lanes set it to NaN — this module rides the card lane).
    """
    d = float(t.disp_at_arming)
    if not np.isfinite(d):
        return "NO-DISPLACEMENT (non-card lane)"
    for lab, hi in zip(DISP_LABELS, DISP_EDGES[1:]):
        if d < hi:
            return lab
    return DISP_LABELS[-1]


def wall_context(t, champs: dict, tf: str = WALL_TF) -> dict:
    """The champion-wall context of ONE campaign, at its TRIGGER bar.

    `RC.wall_alignment(entry_px, stop_px, r_dist, wall_px, direction)` with
    `wall_px` read out of `T6.wall(symbol, champion_len)` at `t.entry_i`.  Four
    buckets: `beyond_stop` / `blocks_2r` / `both` / `neither`, plus `no_wall`.

    **THE PROFIT SIDE DECIDES WHICH CHAMPION.**  A long makes money upward, so
    the wall in its way is RESISTANCE; a short makes money downward, so its wall
    is SUPPORT.  `T6.profit_side` supplies it.  Scoring a short against the
    resistance champion would measure the floor it has already left.

    ── THREE LIVE TRAPS ON THIS PATH, ALL MEASURED, ALL PRINTED ──

    **(i) `no_wall` HERE MEANS "THE EMA WAS NOT YET WARM", NOT "NO WALL".**
    With ONE champion per side, a warm bar ALWAYS has a wall price, so the
    bucket is empty of market meaning and full of calendar.  `wall_series_12h`
    NaNs the EMA until `length` closed 12h bars exist: at length 889 that is
    2,667 4h bars — over a YEAR into each asset's panel.  Measured on the v6
    book: 29 `no_wall` campaigns, and ALL 29 are unwarm (28 resistance-side + 1
    support-side); ZERO are a genuine absence.  The row carries
    `wall_unwarm_share_pct` and the `no_wall_means` sentence so the bucket can
    never be read as a market state.

    **(ii) THE TWO SIDES HAVE DIFFERENT CHAMPION LENGTHS**, so the unwarm region
    is ASYMMETRIC BETWEEN LONGS AND SHORTS for a purely mechanical reason
    (resistance 889 vs support 316 on this league). A wall-bucket difference
    between directions is therefore partly a warm-up artifact and the row says
    so.

    **(iii) `both` IS DEGENERATE WITH ONE CHAMPION PER SIDE** — a single level
    cannot be beyond the stop AND between entry and +2R.  It is printed as a
    zero row rather than omitted, because a silently absent bucket looks like a
    bucket that was never possible.

    READ AT THE TRIGGER, NOT AT THE ARMING, AND NOT AT THE EXIT.  `entry_px`,
    `stop_px` and `r_dist` do not EXIST at the arming bar — the structural stop
    is chosen at the trigger — so "at the arming" is unbuildable for three of
    the four arguments.  The wall series is itself as-of the last CLOSED 12h
    bar, so nothing here reads a level the trigger bar had not seen.

    WHAT WOULD MAKE THIS WRONG: reading the wall at `exit_i` (it would be an
    outcome, not a context); using one side's champion for both directions;
    treating an unwarm NaN as a level; or folding `no_wall` into `neither`,
    which would bury a 29-campaign calendar artifact inside a market bucket.
    """
    side = profit_side(t.direction)
    L = champs.get((side, tf))
    if L is None:
        return {"wall_alignment": "no_wall", "wall_px": None,
                "champion_len": None, "champion_side": side, "warm": False,
                "reason": "no champion for this (side, tf)"}
    w = wall(t.symbol, int(L), tf)
    wp = float(w[0][t.entry_i])
    warm = bool(np.isfinite(wp))
    return {"wall_alignment": RC.wall_alignment(t.entry_px, t.stop_px, t.r_dist,
                                                wp, t.direction),
            "wall_px": (r6(wp) if warm else None),
            "champion_len": int(L), "champion_side": side, "warm": warm,
            "reason": "" if warm else "EMA not yet warm at the trigger bar"}


def _default_champs() -> dict:
    """`T6.champions` over BOTH league sides — the one construction, in one
    place, so `ae_by_context`, `selfcheck` and `build` cannot disagree about
    which champions were in force while each was claiming to describe the same
    book.  About 7 seconds; resolve it once and thread it.
    """
    _, hi_ms, _meta = corridor()
    lg = pd.concat([league(hi_ms, s) for s in T6.SIDES], ignore_index=True)
    return champions(lg)


def _ctx_row(axis: str, key: str, ts: list, book_n: int, extra: dict) -> dict:
    r = np.array([-campaign_mae(t)[0] for t in ts], dtype=float)
    oa = np.array([_r_over_atr(t) for t in ts], dtype=float)
    a = r * oa
    row = {"axis": axis, "context": axis, "key": key, "bucket": key,
           "f_key": "(context, bucket)", "n": len(ts),
           "share_of_book_pct": pct(len(ts), book_n),
           "provisional": bool(len(ts) < RC.PROVISIONAL_MIN_N),
           "mean_r_over_atr": r6(float(oa.mean())),
           "winners_n": int(sum(1 for t in ts if t.net_r > 0)),
           "win_rate_pct": pct(sum(1 for t in ts if t.net_r > 0), len(ts)),
           "expectancy_r": r4(float(np.mean([t.net_r for t in ts]))),
           "window": WINDOW, "in_sample": True,
           "population": AE_POPULATION_NOTE}
    row.update(_quantile_block(r, a))
    row.update(extra)
    return row


def ae_by_context(book: list, champs: dict | None = None,
                  tf: str = WALL_TF) -> pd.DataFrame:
    """L-LIMIT-2 (a) · AE DECILES BY CONTEXT — four margins, one cross, one
    refusal.

    AXES, each with a PRE-REGISTERED, NON-FITTED definition:
      `displacement`     multiples of the registered gate 0.75 (`disp_bucket`)
      `wall_alignment`   `RC.wall_alignment` off the league champion for the
                         campaign's PROFIT SIDE (`wall_context` — read its three
                         traps, they are live on this book)
      `asset`            the five panel assets
      `regime_year`      `iso(entry_ms)[:4]`

    **FOUR MARGINS WHOLE, PLUS ONE TWO-WAY, PLUS A REFUSAL THAT NAMES ITS
    ARITHMETIC.**  `{disp x wall x asset x year}` is 4 x 4 x 5 x 7 = 560 cells
    over 195 campaigns — median cell 0.  It is REFUSED, and the refusal is a ROW
    in the table with the arithmetic on it, not an omission a reader has to
    notice.  The one cross that is reported is `displacement x wall_alignment`
    (16 cells); almost all of them are provisional and every one says so.

    **R AND ATR DO NOT RANK THE BUCKETS THE SAME WAY, BY CONSTRUCTION.**
    `mean_r_over_atr` rises monotonically with displacement on this book, so the
    R-denominated and ATR-denominated deciles disagree about which displacement
    bucket is "deepest".  That disagreement is the whole reason both are asked
    for; both are printed side by side on every row.

    `champs` is `T6.champions(league)`, keyed `(side, tf) -> ema length`.  If
    None it is built here from BOTH league sides — about 7 seconds — and the
    lengths used are printed on the rows.

    WHAT WOULD MAKE THIS WRONG: cutting any axis at in-sample quantiles;
    printing the 4-way cross; reporting a bucket without `provisional` at
    n < 30; folding the unwarm-EMA campaigns into a market bucket; or reading a
    ranking off this table as a decision — it is descriptive and says so in the
    `selection_surface` column on every row.
    """
    if champs is None:
        champs = _default_champs()

    n = len(book)
    ctx = {id(t): wall_context(t, champs, tf) for t in book}
    dispb = {id(t): disp_bucket(t) for t in book}
    unwarm_total = sum(1 for t in book if not ctx[id(t)]["warm"])

    common = {
        "selection_surface": "NO — descriptive margins. Nothing is chosen, "
                             "ranked or promoted on this table.",
        "cross_refused": ("disp x wall x asset x year = 4 x 4 x 5 x 7 = 560 "
                          "cells over 195 campaigns; median cell 0. REFUSED, "
                          "not empty."),
        "both_axes_printed_because": ("mean_r_over_atr rises with displacement, "
                                      "so R-deciles and ATR-deciles do NOT rank "
                                      "the buckets the same way."),
        "no_wall_means": ("THE CHAMPION EMA WAS NOT YET WARM at the trigger bar "
                          "— a CALENDAR artifact, not an absent wall. With ONE "
                          "champion per side, a warm bar always has a wall. "
                          f"{unwarm_total} of {n} campaigns on this book are "
                          "unwarm and every one of them lands in no_wall."),
        "wall_both_bucket": ("'both' is DEGENERATE with one champion per side "
                             "(a single level cannot be beyond the stop AND "
                             "between entry and +2R). Printed as a zero row so "
                             "the bucket is never silently absent."),
        "champion_lengths": json.dumps(
            {f"{s}/{t_}": int(v) for (s, t_), v in sorted(champs.items())}),
        "wall_read_at": "the TRIGGER bar (entry_i). entry_px/stop_px/r_dist do "
                        "not exist at the arming bar; the wall series is itself "
                        "as-of the last CLOSED 12h bar.",
    }

    rows: list[dict] = []
    rows.append(_ctx_row("__PANEL__", "ALL", list(book), n, dict(
        common, wall_unwarm_share_pct=pct(unwarm_total, n))))

    for lab in DISP_LABELS:
        ts = [t for t in book if dispb[id(t)] == lab]
        if ts:
            rows.append(_ctx_row("displacement", lab, ts, n, dict(
                common,
                wall_unwarm_share_pct=pct(sum(1 for t in ts
                                              if not ctx[id(t)]["warm"]), len(ts)))))

    for lab in ("beyond_stop", "blocks_2r", "both", "neither", "no_wall"):
        ts = [t for t in book if ctx[id(t)]["wall_alignment"] == lab]
        if ts:
            rows.append(_ctx_row("wall_alignment", lab, ts, n, dict(
                common,
                wall_unwarm_share_pct=pct(sum(1 for t in ts
                                              if not ctx[id(t)]["warm"]), len(ts)))))
        else:
            rows.append({"axis": "wall_alignment", "context": "wall_alignment",
                         "key": lab, "bucket": lab,
                         "f_key": "(context, bucket)", "n": 0,
                         "share_of_book_pct": 0.0, "provisional": True,
                         "window": WINDOW, "in_sample": True,
                         "population": AE_POPULATION_NOTE,
                         "empty_bucket_printed_on_purpose":
                             "0 campaigns. Printed rather than omitted — an "
                             "absent row and an empty bucket look identical.",
                         **common})

    for s in sorted({t.symbol for t in book}):
        ts = [t for t in book if t.symbol == s]
        rows.append(_ctx_row("asset", s, ts, n, dict(
            common,
            wall_unwarm_share_pct=pct(sum(1 for t in ts
                                          if not ctx[id(t)]["warm"]), len(ts)))))

    for y in sorted({_regime_year(t) for t in book}):
        ts = [t for t in book if _regime_year(t) == y]
        rows.append(_ctx_row("regime_year", y, ts, n, dict(
            common,
            wall_unwarm_share_pct=pct(sum(1 for t in ts
                                          if not ctx[id(t)]["warm"]), len(ts)))))

    for lab in DISP_LABELS:
        for wl in ("beyond_stop", "blocks_2r", "both", "neither", "no_wall"):
            ts = [t for t in book if dispb[id(t)] == lab
                  and ctx[id(t)]["wall_alignment"] == wl]
            if not ts:
                rows.append({"axis": "displacement x wall_alignment",
                             "context": "displacement x wall_alignment",
                             "key": f"{lab} | {wl}", "bucket": f"{lab} | {wl}",
                             "f_key": "(context, bucket)", "n": 0,
                             "share_of_book_pct": 0.0, "provisional": True,
                             "window": WINDOW, "in_sample": True,
                             "population": AE_POPULATION_NOTE,
                             "empty_bucket_printed_on_purpose":
                                 "0 campaigns. The cross is printed WHOLE.",
                             **common})
                continue
            rows.append(_ctx_row("displacement x wall_alignment",
                                 f"{lab} | {wl}", ts, n, dict(
                                     common,
                                     wall_unwarm_share_pct=pct(
                                         sum(1 for t in ts
                                             if not ctx[id(t)]["warm"]), len(ts)))))

    rows.append({"axis": "REFUSAL", "context": "REFUSAL",
                 "key": "disp x wall x asset x regime_year",
                 "bucket": "disp x wall x asset x regime_year",
                 "f_key": "(context, bucket)",
                 "n": 0, "share_of_book_pct": 0.0, "provisional": True,
                 "window": WINDOW, "in_sample": True,
                 "population": AE_POPULATION_NOTE,
                 "refusal": ("4 x 4 x 5 x 7 = 560 cells over 195 campaigns; "
                             "median cell 0. REFUSED, NOT EMPTY. The commission's "
                             "slash is read as margins plus ONE two-way cross."),
                 **common})
    return pd.DataFrame(rows)


# ═══════════════════════════════════════════ L-LIMIT-2 (b) · THE FRONTIER
def limit_px(t, k: float) -> float:
    """The resting limit price: `entry_px - direction * k * atr_at_entry`.

    k IS AN ABSOLUTE ATR MULTIPLE.  Not a multiple of avg-AE, not a multiple of
    r_dist.  This one line is what cures F-C5-g: `atr_at_entry` is the ATR(14)
    the card read AT ITS OWN TRIGGER BAR, before any outcome existed, so no
    function of the outcome variable enters the fill rule.

    WHAT WOULD MAKE THIS WRONG: scaling by `r_dist` (the offset would then be an
    R-multiple and the ATR sweet spot the operator asked for would be
    unmeasurable); scaling by any statistic of the book; or using an ATR read
    anywhere other than the trigger bar. GEOMETRY, PROVEN NOT ASSUMED: the rail
    is MIN_STOP_ATR = 1.0 and this book's min `r_over_atr` is 1.0, while
    k <= 0.50, so `lim` is STRICTLY between entry and the initial stop on every
    campaign at every k (F-C6-LIM-1, checked in `selfcheck`).
    """
    return float(t.entry_px - t.direction * float(k) * float(t.atr_at_entry))


def _fill_bar(t, lim: float) -> int | None:
    """First bar AFTER the trigger, up to the CARD'S OWN exit inclusive, whose
    adverse extreme reaches `lim`.

    The scan window is Tier-C5's, unchanged, so the two arms' fill sets are the
    same object and a miss rate stays a miss rate: the arm never changes which
    campaigns exist, so a level that never fills books a MISS rather than
    freeing the slot for someone else.

    INTRA-BAR ORDER IS ADVERSE-FIRST AND DISTANCE-ORDERED.  `lim` is strictly
    nearer the entry than the market stop, so on a bar that reaches both, the
    limit fills FIRST and the market half stops after. Including `exit_i` in the
    scan is what enacts that; excluding it would lose exactly the fills the
    campaign's last bar granted.

    WHAT WOULD MAKE THIS WRONG: starting at `ti` (a close entry has no tradeable
    remainder on its own bar); stopping at `exit_i - 1` (the arm would lose the
    fill on the bar the card exited); or running past `exit_i` (the arm would be
    offered a campaign the card no longer occupies).
    """
    f, d = frame(t.symbol)["f"], t.direction
    for j in range(t.entry_i + 1, t.exit_i + 1):
        if (d == 1 and f.l[j] <= lim) or (d == -1 and f.h[j] >= lim):
            return j
    return None


def _fill_px(t, lim: float, fill_i: int) -> float:
    """THE GAP-THROUGH FIX.  A resting limit fills at the OPEN when the market
    gaps past it — never at `lim`.

    Tier-C5's `limit_grid` booked every fill AT `lim` even when the bar opened
    beyond it, which is an optimistic fill worth real R on a gap.  Fixed here,
    in the new probe only, which is why this frontier's fills are slightly WORSE
    than a naive re-run of `limit_grid` at ATR offsets: the two must not be
    compared as if they were the same measurement.

    WHAT WOULD MAKE THIS WRONG: booking any long fill better than
    `min(lim, open)` or any short fill better than `max(lim, open)`; or applying
    the fix without also moving the stop, which is 1R beyond THE FILL and not 1R
    beyond `lim` — a gapped fill must carry its own stop or the campaign's risk
    silently exceeds 1R.
    """
    f, d = frame(t.symbol)["f"], t.direction
    o = float(f.o[fill_i])
    return min(lim, o) if d == 1 else max(lim, o)


def ride_limit_half(t, k: float, hi_i: int, card) -> dict | None:
    """The LIMIT leg at UNIT size.  `None` on a MISS.

    The stop is 1R beyond THE FILL, so a gapped fill carries its own stop and
    the leg's worst case is exactly 1R of the campaign's own R.
    `test_stop_on_entry_bar=True` is inherited and REQUIRED: a limit fills
    mid-bar and the remainder of that bar is real tradeable time — discarding it
    silently gave every Tier-C5 S-LIMIT cell a free bar of immunity.

    THAT FLAG IS PESSIMISTIC BY DESIGN AND IT SUPPRESSES AE.  It reads the WHOLE
    fill bar's adverse extreme, including the part that ran before the limit
    filled, because 4h OHLC cannot resolve intra-bar order and the estate's F-4
    convention resolves the unknowable adversely.  When it fires the ride
    returns `mae_to_1r = None`, so limit-arm campaigns killed on their fill bar
    contribute NOTHING to any AE statistic — which is why L-AE reports AE on the
    CARD's book only and never on an arm's.

    THE CARD IS THREADED THROUGH, NOT DEFAULTED.  The leg must ride the SAME
    knobs the book was produced with (trail arming, minimum advance, harvest
    fraction, funding ceiling); a leg riding v6 defaults against a v5-control
    book would differ from its own base in two things at once and the frontier
    would be measuring both.

    WHAT WOULD MAKE THIS WRONG: `test_stop_on_entry_bar=False` (a free bar of
    immunity at every k); `hi_i` taken as the ASSET's last bar rather than the
    CORRIDOR's (Tier-C5 did the latter — latent today because all five assets
    end on the same bar, wrong the moment one cache is staler); or a stop placed
    1R beyond `lim` rather than 1R beyond the fill.
    """
    lim = limit_px(t, k)
    j = _fill_bar(t, lim)
    if j is None:
        return None
    px = _fill_px(t, lim, j)
    stop = px - t.direction * t.r_dist
    c = dataclasses.replace(card, name=f"L-LIMIT-2 k={k}", grid="P-LIM-2")
    ride = _ride(t.symbol, c, t.direction, j, px, stop, t.r_dist, hi_i,
                 test_stop_on_entry_bar=True)
    acc = _account(t.symbol, c, t.direction, j, px, t.r_dist, ride)
    return {"fill_i": j, "fill_px": px, "stop_px": stop, "lim": lim,
            "gapped": bool(abs(px - lim) > 1e-12),
            "fill_bar_stop": bool(ride["exit_i"] == j
                                  and ride["exit_reason"] == "stop"),
            "improvement_r": float((t.entry_px - px) * t.direction / t.r_dist),
            "ride": ride, "acc": acc}


def book_split(t, half: dict | None, card=None) -> dict:
    """SPLIT-ENTRY: half at the market trigger, half on the limit.
    **TWO STOPS, ONE R.**

    THE MARKET HALF *IS* THE CARD.  `t.stop_px == entry_px - d*r_dist` to 0.0 on
    this book, so "1R beyond the market fill" is the card's own structural
    anchor, unchanged — which is why the split arm differs from the card in
    exactly one thing, the extra half, and a frontier is supposed to isolate
    exactly one thing.  No re-ride is needed: the market half's gross, fee and
    uncapped funding are already on the `Trade`.

    THE ALGEBRA, AND WHY IT IS EXACT.  `_account` is LINEAR IN SIZE for gross,
    fee and UNCAPPED funding, so at half size each leg is exactly half of its
    own unit-size accounting:

        net_r_split = 0.5*(gross_card - fee_card)
                    + 0.5*(gross_lim  - fee_lim )      # zero if the limit missed
                    - min(0.5*fund_card_uncapped + 0.5*fund_lim_uncapped, D12)

    **THE D12 CEILING IS APPLIED ONCE, AT THE CAMPAIGN LEVEL, TO THE SUMMED
    UNCAPPED FUNDING.**  Capping each half at 1R would enact a 2R campaign
    ceiling; capping an already-capped half would enact 0.5R.  Both are wrong
    and both are silent.  It is inert at unit size on this book (0 of 195 bind)
    and live the moment size moves — the same defect `size_grid` names for
    S-SIZE.

    A MISS ON THIS ARM IS NOT A FLAT BOOK.  The market half was taken, so a miss
    books HALF A CARD — not 0.0, and not the card.  `_ride` runs the card's band
    harvest on each leg, so a filled split campaign is FOUR QUARTERS (25%+25%
    harvested, 25%+25% runner) and the two legs ratchet off the same fractal
    confirmations from different starting stops.

    **THE CEILING COMES FROM THE CARD, NOT FROM A GLOBAL.**  `card` is the same
    object `ride_limit_half` rode the limit leg with.  Reading
    `RC.FUNDING_CEILING_R` here instead would let a caller turn the ceiling off
    on the legs and still have it re-applied at the campaign level — the arm
    would then differ from its own base in a knob the caller explicitly set, and
    it would do so silently, because `RC.FUNDING_CEILING_R` and
    `CARD_V6.funding_ceiling_r` are both 1.0 on this book and the divergence is
    invisible until someone rides a control card.  `card=None` falls back to the
    module constant so the signature stays compatible.

    WHAT WOULD MAKE THIS WRONG: computing `fund_eff` from either leg's already
    capped `funding_r`; taking the ceiling from `RC` while the legs took theirs
    from `card`; booking a miss at 0.0; deriving R from the fill rather
    than from the campaign (R must stay one denominator or the book stops
    summing); or applying the fill-bar stop test to the MARKET half — a close
    entry has no tradeable remainder and the asymmetry between the two legs is
    required, not an oversight.
    """
    gm, fm, um = float(t.gross_r), float(t.fee_r), float(t.funding_r_uncapped)
    if half is None:
        gl = fl = ul = 0.0
    else:
        a = half["acc"]
        gl, fl, ul = (float(a["gross_r"]), float(a["fee_r"]),
                      float(a["funding_r_uncapped"]))
    fund_raw = 0.5 * um + 0.5 * ul
    cap = RC.FUNDING_CEILING_R if card is None else card.funding_ceiling_r
    bound = bool(cap is not None and fund_raw > cap)
    fund_eff = cap if bound else fund_raw
    return {"net_r": 0.5 * (gm - fm) + 0.5 * (gl - fl) - fund_eff,
            "gross_r": 0.5 * (gm + gl), "fee_r": 0.5 * (fm + fl),
            "funding_r": fund_eff, "funding_ceiling_bound": bound,
            "market_half_r": 0.5 * (gm - fm), "limit_half_r": 0.5 * (gl - fl),
            "limit_filled": half is not None}


@dataclass(frozen=True)
class ArmRow:
    """One campaign as an ARM saw it — the minimum surface `agg` and `d15` read.

    It carries the keys they need and NOTHING ELSE, deliberately: an object that
    looked like a `Trade` would eventually be passed to something that expects a
    `Trade`, and the arm's `net_r` is not a campaign the card ever took.

    WHAT WOULD MAKE THIS WRONG: giving it a `mae_to_1r_r` or a `reached_1r`
    (the fill-bar stop test suppresses AE on the arm, so any AE read off an arm
    is systematically shallow); or keying it on anything but
    `(symbol, entry_ms)`, which is the estate's declared F-KEY and what `d15`
    pairs on.
    """
    symbol: str
    entry_ms: int
    exit_ms: int
    net_r: float
    gross_r: float
    fee_r: float
    funding_r: float
    filled: bool


def _overlap(book: list, rides: dict) -> tuple[int, int, int, int]:
    """How often the arm's limit leg is still open when the CARD's next campaign
    on that asset enters — MEASURED AND PRINTED, never repaired.

    The fill scan is capped at the card's exit but the RIDE is not, so a filled
    limit leg can outlive the campaign it was offered inside and the arm's book
    can hold two positions per asset while the card holds one.  Dropping the
    overlaps would change the offered set, and a miss rate over a population
    that moved is not a miss rate — so the violation goes on the table's face
    instead of into the arithmetic.

    A ZERO HERE IS ONLY MEANINGFUL BESIDE `outlived`.  `overlapping_campaigns_n
    = 0` could mean "the leak never fires" or "the measurement is dead", and
    those look identical on a table.  So the second pair — how often the limit
    leg outlives the CARD's own exit at all, and by how many bars at most — is
    returned with it.  On this book the leg outlives the card on 25 to 64
    campaigns depending on k, by up to 64 bars, and STILL never collides with
    the card's next entry: the measurement is live and the violation is absent.

    WHAT WOULD MAKE THIS WRONG: silently dropping overlapping campaigns;
    counting overlap against the ARM's own next campaign rather than the CARD's
    (the arm has no occupancy rule of its own); reporting bars without
    campaigns, which hides whether it is one long tail or many short ones; or
    publishing the zero without `outlived`, which is a check satisfied by no
    examples wearing the face of a passed one.
    """
    n = bars = outlived = max_extra = 0
    by_asset: dict[str, list] = {}
    for t in book:
        by_asset.setdefault(t.symbol, []).append(t)
        h = rides.get((t.symbol, t.entry_ms))
        if h is not None:
            extra = int(h["ride"]["exit_i"]) - t.exit_i
            if extra > 0:
                outlived += 1
                max_extra = max(max_extra, extra)
    for sym, ts in by_asset.items():
        ts = sorted(ts, key=lambda x: x.entry_i)
        for a, b in zip(ts, ts[1:]):
            h = rides.get((a.symbol, a.entry_ms))
            if h is None:
                continue
            xi = int(h["ride"]["exit_i"])
            if xi >= b.entry_i:
                n += 1
                bars += xi - b.entry_i + 1
    return n, bars, outlived, max_extra


def frontier(book: list, lo_ms: int, hi_ms: int,
             ks: tuple[float, ...] = K_GRID, card=None,
             prereg_path: str | Path | None = None) -> pd.DataFrame:
    """**THE LIMIT FRONTIER** — offsets k x ATR(14), TWO ARMS per k, reported
    WHOLE.  10 cells built, 10 cells printed, nothing dropped and NO k PROMOTED.

    ARMS
      `FULL-LIMIT`   the whole position rests at `entry_px - d*k*ATR`; a miss is
                     NO POSITION and books 0.0.
      `SPLIT-ENTRY`  half at the market trigger, half on the limit; TWO STOPS,
                     ONE R (see `book_split`); a miss books HALF A CARD.

    E[R] IS DENOMINATED IN THE OFFERED SET — all 195 campaigns the card took,
    misses at their true value.  `expectancy_r_filled_only` is printed BESIDE it
    (that is Tier-C5's shape) because the two rank the k grid differently, and a
    per-fill expectancy is not a quantity anyone can spend.  The pre-registered
    form names the offered one, before the table exists.

    THE D15 TRIO RIDES EVERY ROW AND GATES NOTHING.  `d15` is called with the
    misses PRESENT in the cell — at 0.0 for FULL-LIMIT and half a card for
    SPLIT-ENTRY — so `n_paired == len(book)` on every row.  Calling it on the
    filled-only list would push every miss into `unpaired_base_n` and report a
    delta that ignores the arm's single largest effect: not being in the trade.

    WHAT WOULD MAKE THIS WRONG: dropping a cell (the grid is reported whole);
    promoting a k (`k_promoted` says NO on every row and the argmax is stamped
    as the FORM's output, not a decision); calling `d15` on the filled subset;
    `provisional` computed on 195 rather than on `filled`; riding a `card` whose
    knobs differ from the ones that produced `book` (the arm would then differ
    from its own base in two things at once); `hi_i` taken per asset rather than
    per corridor; or letting the declared m and the constructed m disagree —
    this function HALTs on that, because a selection surface the code derived
    from itself is not a declaration.
    """
    if not book:
        raise SystemExit("HALT: the frontier was handed an empty book.")
    if card is None:
        card = RC.CARD_V6
    lanes = {t.lane for t in book}
    if lanes != {"card"}:
        raise SystemExit(f"HALT: the frontier rides the card lane; got {lanes}")
    built = len(ks) * len(FRONTIER_ARMS)
    if built != LIM2_M:
        raise SystemExit(
            f"HALT: the declared selection surface and the constructed one "
            f"disagree. LIM2_M={LIM2_M}, built={built}. A declared m that the "
            f"code can silently outgrow is not a declaration.")

    prereg_on_disk = ""
    if prereg_path is not None:
        p = Path(prereg_path)
        if not p.exists():
            raise SystemExit(f"HALT: no pre-registration at {p}. Call "
                             f"write_prereg() BEFORE the frontier.")
        stamp = json.loads(p.read_text())
        if stamp.get("sha256") != prereg_sha256():
            raise SystemExit(
                "HALT: the pre-registration on disk does not match the module "
                "constant. Either the text moved after the look, or the file "
                "belongs to another run.")
        prereg_on_disk = (f"{p} · sha256={stamp['sha256'][:16]} · written "
                          f"{stamp.get('written_at')} · BEFORE this table")
    else:
        prereg_on_disk = ("NOT WRITTEN TO DISK BY THIS CALL. The text is a "
                          "module constant defined above every function that "
                          "can compute a result; pass prereg_path= to make the "
                          "ordering claim checkable by mtime.")

    hi_i = {s: _idx_range(frame(s)["f"].open_ms, lo_ms, hi_ms)[1]
            for s in {t.symbol for t in book}}
    n_off = len(book)
    sha = prereg_sha256()
    rows: list[dict] = []

    for k in ks:
        halves = {}
        for t in book:
            h = ride_limit_half(t, float(k), hi_i[t.symbol], card)
            if h is not None:
                halves[(t.symbol, t.entry_ms)] = h
        filled_keys = set(halves)
        n_fill = len(filled_keys)
        n_miss = n_off - n_fill
        ov_n, ov_bars, outlived, max_extra = _overlap(book, halves)
        gapped = sum(1 for h in halves.values() if h["gapped"])
        fbstop = sum(1 for h in halves.values() if h["fill_bar_stop"])
        impr = [h["improvement_r"] for h in halves.values()]
        margin = [float((frame(t.symbol)["f"].o[halves[(t.symbol, t.entry_ms)]["fill_i"]]
                         - halves[(t.symbol, t.entry_ms)]["lim"]) * t.direction
                        / t.atr_at_entry)
                  for t in book if (t.symbol, t.entry_ms) in halves]

        missed = [t for t in book if (t.symbol, t.entry_ms) not in filled_keys]
        got = [t for t in book if (t.symbol, t.entry_ms) in filled_keys]

        for arm in FRONTIER_ARMS:
            cell: list[ArmRow] = []
            for t in book:
                key = (t.symbol, t.entry_ms)
                h = halves.get(key)
                if arm == "FULL-LIMIT":
                    if h is None:
                        cell.append(ArmRow(t.symbol, t.entry_ms, t.exit_ms,
                                           0.0, 0.0, 0.0, 0.0, False))
                    else:
                        a = h["acc"]
                        xm = int(frame(t.symbol)["f"]
                                 .open_ms[h["ride"]["exit_i"]])
                        cell.append(ArmRow(t.symbol, t.entry_ms, xm,
                                           float(a["net_r"]), float(a["gross_r"]),
                                           float(a["fee_r"]), float(a["funding_r"]),
                                           True))
                else:
                    sp = book_split(t, h, card)
                    xm = t.exit_ms if h is None else max(
                        t.exit_ms,
                        int(frame(t.symbol)["f"].open_ms[h["ride"]["exit_i"]]))
                    cell.append(ArmRow(t.symbol, t.entry_ms, xm,
                                       float(sp["net_r"]), float(sp["gross_r"]),
                                       float(sp["fee_r"]), float(sp["funding_r"]),
                                       h is not None))

            a_off = agg(cell, f"P-LIM-2 {arm}", f"k={k}")
            fil = [c for c in cell if c.filled]
            dd = _maxdd_r([(c.exit_ms, c.symbol, c.net_r) for c in cell])
            deltas = np.array([c.net_r for c in cell]) - np.array(
                [t.net_r for t in book])
            draws = cluster_boot(deltas, np.array([c.symbol for c in cell]),
                                 seed=SEED, n_boot=4000)
            ci = _ci_from(draws, float(deltas.mean()))
            fac = 1.0 if arm == "FULL-LIMIT" else 0.5

            row = {
                "arm": arm, "k_x_atr": float(k), "k_atr": float(k),
                "f_key": "(k_atr, arm)",
                "offset_basis": OFFSET_BASIS,
                "card_name": card.name,
                "campaigns_offered": n_off, "filled": n_fill, "missed": n_miss,
                "fill_pct": pct(n_fill, n_off), "miss_pct": pct(n_miss, n_off),
                # ── E[R], on the OFFERED set (the form's argument) ───────────
                "net_r": a_off["net_r"], "expectancy_r": a_off["expectancy_r"],
                "win_rate_pct": a_off["win_rate_pct"],
                "max_dd_r": r4(dd), "best_r": a_off["best_r"],
                "strip_best_net_r": a_off["strip_best_net_r"],
                "top_decile_share_pct": a_off["top_decile_share_pct"],
                "gross_r": a_off["gross_r"], "fee_r": a_off["fee_r"],
                "funding_r": a_off["funding_r"],
                "expectancy_denominator": "OFFERED SET — every campaign the "
                                          "card took, misses at their true "
                                          "value. This is the form's argument.",
                # ── E[R] the Tier-C5 way, printed beside it ──────────────────
                "net_r_filled_only": r4(sum(c.net_r for c in fil)) if fil else None,
                "expectancy_r_filled_only": (r4(float(np.mean([c.net_r
                                                               for c in fil])))
                                             if fil else None),
                "win_rate_pct_filled_only": pct(sum(1 for c in fil
                                                    if c.net_r > 0), len(fil)),
                # ── the counterfactual ──────────────────────────────────────
                "missed_would_have_net_r": (r4(fac * sum(t.net_r for t in missed))
                                            if missed else None),
                "missed_would_have_expectancy_r": (
                    r4(fac * float(np.mean([t.net_r for t in missed])))
                    if missed else None),
                "missed_would_have_win_rate_pct": pct(
                    sum(1 for t in missed if t.net_r > 0), len(missed)),
                "missed_would_have_best_r": (r4(fac * max(t.net_r for t in missed))
                                             if missed else None),
                "filled_would_have_expectancy_r": (
                    r4(float(np.mean([t.net_r for t in got]))) if got else None),
                "miss_semantics": MISS_SEMANTICS[arm],
                "card_expectancy_r": r4(float(np.mean([t.net_r for t in book]))),
                # ── the D15 trio + context ──────────────────────────────────
                **d15(cell, book),
                "d15_disposition": D15_DISPOSITION,
                # ── the interval, stamped ───────────────────────────────────
                "ci_lo": (r6(ci["lo"]) if ci["lo"] is not None else None),
                "ci_hi": (r6(ci["hi"]) if ci["hi"] is not None else None),
                "ci_p_one_sided": (r6(ci["p_one_sided"])
                                   if ci["p_one_sided"] is not None else None),
                "ci_stamp": CI_STAMP,
                # ── the mechanics, on the face ──────────────────────────────
                "gap_through_fills_n": gapped,
                "min_open_minus_lim_atr": (r6(float(np.min(margin)))
                                           if margin else None),
                "gap_through_note": (
                    "fills booked at the bar OPEN because the market gapped "
                    "past the limit. Tier-C5 booked ALL fills at the limit, "
                    "which is optimistic on a gap. MEASURED ON THIS BOOK: "
                    f"{gapped} of {n_fill} fills gapped through — the closest "
                    "any fill bar came to opening past its limit is "
                    f"{r6(float(np.min(margin))) if margin else None} ATR. THE "
                    "FIX IS THEREFORE LATENT INSURANCE HERE, NOT A LIVE "
                    "CORRECTION, and this frontier's fill PRICES coincide with "
                    "a naive re-run's. Said plainly so the repair is not "
                    "credited with a difference it did not make."),
                "fill_bar_stopped_n": fbstop,
                "fill_bar_stop_note": ("limit legs killed on their own fill bar "
                                       "by the inherited whole-bar stop test. "
                                       "Pessimistic by design (F-4); it also "
                                       "returns mae_to_1r=None, which is why "
                                       "no AE is reported on an arm."),
                "mean_entry_improvement_r": (r6(float(np.mean(impr)))
                                             if impr else None),
                "overlapping_campaigns_n": ov_n, "overlapping_bars": ov_bars,
                "arm_outlived_card_n": outlived,
                "arm_max_extra_bars": max_extra,
                "overlap_note": (
                    "the limit leg's RIDE is not capped at the card's exit, so "
                    "it can still be open when the card's next campaign on that "
                    "asset enters. MEASURED AND PRINTED, not repaired — dropping "
                    "overlaps would move the offered set, and a miss rate over a "
                    "population that moved is not a miss rate. THE ZERO IS "
                    "MEANINGFUL ONLY BESIDE arm_outlived_card_n: the leg "
                    f"outlives the card on {outlived} campaigns by up to "
                    f"{max_extra} bars and still never collides with the card's "
                    "next entry, so the measurement is live and the violation is "
                    "absent — not the other way round."),
                "provisional": bool(n_fill < RC.PROVISIONAL_MIN_N),
                "provisional_basis": "computed on `filled`, not on the 195 "
                                     "offered.",
                # ── the pre-registration, inseparable from the numbers ──────
                "k_promoted": K_PROMOTED,
                "preregistration": LIM2_PREREG["the_form"],
                "instrument": LIM2_PREREG["the_instrument"],
                "falsification": LIM2_PREREG["what_would_falsify_the_form"],
                "residual_in_sample_fitting":
                    LIM2_PREREG["the_residual_in_sample_fitting"],
                "selection_surface": SELECTION_SURFACE,
                "m_cells_on_the_frontier": LIM2_M,
                "prereg_sha256": sha,
                "prereg_on_disk": prereg_on_disk,
                "window": WINDOW, "in_sample": True,
                "aggregation": "raw_panel",
            }
            rows.append(row)

    df = pd.DataFrame(rows)
    # THE FORM'S OUTPUT — an argmax, stamped as a form and NOT as a promotion.
    df["k_is_argmax_of_this_arm"] = False
    kstar: dict[str, float] = {}
    for arm in FRONTIER_ARMS:
        m = df["arm"] == arm
        sub = df[m].sort_values(["expectancy_r", "k_x_atr"],
                                ascending=[False, True])
        if len(sub):
            df.loc[sub.index[0], "k_is_argmax_of_this_arm"] = True
            kstar[arm] = float(df.loc[sub.index[0], "k_x_atr"])
    df["argmax_is_the_form_not_a_decision"] = (
        "k*(A) is the OUTPUT OF A PRE-REGISTERED FORM, computed after the text "
        "was fixed. IT IS NOT A PROMOTION. It is the value H-LIM-2 is to be "
        "tested at on an out-of-sample instrument that this estate has not yet "
        "named. Ties break to the SMALLER k.")
    df["k_star_of_this_arm"] = df["arm"].map(kstar)
    return _evaluate_falsification(df, ks, kstar)


def _evaluate_falsification(df: pd.DataFrame, ks: tuple[float, ...],
                            kstar: dict[str, float]) -> pd.DataFrame:
    """RUN THE PRE-REGISTERED FALSIFICATION CLAUSES AGAINST THE TABLE THAT WAS
    JUST BUILT, and put the verdict on every row.

    A falsification clause written before the look and never evaluated is
    decoration.  All three of `LIM2_PREREG["what_would_falsify_the_form"]` are
    tested here, and each row says which fired.

      (a) `expectancy_r` non-monotonic in k with NO interior maximum on EITHER
          arm — the frontier would be noise and the argmax would be picking the
          biggest of ten draws.  Fires when an arm's argmax sits on a grid
          ENDPOINT.
      (b) k* differing between the two arms by more than one grid step.
          **THIS CLAUSE IS VACUOUS BY CONSTRUCTION AND THE TABLE SAYS SO** —
          see `split_is_a_convex_combination`.
      (c) a k* whose `max_single_trade_delta_share >= 1.0` — F-C5-f's defect:
          the number is real and the mechanism is one trade.

    **CLAUSE (b) CANNOT FIRE, AND THAT IS A DEFECT IN THE PRE-REGISTRATION, NOT
    IN THE DATA.**  Under resolution (A) — two stops, one R — with the D12
    ceiling inert, the split arm is EXACTLY the 50/50 convex combination of the
    card and the full-limit arm:
    `net_r_split = 0.5*net_r_card + 0.5*net_r_limit` per campaign, hence
    `expectancy_split(k) = 0.5*(expectancy_card + expectancy_full(k))` with
    `expectancy_card` CONSTANT IN k.  An affine, increasing transform of the
    quantity being maximised cannot move an argmax, so `k*(SPLIT) == k*(FULL)`
    ALWAYS, and the paired delta of the split arm is exactly half the full
    arm's, campaign by campaign.  The two arms therefore carry the same
    bootstrap interval shape, the same `max_single_trade_delta_share`, and the
    same k*.  The SPLIT arm is a real book with a real risk profile — it is not
    a second independent search.  **THE EFFECTIVE SELECTION SURFACE FOR THE
    ARGMAX IS 5 CELLS, NOT 10.**  The declared m stays 10 because it was
    declared before the look and a declaration is not revised by its own
    result; the observation is printed beside it.

    WHAT WOULD MAKE THIS WRONG: reporting a verdict without naming which clause
    fired; treating clause (b)'s silence as evidence of agreement between the
    arms (it is an identity, not a measurement); or evaluating the clauses
    against a table other than the one the form named.
    """
    fired_a: dict[str, bool] = {}
    for arm in FRONTIER_ARMS:
        sub = df[df["arm"] == arm].sort_values("k_x_atr")
        e = list(sub["expectancy_r"])
        j = int(np.argmax(e))
        fired_a[arm] = bool(j in (0, len(e) - 1))
    step = (max(ks) - min(ks)) / (len(ks) - 1) if len(ks) > 1 else 1.0
    fired_b = bool(len(kstar) == 2
                   and abs(kstar[FRONTIER_ARMS[0]] - kstar[FRONTIER_ARMS[1]])
                   > step + 1e-12)
    fired_c: dict[str, bool] = {}
    kstar_share: dict[str, float] = {}
    for arm in FRONTIER_ARMS:
        row = df[(df["arm"] == arm) & df["k_is_argmax_of_this_arm"]]
        if len(row) != 1:
            raise SystemExit(
                f"HALT: arm {arm!r} carries {len(row)} argmax rows, not exactly "
                f"1. Clause (c) is read OFF the k* row; with no k* row the old "
                f"default was 0.0, i.e. a falsification clause reporting NOT "
                f"FIRED because it could not be evaluated.")
        v = float(row["max_single_trade_delta_share"].iloc[0])
        kstar_share[arm] = v
        fired_c[arm] = bool(v >= 1.0)

    df = df.copy()
    df["falsify_a_argmax_on_an_endpoint"] = df["arm"].map(fired_a)
    df["falsify_b_arms_disagree_on_k_star"] = fired_b
    df["falsify_b_is_vacuous"] = True
    df["falsify_c_k_star_is_one_trade"] = df["arm"].map(fired_c)
    # THE VALUE THAT FIRED CLAUSE (c) IS THE k* ROW'S, NOT THE ROW BEING
    # RENDERED.  It is carried as its own column so the verdict quotes the
    # number the clause was evaluated on. Rendering `r[...]` row-wise instead
    # printed each row's own share under the label "k*'s", which is wrong on
    # every non-argmax row and can print the self-refuting sentence
    # "k*'s max_single_trade_delta_share = 0.83 >= 1.0".
    df["k_star_max_single_trade_delta_share"] = df["arm"].map(kstar_share)
    df["split_is_a_convex_combination"] = (
        "net_r_split = 0.5*net_r_card + 0.5*net_r_limit EXACTLY (D12 inert), so "
        "expectancy_split(k) is an affine increasing transform of "
        "expectancy_full(k) and k*(SPLIT) == k*(FULL) BY CONSTRUCTION. The "
        "split arm is a different RISK PROFILE, not a second independent "
        "search. EFFECTIVE SELECTION SURFACE FOR THE ARGMAX = 5 CELLS, NOT 10; "
        "the declared m stays 10 because it was declared before the look.")

    def verdict(r) -> str:
        f = []
        if r["falsify_a_argmax_on_an_endpoint"]:
            f.append("(a) the argmax sits on a grid ENDPOINT — the interior "
                     "maximum the form assumed does not exist")
        if r["falsify_b_arms_disagree_on_k_star"]:
            f.append("(b) the arms disagree on k* by more than one grid step")
        if r["falsify_c_k_star_is_one_trade"]:
            f.append(f"(c) k* = {r['k_star_of_this_arm']}: ITS "
                     f"max_single_trade_delta_share = "
                     f"{r['k_star_max_single_trade_delta_share']} >= 1.0 — THE "
                     f"NUMBER IS REAL AND THE MECHANISM IS ONE TRADE (this row "
                     f"is k = {r['k_x_atr']}, whose own share is "
                     f"{r['max_single_trade_delta_share']})")
        if not f:
            return ("NOT FALSIFIED in-sample. That is NOT support: the claim "
                    "H-LIM-2 is an OUT-OF-SAMPLE claim and this estate has not "
                    "named the instrument.")
        return ("FALSIFIED IN-SAMPLE BY THE FORM'S OWN PRE-REGISTERED CRITERIA: "
                + "; ".join(f) + ". The k* on this table MUST NOT be carried "
                "forward as if the form had survived.")

    df["form_verdict"] = df.apply(verdict, axis=1)
    return df


# ═══════════════════════════════════════════════════════════════ THE CHECKS
def _ledger_identity_rows(book: list) -> list[dict]:
    """`mae_held_r` cross-checked BY A DIFFERENT PATH — the trail ledger and the
    exit reason, never the bars.

    THE IDENTITY.  The initial stop sits exactly 1R below entry and the trail is
    MONOTONE, so `mae_held_r == -1.0` EXACTLY iff the campaign was stopped at an
    UN-ADVANCED stop — which the book records independently as
    `exit_reason == "stop" and not ratchet_exit`.  Neither side of that
    equivalence reads a bar extreme, and `campaign_mae` reads nothing else, so
    agreement is evidence rather than an echo.

    IT IS A CARDINALITY ASSERTION, NOT AN EXAMPLE.  Both counts and the
    symmetric difference are returned; a check that a single campaign satisfies
    is not a check.

    WHAT WOULD MAKE THIS WRONG: comparing only one direction of the
    equivalence; using a tolerance loose enough to absorb a ratcheted stop
    (advances are >= 0.05 ATR by the card's own minimum, far outside 1e-9); or
    reporting agreement without the counts, which is how a book once lost 64% of
    its rows with every fixture green.
    """
    held = np.array([campaign_mae(t)[0] for t in book])
    by_bars = {i for i, v in enumerate(held) if abs(v + 1.0) <= 1e-9}
    by_ledger = {i for i, t in enumerate(book)
                 if t.exit_reason == "stop" and not t.ratchet_exit}
    return [{
        "leg": "F-C6-AE-INDEP · mae_held_r == -1.0R  <=>  stopped at the "
               "un-advanced stop",
        "independent_path": "INDEPENDENT — bars vs (exit_reason, ratchet_exit)",
        "n_by_bars": len(by_bars), "n_by_ledger": len(by_ledger),
        "symmetric_difference": len(by_bars ^ by_ledger),
        "n_total": len(book),
        "passed": bool(by_bars == by_ledger and len(by_bars) > 0),
        "fails_if": "the two populations differ, or either is empty — an "
                    "identity nobody instantiates is not a check.",
    }]


def selfcheck(book: list, lo_ms: int, hi_ms: int,
              ks: tuple[float, ...] = K_GRID, card=None,
              sample_n: int = 20, champs: dict | None = None) -> pd.DataFrame:
    """EVERY FIXTURE LEG FOR THIS AREA, EACH STATING ITS OWN FAIL CONDITION AND
    WHETHER IT IS AN INDEPENDENT PATH OR A REPLICATION.

    ALL FOURTEEN LEGS, IN THE ORDER THEY RUN: LIM-0 (the fitted quantity is
    absent from the decision path), AE-1 (replication), AE-INDEP (independent,
    cardinality), AE-2 (bounds), HZ-1 (nested), HZ-2 (the degeneracy is
    labelled on exactly the rows that carry it — a count over 40, not a look at
    one), LIM-1 (geometry, all campaigns x all k), SPLIT-0 (the market half IS
    the card), LIM-2 (`book_split` CALLED and checked against a per-leg
    composition, both branches exercised), LIM-3 (the D12 cap applied ONCE,
    exercised at 3x funding where it actually bites), LIM-4 (`n_paired` on every
    frontier row), LIM-6 (the split arm is the convex combination, so clause (b)
    is vacuous), KEY (every table `BUILD_TABLES` names is uniquely keyed),
    LIM-5 (declared m == built m).

    `champs` is threaded in by `build` so the `ae_by_context` frame this keys is
    the same one that was published, not a second one built off a re-derived
    league.

    WHAT WOULD MAKE THIS WRONG: a leg that passes on a single example (every
    numeric leg here is a cardinality or an all-campaigns assertion); a leg
    labelled INDEPENDENT that re-walks the program's own loop; or a green table
    with an empty population — every leg prints the n it ran over so a vacuous
    pass is visible.
    """
    if card is None:
        card = RC.CARD_V6
    rows: list[dict] = []
    src = Path(__file__).read_text()

    # ── F-C6-LIM-0 · the fitted quantity does not enter the decision ─────────
    core = (Path(__file__).parent / "tierc6.py").read_text()
    tok = [t for t in ("avg_ae", "0.310491") if t in core]
    rows.append({
        "leg": "F-C6-LIM-0 · the Tier-C5 fitted scalar is absent from the core "
               "decision path (scripts/tierc6.py)",
        "independent_path": "INDEPENDENT — a source scan, not a re-computation",
        "n_total": 1, "detail": f"tokens found in tierc6.py: {tok or 'none'}; "
                                f"in this module the tokens appear only inside "
                                f"legacy_ae_study's disclosure "
                                f"({src.count('avg_ae')} textual hits).",
        "passed": not tok,
        "fails_if": "either token appears in the core — F-C5-g would be uncured "
                    "and the cure would be a claim rather than a fact.",
    })

    # ── F-C6-AE-1 · replication of _ride's AE accumulator ───────────────────
    errs, mism = [], 0
    for t in book:
        rec = _mae_to_1r_replicated(t)
        if (rec is None) != (t.mae_to_1r_r is None):
            mism += 1
        elif rec is not None:
            errs.append(abs(rec - float(t.mae_to_1r_r)))
    rows.append({
        "leg": "F-C6-AE-1 · campaign_mae's scan truncated at the first +1R bar "
               "reproduces t.mae_to_1r_r",
        "independent_path": "REPLICATION — it re-walks the program's own loop "
                            "and can only catch indexing drift. NOT evidence "
                            "about the quantity's meaning.",
        "n_total": len(book), "n_compared": len(errs),
        "max_abs_err": (max(errs) if errs else None),
        "none_ness_mismatches": mism,
        "passed": bool(mism == 0 and errs and max(errs) < 1e-12),
        "fails_if": "the two disagree beyond 1e-12 in memory, or a campaign the "
                    "book calls reached_1r fails to reach +1R on recomputation.",
    })
    rows += _ledger_identity_rows(book)

    # ── F-C6-AE-2 · bounds ──────────────────────────────────────────────────
    pairs = [campaign_mae(t) for t in book]
    h = np.array([p[0] for p in pairs])
    tp = np.array([p[1] for p in pairs])
    rows.append({
        "leg": "F-C6-AE-2 · mae_held_r >= -1.0 for EVERY campaign, and "
               "mae_held_r >= mae_tape_r always",
        "independent_path": "INDEPENDENT — a bound implied by the card's rail, "
                            "checked over the whole book",
        "n_total": len(book),
        "min_held": r6(float(h.min())), "min_tape": r6(float(tp.min())),
        "n_deeper_than_1R": int((h < -1.0 - 1e-9).sum()),
        "n_tape_beyond_1R": int((tp < -1.0 - 1e-9).sum()),
        "n_tape_differs": int((np.abs(h - tp) > 1e-12).sum()),
        "passed": bool((h >= -1.0 - 1e-9).all() and (h >= tp - 1e-12).all()),
        "fails_if": "any held excursion is deeper than the campaign's own stop "
                    "— the exit-bar clip would be broken and the hazard curve "
                    "would be conditioning on post-exit tape.",
    })

    # ── F-C6-HZ-1 / HZ-2 ────────────────────────────────────────────────────
    hz = hazard_curve(book, "both")
    ok = True
    for b in ("R", "ATR"):
        s = hz[hz["basis"] == b].sort_values("x")
        ok &= bool((s["n_at_or_beyond"].diff().dropna() <= 0).all())
        ok &= bool((s["wins"].diff().dropna() <= 0).all())
    rows.append({
        "leg": "F-C6-HZ-1 · n_at_or_beyond and wins are both NON-INCREASING in "
               "x, on both bases",
        "independent_path": "INDEPENDENT — a structural property of a nested "
                            "conditioning set",
        "n_total": len(hz), "passed": ok,
        "fails_if": "either rises — the conditioning set is not nested and the "
                    "curve is not a hazard curve.",
    })
    d1 = hz[(hz["basis"] == "R") & (np.abs(hz["x"] - 1.0) < 1e-9)]
    degen_rows = hz["degenerate"].astype(str).str.len() > 0
    n_degen = int(degen_rows.sum())
    n_degen_atr = int((degen_rows & (hz["basis"] == "ATR")).sum())
    n_appr = int(hz["approaching_the_identity"].astype(bool).sum())
    appr_expected = int(((hz["basis"] == "R")
                         & (hz["x"] >= 0.95 - 1e-12)).sum())
    rows.append({
        "leg": "F-C6-HZ-2 · the degeneracy is labelled on EXACTLY the rows that "
               "carry it — 1 degenerate row (R, x = 1.00) with wins == 0, "
               "approaching_the_identity on exactly the R rows at x >= 0.95, "
               "and NOTHING on the ATR basis",
        "independent_path": "INDEPENDENT — the identity is implied by the rail, "
                            "not by the curve. Asserted as a CARDINALITY over "
                            "all 40 rows of basis='both', not as a property of "
                            "the one row it is expected on.",
        "n_total": len(hz),
        "n_at_or_beyond_at_1r": int(d1["n_at_or_beyond"].iloc[0]) if len(d1) else 0,
        "wins": int(d1["wins"].iloc[0]) if len(d1) else None,
        "n_degenerate_rows": n_degen, "n_degenerate_on_atr": n_degen_atr,
        "n_approaching_rows": n_appr,
        "n_approaching_expected": appr_expected,
        "passed": bool(len(d1) == 1 and int(d1["wins"].iloc[0]) == 0
                       and bool(d1["degenerate"].iloc[0])
                       and n_degen == 1 and n_degen_atr == 0
                       and appr_expected > 0 and n_appr == appr_expected),
        "fails_if": "the identity is printed as evidence; or the degenerate "
                    "label SPREADS to rows that are not the identity. Reading "
                    "only the x=1.00R row prints green just as happily when "
                    "EVERY R row is stamped degenerate — a label checked on one "
                    "example where a count over 40 rows was available.",
    })

    # ── F-C6-LIM-1 · geometry, ALL campaigns x ALL k ────────────────────────
    bad = 0
    for t in book:
        for k in ks:
            lim = limit_px(t, k)
            near = (lim - t.entry_px) * t.direction
            far = (lim - t.stop_px) * t.direction
            if not (near < 0.0 and far > 0.0):
                bad += 1
    rows.append({
        "leg": "F-C6-LIM-1 · the limit is STRICTLY between entry and the "
               "initial stop, all campaigns x all k",
        "independent_path": "INDEPENDENT — a geometric bound from the 1.0 ATR "
                            "rail, exhaustive not sampled",
        "n_total": len(book) * len(ks), "n_violations": bad,
        "min_r_over_atr": r6(min(_r_over_atr(t) for t in book)),
        "max_k": max(ks), "passed": bad == 0,
        "fails_if": "any k puts the limit at or beyond the stop — the "
                    "'improvement' would be worse than the stop it replaced.",
    })

    # ── F-C6-SPLIT-0 · the market half IS the card ──────────────────────────
    ident = [abs((t.entry_px - t.stop_px) * t.direction - t.r_dist) for t in book]
    rows.append({
        "leg": "F-C6-SPLIT-0 · stop_px == entry_px - d*r_dist on EVERY campaign "
               "— which is what makes '1R beyond the market fill' the CARD's own "
               "anchor and lets the split arm reuse the filed Trade instead of "
               "re-riding it",
        "independent_path": "INDEPENDENT — the filed stop is compared with the "
                            "filed R, two fields the split arm never combines",
        "n_total": len(book), "max_abs_err": max(ident),
        "passed": bool(max(ident) < 1e-9),
        "fails_if": "the identity does not hold — then 'two stops, one R' is "
                    "not the card plus a limit leg, the split arm silently "
                    "changes the market half's risk, and every net_r on the "
                    "SPLIT rows is a different quantity from the one claimed.",
    })

    # ── F-C6-LIM-2 · the split algebra, ceiling OFF ─────────────────────────
    rng = np.random.default_rng(SEED)
    idx = rng.choice(len(book), size=min(sample_n, len(book)), replace=False)
    nocap = dataclasses.replace(card, funding_ceiling_r=None)
    worst, ncmp, n_miss, n_fill, flag_bad = 0.0, 0, 0, 0, 0
    hi_i = {s: _idx_range(frame(s)["f"].open_ms, lo_ms, hi_ms)[1]
            for s in {t.symbol for t in book}}
    for i in idx:
        t = book[int(i)]
        base_uncapped = t.gross_r - t.fee_r - t.funding_r_uncapped
        for k in ks:
            h = ride_limit_half(t, float(k), hi_i[t.symbol], nocap)
            # THE TARGET IS COMPOSED PER LEG — each leg's OWN
            # (gross - fee - funding), halved.  `book_split` composes the same
            # quantity PER COMPONENT (halved gross, halved fee, one
            # campaign-level funding term).  Different grouping, same number:
            # so this leg is a test OF THE FUNCTION and not the distributive law
            # applied twice to one set of operands.  The previous form of this
            # leg computed both sides here and never called `book_split`; it
            # passed at 8.9e-16 with `book_split` returning net_r + 999.
            leg_uncapped = 0.0 if h is None else (
                float(h["acc"]["gross_r"]) - float(h["acc"]["fee_r"])
                - float(h["acc"]["funding_r_uncapped"]))
            target = 0.5 * base_uncapped + 0.5 * leg_uncapped
            sp = book_split(t, h, nocap)
            if h is None:
                n_miss += 1
            else:
                n_fill += 1
            flag_bad += int(bool(sp["limit_filled"]) != (h is not None))
            worst = max(worst, abs(float(sp["net_r"]) - target))
            ncmp += 1
    rows.append({
        "leg": "F-C6-LIM-2 · with the ceiling OFF, book_split's OWN net_r == "
               "0.5*net_r_card + 0.5*net_r_limit, and 0.5*net_r_card on a miss",
        "independent_path": "INDEPENDENT — book_split is CALLED and its return "
                            "compared with a per-leg composition of _account's "
                            "own fields, a different grouping of the same "
                            "quantity. Exercised on BOTH branches (fills and "
                            "misses), counts printed.",
        "n_total": ncmp, "n_fills_exercised": n_fill,
        "n_misses_exercised": n_miss,
        "n_limit_filled_flag_wrong": flag_bad,
        "max_abs_err": worst,
        "passed": bool(worst < 1e-9 and flag_bad == 0
                       and n_fill > 0 and n_miss > 0),
        "fails_if": "the identity fails — the two-stop resolution was not "
                    "implemented as two independent rides at half size; or the "
                    "sample exercised only one branch, which would leave the "
                    "miss arithmetic (half a card, NOT 0.0) untested while the "
                    "leg printed green.",
    })

    # ── F-C6-LIM-3 · the D12 cap applied ONCE, exercised where it bites ─────
    cap = RC.FUNDING_CEILING_R
    differ_1x = differ_3x = 0
    bound_1x = bound_3x = 0
    for t in book:
        for k in ks:
            h = ride_limit_half(t, float(k), hi_i[t.symbol], card)
            ul = 0.0 if h is None else float(h["acc"]["funding_r_uncapped"])
            for mult, sink in ((1.0, "1x"), (3.0, "3x")):
                a_ = 0.5 * mult * float(t.funding_r_uncapped)
                b_ = 0.5 * mult * ul
                once = min(a_ + b_, cap)
                twice = min(a_, cap) + min(b_, cap)
                if sink == "1x":
                    differ_1x += int(abs(once - twice) > 1e-12)
                    bound_1x += int(a_ + b_ > cap)
                else:
                    differ_3x += int(abs(once - twice) > 1e-12)
                    bound_3x += int(a_ + b_ > cap)
    rows.append({
        "leg": "F-C6-LIM-3 · the D12 ceiling is applied ONCE to the summed "
               "uncapped funding; capping per half is a different (wrong) rule",
        "independent_path": "INDEPENDENT — the two cap orderings are compared "
                            "directly, and the leg is EXERCISED at 3x where the "
                            "ceiling actually binds",
        "n_total": len(book) * len(ks),
        "n_bound_at_1x": bound_1x, "n_differ_at_1x": differ_1x,
        "n_bound_at_3x": bound_3x, "n_differ_at_3x": differ_3x,
        "passed": bool(differ_3x > 0 or bound_3x == 0),
        "fails_if": "the cap is applied per half — a silent 2R campaign "
                    "ceiling. NOTE: at unit size the ceiling binds on 0 "
                    "campaigns, so the 1x leg is VACUOUS and is reported as "
                    "such; the 3x leg is the one carrying evidence.",
    })

    # ── F-C6-LIM-4 / LIM-5 ──────────────────────────────────────────────────
    fr = frontier(book, lo_ms, hi_ms, ks=ks, card=card)
    rows.append({
        "leg": "F-C6-LIM-4 · d15's n_paired == len(book) on EVERY frontier row",
        "independent_path": "INDEPENDENT — d15 is the estate's own function, "
                            "not reimplemented here",
        "n_total": len(fr),
        "n_paired_values": sorted(set(int(v) for v in fr["n_paired"])),
        "passed": bool((fr["n_paired"] == len(book)).all()),
        "fails_if": "misses were dropped from the cell and the arm's largest "
                    "effect — not being in the trade — went into "
                    "unpaired_base_n.",
    })
    ce = float(np.mean([t.net_r for t in book]))
    worst_cc, worst_pd = 0.0, 0.0
    for k in ks:
        f_ = fr[(fr["arm"] == "FULL-LIMIT") & (np.abs(fr["k_x_atr"] - k) < 1e-12)]
        s_ = fr[(fr["arm"] == "SPLIT-ENTRY") & (np.abs(fr["k_x_atr"] - k) < 1e-12)]
        worst_cc = max(worst_cc, abs(float(s_["expectancy_r"].iloc[0])
                                     - 0.5 * (ce + float(f_["expectancy_r"].iloc[0]))))
        worst_pd = max(worst_pd,
                       abs(float(s_["paired_delta_expectancy_r"].iloc[0])
                           - 0.5 * float(f_["paired_delta_expectancy_r"].iloc[0])))
    rows.append({
        "leg": "F-C6-LIM-6 · the SPLIT arm is EXACTLY the 50/50 convex "
               "combination of the card and the FULL-LIMIT arm, so k*(SPLIT) == "
               "k*(FULL) BY CONSTRUCTION and falsification clause (b) is VACUOUS",
        "independent_path": "INDEPENDENT — the identity is derived from "
                            "_account's linearity in size and checked against "
                            "the built table, which never used it",
        "n_total": len(ks) * 2,
        "max_abs_err_expectancy": worst_cc,
        "max_abs_err_paired_delta": worst_pd,
        "passed": bool(worst_cc < 5e-4 and worst_pd < 5e-4),
        "fails_if": "the identity does NOT hold — then the split arm was not "
                    "implemented as two independent legs at half size sharing "
                    "one R, or the D12 ceiling bound somewhere and the arm "
                    "stopped being affine. EITHER WAY THE FINDING STANDS: while "
                    "it DOES hold, the declared m = 10 overstates the argmax's "
                    "effective selection surface, which is 5.",
    })
    # EVERY frame `build()` publishes, enumerated against `build()` itself so
    # the leg cannot go on saying "every published table" while checking a
    # subset of them. The earlier form checked 5 of the 7 and omitted
    # `ae_by_context` — the one table in this module with a 20-cell cross and
    # hand-built zero rows, i.e. the one where a duplicate key was most likely.
    keyed = {"ae_deciles": (ae_deciles(book, lo_ms, hi_ms), ["bucket", "key"]),
             "legacy_ae_study": (legacy_ae_study(book, lo_ms, hi_ms),
                                 ["population"]),
             "hazard_curve(R)": (hazard_curve(book, "R"), ["x_r"]),
             "hazard_curve(ATR)": (hazard_curve(book, "ATR"), ["x_atr"]),
             "hazard_curve(both)": (hz, ["basis", "x"]),
             "ae_by_context": (ae_by_context(book, champs), ["context", "bucket"]),
             "frontier": (fr, ["k_atr", "arm"])}
    published = set(BUILD_TABLES)
    covered = {"hazard_curve": "hazard_curve(R)",
               "hazard_curve_atr": "hazard_curve(ATR)"}
    missing = sorted(p for p in published
                     if p not in keyed and covered.get(p) not in keyed
                     and p != "selfcheck")
    dups = {k: int(v.duplicated(subset=ky).sum()) for k, (v, ky) in keyed.items()}
    rows.append({
        "leg": "F-C6-KEY · EVERY table build() publishes has a unique DECLARED "
               "key (F-KEY) — the coverage is enumerated against build()'s own "
               "table list, not against a hand-kept subset",
        "independent_path": "INDEPENDENT — a property of the emitted frames, "
                            "not of the code that built them",
        "n_total": sum(len(v) for v, _ in keyed.values()),
        "n_tables_checked": len(keyed),
        "published_tables": sorted(published),
        "published_but_unchecked": missing,
        "duplicates_per_table": dups,
        "passed": bool(all(v == 0 for v in dups.values()) and not missing),
        "fails_if": "any declared key repeats — a join on a non-unique key "
                    "silently drops or multiplies rows, and the driver would "
                    "HALT at write time instead of here; OR build() grows a "
                    "table this leg does not key, which is how a check that "
                    "says 'every' becomes a check that says 'the five I "
                    "remembered'. NOTE the deliberate asymmetry: "
                    "hazard_curve('both') is keyed on (basis, x) because 0.50R "
                    "and 0.50 ATR are thresholds of DIFFERENT quantities and a "
                    "bare threshold column across both bases is not a key.",
    })
    rows.append({
        "leg": "F-C6-LIM-5 · declared m == built m, and k_promoted says NO on "
               "every row",
        "independent_path": "INDEPENDENT — the declaration is a constant, the "
                            "count is the table's length",
        "n_total": len(fr), "declared_m": LIM2_M, "built_m": len(fr),
        "prereg_sha256": prereg_sha256(),
        "passed": bool(len(fr) == LIM2_M
                       and (fr["k_promoted"] == K_PROMOTED).all()),
        "fails_if": "the declared m and the constructed m disagree — the "
                    "selection surface would be a number the code derived from "
                    "itself.",
    })
    return pd.DataFrame(rows)


def build(book: list, lo_ms: int, hi_ms: int, champs: dict | None = None,
          card=None, prereg_path: str | Path | None = None
          ) -> dict[str, pd.DataFrame]:
    """Every table this module publishes, in one call, in publication order.

    The champions are resolved ONCE here and threaded into both `ae_by_context`
    and `selfcheck`, so the table and the check that keys it cannot be
    describing two different league states.

    WHAT WOULD MAKE THIS WRONG: computing the frontier before the
    pre-registration exists (pass `prereg_path` and `frontier` enforces it);
    returning the frontier without `selfcheck`, which is where every fail
    condition on this area is actually evaluated; or adding a table here without
    adding it to `BUILD_TABLES` — F-C6-KEY keys what this list names, so a table
    that is published but unlisted would be published unkeyed.
    """
    if champs is None:
        champs = _default_champs()
    out = {
        "ae_deciles": ae_deciles(book, lo_ms, hi_ms),
        "legacy_ae_study": legacy_ae_study(book, lo_ms, hi_ms),
        "hazard_curve": hazard_curve(book, "R"),
        "hazard_curve_atr": hazard_curve(book, "ATR"),
        "ae_by_context": ae_by_context(book, champs),
        "frontier": frontier(book, lo_ms, hi_ms, card=card,
                             prereg_path=prereg_path),
        "selfcheck": selfcheck(book, lo_ms, hi_ms, card=card, champs=champs),
    }
    if tuple(out) != BUILD_TABLES:
        raise SystemExit(
            f"HALT: build() publishes {tuple(out)} but BUILD_TABLES declares "
            f"{BUILD_TABLES}. F-C6-KEY keys what BUILD_TABLES names; a table "
            f"published outside that list would be published unkeyed.")
    return out


def main() -> int:                                          # pragma: no cover
    raise SystemExit("tierc6_lab_limit is a library; drive it from the build "
                     "driver or from build().")
