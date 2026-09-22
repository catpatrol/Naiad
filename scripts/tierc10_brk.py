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
    'R2 (verbatim): "All 17" -> PANEL17 for both lanes; P-BRK-S1 is scored on '
    'the HOLDOUT era only; P-BRK-I1 rides the full corridor.',
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
    card = card or TP.CONTROL_CARD
    roles = roles or T9.V6_ROLES
    tuned = tuned or tuned_pins("5m")
    band = r1_band(tuned["band"])
    era = g["era"]
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
    card = card or TP.CONTROL_CARD
    roles = roles or T9.V6_ROLES
    era = g["era"]
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


# ══════════════════════════════════════════════════════ 13 · THE MECHANICS CARD
def mechanics_card(disk: bool = True, out_root: Path | None = None) -> dict:
    """WHAT THIS MODULE PINS, as a deterministic record — no clocks, no bars,
    no result.  F-DET compares two runs of it byte for byte.

    TWO BLOCKS, AND THE LINE BETWEEN THEM IS THE POINT.  `pins` is a pure
    function of THIS SOURCE and of the estate objects it binds: same bytes on
    any disk, in any order, whatever else has or has not been filed.
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
        }
    return {
        "module": "scripts/tierc10_brk.py",
        "lanes": {LANE_S1: {"lens": LANE_LENS[LANE_S1],
                            "anchor_scored": LANE_ANCHOR[LANE_S1],
                            "anchor_tier_e": LANE_TIER_E_ANCHOR[LANE_S1],
                            "era": LANE_ERA[LANE_S1],
                            "era_note": TP.era_note(LANE_ERA[LANE_S1]),
                            "permission": "4h tide aligned, engine.htf visibility"},
                  LANE_I1: {"lens": LANE_LENS[LANE_I1],
                            "anchor_scored": LANE_ANCHOR[LANE_I1],
                            "anchor_tier_e": LANE_TIER_E_ANCHOR[LANE_I1],
                            "era": LANE_ERA[LANE_I1],
                            "era_note": TP.era_note(LANE_ERA[LANE_I1]),
                            "permission": ("weekly 12/25 posture on the last "
                                           "CLOSED Monday-week AND daily "
                                           "DIRECTION from the R4 lifecycle")}},
        "pins": {
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
    print(f"\nLAW 4: {card['law4']}.")
    print(f"filed: {out / 'BRK_MECHANICS.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
