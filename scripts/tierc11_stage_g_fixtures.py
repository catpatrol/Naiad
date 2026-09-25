#!/usr/bin/env python
"""TIER-C11 · STAGE G — F-DEF · F-GATE · F-PRIORITY · F-DISC · F-EDGE · F-HARVEST-INSTANTS ·
F-GRID · F-KEY · F-DET.
The fixtures of scripts/tierc11_stage_g.py (the admission gates P-AGE-1 and
P-WIN-1, their regbooks, and the L-G.3 Tier-E structure) [LEANS L-G.1, L-G.2,
L-G.3, L-1.3, L-1.4, L-1.5, AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID [the prove() law of scripts/tierc10_rf_fixtures.py / tierc11_books_fixtures.py].
A break leg is a set of PLANTS judged one at a time; a plant counts as CAUGHT only
if a finding NAMES THE INTENDED DETECTOR (its expected substring).  A plant that
crashes is a FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a
frame, a list, a temp dir) or under a MUTATION of the module restored in
`finally`; no artifact of record moves.  The referees are TYPED HERE: the cuts
(q75 / 206 / 16 / 7..15 / 2.2), the trailing-pool law, the D gate 0.75, the rail
1.0 ATR, the era cut, the charter slippage tiers, the regbook schema and arm
table, every grid's declared cells, the collar.  THIS FILE READS THE SNAPSHOT
ITSELF (pandas on the 4h kline path strings, clipped at the pin) and derives with
its own loops: EMA 12/26/89/316, Wilder ATR14, the 12/89 and 12/26 crosses, the
two-state tide streak from bar 316, the three-state arm-bar age, the pooled
CLASSIC5 trailing quartiles (np.quantile over bars with open <= the entry bar,
>= 30 bars), the armings (tide at the arm bar, displacement >= 0.75 ATR), the
windows and triggers, and a whole replay of v6 and of the priority rule.  Only
v6's stop law (tierc7_rules.struct_stop_4h on the lineage's pivots) and v6's
ride (tierc9._ride_leg9 + tierc7._account_chain) are taken from the lineage —
never from tierc11_stage_g or tierc11_ride.

  F-DEF       FAILS IF, on any v6 campaign, the module's ENTRY-bar tide streak,
              left-censoring, trailing q25/q50/q75, band, OLD flag, >206 flag or
              ARM-bar three-state age differs from this file's derivation; or the
              gated set of P-AGE-1 (base keys minus scored keys in the WRITTEN
              regbook) is not exactly {streak >= own trailing q75}; or the shadow's
              is not {streak > 206}.  Both definitions are computed and printed.
              SABOTAGE (module mutations): the ABSOLUTE cut swapped in for the
              trailing one (DEF-SET); the ARM-bar tide_streak_age swapped in for
              the entry-bar streak (DEF-AGE); a ONE-BAR-AHEAD trailing pool
              (DEF-EDGE); whole-corridor edges (LR.cuts) (DEF-EDGE).
  F-GATE      FAILS IF, for any of the five gates (P-AGE-1, its >206 shadow,
              P-WIN-1, its 7..15 shadow, the r_over_atr > 2.2 admission), the
              written gated regbook is not the written base minus EXACTLY this
              file's typed refused set, row-identical on EVERY column; a refused
              cohort is not exactly the base rows of that set; an era slice is not
              exactly the scored rows of that era; the two base arms differ or are
              not the v6 book; the gate-row table's refused n / ΣR differ from this
              file's; or the rival count is not this file's own replay's
              position_open count whose blocker is refused; or a base arm differs
              from the LINEAGE v6 Trade objects on any required column (exit_close_ms
              = the exit bar's close, stop_px = the INITIAL stop, ...) or from
              books/v6_campaigns on the 13 SC-7 columns at 6 dp; or, with ONE planted
              position_open rejection fed to BOTH the module and this file's counter,
              the module's per-gate rival counts differ from this file's or miss it.
              SABOTAGE: an UN-GATED book (scored == base) (GATE-MISSED); a gate that
              also removes one unnamed campaign (GATE-UNNAMED); a kept row's net_r
              +1e-12 (GATE-ROW); a cohort missing one refused campaign (COHORT-SET);
              the module's apply_gate returning the base (the module must HALT); the
              module's refused set carrying one unnamed campaign (GATE-UNNAMED); the
              module's blocker_of naming a campaign the gate keeps (RIVAL-COUNT);
              (copy) a base arm's exit_close_ms at the exit bar's OPEN (BASE-COL);
              (copy) a base arm's stop_px = the final trailed stop (BASE-COL).
  F-PRIORITY  FAILS IF the module's priority replay without hooks is not v6 at
              0.000e+00 on the 12 CTRL_COLS; or this file's own replay of v6 is not
              the v6 book; or the priority book (in-process AND the written regbook)
              differs from this file's own replay of the rule on ANY entry: keys,
              the pass (first trigger r_over_atr > 2.2), the substitute (the FIRST
              later same-direction 12/26 cross inside the window with the asset flat
              and r_over_atr <= 2.2), the stop / R, the ride (exit bar, reason, net_r
              exact), overlap on one asset, or the substitution count; or the WRITTEN
              priority arm differs from this file's replay on any required column
              (entry_px, stop_px, r_dist, exit_close_ms, exit_reason, gross / fee /
              funding / net R, era).  3 substitutions are hand-walked and printed.
              SABOTAGE (module mutations): the substitute's 2.2 test ignored
              (PRIO-RATR); the scan run past the window's close (PRIO-WINDOW); the
              pass rule inverted (PRIO-PASS); (copy) one substitute moved inside its
              asset's previous campaign (PRIO-FLAT); (copy) one substitute's net_r
              +1e-9 (PRIO-RIDE); (copy) the written arm's exit_close_ms at the exit
              bar's open, and one stop_px bent (PRIO-WRITTEN).
  F-DISC      FAILS IF any Tier-E DISCLOSURE table differs from this file's own
              recomputation: g_gate_rows (n / ΣR / mean of base, gated and refused;
              the forfeit note's text and X = the refused ΣR; the rival counts; the
              re-ride book from this file's OWN re-ride with the gate's rule as a
              refusal hook: n / ΣR / mean / not-in-v6 / v6-not-taken; the >206
              caveat), g_tide_bands (every row, n_left_censored included; the >206
              caveat), g_collisions, g_collision_list_v6, g_arrivals, g_priority_windows
              (outcome, entry, r/ATR, every scan count, both net_r), g_rivals,
              g_priority_vs_v6 (6 dp).  SABOTAGE: the module's re-ride hook for P-WIN-1
              at lag - 1 (DISC-RERIDE); (copies) forfeit X from the gated sum
              (DISC-FORFEIT); refused mean = gated mean (DISC-GATEROW); collisions
              counted at >= 3 (DISC-COLLIDE); the arm-bar >206 rows read the entry-bar
              flag (DISC-TIDE); n_left_censored -1 (DISC-TIDE); scan counts doubled
              (DISC-WINDOWS); 199 campaigns marked continuation (DISC-ARRIVALS); a
              re-ride ΣR +1 (DISC-RERIDE); the placeholder flag dropped (DISC-RIVALS);
              the >206 caveat dropped from a tide row and from the gate row
              (DISC-LABEL); a collision row dropped (DISC-COLLIST); a priority_net_r
              moved (DISC-PVS).
  F-EDGE      FAILS IF a cut's comparator is not the typed one AT its boundary
              (OLD: run == q75 refused; >206: 206 kept, 207 refused; lag >= 16: 15
              kept, 16 refused; shadow 7..15: 6 / 16 kept, 7 / 15 refused; r/ATR >
              2.2: 2.2 kept; the priority pass and substitute tests at 2.2; flat iff
              the bar is AFTER the open campaign's exit bar); an entry bar straddling
              the era cut (open 2024-06-30T20:00Z, close 2024-07-01T00:00Z) is not
              'holdout' in the module's facts, regbook frame and era-slice rows (its
              predecessor 'tuning'); the one-position sentence claims 'never binds'
              under any non-zero count (5 typed variants) or drops it under all
              zeros; or, under a FORCED HOLD (every ride's exit bar + 90 bars, clipped
              at the corridor end), the module's v6 and priority replays differ from
              this file's replay under the same hold (entries, exits, window outcomes,
              scan counts) or overlap on one asset — the scenario must bind.
              SABOTAGE (module mutations): OLD strict '>' (EDGE-OLD); '>= 206'
              (EDGE-ABS); lag '> 16' (EDGE-WIN); shadow 7..16 (EDGE-LAG); r/ATR '>='
              (EDGE-RATR); era by the bar's OPEN (EDGE-ERA); the claim printed always
              (EDGE-CLAIM); the flat test removed (EDGE-HOLD).
  F-HARVEST-INSTANTS  FAILS IF, on ANY row of ANY of the 14 regbooks, the extra column
              harvest_close_ms [L-R.5, AM-6 — the lanes pass] is absent or not Int64, is
              set on a row that did not harvest or NA on one that did, or differs from
              THIS FILE'S hand harvest law on its own 4h read (the band edge max/min(own
              EMA89, EMA316); from the bar after the entry on a fresh state, armed once
              any close[j-1] sat outside the edge, touched on the whole bar j; the first
              such bar strictly before the exit bar, the exit bar itself only at
              corridor_end; the bar's CLOSE); or a v6 key's instant differs from
              books/v6_campaigns.parquet's harvest_close_ms; or the priority book's
              substitutes (no v6 key: the rows the pairing-key join could not stamp)
              are not all covered.  SABOTAGE: (copies) one harvest one 4h bar late; one
              substitute's harvest dropped (nulled); [mutant] the writer's
              harvest_close_of stamping the harvest bar's OPEN (rebuilt priority arm).
  F-GRID      FAILS IF any stage table is not WHOLE against its typed declared
              cells (TP.grid_whole: missing / undeclared / duplicated), a non-
              registered table lacks the collar or carries a verdict column or a
              verdict word, an n = 0 cell carries a number or no nan_reason, or a
              grid cell's n / ΣR / mean differs from this file's recomputation (at
              the written 6 dp).  SABOTAGE (copies): a cell dropped; an undeclared
              cell; a duplicated cell; the collar removed; a verdict column; a
              verdict word; a NaN mean under n > 0; one cell's n + 1.
  F-KEY       FAILS IF a regbook parquet lacks a required column (or, for a Tier-E
              arm, the collar columns), has the wrong dtype, a null, a duplicated (symbol, entry_ms) or (symbol,
              entry_close_ms), an era not by the typed cut on entry_close_ms, a
              haircut not net_r - fee_r x slip / 5.0 (typed tiers), a net_r not
              gross - fee - funding, or entry_close_ms != entry_ms + 4h; a sidecar
              whose keys / kind / ruler / era_scope / panel / n / sum / book_sha256 /
              collar differ from the typed table and this file's canonical CSV; a
              STATUS.json whose arms are not the typed ones; the manifest's declared
              keys are not this file's TYPED keys, or TP.check_keys(stage_g) under
              the typed keys is RED; a manifest content sha not the table's; a
              manifest regbook file sha not the file's; the manifest or STAGE_G.md not
              printing the latest close at fetch time (AS_OF_PIN.json) beside the pin
              [L-0.1]; a table STAGE_G.md prints without the collar (bar the
              registered books) [L-1.4]; the one-position sentence not matching this
              file's own counts; or STAGE_G.md not printing both texts of record, the
              pre_seen and the selection_hazard verbatim.  SABOTAGE (copies): a
              duplicated row; a nulled net_r; direction as int64; sidecar n + 1; a
              bent book_sha256; STATUS missing an arm; a moved haircut; a flipped era;
              the collar dropped from a Tier-E parquet; TP.check_keys on a temp root
              holding a duplicated row; a declared key made a superset (KEY-DECLARED);
              a bent regbook file sha (KEY-FILESHA); the fetch-time line dropped
              (REPORT-ASOF); a printed table's collar renamed (REPORT-COLLAR); the
              claim under a non-zero own count (REPORT-CLAIM).
  F-DET       FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) differ
              from each other or from the canonical files in the typed file set,
              any byte, or any parquet content sha, or either exits nonzero.
              SABOTAGE: one byte bent in a copy; a parquet copy with one float
              moved; a hash-order-dependent line under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_g.py          # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_g_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the F-DET twins (DIR/_det_stage_g/);
      the canonical files compared against are always the record.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import dataclasses
import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_g as G                                          # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E = G.E
TP, T9, T7, TB, LR = E.TP, E.T9, E.T7, E.TB, E.LAB
RC = T9.RC
iso = TB.iso

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never G's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN = 1790006400000                 # 2026-09-21T16:00:00Z
LO_TYPED = 1567958400000                 # the TC11 corridor start (2019-09-08T16:00Z)
MS4H = 14_400_000
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
CLASSIC5_TYPED = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
V6_N_TYPED = 200
FLOOR_TYPED = 316                        # the warm floor (tide 89/316)
TIDE_F, TIDE_S = 89, 316
WIN_F, WIN_S = 12, 89                    # the window: EMA12 x EMA89 of 4h close
TRG_F, TRG_S = 12, 26                    # the trigger: EMA12 x EMA26
ATR_LEN = 14
D_DISP_TYPED = 0.75                      # displacement at the arm bar, ATR units
RAIL_TYPED = 1.0                         # "railed 1.0 ATR"
STREAK_Q = (0.25, 0.50, 0.75)
POOL_MIN = 30                            # L-G.1 "(tierc9._trailing_edges, >= 30 bars)"
ABS_CUT_TYPED = 206                      # L-G.1 "refuse streak > 206"
LAG_CUT_TYPED = 16                       # L-G.2 "refuse lag >= 16"
SHADOW_LAG_TYPED = (7, 15)               # L-G.2 "the shadow cut refuses 7-15"
RATR_CUT_TYPED = 2.2                     # L-G.3 "refuse > 2.2"
ERA_CUT_TYPED = 1_719_791_999_000        # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
TAKER_TYPED = 5.0
SLIP_TYPED = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0,
              "ZECUSDT": 5.0}            # charter tiers A/A/B/B/B (fee_schedule.json)
BANDS_TYPED = ("B1", "B2", "B3", "B4", "unbanded")
REQUIRED_TYPED = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px",
                  "stop_px", "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r",
                  "fee_r", "funding_r", "haircut_net_r", "era", "lane")
DTYPES_TYPED = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
                "direction": "int8", "entry_px": "float64", "stop_px": "float64",
                "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
                "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
                "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
                "lane": "object"}
FLOAT_REQ = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
             "haircut_net_r")
# (registration, arm) -> (kind, ruler, era_scope)
ARMS_TYPED = {
    ("P-AGE-1", "scored"): ("scored", "two_sample", "full"),
    ("P-AGE-1", "base"): ("base", "two_sample", "full"),
    ("P-AGE-1", "tierE__shadow_abs206"): ("tierE", "two_sample", "full"),
    ("P-AGE-1", "tierE__tuning"): ("tierE", "two_sample", "tuning"),
    ("P-AGE-1", "tierE__holdout"): ("tierE", "two_sample", "holdout"),
    ("P-AGE-1", "tierE__refused_cohort"): ("tierE", "vs_zero", "full"),
    ("P-WIN-1", "scored"): ("scored", "two_sample", "full"),
    ("P-WIN-1", "base"): ("base", "two_sample", "full"),
    ("P-WIN-1", "tierE__shadow_lag7_15"): ("tierE", "two_sample", "full"),
    ("P-WIN-1", "tierE__tuning"): ("tierE", "two_sample", "tuning"),
    ("P-WIN-1", "tierE__holdout"): ("tierE", "two_sample", "holdout"),
    ("P-WIN-1", "tierE__refused_cohort"): ("tierE", "vs_zero", "full"),
    ("P-WIN-1", "tierE__ratr_admission"): ("tierE", "two_sample", "full"),
    ("P-WIN-1", "tierE__ratr_priority"): ("tierE", "two_sample", "full"),
}
SIDECAR_KEYS_TYPED = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                      "sum_net_r", "book_sha256", "description", "source_script",
                      "book_sha256_law", "haircut_law", "as_of", "seed")
COLLAR_TYPED = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                "gates": "nothing"}
SOURCE_TYPED = "scripts/tierc11_stage_g.py"
# (registration, gated arm, typed refused set, cohort arm or None)
GATES_TYPED = (("P-AGE-1", "scored", "AGE", "tierE__refused_cohort"),
               ("P-AGE-1", "tierE__shadow_abs206", "ABS", None),
               ("P-WIN-1", "scored", "WIN", "tierE__refused_cohort"),
               ("P-WIN-1", "tierE__shadow_lag7_15", "LAG7_15", None),
               ("P-WIN-1", "tierE__ratr_admission", "RATR", None))
GATE_ROW_OF = {"AGE": "P-AGE-1", "ABS": "P-AGE-1/shadow_abs206", "WIN": "P-WIN-1",
               "LAG7_15": "P-WIN-1/shadow_lag7_15", "RATR": "L-G.3/ratr_admission"}
STAGE_TABLES_TYPED = ("g_age_crosstab", "g_arrivals", "g_campaign_gates",
                      "g_collision_list_v6", "g_collisions", "g_era_slices", "g_gate_rows",
                      "g_grid_books", "g_grid_partition", "g_lag_bands", "g_priority_vs_v6",
                      "g_priority_windows", "g_registered_books", "g_rivals", "g_tide_bands",
                      "g_tiere_books")
UNCOLLARED_TYPED = ("g_registered_books",)       # registered-book arithmetic
TIDE_MEASURES_TYPED = (
    "entry_bar_streak (L-G.1 of record)",
    "arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges)",
    "entry_bar_streak > 206 (ABSOLUTE shadow)",
    "arm_bar_tide_streak_age > 206 (disclosure)")
COLLISION_BOOKS_TYPED = ("v6", "P-AGE-1 scored", "P-WIN-1 scored", "ratr admission",
                         "ratr priority")
# the declared key of every stage table (F-KEY holds the manifest to THESE, not its own)
KEYS_TYPED = {
    "g_age_crosstab": ["cell"], "g_arrivals": ["kind", "symbol", "entry_ms"],
    "g_campaign_gates": ["symbol", "entry_ms"], "g_collision_list_v6": ["entry_close_ms", "symbol"],
    "g_collisions": ["book"], "g_era_slices": ["registration", "book", "era"],
    "g_gate_rows": ["gate"], "g_grid_books": ["cell"], "g_grid_partition": ["cell"],
    "g_lag_bands": ["lag_band"], "g_priority_vs_v6": ["symbol", "entry_ms"],
    "g_priority_windows": ["symbol", "arm_ms", "direction"],
    "g_registered_books": ["registration", "arm"], "g_rivals": ["symbol", "trigger_ms", "direction"],
    "g_tide_bands": ["measure", "band"], "g_tiere_books": ["registration", "arm"]}
# L-G.1: "The shadow row prints that 206 is the whole-corridor median edge, not the OLD
# edge, and that it reads the corridor ahead" — the words looked for (case-free)
ABS_PHRASES_TYPED = ("whole-corridor median edge", "not the old edge", "reads the corridor ahead")
ABS_GATE_TYPED = "P-AGE-1/shadow_abs206"
# L-1.5: "on per-campaign expectancy only; the gate forfeits +X R total" (X at 4 dp)
FORFEIT_TYPED = "on per-campaign expectancy only; the gate forfeits {x:+.4f} R total"
# the module's per-gate rival columns (g_rivals / rival_rows)
RIVAL_COL_TYPED = {"AGE": "rival__P_AGE_1", "ABS": "rival__P_AGE_1__shadow_abs206",
                   "WIN": "rival__P_WIN_1", "LAG7_15": "rival__P_WIN_1__shadow_lag7_15",
                   "RATR": "rival__L_G_3__ratr_admission"}
SELF_COL_TYPED = {k: v.replace("rival__", "rival_self_refused__") for k, v in RIVAL_COL_TYPED.items()}
OUTCOME_NAME_TYPED = {"entered": "entered", "position_open": "position_open",
                      "no_stop": "no_stop_or_atr", "passed_substituted": "passed_substituted",
                      "passed_no_substitute": "passed_no_substitute"}
AS_OF_PIN_JSON = ROOT / "research_outputs" / "tierc11" / "data" / "AS_OF_PIN.json"
V6_CAMPAIGNS = ROOT / "research_outputs" / "tierc11" / "books" / "v6_campaigns.parquet"
# SC-7: the 13 regbook columns books/v6_campaigns carries (regbook col, v6_campaigns col)
SC7_TYPED = (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
             ("entry_px", "entry_px"), ("stop_px", "stop_px"), ("r_dist", "r_dist"),
             ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
             ("net_r", "net_r"), ("gross_r", "gross_r"), ("fee_r", "fee_r"),
             ("funding_r", "funding_r"), ("era", "era_of_entry"), ("lane", "lane"))
REGISTERED_MD_HEADING = "## Registered books (book, not a verdict)"
MD_TABLES_TYPED = 17                     # the tables STAGE_G.md prints
# L-0.1 "the latest close at fetch time is printed beside it" (BOOKS.md's wording)
FETCH_PHRASE_TYPED = "latest closed 4h at fetch time (AS_OF_PIN.json latest_closed_4h_at_pin_run): "
CLAIM_PHRASE_TYPED = "never binds"
STRADDLE_OPEN_TYPED = 1_719_777_600_000  # 2024-06-30T20:00Z: open <= the era cut < close
STRADDLE_CLOSE_TYPED = 1_719_792_000_000  # 2024-07-01T00:00Z
HOLD_TYPED = 90                          # F-EDGE forced hold: exit bar + 90 4h bars (the
                                         # hold must bind on BOTH paths: +30 left the
                                         # priority scan's not-flat skip at 0)
VERDICT_COLUMNS = ("verdict", "verdict_of_record", "clears_bh_bar", "promotable",
                   "scored_in_family", "p_one_sided", "is_the_registered_cell")
VERDICT_RX = re.compile(r"\b(SUPPORTED|PASS|PASSES|FAIL|FAILS|MET)\b")

OUT = G.OUT_ROOT / G.STAGE_DIR                  # research_outputs/tierc11/stage_g
REGB = G.OUT_ROOT / G.REGBOOK_DIR               # research_outputs/tierc11/regbooks
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_G.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_why = break_leg()
    except BaseException as e:              # a break leg that errors proved nothing
        if isinstance(e, KeyboardInterrupt):
            raise
        b_ok, b_why = True, f"break leg RAISED {type(e).__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'GREEN (FIXTURE IS VOID)'}: {b_why}")
    try:
        r_ok, r_why = real_leg()
    except SystemExit as e:                 # a HALT in the real leg is a FAIL
        r_ok, r_why = False, f"HALT {e}"
    except Exception as e:                  # a real leg that errors is a FAIL
        r_ok, r_why = False, f"raised {type(e).__name__}: {e}"
    say(f"  [{'PASS' if r_ok else 'FAIL'}] {fid}: {r_why}")
    if b_ok:
        FAILED.append(f"{fid} (break leg did not go RED — fixture proves nothing)")
    elif not r_ok:
        FAILED.append(fid)
    else:
        PASSED.append(fid)


def plants(rows) -> tuple[bool, str]:
    """rows = (name, expected detector substring, thunk -> list of findings).
    Judged ONE AT A TIME.  CAUGHT only if a finding names the intended detector.
    No finding = the plant PASSED (VOID); a finding without the substring = the
    WRONG detector (VOID); a crash = a FIXTURE DEFECT (VOID).  A SystemExit (a
    module HALT) is a finding."""
    passed, wrong, caught, crashed = [], [], [], []
    for name, want, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:
            found = [f"HALT: {e}"]
        except Exception as e:
            crashed.append(f"{name} -> RAISED {type(e).__name__}: {e}")
            continue
        if not found:
            passed.append(name)
        elif not any(want in str(f) for f in found):
            wrong.append(f"{name} -> {str(found[0])[:160]} (wanted {want!r})")
        else:
            hit = next(str(f) for f in found if want in str(f))
            i = hit.index(want)
            shown = hit[:190] if i + len(want) <= 190 else (hit[:60] + " … " + hit[i:i + 160])
            caught.append(f"{name} -> {shown}")
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED — a FIXTURE DEFECT, not a "
                      f"finding: " + " · ".join(crashed))
    if passed or wrong:
        return True, (f"{len(passed)} plant(s) PASSED {passed}; {len(wrong)} caught by the "
                      f"WRONG detector {wrong}")
    return False, (f"all {len(caught)} plants caught by their named detector, one at a "
                   f"time: " + " · ".join(caught))


@contextlib.contextmanager
def mutated(obj, name: str, value):
    """A MUTATION of the module under trial, restored in `finally`."""
    old = getattr(obj, name)
    setattr(obj, name, value)
    try:
        yield
    finally:
        setattr(obj, name, old)


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def _f6(x: float) -> float:
    """The writer's rounding (pandas .round(6) == numpy.around), reproduced exactly."""
    return float(np.round(np.float64(x), 6))


def _same(a, b) -> bool:
    """Exact equality, NaN == NaN, NA == NA (a nullable Int64 column's missing value —
    the lanes pass's harvest_close_ms; NA never equals a number)."""
    if a is pd.NA or b is pd.NA:
        return a is pd.NA and b is pd.NA
    if isinstance(a, float) or isinstance(b, float):
        try:
            fa, fb = float(a), float(b)
        except (TypeError, ValueError):
            return False
        return (math.isnan(fa) and math.isnan(fb)) or fa == fb
    return a == b


# ═══════════════════════════════════ THIS FILE'S OWN READ + OWN DERIVATIONS
_C: dict = {}


def own_ema(x, n: int) -> np.ndarray:
    """A plain recursive EMA (alpha 2/(n+1), seeded at the first value)."""
    a = 2.0 / (n + 1.0)
    out = np.empty(len(x))
    prev = None
    for i, v in enumerate(x):
        v = float(v)
        prev = v if prev is None else prev + a * (v - prev)
        out[i] = prev
    return out


def own_atr(h, l, c, n: int) -> np.ndarray:
    """Wilder ATR: true range (bar 0 = high - low), RMA alpha 1/n seeded at bar 0."""
    out = np.empty(len(c))
    prev = None
    a = 1.0 / n
    for i in range(len(c)):
        hi_, lo_ = float(h[i]), float(l[i])
        tr = hi_ - lo_ if i == 0 else max(hi_ - lo_, abs(hi_ - float(c[i - 1])),
                                          abs(lo_ - float(c[i - 1])))
        prev = tr if prev is None else prev + a * (tr - prev)
        out[i] = prev
    return out


def own_cross(fast: np.ndarray, slow: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    up = np.zeros(len(fast), dtype=bool)
    dn = np.zeros(len(fast), dtype=bool)
    up[1:] = (fast[1:] > slow[1:]) & (fast[:-1] <= slow[:-1])
    dn[1:] = (fast[1:] < slow[1:]) & (fast[:-1] >= slow[:-1])
    return up, dn


def own4(sym: str) -> dict:
    k = ("own4", sym)
    if k not in _C:
        d = pd.read_parquet(str(TC11_SNAP / "klines" / f"{sym}_4h.parquet"))
        d = d.sort_values("open_time", kind="mergesort")
        d = d[d["open_time"].astype(np.int64) + MS4H <= PIN].reset_index(drop=True)
        o = d["open_time"].to_numpy(np.int64)
        h, l, c = (d[x].to_numpy(float) for x in ("high", "low", "close"))
        e12, e26, e89, e316 = (own_ema(c, p) for p in (WIN_F, TRG_S, WIN_S, TIDE_S))
        atr = own_atr(h, l, c, ATR_LEN)
        n = len(c)
        st2 = np.zeros(n, int)
        run = np.full(n, -1, int)
        cens = np.zeros(n, bool)
        cur = -1
        for j in range(FLOOR_TYPED, n):     # the two-state tide streak, a plain loop
            s_ = 1 if e89[j] > e316[j] else -1
            if j == FLOOR_TYPED or s_ != st2[j - 1]:
                cur = j
            st2[j], run[j] = s_, j - cur + 1
            cens[j] = cur == FLOOR_TYPED
        st3 = np.where((e89 > e316) & (c > e316), 1, np.where((e89 < e316) & (c < e316), -1, 0))
        w_up, w_dn = own_cross(e12, e89)
        t_up, t_dn = own_cross(e12, e26)
        _C[k] = {"o": o, "h": h, "l": l, "c": c, "e89": e89, "e316": e316, "atr": atr,
                 "run": run, "cens": cens, "st3": st3, "w_up": w_up, "w_dn": w_dn,
                 "t_up": t_up, "t_dn": t_dn, "n": n,
                 "lo_i": max(int(np.searchsorted(o, LO_TYPED, "left")), FLOOR_TYPED),
                 "hi_i": int(np.searchsorted(o, PIN - 1, "right")) - 1}
    return _C[k]


def idx(sym: str, ms: int) -> int:
    o = own4(sym)["o"]
    i = int(np.searchsorted(o, int(ms)))
    if i >= len(o) or int(o[i]) != int(ms):
        raise RuntimeError(f"{sym} {iso(int(ms))} is no 4h bar open in the own read")
    return i


def own_pool() -> tuple[np.ndarray, np.ndarray]:
    if "pool" not in _C:
        vs, ts = [], []
        for s in CLASSIC5_TYPED:
            X = own4(s)
            m = (X["o"] >= LO_TYPED) & (X["o"] <= PIN - 1) & (X["run"] > 0)
            vs.append(X["run"][m])
            ts.append(X["o"][m])
        v, tm = np.concatenate(vs), np.concatenate(ts)
        o = np.argsort(tm, kind="stable")
        _C["pool"] = (v[o], tm[o])
    return _C["pool"]


def own_edges(at_ms: int) -> list | None:
    v, tm = own_pool()
    m = tm <= int(at_ms)
    if int(m.sum()) < POOL_MIN:
        return None
    return [float(x) for x in np.quantile(v[m], STREAK_Q)]


def typed_band(run: int, ed) -> str:
    if ed is None or run <= 0:
        return "unbanded"
    return f"B{1 + sum(1 for e in ed if run >= e)}"


def own_arm_age(sym: str, arm_i: int) -> tuple[int, bool]:
    st3 = own4(sym)["st3"]
    s0 = int(st3[arm_i])
    age, j = 1, arm_i - 1
    while j >= FLOOR_TYPED and int(st3[j]) == s0:
        age += 1
        j -= 1
    return age, bool(j < FLOOR_TYPED)


def own_facts_row(sym: str, entry_ms: int, arm_ms: int, r_dist: float) -> dict:
    X = own4(sym)
    i, a = idx(sym, entry_ms), idx(sym, arm_ms)
    run = int(X["run"][i])
    ed = own_edges(int(X["o"][i]))
    arm_age, arm_cens = own_arm_age(sym, a)
    lag = i - a
    r = float(r_dist) / float(X["atr"][i])
    return {"symbol": sym, "entry_ms": int(entry_ms), "run": run, "cens": bool(X["cens"][i]),
            "edges": ed, "band": typed_band(run, ed),
            "AGE": ed is not None and run >= ed[2], "ABS": run > ABS_CUT_TYPED,
            "arm_age": arm_age, "arm_cens": arm_cens, "arm_band": typed_band(arm_age, ed),
            "lag": lag, "WIN": lag >= LAG_CUT_TYPED,
            "LAG7_15": SHADOW_LAG_TYPED[0] <= lag <= SHADOW_LAG_TYPED[1],
            "r_over_atr": r, "RATR": r > RATR_CUT_TYPED,
            "era": "tuning" if int(entry_ms) + MS4H <= ERA_CUT_TYPED else "holdout"}


def v6_book() -> list:
    """The v6 book from the lineage (the base every gate filters) — the module's
    regbook base is judged against it, never read from the module."""
    if "v6" not in _C:
        lo, hi = LO_TYPED, PIN - 1
        _C["v6"] = [t for s in CLASSIC5_TYPED
                    for t in T9.replay9(s, TP.CONTROL_CARD, T9.V6_ROLES, lo, hi)[1]]
    return _C["v6"]


def own_facts() -> dict:
    """{(symbol, entry_ms): own facts} for every v6 campaign."""
    if "facts" not in _C:
        _C["facts"] = {(t.symbol, int(t.entry_ms)): own_facts_row(t.symbol, int(t.entry_ms),
                                                                   int(t.arm_ms), float(t.r_dist))
                       for t in v6_book()}
    return _C["facts"]


def typed_set(name: str) -> set:
    return {k for k, f in own_facts().items() if f[name]}


def module_R() -> dict:
    if "R" not in _C:
        _C["R"] = G.compute()
    return _C["R"]


def reg_df(reg: str, arm: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet(str((root or REGB) / reg / f"{arm}.parquet"))


def reg_side(reg: str, arm: str, root: Path | None = None) -> dict:
    return json.loads(((root or REGB) / reg / f"{arm}.json").read_text(encoding="utf-8"))


def stage_df(name: str, root: Path | None = None) -> pd.DataFrame:
    return pd.read_parquet(str((root or OUT) / f"{name}.parquet"))


def keys_of(df: pd.DataFrame) -> set:
    return set(zip(df["symbol"].astype(str), df["entry_ms"].astype(np.int64).tolist()))


# ═══════════════════════════════════════════════════════════════════ F-DEF
def def_findings(facts: pd.DataFrame, label: str, written: bool = False) -> list[str]:
    """The module's gate facts vs this file's derivation.  `written` = the table
    was rounded at 6 dp on write (the edges compared at 6 dp)."""
    own = own_facts()
    out = []
    if sorted(zip(facts["symbol"], facts["entry_ms"].astype(int))) != sorted(own):
        out.append(f"DEF-KEYS {label}: the facts' keys are not the v6 book's")
        return out
    q = (lambda x: _f6(x)) if written else (lambda x: float(x))
    for r in facts.itertuples(index=False):
        k = (r.symbol, int(r.entry_ms))
        f = own[k]
        tag = f"{r.symbol} {iso(k[1])}"
        if int(r.tide_streak_entry) != f["run"] or bool(r.tide_left_censored) != f["cens"]:
            out.append(f"DEF-AGE {label} {tag}: entry-bar streak {r.tide_streak_entry} "
                       f"(censored {r.tide_left_censored}) != own {f['run']} ({f['cens']})")
        ed = f["edges"]
        got = [r.tide_edge_q25, r.tide_edge_q50, r.tide_edge_q75]
        want = [float("nan")] * 3 if ed is None else [q(x) for x in ed]
        if not all(_same(float(g), w) for g, w in zip(got, want)):
            out.append(f"DEF-EDGE {label} {tag}: trailing edges {got} != own {want}")
        if str(r.tide_band) != f["band"]:
            out.append(f"DEF-BAND {label} {tag}: band {r.tide_band} != own {f['band']}")
        if bool(r.age_abs206_refused) != f["ABS"]:
            out.append(f"DEF-ABS {label} {tag}: >206 flag {r.age_abs206_refused} != own "
                       f"{f['ABS']} (streak {f['run']})")
        if int(r.tide_streak_age_arm) != f["arm_age"] or \
                bool(r.tide_streak_age_arm_censored) != f["arm_cens"]:
            out.append(f"DEF-ARM {label} {tag}: arm-bar age {r.tide_streak_age_arm} != own "
                       f"{f['arm_age']}")
        if str(r.arm_band_on_entry_edges) != f["arm_band"]:
            out.append(f"DEF-ARM {label} {tag}: arm band {r.arm_band_on_entry_edges} != own "
                       f"{f['arm_band']}")
        if str(r.era) != f["era"]:
            out.append(f"DEF-ERA {label} {tag}: era {r.era} != own {f['era']} (entry close vs "
                       f"the typed cut)")
    got_set = set(zip(facts["symbol"][facts["age_old_refused"].astype(bool)],
                      facts["entry_ms"][facts["age_old_refused"].astype(bool)].astype(int)))
    want_set = typed_set("AGE")
    if got_set != want_set:
        out.append(f"DEF-SET {label}: the OLD (refused) set has {len(got_set)} campaigns, the "
                   f"typed trailing-q75 set {len(want_set)} ({len(got_set - want_set)} extra, "
                   f"{len(want_set - got_set)} missing)")
    return out


def _v6_pool():
    R = module_R()
    return R["v6"], R["pool"]


def def_break():
    v6, pool = _v6_pool()
    lo, hi = LO_TYPED, PIN - 1

    def under(name, fn):
        def thunk():
            with mutated(G, name, fn):
                return def_findings(G.facts_frame(v6, pool), f"[plant {name}]")
        return thunk

    om = {s: np.asarray(T9.frame(s)["f"].open_ms, np.int64) for s in CLASSIC5_TYPED}
    whole = [float(x) for x in LR.cuts(lo, hi)["streak_bar"]]
    return plants([
        ("the ABSOLUTE cut (streak > 206) swapped in for the trailing q75", "DEF-SET",
         under("old_refused", lambda run, edges: int(run) > ABS_CUT_TYPED)),
        ("the ARM-bar tierc9.tide_streak_age swapped in for the ENTRY-bar streak",
         "DEF-AGE", under("age_of", lambda t: T9.tide_streak_age(t, T9.V6_ROLES))),
        ("a ONE-BAR-AHEAD trailing pool (open <= entry bar + 4h)", "DEF-EDGE",
         under("edges_of", lambda t, p: T9._trailing_edges(
             p, int(om[t.symbol][int(t.entry_i)]) + MS4H)["streak_bar"])),
        ("whole-corridor edges (LR.cuts) for the trailing ones", "DEF-EDGE",
         under("edges_of", lambda t, p: list(whole))),
    ])


def def_real():
    R = module_R()
    bad = def_findings(R["facts"], "in-process")
    bad += def_findings(stage_df("g_campaign_gates"), "written g_campaign_gates", written=True)
    base, sc = reg_df("P-AGE-1", "base"), reg_df("P-AGE-1", "scored")
    sh = reg_df("P-AGE-1", "tierE__shadow_abs206")
    gated, shadow = keys_of(base) - keys_of(sc), keys_of(base) - keys_of(sh)
    if gated != typed_set("AGE"):
        bad.append(f"DEF-SET written P-AGE-1/scored: gated {len(gated)} != typed "
                   f"{len(typed_set('AGE'))}")
    if shadow != typed_set("ABS"):
        bad.append(f"DEF-SET written P-AGE-1/shadow_abs206: gated {len(shadow)} != typed "
                   f"{len(typed_set('ABS'))}")
    own = own_facts()
    runs = np.array([f["run"] for f in own.values()])
    arms = np.array([f["arm_age"] for f in own.values()])
    bands = {b: sum(1 for f in own.values() if f["band"] == b) for b in BANDS_TYPED}
    abands = {b: sum(1 for f in own.values() if f["arm_band"] == b) for b in BANDS_TYPED}
    both = len(typed_set("AGE") & {k for k, f in own.items() if f["arm_band"] == "B4"})
    say(f"  [DEF] (record) ENTRY-bar streak sign(e89-e316) from bar 316: median "
        f"{float(np.median(runs)):.1f}, min {int(runs.min())}, max {int(runs.max())}; > 206 on "
        f"{int((runs > 206).sum())}/{len(runs)}; trailing bands {bands}; left-censored "
        f"{sum(1 for f in own.values() if f['cens'])}")
    say(f"  [DEF] (disclosure) ARM-bar three-state age (tierc9.tide_streak_age): median "
        f"{float(np.median(arms)):.1f}, min {int(arms.min())}, max {int(arms.max())}; > 206 on "
        f"{int((arms > 206).sum())}/{len(arms)}; banded on the same trailing edges {abands}; "
        f"left-censored {sum(1 for f in own.values() if f['arm_cens'])}")
    say(f"  [DEF] gated (refused) sets: P-AGE-1 OLD {len(typed_set('AGE'))} -> scored n "
        f"{len(sc)}; ABSOLUTE shadow >206 {len(typed_set('ABS'))} -> n {len(sh)}; OLD on BOTH "
        f"definitions {both}; pre_seen (TC10): gated n 141 = 200 - 59 B4")
    return (not bad), (f"{len(own)} v6 campaigns: both tide-age definitions re-derived by this "
                       f"file (entry-bar streak, trailing q25/q50/q75 over the pooled CLASSIC5 "
                       f"prefix open <= entry, band, >206, arm-bar three-state age) == the "
                       f"module in-process and the written g_campaign_gates (6 dp) on every "
                       f"campaign; the written P-AGE-1 scored refuses exactly the typed "
                       f"{len(typed_set('AGE'))} (streak >= own q75), the shadow exactly the "
                       f"typed {len(typed_set('ABS'))} (streak > 206)"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-GATE
def _row_diff(a: pd.DataFrame, b: pd.DataFrame, label: str, det: str) -> list[str]:
    """Row-identity on EVERY column of the reference `b`, keyed (symbol, entry_ms);
    `a` may carry the collar columns and nothing else beside them [L-1.4]."""
    out = []
    cols = list(b.columns)
    miss = [c for c in cols if c not in a.columns]
    extra = [c for c in a.columns if c not in cols and c not in COLLAR_TYPED]
    if miss or extra:
        return [f"{det} {label}: columns missing {miss} / extra {extra}"]
    a = a[cols]
    a = a.sort_values(["symbol", "entry_ms"], kind="mergesort").reset_index(drop=True)
    b = b.sort_values(["symbol", "entry_ms"], kind="mergesort").reset_index(drop=True)
    if len(a) != len(b):
        return [f"{det} {label}: {len(a)} rows vs {len(b)}"]
    for c in a.columns:
        if str(a[c].dtype) != str(b[c].dtype):
            out.append(f"{det} {label}: column {c} dtype {a[c].dtype} != {b[c].dtype}")
            continue
        for i, (x, y) in enumerate(zip(a[c].tolist(), b[c].tolist())):
            if not _same(x, y):
                out.append(f"{det} {label}: {a['symbol'][i]} {iso(int(a['entry_ms'][i]))} "
                           f"column {c}: {x!r} != {y!r}")
                break
    return out


def gate_findings(scored: pd.DataFrame, base: pd.DataFrame, refused: set,
                  label: str) -> list[str]:
    ks, kb = keys_of(scored), keys_of(base)
    out = []
    if ks - kb:
        out.append(f"GATE-FOREIGN {label}: {len(ks - kb)} campaigns not in the base")
    if refused & ks:
        out.append(f"GATE-MISSED {label}: {len(refused & ks)} typed-refused campaigns still "
                   f"in the gated book (e.g. {sorted(refused & ks)[0]})")
    unnamed = (kb - ks) - refused
    if unnamed:
        out.append(f"GATE-UNNAMED {label}: {len(unnamed)} campaigns removed that the rule does "
                   f"not name (e.g. {sorted(unnamed)[0]})")
    keep = kb - refused
    bk = base[[k in keep for k in zip(base["symbol"], base["entry_ms"].astype(int))]]
    sk = scored[[k in keep for k in zip(scored["symbol"], scored["entry_ms"].astype(int))]]
    out += _row_diff(sk, bk, label, "GATE-ROW")
    return out


def cohort_findings(cohort: pd.DataFrame, base: pd.DataFrame, refused: set,
                    label: str) -> list[str]:
    out = []
    if keys_of(cohort) != refused:
        out.append(f"COHORT-SET {label}: {len(keys_of(cohort))} campaigns != the typed "
                   f"refused {len(refused)}")
    bk = base[[k in refused for k in zip(base["symbol"], base["entry_ms"].astype(int))]]
    if keys_of(cohort) == refused:
        out += _row_diff(cohort, bk, label, "COHORT-ROW")
    return out


def own_stop(sym: str, ti: int, d: int):
    """(Stop | None, atr) — v6's stop law (the lineage's struct_stop_4h on the lineage's
    pivots, railed at the TYPED 1.0 ATR) on THIS file's close and ATR."""
    X = own4(sym)
    at = float(X["atr"][ti])
    if not (np.isfinite(at) and at > 0):
        return None, at
    s_ = RC.struct_stop_4h(T9.frame(sym)["pv4"], int(ti), float(X["c"][ti]), int(d), at,
                           min_stop_atr=RAIL_TYPED, forbidden=None)
    if s_ is None or not (np.isfinite(s_.r_dist) and s_.r_dist > 0):
        return None, at
    return s_, at


def own_rule(tset: str, sym: str, ti: int, arm_i: int, r: float) -> bool:
    """A gate's TYPED rule evaluated on a candidate at its own trigger bar `ti`."""
    X = own4(sym)
    if tset in ("AGE", "ABS"):
        run = int(X["run"][ti])
        if tset == "ABS":
            return run > ABS_CUT_TYPED
        ed = own_edges(int(X["o"][ti]))
        return ed is not None and run > 0 and run >= ed[2]
    lag = int(ti) - int(arm_i)
    if tset == "WIN":
        return lag >= LAG_CUT_TYPED
    if tset == "LAG7_15":
        return SHADOW_LAG_TYPED[0] <= lag <= SHADOW_LAG_TYPED[1]
    if tset == "RATR":
        return float(r) > RATR_CUT_TYPED
    raise RuntimeError(f"no typed rule {tset}")


def own_ride(sym: str, ti: int, d: int, s_) -> dict:
    """v6's ride (tierc9._ride_leg9 + tierc7._account_chain) from the 4h close of `ti`,
    cached by (sym, ti, d) — the stop at a bar is a function of the bar."""
    k = ("ride", sym, int(ti), int(d))
    if k not in _C:
        X = own4(sym)
        leg = T9._ride_leg9(sym, TP.CONTROL_CARD, T9.V6_ROLES, d, ti, float(X["c"][ti]),
                            s_.stop_px, s_.r_dist, X["hi_i"])
        acc = T7._account_chain(sym, TP.CONTROL_CARD, d, s_.r_dist,
                                {"legs": [leg], "n_reentries": 0, "reentry_refused": ""})
        _C[k] = {"exit_i": int(leg["exit_i"]), "exit_reason": str(leg["exit_reason"]),
                 "net_r": float(acc["net_r"]), "gross_r": float(acc["gross_r"]),
                 "fee_r": float(acc["fee_r"]), "funding_r": float(acc["funding_r"])}
    return _C[k]


def own_replay(sym: str, cut: float | None, refuse: str | None = None, hold: int = 0) -> dict:
    """THIS FILE'S replay of card v6's candidate loop (and, with `cut`, of the
    L-G.3 priority rule) on its own read: armings, gates, windows, triggers,
    occupancy.  v6's stop law and ride are the lineage's (struct_stop_4h,
    _ride_leg9, _account_chain).  `refuse` = a typed gate evaluated on every
    candidate at its own trigger bar (a refused trigger does not occupy the slot:
    the re-ride); `hold` = F-EDGE's forced hold (every campaign holds its slot to
    its exit bar + `hold`, clipped at the corridor end)."""
    k = ("replay", sym, cut, refuse, int(hold))
    if k in _C:
        return _C[k]
    X = own4(sym)
    c, e89, e316, atr, n = X["c"], X["e89"], X["e316"], X["atr"], X["n"]
    lo_i, hi_i = X["lo_i"], X["hi_i"]
    arms = []
    for d, opens, counter in ((1, X["w_up"], X["w_dn"]), (-1, X["w_dn"], X["w_up"])):
        for i in (int(x) for x in np.flatnonzero(opens)):
            if not (lo_i <= i <= hi_i):
                continue
            later = np.flatnonzero(counter[i + 1:])
            end = int(i + 1 + later[0]) if later.size else n
            tide = (e89[i] > e316[i] and c[i] > e316[i]) if d == 1 else \
                (e89[i] < e316[i] and c[i] < e316[i])
            disp = abs(c[i] - e89[i]) / atr[i] if (np.isfinite(atr[i]) and atr[i] > 0) \
                else float("nan")
            arms.append({"i": i, "d": d, "end": end, "ms": int(X["o"][i]), "tide": bool(tide),
                         "d_ok": bool(np.isfinite(disp) and disp >= D_DISP_TYPED)})
    arms.sort(key=lambda a: (a["ms"], -a["d"]))
    wins = []
    for a in arms:
        if not (a["tide"] and a["d_ok"]):
            continue
        trig = X["t_up"] if a["d"] == 1 else X["t_dn"]
        endx = min(a["end"], hi_i + 1)
        cs = [a["i"] + int(x) for x in np.flatnonzero(trig[a["i"]:endx])]
        if cs:
            wins.append({**a, "endx": endx, "crosses": cs, "c0": cs[0]})
    wins.sort(key=lambda w: (w["c0"], -w["d"]))

    def ride(w, ti, s_, sub):
        rd = own_ride(sym, ti, w["d"], s_)
        return {"symbol": sym, "entry_i": int(ti), "entry_ms": int(X["o"][ti]), "d": w["d"],
                "arm_i": w["i"], "sub": sub, "entry_px": float(c[ti]),
                "stop_px": float(s_.stop_px), "r_dist": float(s_.r_dist),
                "r_over_atr": float(s_.r_dist) / float(atr[ti]),
                "exit_i": min(rd["exit_i"] + int(hold), hi_i), "exit_reason": rd["exit_reason"],
                "net_r": rd["net_r"], "gross_r": rd["gross_r"], "fee_r": rd["fee_r"],
                "funding_r": rd["funding_r"]}

    entries, wlog, open_until, n_po = [], [], -1, 0
    for w in wins:
        c0, d = w["c0"], w["d"]
        s0, a0 = own_stop(sym, c0, d)
        r0 = float(s0.r_dist) / a0 if s0 is not None else float("nan")
        rec = {"w": w, "r0": r0, "outcome": "", "entry": None, "scan": []}
        if not (cut is not None and s0 is not None and r0 > cut):
            if c0 <= open_until:
                rec["outcome"] = "position_open"
                n_po += 1
            elif s0 is None:
                rec["outcome"] = "no_stop"
            elif refuse is not None and own_rule(refuse, sym, c0, w["i"], r0):
                rec["outcome"] = "refused"
            else:
                e = ride(w, c0, s0, False)
                entries.append(e)
                open_until = e["exit_i"]
                rec.update(outcome="entered", entry=e)
        else:
            rec["outcome"] = "passed_no_substitute"
            for cc in w["crosses"][1:]:
                if cc <= open_until:
                    rec["scan"].append((cc, "not flat", float("nan")))
                    continue
                s_, a_ = own_stop(sym, cc, d)
                if s_ is None:
                    rec["scan"].append((cc, "no stop", float("nan")))
                    continue
                r = float(s_.r_dist) / a_
                if r > cut:
                    rec["scan"].append((cc, "r > 2.2", r))
                    continue
                if refuse is not None and own_rule(refuse, sym, cc, w["i"], r):
                    continue
                e = ride(w, cc, s_, True)
                entries.append(e)
                open_until = e["exit_i"]
                rec["scan"].append((cc, "SUBSTITUTE", r))
                rec.update(outcome="passed_substituted", entry=e)
                break
        wlog.append(rec)
    _C[k] = {"entries": entries, "wins": wlog, "n_position_open": n_po}
    return _C[k]


def own_rival_rows(planted=()) -> list[dict]:
    """Every position_open rejection of THIS file's own v6 replay (plus `planted`
    rejections (sym, trigger bar, arm bar, direction)), with its blocking campaign
    and, per typed gate, whether the blocker is refused (a RIVAL) and whether the
    gate's rule refuses the rival trigger itself at its own bar."""
    rows = []
    for s in CLASSIC5_TYPED:
        rp = own_replay(s, None)
        ents = rp["entries"]
        pos = [(rec["w"]["c0"], rec["w"]["i"], rec["w"]["d"]) for rec in rp["wins"]
               if rec["outcome"] == "position_open"]
        pos += [(int(ti), int(ai), int(d)) for ps, ti, ai, d in planted if ps == s]
        for c0, arm_i, d in pos:
            blk = [e for e in ents if e["entry_i"] <= c0 <= e["exit_i"]]
            if len(blk) != 1:
                raise RuntimeError(f"{s} bar {c0}: {len(blk)} blocking campaigns in the own replay")
            bk = (s, blk[0]["entry_ms"])
            s0, a0 = own_stop(s, c0, d)
            r0 = float(s0.r_dist) / a0 if s0 is not None else float("nan")
            rows.append({"symbol": s, "trigger_ms": int(own4(s)["o"][c0]), "direction": int(d),
                         "blocker_entry_ms": int(bk[1]),
                         "rival": {g: bk in typed_set(g) for g in GATE_ROW_OF},
                         "self": {g: bool(s0 is not None and own_rule(g, s, c0, arm_i, r0))
                                  for g in GATE_ROW_OF}})
    return rows


def own_position_open_rivals(planted=()) -> dict:
    """{gate: count} of the own rejections whose blocker is in the gate's typed set."""
    rows = own_rival_rows(planted)
    return {g: sum(1 for r in rows if r["rival"][g]) for g in GATE_ROW_OF}


def typed_era(close_ms: int) -> str:
    return "tuning" if int(close_ms) <= ERA_CUT_TYPED else "holdout"


def base_findings(b: pd.DataFrame, label: str) -> list[str]:
    """A base arm vs (i) the LINEAGE v6 Trade objects (T9.replay9) on every required
    column, exactly — exit_close_ms = the exit bar's open + 4h, stop_px = the INITIAL
    stop — and (ii) books/v6_campaigns on the 13 SC-7 columns at 6 dp."""
    out = []
    v6 = {(t.symbol, int(t.entry_ms)): t for t in v6_book()}
    ks = list(zip(b["symbol"].astype(str), b["entry_ms"].astype(np.int64).tolist()))
    if sorted(ks) != sorted(v6) or len(b) != V6_N_TYPED:
        return [f"BASE-KEYS {label}: keys are not the v6 book's {V6_N_TYPED}"]
    bad: dict = {}
    for i, k in enumerate(ks):
        t = v6[k]
        want = {"entry_close_ms": int(t.entry_ms) + MS4H, "direction": int(t.direction),
                "entry_px": float(t.entry_px), "stop_px": float(t.stop_px),
                "r_dist": float(t.r_dist), "exit_close_ms": int(t.exit_ms) + MS4H,
                "exit_reason": str(t.exit_reason), "net_r": float(t.net_r),
                "gross_r": float(t.gross_r), "fee_r": float(t.fee_r),
                "funding_r": float(t.funding_r), "lane": str(t.lane),
                "era": typed_era(int(t.entry_ms) + MS4H)}
        for c_, w in want.items():
            got = b[c_].iloc[i]
            got = got.item() if hasattr(got, "item") else got
            if not _same(got, w):
                bad.setdefault(c_, (0, f"{k[0]} {iso(k[1])}: {got!r} != lineage {w!r}"))
                bad[c_] = (bad[c_][0] + 1, bad[c_][1])
    for c_, (nb, ex) in sorted(bad.items()):
        out.append(f"BASE-COL {label}: {c_} differs from the lineage v6 book on {nb} row(s), "
                   f"e.g. {ex}")
    vc = pd.read_parquet(str(V6_CAMPAIGNS))
    m = b.merge(vc, on=["symbol", "entry_ms"], how="inner", suffixes=("_b", "_v"))
    if len(m) != V6_N_TYPED:
        return out + [f"BASE-V6COL {label}: {len(m)} rows join books/v6_campaigns"]
    for bc, vcn in SC7_TYPED:
        x = m[f"{bc}_b"] if f"{bc}_b" in m.columns else m[bc]
        y = m[f"{vcn}_v"] if f"{vcn}_v" in m.columns else m[vcn]
        if bc in FLOAT_REQ:
            nb = sum(1 for p, q in zip(x, y) if _f6(float(p)) != float(q))
        elif bc in ("entry_close_ms", "exit_close_ms", "direction"):
            nb = sum(1 for p, q in zip(x, y) if int(p) != int(q))
        else:
            nb = sum(1 for p, q in zip(x, y) if str(p) != str(q))
        if nb:
            out.append(f"BASE-V6COL {label}: {bc} differs from books/v6_campaigns {vcn} on {nb} "
                       f"row(s) at 6 dp")
    return out


def rival_planted_findings(label: str) -> tuple[list[str], int, int]:
    """ONE planted position_open rejection (an ETH trigger one bar into a P-AGE-1-refused
    campaign) fed to BOTH the module's rival_rows and this file's own counter: every
    gate's rival and self-refused counts must agree, and P-AGE-1's must see it (> 0)."""
    R = module_R()
    s = "ETHUSDT"
    age = typed_set("AGE")
    victim = next(t for t in v6_book() if t.symbol == s and (s, int(t.entry_ms)) in age
                  and int(t.exit_i) > int(t.entry_i))
    a0 = next(a for a in R["arms"][s] if a.reject == "entered")
    ti = int(victim.entry_i) + 1
    fake = dataclasses.replace(a0, trigger_i=ti, trigger_ms=int(own4(s)["o"][ti]),
                               reject="position_open", arm_i=int(victim.entry_i))
    arms = {k: list(v) for k, v in R["arms"].items()}
    arms[s] = arms[s] + [fake]
    rv = G.rival_rows(arms, R["v6"], R["pool"], R["facts"])
    own = own_rival_rows(planted=[(s, ti, int(victim.entry_i), int(a0.direction))])
    out = []
    for g in GATE_ROW_OF:
        got = int(rv[RIVAL_COL_TYPED[g]].sum()) if len(rv) else 0
        want = sum(1 for r in own if r["rival"][g])
        gs = int((rv[RIVAL_COL_TYPED[g]] & rv[SELF_COL_TYPED[g]]).sum()) if len(rv) else 0
        ws = sum(1 for r in own if r["rival"][g] and r["self"][g])
        if got != want or gs != ws:
            out.append(f"RIVAL-COUNT {label} {GATE_ROW_OF[g]}: module rivals {got} / self-refused "
                       f"{gs} != this file's {want} / {ws} on the same planted log")
    got_age = int(rv[RIVAL_COL_TYPED["AGE"]].sum()) if len(rv) else 0
    want_age = sum(1 for r in own if r["rival"]["AGE"])
    if want_age == 0 or got_age == 0:
        out.append(f"RIVAL-COUNT {label}: the planted rejection is not counted (module "
                   f"{got_age}, this file {want_age})")
    return out, got_age, want_age


def gate_break():
    base = reg_df("P-AGE-1", "base")
    sc = reg_df("P-AGE-1", "scored")
    age = typed_set("AGE")

    def extra():
        kept = sorted(keys_of(sc))
        drop = kept[len(kept) // 2]
        bent = sc[[k != drop for k in zip(sc["symbol"], sc["entry_ms"].astype(int))]]
        return gate_findings(bent, base, age, "[plant extra removal]")

    def moved_row():
        bent = sc.copy()
        bent.loc[bent.index[3], "net_r"] = float(bent["net_r"].iloc[3]) + 1e-12
        return gate_findings(bent, base, age, "[plant row moved]")

    def cohort_short():
        co = reg_df("P-AGE-1", "tierE__refused_cohort")
        return cohort_findings(co.iloc[1:], base, age, "[plant cohort short]")

    def apply_base():
        with mutated(G, "apply_gate", lambda book, refused: list(book)):
            G.compute()
        return []

    def unnamed_in_module():
        orig = G.refused_keys
        one = sorted(keys_of(sc))[7]

        def bent(facts, gate):
            s_ = orig(facts, gate)
            return s_ | {one} if gate == "P-AGE-1" else s_
        with mutated(G, "refused_keys", bent):
            R = G.compute()
            fr = G.regbook_dfs(R)
        return gate_findings(fr[("P-AGE-1", "scored")][3], fr[("P-AGE-1", "base")][3], age,
                             "[plant module refuses one unnamed]")

    def rival_blocker_kept():
        # the module's blocker_of names a campaign of the asset that P-AGE-1 KEEPS
        def bent(arm, trades_sym):
            return next(t for t in trades_sym if (t.symbol, int(t.entry_ms)) not in age)
        with mutated(G, "blocker_of", bent):
            return rival_planted_findings("[plant blocker_of names a kept campaign]")[0]

    def base_exit_open():
        return base_findings(base.assign(exit_close_ms=base["exit_close_ms"] - MS4H),
                             "[plant exit_close_ms at the exit bar's open]")

    def base_final_stop():
        v6 = {(t.symbol, int(t.entry_ms)): t for t in v6_book()}
        return base_findings(base.assign(stop_px=[float(v6[k].final_stop_px) for k in
                                                  zip(base["symbol"], base["entry_ms"].astype(int))]),
                             "[plant stop_px = the final trailed stop]")

    return plants([
        ("an UN-GATED book (scored == base)", "GATE-MISSED",
         lambda: gate_findings(base.copy(), base, age, "[plant un-gated]")),
        ("a gate that also removes one unnamed campaign", "GATE-UNNAMED", extra),
        ("a kept row's net_r moved 1e-12", "GATE-ROW", moved_row),
        ("the refused cohort missing one refused campaign", "COHORT-SET", cohort_short),
        ("the module's apply_gate returning the base (module must HALT)",
         "is not v6 minus exactly its refused set", apply_base),
        ("the module's refused set carrying one unnamed campaign", "GATE-UNNAMED",
         unnamed_in_module),
        ("the module's blocker_of naming a campaign the gate keeps (planted rejection fed "
         "to both counters)", "RIVAL-COUNT", rival_blocker_kept),
        ("(copy) a base arm's exit_close_ms at the exit bar's open", "BASE-COL",
         base_exit_open),
        ("(copy) a base arm's stop_px = the final trailed stop", "BASE-COL", base_final_stop),
    ])


def gate_real():
    bad, lines = [], []
    v6 = v6_book()
    v6k = {(t.symbol, int(t.entry_ms)) for t in v6}
    v6net = {(t.symbol, int(t.entry_ms)): float(t.net_r) for t in v6}
    bases = {}
    for reg in ("P-AGE-1", "P-WIN-1"):
        b = reg_df(reg, "base")
        bases[reg] = b
        if keys_of(b) != v6k or len(b) != V6_N_TYPED:
            bad.append(f"BASE {reg}: keys are not the v6 book's {V6_N_TYPED}")
        bad += base_findings(b, f"{reg}/base")
    bad += _row_diff(bases["P-AGE-1"], bases["P-WIN-1"], "P-AGE-1/base vs P-WIN-1/base",
                     "BASE")
    pf, got_p, want_p = rival_planted_findings("[planted log, real module]")
    bad += pf
    for reg, arm, tset, co in GATES_TYPED:
        ref = typed_set(tset)
        base = bases[reg]
        g = reg_df(reg, arm)
        f = gate_findings(g, base, ref, f"{reg}/{arm}")
        if co:
            f += cohort_findings(reg_df(reg, co), base, ref, f"{reg}/{co}")
        bad += f
        lines.append(f"{reg}/{arm} refuses {len(ref)} ({tset}) -> n {len(g)}")
        if arm == "scored":
            for era in ("tuning", "holdout"):
                sl = reg_df(reg, f"tierE__{era}")
                want = g[[("tuning" if int(x) <= ERA_CUT_TYPED else "holdout") == era
                          for x in g["entry_close_ms"]]]
                bad += _row_diff(sl, want, f"{reg}/tierE__{era}", "SLICE-ROW")
    # the gate-row table (refused n / ΣR, both books' ΣR, rivals) vs this file
    gr = stage_df("g_gate_rows").set_index("gate")
    riv = own_position_open_rivals()
    for tset, gate in GATE_ROW_OF.items():
        ref = typed_set(tset)
        rsum = math.fsum(v6net[k] for k in ref)
        ksum = math.fsum(v6net[k] for k in v6k - ref)
        row = gr.loc[gate]
        chk = {"n_refused": (int(row["n_refused"]), len(ref)),
               "sum_net_r_refused": (float(row["sum_net_r_refused"]), _f6(rsum)),
               "n_gated": (int(row["n_gated"]), len(v6k - ref)),
               "sum_net_r_gated": (float(row["sum_net_r_gated"]), _f6(ksum)),
               "sum_net_r_base": (float(row["sum_net_r_base"]),
                                  _f6(math.fsum(v6net.values()))),
               "rival_count_rejection_log": (int(row["rival_count_rejection_log"]), riv[tset])}
        for c_, (x, y) in chk.items():
            if not _same(x, y):
                bad.append(f"GATE-ROWS {gate}: {c_} {x} != own {y}")
        fo = str(row["forfeit_note"])
        mean_pos = len(ref) and rsum / len(ref) > 0
        if bool(fo) != bool(mean_pos):
            bad.append(f"GATE-ROWS {gate}: forfeit note {'present' if fo else 'absent'} but "
                       f"mean(refused) {'>' if mean_pos else '<='} 0")
    npo = sum(own_replay(s, None)["n_position_open"] for s in CLASSIC5_TYPED)
    return (not bad), (" · ".join(lines) + f"; each gated book == the written base minus "
                       f"EXACTLY the typed refused set, row-identical on every column; both "
                       f"refused cohorts == the base rows of their set; the four era slices == "
                       f"the scored rows of their era; both base arms == the lineage v6 Trade "
                       f"objects on every required column exactly (exit_close_ms = exit bar "
                       f"close, stop_px = the initial stop) and books/v6_campaigns on the 13 "
                       f"SC-7 columns at 6 dp, and each other; the gate-row table's refused / "
                       f"gated n and ΣR (6 dp) and forfeit notes == this file's; rival count == "
                       f"this file's replay: position_open rejections {npo}, rivals {riv}; one "
                       f"planted rejection fed to both counters: P-AGE-1 rivals module "
                       f"{got_p} == this file {want_p}, every gate's rival / self-refused count "
                       f"equal"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ══════════════════════════════════════════════════════════════ F-PRIORITY
def entries_of(book: list) -> list[dict]:
    """The module's priority book as entry records (Trade objects)."""
    out = []
    for t in book:
        out.append({"symbol": t.symbol, "entry_i": int(t.entry_i), "entry_ms": int(t.entry_ms),
                    "d": int(t.direction), "arm_i": int(t.arm_i),
                    "sub": bool(getattr(t, "priority_substitute", False)),
                    "stop_px": float(t.stop_px), "r_dist": float(t.r_dist),
                    "exit_i": int(t.exit_i), "exit_reason": str(t.exit_reason),
                    "net_r": float(t.net_r)})
    return out


def prio_findings(ents: list[dict], label: str) -> list[str]:
    out = []
    own = {s: own_replay(s, RATR_CUT_TYPED) for s in CLASSIC5_TYPED}
    oe = {(e["symbol"], e["entry_i"]): e for s in CLASSIC5_TYPED for e in own[s]["entries"]}
    me = {(e["symbol"], e["entry_i"]): e for e in ents}
    if len(me) != len(ents):
        out.append(f"PRIO-KEYS {label}: a repeated (symbol, entry bar)")
    if set(me) != set(oe):
        out.append(f"PRIO-KEYS {label}: {len(set(me) - set(oe))} entries this file's replay "
                   f"does not take, {len(set(oe) - set(me))} it takes that the module lacks")
    wins = {(s, rec["w"]["i"], rec["w"]["d"]): rec for s in CLASSIC5_TYPED
            for rec in own[s]["wins"]}
    for rec_k, rec in sorted(wins.items(), key=lambda kv: (kv[0][0], kv[0][1], kv[0][2])):
        s, w = rec_k[0], rec["w"]
        inw = [e for e in ents if e["symbol"] == s and e["arm_i"] == w["i"] and e["d"] == w["d"]]
        tag = f"{s} arm {iso(w['ms'])} d {w['d']:+d}"
        if not (rec["r0"] > RATR_CUT_TYPED):
            want = [w["c0"]] if rec["outcome"] == "entered" else []
            if [e["entry_i"] for e in inw] != want or any(e["sub"] for e in inw):
                out.append(f"PRIO-PASS {label} {tag}: first trigger r/ATR {rec['r0']:.4f} <= "
                           f"2.2 (v6's law: entry {want}) but the module entered "
                           f"{[(e['entry_i'], e['sub']) for e in inw]}")
        else:
            if any(e["entry_i"] == w["c0"] for e in inw):
                out.append(f"PRIO-PASS {label} {tag}: first trigger r/ATR {rec['r0']:.4f} > "
                           f"2.2 was entered, not passed")
            own_sub = rec["entry"]["entry_i"] if rec["entry"] is not None else None
            for e in inw:
                if e["entry_i"] == w["c0"]:
                    continue
                if not (w["c0"] < e["entry_i"] < w["endx"]):
                    out.append(f"PRIO-WINDOW {label} {tag}: substitute at bar {e['entry_i']} "
                               f"outside the window ({w['c0']}, {w['endx']})")
                    continue
                r = e["r_dist"] / float(own4(s)["atr"][e["entry_i"]])
                if r > RATR_CUT_TYPED:
                    out.append(f"PRIO-RATR {label} {tag}: substitute at {iso(e['entry_ms'])} has "
                               f"r/ATR {r:.4f} > 2.2")
                if own_sub is not None and e["entry_i"] > own_sub:
                    out.append(f"PRIO-FIRST {label} {tag}: substitute at bar {e['entry_i']} "
                               f"skipped the first qualifying cross {own_sub}")
            if len([e for e in inw if e["entry_i"] != w["c0"]]) > 1:
                out.append(f"PRIO-FIRST {label} {tag}: more than one substitute in one window")
    known = {(s, rec["w"]["i"], rec["w"]["d"]) for s, rec in
             ((s, r) for s in CLASSIC5_TYPED for r in own[s]["wins"])}
    for e in ents:
        if (e["symbol"], e["arm_i"], e["d"]) not in known:
            out.append(f"PRIO-WINDOW {label} {e['symbol']} {iso(e['entry_ms'])}: arm bar "
                       f"{e['arm_i']} is no window of this file's replay")
    for s in CLASSIC5_TYPED:
        seq = sorted((e for e in ents if e["symbol"] == s), key=lambda e: e["entry_i"])
        for a, b in zip(seq, seq[1:]):
            if b["entry_i"] <= a["exit_i"]:
                out.append(f"PRIO-FLAT {label} {s}: entry at bar {b['entry_i']} while the "
                           f"campaign entered at {a['entry_i']} is open to bar {a['exit_i']}")
    for k in sorted(set(me) & set(oe)):
        m, o = me[k], oe[k]
        for c_ in ("d", "sub", "stop_px", "r_dist", "exit_i", "exit_reason", "net_r"):
            if not _same(m[c_], o[c_]):
                out.append(f"PRIO-RIDE {label} {k[0]} bar {k[1]}: {c_} {m[c_]!r} != this "
                           f"file's {o[c_]!r}")
    ns_m, ns_o = sum(e["sub"] for e in ents), sum(e["sub"] for e in oe.values())
    if ns_m != ns_o:
        out.append(f"PRIO-COUNT {label}: {ns_m} substitutions != this file's {ns_o}")
    return out


def prio_written_findings(w: pd.DataFrame, label: str) -> list[str]:
    """The WRITTEN priority arm vs this file's replay of the rule, every required
    column (floats exact: the regbook is written at full precision)."""
    oe = {(e["symbol"], e["entry_ms"]): e for s in CLASSIC5_TYPED
          for e in own_replay(s, RATR_CUT_TYPED)["entries"]}
    ks = list(zip(w["symbol"].astype(str), w["entry_ms"].astype(np.int64).tolist()))
    if sorted(ks) != sorted(oe) or len(ks) != len(oe):
        return [f"PRIO-WRITTEN {label}: {len(ks)} rows, keys != this file's {len(oe)} entries"]
    bad: dict = {}
    for i, k in enumerate(ks):
        e = oe[k]
        X = own4(k[0])
        want = {"priority_substitute": bool(e["sub"]), "direction": int(e["d"]),
                "entry_close_ms": int(k[1]) + MS4H, "entry_px": e["entry_px"],
                "stop_px": e["stop_px"], "r_dist": e["r_dist"],
                "exit_close_ms": int(X["o"][e["exit_i"]]) + MS4H,
                "exit_reason": e["exit_reason"], "net_r": e["net_r"], "gross_r": e["gross_r"],
                "fee_r": e["fee_r"], "funding_r": e["funding_r"],
                "era": typed_era(int(k[1]) + MS4H)}
        for c_, v in want.items():
            got = w[c_].iloc[i]
            got = got.item() if hasattr(got, "item") else got
            if not _same(got, v):
                bad.setdefault(c_, [0, f"{k[0]} {iso(k[1])}: {got!r} != own {v!r}"])
                bad[c_][0] += 1
    return [f"PRIO-WRITTEN {label}: {c_} differs from this file's replay on {nb} row(s), e.g. "
            f"{ex}" for c_, (nb, ex) in sorted(bad.items())]


def prio_break():
    lo, hi = LO_TYPED, PIN - 1

    def under(name, fn):
        def thunk():
            with mutated(G, name, fn):
                bk, _ = G.replay_book(lo, hi, priority_cut=G.RATR_CUT)
            return prio_findings(entries_of(bk), f"[plant {name}]")
        return thunk

    real = entries_of(module_R()["priority"])

    def flat_copy():
        ents = copy.deepcopy(real)
        for i, e in enumerate(ents):
            prev = [x for x in ents if x["symbol"] == e["symbol"] and x["entry_i"] < e["entry_i"]]
            if e["sub"] and prev:
                p = max(prev, key=lambda x: x["entry_i"])
                ents[i] = dict(e, entry_i=int(p["exit_i"]))
                break
        return prio_findings(ents, "[plant substitute inside the previous campaign]")

    def ride_copy():
        ents = copy.deepcopy(real)
        i = next(j for j, e in enumerate(ents) if e["sub"])
        ents[i] = dict(ents[i], net_r=ents[i]["net_r"] + 1e-9)
        return prio_findings(ents, "[plant substitute net_r +1e-9]")

    wr = reg_df("P-WIN-1", "tierE__ratr_priority")

    def written_exit_open():
        return prio_written_findings(wr.assign(exit_close_ms=wr["exit_close_ms"] - MS4H),
                                     "[plant exit_close_ms at the exit bar's open]")

    def written_stop_bent():
        b = wr.copy()
        b.loc[b.index[5], "stop_px"] = float(b["stop_px"].iloc[5]) * (1.0 + 1e-9)
        return prio_written_findings(b, "[plant one stop_px bent 1e-9]")

    return plants([
        ("the substitute's r_over_atr <= 2.2 test ignored", "PRIO-RATR",
         under("sub_admissible", lambda r, cut: True)),
        ("the substitute scan run past the window's close", "PRIO-WINDOW",
         under("window_end", lambda a, hi_i: int(hi_i) + 1)),
        ("the pass rule inverted (pass when r_over_atr <= 2.2)", "PRIO-PASS",
         under("ratr_ok", lambda r, cut: float(r) > float(cut))),
        ("(copy) one substitute moved inside its asset's previous campaign", "PRIO-FLAT",
         flat_copy),
        ("(copy) one substitute's net_r +1e-9", "PRIO-RIDE", ride_copy),
        ("(copy) the written arm's exit_close_ms at the exit bar's open", "PRIO-WRITTEN",
         written_exit_open),
        ("(copy) one written stop_px bent 1e-9", "PRIO-WRITTEN", written_stop_bent),
    ])


def prio_real():
    lo, hi = LO_TYPED, PIN - 1
    bad = []
    # (a) identity: replay_g without hooks == replay9 at 0.000e+00; own replay == v6
    ident, _ = G.replay_book(lo, hi)
    ok, worst, why = TP.ctrl_diff(TP.journal_frame(ident), TP.journal_frame(v6_book()))
    if not ok or worst != 0.0:
        bad.append(f"PRIO-IDENT: replay_g (no hook) vs T9.replay9 — {why}")
    ownv6 = {(e["symbol"], e["entry_ms"]) for s in CLASSIC5_TYPED
             for e in own_replay(s, None)["entries"]}
    if ownv6 != {(t.symbol, int(t.entry_ms)) for t in v6_book()}:
        bad.append("PRIO-IDENT: this file's own v6 replay is not the v6 book")
    own_net = {(e["symbol"], e["entry_ms"]): e["net_r"] for s in CLASSIC5_TYPED
               for e in own_replay(s, None)["entries"]}
    if any(own_net.get((t.symbol, int(t.entry_ms))) != float(t.net_r) for t in v6_book()):
        bad.append("PRIO-IDENT: this file's own v6 replay's net_r differs from the book")
    # (b) the priority book in-process and as written
    R = module_R()
    ents = entries_of(R["priority"])
    bad += prio_findings(ents, "in-process")
    w = reg_df("P-WIN-1", "tierE__ratr_priority")
    oe = [e for s in CLASSIC5_TYPED for e in own_replay(s, RATR_CUT_TYPED)["entries"]]
    bad += prio_written_findings(w, "written tierE__ratr_priority")
    # (c) three substitutions hand-walked (seeded choice), printed
    subs = [e for e in oe if e["sub"]]
    pick = sorted(int(i) for i in np.random.default_rng(SEED).choice(len(subs), 3,
                                                                      replace=False))
    for j in pick:
        e = subs[j]
        s = e["symbol"]
        rec = next(r for r in own_replay(s, RATR_CUT_TYPED)["wins"]
                   if r["entry"] is not None and r["entry"]["entry_i"] == e["entry_i"])
        X, wv = own4(s), rec["w"]
        scan = "; ".join(f"{iso(int(X['o'][cc]))} {why}" + (f" r/ATR {r:.4f}" if r == r else "")
                         for cc, why, r in rec["scan"])
        mod = next((m for m in ents if m["symbol"] == s and m["entry_i"] == e["entry_i"]), None)
        say(f"  [HAND] {s} {'long' if wv['d'] == 1 else 'short'} · arm (12/89) "
            f"{iso(wv['ms'])} · window closes (counter 12/89) "
            f"{iso(int(X['o'][wv['endx']])) if wv['endx'] < X['n'] else 'open at the pin'} · "
            f"first 12/26 trigger {iso(int(X['o'][wv['c0']]))} r/ATR {rec['r0']:.4f} > 2.2 -> "
            f"PASSED · later crosses: {scan}")
        say(f"         entry {iso(e['entry_ms'])} close {float(X['c'][e['entry_i']])!r} · stop "
            f"{e['stop_px']!r} · R {e['r_dist']!r} · r/ATR {e['r_over_atr']:.6f} · exit "
            f"{iso(int(X['o'][e['exit_i']]))} {e['exit_reason']} · net_r {e['net_r']:+.6f} "
            f"(_ride_leg9 + _account_chain) == module "
            f"{(mod['net_r'] if mod else float('nan')):+.6f}: "
            f"{mod is not None and mod['net_r'] == e['net_r']}")
    ow = [r for s in CLASSIC5_TYPED for r in own_replay(s, RATR_CUT_TYPED)["wins"]]
    oc = {k: sum(1 for r in ow if r["outcome"] == k) for k in
          ("entered", "passed_substituted", "passed_no_substitute", "position_open", "no_stop")}
    return (not bad), (f"replay_g without hooks == T9.replay9 on all 200 (CTRL_COLS worst "
                       f"{worst:.3e}); this file's own replay of v6 == the v6 book (200 keys, "
                       f"net_r exact); the priority book (in-process {len(ents)} entries, and the "
                       f"written regbook on every required column: entry_px, stop_px, r_dist, "
                       f"exit_close_ms, exit_reason, gross / fee / funding / net R, era) == this "
                       f"file's own replay of the rule on every entry "
                       f"(pass, substitute = first later flat cross with r/ATR <= 2.2 inside the "
                       f"window, stop, R, exit bar, reason, net_r exact, no overlap); windows "
                       f"{oc}; substitutions {len(subs)}; 3 hand-walked (seeded {pick})"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-DISC
def _w6(df: pd.DataFrame) -> pd.DataFrame:
    """An in-process table as the writer files it: every float column at 6 dp."""
    d = df.copy()
    for c in d.columns:
        if pd.api.types.is_float_dtype(d[c]):
            d[c] = d[c].round(6)
    return d


def own_stats(vals) -> dict:
    v = [float(x) for x in vals]
    n = len(v)
    if n == 0:
        return {"n": 0, "sum_net_r": 0.0, "mean_net_r": float("nan"), "win_pct": float("nan")}
    s = math.fsum(v)
    return {"n": n, "sum_net_r": _f6(s), "mean_net_r": _f6(s / n),
            "win_pct": _f6(100.0 * sum(1 for x in v if x > 0) / n)}


def _val(x):
    if x is None or x is pd.NA:
        return None
    return x.item() if hasattr(x, "item") else x


def _cmp(out: list, det: str, label: str, row, want: dict) -> None:
    for c_, v in want.items():
        got = _val(row[c_]) if c_ in row.index else "<absent>"
        if not _same(got, v):
            out.append(f"{det} {label}: {c_} {got!r} != own {v!r}")


def v6_net() -> dict:
    return {(t.symbol, int(t.entry_ms)): float(t.net_r) for t in v6_book()}


def own_reride(g: str) -> list[dict]:
    return [e for s in CLASSIC5_TYPED for e in own_replay(s, None, refuse=g)["entries"]]


def has_abs_label(txt) -> bool:
    t = str(txt).lower()
    return all(p in t for p in ABS_PHRASES_TYPED)


def disc_gate_rows(gr: pd.DataFrame) -> list[str]:
    out = []
    net = v6_net()
    v6k = set(net)
    if sorted(gr["gate"]) != sorted(GATE_ROW_OF.values()):
        return [f"DISC-GATEROW: gate rows {sorted(gr['gate'])} != typed"]
    gi = gr.set_index("gate")
    riv = own_rival_rows()
    s0 = own_stats(net.values())
    for g, gate in GATE_ROW_OF.items():
        row = gi.loc[gate]
        ref = typed_set(g)
        sb, sr = own_stats(net[k] for k in v6k - ref), own_stats(net[k] for k in ref)
        _cmp(out, "DISC-GATEROW", gate, row, {
            "n_base": s0["n"], "sum_net_r_base": s0["sum_net_r"], "n_gated": sb["n"],
            "sum_net_r_gated": sb["sum_net_r"], "mean_net_r_gated": sb["mean_net_r"],
            "n_refused": sr["n"], "mean_net_r_refused": sr["mean_net_r"],
            "sum_net_r_refused": sr["sum_net_r"]})
        rsum = math.fsum(net[k] for k in ref)
        want_note = FORFEIT_TYPED.format(x=rsum) if ref and rsum / len(ref) > 0 else ""
        if str(row["forfeit_note"]) != want_note:
            out.append(f"DISC-FORFEIT {gate}: forfeit note {str(row['forfeit_note'])!r} != "
                       f"{want_note!r} (X = the refused ΣR {rsum:+.6f}) [L-1.5]")
        _cmp(out, "DISC-RIVAL", gate, row, {
            "rival_count_rejection_log": sum(1 for r in riv if r["rival"][g]),
            "rival_count_self_refused": sum(1 for r in riv if r["rival"][g] and r["self"][g])})
        rr = own_reride(g)
        rrk = {(e["symbol"], e["entry_ms"]) for e in rr}
        srr = own_stats(e["net_r"] for e in rr)
        _cmp(out, "DISC-RERIDE", gate, row, {
            "reride_n": srr["n"], "reride_sum_net_r": srr["sum_net_r"],
            "reride_mean_net_r": srr["mean_net_r"], "reride_admitted_not_in_v6": len(rrk - v6k),
            "reride_v6_not_taken": len(v6k - rrk)})
        if gate == ABS_GATE_TYPED and not has_abs_label(row.get("caveat", "")):
            out.append(f"DISC-LABEL {gate}: the shadow's gate row does not say that 206 is the "
                       f"whole-corridor median edge, not the OLD edge, reading the corridor ahead")
    return out


def disc_tide(tb: pd.DataFrame) -> list[str]:
    out = []
    own, net = own_facts(), v6_net()
    want = {}
    for b in BANDS_TYPED:
        ks = [k for k, f in own.items() if f["band"] == b]
        want[(TIDE_MEASURES_TYPED[0], b)] = (ks, "cens")
        ks = [k for k, f in own.items() if f["arm_band"] == b]
        want[(TIDE_MEASURES_TYPED[1], b)] = (ks, "arm_cens")
    for v in (True, False):
        lab = ">206" if v else "<=206"
        want[(TIDE_MEASURES_TYPED[2], lab)] = ([k for k, f in own.items() if f["ABS"] == v], "cens")
        want[(TIDE_MEASURES_TYPED[3], lab)] = (
            [k for k, f in own.items() if (f["arm_age"] > ABS_CUT_TYPED) == v], "arm_cens")
    ti = tb.set_index(["measure", "band"])
    for (m, b), (ks, cens) in want.items():
        if (m, b) not in ti.index:
            out.append(f"DISC-TIDE {m}|{b}: row absent")
            continue
        row = ti.loc[(m, b)]
        _cmp(out, "DISC-TIDE", f"{m}|{b}", row,
             {**own_stats(net[k] for k in ks),
              "n_left_censored": sum(1 for k in ks if own[k][cens])})
        if m in TIDE_MEASURES_TYPED[2:] and not has_abs_label(row.get("caveat", "")):
            out.append(f"DISC-LABEL {m}|{b}: the >206 row does not carry the label (whole-corridor "
                       f"median edge, not the OLD edge, reads the corridor ahead)")
    return out


def own_books_for_collisions() -> dict:
    own = own_facts()
    v6 = [(k, own[k]["r_over_atr"]) for k in own]
    pri = [((e["symbol"], e["entry_ms"]), e["r_over_atr"]) for s in CLASSIC5_TYPED
           for e in own_replay(s, RATR_CUT_TYPED)["entries"]]
    return {"v6": v6,
            "P-AGE-1 scored": [x for x in v6 if x[0] not in typed_set("AGE")],
            "P-WIN-1 scored": [x for x in v6 if x[0] not in typed_set("WIN")],
            "ratr admission": [x for x in v6 if x[0] not in typed_set("RATR")],
            "ratr priority": pri}


def own_collision_row(book: list, min_n: int = 2) -> dict:
    by: dict = {}
    for (s, m), r in book:
        by.setdefault(int(m) + MS4H, []).append(r)
    coll = {k: v for k, v in by.items() if len(v) >= min_n}
    return {"n_campaigns": len(book), "n_entry_closes": len(by), "n_collision_closes": len(coll),
            "n_campaigns_in_collisions": sum(len(v) for v in coll.values()),
            "max_assets_at_one_close": max((len(v) for v in by.values()), default=0),
            "n_collisions_mixed_ratr_class": sum(
                1 for v in coll.values() if len({r > RATR_CUT_TYPED for r in v}) > 1)}


def disc_collisions(co: pd.DataFrame) -> list[str]:
    out = []
    if sorted(co["book"]) != sorted(COLLISION_BOOKS_TYPED):
        return [f"DISC-COLLIDE: books {sorted(co['book'])} != typed"]
    ci = co.set_index("book")
    for name, bk in own_books_for_collisions().items():
        _cmp(out, "DISC-COLLIDE", name, ci.loc[name], own_collision_row(bk))
    return out


def disc_collist(cl: pd.DataFrame) -> list[str]:
    own, net = own_facts(), v6_net()
    by: dict = {}
    for k in own:
        by.setdefault(k[1] + MS4H, []).append(k)
    want = {(ec, k[0]): {"direction": int(next(t.direction for t in v6_book()
                                                if (t.symbol, int(t.entry_ms)) == k)),
                         "r_over_atr": _f6(own[k]["r_over_atr"]), "net_r": _f6(net[k]),
                         "placeholder": False}
            for ec, ks in by.items() if len(ks) >= 2 for k in ks}
    real = cl[~cl["placeholder"].astype(bool)]
    ph = cl[cl["placeholder"].astype(bool)]
    out = []
    got = {(int(a), str(b)) for a, b in zip(real["entry_close_ms"], real["symbol"])}
    if got != set(want) or len(real) != len(want):
        out.append(f"DISC-COLLIST: {len(real)} listed (close, asset) rows != this file's "
                   f"{len(want)} ({len(got - set(want))} extra, {len(set(want) - got)} missing)")
    if len(ph) != (0 if want else 1):
        out.append(f"DISC-COLLIST: {len(ph)} placeholder row(s), want {0 if want else 1}")
    ri = real.set_index(["entry_close_ms", "symbol"])
    for k, w in want.items():
        if k in ri.index:
            _cmp(out, "DISC-COLLIST", f"{iso(k[0])} {k[1]}", ri.loc[k], w)
    return out


def disc_arrivals(ar: pd.DataFrame) -> list[str]:
    """kinds typed here: entered_after_tc10_pin = entry close > the TC10 pin; continuation =
    entry close <= the pin and the exit bar opening at or after it (open at the pin)."""
    own, out = own_facts(), []
    want = {}
    for t in v6_book():
        ec = int(t.entry_ms) + MS4H
        kind = ("entered_after_tc10_pin" if ec > TC10_PIN else
                "continuation" if int(t.exit_ms) >= TC10_PIN else None)
        if kind is None:
            continue
        f = own[(t.symbol, int(t.entry_ms))]
        want[(kind, t.symbol, int(t.entry_ms))] = {
            "exit": iso(int(t.exit_ms)), "exit_reason": str(t.exit_reason),
            "net_r": _f6(float(t.net_r)), "tide_band": f["band"], "age_old_refused": f["AGE"],
            "lag": f["lag"], "win_refused": f["WIN"], "placeholder": False}
    for kind in ("entered_after_tc10_pin", "continuation"):
        if not any(k[0] == kind for k in want):
            want[(kind, "(none)", -1)] = {"net_r": float("nan"), "age_old_refused": None,
                                          "lag": None, "win_refused": None, "placeholder": True}
    got = {(str(a), str(b), int(c)) for a, b, c in zip(ar["kind"], ar["symbol"], ar["entry_ms"])}
    if got != set(want) or len(ar) != len(want):
        out.append(f"DISC-ARRIVALS: rows {len(ar)} != this file's {len(want)} "
                   f"({len(got - set(want))} extra, {len(set(want) - got)} missing)")
    ai = ar.set_index(["kind", "symbol", "entry_ms"])
    for k, w in want.items():
        if k in ai.index:
            _cmp(out, "DISC-ARRIVALS", f"{k[0]} {k[1]} {k[2]}", ai.loc[k], w)
    return out


def disc_windows(pw: pd.DataFrame) -> list[str]:
    out, net = [], v6_net()
    want = {}
    for s in CLASSIC5_TYPED:
        X = own4(s)
        for rec in own_replay(s, RATR_CUT_TYPED)["wins"]:
            w, e = rec["w"], rec["entry"]
            c0ms = int(X["o"][w["c0"]])
            scan = [x[1] for x in rec["scan"]]
            want[(s, w["ms"], w["d"])] = {
                "first_trigger_ms": c0ms, "window_end_i": int(w["endx"]),
                "first_r_over_atr": _f6(rec["r0"]) if rec["r0"] == rec["r0"] else float("nan"),
                "outcome": OUTCOME_NAME_TYPED[rec["outcome"]],
                "entry_i": (int(e["entry_i"]) if e else None),
                "entry_ms": (int(e["entry_ms"]) if e else None),
                "entry_r_over_atr": (_f6(e["r_over_atr"]) if e else float("nan")),
                "n_scanned": len(scan), "n_scan_not_flat": scan.count("not flat"),
                "n_scan_no_stop": scan.count("no stop"), "n_scan_over_cut": scan.count("r > 2.2"),
                "v6_net_r_at_first_trigger": (_f6(net[(s, c0ms)]) if (s, c0ms) in net
                                              else float("nan")),
                "priority_net_r": (_f6(e["net_r"]) if e else float("nan"))}
    got = {(str(a), int(b), int(c)) for a, b, c in zip(pw["symbol"], pw["arm_ms"], pw["direction"])}
    if got != set(want) or len(pw) != len(want):
        out.append(f"DISC-WINDOWS: {len(pw)} windows != this file's {len(want)}")
    wi = pw.set_index(["symbol", "arm_ms", "direction"])
    for k, w in sorted(want.items()):
        if k in wi.index:
            _cmp(out, "DISC-WINDOWS", f"{k[0]} arm {iso(k[1])} d {k[2]:+d}", wi.loc[k], w)
    return out


def disc_rivals(rv: pd.DataFrame) -> list[str]:
    own, out = own_rival_rows(), []
    ph = rv["placeholder"].astype(bool) if "placeholder" in rv.columns else None
    if ph is None:
        return ["DISC-RIVALS: no placeholder column"]
    real = rv[~ph]
    if not own:
        if len(rv) != 1 or not bool(ph.iloc[0]) or str(rv["symbol"].iloc[0]) != "(none)":
            out.append(f"DISC-RIVALS: this file counts 0 position_open rejections; the table "
                       f"holds {len(rv)} row(s), placeholder flags {list(ph)}")
        else:
            for c_ in ("arm_ms", "trigger_close_ms", "blocker_entry_ms", "blocker_exit_ms",
                       "blocker_net_r"):
                if c_ in rv.columns and _val(rv[c_].iloc[0]) is not None and \
                        not (isinstance(_val(rv[c_].iloc[0]), float)
                             and math.isnan(_val(rv[c_].iloc[0]))):
                    out.append(f"DISC-RIVALS: the placeholder row carries {c_} = "
                               f"{_val(rv[c_].iloc[0])!r} (want null)")
        return out
    want = {(r["symbol"], r["trigger_ms"], r["direction"]): r for r in own}
    got = {(str(a), int(b), int(c)) for a, b, c in zip(real["symbol"], real["trigger_ms"],
                                                        real["direction"])}
    if got != set(want) or len(rv) != len(want):
        out.append(f"DISC-RIVALS: {len(real)} rows (+{int(ph.sum())} placeholder) != this file's "
                   f"{len(want)}")
    ri = real.set_index(["symbol", "trigger_ms", "direction"])
    for k, r in want.items():
        if k in ri.index:
            _cmp(out, "DISC-RIVALS", f"{k}", ri.loc[k],
                 {"blocker_entry_ms": r["blocker_entry_ms"],
                  **{RIVAL_COL_TYPED[g]: r["rival"][g] for g in GATE_ROW_OF},
                  **{SELF_COL_TYPED[g]: r["self"][g] for g in GATE_ROW_OF}})
    return out


def disc_pvs(pv: pd.DataFrame) -> list[str]:
    own, net, out = own_facts(), v6_net(), []
    pr = {(e["symbol"], e["entry_ms"]): e for s in CLASSIC5_TYPED
          for e in own_replay(s, RATR_CUT_TYPED)["entries"]}
    want = {}
    for k in set(net) | set(pr):
        want[k] = {"in_v6": k in net, "in_priority": k in pr,
                   "priority_substitute": bool(pr[k]["sub"]) if k in pr else False,
                   "v6_net_r": _f6(net[k]) if k in net else float("nan"),
                   "priority_net_r": _f6(pr[k]["net_r"]) if k in pr else float("nan"),
                   "r_over_atr": _f6(own[k]["r_over_atr"] if k in net else pr[k]["r_over_atr"])}
    got = {(str(a), int(b)) for a, b in zip(pv["symbol"], pv["entry_ms"])}
    if got != set(want) or len(pv) != len(want):
        out.append(f"DISC-PVS: {len(pv)} keys != this file's {len(want)}")
    pi = pv.set_index(["symbol", "entry_ms"])
    for k, w in sorted(want.items()):
        if k in pi.index:
            _cmp(out, "DISC-PVS", f"{k[0]} {iso(k[1])}", pi.loc[k], w)
    return out


def disc_findings(fr: dict) -> list[str]:
    return (disc_gate_rows(fr["g_gate_rows"]) + disc_tide(fr["g_tide_bands"])
            + disc_collisions(fr["g_collisions"]) + disc_collist(fr["g_collision_list_v6"])
            + disc_arrivals(fr["g_arrivals"]) + disc_windows(fr["g_priority_windows"])
            + disc_rivals(fr["g_rivals"]) + disc_pvs(fr["g_priority_vs_v6"]))


def disc_break():
    fr = _frames()

    def with_(name, d):
        x = dict(fr)
        x[name] = d
        return disc_findings(x)

    def reride_lag_minus_1():
        orig = G.refuse_hook

        def bent(gate, pool):
            if gate == "P-WIN-1":
                return lambda ctx: G.win_refused(int(ctx["ti"]) - int(ctx["arm"].arm_i) - 1)
            return orig(gate, pool)
        with mutated(G, "refuse_hook", bent):
            R = G.compute()
        return disc_gate_rows(_w6(R["tables"]["g_gate_rows"][0]))

    gr = fr["g_gate_rows"]

    def on_gate(gate, **cols):
        d = gr.copy()
        i = d.index[d["gate"] == gate][0]
        for c_, v in cols.items():
            d.loc[i, c_] = v(d.loc[i]) if callable(v) else v
        return d

    tb = fr["g_tide_bands"]

    def tide_arm_reads_entry_flag():
        d = tb.copy()
        for lab in (">206", "<=206"):
            src = d[(d["measure"] == TIDE_MEASURES_TYPED[2]) & (d["band"] == lab)].iloc[0]
            j = d.index[(d["measure"] == TIDE_MEASURES_TYPED[3]) & (d["band"] == lab)][0]
            for c_ in ("n", "sum_net_r", "mean_net_r", "win_pct"):
                d.loc[j, c_] = src[c_]
        return d

    def tide_on_shadow(**cols):
        d = tb.copy()
        m = d["measure"] == TIDE_MEASURES_TYPED[2]
        for c_, v in cols.items():
            d.loc[m, c_] = v
        return d

    co = fr["g_collisions"]

    def collide_ge3():
        d = co.copy()
        j = d.index[d["book"] == "v6"][0]
        n3 = own_collision_row(own_books_for_collisions()["v6"], min_n=3)["n_collision_closes"]
        d.loc[j, "n_collision_closes"] = n3 if n3 != int(d.loc[j, "n_collision_closes"]) else n3 + 1
        return d

    ar = fr["g_arrivals"]

    def arrivals_199():
        base = ar[~ar["placeholder"].astype(bool)].iloc[[0]]
        cont = {(str(s), int(m)) for s, m in zip(ar["symbol"], ar["entry_ms"])}
        extra = [(t.symbol, int(t.entry_ms)) for t in v6_book()
                 if (t.symbol, int(t.entry_ms)) not in cont]
        if not extra:                       # (a module that already lists them all)
            return ar.assign(kind="continuation")
        rows = pd.concat([base] * len(extra), ignore_index=True)
        rows["symbol"] = [k[0] for k in extra]
        rows["entry_ms"] = [k[1] for k in extra]
        rows["kind"] = "continuation"
        return pd.concat([ar, rows], ignore_index=True)

    pw = fr["g_priority_windows"]
    pv = fr["g_priority_vs_v6"]

    def pvs_moved():
        d = pv.copy()
        j = d.index[d["in_priority"].astype(bool)][4]
        d.loc[j, "priority_net_r"] = float(d.loc[j, "priority_net_r"]) + 1e-6
        return d

    cl = fr["g_collision_list_v6"]
    rv = fr["g_rivals"]
    return plants([
        ("the module's re-ride hook for P-WIN-1 at lag - 1", "DISC-RERIDE", reride_lag_minus_1),
        ("(copy) forfeit X from the GATED sum", "DISC-FORFEIT", lambda: with_(
            "g_gate_rows", on_gate("L-G.3/ratr_admission", forfeit_note=lambda r: FORFEIT_TYPED
                                   .format(x=float(r["sum_net_r_gated"]))))),
        ("(copy) the refused mean replaced by the gated mean", "DISC-GATEROW", lambda: with_(
            "g_gate_rows", on_gate("P-AGE-1", mean_net_r_refused=lambda r:
                                   float(r["mean_net_r_gated"])))),
        ("(copy) collisions counted at >= 3 assets", "DISC-COLLIDE",
         lambda: with_("g_collisions", collide_ge3())),
        ("(copy) the arm-bar >206 rows read the entry-bar flag", "DISC-TIDE",
         lambda: with_("g_tide_bands", tide_arm_reads_entry_flag())),
        ("(copy) n_left_censored -1 on the >206 rows", "DISC-TIDE",
         lambda: with_("g_tide_bands", tide_on_shadow(n_left_censored=-1))),
        ("(copy) the window log's scan counts doubled", "DISC-WINDOWS",
         lambda: with_("g_priority_windows", pw.assign(n_scan_over_cut=pw["n_scan_over_cut"] * 2))),
        ("(copy) every campaign marked continuation (199 rows)", "DISC-ARRIVALS",
         lambda: with_("g_arrivals", arrivals_199())),
        ("(copy) a re-ride ΣR + 1", "DISC-RERIDE", lambda: with_(
            "g_gate_rows", on_gate("P-AGE-1", reride_sum_net_r=lambda r:
                                   float(r["reride_sum_net_r"]) + 1.0))),
        ("(copy) the rival placeholder flag dropped", "DISC-RIVALS",
         lambda: with_("g_rivals", rv.assign(placeholder=False))),
        ("(copy) the >206 caveat dropped from the tide rows", "DISC-LABEL",
         lambda: with_("g_tide_bands", tide_on_shadow(caveat=""))),
        ("(copy) the >206 caveat dropped from the shadow's gate row", "DISC-LABEL",
         lambda: with_("g_gate_rows", on_gate(ABS_GATE_TYPED, caveat=""))),
        ("(copy) one v6 collision row dropped", "DISC-COLLIST",
         lambda: with_("g_collision_list_v6", cl.iloc[1:])),
        ("(copy) one priority_net_r moved 1e-6", "DISC-PVS",
         lambda: with_("g_priority_vs_v6", pvs_moved())),
    ])


def disc_real():
    fr = _frames()
    bad = disc_findings(fr)
    net = v6_net()
    rr = {g: own_reride(g) for g in GATE_ROW_OF}
    rrs = {GATE_ROW_OF[g]: (len(v), f"{math.fsum(e['net_r'] for e in v):+.6f}")
           for g, v in rr.items()}
    ratr = typed_set("RATR")
    say(f"  [DISC] this file's own re-ride per gate (the gate's rule as a refusal hook at each "
        f"trigger bar), n / ΣR: {rrs}")
    say(f"  [DISC] forfeit note on the r/ATR admission row: mean(refused) "
        f"{math.fsum(net[k] for k in ratr) / len(ratr):+.6f} > 0 -> X = "
        f"{math.fsum(net[k] for k in ratr):+.4f}; the four others carry none (mean <= 0)")
    cb = {n: own_collision_row(b)["n_collision_closes"] for n, b in own_books_for_collisions().items()}
    say(f"  [DISC] collision closes (>= 2 assets) per book: {cb}; own position_open rejections "
        f"{len(own_rival_rows())}; arrivals rows {len(fr['g_arrivals'])} (placeholder "
        f"{int(fr['g_arrivals']['placeholder'].astype(bool).sum())})")
    return (not bad), (f"every disclosure table == this file's recomputation: g_gate_rows (5 "
                       f"gates: base / gated / refused n, ΣR, mean; forfeit text and X; rival "
                       f"counts; re-ride n / ΣR / mean / not-in-v6 / v6-not-taken from this "
                       f"file's own re-ride; the shadow caveat), g_tide_bands (14 rows incl. "
                       f"n_left_censored; the >206 caveat), g_collisions (5 books), "
                       f"g_collision_list_v6 ({len(fr['g_collision_list_v6'])} rows), g_arrivals, "
                       f"g_priority_windows ({len(fr['g_priority_windows'])} windows: outcome, "
                       f"entry, r/ATR, 4 scan counts, both net_r), g_rivals (placeholder, null "
                       f"fields), g_priority_vs_v6 ({len(fr['g_priority_vs_v6'])} keys), 6 dp"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-EDGE
def edge_cases() -> list[tuple]:
    """(detector, what, thunk, typed answer) — every cut AT its boundary."""
    nx = float(np.nextafter(RATR_CUT_TYPED, np.inf))
    ed = [10.0, 20.0, 30.0]
    return [
        ("EDGE-OLD", "old_refused(30, edges [10, 20, 30]): run == q75 is OLD",
         lambda: G.old_refused(30, ed), True),
        ("EDGE-OLD", "old_refused(29, edges [10, 20, 30])", lambda: G.old_refused(29, ed), False),
        ("EDGE-OLD", "old_refused(400, no edges)", lambda: G.old_refused(400, None), False),
        ("EDGE-ABS", "abs_refused(206)", lambda: G.abs_refused(206), False),
        ("EDGE-ABS", "abs_refused(207)", lambda: G.abs_refused(207), True),
        ("EDGE-WIN", "win_refused(15)", lambda: G.win_refused(15), False),
        ("EDGE-WIN", "win_refused(16)", lambda: G.win_refused(16), True),
        ("EDGE-LAG", "lag7_15_refused(6)", lambda: G.lag7_15_refused(6), False),
        ("EDGE-LAG", "lag7_15_refused(7)", lambda: G.lag7_15_refused(7), True),
        ("EDGE-LAG", "lag7_15_refused(15)", lambda: G.lag7_15_refused(15), True),
        ("EDGE-LAG", "lag7_15_refused(16)", lambda: G.lag7_15_refused(16), False),
        ("EDGE-RATR", "ratr_refused(2.2)", lambda: G.ratr_refused(2.2), False),
        ("EDGE-RATR", "ratr_refused(next float above 2.2)", lambda: G.ratr_refused(nx), True),
        ("EDGE-PASS", "ratr_ok(2.2, 2.2): the first trigger kept", lambda: G.ratr_ok(2.2, 2.2),
         True),
        ("EDGE-PASS", "ratr_ok(next above 2.2, 2.2)", lambda: G.ratr_ok(nx, 2.2), False),
        ("EDGE-SUB", "sub_admissible(2.2, 2.2)", lambda: G.sub_admissible(2.2, 2.2), True),
        ("EDGE-SUB", "sub_admissible(next above 2.2, 2.2)", lambda: G.sub_admissible(nx, 2.2),
         False),
        ("EDGE-FLAT", "is_flat(100, open until 100)", lambda: G.is_flat(100, 100), False),
        ("EDGE-FLAT", "is_flat(101, open until 100)", lambda: G.is_flat(101, 100), True),
        ("EDGE-ERA", "E.era_of(close 2024-06-30T20:00Z)",
         lambda: str(E.era_of(STRADDLE_OPEN_TYPED)), "tuning"),
        ("EDGE-ERA", "E.era_of(close 2024-07-01T00:00Z)",
         lambda: str(E.era_of(STRADDLE_CLOSE_TYPED)), "holdout"),
        ("EDGE-ERA", "G.era_of_entry(bar open 2024-06-30T20:00Z, the straddling bar)",
         lambda: G.era_of_entry(STRADDLE_OPEN_TYPED), "holdout"),
        ("EDGE-ERA", "G.era_of_entry(bar open 2024-06-30T16:00Z)",
         lambda: G.era_of_entry(STRADDLE_OPEN_TYPED - MS4H), "tuning"),
    ]


def straddle_findings() -> list[str]:
    """Two synthetic BTC campaigns (a v6 trade moved to the straddling bar and to the
    bar before it) through the module's facts, regbook frame and era-slice rows."""
    pool = module_R()["pool"]
    t0 = next(t for t in v6_book() if t.symbol == "BTCUSDT")
    i1, i0 = idx("BTCUSDT", STRADDLE_OPEN_TYPED), idx("BTCUSDT", STRADDLE_OPEN_TYPED - MS4H)
    ts1 = dataclasses.replace(t0, entry_ms=STRADDLE_OPEN_TYPED, entry_i=i1)
    ts0 = dataclasses.replace(t0, entry_ms=STRADDLE_OPEN_TYPED - MS4H, entry_i=i0)
    out = []
    f1, f0 = G.facts_of(ts1, pool), G.facts_of(ts0, pool)
    if (f1["era"], int(f1["entry_close_ms"])) != ("holdout", STRADDLE_CLOSE_TYPED):
        out.append(f"EDGE-ERA facts_of: the straddling bar is {f1['era']} at close "
                   f"{f1['entry_close_ms']} (typed holdout at {STRADDLE_CLOSE_TYPED})")
    if f0["era"] != "tuning":
        out.append(f"EDGE-ERA facts_of: the bar before the straddle is {f0['era']} (typed tuning)")
    rb = G.regbook_frame([ts1, ts0], pool)
    got = list(zip(rb["entry_close_ms"].astype(np.int64).tolist(), rb["era"]))
    want = [(STRADDLE_OPEN_TYPED, "tuning"), (STRADDLE_CLOSE_TYPED, "holdout")]
    if got != want:
        out.append(f"EDGE-ERA regbook_frame: (entry_close_ms, era) {got} != typed {want}")
    rows = G.era_slice_rows([("EDGE", "synthetic", [ts0, ts1])])
    gs = {r["era"]: int(r["n"]) for r in rows}
    if gs != {"tuning": 1, "holdout": 1, "full": 2}:
        out.append(f"EDGE-ERA era_slice_rows: n by era {gs} != typed tuning 1 / holdout 1 / "
                   f"full 2")
    return out


def claim_findings() -> list[str]:
    zp = {"n_position_open_v6": 0, "n_position_open_priority": 0, "n_scan_not_flat": 0}
    zg = pd.DataFrame({"rival_count_rejection_log": [0] * 5, "reride_admitted_not_in_v6": [0] * 5})
    out = []
    if CLAIM_PHRASE_TYPED not in G.flat_claim(zp, zg):
        out.append("EDGE-CLAIM: every count 0 but the 'never binds' sentence is absent")
    variants = [(f"{k} = 1", dict(zp, **{k: 1}), zg) for k in zp]
    for c_ in zg.columns:
        g2 = zg.copy()
        g2.loc[2, c_] = 1
        variants.append((f"one gate's {c_} = 1", zp, g2))
    for name, ps, gr in variants:
        if CLAIM_PHRASE_TYPED in G.flat_claim(ps, gr):
            out.append(f"EDGE-CLAIM: '{CLAIM_PHRASE_TYPED}' printed although {name}")
    return out


def hold_findings() -> tuple[list[str], dict]:
    """The one-position rule under a FORCED HOLD: every ride's exit bar + HOLD_TYPED
    (clipped at the corridor end), in the module (tierc11_ride.ride11 wrapped) and in
    this file's replay (own_replay hold=) — entries, exits, window outcomes and scan
    counts must agree and no asset may hold two campaigns; the hold must bind."""
    lo, hi = LO_TYPED, PIN - 1
    real = G.RD.ride11

    def held(*a, **k):
        leg = real(*a, **k)
        return dict(leg, exit_i=min(int(leg["exit_i"]) + HOLD_TYPED, int(a[8])))
    with mutated(G.RD, "ride11", held):
        mods = {"v6": G.replay_book(lo, hi), "priority": G.replay_book(lo, hi,
                                                                        priority_cut=G.RATR_CUT)}
    out, cnt = [], {}
    for name, cut in (("v6", None), ("priority", RATR_CUT_TYPED)):
        bk, lg = mods[name]
        own = {s: own_replay(s, cut, hold=HOLD_TYPED) for s in CLASSIC5_TYPED}
        oe = {(e["symbol"], e["entry_i"]): e for s in CLASSIC5_TYPED for e in own[s]["entries"]}
        me = {(t.symbol, int(t.entry_i)): t for t in bk}
        if set(me) != set(oe) or len(me) != len(bk):
            out.append(f"EDGE-HOLD {name}: {len(set(me) - set(oe))} module entries this file's "
                       f"held replay does not take, {len(set(oe) - set(me))} missing")
        for k in sorted(set(me) & set(oe)):
            t, e = me[k], oe[k]
            if int(t.exit_i) != e["exit_i"] or \
                    bool(getattr(t, "priority_substitute", False)) != e["sub"]:
                out.append(f"EDGE-HOLD {name} {k}: exit bar {t.exit_i} / substitute "
                           f"{getattr(t, 'priority_substitute', False)} != own {e['exit_i']} / "
                           f"{e['sub']}")
                break
        for s in CLASSIC5_TYPED:
            seq = sorted((t for t in bk if t.symbol == s), key=lambda t: int(t.entry_i))
            if any(int(b.entry_i) <= int(a.exit_i) for a, b in zip(seq, seq[1:])):
                out.append(f"EDGE-HOLD {name} {s}: an entry while the asset's campaign is open")
        ow = {(s, rec["w"]["ms"], rec["w"]["d"]): rec for s in CLASSIC5_TYPED
              for rec in own[s]["wins"]}
        mw = {(r["symbol"], int(r["arm_ms"]), int(r["direction"])): r for r in lg}
        if set(ow) != set(mw):
            out.append(f"EDGE-HOLD {name}: window keys differ ({len(set(mw) ^ set(ow))})")
        nbad = 0
        for k in sorted(set(ow) & set(mw)):
            rec, r = ow[k], mw[k]
            scan = [x[1] for x in rec["scan"]]
            want = (OUTCOME_NAME_TYPED[rec["outcome"]],
                    rec["entry"]["entry_i"] if rec["entry"] else -1,
                    len(scan), scan.count("not flat"))
            got = (r["outcome"], int(r["entry_i"]), int(r["n_scanned"]), int(r["n_scan_not_flat"]))
            if got != want:
                nbad += 1
                if nbad == 1:
                    out.append(f"EDGE-HOLD {name} {k[0]} arm {iso(k[1])}: (outcome, entry bar, "
                               f"scanned, not flat) {got} != own {want}")
        cnt[name] = {"entries": len(bk),
                     "position_open": sum(own[s]["n_position_open"] for s in CLASSIC5_TYPED),
                     "scan_not_flat": sum(x[1] == "not flat" for s in CLASSIC5_TYPED
                                          for rec in own[s]["wins"] for x in rec["scan"])}
    if cnt["v6"]["position_open"] == 0 or cnt["priority"]["scan_not_flat"] == 0:
        out.append(f"EDGE-HOLD: the forced hold does not bind (v6 position_open "
                   f"{cnt['v6']['position_open']}, priority not-flat skips "
                   f"{cnt['priority']['scan_not_flat']}) — the scenario proves nothing")
    return out, cnt


def edge_findings() -> tuple[list[str], dict]:
    out = []
    for det, what, th, want in edge_cases():
        got = th()
        if not _same(bool(got) if isinstance(want, bool) else got, want):
            out.append(f"{det}: {what} -> {got!r}, typed {want!r}")
    out += straddle_findings()
    out += claim_findings()
    hf, cnt = hold_findings()
    return out + hf, cnt


def edge_break():
    def under(name, fn, obj=None):
        def thunk():
            with mutated(obj or G, name, fn):
                return edge_findings()[0]
        return thunk
    return plants([
        ("OLD made strict (run > q75)", "EDGE-OLD",
         under("old_refused", lambda run, edges: edges is not None
               and int(run) > float(edges[2]))),
        ("the shadow at >= 206", "EDGE-ABS", under("abs_refused", lambda run: int(run) >= 206)),
        ("P-WIN-1 at lag > 16", "EDGE-WIN", under("win_refused", lambda lag: int(lag) > 16)),
        ("the shadow cut 7..16", "EDGE-LAG",
         under("lag7_15_refused", lambda lag: 7 <= int(lag) <= 16)),
        ("r/ATR refused at >= 2.2", "EDGE-RATR",
         under("ratr_refused", lambda r: float(r) >= 2.2)),
        ("era by the entry bar's OPEN", "EDGE-ERA",
         under("era_of_entry", lambda m: str(E.era_of(int(m))))),
        ("the 'never binds' sentence printed always", "EDGE-CLAIM",
         under("flat_claim", lambda ps, gr: G.FLAT_CLAIM)),
        ("the flat test removed (asset always flat)", "EDGE-HOLD",
         under("is_flat", lambda ti, open_until: True)),
    ])


def edge_real():
    bad, cnt = edge_findings()
    cases = edge_cases()
    say(f"  [EDGE] {len(cases)} typed boundary cases: "
        + " · ".join(f"{what} -> {want}" for _d, what, _t, want in cases))
    say(f"  [EDGE] forced hold (+{HOLD_TYPED} bars): {cnt}")
    return (not bad), (f"every cut at its boundary == typed ({len(cases)} cases: OLD at q75, "
                       f"206 / 207, lag 15 / 16, shadow 6 / 7 / 15 / 16, r/ATR 2.2 in the "
                       f"admission, the pass and the substitute test, flat at open_until, the era "
                       f"cut); a synthetic straddling entry bar is holdout (its predecessor "
                       f"tuning) in facts_of, regbook_frame and era_slice_rows; the one-position "
                       f"sentence 'never binds' under all-zero counts only (5 non-zero variants "
                       f"refused); under a forced hold of +{HOLD_TYPED} bars the module's v6 and "
                       f"priority replays == this file's held replay (entries, exit bars, window "
                       f"outcomes, scan counts), no overlap, and the hold binds (v6 "
                       f"position_open {cnt.get('v6', {}).get('position_open')}, priority "
                       f"not-flat skips {cnt.get('priority', {}).get('scan_not_flat')})"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-GRID
def declared() -> dict:
    """{table: (declared cells, cell builder)} — the commission, typed here."""
    bands = BANDS_TYPED
    return {
        "g_grid_partition": ([f"A{a}|W{w}|S{s}" for a in (0, 1) for w in (0, 1)
                              for s in (0, 1)], lambda d: d["cell"]),
        "g_grid_books": ([f"age:{a}|win:{w}|ratr:{s}" for a in ("off", "on")
                          for w in ("off", "on") for s in ("off", "on")], lambda d: d["cell"]),
        "g_age_crosstab": ([f"entry:{a}|arm:{b}" for a in bands for b in bands],
                           lambda d: d["cell"]),
        "g_lag_bands": (["0", "1-6", "7-15", ">=16"], lambda d: d["lag_band"]),
        "g_tide_bands": ([f"{TIDE_MEASURES_TYPED[0]}|{b}" for b in bands]
                         + [f"{TIDE_MEASURES_TYPED[1]}|{b}" for b in bands]
                         + [f"{TIDE_MEASURES_TYPED[2]}|{b}" for b in (">206", "<=206")]
                         + [f"{TIDE_MEASURES_TYPED[3]}|{b}" for b in (">206", "<=206")],
                         lambda d: d["measure"] + "|" + d["band"]),
        "g_era_slices": ([f"{r}|{b}|{e}" for r in ("P-AGE-1", "P-WIN-1")
                          for b in ("scored", "base") for e in ("tuning", "holdout", "full")],
                         lambda d: d["registration"] + "|" + d["book"] + "|" + d["era"]),
        "g_gate_rows": (list(GATE_ROW_OF.values()), lambda d: d["gate"],
                        ("n_refused", "n_gated", "sum_net_r_refused", "sum_net_r_gated")),
        "g_collisions": (list(COLLISION_BOOKS_TYPED), lambda d: d["book"],
                         ("n_campaigns", "n_collision_closes")),
        "g_tiere_books": ([f"{r}|{a}" for (r, a), v in ARMS_TYPED.items() if v[0] == "tierE"],
                          lambda d: d["registration"] + "|" + d["arm"]),
        "g_registered_books": ([f"{r}|{a}" for r in ("P-AGE-1", "P-WIN-1")
                                for a in ("scored", "base")],
                               lambda d: d["registration"] + "|" + d["arm"]),
    }


def grid_findings(frames: dict) -> list[str]:
    out = []
    for name, spec in declared().items():
        dec, cell = spec[0], spec[1]
        req = spec[2] if len(spec) > 2 else ("n", "sum_net_r")
        d = frames[name]
        ok, lines = TP.grid_whole(dec, d.assign(cell=cell(d)), "cell", require_cols=req,
                                  label=name)
        if not ok:
            out += [f"GRID-WHOLE {ln}" for ln in lines if ln.startswith("[BAD]")]
        if "n" in d.columns and "mean_net_r" in d.columns:
            z = d["n"].astype(int) == 0
            if (z & d["mean_net_r"].notna()).any() or \
                    ("nan_reason" in d.columns and (z & (d["nan_reason"].astype(str) == "")).any()):
                out.append(f"GRID-NAN {name}: an n = 0 cell carries a mean or no nan_reason")
            if (~z & d["mean_net_r"].isna()).any():
                out.append(f"GRID-NAN {name}: a NaN mean under n > 0")
    for name in STAGE_TABLES_TYPED:
        d = frames[name]
        if name not in UNCOLLARED_TYPED:
            for k, v in COLLAR_TYPED.items():
                if k not in d.columns or not (d[k].astype(str) == v).all():
                    out.append(f"GRID-COLLAR {name}: collar column {k} absent or not {v!r}")
        vc = [c for c in d.columns if c in VERDICT_COLUMNS or c.startswith("verdict")]
        if vc:
            out.append(f"GRID-VERDICT {name}: verdict column(s) {vc}")
        if name not in UNCOLLARED_TYPED:
            for c in d.columns:
                if d[c].dtype == object:
                    hits = [str(x) for x in d[c] if isinstance(x, str) and VERDICT_RX.search(x)]
                    if hits:
                        out.append(f"GRID-VERDICT {name}: verdict word in column {c}: "
                                   f"{hits[0][:80]!r}")
    return out


def recompute_findings(frames: dict) -> list[str]:
    """Every grid cell's n / ΣR / mean from THIS file's flags and the v6 book."""
    own = own_facts()
    net = {(t.symbol, int(t.entry_ms)): float(t.net_r) for t in v6_book()}
    out = []

    def cmp(name, cellname, keys, row):
        n, s = len(keys), math.fsum(net[k] for k in keys)
        want = {"n": n, "sum_net_r": _f6(s), "mean_net_r": (_f6(s / n) if n else float("nan"))}
        for c_, v in want.items():
            if not _same(float(row[c_]), float(v)):
                out.append(f"GRID-RECOMPUTE {name} {cellname}: {c_} {row[c_]} != own {v}")

    p = frames["g_grid_partition"].set_index("cell")
    for a in (0, 1):
        for w in (0, 1):
            for s in (0, 1):
                ks = [k for k, f in own.items() if (f["AGE"], f["WIN"], f["RATR"]) ==
                      (bool(a), bool(w), bool(s))]
                cell = f"A{a}|W{w}|S{s}"
                if cell in p.index:
                    cmp("g_grid_partition", cell, ks, p.loc[cell])
    if int(frames["g_grid_partition"]["n"].sum()) != V6_N_TYPED:
        out.append("GRID-RECOMPUTE g_grid_partition: the partition does not sum to 200")
    gb = frames["g_grid_books"].set_index("cell")
    for a in ("off", "on"):
        for w in ("off", "on"):
            for s in ("off", "on"):
                ks = [k for k, f in own.items()
                      if not ((a == "on" and f["AGE"]) or (w == "on" and f["WIN"])
                              or (s == "on" and f["RATR"]))]
                cell = f"age:{a}|win:{w}|ratr:{s}"
                if cell in gb.index:
                    cmp("g_grid_books", cell, ks, gb.loc[cell])
    ct = frames["g_age_crosstab"].set_index("cell")
    for be in BANDS_TYPED:
        for ba in BANDS_TYPED:
            ks = [k for k, f in own.items() if f["band"] == be and f["arm_band"] == ba]
            cell = f"entry:{be}|arm:{ba}"
            if cell in ct.index:
                cmp("g_age_crosstab", cell, ks, ct.loc[cell])
    lb = frames["g_lag_bands"].set_index("lag_band")
    for name, a, b in (("0", 0, 0), ("1-6", 1, 6), ("7-15", 7, 15), (">=16", 16, 10 ** 9)):
        ks = [k for k, f in own.items() if a <= f["lag"] <= b]
        if name in lb.index:
            cmp("g_lag_bands", name, ks, lb.loc[name])
    es = frames["g_era_slices"]
    for r in es.itertuples(index=False):
        rr = r._asdict()
        tset = {"P-AGE-1": "AGE", "P-WIN-1": "WIN"}[rr["registration"]]
        ks = [k for k, f in own.items()
              if (rr["book"] == "base" or not f[tset])
              and (rr["era"] == "full" or f["era"] == rr["era"])]
        cmp("g_era_slices", f"{rr['registration']}|{rr['book']}|{rr['era']}", ks, rr)
    return out


def _frames(root: Path | None = None) -> dict:
    return {n: stage_df(n, root) for n in STAGE_TABLES_TYPED}


def grid_break():
    fr = _frames()

    def with_(name, d):
        x = dict(fr)
        x[name] = d
        return x

    p = fr["g_grid_partition"]
    return plants([
        ("a cell dropped from the 2x2x2 partition", "GRID-WHOLE",
         lambda: grid_findings(with_("g_grid_partition", p.iloc[1:]))),
        ("an undeclared cell in the gate books", "GRID-WHOLE",
         lambda: grid_findings(with_("g_grid_books", pd.concat(
             [fr["g_grid_books"], fr["g_grid_books"].iloc[:1].assign(
                 cell="age:on|win:on|ratr:maybe")], ignore_index=True)))),
        ("a duplicated crosstab cell", "GRID-WHOLE",
         lambda: grid_findings(with_("g_age_crosstab", pd.concat(
             [fr["g_age_crosstab"], fr["g_age_crosstab"].iloc[:1]], ignore_index=True)))),
        ("the collar removed from g_gate_rows", "GRID-COLLAR",
         lambda: grid_findings(with_("g_gate_rows", fr["g_gate_rows"].drop(columns=["tier"])))),
        ("a verdict column on g_tiere_books", "GRID-VERDICT",
         lambda: grid_findings(with_("g_tiere_books",
                                     fr["g_tiere_books"].assign(verdict="x")))),
        ("a verdict word in g_gate_rows", "GRID-VERDICT",
         lambda: grid_findings(with_("g_gate_rows", fr["g_gate_rows"].assign(
             forfeit_note="SUPPORTED")))),
        ("a NaN mean under n > 0", "GRID-NAN",
         lambda: grid_findings(with_("g_lag_bands", fr["g_lag_bands"].assign(
             mean_net_r=[float("nan")] + list(fr["g_lag_bands"]["mean_net_r"].iloc[1:]))))),
        ("one partition cell's n + 1", "GRID-RECOMPUTE",
         lambda: recompute_findings(with_("g_grid_partition", p.assign(
             n=[int(p["n"].iloc[0]) + 1] + list(p["n"].iloc[1:]))))),
    ])


def grid_real():
    fr = _frames()
    bad = grid_findings(fr) + recompute_findings(fr)
    sizes = {n: len(fr[n]) for n in ("g_grid_partition", "g_grid_books", "g_age_crosstab",
                                     "g_lag_bands", "g_tide_bands", "g_era_slices")}
    return (not bad), (f"every declared grid WHOLE ({sizes}; plus g_gate_rows 5, g_collisions 5, "
                       f"g_tiere_books 10, g_registered_books 4); the collar on all "
                       f"{len(STAGE_TABLES_TYPED) - len(UNCOLLARED_TYPED)} non-registered "
                       f"tables, no verdict column or word; n = 0 cells NaN with a reason; the "
                       f"partition sums to 200; every partition / gate-book / crosstab / lag / "
                       f"era cell's n, ΣR and mean == this file's recomputation at 6 dp"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-KEY
def canon_sha(df: pd.DataFrame) -> str:
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(REQUIRED_TYPED)]
    for row in d[list(REQUIRED_TYPED)].itertuples(index=False):
        f = []
        for c_, v in zip(REQUIRED_TYPED, row):
            f.append(repr(float(v)) if c_ in FLOAT_REQ else
                     str(int(v)) if c_ in ("entry_ms", "entry_close_ms", "exit_close_ms",
                                           "direction") else str(v))
        lines.append(",".join(f))
    return sha_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def regbook_findings(root: Path) -> list[str]:
    out = []
    for reg in ("P-AGE-1", "P-WIN-1"):
        want_arms = sorted(a for (r, a) in ARMS_TYPED if r == reg)
        stp = root / reg / "STATUS.json"
        if not stp.exists():
            out.append(f"KEY-STATUS {reg}: STATUS.json absent")
        else:
            st = json.loads(stp.read_text(encoding="utf-8"))
            if st.get("registration") != reg or st.get("status") != "BUILT" or \
                    sorted(st.get("arms", [])) != want_arms:
                out.append(f"KEY-STATUS {reg}: {st.get('status')} arms {sorted(st.get('arms', []))} "
                           f"!= typed {want_arms}")
        have = sorted(p.stem for p in (root / reg).glob("*.parquet"))
        if have != want_arms:
            out.append(f"KEY-FILES {reg}: parquets {have} != typed {want_arms}")
    for (reg, arm), (kind, ruler, scope) in ARMS_TYPED.items():
        p = root / reg / f"{arm}.parquet"
        if not p.exists():
            out.append(f"KEY-FILES {reg}/{arm}: absent")
            continue
        df = pd.read_parquet(str(p))
        lab = f"{reg}/{arm}"
        miss = [c for c in REQUIRED_TYPED if c not in df.columns]
        if miss:
            out.append(f"KEY-NULL {lab}: required column(s) absent {miss}")
            continue
        for c_, t in DTYPES_TYPED.items():
            if str(df[c_].dtype) != t:
                out.append(f"KEY-DTYPE {lab}: {c_} is {df[c_].dtype}, typed {t}")
        nul = [c_ for c_ in REQUIRED_TYPED if df[c_].isna().any()]
        if nul:
            out.append(f"KEY-NULL {lab}: null(s) in {nul}")
        for k in (["symbol", "entry_ms"], ["symbol", "entry_close_ms"]):
            if df.duplicated(subset=k).any():
                out.append(f"KEY-DUP {lab}: duplicated {k}")
        era = ["tuning" if int(x) <= ERA_CUT_TYPED else "holdout" for x in df["entry_close_ms"]]
        if list(df["era"].astype(str)) != era:
            out.append(f"KEY-ERA {lab}: era is not by the typed cut on entry_close_ms")
        if scope != "full" and set(df["era"]) - {scope}:
            out.append(f"KEY-ERA {lab}: rows outside its era_scope {scope}")
        hc = [float(n) - float(f) * SLIP_TYPED[s] / TAKER_TYPED
              for s, n, f in zip(df["symbol"], df["net_r"], df["fee_r"])]
        if any(float(x) != y for x, y in zip(df["haircut_net_r"], hc)):
            out.append(f"KEY-HAIRCUT {lab}: haircut_net_r != net_r - fee_r x slip / 5.0")
        if any(float(n) != float(g) - float(f) - float(u) for n, g, f, u in
               zip(df["net_r"], df["gross_r"], df["fee_r"], df["funding_r"])):
            out.append(f"KEY-NET {lab}: net_r != gross_r - fee_r - funding_r")
        if (df["entry_close_ms"].astype(np.int64) != df["entry_ms"].astype(np.int64) + MS4H).any():
            out.append(f"KEY-CLOSE {lab}: entry_close_ms != entry_ms + 4h")
        if (df["exit_close_ms"].astype(np.int64) < df["entry_close_ms"].astype(np.int64)).any():
            out.append(f"KEY-CLOSE {lab}: an exit before its entry")
        sp = root / reg / f"{arm}.json"
        if not sp.exists():
            out.append(f"KEY-SIDECAR {lab}: sidecar absent")
            continue
        sd = json.loads(sp.read_text(encoding="utf-8"))
        want_keys = sorted(SIDECAR_KEYS_TYPED + (tuple(COLLAR_TYPED) if kind == "tierE" else ()))
        if sorted(sd) != want_keys:
            out.append(f"KEY-SIDECAR {lab}: keys {sorted(sd)} != typed {want_keys}")
        exp = {"registration": reg, "arm": arm, "kind": kind, "ruler": ruler,
               "era_scope": scope, "panel": list(CLASSIC5_TYPED), "n": len(df),
               "sum_net_r": math.fsum(float(x) for x in df["net_r"]),
               "source_script": SOURCE_TYPED, "as_of": "2026-09-25T00:00:00Z", "seed": SEED}
        if kind == "tierE":
            exp.update(COLLAR_TYPED)
            for k, v in COLLAR_TYPED.items():
                if k not in df.columns or not (df[k].astype(str) == v).all():
                    out.append(f"KEY-COLLAR {lab}: collar column {k} absent or not {v!r}")
        for k, v in exp.items():
            if not _same(sd.get(k), v):
                out.append(f"KEY-SIDECAR {lab}: {k} {sd.get(k)!r} != {v!r}")
        if sd.get("book_sha256") != canon_sha(df):
            out.append(f"KEY-SHA {lab}: book_sha256 {str(sd.get('book_sha256'))[:16]}… != this "
                       f"file's canonical CSV {canon_sha(df)[:16]}…")
    return out


def stage_key_findings(root: Path) -> list[str]:
    out = []
    man = json.loads((root / G.MANIFEST).read_text(encoding="utf-8"))
    if man.get("keys") != KEYS_TYPED:
        diff = sorted(k for k in set(man.get("keys", {})) | set(KEYS_TYPED)
                      if man.get("keys", {}).get(k) != KEYS_TYPED.get(k))
        out.append(f"KEY-DECLARED: the manifest's declared keys differ from the typed keys on "
                   f"{diff} (e.g. {diff[0]}: {man.get('keys', {}).get(diff[0])} vs typed "
                   f"{KEYS_TYPED.get(diff[0])})")
    ok, lines = TP.check_keys(root, {**man, "keys": KEYS_TYPED})
    if not ok:
        out += [f"KEY-TABLE {ln}" for ln in lines if ln.startswith("[BAD]")]
    stems = sorted(p.stem for p in root.glob("*.parquet"))
    if stems != sorted(STAGE_TABLES_TYPED):
        out.append(f"KEY-TABLE file set {stems} != typed")
    for s in stems:
        d = pd.read_parquet(str(root / f"{s}.parquet"))
        if man["sha"].get(s) != TB._content_sha(d):
            out.append(f"KEY-TABLE {s}: manifest content sha is not the table's")
        k = KEYS_TYPED.get(s, [])
        if k and d[k].isna().any().any():
            out.append(f"KEY-TABLE {s}: a null in the key {k}")
    return out


def manifest_findings(man: dict, regroot: Path) -> list[str]:
    """The manifest's L-0.1 record (the latest close at fetch time, from AS_OF_PIN.json read
    HERE) and its regbook file shas (sha256 of the files as they lie)."""
    out = []
    pr = json.loads(AS_OF_PIN_JSON.read_text(encoding="utf-8"))
    mp = man.get("as_of_pin_record", {})
    if mp.get("latest_closed_4h_at_pin_run") != pr["latest_closed_4h_at_pin_run"] or \
            int(pr["as_of_last_closed_4h_close_ms"]) != PIN:
        out.append(f"KEY-ASOF: the manifest's latest close at fetch time "
                   f"{mp.get('latest_closed_4h_at_pin_run')!r} != AS_OF_PIN.json "
                   f"{pr['latest_closed_4h_at_pin_run']!r}")
    for (reg, arm) in ARMS_TYPED:
        e = man.get("regbooks", {}).get(f"{reg}/{arm}", {})
        for fld, ext in (("parquet_file_sha256", "parquet"), ("sidecar_file_sha256", "json")):
            p = regroot / reg / f"{arm}.{ext}"
            if e.get(fld) != sha_bytes(p.read_bytes()):
                out.append(f"KEY-FILESHA {reg}/{arm}: manifest {fld} "
                           f"{str(e.get(fld))[:16]}… != the file's {sha_bytes(p.read_bytes())[:16]}…")
    return out


def md_tables(md: str) -> list[tuple[str, list[str]]]:
    """(the heading above it, header columns) of every markdown table in md."""
    lines, heading, out = md.split("\n"), "", []
    for i, ln in enumerate(lines):
        if ln.startswith("#"):
            heading = ln.strip()
        if ln.startswith("| ") and i + 1 < len(lines) and lines[i + 1].startswith("|---"):
            out.append((heading, [c.strip() for c in ln.strip().strip("|").split("|")]))
    return out


def report_form_findings(md: str) -> list[str]:
    """L-0.1: the header prints the latest close at fetch time beside the pin; L-1.4: every
    table printed carries the collar, bar the registered books."""
    out = []
    pr = json.loads(AS_OF_PIN_JSON.read_text(encoding="utf-8"))
    hdr = [ln for ln in md.split("\n") if ln.startswith(AS_OF_LINE)]
    if len(hdr) != 1 or FETCH_PHRASE_TYPED + pr["latest_closed_4h_at_pin_run"] + " " not in hdr[0]:
        out.append(f"REPORT-ASOF: STAGE_G.md's pin line does not print the latest close at "
                   f"fetch time ({pr['latest_closed_4h_at_pin_run']}) beside the pin [L-0.1]")
    tabs = md_tables(md)
    if len(tabs) != MD_TABLES_TYPED:
        out.append(f"REPORT-TABLES: STAGE_G.md prints {len(tabs)} tables, typed {MD_TABLES_TYPED}")
    exempt = [h for h, _c in tabs if h == REGISTERED_MD_HEADING]
    if len(exempt) != 1:
        out.append(f"REPORT-COLLAR: {len(exempt)} registered-book tables (typed 1)")
    for h, cols in tabs:
        if h == REGISTERED_MD_HEADING:
            continue
        miss = [k for k in COLLAR_TYPED if k not in cols]
        if miss:
            out.append(f"REPORT-COLLAR: the table under '{h}' prints without {miss} [L-1.4]")
    return out


def own_counts() -> dict:
    """The counts the one-position sentence rests on, from THIS file's replays."""
    v6k = {(t.symbol, int(t.entry_ms)) for t in v6_book()}
    return {"position_open_v6": sum(own_replay(s, None)["n_position_open"]
                                    for s in CLASSIC5_TYPED),
            "position_open_priority": sum(own_replay(s, RATR_CUT_TYPED)["n_position_open"]
                                          for s in CLASSIC5_TYPED),
            "scan_not_flat": sum(x[1] == "not flat" for s in CLASSIC5_TYPED
                                 for rec in own_replay(s, RATR_CUT_TYPED)["wins"]
                                 for x in rec["scan"]),
            "rivals": sum(own_position_open_rivals().values()),
            "reride_not_in_v6": sum(len({(e["symbol"], e["entry_ms"]) for e in own_reride(g)}
                                        - v6k) for g in GATE_ROW_OF)}


def report_claim_findings(md: str, counts: dict) -> list[str]:
    has = CLAIM_PHRASE_TYPED in md
    nz = {k: v for k, v in counts.items() if v}
    if has and nz:
        return [f"REPORT-CLAIM: STAGE_G.md says '{CLAIM_PHRASE_TYPED}' but this file counts {nz}"]
    if not has and not nz:
        return [f"REPORT-CLAIM: every own count is 0 but STAGE_G.md drops '{CLAIM_PHRASE_TYPED}'"]
    return []


def report_findings(md: str) -> list[str]:
    regs = json.loads((ROOT / "research_outputs/tierc11/registrations/REGISTRATIONS.json")
                      .read_text(encoding="utf-8"))
    out = []
    for r in regs["registrations"]:
        if r["registration"] not in ("P-AGE-1", "P-WIN-1"):
            continue
        for lab, txt in (("text_of_record", r["text_of_record"]),
                         ("pre_seen", r["operative_spec"].get("pre_seen")),
                         ("selection_hazard", r["operative_spec"].get("selection_hazard"))):
            if txt and txt not in md:
                out.append(f"KEY-REPORT: STAGE_G.md does not print {r['registration']} {lab} "
                           f"verbatim")
    return out


def key_break():
    def tmp_regbooks(mut):
        d = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            shutil.copytree(REGB / "P-AGE-1", d / "P-AGE-1")
            shutil.copytree(REGB / "P-WIN-1", d / "P-WIN-1")
            mut(d)
            return regbook_findings(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def edit_parquet(reg, arm, fn):
        def m(d):
            p = d / reg / f"{arm}.parquet"
            df = fn(pd.read_parquet(str(p)))
            df.to_parquet(str(p), index=False)
        return m

    def edit_json(reg, arm, fn):
        def m(d):
            p = d / reg / f"{arm}.json"
            p.write_text(json.dumps(fn(json.loads(p.read_text(encoding="utf-8")))),
                         encoding="utf-8")
        return m

    def dup_table():
        d = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            for p in OUT.glob("*.parquet"):
                shutil.copy(p, d / p.name)
            shutil.copy(OUT / G.MANIFEST, d / G.MANIFEST)
            x = pd.read_parquet(str(d / "g_lag_bands.parquet"))
            pd.concat([x, x.iloc[:1]], ignore_index=True).to_parquet(
                str(d / "g_lag_bands.parquet"), index=False)
            return stage_key_findings(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def superset_key():
        d = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            for p in OUT.glob("*.parquet"):
                shutil.copy(p, d / p.name)
            man = json.loads((OUT / G.MANIFEST).read_text(encoding="utf-8"))
            man["keys"]["g_lag_bands"] = ["lag_band", "n"]
            (d / G.MANIFEST).write_text(json.dumps(man), encoding="utf-8")
            return stage_key_findings(d)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def bent_filesha():
        man = json.loads((OUT / G.MANIFEST).read_text(encoding="utf-8"))
        man["regbooks"]["P-WIN-1/scored"]["parquet_file_sha256"] = "0" * 64
        return manifest_findings(man, REGB)

    md = (OUT / G.REPORT).read_text(encoding="utf-8")

    def no_fetch_line():
        return report_form_findings(md.replace(FETCH_PHRASE_TYPED + "2026-09-25T00:00:00Z",
                                               FETCH_PHRASE_TYPED + "n/a"))

    def uncollared_table():
        # the first collared table after the registered books: its collar headers renamed
        lines = md.split("\n")
        j = next(i for i, ln in enumerate(lines) if ln.startswith("| ") and i + 1 < len(lines)
                 and lines[i + 1].startswith("|---") and "| tier |" in ln)
        lines[j] = (lines[j].replace("| tier |", "| c1 |")
                    .replace("| selection_not_a_result |", "| c2 |").replace("| gates |", "| c3 |"))
        return report_form_findings("\n".join(lines))

    def claim_nonzero():
        return report_claim_findings(md, dict(own_counts(), position_open_v6=1))

    def flip_era(df):
        df = df.copy()
        df.loc[df.index[0], "era"] = "holdout" if df["era"].iloc[0] == "tuning" else "tuning"
        return df

    def move_hc(df):
        df = df.copy()
        df.loc[df.index[0], "haircut_net_r"] = float(df["haircut_net_r"].iloc[0]) + 1e-9
        return df

    return plants([
        ("a duplicated row in P-AGE-1/scored", "KEY-DUP", lambda: tmp_regbooks(edit_parquet(
            "P-AGE-1", "scored", lambda df: pd.concat([df, df.iloc[:1]], ignore_index=True)))),
        ("a nulled net_r in P-WIN-1/base", "KEY-NULL", lambda: tmp_regbooks(edit_parquet(
            "P-WIN-1", "base", lambda df: df.assign(net_r=[float("nan")] + list(df["net_r"][1:]))))),
        ("direction written as int64", "KEY-DTYPE", lambda: tmp_regbooks(edit_parquet(
            "P-WIN-1", "tierE__ratr_priority",
            lambda df: df.assign(direction=df["direction"].astype("int64"))))),
        ("a sidecar's n + 1", "KEY-SIDECAR", lambda: tmp_regbooks(edit_json(
            "P-AGE-1", "tierE__tuning", lambda s: dict(s, n=int(s["n"]) + 1)))),
        ("a bent book_sha256", "KEY-SHA", lambda: tmp_regbooks(edit_json(
            "P-WIN-1", "scored", lambda s: dict(s, book_sha256="0" * 64)))),
        ("STATUS.json missing an arm", "KEY-STATUS", lambda: tmp_regbooks(edit_json(
            "P-AGE-1", "STATUS", lambda s: dict(s, arms=s["arms"][1:])))),
        ("a haircut moved 1e-9", "KEY-HAIRCUT", lambda: tmp_regbooks(edit_parquet(
            "P-AGE-1", "base", move_hc))),
        ("an era flipped", "KEY-ERA", lambda: tmp_regbooks(edit_parquet(
            "P-WIN-1", "tierE__refused_cohort", flip_era))),
        ("the collar dropped from a Tier-E arm's parquet", "KEY-COLLAR",
         lambda: tmp_regbooks(edit_parquet("P-AGE-1", "tierE__shadow_abs206",
                                           lambda df: df.drop(columns=["gates"])))),
        ("TP.check_keys on a temp stage root holding a duplicated row", "unique keys",
         dup_table),
        ("(copy) the manifest's g_lag_bands key made a superset", "KEY-DECLARED", superset_key),
        ("(copy) a manifest regbook file sha bent", "KEY-FILESHA", bent_filesha),
        ("(copy) STAGE_G.md without the latest close at fetch time", "REPORT-ASOF",
         no_fetch_line),
        ("(copy) STAGE_G.md with one table's collar headers renamed",
         "REPORT-COLLAR", uncollared_table),
        ("the 'never binds' sentence under a non-zero own count", "REPORT-CLAIM",
         claim_nonzero),
    ])


def key_real():
    bad = regbook_findings(REGB) + stage_key_findings(OUT)
    md = (OUT / G.REPORT).read_text(encoding="utf-8")
    man = json.loads((OUT / G.MANIFEST).read_text(encoding="utf-8"))
    bad += report_findings(md)
    bad += manifest_findings(man, REGB) + report_form_findings(md)
    cnt = own_counts()
    bad += report_claim_findings(md, cnt)
    n = {f"{r}/{a}": len(reg_df(r, a)) for (r, a) in ARMS_TYPED}
    return (not bad), (f"{len(ARMS_TYPED)} regbook arms (+2 STATUS.json): the 16 required "
                       f"columns at the typed dtypes, no null, unique (symbol, entry_ms) and "
                       f"(symbol, entry_close_ms), era by the typed cut, haircut = net_r - "
                       f"fee_r x slip / 5.0 on the typed tiers, net = gross - fee - funding, "
                       f"entry_close = entry + 4h; every Tier-E parquet carries the collar; "
                       f"every sidecar's keys / kind / ruler / scope / "
                       f"panel / n / fsum ΣR / collar == typed and book_sha256 == this file's "
                       f"canonical CSV; rows {n}; the manifest's keys == the {len(KEYS_TYPED)} "
                       f"typed keys and TP.check_keys(stage_g) under them GREEN, manifest content "
                       f"shas == the tables, {len(STAGE_TABLES_TYPED)} typed tables, every "
                       f"regbook file sha == the file; the latest close at fetch time "
                       f"(AS_OF_PIN.json) beside the pin in the manifest and STAGE_G.md; all "
                       f"{MD_TABLES_TYPED} tables of STAGE_G.md collared bar the registered books; "
                       f"the one-position sentence matches this file's counts {cnt}; STAGE_G.md "
                       f"prints both texts of record, the pre_seen and the selection_hazard "
                       f"verbatim"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def files_typed() -> list[str]:
    out = [f"{G.STAGE_DIR}/{G.MANIFEST}", f"{G.STAGE_DIR}/{G.REPORT}"]
    out += [f"{G.STAGE_DIR}/{t}.parquet" for t in STAGE_TABLES_TYPED]
    for reg in ("P-AGE-1", "P-WIN-1"):
        out.append(f"{G.REGBOOK_DIR}/{reg}/STATUS.json")
        for (r, a) in ARMS_TYPED:
            if r == reg:
                out += [f"{G.REGBOOK_DIR}/{reg}/{a}.parquet", f"{G.REGBOOK_DIR}/{reg}/{a}.json"]
    return sorted(out)


def _files(root: Path) -> dict:
    """{rel path: Path} of the Stage G outputs under an output root."""
    out = {}
    sd = root / G.STAGE_DIR
    if sd.exists():
        for p in sorted(sd.iterdir()):
            if p.is_file() and p.name != TRANSCRIPT and not p.name.startswith("FIXTURES_"):
                out[f"{G.STAGE_DIR}/{p.name}"] = p
    for reg in ("P-AGE-1", "P-WIN-1"):
        rd = root / G.REGBOOK_DIR / reg
        if rd.exists():
            for p in sorted(rd.iterdir()):
                if p.is_file():
                    out[f"{G.REGBOOK_DIR}/{reg}/{p.name}"] = p
    return out


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    """(exit, {rel: Path}) x 2 vs the canonical files -> findings."""
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical", canon)):
        if sorted(x) != files_typed():
            out.append(f"{lab}: file set differs from the typed {len(files_typed())} files "
                       f"({sorted(set(x) ^ set(files_typed()))[:4]})")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            bx, by = x[name].read_bytes(), y[name].read_bytes()
            if bx != by:
                k = next((i for i in range(min(len(bx), len(by))) if bx[i] != by[i]),
                         min(len(bx), len(by)))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = TB._content_sha(pd.read_parquet(str(x[name])))
                cb = TB._content_sha(pd.read_parquet(str(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    return RUN_ROOT / G.DET_NAME


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_g.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_g as G\n"
                f"d = Path({str(d)!r})\nG.build(d)\n"
                f"p = d / G.STAGE_DIR / G.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(G.E.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT),
                       timeout=3600)
    if r.returncode != 0:
        clock(f"det build seed {seed} stderr tail: {r.stderr[-600:]}")
    return r.returncode, (_files(d) if d.exists() else {})


def det_break():
    canon = _files(G.OUT_ROOT)
    tmp = Path(tempfile.mkdtemp(prefix="f-det-"))
    try:
        bent = dict(canon)
        md = bytearray(canon[f"{G.STAGE_DIR}/{G.REPORT}"].read_bytes())
        md[len(md) // 2] ^= 0x01
        (tmp / "STAGE_G.md").write_bytes(bytes(md))
        bent[f"{G.STAGE_DIR}/{G.REPORT}"] = tmp / "STAGE_G.md"

        def float_moved():
            name = f"{G.REGBOOK_DIR}/P-AGE-1/scored.parquet"
            d = pd.read_parquet(str(canon[name]))
            d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
            p = tmp / "scored.parquet"
            d.to_parquet(str(p), index=False)
            c2 = dict(canon)
            c2[name] = p
            return det_findings((0, c2), (0, c2), canon)

        def hashorder():
            o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
            a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
            return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

        return plants([
            ("one byte bent in a copy of STAGE_G.md", "STAGE_G.md bytes differ",
             lambda: det_findings((0, canon), (0, bent), canon)),
            ("one net_r moved 1e-6 in a parquet copy", "scored.parquet content sha",
             float_moved),
            ("a hash-order-dependent line (set iteration) under the two seeds",
             f"seed 1 vs seed {SEED}: {G.STAGE_DIR}/{G.REPORT} bytes differ", hashorder),
        ])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def det_real():
    canon = _files(G.OUT_ROOT)
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    man = json.loads(canon[f"{G.STAGE_DIR}/{G.MANIFEST}"].read_text(encoding="utf-8"))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == the typed {len(files_typed())} files in "
                       f"both builds and in the record; every file byte-identical seed 1 == seed "
                       f"{SEED} == canonical, every parquet content sha equal: {not bad}; "
                       f"regbook shas P-AGE-1/scored "
                       f"{man['regbooks']['P-AGE-1/scored']['book_sha256'][:16]}… P-WIN-1/scored "
                       f"{man['regbooks']['P-WIN-1/scored']['book_sha256'][:16]}…"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ══════════════════════════════════════════════════════════ F-HARVEST-INSTANTS
def own_harvest_close(sym: str, d: int, entry_close_ms: int, exit_close_ms: int,
                      reason: str) -> int | None:
    """THIS FILE'S hand harvest law [v6's band harvest] on its own 4h read: the CLOSE
    of the first bar after the entry whose close slot fires the harvest, or None."""
    X = own4(sym)
    o, h, l, c, e89, e316 = X["o"], X["h"], X["l"], X["c"], X["e89"], X["e316"]

    def edge(j: int) -> float:
        return max(e89[j], e316[j]) if d == 1 else min(e89[j], e316[j])

    ei = int(np.searchsorted(o, int(entry_close_ms), "left")) - 1
    xi = int(np.searchsorted(o, int(exit_close_ms), "left")) - 1
    if int(o[ei]) + MS4H != int(entry_close_ms):
        raise RuntimeError(f"{sym} {iso(int(entry_close_ms))}: not a 4h-close entry")
    last = xi if reason == "corridor_end" else xi - 1
    armed = False
    for j in range(ei + 1, last + 1):
        if not armed and ((c[j - 1] > edge(j - 1)) if d == 1 else (c[j - 1] < edge(j - 1))):
            armed = True
        if armed and ((l[j] <= edge(j)) if d == 1 else (h[j] >= edge(j))):
            return int(o[j]) + MS4H
    return None


def harvest_instant_findings(tag: str, df: pd.DataFrame, v6hc: dict) -> tuple[list[str], dict]:
    out = []
    t = {"rows": len(df), "harvested": 0, "stamped": 0, "v6_keys": 0, "substitutes": 0,
         "substitutes_harvested": 0}
    if "harvest_close_ms" not in df.columns:
        return [f"INSTANT-HARVEST: {tag} carries no harvest_close_ms column"], t
    if str(df["harvest_close_ms"].dtype) != "Int64":
        out.append(f"INSTANT-HARVEST: {tag}.harvest_close_ms dtype "
                   f"{df['harvest_close_ms'].dtype} != Int64")
    for r in df.itertuples(index=False):
        got = None if pd.isna(r.harvest_close_ms) else int(r.harvest_close_ms)
        want = own_harvest_close(str(r.symbol), int(r.direction), int(r.entry_close_ms),
                                 int(r.exit_close_ms), str(r.exit_reason))
        k = (str(r.symbol), int(r.entry_ms))
        w = f"{tag} {r.symbol} {iso(int(r.entry_close_ms))}"
        t["harvested"] += int(bool(r.harvested))
        t["stamped"] += int(got is not None)
        if (got is not None) != bool(r.harvested):
            out.append(f"INSTANT-HARVEST: {w}: harvested {bool(r.harvested)} but "
                       f"harvest_close_ms {got}")
        if got != want:
            out.append(f"INSTANT-HARVEST: {w}: harvest_close_ms {iso(got) if got else None} "
                       f"!= the hand law's {iso(want) if want else None}")
        if k in v6hc:
            t["v6_keys"] += 1
            if v6hc[k] != got:
                out.append(f"INSTANT-HARVEST: {w}: harvest_close_ms {got} != books/"
                           f"v6_campaigns' {v6hc[k]}")
        else:
            t["substitutes"] += 1
            t["substitutes_harvested"] += int(bool(r.harvested))
    return out, t


def _v6_harvests() -> dict:
    v = pd.read_parquet(str(ROOT / "research_outputs" / "tierc11" / "books"
                            / "v6_campaigns.parquet"))
    return {(str(a), int(b)): (None if pd.isna(c) else int(c))
            for a, b, c in zip(v["symbol"], v["entry_ms"], v["harvest_close_ms"])}


def hinst_break():
    v6hc = _v6_harvests()
    pr = reg_df("P-WIN-1", "tierE__ratr_priority")
    sub_h = pr.index[pr["priority_substitute"].astype(bool) & pr["harvested"].astype(bool)]
    hv = pr.index[pr["harvested"].astype(bool)]

    def late():
        d = pr.copy()
        d.loc[hv[0], "harvest_close_ms"] = int(d.loc[hv[0], "harvest_close_ms"]) + MS4H
        return harvest_instant_findings("P-WIN-1/tierE__ratr_priority (copy)", d, v6hc)[0]

    def dropped_sub():
        d = pr.copy()
        d.loc[sub_h[0], "harvest_close_ms"] = pd.NA
        return harvest_instant_findings("P-WIN-1/tierE__ratr_priority (copy)", d, v6hc)[0]

    def open_stamped():
        orig = G.harvest_close_of

        def at_open(t):
            x = orig(t)
            return None if x is None else x - MS4H
        R = module_R()
        with mutated(G, "harvest_close_of", at_open):
            f = G.regbook_frame(R["priority"], R["pool"])
        return harvest_instant_findings("P-WIN-1/tierE__ratr_priority (rebuilt, mutant)", f,
                                        v6hc)[0]

    return plants([
        ("one harvest one 4h bar late (a copy of the priority arm)", "INSTANT-HARVEST", late),
        ("one SUBSTITUTE's harvest instant dropped — nulled (a copy of the priority arm)",
         "INSTANT-HARVEST", dropped_sub),
        ("[mutant] the writer's harvest_close_of stamping the harvest bar's OPEN (the "
         "priority arm rebuilt)", "INSTANT-HARVEST", open_stamped),
    ])


def hinst_real():
    v6hc = _v6_harvests()
    bad, lines = [], []
    subs = (0, 0)
    for (reg, arm) in ARMS_TYPED:
        f, t = harvest_instant_findings(f"{reg}/{arm}", reg_df(reg, arm), v6hc)
        bad += f
        lines.append(f"{reg}/{arm} {t['stamped']}/{t['harvested']}")
        if (reg, arm) == ("P-WIN-1", "tierE__ratr_priority"):
            subs = (t["substitutes"], t["substitutes_harvested"])
    R = module_R()
    rb = G.regbook_frame(R["priority"], R["pool"])
    same = (rb["harvest_close_ms"].fillna(-1).to_numpy(np.int64).tolist()
            == reg_df("P-WIN-1", "tierE__ratr_priority")["harvest_close_ms"].fillna(-1)
            .to_numpy(np.int64).tolist())
    if not same:
        bad.append("INSTANT-HARVEST: the in-process priority rebuild differs from its record "
                   "on harvest_close_ms")
    if subs[0] < 1 or subs[1] < 1:
        bad.append(f"INSTANT-HARVEST: the priority arm holds {subs} (substitutes, harvested) "
                   f"— the rows the pairing-key join cannot stamp are not exercised")
    return (not bad), (
        f"harvest_close_ms (Int64) on EVERY row of the {len(ARMS_TYPED)} regbooks == this "
        f"file's hand harvest law on its own 4h read (from the bar after the entry, armed once "
        f"a close sat outside the own EMA89/316 edge, touched on the whole bar, strictly before "
        f"the exit bar, corridor_end excepted; the bar's CLOSE), NA iff not harvested "
        f"(stamped/harvested: {' · '.join(lines)}); every v6 key == "
        f"books/v6_campaigns.parquet; the priority arm's {subs[0]} substitutes ({subs[1]} "
        f"harvested) — the rows no pairing-key join can stamp — covered; rebuild == record: "
        f"{same}" + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-DEF", "both tide-age definitions computed; the gated set recomputed from a typed "
     "definition [L-G.1]",
     "on any v6 campaign the module's entry-bar streak / censoring / trailing q25-q50-q75 / "
     "band / >206 flag / arm-bar age differs from this file's derivation, or the written "
     "P-AGE-1 scored refuses any set but {streak >= own trailing q75}, or the shadow any set "
     "but {streak > 206}",
     def_break, def_real),
    ("F-GATE", "each gate removes only the trades its text names — a post-filter, "
     "row-identical [L-1.5]",
     "any gated regbook is not the base minus EXACTLY the typed refused set row-identical on "
     "every column; a refused cohort / era slice is not exactly its rows; a base arm is not "
     "the lineage v6 book on every required column (exact) and books/v6_campaigns on the 13 "
     "SC-7 columns (6 dp); the gate-row table disagrees with this file; or the rival count "
     "is not this file's replay's, on the real log and on one planted rejection fed to both",
     gate_break, gate_real),
    ("F-PRIORITY", "the within-window priority book == this file's own replay of the rule; "
     "3 substitutions hand-walked [L-G.3]",
     "replay_g without hooks is not v6 at 0.000e+00; this file's own v6 replay is not the v6 "
     "book; or the priority book (in-process or written) differs from this file's replay on "
     "any entry (pass, substitute, window, flat, stop, R, ride, count) or, as written, on any "
     "required column",
     prio_break, prio_real),
    ("F-DISC", "every Tier-E disclosure table == this file's own recomputation [L-1.5, L-G.1, "
     "L-G.3]",
     "g_gate_rows (means, forfeit X, rivals, the re-ride from this file's own re-ride, the >206 "
     "caveat), g_tide_bands, g_collisions, g_collision_list_v6, g_arrivals, "
     "g_priority_windows, g_rivals or g_priority_vs_v6 differs from this file's recomputation "
     "at 6 dp",
     disc_break, disc_real),
    ("F-EDGE", "every cut at its boundary; the era straddle; the one-position claim; a forced "
     "hold [L-G.1, L-G.2, L-G.3, L-1.3]",
     "a comparator is not the typed one at its boundary, a straddling entry bar is not holdout "
     "in the module's facts / regbook frame / era slices, the 'never binds' sentence does not "
     "follow the counts, or under a forced hold the module's replays differ from this file's "
     "held replay (or the hold does not bind)",
     edge_break, edge_real),
    ("F-HARVEST-INSTANTS", "the harvest's named-event instant on every regbook row == this "
     "file's hand harvest law; v6 keys == books/ [L-R.5, AM-6 — the lanes pass]",
     "a regbook lacks harvest_close_ms (Int64), stamps a row that did not harvest or leaves a "
     "harvested row NA, an instant differs from the hand harvest law on the own 4h read, a v6 "
     "key differs from books/v6_campaigns, the priority substitutes are not covered, or the "
     "priority rebuild differs from its record",
     hinst_break, hinst_real),
    ("F-GRID", "every Stage G table whole, collared, verdict-free, recomputed [L-1.4, L-G.3]",
     "a table is not whole against its typed cells, a non-registered table lacks the collar "
     "or carries a verdict column / word, an n = 0 cell carries a number, or a cell's n / ΣR / "
     "mean differs from this file's recomputation at 6 dp",
     grid_break, grid_real),
    ("F-KEY", "the regbook interface, the sidecars, the stage tables, the report's texts",
     "a regbook breaks the typed schema (columns, dtypes, nulls, keys, era, haircut, net law), "
     "a sidecar or STATUS disagrees with the typed arm table or this file's canonical CSV, "
     "the manifest's keys are not the typed keys or TP.check_keys(stage_g) under them is RED, "
     "a manifest sha is not its table's or file's, the latest close at fetch time is not "
     "printed beside the pin, a printed table lacks the collar, the one-position sentence "
     "does not match this file's counts, or STAGE_G.md does not print the texts of record, "
     "pre_seen and selection_hazard verbatim",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds differ from each other or from the canonical "
     "files in the typed file set, any byte or any parquet content sha, or either exits "
     "nonzero",
     det_break, det_real),
)


def file_transcript(out: Path, body: bytes, refile: bool) -> list[str]:
    """NEVER CLOBBER the transcript of record [tierc10_resume_fixtures.file_transcript]."""
    if not out.exists() and not refile:
        return [f"{out.name} ABSENT — nothing written; re-file with --refile-transcript"]
    if out.exists() and out.read_bytes() == body:
        return []
    if out.exists() and not refile:
        (rr := out.with_name(out.stem + "_rerun.txt")).write_bytes(body)
        return [f"{out.name} NOT byte-identical; this run -> {rr.name}; record untouched"]
    out.write_bytes(body)
    return []


def main() -> int:
    args = sys.argv[1:]
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT)).resolve()
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 STAGE G FIXTURES — scripts/tierc11_stage_g.py (the admission gates, their "
        "regbooks, the L-G.3 Tier-E structure) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · TC10 pin {TC10_PIN}")
    for ln in G.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            prove(fid, title, fails_if, b, r)
    say(f"\n  {len(PASSED)} GREEN, {len(FAILED)} RED")
    for f in FAILED:
        say(f"    RED: {f}")
    root.mkdir(parents=True, exist_ok=True)
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    bad = file_transcript(root / name, body, "--refile-transcript" in args or bool(pick))
    for x in bad:
        clock(x)
    clock(f"wall {time.time() - t0:.1f}s · transcript sha {sha_bytes(body)}")
    if FAILED:
        print("*** HALT: fixture mismatch. Nothing downstream is trustworthy. ***")
    return 1 if (FAILED or bad) else 0


if __name__ == "__main__":
    raise SystemExit(main())
