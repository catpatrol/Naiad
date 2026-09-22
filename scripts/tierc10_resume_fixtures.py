#!/usr/bin/env python
"""TIER-C10 · F-C10-RESUME — THE FIXTURE THAT MAKES THE LAW OF RESUMPTION CHECKABLE.

The RESUME contract names this fixture:

    F-C10-RESUME (every COMPLETE stage re-hashes identical to its PROGRESS.json
    record; a tampered partial must FAIL)

and LAW 6 requires `research_outputs/tierc10/PROGRESS.json` after every stage.
Until now the ledger existed and the fixture did not, so the ledger's own claim
of COMPLETE-VERIFIED was unfalsifiable. This file is the falsifier.

WHAT IS HASHED, AND WHAT IS NOT
  F-C10-RESUME hashes FILED ARTIFACT CONTENT SHAS — the `artifact_shas` block of
  each stage record.  It NEVER demands byte-identity of a fixture TRANSCRIPT.
  A transcript-level re-hash of Stage D is impossible by construction and the
  drift is MEASURED, not asserted: see [LEAN-HEPHAESTUS] R1 below and the
  exemption registry `EXEMPTIONS`, which F-C10-RESUME-4 forces to stay named.

THE LEGS
  F-C10-RESUME-0  THE EXTERNAL ANCHOR — THE ONE LEG THAT DOES NOT READ ITS
                  ANSWER OUT OF PROGRESS.json.  Every other ledger-side guard
                  judges the ledger by the ledger, so ONE working-tree edit
                  defeats them all at once.  This leg judges the working tree
                  against the COMMITTED blob (which a working-tree edit cannot
                  reach) and the committed blob against a sha typed HERE as a
                  module literal (which an amend cannot reach).  Planted: a
                  re-recorded sha, a promoted stage with its blockers deleted,
                  a de-recorded artifact, a bent anchor literal, an unreachable
                  anchor, an uncommitted ledger, a settled stage DEMOTED in the
                  working tree, a settled stage DELETED from it, and
                  DEMOTE-THEN-TAMPER — the laundering case where the demotion
                  hides a re-recorded sha [LEAN R10].
  F-C10-RESUME-1  every artifact a COMPLETE-VERIFIED stage records re-hashes to
                  the recorded sha and the recorded byte count; and no file sits
                  inside a completed stage's directory that the ledger does not
                  record.  Planted: a flipped byte, a deleted artifact, an
                  unrecorded extra file, a laundered quarantine redirect.
  F-C10-RESUME-2  the two LAW-2 kill-partials in the quarantine re-hash to shas
                  typed HERE as independent literals, and agree three ways
                  (literal == disk == PROGRESS.json).  Planted: an appended
                  byte, a swap of the two partials, a deleted partial.
  F-C10-RESUME-3  THE CORRIDOR IS ONE.  PROGRESS.json's as_of_of_record, the
                  Stage D manifest's as_of_last_closed_4h and AS_OF_PIN.json's
                  are one value, 2026-09-21T16:00:00Z, the close_ms one value,
                  1790006400000, and every stage record carries it.  Planted:
                  a re-stamped stage, a moved manifest, a shifted close_ms, a
                  stage with no as_of at all.
  F-C10-RESUME-4  THE VENUE EXEMPTION IS NAMED, NOT SILENT.  Every waiver of
                  byte-reproducibility is a record with a scope, a reason and
                  EVIDENCE that is corroborated on disk; the exempted legs are
                  exactly the legs the exempted suite itself declares as
                  venue-reaching; THE EXEMPTED SUITE IS THE ONE THE EXEMPTED
                  STAGE'S OWN LEDGER BLOCK NAMES [LEAN R11]; and no stage is
                  COMPLETE on an exemption's strength.  Planted: an empty reason,
                  a sourceless evidence block, a bent number, an unexempted
                  drifting suite, a leg that does not exist, a stage promoted
                  while its exemption stands, and a BORROWED SUITE — a verbatim
                  copy of the real waiver re-pointed at another stage.
  F-C10-RESUME-5  PROGRESS.json IS WELL-FORMED AND HONEST.  Every stage carries
                  {stage, status, as_of, artifact_shas, fixtures, blockers};
                  status is one of the three legal values; COMPLETE-VERIFIED
                  implies zero blockers AND zero red legs AND exit 0.  Planted:
                  a blocker under a COMPLETE claim, an illegal status, a missing
                  key, a miscounted artifact set, a red leg under a COMPLETE
                  claim, a duplicated stage, a touched live cache.
  F-C10-RESUME-6  STEP0_RECORD.json re-hashes.  The four STEP 0 source shas are
                  re-measured from disk NOW, the twin's STEP 0 blob is re-read
                  from git, the twelve pins are re-read from the live port AND
                  re-parsed from the Pine, and the record rebuilds byte-identical.
                  Planted: a bent Pine sha, the phantom 0.67 pin, a source that
                  does not exist, a bent twin blob sha, a source whose DISK sha
                  has left its STEP 0 literal, a deleted record.
  F-C10-RESUME-T  THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED.  A whole-suite
                  run that does not reproduce the filed FIXTURES_RESUME.txt to
                  the byte writes FIXTURES_RESUME_rerun.txt, prints the delta,
                  LEAVES the artifact of record untouched and exits 1.
                  Planted: a non-reproducing run, a truncated run, an empty run,
                  an appended byte.

HOUSE LAWS OBSERVED HERE
  · TEXT BEFORE RESULT — nothing here rides a bar, scores a row or touches a
    P-* registration.  This is bookkeeping mechanics only.
  · EVERY LEG STATES ITS FAILURE CONDITION and every guard has a BREAK LEG that
    plants a deliberate violation and must go RED, judged ONE PLANT AT A TIME.
  · EVERY GRID WHOLE — every stage, every artifact, every sha.  No sampling.
    The counts are printed and they are totals.
  · NO REPO FILE IS EDITED BY A BREAK LEG.  Every plant runs on a COPY in a
    throwaway temp tree, or on a deep copy of an in-memory dict.  The real
    quarantine at `_partial_*/` is opened read-only and never written.
  · DETERMINISM — the transcript carries no clock, no temp path, no set
    iteration order AND NO LIVE VALUE OUT OF A FILE THIS TRACK DOES NOT OWN
    [LEAN R8].  Two runs are byte-identical, and a run that is not says so
    instead of overwriting the evidence [LEAN R9].

Run:
  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 \
         PYTHONDONTWRITEBYTECODE=1
  ~/venvs/naiad/bin/python -B scripts/tierc10_resume_fixtures.py [leg-substring ...]

Exit 0 = every leg GREEN and every break leg RED.  Exit 1 = at least one leg
RED, or a break leg that failed to go red (a guard nobody has seen fail).
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

TC = ROOT / "research_outputs" / "tierc10"
LEDGER_REL = "research_outputs/tierc10/PROGRESS.json"
PROGRESS_PATH = ROOT / LEDGER_REL
STEP0_RECORD_PATH = TC / "STEP0_RECORD.json"
TRANSCRIPT = "FIXTURES_RESUME.txt"

# ── THE EXTERNAL ANCHOR ────────────────────────────────────────────────────
# F-C10-RESUME-1, -4 and -5 all read their answer out of PROGRESS.json, so a
# builder who edits PROGRESS.json defeats all three with one line: re-record a
# tampered artifact's sha, promote a blockered stage, de-record an artifact.
# PROGRESS.json IS TRACKED (committed at f97cded despite .gitignore), so an
# answer exists OUTSIDE the working tree, and the pinned sha is typed here as a
# module literal so the anchor itself is pinned and not merely "whatever git
# says today".  F-C10-RESUME-0 is that check.  [LEAN-HEPHAESTUS] R5
PINNED_LEDGER_REV = "f97cded"
PINNED_LEDGER_SHA = "b85eacc44a366359b718d0e0b13ca21bc9bafb0be79cda351875f8837c50b845"

# ── the ONLY files that may sit LOOSE in the tierc10 root with no ledger
#    record.  STEP 0's own directory IS this root and is sweep-exempt [LEAN R3],
#    which left the root itself unswept; it is swept NON-RECURSIVELY here
#    against the UNION of every recorded artifact plus this NAMED list.
#    [LEAN-HEPHAESTUS] R7
TC_ROOT_ALLOWLIST = (
    "BUILD_DRAFT.md",
    "FIXTURES_RESUME.txt",
    "FIXTURES_RESUME_partial.txt",
    "FIXTURES_RESUME_rerun.txt",
    "FIXTURES_RF.txt",
    "OPERATOR_RULINGS.md",
    "PROGRESS.json",
    "STEP0_RECORD.json",
)

# ── THE RANGEFINDER'S CODE, PINNED.  _qr5_scan used to glob pine/*.pine — a
#    MOVING SET — and that moving set was baked into STEP0_RECORD.json's filed
#    bytes, so adding ANY .pine file turned leg 6 red for a reason with nothing
#    to do with STEP 0.  The RECORDED scan is over this pinned list; the BREADTH
#    of the [Q-R5] claim is kept by a separate live sweep of every other
#    pine/*.pine whose hits are still RED but whose MEMBERSHIP never enters the
#    filed bytes.  [LEAN-HEPHAESTUS] R6
RF_CODE_FILES = (
    "analytics/rangefinder_census.py",
    "engine/rangefinder.py",
    "pine/SS12_RangeFinder_v2.pine",
    "scripts/rangefinder_twin.py",
)

REWRITE_STEP0 = False                # set by main(); see step0_record_presence_findings

SEED = 20260921
AS_OF = "2026-09-21T16:00:00Z"
CLOSE_MS = 1790006400000
LEGAL_STATUS = ("COMPLETE-VERIFIED", "PARTIAL", "ABSENT")
STAGE_KEYS = ("stage", "status", "as_of", "artifact_shas", "fixtures", "blockers")
FIXTURE_KEYS = ("suite", "exit_code", "legs_red", "legs_total",
                "transcript_drift", "transcript_sha_before",
                "transcript_sha_after", "wall_seconds")

# ── the two LAW-2 kill-partials, typed HERE as INDEPENDENT literals so the
#    three-way check below is never one number counted twice ─────────────────
QUARANTINED_PARTIALS = {
    "lanes/FIXTURES_LANES_partial.txt":
        "d531b43b7248bc6a44d11a31d154be1b5f8dd6f77bb54d5aeaf80736de50e009",
    "panel/FIXTURES_PANEL_partial.txt":
        "4a068ea4d20a920a2e4fdb1a4ed0a60752fae391b3e5ad72e85877854bb5cbeb",
}

# ── STEP 0, rebuilt from what R0 established.  Every literal here is
#    RE-VERIFIED against disk / git by F-C10-RESUME-6 before it is believed. ──
STEP0_COMMIT = "d63592f"          # the STEP 0 commit of record (branch v12-v1-census)
STEP0_SOURCES = {
    # path                              : sha256 EXPECTED ON DISK NOW
    "pine/SS12_RangeFinder_v2.pine":
        "4bed1e01189106c0339d0375a1049f2d9868d54c3644363a9436d43c7a14ddb6",
    "scripts/rangefinder_twin.py":
        "168d6229d33a4387c90f2d6318de0c6a9ed58b5fde9ddfcfbfcb24c6ace2206b",
    "engine/rangefinder.py":
        "bbae464fdc8e0e01fc90b286aa79e726fcff4422e6118dee1173f2460dab84d4",
    "analytics/rangefinder_census.py":
        "19c5507ff2d39b68aa119ff701aef58a2d219fa287c34cdf7302ebf2bbb7b37d",
}
# the twin is the ONE STEP 0 source whose bytes moved after STEP 0, by the
# Stage 0a anchor edit; its STEP 0 blob sha is recorded beside its current one.
STEP0_TWIN_BLOB_SHA = "7646b5762490e699f71193ad38f5e265103ca95fa3fc58b5cda6e5993f3772e9"
TWIN_SANCTIONED = ("RECORD_ANCHOR_MS", "bars_4h", "daily_bars")

PINS_OF_RECORD = (           # ORDER IS PART OF THE RECORD — export order is bytes
    ("LEG_MIN", 0.5),
    ("REV_MIN", 1.75),
    ("TOUCH_EPS", 0.60),
    ("DEV_RETURN_BARS", 7),
    ("BREAK_CONFIRM_N", 8),
    ("BREAK_MARGIN", 1.5),
    ("BOUNDARY_MODE", "body"),
    ("SCALE_MULT", 3.0),
    ("FLIP_HOLD_MARGIN", 1.0),
    ("FLIP_HOLD_BARS", 6),
    ("MEM_TTL_BARS", 400),
    ("ATR_LEN", 14),
)
PINE_PATH = ROOT / "pine" / "SS12_RangeFinder_v2.pine"
PINE_NUM_VARS = {"LEG_MIN": "legMin", "REV_MIN": "revMin", "TOUCH_EPS": "touchEps",
                 "DEV_RETURN_BARS": "devRet", "BREAK_CONFIRM_N": "brkN",
                 "BREAK_MARGIN": "brkMargin", "SCALE_MULT": "scaleMult",
                 "FLIP_HOLD_MARGIN": "flipMargin", "FLIP_HOLD_BARS": "flipBars",
                 "MEM_TTL_BARS": "memTtl"}

# ═══════════════════════════════════════════ THE EXEMPTION REGISTRY
# A waiver of byte-reproducibility lives HERE or it does not exist.
# F-C10-RESUME-4 forces every field below to be filled and CORROBORATED.
EXEMPTIONS = (
    {
        "id": "X-STAGE-D-VENUE",
        "suite": "scripts/tierc10_data_fixtures.py",
        "stage": "D-CORE",
        "transcript": "research_outputs/tierc10/data/FIXTURES_STAGE_D.txt",
        # the substring(s) by which a PROGRESS.json fixture record is recognised
        # as falling under this waiver — each one must match at least one real
        # record of the named stage, or it is a dead pattern and the leg is RED
        "covers_record_match": ("Stage D fixtures",),
        "legs": ("F-D-1", "F-D-1b"),
        "conditional_legs": ("F-D-2",),
        "waives": ("transcript byte-reproducibility of the Stage D ONLINE "
                   "transcript FIXTURES_STAGE_D.txt"),
        "reason": (
            "These legs reach the public venue APIs by design (Binance USDT-M "
            "fapi; Bybit v5 for MNT) and F-D-1b classifies every sampled bar "
            "against the venue's TWO publications — the bulk archive and REST. "
            "The bulk archive BACKFILLS: bars it had not published when the "
            "filed run executed it publishes the next day. The transcript is "
            "therefore a function of the venue's publication state at run time, "
            "not of this build's inputs, and demanding byte-identity of it "
            "would leave a permanently red leg that says nothing about the "
            "build's integrity. The ARTIFACTS Stage D files are unaffected and "
            "are re-hashed in full by F-C10-RESUME-1; only the TRANSCRIPT is "
            "waived, and only for this suite."),
        "evidence": {
            "filed": {"archive-only": 74, "both": 215, "rest": 28, "rest-only": 105},
            "remeasured": {"archive-only": 74, "both": 223, "rest": 20, "rest-only": 105},
            "delta_bars": 8,
            "measured_on": "2026-09-22 (R0), against the 2026-09-21 filed run",
            "source": {
                "file": "research_outputs/tierc10/PROGRESS.json",
                "stage": "D-CORE",
                "field": "blockers",
                "match": "TRANSCRIPT BYTE-REPRODUCIBILITY IS DISPROVEN",
            },
        },
        "ruling_status": ("EXECUTOR READING — PUT TO THE OPERATOR, UNRULED. "
                          "See [LEAN-HEPHAESTUS] R1."),
    },
)

LEANS = (
    "[LEAN-HEPHAESTUS] R1 WHAT F-C10-RESUME HASHES. The contract says 'every "
    "COMPLETE stage re-hashes identical to its PROGRESS.json record'. I read "
    "'record' as the FILED ARTIFACT CONTENT SHAS, never the fixture transcript, "
    "and I exempt any leg that reaches a venue. EVIDENCE, measured not asserted: "
    "F-D-1b's publication census moved {archive-only:74, both:215, rest:28, "
    "rest-only:105} -> {archive-only:74, both:223, rest:20, rest-only:105} "
    "between the 2026-09-21 filed run and R0's 2026-09-22 re-run — 8 bars the "
    "bulk archive did not publish on the 21st and does publish on the 22nd. A "
    "transcript-byte demand on Stage D is therefore permanently red for a reason "
    "that has nothing to do with this build's integrity. The waiver is narrow "
    "(one suite, one transcript, the artifacts still fully re-hashed) and it is "
    "REGISTERED in EXEMPTIONS, where F-C10-RESUME-4 keeps it named. THE OPERATOR "
    "MAY WANT TO RULE ON THIS — it is an executor's reading of a contract clause.",
    "[LEAN-HEPHAESTUS] R2 THE QUARANTINE REDIRECT. PROGRESS.json records the two "
    "kill-partials at their ORIGINAL paths (panel/ and lanes/), but R0's own LAW-2 "
    "quarantine MOVED them to _partial_20260922T0955Z/<same subpath>. A naive "
    "re-hash is red on two files for a move the ledger itself ordered. I resolve a "
    "recorded path that is absent against the LAW-2 quarantine dirs at the IDENTICAL "
    "relative subpath, and ONLY when the quarantined bytes hash to the recorded sha "
    "— a redirect that cannot launder a tamper (F-C10-RESUME-1's fourth plant "
    "proves it). Every redirect is PRINTED by name. The clean repair belongs to "
    "whoever owns PROGRESS.json: re-path those two records. CROSS-TRACK REQUEST.",
    "[LEAN-HEPHAESTUS] R3 THE UNRECORDED-FILE SWEEP'S SCOPE. 'A file the ledger "
    "does not record' is judged inside a stage's OWN directory, taken as the common "
    "parent of its recorded artifacts. STEP 0's common parent is the tierc10 root "
    "itself, which holds cross-stage bookkeeping (PROGRESS.json, BUILD_DRAFT.md, "
    "OPERATOR_RULINGS.md, the quarantine, this transcript and every other stage's "
    "tree). Sweeping it would call 1,072 files 'unrecorded'. STEP 0 is therefore "
    "NAMED AS EXEMPT FROM THE SWEEP rather than silently passed, and its one "
    "artifact is still re-hashed. The sweep runs on COMPLETE-VERIFIED stages only: "
    "a PARTIAL stage is expected to have loose ends (census/smoke/'s 22 disclosed "
    "lookalike files sit under the PARTIAL CENSUS-R and are not swept).",
    "[LEAN-HEPHAESTUS] R4 STEP0_RECORD.json IS WRITTEN BY THIS MODULE, AND THAT IS "
    "CIRCULAR UNLESS THE CHECK IS INDEPENDENT. STEP 0's manifest died with the "
    "killed session's scratchpad (`find` for STEP0* returns nothing), so LAW 1(b) "
    "has no record. I rebuild it deterministically here. F-C10-RESUME-6 does NOT "
    "merely round-trip it: it re-measures all four source shas from disk, re-reads "
    "the twin's STEP 0 blob from git, re-reads the twelve pins from the live port "
    "AND re-parses them from the Pine source, and only then compares. The write is "
    "WRITE-ONCE: the file is created if absent and is never silently rewritten "
    "(--rewrite-step0-record is the explicit refresh), so the byte-reproducibility "
    "claim is not vacuous — a hand edit or a drift shows RED. R0-REPAIR: 'created if "
    "absent' was itself the laundry chute — `rm STEP0_RECORD.json && re-run` rebuilt "
    "the whole record from whatever the tree looked like. ABSENCE IS NOW A FINDING; "
    "only --rewrite-step0-record writes.",
    "[LEAN-HEPHAESTUS] R5 THE LEDGER IS ANCHORED OUTSIDE ITSELF. Legs 1, 4 and 5 all "
    "read their answer out of PROGRESS.json, so one working-tree edit defeated all "
    "three at once and the suite stayed GREEN: a re-recorded sha over a tampered "
    "artifact, a PARTIAL stage promoted to COMPLETE-VERIFIED with its blockers "
    "emptied, an artifact de-recorded and deleted. PROGRESS.json IS TRACKED (committed "
    "at f97cded despite .gitignore), so an answer exists outside the working tree. "
    "F-C10-RESUME-0 pins f97cded's blob sha as a MODULE LITERAL "
    "(b85eacc4…) and demands that every stage the working tree calls "
    "COMPLETE-VERIFIED be COMPLETE-VERIFIED at HEAD with a BYTE-IDENTICAL block. "
    "I CHOSE THE WEAKER OF TWO RULES so the ledger can still advance: a PARTIAL or "
    "ABSENT stage moves freely in the working tree; a COMPLETE-VERIFIED block moves "
    "ONLY through a commit. The orchestrator owns commits, so promotion is the "
    "orchestrator's act, not a builder's edit — which is the discipline this estate "
    "already runs on.",
    "[LEAN-HEPHAESTUS] R6 THE [Q-R5] SCAN'S FILE LIST IS PINNED, ITS BREADTH IS NOT. "
    "_qr5_scan() globbed pine/*.pine — 10 files today, 4 of them untracked additions "
    "with nothing to do with the RangeFinder — and that MOVING MEMBERSHIP went into "
    "STEP0_RECORD.json's filed bytes, so adding or removing ANY .pine file made leg 6 "
    "RED for a reason with nothing to do with STEP 0 (a false red, not a false green, "
    "but a confusing one). The RECORDED scan is now over four pinned files: the Pine "
    "source, the machine, the port, the twin. The CLAIM'S BREADTH IS NOT WEAKENED — "
    "_qr5_sweep() scans every other pine/*.pine on every run and a marker or a 0.67 "
    "there is still RED; only the moving set's membership is kept out of the record. "
    "This changed STEP0_RECORD.json's bytes, so it was re-filed with "
    "--rewrite-step0-record, deliberately and by name.",
    "[LEAN-HEPHAESTUS] R7 THE TIERC10 ROOT IS SWEPT, NON-RECURSIVELY. [LEAN R3] made "
    "STEP 0 sweep-exempt because its stage_root IS the tierc10 root — honest, but it "
    "left the root itself unswept, so a file dropped straight into "
    "research_outputs/tierc10 was invisible (this track's own two artifacts among "
    "them). The root is now swept NON-RECURSIVELY against the UNION of every recorded "
    "artifact of EVERY stage plus a NAMED allowlist that is printed in full. "
    "Non-recursively because the sub-directories belong to their stages and four of "
    "them are PARTIAL stages under live construction by other tracks; sweeping those "
    "recursively would be a permanent red that says nothing. A NEW loose file in the "
    "root will turn this leg RED, and that is the intended answer, not a bug.",
    "[LEAN-HEPHAESTUS] R8 NO FOREIGN FILE'S LIVE STATE MAY ENTER THE TRANSCRIPT. The "
    "line 'whole LEGS table = N legs' was AST-parsed live out of "
    "scripts/tierc10_data_fixtures.py, a file THIS TRACK DOES NOT OWN, and printed "
    "into the filed artifact — so the D-CORE owner editing their own suite broke this "
    "track's DETERMINISM claim (15 -> 19 legs across two runs of the review; the same "
    "file has moved again since, sha 626c0a97… -> 3807d905…). Every value derived "
    "from a foreign file now goes through clock() to STDOUT ONLY. What stays on the "
    "transcript is what this module PINS: sorted(x['legs']), a module literal, "
    "verified equal to the suite's own needs_net set on every run. The transcript IS "
    "still a function of PROGRESS.json — by design, since that is this track's "
    "declared input — and the no-clobber guard below turns any ledger advance into an "
    "explicit re-file instead of a silent overwrite.",
    "[LEAN-HEPHAESTUS] R9 THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED. main() wrote "
    "FIXTURES_RESUME.txt unconditionally at the end of every whole-suite run, so an "
    "ordinary sanctioned run DESTROYED the filed artifact and the evidence of the "
    "original with it — silently, exiting 0. A run that produces bytes different from "
    "the filed transcript now writes FIXTURES_RESUME_rerun.txt instead, prints the "
    "first differing lines, LEAVES THE ARTIFACT OF RECORD UNTOUCHED and EXITS 1. "
    "--refile-transcript is the deliberate, named re-file.",
    "[LEAN-HEPHAESTUS] R10 THE ANCHOR NOW LOOKS BOTH WAYS, AND HERE IS WHAT IT STILL "
    "CANNOT DO. [LEAN R5]'s anchor asked what a COMPLETE claim was standing on and "
    "never asked what happened to a COMPLETE claim that was WITHDRAWN. A review beat "
    "it twice with a spy on file_sha: demoting 'A (stamps)' from COMPLETE-VERIFIED to "
    "PARTIAL in the working tree took files_hashed from 647 to 637 — its 10 filed "
    "artifacts left EVERY guard in the suite — with findings 0 and the whole suite "
    "GREEN; deleting the block outright did the same. F-C10-RESUME-0 now runs a THIRD "
    "loop, over HEAD's own stages: a stage COMPLETE-VERIFIED at HEAD must still be "
    "present, and still COMPLETE-VERIFIED, on disk. Three plants prove it — DEMOTED, "
    "DELETED and DEMOTE-THEN-TAMPER, the laundering case where the demotion hides a "
    "re-recorded sha. This matters most AHEAD of us, not behind: D-CORE, CENSUS-R, "
    "LANES and BRK are NOT COMPLETE-VERIFIED at the pinned rev f97cded, so when they "
    "complete, the pinned loop can never guard them and this loop is all there is. "
    "THE LIMIT, STATED PLAINLY AND PRINTED IN THE TRANSCRIPT: this fixture is still "
    "the record checking the record, one hop out. It proves the working tree has not "
    "departed from the COMMITTED ledger, and that f97cded's blob has not been "
    "rewritten under it. It does NOT judge the honesty of a COMMIT: for a stage "
    "completed after f97cded, HEAD is its own witness and only review stands behind "
    "it. It does NOT judge a stage that is COMPLETE-VERIFIED on neither side. It does "
    "NOT prove the ledger describes the world — that a recorded sha is the artifact's "
    "real sha is F-C10-RESUME-1's job, on disk. And it cannot defend itself against "
    "an edit to THIS FILE, where the pin and the three loops live. A named limit is "
    "worth more than a guard that pretends.",
    "[LEAN-HEPHAESTUS] R11 THE VENUE EXEMPTION IS BOUND TO ITS STAGE, NOT JUST TO A "
    "SUITE. Every hardening of F-C10-RESUME-4 validated the exemption's OWN suite — "
    "its LEGS table, its venue client, its re-derivable evidence — and NOTHING tied "
    "x['suite'] to x['stage'] or to the records x['covers_record_match'] selects; "
    "they were unrelated free strings. The review beat it in one move: copy "
    "X-STAGE-D-VENUE VERBATIM (same real, parseable, venue-reaching "
    "scripts/tierc10_data_fixtures.py, same corroborated evidence, same 675-char "
    "reason), change ONLY the id, the stage, the transcript and covers_record_match, "
    "and a REAL planted drift on LANES (B mech) went from ONE finding to ZERO — every "
    "hardened check passed, because every one of them aimed at the BORROWED suite. It "
    "worked for LANES, BRK, D-CORE and CENSUS-R. The builder's own 'BLANKET SECOND "
    "EXEMPTION' plant only ever bit because it picked an unreadable suite; pick a "
    "readable one and the leg was silent. THE LEDGER ALREADY CARRIES THE BINDING — "
    "D-CORE's block names tierc10_data_fixtures, LANES's names tierc10_lanes_fixtures, "
    "BRK's names tierc10_brk_fixtures — so the binding is now DEMANDED: "
    "Path(x['suite']).stem must occur in the exempted stage's own ledger block, and "
    "the field that carries it is printed. Four plants prove it, including the "
    "borrowed waiver judged on the binding alone and on the covered drift alone. "
    "THE LIMIT: the binding is read out of PROGRESS.json, and for D-CORE it lands in "
    "a BLOCKER SENTENCE that another track owns. If that track rewrites the sentence "
    "without naming the suite, this leg goes RED for a reason that is not a tamper — "
    "a false red, not a false green, and the honest trade. CROSS-TRACK REQUEST: keep "
    "each stage block naming the suite that produced its fixture records.",
)

# ═══════════════════════════════════════════════════════ transcript plumbing
LINES: list[str] = []
PASSED: list[str] = []
FAILED: list[str] = []


def say(line: str = "") -> None:
    print(line)
    LINES.append(line)


def clock(line: str) -> None:
    """Anything that cannot be reproduced byte for byte goes to stdout ONLY —
    the transcript is compared across runs."""
    print(line)


def check(fixture: str, ok: bool, detail: str) -> bool:
    say(f"  [{'PASS' if ok else 'FAIL'}] {fixture}: {detail}")
    return ok


def prove(fixture: str, title: str, fails_if: str, break_leg, real_leg) -> None:
    """Both legs, in order. The break leg must go RED or the fixture is void —
    a guard nobody has seen fail is a guard nobody has seen."""
    say(f"\n{fixture} — {title}")
    say(f"  FAILS IF: {fails_if}")
    try:
        b_ok, b_detail = break_leg()
    except Exception as e:                  # a break leg that errors proved nothing
        b_ok, b_detail = True, f"break leg RAISED {e.__class__.__name__}: {e}"
    say(f"  [BREAK] deliberate violation -> "
        f"{'RED (correct)' if not b_ok else 'NOT RED (FIXTURE IS VOID)'}: {b_detail}")
    try:
        r_ok, r_detail = real_leg()
    except Exception as e:                  # a fixture that errors is a fail
        r_ok, r_detail = False, f"raised {e.__class__.__name__}: {e}"
    green = check(fixture, r_ok, r_detail)
    if b_ok:
        FAILED.append(f"{fixture} (break leg did not go RED — fixture proves nothing)")
    elif not green:
        FAILED.append(fixture)
    else:
        PASSED.append(fixture)


def plants(rows) -> tuple[bool, str]:
    """One plant per guard, judged ONE AT A TIME. `rows` = (name, thunk ->
    list of findings). A plant that yields NO finding PASSED — the break leg is
    then not RED and the fixture void.

    A plant that CRASHES is NOT a catch. It used to be counted as one ("RAISED
    <Class>: …"), so a plant could go red for a reason with nothing to do with
    the sabotage it planted and the guard would never have been exercised. An
    unexpected exception is now a FIXTURE DEFECT and voids the break leg."""
    passed, caught, crashed = [], [], []
    for name, thunk in rows:
        try:
            found = thunk()
        except SystemExit as e:             # a HALT is a finding, and the best kind
            found = [f"HALT: {e}"]
        except Exception as e:              # a CRASH proves nothing about the guard
            crashed.append(f"{name} -> RAISED {e.__class__.__name__}: {e}")
            continue
        (caught if found else passed).append(
            f"{name} -> {str(found[0])[:150]}" if found else name)
    if crashed:
        return True, (f"{len(crashed)} plant(s) CRASHED instead of being CAUGHT — an "
                      f"unexpected exception is a FIXTURE DEFECT, not a finding: "
                      + " · ".join(crashed))
    if passed:
        return True, f"{len(passed)} plant(s) PASSED: {passed}"
    return False, (f"all {len(caught)} plants caught, one at a time: "
                   + " · ".join(caught))


# ═══════════════════════════════════════════════════════════════ primitives
def sha_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def file_sha(p: Path) -> tuple[str, int]:
    b = p.read_bytes()
    return sha_bytes(b), len(b)


def load_progress() -> dict:
    if not PROGRESS_PATH.exists():
        raise SystemExit(f"HALT: LAW 6 breached — no ledger at {PROGRESS_PATH}")
    return json.loads(PROGRESS_PATH.read_text(encoding="utf-8"))


def quarantine_dirs(base: Path = TC) -> list[Path]:
    return sorted((d for d in base.glob("_partial_*") if d.is_dir()),
                  key=lambda d: d.name)


def stage_root(recorded: dict) -> str:
    """The stage's own directory: the common parent of its recorded artifacts."""
    parents = {str(Path(p).parent) for p in recorded}
    return os.path.commonpath(sorted(parents)).replace(os.sep, "/")


# ═══════════════════════════ F-C10-RESUME-0 · THE EXTERNAL ANCHOR
def _jb(v) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _stage_bytes(stage: dict) -> bytes:
    """A stage block's CANONICAL bytes — key-order independent, so comparing two
    ledgers compares CONTENT and never formatting."""
    return _jb(stage).encode("utf-8")


def _stages_by_name(doc: dict) -> dict:
    return {s.get("stage"): s for s in (doc.get("stages") or [])
            if isinstance(s, dict)}


def _stage_delta(d: dict, h: dict) -> str:
    """Name WHAT moved, so a red anchor reads as an accusation and not a hash."""
    bits: list[str] = []
    da = d.get("artifact_shas") or {}
    ha = h.get("artifact_shas") or {}
    gone = sorted(set(ha) - set(da))
    added = sorted(set(da) - set(ha))
    moved = sorted(k for k in (set(da) & set(ha)) if _jb(da[k]) != _jb(ha[k]))
    if gone:
        bits.append(f"{len(gone)} artifact(s) DE-RECORDED, e.g. {gone[0]}")
    if added:
        bits.append(f"{len(added)} artifact(s) ADDED to the record, e.g. {added[0]}")
    if moved:
        k = moved[0]
        bits.append(f"{len(moved)} recorded sha/bytes RE-RECORDED, e.g. {k} "
                    f"{str((ha[k] or {}).get('sha256'))[:12]}… -> "
                    f"{str((da[k] or {}).get('sha256'))[:12]}…")
    nd, nh = len(d.get("blockers") or []), len(h.get("blockers") or [])
    if nd != nh:
        bits.append(f"blockers {nh} -> {nd}")
    if d.get("status") != h.get("status"):
        bits.append(f"status {h.get('status')!r} -> {d.get('status')!r}")
    if not bits:
        keys = sorted(k for k in (set(d) | set(h)) if _jb(d.get(k)) != _jb(h.get(k)))
        bits.append(f"field(s) {keys} differ")
    return "; ".join(bits)


def anchor_findings(disk: dict, head_blob: bytes | None, pinned_blob: bytes | None,
                    pinned_sha: str = PINNED_LEDGER_SHA,
                    rev: str = PINNED_LEDGER_REV) -> list[str]:
    """THE ONE LEG THAT DOES NOT READ ITS ANSWER OUT OF PROGRESS.json.

    THE HOLE THIS CLOSES.  Legs 1, 4 and 5 judge the ledger by the ledger.  Three
    one-line working-tree edits defeated all of them and left the suite GREEN:
      (1) tamper a filed artifact, then RE-RECORD its sha and byte count;
      (2) flip a PARTIAL stage to COMPLETE-VERIFIED, empty its blockers, set its
          fixture record to exit 0 / 0 red legs;
      (3) DE-RECORD an artifact and delete it from disk.
    Each is exactly the "named future lie" this suite claims to make impossible.

    THE RULE, stated so the ledger can still legitimately ADVANCE:
      · the pinned rev's blob must hash to the literal typed in this module;
      · every stage the PINNED blob calls COMPLETE-VERIFIED must still be
        COMPLETE-VERIFIED at HEAD and byte-identical there — a completed stage
        is settled and may not be quietly rewritten by a later commit;
      · every stage the WORKING TREE calls COMPLETE-VERIFIED must exist at HEAD,
        be COMPLETE-VERIFIED at HEAD, and be byte-identical to HEAD's block;
      · AND THE SAME RULE READ THE OTHER WAY — every stage HEAD calls
        COMPLETE-VERIFIED must still be present in the working tree and still be
        COMPLETE-VERIFIED there.
    A PARTIAL or ABSENT stage may move freely in the working tree — that is the
    work in progress.  A COMPLETE-VERIFIED block moves ONLY through a commit.

    R1-REPAIR — THE ANCHOR ONLY LOOKED ONE WAY.  The two loops above ask what a
    COMPLETE claim is standing on; NEITHER asks what happened to a COMPLETE claim
    that was WITHDRAWN.  A review beat it twice, instrumented on file_sha:
      BASELINE : findings 0, files_hashed 647, of them 10 for 'A (stamps)'
      DEMOTED  ('A (stamps)' COMPLETE-VERIFIED -> PARTIAL on disk, one artifact
                 sha re-recorded as 64 zeros): findings 0, files_hashed 637,
                 'A (stamps)' files hashed 0
      DELETED  (the whole 'A (stamps)' block removed): findings 0, 637, 0
    Ten filed artifacts left every guard in the suite and the suite stayed GREEN,
    because leg 1 re-hashes COMPLETE-VERIFIED stages and a demoted stage is not
    one.  A DEMOTION IS A WITHDRAWAL OF A SETTLED CLAIM and it is exactly as much
    a commit's act as a promotion.  The third loop below is that rule.  It also
    carries the build forward: D-CORE, CENSUS-R, LANES and BRK are NOT
    COMPLETE-VERIFIED at the pinned rev, so when they complete, the pinned loop
    can never guard them and this loop is the only thing that will.
    """
    bad: list[str] = []
    if pinned_blob is None:
        bad.append(f"the pinned ledger blob {rev}:{LEDGER_REL} is UNREACHABLE — the "
                   f"anchor this whole suite stands on is gone; silence is not health")
    else:
        got = sha_bytes(pinned_blob)
        if got != pinned_sha:
            bad.append(f"PINNED ANCHOR MOVED: {rev}:{LEDGER_REL} hashes {got[:16]}…, "
                       f"not the module literal of record {pinned_sha[:16]}… — the "
                       f"committed ledger this fixture anchors on was rewritten")
    if head_blob is None:
        bad.append(f"HEAD:{LEDGER_REL} is UNREACHABLE — the ledger is not committed, "
                   f"so NOTHING outside the working tree can contradict it and every "
                   f"ledger-side leg in this suite is self-referential")
        return bad
    try:
        head = json.loads(head_blob.decode("utf-8"))
    except Exception as e:
        return bad + [f"HEAD:{LEDGER_REL} will not parse as JSON: "
                      f"{e.__class__.__name__}: {e}"]
    head_st = _stages_by_name(head)
    disk_st = _stages_by_name(disk)
    if pinned_blob is not None:
        try:
            pin_st = _stages_by_name(json.loads(pinned_blob.decode("utf-8")))
        except Exception:
            pin_st = {}
        for name in sorted(pin_st, key=str):
            p = pin_st[name]
            if p.get("status") != "COMPLETE-VERIFIED":
                continue
            h = head_st.get(name)
            if h is None:
                bad.append(f"{name!r}: COMPLETE-VERIFIED at the pinned rev {rev} and "
                           f"GONE at HEAD — a completed stage was deleted by a commit")
            elif h.get("status") != "COMPLETE-VERIFIED":
                bad.append(f"{name!r}: COMPLETE-VERIFIED at {rev}, {h.get('status')!r} "
                           f"at HEAD — a completed stage was DEMOTED by a commit")
            elif _stage_bytes(h) != _stage_bytes(p):
                bad.append(f"{name!r}: its COMPLETE-VERIFIED block was REWRITTEN "
                           f"between {rev} and HEAD ({_stage_delta(h, p)}) — a "
                           f"completed stage is settled")
    for name in sorted(disk_st, key=str):
        d = disk_st[name]
        if d.get("status") != "COMPLETE-VERIFIED":
            continue
        h = head_st.get(name)
        if h is None:
            bad.append(f"{name!r}: the WORKING TREE calls it COMPLETE-VERIFIED and "
                       f"HEAD carries no such stage — A COMPLETE CLAIM MAY NOT BE "
                       f"BORN IN AN UNCOMMITTED EDIT")
        elif h.get("status") != "COMPLETE-VERIFIED":
            bad.append(f"{name!r}: PROMOTED IN THE WORKING TREE — {h.get('status')!r} "
                       f"at HEAD, COMPLETE-VERIFIED on disk ({_stage_delta(d, h)}). A "
                       f"stage is promoted by a commit or it is not promoted")
        elif _stage_bytes(d) != _stage_bytes(h):
            bad.append(f"{name!r}: its COMPLETE-VERIFIED block was EDITED IN THE "
                       f"WORKING TREE ({_stage_delta(d, h)}) — the committed blob is "
                       f"the record and an uncommitted edit is not a correction")
    # THE THIRD LOOP — THE ANCHOR LOOKS BOTH WAYS [LEAN R10]. A settled claim may
    # not be QUIETLY WITHDRAWN either: a stage COMPLETE-VERIFIED at HEAD must
    # still be there, and still be COMPLETE-VERIFIED, in the working tree.
    for name in sorted(head_st, key=str):
        h = head_st[name]
        if h.get("status") != "COMPLETE-VERIFIED":
            continue
        d = disk_st.get(name)
        n_art = len(h.get("artifact_shas") or {})
        if d is None:
            bad.append(f"{name!r}: COMPLETE-VERIFIED at HEAD and GONE FROM THE "
                       f"WORKING TREE — deleting a settled stage's block deletes "
                       f"every guard that stood on its {n_art} recorded artifact(s) "
                       f"at once, and this suite would go GREEN over the hole. A "
                       f"completed stage is withdrawn by a commit or it is not "
                       f"withdrawn")
        elif d.get("status") != "COMPLETE-VERIFIED":
            bad.append(f"{name!r}: DEMOTED IN THE WORKING TREE — COMPLETE-VERIFIED "
                       f"at HEAD, {d.get('status')!r} on disk ({_stage_delta(d, h)}). "
                       f"A demotion drops the stage's {n_art} artifact(s) out of "
                       f"every re-hash in this suite; a settled stage is demoted by "
                       f"a commit or it is not demoted")
        # BYTE-IDENTITY when BOTH sides call it COMPLETE-VERIFIED is asserted by
        # the working-tree loop above; it is deliberately NOT repeated here, so a
        # single tamper prints a single finding and the count stays readable.
    return bad


def resume0_break():
    disk = load_progress()
    head_blob = _git_blob("HEAD", LEDGER_REL)
    pin_blob = _git_blob(PINNED_LEDGER_REV, LEDGER_REL)

    def mutated(fn) -> list[str]:
        d = copy.deepcopy(disk)
        fn(d)
        return anchor_findings(d, head_blob, pin_blob)

    def rerecord(d):
        """ATTACK 1 — tamper a filed artifact, then re-record its sha and bytes
        exactly as a lying builder would. Legs 1 and 5 see nothing."""
        st = next(s for s in d["stages"] if s["status"] == "COMPLETE-VERIFIED")
        k = sorted(st["artifact_shas"])[0]
        st["artifact_shas"][k]["sha256"] = "0" * 64
        st["artifact_shas"][k]["bytes"] = st["artifact_shas"][k]["bytes"] + 1

    def promote(d):
        """ATTACK 2 — flip a blockered PARTIAL stage to COMPLETE-VERIFIED, empty
        its blockers, and clean its fixture record. wellformed_findings -> []."""
        st = next(s for s in d["stages"]
                  if s["status"] == "PARTIAL" and s["blockers"])
        st["status"] = "COMPLETE-VERIFIED"
        st["blockers"] = []
        for f in st["fixtures"]:
            f["exit_code"] = 0
            f["legs_red"] = 0
            f["legs_total"] = f.get("legs_total") or 1

    def _settled() -> str:
        """The name of a stage that HEAD itself calls COMPLETE-VERIFIED, chosen
        DETERMINISTICALLY (first in sort order) so the plant, and the transcript
        line it produces, are the same on every run."""
        h = json.loads(head_blob.decode("utf-8")) if head_blob else {}
        names = sorted(n for n, st in _stages_by_name(h).items()
                       if st.get("status") == "COMPLETE-VERIFIED")
        if not names:
            raise AssertionError("no COMPLETE-VERIFIED stage exists at HEAD to "
                                 "withdraw — this plant cannot be planted")
        return names[0]

    def demote(d):
        """ATTACK 4 — WITHDRAW a settled claim in the working tree. Leg 1
        re-hashes COMPLETE-VERIFIED stages, so a demoted stage's artifacts leave
        every guard in the suite at once and the old anchor said nothing."""
        st = next(s for s in d["stages"] if s["stage"] == _settled())
        st["status"] = "PARTIAL"

    def delete_stage(d):
        """ATTACK 5 — delete the settled stage's block outright. Same hole, one
        step cruder: nothing is left on disk to compare, and absence was health."""
        name = _settled()
        d["stages"] = [s for s in d["stages"] if s["stage"] != name]

    def demote_then_tamper(d):
        """ATTACK 6 — THE LAUNDERING CASE. Demote the stage AND re-record one of
        its artifact shas. Under the old anchor the demotion hid the tamper: the
        re-record loop only ran over stages the working tree still called
        COMPLETE-VERIFIED."""
        name = _settled()
        st = next(s for s in d["stages"] if s["stage"] == name)
        st["status"] = "PARTIAL"
        k = sorted(st["artifact_shas"])[0]
        st["artifact_shas"][k]["sha256"] = "0" * 64
        st["artifact_shas"][k]["bytes"] = st["artifact_shas"][k]["bytes"] + 1

    def derecord(d):
        """ATTACK 3 — de-record an artifact. The re-hash then has nothing to
        re-hash and the sweep's commonpath NARROWS to match."""
        st = next(s for s in d["stages"] if s["status"] == "COMPLETE-VERIFIED")
        st["artifact_shas"].pop(sorted(st["artifact_shas"])[0])
        if "artifact_count" in st:
            st["artifact_count"] = len(st["artifact_shas"])

    return plants([
        ("RE-RECORDED SHA (ATTACK 1: a COMPLETE-VERIFIED stage's artifact sha and "
         "byte count rewritten in the working tree)", lambda: mutated(rerecord)),
        ("PROMOTED STAGE (ATTACK 2: a blockered PARTIAL flipped to "
         "COMPLETE-VERIFIED, blockers emptied, fixture record cleaned)",
         lambda: mutated(promote)),
        ("DE-RECORDED ARTIFACT (ATTACK 3: an artifact dropped from a "
         "COMPLETE-VERIFIED stage's record)", lambda: mutated(derecord)),
        ("DEMOTED IN THE WORKING TREE (ATTACK 4: a stage COMPLETE-VERIFIED at "
         "HEAD flipped to PARTIAL on disk — its artifacts then leave every "
         "re-hash in this suite)", lambda: mutated(demote)),
        ("DELETED FROM THE WORKING TREE (ATTACK 5: the settled stage's whole "
         "block removed from the ledger on disk)", lambda: mutated(delete_stage)),
        ("DEMOTE-THEN-TAMPER (ATTACK 6, THE LAUNDERING CASE: the settled stage "
         "is demoted AND one of its artifact shas re-recorded, so the demotion "
         "hides the tamper from every COMPLETE-VERIFIED-only guard)",
         lambda: mutated(demote_then_tamper)),
        ("BENT ANCHOR LITERAL (the module's PINNED_LEDGER_SHA replaced by 64 "
         "zeros — the anchor must check itself)",
         lambda: anchor_findings(disk, head_blob, pin_blob, "0" * 64)),
        ("UNREACHABLE ANCHOR (the pinned blob cannot be read — silence is not "
         "health)", lambda: anchor_findings(disk, head_blob, None)),
        ("UNCOMMITTED LEDGER (HEAD carries no ledger at all, so nothing outside "
         "the working tree can contradict it)",
         lambda: anchor_findings(disk, None, pin_blob)),
    ])


def resume0_real():
    disk = load_progress()
    dsha, dn = file_sha(PROGRESS_PATH)
    head_blob = _git_blob("HEAD", LEDGER_REL)
    pin_blob = _git_blob(PINNED_LEDGER_REV, LEDGER_REL)
    bad = anchor_findings(disk, head_blob, pin_blob)
    say(f"      working tree  {LEDGER_REL}")
    say(f"        {dsha}  {dn:>9,} B")
    say(f"      HEAD blob     {sha_bytes(head_blob) if head_blob is not None else 'UNREACHABLE'}"
        f"  {len(head_blob) if head_blob is not None else 0:>9,} B")
    say(f"      pinned blob   {sha_bytes(pin_blob) if pin_blob is not None else 'UNREACHABLE'}"
        f"  {len(pin_blob) if pin_blob is not None else 0:>9,} B  @{PINNED_LEDGER_REV}")
    say(f"      module literal{PINNED_LEDGER_SHA}  PINNED_LEDGER_SHA")
    head_st = _stages_by_name(json.loads(head_blob.decode("utf-8"))) if head_blob else {}
    pinned_blob_cv = sorted(
        n for n, st in _stages_by_name(
            json.loads(pin_blob.decode("utf-8"))).items()
        if st.get("status") == "COMPLETE-VERIFIED") if pin_blob else None
    n_cv = n_free = 0
    say(f"      {'stage':<20} {'HEAD':<18} {'working tree':<18} block vs HEAD")
    for st in disk.get("stages", []):
        name = st.get("stage")
        h = head_st.get(name)
        same = h is not None and _stage_bytes(st) == _stage_bytes(h)
        if st.get("status") == "COMPLETE-VERIFIED":
            n_cv += 1
        else:
            n_free += 1
        say(f"      {str(name):<20} {str(h.get('status') if h else '— not at HEAD'):<18} "
            f"{str(st.get('status')):<18} "
            f"{'byte-identical' if same else 'DIFFERS'}")
        if not same and h is not None:
            # a PARTIAL stage may move; the DETAIL is a live value and stays off
            # the transcript so an in-progress ledger does not churn the artifact
            clock(f"        [stdout only] {name}: {_stage_delta(st, h)}")
    # EVERY GRID WHOLE — a stage that exists at HEAD and NOT on disk would never
    # appear in the loop above, and that is precisely the deletion attack.
    disk_names = {st.get("stage") for st in disk.get("stages", [])}
    for name in sorted(head_st, key=str):
        if name in disk_names:
            continue
        say(f"      {str(name):<20} {str(head_st[name].get('status')):<18} "
            f"{'— NOT IN THE WORKING TREE':<18} ABSENT")
    n_head_cv = sum(1 for st in head_st.values()
                    if st.get("status") == "COMPLETE-VERIFIED")
    pin_cv = []
    if pinned_blob_cv is not None:
        pin_cv = pinned_blob_cv
    say(f"      WHAT THIS ANCHOR PROVES, AND WHAT IT DOES NOT [LEAN R10]")
    say(f"        PROVES   {LEDGER_REL} is TRACKED, so an answer to 'what does the "
        f"record say' exists OUTSIDE the working tree; the {PINNED_LEDGER_REV} blob "
        f"still hashes to a literal typed in this module, so a rewritten history is "
        f"caught; and a COMPLETE-VERIFIED block cannot be BORN, PROMOTED, EDITED, "
        f"DEMOTED or DELETED by a working-tree edit — all of those are planted in "
        f"the break leg and every one of them is RED.")
    say(f"        CANNOT   judge a stage that is COMPLETE-VERIFIED on NEITHER side: "
        f"{n_free} stage(s) are free to move on disk and this leg says nothing about "
        f"them (leg 1 does not hash them either — that is the cost of letting the "
        f"build advance).")
    say(f"        CANNOT   judge a COMMIT. {len(pin_cv)} stage(s) were "
        f"COMPLETE-VERIFIED at the pinned rev and are anchored to a sha a later "
        f"commit cannot move; the other {n_head_cv - len(pin_cv)} COMPLETE-VERIFIED "
        f"stage(s) at HEAD are witnessed by HEAD alone, so for them this leg proves "
        f"only that the working tree has not departed from the commit. The honesty "
        f"of the COMMIT ITSELF rests on review, not on this fixture.")
    say(f"        CANNOT   prove the ledger DESCRIBES THE WORLD. That the recorded "
        f"sha is the artifact's real sha is F-C10-RESUME-1's job, on disk; this leg "
        f"only proves the RECORD did not move.")
    say(f"        CANNOT   defend itself against an edit to THIS FILE. The pin and "
        f"the three loops live here; whoever may rewrite scripts/"
        f"tierc10_resume_fixtures.py may weaken them, and only the commit record "
        f"and a reader can catch that.")
    ok = not bad
    return ok, (f"the ledger is anchored OUTSIDE itself, BOTH WAYS: {LEDGER_REL} is "
                f"TRACKED, its {PINNED_LEDGER_REV} blob hashes to the module literal "
                f"{PINNED_LEDGER_SHA[:16]}…, every one of the {n_cv} stage(s) the "
                f"working tree calls COMPLETE-VERIFIED is COMPLETE-VERIFIED at HEAD "
                f"with a BYTE-IDENTICAL block, every one of the {n_head_cv} stage(s) "
                f"HEAD calls COMPLETE-VERIFIED is still present and still "
                f"COMPLETE-VERIFIED in the working tree (so a settled claim cannot be "
                f"quietly WITHDRAWN either), and every stage the pinned rev called "
                f"COMPLETE-VERIFIED still is; {n_free} non-complete stage(s) are free "
                f"to move in the working tree"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═══════════════════════════════ F-C10-RESUME-1 · the re-hash and the sweep
def rehash_findings(recorded: dict, base: Path,
                    quars: list[Path], tc_rel: str = "research_outputs/tierc10",
                    redirects: list | None = None) -> list[str]:
    """Re-hash every recorded artifact under `base`. A recorded path that is
    absent is resolved against the LAW-2 quarantine dirs at the IDENTICAL
    relative subpath, and ONLY if the quarantined bytes hash to the RECORDED
    sha — a redirect that cannot launder a tamper. Absence is a finding:
    silence must not read as health."""
    bad: list[str] = []
    for rel in sorted(recorded):
        rec = recorded[rel]
        p = base / rel
        tag = ""
        if not p.exists():
            sub = rel[len(tc_rel) + 1:] if rel.startswith(tc_rel + "/") else None
            found = None
            for q in quars:
                cand = q / sub if sub else None
                if cand is not None and cand.exists():
                    h, n = file_sha(cand)
                    if h == rec["sha256"]:
                        found, tag = cand, f" [redirected to {q.name}/{sub}]"
                        if redirects is not None:
                            redirects.append(f"{rel} -> {q.name}/{sub}")
                        break
                    bad.append(f"{rel}: found in quarantine {q.name} but its bytes "
                               f"do NOT match the recorded sha "
                               f"({rec['sha256'][:12]}… vs {h[:12]}…, {n:,} B) — "
                               f"a redirect may not launder a tamper")
                    found = "poisoned"
                    break
            if found is None:
                bad.append(f"{rel}: ABSENT — recorded by the ledger, on disk nowhere "
                           f"(not at its path, not in {len(quars)} quarantine dir(s)); "
                           f"silence is not health")
                continue
            if found == "poisoned":
                continue
            p = found
        h, n = file_sha(p)
        if h != rec["sha256"]:
            bad.append(f"{rel}: CONTENT SHA MOVED{tag} — ledger {rec['sha256'][:16]}… "
                       f"re-hashes {h[:16]}…")
        elif n != rec["bytes"]:
            bad.append(f"{rel}: BYTE COUNT MOVED{tag} — ledger {rec['bytes']:,} B, "
                       f"on disk {n:,} B")
    return bad


def sweep_findings(recorded: dict, root: Path, root_rel: str,
                   base: Path) -> list[str]:
    """Every file inside a completed stage's own directory must be recorded.
    An unrecorded artifact is as bad as a moved one."""
    if not root.exists():
        return [f"{root_rel}: the stage directory does not exist"]
    on_disk = sorted(str(f.relative_to(base)).replace(os.sep, "/")
                     for f in root.rglob("*") if f.is_file())
    extra = [f for f in on_disk if f not in recorded]
    return [f"{root_rel}: {len(extra)} file(s) on disk that the ledger does NOT "
            f"record: {extra[:4]}"] if extra else []


def root_sweep_findings(loose: list[str], all_recorded: set[str],
                        allow: tuple = TC_ROOT_ALLOWLIST,
                        tc_rel: str = "research_outputs/tierc10") -> list[str]:
    """THE TIERC10 ROOT ITSELF.  STEP 0's own directory IS this root and is
    SWEEP EXEMPT [LEAN R3], and a PARTIAL stage is never swept — so a file
    dropped straight into research_outputs/tierc10 was invisible to every
    guard here, this track's own artifacts included.  Swept NON-RECURSIVELY
    (the sub-directories belong to their stages) against the UNION of every
    recorded artifact of EVERY stage plus a NAMED allowlist.  [LEAN R7]"""
    extra = sorted(n for n in loose
                   if f"{tc_rel}/{n}" not in all_recorded and n not in allow)
    return [f"{tc_rel} (root, non-recursive): {len(extra)} loose file(s) that NO "
            f"stage records and the named allowlist does not carry: {extra} — a "
            f"file nobody recorded is a file nobody will re-hash"] if extra else []


class _StageCopy:
    """A COPY of a handful of a real stage's recorded artifacts, in a throwaway
    tree laid out exactly as the repo is. Break legs sabotage the COPY; no file
    of the repo is ever written."""

    def __init__(self, recorded: dict, n: int = 3):
        self.pick = dict(sorted(recorded.items(),
                                key=lambda kv: (kv[1]["bytes"], kv[0]))[:n])
        self.dir = Path(tempfile.mkdtemp(prefix="tc10_resume_"))
        for rel in self.pick:
            src = ROOT / rel
            dst = self.dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(src, dst)

    def run(self) -> list[str]:
        root_rel = stage_root(self.pick)
        return (rehash_findings(self.pick, self.dir, [])
                + sweep_findings(self.pick, self.dir / root_rel, root_rel, self.dir))

    def close(self) -> None:
        shutil.rmtree(self.dir, ignore_errors=True)


def _copy_plant(recorded: dict, mutate) -> list[str]:
    c = _StageCopy(recorded)
    try:
        mutate(c)
        return c.run()
    finally:
        c.close()


def _complete_stages(prog: dict) -> list[dict]:
    return [s for s in prog["stages"] if s.get("status") == "COMPLETE-VERIFIED"]


def resume1_break():
    prog = load_progress()
    st = next(s for s in _complete_stages(prog) if s["stage"] == "A (stamps)")
    rec = st["artifact_shas"]

    def flip(c: _StageCopy):
        rel = sorted(c.pick)[0]
        p = c.dir / rel
        b = bytearray(p.read_bytes())
        b[len(b) // 2] ^= 0x01               # ONE bit, in a COPY
        p.write_bytes(bytes(b))

    def remove(c: _StageCopy):
        (c.dir / sorted(c.pick)[0]).unlink()

    def intrude(c: _StageCopy):
        root = c.dir / stage_root(c.pick)
        (root / "UNRECORDED_INTRUDER.parquet").write_bytes(b"not in the ledger")

    # fourth plant: the quarantine redirect must not launder a tampered file
    def laundered() -> list[str]:
        q = Path(tempfile.mkdtemp(prefix="tc10_resume_q_"))
        try:
            sub = "panel/FIXTURES_PANEL_partial.txt"
            real = TC / quarantine_dirs()[0].name / sub
            dst = q / "_partial_FAKE" / sub
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(real.read_bytes() + b"\n")      # tampered COPY
            rel = f"research_outputs/tierc10/{sub}"
            recorded = {rel: {"sha256": QUARANTINED_PARTIALS[sub],
                              "bytes": real.stat().st_size}}
            return rehash_findings(recorded, q, [q / "_partial_FAKE"])
        finally:
            shutil.rmtree(q, ignore_errors=True)

    return plants([
        ("BYTE FLIP (one bit in a COPY of the smallest recorded Stage A artifact)",
         lambda: _copy_plant(rec, flip)),
        ("DELETE (a recorded artifact removed from the COPY — silence is not health)",
         lambda: _copy_plant(rec, remove)),
        ("UNRECORDED EXTRA (a file added to the COPY's stage directory)",
         lambda: _copy_plant(rec, intrude)),
        ("LAUNDERED REDIRECT (a tampered COPY of a quarantined partial, offered "
         "to the quarantine resolver)", laundered),
        ("LOOSE FILE IN THE TIERC10 ROOT (an unrecorded, un-allowlisted file "
         "dropped straight into research_outputs/tierc10) [LEAN R7]",
         lambda: root_sweep_findings(
             sorted(p.name for p in TC.iterdir() if p.is_file())
             + ["UNRECORDED_ROOT_INTRUDER.json"],
             {rel for st in load_progress()["stages"] for rel in st["artifact_shas"]})),
    ])


def resume1_real():
    prog = load_progress()
    quars = quarantine_dirs()
    bad: list[str] = []
    redirects: list[str] = []
    n_art = n_bytes = 0
    swept = 0
    say(f"      LAW-2 quarantine dir(s): "
        f"{[q.name for q in quars] if quars else 'none'}")
    for st in _complete_stages(prog):
        rec = st["artifact_shas"]
        root_rel = stage_root(rec)
        bad += rehash_findings(rec, ROOT, quars, redirects=redirects)
        if root_rel == "research_outputs/tierc10":
            sweep = ("SWEEP EXEMPT — the stage's own directory IS the tierc10 root, "
                     "shared by every stage [LEAN R3]")
        else:
            f = sweep_findings(rec, ROOT / root_rel, root_rel, ROOT)
            bad += f
            swept += 1
            n_disk = sum(1 for p in (ROOT / root_rel).rglob("*") if p.is_file())
            sweep = f"swept, {n_disk:,} file(s) on disk, all recorded" if not f else f[0]
        n_art += len(rec)
        n_bytes += sum(r["bytes"] for r in rec.values())
        say(f"      {st['stage']:<18} {len(rec):>4} artifact(s)  "
            f"{sum(r['bytes'] for r in rec.values()):>12,} B  root {root_rel}")
        say(f"        {sweep}")
    all_recorded = {rel for st in prog["stages"] for rel in st["artifact_shas"]}
    loose = sorted(p.name for p in TC.iterdir() if p.is_file())
    rootbad = root_sweep_findings(loose, all_recorded)
    bad += rootbad
    say(f"      tierc10 ROOT swept NON-RECURSIVELY [LEAN R7] against "
        f"{len(all_recorded):,} recorded artifact(s) of ALL "
        f"{len(prog['stages'])} stage(s) + allowlist {list(TC_ROOT_ALLOWLIST)}")
    say(f"        {rootbad[0] if rootbad else 'every loose file accounted for'}")
    # the LOOSE-FILE COUNT is a live number this module's own _rerun.txt
    # byproduct changes, so it is stdout only [LEAN R8]; what the transcript
    # carries is the VERDICT and the allowlist, both pinned
    clock(f"        [stdout only, live count] {len(loose)} loose file(s): {loose}")
    for r in sorted(redirects):
        say(f"      REDIRECT [LEAN R2]: {r}")
    # the harness must be able to read GREEN as well as RED: the unsabotaged copy.
    # The stage is named, with a DETERMINISTIC fallback — the hard-coded next()
    # raised StopIteration on any ledger that no longer carries 'A (stamps)' as
    # COMPLETE-VERIFIED, which is exactly the ledger F-C10-RESUME-0's new
    # withdrawal plants produce. It failed CLOSED (prove() reads a raise as a
    # FAIL), so it was never a false green — but a control that cannot run tells
    # a reader nothing, and a FINDING says more than a traceback.
    cvs = {s["stage"]: s for s in _complete_stages(prog)}
    pick_name = ("A (stamps)" if "A (stamps)" in cvs
                 else (sorted(cvs, key=str)[0] if cvs else None))
    if pick_name is None:
        bad.append("CONTROL: the ledger carries NO COMPLETE-VERIFIED stage at all, "
                   "so the unsabotaged-copy control cannot run — this leg can show "
                   "RED but has not been shown able to show GREEN")
        return (not bad), (f"{len(bad)} finding(s): " + " · ".join(bad[:4]))
    ctrl = _StageCopy(cvs[pick_name]["artifact_shas"])
    try:
        ctrl_bad = ctrl.run()
    finally:
        ctrl.close()
    if ctrl_bad:
        bad.append(f"CONTROL: an UNSABOTAGED copy yielded findings {ctrl_bad[:2]} — "
                   f"the checker is red on everything and proves nothing")
    ok = not bad
    n_complete = len(_complete_stages(prog))
    return ok, (f"{n_art:,} recorded artifact content-sha(s) across {n_complete} "
                f"COMPLETE-VERIFIED stage(s) re-hashed, every one a MATCH "
                f"({n_bytes:,} B total); {swept} stage directory/ies swept for "
                f"unrecorded files, 0 found; the tierc10 ROOT swept "
                f"non-recursively, 0 loose file(s) unaccounted; "
                f"{len(redirects)} LAW-2 quarantine "
                f"redirect(s), each sha-proven; control copy clean"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ══════════════════════════════════ F-C10-RESUME-2 · a tampered partial FAILS
def partial_findings(base_q: Path, expect: dict) -> list[str]:
    bad = []
    for sub in sorted(expect):
        p = base_q / sub
        if not p.exists():
            bad.append(f"{sub}: ABSENT from the quarantine — a kill-partial may be "
                       f"moved, never deleted (LAW 2)")
            continue
        h, n = file_sha(p)
        if h != expect[sub]:
            bad.append(f"{sub}: TAMPERED — expected {expect[sub][:16]}…, "
                       f"re-hashes {h[:16]}… ({n:,} B)")
    return bad


def resume2_break():
    real_q = quarantine_dirs()[0]

    def copy_q() -> Path:
        d = Path(tempfile.mkdtemp(prefix="tc10_resume_p_"))
        for sub in QUARANTINED_PARTIALS:
            dst = d / sub
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(real_q / sub, dst)
        return d

    def append_byte() -> list[str]:
        d = copy_q()
        try:
            p = d / "lanes/FIXTURES_LANES_partial.txt"
            p.write_bytes(p.read_bytes() + b"\n")
            return partial_findings(d, QUARANTINED_PARTIALS)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def swap() -> list[str]:
        d = copy_q()
        try:
            a, b = (d / "lanes/FIXTURES_LANES_partial.txt",
                    d / "panel/FIXTURES_PANEL_partial.txt")
            ab, bb = a.read_bytes(), b.read_bytes()
            a.write_bytes(bb)
            b.write_bytes(ab)
            return partial_findings(d, QUARANTINED_PARTIALS)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def delete() -> list[str]:
        d = copy_q()
        try:
            (d / "panel/FIXTURES_PANEL_partial.txt").unlink()
            return partial_findings(d, QUARANTINED_PARTIALS)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def truncate() -> list[str]:
        d = copy_q()
        try:
            p = d / "panel/FIXTURES_PANEL_partial.txt"
            p.write_bytes(p.read_bytes()[:-1])
            return partial_findings(d, QUARANTINED_PARTIALS)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    return plants([
        ("APPEND ONE BYTE to a COPY of lanes/FIXTURES_LANES_partial.txt", append_byte),
        ("SWAP the two quarantined partials in a COPY", swap),
        ("DELETE a quarantined partial from the COPY", delete),
        ("TRUNCATE one byte from a COPY of panel/FIXTURES_PANEL_partial.txt", truncate),
    ])


def resume2_real():
    quars = quarantine_dirs()
    if not quars:
        return False, "no LAW-2 quarantine directory exists under research_outputs/tierc10"
    q = quars[0]
    bad = partial_findings(q, QUARANTINED_PARTIALS)
    # three-way: the literal typed HERE == the bytes on disk == the ledger's record
    prog = load_progress()
    ledger = {}
    for st in prog["stages"]:
        for rel, rec in st["artifact_shas"].items():
            pre = "research_outputs/tierc10/"
            if rel.startswith(pre) and rel[len(pre):] in QUARANTINED_PARTIALS:
                ledger[rel[len(pre):]] = (st["stage"], rec["sha256"], rec["bytes"])
    for sub, want in sorted(QUARANTINED_PARTIALS.items()):
        if sub not in ledger:
            bad.append(f"{sub}: the ledger records no such artifact — a kill-partial "
                       f"outside the ledger is unaccounted for")
            continue
        stage, sha, nb = ledger[sub]
        h, n = file_sha(q / sub) if (q / sub).exists() else ("", -1)
        if sha != want:
            bad.append(f"{sub}: ledger sha {sha[:16]}… != the literal typed in this "
                       f"fixture {want[:16]}…")
        if n != nb:
            bad.append(f"{sub}: ledger {nb:,} B != on disk {n:,} B")
        say(f"      {sub}")
        say(f"        ledger  {stage:<18} {sha}  {nb:,} B")
        say(f"        on disk {q.name:<18} {h}  {n:,} B")
    readme = q / "README.md"
    if not readme.exists():
        bad.append(f"{q.name}/README.md absent — a quarantine with no note is a "
                   f"pile of files")
    else:
        txt = readme.read_text(encoding="utf-8")
        for sub in sorted(QUARANTINED_PARTIALS):
            if Path(sub).name not in txt:
                bad.append(f"{q.name}/README.md does not name {sub}")
    ok = not bad
    return ok, (f"{len(QUARANTINED_PARTIALS)} quarantined kill-partial(s) in "
                f"{q.name} re-hash to the shas typed here, and agree THREE WAYS "
                f"(fixture literal == disk bytes == PROGRESS.json record); the "
                f"quarantine README names both; the real quarantine was opened "
                f"read-only and never written"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═══════════════════════════════════════ F-C10-RESUME-3 · the corridor is one
def corridor_findings(prog: dict, man: dict, pin: dict) -> list[str]:
    bad = []
    trio = {
        "PROGRESS.json as_of_of_record": prog.get("as_of_of_record"),
        "STAGE_D_MANIFEST.json as_of_last_closed_4h": man.get("as_of_last_closed_4h"),
        "AS_OF_PIN.json as_of_last_closed_4h": pin.get("as_of_last_closed_4h"),
    }
    for k, v in sorted(trio.items()):
        if v != AS_OF:
            bad.append(f"{k} = {v!r}, not {AS_OF} — THE CORRIDOR MOVED")
    ms = {
        "PROGRESS.json as_of_last_closed_4h_close_ms":
            prog.get("as_of_last_closed_4h_close_ms"),
        "STAGE_D_MANIFEST.json as_of_last_closed_4h_close_ms":
            man.get("as_of_last_closed_4h_close_ms"),
        "AS_OF_PIN.json as_of_last_closed_4h_close_ms":
            pin.get("as_of_last_closed_4h_close_ms"),
    }
    for k, v in sorted(ms.items()):
        if v != CLOSE_MS:
            bad.append(f"{k} = {v!r}, not {CLOSE_MS}")
    for s in prog.get("stages", []):
        if s.get("as_of") != AS_OF:
            bad.append(f"stage {s.get('stage')!r} is stamped {s.get('as_of')!r}, "
                       f"not {AS_OF} — a stage outside the corridor")
    for k, want in (("seed", SEED), ("live_cache_touched", False)):
        if prog.get(k) != want:
            bad.append(f"PROGRESS.json {k} = {prog.get(k)!r}, not {want!r}")
    if man.get("snapshot_root") != str(Path.home() / ".cache/naiad/snapshots/tc10_20260921"):
        bad.append(f"Stage D manifest snapshot_root = {man.get('snapshot_root')!r} "
                   f"— the substrate moved")
    return bad


def _corridor_inputs() -> tuple[dict, dict, dict]:
    man = json.loads((TC / "data" / "STAGE_D_MANIFEST.json").read_text(encoding="utf-8"))
    pin = json.loads((TC / "data" / "AS_OF_PIN.json").read_text(encoding="utf-8"))
    return load_progress(), man, pin


def resume3_break():
    prog, man, pin = _corridor_inputs()

    def restamp():
        p = copy.deepcopy(prog)
        p["stages"][3]["as_of"] = "2026-09-22T00:00:00Z"
        return corridor_findings(p, man, pin)

    def move_manifest():
        return corridor_findings(prog, dict(man, as_of_last_closed_4h="2026-09-21T20:00:00Z"), pin)

    def shift_ms():
        return corridor_findings(prog, man, dict(pin, as_of_last_closed_4h_close_ms=CLOSE_MS + 14_400_000))

    def strip_as_of():
        p = copy.deepcopy(prog)
        del p["stages"][0]["as_of"]
        return corridor_findings(p, man, pin)

    def touched_cache():
        return corridor_findings(dict(prog, live_cache_touched=True), man, pin)

    def move_substrate():
        return corridor_findings(prog, dict(man, snapshot_root="/Users/luis/.cache/naiad/data_cache"), pin)

    return plants([
        ("RE-STAMPED STAGE (stages[3].as_of -> 2026-09-22T00:00:00Z, in a deep COPY)", restamp),
        ("MOVED MANIFEST (Stage D as_of_last_closed_4h -> 2026-09-21T20:00:00Z)", move_manifest),
        ("SHIFTED close_ms (AS_OF_PIN + one 4h bar)", shift_ms),
        ("STRIPPED as_of (stages[0] loses the field entirely — absence is not agreement)", strip_as_of),
        ("TOUCHED LIVE CACHE (live_cache_touched -> True)", touched_cache),
        ("MOVED SUBSTRATE (snapshot_root -> the LIVE cache)", move_substrate),
    ])


def resume3_real():
    prog, man, pin = _corridor_inputs()
    bad = corridor_findings(prog, man, pin)
    say(f"      PROGRESS.json        as_of_of_record        {prog.get('as_of_of_record')}")
    say(f"      STAGE_D_MANIFEST.json as_of_last_closed_4h  {man.get('as_of_last_closed_4h')}")
    say(f"      AS_OF_PIN.json        as_of_last_closed_4h  {pin.get('as_of_last_closed_4h')}")
    say(f"      close_ms, all three                         "
        f"{prog.get('as_of_last_closed_4h_close_ms')} / "
        f"{man.get('as_of_last_closed_4h_close_ms')} / "
        f"{pin.get('as_of_last_closed_4h_close_ms')}")
    say(f"      substrate                                   {man.get('snapshot_root')}")
    n = len(prog.get("stages", []))
    ok = not bad
    return ok, (f"the corridor is ONE: three independent files agree on "
                f"{AS_OF} and close_ms {CLOSE_MS}, and all {n} stage record(s) "
                f"carry the same as_of; seed {SEED}; live cache untouched; "
                f"substrate the frozen snapshot"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═════════════════════════ F-C10-RESUME-4 · the exemption is named, not silent
def _suite_net_legs(src: str) -> tuple[set[str], dict[str, bool], str | None]:
    """The exempted suite's OWN declaration of which legs reach the venue —
    parsed from its LEGS table, never a list this fixture chose.

    HARDENED: it used to RAISE on any LEGS table that is not a tuple of literal
    rows (scripts/tierc10_lanes_fixtures.py's `LEGS = (f_lanes_off, …)` raises
    AttributeError: 'Name' object has no attribute 'elts'), and a raise inside a
    break leg was swallowed as a "catch". A suite whose venue declaration cannot
    be READ must be an explicit FINDING for that exemption, never a pass and
    never a traceback."""
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return set(), {}, f"the suite will not parse: SyntaxError {e}"
    table: dict[str, bool] = {}
    seen = False
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Assign) and any(
                getattr(t, "id", "") == "LEGS" for t in node.targets)):
            continue
        seen = True
        elts = getattr(node.value, "elts", None)
        if elts is None:
            return set(), {}, (f"its LEGS is a {type(node.value).__name__}, not a "
                               f"literal table this parser can read")
        for el in elts:
            sub = getattr(el, "elts", None)
            if not sub:
                return set(), {}, (f"a LEGS row is a {type(el).__name__}, not a "
                                   f"literal row — no venue flag can be read from it")
            try:
                name = ast.literal_eval(sub[0])
            except Exception:
                return set(), {}, "a LEGS row's leg name is not a literal"
            flag = False
            if len(sub) > 4:
                try:
                    flag = bool(ast.literal_eval(sub[4]))
                except Exception:
                    return set(), {}, f"leg {name!r}'s venue flag is not a literal"
            table[str(name)] = flag
    if not seen:
        return set(), {}, "it declares no LEGS table at all"
    if not table:
        return set(), {}, "its LEGS table is empty"
    return {k for k, v in table.items() if v}, table, None


def _pairs_from_strings(lines, match: str) -> tuple[dict | None, dict | None]:
    """The measured pair, RE-DERIVED out of whatever the evidence points at."""
    for line in lines:
        t = str(line)
        if match not in t:
            continue
        vals = []
        for d in re.findall(r"\{[^{}]*\}", t):
            try:
                v = ast.literal_eval(d)
            except Exception:
                continue
            if isinstance(v, dict) and "both" in v:
                vals.append(v)
        if len(vals) >= 2:
            return vals[0], vals[1]
    return None, None


def _walk_strings(obj) -> list[str]:
    out: list[str] = []
    if isinstance(obj, dict):
        for k in sorted(obj, key=str):
            out += _walk_strings(obj[k])
    elif isinstance(obj, list):
        for v in obj:
            out += _walk_strings(v)
    elif isinstance(obj, str):
        out.append(obj)
    return out


def _strings_at(doc, field: str, stage: str | None) -> list[str]:
    """The strings the named stage's named field holds — the narrow reading the
    evidence itself asks for, before any fallback."""
    out: list[str] = []
    if not isinstance(doc, dict) or not field:
        return out
    stages = doc.get("stages")
    if isinstance(stages, list) and stage:
        for st in stages:
            if isinstance(st, dict) and st.get("stage") == stage:
                v = st.get(field)
                if isinstance(v, list):
                    out += [str(i) for i in v]
                elif v is not None:
                    out.append(str(v))
        if out:
            return out
    v = doc.get(field)
    if isinstance(v, list):
        out += [str(i) for i in v]
    elif isinstance(v, str):
        out.append(v)
    return out


def evidence_findings(xid: str, ev: dict, root: Path = ROOT) -> list[str]:
    """CORROBORATION IS UNCONDITIONAL.

    THE HOLE THIS CLOSES.  The corroboration block used to be gated on
    `src["file"] == "research_outputs/tierc10/PROGRESS.json"`, the one file the
    checker knew how to open.  Change that ONE STRING to any other path and the
    entire evidence block — filed, remeasured, delta_bars — became unchecked
    prose: fabricated numbers, a delta of 99999, ZERO findings.  The escape also
    hid real failures, since a fabricated exemption over a PARTIAL stage could
    silently cover a genuine transcript drift.

    Now the named file is RESOLVED AND OPENED, whatever it is, and an exemption
    whose numbers cannot be RE-DERIVED off disk is a FINDING, never a pass.
    PROGRESS.json is one handler among several, not the gate."""
    bad: list[str] = []
    src = ev.get("source") or {}
    rel = str(src.get("file") or "")
    match = str(src.get("match") or "")
    if not rel:
        return [f"{xid}: evidence.source.file is empty — evidence a reader cannot "
                f"chase is not evidence"]
    if not match:
        return [f"{xid}: evidence.source.match is empty — there is nothing to look "
                f"for in {rel}, so nothing can corroborate anything"]
    p = root / rel
    if not p.exists() or not p.is_file():
        return [f"{xid}: evidence.source.file {rel!r} DOES NOT EXIST on disk — an "
                f"exemption whose evidence cannot even be opened is an assertion"]
    raw = p.read_bytes()
    if p.suffix == ".json":
        try:
            doc = json.loads(raw.decode("utf-8"))
        except Exception as e:
            return [f"{xid}: evidence.source.file {rel!r} will not parse as JSON "
                    f"({e.__class__.__name__}) — the pair cannot be re-derived"]
        lines = _strings_at(doc, str(src.get("field") or ""), src.get("stage"))
        handler = f"json[{src.get('stage')}].{src.get('field')}"
        if not lines:
            lines = _walk_strings(doc)
            handler = "json, WHOLE DOCUMENT (the named stage/field held nothing)"
    else:
        lines = raw.decode("utf-8", errors="replace").splitlines()
        handler = f"text, {p.suffix or 'no-suffix'}"
    filed, remeas = _pairs_from_strings(lines, match)
    if filed is None or remeas is None:
        return [f"{xid}: evidence.source names {rel} [{src.get('stage')}]."
                f"{src.get('field')} / {match!r} but NO measured pair can be "
                f"RE-DERIVED there ({handler}, {len(lines):,} string(s) searched, "
                f"{len(raw):,} B) — unre-derivable evidence is not evidence"]
    if filed != ev.get("filed"):
        bad.append(f"{xid}: evidence.filed {ev.get('filed')} != the {rel} record's "
                   f"{filed}")
    if remeas != ev.get("remeasured"):
        bad.append(f"{xid}: evidence.remeasured {ev.get('remeasured')} != the {rel} "
                   f"record's {remeas}")
    if not bad:
        d = remeas.get("both", 0) - filed.get("both", 0)
        if d != ev.get("delta_bars"):
            bad.append(f"{xid}: evidence.delta_bars {ev.get('delta_bars')} != the "
                       f"measured {d} re-derived from {rel}")
    return bad


def _binding_field(stage: dict, srel: str) -> str | None:
    """WHICH FIELD of the stage's own ledger block names the exempted suite —
    the binding, printed by name so a reader can chase it. None = not bound."""
    stem = Path(srel).stem
    if not stem:
        return None
    for key in sorted(stage, key=str):
        if stem in _jb(stage[key]):
            return key
    return None


def exemption_findings(exemptions, prog: dict, root: Path = ROOT) -> list[str]:
    """THE SUITE IS READ PER EXEMPTION.

    THE HOLE THIS CLOSES.  resume4_real used to read ONE suite source —
    EXEMPTIONS[0]'s — and pass that single string in for ALL exemptions, so the
    "the exempted legs are EXACTLY the legs the suite itself declares
    venue-reaching" and "the suite really reaches a venue" checks were applied
    to the WRONG FILE for every exemption but the first.  A second exemption
    naming any other suite was a blanket escape: it was validated against
    EXEMPTIONS[0]'s LEGS table and its own file was never opened."""
    bad: list[str] = []
    seen = set()
    # an exemption may cover a drift ONLY IF IT IS ITSELF CLEAN. A defective
    # exemption that still silenced the thing it names would be the review's
    # cover-up with extra steps: red on its own fields, and the REAL failure
    # underneath it never spoken aloud.
    clean: set[str] = set()
    for x in exemptions:
        n0 = len(bad)
        xid = x.get("id") or "<unnamed exemption>"
        if xid in seen:
            bad.append(f"{xid}: duplicated exemption id")
        seen.add(xid)
        for field in ("id", "suite", "stage", "transcript", "covers_record_match",
                      "legs", "waives", "reason", "evidence", "ruling_status"):
            if not x.get(field):
                bad.append(f"{xid}: field {field!r} is empty or missing — AN UNNAMED "
                           f"EXEMPTION IS HOW A BUILD LAUNDERS A FAILURE")
        if len(str(x.get("reason", ""))) < 120:
            bad.append(f"{xid}: reason is {len(str(x.get('reason','')))} chars — a "
                       f"waiver needs a reason a reader can weigh, not a label")
        ev = x.get("evidence") or {}
        src = ev.get("source") or {}
        for field in ("filed", "remeasured", "delta_bars", "measured_on"):
            if ev.get(field) in (None, "", {}):
                bad.append(f"{xid}: evidence.{field} is empty — a waiver with no "
                           f"measured evidence is an assertion")
        for field in ("file", "stage", "field", "match"):
            if not src.get(field):
                bad.append(f"{xid}: evidence.source.{field} is empty — evidence a "
                           f"reader cannot chase is not evidence")
        # CORROBORATION, UNCONDITIONAL: the numbers must be RE-DERIVABLE off the
        # named on-disk record, WHATEVER that record is
        bad += evidence_findings(xid, ev, root)
        # THE EXEMPTED LEGS must be EXACTLY what THIS exemption's OWN suite
        # declares venue-reaching, read from THIS exemption's OWN file
        srel = str(x.get("suite") or "")
        if srel:
            sp = root / srel
            if not sp.exists() or not sp.is_file():
                bad.append(f"{xid}: its suite {srel!r} DOES NOT EXIST on disk — an "
                           f"exemption over nothing may not waive anything")
            else:
                ssrc = sp.read_text(encoding="utf-8", errors="replace")
                net, table, err = _suite_net_legs(ssrc)
                if err:
                    bad.append(f"{xid}: {srel} — {err}. A suite whose venue "
                               f"declaration cannot be READ may not be exempted on "
                               f"its own word")
                else:
                    if set(x.get("legs", ())) != net:
                        bad.append(f"{xid}: exempted legs {sorted(x.get('legs', ()))} "
                                   f"!= the legs {srel} ITSELF declares "
                                   f"venue-reaching {sorted(net)}")
                    for leg in x.get("legs", ()):
                        if leg not in table:
                            bad.append(f"{xid}: exempted leg {leg!r} does not exist "
                                       f"in {srel}")
                    for leg in x.get("conditional_legs", ()):
                        if leg not in table:
                            bad.append(f"{xid}: conditional leg {leg!r} does not "
                                       f"exist in {srel}")
                # the exempted suite must REALLY reach a venue, or there is no
                # ground for a waiver — checked for THIS suite, not for the first
                if "import requests" not in ssrc:
                    bad.append(f"{xid}: {srel} does not import requests — it reaches "
                               f"NO venue and needs no exemption")
        # the named stage must exist, and the match patterns must be live
        stage = next((s for s in prog["stages"] if s.get("stage") == x.get("stage")), None)
        if x.get("stage") and stage is None:
            bad.append(f"{xid}: names stage {x.get('stage')!r}, which the ledger does "
                       f"not carry — an exemption over nothing")
        elif stage is not None:
            suites = [str(f.get("suite", "")) for f in stage.get("fixtures", [])]
            for pat in x.get("covers_record_match", ()):
                if not any(pat in s for s in suites):
                    bad.append(f"{xid}: covers_record_match {pat!r} matches none of "
                               f"stage {x['stage']!r}'s {len(suites)} fixture record(s) "
                               f"— a dead pattern covers nothing and hides everything")
            # ── THE SUITE IS BOUND TO THE STAGE IT EXEMPTS [LEAN R11] ──
            # THE HOLE THIS CLOSES. Everything above validates the exemption's
            # OWN suite — its LEGS table, its venue client, its evidence — and
            # NOTHING tied x['suite'] to x['stage'] or to the records
            # x['covers_record_match'] selects. `suite` and `stage` were
            # unrelated free strings. A review beat it in one move: copy
            # X-STAGE-D-VENUE VERBATIM — same real, parseable, venue-reaching
            # scripts/tierc10_data_fixtures.py, same corroborated evidence —
            # change only the id, the stage and covers_record_match, and a REAL
            # planted drift on LANES went from 1 finding to ZERO. Every hardened
            # check passed because every one of them aimed at the BORROWED
            # suite. It worked for LANES, BRK, D-CORE and CENSUS-R.
            # THE FIX. The ledger already carries the binding: each stage's own
            # block names the suite that produced its records. Demand it.
            if srel and _binding_field(stage, srel) is None:
                bad.append(f"{xid}: stage {x['stage']!r}'s ledger block does not name "
                           f"the exempted suite {Path(srel).stem!r} — this exemption "
                           f"was validated against a suite that did not produce the "
                           f"records it covers. A waiver borrowed from another "
                           f"stage's suite is a BLANKET ESCAPE: everything checkable "
                           f"about it is checkable about the WRONG FILE")
            # an exemption may never be what makes a stage COMPLETE
            if stage.get("status") == "COMPLETE-VERIFIED":
                bad.append(f"{xid}: stage {stage['stage']!r} is COMPLETE-VERIFIED while "
                           f"an exemption stands over it — an exemption may not be what "
                           f"completes a stage")
        if len(bad) == n0:
            clean.add(id(x))
    # CLOSURE: nothing may drift outside the registry
    for s in prog["stages"]:
        for f in s.get("fixtures", []):
            drifted = bool(f.get("transcript_drift")) or (
                f.get("transcript_sha_before") != f.get("transcript_sha_after"))
            if not drifted:
                continue
            covered = any(
                id(x) in clean
                and x.get("stage") == s.get("stage")
                and any(p in str(f.get("suite", "")) for p in x.get("covers_record_match", ()))
                for x in exemptions)
            if not covered:
                dirty = any(
                    id(x) not in clean
                    and x.get("stage") == s.get("stage")
                    and any(p in str(f.get("suite", ""))
                            for p in x.get("covers_record_match", ()))
                    for x in exemptions)
                bad.append(f"stage {s['stage']!r} fixture {str(f.get('suite'))[:48]!r} "
                           f"DRIFTED between runs and "
                           + ("the only exemption naming it is ITSELF DEFECTIVE — a "
                              "waiver that cannot stand may not silence the failure "
                              "it names" if dirty else
                              "no exemption names it — an unnamed exemption is how a "
                              "build launders a failure"))
    return bad


def resume4_break():
    prog = load_progress()

    def mut(**kw):
        x = copy.deepcopy(EXEMPTIONS[0])
        x.update(kw)
        return (x,)

    def no_reason():
        return exemption_findings(mut(reason=""), prog)

    def no_source():
        x = copy.deepcopy(EXEMPTIONS[0])
        x["evidence"]["source"] = {"file": "", "stage": "", "field": "", "match": ""}
        return exemption_findings((x,), prog)

    def bent_number():
        x = copy.deepcopy(EXEMPTIONS[0])
        x["evidence"]["remeasured"]["both"] = 222
        return exemption_findings((x,), prog)

    def bent_number_redirected():
        """THE REVIEW'S ESCAPE: bend the number AND redirect source.file away
        from PROGRESS.json. Under the old one-line gate this was GREEN."""
        x = copy.deepcopy(EXEMPTIONS[0])
        x["evidence"]["filed"] = {"archive-only": 9, "both": 9, "rest": 9, "rest-only": 9}
        x["evidence"]["remeasured"] = {"archive-only": 1, "both": 2, "rest": 3,
                                       "rest-only": 4}
        x["evidence"]["delta_bars"] = 99999
        x["evidence"]["source"]["file"] = \
            "research_outputs/tierc10/data/STAGE_D_MANIFEST.json"
        return exemption_findings((x,), prog)

    def ghost_evidence_file():
        x = copy.deepcopy(EXEMPTIONS[0])
        x["evidence"]["source"]["file"] = "research_outputs/tierc10/lanes/ANY.txt"
        return exemption_findings((x,), prog)

    def unrederivable_evidence():
        x = copy.deepcopy(EXEMPTIONS[0])
        x["evidence"]["source"]["match"] = "A SENTENCE NOBODY EVER WROTE"
        return exemption_findings((x,), prog)

    def ghost_leg():
        return exemption_findings(mut(legs=("F-D-1", "F-D-1b", "F-D-99")), prog)

    def over_broad():
        return exemption_findings(mut(legs=("F-D-1", "F-D-1b", "F-D-SEAL")), prog)

    def unexempted_drift():
        p = copy.deepcopy(prog)
        p["stages"][5]["fixtures"][0]["transcript_drift"] = True
        return exemption_findings(EXEMPTIONS, p)

    def promoted_stage():
        p = copy.deepcopy(prog)
        for s in p["stages"]:
            if s["stage"] == "D-CORE":
                s["status"] = "COMPLETE-VERIFIED"
        return exemption_findings(EXEMPTIONS, p)

    def label_not_reason():
        return exemption_findings(mut(reason="venue"), prog)

    def ghost_stage():
        return exemption_findings(mut(stage="STAGE Z"), prog)

    def dead_pattern():
        return exemption_findings(mut(covers_record_match=("a suite nobody ran",)),
                                  prog)

    def _fabricated(stage_name: str, suite_rel: str, src_file: str) -> dict:
        return {
            "id": "X-FABRICATED", "suite": suite_rel, "stage": stage_name,
            "transcript": "research_outputs/tierc10/lanes/ANY.txt",
            "covers_record_match": ("tierc10_lanes_fixtures",),
            "legs": ("F-D-1", "F-D-1b"),
            "waives": "everything anybody might ask about",
            "reason": ("a reason long enough to clear the 120-character floor and "
                       "say precisely nothing that a reader could ever weigh, which "
                       "is exactly what a blanket escape looks like in the wild."),
            "ruling_status": "UNRULED",
            "evidence": {"filed": {"both": 1}, "remeasured": {"both": 1},
                         "delta_bars": 0, "measured_on": "never",
                         "source": {"file": src_file, "stage": stage_name,
                                    "field": "blockers", "match": "q"}},
        }

    def second_suite_blanket():
        """THE REVIEW'S BLANKET ESCAPE: a SECOND exemption naming a DIFFERENT
        suite. It used to be judged against EXEMPTIONS[0]'s source string and
        its own file was never opened."""
        y = _fabricated("LANES (B mech)", "scripts/tierc10_lanes_fixtures.py",
                        "research_outputs/tierc10/lanes/ANY.txt")
        return exemption_findings((EXEMPTIONS[0], y), prog)

    def defective_exemption_cannot_cover():
        """THE REVIEW'S COVER-UP, judged ONLY on the covered failure: a REAL
        drift on a PARTIAL stage under a FABRICATED exemption. This thunk
        returns the DRIFT findings alone, so it goes red only if the real
        failure is still SPOKEN ALOUD beneath the defective waiver."""
        p = copy.deepcopy(prog)
        for st in p["stages"]:
            if st["stage"] == "LANES (B mech)" and st["fixtures"]:
                st["fixtures"][0]["transcript_drift"] = True
        y = _fabricated("LANES (B mech)", "scripts/tierc10_lanes_fixtures.py",
                        "research_outputs/tierc10/lanes/ANY.txt")
        return [q for q in exemption_findings((EXEMPTIONS[0], y), p) if "DRIFTED" in q]

    def covered_real_drift():
        """THE REVIEW'S COVER-UP: plant a REAL drift on a PARTIAL stage, then
        fabricate an exemption over it whose source.file points anywhere but
        PROGRESS.json. It used to silence the drift completely."""
        p = copy.deepcopy(prog)
        for st in p["stages"]:
            if st["stage"] == "LANES (B mech)" and st["fixtures"]:
                st["fixtures"][0]["transcript_drift"] = True
        y = _fabricated("LANES (B mech)", "scripts/tierc10_lanes_fixtures.py",
                        "research_outputs/tierc10/lanes/ANY.txt")
        return exemption_findings((EXEMPTIONS[0], y), p)

    def _borrowed() -> tuple[tuple, dict]:
        """THE REVIEW'S SECOND ESCAPE, BUILT EXACTLY AS THE REVIEW BUILT IT: a
        VERBATIM COPY of the real X-STAGE-D-VENUE — the same real, parseable,
        venue-reaching suite, the same corroborated evidence, the same reason —
        with ONLY the id, the stage, the transcript and covers_record_match
        changed, standing over a REAL planted drift on LANES. Every hardened
        check in this leg passes, because every one of them aims at the
        BORROWED suite. Nothing but the suite-to-stage binding catches it."""
        y = copy.deepcopy(EXEMPTIONS[0])
        y["id"] = "X-LANES-BORROWED"
        y["stage"] = "LANES (B mech)"
        y["transcript"] = "research_outputs/tierc10/lanes/FIXTURES_LANES.txt"
        y["covers_record_match"] = ("tierc10_lanes_fixtures",)
        q = copy.deepcopy(prog)
        for st in q["stages"]:
            if st["stage"] == "LANES (B mech)" and st["fixtures"]:
                st["fixtures"][0]["transcript_drift"] = True
        return (EXEMPTIONS[0], y), q

    def borrowed_suite():
        xs, q = _borrowed()
        return exemption_findings(xs, q)

    def borrowed_suite_binding_only():
        """Judged on the BINDING finding alone: the plant must go red FOR THE
        RIGHT REASON, not because some incidental field tripped."""
        xs, q = _borrowed()
        return [f for f in exemption_findings(xs, q)
                if "does not name the exempted suite" in f]

    def borrowed_suite_drift_only():
        """Judged on the COVERED FAILURE alone: the real drift underneath the
        borrowed waiver must still be SPOKEN ALOUD."""
        xs, q = _borrowed()
        return [f for f in exemption_findings(xs, q) if "DRIFTED" in f]

    def borrowed_suite_no_drift():
        """The same borrowed waiver with NOTHING to hide: the binding is a
        standing requirement, not a consequence of the drift."""
        xs, _ = _borrowed()
        return exemption_findings(xs, prog)

    return plants([
        ("GHOST STAGE (the exemption names a stage the ledger does not carry)", ghost_stage),
        ("DEAD PATTERN (covers_record_match matches no record of its own stage)",
         dead_pattern),
        ("EMPTY REASON (an exemption with no reason at all)", no_reason),
        ("LABEL, NOT A REASON (reason='venue' — 5 chars)", label_not_reason),
        ("SOURCELESS EVIDENCE (evidence.source blanked — unchaseable)", no_source),
        ("BENT NUMBER (evidence.remeasured both 223 -> 222, ledger untouched)", bent_number),
        ("GHOST LEG (exempting F-D-99, which does not exist in the suite)", ghost_leg),
        ("OVER-BROAD (exempting F-D-SEAL, which the suite declares OFFLINE-safe)", over_broad),
        ("UNEXEMPTED DRIFT (a stage's fixture record planted with transcript_drift=True)",
         unexempted_drift),
        ("PROMOTED STAGE (D-CORE flipped to COMPLETE-VERIFIED while its exemption stands)",
         promoted_stage),
        ("BENT NUMBER + REDIRECTED SOURCE (fabricated filed/remeasured/delta_bars "
         "AND source.file moved off PROGRESS.json — the review's one-line escape)",
         bent_number_redirected),
        ("GHOST EVIDENCE FILE (source.file names a path that does not exist)",
         ghost_evidence_file),
        ("UNRE-DERIVABLE EVIDENCE (source.match names a sentence the record does "
         "not contain)", unrederivable_evidence),
        ("BLANKET SECOND EXEMPTION (a 2nd exemption over a DIFFERENT suite — "
         "tierc10_lanes_fixtures.py, whose LEGS table this parser cannot read and "
         "which reaches no venue)", second_suite_blanket),
        ("A FABRICATED EXEMPTION COVERING A REAL DRIFT (the review's cover-up)",
         covered_real_drift),
        ("A DEFECTIVE EXEMPTION MAY NOT SILENCE THE DRIFT IT NAMES (the cover-up, "
         "judged on the COVERED failure alone — findings about the waiver's own "
         "fields are discarded)", defective_exemption_cannot_cover),
        ("BORROWED SUITE (the review's 2nd escape: a VERBATIM copy of the real "
         "exemption — same real, parseable, venue-reaching suite, same "
         "corroborated evidence — with only id/stage/transcript/covers changed, "
         "standing over a REAL planted drift)", borrowed_suite),
        ("BORROWED SUITE, JUDGED ON THE BINDING ALONE (it must go red because "
         "the stage's ledger block does not name the exempted suite, not for "
         "some incidental reason)", borrowed_suite_binding_only),
        ("BORROWED SUITE, JUDGED ON THE COVERED DRIFT ALONE (the real LANES "
         "drift underneath the borrowed waiver must still be spoken aloud)",
         borrowed_suite_drift_only),
        ("BORROWED SUITE WITH NOTHING TO HIDE (no drift planted — the binding is "
         "a standing requirement, not a consequence of the drift)",
         borrowed_suite_no_drift),
    ])


def resume4_real():
    prog = load_progress()
    bad = exemption_findings(EXEMPTIONS, prog)
    # NEGATIVE CONTROL: the waiver must actually COVER the thing it claims to.
    # Plant the drift the exemption exists for, on the record it names, and
    # demand SILENCE — a registry that fires on everything covers nothing.
    covered_probe = copy.deepcopy(prog)
    hit = 0
    for s in covered_probe["stages"]:
        if s["stage"] != EXEMPTIONS[0]["stage"]:
            continue
        for f in s["fixtures"]:
            if any(p in str(f.get("suite", "")) for p in EXEMPTIONS[0]["covers_record_match"]):
                f["transcript_drift"] = True
                f["transcript_sha_after"] = "0" * 64
                hit += 1
    if not hit:
        bad.append("CONTROL: the exemption's own record could not be found to plant "
                   "drift on — the registry points at nothing")
    else:
        ctrl = exemption_findings(EXEMPTIONS, covered_probe)
        if ctrl:
            bad.append(f"CONTROL: the exemption does NOT cover the drift it exists for "
                       f"— {ctrl[:2]}")
    n_fix = sum(len(s.get("fixtures", [])) for s in prog["stages"])
    n_drift = sum(1 for s in prog["stages"] for f in s.get("fixtures", [])
                  if f.get("transcript_drift")
                  or f.get("transcript_sha_before") != f.get("transcript_sha_after"))
    for x in EXEMPTIONS:
        srel = x["suite"]
        sp = ROOT / srel
        ssrc = sp.read_text(encoding="utf-8", errors="replace") if sp.exists() else ""
        net, table, err = _suite_net_legs(ssrc)
        say(f"      {x['id']}  ·  {x['suite']}  ·  stage {x['stage']}")
        say(f"        waives     {x['waives']}")
        say(f"        covers     records of stage {x['stage']} matching "
            f"{list(x['covers_record_match'])}")
        say(f"        legs       {sorted(x['legs'])} — VERIFIED this run to be EXACTLY "
            f"the set {srel} itself declares needs_net=True")
        # THE SUITE IS A FOREIGN FILE THIS TRACK DOES NOT OWN, and another track
        # edits it. Its LIVE state (sha, whole-LEGS-table size) is printed to
        # STDOUT ONLY and never enters the transcript: a filed table that embeds
        # a live count out of somebody else's file cannot reproduce to the byte,
        # and the original of this line did exactly that. [LEAN-HEPHAESTUS] R8
        clock(f"        [stdout only, foreign file] {srel} sha "
              f"{file_sha(sp)[0] if sp.exists() else 'ABSENT'}, whole LEGS table "
              f"{len(table)} leg(s), needs_net {sorted(net)}, parse "
              f"{'OK' if not err else err}")
        say(f"        also       conditional {sorted(x.get('conditional_legs', ()))} "
            f"(reaches the venue only on a planted-zero 5m bar)")
        say(f"        evidence   filed {x['evidence']['filed']}")
        say(f"                   remeas {x['evidence']['remeasured']}  "
            f"delta {x['evidence']['delta_bars']} bar(s), {x['evidence']['measured_on']}")
        say(f"        corroborated by {x['evidence']['source']['file']} "
            f"[{x['evidence']['source']['stage']}].{x['evidence']['source']['field']}")
        stg = next((t for t in prog["stages"] if t.get("stage") == x["stage"]), None)
        fld = _binding_field(stg, srel) if stg is not None else None
        say(f"        bound      stage {x['stage']}'s OWN ledger block names the "
            f"exempted suite {Path(srel).stem!r} (in its {fld!r}) — a waiver may not "
            f"be validated against a suite that produced none of the records it "
            f"covers [LEAN R11]")
        say(f"        ruling     {x['ruling_status']}")
    ok = not bad
    return ok, (f"{len(EXEMPTIONS)} exemption(s), each with a scope, a reason "
                f"({len(EXEMPTIONS[0]['reason'])} chars), a ruling status and EVIDENCE "
                f"RE-DERIVED off disk from the file it names, whatever that file "
                f"is; the exempted legs are EXACTLY the "
                f"{len(EXEMPTIONS[0]['legs'])} that the suite ITSELF declares "
                f"venue-reaching, read from that suite's own source; the suite is "
                f"BOUND to the stage it exempts — {EXEMPTIONS[0]['stage']}'s own "
                f"ledger block names "
                f"{Path(EXEMPTIONS[0]['suite']).stem!r}, so the waiver cannot be a "
                f"borrowed one; no stage is "
                f"COMPLETE on an exemption's strength (stage {EXEMPTIONS[0]['stage']} "
                f"reads PARTIAL); {n_fix} fixture record(s) scanned across "
                f"{len(prog['stages'])} stages, {n_drift} drifting, 0 of them unnamed; "
                f"negative control: the planted drift on the {hit} record(s) the "
                f"registry names is SILENTLY covered"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═══════════════════ F-C10-RESUME-5 · PROGRESS.json well-formed and honest
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


def wellformed_findings(prog: dict) -> list[str]:
    bad: list[str] = []
    for k in ("as_of_of_record", "as_of_last_closed_4h_close_ms", "branch",
              "contract_of_record", "head", "seed", "stages", "substrate",
              "tier", "live_cache_touched"):
        if k not in prog:
            bad.append(f"PROGRESS.json has no top-level {k!r}")
    if prog.get("live_cache_touched") is not False:
        bad.append(f"live_cache_touched = {prog.get('live_cache_touched')!r} — the "
                   f"live cache belongs to another lane and must read False")
    names = []
    for i, s in enumerate(prog.get("stages", [])):
        tag = s.get("stage", f"<stage {i}>")
        names.append(tag)
        for k in STAGE_KEYS:
            if k not in s:
                bad.append(f"{tag}: missing required key {k!r}")
        status = s.get("status")
        if status not in LEGAL_STATUS:
            bad.append(f"{tag}: status {status!r} is not one of {list(LEGAL_STATUS)}")
        shas = s.get("artifact_shas")
        if not isinstance(shas, dict):
            bad.append(f"{tag}: artifact_shas is {type(shas).__name__}, not a mapping")
            continue
        if "artifact_count" in s and s["artifact_count"] != len(shas):
            bad.append(f"{tag}: artifact_count {s['artifact_count']} != "
                       f"{len(shas)} recorded sha(s)")
        for rel, rec in sorted(shas.items()):
            if not isinstance(rec, dict) or "sha256" not in rec or "bytes" not in rec:
                bad.append(f"{tag}/{rel}: record is not {{sha256, bytes}}")
                continue
            if not _HEX64.match(str(rec["sha256"])):
                bad.append(f"{tag}/{rel}: sha256 {rec['sha256']!r} is not 64 lowercase hex")
            if not isinstance(rec["bytes"], int) or rec["bytes"] <= 0:
                bad.append(f"{tag}/{rel}: bytes {rec['bytes']!r} is not a positive int")
        blockers = s.get("blockers")
        if not isinstance(blockers, list):
            bad.append(f"{tag}: blockers is {type(blockers).__name__}, not a list")
            blockers = []
        fixtures = s.get("fixtures")
        if not isinstance(fixtures, list):
            bad.append(f"{tag}: fixtures is {type(fixtures).__name__}, not a list")
            fixtures = []
        for f in fixtures:
            for k in FIXTURE_KEYS:
                if k not in f:
                    bad.append(f"{tag}: a fixture record has no {k!r}")
        if status == "COMPLETE-VERIFIED":
            if blockers:
                bad.append(f"{tag}: claims COMPLETE-VERIFIED with {len(blockers)} "
                           f"blocker(s) listed — {str(blockers[0])[:80]!r}")
            if not fixtures:
                bad.append(f"{tag}: claims COMPLETE-VERIFIED with NO fixture record — "
                           f"LAW 1 says a stage is complete only if its fixtures re-pass")
            for f in fixtures:
                if f.get("exit_code") != 0:
                    bad.append(f"{tag}: claims COMPLETE-VERIFIED but a fixture record "
                               f"exits {f.get('exit_code')!r}")
                if f.get("legs_red"):
                    bad.append(f"{tag}: claims COMPLETE-VERIFIED but a fixture record "
                               f"carries {f.get('legs_red')} RED leg(s)")
                if not f.get("legs_total"):
                    bad.append(f"{tag}: a COMPLETE-VERIFIED fixture record reports "
                               f"{f.get('legs_total')!r} legs total")
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        bad.append(f"duplicated stage name(s) {dupes} — a ledger with two rows for one "
                   f"stage can say two things at once")
    return bad


def resume5_break():
    prog = load_progress()

    def mutate(fn):
        p = copy.deepcopy(prog)
        fn(p)
        return wellformed_findings(p)

    def add_blocker(p):
        next(s for s in p["stages"] if s["status"] == "COMPLETE-VERIFIED")["blockers"].append(
            "a blocker nobody looked at")

    def illegal_status(p):
        p["stages"][1]["status"] = "DONE"

    def drop_key(p):
        del p["stages"][2]["blockers"]

    def miscount(p):
        p["stages"][5]["artifact_count"] = 999

    def red_leg(p):
        next(s for s in p["stages"] if s["status"] == "COMPLETE-VERIFIED")["fixtures"][0]["legs_red"] = 1

    def bad_exit(p):
        next(s for s in p["stages"] if s["status"] == "COMPLETE-VERIFIED")["fixtures"][0]["exit_code"] = 1

    def no_fixtures(p):
        next(s for s in p["stages"] if s["status"] == "COMPLETE-VERIFIED")["fixtures"] = []

    def duplicate(p):
        p["stages"].append(copy.deepcopy(p["stages"][0]))

    def short_sha(p):
        k = sorted(p["stages"][5]["artifact_shas"])[0]
        p["stages"][5]["artifact_shas"][k]["sha256"] = "deadbeef"

    def touched(p):
        p["live_cache_touched"] = True

    return plants([
        ("COMPLETE-VERIFIED WITH A BLOCKER (the most likely future lie)",
         lambda: mutate(add_blocker)),
        ("ILLEGAL STATUS ('DONE')", lambda: mutate(illegal_status)),
        ("MISSING KEY (a stage loses 'blockers')", lambda: mutate(drop_key)),
        ("MISCOUNTED ARTIFACTS (artifact_count 10 -> 999)", lambda: mutate(miscount)),
        ("RED LEG UNDER A COMPLETE CLAIM (legs_red 0 -> 1)", lambda: mutate(red_leg)),
        ("NONZERO EXIT UNDER A COMPLETE CLAIM (exit_code 0 -> 1)", lambda: mutate(bad_exit)),
        ("COMPLETE WITH NO FIXTURE RECORD AT ALL", lambda: mutate(no_fixtures)),
        ("DUPLICATED STAGE ROW", lambda: mutate(duplicate)),
        ("TRUNCATED SHA ('deadbeef' in place of 64 hex)", lambda: mutate(short_sha)),
        ("TOUCHED LIVE CACHE (live_cache_touched -> True)", lambda: mutate(touched)),
    ])


def resume5_real():
    prog = load_progress()
    bad = wellformed_findings(prog)
    n_sha = sum(len(s["artifact_shas"]) for s in prog["stages"])
    n_fix = sum(len(s["fixtures"]) for s in prog["stages"])
    n_blk = sum(len(s["blockers"]) for s in prog["stages"])
    say(f"      {'stage':<20} {'status':<18} {'shas':>5} {'fixt':>5} {'blk':>4}")
    for s in prog["stages"]:
        say(f"      {s['stage']:<20} {s['status']:<18} {len(s['artifact_shas']):>5} "
            f"{len(s['fixtures']):>5} {len(s['blockers']):>4}")
    ok = not bad
    n_c = sum(1 for s in prog["stages"] if s["status"] == "COMPLETE-VERIFIED")
    return ok, (f"{len(prog['stages'])} stage record(s), every one carrying "
                f"{list(STAGE_KEYS)}; every status one of {list(LEGAL_STATUS)}; "
                f"{n_c} COMPLETE-VERIFIED, every one with ZERO blockers, a fixture "
                f"record, exit 0 and 0 red legs; {n_sha:,} sha(s) all 64 lowercase "
                f"hex with positive byte counts; {n_fix} fixture record(s) complete; "
                f"{n_blk} blocker(s) total, all under non-complete stages"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═══════════════════════════════════ F-C10-RESUME-6 · STEP0_RECORD re-hashes
def _git_blob(rev: str, rel: str) -> bytes | None:
    try:
        out = subprocess.run(["git", "-C", str(ROOT), "show", f"{rev}:{rel}"],
                             capture_output=True, check=False)
    except Exception:
        return None
    return out.stdout if out.returncode == 0 else None


def _pine_defaults(text: str) -> dict:
    out: dict = {}
    for pin, var in PINE_NUM_VARS.items():
        m = re.search(rf"^{var}\s*=\s*input\.(?:float|int)\(\s*([0-9.]+)", text, re.M)
        out[pin] = float(m.group(1)) if m else None
    m = re.search(r'^boundaryMode\s*=\s*input\.string\(\s*"(\w+)"', text, re.M)
    out["BOUNDARY_MODE"] = m.group(1) if m else None
    m = re.search(r"^ATR_LEN\s*=\s*(\d+)", text, re.M)
    out["ATR_LEN"] = int(m.group(1)) if m else None
    return out


QR5_MARKERS = ("breakout scanner", "ss_breakout", "ss breakout", "saucer")
QR5_PHANTOM = "0.67"


def _qr5_scan(files: tuple = RF_CODE_FILES) -> dict:
    """[Q-R5], MEASURED rather than asserted. The claim is about the MACHINE, so
    the scan covers the RangeFinder's code — the Pine source, the machine, the
    port and the twin — and NOT the fixture suites, whose only 0.67 is their own
    deliberate sabotage plant (counted separately below).

    THE FILE LIST IS PINNED. It used to glob pine/*.pine — a MOVING SET, 10
    files today of which 4 are untracked additions with nothing to do with the
    RangeFinder — and that moving membership went straight into
    STEP0_RECORD.json's filed bytes, so adding or removing ANY .pine file turned
    leg 6 RED for a reason with nothing to do with STEP 0. The BREADTH of the
    claim is kept by _qr5_sweep() below, whose hits are still RED but whose
    membership never enters the filed bytes. [LEAN-HEPHAESTUS] R6"""
    files = list(files)
    marker_hits: dict[str, list[str]] = {}
    phantom_hits: dict[str, int] = {}
    missing: list[str] = []
    for rel in files:
        p = ROOT / rel
        if not p.exists():
            missing.append(rel)
            continue
        txt = p.read_text(encoding="utf-8", errors="replace")
        low = txt.lower()
        hits = [m for m in QR5_MARKERS if m in low]
        if hits:
            marker_hits[rel] = hits
        n = txt.count(QR5_PHANTOM)
        if n:
            phantom_hits[rel] = n
    return {"files_scanned": files, "files_missing": missing,
            "marker_hits": marker_hits, "phantom_0_67_hits": phantom_hits}


def _qr5_sweep() -> dict:
    """THE BREADTH OF [Q-R5], kept LIVE and kept OUT OF THE FILED BYTES. Every
    pine/*.pine source that is not one of the pinned RangeFinder files is
    scanned on every run; a marker or a phantom 0.67 landing in pine/ is still
    RED. Only the MEMBERSHIP of this moving set is excluded from the record."""
    rest = tuple(str(p.relative_to(ROOT)).replace(os.sep, "/")
                 for p in sorted((ROOT / "pine").glob("*.pine"))
                 if str(p.relative_to(ROOT)).replace(os.sep, "/") not in RF_CODE_FILES)
    out = _qr5_scan(rest)
    out["files_missing"] = []          # a glob cannot miss what it just listed
    return out


def build_step0_record(step0_sources: dict | None = None) -> dict:
    """Rebuilt from what R0 established. Deterministic: no clock, no ordering
    that is not explicit. Every sha is MEASURED here, never copied forward."""
    STEP0 = STEP0_SOURCES if step0_sources is None else step0_sources
    sources = {}
    for rel in sorted(STEP0):
        p = ROOT / rel
        if p.exists():
            h, n = file_sha(p)
        else:
            h, n = None, None
        row = {"sha256_now": h, "bytes": n,
               "sha256_expected": STEP0[rel]}
        if rel == "scripts/rangefinder_twin.py":
            blob = _git_blob(STEP0_COMMIT, rel)
            row["sha256_at_step0_commit"] = sha_bytes(blob) if blob is not None else None
            row["moved_since_step0"] = (row["sha256_at_step0_commit"] != h)
            row["sanctioned_difference"] = list(TWIN_SANCTIONED)
            row["note"] = ("the ONE STEP 0 source whose bytes moved after STEP 0, by "
                           "the Stage 0a anchor edit; the difference is loader-only "
                           "and proven so by F-RF-PINS' twin plant")
        sources[rel] = row
    pine_txt = PINE_PATH.read_text(encoding="utf-8") if PINE_PATH.exists() else ""
    qr5 = _qr5_scan()
    rf_fix = ROOT / "scripts" / "tierc10_rf_fixtures.py"
    rf_fixture_plants = (rf_fix.read_text(encoding="utf-8").count(QR5_PHANTOM)
                         if rf_fix.exists() else None)
    return {
        "record": "STEP0_RECORD",
        "tier": "TIER-C10",
        "stage": "STEP 0",
        "status": "COMPLETE-VERIFIED",
        "as_of_last_closed_4h": AS_OF,
        "as_of_last_closed_4h_close_ms": CLOSE_MS,
        "seed": SEED,
        "branch": "v12-v1-census",
        "step0_commit": STEP0_COMMIT,
        "rebuilt_by": "scripts/tierc10_resume_fixtures.py (F-C10-RESUME-6)",
        "why_rebuilt": (
            "R0 (2026-09-22) found STEP 0 COMPLETE-VERIFIED on clauses (a) and (c) "
            "only: its manifest was destroyed with the killed session's scratchpad "
            "and `find` for STEP0* returns nothing. This file restores the LAW 1(b) "
            "record from what R0 established, with every sha RE-MEASURED here."),
        "sources": sources,
        "pins_of_record": {k: v for k, v in PINS_OF_RECORD},
        "pins_key_order": [k for k, _ in PINS_OF_RECORD],
        "pins_reconciled": "PINS-OK 12/12 — port == machine == Pine, key order included",
        "pine_defaults_reparsed": _pine_defaults(pine_txt),
        "q_r5_attestation": {
            "claim": ("the RangeFinder inherits NO starting value from the SS Breakout "
                      "Scanner (operator ruling 2026-07-29, [Q-R5])"),
            "method": ("grep-attest, RE-MEASURED on every run over the RangeFinder's "
                       "PINNED code set: the Pine source, the machine "
                       "(engine/rangefinder.py), the port (analytics/rangefinder_census.py) "
                       "and the twin (scripts/rangefinder_twin.py); markers "
                       + str(list(QR5_MARKERS)) + ". Every OTHER pine/*.pine source is "
                       "swept live on every run by _qr5_sweep() and a hit there is RED "
                       "too; only that moving set's MEMBERSHIP is kept out of these "
                       "filed bytes, so a .pine file appearing in or leaving the repo "
                       "cannot make this record un-reproduce. [LEAN-HEPHAESTUS] R6"),
            "scan": qr5,
            "holds": (not qr5["marker_hits"] and not qr5["phantom_0_67_hits"]
                      and not qr5["files_missing"]),
            "note": ("the scanner's source is not in this repo at all — no pine/ file "
                     "is a scanner, and the marker words occur only in prose "
                     "(LEDGER.md, the RESUME contract and three contract drafts), "
                     "never in code"),
        },
        "argus_note_finding": {
            "claim_in_note": {"TOUCH_EPS": 0.67, "DEV_RETURN_BARS": 8},
            "on_disk": {"TOUCH_EPS": 0.60, "DEV_RETURN_BARS": 7},
            "phantom_hits_in_code": qr5["phantom_0_67_hits"],
            "phantom_hits_in_the_rf_fixture_suite": rf_fixture_plants,
            "verdict": ("NO ON-DISK SOURCE. 0.67 occurs ZERO times across the "
                        f"{len(qr5['files_scanned'])} PINNED RangeFinder code file(s) "
                        f"(the Pine source, the machine, the port, the twin), and zero "
                        f"times in the live sweep of every other pine/*.pine. Its only "
                        f"occurrences anywhere in the lane are {rf_fixture_plants} inside "
                        "scripts/tierc10_rf_fixtures.py, where they ARE the fixture's own "
                        "deliberate sabotage plants ('PIN PLANT … TOUCH_EPS 0.60 -> 0.67'). "
                        "DEV_RETURN_BARS reads 7 in the Pine input, the machine and the "
                        "port alike."),
        },
        "fixture_transcript": "research_outputs/tierc10/FIXTURES_RF.txt",
    }


def _step0_bytes(rec: dict) -> bytes:
    # NOT sort_keys: the pin KEY ORDER is part of the record (export order is
    # bytes). Every dict below is built in a fixed, explicit order, so this is
    # deterministic without sorting.
    return (json.dumps(rec, indent=2, ensure_ascii=False)
            .encode("utf-8") + b"\n")


def step0_record_presence_findings(exists: bool, rewrite: bool) -> list[str]:
    """DELETE-AND-RERUN MAY NOT LAUNDER A SOURCE CHANGE.

    main() used to write STEP0_RECORD.json whenever it was absent — silently,
    from whatever the tree looked like at that moment — so the entire write-once
    discipline [LEAN R4] came off with one `rm`, and with it the only thing
    pinning STEP 0's four sources. Absence is now a FINDING unless the refresh
    is asked for by name."""
    if exists or rewrite:
        return []
    return [f"{STEP0_RECORD_PATH.name} is ABSENT and this module REFUSED to "
            f"regenerate it: a record that reappears on demand, rebuilt from "
            f"whatever the tree looks like now, pins NOTHING — delete-and-rerun "
            f"would launder any STEP 0 source change. Re-file it deliberately "
            f"with --rewrite-step0-record."]


def step0_findings(rec: dict, step0_sources: dict | None = None) -> list[str]:
    """Judged against INDEPENDENT measurement — disk, git and the live port —
    never against the record's own arithmetic."""
    STEP0 = STEP0_SOURCES if step0_sources is None else step0_sources
    bad: list[str] = []
    for rel in sorted(STEP0):
        row = (rec.get("sources") or {}).get(rel)
        if not row:
            bad.append(f"STEP0_RECORD records no source {rel!r}")
            continue
        p = ROOT / rel
        if not p.exists():
            bad.append(f"{rel}: recorded by STEP0_RECORD, absent from disk")
            continue
        h, n = file_sha(p)
        if row.get("sha256_now") != h:
            bad.append(f"{rel}: STEP0_RECORD says {str(row.get('sha256_now'))[:16]}…, "
                       f"re-hashes {h[:16]}…")
        if row.get("bytes") != n:
            bad.append(f"{rel}: STEP0_RECORD says {row.get('bytes')!r} B, on disk {n:,} B")
        if row.get("sha256_expected") != STEP0[rel]:
            bad.append(f"{rel}: STEP0_RECORD's expected sha is not the literal of record")
        # DISK vs THE STEP 0 LITERAL — the comparison that was MISSING. The two
        # checks above are record-vs-disk and record-vs-literal; neither asks
        # whether the SOURCE ITSELF still hashes to STEP 0's value. A source that
        # moved away produced a record whose own two fields openly contradicted
        # each other (sha256_now beside a different sha256_expected) with NO leg
        # firing, and deleting the record and re-running laundered the change.
        if h != STEP0[rel]:
            bad.append(f"{rel}: A STEP 0 SOURCE MOVED — on disk it hashes {h[:16]}…, "
                       f"the STEP 0 literal of record is {STEP0[rel][:16]}…. "
                       f"STEP0_RECORD would carry both numbers side by side and "
                       f"contradict itself in plain sight")
    twin = "scripts/rangefinder_twin.py"
    trow = (rec.get("sources") or {}).get(twin) or {}
    blob = _git_blob(STEP0_COMMIT, twin)
    if blob is None:
        bad.append(f"{twin}: the STEP 0 blob at {STEP0_COMMIT} is unreachable — "
                   f"silence is not health")
    else:
        bsha = sha_bytes(blob)
        if bsha != STEP0_TWIN_BLOB_SHA:
            bad.append(f"{twin}: the {STEP0_COMMIT} blob hashes {bsha[:16]}…, not the "
                       f"STEP 0 literal {STEP0_TWIN_BLOB_SHA[:16]}…")
        if trow.get("sha256_at_step0_commit") != bsha:
            bad.append(f"{twin}: STEP0_RECORD's step0-commit sha "
                       f"{str(trow.get('sha256_at_step0_commit'))[:16]}… != the git blob's "
                       f"{bsha[:16]}…")
    # the twelve pins, re-read from the LIVE port and re-parsed from the Pine
    try:
        import analytics.rangefinder_census as RC
        live = {**RC.PINS, **RC.PINS_V2, "ATR_LEN": RC.ATR_LEN}
    except Exception as e:
        live = {}
        bad.append(f"analytics/rangefinder_census.py would not import: "
                   f"{e.__class__.__name__}: {e}")
    pine = _pine_defaults(PINE_PATH.read_text(encoding="utf-8"))
    recorded_pins = rec.get("pins_of_record") or {}
    if list(recorded_pins) != [k for k, _ in PINS_OF_RECORD]:
        bad.append(f"STEP0_RECORD's pin KEY ORDER {list(recorded_pins)} != the order of "
                   f"record {[k for k, _ in PINS_OF_RECORD]} — export order is bytes")
    for k, want in PINS_OF_RECORD:
        got = recorded_pins.get(k)
        if got != want:
            bad.append(f"pin {k}: STEP0_RECORD says {got!r}, the record is {want!r}")
        if live and k in live and live[k] != want:
            bad.append(f"pin {k}: the LIVE port says {live[k]!r}, the record {want!r}")
        if isinstance(want, (int, float)) and k in pine:
            if pine[k] is None:
                bad.append(f"pin {k}: no default could be parsed out of the Pine source "
                           f"— silence is not agreement")
            elif float(pine[k]) != float(want):
                bad.append(f"pin {k}: the PINE default says {pine[k]!r}, the record {want!r}")
    if pine.get("BOUNDARY_MODE") != "body":
        bad.append(f"pin BOUNDARY_MODE: the PINE default says "
                   f"{pine.get('BOUNDARY_MODE')!r}, the record 'body'")
    # the phantom pin must never be launderable into the record
    phantom = {k: v for k, v in recorded_pins.items()
               if (k == "TOUCH_EPS" and v == 0.67)
               or (k == "DEV_RETURN_BARS" and v == 8)}
    if phantom:
        bad.append(f"STEP0_RECORD carries the Argus note's phantom pin {phantom} as a "
                   f"PIN OF RECORD — 0.67 / DEV_RETURN 8 has NO on-disk source")
    if (rec.get("argus_note_finding") or {}).get("on_disk") != {"TOUCH_EPS": 0.60,
                                                                "DEV_RETURN_BARS": 7}:
        bad.append("STEP0_RECORD's Argus finding no longer names the on-disk values")
    qr5 = (rec.get("q_r5_attestation") or {})
    if qr5.get("holds") is not True:
        bad.append("STEP0_RECORD's [Q-R5] attestation does not hold")
    sweep = _qr5_sweep()                    # the BREADTH, live, off the record
    if sweep["marker_hits"]:
        bad.append(f"[Q-R5] BREACHED IN pine/: SS Breakout Scanner marker(s) now occur "
                   f"in {sweep['marker_hits']} — the pinned set is clean but the claim "
                   f"is about the machine and a scanner in pine/ contradicts it")
    if sweep["phantom_0_67_hits"]:
        bad.append(f"[Q-R5]/ARGUS: the phantom 0.67 now occurs in pine/: "
                   f"{sweep['phantom_0_67_hits']}")
    now = _qr5_scan()                       # RE-MEASURED, never trusted
    if now["marker_hits"]:
        bad.append(f"[Q-R5] BREACHED: SS Breakout Scanner marker(s) now occur in the "
                   f"RangeFinder's own code: {now['marker_hits']}")
    if now["phantom_0_67_hits"]:
        bad.append(f"[Q-R5]/ARGUS: the phantom 0.67 now occurs in the RangeFinder's own "
                   f"code: {now['phantom_0_67_hits']}")
    if now["files_missing"]:
        bad.append(f"[Q-R5]: {now['files_missing']} could not be scanned — silence is "
                   f"not health")
    if qr5.get("scan") != now:
        bad.append(f"[Q-R5]: STEP0_RECORD's filed scan does not reproduce "
                   f"({len((qr5.get('scan') or {}).get('files_scanned', []))} file(s) "
                   f"filed vs {len(now['files_scanned'])} scanned now)")
    if rec.get("as_of_last_closed_4h") != AS_OF:
        bad.append(f"STEP0_RECORD as_of {rec.get('as_of_last_closed_4h')!r} != {AS_OF}")
    return bad


def step0_reproduces(on_disk: bytes) -> list[str]:
    """The filed record must be exactly what a fresh, deterministic rebuild
    produces — no drift, no hand edit, no stale copy."""
    rebuilt = _step0_bytes(build_step0_record())
    if rebuilt == on_disk:
        return []
    return [f"STEP0_RECORD.json is NOT byte-reproducible: a rebuild is "
            f"{len(rebuilt):,} B / {sha_bytes(rebuilt)[:16]}… against the filed "
            f"{len(on_disk):,} B / {sha_bytes(on_disk)[:16]}…"]


def resume6_break():
    rec = build_step0_record()

    def mutate(fn):
        r = copy.deepcopy(rec)
        fn(r)
        return step0_findings(r)

    def bent_pine(r):
        r["sources"]["pine/SS12_RangeFinder_v2.pine"]["sha256_now"] = "0" * 64

    def phantom(r):
        r["pins_of_record"]["TOUCH_EPS"] = 0.67
        r["pins_of_record"]["DEV_RETURN_BARS"] = 8

    def ghost_source(r):
        r["sources"].pop("analytics/rangefinder_census.py")

    def bent_blob(r):
        r["sources"]["scripts/rangefinder_twin.py"]["sha256_at_step0_commit"] = "1" * 64

    def reorder(r):
        r["pins_of_record"] = {k: v for k, v in sorted(r["pins_of_record"].items())}

    def bent_bytes(r):
        r["sources"]["engine/rangefinder.py"]["bytes"] = 1

    def drop_qr5(r):
        r["q_r5_attestation"]["holds"] = False

    def move_as_of(r):
        r["as_of_last_closed_4h"] = "2026-09-22T00:00:00Z"

    def bent_scan(r):
        r["q_r5_attestation"]["scan"]["files_scanned"] = \
            r["q_r5_attestation"]["scan"]["files_scanned"][:2]

    def source_left_the_literal():
        """THE REALISTIC FAILURE: a STEP 0 SOURCE moves away from its STEP 0 sha
        and the record is rebuilt from the tree. The record then carries
        sha256_now beside a DIFFERENT sha256_expected — contradicting itself in
        plain sight — and under the old code NO leg fired."""
        srcs = dict(STEP0_SOURCES)
        srcs["engine/rangefinder.py"] = "0" * 64
        return step0_findings(build_step0_record(srcs), srcs)

    def deleted_record():
        """DELETE-AND-RERUN: the record is absent and no refresh was asked for."""
        return step0_record_presence_findings(False, False)

    def hand_edited_file():
        # a tampered COPY of the filed bytes, never the file itself
        filed = (STEP0_RECORD_PATH.read_bytes()
                 if STEP0_RECORD_PATH.exists() else _step0_bytes(rec))
        return step0_reproduces(filed.replace(b'"seed": 20260921',
                                              b'"seed": 20260922'))

    return plants([
        (f"BENT [Q-R5] SCAN (the filed scan claims 2 files were scanned, not "
         f"{len(RF_CODE_FILES)})",
         lambda: mutate(bent_scan)),
        ("HAND-EDITED FILE (a COPY of the filed bytes with seed 20260921 -> 20260922)",
         hand_edited_file),
        ("BENT PINE SHA (sha256_now -> 64 zeros)", lambda: mutate(bent_pine)),
        ("THE PHANTOM PIN (TOUCH_EPS 0.60 -> 0.67, DEV_RETURN_BARS 7 -> 8)",
         lambda: mutate(phantom)),
        ("GHOST SOURCE (analytics/rangefinder_census.py dropped from the record)",
         lambda: mutate(ghost_source)),
        ("BENT TWIN BLOB (sha256_at_step0_commit -> 64 ones)", lambda: mutate(bent_blob)),
        ("REORDERED PINS (alphabetical — export order is bytes)", lambda: mutate(reorder)),
        ("BENT BYTE COUNT (engine/rangefinder.py -> 1 B)", lambda: mutate(bent_bytes)),
        ("[Q-R5] WITHDRAWN (holds -> False)", lambda: mutate(drop_qr5)),
        ("MOVED AS-OF (2026-09-22T00:00:00Z)", lambda: mutate(move_as_of)),
        ("A STEP 0 SOURCE LEFT ITS LITERAL (engine/rangefinder.py's literal of "
         "record moved to 64 zeros and the record was rebuilt from the tree — the "
         "record's own two fields contradict each other)", source_left_the_literal),
        ("DELETED RECORD (STEP0_RECORD.json absent, no --rewrite-step0-record — "
         "delete-and-rerun may not launder a source change)", deleted_record),
    ])


def resume6_real():
    absent = step0_record_presence_findings(STEP0_RECORD_PATH.exists(), REWRITE_STEP0)
    if absent:
        return False, absent[0]
    if not STEP0_RECORD_PATH.exists():
        return False, f"{STEP0_RECORD_PATH.relative_to(ROOT)} does not exist"
    on_disk = STEP0_RECORD_PATH.read_bytes()
    rec = json.loads(on_disk.decode("utf-8"))
    bad = step0_findings(rec) + step0_reproduces(on_disk)
    for rel in sorted(STEP0_SOURCES):
        row = rec["sources"][rel]
        disk_h = file_sha(ROOT / rel)[0] if (ROOT / rel).exists() else ""
        mark = ("== STEP 0 (disk sha == the literal of record)"
                if disk_h == STEP0_SOURCES[rel] else "MOVED OFF THE STEP 0 LITERAL")
        say(f"      {rel}")
        say(f"        {row['sha256_now']}  {row['bytes']:>9,} B  {mark}")
        if rel == "scripts/rangefinder_twin.py":
            say(f"        blob @{STEP0_COMMIT}  {row['sha256_at_step0_commit']}  "
                f"moved_since_step0={row['moved_since_step0']} "
                f"(sanctioned: {row['sanctioned_difference']})")
    say(f"      pins {', '.join(f'{k} {v}' for k, v in PINS_OF_RECORD)}")
    q = rec["q_r5_attestation"]
    say(f"      [Q-R5] {len(q['scan']['files_scanned'])} RangeFinder code file(s) "
        f"scanned for {list(QR5_MARKERS)} and '0.67': "
        f"{len(q['scan']['marker_hits'])} marker hit(s), "
        f"{len(q['scan']['phantom_0_67_hits'])} phantom hit(s) — HOLDS={q['holds']}")
    sweep = _qr5_sweep()
    say(f"      [Q-R5] breadth sweep of every OTHER pine/*.pine source "
        f"[LEAN R6]: {len(sweep['marker_hits'])} marker hit(s), "
        f"{len(sweep['phantom_0_67_hits'])} phantom hit(s) — membership is LIVE and "
        f"is deliberately NOT part of the filed bytes")
    clock(f"      [stdout only, moving set] swept {len(sweep['files_scanned'])} "
          f"further .pine file(s): {sweep['files_scanned']}")
    say(f"      [Q-R5] {q['note']}")
    say(f"      ARGUS NOTE {rec['argus_note_finding']['verdict'][:96]}…")
    ok = not bad
    return ok, (f"STEP0_RECORD.json ({len(on_disk):,} B, sha "
                f"{sha_bytes(on_disk)[:16]}…) re-hashes: {len(STEP0_SOURCES)} STEP 0 "
                f"source sha(s) re-measured from disk NOW and all MATCH, the twin's "
                f"{STEP0_COMMIT} blob re-read from git and MATCHES the STEP 0 literal, "
                f"{len(PINS_OF_RECORD)} pins agree with the LIVE port AND the Pine "
                f"defaults in the recorded KEY ORDER, [Q-R5] holds, the Argus note's "
                f"0.67 / DEV_RETURN 8 is recorded as having no on-disk source, every "
                f"STEP 0 source's DISK sha still equals its STEP 0 literal, the record "
                f"was NOT auto-regenerated, and a rebuild is BYTE-IDENTICAL"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


def _first_diff(old: bytes, new: bytes, limit: int = 6) -> list[str]:
    a = old.decode("utf-8", errors="replace").splitlines()
    b = new.decode("utf-8", errors="replace").splitlines()
    out: list[str] = []
    for i in range(max(len(a), len(b))):
        x = a[i] if i < len(a) else "<absent>"
        y = b[i] if i < len(b) else "<absent>"
        if x == y:
            continue
        out.append(f"line {i + 1:>4}  filed    {x[:112]}")
        out.append(f"line {i + 1:>4}  this run {y[:112]}")
        if len(out) >= 2 * limit:
            break
    out.append(f"({len(a):,} filed line(s) vs {len(b):,} this run)")
    return out


# ════════════════ F-C10-RESUME-T · the transcript of record is never clobbered
def file_transcript(out: Path, body: bytes, refile: bool,
                    quiet: bool = False) -> list[str]:
    """THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED.

    THE DEFECT THIS REPLACES.  main() wrote the transcript UNCONDITIONALLY at the
    end of every whole-suite run.  So an ordinary, sanctioned run that produced
    different bytes — because a foreign file this track does not own had moved —
    silently DESTROYED the filed artifact and the evidence of the original with
    it, and exited 0.  The house DETERMINISM law says a filed table must
    reproduce to the byte; the failure mode must therefore be loud and
    non-destructive, not silent and destructive.

    The artifact of record is written only when it is ABSENT, when the new bytes
    are IDENTICAL to it, or when --refile-transcript asks for a re-file by name.
    Otherwise this run goes to <name>_rerun.txt, the delta is printed, the
    artifact of record is left exactly as it was, and the finding is RED."""
    def note(line: str) -> None:
        if not quiet:
            clock(line)
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists():
        out.write_bytes(body)
        note(f"\n  transcript -> {out}  {len(body):,} B  sha {sha_bytes(body)}  [NEW]")
        return []
    filed = out.read_bytes()
    if filed == body:
        note(f"\n  transcript == {out}  {len(body):,} B  sha {sha_bytes(body)}  "
             f"BYTE-IDENTICAL to the filed artifact; not rewritten")
        return []
    if refile:
        out.write_bytes(body)
        note(f"\n  transcript -> {out}  RE-FILED on --refile-transcript: "
             f"{sha_bytes(filed)} -> {sha_bytes(body)}")
        return []
    rerun = out.with_name(out.stem + "_rerun.txt")
    rerun.write_bytes(body)
    bad = [f"this run's transcript is NOT byte-identical to the filed artifact "
           f"{out.name}: filed {len(filed):,} B sha {sha_bytes(filed)[:16]}… vs this "
           f"run {len(body):,} B sha {sha_bytes(body)[:16]}…. THE ARTIFACT OF RECORD "
           f"WAS NOT OVERWRITTEN; this run went to {rerun.name}. "
           + " | ".join(_first_diff(filed, body, 3))]
    if out.read_bytes() != filed:
        bad.append(f"{out.name}: THE FILED ARTIFACT WAS OVERWRITTEN ANYWAY — the "
                   f"no-clobber guard does not guard")
    return bad


def _tmp_transcript(filed: bytes) -> Path:
    d = Path(tempfile.mkdtemp(prefix="tc10_resume_t_"))
    p = d / TRANSCRIPT
    p.write_bytes(filed)
    return p


# the fixed, module-literal stand-in for "a filed transcript". It is NOT the
# live FIXTURES_RESUME.txt: reading the artifact of record into the leg and
# printing its sha would embed the transcript's own previous sha in itself, a
# self-reference that can never converge — the very defect [LEAN R8] names.
_T_FILED = (b"TIER-C10 FIXTURES_RESUME (stand-in)\n"
            b"  line two, the one a drifting run rewrites\n"
            b"  line three\n")


def resumeT_break():
    filed = _T_FILED

    def attempt(body: bytes) -> list[str]:
        p = _tmp_transcript(filed)
        try:
            bad = file_transcript(p, body, refile=False, quiet=True)
            if p.read_bytes() != filed:
                bad.append("THE FILED ARTIFACT WAS CLOBBERED by a non-reproducing run")
            return bad
        finally:
            shutil.rmtree(p.parent, ignore_errors=True)

    return plants([
        ("NON-REPRODUCING RUN (one line of the filed transcript changed — exactly "
         "what a foreign file's live count does to this artifact)",
         lambda: attempt(filed.replace(b"legs", b"LEGS", 1) + b"drift\n")),
        ("TRUNCATED RUN (the run dies half way and would have left a short file "
         "standing as the artifact of record)", lambda: attempt(filed[:len(filed) // 2])),
        ("EMPTY RUN (zero bytes offered as the transcript of record)",
         lambda: attempt(b"")),
        ("APPENDED BYTE (one newline more than the filed artifact)",
         lambda: attempt(filed + b"\n")),
    ])


def resumeT_real():
    filed_p = TC / TRANSCRIPT
    filed = _T_FILED
    bad: list[str] = []
    # (a) NEGATIVE CONTROL — a guard that fires on everything guards nothing:
    #     identical bytes must be silent AND must not rewrite the file
    p = _tmp_transcript(filed)
    try:
        before = p.stat().st_mtime_ns
        f = file_transcript(p, filed, refile=False, quiet=True)
        if f:
            bad.append(f"CONTROL: byte-identical bytes were reported as a delta: {f[:1]}")
        if p.read_bytes() != filed:
            bad.append("CONTROL: byte-identical bytes still rewrote the artifact")
        rerun_made = (p.parent / (Path(TRANSCRIPT).stem + "_rerun.txt")).exists()
        if rerun_made:
            bad.append("CONTROL: a rerun file was written for an identical run")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    # (b) a NON-REPRODUCING run is RED, the artifact survives, the rerun is filed
    p = _tmp_transcript(filed)
    other = filed + b"A LINE THE FILED ARTIFACT DOES NOT CARRY\n"
    try:
        f = file_transcript(p, other, refile=False, quiet=True)
        if not f:
            bad.append("a non-reproducing run produced NO finding — the guard is void")
        if p.read_bytes() != filed:
            bad.append("a non-reproducing run CLOBBERED the artifact of record")
        rp = p.with_name(p.stem + "_rerun.txt")
        if not rp.exists() or rp.read_bytes() != other:
            bad.append("the non-reproducing run's bytes were not preserved in "
                       "<name>_rerun.txt — the evidence is gone either way")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    # (c) --refile-transcript is the ONE deliberate escape, and it is silent
    p = _tmp_transcript(filed)
    try:
        f = file_transcript(p, other, refile=True, quiet=True)
        if f:
            bad.append(f"--refile-transcript still reported a finding: {f[:1]}")
        if p.read_bytes() != other:
            bad.append("--refile-transcript did not actually re-file")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    say(f"      stand-in filed artifact  {sha_bytes(_T_FILED)}  {len(_T_FILED)} B "
        f"(a module literal — reading the LIVE transcript here would embed its own "
        f"previous sha in itself [LEAN R8])")
    clock(f"      [stdout only, live] artifact of record "
          f"{filed_p if filed_p.exists() else '(none yet)'} "
          f"{file_sha(filed_p)[0] if filed_p.exists() else '—'}")
    say(f"      the writer main() uses IS file_transcript(); it writes the artifact "
        f"of record only when it is ABSENT, when the bytes are IDENTICAL, or on an "
        f"explicit --refile-transcript [LEAN R9]")
    ok = not bad
    return ok, ("the transcript of record cannot be clobbered: identical bytes are "
                "silent and do not rewrite the file (negative control); a "
                "non-reproducing run yields a RED finding naming the first differing "
                "lines, LEAVES the filed artifact byte-for-byte as it was, and "
                "preserves its own bytes in FIXTURES_RESUME_rerun.txt; and "
                "--refile-transcript is the one deliberate, named escape"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ══════════════════════════════════════════════════════════════════ the table
FIXTURES = (
    ("F-C10-RESUME-0", "THE EXTERNAL ANCHOR — the working-tree ledger is judged "
     "against the COMMITTED blob, and the committed blob against a module literal",
     "the pinned blob f97cded:research_outputs/tierc10/PROGRESS.json is unreachable "
     "or does not hash to the literal typed in this module; HEAD carries no ledger at "
     "all; any stage the pinned rev called COMPLETE-VERIFIED is gone, demoted or "
     "rewritten at HEAD; or any stage the WORKING TREE calls COMPLETE-VERIFIED is "
     "absent from HEAD, not COMPLETE-VERIFIED at HEAD, or carries a block that is not "
     "byte-identical to HEAD's — a re-recorded sha, a promoted stage with its blockers "
     "deleted, or a de-recorded artifact each being exactly that; OR, READ THE OTHER "
     "WAY, any stage HEAD calls COMPLETE-VERIFIED is MISSING from the working tree or "
     "is no longer COMPLETE-VERIFIED there — a demotion or a deletion drops every one "
     "of that stage's artifacts out of every re-hash in this suite, so silence over "
     "it is not health",
     resume0_break, resume0_real),
    ("F-C10-RESUME-1", "every artifact a COMPLETE-VERIFIED stage records re-hashes, "
     "and nothing unrecorded sits in a completed stage's directory",
     "any recorded content sha does not re-hash, any recorded byte count moves, a "
     "recorded artifact is absent from both its path and the LAW-2 quarantine, a "
     "quarantine redirect resolves to bytes that are not the recorded ones, a file "
     "sits inside a COMPLETE-VERIFIED stage's own directory that the ledger does not "
     "record, or a file sits LOOSE IN THE TIERC10 ROOT that no stage records and the "
     "named allowlist does not carry",
     resume1_break, resume1_real),
    ("F-C10-RESUME-2", "the LAW-2 kill-partials are intact and a tampered partial FAILS",
     "a quarantined kill-partial is absent, or its bytes hash to anything but the sha "
     "typed in this fixture, or the fixture literal / the disk bytes / the "
     "PROGRESS.json record disagree, or the quarantine README does not name it",
     resume2_break, resume2_real),
    ("F-C10-RESUME-3", "the corridor is ONE — LAW 4 made checkable",
     "PROGRESS.json's as_of_of_record, the Stage D manifest's as_of_last_closed_4h and "
     "AS_OF_PIN.json's are not all 2026-09-21T16:00:00Z, any close_ms is not "
     "1790006400000, any stage record carries a different (or missing) as_of, the seed "
     "is not 20260921, the live cache reads touched, or the substrate moved off the "
     "frozen snapshot",
     resume3_break, resume3_real),
    ("F-C10-RESUME-4", "every waiver of byte-reproducibility is NAMED, with a reason "
     "and evidence a reader can chase",
     "an exemption is missing a scope, a reason, a ruling status or evidence; its "
     "evidence numbers cannot be RE-DERIVED off the on-disk record it names — "
     "whatever file that is, and a file that does not exist, will not parse, or holds "
     "no such pair is itself the finding; ITS OWN suite (not the first exemption's) "
     "is missing, has no readable LEGS table, or imports no venue client; its exempted "
     "legs are not exactly the legs THAT suite declares venue-reaching; it names a leg "
     "that does not exist; THE LEDGER BLOCK OF THE STAGE IT EXEMPTS DOES NOT NAME THE "
     "EXEMPTED SUITE, so the exemption was validated against a suite that produced "
     "none of the records it covers; a stage is COMPLETE-VERIFIED while an exemption "
     "stands over its suite; or any fixture record drifts between runs with no "
     "exemption naming it",
     resume4_break, resume4_real),
    ("F-C10-RESUME-5", "PROGRESS.json is well-formed and HONEST",
     "a stage is missing one of {stage, status, as_of, artifact_shas, fixtures, "
     "blockers}; a status is not one of COMPLETE-VERIFIED / PARTIAL / ABSENT; a stage "
     "claiming COMPLETE-VERIFIED lists a blocker, has no fixture record, or carries a "
     "nonzero exit or a red leg; artifact_count disagrees with the recorded set; a sha "
     "is not 64 lowercase hex; a byte count is not positive; a stage name is "
     "duplicated; or live_cache_touched is not False",
     resume5_break, resume5_real),
    ("F-C10-RESUME-6", "STEP0_RECORD.json re-hashes against disk, git and the live port",
     "STEP0_RECORD.json is absent; any of its four STEP 0 source shas does not "
     "re-hash from disk now; its byte counts move; the twin's STEP 0 blob at "
     "d63592f does not hash to the literal of record or is unreachable; any of the "
     "twelve pins disagrees with the live port, with the Pine default, or with the "
     "recorded key order; ANY STEP 0 SOURCE'S DISK SHA HAS LEFT ITS STEP 0 LITERAL; "
     "the record is ABSENT and no --rewrite-step0-record was given; the Argus note's "
     "phantom 0.67 / DEV_RETURN 8 appears as a pin of record; [Q-R5] does not hold in "
     "the pinned set or in the live pine/ sweep; or a deterministic rebuild is not "
     "byte-identical to the filed file",
     resume6_break, resume6_real),
    ("F-C10-RESUME-T", "THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED",
     "a whole-suite run produces bytes that are not byte-identical to the filed "
     "FIXTURES_RESUME.txt and no --refile-transcript was given; or the filed artifact "
     "is overwritten by such a run; or the non-reproducing run's own bytes are not "
     "preserved in FIXTURES_RESUME_rerun.txt; or the guard fires on a run that IS "
     "byte-identical",
     resumeT_break, resumeT_real),
)


def main() -> int:
    global REWRITE_STEP0
    pick = [a for a in sys.argv[1:] if not a.startswith("--")]
    root = TC
    for a in sys.argv[1:]:
        if a.startswith("--root="):
            root = Path(a.split("=", 1)[1])

    # STEP0_RECORD is WRITE-ONCE here: written if absent, and otherwise only on an
    # explicit --rewrite-step0-record. F-C10-RESUME-6 then judges the FILED file
    # against a fresh rebuild, against disk, against git and against the live port
    # [LEAN R4]. A module that silently rewrote the file it checks would make its
    # own byte-reproducibility claim vacuous.
    rewrite = "--rewrite-step0-record" in sys.argv[1:]
    refile = "--refile-transcript" in sys.argv[1:]
    REWRITE_STEP0 = rewrite
    if rewrite:
        STEP0_RECORD_PATH.parent.mkdir(parents=True, exist_ok=True)
        STEP0_RECORD_PATH.write_bytes(_step0_bytes(build_step0_record()))
        born = "REWRITTEN on --rewrite-step0-record"
    elif STEP0_RECORD_PATH.exists():
        born = "read as filed (write-once; --rewrite-step0-record to refresh)"
    else:
        # DELETE-AND-RERUN MAY NOT LAUNDER A SOURCE CHANGE. This branch used to
        # write the record silently from whatever the tree looked like, which
        # made the whole write-once discipline removable with one `rm`.
        born = ("ABSENT and NOT regenerated — a record that reappears on demand pins "
                "nothing; --rewrite-step0-record to re-file it deliberately")

    say("=" * 78)
    say("TIER-C10 · F-C10-RESUME — THE LAW OF RESUMPTION, MADE ENFORCEABLE")
    say("=" * 78)
    prog = load_progress()
    psha, pn = file_sha(PROGRESS_PATH)
    say(f"  ledger   research_outputs/tierc10/PROGRESS.json  {pn:,} B  sha {psha}")
    say(f"  as_of_last_closed_4h {prog.get('as_of_of_record')}  ·  close_ms "
        f"{prog.get('as_of_last_closed_4h_close_ms')}  ·  seed {prog.get('seed')}")
    say(f"  substrate {prog.get('substrate')}  ·  branch {prog.get('branch')}  ·  "
        f"head {str(prog.get('head'))[:12]}")
    say(f"  contract  {(prog.get('contract_of_record') or {}).get('path')}  sha "
        f"{str((prog.get('contract_of_record') or {}).get('sha256'))[:16]}…")
    n_c = sum(1 for s in prog["stages"] if s["status"] == "COMPLETE-VERIFIED")
    n_p = sum(1 for s in prog["stages"] if s["status"] == "PARTIAL")
    n_a = sum(1 for s in prog["stages"] if s["status"] == "ABSENT")
    say(f"  ledger   {len(prog['stages'])} stage(s): {n_c} COMPLETE-VERIFIED, "
        f"{n_p} PARTIAL, {n_a} ABSENT · "
        f"{sum(len(s['artifact_shas']) for s in prog['stages']):,} artifact sha(s)")
    if STEP0_RECORD_PATH.exists():
        s0sha, s0n = file_sha(STEP0_RECORD_PATH)
        say(f"  step0    research_outputs/tierc10/STEP0_RECORD.json  {s0n:,} B  "
            f"sha {s0sha}")
    else:
        say(f"  step0    research_outputs/tierc10/STEP0_RECORD.json  ABSENT — this "
            f"module REFUSES to regenerate it [F-C10-RESUME-6]")
    clock(f"  step0    {born}")
    say(f"  NOTHING HERE RIDES A BAR. No lane, no verdict, no scored P-* row — "
        f"bookkeeping mechanics only.")
    say("")
    for s in LEANS:
        say(f"  {s}")

    chosen = [f for f in FIXTURES
              if not pick or any(q.lower() in f[0].lower() for q in pick)]
    for name, title, fails_if, b, r in chosen:
        prove(name, title, fails_if, b, r)

    say("")
    say("=" * 78)
    say(f"  {len(PASSED)} GREEN, {len(FAILED)} RED "
        f"({len(chosen)} fixture(s) run)")
    for f in FAILED:
        say(f"    RED: {f}")
    say("=" * 78)
    name = TRANSCRIPT if not pick else TRANSCRIPT.replace(".txt", "_partial.txt")
    root.mkdir(parents=True, exist_ok=True)
    out = root / name
    body = ("\n".join(LINES) + "\n").encode("utf-8")
    rc = 1 if FAILED else 0
    clobber = file_transcript(out, body, refile)
    if clobber:
        clock(f"\n  F-C10-RESUME-T — THE TRANSCRIPT OF RECORD · RED")
        clock(f"    FAILS IF: a whole-suite run produces a transcript that is not "
              f"byte-identical to the filed one.")
        for f in clobber:
            clock(f"    {f}")
        clock(f"    Understand the delta, then re-file deliberately with "
              f"--refile-transcript.")
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
