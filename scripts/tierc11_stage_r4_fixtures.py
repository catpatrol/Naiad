#!/usr/bin/env python
"""TIER-C11 · STAGE R-b · R4 — F-R4-EVENTS · F-R4-SCAN · F-R4-OUTCOME · F-R4-BASE ·
F-R4-GRIDSTAT · F-NULL · F-R4-L1 · F-R4-CONT · F-GRID · F-KEY · F-DET.  The fixtures of
scripts/tierc11_stage_r4.py (the two trades per lens, Tier-E, whole) [LEANS
L-R.6; AM-1, AM-4, AM-6].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen [the prove() law
of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py; the worked
example scripts/tierc11_books_fixtures.py].  A break leg is a set of PLANTS
judged one at a time; a plant counts as CAUGHT only if a finding NAMES THE
INTENDED DETECTOR.  A plant that crashes is a FIXTURE DEFECT, never a catch.
Every plant is made on a COPY (a frame, a temp dir) or under a MUTATION of the
module restored in `finally`; no artifact of record moves.  The referees are
typed HERE (a second object): the commission (panels, lenses, the ladder, the
events, cells, laws, directions, eras, horizons), the anchor laws (tap touch + 3,
memory line touch + 6, harden at its own bar), the toll (10 bps round trip),
the era cut, the coincidence width and the mid band, the ATR recurrence
(Wilder, 14, seeded at TR[0]), the 1d derivation (six complete 4h bars per UTC
day), the null's draw law (default_rng([seed + draw, crc32("asset|lens|scale")]),
gaps permuted, u's, then the order of the pairs; the lead-gap floor 14), the
TC10 continuity figures (n 236 / NET +0.681 ALL, n 88 / +0.706 holdout, L-T.1),
the table keys, the files, the collar.  Raw bars are read from the snapshot's
kline files by this file's own loader.

  F-R4-EVENTS  FAILS IF, on ANY of the 112 (asset, lens, scale) cells, the filed
               events differ from N's own frames (N.events: the first-hold scan
               rows, C.retest_holds' hold rows, the memory-line scan and the
               engine's one-shot flip, the hardens) in their key set, their
               known_at, their death bar or boundary; or break the typed laws
               (anchor = touch + 3 on a tap, touch + 6 on the memory line, the
               harden's own bar; direction +1 iff a top death / a bottom harden;
               the close stamp = the raw bar's open + the lens step; era by that
               close).  SABOTAGE: events read at their bar close (touch) instead
               of known_at (module mutation); the one-shot rows filed as
               first-hold; a spring filed short; a boundary moved.
  F-R4-SCAN    FAILS IF, on ANY of the 112 cells, R4_SCAN's rows are not N's
               first-retest scan rows (N.first_retest_scan: key set, seq,
               known_at, verdict, first-hold flag, death bar), a (death, band)
               sequence breaks the typed scan law (seq 0..m-1 in touch order,
               inside (die_i, min(die_i + 400, next death - 1)]; every row but
               the last failed; a hold or a truncated row ends it; first hold
               iff hold; known_at = touch + 3 on a tap, + 6 on the memory line;
               the close stamp from raw bars, 'beyond_pin' past the tape; era
               by that close), a hold row is not R4_EVENTS' first-hold event,
               or R4_DEATHS is not N's deaths with each band's touch count, end
               and hold touch re-derived here from R4_SCAN.  SABOTAGE (copies):
               a failed touch dropped; a failed touch re-filed as a hold
               mid-sequence; a death's end relabelled.
  F-R4-OUTCOME FAILS IF, on >= 30 events chosen by a typed rule (the two last of
               each CLASSIC5 lens cell — censored — plus seeded ones, and every
               UNSEEN12 1d frozen cell once), the filed known_at, censor flags,
               H20 / H100 terms, MFE / MAE or toll differ from this file's own
               computation on raw bars (typed ATR loop, c[k + H] in bars of L,
               censored when k + H > n - 1, toll = 10 bps x c / ATR) at 8 dp; or
               the selection holds no censored case.  SABOTAGE: the horizon
               shortened to the tape's end (module mutation); a half toll.
  F-R4-BASE    FAILS IF one FULL base cell per lens (1h, 4h, 12h, 1d; plus an
               own-side twin cell), recomputed by a plain loop over every bar of
               L (cells from N.nest_at at each close with this file's cell law,
               terms and tolls from raw bars), differs from the filed R4_BASE
               row in n_events, n, n_censored, median, mean, hit rates, toll or
               NET.  SABOTAGE: the base cell read one bar late; the horizon
               shortened (module mutations).
  F-R4-GRIDSTAT FAILS IF ANY R4_GRID row (all of them, per asset and pooled)
               differs from this file's own statistics on the FILED R4_EVENTS
               (typed law -> column map, direction map, era cut; n_events / n /
               n_censored / n_bad_atr, median / q25 / q75 (the linear rule) /
               hit rates / median MFE / MAE, the toll = the median over the
               row's uncensored anchors, a pool's = the MAX over members with
               n > 0, toll_atr_all, NET = median - toll at 8 dp, the binding
               count; mean_term exact at 8 dp save at a half-unit tie, where the
               order of summation may pick either neighbour), or a POOLED
               R4_BASE row (one per lens, both panels) differs from the members'
               plain loops over every bar with the binding toll.  SABOTAGE
               (module mutations, the CLASSIC5 4h calibrated unit rebuilt):
               long / short swapped in the grouping; the record cells
               partitioned by the memory-line twin's column; the pooled toll
               taken from the members' ALL-cell rows (grid, and base).
  F-NULL       FAILS IF a filed draw's box schedule does not reproduce from its
               seed by this file's own draw law (5 cells x 20 draws); any filed
               draw (all 112 cells x 20) breaks the multiset of gaps or of
               (life, height) pairs against the real ranges; any draw's schedule
               is the real one; the null's event road fed the REAL bundle does
               not give N.events' frames; or, on 3 cells x 2 draws and one
               pooled draw, the filed box fates or draw n / NET differ from
               this file's INDEPENDENT rebuild (its own static-box law on the
               seed's schedule and raw bars, its own EMA tap scans, the L+1
               cell from N.nest_at at the known_at close with its own
               partition, its own term / toll / grid arithmetic).  SABOTAGE: a
               draw that re-uses real positions (NL.schedule bent); a stream
               shared across cells (NL.draw_rng bent); a box moved one bar in a
               copy; the null's L+1 read one bar late; the null's springs filed
               short (module mutations).
  F-R4-L1      FAILS IF the filed L+1 cell (record, memory-line twin, SFP
               post-redraw twin) of >= 30 events (aimed at events whose cell
               moves one bar later, plus seeded ones) differs from this file's
               recomputation from N.nest_at at the known_at close.  SABOTAGE:
               the L+1 read one bar of L late (module mutation).
  F-R4-CONT    FAILS IF TC10's filed row is not the typed n / NET, the manifest's
               continuity block says the replay differs, the replay run here
               differs from the file at 8 dp, or TC11's grid row is not the
               block's.  SABOTAGE: the replay under the provisional retest pins
               (hold 6); a filed-row copy with n 235.
  F-GRID       FAILS IF R4_GRID / R4_BASE / R4_NULL do not hold exactly the
               declared cells typed here (TP.grid_whole), a row breaks the NaN
               law or the NET law, the era / direction / cell partitions do not
               add up, the collar is not the typed one, a verdict column or word
               appears, a grid row's base columns are not R4_BASE's row under the
               typed law mapping, or a null summary figure is not re-derivable
               from the filed draws.  SABOTAGE (copies): a row dropped, a row
               duplicated, an undeclared cell, NaN under n > 0, a verdict column,
               gates altered, an era count bent, a base join to the wrong law, a
               null median moved.
  F-KEY        FAILS IF a table's key is not the typed one or not unique, a
               required column is null, TP.check_keys over the stage root is
               RED, or a manifest content sha is not the table's.  SABOTAGE: a
               duplicated row; a nulled key; an as-of column dropped; a manifest
               sha altered; the module's R4_EVENTS key without `event`.
  F-DET        FAILS IF two builds under PYTHONHASHSEED 1 and 20260924 (each: the
               14 units in fresh interpreters, then the merge) differ from each
               other or from the files of record in the file set, any byte or any
               parquet content sha, or either exits nonzero.  SABOTAGE: a byte
               bent in a copy; a float moved in a parquet copy; a hash-order
               line emitted under the two seeds.  Parquet is read and written
               through pandas on path strings only [AM-2].
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_r4_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript AND the F-DET twins (DIR/_det_r4/); the
      files compared against are always the record, research_outputs/tierc11/stage_r4/.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import hashlib
import json
import math
import os
import re
import shutil
import statistics
import subprocess
import sys
import time
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_r4 as R                                         # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

N, E, C, NL = R.N, R.E, R.C, R.NL
TP = E.TP

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never R's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
TC10_PIN = 1790006400000                 # 2026-09-21T16:00:00Z
SEED, SEED_SENS, K = 20260924, 20260816, 20
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
CLASSIC5_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
UNSEEN12_T = ("ENAUSDT", "PUMPUSDT", "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT",
              "XMRUSDT", "BNBUSDT", "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
PANELS_T = {"CLASSIC5": CLASSIC5_T, "UNSEEN12": UNSEEN12_T}
POOL_T = {"CLASSIC5": "POOLED:CLASSIC5", "UNSEEN12": "POOLED:UNSEEN12"}
LENSES_T = {"CLASSIC5": ("1h", "4h", "12h", "1d"), "UNSEEN12": ("1h", "4h", "1d")}
LADDER_T = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": "1w"}
HAS_L1_T = {("CLASSIC5", "1h"): True, ("CLASSIC5", "4h"): True, ("CLASSIC5", "12h"): True,
            ("CLASSIC5", "1d"): True, ("UNSEEN12", "1h"): True, ("UNSEEN12", "4h"): False,
            ("UNSEEN12", "1d"): False}
STEP_T = {"1h": 3_600_000, "4h": 14_400_000, "12h": 43_200_000, "1d": 86_400_000}
SCALES_T = ("calibrated", "frozen3.0")
EVENTS_T = ("BRK_tap89_first", "BRK_tap89_oneshot", "BRK_tap127_first", "BRK_tap127_oneshot",
            "BRK_tap200_first", "BRK_tap200_oneshot", "BRK_mem_first", "BRK_mem_oneshot",
            "SFP_harden")
PART_T = ("EXP_ALIGNED", "EXP_COUNTER", "IN_RANGE_COINCIDENT", "IN_RANGE_MID",
          "IN_RANGE_OTHER", "NONE")
DIRS_T = ("both", "long", "short")
ERAS_T = ("ALL", "tuning", "holdout")
HOR_T = {"H20": 20, "H100": 100}
EV_LAWS_T = {"BRK": ("record", "mem_twin"), "SFP": ("record", "mem_twin", "post_redraw")}
BASE_LAWS_T = ("record", "mem_twin", "topside", "botside", "own_side_brk", "own_side_sfp",
               "own_side_brk_mem", "own_side_sfp_mem")
CELL_BASE_T = {"record": "record", "mem_twin": "mem_twin", "post_redraw": "record"}
SIDE_BASE_T = {("BRK", "record"): "own_side_brk", ("BRK", "mem_twin"): "own_side_brk_mem",
               ("SFP", "record"): "own_side_sfp", ("SFP", "mem_twin"): "own_side_sfp_mem",
               ("SFP", "post_redraw"): "own_side_sfp"}
LAWCOL_T = {"record": "cell", "mem_twin": "cell_mem", "post_redraw": "cell_post"}
DIRSET_T = {"both": (1, -1), "long": (1,), "short": (-1,)}
SCAN_BANDS_T = ("tap89", "tap127", "tap200", "memory-line")
SLUG_T = {"tap89": "tap89", "tap127": "tap127", "tap200": "tap200", "memory-line": "mem"}
TTL_T = 400                              # C.RETEST_PINS ttl 400 · MEM_TTL_BARS 400
RETEST_T = {"margin": 1.0, "hold": 3}    # the taps' hold test [L-R.6(a)]
STATIC_T = {"dev_return": 7, "break_n": 8, "break_margin": 1.5}   # the static-box pins
ANCHOR_LAG_T = {"tap89": 3, "tap127": 3, "tap200": 3, "memory-line": 6, "harden": 0}
TOLL_BPS_T = 10.0
ERA_CUT_T = 1_719_791_999_000            # tuning closes <= 2024-06-30T23:59:59Z
COIN_T, MID_T, ATR_LEN_T, LEAD_FLOOR_T = 0.25, (25.0, 75.0), 14, 14
DAY_MS_T, BARS_PER_DAY_T = 86_400_000, 6
TC10_TYPED = {"ALL": (236, "+0.681"), "holdout": (88, "+0.706")}    # L-T.1 / AM-1
KEYS_T = {"R4_EVENTS": ["asset", "lens", "scale_kind", "event", "rid", "side", "anchor_i"],
          "R4_GRID": ["asset", "lens", "scale_kind", "event", "cell_law", "cell", "direction",
                      "era", "horizon"],
          "R4_BASE": ["asset", "lens", "scale_kind", "cell_law", "cell", "direction", "era",
                      "horizon"],
          "R4_NULL": ["asset", "lens", "scale_kind", "event", "cell", "direction", "era",
                      "horizon"],
          "R4_NULL_BOXES": ["asset", "lens", "scale_kind", "draw", "box"],
          "R4_SCAN": ["asset", "lens", "scale_kind", "band", "rid", "side", "touch_i"],
          "R4_DEATHS": ["asset", "lens", "scale_kind", "rid", "side"]}
FILES_T = ("R4_BASE.parquet", "R4_DEATHS.parquet", "R4_EVENTS.parquet", "R4_GRID.md",
           "R4_GRID.parquet", "R4_NULL.parquet", "R4_NULL_BOXES.parquet", "R4_SCAN.parquet",
           "STAGE_R4.md", "build_manifest.json")
COLLAR_T = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
            "gates": "nothing"}
AS_OF_T = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days", "warranty",
           "as_of_lens", "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
           "as_of_substrate")
REQUIRED_T = {
    "R4_EVENTS": ["family", "band", "rule", "dir", "die_i", "seq", "known_at",
                  "known_close_ms", "era", "cell", "cell_mem", "cell_post", "u_state",
                  "bad_atr", "cens_H20", "cens_H100", "l_pick_window", "u_pick_window"],
    "R4_GRID": ["n_events", "n", "n_censored", "nan_reason", "horizon_bars", "toll_pooling",
                "n_l_scale_in_sample", "n_u_scale_in_sample", "l_pick_window"],
    "R4_BASE": ["n_events", "n", "n_censored", "nan_reason", "horizon_bars",
                "n_l_scale_in_sample", "n_u_scale_in_sample", "l_pick_window"],
    "R4_NULL": ["real_n", "n_draws", "seed", "pctile_law", "schedule_variant", "nan_reason",
                "n_draws_valid_net"] + [f"n_d{i:02d}" for i in range(K)],
    "R4_NULL_BOXES": ["src_rid", "confirm_i", "life", "sched_end", "height_atr", "u",
                      "fate", "lead_gap_swapped", "identity_perm"],
    "R4_SCAN": ["die_i", "dir", "seq", "known_at", "known_close_ms", "verdict",
                "is_first_hold", "era", "pick_window"],
    "R4_DEATHS": ["die_i", "dir", "known_at", "known_close_ms", "boundary", "era"]
                 + [f"{x}_{b}" for b in ("tap89", "tap127", "tap200", "mem")
                    for x in ("n_touches", "end", "hold_touch_i")],
}
VERDICT_COL_RX = re.compile(r"(^|_)(verdict|ci|p|pvalue|clears|promot\w*|supported)(_|$)")
VERDICT_WORD_RX = re.compile(r"\b(?:PASS|FAIL|SUPPORTED|REJECTED|CONFIRMED)\b")
BASE_CELLS_T = (   # one FULL base cell per lens, plus an own-side twin
    ("BTCUSDT", "1h", "calibrated", "record", "IN_RANGE_MID", "long", "ALL"),
    ("ETHUSDT", "4h", "calibrated", "record", "EXP_ALIGNED", "short", "tuning"),
    ("SOLUSDT", "12h", "calibrated", "record", "IN_RANGE_OTHER", "both", "holdout"),
    ("NEARUSDT", "1d", "calibrated", "record", "EXP_COUNTER", "long", "ALL"),
    ("ZECUSDT", "4h", "frozen3.0", "own_side_brk", "IN_RANGE_COINCIDENT", "both", "ALL"),
    ("SOLUSDT", "1h", "calibrated", "own_side_brk_mem", "IN_RANGE_COINCIDENT", "long", "ALL"),
    ("NEARUSDT", "12h", "frozen3.0", "own_side_sfp_mem", "IN_RANGE_COINCIDENT", "both",
     "holdout"),
    ("BTCUSDT", "4h", "calibrated", "record", "ALL", "both", "holdout"),   # holds the tape end
)
BASE_POOL_T = (    # one POOLED base row per lens (and the twelve's pool), typed cells
    ("POOLED:CLASSIC5", "1h", "calibrated", "record", "IN_RANGE_COINCIDENT", "short", "holdout"),
    ("POOLED:CLASSIC5", "4h", "calibrated", "own_side_sfp", "IN_RANGE_MID", "both", "ALL"),
    ("POOLED:CLASSIC5", "12h", "frozen3.0", "own_side_brk_mem", "EXP_ALIGNED", "long", "tuning"),
    ("POOLED:CLASSIC5", "1d", "calibrated", "mem_twin", "IN_RANGE_OTHER", "both", "ALL"),
    ("POOLED:UNSEEN12", "4h", "calibrated", "record", "NA", "short", "holdout"),
    ("POOLED:UNSEEN12", "1h", "frozen3.0", "topside", "EXP_COUNTER", "long", "ALL"),
)
GRIDSTAT_UNIT_T = ("CLASSIC5", "4h", "calibrated")     # the unit the break legs rebuild
NULL_REPRO_T = (("BTCUSDT", "4h", "calibrated"), ("ETHUSDT", "1h", "calibrated"),
                ("SOLUSDT", "12h", "frozen3.0"), ("HYPEUSDT", "1d", "calibrated"),
                ("NEARUSDT", "1d", "frozen3.0"))
NULL_ROAD_T = (("BTCUSDT", "4h", "calibrated"), ("ZECUSDT", "1d", "frozen3.0"),
               ("ETHUSDT", "12h", "calibrated"), ("SUIUSDT", "1h", "calibrated"))
NULL_INDEP_T = (("BTCUSDT", "4h", "calibrated"), ("ETHUSDT", "12h", "frozen3.0"),
                ("SUIUSDT", "1h", "calibrated"))
NULL_INDEP_DRAWS_T = (0, 13)
NULL_INDEP_POOL_T = ("CLASSIC5", "4h", "calibrated", 0)    # one pooled draw, every member
NULL_INDEP_EVENTS_T = ("BRK_tap89_first", "BRK_tap89_oneshot", "BRK_tap200_first",
                       "SFP_harden")
OUT = R.OUT
RUN_ROOT = OUT
DET_DIRNAME = "_det_r4"
TRANSCRIPT = "FIXTURES_R4.txt"
PY = sys.executable
DET_PROCS = 16
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


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def prove(fid: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Break first; it must go RED (ok False) or the fixture is VOID."""
    t0 = time.time()
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
    clock(f"{fid} {time.time() - t0:.1f}s")


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
            caught.append(f"{name} -> {len(found)} finding(s), e.g. {hit[:170]}")
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


def r8(x) -> np.ndarray:
    return np.round(np.asarray(x, dtype=float), 8)


def same8(a, b) -> np.ndarray:
    a, b = r8(a), r8(b)
    return (a == b) | (np.isnan(a) & np.isnan(b))


# ═══════════════════════════════════════════════ the filed record + raw bars
_FILED: dict = {}


def filed(name: str) -> pd.DataFrame:
    if name not in _FILED:
        _FILED[name] = pd.read_parquet(str(OUT / f"{name}.parquet"))
    return _FILED[name]


def manifest() -> dict:
    return json.loads((OUT / "build_manifest.json").read_text(encoding="utf-8"))


_RAW: dict = {}


def raw_bars(stem: str, lens: str) -> dict:
    """THIS FILE'S OWN LOADER: the snapshot's kline file, sorted, CLOSED bars <=
    the pin; 1d = six complete native 4h bars per UTC day (typed law); ATR by
    the typed Wilder recurrence (TR[0] = h - l; atr[0] = TR[0]; atr[i] =
    atr[i-1] + (TR[i] - atr[i-1]) / 14)."""
    key = (stem, lens)
    if key in _RAW:
        return _RAW[key]
    src = "4h" if lens == "1d" else lens
    f = pd.read_parquet(str(TC11_SNAP / "klines" / f"{stem}_{src}.parquet"))
    f = f.sort_values("open_time", kind="mergesort").reset_index(drop=True)
    step_src = STEP_T[src]
    f = f[f["open_time"] + step_src <= PIN].reset_index(drop=True)
    if lens == "1d":
        day = (f["open_time"] // DAY_MS_T).to_numpy()
        rows = []
        for dd, g in f.groupby(day, sort=True):
            if len(g) == BARS_PER_DAY_T:
                rows.append((int(dd) * DAY_MS_T, float(g["open"].iloc[0]),
                             float(g["high"].max()), float(g["low"].min()),
                             float(g["close"].iloc[-1])))
        f = pd.DataFrame(rows, columns=["open_time", "open", "high", "low", "close"])
        f = f[f["open_time"] + DAY_MS_T <= PIN].reset_index(drop=True)
    t0 = f["open_time"].to_numpy(np.int64)
    h, l, c = (f[k].to_numpy(float) for k in ("high", "low", "close"))
    n = len(c)
    atr = np.empty(n)
    prev = None
    for i in range(n):
        tr = (h[i] - l[i]) if i == 0 else max(h[i] - l[i], abs(h[i] - c[i - 1]),
                                              abs(l[i] - c[i - 1]))
        prev = tr if prev is None else prev + (1.0 / ATR_LEN_T) * (tr - prev)
        atr[i] = prev
    out = {"t0": t0, "h": h, "l": l, "c": c, "atr": atr, "n": n, "step": STEP_T[lens],
           "close": t0 + STEP_T[lens]}
    _RAW[key] = out
    return out


def all_cells() -> list:
    return [(s, L, k) for p in PANELS_T for s in PANELS_T[p] for L in LENSES_T[p]
            for k in SCALES_T]


def panel_of(stem: str) -> str:
    return "CLASSIC5" if stem in CLASSIC5_T else "UNSEEN12"


def typed_cell(d: int, state: str, pct: float, coin: bool) -> str:
    """THIS FILE'S L+1 PARTITION [L-R.6]."""
    if state == "IN_RANGE":
        if coin:
            return "IN_RANGE_COINCIDENT"
        if MID_T[0] <= pct <= MID_T[1]:
            return "IN_RANGE_MID"
        return "IN_RANGE_OTHER"
    if state == "BULL_EXP":
        return "EXP_ALIGNED" if d == 1 else "EXP_COUNTER"
    if state == "BEAR_EXP":
        return "EXP_ALIGNED" if d == -1 else "EXP_COUNTER"
    return "NONE"


# ═══════════════════════════════════════════════════════ F-R4-EVENTS
def expected_events(stem: str, lens: str, kind: str) -> dict:
    """{(event, rid, side, anchor_i): (known_at, die_i, dir, boundary, boundary_post)}
    assembled HERE from N.events' own frames."""
    ev = N.events(stem, lens, kind)
    D = ev["deaths"]
    bnd = dict(zip(D["die_i"].astype(int), D["boundary"].astype(float)))
    out = {}
    sc, os_ = ev["scan"], ev["oneshot"]
    for band in ("tap89", "tap127", "tap200"):
        for r in sc[(sc["band"] == band) & sc["is_first_hold"]].itertuples(index=False):
            out[(f"BRK_{band}_first", int(r.rid), r.side, int(r.touch_i))] = (
                int(r.known_at), int(r.die_i), int(r.dir), bnd[int(r.die_i)], np.nan)
        for r in os_[(os_["band"] == band) & (os_["verdict"] == "hold")].itertuples(index=False):
            out[(f"BRK_{band}_oneshot", int(r.rid), r.side, int(r.touch_i))] = (
                int(r.known_at), int(r.die_i), int(r.dir), bnd[int(r.die_i)], np.nan)
    sm, om = ev["scan_mem"], ev["oneshot_mem"]
    for r in sm[sm["is_first_hold"]].itertuples(index=False):
        out[("BRK_mem_first", int(r.rid), r.side, int(r.touch_i))] = (
            int(r.known_at), int(r.die_i), int(r.dir), bnd[int(r.die_i)], np.nan)
    for r in om[om["verdict"] == "hold"].itertuples(index=False):
        out[("BRK_mem_oneshot", int(r.rid), r.side, int(r.touch_i))] = (
            int(r.known_at), int(r.die_i), int(r.dir), bnd[int(r.die_i)], np.nan)
    for r in ev["hardens"].itertuples(index=False):
        out[("SFP_harden", int(r.rid), r.side, int(r.harden_i))] = (
            int(r.known_at), -1, int(r.dir), float(r.boundary_pre), float(r.boundary_post))
    return out


def events_findings(got: pd.DataFrame, stem: str, lens: str, kind: str,
                    exp: dict | None = None) -> list[str]:
    exp = expected_events(stem, lens, kind) if exp is None else exp
    tag = f"{stem} {lens} {kind}"
    bad = []
    g = {(r.event, int(r.rid), r.side, int(r.anchor_i)): r for r in got.itertuples(index=False)}
    miss, extra = sorted(set(exp) - set(g)), sorted(set(g) - set(exp))
    if miss or extra:
        bad.append(f"EVENT-SET: {tag}: {len(miss)} of N's events missing, {len(extra)} not N's, "
                   f"e.g. {(miss or extra)[0]}")
    raw = raw_bars(stem, lens)
    n_anchor = n_dir = n_bnd = n_close = n_era = 0
    first = {}
    for key in sorted(set(exp) & set(g)):
        r, (ka, die, d, b, bp) = g[key], exp[key]
        band = ("memory-line" if key[0].startswith("BRK_mem") else
                "harden" if key[0] == "SFP_harden" else key[0].split("_")[1])
        if int(r.known_at) != ka or int(r.known_at) != key[3] + ANCHOR_LAG_T[band]:
            n_anchor += 1
            first.setdefault("ANCHOR", f"{key} filed known_at {r.known_at}, N {ka}, typed "
                                       f"{key[3] + ANCHOR_LAG_T[band]}")
        fam = key[0].split("_")[0]
        want_d = (1 if key[2] == "top" else -1) * (1 if fam == "BRK" else -1)
        if int(r.dir) != d or int(r.dir) != want_d or int(r.die_i) != die:
            n_dir += 1
            first.setdefault("DIR-LAW", f"{key} filed dir {r.dir} / die {r.die_i}, N {d} / "
                                        f"{die}, typed dir {want_d}")
        if not (same8(r.boundary, b) and same8(r.boundary_post, bp)):
            n_bnd += 1
            first.setdefault("BOUNDARY", f"{key} filed {r.boundary} / {r.boundary_post}, N "
                                         f"{b} / {bp}")
        k = int(r.known_at)
        want_close = int(raw["t0"][k]) + raw["step"] if 0 <= k < raw["n"] else -1
        if int(r.known_close_ms) != want_close:
            n_close += 1
            first.setdefault("CLOSE-STAMP", f"{key} filed {r.known_close_ms}, raw {want_close}")
        want_era = "tuning" if 0 <= want_close <= ERA_CUT_T else "holdout"
        if r.era != want_era:
            n_era += 1
            first.setdefault("ERA", f"{key} filed {r.era}, typed {want_era}")
    for det, n_ in (("ANCHOR", n_anchor), ("DIR-LAW", n_dir), ("BOUNDARY", n_bnd),
                    ("CLOSE-STAMP", n_close), ("ERA", n_era)):
        if n_:
            bad.append(f"{det}: {tag}: {n_} row(s), e.g. {first[det]}")
    return bad


def _cell_rows(df: pd.DataFrame, stem: str, lens: str, kind: str) -> pd.DataFrame:
    return df[(df["asset"] == stem) & (df["lens"] == lens) & (df["scale_kind"] == kind)]


def ev_break():
    cell = ("ETHUSDT", "4h", "calibrated")
    ev_f = _cell_rows(filed("R4_EVENTS"), *cell)
    exp = expected_events(*cell)

    def at_close():
        with mutated(R, "_anchor", lambda f: (f["touch_i"] if "touch_i" in f else
                                              f["harden_i"]).to_numpy(np.int64)):
            got = R.real_events(*cell)
        return events_findings(got, *cell, exp=exp)

    def oneshot_as_first():
        d = ev_f[ev_f["event"] != "BRK_tap89_first"]
        o = ev_f[ev_f["event"] == "BRK_tap89_oneshot"].assign(event="BRK_tap89_first")
        return events_findings(pd.concat([d, o], ignore_index=True), *cell, exp=exp)

    def spring_short():
        d = ev_f.copy()
        i = d.index[(d["event"] == "SFP_harden") & (d["side"] == "bottom")][0]
        d.loc[i, "dir"] = -1
        return events_findings(d, *cell, exp=exp)

    def boundary_moved():
        d = ev_f.copy()
        i = d.index[d["event"] == "BRK_tap127_first"][0]
        d.loc[i, "boundary"] = float(d.loc[i, "boundary"]) * (1 + 1e-4)
        return events_findings(d, *cell, exp=exp)

    return plants([
        ("events read at their bar close (touch) instead of known_at (module mutation)",
         "ANCHOR", at_close),
        ("the one-shot tap89 rows filed as first-hold", "EVENT-SET", oneshot_as_first),
        ("a spring (bottom harden) filed short", "DIR-LAW", spring_short),
        ("a BREAKOUT boundary moved 1e-4 x", "BOUNDARY", boundary_moved),
    ])


def ev_real():
    f = filed("R4_EVENTS")
    bad, n_rows, n_cells = [], 0, 0
    by = {k: g for k, g in f.groupby(["asset", "lens", "scale_kind"], sort=True)}
    cells = all_cells()
    for cell in cells:
        got = by.get(cell, f.iloc[:0])
        bad += events_findings(got, *cell)
        n_rows += len(got)
        n_cells += 1
    extra = sorted(set(by) - set(cells))
    if extra:
        bad.append(f"EVENT-SET: cells outside the commission {extra[:3]}")
    fams = f.groupby("event").size().to_dict()
    return (not bad), (f"{n_cells} (asset, lens, scale) cells, {n_rows} filed events == N's own "
                       f"frames (key set, known_at, death bar, boundary), typed anchor / "
                       f"direction / close-stamp / era laws hold; per event {fams}"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-SCAN
SCAN_CMP_T = ("die_i", "dir", "seq", "known_at", "known_close_ms", "verdict", "is_first_hold")


def scan_findings(sc: pd.DataFrame, dth: pd.DataFrame, ev: pd.DataFrame, stem: str, lens: str,
                  kind: str) -> list[str]:
    """ONE cell's scan ledger against N's frames and the typed scan law."""
    tag = f"{stem} {lens} {kind}"
    bad, cnt, first = [], {}, {}

    def hit(det, msg):
        cnt[det] = cnt.get(det, 0) + 1
        first.setdefault(det, msg)
    exp = N.first_retest_scan(stem, lens, kind)
    ek = {(r.band, int(r.rid), r.side, int(r.touch_i)): r for r in exp.itertuples(index=False)}
    gk = {(r.band, int(r.rid), r.side, int(r.touch_i)): r for r in sc.itertuples(index=False)}
    miss, extra = sorted(set(ek) - set(gk)), sorted(set(gk) - set(ek))
    if miss or extra:
        hit("SCAN-SET", f"{len(miss)} of N's evaluated touches missing, {len(extra)} not N's, "
                        f"e.g. {(miss or extra)[0]}")
    for k in sorted(set(ek) & set(gk)):
        if any(getattr(ek[k], c_) != getattr(gk[k], c_) for c_ in SCAN_CMP_T):
            hit("SCAN-SET", f"{k}: filed {[getattr(gk[k], c_) for c_ in SCAN_CMP_T]}, N "
                            f"{[getattr(ek[k], c_) for c_ in SCAN_CMP_T]}")
    raw = raw_bars(stem, lens)
    dies = sorted(int(x) for x in dth["die_i"])
    nxt = {d_: (dies[i + 1] if i + 1 < len(dies) else raw["n"]) for i, d_ in enumerate(dies)}
    for (band, rid, side), g in sc.groupby(["band", "rid", "side"], sort=True):
        g = g.sort_values("seq", kind="mergesort")
        v, t = g["verdict"].tolist(), g["touch_i"].to_numpy(np.int64)
        d_i = int(g["die_i"].iloc[0])
        key = f"{band} rid {rid} {side}"
        lag = 6 if band == "memory-line" else 3
        if (g["seq"].tolist() != list(range(len(g))) or not (np.diff(t) > 0).all()
                or t[0] <= d_i or t[-1] > min(d_i + TTL_T, nxt.get(d_i, raw["n"]) - 1,
                                              raw["n"] - 1)):
            hit("SCAN-LAW", f"{key}: seq {g['seq'].tolist()} touches {t.tolist()} outside "
                            f"(die {d_i}, window end) or out of order")
        if any(x != "failed" for x in v[:-1]) or v[-1] not in ("failed", "hold", "truncated"):
            hit("SCAN-LAW", f"{key}: verdicts {v} — only the last row may be other than failed")
        if (g["is_first_hold"].to_numpy(bool) != (g["verdict"] == "hold").to_numpy()).any():
            hit("SCAN-LAW", f"{key}: first-hold flag != verdict hold")
        if ((g["known_at"].to_numpy(np.int64) != t + lag).any()
                or (g["dir"].to_numpy(np.int64) != (1 if side == "top" else -1)).any()):
            hit("SCAN-LAW", f"{key}: known_at != touch + {lag} or dir != the death side")
        for r in g.itertuples(index=False):
            k = int(r.known_at)
            want_close = int(raw["close"][k]) if k < raw["n"] else -1
            want_era = ("beyond_pin" if want_close < 0 else
                        "tuning" if want_close <= ERA_CUT_T else "holdout")
            if int(r.known_close_ms) != want_close or r.era != want_era:
                hit("SCAN-LAW", f"{key} touch {r.touch_i}: close {r.known_close_ms} / era "
                                f"{r.era}, raw {want_close} / {want_era}")
    holds = sc[sc["is_first_hold"]]
    hk = {(f"BRK_{'mem' if b == 'memory-line' else b}_first", int(r_), s_, int(t_), int(k_))
          for b, r_, s_, t_, k_ in zip(holds["band"], holds["rid"], holds["side"],
                                       holds["touch_i"], holds["known_at"])}
    fe = ev[ev["rule"] == "first"]
    fk = {(e_, int(r_), s_, int(a_), int(k_)) for e_, r_, s_, a_, k_ in
          zip(fe["event"], fe["rid"], fe["side"], fe["anchor_i"], fe["known_at"])}
    if hk != fk:
        hit("SCAN-EVENTS", f"{len(hk - fk)} hold rows not first-hold events, {len(fk - hk)} "
                           f"events without a hold row")
    D = N.events(stem, lens, kind)["deaths"]
    nd = {(int(r.rid), r.side): r for r in D.itertuples(index=False)}
    fd = {(int(r.rid), r.side): r for r in dth.itertuples(index=False)}
    if set(nd) != set(fd):
        hit("DEATHS-SET", f"{len(set(nd) - set(fd))} of N's deaths missing, "
                          f"{len(set(fd) - set(nd))} not N's")
    for k in sorted(set(nd) & set(fd)):
        a_, b_ = nd[k], fd[k]
        if (int(a_.die_i), int(a_.dir), int(a_.known_close_ms)) != (
                int(b_.die_i), int(b_.dir), int(b_.known_close_ms)) \
                or not same8(a_.boundary, b_.boundary):
            hit("DEATHS-SET", f"{k}: filed die {b_.die_i} dir {b_.dir} boundary {b_.boundary}, "
                              f"N {a_.die_i} {a_.dir} {a_.boundary}")
        for band in SCAN_BANDS_T:
            g = sc[(sc["band"] == band) & (sc["rid"] == k[0]) & (sc["side"] == k[1])]
            g = g.sort_values("seq", kind="mergesort")
            last = g["verdict"].iloc[-1] if len(g) else None
            want_end = ("no-touch" if last is None else "failed-out" if last == "failed"
                        else last)
            want_hold = int(g["touch_i"].iloc[-1]) if last == "hold" else -1
            sl = SLUG_T[band]
            got = (int(getattr(b_, f"n_touches_{sl}")), getattr(b_, f"end_{sl}"),
                   int(getattr(b_, f"hold_touch_i_{sl}")))
            if got != (len(g), want_end, want_hold):
                hit("DEATHS-END", f"{k} {band}: filed {got}, from R4_SCAN "
                                  f"{(len(g), want_end, want_hold)}")
    return [f"{det}: {tag}: {n_} finding(s), e.g. {first[det]}" for det, n_ in sorted(cnt.items())]


def scan_break():
    cell = ("SOLUSDT", "4h", "calibrated")
    sc, dth, ev = (_cell_rows(filed(x), *cell) for x in ("R4_SCAN", "R4_DEATHS", "R4_EVENTS"))
    multi = (sc.groupby(["band", "rid", "side"]).size() >= 3)
    b0, r0, s0 = multi[multi].index[0]
    seq_ = sc[(sc["band"] == b0) & (sc["rid"] == r0) & (sc["side"] == s0)]

    def dropped():
        i = seq_.index[seq_["seq"] == 0][0]
        return scan_findings(sc.drop(index=i), dth, ev, *cell)

    def mid_hold():
        d = sc.copy()
        i = seq_.index[seq_["seq"] == 0][0]
        d.loc[i, "verdict"] = "hold"
        d.loc[i, "is_first_hold"] = True
        return scan_findings(d, dth, ev, *cell)

    def relabelled():
        d = dth.copy()
        i = d.index[d["end_tap89"] == "hold"][0]
        d.loc[i, "end_tap89"] = "failed-out"
        return scan_findings(sc, d, ev, *cell)

    return plants([
        ("an evaluated failed touch dropped from a copy of R4_SCAN", "SCAN-SET", dropped),
        ("a failed touch re-filed as a hold mid-sequence (copy)", "SCAN-LAW", mid_hold),
        ("a death's tap89 end relabelled hold -> failed-out (copy of R4_DEATHS)", "DEATHS-END",
         relabelled),
    ])


def scan_real():
    sc_all, d_all, ev_all = filed("R4_SCAN"), filed("R4_DEATHS"), filed("R4_EVENTS")
    by = {k: g for k, g in sc_all.groupby(["asset", "lens", "scale_kind"], sort=True)}
    bd = {k: g for k, g in d_all.groupby(["asset", "lens", "scale_kind"], sort=True)}
    be = {k: g for k, g in ev_all.groupby(["asset", "lens", "scale_kind"], sort=True)}
    bad = []
    cells = all_cells()
    for cell in cells:
        bad += scan_findings(by.get(cell, sc_all.iloc[:0]), bd.get(cell, d_all.iloc[:0]),
                             be.get(cell, ev_all.iloc[:0]), *cell)
    extra = sorted((set(by) | set(bd)) - set(cells))
    if extra:
        bad.append(f"SCAN-SET: cells outside the commission {extra[:3]}")
    v = sc_all["verdict"].value_counts().to_dict()
    ends = {b: d_all[f"end_{SLUG_T[b]}"].value_counts().to_dict() for b in SCAN_BANDS_T}
    return (not bad), (f"{len(cells)} cells: {len(sc_all)} evaluated touches == N's scan rows "
                       f"(verdicts {dict(sorted(v.items()))}) under the typed scan law, every "
                       f"hold row == a first-hold event; {len(d_all)} deaths == N's, each "
                       f"band's touch count / end / hold touch re-derived from R4_SCAN: ends "
                       f"{ {b: dict(sorted(x.items())) for b, x in ends.items()} }"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-OUTCOME
def outcome_selection() -> pd.DataFrame:
    f = filed("R4_EVENTS")
    rng = np.random.default_rng(SEED)
    pick = []
    for s in CLASSIC5_T:
        for L in LENSES_T["CLASSIC5"]:
            g = _cell_rows(f, s, L, "calibrated").sort_values(["known_at", "event", "rid"],
                                                               kind="mergesort")
            pick.append(g.tail(2))
            rest = g.iloc[:-2]
            pick.append(rest.iloc[sorted(rng.choice(len(rest), 2, replace=False))])
    for s in UNSEEN12_T:
        g = _cell_rows(f, s, "1d", "frozen3.0").sort_values(["known_at", "event", "rid"],
                                                             kind="mergesort")
        if len(g):
            pick.append(g.iloc[[int(rng.integers(len(g)))]])
    return pd.concat(pick, ignore_index=True)


def outcome_findings(got: pd.DataFrame) -> list[str]:
    bad = []
    cnt = {}
    for r in got.itertuples(index=False):
        raw = raw_bars(r.asset, r.lens)
        k = int(np.searchsorted(raw["close"], int(r.known_close_ms)))
        tag = f"{r.asset} {r.lens} {r.scale_kind} {r.event} anchor {r.anchor_i}"
        if k >= raw["n"] or int(raw["close"][k]) != int(r.known_close_ms) or k != int(r.known_at):
            bad.append(f"KNOWN-AT: {tag}: filed bar {r.known_at}, raw bar {k}")
            continue
        c, a, d = raw["c"], raw["atr"], int(r.dir)
        toll = (TOLL_BPS_T / 10_000) * c[k] / a[k]
        if not same8(r.toll_atr_evt, toll):
            cnt["TOLL"] = cnt.get("TOLL", 0) + 1
            bad.append(f"TOLL: {tag}: filed {r.toll_atr_evt!r}, raw {toll!r}")
        for hn, H in HOR_T.items():
            cens = k + H > raw["n"] - 1
            fc = bool(getattr(r, f"cens_{hn}"))
            ft, fm, fa = (getattr(r, f"term_{hn}"), getattr(r, f"mfe_{hn}"),
                          getattr(r, f"mae_{hn}"))
            if fc != cens or (cens and not (np.isnan(ft) and np.isnan(fm) and np.isnan(fa))):
                bad.append(f"CENSOR: {tag} {hn}: k {k} + {H} vs n - 1 = {raw['n'] - 1}: typed "
                           f"censored {cens}, filed {fc} with term {ft!r}")
                continue
            if cens:
                cnt[f"cens_{hn}"] = cnt.get(f"cens_{hn}", 0) + 1
                continue
            term = d * (c[k + H] - c[k]) / a[k]
            hi, lo = raw["h"][k + 1:k + H + 1].max(), raw["l"][k + 1:k + H + 1].min()
            mfe = ((hi - c[k]) if d > 0 else (c[k] - lo)) / a[k]
            mae = ((c[k] - lo) if d > 0 else (hi - c[k])) / a[k]
            if not same8(ft, term):
                bad.append(f"TERM: {tag} {hn}: filed {ft!r}, raw {term!r}")
            if not (same8(fm, mfe) and same8(fa, mae)):
                bad.append(f"MFE-MAE: {tag} {hn}: filed {fm!r}/{fa!r}, raw {mfe!r}/{mae!r}")
    return bad


def _rebuilt(sel: pd.DataFrame) -> pd.DataFrame:
    """The selected events re-extracted from R.real_events (under whatever
    mutation is live), keyed as filed."""
    parts = []
    for (s, L, k), g in sel.groupby(["asset", "lens", "scale_kind"], sort=True):
        ev = R.real_events(s, L, k)
        parts.append(ev.merge(g[R.EVENTS_KEY], on=R.EVENTS_KEY, how="inner"))
    return pd.concat(parts, ignore_index=True)


def _shortened_ledger(tape, evf, bps):
    """SABOTAGE: the horizon shortened to the tape's end (never censored)."""
    led = R.C.outcome_ledger(tape, evf, R._stub_view(tape.n), bps).drop(columns=list(R._AT_COLS))
    k = led["known_at"].to_numpy(np.int64)
    sg = led["sgn"].to_numpy(float)
    ks = np.clip(k, 0, tape.n - 1)
    for hn, H in HOR_T.items():
        e = np.minimum(k + H, tape.n - 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            led[f"term_{hn}"] = sg * (tape.c[e] - tape.c[ks]) / tape.atr[ks]
        led[f"cens_{hn}"] = False
    return led


def outcome_break():
    sel = outcome_selection()
    cen = sel[sel["cens_H100"]]
    tgt = cen[cen["asset"] == "BTCUSDT"].head(4) if len(cen) else sel.head(4)

    def shortened():
        with mutated(R, "_ledger", _shortened_ledger):
            return outcome_findings(_rebuilt(tgt))

    def half_toll():
        orig = R._ledger
        with mutated(R, "_ledger", lambda t, e, b: orig(t, e, b / 2.0)):
            return outcome_findings(_rebuilt(sel.head(3)))

    return plants([
        ("the horizon shortened to the tape's end (module mutation)", "CENSOR", shortened),
        ("a half toll (5 bps round trip)", "TOLL", half_toll),
    ])


def outcome_real():
    sel = outcome_selection()
    bad = outcome_findings(sel)
    n20, n100 = int(sel["cens_H20"].sum()), int(sel["cens_H100"].sum())
    if len(sel) < 30:
        bad.append(f"SELECTION: {len(sel)} < 30 events")
    if n20 == 0 or n100 == n20:
        bad.append(f"SELECTION: censored cases H20 {n20} / H100 {n100} — the typed rule must "
                   f"hold an H20-censored AND an H100-only-censored case")
    return (not bad), (f"{len(sel)} events (every CLASSIC5 lens cell's last two + two seeded; "
                       f"one per UNSEEN12 1d frozen cell) hand-computed from raw bars: known_at, "
                       f"censor flags, H20/H100 term, MFE/MAE and toll equal at 8 dp; censored "
                       f"H20 {n20}, H100 {n100}" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-BASE
TIES: dict = {"mean": 0}


def mean_ok(filed_v, t: list) -> bool:
    """THE MEAN'S TIE LAW (typed): the filed mean equals, at 8 dp, the float64 sum
    of the anchors' filed terms — taken in the FILED row order, a pool's members in
    panel order — over n; save at a half-unit tie in the 8th decimal (within 1e-5 of
    a unit: far above any summation-order error of these n, far below any change of
    the anchor set), where the order of a float sum may pick either neighbour and
    both are the filed value's legal forms."""
    if not t:
        return bool(np.isnan(float(filed_v)))
    x = float(np.sum(np.asarray(t, dtype=float))) / len(t)
    y = x * 1e8
    fl = math.floor(y)
    if abs((y - fl) - 0.5) <= 1e-5:
        ok = float(r8(filed_v)) in (float(r8(fl / 1e8)), float(r8((fl + 1) / 1e8)))
        TIES["mean"] += int(ok and not bool(same8(filed_v, x)))   # the exception USED
        return ok
    return bool(same8(filed_v, x))


def ref_stats(parts: list, pooled: bool) -> dict:
    """THIS FILE's grid arithmetic over one row's anchors — `parts` = one dict per
    member (a pool: every member in panel order) holding n_events, n_ok (not a
    bad ATR), the uncensored anchors' terms t / own tolls tl (/ mfe / mae), and
    toll_ok (every non-bad anchor's toll).  Typed laws: n = uncensored non-bad
    anchors; median of the terms; q25 / q75 by the linear rule; hit_rate = share
    of terms > 0; hit_rate_net = share of term - own toll > 0; toll = the median
    of the row's uncensored anchors' tolls, a POOL's = the MAX over members with
    n > 0 (the binding toll); toll_atr_all = the median over every non-bad anchor
    (a pool: the max over members); NET = median - toll, each at 8 dp."""
    t = [x for q in parts for x in q["t"]]
    tl = [x for q in parts for x in q["tl"]]
    n = len(t)
    ne = sum(q["n_events"] for q in parts)
    nok = sum(q["n_ok"] for q in parts)
    r = {"n_events": ne, "n": n, "n_censored": nok - n, "n_bad_atr": ne - nok, "t": t}
    own_all = [statistics.median(q["toll_ok"]) for q in parts if q["toll_ok"]]
    r["toll_atr_all"] = ((max(own_all) if own_all else np.nan) if pooled
                         else (own_all[0] if own_all else np.nan))
    nanf = ("median_term", "mean_term", "q25_term", "q75_term", "hit_rate", "hit_rate_net",
            "median_mfe", "median_mae", "toll_atr", "net")
    if not n:
        r.update({k: np.nan for k in nanf})
        r["binding_over_n_assets"] = 0
        return r
    srt = sorted(t)
    r["median_term"] = statistics.median(t)
    r["mean_term"] = float(np.sum(np.asarray(t, dtype=float))) / n
    r["q25_term"], r["q75_term"] = q_linear(srt, 0.25), q_linear(srt, 0.75)
    r["hit_rate"] = sum(1 for x in t if x > 0) / n
    r["hit_rate_net"] = sum(1 for x, w in zip(t, tl) if x - w > 0) / n
    if all("mfe" in q for q in parts):
        r["median_mfe"] = statistics.median([x for q in parts for x in q["mfe"]])
        r["median_mae"] = statistics.median([x for q in parts for x in q["mae"]])
    else:
        r["median_mfe"] = r["median_mae"] = None          # not checked (the base)
    if pooled:
        mt = [statistics.median(q["tl"]) for q in parts if q["t"]]
        r["toll_atr"], r["binding_over_n_assets"] = max(mt), len(mt)
    else:
        r["toll_atr"], r["binding_over_n_assets"] = statistics.median(tl), 1
    r["net"] = float(r8(float(r8(r["median_term"])) - float(r8(r["toll_atr"]))))
    return r


def q_linear(srt: list, q: float) -> float:
    """THE LINEAR QUANTILE RULE (typed; numpy's 'linear' arithmetic): position
    q x (m - 1) between the order statistics a = s[floor], b = s[floor + 1];
    a + (b - a) x frac below frac 0.5, b - (b - a) x (1 - frac) from 0.5 up."""
    m = len(srt)
    pos = q * (m - 1)
    lo = int(math.floor(pos))
    fr = pos - lo
    a_, b_ = srt[lo], srt[min(lo + 1, m - 1)]
    d_ = b_ - a_
    return (b_ - d_ * (1 - fr)) if fr >= 0.5 else (a_ + d_ * fr)


def base_terms(stem, lens, kind, law, cell, direction, era) -> dict:
    """ONE asset's anchors of ONE base cell by a plain loop over every bar of L:
    the L+1 cell from N.nest_at at each close with this file's partition and cell
    laws ('NA' on every bar where the commission has no L+1); terms / tolls from
    raw bars, each filed at 8 dp (the census's filing law).  Anchors in the
    module's order (long bars, then short bars).  {horizon: part for ref_stats}."""
    raw = raw_bars(stem, lens)
    n, c, a = raw["n"], raw["c"], raw["atr"]
    l1 = HAS_L1_T[(panel_of(stem), lens)]
    if l1:
        U = LADDER_T[lens]
        nv = N.nest_at(stem, raw["close"], kind)
        st = nv[f"{U}_state"].to_numpy()
        pc = nv[f"{U}_pct"].to_numpy(float)
        ct = nv[f"{lens}_coin_top"].fillna(False).to_numpy(bool)
        cb = nv[f"{lens}_coin_bot"].fillna(False).to_numpy(bool)
        ctm = nv[f"{lens}_coin_top_mem"].fillna(False).to_numpy(bool)
        cbm = nv[f"{lens}_coin_bot_mem"].fillna(False).to_numpy(bool)
    dirs = DIRSET_T[direction]
    out = {hn: {"n_events": 0, "n_ok": 0, "t": [], "tl": [], "toll_ok": []} for hn in HOR_T}
    for d in (1, -1):
        if d not in dirs:
            continue
        for k in range(n):
            close = int(raw["close"][k])
            if era != "ALL" and (("tuning" if close <= ERA_CUT_T else "holdout") != era):
                continue
            if cell != "ALL":
                if not l1:
                    here = "NA"
                else:
                    coin = {"record": ct[k] or cb[k], "mem_twin": ctm[k] or cbm[k],
                            "topside": ct[k], "botside": cb[k],
                            "own_side_brk": ct[k] if d == 1 else cb[k],
                            "own_side_sfp": cb[k] if d == 1 else ct[k],
                            "own_side_brk_mem": ctm[k] if d == 1 else cbm[k],
                            "own_side_sfp_mem": cbm[k] if d == 1 else ctm[k]}[law]
                    here = typed_cell(d, st[k] or "NONE", pc[k], bool(coin))
                if here != cell:
                    continue
            for hn, H in HOR_T.items():
                x = out[hn]
                x["n_events"] += 1
                if not a[k] > 0:
                    continue
                x["n_ok"] += 1
                toll = float(np.round((TOLL_BPS_T / 10_000) * c[k] / a[k], 8))
                x["toll_ok"].append(toll)
                if k + H > n - 1:
                    continue
                x["t"].append(float(np.round(d * (c[k + H] - c[k]) / a[k], 8)))
                x["tl"].append(toll)
    return out


def base_loop(stem, lens, kind, law, cell, direction, era) -> dict:
    """ONE FULL base cell (an asset, or a POOL of its members in panel order) by
    the plain loop, through this file's grid arithmetic."""
    pooled = stem.startswith("POOLED:")
    mem = PANELS_T[stem.split(":")[1]] if pooled else (stem,)
    parts = [base_terms(s, lens, kind, law, cell, direction, era) for s in mem]
    return {hn: ref_stats([q[hn] for q in parts], pooled) for hn in HOR_T}


BASE_STAT_T = ("median_term", "hit_rate", "hit_rate_net", "toll_atr", "toll_atr_all", "net")


def base_findings(rows: pd.DataFrame, spec: tuple, det: str = "BASE") -> list[str]:
    stem, lens, kind, law, cell, direction, era = spec
    want = base_loop(*spec)
    bad = []
    for hn in HOR_T:
        r = rows[(rows["asset"] == stem) & (rows["lens"] == lens) & (rows["scale_kind"] == kind)
                 & (rows["cell_law"] == law) & (rows["cell"] == cell)
                 & (rows["direction"] == direction) & (rows["era"] == era)
                 & (rows["horizon"] == hn)]
        tag = f"{stem} {lens} {kind} {law} {cell} {direction} {era} {hn}"
        if len(r) != 1:
            bad.append(f"{det}-N: {tag}: {len(r)} filed rows")
            continue
        r = r.iloc[0]
        w = want[hn]
        for f_ in ("n_events", "n", "n_censored", "n_bad_atr", "binding_over_n_assets"):
            if int(r[f_]) != int(w[f_]):
                bad.append(f"{det}-N: {tag}: {f_} filed {int(r[f_])}, loop {w[f_]}")
        for f_ in BASE_STAT_T:
            if not same8(r[f_], w[f_]):
                bad.append(f"{det}-STAT: {tag}: {f_} filed {r[f_]!r}, loop {w[f_]!r}")
        if not mean_ok(r["mean_term"], w["t"]):
            bad.append(f"{det}-STAT: {tag}: mean_term filed {r['mean_term']!r}, loop "
                       f"{w['mean_term']!r}")
    return bad


def base_break():
    spec = BASE_CELLS_T[1]                 # ETHUSDT 4h calibrated record EXP_ALIGNED short tuning
    stem, lens, kind = spec[:3]
    orig = R._base_cells

    def late(s, L, k):
        cells = orig(s, L, k)
        return {law: (np.concatenate([cl[1:], cl[-1:]]), np.concatenate([cs[1:], cs[-1:]]))
                for law, (cl, cs) in cells.items()}

    def one_bar_late():
        with mutated(R, "_base_cells", late):
            rows = R.asset_real(stem, "CLASSIC5", lens, kind)["base"]
        return base_findings(rows, spec)

    def shortened():
        end = BASE_CELLS_T[-1]             # the unconditional holdout cell: it holds the tape end
        with mutated(R, "_ledger", _shortened_ledger):
            rows = R.asset_real(end[0], "CLASSIC5", end[1], end[2])["base"]
        return base_findings(rows, end)

    return plants([
        ("the base cell read one bar late (look-ahead; module mutation)", "BASE-", one_bar_late),
        ("the base horizon shortened to the tape's end (module mutation)", "BASE-N", shortened),
    ])


def base_real():
    rows = filed("R4_BASE")
    bad, lines = [], []
    for spec in BASE_CELLS_T:
        bad += base_findings(rows, spec)
        r = rows[(rows["asset"] == spec[0]) & (rows["lens"] == spec[1])
                 & (rows["scale_kind"] == spec[2]) & (rows["cell_law"] == spec[3])
                 & (rows["cell"] == spec[4]) & (rows["direction"] == spec[5])
                 & (rows["era"] == spec[6]) & (rows["horizon"] == "H20")]
        if len(r):
            lines.append(f"{'/'.join(spec)} n_events {int(r['n_events'].iloc[0])} H20 n "
                         f"{int(r['n'].iloc[0])}")
    return (not bad), (f"{len(BASE_CELLS_T)} full per-asset base cells (one per lens + the "
                       f"own-side twins, record and memory-line), both horizons, equal a plain "
                       f"loop over every bar on n_events / n / n_censored / n_bad_atr / median / "
                       f"mean / hit rates / toll / toll_atr_all / NET: {lines}"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-GRIDSTAT
GRID_INT_T = ("n_events", "n", "n_censored", "n_bad_atr", "binding_over_n_assets")
GRID_FLOAT_T = ("median_term", "q25_term", "q75_term", "hit_rate", "hit_rate_net", "median_mfe",
                "median_mae", "toll_atr", "toll_atr_all", "net")


def ev_index(ev: pd.DataFrame) -> dict:
    """The FILED events as arrays per (asset, lens, scale, event), in the filed row
    order; era by the typed cut on the filed known_at close (never the filed era)."""
    out = {}
    for key, g in ev.groupby(["asset", "lens", "scale_kind", "event"], sort=True):
        d = {"dir": g["dir"].to_numpy(np.int64),
             "era": np.where(g["known_close_ms"].to_numpy(np.int64) <= ERA_CUT_T, "tuning",
                             "holdout"),
             "bad": g["bad_atr"].to_numpy(bool), "toll": g["toll_atr_evt"].to_numpy(float)}
        for law, col in LAWCOL_T.items():
            d[law] = g[col].to_numpy(object)
        for hn in HOR_T:
            d[f"cens_{hn}"] = g[f"cens_{hn}"].to_numpy(bool)
            for x in ("term", "mfe", "mae"):
                d[f"{x}_{hn}"] = g[f"{x}_{hn}"].to_numpy(float)
        out[key] = d
    return out


def ev_part(idx: dict, asset, lens, kind, event, law, cell, direction, era, hn) -> dict:
    """ONE member's anchors of one grid row, by the typed maps."""
    d = idx.get((asset, lens, kind, event))
    if d is None:
        return {"n_events": 0, "n_ok": 0, "t": [], "tl": [], "mfe": [], "mae": [],
                "toll_ok": []}
    m = np.isin(d["dir"], DIRSET_T[direction])
    if cell != "ALL":
        m &= d[law] == cell
    if era != "ALL":
        m &= d["era"] == era
    ok = m & ~d["bad"]
    S = ok & ~d[f"cens_{hn}"]
    return {"n_events": int(m.sum()), "n_ok": int(ok.sum()), "t": d[f"term_{hn}"][S].tolist(),
            "tl": d["toll"][S].tolist(), "mfe": d[f"mfe_{hn}"][S].tolist(),
            "mae": d[f"mae_{hn}"][S].tolist(), "toll_ok": d["toll"][ok].tolist()}


def gridstat_findings(G: pd.DataFrame, idx: dict) -> tuple[list[str], int]:
    """Every row of G against this file's statistics on the filed events."""
    cnt, first, n_rows = {}, {}, 0
    for r in G.itertuples(index=False):
        pooled = r.asset.startswith("POOLED:")
        mem = PANELS_T[r.asset.split(":")[1]] if pooled else (r.asset,)
        w = ref_stats([ev_part(idx, s, r.lens, r.scale_kind, r.event, r.cell_law, r.cell,
                               r.direction, r.era, r.horizon) for s in mem], pooled)
        n_rows += 1
        tag = (f"{r.asset} {r.lens} {r.scale_kind} {r.event} {r.cell_law} {r.cell} "
               f"{r.direction} {r.era} {r.horizon}")
        for f_ in GRID_INT_T:
            if int(getattr(r, f_)) != int(w[f_]):
                cnt[f_] = cnt.get(f_, 0) + 1
                first.setdefault(f_, f"{tag}: row {int(getattr(r, f_))}, referee {w[f_]}")
        for f_ in GRID_FLOAT_T:
            if not same8(getattr(r, f_), w[f_]):
                cnt[f_] = cnt.get(f_, 0) + 1
                first.setdefault(f_, f"{tag}: row {getattr(r, f_)!r}, referee {w[f_]!r}")
        if not mean_ok(r.mean_term, w["t"]):
            cnt["mean_term"] = cnt.get("mean_term", 0) + 1
            first.setdefault("mean_term", f"{tag}: row {r.mean_term!r}")
    return [f"GRIDSTAT: {f_} differs on {n_} row(s), e.g. {first[f_]}"
            for f_, n_ in sorted(cnt.items())], n_rows


def unit_rebuilt(panel: str, lens: str, kind: str) -> tuple[pd.DataFrame, pd.DataFrame]:
    """The unit's grid and POOLED base rows rebuilt by the module's own per-asset
    step (R.asset_real) and pool step (R.pooled_rows) under whatever mutation is
    live — the break legs' material (never filed)."""
    stems = PANELS_T[panel]
    A = {s: R.asset_real(s, panel, lens, kind) for s in stems}
    ev = pd.concat([A[s]["events"] for s in stems], ignore_index=True)
    gp = R.pooled_rows(panel, lens, kind, stems, ev, R.event_groups(ev, panel, lens),
                       {s: A[s]["ev_rows"] for s in stems}, R.EV_KEYCOLS)
    bl = pd.concat([A[s]["base_led"] for s in stems], ignore_index=True)
    bp = R.pooled_rows(panel, lens, kind, stems, bl, R.base_groups(bl, panel, lens),
                       {s: A[s]["base_rows"] for s in stems}, R.BASE_KEYCOLS)
    return pd.concat([A[s]["grid"] for s in stems] + [gp], ignore_index=True), bp


def _dir_swapped(d, direction):
    """SABOTAGE: long and short swapped in the grouping."""
    return np.ones(len(d), bool) if direction == "both" else d == -{"long": 1, "short": -1}[direction]


def _toll_from_all(orig):
    """SABOTAGE: a pooled row's binding toll taken from the members' ALL-cell rows."""
    def f(led, groups, asset, lens, kind, sm, bps, src, tolls=None):
        if tolls is not None:
            def allkey(k):
                if len(k) == 4 and k[2] != "NA":
                    return (k[0], "record", "ALL", k[3])
                if len(k) == 3 and k[1] != "NA":
                    return ("record", "ALL", k[2])
                return k
            tolls = {k: tolls[allkey(k)] for k in tolls}
        return orig(led, groups, asset, lens, kind, sm, bps, src, tolls=tolls)
    return f


def gridstat_break():
    idx = ev_index(filed("R4_EVENTS"))
    panel, lens, kind = GRIDSTAT_UNIT_T
    pool_spec = next(x for x in BASE_POOL_T if x[:3] == (POOL_T[panel], lens, kind))
    cache: dict = {}

    def rebuilt(name, obj, attr, value):
        if name not in cache:
            with mutated(obj, attr, value):
                cache[name] = unit_rebuilt(panel, lens, kind)
        return cache[name]

    def swapped():
        return gridstat_findings(rebuilt("M1", R, "_dir_mask", _dir_swapped)[0], idx)[0]

    def by_mem_col():
        cols = dict(R.EV_LAW_COL, record="cell_mem")
        return gridstat_findings(rebuilt("M2", R, "EV_LAW_COL", cols)[0], idx)[0]

    def toll_all_grid():
        g = rebuilt("M4", R, "packed_rows", _toll_from_all(R.packed_rows))[0]
        return gridstat_findings(g[g["asset"] == POOL_T[panel]], idx)[0]

    def toll_all_base():
        bp = rebuilt("M4", R, "packed_rows", _toll_from_all(R.packed_rows))[1]
        return base_findings(bp, pool_spec, det="BASESTAT-POOL")

    return plants([
        ("long / short swapped in the event grouping (module mutation)",
         "GRIDSTAT: n_events", swapped),
        ("the record cells partitioned by the memory-line twin's column (module mutation)",
         "GRIDSTAT: n_events", by_mem_col),
        ("the pooled grid toll taken from the members' ALL-cell rows (module mutation)",
         "GRIDSTAT: toll_atr", toll_all_grid),
        ("the pooled BASE toll taken from the members' ALL-cell rows (module mutation)",
         "BASESTAT-POOL-STAT", toll_all_base),
    ])


def gridstat_real():
    G = filed("R4_GRID")
    idx = ev_index(filed("R4_EVENTS"))
    t0 = TIES["mean"]
    bad, n_rows = gridstat_findings(G, idx)
    n_tie = TIES["mean"] - t0
    pooled = int(G["asset"].str.startswith("POOLED:").sum())
    B = filed("R4_BASE")
    lines = []
    for spec in BASE_POOL_T:
        bad += base_findings(B, spec, det="BASESTAT-POOL")
        r = B[(B["asset"] == spec[0]) & (B["lens"] == spec[1]) & (B["scale_kind"] == spec[2])
              & (B["cell_law"] == spec[3]) & (B["cell"] == spec[4]) & (B["direction"] == spec[5])
              & (B["era"] == spec[6]) & (B["horizon"] == "H20")]
        if len(r):
            lines.append(f"{'/'.join(spec)} H20 n {int(r['n'].iloc[0])} toll "
                         f"{float(r['toll_atr'].iloc[0]):.6f} over "
                         f"{int(r['binding_over_n_assets'].iloc[0])} assets")
    if n_rows != len(G) or n_rows == 0:
        bad.append(f"GRIDSTAT: {n_rows} rows compared of {len(G)}")
    return (not bad), (f"EVERY R4_GRID row ({n_rows}: {n_rows - pooled} per asset, {pooled} "
                       f"pooled) == this file's statistics on the filed R4_EVENTS (n_events / n "
                       f"/ n_censored / n_bad_atr / median / q25 / q75 / hit rates / MFE / MAE / "
                       f"toll / toll_atr_all / NET / binding count exact at 8 dp; mean exact at "
                       f"8 dp on all but {n_tie} rows, which sit on a half-unit tie and carry "
                       f"its other neighbour); {len(BASE_POOL_T)} pooled base rows == the members' plain "
                       f"loops with the binding toll: {lines}"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-NULL
def typed_real_boxes(stem: str, lens: str, kind: str) -> dict:
    """The real box set by THIS FILE's law: the confirmed macro ranges in list
    order, life = die_i - confirm_i (dead) else n - confirm_i, height =
    (top0 - bottom0) / ATR[confirm] (typed ATR), the m + 1 gaps."""
    raw = raw_bars(stem, lens)
    n = raw["n"]
    b = N.bundle11(stem, lens, kind)
    rows, gaps, prev = [], [], 0
    for r in b["v2"]["macro"]["ranges"]:
        if r.confirm_i < 0:
            continue
        a_ = int(r.confirm_i)
        end = int(r.die_i) if (r.state == "DEAD" and r.die_i >= 0) else n
        gaps.append(a_ - prev)
        rows.append({"src_rid": int(r.rid), "confirm_i": a_, "life": end - a_,
                     "height_atr": float((r.top0 - r.bottom0) / raw["atr"][a_])})
        prev = end
    gaps.append(n - prev)
    return {"rows": rows, "gaps": gaps, "n": n}


def typed_schedule(real: dict, stem: str, lens: str, kind: str, draw: int,
                   seed: int = SEED, with_identity: bool = False):
    """THIS FILE's draw law: default_rng([seed + draw, crc32('asset|lens|scale')]);
    gaps permuted, u's, then the order of the pairs; a lead gap < 14 swapped with
    the first gap >= 14."""
    rng = np.random.default_rng([seed + draw,
                                 zlib.crc32(f"{stem}|{lens}|{kind}".encode("utf-8"))])
    rows, gaps = real["rows"], real["gaps"]
    m = len(rows)
    perm = [int(x) for x in rng.permutation(m + 1)]
    u = rng.random(m)
    order = [int(x) for x in rng.permutation(m)]
    g = [gaps[i] for i in perm]
    if m and g[0] < LEAD_FLOOR_T:
        j = next(i for i in range(1, m + 1) if g[i] >= LEAD_FLOOR_T)
        g[0], g[j] = g[j], g[0]
        perm[0], perm[j] = perm[j], perm[0]
    ident = perm == list(range(m + 1)) and order == list(range(m))
    out, pos = [], g[0] if g else 0
    for k in range(m):
        x = rows[order[k]]
        out.append({"box": k + 1, "src_rid": x["src_rid"], "confirm_i": pos, "life": x["life"],
                    "height_atr": x["height_atr"], "u": float(u[k])})
        pos += x["life"] + g[k + 1]
    return (out, ident) if with_identity else out


def seed_is_real(real: dict, sched: list) -> bool:
    """The seed's OWN schedule puts every box at its real range's confirm bar (a
    small m makes the identity permutation a fair draw: m = 2 -> 1 in 12)."""
    rpos = {x["src_rid"]: x["confirm_i"] for x in real["rows"]}
    return bool(sched) and all(rpos[b["src_rid"]] == b["confirm_i"] for b in sched)


def repro_findings(boxes: pd.DataFrame, stem, lens, kind, real: dict, draws) -> list[str]:
    bad = []
    for d in draws:
        want = typed_schedule(real, stem, lens, kind, d)
        got = boxes[boxes["draw"] == d].sort_values("box")
        tag = f"{stem} {lens} {kind} draw {d}"
        if len(got) != len(want):
            bad.append(f"SEED-REPRO: {tag}: {len(got)} boxes, the seed draws {len(want)}")
            continue
        for w, g in zip(want, got.itertuples(index=False)):
            if (int(g.src_rid), int(g.confirm_i), int(g.life)) != (w["src_rid"], w["confirm_i"],
                                                                   w["life"]) \
                    or not (same8(g.height_atr, w["height_atr"]) and same8(g.u, w["u"])):
                bad.append(f"SEED-REPRO: {tag} box {g.box}: filed (rid {g.src_rid}, confirm "
                           f"{g.confirm_i}, life {g.life}, u {g.u}) vs the seed's (rid "
                           f"{w['src_rid']}, confirm {w['confirm_i']}, life {w['life']}, u "
                           f"{w['u']:.8f})")
                break
    return bad


def multiset_findings(boxes: pd.DataFrame, real: dict, tag: str, stem: str, lens: str,
                      kind: str) -> list[str]:
    bad = []
    rg = sorted(real["gaps"])
    rp = sorted((x["life"], float(r8(x["height_atr"]))) for x in real["rows"])
    rpos = {x["src_rid"]: x["confirm_i"] for x in real["rows"]}
    for d, g in boxes.groupby("draw", sort=True):
        g = g.sort_values("confirm_i")
        ci, li = g["confirm_i"].to_numpy(np.int64), g["life"].to_numpy(np.int64)
        gaps = ([int(ci[0])] if len(ci) else []) + [int(ci[i + 1] - (ci[i] + li[i]))
                                                    for i in range(len(ci) - 1)]
        gaps.append(int(real["n"] - (ci[-1] + li[-1])) if len(ci) else int(real["n"]))
        pairs = sorted(zip(li.tolist(), r8(g["height_atr"]).tolist()))
        if sorted(gaps) != rg or pairs != rp:
            bad.append(f"MULTISET: {tag} draw {d}: gaps {'==' if sorted(gaps) == rg else '!='} "
                       f"real, (life, height) pairs {'==' if pairs == rp else '!='} real")
        at_real = len(g) > 0 and all(rpos.get(int(r_), -1) == int(c_) for r_, c_ in
                                     zip(g["src_rid"], g["confirm_i"]))
        sched, ident = typed_schedule(real, stem, lens, kind, int(d), with_identity=True)
        if at_real and not seed_is_real(real, sched):
            bad.append(f"REAL-POSITIONS: {tag} draw {d}: every box sits at its real range's "
                       f"confirm bar and the seed's own schedule does not — the draw re-uses "
                       f"the real positions")
        if bool(g["identity_perm"].all()) != ident or bool(g["identity_perm"].any()) != ident:
            bad.append(f"SEED-REPRO: {tag} draw {d}: identity_perm filed "
                       f"{sorted(set(g['identity_perm'].tolist()))}, the seed's permutations "
                       f"{'are' if ident else 'are not'} the identity")
    return bad


def _null_boxes_rebuilt(stem, lens, kind) -> pd.DataFrame:
    tape = N.load11(stem, lens)
    b = N.bundle11(stem, lens, kind)
    real = NL.real_box_set(tape, b["v2"]["macro"])
    bands = R.band_memo(tape)
    rows = []
    for d in range(K):
        rows += R.box_rows(stem, lens, kind, d, R.null_draw(stem, lens, kind, tape, real, d, SEED,
                                                            bands))
    return pd.DataFrame(rows)


def null_break():
    cell = ("NEARUSDT", "1d", "frozen3.0")
    real = typed_real_boxes(*cell)

    def real_positions_schedule(real_, rng, keep_order=False):
        rows = real_["boxes"]
        u = rng.random(len(rows))
        boxes = [NL.Box(box=k + 1, src_rid=x["src_rid"], confirm_i=int(x["real_confirm_i"]),
                        life=int(x["life"]), height_atr=float(x["height_atr"]), u=float(u[k]),
                        censored=bool(x["censored"])) for k, x in enumerate(rows)]
        return boxes, {"perm": [], "order": [], "gaps": [], "lead_gap_swapped": False,
                       "identity_perm": True, "own_window_overlap_bars": 0}

    def reuse():
        with mutated(R.NL, "schedule", real_positions_schedule):
            bx = _null_boxes_rebuilt(*cell)
        return (multiset_findings(bx, real, " ".join(cell), *cell)
                + repro_findings(bx, *cell, real, range(K)))

    def shared_stream():
        with mutated(R.NL, "draw_rng", lambda seed, draw, a, L, k:
                     np.random.default_rng(int(seed) + int(draw))):
            bx = _null_boxes_rebuilt(*cell)
        return repro_findings(bx, *cell, real, range(K))

    def moved():
        f = filed("R4_NULL_BOXES")
        bx = _cell_rows(f, *cell).copy()
        i = bx.index[(bx["draw"] == 3) & (bx["box"] == 2)][0]
        bx.loc[i, "confirm_i"] = int(bx.loc[i, "confirm_i"]) + 1
        return multiset_findings(bx, real, " ".join(cell), *cell)

    icell = NULL_INDEP_T[0]
    orig_l1, orig_asm = R._l1, R.assemble

    def l1_late(stem, lens, kind, d, b, kms):
        return orig_l1(stem, lens, kind, d, b, np.asarray(kms, dtype=np.int64) + STEP_T[lens])

    def springs_short(fr, die_bnd):
        f = orig_asm(fr, die_bnd)
        f.loc[(f["family"] == "SFP") & (f["side"] == "bottom"), "dir"] = -1
        return f

    def null_late():
        with mutated(R, "_l1", l1_late):
            got = module_null_values(*icell, NULL_INDEP_DRAWS_T[0])
        return null_indep_findings(*icell, NULL_INDEP_DRAWS_T[0], got)[0]

    def null_springs():
        with mutated(R, "assemble", springs_short):
            got = module_null_values(*icell, NULL_INDEP_DRAWS_T[0])
        return null_indep_findings(*icell, NULL_INDEP_DRAWS_T[0], got)[0]

    return plants([
        ("a draw that re-uses the real positions (NL.schedule bent)", "REAL-POSITIONS", reuse),
        ("a stream shared across cells (NL.draw_rng without the cell key)", "SEED-REPRO",
         shared_stream),
        ("one box moved one bar in a copy of a filed draw", "MULTISET", moved),
        ("the null's L+1 cell read one bar of L late (look-ahead; module mutation)",
         "NULL-INDEP", null_late),
        ("the null's springs (bottom hardens) filed short (module mutation)", "NULL-INDEP",
         null_springs),
    ])


def road_findings(stem, lens, kind) -> list[str]:
    """The null's event road fed the REAL bundle must give N.events' frames — on
    the two frames the null ASSEMBLES itself (the taps' scan with memoised bands,
    the one-shot twin from C.retest_holds); its memory-line frames are N's own
    functions called directly, so comparing them would be a self-comparison."""
    b = N.bundle11(stem, lens, kind)
    fr = R.null_frames(b, R.band_memo(b["tape"]))
    ev = N.events(stem, lens, kind)
    bad = []
    for name, cols in (("scan", ["band", "die_i", "rid", "side", "dir", "seq", "touch_i",
                                 "known_at", "verdict", "is_first_hold", "known_close_ms"]),
                       ("oneshot", ["band", "rid", "side", "die_i", "touch_i", "known_at",
                                    "verdict", "dir", "known_close_ms"])):
        a = fr[name][cols].reset_index(drop=True)
        b_ = ev[name][cols].reset_index(drop=True)
        if not a.equals(b_):
            bad.append(f"NULL-ROAD: {stem} {lens} {kind} {name}: {len(a)} rows vs N's {len(b_)}")
    return bad


_EMA_T: dict = {}


def typed_ema(stem: str, lens: str, period: int) -> np.ndarray:
    """THIS FILE's tap band: the EMA of close on the lens's own bars, alpha = 2 /
    (P + 1), seeded at the first close, NaN (unreadable) for the first P bars."""
    key = (stem, lens, period)
    if key not in _EMA_T:
        c = raw_bars(stem, lens)["c"]
        al = 2.0 / (period + 1.0)
        e = np.empty(len(c))
        prev = None
        for i, v in enumerate(c):
            prev = v if prev is None else prev + al * (v - prev)
            e[i] = prev
        e[:period] = np.nan
        _EMA_T[key] = e
    return _EMA_T[key]


def indep_static_boxes(raw: dict, sched: list) -> tuple[list, list, dict]:
    """THIS FILE's static-box law on the seed's schedule (typed_schedule, unrounded)
    and raw bars: box = [c[a] - u x h, + h], h = height_atr x ATR[a], fixed for its
    life [a, a + life); bar by bar an open breach is updated first (another close
    beyond; a close back inside within 7 bars of the breach bar = a HARDEN, later = a
    lapse), else a close beyond opens one; then, the breach open, the DEATH test: 8
    closes beyond, or one close 1.5 ATR beyond.  -> hardens [(i, box, side, px)],
    deaths [(i, box, side, px)] in bar order, {box: (die_i, die_side, n_harden)}."""
    c, atr, n = raw["c"], raw["atr"], raw["n"]
    hard, dies, fate = [], [], {}
    for b in sched:
        a = int(b["confirm_i"])
        if a >= n:
            break
        h_ = b["height_atr"] * atr[a]
        bot = c[a] - b["u"] * h_
        top = bot + h_
        pend, nh, die = None, 0, (-1, "")
        for i in range(a, min(a + int(b["life"]), n)):
            if pend is None:
                if c[i] > top:
                    pend = ["top", i, 1]
                elif c[i] < bot:
                    pend = ["bottom", i, 1]
            else:
                if (c[i] > top) if pend[0] == "top" else (c[i] < bot):
                    pend[2] += 1
                else:
                    if i - pend[1] <= STATIC_T["dev_return"]:
                        nh += 1
                        hard.append((i, int(b["box"]), pend[0], top if pend[0] == "top" else bot))
                    pend = None
            if pend is not None:
                edge = top if pend[0] == "top" else bot
                beyond_m = (c[i] - edge >= STATIC_T["break_margin"] * atr[i] if pend[0] == "top"
                            else edge - c[i] >= STATIC_T["break_margin"] * atr[i])
                if pend[2] >= STATIC_T["break_n"] or beyond_m:
                    die = (i, pend[0])
                    dies.append((i, int(b["box"]), pend[0], edge))
                    break
        fate[int(b["box"])] = (die[0], die[1], nh)
    return sorted(hard), sorted(dies), fate


def indep_taps(raw: dict, ema: np.ndarray, dies: list, rule: str) -> list:
    """THIS FILE's tap scan on the null's deaths [L-R.6(a)]: per death, the window
    (die, min(die + 400, next death - 1, n - 1)]; a touch = the bar's [low, high]
    meets the EMA and the PRIOR close sat beyond it on the die side; its test over
    touch..touch + 3: FAILED iff a close goes through the EMA by 1.0 ATR (or the EMA
    is unreadable); touch + 3 past the tape = truncated (ends the scan).  'first' =
    the first hold of the scan; 'oneshot' = the first touch's verdict only.
    -> [(known_at, dir, boundary)]."""
    h, l, c, atr, n = raw["h"], raw["l"], raw["c"], raw["atr"], raw["n"]
    H, mg = RETEST_T["hold"], RETEST_T["margin"]
    out = []
    for q, (d_i, _box, side, px) in enumerate(dies):
        nxt = dies[q + 1][0] if q + 1 < len(dies) else n
        end = min(d_i + TTL_T, nxt - 1, n - 1)
        for j in range(d_i + 1, end + 1):
            e0, ep = ema[j], ema[j - 1]
            if not (l[j] <= e0 and h[j] >= e0):
                continue
            if not ((c[j - 1] > ep) if side == "top" else (c[j - 1] < ep)):
                continue
            if j + H >= n:
                break                                   # truncated: never a hold
            failed = False
            for k in range(j, j + H + 1):
                if not np.isfinite(ema[k]) or ((c[k] < ema[k] - mg * atr[k]) if side == "top"
                                               else (c[k] > ema[k] + mg * atr[k])):
                    failed = True
                    break
            if not failed:
                out.append((j + H, 1 if side == "top" else -1, px))
                break
            if rule == "oneshot":
                break
    return out


def indep_record_cells(stem: str, lens: str, kind: str, evs: list, raw: dict) -> list:
    """The record L+1 cell of each null event: N.nest_at at the known_at close,
    this file's coincidence (the event boundary within 0.25 x ATR_L of a live L+1
    boundary) and partition; 'NA' where the commission has no L+1."""
    if not HAS_L1_T[(panel_of(stem), lens)]:
        return ["NA"] * len(evs)
    if not evs:
        return []
    U = LADDER_T[lens]
    nv = N.nest_at(stem, [int(raw["close"][k]) for k, _, _ in evs], kind)
    st = nv[f"{U}_state"].tolist()
    inr = nv[f"{U}_in_range"].fillna(False).to_numpy(bool)
    top, bot = nv[f"{U}_top"].to_numpy(float), nv[f"{U}_bot"].to_numpy(float)
    pct, atr_l = nv[f"{U}_pct"].to_numpy(float), nv[f"{lens}_atr_L"].to_numpy(float)
    out = []
    for i, (_, d, b) in enumerate(evs):
        coin = bool(inr[i]) and (abs(b - top[i]) <= COIN_T * atr_l[i]
                                 or abs(b - bot[i]) <= COIN_T * atr_l[i])
        out.append(typed_cell(d, st[i] or "NONE", pct[i], coin))
    return out


def indep_null_parts(stem: str, lens: str, kind: str, draw: int) -> tuple[dict, list]:
    """ONE asset's null draw rebuilt INDEPENDENTLY: {(event, cell, direction, era,
    horizon): part for ref_stats} over NULL_INDEP_EVENTS_T, and the box-fate
    findings against the filed schedule."""
    raw = raw_bars(stem, lens)
    n, c, a = raw["n"], raw["c"], raw["atr"]
    sched = typed_schedule(typed_real_boxes(stem, lens, kind), stem, lens, kind, draw)
    hard, dies, fate = indep_static_boxes(raw, sched)
    bad = []
    fb = _cell_rows(filed("R4_NULL_BOXES"), stem, lens, kind)
    fb = fb[fb["draw"] == draw]
    nfb = 0
    for r in fb.itertuples(index=False):
        own = fate.get(int(r.box), (-1, "", 0))
        if (int(r.die_i), str(r.die_side) if int(r.die_i) >= 0 else "", int(r.n_harden)) != own:
            nfb += 1
            if nfb == 1:
                bad.append(f"NULL-INDEP: {stem} {lens} {kind} draw {draw} box {r.box}: filed "
                           f"die {r.die_i} {r.die_side} hardens {r.n_harden}, own law {own}")
    evs = {"SFP_harden": [(i, 1 if side == "bottom" else -1, px) for i, _, side, px in hard],
           "BRK_tap89_first": indep_taps(raw, typed_ema(stem, lens, 89), dies, "first"),
           "BRK_tap89_oneshot": indep_taps(raw, typed_ema(stem, lens, 89), dies, "oneshot"),
           "BRK_tap200_first": indep_taps(raw, typed_ema(stem, lens, 200), dies, "first")}
    cells_of = PART_T if HAS_L1_T[(panel_of(stem), lens)] else ("NA",)
    parts = {}
    for ev in NULL_INDEP_EVENTS_T:
        E_ = evs[ev]
        cl = indep_record_cells(stem, lens, kind, E_, raw)
        for cell in ("ALL",) + tuple(cells_of):
            for direction, dset in DIRSET_T.items():
                for era in ERAS_T:
                    for hn, H in HOR_T.items():
                        q = {"n_events": 0, "n_ok": 0, "t": [], "tl": [], "toll_ok": []}
                        for (k, d, _), ce in zip(E_, cl):
                            if d not in dset or (cell != "ALL" and ce != cell):
                                continue
                            if era != "ALL" and (("tuning" if raw["close"][k] <= ERA_CUT_T
                                                  else "holdout") != era):
                                continue
                            q["n_events"] += 1
                            if not a[k] > 0:
                                continue
                            q["n_ok"] += 1
                            toll = float(np.round((TOLL_BPS_T / 10_000) * c[k] / a[k], 8))
                            q["toll_ok"].append(toll)
                            if k + H > n - 1:
                                continue
                            q["t"].append(float(np.round(d * (c[k + H] - c[k]) / a[k], 8)))
                            q["tl"].append(toll)
                        parts[(ev, cell, direction, era, hn)] = q
    return parts, bad


def filed_null_values(asset: str, lens: str, kind: str, draw: int) -> dict:
    f = _cell_rows(filed("R4_NULL"), asset, lens, kind)
    return {(r.event, r.cell, r.direction, r.era, r.horizon):
            (int(getattr(r, f"n_d{draw:02d}")), float(getattr(r, f"net_d{draw:02d}")))
            for r in f.itertuples(index=False)}


def module_null_values(stem: str, lens: str, kind: str, draw: int) -> dict:
    """The module's own null road for one draw (R.null_draw -> R.event_groups ->
    R.packed_rows) under whatever mutation is live — the break legs' material."""
    panel = panel_of(stem)
    tape = N.load11(stem, lens)
    real = NL.real_box_set(tape, N.bundle11(stem, lens, kind)["v2"]["macro"])
    dd = R.null_draw(stem, lens, kind, tape, real, draw, SEED, R.band_memo(tape))
    rec = [(e, "record", c_) for (e, law, c_) in R.event_cells(panel, lens) if law == "record"]
    bps, src = C.toll_bps_for(stem)
    rr = R.packed_rows(dd["ledger"], R.event_groups(dd["ledger"], panel, lens, rec), stem, lens,
                       kind, N.scale_of(stem, lens, kind), bps, src)
    return {(e, cell, direction, r["era"], r["horizon"]): (int(r["n"]), float(r["net"]))
            for (e, law, cell, direction), rows in rr.items() for r in rows}


def null_indep_findings(asset: str, lens: str, kind: str, draw: int, got: dict,
                        parts_by: dict | None = None) -> tuple[list[str], int]:
    """`got` {(event, cell, direction, era, horizon): (n, NET)} (the filed draw, or a
    module re-run) against the independent rebuild — per asset, or a POOL of its
    members (median over every member's anchors, the binding MAX toll)."""
    pooled = asset.startswith("POOLED:")
    mem = PANELS_T[asset.split(":")[1]] if pooled else (asset,)
    bad = []
    if parts_by is None:
        parts_by = {}
    for s_ in mem:
        if s_ not in parts_by:
            parts_by[s_] = indep_null_parts(s_, lens, kind, draw)
        bad += parts_by[s_][1]
    n_cmp, n_bad, first = 0, 0, None
    for key in parts_by[mem[0]][0]:
        w = ref_stats([parts_by[s_][0][key] for s_ in mem], pooled)
        if key not in got:
            bad.append(f"NULL-INDEP: {asset} {lens} {kind} draw {draw} {key}: no filed row")
            continue
        n_cmp += 1
        gn, gnet = got[key]
        if gn != w["n"] or not same8(gnet, w["net"]):
            n_bad += 1
            first = first or (f"{key}: filed n {gn} NET {gnet!r}, own rebuild n {w['n']} NET "
                              f"{w['net']!r}")
    if n_bad:
        bad.append(f"NULL-INDEP: {asset} {lens} {kind} draw {draw}: {n_bad} of {n_cmp} rows "
                   f"differ, e.g. {first}")
    return bad, n_cmp


def indep_null_all() -> tuple[list[str], int, list]:
    bad, n_cmp, lines = [], 0, []
    for stem, lens, kind in NULL_INDEP_T:
        for d in NULL_INDEP_DRAWS_T:
            b_, n_ = null_indep_findings(stem, lens, kind, d, filed_null_values(stem, lens, kind, d))
            bad += b_
            n_cmp += n_
            lines.append(f"{stem} {lens} {kind} d{d}")
    panel, lens, kind, d = NULL_INDEP_POOL_T
    b_, n_ = null_indep_findings(POOL_T[panel], lens, kind, d,
                                 filed_null_values(POOL_T[panel], lens, kind, d))
    bad += b_
    n_cmp += n_
    lines.append(f"{POOL_T[panel]} {lens} {kind} d{d}")
    return bad, n_cmp, lines


def null_real():
    boxes = filed("R4_NULL_BOXES")
    by = {k: g for k, g in boxes.groupby(["asset", "lens", "scale_kind"], sort=True)}
    bad, n_draws_seen, n_boxes, n_ident = [], 0, 0, 0
    for cell in all_cells():
        g = by.get(cell)
        real = typed_real_boxes(*cell)
        if g is None:
            if real["rows"]:
                bad.append(f"MULTISET: {cell}: no filed draw for a cell with real ranges")
            continue
        if sorted(g["draw"].unique().tolist()) != list(range(K)):
            bad.append(f"MULTISET: {cell}: draws {sorted(g['draw'].unique().tolist())[:5]}…")
        bad += multiset_findings(g, real, " ".join(cell), *cell)
        n_draws_seen += g["draw"].nunique()
        n_boxes += len(g)
        bad += repro_findings(g, *cell, real, range(K))
        n_ident += sum(1 for d in range(K)
                       if seed_is_real(real, typed_schedule(real, *cell, d)))
    for cell in NULL_ROAD_T:
        bad += road_findings(*cell)
    ib, n_cmp, lines = indep_null_all()
    bad += ib
    return (not bad), (f"{len(by)} cells x {K} draws ({n_draws_seen} draws, {n_boxes} boxes): "
                       f"every draw reproduces from the typed seed law box by box; gaps and "
                       f"(life, height) multisets == the real ranges' on every draw; a draw sits "
                       f"on the real positions only where the seed's own permutation is the "
                       f"identity ({n_ident} draws, all small-m cells; identity_perm filed alike); "
                       f"the null road fed the "
                       f"real bundle == N.events on {len(NULL_ROAD_T)} cells; the INDEPENDENT "
                       f"rebuild (own static-box law on the seed's schedule, own EMA tap scans, "
                       f"L+1 from N.nest_at with the typed partition, own terms / tolls / binding "
                       f"toll) == the filed box fates and draw n / NET on {n_cmp} rows "
                       f"({', '.join(NULL_INDEP_EVENTS_T)} x ALL + every L+1 cell x 3 directions x "
                       f"3 eras x 2 horizons) of {'; '.join(lines)}"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-L1
def indep_cells(stem, lens, kind, d, bnd, post, kms) -> tuple[str, str, str]:
    U = LADDER_T[lens]
    nv = N.nest_at(stem, [int(kms)], kind).iloc[0]
    state = nv[f"{U}_state"] or "NONE"
    inr = bool(nv[f"{U}_in_range"]) if not pd.isna(nv[f"{U}_in_range"]) else False
    top, bot, pct = float(nv[f"{U}_top"]), float(nv[f"{U}_bot"]), float(nv[f"{U}_pct"])
    atr = float(nv[f"{lens}_atr_L"])
    uk = int(nv[f"{U}_k"])
    mem = N.memory_lines(stem, U, kind)
    live = mem[(mem["born"] <= uk) & (uk < mem["end_live"])]

    def coin_of(b):
        return inr and (abs(b - top) <= COIN_T * atr or abs(b - bot) <= COIN_T * atr)

    def mcoin_of(b):
        return inr and bool((np.abs(b - live["px"].to_numpy(float)) <= COIN_T * atr).any())
    rec = typed_cell(d, state, pct, coin_of(bnd))
    memc = typed_cell(d, state, pct, coin_of(bnd) or mcoin_of(bnd))
    pc = typed_cell(d, state, pct, coin_of(post)) if np.isfinite(post) else "n/a"
    return rec, memc, pc


def l1_selection() -> pd.DataFrame:
    f = filed("R4_EVENTS")
    rng = np.random.default_rng(SEED + 1)
    pick = []
    for L in LENSES_T["CLASSIC5"]:
        g = f[(f["lens"] == L) & (f["scale_kind"] == "calibrated")
              & f["asset"].isin(CLASSIC5_T)].sort_values(["asset", "known_at", "event", "rid"],
                                                         kind="mergesort")
        aimed = []
        for r in g.iloc[::7].itertuples(index=False):   # a typed stride through the cell
            a = indep_cells(r.asset, L, "calibrated", int(r.dir), float(r.boundary),
                            float(r.boundary_post), int(r.known_close_ms))
            b = indep_cells(r.asset, L, "calibrated", int(r.dir), float(r.boundary),
                            float(r.boundary_post), int(r.known_close_ms) + STEP_T[L])
            if a[0] != b[0]:
                aimed.append(r)
            if len(aimed) == 3:
                break
        if aimed:
            pick.append(pd.DataFrame(aimed))
        pick.append(g.iloc[sorted(rng.choice(len(g), 5, replace=False))])
    return pd.concat(pick, ignore_index=True)


def l1_findings(got: pd.DataFrame) -> list[str]:
    bad = []
    for r in got.itertuples(index=False):
        rec, memc, pc = indep_cells(r.asset, r.lens, r.scale_kind, int(r.dir), float(r.boundary),
                                    float(r.boundary_post), int(r.known_close_ms))
        tag = f"{r.asset} {r.lens} {r.event} anchor {r.anchor_i}"
        if r.cell != rec:
            bad.append(f"L1-CELL: {tag}: filed {r.cell}, nest_at at known_at {rec}")
        if r.cell_mem != memc:
            bad.append(f"L1-MEM: {tag}: filed {r.cell_mem}, nest_at {memc}")
        if r.cell_post != pc:
            bad.append(f"L1-POST: {tag}: filed {r.cell_post}, nest_at {pc}")
    return bad


def l1_break():
    sel = l1_selection()
    orig = R._l1

    def late(stem, lens, kind, d, b, kms):
        return orig(stem, lens, kind, d, b, np.asarray(kms, dtype=np.int64) + STEP_T[lens])

    def one_bar_late():
        with mutated(R, "_l1", late):
            return l1_findings(_rebuilt(sel))
    return plants([("the L+1 read one bar of L late (module mutation)", "L1-CELL",
                    one_bar_late)])


def l1_real():
    sel = l1_selection()
    bad = l1_findings(sel)
    cells = sel["cell"].value_counts().to_dict()
    if len(sel) < 30:
        bad.append(f"SELECTION: {len(sel)} < 30 events")
    return (not bad), (f"{len(sel)} events (per CLASSIC5 lens: up to 3 aimed at a cell that moves "
                       f"one bar later along a typed stride + 5 seeded), record / memory-line "
                       f"twin / post-redraw cells == "
                       f"this file's recomputation from N.nest_at at the known_at close; cells "
                       f"{cells}" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-R4-CONT
def cont_findings(filed_rows: pd.DataFrame, replay: list, man: dict, grid: pd.DataFrame
                  ) -> list[str]:
    bad = []
    for era, (n, net3) in TC10_TYPED.items():
        f = filed_rows[filed_rows["era"] == era]
        if len(f) != 1 or int(f["n"].iloc[0]) != n or f"{float(f['net'].iloc[0]):+.3f}" != net3:
            bad.append(f"CONT-FILED: TC10 {era}: filed {f[['n', 'net']].to_dict('records')} vs "
                       f"typed n {n} NET {net3}")
    for era in ERAS_T:
        f = filed_rows[filed_rows["era"] == era].iloc[0]
        r = next(x for x in replay if x["era"] == era)
        for k in ("n", "n_events", "median_term", "toll_atr", "net"):
            if not same8(f[k], r[k]):
                bad.append(f"CONT-REPLAY: {era} {k}: replayed {r[k]!r}, TC10 filed {f[k]!r}")
        t = grid[(grid["asset"] == "POOLED:CLASSIC5") & (grid["lens"] == "4h")
                 & (grid["scale_kind"] == "frozen3.0") & (grid["event"] == "BRK_tap89_oneshot")
                 & (grid["cell_law"] == "record") & (grid["cell"] == "ALL")
                 & (grid["direction"] == "both") & (grid["era"] == era)
                 & (grid["horizon"] == "H20")]
        blk = man["tc10_continuity"]["tc11"][era]
        if len(t) != 1 or int(t["n"].iloc[0]) != blk["n"] or not same8(t["net"].iloc[0],
                                                                        blk["net"]):
            bad.append(f"CONT-TC11: {era}: grid {t[['n', 'net']].to_dict('records')} vs the "
                       f"manifest block {blk}")
    if not man["tc10_continuity"]["replay_equals_filed"]:
        bad.append("CONT-REPLAY: the manifest says the replay differs from the filed row")
    return bad


def cont_break():
    filed_rows = R.tc10_filed_rows()
    man, grid = manifest(), filed("R4_GRID")

    def provisional():
        pins = dict(C.RETEST_PINS, hold_bars=6)
        with mutated(C, "RETEST_PINS", pins):
            rep = R.tc10_replay()["pooled"]
        return cont_findings(filed_rows, rep, man, grid)

    def n235():
        f = filed_rows.copy()
        f.loc[f["era"] == "ALL", "n"] = 235
        return cont_findings(f, R.tc10_replay()["pooled"], man, grid)

    return plants([("the replay under the provisional retest pins (hold 6)", "CONT-REPLAY",
                    provisional),
                   ("a copy of TC10's filed row with n 235", "CONT-FILED", n235)])


def cont_real():
    filed_rows = R.tc10_filed_rows()
    rep = R.tc10_replay()["pooled"]
    man = manifest()
    bad = cont_findings(filed_rows, rep, man, filed("R4_GRID"))
    blk = man["tc10_continuity"]
    dcm = blk["decomposition"]
    return (not bad), (f"TC10 filed (read here by absolute main-tree path) ALL n "
                       f"{blk['filed']['ALL']['n']} NET {blk['filed']['ALL']['net']:+.6f}, holdout "
                       f"n {blk['filed']['holdout']['n']} NET {blk['filed']['holdout']['net']:+.6f} "
                       f"== typed; the replay run here == the file at 8 dp on n / n_events / "
                       f"median / toll / NET every era; TC11 ALL NET "
                       f"{blk['tc11']['ALL']['net']:+.6f} holdout {blk['tc11']['holdout']['net']:+.6f}"
                       f"; decomposition: extra bars {sorted(set(dcm['extra_4h_bars'].values()))}, "
                       f"only-TC11 {dcm['only_tc11']}, uncensored-now "
                       f"{dcm['in_both_censored_at_tc10_uncensored_now']}"
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-GRID
def declared(table: str) -> list[str]:
    out = []
    for p in PANELS_T:
        for a in PANELS_T[p] + (POOL_T[p],):
            for L in LENSES_T[p]:
                l1 = HAS_L1_T[(p, L)]
                for k in SCALES_T:
                    if table == "R4_BASE":
                        for law in (BASE_LAWS_T if l1 else ("record",)):
                            cells = (("ALL",) if law == "record" else ()) + (PART_T if l1 else
                                                                            ("NA",))
                            for c in cells:
                                for d in DIRS_T:
                                    for e in ERAS_T:
                                        for h in HOR_T:
                                            out.append("|".join((a, L, k, law, c, d, e, h)))
                        continue
                    for ev in EVENTS_T:
                        laws = EV_LAWS_T[ev.split("_")[0]] if l1 else ("record",)
                        if table == "R4_NULL":
                            laws = ("record",)
                        for law in laws:
                            cells = (("ALL",) if law == "record" else ()) + (PART_T if l1 else
                                                                            ("NA",))
                            for c in cells:
                                for d in DIRS_T:
                                    for e in ERAS_T:
                                        for h in HOR_T:
                                            key = ((a, L, k, ev, law, c, d, e, h) if
                                                   table == "R4_GRID" else
                                                   (a, L, k, ev, c, d, e, h))
                                            out.append("|".join(key))
    return out


def grid_whole(declared_: list, written: pd.DataFrame, cell_col: str, require_cols: tuple,
               label: str) -> tuple[bool, list[str]]:
    """TP.grid_whole's claims (exact set equality, no duplicate on either side,
    equal length, every required column present and non-null), counted with a
    Counter — TP.grid_whole's list.count is quadratic, and these grids hold 10^5
    rows.  grid_real() also runs TP.grid_whole itself on one block and requires
    the two to agree."""
    from collections import Counter
    dec = [str(c) for c in declared_]
    got = [str(c) for c in written[cell_col]]
    cd, cg = Counter(dec), Counter(got)
    miss = sorted(set(cd) - set(cg))
    extra = sorted(set(cg) - set(cd))
    dups = sorted(c for c, n in cg.items() if n > 1)
    ddec = sorted(c for c, n in cd.items() if n > 1)
    ok = not (miss or extra or dups or ddec) and len(got) == len(dec)
    lines = [f"[{'OK ' if ok else 'BAD'}] {label}: declared {len(dec)} cells, written "
             f"{len(got)}; missing {miss[:3] or 'none'}, undeclared {extra[:3] or 'none'}, "
             f"duplicated {(dups + ddec)[:3] or 'none'}"]
    for c in require_cols:
        g = c in written.columns and bool(written[c].notna().all())
        ok &= g
        lines.append(f"[{'OK ' if g else 'BAD'}] {label}: column `{c}` present and non-null on "
                     f"every row")
    return bool(ok), lines


def _keystr(df: pd.DataFrame, table: str) -> pd.Series:
    return df[KEYS_T[table]].astype(str).agg("|".join, axis=1)


STAT_T = ("median_term", "mean_term", "hit_rate", "hit_rate_net", "toll_atr", "net")


def grid_findings(G: pd.DataFrame, B: pd.DataFrame, NU: pd.DataFrame) -> list[str]:
    bad = []
    for name, df in (("R4_GRID", G), ("R4_BASE", B), ("R4_NULL", NU)):
        ok, lines = grid_whole(declared(name), df.assign(cell=_keystr(df, name)), "cell",
                                  require_cols=(("n", "n_events", "nan_reason") if name != "R4_NULL"
                                                else ("real_n", "nan_reason")) + tuple(COLLAR_T)
                                  + ("as_of_last_closed_4h",), label=name)
        if not ok:
            bad += [f"GRID-WHOLE: {x}" for x in lines if x.startswith("[BAD]")]
        cols = [c for c in df.columns if VERDICT_COL_RX.search(c)]
        if cols:
            bad.append(f"VERDICT-WORD: {name}: verdict-like column(s) {cols}")
        for c in df.columns:
            if df[c].dtype == object:
                v = df[c].dropna().astype(str)
                hit = v[v.str.contains(VERDICT_WORD_RX)]
                if len(hit):
                    bad.append(f"VERDICT-WORD: {name}.{c}: {hit.iloc[0]!r}")
        for k, v in COLLAR_T.items():
            if k not in df or not (df[k] == v).all():
                bad.append(f"COLLAR: {name}.{k} is not {v!r} on every row")
        if "m_selections_this_table" not in df or not (df["m_selections_this_table"]
                                                         == len(df)).all():
            bad.append(f"COLLAR: {name}.m_selections_this_table != len(table)")
    # a duplicated key is reported above (GRID-WHOLE); the laws below read one row per key
    G = G.drop_duplicates(subset=KEYS_T["R4_GRID"])
    B = B.drop_duplicates(subset=KEYS_T["R4_BASE"])
    NU = NU.drop_duplicates(subset=KEYS_T["R4_NULL"])
    for name, df in (("R4_GRID", G), ("R4_BASE", B)):
        n0 = df["n"] == 0
        nan_all = df[list(STAT_T)].isna().all(axis=1)
        fin_all = df[list(STAT_T)].notna().all(axis=1)
        reason = df["nan_reason"].astype(str) != ""
        badn = df[(n0 & ~(nan_all & reason)) | (~n0 & ~(fin_all & ~reason))]
        if len(badn):
            bad.append(f"NAN-LAW: {name}: {len(badn)} row(s), e.g. "
                       f"{badn.iloc[0][KEYS_T[name]].tolist()}")
        m = ~n0
        net = r8(df.loc[m, "median_term"].to_numpy(float) - df.loc[m, "toll_atr"].to_numpy(float))
        if not same8(df.loc[m, "net"], net).all():
            bad.append(f"NET-LAW: {name}: net != median_term - toll_atr on "
                       f"{int((~same8(df.loc[m, 'net'], net)).sum())} row(s)")
        kk = [c for c in KEYS_T[name] if c not in ("era",)]
        w = df.pivot_table(index=kk, columns="era", values="n_events", aggfunc="sum")
        if not (w["ALL"] == w["tuning"] + w["holdout"]).all():
            bad.append(f"PARTITION-ERA: {name}: {int((w['ALL'] != w['tuning'] + w['holdout']).sum())} "
                       f"cell(s) where ALL != tuning + holdout")
        kk = [c for c in KEYS_T[name] if c not in ("direction",)]
        w = df.pivot_table(index=kk, columns="direction", values="n_events", aggfunc="sum")
        if not (w["both"] == w["long"] + w["short"]).all():
            bad.append(f"PARTITION-DIR: {name}: both != long + short on "
                       f"{int((w['both'] != w['long'] + w['short']).sum())} cell(s)")
        kk = [c for c in KEYS_T[name] if c not in ("cell", "cell_law")]
        allr = df[(df["cell_law"] == "record") & (df["cell"] == "ALL")].set_index(kk)["n_events"]
        parts = df[df["cell"] != "ALL"].groupby(kk + ["cell_law"], sort=True)["n_events"].sum()
        pdf = parts.reset_index()
        joined = pdf.set_index(kk)["n_events"]
        diff = (joined - allr.reindex(joined.index)).abs()
        if (diff != 0).any():
            bad.append(f"PARTITION-CELL: {name}: {int((diff != 0).sum())} law(s) whose cells do "
                       f"not add to ALL")
    # base join, typed law mapping
    b = B.set_index(KEYS_T["R4_BASE"])
    fam = G["event"].str.split("_").str[0]
    has = G["cell"].isin(PART_T)
    maps = {"base_all": (np.array(["record"] * len(G), dtype=object),
                         np.array(["ALL"] * len(G), dtype=object)),
            "base_cell": (G["cell_law"].map(CELL_BASE_T).to_numpy(), G["cell"].to_numpy()),
            "base_side": (np.array([SIDE_BASE_T[(f_, lw)] if h_ else "record" for f_, lw, h_ in
                                    zip(fam, G["cell_law"], has)], dtype=object),
                          G["cell"].to_numpy())}
    for p, (law, cell) in maps.items():
        idx = pd.MultiIndex.from_arrays([G["asset"], G["lens"], G["scale_kind"], law, cell,
                                         G["direction"], G["era"], G["horizon"]])
        want = b["net"].reindex(idx).to_numpy(float)
        okj = same8(G[f"{p}_net"], want) & (G[f"{p}_law"].to_numpy() == law)
        okd = same8(G[f"net_minus_{p}"], r8(G["net"].to_numpy(float)) - r8(want))
        if not (okj & okd).all():
            i = int(np.nonzero(~(okj & okd))[0][0])
            bad.append(f"BASE-JOIN: R4_GRID.{p}: {int((~(okj & okd)).sum())} row(s) not R4_BASE's "
                       f"row under the typed law, e.g. {G.iloc[i][KEYS_T['R4_GRID']].tolist()}")
    # null: real == grid; the summary re-derived from the filed draws
    gr = G[G["cell_law"] == "record"].set_index(KEYS_T["R4_NULL"])
    nu = NU.set_index(KEYS_T["R4_NULL"])
    rn = gr["net"].reindex(nu.index).to_numpy(float)
    if not same8(nu["real_net"], rn).all():
        bad.append(f"NULL-LAW: real_net != the grid's NET on {int((~same8(nu['real_net'], rn)).sum())} "
                   f"row(s)")
    V = nu[[f"net_d{i:02d}" for i in range(K)]].to_numpy(float)
    ok = np.isfinite(V)
    nv = ok.sum(axis=1)
    rv = nu["real_net"].to_numpy(float)
    med = np.array([np.median(v[o]) if o.any() else np.nan for v, o in zip(V, ok)])
    pc = np.array([100.0 * (float((v[o] < x).sum()) + 0.5 * float((v[o] == x).sum())) / o.sum()
                   if o.any() and np.isfinite(x) else np.nan for v, o, x in zip(V, ok, rv)])
    for col, want in (("n_draws_valid_net", nv), ("null_median_net", med),
                      ("real_pctile_in_null_net", pc)):
        good = same8(nu[col], want)
        if not good.all():
            bad.append(f"NULL-LAW: {col} not re-derivable from the filed draws on "
                       f"{int((~good).sum())} row(s)")
    if not (nu["n_draws"] == K).all() or not (nu["seed"] == SEED).all():
        bad.append("NULL-LAW: n_draws / seed not the typed 20 / 20260924")
    return bad


def grid_break():
    G, B, NU = filed("R4_GRID"), filed("R4_BASE"), filed("R4_NULL")

    def g(fn):
        return lambda: grid_findings(fn(G.copy()), B, NU)

    def first(df, **kw):
        m = np.ones(len(df), bool)
        for k, v in kw.items():
            m &= (df[k] == v).to_numpy()
        return df.index[m][0]

    def nan_under_n(d):
        i = first(d, asset="POOLED:CLASSIC5", lens="4h", event="SFP_harden", cell="ALL",
                  direction="both", era="ALL", horizon="H20", scale_kind="calibrated",
                  cell_law="record")
        d.loc[i, "median_term"] = np.nan
        return d

    def era_bent(d):
        i = first(d, asset="BTCUSDT", lens="1h", event="BRK_tap89_first", cell="ALL",
                  direction="long", era="tuning", horizon="H20", scale_kind="calibrated",
                  cell_law="record")
        d.loc[i, "n_events"] = int(d.loc[i, "n_events"]) + 1
        return d

    def wrong_law(d):
        m = (d["cell_law"] == "mem_twin") & (d["cell"] == "IN_RANGE_MID")
        d.loc[m, "base_cell_net"] = d.loc[m, "base_side_net"]
        return d

    def null_moved():
        nu = NU.copy()
        nu.loc[nu.index[0], "null_median_net"] = float(nu["null_median_net"].iloc[0]) + 0.01
        return grid_findings(G, B, nu)

    return plants([
        ("a grid row dropped", "GRID-WHOLE", g(lambda d: d.drop(index=d.index[5]))),
        ("a grid row duplicated", "GRID-WHOLE", g(lambda d: pd.concat([d, d.iloc[[7]]]))),
        ("an undeclared cell (IN_RANGE_EDGE)", "GRID-WHOLE",
         g(lambda d: pd.concat([d, d.iloc[[9]].assign(cell="IN_RANGE_EDGE")]))),
        ("NaN under n > 0", "NAN-LAW", g(nan_under_n)),
        ("a verdict column", "VERDICT-WORD", g(lambda d: d.assign(verdict="PASS"))),
        ("gates altered on one row", "COLLAR",
         g(lambda d: d.assign(gates=["P-BRK-4H"] + ["nothing"] * (len(d) - 1)))),
        ("one tuning n_events bent", "PARTITION-ERA", g(era_bent)),
        ("mem-twin rows joined to the own-side base", "BASE-JOIN", g(wrong_law)),
        ("a null median moved", "NULL-LAW", null_moved),
    ])


def grid_real():
    G, B, NU = filed("R4_GRID"), filed("R4_BASE"), filed("R4_NULL")
    bad = grid_findings(G, B, NU)
    # the helper of record on one block agrees with the Counter form
    blk = G[(G["asset"] == "POOLED:CLASSIC5") & (G["lens"] == "4h")
            & (G["scale_kind"] == "calibrated")]
    dec = [c for c in declared("R4_GRID") if c.startswith("POOLED:CLASSIC5|4h|calibrated|")]
    w = blk.assign(cell=_keystr(blk, "R4_GRID"))
    a_ok, _ = TP.grid_whole(dec, w, "cell", require_cols=("n",), label="block")
    b_ok, _ = grid_whole(dec, w, "cell", ("n",), "block")
    a2, _ = TP.grid_whole(dec, w.iloc[1:], "cell", require_cols=("n",), label="block")
    b2, _ = grid_whole(dec, w.iloc[1:], "cell", ("n",), "block")
    if not (a_ok and b_ok and not a2 and not b2):
        bad.append(f"GRID-WHOLE: TP.grid_whole and the Counter form disagree on the "
                   f"POOLED:CLASSIC5 4h calibrated block ({a_ok}/{b_ok}; dropped row {a2}/{b2})")
    return (not bad), (f"R4_GRID {len(G)} / R4_BASE {len(B)} / R4_NULL {len(NU)} rows == the "
                       f"declared cells typed here ({len(declared('R4_GRID'))} / "
                       f"{len(declared('R4_BASE'))} / {len(declared('R4_NULL'))}); NaN and NET "
                       f"laws, era / direction / cell partitions, the collar, no verdict word, "
                       f"the base join under the typed law and the null summary re-derived from "
                       f"the filed draws all hold" + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-KEY
def key_findings(frames: dict, man: dict) -> list[str]:
    bad = []
    if man.get("keys") != KEYS_T:
        bad.append(f"KEY-TYPED: manifest keys {man.get('keys')} != typed")
    for name, df in frames.items():
        key = KEYS_T[name]
        miss = [c for c in key + REQUIRED_T[name] + list(COLLAR_T) + list(AS_OF_T)
                if c not in df.columns]
        if miss:
            bad.append(f"KEY-COLUMNS: {name} lacks {miss}")
            continue
        dup = int(df.duplicated(subset=key).sum())
        if dup:
            bad.append(f"KEY-UNIQUE: {name}: {dup} duplicated key row(s)")
        nul = [c for c in key + REQUIRED_T[name] + list(AS_OF_T) if df[c].isna().any()]
        if nul:
            bad.append(f"KEY-NULL: {name}: null in {nul}")
        sha = C.content_sha(df)
        if man["sha"].get(name) != sha:
            bad.append(f"KEY-SHA: {name}: manifest {str(man['sha'].get(name))[:12]}… != table "
                       f"{sha[:12]}…")
    return bad


def _frames() -> dict:
    return {k: filed(k) for k in KEYS_T}


def key_break():
    fr, man = _frames(), manifest()

    def with_(name, df):
        x = dict(fr)
        x[name] = df
        return key_findings(x, man)

    def module_key():
        k = dict(R.TABLE_KEYS)
        k["R4_EVENTS"] = [c for c in k["R4_EVENTS"] if c != "event"]
        d = fr["R4_EVENTS"][fr["R4_EVENTS"]["asset"] == "ZECUSDT"]
        with mutated(R, "TABLE_KEYS", k):
            import tempfile
            with tempfile.TemporaryDirectory(prefix="r4key_") as t:
                R._put(d, "R4_EVENTS", Path(t))
        return []

    def check_keys_dup():
        import tempfile
        with tempfile.TemporaryDirectory(prefix="r4ck_") as t:
            d = fr["R4_NULL_BOXES"].head(50)
            pd.concat([d, d.iloc[[3]]]).to_parquet(str(Path(t) / "R4_NULL_BOXES.parquet"),
                                                    index=False)
            ok, lines = TP.check_keys(Path(t), {"keys": {"R4_NULL_BOXES": KEYS_T["R4_NULL_BOXES"]}})
        return [] if ok else [f"KEY-CHECK: {x}" for x in lines if x.startswith("[BAD]")]

    return plants([
        ("a duplicated R4_GRID row", "KEY-UNIQUE",
         lambda: with_("R4_GRID", pd.concat([fr["R4_GRID"], fr["R4_GRID"].iloc[[11]]]))),
        ("a nulled R4_EVENTS key cell", "KEY-NULL",
         lambda: with_("R4_EVENTS", fr["R4_EVENTS"].assign(
             rid=pd.array([None] + fr["R4_EVENTS"]["rid"].tolist()[1:], dtype="Int64")))),
        ("as_of_last_closed_4h dropped from R4_BASE", "KEY-COLUMNS",
         lambda: with_("R4_BASE", fr["R4_BASE"].drop(columns=["as_of_last_closed_4h"]))),
        ("a manifest sha altered", "KEY-SHA",
         lambda: key_findings(fr, dict(man, sha=dict(man["sha"], R4_NULL="0" * 64)))),
        ("the module's R4_EVENTS key without `event` (C.canon must HALT)", "F-KEY", module_key),
        ("TP.check_keys on a temp root holding a duplicated row", "KEY-CHECK", check_keys_dup),
    ])


def key_real():
    fr, man = _frames(), manifest()
    bad = key_findings(fr, man)
    ok, lines = TP.check_keys(OUT, man)
    if not ok:
        bad += [f"KEY-CHECK: {x}" for x in lines if x.startswith("[BAD]")]
    return (not bad), (f"{len(fr)} tables, typed keys unique, no null in keys / required / the "
                       f"nine as-of columns, manifest content shas == the tables'; TP.check_keys: "
                       + " · ".join(x.split('] ', 1)[1][:60] for x in lines)
                       + (f"; findings {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════ F-DET
def _files(d: Path) -> dict:
    return {p.name: p.read_bytes() for p in sorted(d.iterdir()) if p.is_file()}


def _content_sha_bytes(blob: bytes) -> str:
    """A parquet's content sha from its bytes, read through pandas on a PATH STRING
    [AM-2] (the bytes are put in a temp file first)."""
    import tempfile
    with tempfile.TemporaryDirectory(prefix="r4det_") as t:
        q = Path(t) / "x.parquet"
        q.write_bytes(blob)
        return C.content_sha(pd.read_parquet(str(q)))


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"seed-run {lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical stage_r4/", canon)):
        if sorted(x) != sorted(FILES_T):
            out.append(f"{lab}: file set {sorted(x)} != typed {sorted(FILES_T)}")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                k = next((i for i in range(min(len(x[name]), len(y[name])))
                          if x[name][i] != y[name][i]), min(len(x[name]), len(y[name])))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca, cb = _content_sha_bytes(x[name]), _content_sha_bytes(y[name])
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    return RUN_ROOT / DET_DIRNAME


def det_builds(seeds=DET_SEEDS) -> dict:
    """Each seed's build = the 14 units in FRESH interpreters (the fixture harness
    starts them, AM-2), then the merge — PYTHONHASHSEED = the seed throughout.
    Units of both seeds share one queue of DET_PROCS slots."""
    jobs, res = [], {}
    for s in seeds:
        d = det_dir() / f"seed_{s}"
        if d.exists():
            shutil.rmtree(d)
        d.mkdir(parents=True)
        jobs += [(s, d, u) for u in R.UNITS]
    run, q, rc = [], list(jobs), {s: 0 for s in seeds}
    while q or run:
        while q and len(run) < DET_PROCS:
            s, d, u = q.pop(0)
            env = dict(_env(), PYTHONHASHSEED=str(s))
            run.append((s, subprocess.Popen(
                [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_r4.py"), f"--unit={u}",
                 f"--parts={d / '_det_parts'}"], env=env, cwd=str(ROOT),
                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)))
        time.sleep(0.5)
        still = []
        for s, p in run:
            if p.poll() is None:
                still.append((s, p))
            elif p.returncode != 0:
                rc[s] = p.returncode
        run = still
    for s in seeds:
        d = det_dir() / f"seed_{s}"
        if rc[s] == 0:
            r = subprocess.run([PY, "-B", str(ROOT / "scripts" / "tierc11_stage_r4.py"), "--merge",
                                f"--parts={d / '_det_parts'}", f"--out-dir={d}"],
                               env=dict(_env(), PYTHONHASHSEED=str(s)), cwd=str(ROOT),
                               capture_output=True, text=True, timeout=3600)
            rc[s] = r.returncode
        res[s] = (rc[s], _files(d))
    return res


def _canon() -> dict:
    return {k: v for k, v in _files(OUT).items() if k in FILES_T}


def det_break():
    canon = _canon()
    bent = dict(canon)
    md = bytearray(bent["STAGE_R4.md"])
    md[len(md) // 2] ^= 0x01
    bent["STAGE_R4.md"] = bytes(md)

    def float_moved():
        import tempfile
        d = pd.read_parquet(str(OUT / "R4_GRID.parquet"))
        i = d.index[d["n"] > 0][0]
        d.loc[i, "net"] = float(d.loc[i, "net"]) + 1e-6
        with tempfile.TemporaryDirectory(prefix="r4det_") as t:
            q = Path(t) / "R4_GRID.parquet"
            d.to_parquet(str(q), index=False)
            c2 = dict(canon)
            c2["R4_GRID.parquet"] = q.read_bytes()
        return det_findings((0, c2), (0, c2), canon)

    def hashorder():
        outs = {}
        for s in DET_SEEDS:
            code = (f"import sys\nsys.dont_write_bytecode = True\n"
                    f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                    f"import tierc11_stage_r4 as R\n"
                    f"print(R.lean_block() + 'set order: ' + ','.join(set(R.PANELS['UNSEEN12'])))\n")
            r = subprocess.run([PY, "-B", "-c", code], env=dict(_env(), PYTHONHASHSEED=str(s)),
                               cwd=str(ROOT), capture_output=True, text=True, timeout=600)
            outs[s] = (r.returncode, {"STAGE_R4.md": r.stdout.encode()})
        a, b = outs[DET_SEEDS[0]], outs[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_R4.md", "STAGE_R4.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("one NET moved 1e-6 in a copy of R4_GRID.parquet", "R4_GRID.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: STAGE_R4.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = det_builds()
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    man = json.loads(canon["build_manifest.json"]) if "build_manifest.json" in canon else {}
    shas = ", ".join(f"{k} {sha_bytes(v)[:12]}…" for k, v in sorted(a[1].items()))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == typed {len(FILES_T)} files in both builds "
                       f"and in stage_r4/; every file byte-identical seed 1 == seed {SEED} == "
                       f"canonical, every parquet content sha equal: {not bad} ({shas}); content "
                       f"shas R4_GRID {man.get('sha', {}).get('R4_GRID', '?')[:16]}… R4_NULL "
                       f"{man.get('sha', {}).get('R4_NULL', '?')[:16]}…"
                       + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-R4-EVENTS", "the grid's events are N's events at the same (asset, lens, scale), anchored "
     "at N's known_at [L-R.6(a)(b)]",
     "on any of the 112 cells the filed events differ from N.events' frames in key set, known_at, "
     "death bar or boundary, or break the typed anchor (tap +3, memory line +6, harden +0), "
     "direction, close-stamp or era laws",
     ev_break, ev_real),
    ("F-R4-SCAN", "every evaluated touch is a row (R4_SCAN) and every death its scan's end "
     "(R4_DEATHS) [L-R.6(a)]",
     "on any of the 112 cells R4_SCAN is not N's first-retest scan rows, a (death, band) "
     "sequence breaks the typed scan law, a hold row is not a first-hold event, or R4_DEATHS "
     "is not N's deaths with each band's touch count / end / hold touch as R4_SCAN gives them",
     scan_break, scan_real),
    ("F-R4-OUTCOME", ">= 30 events hand-computed from raw bars: H20 / H100 term, censoring, "
     "MFE / MAE, toll [L-R.6 outcomes]",
     "a selected event's known_at, censor flag, term, MFE / MAE or toll differs from this file's "
     "raw-bar computation at 8 dp, or the typed selection holds no censored case",
     outcome_break, outcome_real),
    ("F-R4-BASE", "one full base cell per lens by a plain loop over every bar [L-R.6 base rate, "
     "AM-6 R-BASE-COIN]",
     "a typed base cell recomputed by a plain loop (N.nest_at cells, raw-bar terms) differs from "
     "R4_BASE in n_events / n / n_censored / median / mean / hit rates / toll / NET",
     base_break, base_real),
    ("F-R4-GRIDSTAT", "every grid row's statistics re-derived from the filed events, per asset "
     "and pooled (the binding toll), and a pooled base row per lens [L-R.6 statistics, R4-4, "
     "R4-5]",
     "any R4_GRID row differs from this file's statistics on the filed R4_EVENTS (typed law / "
     "direction / era maps; n's, median, q25 / q75, hit rates, MFE / MAE, toll, toll_atr_all, "
     "NET, binding count at 8 dp; the mean under the tie law), or a typed pooled R4_BASE row "
     "differs from its members' plain loops over every bar with the binding toll",
     gridstat_break, gridstat_real),
    ("F-NULL", "the gaps+order null of record rebuilt for TC11: seeded draws, multisets kept, "
     "N's scan on the null [L-R.6 null, ruling R10]",
     "a filed draw does not reproduce from the typed seed law, a draw breaks the gap or (life, "
     "height) multiset or IS the real schedule, the null road fed the real bundle is not "
     "N.events, or the filed box fates / draw n / NET differ from this file's independent "
     "rebuild (own static-box law, own tap scans, N.nest_at L+1 with the typed partition, own "
     "arithmetic) on 3 cells x 2 draws and one pooled draw",
     null_break, null_real),
    ("F-R4-L1", "the L+1 cell of >= 30 events recomputed from N.nest_at at the known_at close "
     "[L-R.6 L+1 conditioning]",
     "a selected event's filed record / memory-line / post-redraw cell differs from this file's "
     "recomputation from N.nest_at at its known_at close",
     l1_break, l1_real),
    ("F-R4-CONT", "TC10 continuity at frozen3.0 · one-shot · 4h · POOLED:CLASSIC5 · tap89 · H20 "
     "[AM-1]",
     "TC10's filed row is not the typed n / NET, the replay differs from it at 8 dp, the manifest "
     "says so, or TC11's grid row is not the manifest block's",
     cont_break, cont_real),
    ("F-GRID", "every R4 grid WHOLE: declared cells typed here, NaN / NET / partition laws, the "
     "collar, no verdict word, the base join, the null summary",
     "R4_GRID / R4_BASE / R4_NULL do not hold exactly the typed declared cells, or break the NaN, "
     "NET, era / direction / cell partition, collar, verdict-word, base-join or null-summary laws",
     grid_break, grid_real),
    ("F-KEY", "typed unique keys, no null in required columns, the as-of warranty, manifest shas",
     "a key is not the typed one or not unique, a required / as-of column is null or absent, "
     "TP.check_keys is RED, or a manifest content sha is not the table's",
     key_break, key_real),
    ("F-DET", "two builds under different hash seeds (units in fresh interpreters, then the "
     "merge), one set of bytes [L-F.1 variant (i)]",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_r4) differ from each other or "
     "from the files of record in the file set, any byte or any parquet content sha, or either "
     "exits nonzero",
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
    say("TIER-C11 STAGE R-b · R4 FIXTURES — scripts/tierc11_stage_r4.py (the two trades per "
        "lens, Tier-E, whole; L-R.6, AM-1, AM-4, AM-6) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} (sensitivity {SEED_SENS}) · K {K} · substrate {TC11_SNAP.name} · pin {PIN} "
        f"· TC10 pin {TC10_PIN}")
    for ln in R.lean_block().rstrip("\n").splitlines():
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
