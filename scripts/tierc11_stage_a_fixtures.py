#!/usr/bin/env python
"""TIER-C11 · STAGE A — F-ADD · F-ADD-BOOK · F-IDENTITY · F-ADD-INSTANTS · F-GRID · F-KEY ·
F-DET.
The fixtures of scripts/tierc11_stage_a.py (the P-ADD-BRK / P-ADD-SFP books)
[LEANS L-A.1, L-A.2, L-A.3, L-W.0, L-W.3, L-1.5; AM-3, AM-5, AM-6, AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen.  A break leg is a
set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is a MUTATION of the stage module
(or of the ride's add hook as the stage calls it), restored in `finally`, or a
CORRUPTED COPY of a written table; no artifact of record moves.  The referees
are TYPED HERE (a second object): the machine's death / harden law (8 closes or
1.5 ATR beyond; a close back inside within 7 bars), the add law (<= 2, 0.5 unit,
post-+1R, in-trade, the 1h close), the 1h picks of record, the charter tiers,
the column commission, the declared grids, the collar.  The data referees are
THIS FILE'S OWN: its own parquet read of the TC11 snapshot (1h / 4h bars,
funding), its own Wilder ATR loop, its own walk law, its own +1R latch and
1h-resolved exit, its own hand booking — and the RANGE MACHINE ITSELF, run on
PREFIX tapes (C.run_scale(tape.head(m))) as the as-of referee, never the
stage's event table.

  F-ADD        FAILS IF, on ANY admitted add of ANY ridden arm of either rule
               (every add, not a sample): the machine run on the 1h prefix
               ending at the add's event bar k has no death (P-ADD-BRK) / harden
               (P-ADD-SFP) at k on the trade's side (ADD-ASOF / ADD-SIDE); this
               file's plain-loop re-walk of the as-of box (the machine's as-of
               view, cross-checked against the prefix run's live range) does not
               first meet the death law (8 closes or 1.5 ATR beyond) / the harden
               law (a close back inside within 7 bars) at k (ADD-REWALK /
               ADD-BOX); the event is not on the written 1h event tape
               (ADD-TAPE); the add is not in-trade against this file's own
               1h-resolved exit (ADD-INTRADE), not at/after its own +1R latch
               (ADD-LATCH), a 3rd add (ADD-CAP), not 0.5 (ADD-SIZE), not priced
               at its own 1h close (the parent's close on a mismatch bar)
               (ADD-PX / ADD-MOVED), not in the 4h bar containing it (ADD-BAR),
               or flagged wrongly (ADD-FLAG); or any campaign's admitted set
               differs from this file's re-derivation from the machine's full
               run (ADD-SET); or any candidate event's written disposition
               differs, row by row, from this file's TYPED disposition
               re-derived from the machine's full run (order: pre-entry, not
               before the own 1h-resolved exit, before the own latch, the twin,
               then the cap, AM-6 s4) (ADD-DISP), or DISPOSITION_COUNTS from
               the own tally (ADD-DISP-COUNT); or an ADDS / EVENTS_1H / regbook
               row's scale_in_sample, pick_window or stability_changed breaks
               the TYPED label law (calibrated & read <= the era cut; 'tuning';
               BTC/SOL/NEAR changed; frozen 3.0 never in-sample, 'NA')
               (ADD-LABEL-ROW / -ADDS / -EVENTS / -REGBOOK); or a slice's
               ADDS rows are not the scored adds of its era (ADD-SLICE).
               SABOTAGE (stage mutations): events handed to the ride one 1h bar
               BEFORE they are known (look-ahead), per rule; the +1R latch
               gate removed from the add hook, per rule; a 3rd add (max_adds 3 on P-ADD-BRK; a planted 3rd row on
               P-ADD-SFP, whose cap never binds); the events of the WRONG side;
               adds after the 1h-resolved exit; the refused dispositions
               dropped by the add hook; the SCALE-IN-SAMPLE flags zeroed on
               the range facts the stage reads.  (copies): one add price bent;
               a disposition relabelled; n_adds_scale_in_sample zeroed; a
               stability label flipped; a slice row dropped.
  F-ADD-BOOK   FAILS IF, on ANY campaign of ANY arm (the base, the ridden arms,
               the slices, the head-to-head), the
               written gross / fee / funding (uncapped and capped) / net / add_r
               differ by more than 1e-9 (representation) from this file's hand
               booking (own bars, own funding, 5 bps a side, the harvest half at
               its fill, each add 0.5 from its 1h close to the exit, funding from
               the next 4h open, the D12 ceiling 1.0 ONCE on the total); Δ −
               add_r != absorbed(book) − absorbed(v6) (AM-3); the printed
               v6_net_r / delta_net_r != the referee's v6 net_r / net_r − it,
               EXACTLY (BOOK-DELTA); an ACTED row is not a regbook acted
               campaign or its Δ / add_r / absorbed / residual do not
               re-derive (BOOK-ACTED); or haircut_net_r != net_r − fee_r ×
               tier / 5.0 with the stem's charter tier (AM-7).  Every arm (the
               base, the ridden arms, the slices, the head-to-head).
               SABOTAGE: tranche size 1.0 (stage mutation); delta_net_r written
               as add_r, AM-3's forbidden reading (stage mutation); a corrupted
               charter tier (BTC 10 bps) handed to the stage; add_r bent in a
               copy; the uncapped funding bent on a ceiling-bound row of a
               copy; the ACTED Δ written as add_r in a copy.
  F-IDENTITY   FAILS IF, in ANY written regbook, a campaign without an add
               differs from this file's v6 referee (TP.run_cell_n, full
               precision) on net_r, gross_r, fee_r, funding_r, entry_px, stop_px,
               r_dist, exit_ms, exit_px or exit_reason by ANY amount (0.000e+00),
               an acted campaign moves the v6 leg, the key set is not v6's (or,
               for a slice, v6's keys of that era), a row's exit_close_ms is not
               the v6 exit bar's close or its exit_close_1h_ms not this file's own
               1h-resolved exit, or a base arm differs from books/v6_campaigns
               .parquet (typed sha) on its 13 regbook columns at 6 dp (the
               scorer's F-BASE-IDENT law); or a head-to-head arm is not its
               registration's scored rows, or its opponent_net_r / delta is not
               the other registration's scored net_r / net_r − it exactly on
               identical keys (H2H).  SABOTAGE (copies): net_r +1e-12 on an
               untouched row; an exit_reason relabelled; an acted row's exit_px
               moved; a row dropped; the base 1h exit instant moved 1h; the base
               exit_close_ms written as a 1h instant; a scored exit_close_ms moved
               a bar; the head-to-head opponent_net_r bent 1e-12; the
               head-to-head arm built from the frozen-3.0 twin's rows.
  F-ADD-INSTANTS FAILS IF, on ANY row of ANY written regbook of either rule (the base, the
               ridden arms, the slices, the head-to-head), the extra columns
               add1_close_ms / add2_close_ms [SA-12; L-R.5, AM-6 — the lanes pass]
               are absent or not Int64, or differ from THIS FILE'S re-derivation from
               the machine's FULL 1h run (expected_adds: the rule's events on the
               trade's side, each at its 1h close — the parent's close on an own
               L-W.0 mismatch bar — in-trade against the own 1h-resolved exit, at/after
               the own +1R latch, the arm's twin, then the first 2): add k's instant or
               NA when fewer than k adds; or the count of stamped instants != n_adds;
               or add1 >= add2; or an instant lies outside (entry close, own
               1h-resolved exit); or a base row carries an add instant.  SABOTAGE:
               (copies) add1 moved one 1h bar late; add2 dropped (nulled on a 2-add
               row); [mutant] the writer's add_instants_of stamping each add at the
               CLOSE of its 4h bar (the parent's close, not the 1h event).
  F-GRID       FAILS IF a grid is not WHOLE against the cells declared here
               (TP.grid_whole: DISPOSITION_COUNTS 2x4x7, HEAD_TO_HEAD 6x2,
               TIER_E_ARMS 2x6, REGISTERED_BOOKS 2x2, OVERLAP 6, PICK_STABILITY_1H
               5, MISMATCH_BOOKS 2x5), a count does not re-derive from the row
               tables, a printed Δ sum / mean, base sum or ruled-base sum
               (HEAD_TO_HEAD, REGISTERED_BOOKS, TIER_E_ARMS) does not re-derive
               from the regbooks' net_r and the referee's v6 net_r (or the
               head-to-head base_arm book's net_r) (GRID-DELTA), OVERLAP does
               not re-derive from the regbooks, a pick is not the typed 1h pick,
               the corridor mismatch bars are not the typed per-asset counts,
               or the head-to-head lacks 'neither promoted by the other's
               failure'.  SABOTAGE: delta_net_r written as add_r (stage
               mutation); (copies) the head-to-head ΣΔ sign-flipped; a slice's
               base sum printed as the full base's; a zero cell dropped; an
               undeclared cell; a duplicated cell; a count +1; the note
               removed.
  F-KEY        FAILS IF any written regbook lacks a required column or has
               another dtype than the typed one, a null in a required column, a
               repeated (symbol, entry_ms), an era not by the entry CLOSE,
               entry_close_ms != entry_ms + 4h, a direction outside +/-1, a
               sidecar whose n / sum_net_r / book_sha256 (this file's canonical
               CSV) / kind / ruler / era_scope / panel / collar disagree; a
               STATUS.json not BUILT or not listing the typed arms; a base_arm
               on any arm but the head-to-head or not the typed opponent's
               scored arm (KEY-BASEARM); a head-to-head key set != its
               base_arm's (KEY-PAIRED); any stage table with a repeated key, a
               null key cell, a missing as-of stamp, a missing collar (every
               table but REGISTERED_BOOKS), a verdict column or a verdict word;
               or a manifest content sha that is not the file's.  SABOTAGE
               (copies): the head-to-head base_arm dropped; a head-to-head row
               dropped; a duplicated row; a null net_r; direction as int64; the
               haircut column dropped; one era flipped; a bent book_sha256; the
               collar dropped; a verdict column added; the sidecar n off by one.
  F-DET        FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) under
               RUN_ROOT/_det_stage_a differ from each other or from the
               canonical files of record in the file set, any byte or any parquet
               content sha, or either exits nonzero.  SABOTAGE: one byte bent in
               a copy; a parquet copy with one float moved; a hash-order-dependent
               line emitted under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE (tierc11_env's guard).  Seed 20260924.  The
transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_a.py            # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_a_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_stage_a as SA                                         # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

N, RD, B, E = SA.N, SA.RD, SA.B, SA.E
TP, T9, T7, TB = E.TP, E.T9, E.T7, E.TB
C, RCP = N.C, N.RC                       # the machine (the census's port) — the as-of referee
CARD, ROLES = TP.CONTROL_CARD, T9.V6_ROLES

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never SA's own ──
SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1_790_294_400_000                  # 2026-09-25T00:00:00Z [L-0.1]
SEED = 20260924
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
H1, H4 = 3_600_000, 14_400_000
ERA_CUT_T = 1_719_791_999_000            # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
TOL = 1e-9                               # a REPRESENTATION tolerance
ADDS_MAX_T, ADD_SIZE_T = 2, 0.5          # L-A.1 "at most 2 adds, each a 0.5-unit tranche"
BRK_N_T, BRK_M_T, DEV_RET_T, ATR_LEN_T = 8, 1.5, 7, 14   # the machine's death / harden law
CEILING_T = 1.0                          # D12
BPS_T = 5.0 / 10_000.0                   # taker 5 bps per side [L-1.1]
HARVEST_Q_T = 0.5
TAKER_SIDE_T = 5.0                       # AM-7's divisor
TIER_BPS_T = {"A": 2.0, "B": 5.0, "C": 10.0}
PICK_1H_T = {"BTCUSDT": 1.75, "ETHUSDT": 2.0, "SOLUSDT": 1.75, "NEARUSDT": 1.75,
             "ZECUSDT": 2.0}             # SCALE_PICKS.json (filed at TC11-NEST, before Stage A)
FROZEN_T = 3.0
CLASSIC5_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
REGS_T = ("P-ADD-BRK", "P-ADD-SFP")
KIND_T = {"P-ADD-BRK": "breakout-die", "P-ADD-SFP": "harden"}
SIDE_FOR_T = {("P-ADD-BRK", 1): "top", ("P-ADD-BRK", -1): "bottom",      # L-A.2
              ("P-ADD-SFP", 1): "bottom", ("P-ADD-SFP", -1): "top"}      # L-A.3 spring/upthrust
RIDDEN_T = ("scored", "tierE__frozen3", "tierE__refuse_below_entry", "tierE__refuse_post_harvest")
SCALE_ARM_T = {"scored": "calibrated", "tierE__frozen3": "frozen3.0",
               "tierE__refuse_below_entry": "calibrated", "tierE__refuse_post_harvest": "calibrated"}
TWIN_T = {"scored": None, "tierE__frozen3": None, "tierE__refuse_below_entry": "below",
          "tierE__refuse_post_harvest": "post"}
SLICES_T = {"tierE__tuning": "tuning", "tierE__holdout": "holdout"}
# the head-to-head Tier-E arm of each registration ("head-to-head vs P-ADD-SFP / BRK",
# REGISTRATIONS.json tier_e_arms), ruled against the OTHER registration's scored arm
H2H_T = {"P-ADD-BRK": "tierE__head_to_head_vs_p_add_sfp",
         "P-ADD-SFP": "tierE__head_to_head_vs_p_add_brk"}
H2H_BASE_T = {"P-ADD-BRK": "P-ADD-SFP/scored", "P-ADD-SFP": "P-ADD-BRK/scored"}
ARMS_OF_T = {r: ("scored", "base", H2H_T[r], "tierE__frozen3", "tierE__refuse_below_entry",
                 "tierE__refuse_post_harvest", "tierE__tuning", "tierE__holdout")
             for r in REGS_T}
# the honesty labels of the 1h scale [L-R.2; SCALE_PICKS.json filed at TC11-NEST]:
# calibrated = the tuning-window pick, in-sample at a read instant <= the era cut;
# stability changed (first-half-of-tuning pick != tuning pick) for BTC, SOL, NEAR;
# frozen 3.0 is never in-sample and has no stability label
PICK_WINDOW_T = {"calibrated": "tuning", "frozen3.0": "frozen3.0"}
STAB_T = {"BTCUSDT": "True", "ETHUSDT": "False", "SOLUSDT": "True", "NEARUSDT": "True",
          "ZECUSDT": "False"}
DISP_T = ("admitted", "refused: pre-entry", "refused: not before the 1h-resolved exit",
          "refused: before the +1R latch", "refused: below entry (twin)",
          "refused: post-harvest (twin)", "refused: cap 2 reached")
REQUIRED_T = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
              "direction": "int8", "entry_px": "float64", "stop_px": "float64",
              "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
              "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
              "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
              "lane": "object"}
SIDECAR_KEYS_T = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                  "sum_net_r", "book_sha256", "description", "source_script")
COLLAR_T = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
            "gates": "nothing"}
AS_OF_T = ("as_of_last_closed_4h", "as_of_panel_start", "as_of_span_days", "warranty",
           "as_of_lens", "as_of_last_closed_bar", "as_of_panel", "as_of_n_assets",
           "as_of_substrate")
VERDICT_COLS_T = ("verdict", "verdict_of_record", "clears_bh_bar", "promotable",
                  "scored_in_family", "p_one_sided", "is_the_registered_cell")
VERDICT_WORDS_T = ("SUPPORTED",)
NEITHER_T = "neither promoted by the other's failure"
BOOK_LABEL_T = "book, not a verdict"
TABLES_T = {"ADDS": ["registration", "arm", "symbol", "entry_ms", "seq"],
            "DISPOSITIONS": ["registration", "arm", "symbol", "entry_ms", "event_ms", "event_rid"],
            "ACTED": ["registration", "arm", "symbol", "entry_ms"],
            "DISPOSITION_COUNTS": ["registration", "arm", "disposition"],
            "HEAD_TO_HEAD": ["arm", "registration"], "OVERLAP": ["arm"],
            "TIER_E_ARMS": ["registration", "arm"], "REGISTERED_BOOKS": ["registration", "arm"],
            "EVENTS_1H": ["asset", "scale_kind", "event_kind", "event_i"],
            "PICK_STABILITY_1H": ["asset"], "MISMATCH_BOOKS": ["registration", "arm"],
            "MISMATCH_BARS": ["asset", "bar_open_ms"]}
UNCOLLARED_T = ("REGISTERED_BOOKS",)
STAGE_FILES_T = tuple(sorted([f"{t}.parquet" for t in TABLES_T] + ["STAGE_A.md",
                                                                    "STAGE_A_MANIFEST.json"]))
REG_FILES_OF_T = {r: tuple(sorted([f"{a}.{x}" for a in ARMS_OF_T[r] for x in ("parquet", "json")]
                                  + ["STATUS.json"])) for r in REGS_T}
MISMATCH_N_T = {"BTCUSDT": 5, "ETHUSDT": 4, "SOLUSDT": 3, "NEARUSDT": 2, "ZECUSDT": 2}
V6_CAMPAIGNS_SHA_T = "aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5"  # PROGRESS TC11-BOOKS
V6_CMP_T = (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
            ("entry_px", "entry_px"), ("stop_px", "stop_px"), ("r_dist", "r_dist"),
            ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
            ("net_r", "net_r"), ("gross_r", "gross_r"), ("fee_r", "fee_r"),
            ("funding_r", "funding_r"), ("era", "era_of_entry"), ("lane", "lane"))
MISMATCH_SHARED_T = ("2023-11-10T12:00:00Z", "2024-10-28T20:00:00Z")   # AM-5

OUT = SA.OUT
REGBOOKS = SA.REGBOOKS
DET_ROOT = SA.DET_ROOT
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_A.txt"
PY = sys.executable
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []
_TMP_RX = re.compile(r"(/private)?/(var/folders|tmp)/[^\s'\"]+")

if (RCP.PINS["BREAK_CONFIRM_N"], RCP.PINS["BREAK_MARGIN"], RCP.PINS["DEV_RETURN_BARS"],
        RCP.ATR_LEN) != (BRK_N_T, BRK_M_T, DEV_RET_T, ATR_LEN_T):
    raise SystemExit("HALT: the machine's death / harden pins are not the ones this file types")
if CARD.funding_ceiling_r != CEILING_T or CARD.harvest_frac != HARVEST_Q_T:
    raise SystemExit("HALT: the v6 card's ceiling / harvest fraction are not the typed ones")


def say(line: str = "") -> None:            # deterministic -> transcript
    line = _TMP_RX.sub("<tmp>", line)
    print(line)
    LINES.append(line)


def clock(line: str) -> None:               # wall clock, temp paths -> stdout ONLY
    print(f"  [clock · stdout only] {line}")


def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def iso(ms) -> str:
    return T9.iso(int(ms))


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
    if isinstance(r_why, list):
        for ln in r_why[:-1]:
            say(f"    {ln}")
        r_why = r_why[-1]
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
            caught.append(f"{name} -> [{len(found)} finding(s)] {shown}")
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
    return dict(os.environ, NAIAD_CACHE_DIR=str(SNAP), PYTHONDONTWRITEBYTECODE="1")


def same(a, b) -> bool:
    return abs(float(a) - float(b)) <= TOL * max(1.0, abs(float(a)), abs(float(b)))


# ═══════════════════════════════════════ THIS FILE'S OWN READ OF THE SNAPSHOT
_C: dict = {}


def own_bars(sym: str, lens: str) -> pd.DataFrame:
    k = ("own", sym, lens)
    if k not in _C:
        step = {"1h": H1, "4h": H4}[lens]
        d = pd.read_parquet(str(SNAP / "klines" / f"{sym}_{lens}.parquet"))
        d = d.sort_values("open_time", kind="mergesort")
        d = d[d["open_time"] + step <= PIN].reset_index(drop=True)
        _C[k] = d
    return _C[k]


def own_atr(h, l, c, n: int) -> np.ndarray:
    """Wilder's ATR as a plain loop (TR[0] = h - l; RMA seeded at TR[0])."""
    out = np.empty(len(c))
    prev = None
    a = 1.0 / n
    for i in range(len(c)):
        tr = float(h[i] - l[i]) if i == 0 else max(float(h[i] - l[i]), abs(float(h[i] - c[i - 1])),
                                                    abs(float(l[i] - c[i - 1])))
        prev = tr if prev is None else prev + a * (tr - prev)
        out[i] = prev
    return out


def own1(sym: str) -> dict:
    k = ("own1", sym)
    if k not in _C:
        b = own_bars(sym, "1h")
        t = b["open_time"].to_numpy(np.int64)
        h, l, c = (b[x].to_numpy(float) for x in ("high", "low", "close"))
        _C[k] = {"t": t, "h": h, "l": l, "c": c, "atr": own_atr(h, l, c, ATR_LEN_T),
                 "idx": {int(x): i for i, x in enumerate(t)}}
    return _C[k]


def own4(sym: str) -> dict:
    k = ("own4", sym)
    if k not in _C:
        b = own_bars(sym, "4h")
        _C[k] = {"t": b["open_time"].to_numpy(np.int64),
                 **{x: b[y].to_numpy(float) for x, y in (("h", "high"), ("l", "low"),
                                                          ("c", "close"))}}
    return _C[k]


def own_fund(sym: str) -> dict:
    k = ("fund", sym)
    if k not in _C:
        d = pd.read_parquet(str(SNAP / "funding" / f"{sym}.parquet"))
        out: dict = {}
        for ft, fr in zip(d["funding_time"].astype(np.int64), d["funding_rate"].astype(float)):
            hh = int(ft) // H1 * H1
            out[hh] = out.get(hh, 0.0) + fr
        _C[k] = out
    return _C[k]


def bar4(sym: str, close_ms: int) -> int:
    """The index of the own 4h bar CONTAINING a 1h close (open < close <= open + 4h)."""
    return int(np.searchsorted(own4(sym)["t"], int(close_ms), "left")) - 1


def own_kids(sym: str, j: int):
    """THIS file's walk law: 4 native 1h rows on the grid inside bar j reproducing
    its high, low and close (1e-9 relative); else None (a mismatch bar)."""
    k = ("kids", sym, int(j))
    if k not in _C:
        X, Hh = own4(sym), own1(sym)
        o4 = int(X["t"][j])
        ks = [Hh["idx"].get(o4 + q * H1) for q in range(4)]
        n_in = int(np.searchsorted(Hh["t"], o4 + H4, "left") - np.searchsorted(Hh["t"], o4, "left"))
        ok = all(x is not None for x in ks) and n_in == 4
        if ok:
            ok = (same(max(Hh["h"][x] for x in ks), X["h"][j])
                  and same(min(Hh["l"][x] for x in ks), X["l"][j])
                  and same(Hh["c"][ks[3]], X["c"][j]))
        _C[k] = ks if ok else None
    return _C[k]


def own_latch(t):
    """THIS file's +1R latch [L-W.3 / L-W.5]: the first 1h child after the entry
    close whose favourable extreme reaches entry +/- R, a child that touches the
    initial stop first ending the campaign un-latched; on a mismatch bar the
    PARENT decides (latch at the top of the bar, at its close).  Before the latch
    the stop is the initial stop (the trail arms only at +1R)."""
    X, Hh = own4(t.symbol), own1(t.symbol)
    d, e, R, s0 = int(t.direction), float(t.entry_px), float(t.r_dist), float(t.stop_px)
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        kids = own_kids(t.symbol, j)
        if kids is not None:
            for x in kids:
                fav = Hh["h"][x] if d == 1 else Hh["l"][x]
                adv = Hh["l"][x] if d == 1 else Hh["h"][x]
                if (d == 1 and adv <= s0) or (d == -1 and adv >= s0):
                    return None
                if (fav - e) * d / R >= 1.0:
                    return int(Hh["t"][x]) + H1
        else:
            fav = X["h"][j] if d == 1 else X["l"][j]
            adv = X["l"][j] if d == 1 else X["h"][j]
            if (fav - e) * d / R >= 1.0:
                return int(X["t"][j]) + H4
            if (d == 1 and adv <= s0) or (d == -1 and adv >= s0):
                return None
    return None


def own_exit(t) -> int:
    """THIS file's 1h-resolved exit instant [L-W.3]: a stop at the close of the
    first 1h child of the exit bar touching the exit (stop) price; a bell /
    corridor_end at the 4h close; a stop on a mismatch bar at the parent's close."""
    X, Hh = own4(t.symbol), own1(t.symbol)
    j, d = int(t.exit_i), int(t.direction)
    if t.exit_reason == "stop":
        kids = own_kids(t.symbol, j)
        if kids is not None:
            for x in kids:
                if (d == 1 and Hh["l"][x] <= float(t.exit_px)) or \
                        (d == -1 and Hh["h"][x] >= float(t.exit_px)):
                    return int(Hh["t"][x]) + H1
            raise RuntimeError(f"{t.symbol} {iso(t.entry_ms)}: no own child touches the stop")
    return int(X["t"][j]) + H4


def own_tiers() -> dict:
    k = ("tiers",)
    if k not in _C:
        raw = json.loads((E.OUT / "data" / "fee_schedule.json").read_text(encoding="utf-8"))
        _C[k] = {a["stem"]: TIER_BPS_T[a["charter_slippage_tier"]] for a in raw["assets"]
                 if a["stem"] in CLASSIC5_T}
    return _C[k]


# ═══════════════════════════════════════════ THE REFEREE BOOK AND THE MACHINE
def corridor() -> tuple[int, int]:
    if "lo" not in _C:
        lo, hi, _ = TP.corridor_n(E.CLASSIC5)
        if hi + 1 != PIN:
            raise SystemExit(f"HALT: the corridor ends {iso(hi + 1)}, not the pin")
        _C["lo"], _C["hi"] = lo, hi
    return _C["lo"], _C["hi"]


def v6() -> dict:
    """The v6 referee: TP.run_cell_n over the TC11 corridor (F-CTRL's path), full
    precision, keyed (symbol, entry_ms)."""
    if "v6" not in _C:
        lo, hi = corridor()
        bk = TP.run_cell_n(CARD, ROLES, E.CLASSIC5, lo, hi)
        _C["v6"] = {(t.symbol, int(t.entry_ms)): t for t in bk}
        _C["v6_list"] = bk
    return _C["v6"]


def tape1(sym: str):
    k = ("tape1", sym)
    if k not in _C:
        tp = N.load11(sym, "1h")
        Hh = own1(sym)
        if not (np.array_equal(tp.t0, Hh["t"]) and np.array_equal(tp.c, Hh["c"])
                and np.array_equal(tp.h, Hh["h"]) and np.array_equal(tp.l, Hh["l"])):
            raise RuntimeError(f"{sym}: the machine's 1h tape is not this file's own read")
        _C[k] = tp
    return _C[k]


def scale_t(sym: str, scale_kind: str) -> float:
    return PICK_1H_T[sym] if scale_kind == "calibrated" else FROZEN_T


def machine(sym: str, scale_kind: str, m: int | None = None) -> dict:
    """The machine run on the 1h tape (m None) or on its PREFIX of m bars (bars
    0..m-1) at the TYPED scale — the as-of referee."""
    k = ("mach", sym, scale_kind, m)
    if k not in _C:
        tp = tape1(sym)
        _C[k] = C.run_scale(tp if m is None else tp.head(int(m)), scale_t(sym, scale_kind))["macro"]
        if m is not None and len(_C) > 4000:
            for kk in [x for x in _C if x[0] == "mach" and x[3] is not None][:2000]:
                del _C[kk]
    return _C[k]


def facts(sym: str, scale_kind: str) -> dict:
    k = ("facts", sym, scale_kind)
    if k not in _C:
        _C[k] = N.range_facts(sym, "1h", scale_kind)
    return _C[k]


def full_events(sym: str, scale_kind: str, rule: str) -> list:
    """(i, rid, side) of the rule's machine events on the full 1h tape."""
    k = ("fev", sym, scale_kind, rule)
    if k not in _C:
        _C[k] = [(int(e["i"]), int(e["rid"]), str(e["side"]))
                 for e in machine(sym, scale_kind)["events"] if e["event"] == KIND_T[rule]]
    return _C[k]


def rewalk(sym: str, scale_kind: str, rid: int, k: int) -> dict:
    """THIS file's PLAIN-LOOP RE-WALK of the breach lifecycle of range `rid` from
    its confirm bar through bar k, against the machine's AS-OF box (the bar
    before each bar: the view's top / bot at j-1), with this file's own closes
    and Wilder ATR: a breach opens on a close beyond; each further close beyond
    counts; a close back inside within 7 bars is a HARDEN (else a lapse); a
    pending breach DIES at 8 closes or a close 1.5 ATR beyond.  Returns the
    events it finds (bar, kind, side, detail)."""
    rf, Hh = facts(sym, scale_kind), own1(sym)
    c, a = Hh["c"], Hh["atr"]
    inr, rr, top, bot = rf["in_range"], rf["rid"], rf["top"], rf["bot"]
    alive = np.flatnonzero(inr[:k] & (rr[:k] == rid))
    if not len(alive):
        return {"events": [], "why": f"range {rid} is never alive before bar {k}"}
    c0 = int(alive[0])
    evs, pend = [], None
    for j in range(c0 + 1, k + 1):
        if not (inr[j - 1] and rr[j - 1] == rid):
            return {"events": evs, "why": f"range {rid} not alive at bar {j - 1}", "c0": c0}
        T, Bt = float(top[j - 1]), float(bot[j - 1])
        if pend is None:
            if c[j] > T:
                pend = {"side": "top", "open": j, "closes": 1}
            elif c[j] < Bt:
                pend = {"side": "bottom", "open": j, "closes": 1}
        else:
            beyond = c[j] > T if pend["side"] == "top" else c[j] < Bt
            if beyond:
                pend["closes"] += 1
            else:
                if j - pend["open"] <= DEV_RET_T:
                    evs.append((j, "harden", pend["side"],
                                f"breach open {iso(Hh['t'][pend['open']])}, back inside at "
                                f"{iso(Hh['t'][j] + H1)} after {j - pend['open']} bar(s) "
                                f"(close {float(c[j])!r} vs {'top' if pend['side'] == 'top' else 'bot'} "
                                f"{float(T if pend['side'] == 'top' else Bt)!r})"))
                pend = None
        if pend is not None:
            bnd = T if pend["side"] == "top" else Bt
            dist = (c[j] - bnd) if pend["side"] == "top" else (bnd - c[j])
            by_n = pend["closes"] >= BRK_N_T
            by_m = dist >= BRK_M_T * a[j] and dist > 0
            if by_n or by_m:
                evs.append((j, "breakout-die", pend["side"],
                            f"breach open {iso(Hh['t'][pend['open']])}, {pend['closes']} close(s) "
                            f"beyond {'top' if pend['side'] == 'top' else 'bot'} {float(bnd)!r}; at "
                            f"{iso(Hh['t'][j] + H1)} close {float(c[j])!r} is {float(dist / a[j]):.4f} "
                            f"ATR beyond (own ATR {float(a[j]):.6g}) -> "
                            f"{'8 closes' if by_n else '1.5 ATR'}"))
                return {"events": evs, "why": "", "c0": c0, "dead": j}
    return {"events": evs, "why": "", "c0": c0}


# ═══════════════════════════════════════════════════════════════ F-ADD
def book_adds(book: list, rule: str, arm: str) -> pd.DataFrame:
    """The adds of an in-process book, read off the Trade objects (never through
    the stage's event table)."""
    rows = []
    for t in book:
        disp = [r for r in t.add_dispositions if r["disposition"] == "admitted"]
        for q, (r, a) in enumerate(zip(disp, t.adds), start=1):
            rows.append({"registration": rule, "arm": arm, "symbol": t.symbol,
                         "entry_ms": int(t.entry_ms), "seq": q, "direction": int(t.direction),
                         "event_ms": int(r["event_ms"]), "add_ms": int(a.ms),
                         "add_px": float(a.px), "add_size": float(a.size),
                         "add_4h_open_ms": int(T9.frame(t.symbol)["f"].open_ms[int(a.i)]),
                         "moved_to_parent_close": bool(r["moved_to_parent_close"]),
                         "below_entry": bool(r["below_entry"]),
                         "post_harvest": bool(r["post_harvest"])})
    cols = ["registration", "arm", "symbol", "entry_ms", "seq", "direction", "event_ms",
            "add_ms", "add_px", "add_size", "add_4h_open_ms", "moved_to_parent_close",
            "below_entry", "post_harvest"]
    return pd.DataFrame(rows, columns=cols)


def expected_adds(t, rule: str, scale_kind: str, twin) -> list:
    """THIS file's re-derivation of one campaign's admitted adds from the
    machine's FULL run: the rule's events on the trade's side, each at its 1h
    close (the parent's close on a mismatch bar), in-trade against the own exit,
    at/after the own latch, the twin refusals, then the first 2."""
    sym, d = t.symbol, int(t.direction)
    Hh, X = own1(sym), own4(sym)
    ec, xc, lt = int(t.entry_ms) + H4, own_exit(t), own_latch(t)
    out = []
    for i, rid, side in full_events(sym, scale_kind, rule):
        if side != SIDE_FOR_T[(rule, d)]:
            continue
        ems = int(Hh["t"][i]) + H1
        if not (ec - H4 < ems <= xc + H4):
            continue
        j = bar4(sym, ems)
        if own_kids(sym, j) is None:
            teff, px = int(X["t"][j]) + H4, float(X["c"][j])
        else:
            teff, px = ems, float(Hh["c"][i])
        if not (ec < teff < xc) or lt is None or teff < lt:
            continue
        if twin == "below" and (px - float(t.entry_px)) * d < 0:
            continue
        if twin == "post" and bool(t.harvested) and j >= int(t.harvest_i):
            continue
        out.append((teff, px))
        if len(out) == ADDS_MAX_T:
            break
    return out


def label_want(sym: str, scale_kind: str, read_ms: int) -> tuple:
    """THE TYPED HONESTY LABELS of a 1h range read at `read_ms` [L-R.2, AM-4]:
    (scale_in_sample, pick_window, stability_changed)."""
    if scale_kind == "calibrated":
        return (int(read_ms) <= ERA_CUT_T, PICK_WINDOW_T["calibrated"], STAB_T[sym])
    if scale_kind == "frozen3.0":
        return (False, PICK_WINDOW_T["frozen3.0"], "NA")
    raise RuntimeError(f"no typed label law for scale {scale_kind!r}")


DISP_ORDER_T = (  # SA-2 / L-A.1 / AM-6 (s4): in-trade, the latch, the twins, THEN the cap
    "refused: pre-entry", "refused: not before the 1h-resolved exit",
    "refused: before the +1R latch", "refused: below entry (twin)",
    "refused: post-harvest (twin)", "refused: cap 2 reached", "admitted")


def expected_dispositions(t, rule: str, scale_kind: str, twin) -> list[tuple]:
    """THIS file's disposition of EVERY candidate event of one campaign, re-derived
    from the machine's FULL run (never the stage's tables): the rule's events on
    the trade's side whose 1h close lies in (entry close, close of the v6 exit 4h
    bar] [SA-2], in time order, each at its effective instant / price (the parent's
    close on a mismatch bar, L-W.0), judged in the typed order: pre-entry, not
    before the own 1h-resolved exit, before the own +1R latch (the latch child
    counts as after), the twin's class, then the 2-add cap (AM-6 s4)."""
    sym, d = t.symbol, int(t.direction)
    Hh, X = own1(sym), own4(sym)
    ec, xc, lt = int(t.entry_ms) + H4, own_exit(t), own_latch(t)
    x4 = int(t.exit_ms) + H4
    out, n_adm = [], 0
    for i, rid, side in sorted(full_events(sym, scale_kind, rule)):
        if side != SIDE_FOR_T[(rule, d)]:
            continue
        ems = int(Hh["t"][i]) + H1
        if not (ec < ems <= x4):
            continue
        j = bar4(sym, ems)
        moved = own_kids(sym, j) is None
        teff, px = (int(X["t"][j]) + H4, float(X["c"][j])) if moved else (ems, float(Hh["c"][i]))
        below = (px - float(t.entry_px)) * d < 0
        post = bool(t.harvested) and j >= int(t.harvest_i)
        if teff <= ec:
            z = DISP_ORDER_T[0]
        elif teff >= xc:
            z = DISP_ORDER_T[1]
        elif lt is None or teff < lt:
            z = DISP_ORDER_T[2]
        elif twin == "below" and below:
            z = DISP_ORDER_T[3]
        elif twin == "post" and post:
            z = DISP_ORDER_T[4]
        elif n_adm >= ADDS_MAX_T:
            z = DISP_ORDER_T[5]
        else:
            z, n_adm = DISP_ORDER_T[6], n_adm + 1
        out.append((ems, int(i), int(rid), z, teff, px, moved, below, post,
                    label_want(sym, scale_kind, ems)[0]))
    return out


DISP_COLS_T = ("event_ms", "event_i", "event_rid", "disposition", "add_ms", "add_px",
               "moved_to_parent_close", "below_entry", "post_harvest", "scale_in_sample")


def disp_findings(D: pd.DataFrame, rule: str, arm: str,
                  counts: pd.DataFrame | None = None) -> tuple[list[str], dict]:
    """Every DISPOSITIONS row of one (rule, arm) against this file's own
    dispositions of every candidate event of every v6 campaign, row by row; and
    the written DISPOSITION_COUNTS against this file's own tally."""
    sk, twin = SCALE_ARM_T[arm], TWIN_T[arm]
    V = v6()
    out, tally = [], {z: 0 for z in DISP_T}
    d = D[(D["registration"] == rule) & (D["arm"] == arm)]
    by_c = {(s_, int(m_)): g.sort_values("event_ms", kind="mergesort")
            for (s_, m_), g in d.groupby(["symbol", "entry_ms"])}
    stray = sorted(set(by_c) - set(V))
    if stray:
        out.append(f"ADD-DISP {rule} {arm}: rows for campaigns outside the v6 set {stray[:3]}")
    for key, t in V.items():
        want = expected_dispositions(t, rule, sk, twin)
        g = by_c.get(key)
        got = [] if g is None else [
            (int(r[0]), int(r[1]), int(r[2]), str(r[3]), int(r[4]), float(r[5]), bool(r[6]),
             bool(r[7]), bool(r[8]), bool(r[9]))
            for r in g[list(DISP_COLS_T)].itertuples(index=False, name=None)]
        if got != want:
            k = next((q for q in range(min(len(got), len(want))) if got[q] != want[q]),
                     min(len(got), len(want)))
            out.append(f"ADD-DISP {rule} {arm} {key[0]} {iso(key[1])}: {len(got)} written row(s) "
                       f"!= {len(want)} own; first difference at #{k}: written "
                       f"{(iso(got[k][0]), got[k][3]) if k < len(got) else 'none'} vs own "
                       f"{(iso(want[k][0]), want[k][3]) if k < len(want) else 'none'}")
        for x in want:
            tally[x[3]] += 1
    if counts is not None:
        c = counts[(counts["registration"] == rule) & (counts["arm"] == arm)]
        for z in DISP_T:
            n = c.loc[c["disposition"] == z, "n_events"]
            if len(n) != 1 or int(n.iloc[0]) != tally[z]:
                out.append(f"ADD-DISP-COUNT {rule} {arm} {z!r}: written "
                           f"{n.tolist()} != own {tally[z]}")
    return out, tally


def slice_findings(A: pd.DataFrame) -> list[str]:
    """The slices' ADDS rows ARE the scored adds of the campaigns of that era (era by
    the entry close, typed cut)."""
    out = []
    cols = ["symbol", "entry_ms", "seq", "event_ms", "add_ms", "add_px"]
    for rule in REGS_T:
        sc = A[(A["registration"] == rule) & (A["arm"] == "scored")]
        for arm, era in SLICES_T.items():
            e_ok = (sc["entry_ms"].astype(np.int64) + H4 <= ERA_CUT_T) == (era == "tuning")
            want = sorted(map(tuple, sc.loc[e_ok, cols].values.tolist()))
            got = sorted(map(tuple, A.loc[(A["registration"] == rule) & (A["arm"] == arm),
                                          cols].values.tolist()))
            if got != want:
                out.append(f"ADD-SLICE {rule} {arm}: {len(got)} ADDS rows != the {len(want)} "
                           f"scored adds of {era}-era campaigns")
    return out


def label_findings(A: pd.DataFrame, EV: pd.DataFrame, rbs: dict) -> list[str]:
    """The honesty labels [L-R.2, AM-4] against the TYPED law on every ADDS row,
    every EVENTS_1H row and every regbook row (n_adds_scale_in_sample,
    pick_window_1h, stability_changed_1h)."""
    out = []
    for r in A.itertuples():
        sk = "frozen3.0" if r.arm == "tierE__frozen3" else "calibrated"
        lw = label_want(r.symbol, sk, int(r.event_ms))
        lg = (bool(r.scale_in_sample), str(r.pick_window), str(r.stability_changed))
        if str(r.scale_kind) != sk or lg != lw:
            out.append(f"ADD-LABEL-ADDS {r.registration} {r.arm} {r.symbol} {iso(r.entry_ms)} "
                       f"add {int(r.seq)}: scale {r.scale_kind} labels {lg} != typed {sk} {lw}")
    if set(EV["scale_kind"]) != set(PICK_WINDOW_T):
        out.append(f"ADD-LABEL-EVENTS: scales {sorted(set(EV['scale_kind']))} != "
                   f"{sorted(PICK_WINDOW_T)}")
    bad_ev = 0
    first = None
    for r in EV.itertuples():
        lw = label_want(r.asset, r.scale_kind, int(r.known_close_ms))
        lg = (bool(r.scale_in_sample), str(r.pick_window), str(r.stability_changed))
        if lg != lw:
            bad_ev += 1
            first = first or f"{r.asset} {r.scale_kind} {r.event_kind} @ {iso(r.known_close_ms)} {lg} != {lw}"
    if bad_ev:
        out.append(f"ADD-LABEL-EVENTS: {bad_ev} row(s) off the typed law (first {first})")
    for (rule, arm), rb in sorted(rbs.items()):
        src = "scored" if arm == H2H_T[rule] else arm
        sk = "frozen3.0" if src == "tierE__frozen3" else "calibrated"
        a = A[(A["registration"] == rule) & (A["arm"] == src)]
        cnt: dict = {}
        for x in a.itertuples():
            if label_want(x.symbol, sk, int(x.event_ms))[0]:
                cnt[(x.symbol, int(x.entry_ms))] = cnt.get((x.symbol, int(x.entry_ms)), 0) + 1
        for r in rb.itertuples():
            k = (r.symbol, int(r.entry_ms))
            if int(r.n_adds_scale_in_sample) != cnt.get(k, 0) or str(r.pick_window_1h) != \
                    PICK_WINDOW_T["calibrated"] or str(r.stability_changed_1h) != STAB_T[r.symbol]:
                out.append(f"ADD-LABEL-REGBOOK {rule}/{arm} {r.symbol} {iso(r.entry_ms)}: "
                           f"n_adds_scale_in_sample {int(r.n_adds_scale_in_sample)} (typed "
                           f"{cnt.get(k, 0)}), pick_window_1h {r.pick_window_1h!r}, "
                           f"stability_changed_1h {r.stability_changed_1h!r} (typed "
                           f"{STAB_T[r.symbol]!r})")
    return out


def add_findings(adds: pd.DataFrame, rule: str, arm: str, events_tape: pd.DataFrame | None,
                 detail: list | None = None) -> tuple[list[str], dict]:
    """Every add of one (rule, arm) against this file's referees."""
    sk, twin = SCALE_ARM_T[arm], TWIN_T[arm]
    V = v6()
    out, n_ev = [], 0
    a = adds[(adds["registration"] == rule) & (adds["arm"] == arm)]
    by_c = {k: g.sort_values("seq") for k, g in a.groupby(["symbol", "entry_ms"])}
    for s in CLASSIC5_T:
        if N.scale_of(s, "1h", sk) != scale_t(s, sk):
            out.append(f"ADD-SCALE {s}: the module's 1h scale {N.scale_of(s, '1h', sk)} is not the "
                       f"typed {scale_t(s, sk)}")
    for key, t in V.items():
        sym, d = key[0], int(t.direction)
        g = by_c.get(key)
        got = [] if g is None else [(int(r.add_ms), float(r.add_px)) for r in g.itertuples()]
        want = expected_adds(t, rule, sk, twin)
        if got != want:
            out.append(f"ADD-SET {sym} {iso(key[1])}: admitted {[(iso(m), p) for m, p in got]} "
                       f"!= re-derived {[(iso(m), p) for m, p in want]}")
        if g is None:
            continue
        if len(g) > ADDS_MAX_T or int(g["seq"].max()) > ADDS_MAX_T:
            out.append(f"ADD-CAP {sym} {iso(key[1])}: {len(g)} adds (at most {ADDS_MAX_T})")
        Hh, X = own1(sym), own4(sym)
        ec, xc, lt = int(t.entry_ms) + H4, own_exit(t), own_latch(t)
        for r in g.itertuples():
            n_ev += 1
            tag = f"{sym} {iso(key[1])} add {int(r.seq)} @ {iso(r.add_ms)}"
            if float(r.add_size) != ADD_SIZE_T:
                out.append(f"ADD-SIZE {tag}: size {r.add_size} != {ADD_SIZE_T}")
            ems = int(r.event_ms)
            if "scale_in_sample" in a.columns:           # the honesty labels [L-R.2, AM-4]
                lw = label_want(sym, sk, ems)
                lg = (bool(r.scale_in_sample), str(r.pick_window), str(r.stability_changed))
                if lg != lw:
                    out.append(f"ADD-LABEL-ROW {tag}: (scale_in_sample, pick_window, "
                               f"stability_changed) {lg} != typed {lw}")
            k = Hh["idx"].get(ems - H1)
            if k is None:
                out.append(f"ADD-ASOF {tag}: the event instant {iso(ems)} is no 1h close")
                continue
            pre = machine(sym, sk, k + 1)            # bars 0..k: what is KNOWN at the close of k
            evk = [(int(e["rid"]), str(e["side"])) for e in pre["events"]
                   if e["event"] == KIND_T[rule] and int(e["i"]) == k]
            want_side = SIDE_FOR_T[(rule, d)]
            ok_ev = [x for x in evk if x[1] == want_side]
            if not ok_ev:
                if evk:
                    out.append(f"ADD-SIDE {tag}: the machine's {KIND_T[rule]} at {iso(ems)} is on "
                               f"the {evk[0][1]} side, not the {want_side} side of a "
                               f"{'long' if d == 1 else 'short'}")
                else:
                    out.append(f"ADD-ASOF {tag}: the machine fed the 1h bars through "
                               f"{iso(ems)} has NO {KIND_T[rule]} ({want_side}) at that close — "
                               f"the event is not known there")
                continue
            rid = ok_ev[0][0]
            if (k, rid, want_side) not in set(full_events(sym, sk, rule)):
                out.append(f"ADD-ASOF {tag}: the prefix event is not in the full run")
            box = machine(sym, sk, k)                # bars 0..k-1: the as-of box at k-1
            alive = [x for x in box["ranges"] if x.state == "CONFIRMED" and x.rid == rid]
            rf = facts(sym, sk)
            if len(alive) != 1 or not (bool(rf["in_range"][k - 1]) and int(rf["rid"][k - 1]) == rid
                                       and float(alive[0].top) == float(rf["top"][k - 1])
                                       and float(alive[0].bottom) == float(rf["bot"][k - 1])):
                out.append(f"ADD-BOX {tag}: the prefix run's live range {rid} and the as-of view "
                           f"at {iso(Hh['t'][k - 1] + H1)} disagree")
            rw = rewalk(sym, sk, rid, k)
            fk = [x for x in rw["events"] if x[1] == KIND_T[rule]]
            if rule == "P-ADD-BRK":
                ok_rw = bool(fk) and fk[0][0] == k and fk[0][2] == want_side and rw.get("dead") == k
            else:
                ok_rw = any(x[0] == k and x[2] == want_side for x in fk) and "dead" not in rw
            if not ok_rw:
                out.append(f"ADD-REWALK {tag}: the plain-loop re-walk of range {rid} gives "
                           f"{[(iso(Hh['t'][x[0]] + H1), x[1], x[2]) for x in rw['events']]} "
                           f"{rw.get('why', '')}")
            if detail is not None:
                detail.append((tag, rid, rw, k))
            if events_tape is not None:
                et = events_tape[(events_tape["asset"] == sym) & (events_tape["scale_kind"] == sk)
                                 & (events_tape["event_kind"] == SA.EVENT_OF[rule])
                                 & (events_tape["known_close_ms"] == ems)]
                if len(et) != 1 or int(et["event_rid"].iloc[0]) != rid \
                        or int(et["dir"].iloc[0]) != d or int(et["event_i"].iloc[0]) != k:
                    out.append(f"ADD-TAPE {tag}: the written 1h event tape does not hold this "
                               f"event (rid {rid}, dir {d}, bar {k})")
            j = bar4(sym, int(r.add_ms))
            moved = own_kids(sym, bar4(sym, ems)) is None
            if bool(r.moved_to_parent_close) != moved:
                out.append(f"ADD-MOVED {tag}: moved flag {r.moved_to_parent_close} != own {moved}")
            want_ms = int(X["t"][bar4(sym, ems)]) + H4 if moved else ems
            want_px = float(X["c"][bar4(sym, ems)]) if moved else float(Hh["c"][k])
            if int(r.add_ms) != want_ms or float(r.add_px) != want_px:
                out.append(f"ADD-PX {tag}: priced {float(r.add_px)!r} at {iso(r.add_ms)}, the "
                           f"{'parent' if moved else '1h'} close is {want_px!r} at {iso(want_ms)}")
            if int(r.add_4h_open_ms) != int(X["t"][j]):
                out.append(f"ADD-BAR {tag}: 4h bar {iso(r.add_4h_open_ms)} is not the bar "
                           f"containing the add ({iso(X['t'][j])})")
            if not (ec < int(r.add_ms) < xc):
                out.append(f"ADD-INTRADE {tag}: not inside (entry close {iso(ec)}, own 1h-resolved "
                           f"exit {iso(xc)})")
            if lt is None or int(r.add_ms) < lt:
                out.append(f"ADD-LATCH {tag}: before the own +1R latch "
                           f"({'none' if lt is None else iso(lt)})")
            be = (float(r.add_px) - float(t.entry_px)) * d < 0
            ph = bool(t.harvested) and j >= int(t.harvest_i)
            if bool(r.below_entry) != be or bool(r.post_harvest) != ph:
                out.append(f"ADD-FLAG {tag}: flags below {r.below_entry}/{be} post "
                           f"{r.post_harvest}/{ph}")
    return out, {"n_adds": n_ev, "n_campaigns": len(by_c)}


def ctx() -> dict:
    if "ctx" not in _C:
        _C["ctx"] = SA.context()
    return _C["ctx"]


def written(name: str) -> pd.DataFrame:
    return pd.read_parquet(str(OUT / f"{name}.parquet"))


def ride_adds(rule: str, arm: str = "scored", **kw) -> pd.DataFrame:
    return book_adds(SA.ride_arm(ctx(), rule, arm, **kw), rule, arm)


def add_break():
    orig = RD.admit_adds

    def no_latch(leg, events, **kw):
        leg2 = dict(leg)
        leg2["latch_1h_ms"] = int(kw["entry_close_ms"])
        return orig(leg2, events, **kw)

    def past_exit(leg, events, **kw):
        leg2 = dict(leg)
        leg2["exit_close_ms"] = int(leg["exit_close_ms"]) + 40 * H4
        return orig(leg2, events, **kw)

    def lookahead(rule):
        a = ride_adds(rule, event_shift_ms=-H1)
        return add_findings(a, rule, "scored", None)[0]

    def prelatch(rule):
        with mutated(RD, "admit_adds", no_latch):
            a = ride_adds(rule)
        return add_findings(a, rule, "scored", None)[0]

    def third_brk():
        a = ride_adds("P-ADD-BRK", max_adds=3)
        return add_findings(a, "P-ADD-BRK", "scored", None)[0]

    def third_sfp():
        a = written("ADDS")
        a = a[(a["registration"] == "P-ADD-SFP") & (a["arm"] == "scored")].copy()
        two = a.groupby(["symbol", "entry_ms"])["seq"].max()
        key = sorted(two[two == 2].index)[0]
        r2 = a[(a["symbol"] == key[0]) & (a["entry_ms"] == key[1]) & (a["seq"] == 2)].copy()
        r2["seq"] = 3
        return add_findings(pd.concat([a, r2], ignore_index=True), "P-ADD-SFP", "scored", None)[0]

    def wrong_side():
        orig_c = SA.candidates

        def flipped(cx, rule, scale_kind, key):
            t = cx["wmap"][key]
            s, d = key[0], int(t.direction)
            lo_ms = int(t.entry_close_ms)
            hi_ms = int(T9.frame(s)["f"].open_ms[int(t.exit_i)]) + H4
            e = cx["events"][(rule, scale_kind)][s]
            kc = e["known_close_ms"].to_numpy(np.int64)
            sel = (e["dir"].to_numpy(np.int64) == -d) & (kc > lo_ms) & (kc <= hi_ms)
            return [(int(ms), None) for ms in kc[sel]]
        out = []
        with mutated(SA, "candidates", flipped):
            for rule in REGS_T:
                out += add_findings(ride_adds(rule), rule, "scored", None)[0]
        assert orig_c is SA.candidates
        return out

    def after_exit():
        out = []
        with mutated(RD, "admit_adds", past_exit):
            for rule in REGS_T:
                out += add_findings(ride_adds(rule), rule, "scored", None)[0]
        return out

    def px_bent():
        a = written("ADDS").copy()
        i = a.index[(a["registration"] == "P-ADD-BRK") & (a["arm"] == "scored")][0]
        a.loc[i, "add_px"] = float(np.nextafter(a.loc[i, "add_px"], np.inf))
        return add_findings(a, "P-ADD-BRK", "scored", None)[0]

    def disp_dropped():                      # the stage writes only the admitted rows
        def only_admitted(leg, events, **kw):
            adds, disp = orig(leg, events, **kw)
            return adds, [r for r in disp if r["disposition"] == "admitted"]
        with mutated(RD, "admit_adds", only_admitted):
            bk = SA.ride_arm(ctx(), "P-ADD-SFP", "scored")
        D = pd.DataFrame(SA.disposition_rows(ctx(), bk, "P-ADD-SFP", "scored"))
        return disp_findings(D, "P-ADD-SFP", "scored")[0]

    def disp_relabel():
        D = written("DISPOSITIONS").copy()
        i = D.index[(D["registration"] == "P-ADD-BRK") & (D["arm"] == "scored")
                    & (D["disposition"] == "refused: before the +1R latch")][0]
        D.loc[i, "disposition"] = "refused: cap 2 reached"
        return disp_findings(D, "P-ADD-BRK", "scored")[0]

    def sis_zeroed():                        # the stage reads range facts without the flag
        rule, orig_rf = "P-ADD-BRK", N.range_facts

        def zeroed(stem, lens, scale_kind):
            rf = dict(orig_rf(stem, lens, scale_kind))
            for kk in ("die_scale_in_sample", "harden_scale_in_sample"):
                rf[kk] = np.zeros(len(np.asarray(rf[kk])), dtype=bool)
            return rf
        with mutated(N, "range_facts", zeroed):
            ev = {s: SA.event_frame(s, rule, "calibrated") for s in CLASSIC5_T}
        cx = dict(ctx())
        cx["events"] = dict(cx["events"])
        cx["events"][(rule, "calibrated")] = ev
        bk = SA.ride_arm(ctx(), rule, "scored")
        return add_findings(pd.DataFrame(SA.adds_rows(cx, bk, rule, "scored")), rule, "scored",
                            None)[0]

    def rb_sis_zeroed():
        rb = rb_frame("P-ADD-BRK", "scored").assign(n_adds_scale_in_sample=0)
        return label_findings(written("ADDS"), written("EVENTS_1H"),
                              {("P-ADD-BRK", "scored"): rb})

    def ev_stab_flipped():
        ev = written("EVENTS_1H").copy()
        m = (ev["asset"] == "ETHUSDT") & (ev["scale_kind"] == "calibrated")
        ev.loc[m, "stability_changed"] = "True"
        return label_findings(written("ADDS").head(0), ev, {})

    def slice_dropped():
        a = written("ADDS")
        i = a.index[(a["registration"] == "P-ADD-SFP") & (a["arm"] == "tierE__tuning")][0]
        return slice_findings(a.drop(index=i))

    return plants([
        ("P-ADD-BRK: deaths handed to the ride one 1h bar BEFORE they are known (look-ahead)",
         "ADD-ASOF", lambda: lookahead("P-ADD-BRK")),
        ("P-ADD-SFP: hardens handed to the ride one 1h bar BEFORE they are known (look-ahead)",
         "ADD-ASOF", lambda: lookahead("P-ADD-SFP")),
        ("P-ADD-BRK: the +1R latch gate removed from the add hook", "ADD-LATCH",
         lambda: prelatch("P-ADD-BRK")),
        ("P-ADD-SFP: the +1R latch gate removed from the add hook", "ADD-LATCH",
         lambda: prelatch("P-ADD-SFP")),
        ("P-ADD-BRK: max_adds 3 (a 3rd add admitted)", "ADD-CAP", third_brk),
        ("P-ADD-SFP: a planted 3rd add row (its cap never binds on the data)", "ADD-CAP",
         third_sfp),
        ("both rules: the events of the WRONG side handed to the ride", "ADD-SIDE", wrong_side),
        ("both rules: the 1h-resolved exit moved 40 bars later in the add hook", "ADD-INTRADE",
         after_exit),
        ("one P-ADD-BRK add price bent one ulp in a copy", "ADD-PX", px_bent),
        ("P-ADD-SFP: the add hook's refused dispositions dropped (only admitted rows written)",
         "ADD-DISP", disp_dropped),
        ("one P-ADD-BRK 'before the +1R latch' disposition relabelled 'cap 2 reached' in a copy",
         "ADD-DISP", disp_relabel),
        ("P-ADD-BRK: the SCALE-IN-SAMPLE flags zeroed on the range facts the stage reads",
         "ADD-LABEL-ROW", sis_zeroed),
        ("n_adds_scale_in_sample zeroed in a copy of the P-ADD-BRK scored regbook",
         "ADD-LABEL-REGBOOK P-ADD-BRK/scored", rb_sis_zeroed),
        ("ETHUSDT's stability_changed flipped on its calibrated EVENTS_1H rows of a copy",
         "ADD-LABEL-EVENTS", ev_stab_flipped),
        ("one P-ADD-SFP tuning-slice ADDS row dropped in a copy", "ADD-SLICE", slice_dropped),
    ])


def add_real():
    A = written("ADDS")
    EV = written("EVENTS_1H")
    D, DC = written("DISPOSITIONS"), written("DISPOSITION_COUNTS")
    lines, bad, tally, dtally = [], [], {}, {}
    rbs = {(rule, arm): rb_frame(rule, arm) for rule in REGS_T for arm in ARMS_OF_T[rule]}
    for rule in REGS_T:
        for arm in RIDDEN_T:
            det = [] if arm == "scored" else None
            f, st = add_findings(A, rule, arm, EV, det)
            bad += f
            tally[(rule, arm)] = st["n_adds"]
            if det is not None:
                lines += hand_walk_lines(rule, det)
            f, dt = disp_findings(D, rule, arm, DC)
            bad += f
            dtally[(rule, arm)] = dt
        for arm in ARMS_OF_T[rule]:
            if arm == "base":
                continue
            src = "scored" if arm == H2H_T[rule] else arm
            na = A[(A["registration"] == rule) & (A["arm"] == src)].groupby(
                ["symbol", "entry_ms"]).size()
            for r in rbs[(rule, arm)].itertuples():
                if int(r.n_adds) != int(na.get((r.symbol, int(r.entry_ms)), 0)):
                    bad.append(f"ADD-BOOK {rule} {arm} {r.symbol} {iso(r.entry_ms)}: regbook "
                               f"n_adds {r.n_adds} != ADDS rows")
    bad += label_findings(A, EV, rbs)
    bad += slice_findings(A)
    n_disp = len(D)
    if n_disp != sum(sum(v.values()) for v in dtally.values()):
        bad.append(f"ADD-DISP: {n_disp} DISPOSITIONS rows != the own "
                   f"{sum(sum(v.values()) for v in dtally.values())} candidate events")
    for (rule, arm), dt in sorted(dtally.items()):
        lines.append(f"  DISPOSITIONS {rule} {arm} (own re-derivation == written, row by row): "
                     + ", ".join(f"{z.replace('refused: ', '')} {n}" for z, n in dt.items() if n))
    n_sis = {r: int(sum(label_want(x.symbol, "calibrated", int(x.event_ms))[0]
                        for x in A[(A["registration"] == r) & (A["arm"] == "scored")].itertuples()))
             for r in REGS_T}
    total = sum(tally.values())
    n_moved = int(A[A["arm"].isin(RIDDEN_T)]["moved_to_parent_close"].sum())
    ok = not bad and all(tally[(r, "scored")] >= 3 for r in REGS_T)
    lines.append(
        f"labels [L-R.2, AM-4]: every ADDS row ({len(A)}), every EVENTS_1H row ({len(EV)}) and "
        f"every regbook row carry the TYPED law (scale_in_sample == calibrated and read <= "
        f"{iso(ERA_CUT_T)}; pick_window {PICK_WINDOW_T}; stability_changed {STAB_T} on the "
        f"calibrated scale, 'NA' on frozen 3.0); scale-in-sample adds on the scored arms "
        + ", ".join(f"{r} {n_sis[r]}/{tally[(r, 'scored')]}" for r in REGS_T)
        + "; the slices' ADDS rows == the scored adds of their era")
    lines.append(
        f"{total} admitted adds verified, every one ({'; '.join(f'{r} {a} {n}' for (r, a), n in sorted(tally.items()))}): "
        f"each event known at its 1h close by the machine fed only the prefix through that "
        f"close, on the trade's side, the plain-loop re-walk of the as-of box first meeting the "
        f"law there, the as-of box == the prefix run's live range, on the written event tape; "
        f"each add in-trade against the own 1h-resolved exit, at/after the own +1R latch, <= "
        f"{ADDS_MAX_T} per campaign, {ADD_SIZE_T} unit, priced at the own 1h close (parent close "
        f"on a mismatch bar: {n_moved} such), flags own; every one of the 200 campaigns' admitted "
        f"sets == "
        f"the re-derivation from the machine's full run, for all {len(REGS_T) * len(RIDDEN_T)} "
        f"(rule, arm) books; every candidate event's disposition ({n_disp} DISPOSITIONS rows) == "
        f"this file's own typed disposition re-derived from the machine's full run, row by row, "
        f"and DISPOSITION_COUNTS == the own tally; the typed labels hold on every row"
        + (f"; findings {len(bad)}: {bad[:4]}" if bad else ""))
    return ok, lines


def hand_walk_lines(rule: str, det: list) -> list[str]:
    """Three adds per rule printed child by child (the first three in key order)."""
    out = [f"HAND-WALK {rule} (scored; the first 3 adds in (symbol, entry, seq) order):"]
    V = v6()
    for tag, rid, rw, k in sorted(det, key=lambda x: x[0])[:3]:
        sym, ent = tag.split(" ")[0], tag.split(" ")[1]
        t = next(x for x in V.values() if x.symbol == sym and iso(x.entry_ms) == ent)
        Hh, d = own1(sym), int(t.direction)
        lt, xc = own_latch(t), own_exit(t)
        ev = [x for x in rw["events"] if x[0] == k and x[1] == KIND_T[rule]][0]
        out.append(f"  {tag}: {'long' if d == 1 else 'short'} entry close {iso(int(t.entry_ms) + H4)} "
                   f"px {float(t.entry_px)!r} R {float(t.r_dist):.6g}; own +1R latch {iso(lt)}; "
                   f"own 1h-resolved exit {iso(xc)} ({t.exit_reason})")
        out.append(f"    event: range {rid} (confirmed {iso(Hh['t'][rw['c0']] + H1)}), "
                   f"{KIND_T[rule]} {ev[2]} — {ev[3]}")
        out.append(f"    known at the 1h close {iso(Hh['t'][k] + H1)} (the machine on bars 0..{k} "
                   f"has it, on bars 0..{k - 1} the range is alive); add at that close, price = "
                   f"own 1h close {float(Hh['c'][k])!r}; latch {iso(lt)} <= add < exit {iso(xc)}")
    return out


# ═══════════════════════════════════════════════════════════════ F-ADD-BOOK
def hand_book(t, adds: list) -> dict:
    """THE HAND CALCULATION on this file's own bars and funding: the leg (the
    harvest half at its fill, the rest at the exit), each add 0.5 from its 1h
    close to the exit, fees 5 bps a side, funding from the NEXT 4h open, the D12
    ceiling ONCE on the total."""
    sym, d, R, e = t.symbol, int(t.direction), float(t.r_dist), float(t.entry_px)
    X, fund = own4(sym), own_fund(sym)
    ti, xi, xpx = int(t.entry_i), int(t.exit_i), float(t.exit_px)

    def fl(lo_j, hi_j, qty):
        s = 0.0
        for j in range(lo_j + 1, hi_j + 1):
            rate = fund.get(int(X["t"][j]))
            if rate:
                s += rate * float(X["c"][j - 1]) * d * qty
        return s
    if t.harvested:
        hj, hpx = int(t.harvest_i), float(t.harvest_px)
        g = HARVEST_Q_T * (hpx - e) * d + (1 - HARVEST_Q_T) * (xpx - e) * d
        fe = BPS_T * HARVEST_Q_T * (e + hpx) + BPS_T * (1 - HARVEST_Q_T) * (e + xpx)
        u = fl(ti, hj, HARVEST_Q_T) + fl(ti, xi, 1 - HARVEST_Q_T)
    else:
        g, fe, u = (xpx - e) * d, BPS_T * (e + xpx), fl(ti, xi, 1.0)
    add_r = 0.0
    for ms, px in adds:
        ai = bar4(sym, ms)
        ga, fa, ua = ADD_SIZE_T * (xpx - px) * d, BPS_T * ADD_SIZE_T * (px + xpx), \
            fl(ai, xi, ADD_SIZE_T)
        g, fe, u = g + ga, fe + fa, u + ua
        add_r += (ga - fa - ua) / R
    unc = u / R
    eff = min(unc, CEILING_T) if unc > CEILING_T else unc
    return {"gross_r": g / R, "fee_r": fe / R, "funding_r_uncapped": unc, "funding_r": eff,
            "net_r": g / R - fe / R - eff, "add_r": add_r}


def book_findings(rb: pd.DataFrame, adds: pd.DataFrame, rule: str, arm: str) -> tuple[list, dict]:
    V, tiers = v6(), own_tiers()
    out, worst, n_bind, n_ne = [], 0.0, 0, 0
    a = adds[(adds["registration"] == rule) & (adds["arm"] == arm)] if len(adds) else adds
    by_c = {k: [(int(r.add_ms), float(r.add_px)) for r in g.sort_values("seq").itertuples()]
            for k, g in a.groupby(["symbol", "entry_ms"])} if len(a) else {}
    for r in rb.itertuples():
        key = (r.symbol, int(r.entry_ms))
        t = V[key]
        h = hand_book(t, by_c.get(key, []))
        for col, lab in (("gross_r", "BOOK-GROSS"), ("fee_r", "BOOK-FEE"),
                         ("funding_r_uncapped", "BOOK-FUND"), ("funding_r", "BOOK-FUND"),
                         ("net_r", "BOOK-NET"), ("add_r", "BOOK-ADD-R")):
            dv = abs(float(getattr(r, col)) - h[col])
            worst = max(worst, dv)
            if not same(getattr(r, col), h[col]):
                out.append(f"{lab} {rule} {arm} {key[0]} {iso(key[1])}: {col} "
                           f"{float(getattr(r, col))!r} vs hand {h[col]!r}")
        delta = float(r.net_r) - float(t.net_r)
        absb = float(r.funding_r_uncapped) - float(r.funding_r)
        absv = float(t.funding_r_uncapped) - float(t.funding_r)
        if abs(delta - float(r.add_r) - (absb - absv)) > TOL:
            out.append(f"BOOK-AM3 {rule} {arm} {key[0]} {iso(key[1])}: Δ {delta!r} − add_r "
                       f"{float(r.add_r)!r} != absorbed {absb!r} − v6 absorbed {absv!r}")
        if float(r.v6_net_r) != float(t.net_r) or float(r.delta_net_r) != delta:
            out.append(f"BOOK-DELTA {rule} {arm} {key[0]} {iso(key[1])}: printed v6_net_r "
                       f"{float(r.v6_net_r)!r} / delta_net_r {float(r.delta_net_r)!r} != the "
                       f"referee's v6 net_r {float(t.net_r)!r} / net_r − v6 net_r {delta!r} "
                       f"(exact; AM-3: the paired Δ is net_r − v6, never add_r)")
        if absb > 0 and r.n_adds:
            n_bind += 1
        if r.n_adds and not same(delta, r.add_r):
            n_ne += 1
        hc = float(r.net_r) - float(r.fee_r) * tiers[key[0]] / TAKER_SIDE_T
        if not same(r.haircut_net_r, hc):
            out.append(f"BOOK-HAIRCUT {rule} {arm} {key[0]} {iso(key[1])}: haircut "
                       f"{float(r.haircut_net_r)!r} != net − fee × {tiers[key[0]]}/5 = {hc!r}")
    return out, {"n": len(rb), "worst": worst, "n_bind": n_bind, "n_delta_ne_add_r": n_ne}


def rb_frame(rule: str, arm: str) -> pd.DataFrame:
    return pd.read_parquet(str(REGBOOKS / rule / f"{arm}.parquet"))


def acted_findings(ACT: pd.DataFrame, rb: pd.DataFrame, rule: str, arm: str) -> list[str]:
    """The ACTED rows of one (rule, arm) == the regbook's acted campaigns, each Δ
    printed == net_r − the referee's v6 net_r EXACTLY, add_r and the absorbed
    funding == the regbook's / the referee's, the AM-3 residual re-derived."""
    V, out = v6(), []
    a = ACT[(ACT["registration"] == rule) & (ACT["arm"] == arm)]
    want = sorted((s, int(m)) for s, m, n in zip(rb["symbol"], rb["entry_ms"], rb["n_adds"])
                  if int(n) > 0)
    got = sorted((s, int(m)) for s, m in zip(a["symbol"], a["entry_ms"]))
    if got != want:
        out.append(f"BOOK-ACTED {rule} {arm}: {len(got)} ACTED rows != the regbook's "
                   f"{len(want)} acted campaigns")
    rbi = {(s, int(m)): i for i, (s, m) in enumerate(zip(rb["symbol"], rb["entry_ms"]))}
    for r in a.itertuples():
        k = (r.symbol, int(r.entry_ms))
        if k not in rbi or k not in V:
            continue
        b, t = rb.iloc[rbi[k]], V[k]
        dl = float(b["net_r"]) - float(t.net_r)
        absb = float(b["funding_r_uncapped"]) - float(b["funding_r"])
        absv = float(t.funding_r_uncapped) - float(t.funding_r)
        exact = {"net_r": float(b["net_r"]), "v6_net_r": float(t.net_r), "delta_net_r": dl,
                 "add_r": float(b["add_r"]), "funding_absorbed_r": absb,
                 "v6_funding_absorbed_r": absv, "delta_minus_add_r": dl - float(b["add_r"])}
        bad = [c for c, v in exact.items() if float(getattr(r, c)) != v]
        if bad or abs(float(r.am3_residual) - (dl - float(b["add_r"]) - (absb - absv))) > TOL:
            out.append(f"BOOK-ACTED {rule} {arm} {k[0]} {iso(k[1])}: {bad or ['am3_residual']} "
                       f"!= net_r − referee v6 / the regbook (Δ own {dl!r}, printed "
                       f"{float(r.delta_net_r)!r})")
    return out


def delta_as_add_r_run() -> dict:
    """A STAGE MUTATION (AM-3's forbidden reading): book_frame writes delta_net_r =
    add_r; the whole stage computed under it (nothing written)."""
    if "mut_delta" not in _C:
        orig = SA.book_frame

        def bent(*a, **k):
            f = orig(*a, **k)
            return f.assign(delta_net_r=f["add_r"])
        with mutated(SA, "book_frame", bent):
            _C["mut_delta"] = SA.compute()
    return _C["mut_delta"]


def book_break():
    def size_one():
        cx = ctx()
        opts = dict(SA.OPTS_OF_ARM)
        opts["scored"] = {"size": 1.0}
        with mutated(SA, "OPTS_OF_ARM", opts):
            bk = SA.ride_arm(cx, "P-ADD-BRK", "scored")
        bf = SA.book_frame(cx, bk, "P-ADD-BRK", "scored", "calibrated")
        return book_findings(bf, book_adds(bk, "P-ADD-BRK", "scored"), "P-ADD-BRK", "scored")[0]

    def bad_tier():
        cx = dict(ctx())
        fees = copy.deepcopy(cx["fees"])
        fees["BTCUSDT"]["slippage_bps_side"] = 10.0
        cx["fees"] = fees
        bf = SA.book_frame(cx, cx["walked"], "v6", "base", None)
        return book_findings(bf, pd.DataFrame(), "P-ADD-BRK", "base")[0]

    def add_r_bent():
        rb = rb_frame("P-ADD-SFP", "scored").copy()
        i = rb.index[rb["n_adds"] > 0][0]
        rb.loc[i, "add_r"] = float(rb.loc[i, "add_r"]) + 1e-6
        return book_findings(rb, written("ADDS"), "P-ADD-SFP", "scored")[0]

    def fund_bent():
        rb = rb_frame("P-ADD-BRK", "scored").copy()
        i = rb.index[(rb["n_adds"] > 0) & (rb["funding_r_uncapped"] > rb["funding_r"])][0]
        rb.loc[i, "funding_r_uncapped"] = float(rb.loc[i, "funding_r_uncapped"]) + 1e-3
        return book_findings(rb, written("ADDS"), "P-ADD-BRK", "scored")[0]

    def delta_add_r():
        R = delta_as_add_r_run()
        rule = "P-ADD-BRK"
        return book_findings(R["frames"][(rule, "scored")],
                             book_adds(R["books"][(rule, "scored")], rule, "scored"), rule,
                             "scored")[0]

    def acted_delta_add_r():
        act = written("ACTED").copy()
        m = (act["registration"] == "P-ADD-BRK") & (act["arm"] == "scored")
        act.loc[m, "delta_net_r"] = act.loc[m, "add_r"]
        return acted_findings(act, rb_frame("P-ADD-BRK", "scored"), "P-ADD-BRK", "scored")

    return plants([
        ("the stage rides P-ADD-BRK with a 1.0-unit tranche", "BOOK-NET", size_one),
        ("a corrupted charter tier (BTC 10 bps) handed to the stage", "BOOK-HAIRCUT", bad_tier),
        ("add_r bent 1e-6 on an acted P-ADD-SFP row of a copy", "BOOK-ADD-R", add_r_bent),
        ("funding_r_uncapped bent on a ceiling-bound P-ADD-BRK row of a copy", "BOOK-AM3",
         fund_bent),
        ("the stage writes delta_net_r = add_r (AM-3's forbidden reading; stage mutation)",
         "BOOK-DELTA", delta_add_r),
        ("the P-ADD-BRK scored ACTED rows' delta_net_r written as add_r in a copy", "BOOK-ACTED",
         acted_delta_add_r),
    ])


def book_real():
    A = written("ADDS")
    ACT = written("ACTED")
    bad, parts, n_act = [], [], 0
    for rule in REGS_T:
        for arm in ARMS_OF_T[rule]:
            rb = rb_frame(rule, arm)
            if arm == "base":
                ad = pd.DataFrame()
            elif arm == H2H_T[rule]:                     # the scored rows, the scored adds
                ad = A[(A["registration"] == rule) & (A["arm"] == "scored")].assign(arm=arm)
            else:
                ad = A
            f, st = book_findings(rb, ad, rule, arm)
            bad += f
            if arm in RIDDEN_T or arm in SLICES_T:
                bad += acted_findings(ACT, rb, rule, arm)
                n_act += int((rb["n_adds"] > 0).sum())
            parts.append(f"{rule} {arm} n {st['n']} worst {st['worst']:.3e} ceiling-absorbing "
                         f"acted {st['n_bind']} Δ≠add_r {st['n_delta_ne_add_r']}")
    n_ra = len(ACT[ACT["arm"].isin(RIDDEN_T + tuple(SLICES_T))])
    if n_ra != n_act or len(ACT) != n_ra:
        bad.append(f"BOOK-ACTED: {len(ACT)} ACTED rows != the {n_act} acted campaigns of the "
                   f"ridden arms and slices")
    return (not bad), ([f"  {p}" for p in parts] +
                       [f"every campaign of every arm (the base, the ridden arms, the slices, the "
                        f"head-to-head) re-booked by hand (own bars, own funding, 5 bps/side, "
                        f"harvest half, 0.5 tranches from the 1h close, funding from the next 4h "
                        f"open, the ceiling once): gross / fee / funding (uncapped, capped) / net "
                        f"/ add_r within 1e-9; AM-3 Δ − add_r == absorbed − v6 absorbed on every "
                        f"row; the printed v6_net_r and delta_net_r == the referee's v6 net_r and "
                        f"net_r − it EXACTLY on every row; the {len(ACT)} ACTED rows == the "
                        f"regbooks' acted campaigns with Δ / add_r / absorbed / residual "
                        f"re-derived; haircut == net − fee × own charter tier / 5.0 on every row"
                        + (f"; findings {len(bad)}: {bad[:4]}" if bad else "")])


# ═══════════════════════════════════════════════════════════════ F-IDENTITY
UNTOUCHED_COLS = ("net_r", "gross_r", "fee_r", "funding_r", "entry_px", "stop_px", "r_dist",
                  "exit_ms", "exit_px")
LEG_COLS = ("entry_px", "stop_px", "r_dist", "exit_ms", "exit_px")


def identity_findings(rb: pd.DataFrame, rule: str, arm: str) -> tuple[list, dict]:
    V = v6()
    out, worst = [], 0.0
    era = SLICES_T.get(arm)
    want = sorted(k for k, t in V.items()
                  if era is None or (("tuning" if int(k[1]) + H4 <= ERA_CUT_T else "holdout") == era))
    got = sorted(zip(rb["symbol"], rb["entry_ms"].astype(np.int64)))
    got = [(s, int(m)) for s, m in got]
    if got != want:
        out.append(f"PAIRED {rule} {arm}: key set {len(got)} != v6's {len(want)} "
                   f"(missing {sorted(set(want) - set(got))[:3]}, extra "
                   f"{sorted(set(got) - set(want))[:3]})")
    n_un = n_act = 0
    for r in rb.itertuples():
        t = V.get((r.symbol, int(r.entry_ms)))
        if t is None:
            continue
        cols = UNTOUCHED_COLS if int(r.n_adds) == 0 else LEG_COLS
        n_un += int(r.n_adds) == 0
        n_act += int(r.n_adds) > 0
        for c in cols:
            dv = abs(float(getattr(r, c)) - float(getattr(t, c)))
            worst = max(worst, dv)
            if dv != 0.0:
                out.append(f"IDENTITY{'-LEG' if int(r.n_adds) else ''} {rule} {arm} {r.symbol} "
                           f"{iso(r.entry_ms)}: {c} differs by {dv:.3e}")
        if r.exit_reason != t.exit_reason:
            out.append(f"IDENTITY{'-LEG' if int(r.n_adds) else ''} {rule} {arm} {r.symbol} "
                       f"{iso(r.entry_ms)}: exit_reason {r.exit_reason!r} != v6 {t.exit_reason!r}")
        if int(r.exit_close_ms) != int(t.exit_ms) + H4:
            out.append(f"IDENTITY-EXIT {rule} {arm} {r.symbol} {iso(r.entry_ms)}: exit_close_ms "
                       f"{iso(r.exit_close_ms)} != the v6 exit bar's close "
                       f"{iso(int(t.exit_ms) + H4)}")
        if int(r.exit_close_1h_ms) != own_exit(t):
            out.append(f"IDENTITY-EXIT1H {rule} {arm} {r.symbol} {iso(r.entry_ms)}: "
                       f"exit_close_1h_ms {iso(r.exit_close_1h_ms)} != own 1h-resolved exit "
                       f"{iso(own_exit(t))}")
    if arm == "base":
        out += base_ident_findings(rb)
    return out, {"n": len(rb), "unacted": n_un, "acted": n_act, "worst": worst}


def v6_campaigns() -> pd.DataFrame:
    """The v6 book of record (books/), its bytes checked against the typed sha."""
    if "v6c" not in _C:
        p = E.OUT / "books" / "v6_campaigns.parquet"
        if sha_bytes(p.read_bytes()) != V6_CAMPAIGNS_SHA_T:
            raise RuntimeError("books/v6_campaigns.parquet is not the typed bytes")
        _C["v6c"] = pd.read_parquet(str(p))
    return _C["v6c"]


def base_ident_findings(rb: pd.DataFrame) -> list[str]:
    """THIS file's BASE-IDENT: the base arm == books/v6_campaigns.parquet on its 13
    regbook columns, floats rounded to that file's 6 dp (the scorer's F-BASE-IDENT
    law, SC-7), keyed (symbol, entry_ms)."""
    v = v6_campaigns()
    out = []
    vk = {(s_, int(m_)): i for i, (s_, m_) in enumerate(zip(v["symbol"], v["entry_ms"]))}
    if sorted(vk) != sorted((s_, int(m_)) for s_, m_ in zip(rb["symbol"], rb["entry_ms"])):
        return ["BASE-IDENT: the base arm's keys are not books/v6_campaigns' keys"]
    for r in rb.itertuples():
        w = v.iloc[vk[(r.symbol, int(r.entry_ms))]]
        for a, b in V6_CMP_T:
            x, y = getattr(r, a), w[b]
            x = x.item() if isinstance(x, np.generic) else x
            y = y.item() if isinstance(y, np.generic) else y
            if isinstance(x, float):
                ok = float(pd.Series([float(x)]).round(6).iloc[0]) == float(y)
            else:
                ok = str(x) == str(y)
            if not ok:
                out.append(f"BASE-IDENT {r.symbol} {iso(r.entry_ms)}: {a} {x!r} != "
                           f"books/v6_campaigns {b} {y!r}")
    return out


def h2h_findings(rule: str, h: pd.DataFrame, sc: pd.DataFrame, opp: pd.DataFrame) -> list[str]:
    """The head-to-head arm IS the registration's scored rows (every required
    column), its opponent_net_r IS the other registration's scored net_r on the
    same key, delta_vs_opponent_net_r == net_r − it exactly, and the key sets are
    identical (the paired premise of its base_arm)."""
    out = []
    cols = list(REQUIRED_T)
    if not h[cols].reset_index(drop=True).equals(sc[cols].reset_index(drop=True)):
        out.append(f"H2H {rule}: {H2H_T[rule]} is not the {rule}/scored rows")
    om = {(s, int(m)): float(x) for s, m, x in zip(opp["symbol"], opp["entry_ms"], opp["net_r"])}
    hk = [(s, int(m)) for s, m in zip(h["symbol"], h["entry_ms"])]
    if sorted(hk) != sorted(om) or len(hk) != len(set(hk)):
        out.append(f"H2H {rule}: the key set of {H2H_T[rule]} != {H2H_BASE_T[rule]}'s (the "
                   f"paired premise)")
    nb = 0
    for r in h.itertuples():
        k = (r.symbol, int(r.entry_ms))
        o = om.get(k)
        if o is None or str(r.h2h_opponent) != H2H_BASE_T[rule] or float(r.opponent_net_r) != o \
                or float(r.delta_vs_opponent_net_r) != float(r.net_r) - o:
            nb += 1
            if nb == 1:
                out.append(f"H2H {rule} {k[0]} {iso(k[1])}: opponent {r.h2h_opponent!r} "
                           f"opponent_net_r {float(r.opponent_net_r)!r} / delta "
                           f"{float(r.delta_vs_opponent_net_r)!r} != {H2H_BASE_T[rule]} net_r "
                           f"{o!r} / net_r − it")
    if nb > 1:
        out.append(f"H2H {rule}: {nb} rows off in all")
    return out


def identity_break():
    rb = rb_frame("P-ADD-BRK", "scored")
    un, act = rb.index[rb["n_adds"] == 0], rb.index[rb["n_adds"] > 0]
    h = rb_frame("P-ADD-BRK", H2H_T["P-ADD-BRK"])
    opp = rb_frame("P-ADD-SFP", "scored")

    def h2h_bent():
        d = h.copy()
        i = d.index[d["n_adds"] > 0][0]
        d.loc[i, "opponent_net_r"] = float(d.loc[i, "opponent_net_r"]) + 1e-12
        return h2h_findings("P-ADD-BRK", d, rb, opp)

    def h2h_frozen():
        fz = rb_frame("P-ADD-BRK", "tierE__frozen3").assign(
            h2h_opponent=h["h2h_opponent"].to_numpy(object),
            opponent_net_r=h["opponent_net_r"].to_numpy(float))
        fz["delta_vs_opponent_net_r"] = fz["net_r"] - fz["opponent_net_r"]
        return h2h_findings("P-ADD-BRK", fz, rb, opp)

    def bend(col, val_fn, idx, arm="scored", src=None):
        d = (src if src is not None else rb).copy()
        d.loc[idx, col] = val_fn(d.loc[idx, col])
        return identity_findings(d, "P-ADD-BRK", arm)[0]

    base = rb_frame("P-ADD-BRK", "base")
    return plants([
        ("net_r +1e-12 on an untouched row", "IDENTITY P-ADD-BRK",
         lambda: bend("net_r", lambda v: float(v) + 1e-12, un[0])),
        ("an untouched row's exit_reason relabelled", "exit_reason",
         lambda: bend("exit_reason", lambda v: "relabelled", un[1])),
        ("an acted row's exit_px moved (the v6 leg moved by an add)", "IDENTITY-LEG",
         lambda: bend("exit_px", lambda v: float(v) * 1.001, act[0])),
        ("a row dropped (the paired premise)", "PAIRED",
         lambda: identity_findings(rb.drop(index=un[2]), "P-ADD-BRK", "scored")[0]),
        ("the base arm's exit_close_1h_ms moved 1h on one row", "IDENTITY-EXIT1H",
         lambda: bend("exit_close_1h_ms", lambda v: int(v) + H1, base.index[0], "base", base)),
        ("the base arm's exit_close_ms moved 1h earlier on one row",
         "BASE-IDENT", lambda: bend("exit_close_ms", lambda v: int(v) - H1, base.index[0], "base",
                                    base)),
        ("a scored row's exit_close_ms moved off the v6 exit bar's close", "IDENTITY-EXIT",
         lambda: bend("exit_close_ms", lambda v: int(v) + H4, un[3])),
        ("the head-to-head arm's opponent_net_r bent 1e-12 on an acted row of a copy", "H2H",
         h2h_bent),
        ("the head-to-head arm built from the frozen-3.0 twin's rows (not the scored book)",
         "is not the P-ADD-BRK/scored rows", h2h_frozen),
    ])


def identity_real():
    bad, parts = [], []
    for rule in REGS_T:
        for arm in ARMS_OF_T[rule]:
            f, st = identity_findings(rb_frame(rule, arm), rule, arm)
            bad += f
            parts.append(f"{rule} {arm}: n {st['n']} untouched {st['unacted']} acted "
                         f"{st['acted']} worst {st['worst']:.3e}")
    sc = {r: rb_frame(r, "scored") for r in REGS_T}
    for rule in REGS_T:                                  # the head-to-head IS the scored rows
        o = H2H_BASE_T[rule].split("/")[0]
        bad += h2h_findings(rule, rb_frame(rule, H2H_T[rule]), sc[rule], sc[o])
    for rule in REGS_T:                                  # the slices ARE the scored rows
        for arm, era in SLICES_T.items():
            sl = rb_frame(rule, arm)
            want = sc[rule][sc[rule]["era"] == era].reset_index(drop=True)
            cols = list(REQUIRED_T)
            if not sl[cols].reset_index(drop=True).equals(want[cols]):
                bad.append(f"SLICE {rule} {arm}: not the scored rows of era {era}")
    return (not bad), ([f"  {p}" for p in parts] +
                       [f"every campaign without an add == this file's v6 referee "
                        f"(TP.run_cell_n, full precision) on {list(UNTOUCHED_COLS)} + "
                        f"exit_reason at 0.000e+00; every acted campaign keeps the v6 leg; key "
                        f"sets == v6's (slices: v6's keys of that era, == the scored rows); each "
                        f"head-to-head arm == its scored rows, its opponent_net_r == the other "
                        f"registration's scored net_r on the same key and its delta == net_r − "
                        f"it, exactly, on identical key sets; on "
                        f"every row of every arm exit_close_ms == the v6 exit bar's close and "
                        f"exit_close_1h_ms == the own 1h-resolved exit; both base arms == "
                        f"books/v6_campaigns.parquet (sha {V6_CAMPAIGNS_SHA_T[:12]}…) on its 13 "
                        f"regbook columns at 6 dp (the scorer's F-BASE-IDENT law)"
                        + (f"; findings {len(bad)}: {bad[:4]}" if bad else "")])


# ═══════════════════════════════════════════════════════════════ F-ADD-INSTANTS
def add_instant_findings(rb: pd.DataFrame, rule: str, arm: str) -> tuple[list[str], dict]:
    """Every row's add1_close_ms / add2_close_ms against expected_adds (the machine's
    full run, the own exit / latch / walk law) for the arm's scale and twin."""
    out, tally = [], {"rows": len(rb), "n_adds": 0, "stamped": 0}
    for c in ("add1_close_ms", "add2_close_ms"):
        if c not in rb.columns:
            return [f"INSTANT-ADD: {rule} {arm} carries no {c} column"], tally
        if str(rb[c].dtype) != "Int64":
            out.append(f"INSTANT-ADD: {rule} {arm}.{c} dtype {rb[c].dtype} != Int64")
    src = "scored" if arm in (H2H_T[rule],) + tuple(SLICES_T) else arm
    V = v6()
    for r in rb.itertuples(index=False):
        got = [None if pd.isna(x) else int(x) for x in (r.add1_close_ms, r.add2_close_ms)]
        tag = f"{rule} {arm} {r.symbol} {iso(int(r.entry_ms))}"
        tally["n_adds"] += int(r.n_adds)
        tally["stamped"] += sum(x is not None for x in got)
        if src == "base":
            want = [None, None]
        else:
            t = V[(str(r.symbol), int(r.entry_ms))]
            ex = [int(x) for x, _ in expected_adds(t, rule, SCALE_ARM_T[src], TWIN_T[src])]
            want = (ex + [None, None])[:2]
            xc = own_exit(t)
            for x in ex:
                if not (int(t.entry_ms) + H4 < x < xc):
                    out.append(f"INSTANT-ADD: {tag}: add instant {iso(x)} outside (entry "
                               f"close, own 1h-resolved exit {iso(xc)})")
        if got != want:
            out.append(f"INSTANT-ADD: {tag}: (add1, add2) "
                       f"{[iso(x) if x else None for x in got]} != the re-derivation "
                       f"{[iso(x) if x else None for x in want]}")
        if sum(x is not None for x in got) != int(r.n_adds):
            out.append(f"INSTANT-ADD: {tag}: {sum(x is not None for x in got)} stamped add "
                       f"instant(s) != n_adds {int(r.n_adds)}")
        if got[0] is None and got[1] is not None or (None not in got and got[0] >= got[1]):
            out.append(f"INSTANT-ADD: {tag}: add1 {got[0]} / add2 {got[1]} not in time order")
    return out, tally


def instants_break():
    sc = rb_frame("P-ADD-BRK", "scored")
    two = sc.index[sc["n_adds"].astype(int) == 2]
    one = sc.index[sc["n_adds"].astype(int) >= 1]

    def late():
        d = sc.copy()
        d.loc[one[0], "add1_close_ms"] = int(d.loc[one[0], "add1_close_ms"]) + H1
        return add_instant_findings(d, "P-ADD-BRK", "scored")[0]

    def dropped():
        d = sc.copy()
        d.loc[two[0], "add2_close_ms"] = pd.NA
        return add_instant_findings(d, "P-ADD-BRK", "scored")[0]

    def parent_close():
        om = {s: T9.frame(s)["f"].open_ms for s in CLASSIC5_T}
        orig = SA.add_instants_of

        def mutant(t):
            a1, a2 = orig(t)
            ads = list(t.adds)
            return tuple(None if a is None else int(om[t.symbol][int(ads[k].i)]) + H4
                         for k, a in enumerate((a1, a2)))
        with mutated(SA, "add_instants_of", mutant):
            bk = SA.ride_arm(ctx(), "P-ADD-BRK", "scored")
            bf = SA.book_frame(ctx(), bk, "P-ADD-BRK", "scored", "calibrated")
        return add_instant_findings(bf, "P-ADD-BRK", "scored")[0]

    return plants([
        ("add1 moved one 1h bar late (a copy of P-ADD-BRK scored)", "INSTANT-ADD", late),
        ("add2 dropped — nulled on a 2-add row (a copy of P-ADD-BRK scored)", "INSTANT-ADD",
         dropped),
        ("[mutant] the writer's add_instants_of stamping each add at its 4h bar's CLOSE",
         "INSTANT-ADD", parent_close),
    ])


def instants_real():
    bad, lines = [], []
    for rule in REGS_T:
        parts = []
        for arm in ARMS_OF_T[rule]:
            f, t = add_instant_findings(rb_frame(rule, arm), rule, arm)
            bad += f
            parts.append(f"{arm} {t['stamped']}/{t['n_adds']}")
        lines.append(f"{rule} stamped/admitted adds: " + " · ".join(parts))
    return (not bad), lines + [
        f"add1_close_ms / add2_close_ms (Int64) on EVERY row of the "
        f"{sum(len(ARMS_OF_T[r]) for r in REGS_T)} regbooks == this file's re-derivation from "
        f"the machine's full 1h run (the rule's events on the trade's side at their 1h close, "
        f"the parent's close on an own mismatch bar, in-trade against the own 1h-resolved exit, "
        f"at/after the own +1R latch, the arm's twin, the first 2); the stamped count == "
        f"n_adds; add1 < add2; every instant inside (entry close, own exit); the base arms carry "
        f"none" + (f"; findings {len(bad)}: {bad[:4]}" if bad else "")]


# ═══════════════════════════════════════════════════════════════ F-GRID
def grid_findings(T: dict, A: pd.DataFrame, D: pd.DataFrame) -> list[str]:
    out = []

    def gw(name, declared, cells, require=()):
        d = T[name].copy()
        d["cell"] = ["|".join(str(x) for x in r) for r in d[cells].itertuples(index=False, name=None)]
        ok, lines = TP.grid_whole(declared, d, "cell", require_cols=require, label=name)
        return [f"GRID-WHOLE {x}" for x in lines if x.startswith("[BAD]")]

    col = tuple(COLLAR_T)
    out += gw("DISPOSITION_COUNTS", [f"{r}|{a}|{z}" for r in REGS_T for a in RIDDEN_T for z in DISP_T],
              ["registration", "arm", "disposition"], ("n_events",) + col)
    arms6 = RIDDEN_T + tuple(SLICES_T)
    out += gw("HEAD_TO_HEAD", [f"{a}|{r}" for a in arms6 for r in REGS_T], ["arm", "registration"],
              ("n_adds", "note") + col)
    out += gw("TIER_E_ARMS", [f"{r}|{a}" for r in REGS_T for a in ARMS_OF_T[r][2:]],
              ["registration", "arm"], ("n", "sum_net_r", "ruled_against") + col)
    out += gw("REGISTERED_BOOKS", [f"{r}|{a}" for r in REGS_T for a in ("scored", "base")],
              ["registration", "arm"], ("n", "sum_net_r", "label"))
    out += gw("OVERLAP", list(arms6), ["arm"], ("acted_both",) + col)
    out += gw("PICK_STABILITY_1H", list(CLASSIC5_T), ["asset"], ("pick_of_record",) + col)
    out += gw("MISMATCH_BOOKS", [f"{r}|{a}" for r in REGS_T for a in ("base",) + RIDDEN_T],
              ["registration", "arm"], ("n_mismatch_bars_ridden",) + col)
    dc = T["DISPOSITION_COUNTS"]
    for r in dc.itertuples():
        n = int(((D["registration"] == r.registration) & (D["arm"] == r.arm)
                 & (D["disposition"] == r.disposition)).sum())
        if n != int(r.n_events):
            out.append(f"GRID-COUNT DISPOSITION_COUNTS {r.registration}|{r.arm}|{r.disposition}: "
                       f"{r.n_events} != {n} rows")
    V, rbs = v6(), {}

    def rbf(rule, arm):
        if (rule, arm) not in rbs:
            rbs[(rule, arm)] = rb_frame(rule, arm)
        return rbs[(rule, arm)]

    def keys(rb):
        return [(s, int(m)) for s, m in zip(rb["symbol"], rb["entry_ms"])]

    def ref(rb):                            # the REFEREE's v6 net_r on the book's keys
        return np.array([float(V[k].net_r) for k in keys(rb)], dtype=float)

    def mean(x):
        return float(np.mean(x)) if len(x) else float("nan")

    def close(a, b):
        a, b = float(a), float(b)
        return (np.isnan(a) and np.isnan(b)) or (not np.isnan(a) and not np.isnan(b)
                                                 and same(a, b))

    def delta_checks(tab, cell, row, floats: dict, ints: dict):
        for c, v in floats.items():
            if not close(getattr(row, c), v):
                out.append(f"GRID-DELTA {tab} {cell}: {c} {float(getattr(row, c))!r} != "
                           f"re-derived from the regbook net_r and the referee {float(v)!r}")
        for c, v in ints.items():
            if int(getattr(row, c)) != int(v):
                out.append(f"GRID-COUNT {tab} {cell}: {c} {int(getattr(row, c))} != {int(v)}")

    for r in T["HEAD_TO_HEAD"].itertuples():
        a = A[(A["registration"] == r.registration) & (A["arm"] == r.arm)]
        rb = rbf(r.registration, r.arm)
        want = (int(len(a)), int((rb["n_adds"] > 0).sum()), len(rb))
        if (int(r.n_adds), int(r.n_campaigns_acted), int(r.n_campaigns)) != want:
            out.append(f"GRID-COUNT HEAD_TO_HEAD {r.arm}|{r.registration}: (adds, acted, n) "
                       f"{(r.n_adds, r.n_campaigns_acted, r.n_campaigns)} != {want}")
        dv, act = rb["net_r"].to_numpy(float) - ref(rb), rb["n_adds"].to_numpy(int) > 0
        sk = "frozen3.0" if r.arm == "tierE__frozen3" else "calibrated"
        delta_checks("HEAD_TO_HEAD", f"{r.arm}|{r.registration}", r,
                     {"sum_delta_net_r": dv.sum(), "mean_delta_net_r": mean(dv),
                      "mean_delta_net_r_acted": mean(dv[act]),
                      "sum_add_r": rb["add_r"].to_numpy(float).sum()},
                     {"n_adds_below_entry": a["below_entry"].sum(),
                      "n_adds_post_harvest": a["post_harvest"].sum(),
                      "n_adds_moved": a["moved_to_parent_close"].sum(),
                      "n_adds_scale_in_sample": sum(label_want(x.symbol, sk, int(x.event_ms))[0]
                                                    for x in a.itertuples())})
        if r.note != NEITHER_T:
            out.append(f"GRID-NOTE HEAD_TO_HEAD {r.arm}|{r.registration}: note {r.note!r}")
    for r in T["REGISTERED_BOOKS"].itertuples():
        if r.label != BOOK_LABEL_T:
            out.append(f"GRID-NOTE REGISTERED_BOOKS {r.registration}|{r.arm}: label {r.label!r}")
        rb = rbf(r.registration, r.arm)
        net = rb["net_r"].to_numpy(float)
        dv = net - ref(rb)
        delta_checks("REGISTERED_BOOKS", f"{r.registration}|{r.arm}", r,
                     {"sum_net_r": net.sum(), "mean_net_r": mean(net),
                      "sum_haircut_net_r": rb["haircut_net_r"].to_numpy(float).sum(),
                      "sum_delta_vs_base": dv.sum(), "mean_delta_vs_base": mean(dv)},
                     {"n": len(rb), "n_acted": (rb["n_adds"] > 0).sum(),
                      "n_adds": rb["n_adds"].sum()})
    for r in T["TIER_E_ARMS"].itertuples():
        rb = rbf(r.registration, r.arm)
        net, rv = rb["net_r"].to_numpy(float), ref(rb)
        if r.arm == H2H_T.get(r.registration):
            ruled = H2H_BASE_T[r.registration]
            ob = rbf(*ruled.split("/"))
            om = dict(zip(keys(ob), ob["net_r"].to_numpy(float)))
            ov = np.array([om[k] for k in keys(rb)], dtype=float)
        else:
            ruled, ov = "base", rv
        if str(r.ruled_against) != ruled:
            out.append(f"GRID-DELTA TIER_E_ARMS {r.registration}|{r.arm}: ruled_against "
                       f"{r.ruled_against!r} != {ruled!r}")
        delta_checks("TIER_E_ARMS", f"{r.registration}|{r.arm}", r,
                     {"sum_net_r": net.sum(), "mean_net_r": mean(net),
                      "base_sum_net_r": rv.sum(), "sum_delta_net_r": (net - rv).sum(),
                      "mean_delta_net_r": mean(net - rv),
                      "sum_add_r": rb["add_r"].to_numpy(float).sum(),
                      "ruled_base_sum_net_r": ov.sum(),
                      "sum_delta_vs_ruled_base": (net - ov).sum(),
                      "mean_delta_vs_ruled_base": mean(net - ov)},
                     {"n": len(rb), "n_acted": (rb["n_adds"] > 0).sum(),
                      "n_adds": rb["n_adds"].sum()})
    for r in T["OVERLAP"].itertuples():
        ab = {r_: {k for k, n in zip(keys(rbf(r_, r.arm)), rbf(r_, r.arm)["n_adds"]) if int(n) > 0}
              for r_ in REGS_T}
        a, b = ab["P-ADD-BRK"], ab["P-ADD-SFP"]
        delta_checks("OVERLAP", r.arm, r, {},
                     {"n_campaigns": len(rbf("P-ADD-BRK", r.arm)), "acted_brk": len(a),
                      "acted_sfp": len(b), "acted_both": len(a & b), "acted_either": len(a | b),
                      "acted_brk_only": len(a - b), "acted_sfp_only": len(b - a)})
    for r in T["PICK_STABILITY_1H"].itertuples():
        if float(r.pick_of_record) != PICK_1H_T[r.asset]:
            out.append(f"GRID-PICK {r.asset}: {r.pick_of_record} != typed {PICK_1H_T[r.asset]}")
    mb = T["MISMATCH_BARS"]
    for s, n in MISMATCH_N_T.items():
        g = mb[mb["asset"] == s]
        if len(g) != n or not set(MISMATCH_SHARED_T) <= set(g["bar_open"]):
            out.append(f"GRID-MISMATCH {s}: {len(g)} bars (typed {n}) / shared bars "
                       f"{sorted(set(MISMATCH_SHARED_T) - set(g['bar_open']))} absent")
    return out


def grid_tables() -> dict:
    return {n: written(n) for n in ("DISPOSITION_COUNTS", "HEAD_TO_HEAD", "TIER_E_ARMS",
                                     "REGISTERED_BOOKS", "OVERLAP", "PICK_STABILITY_1H",
                                     "MISMATCH_BOOKS", "MISMATCH_BARS")}


def grid_break():
    T0, A, D = grid_tables(), written("ADDS"), written("DISPOSITIONS")

    def with_(name, df):
        T = dict(T0)
        T[name] = df
        return grid_findings(T, A, D)
    dc = T0["DISPOSITION_COUNTS"]
    z = dc.index[dc["n_events"] == 0][0]
    extra = dc.iloc[[0]].copy()
    extra["disposition"] = "refused: by the weather"
    bump = dc.copy()
    bump.loc[bump.index[0], "n_events"] = int(bump.loc[bump.index[0], "n_events"]) + 1
    h = T0["HEAD_TO_HEAD"].copy()
    h.loc[h.index[3], "note"] = ""

    def delta_add_r():                       # the stage mutation: Δ written as add_r
        R = delta_as_add_r_run()
        T = {n: (SA._collar(R["T"][n]) if n not in UNCOLLARED_T else R["T"][n]) for n in T0}
        return grid_findings(T, R["T"]["ADDS"], R["T"]["DISPOSITIONS"])

    def h2h_flipped():
        te = T0["TIER_E_ARMS"].copy()
        i = te.index[(te["registration"] == "P-ADD-SFP") & (te["arm"] == H2H_T["P-ADD-SFP"])][0]
        te.loc[i, "sum_delta_vs_ruled_base"] = -float(te.loc[i, "sum_delta_vs_ruled_base"])
        return with_("TIER_E_ARMS", te)

    def slice_base_full():
        te = T0["TIER_E_ARMS"].copy()
        i = te.index[(te["registration"] == "P-ADD-BRK") & (te["arm"] == "tierE__holdout")][0]
        te.loc[i, "base_sum_net_r"] = float(T0["REGISTERED_BOOKS"]["sum_net_r"][
            (T0["REGISTERED_BOOKS"]["arm"] == "base")].iloc[0])
        return with_("TIER_E_ARMS", te)
    return plants([
        ("the stage writes delta_net_r = add_r (stage mutation): the printed Δ sums",
         "GRID-DELTA HEAD_TO_HEAD", delta_add_r),
        ("the P-ADD-SFP head-to-head ΣΔ vs P-ADD-BRK/scored sign-flipped in a copy",
         "GRID-DELTA TIER_E_ARMS", h2h_flipped),
        ("the P-ADD-BRK holdout slice's base_sum_net_r printed as the full base's in a copy",
         "base_sum_net_r", slice_base_full),
        ("a zero cell dropped from DISPOSITION_COUNTS", "missing ['",
         lambda: with_("DISPOSITION_COUNTS", dc.drop(index=z))),
        ("an undeclared disposition cell", "undeclared ['",
         lambda: with_("DISPOSITION_COUNTS", pd.concat([dc, extra], ignore_index=True))),
        ("a duplicated TIER_E_ARMS cell", "duplicated ['",
         lambda: with_("TIER_E_ARMS", pd.concat([T0["TIER_E_ARMS"], T0["TIER_E_ARMS"].iloc[[2]]],
                                                ignore_index=True))),
        ("a DISPOSITION_COUNTS count +1", "GRID-COUNT", lambda: with_("DISPOSITION_COUNTS", bump)),
        ("the head-to-head note removed on one row", "GRID-NOTE", lambda: with_("HEAD_TO_HEAD", h)),
    ])


def grid_real():
    T = grid_tables()
    bad = grid_findings(T, written("ADDS"), written("DISPOSITIONS"))
    sizes = ", ".join(f"{k} {len(v)}" for k, v in T.items())
    return (not bad), (f"every grid whole against the cells declared here ({sizes}); every "
                       f"count re-derives from DISPOSITIONS / ADDS / the regbooks; every printed "
                       f"Δ sum / mean, base sum and ruled-base sum (HEAD_TO_HEAD, "
                       f"REGISTERED_BOOKS, TIER_E_ARMS incl. the head-to-head arms) re-derives "
                       f"from the regbooks' net_r and the referee's v6 net_r (or the base_arm "
                       f"book's net_r); OVERLAP from the regbooks; the 1h picks "
                       f"== the typed {PICK_1H_T}; mismatch bars per asset == typed "
                       f"{MISMATCH_N_T} incl. {list(MISMATCH_SHARED_T)}; the head-to-head carries "
                       f"'{NEITHER_T}' on every row"
                       + (f"; findings {len(bad)}: {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-KEY
def own_canon_sha(df: pd.DataFrame) -> str:
    """THIS file's canonical CSV (the law printed in every sidecar)."""
    cols = list(REQUIRED_T)
    d = df.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    lines = [",".join(cols)]
    for row in d[cols].itertuples(index=False, name=None):
        f = []
        for c, v in zip(cols, row):
            t = REQUIRED_T[c]
            f.append(repr(float(v)) if t == "float64" else str(int(v)) if t in ("int64", "int8")
                     else str(v))
        lines.append(",".join(f))
    return sha_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def regbook_findings(rule: str, arm: str, df: pd.DataFrame, side: dict) -> list[str]:
    out = []
    tag = f"{rule}/{arm}"
    for c, t in REQUIRED_T.items():
        if c not in df.columns:
            out.append(f"KEY-COL {tag}: required column {c!r} absent")
        elif str(df[c].dtype) != t:
            out.append(f"KEY-DTYPE {tag}: {c} is {df[c].dtype}, typed {t}")
        elif df[c].isna().any():
            out.append(f"KEY-NULL {tag}: {int(df[c].isna().sum())} null(s) in {c}")
    if out:
        return out
    if df.duplicated(subset=["symbol", "entry_ms"]).any():
        out.append(f"KEY-DUP {tag}: a repeated (symbol, entry_ms)")
    era = np.where(df["entry_close_ms"].to_numpy(np.int64) <= ERA_CUT_T, "tuning", "holdout")
    if not np.array_equal(era, df["era"].to_numpy(str)):
        out.append(f"KEY-ERA {tag}: {int((era != df['era'].to_numpy(str)).sum())} era(s) not by "
                   f"the entry close")
    if not (df["entry_close_ms"] == df["entry_ms"] + H4).all():
        out.append(f"KEY-CLOSE {tag}: entry_close_ms != entry_ms + 4h")
    if not df["direction"].isin([1, -1]).all():
        out.append(f"KEY-DIR {tag}: a direction outside +/-1")
    for k in SIDECAR_KEYS_T:
        if k not in side:
            out.append(f"KEY-SIDECAR {tag}: {k!r} absent")
    kind = "scored" if arm == "scored" else "base" if arm == "base" else "tierE"
    want = {"registration": rule, "arm": arm, "kind": kind, "ruler": "paired",
            "panel": list(CLASSIC5_T), "era_scope": SLICES_T.get(arm, "full"), "n": len(df),
            "source_script": "scripts/tierc11_stage_a.py"}
    for k, v in want.items():
        if side.get(k) != v:
            out.append(f"KEY-SIDECAR {tag}: {k} {side.get(k)!r} != {v!r}")
    if not same(side.get("sum_net_r", float("nan")), float(df["net_r"].sum())):
        out.append(f"KEY-SIDECAR {tag}: sum_net_r {side.get('sum_net_r')} != {float(df['net_r'].sum())}")
    if side.get("book_sha256") != own_canon_sha(df):
        out.append(f"KEY-BOOKSHA {tag}: sidecar {str(side.get('book_sha256'))[:12]}… != this "
                   f"file's canonical CSV {own_canon_sha(df)[:12]}…")
    if kind == "tierE":
        for k, v in COLLAR_T.items():
            if side.get(k) != v:
                out.append(f"KEY-COLLAR {tag}: sidecar {k} {side.get(k)!r}")
    want_ba = H2H_BASE_T[rule] if arm == H2H_T[rule] else None   # the scorer's SC-3
    if side.get("base_arm") != want_ba:
        out.append(f"KEY-BASEARM {tag}: sidecar base_arm {side.get('base_arm')!r} != "
                   f"{want_ba!r}")
    for c in AS_OF_T:
        if c not in df.columns or df[c].isna().any():
            out.append(f"KEY-ASOF {tag}: as-of stamp {c} absent or null")
    return out


def table_findings(name: str, df: pd.DataFrame) -> list[str]:
    out = []
    key = TABLES_T[name]
    miss = [c for c in key if c not in df.columns]
    if miss:
        return [f"KEY-COL {name}: key column(s) {miss} absent"]
    if df.duplicated(subset=key).any():
        out.append(f"KEY-DUP {name}: {int(df.duplicated(subset=key).sum())} repeated key(s) {key}")
    if df[key].isna().any().any():
        out.append(f"KEY-NULL {name}: a null key cell")
    for c in AS_OF_T:
        if c not in df.columns or df[c].isna().any():
            out.append(f"KEY-ASOF {name}: as-of stamp {c} absent or null")
    if name not in UNCOLLARED_T:
        for k, v in COLLAR_T.items():
            if k not in df.columns or not (df[k] == v).all():
                out.append(f"KEY-COLLAR {name}: collar {k} absent or not {v!r} on every row")
    vc = [c for c in df.columns if c in VERDICT_COLS_T]
    if vc:
        out.append(f"KEY-VERDICT {name}: verdict column(s) {vc}")
    for c in df.columns:
        if df[c].dtype == object:
            s = df[c].astype(str)
            for w in VERDICT_WORDS_T:
                if s.str.contains(w, regex=False).any():
                    out.append(f"KEY-VERDICT {name}: the verdict word {w!r} in column {c}")
    return out


def key_findings(files: dict) -> list[str]:
    out = []
    for rule in REGS_T:
        for arm in ARMS_OF_T[rule]:
            out += regbook_findings(rule, arm, files[f"regbooks/{rule}/{arm}.parquet"],
                                    files[f"regbooks/{rule}/{arm}.json"])
        st = files[f"regbooks/{rule}/STATUS.json"]
        if st.get("registration") != rule or st.get("status") != "BUILT" \
                or st.get("arms") != list(ARMS_OF_T[rule]) or not st.get("reason"):
            out.append(f"KEY-STATUS {rule}: {st}")
        h = files[f"regbooks/{rule}/{H2H_T[rule]}.parquet"]      # SC-3's paired premise
        ob = files[f"regbooks/{H2H_BASE_T[rule]}.parquet"]
        kh = sorted((s, int(m)) for s, m in zip(h["symbol"], h["entry_ms"]))
        ko = sorted((s, int(m)) for s, m in zip(ob["symbol"], ob["entry_ms"]))
        if kh != ko:
            out.append(f"KEY-PAIRED {rule}/{H2H_T[rule]}: key set != its base_arm "
                       f"{H2H_BASE_T[rule]}'s ({len(kh)} vs {len(ko)})")
    for name in TABLES_T:
        out += table_findings(name, files[f"stage_a/{name}.parquet"])
    man = files["stage_a/STAGE_A_MANIFEST.json"]
    for rel, rec in man.get("files", {}).items():
        if rel in files and TB._content_sha(files[rel]) != rec.get("content_sha256"):
            out.append(f"KEY-MANIFEST {rel}: content sha != the manifest's")
    want = {f"stage_a/{t}.parquet" for t in TABLES_T} | {
        f"regbooks/{r}/{a}.parquet" for r in REGS_T for a in ARMS_OF_T[r]}
    if set(man.get("files", {})) != want:
        out.append(f"KEY-MANIFEST: files {sorted(set(man.get('files', {})) ^ want)[:4]} differ")
    return out


def key_files() -> dict:
    f = {}
    for rule in REGS_T:
        for arm in ARMS_OF_T[rule]:
            f[f"regbooks/{rule}/{arm}.parquet"] = rb_frame(rule, arm)
            f[f"regbooks/{rule}/{arm}.json"] = json.loads(
                (REGBOOKS / rule / f"{arm}.json").read_text(encoding="utf-8"))
        f[f"regbooks/{rule}/STATUS.json"] = json.loads(
            (REGBOOKS / rule / "STATUS.json").read_text(encoding="utf-8"))
    for name in TABLES_T:
        f[f"stage_a/{name}.parquet"] = written(name)
    f["stage_a/STAGE_A_MANIFEST.json"] = json.loads(
        (OUT / "STAGE_A_MANIFEST.json").read_text(encoding="utf-8"))
    return f


def key_break():
    F = key_files()
    rel = "regbooks/P-ADD-BRK/scored.parquet"
    sc = F[rel]

    def with_(k, v):
        G = dict(F)
        G[k] = v
        return key_findings(G)

    def era_flip():
        d = sc.copy()
        d.loc[d.index[0], "era"] = "holdout" if d.loc[d.index[0], "era"] == "tuning" else "tuning"
        return with_(rel, d)

    def sha_bent():
        s = dict(F["regbooks/P-ADD-SFP/tierE__holdout.json"])
        s["book_sha256"] = "0" + s["book_sha256"][1:]
        return with_("regbooks/P-ADD-SFP/tierE__holdout.json", s)

    def n_off():
        s = dict(F["regbooks/P-ADD-BRK/base.json"])
        s["n"] = int(s["n"]) + 1
        return with_("regbooks/P-ADD-BRK/base.json", s)

    def verdict_col():
        d = F["stage_a/TIER_E_ARMS.parquet"].copy()
        d["verdict"] = "NOT SUPPORTED"
        return with_("stage_a/TIER_E_ARMS.parquet", d)

    def base_arm_dropped():
        k = f"regbooks/P-ADD-SFP/{H2H_T['P-ADD-SFP']}.json"
        s = dict(F[k])
        s.pop("base_arm", None)
        return with_(k, s)

    def h2h_row_dropped():
        k = f"regbooks/P-ADD-BRK/{H2H_T['P-ADD-BRK']}.parquet"
        return with_(k, F[k].drop(index=F[k].index[7]))

    null = sc.copy()
    null.loc[null.index[5], "net_r"] = np.nan
    return plants([
        ("the head-to-head sidecar's base_arm dropped (the scorer would rule it vs v6)",
         "KEY-BASEARM", base_arm_dropped),
        ("a campaign dropped from a copy of the P-ADD-BRK head-to-head arm", "KEY-PAIRED",
         h2h_row_dropped),
        ("a duplicated campaign row in a copy of the P-ADD-BRK scored regbook", "KEY-DUP",
         lambda: with_(rel, pd.concat([sc, sc.iloc[[4]]], ignore_index=True))),
        ("net_r nulled on one row", "KEY-NULL", lambda: with_(rel, null)),
        ("direction written as int64", "KEY-DTYPE",
         lambda: with_(rel, sc.assign(direction=sc["direction"].astype(np.int64)))),
        ("the haircut column dropped", "KEY-COL",
         lambda: with_(rel, sc.drop(columns=["haircut_net_r"]))),
        ("one era flipped", "KEY-ERA", era_flip),
        ("a bent book_sha256 in a sidecar", "KEY-BOOKSHA", sha_bent),
        ("the collar dropped from HEAD_TO_HEAD", "KEY-COLLAR",
         lambda: with_("stage_a/HEAD_TO_HEAD.parquet",
                       F["stage_a/HEAD_TO_HEAD.parquet"].drop(columns=["tier"]))),
        ("a verdict column added to TIER_E_ARMS", "KEY-VERDICT", verdict_col),
        ("a sidecar n off by one", "KEY-SIDECAR", n_off),
    ])


def key_real():
    F = key_files()
    bad = key_findings(F)
    n_rb = sum(len(v) for k, v in F.items() if k.startswith("regbooks/") and k.endswith(".parquet"))
    n_tb = sum(len(v) for k, v in F.items() if k.startswith("stage_a/") and k.endswith(".parquet"))
    n_arms = sum(len(ARMS_OF_T[r]) for r in REGS_T)
    return (not bad), (f"{n_arms} regbooks ({n_rb} rows): the typed {len(REQUIRED_T)} "
                       f"required columns and dtypes, no null, unique (symbol, entry_ms), era by "
                       f"the entry close, entry_close == entry + 4h, direction +/-1, sidecars "
                       f"(n, sum_net_r, book_sha256 == this file's canonical CSV, kind, ruler, "
                       f"era_scope, panel, collar; base_arm {H2H_BASE_T} on the head-to-head "
                       f"arms {list(H2H_T.values())} only, their key sets == their base_arm's) "
                       f"and STATUS.json BUILT with the typed arms; {len(TABLES_T)} stage "
                       f"tables ({n_tb} rows): unique keys, no null key, the 9 as-of stamps, "
                       f"the collar on all but REGISTERED_BOOKS, no verdict column or word; "
                       f"manifest content shas == the files"
                       + (f"; findings {len(bad)}: {bad[:4]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════════ F-DET
def _files(root: Path) -> dict:
    out = {}
    sd, rd = root / "stage_a", root / "regbooks"
    if sd.exists():
        out.update({f"stage_a/{p.name}": p.read_bytes() for p in sorted(sd.iterdir())
                    if p.is_file() and p.name in STAGE_FILES_T})
    for rule in REGS_T:
        d = rd / rule
        if d.exists():
            out.update({f"regbooks/{rule}/{p.name}": p.read_bytes() for p in sorted(d.iterdir())
                        if p.is_file()})
    return out


def _canon() -> dict:
    out = {f"stage_a/{p.name}": p.read_bytes() for p in sorted(OUT.iterdir())
           if p.is_file() and p.name in STAGE_FILES_T}
    for rule in REGS_T:
        out.update({f"regbooks/{rule}/{p.name}": p.read_bytes()
                    for p in sorted((REGBOOKS / rule).iterdir()) if p.is_file()})
    return out


FILESET_T = sorted([f"stage_a/{x}" for x in STAGE_FILES_T]
                   + [f"regbooks/{r}/{x}" for r in REGS_T for x in REG_FILES_OF_T[r]])


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical", canon)):
        if sorted(x) != FILESET_T:
            out.append(f"{lab}: file set differs from the typed {len(FILESET_T)} "
                       f"({sorted(set(x) ^ set(FILESET_T))[:3]})")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                k = next((i for i in range(min(len(x[name]), len(y[name])))
                          if x[name][i] != y[name][i]), min(len(x[name]), len(y[name])))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
            if name.endswith(".parquet"):
                ca = TB._content_sha(pd.read_parquet(io.BytesIO(x[name])))
                cb = TB._content_sha(pd.read_parquet(io.BytesIO(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    return RUN_ROOT / DET_ROOT.name


def det_launch(d: Path, seed: int, hashorder: bool = False):
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_a.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\nsys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_a as SA\n"
                f"d = Path({str(d)!r})\nSA.build(d)\n"
                f"p = d / 'stage_a' / SA.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(SA.E.PANEL17)) + '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    return subprocess.Popen(cmd, env=env, cwd=str(ROOT), stdout=subprocess.DEVNULL,
                            stderr=subprocess.PIPE, text=True)


def det_collect(procs: dict) -> dict:
    out = {}
    for k, (p, d) in procs.items():
        _, err = p.communicate(timeout=1800)
        if p.returncode != 0:
            clock(f"F-DET twin {k} exit {p.returncode}: {err[-600:]}")
        out[k] = (p.returncode, _files(d) if d.exists() else {})
    return out


_DET: dict = {}
_DET_PROCS: dict = {}


def det_start() -> None:
    """Launch all four twins in parallel (fresh interpreters): the two builds of
    record and the two hash-order sabotage twins.  Collected by det_runs()."""
    if not _DET_PROCS and not _DET:
        for s in DET_SEEDS:
            d = det_dir() / f"seed_{s}"
            _DET_PROCS[("real", s)] = (det_launch(d, s), d)
            h = det_dir() / f"hashorder_{s}"
            _DET_PROCS[("hash", s)] = (det_launch(h, s, hashorder=True), h)


def det_runs() -> dict:
    if not _DET:
        det_start()
        _DET.update(det_collect(_DET_PROCS))
        _DET_PROCS.clear()
    return _DET


def det_break():
    canon = _canon()
    bent = dict(canon)
    md = bytearray(bent["stage_a/STAGE_A.md"])
    md[len(md) // 2] ^= 0x01
    bent["stage_a/STAGE_A.md"] = bytes(md)

    def float_moved():
        rel = "regbooks/P-ADD-BRK/scored.parquet"
        d = pd.read_parquet(io.BytesIO(canon[rel]))
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        buf = io.BytesIO()
        d.to_parquet(buf, index=False)
        c2 = dict(canon)
        c2[rel] = buf.getvalue()
        return det_findings((0, c2), (0, c2), canon)

    def hashorder():
        o = det_runs()
        a, b = o[("hash", DET_SEEDS[0])], o[("hash", DET_SEEDS[1])]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_A.md", "STAGE_A.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("one net_r moved 1e-6 in a regbook parquet copy", "scored.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: stage_a/STAGE_A.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = det_runs()
    a, b = o[("real", DET_SEEDS[0])], o[("real", DET_SEEDS[1])]
    bad = det_findings(a, b, canon)
    shas = ", ".join(f"{k.split('/')[-1] if k.startswith('stage_a') else k[9:]} "
                     f"{sha_bytes(v)[:10]}…" for k, v in sorted(a[1].items())
                     if k.endswith(("scored.parquet", "STAGE_A.md", "STAGE_A_MANIFEST.json")))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == the typed {len(FILESET_T)} files in both "
                       f"builds and in the record; every file byte-identical seed 1 == seed {SEED} "
                       f"== canonical, every parquet content sha equal: {not bad} ({shas})"
                       + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-ADD", "every admitted add hand-verified against the machine's 1h prefix run and "
     "this file's own tape: known at its 1h close, on the trade's side, after the latch, "
     "in-trade, <= 2, 0.5, at the 1h close [L-A.1, L-A.2, L-A.3, L-W.0, L-W.3]",
     "on any admitted add of any ridden arm: the machine on the 1h prefix through the add's "
     "event bar has no death / harden there on the trade's side; the plain-loop re-walk of "
     "the as-of box does not first meet the law (8 closes or 1.5 ATR beyond / a close back "
     "inside within 7 bars) there; the as-of box != the prefix run's live range; the event is "
     "not on the written tape; the add is out of trade, before the own +1R latch, a 3rd, "
     "not 0.5, not at the own 1h close (parent close on a mismatch bar), in another 4h bar "
     "or flagged wrongly; or a campaign's admitted set differs from the re-derivation from "
     "the machine's full run; or a candidate event's written disposition differs, row by row, "
     "from this file's typed disposition re-derived from the machine's full run (or the "
     "disposition counts from the own tally); or an ADDS / EVENTS_1H / regbook row breaks the "
     "typed scale-in-sample / pick-window / stability label law; or a slice's adds are not "
     "the scored adds of its era",
     add_break, add_real),
    ("F-ADD-BOOK", "every campaign re-booked by hand; the AM-3 Δ decomposition; the AM-7 "
     "haircut [L-A.1, AM-3, AM-7]",
     "the written gross / fee / funding (uncapped, capped) / net / add_r of any campaign of "
     "any arm differ from the hand booking by more than 1e-9; Δ − add_r != absorbed(book) − "
     "absorbed(v6); the printed v6_net_r / delta_net_r != the referee's v6 net_r / net_r − it "
     "exactly; an ACTED row does not re-derive from the regbooks and the referee; or "
     "haircut_net_r != net_r − fee_r × charter tier / 5.0",
     book_break, book_real),
    ("F-IDENTITY", "untouched campaigns carry v6 at 0.000e+00; acted ones keep the v6 leg; "
     "the paired key set [L-1.5]",
     "in any regbook a campaign without an add differs from the v6 referee on net_r, gross_r, "
     "fee_r, funding_r, entry_px, stop_px, r_dist, exit_ms, exit_px or exit_reason by ANY "
     "amount; an acted campaign's v6 leg moves; the key set is not v6's (a slice: v6's keys "
     "of its era, == the scored rows); a row's exit_close_ms is not the v6 exit bar's close or "
     "its exit_close_1h_ms not the own 1h-resolved exit; a base arm differs from "
     "books/v6_campaigns.parquet on its 13 regbook columns at 6 dp; or a head-to-head arm is "
     "not its scored rows with the other registration's scored net_r beside it exactly",
     identity_break, identity_real),
    ("F-ADD-INSTANTS", "the adds' named-event instants on every regbook row == this file's "
     "re-derivation from the machine's full run [SA-12; L-R.5, AM-6 — the lanes pass]",
     "a regbook lacks add1_close_ms / add2_close_ms (Int64), an instant differs from the "
     "re-derivation from the machine's full 1h run (1h close, parent close on a mismatch "
     "bar, in-trade, after the own latch, the twin, the first 2), the stamped count != "
     "n_adds, add1 >= add2, an instant lies outside (entry close, own exit), or a base row "
     "carries one",
     instants_break, instants_real),
    ("F-GRID", "every grid WHOLE against the cells declared here; counts re-derived",
     "a grid is not whole against the declared cells (TP.grid_whole), a count does not "
     "re-derive from the row tables, a printed Δ sum / mean, base sum or ruled-base sum does "
     "not re-derive from the regbooks' net_r and the referee's v6 net_r (or the head-to-head "
     "base_arm book), a pick is not the typed 1h pick, the mismatch bars are not the typed "
     "per-asset counts, or the head-to-head lacks its note",
     grid_break, grid_real),
    ("F-KEY", "regbook schema, sidecars, STATUS; stage-table keys, stamps, collars, no verdict",
     "a regbook lacks a typed required column or dtype, holds a null there, repeats a key, "
     "reads an era not by the entry close, or its sidecar / STATUS disagrees (incl. a "
     "base_arm anywhere but the head-to-head arms, or not the typed opponent, or a "
     "head-to-head key set != its base_arm's); a stage table "
     "repeats a key, lacks an as-of stamp or its collar, or carries a verdict; or a manifest "
     "content sha is not the file's",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_stage_a) differ from each "
     "other or from the canonical files of record in the file set, any byte or any parquet "
     "content sha, or either exits nonzero",
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
    say("TIER-C11 STAGE A FIXTURES — scripts/tierc11_stage_a.py (P-ADD-BRK / P-ADD-SFP) — "
        "break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {SNAP.name} · pin {PIN} · the machine's law typed: death at "
        f"{BRK_N_T} closes or {BRK_M_T} ATR beyond, harden within {DEV_RET_T} bars, ATR "
        f"{ATR_LEN_T} · adds <= {ADDS_MAX_T} x {ADD_SIZE_T} · 1h picks {PICK_1H_T}")
    for ln in SA.READINGS:
        say(ln)
    sel = [fx for fx in FIXTURES if not pick or any(q in fx[0].lower() for q in pick)]
    if any(fx[0] == "F-DET" for fx in sel):
        det_start()                          # the four twins run beside the other legs
    for fid, title, fails_if, b, r in sel:
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
