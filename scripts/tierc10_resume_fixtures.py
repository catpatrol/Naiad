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
                  hides a re-recorded sha [LEAN R10].  A FOURTH LOOP applies the
                  same rule ONE LEVEL DOWN, at the FIXTURE RECORD and at the
                  STAGE'S OWN ADMISSIONS, over every stage at HEAD REGARDLESS OF
                  STATUS (standing down only where loops 2-3 already demand the
                  strictly stronger BYTE-IDENTITY):
                  NO ADMISSION THAT REACHED THE COMMIT RECORD MAY BE TAKEN BACK
                  BY AN EDIT NOBODY COMMITTED [LEAN R17, widened to its general
                  shape by R18].  The anchored vocabulary is named in
                  ADMISSION_FIELDS — a transcript drift, a nonzero exit_code, a
                  legs_red count, a named red leg, a wall clock, a stage's
                  blockers list by COUNT, and a PARTIAL stage un-claimed to
                  ABSENT — and a record at HEAD may not VANISH from the working
                  tree, its whole block being gone counting as gone.  WITHDRAWAL
                  ONLY: a new drift, a NEW failure, a red leg newly NAMED, a
                  costlier run, an added blocker, an appended record, a born
                  stage and a CLAIMED stage are a build advancing, and eight
                  controls assert each of them is SILENT.  AND IT NEVER RAISES —
                  every run drives a WHOLE GRID of twelve deletion shapes across
                  every stage and demands a NAMED FINDING, never an exception,
                  from each [LEAN R18].
  F-C10-RESUME-S  THE SELF-ANCHOR.  This module carries PINNED_LEDGER_SHA,
                  PINNED_LEDGER_REV, the two LAW-2 quarantine literals, the
                  EXEMPTIONS registry and its breadth law, the STEP 0 pins, the
                  root allowlist and the corridor constants — and until round 3
                  it never read its own bytes.  It is now TRACKED, and this leg
                  demands that the bytes being EXECUTED are the bytes that are
                  COMMITTED.  Planted: eight one-edit bends of a copy of the
                  HEAD blob (the ledger anchor sha, its rev, a quarantine sha,
                  the re-widened waiver, a lowered breadth floor, a widened
                  allowlist, STEP0_COMMIT, the corridor's close_ms), a
                  whitespace-only edit, an untracked path, three unreachable
                  revs and a vanished subject.  THE LIMIT IS PRINTED IN THE
                  TRANSCRIPT: a self-anchor against HEAD cannot catch an edit
                  that is itself committed.
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
  F-C10-RESUME-4  THE VENUE EXEMPTION IS NAMED, BOUND AND NARROW.  Every waiver of
                  byte-reproducibility is a record with a scope, a reason and
                  EVIDENCE that is corroborated on disk; the exempted legs are
                  exactly the legs the exempted suite itself declares as
                  venue-reaching; THE EXEMPTED SUITE IS THE ONE THE EXEMPTED
                  STAGE'S OWN LEDGER BLOCK NAMES [LEAN R11]; and no stage is
                  COMPLETE on an exemption's strength.  Planted: an empty reason,
                  a sourceless evidence block, a bent number, an unexempted
                  drifting suite, a leg that does not exist, a stage promoted
                  while its exemption stands, a BORROWED SUITE — a verbatim
                  copy of the real waiver re-pointed at another stage — and
                  FOUR WIDENED PATTERNS, each the real waiver with one string
                  changed ('', 'TIER-C10', 'D-CORE' and the stage-name substring
                  this file shipped in round 2), judged both on their own fields
                  and on the real drift they were planted over [LEAN R12].
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
  F-C10-RESUME-T  THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED, AND NEVER
                  QUIETLY REPLACED BY DELETING IT.  A whole-suite run that does
                  not reproduce the filed FIXTURES_RESUME.txt to the byte writes
                  FIXTURES_RESUME_rerun.txt, prints the delta, LEAVES the
                  artifact of record untouched and exits 1.  An ABSENT artifact
                  of record is a NAMED FINDING, not a blank page to fill: it is
                  written only on an explicit --refile-transcript.  AND IT IS
                  ANCHORED: the filed transcript is TRACKED and judged against
                  its own HEAD blob, so an erasure or an uncommitted replacement
                  is named rather than passed [LEAN R19].  Planted: a
                  non-reproducing run, a truncated run, an empty run, an appended
                  byte, the absent-artifact escape, an untracked anchor path, an
                  unreachable rev, a bent artifact, an erased artifact.

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
# the artifact of record's repo-relative path. F-C10-RESUME-T anchors on the
# HEAD BLOB of this path the way F-C10-RESUME-0 anchors on PROGRESS.json's: the
# tierc10 tree is gitignored, so the orchestrator commits it with `git add -f`,
# exactly as PROGRESS.json is tracked. [LEAN-HEPHAESTUS] R19
TRANSCRIPT_REL = "research_outputs/tierc10/FIXTURES_RESUME.txt"

# ── THE EXTERNAL ANCHOR ────────────────────────────────────────────────────
# F-C10-RESUME-1, -4 and -5 all read their answer out of PROGRESS.json, so a
# builder who edits PROGRESS.json defeats all three with one line: re-record a
# tampered artifact's sha, promote a blockered stage, de-record an artifact.
# PROGRESS.json IS TRACKED (committed at f97cded despite .gitignore), so an
# answer exists OUTSIDE the working tree, and the pinned sha is typed here as a
# module literal so the anchor itself is pinned and not merely "whatever git
# says today".  F-C10-RESUME-0 is that check.  [LEAN-HEPHAESTUS] R5
PINNED_LEDGER_REV = "2e92972"
PINNED_LEDGER_SHA = "f0908960e3764aadf45b3544c9e9cc084fdac0b0b98b35ce616af069f39976ba"

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
    # ORCHESTRATOR RULING OF 2026-09-22 (a RULING, not a lean, and not a
    # weakening). research_outputs/tierc10/REGISTRATION_PLAN.md is a FILED BUILD
    # DOCUMENT of exactly the same class as the four names above: Stage B's
    # structural plan, filed 2026-09-22 and COMMITTED at 54cfd60, pinning the
    # panel / era / ruler / base / runner / LOAO line of all six registrations
    # BEFORE any text is written. The executor refused to silence the standing
    # RED unilaterally and was right to; the operator ruled the file admissible.
    # NOTE THE PRICE OF ADMITTING IT: this tuple is itself under the self-anchor
    # F-C10-RESUME-S, so adding a name to it is NOT a free edit — it reaches a
    # GREEN run only through the commit record, where a reviewer can diff it.
    "REGISTRATION_PLAN.md",
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

# ── EVERY FILE THAT MAY JOIN THE EXEMPTION CHAIN, RECORDED.  [LEAN R16]
#    NOTHING IN THIS SUITE SWEPT scripts/ — that was the hole that made the
#    review's second forgery cheap.  It built a full symlink mirror of the repo,
#    ADDED ONE FILE under scripts/, and that file bound itself to a stage for
#    free because `_binding_field` matched by substring and no leg ever asked
#    whether a scripts/ file was RECORDED anywhere at all.
#
#    WHAT "RECORDED" MEANS HERE, AND WHY.  Two registers, BOTH required, neither
#    of which a working-tree edit can write:
#      · THE GIT INDEX — `git ls-files` must know the path.  This is the primary
#        register because it is the one answer that exists OUTSIDE the working
#        tree; an added file is free, `git add` is not, and a COMMIT (which the
#        exemption chain additionally requires, below) is less free still.
#      · THIS MODULE LITERAL — a name typed here, under F-C10-RESUME-S, so a new
#        participant cannot APPEAR without an edit that must itself be committed
#        before any run of this suite goes green.
#    REJECTED: PROGRESS.json (it records research_outputs/ artifacts, not code,
#    and it is the very document under audit — recording the auditor's inputs in
#    the audited file is the circle this track exists to break) and RF_CODE_FILES
#    (that tuple is STEP 0's RangeFinder pin and means something else entirely;
#    overloading it would make leg 6 red for reasons with nothing to do with
#    STEP 0, which is the exact mistake [LEAN R6] was written to undo).
#
#    THE COST, STATED: a teammate who adds a new scripts/tierc10_*.py turns this
#    leg RED until the name is added here and committed. That is the leg working.
TC_SUITE_GLOB = "tierc10_*.py"
TC_SUITE_FILES = (
    "scripts/tierc10_brk.py",
    "scripts/tierc10_brk_fixtures.py",
    "scripts/tierc10_census.py",
    "scripts/tierc10_census_fixtures.py",
    "scripts/tierc10_close_close_box_cost.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_census_r.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_findings.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_ledger_append.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_s0_verdicts.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_stage_d.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_close_stage_log.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_forward_strip.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_ledger_append_root.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_p_age_1_tide_youth.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_p_trg_2_seen_share.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_regime_prior.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_regime_prior_fixtures.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_close_v6_control_twin.py",   # CLOSE (2026-09-23)
    "scripts/tierc10_data.py",
    "scripts/tierc10_data_fixtures.py",
    "scripts/tierc10_file_registrations.py",   # Stage B's filer (371123f)
    "scripts/tierc10_lanes.py",
    "scripts/tierc10_lanes_fixtures.py",
    "scripts/tierc10_null.py",
    "scripts/tierc10_null_fixtures.py",
    "scripts/tierc10_panel.py",
    "scripts/tierc10_panel_fixtures.py",
    "scripts/tierc10_resume_fixtures.py",
    "scripts/tierc10_rf_fixtures.py",
    "scripts/tierc10_score.py",                # Stage B's scoring driver
    "scripts/tierc10_score_fixtures.py",
    "scripts/tierc10_stamps.py",
    "scripts/tierc10_stamps_fixtures.py",
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
#
# ── THE BREADTH OF A WAIVER IS POLICED, NOT TRUSTED [LEAN-HEPHAESTUS] R12 ──
# covers_record_match used to be checked for being DEAD (matching no record) and
# for nothing else. Nothing checked it for OVER-matching, so one widened string
# on an otherwise legitimately-bound exemption was a blanket escape over its
# whole stage. MEASURED against the real, properly-bound X-STAGE-D-VENUE:
#   covers_record_match = ("",)         -> 0 findings, a planted drift silenced
#   covers_record_match = ("TIER-C10",) -> 0 findings, a planted drift silenced
# Both cleared field presence (a non-empty tuple is truthy), both cleared the
# dead-pattern check (each matches at least one record), both cleared the legs,
# venue-client, evidence and R11-binding checks. The two floors below are the
# breadth law; `_coverage_findings` enforces them.
COVERAGE_MIN_CHARS = 4
TIER_WIDE_TOKENS = (
    "TIER-C10", "TIER C10", "TIERC10", "tierc10", "TC10",
    "research_outputs/tierc10", "NAIAD", "fixtures", "FIXTURES", "suite",
)
EXEMPTIONS = (
    {
        "id": "X-STAGE-D-VENUE",
        "suite": "scripts/tierc10_data_fixtures.py",
        "stage": "D-CORE",
        "transcript": "research_outputs/tierc10/data/FIXTURES_STAGE_D.txt",
        # ── THE WAIVER IS BOUND TO THE WAIVED LEGS, NOT TO A STAGE NAME ──
        # the substring(s) by which a PROGRESS.json fixture record is recognised
        # as falling under this waiver. Each one must match at least one real
        # record of the named stage (or it is a DEAD pattern), and — the law
        # added in round 3 — every record it SELECTS must itself name one of
        # `legs` below, which are in turn forced to be EXACTLY the legs the
        # suite's own LEGS table declares venue-reaching.
        #
        # THE HOLE THIS CLOSES. This read ("Stage D fixtures",) — the stage's
        # NAME — and D-CORE carries TWO fixture records, both of which contain
        # that substring: the ONLINE run that fetches the venue AND the OFFLINE
        # run that, by its own name, reaches no venue API at all. MEASURED: a
        # drift planted on the OFFLINE record yielded 0 findings, and so did
        # transcript_sha_after='9'*64 on it. The waiver exists ONLY because
        # F-D-1/F-D-1b fetch from a venue that backfills; it may not cover the
        # offline run. ("F-D-1",) selects the ONLINE record alone — the OFFLINE
        # record does not name F-D-1 and is no longer silenced (1 finding).
        # [LEAN-HEPHAESTUS] R12
        "covers_record_match": ("F-D-1",),
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

# ══ RULINGS OF RECORD ═══════════════════════════════════════════════════════
# NOT LEANS. A lean is an executor's reading, offered for the operator to
# overturn. A ruling is the operator's answer, and it binds this module.
RULINGS = (
    "[RULING · ORCHESTRATOR · 2026-09-22] REGISTRATION_PLAN.md IS A FILED BUILD "
    "DOCUMENT. F-C10-RESUME-1's root sweep [LEAN R7] stood RED on "
    "research_outputs/tierc10/REGISTRATION_PLAN.md: a loose file in the tierc10 "
    "root that no stage records and TC_ROOT_ALLOWLIST did not carry. The executor "
    "refused to silence it unilaterally — adding a name to an escape list to make "
    "one's own suite green is the exact move this track exists to catch — and put "
    "it to the operator. THE RULING: REGISTRATION_PLAN.md is a filed build "
    "document of EXACTLY the same class as the four names already in the list "
    "(BUILD_DRAFT.md, OPERATOR_RULINGS.md, PROGRESS.json, STEP0_RECORD.json). It "
    "is Stage B's structural plan, filed 2026-09-22 and COMMITTED at 54cfd60, "
    "pinning the panel / era / ruler / base / runner / LOAO line of all six "
    "registrations BEFORE any text is written. It is therefore ADMITTED to "
    "TC_ROOT_ALLOWLIST. THE RED IS RESOLVED BY RULING, NOT BY WEAKENING, AND HERE "
    "IS WHY THAT DISTINCTION IS CHECKABLE RATHER THAN RHETORICAL: "
    "TC_ROOT_ALLOWLIST is itself under the self-anchor F-C10-RESUME-S, so adding "
    "a name to it is NOT a free edit — it reaches a green run only through the "
    "commit record, where a reviewer can diff it, and F-C10-RESUME-S's break leg "
    "plants a WIDENED ROOT ALLOWLIST and proves that plant goes RED. The escape "
    "list is still a list of five named files, still swept non-recursively "
    "against the union of every recorded artifact, and every other loose file in "
    "that directory is still a finding.",
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
    "[LEAN-HEPHAESTUS] R12 A WAIVER IS BOUND TO THE WAIVED LEGS, NOT TO A STAGE-NAME "
    "SUBSTRING. Round 2 shipped covers_record_match=('Stage D fixtures',) — the STAGE'S "
    "OWN NAME — and D-CORE carries TWO fixture records, BOTH of which contain it: the "
    "ONLINE run that fetches the venue AND the OFFLINE run that, by its own name, "
    "reaches no venue API at all. MEASURED against the real unwidened registry: a drift "
    "planted on the OFFLINE record gave 0 findings, and so did transcript_sha_after="
    "'9'*64 on it — a blanket escape over all of D-CORE, and the leg's own NEGATIVE "
    "CONTROL certified it as healthy, because a negative control alone cannot tell a "
    "narrow waiver from a blanket one. WORSE, breadth was ENTIRELY UNPOLICED: the only "
    "test on a pattern was that it is not DEAD. Taking the real, properly-bound "
    "X-STAGE-D-VENUE and changing ONE string, covers_record_match=('',) and "
    "('TIER-C10',) each scored 0 findings and each silenced a planted drift, clearing "
    "field presence (a non-empty tuple is truthy), the dead-pattern check (each matches "
    "at least one record), the legs, venue-client, evidence and R11-binding checks. "
    "THE FIX IS A LAW, NOT A VALUE. The registry now reads ('F-D-1',), and "
    "_coverage_findings makes the narrowing enforceable: (a) a pattern must be at "
    "least COVERAGE_MIN_CHARS=4 characters and may not be a substring of its stage's "
    "own name nor of any of the 10 tier-wide tokens; (b) EVERY record a pattern "
    "SELECTS must NAME one of the waived legs. I chose leg-naming over an explicit "
    "covers_record_ids list: an id list is more PRECISE but not STRONGER — it is a "
    "second free author-written field with nothing outside the registry corroborating "
    "it, so widening it is exactly as cheap as widening covers_record_match was, and "
    "the hole moves rather than closes. x['legs'] is already forced to equal EXACTLY "
    "the set the exempted suite's OWN LEGS table declares venue-reaching, parsed out "
    "of that suite's source with ast — so widening the waiver's reach now requires a "
    "ledger record to name a leg AND a foreign suite's source to declare that leg "
    "venue-reaching, a chain no single string in this file can forge. A POSITIVE "
    "CONTROL was added beside the negative one: a drift is planted, one at a time, on "
    "every record of an exempted stage the registry does NOT select, and each must be "
    "SPOKEN ALOUD. Eight new plants, including the round-2 value itself. THE LIMIT: (b) "
    "reads the record's NAME, so a genuinely venue-reaching record whose name never "
    "spells its legs goes FALSE RED — a false red, not a false green. CROSS-TRACK "
    "REQUEST: keep a venue-reaching fixture record's suite string naming the legs that "
    "reach the venue, as D-CORE's ONLINE record already does.",
    "[LEAN-HEPHAESTUS] R13 THE MODULE NOW READS ITS OWN BYTES. R10 ended on 'it "
    "cannot defend itself against an edit to THIS FILE, where the pin and the three "
    "loops live' and fell back on 'only the commit record and a reader can catch that'. "
    "AT REVIEW TIME THERE WAS NO COMMIT RECORD — this module was untracked — so the "
    "fallback fell back to nothing, and the file that holds PINNED_LEDGER_SHA, "
    "PINNED_LEDGER_REV, the two LAW-2 quarantine literals, EXEMPTIONS and its breadth "
    "law, the STEP 0 pins, TC_ROOT_ALLOWLIST and the corridor constants used __file__ "
    "for exactly one thing: ROOT = Path(__file__).resolve().parents[1]. The module is "
    "now TRACKED (added at d8a6f81 on v12-v1-census) and F-C10-RESUME-S demands that "
    "the path be in the index, that its HEAD blob be readable, and that the bytes "
    "being EXECUTED be byte-identical to that blob. Fourteen plants: eight one-edit "
    "bends of a COPY OF THE HEAD BLOB (the plants are judged against the committed "
    "blob, not the working tree — a bent copy of an already-divergent working tree "
    "would go red for free and prove nothing), a whitespace-only edit, an untracked "
    "path, three unreachable revs and a vanished subject; the negative control is a "
    "copy of the HEAD blob at ZERO findings. THE LIMIT IS PRINTED IN THE TRANSCRIPT "
    "AND IT IS REAL: a self-anchor against HEAD cannot catch an edit that is ITSELF "
    "COMMITTED, nor a rewritten history that moves blob and working tree together. "
    "It cannot be repaired by pinning either — a literal holding the sha of the file "
    "that contains it is a fixed point no author can type. What this leg buys is "
    "narrow and worth having: an edit to any of the 15 pinned literals (TC_SUITE_FILES "
    "joined them in round 4) can no longer "
    "reach a GREEN run without first reaching the commit record, where a reviewer "
    "can diff it. OPERATOR / ORCHESTRATOR NOTE: this leg is RED for as long as the "
    "round-3 and round-4 repairs sit uncommitted in the working tree. That is the "
    "leg working, not the leg broken. Commit scripts/tierc10_resume_fixtures.py and "
    "re-run with --refile-transcript; the executor is forbidden to commit and "
    "cannot close it.",
    "[LEAN-HEPHAESTUS] R14 THE TIE IS ANCHORED, AND ONLY THE TIE. Floor (b) of the "
    "breadth law says every record an exemption's pattern SELECTS must NAME one of "
    "the waived legs. That tie is only as strong as the text it reads, and in round "
    "3 the text it read was a PARTIAL stage's WORKING-TREE prose — which "
    "F-C10-RESUME-0 deliberately leaves unanchored so a build in progress can "
    "advance. The review wrote that evidence for free. MEASURED: append the single "
    "clause ' (shares fixture plumbing with F-D-1)' to D-CORE's OFFLINE fixture "
    "record and a drift planted on that record goes from 1 finding to 0 — no module "
    "edit, no new file, one clause. The record then NAMES a waived leg (floor (b) "
    "satisfied) and the pattern then SELECTS it (the closure calls the drift "
    "covered). THE REPAIR: the FIELDS THE TIE READS — each selected fixture "
    "record's `suite` string, and the block the suite-to-stage binding is found in "
    "— are now read out of the COMMITTED PROGRESS.json at HEAD, for EVERY stage "
    "REGARDLESS OF STATUS. The pattern must select the record at HEAD too, and it "
    "must be the HEAD text that names the leg. The rest of a PARTIAL block stays "
    "free to move and a move in the anchored fields is REPORTED, not forbidden "
    "(the per-record IDENTICAL / CHANGED / NOT AT HEAD line is printed to stdout "
    "beside each exemption); it becomes a FINDING only when the change is what "
    "CREATES the tie. WHY NOT THE OTHER TWO OPTIONS. Deriving the tie from the "
    "suite's own AST does not reach: D-CORE's ONLINE and OFFLINE records are TWO "
    "RUNS OF THE SAME FILE, so no parse of scripts/tierc10_data_fixtures.py can "
    "tell them apart — what the AST already fixes is the LEG NAMES (x['legs'] is "
    "forced to equal the suite's own needs_net set), which left the RECORD TEXT as "
    "the only forgeable half, and that is the half anchored here. A STRUCTURED "
    "FIELD emitted by the suite is the better shape and this track cannot build it: "
    "PROGRESS.json is not ours to write. CROSS-TRACK REQUEST, FILED: have each "
    "fixture record carry an explicit `legs_reaching_venue: [...]` emitted by the "
    "suite itself, and (b) can read a field instead of a sentence. THE NEW LIMIT "
    "THIS INTRODUCES, STATED: a stage whose block is NOT YET AT HEAD cannot carry "
    "an exemption at all, and a legitimately new fixture record cannot tie one "
    "until it is committed. That is a false RED, not a false green, and it is the "
    "trade this house takes every time. AND THE OLD LIMIT IS UNCHANGED AND STILL "
    "TRUE: an anchor against HEAD cannot catch an edit that is ITSELF COMMITTED. "
    "Commit the forged clause and this guard is green on it. What the anchor buys "
    "is that the forgery must pass through the commit record first. AND THE "
    "MATCHING LIMIT, STATED: HEAD fixture-record counterparts are matched BY INDEX, so an INSERTION or a RE-ORDER of a stage's fixture records goes FALSE RED — a false red, not a false green, and the honest trade. The clean repair is a stable per-record id emitted by each suite, which is PROGRESS.json's to write and not this track's; FILED AS A CROSS-TRACK REQUEST. [LEAN R17]'s fourth loop matches the "
    "same way and INHERITS this limit verbatim.",
    "[LEAN-HEPHAESTUS] R15 THE BINDING MATCHES EXACTLY. `_binding_field` asked "
    "`stem in <the stage's block>` — a SUBSTRING test — so every name that merely "
    "SAT INSIDE a name the ledger did spell bound for free. MEASURED against "
    "D-CORE, whose blockers name scripts/tierc10_data_fixtures.py: a brand-new "
    "scripts/tierc10_dat.py (stem 'tierc10_dat') returned the binding field "
    "'blockers' though the ledger never names it once; the review proved the same "
    "thing on a full symlink mirror of the repo with one added file. The block is "
    "now TOKENISED and the suite matched as a WHOLE NAME — its full relative path, "
    "its basename or its stem — and nothing shorter. NOTE WHAT THIS DOES NOT DO: "
    "FRESH C2 reaches the same binding by APPENDING 'see "
    "scripts/tierc10_venue_extra.py' to D-CORE's unanchored blockers list, which is "
    "an exact name and which exact matching cannot touch. That one is closed by "
    "R14's HEAD anchor and by R16's sweep, not by this. Exactness is necessary "
    "here and it was never sufficient.",
    "[LEAN-HEPHAESTUS] R16 NOTHING SWEPT scripts/. Every sweep in this suite "
    "looked at research_outputs/tierc10 — the OUTPUT side — and the exemption "
    "chain runs through CODE: a waiver names a scripts/ file, that file's own LEGS "
    "table decides which legs may be waived, and its name is what the ledger must "
    "spell for the binding to hold. So a scripts/ file could APPEAR — untracked, "
    "recorded nowhere, named by nobody — and join that chain, which is exactly "
    "what the review built. WHAT 'RECORDED' MEANS, AND WHY: TWO REGISTERS, BOTH "
    "REQUIRED. (1) THE GIT INDEX — it is the one answer that exists OUTSIDE the "
    "working tree; adding a file is free, `git add` is not. (2) A MODULE LITERAL, "
    "TC_SUITE_FILES, which lives under F-C10-RESUME-S, so a new participant cannot "
    "appear without an edit that must be COMMITTED before this suite goes green. "
    "An exemption's own suite must additionally have a READABLE HEAD BLOB: the "
    "legs it may waive are read from that source, and an uncommitted source is a "
    "file only its author has seen. REJECTED AS THE REGISTER: PROGRESS.json, "
    "because it records research_outputs/ artifacts rather than code and because "
    "it is the very document under audit — recording the auditor's inputs in the "
    "audited file is the circle this track exists to break; and RF_CODE_FILES, "
    "because that tuple is STEP 0's RangeFinder pin and overloading it would turn "
    "leg 6 red for reasons with nothing to do with STEP 0, the exact mistake "
    "[LEAN R6] was written to undo. WHAT IS DELIBERATELY NOT CHECKED: the suites' "
    "CONTENT shas. Those files belong to other tracks and move under this one; "
    "their live shas stay on stdout only [LEAN R8]. THE COST, STATED PLAINLY: a "
    "teammate who adds a new scripts/tierc10_*.py turns this leg RED until the "
    "name is added here and committed. That is the leg working, not the leg "
    "broken, and it is one line under an anchor.",
    "[LEAN-HEPHAESTUS] R17 R14 ANCHORED THE WAIVER'S EVIDENCE AND LEFT THE "
    "FAILURE'S EVIDENCE FREE. Round 4 spent itself closing FORGERY 1 — appending "
    "' (shares fixture plumbing with F-D-1)' to D-CORE's OFFLINE fixture record, "
    "which bought a waiver over a real drift — and the whole time a cheaper move "
    "was open beside it and nowhere stated: DO NOT BUY A WAIVER, ERASE THE CLAIM. "
    "One boolean and one string copy inside a PARTIAL stage's block, no module "
    "edit, no new file, no exemption and no pattern: "
    "for f in D-CORE['fixtures']: if 'OFFLINE' in f['suite']: "
    "f['transcript_drift'] = False; f['transcript_sha_after'] = "
    "f['transcript_sha_before']. MEASURED through main(), load_progress() "
    "returning the tampered ledger and --root in a scratchpad: drift HONESTLY "
    "RECORDED -> exit 1, 7 GREEN 2 RED, leg 4 raising 2 findings; drift ERASED -> "
    "exit 1, 8 GREEN 1 RED, leg 4 PASS, leg 0 zero findings, leg 5 zero findings, "
    "and the erased run's transcript BYTE-IDENTICAL to the filed artifact of "
    "record. The leg round 4 was spent repairing stood GREEN over a real, hidden "
    "transcript drift, and this suite's own output carried no trace of it. ON THE "
    "IDENTICAL RECORD: forging the clause cost 2 findings, erasing the fields cost "
    "0 — the cheaper move was the one left open, and it is BROADER, because the "
    "forgery only ever worked on the one stage carrying an exemption while erasure "
    "works on all four non-complete stages. THE SECOND HALF, SAME ROOT: delete a "
    "PARTIAL stage's fixture record outright (LANES (B mech) 1 -> 0) and leg 4's "
    "REAL leg PASSES, leg 0 finds 0 and leg 5 finds 0; the suite goes red only on "
    "'F-C10-RESUME-4 (break leg did not go RED — fixture proves nothing)', which "
    "fired because LANES happens to be a break-leg plant subject. That is an "
    "ACCIDENT reporting that a fixture proved nothing, not a guard catching a "
    "tamper, and it would evaporate the moment the plant moved. THE REPAIR is "
    "leg 0's own third loop [LEAN R10] — 'a settled claim may not be QUIETLY "
    "WITHDRAWN' — applied ONE LEVEL DOWN, at the FIXTURE-RECORD level, using the "
    "same index-matching against the committed ledger that _coverage_findings "
    "already implements. For every stage REGARDLESS OF STATUS, working-tree "
    "record #i is paired with HEAD's record #i and a finding is raised on "
    "WITHDRAWAL ONLY: (i) HEAD's #i admits a transcript drift and the working "
    "tree's #i admits none — a claim that existed in the commit record and does "
    "not exist this afternoon; (ii) HEAD carries #i and the working tree does "
    "not — a record that was in the commit record and has vanished, which also "
    "gives LANES a REAL guard in place of the accidental one. 'Admits a drift' is "
    "read BOTH ways, the flag and the two shas disagreeing, because the attack "
    "rewrites both halves in one move; and a MISSING field reads as NO CLAIM, "
    "never as a claim of health. WITHDRAWAL-ONLY IS DELIBERATE AND IT KEEPS THE "
    "BUILD ADVANCING: a NEW drift appearing, a record being ADDED and a stage "
    "being BORN are normal progress and must not go red — that is the same trade "
    "[LEAN R5] made at the stage level — and all three are planted in the REAL "
    "leg as controls that must stay SILENT, because a guard that reddens on "
    "progress is a guard the next builder deletes, and they would be right to. "
    "Six plants prove both halves RED: the shas, the flag, the fields removed, "
    "the record deleted, the drifting record deleted, the whole block deleted; "
    "each is planted on a NON-COMPLETE stage, where the three loops above are "
    "silent by design, so nothing but the fourth loop can be what catches them. "
    "THE LIMIT INHERITED FROM R14, IN R14'S OWN WORDS: HEAD fixture-record "
    "counterparts are matched BY INDEX, so an INSERTION or a RE-ORDER of a "
    "stage's fixture records goes FALSE RED — a false red, not a false green, and "
    "the honest trade. The clean repair is a stable per-record id emitted by each "
    "suite, which is PROGRESS.json's to write and not this track's; FILED AS A "
    "CROSS-TRACK REQUEST. MEASURED, both halves: inserting one new D-CORE record "
    "at #0 and re-ordering D-CORE's two records each gave leg 4 ONE false-RED "
    "finding; and with a drift honestly carried forward, an insertion at #0 gave "
    "the fourth loop ONE false-RED finding. A PLAIN insertion with no drift at "
    "HEAD is SILENT here (0 findings), so this loop pays the index tax only where "
    "a drift claim is actually in play. AND A SECOND LIMIT THIS LOOP HAS, MEASURED "
    "AND STATED RATHER THAN IMPLIED: the pairing tests DRIFT-PRESENCE at an index, "
    "not RECORD IDENTITY, so SUBSTITUTING a different record that also admits a "
    "drift at the same index is 0 findings in this loop — the admission at #i "
    "survives, the record it belonged to does not. That substitution is NOT a free "
    "escape and the numbers say why: keeping the drift alive costs a leg-4 RED "
    "(measured, 1 finding: the substitute names no waived leg, so no exemption "
    "covers it), and dropping the drift costs a leg-0 RED (measured, 1 finding: it "
    "is then an ordinary erasure). The only silent substitution is one that keeps "
    "a drift admission alive AND gets it exempted, which is the chain [LEAN R11], "
    "[LEAN R14], [LEAN R15] and [LEAN R16] already police. Closing it here would "
    "mean demanding a record's TEXT never change, which would go false RED on "
    "every legitimate rename; the reviewer's WITHDRAWAL-ONLY shape is deliberately "
    "narrower than that, and this is the price of the shape, named. THE LIMIT THIS LOOP ADDS: it anchors on HEAD like every "
    "other loop here, so a drift that appears and is erased BETWEEN TWO COMMITS "
    "leaves no committed claim to withdraw and this guard never sees it, and an "
    "erasure that is ITSELF COMMITTED is a commit's act, which this fixture does "
    "not judge. What the anchor buys is that the erasure must pass through the "
    "commit record first, where a reviewer can diff it.",
    "[LEAN-HEPHAESTUS] R18 R17 ANCHORED ONE ADMISSION AND CRASHED ON THE REST. "
    "TWO DEFECTS, ONE SHAPE. (a) THE LOOP RAISED INSTEAD OF ACCUSING. Driving the "
    "deletion attacks R17 had just repaired — delete a record at #0, at the end, "
    "the only record, the whole fixtures list, the whole stage block — produced "
    "KeyError: 'BRK (B mech)', KeyError: 'fixtures', KeyError: 0, IndexError and "
    "TypeError in place of the accusation AND the whole evidence block. MEASURED: "
    "every one of the 8 deletion shapes on the stage that sorts first crashed "
    "resume0_real, because the withdrawal-only CONTROLS indexed a HEAD-derived "
    "stage name into the DISK document, and every plant in resume0_break crashed "
    "with it, so the break leg went NOT-RED — void — in exactly the state where a "
    "break leg matters. An exception name where a finding should be is "
    "indistinguishable from a bug in the fixture. (b) THE SCOPE SENTENCE WAS "
    "FALSE. Leg 0 printed 'CANNOT judge a stage that is COMPLETE-VERIFIED on "
    "NEITHER side … this leg says nothing about them' while the fourth loop was "
    "judging exactly those stages; a reader trusting that sentence would have "
    "believed the opposite of what the code did. THE REPAIR IS THE GENERAL SHAPE, "
    "NOT ONE MORE FIELD: no admission that reached the commit record may be taken "
    "back by an edit nobody committed — it may APPEAR, it may GROW, it may not "
    "SHRINK or VANISH — over a NAMED vocabulary (drift, exit_code, legs_red, "
    "red_leg_names, wall_seconds, the stage's blockers by COUNT, PARTIAL "
    "un-claimed to ABSENT). THE RESIDUE WAS NOT HYPOTHETICAL: the committed "
    "ledger carries ONE live admission of failure, D-CORE's ONLINE record at exit "
    "1 with 1 red leg, and on the R17 shape erasing it cost 0 findings, emptying "
    "all 23 blockers cost 0, un-claiming a PARTIAL stage cost 0 — the reviewer's "
    "8 GREEN / 1 RED was the same count the pre-R17 ERASE attack produced. On the "
    "R18 shape: 2, 4 and 1. TOTALITY IS NOW ASSERTED, NOT CLAIMED: every run "
    "drives 12 deletion shapes against all 9 stages and demands a NAMED finding "
    "and no exception from every cell that changes the ledger; it caught a real "
    "hole on its first run (a record replaced by a non-dict was silent whenever "
    "the record admitted nothing) and that is repaired. WITHDRAWAL ONLY IS "
    "ASSERTED TOO: 8 controls run the leg over a build ADVANCING and every one is "
    "silent. WHAT IS STILL OPEN IS STATED AND PRICED IN THE TRANSCRIPT: index "
    "matching (and its use as CAMOUFLAGE — an attacker can provoke the known "
    "false RED on purpose until a reader learns to wave the leg through), "
    "admission-presence-at-an-index rather than record identity, a vocabulary "
    "that is a list, and blockers matched by COUNT. All four share one clean "
    "repair — a stable per-record id emitted by each suite — which is "
    "PROGRESS.json's to write and NOT this track's. CROSS-TRACK REQUEST, FILED.",
    "[LEAN-HEPHAESTUS] R19 TWO HOLES AT THE EDGES OF A SUITE THAT WAS TOTAL IN "
    "THE MIDDLE. (a) main()'s HEADER WAS NOT TOTAL, so the process died before "
    "any fixture ran. R18 made anchor_findings, resume0_real and resume0_break "
    "total and drove 12 deletion shapes x 9 stages through them; the header "
    "above them still read prog['stages'], s['status'] and s['artifact_shas'] "
    "directly. MEASURED THROUGH main(): 40 of 45 cells gave leg-0 RED with a "
    "named finding and 5 DIED — KeyError: 'stages', and TypeError: string "
    "indices must be integers on EVERY stage for 'the stage ROW is not an "
    "object'. THE CONSEQUENCE WAS THE WORST AVAILABLE ONE: a traceback, no leg, "
    "no accusation, F-C10-RESUME-T never reached, and NO TRANSCRIPT WRITTEN AT "
    "ALL — so the stale FIXTURES_RESUME.txt stood as the artifact of record "
    "while the ledger it describes had been gutted. The header now reads the "
    "ledger exactly as the display loop does: _stage_list(), isinstance-guarded "
    ".get(), an UNREADABLE row printed for a stage row that is not an object, "
    "and a named line for a ledger that is not an object at all. RE-MEASURED "
    "THROUGH main() AFTER THE REPAIR: 12 shapes x 9 stages = 108 cells, plus 3 "
    "whole-ledger shapes; 0 crashes. (b) THE ABSENT-TRANSCRIPT ESCAPE. The "
    "no-clobber guard of R9 answered 'may this run overwrite the filed "
    "transcript?' and never 'is the filed transcript still there?'. MEASURED: "
    "with a foreign filed transcript present the guard was correct — RED, the "
    "delta named, the artifact preserved, the run diverted to "
    "FIXTURES_RESUME_rerun.txt; after `rm FIXTURES_RESUME.txt "
    "FIXTURES_RESUME_rerun.txt` the SAME run went SILENT, ZERO findings "
    "anywhere, '[NEW]' on stdout only, and its own bytes became the artifact of "
    "record. Total cost: one rm of a file git does not track. AND THE [PASS] "
    "LINE WAS OVERSTATED — it called --refile-transcript 'the one deliberate, "
    "named escape' while the ABSENT branch was a second escape needing no flag; "
    "a sentence claiming a scope the code lacks is worse than the hole it "
    "hides. BOTH HALVES TAKEN: the ABSENT branch now REFUSES and names the "
    "absence as a finding, mirroring STEP0_RECORD.json's refusal, and the "
    "artifact of record is ANCHORED on its own HEAD blob the way the ledger is "
    "— the orchestrator commits it with `git add -f`, the tierc10 tree being "
    "gitignored exactly as it is for PROGRESS.json. An erasure, an uncommitted "
    "replacement, an untracked path and an unreachable blob are four named "
    "findings where there was one blank page. THE PRICE, STATED: this leg now "
    "shares F-C10-RESUME-S's standing one-step-behind condition — a re-file "
    "moves the working tree ahead of the blob until the next commit, and a run "
    "inside that window is a FALSE RED, never a false green. NO SHA OF THE "
    "TRANSCRIPT PATH IS PRINTED ON THE GREEN PATH: the next commit makes this "
    "file that blob, so a line carrying the blob's sha would have to contain "
    "the sha of the bytes containing it. The VERDICT is printed instead, which "
    "is a fact about two files that both existed before the run and converges "
    "in one commit.",
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


def stage_root(recorded: dict) -> str | None:
    """The stage's own directory: the common parent of its recorded artifacts.

    None for a stage that RECORDS NOTHING.  A stage may legitimately record no
    artifact — F-C10-RESUME records none, because its only artifact is THIS
    suite's own transcript and a ledger recording the sha of the transcript that
    audits it does not converge (measured: re-file -> sha moves -> the record is
    stale -> leg 1 red -> the next run differs -> re-file).  os.path.commonpath
    RAISES on an empty sequence, and a guard that raises instead of accusing
    tells a reader nothing — the same defect round 7 repaired in main()'s header.
    The caller sweeps no directory for such a stage and says so."""
    parents = {str(Path(p).parent) for p in recorded}
    if not parents:
        return None
    return os.path.commonpath(sorted(parents)).replace(os.sep, "/")


# ═══════════════════════════ F-C10-RESUME-0 · THE EXTERNAL ANCHOR
def _jb(v) -> str:
    return json.dumps(v, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _stage_bytes(stage: dict) -> bytes:
    """A stage block's CANONICAL bytes — key-order independent, so comparing two
    ledgers compares CONTENT and never formatting."""
    return _jb(stage).encode("utf-8")


def _drifted(rec) -> bool:
    """DOES THIS FIXTURE RECORD ADMIT A TRANSCRIPT DRIFT?

    Read TWO ways, because the erasure attack rewrites both halves in one move
    and either half left standing is still a claim: the record's own
    `transcript_drift` flag, and the DISAGREEMENT of the two shas it records.
    A record carrying neither is NOT drifted — the absence of the fields is the
    absence of a claim, never a claim of health."""
    if not isinstance(rec, dict):
        return False
    if rec.get("transcript_drift"):
        return True
    b, a = rec.get("transcript_sha_before"), rec.get("transcript_sha_after")
    return bool(b) and bool(a) and b != a


def _stage_list(doc) -> tuple[list, str | None]:
    """A LEDGER'S STAGE ROWS, TOTAL.  Returns the list to walk and, when the
    document does not carry one, a NAMED description of what it carries instead.

    NOTHING IN THIS FAMILY RAISES.  [LEAN R18]  A guard that raises instead of
    accusing tells the reader nothing, and an exception name where a finding
    should be is indistinguishable from a bug in the fixture itself — so every
    malformed shape below becomes a NAMED FINDING and never a traceback."""
    if not isinstance(doc, dict):
        return [], f"the ledger is {type(doc).__name__}, not an object"
    s = doc.get("stages")
    if isinstance(s, list):
        return s, None
    if s is None:
        return [], "the ledger has no 'stages' key at all"
    return [], f"the ledger's 'stages' is {type(s).__name__}, not a list"


def _stages_by_name(doc) -> dict:
    rows, _ = _stage_list(doc)
    return {s.get("stage"): s for s in rows if isinstance(s, dict)}


def _malformed_rows(doc, side: str) -> list[str]:
    """The rows `_stages_by_name` HAD TO DROP, named.  A stage row that is not an
    object carries no stage name, so every by-name comparison in this leg looks
    straight past it and its absence reads as health — which is precisely what a
    deletion buys.  It is named here instead."""
    rows, why = _stage_list(doc)
    out: list[str] = []
    if why:
        out.append(f"{side}: {why} — a ledger this leg cannot walk is a ledger "
                   f"that cannot contradict anything, and silence is not health")
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            out.append(f"{side}: stage row #{i} is {type(row).__name__}, not an "
                       f"object — it carries no stage name, so every by-name guard "
                       f"in this leg looks straight past it and the stage it "
                       f"replaced reads as simply absent")
    return out


def _reclist(stage) -> tuple[list, str | None]:
    """A STAGE'S FIXTURE RECORDS, TOTAL.  Returns the list to pair over and, when
    the block does not carry one, a NAMED description of what it carries instead.

    EVERY DELETION SHAPE ARRIVES HERE: a missing 'fixtures' key, a null, a dict
    or a string in place of the list, a short list, an empty list.  Each returns
    a list and a name; none raises."""
    if not isinstance(stage, dict):
        return [], f"the stage entry is {type(stage).__name__}, not an object"
    if "fixtures" not in stage:
        return [], "the stage block has NO 'fixtures' key at all"
    f = stage["fixtures"]
    if isinstance(f, list):
        return f, None
    if f is None:
        return [], "the stage block's 'fixtures' is null"
    return [], (f"the stage block's 'fixtures' is {type(f).__name__}, not a list, "
                f"so it holds no records this leg can pair against HEAD's")


def _blockerlist(stage) -> tuple[list, str | None]:
    """A STAGE'S BLOCKERS, TOTAL.  Same contract as `_reclist`."""
    if not isinstance(stage, dict):
        return [], f"the stage entry is {type(stage).__name__}, not an object"
    if "blockers" not in stage:
        return [], "the stage block has NO 'blockers' key at all"
    b = stage["blockers"]
    if isinstance(b, list):
        return b, None
    if b is None:
        return [], "the stage block's 'blockers' is null"
    return [], f"the stage block's 'blockers' is {type(b).__name__}, not a list"


# ══ WHAT A LEDGER CAN CONFESS, AND THE ONE DIRECTION IT MAY MOVE [LEAN R18] ══
# The fourth loop was born anchoring ONE admission — a transcript drift — and a
# review measured exactly what that left standing: 8 GREEN, 1 RED, the identical
# count the round-5 ERASE attack produced BEFORE it was repaired, because
# exit_code, legs_red, red_leg_names, wall_seconds and the stage's whole blockers
# list were all still free to be taken back by an uncommitted edit, and a stage
# could move PARTIAL -> ABSENT with nothing said.
#
# THE REPAIR IS THE GENERAL SHAPE, NOT ONE MORE FIELD: AN ADMISSION THAT REACHED
# THE COMMIT RECORD MAY NOT BE TAKEN BACK BY AN EDIT NOBODY COMMITTED.  It may
# APPEAR, it may GROW, it may not SHRINK or VANISH.
#
# THE VOCABULARY IS A NAMED LIST AND THAT IS ITSELF A LIMIT — a confession made
# in a field not named here is not anchored.  It is stated and measured on the
# LIMIT lines in resume0_real, not left for a reader to discover.
ADMISSION_FIELDS = ("transcript_drift/transcript_sha_before/transcript_sha_after",
                    "exit_code", "legs_red", "red_leg_names", "wall_seconds",
                    "blockers (stage-level, by COUNT)", "status (PARTIAL -> ABSENT)")


def _num(v):
    """A real number, or None.  A bool is not a number and the string '3' is not
    a number: a field whose TYPE changed has stopped saying what it said, and the
    callers read that as a withdrawal rather than coerce it into agreement."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return v


def _nameset(v) -> set:
    """The set of NAMED failures a field carries, out of whatever shape it is."""
    if isinstance(v, str):
        return {v}
    if isinstance(v, (list, tuple, set)):
        return {str(x) for x in v}
    return set()


def _record_admissions(rec) -> list[str]:
    """EVERY ADMISSION a fixture record makes, rendered for a reader.  Used to
    say what a DELETED or UNREADABLE record was carrying when it went."""
    if not isinstance(rec, dict):
        return []
    out: list[str] = []
    if _drifted(rec):
        out.append(f"a transcript drift (drift={rec.get('transcript_drift')!r}, "
                   f"{str(rec.get('transcript_sha_before'))[:12]}\u2026 -> "
                   f"{str(rec.get('transcript_sha_after'))[:12]}\u2026)")
    ec = _num(rec.get("exit_code"))
    if ec is not None and ec != 0:
        out.append(f"exit_code={ec!r}")
    lr = _num(rec.get("legs_red"))
    if lr is not None and lr > 0:
        out.append(f"legs_red={lr!r}")
    rn = _nameset(rec.get("red_leg_names"))
    if rn:
        out.append(f"red_leg_names={sorted(rn)}")
    ws = _num(rec.get("wall_seconds"))
    if ws is not None and ws > 0:
        out.append(f"wall_seconds={ws!r}")
    return out


def _where(name, i, hrec, drec) -> str:
    """How a paired record is NAMED in a finding: the stage, the index, and the
    suite string as the WORKING TREE spells it when it has one, as HEAD spells it
    otherwise.  Total: either side may be any object."""
    src = drec if isinstance(drec, dict) and drec.get("suite") is not None else hrec
    suite = src.get("suite") if isinstance(src, dict) else None
    return f"{name!r}: fixture record #{i} {str(suite)[:64]!r}"


def _record_withdrawals(h, d, where: str) -> list[str]:
    """THE ONE-WAY TEST, FIELD BY FIELD, on one HEAD/disk record pair.

    TOTAL BY CONSTRUCTION: `h` and `d` may be ANY object.  Every path returns a
    NAMED FINDING or nothing and none of them raises.

    WITHDRAWAL ONLY, DELIBERATELY.  A failure APPEARING, a count GROWING, a name
    being ADDED, a run costing MORE — all of that is a build advancing and is
    SILENT here, and the controls in resume0_real assert it rather than promise
    it.  A guard that reddens on progress is a guard the next builder deletes."""
    if not isinstance(h, dict):
        return []                      # HEAD admits nothing legible to withdraw
    if not isinstance(d, dict):
        # UNCONDITIONAL, and the totality probe is why.  A record that admits no
        # failure is still the EVIDENCE that its stage was run and what it ran —
        # the suite it was, how many legs it had, the transcript shas it stood
        # on — so a record replaced by a string is GONE as a record whether or
        # not it happened to be confessing anything.  This branch returned []
        # when the record admitted nothing, and the probe caught it on its first
        # run against D-CORE's record #0.  [LEAN R18]
        adm = _record_admissions(h)
        return [f"{where}: HEAD CARRIES A FIXTURE RECORD HERE AND THE WORKING "
                f"TREE CARRIES {type(d).__name__} — a record that cannot be READ "
                f"as a record is gone as surely as one that was deleted, and with "
                f"it the evidence that this stage was run at all"
                + (f". HEAD's record ADMITS {'; '.join(adm)}" if adm
                   else ". HEAD's record admits no failure, which is not a reason "
                        "to let it vanish: it is the proof the suite ran")]
    out: list[str] = []
    if _drifted(h) and not _drifted(d):
        out.append(f"{where}: ADMITS A TRANSCRIPT DRIFT AT HEAD AND ADMITS NONE IN "
                   f"THE WORKING TREE — HEAD drift={h.get('transcript_drift')!r} "
                   f"{str(h.get('transcript_sha_before'))[:12]}\u2026 -> "
                   f"{str(h.get('transcript_sha_after'))[:12]}\u2026, disk "
                   f"drift={d.get('transcript_drift')!r} "
                   f"{str(d.get('transcript_sha_before'))[:12]}\u2026 -> "
                   f"{str(d.get('transcript_sha_after'))[:12]}\u2026. THE DRIFT "
                   f"CLAIM WAS WITHDRAWN BY AN EDIT NOBODY COMMITTED — one boolean "
                   f"and one string copy, cheaper than any forgery and needing no "
                   f"exemption at all")
    he, de = _num(h.get("exit_code")), _num(d.get("exit_code"))
    if he is not None and he != 0 and (de is None or de == 0):
        out.append(f"{where}: EXITS {he!r} AT HEAD AND {d.get('exit_code')!r} IN "
                   f"THE WORKING TREE — a suite that FAILED is being recorded as a "
                   f"suite that passed, and the nonzero exit is the plainest "
                   f"admission of failure a fixture record can make")
    hr, dr = _num(h.get("legs_red")), _num(d.get("legs_red"))
    if hr is not None and hr > 0 and (dr is None or dr < hr):
        out.append(f"{where}: legs_red {hr!r} AT HEAD AND {d.get('legs_red')!r} IN "
                   f"THE WORKING TREE — a red leg is not un-run by an uncommitted "
                   f"edit; it is re-run, and a re-run APPENDS a record")
    hn, dn_ = _nameset(h.get("red_leg_names")), _nameset(d.get("red_leg_names"))
    lost = sorted(hn - dn_)
    if lost:
        out.append(f"{where}: {len(lost)} NAMED RED LEG(S) UN-NAMED in the working "
                   f"tree, e.g. {lost[0]!r} — HEAD names {sorted(hn)}, the working "
                   f"tree {sorted(dn_)}. A named failure is the one a reader can "
                   f"chase, so un-naming it is the withdrawal that costs least")
    hw, dw = _num(h.get("wall_seconds")), _num(d.get("wall_seconds"))
    if hw is not None and hw > 0 and (dw is None or dw < hw):
        out.append(f"{where}: wall_seconds {hw!r} AT HEAD AND {d.get('wall_seconds')!r} "
                   f"IN THE WORKING TREE. This is an admission of COST rather than "
                   f"of failure and it is anchored the same ONE way: a run may be "
                   f"recorded as costing MORE than the commit record says, never "
                   f"LESS — a stage shrunk from hours to milliseconds reads as "
                   f"cheap to redo, and that is a claim about the build")
    return out


def _stage_withdrawals(h, d, name) -> list[str]:
    """THE ONE-WAY TEST AT THE STAGE LEVEL: the blockers list and the status.

    Total in the same sense: `h` and `d` may be any object."""
    out: list[str] = []
    if not isinstance(h, dict):
        return out
    hb, hb_why = _blockerlist(h)
    db, db_why = _blockerlist(d)
    if hb and db_why:
        out.append(f"{name!r}: HEAD lists {len(hb)} BLOCKER(S) and in the working "
                   f"tree {db_why} — blockers that cannot be read are blockers that "
                   f"no longer block, e.g. {str(hb[0])[:80]!r}")
    elif len(db) < len(hb):
        out.append(f"{name!r}: BLOCKERS WITHDRAWN — HEAD lists {len(hb)}, the "
                   f"working tree {len(db)}"
                   + (" (the list is EMPTIED)" if not db else "")
                   + f". A blocker that reached the commit record is cleared by a "
                     f"commit or it is not cleared; e.g. HEAD's first is "
                     f"{str(hb[0])[:80]!r}")
    hs = h.get("status")
    ds = d.get("status") if isinstance(d, dict) else None
    if hs == "PARTIAL" and ds not in ("PARTIAL", "COMPLETE-VERIFIED"):
        out.append(f"{name!r}: PARTIAL AT HEAD AND {ds!r} IN THE WORKING TREE — the "
                   f"stage is being UN-CLAIMED rather than finished. PARTIAL is an "
                   f"admission that work was started and did not complete; "
                   f"retreating to ABSENT erases the fact that it was ever "
                   f"attempted, and every blocker and record under it with it")
    return out




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

    R17/R18-REPAIR — AND ONE LEVEL DOWN, FOR EVERY STAGE.  The three loops above
    leave a non-complete stage FREE TO MOVE, which is what lets the build
    advance, and a review turned that freedom into an ERASURE: the admissions of
    failure inside a PARTIAL stage's block could simply be taken back in an
    uncommitted edit.  The FOURTH loop is the rule that closes it, stated once
    and generally rather than field by field:

        AN ADMISSION THAT REACHED THE COMMIT RECORD MAY NOT BE TAKEN BACK BY AN
        EDIT NOBODY COMMITTED.  It may APPEAR, it may GROW, it may not SHRINK or
        VANISH.

    The anchored vocabulary is `ADMISSION_FIELDS`; the fact that it IS a
    vocabulary is a limit, and resume0_real states and measures it.  Where either
    side calls a stage COMPLETE-VERIFIED the fourth loop STANDS DOWN, because
    loops 2 and 3 already demand something strictly stronger and one tamper
    should print one finding.

    TOTAL BY CONSTRUCTION [LEAN R18].  Every pairing path goes through
    `_stage_list`, `_reclist`, `_blockerlist`, `_record_withdrawals` and
    `_stage_withdrawals`, none of which raises: a missing stage, a missing
    fixtures list, a null, a dict where a list belongs, a short list, a record
    that is not a dict and a stage row that is not an object each produce a
    NAMED FINDING.  Round 6 opened because they did not — they produced
    KeyError, IndexError and TypeError in place of the accusation and the whole
    evidence block, on two of the exact deletion attacks round 5 had just
    repaired.
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
    # ── THE FOURTH LOOP — THE SAME RULE ONE LEVEL DOWN, AT THE FIXTURE RECORD
    #    AND AT THE STAGE'S OWN ADMISSIONS, FOR EVERY STAGE REGARDLESS OF STATUS.
    #    [LEAN-HEPHAESTUS] R17, WIDENED TO ITS GENERAL SHAPE BY R18
    #
    # THE HOLE R17 CLOSED.  R14 anchored the WAIVER'S evidence — the record text
    # that floor (b) reads — and left THE FAILURE'S EVIDENCE FREE.  A drift claim
    # on any non-complete stage could therefore simply be ERASED: one boolean and
    # one string copy inside a PARTIAL stage's block, with no module edit, no new
    # file, no exemption and no pattern.
    #     for f in D-CORE['fixtures']:
    #         if 'OFFLINE' in f['suite']:
    #             f['transcript_drift'] = False
    #             f['transcript_sha_after'] = f['transcript_sha_before']
    # MEASURED through main(), load_progress() returning the tampered ledger and
    # --root in a scratchpad:
    #     drift HONESTLY RECORDED : exit 1 · 7 GREEN 2 RED · leg 4 -> 2 findings
    #     drift ERASED            : exit 1 · 8 GREEN 1 RED · leg 4 PASS,
    #                               leg 0 -> 0 findings, leg 5 -> 0 findings
    # The leg round 4 was spent repairing was GREEN over a real, hidden drift, and
    # the erased run's transcript was BYTE-IDENTICAL to the filed artifact of
    # record — the erasure left no trace anywhere in this suite's output.
    #
    # THE HOLE R17 LEFT, AND WHY ONE MORE FIELD WAS THE WRONG REPAIR.  Anchoring
    # the DRIFT ADMISSION alone left every other admission of failure on a
    # non-complete stage free — exit_code, legs_red, red_leg_names, wall_seconds,
    # the stage's whole blockers list — and left a stage free to move PARTIAL ->
    # ABSENT with nothing said.  A review measured the residue at 8 GREEN, 1 RED:
    # THE SAME COUNT THE ERASE ATTACK PRODUCED BEFORE R17 REPAIRED IT.  So the
    # rule below is stated once, generally, over a NAMED VOCABULARY of admissions
    # (`ADMISSION_FIELDS`), and not patched field by field:
    #
    #     AN ADMISSION THAT REACHED THE COMMIT RECORD MAY NOT BE TAKEN BACK BY AN
    #     EDIT NOBODY COMMITTED.  It may APPEAR, it may GROW, it may not SHRINK
    #     or VANISH.
    #
    # IT IS CHEAPER AND BROADER THAN THE FORGERY ROUND 4 CLOSED.  On the identical
    # record: appending ' (shares fixture plumbing with F-D-1)' -> 2 findings;
    # erasing the drift fields instead -> 0.  The forgery only ever worked on the
    # one stage carrying an exemption; erasure needs no exemption and works on all
    # four non-complete stages.  DELETING the record outright is the same attack
    # one step cruder, and it was red only BY ACCIDENT: LANES happens to be a
    # break-leg plant subject, so the suite went red on "F-C10-RESUME-4 (break leg
    # did not go RED — fixture proves nothing)", which is a fixture reporting that
    # it proved nothing, not a guard catching a tamper.
    #
    # WITHDRAWAL ONLY, AND DELIBERATELY SO.  A NEW drift appearing, a NEW failure
    # appearing, a blocker being ADDED, a record being ADDED, a stage being BORN
    # or CLAIMED (ABSENT -> PARTIAL), a run costing MORE — every one of those is a
    # build ADVANCING and must not go red, the same trade [LEAN R5] made at the
    # stage level so that work can proceed.  What may not happen is a claim that
    # REACHED THE COMMIT RECORD leaving it in an uncommitted edit.  All of it is
    # ASSERTED by controls in resume0_real, not promised in prose.
    #
    # TOTAL BY CONSTRUCTION [LEAN R18].  Every pairing path below goes through
    # `_stage_list`, `_reclist`, `_blockerlist`, `_record_withdrawals` and
    # `_stage_withdrawals`, none of which raises.  A missing stage, a missing
    # 'fixtures' key, a null, a dict where a list belongs, a short list, a record
    # that is not a dict, a stage row that is not an object — each yields a NAMED
    # FINDING.  R18 was opened because the previous shape did NOT: driving the
    # deletion attacks this same loop was written to catch produced KeyError,
    # IndexError and TypeError in place of the accusation and the whole evidence
    # block, and an exception name where a finding should be is indistinguishable
    # from a bug in the fixture.
    bad += _malformed_rows(head, "HEAD")
    bad += _malformed_rows(disk, "the working tree")
    for name in sorted(head_st, key=str):
        h = head_st[name]
        hf, hf_why = _reclist(h)
        hb, _ = _blockerlist(h)
        if hf_why:
            bad.append(f"{name!r}: HEAD'S OWN BLOCK CARRIES NO FIXTURE LIST — "
                       f"{hf_why}. The anchor cannot pair what it cannot read, so "
                       f"this stage's records are unguarded at the source")
        d = disk_st.get(name)
        if d is None:
            # The whole block is gone from the working tree, which withdraws every
            # admission it carried at once.  A COMPLETE-VERIFIED stage is already
            # named by the third loop; naming it twice only makes the count harder
            # to read, so this speaks for the stages that loop deliberately leaves
            # free.  A stage that admitted NOTHING — ABSENT, no blockers, no
            # records — is tidying, not withdrawal, and stays silent.
            if h.get("status") == "COMPLETE-VERIFIED":
                continue
            adm = sorted({a for r in hf for a in _record_admissions(r)})
            if h.get("status") == "PARTIAL" or hf or hb:
                bad.append(f"{name!r}: HEAD carries this stage as "
                           f"{h.get('status')!r} with {len(hf)} fixture record(s) "
                           f"and {len(hb)} blocker(s), and THE WORKING TREE CARRIES "
                           f"NO SUCH STAGE — deleting a block deletes every record "
                           f"and every blocker in it, and with them everything they "
                           f"admitted"
                           + (f" (namely {'; '.join(adm[:3])})" if adm else "")
                           + f". A claim that reached the commit record is "
                             f"withdrawn by a commit or it is not withdrawn")
            continue
        # WHERE LOOPS 2 AND 3 ALREADY RULE, THIS ONE STANDS DOWN — not because
        # it has nothing to say, but because they say something STRICTLY
        # STRONGER and one tamper should print one finding.  If EITHER side
        # calls the stage COMPLETE-VERIFIED then either both do, and loop 2
        # demands the two blocks be BYTE-IDENTICAL (which forbids every
        # withdrawal below and every edit besides), or they disagree, and loop 2
        # or loop 3 has already named the promotion or the demotion.  There is
        # no shape that reaches here unjudged.
        if "COMPLETE-VERIFIED" in (h.get("status"),
                                   d.get("status") if isinstance(d, dict) else None):
            continue
        bad += _stage_withdrawals(h, d, name)
        df, df_why = _reclist(d)
        if df_why and hf:
            adm = sorted({a for r in hf for a in _record_admissions(r)})
            bad.append(f"{name!r}: HEAD carries {len(hf)} fixture record(s) and in "
                       f"the working tree {df_why} — records that cannot be read "
                       f"are records that cannot contradict anything, which is "
                       f"exactly what deleting them buys"
                       + (f"; HEAD's records admit {'; '.join(adm[:3])}" if adm
                          else ""))
        for i, hrec in enumerate(hf):
            if i >= len(df):
                adm = _record_admissions(hrec)
                bad.append(f"{name!r}: fixture record #{i} "
                           f"{str(hrec.get('suite') if isinstance(hrec, dict) else hrec)[:64]!r} "
                           f"IS AT HEAD AND IS GONE FROM THE WORKING TREE (HEAD "
                           f"carries {len(hf)} record(s), the working tree "
                           f"{len(df)})"
                           + (f" — AND THE RECORD THAT VANISHED ADMITTED "
                              f"{'; '.join(adm)}" if adm else "")
                           + f". A fixture record is the evidence that its stage "
                             f"was actually run and what that run cost; deleting "
                             f"one deletes whatever it admitted, and without this "
                             f"loop the suite goes GREEN over the hole")
                continue
            bad += _record_withdrawals(hrec, df[i], _where(name, i, hrec, df[i]))
    return bad


def resume0_break():
    disk = load_progress()
    head_blob = _git_blob("HEAD", LEDGER_REL)
    pin_blob = _git_blob(PINNED_LEDGER_REV, LEDGER_REL)

    head_doc = json.loads(head_blob.decode("utf-8")) if head_blob else {"stages": []}

    # ── EVERY PLANT PATH IS TOTAL, AND ITS SUBJECT IS SEEDED FROM HEAD.
    #    [LEAN-HEPHAESTUS] R18
    # Round 6 drove the deletion attacks this leg was written to catch and found
    # EVERY plant below raising KeyError / IndexError / TypeError the moment the
    # WORKING TREE was itself the thing under investigation — which is the only
    # state in which a break leg matters at all.  `_seed`/`_rec` restore HEAD's
    # own block for the plant's subject into the deep copy before the plant runs,
    # so a plant proves ITS GUARD against a known shape and never depends on what
    # the tree happens to hold today.  A break leg that crashes because the tree
    # was tampered with is a break leg that proved nothing exactly when it
    # mattered.  NO REPO FILE IS WRITTEN BY ANY OF THIS.
    def _pick(pred, why: str) -> str:
        names = sorted(n for n, st in _stages_by_name(head_doc).items()
                       if pred(st))
        return names[0] if names else f"<SYNTHESISED SUBJECT — {why}>"

    NC = _pick(lambda st: st.get("status") != "COMPLETE-VERIFIED"
               and (st.get("fixtures") or []),
               "no non-complete stage with a fixture record exists at HEAD")
    CV = _pick(lambda st: st.get("status") == "COMPLETE-VERIFIED",
               "no COMPLETE-VERIFIED stage exists at HEAD")
    PB = _pick(lambda st: st.get("status") == "PARTIAL" and (st.get("blockers") or []),
               "no blockered PARTIAL stage exists at HEAD")

    def _synth_rec(i: int) -> dict:
        return {"suite": f"SYNTHESISED FIXTURE RECORD #{i}", "exit_code": 0,
                "legs_red": 0, "legs_total": 1, "transcript_drift": False,
                "transcript_sha_before": "0" * 64,
                "transcript_sha_after": "0" * 64, "wall_seconds": 1.0}

    def _blk(name: str) -> dict:
        b = _stages_by_name(head_doc).get(name)
        if isinstance(b, dict):
            return copy.deepcopy(b)
        return {"stage": name, "status": "PARTIAL", "as_of": AS_OF,
                "artifact_shas": {}, "fixtures": [_synth_rec(0)],
                "blockers": ["SYNTHESISED BLOCKER"]}

    def _put(doc: dict, block: dict) -> None:
        rows, _ = _stage_list(doc)
        out, done = [], False
        for r in rows:
            if isinstance(r, dict) and r.get("stage") == block.get("stage"):
                out.append(copy.deepcopy(block))
                done = True
            else:
                out.append(r)
        if not done:
            out.append(copy.deepcopy(block))
        doc["stages"] = out

    def _stage(doc: dict, name: str) -> dict:
        st = _stages_by_name(doc).get(name)
        if not isinstance(st, dict):
            _put(doc, _blk(name))
            st = _stages_by_name(doc)[name]
        return st

    def _recs(doc: dict, name: str = None) -> list:
        st = _stage(doc, name or NC)
        if not isinstance(st.get("fixtures"), list):
            st["fixtures"] = []
        return st["fixtures"]

    def _rec(doc: dict, idx: int = 0, name: str = None) -> dict:
        f = _recs(doc, name)
        while len(f) <= idx:
            f.append(_synth_rec(len(f)))
        if not isinstance(f[idx], dict):
            f[idx] = _synth_rec(idx)
        return f[idx]

    def _blockers(doc: dict, name: str = None) -> list:
        st = _stage(doc, name or NC)
        if not isinstance(st.get("blockers"), list):
            st["blockers"] = []
        if not st["blockers"]:
            st["blockers"] = ["SYNTHESISED BLOCKER A", "SYNTHESISED BLOCKER B"]
        return st["blockers"]

    def mutated(fn, *seed: str) -> list[str]:
        d = copy.deepcopy(disk)
        for nm in seed:
            _put(d, _blk(nm))
        fn(d)
        return anchor_findings(d, head_blob, pin_blob)

    def against(head_fn, disk_fn=None) -> list[str]:
        """A WITHDRAWAL NEEDS SOMETHING TO WITHDRAW.  The committed ledger admits
        no failure today — every record exits 0 with 0 red legs, no drift, no
        named red leg — so the HONEST record, the one a truthful builder would
        have filed and committed, is synthesised HERE inside the plant, and the
        working tree is the WITHDRAWN one.  The plant is therefore the real
        attack run against a real anchor, not a mutation of the anchor itself.

        BOTH sides start from HEAD's own block for the subject stage, so the
        plant is the SAME plant whatever state the working tree is in."""
        h = copy.deepcopy(head_doc)
        d = copy.deepcopy(disk)
        _put(h, _blk(NC))
        _put(d, _blk(NC))
        head_fn(h)
        if disk_fn is not None:
            disk_fn(d)
        return anchor_findings(d, _jb(h).encode("utf-8"), pin_blob)

    # ── the HONEST HEAD halves: what a truthful builder committed ──────────
    def honest_flag(h):
        """HEAD records the drift the honest way: the record's own flag."""
        _rec(h)["transcript_drift"] = True

    def honest_shas(h):
        """HEAD records the drift the OTHER honest way: the two shas disagree,
        with the flag left alone.  Both halves of `_drifted` are exercised
        because the attack rewrites both halves in one move."""
        _rec(h)["transcript_sha_after"] = "9" * 64

    def honest_exit(h):
        """HEAD records a suite that FAILED: nonzero exit, red legs, names."""
        r = _rec(h)
        r["exit_code"] = 1
        r["legs_red"] = 4
        r["legs_total"] = 11
        r["red_leg_names"] = ["F-SYN-1", "F-SYN-2", "F-SYN-3", "F-SYN-4"]

    def honest_wall(h):
        """HEAD records what the run COST."""
        _rec(h)["wall_seconds"] = 3600.5

    # ── the WITHDRAWALS: the working tree takes the admission back ─────────
    def erase_shas(d):
        """THE ATTACK, VERBATIM: one boolean and one string copy."""
        r = _rec(d)
        r["transcript_drift"] = False
        r["transcript_sha_after"] = r.get("transcript_sha_before")

    def erase_fields(d):
        """THE ATTACK, CRUDER: the fields that carry the admission are simply
        removed.  A missing field must read as NO CLAIM, never as health."""
        for k in ("transcript_drift", "transcript_sha_before",
                  "transcript_sha_after"):
            _rec(d).pop(k, None)

    def erase_exit(d):
        """THE SAME MOVE ON THE PLAINEST ADMISSION THERE IS: a suite that exited
        nonzero is recorded as one that exited 0."""
        _rec(d)["exit_code"] = 0

    def erase_exit_field(d):
        _rec(d).pop("exit_code", None)

    def erase_legs_red(d):
        """The count of red legs goes to zero and the names go with it."""
        r = _rec(d)
        r["legs_red"] = 0
        r["red_leg_names"] = []

    def shrink_legs_red(d):
        """PARTIAL withdrawal: 4 red legs become 1.  Shrinking is withdrawing."""
        r = _rec(d)
        r["legs_red"] = 1
        r["red_leg_names"] = ["F-SYN-1"]

    def unname_one_leg(d):
        """THE CHEAPEST OF ALL: the COUNT is left alone and ONE NAME is dropped,
        so a reader can no longer chase the leg that failed."""
        r = _rec(d)
        r["red_leg_names"] = ["F-SYN-1", "F-SYN-2", "F-SYN-3"]

    def shrink_wall(d):
        """A run that cost an hour is recorded as costing a tenth of a second."""
        _rec(d)["wall_seconds"] = 0.1

    def empty_blockers(d):
        """THE STAGE-LEVEL ERASURE: the whole blockers list goes."""
        st = _stage(d, NC)
        _blockers(d)
        st["blockers"] = []

    def shrink_blockers(d):
        b = _blockers(d)
        _stage(d, NC)["blockers"] = list(b)[:-1]

    def drop_blockers_key(d):
        _blockers(d)
        _stage(d, NC).pop("blockers", None)

    def unclaim(d):
        """PARTIAL -> ABSENT: the stage is UN-CLAIMED rather than finished."""
        _stage(d, NC)["status"] = "ABSENT"

    def delete_record(d):
        """THE SECOND HALF: the record itself is gone.  Before this loop, leg 4's
        REAL leg PASSED on exactly this, leg 0 found 0 and leg 5 found 0; the
        suite went red only on a break-leg plant that stopped firing."""
        _stage(d, NC)["fixtures"] = []

    def delete_record_at_0(d):
        """THE SHORT-LIST SHAPE: one record is popped and the rest slide up, so
        every later pairing is off by one AND record #n-1 has no counterpart."""
        f = _recs(d)
        while len(f) < 2:
            f.append(_synth_rec(len(f)))
        f.pop(0)

    def drop_fixtures_key(d):
        """THE LIST ITSELF IS GONE.  This raised KeyError before R18."""
        _stage(d, NC).pop("fixtures", None)

    def fixtures_not_a_list(d):
        """A DICT WHERE THE LIST BELONGS.  This raised KeyError: 0 before R18 —
        `len()` answered, `[0]` did not."""
        _stage(d, NC)["fixtures"] = {"0": "not a list"}

    def fixtures_null(d):
        _stage(d, NC)["fixtures"] = None

    def record_not_a_dict(d):
        """A STRING WHERE THE RECORD BELONGS."""
        _recs(d)[0] = "this is not a fixture record"

    def stage_row_not_an_object(d):
        """A STRING WHERE THE STAGE ROW BELONGS — it carries no stage name, so
        every by-name guard in this leg looks straight past it."""
        _stage(d, NC)
        d["stages"] = [("THIS ROW IS NOT AN OBJECT"
                        if isinstance(r, dict) and r.get("stage") == NC else r)
                       for r in _stage_list(d)[0]]

    def delete_block(d):
        """THE SECOND HALF, ONE STEP CRUDER: the whole non-complete stage block
        leaves the working tree, taking every fixture record with it.  The third
        loop guards only COMPLETE-VERIFIED stages, so nothing above sees this."""
        _stage(d, NC)
        d["stages"] = [t for t in _stage_list(d)[0]
                       if not (isinstance(t, dict) and t.get("stage") == NC)]

    # ── the STAGE-LEVEL plants (loops 1-3) ────────────────────────────────
    def rerecord(d):
        """ATTACK 1 — tamper a filed artifact, then re-record its sha and bytes
        exactly as a lying builder would. Legs 1 and 5 see nothing."""
        st = _stage(d, CV)
        k = sorted(st["artifact_shas"])[0]
        st["artifact_shas"][k]["sha256"] = "0" * 64
        st["artifact_shas"][k]["bytes"] = st["artifact_shas"][k]["bytes"] + 1

    def promote(d):
        """ATTACK 2 — flip a blockered PARTIAL stage to COMPLETE-VERIFIED, empty
        its blockers, and clean its fixture record. wellformed_findings -> []."""
        st = _stage(d, PB)
        st["status"] = "COMPLETE-VERIFIED"
        st["blockers"] = []
        for f in (st.get("fixtures") or []):
            if isinstance(f, dict):
                f["exit_code"] = 0
                f["legs_red"] = 0
                f["legs_total"] = f.get("legs_total") or 1

    def demote(d):
        """ATTACK 4 — WITHDRAW a settled claim in the working tree. Leg 1
        re-hashes COMPLETE-VERIFIED stages, so a demoted stage's artifacts leave
        every guard in the suite at once and the old anchor said nothing."""
        _stage(d, CV)["status"] = "PARTIAL"

    def delete_stage(d):
        """ATTACK 5 — delete the settled stage's block outright. Same hole, one
        step cruder: nothing is left on disk to compare, and absence was health."""
        _stage(d, CV)
        d["stages"] = [t for t in _stage_list(d)[0]
                       if not (isinstance(t, dict) and t.get("stage") == CV)]

    def demote_then_tamper(d):
        """ATTACK 6 — THE LAUNDERING CASE. Demote the stage AND re-record one of
        its artifact shas. Under the old anchor the demotion hid the tamper: the
        re-record loop only ran over stages the working tree still called
        COMPLETE-VERIFIED."""
        st = _stage(d, CV)
        st["status"] = "PARTIAL"
        k = sorted(st["artifact_shas"])[0]
        st["artifact_shas"][k]["sha256"] = "0" * 64
        st["artifact_shas"][k]["bytes"] = st["artifact_shas"][k]["bytes"] + 1

    def derecord(d):
        """ATTACK 3 — de-record an artifact. The re-hash then has nothing to
        re-hash and the sweep's commonpath NARROWS to match."""
        st = _stage(d, CV)
        st["artifact_shas"].pop(sorted(st["artifact_shas"])[0])
        if "artifact_count" in st:
            st["artifact_count"] = len(st["artifact_shas"])

    return plants([
        ("RE-RECORDED SHA (ATTACK 1: a COMPLETE-VERIFIED stage's artifact sha and "
         "byte count rewritten in the working tree)", lambda: mutated(rerecord, CV)),
        ("PROMOTED STAGE (ATTACK 2: a blockered PARTIAL flipped to "
         "COMPLETE-VERIFIED, blockers emptied, fixture record cleaned)",
         lambda: mutated(promote, PB)),
        ("DE-RECORDED ARTIFACT (ATTACK 3: an artifact dropped from a "
         "COMPLETE-VERIFIED stage's record)", lambda: mutated(derecord, CV)),
        ("DEMOTED IN THE WORKING TREE (ATTACK 4: a stage COMPLETE-VERIFIED at "
         "HEAD flipped to PARTIAL on disk — its artifacts then leave every "
         "re-hash in this suite)", lambda: mutated(demote, CV)),
        ("DELETED FROM THE WORKING TREE (ATTACK 5: the settled stage's whole "
         "block removed from the ledger on disk)", lambda: mutated(delete_stage, CV)),
        ("DEMOTE-THEN-TAMPER (ATTACK 6, THE LAUNDERING CASE: the settled stage "
         "is demoted AND one of its artifact shas re-recorded, so the demotion "
         "hides the tamper from every COMPLETE-VERIFIED-only guard)",
         lambda: mutated(demote_then_tamper, CV)),
        ("BENT ANCHOR LITERAL (the module's PINNED_LEDGER_SHA replaced by 64 "
         "zeros — the anchor must check itself)",
         lambda: anchor_findings(disk, head_blob, pin_blob, "0" * 64)),
        ("UNREACHABLE ANCHOR (the pinned blob cannot be read — silence is not "
         "health)", lambda: anchor_findings(disk, head_blob, None)),
        ("UNCOMMITTED LEDGER (HEAD carries no ledger at all, so nothing outside "
         "the working tree can contradict it)",
         lambda: anchor_findings(disk, None, pin_blob)),
        # ── THE FOURTH LOOP'S PLANTS [LEAN R17, WIDENED R18] — one per
        #    ADMISSION in the named vocabulary, each on a NON-COMPLETE stage,
        #    where the three loops above are silent by design and only the
        #    fourth can speak ──
        ("ERASED DRIFT CLAIM — THE SHAS (ATTACK 7, THE CHEAPEST MOVE IN THIS "
         "SUITE: a record ADMITS a transcript drift at HEAD and the working "
         "tree copies transcript_sha_before over transcript_sha_after and sets "
         "transcript_drift False — one boolean and one string copy, no module "
         "edit, no new file, no exemption)",
         lambda: against(honest_shas, erase_shas)),
        ("ERASED DRIFT CLAIM — THE FLAG (ATTACK 7b: HEAD's record carries "
         "transcript_drift True and the working tree's does not — the other "
         "half of what 'drifted' means, so neither half alone is the guard)",
         lambda: against(honest_flag, erase_shas)),
        ("ERASED DRIFT CLAIM — THE FIELDS REMOVED (ATTACK 7c: the working-tree "
         "record simply drops transcript_drift and the two shas — a MISSING "
         "field must read as NO CLAIM, never as a claim of health)",
         lambda: against(honest_flag, erase_fields)),
        ("WITHDRAWN NONZERO EXIT (ATTACK 9: HEAD's record exits 1 and the "
         "working tree's exits 0 — the plainest admission of failure a fixture "
         "record can make, and until R18 it was free)",
         lambda: against(honest_exit, erase_exit)),
        ("WITHDRAWN NONZERO EXIT — THE FIELD REMOVED (ATTACK 9b: exit_code is "
         "simply dropped; a missing field is no claim, not a claim of health)",
         lambda: against(honest_exit, erase_exit_field)),
        ("WITHDRAWN RED LEGS (ATTACK 9c: legs_red 4 -> 0 and red_leg_names "
         "emptied — the suite is recorded as having passed)",
         lambda: against(honest_exit, erase_legs_red)),
        ("SHRUNK RED LEGS (ATTACK 9d: legs_red 4 -> 1 — a PARTIAL withdrawal is "
         "a withdrawal, and a count that only ever shrinks under an uncommitted "
         "edit is a count nobody can trust)",
         lambda: against(honest_exit, shrink_legs_red)),
        ("UN-NAMED RED LEG (ATTACK 9e, THE CHEAPEST OF THIS FAMILY: the COUNT is "
         "left alone at 4 and ONE NAME is dropped, so the leg that failed is the "
         "one a reader can no longer chase)",
         lambda: against(honest_exit, unname_one_leg)),
        ("SHRUNK WALL CLOCK (ATTACK 9f: wall_seconds 3600.5 -> 0.1 — an "
         "admission of COST, anchored the same one way: a stage shrunk from an "
         "hour to a tenth of a second reads as cheap to redo)",
         lambda: against(honest_wall, shrink_wall)),
        ("EMPTIED BLOCKERS (ATTACK 10: a non-complete stage's whole blockers "
         "list is cleared in the working tree — the list is the stage's standing "
         "admission of what it has NOT done)",
         lambda: against(lambda h: None, empty_blockers)),
        ("SHRUNK BLOCKERS (ATTACK 10b: one blocker of several is dropped)",
         lambda: against(lambda h: None, shrink_blockers)),
        ("BLOCKERS KEY REMOVED (ATTACK 10c: the list is not emptied, it is "
         "deleted — a list that cannot be read is a list that no longer blocks)",
         lambda: against(lambda h: None, drop_blockers_key)),
        ("UN-CLAIMED STAGE (ATTACK 11: PARTIAL at HEAD, ABSENT in the working "
         "tree — the stage is not finished, it is retreated from, and every "
         "blocker and record under it goes with it)",
         lambda: against(lambda h: None, unclaim)),
        ("DELETED FIXTURE RECORD (ATTACK 8: a record that is at HEAD is gone "
         "from the working tree — MEASURED before this loop: leg 4's real leg "
         "PASSED, leg 0 found 0, leg 5 found 0, and the suite went red only on "
         "an unrelated break-leg plant that stopped firing)",
         lambda: against(lambda h: None, delete_record)),
        ("DELETED THE RECORD THAT ADMITTED THE DRIFT (ATTACK 8b, THE "
         "LAUNDERING CASE: HEAD's record admits a transcript drift and the "
         "working tree deletes that record outright rather than erasing its "
         "fields — the admission and its evidence leave together)",
         lambda: against(honest_shas, delete_record)),
        ("DELETED RECORD #0 OF SEVERAL (ATTACK 8d, THE SHORT-LIST SHAPE: one "
         "record is popped and the rest slide up, so the last index has no "
         "counterpart at all — this raised IndexError before R18)",
         lambda: against(honest_exit, delete_record_at_0)),
        ("DELETED STAGE BLOCK (ATTACK 8c: a NON-COMPLETE stage's whole block "
         "leaves the working tree with every fixture record in it — the third "
         "loop guards COMPLETE-VERIFIED stages only, so nothing above sees it. "
         "This raised KeyError before R18)",
         lambda: against(honest_shas, delete_block)),
        # ── R18's MALFORMED SHAPES.  Each of these replaced the accusation and
        #    the whole evidence block with an exception name before round 6 ──
        ("FIXTURES KEY REMOVED (ATTACK 12: the stage keeps its block and loses "
         "its whole fixtures list — raised KeyError: 'fixtures' before R18)",
         lambda: against(honest_exit, drop_fixtures_key)),
        ("FIXTURES IS NOT A LIST (ATTACK 12b: a dict where the list belongs, so "
         "len() answers and [0] does not — raised KeyError: 0 before R18)",
         lambda: against(honest_exit, fixtures_not_a_list)),
        ("FIXTURES IS NULL (ATTACK 12c — raised TypeError: 'NoneType' object is "
         "not subscriptable before R18)",
         lambda: against(honest_exit, fixtures_null)),
        ("RECORD IS NOT A DICT (ATTACK 12d: a string where the record belongs — "
         "an admission that cannot be READ is withdrawn as surely as one that "
         "was deleted)",
         lambda: against(honest_exit, record_not_a_dict)),
        ("STAGE ROW IS NOT AN OBJECT (ATTACK 12e: a string in the stages list "
         "carries no stage name, so every by-name guard in this leg looks "
         "straight past it and the stage it replaced reads as simply absent)",
         lambda: against(honest_exit, stage_row_not_an_object)),
    ])


# ── THE TOTALITY PROBE'S GRID.  [LEAN-HEPHAESTUS] R18
#    Every shape a DELETION can take in this ledger, driven against EVERY stage
#    at HEAD by resume0_real.  Round 6 opened because the fourth loop crashed on
#    two of these on the stage that happens to sort first; the answer is not two
#    guards but a grid that is WHOLE, run on every run, and asserted.
PROBE_SHAPES = (
    "delete fixture record #0",
    "delete the LAST fixture record",
    "delete EVERY fixture record (the list is emptied)",
    "delete the 'fixtures' KEY",
    "'fixtures' is null",
    "'fixtures' is a dict, not a list",
    "fixture record #0 is not a dict",
    "delete the WHOLE stage block",
    "the stage ROW is not an object",
    "empty the blockers list",
    "delete the 'blockers' KEY",
    "status -> ABSENT",
)


def probe_apply(shape: str, doc: dict, name: str) -> None:
    """Apply one PROBE_SHAPES deletion to `doc`'s `name` stage, in place.  Total:
    a shape that has nothing to delete leaves the document alone and the caller
    scores it a NO-OP rather than demanding a finding for it."""
    st = _stages_by_name(doc).get(name)
    if not isinstance(st, dict):
        return
    f = st.get("fixtures")
    have = isinstance(f, list) and bool(f)
    if shape == "delete fixture record #0" and have:
        f.pop(0)
    elif shape == "delete the LAST fixture record" and have:
        f.pop()
    elif shape == "delete EVERY fixture record (the list is emptied)":
        st["fixtures"] = []
    elif shape == "delete the 'fixtures' KEY":
        st.pop("fixtures", None)
    elif shape == "'fixtures' is null":
        st["fixtures"] = None
    elif shape == "'fixtures' is a dict, not a list":
        st["fixtures"] = {"0": "not a list"}
    elif shape == "fixture record #0 is not a dict" and have:
        f[0] = "this is not a fixture record"
    elif shape == "delete the WHOLE stage block":
        doc["stages"] = [r for r in _stage_list(doc)[0]
                         if not (isinstance(r, dict) and r.get("stage") == name)]
    elif shape == "the stage ROW is not an object":
        doc["stages"] = [("THIS ROW IS NOT AN OBJECT"
                          if isinstance(r, dict) and r.get("stage") == name else r)
                         for r in _stage_list(doc)[0]]
    elif shape == "empty the blockers list":
        st["blockers"] = []
    elif shape == "delete the 'blockers' KEY":
        st.pop("blockers", None)
    elif shape == "status -> ABSENT":
        st["status"] = "ABSENT"


def resume0_real():
    disk = load_progress()
    dsha, dn = file_sha(PROGRESS_PATH)
    head_blob = _git_blob("HEAD", LEDGER_REL)
    pin_blob = _git_blob(PINNED_LEDGER_REV, LEDGER_REL)
    bad = anchor_findings(disk, head_blob, pin_blob)

    def _parse(blob):
        try:
            doc = json.loads(blob.decode("utf-8"))
            return doc if isinstance(doc, dict) else {}
        except Exception:
            return {}

    head_doc = _parse(head_blob) if head_blob is not None else {}
    head_st = _stages_by_name(head_doc)
    disk_st = _stages_by_name(disk)

    # ── THE TOTALITY PROBE — EVERY DELETION SHAPE, EVERY STAGE, EVERY RUN.
    #    [LEAN-HEPHAESTUS] R18  A guard that RAISES instead of accusing tells the
    #    reader nothing, and an exception name where a finding should be is
    #    indistinguishable from a bug in this fixture.  Round 6 opened on exactly
    #    that: driving the deletion attacks round 5 had just repaired produced
    #    KeyError, IndexError and TypeError in place of the accusation and the
    #    whole evidence block.  The repair is not two more guards; it is this
    #    grid, WHOLE and asserted on every run.  Each cell demands BOTH that the
    #    shape does not raise AND that it yields at least one NAMED finding.
    n_probe = n_probe_noop = n_hdr = 0

    def _hdr_total(label: str, doc) -> None:
        """main()'s HEADER, driven over the same shape. [LEAN R19] The header
        runs BEFORE any fixture, so a shape it cannot read costs the whole run:
        no leg, no accusation, and NO TRANSCRIPT WRITTEN — the stale artifact of
        record then stands over a gutted ledger. It is asserted here, every run,
        and not merely measured once by whoever happened to look."""
        nonlocal n_hdr
        n_hdr += 1
        try:
            lines = header_ledger_lines(doc)
        except Exception as e:
            bad.append(f"HEADER TOTALITY: {label} -> header_ledger_lines RAISED "
                       f"{e.__class__.__name__}: {e}. main() prints this block "
                       f"BEFORE any fixture runs, so this is not one leg lost — it "
                       f"is the whole run, the transcript included")
            return
        if not lines:
            bad.append(f"HEADER TOTALITY: {label} -> the header printed NOTHING at "
                       f"all; a silent header over a broken ledger is the same "
                       f"blank page this suite exists to refuse")

    # the WHOLE-LEDGER shapes, which no per-stage probe can reach: they are the
    # two that actually killed main() (KeyError: 'stages') plus the ledger that
    # is not an object at all.
    for _lbl, _mk in (
            ("the ledger's 'stages' KEY is deleted",
             lambda: {k: v for k, v in disk.items() if k != "stages"}),
            ("the ledger's 'stages' is a STRING, not a list",
             lambda: dict(disk, stages="not a list at all")),
            ("the LEDGER ITSELF is not an object",
             lambda: ["the whole ledger is a list"]),
            ("the ledger is EMPTY", lambda: {}),
    ):
        _d = _mk()
        _hdr_total(_lbl, _d)
        try:
            _f = anchor_findings(_d, head_blob, pin_blob)
        except Exception as e:
            bad.append(f"TOTALITY: {_lbl} -> RAISED {e.__class__.__name__}: {e}")
            _f = ["raised"]
        if not _f:
            bad.append(f"TOTALITY: {_lbl} -> 0 findings. A ledger this leg cannot "
                       f"walk cannot contradict anything, and silence is not health")

    for name in sorted(head_st, key=str):
        for shape in PROBE_SHAPES:
            d2 = copy.deepcopy(disk)
            before = _jb(d2)
            probe_apply(shape, d2, name)
            _hdr_total(f"{name!r} · {shape}", d2)
            if _jb(d2) == before:
                # nothing to delete (an empty blockers list, an absent key): the
                # cell is honestly a NO-OP and demanding a finding for it would
                # be demanding a finding over an unchanged ledger.
                n_probe_noop += 1
                continue
            n_probe += 1
            try:
                found = anchor_findings(d2, head_blob, pin_blob)
            except Exception as e:
                bad.append(f"TOTALITY: {name!r} · {shape} -> RAISED "
                           f"{e.__class__.__name__}: {e}. A guard that raises "
                           f"instead of accusing replaces the finding AND the "
                           f"whole evidence block with an exception name, which "
                           f"a reader cannot tell from a bug in this fixture")
                continue
            if not found:
                bad.append(f"TOTALITY: {name!r} · {shape} -> 0 findings. The shape "
                           f"was applied to the ledger and this leg said NOTHING; "
                           f"silence over a deletion is the hole this loop exists "
                           f"to close")

    # ── WITHDRAWAL ONLY, AND THAT IS ASSERTED, NOT PROMISED.  [LEAN R17/R18]
    #    A guard that goes red on a build ADVANCING is a guard the next person
    #    who needs to advance the build will delete, and they will be right to.
    #    Eight ADVANCES are planted here, one at a time, and every one of them
    #    must be SILENT.  Where a control needs HEAD to say something the
    #    committed ledger does not (a stage it calls ABSENT), that half is
    #    synthesised here, exactly as the break leg's `against` does.
    n_pairs = n_head_drift = n_head_fail = n_head_wall = 0
    n_ctl = 0
    ctl_subject = None
    for _n, _h in head_st.items():
        _hf, _ = _reclist(_h)
        _df, _ = _reclist(disk_st.get(_n))
        for _i, _r in enumerate(_hf):
            if _i < len(_df):
                n_pairs += 1
            if _drifted(_r):
                n_head_drift += 1
            if [a for a in _record_admissions(_r)
                    if not a.startswith("wall_seconds")]:
                n_head_fail += 1
            if isinstance(_r, dict) and (_num(_r.get("wall_seconds")) or 0) > 0:
                n_head_wall += 1
    if head_blob is not None:
        def _ctl(head_fn, disk_fn) -> list[str]:
            hh = copy.deepcopy(head_doc)
            dd = copy.deepcopy(disk)
            head_fn(hh)
            disk_fn(dd)
            return anchor_findings(dd, _jb(hh).encode("utf-8"), pin_blob)

        def _fail_rec(tag: str) -> dict:
            return {"suite": f"A SUITE THAT HAS JUST RUN AND FAILED ({tag})",
                    "exit_code": 1, "legs_red": 2, "legs_total": 9,
                    "red_leg_names": ["F-NEW-1", "F-NEW-2"],
                    "transcript_drift": True,
                    "transcript_sha_before": "0" * 64,
                    "transcript_sha_after": "9" * 64, "wall_seconds": 12.5}

        _cands = sorted(
            n for n in (set(head_st) & set(disk_st))
            if head_st[n].get("status") != "COMPLETE-VERIFIED"
            and _reclist(head_st[n])[0] and _reclist(disk_st[n])[0]
            and isinstance(_reclist(head_st[n])[0][0], dict)
            and isinstance(_reclist(disk_st[n])[0][0], dict))
        controls: list[tuple[str, object, object]] = []
        if _cands:
            ctl_subject = _cands[0]
            _nm = ctl_subject

            def _drec(dd):
                return _stages_by_name(dd)[_nm]["fixtures"][0]

            controls += [
                ("A NEW DRIFT APPEARS in the working tree on a record HEAD calls "
                 "clean — a suite that has just started drifting is a build "
                 "advancing, and leg 4 is what judges whether that drift is named",
                 lambda h: None,
                 lambda d: _drec(d).update({"transcript_drift": True,
                                            "transcript_sha_after": "9" * 64})),
                ("A NEW FAILURE APPEARS — exit_code 0 -> 1, legs_red 0 -> 3, two "
                 "red legs NAMED where none were named before",
                 lambda h: None,
                 lambda d: _drec(d).update({"exit_code": 1, "legs_red": 3,
                                            "red_leg_names": ["F-NEW-1",
                                                              "F-NEW-2"]})),
                ("A RED LEG THAT WAS ONLY COUNTED IS NOW NAMED — HEAD carries a "
                 "count with no names, the working tree carries the same count "
                 "WITH them; naming a failure is not withdrawing it",
                 lambda h: _stages_by_name(h)[_nm]["fixtures"][0].update(
                     {"legs_red": 2, "red_leg_names": []}),
                 lambda d: _drec(d).update({"legs_red": 2,
                                            "red_leg_names": ["F-A", "F-B"]})),
                ("A RUN COST MORE — wall_seconds grows; the cost admission is "
                 "anchored one way and up is the free direction",
                 lambda h: None,
                 lambda d: _drec(d).update(
                     {"wall_seconds": (_num(_drec(d).get("wall_seconds")) or 0) + 1000})),
                ("A BLOCKER IS ADDED to a non-complete stage — discovering what "
                 "is in the way is the work, not a retreat from it",
                 lambda h: None,
                 lambda d: _stages_by_name(d)[_nm]["blockers"].append(
                     "a blocker discovered today")),
                ("A FIXTURE RECORD IS ADDED to a non-complete stage, AND THE "
                 "ADDED RECORD ADMITS A DRIFT AND TWO RED LEGS — another run of "
                 "a suite in progress, failing honestly",
                 lambda h: None,
                 lambda d: _stages_by_name(d)[_nm]["fixtures"].append(
                     _fail_rec("appended"))),
            ]
        controls += [
            ("A WHOLE STAGE IS BORN in the working tree, carrying blockers and a "
             "failing record",
             lambda h: None,
             lambda d: d.__setitem__("stages", list(_stage_list(d)[0]) + [
                 {"stage": "A STAGE THE WORKING TREE HAS AND HEAD DOES NOT",
                  "status": "PARTIAL", "as_of": AS_OF, "artifact_shas": {},
                  "fixtures": [_fail_rec("born")],
                  "blockers": ["not finished yet"]}])),
            ("A STAGE IS CLAIMED — ABSENT at HEAD, PARTIAL in the working tree, "
             "with blockers and a failing record under it. Starting work is the "
             "opposite of withdrawing a claim and must be silent",
             lambda h: h.__setitem__("stages", list(_stage_list(h)[0]) + [
                 {"stage": "A STAGE HEAD CALLS ABSENT", "status": "ABSENT",
                  "as_of": AS_OF, "artifact_shas": {}, "fixtures": [],
                  "blockers": []}]),
             lambda d: d.__setitem__("stages", list(_stage_list(d)[0]) + [
                 {"stage": "A STAGE HEAD CALLS ABSENT", "status": "PARTIAL",
                  "as_of": AS_OF, "artifact_shas": {},
                  "fixtures": [_fail_rec("claimed")],
                  "blockers": ["not finished yet"]}])),
        ]
        for _label, _hfn, _dfn in controls:
            n_ctl += 1
            try:
                _f = _ctl(_hfn, _dfn)
            except Exception as e:
                bad.append(f"CONTROL: {_label} — and this leg RAISED "
                           f"{e.__class__.__name__}: {e}. A control that cannot "
                           f"be run proves nothing about the trade this loop makes")
                continue
            if _f:
                bad.append(f"CONTROL: {_label} — and this leg called it a "
                           f"WITHDRAWAL: {_f[:1]}. The fourth loop is WITHDRAWAL "
                           f"ONLY or it is a brake on the build")

    say(f"      working tree  {LEDGER_REL}")
    say(f"        {dsha}  {dn:>9,} B")
    say(f"      HEAD blob     {sha_bytes(head_blob) if head_blob is not None else 'UNREACHABLE'}"
        f"  {len(head_blob) if head_blob is not None else 0:>9,} B")
    say(f"      pinned blob   {sha_bytes(pin_blob) if pin_blob is not None else 'UNREACHABLE'}"
        f"  {len(pin_blob) if pin_blob is not None else 0:>9,} B  @{PINNED_LEDGER_REV}")
    say(f"      module literal{PINNED_LEDGER_SHA}  PINNED_LEDGER_SHA")
    pinned_blob_cv = sorted(
        n for n, st in _stages_by_name(_parse(pin_blob)).items()
        if st.get("status") == "COMPLETE-VERIFIED") if pin_blob else None
    n_cv = n_free = 0
    say(f"      {'stage':<20} {'HEAD':<18} {'working tree':<18} block vs HEAD")
    rows, rows_why = _stage_list(disk)
    if rows_why:
        say(f"      THE WORKING-TREE LEDGER CANNOT BE WALKED: {rows_why}")
    for st in rows:
        if not isinstance(st, dict):
            # a row that is not an object carries no stage name, so it appears in
            # no by-name comparison at all; it is PRINTED rather than skipped.
            say(f"      {'<STAGE ROW IS NOT AN OBJECT>':<20} {'—':<18} "
                f"{str(type(st).__name__):<18} UNREADABLE")
            continue
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
    disk_names = set(disk_st)
    for name in sorted(head_st, key=str):
        if name in disk_names:
            continue
        say(f"      {str(name):<20} {str(head_st[name].get('status')):<18} "
            f"{'— NOT IN THE WORKING TREE':<18} ABSENT")
    n_head_cv = sum(1 for st in head_st.values()
                    if st.get("status") == "COMPLETE-VERIFIED")
    n_free_ncs = sum(1 for st in head_st.values()
                     if st.get("status") != "COMPLETE-VERIFIED")
    n_head_blk = sum(len(_blockerlist(st)[0]) for st in head_st.values())
    pin_cv = pinned_blob_cv if pinned_blob_cv is not None else []
    say(f"      WHAT THIS ANCHOR PROVES, AND WHAT IT DOES NOT [LEAN R10/R17/R18]")
    say(f"        PROVES   {LEDGER_REL} is TRACKED, so an answer to 'what does the "
        f"record say' exists OUTSIDE the working tree; the {PINNED_LEDGER_REV} blob "
        f"still hashes to a literal typed in this module, so a rewritten history is "
        f"caught; and a COMPLETE-VERIFIED block cannot be BORN, PROMOTED, EDITED, "
        f"DEMOTED or DELETED by a working-tree edit — all of those are planted in "
        f"the break leg and every one of them is RED.")
    say(f"        CANNOT   hold a stage that is COMPLETE-VERIFIED on NEITHER side to "
        f"its BYTES. {n_free} stage(s) are free to move in the working tree: their "
        f"artifact_shas, their as_of, the TEXT of their blockers and of their "
        f"fixture records may all change with no finding here, and leg 1 does not "
        f"re-hash them either — that is the cost of letting the build advance. THIS "
        f"LEG IS NOT SILENT ABOUT THEM: the fourth loop below judges every stage at "
        f"HEAD regardless of status, in ONE DIRECTION ONLY.")
    say(f"        CANNOT   judge a COMMIT. {len(pin_cv)} stage(s) were "
        f"COMPLETE-VERIFIED at the pinned rev and are anchored to a sha a later "
        f"commit cannot move; the other {n_head_cv - len(pin_cv)} COMPLETE-VERIFIED "
        f"stage(s) at HEAD are witnessed by HEAD alone, so for them this leg proves "
        f"only that the working tree has not departed from the commit. The honesty "
        f"of the COMMIT ITSELF rests on review, not on this fixture.")
    say(f"        CANNOT   prove the ledger DESCRIBES THE WORLD. That the recorded "
        f"sha is the artifact's real sha is F-C10-RESUME-1's job, on disk; this leg "
        f"only proves the RECORD did not move.")
    say(f"        PROVES   AND ONE LEVEL DOWN — NO ADMISSION THAT REACHED THE "
        f"COMMIT RECORD MAY BE TAKEN BACK BY AN EDIT NOBODY COMMITTED [LEAN R18]. "
        f"Over ALL {len(head_st)} stage(s) at HEAD regardless of status, pairing "
        f"fixture record #i at HEAD with #i on disk, this loop raises a finding on "
        f"the WITHDRAWAL of any of: a transcript drift; a nonzero exit_code going "
        f"to zero or missing; legs_red decreasing; a named red leg UN-NAMED; "
        f"wall_seconds decreasing (a COST admission, anchored the same one way); "
        f"the stage's blockers list shrinking or becoming unreadable; and a stage "
        f"PARTIAL at HEAD reading anything but PARTIAL-or-COMPLETE on disk — a "
        f"stage UN-CLAIMED rather than finished. A record that is at HEAD may not "
        f"be GONE from the working tree, its whole stage block being gone counting "
        f"as gone. WHERE EITHER SIDE CALLS A STAGE COMPLETE-VERIFIED THIS LOOP "
        f"STANDS DOWN AND LOOPS 2-3 RULE INSTEAD — they demand the two blocks be "
        f"BYTE-IDENTICAL, or they have already named the promotion or the "
        f"demotion, which is strictly stronger than anything below; the scope is "
        f"whole and one tamper still prints one finding. "
        f"{n_pairs} record pair(s) matched, {n_head_drift} admitting a "
        f"drift at HEAD and {n_head_fail} admitting a FAILURE; {n_head_blk} "
        f"blocker(s) under {n_free_ncs} non-complete stage(s). THE RESIDUE R17 LEFT "
        f"WAS NOT HYPOTHETICAL: the committed ledger carries ONE live admission of "
        f"failure — D-CORE's ONLINE record, exit 1 with 1 red leg — and MEASURED on "
        f"the R17 shape, erasing it cost 0 findings, emptying all 23 blockers cost "
        f"0, and un-claiming a PARTIAL stage cost 0. On this shape: 2, 4 and 1.")
    say(f"        PROVES   AND IT NEVER RAISES [LEAN R18]. A guard that raises "
        f"instead of accusing replaces the finding AND the evidence with an "
        f"exception name, which a reader cannot tell from a bug in the fixture. "
        f"Round 6 opened on exactly that. EVERY RUN drives a WHOLE GRID: {len(PROBE_SHAPES)} "
        f"deletion shape(s) — record #0, the last record, every record, the "
        f"'fixtures' key, a null, a dict where the list belongs, a record that is "
        f"not a dict, the whole stage block, a stage row that is not an object, the "
        f"blockers list, the 'blockers' key, status -> ABSENT — against EVERY one "
        f"of the {len(head_st)} stage(s) at HEAD, COMPLETE-VERIFIED and not. "
        f"{n_probe} cell(s) changed the ledger and EVERY ONE yielded a NAMED "
        f"finding and no exception; {n_probe_noop} cell(s) had nothing to delete "
        f"and are scored NO-OP rather than counted as caught. AND THE SAME IS NOW "
        f"DEMANDED OF main()'s HEADER [LEAN R19], which runs BEFORE any fixture "
        f"and whose failure costs not one leg but the whole run, the transcript "
        f"included: {n_hdr} cell(s) — the {len(PROBE_SHAPES)} deletion shapes x "
        f"{len(head_st)} stages plus 4 WHOLE-LEDGER shapes no per-stage probe can "
        f"reach (the 'stages' key deleted, 'stages' a string, the ledger not an "
        f"object, the ledger empty) — were driven through header_ledger_lines() "
        f"and not one raised. MEASURED BEFORE THE REPAIR, at the main() boundary: "
        f"40 of 45 cells gave leg-0 RED with a named finding and 5 DIED, "
        f"KeyError: 'stages' and TypeError: string indices must be integers.")
    say(f"        PROVES   WITHDRAWAL ONLY, AND IT IS ASSERTED HERE, NOT PROMISED: "
        f"{n_ctl} control(s) ran this leg over a build ADVANCING — a NEW drift, a "
        f"NEW failure (exit 0 -> 1, legs_red 0 -> 3, two legs newly NAMED), a red "
        f"leg that was only counted now being NAMED, a run costing MORE, a blocker "
        f"ADDED, a failing record APPENDED, a stage BORN, and a stage CLAIMED "
        f"(ABSENT at HEAD, PARTIAL on disk) — and every one of them was SILENT. A "
        f"guard that reddens on progress is a guard the next builder deletes.")
    say(f"        CANNOT   catch an admission that NEVER REACHED A COMMIT. This "
        f"loop anchors on HEAD like every other loop here, so a failure that "
        f"appears and is erased between two commits leaves no committed claim to "
        f"withdraw; and an erasure that is ITSELF COMMITTED is a commit's act, "
        f"which this fixture does not judge [LEAN R10]. What the anchor buys is "
        f"that the erasure must pass through the commit record first.")
    say(f"        LIMIT    HEAD fixture-record counterparts are matched BY INDEX, "
        f"so an INSERTION or a RE-ORDER of a stage's fixture records goes FALSE "
        f"RED — a false red, not a false green, and the honest trade. The clean "
        f"repair is a stable per-record id emitted by each suite, which is "
        f"PROGRESS.json's to write and not this track's; FILED AS A CROSS-TRACK "
        f"REQUEST. This loop INHERITS the limit from [LEAN R14]'s floor-(b) "
        f"anchor, which matches the same way. MEASURED on today's ledger: a PLAIN "
        f"insertion at #0 where HEAD's #0 admits nothing is SILENT (0 findings); "
        f"an insertion at #0 where HEAD's #0 admits a drift costs 1; an insertion "
        f"at #0 where HEAD's #0 exits nonzero costs 2; and RE-ORDERING D-CORE's "
        f"two records costs 2, because HEAD's #1 is the one live admission of "
        f"failure in this ledger and index #1 then reads clean.")
    say(f"        LIMIT    AND THAT FALSE RED IS USABLE AS CAMOUFLAGE. Say it "
        f"plainly: an attacker who wants this leg IGNORED can PROVOKE the false "
        f"red on purpose — re-order two fixture records, or insert one at #0 — "
        f"and the leg goes RED for a reason that is genuinely innocent. Do that "
        f"two or three times and a reader learns to wave the fourth loop through, "
        f"which is the state in which a real withdrawal passes unread. The finding "
        f"TEXT is the only defence this fixture has: it names the stage, the index "
        f"and the exact field that moved, so an innocent re-order and a withdrawn "
        f"failure do not read alike to anyone who actually reads them. THE "
        f"STRUCTURAL REPAIR IS THE SAME ONE: stable per-record ids, PROGRESS.json's "
        f"to write, FILED AS A CROSS-TRACK REQUEST.")
    say(f"        LIMIT    THE PAIRING TESTS ADMISSION-PRESENCE AT AN INDEX, NOT "
        f"RECORD IDENTITY. SUBSTITUTING a different record at the same index that "
        f"repeats every admission — same drift, same exit_code, same legs_red, the "
        f"same red_leg_names, no less wall clock — is 0 findings HERE: MEASURED. "
        f"The admission at #i survives; the record it belonged to does not. It is "
        f"not a free escape and the numbers say why: keeping the drift alive costs "
        f"a leg-4 RED (the substitute names no waived leg, so no exemption covers "
        f"it) and dropping it costs a leg-0 RED (it is then an ordinary erasure). "
        f"Closing it here would mean demanding a record's TEXT never change, which "
        f"goes false RED on every legitimate rename; WITHDRAWAL ONLY is "
        f"deliberately narrower, and this is the price of the shape, named rather "
        f"than implied.")
    say(f"        LIMIT    THE ADMISSION VOCABULARY IS A NAMED LIST, AND A "
        f"CONFESSION MADE OUTSIDE IT IS NOT ANCHORED. Anchored: "
        f"{'; '.join(ADMISSION_FIELDS)}. NOT anchored, and MEASURED at 0 findings "
        f"each on today's ledger: legs_total shrinking (177 -> 3, so a suite that "
        f"ran 177 legs is recorded as having run 3); the `suite` TEXT of a record "
        f"being rewritten; and any field a future suite invents. WHAT IT COSTS AN "
        f"ATTACKER: nothing at all — these are one-line edits with no finding "
        f"anywhere in this leg. WHAT IT BUYS THEM: less than the fields above, "
        f"because none of them is the claim that a suite PASSED; a shrunken "
        f"legs_total under a record that still exits 1 with 1 red leg hides scope, "
        f"not failure. AND A FIELD THAT IS ABSENT ADMITS NOTHING, SO THERE IS "
        f"NOTHING TO ANCHOR: only {n_head_wall} of the {n_pairs} paired record(s) "
        f"at HEAD carry a positive wall_seconds at all — for the rest the cost "
        f"guard is vacuous, not broken, and a suite that never records what it "
        f"cost can never be caught shrinking it. THE CLEAN REPAIR IS A "
        f"WHOLE-RECORD ONE-WAY DIFF keyed on a stable per-record id, over a "
        f"record shape every suite is required to fill — the SAME cross-track "
        f"request as the two limits above, and the reason it is filed once and "
        f"named three times.")
    say(f"        LIMIT    BLOCKERS ARE MATCHED BY COUNT, NOT BY TEXT. A list that "
        f"SHRINKS or becomes unreadable is a finding; a list whose entries are "
        f"SWAPPED for different text at the same length is 0 findings, MEASURED. "
        f"THAT IS A DELIBERATE CHOICE, NOT AN OVERSIGHT: blockers on a PARTIAL "
        f"stage are working notes that a builder legitimately re-words as "
        f"understanding improves, and matching them by text would go FALSE RED on "
        f"every honest re-wording — the brake this loop must not be. WHAT IT COSTS "
        f"AN ATTACKER: one extra line, swapping a real blocker for a harmless one "
        f"instead of deleting it. THE CLEAN REPAIR is again stable ids, this time "
        f"per blocker, PROGRESS.json's to write.")
    say(f"        CANNOT   defend itself against an edit to THIS FILE. The pin, the "
        f"four loops, the admission vocabulary and the probe grid all live here; "
        f"whoever may rewrite scripts/tierc10_resume_fixtures.py may weaken them, "
        f"and only F-C10-RESUME-S, the commit record and a reader can catch that.")
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
                f"to move in the working tree — FREE TO ADVANCE, NOT FREE TO "
                f"WITHDRAW: across ALL {len(head_st)} stage(s) at HEAD regardless of "
                f"status, {n_pairs} fixture record pair(s) were matched by index and "
                f"NO ADMISSION AT HEAD IS TAKEN BACK ON DISK — not a drift "
                f"({n_head_drift} admit one), not a nonzero exit or a red leg or a "
                f"red leg's NAME ({n_head_fail} admit a failure), not a wall clock "
                f"(of the ones that record a positive one), not one of the "
                f"{n_head_blk} blocker(s) BY COUNT, and no PARTIAL stage is "
                f"un-claimed to ABSENT; no record at HEAD is missing from the "
                f"working tree; {n_probe} totality cell(s) ({len(PROBE_SHAPES)} "
                f"deletion shapes x {len(head_st)} stages, {n_probe_noop} no-op) each "
                f"yielded a NAMED finding and not one raised; and {n_ctl} "
                f"withdrawal-only control(s) — a new drift, a new failure, a red leg "
                f"newly named, a costlier run, an added blocker, an appended failing "
                f"record, a born stage, a claimed stage — were each SILENT"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:4]))


# ═══════════════════════════ F-C10-RESUME-S · THE SELF-ANCHOR
# [LEAN-HEPHAESTUS] R10 ended on a named limit: "it cannot defend itself against
# an edit to THIS FILE, where the pin and the three loops live", and fell back on
# "only the commit record and a reader can catch that". At review time NO COMMIT
# RECORD EXISTED — this module was untracked — so the fallback was a fallback to
# nothing. The module is now tracked on v12-v1-census (added at d8a6f81), a HEAD
# blob exists, and this leg is the guard that uses it.
SELF_REL = "scripts/tierc10_resume_fixtures.py"
SELF_PATH = Path(__file__).resolve()

# WHAT IS UNDER THE ANCHOR — every module literal that is the last word on a
# fact no other file in this build can contradict. Named here so the transcript
# says what an unrecorded edit to this file would buy.
SELF_ANCHORED_LITERALS = (
    "PINNED_LEDGER_REV", "PINNED_LEDGER_SHA",     # F-C10-RESUME-0's external anchor
    "QUARANTINED_PARTIALS",                        # the two LAW-2 kill-partial shas
    "STEP0_COMMIT", "STEP0_SOURCES", "RF_CODE_FILES",   # STEP 0's pins
    "EXEMPTIONS", "COVERAGE_MIN_CHARS", "TIER_WIDE_TOKENS",  # the waiver + its breadth law
    "TC_ROOT_ALLOWLIST",                           # the loose-file escape list
    "TC_SUITE_FILES",                              # the scripts/ sweep inventory
    "AS_OF", "CLOSE_MS", "SEED",                   # the corridor
    "_T_FILED",                                    # the no-clobber stand-in
    "TRANSCRIPT_REL",                              # the artifact of record's anchor path
)


def _git_tracked(rel: str) -> tuple[bool, str]:
    """`git ls-files --error-unmatch` — the only question git answers plainly
    about whether a path is under version control at all. A path that is merely
    PRESENT on disk and absent from the index has no answer outside the working
    tree, which is exactly the condition this leg exists to refuse."""
    try:
        out = subprocess.run(
            ["git", "-C", str(ROOT), "ls-files", "--error-unmatch", "--", rel],
            capture_output=True, check=False)
    except Exception as e:
        return False, f"git ls-files could not run: {e.__class__.__name__}: {e}"
    if out.returncode != 0:
        msg = (out.stderr or out.stdout).decode("utf-8", errors="replace").strip()
        return False, (msg.splitlines() or ["no such entry in the index"])[0]
    return True, "in the index"


def selfanchor_findings(subject: Path, rel: str = SELF_REL,
                        rev: str = "HEAD") -> list[str]:
    """THE MODULE IS JUDGED AGAINST ITS OWN COMMITTED BLOB.

    FAILS IF: `rel` is NOT TRACKED by git; the `rev` blob of `rel` CANNOT BE
    READ; or the SUBJECT's bytes are not BYTE-IDENTICAL to that blob.

    `subject`, `rel` and `rev` are parameters ONLY so the break legs can plant a
    bent copy, an untracked path and an unreachable rev WITHOUT writing one byte
    into the repository or making one git write. The real leg passes the
    module's own file, its own repo-relative path, and HEAD."""
    bad: list[str] = []
    if not subject.exists() or not subject.is_file():
        return [f"SELF-ANCHOR: the subject {subject.name} does not exist — a module "
                f"that cannot read its own bytes anchors nothing, and a check with "
                f"no subject must be RED, never silently green"]
    wsha, wn = file_sha(subject)
    ok_tracked, why = _git_tracked(rel)
    if not ok_tracked:
        bad.append(f"SELF-ANCHOR: {rel!r} IS NOT TRACKED by git ({why}) — an "
                   f"untracked fixture module has NO answer outside the working "
                   f"tree, so each of the {len(SELF_ANCHORED_LITERALS)} pinned "
                   f"literals it carries can be edited with no trace any reader "
                   f"can chase. This is the exact condition [LEAN R10] was written "
                   f"under and it must not recur silently")
    blob = _git_blob(rev, rel)
    if blob is None:
        bad.append(f"SELF-ANCHOR: the {rev} blob of {rel!r} IS UNREACHABLE — the "
                   f"anchor has nothing to anchor against. A guard whose reference "
                   f"cannot be read is RED, not green")
    if ok_tracked and blob is not None:
        bsha = sha_bytes(blob)
        if bsha != wsha:
            bad.append(
                f"SELF-ANCHOR: DIVERGENCE — the working-tree module hashes to "
                f"{wsha} ({wn:,} B), the {rev} blob of {rel} to {bsha} "
                f"({len(blob):,} B). The literals in this file are the last word "
                f"on {len(SELF_ANCHORED_LITERALS)} pinned facts "
                f"({', '.join(SELF_ANCHORED_LITERALS[:4])}, …); an edit to them "
                f"that is NOT in the commit record is precisely the tamper "
                f"F-C10-RESUME-0 refuses to accept for PROGRESS.json, and this "
                f"module may not hold itself to a lower standard than the ledger "
                f"it audits")
    return bad


def _self_plant(body: bytes) -> Path:
    """one throwaway copy of the module, in a temp tree. NO REPO FILE IS
    EDITED and NO GIT WRITE IS MADE by any plant below."""
    d = Path(tempfile.mkdtemp(prefix="tc10_resume_s_"))
    p = d / "tierc10_resume_fixtures.py"
    p.write_bytes(body)
    return p


def resumeS_break():
    """THE PLANTS ARE JUDGED AGAINST THE COMMITTED BLOB, NOT THE WORKING TREE.

    WHY THAT MATTERS.  If a plant were a bent copy of the WORKING-TREE bytes,
    then during any round in which this module has uncommitted edits EVERY plant
    would go red for free — the copy would diverge from HEAD whether or not the
    plant did anything — and the break leg would prove nothing at all.  Each
    plant is therefore ONE EDIT to a copy of the HEAD BLOB ITSELF, whose
    unedited twin is the real leg's negative control at ZERO findings.  The bend
    is then the only thing that can be making it red."""
    blob = _git_blob("HEAD", SELF_REL)
    if blob is None:
        raise AssertionError(
            f"PLANT BASELINE UNAVAILABLE: HEAD:{SELF_REL} cannot be read, so no "
            f"plant can be judged against it")

    def bend(*cands: tuple[bytes, bytes]):
        """CANDIDATE PAIRS, first present in the blob wins.

        The HEAD blob MOVES — it is this module's own history — so a plant
        pinned to one exact byte string silently becomes a CRASH (and, under
        plants(), a FIXTURE DEFECT that voids the whole break leg) the moment
        the orchestrator commits a round.  Each plant therefore offers the same
        tamper in every spelling this file has carried."""
        def go():
            for find, repl in cands:
                if find in blob:
                    p = _self_plant(blob.replace(find, repl, 1))
                    try:
                        return selfanchor_findings(p, SELF_REL, "HEAD")
                    finally:
                        shutil.rmtree(p.parent, ignore_errors=True)
            raise AssertionError(
                f"NO spelling of this plant's target is in the HEAD blob of "
                f"{SELF_REL} ({[c[0][:40] for c in cands]}) — the plant would "
                f"prove nothing and a plant that proves nothing is a defect")
        return go

    def at(rel: str, rev: str):
        def go():
            p = _self_plant(blob)            # byte-identical to HEAD: 0 findings
            try:
                return selfanchor_findings(p, rel, rev)
            finally:
                shutil.rmtree(p.parent, ignore_errors=True)
        return go

    def no_subject():
        p = _self_plant(blob)
        shutil.rmtree(p.parent, ignore_errors=True)
        return selfanchor_findings(p, SELF_REL, "HEAD")

    return plants([
        ("BENT PINNED_LEDGER_SHA (F-C10-RESUME-0's external anchor literal "
         "replaced by 64 zeros on a copy of the committed module — the one edit "
         "that turns the ledger anchor into whatever git says today)",
         bend((PINNED_LEDGER_SHA.encode(), b"0" * 64))),
        ("BENT PINNED_LEDGER_REV (the anchor's rev moved off f97cded)",
         bend((b'PINNED_LEDGER_REV = "f97cded"',
               b'PINNED_LEDGER_REV = "d8a6f81"'))),
        ("BENT QUARANTINE LITERAL (one of the two LAW-2 kill-partial shas "
         "re-typed — the three-way check becomes one number counted twice)",
         bend((QUARANTINED_PARTIALS["lanes/FIXTURES_LANES_partial.txt"].encode(),
               b"f" * 64))),
        ("RE-WIDENED WAIVER (the venue exemption's covers_record_match widened "
         "by one string — the round-3 narrowing put back to the round-2 "
         "stage-name substring, or the round-2 value widened to a tier-wide "
         "token, whichever spelling the committed blob carries)",
         bend((b'"covers_record_match": ("F-D-1",)',
               b'"covers_record_match": ("Stage D fixtures",)'),
              (b'"covers_record_match": ("Stage D fixtures",)',
               b'"covers_record_match": ("TIER-C10",)'))),
        ("LOWERED FLOOR (a numeric threshold in the waiver law dropped to 0 — "
         "COVERAGE_MIN_CHARS, which re-admits the empty pattern, or the reason "
         "floor, which re-admits a label in place of a reason)",
         bend((b"COVERAGE_MIN_CHARS = 4", b"COVERAGE_MIN_CHARS = 0"),
              (b'"reason", ""))) < 120', b'"reason", ""))) < 0'))),
        ("WIDENED ROOT ALLOWLIST (one more loose file waved through the "
         "unrecorded-file sweep)",
         bend((b'TC_ROOT_ALLOWLIST = (\n    "BUILD_DRAFT.md",',
               b'TC_ROOT_ALLOWLIST = (\n    "ANYTHING_AT_ALL.md",'
               b'\n    "BUILD_DRAFT.md",'))),
        ("BENT STEP0_COMMIT (STEP 0's commit of record moved)",
         bend((b'STEP0_COMMIT = "d63592f"', b'STEP0_COMMIT = "f97cded"'))),
        ("BENT CORRIDOR (CLOSE_MS moved by one millisecond — the corridor NEVER "
         "MOVES, and a one-byte edit here moves it)",
         bend((b"CLOSE_MS = 1790006400000", b"CLOSE_MS = 1790006400001"))),
        ("WHITESPACE ONLY (one newline appended — the anchor is BYTE-level, not "
         "semantic, and must not be fooled by a meaningless edit)",
         bend((b"from __future__ import annotations",
               b"from __future__ import annotations\n"))),
        ("UNTRACKED PATH (the subject is byte-identical to HEAD, but the path is "
         "not in the index — the review-time condition, where this module had no "
         "commit record at all)",
         at("scripts/tierc10_resume_fixtures_UNTRACKED.py", "HEAD")),
        ("UNREACHABLE BLOB · NONEXISTENT REV (the subject is byte-identical to "
         "HEAD and the path is tracked, but the rev cannot be resolved — the leg "
         "must go RED, not silently pass on a missing reference)",
         at(SELF_REL, "0" * 40)),
        ("UNREACHABLE BLOB · REV OUT OF RANGE (HEAD~9999)", at(SELF_REL, "HEAD~9999")),
        ("UNREACHABLE BLOB · GHOST REF (a branch nobody created)",
         at(SELF_REL, "refs/heads/tc10-no-such-branch")),
        ("NO SUBJECT AT ALL (the module's own file is gone from under the leg)",
         no_subject),
    ])


def resumeS_real():
    blob = _git_blob("HEAD", SELF_REL)
    tracked, why = _git_tracked(SELF_REL)
    wsha, wn = file_sha(SELF_PATH)
    bad: list[str] = []
    # NEGATIVE CONTROL — a guard that fires on everything guards nothing. A copy
    # that IS byte-identical to the committed blob must yield ZERO findings.
    if blob is None:
        bad.append("CONTROL: HEAD blob unreadable, so the negative control could "
                   "not be run — see the live verdict below")
    else:
        p = _self_plant(blob)
        try:
            ctrl = selfanchor_findings(p, SELF_REL, "HEAD")
            if ctrl:
                bad.append(f"CONTROL: bytes byte-identical to the HEAD blob were "
                           f"reported as a divergence: {ctrl[:1]}")
        finally:
            shutil.rmtree(p.parent, ignore_errors=True)
    say(f"      subject   {SELF_REL}")
    say(f"      worktree  {wsha}  {wn:,} B")
    say(f"      HEAD blob {sha_bytes(blob) if blob is not None else 'UNREACHABLE':<64}  "
        f"{len(blob) if blob is not None else 0:,} B")
    say(f"      tracked   {'YES' if tracked else 'NO'} ({why})")
    say(f"      under the anchor: {len(SELF_ANCHORED_LITERALS)} module literal(s) "
        f"{list(SELF_ANCHORED_LITERALS)}")
    # ── THE HONEST LIMIT, PRINTED IN THE TRANSCRIPT ────────────────────────
    say(f"      LIMIT, STATED PLAINLY. THIS LEG PROVES: this module is under "
        f"version control, its HEAD blob is readable, and the bytes being "
        f"EXECUTED right now are the bytes that are COMMITTED — so an edit to any "
        f"of the {len(SELF_ANCHORED_LITERALS)} literals above cannot reach a run "
        f"without first reaching the commit record, where a reviewer can diff it. "
        f"IT DOES NOT PROVE: that the COMMITTED bytes are honest. A self-anchor "
        f"against HEAD cannot catch an edit that is ITSELF COMMITTED — bend "
        f"PINNED_LEDGER_SHA and commit it and this leg is green on a bent pin. "
        f"Nor can it catch a rewritten history (amend, force-push) that moves the "
        f"blob and the working tree together. AND IT CANNOT BE FIXED BY PINNING: "
        f"the module cannot carry its own sha as a literal the way "
        f"PINNED_LEDGER_SHA pins the ledger's, because a literal holding the sha "
        f"of the file that contains it is a fixed point no author can write — "
        f"typing the sha changes the sha. HEAD is therefore the only external "
        f"answer available to this file, and what stands behind HEAD is review, "
        f"not arithmetic. An accurate statement of a limit is worth more than a "
        f"guard that pretends.")
    bad += selfanchor_findings(SELF_PATH, SELF_REL, "HEAD")
    ok = not bad
    return ok, (f"this module ({wn:,} B, sha {wsha[:16]}…) is TRACKED at {SELF_REL} "
                f"and its working-tree bytes are BYTE-IDENTICAL to the HEAD blob, so "
                f"the {len(SELF_ANCHORED_LITERALS)} literals this file pins are the "
                f"committed ones; negative control: bytes equal to the HEAD blob "
                f"yield zero findings"
                if ok else f"{len(bad)} finding(s): " + " · ".join(bad[:3]))


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
        if root_rel is None:
            # A stage that RECORDS NOTHING has no directory to sweep.  This is
            # legitimate and is F-C10-RESUME's own case: its only artifact is
            # THIS suite's transcript, and a ledger that records the sha of the
            # transcript auditing it does not converge.  The stage must still
            # SAY SO — silence here would let a stage hide by recording nothing.
            sweep = ("NO ARTIFACT RECORDED — no directory to sweep. The stage's "
                     "ledger block must say why it records none; leg 5 holds it "
                     "to the required keys either way [LEAN R19]")
            if not str(st.get("artifact_note") or "").strip():
                bad.append(f"{st['stage']!r}: COMPLETE-VERIFIED and records NO "
                           f"artifact, with no 'artifact_note' saying why — a "
                           f"stage that records nothing and explains nothing is "
                           f"indistinguishable from one whose record was emptied")
        elif root_rel == "research_outputs/tierc10":
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


# a path/identifier token. NOT a word-boundary regex over the raw prose: the
# ledger names its suites as PATHS ("LEGS[] in scripts/tierc10_data_fixtures.py"),
# and a token must be able to be a whole path, a whole basename or a whole stem —
# and NOTHING SHORTER.
_NAME_TOKEN = re.compile(r"[A-Za-z0-9_][A-Za-z0-9_./\\-]*")


def _name_tokens(blob: str) -> set[str]:
    """Every WHOLE name the text contains, plus each one's basename and stem.

    THE HOLE THIS CLOSES.  `_binding_field` used to ask `stem in <blob>` — a
    SUBSTRING test.  D-CORE's block names `scripts/tierc10_data_fixtures.py`, so
    EVERY shorter stem inside it bound for free: MEASURED, a brand-new
    `scripts/tierc10_dat.py` (stem 'tierc10_dat') and the unrelated, already
    existing `scripts/tierc10_data.py` (stem 'tierc10_data') each returned the
    binding field 'blockers' without the ledger naming either of them once.  The
    review proved it on a full symlink mirror of the repo with ONE added file.
    Tokenising and comparing WHOLE names removes the free ride: a stem now binds
    only when the ledger actually spells that name."""
    out: set[str] = set()
    for t in _NAME_TOKEN.findall(blob):
        t = t.strip("./-")
        if not t:
            continue
        out.add(t)
        base = t.rsplit("/", 1)[-1]
        out.add(base)
        out.add(base.rsplit(".", 1)[0] if "." in base else base)
        out.add(base.split(".", 1)[0])       # `tierc10_data.load_asof` names
    return out                               # the module tierc10_data


def _binding_field(stage: dict, srel: str) -> str | None:
    """WHICH FIELD of the stage's own ledger block names the exempted suite —
    the binding, printed by name so a reader can chase it. None = not bound.

    MATCHES EXACTLY, NEVER BY SUBSTRING. [LEAN-HEPHAESTUS] R15"""
    if not isinstance(stage, dict) or not srel:
        return None
    want = {srel, Path(srel).name, Path(srel).stem} - {""}
    if not want:
        return None
    for key in sorted(stage, key=str):
        if _name_tokens(_jb(stage[key])) & want:
            return key
    return None


# ── THE TIE'S EVIDENCE IS ANCHORED, WHATEVER THE STAGE'S STATUS [LEAN R14] ──
_HEAD_LEDGER_CACHE: dict = {}


def _head_ledger() -> tuple[dict | None, str | None]:
    """The COMMITTED PROGRESS.json, parsed — the text the exemption tie is
    allowed to read.

    WHY THIS EXISTS.  F-C10-RESUME-0 anchors COMPLETE-VERIFIED blocks to HEAD
    and deliberately lets a PARTIAL stage move in the working tree, because a
    build in progress must be able to advance.  The exemption tie then read
    exactly that unanchored prose as its evidence, and the review wrote the
    evidence for free: ONE CLAUSE appended to D-CORE's OFFLINE fixture record —
    ' (shares fixture plumbing with F-D-1)' — took a planted drift from 1
    finding to 0 with no module edit and no new file.  So the FIELDS THE TIE
    READS are anchored here for EVERY stage, PARTIAL included, while the rest of
    a PARTIAL block stays free to move.  A change in those fields is REPORTED,
    not forbidden; it is a FINDING only when the change is what CREATES the
    tie."""
    if "v" not in _HEAD_LEDGER_CACHE:
        blob = _git_blob("HEAD", LEDGER_REL)
        if blob is None:
            _HEAD_LEDGER_CACHE["v"] = (
                None, f"the HEAD blob of {LEDGER_REL} is UNREACHABLE")
        else:
            try:
                _HEAD_LEDGER_CACHE["v"] = (
                    json.loads(blob.decode("utf-8")), None)
            except Exception as e:
                _HEAD_LEDGER_CACHE["v"] = (
                    None, f"the HEAD blob of {LEDGER_REL} will not parse as JSON "
                          f"({e.__class__.__name__})")
    return _HEAD_LEDGER_CACHE["v"]


def _head_stage(name) -> tuple[dict | None, str | None]:
    doc, err = _head_ledger()
    if err:
        return None, err
    st = _stages_by_name(doc).get(name)
    if st is None:
        return None, (f"stage {name!r} is NOT IN THE COMMITTED LEDGER at HEAD — a "
                      f"stage that exists only in the working tree carries no "
                      f"anchored text, so nothing it says can tie a waiver")
    return st, None


def _coverage_findings(xid: str, x: dict, stage: dict,
                       head_stage: dict | None = None,
                       head_err: str | None = None) -> list[str]:
    """HOW WIDE MAY A WAIVER REACH?  [LEAN-HEPHAESTUS] R12

    THE HOLE THIS CLOSES.  `covers_record_match` was checked only for being
    DEAD.  Nothing checked it for OVER-matching, and a free substring is a
    blanket escape one keystroke wide: ("",) and ("TIER-C10",) each swallowed
    every D-CORE record with ZERO findings and silenced a planted drift.

    TWO FLOORS, BOTH REQUIRED.

    (a) THE PATTERN ITSELF may not be a generic selector: at least
        COVERAGE_MIN_CHARS characters, and not a substring of the stage's own
        name nor of any tier-wide token.  This is the cheap floor and it catches
        the two measured escapes on sight.

    (b) EVERY RECORD THE PATTERN SELECTS must be POSITIVELY TIED to the waiver:
        the record's own suite/name string must name one of the waived legs.

    WHY (b) IS LEG-NAMING AND NOT AN EXPLICIT `covers_record_ids` LIST.  Both
    forms were on the table.  An id list checked by exact membership is more
    PRECISE, but it is not STRONGER: it is a second free, author-written field
    with nothing outside the registry corroborating it, so widening it is
    exactly as cheap as widening covers_record_match was — the hole moves, it
    does not close.  Leg-naming binds coverage to a fact the exemption's author
    does NOT control: `legs` is already forced, above, to equal EXACTLY the set
    that the exempted suite's OWN LEGS table declares venue-reaching, parsed out
    of that suite's source with ast.  So to widen the waiver's reach you must
    make a ledger record name a leg, and to add a leg you must make a foreign
    suite's own source declare that leg venue-reaching.  That is a chain no
    single string in this file can forge, which is the whole point.

    (b·HEAD) AND THE TEXT (b) READS IS THE COMMITTED TEXT. [LEAN R14]

    THE HOLE THIS CLOSES.  (b) is only as strong as the string it reads, and in
    round 3 that string was a PARTIAL stage's working-tree prose, which
    F-C10-RESUME-0 deliberately leaves unanchored so a build in progress can
    advance.  MEASURED: append ' (shares fixture plumbing with F-D-1)' to
    D-CORE's OFFLINE fixture record in the working tree and a planted drift on
    that record goes from 1 finding to 0 — no module edit, no new file, one
    clause.  The record now NAMES a waived leg, so (b) is satisfied; the pattern
    now SELECTS it, so the closure calls the drift covered.  A guard whose
    evidence is free text the attacker also writes is not a guard.

    SO THE TIE IS ANCHORED, AND ONLY THE TIE.  For every record a pattern
    SELECTS, the pattern must select it in the COMMITTED text too, and the
    committed text must be what names the waived leg.  The rest of a PARTIAL
    block stays free to move; a change in the anchored field is REPORTED (see
    resume4_real's per-record `anchored` lines), not forbidden — it is a FINDING
    only when the change is what CREATES the tie.

    WHY NOT DERIVE THE TIE FROM THE SUITE'S OWN AST INSTEAD.  It was the other
    live option and it does not reach: D-CORE's ONLINE and OFFLINE records are
    TWO RUNS OF THE SAME FILE, so no parse of scripts/tierc10_data_fixtures.py
    can tell them apart.  What the AST already fixes is the LEG NAMES — x['legs']
    is forced, above, to equal exactly the suite's own needs_net set — so the
    only forgeable half left was the RECORD TEXT, and that is the half anchored
    here.  WHY NOT A STRUCTURED FIELD EMITTED BY THE SUITE.  It is the better
    shape and this track cannot build it: PROGRESS.json is not ours to write.
    FILED AS A CROSS-TRACK REQUEST — have each fixture record carry an explicit
    `legs_reaching_venue: [...]` emitted by the suite, and (b) can read a field
    instead of a sentence.

    THE HONEST LIMIT.  (b) reads the record's name, so a genuinely
    venue-reaching record whose name never spells its legs goes FALSE RED here.
    That is a false red, not a false green, and it is the trade this house takes
    every time.  CROSS-TRACK REQUEST: keep a venue-reaching fixture record's
    `suite` string naming the legs that reach the venue — D-CORE's ONLINE record
    already does ('targeted named legs F-D-1 …')."""
    bad: list[str] = []
    suites = [str(f.get("suite", "")) for f in stage.get("fixtures", [])]
    head_suites = ([str(f.get("suite", "")) for f in head_stage.get("fixtures", [])]
                   if isinstance(head_stage, dict) else None)
    legs = tuple(str(g) for g in x.get("legs", ()) if str(g))
    sname = str(stage.get("stage", ""))
    for pat in x.get("covers_record_match", ()):
        p = str(pat)
        pcf = p.strip().casefold()
        # (a) THE PATTERN MAY NOT BE A GENERIC SELECTOR
        if len(p.strip()) < COVERAGE_MIN_CHARS:
            bad.append(f"{xid}: covers_record_match {p!r} is {len(p.strip())} "
                       f"character(s) — a waiver pattern under {COVERAGE_MIN_CHARS} "
                       f"selects by accident, and the empty string selects "
                       f"EVERYTHING its stage carries")
        if pcf and pcf in sname.casefold():
            bad.append(f"{xid}: covers_record_match {p!r} is a substring of the "
                       f"stage's OWN NAME {sname!r} — a waiver named after its "
                       f"stage is a waiver over the whole stage, which is the one "
                       f"thing an exemption may never be")
        for tok in TIER_WIDE_TOKENS:
            if pcf and pcf in tok.casefold():
                bad.append(f"{xid}: covers_record_match {p!r} is a substring of the "
                           f"tier-wide token {tok!r} — a pattern every record in "
                           f"TIER-C10 matches waives TIER-C10, not two legs")
                break
        # (b) EVERY SELECTED RECORD MUST BE TIED TO A WAIVED LEG
        for i, s in enumerate(suites):
            if p not in s:
                continue
            if not any(g in s for g in legs):
                bad.append(f"{xid}: covers_record_match {p!r} SELECTS the record "
                           f"{s[:80]!r}, which names NONE of the waived legs "
                           f"{sorted(legs)} — an exemption that selects a record no "
                           f"waived leg can explain is a BLANKET ESCAPE over that "
                           f"record, and the record's own name is usually telling "
                           f"you so")
            # ── (b·HEAD) THE TIE IS READ OUT OF THE COMMITTED TEXT [LEAN R14] ──
            if head_err:
                bad.append(f"{xid}: covers_record_match {p!r} SELECTS record #{i} of "
                           f"stage {sname!r}, but the tie CANNOT BE ANCHORED — "
                           f"{head_err}. Floor (b)'s whole evidence is the record's "
                           f"own text; with no committed copy to read it against, "
                           f"that text is whatever the working tree says today, and "
                           f"a waiver resting on it is resting on nothing")
            elif head_suites is None:
                bad.append(f"{xid}: covers_record_match {p!r} SELECTS record #{i} of "
                           f"stage {sname!r}, whose ledger block is NOT AT HEAD — an "
                           f"uncommitted stage carries no anchored text, so floor "
                           f"(b) has no evidence it did not read out of the working "
                           f"tree")
            elif i >= len(head_suites):
                bad.append(f"{xid}: covers_record_match {p!r} SELECTS record #{i} "
                           f"{s[:64]!r}, which HAS NO COMMITTED COUNTERPART (stage "
                           f"{sname!r} carries {len(head_suites)} fixture record(s) "
                           f"at HEAD, {len(suites)} in the working tree) — a record "
                           f"that appeared since the last commit may not be what "
                           f"ties a waiver to a leg")
            else:
                h = head_suites[i]
                if p not in h:
                    bad.append(f"{xid}: covers_record_match {p!r} SELECTS record #{i} "
                               f"{s[:80]!r} ONLY IN THE WORKING TREE — the COMMITTED "
                               f"text of that record is {h[:80]!r}, which this "
                               f"pattern does NOT select. THE SELECTION WAS CREATED "
                               f"BY AN EDIT NOBODY COMMITTED. That is one appended "
                               f"clause in an unanchored PARTIAL block, and it is "
                               f"exactly how a drift on a record the waiver may not "
                               f"cover goes from a finding to silence")
                elif not any(g in h for g in legs):
                    bad.append(f"{xid}: covers_record_match {p!r} SELECTS record #{i}, "
                               f"and it is only the WORKING-TREE text that names a "
                               f"waived leg: the COMMITTED text {h[:80]!r} names NONE "
                               f"of {sorted(legs)}. Floor (b) reads the committed "
                               f"record, not today's prose")
    out: list[str] = []
    for f in bad:                      # deterministic, de-duplicated
        if f not in out:
            out.append(f)
    return out


def scripts_sweep_findings(exemptions, root: Path = ROOT,
                           pinned: tuple = TC_SUITE_FILES) -> list[str]:
    """NOTHING IN THIS SUITE SWEPT scripts/. THAT WAS THE HOLE. [LEAN R16]

    Every other sweep in this module looks at research_outputs/tierc10 — the
    OUTPUT side. The exemption chain, though, runs through CODE: an exemption
    names a scripts/ file, that file's own LEGS table decides which legs may be
    waived, and its stem is what the ledger must name for the binding to hold.
    A scripts/ file could therefore APPEAR — untracked, unrecorded, named by
    nobody — and join that chain. The review built exactly that: a full symlink
    mirror of the repo plus ONE added file.

    THE LAW, in three parts:
      · EVERY scripts/tierc10_*.py ON DISK is RECORDED — present in the pinned
        TC_SUITE_FILES literal (which lives under F-C10-RESUME-S, so adding a
        name is not a free edit) AND known to the git index.
      · EVERY PINNED NAME IS STILL THERE — a sweep that only looks at what it
        finds cannot see a deletion.
      · EVERY FILE THE REGISTRY NAMES AS A `suite` is pinned AND has a readable
        HEAD BLOB. The exemption chain may not be validated against a file that
        exists only in somebody's working tree.

    WHAT IS DELIBERATELY *NOT* CHECKED: the suite's CONTENT sha. Those files
    belong to other tracks and move under this one; pinning their bytes here
    would make this leg red for somebody else's honest commit, and their live
    shas stay on stdout only [LEAN R8]."""
    bad: list[str] = []
    d = root / "scripts"
    if not d.is_dir():
        return [f"SCRIPTS SWEEP: {d} is not a directory — the sweep has nothing to "
                f"read, and a sweep that reads nothing must be RED, not silent"]
    on_disk = sorted(f"scripts/{q.name}" for q in d.glob(TC_SUITE_GLOB) if q.is_file())
    pin = tuple(pinned)
    for rel in on_disk:
        if rel not in pin:
            bad.append(f"SCRIPTS SWEEP: {rel} sits in scripts/ and NO module literal "
                       f"records it. A TIER-C10 script that can name itself into an "
                       f"exemption's chain — as the suite, or as the stem a ledger "
                       f"block names — may not simply APPEAR; it is added to "
                       f"TC_SUITE_FILES, and that edit must be COMMITTED before this "
                       f"suite goes green")
        ok, why = _git_tracked(rel)
        if not ok:
            bad.append(f"SCRIPTS SWEEP: {rel} is UNTRACKED ({why}) — a file with no "
                       f"answer outside the working tree may not participate in a "
                       f"waiver, because nothing a reader can chase says it exists")
    for rel in pin:
        if rel not in on_disk:
            bad.append(f"SCRIPTS SWEEP: {rel} is PINNED in TC_SUITE_FILES and is NOT "
                       f"ON DISK — a recorded file that vanished is a finding; a "
                       f"sweep that only inspects what it finds cannot see a deletion")
    for x in exemptions:
        xid = x.get("id") or "<unnamed exemption>"
        srel = str(x.get("suite") or "")
        if not srel:
            continue
        if srel not in pin:
            bad.append(f"{xid}: its suite {srel!r} is not in TC_SUITE_FILES — a file "
                       f"that carries a waiver must be RECORDED under the self-anchor "
                       f"first")
        if _git_blob("HEAD", srel) is None:
            bad.append(f"{xid}: its suite {srel!r} has NO READABLE HEAD BLOB — the "
                       f"legs this exemption may waive are read from that file's own "
                       f"source, so an uncommitted suite means the waiver's authority "
                       f"is a file only its author has seen")
    out: list[str] = []
    for f in bad:
        if f not in out:
            out.append(f)
    return out


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
            # ── AND THE OTHER DIRECTION: A PATTERN MAY NOT OVER-MATCH ──
            # DEAD was policed; OVER-BROAD was not. [LEAN-HEPHAESTUS] R12
            h_stage, h_err = _head_stage(x.get("stage"))
            bad += _coverage_findings(xid, x, stage, h_stage, h_err)
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
            # ── AND THE BINDING IS ANCHORED TOO [LEAN R14/R15] ──
            # FRESH C2, reproduced: appending 'see scripts/tierc10_venue_extra.py'
            # to D-CORE's (PARTIAL, hence unanchored) blockers list makes
            # _binding_field return 'blockers' for a file that does not exist.
            # The binding must be found in the COMMITTED block or it is not a
            # binding, it is a sentence somebody typed this afternoon.
            fld_head = _binding_field(h_stage, srel) if h_stage is not None else None
            if srel and h_err:
                bad.append(f"{xid}: the suite-to-stage binding CANNOT BE ANCHORED — "
                           f"{h_err}. A binding read only out of the working tree is "
                           f"free to whoever holds the editor")
            elif srel and fld_head is None and _binding_field(stage, srel) is not None:
                bad.append(f"{xid}: stage {x['stage']!r} names the exempted suite "
                           f"{Path(srel).stem!r} ONLY IN THE WORKING TREE — the "
                           f"COMMITTED block at HEAD does not name it. A binding that "
                           f"exists only in an uncommitted edit is not a binding: it "
                           f"is the same free text floor (b) was forged with, one "
                           f"field over")
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

    # ── THE BREADTH LAW [LEAN-HEPHAESTUS] R12 ──────────────────────────────
    # Each of these is the REAL, properly-bound X-STAGE-D-VENUE with ONE string
    # changed. Every one of them scored ZERO findings before round 3 and every
    # one of them silenced a real planted drift.
    def widened(pat: str):
        return lambda: exemption_findings(mut(covers_record_match=(pat,)), prog)

    def _drift_offline():
        """the drift planted on D-CORE's OFFLINE record — the run that, by its
        own name, reaches no venue API and may not be covered by a venue
        waiver."""
        p = copy.deepcopy(prog)
        for s in p["stages"]:
            if s.get("stage") != "D-CORE":
                continue
            for f in s["fixtures"]:
                if "OFFLINE" in str(f.get("suite", "")):
                    f["transcript_drift"] = True
                    f["transcript_sha_after"] = "9" * 64
        return p

    def widened_hides_offline_drift(pat: str):
        """judged on the COVERED DRIFT ALONE: a widened pattern may not be the
        reason the OFFLINE record's drift goes unspoken."""
        return lambda: [f for f in
                        exemption_findings(mut(covers_record_match=(pat,)),
                                           _drift_offline())
                        if "DRIFTED" in f]

    def offline_drift_unnamed():
        """THE ROUND-2 REGRESSION ITSELF: with covers_record_match narrowed to
        the waived leg, a drift on the OFFLINE record is no longer covered by
        anything and must be spoken aloud."""
        return exemption_findings(EXEMPTIONS, _drift_offline())

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

    # ══ ROUND 4 · THE TWO FORGERIES OF FLOOR (b), REPRODUCED [LEAN R14/R15/R16]
    FORGED_CLAUSE = " (shares fixture plumbing with F-D-1)"

    def _clause_forgery() -> dict:
        """FORGERY 1, EXACTLY AS THE REVIEW WROTE IT. One clause appended to
        D-CORE's OFFLINE fixture record — a PARTIAL stage's ledger block, which
        F-C10-RESUME-0 deliberately leaves unanchored — makes the waiver's
        pattern SELECT that record and makes the record NAME a waived leg. No
        module edit. No new file. MEASURED at round 3: 1 finding -> 0."""
        q = _drift_offline()
        for st in q["stages"]:
            if st.get("stage") != "D-CORE":
                continue
            for f in st["fixtures"]:
                if "OFFLINE" in str(f.get("suite", "")):
                    f["suite"] = str(f["suite"]) + FORGED_CLAUSE
        return q

    def clause_forgery_drift_only():
        """Judged on the COVERED FAILURE alone: the OFFLINE drift the round-3
        repair spoke aloud must STILL be spoken aloud after the clause."""
        return [f for f in exemption_findings(EXEMPTIONS, _clause_forgery())
                if "DRIFTED" in f]

    def clause_forgery_anchor_only():
        """Judged on the ANCHOR finding alone: the plant must go red because the
        selection exists only in the working tree, not for some other reason."""
        return [f for f in exemption_findings(EXEMPTIONS, _clause_forgery())
                if "ONLY IN THE WORKING TREE" in f and "SELECTS record" in f]

    def clause_forgery_no_drift():
        """The same appended clause with NOTHING to hide: an unanchored tie is a
        standing finding, not a consequence of the drift."""
        q = copy.deepcopy(prog)
        for st in q["stages"]:
            if st.get("stage") != "D-CORE":
                continue
            for f in st["fixtures"]:
                if "OFFLINE" in str(f.get("suite", "")):
                    f["suite"] = str(f["suite"]) + FORGED_CLAUSE
        return exemption_findings(EXEMPTIONS, q)

    def substring_binding():
        """FORGERY 2, THE BINDING HALF. `_binding_field` matched the exempted
        suite's stem by SUBSTRING, so a NEWLY ADDED scripts/ file whose stem is
        a substring of the bound suite's stem bound itself to the stage for
        free: MEASURED, 'scripts/tierc10_dat.py' (stem a substring of
        'tierc10_data_fixtures') returned the binding field 'blockers' though
        D-CORE's block never names it. The match is now EXACT."""
        return [f for f in exemption_findings(mut(suite="scripts/tierc10_dat.py"),
                                             prog)
                if "does not name the exempted suite" in f]

    def fresh_c2_unanchored_blocker():
        """FRESH C2: the substring trick is convenience, not necessity — the
        same binding is reachable by APPENDING 'see scripts/tierc10_venue_extra.py'
        to D-CORE's (PARTIAL, hence unanchored) blockers list. Exact matching
        does not touch this one; anchoring the binding to HEAD does."""
        q = copy.deepcopy(prog)
        for st in q["stages"]:
            if st.get("stage") == "D-CORE":
                st["blockers"].append("see scripts/tierc10_venue_extra.py")
        y = mut(id="X-C2-FRESH", suite="scripts/tierc10_venue_extra.py")
        return [f for f in exemption_findings(y, q)
                if "COMMITTED block at HEAD does not name it" in f]

    # ── THE scripts/ SWEEP [LEAN R16] ──
    def _scripts_mirror(add: tuple = (), drop: tuple = ()) -> Path:
        """A throwaway scripts/ tree of SYMLINKS to the real files — the review's
        own apparatus. NO REPO FILE IS WRITTEN, MOVED OR DELETED by any plant."""
        d = Path(tempfile.mkdtemp(prefix="tc10_scripts_sweep_"))
        sd = d / "scripts"
        sd.mkdir()
        for q in sorted((ROOT / "scripts").glob(TC_SUITE_GLOB)):
            if f"scripts/{q.name}" in drop:
                continue
            (sd / q.name).symlink_to(q)
        for name in add:
            (sd / name).write_text("# planted\n", encoding="utf-8")
        return d

    def sweep(add=(), drop=(), pinned=TC_SUITE_FILES, xs=EXEMPTIONS, grep=None):
        def go():
            d = _scripts_mirror(add, drop)
            try:
                found = scripts_sweep_findings(xs, root=d, pinned=pinned)
            finally:
                shutil.rmtree(d, ignore_errors=True)
            return [f for f in found if grep is None or grep in f]
        return go

    _UNPINNED = "scripts/tierc10_venue_extra.py"

    return plants([
        ("GHOST STAGE (the exemption names a stage the ledger does not carry)", ghost_stage),
        ("DEAD PATTERN (covers_record_match matches no record of its own stage)",
         dead_pattern),
        ("WIDENED TO THE EMPTY STRING (covers_record_match=('',) — a non-empty "
         "tuple, not a dead pattern, and a blanket escape over the whole stage; "
         "MEASURED at 0 findings before R12)", widened("")),
        ("WIDENED TO A TIER-WIDE TOKEN (covers_record_match=('TIER-C10',) — every "
         "record in the tier matches it; MEASURED at 0 findings before R12)",
         widened("TIER-C10")),
        ("WIDENED TO THE STAGE'S OWN NAME (covers_record_match=('D-CORE',) — a "
         "waiver named after its stage is a waiver over its stage)",
         widened("D-CORE")),
        ("WIDENED TO THE ROUND-2 VALUE (covers_record_match=('Stage D fixtures',) "
         "— the exact string this module shipped in round 2, which selects the "
         "OFFLINE record that names no waived leg)", widened("Stage D fixtures")),
        ("WIDENED, JUDGED ON THE COVERED DRIFT ALONE (('',) standing over a REAL "
         "drift planted on the OFFLINE record — the drift must still be spoken)",
         widened_hides_offline_drift("")),
        ("WIDENED, JUDGED ON THE COVERED DRIFT ALONE (('TIER-C10',) over the same "
         "real OFFLINE drift)", widened_hides_offline_drift("TIER-C10")),
        ("WIDENED, JUDGED ON THE COVERED DRIFT ALONE (('Stage D fixtures',) — the "
         "round-2 value — over the same real OFFLINE drift)",
         widened_hides_offline_drift("Stage D fixtures")),
        ("THE OFFLINE RECORD DRIFTS AND NO WAIVER REACHES IT (the venue waiver "
         "covers F-D-1/F-D-1b only; the run that reaches no venue API has no "
         "excuse and must go RED)", offline_drift_unnamed),
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
        ("FORGERY 1 · ONE CLAUSE APPENDED TO A PARTIAL STAGE'S FIXTURE RECORD, "
         "JUDGED ON THE COVERED DRIFT ALONE (' (shares fixture plumbing with "
         "F-D-1)' on D-CORE's OFFLINE record; MEASURED at round 3: 1 finding -> "
         "0, no module edit and no new file — the drift must be spoken again)",
         clause_forgery_drift_only),
        ("FORGERY 1, JUDGED ON THE ANCHOR FINDING ALONE (the tie must go red "
         "because the pattern selects that record ONLY IN THE WORKING TREE, not "
         "for some incidental reason)", clause_forgery_anchor_only),
        ("FORGERY 1 WITH NOTHING TO HIDE (the appended clause with no drift "
         "planted — an unanchored tie is a standing finding)",
         clause_forgery_no_drift),
        ("FORGERY 2 · SUBSTRING BINDING (an exemption over 'scripts/"
         "tierc10_dat.py', whose stem is a SUBSTRING of the bound suite's — "
         "MEASURED to bind to D-CORE's 'blockers' for free before R15)",
         substring_binding),
        ("FRESH C2 · THE BINDING WRITTEN INTO AN UNANCHORED BLOCKERS LIST ('see "
         "scripts/tierc10_venue_extra.py' appended to D-CORE's blockers — exact "
         "matching does not touch this one; the HEAD anchor does)",
         fresh_c2_unanchored_blocker),
        ("SCRIPTS SWEEP · A NEW FILE APPEARS UNRECORDED (one added "
         "scripts/tierc10_*.py in a symlink mirror of scripts/ — the review's own "
         "apparatus, and the hole that made forgery 2 cheap)",
         sweep(add=(Path(_UNPINNED).name,), grep="NO module literal records it")),
        ("SCRIPTS SWEEP · THE NEW FILE IS ALSO UNTRACKED (the same added file, "
         "judged on the git-index half of 'recorded' alone)",
         sweep(add=(Path(_UNPINNED).name,), grep="is UNTRACKED")),
        ("SCRIPTS SWEEP · A RECORDED FILE VANISHES (a pinned name dropped from "
         "the mirror — a sweep that only inspects what it finds cannot see a "
         "deletion)",
         sweep(drop=("scripts/tierc10_data_fixtures.py",), grep="is PINNED in")),
        ("SCRIPTS SWEEP · AN EXEMPTION OVER AN UNRECORDED SUITE (the waiver names "
         "a scripts/ file no literal carries)",
         sweep(xs=mut(suite=_UNPINNED), grep="is not in TC_SUITE_FILES")),
        ("SCRIPTS SWEEP · AN EXEMPTION OVER A SUITE WITH NO HEAD BLOB (the file "
         "is pinned and on disk, but exists only in the working tree — the legs "
         "it may waive are read from a source nobody has committed)",
         sweep(add=(Path(_UNPINNED).name,),
               pinned=TC_SUITE_FILES + (_UNPINNED,),
               xs=mut(suite=_UNPINNED), grep="NO READABLE HEAD BLOB")),
        ("SCRIPTS SWEEP · NO scripts/ AT ALL (the sweep's own subject is gone — a "
         "sweep that reads nothing must be RED, not silent)",
         sweep(drop=tuple(TC_SUITE_FILES), grep="is PINNED in")),
    ])


def resume4_real():
    prog = load_progress()
    bad = exemption_findings(EXEMPTIONS, prog)
    # ── THE scripts/ SWEEP [LEAN R16] — nothing in this suite swept scripts/,
    #    and that is the hole that made the review's second forgery cheap.
    bad += scripts_sweep_findings(EXEMPTIONS)
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
    # POSITIVE CONTROL — THE OTHER HALF, AND THE ONE ROUND 2 DID NOT HAVE.
    # A negative control alone certifies a BLANKET waiver as healthy: round 2's
    # covers_record_match was the stage's name, it selected BOTH D-CORE records,
    # and this control watched both go silent and called it a pass. So the
    # UNSELECTED records of every exempted stage are now planted ONE AT A TIME
    # and each one MUST be spoken aloud. [LEAN-HEPHAESTUS] R12
    uncovered = 0
    for x in EXEMPTIONS:
        for s in prog["stages"]:
            if s.get("stage") != x.get("stage"):
                continue
            for i, f in enumerate(s.get("fixtures", [])):
                suite = str(f.get("suite", ""))
                if any(p in suite for p in x.get("covers_record_match", ())):
                    continue                       # this one IS waived; tested above
                probe = copy.deepcopy(prog)
                for t in probe["stages"]:
                    if t.get("stage") != s.get("stage"):
                        continue
                    t["fixtures"][i]["transcript_drift"] = True
                    t["transcript_sha_after"] = "9" * 64
                spoken = [q for q in exemption_findings(EXEMPTIONS, probe)
                          if "DRIFTED" in q]
                uncovered += 1
                if not spoken:
                    bad.append(
                        f"CONTROL: {x['id']} SILENCED a drift on stage "
                        f"{s['stage']!r}'s record {suite[:64]!r}, which none of its "
                        f"patterns {list(x.get('covers_record_match', ()))} select — "
                        f"a waiver that covers records it does not name is a "
                        f"BLANKET ESCAPE, and a negative control alone would call "
                        f"it healthy")
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
        _sel = [str(f.get("suite", ""))
                for t in prog["stages"] if t.get("stage") == x["stage"]
                for f in t.get("fixtures", [])
                if any(p in str(f.get("suite", "")) for p in x["covers_record_match"])]
        _unsel = [str(f.get("suite", ""))
                  for t in prog["stages"] if t.get("stage") == x["stage"]
                  for f in t.get("fixtures", [])
                  if not any(p in str(f.get("suite", "")) for p in x["covers_record_match"])]
        say(f"        selects    {len(_sel)} record(s), EACH naming a waived leg; "
            f"{len(_unsel)} record(s) of the same stage are NOT reached and a drift "
            f"planted on each of them is spoken aloud (positive control)")
        for _s in _sel:
            say(f"          reached  {_s[:96]!r}")
        for _s in _unsel:
            say(f"          NOT      {_s[:96]!r}")
        say(f"        breadth    every pattern is >= {COVERAGE_MIN_CHARS} chars, is "
            f"not a substring of the stage name {x['stage']!r} nor of any of the "
            f"{len(TIER_WIDE_TOKENS)} tier-wide tokens, and SELECTS ONLY records "
            f"that name one of the waived legs — the waiver is bound to the WAIVED "
            f"LEGS, not to a stage-name substring [LEAN R12]")
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
        h_stage, h_err = _head_stage(x["stage"])
        fld_h = _binding_field(h_stage, srel) if h_stage is not None else None
        say(f"        bound      stage {x['stage']}'s OWN ledger block names the "
            f"exempted suite {Path(srel).stem!r} (in its {fld!r}) — a waiver may not "
            f"be validated against a suite that produced none of the records it "
            f"covers [LEAN R11]. The name is matched EXACTLY, never by substring: a "
            f"new scripts/ file whose stem merely SITS INSIDE this one bound here "
            f"for free before R15. And the binding is read out of the COMMITTED "
            f"block too (HEAD names it in its {fld_h!r}), so it cannot be typed into "
            f"an unanchored PARTIAL block this afternoon [LEAN R14]")
        say(f"        anchored   floor (b)'s evidence is the COMMITTED text of every "
            f"record the pattern SELECTS — for EVERY stage, PARTIAL included. The "
            f"pattern must select the record at HEAD as well, and it is the HEAD "
            f"text that must name a waived leg. A PARTIAL block may still move; a "
            f"move in these fields is REPORTED (stdout) and is a FINDING only when "
            f"it is what CREATES the tie. MEASURED before R14: one clause appended "
            f"to D-CORE's OFFLINE record took a planted drift from 1 finding to 0 "
            f"with no module edit and no new file")
        say(f"        LIMIT      HEAD fixture-record counterparts are matched BY INDEX, so an INSERTION or a RE-ORDER of a stage's fixture records goes FALSE RED — a false red, not a false green, and the honest trade. The clean repair is a stable per-record id emitted by each suite, which is PROGRESS.json's to write and not this track's; FILED AS A CROSS-TRACK REQUEST. [LEAN R17]'s fourth loop, which "
            f"anchors the FAILURE'S evidence the way this anchors the WAIVER'S, "
            f"matches the same way and INHERITS this limit verbatim")
        _hs = ([str(f.get("suite", "")) for f in h_stage.get("fixtures", [])]
               if h_stage is not None else [])
        for _i, _f in enumerate([f for t in prog["stages"]
                                 if t.get("stage") == x["stage"]
                                 for f in t.get("fixtures", [])]):
            _w = str(_f.get("suite", ""))
            _h = _hs[_i] if _i < len(_hs) else None
            clock(f"        [stdout only, live] record #{_i} vs HEAD: "
                  f"{'IDENTICAL' if _h == _w else 'CHANGED' if _h is not None else 'NOT AT HEAD'}"
                  f"  selected_wt={any(q in _w for q in x['covers_record_match'])} "
                  f"selected_head={None if _h is None else any(q in _h for q in x['covers_record_match'])}")
        say(f"        sweep      scripts/ is swept: all {len(TC_SUITE_FILES)} pinned "
            f"TIER-C10 script(s) are on disk and in the git index, no unrecorded "
            f"scripts/{TC_SUITE_GLOB} sits beside them, and this exemption's suite is "
            f"pinned in TC_SUITE_FILES with a readable HEAD blob. 'Recorded' means "
            f"BOTH registers — the git index and a module literal under "
            f"F-C10-RESUME-S — because neither can be written by a working-tree edit "
            f"[LEAN R16]")
        say(f"        ruling     {x['ruling_status']}")
    ok = not bad
    return ok, (f"{len(EXEMPTIONS)} exemption(s), each with a scope, a reason "
                f"({len(EXEMPTIONS[0]['reason'])} chars), a ruling status and EVIDENCE "
                f"RE-DERIVED off disk from the file it names, whatever that file "
                f"is; the exempted legs are EXACTLY the "
                f"{len(EXEMPTIONS[0]['legs'])} that the suite ITSELF declares "
                f"venue-reaching, read from that suite's own source; the suite is "
                f"BOUND to the stage it exempts — {EXEMPTIONS[0]['stage']}'s own "
                f"COMMITTED ledger block names "
                f"{Path(EXEMPTIONS[0]['suite']).stem!r} EXACTLY, so the waiver cannot "
                f"be a borrowed one and cannot be bound by a substring nor by an "
                f"uncommitted edit; floor (b)'s tie is read out of the COMMITTED "
                f"record text for every selected record, whatever the stage's status; "
                f"all {len(TC_SUITE_FILES)} pinned TIER-C10 script(s) are on disk, in "
                f"the index and unaccompanied by any unrecorded sibling; no stage is "
                f"COMPLETE on an exemption's strength (stage {EXEMPTIONS[0]['stage']} "
                f"reads PARTIAL); {n_fix} fixture record(s) scanned across "
                f"{len(prog['stages'])} stages, {n_drift} drifting, 0 of them unnamed; "
                f"negative control: the planted drift on the {hit} record(s) the "
                f"registry names is SILENTLY covered; POSITIVE control: a drift "
                f"planted on each of the {uncovered} record(s) of an exempted stage "
                f"that the registry does NOT name is SPOKEN ALOUD"
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
                    quiet: bool = False, of_record: bool = True) -> list[str]:
    """THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED.

    THE DEFECT THIS REPLACES.  main() wrote the transcript UNCONDITIONALLY at the
    end of every whole-suite run.  So an ordinary, sanctioned run that produced
    different bytes — because a foreign file this track does not own had moved —
    silently DESTROYED the filed artifact and the evidence of the original with
    it, and exited 0.  The house DETERMINISM law says a filed table must
    reproduce to the byte; the failure mode must therefore be loud and
    non-destructive, not silent and destructive.

    THE SECOND DEFECT, AND THE REASON `of_record` EXISTS.  The ABSENT branch
    used to write this run's bytes as the new artifact of record, silently, with
    no flag and ZERO findings anywhere.  MEASURED: with a foreign filed
    transcript present the guard was correct — RED, delta named, artifact
    preserved, the run diverted to FIXTURES_RESUME_rerun.txt; after one
    `rm FIXTURES_RESUME.txt FIXTURES_RESUME_rerun.txt` the very same run went
    SILENT and its own bytes became the record, at a total cost of one rm of a
    file git does not track.  A MISSING ARTIFACT OF RECORD IS A FACT TO ACCUSE,
    NOT A BLANK PAGE TO FILL: the ABSENT branch now mirrors STEP0_RECORD.json's
    refusal — it names the absence as a FINDING and writes nothing unless
    --refile-transcript asks for the first filing by name.  `of_record` is False
    only for a PARTIAL run's FIXTURES_RESUME_partial.txt, which is a scratch
    by-product and was never the record of anything.

    The artifact of record is written only when the new bytes are IDENTICAL to
    it, or when --refile-transcript asks for a re-file (or a first filing) by
    name.  Otherwise this run goes to <name>_rerun.txt, the delta is printed, the
    artifact of record is left exactly as it was, and the finding is RED."""
    def note(line: str) -> None:
        if not quiet:
            clock(line)
    out.parent.mkdir(parents=True, exist_ok=True)
    # THE PATH ITSELF IS EVIDENCE.  `out.exists()` and `read_bytes()` both
    # FOLLOW SYMLINKS, and both RAISE on a path that is not a readable regular
    # file, so three filesystem shapes used to get past this guard with no
    # finding at all [close-out audit, round 8]:
    #   SYMLINK   — silent and GREEN.  The anchor hashed the TARGET, a re-file
    #               wrote THROUGH it, and the record moved somewhere this suite
    #               never names while the tracked path kept only a pointer.
    #   DIRECTORY — IsADirectoryError, uncaught, out of main()'s writer.
    #   chmod 000 — PermissionError, the same way.
    # The two raising shapes are the worse pair: the process dies before the
    # transcript is written, so NO accusation is filed and the STALE artifact
    # stands as the record of a run that never finished.  A record that can be
    # RELOCATED or made UNREADABLE is not a record.  Each shape is now a NAMED
    # FINDING, and nothing is written in any of them.
    if out.is_symlink():
        _tgt = os.readlink(out)
        note(f"\n  transcript path is a SYMLINK at {out} -> {_tgt} "
             f"— NOT WRITTEN, NOT FILED [F-C10-RESUME-T]")
        return [f"{out.name}: THE ARTIFACT OF RECORD IS A SYMLINK to "
                f"{_tgt!r}. A read FOLLOWS it and a --refile-transcript writes "
                f"THROUGH it, so the record would live at a path this suite "
                f"never names while the tracked path keeps only the pointer — "
                f"silently, and GREEN. Nothing was written. Restore a regular "
                f"file from the commit record ({TRANSCRIPT_REL})"]
    if out.exists() and not out.is_file():
        _what = "a DIRECTORY" if out.is_dir() else "a SPECIAL FILE"
        note(f"\n  transcript path is NOT A REGULAR FILE at {out} ({_what}) "
             f"— NOT WRITTEN, NOT FILED [F-C10-RESUME-T]")
        return [f"{out.name}: THE ARTIFACT OF RECORD IS NOT A REGULAR FILE — "
                f"it is {_what}. Nothing was read and nothing was written; "
                f"before this guard the read raised and killed the writer, so "
                f"no transcript was filed at all and the stale artifact stood "
                f"as the record. Restore it from the commit record "
                f"({TRANSCRIPT_REL})"]
    if not out.exists():
        if of_record and not refile:
            note(f"\n  transcript ABSENT at {out} — NOT WRITTEN, NOT FILED "
                 f"[F-C10-RESUME-T]")
            return [f"{out.name}: THE ARTIFACT OF RECORD IS ABSENT and no "
                    f"--refile-transcript was given, so this run's {len(body):,} "
                    f"bytes were NOT written in its place and NOTHING was filed. A "
                    f"transcript of record that can be REPLACED by deleting it is "
                    f"not a record: `rm` costs nothing, leaves no trace in a tree "
                    f"git does not track by default, and the next ordinary run "
                    f"would have made its own bytes the artifact with ZERO findings "
                    f"anywhere. Either restore the filed artifact from the commit "
                    f"record ({TRANSCRIPT_REL}) or file this run deliberately with "
                    f"--refile-transcript"]
        out.write_bytes(body)
        note(f"\n  transcript -> {out}  {len(body):,} B  sha {sha_bytes(body)}  "
             f"[NEW{' on --refile-transcript' if of_record else ''}]")
        return []
    try:
        filed = out.read_bytes()
    except OSError as _exc:
        note(f"\n  transcript UNREADABLE at {out} "
             f"({type(_exc).__name__}) — NOT WRITTEN, NOT FILED "
             f"[F-C10-RESUME-T]")
        return [f"{out.name}: THE ARTIFACT OF RECORD IS UNREADABLE "
                f"({type(_exc).__name__}: {_exc}). Nothing was written. Before "
                f"this guard the read raised out of main()'s writer, so the "
                f"run died with a traceback, NO transcript was filed and the "
                f"stale artifact stood as the record of a run that never "
                f"finished. Restore it from the commit record "
                f"({TRANSCRIPT_REL})"]
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




# ── THE ARTIFACT OF RECORD IS ANCHORED OUTSIDE THE WORKING TREE ────────────
# The no-clobber guard above answers "may this run overwrite the filed
# transcript?".  It cannot answer "IS THE FILED TRANSCRIPT STILL THE ONE THAT
# WAS FILED?", because nothing in this module records what the artifact of
# record said — _T_FILED is a 93 B stand-in on purpose [LEAN R8], and embedding
# the live sha would be a fixed point no author can write.  git can answer it,
# the way it answers it for the ledger: the orchestrator commits
# research_outputs/tierc10/FIXTURES_RESUME.txt with `git add -f` (the tierc10
# tree is gitignored; PROGRESS.json is tracked the same way), and this leg holds
# the working-tree artifact against that blob.  [LEAN-HEPHAESTUS] R19
def transcript_anchor_findings(subject: Path, rel: str = TRANSCRIPT_REL,
                               rev: str = "HEAD") -> list[str]:
    """THE ARTIFACT OF RECORD IS JUDGED AGAINST ITS OWN COMMITTED BLOB.

    FAILS IF: `rel` is NOT TRACKED by git; the `rev` blob of `rel` CANNOT BE
    READ; the SUBJECT is ABSENT from the working tree while the blob remembers
    it; or the subject's bytes are not BYTE-IDENTICAL to that blob.

    `subject`, `rel` and `rev` are parameters ONLY so the break legs can plant an
    untracked path, an unreachable rev, a bent copy and an erasure WITHOUT
    writing one byte into the repository and WITHOUT one git write.  The real leg
    passes the filed transcript, its own repo-relative path, and HEAD.

    NOTHING THIS FUNCTION RETURNS CARRIES THE TRANSCRIPT'S OWN SHA WHEN IT IS
    GREEN, and the real leg prints only the VERDICT.  A transcript that printed
    the sha of the blob it is about to become could never converge [LEAN R8]; a
    verdict over two files that both exist BEFORE this run is a fact about the
    environment, not about these bytes, so it converges in one commit."""
    bad: list[str] = []
    ok_tracked, why = _git_tracked(rel)
    blob = _git_blob(rev, rel)
    if not ok_tracked:
        bad.append(f"TRANSCRIPT ANCHOR: {rel!r} IS NOT TRACKED by git ({why}) — the "
                   f"artifact of record has NO answer outside the working tree, so "
                   f"deleting it costs one `rm` of a file git never reports as "
                   f"missing and leaves NO trace a reader can chase. The no-clobber "
                   f"guard cannot help here: it only decides whether a run may "
                   f"overwrite a file that is THERE. `git add -f {rel}` is the "
                   f"repair, and it is the orchestrator's to make")
    if blob is None:
        bad.append(f"TRANSCRIPT ANCHOR: the {rev} blob of {rel!r} IS UNREACHABLE — "
                   f"the anchor has nothing to anchor against, and a guard whose "
                   f"reference cannot be read is RED, not green")
    if not subject.exists() or not subject.is_file():
        # the BASENAME, never the absolute path: a break-leg plant lives in a
        # randomly named temp tree, and printing it would put a fresh random
        # string in the transcript on every run — a DETERMINISM break introduced
        # by the guard itself. The repo-relative path is the identifying fact.
        bad.append(f"TRANSCRIPT ANCHOR: the artifact of record is ABSENT from the "
                   f"working tree — {rel} (looked for as {subject.name}) — an "
                   f"erasure, named. The whole point of the anchor is that this "
                   f"sentence gets printed instead of a blank page being filled "
                   f"in silence")
        return bad
    if ok_tracked and blob is not None:
        wsha, wn = file_sha(subject)
        if sha_bytes(blob) != wsha:
            bad.append(
                f"TRANSCRIPT ANCHOR: DIVERGENCE — the working-tree artifact of "
                f"record hashes to {wsha[:16]}… ({wn:,} B), the {rev} blob of {rel} "
                f"to {sha_bytes(blob)[:16]}… ({len(blob):,} B). EITHER the filed "
                f"transcript was edited or re-filed and not committed — the standing "
                f"ONE-STEP-BEHIND condition this leg shares with F-C10-RESUME-S, a "
                f"FALSE RED that a commit clears — OR the artifact of record was "
                f"replaced by bytes nobody filed. This leg cannot tell those apart "
                f"and does not pretend to; it is RED for both, which is a false RED "
                f"and NEVER a false green")
    return bad


def _ledger_blob_or(default: bytes) -> bytes:
    """HEAD's ledger blob, or `default` if it cannot be read. The plants that
    need A TRACKED PATH WITH A READABLE BLOB borrow the ledger's; a run in which
    even that is unreadable still has a plant, it just has less of one."""
    b = _git_blob("HEAD", LEDGER_REL)
    return b if b is not None else default


def _t_plant(body: bytes | None) -> Path:
    """one throwaway file (or one deliberately absent path) in a temp tree. NO
    REPO FILE IS WRITTEN and NO GIT WRITE IS MADE by any plant below."""
    d = Path(tempfile.mkdtemp(prefix="tc10_resume_ta_"))
    p = d / TRANSCRIPT
    if body is not None:
        p.write_bytes(body)
    return p


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

    def absent_no_refile() -> list[str]:
        """THE PLANT RETURNS ONLY THE GUARD'S OWN FINDINGS, DELIBERATELY. If it
        also asserted "and the file was not written" it would MANUFACTURE a
        finding in exactly the state where the guard had regressed, and the
        break leg would go green over the hole. Returning the guard's findings
        alone means a regression makes this plant PASS — which voids the break
        leg and turns the fixture RED — while the REAL leg's (d) asserts both
        halves directly."""
        p = _t_plant(None)
        try:
            return file_transcript(p, filed, refile=False, quiet=True)
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
        # ── the ABSENT escape: one `rm` and this run's bytes became the record
        ("THE ARTIFACT OF RECORD IS ABSENT and no --refile-transcript (the `rm` "
         "escape: a blank page offered in place of a record)", absent_no_refile),
        # ── the anchor. LEDGER_REL stands in as A TRACKED PATH OF THIS BUILD so
        #    the divergence and erasure limbs are exercised against a real blob
        #    even on a round in which TRANSCRIPT_REL itself is not yet committed.
        ("ANCHOR · UNTRACKED PATH (a transcript git was never told about)",
         lambda: transcript_anchor_findings(
             _t_plant(b"present on disk, absent from the index\n"),
             "research_outputs/tierc10/A_TRANSCRIPT_NEVER_COMMITTED.txt", "HEAD")),
        ("ANCHOR · UNREACHABLE REV (the blob cannot be read — silence is not "
         "health)",
         lambda: transcript_anchor_findings(_t_plant(_ledger_blob_or(b"x")),
                                            LEDGER_REL, "HEAD~9999")),
        ("ANCHOR · BENT ARTIFACT (one byte on top of the committed blob)",
         lambda: transcript_anchor_findings(
             _t_plant(_ledger_blob_or(b"") + b"\nONE BYTE NOBODY COMMITTED\n"),
             LEDGER_REL, "HEAD")),
        ("ANCHOR · ERASED ARTIFACT (tracked, blob readable, working tree gone)",
         lambda: transcript_anchor_findings(_t_plant(None), LEDGER_REL, "HEAD")),
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
    # (c) --refile-transcript is a deliberate, named escape, and it is silent
    p = _tmp_transcript(filed)
    try:
        f = file_transcript(p, other, refile=True, quiet=True)
        if f:
            bad.append(f"--refile-transcript still reported a finding: {f[:1]}")
        if p.read_bytes() != other:
            bad.append("--refile-transcript did not actually re-file")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    # (d) THE ABSENT BRANCH, BOTH WAYS. An absent artifact of record is a FINDING
    #     and nothing is written; with --refile-transcript the first filing is
    #     deliberate and silent. A refusal that also refused the deliberate
    #     filing would leave no way to file at all, so both halves are asserted.
    p = _t_plant(None)
    try:
        f = file_transcript(p, filed, refile=False, quiet=True)
        if not f:
            bad.append("an ABSENT artifact of record produced NO finding — the `rm` "
                       "escape is open")
        if p.exists():
            bad.append("an ABSENT artifact of record was WRITTEN with no "
                       "--refile-transcript — the refusal does not refuse")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    p = _t_plant(None)
    try:
        f = file_transcript(p, filed, refile=True, quiet=True)
        if f:
            bad.append(f"CONTROL: a deliberate FIRST FILING on --refile-transcript "
                       f"still reported a finding: {f[:1]}")
        if not p.exists() or p.read_bytes() != filed:
            bad.append("CONTROL: --refile-transcript did not file the absent "
                       "artifact — the refusal has no door")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    # (e) A PARTIAL run's by-product is NOT the record and must stay writable
    p = _t_plant(None)
    try:
        f = file_transcript(p, filed, refile=False, quiet=True, of_record=False)
        if f or not p.exists():
            bad.append(f"CONTROL: a non-of-record transcript (the _partial.txt "
                       f"by-product) was refused: {f[:1]}")
    finally:
        shutil.rmtree(p.parent, ignore_errors=True)
    # (f) THE ANCHOR'S NEGATIVE CONTROL — a copy that IS the committed blob of a
    #     tracked path yields ZERO findings, so the anchor is not red-on-sight
    lb = _git_blob("HEAD", LEDGER_REL)
    if lb is None:
        bad.append("CONTROL: HEAD's ledger blob is unreadable, so the anchor's "
                   "negative control could not be run")
    else:
        p = _t_plant(lb)
        try:
            ctrl = transcript_anchor_findings(p, LEDGER_REL, "HEAD")
            if ctrl:
                bad.append(f"CONTROL: bytes byte-identical to a tracked path's HEAD "
                           f"blob were reported as a divergence: {ctrl[:1]}")
        finally:
            shutil.rmtree(p.parent, ignore_errors=True)
    say(f"      stand-in filed artifact  {sha_bytes(_T_FILED)}  {len(_T_FILED)} B "
        f"(a module literal — reading the LIVE transcript here would embed its own "
        f"previous sha in itself [LEAN R8])")
    clock(f"      [stdout only, live] artifact of record "
          f"{filed_p if filed_p.exists() else '(none yet)'} "
          f"{file_sha(filed_p)[0] if filed_p.exists() else '—'}")
    say(f"      the writer main() uses IS file_transcript(); it writes the artifact "
        f"of record ONLY when the bytes are IDENTICAL to the filed ones or on an "
        f"explicit --refile-transcript. An ABSENT artifact of record is a NAMED "
        f"FINDING and is not filled in silence [LEAN R9/R19]")
    # ── THE ANCHOR, LIVE. VERDICTS ONLY: NO SHA OF THIS PATH REACHES THE PAGE
    #    WHEN IT IS GREEN. Printing the HEAD blob's sha here would be the fixed
    #    point [LEAN R8] — the next commit makes THIS file that blob, so the
    #    line would have to contain the sha of the bytes that contain it.
    t_tracked, t_why = _git_tracked(TRANSCRIPT_REL)
    t_blob = _git_blob("HEAD", TRANSCRIPT_REL)
    t_bad = transcript_anchor_findings(filed_p, TRANSCRIPT_REL, "HEAD")
    say(f"      ANCHOR   the artifact of record {TRANSCRIPT_REL}")
    say(f"        tracked      {'YES' if t_tracked else 'NO'} ({t_why})")
    say(f"        HEAD blob    {'READABLE' if t_blob is not None else 'UNREACHABLE'}")
    say(f"        working tree {'PRESENT' if filed_p.exists() else 'ABSENT'}")
    say(f"        verdict      "
        f"{'AGREES with the HEAD blob' if not t_bad else 'NOT ANCHORED — see the finding(s) below'}")
    say(f"        NO SHA OF THIS PATH IS PRINTED WHEN THE VERDICT IS 'AGREES', and "
        f"that is not squeamishness: the next commit makes THIS transcript that "
        f"blob, so a line carrying the blob's sha would have to contain the sha of "
        f"the bytes containing it — the fixed point [LEAN R8] names. The VERDICT is "
        f"a fact about two files that both existed BEFORE this run, so it converges "
        f"in one commit and the live sha still goes to stdout above.")
    say(f"      EVERY ESCAPE THAT EXISTS, NAMED [LEAN R19]. (1) --refile-transcript: "
        f"a deliberate flag, typed by a human, that re-files over a delta and is "
        f"SILENT by design. (2) THE FIRST FILING of an absent artifact — the same "
        f"flag, and ONLY that flag: until this round the ABSENT branch was a second "
        f"escape needing no flag at all, and the [PASS] line that called "
        f"--refile-transcript 'the one deliberate, named escape' was OVERSTATED. "
        f"MEASURED, before the repair: with a foreign filed transcript present the "
        f"guard was correct (RED, delta named, artifact preserved, run diverted to "
        f"FIXTURES_RESUME_rerun.txt); after `rm FIXTURES_RESUME.txt "
        f"FIXTURES_RESUME_rerun.txt` the same run was SILENT, ZERO findings "
        f"anywhere, and its own bytes became the record. (3) A COMMITTED erasure or "
        f"a COMMITTED edit: the anchor is HEAD, so whoever may commit may move the "
        f"blob and the working tree together and this leg is green over it — the "
        f"same limit F-C10-RESUME-S states about this module and F-C10-RESUME-0 "
        f"about the ledger. What the anchor buys is that the erasure must pass "
        f"through the commit record first, where a reviewer can diff it.")
    say(f"      LIMIT    THIS LEG SHARES F-C10-RESUME-S'S STANDING ONE-STEP-BEHIND "
        f"CONDITION. A re-file moves the working tree AHEAD of the blob and the "
        f"anchor is RED until the next commit lands; a run inside that window is a "
        f"FALSE RED, never a false green. The sequence that converges is: commit "
        f"the transcript, run --refile-transcript, commit the re-filed transcript, "
        f"re-run — the fourth step is byte-identical and silent.")
    say(f"      LIMIT    THE RERUN FILE IS ITSELF CLOBBERED. Two non-reproducing "
        f"runs in a row leave only the SECOND one's bytes in "
        f"FIXTURES_RESUME_rerun.txt; the first run's evidence is gone. The artifact "
        f"of RECORD survives both, which is what this leg is for, but the diverted "
        f"bytes are a scratch lane and are not a record.")
    say(f"      LIMIT    A RUN THAT NEVER HAPPENS IS NOT CAUGHT HERE. Nothing in "
        f"this module can make a suite run; --root= diverts this run's own writing "
        f"somewhere else entirely. The ANCHOR is root-independent — it reads "
        f"{TRANSCRIPT_REL} and HEAD whatever --root says — so a diverted run still "
        f"names an erasure it finds, but a run nobody starts accuses nobody.")
    bad += t_bad
    ok = not bad
    return ok, ("the transcript of record cannot be clobbered AND cannot be "
                "quietly replaced by deleting it: identical bytes are silent and do "
                "not rewrite the file (negative control); a non-reproducing run "
                "yields a RED finding naming the first differing lines, LEAVES the "
                "filed artifact byte-for-byte as it was, and preserves its own bytes "
                "in FIXTURES_RESUME_rerun.txt; an ABSENT artifact of record is a "
                "NAMED FINDING and is NOT filled in silence (the `rm` escape, shut); "
                "the artifact of record is TRACKED and its working-tree bytes are "
                "BYTE-IDENTICAL to its HEAD blob, so an erasure or an uncommitted "
                "replacement is named rather than passed; negative control: bytes "
                "equal to a tracked path's HEAD blob yield zero findings; and the "
                "escapes THIS MODULE'S WRITER OFFERS are EXACTLY TWO, both spelled "
                "--refile-transcript — a deliberate re-file and a deliberate first "
                "filing — while the one escape it does NOT close, and says so "
                "above, is an erasure or an edit that is ITSELF COMMITTED, which "
                "the anchor is green over by construction"
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
     "it is not health; OR, ONE LEVEL DOWN AND FOR EVERY STAGE REGARDLESS OF STATUS, "
     "a fixture record that ADMITS A TRANSCRIPT DRIFT at HEAD admits none in the "
     "working tree (its flag cleared, its two shas made equal, or the fields removed "
     "outright), or a fixture record that is at HEAD is MISSING from the working tree "
     "— its whole stage block being gone counting as missing. IT DOES NOT FAIL ON A "
     "BUILD ADVANCING, AND THAT IS DELIBERATE: a NEW drift, an ADDED record and a "
     "BORN stage are each planted as a control that must stay SILENT, because a "
     "guard that reddens on progress is a guard the next builder deletes. THE "
     "STATED LIMIT: HEAD fixture-record counterparts are matched BY INDEX, so an INSERTION or a RE-ORDER of a stage's fixture records goes FALSE RED — a false red, not a false green, and the honest trade. The clean repair is a stable per-record id emitted by each suite, which is PROGRESS.json's to write and not this track's; FILED AS A CROSS-TRACK REQUEST.",
     resume0_break, resume0_real),
    ("F-C10-RESUME-S", "THE SELF-ANCHOR — this module's own bytes are judged "
     "against its own COMMITTED blob",
     "scripts/tierc10_resume_fixtures.py is NOT TRACKED by git, so the "
     "PINNED_LEDGER_SHA / PINNED_LEDGER_REV anchor, the two LAW-2 quarantine "
     "literals, the EXEMPTIONS registry and its breadth law, the STEP 0 pins, the "
     "root allowlist and the corridor constants can all be edited with no trace a "
     "reader can chase; OR the HEAD blob of that path cannot be read, so the anchor "
     "has no reference; OR the working-tree bytes are not BYTE-IDENTICAL to that "
     "blob, which is an edit to this file that never reached the commit record — "
     "the one tamper [LEAN R10] named and could not catch",
     resumeS_break, resumeS_real),
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
     "stands over its suite; ANY covers_record_match PATTERN IS OVER-BROAD — under "
     "4 characters, a substring of the stage's own name or of a tier-wide token, or "
     "SELECTING a fixture record that names none of the waived legs, each of which "
     "is a blanket escape one keystroke wide; THE TIE FLOOR (b) RESTS ON IS NOT IN "
     "THE COMMITTED LEDGER — a pattern selects a record only in the working tree, or "
     "only the working-tree text of a selected record names a waived leg, or the "
     "stage's block is not at HEAD at all, or the HEAD ledger cannot be read; the "
     "suite-to-stage binding is found only in an UNCOMMITTED edit, or is found only "
     "by SUBSTRING rather than by the ledger naming the file exactly; a "
     "scripts/tierc10_*.py sits on disk that TC_SUITE_FILES does not record or that "
     "git does not track, a pinned one has vanished, or an exemption's suite is "
     "unrecorded or has no readable HEAD blob; or any fixture record drifts between "
     "runs with no exemption naming it",
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
    ("F-C10-RESUME-T", "THE TRANSCRIPT OF RECORD IS NEVER CLOBBERED, AND NEVER "
     "QUIETLY REPLACED BY DELETING IT",
     "a whole-suite run produces bytes that are not byte-identical to the filed "
     "FIXTURES_RESUME.txt and no --refile-transcript was given; or the filed artifact "
     "is overwritten by such a run; or the non-reproducing run's own bytes are not "
     "preserved in FIXTURES_RESUME_rerun.txt; or the guard fires on a run that IS "
     "byte-identical; OR the artifact of record is ABSENT and this run's bytes are "
     "written in its place without an explicit --refile-transcript, or that absence "
     "raises no finding at all; OR, THE ANCHOR, research_outputs/tierc10/"
     "FIXTURES_RESUME.txt is NOT TRACKED by git, its HEAD blob cannot be read, the "
     "path is ABSENT from the working tree while the blob remembers it, or the "
     "working-tree bytes are not byte-identical to that blob — the last of which is "
     "ALSO RED for one commit after a legitimate re-file (the standing "
     "one-step-behind condition this leg shares with F-C10-RESUME-S: a false RED, "
     "never a false green); or a deliberate --refile-transcript first filing is "
     "refused, or a PARTIAL run's _partial.txt by-product is refused",
     resumeT_break, resumeT_real),
)


# ══════════════════════ main()'s LEDGER HEADER — TOTAL, AND ASSERTED
# [LEAN-HEPHAESTUS] R19.  This block runs BEFORE any fixture, so a ledger shape
# it cannot read used to kill the process with a traceback: no leg ran, no
# accusation was printed, F-C10-RESUME-T never fired, and NO TRANSCRIPT WAS
# WRITTEN AT ALL — leaving a stale FIXTURES_RESUME.txt standing as the artifact
# of record over a ledger that had been gutted.  MEASURED at the boundary
# before the repair: of 45 cells driven through main(), 40 gave leg-0 RED with a
# named finding and 5 DIED — KeyError: 'stages', and TypeError: string indices
# must be integers on EVERY stage for "the stage ROW is not an object".
# anchor_findings, resume0_real and resume0_break were already total and named
# all of it when driven directly; the hole was four lines of convenience
# indexing in the header above them.
#
# IT IS A MODULE-LEVEL FUNCTION SO THAT IT CAN BE ASSERTED RATHER THAN MERELY
# MEASURED: F-C10-RESUME-0's probe grid drives every deletion shape through THIS
# function on every run and demands that it never raises, exactly as it demands
# of anchor_findings.  A header whose totality is only measured once by whoever
# happened to look is a header that stops being total on the next edit.
def header_ledger_lines(prog) -> list[str]:
    """THE LEDGER LINES main() PRINTS BEFORE ANY FIXTURE RUNS, TOTAL.

    NOTHING HERE RAISES.  Every field goes through an isinstance-guarded .get(),
    the stage rows go through _stage_list(), and a stage row that is not an
    object is PRINTED as UNREADABLE exactly as resume0_real's display loop
    prints it — never skipped, never allowed to raise."""
    def _pg(key, default=None):
        return prog.get(key, default) if isinstance(prog, dict) else default

    def _n_shas(st) -> int:
        a = st.get("artifact_shas") if isinstance(st, dict) else None
        try:
            return len(a)
        except TypeError:
            return 0

    out: list[str] = []
    contract = _pg("contract_of_record")
    if not isinstance(contract, dict):
        contract = {}
    if not isinstance(prog, dict):
        out.append(f"  ledger   THE LEDGER IS {type(prog).__name__.upper()}, NOT AN "
                   f"OBJECT — every field below reads as None and this header does "
                   f"NOT die; F-C10-RESUME-0 is the leg that accuses it")
    out.append(f"  as_of_last_closed_4h {_pg('as_of_of_record')}  ·  close_ms "
               f"{_pg('as_of_last_closed_4h_close_ms')}  ·  seed {_pg('seed')}")
    out.append(f"  substrate {_pg('substrate')}  ·  branch {_pg('branch')}  ·  "
               f"head {str(_pg('head'))[:12]}")
    out.append(f"  contract  {contract.get('path')}  sha "
               f"{str(contract.get('sha256'))[:16]}…")
    rows, rows_why = _stage_list(prog)
    if rows_why:
        out.append(f"  ledger   THE LEDGER'S STAGE ROWS CANNOT BE WALKED: "
                   f"{rows_why}. The header reads ZERO stage(s) and RUNS ON — a "
                   f"header that died here would take every leg, every accusation "
                   f"and the transcript itself with it [LEAN R19]")
    n_c = sum(1 for st in rows
              if isinstance(st, dict) and st.get("status") == "COMPLETE-VERIFIED")
    n_p = sum(1 for st in rows
              if isinstance(st, dict) and st.get("status") == "PARTIAL")
    n_a = sum(1 for st in rows
              if isinstance(st, dict) and st.get("status") == "ABSENT")
    n_u = sum(1 for st in rows if not isinstance(st, dict))
    out.append(f"  ledger   {len(rows)} stage(s): {n_c} COMPLETE-VERIFIED, "
               f"{n_p} PARTIAL, {n_a} ABSENT"
               f"{f', {n_u} UNREADABLE' if n_u else ''} · "
               f"{sum(_n_shas(st) for st in rows):,} artifact sha(s)")
    for i, st in enumerate(rows):
        if not isinstance(st, dict):
            out.append(f"  ledger   stage row #{i} is {type(st).__name__}, not an "
                       f"object — UNREADABLE. It carries no stage name, so every "
                       f"by-name guard below looks straight past it and the stage "
                       f"it replaced reads as simply absent")
    return out


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
    # THE HEADER IS TOTAL, AND ITS TOTALITY IS ASSERTED ON EVERY RUN by
    # F-C10-RESUME-0's probe grid, not merely measured once. [LEAN R19]
    say(f"  ledger   research_outputs/tierc10/PROGRESS.json  {pn:,} B  sha {psha}")
    for _hl in header_ledger_lines(prog):
        say(_hl)
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
    for s in RULINGS:
        say(f"  {s}")
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
    # a PARTIAL run's FIXTURES_RESUME_partial.txt is a by-product, not the
    # record of anything, so the absent-artifact refusal does not apply to it.
    clobber = file_transcript(out, body, refile, of_record=not pick)
    if clobber:
        clock(f"\n  F-C10-RESUME-T — THE TRANSCRIPT OF RECORD · RED")
        clock(f"    FAILS IF: a whole-suite run produces a transcript that is not "
              f"byte-identical to the filed one, or the filed one is ABSENT and no "
              f"--refile-transcript was given.")
        for f in clobber:
            clock(f"    {f}")
        clock(f"    Understand the delta, then re-file deliberately with "
              f"--refile-transcript.")
        rc = 1
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
