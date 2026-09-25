#!/usr/bin/env python
"""TIER-C11 · STAGE R-a — F-FEAS · F-R5-ANCHOR · F-CHOP-VALUE · F-NEST-BOOK · F-GRID ·
F-KEY · F-DET.  The fixtures of scripts/tierc11_stage_r.py (R1 lenses, R2 feasibility,
R3 the nest on the books + the nest-book door, R5 the chop table) [LEANS L-R.1..L-R.5,
L-R.7; AM-1, AM-2, AM-4, AM-6].  REPAIRED after the stage verifier's report (MAJOR-1..4,
MINOR-1..11, 14): the tolls, the R5 / NEST_GRID values and honesty labels, the door's
named events and its extra paths, the causal (prefix-run) nest check.

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law of
scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py; H §8].  A break leg is
a set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a frame, a dict, a
temp dir) or under a MUTATION of the module restored in `finally`; no artifact of
record moves.  The referees are typed HERE (a second object): the commission (lenses,
panels, eras, scales, tolls and the charter tier of every stem, the record cell),
the [Q-R3] thresholds and the word law, the TC10 control journal's sha / n and its
five-row table's counts, the instant stamp law, the bucket / coincidence / honesty
laws of R5 and NEST_GRID, the regbook book_sha256 law, every declared grid cell,
every key and required column.

  F-FEAS        FAILS IF any R2 record row's word or verdict, or any Tier-E row's
                would_read, differs from the word re-derived HERE from its printed
                columns (height: n_ranges >= 30, ratio_median >= 3.0,
                share_ratio_lt_1 <= 0.10; edge: edge_n >= 30, edge_n_ranges >= 30,
                round(edge_median_term_h20, 8) - round(edge_toll_atr, 8) > 0; under a
                floor -> 'FAIL (provisional, n<30)'; a record verdict = the taker word,
                or the reopening-path text when taker FAILs and the maker row PASSES);
                a Tier-E row carries a verdict word (`word` / `verdict`, or a
                *_pass / tc10_word column name) [L-1.4]; the record rows are not
                exactly POOLED:CLASSIC5 · holdout · calibrated · taker on the seven
                typed lenses; a row's toll_bps_rt_min/max is not the typed toll of its
                members (taker 10.0, maker 4.0, charter 2 x (5 + the stem's typed tier
                A 2 / B 5 / C 10) bps round trip); on an ASSET row the maker / charter
                edge_toll_atr or toll_atr_median is not the typed ratio (0.4, (5 +
                slip) / 5) x the taker row's, to the 8-dp rounding bound; a pooled
                row's edge_toll_atr is not the binding (max) member ASSET edge toll of
                the same era / scale / toll [census law C-f]; the printed height-ratio
                deciles d1..d9 are not a non-decreasing distribution with d5 ==
                ratio_median (all NaN iff n_ranges 0); the JSON of record
                disagrees with its row (verdict, word, provisional, the maker /
                charter twin words, the Tier-E tuning / ALL words, the printed
                numbers, toll_bps_rt, pick window, in-sample text, fallback and
                stability-changed members, era / scale / pool / toll); or a
                frozen-3.0 TUNING-era taker row at 5m / 4h / 1d (typed 44 rows)
                differs from TC10's filed height_toll_verdict.parquet on n_ranges,
                ratio_median, share<1, edge_n, edge_n_ranges, median term, toll, net
                or verdict (the cross-process continuity anchor).  SABOTAGE: the
                record read off the TUNING era (module RECORD mutated); the height
                threshold 3.0 -> 2.0 (C.HEIGHT_RATIO_MIN mutated) on a copy holding a
                row in the band; an under-floor row's would_read printed PASS; a
                Tier-E row printed with a verdict word; the JSON's 1h verdict PASS;
                on a 12h sub-build of the module: the maker toll halved and the
                charter toll charged on one side (SR.toll_bps mutated), the twin edge
                toll left at the taker's (SR._twin_edge mutated); a pooled row's toll
                set to the smallest member's on a copy; the deciles reversed on a copy.
  F-R5-ANCHOR   FAILS IF the filed TC10 control journal is not the typed bytes
                (sha256 fcbf5db0…, 200 rows, every entry closing <= 2026-09-21T16:00Z),
                or the frozen-3.0 4h entry-state table re-derived from its 200
                campaigns with the TC11 nest (stage_r.five_row) differs from TC10's
                stamps/control_entry_by_state.parquet on any of the eleven typed
                columns of the five typed rows (typed n 40/66/94/0/200), or the
                written R5_FIVE_ROW's tc10_* columns (all eleven) are not the filed
                ones, or its tc11_* columns (all eleven) are not the five rows
                re-derived HERE by this file's own crosstab from NEST_v6's frozen-3.0
                entry rows and the books' net_r / mfe_r (6-dp rounding bound), or
                R5_CHOP's frozen 4h rows do not partition them.  SABOTAGE: a
                one-bar-late state read (+4h); the state read at the entry bar's OPEN
                (-4h); the calibrated scale in place of frozen 3.0; R5_FIVE_ROW's
                tc11_median_mfe_r replaced by the median net R on a copy.
  F-CHOP-VALUE  FAILS IF any cell of R5_CHOP, NEST_GRID_FREQ, NEST_GRID_BY_STATE or
                NEST_GRID_BY_COIN differs from the cell re-derived HERE from the
                written NEST_v6 / NEST_trg912 ENTRY rows and the books' net_r by the
                laws typed here (bucket: not IN_RANGE -> 'not-in-range:<state>',
                pct < 0 -> '<0', pct >= 100 -> '>=100', else [10d, 10d+10) with d =
                floor(pct / 10); coincidence: 1w 'NA', else both / top / bot / none
                from coin_top / coin_bot (record) or coin_*_mem (twin); n, mean,
                share > 0, sum; the HOLDOUT slice = entries closing after
                1719791999000; n_scale_in_sample = calibrated AND (entry close <= the
                cut OR a consumed lens's FILED pick is a whole-tape fallback);
                n_stability_changed = calibrated AND a consumed lens's FILED pick
                changed first-half vs tuning; consumed lenses = L, plus L+1 for a
                coincidence cell) — counts exact, floats to the 8-dp rounding bound.
                SABOTAGE (the module's own R5 / grid code re-run on the written
                entries): deciles mirrored (SR.bucket_of mutated); coincidence top /
                bot swapped (SR.coin_cat mutated); the mean replaced by the median
                (SR._stats mutated); the 12h table bucketed on the 4h pct (a copy of
                the entries); the 4h in-sample labels dropped (a copy of the entries).
  F-NEST-BOOK   FAILS IF, for either book at either scale, the written NEST's instant
                set differs from the law typed HERE and derived from the raw 4h tape
                (every 4h close from the arm bar through the exit stamp; arm / entry /
                harvest / bell at their close; +1R at the OPEN of the first bar in
                (entry, exit] whose favourable extreme reaches entry +/- R, its twin at
                the close; a stop exit at its bar's OPEN, its twin at the close; a close
                exit at the close; a campaign OPEN at the pin (corridor_end) at
                'as_of_pin', never 'exit'); or the JOIN of the nest onto those instants
                differs from N.nest_at at the same instants (a join-integrity check —
                the same function the module calls, NOT an independent value check);
                or the CAUSAL check fails: on 16 v6 campaigns sampled with seed
                20260924, at the entry instant, per {4h, 12h} x both scales, the
                written state / pct / top / bot / bar close / ATR differ from a run of
                the machine on the tape CUT at the read bar (a prefix run: no later
                bar exists to leak); or the nest-book CLI on the v6 probe differs from
                the in-process door (plumbing) or, outside stamp_law, from NEST_v6; or
                the door's DERIVED path (the v6 probe stripped of its arm / latch /
                exit-stamp / harvest columns, reached_1r and harvested added: v6's arm
                and harvest by the pairing key, exit from exit_reason, +1R by the
                bar-OPEN law) differs from the typed law; or the door, run read-only
                into a temp dir on real regbooks, differs from the law typed HERE:
                P-BRK-4H scored (lane4h: 4h closes from the entry, +1R derived,
                harvest_i, the exit stamp typed from exit_reason and the tape),
                P-WARN-1 scored (v6transform: arm_ms, v6's harvest by the pairing key,
                derived exit and +1R), a harvest-free copy of P-RELAY-1 scored
                re-sidecar'd here (relay: window_arm_close_ms, exit_stamp_ms,
                latch_1h_ms at the resolving 1h child's close, and planted
                parent-decided latches at the parent's OPEN with the close as twin);
                or the door does NOT refuse P-RELAY-1 scored and P-ADD-BRK scored with
                the typed UNSTAMPED counts (their harvested / n_adds records).
                SABOTAGE: intrabar events close-stamped (the module's
                INTRABAR_STAMP mutated), on the books path and on the derived path; a
                one-bar-late nest read on a copy; one bar_close instant dropped; a
                tampered probe regbook (the door must HALT on its book_sha256); a
                leaked next-bar read at the sampled entries (a copy); a harvested
                regbook with no harvest instant (the door must HALT UNSTAMPED); an
                n_adds > 0 regbook with no add instants (HALT UNSTAMPED); the
                parent-latch law disabled (SR._parent_latch mutated) on the relay copy.
  F-GRID        FAILS IF a written grid is not WHOLE against the cells typed HERE
                (R1 71 · R2 1458 · R5 64 · NEST_GRID_FREQ 544 · BY_STATE 100 · BY_COIN
                136); an R1 pick (record / tuning / whole / first half) or window
                differs from the FILED SCALE_PICKS.json, or its window density from the
                filed one; an R1 density (ALL / tuning / holdout, record and frozen) is
                not 100 x its printed confirmed count / its era's printed bar count; an
                R2 fallback-member / stability-changed-member / pick-window label
                differs from the filed picks [AM-4]; an R5 / NEST_GRID row's
                lenses_read / pick_window / stability_changed_members differs from the
                filed picks of the lenses it consumes [AM-4, L-R.2]; a Tier-E table
                lacks the exact collar on any row, or carries a verdict column (R2:
                `word` / `verdict` only on the 7 record rows); a stat (whole or holdout
                slice) is NaN with n > 0 or finite with n = 0; or a partition breaks
                (R1 confirmed ranges and bars, R2 n_ranges and edge_n: tuning +
                holdout == ALL; R5 buckets and NEST_GRID states / coincidence
                categories sum to the entries).  SABOTAGE: an R1 pick moved; an R1
                holdout density struck over ALL bars; the 1w record cell's fallback
                members hidden; the 12h record cell's stability-changed members
                hidden; an R5 pick_window blanked; a dropped R2 cell; an undeclared R5
                cell; R1's collar blanked; a verdict column on a grid; a NaN mean
                under n > 0; a NaN holdout mean under n_holdout > 0; a FREQ count +1.
  F-KEY         FAILS IF a written parquet's key (typed HERE) is not unique, a typed
                required column holds a null, a parquet on disk is undeclared in the
                manifest (or a declared one absent), the manifest's key is not the
                typed one, or its content sha is not the table's.  SABOTAGE: a
                duplicated NEST row; a nulled R2 would_read; a manifest sha altered; a
                manifest key altered; an undeclared parquet in a temp copy.
  F-DET         FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) under
                RUN_ROOT/_det_stage_r differ from each other or from the canonical
                stage_r/ files of record in the file set (recursive), any byte, or any
                parquet content sha (read through pandas on a PATH string, AM-2), or
                either exits nonzero.  SABOTAGE: one byte bent in a copy; a parquet
                copy with one float moved; a hash-order line emitted under the two
                seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity (the only bounds used are the printed
precision's rounding half-ulps, 0.5e-8 and 0.5e-6, derived, not tuned); a check whose
claim is not the design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the
TC11 snapshot (the env shim's guard).  Seed 20260924.  The transcript carries no clock,
no temp path and no number read from another stage's regbook (those go to stdout only:
an owner's re-file must not break this transcript's byte-identical re-pass).

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r.py build     # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
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
import tierc11_stage_r as SR                                         # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

N, E, C = SR.N, SR.E, SR.C
TP = E.TP

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never SR's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN = 1790006400000                 # 2026-09-21T16:00:00Z
ERA_CUT_T = 1719791999000                # 2024-06-30T23:59:59Z [L-1.3]
MS1H = 3_600_000
MS4H = 14_400_000
MS12H = 43_200_000
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
C5_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
U12_T = ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT", "XMRUSDT",
         "BNBUSDT", "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
P17_T = C5_T + U12_T
LENSES_T = ("5m", "15m", "1h", "4h", "12h", "1d", "1w")          # L-R.1
U_LENSES_T = ("1h", "4h", "1d")                                   # L-R.1 the twelve
NEST_LENSES_T = ("1h", "4h", "12h", "1d", "1w")                   # L-R.5
LADDER_T = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": "1w", "1w": None}
ERAS_T = ("ALL", "tuning", "holdout")
SCALES_T = ("calibrated", "frozen3.0")
FROZEN_T = 3.0
TOLLS_T = ("taker", "charter", "maker")
POOLS_T = {"POOLED:CLASSIC5": (C5_T, LENSES_T), "POOLED:PANEL17": (P17_T, U_LENSES_T)}
RECORD_T = ("POOLED:CLASSIC5", "holdout", "calibrated", "taker")  # L-R.4
H_MIN_N, RATIO_MIN, SHARE_MAX = 30, 3.0, 0.10                      # TC10 [Q-R3] height leg
EDGE_MIN_N, EDGE_MIN_R, ROUND_ND = 30, 30, 8                        # edge leg; census net rounding
W_PASS, W_FAIL, W_PROV = "PASS", "FAIL", "FAIL (provisional, n<30)"
REOPEN_T = ("FAIL — maker twin PASSES (the reopening path; needs a toll-model change the "
            "operator rules)")
# THE TOLLS [L-1.1, L-1.2, L-R.4]: taker 5.0 / side (10.0 rt); maker 2.0 / side, zero
# slippage (4.0 rt); charter = taker + the stem's slippage tier, both sides
TAKER_SIDE_T, TAKER_RT_T, MAKER_RT_T = 5.0, 10.0, 4.0
SLIP_TIER_T = {"A": 2.0, "B": 5.0, "C": 10.0}
STEM_TIER_T = {"BTCUSDT": "A", "ETHUSDT": "A", "SOLUSDT": "B", "NEARUSDT": "B", "ZECUSDT": "B",
               "LTCUSDT": "B", "BNBUSDT": "B", "DOGEUSDT": "B", "UNIUSDT": "B", "SUIUSDT": "B",
               "XMRUSDT": "B", "ENAUSDT": "C", "PUMPUSDT": "C", "HYPEUSDT": "C",
               "MNTUSDT_BYBIT": "C", "1000PEPEUSDT": "C", "1000BONKUSDT": "C"}
ROUND8_HALF = 0.5e-8                     # the tables' 8-dp rounding (C.canon) — a half-ulp
ROUND6_HALF = 0.5e-6                     # the five-row table's 6-dp rounding (TB.r6)
FLOAT_EPS = 1e-12                        # float noise far below either half-ulp
COLLAR_T = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
            "gates": "nothing"}
VERDICT_COLS_T = ("verdict", "word", "clears_bh_bar", "promotable", "scored_in_family",
                  "p_one_sided", "is_the_registered_cell", "verdict_pass", "gate_height_pass",
                  "gate_edge_fade_pass", "census_verdict_pass", "tc10_verdict_pass",
                  "tc10_word")
R2_RECORD_ONLY_T = ("word", "verdict")
R2_BANNED_T = ("verdict_pass", "gate_height_pass", "gate_edge_fade_pass",
               "census_verdict_pass", "tc10_verdict_pass", "tc10_word")
TC10_LENSES_T = ("5m", "4h", "1d")
TC10_POOL_T = {"POOLED:CLASSIC5": "POOLED:CLASSIC5", "POOLED:PANEL17": "POOLED:ALL"}
CONTINUITY_N_T = 44                      # frozen tuning taker rows at 5m / 4h / 1d: 5+1 · 17+2 · 17+2
STATES_T = ("NONE", "IN_RANGE", "BULL_EXP", "BEAR_EXP")
STATE_CODE_T = {0: "NONE", 1: "BULL_EXP", -1: "BEAR_EXP"}
COIN_CATS_T = ("both", "top", "bot", "none")
COIN_RULES_T = ("record", "mem_twin")
BOOKS_T = ("v6", "trg912")
BOOK_N_T = {"v6": 200, "trg912": 199}
DEC_T = tuple(f"[{10 * d},{10 * d + 10})" for d in range(10))
R5_BUCKETS_T = DEC_T + ("<0", ">=100", "not-in-range:NONE", "not-in-range:BULL_EXP",
                        "not-in-range:BEAR_EXP", "__ALL__")
R5_LENSES_T = ("4h", "12h")
TC10_JOURNAL_REL = "research_outputs/tierc10/panel/control_journal.parquet"
TC10_JOURNAL_SHA = "fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c"
TC10_JOURNAL_N = 200
TC10_FIVE_REL = "research_outputs/tierc10/stamps/control_entry_by_state.parquet"
TC10_VERDICT_REL = "research_outputs/tierc10/census/height_toll_verdict.parquet"
FIVE_STATES_T = ("BEAR_EXP", "BULL_EXP", "NEUTRAL", "NONE", "__ALL__")
FIVE_N_T = {"BEAR_EXP": 40, "BULL_EXP": 66, "NEUTRAL": 94, "NONE": 0, "__ALL__": 200}
FIVE_COLS_T = ("n", "n_assets", "net_r_sum", "expectancy_r", "median_net_r", "win_rate_pct",
               "median_mfe_r", "median_pct_of_range", "median_dist_boundary_atr", "n_in_range",
               "provisional")
NEST_FIELDS_T = ("k", "bar_close_ms", "state", "in_range", "pct", "dist_signed_atr",
                 "near_side", "bnd_age", "dev_top", "dev_bot", "flip_pol", "flip_age", "top",
                 "bot", "atr_L", "coin_top", "coin_bot", "coin_top_mem", "coin_bot_mem",
                 "pick_window", "scale_in_sample", "stability_changed")
NEST_KEY_T = ["scale_kind", "symbol", "entry_ms", "instant_kind", "instant_ms"]
PREFIX_N_T = 16                          # sampled v6 campaigns for the causal (prefix) check
PREFIX_LENSES_T = ("4h", "12h")
KEYS_T = {"R1_LENSES": ["asset", "lens"],
          "R2_FEASIBILITY": ["panel", "lens", "era", "scale_kind", "toll"],
          "NEST_v6": ["book"] + NEST_KEY_T, "NEST_trg912": ["book"] + NEST_KEY_T,
          "NEST_GRID_FREQ": ["book", "scale_kind", "lens", "coin_rule", "state", "coin_cat"],
          "NEST_GRID_BY_STATE": ["book", "scale_kind", "lens", "state"],
          "NEST_GRID_BY_COIN": ["book", "scale_kind", "lens", "coin_rule", "coin_cat"],
          "R5_CHOP": ["scale_kind", "lens", "bucket"],
          "R5_FIVE_ROW": ["macro_state_at_entry"],
          "nestbook_probe/V6-PROBE/base": ["symbol", "entry_ms"],
          "nest_books/V6-PROBE__base": NEST_KEY_T}
ASOF_T = ("as_of_last_closed_4h", "as_of_substrate")
COLLAR_COLS_T = ("tier", "selection_not_a_result", "gates")
HONEST_COLS_T = ("n_scale_in_sample", "n_stability_changed", "n_holdout", "lenses_read",
                 "pick_window", "stability_changed_members")
REGBOOK_REQ_T = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
                 "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
                 "funding_r", "haircut_net_r", "era", "lane")
REGBOOK_FLOATS_T = ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r",
                    "haircut_net_r")
REQUIRED_T = {
    "R1_LENSES": ("cell", "asset", "lens", "panel", "n_bars", "pick_of_record", "pick_window",
                  "label", "whole_tape_pick", "frozen_scale", "n_confirmed_ALL",
                  "n_confirmed_tuning", "n_confirmed_holdout", "density_per_100_ALL")
                 + COLLAR_COLS_T + ASOF_T,
    "R2_FEASIBILITY": ("cell", "panel", "lens", "era", "scale_kind", "toll", "members",
                       "toll_bps_rt_min", "toll_bps_rt_max", "n_ranges", "edge_n",
                       "edge_n_ranges", "is_lens_verdict_of_record", "under_floor",
                       "pick_window", "scale_in_sample") + COLLAR_COLS_T + ASOF_T,
    "NEST": ("book", "stamp_law", "instant_ts", "direction", "entry_close_ms",
             "campaign_lens") + tuple(NEST_KEY_T) + tuple(f"{L}_state" for L in NEST_LENSES_T)
            + tuple(f"{L}_k" for L in NEST_LENSES_T) + COLLAR_COLS_T + ASOF_T,
    "NEST_GRID_FREQ": ("cell", "n", "n_entries", "share") + HONEST_COLS_T + COLLAR_COLS_T
                      + ASOF_T,
    "NEST_GRID_BY_STATE": ("cell", "n", "nan_reason", "nan_reason_holdout") + HONEST_COLS_T
                          + COLLAR_COLS_T + ASOF_T,
    "NEST_GRID_BY_COIN": ("cell", "n", "nan_reason", "nan_reason_holdout") + HONEST_COLS_T
                         + COLLAR_COLS_T + ASOF_T,
    "R5_CHOP": ("cell", "n", "nan_reason", "nan_reason_holdout") + HONEST_COLS_T
               + COLLAR_COLS_T + ASOF_T,
    "R5_FIVE_ROW": ("tc11_n", "tc10_n", "tc11_n_assets", "tc10_n_assets", "tc11_provisional",
                    "tc10_provisional", "tc10_reproduced_on_filed_journal") + COLLAR_COLS_T
                   + ASOF_T,
    "nestbook_probe/V6-PROBE/base": REGBOOK_REQ_T + ("arm_close_ms", "exit_stamp_ms"),
    "nest_books/V6-PROBE__base": ("registration", "arm", "stamp_law") + tuple(NEST_KEY_T)
                                 + COLLAR_COLS_T + ASOF_T,
}
REGBOOKS = E.OUT / "regbooks"                # other stages' regbooks: READ-ONLY here

OUT = SR.OUT
DET_ROOT = SR.DET_ROOT
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_R.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line, flush=True)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}", flush=True)


def note(line: str) -> None:                # OTHER STAGES' data (their regbooks) -> stdout ONLY
    """Counts read from other stages' regbooks: they move when an owner re-files, so
    they never enter the transcript of record (which must re-pass byte-identical)."""
    print(f"  [other stages' regbooks · stdout only] {line}", flush=True)


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    say(f"\n{fid} — {title}")
    say(f"  FAILS IF: {fails_if}")
    t0 = time.time()
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
    clock(f"{fid} {time.time() - t0:.1f}s")
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


_W: dict = {}


def written(name: str) -> pd.DataFrame:
    """The canonical stage_r tables of record (read once, a copy handed out)."""
    if name not in _W:
        _W[name] = pd.read_parquet(str(OUT / f"{name}.parquet"))
    return _W[name].copy()


def verdicts_json() -> dict:
    return json.loads((OUT / "R2_LENS_VERDICTS.json").read_text(encoding="utf-8"))


def _isna(x) -> bool:
    try:
        return bool(pd.isna(x))
    except (TypeError, ValueError):
        return False


def _py(x):
    """a finding's value as plain Python (no numpy repr in the transcript)."""
    if _isna(x):
        return None
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    if isinstance(x, (np.bool_,)):
        return bool(x)
    return x


def _close(a, b, half: float) -> bool:
    """equal at the printed precision: NaN == NaN, else |a - b| <= the rounding
    half-ulp (+ float noise) — a DERIVED bound, never a tuned one."""
    if _isna(a) or _isna(b):
        return _isna(a) and _isna(b)
    a, b = float(a), float(b)
    return abs(a - b) <= half + FLOAT_EPS * max(1.0, abs(b))


_PICKS: dict = {}


def picks_filed() -> dict:
    """SCALE_PICKS.json (the filed pins), read HERE — a second object."""
    if not _PICKS:
        rec = json.loads((E.OUT / "ranges" / "SCALE_PICKS.json").read_text(encoding="utf-8"))
        _PICKS.update({(c["asset"], c["lens"]): c for c in rec["cells"]})
    return _PICKS


def _pick_changed(s: str, L: str) -> bool:
    return picks_filed()[(s, L)]["stable_first_half_vs_tuning"] is False


def _pick_fallback(s: str, L: str) -> bool:
    return picks_filed()[(s, L)]["pick_window"] != "tuning"


# ═══════════════════════════════════════════════════════════════════ F-FEAS
def typed_net(med, toll) -> float:
    if _isna(med) or _isna(toll) or not (np.isfinite(med) and np.isfinite(toll)):
        return float("nan")
    return float(np.round(float(med), ROUND_ND) - np.round(float(toll), ROUND_ND))


def typed_word(r) -> tuple[str, bool]:
    n, en, enr = int(r["n_ranges"]), int(r["edge_n"]), int(r["edge_n_ranges"])
    rm, sh = float(r["ratio_median"]), float(r["share_ratio_lt_1"])
    net = typed_net(r["edge_median_term_h20"], r["edge_toll_atr"])
    h = n >= H_MIN_N and np.isfinite(rm) and rm >= RATIO_MIN and np.isfinite(sh) and sh <= SHARE_MAX
    e = en >= EDGE_MIN_N and enr >= EDGE_MIN_R and np.isfinite(net) and net > 0
    under = n < H_MIN_N or enr < EDGE_MIN_R or en < EDGE_MIN_N
    return (W_PASS if (h and e) else W_PROV if under else W_FAIL), under


def typed_toll(stem: str, toll: str) -> float:
    if toll == "taker":
        return TAKER_RT_T
    if toll == "maker":
        return MAKER_RT_T
    return 2.0 * (TAKER_SIDE_T + SLIP_TIER_T[STEM_TIER_T[stem]])


def _word_finding(tag: str, printed, typed: str, under: bool) -> str:
    det = "FLOOR" if (printed == W_PASS and under) else tag
    return f"{det}: printed {printed!r}, typed law {typed!r}"


def toll_findings(R2: pd.DataFrame) -> list[str]:
    """[L-R.4 'toll'; verifier MAJOR-1] the tolls the reading names, refereed by the
    TYPED toll of every member: the printed bps; on every ASSET row the twin tolls in
    ATR as the typed ratio x the taker row's (the census's toll is bps / 1e4 x close
    / ATR, linear in bps; the 8-dp rounding bound); on every pooled row the edge
    toll as the BINDING (max) member ASSET edge toll [census law C-f]."""
    out = []
    idx = {(r["panel"], r["lens"], r["era"], r["scale_kind"], r["toll"]): r
           for _, r in R2.iterrows()}
    for k, r in idx.items():
        mem = str(r["members"]).split(",")
        want = [typed_toll(s, r["toll"]) for s in mem]
        if float(r["toll_bps_rt_min"]) != min(want) or float(r["toll_bps_rt_max"]) != max(want):
            out.append(f"TOLL-BPS: {r['cell']} prints {r['toll_bps_rt_min']}..{r['toll_bps_rt_max']}"
                       f" bps round trip, the typed toll of its members is "
                       f"{min(want)}..{max(want)}")
    for k, r in idx.items():
        p, l, e, s_k, t = k
        if not p.startswith("ASSET:") or t == "taker":
            continue
        s = p[len("ASSET:"):]
        base = idx.get((p, l, e, s_k, "taker"))
        if base is None:
            out.append(f"TOLL-SCALE: {r['cell']} has no taker row")
            continue
        f = typed_toll(s, t) / typed_toll(s, "taker")
        for c in ("edge_toll_atr", "toll_atr_median"):
            a, b = float(r[c]), float(base[c])
            if np.isnan(a) and np.isnan(b):
                continue
            ok = not (np.isnan(a) or np.isnan(b)) and \
                abs(a - f * b) <= ROUND8_HALF * (1.0 + f) + FLOAT_EPS * max(1.0, abs(b))
            if not ok:
                out.append(f"TOLL-SCALE: {r['cell']} {c} {a!r} != {f:g} x the taker row's "
                           f"{b!r} (the typed {t} / taker toll ratio of {s})")
    for k, r in idx.items():
        p, l, e, s_k, t = k
        if not p.startswith("POOLED:"):
            continue
        vals = []
        for s in str(r["members"]).split(","):
            m = idx.get((f"ASSET:{s}", l, e, s_k, t))
            vals.append(float("nan") if m is None else float(m["edge_toll_atr"]))
        fin = [v for v in vals if np.isfinite(v)]
        want = max(fin) if fin else float("nan")
        a = float(r["edge_toll_atr"])
        if not ((np.isnan(a) and np.isnan(want)) or a == want):
            out.append(f"TOLL-POOL: {r['cell']} edge_toll_atr {a!r} != the binding (max) member "
                       f"ASSET edge toll {want!r} [census law C-f]")
    return out


RATIO_DEC_T = tuple(f"ratio_d{q}" for q in range(1, 10))


def ratio_dist_findings(R2: pd.DataFrame) -> list[str]:
    """[contract R2 'height ÷ round-trip toll (distribution)'; verifier MINOR-3] the
    printed deciles d1..d9 are a distribution: non-decreasing, d5 == ratio_median,
    all NaN iff n_ranges == 0."""
    out = []
    for _, r in R2.iterrows():
        q = [float(r[c]) for c in RATIO_DEC_T]
        n = int(r["n_ranges"])
        if n == 0:
            if not all(np.isnan(x) for x in q):
                out.append(f"RATIO-DIST: {r['cell']} n_ranges 0 but deciles printed")
            continue
        if any(np.isnan(x) for x in q) or any(b < a for a, b in zip(q, q[1:])) or \
                q[4] != float(r["ratio_median"]):
            out.append(f"RATIO-DIST: {r['cell']} deciles {q} are not a distribution with d5 == "
                       f"ratio_median {float(r['ratio_median'])!r}")
    return out


def feas_findings(R2: pd.DataFrame, V: dict) -> list[str]:
    out = []
    want = {f"{RECORD_T[0]}|{l}|{RECORD_T[1]}|{RECORD_T[2]}|{RECORD_T[3]}" for l in LENSES_T}
    rec = R2[R2["is_lens_verdict_of_record"].astype(bool)]
    got = set(rec["cell"])
    if got != want:
        out.append(f"RECORD-SET: record cells {sorted(got - want)[:3]} not typed; typed "
                   f"{sorted(want - got)[:3]} not marked")
    bad_era = rec[rec["era"] != RECORD_T[1]]
    if len(bad_era):
        out.append(f"RECORD-ERA: {len(bad_era)} record row(s) read off era "
                   f"{sorted(set(bad_era['era']))}, the typed record era is {RECORD_T[1]!r}")
    for c in R2_BANNED_T:
        if c in R2.columns:
            out.append(f"TIER-E-WORD: R2 carries the verdict-named column {c!r} [L-1.4]")
    tw = {}
    for _, r in R2.iterrows():
        tw[(r["panel"], r["lens"], r["era"], r["scale_kind"], r["toll"])] = typed_word(r)
    for _, r in R2.iterrows():
        k = (r["panel"], r["lens"], r["era"], r["scale_kind"], r["toll"])
        w, under = tw[k]
        is_rec = bool(r["is_lens_verdict_of_record"])
        if is_rec:
            if r["word"] != w:
                out.append(_word_finding("WORD", r["word"], w, under) + f" on {r['cell']}")
            mk = tw[(k[0], k[1], k[2], k[3], "maker")][0]
            v = W_PASS if w == W_PASS else (REOPEN_T if mk == W_PASS else w)
            if r["verdict"] != v:
                out.append(_word_finding("VERDICT", r["verdict"], v, under) + f" on {r['cell']}")
            if not _isna(r["would_read"]):
                out.append(f"WOULD-READ: the record row {r['cell']} carries would_read")
            if r["tier"] == COLLAR_T["tier"]:
                out.append(f"COLLAR: the record row {r['cell']} is collared Tier-E")
        else:
            if not _isna(r["word"]):
                out.append(f"TIER-E-WORD: {r['cell']} carries the verdict word {r['word']!r} "
                           f"(a Tier-E row's word is would_read only) [L-1.4, L-R.4]")
            if r["would_read"] != w:
                out.append(_word_finding("WOULD-READ", r["would_read"], w, under)
                           + f" on {r['cell']}")
            if not _isna(r["verdict"]):
                out.append(f"VERDICT-ON-TIER-E: {r['cell']} carries verdict {r['verdict']!r}")
            for c, v in COLLAR_T.items():
                if r[c] != v:
                    out.append(f"COLLAR: {r['cell']} {c} = {r[c]!r}")
    out += toll_findings(R2)
    out += ratio_dist_findings(R2)
    lv = V.get("lenses", {})
    if sorted(lv) != sorted(LENSES_T):
        out.append(f"JSON: lenses {sorted(lv)} != typed {sorted(LENSES_T)}")
    for l in LENSES_T:
        v = lv.get(l, {})
        z = R2[(R2["lens"] == l) & (R2["panel"] == RECORD_T[0]) & (R2["scale_kind"] == RECORD_T[2])]
        zr = z[z["era"] == RECORD_T[1]]
        if len(zr) != 3 or len(z) != 9:
            out.append(f"JSON: lens {l}: {len(zr)} rows for the record cell's three tolls")
            continue
        r = zr[zr["toll"] == "taker"].iloc[0]
        w, under = typed_word(r)
        mk = typed_word(zr[zr["toll"] == "maker"].iloc[0])[0]
        ch = typed_word(zr[zr["toll"] == "charter"].iloc[0])[0]
        tu = typed_word(z[(z["era"] == "tuning") & (z["toll"] == "taker")].iloc[0])[0]
        al = typed_word(z[(z["era"] == "ALL") & (z["toll"] == "taker")].iloc[0])[0]
        vv = W_PASS if w == W_PASS else (REOPEN_T if mk == W_PASS else w)
        exp = {"verdict": vv, "word": w, "provisional": under, "maker_twin": mk,
               "charter_twin": ch, "tier_e_tuning_word": tu, "tier_e_all_word": al,
               "n_ranges": int(r["n_ranges"]),
               "edge_n": int(r["edge_n"]), "edge_n_ranges": int(r["edge_n_ranges"]),
               "era": RECORD_T[1], "scale": RECORD_T[2], "pool": RECORD_T[0], "toll": RECORD_T[3],
               "toll_bps_rt": TAKER_RT_T, "members": ",".join(C5_T)}
        for c in ("pick_window", "scale_in_sample", "fallback_members",
                  "stability_changed_members"):
            exp[c] = r[c]
        for c in ("ratio_median", "share_ratio_lt_1", "edge_median_term_h20", "edge_toll_atr",
                  "edge_net_h20"):
            exp[c] = float(r[c])
        for c, e in exp.items():
            g = v.get(c)
            same = (g == e) if not isinstance(e, float) else (
                g is not None and (float(g) == e or (np.isnan(e) and np.isnan(float(g)))))
            if not same:
                out.append(f"JSON: {l}.{c} = {g!r}, its record row / typed law says {e!r}")
    return out


def continuity_findings(R2: pd.DataFrame, tc10: pd.DataFrame) -> tuple[list[str], int]:
    """TC11's frozen-3.0 TUNING-era taker rows at 5m / 4h / 1d == TC10's filed rows."""
    out, n = [], 0
    z = R2[(R2["scale_kind"] == "frozen3.0") & (R2["era"] == "tuning") & (R2["toll"] == "taker")
           & (R2["lens"].isin(TC10_LENSES_T))]
    t = {(r["lens"], r["asset"]): r for _, r in
         tc10[(tc10["scale_kind"] == "frozen3.0") & (tc10["era"] == "tuning")].iterrows()}
    for _, r in z.iterrows():
        key = (r["lens"], TC10_POOL_T.get(r["panel"], r["panel"].replace("ASSET:", "")))
        q = t.get(key)
        if q is None:
            out.append(f"TC10-CONTINUITY: no TC10 row for {key}")
            continue
        n += 1
        for c in ("n_ranges", "edge_n", "edge_n_ranges"):
            if int(r[c]) != int(q[c]):
                out.append(f"TC10-CONTINUITY: {r['cell']} {c} {r[c]} != TC10 {q[c]}")
        for c in ("ratio_median", "share_ratio_lt_1", "edge_median_term_h20", "edge_toll_atr",
                  "edge_net_h20"):
            a, b = float(r[c]), float(q[c])
            if not (a == b or (np.isnan(a) and np.isnan(b))):
                out.append(f"TC10-CONTINUITY: {r['cell']} {c} {a!r} != TC10 {b!r}")
        wr = r["word"] if not _isna(r["word"]) else r["would_read"]
        if (wr == W_PASS) != bool(q["verdict_pass"]):
            out.append(f"TC10-CONTINUITY: {r['cell']} word {wr} vs TC10 verdict_pass "
                       f"{bool(q['verdict_pass'])}")
    if n != CONTINUITY_N_T:
        out.append(f"TC10-CONTINUITY: {n} rows compared, typed {CONTINUITY_N_T}")
    return out, n


def _tc10_verdicts() -> pd.DataFrame:
    return pd.read_parquet(str(E.tc10_record(TC10_VERDICT_REL)))


def sub_r2(lens: str = "12h") -> pd.DataFrame:
    """A SUB-BUILD of R2 for one lens through the module's own code (lens_pass ->
    r2_rows -> finalize_r2) — the seam the toll plants mutate."""
    P = SR.lens_pass(lens)
    return SR.finalize_r2(pd.DataFrame(SR.r2_rows(lens, P, _tc10_verdicts())))


def feas_break():
    R2, V = written("R2_FEASIBILITY"), verdicts_json()
    orig_toll = SR.toll_bps

    def era_swap():
        with mutated(SR, "RECORD", dict(SR.RECORD, era="tuning")):
            d = SR.finalize_r2(R2)
            v = {"lenses": SR.lens_verdicts(d)}
        return feas_findings(d, v)

    def threshold():
        d = R2.copy()
        i = d.index[(d["cell"] == f"{RECORD_T[0]}|4h|{RECORD_T[1]}|{RECORD_T[2]}|"
                                  f"{RECORD_T[3]}")][0]
        d.loc[i, ["ratio_median", "share_ratio_lt_1"]] = [2.5, 0.0]
        d.loc[i, ["n_ranges", "edge_n", "edge_n_ranges"]] = [40, 100, 40]
        d.loc[i, "edge_median_term_h20"] = float(d.loc[i, "edge_toll_atr"]) + 0.25
        with mutated(C, "HEIGHT_RATIO_MIN", 2.0):
            d2 = SR.finalize_r2(d)
            v = {"lenses": SR.lens_verdicts(d2)}
        return feas_findings(d2, v)

    def floor_pass():
        d = R2.copy()
        i = d.index[(d["under_floor"].astype(bool)) & (~d["is_lens_verdict_of_record"]
                                                      .astype(bool))][0]
        d.loc[i, "would_read"] = W_PASS
        return feas_findings(d, V)

    def tier_e_word():
        d = R2.copy()
        i = d.index[~d["is_lens_verdict_of_record"].astype(bool)][3]
        d["word"] = d["word"].astype(object)
        d.loc[i, "word"] = d.loc[i, "would_read"]
        return feas_findings(d, V)

    def json_pass():
        v = json.loads(json.dumps(V))
        v["lenses"]["1h"]["verdict"] = W_PASS
        return feas_findings(R2, v)

    def maker_halved():
        f = (lambda s, t: orig_toll(s, t) / 2.0 if t == "maker" else orig_toll(s, t))
        with mutated(SR, "toll_bps", f):
            d = sub_r2("12h")
        return toll_findings(d)

    def charter_one_side():
        f = (lambda s, t: orig_toll(s, t) / 2.0 if t == "charter" else orig_toll(s, t))
        with mutated(SR, "toll_bps", f):
            d = sub_r2("12h")
        return [x for x in toll_findings(d) if not x.startswith("TOLL-BPS")]

    def twin_at_taker():
        with mutated(SR, "_twin_edge", lambda base, tape, w, bps: base):
            d = sub_r2("12h")
        return toll_findings(d)

    def pool_min():
        d = R2.copy()
        idx = {(r["panel"], r["lens"], r["era"], r["scale_kind"], r["toll"]): i
               for i, r in d.iterrows()}
        hit = 0
        for (p, l, e, k, t), i in idx.items():
            if not p.startswith("POOLED:") or hit:
                continue
            vals = [float(d.loc[idx[(f"ASSET:{s}", l, e, k, t)], "edge_toll_atr"])
                    for s in str(d.loc[i, "members"]).split(",")]
            fin = sorted(v for v in vals if np.isfinite(v))
            if len(fin) >= 2 and fin[0] < fin[-1]:
                d.loc[i, "edge_toll_atr"] = fin[0]
                hit = 1
        return toll_findings(d)

    def dec_reversed():
        d = R2.copy()
        vals = d[list(RATIO_DEC_T)].to_numpy(float)[:, ::-1]
        for i, c in enumerate(RATIO_DEC_T):
            d[c] = vals[:, i]
        return ratio_dist_findings(d)

    return plants([
        ("era swap: the record read off the TUNING era (SR.RECORD mutated)", "RECORD-ERA",
         era_swap),
        ("the height threshold 3.0 -> 2.0 (C.HEIGHT_RATIO_MIN mutated) on a copy with the 4h "
         "record row placed at ratio 2.5", "WORD", threshold),
        ("an under-floor Tier-E row's would_read printed PASS", "FLOOR", floor_pass),
        ("a Tier-E row printed with a verdict word in `word`", "TIER-E-WORD", tier_e_word),
        ("R2_LENS_VERDICTS.json's 1h verdict set to PASS (Stage S's gate)", "JSON", json_pass),
        ("the maker toll halved (SR.toll_bps mutated) on a 12h sub-build", "TOLL-BPS",
         maker_halved),
        ("the charter toll charged on ONE side (SR.toll_bps mutated) on a 12h sub-build — "
         "judged on the ATR ratios alone", "TOLL-SCALE", charter_one_side),
        ("the twin edge toll left at the taker's (SR._twin_edge mutated) on a 12h sub-build",
         "TOLL-SCALE", twin_at_taker),
        ("a pooled row's edge toll set to its smallest member's (not the binding max) on a "
         "copy", "TOLL-POOL", pool_min),
        ("the height-ratio deciles printed in reverse order (d9..d1) on a copy", "RATIO-DIST",
         dec_reversed),
    ])


def feas_real():
    R2, V = written("R2_FEASIBILITY"), verdicts_json()
    f = feas_findings(R2, V)
    cf, n = continuity_findings(R2, _tc10_verdicts())
    f += cf
    rec = R2[R2["is_lens_verdict_of_record"].astype(bool)]
    words = rec["word"].value_counts().to_dict()
    wr = R2["would_read"].value_counts().to_dict()
    n_te = int((~R2["is_lens_verdict_of_record"].astype(bool)).sum())
    n_asset_twin = int((R2["panel"].str.startswith("ASSET:") & (R2["toll"] != "taker")).sum())
    n_pool = int(R2["panel"].str.startswith("POOLED:").sum())
    vs = " · ".join(f"{l} {V['lenses'][l]['verdict']}" for l in LENSES_T)
    n_dist = int((R2["n_ranges"].astype(int) > 0).sum())
    return (not f), (f"{len(R2)} R2 rows: the 7 record rows' word / verdict and the {n_te} "
                     f"Tier-E rows' would_read re-derived from the printed columns by the typed "
                     f"law (record words {dict(sorted(words.items()))}; Tier-E would_read "
                     f"{dict(sorted(wr.items()))}); no Tier-E row carries a verdict word and no "
                     f"verdict-named column is printed; tolls: every row's bps == the typed "
                     f"toll of its members, {n_asset_twin} ASSET twin rows == the typed ratio x "
                     f"the taker row (edge and height toll, 8-dp bound), {n_pool} pooled rows' "
                     f"edge toll == the binding member max; the height ratio d1..d9 a "
                     f"non-decreasing distribution with d5 == ratio_median on the {n_dist} rows "
                     f"with ranges (all NaN on the rest); JSON == its record rows incl. the "
                     f"Tier-E tuning / ALL words, toll and labels ({vs}); TC10 continuity: {n} "
                     f"frozen-3.0 tuning taker rows == TC10's filed verdict table on every "
                     f"compared column" + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-R5-ANCHOR
def anchor_inputs() -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    p = E.tc10_record(TC10_JOURNAL_REL)
    b = p.read_bytes()
    j = pd.read_parquet(str(p))
    f5 = pd.read_parquet(str(E.tc10_record(TC10_FIVE_REL)))
    bad = []
    if sha_bytes(b) != TC10_JOURNAL_SHA or len(j) != TC10_JOURNAL_N:
        bad.append(f"REFEREE: the filed journal is sha {sha_bytes(b)[:12]}… / {len(j)} rows, "
                   f"typed {TC10_JOURNAL_SHA[:12]}… / {TC10_JOURNAL_N}")
    late = int((j["entry_ms"].astype(np.int64) + MS4H > TC10_PIN).sum())
    if late:
        bad.append(f"REFEREE: {late} filed entries close after the TC10 window")
    fn = {str(r["macro_state_at_entry"]): int(r["n"]) for _, r in f5.iterrows()}
    if fn != FIVE_N_T:
        bad.append(f"REFEREE: the filed five-row counts {fn} != typed {FIVE_N_T}")
    return j, f5, bad


def anchor_cmp(got: pd.DataFrame, filed: pd.DataFrame, tag: str = "R5-ANCHOR") -> list[str]:
    out = []
    gb = {str(r["macro_state_at_entry"]): r for _, r in got.iterrows()}
    fb = {str(r["macro_state_at_entry"]): r for _, r in filed.iterrows()}
    if sorted(gb) != sorted(FIVE_STATES_T) or sorted(fb) != sorted(FIVE_STATES_T):
        return [f"{tag}: rows {sorted(gb)} / {sorted(fb)} != typed {sorted(FIVE_STATES_T)}"]
    for st in FIVE_STATES_T:
        for c in FIVE_COLS_T:
            a, b = gb[st][c], fb[st][c]
            if _isna(a) and _isna(b):
                continue
            if _isna(a) != _isna(b) or (c == "provisional" and bool(a) != bool(b)) or \
                    (c != "provisional" and float(a) != float(b)):
                out.append(f"{tag} {st}.{c}: TC11 {a!r} != TC10 filed {b!r}")
    return out


def typed_five(nest_v6: pd.DataFrame) -> dict:
    """The TC11 v6 book's five rows, re-derived HERE (this file's own crosstab) from
    NEST_v6's frozen-3.0 ENTRY rows (4h state; IN_RANGE printed as TC10's NEUTRAL;
    |dist_signed_atr|) and the books' net_r / mfe_r — unrounded."""
    camp = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    jr = pd.read_parquet(str(E.OUT / "books" / "v6_journal.parquet"))
    e = nest_v6[(nest_v6["scale_kind"] == "frozen3.0") & (nest_v6["instant_kind"] == "entry")]
    j = e[["symbol", "entry_ms", "4h_state", "4h_pct", "4h_dist_signed_atr", "4h_in_range"]] \
        .merge(camp[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"], how="left",
               validate="1:1") \
        .merge(jr[["asset", "entry_ms", "mfe_r"]].rename(columns={"asset": "symbol"}),
               on=["symbol", "entry_ms"], how="left", validate="1:1")
    st = j["4h_state"].astype(str).replace({"IN_RANGE": "NEUTRAL"})
    out = {}
    for key in FIVE_STATES_T:
        g = j if key == "__ALL__" else j[st == key]
        net = g["net_r"].to_numpy(float)
        pct = g["4h_pct"].to_numpy(float)
        dist = np.abs(g["4h_dist_signed_atr"].to_numpy(float))
        n = len(g)
        out[key] = {
            "n": n, "n_assets": int(g["symbol"].nunique()),
            "net_r_sum": float(net.sum()) if n else np.nan,
            "expectancy_r": float(net.mean()) if n else np.nan,
            "median_net_r": float(np.median(net)) if n else np.nan,
            "win_rate_pct": 100.0 * float((net > 0).mean()) if n else np.nan,
            "median_mfe_r": float(np.median(g["mfe_r"].to_numpy(float))) if n else np.nan,
            "median_pct_of_range": (float(np.nanmedian(pct)) if n and np.isfinite(pct).any()
                                    else np.nan),
            "median_dist_boundary_atr": (float(np.nanmedian(dist))
                                         if n and np.isfinite(dist).any() else np.nan),
            "n_in_range": int(g["4h_in_range"].astype("boolean").fillna(False).sum()),
            "provisional": bool(n < 30)}
    return out


def five_tc11_findings(w5: pd.DataFrame, t11: dict) -> list[str]:
    out = []
    w = w5.set_index("macro_state_at_entry")
    for st in FIVE_STATES_T:
        for c in FIVE_COLS_T:
            a, b = w.loc[st, f"tc11_{c}"], t11[st][c]
            if c in ("n", "n_assets", "n_in_range"):
                ok = int(a) == int(b)
            elif c == "provisional":
                ok = bool(a) == bool(b)
            else:
                ok = _close(a, b, ROUND6_HALF)
            if not ok:
                out.append(f"R5-FIVE-ROW-TC11: {st}.{c} written {_py(a)!r} != re-derived here "
                           f"{_py(b)!r}")
    return out


def anchor_break():
    j, f5, _ = anchor_inputs()

    def mfe_swapped():
        w5 = written("R5_FIVE_ROW")
        w5["tc11_median_mfe_r"] = w5["tc11_median_net_r"]
        return five_tc11_findings(w5, typed_five(written("NEST_v6")))
    return plants([
        ("a one-bar-late state read (entry close + 4h)", "R5-ANCHOR",
         lambda: anchor_cmp(SR.five_row(j, shift_ms=MS4H), f5)),
        ("the state read at the entry bar's OPEN (entry close - 4h)", "R5-ANCHOR",
         lambda: anchor_cmp(SR.five_row(j, shift_ms=-MS4H), f5)),
        ("the calibrated scale in place of frozen 3.0", "R5-ANCHOR",
         lambda: anchor_cmp(SR.five_row(j, scale_kind="calibrated"), f5)),
        ("R5_FIVE_ROW's tc11_median_mfe_r replaced by the median net R on a copy",
         "R5-FIVE-ROW-TC11", mfe_swapped),
    ])


def anchor_real():
    j, f5, bad = anchor_inputs()
    f = list(bad)
    f += anchor_cmp(SR.five_row(j), f5)
    w5 = written("R5_FIVE_ROW")
    wi = w5.set_index("macro_state_at_entry")
    fb = f5.set_index("macro_state_at_entry")
    for st in FIVE_STATES_T:
        for c in FIVE_COLS_T:
            a, b = wi.loc[st, f"tc10_{c}"], fb.loc[st, c]
            if c == "provisional":
                ok = bool(a) == bool(b)
            else:
                ok = (_isna(a) and _isna(b)) or (not _isna(a) and not _isna(b)
                                                 and float(a) == float(b))
            if not ok:
                f.append(f"R5-FIVE-ROW-TC10: {st}.{c} written {a!r} != filed {b!r}")
    t11 = typed_five(written("NEST_v6"))
    f += five_tc11_findings(w5, t11)
    r5 = written("R5_CHOP")
    z = r5[(r5["scale_kind"] == "frozen3.0") & (r5["lens"] == "4h")].set_index("bucket")
    inr = int(sum(int(z.loc[b, "n"]) for b in DEC_T + ("<0", ">=100")))
    part = {"NEUTRAL": inr, "BULL_EXP": int(z.loc["not-in-range:BULL_EXP", "n"]),
            "BEAR_EXP": int(z.loc["not-in-range:BEAR_EXP", "n"]),
            "NONE": int(z.loc["not-in-range:NONE", "n"]), "__ALL__": int(z.loc["__ALL__", "n"])}
    for st, v in part.items():
        if int(wi.loc[st, "tc11_n"]) != v:
            f.append(f"R5-PARTITION: R5_CHOP frozen 4h {st} n {v} != five-row {wi.loc[st, 'tc11_n']}")
    t11n = {k: t11[k]["n"] for k in FIVE_STATES_T}
    return (not f), (f"the filed TC10 journal (typed sha, {len(j)} campaigns, all inside the TC10 "
                     f"window) re-stamped with the TC11 nest (frozen 3.0, 4h, entry close) "
                     f"reproduces TC10's five-row table exactly on {len(FIVE_COLS_T)} columns x "
                     f"{len(FIVE_STATES_T)} rows (n {dict((k, FIVE_N_T[k]) for k in FIVE_STATES_T)}); "
                     f"R5_FIVE_ROW's tc10_* columns (all {len(FIVE_COLS_T)}) == the filed table; "
                     f"its tc11_* columns (all {len(FIVE_COLS_T)}) == this file's own crosstab of "
                     f"NEST_v6's frozen-3.0 entry rows and the books' net_r / mfe_r (n {t11n}; "
                     f"6-dp bound); R5_CHOP frozen 4h partitions them {part}"
                     + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-CHOP-VALUE
def typed_bucket(state: str, pct: float) -> str:
    if state != "IN_RANGE":
        return f"not-in-range:{state}"
    if pct < 0:
        return "<0"
    if pct >= 100:
        return ">=100"
    d = int(np.floor(pct / 10.0))
    return f"[{10 * d},{10 * d + 10})"


def typed_coin(top, bot, L: str) -> str:
    if L == "1w":
        return "NA"
    t, b = bool(top), bool(bot)
    return "both" if (t and b) else "top" if t else "bot" if b else "none"


def typed_entries(book: str, nest: pd.DataFrame | None = None) -> pd.DataFrame:
    """The ENTRY rows of the written NEST_<book> + the book's net_r, with the typed
    era, in-sample and stability flags per consumed-lens set (from the FILED picks)."""
    nest = written(f"NEST_{book}") if nest is None else nest
    camp = pd.read_parquet(str(E.OUT / "books" / f"{book}_campaigns.parquet"))
    e = nest[nest["instant_kind"] == "entry"].merge(
        camp[["symbol", "entry_ms", "net_r"]], on=["symbol", "entry_ms"], how="left",
        validate="m:1").reset_index(drop=True)
    e["_hold"] = e["entry_close_ms"].astype(np.int64) > ERA_CUT_T
    return e


def _typed_flags(z: pd.DataFrame, lenses: tuple, kind: str) -> tuple[np.ndarray, np.ndarray]:
    if kind != "calibrated":
        return np.zeros(len(z), bool), np.zeros(len(z), bool)
    tun = (z["entry_close_ms"].astype(np.int64) <= ERA_CUT_T).to_numpy(bool)
    isin = np.zeros(len(z), bool)
    stab = np.zeros(len(z), bool)
    for L in lenses:
        fb = np.array([_pick_fallback(s, L) for s in z["symbol"]], dtype=bool)
        ch = np.array([_pick_changed(s, L) for s in z["symbol"]], dtype=bool)
        isin |= tun | fb
        stab |= ch
    return isin, stab


def _cell_stats(net: np.ndarray) -> dict:
    n = len(net)
    return {"n": n, "mean_net_r": float(net.mean()) if n else np.nan,
            "p_win": float((net > 0).mean()) if n else np.nan,
            "sum_net_r": float(net.sum()) if n else np.nan}


def typed_cells(book_entries: dict) -> dict:
    """{table: {cell: expected values}} for R5_CHOP and the three NEST_GRID tables."""
    exp = {"R5_CHOP": {}, "NEST_GRID_FREQ": {}, "NEST_GRID_BY_STATE": {}, "NEST_GRID_BY_COIN": {}}
    for book, e in book_entries.items():
        for kind in SCALES_T:
            z = e[e["scale_kind"] == kind].reset_index(drop=True)
            net = z["net_r"].to_numpy(float)
            hold = z["_hold"].to_numpy(bool)
            n_all = len(z)

            def cellv(m, isin, stab):
                d = _cell_stats(net[m])
                h = _cell_stats(net[m & hold])
                d.update({"n_scale_in_sample": int((isin & m).sum()),
                          "n_stability_changed": int((stab & m).sum()),
                          "n_holdout": h["n"], "mean_net_r_holdout": h["mean_net_r"],
                          "p_win_holdout": h["p_win"], "sum_net_r_holdout": h["sum_net_r"]})
                return d
            if book == "v6":
                for L in R5_LENSES_T:
                    b = np.array([typed_bucket(s, p) for s, p in
                                  zip(z[f"{L}_state"].astype(str), z[f"{L}_pct"].astype(float))],
                                 dtype=object)
                    isin, stab = _typed_flags(z, (L,), kind)
                    for bk in R5_BUCKETS_T:
                        m = np.ones(n_all, bool) if bk == "__ALL__" else (b == bk)
                        exp["R5_CHOP"][f"{kind}|{L}|{bk}"] = cellv(m, isin, stab)
            for L in NEST_LENSES_T:
                st = z[f"{L}_state"].astype(str).to_numpy()
                U = LADDER_T[L]
                lc = (L, U) if U is not None else (L,)
                isin_c, stab_c = _typed_flags(z, lc, kind)
                isin_s, stab_s = _typed_flags(z, (L,), kind)
                cats = ("NA",) if L == "1w" else COIN_CATS_T
                for rule, sfx in (("record", ""), ("mem_twin", "_mem")):
                    cc = np.array([typed_coin(t, b2, L) for t, b2 in
                                   zip(z[f"{L}_coin_top{sfx}"], z[f"{L}_coin_bot{sfx}"])],
                                  dtype=object) if L != "1w" else np.array(["NA"] * n_all,
                                                                           dtype=object)
                    for s4 in STATES_T:
                        for c in cats:
                            m = (st == s4) & (cc == c)
                            exp["NEST_GRID_FREQ"][f"{book}|{kind}|{L}|{rule}|{s4}|{c}"] = {
                                "n": int(m.sum()), "n_entries": n_all,
                                "share": float(m.sum()) / n_all,
                                "n_scale_in_sample": int((isin_c & m).sum()),
                                "n_stability_changed": int((stab_c & m).sum()),
                                "n_holdout": int((hold & m).sum())}
                    for c in cats:
                        exp["NEST_GRID_BY_COIN"][f"{book}|{kind}|{L}|{rule}|{c}"] = \
                            cellv(cc == c, isin_c, stab_c)
                for s4 in STATES_T + ("__ALL__",):
                    m = np.ones(n_all, bool) if s4 == "__ALL__" else (st == s4)
                    exp["NEST_GRID_BY_STATE"][f"{book}|{kind}|{L}|{s4}"] = \
                        cellv(m, isin_s, stab_s)
    return exp


CHOP_INT_T = ("n", "n_entries", "n_scale_in_sample", "n_stability_changed", "n_holdout")


def chop_findings(T: dict, exp: dict) -> tuple[list[str], int]:
    out, n = [], 0
    for name, want in exp.items():
        tag = "CHOP-VALUE" if name == "R5_CHOP" else "GRID-VALUE"
        d = T[name].set_index("cell")
        for cell, ev in want.items():
            if cell not in d.index:
                out.append(f"{tag}: {name} lacks the cell {cell}")
                continue
            r = d.loc[cell]
            for c, v in ev.items():
                n += 1
                a = r[c]
                ok = (int(a) == int(v)) if c in CHOP_INT_T else _close(a, v, ROUND8_HALF)
                if not ok:
                    out.append(f"{tag}: {name} {cell} {c} written {_py(a)!r} != re-derived "
                               f"here {_py(v)!r}")
    return out, n


def _module_tables(entries: dict) -> dict:
    """The module's R5 / grid code re-run on the WRITTEN entries (the plant seam),
    canonicalised the way the build files them."""
    G = SR.nest_grid(entries)
    T = {k: SR.canon(v, SR.KEYS[k]) for k, v in G.items()}
    T["R5_CHOP"] = SR.canon(SR.r5_chop(entries["v6"]), SR.KEYS["R5_CHOP"])
    return T


def _sr_entries(mod=None) -> dict:
    out = {}
    for b in BOOKS_T:
        camp = pd.read_parquet(str(E.OUT / "books" / f"{b}_campaigns.parquet"))
        nest = written(f"NEST_{b}")
        if mod is not None:
            nest = mod(b, nest)
        out[b] = SR.entry_frame(nest, camp)
    return out


def chop_break():
    exp = typed_cells({b: typed_entries(b) for b in BOOKS_T})

    def run(entries):
        return chop_findings(_module_tables(entries), exp)[0]

    orig_bucket, orig_coin, orig_stats = SR.bucket_of, SR.coin_cat, SR._stats

    def mirror():
        def f(state, pct):
            out = orig_bucket(state, pct)
            return np.array([x if x not in SR.DECILES else SR.DECILES[9 - SR.DECILES.index(x)]
                             for x in out], dtype=object)
        with mutated(SR, "bucket_of", f):
            return [x for x in run(_sr_entries()) if "R5_CHOP" in x]

    def swap():
        def f(top, bot, lens):
            return orig_coin(bot, top, lens)
        with mutated(SR, "coin_cat", f):
            return [x for x in run(_sr_entries()) if "NEST_GRID" in x]

    def median():
        def f(net):
            d = orig_stats(net)
            if d["n"]:
                d["mean_net_r"] = float(np.median(np.asarray(net, dtype=float)))
            return d
        with mutated(SR, "_stats", f):
            return run(_sr_entries())

    def pct12_on_4h():
        def mod(b, nest):
            nest = nest.copy()
            nest["12h_pct"] = nest["4h_pct"]
            nest["12h_state"] = nest["4h_state"]
            return nest
        return [x for x in run(_sr_entries(mod)) if "R5_CHOP" in x]

    def labels_dropped():
        def mod(b, nest):
            nest = nest.copy()
            nest["4h_scale_in_sample"] = pd.array([False] * len(nest), dtype="boolean")
            return nest
        return [x for x in run(_sr_entries(mod)) if "n_scale_in_sample" in x]

    return plants([
        ("deciles mirrored (SR.bucket_of mutated), R5 re-run on the written entries",
         "CHOP-VALUE", mirror),
        ("coincidence top / bot swapped (SR.coin_cat mutated), the grids re-run", "GRID-VALUE",
         swap),
        ("the mean replaced by the median (SR._stats mutated), R5 and the grids re-run",
         "VALUE", median),
        ("the 12h table bucketed on the 4h state / pct (a copy of the entries)", "CHOP-VALUE",
         pct12_on_4h),
        ("the 4h in-sample labels dropped (a copy of the entries)", "VALUE", labels_dropped),
    ])


def chop_real():
    exp = typed_cells({b: typed_entries(b) for b in BOOKS_T})
    T = {n: written(n) for n in exp}
    f, n = chop_findings(T, exp)
    cnt = {k: len(v) for k, v in exp.items()}
    return (not f), (f"every cell re-derived HERE from the written NEST entry rows and the books' "
                     f"net_r by the typed bucket / coincidence / honesty laws {cnt}: {n} values "
                     f"(n, mean, P(win), ΣR, the holdout slice, n_scale_in_sample, "
                     f"n_stability_changed, FREQ n / share) == the written tables (counts exact, "
                     f"floats to the 8-dp bound)" + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-NEST-BOOK
def typed_instants(camp: pd.DataFrame) -> tuple[dict, list[str]]:
    """{(symbol, entry_ms, kind): sorted instants} by the law typed HERE from the raw
    4h tape (N.load11: the snapshot's 4h file, closes <= the pin) — the books path."""
    exp, bad = {}, []
    for s in sorted(camp["symbol"].unique()):
        tape = N.load11(s, "4h")
        t0, h, l = tape.t0.astype(np.int64), tape.h, tape.l
        pos = {int(x): i for i, x in enumerate(t0)}
        for _, r in camp[camp["symbol"] == s].iterrows():
            em = int(r["entry_ms"])
            ei, ai, xi = pos[em], pos[int(r["arm_open_ms"])], pos[int(r["exit_ms"])]
            if int(t0[ei]) + MS4H != int(r["entry_close_ms"]) or \
                    int(t0[ai]) + MS4H != int(r["arm_close_ms"]):
                bad.append(f"INSTANT-SET: {s} {em}: the table's closes are not the tape's")
            stop = str(r["exit_reason"]) == "stop"
            last = xi - 1 if stop else xi
            k = (s, em)
            exp[k + ("bar_close",)] = [int(t0[q]) + MS4H for q in range(ai, last + 1)]
            exp[k + ("arm",)] = [int(t0[ai]) + MS4H]
            exp[k + ("entry",)] = [int(t0[ei]) + MS4H]
            d, R, ep = int(r["direction"]), float(r["r_dist"]), float(r["entry_px"])
            j1 = next((q for q in range(ei + 1, xi + 1)
                       if ((h[q] if d == 1 else l[q]) - ep) * d / R >= 1.0), None)
            if (j1 is not None) != bool(r["reached_1r"]):
                bad.append(f"INSTANT-SET: {s} {em}: the typed +1R bar {j1} vs reached_1r "
                           f"{bool(r['reached_1r'])}")
            if j1 is not None:
                exp[k + ("plus_1r",)] = [int(t0[j1])]
                exp[k + ("plus_1r_post_event",)] = [int(t0[j1]) + MS4H]
            if bool(r["harvested"]):
                exp[k + ("harvest",)] = [int(t0[int(r["harvest_i"])]) + MS4H]
            reason = str(r["exit_reason"])
            if reason.startswith("bell"):
                exp[k + ("bell",)] = [int(t0[xi]) + MS4H]
            if reason.startswith("corridor_end"):
                exp[k + ("as_of_pin",)] = [int(t0[xi]) + MS4H]
            else:
                exp[k + ("exit",)] = [int(t0[xi]) if stop else int(t0[xi]) + MS4H]
            if stop:
                exp[k + ("exit_post_event",)] = [int(t0[xi]) + MS4H]
    return exp, bad


def instant_findings(nest: pd.DataFrame, exp: dict, tag: str = "") -> list[str]:
    out = []
    for sc in SCALES_T:
        z = nest[nest["scale_kind"] == sc]
        got = {k: sorted(int(x) for x in g["instant_ms"]) for k, g in
               z.groupby(["symbol", "entry_ms", "instant_kind"], sort=True)}
        got = {(str(a), int(b), str(c)): v for (a, b, c), v in got.items()}
        for k in sorted(set(exp) | set(got)):
            a, b = got.get(k), exp.get(k)
            if a == b:
                continue
            det = "STAMP" if k[2] in ("plus_1r", "exit", "exit_post_event",
                                      "plus_1r_post_event", "as_of_pin") else "INSTANT-SET"
            miss = sorted(set(b or []) - set(a or []))
            extra = sorted(set(a or []) - set(b or []))
            out.append(f"{tag}{det}: {sc} {k[0]} {k[1]} {k[2]}: typed-law instants missing "
                       f"{miss[:3]} ({len(miss)}), written but not in the law {extra[:3]} "
                       f"({len(extra)})")
    return out


def _cell_equal(a: pd.Series, b: pd.Series) -> np.ndarray:
    na, nb = a.isna().to_numpy(), b.isna().to_numpy()
    av, bv = a.astype(object).to_numpy(), b.astype(object).to_numpy()
    eq = np.array([(x == y) if not (p or q) else (p and q)
                   for x, y, p, q in zip(av, bv, na, nb)], dtype=bool)
    return eq


def nest_value_findings(nest: pd.DataFrame) -> tuple[list[str], int]:
    """JOIN INTEGRITY [verifier MINOR-7]: the written nest columns == N.nest_at at the
    same instants — the SAME function the module calls, so this proves the join and
    the write (no row moved, no column shifted), NOT the values' causality; that is
    prefix_findings'."""
    out, cells = [], 0
    cols = [f"{L}_{f}" for L in NEST_LENSES_T for f in NEST_FIELDS_T]
    for sc in SCALES_T:
        for s in sorted(nest["symbol"].unique()):
            z = nest[(nest["scale_kind"] == sc) & (nest["symbol"] == s)].reset_index(drop=True)
            u = np.unique(z["instant_ms"].to_numpy(np.int64))
            nv = N.nest_at(s, u, sc).set_index("instant_ms")
            ref = nv.loc[z["instant_ms"].to_numpy(np.int64)].reset_index(drop=True)
            for c in cols:
                eq = _cell_equal(z[c], ref[c])
                cells += len(eq)
                if not eq.all():
                    i = int(np.nonzero(~eq)[0][0])
                    out.append(f"NEST-VALUE: {sc} {s} {c}: {int((~eq).sum())} cell(s) differ from "
                               f"N.nest_at, e.g. instant {int(z['instant_ms'].iloc[i])} written "
                               f"{z[c].iloc[i]} vs {ref[c].iloc[i]}")
    return out, cells


def prefix_sample(camp: pd.DataFrame) -> list[int]:
    rng = np.random.default_rng(SEED)
    return sorted(int(i) for i in rng.choice(len(camp), PREFIX_N_T, replace=False))


def prefix_findings(nest: pd.DataFrame, camp: pd.DataFrame) -> tuple[list[str], int]:
    """THE CAUSAL CHECK [L-R.5; verifier MINOR-7]: at the ENTRY instant of each
    sampled campaign, per L in {4h, 12h} and both scales, the written read equals a
    run of the machine on the tape CUT at the read bar k (tape.head(k + 1): no later
    bar exists, so nothing can leak) — the scale the filed pick (calibrated) or the
    typed 3.0 (frozen)."""
    out, n = [], 0
    picks = picks_filed()
    for i in prefix_sample(camp):
        r = camp.iloc[i]
        s, inst = str(r["symbol"]), int(r["entry_close_ms"])
        for kind in SCALES_T:
            row = nest[(nest["scale_kind"] == kind) & (nest["symbol"] == s)
                       & (nest["entry_ms"] == int(r["entry_ms"]))
                       & (nest["instant_kind"] == "entry")]
            if len(row) != 1:
                out.append(f"PREFIX: {s} {inst}: {len(row)} entry rows at {kind}")
                continue
            row = row.iloc[0]
            for L in PREFIX_LENSES_T:
                tape = N.load11(s, L)
                closes = (tape.t0 + tape.step).astype(np.int64)
                k = int(np.searchsorted(closes, inst, side="right")) - 1
                pre = tape.head(k + 1)
                sc = float(picks[(s, L)]["pick_of_record"]) if kind == "calibrated" else FROZEN_T
                v2 = C.run_scale(pre, sc)
                vw = C.asof_view(pre, v2["macro"], v2["leash"])
                inr = bool(vw["in_range"][k])
                want = {"state": "IN_RANGE" if inr else STATE_CODE_T[int(vw["state"][k])],
                        "bar_close_ms": int(closes[k]),
                        "pct": float(vw["pct"][k]) if inr else np.nan,
                        "top": float(vw["top"][k]) if inr else np.nan,
                        "bot": float(vw["bot"][k]) if inr else np.nan,
                        "atr_L": float(pre.atr[k])}
                for c, v in want.items():
                    n += 1
                    a = row[f"{L}_{c}"]
                    ok = (a == v) if isinstance(v, str) else (
                        (int(a) == v) if c == "bar_close_ms" else
                        ((_isna(a) and np.isnan(v)) or (not _isna(a) and float(a) == v)))
                    if not ok:
                        out.append(f"PREFIX: {kind} {s} entry {inst} {L}_{c} written "
                                   f"{_py(a)!r} != the prefix run's {_py(v)!r}")
    return out, n


def cli_findings(out_dir: Path) -> list[str]:
    """PLUMBING [verifier MINOR-7]: the nest-book door run as the lanes pass runs it
    (the CLI, a fresh interpreter) == the in-process door (the filed table), and
    == NEST_v6 outside stamp_law (the books path names its unwalked 4h law) — not an
    independent value check (both paths share instants_of / nest_frame)."""
    out = []
    r = subprocess.run([PY, "-B", str(ROOT / "scripts" / "tierc11_stage_r.py"), "nest-book",
                        "--regbook", str(OUT / "nestbook_probe" / "V6-PROBE"), "--arm", "base",
                        "--kind", "v6transform", "--out", str(out_dir)],
                       env=_env(), capture_output=True, text=True, cwd=str(ROOT), timeout=1800)
    if r.returncode != 0:
        return [f"NEST-BOOK-CLI: exit {r.returncode}: {r.stderr.strip()[-300:]}"]
    got = pd.read_parquet(str(out_dir / "V6-PROBE__base.parquet"))
    rec = written("nest_books/V6-PROBE__base")
    if C.content_sha(got) != C.content_sha(rec):
        out.append("NEST-BOOK-CLI: the CLI's table != the filed nest_books/V6-PROBE__base")
    v6 = written("NEST_v6")
    a = got.drop(columns=["registration", "arm", "stamp_law"]).sort_values(NEST_KEY_T,
                                                                           kind="mergesort")
    b = v6.drop(columns=["book", "stamp_law"]).sort_values(NEST_KEY_T, kind="mergesort")
    if list(a.columns) != list(b.columns) or \
            C.content_sha(a.reset_index(drop=True)) != C.content_sha(b.reset_index(drop=True)):
        out.append("NEST-BOOK-CLI: the door's table on the v6 probe != NEST_v6 (R3's own) "
                   "outside stamp_law")
    return out


def stripped_probe(camp: pd.DataFrame) -> pd.DataFrame:
    """The v6 probe WITHOUT its stamp and harvest columns (arm_close_ms,
    latch_stamp_ms, latch_post_event_ms, exit_stamp_ms, harvest_close_ms), reached_1r
    and harvested added: the door must then take v6's arm and harvest by the pairing
    key, derive the exit stamp from exit_reason and the +1R by the bar-OPEN law — the
    paths a later regbook without those columns takes."""
    reg = SR.regframe_from_campaigns(camp).drop(
        columns=["arm_close_ms", "latch_stamp_ms", "latch_post_event_ms", "exit_stamp_ms",
                 "harvest_close_ms"])
    return reg.merge(camp[["symbol", "entry_ms", "reached_1r", "harvested"]],
                     on=["symbol", "entry_ms"], how="left", validate="1:1")


def derived_findings(camp: pd.DataFrame, exp: dict) -> tuple[list[str], dict]:
    inst, src = SR.instants_of(stripped_probe(camp), "v6transform")
    both = pd.concat([inst.assign(scale_kind=k) for k in SCALES_T], ignore_index=True)
    return instant_findings(both, exp), src


# ── the door on REAL regbooks (read-only; outputs to a temp dir) ────────────────
def _holding_open(ms: int) -> int:
    """the OPEN of the 4h bar holding the instant `ms` (a close of that bar or of
    one of its 1h children)."""
    return ((int(ms) + MS4H - 1) // MS4H) * MS4H - MS4H


def _mism(x) -> set:
    if x is None:
        return set()
    if isinstance(x, (list, tuple, np.ndarray)):
        return {int(v) for v in x}
    if isinstance(x, str):
        return {int(t) for t in re.findall(r"\d+", x)}
    return set() if _isna(x) else {int(x)}


def typed_door_instants(reg: pd.DataFrame, kind: str) -> tuple[dict, list[str]]:
    """THE DOOR'S LAW typed HERE for a regbook (4h kinds v6transform / lane4h /
    relay): 4h closes from the start (the arm close; the entry close for lane4h)
    through the exit stamp (exit_stamp_ms as filed; else a stop -> the OPEN of the 4h
    bar holding exit_close_ms, a close reason -> exit_close_ms); arm / entry /
    harvest / bell at their close; +1R: latch_1h_ms (gated by latched_1h) at the
    child's close, or — its parent bar listed in walk_mismatch_ms — at the parent's
    OPEN with the close as twin; else, reached_1r, the OPEN of the first 4h bar in
    (entry, exit] reaching +1R on the raw tape, the close as twin; harvest: harvest_i
    / harvest_ms / (v6transform) v6's harvest_close_ms from books/, when harvested;
    corridor_end -> as_of_pin; an exit stamp before exit_close_ms -> the twin."""
    exp, bad = {}, []
    cols = set(reg.columns)
    v6 = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    v6k = {(str(a), int(b)): (int(c), bool(h), (None if _isna(hc) else int(hc)))
           for a, b, c, h, hc in zip(v6["symbol"], v6["entry_ms"], v6["arm_close_ms"],
                                     v6["harvested"], v6["harvest_close_ms"])}
    for s in sorted(reg["symbol"].unique()):
        tape = N.load11(s, "4h")
        t0 = tape.t0.astype(np.int64)
        closes = t0 + MS4H
        pos = {int(c): i for i, c in enumerate(closes)}
        h, l = tape.h, tape.l
        for _, r in reg[reg["symbol"] == s].iterrows():
            k = (s, int(r["entry_ms"]))
            enc, ec = int(r["entry_close_ms"]), int(r["exit_close_ms"])
            reason = str(r["exit_reason"])
            intrabar = reason in ("stop", "tp", "target")
            if "exit_stamp_ms" in cols:
                ex = int(r["exit_stamp_ms"])
                if ex > ec or ex % MS1H:
                    bad.append(f"DOOR-LAW: {s} {enc}: exit_stamp_ms {ex} is not a 1h instant "
                               f"at or before exit_close_ms {ec}")
            else:
                ex = _holding_open(ec) if intrabar else ec
                if "exit_event_ms" in cols and int(r["exit_event_ms"]) != ex:
                    bad.append(f"DOOR-LAW: {s} {enc}: exit_event_ms {int(r['exit_event_ms'])} != "
                               f"the typed exit stamp {ex}")
            if kind == "lane4h":
                start = None
            elif "arm_close_ms" in cols:
                start = int(r["arm_close_ms"])
            elif "window_arm_close_ms" in cols:
                start = int(r["window_arm_close_ms"])
            elif "arm_ms" in cols:
                start = int(r["arm_ms"]) + MS4H
            else:
                start = v6k[k][0]
            first = enc if start is None else start
            exp[k + ("bar_close",)] = [int(c) for c in closes if first <= c <= ex]
            if start is not None:
                exp[k + ("arm",)] = [start]
            exp[k + ("entry",)] = [enc]
            if "latch_1h_ms" in cols:
                lat = r["latch_1h_ms"]
                on = ("latched_1h" not in cols) or (not _isna(r["latched_1h"])
                                                    and bool(r["latched_1h"]))
                if not _isna(lat) and on:
                    lat = int(lat)
                    mm = _mism(r["walk_mismatch_ms"]) if "walk_mismatch_ms" in cols else set()
                    if lat % MS4H == 0 and (lat - MS4H) in mm:
                        exp[k + ("plus_1r",)] = [lat - MS4H]
                        exp[k + ("plus_1r_post_event",)] = [lat]
                    else:
                        exp[k + ("plus_1r",)] = [lat]
            elif "reached_1r" in cols and kind in ("v6transform", "lane4h"):
                ei = pos[enc]
                xi = int(np.searchsorted(closes, ec, side="left"))
                d, R, ep = int(r["direction"]), float(r["r_dist"]), float(r["entry_px"])
                j1 = next((q for q in range(ei + 1, min(xi, len(closes) - 1) + 1)
                           if ((h[q] if d == 1 else l[q]) - ep) * d / R >= 1.0), None)
                if (j1 is not None) != bool(r["reached_1r"]):
                    bad.append(f"DOOR-LAW: {s} {enc}: the typed +1R bar {j1} vs reached_1r "
                               f"{bool(r['reached_1r'])}")
                if j1 is not None:
                    exp[k + ("plus_1r",)] = [int(t0[j1])]
                    exp[k + ("plus_1r_post_event",)] = [int(t0[j1]) + MS4H]
            if "harvested" in cols and bool(r["harvested"]):
                if "harvest_i" in cols:
                    exp[k + ("harvest",)] = [int(closes[int(r["harvest_i"])])]
                elif "harvest_ms" in cols:
                    exp[k + ("harvest",)] = [int(r["harvest_ms"]) + MS4H]
                elif kind == "v6transform":
                    exp[k + ("harvest",)] = [v6k[k][2]]
            if reason.startswith("bell"):
                exp[k + ("bell",)] = [ec]
            if reason.startswith("corridor_end"):
                exp[k + ("as_of_pin",)] = [ex]
            else:
                exp[k + ("exit",)] = [ex]
                if ex < ec:
                    exp[k + ("exit_post_event",)] = [ec]
    return exp, bad


def typed_book_sha(df: pd.DataFrame) -> str:
    """The REGBOOK INTERFACE's book_sha256, typed HERE: sha256 of a canonical CSV of the
    required columns sorted by (symbol, entry_close_ms), floats at repr precision."""
    d = df[list(REGBOOK_REQ_T)].sort_values(["symbol", "entry_close_ms"],
                                            kind="mergesort").reset_index(drop=True)
    for c in REGBOOK_FLOATS_T:
        d[c] = [repr(float(x)) for x in d[c].to_numpy(float)]
    for c in ("entry_ms", "entry_close_ms", "exit_close_ms", "direction"):
        d[c] = d[c].astype(np.int64)
    return sha_bytes(d.to_csv(index=False, lineterminator="\n").encode("utf-8"))


def relay_copy(tmp: Path, plant_parent: bool = True) -> tuple[Path, int, int]:
    """A harvest-free copy of P-RELAY-1 scored (its harvested rows dropped), every
    latch that sits at a 4h close planted as PARENT-decided (walk_mismatch_ms names its
    parent bar), re-sidecar'd with the typed book_sha256 — a SYNTHETIC regbook for the
    relay / latch_1h_ms / parent-latch paths.  Returns (dir, n rows, n planted)."""
    d = pd.read_parquet(str(REGBOOKS / "P-RELAY-1" / "scored.parquet"))
    d = d[~d["harvested"].astype(bool)].reset_index(drop=True)
    npl = 0
    if plant_parent:
        lat = d["latch_1h_ms"]
        wm = []
        for x in lat:
            if not _isna(x) and int(x) % MS4H == 0:
                wm.append(str(int(x) - MS4H))
                npl += 1
            else:
                wm.append("")
        d["walk_mismatch_ms"] = wm
    reg = tmp / "FIX-RELAY-COPY"
    reg.mkdir(parents=True, exist_ok=True)
    d.to_parquet(str(reg / "scored.parquet"), index=False)
    meta = {"registration": "FIX-RELAY-COPY", "arm": "scored", "kind": "scored",
            "n": int(len(d)), "book_sha256": typed_book_sha(d),
            "description": "F-NEST-BOOK's synthetic copy of P-RELAY-1 scored (harvest-free, "
                           "parent latches planted) — never scored"}
    (reg / "scored.json").write_text(json.dumps(meta, indent=1, sort_keys=True), encoding="utf-8")
    return reg, int(len(d)), npl


def door_run(regdir: Path, arm: str, kind: str, out: Path) -> tuple[pd.DataFrame | None, str]:
    """SR.nest_book (the door) into `out`; (table, '') or (None, the HALT text)."""
    try:
        side = SR.nest_book(regdir, arm, kind, out)
    except SystemExit as e:
        return None, str(e)
    return pd.read_parquet(str(out / f"{side['registration']}__{arm}.parquet")), ""


def door_law_findings(tmp: Path) -> tuple[list[str], list[str]]:
    """The door on real regbooks, read-only (outputs in `tmp`), against the typed law;
    the two refusals with their typed UNSTAMPED counts."""
    f, tally = [], []
    for reg, kind in (("P-BRK-4H", "lane4h"), ("P-WARN-1", "v6transform")):
        src = REGBOOKS / reg
        df = pd.read_parquet(str(src / "scored.parquet"))
        exp, bad = typed_door_instants(df, kind)
        f += [x.replace("DOOR-LAW", f"DOOR-LAW {reg}") for x in bad]
        got, halt = door_run(src, "scored", kind, tmp / reg)
        if got is None:
            f.append(f"DOOR-REAL: {reg} scored ({kind}) HALTED: {halt[:200]}")
            continue
        f += instant_findings(got, exp, tag=f"DOOR-REAL {reg} ")
        kinds = got[got["scale_kind"] == "calibrated"]["instant_kind"].value_counts()
        tally.append(f"{reg} scored ({kind}, {len(df)} campaigns): "
                     + " · ".join(f"{a} {int(kinds.get(a, 0))}" for a in
                                  ("bar_close", "plus_1r", "harvest", "bell", "exit",
                                   "exit_post_event")))
    rc, n_rc, npl = relay_copy(tmp)
    exp, bad = typed_door_instants(pd.read_parquet(str(rc / "scored.parquet")), "relay")
    f += [x.replace("DOOR-LAW", "DOOR-LAW relay copy") for x in bad]
    got, halt = door_run(rc, "scored", "relay", tmp / "relay_out")
    if got is None:
        f.append(f"DOOR-REAL: the relay copy HALTED: {halt[:200]}")
    else:
        f += instant_findings(got, exp, tag="DOOR-REAL relay copy ")
        z = got[got["scale_kind"] == "calibrated"]
        tally.append(f"P-RELAY-1 scored harvest-free copy ({n_rc} campaigns, relay): plus_1r "
                     f"{int((z['instant_kind'] == 'plus_1r').sum())} of which {npl} planted "
                     f"parent-decided (stamped at the parent's OPEN, twin "
                     f"{int((z['instant_kind'] == 'plus_1r_post_event').sum())})")
    if npl < 2:
        f.append(f"DOOR-REAL: only {npl} parent latches could be planted (cardinality)")
    for reg, kind, what, col in (("P-RELAY-1", "relay", "harvest", "harvested"),
                                 ("P-ADD-BRK", "v6transform", "add", "n_adds")):
        df = pd.read_parquet(str(REGBOOKS / reg / "scored.parquet"))
        n_t = int(df[col].astype(bool).sum()) if col == "harvested" else int(df[col].sum())
        got, halt = door_run(REGBOOKS / reg, "scored", kind, tmp / f"refuse_{reg}")
        if got is not None or "UNSTAMPED" not in halt or f"{what} {n_t} " not in halt:
            f.append(f"DOOR-REFUSE: {reg} scored ({kind}) must HALT UNSTAMPED '{what} {n_t}' "
                     f"(typed from its {col}); got "
                     + ("a filed table" if got is not None else f"HALT {halt[:160]}"))
        else:
            tally.append(f"{reg} scored REFUSED: UNSTAMPED {what} {n_t} (typed from its {col})")
    return f, tally


def nestbook_break():
    camp = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    exp, _ = typed_instants(camp)

    def derived_close_stamped():
        with mutated(SR, "INTRABAR_STAMP", "bar_close"):
            return derived_findings(camp, exp)[0]

    def close_stamped():
        with mutated(SR, "INTRABAR_STAMP", "bar_close"):
            f = SR.book_nest(camp, "v6")
        return instant_findings(f, exp)

    def late_read():
        d = written("NEST_v6")
        m = (d["scale_kind"] == "calibrated") & (d["symbol"] == "BTCUSDT")
        inst = d.loc[m, "instant_ms"].to_numpy(np.int64)
        nv = N.nest_at("BTCUSDT", np.unique(inst + MS4H), "calibrated").set_index("instant_ms")
        ref = nv.loc[inst + MS4H].reset_index(drop=True)
        cols = [f"{L}_{f}" for L in NEST_LENSES_T for f in NEST_FIELDS_T]
        for c in cols:
            d.loc[m, c] = ref[c].to_numpy()
        return nest_value_findings(d[m])[0]

    def leaked_prefix():
        d = written("NEST_v6")
        for i in prefix_sample(camp):
            r = camp.iloc[i]
            s, inst = str(r["symbol"]), int(r["entry_close_ms"])
            for kind in SCALES_T:
                m = ((d["scale_kind"] == kind) & (d["symbol"] == s)
                     & (d["entry_ms"] == int(r["entry_ms"])) & (d["instant_kind"] == "entry"))
                for L, step in (("4h", MS4H), ("12h", MS12H)):
                    nv = N.nest_at(s, np.array([inst + step]), kind).iloc[0]
                    for c in ("state", "bar_close_ms", "pct", "top", "bot", "atr_L"):
                        d.loc[m, f"{L}_{c}"] = nv[f"{L}_{c}"]
        return prefix_findings(d, camp)[0]

    def dropped():
        d = written("NEST_v6")
        i = d.index[d["instant_kind"] == "bar_close"][17]
        return instant_findings(d.drop(index=i), exp)

    def tampered():
        tmp = Path(tempfile.mkdtemp(prefix="f-nestbook-"))
        try:
            reg = tmp / "V6-PROBE"
            shutil.copytree(OUT / "nestbook_probe" / "V6-PROBE", reg)
            p = reg / "base.parquet"
            d = pd.read_parquet(str(p))
            d.loc[d.index[3], "net_r"] = float(d["net_r"].iloc[3]) + 1e-6
            d.to_parquet(str(p), index=False)
            SR.nest_book(reg, "base", "v6transform", tmp / "out")
            return []
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    def unstamped_harvest():
        SR.instants_of(stripped_probe(camp), "lane4h")
        return []

    def unstamped_add():
        reg = SR.regframe_from_campaigns(camp)
        reg["n_adds"] = 0
        reg.loc[reg.index[5], "n_adds"] = 1
        SR.instants_of(reg, "v6transform")
        return []

    def parent_off():
        tmp = Path(tempfile.mkdtemp(prefix="f-nestbook-relay-"))
        try:
            rc, _, _ = relay_copy(tmp)
            df = pd.read_parquet(str(rc / "scored.parquet"))
            ex, _ = typed_door_instants(df, "relay")
            with mutated(SR, "_parent_latch", lambda reg, lat, step: np.zeros(len(reg), bool)):
                inst, _ = SR.instants_of(df, "relay")
            both = pd.concat([inst.assign(scale_kind=k) for k in SCALES_T], ignore_index=True)
            f = instant_findings(both, ex)
            return ([f"STAMP: planted parent-decided latches of the relay copy are not stamped "
                     f"at the parent's OPEN with the close as twin (the typed law)"] if f else [])
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    return plants([
        ("intrabar events close-stamped (SR.INTRABAR_STAMP = 'bar_close')", "STAMP",
         close_stamped),
        ("the same on the DERIVED path (a stripped probe: arm, harvest, exit and +1R derived)",
         "STAMP", derived_close_stamped),
        ("a one-bar-late nest read on a copy (BTC, calibrated)", "NEST-VALUE", late_read),
        ("a leaked next-bar read at the sampled entries (4h / 12h, a copy)", "PREFIX",
         leaked_prefix),
        ("one bar_close instant dropped from a copy", "INSTANT-SET", dropped),
        ("a tampered probe regbook (one net_r + 1e-6) handed to the door", "book_sha256",
         tampered),
        ("a harvested regbook with no harvest instant (the stripped probe as lane4h: no "
         "pairing-key join)", "UNSTAMPED", unstamped_harvest),
        ("an n_adds > 0 campaign with no add instants", "UNSTAMPED", unstamped_add),
        ("the parent-latch law disabled (SR._parent_latch mutated) on the relay copy", "STAMP",
         parent_off),
    ])


def nestbook_real():
    f, tally = [], []
    cells = 0
    for book in BOOKS_T:
        camp = pd.read_parquet(str(E.OUT / "books" / f"{book}_campaigns.parquet"))
        if len(camp) != BOOK_N_T[book]:
            f.append(f"INSTANT-SET: {book} campaigns {len(camp)} != typed {BOOK_N_T[book]}")
        exp, bad = typed_instants(camp)
        f += bad
        nest = written(f"NEST_{book}")
        f += instant_findings(nest, exp)
        nf, nc = nest_value_findings(nest)
        f += nf
        cells += nc
        npin = int((nest["instant_kind"] == "as_of_pin").sum()) // len(SCALES_T)
        tally.append(f"{book} {len(nest)} rows / {len(camp)} campaigns ({npin} open at the pin)")
    camp = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    pf, npre = prefix_findings(written("NEST_v6"), camp)
    f += pf
    exp, _ = typed_instants(camp)
    df, dsrc = derived_findings(camp, exp)
    f += [x.replace("STAMP", "DERIVED-STAMP").replace("INSTANT-SET", "DERIVED-INSTANT-SET")
          for x in df]
    tmp = Path(tempfile.mkdtemp(prefix="f-nestbook-cli-"))
    try:
        f += cli_findings(tmp)
        df2, dt = door_law_findings(tmp)
        f += df2
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    for x in dt:
        note(x)
    return (not f), (f"{' · '.join(tally)}: every instant set == the typed law from the raw 4h "
                     f"tape at both scales (+1R and stop exits at their bar OPEN, twins at the "
                     f"close; corridor_end -> as_of_pin); JOIN integrity: {cells} nest cells == "
                     f"N.nest_at at those instants; CAUSAL: {npre} values (state, pct, top, bot, "
                     f"bar close, ATR) of {npre // 6} reads at the entries of {PREFIX_N_T} "
                     f"sampled v6 campaigns x {{4h, 12h}} x both scales == a machine run on the "
                     f"tape cut at the read bar; the nest-book CLI == the in-process "
                     f"door == NEST_v6 outside stamp_law (plumbing); the DERIVED path (arm and "
                     f"harvest by the pairing key, exit from exit_reason, +1R by the bar-OPEN "
                     f"law) == the typed law on every campaign; the door, read-only on real "
                     f"regbooks, == the law typed here: P-BRK-4H scored (lane4h: 4h closes from "
                     f"the entry, +1R derived, harvest_i, the exit stamp typed from exit_reason), "
                     f"P-WARN-1 scored (v6transform: arm_ms, v6's harvest by the pairing key, "
                     f"derived exit and +1R), a harvest-free copy of P-RELAY-1 scored (relay: "
                     f"window_arm_close_ms, exit_stamp_ms, latch_1h_ms at the 1h child's close; "
                     f"every latch at a 4h close planted parent-decided -> the parent's OPEN, "
                     f"twin at the close; >= 2 planted); P-RELAY-1 scored and P-ADD-BRK scored "
                     f"REFUSED with their typed UNSTAMPED harvest / add counts (the counts, "
                     f"other stages' data, on stdout only)"
                     + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-GRID
def declared() -> dict:
    r1 = [f"{s}|{l}" for s in C5_T for l in LENSES_T] + [f"{s}|{l}" for s in U12_T
                                                        for l in U_LENSES_T]
    panels = [(f"ASSET:{s}", l) for s in C5_T for l in LENSES_T] + \
             [(f"ASSET:{s}", l) for s in U12_T for l in U_LENSES_T] + \
             [(p, l) for p, (_, ls) in POOLS_T.items() for l in ls]
    r2 = [f"{p}|{l}|{e}|{k}|{t}" for p, l in panels for e in ERAS_T for k in SCALES_T
          for t in TOLLS_T]
    r5 = [f"{k}|{l}|{b}" for k in SCALES_T for l in R5_LENSES_T for b in R5_BUCKETS_T]
    fq, bs, bc = [], [], []
    for b in BOOKS_T:
        for k in SCALES_T:
            for L in NEST_LENSES_T:
                cats = ("NA",) if L == "1w" else COIN_CATS_T
                for rule in COIN_RULES_T:
                    fq += [f"{b}|{k}|{L}|{rule}|{s}|{c}" for s in STATES_T for c in cats]
                    bc += [f"{b}|{k}|{L}|{rule}|{c}" for c in cats]
                bs += [f"{b}|{k}|{L}|{s}" for s in STATES_T + ("__ALL__",)]
    return {"R1_LENSES": r1, "R2_FEASIBILITY": r2, "R5_CHOP": r5, "NEST_GRID_FREQ": fq,
            "NEST_GRID_BY_STATE": bs, "NEST_GRID_BY_COIN": bc}


DECL_N_T = {"R1_LENSES": 71, "R2_FEASIBILITY": 1458, "R5_CHOP": 64, "NEST_GRID_FREQ": 544,
            "NEST_GRID_BY_STATE": 100, "NEST_GRID_BY_COIN": 136}
TIER_E_TABLES = ("R1_LENSES", "NEST_v6", "NEST_trg912", "NEST_GRID_FREQ", "NEST_GRID_BY_STATE",
                 "NEST_GRID_BY_COIN", "R5_CHOP", "R5_FIVE_ROW", "nest_books/V6-PROBE__base")
STAT_TABLES = ("NEST_GRID_BY_STATE", "NEST_GRID_BY_COIN", "R5_CHOP")
LABELLED_TABLES = ("R5_CHOP", "NEST_GRID_FREQ", "NEST_GRID_BY_STATE", "NEST_GRID_BY_COIN")


def label_findings(T: dict) -> list[str]:
    """R1 against the FILED picks record (read here, a second object), R1's densities
    from its own printed counts and bars, and the R1 / R2 era partitions; R2's
    honesty labels [AM-4] against the filed pick windows and stability."""
    out = []
    by = picks_filed()
    r1 = T["R1_LENSES"]
    for _, r in r1.iterrows():
        c = by.get((r["asset"], r["lens"]))
        if c is None:
            out.append(f"R1-PICKS: no filed pick for {r['cell']}")
            continue
        for col in ("pick_of_record", "whole_tape_pick", "tuning_pick", "first_half_pick"):
            a, b = r[col], c[col]
            if not ((b is None and _isna(a)) or (b is not None and not _isna(a)
                                                  and float(a) == float(b))):
                out.append(f"R1-PICKS: {r['cell']} {col} {a!r} != filed {b!r}")
        if r["pick_window"] != c["pick_window"] or not bool(r["density_window_matches_filed"]):
            out.append(f"R1-PICKS: {r['cell']} window {r['pick_window']!r} / filed "
                       f"{c['pick_window']!r}; density matches filed "
                       f"{bool(r['density_window_matches_filed'])}")
        for sfx in ("", "frozen_"):
            if int(r[f"n_confirmed_{sfx}tuning"]) + int(r[f"n_confirmed_{sfx}holdout"]) != \
                    int(r[f"n_confirmed_{sfx}ALL"]):
                out.append(f"PARTITION: R1 {r['cell']} n_confirmed_{sfx}* tuning + holdout != ALL")
        if int(r["n_bars_tuning"]) + int(r["n_bars_holdout"]) != int(r["n_bars"]):
            out.append(f"PARTITION: R1 {r['cell']} bars tuning + holdout != n_bars")
        for era, nbc in (("ALL", "n_bars"), ("tuning", "n_bars_tuning"),
                         ("holdout", "n_bars_holdout")):
            nb = int(r[nbc])
            for sfx, dcol in (("", f"density_per_100_{era}"),
                              ("frozen_", f"density_frozen_per_100_{era}")):
                want = 100.0 * int(r[f"n_confirmed_{sfx}{era}"]) / nb if nb else float("nan")
                if not _close(r[dcol], want, ROUND8_HALF):
                    out.append(f"R1-DENSITY: {r['cell']} {dcol} {r[dcol]!r} != 100 x "
                               f"n_confirmed_{sfx}{era} / {nbc} = {want!r}")
    r2 = T["R2_FEASIBILITY"]
    for (p, l, k, t), g in r2.groupby(["panel", "lens", "scale_kind", "toll"]):
        a = g.set_index("era")
        if sorted(a.index) != sorted(ERAS_T):
            out.append(f"PARTITION: R2 {p}|{l}|{k}|{t} eras {sorted(a.index)} are not the "
                       f"typed {sorted(ERAS_T)}")
            continue
        for c in ("n_ranges", "edge_n"):
            if int(a.loc["tuning", c]) + int(a.loc["holdout", c]) != int(a.loc["ALL", c]):
                out.append(f"PARTITION: R2 {p}|{l}|{k}|{t} {c} tuning + holdout != ALL")
        mem = a["members"].iloc[0].split(",")
        fb = sorted(m for m in mem if by[(m, l)]["pick_window"] != "tuning") \
            if k == "calibrated" else []
        got = sorted(x for x in str(a["fallback_members"].iloc[0]).split(",") if x)
        if got != fb:
            out.append(f"LABELS: R2 {p}|{l}|{k}|{t} fallback_members {got} != filed {fb}")
        ch = sorted(m for m in mem if _pick_changed(m, l)) if k == "calibrated" else []
        for era in ERAS_T:
            gotc = sorted(x for x in str(a.loc[era, "stability_changed_members"]).split(",") if x)
            if gotc != ch:
                out.append(f"LABELS: R2 {p}|{l}|{era}|{k}|{t} stability_changed_members {gotc} "
                           f"!= filed {ch}")
        if not a["pooled"].iloc[0]:
            want = (by[(mem[0], l)]["pick_window"] if k == "calibrated" else "frozen3.0")
            if a["pick_window"].iloc[0] != want:
                out.append(f"LABELS: R2 {p}|{l}|{k}|{t} pick_window {a['pick_window'].iloc[0]!r} "
                           f"!= {want!r}")
    return out


def honesty_label_findings(T: dict) -> list[str]:
    """[AM-4, L-R.2] each R5 / NEST_GRID row's lens labels == the FILED picks of the
    lenses it consumes (L; L+1 for a coincidence cell), over the book's assets."""
    out = []
    syms = {b: sorted(set(written(f"NEST_{b}")["symbol"]), key=P17_T.index) for b in BOOKS_T}
    for name in LABELLED_TABLES:
        d = T[name]
        for _, r in d.iterrows():
            book = r["book"] if "book" in d.columns else "v6"
            L = r["lens"]
            coin = name in ("NEST_GRID_FREQ", "NEST_GRID_BY_COIN")
            lens = (L, LADDER_T[L]) if (coin and LADDER_T[L] is not None) else (L,)
            cal = r["scale_kind"] == "calibrated"
            pw = "; ".join(f"{c}: " + (" / ".join(sorted({picks_filed()[(s, c)]["pick_window"]
                                                           for s in syms[book]}))
                                       if cal else "frozen3.0") for c in lens)
            sm = "; ".join(f"{c}: " + (",".join(s for s in syms[book] if _pick_changed(s, c))
                                       if cal else "") for c in lens)
            sm = "; ".join(x if not x.endswith(": ") else x + "none" for x in sm.split("; "))
            want = {"lenses_read": "+".join(lens), "pick_window": pw,
                    "stability_changed_members": sm}
            for c, v in want.items():
                if r[c] != v:
                    out.append(f"HONESTY-LABEL: {name} {r['cell']} {c} {r[c]!r} != the filed "
                               f"picks' {v!r}")
    return out


def grid_findings(T: dict) -> tuple[list[str], list[str]]:
    out, lines = [], []
    out += label_findings(T)
    out += honesty_label_findings(T)
    D = declared()
    for name, dec in D.items():
        if len(dec) != DECL_N_T[name]:
            out.append(f"DECLARED: {name} typed product {len(dec)} != typed count {DECL_N_T[name]}")
        ok, ln = TP.grid_whole(dec, T[name], cell_col="cell", label=name)
        lines += ln
        if not ok:
            out += [x for x in ln if x.startswith("[BAD]")]
    for name in TIER_E_TABLES:
        d = T[name]
        for c, v in COLLAR_T.items():
            if c not in d.columns or not bool((d[c] == v).all()):
                out.append(f"COLLAR: {name}.{c} is not {v!r} on every row")
        vc = [c for c in VERDICT_COLS_T if c in d.columns]
        if vc:
            out.append(f"VERDICT-COLUMN: Tier-E table {name} carries {vc}")
    r2 = T["R2_FEASIBILITY"]
    rec = r2["is_lens_verdict_of_record"].astype(bool)
    for c in R2_RECORD_ONLY_T:
        if int(rec.sum()) != len(LENSES_T) or r2.loc[rec, c].isna().any() or \
                r2.loc[~rec, c].notna().any():
            out.append(f"VERDICT-COLUMN: R2 {c} must be non-null on exactly the "
                       f"{len(LENSES_T)} record rows")
    vc = [c for c in R2_BANNED_T if c in r2.columns]
    if vc:
        out.append(f"VERDICT-COLUMN: R2 carries verdict-named columns {vc}")
    for c in COLLAR_T:
        if not bool((r2.loc[~rec, c] == COLLAR_T[c]).all()) or \
                bool((r2.loc[rec, "tier"] == COLLAR_T["tier"]).any()):
            out.append(f"COLLAR: R2 {c} — Tier-E rows collared, record rows not")
    for name in STAT_TABLES:
        d = T[name]
        for ncol, sfx in (("n", ""), ("n_holdout", "_holdout")):
            z = d[ncol].astype(int) == 0
            for c in ("mean_net_r", "p_win", "sum_net_r"):
                cc = c + sfx
                if bool(d.loc[z, cc].notna().any()) or bool(d.loc[~z, cc].isna().any()):
                    out.append(f"NAN: {name}.{cc} is NaN under {ncol} > 0 or finite under "
                               f"{ncol} = 0")
    fq = T["NEST_GRID_FREQ"]
    for (b, k, L, r), g in fq.groupby(["book", "scale_kind", "lens", "coin_rule"]):
        if int(g["n"].sum()) != BOOK_N_T[b] or not bool((g["n_entries"] == BOOK_N_T[b]).all()):
            out.append(f"PARTITION: NEST_GRID_FREQ {b}|{k}|{L}|{r} sums {int(g['n'].sum())}, "
                       f"typed {BOOK_N_T[b]} entries")
    bs = T["NEST_GRID_BY_STATE"]
    for (b, k, L), g in bs.groupby(["book", "scale_kind", "lens"]):
        a = g.set_index("state")
        if int(a.loc[list(STATES_T), "n"].sum()) != int(a.loc["__ALL__", "n"]):
            out.append(f"PARTITION: NEST_GRID_BY_STATE {b}|{k}|{L} states do not sum to ALL")
        if int(a.loc["__ALL__", "n"]) != BOOK_N_T[b]:
            out.append(f"PARTITION: NEST_GRID_BY_STATE {b}|{k}|{L} ALL != {BOOK_N_T[b]}")
    bc = T["NEST_GRID_BY_COIN"]
    for (b, k, L, r), g in bc.groupby(["book", "scale_kind", "lens", "coin_rule"]):
        if int(g["n"].sum()) != BOOK_N_T[b]:
            out.append(f"PARTITION: NEST_GRID_BY_COIN {b}|{k}|{L}|{r}")
    r5 = T["R5_CHOP"]
    for (k, L), g in r5.groupby(["scale_kind", "lens"]):
        a = g.set_index("bucket")
        parts = int(a.loc[[x for x in R5_BUCKETS_T if x != "__ALL__"], "n"].sum())
        if parts != int(a.loc["__ALL__", "n"]) or parts != BOOK_N_T["v6"]:
            out.append(f"PARTITION: R5_CHOP {k}|{L} buckets sum {parts}")
    return out, lines


def _tables() -> dict:
    return {n: written(n) for n in ("R1_LENSES", "R2_FEASIBILITY", "R5_CHOP", "R5_FIVE_ROW",
                                    "NEST_GRID_FREQ", "NEST_GRID_BY_STATE", "NEST_GRID_BY_COIN",
                                    "NEST_v6", "NEST_trg912", "nest_books/V6-PROBE__base")}


def grid_break():
    T = _tables()

    def with_(name, fn):
        U = dict(T)
        U[name] = fn(T[name].copy())
        return grid_findings(U)[0]

    def verdict_col(d):
        d["verdict"] = "PASS"
        return d

    def nan_mean(d):
        i = d.index[d["n"].astype(int) > 0][0]
        d.loc[i, "mean_net_r"] = np.nan
        return d

    def nan_hold(d):
        i = d.index[d["n_holdout"].astype(int) > 0][0]
        d.loc[i, "mean_net_r_holdout"] = np.nan
        return d

    def plus_one(d):
        d.loc[d.index[5], "n"] = int(d["n"].iloc[5]) + 1
        return d

    def undeclared(d):
        x = d.iloc[[0]].copy()
        x["cell"] = "frozen3.0|4h|[100,110)"
        return pd.concat([d, x], ignore_index=True)

    def blank(d):
        d["tier"] = ""
        return d

    def pick_moved(d):
        d.loc[d.index[7], "pick_of_record"] = float(d["pick_of_record"].iloc[7]) + 0.25
        return d

    def density_all(d):
        d["density_per_100_holdout"] = 100.0 * d["n_confirmed_holdout"].astype(int) \
            / d["n_bars"].astype(int)
        return d

    def fallback_hidden(d):
        m = (d["lens"] == "1w") & (d["panel"] == "POOLED:CLASSIC5") & \
            (d["scale_kind"] == "calibrated")
        d.loc[m, "fallback_members"] = ""
        return d

    def stab_hidden(d):
        m = (d["lens"] == "12h") & (d["panel"] == "POOLED:CLASSIC5") & \
            (d["scale_kind"] == "calibrated")
        d.loc[m, "stability_changed_members"] = ""
        return d

    def pw_blank(d):
        d.loc[d["scale_kind"] == "calibrated", "pick_window"] = ""
        return d

    return plants([
        ("an R1 pick of record moved 0.25 on a copy", "R1-PICKS",
         lambda: with_("R1_LENSES", pick_moved)),
        ("R1's holdout density struck over ALL bars on a copy", "R1-DENSITY",
         lambda: with_("R1_LENSES", density_all)),
        ("the 1w record cell's fallback members hidden on a copy", "LABELS",
         lambda: with_("R2_FEASIBILITY", fallback_hidden)),
        ("the 12h record cell's stability-changed members hidden on a copy", "LABELS",
         lambda: with_("R2_FEASIBILITY", stab_hidden)),
        ("R5's calibrated pick_window blanked on a copy", "HONESTY-LABEL",
         lambda: with_("R5_CHOP", pw_blank)),
        ("a dropped R2 cell", "missing ['", lambda: with_("R2_FEASIBILITY",
                                                          lambda d: d.iloc[1:].copy())),
        ("an undeclared R5 cell", "undeclared ['", lambda: with_("R5_CHOP", undeclared)),
        ("R1's collar blanked", "COLLAR: R1_LENSES.tier", lambda: with_("R1_LENSES", blank)),
        ("a verdict column on NEST_GRID_BY_STATE", "VERDICT-COLUMN",
         lambda: with_("NEST_GRID_BY_STATE", verdict_col)),
        ("a NaN mean under n > 0 (R5_CHOP)", "NAN", lambda: with_("R5_CHOP", nan_mean)),
        ("a NaN holdout mean under n_holdout > 0 (NEST_GRID_BY_COIN)", "NAN",
         lambda: with_("NEST_GRID_BY_COIN", nan_hold)),
        ("a NEST_GRID_FREQ count + 1", "PARTITION", lambda: with_("NEST_GRID_FREQ", plus_one)),
    ])


def grid_real():
    f, lines = grid_findings(_tables())
    n = {k: len(v) for k, v in declared().items()}
    return (not f), (f"R1 == the filed SCALE_PICKS.json on every pick and window (density "
                     f"at the window == filed on all 71) and every R1 density == 100 x its "
                     f"printed count / its era's bars (ALL / tuning / holdout, record and "
                     f"frozen); R2 fallback / stability-changed / window labels == the filed "
                     f"picks; every R5 / NEST_GRID row's lenses_read / pick_window / "
                     f"stability_changed_members == the filed picks of the lenses it "
                     f"consumes; era partitions exact (R1 confirmed ranges and bars, R2 "
                     f"n_ranges and edge_n: tuning + holdout == ALL); "
                     f"every grid WHOLE against the typed cells {n}; every Tier-E table "
                     f"collared on every row with no verdict column; R2's word and verdict only "
                     f"on the 7 record rows and no verdict-named column; n = 0 <=> NaN stats "
                     f"(whole and holdout slice); R5 buckets, NEST_GRID states and coincidence "
                     f"categories partition the entries (v6 200 / 9-12 199)"
                     + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-KEY
def _parquets(root: Path) -> list[str]:
    out = []
    for p in sorted(root.rglob("*.parquet")):
        rel = p.relative_to(root)
        if rel.parts[0].startswith("_det_"):
            continue
        out.append(str(rel.with_suffix("")))
    return out


def key_findings(root: Path, man: dict, frames: dict | None = None) -> list[str]:
    out = []
    on_disk = _parquets(root)
    if sorted(on_disk) != sorted(KEYS_T):
        out.append(f"KEY-DECLARED: parquets on disk {sorted(set(on_disk) ^ set(KEYS_T))} are "
                   f"not the typed set")
    if man.get("keys") != KEYS_T:
        diff = sorted(k for k in set(man.get("keys", {})) | set(KEYS_T)
                      if man.get("keys", {}).get(k) != KEYS_T.get(k))
        out.append(f"KEY-MANIFEST: manifest keys differ from the typed keys on {diff}")
    for name, key in KEYS_T.items():
        d = frames[name] if frames and name in frames else (
            pd.read_parquet(str(root / f"{name}.parquet")) if (root / f"{name}.parquet").exists()
            else None)
        if d is None:
            out.append(f"KEY-DECLARED: {name}.parquet absent")
            continue
        dup = int(d.duplicated(subset=key).sum())
        if dup:
            out.append(f"KEY-UNIQUE: {name} key {key} has {dup} duplicate(s)")
        req = REQUIRED_T["NEST"] if name in ("NEST_v6", "NEST_trg912") else REQUIRED_T[name]
        for c in req:
            if c not in d.columns:
                out.append(f"KEY-NULL: {name} lacks required column {c}")
            elif bool(d[c].isna().any()):
                out.append(f"KEY-NULL: {name}.{c} holds {int(d[c].isna().sum())} null(s)")
        sha = C.content_sha(d)
        if man.get("sha", {}).get(name) != sha:
            out.append(f"KEY-SHA: manifest sha of {name} {str(man.get('sha', {}).get(name))[:12]}… "
                       f"!= the table's {sha[:12]}…")
    r2 = frames["R2_FEASIBILITY"] if frames and "R2_FEASIBILITY" in frames else \
        pd.read_parquet(str(root / "R2_FEASIBILITY.parquet"))
    rec = r2["is_lens_verdict_of_record"].astype(bool)
    if r2.loc[rec, "verdict"].isna().any() or r2.loc[rec, "word"].isna().any() or \
            r2.loc[~rec, "would_read"].isna().any():
        out.append("KEY-NULL: R2 verdict / word (record) / would_read (Tier-E) null")
    return out


def _man() -> dict:
    return json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))


def key_break():
    man = _man()

    def dup():
        d = written("NEST_v6")
        return key_findings(OUT, man, {"NEST_v6": pd.concat([d, d.iloc[[0]]], ignore_index=True)})

    def null_would():
        d = written("R2_FEASIBILITY")
        i = d.index[~d["is_lens_verdict_of_record"].astype(bool)][4]
        d.loc[i, "would_read"] = None
        return key_findings(OUT, man, {"R2_FEASIBILITY": d})

    def sha_alt():
        m = json.loads(json.dumps(man))
        m["sha"]["R5_CHOP"] = "0" * 64
        return key_findings(OUT, m)

    def key_alt():
        m = json.loads(json.dumps(man))
        m["keys"]["R5_CHOP"] = ["lens", "bucket"]
        return key_findings(OUT, m)

    def undeclared():
        tmp = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            shutil.copytree(OUT, tmp / "sr", ignore=shutil.ignore_patterns("_det_*"))
            written("R5_CHOP").to_parquet(str(tmp / "sr" / "EXTRA_TABLE.parquet"), index=False)
            return key_findings(tmp / "sr", man)
        finally:
            shutil.rmtree(tmp, ignore_errors=True)

    return plants([
        ("a duplicated NEST_v6 row", "KEY-UNIQUE", dup),
        ("a nulled R2 would_read on a Tier-E row", "KEY-NULL: R2 verdict / word (record) / "
                                                   "would_read (Tier-E) null", null_would),
        ("a manifest content sha altered", "KEY-SHA", sha_alt),
        ("a manifest key altered", "KEY-MANIFEST", key_alt),
        ("an undeclared parquet in a temp copy of stage_r/", "KEY-DECLARED", undeclared),
    ])


def key_real():
    f = key_findings(OUT, _man())
    return (not f), (f"{len(KEYS_T)} parquets == the typed set on disk and in the manifest; "
                     f"every typed key unique; every typed required column non-null; every "
                     f"manifest content sha == the table's" + (f"; findings {f[:4]}" if f else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def _files(d: Path) -> dict:
    """{relative path: the file's PATH} — bytes read by open(), parquet content read
    through pandas on the path string (AM-2; verifier MINOR-14)."""
    out = {}
    for p in sorted(d.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(d)
        if rel.parts[0].startswith("_det_") or rel.name.startswith("FIXTURES_"):
            continue
        out[str(rel)] = p
    return out


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1])):
        if sorted(x) != sorted(canon):
            out.append(f"{lab}: file set {sorted(set(x) ^ set(canon))[:4]} differs from canonical")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            bx, by = x[name].read_bytes(), y[name].read_bytes()
            if bx != by:
                k = next((i for i in range(min(len(bx), len(by))) if bx[i] != by[i]),
                         min(len(bx), len(by)))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = C.content_sha(pd.read_parquet(str(x[name])))
                cb = C.content_sha(pd.read_parquet(str(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    return RUN_ROOT / DET_ROOT.name


def det_launch(d: Path, seed: int, hashorder: bool = False) -> subprocess.Popen:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_r.py"), "build", f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_r as SR\n"
                f"d = Path({str(d)!r})\nSR.build(d)\n"
                f"p = d / 'STAGE_R.md'\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(SR.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    return subprocess.Popen(cmd, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                            text=True, cwd=str(ROOT))


def det_collect(procs: dict) -> dict:
    out = {}
    for k, (d, p) in procs.items():
        _, err = p.communicate(timeout=3600)
        if p.returncode != 0:
            clock(f"F-DET build {k} exit {p.returncode}: {err[-400:]}")
        out[k] = (p.returncode, _files(d) if d.exists() else {})
    return out


def det_break():
    canon = _files(OUT)
    tmp = Path(tempfile.mkdtemp(prefix="f-det-"))
    try:
        md = bytearray(canon["STAGE_R.md"].read_bytes())
        md[len(md) // 2] ^= 0x01
        (tmp / "STAGE_R.md").write_bytes(bytes(md))
        bent = dict(canon, **{"STAGE_R.md": tmp / "STAGE_R.md"})

        def float_moved():
            d = pd.read_parquet(str(canon["R5_CHOP.parquet"]))
            i = d.index[d["n"].astype(int) > 0][0]
            d.loc[i, "sum_net_r"] = float(d.loc[i, "sum_net_r"]) + 1e-6
            p = tmp / "R5_CHOP.parquet"
            d.to_parquet(str(p), index=False)
            c2 = dict(canon, **{"R5_CHOP.parquet": p})
            return det_findings((0, c2), (0, c2), canon)

        def hashorder():
            procs = {s: (det_dir() / f"hashorder_{s}", det_launch(det_dir() / f"hashorder_{s}", s,
                                                                 hashorder=True))
                     for s in DET_SEEDS}
            o = det_collect(procs)
            a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
            return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

        return plants([
            ("one byte bent in a copy of STAGE_R.md", "STAGE_R.md bytes differ",
             lambda: det_findings((0, canon), (0, bent), canon)),
            ("one R5_CHOP sum moved 1e-6 in a parquet copy", "R5_CHOP.parquet content sha",
             float_moved),
            ("a hash-order-dependent line (set iteration) under the two seeds",
             f"seed 1 vs seed {SEED}: STAGE_R.md bytes differ", hashorder),
        ])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def det_real():
    canon = _files(OUT)
    procs = {s: (det_dir() / f"seed_{s}", det_launch(det_dir() / f"seed_{s}", s))
             for s in DET_SEEDS}
    o = det_collect(procs)
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == canonical ({len(canon)} files, "
                       f"recursive) in both builds; every file byte-identical seed 1 == seed "
                       f"{SEED} == canonical, every parquet content sha equal: {not bad}"
                       + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-FEAS", "every R2 word, would_read and lens verdict of record re-derived from its "
     "printed columns (the tolls typed per stem); the TC10 continuity anchor [L-R.4, L-1.4, "
     "AM-1]",
     "a record word / verdict or a Tier-E would_read differs from the typed [Q-R3] law "
     "applied to its printed columns; a Tier-E row carries a verdict word; the record rows are "
     "not exactly POOLED:CLASSIC5 · holdout · calibrated · taker on the 7 typed lenses; a "
     "row's bps is not its members' typed toll (taker 10 · maker 4 · charter 2 x (5 + tier "
     "A 2 / B 5 / C 10)), an ASSET twin toll in ATR is not the typed ratio x the taker row's, "
     "or a pooled edge toll is not the binding member max; the height-ratio deciles are not a "
     "distribution with d5 == the median; the JSON of record disagrees with "
     "its row; or a frozen-3.0 tuning-era taker row at 5m/4h/1d (typed 44) differs from "
     "TC10's filed verdict table",
     feas_break, feas_real),
    ("F-R5-ANCHOR", "TC10's five-row table re-derived from the FILED control journal with the "
     "TC11 nest, exactly; R5_FIVE_ROW's eleven columns on both sides [L-R.7]",
     "the filed journal is not the typed bytes (fcbf5db0…, 200 rows inside the TC10 window), "
     "or its frozen-3.0 4h entry-state table under the TC11 nest differs from TC10's "
     "control_entry_by_state.parquet on any of the 11 typed columns of the five typed rows, "
     "or R5_FIVE_ROW's tc10_* columns are not the filed ones, or its tc11_* columns are not "
     "this file's own crosstab of NEST_v6's frozen entry rows, or R5_CHOP does not partition "
     "them",
     anchor_break, anchor_real),
    ("F-CHOP-VALUE", "every R5_CHOP and NEST_GRID cell re-derived here from the written entry "
     "rows by the typed bucket / coincidence / honesty laws [L-R.7, L-R.5, L-R.2, AM-4]",
     "any cell of R5_CHOP / NEST_GRID_FREQ / BY_STATE / BY_COIN (n, mean, P(win), ΣR, the "
     "holdout slice, n_scale_in_sample, n_stability_changed, FREQ n / share) differs from the "
     "value re-derived here from NEST_v6 / NEST_trg912's entry rows, the books' net_r and the "
     "FILED picks (counts exact, floats to the 8-dp bound)",
     chop_break, chop_real),
    ("F-NEST-BOOK", "the nest at book instants: the instant law typed here from the raw 4h "
     "tape; the join; the causal prefix-run check; the nest-book door on the probe and on "
     "real regbooks [L-R.5, AM-6]",
     "for either book at either scale the written instant set differs from the typed law "
     "(4h closes arm -> exit stamp; +1R and stop exits at their bar OPEN, twins at the close; "
     "close events at the close; corridor_end -> as_of_pin); the join differs from N.nest_at; "
     "a sampled entry read differs from a machine run on the tape cut at the read bar; the "
     "CLI door differs from the in-process door or (outside stamp_law) NEST_v6; the derived "
     "path differs from the typed law; the door on P-BRK-4H / P-WARN-1 / the relay copy "
     "differs from the typed law; or the door files P-RELAY-1 / P-ADD-BRK scored instead of "
     "refusing them with the typed UNSTAMPED counts",
     nestbook_break, nestbook_real),
    ("F-GRID", "every grid WHOLE against cells typed here; R1 == the filed picks, densities "
     "from their counts; honesty labels; collars; no verdict word off the record; NaN law; "
     "partitions",
     "a grid is not whole against the typed cells (R1 71 · R2 1458 · R5 64 · FREQ 544 · "
     "BY_STATE 100 · BY_COIN 136); an R1 pick / window differs from SCALE_PICKS.json or its "
     "window density from the filed one, or an R1 density is not 100 x count / bars of its "
     "era; an R2 fallback / stability-changed / window label, or an R5 / NEST_GRID lens "
     "label, differs from the filed picks; a Tier-E table lacks the exact collar or carries a "
     "verdict column; R2's word / verdict is off the 7 record rows; a stat is NaN under n > 0 "
     "(or finite at n = 0), whole or holdout; or a partition breaks (R1 / R2 eras, R5 "
     "buckets, NEST_GRID states and categories)",
     grid_break, grid_real),
    ("F-KEY", "typed keys unique, typed required columns non-null, the manifest total and "
     "exact",
     "a typed key is not unique, a typed required column holds a null, a parquet on disk is "
     "undeclared (or a declared one absent), a manifest key is not the typed one, or a "
     "manifest content sha is not the table's",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_stage_r) differ from each "
     "other or from the canonical stage_r/ files in the recursive file set, any byte or any "
     "parquet content sha, or either exits nonzero",
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
    say("TIER-C11 STAGE R-a FIXTURES — scripts/tierc11_stage_r.py (R1 lenses · R2 feasibility "
        "· R3 the nest on the books + the nest-book door · R5 chop) — break leg first, RED or "
        "void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · TC10 pin {TC10_PIN}")
    for ln in SR.lean_block().rstrip("\n").split("\n"):
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
