# HEPHAESTUS — retention fix, alarm verification, second-account reminder

**Date:** 2026-08-03 · **Branch:** `v12-v1-census` · **HEAD at start:** `484d62c`
**Environment:** Windows (`MINGW64_NT-10.0-26200`, `OS=Windows_NT`), repo root
`C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`

**Authorisation note:** `scripts/backup_estate.py` sits on the ARGUS lane's
DO-NOT-MODIFY list. This paste explicitly instructs amending it, so the
amendment is made under that instruction and recorded here.

---

## 0 · HEADLINE

| | |
|---|---|
| Flagged as prunable **before** | **8 archives, 1,025,216,046 B = 1,025.2 MB** |
| Flagged as prunable **after** | **0 archives, 0 B** |
| Alarm sections | both already present; **verified, not rebuilt** |
| New checks | second-account reminder (fires today) |
| New flag | `--force-same-day`, both paths fixtured |
| **Regression found and fixed** | **v1.1 brief had been HALTING since cycle 3** |

The reported figure was 978 MB. **Measured, it was 1,025.2 MB** — the report
understated it.

---

## 1 · THE RETENTION RULE — CORRECTED

### What was wrong

`scripts/backup_estate.py` carried `KEEP_PHASE_SETS = 1` and grouped phase
archives by date, keeping only the newest dated "set". The reasoning was that
the phases were archived in a batch and therefore aged as a batch.

**That reasoning is wrong, and wrong in a dangerous direction.** `s1`, `s2`,
`s3`, `tc1`, `tc4`, `tc5` and `v3_anchor` each hold a **different phase's
evidence**. An older phase archive is not a superseded copy of a newer one — it
is the only copy of work that will never be produced again.

A retention report that names unique evidence as prunable is worse than no
retention report, because it launders a deletion decision as routine
housekeeping.

### The same defect existed in a SECOND place

`scripts/daily_routine.py:_retention_violations()` carried its own copy of the
phase-set rule and read a `keep_phase_sets` key. **So the alarm was
independently reporting unique study evidence as "outside the rule" on every
run.** That is how a wrong rule becomes received wisdom — it gets restated by
two systems and starts to look corroborated. Both are now corrected.

### What the rule is now

- **estate** — keep newest **4** generations; older ones LISTED as prunable
- **workflow** — keep newest **4** generations; older ones LISTED as prunable
- **phase** — **NEVER prunable.** No keep-count exists. Reported under its own
  heading with the reason stated.

`KEEP_PHASE_SETS` is **removed**, not retuned.

### `exchange/status/RETENTION.md` — new phase section, verbatim

```
## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a
superseded copy of a newer one — it is the only copy of work that will never be
produced again.

Location: `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad\research_outputs\_archive`

9 archive(s), 1,043,591,544 B (1,043.6 MB). **All permanent. None prunable.**

| archive | date | size (B) | status |
|---|---|---|---|
| `analytics_tests_v1.0.0_2026-07-29.zip` | 2026-07-29 | 6,816 | **PERMANENT — never prune** |
| `analytics_v1.0.0_2026-07-29.zip` | 2026-07-29 | 19,641 | **PERMANENT — never prune** |
| `s1_2026-07-27.zip` | 2026-07-27 | 106,239,157 | **PERMANENT — never prune** |
| `s2_2026-07-27.zip` | 2026-07-27 | 246,355,294 | **PERMANENT — never prune** |
| `s3_2026-07-27.zip` | 2026-07-27 | 269,919,602 | **PERMANENT — never prune** |
| `tc1_2026-07-27.zip` | 2026-07-27 | 242,926,299 | **PERMANENT — never prune** |
| `tc4_2026-07-27.zip` | 2026-07-27 | 68,700,167 | **PERMANENT — never prune** |
| `tc5_2026-08-02.zip` | 2026-08-02 | 18,375,498 | **PERMANENT — never prune** |
| `v3_anchor_2026-07-27.zip` | 2026-07-27 | 91,049,070 | **PERMANENT — never prune** |

There is no keep-count for phase archives and no circumstance under which this
report will list one as prunable.
```

---

## 2 · ALARM VERIFICATION — both parts already present

| component | state | location |
|---|---|---|
| `## 0. ACTION REQUIRED` | **PRESENT** | `daily_routine.py:887` |
| writes `exchange/status/HEARTBEAT.md` | **PRESENT** | `daily_routine.py:979`, via `write_heartbeat()` |

Neither was missing, so the "add both now" branch did **not** apply. Every check
in the spec was verified to exist and to be computed from real state:

| check | present | ALERT threshold |
|---|---|---|
| days since newest estate zip | yes | > 8 |
| days since newest workflow zip | yes | > 8 |
| OPERATOR_PREFERENCES.md Part 1 empty, naming blocks | yes | any empty |
| days since newest file in `<dest>\operator-exports\` | yes | > 35 or empty |
| retention items prunable | yes | **now under the CORRECTED rule** |
| OneDrive.exe running | yes | not running |
| queue items lacking a RATIFIED stamp | yes | any |
| backup destination unreachable | yes | unreadable |

The destination check already refuses to let an unreachable drive read as a
healthy one — it reports UNKNOWN rather than "0 days since backup". That is the
right posture and was left alone.

---

## 3 · SECOND-ACCOUNT REMINDER — added

`_second_account_due()` compares the newest estate/workflow archive against a
date the operator records in `exchange/status/SECOND_ACCOUNT.md`.

**Why a written date and not a check:** that account has no API, no mounted
drive, nothing the script can read. It is a genuine blind spot. The only honest
mechanism is a date the operator maintains — and a missing or unreadable date
line is **itself an alert**, on the same principle as the unreachable-destination
check: an unknown state must never read as a healthy one.

`SECOND_ACCOUNT.md` was created with a header explaining the mechanism, what to
upload, and the note that phase archives are permanent and belong there too.

**It fires today** — see §6 item 4.

---

## 4 · `--force-same-day` — added

The no-clobber guard made no distinction between overwriting **yesterday's**
archive (a real loss) and re-running **today's** (ordinary). It had forced
**four manual archive deletions**. A safety rail that trains the operator to
delete archives by hand is doing harm.

With the flag, and **only** when the existing file was written today, the new
archive takes a `-NN` suffix and **both are kept**. Nothing is deleted, nothing
is overwritten. An archive from an earlier day still refuses, flag or no flag.

The refusal message now also tells you which case you are in.

### Fixture — F-K6, both paths, exercised directly

```
(1) target does not exist            -> returns target unchanged        True
(2) exists, NO flag                  -> refused, exit 3                 OK
(3) exists, written TODAY, WITH flag -> naiad_estate_2026-08-03-01.zip
        original still present: True      new not yet written: True
    second re-run                    -> naiad_estate_2026-08-03-02.zip  (increments)
(4) exists, EARLIER day, WITH flag   -> refused, exit 3   OK — same-day only

nothing overwritten: ['naiad_estate_2026-08-01.zip',
                      'naiad_estate_2026-08-03-01.zip',
                      'naiad_estate_2026-08-03.zip']
```

`fk6_no_clobber` in-script now asserts **both** paths plus the earlier-day
refusal (recorded as `F-K6b`). Asserting only the refusal would have let the new
flag silently become a clobber.

---

## 5 · ARCHIVE INVENTORY UNDER THE CORRECTED RULE

### ESTATE — `G:\My Drive\naiad-backups` · 2 archives, 985,849,379 B (985.8 MB)

| archive | size (B) | written | status |
|---|---:|---|---|
| `naiad_estate_2026-08-02.zip` | 493,542,600 | 2026-08-02 18:30 | within rule |
| `naiad_estate_2026-07-28.zip` | 492,306,779 | 2026-07-28 21:20 | within rule |

### WORKFLOW — `G:\My Drive\naiad-backups` · 1 archive, 1,132,236 B (1.1 MB)

| archive | size (B) | written | status |
|---|---:|---|---|
| `naiad_workflow_2026-08-02.zip` | 1,132,236 | 2026-08-02 18:22 | within rule |

### PHASE — `research_outputs\_archive` · 9 archives, 1,043,591,544 B (1,043.6 MB)

| archive | size (B) | written | status |
|---|---:|---|---|
| `analytics_tests_v1.0.0_2026-07-29.zip` | 6,816 | 2026-07-29 04:42 | PERMANENT |
| `analytics_v1.0.0_2026-07-29.zip` | 19,641 | 2026-07-29 02:56 | PERMANENT |
| `s1_2026-07-27.zip` | 106,239,157 | 2026-07-27 04:00 | PERMANENT |
| `s2_2026-07-27.zip` | 246,355,294 | 2026-07-27 03:57 | PERMANENT |
| `s3_2026-07-27.zip` | 269,919,602 | 2026-07-27 03:55 | PERMANENT |
| `tc1_2026-07-27.zip` | 242,926,299 | 2026-07-27 03:51 | PERMANENT |
| `tc4_2026-07-27.zip` | 68,700,167 | 2026-07-27 04:01 | PERMANENT |
| `tc5_2026-08-02.zip` | 18,375,498 | 2026-08-02 15:40 | PERMANENT |
| `v3_anchor_2026-07-27.zip` | 91,049,070 | 2026-07-27 03:59 | PERMANENT |

**TOTAL PRUNABLE UNDER THE CORRECTED RULE: 0 archives, 0 B.**
Under the old rule: **8 archives, 1,025,216,046 B**.

> **Only 2 estate generations and 1 workflow generation exist**, against a
> keep-4 rule. Nothing is near the threshold in either direction, so the rule is
> currently inert for generations — which is the correct state, not a reason to
> loosen it.

---

## 6 · ROUTINE RUN — section 0 and HEARTBEAT, verbatim

```
## 0. ACTION REQUIRED

**5 item(s) need attention.**

1. **no operator data export yet** — `G:\My Drive\naiad-backups\operator-exports` is empty. Project memory, preferences, instructions and custom style are not in any export, so this folder is the only route for the rest.
2. **operator preferences not captured** — 3 of 3 PART 1 blocks still empty: User preferences, Project instructions, Custom style. These exist only in Claude's cloud settings, are excluded from data exports, and can only be pasted by hand.
3. **OneDrive.exe is not running** — the repo lives inside the OneDrive tree, so nothing here is syncing to the cloud right now.
4. **manual upload to the second Google Drive account is outstanding** — the newest estate archive is 2026-08-02, but the last recorded manual upload was 2026-07-28. That account cannot be checked by machine; upload in the browser, then update the date line in `exchange/status/SECOND_ACCOUNT.md`.
5. **1 queue item(s) awaiting your ratification stamp**: 001. They are requests, not work, until stamped.
```

```
# HEARTBEAT
run: 2026-08-04T00:51:45Z
exit: 0 (jobs + window; publish outcome in the day's DAILY report)
overdue: 5
archives — estate: 2026-08-02 · workflow: 2026-08-02 · phase: 2026-08-02
```

**Item 4 is the new check, firing correctly on its first run.** Retention is
correctly **absent** from the list: under the corrected rule there are no
violations.

---

## 7 · 🔴 REGRESSION FOUND — the v1.1 brief had been HALTING since cycle 3

The routine reported `brief: exit=1`. Investigated rather than noted.

**`F-B3` was failing:** `UndecidableStepError: cannot infer source bar spacing
from 1 timestamp(s)`.

**Cause: mine.** Cycle 3's D-3 change routed `daily_brief.resample()` through
`analytics.structure.resample_ohlcv`, which — correctly, per Amendment 2 §1.2 —
**raises** on an undecidable step. The frozen fixture day contains a degenerate
one-bar slice, so the raise took the whole brief down with
`HALT: F-B3 failed — no partial adoption`.

**It has been failing since `d622b20` and I did not catch it**, for two reasons
worth recording:

1. the `brief` job is `required: false`, so the routine exited 0 and the failure
   never surfaced as a broken run;
2. **F-B1..F-B8 run inside `daily_brief.py`, not pytest** — so a green 248-test
   suite said nothing about them.

**Fix, at the caller and not in analytics.** The refusal is correct and stays:
analytics still guesses nothing. What was wrong is that the caller treated a
refusal as fatal. A timeframe that cannot be resampled now **degrades to empty**,
exactly as a failed Tier-2 fetch degrades under F-B6.

```
PASS F-B1 · PASS F-B2 · PASS F-B3 · PASS F-B4
PASS F-B5 · PASS F-B6 · PASS F-B7 · PASS F-B8
8/8 fixtures pass          exit 0
```

Full pytest suite unaffected: **248 passed, 1 skipped**.

### Also fixed while there

`brief2_capture` is `slot_aware` and `brief_capture.py` makes `--slot` required,
so a no-slot routine run would have failed it on argparse. A slot-aware job with
no slot is now **SKIPPED**, which is the honest state — it is inapplicable, not
broken.

---

## 8 · FILE DISPOSITION TABLE

| file | disposition | why | tracked | pushed |
|---|---|---|---|---|
| `scripts/backup_estate.py` | **MODIFIED** | `KEEP_PHASE_SETS` removed; phase section rewritten as permanent; `--force-same-day`; `assert_no_clobber` returns a path; F-K6 asserts both paths + F-K6b | yes | yes |
| `scripts/daily_routine.py` | **MODIFIED** | `_retention_violations` phase clause removed; `_second_account_due()` added and wired into section 0; slot-aware jobs SKIP without a slot | yes | yes |
| `scripts/daily_brief.py` | **MODIFIED** | regression fix — `UndecidableStepError` degrades to an empty frame instead of halting the brief | yes | yes |
| `exchange/status/SECOND_ACCOUNT.md` | **NEW** | the manual-upload date record; missing/unreadable is itself an alert | yes | yes |
| `exchange/status/RETENTION.md` | **REGENERATED** | 0 prunable, 9 phase archives PERMANENT | yes | yes |
| `exchange/status/HEARTBEAT.md` | **REGENERATED** | routine run | yes | yes |
| `exchange/status/daily/DAILY_2026-08-03.md` | **REGENERATED** | routine run | yes | yes |
| `exchange/status/MANIFEST.json` | **REGENERATED** | manifest job | yes | yes |
| `exchange/reports/2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md` | **NEW** | this report | yes | yes |
| `research_outputs/_archive/*.zip` (9) | **UNTOUCHED** | permanent evidence; nothing read, moved, renamed or deleted | no (gitignored) | no |
| `G:\My Drive\naiad-backups\*.zip` (3) | **UNTOUCHED** | inventoried read-only | no (external) | no |
| `analytics/*` | **UNTOUCHED** | §1.2's refusal is correct and stays | yes | yes |
| `scripts/publish_exchange.py` | **UNTOUCHED** | DO-NOT-MODIFY | yes | yes |
| `scripts/reviewer_manifest.py` | **UNTOUCHED** | DO-NOT-MODIFY | yes | yes |
| `engine/*`, `configs/*`, `study/*` | **UNTOUCHED** | DO-NOT-MODIFY | yes | yes |

**No archive was deleted, moved, renamed or opened for writing at any point.**

— HEPHAESTUS, 2026-08-03
