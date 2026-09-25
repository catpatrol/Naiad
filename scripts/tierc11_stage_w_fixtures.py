#!/usr/bin/env python
"""TIER-C11 · STAGE W — F-WARN-ASOF · F-WARN-COHORT · F-W2-HAND · F-W2-MARK · F-IDENTITY ·
F-GRID · F-KEY · F-DET.  The fixtures of scripts/tierc11_stage_w.py (the 1h event
tape, the W2 tables, the P-WARN-1 condition and its regbook) [LEANS L-W.0..L-W.6,
L-1.5; AM-5, AM-6, AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is
VOID — a guard nobody has seen fail is a guard nobody has seen.  A break leg is a
set of PLANTS judged one at a time; a plant counts as CAUGHT only if a finding
NAMES THE INTENDED DETECTOR (its expected substring).  A plant that crashes is a
FIXTURE DEFECT, never a catch.  Every plant is made on a COPY (a frame, a dict, a
temp dir) or under a MUTATION of the module restored in `finally`; no artifact of
record moves.  The referees are TYPED HERE (a second object): the pin, the three
EMA pairs, the warn label, the era cut, the collar, the regbook's required columns
and sha law, every declared grid cell, the file sets, the cluster-bootstrap law.
The hand walk reads the TC11 snapshot's raw 4h / 1h parquet itself and computes
its own EMA by a plain loop — never through the module's event code.

  F-WARN-ASOF   FAILS IF (visibility, L-W.1) any W1 event's visible_4h_close_ms is
                not the first 4h close >= its 1h close, or any W1_TIMELINE row set /
                count / stage at a 4h close T differs from this file's hand walk (the
                campaign's 4h closes in (arm close, exit-bar close]; per class the
                hand-walked events with 1h close <= T, the in-trade pre-+1R counter
                12/89 count included; stage armed / in_trade / exit_bar by the typed
                law); (causality) at any aimed or seeded cut T the module's event
                arrays on the 1h PREFIX (close <= T) differ from its arrays on the
                whole tape restricted to close <= T; (exit resolution, L-W.3) any
                IN-TRADE event is not strictly before this file's hand-walked 1h exit,
                or the PLANTED campaign's counter 12/89 cross closing after its stop
                child is not POST-EXIT / joins cohort C1.  SABOTAGE: `visible` reading
                the 1h bar that closes after the 4h close; a look-ahead event tape (a
                cross flagged one 1h bar early); the exit taken at the 4h exit-bar
                close (the plant and the real post-stop-child crosses must go RED); the
                timeline stage read with the exit-bar close counted in-trade.
  F-WARN-COHORT FAILS IF the condition cohort keys != the rule book's warn-exit keys
                plus the keys whose first qualifying cross fell on a mismatch bar
                (listed, derived here from W1_EVENTS and equal to condition.json's
                list); the W1_CAMPAIGNS C1 set differs from condition.json's; any
                condition number (cohort n / mean, book mean, delta, the cluster-90%
                lo / hi at seed 20260924 and at 20260816, MET) differs from this
                file's own recomputation (the typed cluster-bootstrap law);
                condition.json's cohort_law_holds is not the FROZEN law (cohort ==
                warn ∪ mismatch, belltie never absorbed) evaluated here; or the
                STATUS / arm set is not the typed one for the condition.  SABOTAGE:
                pre-entry crosses admitted into the in-trade classes (the in-process
                cohort must break the law); the rival (complement) delta passed off
                as the condition; the MET flag flipped; a listed mismatch key
                omitted; cohort_law_holds printed True with a belltie warn key.
  F-W2-HAND     FAILS IF, on ALL 200 v6 campaigns hand-walked from the raw 1h bars by
                a plain loop (own EMA, own walk law, own stop-in-force from the trail
                advances, own exit child and +1R child), any W1 event row (cross,
                side, phase, latch relation, taken instant, visibility, mismatch flag,
                strict re-cross flag) or any W1_CAMPAIGNS fact (exit instant, latch,
                cohort / pre-entry memberships and counts, relay cross, its instants,
                flag and leads) differs; any W2_COHORTS / W2_PREENTRY count or sum,
                or any W2_RELAY_SUMMARY cell (n, lag-0 n, relay n, share, the six lead
                statistics per lens) or W2_RELAY_HIST bin re-derived from this file's
                hand-walked leads (its own linear-interpolation percentile) differs;
                any W2_RELAY_WINDOWS_TWIN row differs from this file's hand walk of
                the twin population (the armed gate-passing windows of v6's card with
                no v6 campaign, the window end by the TYPED law, the relay cross by the
                own EMA and walk); or, planting a MISMATCH bar ONE AT A TIME under
                every C1 campaign's first C1 event, every latch bar and every stop-exit
                bar holding a W1 event, the module's re-ride + event tape disagrees with
                this file's hand walk under that plant (events taken at the parent's
                close, flagged; the parent deciding the latch / the stop).
                SABOTAGE (module mutations, W1 recomputed in-process): pre-entry
                crosses admitted as in-trade; with/against flipped for shorts; the +1R
                latch ignored; the raw 1h close kept on the planted mismatch bars; the
                relay lead median read at the 45th percentile; the twin's known window
                end one 4h bar late; the strict re-cross flag ignored.
  F-W1-OTHER    (final-review fidelity MINOR-1; readings w12..w14) FAILS IF, on ANY
                campaign of the three other 4h books — the 9/12 book (199), P-BRK-4H
                scored (322), P-RELAY-1 scored (173): every one hand-walked, the typed n
                per book and never fewer than 20 — a W1_EVENTS_OTHER row (cross, side,
                phase, latch relation, taken instant, visibility, mismatch flag, strict
                flag, era) or a W1_CAMPAIGNS_OTHER fact (the TYPED window open per book,
                the 1h-resolved exit and its resolver, the L-W.3 and L-W.5 latches,
                memberships, counts, first events, era) differs from this file's hand walk
                (own EMA, own walk law; the book's exit bar and — for a stop — its exit
                price as the stop in force; own first touching child; own +1R child); an
                event is visible at a 4h close other than the first >= its 1h close; a
                relay's hand-walked exit / L-W.5 latch differs from the regbook of record's
                exit_close_ms / latch_1h_ms; any W1_OTHER_SUMMARY cell (n campaigns, n
                events) differs from its re-derivation from the hand walk; or a fallback
                row is off the TYPED 4h-close law, has no reason, or claims a walk HALT
                where the raw 1h bars resolve the exit (and a row resolved on 1h where
                they cannot).  SABOTAGE (module mutations, the other books recomputed
                in-process; copies): `visible` reading the 1h bar that closes after the 4h
                close; a look-ahead event tape; the 9/12 / P-BRK-4H resolver walking
                children shifted one 1h bar late (the child closing after the 4h bar's
                close read); the exit taken at the 4h exit-bar close; a relay's in-trade
                window opened at its 4h bar close; P-BRK-4H's window opened at the touch;
                a summary cell bent; a 1h row relabelled a fallback with no reason; a book
                cut below 20 rows.
  F-W2-MARK     FAILS IF, for any member of C1, C2, C3, C4 or C3S, this file's OWN
                price of the first event (the tape's price at the taken instant; gross,
                taker fee 5 bps/side on every fill, funding from the snapshot's own
                funding read floored to the hour, the v6 band harvest only if its bar
                precedes the event's bar, the D12 ceiling once — the TYPED account law)
                is not the module's full-precision mark exactly; a C1 mark is not the
                rule book's net R exactly; a C2 mark is not the net R of the
                foundation ride with the 12/26 warn hook exactly (a second referee); a
                non-member warn exit of that ride is not a bell-tie at the exit
                instant; or any W1_CAMPAIGNS mark / forward leg or W2_FORWARD cell
                (n, mean final R, mean mark, mean forward, sum forward, n / share
                forward > 0) differs from its re-derivation from the OWN marks.
                SABOTAGE: the harvest booked at the event's own 4h bar (mark_at's law
                bent in-process); W2_FORWARD's mean_mark_r replaced by the mean final
                R (copy); one C4 mark moved 1e-12 (copy); C3S read without its strict
                flag (in-process).
  F-IDENTITY    FAILS IF the rule book and base do not hold identical key sets of n
                200 (the paired premise); any campaign the rule never acted on
                differs from v6 on net_r, gross_r, fee_r, funding_r, haircut_net_r,
                exit_close_ms or exit_reason (0.000e+00); the acted set is not the
                warn-exit set; an acted campaign's exit is not a warn exit strictly
                before v6's; the base arm is not the v6 book (Trade net_r exact, the
                filed TC11-BOOKS book sha, books/v6_campaigns.parquet on every shared
                required column at its 6 dp — the scorer's F-BASE-IDENT referee); the
                C1 mark is not the rule book's net R exactly (w5); or
                P_WARN_1_COMPLEMENT (net and AM-7 haircut sums) differs from its
                re-derivation from the two regbook parquets.  SABOTAGE (copies): an
                unacted campaign's net_r +1e-12; one campaign dropped from the rule
                book; an acted campaign's exit relabelled to v6's (no footprint).
  F-GRID        FAILS IF any Tier-E table's cell set is not the TYPED declared set
                (TP.grid_whole), any stage_w table or condition.json lacks the collar
                (exact values), carries a verdict column or a verdict word, n == 0 does
                not coincide with NaN stats + a nan_reason, an era split is not a
                partition (ALL = tuning + holdout; W1_OTHER_SUMMARY on n campaigns and
                n events per (book, kind, class, group)), or a relay histogram does not
                sum to its population.  The three W1 tables of the other books are in
                the typed set (W1_OTHER_SUMMARY's 522 cells declared here).  SABOTAGE
                (copies): a cell dropped; an undeclared cell; the collar removed; a
                verdict column; a verdict word; a silent NaN; a broken era partition;
                condition.json's `gates` not 'nothing'; a W1_OTHER_SUMMARY cell
                dropped; its era partition broken; W1_EVENTS_OTHER's collar removed; a
                verdict word in W1_CAMPAIGNS_OTHER.
  F-KEY         FAILS IF a stage_w table has a duplicated key or an absent / null
                as-of stamp (TP.check_keys), or a regbook parquet lacks a required
                column, has a null in one, a wrong dtype, a duplicated (symbol,
                entry_ms), rows out of (symbol, entry_close_ms) order, an era that is
                not E.era_of(entry_close_ms) by the TYPED cut, a haircut that is not
                AM-7's, an exit_close_ms that is not the 4h exit-bar close (the v6
                schema) or an exit_instant_ms outside (entry close, exit_close_ms], or
                a sidecar whose n / sum_net_r / book_sha256 (this file's own canonical
                CSV) / kind / ruler / collar / L-1.3 straddle count differ; or a
                W1_CAMPAIGNS / W2_RELAY_WINDOWS fee or AM-7 haircut column is not the
                6-dp image of the typed law on the regbook rows; or a W1_CAMPAIGNS_OTHER
                row set / net_r / fee_r / haircut_net_r / era is not the 6-dp image of
                its source book (the typed keys of the three new tables are in the
                manifest check).  SABOTAGE (copies): a duplicated row; a nulled net_r; a
                required column dropped; a float moved behind the sidecar's sha;
                TP.check_keys on a temp root with a duplicated row; a tierE sidecar
                without its collar; a straddle count bent; a W1_CAMPAIGNS haircut moved;
                a W1_CAMPAIGNS_OTHER haircut moved; a duplicated W1_EVENTS_OTHER key.
  F-DET         FAILS IF two subprocess builds (PYTHONHASHSEED 1, 20260924) under
                RUN_ROOT/_det_stage_w differ from each other or from the canonical
                files of record (stage_w/ — W1_EVENTS_OTHER, W1_CAMPAIGNS_OTHER and
                W1_OTHER_SUMMARY in the typed set — + regbooks/P-WARN-1/) in the file
                set, any byte, or any parquet content sha, or either exits nonzero.
                SABOTAGE: one byte bent in a copy; a parquet copy with one float
                moved; a hash-order-dependent line emitted under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned
magnitude bound standing in for an identity; a check whose claim is not the
design's claim.  FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11
snapshot (tierc11_env's guard).  Seed 20260924.  The transcript carries no clock
and no temp path.
SHARED INPUTS (stated, not hidden): the v6 Trades (arm, entry, stop, trail
advances, harvest bar and price) come from the foundation book (B.v6_book, itself
fixture-GREEN); the twin population's ARMINGS come from the lineage's card machine
(T9.card_candidates9 over B.ride_bounds) — this file types the gate filter, the
v6-key exclusion (books/v6_campaigns.parquet), the window-end law, the relay search,
the walk and the leads itself; the 12/26 warn referee rides the foundation ride
(RD.transform_book), never the module's mark code.  F-W1-OTHER's inputs per campaign
(entry, R, the exit bar, the exit price and reason — the WHAT the walk never changes)
come from the 9/12 foundation Trades (B.trg912_book) and the P-BRK-4H / P-RELAY-1
scored regbook parquets read here; the window open per book is TYPED here (w13); the
walk, the exit child, the +1R child, the events and every count are this file's.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_w.py            # the canonical build first
      ~/venvs/naiad/bin/python -B scripts/tierc11_stage_w_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a
transcript finding, or a HALT.
"""
from __future__ import annotations

import contextlib
import copy
import csv
import hashlib
import io
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
import tierc11_stage_w as S                                          # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

B, RD, E = S.B, S.RD, S.E
TP, T9, T5, TB = E.TP, E.T9, E.T5, E.TB
iso = TB.iso

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never S's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
PIN = 1790294400000                      # 2026-09-25T00:00:00Z [L-0.1]
H1, H4 = 3_600_000, 14_400_000
SEED, SEED_SENS, N_BOOT = 20260924, 20260816, 4000
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
ERA_CUT = 1_719_791_999_000              # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
TOL = 1e-9                               # the be_sequence REPRESENTATION law [L-W.0]
CLASSIC5_TYPED = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
PAIRS_TYPED = {"9/12": (9, 12), "12/26": (12, 26), "12/89": (12, 89)}    # L-W.2
WARN_LBL = "warn_1h_12_89"
N_BOOK = 200
COLLAR_TYPED = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                "gates": "nothing"}
VERDICT_COLS = ("verdict", "verdict_of_record", "clears_bh_bar", "promotable",
                "scored_in_family", "p_one_sided", "is_the_registered_cell")
VERDICT_WORDS = ("SUPPORTED", "PASS", "FAIL", "VERDICT", "CONFIRM")
ERAS_T = ("ALL", "tuning", "holdout")
# cohort commission [contract W2 / L-W.4]: id, label, pair, side, latch relation, at-risk
COHORTS_T = (("C1", "counter_12_89_before_1r", "12/89", "counter", "before", "whole"),
             ("C2", "counter_12_26_before_1r", "12/26", "counter", "before", "whole"),
             ("C3", "with_9_12_recross_after_entry", "9/12", "with", "any", "open1h"),
             ("C4", "counter_12_89_after_1r", "12/89", "counter", "after", "reached"),
             # (w10) the strict re-cross reading, printed beside C3
             ("C3S", "with_9_12_recross_strict", "9/12", "with", "any", "open1h"))
STRICT_T = ("C3S",)
WARN26_LBL = "warn_1h_12_26"             # RD.warn_of(walk, 12, 26)'s label
HARVEST_FRAC_T = 0.5                     # card v6: half harvested at the band
FUND_CAP_T = 1.0                         # D12: the funding ceiling, 1R, once per campaign
PRE_T = (("P1", "counter_12_89", "12/89", "counter"), ("P2", "counter_12_26", "12/26", "counter"),
         ("P3", "with_9_12", "9/12", "with"), ("P4", "with_12_26", "12/26", "with"))
LAGS_T = ("ALL", "0", "1-6", "7-15", ">=16")
LEAD_STATS_T = ("min", "q25", "median", "q75", "max", "mean")
L1_BINS_T = (("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8-15", 8, 15), ("16-31", 16, 31),
             ("32-63", 32, 63), ("64-127", 64, 127), ("128-255", 128, 255), (">=256", 256, None))
L4_BINS_T = (("0", 0, 0), ("1", 1, 1), ("2-3", 2, 3), ("4-7", 4, 7), ("8-15", 8, 15),
             ("16-31", 16, 31), ("32-63", 32, 63), (">=64", 64, None))
# (w12..w14) the other 4h books — the commission: the three books, each book's n of
# record (books/trg912_campaigns.parquet; the P-BRK-4H and P-RELAY-1 scored sidecars),
# the floor of hand-walked campaigns per book, the W1 event classes
OTHER_BOOKS_T = ("trg912", "P-BRK-4H", "P-RELAY-1")
N_OTHER_T = {"trg912": 199, "P-BRK-4H": 322, "P-RELAY-1": 173}
MIN_HAND_T = 20
PHASES_T = ("PRE-ENTRY", "IN-TRADE", "AT-EXIT", "POST-EXIT")
EV_CLASSES_T = tuple(f"{ph}|{p}|{sd}|{rl}" for ph in PHASES_T for p in PAIRS_TYPED
                     for sd in ("counter", "with")
                     for rl in (("before", "after") if ph == "IN-TRADE" else ("-",)))
DECLARED = {
    "W2_COHORTS": [f"{c}_{lab}|{g}|{e}" for c, lab, *_ in COHORTS_T
                   for e in ERAS_T for g in ("cohort", "at_risk", "complement")],
    "W2_FORWARD": [f"{c}_{lab}|{e}" for c, lab, *_ in COHORTS_T for e in ERAS_T],
    "W2_PREENTRY": [f"{p}_{lab}|{g}|{e}" for p, lab, *_ in PRE_T
                    for e in ERAS_T for g in ("cohort", "whole_book", "complement")],
    "W2_RELAY_SUMMARY": ([f"v6_campaigns|{e}|{lb}" for e in ERAS_T for lb in LAGS_T]
                         + [f"armed_windows_not_entered|{e}|ALL" for e in ERAS_T]),
    "W2_RELAY_HIST": [f"{pop}|{m}|{b}" for pop in ("v6_campaigns", "armed_windows_not_entered")
                      for m, bins in (("lead_1h", L1_BINS_T), ("lead_4h", L4_BINS_T))
                      for b in [x[0] for x in bins] + ["none"]],
    "P_WARN_1_COMPLEMENT": [f"{g}|{e}" for g in ("cohort_C1", "complement_C1", "acted",
                                                  "unacted", "ALL") for e in ERAS_T],
    "W1_OTHER_SUMMARY": [c for bk in OTHER_BOOKS_T for e in ERAS_T for c in (
        [f"{bk}|{e}|campaigns|all|book"]
        + [f"{bk}|{e}|events|{cls}|events" for cls in EV_CLASSES_T]
        + [f"{bk}|{e}|cohort|{cid}_{lab}|{g}" for cid, lab, *_ in COHORTS_T
           for g in ("cohort", "at_risk", "complement")]
        + [f"{bk}|{e}|pre_entry|{pid}_{lab}|{g}" for pid, lab, *_ in PRE_T
           for g in ("cohort", "whole_book", "complement")])],
}
KEYS_TYPED = {"W1_EVENTS": ["symbol", "entry_ms", "pair", "h1_open_ms"],
              "W1_TIMELINE": ["symbol", "entry_ms", "bar_close_ms"],
              "W1_CAMPAIGNS": ["symbol", "entry_ms"],
              "W2_COHORTS": ["cell"], "W2_FORWARD": ["cell"], "W2_PREENTRY": ["cell"],
              "W2_RELAY_WINDOWS": ["symbol", "entry_ms"],
              "W2_RELAY_WINDOWS_TWIN": ["symbol", "arm_ms", "direction"],
              "W2_RELAY_SUMMARY": ["cell"], "W2_RELAY_HIST": ["cell"],
              "P_WARN_1_COMPLEMENT": ["cell"],
              "W1_EVENTS_OTHER": ["book", "symbol", "entry_close_ms", "pair", "h1_open_ms"],
              "W1_CAMPAIGNS_OTHER": ["book", "symbol", "entry_close_ms"],
              "W1_OTHER_SUMMARY": ["cell"]}
STAGE_FILES_TYPED = tuple(sorted([f"{k}.parquet" for k in KEYS_TYPED]
                                 + ["MANIFEST_STAGE_W.json", "STAGE_W.md"]))
REQUIRED_T = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
              "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r",
              "funding_r", "haircut_net_r", "era", "lane")
REQ_DTYPES_T = {"symbol": "object", "entry_ms": "int64", "entry_close_ms": "int64",
                "direction": "int8", "entry_px": "float64", "stop_px": "float64",
                "r_dist": "float64", "exit_close_ms": "int64", "exit_reason": "object",
                "net_r": "float64", "gross_r": "float64", "fee_r": "float64",
                "funding_r": "float64", "haircut_net_r": "float64", "era": "object",
                "lane": "object"}
ARMS_T = {"BUILT": ("scored", "base", "tierE__tuning", "tierE__holdout"),
          "CONDITION_NOT_MET": ("tierE__rule_book_condition_not_met", "base",
                                "tierE__tuning", "tierE__holdout")}
KIND_T = {"scored": "scored", "base": "base", "tierE__tuning": "tierE",
          "tierE__holdout": "tierE", "tierE__rule_book_condition_not_met": "tierE"}
SCOPE_T = {"scored": "full", "base": "full", "tierE__tuning": "tuning",
           "tierE__holdout": "holdout", "tierE__rule_book_condition_not_met": "full"}
SIDECAR_KEYS_T = ("registration", "arm", "kind", "ruler", "panel", "era_scope", "n",
                  "sum_net_r", "book_sha256", "description", "source_script")
COND_KEYS_T = ("cohort_n", "cohort_mean", "book_mean", "delta", "ci_lo", "ci_hi", "met",
               "seed", "n_boot", "sens_seed_ci")
SLIP_T = {"BTCUSDT": 2.0, "ETHUSDT": 2.0, "SOLUSDT": 5.0, "NEARUSDT": 5.0, "ZECUSDT": 5.0}
TAKER_T = 5.0
BPS_T = TAKER_T / 10_000.0               # the taker fee per side, as a fraction

OUT = S.OUT
REG_DIR = S.REG_DIR
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_STAGE_W.txt"
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
            caught.append(f"{name} -> {shown} [{len(found)} finding(s)]")
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


def verdict(bad: list, ok_line: str) -> tuple[bool, str]:
    return (not bad), (ok_line if not bad else f"{len(bad)} finding(s): " + " · ".join(
        str(x)[:220] for x in bad[:4]))


def _env() -> dict:
    return dict(os.environ, NAIAD_CACHE_DIR=str(TC11_SNAP), PYTHONDONTWRITEBYTECODE="1")


def kstr(s, e) -> str:
    return f"{s}|{int(e)}"


# ═══════════════════════════════════════════════ THE RECORD (read back) + LIVE
_C: dict = {}


def written(name: str) -> pd.DataFrame:
    k = ("w", name)
    if k not in _C:
        _C[k] = pd.read_parquet(str(OUT / f"{name}.parquet"))
    return _C[k].copy()


def reg_parquet(arm: str) -> pd.DataFrame:
    return pd.read_parquet(str(REG_DIR / f"{arm}.parquet"))


def reg_json(name: str) -> dict:
    return json.loads((REG_DIR / name).read_text(encoding="utf-8"))


def rides() -> dict:
    return S.rides()


def base() -> list:
    return rides()["base"]


def full_campaigns() -> pd.DataFrame:
    """The module's W1_CAMPAIGNS at FULL precision, marks included (in-process; the
    written table carries the marks at 6 dp)."""
    if "fullc" not in _C:
        _C["fullc"] = S.campaign_table(S.w1(rides())["camps"], marks=True)
    return _C["fullc"].copy()


def module_w1() -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """The module's W1 recomputed IN-PROCESS (the path a mutation is judged on)."""
    W = S.w1(rides())
    c = S.campaign_table(W["camps"], marks=False)
    ev = pd.DataFrame(W["events"])
    tl = pd.DataFrame(W["timeline"])
    return ev, c, {"W": W, "timeline": tl}


# ═══════════════════════════════════ THIS FILE'S OWN READ OF THE SNAPSHOT + WALK
def own_bars(sym: str, lens: str) -> pd.DataFrame:
    k = ("own", sym, lens)
    if k not in _C:
        step = {"1h": H1, "4h": H4}[lens]
        d = pd.read_parquet(str(TC11_SNAP / "klines" / f"{sym}_{lens}.parquet"))
        d = d.sort_values("open_time", kind="mergesort")
        d = d[d["open_time"] + step <= PIN].reset_index(drop=True)
        _C[k] = d
    return _C[k]


def own_ema(x, n: int) -> np.ndarray:
    """A plain recursive EMA (alpha 2/(n+1), seeded at the first value) — THIS
    file's loop, never the engine's."""
    a = 2.0 / (n + 1.0)
    out = np.empty(len(x))
    prev = None
    for i, v in enumerate(x):
        v = float(v)
        if v != v:
            raise RuntimeError("a NaN close in the own read")
        prev = v if prev is None else prev + a * (v - prev)
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
        b = own_bars(sym, "4h")
        om = b["open_time"].to_numpy(np.int64)
        h, l, c = (b[x].to_numpy(float) for x in ("high", "low", "close"))
        f = T9.frame(sym)["f"]
        if not (np.array_equal(om, np.asarray(f.open_ms, dtype=np.int64))
                and np.array_equal(h, f.h) and np.array_equal(l, f.l)
                and np.array_equal(c, f.c)):
            raise RuntimeError(f"{sym}: the own 4h read is not the module's frame")
        _C[k] = dict(om=om, h=h, l=l, c=c, closes=om + H4)
    return _C[k]


def own1(sym: str) -> dict:
    k = ("own1", sym)
    if k not in _C:
        b = own_bars(sym, "1h")
        t = b["open_time"].to_numpy(np.int64)
        if not np.array_equal(t, RD.h1_tape(sym).open_ms):
            raise RuntimeError(f"{sym}: the own 1h read is not row-aligned with the module's")
        c = b["close"].to_numpy(float)
        crosses, prev = {}, {}
        for p, (fa, sl) in PAIRS_TYPED.items():
            up, dn = own_cross(own_ema(c, fa), own_ema(c, sl))
            crosses[p] = (up, dn)
            # the pair's crosses in tape order; each one's PRECEDING cross (w10's input)
            seq = sorted([(int(x), "up") for x in np.flatnonzero(up)]
                         + [(int(x), "dn") for x in np.flatnonzero(dn)])
            pm, last = {}, (None, None)
            for kk, cr in seq:
                pm[kk] = last
                last = (cr, int(t[kk]) + H1)
            prev[p] = pm
        _C[k] = dict(t=t, o=b["open"].to_numpy(float), h=b["high"].to_numpy(float),
                     l=b["low"].to_numpy(float), c=c,
                     idx={int(x): i for i, x in enumerate(t)}, crosses=crosses, prev=prev)
    return _C[k]


def same(a, b_) -> bool:
    return abs(float(a) - float(b_)) <= TOL * max(1.0, abs(float(a)), abs(float(b_)))


def own_kids(sym: str, J: int, planted: frozenset = frozenset()):
    """THIS file's walk law: the 4 rows of bar J on the 1h grid (none other in the
    bar) reproducing its high, low and close to the representation tolerance;
    else None (a mismatch bar).  A bar in `planted` is a mismatch bar (the
    fixture's plant)."""
    if int(J) in planted:
        return None
    k = ("kids", sym, int(J))
    if k not in _C:
        X, Hh = own4(sym), own1(sym)
        o4 = int(X["om"][J])
        ks = [Hh["idx"].get(o4 + q * H1) for q in range(4)]
        n_in = int(np.searchsorted(Hh["t"], o4 + H4, "left") - np.searchsorted(Hh["t"], o4, "left"))
        ok = all(x is not None for x in ks) and n_in == 4
        if ok:
            ok = (same(max(Hh["h"][x] for x in ks), X["h"][J])
                  and same(min(Hh["l"][x] for x in ks), X["l"][J])
                  and same(Hh["c"][ks[3]], X["c"][J]))
        _C[k] = ks if ok else None
    return _C[k]


def stop_at(t, j: int) -> float:
    """The stop in force at bar j of a v6 campaign (its trail advances, conf < j)."""
    st = float(t.stop_px)
    for a in t.advances:
        if a.conf_i < j:
            st = float(a.new_stop)
    return st


def bar_of(sym: str, open_ms: int) -> int:
    """The 4h bar of the own frame holding the 1h bar opening at open_ms."""
    return int(np.searchsorted(own4(sym)["om"], int(open_ms), "right")) - 1


def side_t(cross: str, d: int) -> str:
    """TYPED L-W.2: with = the fast line crosses in the trade's direction."""
    return "with" if (cross == "up") == (int(d) == 1) else "counter"


def hand_campaign(t, planted: frozenset = frozenset()) -> dict:
    """THE HAND WALK of one v6 campaign from the raw bars [L-W.0..L-W.3, w1, w2,
    w10]; `planted` = bars this file declares mismatch bars (the parent decides)."""
    planted = frozenset(int(x) for x in planted)
    k0 = ("hand", t.symbol, int(t.entry_ms), planted)
    if k0 in _C:
        return _C[k0]
    s, d, e, R = t.symbol, int(t.direction), float(t.entry_px), float(t.r_dist)
    X, Hh = own4(s), own1(s)
    arm_close = int(X["om"][int(t.arm_i)]) + H4
    entry_close = int(X["om"][int(t.entry_i)]) + H4
    exit_close, latch, by, latch_by = None, None, None, None
    for j in range(int(t.entry_i) + 1, int(t.exit_i) + 1):
        stp = stop_at(t, j)
        ks = own_kids(s, j, planted)
        close_j = int(X["om"][j]) + H4
        if ks is not None:
            for k in ks:
                hi_, lo_ = float(Hh["h"][k]), float(Hh["l"][k])
                fav = hi_ if d == 1 else lo_
                if latch is None and (fav - e) * d / R >= 1.0:
                    latch, latch_by = int(Hh["t"][k]) + H1, "1h"
                if (d == 1 and lo_ <= stp) or (d == -1 and hi_ >= stp):
                    exit_close, by = int(Hh["t"][k]) + H1, "1h"
                    break
        else:
            fav = float(X["h"][j]) if d == 1 else float(X["l"][j])
            if latch is None and (fav - e) * d / R >= 1.0:
                latch, latch_by = close_j, "parent"
            if (d == 1 and float(X["l"][j]) <= stp) or (d == -1 and float(X["h"][j]) >= stp):
                exit_close, by = close_j, "parent"
        if exit_close is not None:
            if j != int(t.exit_i) or t.exit_reason != "stop":
                raise RuntimeError(f"{s} {iso(int(t.entry_ms))}: the hand walk stops at bar "
                                   f"{j}, v6 exits at {t.exit_i} ({t.exit_reason}) — a fixture "
                                   f"defect")
            break
    if exit_close is None:
        if t.exit_reason == "stop":
            raise RuntimeError(f"{s}: v6 stopped and the hand walk found no stop child")
        exit_close, by = int(X["om"][int(t.exit_i)]) + H4, "close"
    exit_bar_close = int(X["om"][int(t.exit_i)]) + H4
    evs = []
    k_lo = int(np.searchsorted(Hh["t"], arm_close - H4, "left"))
    k_hi = int(np.searchsorted(Hh["t"], exit_bar_close, "left"))
    for p in PAIRS_TYPED:
        up, dn = Hh["crosses"][p]
        for cross, arr in (("up", up), ("dn", dn)):
            for k in range(k_lo, k_hi):
                if not arr[k]:
                    continue
                op = int(Hh["t"][k])
                close = op + H1
                J = bar_of(s, op)
                walk = own_kids(s, J, planted) is not None
                taken = close if walk else int(X["om"][J]) + H4
                if not (arm_close < taken <= exit_bar_close):
                    continue
                if taken <= entry_close:
                    ph = "PRE-ENTRY"
                elif taken < exit_close:
                    ph = "IN-TRADE"
                elif taken == exit_close:
                    ph = "AT-EXIT"
                else:
                    ph = "POST-EXIT"
                side = side_t(cross, d)
                rel = None
                if ph == "IN-TRADE":
                    rel = "before" if (latch is None or taken < latch) else "after"
                vis = int(X["closes"][int(np.searchsorted(X["closes"], close, "left"))])
                pc, pcl = Hh["prev"][p].get(k, (None, None))
                strict = bool(p == "9/12" and side == "with" and pc is not None
                              and side_t(pc, d) == "counter" and int(pcl) > entry_close)
                evs.append({"pair": p, "cross": cross, "h1_open_ms": op, "close_ms": close,
                            "taken_ms": taken, "on_mismatch_bar": not walk, "phase": ph,
                            "side": side, "latch_rel": rel, "visible_4h_close_ms": vis,
                            "recross_strict": strict, "k": k, "J": J})
    out = {"arm_close": arm_close, "entry_close": entry_close, "exit_close": exit_close,
           "exit_by": by, "exit_bar_close": exit_bar_close, "latch": latch,
           "latch_by": latch_by, "events": evs,
           "net_r": float(t.net_r), "era": "tuning" if entry_close <= ERA_CUT else "holdout",
           "lag": int(t.entry_i) - int(t.arm_i), "d": d}
    _C[k0] = out
    return out


def hand_classes(h: dict) -> dict:
    """Cohort / pre-entry memberships and the relay cross from the hand walk."""
    evs = h["events"]
    out = {}
    for cid, _lab, pair, side, rel, _ar in COHORTS_T:
        hits = [x for x in evs if x["pair"] == pair and x["side"] == side
                and x["phase"] == "IN-TRADE" and (rel == "any" or x["latch_rel"] == rel)
                and (cid not in STRICT_T or x["recross_strict"])]
        out[cid] = hits
    for pid, _lab, pair, side in PRE_T:
        out[pid] = [x for x in evs if x["pair"] == pair and x["side"] == side
                    and x["phase"] == "PRE-ENTRY"]
    rel = [x for x in evs if x["pair"] == "12/26" and x["side"] == "with"
           and h["arm_close"] < x["taken_ms"] < h["entry_close"]]
    rel.sort(key=lambda x: (x["taken_ms"], x["close_ms"]))
    out["relay"] = rel[0] if rel else None
    out["open1h"] = h["exit_close"] > h["entry_close"] + H1
    out["reached"] = h["latch"] is not None
    return out


def first_of(hits: list):
    return min(hits, key=lambda x: (x["taken_ms"], x["close_ms"])) if hits else None


def own_relay(sym: str, d: int, lo_close: int, end_close: int) -> dict:
    """THIS file's relay search [L-W.6]: the first with-trend 1h 12/26 cross (own EMA)
    with lo_close < taken < end_close (taken by the own walk law), its visibility
    and its leads to end_close."""
    X, Hh = own4(sym), own1(sym)
    up, dn = Hh["crosses"]["12/26"]
    arr = up if d == 1 else dn
    k0 = int(np.searchsorted(Hh["t"], lo_close, "left"))
    k1 = int(np.searchsorted(Hh["t"], end_close - H1, "left"))
    best = None
    for k in range(k0, k1):
        if not arr[k]:
            continue
        op = int(Hh["t"][k])
        close = op + H1
        J = bar_of(sym, op)
        walk = own_kids(sym, J) is not None
        taken = close if walk else int(X["om"][J]) + H4
        if lo_close < taken < end_close and (best is None or (taken, close) < best[:2]):
            best = (taken, close, walk)
    if best is None:
        return {"relay_cross": False, "relay_close_ms": None, "relay_taken_ms": None,
                "relay_visible_4h_close_ms": None, "relay_on_mismatch_bar": None,
                "relay_lead_1h": None, "relay_lead_4h": None}
    taken, close, walk = best
    vis = int(X["closes"][int(np.searchsorted(X["closes"], close, "left"))])
    return {"relay_cross": True, "relay_close_ms": close, "relay_taken_ms": taken,
            "relay_visible_4h_close_ms": vis, "relay_on_mismatch_bar": not walk,
            "relay_lead_1h": (end_close - taken) // H1, "relay_lead_4h": (end_close - vis) // H4}


# ═══════════════════════════════════════════════════════════════ F-W2-HAND
def _nn(x):
    return None if (x is None or x is pd.NA or (isinstance(x, float) and x != x)) else x


def w1_findings(ev: pd.DataFrame, c: pd.DataFrame, tag: str = "W2-HAND") -> tuple[list, dict]:
    """The module's W1 (events + campaigns) vs THIS file's hand walk, all 200."""
    bad = []
    evk = {}
    for r in ev.itertuples(index=False):
        evk[(r.symbol, int(r.entry_ms), r.pair, int(r.h1_open_ms))] = r
    ck = {(r.symbol, int(r.entry_ms)): r for r in c.itertuples(index=False)}
    n_ev = n_hand = n_strict = 0
    for t in base():
        h = hand_campaign(t)
        hc = hand_classes(h)
        key = (t.symbol, int(t.entry_ms))
        lab = f"{t.symbol} {iso(int(t.entry_ms))}"
        mine = {(x["pair"], x["h1_open_ms"]): x for x in h["events"]}
        theirs = {(k[2], k[3]): v for k, v in evk.items() if k[:2] == key}
        n_hand += len(mine)
        n_ev += len(theirs)
        n_strict += sum(1 for x in mine.values() if x["recross_strict"])
        if set(mine) != set(theirs):
            miss = sorted(set(mine) - set(theirs))[:2]
            extra = sorted(set(theirs) - set(mine))[:2]
            bad.append(f"{tag} {lab}: event set differs — hand-only {miss}, module-only {extra}")
        for k in sorted(set(mine) & set(theirs)):
            x, r = mine[k], theirs[k]
            got = (r.cross, r.side, r.phase, _nn(r.latch_rel), int(r.taken_ms),
                   int(r.visible_4h_close_ms), bool(r.on_mismatch_bar), int(r.close_ms),
                   bool(r.recross_strict))
            want = (x["cross"], x["side"], x["phase"], x["latch_rel"], x["taken_ms"],
                    x["visible_4h_close_ms"], x["on_mismatch_bar"], x["close_ms"],
                    x["recross_strict"])
            if got != want:
                bad.append(f"{tag} {lab} {k[0]} {iso(k[1])}: module {got} != hand {want}")
        r = ck.get(key)
        if r is None:
            bad.append(f"{tag} {lab}: no W1_CAMPAIGNS row")
            continue
        facts = [("exit_close_ms", int(r.exit_close_ms), h["exit_close"]),
                 ("latch_ms", _nn(r.latch_ms), h["latch"]),
                 ("arm_close_ms", int(r.arm_close_ms), h["arm_close"]),
                 ("era", r.era, h["era"]),
                 ("open_1h_after_entry", bool(r.open_1h_after_entry), hc["open1h"]),
                 ("reached_1r", bool(r.reached_1r), hc["reached"])]
        for cid, *_ in COHORTS_T:
            f0 = first_of(hc[cid])
            facts += [(f"{cid}_member", bool(getattr(r, f"{cid}_member")), bool(hc[cid])),
                      (f"{cid}_n_events", int(getattr(r, f"{cid}_n_events")), len(hc[cid])),
                      (f"{cid}_first_taken_ms", _nn(getattr(r, f"{cid}_first_taken_ms")),
                       f0["taken_ms"] if f0 else None),
                      (f"{cid}_first_on_mismatch_bar",
                       _nn(getattr(r, f"{cid}_first_on_mismatch_bar")),
                       f0["on_mismatch_bar"] if f0 else None)]
        for pid, *_ in PRE_T:
            facts += [(f"{pid}_member", bool(getattr(r, f"{pid}_member")), bool(hc[pid])),
                      (f"{pid}_n_events", int(getattr(r, f"{pid}_n_events")), len(hc[pid]))]
        rl = hc["relay"]
        orl = own_relay(t.symbol, h["d"], h["arm_close"], h["entry_close"])
        if (rl is not None) != orl["relay_cross"] or (
                rl is not None and rl["taken_ms"] != orl["relay_taken_ms"]):
            raise RuntimeError(f"{lab}: the hand walk's relay and own_relay disagree — a "
                               f"fixture defect")
        for nm in ("relay_cross", "relay_close_ms", "relay_taken_ms",
                   "relay_visible_4h_close_ms", "relay_on_mismatch_bar", "relay_lead_1h",
                   "relay_lead_4h"):
            facts.append((nm, _nn(getattr(r, nm)), orl[nm]))
        for nm, got, want in facts:
            g = None if got is None else (int(got) if isinstance(got, (np.integer,)) else got)
            if isinstance(g, np.bool_):
                g = bool(g)
            if g != want:
                bad.append(f"{tag} {lab}: {nm} module {g!r} != hand {want!r}")
    return bad, {"campaigns": len(base()), "events_hand": n_hand, "events_module": n_ev,
                 "strict_events": n_strict}


def w2_findings() -> tuple[list, str]:
    """W2 counts / sums re-derived from THIS file's classification (book order)."""
    bad = []
    hs = [(t, hand_campaign(t)) for t in base()]
    hcs = [hand_classes(h) for _, h in hs]
    net = np.array([h["net_r"] for _, h in hs])
    era = np.array([h["era"] for _, h in hs])

    def em(e):
        return np.ones(len(net), bool) if e == "ALL" else era == e

    def cmp(tab, cell, n, nwin, sm, label):
        row = tab[tab["cell"] == cell]
        if len(row) != 1:
            bad.append(f"W2-HAND {label}: cell {cell} absent")
            return
        row = row.iloc[0]
        got = (int(row["n"]), int(row["n_win"]), float(row["sum_net_r"]))
        want = (n, nwin, float(np.round(sm, 6)))
        if got != want:
            bad.append(f"W2-HAND {label} {cell}: module (n, n_win, sum) {got} != hand {want}")

    coh = written("W2_COHORTS")
    for cid, lab, pair, side, rel, ar in COHORTS_T:
        mem = np.array([bool(x[cid]) for x in hcs])
        risk = (np.ones(len(net), bool) if ar == "whole" else
                np.array([x["open1h"] for x in hcs]) if ar == "open1h" else
                np.array([x["reached"] for x in hcs]))
        for e in ERAS_T:
            for g, m in (("cohort", mem), ("at_risk", risk), ("complement", risk & ~mem)):
                mm = m & em(e)
                cmp(coh, f"{cid}_{lab}|{g}|{e}", int(mm.sum()), int((net[mm] > 0).sum()),
                    net[mm].sum(), "W2_COHORTS")
    pre = written("W2_PREENTRY")
    for pid, lab, pair, side in PRE_T:
        mem = np.array([bool(x[pid]) for x in hcs])
        for e in ERAS_T:
            for g, m in (("cohort", mem), ("whole_book", np.ones(len(net), bool)),
                         ("complement", ~mem)):
                mm = m & em(e)
                cmp(pre, f"{pid}_{lab}|{g}|{e}", int(mm.sum()), int((net[mm] > 0).sum()),
                    net[mm].sum(), "W2_PREENTRY")
    return bad, (f"{len(DECLARED['W2_COHORTS'])} cohort + {len(DECLARED['W2_PREENTRY'])} "
                 f"pre-entry cells re-derived")


# ── the relay distribution, re-derived from THIS file's leads [L-W.6, w7] ──
def own_pct(xs, q: float) -> float:
    """THE TYPED PERCENTILE: linear interpolation between order statistics at
    position (n − 1) · q / 100 — this file's loop."""
    v = sorted(float(x) for x in xs)
    pos = (len(v) - 1) * (float(q) / 100.0)
    i = int(np.floor(pos))
    j = min(i + 1, len(v) - 1)
    return v[i] + (v[j] - v[i]) * (pos - i)


def own_lead_stats(xs: list, pre: str) -> dict:
    if not xs:
        return {f"{pre}_{s}": float("nan") for s in LEAD_STATS_T}
    return {f"{pre}_min": float(min(xs)), f"{pre}_q25": own_pct(xs, 25),
            f"{pre}_median": own_pct(xs, 50), f"{pre}_q75": own_pct(xs, 75),
            f"{pre}_max": float(max(xs)), f"{pre}_mean": float(sum(xs)) / len(xs)}


def lag_band_t(v: int) -> str:
    return "0" if v == 0 else "1-6" if v <= 6 else "7-15" if v <= 15 else ">=16"


def bin_t(v: int, bins) -> str:
    for name, a, b in bins:
        if v >= a and (b is None or v <= b):
            return name
    raise RuntimeError(f"a lead {v} in no typed bin — a fixture defect")


def own_v6_windows() -> list:
    """Per v6 campaign (book order): era, lag and this file's relay facts."""
    if "v6win" not in _C:
        out = []
        for t in base():
            h = hand_campaign(t)
            out.append({"symbol": t.symbol, "key": (t.symbol, int(t.entry_ms)), "era": h["era"],
                        "lag": h["lag"],
                        **own_relay(t.symbol, h["d"], h["arm_close"], h["entry_close"])})
        _C["v6win"] = out
    return _C["v6win"]


def own_twin() -> tuple[list, dict]:
    """THE TWIN POPULATION hand-walked (w7): every armed window of v6's card (the
    lineage's armings over replay9's bounds) passing the TYPED gates (tide_ok and
    d_ok) whose trigger key is not a v6 campaign (books/v6_campaigns.parquet);
    the window end by THIS file's law — the trigger close if it triggered, else
    the window close (the counter 12/89 4h cross) if that bar is <= the as-of bar,
    else the as-of close; the relay by own_relay."""
    if "twin" in _C:
        return _C["twin"]
    v6c = pd.read_parquet(str(B.OUT / "v6_campaigns.parquet"))
    v6k = {(str(s), int(e)) for s, e in zip(v6c["symbol"], v6c["entry_ms"])}
    lo, hi, _ = B.corridor()
    rows, trig_keys, bad = [], set(), []
    for s in CLASSIC5_TYPED:
        X = own4(s)
        lo_i, hi_i, _n = B.ride_bounds(s, S.ROLES, lo, hi)
        if int(X["om"][hi_i]) + H4 != PIN:
            bad.append(f"W2-HAND-TWIN {s}: the ride's last bar closes {iso(int(X['om'][hi_i]) + H4)}"
                       f", not the typed pin")
        arms_, cands = T9.card_candidates9(s, S.ROLES, lo_i, hi_i)
        trig = {(int(a.arm_i), int(a.direction)): int(ti) for ti, _d, a in cands}
        for a in arms_:
            if not (bool(a.tide_ok) and bool(a.d_ok)):
                continue
            d, ai = int(a.direction), int(a.arm_i)
            arm_close = int(X["om"][ai]) + H4
            if (ai, d) in trig:
                tk = (s, int(X["om"][trig[(ai, d)]]))
                trig_keys.add(tk)
                if tk in v6k:
                    continue
                end, kind = tk[1] + H4, "trigger_not_entered"
            elif int(a.window_end_i) <= hi_i:
                end, kind = int(X["om"][int(a.window_end_i)]) + H4, "window_close"
            else:
                end, kind = int(X["om"][hi_i]) + H4, "as_of"
            rows.append({"symbol": s, "arm_ms": int(X["om"][ai]), "direction": d,
                         "arm_close_ms": arm_close, "end_close_ms": end, "end_kind": kind,
                         "window_bars": (end - arm_close) // H4,
                         "era": "tuning" if end <= ERA_CUT else "holdout",
                         **own_relay(s, d, arm_close, end)})
    chk = {"triggered_gate_passing": len(trig_keys), "v6": len(v6k),
           "triggered_equals_v6": trig_keys == v6k, "bad": bad}
    _C["twin"] = (rows, chk)
    return _C["twin"]


TWIN_COLS_T = ("arm_close_ms", "end_close_ms", "end_kind", "window_bars", "era", "relay_cross",
               "relay_close_ms", "relay_taken_ms", "relay_visible_4h_close_ms",
               "relay_on_mismatch_bar", "relay_lead_1h", "relay_lead_4h")


def twin_findings(tw: pd.DataFrame, tag: str = "W2-HAND-TWIN") -> tuple[list, dict]:
    rows, chk = own_twin()
    bad = list(chk["bad"])
    mine = {(r["symbol"], r["arm_ms"], r["direction"]): r for r in rows}
    theirs = {(str(r.symbol), int(r.arm_ms), int(r.direction)): r
              for r in tw.itertuples(index=False)}
    if set(mine) != set(theirs):
        bad.append(f"{tag}: window set differs — hand-only {sorted(set(mine) - set(theirs))[:2]}, "
                   f"module-only {sorted(set(theirs) - set(mine))[:2]} ({len(mine)} vs "
                   f"{len(theirs)})")
    for k in sorted(set(mine) & set(theirs)):
        x, r = mine[k], theirs[k]
        for col in TWIN_COLS_T:
            g = _nn(getattr(r, col))
            g = bool(g) if isinstance(g, (bool, np.bool_)) else (
                int(g) if isinstance(g, (int, np.integer)) else g)
            if g != x[col]:
                bad.append(f"{tag} {k[0]} {iso(k[1])} d{k[2]:+d}: {col} module {g!r} != hand "
                           f"{x[col]!r}")
    man = json.loads((OUT / "MANIFEST_STAGE_W.json").read_text(encoding="utf-8"))
    tc = man["disclosures"]["relay_twin_check"]
    if bool(tc["triggered_equals_v6_set"]) != bool(chk["triggered_equals_v6"]):
        bad.append(f"{tag}: the manifest's triggered_equals_v6_set {tc['triggered_equals_v6_set']}"
                   f" != this file's {chk['triggered_equals_v6']}")
    kinds = {}
    for r in rows:
        kinds[r["end_kind"]] = kinds.get(r["end_kind"], 0) + 1
    return bad, {"n": len(rows), "kinds": dict(sorted(kinds.items())),
                 "relay": sum(1 for r in rows if r["relay_cross"]), **chk}


def _eq6(a, b) -> bool:
    fa, fb = float(a), float(b)
    if not np.isfinite(fa) or not np.isfinite(fb):
        return (not np.isfinite(fa)) and (not np.isfinite(fb))
    return float(np.round(fa, 6)) == float(np.round(fb, 6))


def relay_findings(rs: pd.DataFrame, rh: pd.DataFrame, tag: str = "W2-HAND-RELAY") -> list:
    """Every W2_RELAY_SUMMARY cell (both populations) and every W2_RELAY_HIST bin
    re-derived from THIS file's relay facts (own_v6_windows, own_twin)."""
    bad = []
    pops = {"v6_campaigns": own_v6_windows(), "armed_windows_not_entered": own_twin()[0]}
    for pop, ws in pops.items():
        lags = LAGS_T if pop == "v6_campaigns" else ("ALL",)
        for e in ERAS_T:
            for band in lags:
                sub = [w for w in ws if (e == "ALL" or w["era"] == e)
                       and (band == "ALL" or lag_band_t(w["lag"]) == band)]
                has = [w for w in sub if w["relay_cross"]]
                want = {"n_windows": len(sub),
                        "n_lag0": (sum(1 for w in sub if w["lag"] == 0)
                                   if pop == "v6_campaigns" else 0),
                        "n_relay_cross": len(has),
                        "share_relay_cross": (len(has) / len(sub)) if sub else float("nan"),
                        **own_lead_stats([w["relay_lead_1h"] for w in has], "lead_1h"),
                        **own_lead_stats([w["relay_lead_4h"] for w in has], "lead_4h")}
                cell = f"{pop}|{e}|{band}"
                row = rs[rs["cell"] == cell]
                if len(row) != 1:
                    bad.append(f"{tag}: cell {cell} absent")
                    continue
                row = row.iloc[0]
                for col, v in want.items():
                    ok = (int(row[col]) == v) if col.startswith("n_") else _eq6(row[col], v)
                    if not ok:
                        bad.append(f"{tag} {cell}: {col} module {float(row[col])!r} != this "
                                   f"file's {v!r}")
        has = [w for w in ws if w["relay_cross"]]
        for metric, bins in (("lead_1h", L1_BINS_T), ("lead_4h", L4_BINS_T)):
            cnt = {b[0]: 0 for b in bins}
            for w in has:
                cnt[bin_t(int(w[f"relay_{metric}"]), bins)] += 1
            cnt["none"] = len(ws) - len(has)
            for name, v in cnt.items():
                row = rh[rh["cell"] == f"{pop}|{metric}|{name}"]
                if len(row) != 1 or int(row.iloc[0]["n"]) != v:
                    bad.append(f"{tag} HIST {pop}|{metric}|{name}: module "
                               f"{None if len(row) != 1 else int(row.iloc[0]['n'])} != this "
                               f"file's {v}")
    return bad


# ── (w1) planted mismatch bars, one at a time, under the module's re-ride ──
def plant_cases() -> list:
    """(kind, t, J): a planted mismatch bar J for EVERY C1 campaign's first C1 event
    (its bar), EVERY campaign whose 1h latch child's bar holds a W1 event of the
    campaign, and EVERY 1h-resolved stop exit whose exit bar holds one — each (t, J)
    once, walkable bars only (planting a bar that is already a mismatch bar is no
    plant)."""
    if "cases" in _C:
        return _C["cases"]
    out, seen = [], set()
    for t in base():
        h = hand_campaign(t)
        s = t.symbol
        bars_ev = {x["J"] for x in h["events"]}
        c1 = first_of([x for x in h["events"] if x["pair"] == "12/89" and x["side"] == "counter"
                       and x["phase"] == "IN-TRADE" and x["latch_rel"] == "before"])
        cands = []
        if c1 is not None:
            cands.append(("C1-first", c1["J"]))
        if h["latch"] is not None and h["latch_by"] == "1h":
            jl = bar_of(s, h["latch"] - H1)
            if jl in bars_ev:
                cands.append(("latch-bar", jl))
        if h["exit_by"] == "1h" and int(t.exit_i) in bars_ev:
            cands.append(("stop-exit-bar", int(t.exit_i)))
        for kind, J in cands:
            k = (s, int(t.entry_ms), int(J))
            if k in seen or own_kids(s, J) is None:
                continue
            seen.add(k)
            out.append((kind, t, int(J)))
    _C["cases"] = out
    return out


def _arrays_memo(real):
    """The 1h cross arrays do not depend on the walk: memoised for the plants (the
    plants judge the walk-dependent TAKING law, never the crosses)."""
    store = _C.setdefault("arrmemo", {})

    def f(h1):
        k = id(h1)
        if k not in store:
            store[k] = (h1, real(h1))
        return store[k][1]
    return f


def module_under_plant(t, J: int, transform=None):
    """The module on campaign t with bar J PLANTED as a mismatch bar: the walk
    (RD.walk_of) planted, the campaign re-ridden by the foundation ride on that
    walk (latch / exit decided by the parent on J), the module's event tape rebuilt
    (memo cleared) and classified.  `transform` post-edits the asset tape (the
    sabotage seam)."""
    sym = t.symbol
    real_walk_of = RD.walk_of
    W0 = real_walk_of(sym)
    ok2 = W0.ok.copy()
    ok2[J] = False
    why2 = dict(W0.why)
    why2[J] = "PLANTED mismatch (fixture)"
    Wp = RD.Walk(W0.sym, W0.h1, W0.open4, W0.a, W0.n, ok2, why2)
    real_asset_events = S.asset_events
    lo, hi, _ = B.corridor()

    def planted_walk_of(s_, h1=None):
        return Wp if (s_ == sym and h1 is None) else real_walk_of(s_, h1)

    def events_of(s_):
        ev = real_asset_events(s_)
        return transform(ev) if transform is not None else ev

    try:
        S.clear_memo(events=True)
        with mutated(RD, "walk_of", planted_walk_of), mutated(S, "asset_events", events_of), \
                mutated(S, "event_arrays", _arrays_memo(S.event_arrays)):
            wp = RD.transform_book([t], S.CARD, S.ROLES, lo, hi, walk=lambda s_: Wp)[0]
            ci = S.campaign_info(t, wp)
            rows = S.classify_campaign(ci, S.asset_events(sym), own4(sym)["closes"])
    finally:
        S.clear_memo(events=True)
    return wp, ci, rows


def plant_findings(transform=None, tag: str = "W2-HAND-MISMATCH") -> tuple[list, dict]:
    """(w1) + L-W.3 under a planted mismatch bar, EVERY case of plant_cases, one at
    a time: the re-ride is v6 and counts the bar; its exit / latch are the law's
    (the parent decides on J); every event of the campaign equals THIS file's hand
    walk under the same plant (taken at J's close on J, flagged; phase and latch
    relation by the law at that instant)."""
    bad, by_kind, n_on, n_moved = [], {}, 0, 0
    for kind, t, J in plant_cases():
        by_kind[kind] = by_kind.get(kind, 0) + 1
        h0 = hand_campaign(t)
        h = hand_campaign(t, frozenset({J}))
        wp, ci, rows = module_under_plant(t, J, transform)
        lab = f"{tag} [{kind}] {t.symbol} {iso(int(t.entry_ms))} bar {iso(int(X_om(t.symbol)[J]))}"
        if (float(wp.net_r), int(wp.exit_ms), str(wp.exit_reason)) != (
                float(t.net_r), int(t.exit_ms), str(t.exit_reason)):
            bad.append(f"{lab}: the planted re-ride is not v6 (net {wp.net_r!r} vs {t.net_r!r})")
        if int(X_om(t.symbol)[J]) not in [int(x) for x in wp.walk_mismatch_ms]:
            bad.append(f"{lab}: the planted bar is not counted in the ride's mismatch column")
        if (int(ci["exit_close_ms"]), ci["latch_ms"]) != (h["exit_close"], h["latch"]):
            bad.append(f"{lab}: exit / latch module ({ci['exit_close_ms']}, {ci['latch_ms']}) != "
                       f"the law under the plant ({h['exit_close']}, {h['latch']})")
        mine = {(x["pair"], x["h1_open_ms"]): x for x in h["events"]}
        mod = {(r["pair"], r["h1_open_ms"]): r for r in rows}
        if set(mine) != set(mod):
            bad.append(f"{lab}: the event set differs under the plant")
        base_ev = {(x["pair"], x["h1_open_ms"]): x for x in h0["events"]}
        for k in sorted(set(mine) & set(mod)):
            x, r = mine[k], mod[k]
            n_on += int(x["on_mismatch_bar"])
            b0 = base_ev.get(k)
            if b0 is not None and (b0["taken_ms"], b0["phase"], b0["latch_rel"]) != (
                    x["taken_ms"], x["phase"], x["latch_rel"]):
                n_moved += 1
            got = (int(r["taken_ms"]), bool(r["on_mismatch_bar"]), int(r["visible_4h_close_ms"]),
                   r["phase"], r["latch_rel"])
            want = (x["taken_ms"], x["on_mismatch_bar"], x["visible_4h_close_ms"], x["phase"],
                    x["latch_rel"])
            if got != want:
                bad.append(f"{lab} {k[0]} {iso(k[1])}: module {got} != the law {want}")
    return bad, {"cases": len(plant_cases()), "by_kind": dict(sorted(by_kind.items())),
                 "events_on_planted_bars": n_on, "events_whose_class_the_plant_moves": n_moved}


def X_om(sym: str) -> np.ndarray:
    return own4(sym)["om"]


def hand_break():
    def run(obj, name, value):
        def thunk():
            with mutated(obj, name, value):
                ev, c, _ = module_w1()
            return w1_findings(ev, c)[0]
        return thunk

    real_phase, real_side = S.phase_of, S.side_of

    def phase_admits_pre(taken, arm_close, entry_close, exit_close):
        ph = real_phase(taken, arm_close, entry_close, exit_close)
        return "IN-TRADE" if ph == "PRE-ENTRY" else ph

    def side_flipped_shorts(cross, d):
        sd = real_side(cross, d)
        return sd if int(d) == 1 else ("counter" if sd == "with" else "with")

    def median45():
        real = S._lead_stats

        def bent(x, pre):
            out = real(x, pre)
            if len(x):
                out[f"{pre}_median"] = float(np.percentile(x, 45))
            return out
        pops = {"v6_campaigns": written("W2_RELAY_WINDOWS"),
                "armed_windows_not_entered": written("W2_RELAY_WINDOWS_TWIN")}
        with mutated(S, "_lead_stats", bent):
            rs = S.relay_summary(pops)
        return relay_findings(rs, written("W2_RELAY_HIST"))

    def twin_end_late():
        real = B.known_window_end

        def late(end_i, hi_i):
            return int(end_i) + 1 if int(end_i) + 1 <= int(hi_i) else real(end_i, hi_i)
        v6k = {(t.symbol, int(t.entry_ms)) for t in base()}
        with mutated(B, "known_window_end", late):
            tw, _ = S.relay_twin_windows(v6k)
        return twin_findings(tw)[0]

    return plants([
        ("pre-entry crosses admitted as IN-TRADE", "W2-HAND",
         run(S, "phase_of", phase_admits_pre)),
        ("with/against flipped for shorts", "W2-HAND", run(S, "side_of", side_flipped_shorts)),
        ("the +1R latch ignored (every in-trade cross 'before')", "W2-HAND",
         run(S, "latch_instant", lambda w: None)),
        ("the strict re-cross flag ignored (every with-trend 9/12 cross strict)", "W2-HAND",
         run(S, "recross_strict", lambda pair, side, *_a: pair == "9/12" and side == "with")),
        ("the raw 1h close kept as the taken instant on EVERY planted mismatch bar",
         "W2-HAND-MISMATCH",
         lambda: plant_findings(lambda ev: ev.assign(taken_ms=ev["close_ms"]))[0]),
        ("the relay lead median read at the 45th percentile (in-process summary)",
         "W2-HAND-RELAY", median45),
        ("the twin's known window end one 4h bar late (in-process twin)", "W2-HAND-TWIN",
         twin_end_late),
    ])


def hand_real():
    ev, c = written("W1_EVENTS"), written("W1_CAMPAIGNS")
    bad, st = w1_findings(ev, c)
    b2, line2 = w2_findings()
    bad += b2
    bad += relay_findings(written("W2_RELAY_SUMMARY"), written("W2_RELAY_HIST"))
    b4, tst = twin_findings(written("W2_RELAY_WINDOWS_TWIN"))
    bad += b4
    b3, pst = plant_findings()
    bad += b3
    n_mis = sum(1 for t in base() for x in hand_campaign(t)["events"] if x["on_mismatch_bar"])
    ph, by = {}, {}
    for t in base():
        for x in hand_campaign(t)["events"]:
            ph[x["phase"]] = ph.get(x["phase"], 0) + 1
        b_ = hand_campaign(t)["exit_by"]
        by[b_] = by.get(b_, 0) + 1
    v6w = own_v6_windows()
    return verdict(bad, (
        f"ALL {st['campaigns']} v6 campaigns hand-walked from the raw 1h bars (own EMA "
        f"9/12, 12/26, 12/89; own walk law; own stop-in-force from the trail advances): "
        f"{st['events_hand']} events == the module's {st['events_module']} W1 rows on (cross, "
        f"side, phase, latch relation, taken, visible 4h close, mismatch flag, close, strict "
        f"re-cross flag — {st['strict_events']} strict); exits by {dict(sorted(by.items()))}; "
        f"phases {dict(sorted(ph.items()))}; events on mismatch bars {n_mis}; every "
        f"W1_CAMPAIGNS exit / latch / membership / count / first-event / relay fact equal; "
        f"{line2} equal; relay: {sum(1 for w in v6w if w['relay_cross'])}/{len(v6w)} v6 "
        f"windows, every W2_RELAY_SUMMARY cell (n, lag-0, relay n, share, 6 lead statistics "
        f"x 2 lenses, this file's percentile) and W2_RELAY_HIST bin equal; twin hand-walked: "
        f"{tst['n']} armed windows with no v6 campaign by end kind {tst['kinds']}, "
        f"{tst['relay']} with a relay cross, every row equal (triggered gate-passing windows "
        f"{tst['triggered_gate_passing']} == v6 {tst['v6']}: {tst['triggered_equals_v6']}); "
        f"(w1) {pst['cases']} PLANTED mismatch bars one at a time {pst['by_kind']}: every "
        f"re-ride v6 and counting its bar, exit / latch by the parent's law, "
        f"{pst['events_on_planted_bars']} events on the planted bars taken at the parent "
        f"close, {pst['events_whose_class_the_plant_moves']} classifications moved by the "
        f"plants, all by the law"))


# ═══════════════════════════════════════════════════════════════ F-W1-OTHER
def _law_haircut(sym: str, net_r: float, fee_r: float) -> float:
    return float(net_r) - float(fee_r) * (SLIP_T[sym] / TAKER_T)


def other_src() -> dict:
    """THE SHARED INPUTS of the other books (stated, not hidden) — per campaign the
    book's own entry, R, window open (w13, TYPED here), exit bar, exit price and exit
    reason: the 9/12 book from the foundation Trades (B.trg912_book; fixture-GREEN in
    the books suite; its stop exits cross-checked against the stop in force from its
    own trail advances), P-BRK-4H and P-RELAY-1 from their scored regbook parquets,
    read HERE.  The hand walk resolves WHEN on the raw 1h bars; the WHAT (the exit
    bar, the price at a stop) is the book's."""
    if "osrc" in _C:
        return _C["osrc"]
    lo, hi, _ = B.corridor()
    out = {bk: [] for bk in OTHER_BOOKS_T}
    for t in B.trg912_book(lo, hi):
        if t.exit_reason == "stop" and float(t.exit_px) != stop_at(t, int(t.exit_i)):
            raise RuntimeError(f"9/12 {t.symbol} {iso(int(t.entry_ms))}: exit px is not the stop "
                               f"in force — a fixture defect")
        out["trg912"].append({
            "symbol": t.symbol, "d": int(t.direction), "entry_ms": int(t.entry_ms),
            "entry_px": float(t.entry_px), "R": float(t.r_dist),
            "arm_close": int(t.arm_ms) + H4, "entry_close": int(t.entry_ms) + H4,
            "exit_ms": int(t.exit_ms), "exit_px": float(t.exit_px),
            "exit_reason": str(t.exit_reason), "net_r": float(t.net_r), "fee_r": float(t.fee_r),
            "haircut": _law_haircut(t.symbol, t.net_r, t.fee_r), "reached_book": bool(t.reached_1r),
            "record_exit": None, "record_latch": None})
    for bk, arm_col in (("P-BRK-4H", "die_close_ms"), ("P-RELAY-1", "window_arm_close_ms")):
        d = pd.read_parquet(str(E.OUT / "regbooks" / bk / "scored.parquet"))
        for r in d.itertuples(index=False):
            out[bk].append({
                "symbol": str(r.symbol), "d": int(r.direction), "entry_ms": int(r.entry_ms),
                "entry_px": float(r.entry_px), "R": float(r.r_dist),
                "arm_close": int(getattr(r, arm_col)), "entry_close": int(r.entry_close_ms),
                "exit_ms": int(r.exit_ms), "exit_px": float(r.exit_px),
                "exit_reason": str(r.exit_reason), "net_r": float(r.net_r),
                "fee_r": float(r.fee_r), "haircut": float(r.haircut_net_r),
                "reached_book": bool(r.reached_1r),
                "record_exit": int(r.exit_close_ms) if bk == "P-RELAY-1" else None,
                "record_latch": (None if bk != "P-RELAY-1" or pd.isna(r.latch_1h_ms)
                                 else int(r.latch_1h_ms))})
    _C["osrc"] = out
    return out


def hand_other(src: dict) -> dict:
    """THE HAND WALK of one campaign of an other book from the raw bars [L-W.0..L-W.3,
    w1, w2, w10, w13, w14]: the bars after the entry close (a relay: its entry bar's
    children after its 1h entry close, then the next bars), per walkable bar its four
    children in tape order — the +1R child (L-W.3: the literal first child reaching
    entry ± R, the stop child included), the L-W.5 latch (a child that stops does not
    latch), and on the book's exit bar, for a stop exit, the FIRST child touching the
    book's exit price (the stop in force); on a mismatch bar (own walk law) the parent
    decides.  A walkable stop-exit bar where no child touches is NOT resolvable on 1h
    (L-W.3's HALT): the law then demands the labelled 4h-close fallback."""
    k0 = ("hando",) + tuple(sorted(src.items()))   # the whole input: two books can share
    #                                                  (symbol, entry close, window open)
    if k0 in _C:
        return _C[k0]
    s, d, e, R = src["symbol"], src["d"], src["entry_px"], src["R"]
    X, Hh = own4(s), own1(s)
    om = X["om"]
    ec = src["entry_close"]
    xi = int(np.searchsorted(om, src["exit_ms"], "left"))
    if int(om[xi]) != src["exit_ms"]:
        raise RuntimeError(f"{s}: exit bar {iso(src['exit_ms'])} not on the own 4h frame")
    J = int(np.searchsorted(om, ec, "left")) - 1
    if not int(om[J]) < ec <= int(om[J]) + H4:
        raise RuntimeError(f"{s}: entry close {iso(ec)} in no own 4h bar")
    start = J + 1 if ec == int(om[J]) + H4 else J
    if start == J and own_kids(s, J) is None:
        raise RuntimeError(f"{s}: a 1h entry inside a mismatch bar — a fixture defect")
    exit_close, by, latch, lby, lw5 = None, None, None, None, None
    resolvable = True
    stop_px = src["exit_px"]
    for j in range(start, xi + 1):
        close_j = int(om[j]) + H4
        stop_bar = (j == xi and src["exit_reason"] == "stop")
        ks = own_kids(s, j)
        if ks is not None:
            for k in [k for k in ks if int(Hh["t"][k]) + H1 > ec]:
                hi_, lo_ = float(Hh["h"][k]), float(Hh["l"][k])
                fav = hi_ if d == 1 else lo_
                reach = (fav - e) * d / R >= 1.0
                stops = stop_bar and ((d == 1 and lo_ <= stop_px) or (d == -1 and hi_ >= stop_px))
                if latch is None and reach:
                    latch, lby = int(Hh["t"][k]) + H1, "1h"
                if lw5 is None and reach and not stops:
                    lw5 = int(Hh["t"][k]) + H1
                if stops:
                    exit_close, by = int(Hh["t"][k]) + H1, "1h"
                    break
            if stop_bar and exit_close is None:
                resolvable = False
        else:
            fav = float(X["h"][j]) if d == 1 else float(X["l"][j])
            if (fav - e) * d / R >= 1.0:
                if latch is None:
                    latch, lby = close_j, "parent"
                if lw5 is None:
                    lw5 = close_j
            if stop_bar:
                exit_close, by = close_j, "parent"
    exit_bar_close = int(om[xi]) + H4
    if exit_close is None:
        exit_close, by = exit_bar_close, "close"
    evs = []
    k_lo = int(np.searchsorted(Hh["t"], src["arm_close"] - H4, "left"))
    k_hi = int(np.searchsorted(Hh["t"], exit_bar_close, "left"))
    for p in PAIRS_TYPED:
        up, dn = Hh["crosses"][p]
        for cross, arr in (("up", up), ("dn", dn)):
            for k in (k_lo + np.flatnonzero(arr[k_lo:k_hi])).tolist():
                op = int(Hh["t"][k])
                close = op + H1
                Jk = bar_of(s, op)
                walk = own_kids(s, Jk) is not None
                taken = close if walk else int(om[Jk]) + H4
                if not (src["arm_close"] < taken <= exit_bar_close):
                    continue
                ph = ("PRE-ENTRY" if taken <= ec else "IN-TRADE" if taken < exit_close
                      else "AT-EXIT" if taken == exit_close else "POST-EXIT")
                side = side_t(cross, d)
                rel = None
                if ph == "IN-TRADE":
                    rel = "before" if (latch is None or taken < latch) else "after"
                vis = int(X["closes"][int(np.searchsorted(X["closes"], close, "left"))])
                pc, pcl = Hh["prev"][p].get(k, (None, None))
                strict = bool(p == "9/12" and side == "with" and pc is not None
                              and side_t(pc, d) == "counter" and int(pcl) > ec)
                evs.append({"pair": p, "cross": cross, "h1_open_ms": op, "close_ms": close,
                            "taken_ms": taken, "on_mismatch_bar": not walk, "phase": ph,
                            "side": side, "latch_rel": rel, "visible_4h_close_ms": vis,
                            "recross_strict": strict, "k": k, "J": Jk})
    out = {"arm_close": src["arm_close"], "entry_close": ec, "exit_close": exit_close,
           "exit_by": by, "exit_bar_close": exit_bar_close, "latch": latch, "latch_by": lby,
           "latch_w5": lw5, "resolvable": resolvable, "events": evs,
           "era": "tuning" if ec <= ERA_CUT else "holdout", "d": d}
    _C[k0] = out
    return out


def own_fallback(src: dict) -> dict:
    """The TYPED fallback law (w14): the exit at the 4h exit-bar close; the latch at
    the close of the first 4h bar after the entry bar whose favourable extreme
    reaches entry ± R (through the exit bar)."""
    X = own4(src["symbol"])
    om = X["om"]
    xi = int(np.searchsorted(om, src["exit_ms"], "left"))
    ti = int(np.searchsorted(om, src["entry_close"] - H4, "left"))
    lat = None
    for j in range(ti + 1, xi + 1):
        fav = float(X["h"][j]) if src["d"] == 1 else float(X["l"][j])
        if (fav - src["entry_px"]) * src["d"] / src["R"] >= 1.0:
            lat = int(om[j]) + H4
            break
    return {"exit_close": int(om[xi]) + H4, "latch": lat}


def other_findings(ev: pd.DataFrame, c: pd.DataFrame, sm: pd.DataFrame | None,
                   tag: str = "W1-OTHER") -> tuple[list, dict]:
    """The module's W1 on the other books (events, campaigns, summary) vs THIS file's
    hand walk of EVERY campaign of every book (>= MIN_HAND_T per book, the typed n)."""
    bad = []
    src = other_src()
    evg = {}
    for r in ev.itertuples(index=False):
        evg.setdefault((r.book, r.symbol, int(r.entry_close_ms)), {})[
            (r.pair, int(r.h1_open_ms))] = r
        cl = own4(r.symbol)["closes"]
        i = int(np.searchsorted(cl, int(r.close_ms), "left"))
        if int(r.visible_4h_close_ms) != int(cl[i]):
            bad.append(f"{tag}-VIS {r.book} {r.symbol} {r.pair} 1h close {iso(int(r.close_ms))}: "
                       f"visible at {iso(int(r.visible_4h_close_ms))}, the law (the first 4h "
                       f"close >= the 1h close) says {iso(int(cl[i]))}")
    ck = {(r.book, r.symbol, int(r.entry_close_ms)): r for r in c.itertuples(index=False)}
    st = {"n": {}, "events": {}, "by": {}, "fallback": {}, "record_checked": 0}
    hand_rows = []
    for bk in OTHER_BOOKS_T:
        rows = src[bk]
        n_c = int((c["book"] == bk).sum())
        if len(rows) != N_OTHER_T[bk] or n_c != N_OTHER_T[bk] or n_c < MIN_HAND_T:
            bad.append(f"{tag}-N {bk}: source n {len(rows)}, module rows {n_c}, typed n "
                       f"{N_OTHER_T[bk]} (at least {MIN_HAND_T} hand-walked per book)")
        st["n"][bk], st["events"][bk], st["by"][bk], st["fallback"][bk] = len(rows), 0, {}, 0
        for x in rows:
            h = hand_other(x)
            hc = hand_classes(h)
            key = (bk, x["symbol"], x["entry_close"])
            lab = f"{tag}-HAND {bk} {x['symbol']} {iso(x['entry_close'])}"
            hand_rows.append((bk, h, hc))       # the summary's referee: every source campaign
            r = ck.get(key)
            mine = {(y["pair"], y["h1_open_ms"]): y for y in h["events"]}
            theirs = evg.get(key, {})
            st["events"][bk] += len(mine)
            if r is None:
                bad.append(f"{lab}: no W1_CAMPAIGNS_OTHER row (the campaign set differs)")
                continue
            fb = str(r.resolution) == "4h-close-fallback"
            if fb:
                st["fallback"][bk] += 1
                own = own_fallback(x)
                if (int(r.exit_close_ms), _nn(r.latch_ms), str(r.exit_resolved_by)) != (
                        own["exit_close"], own["latch"], "4h-close-fallback") \
                        or not str(r.fallback_reason):
                    bad.append(f"{tag}-FALLBACK {bk} {x['symbol']} {iso(x['entry_close'])}: a "
                               f"fallback row off the typed law (exit {_nn(r.exit_close_ms)} vs "
                               f"{own['exit_close']}, latch {_nn(r.latch_ms)} vs {own['latch']}, "
                               f"reason {str(r.fallback_reason)[:40]!r})")
                if str(r.fallback_reason).startswith("walk-halt") and h["resolvable"]:
                    bad.append(f"{tag}-FALLBACK {bk} {x['symbol']} {iso(x['entry_close'])}: "
                               f"'walk-halt' claimed, but the raw 1h bars resolve the exit at "
                               f"{iso(h['exit_close'])}")
            else:
                if not h["resolvable"]:
                    bad.append(f"{tag}-FALLBACK {bk} {x['symbol']} {iso(x['entry_close'])}: no "
                               f"1h child touches the stop on the walkable exit bar, yet the "
                               f"row is resolved {r.resolution!r} (a silent resolution)")
                st["by"][bk][h["exit_by"]] = st["by"][bk].get(h["exit_by"], 0) + 1
            if x["record_exit"] is not None:
                st["record_checked"] += 1
                if (h["exit_close"], h["latch_w5"]) != (x["record_exit"], x["record_latch"]):
                    bad.append(f"{lab}: the hand walk's exit / L-W.5 latch ({h['exit_close']}, "
                               f"{h['latch_w5']}) != the regbook of record's "
                               f"({x['record_exit']}, {x['record_latch']})")
            if set(mine) != set(theirs):
                bad.append(f"{lab}: event set differs — hand-only "
                           f"{sorted(set(mine) - set(theirs))[:2]}, module-only "
                           f"{sorted(set(theirs) - set(mine))[:2]}")
            if not fb:
                for k in sorted(set(mine) & set(theirs)):
                    y, q = mine[k], theirs[k]
                    got = (q.cross, q.side, q.phase, _nn(q.latch_rel), int(q.taken_ms),
                           int(q.visible_4h_close_ms), bool(q.on_mismatch_bar), int(q.close_ms),
                           bool(q.recross_strict), q.era)
                    want = (y["cross"], y["side"], y["phase"], y["latch_rel"], y["taken_ms"],
                            y["visible_4h_close_ms"], y["on_mismatch_bar"], y["close_ms"],
                            y["recross_strict"], h["era"])
                    if got != want:
                        bad.append(f"{lab} {k[0]} {iso(k[1])}: module {got} != hand {want}")
            facts = [("arm_close_ms", int(r.arm_close_ms), h["arm_close"]),
                     ("entry_ms", int(r.entry_ms), x["entry_ms"]),
                     ("direction", int(r.direction), x["d"]),
                     ("exit_bar_close_ms", int(r.exit_bar_close_ms), h["exit_bar_close"]),
                     ("era", r.era, h["era"]),
                     ("reached_1r_book", bool(r.reached_1r_book), x["reached_book"]),
                     ("n_events_w1", int(r.n_events_w1), len(h["events"]))]
            if not fb:
                facts += [("exit_close_ms", int(r.exit_close_ms), h["exit_close"]),
                          ("exit_resolved_by", str(r.exit_resolved_by), h["exit_by"]),
                          ("latch_ms", _nn(r.latch_ms), h["latch"]),
                          ("latch_w5_ms", _nn(r.latch_w5_ms), h["latch_w5"]),
                          ("reached_1r", bool(r.reached_1r), hc["reached"]),
                          ("open_1h_after_entry", bool(r.open_1h_after_entry), hc["open1h"])]
                for cid, *_ in COHORTS_T:
                    f0 = first_of(hc[cid])
                    facts += [(f"{cid}_member", bool(getattr(r, f"{cid}_member")), bool(hc[cid])),
                              (f"{cid}_n_events", int(getattr(r, f"{cid}_n_events")),
                               len(hc[cid])),
                              (f"{cid}_first_taken_ms", _nn(getattr(r, f"{cid}_first_taken_ms")),
                               f0["taken_ms"] if f0 else None),
                              (f"{cid}_first_on_mismatch_bar",
                               _nn(getattr(r, f"{cid}_first_on_mismatch_bar")),
                               f0["on_mismatch_bar"] if f0 else None)]
                for pid, *_ in PRE_T:
                    facts += [(f"{pid}_member", bool(getattr(r, f"{pid}_member")), bool(hc[pid])),
                              (f"{pid}_n_events", int(getattr(r, f"{pid}_n_events")),
                               len(hc[pid]))]
            for nm, got, want in facts:
                g = None if got is None else (int(got) if isinstance(got, np.integer) else got)
                if isinstance(g, np.bool_):
                    g = bool(g)
                if g != want:
                    bad.append(f"{lab}: {nm} module {g!r} != hand {want!r}")
    if sm is not None:
        bad += other_summary_findings(sm, hand_rows, tag)
    extra = set(ck) - {(bk, x["symbol"], x["entry_close"]) for bk in OTHER_BOOKS_T
                       for x in src[bk]}
    if extra:
        bad.append(f"{tag}-HAND: module rows with no source campaign {sorted(extra)[:2]}")
    return bad, st


def other_summary_findings(sm: pd.DataFrame, hand_rows: list, tag: str) -> list:
    """Every W1_OTHER_SUMMARY cell re-derived from THIS file's hand walk."""
    bad = []
    want = {}
    for bk in OTHER_BOOKS_T:
        hs = [(h, hc) for b_, h, hc in hand_rows if b_ == bk]
        for e in ERAS_T:
            sub = [(h, hc) for h, hc in hs if e == "ALL" or h["era"] == e]
            evs = [y for h, _ in sub for y in h["events"]]
            want[f"{bk}|{e}|campaigns|all|book"] = (len(sub), len(evs))
            for cls in EV_CLASSES_T:
                ph, p, sd, rl = cls.split("|")
                hit_c, n_e = 0, 0
                for h, _ in sub:
                    m = [y for y in h["events"] if y["phase"] == ph and y["pair"] == p
                         and y["side"] == sd and (rl == "-" or y["latch_rel"] == rl)]
                    n_e += len(m)
                    hit_c += int(bool(m))
                want[f"{bk}|{e}|events|{cls}|events"] = (hit_c, n_e)
            for cid, lab, _p, _s, _r, ar in COHORTS_T:
                risk = [(h, hc) for h, hc in sub if ar == "whole" or (ar == "open1h" and
                                                                     hc["open1h"])
                        or (ar == "reached" and hc["reached"])]
                mem = [(h, hc) for h, hc in risk if hc[cid]]
                comp = [(h, hc) for h, hc in risk if not hc[cid]]
                for g, grp in (("cohort", mem), ("at_risk", risk), ("complement", comp)):
                    want[f"{bk}|{e}|cohort|{cid}_{lab}|{g}"] = (
                        len(grp), sum(len(hc[cid]) for _, hc in grp))
            for pid, lab, _p, _s in PRE_T:
                mem = [(h, hc) for h, hc in sub if hc[pid]]
                comp = [(h, hc) for h, hc in sub if not hc[pid]]
                for g, grp in (("cohort", mem), ("whole_book", sub), ("complement", comp)):
                    want[f"{bk}|{e}|pre_entry|{pid}_{lab}|{g}"] = (
                        len(grp), sum(len(hc[pid]) for _, hc in grp))
    got = {str(r.cell): (int(r.n_campaigns), int(r.n_events)) for r in sm.itertuples(index=False)}
    if set(got) != set(want):
        bad.append(f"{tag}-SUMMARY: cell set differs — missing {sorted(set(want) - set(got))[:2]}, "
                   f"undeclared {sorted(set(got) - set(want))[:2]}")
    for cell in sorted(set(got) & set(want)):
        if got[cell] != want[cell]:
            bad.append(f"{tag}-SUMMARY {cell}: module (n campaigns, n events) {got[cell]} != "
                       f"this file's hand walk {want[cell]}")
    return bad


def module_other() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """The module's W1 on the other books recomputed IN-PROCESS (the path a mutation
    is judged on); every memo it reads is dropped before and after."""
    S._MEMO.pop("other", None)
    S.clear_memo(events=True)
    try:
        WO = S.w1_other()
        c = S.campaign_table_other(WO["camps"])
        ev = pd.DataFrame(WO["events"])
        sm = S.other_summary(c, ev)
    finally:
        S._MEMO.pop("other", None)
        S.clear_memo(events=True)
    return ev, c, sm


def other_break():
    def run(obj, name, value, summary=False):
        def thunk():
            with mutated(obj, name, value):
                ev, c, sm = module_other()
            return other_findings(ev, c, sm if summary else None)[0]
        return thunk

    real_arrays = S.event_arrays

    def lookahead(h1):
        a = real_arrays(h1)
        out = {}
        for p, (up, dn) in a.items():
            u, d_ = np.zeros(len(up), bool), np.zeros(len(dn), bool)
            u[:-1], d_[:-1] = up[1:], dn[1:]
            out[p] = (u, d_)
        return out

    def shifted_walk(sym):
        W = RD.walk_of(sym)
        n1 = len(W.h1.open_ms)
        a2 = np.where(W.a + RD.N_1H < n1, W.a + 1, W.a).astype(np.int64)
        return RD.Walk(W.sym, W.h1, W.open4, a2, W.n, W.ok, W.why)

    real_window = S.window_of

    def relay_at_4h_close(book, row):
        a, e = real_window(book, row)
        return (a, int(row.entry_ms) + H4) if book == "P-RELAY-1" else (a, e)

    def brk_at_touch(book, row):
        a, e = real_window(book, row)
        return (int(row.touch_close_ms), e) if book == "P-BRK-4H" else (a, e)

    def summary_bent():
        sm = written("W1_OTHER_SUMMARY")
        i = int(np.flatnonzero((sm["kind"] == "cohort").to_numpy())[0])
        sm.loc[i, "n_campaigns"] = int(sm.loc[i, "n_campaigns"]) + 1
        return other_findings(written("W1_EVENTS_OTHER"), written("W1_CAMPAIGNS_OTHER"), sm)[0]

    def fallback_unlabelled():
        c = written("W1_CAMPAIGNS_OTHER")
        i = int(np.flatnonzero(((c["book"] == "P-BRK-4H")
                                & (c["exit_resolved_by"] == "1h")).to_numpy())[0])
        c.loc[i, "resolution"] = "4h-close-fallback"
        return other_findings(written("W1_EVENTS_OTHER"), c, None)[0]

    def book_cut():
        c = written("W1_CAMPAIGNS_OTHER")
        keep = c[c["book"] == "P-RELAY-1"].index[:MIN_HAND_T - 1]
        c = c[(c["book"] != "P-RELAY-1") | c.index.isin(keep)]
        return other_findings(written("W1_EVENTS_OTHER"), c, None)[0]

    def lookahead_thunk():
        with mutated(S, "event_arrays", lookahead):
            ev, c, sm = module_other()
        return other_findings(ev, c, None)[0]

    return plants([
        ("`visible` reads the 1h bar that closes after the 4h close (other books, in-process)",
         "W1-OTHER-VIS", run(S, "visible", lambda close, T: int(close) <= int(T) + H1)),
        ("a look-ahead event tape: each cross flagged on the 1h bar before it (in-process)",
         "W1-OTHER-HAND", lookahead_thunk),
        ("the 9/12 / P-BRK-4H resolver walks children shifted one 1h bar late (the child "
         "closing after the 4h bar's close read)", "W1-OTHER-HAND",
         run(S, "other_walk", shifted_walk)),
        ("the exit instant taken at the 4h exit-bar close on every book (in-process)",
         "W1-OTHER-HAND", run(S, "exit_instant", lambda w: int(w.exit_ms) + H4)),
        ("a relay's in-trade window opened at its 4h bar close, not its 1h entry close",
         "W1-OTHER-HAND", run(S, "window_of", relay_at_4h_close)),
        ("P-BRK-4H's window opened at the touch close, not the death close", "W1-OTHER-HAND",
         run(S, "window_of", brk_at_touch)),
        ("one W1_OTHER_SUMMARY cohort size bent by one (copy)", "W1-OTHER-SUMMARY",
         summary_bent),
        ("a 1h-resolved row relabelled a fallback with no reason (copy)", "W1-OTHER-FALLBACK",
         fallback_unlabelled),
        ("P-RELAY-1 cut to 19 hand-walkable rows (copy)", "W1-OTHER-N", book_cut),
    ])


def other_real():
    ev, c, sm = (written("W1_EVENTS_OTHER"), written("W1_CAMPAIGNS_OTHER"),
                 written("W1_OTHER_SUMMARY"))
    bad, st = other_findings(ev, c, sm)
    man = json.loads((OUT / "MANIFEST_STAGE_W.json").read_text(encoding="utf-8"))
    dis = man["disclosures"].get("other_books", {})
    for bk in OTHER_BOOKS_T:
        if len(dis.get(bk, {}).get("fallbacks", [None])) != st["fallback"][bk]:
            bad.append(f"W1-OTHER-FALLBACK {bk}: the manifest lists "
                       f"{len(dis.get(bk, {}).get('fallbacks', []))} fallbacks, the table "
                       f"{st['fallback'][bk]}")
    per = "; ".join(f"{bk} n {st['n'][bk]} (events {st['events'][bk]}, 1h exits by "
                    f"{dict(sorted(st['by'][bk].items()))}, 4h-close fallbacks "
                    f"{st['fallback'][bk]})" for bk in OTHER_BOOKS_T)
    return verdict(bad, (
        f"EVERY campaign of the three other 4h books hand-walked from the raw 1h bars (own "
        f"EMA 9/12, 12/26, 12/89; own walk law; the book's exit bar and exit price, the "
        f"typed window open per book): {per}; every W1_EVENTS_OTHER row == the hand walk on "
        f"(cross, side, phase, latch relation, taken, visible 4h close, mismatch flag, close, "
        f"strict flag, era); every W1_CAMPAIGNS_OTHER fact (window open, exit instant and "
        f"resolver, both latch readings, memberships, counts, first events) equal; the "
        f"relay hand walk == its regbook of record's exit_close_ms and latch_1h_ms on "
        f"{st['record_checked']} relays; all {len(sm)} W1_OTHER_SUMMARY cells re-derived "
        f"equal; visibility: each event first visible at the first 4h close >= its 1h close"))


# ═══════════════════════════════════════════════════════════════ F-WARN-ASOF
def vis_findings(ev: pd.DataFrame, tl: pd.DataFrame, tag: str = "WARN-ASOF-VIS") -> list:
    bad = []
    for r in ev.itertuples(index=False):
        cl = own4(r.symbol)["closes"]
        i = int(np.searchsorted(cl, int(r.close_ms), "left"))
        want = int(cl[i])
        prev_ok = i == 0 or int(cl[i - 1]) < int(r.close_ms)
        if int(r.visible_4h_close_ms) != want or not prev_ok:
            bad.append(f"{tag} {r.symbol} {r.pair} 1h close {iso(int(r.close_ms))}: visible at "
                       f"{iso(int(r.visible_4h_close_ms))}, the law says {iso(want)}")
    # the timeline, against THIS file's hand walk (row set, the six class counts, the
    # in-trade pre-+1R counter 12/89 count, the stage) [L-W.1]
    cols = [f"n_vis_{p.replace('/', '_')}_{s}" for p in PAIRS_TYPED for s in ("counter", "with")]
    rows_of = {}
    for r in tl.itertuples(index=False):
        rows_of.setdefault((r.symbol, int(r.entry_ms)), []).append(r)
    for t in base():
        h = hand_campaign(t)
        key = (t.symbol, int(t.entry_ms))
        lab = f"{t.symbol} {iso(int(t.entry_ms))}"
        cl = own4(t.symbol)["closes"]
        want_T = [int(x) for x in cl[int(np.searchsorted(cl, h["arm_close"], "right")):
                                     int(np.searchsorted(cl, h["exit_bar_close"], "right"))]]
        rows = rows_of.get(key, [])
        if sorted(int(r.bar_close_ms) for r in rows) != want_T:
            bad.append(f"{tag} {lab}: timeline rows {len(rows)} are not this file's 4h closes "
                       f"in (arm close, exit-bar close] ({len(want_T)})")
        for r in rows:
            T = int(r.bar_close_ms)
            vis = [x for x in h["events"] if x["close_ms"] <= T]
            want = {c: 0 for c in cols}
            for x in vis:
                want[f"n_vis_{x['pair'].replace('/', '_')}_{x['side']}"] += 1
            want["n_vis_in_trade_pre1r_counter_12_89"] = sum(
                1 for x in vis if x["pair"] == "12/89" and x["side"] == "counter"
                and x["phase"] == "IN-TRADE" and x["latch_rel"] == "before")
            want["stage"] = ("armed" if T <= h["entry_close"] else
                             "in_trade" if T < h["exit_bar_close"] else "exit_bar")
            for col, v in want.items():
                g = getattr(r, col)
                if (str(g) if col == "stage" else int(g)) != v:
                    bad.append(f"{tag} {lab} at {iso(T)}: {col} {g!r} != this file's {v!r} "
                               f"(hand-walked events with close <= T; the typed stage law)")
                    break
    return bad


def _prefix_tape(sym: str, T: int) -> RD.H1Tape:
    Hh = own1(sym)
    n = int(np.searchsorted(Hh["t"] + H1, int(T), "right"))
    return RD.H1Tape(sym, Hh["t"][:n].copy(), Hh["o"][:n].copy(), Hh["h"][:n].copy(),
                     Hh["l"][:n].copy(), Hh["c"][:n].copy(), source="fixture-prefix")


def cuts() -> list:
    """AIMED cuts: for every C1 campaign, the 4h close just before its first C1 event
    becomes visible and that close; for every asset, 4h closes immediately BEFORE a
    W1 cross on a bar's first child (the look-ahead's bite point), 6 per asset;
    plus 12 SEEDED cuts over the campaigns' 4h timelines."""
    if "cuts" in _C:
        return _C["cuts"]
    ev = written("W1_EVENTS")
    out = set()
    c1 = ev[(ev["pair"] == "12/89") & (ev["side"] == "counter") & (ev["phase"] == "IN-TRADE")
            & (ev["latch_rel"] == "before")]
    first = c1.sort_values(["taken_ms"]).groupby(["symbol", "entry_ms"]).head(1)
    for r in first.itertuples(index=False):
        out.add((r.symbol, int(r.visible_4h_close_ms)))
        out.add((r.symbol, int(r.visible_4h_close_ms) - H4))
    for s in CLASSIC5_TYPED:
        e0 = ev[(ev["symbol"] == s) & ((ev["close_ms"] - H1) % H4 == 0)].sort_values(
            ["close_ms", "pair"])
        for r in e0.head(6).itertuples(index=False):
            out.add((s, int(r.close_ms) - H1))
    tl = written("W1_TIMELINE")
    rng = np.random.default_rng(SEED)
    for i in sorted(rng.choice(len(tl), size=12, replace=False).tolist()):
        out.add((str(tl.iloc[i]["symbol"]), int(tl.iloc[i]["bar_close_ms"])))
    _C["cuts"] = sorted(out)
    return _C["cuts"]


def prefix_findings(tag: str = "WARN-ASOF-PREFIX") -> tuple[list, int]:
    bad = []
    full = {}
    cs = cuts()
    for s, T in cs:
        if s not in full:
            fa = S.event_arrays(RD.h1_tape(s))
            full[s] = fa
        fa = full[s]
        tp = _prefix_tape(s, T)
        pa = S.event_arrays(tp)
        n = len(tp.open_ms)
        for p in PAIRS_TYPED:
            for j, nm in ((0, "up"), (1, "dn")):
                a_full = np.asarray(fa[p][j][:n], bool)
                a_pre = np.asarray(pa[p][j], bool)
                if not np.array_equal(a_full, a_pre):
                    k = int(np.flatnonzero(a_full != a_pre)[0])
                    bad.append(f"{tag} {s} cut {iso(T)} {p} {nm}: the whole-tape event tape "
                               f"says {bool(a_full[k])} at the 1h bar closing "
                               f"{iso(int(tp.open_ms[k]) + H1)}, the prefix says "
                               f"{bool(a_pre[k])}")
                    break
    return bad, len(cs)


def plant_campaign():
    """A REAL v6 stop exit whose stop child is not the exit bar's last child, pre-+1R,
    outside cohort C1 — the first by key; the plant: a counter 12/89 cross on the
    child AFTER the stop child (walkable)."""
    c = written("W1_CAMPAIGNS")
    for t in base():
        r = c[(c["symbol"] == t.symbol) & (c["entry_ms"] == int(t.entry_ms))].iloc[0]
        if (t.exit_reason == "stop" and r["exit_resolved_by"] == "1h"
                and int(r["exit_close_ms"]) + H1 <= int(r["exit_bar_close_ms"])
                and pd.isna(r["latch_ms"]) and not bool(r["C1_member"])):
            return t
    raise RuntimeError("no campaign fits the plant")


def exit_plant_findings(tag: str = "WARN-ASOF-EXIT") -> tuple[list, str]:
    """The PLANTED campaign through the module's own path (campaign_info ->
    classify_campaign -> in_class) with a planted event DataFrame."""
    rd = rides()
    t = plant_campaign()
    w = next(x for x in rd["walked"] if (x.symbol, int(x.entry_ms)) == (t.symbol,
                                                                        int(t.entry_ms)))
    ci = S.campaign_info(t, w)
    h = hand_campaign(t)
    x_close = h["exit_close"]
    k = own1(t.symbol)["idx"][x_close]           # the 1h bar AFTER the stop child
    d = int(t.direction)
    plant = pd.DataFrame([{"pair": "12/89", "cross": "dn" if d == 1 else "up", "k": k,
                           "h1_open_ms": x_close, "close_ms": x_close + H1,
                           "J": int(t.exit_i), "parent_open_ms": int(t.exit_ms),
                           "parent_close_ms": int(t.exit_ms) + H4, "walkable": True,
                           "taken_ms": x_close + H1, "px_taken": 0.0}])
    rows = S.classify_campaign(ci, plant, own4(t.symbol)["closes"])
    bad = []
    if len(rows) != 1:
        bad.append(f"{tag} plant: {len(rows)} rows classified, expected 1")
    else:
        r = rows[0]
        if r["phase"] != "POST-EXIT" or S.in_class(r, "12/89", "counter", "IN-TRADE", "before"):
            bad.append(f"{tag} PLANT {t.symbol} {iso(int(t.entry_ms))}: a counter 12/89 cross "
                       f"closing {iso(x_close + H1)} AFTER the stop child "
                       f"({iso(x_close)}) classified {r['phase']} / C1 "
                       f"{S.in_class(r, '12/89', 'counter', 'IN-TRADE', 'before')}")
    return bad, f"{t.symbol} {iso(int(t.entry_ms))} stop child {iso(x_close)}"


def exit_real_findings(ev: pd.DataFrame, tag: str = "WARN-ASOF-EXIT") -> tuple[list, int]:
    """Every IN-TRADE event is strictly before the hand-walked exit; every event after
    it (inside the exit bar) is POST-EXIT."""
    bad = []
    n_post = 0
    hk = {(t.symbol, int(t.entry_ms)): hand_campaign(t) for t in base()}
    for r in ev.itertuples(index=False):
        h = hk[(r.symbol, int(r.entry_ms))]
        if r.phase == "IN-TRADE" and not int(r.taken_ms) < h["exit_close"]:
            bad.append(f"{tag} {r.symbol} {iso(int(r.entry_ms))} {r.pair}: IN-TRADE at "
                       f"{iso(int(r.taken_ms))}, not before the 1h exit {iso(h['exit_close'])}")
        if int(r.taken_ms) > h["exit_close"]:
            n_post += 1
            if r.phase != "POST-EXIT":
                bad.append(f"{tag} {r.symbol} {iso(int(r.entry_ms))} {r.pair}: a cross at "
                           f"{iso(int(r.taken_ms))} after the 1h exit {iso(h['exit_close'])} "
                           f"classified {r.phase}")
    return bad, n_post


def asof_break():
    def vis_plant():
        with mutated(S, "visible", lambda close, T: int(close) <= int(T) + H1):
            ev, c, x = module_w1()
        return vis_findings(ev, x["timeline"])

    real_arrays = S.event_arrays

    def lookahead(h1):
        a = real_arrays(h1)
        out = {}
        for p, (up, dn) in a.items():
            u, d_ = np.zeros(len(up), bool), np.zeros(len(dn), bool)
            u[:-1], d_[:-1] = up[1:], dn[1:]
            out[p] = (u, d_)
        return out

    def prefix_plant():
        with mutated(S, "event_arrays", lookahead):
            return prefix_findings()[0]

    def exit_plant():
        with mutated(S, "exit_instant", lambda w: int(w.exit_ms) + H4):
            b1, _ = exit_plant_findings()
            ev, c, _ = module_w1()
            b2, _ = exit_real_findings(ev)
        return b1 + b2

    def stage_bent():
        tl = written("W1_TIMELINE")
        tl.loc[tl["stage"] == "exit_bar", "stage"] = "in_trade"
        return vis_findings(written("W1_EVENTS"), tl)

    def pre1r_bent():
        tl = written("W1_TIMELINE")
        i = int(np.flatnonzero((tl["n_vis_in_trade_pre1r_counter_12_89"] > 0).to_numpy())[0])
        tl.loc[i, "n_vis_in_trade_pre1r_counter_12_89"] = int(
            tl.loc[i, "n_vis_in_trade_pre1r_counter_12_89"]) - 1
        return vis_findings(written("W1_EVENTS"), tl)

    return plants([
        ("`visible` reads the 1h bar that closes after the 4h close", "WARN-ASOF-VIS",
         vis_plant),
        ("the timeline stage read with the exit-bar close counted in-trade (copy)",
         "WARN-ASOF-VIS", stage_bent),
        ("one in-trade pre-+1R counter 12/89 visible count dropped (copy)",
         "n_vis_in_trade_pre1r_counter_12_89", pre1r_bent),
        ("a look-ahead event tape (a cross flagged one 1h bar early)", "WARN-ASOF-PREFIX",
         prefix_plant),
        ("the exit taken at the 4h exit-bar close (plant + real post-stop-child crosses)",
         "WARN-ASOF-EXIT", exit_plant),
    ])


def asof_real():
    ev, tl = written("W1_EVENTS"), written("W1_TIMELINE")
    bad = vis_findings(ev, tl)
    b2, ncut = prefix_findings()
    b3, pl = exit_plant_findings()
    b4, n_post = exit_real_findings(ev)
    bad += b2 + b3 + b4
    return verdict(bad, (
        f"visibility: all {len(ev)} W1 events visible first at the first 4h close >= their "
        f"1h close; all {len(tl)} W1_TIMELINE rows == this file's hand walk (row set = the 4h "
        f"closes in (arm close, exit-bar close]; the six class counts and the in-trade "
        f"pre-+1R counter 12/89 count of hand-walked events with close <= T; the typed "
        f"stage); causality: {ncut} aimed + seeded cuts, the module's event arrays on the 1h "
        f"prefix == its whole-tape arrays restricted to close <= T; exit resolution: every "
        f"IN-TRADE event strictly before the hand-walked 1h exit, {n_post} real crosses after "
        f"the exit child all POST-EXIT, and the PLANT ({pl}; a counter 12/89 cross on the "
        f"next child) is POST-EXIT, outside C1"))


# ═══════════════════════════════════════════════════════════════ F-WARN-COHORT
def own_boot_diff(va, ca, vb, cb, seed: int, n: int) -> np.ndarray:
    """THE TYPED LAW: two-sample asset-cluster bootstrap of (mean A − mean B), the
    SAME asset draw into both arms (np.random.default_rng(seed); per draw
    rng.choice(sorted unique assets, k, replace=True)) — this file's loop."""
    va, vb = np.asarray(va, float), np.asarray(vb, float)
    ca, cb = np.asarray(ca), np.asarray(cb)
    uniq = np.unique(np.concatenate([ca, cb]))
    ia = {u: [i for i in range(len(ca)) if ca[i] == u] for u in uniq}
    ib = {u: [i for i in range(len(cb)) if cb[i] == u] for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(n)
    for b in range(n):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        ta = [i for u in pick for i in ia[u]]
        tb = [i for u in pick for i in ib[u]]
        out[b] = ((float(np.mean(va[ta])) if ta else np.nan)
                  - (float(np.mean(vb[tb])) if tb else np.nan))
    return out


def own_ci(draws: np.ndarray) -> tuple[float, float]:
    d = draws[np.isfinite(draws)]
    return float(np.percentile(d, 5)), float(np.percentile(d, 95))


def cohort_findings(cond: dict, c: pd.DataFrame, ev: pd.DataFrame, warn_keys: set,
                    status: dict | None = None, tag: str = "WARN-COHORT") -> tuple[list, dict]:
    bad = []
    coh = set(cond["cohort_keys"])
    c1 = {kstr(s, e) for s, e, m in zip(c["symbol"], c["entry_ms"], c["C1_member"]) if bool(m)}
    if coh != c1:
        bad.append(f"{tag}: condition.json cohort ({len(coh)}) != the W1_CAMPAIGNS C1 set "
                   f"({len(c1)})")
    q = ev[(ev["pair"] == "12/89") & (ev["side"] == "counter") & (ev["phase"] == "IN-TRADE")
           & (ev["latch_rel"] == "before")].sort_values(["taken_ms", "close_ms"])
    first = q.groupby(["symbol", "entry_ms"]).head(1)
    mism = {kstr(r.symbol, r.entry_ms) for r in first.itertuples(index=False)
            if bool(r.on_mismatch_bar)}
    if sorted(mism) != list(cond["listed_mismatch_keys"]):
        bad.append(f"{tag}-MISMATCH-LIST: keys whose first qualifying cross fell on a mismatch "
                   f"bar {sorted(mism)} != listed {cond['listed_mismatch_keys']}")
    if coh != (warn_keys | mism):
        bad.append(f"{tag}: cohort keys ({len(coh)}) != warn-exit keys ({len(warn_keys)}) + "
                   f"listed mismatch keys ({len(mism)}); cohort-only "
                   f"{sorted(coh - warn_keys - mism)[:3]}, warn-only "
                   f"{sorted(warn_keys - coh)[:3]} [L-W.4]")
    # the printed flag is THE FROZEN LAW evaluated here (belltie never absorbed)
    law = coh == (warn_keys | mism)
    if cond.get("cohort_law_holds") is not law:
        bad.append(f"{tag}-LAWFLAG: condition.json cohort_law_holds "
                   f"{cond.get('cohort_law_holds')!r} != the frozen L-W.4 law evaluated here "
                   f"({law!r}: cohort == warn ∪ mismatch)")
    belltie = sorted(warn_keys - coh)
    if list(cond.get("listed_belltie_keys", [])) != belltie or \
            cond.get("belltie_n") != len(belltie):
        bad.append(f"{tag}-BELLTIE: listed belltie {cond.get('listed_belltie_keys')} / n "
                   f"{cond.get('belltie_n')} != warn keys outside the cohort {belltie}")
    # the condition numbers, recomputed by the typed law
    bk = [(t.symbol, float(t.net_r)) for t in base()]
    net = np.array([x[1] for x in bk])
    sym = np.array([x[0] for x in bk])
    mem = np.array([kstr(t.symbol, t.entry_ms) in coh for t in base()])
    va, ca = net[mem], sym[mem]
    lo, hi = own_ci(own_boot_diff(va, ca, net, sym, SEED, N_BOOT))
    slo, shi = own_ci(own_boot_diff(va, ca, net, sym, SEED_SENS, N_BOOT))
    want = {"cohort_n": int(mem.sum()), "cohort_mean": float(va.mean()),
            "book_mean": float(net.mean()), "delta": float(va.mean() - net.mean()),
            "ci_lo": lo, "ci_hi": hi, "met": bool(hi < 0), "seed": SEED, "n_boot": N_BOOT}
    for k, v in want.items():
        if cond.get(k) != v:
            bad.append(f"{tag}-COND: {k} = {cond.get(k)!r}, the typed law gives {v!r}")
    sc = cond.get("sens_seed_ci", {})
    if (sc.get("seed"), sc.get("lo"), sc.get("hi")) != (SEED_SENS, slo, shi):
        bad.append(f"{tag}-COND: sensitivity CI {sc} != ({SEED_SENS}, {slo!r}, {shi!r})")
    if status is not None:
        st = "BUILT" if want["met"] else "CONDITION_NOT_MET"
        if status.get("status") != st or tuple(status.get("arms", ())) != ARMS_T[st]:
            bad.append(f"{tag}-COND: STATUS {status.get('status')} arms {status.get('arms')} "
                       f"!= typed {st} {ARMS_T[st]}")
    return bad, {**want, "mism": sorted(mism), "sens": (slo, shi)}


def warn_keys_of(rule_book) -> set:
    return {kstr(t.symbol, t.entry_ms) for t in rule_book if t.exit_reason == WARN_LBL}


def cohort_break():
    cond = reg_json("condition.json")
    c, ev = written("W1_CAMPAIGNS"), written("W1_EVENTS")
    wk = warn_keys_of(rides()["rule"])
    real_phase = S.phase_of

    def phase_admits_pre(taken, arm_close, entry_close, exit_close):
        ph = real_phase(taken, arm_close, entry_close, exit_close)
        return "IN-TRADE" if ph == "PRE-ENTRY" else ph

    def pre_admitted():
        with mutated(S, "phase_of", phase_admits_pre):
            ev2, c2, _ = module_w1()
            cd = S.condition(c2, rides())
        return [x for x in cohort_findings(cd, c2, ev2, wk)[0]
                if x.startswith("WARN-COHORT:")]

    def rival_as_condition():
        cd = copy.deepcopy(cond)
        rv = cd["rival_complement"]
        cd.update(delta=rv["delta"], ci_lo=rv["ci_lo"], ci_hi=rv["ci_hi"])
        return cohort_findings(cd, c, ev, wk)[0]

    def met_flipped():
        cd = copy.deepcopy(cond)
        cd["met"] = not cd["met"]
        return cohort_findings(cd, c, ev, wk)[0]

    def mismatch_omitted():
        ev2 = ev.copy()
        q = ev2[(ev2["pair"] == "12/89") & (ev2["side"] == "counter")
                & (ev2["phase"] == "IN-TRADE") & (ev2["latch_rel"] == "before")]
        i = q.sort_values(["taken_ms"]).index[0]
        ev2.loc[i, "on_mismatch_bar"] = True       # the first C1 cross now sits on a mismatch bar
        return cohort_findings(cond, c, ev2, wk)[0]

    def belltie_absorbed():
        cd = copy.deepcopy(cond)                   # the flag stays True, as the loose law
        return cohort_findings(cd, c, ev, wk | {"ZZZPLANT|1"})[0]   # would print it

    return plants([
        ("pre-entry crosses admitted into the in-trade classes (in-process cohort)",
         "WARN-COHORT:", pre_admitted),
        ("cohort_law_holds printed True with a planted belltie warn key (the loose law)",
         "WARN-COHORT-LAWFLAG", belltie_absorbed),
        ("the rival (complement) delta passed off as the condition", "WARN-COHORT-COND",
         rival_as_condition),
        ("the MET flag flipped", "WARN-COHORT-COND", met_flipped),
        ("a mismatch-bar first cross not listed", "WARN-COHORT-MISMATCH-LIST",
         mismatch_omitted),
    ])


def cohort_real():
    cond = reg_json("condition.json")
    status = reg_json("STATUS.json")
    c, ev = written("W1_CAMPAIGNS"), written("W1_EVENTS")
    rule_pq = reg_parquet(ARMS_T[status["status"]][0])
    wk_pq = {kstr(s, e) for s, e, r in zip(rule_pq["symbol"], rule_pq["entry_ms"],
                                             rule_pq["exit_reason"]) if r == WARN_LBL}
    wk = warn_keys_of(rides()["rule"])
    bad, st = cohort_findings(cond, c, ev, wk_pq, status)
    if wk != wk_pq:
        bad.append("WARN-COHORT: the rule regbook's warn keys != the live rule book's")
    return verdict(bad, (
        f"condition cohort {st['cohort_n']} keys == the rule book's {len(wk_pq)} warn-exit keys "
        f"+ listed mismatch keys {st['mism'] or 'none'}, and condition.json's "
        f"cohort_law_holds {cond['cohort_law_holds']} is the frozen law evaluated here (belltie "
        f"listed separately: {cond['listed_belltie_keys'] or 'none'}); == the W1_CAMPAIGNS C1 "
        f"set; cohort mean "
        f"{st['cohort_mean']:+.6f}, book mean {st['book_mean']:+.6f}, delta "
        f"{st['delta']:+.6f}, cluster-90% [{st['ci_lo']:+.6f}, {st['ci_hi']:+.6f}] (seed "
        f"{SEED}, {N_BOOT} draws, this file's bootstrap loop) and [{st['sens'][0]:+.6f}, "
        f"{st['sens'][1]:+.6f}] at {SEED_SENS} equal condition.json exactly; MET "
        f"{st['met']} -> STATUS {status['status']} with the typed arms {list(status['arms'])}"))


# ═══════════════════════════════════════════════════════════════ F-W2-MARK
def own_fund(sym: str) -> dict:
    """THIS file's funding read of the snapshot: every print floored to its hour,
    prints on one hour summed (the estate's funding convention, typed here)."""
    k = ("fund", sym)
    if k not in _C:
        d = pd.read_parquet(str(TC11_SNAP / "funding" / f"{sym}.parquet"))
        out: dict = {}
        for ft, fr in zip(d["funding_time"].astype(np.int64), d["funding_rate"].astype(float)):
            h = int(ft) // H1 * H1
            out[h] = out.get(h, 0.0) + fr
        _C[k] = out
    return _C[k]


def own_mark(t, ev: dict) -> float:
    """THE TYPED ACCOUNT LAW (w5) on this file's own prices: the campaign exited at
    the event's taken instant at the tape's price there (the 1h close on a walkable
    bar, the parent's 4h close on a mismatch bar); one unit, half harvested at v6's
    band price iff v6's harvest bar PRECEDES the event's bar; gross and the taker
    fee (5 bps per side of every fill) over r_dist; funding = sum over the held bars
    (entry bar, exit bar] of rate(bar open) x the prior 4h close x direction x the
    held fraction; the D12 ceiling (1R) once on the total."""
    s, d = t.symbol, int(t.direction)
    X, Hh = own4(s), own1(s)
    fund = own_fund(s)
    J = int(ev["J"])
    xpx = (float(X["c"][J]) if ev["on_mismatch_bar"]
           else float(Hh["c"][Hh["idx"][int(ev["h1_open_ms"])]]))
    e, R, ti = float(t.entry_px), float(t.r_dist), int(t.entry_i)
    q, size, bps = HARVEST_FRAC_T, 1.0, BPS_T

    def fund_leg(lo_j: int, hi_j: int, qty: float) -> float:
        acc = 0.0
        for j in range(lo_j + 1, hi_j + 1):
            rate = fund.get(int(X["om"][j]))
            if rate:
                acc += rate * float(X["c"][j - 1]) * d * qty
        return acc

    if bool(t.harvested) and int(t.harvest_i) < J:
        hj, hpx = int(t.harvest_i), float(t.harvest_px)
        g1 = size * q * (hpx - e) * d
        fe1 = bps * size * q * (e + hpx)
        u1 = fund_leg(ti, hj, size * q)
        g2 = size * (1.0 - q) * (xpx - e) * d
        fe2 = bps * size * (1.0 - q) * (e + xpx)
        u2 = fund_leg(ti, J, size * (1.0 - q))
        g, fe, u = g1 + g2, fe1 + fe2, u1 + u2
    else:
        g = size * (xpx - e) * d
        fe = bps * size * (e + xpx)
        u = fund_leg(ti, J, size)
    gross, fee, fund_raw = (0.0 + g) / R, (0.0 + fe) / R, (0.0 + u) / R
    fund_eff = min(fund_raw, FUND_CAP_T) if fund_raw > FUND_CAP_T else fund_raw
    return gross - fee - fund_eff


def warn26_ride() -> list:
    """THE SECOND REFEREE for C2: the foundation ride (RD.transform_book, the v6 set
    on the 1h walk) with the warn hook on the 12/26 pair — never the module's mark
    code.  A C2 member's first event IS that ride's warn exit."""
    if "r26" not in _C:
        lo, hi, _ = B.corridor()
        w26: dict = {}

        def wof(s_):
            if s_ not in w26:
                w26[s_] = RD.warn_of(RD.walk_of(s_), 12, 26)
            return w26[s_]
        _C["r26"] = RD.transform_book(base(), S.CARD, S.ROLES, lo, hi, walk=True, warn_of=wof)
    return _C["r26"]


def own_marks() -> dict:
    """{(cid, key): (own mark, first event)} for every member of every cohort."""
    if "ownmarks" not in _C:
        out = {}
        for t in base():
            hc = hand_classes(hand_campaign(t))
            for cid, *_ in COHORTS_T:
                f0 = first_of(hc[cid])
                if f0 is not None:
                    out[(cid, (t.symbol, int(t.entry_ms)))] = (own_mark(t, f0), f0)
        _C["ownmarks"] = out
    return _C["ownmarks"]


def mark_findings(cf: pd.DataFrame, fw: pd.DataFrame, cw: pd.DataFrame,
                  tag: str = "W2-MARK") -> tuple[list, dict]:
    """cf = the module's W1_CAMPAIGNS at full precision; fw / cw = W2_FORWARD /
    W1_CAMPAIGNS as written (6 dp)."""
    bad = []
    for nm, got, want in (("harvest_frac", float(S.CARD.harvest_frac), HARVEST_FRAC_T),
                          ("funding_ceiling_r", float(S.CARD.funding_ceiling_r), FUND_CAP_T),
                          ("FEE_BPS_SIDE", float(T9.RC.FEE_BPS_SIDE), TAKER_T)):
        if got != want:
            bad.append(f"{tag} TYPED: the card's {nm} {got!r} != the commission's {want!r}")
    OM = own_marks()
    ci = cf.set_index(["symbol", "entry_ms"])
    wi = cw.set_index(["symbol", "entry_ms"])
    rule = reg_parquet(ARMS_T[reg_json("STATUS.json")["status"]][0]).set_index(
        ["symbol", "entry_ms"])
    r26 = {(x.symbol, int(x.entry_ms)): x for x in warn26_ride()}
    per = {cid: 0 for cid, *_ in COHORTS_T}
    n_c1_rule = n_c2_ride = 0
    for t in base():
        key = (t.symbol, int(t.entry_ms))
        lab = f"{t.symbol} {iso(key[1])}"
        h = hand_campaign(t)
        for cid, *_ in COHORTS_T:
            mine = OM.get((cid, key))
            mod = _nn(ci.loc[key, f"{cid}_mark_r"])
            if (mine is None) != (mod is None):
                bad.append(f"{tag} {cid} {lab}: a mark on one side only (own "
                           f"{None if mine is None else mine[0]!r}, module "
                           f"{None if mod is None else float(mod)!r})")
                continue
            if mine is None:
                continue
            per[cid] += 1
            mk = mine[0]
            if float(mod) != mk:
                bad.append(f"{tag} {cid} {lab}: module mark {float(mod)!r} != this file's own "
                           f"price {mk!r} (diff {float(mod) - mk:.3e})")
            for col, v in ((f"{cid}_mark_r", mk), (f"{cid}_fwd_r", float(t.net_r) - mk)):
                if float(wi.loc[key, col]) != float(np.round(v, 6)):
                    bad.append(f"{tag} {cid} {lab}: written {col} {float(wi.loc[key, col])!r} != "
                               f"the 6-dp image of this file's {v!r}")
            if cid == "C1":
                n_c1_rule += 1
                if float(rule.loc[key, "net_r"]) != mk:
                    bad.append(f"{tag} C1 {lab}: the rule book's net R "
                               f"{float(rule.loc[key, 'net_r'])!r} != this file's mark {mk!r}")
            if cid == "C2":
                x = r26[key]
                if (str(x.exit_reason), int(x.exit_close_ms), float(x.net_r)) != (
                        WARN26_LBL, int(mine[1]["taken_ms"]), mk):
                    bad.append(f"{tag} C2 {lab}: the 12/26 warn ride exits "
                               f"{x.exit_reason}@{iso(int(x.exit_close_ms))} net {x.net_r!r}, the "
                               f"first C2 event is {iso(int(mine[1]['taken_ms']))} priced {mk!r}")
                else:
                    n_c2_ride += 1
        x = r26[key]
        if (("C2", key) not in OM and str(x.exit_reason) == WARN26_LBL
                and int(x.exit_close_ms) != h["exit_close"]):
            bad.append(f"{tag} C2 {lab}: the 12/26 warn ride exits at "
                       f"{iso(int(x.exit_close_ms))} on a non-member, not a bell-tie at the exit "
                       f"{iso(h['exit_close'])}")
    # W2_FORWARD from the OWN marks, book order
    order = [(t.symbol, int(t.entry_ms)) for t in base()]
    net = np.array([float(t.net_r) for t in base()])
    era = np.array([hand_campaign(t)["era"] for t in base()])
    for cid, lab, *_ in COHORTS_T:
        mem = np.array([(cid, k) in OM for k in order])
        mk_all = np.array([OM[(cid, k)][0] if (cid, k) in OM else np.nan for k in order])
        for e in ERAS_T:
            m = mem & (np.ones(len(order), bool) if e == "ALL" else era == e)
            n = int(m.sum())
            fin, mk = net[m], mk_all[m]
            fwd = fin - mk
            want = {"n": n,
                    "mean_final_net_r": float(fin.mean()) if n else float("nan"),
                    "mean_mark_r": float(mk.mean()) if n else float("nan"),
                    "mean_fwd_r": float(fwd.mean()) if n else float("nan"),
                    "sum_fwd_r": float(fwd.sum()) if n else 0.0,
                    "n_fwd_pos": int((fwd > 0).sum()),
                    "p_fwd_pos": float((fwd > 0).mean()) if n else float("nan")}
            row = fw[fw["cell"] == f"{cid}_{lab}|{e}"]
            if len(row) != 1:
                bad.append(f"{tag} W2_FORWARD {cid}|{e}: cell absent")
                continue
            row = row.iloc[0]
            for col, v in want.items():
                ok = (int(row[col]) == v) if col in ("n", "n_fwd_pos") else _eq6(row[col], v)
                if not ok:
                    bad.append(f"{tag} W2_FORWARD {cid}_{lab}|{e}: {col} module "
                               f"{float(row[col])!r} != this file's {v!r} (own marks)")
    return bad, {"per": per, "c1_rule": n_c1_rule, "c2_ride": n_c2_ride}


def _w1_live() -> dict:
    if "w1live" not in _C:
        _C["w1live"] = S.w1(rides())
    return _C["w1live"]


def mark_break():
    fw, cw = written("W2_FORWARD"), written("W1_CAMPAIGNS")

    def harvest_same_bar():
        def bent(t, ev):                           # mark_at with the harvest law `<=`
            f = T9.frame(t.symbol)["f"]
            o4 = np.asarray(f.open_ms, dtype=np.int64)
            J = int(np.searchsorted(o4, int(ev["taken_ms"]) - 1, "right")) - 1
            harv = None
            if t.harvested and int(t.harvest_i) <= J:
                harv = (int(t.harvest_i), float(t.harvest_px), float(t.harvest_unit_move_r))
            leg = {"entry_i": int(t.entry_i), "exit_i": J, "exit_px": float(ev["px_taken"]),
                   "entry_px": float(t.entry_px), "harvest": harv, "adds": [],
                   "own_r": abs(float(t.entry_px) - float(t.stop_px))}
            return float(RD.account11(t.symbol, S.CARD, int(t.direction), float(t.r_dist),
                                      leg)["net_r"])
        with mutated(S, "mark_at", bent):
            c2 = S.campaign_table(_w1_live()["camps"], marks=True)
        return mark_findings(c2, fw, cw)[0]

    def mean_mark_is_final():
        f2 = fw.copy()
        f2["mean_mark_r"] = f2["mean_final_net_r"]
        return mark_findings(full_campaigns(), f2, cw)[0]

    def c4_moved():
        c2 = full_campaigns()
        i = int(np.flatnonzero(c2["C4_member"].to_numpy(bool))[0])
        c2.loc[i, "C4_mark_r"] = float(c2.loc[i, "C4_mark_r"]) + 1e-12
        return mark_findings(c2, fw, cw)[0]

    def strict_ignored():
        with mutated(S, "recross_strict", lambda pair, side, *_a: pair == "9/12"
                     and side == "with"):
            W = S.w1(rides())
            c2 = S.campaign_table(W["camps"], marks=True)
        return mark_findings(c2, fw, cw)[0]

    return plants([
        ("the harvest booked at the event's own 4h bar (mark_at's `<` bent to `<=`)",
         "W2-MARK C", harvest_same_bar),
        ("W2_FORWARD's mean_mark_r replaced by the mean final net R (copy)",
         "W2-MARK W2_FORWARD", mean_mark_is_final),
        ("one C4 mark moved 1e-12 (copy of the full-precision table)", "W2-MARK C4",
         c4_moved),
        ("C3S read without its strict flag (in-process)", "W2-MARK C3S", strict_ignored),
    ])


def mark_real():
    bad, st = mark_findings(full_campaigns(), written("W2_FORWARD"), written("W1_CAMPAIGNS"))
    per = " · ".join(f"{k} {v}" for k, v in st["per"].items())
    return verdict(bad, (
        f"every member's first event priced by THIS file's typed account law on its own "
        f"prices and its own funding read ({per} members) == the module's full-precision "
        f"mark EXACTLY; C1: {st['c1_rule']} marks == the rule book's net R exactly; C2: "
        f"{st['c2_ride']} marks == the 12/26 warn ride's net R exactly (exit at the first C2 "
        f"event), and every non-member 12/26 warn exit is a bell-tie at the exit instant; the "
        f"written W1_CAMPAIGNS marks / forward legs are their 6-dp image; W2_FORWARD "
        f"({len(DECLARED['W2_FORWARD'])} cells: n, mean final R, mean mark, mean forward, "
        f"sum forward, n / share forward > 0) re-derived from the own marks, equal"))


# ═══════════════════════════════════════════════════════════════ F-IDENTITY
def identity_findings(rule: pd.DataFrame, bas: pd.DataFrame, c: pd.DataFrame,
                      tag: str = "IDENTITY") -> tuple[list, dict]:
    bad = []
    kr = list(zip(rule["symbol"], rule["entry_ms"].astype(int)))
    kb = list(zip(bas["symbol"], bas["entry_ms"].astype(int)))
    if sorted(kr) != sorted(kb) or len(kb) != N_BOOK or len(set(kr)) != len(kr):
        bad.append(f"{tag}: paired premise — rule keys {len(set(kr))}/{len(kr)} vs base "
                   f"{len(set(kb))}/{len(kb)}, typed n {N_BOOK}")
    bm = {k: r for k, r in zip(kb, bas.itertuples(index=False))}
    cm = {(r.symbol, int(r.entry_ms)): r for r in c.itertuples(index=False)}
    n_acted = n_un = 0
    for k, r in zip(kr, rule.itertuples(index=False)):
        b = bm.get(k)
        if b is None:
            continue
        if r.exit_reason == WARN_LBL:
            n_acted += 1
            if not int(r.exit_instant_ms) < int(b.exit_instant_ms):
                bad.append(f"{tag} {k[0]} {iso(k[1])}: the warn exit "
                           f"{iso(int(r.exit_instant_ms))} is not before v6's "
                           f"{iso(int(b.exit_instant_ms))}")
            cr = cm.get(k)
            if cr is None or not bool(cr.C1_member) or float(cr.C1_mark_r) != float(r.net_r):
                bad.append(f"{tag} {k[0]} {iso(k[1])}: the C1 mark "
                           f"{None if cr is None else cr.C1_mark_r!r} != the rule book's net R "
                           f"{float(r.net_r)!r} (w5)")
            continue
        n_un += 1
        for col in ("net_r", "gross_r", "fee_r", "funding_r", "haircut_net_r"):
            dv = abs(float(getattr(r, col)) - float(getattr(b, col)))
            if dv != 0.0:
                bad.append(f"{tag} {k[0]} {iso(k[1])}: {col} differs by {dv:.3e} on a "
                           f"campaign the rule never acted on")
        if (int(r.exit_close_ms), int(r.exit_instant_ms), r.exit_reason) != (
                int(b.exit_close_ms), int(b.exit_instant_ms), b.exit_reason):
            bad.append(f"{tag} {k[0]} {iso(k[1])}: exit {r.exit_reason}@{r.exit_close_ms} != v6 "
                       f"{b.exit_reason}@{b.exit_close_ms} on an unacted campaign")
        if str(r.acted_by) != "":
            bad.append(f"{tag} {k[0]} {iso(k[1])}: acted_by {r.acted_by!r} without a warn exit "
                       f"— an acted campaign with no footprint")
    return bad, {"acted": n_acted, "unacted": n_un}


def complement_findings(rule: pd.DataFrame, bas: pd.DataFrame,
                        tag: str = "IDENTITY-TABLES") -> list:
    """P_WARN_1_COMPLEMENT re-derived from the two regbook parquets (the rule ride vs
    v6), in book order: n, the net sums and their delta, and the AM-7 haircut sums
    by THIS file's typed tiers."""
    bad = []
    order = [(t.symbol, int(t.entry_ms)) for t in base()]
    era = np.array([hand_campaign(t)["era"] for t in base()])
    rm = rule.set_index(["symbol", "entry_ms"]).loc[order]
    bm = bas.set_index(["symbol", "entry_ms"]).loc[order]
    rv, bv = rm["net_r"].to_numpy(float), bm["net_r"].to_numpy(float)
    slip = np.array([SLIP_T[s_] for s_, _ in order])
    rh = rv - rm["fee_r"].to_numpy(float) * (slip / TAKER_T)
    bh = bv - bm["fee_r"].to_numpy(float) * (slip / TAKER_T)
    coh = set(reg_json("condition.json")["cohort_keys"])
    mem = np.array([kstr(s_, e_) in coh for s_, e_ in order])
    act = (rm["exit_reason"] == WARN_LBL).to_numpy()
    groups = {"cohort_C1": mem, "complement_C1": ~mem, "acted": act, "unacted": ~act,
              "ALL": np.ones(len(order), bool)}
    cp = written("P_WARN_1_COMPLEMENT")
    for g, gm in groups.items():
        for e in ERAS_T:
            m = gm & (np.ones(len(order), bool) if e == "ALL" else era == e)
            row = cp[cp["cell"] == f"{g}|{e}"].iloc[0]
            got = (int(row["n"]), float(row["sum_v6_r"]), float(row["sum_rule_r"]),
                   float(row["sum_delta_r"]), float(row["sum_v6_haircut_r"]),
                   float(row["sum_rule_haircut_r"]))
            want = (int(m.sum()), float(np.round(bv[m].sum(), 6)),
                    float(np.round(rv[m].sum(), 6)), float(np.round((rv[m] - bv[m]).sum(), 6)),
                    float(np.round(bh[m].sum(), 6)), float(np.round(rh[m].sum(), 6)))
            if got != want:
                bad.append(f"{tag} P_WARN_1_COMPLEMENT {g}|{e}: module {got} != re-derived "
                           f"{want}")
    return bad


def ident_break():
    status = reg_json("STATUS.json")
    rule = reg_parquet(ARMS_T[status["status"]][0])
    bas = reg_parquet("base")
    c = full_campaigns()

    def bent():
        r2 = rule.copy()
        i = int(np.flatnonzero((r2["exit_reason"] != WARN_LBL).to_numpy())[0])
        r2.loc[i, "net_r"] = float(r2.loc[i, "net_r"]) + 1e-12
        return identity_findings(r2, bas, c)[0]

    def dropped():
        return identity_findings(rule.iloc[1:].reset_index(drop=True), bas, c)[0]

    def relabelled():
        r2 = rule.copy()
        i = int(np.flatnonzero((r2["exit_reason"] == WARN_LBL).to_numpy())[0])
        k = (r2.loc[i, "symbol"], int(r2.loc[i, "entry_ms"]))
        b = bas[(bas["symbol"] == k[0]) & (bas["entry_ms"] == k[1])].iloc[0]
        r2.loc[i, "exit_reason"] = b["exit_reason"]      # the warn exit relabelled to v6's
        return identity_findings(r2, bas, c)[0]

    return plants([
        ("an unacted campaign's net_r +1e-12 in a copy", "IDENTITY", bent),
        ("one campaign dropped from the rule book", "IDENTITY: paired premise", dropped),
        ("an acted campaign's exit relabelled to v6's (no footprint)", "without a warn exit",
         relabelled),
    ])


def ident_real():
    status = reg_json("STATUS.json")
    rule = reg_parquet(ARMS_T[status["status"]][0])
    bas = reg_parquet("base")
    c = full_campaigns()
    bad, st = identity_findings(rule, bas, c)
    cw = written("W1_CAMPAIGNS").set_index(["symbol", "entry_ms"])
    cf = c.set_index(["symbol", "entry_ms"]).loc[cw.index]
    for cid, *_ in COHORTS_T:
        for col in (f"{cid}_mark_r", f"{cid}_fwd_r"):
            a = cw[col].to_numpy(float)
            b = np.round(cf[col].to_numpy(float), 6)
            if not np.array_equal(a, b, equal_nan=True):
                bad.append(f"IDENTITY: the written {col} is not the 6-dp image of the "
                           f"module's full-precision column")
    rd = rides()
    idf, ist = RD.identity_findings(rd["base"], rd["rule"])
    bad += [f"IDENTITY (RD helper): {x}" for x in idf]
    bt = {(t.symbol, int(t.entry_ms)): t for t in rd["base"]}
    for r in bas.itertuples(index=False):
        t = bt.get((r.symbol, int(r.entry_ms)))
        if t is None or float(t.net_r) != float(r.net_r) or float(t.fee_r) != float(r.fee_r) \
                or t.exit_reason != r.exit_reason:
            bad.append(f"IDENTITY base {r.symbol} {iso(int(r.entry_ms))}: the base arm is not "
                       f"the v6 Trade")
    v6c = pd.read_parquet(str(B.OUT / "v6_campaigns.parquet")).set_index(["symbol",
                                                                         "entry_ms"])
    bi = bas.set_index(["symbol", "entry_ms"])
    if sorted(v6c.index) != sorted(bi.index):
        bad.append("IDENTITY base: the base arm's keys are not books/v6_campaigns.parquet's")
    else:
        v6c = v6c.loc[bi.index]
        for col, vcol in (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
                          ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
                          ("lane", "lane"), ("era", "era_of_entry")):
            if not bool((bi[col].to_numpy() == v6c[vcol].to_numpy()).all()):
                bad.append(f"IDENTITY base: {col} != books/v6_campaigns.parquet {vcol}")
        for col in ("entry_px", "stop_px", "r_dist", "net_r", "gross_r", "fee_r", "funding_r"):
            if not bool((np.round(bi[col].to_numpy(float), 6)
                         == v6c[col].to_numpy(float)).all()):
                bad.append(f"IDENTITY base: {col} at 6 dp != books/v6_campaigns.parquet")
    man = json.loads((B.OUT / "build_manifest.json").read_text(encoding="utf-8"))
    if B.book_sha(rd["base"]) != man["book_sha"]["v6"]:
        bad.append("IDENTITY base: the live v6 book is not the filed TC11-BOOKS v6 sha")
    if st["acted"] != ist["acted"]:
        bad.append(f"IDENTITY: acted {st['acted']} != the RD helper's {ist['acted']}")
    bad += complement_findings(rule, bas)
    return verdict(bad, (
        f"paired premise: identical key sets, n {N_BOOK} each; {st['unacted']} unacted "
        f"campaigns == v6 on net_r / gross_r / fee_r / funding_r / haircut_net_r / exit instant "
        f"/ exit_reason at 0.000e+00; {st['acted']} acted campaigns are warn exits strictly "
        f"before v6's exit, each with the C1 mark (full precision) == the rule book's net R "
        f"exactly, the written marks / forward legs their 6-dp image; RD identity "
        f"helper {ist}; the base arm == the v6 Trades and the filed v6 book sha "
        f"{man['book_sha']['v6'][:16]}…, and books/v6_campaigns.parquet on every shared "
        f"required column (floats at its 6 dp, exit_close_ms = the 4h exit-bar close); "
        f"P_WARN_1_COMPLEMENT (15 cells: n, net sums, delta, AM-7 haircut sums by the typed "
        f"tiers) re-derived from the two regbook parquets, equal (W2_FORWARD: F-W2-MARK)"))


# ═══════════════════════════════════════════════════════════════ F-GRID
def _verdict_words(d: pd.DataFrame) -> list:
    out = []
    for col in d.columns:
        if d[col].dtype == object:
            for v in d[col].dropna().unique():
                u = str(v).upper()
                for w in VERDICT_WORDS:
                    if re.search(rf"\b{w}\b", u):
                        out.append(f"{col}={str(v)[:60]!r} holds {w!r}")
    return out


def _json_words(x, path: str = "") -> list:
    """Verdict words in every string value of a JSON document (keys excluded)."""
    out = []
    if isinstance(x, dict):
        for k, v in x.items():
            out += _json_words(v, f"{path}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            out += _json_words(v, f"{path}[{i}]")
    elif isinstance(x, str):
        for w in VERDICT_WORDS:
            if re.search(rf"\b{w}\b", x.upper()):
                out.append(f"{path}={x[:60]!r} holds {w!r}")
    return out


def cond_collar_findings(cond: dict, tag: str = "GRID") -> list:
    """condition.json is the Tier-E condition block (L-W.4): the exact collar, no
    verdict word in any string value."""
    bad = []
    for k, v in COLLAR_TYPED.items():
        if cond.get(k) != v:
            bad.append(f"{tag} COLLAR condition.json: `{k}` is {str(cond.get(k))[:50]!r}, not "
                       f"{v!r}")
    vw = _json_words(cond)
    if vw:
        bad.append(f"{tag} VERDICT condition.json: a verdict word — {vw[:2]}")
    return bad


def grid_findings(frames: dict, tag: str = "GRID", cond: dict | None = None) -> tuple[list, list]:
    bad, lines = [], []
    bad += cond_collar_findings(reg_json("condition.json") if cond is None else cond, tag)
    for name, dec in DECLARED.items():
        d = frames[name]
        ok, ls = TP.grid_whole(dec, d, cell_col="cell", require_cols=tuple(COLLAR_TYPED),
                               label=name)
        lines.append(f"{name} {len(dec)}")
        if not ok:
            bad += [f"{tag} {x}" for x in ls if x.startswith("[BAD]")]
    for name, d in frames.items():
        for k, v in COLLAR_TYPED.items():
            if k not in d.columns or not bool((d[k] == v).all()):
                bad.append(f"{tag} COLLAR {name}: `{k}` is not {v!r} on every row")
        vc = [c for c in d.columns if c in VERDICT_COLS]
        if vc:
            bad.append(f"{tag} VERDICT {name}: verdict column(s) {vc}")
        vw = _verdict_words(d)
        if vw:
            bad.append(f"{tag} VERDICT {name}: a verdict word in a cell — {vw[:2]}")
        if "n" in d.columns and "nan_reason" in d.columns:
            stat = [c for c in ("mean_net_r", "p_win", "mean_fwd_r") if c in d.columns]
            for r in d.itertuples(index=False):
                zero = int(r.n) == 0
                nanall = all(not np.isfinite(float(getattr(r, s))) for s in stat)
                anynan = any(not np.isfinite(float(getattr(r, s))) for s in stat)
                if zero != bool(str(r.nan_reason)) or (zero and not nanall) or \
                        (not zero and anynan):
                    bad.append(f"{tag} NAN {name} {r.cell}: n {int(r.n)} with stats NaN "
                               f"{anynan} and nan_reason {str(r.nan_reason)!r}")
    for name, gcols in (("W2_COHORTS", ("cohort", "group")), ("W2_PREENTRY", ("event_class", "group")),
                        ("W2_FORWARD", ("cohort",)), ("P_WARN_1_COMPLEMENT", ("group",))):
        d = frames[name]
        for key, g in d.groupby(list(gcols)):
            n = {r.era: int(r.n) for r in g.itertuples(index=False)}
            if n.get("ALL") != n.get("tuning", 0) + n.get("holdout", 0):
                bad.append(f"{tag} ERA {name} {key}: ALL {n.get('ALL')} != tuning "
                           f"{n.get('tuning')} + holdout {n.get('holdout')}")
    so = frames["W1_OTHER_SUMMARY"]
    for key, g in so.groupby(["book", "kind", "event_class", "group"]):
        for col in ("n_campaigns", "n_events"):
            n = {r.era: int(getattr(r, col)) for r in g.itertuples(index=False)}
            if n.get("ALL") != n.get("tuning", 0) + n.get("holdout", 0):
                bad.append(f"{tag} ERA W1_OTHER_SUMMARY {key} {col}: ALL {n.get('ALL')} != "
                           f"tuning {n.get('tuning')} + holdout {n.get('holdout')}")
    rs, rh = frames["W2_RELAY_SUMMARY"], frames["W2_RELAY_HIST"]
    for pop in ("v6_campaigns", "armed_windows_not_entered"):
        nw = int(rs[rs["cell"] == f"{pop}|ALL|ALL"]["n_windows"].iloc[0])
        for m in ("lead_1h", "lead_4h"):
            tot = int(rh[(rh["population"] == pop) & (rh["metric"] == m)]["n"].sum())
            if tot != nw:
                bad.append(f"{tag} HIST {pop} {m}: bins sum {tot} != n_windows {nw}")
    return bad, lines


def _frames() -> dict:
    return {k: written(k) for k in KEYS_TYPED}


def grid_break():
    fr = _frames()

    def mod(name, fn):
        def thunk():
            f2 = {k: v.copy() for k, v in fr.items()}
            f2[name] = fn(f2[name])
            return grid_findings(f2)[0]
        return thunk

    def add_row(d):
        r = d.iloc[[0]].copy()
        r["cell"] = "C9_undeclared|cohort|ALL"
        return pd.concat([d, r], ignore_index=True)

    def silent_nan(d):
        d = d.copy()
        i = int(np.flatnonzero((d["n"] > 0).to_numpy())[0])
        d.loc[i, "mean_net_r"] = float("nan")
        return d

    def era_broken(d):
        d = d.copy()
        i = int(np.flatnonzero((d["era"] == "tuning").to_numpy())[0])
        d.loc[i, "n"] = int(d.loc[i, "n"]) + 1
        return d

    def word(d):
        d = d.copy()
        d.loc[0, "at_risk_set"] = "SUPPORTED at the family bar"
        return d

    def summary_era(d):
        d = d.copy()
        i = int(np.flatnonzero(((d["era"] == "holdout") & (d["kind"] == "events")
                                & (d["n_events"] > 0)).to_numpy())[0])
        d.loc[i, "n_events"] = int(d.loc[i, "n_events"]) - 1
        return d

    def cond_gates():
        cd = copy.deepcopy(reg_json("condition.json"))
        cd["gates"] = "only whether P-WARN-1 is scored"
        return grid_findings(fr, cond=cd)[0]

    return plants([
        ("a declared cell dropped", "missing", mod("W2_COHORTS", lambda d: d.iloc[1:])),
        ("condition.json's collar `gates` not 'nothing' (copy)", "COLLAR condition.json",
         cond_gates),
        ("an undeclared cell", "undeclared", mod("W2_COHORTS", add_row)),
        ("the collar removed", "COLLAR", mod("W2_FORWARD", lambda d: d.drop(columns=["gates"]))),
        ("a verdict column", "VERDICT", mod("P_WARN_1_COMPLEMENT",
                                            lambda d: d.assign(verdict="x"))),
        ("a verdict word in a cell", "VERDICT", mod("W2_COHORTS", word)),
        ("a silent NaN (n > 0, mean NaN)", "NAN", mod("W2_PREENTRY", silent_nan)),
        ("the era partition broken", "ERA", mod("W2_COHORTS", era_broken)),
        ("a W1_OTHER_SUMMARY declared cell dropped (copy)", "W1_OTHER_SUMMARY: declared",
         mod("W1_OTHER_SUMMARY", lambda d: d.iloc[1:])),
        ("W1_OTHER_SUMMARY's era partition broken (copy)", "ERA W1_OTHER_SUMMARY",
         mod("W1_OTHER_SUMMARY", summary_era)),
        ("the collar removed from W1_EVENTS_OTHER (copy)", "COLLAR W1_EVENTS_OTHER",
         mod("W1_EVENTS_OTHER", lambda d: d.drop(columns=["tier"]))),
        ("a verdict word in a W1_CAMPAIGNS_OTHER cell (copy)", "VERDICT W1_CAMPAIGNS_OTHER",
         mod("W1_CAMPAIGNS_OTHER", lambda d: d.assign(arm_kind="PASS at the bar"))),
    ])


def grid_real():
    fr = _frames()
    bad, lines = grid_findings(fr)
    return verdict(bad, (
        f"every Tier-E grid whole against its TYPED declared cells ({', '.join(lines)}); the "
        f"collar exact on every row of all {len(fr)} stage_w tables and on condition.json "
        f"(gates 'nothing'); no verdict column, no "
        f"verdict word; n == 0 <=> NaN stats + nan_reason; ALL = tuning + holdout in every "
        f"cohort / pre-entry / forward / complement group and in every W1_OTHER_SUMMARY "
        f"(book, kind, class, group) on n campaigns and n events; relay bins sum to each "
        f"population"))


# ═══════════════════════════════════════════════════════════════ F-KEY
def own_csv_sha(d: pd.DataFrame) -> str:
    """THE TYPED BOOK_SHA LAW, this file's code."""
    x = d.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(REQUIRED_T)
    for _, r in x.iterrows():
        row = []
        for c in REQUIRED_T:
            v = r[c]
            if REQ_DTYPES_T[c] == "float64":
                row.append(repr(float(v)))
            elif REQ_DTYPES_T[c] in ("int64", "int8"):
                row.append(str(int(v)))
            else:
                row.append(str(v))
        w.writerow(row)
    return hashlib.sha256(buf.getvalue().encode("utf-8")).hexdigest()


def reg_findings(arms: dict, tag: str = "KEY") -> list:
    """arms = {arm: (frame, sidecar)}."""
    bad = []
    for arm, (d, side) in arms.items():
        miss = [c for c in REQUIRED_T if c not in d.columns]
        if miss:
            bad.append(f"{tag} {arm}: required column(s) missing {miss}")
            continue
        for c, dt in REQ_DTYPES_T.items():
            if str(d[c].dtype) != dt:
                bad.append(f"{tag} {arm}: {c} dtype {d[c].dtype} != typed {dt}")
        nul = [c for c in REQUIRED_T if bool(d[c].isna().any())]
        if nul:
            bad.append(f"{tag} {arm}: null(s) in required column(s) {nul}")
        if int(d.duplicated(subset=["symbol", "entry_ms"]).sum()):
            bad.append(f"{tag} {arm}: duplicated (symbol, entry_ms)")
        srt = d.sort_values(["symbol", "entry_close_ms"], kind="mergesort")
        if not srt.index.equals(d.index):
            bad.append(f"{tag} {arm}: rows not in (symbol, entry_close_ms) order")
        if "exit_bar_open_ms" not in d.columns or not bool(
                (d["exit_close_ms"] == d["exit_bar_open_ms"] + H4).all()):
            bad.append(f"{tag} {arm}: exit_close_ms is not the 4h exit-bar close (the v6 "
                       f"schema)")
        if "exit_instant_ms" not in d.columns or not bool(
                ((d["exit_instant_ms"] > d["entry_close_ms"])
                 & (d["exit_instant_ms"] <= d["exit_close_ms"])).all()):
            bad.append(f"{tag} {arm}: exit_instant_ms not inside (entry close, exit-bar close]")
        if not bool((d["entry_close_ms"] == d["entry_ms"] + H4).all()):
            bad.append(f"{tag} {arm}: entry_close_ms != entry_ms + 4h on a v6-derived row")
        era = np.where(d["entry_close_ms"].to_numpy(np.int64) <= ERA_CUT, "tuning", "holdout")
        if not bool((d["era"].to_numpy() == era).all()):
            bad.append(f"{tag} {arm}: era is not the typed cut by the entry close")
        hc = d["net_r"] - d["fee_r"] * (d["symbol"].map(SLIP_T) / TAKER_T)
        if not bool((hc == d["haircut_net_r"]).all()):
            bad.append(f"{tag} {arm}: haircut_net_r is not AM-7's (typed tiers)")
        want = {"registration": "P-WARN-1", "arm": arm, "kind": KIND_T[arm], "ruler": "paired",
                "panel": list(CLASSIC5_TYPED), "era_scope": SCOPE_T[arm], "n": int(len(d)),
                "sum_net_r": float(d["net_r"].sum()), "book_sha256": own_csv_sha(d),
                "source_script": "scripts/tierc11_stage_w.py",
                # L-1.3: entry bars straddling the era cut (open <= cut < close), a count
                "n_entry_bar_straddles_era_cut": int(
                    ((d["entry_ms"].to_numpy(np.int64) <= ERA_CUT)
                     & (d["entry_close_ms"].to_numpy(np.int64) > ERA_CUT)).sum())}
        if KIND_T[arm] == "tierE":
            want.update({"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
                         "gates": "nothing"})
        for k in SIDECAR_KEYS_T:
            if k not in side:
                bad.append(f"{tag} SIDECAR {arm}: key {k!r} absent")
        for k, v in want.items():
            if side.get(k) != v:
                bad.append(f"{tag} SIDECAR {arm}: {k} = {str(side.get(k))[:40]!r}, typed / "
                           f"recomputed {str(v)[:40]!r}")
        if arm in ("tierE__tuning", "tierE__holdout"):
            if not bool((d["era"] == SCOPE_T[arm]).all()):
                bad.append(f"{tag} {arm}: a row outside its era scope")
    return bad


def table_haircut_findings(cw: pd.DataFrame, rw: pd.DataFrame, tag: str = "KEY") -> list:
    """AM-7 beside every per-campaign net R (w11): W1_CAMPAIGNS fee_r / haircut_net_r
    (v6) and rule_fee_r / rule_haircut_net_r (the rule book), W2_RELAY_WINDOWS
    haircut_net_r — each the 6-dp image of the TYPED law on the regbook rows."""
    bad = []
    st = reg_json("STATUS.json")["status"]
    rp = reg_parquet(ARMS_T[st][0]).set_index(["symbol", "entry_ms"])
    bp = reg_parquet("base").set_index(["symbol", "entry_ms"])

    def law(x, sym):
        return float(x["net_r"]) - float(x["fee_r"]) * (SLIP_T[sym] / TAKER_T)
    for r in cw.itertuples(index=False):
        k = (r.symbol, int(r.entry_ms))
        b, q = bp.loc[k], rp.loc[k]
        for col, v in (("fee_r", float(b["fee_r"])), ("haircut_net_r", law(b, r.symbol)),
                       ("rule_fee_r", float(q["fee_r"])),
                       ("rule_haircut_net_r", law(q, r.symbol))):
            if float(getattr(r, col)) != float(np.round(v, 6)):
                bad.append(f"{tag} W1-HAIRCUT {r.symbol} {iso(k[1])}: {col} "
                           f"{float(getattr(r, col))!r} != the 6-dp image of the typed law "
                           f"{v!r}")
    for r in rw.itertuples(index=False):
        k = (r.symbol, int(r.entry_ms))
        v = law(bp.loc[k], r.symbol)
        if float(r.haircut_net_r) != float(np.round(v, 6)):
            bad.append(f"{tag} RELAY-HAIRCUT {r.symbol} {iso(k[1])}: haircut_net_r "
                       f"{float(r.haircut_net_r)!r} != {v!r} at 6 dp")
    return bad


def other_value_findings(co: pd.DataFrame, tag: str = "KEY") -> list:
    """W1_CAMPAIGNS_OTHER's carried book values (w12): net_r, fee_r and haircut_net_r
    are the 6-dp image of the source book's own (P-BRK-4H / P-RELAY-1: the regbook's
    columns; the 9/12 book: its Trades, the haircut by the TYPED AM-7 law); era by
    the typed cut on the entry close; one row per source campaign."""
    bad = []
    src = other_src()
    want = {(bk, x["symbol"], x["entry_close"]): x for bk in OTHER_BOOKS_T for x in src[bk]}
    got = {(r.book, r.symbol, int(r.entry_close_ms)): r for r in co.itertuples(index=False)}
    if set(got) != set(want) or len(co) != len(want):
        bad.append(f"{tag} W1-OTHER: rows {len(co)} / keys differ from the {len(want)} source "
                   f"campaigns")
    for k in sorted(set(got) & set(want)):
        r, x = got[k], want[k]
        for col, v in (("net_r", x["net_r"]), ("fee_r", x["fee_r"]),
                       ("haircut_net_r", x["haircut"])):
            if float(getattr(r, col)) != float(np.round(v, 6)):
                bad.append(f"{tag} W1-OTHER {k[0]} {k[1]} {iso(k[2])}: {col} "
                           f"{float(getattr(r, col))!r} != the 6-dp image of the book's "
                           f"{v!r}")
        era = "tuning" if k[2] <= ERA_CUT else "holdout"
        if r.era != era:
            bad.append(f"{tag} W1-OTHER {k[0]} {k[1]} {iso(k[2])}: era {r.era!r} != typed {era!r}")
    return bad


def _arms_written() -> dict:
    status = reg_json("STATUS.json")
    return {a: (reg_parquet(a), reg_json(f"{a}.json")) for a in ARMS_T[status["status"]]}


def key_break():
    A = _arms_written()
    arm0 = next(iter(A))

    def edit(fn):
        def thunk():
            a2 = {k: (v[0].copy(), dict(v[1])) for k, v in A.items()}
            a2[arm0] = fn(*a2[arm0])
            return reg_findings(a2)
        return thunk

    def dup(d, s):
        return pd.concat([d, d.iloc[[0]]]).sort_values(["symbol", "entry_close_ms"],
                                                        kind="mergesort"), s

    def nulled(d, s):
        d = d.copy()
        d.loc[3, "net_r"] = np.nan
        return d, s

    def moved(d, s):
        d = d.copy()
        d.loc[5, "gross_r"] = float(d.loc[5, "gross_r"]) + 1e-9
        return d, s

    def tier_dir():
        root = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            src = OUT / "W2_COHORTS.parquet"
            d = pd.read_parquet(str(src))
            pd.concat([d, d.iloc[[0]]]).to_parquet(str(root / "W2_COHORTS.parquet"), index=False)
            ok, ls = TP.check_keys(root, {"keys": {"W2_COHORTS": ["cell"]}})
            return [] if ok else [f"KEY check_keys: {x}" for x in ls if x.startswith("[BAD]")]
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def collarless():
        a2 = {k: (v[0], dict(v[1])) for k, v in A.items()}
        a2["tierE__tuning"][1].pop("selection_not_a_result")
        return reg_findings(a2)

    def straddle_bent():
        a2 = {k: (v[0], dict(v[1])) for k, v in A.items()}
        a2["base"][1]["n_entry_bar_straddles_era_cut"] = 1
        return reg_findings(a2)

    def other_haircut_moved():
        co = written("W1_CAMPAIGNS_OTHER")
        i = int(np.flatnonzero((co["book"] == "P-BRK-4H").to_numpy())[0])
        co.loc[i, "haircut_net_r"] = float(co.loc[i, "haircut_net_r"]) + 1e-3
        return other_value_findings(co)

    def other_dup_key():
        root = Path(tempfile.mkdtemp(prefix="f-key-"))
        try:
            d = pd.read_parquet(str(OUT / "W1_EVENTS_OTHER.parquet"))
            pd.concat([d, d.iloc[[5]]]).to_parquet(str(root / "W1_EVENTS_OTHER.parquet"),
                                                   index=False)
            ok, ls = TP.check_keys(root, {"keys": {"W1_EVENTS_OTHER":
                                                   KEYS_TYPED["W1_EVENTS_OTHER"]}})
            return [] if ok else [f"KEY check_keys: {x}" for x in ls if x.startswith("[BAD]")]
        finally:
            shutil.rmtree(root, ignore_errors=True)

    def haircut_moved():
        cw = written("W1_CAMPAIGNS")
        cw.loc[7, "rule_haircut_net_r"] = float(cw.loc[7, "rule_haircut_net_r"]) + 1e-3
        return table_haircut_findings(cw, written("W2_RELAY_WINDOWS"))

    return plants([
        ("a duplicated row", "duplicated (symbol, entry_ms)", edit(dup)),
        ("a sidecar's L-1.3 straddle count bent (copy)", "n_entry_bar_straddles_era_cut",
         straddle_bent),
        ("a W1_CAMPAIGNS AM-7 haircut moved 1e-3 (copy)", "KEY W1-HAIRCUT", haircut_moved),
        ("a nulled net_r", "null(s) in required", edit(nulled)),
        ("a required column dropped", "required column(s) missing",
         edit(lambda d, s: (d.drop(columns=["haircut_net_r"]), s))),
        ("a float moved behind the sidecar's sha", "SIDECAR", edit(moved)),
        ("TP.check_keys on a temp root holding a duplicated row", "KEY check_keys", tier_dir),
        ("a tierE sidecar without its collar", "SIDECAR tierE__tuning", collarless),
        ("a W1_CAMPAIGNS_OTHER P-BRK-4H haircut moved 1e-3 (copy)", "KEY W1-OTHER",
         other_haircut_moved),
        ("TP.check_keys on a temp root holding a duplicated W1_EVENTS_OTHER row",
         "KEY check_keys: [BAD] unique keys", other_dup_key),
    ])


def key_real():
    A = _arms_written()
    bad = reg_findings(A)
    man = json.loads((OUT / "MANIFEST_STAGE_W.json").read_text(encoding="utf-8"))
    if man.get("keys") != KEYS_TYPED:
        bad.append(f"KEY manifest keys {man.get('keys')} != typed")
    ok, ls = TP.check_keys(OUT, man)
    if not ok:
        bad += [f"KEY check_keys: {x}" for x in ls if x.startswith("[BAD]")]
    for name, key in KEYS_TYPED.items():
        d = written(name)
        if int(d.duplicated(subset=key).sum()) or bool(d[key].isna().any().any()):
            bad.append(f"KEY {name}: duplicated or null key {key}")
        if TB._content_sha(d) != man["sha"].get(name):
            bad.append(f"KEY {name}: manifest content sha is not the table's")
    bad += table_haircut_findings(written("W1_CAMPAIGNS"), written("W2_RELAY_WINDOWS"))
    bad += other_value_findings(written("W1_CAMPAIGNS_OTHER"))
    cond = reg_json("condition.json")
    miss = [k for k in COND_KEYS_T if k not in cond]
    if miss:
        bad.append(f"KEY condition.json lacks {miss}")
    arms_line = "; ".join(f"{a} n {s['n']} ΣR {s['sum_net_r']:+.6f} sha {s['book_sha256'][:12]}… "
                          f"straddle {s['n_entry_bar_straddles_era_cut']}"
                          for a, (d, s) in A.items())
    return verdict(bad, (
        f"regbooks: {len(A)} arms, every required column typed / non-null, unique keys in "
        f"(symbol, entry_close_ms) order, era by the typed cut, AM-7 haircut by the typed "
        f"tiers, sidecars == this file's recomputation incl. the L-1.3 straddle count "
        f"({arms_line}); W1_CAMPAIGNS fee / AM-7 haircut columns (v6 and rule) and "
        f"W2_RELAY_WINDOWS haircut == the 6-dp image of the typed law on the regbook rows; "
        f"W1_CAMPAIGNS_OTHER: one row per source campaign of the three other books, net_r / "
        f"fee_r / haircut_net_r the 6-dp image of each book's own (the 9/12 haircut by the "
        f"typed law), era by the typed cut; stage_w: "
        f"{len(KEYS_TYPED)} tables with the typed keys, TP.check_keys "
        f"{' · '.join(ls)}; manifest content shas == the tables; condition.json carries "
        f"{len(COND_KEYS_T)} typed keys"))


# ═══════════════════════════════════════════════════════════════ F-DET
def _files_of(stage: Path, reg: Path) -> dict:
    out = {}
    for p in sorted(stage.iterdir()) if stage.exists() else []:
        if p.is_file() and p.name in STAGE_FILES_TYPED:
            out[f"stage_w/{p.name}"] = p.read_bytes()
    for p in sorted(reg.iterdir()) if reg.exists() else []:
        if p.is_file():
            out[f"regbooks/P-WARN-1/{p.name}"] = p.read_bytes()
    return out


def _typed_reg_files() -> list:
    st = reg_json("STATUS.json")["status"]
    return sorted([f"regbooks/P-WARN-1/{a}.{x}" for a in ARMS_T[st] for x in ("parquet", "json")]
                  + ["regbooks/P-WARN-1/STATUS.json", "regbooks/P-WARN-1/condition.json"])


def det_findings(a: tuple, b: tuple, canon: dict) -> list:
    out = []
    typed = sorted([f"stage_w/{x}" for x in STAGE_FILES_TYPED] + _typed_reg_files())
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("canonical", canon)):
        if sorted(x) != typed:
            out.append(f"{lab}: file set {len(x)} != typed {len(typed)} "
                       f"({sorted(set(x) ^ set(typed))[:3]})")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs canonical", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                out.append(f"{lab}: {name} bytes differ")
            if name.endswith(".parquet"):
                ca = TB._content_sha(pd.read_parquet(io.BytesIO(x[name])))
                cb = TB._content_sha(pd.read_parquet(io.BytesIO(y[name])))
                if ca != cb:
                    out.append(f"{lab}: {name} content sha {ca[:12]}… != {cb[:12]}…")
    return out


def det_dir() -> Path:
    return RUN_ROOT / S.DET_ROOT.name


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_stage_w.py"), f"--out-dir={d}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path.insert(0, {str(ROOT)!r})\n"
                f"sys.path.insert(0, {str(ROOT / 'scripts')!r})\n"
                f"from pathlib import Path\nimport tierc11_stage_w as S\n"
                f"d = Path({str(d)!r})\nS.build(d)\n"
                f"p = d / S.REPORT\n"
                f"p.write_text(p.read_text() + 'set order: ' + ','.join(set(S.E.PANEL17)) "
                f"+ '\\n')\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT),
                       timeout=3600)
    if r.returncode != 0:
        clock(f"det build {d.name} exit {r.returncode}: {r.stderr[-400:]}")
    return r.returncode, (_files_of(d, d / "regbooks" / "P-WARN-1") if d.exists() else {})


def _canon() -> dict:
    return _files_of(OUT, REG_DIR)


def det_break():
    canon = _canon()
    bent = dict(canon)
    md = bytearray(bent["stage_w/STAGE_W.md"])
    md[len(md) // 2] ^= 0x01
    bent["stage_w/STAGE_W.md"] = bytes(md)

    def float_moved():
        name = "regbooks/P-WARN-1/base.parquet"
        d = pd.read_parquet(io.BytesIO(canon[name]))
        d.loc[d.index[0], "net_r"] = float(d["net_r"].iloc[0]) + 1e-6
        buf = io.BytesIO()
        d.to_parquet(buf, index=False)
        c2 = dict(canon)
        c2[name] = buf.getvalue()
        return det_findings((0, c2), (0, c2), canon)

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of STAGE_W.md", "STAGE_W.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("one net_r moved 1e-6 in a regbook parquet copy", "base.parquet content sha",
         float_moved),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: stage_w/STAGE_W.md bytes differ", hashorder),
    ])


def det_real():
    canon = _canon()
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    return verdict(bad, (
        f"exit {a[0]}/{b[0]}; file set == the typed {len(canon)} files (stage_w "
        f"{len(STAGE_FILES_TYPED)} + regbooks {len(_typed_reg_files())}) in both builds and "
        f"in the record; every file byte-identical seed 1 == seed {SEED} == canonical; every "
        f"parquet content sha equal"))


FIXTURES = (
    ("F-WARN-ASOF", "only 1h bars CLOSED by the 4h instant are visible; the event tape is "
     "causal; the in-trade window ends at the 1h-RESOLVED exit [L-W.1, L-W.2, L-W.3]",
     "a W1 event visible at a 4h close other than the first >= its 1h close, a W1_TIMELINE "
     "row set / class count / in-trade pre-+1R counter 12/89 count / stage that is not this "
     "file's hand walk at close <= T, a prefix event tape that differs from the whole tape at "
     "close <= T on any cut, an IN-TRADE event not strictly before the hand-walked 1h exit, "
     "or the planted post-stop-child counter 12/89 cross not POST-EXIT / in cohort C1",
     asof_break, asof_real),
    ("F-WARN-COHORT", "the P-WARN-1 condition cohort is the rule book's warn-exit set; the "
     "condition numbers re-derive by the typed law [L-W.4, L-W.5]",
     "condition cohort keys != warn-exit keys + listed mismatch-bar keys, or != the "
     "W1_CAMPAIGNS C1 set, or any of cohort n / means / delta / cluster-90% lo, hi (seed "
     "20260924 and 20260816) / MET differs from this file's recomputation, or "
     "cohort_law_holds / the belltie list is not the frozen law evaluated here, or the "
     "STATUS / arm set is not the typed one",
     cohort_break, cohort_real),
    ("F-W2-HAND", "every campaign's 1h event classification hand-walked from raw bars by a "
     "plain loop; W2 and the relay (v6 windows and the twin) re-derived; the mismatch-bar law "
     "planted on every eligible bar [L-W.0..L-W.4, L-W.6, w1, w7, w10]",
     "on any of the 200 v6 campaigns a W1 event row or W1_CAMPAIGNS fact differs from this "
     "file's hand walk; a W2_COHORTS / W2_PREENTRY count or sum, a W2_RELAY_SUMMARY cell "
     "(counts, share, six lead statistics per lens) or a W2_RELAY_HIST bin differs from this "
     "file's hand-walked leads; a W2_RELAY_WINDOWS_TWIN row differs from this file's hand walk "
     "of the twin population; or, under ANY planted mismatch bar (every C1 first-event bar, "
     "latch bar and stop-exit bar holding a W1 event), the module's re-ride / event tape is "
     "not the law's",
     hand_break, hand_real),
    ("F-W1-OTHER", "the Tier-E W1 stamps of the OTHER 4h books (the 9/12 book, P-BRK-4H "
     "scored, P-RELAY-1 scored): every campaign hand-walked from raw bars by a plain loop "
     "[L-W.0..L-W.3, w12..w14; final-review fidelity MINOR-1]",
     "on any campaign of the three books (every one, the typed n per book, at least 20) a "
     "W1_EVENTS_OTHER row or W1_CAMPAIGNS_OTHER fact (window open, 1h-resolved exit and its "
     "resolver, both +1R latch readings, memberships, counts, first events) differs from "
     "this file's hand walk; an event is visible at a 4h close other than the first >= its "
     "1h close; a relay's hand-walked exit / L-W.5 latch differs from its regbook of "
     "record; any W1_OTHER_SUMMARY cell differs from its re-derivation from the hand walk; "
     "a fallback row is off the typed 4h-close law, carries no reason, or claims a walk "
     "HALT where the raw 1h bars resolve the exit; a row resolved on 1h where they cannot",
     other_break, other_real),
    ("F-W2-MARK", "the forward leg priced independently: every cohort member's mark by this "
     "file's typed account law; C1 by the rule book, C2 by a 12/26 warn ride [L-W.4, w5]",
     "any member's module mark != this file's own price of its first event exactly, a C1 mark "
     "!= the rule book's net R, a C2 mark != the 12/26 warn ride's net R (or that ride warns a "
     "non-member away from its exit instant), or a written mark / forward leg / W2_FORWARD "
     "cell differs from its re-derivation from the own marks",
     mark_break, mark_real),
    ("F-IDENTITY", "the paired premise and the identity law on the rule book [L-1.5, L-W.5]",
     "key sets differ or n != 200; an unacted campaign differs from v6 on net_r / gross_r / "
     "fee_r / funding_r / haircut_net_r / exit instant / exit_reason by any amount; an acted "
     "campaign is not a warn exit before v6's; the base arm is not the v6 book (Trades, "
     "filed sha, books/v6_campaigns.parquet at 6 dp); the C1 mark is not the rule book's net "
     "R exactly; or P_WARN_1_COMPLEMENT (net and haircut sums) differs from its re-derivation",
     ident_break, ident_real),
    ("F-GRID", "every Tier-E grid whole, collared, verdict-free [L-1.4]",
     "a Tier-E table's cells are not the typed declared set (W1_OTHER_SUMMARY's 522 "
     "included), a row of any of the 14 stage_w tables (or condition.json) lacks the exact "
     "collar, a verdict column or word appears, n == 0 does not coincide with NaN stats + "
     "nan_reason, an era split is not a partition (W1_OTHER_SUMMARY on n campaigns and n "
     "events), or a relay histogram does not sum to its population",
     grid_break, grid_real),
    ("F-KEY", "unique keys, no nulls in required columns, the regbook interface exact",
     "a duplicated key, a null or missing required column, a wrong dtype, rows out of order, "
     "an era, haircut or exit_close_ms off the typed law, a sidecar n / sum / sha / kind / "
     "ruler / collar / straddle count that is not this file's recomputation, a W1_CAMPAIGNS / "
     "W2_RELAY_WINDOWS fee or haircut column off the typed law, a W1_CAMPAIGNS_OTHER row set "
     "/ net_r / fee_r / haircut / era off its source book, TP.check_keys RED (the three "
     "other-book tables' typed keys included), or a manifest content sha that is not the "
     "table's",
     key_break, key_real),
    ("F-DET", "two subprocess builds under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 builds (under RUN_ROOT/_det_stage_w) differ from each "
     "other or from the canonical stage_w/ (the three other-book W1 tables included) + "
     "regbooks/P-WARN-1/ files in the file set, any byte or any parquet content sha, or "
     "either exits nonzero",
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
    say("TIER-C11 STAGE W FIXTURES — scripts/tierc11_stage_w.py (the 1h event tape, W2, "
        "P-WARN-1) — break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} · substrate {TC11_SNAP.name} · pin {PIN} · n_boot {N_BOOT}")
    for ln in S.READINGS:
        say(ln)
    for fid, title, fails_if, b, r in FIXTURES:
        if not pick or any(q in fid.lower() for q in pick):
            t1 = time.time()
            prove(fid, title, fails_if, b, r)
            clock(f"{fid} {time.time() - t1:.1f}s")
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
