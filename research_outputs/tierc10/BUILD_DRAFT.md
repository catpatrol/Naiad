# BUILD — TIER-C10 · TWELVE UNSEEN ASSETS, THE RANGE CENSUS, AND THREE SETUPS ON TRIAL

> **DRAFT.** This document lives at `research_outputs/tierc10/BUILD_DRAFT.md` and moves to
> `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` **only at CLOSE**
> (LAW 5: a draft under `exchange/` is not a draft). The filed name keeps the 2026-09-21 date —
> one build, one document, however many sessions.

- **Contract of record:** `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`
  (sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a`)
- **Original contract:** TIER-C10, ratified by the operator 2026-09-21.
- **Operator rulings:** `research_outputs/tierc10/OPERATOR_RULINGS.md`
  (sha256 `70188a0cc32422be40e74d8e7adf7d444aa610bb3abf0384b4f4a2f66f57bbec`) — six rulings,
  recovered verbatim from the interrupted session's transcript after its scratchpad was destroyed.
- **Drafted:** APOLLO. **Executor:** HEPHAESTUS. **Seed:** 20260921 (unchanged across the interruption).
- **AS-OF OF RECORD:** 2026-09-21T16:00:00Z — the last closed 4h bar at the first run's start.
  One corridor governs every stage (LAW 4).
- **Substrate:** `/Users/luis/.cache/naiad/snapshots/tc10_20260921` (frozen copy; the live cache is
  untouched because a separate live lane commits to it).

---

## 0 · VERDICTS

*Filled at CLOSE. Six registered rows, then the admitted list, then the forward strip.*

| registration | prior | arm | panel | era | point | CI | verdict | BH bar | LOAO |
|---|---|---|---|---|---|---|---|---|---|
| P-GEN-1 | 45% | — | — | — | — | — | *pending* | — | — |
| P-SPR-2 | 45% | — | — | — | — | — | *pending* | — | — |
| P-BE-1 | 40% | — | — | — | — | — | *pending* | — | — |
| P-TRG-2 | 40% | — | — | — | — | — | *pending* | — | — |
| P-BRK-I1 | 35% | — | — | — | — | — | *pending* | — | — |
| P-BRK-S1 | 30% | — | — | — | — | — | *pending* | — | — |

---

## R0 · WHAT THE INTERRUPTION LEFT

*The stage ledger, what was quarantined, and what was redone.*

### R0.1 · The interruption

The 2026-09-21 builder session (`730798c3-4e2c-4d67-8a9b-be6f9aae52f5`) was killed by an
**API 529 at 2026-09-22T01:06:58Z**. Its final workflow had launched 15 agents; 13 completed and
**two died on the same 529**:

- `review:census#1` — the adversarial review of the CENSUS-R module never ran. CENSUS-R is
  therefore the least-reviewed artifact in the build.
- `draft:registrations` — **no registration text was ever drafted, for any of the six lanes.**
  `research_outputs/tierc10/registrations/` does not exist. Stage B had not begun.

The session's scratchpad was destroyed with it, taking the only copies of `OPERATOR_RULINGS.md`,
`REGISTRATION_DRAFTS.md`, `foundations_result.json` and `STEP0_RECORD.md`. The session transcript
and the workflow journals survived and were mined on 2026-09-22; the operator's six rulings were
recovered verbatim and are now filed **inside the build tree** so the next interruption cannot
take them.

### R0.2 · The stage ledger

Every status below was established by **re-running the suite on 2026-09-22**, as LAW 1 demands —
not by reading a filed transcript. 1,035 artifact content-shas were re-hashed independently of the
verifiers' own reports and are recorded in `research_outputs/tierc10/PROGRESS.json`.

| stage | status | artifacts re-hashed | fixtures, re-run NOW | blockers |
|---|---|---|---|---|
| STEP 0 | **COMPLETE-VERIFIED** | 1 | `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 1)` exit 0, 0 red, no drift; `TIER-C10 STAGE 0a · RANGEFINDER CENSUS PORT FIXTURES (run 2, exit-code + reproducibility confirmation)` exit 0, 0 red, no drift | 0 |
| D-CORE | **PARTIAL** | 13 | `TIER-C10 Stage D fixtures — OFFLINE mode (no venue API)` exit 0, 0 red, no drift; `TIER-C10 Stage D fixtures — targeted named legs F-D-1 (matches F-D-1 and F-D-1b), ONLINE; these legs fetch the venue themselves and this mode writes no transcript` exit 1, 1 red, no drift | 7 |
| CENSUS-R{4h,1d} | **PARTIAL** | 372 | `CENSUS-R (TIER-C10 STAGE 0b) census fixtures` exit 0, 0 red, no drift | 3 |
| NULL/gaps-only | **COMPLETE-VERIFIED** | 312 | `F-NULL (scripts/tierc10_null_fixtures.py, --null-root=research_outputs/tierc10/null/gaps_only)` exit 0, 0 red, no drift | 0 |
| NULL/gaps+order | **COMPLETE-VERIFIED** | 312 | `tierc10_null_fixtures.py (F-NULL-COV, F-NULL-BOX, F-NULL-ASOF, F-NULL-SANE, F-NULL-GRID, F-NULL-DET) against --null-root=research_outputs/tierc10/null/gaps_order` exit 0, 0 red, no drift | 0 |
| A (stamps) | **COMPLETE-VERIFIED** | 10 | `Stage A — tierc10_stamps_fixtures.py (run 1 of 2)` exit 0, 0 red, no drift; `Stage A — tierc10_stamps_fixtures.py (run 2 of 2, timed)` exit 0, 0 red, no drift; `Stage A — scratch rebuild (my own extra determinism check; NOT the canonical root)` exit 0, 0 red, no drift | 0 |
| PANEL/gate | **COMPLETE-VERIFIED** | 11 | `TIER-C10 PANEL fixtures (scripts/tierc10_panel_fixtures.py)` exit 0, 0 red, no drift | 0 |
| LANES (B mech) | **PARTIAL** | 2 | `tierc10_lanes_fixtures` exit 0, 0 red, no drift | 7 |
| BRK (B mech) | **PARTIAL** | 2 | `F-BRK (scripts/tierc10_brk_fixtures.py) — 15 fixtures` exit 0, 0 red, no drift | 6 |

**Five stages are COMPLETE-VERIFIED.** STEP 0 reconciles 12/12 pins across
`pine/SS12_RangeFinder_v2.pine` ≡ the twin/engine ≡ the analytics port, key order included
(TOUCH_EPS 0.60 · DEV_RETURN_BARS 7 · BREAK_CONFIRM_N 8 · SCALE_MULT 3.0 · ATR_LEN 14); the Argus
note's *0.67 / DEV_RETURN 8* has **no on-disk source anywhere** — the only `0.67` in the lane is a
fixture's own sabotage plant. [Q-R5] holds: no RangeFinder constant is inherited from the SS
Breakout Scanner, whose source is not in this repo at all. PANEL passes 22/22 with 150/150 break
legs red and **F-CTRL at exactly 0.000e+00** over 12 columns on n=200, cross-process anchored to
the filed tierc9 journal. Both NULL variants re-hash to the byte and re-pass in ~485 s each.
Stage A's six contract stamps all exist and none is all-null.

**Four stages are PARTIAL**, and none of the four is partial because a number moved:

- **D-CORE / D-5M** — all 119 manifest shas re-hash (twice), the write-once seal holds on all four
  records, admission is 17/17 with zero gaps, and the suite's only red is the designed-red F-D-1.
  It is PARTIAL because **four RESUME-contract clauses have no artifact on disk**: F-D-4 (two-token
  trap), F-D-5 (data-spend audit), the tiered COSTS HAIRCUT TWIN, and contract multipliers.
- **CENSUS-R** — re-hashes clean across 8 root tables, 306 cell tables and 34 input tapes, re-passes
  at exit 0 / 11-11 green with a byte-identical transcript, and **every headline number reproduces
  from the parquet and again from the raw event ledgers**. It is PARTIAL because **[Q-R3]
  height-vs-toll and [Q-R4] the acceptance head-to-head do not exist** — zero occurrences of
  `height`, `acceptance`, `stale-run` or `time-beyond` in the engine, the port or the digest.
- **LANES** — the suite re-passes (exit 0, 10/10, 51/51 break legs red, zero drift) but the module
  carries a **confirmed blocking defect**, reproduced independently this session (§5).
- **BRK** — the card re-hashes, its F-DET twin is byte-identical, and all three of the prior
  review's repairs verify from source. It is PARTIAL because height-vs-toll is absent, no BRK row
  printer exists for a verdict to ride on, `LANE_ERA` is a declared pin nothing enforces, and
  `brk/` is the only stage directory with no `build_manifest.json`.

### R0.3 · Quarantined, and what was redone

**Quarantined** to `research_outputs/tierc10/_partial_20260922T0955Z/` (LAW 2 — never deleted): two
kill-partials from filtered fixture runs the 529 interrupted, `lanes/FIXTURES_LANES_partial.txt`
(4,692 B) and `panel/FIXTURES_PANEL_partial.txt` (6,552 B, reading `FIXTURE SUMMARY 1/1 PASS`).
Each recorded a few legs, not a suite, and sat beside the transcript of record where its "1/1 PASS"
could be misread as a verdict.

**Disclosed, not moved:** `census/smoke/` and `null/smoke/` are legitimate smoke roots with their
own manifests, but they carry full lookalike filenames and were built before the R1 bands and the
era split, so their contents are now wrong in substance. Moving them would change two suites'
fallback behaviour mid-resume. Rebuild or remove at CLOSE.

**Redone:** nothing was recomputed, because nothing had moved. The corridor never moved
(AS_OF 2026-09-21T16:00:00Z, substrate frozen, `live_cache_touched: false`). What R0 *did* redo is
every fixture suite in the build — that is what LAW 1 means by COMPLETE.

**Secured:** R0's most urgent finding was not a bug. `git status` showed all fifteen
`scripts/tierc10_*.py`, `analytics/rangefinder_census.py` and the three Stage-0a rangefinder edits
as untracked or modified, with one TC10 commit in the whole resume window — 29,913 lines that a
second 529 would have taken. Committed as `d19f857` before any further work.

---

## 1 · STAGE LOG

*One line per stage, appended as each completes (LAW 6).*

- **STEP Q** · 2026-09-22 · contract filed verbatim to `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`, sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a`, 9,441 bytes. The contract now survives any session.
- **R0 (rulings recovery)** · 2026-09-22 · the six operator rulings of 2026-09-21T22:46Z recovered verbatim from the dead session's transcript and filed to `research_outputs/tierc10/OPERATOR_RULINGS.md`, sha256 `70188a0cc32422be40e74d8e7adf7d444aa610bb3abf0384b4f4a2f66f57bbec`.
- **R0 (progress census)** · 2026-09-22 · ten agents; every fixture suite in the build re-run NOW per LAW 1; 1,035 artifact content-shas re-hashed independently. Ledger: 5 COMPLETE-VERIFIED (STEP 0, NULL/gaps-only, NULL/gaps+order, A, PANEL), 4 PARTIAL (D, CENSUS-R, LANES, BRK). `research_outputs/tierc10/PROGRESS.json` filed, 245,852 bytes.
- **R0 (LAW 6 repair)** · 2026-09-22 · the whole TC10 source tree committed as `d19f857` — 29,913 lines that were untracked and one 529 away from being lost.
- **R0 (LAW 2)** · 2026-09-22 · two kill-partials quarantined to `_partial_20260922T0955Z/`; the two stale smoke roots disclosed in place with reasons.

---

## 2 · CENSUS-R

*Tier-E. A SELECTION, not a result. Outcome-after-event, the acceptance head-to-head [Q-R4] and
height-vs-toll [Q-R3] prominent.*

---

## 3 · STAGE D MANIFEST

*Including the F-D-4 two-token-trap table and the F-D-5 data-spend audit.*

---

## 4 · THE FIXTURE TRANSCRIPT

---

## 5 · FINDINGS — REPORTED, NOT FIXED

---

## 6 · WHAT IS OPEN, AND WHO OWNS IT

---

## 7 · WHAT THIS BUILD IS NOT

---

## 8 · DISPOSITION · BOX-COST
