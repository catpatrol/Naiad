#!/usr/bin/env python
"""TIER-C11 · TC11-SCORE — F-SCORE-REG · F-RULER · F-BOOT · F-VERDICT · F-STATUS ·
F-COLLAR · F-BASE-IDENT · F-GRID · F-KEY · F-CLOSURE · F-DRYRUN · F-EXIT · F-S0-TEXT ·
F-REPORT · F-DET.
REPAIRED 2026-09-25 per VERIFY TC11-SCORE (MAJOR-1/2, m-1..m-14, f-1..f-6), and per the
final review G2 (statistics MINOR-1..4, reproducibility MINOR-2, fidelity MINOR-4: F-EXIT
runs main() itself; F-S0-TEXT and F-REPORT are new).  The fixtures of
scripts/tierc11_score.py (the scorer of the nine) [LEANS L-1.4, L-1.5, L-1.3, L-S.1,
L-W.4, AM-3, AM-7].

TWO LEGS PER FIXTURE, the BREAK leg first, and it must go RED or the fixture is VOID
[the prove() law of scripts/tierc10_rf_fixtures.py / tierc10_resume_fixtures.py; the
worked example scripts/tierc11_books_fixtures.py].  A break leg is a set of PLANTS
judged one at a time; a plant counts as CAUGHT only if a finding NAMES THE INTENDED
DETECTOR (its expected substring).  A plant that crashes is a FIXTURE DEFECT, never a
catch.  Every plant is made on a COPY (a dict, a frame, a temp regbooks root) or under a
MUTATION of the module restored in `finally`; no artifact of record moves.

THE REGBOOKS ON TRIAL ARE PLANTED — synthetic books written by THIS file under
RUN_ROOT/_det_score/planted_regbooks/ (gitignored `_det_*`): the base arm of every
registration is books/v6_campaigns.parquet in the regbook schema (the frozen control,
already published in BOOKS.md), and every scored / Tier-E arm is a SYNTHETIC transform
of it (a typed per-campaign delta, a typed index filter) or a synthetic lane drawn from
a seeded normal.  No registered rule is computed here; no number in this transcript is
a registration's result.  The planted family covers every branch of the verdict law:
  P-WARN-1  CONDITION_NOT_MET (its rule book printed only as a collared Tier-E row); its
            condition.json says met False (ci_hi >= 0); acted_by on every 9th campaign
  P-AGE-1   two-sample gate, refused cohort mean > 0 (the 'forfeits' appendix), pre_seen
  P-WIN-1   two-sample gate, refused cohort mean < 0, selection_hazard; a holdout-scoped
            two-sample Tier-E arm (SC-3)
  P-BRK-4H  vs zero lane (+ a GARBAGE base arm the ruler must ignore), selection_hazard,
            SCALE-IN-SAMPLE, a 17-asset Tier-E view (LOAO bar 9/17; PUMP / HYPE 4h picks
            fell back to the whole tape); one BTC campaign whose 4h entry bar STRADDLES the
            era cut (open 2024-06-30T20:00Z, close 2024-07-01T00:00Z); die_close_ms carried
  P-RELAY-1 two-sample, its own entry keys
  P-SCALP-2 CLOSED_BY_PRECONDITION (the R2 record's 1h word is FAIL)
  P-ADD-BRK paired, ci_lo > 0 but p > 0.10/9 — the named F-VERDICT case (NOT SUPPORTED);
            a head-to-head Tier-E arm ruled against P-ADD-SFP/scored (base_arm)
  P-ADD-SFP paired, SUPPORTED; no head-to-head filed (the scorer derives one, SC-18)
  P-TP-RNG  paired, CI wholly below zero; every 4th campaign unacted (identity law); no
            frozen twin filed (ABSENT printed)
The referees are typed HERE (a second object): the contract sha, the registry head, the
nine ids and their rulers / eras (the L-1.4 table), the bar 1/90, the p law, the 16
required columns, the collar, the verdict-word pattern, the base-ident columns, the
typed verdict cases.  Hand computations use this file's own loops.

  F-SCORE-REG  FAILS IF the real REGISTRATIONS.json does not verify (contract sha typed
               bb38e016…, 9 slices re-cut by THIS file equal the texts, 9 payload shas
               recomputed by THIS file's law, the chain re-walked by THIS file ending at
               the typed head 6772568b… == REGISTRY_PIN.json), or the scorer's verifier
               reports anything on it.  SABOTAGE (copies): a text character; a payload
               field; a chain line's prev; a line_sha256; the pin head; a contract byte;
               a dropped registration; family_m 8; a tampered file in a temp root (the
               scorer must HALT before scoring).
  F-RULER      FAILS IF a registration's ruler / era is not the typed L-1.4 table; on
               ANY of the 4 paired registrations a book with one key moved, one row
               dropped, an unacted row off the base or acted_by dropped is scored (no
               'paired premise failed' / IDENTITY-LAW HALT); a two-sample on identical
               key sets is not flagged on any of the 3 (or a planted one is); the vs-zero
               row changes when its base arm is removed; a BUILT paired row is not n ==
               n_base == 200 with point == this file's delta mean keyed (symbol, entry_ms)
               and the unacted count == this file's; a gate holding a new campaign or a
               changed kept row is scored (either gate); a Tier-E arm scoped to the
               holdout is not ruled against the base's holdout rows (SC-3; a paired and a
               two-sample arm).  SABOTAGE: the premise check disabled; the identity law
               disabled; the two-sample / vs-zero rulers re-read (RULER-TABLE); the
               identical-key flag suppressed; the vs-zero row reading its base; the
               pairing key WITH lane; the gate check disabled; the Tier-E base not
               restricted; corrupted input handed to the scorer.
  F-BOOT       FAILS IF, at a small B and at B 4000, for every ruler on planted books,
               the scorer's point / CI / p / deciding bound differ by ANY amount from
               this file's hand computation with the same rng draws (asset clusters,
               np.random.default_rng(seed).choice), the typed p law (#<=0 + 1)/(B+1),
               the 5th/95th percentile, the typed deciding rank floor((B+1)/90); or its
               LOAO per-panel intervals differ from TP.loao_n (lanes unified) at 6 dp.
               SABOTAGE: the p law bent to #<0/B; the CI bent to 2.5/97.5; the seed of
               record bent to 20260921; the draw unit bent from assets to rows.
  F-VERDICT    FAILS IF any typed case (lo, hi, p) reads other than typed (incl. ci_lo >
               0 with p = 0.03 -> NOT SUPPORTED; p = 44/4001 -> SUPPORTED; 45/4001 -> NOT;
               lo = 0 -> NOT; hi < 0 -> '— CI wholly below zero'); the planted P-ADD-BRK
               (lo > 0, p > bar) does not read NOT SUPPORTED, P-ADD-SFP SUPPORTED,
               P-TP-RNG '— CI wholly below zero'; a label (pre_seen / selection_hazard /
               SCALE-IN-SAMPLE / the gate appendix) is missing where the spec asks or
               present where it does not; a CLOSED / NOT MET row prints a number, spends
               a test or lacks 'no slot spent'; FAMILY is not m 9 / bar 0.011111 / 7
               tests spent; an add row's AM-3 beside-print (sum delta, sum add_r, the
               absorbed funding) differs from this file's sums or a non-add row carries
               one; a SCALE-IN-SAMPLE row's holdout slice n / point differs from this
               file's era=='holdout' (by close) ruling, its frozen twin is not the typed
               arm with this file's n / point (or ABSENT where none is filed), its pick
               stability does not flag EXACTLY the typed changes at its typed lens (1h
               BTC SOL NEAR · 4h NEAR · 12h BTC ETH SOL; re-read from SCALE_PICKS.json and
               required equal) on the §0 cell and on every consuming Tier-E row, its
               in-sample holdout count differs from this file's, the 17-asset view lacks
               the IN-SAMPLE fallback label (HYPE, PUMP 4h) or a CLASSIC5 row carries
               one; the sensitivity-seed verdict is not ruled on the sensitivity seed's
               draws (a harness T5 drawing +1 / -1 by seed, 3 rulers).  SABOTAGE: a
               CI-only verdict; the bar loosened to 0.10/7; a closed row printing a
               number; the honesty label dropped; the AM-3 print dropped; the SCALE
               holdout slice on the tuning era; the frozen twin dropped; the stability
               flag dropped; P-TP-RNG's lens read as 4h; the fallback label dropped; the
               sensitivity seed collapsed onto the seed of record.
  F-STATUS     FAILS IF CLOSED_BY_PRECONDITION / CONDITION_NOT_MET on any of the 8
               registrations without that precondition / condition is not HALTed
               (STATUS-ILLEGAL, 16 cases); P-WARN-1's word disagreeing with condition.json
               (BUILT vs met False; NOT MET vs met True; met False with ci_hi < 0; the
               record absent) is not HALTed; P-SCALP-2's word disagreeing with the R2 1h
               lens word of record (BUILT vs FAIL; CLOSED vs PASS; no readable record) is
               not HALTed; P-SCALP-2's cell lacks the tuning-era R2 1h word (typed FAIL,
               re-read) beside it, collared [§10].  SABOTAGE: each of the four guards /
               prints removed.
  F-COLLAR     FAILS IF a Tier-E row lacks tier 'TIER-E' / selection_not_a_result 'a
               SELECTION, not a result' / gates 'nothing', carries a verdict word or a
               verdict / clears_bar / spent_test field, its would_read_ci_only is not the
               reading of its own interval, the Tier-E rows are not the typed declared
               set, or a Tier-E line of S0_VERDICTS.md lacks the collar.  SABOTAGE
               (copies, judged by this file AND by the scorer's own guard): a verdict
               word; the collar dropped; gates re-worded; would_read_ci_only = a verdict;
               the module's row builder dropping the collar; a Tier-E sidecar without it.
  F-BASE-IDENT FAILS IF the seven base arms do not carry one book_sha256, differ from
               books/v6_campaigns.parquet on the 13 typed columns at 6 dp (this file's
               own join), the scorer's record says otherwise, or any planted arm's
               book_sha256 by the scorer's canonical CSV differs from this file's pandas
               to_csv route.  SABOTAGE: one base net_r +1e-6; one base row dropped; every
               base's exit_close_ms moved (1h-resolved style); a sidecar claiming a wrong
               sha; a registration whose base differs must HALT its row.
  F-GRID       FAILS IF the §0 table, FAMILY, the Tier-E table or a LOAO grid is not
               WHOLE against its typed declared cells (TP.grid_whole).  SABOTAGE: a row
               dropped, duplicated, undeclared.
  F-KEY        FAILS IF a planted arm fails the interface or a corrupted one passes; the
               planted straddle (entry bar open tuning, close holdout) does not read
               'holdout' or is not counted 1 in P-BRK-4H/scored; the score rows' keys are
               not unique or a required field is null.  SABOTAGE: the era judged by the
               OPEN; a duplicated key, a null net_r, a dropped column, an era flipped, a
               direction 0, the haircut law broken, float32 net_r, a sidecar n / sum /
               era_scope, an entry bar longer than 4h, an exit before the entry, r_dist 0,
               a ',' in a string, int64 direction, int32 exit_close_ms, a stray asset.
  F-CLOSURE    FAILS IF a fresh interpreter importing tierc11_score loads a range /
               census / stamps / null / nest module, or its source holds a static import
               of one or an I/O escape the audit hook cannot see (E.hook_escapes).
               SABOTAGE: planted sources with a census import, a lazy nest import, a
               subprocess import.
  F-DRYRUN     FAILS IF the dry run (scripts/tierc11_score.py --dry-run) calls a ruler
               (ruled / stats_block / loao tripwired), prints an interval, a p, LOAO or a
               verdict token, leaves an arm line without '(book, not a verdict)', does not
               print the nine registrations in the typed order, prints book facts other
               than this file's, its last line is not 'EXIT 0 = 0 (no condition)' on the
               planted family, or lets a corrupted input through.  SABOTAGE: its facts
               calling a ruler; its facts printing an interval; a paired key moved; an
               unacted campaign moved (identity law); a kept gate row changed; the
               condition record flipped.
  F-EXIT       FAILS IF any of the 16 subsets of (registered HALT, Tier-E halted, ABSENT,
               no-clobber) exits other than the OR of the typed bits 2 / 4 / 8 / 16 with
               the typed EXIT line, or the dry run on a family with all three row
               conditions does not exit 14, or S.main([...]) run against an out-dir
               holding a BENT record does not return (the process exit code) 16 with the
               typed 'EXIT 16 = 16 (a no-clobber refusal)' line, leave the bent record
               untouched and file the run as FAMILY_rerun.json, or does not return 0 on
               the clean record (score_all stubbed to the memoized planted result; the
               stub asserts main parsed and passed its argv) [reproducibility MINOR-2], or
               `python scripts/tierc11_score.py` run in a SUBPROCESS (unstubbed, the
               planted regbooks) against an out-dir holding a bent FAMILY.json does not
               EXIT 16 — the PROCESS exit code — with the typed EXIT 16 line last, the bent
               record untouched and the run filed as FAMILY_rerun.json [TC11-FIX verify
               MINOR-1].  SABOTAGE: the old masking precedence law; a registered HALT
               dropped from the word; the bits permuted; main mutated to `return
               exit_code(res)` (it prints EXIT 16 but returns 0); a copy of the script whose
               __main__ calls main(...) without sys.exit (the process exits 0).
  F-S0-TEXT    FAILS IF a detail block's status line is not 'status: <word> — builder's
               stage status: <the STATUS.json reason>' or a closed row's §0 cell lacks
               '(builder's stage status: <reason>)' [SC-20]; P-AGE-1's (pre_seen) §0 cell
               lacks '; point known before filing; new campaigns since 2026-09-21T16:00Z:
               scored <n> / base <n>)' inside its pre_seen label with THIS file's counts
               (entry CLOSE > the typed TC10 pin) — on the planted family AND on a copy
               whose P-AGE-1 books were moved so the typed counts are scored 3 / base 4
               (a campaign closing AT the pin, one opening at it, one refused) — or another
               row carries those facts [SC-21]; a two-sample / vs-zero §0 D15 cell is not
               exactly 'D15 n/a (two-sample)' / 'D15 n/a (vs zero)' + this file's own
               concentration (top trade by |net_r|, its share of ΣR, the point without it
               removed from every book holding its key, the point without its asset and
               that asset's share, per-asset Δ / mean), or a paired cell is not T5.d15's
               [SC-22].  SABOTAGE: the builder label dropped; the pre_seen facts dropped;
               the count by the entry OPEN; a campaign closing AT the pin counted new; the
               pre-G2 paired D15 cell on unpaired rows; the top trade removed from the
               scored book only; the base ignored in the concentration points.
  F-REPORT     FAILS IF research_outputs/tierc11/scores/STAGE_SCORE.md lacks, in its first
               12 lines, the typed pointer to S0_VERDICTS.md as the record, still says it
               'computes no registered result', or its planted section holds a table row
               whose verdict cell (§0 verdict / Family verdict_of_record / Tier-E
               would_read_ci_only) does not start 'PLANTED · ', a (NOT) SUPPORTED not
               preceded by 'PLANTED · ', or a planted table that is not (tag removed) the
               planted run's own S0_VERDICTS.md table [statistics MINOR-4], or it prints a
               LEANS_AMENDMENTS.md sha that is not the file's own (THIS file's hash) outside
               a section whose heading carries 'HISTORICAL' [TC11-FIX verify MINOR-11].
               SABOTAGE (copies of the text): a §0 tag stripped; a Family tag stripped; the
               pointer removed; the stale line restored; a §0 cell reverted to the pre-G2
               render; an old amendments sha injected under the Files heading; the
               HISTORICAL label struck from the sections that print an old amendments sha.
  F-DET        FAILS IF two subprocess scorer runs on the planted regbooks (PYTHONHASHSEED
               1, 20260924) differ from each other or from this process's render in the
               file set or any byte, or either exits nonzero.  The regbooks root is printed
               as the fixed token PLANTED/planted_regbooks, so the transcript is the same
               under any --root [f-6].  SABOTAGE: one byte bent; a
               process-dependent salt; a hash-order-dependent line under the two seeds.
BANNED: self-comparison; one example where cardinality was possible; a tuned magnitude
bound standing in for an identity; a check whose claim is not the design's claim.
FROZEN SUBSTRATE: HALTs unless NAIAD_CACHE_DIR is the TC11 snapshot (tierc11_env's
guard).  Seed 20260924.  The transcript carries no clock and no temp path.

Run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B scripts/tierc11_score_fixtures.py \\
          [leg-substring ...] [--refile-transcript] [--root=DIR]
      --root=DIR redirects the transcript, the planted regbooks and the F-DET twins.
      --print-tally-section prints STAGE_SCORE.md's fixture-tally section, rendered from
      the FILED transcript (stdout only) [TC11-FIX verify MINOR-11].
      --print-planted-section prints STAGE_SCORE.md's planted section (the planted run's
          own S0_VERDICTS.md tables, every verdict cell tagged 'PLANTED ·') to stdout and
          exits; nothing is written.
Exit 0 = every leg GREEN, every break RED · 1 = a RED or VOID fixture, a transcript
finding, or a HALT.
"""
from __future__ import annotations

import __future__
import contextlib
import copy
import hashlib
import inspect
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time
import types
from fractions import Fraction
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import tierc11_score as S                                            # noqa: E402  (guards first)

import numpy as np                                                   # noqa: E402
import pandas as pd                                                  # noqa: E402

E = S.E
TP = E.TP

# ── FIXTURE-TYPED LITERALS: the commission, a second object, never S's own ──
TC11_SNAP = Path.home() / ".cache" / "naiad" / "snapshots" / "tc11_20260925"
SEED = 20260924
SEED_SENS = 20260816
N_BOOT = 4000
B_SMALL = 499                           # (499+1)//90 - 1 = 4 -> the 5th-smallest draw decides
DET_SEEDS = (1, SEED)
AS_OF_LINE = "as_of_last_closed_4h: 2026-09-25T00:00:00Z"
CONTRACT_SHA_T = "bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835"
HEAD_T = "6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9"
NINE_T = ("P-WARN-1", "P-AGE-1", "P-WIN-1", "P-BRK-4H", "P-RELAY-1", "P-SCALP-2",
          "P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG")
RULER_T = {"P-WARN-1": "paired", "P-ADD-BRK": "paired", "P-ADD-SFP": "paired",
           "P-TP-RNG": "paired", "P-AGE-1": "two_sample", "P-WIN-1": "two_sample",
           "P-RELAY-1": "two_sample", "P-BRK-4H": "vs_zero", "P-SCALP-2": "vs_zero"}
ERA_T = {r: ("holdout" if r == "P-SCALP-2" else "full") for r in NINE_T}
BAR_T = Fraction(1, 90)                  # 0.10 / 9
ERA_CUT_T = 1_719_791_999_000            # L-1.3: tuning closes <= 2024-06-30T23:59:59Z
CLASSIC5_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT")
PANEL17_T = ("BTCUSDT", "ETHUSDT", "SOLUSDT", "NEARUSDT", "ZECUSDT", "ENAUSDT", "PUMPUSDT",
             "HYPEUSDT", "MNTUSDT_BYBIT", "SUIUSDT", "LTCUSDT", "XMRUSDT", "BNBUSDT",
             "UNIUSDT", "1000PEPEUSDT", "DOGEUSDT", "1000BONKUSDT")
REQ_T = ("symbol", "entry_ms", "entry_close_ms", "direction", "entry_px", "stop_px",
         "r_dist", "exit_close_ms", "exit_reason", "net_r", "gross_r", "fee_r", "funding_r",
         "haircut_net_r", "era", "lane")
COLLAR_T = {"tier": "TIER-E", "selection_not_a_result": "a SELECTION, not a result",
            "gates": "nothing"}
CI_READ_T = {"above": "CI above zero (lo > 0)", "includes": "CI includes zero",
             "below": "CI wholly below zero (hi < 0)", "none": "no interval"}
VERDICT_RX_T = re.compile(r"\bSUPPORTED\b|\bverdict\b", re.IGNORECASE)
FORBID_KEY_T = re.compile(r"verdict|clears_bar|spent_test", re.IGNORECASE)
BASE7_T = ("P-AGE-1", "P-WIN-1", "P-WARN-1", "P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG",
           "P-RELAY-1")
V6_N_T = 200
V6_CMP_T = (("entry_close_ms", "entry_close_ms"), ("direction", "direction"),
            ("entry_px", "entry_px"), ("stop_px", "stop_px"), ("r_dist", "r_dist"),
            ("exit_close_ms", "exit_close_ms"), ("exit_reason", "exit_reason"),
            ("net_r", "net_r"), ("gross_r", "gross_r"), ("fee_r", "fee_r"),
            ("funding_r", "funding_r"), ("era", "era_of_entry"), ("lane", "lane"))
OUTPUT_FILES_T = ("BASE_IDENT.json", "FAMILY.json", "REGISTRY_CHECK.json", "S0_VERDICTS.md",
                  "SCORES.json", "SCORE_MANIFEST.json")
PLANT_BANNER = ("PLANTED — synthetic regbooks written by scripts/tierc11_score_fixtures.py; "
                "NOT A RESULT of any registration")
PLANT_LABEL = "PLANTED/planted_regbooks"   # a fixed root token: the transcript is the same
                                            # under any --root [repair f-6]
STRADDLE_ENTRY_MS = 1_719_777_600_000       # 2024-06-30T20:00Z: the 4h entry bar straddling
                                            # the cut (open tuning, close holdout) [repair f-1]
MS_H, MS_4H, MS_D = 3_600_000, 14_400_000, 86_400_000
T0_LANE = 1_685_577_600_000             # 2023-06-01T00:00:00Z — synthetic lanes span both eras
ZEC_NEG = 0.07                          # P-ADD-BRK's planted ZEC delta: lands lo > 0, p > 1/90

OUT = S.SCORES
RUN_ROOT = OUT
TRANSCRIPT = "FIXTURES_SCORE.txt"
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
            shown = hit[:170] if i + len(want) <= 170 else (hit[:50] + " … " + hit[i:i + 140])
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


# ═══════════════════════════════════════════════ THE PLANTED FAMILY (this file's)
def fee_table() -> dict:
    """{stem: (charter slippage bps/side, taker bps/side)} read from the TC11 record
    fee_schedule.json by THIS file (not E.fees)."""
    raw = json.loads((E.OUT / "data" / "fee_schedule.json").read_text(encoding="utf-8"))
    return {a["stem"]: (float(a["charter_slippage_bps_per_side"]),
                        float(a["taker_bps_side_used"])) for a in raw["assets"]}


def era_t(close) -> np.ndarray:
    return np.where(np.asarray(close, np.int64) <= ERA_CUT_T, "tuning", "holdout").astype(object)


def haircut_t(df: pd.DataFrame, fees: dict) -> np.ndarray:
    slip = np.array([fees[s][0] for s in df["symbol"]], float)
    tak = np.array([fees[s][1] for s in df["symbol"]], float)
    return df["net_r"].to_numpy(float) - df["fee_r"].to_numpy(float) * (slip / tak)


def pandas_sha(df: pd.DataFrame) -> str:
    """The canonical CSV by pandas' own route — the SECOND object the scorer's manual
    writer (SC-13) must equal."""
    d = df.loc[:, list(REQ_T)].sort_values(["symbol", "entry_close_ms"], kind="mergesort")
    return sha_bytes(d.to_csv(index=False).encode("utf-8"))


def v6_base(fees: dict) -> pd.DataFrame:
    """books/v6_campaigns.parquet (the frozen control) in the regbook schema."""
    v = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    v = v.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
    d = pd.DataFrame({
        "symbol": v["symbol"].astype(object), "entry_ms": v["entry_ms"].astype(np.int64),
        "entry_close_ms": v["entry_close_ms"].astype(np.int64),
        "direction": v["direction"].astype(np.int8), "entry_px": v["entry_px"].astype(float),
        "stop_px": v["stop_px"].astype(float), "r_dist": v["r_dist"].astype(float),
        "exit_close_ms": v["exit_close_ms"].astype(np.int64),
        "exit_reason": v["exit_reason"].astype(object), "net_r": v["net_r"].astype(float),
        "gross_r": v["gross_r"].astype(float), "fee_r": v["fee_r"].astype(float),
        "funding_r": v["funding_r"].astype(float), "haircut_net_r": 0.0,
        "era": v["era_of_entry"].astype(object), "lane": v["lane"].astype(object)})
    d["haircut_net_r"] = haircut_t(d, fees)
    return d


def with_net(df: pd.DataFrame, net, fees: dict, lane: str | None = None) -> pd.DataFrame:
    d = df.copy()
    d["net_r"] = np.asarray(net, float)
    d["gross_r"] = d["net_r"] + d["fee_r"] + d["funding_r"]
    d["haircut_net_r"] = haircut_t(d, fees)
    if lane is not None:
        d["lane"] = lane
    return d.reset_index(drop=True)


def synth_lane(panel, per: int, mu: float, seed: int, lane: str, fees: dict) -> pd.DataFrame:
    """A synthetic lane: `per` campaigns per asset, 30 days apart from 2023-06-01 (both
    eras), net_r ~ Normal(mu, 1) from a seeded generator."""
    rng = np.random.default_rng(seed)
    rows = []
    for a, s in enumerate(panel):
        for k in range(per):
            close = T0_LANE + (k * 30 + a) * MS_D + MS_4H
            net = float(rng.normal(mu, 1.0))
            dr = 1 if k % 2 == 0 else -1
            fee = 0.02 + 0.001 * a
            fund = 0.001 * ((k % 3) - 1)
            rows.append({"symbol": s, "entry_ms": close - MS_4H, "entry_close_ms": close,
                         "direction": dr, "entry_px": 100.0 + a, "stop_px": 100.0 + a - dr * 5.0,
                         "r_dist": 5.0, "exit_close_ms": close + 3 * MS_D,
                         "exit_reason": "stop" if net < 0 else "bell", "net_r": net,
                         "gross_r": net + fee + fund, "fee_r": fee, "funding_r": fund,
                         "haircut_net_r": 0.0, "era": "", "lane": lane})
    d = pd.DataFrame(rows)
    d["entry_ms"] = d["entry_ms"].astype(np.int64)
    d["entry_close_ms"] = d["entry_close_ms"].astype(np.int64)
    d["exit_close_ms"] = d["exit_close_ms"].astype(np.int64)
    d["direction"] = d["direction"].astype(np.int8)
    d["haircut_net_r"] = haircut_t(d, fees)
    d["era"] = era_t(d["entry_close_ms"])
    return d


def relay_book(base: pd.DataFrame, mask, fees: dict) -> pd.DataFrame:
    """A synthetic relay: the masked v6 campaigns entered 2h earlier (a 1h close inside
    the 4h window; entry_ms stays the open of that 4h bar, the interface's lens bar),
    net_r = 0.8 * v6 + 0.05."""
    r = base[np.asarray(mask, bool)].copy()
    r["entry_close_ms"] = (r["entry_close_ms"] - 2 * MS_H).astype(np.int64)
    r = with_net(r, 0.8 * r["net_r"].to_numpy(float) + 0.05, fees, lane="relay")
    r["era"] = era_t(r["entry_close_ms"])
    return r


# extra (non-interface) columns a planted arm may carry: AM-3's add columns, L-1.5's
# acted_by (the identity law), the BRK lane's range-death instant (SC-4 in-sample count)
ADD_EXTRA_T = ("add_r", "funding_r_uncapped", "v6_funding_absorbed_r", "acted_by",
               "die_close_ms")


def with_acted(df: pd.DataFrame, acted, word: str) -> pd.DataFrame:
    """L-1.5: `acted_by` = word where the paired rule acts, '' where it never does."""
    d = df.copy()
    d["acted_by"] = np.where(np.asarray(acted, bool), word, "").astype(object)
    return d


def with_straddle(lane: pd.DataFrame, fees: dict) -> pd.DataFrame:
    """One BTC campaign whose 4h entry bar straddles the era cut (open 2024-06-30T20:00Z,
    close 2024-07-01T00:00Z): era 'holdout' by the CLOSE, 'tuning' by the open [L-1.3]."""
    r = lane.iloc[[0]].copy()
    r["entry_ms"] = np.int64(STRADDLE_ENTRY_MS)
    r["entry_close_ms"] = np.int64(STRADDLE_ENTRY_MS + MS_4H)
    r["exit_close_ms"] = np.int64(STRADDLE_ENTRY_MS + MS_4H + 3 * MS_D)
    d = pd.concat([lane, r], ignore_index=True)
    for c in ("entry_ms", "entry_close_ms", "exit_close_ms"):
        d[c] = d[c].astype(np.int64)
    d["direction"] = d["direction"].astype(np.int8)
    d["era"] = era_t(d["entry_close_ms"])
    d["haircut_net_r"] = haircut_t(d, fees)
    # the range death: 8h before the entry close; the straddle's range died 2 days before
    d["die_close_ms"] = (d["entry_close_ms"] - 2 * MS_4H).astype(np.int64)
    d.loc[d.index[-1], "die_close_ms"] = np.int64(STRADDLE_ENTRY_MS + MS_4H - 2 * MS_D)
    return d.sort_values(["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)


def condition_json(root: Path, met: bool, ci_hi: float) -> None:
    """The planted P-WARN-1 condition record (L-W.4: MET iff the cluster-90% hi < 0)."""
    (root / "P-WARN-1").mkdir(parents=True, exist_ok=True)
    (root / "P-WARN-1" / "condition.json").write_text(json.dumps(
        {"met": met, "ci_hi": ci_hi, "ci_lo": ci_hi - 0.2, "delta": ci_hi - 0.1,
         "note": "PLANTED condition record"}, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def with_adds(df: pd.DataFrame, delta: np.ndarray) -> pd.DataFrame:
    """The planted add book's AM-3 columns: absorbed funding 0.002 R on every 10th
    campaign, add_r = delta - absorbed (so delta == add_r + absorbed, row by row); the v6
    leg's OWN absorption 0.001 R on every 20th campaign, carried both inside
    funding_r_uncapped and in v6_funding_absorbed_r (the scorer must net it out) [m-8]."""
    d = df.copy()
    k = np.arange(len(d))
    absorbed = np.where(k % 10 == 0, 0.002, 0.0)
    v6_abs = np.where(k % 20 == 5, 0.001, 0.0)
    d["add_r"] = np.asarray(delta, float) - absorbed
    d["funding_r_uncapped"] = d["funding_r"].to_numpy(float) + absorbed + v6_abs
    d["v6_funding_absorbed_r"] = v6_abs
    return d


def write_arm(root: Path, rid: str, arm: str, df: pd.DataFrame, ruler: str, panel,
              era_scope: str, desc: str, extra: dict | None = None) -> None:
    kind = "tierE" if arm.startswith("tierE__") else arm
    d = root / rid
    d.mkdir(parents=True, exist_ok=True)
    df = df.loc[:, list(REQ_T) + [c for c in ADD_EXTRA_T if c in df.columns]].reset_index(
        drop=True)
    df.to_parquet(str(d / f"{arm}.parquet"), index=False)
    side = {"registration": rid, "arm": arm, "kind": kind, "ruler": ruler,
            "panel": list(panel), "era_scope": era_scope, "n": int(len(df)),
            "sum_net_r": float(df["net_r"].sum()), "book_sha256": pandas_sha(df),
            "description": desc, "source_script": "scripts/tierc11_score_fixtures.py (PLANTED)"}
    if kind == "tierE":
        side.update(COLLAR_T)
    if extra:
        side.update(extra)
    (d / f"{arm}.json").write_text(json.dumps(side, indent=2, sort_keys=True) + "\n",
                                   encoding="utf-8")


def write_status(root: Path, rid: str, status: str, reason: str, arms: list) -> None:
    d = root / rid
    d.mkdir(parents=True, exist_ok=True)
    (d / "STATUS.json").write_text(json.dumps({"registration": rid, "status": status,
                                               "reason": reason, "arms": list(arms)},
                                              indent=2, sort_keys=True) + "\n", encoding="utf-8")


# the Tier-E rows the planted family must yield, declared HERE (F-COLLAR, F-GRID)
TIER_E_DECLARED_T = (
    "P-WARN-1|scored",
    "P-AGE-1|derived__slice_tuning", "P-AGE-1|derived__slice_holdout",
    "P-AGE-1|tierE__shadow_absolute",
    "P-WIN-1|derived__slice_tuning", "P-WIN-1|derived__slice_holdout",
    "P-WIN-1|tierE__shadow_cut", "P-WIN-1|tierE__holdout_shadow",
    "P-BRK-4H|derived__slice_tuning", "P-BRK-4H|derived__slice_holdout",
    "P-BRK-4H|tierE__17_asset_view", "P-BRK-4H|tierE__frozen_3_0_twin",
    "P-BRK-4H|tierE__holdout_slice",
    "P-RELAY-1|derived__slice_tuning", "P-RELAY-1|derived__slice_holdout",
    "P-RELAY-1|tierE__late_relay_twin",
    "P-ADD-BRK|derived__slice_tuning", "P-ADD-BRK|derived__slice_holdout",
    "P-ADD-BRK|tierE__frozen_3_0_twin", "P-ADD-BRK|tierE__head_to_head_vs_p_add_sfp",
    "P-ADD-SFP|derived__slice_tuning", "P-ADD-SFP|derived__slice_holdout",
    "P-ADD-SFP|tierE__frozen_3_0_twin", "P-ADD-SFP|tierE__holdout_slice",
    "P-ADD-SFP|derived__head_to_head_vs_p_add_brk",        # SC-18: none filed by SFP
    "P-TP-RNG|derived__slice_tuning", "P-TP-RNG|derived__slice_holdout",
)


def plant_family(root: Path, zec_neg: float = ZEC_NEG) -> None:
    """Write the nine planted registrations under `root` (wiped first)."""
    if root.exists():
        shutil.rmtree(root)
    fees = fee_table()
    base = v6_base(fees)
    i = np.arange(len(base))
    c5 = list(CLASSIC5_T)
    bdesc = "PLANTED base = books/v6_campaigns.parquet in the regbook schema"
    # P-WARN-1 · CONDITION_NOT_MET; its rule book printed as Tier-E
    write_arm(root, "P-WARN-1", "scored",
              with_acted(with_net(base, base["net_r"] - np.where(i % 9 == 0, 0.05, 0.0), fees),
                         i % 9 == 0, "warn"),
              "paired", c5, "full", "PLANTED rule book: -0.05 R on every 9th campaign")
    write_arm(root, "P-WARN-1", "base", base, "paired", c5, "full", bdesc)
    condition_json(root, False, 0.05)
    write_status(root, "P-WARN-1", "CONDITION_NOT_MET",
                 "PLANTED: condition cohort delta cluster-90% hi >= 0", ["scored", "base"])
    # P-AGE-1 · gate, refused cohort mean > 0
    ref = (base["net_r"].to_numpy() > 0) & (i % 5 == 0)
    write_arm(root, "P-AGE-1", "scored", base[~ref], "two_sample", c5, "full",
              "PLANTED gate: refuse every 5th campaign with net_r > 0")
    write_arm(root, "P-AGE-1", "base", base, "two_sample", c5, "full", bdesc)
    write_arm(root, "P-AGE-1", "tierE__shadow_absolute", base[i % 7 != 0], "two_sample", c5,
              "full", "PLANTED shadow: refuse every 7th campaign")
    write_status(root, "P-AGE-1", "BUILT", "PLANTED", ["scored", "base",
                                                        "tierE__shadow_absolute"])
    # P-WIN-1 · gate, refused cohort mean < 0
    ref = (base["net_r"].to_numpy() < 0) & (i % 5 == 1)
    write_arm(root, "P-WIN-1", "scored", base[~ref], "two_sample", c5, "full",
              "PLANTED gate: refuse every 5th (offset 1) campaign with net_r < 0")
    write_arm(root, "P-WIN-1", "base", base, "two_sample", c5, "full", bdesc)
    write_arm(root, "P-WIN-1", "tierE__shadow_cut", base[i % 11 != 0], "two_sample", c5,
              "full", "PLANTED shadow: refuse every 11th campaign")
    hold = base["era"].to_numpy() == "holdout"
    write_arm(root, "P-WIN-1", "tierE__holdout_shadow", base[(i % 11 != 0) & hold],
              "two_sample", c5, "holdout",
              "PLANTED holdout-scoped shadow (SC-3: ruled vs the base's holdout rows)")
    write_status(root, "P-WIN-1", "BUILT", "PLANTED", ["scored", "base", "tierE__shadow_cut",
                                                       "tierE__holdout_shadow"])
    # P-BRK-4H · vs zero lane; a GARBAGE base the ruler must ignore
    lane = with_straddle(synth_lane(c5, 24, 0.35, SEED, "brk4h", fees), fees)
    write_arm(root, "P-BRK-4H", "scored", lane, "vs_zero", c5, "full",
              "PLANTED lane: 24 campaigns per asset, net ~ N(0.35, 1)")
    write_arm(root, "P-BRK-4H", "base", with_net(base, np.full(len(base), -5.0), fees),
              "vs_zero", c5, "full", "PLANTED GARBAGE base (net -5 R): a vs-zero ruler "
                                     "must ignore it")
    write_arm(root, "P-BRK-4H", "tierE__frozen_3_0_twin",
              synth_lane(c5, 24, 0.20, SEED + 100, "brk4h", fees), "vs_zero", c5, "full",
              "PLANTED frozen-3.0 twin: net ~ N(0.20, 1)")
    write_arm(root, "P-BRK-4H", "tierE__holdout_slice",
              lane[lane["era"] == "holdout"], "vs_zero", c5, "holdout",
              "PLANTED holdout slice of the lane")
    write_arm(root, "P-BRK-4H", "tierE__17_asset_view",
              synth_lane(PANEL17_T, 10, 0.10, SEED + 200, "brk4h", fees), "vs_zero",
              PANEL17_T, "full", "PLANTED 17-asset view: net ~ N(0.10, 1)")
    write_status(root, "P-BRK-4H", "BUILT", "PLANTED",
                 ["scored", "base", "tierE__frozen_3_0_twin", "tierE__holdout_slice",
                  "tierE__17_asset_view"])
    # P-RELAY-1 · two-sample, its own entry keys
    write_arm(root, "P-RELAY-1", "scored", relay_book(base, i % 2 == 0, fees), "two_sample",
              c5, "full", "PLANTED relay: even campaigns 2h earlier, 0.8 v6 + 0.05")
    write_arm(root, "P-RELAY-1", "base", base, "two_sample", c5, "full", bdesc)
    write_arm(root, "P-RELAY-1", "tierE__late_relay_twin", relay_book(base, i % 2 == 1, fees),
              "two_sample", c5, "full", "PLANTED late-relay twin: odd campaigns")
    write_status(root, "P-RELAY-1", "BUILT", "PLANTED",
                 ["scored", "base", "tierE__late_relay_twin"])
    # P-SCALP-2 · CLOSED BY ITS PRECONDITION
    write_status(root, "P-SCALP-2", "CLOSED_BY_PRECONDITION",
                 "CLOSED BY R2 (1h: FAIL) — PLANTED (the R2 record's own 1h word)", [])
    # P-ADD-BRK · paired: ci_lo > 0 but p > bar (ZEC planted negative)
    zec = base["symbol"].to_numpy() == "ZECUSDT"
    d_brk = np.where(zec, -zec_neg, 0.10) + 0.01 * ((i % 3) - 1)
    d_sfp = 0.30 + 0.05 * ((i % 7) - 3)
    brk = with_acted(with_adds(with_net(base, base["net_r"] + d_brk, fees, lane="card+adds"),
                               d_brk), d_brk != 0, "adds")
    sfp = with_acted(with_adds(with_net(base, base["net_r"] + d_sfp, fees, lane="card+adds"),
                               d_sfp), d_sfp != 0, "adds")
    write_arm(root, "P-ADD-BRK", "scored", brk, "paired", c5, "full",
              f"PLANTED adds: +0.10 R per campaign, -{zec_neg} R on ZEC")
    write_arm(root, "P-ADD-BRK", "base", base, "paired", c5, "full", bdesc)
    write_arm(root, "P-ADD-BRK", "tierE__frozen_3_0_twin",
              with_acted(with_net(base, base["net_r"] + 0.05, fees, lane="card+adds"),
                         np.ones(len(base), bool), "adds"), "paired", c5,
              "full", "PLANTED frozen-3.0 twin: +0.05 R per campaign")
    write_arm(root, "P-ADD-BRK", "tierE__head_to_head_vs_p_add_sfp", brk, "paired", c5, "full",
              "PLANTED head-to-head: the BRK add book ruled against the SFP add book",
              extra={"base_arm": "P-ADD-SFP/scored"})
    write_status(root, "P-ADD-BRK", "BUILT", "PLANTED",
                 ["scored", "base", "tierE__frozen_3_0_twin",
                  "tierE__head_to_head_vs_p_add_sfp"])
    # P-ADD-SFP · paired, SUPPORTED
    write_arm(root, "P-ADD-SFP", "scored", sfp, "paired", c5, "full",
              "PLANTED adds: +0.30 R +- 0.15 per campaign")
    write_arm(root, "P-ADD-SFP", "base", base, "paired", c5, "full", bdesc)
    write_arm(root, "P-ADD-SFP", "tierE__frozen_3_0_twin",
              with_acted(with_net(base, base["net_r"] + 0.10, fees, lane="card+adds"),
                         np.ones(len(base), bool), "adds"), "paired", c5,
              "full", "PLANTED frozen-3.0 twin: +0.10 R per campaign")
    write_arm(root, "P-ADD-SFP", "tierE__holdout_slice", sfp[sfp["era"] == "holdout"],
              "paired", c5, "holdout", "PLANTED holdout slice of the SFP add book")
    write_status(root, "P-ADD-SFP", "BUILT", "PLANTED",
                 ["scored", "base", "tierE__frozen_3_0_twin", "tierE__holdout_slice"])
    # P-TP-RNG · paired, CI wholly below zero; no frozen twin filed; every 4th campaign
    # never acted on (the identity law has rows to hold on)
    tp_act = i % 4 != 0
    write_arm(root, "P-TP-RNG", "scored",
              with_acted(with_net(base, base["net_r"] + np.where(
                  tp_act, -0.20 + 0.02 * ((i % 5) - 2), 0.0), fees), tp_act, "tp"),
              "paired", c5, "full",
              "PLANTED take-profit: -0.20 R +- 0.04 on 3 campaigns in 4, the 4th untouched")
    write_arm(root, "P-TP-RNG", "base", base, "paired", c5, "full", bdesc)
    write_status(root, "P-TP-RNG", "BUILT", "PLANTED", ["scored", "base"])


def planted_root() -> Path:
    return RUN_ROOT / "_det_score" / "planted_regbooks"


_MEMO: dict = {}


def planted_run() -> dict:
    """The planted family, scored once in-process (the object most legs judge)."""
    if not _MEMO:
        root = planted_root()
        plant_family(root)
        res = S.score_all(root, banner=PLANT_BANNER, root_label=PLANT_LABEL)
        _MEMO.update({"root": root, "res": res, "files": S.render(res),
                      "rows": {r["registration"]: r for r in res["rows"]}})
    return _MEMO


def copy_family(tmp: Path) -> Path:
    """A private copy of the planted regbooks (plants are made HERE, never on the record)."""
    src = planted_run()["root"]
    dst = tmp / "regbooks"
    shutil.copytree(src, dst)
    return dst


def rewrite_arm(root: Path, rid: str, arm: str, df: pd.DataFrame, **side_over) -> None:
    """Replace one planted arm (parquet + a sidecar re-hashed by THIS file)."""
    js = json.loads((root / rid / f"{arm}.json").read_text(encoding="utf-8"))
    write_arm(root, rid, arm, df, js["ruler"], js["panel"], js["era_scope"], js["description"],
              extra={k: v for k, v in js.items() if k in ("base_arm", "lens")})
    if side_over:
        js2 = json.loads((root / rid / f"{arm}.json").read_text(encoding="utf-8"))
        js2.update(side_over)
        (root / rid / f"{arm}.json").write_text(json.dumps(js2, indent=2, sort_keys=True) + "\n",
                                                encoding="utf-8")


def read_arm(root: Path, rid: str, arm: str) -> pd.DataFrame:
    return pd.read_parquet(str(root / rid / f"{arm}.parquet"))


def score_one(root: Path, rid: str, n_boot: int = 199) -> dict:
    """The scorer's row for ONE registration on a regbooks root (small B: premise legs)."""
    doc, _ = S.load_registry(ROOT)
    reg = next(r for r in doc["registrations"] if r["registration"] == rid)
    L = S.Loader(root, S._fees())
    v6, _ = S.v6_frame()
    bases = {}
    for r7 in S.BASE_IDENT_REGS:
        st, sh, _ = L.status_of(r7)
        if st is None or sh or "base" not in (st.get("arms") or []):
            continue
        B = L.arm(r7, "base")
        if not B["halts"]:
            bases[r7] = {"df": B["df"], "sha": B["sha"]}
    ident = S.base_ident(bases, v6)
    return S.score_registration(L, reg, ident, n_boot=n_boot)


# ═══════════════════════════════════════════════════════════════ F-SCORE-REG
def reg_inputs() -> tuple[dict, bytes, dict, bytes, bytes]:
    fb = (ROOT / S.REGISTRATIONS_REL).read_bytes()
    return (json.loads(fb.decode("utf-8")), (ROOT / S.CONTRACT_REL).read_bytes(),
            json.loads((ROOT / S.PIN_REL).read_text(encoding="utf-8")),
            (ROOT / S.LEANS_REL).read_bytes(), fb)


def own_registry_findings(doc: dict, contract: bytes, pin: dict) -> tuple[list[str], dict]:
    """THIS file's re-derivation: slices re-cut, payload law, chain walk, typed head."""
    out, n = [], {"slices": 0, "payloads": 0, "links": 0}
    if sha_bytes(contract) != CONTRACT_SHA_T:
        out.append("own: contract sha != typed")
    lines = contract.decode("utf-8").split("\n")
    regs = doc["registrations"]
    if tuple(r["registration"] for r in regs) != NINE_T:
        out.append("own: the nine ids are not the typed order")
    for r in regs:
        lo, hi = r["text_lines"]
        if "\n".join(lines[lo - 1:hi]) == r["text_of_record"]:
            n["slices"] += 1
        body = {k: v for k, v in r.items() if k not in ("text_sha256", "sha256")}
        if sha_bytes(json.dumps(body, sort_keys=True, ensure_ascii=False).encode()) == r["sha256"]:
            n["payloads"] += 1
    prev = "0" * 64
    for ln, r in zip(doc["chain"], regs):
        body = {"seq": ln["seq"], "registration": ln["registration"], "sha256": r["sha256"],
                "prev": prev}
        prev = sha_bytes(json.dumps(body, sort_keys=True).encode())
        if prev == ln["line_sha256"]:
            n["links"] += 1
    if prev != HEAD_T or pin["head"] != HEAD_T or doc["head"] != HEAD_T:
        out.append(f"own: head {prev[:16]}… / pin {pin['head'][:16]}… != typed {HEAD_T[:16]}…")
    if n != {"slices": 9, "payloads": 9, "links": 9}:
        out.append(f"own: {n} != 9/9/9")
    return out, n


def reg_break():
    doc, contract, pin, leans, fb = reg_inputs()

    def bent(fn):
        d, c, p = copy.deepcopy(doc), bytearray(contract), copy.deepcopy(pin)
        fn(d, c, p)
        return S.verify_registrations(d, bytes(c), p, leans_bytes=leans)

    def t_text(d, c, p):
        r = d["registrations"][1]
        r["text_of_record"] = r["text_of_record"].replace("tide-age", "tide_age", 1)

    def t_payload(d, c, p):
        d["registrations"][2]["operative_spec"]["era"] = "holdout"

    def t_prev(d, c, p):
        d["chain"][4]["prev"] = "f" * 64

    def t_line(d, c, p):
        d["chain"][8]["line_sha256"] = "e" * 64

    def t_head(d, c, p):
        p["head"] = "d" * 64

    def t_contract(d, c, p):
        c[4000] ^= 0x01

    def t_drop(d, c, p):
        del d["registrations"][5]

    def t_fam(d, c, p):
        d["family_m"] = 8

    def halted_file():
        with tempfile.TemporaryDirectory() as td:
            t = Path(td)
            for rel in (S.CONTRACT_REL, S.PIN_REL, S.LEANS_REL):
                (t / rel).parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(ROOT / rel, t / rel)
            d = copy.deepcopy(doc)
            d["registrations"][8]["operative_spec"]["ruler"] = "two-sample"
            (t / S.REGISTRATIONS_REL).parent.mkdir(parents=True, exist_ok=True)
            (t / S.REGISTRATIONS_REL).write_text(json.dumps(d, indent=2, ensure_ascii=False)
                                                 + "\n", encoding="utf-8")
            S.load_registry(t)               # must HALT (SystemExit -> a finding)
            return []

    return plants([
        ("one character of P-AGE-1's text_of_record", "TEXT-SLICE", lambda: bent(t_text)),
        ("P-WIN-1 operative_spec.era -> holdout", "PAYLOAD-SHA", lambda: bent(t_payload)),
        ("chain line 5 prev replaced", "CHAIN: line 5 prev", lambda: bent(t_prev)),
        ("chain line 9 line_sha256 replaced", "CHAIN: line 9 line_sha256",
         lambda: bent(t_line)),
        ("REGISTRY_PIN head replaced", "HEAD: REGISTRY_PIN.json head", lambda: bent(t_head)),
        ("one contract byte flipped", "CONTRACT-SHA", lambda: bent(t_contract)),
        ("P-SCALP-2 dropped", "ORDER", lambda: bent(t_drop)),
        ("family_m 8", "FAMILY", lambda: bent(t_fam)),
        ("a tampered REGISTRATIONS.json in a temp root (P-TP-RNG ruler -> two-sample)",
         "PAYLOAD-SHA", halted_file),
    ])


def reg_real():
    doc, contract, pin, leans, fb = reg_inputs()
    mod = S.verify_registrations(doc, contract, pin, leans_bytes=leans, file_bytes=fb)
    own, n = own_registry_findings(doc, contract, pin)
    _, rec = S.load_registry(ROOT)
    rc = json.loads(planted_run()["files"]["REGISTRY_CHECK.json"])
    per_ok = (len(rc["per_registration"]) == 9 and all(p["text_slice_recut_equal"]
                                                       and p["payload_sha256"] ==
                                                       p["payload_sha256_filed"]
                                                       for p in rc["per_registration"]))
    ok = (not mod and not own and rec["head"] == HEAD_T and per_ok
          and rec["contract"]["sha256"] == CONTRACT_SHA_T)
    return ok, (f"scorer verifier: {len(mod)} finding(s); this file's re-derivation: slices "
                f"{n['slices']}/9, payload shas {n['payloads']}/9, chain links {n['links']}/9, "
                f"head {HEAD_T[:16]}… == REGISTRY_PIN.json == typed; contract "
                f"{CONTRACT_SHA_T[:16]}…; REGISTRY_CHECK.json 9 rows all re-cut-equal and "
                f"payload-equal: {per_ok}" + (f"; {mod[:2]} {own[:2]}" if (mod or own) else ""))


# ═══════════════════════════════════════════════════════════════ F-RULER
def own_deltas(a: pd.DataFrame, b: pd.DataFrame, col: str = "net_r"):
    """Per-campaign deltas keyed (symbol, entry_ms), in (symbol, entry_ms) order — this
    file's own join (a dict), not the scorer's merge."""
    bk = {(s, int(e)): float(v) for s, e, v in zip(b["symbol"], b["entry_ms"], b[col])}
    rows = sorted((s, int(e), float(v) - bk[(s, int(e))])
                  for s, e, v in zip(a["symbol"], a["entry_ms"], a[col]) if (s, int(e)) in bk)
    return (np.array([r[2] for r in rows], float), np.array([r[0] for r in rows], object))


PAIRED_BUILT_T = ("P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG")    # BUILT paired in the planted family
TWO_SAMPLE_T = ("P-AGE-1", "P-WIN-1", "P-RELAY-1")
GATES_T = ("P-AGE-1", "P-WIN-1")
# SC-3: the planted Tier-E arms whose era_scope is not 'full' and whose ruler reads a base
SC3_ARMS_T = (("P-ADD-SFP", "tierE__holdout_slice", "paired"),
              ("P-WIN-1", "tierE__holdout_shadow", "two_sample"))


def _te(row: dict, arm: str) -> dict | None:
    return next((t for t in row["tier_e"] if t["arm"] == arm), None)


def _paired_halted(row: dict, rid: str, want: str) -> bool:
    """A paired row halted by `want`: the registered row for a BUILT registration, the
    collared Tier-E 'scored' row for the planted CONDITION_NOT_MET P-WARN-1."""
    if rid == "P-WARN-1":
        t = _te(row, "scored")
        return bool(t and t.get("halted") and want in t["halted"] and t.get("n") is None)
    return (row["verdict_of_record"] == "HALT" and row["stats"] is None
            and not row["spent_test"] and any(want in h for h in row["halts"]))


def own_two_sample_point(a: pd.DataFrame, b: pd.DataFrame) -> float:
    return float(np.mean(a["net_r"].to_numpy(float))) - float(np.mean(b["net_r"].to_numpy(float)))


def ruler_findings(tmp: Path) -> list[str]:
    """The ruler claims, each a finding when broken — every one over EVERY registration
    of its kind in the planted family (no one-example claims)."""
    out = []
    doc, *_ = reg_inputs()
    for r in doc["registrations"]:
        sp = S.spec_of(r)
        if (sp["ruler"], sp["era"]) != (RULER_T[r["registration"]], ERA_T[r["registration"]]):
            out.append(f"RULER-TABLE: {r['registration']} reads ({sp['ruler']}, {sp['era']}) != "
                       f"typed ({RULER_T[r['registration']]}, {ERA_T[r['registration']]})")
    root = copy_family(tmp)
    paired4 = PAIRED_BUILT_T + ("P-WARN-1",)
    for rid in paired4:
        sc = read_arm(root, rid, "scored")
        # (b) one key moved / (c) one row dropped -> HALT 'paired premise failed'
        moved = sc.copy()
        moved.loc[3, "entry_ms"] = int(moved.loc[3, "entry_ms"]) + MS_4H
        moved.loc[3, "entry_close_ms"] = int(moved.loc[3, "entry_close_ms"]) + MS_4H
        moved["era"] = era_t(moved["entry_close_ms"])
        for lab, bent in (("one key moved", moved), ("one row dropped", sc.drop(index=7))):
            rewrite_arm(root, rid, "scored", bent)
            row = score_one(root, rid)
            ok = _paired_halted(row, rid, "PAIRED-PREMISE") and (
                rid == "P-WARN-1" or "paired premise failed" in row["verdict_cell"])
            if not ok:
                out.append(f"PAIRED-PREMISE-NOT-ENFORCED: {rid} {lab} -> "
                           f"{row['verdict_of_record']} ({str(row['verdict_cell'])[:80]})")
        # (d) the identity law: an unacted row that moved; acted_by dropped -> HALT
        un = sc.copy()
        un.loc[5, "acted_by"] = ""
        un.loc[5, "net_r"] = float(read_arm(root, rid, "base").set_index(
            ["symbol", "entry_ms"]).loc[(un.loc[5, "symbol"], int(un.loc[5, "entry_ms"])),
                                        "net_r"]) + 0.25
        un = with_net(un, un["net_r"], fee_table())
        for lab, bent in (("an unacted row off the base by +0.25 R", un),
                          ("acted_by dropped", sc.drop(columns="acted_by"))):
            rewrite_arm(root, rid, "scored", bent)
            row = score_one(root, rid)
            if not _paired_halted(row, rid, "IDENTITY-LAW"):
                out.append(f"IDENTITY-LAW-NOT-ENFORCED: {rid} {lab} -> "
                           f"{row['verdict_of_record']} halts {row['halts'][:1]}")
        rewrite_arm(root, rid, "scored", sc)
    # (e) two-sample on identical keys -> FLAG, on all three; the planted rows -> no flag
    rr = planted_run()["rows"]
    for rid in TWO_SAMPLE_T:
        keep = read_arm(root, rid, "scored")
        rewrite_arm(root, rid, "scored", read_arm(root, rid, "base"))
        row = score_one(root, rid)
        if not ("FLAG: TWO-SAMPLE-PREMISE" in str(row["verdict_cell"])
                and (row.get("premise") or {}).get("key_sets_identical") is True):
            out.append(f"TWO-SAMPLE-FLAG-MISSING: {rid} identical key sets -> "
                       f"{str(row['verdict_cell'])[:90]}")
        rewrite_arm(root, rid, "scored", keep)
        if "FLAG" in str(rr[rid]["verdict_cell"]) or (rr[rid]["premise"] or {}).get("flag"):
            out.append(f"TWO-SAMPLE-FLAG-SPURIOUS: the planted {rid} (keys differ) was flagged")
    # (f) vs zero ignores its base (P-BRK-4H: the only vs-zero registration the planted
    # family BUILDS — P-SCALP-2 is closed by its precondition, as the R2 record requires)
    with_b = score_one(root, "P-BRK-4H")
    st = json.loads((root / "P-BRK-4H" / "STATUS.json").read_text(encoding="utf-8"))
    write_status(root, "P-BRK-4H", st["status"], st["reason"],
                 [a for a in st["arms"] if a != "base"])
    (root / "P-BRK-4H" / "base.parquet").unlink()
    (root / "P-BRK-4H" / "base.json").unlink()
    no_b = score_one(root, "P-BRK-4H")
    ka = json.dumps(S._js({k: with_b[k] for k in ("stats", "verdict_of_record", "verdict_cell",
                                                  "tier_e")}), sort_keys=True)
    kb = json.dumps(S._js({k: no_b[k] for k in ("stats", "verdict_of_record", "verdict_cell",
                                                "tier_e")}), sort_keys=True)
    if ka != kb or with_b["verdict_of_record"] == "HALT":
        out.append(f"VS-ZERO-IGNORES-BASE: the vs-zero row moved when its base arm was removed "
                   f"({with_b['verdict_of_record']} vs {no_b['verdict_of_record']})")
    # (g) every BUILT paired row on identical keys, lanes different — re-scored HERE (under
    # any mutation in force), never read from the memo
    for rid in PAIRED_BUILT_T:
        r = score_one(root, rid)
        a, b = read_arm(root, rid, "scored"), read_arm(root, rid, "base")
        dv, _ = own_deltas(a, b)
        m = (r.get("stats") or {}).get("main") or {}
        if not (r["verdict_of_record"] != "HALT" and m.get("n") == V6_N_T
                and m.get("n_base") == V6_N_T and m.get("point") == float(np.mean(dv))
                and (r.get("premise") or {}).get("key_sets_identical") is True
                and ((r.get("premise") or {}).get("identity") or {}).get("unacted")
                == int((a["acted_by"].astype(str) == "").sum())):
            out.append(f"PAIRED-ROW: {rid} n {m.get('n')} / base {m.get('n_base')} point "
                       f"{m.get('point')} vs this file's {float(np.mean(dv)) if len(dv) else None}")
        if rid == "P-ADD-SFP" and set(a["lane"]) == set(b["lane"]):
            out.append("PAIRED-ROW: the planted lanes do not differ (the lane-key case is void)")
    # (h) a gate is a post-filter: a new campaign / a kept row changed -> HALT, both gates
    for rid in GATES_T:
        keep = read_arm(root, rid, "scored")
        extra = keep.iloc[[0]].copy()           # a campaign 1h off every v6 key
        for c in ("entry_ms", "entry_close_ms", "exit_close_ms"):
            extra[c] = (extra[c] + MS_H).astype(np.int64)
        extra["era"] = era_t(extra["entry_close_ms"])
        kept = keep.copy()
        kept = with_net(kept, kept["net_r"].to_numpy() + np.where(np.arange(len(kept)) == 2,
                                                                   0.1, 0.0), fee_table())
        for lab, bent in (("a campaign the base never held", pd.concat(
                [keep, extra], ignore_index=True)), ("a kept row's net_r moved", kept)):
            rewrite_arm(root, rid, "scored", bent)
            row = score_one(root, rid)
            if not (row["verdict_of_record"] == "HALT"
                    and any("GATE-POSTFILTER" in h for h in row["halts"])):
                out.append(f"GATE-POSTFILTER-NOT-ENFORCED: {rid} {lab} -> "
                           f"{row['verdict_of_record']}")
        rewrite_arm(root, rid, "scored", keep)
    # (i) SC-3: a Tier-E arm scoped to an era is ruled against the base's rows of THAT era
    for rid, arm, ruler in SC3_ARMS_T:
        row = score_one(root, rid)
        t = _te(row, arm) or {}
        a = read_arm(root, rid, arm)
        b = read_arm(root, rid, "base")
        bh = b[era_t(b["entry_close_ms"]) == "holdout"]
        want = (float(np.mean(own_deltas(a, bh)[0])) if ruler == "paired"
                else own_two_sample_point(a, bh))
        if t.get("halted") or t.get("n_base") != len(bh) or t.get("point") != want:
            out.append(f"SC-3: {rid}/{arm} ({ruler}, holdout) n_base {t.get('n_base')} point "
                       f"{t.get('point')} halted {str(t.get('halted'))[:60]} != this file's base "
                       f"holdout n {len(bh)}, point {want}")
    return out


def ruler_break():
    def under(obj, name, val):
        def thunk():
            with tempfile.TemporaryDirectory() as td, mutated(obj, name, val):
                return ruler_findings(Path(td))
        return thunk

    def corrupt_key():
        with tempfile.TemporaryDirectory() as td:
            root = copy_family(Path(td))
            sc = read_arm(root, "P-TP-RNG", "scored")
            sc.loc[0, "entry_ms"] = int(sc.loc[0, "entry_ms"]) - MS_4H
            sc.loc[0, "entry_close_ms"] = int(sc.loc[0, "entry_close_ms"]) - MS_4H
            sc["era"] = era_t(sc["entry_close_ms"])
            rewrite_arm(root, "P-TP-RNG", "scored", sc)
            return score_one(root, "P-TP-RNG")["halts"]

    real_tsp = S.two_sample_premise

    def no_flag(a, b):
        x = real_tsp(a, b)
        x.pop("flag", None)
        return x

    r2 = dict(S.RULER_OF_SPEC)
    r2["two-sample"] = "paired"
    r3 = dict(S.RULER_OF_SPEC)
    r3["vs zero"] = "two_sample"
    return plants([
        ("the paired premise check disabled", "PAIRED-PREMISE-NOT-ENFORCED",
         under(S, "paired_premise", lambda a, b: [])),
        ("the identity law disabled (SC-15)", "IDENTITY-LAW-NOT-ENFORCED",
         under(S, "identity_findings", lambda a, b, tag: [])),
        ("the two-sample ruler read as paired", "RULER-TABLE: P-AGE-1",
         under(S, "RULER_OF_SPEC", r2)),
        ("the vs-zero ruler read as two-sample", "RULER-TABLE: P-BRK-4H",
         under(S, "RULER_OF_SPEC", r3)),
        ("the identical-key two-sample flag suppressed (SC-6)", "TWO-SAMPLE-FLAG-MISSING",
         under(S, "two_sample_premise", no_flag)),
        ("the vs-zero row reading its base", "VS-ZERO-IGNORES-BASE",
         under(S, "_uses_base", lambda ruler: True)),
        ("the pairing key taken WITH lane", "PAIRED-ROW",
         under(S, "PAIR_KEY", ["symbol", "lane", "entry_ms"])),
        ("the gate post-filter check disabled (SC-16)", "GATE-POSTFILTER-NOT-ENFORCED",
         under(S, "gate_findings", lambda a, b, tag: [])),
        ("a Tier-E base not restricted to the arm's era_scope (SC-3)", "SC-3:",
         under(S, "_restrict", lambda df, scope: df)),
        ("corrupted input: P-TP-RNG with one entry_ms moved, handed to the scorer",
         "PAIRED-PREMISE", corrupt_key),
    ])


def ruler_real():
    with tempfile.TemporaryDirectory() as td:
        bad = ruler_findings(Path(td))
    rr = planted_run()["rows"]
    return (not bad), (f"the nine rulers/eras == the typed L-1.4 table; on EACH of the 4 paired "
                       f"registrations (P-ADD-BRK, P-ADD-SFP, P-TP-RNG registered; P-WARN-1's "
                       f"Tier-E rule book) one key moved, one row dropped, an unacted row off "
                       f"the base and acted_by dropped each HALT (paired premise / identity law, "
                       f"no number, no slot); two-sample on identical keys FLAGGED on all 3 "
                       f"(P-AGE-1, P-WIN-1, P-RELAY-1), the planted rows not; P-BRK-4H vs zero "
                       f"identical with and without its garbage base; the 3 BUILT paired rows "
                       f"n == n_base == 200, point == this file's delta mean, unacted count == "
                       f"this file's (P-TP-RNG {rr['P-TP-RNG']['premise']['identity']['unacted']})"
                       f"; both gates HALT on a new campaign and on a kept row moved; SC-3: "
                       f"P-ADD-SFP/tierE__holdout_slice (paired) and P-WIN-1/tierE__holdout_shadow "
                       f"(two-sample) ruled vs the base's 77 holdout rows, point == this file's"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BOOT
def hand_draws(values, clusters, seed: int, B: int) -> np.ndarray:
    """THIS file's cluster bootstrap of the mean: assets drawn with replacement by
    np.random.default_rng(seed).choice over the sorted asset labels."""
    v = np.asarray(values, float)
    c = np.asarray(clusters, object)
    uniq = np.array(sorted(set(c.tolist())), dtype=object)
    idx = {u: np.flatnonzero(c == u) for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(B)
    for b in range(B):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        out[b] = float(np.mean(v[np.concatenate([idx[u] for u in pick])]))
    return out


def hand_draws_diff(va, ca, vb, cb, seed: int, B: int) -> np.ndarray:
    va, vb = np.asarray(va, float), np.asarray(vb, float)
    ca, cb = np.asarray(ca, object), np.asarray(cb, object)
    uniq = np.array(sorted(set(ca.tolist()) | set(cb.tolist())), dtype=object)
    ia = {u: np.flatnonzero(ca == u) for u in uniq}
    ib = {u: np.flatnonzero(cb == u) for u in uniq}
    rng = np.random.default_rng(seed)
    out = np.empty(B)
    for b in range(B):
        pick = rng.choice(uniq, size=len(uniq), replace=True)
        ta = np.concatenate([ia[u] for u in pick])
        tb = np.concatenate([ib[u] for u in pick])
        out[b] = ((float(np.mean(va[ta])) if len(ta) else np.nan)
                  - (float(np.mean(vb[tb])) if len(tb) else np.nan))
    return out


def hand_stat(ruler: str, a: pd.DataFrame, b, col: str, seed: int, B: int) -> dict:
    """The hand computation: point, CI 5/95, the typed p law, the typed deciding rank."""
    if ruler == "vs_zero":
        v, c = a[col].to_numpy(float), a["symbol"].to_numpy(object)
        pt, d = float(np.mean(v)), hand_draws(v, c, seed, B)
    elif ruler == "two_sample":
        pt = float(np.mean(a[col].to_numpy(float))) - float(np.mean(b[col].to_numpy(float)))
        d = hand_draws_diff(a[col], a["symbol"], b[col], b["symbol"], seed, B)
    else:
        v, c = own_deltas(a, b, col)
        pt, d = float(np.mean(v)), hand_draws(v, c, seed, B)
    f = d[np.isfinite(d)]
    k = int(sum(1 for x in f if x <= 0))
    kmax = (len(f) + 1) // 90 - 1                      # typed: 90(k+1) <= B+1
    return {"point": pt, "lo": float(np.percentile(f, 5)), "hi": float(np.percentile(f, 95)),
            "p_one_sided": (k + 1) / (len(f) + 1), "p_num": k + 1, "p_den": len(f) + 1,
            "deciding_bound": float(np.sort(f)[kmax]) if kmax >= 0 else None}


BOOT_CASES = (("P-ADD-BRK", "paired"), ("P-AGE-1", "two_sample"), ("P-RELAY-1", "two_sample"),
              ("P-BRK-4H", "vs_zero"))


def boot_findings() -> list[str]:
    out = []
    root = planted_run()["root"]
    rows = planted_run()["rows"]
    for rid, ruler in BOOT_CASES:
        a = read_arm(root, rid, "scored").sort_values(["symbol", "entry_close_ms"],
                                                     kind="mergesort").reset_index(drop=True)
        b = None if ruler == "vs_zero" else read_arm(root, rid, "base").sort_values(
            ["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
        st = S.stats_block(ruler, a, b, CLASSIC5_T, n_boot=B_SMALL, with_loao=False)
        for lab, col, seed, got in (("main", "net_r", SEED, st["main"]),
                                    ("sens", "net_r", SEED_SENS, st["sens"]),
                                    ("haircut", "haircut_net_r", SEED, st["haircut"])):
            h = hand_stat(ruler, a, b, col, seed, B_SMALL)
            for k in ("point", "lo", "hi", "p_one_sided", "p_num", "p_den", "deciding_bound"):
                if got.get(k) != h[k]:
                    tag = ("BOOT-P" if k.startswith("p_") else "BOOT-CI" if k in ("lo", "hi")
                           else "BOOT-BOUND" if k == "deciding_bound" else "BOOT-POINT")
                    out.append(f"{tag}[{rid}/{ruler}/{lab}/B{B_SMALL}] {k}: scorer {got.get(k)!r}"
                               f" != hand {h[k]!r}")
    # B 4000 on the rows of record
    for rid, ruler in (("P-ADD-BRK", "paired"), ("P-AGE-1", "two_sample"),
                       ("P-BRK-4H", "vs_zero")):
        a = read_arm(root, rid, "scored").sort_values(["symbol", "entry_close_ms"],
                                                     kind="mergesort").reset_index(drop=True)
        b = None if ruler == "vs_zero" else read_arm(root, rid, "base").sort_values(
            ["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
        h = hand_stat(ruler, a, b, "net_r", SEED, N_BOOT)
        got = rows[rid]["stats"]["main"]
        for k in ("point", "lo", "hi", "p_one_sided", "deciding_bound"):
            if got.get(k) != h[k]:
                out.append(f"BOOT-RECORD[{rid}] {k}: scorer {got.get(k)!r} != hand {h[k]!r} "
                           f"(B 4000, seed {SEED})")
    # LOAO vs TP.loao_n (the lineage's own, lanes unified so its key == ours)
    for rid, ruler in BOOT_CASES:
        a = read_arm(root, rid, "scored")
        b = None if ruler == "vs_zero" else read_arm(root, rid, "base")
        mine = S.loao(ruler, a.sort_values(["symbol", "entry_close_ms"]).reset_index(drop=True),
                      None if b is None else b.sort_values(["symbol", "entry_close_ms"])
                      .reset_index(drop=True), "net_r", CLASSIC5_T, SEED, B_SMALL)

        def objs(d):
            return [SimpleNamespace(symbol=s, lane="card", entry_ms=int(e), net_r=float(r))
                    for s, e, r in zip(d["symbol"], d["entry_ms"], d["net_r"])]
        if ruler == "paired":
            a2 = a.sort_values(["symbol", "entry_ms"]).reset_index(drop=True)
            b2 = b.sort_values(["symbol", "entry_ms"]).reset_index(drop=True)
            tp = TP.loao_n(objs(a2), objs(b2), CLASSIC5_T, two_sample=False, seed=SEED,
                           n_boot=B_SMALL)
        else:
            tp = TP.loao_n(objs(a), None if b is None else objs(b), CLASSIC5_T,
                           two_sample=(ruler == "two_sample"), seed=SEED, n_boot=B_SMALL)
        per_t = {p["dropped"]: p for p in tp["_per"]}
        for p in mine["per_panel"]:
            q = per_t[p["dropped"]]
            for k in ("ci_lo", "ci_hi"):
                mv = None if p[k] is None else round(p[k], 6)
                if mv != q[k]:
                    out.append(f"BOOT-LOAO[{rid}/{ruler}] -{p['dropped']} {k}: scorer {mv} != "
                               f"TP.loao_n {q[k]}")
        if mine["line"] != tp["loao_line"] or mine["bar"] != tp["loao_bar_above_half"]:
            out.append(f"BOOT-LOAO[{rid}] line {mine['line']} != TP.loao_n {tp['loao_line']}")
    return out


def boot_break():
    real_ci_of = S.ci_of

    def bent_p(draws, point):
        r = real_ci_of(draws, point)
        f = draws[np.isfinite(draws)]
        r["p_one_sided"] = float(np.sum(f < 0) / len(f))
        return r

    def bent_ci(draws, point):
        r = real_ci_of(draws, point)
        f = draws[np.isfinite(draws)]
        r["lo"], r["hi"] = float(np.percentile(f, 2.5)), float(np.percentile(f, 97.5))
        return r

    def row_boot(values, clusters, seed, n_boot):
        v = np.asarray(values, float)
        rng = np.random.default_rng(seed)
        return np.array([float(np.mean(v[rng.integers(0, len(v), len(v))]))
                         for _ in range(n_boot)])

    bent_t5 = SimpleNamespace(cluster_boot=row_boot, cluster_boot_diff=S.T5.cluster_boot_diff,
                              _ci_from=S.T5._ci_from, d15=S.T5.d15)

    def under(obj, name, val):
        def thunk():
            with mutated(obj, name, val):
                return boot_findings()
        return thunk

    return plants([
        ("the p law bent to #draws<0 / B", "BOOT-P", under(S, "ci_of", bent_p)),
        ("the CI bent to the 2.5th..97.5th percentile", "BOOT-CI", under(S, "ci_of", bent_ci)),
        ("the seed of record bent to 20260921", "BOOT-CI", under(S, "SEED", 20260921)),
        ("the draw unit bent from assets to rows", "BOOT-CI", under(S, "T5", bent_t5)),
    ])


def boot_real():
    bad = boot_findings()
    r = planted_run()["rows"]["P-ADD-BRK"]["stats"]["main"]
    return (not bad), (f"{len(BOOT_CASES)} planted books x (seed {SEED}, sens {SEED_SENS}, "
                       f"haircut) at B {B_SMALL}: point, CI, p = (#<=0+1)/(B+1), deciding "
                       f"bound (rank floor((B+1)/90) = {(B_SMALL + 1) // 90}) == this file's hand "
                       f"computation EXACTLY; the rows of record at B 4000 == hand exactly "
                       f"(P-ADD-BRK p {r['p_num']}/{r['p_den']}, deciding rank "
                       f"{r['deciding_rank']}); LOAO per-panel == TP.loao_n at 6 dp on 4 books"
                       + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-VERDICT
VERDICT_CASES_T = (
    (0.05, 0.30, 0.03, "NOT SUPPORTED"),                        # the named case
    (0.05, 0.30, Fraction(44, 4001), "SUPPORTED"),              # k = 43 of 4000
    (0.05, 0.30, Fraction(45, 4001), "NOT SUPPORTED"),          # k = 44
    (0.05, 0.30, 0.011111, "SUPPORTED"),
    (0.05, 0.30, 0.0111112, "NOT SUPPORTED"),
    (0.05, 0.30, 0.0125, "NOT SUPPORTED"),                      # 0.10/8 would pass it
    (0.0, 0.30, 0.00025, "NOT SUPPORTED"),                      # lo not > 0 (strict)
    (-0.01, 0.30, 0.00025, "NOT SUPPORTED"),
    (-0.30, -0.05, 0.99, "NOT SUPPORTED — CI wholly below zero"),
    (0.10, 0.40, None, "NOT SUPPORTED"),
    (None, None, None, "NOT SUPPORTED"),
)
SCALE_T = ("P-BRK-4H", "P-ADD-BRK", "P-ADD-SFP", "P-TP-RNG")
LABEL_T = {"P-AGE-1": "— IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored cohort IS "
                      "TC10 P_AGE_1_TIDE_YOUTH B4",
           "P-WIN-1": "— IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: direction "
                      "informed by TC6V L-LAG deciles",
           "P-BRK-4H": "— IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: the best of "
                       "7,920 TC10 census cells"}
FORFEIT_T = "on per-campaign expectancy only; the gate forfeits +"
# L-R.2 / SC-14 referees, typed: the lens each SCALE row consumes (its text of record), the
# CLASSIC5 assets whose pick changed first-half-of-tuning vs tuning at that lens, the
# PANEL17 assets whose 4h pick fell back to the whole tape — each also re-read by THIS file
# from SCALE_PICKS.json (a second object) and required equal
SCALE_LENS_T = {"P-BRK-4H": "4h", "P-ADD-BRK": "1h", "P-ADD-SFP": "1h", "P-TP-RNG": "12h"}
PICK_CHANGED_T = {"1h": ("BTCUSDT", "SOLUSDT", "NEARUSDT"), "4h": ("NEARUSDT",),
                  "12h": ("BTCUSDT", "ETHUSDT", "SOLUSDT")}
FALLBACK_4H_T = ("HYPEUSDT", "PUMPUSDT")
FROZEN_T = {"P-BRK-4H": "tierE__frozen_3_0_twin", "P-ADD-BRK": "tierE__frozen_3_0_twin",
            "P-ADD-SFP": "tierE__frozen_3_0_twin", "P-TP-RNG": None}
HOLDOUT_ARM_T = {"P-BRK-4H": "tierE__holdout_slice", "P-ADD-BRK": None,
                 "P-ADD-SFP": "tierE__holdout_slice", "P-TP-RNG": None}
FALLBACK_LAB_T = "IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): "


def own_record_changes() -> tuple[dict, tuple]:
    raw = json.loads((E.OUT / "ranges" / "SCALE_PICKS.json").read_text(encoding="utf-8"))
    ch = {lens: tuple(a for a in CLASSIC5_T if any(
        c["asset"] == a and c["lens"] == lens and c["stable_first_half_vs_tuning"] is False
        for c in raw["cells"])) for lens in ("1h", "4h", "12h")}
    fb4 = tuple(sorted(x.rsplit(" ", 1)[0] for x in raw["fallback_cells"]
                       if x.endswith(" 4h") and x.rsplit(" ", 1)[0] in PANEL17_T))
    return ch, fb4


def _sorted_arm(root: Path, rid: str, arm: str) -> pd.DataFrame:
    return read_arm(root, rid, arm).sort_values(["symbol", "entry_close_ms"],
                                                kind="mergesort").reset_index(drop=True)


def own_stat(ruler: str, a: pd.DataFrame, b) -> tuple[int, float]:
    """n and point by THIS file's law: vs zero = mean net_r; paired = mean of per-campaign
    deltas keyed (symbol, entry_ms)."""
    if ruler == "vs_zero":
        v = a["net_r"].to_numpy(float)
        return len(v), float(np.mean(v))
    dv, _ = own_deltas(a, b)
    return len(dv), float(np.mean(dv))


def scale_findings(rows: dict, root: Path) -> list[str]:
    """MAJOR-2: what L-R.2 requires beside the four SCALE-IN-SAMPLE verdicts, checked
    against THIS file's own era=='holdout' (by close) ruling, the typed frozen arms and
    the typed pick-stability flags."""
    out = []
    ch, fb4 = own_record_changes()
    if ch != PICK_CHANGED_T or fb4 != FALLBACK_4H_T:
        out.append(f"SCALE-STABILITY-RECORD: SCALE_PICKS.json reads {ch} / {fb4} != typed "
                   f"{PICK_CHANGED_T} / {FALLBACK_4H_T}")
    for rid in SCALE_T:
        r = rows[rid]
        sb = r.get("scale_beside") or {}
        lens, ruler = SCALE_LENS_T[rid], RULER_T[rid]
        a = _sorted_arm(root, rid, "scored")
        b = None if ruler == "vs_zero" else _sorted_arm(root, rid, "base")
        ah = a[era_t(a["entry_close_ms"]) == "holdout"]
        bh = None if b is None else b[era_t(b["entry_close_ms"]) == "holdout"]
        n, pt = own_stat(ruler, ah, bh)
        hs = sb.get("holdout_slice_derived") or {}
        if hs.get("n") != n or hs.get("point") != pt:
            out.append(f"SCALE-CONTENT: {rid} holdout slice printed n {hs.get('n')} point "
                       f"{hs.get('point')} != this file's era=='holdout' (by close) n {n} point "
                       f"{pt}")
        cell = str(r.get("verdict_cell"))
        if f"holdout slice, derived: n {n}, {pt:+.4f}" not in cell:
            out.append(f"SCALE-CONTENT: {rid} §0 cell lacks 'holdout slice, derived: n {n}, "
                       f"{pt:+.4f}'")
        f_arm = FROZEN_T[rid]
        if sb.get("frozen_arm") != f_arm:
            out.append(f"SCALE-CONTENT: {rid} frozen-3.0 twin {sb.get('frozen_arm')!r} != typed "
                       f"{f_arm!r}")
        if f_arm:
            fn, fpt = own_stat(ruler, _sorted_arm(root, rid, f_arm), b)
            fs = sb.get("frozen_arm_stat") or {}
            if fs.get("n") != fn or fs.get("point") != fpt or \
                    f"frozen-3.0 twin {f_arm}: n {fn}, {fpt:+.4f}" not in cell:
                out.append(f"SCALE-CONTENT: {rid} frozen twin printed n {fs.get('n')} point "
                           f"{fs.get('point')} != this file's n {fn} point {fpt}")
        elif "frozen-3.0 twin: ABSENT" not in cell:
            out.append(f"SCALE-CONTENT: {rid} (no frozen arm filed) does not print ABSENT")
        if sb.get("holdout_arm") != HOLDOUT_ARM_T[rid]:
            out.append(f"SCALE-CONTENT: {rid} filed holdout arm {sb.get('holdout_arm')!r} != "
                       f"typed {HOLDOUT_ARM_T[rid]!r}")
        want = list(PICK_CHANGED_T[lens])
        ps = sb.get("pick_stability") or {}
        clause = cell[cell.find("pick stability ("):].split(";")[0] if "pick stability (" in \
            cell else ""
        if (ps.get("changed_assets") != want or not clause.startswith(f"pick stability ({lens},")
                or "CHANGED on" not in clause or any(x not in clause for x in want)
                or any(x in clause for x in CLASSIC5_T if x not in want)):
            out.append(f"SCALE-STABILITY: {rid} ({lens}) flags {ps.get('changed_assets')} / "
                       f"clause {clause[:110]!r} != exactly typed {want}")
        for t in r["tier_e"]:
            fl = t.get("scale_flags") or ""
            if "frozen" in t["arm"]:
                if not fl.startswith("frozen 3.0"):
                    out.append(f"SCALE-STABILITY: {rid}/{t['arm']} (frozen) flags {fl!r}")
            elif f"pick stability {lens}: CHANGED on {', '.join(want)} (" not in fl:
                out.append(f"SCALE-STABILITY: {rid}/{t['arm']} flags {fl!r} lack the {lens} "
                           f"change on {want}")
        ins = sb.get("holdout_in_sample") or {}
        own_ins = (int((ah["die_close_ms"].astype(np.int64) <= ERA_CUT_T).sum())
                   if "die_close_ms" in ah.columns else None)
        if ins.get("in_sample") != own_ins:
            out.append(f"SCALE-CONTENT: {rid} in-sample range reads in the holdout slice "
                       f"{ins.get('in_sample')} != this file's {own_ins}")
    t17 = next((t for t in rows["P-BRK-4H"]["tier_e"] if t["arm"] == "tierE__17_asset_view"), {})
    lab = FALLBACK_LAB_T + ", ".join(f"{x} 4h" for x in FALLBACK_4H_T)
    if lab not in (t17.get("scale_flags") or ""):
        out.append(f"SCALE-FALLBACK: P-BRK-4H/tierE__17_asset_view flags "
                   f"{t17.get('scale_flags')!r} lack {lab!r}")
    for rid in SCALE_T:
        for t in rows[rid]["tier_e"]:
            if t["arm"] != "tierE__17_asset_view" and FALLBACK_LAB_T in (t.get("scale_flags") or ""):
                out.append(f"SCALE-FALLBACK: {rid}/{t['arm']} (CLASSIC5) carries a fallback label")
    return out


SENS_CASES_T = ("P-ADD-SFP", "P-AGE-1", "P-BRK-4H")        # one registration per ruler


def sens_findings() -> list[str]:
    """The verdict at the sensitivity seed is ruled on THAT seed's draws: under a harness
    T5 whose draws are +1 at the seed of record and -1 at the sensitivity seed (typed),
    each ruler's row must read SUPPORTED / 'NOT SUPPORTED — CI wholly below zero' /
    unstable."""
    def boot(v, c, seed, n_boot):
        return np.full(n_boot, 1.0 if seed == SEED else -1.0)

    def boot_diff(va, ca, vb, cb, seed, n_boot):
        return np.full(n_boot, 1.0 if seed == SEED else -1.0)

    fake = SimpleNamespace(cluster_boot=boot, cluster_boot_diff=boot_diff,
                           _ci_from=S.T5._ci_from, d15=S.T5.d15)
    out = []
    root = planted_run()["root"]
    with mutated(S, "T5", fake):
        for rid in SENS_CASES_T:
            try:
                r = score_one(root, rid)
            except SystemExit as e:             # a module HALT is a finding, never swallowed
                out.append(f"SENS-VERDICT: {rid} HALT {str(e)[:160]}")
                continue
            if not (r.get("verdict_of_record") == "SUPPORTED"
                    and r.get("verdict_at_sens_seed") == "NOT SUPPORTED — CI wholly below zero"
                    and r.get("verdict_stable_across_seeds") is False):
                out.append(f"SENS-VERDICT: {rid} (draws +1 at {SEED}, -1 at {SEED_SENS}) reads "
                           f"{r.get('verdict_of_record')!r} / sens "
                           f"{r.get('verdict_at_sens_seed')!r} / stable "
                           f"{r.get('verdict_stable_across_seeds')}")
    return out


def s0_rows(md: str) -> list[list[str]]:
    """The §0 table's data rows, parsed from S0_VERDICTS.md by THIS file."""
    seg = md.split("## §0 table", 1)[1].split("## Family", 1)[0]
    rows = [ln for ln in seg.splitlines() if ln.startswith("| ") and not ln.startswith("| #")]
    return [[c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]] for ln in rows]


def verdict_findings() -> list[str]:
    out = []
    for lo, hi, p, want in VERDICT_CASES_T:
        got = S.verdict_of_record(lo, hi, p)
        if got != want:
            out.append(f"VERDICT-CASE: (lo {lo}, hi {hi}, p {p}) reads {got!r} != typed {want!r}")
    R = planted_run()
    rows = R["rows"]
    m = rows["P-ADD-BRK"]["stats"]["main"]
    if not (m["lo"] > 0 and Fraction(m["p_num"], m["p_den"]) > BAR_T):
        out.append(f"PLANT-MISSED: P-ADD-BRK lo {m['lo']} p {m['p_one_sided']} is not the "
                   f"named case (lo > 0, p > 1/90) — a FIXTURE defect")
    for rid, want in (("P-ADD-BRK", "NOT SUPPORTED"), ("P-ADD-SFP", "SUPPORTED"),
                      ("P-TP-RNG", "NOT SUPPORTED — CI wholly below zero")):
        if rows[rid]["verdict_of_record"] != want or not rows[rid]["verdict_cell"].startswith(want):
            out.append(f"VERDICT-ROW: {rid} reads {rows[rid]['verdict_of_record']!r} != {want!r}")
    if rows["P-ADD-BRK"]["verdict_cell"].startswith("SUPPORTED"):
        out.append("VERDICT-ROW: P-ADD-BRK cell starts SUPPORTED")
    for rid in NINE_T:
        cell = str(rows[rid]["verdict_cell"])
        if rid in LABEL_T and LABEL_T[rid] not in cell:
            out.append(f"LABEL: {rid} lacks {LABEL_T[rid][:60]!r}")
        if rid not in LABEL_T and "IN-SAMPLE RE-SCORE" in cell:
            out.append(f"LABEL: {rid} carries an honesty label its spec does not name")
        if (rid in SCALE_T) != ("SCALE-IN-SAMPLE" in cell) and rows[rid]["status"] == "BUILT":
            out.append(f"LABEL: {rid} SCALE-IN-SAMPLE flag {'missing' if rid in SCALE_T else 'spurious'}")
    if FORFEIT_T not in rows["P-AGE-1"]["verdict_cell"]:
        out.append("LABEL: P-AGE-1 (refused mean > 0) lacks the forfeits appendix")
    if FORFEIT_T in rows["P-WIN-1"]["verdict_cell"]:
        out.append("LABEL: P-WIN-1 (refused mean < 0) carries the forfeits appendix")
    g = rows["P-AGE-1"]["gate"]
    if f"+{g['refused_sum_r']:.4f} R total" not in rows["P-AGE-1"]["verdict_cell"]:
        out.append("LABEL: P-AGE-1 forfeits X is not the refused cohort's sum")
    md = R["files"]["S0_VERDICTS.md"].decode("utf-8")
    s0 = {r[0].split(" · ")[1]: r for r in s0_rows(md)}
    for rid, word in (("P-SCALP-2", "CLOSED BY PRECONDITION"), ("P-WARN-1", "CONDITION NOT MET")):
        r = rows[rid]
        line = s0.get(rid)
        if line is None:
            out.append(f"CLOSED-NUMBER: {rid} has no §0 line")
            continue
        numeric = [c for j, c in enumerate(line) if j not in (0, 4) and c != "—"]
        if numeric or r["spent_test"] or r["stats"] is not None:
            out.append(f"CLOSED-NUMBER: {rid} prints {numeric} / spent {r['spent_test']}")
        if not (line[4].startswith(word) and "no slot spent" in line[4]
                and str(r["status_reason"]) in line[4]):
            out.append(f"CLOSED-NUMBER: {rid} cell {line[4][:80]!r} lacks its reason / 'no slot "
                       f"spent'")
    fam = json.loads(R["files"]["FAMILY.json"])
    fr = {x["registration"]: x for x in fam["rows"]}
    if (fam["family_m"], fam["bar_filed"], fam["tests_spent"], len(fam["rows"])) != (9, 0.011111,
                                                                                    7, 9):
        out.append(f"FAMILY: m {fam['family_m']} bar {fam['bar_filed']} spent "
                   f"{fam['tests_spent']} rows {len(fam['rows'])} != 9 / 0.011111 / 7 / 9")
    if Fraction(fam["bar"]).limit_denominator(1000) != BAR_T:
        out.append(f"FAMILY: bar {fam['bar']} != 1/90")
    if fr["P-SCALP-2"]["spent_test"] or fr["P-WARN-1"]["spent_test"]:
        out.append("FAMILY: a closed registration spent a test")
    # AM-3: the add rows print Σ add_r and the absorbed funding beside Δ (this file's sums)
    for rid in ("P-ADD-BRK", "P-ADD-SFP"):
        a = read_arm(R["root"], rid, "scored").sort_values(
            ["symbol", "entry_close_ms"], kind="mergesort").reset_index(drop=True)
        b = read_arm(R["root"], rid, "base")
        dv, _ = own_deltas(a, b)                        # (symbol, entry_ms) order
        ad = rows[rid].get("adds") or {}
        want = (float(np.sum(dv)), float(np.sum(a["add_r"].to_numpy(float))),
                float(np.sum(a["funding_r_uncapped"].to_numpy(float)
                             - a["funding_r"].to_numpy(float)))
                - float(np.sum(a["v6_funding_absorbed_r"].to_numpy(float))))
        got = (ad.get("sum_delta_r"), ad.get("sum_add_r"), ad.get("sum_absorbed_funding_r"))
        if not ad.get("carried") or got != want:
            out.append(f"ADDS: {rid} beside-print {got} != this file's (ΣΔ, Σ add_r, absorbed) "
                       f"{want}")
        if "Σ add_r" not in s0[rid][1]:
            out.append(f"ADDS: {rid} §0 line lacks Σ add_r")
    if rows["P-TP-RNG"].get("adds") is not None:
        out.append("ADDS: P-TP-RNG (not an add rule) carries an adds block")
    out += scale_findings(rows, R["root"])
    out += sens_findings()
    return out


def verdict_break():
    def ci_only(lo, hi, p):
        return "SUPPORTED" if (lo is not None and lo > 0) else "NOT SUPPORTED"

    real_s0 = S.s0_line

    def numbered(r):
        x = real_s0(r)
        if not r.get("stats"):
            x = [x[0], "0", "+0.0000", "[+0.0000, +0.0000]", x[4], "1.000000", "0/5 above",
                 "+0.0000", "—"]
        return x

    def under(pairs):
        def thunk():
            with contextlib.ExitStack() as st:
                for obj, name, val in pairs:
                    st.enter_context(mutated(obj, name, val))
                _MEMO_SAVE = dict(_MEMO)
                try:
                    if any(n in ("s0_line", "hazard_of", "adds_block") for _, n, _v in pairs):
                        R = _MEMO
                        res = S.score_all(R["root"], banner=PLANT_BANNER, n_boot=199) \
                            if any(n in ("hazard_of", "adds_block") for _, n, _v in pairs) \
                            else R["res"]
                        _MEMO.update({"res": res, "files": S.render(res),
                                      "rows": {r["registration"]: r for r in res["rows"]}})
                    return verdict_findings()
                finally:
                    _MEMO.clear()
                    _MEMO.update(_MEMO_SAVE)
        return thunk

    real_slug, real_ps = S._slug_pick, S.pick_stability

    def no_frozen(te, exact, sub):
        return None if sub == "frozen" else real_slug(te, exact, sub)

    def no_stability(picks, lens, df):
        x = real_ps(picks, lens, df)
        return {**x, "changed_assets": [], "changed": [],
                "text": f"pick stability ({lens}): printed", "short": f"pick stability {lens}"}

    def scale_under(obj, name, val):
        def thunk():
            root = planted_run()["root"]
            with mutated(obj, name, val):
                return scale_findings({rid: score_one(root, rid) for rid in SCALE_T}, root)
        return thunk

    def sens_collapsed():
        with mutated(S, "SEED_SENS", S.SEED):
            return sens_findings()

    return plants([
        ("the SCALE 'holdout slice' computed on the tuning era", "SCALE-CONTENT",
         scale_under(S, "SCALE_CAUSAL_ERA", "tuning")),
        ("the frozen-3.0 twin dropped from the SCALE cell", "SCALE-CONTENT",
         scale_under(S, "_slug_pick", no_frozen)),
        ("the pick-stability flag dropped (L-R.2)", "SCALE-STABILITY",
         scale_under(S, "pick_stability", no_stability)),
        ("P-TP-RNG's consumed lens read as 4h", "SCALE-STABILITY: P-TP-RNG",
         scale_under(S, "SCALE_LENS_OF", {**S.SCALE_LENS_OF, "P-TP-RNG": "4h"})),
        ("the whole-tape fallback IN-SAMPLE label dropped", "SCALE-FALLBACK",
         scale_under(S, "fallback_label", lambda picks, lens, df: None)),
        ("the sensitivity seed collapsed onto the seed of record", "SENS-VERDICT",
         sens_collapsed),
        ("a CI-only verdict (clause (b) dropped)", "VERDICT-CASE",
         under([(S, "verdict_of_record", ci_only)])),
        ("the bar loosened to 0.10/7 (tests actually run)", "VERDICT-CASE",
         under([(S, "BAR_FRAC", Fraction(1, 70)), (S, "BAR", 0.10 / 7)])),
        ("a closed row printing a number", "CLOSED-NUMBER", under([(S, "s0_line", numbered)])),
        ("the honesty label dropped", "LABEL", under([(S, "hazard_of", lambda spec: None)])),
        ("the AM-3 beside-print dropped", "ADDS",
         under([(S, "adds_block", lambda a, b: {"carried": False, "note": "dropped"})])),
    ])


def verdict_real():
    bad = verdict_findings()
    rows = planted_run()["rows"]
    m = rows["P-ADD-BRK"]["stats"]["main"]
    return (not bad), (f"{len(VERDICT_CASES_T)} typed cases read as typed (lo>0 & p 0.03 -> NOT "
                       f"SUPPORTED; 44/4001 -> SUPPORTED; 45/4001 -> NOT); planted P-ADD-BRK lo "
                       f"{m['lo']:+.4f} > 0, p {m['p_num']}/{m['p_den']} > 1/90 -> NOT SUPPORTED; "
                       f"P-ADD-SFP SUPPORTED; P-TP-RNG '— CI wholly below zero'; labels pre_seen "
                       f"/ selection_hazard x2 / SCALE-IN-SAMPLE x4 / forfeits on P-AGE-1 only; "
                       f"AM-3 ΣΔ / Σ add_r / absorbed funding on both add rows == this file's "
                       f"sums exactly; "
                       f"P-SCALP-2 and P-WARN-1 print no number, 'no slot spent'; FAMILY m 9, bar "
                       f"0.011111 (1/90), 7 tests spent; SCALE-IN-SAMPLE x4: the holdout slice n / "
                       f"point == this file's era=='holdout' (by close) ruling, the frozen twin "
                       f"== typed (3 filed, P-TP-RNG ABSENT) with n / point == this file's, pick "
                       f"stability flags exactly the typed changes (1h BTC SOL NEAR; 4h NEAR; 12h "
                       f"BTC ETH SOL) on the §0 cell and every consuming Tier-E row, frozen rows "
                       f"say so, the in-sample holdout count == this file's, the 17-asset view "
                       f"labelled IN-SAMPLE for HYPE / PUMP 4h; the sensitivity-seed verdict "
                       f"ruled on its own draws on {len(SENS_CASES_T)} rulers"
                       + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-STATUS
PRECOND_T = "P-SCALP-2"                 # the one registration with a precondition (L-S.1)
COND_T = "P-WARN-1"                     # the one registration with a condition (L-W.4)
R2_TUNING_1H_T = "FAIL"                 # the R2 record's tuning-era 1h word (typed; re-read)
R2_HOLDOUT_1H_T = "FAIL"                # the R2 1h lens word of record (typed; re-read)


def _status(root: Path, rid: str) -> dict:
    return json.loads((root / rid / "STATUS.json").read_text(encoding="utf-8"))


def _halted_by(row: dict, want: str) -> bool:
    return (row["verdict_of_record"] == "HALT" and row["stats"] is None
            and not row["spent_test"] and any(want in h for h in row["halts"]))


def status_findings(tmp: Path) -> list[str]:
    """SC-17: a status word stands only where the spec names it AND its gating record
    agrees; the tuning-era R2 word rides P-SCALP-2's cell, collared [§10]."""
    out = []
    root = copy_family(tmp)
    # (a) STATUS-ILLEGAL on EVERY registration without the word's precondition / condition
    for rid in NINE_T:
        st = _status(root, rid)
        for word, owner in (("CLOSED_BY_PRECONDITION", PRECOND_T),
                            ("CONDITION_NOT_MET", COND_T)):
            if rid == owner:
                continue
            write_status(root, rid, word, "PLANTED illegal word", st["arms"])
            row = score_one(root, rid)
            if not _halted_by(row, "STATUS-ILLEGAL"):
                out.append(f"STATUS-NOT-ENFORCED: {rid} {word} -> {row['verdict_of_record']} "
                           f"{row['halts'][:1]}")
        write_status(root, rid, st["status"], st["reason"], st["arms"])
    # (b) the condition record vs P-WARN-1's word (four ways to disagree)
    st = _status(root, COND_T)
    cj = (root / COND_T / "condition.json").read_text(encoding="utf-8")
    for lab, word, met, hi in (("BUILT while the record says NOT MET", "BUILT", False, 0.05),
                               ("CONDITION_NOT_MET while the record says MET",
                                "CONDITION_NOT_MET", True, -0.1),
                               ("met False with ci_hi < 0 (L-W.4 broken)", "CONDITION_NOT_MET",
                                False, -0.1),
                               ("the record absent", "CONDITION_NOT_MET", None, None)):
        write_status(root, COND_T, word, "PLANTED", st["arms"])
        if met is None:
            (root / COND_T / "condition.json").unlink()
        else:
            condition_json(root, met, hi)
        row = score_one(root, COND_T)
        if not _halted_by(row, "CONDITION-RECORD"):
            out.append(f"CONDITION-NOT-ENFORCED: {COND_T} {lab} -> {row['verdict_of_record']} "
                       f"{row['halts'][:1]}")
    write_status(root, COND_T, st["status"], st["reason"], st["arms"])
    (root / COND_T / "condition.json").write_text(cj, encoding="utf-8")
    row = score_one(root, COND_T)
    if row["verdict_of_record"] != "CONDITION_NOT_MET" or (row.get("condition_record") or {}).get(
            "met") is not False:
        out.append(f"CONDITION-RECORD: the planted {COND_T} (NOT MET, record met False) reads "
                   f"{row['verdict_of_record']}")
    # (c) the R2 record vs P-SCALP-2's word: BUILT on a FAIL; CLOSED on a PASS; no record
    st = _status(root, PRECOND_T)
    raw = json.loads(Path(S.R2_VERDICTS_PATH).read_text(encoding="utf-8"))
    passed = copy.deepcopy(raw)
    passed["lenses"]["1h"]["verdict"] = "PASS"
    (tmp / "r2_pass.json").write_text(json.dumps(passed), encoding="utf-8")
    for lab, word, r2path in (("BUILT while the R2 1h word is FAIL", "BUILT", None),
                              ("CLOSED while the R2 1h word is PASS", "CLOSED_BY_PRECONDITION",
                               tmp / "r2_pass.json"),
                              ("CLOSED with no readable R2 record", "CLOSED_BY_PRECONDITION",
                               tmp / "absent_r2.json")):
        write_status(root, PRECOND_T, word, "PLANTED", st["arms"])
        with mutated(S, "R2_VERDICTS_PATH", r2path or S.R2_VERDICTS_PATH):
            row = score_one(root, PRECOND_T)
        if not _halted_by(row, "PRECONDITION-RECORD"):
            out.append(f"PRECONDITION-NOT-ENFORCED: {PRECOND_T} {lab} -> "
                       f"{row['verdict_of_record']} {row['halts'][:1]}")
    write_status(root, PRECOND_T, st["status"], st["reason"], st["arms"])
    # (d) §10: the tuning-era R2 word beside P-SCALP-2's closed row, collared
    if (raw["lenses"]["1h"].get("tier_e_tuning_word"), raw["lenses"]["1h"].get("verdict")) != (
            R2_TUNING_1H_T, R2_HOLDOUT_1H_T):
        out.append(f"R2-TUNING-WORD: the R2 record's 1h words != typed ({R2_TUNING_1H_T}, "
                   f"{R2_HOLDOUT_1H_T})")
    row = score_one(root, PRECOND_T)
    cell = str(row["verdict_cell"])
    want = f"the tuning-era R2 1h word {R2_TUNING_1H_T} (holdout word of record {R2_HOLDOUT_1H_T})"
    if not (row["verdict_of_record"] == "CLOSED_BY_PRECONDITION" and want in cell
            and all(f"{v}" in cell for v in COLLAR_T.values()) and "gates nothing" in cell
            and (row.get("r2_beside") or {}).get("tier") == COLLAR_T["tier"]):
        out.append(f"R2-TUNING-WORD: {PRECOND_T} cell {cell[-160:]!r} lacks {want!r} collared")
    if (row.get("precondition_record") or {}).get("word_of_record") != R2_HOLDOUT_1H_T:
        out.append(f"PRECONDITION-RECORD: the planted {PRECOND_T} record "
                   f"{row.get('precondition_record')} != the R2 1h word")
    return out


def status_break():
    def under(name, val):
        def thunk():
            with tempfile.TemporaryDirectory() as td, mutated(S, name, val):
                return status_findings(Path(td))
        return thunk

    return plants([
        ("the STATUS-ILLEGAL guard removed", "STATUS-NOT-ENFORCED",
         under("status_word_findings", lambda rid, status, spec: [])),
        ("the condition record not cross-checked", "CONDITION-NOT-ENFORCED",
         under("condition_record", lambda regdir, rid, status: ([], None))),
        ("the R2 precondition record not cross-checked", "PRECONDITION-NOT-ENFORCED",
         under("precondition_record", lambda r2, rid, status: ([], None))),
        ("the tuning-era R2 word not printed beside P-SCALP-2", "R2-TUNING-WORD",
         under("r2_beside", lambda r2, rid: None)),
    ])


def status_real():
    with tempfile.TemporaryDirectory() as td:
        bad = status_findings(Path(td))
    return (not bad), (f"CLOSED_BY_PRECONDITION on each of the 8 registrations without a "
                       f"precondition and CONDITION_NOT_MET on each of the 8 without a condition "
                       f"HALT STATUS-ILLEGAL (16/16); P-WARN-1 HALTs CONDITION-RECORD on BUILT vs "
                       f"met False, NOT MET vs met True, met False with ci_hi < 0 and an absent "
                       f"record (4/4), and the planted NOT MET row agrees with its record; "
                       f"P-SCALP-2 HALTs PRECONDITION-RECORD on BUILT vs R2 1h FAIL, CLOSED vs "
                       f"PASS and no readable record (3/3); its closed cell prints the tuning-era "
                       f"R2 1h word {R2_TUNING_1H_T} beside, collared [§10]"
                       + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-COLLAR
def own_reading(lo, hi) -> str:
    if lo is None or hi is None:
        return CI_READ_T["none"]
    return (CI_READ_T["above"] if lo > 0 else CI_READ_T["below"] if hi < 0
            else CI_READ_T["includes"])


def collar_check(rows: list[dict]) -> list[str]:
    """THIS file's collar law, typed."""
    out = []

    def walk(x, path):
        if isinstance(x, dict):
            for k, v in x.items():
                if FORBID_KEY_T.search(str(k)):
                    out.append(f"F-COLLAR: {path}.{k} is a verdict field")
                walk(v, f"{path}.{k}")
        elif isinstance(x, list):
            for j, v in enumerate(x):
                walk(v, f"{path}[{j}]")
        elif isinstance(x, str) and VERDICT_RX_T.search(x):
            out.append(f"F-COLLAR: {path} carries a verdict word {x[:60]!r}")

    for r in rows:
        tag = f"{r.get('registration')}/{r.get('arm')}"
        for k, v in COLLAR_T.items():
            if r.get(k) != v:
                out.append(f"F-COLLAR: {tag} {k} {r.get(k)!r} != {v!r}")
        if r.get("would_read_ci_only") != own_reading(r.get("ci_lo"), r.get("ci_hi")):
            out.append(f"F-COLLAR: {tag} would_read_ci_only {r.get('would_read_ci_only')!r} != "
                       f"the reading of its own interval")
        walk(r, tag)
    return out


def tier_e_rows() -> list[dict]:
    return [t for r in planted_run()["res"]["rows"] for t in r["tier_e"]]


def collar_real_findings(rows: list[dict], md: str) -> list[str]:
    out = collar_check(rows)
    got = sorted(f"{t['registration']}|{t['arm']}" for t in rows)
    if got != sorted(TIER_E_DECLARED_T):
        out.append(f"F-COLLAR: Tier-E rows {len(got)} != declared {len(TIER_E_DECLARED_T)}; "
                   f"missing {sorted(set(TIER_E_DECLARED_T) - set(got))} extra "
                   f"{sorted(set(got) - set(TIER_E_DECLARED_T))}")
    seg = md.split("## Tier-E rows", 1)[1].split("## F-BASE-IDENT", 1)[0]
    lines = [ln for ln in seg.splitlines() if ln.startswith("| P-")]
    for ln in lines:
        if not all(v in ln for v in COLLAR_T.values()) or VERDICT_RX_T.search(ln):
            out.append(f"F-COLLAR: S0_VERDICTS.md Tier-E line lacks the collar: {ln[:80]}")
    if len(lines) != len(TIER_E_DECLARED_T):
        out.append(f"F-COLLAR: S0_VERDICTS.md Tier-E table {len(lines)} lines != "
                   f"{len(TIER_E_DECLARED_T)}")
    return out


def collar_break():
    rows = tier_e_rows()
    md = planted_run()["files"]["S0_VERDICTS.md"].decode("utf-8")

    def bend(fn):
        c = copy.deepcopy(rows)
        fn(c[3])
        return c

    def word(r):
        r["note"] = "reads SUPPORTED on the CI alone"

    def drop(r):
        del r["gates"]

    def reword(r):
        r["gates"] = "NOTHING — Tier-E"

    def wr(r):
        r["would_read_ci_only"] = "SUPPORTED (CI-only)"

    def module_drop():
        real = S.tier_e_row

        def no_collar(*a, **k):
            x = real(*a, **k)
            x.pop("selection_not_a_result", None)
            return x
        with mutated(S, "tier_e_row", no_collar):
            L = S.Loader(planted_run()["root"], S._fees())
            doc, _ = S.load_registry(ROOT)
            spec = S.spec_of(doc["registrations"][3])
            t = S.score_tier_e(L, "P-BRK-4H", "tierE__frozen_3_0_twin", spec, None, "", None, 99)
        return S.collar_findings([t])

    def side_no_collar():
        with tempfile.TemporaryDirectory() as td:
            root = copy_family(Path(td))
            js = json.loads((root / "P-WIN-1" / "tierE__shadow_cut.json").read_text())
            js.pop("gates")
            (root / "P-WIN-1" / "tierE__shadow_cut.json").write_text(json.dumps(js))
            A = S.load_arm(root / "P-WIN-1", "P-WIN-1", "tierE__shadow_cut", S._fees())
            return A["halts"]

    return plants([
        ("a verdict word in a Tier-E note (this file's law)", "F-COLLAR",
         lambda: collar_real_findings(bend(word), md)),
        ("a verdict word in a Tier-E note (the scorer's guard)", "COLLAR-VERDICT-WORD",
         lambda: S.collar_findings(bend(word))),
        ("the gates column dropped (this file)", "F-COLLAR: P-",
         lambda: collar_check(bend(drop))),
        ("the gates column dropped (the scorer's guard)", "COLLAR-MISSING",
         lambda: S.collar_findings(bend(drop))),
        ("gates re-worded (the scorer's guard)", "COLLAR-VALUE",
         lambda: S.collar_findings(bend(reword))),
        ("would_read_ci_only = a verdict (this file)", "F-COLLAR",
         lambda: collar_check(bend(wr))),
        ("the module's Tier-E row builder dropping the collar", "COLLAR-MISSING", module_drop),
        ("a Tier-E sidecar without its collar (input)", "SIDECAR-COLLAR", side_no_collar),
    ])


def collar_real():
    rows = tier_e_rows()
    md = planted_run()["files"]["S0_VERDICTS.md"].decode("utf-8")
    bad = collar_real_findings(rows, md) + S.collar_findings(rows)
    reads = {}
    for t in rows:
        reads[t["would_read_ci_only"]] = reads.get(t["would_read_ci_only"], 0) + 1
    return (not bad), (f"{len(rows)} Tier-E rows == the {len(TIER_E_DECLARED_T)} declared; every "
                       f"one collared exactly, no verdict word or verdict field, "
                       f"would_read_ci_only == the reading of its own interval "
                       f"({dict(sorted(reads.items()))}); the S0_VERDICTS.md Tier-E table "
                       f"carries the collar on every line; the scorer's guard agrees"
                       + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-BASE-IDENT
def own_v6_findings(base: pd.DataFrame) -> list[str]:
    v = pd.read_parquet(str(E.OUT / "books" / "v6_campaigns.parquet"))
    out = []
    kv = {(s, int(e)): j for j, (s, e) in enumerate(zip(v["symbol"], v["entry_ms"]))}
    kb = {(s, int(e)): j for j, (s, e) in enumerate(zip(base["symbol"], base["entry_ms"]))}
    if set(kv) != set(kb) or len(base) != V6_N_T:
        return [f"own: keys differ ({len(kb)} vs {len(kv)})"]
    for bc, vc in V6_CMP_T:
        for key, jb in kb.items():
            x, y = base[bc].iloc[jb], v[vc].iloc[kv[key]]
            if isinstance(y, float):
                eq = round(float(x), 6) == float(y)
            else:
                eq = str(x) == str(y) if isinstance(y, str) else int(x) == int(y)
            if not eq:
                out.append(f"own: {bc} {key}: {x!r} vs {y!r}")
                break
    return out


def ident_break():
    root = planted_run()["root"]
    v6, _ = S.v6_frame()
    fees = S._fees()

    def bases():
        out = {}
        for rid in BASE7_T:
            A = S.load_arm(root / rid, rid, "base", fees)
            out[rid] = {"df": A["df"], "sha": A["sha"]}
        return out

    def bent(fn):
        b = bases()
        fn(b)
        for rid in b:
            b[rid]["sha"] = S.book_sha256(b[rid]["df"])
        return S.base_ident(b, v6)["findings"]

    def nudge(b):
        d = b["P-TP-RNG"]["df"].copy()
        d.loc[5, "net_r"] = float(d.loc[5, "net_r"]) + 1e-6
        b["P-TP-RNG"]["df"] = d

    def dropped(b):
        b["P-RELAY-1"]["df"] = b["P-RELAY-1"]["df"].drop(index=11).reset_index(drop=True)

    def moved_all(b):
        for rid in b:
            d = b[rid]["df"].copy()
            d.loc[0, "exit_close_ms"] = int(d.loc[0, "exit_close_ms"]) - 3 * MS_H
            b[rid]["df"] = d

    def wrong_claim():
        with tempfile.TemporaryDirectory() as td:
            r = copy_family(Path(td))
            js = json.loads((r / "P-WIN-1" / "base.json").read_text())
            js["book_sha256"] = "0" * 64
            (r / "P-WIN-1" / "base.json").write_text(json.dumps(js))
            return S.load_arm(r / "P-WIN-1", "P-WIN-1", "base", fees)["halts"]

    def row_halts():
        """Each of the seven, bent in turn: its row must HALT citing F-BASE-IDENT (the
        planted CONDITION_NOT_MET P-WARN-1: its Tier-E rule-book row) — all 7 or VOID."""
        got, missed = [], []
        with tempfile.TemporaryDirectory() as td:
            r = copy_family(Path(td))
            for rid in BASE7_T:
                h = bent_base_halts(r, rid)
                (got if h else missed).append(rid)
        if missed:
            return [f"NOT HALTED on {missed}"]
        return [f"F-BASE-IDENT halts the bent row on {len(got)}/7: {got}"]

    return plants([
        ("one base net_r +1e-6 (P-TP-RNG)", "BASE-IDENT", lambda: bent(nudge)),
        ("one base row dropped (P-RELAY-1)", "BASE-V6: P-RELAY-1/base keys", lambda: bent(dropped)),
        ("every base's first exit_close_ms moved -3h (1h-resolved style)", "BASE-V6",
         lambda: bent(moved_all)),
        ("a base sidecar claiming a wrong book_sha256", "BOOK-SHA", wrong_claim),
        ("a registration whose base differs: its row must HALT", "F-BASE-IDENT", row_halts),
    ])


def bent_base_halts(root: Path, rid: str) -> list[str]:
    """Bend `rid`'s base (row 0 +0.5 R), score it, restore; the F-BASE-IDENT halt(s)."""
    keep = read_arm(root, rid, "base")
    rewrite_arm(root, rid, "base", with_net(keep, keep["net_r"].to_numpy() + np.where(
        np.arange(len(keep)) == 0, 0.5, 0.0), fee_table()))
    row = score_one(root, rid)
    rewrite_arm(root, rid, "base", keep)
    if rid == "P-WARN-1":
        t = next((t for t in row["tier_e"] if t["arm"] == "scored"), {})
        return [t["halted"]] if "F-BASE-IDENT" in str(t.get("halted")) else []
    return [h for h in row["halts"] if "F-BASE-IDENT" in h] if (
        row["verdict_of_record"] == "HALT" and row["stats"] is None) else []


def ident_real():
    R = planted_run()
    root = R["root"]
    bi = json.loads(R["files"]["BASE_IDENT.json"])
    out = []
    shas = set()
    for rid in BASE7_T:
        d = read_arm(root, rid, "base")
        shas.add(pandas_sha(d))
        out += [f"{rid}: {f}" for f in own_v6_findings(d)]
    n_arms = 0
    for p in sorted(root.glob("*/*.parquet")):
        d = pd.read_parquet(str(p))
        js = json.loads(p.with_suffix(".json").read_text(encoding="utf-8"))
        n_arms += 1
        if not (S.book_sha256(d) == pandas_sha(d) == js["book_sha256"]):
            out.append(f"SC-13: {p.parent.name}/{p.stem} scorer {S.book_sha256(d)[:12]}… vs "
                       f"pandas {pandas_sha(d)[:12]}…")
    if len(shas) != 1:
        out.append(f"own: {len(shas)} base shas")
    # SC-7 scope, on EACH of the seven: its base bent -> ITS row halts, a clean neighbour's
    # row is still ruled
    with tempfile.TemporaryDirectory() as td:
        r2 = copy_family(Path(td))
        for rid in BASE7_T:
            nb = "P-ADD-SFP" if rid != "P-ADD-SFP" else "P-TP-RNG"
            h = bent_base_halts(r2, rid)
            keep = read_arm(r2, rid, "base")
            rewrite_arm(r2, rid, "base", with_net(keep, keep["net_r"].to_numpy() + np.where(
                np.arange(len(keep)) == 0, 0.5, 0.0), fee_table()))
            clean = score_one(r2, nb)
            rewrite_arm(r2, rid, "base", keep)
            if not h or clean["verdict_of_record"] == "HALT":
                out.append(f"SCOPE: bent {rid} base -> halts {h[:1]}; clean {nb} -> "
                           f"{clean['verdict_of_record']}")
    if not (bi["ok"] and sorted(bi["registrations_checked"]) == sorted(BASE7_T)
            and len(set(bi["book_sha256"].values())) == 1 and bi["v6"]["n"] == V6_N_T
            and set(bi["book_sha256"].values()) == shas):
        out.append(f"record: BASE_IDENT.json ok {bi['ok']} checked {bi['registrations_checked']}")
    return (not out), (f"the {len(BASE7_T)} base arms carry ONE book_sha256 "
                       f"{next(iter(shas))[:16]}… and equal books/v6_campaigns.parquet on the "
                       f"13 typed columns at 6 dp (this file's own join, n {V6_N_T}); "
                       f"BASE_IDENT.json agrees; each of the 7 bases bent in turn halts ITS row "
                       f"only (a clean neighbour is ruled); SC-13: the scorer's canonical CSV == pandas "
                       f"to_csv on all {n_arms} planted arms" + (f"; {out[:3]}" if out else ""))


# ═══════════════════════════════════════════════════════════════ F-GRID
def grid_tables(res: dict, files: dict) -> list[tuple]:
    md = files["S0_VERDICTS.md"].decode("utf-8")
    s0 = pd.DataFrame({"cell": [r[0].split(" · ")[1] for r in s0_rows(md)]})
    s0["verdict_cell"] = [r[4] for r in s0_rows(md)]
    fam = json.loads(files["FAMILY.json"])
    fr = pd.DataFrame({"cell": [x["registration"] for x in fam["rows"]],
                       "verdict_of_record": [x["verdict_of_record"] for x in fam["rows"]]})
    te = pd.DataFrame({"cell": [f"{t['registration']}|{t['arm']}" for r in res["rows"]
                                for t in r["tier_e"]]})
    te["tier"] = [t["tier"] for r in res["rows"] for t in r["tier_e"]]
    out = [("§0 table", list(NINE_T), s0, ("verdict_cell",)),
           ("FAMILY", list(NINE_T), fr, ("verdict_of_record",)),
           ("Tier-E table", list(TIER_E_DECLARED_T), te, ("tier",))]
    for r in res["rows"]:
        if r.get("stats"):
            lp = pd.DataFrame({"cell": [p["dropped"] for p in r["stats"]["loao"]["per_panel"]]})
            lp["note"] = [p["note"] for p in r["stats"]["loao"]["per_panel"]]
            out.append((f"LOAO {r['registration']}", list(CLASSIC5_T), lp, ("note",)))
    return out


def grid_findings(tables) -> list[str]:
    out = []
    for lab, dec, df, req in tables:
        ok, lines = TP.grid_whole(dec, df, "cell", require_cols=req, label=lab)
        if not ok:
            out.append(f"GRID: {lab}: " + " ; ".join(ln for ln in lines if ln.startswith("[BAD]")))
    return out


def grid_break():
    R = planted_run()
    tabs = grid_tables(R["res"], R["files"])

    def bent(k, fn):
        t = [list(x) for x in tabs]
        t[k][2] = fn(t[k][2].copy())
        return grid_findings([tuple(x) for x in t])

    return plants([
        ("a §0 row dropped", "GRID: §0 table", lambda: bent(0, lambda d: d.iloc[1:])),
        ("a FAMILY row duplicated", "GRID: FAMILY",
         lambda: bent(1, lambda d: pd.concat([d, d.iloc[:1]]))),
        ("an undeclared Tier-E row", "GRID: Tier-E table",
         lambda: bent(2, lambda d: pd.concat([d, pd.DataFrame({"cell": ["P-X|tierE__x"],
                                                                "tier": ["TIER-E"]})]))),
        ("a LOAO panel dropped", "GRID: LOAO", lambda: bent(3, lambda d: d.iloc[:-1])),
    ])


def grid_real():
    R = planted_run()
    tabs = grid_tables(R["res"], R["files"])
    bad = grid_findings(tabs)
    return (not bad), (f"{len(tabs)} grids WHOLE by TP.grid_whole against typed declared cells: "
                       f"§0 9/9, FAMILY 9/9, Tier-E {len(TIER_E_DECLARED_T)}/"
                       f"{len(TIER_E_DECLARED_T)}, {len(tabs) - 3} LOAO grids x 5 panels"
                       + (f"; {bad[:2]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-KEY
def key_break():
    root = planted_run()["root"]
    fees = S._fees()
    js = json.loads((root / "P-ADD-SFP" / "scored.json").read_text(encoding="utf-8"))
    df0 = read_arm(root, "P-ADD-SFP", "scored")

    def v(fn, side_fn=None, arm="scored"):
        d = fn(df0.copy())
        s = copy.deepcopy(js)
        s["book_sha256"] = pandas_sha(d) if all(c in d.columns for c in REQ_T) else s["book_sha256"]
        s["n"] = len(d)
        s["sum_net_r"] = float(d["net_r"].sum()) if "net_r" in d.columns else 0.0
        if side_fn:
            side_fn(s)
        return S.validate_book(d, s, "P-ADD-SFP", arm, fees)[0]

    def dup(d):
        return pd.concat([d, d.iloc[[4]]]).reset_index(drop=True)

    def nul(d):
        d.loc[2, "net_r"] = np.nan
        return d

    def era(d):
        d.loc[0, "era"] = "holdout" if d.loc[0, "era"] == "tuning" else "tuning"
        return d

    def dir0(d):
        d.loc[1, "direction"] = 0
        return d

    def hair(d):
        d.loc[6, "haircut_net_r"] = float(d.loc[6, "haircut_net_r"]) + 1e-6
        return d

    def f32(d):
        d["net_r"] = d["net_r"].astype(np.float32)
        return d

    def stray(d):
        d.loc[0, "symbol"] = "DOGEUSDT"
        return d

    def side_n(s):
        s["n"] = s["n"] + 1

    def side_sum(s):
        s["sum_net_r"] = s["sum_net_r"] + 1e-3

    def side_scope(s):
        s["era_scope"] = "holdout"

    def gap(d):
        d.loc[3, "entry_ms"] = int(d.loc[3, "entry_ms"]) - MS_4H     # entry bar 8h long
        return d

    def back(d):
        d.loc[4, "exit_close_ms"] = int(d.loc[4, "entry_close_ms"]) - MS_H
        return d

    def rdist(d):
        d.loc[5, "r_dist"] = 0.0
        return d

    def comma(d):
        d.loc[0, "lane"] = "card,adds"
        return d

    def dir64(d):
        d["direction"] = d["direction"].astype(np.int64)
        return d

    def ms32(d):
        d["exit_close_ms"] = (d["exit_close_ms"] // 1000).astype(np.int32)
        return d

    def era_by_open():
        with mutated(S, "ERA_TIME_COL", "entry_ms"):
            return key_real_findings()

    return plants([
        ("the era judged by the entry bar's OPEN (L-1.3 broken)", "REGBOOK-ERA: P-BRK-4H/scored",
         era_by_open),
        ("a sidecar sum_net_r off by 1e-3", "SIDECAR: P-ADD-SFP/scored sum_net_r",
         lambda: v(lambda d: d, side_sum)),
        ("a sidecar era_scope 'holdout' on a full-corridor book", "SIDECAR: P-ADD-SFP/scored "
         "era_scope holdout", lambda: v(lambda d: d, side_scope)),
        ("an entry bar longer than the 4h lens", "REGBOOK-TIME", lambda: v(gap)),
        ("an exit before the entry close", "REGBOOK-TIME", lambda: v(back)),
        ("r_dist 0", "REGBOOK-RDIST", lambda: v(rdist)),
        ("a ',' inside a lane string", "REGBOOK-STR", lambda: v(comma)),
        ("direction as int64", "REGBOOK-DTYPE: P-ADD-SFP/scored direction", lambda: v(dir64)),
        ("exit_close_ms as int32", "REGBOOK-DTYPE: P-ADD-SFP/scored exit_close_ms",
         lambda: v(ms32)),
        ("a duplicated (symbol, entry_close_ms) key", "REGBOOK-KEY", lambda: v(dup)),
        ("a null net_r", "REGBOOK-NULL", lambda: v(nul)),
        ("the lane column dropped", "REGBOOK-COLS", lambda: v(lambda d: d.drop(columns="lane"))),
        ("one row's era flipped", "REGBOOK-ERA", lambda: v(era)),
        ("a direction 0", "REGBOOK-DIR", lambda: v(dir0)),
        ("the haircut law broken by 1e-6 on one row", "REGBOOK-HAIRCUT", lambda: v(hair)),
        ("net_r as float32", "REGBOOK-DTYPE", lambda: v(f32)),
        ("a sidecar n one too many", "SIDECAR: P-ADD-SFP/scored n",
         lambda: v(lambda d: d, side_n)),
        ("a stray asset outside the declared panel", "STRAY-ASSET", lambda: v(stray)),
    ])


STRADDLES_T = {"P-BRK-4H/scored": 1, "P-BRK-4H/tierE__holdout_slice": 1}   # planted, typed


def key_real_findings() -> list[str]:
    """Every planted arm passes the interface; the planted straddle (open tuning, close
    holdout) reads 'holdout' and is counted where typed; score rows keyed, non-null."""
    R = planted_run()
    root = R["root"]
    fees = S._fees()
    out = []
    for p in sorted(root.glob("*/*.parquet")):
        rid, arm = p.parent.name, p.stem
        js = json.loads(p.with_suffix(".json").read_text(encoding="utf-8"))
        d = pd.read_parquet(str(p))
        h, _ = S.validate_book(d, js, rid, arm, fees)
        out += h
        own = int(((d["entry_ms"] <= ERA_CUT_T) & (d["entry_close_ms"] > ERA_CUT_T)).sum())
        if own != STRADDLES_T.get(f"{rid}/{arm}", 0):
            out.append(f"STRADDLE: {rid}/{arm} holds {own} straddling entry bar(s) != typed "
                       f"{STRADDLES_T.get(f'{rid}/{arm}', 0)}")
        if own and set(d.loc[(d["entry_ms"] <= ERA_CUT_T) & (d["entry_close_ms"] > ERA_CUT_T),
                             "era"]) != {"holdout"}:
            out.append(f"STRADDLE: {rid}/{arm} straddle row not 'holdout' by its close")
    prov = R["rows"]["P-BRK-4H"]["provenance"]["scored"]
    if prov.get("entry_bars_straddling_era_cut") != STRADDLES_T["P-BRK-4H/scored"]:
        out.append(f"STRADDLE: the scorer counts {prov.get('entry_bars_straddling_era_cut')} "
                   f"straddling entry bar(s) in P-BRK-4H/scored != typed 1")
    return out


def key_real():
    R = planted_run()
    root = R["root"]
    out = key_real_findings()
    n = len(list(root.glob("*/*.parquet")))
    sc = json.loads(R["files"]["SCORES.json"])
    ids = [r["registration"] for r in sc["rows"]]
    te = [(t["registration"], t["arm"]) for r in sc["rows"] for t in r["tier_e"]]
    if len(ids) != len(set(ids)) or len(te) != len(set(te)):
        out.append("KEY: duplicated score-row keys")
    for r in sc["rows"]:
        need = (("verdict_of_record", "verdict_cell", "status", "status_reason") if not r["stats"]
                else ("verdict_of_record", "verdict_cell", "status", "clears_bar"))
        if any(r.get(k) is None for k in need):
            out.append(f"KEY: {r['registration']} null in {need}")
        if r["stats"]:
            m = r["stats"]["main"]
            if any(m.get(k) is None for k in ("n", "point", "lo", "hi", "p_one_sided",
                                              "deciding_bound")):
                out.append(f"KEY: {r['registration']} null statistic")
    return (not out), (f"all {n} planted arms pass the interface (16 columns, exact dtypes, no "
                       f"nulls, no ',' '\"' CR LF in strings, unique keys, direction +-1, era by "
                       f"close — the planted 2024-06-30T20:00Z straddle reads 'holdout' and is "
                       f"counted 1 in P-BRK-4H/scored —, 0 < entry_close - entry_ms <= 4h, AM-7 "
                       f"haircut law, sidecar n/sum/sha/era_scope/collar); score rows keyed "
                       f"uniquely ({len(ids)} registrations, "
                       f"{len(te)} Tier-E), required fields non-null" + (f"; {out[:3]}" if out else ""))


# ═══════════════════════════════════════════════════════════════ F-CLOSURE
FORBIDDEN_T = ("rangefinder", "tierc10_census", "tierc10_stamps", "tierc10_null",
               "tierc11_nest")


def closure_scan(src: str) -> list[str]:
    out = [f"STATIC: {m}" for m in E.static_imports(src)
           if any(f in m for f in FORBIDDEN_T)]
    out += E.hook_escapes(src)
    return out


def closure_break():
    src = (ROOT / "scripts" / "tierc11_score.py").read_text(encoding="utf-8")
    lazy = src + "\n\ndef _lazy():\n    import tierc11_nest\n    return tierc11_nest\n"
    return plants([
        ("a top-level census import", "STATIC: tierc10_census",
         lambda: closure_scan(src + "\nimport tierc10_census\n")),
        ("a lazy in-function nest import", "STATIC: tierc11_nest", lambda: closure_scan(lazy)),
        ("a subprocess import (an I/O escape)", "HOOK-ESCAPE",
         lambda: closure_scan(src + "\nimport subprocess\n")),
    ])


def closure_real():
    src = (ROOT / "scripts" / "tierc11_score.py").read_text(encoding="utf-8")
    code = ("import sys, json\nsys.dont_write_bytecode = True\n"
            f"sys.path[:0] = [{str(ROOT)!r}, {str(ROOT / 'scripts')!r}]\n"
            "before = set(sys.modules)\nimport tierc11_score\n"
            "print(json.dumps(sorted(set(sys.modules) - before)))\n")
    r = subprocess.run([PY, "-B", "-c", code], env=_env(), capture_output=True, text=True,
                       cwd=str(ROOT), timeout=600)
    mods = json.loads(r.stdout.strip().splitlines()[-1]) if r.returncode == 0 else None
    hit = [m for m in (mods or []) if any(f in m for f in FORBIDDEN_T)]
    stat = closure_scan(src)
    ok = r.returncode == 0 and not hit and not stat
    return ok, (f"fresh interpreter: {len(mods or [])} modules loaded, none range / census / "
                f"stamps / null / nest ({hit or 'none'}); static scan + E.hook_escapes on the "
                f"source: {stat or 'clean'}" + (f"; exit {r.returncode}" if r.returncode else ""))


# ═══════════════════════════════════════════════════════════════ F-DRYRUN
DRY_FORBID_T = (r"\bSUPPORTED\b", r"\bCI\b", r"\bp[ =]\s*[0-9]", r"clears", r"LOAO",
                r"p_one_sided", r"\[\s*[+-]?[0-9.]+,\s*[+-]?[0-9.]+\]")
DRY_LABEL_T = "(book, not a verdict)"


def _tripwire(*a, **k):
    raise RuntimeError("TRIPWIRE: a ruler was called")


def dryrun_findings(root: Path) -> tuple[list[str], list[str], int]:
    """The dry run under tripwires on every ruler: it must complete, print no outcome
    token, label every arm line, and print this file's own book facts."""
    try:
        with mutated(S, "ruled", _tripwire), mutated(S, "stats_block", _tripwire), \
                mutated(S, "loao", _tripwire):
            lines, code = S.dry_run(root)
    except RuntimeError as e:
        return [f"DRYRUN-RULED: {e}"], [], -1
    out = []
    text = "\n".join(lines)
    for rx in DRY_FORBID_T:
        m = re.search(rx, text)
        if m:
            out.append(f"DRYRUN-OUTCOME: {rx!r} found ({text[max(0, m.start() - 40):m.end() + 20]!r})")
    arm_lines = [ln for ln in lines if re.match(r"^    (scored|base|tierE__)", ln)]
    unl = [ln for ln in arm_lines if DRY_LABEL_T not in ln and "HALT" not in ln]
    if unl:
        out.append(f"DRYRUN-LABEL: {len(unl)} arm line(s) without {DRY_LABEL_T!r}")
    heads = [ln for ln in lines if re.match(r"^[1-9] P-", ln)]
    if [h.split()[1].rstrip(":") for h in heads] != list(NINE_T):
        out.append(f"DRYRUN-GRID: registration lines {len(heads)} != the typed nine")
    a = read_arm(root, "P-ADD-SFP", "scored") if (root / "P-ADD-SFP").exists() else None
    if a is not None:
        want = f"n {len(a):>4} · ΣR {float(a['net_r'].sum()):+.6f}"
        line = next((ln for ln in lines if ln.startswith("    scored") and want in ln), None)
        if line is None:
            out.append(f"DRYRUN-FACTS: no P-ADD-SFP scored line carries this file's {want!r}")
    return out, lines, code


def dry_break():
    real = S._dry_facts

    def calls_ruler(df):
        S.stats_block("vs_zero", df, None, CLASSIC5_T, n_boot=9)
        return real(df)

    def prints_ci(df):
        return real(df) + " · CI [+0.1000, +0.2000]"

    def corrupted(rid, fn):
        def thunk():
            with tempfile.TemporaryDirectory() as td:
                root = copy_family(Path(td))
                fn(root, rid)
                f, lines, code = dryrun_findings(root)
                return [ln for ln in lines if "HALT" in ln] + ([f"exit {code}"] if code else [])
        return thunk

    def move_key(root, rid):
        sc = read_arm(root, rid, "scored")
        sc.loc[2, "entry_ms"] = int(sc.loc[2, "entry_ms"]) + MS_4H
        sc.loc[2, "entry_close_ms"] = int(sc.loc[2, "entry_close_ms"]) + MS_4H
        sc["era"] = era_t(sc["entry_close_ms"])
        rewrite_arm(root, rid, "scored", sc)

    def unacted_moved(root, rid):
        sc = read_arm(root, rid, "scored")
        j = int(np.flatnonzero(sc["acted_by"].astype(str).to_numpy() == "")[0])
        rewrite_arm(root, rid, "scored", with_net(sc, sc["net_r"].to_numpy() + np.where(
            np.arange(len(sc)) == j, 0.3, 0.0), fee_table()))

    def gate_moved(root, rid):
        sc = read_arm(root, rid, "scored")
        rewrite_arm(root, rid, "scored", with_net(sc, sc["net_r"].to_numpy() + np.where(
            np.arange(len(sc)) == 1, 0.3, 0.0), fee_table()))

    def cond_flip(root, rid):
        condition_json(root, True, -0.1)

    def under(val):
        def thunk():
            with mutated(S, "_dry_facts", val):
                return dryrun_findings(planted_run()["root"])[0]
        return thunk

    return plants([
        ("the dry run's facts calling a ruler", "DRYRUN-RULED", under(calls_ruler)),
        ("the dry run printing an interval", "DRYRUN-OUTCOME", under(prints_ci)),
        ("corrupted input: a paired key moved (the dry run must HALT the row)",
         "HALT: PAIRED-PREMISE", corrupted("P-ADD-SFP", move_key)),
        ("corrupted input: an unacted P-TP-RNG campaign moved off v6 (identity law)",
         "HALT: IDENTITY-LAW", corrupted("P-TP-RNG", unacted_moved)),
        ("corrupted input: a kept P-WIN-1 gate row changed (post-filter)",
         "HALT: GATE-POSTFILTER", corrupted("P-WIN-1", gate_moved)),
        ("corrupted input: P-WARN-1's condition record flipped to MET under NOT MET",
         "HALT: CONDITION-RECORD", corrupted("P-WARN-1", cond_flip)),
    ])


def dry_real():
    bad, lines, code = dryrun_findings(planted_run()["root"])
    if code != 0:
        bad.append(f"DRYRUN: exit {code} on the planted family")
    if not lines or lines[-1] != "EXIT 0 = 0 (no condition)":
        bad.append(f"DRYRUN: last line {lines[-1] if lines else None!r} is not the typed EXIT 0 line")
    return (not bad), (f"the dry run completes with every ruler tripwired (ruled, stats_block, "
                       f"loao), exit {code} ('EXIT 0 = 0 (no condition)'); 9 registration lines in "
                       f"the typed order, every arm line "
                       f"labelled {DRY_LABEL_T}; no interval, p, LOAO or verdict token; the P-ADD-SFP "
                       f"scored n / ΣR == this file's" + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-EXIT
EXIT_BITS_T = {"halt": 2, "tier_e": 4, "absent": 8, "noclobber": 16}    # SC-10, typed
EXIT_NAMES_T = {"halt": "a registered row HALTed", "tier_e": "a Tier-E row halted",
                "absent": "a registration is ABSENT (no STATUS.json)",
                "noclobber": "a no-clobber refusal"}


def _res(halt=False, tier_e=False, absent=False) -> dict:
    """A minimal scorer result: rows with exactly the conditions asked."""
    rows = [{"verdict_of_record": "SUPPORTED", "status": "BUILT", "tier_e": [{"halted": None}]}]
    if halt:
        rows.append({"verdict_of_record": "HALT", "status": "HALT", "tier_e": []})
    if tier_e:
        rows.append({"verdict_of_record": "NOT SUPPORTED", "status": "BUILT",
                     "tier_e": [{"halted": "BASE-ABSENT"}]})
    if absent:
        rows.append({"verdict_of_record": "ABSENT", "status": "ABSENT", "tier_e": []})
    return {"rows": rows}


def exit_findings(tmp: Path) -> list[str]:
    """Every subset of the four conditions gives the OR of its typed bits and an EXIT line
    naming each; the dry run on a family with a registered HALT, a Tier-E halt and an
    ABSENT registration exits 2|4|8 = 14 and names all three."""
    out = []
    names = ("halt", "tier_e", "absent", "noclobber")
    for mask in range(16):
        on = {k: bool(mask >> j & 1) for j, k in enumerate(names)}
        want = sum(EXIT_BITS_T[k] for k in names if on[k])
        res = _res(on["halt"], on["tier_e"], on["absent"])
        got = S.exit_code(res, noclobber=on["noclobber"])
        line = S.exit_line(S.exit_conditions(res, noclobber=on["noclobber"]))
        want_line = (f"EXIT {want} = " + " + ".join(f"{EXIT_BITS_T[k]} ({EXIT_NAMES_T[k]})"
                                                     for k in names if on[k])
                     if want else "EXIT 0 = 0 (no condition)")
        if got != want or line != want_line:
            out.append(f"EXIT-FLAGS: {on} -> exit {got} / {line!r} != typed {want} / "
                       f"{want_line!r}")
    root = copy_family(tmp)
    d = read_arm(root, "P-TP-RNG", "base")                       # a registered HALT (SC-7)
    rewrite_arm(root, "P-TP-RNG", "base", with_net(d, d["net_r"].to_numpy() + np.where(
        np.arange(len(d)) == 0, 0.5, 0.0), fee_table()))
    js = json.loads((root / "P-AGE-1" / "tierE__shadow_absolute.json").read_text())
    js["n"] = js["n"] + 1                                        # a Tier-E arm unusable
    (root / "P-AGE-1" / "tierE__shadow_absolute.json").write_text(json.dumps(js))
    (root / "P-SCALP-2" / "STATUS.json").unlink()                # ABSENT
    lines, code = S.dry_run(root, root_label=PLANT_LABEL)
    want14 = "EXIT 14 = " + " + ".join(f"{EXIT_BITS_T[k]} ({EXIT_NAMES_T[k]})"
                                       for k in ("halt", "tier_e", "absent"))
    if code != 14 or lines[-1] != want14:
        out.append(f"EXIT-FLAGS: dry run on HALT + Tier-E + ABSENT -> exit {code}, "
                   f"{lines[-1]!r} != typed 14 naming all three")
    out += main_exit_findings(tmp)
    return out


EXIT16_LINE_T = "EXIT 16 = 16 (a no-clobber refusal)"
EXIT0_LINE_T = "EXIT 0 = 0 (no condition)"
MAIN_SITE_T = "return exit_code(res, noclobber=bool(notes))"     # the typed mutation site


def main_exit_findings(tmp: Path) -> list[str]:
    """[reproducibility MINOR-2] S.main ITSELF returns the word it prints — the value
    `sys.exit(main(sys.argv[1:]))` hands the process.  Against an out-dir holding a BENT
    record it must print and return 16, leave the bent record untouched and file the run
    as FAMILY_rerun.json; on the clean record it returns 0.  score_all is stubbed to the
    memoized planted result (F-DET runs the unstubbed script end to end); the stub
    records what main parsed from its argv, and that is judged too."""
    R = planted_run()
    out_dir = tmp / "main_out"
    S.write_outputs(R["files"], out_dir, True)
    rec = out_dir / "FAMILY.json"
    bent = bytearray(R["files"]["FAMILY.json"])
    bent[len(bent) // 2] ^= 0x01
    rec.write_bytes(bytes(bent))
    seen: list = []

    def stub(regbooks_root=None, n_boot=S.N_BOOT, banner=None, root_label=None):
        seen.append((Path(regbooks_root).resolve(), banner, root_label))
        return R["res"]

    argv = [f"--regbooks-root={R['root']}", f"--out-dir={out_dir}", f"--banner={PLANT_BANNER}",
            f"--regbooks-label={PLANT_LABEL}"]
    want_args = (Path(R["root"]).resolve(), PLANT_BANNER, PLANT_LABEL)
    out = []

    def run() -> tuple[int, str]:
        buf = io.StringIO()
        with mutated(S, "score_all", stub), contextlib.redirect_stdout(buf):
            try:
                code = S.main(list(argv))
            except SystemExit as e:              # a HALT inside main is judged, never lost
                code = f"SystemExit {e}"
        lines = buf.getvalue().splitlines()
        return code, (lines[-1] if lines else "")

    code, last = run()
    if code != 16 or last != EXIT16_LINE_T:
        out.append(f"EXIT-MAIN: S.main against an out-dir holding a bent FAMILY.json returned "
                   f"{code!r} and printed {last!r} != typed 16 / {EXIT16_LINE_T!r}")
    rr = out_dir / "FAMILY_rerun.json"
    if rec.read_bytes() != bytes(bent) or not rr.exists() or \
            rr.read_bytes() != R["files"]["FAMILY.json"]:
        out.append("EXIT-MAIN: the no-clobber run did not leave the bent record untouched and "
                   "file itself as FAMILY_rerun.json")
    rec.write_bytes(R["files"]["FAMILY.json"])
    code0, last0 = run()
    if code0 != 0 or last0 != EXIT0_LINE_T:
        out.append(f"EXIT-MAIN: S.main on the clean record returned {code0!r} and printed "
                   f"{last0!r} != typed 0 / {EXIT0_LINE_T!r}")
    if seen != [want_args, want_args]:
        out.append(f"EXIT-MAIN: main passed score_all {[(str(p.name), b is not None, l) for p, b, l in seen]} "
                   f"— not the argv's regbooks root / banner / label")
    return out


SCORE_SCRIPT = ROOT / "scripts" / "tierc11_score.py"
MAIN_LINE_T = "    sys.exit(main(sys.argv[1:]))"              # the typed __main__ line [verify MINOR-1]


def process_exit_findings(tmp: Path, mutant: bool = False) -> list[str]:
    """[TC11-FIX verify MINOR-1] The PROCESS exit code, not main()'s return: scripts/tierc11_score.py
    run in a SUBPROCESS (unstubbed, the planted regbooks) against an out-dir holding a BENT
    FAMILY.json must exit 16, print the typed EXIT 16 line last, leave the bent record untouched
    and file the run as FAMILY_rerun.json.  mutant=True runs a COPY of the script's source whose
    `__main__` calls main(...) WITHOUT sys.exit (compiled under the script's own path, run as
    __main__), which exits 0 — the break."""
    R = planted_run()
    out_dir = tmp / ("proc_mutant" if mutant else "proc_out")
    S.write_outputs(R["files"], out_dir, True)
    rec = out_dir / "FAMILY.json"
    bent = bytearray(R["files"]["FAMILY.json"])
    bent[len(bent) // 2] ^= 0x01
    rec.write_bytes(bytes(bent))
    argv = [f"--regbooks-root={R['root']}", f"--out-dir={out_dir}", f"--banner={PLANT_BANNER}",
            f"--regbooks-label={PLANT_LABEL}"]
    if not mutant:
        cmd = [PY, "-B", str(SCORE_SCRIPT), *argv]
        how = "`python scripts/tierc11_score.py`"
    else:
        src = SCORE_SCRIPT.read_text(encoding="utf-8")
        if src.count(MAIN_LINE_T) != 1:
            raise RuntimeError(f"the typed __main__ line {MAIN_LINE_T.strip()!r} is not in "
                               f"tierc11_score.py once")
        mut = tmp / "tierc11_score_mutant.py"
        mut.write_text(src.replace(MAIN_LINE_T, "    main(sys.argv[1:])"), encoding="utf-8")
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.argv = [{str(SCORE_SCRIPT)!r}] + {argv!r}\n"
                f"src = open({str(mut)!r}, encoding='utf-8').read()\n"
                f"g = {{'__name__': '__main__', '__file__': {str(SCORE_SCRIPT)!r}}}\n"
                f"exec(compile(src, {str(SCORE_SCRIPT)!r}, 'exec'), g)\n")
        cmd = [PY, "-B", "-c", code]
        how = "the mutant __main__ (main(...) without sys.exit)"
    r = subprocess.run(cmd, env=_env(), capture_output=True, text=True, cwd=str(ROOT), timeout=3600)
    lines = r.stdout.splitlines()
    last = lines[-1] if lines else ""
    out = []
    if r.returncode != 16 or last != EXIT16_LINE_T:
        out.append(f"EXIT-PROCESS: {how} against an out-dir holding a bent FAMILY.json exited "
                   f"{r.returncode} and printed {last!r} last != typed process exit 16 / "
                   f"{EXIT16_LINE_T!r}" + (f" (stderr {r.stderr.strip()[-160:]!r})"
                                             if r.returncode not in (0, 16) else ""))
    rr = out_dir / "FAMILY_rerun.json"
    if rec.read_bytes() != bytes(bent) or not rr.exists() or \
            rr.read_bytes() != R["files"]["FAMILY.json"]:
        out.append(f"EXIT-PROCESS: {how} did not leave the bent record untouched and file itself "
                   f"as FAMILY_rerun.json")
    return out


def mutant_main():
    """The reviewer's mutation, made on a COPY of S.main's source: `return exit_code(res)`
    (the no-clobber bit dropped from the RETURN; the printed EXIT line still says 16)."""
    src = inspect.getsource(S.main)
    if src.count(MAIN_SITE_T) != 1:
        raise RuntimeError(f"the typed mutation site {MAIN_SITE_T!r} is not in S.main once")
    ns: dict = {}
    exec(compile(src.replace(MAIN_SITE_T, "return exit_code(res)"), S.__file__, "exec",
                 flags=__future__.annotations.compiler_flag, dont_inherit=True),
         dict(vars(S)), ns)
    f = ns["main"]
    return types.FunctionType(f.__code__, vars(S), "main", f.__defaults__, f.__closure__)


def _proc_mutant() -> list[str]:
    with tempfile.TemporaryDirectory() as td:
        return process_exit_findings(Path(td), mutant=True)


def exit_break():
    def old_law(res, noclobber=False):                  # the masking precedence law
        rows = res["rows"]
        if any(r["verdict_of_record"] == "HALT" for r in rows):
            return 2
        if any(t.get("halted") for r in rows for t in r["tier_e"]):
            return 3
        if any(r["status"] == "ABSENT" for r in rows):
            return 5
        return 4 if noclobber else 0

    real_conds = S.exit_conditions

    def no_halt(res, noclobber=False):                  # exit 0 when a registered row HALTs
        return [(n, b) for n, b in real_conds(res, noclobber) if b != 2]

    def under(name, val):
        def thunk():
            with tempfile.TemporaryDirectory() as td, mutated(S, name, val):
                return exit_findings(Path(td))
        return thunk

    return plants([
        ("the masking precedence law (2 hides 5, 3 hides 5, 4 only when 0)", "EXIT-FLAGS",
         under("exit_code", old_law)),
        ("a registered HALT dropped from the exit word", "EXIT-FLAGS",
         under("exit_conditions", no_halt)),
        ("the flag bits permuted (Tier-E 8, ABSENT 4)", "EXIT-FLAGS",
         under("EXIT_FLAGS", (S.EXIT_FLAGS[0], (S.EXIT_FLAGS[1][0], 8),
                              (S.EXIT_FLAGS[2][0], 4), S.EXIT_FLAGS[3]))),
        ("main mutated to `return exit_code(res)` (prints EXIT 16, returns 0)", "EXIT-MAIN",
         under("main", mutant_main())),
        ("__main__ calls main(...) without sys.exit (a subprocess of the mutated script: the "
         "no-clobber refusal exits 0)", "EXIT-PROCESS", _proc_mutant),
    ])


def exit_real():
    with tempfile.TemporaryDirectory() as td:
        bad = exit_findings(Path(td))
        bad += process_exit_findings(Path(td))
    return (not bad), (f"all 16 subsets of (registered HALT 2, Tier-E halted 4, ABSENT 8, "
                       f"no-clobber 16) exit the OR of their typed bits with an EXIT line naming "
                       f"each; the dry run on a family with all three row conditions exits 14 and "
                       f"names all three; S.main against an out-dir holding a bent FAMILY.json "
                       f"returns 16 and prints {EXIT16_LINE_T!r} (the bent record untouched, the "
                       f"run filed as FAMILY_rerun.json), and on the clean record returns 0 "
                       f"({EXIT0_LINE_T!r}); main passed score_all the argv's root / banner / "
                       f"label; `python scripts/tierc11_score.py` in a SUBPROCESS against an "
                       f"out-dir holding a bent FAMILY.json EXITS 16 (the process exit code) and "
                       f"prints {EXIT16_LINE_T!r} last, the bent record untouched, the run filed "
                       f"as FAMILY_rerun.json" + (f"; findings {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-S0-TEXT
BUILDER_T = "builder's stage status:"                        # SC-20, typed
CLOSED_WORD_T = {"CLOSED_BY_PRECONDITION": "CLOSED BY PRECONDITION",
                 "CONDITION_NOT_MET": "CONDITION NOT MET"}
TC10_PIN_T = 1_790_006_400_000                               # 2026-09-21T16:00:00Z, typed
PRESEEN_T = ("point known before filing; new campaigns since 2026-09-21T16:00Z: scored {} / "
             "base {}")                                      # SC-21, typed
PRESEEN_REGS_T = ("P-AGE-1",)                               # the one pre_seen label [L-G.1]
SHIFT_COUNTS_T = (3, 4)                                     # the moved P-AGE-1 copy: scored / base
D15_NA_T = {"two_sample": "D15 n/a (two-sample)", "vs_zero": "D15 n/a (vs zero)"}   # SC-22


def own_new(df: pd.DataFrame) -> int:
    """SC-21 by THIS file's loop: entry bar CLOSE strictly after the typed TC10 pin."""
    return sum(1 for c in df["entry_close_ms"] if int(c) > TC10_PIN_T)


def _ts(ms: int) -> str:
    return time.strftime("%Y-%m-%dT%H:%M", time.gmtime(int(ms) // 1000)) + "Z"


def _f4(x) -> str:
    return "—" if x is None else f"{x:+.4f}"


def _pc(x) -> str:
    return "n/a" if x is None else f"{100.0 * x:.1f}%"


def own_conc_cell(ruler: str, a: pd.DataFrame, b: pd.DataFrame | None) -> str:
    """SC-22 by THIS file's own selection — the top trade by |net_r| (a scan in (symbol,
    entry_ms) order, the first maximum), the removal law (every book holding its key),
    the asset split, the per-asset grouping — over the books in the scorer's frame order
    (symbol, entry_close_ms) with the same arithmetic primitives (Series.sum, np.mean): the
    F-BOOT law, a hand computation exact to the last bit, so the printed 4 dp compare as
    an identity.  Stamps by time.gmtime; the typed 'D15 n/a (…)' head."""
    ra = [(str(s), int(e), int(c), float(v)) for s, e, c, v in
          zip(a["symbol"], a["entry_ms"], a["entry_close_ms"], a["net_r"])]
    rb = ([] if b is None else
          [(str(s), int(e), float(v)) for s, e, v in zip(b["symbol"], b["entry_ms"], b["net_r"])])
    head = D15_NA_T[ruler]
    if not ra:
        return head + " · the scored book holds no campaign"
    scan = sorted(ra, key=lambda r: (r[0], r[1]))
    top = scan[0]
    for r in scan[1:]:
        if abs(r[3]) > abs(top[3]):
            top = r

    def mean(xs):
        x = np.asarray(list(xs), float)
        return float(np.mean(x)) if len(x) else None

    def total(xs):
        return float(pd.Series(list(xs), dtype=float).sum())

    def point(av, bv):
        ma = mean(av)
        if ma is None or ruler == "vs_zero":
            return ma
        mb = mean(bv)
        return None if mb is None else ma - mb

    key, asset = (top[0], top[1]), top[0]
    tot = total(r[3] for r in ra)
    in_base = any((s, e) == key for s, e, _ in rb)
    pwt = point([r[3] for r in ra if (r[0], r[1]) != key], [v for s, e, v in rb if (s, e) != key])
    pwa = point([r[3] for r in ra if r[0] != asset], [v for s, _, v in rb if s != asset])
    ash = total(r[3] for r in ra if r[0] == asset) / tot
    assets = sorted({r[0] for r in ra} | {s for s, _, _ in rb})
    per = ", ".join(f"{x} {_f4(point([r[3] for r in ra if r[0] == x], [v for s, _, v in rb if s == x]))}"
                    for x in assets)
    return " · ".join([
        head,
        f"top trade {top[0]} {_ts(top[2])} {top[3]:+.4f} R = {_pc(top[3] / tot)} of the scored "
        f"ΣR {tot:+.4f}",
        f"point without it {_f4(pwt)}" + (" (removed from both books)" if in_base else ""),
        f"point without {asset} {_f4(pwa)} ({asset} = {_pc(ash)} of ΣR)",
        ("per-asset Δ (scored mean − base mean): " if ruler == "two_sample" else
         "per-asset mean: ") + per])


def _objs(df: pd.DataFrame) -> list:
    return [SimpleNamespace(symbol=str(s), entry_ms=int(e), net_r=float(v))
            for s, e, v in zip(df["symbol"], df["entry_ms"], df["net_r"])]


def md_view(R: dict) -> dict:
    """The planted run as RENDERED: the §0 cells and each detail block's status line,
    parsed from its S0_VERDICTS.md by THIS file."""
    md = R["files"]["S0_VERDICTS.md"].decode("utf-8")
    status = {}
    for blk in md.split("\n### ")[1:]:
        head, _, body = blk.partition("\n")
        status[head.split(" · ")[1].split(" [")[0]] = next(
            (ln for ln in body.splitlines() if ln.startswith("- status: ")), None)
    return {"rows": R["rows"], "cells": {r[0].split(" · ")[1]: r for r in s0_rows(md)},
            "status": status, "root": R["root"]}


def module_view(root: Path) -> dict:
    """The nine re-scored by the module on `root` (small B) and rendered by its own s0_line
    / _detail — the view a plant bends."""
    rows = {rid: score_one(root, rid) for rid in NINE_T}
    return {"rows": rows,
            "cells": {rid: [str(c).replace("\n", " ") for c in S.s0_line(r)]
                      for rid, r in rows.items()},
            "status": {rid: next((ln for ln in S._detail(r) if ln.startswith("- status: ")), None)
                       for rid, r in rows.items()},
            "root": root}


def preseen_shift_findings(tmp: Path) -> tuple[list[str], tuple]:
    """SC-21 where the counts are not 0: a COPY of the planted family whose P-AGE-1 books
    (the base and the gate's scored arm alike) move five campaigns to the TC10 pin and
    past it — a kept BTC campaign whose entry bar CLOSES AT the pin (seen by TC10: not
    new), a kept ETH one whose bar OPENS at it (new by its close), kept NEAR and SOL ones
    after it, and the first campaign the gate refused (base only): typed scored 3 / base 4.
    Ruled by score_registration under an ident harness (the moved base is no longer
    books/v6; F-BASE-IDENT is not on trial here)."""
    out = []
    d = tmp / "preseen_shift"
    if d.exists():
        shutil.rmtree(d)
    d.mkdir(parents=True)
    root = copy_family(d)
    rid = "P-AGE-1"
    base, sc = read_arm(root, rid, "base"), read_arm(root, rid, "scored")
    kept = set(zip(sc["symbol"], (int(e) for e in sc["entry_ms"])))
    bkeys = sorted(zip(base["symbol"], (int(e) for e in base["entry_ms"])))
    picks = [next(k for k in bkeys if k[0] == s and k in kept)
             for s in ("BTCUSDT", "ETHUSDT", "NEARUSDT", "SOLUSDT")]
    picks.append(next(k for k in bkeys if k not in kept))
    closes = [TC10_PIN_T + j * MS_4H for j in range(len(picks))]   # AT the pin, then after

    def moved(df):
        x = df.copy()
        keys = list(zip(x["symbol"], (int(e) for e in x["entry_ms"])))
        for k, c in zip(picks, closes):
            j = [i for i, kk in enumerate(keys) if kk == k]
            if j:
                x.loc[x.index[j[0]], ["entry_ms", "entry_close_ms", "exit_close_ms"]] = \
                    [c - MS_4H, c, c + MS_4H]
        for col in ("entry_ms", "entry_close_ms", "exit_close_ms"):
            x[col] = x[col].astype(np.int64)
        x["era"] = era_t(x["entry_close_ms"])
        return x

    rewrite_arm(root, rid, "base", moved(base))
    rewrite_arm(root, rid, "scored", moved(sc))
    ns, nb = own_new(read_arm(root, rid, "scored")), own_new(read_arm(root, rid, "base"))
    if (ns, nb) != SHIFT_COUNTS_T:
        out.append(f"S0-PRESEEN: the moved copy counts scored {ns} / base {nb} by this file != "
                   f"typed {SHIFT_COUNTS_T} (a FIXTURE defect)")
    doc, _ = S.load_registry(ROOT)
    reg = next(r for r in doc["registrations"] if r["registration"] == rid)
    row = S.score_registration(S.Loader(root, S._fees()), reg,
                               {"per_registration_ok": {rid: True}, "findings": []}, n_boot=199)
    cell = str(row["verdict_cell"])
    want = "; " + PRESEEN_T.format(ns, nb) + ")"
    if row["verdict_of_record"] == "HALT":
        out.append(f"S0-PRESEEN: the moved {rid} copy HALTed: {row['halts'][:1]}")
    elif want not in cell or cell.find("(pre_seen: ") < 0 or \
            cell.find("(pre_seen: ") > cell.find(want):
        out.append(f"S0-PRESEEN: the moved {rid} copy's cell lacks {want!r} inside its pre_seen "
                   f"label ({cell[cell.find('F-CTRL(b))'):][:110]!r})")
    rec = row.get("pre_seen_new_campaigns") or {}
    if (rec.get("scored"), rec.get("base")) != (ns, nb):
        out.append(f"S0-PRESEEN: the moved {rid} copy records ({rec.get('scored')}, "
                   f"{rec.get('base')}) != this file's ({ns}, {nb})")
    return out, (ns, nb)


def s0_text_findings(view: dict, tmp: Path) -> tuple[list[str], dict]:
    """SC-20 / SC-21 / SC-22 on one view of the nine (rendered or re-scored)."""
    out, tally = [], {"status_lines": 0, "closed_cells": 0, "unpaired": [], "paired": []}
    rows, cells, status, root = view["rows"], view["cells"], view["status"], view["root"]
    for rid in NINE_T:                      # SC-20: the builder's words, labelled
        r = rows[rid]
        reason = r.get("status_reason")
        if reason:
            want = f"- status: {r['status']} — {BUILDER_T} {reason}"
            if status.get(rid) != want:
                out.append(f"S0-BUILDER: {rid} status line {str(status.get(rid))[:90]!r} != typed "
                           f"'- status: {r['status']} — {BUILDER_T} <its STATUS.json reason>'")
            tally["status_lines"] += 1
        if r.get("status") in CLOSED_WORD_T:
            want = f"{CLOSED_WORD_T[r['status']]} ({BUILDER_T} {reason})"
            if not cells[rid][4].startswith(want):
                out.append(f"S0-BUILDER: {rid} closed §0 cell {cells[rid][4][:90]!r} does not "
                           f"start {want[:70]!r}")
            tally["closed_cells"] += 1
    for rid in NINE_T:                      # SC-21: the pre_seen facts, from the books
        cell = cells[rid][4]
        if rid in PRESEEN_REGS_T:
            ns, nb = own_new(read_arm(root, rid, "scored")), own_new(read_arm(root, rid, "base"))
            want = "; " + PRESEEN_T.format(ns, nb) + ")"
            i, j = cell.find("(pre_seen: "), cell.find(want)
            if i < 0 or j < i:
                out.append(f"S0-PRESEEN: {rid} §0 cell lacks {want!r} inside its pre_seen label")
            rec = rows[rid].get("pre_seen_new_campaigns") or {}
            if (rec.get("scored"), rec.get("base")) != (ns, nb):
                out.append(f"S0-PRESEEN: {rid} records ({rec.get('scored')}, {rec.get('base')}) != "
                           f"this file's ({ns}, {nb})")
            tally["preseen"] = (ns, nb)
        elif "point known before filing" in cell:
            out.append(f"S0-PRESEEN: {rid} (no pre_seen label) carries the pre_seen facts")
    sh, tally["shift"] = preseen_shift_findings(tmp)
    out += sh
    for rid in NINE_T:                      # SC-22: D15 where it applies, n/a + concentration
        r = rows[rid]
        if r.get("stats") is None:
            continue
        cell, ruler = cells[rid][8], RULER_T[rid]
        a = _sorted_arm(root, rid, "scored")
        if ruler == "paired":
            d = E.T5.d15(_objs(a), _objs(_sorted_arm(root, rid, "base")))
            want = (f"tail {d['tail_exit_ratio']} · paired n {d['n_paired']} · max Δ share "
                    f"{d['max_single_trade_delta_share']}")
            if not cell.startswith(want) or "D15 n/a" in cell or r.get("concentration"):
                out.append(f"S0-D15: {rid} (paired) cell {cell[:80]!r} != T5.d15's {want!r}")
            tally["paired"].append(rid)
        else:
            b = None if ruler == "vs_zero" else _sorted_arm(root, rid, "base")
            want = own_conc_cell(ruler, a, b) + (f" · named risk: {r['named_risk']}"
                                                 if r.get("named_risk") else "")
            if cell != want:
                k = next((i for i in range(min(len(cell), len(want))) if cell[i] != want[i]),
                         min(len(cell), len(want)))
                out.append(f"S0-D15: {rid} ({ruler}) cell != this file's at char {k}: "
                           f"{cell[max(0, k - 40):k + 60]!r} vs {want[max(0, k - 40):k + 60]!r}")
            tally["unpaired"].append(rid)
    return out, tally


def _old_d15_cell(r: dict) -> str:
    """The pre-G2 D15 cell: T5.d15's paired columns on every row with a base."""
    d = (r.get("stats") or {}).get("d15")
    dc = ("— (vs zero: no base)" if d is None else
          f"tail {d.get('tail_exit_ratio')} · paired n {d.get('n_paired')} · max Δ share "
          f"{d.get('max_single_trade_delta_share')}")
    return dc + (f" · named risk: {r['named_risk']}" if r.get("named_risk") else "")


def s0_text_break():
    real_label, real_point = S.label_of, S.conc_point

    def under(name, val):
        def thunk():
            with tempfile.TemporaryDirectory() as td, mutated(S, name, val):
                return s0_text_findings(module_view(planted_root()), Path(td))[0]
        return thunk

    return plants([
        ("the builder's label dropped from the status line and the closed cells (SC-20)",
         "S0-BUILDER", under("BUILDER_STATUS_LABEL", "")),
        ("the pre_seen facts dropped from the §0 cell (SC-21)", "S0-PRESEEN",
         under("label_of", lambda spec, facts: real_label(spec, None))),
        ("new campaigns counted by the entry bar's OPEN", "S0-PRESEEN: the moved P-AGE-1",
         under("PRESEEN_TIME_COL", "entry_ms")),
        ("a campaign closing AT the TC10 pin counted as new (>=)", "S0-PRESEEN: the moved P-AGE-1",
         under("new_since_pin", lambda df: int((df["entry_close_ms"].to_numpy(np.int64)
                                                >= S.TC10_PIN_MS).sum()))),
        ("the pre-G2 paired D15 cell on the unpaired rows (SC-22)", "S0-D15",
         under("d15_cell", _old_d15_cell)),
        ("the top trade removed from the scored book only (a base holding its key keeps it)",
         "S0-D15: P-AGE-1", under("CONC_TOP_FROM_EVERY_BOOK", False)),
        ("the base ignored in the concentration points (two-sample read as vs zero)",
         "S0-D15: P-RELAY-1", under("conc_point", lambda ruler, a, b: real_point("vs_zero", a, None))),
    ])


def s0_text_real():
    with tempfile.TemporaryDirectory() as td:
        bad, t = s0_text_findings(md_view(planted_run()), Path(td))
    return (not bad), (f"SC-20: {t['status_lines']} detail status lines read '- status: <word> — "
                       f"{BUILDER_T} <the STATUS.json reason>' and {t['closed_cells']} closed §0 "
                       f"cells '<WORD> ({BUILDER_T} <reason>)'; SC-21: P-AGE-1's §0 cell carries "
                       f"'; {PRESEEN_T.format(*t.get('preseen', ('?', '?')))})' inside its "
                       f"pre_seen label (this file's counts, entry close > the typed pin), no "
                       f"other row carries it, and the moved copy reads scored {t['shift'][0]} / "
                       f"base {t['shift'][1]} (closing AT the pin not new, opening at it new, a "
                       f"refused campaign base-only); SC-22: {len(t['unpaired'])} unpaired D15 "
                       f"cells ({', '.join(t['unpaired'])}) == this file's own 'D15 n/a' + "
                       f"concentration exactly, {len(t['paired'])} paired cells "
                       f"({', '.join(t['paired'])}) == T5.d15's" + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-REPORT
REPORT_PATH = S.SCORES / "STAGE_SCORE.md"
REPORT_POINTER_T = "**The record is `research_outputs/tierc11/scores/S0_VERDICTS.md`**"
REPORT_STALE_T = "computes no registered result"
AMEND_PATH_T = ROOT / "research_outputs" / "tierc11" / "LEANS_AMENDMENTS.md"
HISTORICAL_T = "HISTORICAL"
# the report's own pin form: `LEANS_AMENDMENTS.md`, at most three words, then the BACKTICKED sha
# (a transcript line the report quotes prints its shas bare, never backticked)
_AMEND_PIN_RX = re.compile(r"LEANS_AMENDMENTS\.md(?:\s+[^`\s]+){0,3}\s+`([0-9a-f]{8,64})")
PLANTED_TAG_T = "PLANTED · "
PLANTED_SECTION_T = "## The planted run"
# (name, the report's sub-heading, the planted S0_VERDICTS.md segment, verdict column, rows)
PLANTED_TABLES_T = (
    ("§0", "### §0 table (planted)", ("## §0 table", "## Family"),
     "verdict under its own text (with labels)", 9),
    ("Family", "### Family (planted)", ("## Family", "## Detail blocks"), "verdict_of_record", 9),
    ("Tier-E", "### Tier-E rows (planted)", ("## Tier-E rows", "## F-BASE-IDENT"),
     "would_read_ci_only", len(TIER_E_DECLARED_T)),
)


def md_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    """Every markdown table in `text` as (header cells, data rows) — THIS file's parser."""
    out, cur = [], None
    for ln in text.splitlines():
        if ln.startswith("|"):
            cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]]
            if cur is None:
                cur = (cells, [])
            elif not set(ln.replace("|", "").strip()) - {"-"}:
                continue                        # the |---| separator
            else:
                cur[1].append(cells)
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur is not None:
        out.append(cur)
    return out


def _seg(text: str, start: str, end: str | None) -> str:
    if start not in text:
        return ""
    s = text.split(start, 1)[1]
    return s.split(end, 1)[0] if end and end in s else s


def stale_amend_pins(text: str, amend_sha: str) -> tuple[list[str], int]:
    """[TC11-FIX verify MINOR-11] Every LEANS_AMENDMENTS.md pin the report prints in its own pin
    form (`LEANS_AMENDMENTS.md`, at most three words, then a BACKTICKED hex sha of 8..64) must be
    a prefix of the file's own sha, or sit under a heading (any level of the active chain) that
    carries 'HISTORICAL'.  Returns (findings, the number of old shas under HISTORICAL headings)."""
    out, hist, heads = [], 0, {}
    for ln in text.splitlines():
        m = re.match(r"^(#{1,6}) (.*)", ln)
        if m:
            lvl = len(m[1])
            heads = {k: v for k, v in heads.items() if k < lvl}
            heads[lvl] = m[2]
            continue
        for h in _AMEND_PIN_RX.findall(ln):
            if amend_sha.startswith(h):
                continue
            if any(HISTORICAL_T in v for v in heads.values()):
                hist += 1
                continue
            under = heads[max(heads)] if heads else "(no heading)"
            out.append(f"REPORT-STALE-PIN: a LEANS_AMENDMENTS.md sha {h[:12]}… printed outside "
                       f"a {HISTORICAL_T} section (under {under[:70]!r}); the file's sha is "
                       f"{amend_sha[:12]}…")
    return out, hist


def report_findings(text: str, planted_md: str) -> tuple[list[str], dict]:
    """STAGE_SCORE.md is the build report, NOT the record: the pointer, no stale claim,
    and every planted table tagged row by row and equal (tag removed) to the planted run's
    own S0_VERDICTS.md table [statistics MINOR-4]; no old amendments sha outside a HISTORICAL
    section [TC11-FIX verify MINOR-11]."""
    out, tally = [], {}
    amend_sha = hashlib.sha256(AMEND_PATH_T.read_bytes()).hexdigest()
    pins, tally["historical_pins"] = stale_amend_pins(text, amend_sha)
    out += pins
    if not any(REPORT_POINTER_T in ln for ln in text.splitlines()[:12]):
        out.append(f"REPORT-POINTER: STAGE_SCORE.md's first 12 lines lack {REPORT_POINTER_T!r}")
    if REPORT_STALE_T in text:
        out.append("REPORT-STALE: STAGE_SCORE.md still carries the stale no-registered-result "
                   "claim (the scoring of record exists)")
    if PLANTED_SECTION_T not in text:
        return out + [f"REPORT-PLANTED: no {PLANTED_SECTION_T!r} section"], tally
    sec = text.split(PLANTED_SECTION_T, 1)[1].split("\n## ", 1)[0]
    words = list(re.finditer(r"\b(NOT )?SUPPORTED\b", sec))
    for m in words:
        if not sec[:m.start()].endswith(PLANTED_TAG_T):
            out.append(f"REPORT-PLANTED: {m.group(0)!r} not preceded by {PLANTED_TAG_T!r} "
                       f"({sec[max(0, m.start() - 60):m.end()]!r})")
    tally["verdict_words"] = len(words)
    heads = [t[1] for t in PLANTED_TABLES_T]
    for i, (name, sub, (p0, p1), vcol, n_t) in enumerate(PLANTED_TABLES_T):
        rt = md_tables(_seg(sec, sub, heads[i + 1] if i + 1 < len(heads) else None))
        pt = md_tables(_seg(planted_md, p0, p1))
        if not rt or not pt:
            out.append(f"REPORT-PLANTED: the {name} table is absent (report {len(rt)}, planted "
                       f"run {len(pt)})")
            continue
        (rh, rrows), (ph, prows) = rt[0], pt[0]
        if rh != ph or vcol not in rh:
            out.append(f"REPORT-STALE-TABLE: the {name} header != the planted run's")
            continue
        c = rh.index(vcol)
        untag = [r for r in rrows if not r[c].startswith(PLANTED_TAG_T)]
        if untag:
            out.append(f"REPORT-PLANTED: {len(untag)} {name} row(s) whose {vcol!r} cell lacks "
                       f"{PLANTED_TAG_T!r} (first: {untag[0][c][:60]!r})")
        stripped = [r[:c] + [r[c][len(PLANTED_TAG_T):] if r[c].startswith(PLANTED_TAG_T)
                             else r[c]] + r[c + 1:] for r in rrows]
        if stripped != prows:
            k = next((j for j in range(min(len(stripped), len(prows))) if stripped[j] != prows[j]),
                     min(len(stripped), len(prows)))
            out.append(f"REPORT-STALE-TABLE: the {name} table (tag removed) != the planted run's "
                       f"own S0_VERDICTS.md table from row {k} ({len(stripped)} vs {len(prows)} rows)")
        if len(rrows) != n_t:
            out.append(f"REPORT-PLANTED: the {name} table holds {len(rrows)} rows != typed {n_t}")
        tally[name] = len(rrows)
    return out, tally


def planted_report_section() -> str:
    """The report's planted section, rendered from the planted run's own S0_VERDICTS.md
    with every verdict cell tagged (--print-planted-section prints it; F-REPORT checks
    the filed report against the planted run independently of this function)."""
    md = planted_run()["files"]["S0_VERDICTS.md"].decode("utf-8")

    def tagged(seg: str, vcol: str) -> list[str]:
        lines, hdr = [], None
        for ln in seg.strip("\n").splitlines():
            if ln.startswith("|") and hdr is None:
                hdr = [c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]]
            elif ln.startswith("|") and set(ln.replace("|", "").strip()) - {"-"}:
                cells = [c.strip() for c in re.split(r"(?<!\\)\|", ln)[1:-1]]
                c = hdr.index(vcol)
                cells[c] = PLANTED_TAG_T + cells[c]
                ln = "| " + " | ".join(cells) + " |"
            elif not ln.startswith("|"):
                ln = ln.replace("SUPPORTED: ", PLANTED_TAG_T + "SUPPORTED: ")
            lines.append(ln)
        return lines

    L = ["## The planted run (PLANTED — synthetic regbooks; NOT A RESULT of any registration)", "",
         "Every scored and Tier-E arm below is a SYNTHETIC transform of books/v6 (a typed delta or "
         "index filter) or a seeded synthetic lane, written by the fixture file. Every verdict "
         "cell below is prefixed \"PLANTED ·\": the words are the scorer's law exercised on "
         "synthetic data and say nothing about any registration (the record is `S0_VERDICTS.md`). "
         "The pick-stability flags and fallback labels are real, because they are read from the "
         "filed SCALE_PICKS.json record. These tables are the planted run's own S0_VERDICTS.md "
         "tables (F-REPORT checks it), regenerated with `scripts/tierc11_score_fixtures.py "
         "--print-planted-section`.", ""]
    for name, sub, (p0, p1), vcol, _n in PLANTED_TABLES_T:
        seg = _seg(md, p0, p1)
        head = sub
        if not seg.startswith("\n"):            # '## Tier-E rows — …': the heading's tail
            tail, seg = seg.split("\n", 1)
            head += tail
        L += [head, ""] + tagged(seg, vcol) + [""]
    return "\n".join(L).rstrip("\n") + "\n"


OLD_AMEND_T = "b1c6275b5008fa684af9bebdaeefa2c41a99f40e60f033db71d085c9ba3e10fb"   # pre-TC11-FIX


def tally_section(transcript: Path) -> str:
    """STAGE_SCORE.md's fixture-tally section, rendered from the FILED transcript: each
    fixture's [PASS]/[FAIL] line, then its break line (--print-tally-section; stdout only)."""
    raw = transcript.read_bytes()
    lines = raw.decode("utf-8").splitlines()
    tally = next((ln.strip() for ln in reversed(lines) if re.fullmatch(r"\d+ GREEN, \d+ RED",
                                                                        ln.strip())), "? GREEN, ? RED")
    red = tally.split(", ")[1] != "0 RED"
    rows, brk = [], None
    for ln in lines:
        x = ln.lstrip()
        if x.startswith("[BREAK] deliberate violation -> "):
            brk = "  - [BREAK] " + x[len("[BREAK] deliberate violation -> "):]
        elif x.startswith("[PASS] ") or x.startswith("[FAIL] "):
            rows += ["- " + x] + ([brk] if brk else [])
            brk = None
    rel = transcript.resolve().relative_to(ROOT.resolve()).as_posix() \
        if ROOT.resolve() in transcript.resolve().parents else transcript.name
    return "\n".join([f"## Fixture tally — {tally}", "",
                      f"Transcript `{rel}` (sha `{sha_bytes(raw)}`), exit {1 if red else 0}.", "",
                      *rows]) + "\n"


def report_break():
    text = REPORT_PATH.read_text(encoding="utf-8")
    pmd = planted_run()["files"]["S0_VERDICTS.md"].decode("utf-8")

    def strip_first(sub):
        i = text.index(sub)
        j = text.index("| " + PLANTED_TAG_T, i)
        return text[:j + 2] + text[j + 2 + len(PLANTED_TAG_T):]

    def reverted():
        i = text.index("### §0 table (planted)")
        j = text.index(D15_NA_T["two_sample"], i)
        return text[:j] + "tail 1.0 · paired n 187 · max Δ share None" + \
            text[j + len(D15_NA_T["two_sample"]):]

    title_end = text.index("\n", text.index("# TIER-C11"))
    return plants([
        ("a planted §0 row's tag stripped", "REPORT-PLANTED",
         lambda: report_findings(strip_first("### §0 table (planted)"), pmd)[0]),
        ("a planted Family verdict untagged", "REPORT-PLANTED",
         lambda: report_findings(strip_first("### Family (planted)"), pmd)[0]),
        ("the pointer to S0_VERDICTS.md removed", "REPORT-POINTER",
         lambda: report_findings(text.replace(REPORT_POINTER_T, "The record is elsewhere."),
                                 pmd)[0]),
        ("the stale 'no registered result' claim restored", "REPORT-STALE:",
         lambda: report_findings(text[:title_end] + "\n\n**This stage " + REPORT_STALE_T + ".**"
                                 + text[title_end:], pmd)[0]),
        ("a planted §0 D15 cell reverted to the pre-G2 render", "REPORT-STALE-TABLE",
         lambda: report_findings(reverted(), pmd)[0]),
        ("an old LEANS_AMENDMENTS.md sha (the pre-TC11-FIX b1c6275b…) printed under the Files "
         "heading", "REPORT-STALE-PIN",
         lambda: report_findings(text.replace("\n## Files\n", "\n## Files\n\n- LEANS_AMENDMENTS.md "
                                              f"`{OLD_AMEND_T}`\n", 1), pmd)[0]),
        ("the HISTORICAL label struck from every heading (the pre-scoring section prints an old "
         "LEANS_AMENDMENTS.md sha)", "REPORT-STALE-PIN",
         lambda: report_findings("\n".join(
             ln.replace(HISTORICAL_T, "") if ln.startswith("#") else ln
             for ln in text.splitlines()) + "\n", pmd)[0]),
    ])


def report_real():
    text = REPORT_PATH.read_text(encoding="utf-8")
    bad, t = report_findings(text, planted_run()["files"]["S0_VERDICTS.md"].decode("utf-8"))
    return (not bad), (f"STAGE_SCORE.md carries the typed pointer to S0_VERDICTS.md as the record "
                       f"in its first 12 lines and no stale 'no registered result' claim; its "
                       f"planted section's §0 ({t.get('§0')} rows), Family ({t.get('Family')}) and "
                       f"Tier-E ({t.get('Tier-E')}) tables tag every verdict cell "
                       f"{PLANTED_TAG_T.strip()!r} and equal, tag removed, the planted run's own "
                       f"S0_VERDICTS.md tables; all {t.get('verdict_words')} (NOT) SUPPORTED words "
                       f"in the section are tagged; every LEANS_AMENDMENTS.md sha it prints is the "
                       f"file's own or sits under a {HISTORICAL_T} heading "
                       f"({t.get('historical_pins')} old sha(s), all labelled)"
                       + (f"; {bad[:3]}" if bad else ""))


# ═══════════════════════════════════════════════════════════════ F-DET
def det_dir() -> Path:
    return RUN_ROOT / "_det_score"


def det_build(d: Path, seed: int, hashorder: bool = False) -> tuple[int, dict]:
    if d.exists():
        shutil.rmtree(d)
    env = dict(_env(), PYTHONHASHSEED=str(seed))
    root = planted_run()["root"]
    if not hashorder:
        cmd = [PY, "-B", str(ROOT / "scripts" / "tierc11_score.py"), f"--regbooks-root={root}",
               f"--out-dir={d}", f"--banner={PLANT_BANNER}", f"--regbooks-label={PLANT_LABEL}"]
    else:                                   # SABOTAGE twin: a set-order line appended
        code = (f"import sys\nsys.dont_write_bytecode = True\n"
                f"sys.path[:0] = [{str(ROOT)!r}, {str(ROOT / 'scripts')!r}]\n"
                f"from pathlib import Path\nimport tierc11_score as S\n"
                f"d = Path({str(d)!r})\n"
                f"res = S.score_all(Path({str(root)!r}), banner={PLANT_BANNER!r}, n_boot=99, "
                f"root_label={PLANT_LABEL!r})\n"
                f"f = S.render(res)\n"
                f"f['S0_VERDICTS.md'] += ('set order: ' + ','.join(set(S.E.PANEL17))).encode()\n"
                f"S.write_outputs(f, d, True)\n")
        cmd = [PY, "-B", "-c", code]
    r = subprocess.run(cmd, env=env, capture_output=True, text=True, cwd=str(ROOT), timeout=3600)
    files = {p.name: p.read_bytes() for p in sorted(d.iterdir())} if d.exists() else {}
    return r.returncode, files


def det_findings(a: tuple, b: tuple, canon: dict) -> list[str]:
    out = []
    for lab, (rc, _) in (("seed 1", a), (f"seed {SEED}", b)):
        if rc != 0:
            out.append(f"{lab} exit {rc}")
    for lab, x in (("seed 1", a[1]), (f"seed {SEED}", b[1]), ("in-process", canon)):
        if sorted(x) != sorted(OUTPUT_FILES_T):
            out.append(f"{lab}: file set {sorted(x)} != typed {sorted(OUTPUT_FILES_T)}")
    for lab, x, y in ((f"seed 1 vs seed {SEED}", a[1], b[1]), ("seed 1 vs in-process", a[1], canon)):
        for name in sorted(set(x) & set(y)):
            if x[name] != y[name]:
                k = next((i for i in range(min(len(x[name]), len(y[name])))
                          if x[name][i] != y[name][i]), min(len(x[name]), len(y[name])))
                out.append(f"{lab}: {name} bytes differ at byte {k}")
    return out


def det_break():
    canon = planted_run()["files"]
    bent = dict(canon)
    md = bytearray(bent["S0_VERDICTS.md"])
    md[len(md) // 2] ^= 0x01
    bent["S0_VERDICTS.md"] = bytes(md)
    salted = dict(canon)
    salted["FAMILY.json"] = canon["FAMILY.json"].replace(b'"family_m"',
                                                         f'"pid_{os.getpid()}"'.encode())

    def hashorder():
        o = {s: det_build(det_dir() / f"hashorder_{s}", s, hashorder=True) for s in DET_SEEDS}
        a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
        return [x for x in det_findings(a, b, a[1]) if x.startswith(f"seed 1 vs seed {SEED}")]

    return plants([
        ("one byte bent in a copy of S0_VERDICTS.md", "S0_VERDICTS.md bytes differ",
         lambda: det_findings((0, canon), (0, bent), canon)),
        ("a process-dependent salt in FAMILY.json", "FAMILY.json bytes differ",
         lambda: det_findings((0, canon), (0, salted), canon)),
        ("a hash-order-dependent line (set iteration) under the two seeds",
         f"seed 1 vs seed {SEED}: S0_VERDICTS.md bytes differ", hashorder),
    ])


def det_real():
    canon = planted_run()["files"]
    o = {s: det_build(det_dir() / f"seed_{s}", s) for s in DET_SEEDS}
    a, b = o[DET_SEEDS[0]], o[DET_SEEDS[1]]
    bad = det_findings(a, b, canon)
    shas = ", ".join(f"{k} {sha_bytes(v)[:12]}…" for k, v in sorted(a[1].items()))
    return (not bad), (f"exit {a[0]}/{b[0]}; file set == typed {len(OUTPUT_FILES_T)} files; every "
                       f"file byte-identical seed 1 == seed {SEED} == this process's render "
                       f"({shas})" + (f"; findings {bad[:4]}" if bad else ""))


FIXTURES = (
    ("F-SCORE-REG", "REGISTRATIONS.json verified before any score: slices re-cut, payload "
     "shas, the chain, the head [L-1.4]",
     "the real registry does not verify by the scorer AND by this file's own re-derivation "
     "(contract bb38e016…, 9 slices, 9 payloads, 9 links, head 6772568b… == REGISTRY_PIN.json), "
     "or a tampered text / payload / chain line / line sha / head / contract byte / order / "
     "family / file passes", reg_break, reg_real),
    ("F-RULER", "the ruler is the spec's; paired premise and identity law HALT; gates are "
     "post-filters; identical-key two-sample flagged; vs zero ignores base; Tier-E bases "
     "restricted to their era [L-1.4, L-1.5, SC-3, SC-15, SC-16]",
     "a ruler / era differs from the typed L-1.4 table; on any of the 4 paired registrations "
     "a key moved, a row dropped, an unacted row off the base or acted_by dropped is scored; "
     "a two-sample on identical keys is not flagged on any of the 3 (or a planted one is); "
     "the vs-zero row moves when its base is removed; a BUILT paired row is not n == n_base "
     "== 200 with point == this file's delta mean and its unacted count; a gate with a new "
     "campaign or a changed kept row is scored; a holdout-scoped Tier-E arm is not ruled vs "
     "the base's holdout rows", ruler_break, ruler_real),
    ("F-BOOT", "the asset-cluster bootstrap, the CI, the p law and the deciding bound == a "
     "hand computation with the same rng draws [L-1.4, SC-1, SC-2]",
     "the scorer's point / CI / p / deciding bound differ by ANY amount from this file's hand "
     "computation (small B and B 4000, every ruler), or its LOAO per-panel intervals differ "
     "from TP.loao_n at 6 dp", boot_break, boot_real),
    ("F-VERDICT", "SUPPORTED iff lo > 0 AND p <= 1/90; labels; closed rows print no number "
     "[L-1.4, L-1.5, L-S.1, L-W.4]",
     "a typed (lo, hi, p) case reads other than typed; the planted rows do not read their "
     "typed verdicts; a label is missing / spurious; a closed row prints a number, spends a "
     "test or lacks its reason and 'no slot spent'; FAMILY is not m 9 / bar 1/90 / 7 spent; "
     "an add row's AM-3 sums differ from this file's; a SCALE-IN-SAMPLE row's holdout slice / "
     "frozen twin / in-sample count differ from this file's, or its pick stability does not "
     "flag exactly the typed changes at its typed lens (§0 cell and every consuming Tier-E "
     "row), or the fallback label is missing / spurious; the sensitivity-seed verdict is not "
     "ruled on its own draws",
     verdict_break, verdict_real),
    ("F-STATUS", "a status word stands only where the spec names it and its gating record "
     "agrees; the tuning-era R2 word beside P-SCALP-2 [SC-17, L-W.4, L-S.1, §10]",
     "a closing word on a registration without its precondition / condition, a P-WARN-1 word "
     "that disagrees with condition.json (or with L-W.4's MET iff hi < 0, or without the "
     "record), or a P-SCALP-2 word that disagrees with the R2 1h lens word of record is not "
     "HALTed; P-SCALP-2's cell lacks the tuning-era R2 1h word, collared",
     status_break, status_real),
    ("F-COLLAR", "every Tier-E row collared, no verdict word, its CI reading its own [L-1.4]",
     "a Tier-E row lacks the typed collar, carries a verdict word or verdict field, a "
     "would_read_ci_only that is not its interval's reading, the rows are not the declared "
     "set, or a S0_VERDICTS.md Tier-E line lacks the collar", collar_break, collar_real),
    ("F-BASE-IDENT", "the seven base arms are ONE book and it is books/v6 [SC-7, SC-13]",
     "the base arms carry more than one book_sha256, differ from books/v6_campaigns.parquet on "
     "the 13 typed columns at 6 dp, the scorer's record disagrees, or a planted arm's canonical "
     "CSV sha differs between the scorer and pandas", ident_break, ident_real),
    ("F-GRID", "every scorer grid WHOLE against typed declared cells [TP.grid_whole]",
     "the §0 table, FAMILY, the Tier-E table or a LOAO grid misses, duplicates or adds a cell "
     "against its typed declaration", grid_break, grid_real),
    ("F-KEY", "the regbook interface enforced; score rows keyed and non-null",
     "a planted arm fails the interface or a corrupted one passes; the planted straddling "
     "entry bar does not read 'holdout' or is not counted; a score-row key repeats or a "
     "required field is null", key_break, key_real),
    ("F-CLOSURE", "the scorer is range-free and has no hook escape [L-F.2, AM-2]",
     "a fresh interpreter importing tierc11_score loads a range / census / stamps / null / nest "
     "module, or its source holds such an import or an I/O escape", closure_break,
     closure_real),
    ("F-DRYRUN", "the dry run proves the interface and prints books only — never a ruler, "
     "an interval, a p or a verdict word [TC10's dry-run law]",
     "the dry run calls a ruler (tripwired), prints an interval / p / LOAO / verdict token, an "
     "arm line lacks '(book, not a verdict)', the nine registration lines are not the typed "
     "order, its book facts differ from this file's, it does not end 'EXIT 0 = 0 (no "
     "condition)' on the planted family, or a moved paired key / moved unacted campaign / "
     "changed gate row / flipped condition record is not HALTed",
     dry_break, dry_real),
    ("F-EXIT", "the exit code is a bit-flag word; no condition masks another [SC-10]",
     "a subset of (registered HALT, Tier-E halted, ABSENT, no-clobber) exits other than the OR "
     "of the typed bits 2 / 4 / 8 / 16 or its EXIT line fails to name each; the dry run on a "
     "family with all three row conditions does not exit 14; S.main against an out-dir holding "
     "a bent record does not return 16 with the typed EXIT line (bent record untouched, the run "
     "filed as _rerun) or does not return 0 on the clean record; the script run as a SUBPROCESS "
     "against an out-dir holding a bent record does not exit 16 (the process exit code) with the "
     "typed EXIT line last, the bent record untouched and the run filed as _rerun",
     exit_break, exit_real),
    ("F-S0-TEXT", "the §0 text names whose words and which numbers: the builder's stage status "
     "labelled, the pre_seen facts in the cell, D15 n/a on unpaired rulers with the "
     "concentration beside [SC-20, SC-21, SC-22; final review statistics MINOR-1..3, fidelity "
     "MINOR-4]",
     "a status line or closed cell prints a STATUS.json reason without 'builder's stage "
     "status:'; P-AGE-1's pre_seen label lacks 'point known before filing; new campaigns since "
     "2026-09-21T16:00Z: scored <n> / base <n>' with this file's counts (the planted family and "
     "a moved copy typed 3 / 4), or another row carries it; an unpaired D15 cell is not 'D15 "
     "n/a (…)' + this file's own concentration exactly, or a paired cell is not T5.d15's",
     s0_text_break, s0_text_real),
    ("F-REPORT", "the build report is not the record: a pointer to S0_VERDICTS.md, no stale "
     "claim, every planted verdict cell tagged 'PLANTED ·' [statistics MINOR-4], every old "
     "amendments sha under a HISTORICAL heading [TC11-FIX verify MINOR-11]",
     "STAGE_SCORE.md lacks the typed pointer to S0_VERDICTS.md in its first 12 lines, still "
     "carries the stale no-registered-result claim, holds a planted table row whose verdict "
     "cell is untagged "
     "or an untagged (NOT) SUPPORTED in its planted section, a planted table that is not "
     "(tag removed) the planted run's own S0_VERDICTS.md table, or a LEANS_AMENDMENTS.md sha "
     "other than the file's own outside a HISTORICAL section", report_break, report_real),
    ("F-DET", "two subprocess scorer runs under different hash seeds, one set of bytes",
     "the PYTHONHASHSEED 1 and 20260924 runs on the planted regbooks differ from each other or "
     "from this process's render in the file set or any byte, or either exits nonzero",
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


def summary_lines() -> list[str]:
    """The planted run, printed (deterministic): one line per registration."""
    R = planted_run()
    out = [f"planted run ({PLANT_BANNER}):"]
    for r in R["res"]["rows"]:
        m = (r.get("stats") or {}).get("main")
        out.append(f"  {r['seq']} {r['registration']:<10} {r['status']:<23} "
                   + (f"n {m['n']:>3} point {m['point']:+.4f} [{m['lo']:+.4f}, {m['hi']:+.4f}] "
                      f"p {m['p_one_sided']:.6f} " if m else "")
                   + f"-> {r['verdict_of_record']}")
    out.append(f"  F-BASE-IDENT {'OK' if R['res']['base_ident']['ok'] else 'FAILED'}; "
               f"Tier-E rows {sum(len(r['tier_e']) for r in R['res']['rows'])}; findings "
               f"{len(R['res']['findings'])}")
    return out


def main() -> int:
    args = sys.argv[1:]
    global RUN_ROOT
    root = RUN_ROOT = Path(next((a.split("=", 1)[1] for a in args if a.startswith("--root=")),
                                OUT)).resolve()
    if "--print-planted-section" in args:   # STAGE_SCORE.md's planted section (stdout only)
        sys.stdout.write(planted_report_section())
        return 0
    if "--print-tally-section" in args:     # STAGE_SCORE.md's tally section (stdout only)
        sys.stdout.write(tally_section(root / TRANSCRIPT))
        return 0
    pick = [a.lower() for a in args if not a.startswith("--")]
    t0 = time.time()
    say(AS_OF_LINE)
    say("=" * 78)
    say("TIER-C11 TC11-SCORE FIXTURES — scripts/tierc11_score.py (the scorer of the nine) — "
        "break leg first, RED or void")
    say("=" * 78)
    say(f"seed {SEED} (sensitivity {SEED_SENS}) · n_boot {N_BOOT} · substrate {TC11_SNAP.name} · "
        f"registry head {HEAD_T[:16]}…")
    for ln in S.READINGS:
        say(ln)
    for ln in summary_lines():
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
