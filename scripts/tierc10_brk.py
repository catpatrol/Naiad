#!/usr/bin/env python
"""TIER-C10 · BRK LANE MECHANICS — P-BRK-S1 (SCALPER, 5m) · P-BRK-I1 (INVESTOR, 1d).

RATIFIED operator 2026-09-21 (TIER-C10; Q1-Q5 on lean, R1-R6 rulings).  Drafted
APOLLO · Executor HEPHAESTUS · Seed 20260921.  THIS MODULE IS MECHANICS ONLY.

═══════════════════════════════════════════════════════════════════════════════
LAW 4 — TEXT BEFORE RESULT — IS THE FIRST THING IN THIS FILE.
No registration for P-BRK-S1 or P-BRK-I1 exists.  Until one does, EVERY runner
in this module HALTs at its first statement, because its first statement is the
panel gate (`TP.require_arm`).  Nothing here computes a P-BRK number, and the
only real bars this file's fixtures ever read are the KNOWN CONTROL's (card v6
on CLASSIC5) — the one run LAW 4 allows, and the one that licenses the phrase
"v6 management lens-scaled".  Everything else is a synthetic tape.
═══════════════════════════════════════════════════════════════════════════════

WHAT THIS MODULE IS.  Four things, in this order, each usable without the next:

  (A) THE LENS-PARAMETERISED FRAME AND RIDE, keyed `(sym, lens)`.  The lineage's
      runners are 4h-hardwired and memoise on the BARE SYMBOL (`tierc5.frame`,
      `tierc8.anchor_series`, `tierc9.role_arrays`); a 5m or 1d frame stored
      under that key would poison the asset's 4h book — the F-C8-MATCH lesson,
      one tier later.  So every memo here carries the lens IN THE KEY and the
      4h lens is not merely "compatible with" the lineage's frame, it IS it
      (`TP.frame_n`), re-read through the Stage D loader and proved equal.
      THE RIDE IS `tierc9._ride_leg9`, TRANSCRIBED, with every array read
      re-pointed at the lens: same periods, same pins, same within-bar order
      (STOP -> BELL -> HARVEST -> TRAIL), adverse-first, stop fills AT the stop.
      F-BRK-RIDE-4H rides the CONTROL's own entries through it at lens='4h' and
      demands 0.000e+00 against the control book.

  (B) THE DECISION FUNCTIONS, WHICH IMPORT NO RANGE CODE.  Macro DIEs, memory
      -line flips and the as-of layer arrive as ARGUMENTS — plain integers and
      floats.  The one place this file reaches the range machine is §10, a
      named ADAPTER with a FUNCTION-LOCAL import, called by runners and never
      by a decision function.  `f_brk_closure` proves the module-level import
      closure of the decision half is range-free and analytics-free.

  (C) THE PERMISSIONS.  The 4h tide for a 5m bar under `engine.htf`'s
      visibility law (an HTF bar is visible iff it CLOSED at or before the exec
      bar's OPEN), and the R4 ribbon lifecycle — EXPANDING / CONSOLIDATING /
      DIRECTION on (e12 - e25) / ATR14 — for the investor's daily direction and
      weekly posture.

  (D) THE ACCOUNTING.  Fee by OBJECT (`RC.FEE_BPS_SIDE`, 5 bps a side = the
      contract's 10 bps round trip), funding by INTERVAL SUM
      (`entry_ms < funding_hour_ms <= exit_ms`, Stage D LEAN D-g) with the
      lineage's 1R ceiling, and the 5m toll read FROM THE FILED GRID, never
      typed (F-C10-TOLL).

THE OPERATOR'S RULINGS THIS MODULE IMPLEMENTS (verbatim quotes in `RULINGS`):
  R1 the five EMA bands and the TUNED (band, margin_atr, hold_bars) — read at
     run time from the census builder's tuning result FOR THE LENS ASKED FOR
     (5m = P-BRK-S1's scored arm, 1d = the Tier-E EMA-band print of P-BRK-I1),
     never hard-coded, and never one lens's cell served to another;
  R2 PANEL17 for both lanes; S1 scored on the HOLDOUT era only;
  R4 the 12/25 ribbon lifecycle, and lens-scaled v6 management in which a
     component whose EMA is not warm on that lens is INACTIVE for the campaign
     — counted and printed, NEVER imputed — and the BRK lanes bell ALSO on the
     lens's counter 12/25 cross.

THE EIGHT PINS THIS READING ADDS (this module's own; every one printed):
  B1 WARMTH IS DECIDED ONCE, AT THE ENTRY BAR, and holds for the whole
     campaign.  The alternative — a component that switches on mid-ride — is
     NOT taken: it would make "INACTIVE for that campaign" a per-bar fact that
     no per-campaign count could report honestly.
  B2 THE 12/25 BELL IS TESTED LAST.  When two bells ring on one bar the v6
     label wins, so a lens-scaled exit reason can never hide a card exit.
  B3 EXPANDING reads the window s[t-K .. t] — K+1 samples, K steps — because
     the ruling's own comparison is against t-K.
  B4 INTERVAL-SUM FUNDING PRICES EACH STAMP at the close of the last lens bar
     CLOSED at or before that stamp.  On 4h that IS the lineage's
     `rate * c[j-1]`, bar for bar; on 1d it keeps the 08:00 and 16:00 stamps
     the per-bar-open lookup silently drops.
  B5 CANDIDACY ends at the next macro DIE or `MEM_TTL_BARS` bars — the census
     builder's window — applied to BOTH anchors (see FINDINGS, mismatch 1).
  B6 THE ERA TEST IS THE PANEL MODULE'S (`TP.in_era` on `entry_ms`), reached
     through this module's own door so a tuning-era entry HALTS AT THE REPLAY
     rather than being refused later by `external_book`.  The alternative —
     testing the entry bar's CLOSE — is NOT taken: it is LOOSER for a bar that
     straddles the cut, so a campaign could pass here and die at the door.
  B7 EVERY PERMISSION IS READ AT THE ENTRY BAR (the lineage's arming-bar law),
     as of bars CLOSED at that instant.
  B8 THE SPELLING LAW.  This module and the census builder name the same five
     R1 bands in two house styles (`ribbon-127/200` / `ribbon127_200`); every
     name that crosses the boundary — the tuned band read in, the class label
     written out — goes through `band_key` / `census_band`, which are algebra
     over `R1_BANDS` and cannot name a sixth band.  Neither module's style is
     corrected; the translator is the only new object.

Run (mechanics card only; no lane rides, none can):
    export NAIAD_CACHE_DIR=~/.cache/naiad/snapshots/tc10_20260921
    ~/venvs/naiad/bin/python scripts/tierc10_brk.py [--out DIR]
"""
from __future__ import annotations

import dataclasses
import hashlib
import itertools
import json
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

# ── THE IMPORT CLOSURE OF THE DECISION HALF.  Every name below is range-free
# ── and analytics-free; `f_brk_closure` walks the closure and proves it.
import tierc10_panel as TP                                           # noqa: E402
import tierc10_data as D                                             # noqa: E402
import tierc9 as T9                                                  # noqa: E402
import tierc8 as T8                                                  # noqa: E402
import tierc7 as T7                                                  # noqa: E402
import tierc7_rules as RC                                            # noqa: E402
from engine import htf as HTF                                        # noqa: E402
from engine import indicators as ind                                 # noqa: E402

SEED = TP.SEED                      # 20260921, by object
SEED_LINEAGE = TP.SEED_LINEAGE      # 20260816 — the sensitivity echo [L8]
OUT = TP.OUT / "brk"
OUT_RERUN = TP.OUT_RERUN / "brk"
LEAN_TAG = TP.LEAN_TAG

MS_1H = 3_600_000
LENS_MS = dict(D.STEP_MS)           # 5m 1h 4h 12h 1d 1w — by object, Stage D's
LENSES = ("5m", "4h", "1d")         # the lenses this module rides
RANGE_PINS_SOURCE = ROOT / "engine" / "rangefinder.py"

# ── THE FROZEN RANGE PINS, READ OUT OF THE SOURCE, NEVER IMPORTED.  Importing
# ── engine.rangefinder here would put the range machine in the closure of
# ── every module that imports this one — the v6 path must stay range-free
# ── (F-BR-14).  `D.pin_literal` reads ONE literal out of the AST.
FLIP_HOLD_MARGIN = float(D.pin_literal(RANGE_PINS_SOURCE, "PINS_V2",
                                       "FLIP_HOLD_MARGIN"))          # 1.0 ATR
FLIP_HOLD_BARS = int(D.pin_literal(RANGE_PINS_SOURCE, "PINS_V2",
                                   "FLIP_HOLD_BARS"))                # 6 bars
MEM_TTL_BARS = int(D.MEM_TTL_BARS)                                   # 400, by object
FROZEN_SCALE = float(D.pin_literal(RANGE_PINS_SOURCE, "PINS_V2",
                                   "SCALE_MULT"))                    # 3.0 [L2]

# ── THE LANES ────────────────────────────────────────────────────────────────
LANE_S1 = "brk-s1"                  # the string its trades carry into the gate
LANE_I1 = "brk-i1"
LANE_LENS = {LANE_S1: "5m", LANE_I1: "1d"}
ANCHOR_BAND = "band"
ANCHOR_MEMORY = "memory-line"
ANCHORS = (ANCHOR_BAND, ANCHOR_MEMORY)
# THE SCORED ANCHOR PER LANE; each lane ALSO runs with the OTHER anchor as a
# Tier-E print (`run_lane_*(anchor=...)`), which is what the contract's "Both
# BRK forms also printed with the OTHER anchor" asks for.
LANE_ANCHOR = {LANE_S1: ANCHOR_BAND, LANE_I1: ANCHOR_MEMORY}
LANE_TIER_E_ANCHOR = {LANE_S1: ANCHOR_MEMORY, LANE_I1: ANCHOR_BAND}
LANE_ORDER = (LANE_S1, LANE_I1)     # the order every grid and row list rides
FORM_OF = {LANE_S1: "P-BRK-S1", LANE_I1: "P-BRK-I1"}    # the registration name

# ── THE PANEL: DECLARED vs SERVED.  These are two different things and the
# ── module has only ever OWNED the second one.
PANEL_DECLARED = (
    "CLASSIC5 — the 5-asset book, per operator ruling R8 of 2026-09-22 ('5-"
    "asset book — the PANEL PIN governs'), which SUPERSEDES ruling R2 of "
    "2026-09-21 ('All 17') on the operator's own word.  LOAO above-half bar = "
    "3/5.  The 17-asset view prints as TIER-E beside each BRK row [R8], which "
    "is the `tier_e_panel17` slot of the row.")
PANEL_SERVED_LAW = (
    "EITHER PANEL, WITHOUT A CODE CHANGE.  Neither runner names a panel: both "
    "score on `g['panel']` — the panel the REGISTRATION names, checked by "
    "`TP.require_arm` — and every object downstream is keyed on that same "
    "tuple (`TP.corridor_era(g['panel'], era)` for the window, "
    "`TP.panel_name` for the label, `stamp_toll` per asset out of the filed "
    "grid, `TP.external_book` for the door).  So the panel is a "
    "REGISTRATION-TEXT decision and always was; R8 changes the text, not this "
    "file.")

# ── THE ERA [R1/R2] — BOUND TO THE PANEL MODULE, NEVER RESTATED ──────────────
# The panel module owns the era: `ERA_CUT_ISO`, `era_window`, `in_era`,
# `corridor_era`, and the refusal inside `external_book`.  A second cut here,
# even a correct one, could drift from the one that refuses the journal — and
# it would drift in the direction that lets a campaign through this module and
# die at the door.  So this module BINDS.  ("One place, so the corridor, the
# door and the scorer cannot drift apart" — tierc10_panel.in_era.)
ERA_CUT_ISO = TP.ERA_CUT_ISO        # "2024-06-30T23:59:59Z" [R1]
ERA_CUT_MS = TP.ERA_CUT_MS
ERAS = TP.ERAS                      # full | tuning | holdout
LANE_ERA = {LANE_S1: "holdout", LANE_I1: "full"}    # [R1] S1's pins are tuned
#                                   on the tuning era; I1 tunes nothing [R2]

# ── THE RIBBON [R4] ──────────────────────────────────────────────────────────
RIBBON_FAST, RIBBON_SLOW = 12, 25   # the lattice pair (brief2.LATTICE_EMAS)
LIFECYCLE_K = 3                     # [LEAN-HEPHAESTUS B3] the executor's K
PHASE_WARMUP, PHASE_EXPANDING, PHASE_CONSOLIDATING = ("WARMUP", "EXPANDING",
                                                      "CONSOLIDATING")

# ── THE FIVE R1 BANDS ────────────────────────────────────────────────────────
R1_BANDS = ("ribbon-89/127", "ribbon-127/200", "tap-89", "tap-127", "tap-200")


# ── THE SPELLING LAW — ONE OBJECT, TWO HOUSE STYLES, NO THIRD BAND ───────────
# Two modules name the same five bands and do not spell them alike: this one
# writes the operator's own hyphen/slash form (`ribbon-127/200`), the census
# builder writes the form its class labels can carry (`ribbon127_200`, `tap89`
# — `tierc10_census.RETEST_BAND_NAMES`).  Neither spelling is wrong and
# neither module is edited for the other's sake; instead EVERY band name that
# crosses the boundary passes through the two functions below, which are pure
# separator algebra over `R1_BANDS` and cannot invent a sixth band.
#
# WHAT THIS REPLACES IS A HALT, AND IT WAS A REAL ONE (review, 2026-09-21):
# `tuned_pins` refused the census's OWN filed result ("names band
# 'ribbon127_200'") and `toll_class` asked the grid for a row
# (`retest-hold-ribbon-127/200`) that has never existed in it, so P-BRK-S1
# could not have ridden one bar even with a registration in hand.  The
# disagreement was never mathematical: `r1_band` and the census's `band_of`
# were checked equal bar for bar on all five bands, NaN pattern included
# (F-C10-TOLL now re-checks that on every run).  It was two spellings and no
# translator.
def _band_canon(name) -> str:
    """A band name folded to the only thing both house styles share: lower
    case, every separator gone.  `ribbon-127/200` and `ribbon127_200` both
    read `ribbon127200`."""
    return "".join(ch for ch in str(name).strip().lower()
                   if ch not in "-_/ ")


BAND_EXAMPLE = R1_BANDS[1]          # the one the card and the transcript show
_R1_BY_CANON = {_band_canon(b): b for b in R1_BANDS}
if len(_R1_BY_CANON) != len(R1_BANDS):      # a guard on the law, not on data
    raise SystemExit(f"HALT: two of {R1_BANDS} fold to the same skeleton; the "
                     f"spelling law could not tell them apart.")


def band_key(name) -> str:
    """THE OPERATOR'S BAND, BY WHICHEVER SPELLING IT ARRIVES IN — this
    module's canonical name for it.

    HALTS IF: the name is not one of the operator's five under ANY spelling.
    A band that does not fold onto one of the five is not a spelling variant,
    it is a sixth band, and a sixth band is the operator's to name.

    WHAT WOULD MAKE THIS WRONG: a fallback.  A reader that returned some
    default band when the fold missed would silently ride the wrong EMAs.
    """
    b = _R1_BY_CANON.get(_band_canon(name))
    if b is None:
        raise SystemExit(
            f"HALT: {name!r} (folded to {_band_canon(name)!r}) is not one of "
            f"the operator's five bands in any spelling.  This module writes "
            f"them {R1_BANDS}; the census writes them "
            f"{tuple(k + s.replace('/', '_') for k, s in (b_.split('-', 1) for b_ in R1_BANDS))}.")
    return b


def census_band(name) -> str:
    """THE CENSUS GRID'S SPELLING of an R1 band — `ribbonA_B` / `tapP`, which
    is what `tierc10_census.RETEST_BAND_NAMES` holds and what the filed
    `outcome_grid.parquet` keys its `retest-hold-*` rows on.  Built by
    algebra, never by a table, so the two can only drift if the OPERATOR's
    five change — and then `band_key` HALTs rather than guess."""
    kind, spec = band_key(name).split("-", 1)
    return kind + spec.replace("/", "_")


# ── THE TUNED PINS' FILES [R1] — ONE PER TUNED LENS, NEVER A NEIGHBOUR'S ─────
# The census builder files one result per lens it tunes
# (`tierc10_census.TUNING_RESULT_NAME`): the 5m result IS P-BRK-S1's scored
# arm, and the 1d result exists only for the Tier-E EMA-band print of
# P-BRK-I1 ("The 1d lens repeats the tuning with n >= 30 for the Tier-E
# EMA-band print of P-BRK-I1 only" — R1).  They are different cells with
# different bands, margins and holds.  A single path here would have handed
# the 5m cell to the 1d lens and then overwritten its `lens` field with the
# one asked for — a typed pin wearing a tuned pin's name, which is exactly
# what `tuned_pins` exists to refuse (found in review, 2026-09-21).
TUNING_RESULT_FOR = {"5m": TP.OUT / "census" / "TUNING_RESULT.json",
                     "1d": TP.OUT / "census" / "TUNING_RESULT_1d.json"}
TUNED_LENSES = tuple(TUNING_RESULT_FOR)
TUNING_RESULT = TUNING_RESULT_FOR["5m"]     # P-BRK-S1's own, kept by name

# ── THE TOLL [F-C10-TOLL] ────────────────────────────────────────────────────
# The census grid keys its rows on (asset, lens, cls, scale_kind, horizon).
# A lane's own toll is the toll of the EVENT CLASS it enters on.
TOLL_CLASS_PREFIX = {ANCHOR_BAND: "retest-hold-", ANCHOR_MEMORY: "flip-hold"}

ROW_ROUND_ND = 8                    # every filed float, census house rounding

# ── THE [Q-R3] INTERFACE — DECLARED HERE, OWNED BY THE CENSUS TRACK ──────────
# This is the ONE place the BRK side names the height-vs-toll tables.  If the
# census track files them under other names or other schemas, exactly these
# constants move and nothing else in this module does.
#
# REPOINTED 2026-09-22 (review, blocking finding 2).  The interface declared in
# the last round was a GUESS made at 10:15 and the census filed at 10:25: one
# table `height_vs_toll.parquet` with columns (toll_atr, height_over_toll_
# median, verdict, n).  What exists is TWO tables under other column names —
#   census/height_toll.parquet          360 rows, key (asset, lens,
#                                       scale_kind, era), the FIGURES;
#   census/height_toll_verdict.parquet  120 rows, key (asset, lens,
#                                       scale_kind) — NO era — the VERDICT,
#                                       which is not a string but
#                                       verdict_pass (bool) + verdict_law +
#                                       reason.
# The vocabulary (POOLED:ALL / POOLED:CLASSIC5 / POOLED:UNSEEN12, lens
# {5m,4h,1d}, scale_kind {frozen3.0,calibrated}, era {ALL,tuning,holdout})
# matched the guess exactly; only the names and the table split were wrong.
# The guess was `.exists() == False` and always would have been, so every BRK
# row's verdict slot was a PendingVerdict FOREVER and contract line 112's
# second half was unsatisfiable BY CONSTRUCTION.  The three verbatim verdict
# fields are carried through unread, so the "this module pins no vocabulary"
# lean [B10] survives the repoint intact.
HEIGHT_VS_TOLL_PATH = TP.OUT / "census" / "height_toll.parquet"
HEIGHT_VS_TOLL_VERDICT_PATH = TP.OUT / "census" / "height_toll_verdict.parquet"
HEIGHT_VS_TOLL_KEY = ("asset", "lens", "scale_kind", "era")
HEIGHT_VS_TOLL_VERDICT_KEY = ("asset", "lens", "scale_kind")
HEIGHT_VS_TOLL_FIELDS = ("height_atr_median", "toll_atr_median",
                         "ratio_median", "n_ranges")
HEIGHT_VS_TOLL_VERDICT_FIELDS = ("verdict_pass", "verdict_law", "reason")
# the columns BOTH tables carry: the join is keyed differently on each side
# (the verdict has no era), so the figures they share are the only thing that
# can prove the two rows are about the SAME measurement.  They agree today.
HEIGHT_VS_TOLL_AGREE = ("n_ranges", "height_atr_median", "toll_atr_median")
HEIGHT_VS_TOLL_INT_FIELDS = ("n_ranges",)
# THE AS-OF WARRANTY, ENFORCED ACROSS THE TRACK BOUNDARY [LEAN-HEPHAESTUS H3].
# Both filed census tables carry this column.  A measurement stamped at any
# other instant is not one a BRK row may carry, so the read HALTs on it.
HEIGHT_VS_TOLL_ASOF_COL = "as_of_last_closed_4h"
HEIGHT_VS_TOLL_SCALE = "frozen3.0"  # the pin of record [L2]; `calibrated` is
#                                     in-sample by construction and may not
#                                     reach a scored lane's row
HEIGHT_VS_TOLL_ERA = "ALL"          # the census's full-history row; the era
#                                     column exists so a later reading can ask
#                                     for 'holdout' without a schema change
HEIGHT_VS_TOLL_OWNER = ("the CENSUS track, contract item [Q-R3] — 'HEIGHT-vs-"
                        "TOLL feasibility per lens (confirmed-range height / "
                        "round-trip toll, distribution)'")
HEIGHT_VS_TOLL_STATUS = ("FILED by the census track on 2026-09-22T10:25, "
                         "RE-FILED 2026-09-22T11:26 with a `provisional` flag "
                         "and a minimum-n floor, and READ here; this module "
                         "computes none of it.")
# ── THE LAW HALF OF THE CROSS-CHECK [review round 2, finding 2] ────────────
# HEIGHT_VS_TOLL_AGREE above is the NUMERIC half.  Both filed tables also
# carry `gate_law_sha` — the sha of the gate law that produced the row — and
# two rows built under different laws are not one measurement however well
# their numbers line up.  This module pins NO sha of its own: it compares the
# two tables to each other, which is a join check and not a second copy of
# another track's law.
HEIGHT_VS_TOLL_AGREE_STR = ("gate_law_sha",)
# ── THE SAMPLE FLOOR, READ OFF THE ROW AND NEVER RE-PINNED HERE ────────────
# The census re-filed [Q-R3] on 2026-09-22 with a `provisional` flag and a
# minimum-n floor (its PROVISIONAL_MIN_N = 30); the PASS count fell 22 -> 9 of
# 120 rows and a new `edge_n_ranges` column counts the EDGE leg's floor in
# confirmed ranges.  This module keeps NO second copy of that 30: the row
# carries `min_n_ranges_pinned` / `edge_min_n_ranges_pinned` and those are
# what the HALT quotes.  All five columns are REQUIRED of the verdict table,
# so a table re-filed WITHOUT the flag stops the read instead of reading as
# "not provisional".
HEIGHT_VS_TOLL_PROVISIONAL_FIELDS = (
    "provisional", "provisional_reason", "edge_n_ranges",
    "min_n_ranges_pinned", "edge_min_n_ranges_pinned")

# ── THE VERDICT ROW'S ASSET IS DERIVED FROM THE BOOK, NEVER DEFAULTED ──────
# [review round 2, 2026-09-22, finding 1]  `brk_row` used to read
#     asset = str(verdict_asset) if verdict_asset else "POOLED:CLASSIC5"
# and `verdict_asset` was never derived from anything: it was a caller
# argument, a literal, a docstring and a pass-through.  So a row built on ANY
# book silently received POOLED:CLASSIC5's census figures under its own
# panel's name.  REPRODUCED before the fix, on the real filed tables: a
# one-asset BTCUSDT book (panel_name CUSTOM1:19aa16ae) took POOLED:CLASSIC5's
# 1d row — n_ranges 53, ratio_median 413.99176955, verdict_pass TRUE, reason
# 'height gate PASS + edge-fade leg PASS' — while BTCUSDT's OWN 1d row is
# n_ranges 11, verdict_pass False and PROVISIONAL.  The harm landed on the
# most favourable side, with no HALT and no note on the row.
# R8 makes the BRK panel of record CLASSIC5, which makes that default LOOK
# right today and is exactly why it must still be DERIVED: the Tier-E 17-asset
# row R8 also orders must not silently wear CLASSIC5's verdict.
CENSUS_ASSET_OF_PANEL = {"CLASSIC5": "POOLED:CLASSIC5",
                         "UNSEEN12": "POOLED:UNSEEN12"}
CENSUS_POOL_LABELS = ("POOLED:ALL", "POOLED:CLASSIC5", "POOLED:UNSEEN12")
VERDICT_ASSET_LAW = (
    "THE VERDICT ROW'S ASSET IS DERIVED FROM THE BOOK'S PANEL, NEVER "
    "DEFAULTED. TP.panel_name(book.spec['panel']) -> the census's own label: "
    "CLASSIC5 -> POOLED:CLASSIC5, UNSEEN12 -> POOLED:UNSEEN12, a one-asset "
    "panel -> that symbol's own census row. A panel the census files no "
    "counterpart for HALTs, naming the panel and the labels the census does "
    "carry. PANEL17 has NO counterpart today: the census's POOLED:ALL is the "
    "CENSUS COMMISSION's pool and nothing filed proves its membership is this "
    "panel's, so mapping PANEL17 onto it would be the same assumption in a "
    "new coat. `verdict_asset=` remains as an EXPLICIT OVERRIDE only, and an "
    "override that disagrees with the derived label HALTs unless the caller "
    "states `verdict_asset_why=`. The choice and its provenance ride the row "
    "as `height_vs_toll_asset` and print on it.")



# ── WHAT "NET OF MEASURED 5m TOLL" ACTUALLY DOES TODAY, SAID ON THE ROW ──────
# REPORTED, NOT CHANGED.  The contract calls P-BRK-S1's result "NET OF
# MEASURED 5m TOLL"; `account_l` books fee and funding and subtracts NEITHER
# the grid toll nor anything derived from it, and `stamp_toll`'s own docstring
# says so verbatim ("as a PRINT beside the book").  Turning the print into a
# DEDUCTION is a contract reading with a UNIT question inside it, so it is the
# operator's to settle and not an executor's to perform.  The reading rides on
# every row so nobody has to reconstruct it from two docstrings.
TOLL_ACCOUNTING = {
    "status": ("PRINT, NOT A DEDUCTION — reported, not changed. The contract "
               "reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE "
               "and FUNDING only."),
    "net_r_formula": ("account_l: net_r = gross_r - fee_r - funding_r_eff, "
                      "all in R units (divided by r_dist). fee_r is the "
                      "estate's FEE_BPS_SIDE a side on both legs; "
                      "funding_r_eff is the interval sum under the card's 1R "
                      "ceiling [B4]."),
    "grid_toll": ("stamp_toll stamps toll_atr_grid (the census grid's median "
                  "round-trip toll for this lane's event class, in ATR of "
                  "the lens) and toll_pct_of_1r = toll_atr / (r_dist / "
                  "atr_at_entry) x 100, BESIDE the book. Neither ever enters "
                  "net_r."),
    "unit_question": ("toll_atr is a CENSUS-MEASURED MEDIAN over a class's "
                      "anchors, in ATR units, not this campaign's own cost; "
                      "net_r is in R units. toll_pct_of_1r already converts "
                      "it (R and ATR are both known at the entry bar), so "
                      "net_r - toll_pct_of_1r/100 is dimensionally legal. "
                      "What is NOT obvious is whether it is MEANT: the fee "
                      "leg of the same round trip is ALREADY inside net_r "
                      "via fee_r, and the census toll is built from the "
                      "filed fee schedule (toll_bps_source = "
                      "data/fee_schedule.json[...].round_trip_bps_used), so "
                      "a subtraction would charge the spread/fee twice for "
                      "any asset whose grid toll is fee-derived."),
    "what_a_deduction_would_take": (
        "one line in account_l (or a wrapper on its return) subtracting "
        "toll_pct_of_1r/100 from net_r, plus a decision on the double-count "
        "above, plus a re-reading of MISMATCH: I1's text says 'net of 10 bps "
        "+ funding' and S1's says 'NET OF MEASURED 5m TOLL' and does not "
        "mention funding at all."),
    "authority": ("a CONTRACT READING. Not changed on executor authority; "
                  "the operator settles it. Until then the toll is printed "
                  "on every row, labelled, and the row says it is a print."),
}


def as_of_of_record(path: Path | None = None) -> str:
    """THE AS-OF WARRANTY'S VALUE — Stage D's WRITE-ONCE pin, read, never
    restated.  Every row this module files carries it.

    HALTS IF: the pin is absent or carries no `as_of_last_closed_4h`.  A row
    with an invented as-of is a row whose numbers are true of no bars."""
    p = Path(path) if path is not None else TP.AS_OF_PIN
    if not p.exists():
        raise SystemExit(
            f"HALT: no Stage D as-of pin at {p}; every BRK artifact carries "
            f"as_of_last_closed_4h and this module does not invent one.")
    v = json.loads(p.read_text()).get("as_of_last_closed_4h")
    if not v:
        raise SystemExit(f"HALT: {p} carries no 'as_of_last_closed_4h'.")
    return str(v)

FEE_BPS_SIDE = RC.FEE_BPS_SIDE      # 5.0, BY OBJECT — never a literal here
FUNDING_CEILING_R = RC.FUNDING_CEILING_R
ATR_LEN = RC.ATR_LEN
MIN_STOP_ATR = RC.MIN_STOP_ATR      # the rail, 1.0 ATR of the lens
STOP_BUF_ATR = RC.STOP_BUF_ATR      # the card's word for "beyond"

RULINGS = (
    'R1 (verbatim): "Let\'s try the 89/127 ribbon, the 127/200 ribbon, and '
    'taps on each ema. Feel free to search data from past runs to tune the '
    'defaults" -> the five bands in R1_BANDS; (band, margin_atr, hold_bars) '
    'come from the census builder\'s TUNING_RESULT file FOR THE LENS at run '
    'time (5m = the scored arm, 1d = the Tier-E print), never from this file.',
    'R2 (verbatim, 2026-09-21): "All 17" -> PANEL17 for both lanes. '
    'SUPERSEDED by R8 (below) on the operator\'s own word; the era half of '
    'the reading stands — P-BRK-S1 is scored on the HOLDOUT era only, '
    'P-BRK-I1 rides the full corridor, and require_lane_era now ENFORCES '
    'both against the filed arm [B9].',
    'R8 (verbatim, 2026-09-22): "5-asset book - the PANEL PIN governs" -> '
    'P-BRK-S1 and P-BRK-I1 score on CLASSIC5 (LOAO above-half = 3/5); the '
    '17-asset view prints as Tier-E beside each BRK row. This module scores '
    'on whatever panel the REGISTRATION names (g["panel"]), so R8 is a '
    'registration-text decision and no code changed for it; what changed is '
    'the DECLARATION (PANEL_DECLARED) and the row\'s tier_e_panel17 slot.',
    'R4 (verbatim): "It means we observe the transition from expansion of the '
    'bands, into consolidation and closing of the bands. This is followed by '
    'new expansion, either as continuation or as reversal, a final cross after '
    'the interweaving of the ema turns to expanding the ribbon between the '
    "ema's\" -> ribbon_lifecycle(); DIRECTION = sign(s) while EXPANDING.",
)

LEANS = (
    f"{LEAN_TAG} L1 1d = six complete native-4h bars; 1w = Monday complete "
    f"weeks.  Both lenses arrive from the Stage D derived files; 5m arrives "
    f"through the Stage D AS_OF cut (D.load_asof), never through a loader that "
    f"reads past the pin.",
    f"{LEAN_TAG} L2 registered lanes and Stage-A stamps use FROZEN SCALE "
    f"{FROZEN_SCALE}; the census prints the calibrated scale beside.",
    f"{LEAN_TAG} L4 H20/H100 = bars of the lens, censored, anchored at the "
    f"known_at close — the same known_at this module enters on.",
    f"{LEAN_TAG} L6 CLASSIC5 / UNSEEN12 / PANEL17; LOAO above-half = strict "
    f"majority (3/5, 7/12, 9/17).",
    f"{LEAN_TAG} L8 seed {SEED} with the sensitivity echo {SEED_LINEAGE}.",
    f"{LEAN_TAG} B1 a component's WARMTH is decided ONCE, at the entry bar, "
    f"and holds for the campaign; an inactive component is counted per "
    f"campaign and printed, never imputed and never switched on mid-ride.",
    f"{LEAN_TAG} B2 the BRK 12/{RIBBON_SLOW} bell is tested LAST, so a v6 exit "
    f"label wins whenever two bells ring on the same bar.",
    f"{LEAN_TAG} B3 EXPANDING reads the window s[t-K .. t] (K+1 samples, K "
    f"steps), K = {LIFECYCLE_K}; the ruling's comparison is against t-K.",
    f"{LEAN_TAG} B4 interval-sum funding prices each stamp at the close of the "
    f"last lens bar CLOSED at or before it; on 4h that reproduces the "
    f"lineage's rate x c[j-1] exactly, bar for bar.",
    f"{LEAN_TAG} B5 candidacy = (die_i, min(die_i + {MEM_TTL_BARS}, "
    f"next_die_i - 1, n - 1)], the census builder's window, applied to BOTH "
    f"anchors — over DIEs detected on the FULL tape, while the R1 tuning "
    f"detected its own on tapes CUT at the era boundary; the two agree ONLY "
    f"because the macro detector is as-of, which F-BRK-ERA proves rather than "
    f"assumes (BTCUSDT 1d: 7 of 10 dies below the cut, identical; BTCUSDT 5m: "
    f"1839 of 2832, identical).",
    f"{LEAN_TAG} B6 the era is the PANEL MODULE's object (TP.in_era on "
    f"entry_ms, cut {ERA_CUT_ISO}); this module tests it at the replay so a "
    f"tuning-era entry HALTs instead of being refused later by external_book.  "
    f"entry_ms is the entry bar's OPEN and R1 states the era in CLOSE time: "
    f"for a bar straddling the cut this REFUSES what R1 would allow and never "
    f"the reverse — the conservative side, named (FINDINGS, mismatch 4).",
    f"{LEAN_TAG} B7 every permission is read AT the entry bar, from bars "
    f"CLOSED at that instant.",
    f"{LEAN_TAG} B9 LANE_ERA IS ENFORCED, NOT MERELY DECLARED.  "
    f"require_lane_era compares LANE_ERA[lane] to the era of the FILED ARM "
    f"(gate()['era']) inside BOTH runners, immediately after the gate and "
    f"BEFORE corridor_era or frame_l — so a P-BRK-S1 arm filed at era='full' "
    f"HALTs without one bar or one bar-stamp being read.  The alternative — "
    f"NARROWING a 'full' arm's window to the holdout — is NOT taken: a runner "
    f"that silently rides a window its registration does not name has made "
    f"the registration text stop meaning anything.  The registration is "
    f"refiled, or the lane does not ride.",
    f"{LEAN_TAG} B10 THE ROW CARRIES ITS VERDICT; IT DOES NOT COMPUTE ONE.  "
    f"The height-vs-toll figures are the CENSUS track's [Q-R3] measurement "
    f"and are READ through height_vs_toll() from "
    f"{HEIGHT_VS_TOLL_PATH.name} under key {list(HEIGHT_VS_TOLL_KEY)} with "
    f"fields {list(HEIGHT_VS_TOLL_FIELDS)}, and the verdict from "
    f"{HEIGHT_VS_TOLL_VERDICT_PATH.name} under key "
    f"{list(HEIGHT_VS_TOLL_VERDICT_KEY)} with fields "
    f"{list(HEIGHT_VS_TOLL_VERDICT_FIELDS)}; this module pins no verdict "
    f"vocabulary and files no default.  Until [Q-R3] exists the slot holds a "
    f"PendingVerdict whose every read — str, repr, format, float, bool, len, "
    f"iteration, indexing, EQUALITY AND ORDERING, json.dumps(default=str) — "
    f"raises SystemExit, so a row with an unread verdict cannot be printed, "
    f"filed, or silently compared to a string.  The scale read "
    f"is {HEIGHT_VS_TOLL_SCALE!r} (the frozen pin of record [L2]; "
    f"'calibrated' is in-sample by construction and may not reach a scored "
    f"lane's row) and the era read is {HEIGHT_VS_TOLL_ERA!r}.  WHICH ROW is "
    f"read is DERIVED, see H4.",
    f"{LEAN_TAG} H4 THE VERDICT ROW'S ASSET IS DERIVED FROM THE BOOK, NEVER "
    f"DEFAULTED.  {VERDICT_ASSET_LAW}  The shipped defect it replaces: "
    f"`asset = str(verdict_asset) if verdict_asset else \"POOLED:CLASSIC5\"` "
    f"with `verdict_asset` derived from nothing, so a one-asset BTCUSDT book "
    f"took POOLED:CLASSIC5's 1d row (n_ranges 53, ratio_median 413.99176955, "
    f"verdict_pass TRUE) instead of BTCUSDT's own (n_ranges 11, verdict_pass "
    f"False, PROVISIONAL) — the harm on the most favourable side, with no "
    f"HALT and no note.  R8 makes CLASSIC5 the BRK panel of record, which "
    f"makes that default LOOK right today and is exactly why it is derived "
    f"and not assumed: the Tier-E 17-asset row R8 also orders must never "
    f"silently wear CLASSIC5's verdict.",
    f"{LEAN_TAG} H5 THE CENSUS'S SAMPLE FLOOR IS HONOURED ACROSS THE TRACK "
    f"BOUNDARY, AND ITS NUMBER IS NOT COPIED.  [Q-R3] was re-filed with a "
    f"`provisional` flag, an `edge_n_ranges` column and a minimum-n floor; "
    f"the census's own reader refuses a flagged row to a caller that did not "
    f"ask for it by name, and this module reads the PARQUET DIRECTLY, so it "
    f"would have bypassed that refusal entirely.  height_vs_toll() now HALTs "
    f"on a provisional row unless allow_provisional=True, and a row taken by "
    f"name carries provisional / provisional_reason / sample_floor and PRINTS "
    f"them in a starred block.  The floor itself is READ off the census row "
    f"({list(HEIGHT_VS_TOLL_PROVISIONAL_FIELDS)}) and never re-pinned here — "
    f"a second copy of another track's threshold is a threshold that can "
    f"drift in silence.",
    f"{LEAN_TAG} H1 THE [Q-R3] READ IS A TWO-TABLE JOIN, KEYED DIFFERENTLY "
    f"ON EACH SIDE.  The census filed its FIGURES with an `era` column and "
    f"its VERDICT without one, so the figures are selected on "
    f"{list(HEIGHT_VS_TOLL_KEY)} and the verdict on "
    f"{list(HEIGHT_VS_TOLL_VERDICT_KEY)}.  Nothing in that join proves the "
    f"two rows are one measurement, so the columns BOTH tables carry "
    f"({list(HEIGHT_VS_TOLL_AGREE)}, plus the law half "
    f"{list(HEIGHT_VS_TOLL_AGREE_STR)}) are compared and any disagreement "
    f"HALTs.  AN ABSENT SHARED COLUMN IS ALSO A HALT, NOT A SKIP [review "
    f"round 2, finding 2].  It used to `continue`, and those columns were "
    f"not required of the verdict table, so a verdict table re-filed without "
    f"them passed every column check, the cross-check compared NOTHING, and "
    f"`cross_checked` still attested all three from the constant — an "
    f"attestation for a check that never ran.  Reproduced on the two REAL "
    f"filed tables: drop n_ranges / height_atr_median / toll_atr_median from "
    f"the verdict copy and flip 5m POOLED:CLASSIC5 to verdict_pass=True with "
    f"reason 'INVENTED', and the reader returned it.  TWO GUARDS NOW: the "
    f"shared columns are REQUIRED of the verdict side (_hvt_required), and "
    f"`cross_checked` is the list the comparison ACTUALLY built, so the "
    f"attestation cannot outrun the check.  The alternative — asking the "
    f"census for an era column on the verdict table, or for a single joined "
    f"table — was NOT taken: it is another track's file, the cross-check is "
    f"cheap and real, and the figures agree today (13025 / 6.480873 / "
    f"0.292654 on both sides for 5m POOLED:CLASSIC5).",
    f"{LEAN_TAG} H2 THE CENSUS'S VERDICT IS CARRIED AS THREE FIELDS, NOT "
    f"FLATTENED TO A STRING.  [Q-R3] files verdict_pass (bool) + verdict_law "
    f"+ reason, not the single verdict string the last round's interface "
    f"guessed at.  All three ride the row verbatim rather than being "
    f"collapsed into a word of this module's choosing — collapsing them "
    f"would be exactly the verdict vocabulary B10 refuses to pin.  "
    f"verdict_pass must be an actual boolean and verdict_law/reason must be "
    f"non-blank, or the read HALTs.",
    f"{LEAN_TAG} H3 THE AS-OF WARRANTY IS ENFORCED ACROSS THE TRACK "
    f"BOUNDARY.  Both filed census tables carry "
    f"{HEIGHT_VS_TOLL_ASOF_COL!r}; height_vs_toll() requires that column on "
    f"both and HALTs unless it equals this corridor's as-of.  A census "
    f"measurement re-filed after the corridor moves therefore cannot ride a "
    f"BRK row silently — it stops the read instead.",
    f"{LEAN_TAG} B11 THE ROW COMPUTES NO REGISTRATION VERDICT EITHER.  "
    f"brk_row carries the Book, its gate, the counts and the journal's own "
    f"per-campaign sums; the ruler, the LOAO line and the p against the FDR "
    f"bar stay tierc10_panel's (TP.score / TP.headline_n).  A row can only be "
    f"assembled from a TP.Book — the journal WEARING its gate — so a row "
    f"without a filed registration behind it cannot be built at all, which "
    f"is the state of the estate today [LAW 4].",
    f"{LEAN_TAG} B8 one object, two house styles: the operator's band names "
    f"({BAND_EXAMPLE}) and the census's ({census_band(BAND_EXAMPLE)}) are "
    f"translated at the boundary by band_key/census_band, which are algebra "
    f"over R1_BANDS and cannot name a sixth band; the tuned band and the toll "
    f"class both travel through them, and both directions are checked against "
    f"the FILED census artifacts on every fixture run.",
)

FINDINGS = (
    "MISMATCH 1 (reported, not silently reconciled): the census builder's "
    "`retest_holds` ends candidacy at min(die_i + MEM_TTL_BARS, next_die - 1, "
    "n - 1) FROM THE DIE.  The engine's leash, which produces the memory-line "
    "flips this module's I1 anchor consumes, applies MEM_TTL_BARS per LINE "
    "from that line's own death and caps the lines at MEM_CAP_PER_SIDE per "
    "side, and never truncates at the next macro DIE.  They are NOT the same "
    "object.  This module applies the census window ON TOP of whatever the "
    "leash emitted [B5], so the band anchor matches the census exactly and the "
    "memory anchor is the leash's event INTERSECTED with the census window.  "
    "Both counts are carried on every candidate list.",
    "MISMATCH 2: `engine.cells.INTERVAL_MS` has no '1d' or '1w' key, so "
    "`engine.htf.map_htf_to_exec` cannot map a weekly bar onto a daily one.  "
    "`visible_htf_idx` re-states the identical law with the step in ms and is "
    "proved equal to the engine's on 4h (F-BRK-PERM).  engine/cells.py is NOT "
    "edited — it is a frozen file and not this task's to touch.",
    "MISMATCH 3 — CLOSED, AND THE OLD TEXT WAS WRONG.  This finding used to "
    "say the census grid carried the foundations' PROVISIONAL retest-hold "
    "classes (`retest-hold-ema89`, `retest-hold-ema200_300`).  IT DOES NOT: "
    "the filed grid carries the five R1 classes, spelled "
    "`retest-hold-ribbon89_127 / ribbon127_200 / tap89 / tap127 / tap200`.  "
    "What was actually broken was a SPELLING, in this module: this file "
    "writes the operator's `ribbon-127/200` and the census writes "
    "`ribbon127_200`, so `tuned_pins` refused the census's own filed result "
    "and `toll_class` asked the grid for a row that has never existed in it.  "
    "Both are now translated at the boundary by `band_key` / `census_band` "
    "(the spelling law, §THE FIVE R1 BANDS) and both directions are fixture-"
    "checked against the FILED artifacts, not against a synthetic copy of "
    "them.  Neither module's house style was changed; nothing was loosened.",
    "MISMATCH 4 (reported, not fixed): the R1 era rule is stated in CLOSE "
    "time ('bars with close time <= 2024-06-30T23:59:59Z') and every era test "
    "in the estate — `TP.in_era` at this module's `require_era` [B6] and "
    "again at `external_book`'s door — is applied to a campaign's `entry_ms`, "
    "which is the entry bar's OPEN.  The two can only disagree for a bar that "
    "STRADDLES the cut, and the disagreement is in the strict direction: such "
    "a bar is holdout by R1's clock and tuning by the entry stamp, so it "
    "would be REFUSED, never admitted.  Measured today: `corridor_era(panel, "
    "'holdout')` opens at 2024-07-01T00:00:00Z on CLASSIC5, UNSEEN12 and "
    "PANEL17 alike, "
    "so no bar of any lens straddles the cut inside a holdout window and no "
    "legal entry is refused.  One law, one object, one direction of error — "
    "but the direction is now named rather than implied.",
    "OPEN (THE TOLL IS A PRINT, NOT A DEDUCTION) — reported, not changed, "
    "and NOT an executor's to change.  The contract calls P-BRK-S1's result "
    "'NET OF MEASURED 5m TOLL'.  `account_l` returns net_r = gross_r - fee_r "
    "- funding_r_eff and SUBTRACTS NO TOLL; `stamp_toll` stamps "
    "`toll_atr_grid` and `toll_pct_of_1r` BESIDE the book and its own "
    "docstring says so ('as a PRINT beside the book').  A deduction is "
    "dimensionally legal — toll_pct_of_1r already converts the grid's "
    "ATR-unit median into a share of 1R at the entry bar — but it may DOUBLE "
    "COUNT: the census toll is built from the filed fee schedule "
    "(toll_bps_source = data/fee_schedule.json[...].round_trip_bps_used) and "
    "the same round trip's fee is ALREADY inside net_r via fee_r.  It is "
    "also a MEDIAN OVER A CLASS, not this campaign's cost.  The whole "
    "reading rides on every row as TOLL_ACCOUNTING; the operator settles it.",
    "THE DRAFTING ERROR IN THE RESUME PASTE (reported, nothing built on it).  "
    "The contract's P-BRK-S1 line reads 'first HOLD retest of the 5m 89 or "
    "200/300 band (FLIP_HOLD pins)'.  BOTH halves name the wrong objects.  "
    "(a) FLIP_HOLD (FLIP_HOLD_MARGIN 1.0 ATR / FLIP_HOLD_BARS 6 bars, read "
    "out of engine/rangefinder.py) is the MEMORY-LINE pin set — P-BRK-I1's "
    "anchor — and is not P-BRK-S1's.  (b) '89 or 200/300' is the FOUNDATIONS' "
    "provisional band pair; the band set actually built and tuned under "
    "operator ruling R1 is the five {ribbon89_127, ribbon127_200, tap89, "
    "tap127, tap200}, and the 5m cell the census TUNED and FILED is band "
    "'ribbon127_200' at margin_atr 1.0 / hold_bars 3 / ttl_bars 400 "
    "(census/TUNING_RESULT.json).  The 1d Tier-E cell is a DIFFERENT one: "
    "band 'ribbon89_127' at margin_atr 0.25 / hold_bars 6 / ttl_bars 400 "
    "(census/TUNING_RESULT_1d.json).  No registration text may quote the "
    "contract's wording; the pins are READ from the tuning file at run time "
    "(tuned_pins) and never typed.",
    "OPEN: P-BRK-S1's contract text says 'NET OF MEASURED 5m TOLL' and does "
    "not mention funding; P-BRK-I1 says 'net of 10 bps + funding'.  The estate "
    "default is that every book pays journaled funding, so both lanes do here, "
    "and S1 additionally PRINTS toll-as-%-of-1R from the filed grid.  If the "
    "operator means the scalper to pay no funding, `account_l` takes the "
    "funding rows as an argument and an empty table is the whole change.",
)


# ═════════════════════════════════════════════════ 0 · THE SUBSTRATE, PROVEN
def substrate() -> dict:
    """The frozen snapshot, proved before one bar is read — `TP.substrate`'s
    guard, entered through this module's own door so that a caller who never
    touches the panel module still cannot read the live cache."""
    return TP.substrate()


if set(LANE_ERA.values()) - set(ERAS):
    raise SystemExit(f"HALT: LANE_ERA names {sorted(set(LANE_ERA.values()))}; "
                     f"the panel module publishes {ERAS}.")


# ═════════════════════════════════════════ 1 · THE LENS FRAME, KEYED (sym, lens)
_UID = itertools.count(1)           # one id per LensFrame ever built


@dataclass
class LensFrame:
    """Everything a lens-scaled ride can see on ONE lens of ONE asset.

    It is `tierc2_rules.Frame4h` with the lens in the object rather than in the
    name, and with the funding table carried beside the bars because the
    interval-sum accounting reads stamps, not bar opens.

    THE ARRAYS ARE BUILT OVER THE FULL LOADED HISTORY and only then windowed,
    exactly as the lineage does, so that a corridor edge can never move an EMA,
    an anchor or a trail.
    """
    sym: str
    lens: str
    open_ms: np.ndarray
    o: np.ndarray
    h: np.ndarray
    l: np.ndarray
    c: np.ndarray
    atr: np.ndarray
    step_ms: int
    fund_hour_ms: np.ndarray        # int64, sorted, one row per funding stamp
    fund_rate: np.ndarray           # float
    # THE MEMO KEY, AND WHY IT IS AN OBJECT COUNTER AND NOT (sym, lens).
    # Role arrays, fractals and anchor series are memoised per frame.  Keyed on
    # (sym, lens) they would be served to ANY frame wearing that name — and a
    # caller can build two: a fixture's up-tape and down-tape under one
    # synthetic symbol, a lens rebuilt after a reload.  The second frame would
    # then read the FIRST one's EMAs against its OWN closes, which is the
    # F-C8-MATCH poisoned-cache lesson wearing new clothes.  Measured: a
    # falling 4h tape built second under the same name returned tide 0 instead
    # of -1, because `e89 > e316` came from the rising tape.  Caught by
    # F-BRK-LANE-SYN, not by eye.  A per-instance id makes the memo exact:
    # `frame_l` still builds one frame per (sym, lens), so nothing is
    # recomputed that was not recomputed before.
    uid: int = dataclasses.field(default_factory=lambda: next(_UID))

    @property
    def n(self) -> int:
        return int(len(self.c))

    @property
    def key(self) -> tuple:
        """This frame's identity for a memo: the name AND the object."""
        return (self.sym, self.lens, self.uid)

    @property
    def close_ms(self) -> np.ndarray:
        """The bar CLOSE instants — what an as-of stamp and an era test read."""
        return self.open_ms + self.step_ms


_FRAMES: dict[tuple, LensFrame] = {}
_ROLES: dict[tuple, dict] = {}
_FRACTALS: dict[tuple, object] = {}
_ANCHORS: dict[tuple, dict] = {}


def _funding_arrays(sym: str) -> tuple:
    """The funding stamps, hour-keyed and summed — the SAME table
    `tierc2_baseline.load_funding` builds, read through the Stage D door so the
    as-of cut and the 60 s jitter guard ride with it."""
    fd = D.load_funding_asof(sym)
    if len(fd) == 0:
        raise SystemExit(f"HALT: {sym} has no funding stamps at the as-of; a "
                         f"book that pays journaled funding cannot ride it.")
    g = fd.groupby("funding_hour_ms", sort=True)["funding_rate"].sum()
    return (g.index.to_numpy(np.int64), g.to_numpy(float))


def frame_l(sym: str, lens: str, with_funding: bool = True) -> LensFrame:
    """ONE asset, ONE lens, built once — AND THE LENS IS IN THE KEY.

    WHAT WOULD MAKE THIS WRONG: memoising on the bare symbol (a 5m frame would
    be served to the 4h card — the F-C8-MATCH poisoned-cache lesson), or
    building the 1d/1w tape from anything but the Stage D derived file (the
    twin's law L1 is what the F-RF fixtures ride, and a second derivation would
    be a second law).
    """
    substrate()
    if lens not in LENS_MS:
        raise SystemExit(f"HALT: unknown lens {lens!r}; Stage D publishes "
                         f"{sorted(LENS_MS)}.")
    key = (sym, lens, bool(with_funding))
    if key in _FRAMES:
        return _FRAMES[key]
    k = D.load_asof(sym, lens)
    om = k["open_time"].to_numpy(np.int64)
    step = int(LENS_MS[lens])
    dif = np.diff(om)
    if len(dif) and (int(dif.min()) < step or np.any(dif % step)):
        raise SystemExit(f"HALT: {sym} {lens} is not on its own grid "
                         f"(min gap {int(dif.min()) if len(dif) else 0} ms, "
                         f"step {step}) — a foreign lens or a spliced tape.")
    h = k["high"].to_numpy(float)
    l = k["low"].to_numpy(float)
    c = k["close"].to_numpy(float)
    fh, fr = (_funding_arrays(sym) if with_funding
              else (np.zeros(0, np.int64), np.zeros(0, float)))
    lf = LensFrame(sym=sym, lens=lens, open_ms=om,
                   o=k["open"].to_numpy(float), h=h, l=l, c=c,
                   atr=ind.atr(h, l, c, ATR_LEN), step_ms=step,
                   fund_hour_ms=fh, fund_rate=fr)
    _FRAMES[key] = lf
    return lf


def roles_l(lf: LensFrame, roles, ribbon: tuple | None = None) -> dict:
    """`tierc9.role_arrays` on the lens — six role EMAs, their crosses, and
    (when the lane asks) the 12/25 ribbon the BRK bell reads [R4].

    Built with the ENGINE's `ind.ema` on the lens's own closes, so under v6
    periods on the 4h lens each array is bit-identical to its e12/e26/e89/e316
    twin and F-BRK-RIDE-4H can demand exact zero.

    WHAT WOULD MAKE THIS WRONG: caching on the NAME rather than on the FRAME
    (see `LensFrame.uid` — two tapes under one symbol, and the second reads the
    first's EMAs), dropping the roles from the key (a swept cell would read the
    incumbent's arrays), or reading a period through another role's array (the
    aliasing `tierc9` exists to remove).
    """
    key = lf.key + (roles.periods, tuple(ribbon) if ribbon else None)
    if key in _ROLES:
        return _ROLES[key]
    c = lf.c
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
    if ribbon:
        rf, rs = int(ribbon[0]), int(ribbon[1])
        a["rib_f"], a["rib_s"] = ind.ema(c, rf), ind.ema(c, rs)
        a["r_up"] = ind.crossover(a["rib_f"], a["rib_s"])
        a["r_dn"] = ind.crossunder(a["rib_f"], a["rib_s"])
        a["ribbon"] = (rf, rs)
    _ROLES[key] = a
    return a


def fractals_l(lf: LensFrame, L: int, R: int):
    """The confirmed (L,R) fractals of the lens — `RC.build_fractals`, keyed
    (sym, lens, L, R)."""
    key = lf.key + (int(L), int(R))
    if key not in _FRACTALS:
        _FRACTALS[key] = RC.build_fractals(lf.h, lf.l, int(L), int(R))
    return _FRACTALS[key]


def anchor_series_l(lf: LensFrame) -> dict:
    """`tierc8.anchor_series` on the lens — warm-up FLOORED, one pass per
    (sym, lens).  Only the non-pivot anchors read it; the card's own anchor is
    the pivot, so under v6 this dict is built and never consulted.  It is built
    anyway, because a runner that silently had no `s` to pass would be a
    runner that could not ride a non-pivot card at all."""
    key = lf.key
    if key in _ANCHORS:
        return _ANCHORS[key]
    c = lf.c
    idx = np.arange(len(c))
    e26 = np.where(idx >= 26, ind.ema(c, 26), np.nan)
    e89 = np.where(idx >= 89, ind.ema(c, 89), np.nan)
    m_lo, m_hi = RC.ribbon_band(c, "M")
    warm = idx >= max(RC.RIBBONS["M"])
    _ANCHORS[key] = {"e26": e26, "e89": e89,
                     "m_lo": np.where(warm, m_lo, np.nan),
                     "m_hi": np.where(warm, m_hi, np.nan)}
    return _ANCHORS[key]


def idx_range(open_ms: np.ndarray, lo_ms: int, hi_ms: int) -> tuple:
    """[lo_i, hi_i] of the bars whose OPEN lies in [lo_ms, hi_ms] — the
    lineage's `tierc7._idx_range`, by object, so a window means the same thing
    on every lens."""
    return T7._idx_range(open_ms, int(lo_ms), int(hi_ms))


# ══════════════════════════════════ 2 · WARMTH — THE INACTIVE COMPONENTS [R4]
COMPONENTS = ("bell_window", "bell_tide", "harvest", "bell_ribbon", "trail")


def component_periods(roles, ribbon: tuple | None) -> dict:
    """Which EMAs each managed component reads.  The trail reads no EMA at all
    — it is the (2,2) fractal clock — so it is never inactive for want of
    warm-up and says so with an empty tuple."""
    return {
        "bell_window": (roles.win_f, roles.win_s),
        "bell_tide": (roles.tide_f, roles.tide_s),
        "harvest": (roles.tide_f, roles.tide_s),
        "bell_ribbon": (tuple(ribbon) if ribbon else ()),
        "trail": (),
    }


def warm_components(entry_i: int, roles, ribbon: tuple | None,
                    active: tuple = COMPONENTS) -> dict:
    """[LEAN-HEPHAESTUS B1] WHICH COMPONENTS ARE WARM AT THE ENTRY BAR.

    The lineage's warm-up law, unchanged: `ind.ema` seeds at the series start
    and never returns NaN, so an EMA of period p is READABLE from bar p and not
    before (`tierc8.anchor_series` floors exactly this way, and a band is
    floored at its LONGEST member because a band is not defined while only some
    of its members are warm).

    Returns {component: bool}.  A component absent from `active` is False and
    is reported as `off` rather than `cold` by `inactive_note`, because "the
    card does not carry it" and "the lens cannot warm it" are different facts
    and a count that merged them would lie.

    WHAT WOULD MAKE THIS WRONG: imputing a cold EMA with a seeded value (the
    defect this estate has repaired four times), or deciding warmth per bar so
    that a campaign's own count could not be stated.
    """
    per = component_periods(roles, ribbon)
    out = {}
    for name in COMPONENTS:
        if name not in active:
            out[name] = False
            continue
        p = per[name]
        out[name] = bool(int(entry_i) >= (max(p) if p else 0))
    return out


def inactive_note(warm: dict, active: tuple = COMPONENTS) -> tuple:
    """The campaign's INACTIVE components, named — `('harvest:cold',
    'bell_ribbon:off')` — so the printed count can never be a bare integer
    whose reason has been lost."""
    out = []
    for name in COMPONENTS:
        if warm.get(name):
            continue
        out.append(f"{name}:" + ("cold" if name in active else "off"))
    return tuple(out)


# ═══════════════════════════════ 3 · THE RIDE, LENS-PARAMETERISED [R4 / tierc9]
def ride_leg_l(lf: LensFrame, card, roles, d: int, ti: int, entry_px: float,
               stop0: float, r_dist: float, hi_i: int,
               ribbon: tuple | None = None,
               active: tuple = COMPONENTS) -> dict:
    """`tierc9._ride_leg9`, TRANSCRIBED ONTO THE LENS.  Same periods, same
    pins, same within-bar order, same arithmetic:

        STOP -> BELL -> HARVEST -> TRAIL, adverse-first, the stop fills AT the
        stop, the trail governs the NEXT bar.

    The only three differences, each demanded by the ruling and each visible in
    the returned record:
      · every array read is the LENS's (`lf`, `roles_l`, `fractals_l`);
      · a component COLD at the entry bar is INACTIVE for the campaign [B1] —
        it is skipped, never imputed, and named in `inactive`;
      · when `ribbon` is given the bell ALSO rings on the lens's counter 12/25
        cross, tested LAST so a v6 label wins a tie [B2, R4].

    WHAT WOULD MAKE THIS WRONG: reordering the within-bar checks (F-BRK-RIDE-4H
    would go red), testing the stop against the bar that created it, booking a
    harvest on a bar the stop already closed, or applying a trail advance to
    its own bar.
    """
    ra = roles_l(lf, roles, ribbon)
    fr = fractals_l(lf, card.trail_l, card.trail_r) if card.trail else None
    s = anchor_series_l(lf)
    f = lf
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
    warm = warm_components(ti, roles, ribbon, active)
    bell_w = f"bell_{roles.win_f}_{roles.win_s}"
    bell_t = f"bell_{roles.tide_f}_{roles.tide_s}"
    bell_r = (f"bell_{ribbon[0]}_{ribbon[1]}" if ribbon else "")
    do_harvest = bool(card.harvest == "band" and warm["harvest"])
    do_bw, do_bt = bool(warm["bell_window"]), bool(warm["bell_tide"])
    do_br = bool(ribbon and warm["bell_ribbon"])
    do_trail = bool(card.trail and warm["trail"])
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

        if do_harvest:
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
        if d == 1:
            bell = (bell_w if (do_bw and bool(ra["w_dn"][j]))
                    else bell_t if (do_bt and bool(ra["b_dn"][j]))
                    else bell_r if (do_br and bool(ra["r_dn"][j])) else None)
        else:
            bell = (bell_w if (do_bw and bool(ra["w_up"][j]))
                    else bell_t if (do_bt and bool(ra["b_up"][j]))
                    else bell_r if (do_br and bool(ra["r_up"][j])) else None)
        if bell:
            exit_i, exit_px, exit_reason = j, float(f.c[j]), bell
            if touch:
                blocked = "bell"
            break
        if touch:
            harv = (j, RC.harvest_fill_px(f.c[j]),
                    (RC.harvest_fill_px(f.c[j]) - entry_px) * d / R)
        if do_trail and trail_armed:
            adv, opp = T8.matched_step(fr, j, d, stop, float(f.c[j]),
                                       float(f.atr[j]), s, card.anchor_kind,
                                       card.anchor_offset, f.open_ms,
                                       min_advance_atr=card.trail_min_advance_atr)
            n_opp += int(opp)
            if adv is not None:
                advances.append(adv)
                stop = float(adv.new_stop)
    return {"own_r": abs(float(entry_px) - float(stop0)), "entry_i": int(ti),
            "entry_px": float(entry_px), "stop0": float(stop0),
            "exit_i": int(exit_i), "exit_px": float(exit_px),
            "exit_reason": exit_reason, "advances": advances, "harvest": harv,
            "blocked": blocked, "mfe": mfe, "mae": mae, "adds": [],
            "final_stop": stop, "n_opportunities": n_opp,
            "mae_to_1r": mae_to_1r if reached_1r else None,
            "reached_1r": reached_1r,
            "warm": dict(warm), "inactive": inactive_note(warm, active),
            "n_inactive": int(len(inactive_note(warm, active)))}


# ══════════════════════════════════ 4 · THE ACCOUNTING — INTERVAL-SUM FUNDING
def funding_price_idx(lf: LensFrame, stamp_ms) -> np.ndarray:
    """[B4] The index of the last lens bar CLOSED at or before each stamp, -1
    where none exists.  This is `engine.htf`'s visibility law with the funding
    stamp standing in for the exec bar's open — and on 4h, where every stamp is
    a bar OPEN, it returns exactly `j - 1` for the stamp at `open_ms[j]`, which
    is the price the lineage's `fund_leg` uses."""
    st = np.atleast_1d(np.asarray(stamp_ms, np.int64))
    return np.searchsorted(lf.open_ms + lf.step_ms, st, side="right") - 1


def funding_interval(lf: LensFrame, entry_ms: int, exit_ms: int, d: int,
                     qty: float) -> dict:
    """THE INTERVAL SUM [Stage D LEAN D-g, B4].

        every stamp with  entry_ms < funding_hour_ms <= exit_ms,
        priced at the close of the last lens bar closed at or before it.

    Returns the amount AND the census of stamps — `n_stamps`, `n_priced`,
    `n_unpriced`, and `n_on_bar_open` (how many the lineage's per-bar-open
    lookup would have found).  Every print is counted; a stamp that cannot be
    priced (a stamp before the tape's first close) is reported, never dropped
    in silence.

    WHAT WOULD MAKE THIS WRONG: looking the rate up by BAR OPEN (on a 1d lens
    only the 00:00 stamp matches and roughly two thirds of the funding
    disappears — measured on BTC: 5,064 of 7,595 stamps lost), or pricing a
    stamp at a close that had not printed when it settled.
    """
    fh, fr = lf.fund_hour_ms, lf.fund_rate
    lo = np.searchsorted(fh, np.int64(entry_ms), side="right")
    hi = np.searchsorted(fh, np.int64(exit_ms), side="right")
    sel = slice(int(lo), int(hi))
    stamps, rates = fh[sel], fr[sel]
    if len(stamps) == 0:
        return {"amount": 0.0, "n_stamps": 0, "n_priced": 0, "n_unpriced": 0,
                "n_on_bar_open": 0}
    k = funding_price_idx(lf, stamps)
    # THE ACCUMULATION ORDER IS THE LINEAGE'S, AND THAT IS NOT PEDANTRY.
    # `tierc7._account_chain.fund_leg` adds one stamp at a time, ascending,
    # as `rate * close * d * qty`.  A vectorised `np.sum` over the same terms
    # pairwise-reduces and lands 1.665e-16 away on one of the control's 200
    # campaigns — which is not zero, and F-BRK-RIDE-4H demands EXACTLY
    # 0.000e+00.  Measured, then fixed by matching the order.
    amt, n_priced = 0.0, 0
    for q in range(len(stamps)):
        kq = int(k[q])
        if kq < 0:
            continue
        n_priced += 1
        amt += float(rates[q]) * float(lf.c[kq]) * d * qty
    on_open = int(np.isin(stamps, lf.open_ms).sum())
    return {"amount": float(amt), "n_stamps": int(len(stamps)),
            "n_priced": int(n_priced),
            "n_unpriced": int(len(stamps) - n_priced),
            "n_on_bar_open": on_open}


def account_l(lf: LensFrame, card, d: int, r_dist: float, leg: dict) -> dict:
    """ONE CAMPAIGN'S ACCOUNTING ON THE LENS — `tierc7._account_chain` for a
    single leg, with the funding re-pointed at the interval sum [B4].

    Fee is the ESTATE'S OBJECT (`RC.FEE_BPS_SIDE`) a side; the D12 ceiling is
    taken ONCE, on the campaign's total funding, and only when funding is a
    COST (a credit is never capped).  THE FRACTIONS MUST BOOK THE LEG: when a
    campaign harvested, `n1 + n2 == net` exactly (1e-9, asserted), because a
    harvest splits one leg into two fractions that must book it.
    """
    bps = FEE_BPS_SIDE / 10_000.0
    q = float(card.harvest_frac)
    R = float(r_dist)
    ti, xi, xpx = leg["entry_i"], leg["exit_i"], leg["exit_px"]
    e = leg["entry_px"]
    harv = leg["harvest"]
    t_entry = int(lf.open_ms[ti])
    census = {"n_stamps": 0, "n_priced": 0, "n_unpriced": 0, "n_on_bar_open": 0}

    def fund(hi_i: int, qty: float) -> float:
        u = funding_interval(lf, t_entry, int(lf.open_ms[hi_i]), d, qty)
        for k_ in census:
            census[k_] += int(u[k_])
        return float(u["amount"])

    if harv is None:
        g = (xpx - e) * d
        fe = bps * (e + xpx)
        u = fund(xi, 1.0)
        n1 = n2 = None
        would_have = None
    else:
        hj, hpx, _ = harv
        g1 = q * (hpx - e) * d
        fe1 = bps * q * (e + hpx)
        u1 = fund(hj, q)
        g2 = (1.0 - q) * (xpx - e) * d
        fe2 = bps * (1.0 - q) * (e + xpx)
        u2 = fund(xi, 1.0 - q)
        g, fe, u = g1 + g2, fe1 + fe2, u1 + u2
        n1, n2 = (g1 - fe1 - u1) / R, (g2 - fe2 - u2) / R
        gw = q * (xpx - e) * d
        fw = bps * q * (e + xpx)
        uw = fund(xi, q)
        would_have = (gw - fw - uw) / R
        if abs((n1 + n2) - (g - fe - u) / R) > 1e-9:
            raise SystemExit(f"HALT: the fractions do not book the leg. "
                             f"{lf.sym} {lf.lens} entry_i={ti}")
    gross, fee, fund_raw = g / R, fe / R, u / R
    cap = card.funding_ceiling_r
    bound = bool(cap is not None and fund_raw > cap)
    fund_eff = cap if bound else fund_raw
    return {"gross_r": gross, "fee_r": fee, "funding_r": fund_eff,
            "funding_r_uncapped": fund_raw, "funding_ceiling_bound": bound,
            "net_r": gross - fee - fund_eff, "n1": n1, "n2": n2,
            "add_r": None, "harvest_ride_would_have_r": would_have,
            "funding_census": dict(census)}


def toll_class(anchor: str, band: str | None = None) -> str:
    """THE CENSUS GRID'S CLASS LABEL for a lane's anchor — the row whose
    `toll_atr` is this lane's toll.

    The memory anchor is the census's own `flip-hold`.  The band anchor is
    `retest-hold-` + THE CENSUS'S SPELLING of the band actually ridden
    (`census_band`, the spelling law above) — `retest-hold-ribbon127_200`,
    which is a row the filed grid holds, and not `retest-hold-ribbon-127/200`,
    which is a row no grid has ever held.  The label is BUILT, never a
    constant, and `get_toll` HALTs if the grid has no such row: a toll that
    cannot be READ is not one that may be guessed.
    """
    if anchor == ANCHOR_MEMORY:
        return TOLL_CLASS_PREFIX[ANCHOR_MEMORY]
    if anchor != ANCHOR_BAND:
        raise SystemExit(f"HALT: unknown anchor {anchor!r}; one of {ANCHORS}.")
    if not band:
        raise SystemExit("HALT: the band anchor's toll class needs the band "
                         "actually ridden; it is not a constant.")
    return TOLL_CLASS_PREFIX[ANCHOR_BAND] + census_band(band)


def toll_pct_of_1r(toll_atr: float, r_dist: float, atr_at_entry: float) -> float:
    """THE TOLL AS A PERCENTAGE OF 1R.  `toll_atr` is the round trip measured
    in the anchor's OWN ATR units and READ FROM THE FILED GRID (§10); R is the
    entry stop distance.  Both are ATR-normalised, so the ratio is the share of
    one unit of risk the round trip eats.

    F-C10-TOLL: no number in this function, and an AST scan of this file proves
    no float sits in a toll position anywhere in it."""
    r_atr = float(r_dist) / float(atr_at_entry)
    if not (np.isfinite(r_atr) and r_atr > 0):
        return float("nan")
    return float(toll_atr) / r_atr * float(100)


# ════════════════════════════════════════════════════ 5 · THE STOP [contract C]
def brk_stop(direction: int, retest_extreme: float, touch_i: int,
             entry_px: float, atr_sig: float,
             rail_atr: float = MIN_STOP_ATR):
    """STOP BEYOND THE RETEST EXTREME, RAILED — `tierc5_rules.spring_stop`'s
    geometry, entered with the retest extreme standing in for the sweep
    extreme, exactly as the contract says.

    The function is the estate's, not a copy: `stop = farther of {extreme -/+
    STOP_BUF_ATR x ATR, entry -/+ rail x ATR}`, and `STOP_BUF_ATR` is the
    card's one definition of the word "beyond".  Returns the estate's `Stop`
    record, so the rail's provenance is in the journal, or None when the ATR is
    unreadable (the lane then does NOT take the trade — the rail does not
    invent a stop where structure names none).
    """
    sp = RC.Spring(direction=int(direction), sweep_i=int(touch_i), sweep_ms=0,
                   sweep_extreme=float(retest_extreme),
                   swept_level=float("nan"), reclaim_i=int(touch_i),
                   reclaim_ms=0, bars_to_reclaim=0)
    return RC.spring_stop(sp, float(entry_px), float(atr_sig),
                          rail_atr=float(rail_atr))


# ══════════════════════════════════════ 6 · THE ANCHORS — SIGNALS AS ARGUMENTS
@dataclass(frozen=True)
class Candidate:
    """ONE anchor event, already as-of clean.

    `known_i` is the bar whose CLOSE the lane enters on and is the ONLY bar
    index a feature may read: the touch is stamped at `touch_i` but the hold is
    not KNOWN until `touch_i + hold_bars` (the leash's own trap — a feature
    keyed on the stamp bar leaks the hold window).  `extreme` is the retest
    extreme over [touch_i, known_i] read from the RAW tape, never from a
    rounded event field.
    """
    direction: int
    anchor: str
    die_i: int
    touch_i: int
    known_i: int
    extreme: float
    rid: int = -1
    verdict: str = "hold"
    note: str = ""


def candidacy_window(dies: list, n: int, ttl_bars: int = MEM_TTL_BARS) -> list:
    """[B5] (die_i, end] per DIE, the census builder's window:

        end = min(die_i + ttl_bars, next_die_i - 1, n - 1)

    `dies` is [(die_i, rid, side)] in bar order.  A DIE whose window is empty
    yields no row — its end is not a bar-t fact.
    """
    out = []
    for q, (d_i, rid, side) in enumerate(dies):
        nxt = int(dies[q + 1][0]) if q + 1 < len(dies) else int(n)
        end = min(int(d_i) + int(ttl_bars), nxt - 1, int(n) - 1)
        if end <= int(d_i):
            continue
        out.append((int(d_i), int(rid), str(side), end))
    return out


def r1_band(name: str):
    """THE FIVE R1 BANDS, as callables `close -> (lo, hi)`.

    OPERATOR R1 (verbatim): "Let's try the 89/127 ribbon, the 127/200 ribbon,
    and taps on each ema."  A ribbon is [min, max] of its two EMAs evaluated AT
    each bar; a tap is the single line (lo == hi).  Both are NaN — so no touch
    can read them — until the SLOWER member has seen its own period of bars,
    which is the lineage's warm-up law and the census module's band law.

    This REPLACES the contract's "89 or 200/300 band" and the foundations'
    provisional `ema89` / `ema200_300` classes.  THE RULINGS WIN.

    THE NAME MAY ARRIVE IN EITHER HOUSE STYLE (`band_key`, the spelling law):
    the census's `ribbon127_200` and this module's `ribbon-127/200` build the
    SAME callable, which is what lets the tuned band travel from
    TUNING_RESULT.json into this function untranslated by hand.  Anything that
    is not one of the five in either style HALTs.
    """
    name = band_key(name)
    kind, spec = name.split("-", 1)
    if kind == "tap":
        p = int(spec)

        def band(c: np.ndarray):
            e = ind.ema(np.asarray(c, float), p)
            e = np.asarray(e, float).copy()
            e[:p] = np.nan
            return e, e.copy()
        band.label = f"tap EMA{p} (lo == hi)"
        band.periods = (p,)
        return band
    p1, p2 = (int(x) for x in spec.split("/"))

    def band(c: np.ndarray):
        c = np.asarray(c, float)
        a, b = ind.ema(c, p1), ind.ema(c, p2)
        lo, hi = np.minimum(a, b), np.maximum(a, b)
        lo, hi = np.asarray(lo, float).copy(), np.asarray(hi, float).copy()
        lo[:max(p1, p2)] = np.nan
        hi[:max(p1, p2)] = np.nan
        return lo, hi
    band.label = f"ribbon [min,max](EMA{p1}, EMA{p2})"
    band.periods = (p1, p2)
    return band


def band_hold_candidates(h: np.ndarray, l: np.ndarray, c: np.ndarray,
                         atr: np.ndarray, dies: list, lo: np.ndarray,
                         hi: np.ndarray, margin_atr: float, hold_bars: int,
                         ttl_bars: int = MEM_TTL_BARS,
                         anchor_label: str = ANCHOR_BAND) -> tuple:
    """THE S1 ANCHOR — the first HOLD retest of the band after a macro DIE, in
    the DIE direction.  A TRANSCRIPTION of `tierc10_census.retest_holds`, whose
    law is the flip-hold law with the band in place of the memory line:

      · ONE evaluation per DIE.  The first bar j in the candidacy window whose
        [low, high] MEETS the band AND whose PRIOR close sat BEYOND the band on
        the die side (a top-DIE: price comes back DOWN to it).  A touch from
        the other side spends nothing.
      · HOLD iff, for k in j .. j + hold_bars, no close goes through the band's
        far edge by margin_atr x ATR[k] — the ATR of bar k, not of the touch.
      · j + hold_bars >= n  =>  TRUNCATED, and a truncated window NEVER
        confirms.  A band that is unreadable (NaN) inside the window FAILS it.
      · known_at = j + hold_bars for all three verdicts.

    Signals arrive as ARGUMENTS: `dies` = [(die_i, rid, side)], `(lo, hi)` the
    per-bar band.  This function imports no range code and touches no file.

    Returns (candidates, tally).  Only `hold` rows become candidates; `failed`
    and `truncated` are counted, which is what makes "a failed hold must FAIL"
    a countable claim rather than an absence.
    """
    n = int(len(c))
    H = int(hold_bars)
    cands, rows = [], []
    for d_i, rid, side, end in candidacy_window(dies, n, ttl_bars):
        w = np.arange(d_i + 1, end + 1)
        with np.errstate(invalid="ignore"):
            touch = (l[w] <= hi[w]) & (h[w] >= lo[w])
            opp = (c[w - 1] > hi[w - 1]) if side == "top" else (c[w - 1] < lo[w - 1])
        hit = np.nonzero(touch & opp)[0]
        if not len(hit):
            continue
        j = int(w[hit[0]])
        if j + H >= n:
            verdict = "truncated"
        else:
            k = np.arange(j, j + H + 1)
            with np.errstate(invalid="ignore"):
                through = ((c[k] < lo[k] - margin_atr * atr[k]) if side == "top"
                           else (c[k] > hi[k] + margin_atr * atr[k]))
                unread = ~np.isfinite(lo[k]) | ~np.isfinite(hi[k])
            verdict = "failed" if (through | unread).any() else "hold"
        rows.append({"rid": int(rid), "side": side, "die_i": int(d_i),
                     "touch_i": j, "known_at": j + H, "verdict": verdict})
        if verdict != "hold":
            continue
        direction = 1 if side == "top" else -1
        seg = slice(j, j + H + 1)
        ext = float(np.min(l[seg])) if direction == 1 else float(np.max(h[seg]))
        cands.append(Candidate(direction=direction, anchor=anchor_label,
                               die_i=int(d_i), touch_i=j, known_i=j + H,
                               extreme=ext, rid=int(rid), verdict="hold",
                               note=f"band hold, side={side}"))
    tally = {"n_dies": len(dies), "n_evaluated": len(rows),
             "n_hold": sum(1 for r in rows if r["verdict"] == "hold"),
             "n_failed": sum(1 for r in rows if r["verdict"] == "failed"),
             "n_truncated": sum(1 for r in rows if r["verdict"] == "truncated"),
             "rows": rows}
    return cands, tally


def memory_flip_candidates(h: np.ndarray, l: np.ndarray, dies: list,
                           flips: list, n: int,
                           hold_bars: int = FLIP_HOLD_BARS,
                           ttl_bars: int = MEM_TTL_BARS,
                           same_range_only: bool = False) -> tuple:
    """THE I1 ANCHOR — the first memory-line FLIP-HOLD after a macro DIE.

    `flips` arrive as ARGUMENTS, one dict per leash `flip` event, carrying at
    least `{"i": touch bar, "polarity": "support"|"resistance"}` and optionally
    `rid`.  THE AS-OF TRAP IS THE WHOLE POINT: the leash stamps a flip at the
    RETEST bar `i`, but it is only KNOWABLE at `i + FLIP_HOLD_BARS`, because
    the confirming loop reads c[i .. i+6].  So the earliest legal entry is the
    CLOSE of bar `i + hold_bars`, never bar `i`, and this function refuses to
    emit any other.

    Direction is the flip's POLARITY: a dead TOP that holds as support flips
    long (+1); a dead BOTTOM that holds as resistance flips short (-1).  Where
    the parent DIE's own side disagrees with the polarity the row is COUNTED
    (`n_polarity_vs_die_mismatch`) and still emitted, because the ruling names
    the flip's polarity and not the DIE's side — unless `same_range_only`, in
    which case only flips whose `rid` is the DIE's range are admitted and both
    counts are printed.

    [B5] the candidacy window is the census builder's, applied ON TOP of the
    leash's own TTL/cap — see FINDINGS, mismatch 1.
    """
    H = int(hold_bars)
    pol = {"support": 1, "resistance": -1}
    ev = sorted((dict(x) for x in flips), key=lambda x: int(x["i"]))
    cands, rows = [], []
    mism = 0
    for d_i, rid, side, end in candidacy_window(dies, n, ttl_bars):
        pick = None
        for e in ev:
            i = int(e["i"])
            if not (d_i < i <= end):
                continue
            if same_range_only and int(e.get("rid", -1)) != int(rid):
                continue
            pick = e
            break
        if pick is None:
            continue
        i = int(pick["i"])
        p = str(pick.get("polarity", ""))
        if p not in pol:
            raise SystemExit(f"HALT: a flip at bar {i} carries polarity "
                             f"{p!r}; the leash publishes support|resistance.")
        direction = pol[p]
        known = i + H
        if known >= int(n):
            rows.append({"rid": int(rid), "die_i": int(d_i), "touch_i": i,
                         "known_at": known, "verdict": "truncated"})
            continue
        die_dir = 1 if side == "top" else -1
        if die_dir != direction:
            mism += 1
        seg = slice(i, known + 1)
        ext = float(np.min(l[seg])) if direction == 1 else float(np.max(h[seg]))
        rows.append({"rid": int(rid), "die_i": int(d_i), "touch_i": i,
                     "known_at": known, "verdict": "hold"})
        cands.append(Candidate(direction=direction, anchor=ANCHOR_MEMORY,
                               die_i=int(d_i), touch_i=i, known_i=known,
                               extreme=ext, rid=int(pick.get("rid", rid)),
                               verdict="hold",
                               note=f"flip polarity={p}, die side={side}"))
    tally = {"n_dies": len(dies), "n_flips_offered": len(ev),
             "n_evaluated": len(rows),
             "n_hold": sum(1 for r in rows if r["verdict"] == "hold"),
             "n_truncated": sum(1 for r in rows
                                if r["verdict"] == "truncated"),
             "n_polarity_vs_die_mismatch": int(mism),
             "same_range_only": bool(same_range_only), "rows": rows}
    return cands, tally


# ══════════════════════════════════════════════ 7 · THE TUNED PINS [R1], READ
_TUNE_BAND_KEYS = ("band", "band_name", "anchor", "chosen_band", "scored_band")
_TUNE_MARGIN_KEYS = ("margin_atr", "margin", "hold_margin_atr")
_TUNE_HOLD_KEYS = ("hold_bars", "hold", "hold_n")
_TUNE_TTL_KEYS = ("ttl_bars", "ttl", "mem_ttl_bars")


def _tune_dig(obj, lens: str) -> dict | None:
    """Find the one scored cell in whatever shape the census builder files it:
    the top level, `scored`/`result`/`scored_arm`, or a per-lens map."""
    if not isinstance(obj, dict):
        return None
    if any(k in obj for k in _TUNE_BAND_KEYS):
        return obj
    for k in ("scored", "scored_arm", "result", "chosen", "winner"):
        got = _tune_dig(obj.get(k), lens)
        if got:
            return got
    for k in ("lens", "by_lens", "lenses", "per_lens"):
        m = obj.get(k)
        if isinstance(m, dict):
            got = _tune_dig(m.get(lens), lens)
            if got:
                return got
    got = _tune_dig(obj.get(lens), lens)
    return got


def _pick(d: dict, keys: tuple, what: str, path: Path):
    for k in keys:
        if k in d and d[k] is not None:
            return d[k]
    raise SystemExit(f"HALT: {path} names no {what}; it was looked for under "
                     f"{keys} and the file carries {sorted(d)}.")


def tuned_pins(lens: str = "5m", path: Path | None = None) -> dict:
    """THE SCORED (band, margin_atr, hold_bars), READ AT RUN TIME [R1].

    The tuning protocol was fixed BEFORE any look (R1: tuning era <=
    2024-06-30T23:59:59Z, grid = five bands x margin {0.25, 0.5, 1.0} x hold
    {3, 6, 12}, objective = pooled median NET term at H20 subject to n >= 200,
    tie-break to the pins already on disk then to the simpler band).  The
    RESULT is the census builder's to produce; this module's only business with
    it is to READ it and to refuse to run without it.

    ONE FILE PER TUNED LENS (`TUNING_RESULT_FOR`), AND THE CELL MUST SAY IT IS
    THAT LENS'S.  The 5m file is P-BRK-S1's scored arm; the 1d file is the
    Tier-E EMA-band print of P-BRK-I1 and nothing else (R1).  The two cells
    carry different bands, margins and holds, so reading one for the other is
    not an approximation, it is the wrong pin.

    HALTS IF: the lens is not one the R1 protocol tunes; the file is absent
    (the pins are not this module's to invent); the file's scored cell names a
    DIFFERENT lens than the one asked for; the band named is not one of the
    operator's five under any spelling; the margin or hold is missing or not a
    positive number.

    WHAT WOULD MAKE THIS WRONG: a default value anywhere in this function.  A
    tuned pin with a fallback is a typed pin wearing a tuned pin's name — and
    so is a tuned pin read for the wrong lens, which is why the `lens` field
    is CHECKED here and not merely overwritten with the answer wanted.
    """
    if path is None and lens not in TUNING_RESULT_FOR:
        raise SystemExit(
            f"HALT: no tuned pins exist for lens {lens!r}.  The R1 protocol "
            f"tunes {TUNED_LENSES} and this module reads the file the census "
            f"filed FOR THE LENS ASKED FOR, never a neighbour lens's cell.")
    p = Path(path) if path else TUNING_RESULT_FOR[lens]
    if not p.exists():
        raise SystemExit(
            f"HALT: {p} is absent.  P-BRK-S1's band and hold pins are TUNED "
            f"under the R1 protocol and are READ, never typed.  The census "
            f"builder files this; until it does, no S1 lane may ride.")
    try:
        raw = json.loads(p.read_text(encoding="utf-8"))
    except Exception as e:                                  # noqa: BLE001
        raise SystemExit(f"HALT: {p} is not readable JSON ({e!r}).")
    cell = _tune_dig(raw, lens)
    if not cell:
        raise SystemExit(
            f"HALT: {p} carries no scored cell for lens {lens!r} — looked at "
            f"the top level, at scored/result/chosen/winner and at a per-lens "
            f"map; the file's top-level keys are {sorted(raw) if isinstance(raw, dict) else type(raw).__name__}.")
    cell_lens = cell.get("lens")
    if cell_lens is not None and str(cell_lens) != str(lens):
        raise SystemExit(
            f"HALT: {p} holds the scored cell of lens {str(cell_lens)!r}, not "
            f"{lens!r}.  The R1 grid is tuned PER LENS (5m = P-BRK-S1's "
            f"scored arm, 1d = the Tier-E EMA-band print of P-BRK-I1) and the "
            f"two cells do not stand in for each other; a tuned pin read for "
            f"the wrong lens is a typed pin wearing a tuned pin's name.  The "
            f"file for {lens!r} is {TUNING_RESULT_FOR.get(lens, '(none)')}.")
    filed = str(_pick(cell, _TUNE_BAND_KEYS, "band", p))
    band = band_key(filed)              # HALTs on a sixth band, in any spelling
    margin = float(_pick(cell, _TUNE_MARGIN_KEYS, "margin_atr", p))
    hold = int(_pick(cell, _TUNE_HOLD_KEYS, "hold_bars", p))
    ttl_key = next((k for k in _TUNE_TTL_KEYS if k in cell), None)
    ttl = int(cell[ttl_key]) if ttl_key else MEM_TTL_BARS
    if not (np.isfinite(margin) and margin > 0) or hold <= 0 or ttl <= 0:
        raise SystemExit(f"HALT: {p} scores band={band} margin={margin} "
                         f"hold={hold} ttl={ttl}; none of the three may be "
                         f"non-positive.")
    return {"lens": lens, "band": band, "band_as_filed": filed,
            "band_census": census_band(band), "margin_atr": margin,
            "hold_bars": hold, "ttl_bars": ttl, "source": str(p),
            "cell": cell}


# ════════════════════════════════════════════════════════════ 8 · PERMISSIONS
def visible_htf_idx(exec_open_ms: np.ndarray, htf_open_ms: np.ndarray,
                    htf_step_ms: int) -> np.ndarray:
    """`engine.htf.map_htf_to_exec`'S LAW, WITH THE STEP IN MILLISECONDS.

        the HTF bar visible to an exec bar is the most recent one whose CLOSE
        time is <= that exec bar's OPEN time; -1 where none exists yet.

    The engine's own function keys the step off `engine.cells.INTERVAL_MS`,
    which publishes 1m/5m/15m/1h/4h/12h and NO '1d' or '1w' — so the investor's
    weekly-onto-daily map cannot go through it, and `engine/cells.py` is a
    frozen file this task does not own.  This restates the law and F-BRK-PERM
    proves the two agree bar for bar on 4h, including at an exact boundary.

    WHAT WOULD MAKE THIS WRONG: `side='left'`, or comparing against the exec
    bar's CLOSE — either would make an HTF bar visible one exec bar early, and
    the entry is at a CLOSE, so the leak would be invisible in the prices.
    """
    ex = np.atleast_1d(np.asarray(exec_open_ms, np.int64))
    ht = np.asarray(htf_open_ms, np.int64) + np.int64(htf_step_ms)
    return np.searchsorted(ht, ex, side="right") - 1


def tide_state(e_fast: np.ndarray, e_slow: np.ndarray,
               c: np.ndarray) -> np.ndarray:
    """THE TIDE, three-state, as the card has stated it since TIER-C2:

        +1 iff e89 > e316 AND close > e316;  -1 on the mirror;  0 = STAND DOWN
        (the state that exists, and is not a synonym for "no opinion").
    """
    up = (e_fast > e_slow) & (c > e_slow)
    dn = (e_fast < e_slow) & (c < e_slow)
    return np.where(up, 1, np.where(dn, -1, 0)).astype(np.int64)


def tide_4h_for_exec(exec_open_ms: np.ndarray, f4: LensFrame,
                     roles=None) -> tuple:
    """THE 4h TIDE AS OF THE LAST CLOSED 4h BAR, for each exec bar [S1, (D)].

    Returns (state, htf_idx).  `state` is -1/0/+1 and is 0 where no 4h bar has
    closed yet (an exec bar with nothing behind it is STAND DOWN, never
    silently long).  The visibility is the engine's: an HTF bar is visible iff
    it closed at or before the exec bar's OPEN.  The entry is at the exec bar's
    CLOSE, so this is the conservative choice and it is named: a 4h bar that
    closes exactly AT the entry instant is NOT read.
    """
    roles = roles or T9.V6_ROLES
    ra = roles_l(f4, roles)
    st = tide_state(ra["tide_f"], ra["tide_s"], f4.c)
    idx = HTF.map_htf_to_exec(np.atleast_1d(np.asarray(exec_open_ms, np.int64)),
                              f4.open_ms, f4.lens)
    out = np.where(idx < 0, 0, st[np.clip(idx, 0, None)]).astype(np.int64)
    return out, idx


def ribbon_lifecycle(c: np.ndarray, atr: np.ndarray, fast: int = RIBBON_FAST,
                     slow: int = RIBBON_SLOW, k: int = LIFECYCLE_K) -> dict:
    """THE 12/25 RIBBON LIFECYCLE [R4], as-of closed bars only.

    OPERATOR (verbatim): "It means we observe the transition from expansion of
    the bands, into consolidation and closing of the bands. This is followed by
    new expansion, either as continuation or as reversal, a final cross after
    the interweaving of the ema turns to expanding the ribbon between the
    ema's".

    READING, mechanically:
        s[t]           = (e12[t] - e25[t]) / ATR14[t]
        EXPANDING(t)   = sign(s) unchanged over the window s[t-K .. t]  [B3]
                         AND |s[t]| > |s[t-K]|
        CONSOLIDATING  = warm and not EXPANDING (the ribbon is closing and/or
                         the EMAs are interweaving — a sign change inside the
                         window is exactly the interweave)
        DIRECTION      = sign(s) while EXPANDING, else 0 (NONE)
    A lifecycle is RENEWED when EXPANDING resumes after at least one
    CONSOLIDATING bar; an episode is CONTINUATION when its sign equals the
    previous episode's and REVERSAL when it does not — the "final cross after
    the interweaving" is precisely a reversal episode's first bar.

    NaN WARM-UP IS NO PERMISSION.  `ind.ema` seeds at the series start and never
    returns NaN, so warmth is the index law: bar >= max(fast, slow), and an ATR
    that is not finite and positive is not warm either.  Bars before that are
    PHASE_WARMUP with direction 0 — never CONSOLIDATING, because "the bands are
    closing" is a claim and a cold EMA makes no claims.

    Returns per-bar arrays plus `episodes`, each
    {start, end, sign, kind in first|continuation|reversal}.
    """
    c = np.asarray(c, float)
    atr = np.asarray(atr, float)
    n = int(len(c))
    k = int(k)
    e_f, e_s = ind.ema(c, int(fast)), ind.ema(c, int(slow))
    warm = np.arange(n) >= max(int(fast), int(slow))
    warm &= np.isfinite(atr) & (atr > 0)
    with np.errstate(invalid="ignore", divide="ignore"):
        s = np.where(warm, (e_f - e_s) / atr, np.nan)
    sg = np.zeros(n, np.int64)
    fin = np.isfinite(s)
    sg[fin] = np.sign(s[fin]).astype(np.int64)
    expanding = np.zeros(n, bool)
    for t in range(k, n):
        if not warm[t] or sg[t] == 0:
            continue
        win = slice(t - k, t + 1)
        if not warm[win].all() or not (sg[win] == sg[t]).all():
            continue
        if abs(float(s[t])) > abs(float(s[t - k])):
            expanding[t] = True
    phase = np.where(~warm, PHASE_WARMUP,
                     np.where(expanding, PHASE_EXPANDING, PHASE_CONSOLIDATING))
    direction = np.where(expanding, sg, 0).astype(np.int64)
    episodes, prev_sign = [], None
    t = 0
    while t < n:
        if not expanding[t]:
            t += 1
            continue
        u = t
        while u + 1 < n and expanding[u + 1] and sg[u + 1] == sg[t]:
            u += 1
        kind = ("first" if prev_sign is None
                else "continuation" if int(sg[t]) == prev_sign else "reversal")
        episodes.append({"start": int(t), "end": int(u), "sign": int(sg[t]),
                         "kind": kind})
        prev_sign = int(sg[t])
        t = u + 1
    return {"s": s, "sign": sg, "warm": warm, "expanding": expanding,
            "phase": phase, "direction": direction, "episodes": episodes,
            "k": k, "fast": int(fast), "slow": int(slow)}


def weekly_posture(c_1w: np.ndarray, fast: int = RIBBON_FAST,
                   slow: int = RIBBON_SLOW) -> np.ndarray:
    """THE WEEKLY 12/25 POSTURE, per CLOSED Monday-week bar: +1 iff e12 > e25,
    -1 iff e12 < e25, 0 while the slower EMA is not warm.

    The bars are Stage D's derived 1w file — MONDAY-anchored COMPLETE weeks
    [L1].  `analytics.structure.resample_ohlcv` would have floored the week to
    THURSDAY (epoch day 0) and kept a partial head bucket; it is not used, and
    that is why the tape comes from Stage D rather than from a resampler here.
    """
    c_1w = np.asarray(c_1w, float)
    e_f, e_s = ind.ema(c_1w, int(fast)), ind.ema(c_1w, int(slow))
    warm = np.arange(len(c_1w)) >= max(int(fast), int(slow))
    return np.where(~warm, 0, np.where(e_f > e_s, 1,
                                       np.where(e_f < e_s, -1, 0))).astype(np.int64)


def i1_permission(entry_i: int, direction: int, daily_direction: np.ndarray,
                  weekly_state: np.ndarray, weekly_idx: np.ndarray) -> dict:
    """P-BRK-I1's PERMISSION [R4]: weekly e12 > e25 on the LAST CLOSED
    Monday-week AND daily DIRECTION = +1 (mirror for a short).

    Both are read AT the entry bar [B7]: the daily direction from the 1d
    lifecycle at `entry_i` (the bar whose close the lane enters on, and which
    IS closed at that instant), the weekly posture from the last weekly bar
    CLOSED at or before that day's OPEN.  A weekly EMA25 that is not warm is
    posture 0 and is NO permission — HYPE has 68 complete weeks and several of
    the unseen twelve have fewer; a lane that treated cold as neutral would let
    them all through.
    """
    wi = int(weekly_idx[int(entry_i)]) if np.ndim(weekly_idx) else int(weekly_idx)
    w = int(weekly_state[wi]) if wi >= 0 else 0
    dd = int(daily_direction[int(entry_i)])
    ok = bool(w == int(direction) and dd == int(direction))
    return {"ok": ok, "weekly_posture": w, "weekly_bar": wi,
            "daily_direction": dd,
            "why": "" if ok else
                   (f"weekly={w} daily={dd} need both == {int(direction)}")}


def s1_permission(entry_i: int, direction: int,
                  tide_state_exec: np.ndarray) -> dict:
    """P-BRK-S1's PERMISSION [(D)]: the 4h tide ALIGNED with the trade at the
    last CLOSED 4h bar visible to the entry bar's OPEN."""
    t = int(tide_state_exec[int(entry_i)])
    ok = bool(t == int(direction))
    return {"ok": ok, "tide_4h": t,
            "why": "" if ok else f"4h tide={t}, need {int(direction)}"}


# ════════════════════════════════════════════════════════ 9 · THE ERA [R1/R2]
def require_era(entry_ms: int, sym: str, lane: str, era: str) -> None:
    """[B6] AN OUT-OF-ERA ENTRY IS A HALT, NOT A FILTER APPLIED AFTERWARDS.

    P-BRK-S1's band and hold pins are TUNED on entries at or before the R1 cut,
    so an entry taken there is in-sample by construction.  The lane's WINDOW is
    what must exclude them (`TP.corridor_era(panel, "holdout")`); if one still
    reaches the replay the window was wrong, and a filter that quietly dropped
    it would hide that the window was wrong.  So this raises.

    THE TEST IS `TP.in_era`, the panel module's own — the same object that
    refuses the journal at `external_book`.  A second cut restated here could
    drift, and it would drift toward admitting a campaign this module rides and
    the door then kills.

    WHICH INSTANT IS TESTED, SAID PLAINLY.  `entry_ms` is the entry bar's
    OPEN; R1 states the era in CLOSE time.  For a bar that STRADDLES the cut
    the two disagree, and they disagree in one direction only: such a bar is
    HOLDOUT by R1's clock and TUNING by its open, so this test REFUSES a bar
    R1 would allow and can never admit one R1 would forbid.  That is the
    conservative side of the line, and it is the same side `external_book`
    takes, so nothing this module rides can die at the door — but it is a
    refusal, not merely a caution, and it is named here for that reason.
    Measured today: the holdout corridor opens at 2024-07-01T00:00:00Z, a
    boundary of every lens's grid, so no bar straddles the cut inside a
    holdout window and no legal entry is refused (FINDINGS, mismatch 4).

    HALTS IF: `entry_ms` lies outside `era` (e.g. a tuning-era entry offered to
    a lane whose filed arm rides the HOLDOUT era).
    """
    if era is None:
        return
    if not TP.in_era(int(entry_ms), era):
        raise SystemExit(
            f"HALT: {lane} offered {sym} an entry at "
            f"{TP.iso(int(entry_ms))}, OUTSIDE the arm's filed {era!r} era "
            f"(cut {ERA_CUT_ISO} [R1]). {TP.era_note(era)} The WINDOW is what "
            f"must exclude it — ride TP.corridor_era(panel, {era!r}); a filter "
            f"applied after the fact would hide that the window was wrong.")


# ──────────── 9b · THE DECLARED ERA PIN, HELD AGAINST THE FILED ARM [B9] ────
LANE_ERA_REASON = {
    LANE_S1: ("P-BRK-S1's (band, margin_atr, hold_bars) were CHOSEN by the "
              "census builder's R1 tuning on entries AT OR BEFORE the cut.  "
              "Scoring the scalper on 'full' — or on 'tuning' — would score "
              "it IN SAMPLE on the very grid that picked its pins, and the "
              "row would read as a result when it is a fit."),
    LANE_I1: ("P-BRK-I1 tunes nothing and is declared on the FULL corridor "
              "[R2].  An arm that collars it to one era would score the "
              "investor on a window its own text does not name, and the "
              "holdout half of that window is P-BRK-S1's collar, not its."),
}
LANE_ERA_LAW = (
    "LANE_ERA is a PIN, and a pin nothing checks is a comment.  The era a "
    "lane actually rides comes from the FILED ARM (`gate()['era']`, i.e. "
    "`arm_spec(..., era=...)`), so the declared pin and the filed arm are two "
    "different objects that can disagree — and the disagreement that matters "
    "is silent: a P-BRK-S1 arm filed at era='full' rides the whole corridor, "
    "passes `external_book`'s door (which only holds the journal to the arm's "
    "OWN era) and prints a number that looks out of sample and is not.  "
    "`require_lane_era` closes that: it runs INSIDE both runners, immediately "
    "after the gate and BEFORE the corridor is read, so not one bar is "
    "touched on a mismatch.")


def require_lane_era(lane: str, gate_: dict) -> str:
    """THE DECLARED ERA PIN vs THE FILED ARM — a HALT, named [B9].

    `LANE_ERA` says which era each BRK lane is scored on: brk-s1 the HOLDOUT
    (its pins are tuned at or before the R1 cut, so that is the only era on
    which they are out of sample), brk-i1 the FULL corridor (it tunes
    nothing).  Until this function existed the pin was DECLARED and nothing
    compared it to anything: both runners took `era = g["era"]` from the arm
    and rode it.

    WHY THE HALT AND NOT A NARROWING.  `corridor_era` would happily cut a
    'full' arm's window to the holdout, and that would be the WRONG repair:
    the arm's TEXT is what is registered, and a runner that silently rides a
    window its registration does not name has made the text stop meaning
    anything.  The registration is refiled, or the lane does not ride.

    WHERE IT SITS.  Immediately after `gate()` in both runners, before
    `corridor_era` (which reads bar stamps) and long before `frame_l` (which
    reads bars).  F-BRK-LANE-ERA proves the HALT fires with ZERO calls to
    either.

    HALTS IF: `lane` has no declared era; the gate is not a gate; or the filed
    arm's era is not `LANE_ERA[lane]` — e.g. P-BRK-S1 filed at era='full'.
    """
    if lane not in LANE_ERA:
        raise SystemExit(
            f"HALT: lane {lane!r} has no declared era in LANE_ERA "
            f"({dict(sorted(LANE_ERA.items()))}); a lane whose era is not "
            f"DECLARED may not ride, because there is then nothing for the "
            f"filed arm to be held against. {LANE_ERA_LAW}")
    if not isinstance(gate_, dict) or "era" not in gate_:
        raise SystemExit(
            f"HALT: require_lane_era({lane!r}) was handed "
            f"{type(gate_).__name__} and not the dict `gate()` returns; the "
            f"era must come from the FILED ARM, never from the caller.")
    want, got = str(LANE_ERA[lane]), str(gate_["era"])
    if got != want:
        raise SystemExit(
            f"HALT: {lane} is DECLARED to ride the {want!r} era (LANE_ERA), "
            f"but the filed arm {str(gate_.get('registration'))!r} / "
            f"{str(gate_.get('arm'))!r} names {got!r}. "
            f"{LANE_ERA_REASON[lane]} {TP.era_note(want)} Not one bar has "
            f"been read. REFILE the arm at era={want!r} (TP.arm_spec(..., "
            f"era={want!r})) — the window is NOT narrowed here, because a "
            f"runner that rides a window its registration does not name has "
            f"made the registration text stop meaning anything. "
            f"{LANE_ERA_LAW}")
    return want


# ═══════════════════════════════════════════════════ 10 · THE CORE REPLAY
@dataclass
class Leg:
    """What the core rides: a direction, an entry bar, and a stop that is
    already the lane's own geometry.  Keeping the stop OUTSIDE the core is what
    lets F-BRK-RIDE-4H feed the control's `struct_stop_4h` stops through the
    identical ride."""
    direction: int
    entry_i: int
    stop_px: float
    r_dist: float
    anchor: float = float("nan")
    anchor_bar: int = -1
    rail_binding: bool = False
    n_eligible: int = 1
    touch_i: int = -1
    die_i: int = -1
    rid: int = -1
    anchor_kind: str = ""
    note: str = ""


def brk_campaigns(lf: LensFrame, legs: list, card, roles, lane: str,
                  lo_i: int, hi_i: int, ribbon: tuple | None = None,
                  active: tuple = COMPONENTS, era: str | None = None,
                  account: bool = True) -> list:
    """THE CORE REPLAY — one position per (asset, lane), rides ONE campaign at
    a time in bar order, and accounts each on the lens.

    `legs` are already gated (permissions, era, stop); this function's own laws
    are the lineage's: a candidate whose entry bar is at or before the open
    campaign's exit bar is REFUSED (`position_open`), the ride is
    `ride_leg_l`, the accounting is `account_l`.

    The era test runs HERE as well as in the runner [B6], because the core is
    what a fixture can reach and a law that only the runner enforces is a law
    the fixtures cannot prove.
    """
    out = []
    open_until = -1
    legs = sorted(legs, key=lambda L: (int(L.entry_i), -int(L.direction)))
    for L in legs:
        ti = int(L.entry_i)
        if not (int(lo_i) <= ti <= int(hi_i)):
            continue
        if ti <= open_until:
            continue
        require_era(int(lf.open_ms[ti]), lf.sym, lane, era)
        entry_px = float(lf.c[ti])
        atr_sig = float(lf.atr[ti])
        if not (np.isfinite(atr_sig) and atr_sig > 0):
            continue
        if not (np.isfinite(L.r_dist) and L.r_dist > 0):
            continue
        leg = ride_leg_l(lf, card, roles, int(L.direction), ti, entry_px,
                         float(L.stop_px), float(L.r_dist), int(hi_i),
                         ribbon=ribbon, active=active)
        open_until = leg["exit_i"]
        acc = (account_l(lf, card, int(L.direction), float(L.r_dist), leg)
               if account else {})
        harv = leg["harvest"]
        t = RC.Trade(
            symbol=lf.sym, lane=lane, direction=int(L.direction),
            arm_i=int(L.touch_i if L.touch_i >= 0 else ti),
            arm_ms=int(lf.open_ms[L.touch_i if L.touch_i >= 0 else ti]),
            entry_i=ti, entry_ms=int(lf.open_ms[ti]), entry_px=entry_px,
            stop_px=float(L.stop_px), r_dist=float(L.r_dist),
            anchor=float(L.anchor), anchor_bar_ms=(int(lf.open_ms[L.anchor_bar])
                                                   if L.anchor_bar >= 0 else -1),
            anchor_was_sealed=False, atr_at_entry=atr_sig,
            disp_at_arming=float("nan"),
            exit_i=leg["exit_i"], exit_ms=int(lf.open_ms[leg["exit_i"]]),
            exit_px=leg["exit_px"], exit_reason=leg["exit_reason"],
            bars_held=leg["exit_i"] - ti, scored=True,
            advances=list(leg["advances"]), final_stop_px=leg["final_stop"],
            stop_advanced_atr=((leg["final_stop"] - leg["stop0"])
                               * int(L.direction) / atr_sig),
            ratchet_exit=bool(leg["exit_reason"] == "stop" and leg["advances"]
                              and abs(leg["final_stop"] - leg["stop0"]) > 1e-12),
            harvested=harv is not None,
            harvest_i=(harv[0] if harv else None),
            harvest_ms=(int(lf.open_ms[harv[0]]) if harv else None),
            harvest_px=(harv[1] if harv else None),
            harvest_unit_move_r=(harv[2] if harv else None),
            harvest_blocked_by=leg["blocked"],
            harvest_ride_would_have_r=acc.get("harvest_ride_would_have_r"),
            adds=[], add_r=None, spring=None,
            mfe_r=(leg["mfe"] - entry_px) * int(L.direction) / float(L.r_dist),
            mae_to_1r_r=leg["mae_to_1r"], reached_1r=leg["reached_1r"],
            gross_r=acc.get("gross_r"), fee_r=acc.get("fee_r"),
            funding_r=acc.get("funding_r"),
            funding_r_uncapped=acc.get("funding_r_uncapped"),
            funding_ceiling_bound=bool(acc.get("funding_ceiling_bound", False)),
            net_r=acc.get("net_r"), net_r_harvest_half=acc.get("n1"),
            net_r_runner_half=acc.get("n2"), net_r_bellonly=None)
        for k_, v_ in (("mae_r", leg["mae"]),
                       ("n_opportunities", leg["n_opportunities"]),
                       ("roles_name", roles.name), ("lens", lf.lens),
                       ("inactive_components", leg["inactive"]),
                       ("n_inactive_components", leg["n_inactive"]),
                       ("anchor_kind", L.anchor_kind or lane),
                       ("touch_i", int(L.touch_i)), ("die_i", int(L.die_i)),
                       ("rid", int(L.rid)),
                       ("funding_census", acc.get("funding_census")),
                       ("entry_close_ms", int(lf.close_ms[ti])),
                       ("exit_close_ms", int(lf.close_ms[leg["exit_i"]]))):
            object.__setattr__(t, k_, v_)
        out.append(t)
    return out


def legs_from_candidates(lf: LensFrame, cands: list, lane: str,
                         permit=None, rail_atr: float = MIN_STOP_ATR) -> tuple:
    """CANDIDATES -> LEGS: the stop geometry (§5) and the permission (§8),
    applied AT the entry bar [B7], with every refusal COUNTED.

    `permit(entry_i, direction) -> dict with 'ok'` or None for no gate (the
    Tier-E other-anchor prints run ungated and say so).
    """
    legs, refused = [], {"permission": 0, "no_atr": 0, "no_stop": 0,
                         "out_of_tape": 0}
    for cd in cands:
        ti = int(cd.known_i)
        if not (0 <= ti < lf.n):
            refused["out_of_tape"] += 1
            continue
        atr_sig = float(lf.atr[ti])
        if not (np.isfinite(atr_sig) and atr_sig > 0):
            refused["no_atr"] += 1
            continue
        if permit is not None and not permit(ti, int(cd.direction))["ok"]:
            refused["permission"] += 1
            continue
        stp = brk_stop(int(cd.direction), float(cd.extreme), int(cd.touch_i),
                       float(lf.c[ti]), atr_sig, rail_atr=rail_atr)
        if stp is None or not (np.isfinite(stp.r_dist) and stp.r_dist > 0):
            refused["no_stop"] += 1
            continue
        legs.append(Leg(direction=int(cd.direction), entry_i=ti,
                        stop_px=float(stp.stop_px), r_dist=float(stp.r_dist),
                        anchor=float(stp.anchor), anchor_bar=int(cd.touch_i),
                        rail_binding=bool(stp.rail_binding),
                        touch_i=int(cd.touch_i), die_i=int(cd.die_i),
                        rid=int(cd.rid), anchor_kind=cd.anchor,
                        note=cd.note))
    return legs, refused


# ══════════════════════════════════════════ 11 · THE RUNNERS — GATED FIRST [G]
GATE_HELPER = "TP.require_arm"      # the CURRENT panel API for external lanes


def gate(reg_id: str, text: str, arm: str, panel, lane: str,
         head_of_record=None, reg_root: Path | None = None) -> dict:
    """THE PANEL GATE, CALLED BEFORE A SINGLE REAL BAR IS REPLAYED [G].

    `tierc10_panel.require_arm` is the panel module's CURRENT external-runner
    door (the API report names it for exactly these lanes): it is
    `require_registered` — text on file, sha, hash-chained registry, the head
    pin with stale pins refused, the LOAO line of record — PLUS the arm lookup,
    which proves the named arm is FILED, filed for an EXTERNAL runner, on
    exactly this panel, and that the lane string these trades will carry is a
    filed lane.  The fallback named in the task (`TP.require_registered`) is
    NOT used and does not need to be: `require_arm` exists and is strictly
    stronger.  Said out loud so a reviewer can check the choice.

    HALTS IF: nothing is filed for `reg_id` (which is the case TODAY for both
    BRK lanes, and F-BRK-GATE proves it).
    """
    return TP.require_arm(reg_id, text, arm, panel, lanes=(lane,),
                          head_of_record=head_of_record, root=reg_root)


def run_lane_s1(panel, reg_id: str, text: str, arm: str, signals: dict,
                tuned: dict | None = None, head_of_record=None,
                anchor: str = ANCHOR_BAND, card=None, roles=None,
                lo_ms: int | None = None, hi_ms: int | None = None,
                reg_root: Path | None = None) -> dict:
    """P-BRK-S1 · THE SCALPER, 5m.  GATE FIRST, THEN BARS.

    5m macro DIE at FROZEN SCALE -> first HOLD retest of the TUNED band (R1) in
    the DIE direction -> enter at the hold bar's close; stop beyond the retest
    extreme railed 1.0 ATR(5m); 4h tide aligned; v6 management lens-scaled with
    the 12/25 bell; the arm's filed era (holdout for the scored arm); net of
    fees + journaled funding, with the measured 5m toll printed as a share of
    1R from the filed grid.

    `signals` = {sym: {'dies': [(die_i, rid, side)], 'flips': [...]}} — built by
    the ADAPTER (§12) and handed IN, so this function reaches no range code.

    THE WINDOW COMES FROM THE FILED ERA, not from the caller: `corridor_era`
    cuts the panel's corridor to the arm's era on the 4h grid, so a HOLDOUT
    arm cannot be handed a window that reaches into the tuning era.  A caller
    may narrow it further but never widen it.
    """
    g = gate(reg_id, text, arm, panel, LANE_S1, head_of_record, reg_root)
    era = require_lane_era(LANE_S1, g)      # [B9] the DECLARED pin, ENFORCED
    card = card or TP.CONTROL_CARD          # — before one bar, one stamp or
    roles = roles or T9.V6_ROLES            #   one tuning file is read
    tuned = tuned or tuned_pins("5m")
    band = r1_band(tuned["band"])
    e_lo, e_hi, e_meta = TP.corridor_era(g["panel"], era)
    lo_ms = e_lo if lo_ms is None else max(int(lo_ms), e_lo)
    hi_ms = e_hi if hi_ms is None else min(int(hi_ms), e_hi)
    out = {"gate": g, "era": era, "window": (lo_ms, hi_ms), "meta": e_meta,
           "tuned": {k: tuned.get(k) for k in
                     ("lens", "band", "band_as_filed", "band_census",
                      "margin_atr", "hold_bars", "ttl_bars", "source")},
           "anchor": anchor, "trades": [], "tally": {}, "refused": {}}
    missing = [s for s in g["panel"] if s not in signals]
    if missing:
        raise SystemExit(f"HALT: run_lane_s1 was handed no macro signals for "
                         f"{missing}. Signals ARRIVE AS ARGUMENTS (§12's "
                         f"adapter builds them); this runner reaches no range "
                         f"code and cannot make them up.")
    for sym in g["panel"]:
        lf = frame_l(sym, "5m")
        f4 = frame_l(sym, "4h", with_funding=False)
        sig = signals[sym]
        if anchor == ANCHOR_BAND:
            lo, hi = band(lf.c)
            cands, tal = band_hold_candidates(
                lf.h, lf.l, lf.c, lf.atr, sig["dies"], lo, hi,
                tuned["margin_atr"], tuned["hold_bars"], tuned["ttl_bars"])
        else:
            cands, tal = memory_flip_candidates(
                lf.h, lf.l, sig["dies"], sig["flips"], lf.n,
                ttl_bars=tuned["ttl_bars"])
        tide, _ = tide_4h_for_exec(lf.open_ms, f4, roles)
        legs, ref = legs_from_candidates(
            lf, cands, LANE_S1,
            permit=lambda i, d, _t=tide: s1_permission(i, d, _t))
        lo_i, hi_i = idx_range(lf.open_ms, lo_ms, hi_ms)
        out["trades"] += brk_campaigns(
            lf, legs, card, roles, LANE_S1, lo_i, hi_i,
            ribbon=(RIBBON_FAST, RIBBON_SLOW), era=era)
        out["tally"][sym], out["refused"][sym] = tal, ref
    out["toll"] = stamp_toll(out["trades"], "5m", anchor,
                             tuned["band"] if anchor == ANCHOR_BAND else None)
    out["book"] = TP.external_book(out["trades"], g, lo_ms, hi_ms)
    return out


def run_lane_i1(panel, reg_id: str, text: str, arm: str, signals: dict,
                head_of_record=None, anchor: str = ANCHOR_MEMORY, card=None,
                roles=None, tuned: dict | None = None,
                lo_ms: int | None = None, hi_ms: int | None = None,
                reg_root: Path | None = None) -> dict:
    """P-BRK-I1 · THE INVESTOR, 1d.  GATE FIRST, THEN BARS.

    1d macro DIE -> first memory-line flip-hold (FROZEN 1.0 ATR / 6 bars) ->
    enter at the close of bar flip.i + FLIP_HOLD_BARS; stop beyond the retest
    extreme railed 1.0 ATR(1d); permission = weekly 12>25 posture on the last
    CLOSED Monday-week AND daily DIRECTION from the R4 lifecycle; v6 management
    lens-scaled with the 12/25 bell; full corridor [R2]; net of 10 bps +
    funding by interval sum.
    """
    g = gate(reg_id, text, arm, panel, LANE_I1, head_of_record, reg_root)
    era = require_lane_era(LANE_I1, g)      # [B9] the DECLARED pin, ENFORCED
    card = card or TP.CONTROL_CARD
    roles = roles or T9.V6_ROLES
    e_lo, e_hi, e_meta = TP.corridor_era(g["panel"], era)
    lo_ms = e_lo if lo_ms is None else max(int(lo_ms), e_lo)
    hi_ms = e_hi if hi_ms is None else min(int(hi_ms), e_hi)
    out = {"gate": g, "era": era, "window": (lo_ms, hi_ms), "meta": e_meta,
           "anchor": anchor, "trades": [], "tally": {}, "refused": {}}
    missing = [s for s in g["panel"] if s not in signals]
    if missing:
        raise SystemExit(f"HALT: run_lane_i1 was handed no macro signals for "
                         f"{missing}. Signals ARRIVE AS ARGUMENTS (§12's "
                         f"adapter builds them); this runner reaches no range "
                         f"code and cannot make them up.")
    for sym in g["panel"]:
        lf = frame_l(sym, "1d")
        w1 = frame_l(sym, "1w", with_funding=False)
        sig = signals[sym]
        if anchor == ANCHOR_MEMORY:
            cands, tal = memory_flip_candidates(lf.h, lf.l, sig["dies"],
                                                sig["flips"], lf.n)
        else:
            t_ = tuned or tuned_pins("1d")
            band = r1_band(t_["band"])
            lo, hi = band(lf.c)
            cands, tal = band_hold_candidates(
                lf.h, lf.l, lf.c, lf.atr, sig["dies"], lo, hi,
                t_["margin_atr"], t_["hold_bars"], t_["ttl_bars"])
        life = ribbon_lifecycle(lf.c, lf.atr)
        wk = weekly_posture(w1.c)
        widx = visible_htf_idx(lf.open_ms, w1.open_ms, w1.step_ms)
        legs, ref = legs_from_candidates(
            lf, cands, LANE_I1,
            permit=lambda i, d, _l=life, _w=wk, _x=widx:
                i1_permission(i, d, _l["direction"], _w, _x))
        lo_i, hi_i = idx_range(lf.open_ms, lo_ms, hi_ms)
        out["trades"] += brk_campaigns(lf, legs, card, roles, LANE_I1,
                                       lo_i, hi_i,
                                       ribbon=(RIBBON_FAST, RIBBON_SLOW),
                                       era=era)
        out["tally"][sym], out["refused"][sym] = tal, ref
    out["book"] = TP.external_book(out["trades"], g, lo_ms, hi_ms)
    return out


# ══════════════════════════════════ 12 · THE ADAPTERS — THE ONE RANGE DOORWAY
def macro_signals(sym: str, lens: str, scale_mult: float = FROZEN_SCALE) -> dict:
    """THE ONLY PLACE IN THIS FILE THAT REACHES THE RANGE MACHINE, and it does
    so through a FUNCTION-LOCAL import so that the range machine never enters
    the module-level closure of the decision half (F-BR-14's law, extended).

    Returns {'dies': [(die_i, rid, side)], 'flips': [{'i','polarity','rid'}],
    'scale_mult': ...} — plain numbers.  A decision function never calls this;
    a RUNNER does, and hands the result in as an argument.

    THE TAPE IS THE WHOLE TAPE, AND THAT IS A DEPENDENCY WORTH NAMING [B5].
    A lane run on the HOLDOUT era detects its DIEs here on the FULL history
    and is then windowed; the R1 tuning detected ITS DIEs on tapes CUT at the
    era boundary before the detector ever ran (`tierc10_census.era_cut`).  The
    two agree only because the macro detector is AS-OF — no event moves when
    later bars arrive — and if that ever stopped being true, the holdout would
    be contaminated by the shape of the tuning era and nothing in this module
    would notice.  So it is checked rather than assumed: F-BRK-ERA re-runs the
    detector on the full tape and on the cut tape and demands the events below
    the cut be IDENTICAL, triple (i, rid, side) for triple.

    WHAT WOULD MAKE THIS WRONG: importing `tierc10_census` at module level (it
    reaches `analytics.rangefinder_census`), or returning the machine's own
    objects instead of numbers — a decision path that held a live event object
    could read a field stamped after its bar.
    """
    import tierc10_census as C                              # noqa: PLC0415
    tape = C.load_tape(sym, lens)
    m = C.run_scale(tape, float(scale_mult))
    macro, leash = m["macro"], m["leash"]
    dies = [(int(e["i"]), int(e["rid"]), str(e["side"]))
            for e in macro["events"] if e["event"] == "breakout-die"]
    dies.sort(key=lambda x: x[0])
    flips = [{"i": int(e["i"]), "polarity": str(e["polarity"]),
              "rid": int(e["rid"])}
             for e in leash if e.get("event") == "flip"]
    return {"dies": dies, "flips": flips, "scale_mult": float(scale_mult),
            "lens": lens, "sym": sym, "n_bars": int(tape.n)}


def grid_toll_atr(asset: str, lens: str, cls: str,
                  scale_kind: str = "frozen3.0", horizon: str | None = None,
                  grid_path: Path | None = None) -> float:
    """THE TOLL, READ FROM THE FILED GRID [F-C10-TOLL] — never typed.

    `tierc10_census.get_toll` HALTs on a missing grid, a missing row or a NaN,
    which is the behaviour this lane wants: a toll that cannot be read is not a
    toll that may be guessed.  Function-local import, same law as above.
    """
    import tierc10_census as C                              # noqa: PLC0415
    return float(C.get_toll(asset, lens, cls, scale_kind=scale_kind,
                            horizon=horizon, grid_path=grid_path))


def stamp_toll(trades: list, lens: str, anchor: str, band: str | None = None,
               horizon: str | None = None) -> dict:
    """P-BRK-S1's "NET OF MEASURED 5m TOLL", as a PRINT beside the book [(E)].

    A trade book's exact cost is its per-trade fee, which `account_l` already
    books; the contract's "measured toll" is the census grid's `toll_atr` for
    the class this lane enters on, expressed as a share of 1R.  It is READ, per
    asset, from the filed grid — `toll_class()` names the row and `get_toll`
    HALTs if the grid has none — and stamped on each campaign as
    `toll_atr_grid` / `toll_pct_of_1r`.

    Returns the per-asset tolls that were read, so the doc quotes THIS dict and
    never a literal.
    """
    cls = toll_class(anchor, band)
    seen: dict = {}
    for t in trades:
        a = str(t.symbol)
        if a not in seen:
            seen[a] = grid_toll_atr(a, lens, cls)
        object.__setattr__(t, "toll_atr_grid", seen[a])
        object.__setattr__(t, "toll_pct_of_1r",
                           toll_pct_of_1r(seen[a], t.r_dist, t.atr_at_entry))
    return {"cls": cls, "lens": lens, "horizon": horizon, "per_asset": seen}


# ═══════════════════════ 14 · THE ROW — THE CONTRACT'S LINE 112, ASSEMBLED
# "Each BRK form also prints the OTHER anchor (EMA band <-> memory-line) as
#  Tier-E, and carries its lens's height-vs-toll verdict ON ITS ROW."
#      — RESUME contract 2026-09-22, line 112.
# "The 17-asset view prints as Tier-E beside each BRK row." — operator R8.
#
# THE MECHANISM ALREADY EXISTED AND THE ASSEMBLY DID NOT.  `LANE_ANCHOR` /
# `LANE_TIER_E_ANCHOR` name the two anchors, both runners take `anchor=`, and
# `stamp_toll` stamps the toll — but nothing put the three of them on one row,
# so there was no row for a verdict to ride on and `brk/` held no table at all.
#
# WHAT THIS SECTION MAY NOT DO, AND DOES NOT.  It computes NO verdict.  The
# height-vs-toll verdict is the CENSUS track's measurement ([Q-R3]) and is
# READ from its filed table through `height_vs_toll()`; until that table
# exists the slot holds a `PendingVerdict` whose every read HALTs.  The
# REGISTRATION's own verdict (the ruler, the p against the FDR bar) is the
# panel module's and is not computed here either: the row carries the journal
# and its provenance, and `TP.score` / `TP.headline_n` remain the only things
# that turn a journal into a verdict.  LAW 4 is the reason: no BRK
# registration exists, so no real Book can be offered to this function at all,
# and every row built today is built on a SYNTHETIC campaign.

def verdict_asset_of(panel, override: str | None = None,
                     why: str | None = None) -> dict:
    """WHICH CENSUS ROW THIS BOOK'S VERDICT IS, DERIVED FROM THE BOOK.

    [review round 2, 2026-09-22, finding 1]  The verdict slot used to default
    to POOLED:CLASSIC5 for ANY book.  It is now derived:

        TP.panel_name(panel) == 'CLASSIC5' -> 'POOLED:CLASSIC5'
        TP.panel_name(panel) == 'UNSEEN12' -> 'POOLED:UNSEEN12'
        a ONE-ASSET panel                  -> that symbol's own census row
        anything else                      -> HALT

    PANEL17 falls in the HALT case on purpose.  The census does file a
    POOLED:ALL row whose `as_of_n_assets` is 17, but POOLED:ALL is the CENSUS
    COMMISSION's pool: nothing filed states its membership is this panel's,
    and quietly mapping PANEL17 onto it would be the very assumption this
    repair exists to remove — the same default wearing a new coat.  R8 orders
    a Tier-E 17-asset print beside each BRK row; when that arm is filed the
    operator names its census counterpart with `verdict_asset=` and says why,
    or the census files a PANEL17 row.

    `override` is an EXPLICIT OVERRIDE and never a fallback: an override that
    disagrees with the derived label HALTs unless `why` states the reason,
    and an override where nothing can be derived REQUIRES `why`.

    Returns the choice AND its provenance, which rides the row as
    `height_vs_toll_asset` and prints on it.
    """
    pnl = tuple(str(x) for x in (panel or ()))
    if not pnl:
        raise SystemExit(
            "HALT: a BRK row's [Q-R3] verdict asset is DERIVED from the "
            "Book's panel, and the Book offered an EMPTY panel. A row with no "
            "panel has no census counterpart to read, and a default would be "
            "an invented measurement wearing a census row's name [B10].")
    name = TP.panel_name(pnl)
    if name in CENSUS_ASSET_OF_PANEL:
        derived = CENSUS_ASSET_OF_PANEL[name]
        how = (f"panel {name} -> the census's pooled label {derived!r} "
               f"(CENSUS_ASSET_OF_PANEL)")
    elif len(pnl) == 1:
        derived = pnl[0]
        how = (f"a ONE-ASSET panel reads that symbol's OWN census row "
               f"({derived!r}), not a pool's")
    else:
        derived, how = None, None
    ov = str(override) if override else None
    wy = str(why).strip() if why and str(why).strip() else None
    if derived is None and ov is None:
        raise SystemExit(
            f"HALT: the [Q-R3] verdict row for a BRK row on panel {name} "
            f"({len(pnl)} assets: {list(pnl)}) cannot be DERIVED. The census "
            f"files its rows under the pooled labels "
            f"{list(CENSUS_POOL_LABELS)} and under single symbols; this "
            f"module maps {sorted(CENSUS_ASSET_OF_PANEL)} onto "
            f"{[CENSUS_ASSET_OF_PANEL[k] for k in sorted(CENSUS_ASSET_OF_PANEL)]} "
            f"and a one-asset panel onto its own symbol, and it has NO "
            f"counterpart for this one. PANEL17 has none today: the census's "
            f"{CENSUS_POOL_LABELS[0]!r} is the CENSUS COMMISSION's pool and "
            f"nothing filed proves its membership is this panel's. Name the "
            f"row explicitly with verdict_asset= AND state verdict_asset_why=, "
            f"or have the census file the counterpart. A DEFAULT here is what "
            f"this HALT replaced: before the repair every book, this one "
            f"included, silently received POOLED:CLASSIC5's figures. "
            f"{VERDICT_ASSET_LAW}")
    if ov is not None and derived is not None and ov != derived and wy is None:
        raise SystemExit(
            f"HALT: the [Q-R3] verdict asset was OVERRIDDEN to {ov!r} for a "
            f"row on panel {name} ({list(pnl)}), whose DERIVED census "
            f"counterpart is {derived!r} ({how}). An override that disagrees "
            f"with the derivation is a deliberate act and must say why: pass "
            f"verdict_asset_why='...'. Silence here is how a row comes to "
            f"wear another panel's verdict. {VERDICT_ASSET_LAW}")
    if ov is not None and derived is None and wy is None:
        raise SystemExit(
            f"HALT: the [Q-R3] verdict asset was set to {ov!r} for a row on "
            f"panel {name} ({list(pnl)}), for which NOTHING can be derived. "
            f"An override standing in for an impossible derivation must say "
            f"why: pass verdict_asset_why='...'. {VERDICT_ASSET_LAW}")
    asset = ov if ov is not None else derived
    return {
        "asset": str(asset),
        "panel_name": name,
        "n_panel_assets": len(pnl),
        "derived": derived,
        "derived_how": (how if derived is not None else
                        "NOTHING DERIVABLE — the census files no counterpart "
                        "for this panel"),
        "override": ov,
        "override_why": wy,
        "source": ("DERIVED FROM THE BOOK" if ov is None else
                   ("EXPLICIT OVERRIDE, agreeing with the derivation"
                    if ov == derived else "EXPLICIT OVERRIDE, stated")),
        "law": VERDICT_ASSET_LAW,
    }


def height_vs_toll_spec() -> dict:
    """THE INTERFACE, AS A PRINTABLE CLAIM — what this module will read, from
    where, under which key, and who owns it.  It rides the mechanics card and
    the build manifest so the census track can read the requirement off the
    artifact instead of off a conversation."""
    return {
        "status": HEIGHT_VS_TOLL_STATUS,
        "path": str(HEIGHT_VS_TOLL_PATH),
        "verdict_path": str(HEIGHT_VS_TOLL_VERDICT_PATH),
        "two_tables_why": ("the census keys its FIGURES on "
                           + str(list(HEIGHT_VS_TOLL_KEY)) + " and its "
                           "VERDICT on " + str(list(HEIGHT_VS_TOLL_VERDICT_KEY))
                           + " — the verdict table carries NO era column — so "
                           "this is a two-table read keyed differently on each "
                           "side, cross-checked on the figures both carry."),
        "key": list(HEIGHT_VS_TOLL_KEY),
        "verdict_key": list(HEIGHT_VS_TOLL_VERDICT_KEY),
        "required_fields": list(HEIGHT_VS_TOLL_FIELDS),
        "required_verdict_fields": list(HEIGHT_VS_TOLL_VERDICT_FIELDS),
        "required_verdict_columns": _hvt_required("VERDICT"),
        "required_figures_columns": _hvt_required("FIGURES"),
        "cross_checked_fields": list(HEIGHT_VS_TOLL_AGREE),
        "cross_checked_law_fields": list(HEIGHT_VS_TOLL_AGREE_STR),
        "cross_check_on_absence": (
            "HALT. An absent shared column SEVERS the join between the "
            "era-keyed figures row and the era-less verdict row, so it stops "
            "the read; it used to be SKIPPED while `cross_checked` went on "
            "attesting the constant. `cross_checked` on a returned row is "
            "the list the comparison ACTUALLY built [review round 2, "
            "finding 2]."),
        "as_of_column_required": HEIGHT_VS_TOLL_ASOF_COL,
        "as_of_required_value": as_of_of_record(),
        "asset_values": ("a PANEL symbol, or the census's pooled labels "
                         "POOLED:ALL / POOLED:CLASSIC5 / POOLED:UNSEEN12"),
        "lens_values": list(LENSES),
        "scale_kind_read": HEIGHT_VS_TOLL_SCALE,
        "era_read": HEIGHT_VS_TOLL_ERA,
        "asset_read": {
            "law": VERDICT_ASSET_LAW,
            "derived_by": ("tierc10_brk.verdict_asset_of("
                           "book.spec['panel'], verdict_asset, "
                           "verdict_asset_why)"),
            "panel_to_census_label": dict(sorted(
                CENSUS_ASSET_OF_PANEL.items())),
            "one_asset_panel": ("reads that symbol's OWN census row, not a "
                                "pool's"),
            "no_counterpart": ("HALT, naming the panel and the labels the "
                               "census carries. PANEL17 has none today."),
            "census_pool_labels": list(CENSUS_POOL_LABELS),
            "override": ("verdict_asset= is an EXPLICIT OVERRIDE only; one "
                         "that disagrees with the derived label HALTs unless "
                         "verdict_asset_why= states the reason"),
            "printed_on_the_row": "height_vs_toll_asset",
            "was": ("DEFAULTED to 'POOLED:CLASSIC5' for any book until "
                    "2026-09-22 [review round 2, finding 1]"),
        },
        "provisional_policy": (
            "the census files a `provisional` flag and a minimum-n floor; a "
            "flagged row HALTs here unless allow_provisional=True, and when "
            "taken by name it rides the row as provisional / "
            "provisional_reason / sample_floor and PRINTS. The floor itself "
            "is READ off the row (min_n_ranges_pinned, "
            "edge_min_n_ranges_pinned) and is not re-pinned by this module."),
        "provisional_columns_required": list(
            HEIGHT_VS_TOLL_PROVISIONAL_FIELDS),
        "verdict_vocabulary": ("NOT PINNED HERE — the census's own three "
                               "fields (verdict_pass, verdict_law, reason) "
                               "are carried through VERBATIM. This module "
                               "reads a verdict; it never names one, never "
                               "restates one as a string of its own, and "
                               "never computes one."),
        "owner": HEIGHT_VS_TOLL_OWNER,
        "on_absence": ("HALT. The row's verdict slot holds a PendingVerdict "
                       "whose every read raises SystemExit, so a row can be "
                       "assembled and named PENDING but can never be printed "
                       "or serialised as though the verdict existed."),
    }


class PendingVerdict:
    """THE VERDICT SLOT BEFORE [Q-R3] EXISTS — an object that cannot be read.

    A `None` in this slot would serialise to `null` and print as a blank, and
    a blank in a verdict column is the kind of thing a later reader fills in
    from memory.  So the empty slot is an OBJECT whose every read — `str`,
    `repr`, `format`, `float`, `int`, `bool`, `len`, iteration, indexing, and
    any attribute but the key it was built with — raises SystemExit naming the
    table that is missing.  `json.dumps(..., default=str)` therefore HALTs
    too, which is the point: a row with an unread verdict cannot be filed.

    COMPARISON IS A READ TOO (review, 2026-09-22).  `__eq__`/`__ne__` were
    left at object identity, so `pv == 'PASS'` came back False SILENTLY and a
    downstream `if row['height_vs_toll'] != 'TOLL DOMINATES': ship()` would
    have proceeded on an UNREAD verdict.  Asking whether an absent
    measurement equals something is asking what it says, so the six rich
    comparisons HALT as well.  `pv is None` still answers False — identity is
    not a read, and the module's own `is not None` printing path needs it.

    The KEY fields stay readable (`lens`, `asset`, `scale_kind`, `era`,
    `path`, `verdict_path`) because they are the request, not the answer — a
    reporter must be able to say WHICH verdict is missing without tripping
    the guard.
    """
    __slots__ = ("lens", "asset", "scale_kind", "era", "path", "verdict_path")

    def __init__(self, lens: str, asset: str, scale_kind: str, era: str,
                 path, verdict_path=None) -> None:
        self.lens, self.asset = str(lens), str(asset)
        self.scale_kind, self.era = str(scale_kind), str(era)
        self.path = str(path)
        self.verdict_path = str(verdict_path if verdict_path is not None
                                else HEIGHT_VS_TOLL_VERDICT_PATH)

    def _halt(self, *a, **k):
        raise SystemExit(
            f"HALT: the height-vs-toll VERDICT for lens {self.lens!r} "
            f"(asset {self.asset!r}, scale {self.scale_kind!r}, era "
            f"{self.era!r}) was READ, but {HEIGHT_VS_TOLL_OWNER} has filed no "
            f"readable table at {self.path} (verdict table "
            f"{self.verdict_path}). The BRK row CARRIES its lens's verdict; "
            f"it does not compute one, and a default would be an invented "
            f"measurement wearing a census row's name. Expected key "
            f"{list(HEIGHT_VS_TOLL_KEY)} and fields "
            f"{list(HEIGHT_VS_TOLL_FIELDS)}, plus verdict key "
            f"{list(HEIGHT_VS_TOLL_VERDICT_KEY)} and fields "
            f"{list(HEIGHT_VS_TOLL_VERDICT_FIELDS)}. Either file [Q-R3] or "
            f"leave the slot PENDING and unread.")

    __str__ = __repr__ = __format__ = __float__ = __int__ = _halt
    __bool__ = __len__ = __iter__ = __getitem__ = __hash__ = _halt
    # COMPARISON IS A READ: identity-equality here is a SILENT False, which
    # is the one answer an unread verdict must never give.  `__hash__` above
    # stays a HALT and is in this namespace, so defining `__eq__` does not
    # get it replaced with None.
    __eq__ = __ne__ = __lt__ = __le__ = __gt__ = __ge__ = _halt

    def __getattr__(self, name):                # slots resolve before this
        if name.startswith("_"):
            raise AttributeError(name)
        self._halt()


def _hvt_required(what: str) -> list:
    """THE COLUMNS A [Q-R3] TABLE MUST CARRY, BY SIDE OF THE JOIN.

    [review round 2, finding 2]  This used to be `key + fields + as_of` on
    BOTH sides, and HEIGHT_VS_TOLL_AGREE was NOT in the verdict side's set —
    so a verdict table lacking n_ranges / height_atr_median / toll_atr_median
    passed every column check and the two-table cross-check then compared
    NOTHING while still attesting all three.  The shared figures are now
    REQUIRED of the verdict table, which is the first of the two guards: the
    absent column cannot reach the comparison loop at all.
    """
    if what == "VERDICT":
        want = (list(HEIGHT_VS_TOLL_VERDICT_KEY)
                + list(HEIGHT_VS_TOLL_VERDICT_FIELDS)
                + list(HEIGHT_VS_TOLL_AGREE)
                + list(HEIGHT_VS_TOLL_AGREE_STR)
                + list(HEIGHT_VS_TOLL_PROVISIONAL_FIELDS)
                + [HEIGHT_VS_TOLL_ASOF_COL])
    else:
        want = (list(HEIGHT_VS_TOLL_KEY) + list(HEIGHT_VS_TOLL_FIELDS)
                + list(HEIGHT_VS_TOLL_AGREE)
                + list(HEIGHT_VS_TOLL_AGREE_STR)
                + [HEIGHT_VS_TOLL_ASOF_COL])
    out: list = []
    for c in want:
        if c not in out:
            out.append(c)
    return out


def _hvt_shared_or_halt(r, v, p: Path, vp: Path, sel: dict) -> list:
    """THE ONLY EVIDENCE THE TWO ROWS ARE ONE MEASUREMENT [H1] — compared,
    never skipped, and the list it RETURNS is what was ACTUALLY compared.

    The figures table is keyed with an `era` and the verdict table without
    one, so nothing in the join proves the two rows describe the same
    measurement except the columns they share.  An ABSENT shared column
    SEVERS that join, so it HALTs; it used to `continue`, which turned the
    cross-check into a no-op while `out['cross_checked']` went on attesting
    all three fields from the constant.  The attestation can no longer
    outrun the check, because the attestation IS the check's own output.
    """
    shared = list(HEIGHT_VS_TOLL_AGREE) + list(HEIGHT_VS_TOLL_AGREE_STR)
    missing = [f_ for f_ in shared
               if f_ not in v.index or f_ not in r.index]
    if missing:
        raise SystemExit(
            f"HALT: the [Q-R3] cross-check cannot run — the shared column(s) "
            f"{missing} are absent from the FIGURES row in {p} and/or the "
            f"VERDICT row in {vp} for "
            f"{ {k: sel[k] for k in HEIGHT_VS_TOLL_KEY} }. The figures are "
            f"keyed on {list(HEIGHT_VS_TOLL_KEY)} and the verdict on "
            f"{list(HEIGHT_VS_TOLL_VERDICT_KEY)} — the verdict table carries "
            f"NO era — so the columns BOTH tables carry "
            f"({shared}) are the ONLY evidence the two rows are one "
            f"measurement. Their absence SEVERS the join, and a severed join "
            f"read anyway is a verdict of unknown provenance riding a BRK "
            f"row. This is a HALT and not a skip [review round 2, finding 2].")
    compared, disagree = [], {}
    for f_ in HEIGHT_VS_TOLL_AGREE:
        a_, b_ = _num(r[f_]), _num(v[f_])
        compared.append(f_)
        if a_ != b_:
            disagree[f_] = (a_, b_)
    for f_ in HEIGHT_VS_TOLL_AGREE_STR:
        a_, b_ = str(r[f_]), str(v[f_])
        compared.append(f_)
        if a_ != b_:
            disagree[f_] = (a_, b_)
    if disagree:
        raise SystemExit(
            f"HALT: the [Q-R3] FIGURES row in {p} and the VERDICT row in "
            f"{vp} disagree on {sorted(disagree)} "
            f"(figures vs verdict: {disagree}) for "
            f"{ {k: sel[k] for k in HEIGHT_VS_TOLL_KEY} }. The verdict table "
            f"carries no era, so the shared figures are the ONLY evidence "
            f"the two rows are one measurement; without it a BRK row would "
            f"carry an 'ALL'-era height beside some other era's verdict.")
    return compared


def _hvt_provisional_or_halt(v, sel: dict, vp: Path, allow: bool) -> tuple:
    """A PROVISIONAL CENSUS ROW NEVER REACHES A BRK ROW QUIETLY.

    The census re-filed [Q-R3] with a `provisional` flag and a minimum-n
    floor, and its own reader HALTs on such a row unless the caller asks for
    it by name.  This module reads the PARQUET directly, so it would have
    bypassed that refusal entirely: BTCUSDT 1d (n_ranges 11, edge_n_ranges
    11, floor 30) read clean here before this guard existed.  The floor is
    READ OFF THE ROW (`min_n_ranges_pinned` / `edge_min_n_ranges_pinned`) and
    never re-pinned here — one law, one copy.
    """
    prov = v["provisional"]
    if not isinstance(prov, (bool, np.bool_)):
        raise SystemExit(
            f"HALT: the [Q-R3] VERDICT row for "
            f"{ {k: sel[k] for k in HEIGHT_VS_TOLL_VERDICT_KEY} } in {vp} "
            f"carries provisional={prov!r} ({type(prov).__name__}), which is "
            f"not a boolean. A sample-floor flag read from a non-boolean is a "
            f"flag this module decided, not one the census filed.")
    prov = bool(prov)
    reason = str(v["provisional_reason"] if v["provisional_reason"] is not None
                 else "")
    if reason.strip().lower() in ("nan", "none"):
        reason = ""
    if prov and not reason.strip():
        raise SystemExit(
            f"HALT: the [Q-R3] VERDICT row for "
            f"{ {k: sel[k] for k in HEIGHT_VS_TOLL_VERDICT_KEY} } in {vp} is "
            f"flagged provisional=True but carries no provisional_reason. A "
            f"flag with no stated floor behind it is not one a BRK row can "
            f"print.")
    if prov and not allow:
        raise SystemExit(
            f"HALT: the [Q-R3] VERDICT row for "
            f"{ {k: sel[k] for k in HEIGHT_VS_TOLL_VERDICT_KEY} } in {vp} is "
            f"PROVISIONAL — {reason}. n_ranges {int(v['n_ranges'])} against "
            f"the filed floor min_n_ranges_pinned "
            f"{int(v['min_n_ranges_pinned'])}; edge_n_ranges "
            f"{int(v['edge_n_ranges'])} against edge_min_n_ranges_pinned "
            f"{int(v['edge_min_n_ranges_pinned'])}. The census files it and "
            f"it is readable AS DATA; it is NOT served to a BRK row that did "
            f"not ask for it by name. Pass allow_provisional=True to take it "
            f"— the row then CARRIES provisional=True and this reason and "
            f"PRINTS them — or read a row that clears the floor. The quiet "
            f"path is the safe one [census F-C10-HT-PROVISIONAL].")
    return prov, reason


def _hvt_one(p: Path, key: tuple, fields: tuple, sel: dict, what: str):
    """EXACTLY ONE ROW of a filed census table, under `key`, or a HALT.

    HALTS IF: the table is absent; a declared key/field/as-of column is
    missing; the key selects zero or more than one row; or the row's as-of
    stamp is not this corridor's.  Shared by the FIGURES table and the
    VERDICT table, which are keyed differently and must be read the same way.
    """
    import pandas as pd                                       # noqa: PLC0415
    if not p.exists():
        raise SystemExit(
            f"HALT: no height-vs-toll {what} table at {p}. It is owned by "
            f"{HEIGHT_VS_TOLL_OWNER}; the BRK row READS it and computes "
            f"nothing. Expected key {list(key)} and fields {list(fields)}.")
    df = pd.read_parquet(p)
    want = _hvt_required(what)
    missing = [c for c in want if c not in df.columns]
    if missing:
        raise SystemExit(
            f"HALT: the {what} table {p} is missing the declared column(s) "
            f"{missing}; it holds {sorted(df.columns)}. The BRK row's "
            f"interface to [Q-R3] on the {what} side is {want} — key "
            f"{list(key)} + fields {list(fields)} + the shared cross-check "
            f"columns {list(HEIGHT_VS_TOLL_AGREE)} / "
            f"{list(HEIGHT_VS_TOLL_AGREE_STR)}"
            + (f" + the sample-floor columns "
               f"{list(HEIGHT_VS_TOLL_PROVISIONAL_FIELDS)}"
               if what == "VERDICT" else "")
            + f" + the as-of stamp {HEIGHT_VS_TOLL_ASOF_COL!r}.")
    m = np.ones(len(df), dtype=bool)
    for k in key:
        m &= (df[k].astype(str) == str(sel[k])).to_numpy()
    q = df[m]
    if len(q) != 1:
        raise SystemExit(
            f"HALT: the {what} table {p} holds {len(q)} row(s) for "
            f"{ {k: str(sel[k]) for k in key} } — a verdict must be exactly "
            f"one row of the table, and a repeated key is as unreadable as "
            f"an absent one.")
    r = q.iloc[0]
    stamp = str(r[HEIGHT_VS_TOLL_ASOF_COL])
    if stamp != as_of_of_record():
        raise SystemExit(
            f"HALT: the {what} row in {p} is stamped "
            f"{HEIGHT_VS_TOLL_ASOF_COL}={stamp!r}, not this corridor's "
            f"{as_of_of_record()!r}. A BRK row carries the AS-OF WARRANTY; a "
            f"measurement true of another instant may not ride on it.")
    return r


def height_vs_toll(lens: str, asset: str,
                   scale_kind: str = HEIGHT_VS_TOLL_SCALE,
                   era: str = HEIGHT_VS_TOLL_ERA,
                   path: Path | None = None,
                   verdict_path: Path | None = None,
                   allow_provisional: bool = False) -> dict:
    """THE [Q-R3] VERDICT, READ FROM THE CENSUS TRACK'S TWO FILED TABLES —
    never computed, never defaulted, never guessed.

    The same law `grid_toll_atr` is held to, for the same reason: a
    measurement that cannot be READ is not one that may be invented.  The
    census's own verdict fields — `verdict_pass` (bool), `verdict_law`,
    `reason` — are carried through VERBATIM; this module pins no vocabulary,
    because the vocabulary is [Q-R3]'s.

    TWO TABLES, TWO KEYS, ONE CROSS-CHECK.  The FIGURES carry `era` and the
    VERDICT does not, so the figures are keyed on (asset, lens, scale_kind,
    era) and the verdict on (asset, lens, scale_kind) alone.  Nothing in that
    join guarantees the two rows are about the same measurement, so the
    columns BOTH tables carry (HEIGHT_VS_TOLL_AGREE, plus the law half
    HEIGHT_VS_TOLL_AGREE_STR) are REQUIRED of the verdict table, are
    compared, and a disagreement HALTs.  `cross_checked` is the list the
    comparison actually built, never the constant, so the attestation cannot
    outrun the check [review round 2, finding 2].  They agree today: 13025 /
    6.480873 / 0.292654 on both sides for 5m POOLED:CLASSIC5.

    THE SAMPLE FLOOR.  The census re-filed [Q-R3] with a `provisional` flag;
    a flagged row HALTs unless `allow_provisional=True`, and when taken
    knowingly it rides the returned dict as provisional / provisional_reason
    and PRINTS on the row.

    HALTS IF: either table is absent; a declared key, field, shared
    cross-check column, sample-floor column or as-of column is missing;
    either key selects zero or more than one row; either row is stamped at
    another as-of; the two rows disagree on a shared figure or on
    gate_law_sha; the row is provisional and was not asked for by name; or
    the verdict fields are null/blank/non-boolean.
    """
    p = Path(path) if path is not None else HEIGHT_VS_TOLL_PATH
    vp = (Path(verdict_path) if verdict_path is not None
          else HEIGHT_VS_TOLL_VERDICT_PATH)
    sel = {"asset": str(asset), "lens": str(lens),
           "scale_kind": str(scale_kind), "era": str(era)}
    r = _hvt_one(p, HEIGHT_VS_TOLL_KEY, HEIGHT_VS_TOLL_FIELDS, sel, "FIGURES")
    v = _hvt_one(vp, HEIGHT_VS_TOLL_VERDICT_KEY, HEIGHT_VS_TOLL_VERDICT_FIELDS,
                 sel, "VERDICT")
    # ── the two rows are about the SAME measurement, or neither is read ──
    compared = _hvt_shared_or_halt(r, v, p, vp, sel)
    # ── and the row clears the census's own sample floor, or is taken by
    # ── NAME and carries the flag onto whatever it rides ─────────────────
    prov, prov_reason = _hvt_provisional_or_halt(v, sel, vp,
                                                 bool(allow_provisional))
    vp_ = v["verdict_pass"]
    if isinstance(vp_, (bool, np.bool_)):
        passed = bool(vp_)
    else:
        raise SystemExit(
            f"HALT: the height-vs-toll VERDICT row for lens {lens!r} / asset "
            f"{asset!r} in {vp} carries verdict_pass={vp_!r} "
            f"({type(vp_).__name__}), which is not a boolean. A verdict slot "
            f"filled from a non-boolean is a verdict this module invented.")
    for f_ in ("verdict_law", "reason"):
        t = v[f_]
        if t is None or (isinstance(t, float) and not np.isfinite(t)) \
                or not str(t).strip() \
                or str(t).strip().lower() in ("nan", "none"):
            raise SystemExit(
                f"HALT: the height-vs-toll row for lens {lens!r} / asset "
                f"{asset!r} exists in {vp} but carries no {f_} ({t!r}). A "
                f"verdict with no law and no reason behind it is not a "
                f"verdict a BRK row may print.")
    out = {k: str(r[k]) for k in HEIGHT_VS_TOLL_KEY}
    for f_ in HEIGHT_VS_TOLL_FIELDS:
        val = r[f_]
        out[f_] = (None if val is None
                   or (isinstance(val, float) and not np.isfinite(val))
                   else (int(val) if f_ in HEIGHT_VS_TOLL_INT_FIELDS
                         else round(float(val), ROW_ROUND_ND)))
    out["verdict_pass"] = passed
    out["verdict_law"] = str(v["verdict_law"])
    out["reason"] = str(v["reason"])
    out["provisional"] = prov
    out["provisional_reason"] = prov_reason
    out["provisional_taken_by_name"] = bool(allow_provisional) if prov else False
    out["sample_floor"] = {
        "n_ranges": int(v["n_ranges"]),
        "min_n_ranges_pinned": int(v["min_n_ranges_pinned"]),
        "edge_n_ranges": int(v["edge_n_ranges"]),
        "edge_min_n_ranges_pinned": int(v["edge_min_n_ranges_pinned"]),
        "read_not_pinned_here": ("the floor is READ off the census row; this "
                                 "module keeps no second copy of it"),
    }
    out["gate_law_sha"] = str(v["gate_law_sha"])
    out["as_of_last_closed_4h"] = as_of_of_record()
    out["source"] = str(p)
    out["verdict_source"] = str(vp)
    # THE ATTESTATION IS THE CHECK'S OWN OUTPUT, never the constant
    # [review round 2, finding 2].
    out["cross_checked"] = compared
    out["read_not_computed"] = True
    return out


# ── THE FIGURES ONE RUN CONTRIBUTES TO A ROW ────────────────────────────────
def _num(x):
    """A float rounded to the house precision, or None — so two assemblies of
    the same journal are the same bytes (DETERMINISM)."""
    if x is None:
        return None
    x = float(x)
    return None if not np.isfinite(x) else round(x, ROW_ROUND_ND)


def _figures(run: dict, tier: str) -> dict:
    """WHAT ONE RUN OF ONE ANCHOR CONTRIBUTES — counts, the journal's own
    per-campaign sums, and the refusal tallies.  No ruler, no p, no verdict:
    turning a journal into a verdict is `TP.score`'s job and nobody else's.

    HALTS IF: `run` carries no `TP.Book`.  A Book is the journal WEARING the
    gate it entered through; a plain list has no registration behind it, and
    a row assembled on one would be a number with no text before it.  No BRK
    registration exists today, so no real Book can be offered at all — which
    is exactly why every row built today is built on a synthetic campaign.
    """
    book = run.get("book")
    if not isinstance(book, TP.Book):
        raise SystemExit(
            f"HALT: a BRK row is assembled from a TP.Book — the journal "
            f"wearing the gate it entered through (TP.external_book) — and "
            f"from nothing else; got {type(book).__name__}. A filtered book, "
            f"a list or a hand-built record has no registration behind it. "
            f"[LAW 4] No BRK registration is filed, so no real Book exists "
            f"today and every row is a SYNTHETIC one.")
    tr = list(book)
    per: dict = {}
    for t in tr:
        per[str(t.symbol)] = per.get(str(t.symbol), 0) + 1
    nets = [float(t.net_r) for t in tr if t.net_r is not None]
    tolls = [float(getattr(t, "toll_pct_of_1r", float("nan"))) for t in tr]
    tolls = [x for x in tolls if np.isfinite(x)]
    ref: dict = {}
    for _sym, d in sorted((run.get("refused") or {}).items()):
        for k_, v_ in sorted(dict(d).items()):
            ref[k_] = ref.get(k_, 0) + int(v_)
    return {
        "tier": tier,
        "anchor": str(run["anchor"]),
        "era": str(run["era"]),
        "window_iso": [TP.iso(int(run["window"][0])),
                       TP.iso(int(run["window"][1]))],
        "n_campaigns": len(tr),
        "n_assets_with_campaigns": len(per),
        "per_asset_n_campaigns": dict(sorted(per.items())),
        "gross_r_sum": _num(sum(float(t.gross_r) for t in tr
                                if t.gross_r is not None)) if tr else None,
        "fee_r_sum": _num(sum(float(t.fee_r) for t in tr
                              if t.fee_r is not None)) if tr else None,
        "funding_r_sum": _num(sum(float(t.funding_r) for t in tr
                                  if t.funding_r is not None)) if tr else None,
        "net_r_sum": _num(sum(nets)) if nets else None,
        "net_r_median": _num(np.median(nets)) if nets else None,
        "toll_pct_of_1r_median": _num(np.median(tolls)) if tolls else None,
        "n_inactive_components": int(sum(int(t.n_inactive_components)
                                         for t in tr)),
        "refused": ref,
        "book_spec": {k: run["book"].spec.get(k) for k in
                      ("runner", "registration", "arm", "era",
                       "registration_sha256")},
        "scored_statistic": None,
        "scored_statistic_note": (
            "NOT COMPUTED HERE. The ruler, the LOAO line and the p against "
            "the FDR bar are tierc10_panel's (TP.score / TP.headline_n) and "
            "are applied to this Book by the registration's own scorer. This "
            "row carries the journal and its provenance."),
    }


# ── EVERY GRID WHOLE: the row's fields are DECLARED, and `brk_row` proves the
# ── dict it built carries exactly them — no silent extra, no silent drop.
ROW_FIELDS = (
    "form", "lane", "lens", "era", "era_note",
    "registration", "arm", "registration_sha256",
    "panel", "panel_name", "n_panel_assets",
    "anchor_scored", "anchor_tier_e",
    "tuned", "tuned_note", "flip_hold_pins",
    "toll", "toll_accounting",
    "scored_figures",
    "tier_e_other_anchor", "tier_e_other_anchor_note",
    "tier_e_panel17", "tier_e_panel17_note",
    "height_vs_toll", "height_vs_toll_asset", "height_vs_toll_interface",
    "as_of_last_closed_4h", "seed", "law4",
)


def brk_row(lane: str, scored: dict, tier_e: dict | None = None,
            panel_tier_e: dict | None = None,
            verdict_asset: str | None = None,
            hvt_path: Path | None = None,
            require_verdict: bool = True,
            hvt_verdict_path: Path | None = None,
            verdict_asset_why: str | None = None,
            allow_provisional: bool = False) -> dict:
    """ONE BRK FORM'S ROW — the scored anchor, the OTHER anchor as Tier-E, the
    lens, the era, the panel, the toll `stamp_toll` already stamped, and the
    slot for that lens's height-vs-toll verdict [contract line 112].

    `scored` and `tier_e` are `run_lane_s1` / `run_lane_i1` returns — the
    SAME runner, called twice with the two `anchor=` values.  `panel_tier_e`
    is the optional 17-asset print R8 orders beside the 5-asset row; it is a
    third run of the same runner on a PANEL17 arm, and is None (with a stated
    reason) when no such arm is filed.

    `require_verdict=False` builds the row with a `PendingVerdict` in the
    verdict slot instead of HALTing — the row can then be assembled and
    NAMED, but any read of the slot, `json.dumps` included, HALTs.

    WHICH CENSUS ROW THE VERDICT IS, IS DERIVED FROM THE BOOK — never
    defaulted [review round 2, finding 1].  `verdict_asset_of(spec['panel'])`
    decides it, `verdict_asset=` is an explicit override that must be
    explained when it disagrees, and the choice plus its provenance ride the
    row as `height_vs_toll_asset` and PRINT on it.

    HALTS IF: the lane is unknown; a run's lens/era/lane does not match the
    row's; `tier_e` is not the lane's declared OTHER anchor; a run carries no
    Book; the Book's panel has no census counterpart (or an unexplained
    override disagrees with it); `require_verdict` and [Q-R3] is not filed;
    or the derived census row is PROVISIONAL and `allow_provisional` is not
    set — a row under the census's own sample floor is never carried quietly.
    """
    if lane not in LANE_LENS:
        raise SystemExit(f"HALT: unknown BRK lane {lane!r}; "
                         f"{sorted(LANE_LENS)}.")
    lens = LANE_LENS[lane]
    if str(scored["anchor"]) != LANE_ANCHOR[lane]:
        raise SystemExit(
            f"HALT: {lane}'s SCORED anchor is {LANE_ANCHOR[lane]!r} "
            f"(LANE_ANCHOR); the run offered as scored carries "
            f"{scored['anchor']!r}. The scored arm and the Tier-E print are "
            f"not interchangeable.")
    if str(scored["era"]) != LANE_ERA[lane]:
        raise SystemExit(
            f"HALT: {lane} is declared on the {LANE_ERA[lane]!r} era "
            f"(LANE_ERA) and the scored run carries {scored['era']!r}. "
            f"{LANE_ERA_LAW}")
    fig = _figures(scored, "SCORED")
    other = None
    if tier_e is not None:
        if str(tier_e["anchor"]) != LANE_TIER_E_ANCHOR[lane]:
            raise SystemExit(
                f"HALT: {lane}'s Tier-E print is the OTHER anchor, "
                f"{LANE_TIER_E_ANCHOR[lane]!r} (LANE_TIER_E_ANCHOR); the run "
                f"offered as Tier-E carries {tier_e['anchor']!r}. The "
                f"contract's 'also prints the OTHER anchor' is not satisfied "
                f"by printing the same one twice.")
        other = _figures(tier_e, "TIER-E — UNSCORED, GATES NOTHING")
    panel17 = None
    if panel_tier_e is not None:
        a_ = list(scored["book"].spec.get("panel") or [])
        b_ = list(panel_tier_e["book"].spec.get("panel") or []) \
            if isinstance(panel_tier_e.get("book"), TP.Book) else []
        if set(a_) == set(b_):
            raise SystemExit(
                f"HALT: the Tier-E PANEL print [R8] is a SECOND VIEW — the "
                f"17-asset one beside the scored 5-asset book. The run "
                f"offered rides {TP.panel_name(b_)} ({len(b_)} assets), the "
                f"same panel as the scored arm ({TP.panel_name(a_)}); "
                f"printing the same panel twice satisfies nothing.")
        panel17 = _figures(panel_tier_e, "TIER-E — UNSCORED, GATES NOTHING")
    spec = scored["book"].spec
    # THE VERDICT SLOT'S ASSET IS DERIVED FROM THE BOOK, NEVER DEFAULTED
    # [review round 2, finding 1].  It used to read
    #     asset = str(verdict_asset) if verdict_asset else "POOLED:CLASSIC5"
    # with `verdict_asset` derived from nothing.
    va = verdict_asset_of(list(spec.get("panel") or []),
                          verdict_asset, verdict_asset_why)
    asset = va["asset"]
    if require_verdict:
        hv = height_vs_toll(lens, asset, path=hvt_path,
                            verdict_path=hvt_verdict_path,
                            allow_provisional=bool(allow_provisional))
    else:
        hv = PendingVerdict(lens, asset, HEIGHT_VS_TOLL_SCALE,
                            HEIGHT_VS_TOLL_ERA,
                            hvt_path or HEIGHT_VS_TOLL_PATH,
                            hvt_verdict_path or HEIGHT_VS_TOLL_VERDICT_PATH)
    row = {
        "form": FORM_OF[lane],
        "lane": lane,
        "lens": lens,
        "era": str(scored["era"]),
        "era_note": TP.era_note(str(scored["era"])),
        "registration": spec.get("registration"),
        "arm": spec.get("arm"),
        "registration_sha256": spec.get("registration_sha256"),
        "panel": list(spec.get("panel") or []),
        "panel_name": TP.panel_name(spec.get("panel") or []),
        "n_panel_assets": len(spec.get("panel") or []),
        "anchor_scored": LANE_ANCHOR[lane],
        "anchor_tier_e": LANE_TIER_E_ANCHOR[lane],
        "tuned": dict(scored.get("tuned") or {}) or None,
        "tuned_note": (None if scored.get("tuned") else
                       "the memory-line anchor has no tuned pins: its margin "
                       "and hold are the FROZEN range pins (FLIP_HOLD)"),
        "flip_hold_pins": {"margin_atr": FLIP_HOLD_MARGIN,
                           "hold_bars": FLIP_HOLD_BARS,
                           "ttl_bars": MEM_TTL_BARS},
        "toll": (dict(scored["toll"]) if scored.get("toll") else
                 {"stamped": False,
                  "why": ("this runner stamps no toll; 'NET OF MEASURED 5m "
                          "TOLL' is P-BRK-S1's contract clause and "
                          "stamp_toll is called only there")}),
        "toll_accounting": TOLL_ACCOUNTING,
        "scored_figures": fig,
        "tier_e_other_anchor": other,
        "tier_e_other_anchor_note": (
            None if other is not None else
            "ABSENT — the contract's line 112 requires the OTHER anchor as a "
            "Tier-E print beside this row; assemble it by calling the SAME "
            "runner with anchor=" + repr(LANE_TIER_E_ANCHOR[lane])),
        "tier_e_panel17": panel17,
        "tier_e_panel17_note": (
            None if panel17 is not None else
            "ABSENT — operator R8 (2026-09-22) orders the 17-asset view "
            "printed as Tier-E beside each BRK row; it is a third run of the "
            "same runner on a PANEL17 arm, and no such arm is filed."),
        "height_vs_toll": hv,
        "height_vs_toll_asset": va,
        "height_vs_toll_interface": height_vs_toll_spec(),
        "as_of_last_closed_4h": as_of_of_record(),
        "seed": SEED,
        "law4": ("this row's Book carries a filed registration or it does not "
                 "exist; no BRK registration is filed today"),
    }
    if tuple(row) != ROW_FIELDS:
        raise SystemExit(
            f"HALT: the assembled row's fields are {tuple(row)}, not the "
            f"DECLARED {ROW_FIELDS}. Extra "
            f"{sorted(set(row) - set(ROW_FIELDS))}, missing "
            f"{sorted(set(ROW_FIELDS) - set(row))}. A row whose shape drifts "
            f"from its declaration is a row a reader cannot trust a column of.")
    return row


def brk_rows(runs: dict, hvt_path: Path | None = None,
             require_verdict: bool = True,
             hvt_verdict_path: Path | None = None) -> list:
    """ONE ROW PER BRK FORM, in lane order.

    `runs` = {lane: {"scored": run, "tier_e": run | None,
                     "panel_tier_e": run | None, "verdict_asset": str | None,
                     "verdict_asset_why": str | None,
                     "allow_provisional": bool}}.
    `verdict_asset` is an OVERRIDE, not a default: with it absent the census
    row is DERIVED from the Book's panel [review round 2, finding 1].
    EVERY GRID WHOLE: every lane present is emitted, in `LANE_ORDER`, and a
    lane `runs` does not carry is NAMED as absent rather than dropped.
    """
    unknown = sorted(set(runs) - set(LANE_ORDER))
    if unknown:
        raise SystemExit(f"HALT: brk_rows was handed lane(s) {unknown}; the "
                         f"BRK forms are {list(LANE_ORDER)}.")
    out = []
    for lane in LANE_ORDER:
        if lane not in runs:
            continue
        r = runs[lane]
        out.append(brk_row(lane, r["scored"], r.get("tier_e"),
                           r.get("panel_tier_e"), r.get("verdict_asset"),
                           hvt_path=hvt_path,
                           require_verdict=require_verdict,
                           hvt_verdict_path=hvt_verdict_path,
                           verdict_asset_why=r.get("verdict_asset_why"),
                           allow_provisional=bool(
                               r.get("allow_provisional", False))))
    return out


def row_schema() -> dict:
    """THE ROW'S SHAPE, printable with NO book in hand — which is the only
    state this estate is in today.  It is what `main()` prints in place of
    rows, so the absence of a BRK table is a described absence and not a
    silence."""
    return {
        "contract": ("RESUME 2026-09-22 line 112: 'Each BRK form also prints "
                     "the OTHER anchor (EMA band <-> memory-line) as Tier-E, "
                     "and carries its lens's height-vs-toll verdict ON ITS "
                     "ROW.'  Operator R8: 'The 17-asset view prints as "
                     "Tier-E beside each BRK row.'"),
        "one_row_per": "BRK form",
        "forms": {lane: {"form": FORM_OF[lane], "lens": LANE_LENS[lane],
                         "era": LANE_ERA[lane],
                         "anchor_scored": LANE_ANCHOR[lane],
                         "anchor_tier_e": LANE_TIER_E_ANCHOR[lane],
                         "toll_stamped": lane == LANE_S1}
                  for lane in LANE_ORDER},
        "fields": list(ROW_FIELDS),
        "assembled_by": "tierc10_brk.brk_rows(runs)",
        "needs": ("a TP.Book per anchor, i.e. a FILED registration — none "
                  "exists, so no row can be built on real bars today [LAW 4]"),
        "height_vs_toll": height_vs_toll_spec(),
        "computes_no_verdict": (
            "the height-vs-toll verdict is READ from [Q-R3]; the "
            "registration's own verdict is TP.score's and is not computed "
            "here"),
    }


def print_rows(rows: list, out=None) -> None:
    """THE PRINTER.  One block per form; the Tier-E print is LABELLED Tier-E
    on every line it appears on, and the verdict slot prints PENDING (naming
    the table it waits on) rather than a blank."""
    w = (out.write if out is not None else
         (lambda s: print(s, end="")))
    for r in rows:
        w(f"\n{'=' * 78}\n{r['form']} · {r['lane']} · lens {r['lens']} · era "
          f"{r['era']}\n{'=' * 78}\n")
        w(f"  registration {r['registration']!r} arm {r['arm']!r} "
          f"(sha {str(r['registration_sha256'])[:16]})\n")
        w(f"  panel {r['panel_name']} ({r['n_panel_assets']} assets): "
          f"{', '.join(r['panel'])}\n")
        f_ = r["scored_figures"]
        w(f"  SCORED anchor {r['anchor_scored']!r}: {f_['n_campaigns']} "
          f"campaigns on {f_['n_assets_with_campaigns']} assets, net_r sum "
          f"{f_['net_r_sum']}, median {f_['net_r_median']} "
          f"(verdict: {f_['scored_statistic_note']})\n")
        o = r["tier_e_other_anchor"]
        w(f"  TIER-E other anchor {r['anchor_tier_e']!r}: "
          + (f"{o['n_campaigns']} campaigns, net_r sum {o['net_r_sum']} "
             f"[{o['tier']}]\n" if o else
             f"{r['tier_e_other_anchor_note']}\n"))
        p17 = r["tier_e_panel17"]
        w(f"  TIER-E 17-asset view [R8]: "
          + (f"{p17['n_campaigns']} campaigns on "
             f"{p17['n_assets_with_campaigns']} assets [{p17['tier']}]\n"
             if p17 else f"{r['tier_e_panel17_note']}\n"))
        t = r["toll"]
        w("  TOLL: " + (f"cls {t['cls']!r} lens {t['lens']!r}, per asset "
                        f"{t['per_asset']}, median "
                        f"{f_['toll_pct_of_1r_median']} % of 1R\n"
                        if t.get("cls") else f"{t['why']}\n"))
        w(f"        {TOLL_ACCOUNTING['status']}\n")
        va = r["height_vs_toll_asset"]
        w(f"  [Q-R3] CENSUS ROW READ: asset {va['asset']!r} — {va['source']}"
          f" ({va['derived_how']})"
          + (f"; OVERRIDE {va['override']!r} because {va['override_why']!r}"
             if va["override"] else "") + "\n")
        hv = r["height_vs_toll"]
        if isinstance(hv, PendingVerdict):
            w(f"  HEIGHT-vs-TOLL [Q-R3]: PENDING — no readable table at "
              f"{HEIGHT_VS_TOLL_PATH} / {HEIGHT_VS_TOLL_VERDICT_PATH}; owned "
              f"by {HEIGHT_VS_TOLL_OWNER}. Reading this slot HALTs.\n")
        else:
            w(f"  HEIGHT-vs-TOLL [Q-R3] for {hv['asset']!r}: verdict_pass "
              f"{hv['verdict_pass']} "
              f"— {hv['reason']!r} (height/toll ratio_median "
              f"{hv['ratio_median']}, height_atr_median "
              f"{hv['height_atr_median']}, toll_atr_median "
              f"{hv['toll_atr_median']}, n_ranges {hv['n_ranges']}) READ "
              f"from {hv['source']} + {hv['verdict_source']}, cross-checked "
              f"on {hv['cross_checked']}\n")
            if hv["provisional"]:
                w(f"  *** PROVISIONAL [Q-R3] ROW, TAKEN BY NAME: "
                  f"{hv['provisional_reason']} — n_ranges "
                  f"{hv['sample_floor']['n_ranges']} / floor "
                  f"{hv['sample_floor']['min_n_ranges_pinned']}, "
                  f"edge_n_ranges "
                  f"{hv['sample_floor']['edge_n_ranges']} / floor "
                  f"{hv['sample_floor']['edge_min_n_ranges_pinned']}. This "
                  f"verdict rests UNDER the census's own sample floor and "
                  f"gates nothing. ***\n")
        w(f"  as_of {r['as_of_last_closed_4h']} · seed {r['seed']}\n")


# ══════════════════════════════════════════════════════ 13 · THE MECHANICS CARD
def mechanics_card(disk: bool = True, out_root: Path | None = None) -> dict:
    """WHAT THIS MODULE PINS, as a deterministic record — no clocks, no bars,
    no result.  F-DET compares two runs of it byte for byte.

    TWO BLOCKS, AND THE LINE BETWEEN THEM IS THE POINT.  `pins` is a pure
    function of THIS SOURCE, of the estate objects it binds, and of ONE
    write-once pin off disk — Stage D's AS_OF_PIN.json, read through
    `as_of_of_record()`: same bytes on any disk, in any order, whatever else
    has or has not been filed.  The as-of is in `pins` and not in
    `environment` deliberately — a pin that happens to live in a file is
    still a pin, and `out_root` (which re-points the OUTPUT-directory reads)
    does not and must not redirect it.
    `environment` is a READING OF THE DISK AT THE INSTANT OF THE RUN — has the
    census filed its tuning results yet, does Stage D's fee schedule agree
    with the fee object — and is therefore deterministic only across an
    instant, not across disks.  They sat in one block until review observed
    that F-DET (two runs, one instant, one disk) structurally cannot tell the
    two apart, and that a twin card written before a later edit had already
    diverged from the card of record because of it.  `mechanics_card(disk=
    False)` is the half the stronger claim can be made about, `out_root`
    re-points ONLY the disk reads, and F-DET now makes both claims.
    """
    root = Path(out_root) if out_root is not None else TP.OUT
    env = None
    if disk:
        sched = root / "data" / "fee_schedule.json"
        schedule_agrees = None
        if sched.exists():
            rows = json.loads(sched.read_text())["assets"]
            sides = sorted({float(a["taker_bps_side_used"]) for a in rows})
            schedule_agrees = bool(len(sides) == 1
                                   and abs(sides[0] - FEE_BPS_SIDE) < 1e-12)
        env = {
            "read_at": str(root),
            "note": ("READ FROM THE DISK AT THE INSTANT OF THE RUN — a "
                     "reading, not a pin; `pins` above is the part that is "
                     "the same bytes on every disk"),
            "fee_matches_stage_d_schedule": schedule_agrees,
            "tuning_result_present": {
                k: (root / v.relative_to(TP.OUT)).exists()
                for k, v in sorted(TUNING_RESULT_FOR.items())},
            "height_vs_toll_filed": (
                root / HEIGHT_VS_TOLL_PATH.relative_to(TP.OUT)).exists(),
            "height_vs_toll_verdict_filed": (
                root / HEIGHT_VS_TOLL_VERDICT_PATH.relative_to(TP.OUT)
            ).exists(),
        }
    return {
        "module": "scripts/tierc10_brk.py",
        "lanes": {LANE_S1: {"lens": LANE_LENS[LANE_S1],
                            "anchor_scored": LANE_ANCHOR[LANE_S1],
                            "anchor_tier_e": LANE_TIER_E_ANCHOR[LANE_S1],
                            "era": LANE_ERA[LANE_S1],
                            "era_note": TP.era_note(LANE_ERA[LANE_S1]),
                            "permission": "4h tide aligned, engine.htf visibility",
                            "panel_declared": PANEL_DECLARED,
                            "panel_served": PANEL_SERVED_LAW},
                  LANE_I1: {"lens": LANE_LENS[LANE_I1],
                            "anchor_scored": LANE_ANCHOR[LANE_I1],
                            "anchor_tier_e": LANE_TIER_E_ANCHOR[LANE_I1],
                            "era": LANE_ERA[LANE_I1],
                            "era_note": TP.era_note(LANE_ERA[LANE_I1]),
                            "permission": ("weekly 12/25 posture on the last "
                                           "CLOSED Monday-week AND daily "
                                           "DIRECTION from the R4 lifecycle"),
                            "panel_declared": PANEL_DECLARED,
                            "panel_served": PANEL_SERVED_LAW}},
        "pins": {
            # THE AS-OF WARRANTY, ON THE CARD OF RECORD (review, 2026-09-22,
            # blocking finding 1).  This card was filed with NO as-of stamp
            # at any depth while the report attested it carried one, so the
            # stage's pinned statement of mechanics was true of no stated
            # instant and could be re-read after the corridor moved and
            # silently believed.  It belongs in `pins` and NOT in
            # `environment`: the as-of is a WRITE-ONCE PIN read through
            # as_of_of_record() from Stage D's AS_OF_PIN.json, not a reading
            # of this stage's output directory — which is exactly why
            # `out_root` does not redirect it and why F-DET's empty-root leg
            # still sees this value.
            "as_of_last_closed_4h": as_of_of_record(),
            "as_of_source": "Stage D AS_OF_PIN.json (write-once)",
            "fee_bps_side": FEE_BPS_SIDE, "fee_object": "tierc7_rules.FEE_BPS_SIDE",
            "funding_ceiling_r": FUNDING_CEILING_R,
            "funding_law": ("interval sum: entry_ms < funding_hour_ms <= "
                            "exit_ms, priced at the close of the last lens bar "
                            "CLOSED at or before the stamp [B4]"),
            "rail_atr": MIN_STOP_ATR, "stop_buf_atr": STOP_BUF_ATR,
            "stop_geometry": "tierc5_rules.spring_stop on the retest extreme",
            "atr_len": ATR_LEN,
            "flip_hold_margin": FLIP_HOLD_MARGIN,
            "flip_hold_bars": FLIP_HOLD_BARS,
            "mem_ttl_bars": MEM_TTL_BARS,
            "frozen_scale": FROZEN_SCALE,
            "ribbon": [RIBBON_FAST, RIBBON_SLOW], "lifecycle_k": LIFECYCLE_K,
            "r1_bands": list(R1_BANDS),
            "r1_bands_census_spelling": {b: census_band(b) for b in R1_BANDS},
            "era_cut_iso": ERA_CUT_ISO, "era_cut_ms": ERA_CUT_MS,
            "era_object": "tierc10_panel.in_era / era_window / corridor_era",
            "era_instant_tested": ("entry bar OPEN (TP.in_era on entry_ms); "
                                   "R1 states the era in CLOSE time, so a "
                                   "straddling bar is refused, never admitted "
                                   "[B6]"),
            "tuning_result_paths": {k: str(v) for k, v in
                                    sorted(TUNING_RESULT_FOR.items())},
            "tuned_lenses": list(TUNED_LENSES),
            "gate_helper": GATE_HELPER,
            "lane_era": dict(sorted(LANE_ERA.items())),
            "lane_era_enforced": "require_lane_era(lane, gate()) [B9]",
            "lane_era_law": LANE_ERA_LAW,
            "lane_era_reason": dict(sorted(LANE_ERA_REASON.items())),
            "row_schema": row_schema(),
            "toll_accounting": dict(sorted(TOLL_ACCOUNTING.items())),
            "toll_class_band": (TOLL_CLASS_PREFIX[ANCHOR_BAND]
                                + "<band, in the CENSUS's spelling>"),
            "toll_class_band_example": toll_class(ANCHOR_BAND, BAND_EXAMPLE),
            "toll_class_memory": TOLL_CLASS_PREFIX[ANCHOR_MEMORY],
            "components": list(COMPONENTS),
            "within_bar_order": "STOP -> BELL -> HARVEST -> TRAIL",
            "bell_order": ["window", "tide", "ribbon (tested LAST) [B2]"],
        },
        "seed": SEED, "seed_sensitivity": SEED_LINEAGE,
        "rulings": list(RULINGS), "leans": list(LEANS),
        "findings_not_fixed": list(FINDINGS),
        "law4": ("no registration for P-BRK-S1 or P-BRK-I1 exists; every "
                 "runner HALTs at its gate, which is its first statement"),
        "environment": env,
    }


# ══════════════════════════════════════════════════ 15 · THE BUILD MANIFEST
# LAW 1(b) WANTS AN ON-DISK RECORD PER STAGE, and `brk/` was one of only two
# stage directories without one (R0, 2026-09-22).  This is that record, in the
# shape `census/`, `panel/` and `stamps/` already use: stage, as-of, substrate,
# seed, code shas, the commission, and the content sha of EVERY artifact the
# directory holds.
MANIFEST_NAME = "build_manifest.json"
DECLARED_ARTIFACTS = ("BRK_MECHANICS.json", "FIXTURES_BRK.txt")
# THIS STAGE'S OWN CODE — the two files this track owns, and the only two
# whose sha this manifest may present as a REPRODUCIBLE pin.
CODE_FILES = ("scripts/tierc10_brk.py", "scripts/tierc10_brk_fixtures.py")
# EVERY OTHER MODULE THIS STAGE DEPENDS ON — read at the instant of the run
# and NOT a pin (review, 2026-09-22).  tierc10_census.py and tierc10_data.py
# are being edited by two live parallel tracks: the sha filed in the last
# round (census f52cc906 / data e6e82f93) had already moved twice within
# minutes, so a manifest that presents them beside its own code sha claims a
# byte-reproducibility it does not have.  Moved here WITH the disclaimer
# inline rather than dropped, because naming the dependency is the point.
SIBLING_CODE_FILES = ("scripts/tierc10_panel.py", "scripts/tierc10_census.py",
                      "scripts/tierc10_data.py")
SIBLING_CODE_NOTE = (
    "READ AT THE INSTANT OF THE RUN — a reading, not a pin, and the ONE "
    "part of this manifest that is not byte-reproducible. These modules "
    "belong to other tracks and are edited while this stage builds; two "
    "runs of tierc10_brk.main() minutes apart will differ here and nowhere "
    "else but the directory enumeration. `code_sha` above is this track's "
    "own two files and IS reproducible.")


def sha_of(path: Path) -> str | None:
    """A file's content sha256, or None when it is not there.  None is a
    STATEMENT (the artifact is absent) and never a blank."""
    p = Path(path)
    return (hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file()
            else None)


def _summary_line(p: Path) -> str | None:
    """The `FIXTURE SUMMARY n/n PASS {...}` line out of a filed transcript —
    LAW 1(b)'s evidence, quoted rather than retyped."""
    if not p.is_file():
        return None
    for ln in reversed(p.read_text(encoding="utf-8").splitlines()):
        if ln.startswith("FIXTURE SUMMARY"):
            return ln.strip()
    return None


def build_manifest(out: Path, card: dict | None = None) -> dict:
    """THIS STAGE'S RECORD.  Every float is already rounded upstream, every
    sha is read off the disk at the instant of the run, and the manifest never
    hashes ITSELF (a record that contains its own digest cannot be written).

    EVERY GRID WHOLE: `sha` is built by ENUMERATING the directory, so an
    artifact nobody declared still appears; `declared_artifacts` says which
    ones were expected and whether each is there.
    """
    out = Path(out)
    card = card if card is not None else mechanics_card(out_root=None)
    tuned = {}
    for lens_, path_ in sorted(TUNING_RESULT_FOR.items()):
        tuned[lens_] = ({k: v for k, v in sorted(tuned_pins(lens_).items())}
                        if path_.is_file() else None)
    files = sorted(q.name for q in out.iterdir()
                   if q.is_file() and q.name != MANIFEST_NAME) \
        if out.is_dir() else []
    fixtures_txt = out / "FIXTURES_BRK.txt"
    return {
        "stage": "TIER-C10 · BRK LANE MECHANICS — P-BRK-S1 / P-BRK-I1",
        "as_of_last_closed_4h": as_of_of_record(),
        "as_of_source": "Stage D AS_OF_PIN.json (write-once)",
        "substrate": substrate()["substrate"],
        "seed": SEED, "seed_sensitivity": SEED_LINEAGE,
        "lean_tag": LEAN_TAG,
        "tier": ("MECHANICS ONLY — no P-BRK number is computed, printed or "
                 "filed anywhere in this stage [LAW 4]"),
        "gates": ("NOTHING. Every runner's first statement is the panel gate "
                  "(TP.require_arm); no registration for P-BRK-S1 or "
                  "P-BRK-I1 is filed, so no runner can reach a bar."),
        "law4": card["law4"],
        "code_sha": {f: sha_of(ROOT / f) for f in CODE_FILES},
        "sibling_code_sha_read_at": {
            "note": SIBLING_CODE_NOTE,
            "read_at": str(ROOT),
            "sha": {f: sha_of(ROOT / f) for f in SIBLING_CODE_FILES},
        },
        "commission": {
            "forms": [FORM_OF[ln] for ln in LANE_ORDER],
            "lanes": {ln: {"form": FORM_OF[ln], "lens": LANE_LENS[ln],
                           "era": LANE_ERA[ln],
                           "era_enforced_against_filed_arm": True,
                           "anchor_scored": LANE_ANCHOR[ln],
                           "anchor_tier_e": LANE_TIER_E_ANCHOR[ln],
                           "toll_stamped": ln == LANE_S1}
                      for ln in LANE_ORDER},
            "panel_declared": PANEL_DECLARED,
            "panel_served": PANEL_SERVED_LAW,
            "r1_bands": list(R1_BANDS),
            "r1_bands_census_spelling": {b: census_band(b) for b in R1_BANDS},
            "tuned_pins_of_record": tuned,
            "era_cut_iso": ERA_CUT_ISO, "era_cut_ms": ERA_CUT_MS,
            "toll_accounting": dict(sorted(TOLL_ACCOUNTING.items())),
            "row": row_schema(),
            "height_vs_toll": height_vs_toll_spec(),
            "n_rows_filed": 0,
            "why_no_rows": ("a row is assembled from a TP.Book and a Book "
                            "needs a FILED registration; none exists, so "
                            "this stage files a ROW SCHEMA and no rows "
                            "[LAW 4 — text before result]"),
            "parquet_filed": 0,
            "parquet_note": ("this stage files NO parquet: everything it "
                             "holds is a pin, a schema or a transcript, and "
                             "the one table it would file (the BRK rows) "
                             "cannot exist until a registration does"),
        },
        "input_sha": {
            str(v.relative_to(ROOT)): sha_of(v)
            for v in list(TUNING_RESULT_FOR.values())
            + [TP.OUT / "census" / "outcome_grid.parquet",
               HEIGHT_VS_TOLL_PATH, HEIGHT_VS_TOLL_VERDICT_PATH,
               TP.AS_OF_PIN]},
        "sha": {n: sha_of(out / n) for n in files},
        "declared_artifacts": {n: {"present": (out / n).is_file(),
                                   "sha": sha_of(out / n)}
                               for n in DECLARED_ARTIFACTS},
        "undeclared_artifacts_present": [n for n in files
                                         if n not in DECLARED_ARTIFACTS],
        "fixtures": {
            "module": "scripts/tierc10_brk_fixtures.py",
            "module_sha": sha_of(ROOT / "scripts" / "tierc10_brk_fixtures.py"),
            "transcript": "FIXTURES_BRK.txt",
            "transcript_sha": sha_of(fixtures_txt),
            "summary_line": _summary_line(fixtures_txt),
            "law": ("break legs FIRST and judged one at a time; a break leg "
                    "that comes back GREEN voids its fixture"),
        },
        "cross_track_dependencies": {
            "census [Q-R3] height-vs-toll": dict(
                height_vs_toll_spec(),
                request_to_census_track=(
                    "RETRACTED 2026-09-22. The last manifest asked the census "
                    "track to file a table it had ALREADY FILED ten minutes "
                    "after this manifest was written, under other names and "
                    "split in two. Nothing is asked of the census track: this "
                    "module was repointed at what is on disk."),
                read_today={
                    "figures": {"path": str(HEIGHT_VS_TOLL_PATH),
                                "present": HEIGHT_VS_TOLL_PATH.is_file()},
                    "verdict": {"path": str(HEIGHT_VS_TOLL_VERDICT_PATH),
                                "present":
                                    HEIGHT_VS_TOLL_VERDICT_PATH.is_file()}}),
            "census TUNING_RESULT": {lens_: str(v) for lens_, v
                                     in sorted(TUNING_RESULT_FOR.items())},
            "census outcome_grid (the toll)": str(
                TP.OUT / "census" / "outcome_grid.parquet"),
            "panel (gate, corridor, era, book)": "scripts/tierc10_panel.py",
        },
        "rulings": list(RULINGS),
        "leans": list(LEANS),
        "findings_not_fixed": list(FINDINGS),
        "skipped_empty": ["rows (no registration filed)",
                          "parquet (nothing to file)"],
        "warranty": ("every artifact in this directory is true AS OF "
                     "2026-09-21T16:00:00Z and of no other instant; no "
                     "feature reads a value stamped after its own bar"),
    }


def main(argv=None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    out = OUT
    if "--out" in argv:
        out = Path(argv[argv.index("--out") + 1])
    substrate()
    card = mechanics_card()
    out.mkdir(parents=True, exist_ok=True)
    (out / "BRK_MECHANICS.json").write_text(
        json.dumps(card, indent=1, sort_keys=True, default=str) + "\n")
    print("=" * 78)
    print("TIER-C10 · BRK LANE MECHANICS — P-BRK-S1 / P-BRK-I1")
    print("=" * 78)
    print(f"substrate {substrate()['substrate']} · seed {SEED} "
          f"(sensitivity {SEED_LINEAGE})")
    print(f"gate helper: {GATE_HELPER} (the panel module's CURRENT external "
          f"door; the require_registered fallback is NOT used)")
    for lens_, p_ in sorted(TUNING_RESULT_FOR.items()):
        print(f"tuned pins, lens {lens_}: present={p_.exists()} ({p_})")
    print(f"band spelling: {BAND_EXAMPLE} (operator / this module) == "
          f"{census_band(BAND_EXAMPLE)} (census grid); toll class "
          f"{toll_class(ANCHOR_BAND, BAND_EXAMPLE)}")
    print("\nOPERATOR RULINGS IMPLEMENTED")
    for r in RULINGS:
        print("  · " + r)
    print("\nLEANS")
    for ln in LEANS:
        print("  " + ln)
    print("\nFINDINGS NOT FIXED")
    for f_ in FINDINGS:
        print("  · " + f_)
    print("\nTHE ERA PIN, ENFORCED [B9]")
    for ln_ in LANE_ORDER:
        print(f"  · {FORM_OF[ln_]} ({ln_}) is DECLARED on the "
              f"{LANE_ERA[ln_]!r} era; require_lane_era holds the FILED ARM "
              f"to it inside the runner, before one bar or one bar-stamp is "
              f"read. {LANE_ERA_REASON[ln_]}")
    print("\nTHE PANEL")
    print(f"  DECLARED: {PANEL_DECLARED}")
    print(f"  SERVED:   {PANEL_SERVED_LAW}")
    print("\nTHE ROW [contract line 112 · R8]")
    rs = row_schema()
    print(f"  {rs['contract']}")
    for ln_ in LANE_ORDER:
        f_ = rs["forms"][ln_]
        print(f"  · {f_['form']}: lens {f_['lens']}, era {f_['era']}, scored "
              f"anchor {f_['anchor_scored']!r}, TIER-E other anchor "
              f"{f_['anchor_tier_e']!r}, toll stamped {f_['toll_stamped']}")
    print(f"  fields ({len(ROW_FIELDS)}): {list(ROW_FIELDS)}")
    print(f"  rows filed: 0 — {rs['needs']}")
    print("\nTHE [Q-R3] INTERFACE — READ, NEVER COMPUTED HERE")
    hv = height_vs_toll_spec()
    print(f"  status  {hv['status']}")
    print(f"  figures {hv['path']}  (filed today: "
          f"{HEIGHT_VS_TOLL_PATH.is_file()})")
    print(f"          key {hv['key']}  fields {hv['required_fields']}")
    print(f"  verdict {hv['verdict_path']}  (filed today: "
          f"{HEIGHT_VS_TOLL_VERDICT_PATH.is_file()})")
    print(f"          key {hv['verdict_key']}  fields "
          f"{hv['required_verdict_fields']}")
    print(f"  cross-checked on {hv['cross_checked_fields']} + the law half "
          f"{hv['cross_checked_law_fields']}; an ABSENT shared column is a "
          f"HALT, and `cross_checked` on a row is what was actually "
          f"compared; as-of column "
          f"{hv['as_of_column_required']!r} must read "
          f"{hv['as_of_required_value']!r}")
    print(f"  scale {hv['scale_kind_read']!r} era {hv['era_read']!r}")
    print(f"  asset READ is DERIVED from the Book's panel, never defaulted: "
          f"{hv['asset_read']['panel_to_census_label']}, a one-asset panel "
          f"-> its own symbol, anything else HALTs "
          f"({hv['asset_read']['no_counterpart']})")
    print(f"  provisional: {hv['provisional_policy'][:120]}")
    print(f"  owner {hv['owner']}")
    print(f"  absent -> {hv['on_absence']}")
    print("\nTHE TOLL, SAID PLAINLY")
    print(f"  {TOLL_ACCOUNTING['status']}")
    print(f"  {TOLL_ACCOUNTING['net_r_formula']}")
    print(f"  {TOLL_ACCOUNTING['grid_toll']}")
    print(f"\nLAW 4: {card['law4']}.")
    man = build_manifest(out, card)
    (out / MANIFEST_NAME).write_text(
        json.dumps(man, indent=1, sort_keys=True, default=str) + "\n")
    print(f"filed: {out / 'BRK_MECHANICS.json'}")
    print(f"filed: {out / MANIFEST_NAME}  (LAW 1(b): "
          f"{len(man['sha'])} artifact sha(s), "
          f"{len(man['code_sha'])} code sha(s), as-of "
          f"{man['as_of_last_closed_4h']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
