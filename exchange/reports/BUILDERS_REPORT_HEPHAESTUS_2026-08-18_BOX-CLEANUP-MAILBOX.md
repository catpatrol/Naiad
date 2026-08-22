# BUILDER'S REPORT — HEPHAESTUS — BOX CLEANUP, ROOT ORDER, MAILBOX

**Lane** HEPHAESTUS (local Claude Code at `~/Naiad`) · **Branch** `v12-v1-census` · **HEAD at start**
`4c6211d` · **Commissioned by** the operator directly, brief issued **2026-08-18** ("Operator go
2026-08-18") · **Executed** 2026-08-22.

> **THE FILENAME AND THE DATE DISAGREE, AND THE FILENAME IS THE OPERATOR'S.** The brief named this
> document `BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md`. The session ran on
> **2026-08-22**, four days later. The name is used exactly as issued — the operator's live
> instruction wins (CONVENTIONS §0, precedence 1) — and the date in it is the **go date**, not the
> build date. **Every age calculation in this document uses 2026-08-22**, the real one, because "14
> days old" is measured from now and measuring it from the go date would have kept six more
> documents hot on a false reading of their age. Both dates are stated wherever one could be
> mistaken for the other.

---

## 0 · WHAT THIS IS, IN PLAIN LANGUAGE

Six actors write into this repository. Three of them are web chats that can only see what is inside
a synced "project box"; the box holds `exchange/` and `LEDGER.md`, and it has a hard ceiling of
16,000,000 bytes. Every builder session adds one document to `exchange/reports/` by design, so the
box fills by construction. It stood at **24.07%** this morning.

Three things happened in this session, and **not one file was deleted**:

1. **The bus was rotated.** 86 documents that are finished — spent work orders, superseded status
   notes, and the whole infrastructure record of a Windows machine this project no longer runs on —
   were **moved** to `docs/history/`. They are still tracked, still on GitHub, still reachable, and
   `git log --follow` still returns their full history at the new path. They are simply no longer in
   the box the web lanes read.
2. **The root folder was swept.** 24 documents nobody's code refers to moved to `docs/history/` as
   well. Every single candidate was grepped across `scripts/`, `fixtures/`, `tests/` and `engine/`
   **before** it moved, and the check was re-run immediately before each `git mv`. 36 root documents
   turned out to be referenced by code; every one of them stayed exactly where it is.
3. **A mailbox was built.** `~/Naiad/MAILBOX` is a flat folder of shortcuts to whatever is current —
   the ledgers, the rules, every open work order, and the newest 25 reports. It rebuilds itself on
   every publish and every daily routine. Drag it into the Finder sidebar once and it stays right.

**The result: the box went from 24.07% to 15.19%.** Nothing is gone.

---

## 1 · THE RETENTION LAW, AS APPLIED

Verbatim from the brief, with the reading used for each clause where the clause needed one.

| clause | reading applied |
|---|---|
| KEEP-HOT: **all of `exchange/status/**` and `LEDGER.md`** | Literal. 16 status files + 14 dailies + `LEDGER.md` kept, including `2026-08-02_DELTA_W1-rulings-and-exchange.md` at 20 days old — location, not age, is what the clause names. |
| KEEP-HOT: **queue items not BUILT-and-spent (003, 008 + README)** | The **RULE** was applied, not the parenthetical — see finding **F-6**. `BUILT` was read by `reviewer_manifest.queue_items()`, the same parser `MANIFEST.json` uses, so the mailbox and the manifest cannot disagree about what is open. |
| KEEP-HOT: **the living working set, by name** | Literal, 7 of 8 present; `QUEUE-008-BUILD` is "when present" and is not yet filed. It is pinned by glob, so it joins the mailbox the day it lands without anyone editing a list. |
| KEEP-HOT: **the newest NOTE per lane pair** | Applied mechanically: sender→recipient parsed from the filename, broadcasts grouped as `<LANE>→ALL-LANES`, newest by filename date then mtime. This **overrides age** — it kept `NOTE_ARGUS_to_ATHENA_2026-08-03` (19 d) and `NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings` (18 d) hot, and rotated the four notes that a newer note of the same pair supersedes. |
| KEEP-HOT: **anything <14 days old NOT superseded by a successor document** | Cutoff 2026-08-09 (age < 14 from 2026-08-22). **"Superseded" was held to mean a successor that can be NAMED** — the table below prints the successor's filename for every one of the 33 rotated on this ground. Where no successor could be named, the file stayed, even where it looked stale. That is why `BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` and both VIZ design contracts are still on the bus. |
| ROTATE: **the Windows-era infra reports** | The 15 HEPHAESTUS infra reports dated 2026-08-11 and 2026-08-12 describe OneDrive, drive letters, Task Scheduler and a machine that was replaced on 2026-08-14/15. Successor named for each: `M3-SWEEP` / `M4-LAUNCHD`. |
| ROTATE: **spent queue items 001/002/004/005/006** | 001, 002 and 004 exist and rotated. **005 and 006 do not exist** — enumerated, finding **F-7**. |

**Destination.** Reports keep queue-003 D-1's `YYYY-MM` date bucket rather than landing in one
folder, so four July documents went to `docs/history/reports/2026-07/`. The brief named
`docs/history/reports/2026-08/`; D-1's bucketing was used instead **because the brief also says
"003 semantics"**, and because a layout the script cannot reproduce later is a layout that will
drift. Queue work orders went to `docs/history/queue/` exactly as instructed.

---

## 2 · THE INVENTORY — every file on the bus, with its verdict

187 files: `exchange/**` as tracked in the index at `4c6211d`, plus `LEDGER.md`. **86 ROTATE,
101 KEEP-HOT.** Sizes are the tracked blob sizes that the box budget actually meters, not on-disk
sizes — the two differ for the untracked `exchange/queue/.DS_Store`, which is not in the box at all
(its sibling `exchange/.DS_Store` **is**, and that is finding **F-1**).

| path | bytes | mtime | age d | verdict | why |
|---|--:|---|--:|:-:|---|
| `exchange/queue/001_condensed-project-history.md` | 5,796 | 2026-08-05 21:12 | 20 | **ROT** | operator-named spent; ratified 08-06, no BUILT stamp — see finding F-3 |
| `exchange/queue/002_backup-and-publish-guards.md` | 8,801 | 2026-08-11 23:28 | 17 | **ROT** | BUILT c32ffa5 — spent |
| `exchange/queue/004_move-clone-out-of-onedrive.md` | 7,725 | 2026-08-12 05:40 | 10 | **ROT** | operator-named spent; Phase A accepted, Phase B mooted by the Mac crossing (queue 005) |
| `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | 4,031 | 2026-08-11 23:28 | 19 | **ROT** | BUILT WF1_tables.md — spent |
| `exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | 10,860 | 2026-08-12 09:41 | 18 | **ROT** | BUILT BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md — spent |
| `exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md` | 9,494 | 2026-08-11 23:29 | 16 | **ROT** | BUILT BUILD_APOLLO_2026-08-06_MC1.md — spent |
| `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` | 25,756 | 2026-08-12 17:55 | 10 | **ROT** | CENSUS-2A contract SPENT (ROTATION_LOG 2026-08-15 block); closeout kept hot |
| `exchange/queue/2026-08-16_BR1_brief_redesign_ARGUS.md` | 8,152 | 2026-08-16 04:36 | 6 | **ROT** | BUILT BUILD_2026-08-16_ORACLE_REBIRTH.md — spent |
| `exchange/queue/2026-08-16_BR1b_oracle_topup_ARGUS.md` | 3,414 | 2026-08-16 04:19 | 6 | **ROT** | BUILT BUILD_2026-08-16_ORACLE_TOPUP.md — spent |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_ai-operating-system.md` | 11,836 | 2026-08-02 15:29 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_backup-catchup-and-reminders.md` | 13,869 | 2026-08-02 18:40 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_coverage-and-identity.md` | 16,705 | 2026-08-02 18:25 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_disposition-inventory.md` | 33,556 | 2026-08-02 16:36 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-slimming.md` | 12,178 | 2026-08-02 16:21 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_exchange-v1-build.md` | 46,324 | 2026-08-02 14:31 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-02_HEPHAESTUS_report_tc5-archive-and-scaffolding.md` | 17,401 | 2026-08-02 15:44 | 20 | **ROT** | age 20d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-03_HEPHAESTUS_report_retention-fix-and-alarm.md` | 14,330 | 2026-08-03 22:09 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-04_ATHENA_handoff_orphan-data-files.md` | 3,180 | 2026-08-05 02:19 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-04_ATHENA_s3-journal-restore.md` | 2,588 | 2026-08-04 16:25 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | 7,484 | 2026-08-04 20:49 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | 2,876 | 2026-08-04 00:21 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/APOLLO_LANE_STATUS_2026-08-15.md` | 5,446 | 2026-08-16 00:28 | 7 | **ROT** | ← APOLLO_SESSION_REPORT_2026-08-16.md |
| `exchange/reports/APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md` | 13,476 | 2026-08-12 07:30 | 10 | **ROT** | ← APOLLO_LANE_STATUS_2026-08-15.md → APOLLO_SESSION_REPORT_2026-08-16.md |
| `exchange/reports/ARGUS_PANTHEON_REPORT_2026-08-06.md` | 23,454 | 2026-08-05 20:46 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/ATHENA_STATUS_2026-08-01.md` | 19,086 | 2026-08-02 12:01 | 21 | **ROT** | age 21d >= 14d, no keep-rule reaches it |
| `exchange/reports/BACKUP_BUILD_2026-07-28.md` | 12,174 | 2026-07-28 21:23 | 25 | **ROT** | age 25d >= 14d, no keep-rule reaches it |
| `exchange/reports/BRIEF2_CALIBRATION_2026-08-05.json` | 3,773 | 2026-08-12 07:46 | 17 | **ROT** | age 17d >= 14d, no keep-rule reaches it |
| `exchange/reports/BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md` | 3,383 | 2026-08-17 03:01 | 6 | **ROT** | ← BUILD_2026-08-16_PINE_ESTATE_V12_6.md (filed 08-21) |
| `exchange/reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` | 34,971 | 2026-08-04 17:14 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_CONVENTIONS.md` | 26,774 | 2026-08-04 01:54 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md` | 22,478 | 2026-08-04 00:41 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_WRAPUP.md` | 22,201 | 2026-08-04 02:23 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ANALYTICS-ARCHIVES-AND-EXCHANGE-SIZING.md` | 23,480 | 2026-08-04 23:58 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ARCHIVE-VERIFY-AND-QUEUE-002.md` | 21,444 | 2026-08-05 02:22 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md` | 19,934 | 2026-08-04 23:01 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_EXCHANGE-GUARD-ENFORCEMENT.md` | 22,812 | 2026-08-05 00:17 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` | 33,748 | 2026-08-04 21:35 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SIDECARS-AND-LANE-CLOSE.md` | 18,014 | 2026-08-05 02:40 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_TC5-OFFSITE-AND-PHASE-MODE-READ.md` | 35,526 | 2026-08-04 23:46 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-06_ARCHIVE-RELOCATION-D.md` | 22,227 | 2026-08-11 19:19 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_BULK-RELOCATION-SEQ8-UNARCHIVED.md` | 20,685 | 2026-08-11 20:00 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-002.md` | 22,065 | 2026-08-11 20:42 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-FILED.md` | 6,662 | 2026-08-11 20:49 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003-RATIFIED.md` | 10,749 | 2026-08-11 20:56 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-003.md` | 17,335 | 2026-08-11 21:12 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_R1-R2-R3.md` | 17,277 | 2026-08-11 20:20 | 11 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_BACKUP-PATH-REROUTE.md` | 31,324 | 2026-08-12 02:53 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md` | 33,372 | 2026-08-12 00:15 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md` | 16,407 | 2026-08-12 03:29 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md` | 23,178 | 2026-08-12 03:49 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md` | 11,834 | 2026-08-12 00:37 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md` | 35,498 | 2026-08-12 07:22 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-FILED-AND-D0A.md` | 42,181 | 2026-08-12 06:00 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md` | 28,705 | 2026-08-12 05:21 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md` | 26,876 | 2026-08-12 08:12 | 10 | **ROT** | ← M3-SWEEP / M4-LAUNCHD (Windows-era infra) |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-14_M2-RESTORE.md` | 31,142 | 2026-08-15 01:14 | 8 | **ROT** | ← BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M2-RESTORE-V2.md |
| `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` | 18,973 | 2026-08-05 20:36 | 17 | **ROT** | age 17d >= 14d, no keep-rule reaches it |
| `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` | 14,277 | 2026-08-11 22:10 | 10 | **ROT** | ← BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007-LANE-CLOSE.md (lane dormant) |
| `exchange/reports/BUILD_2026-08-12_CENSUS2A_PASTE1.md` | 41,307 | 2026-08-12 12:05 | 10 | **ROT** | ← CENSUS2A_CLOSEOUT_2026-08-12.md (contract spent) |
| `exchange/reports/BUILD_2026-08-12_CENSUS2A_VIZ1.md` | 17,525 | 2026-08-12 19:36 | 10 | **ROT** | ← CENSUS2A_CLOSEOUT_2026-08-12.md (contract spent) |
| `exchange/reports/BUILD_APOLLO_2026-08-06_MC1.md` | 38,482 | 2026-08-10 00:42 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/CENSUS2A_CONTRACT_DRAFT_v0.2_2026-08-12.md` | 13,405 | 2026-08-12 10:26 | 10 | **ROT** | ← CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md |
| `exchange/reports/CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md` | 12,887 | 2026-08-12 12:49 | 10 | **ROT** | ← CENSUS2A_CLOSEOUT_2026-08-12.md (contract spent) |
| `exchange/reports/CONTRACT_V4_2026-07-28.md` | 16,887 | 2026-07-28 22:16 | 25 | **ROT** | age 25d >= 14d, no keep-rule reaches it |
| `exchange/reports/DESIGN_BRIEF_CENSUS2A_VIZ_2026-08-12.md` | 6,067 | 2026-08-15 22:47 | 10 | **ROT** | ← BUILD_2026-08-12_CENSUS2A_VIZ1.md |
| `exchange/reports/EXCURSION_EPISODES_2026-08-06.json` | 9,077 | 2026-08-12 07:46 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/FIXUP_2026-07-28.md` | 13,598 | 2026-07-28 21:09 | 25 | **ROT** | age 25d >= 14d, no keep-rule reaches it |
| `exchange/reports/MC1_results.json.pointer.md` | 362 | 2026-08-11 23:30 | 11 | **ROT** | ← spent MC1 family (queue 2026-08-06_MC1 rotates in this sweep) |
| `exchange/reports/MC1_tables.md` | 18,887 | 2026-08-10 00:37 | 12 | **ROT** | ← spent MC1 family (queue 2026-08-06_MC1 rotates in this sweep) |
| `exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | 18,065 | 2026-08-03 20:40 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` | 9,986 | 2026-08-12 08:42 | 10 | **ROT** | ← NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS (newer, same pair) |
| `exchange/reports/NOTE_ATHENA_2026-08-12_CROSS-LANE-RECONCILIATION.md` | 6,638 | 2026-08-12 06:56 | 10 | **ROT** | ← NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS (newer, same pair) |
| `exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | 7,275 | 2026-08-04 17:35 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/PUSH_2026-07-28.md` | 3,430 | 2026-07-28 23:42 | 25 | **ROT** | age 25d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` | 10,714 | 2026-08-05 19:46 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-06_C6.md` | 9,368 | 2026-08-05 19:27 | 16 | **ROT** | age 16d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` | 9,514 | 2026-08-04 00:21 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-WORKSTREAM.md` | 8,859 | 2026-08-04 03:32 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` | 6,705 | 2026-08-04 20:37 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/SESSION_SUMMARY_HEPHAESTUS_2026-08-04_SEQ8.md` | 10,412 | 2026-08-04 21:34 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `exchange/reports/SETUP_2026-07-28.md` | 19,691 | 2026-08-05 02:18 | 25 | **ROT** | age 25d >= 14d, no keep-rule reaches it |
| `exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md` | 8,282 | 2026-08-03 18:55 | 19 | **ROT** | age 19d >= 14d, no keep-rule reaches it |
| `exchange/reports/STATUS_ATHENA_2026-08-11_LANE-CLOSE.md` | 5,259 | 2026-08-11 21:13 | 11 | **ROT** | ← NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS (status refresh) |
| `exchange/reports/STATUS_ATHENA_2026-08-11_LANE-CLOSEOUT.md` | 8,744 | 2026-08-11 21:31 | 11 | **ROT** | ← NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS (status refresh) |
| `exchange/reports/WF1_discriminants.json.pointer.md` | 374 | 2026-08-11 23:30 | 11 | **ROT** | ← spent WF1 family (queue 2026-08-03_WF1 rotates in this sweep) |
| `exchange/reports/WF1_tables.md` | 29,660 | 2026-08-04 17:09 | 18 | **ROT** | age 18d >= 14d, no keep-rule reaches it |
| `LEDGER.md` | 259,298 | 2026-08-15 20:59 | 44 | keep | rule: LEDGER.md |
| `exchange/.DS_Store` | 8,196 | 2026-08-18 17:45 | 7 | keep | FINDING F-1: tracked Finder blob; untracking is a deletion — out of scope |
| `exchange/DIGEST.md` | 561 | 2026-08-15 22:53 | 20 | keep | structural folder document / retired-DIGEST tombstone |
| `exchange/README.md` | 2,163 | 2026-08-15 22:26 | 20 | keep | structural folder document / retired-DIGEST tombstone |
| `exchange/drops/README.md` | 561 | 2026-08-02 12:10 | 20 | keep | structural folder document / retired-DIGEST tombstone |
| `exchange/queue/003_report-rotation-and-provenance.md` | 5,374 | 2026-08-11 20:55 | 11 | keep | rule: queue item not BUILT-and-spent |
| `exchange/queue/008_sail-skeleton.md` | 64,058 | 2026-08-18 04:04 | 4 | keep | rule: queue item not BUILT-and-spent |
| `exchange/queue/2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md` | 3,122 | 2026-08-16 05:07 | 6 | keep | rule: queue item not BUILT-and-spent |
| `exchange/queue/README.md` | 967 | 2026-08-11 23:28 | 20 | keep | rule: queue item not BUILT-and-spent |
| `exchange/reports/APOLLO_SESSION_REPORT_2026-08-16.md` | 42,538 | 2026-08-17 02:49 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/ARGUS_RESCOPE_2026-08-15.md` | 8,250 | 2026-08-16 00:28 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/ARGUS_VIZ_RENDER_AUDIT_2026-08-16.md` | 1,431 | 2026-08-16 01:25 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BRIEF_ATHENA_SAIL_REPO_2026-08-17.md` | 5,171 | 2026-08-17 05:05 | 5 | keep | rule: named living working set |
| `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` | 30,800 | 2026-08-11 22:44 | 11 | keep | rule: <14 days old (11d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_BOX-GOVERNANCE.md` | 9,624 | 2026-08-15 19:06 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_COLLAPSE.md` | 36,926 | 2026-08-15 21:25 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M2-RESTORE-V2.md` | 31,219 | 2026-08-15 02:32 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M3-SWEEP.md` | 21,786 | 2026-08-15 03:03 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md` | 68,524 | 2026-08-15 13:20 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007-LANE-CLOSE.md` | 15,352 | 2026-08-16 00:47 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_RULING-007.md` | 22,240 | 2026-08-15 22:59 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_ZIP-RESIDENCY.md` | 26,301 | 2026-08-15 13:57 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-17_SAIL-STEP1-INVENTORY.md` | 54,645 | 2026-08-18 01:21 | 5 | keep | rule: named living working set |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-18_QUEUE-008-FILED.md` | 15,642 | 2026-08-18 04:06 | 4 | keep | rule: named living working set |
| `exchange/reports/BUILD_2026-08-12_CENSUS2B_VULT1.md` | 105,838 | 2026-08-14 07:26 | 10 | keep | rule: <14 days old (10d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md` | 97,369 | 2026-08-14 13:53 | 8 | keep | rule: <14 days old (8d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-15_CENSUS2B_ORACLE.md` | 44,301 | 2026-08-15 17:15 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-15_TIERC2_BASELINE.md` | 37,459 | 2026-08-15 20:22 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-15_TIERC3_RAILED.md` | 39,595 | 2026-08-15 23:19 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-15_VIZ2_CATHEDRAL.md` | 12,843 | 2026-08-15 18:13 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-15_VIZ4_MANTLE.md` | 12,735 | 2026-08-15 21:57 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_ORACLE_A2_CLOSE.md` | 12,075 | 2026-08-16 04:43 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md` | 30,817 | 2026-08-16 02:51 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_ORACLE_TOPUP.md` | 21,618 | 2026-08-16 04:19 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_PINE_ESTATE_V12_6.md` | 51,923 | 2026-08-21 21:31 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_TIERC4_MEANCARD.md` | 69,480 | 2026-08-16 19:15 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_TIERC5_FULLWATER.md` | 45,902 | 2026-08-17 00:38 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-16_TIERC6_REVB.md` | 39,827 | 2026-08-17 22:54 | 6 | keep | rule: named living working set |
| `exchange/reports/BUILD_2026-08-17_TC6V_TIERC7.md` | 36,297 | 2026-08-18 00:33 | 5 | keep | rule: <14 days old (5d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-18_TC7C_TC8.md` | 19,902 | 2026-08-18 01:41 | 4 | keep | rule: <14 days old (4d), no successor document nameable |
| `exchange/reports/BUILD_2026-08-18_TIERC9_HABITAT_PAIRS.md` | 20,870 | 2026-08-22 01:04 | 4 | keep | rule: <14 days old (4d), no successor document nameable |
| `exchange/reports/CENSUS2A_CLOSEOUT_2026-08-12.md` | 19,464 | 2026-08-15 22:47 | 10 | keep | rule: named living working set |
| `exchange/reports/CENSUS2A_PROBE_LEDGER.md` | 17,767 | 2026-08-15 17:40 | 10 | keep | rule: <14 days old (10d), no successor document nameable |
| `exchange/reports/DEFINITIONS_D_H_2026-08-16.md` | 11,075 | 2026-08-17 03:31 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` | 4,216 | 2026-08-15 22:47 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md` | 3,857 | 2026-08-15 21:42 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15_1.md` | 3,857 | 2026-08-15 22:47 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/HANDOFF_APOLLO_NAIAD_SUCCESSION_2026-08-17.md` | 5,524 | 2026-08-17 11:10 | 5 | keep | rule: named living working set |
| `exchange/reports/INCIDENT_ORACLE_2026-08-20_CRASH.md` | 24,918 | 2026-08-22 02:13 | 2 | keep | rule: <14 days old (2d), no successor document nameable |
| `exchange/reports/LANE_UPDATE_DIONYSUS_2026-08-13_BR-momentum_winner-zoom_brief-feedback.md` | 15,571 | 2026-08-14 09:27 | 9 | keep | rule: <14 days old (9d), no successor document nameable |
| `exchange/reports/MEMORY_MODEL_APOLLO_LIGHT_AND_MEASURE_2026-08-17.md` | 1,733 | 2026-08-17 11:10 | 5 | keep | rule: <14 days old (5d), no successor document nameable |
| `exchange/reports/NOTE_APOLLO_2026-08-15_TO_ATHENA_box-governance-handoff.md` | 3,090 | 2026-08-15 19:04 | 7 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-16_rulings_relay.md` | 2,627 | 2026-08-16 04:41 | 6 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md` | 4,375 | 2026-08-03 14:09 | 19 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` | 6,371 | 2026-08-15 18:45 | 7 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_ATHENA_to_APOLLO_2026-08-11_data-residency.md` | 1,747 | 2026-08-11 21:13 | 11 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md` | 4,728 | 2026-08-12 07:05 | 11 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_DIONYSUS_2026-08-12_PANTHEON_lane_status_and_census_challenge.md` | 7,767 | 2026-08-12 09:53 | 10 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` | 5,645 | 2026-08-05 21:14 | 18 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_HEPHAESTUS_2026-08-15_TO_ATHENA_digest-refresh-contract-draft.md` | 19,216 | 2026-08-15 21:35 | 7 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_HERMES_2026-08-12_ALL-LANES_DIGEST-REFRESH.md` | 15,000 | 2026-08-12 09:03 | 10 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/NOTE_HERMES_to_ATHENA_2026-08-12_STALE-CLONE-DETECTION.md` | 10,707 | 2026-08-12 09:31 | 10 | keep | rule: newest NOTE of its lane pair |
| `exchange/reports/ORACLE_CHAIN_CLOSE_2026-08-16.md` | 16,162 | 2026-08-16 05:07 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/PINE_LANE_PRIMER_2026-08-15.md` | 4,454 | 2026-08-16 00:28 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/PRIMER_APOLLO_LIGHT_AND_MEASURE_2026-08-17.md` | 6,191 | 2026-08-17 11:10 | 5 | keep | rule: <14 days old (5d), no successor document nameable |
| `exchange/reports/PRIMER_HERMES_2026-08-11_v4.md` | 8,822 | 2026-08-16 00:44 | 11 | keep | rule: <14 days old (11d), no successor document nameable |
| `exchange/reports/README.md` | 533 | 2026-08-02 12:10 | 20 | keep | structural folder document / retired-DIGEST tombstone |
| `exchange/reports/RULES_OF_RECORD_VIZ_IRON_2026-08-15.md` | 913 | 2026-08-15 22:40 | 7 | keep | rule: <14 days old (7d), no successor document nameable |
| `exchange/reports/SESSION_REPORT_PANTHEON_APOLLO_2026-08-17.md` | 3,060 | 2026-08-17 11:10 | 5 | keep | rule: <14 days old (5d), no successor document nameable |
| `exchange/reports/SSV12_LOGIC_2026-08-16.md` | 8,922 | 2026-08-17 02:36 | 6 | keep | rule: <14 days old (6d), no successor document nameable |
| `exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md` | 31,822 | 2026-08-06 11:42 | 16 | keep | rule: named living working set |
| `exchange/status/2026-08-02_DELTA_W1-rulings-and-exchange.md` | 6,506 | 2026-08-02 13:44 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/CADENCE.md` | 10,441 | 2026-08-22 02:13 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/CONVENTIONS.md` | 67,752 | 2026-08-22 02:12 | 18 | keep | rule: ALL of exchange/status/** |
| `exchange/status/HEARTBEAT.md` | 175 | 2026-08-21 07:00 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/INTERFACE_PUBLISHED.md` | 48,885 | 2026-08-11 22:05 | 11 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_APOLLO.md` | 174,090 | 2026-08-22 01:05 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_ARGUS.md` | 24,241 | 2026-08-22 02:16 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_ATHENA.md` | 118,571 | 2026-08-18 04:06 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_DIONYSUS.md` | 5,685 | 2026-08-14 08:45 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_HEPHAESTUS.md` | 14,061 | 2026-08-15 22:59 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/LEDGER_HERMES.md` | 8,567 | 2026-08-16 00:48 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/MANIFEST.json` | 24,929 | 2026-08-21 07:00 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/README.md` | 554 | 2026-08-02 12:10 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/RETENTION.md` | 3,175 | 2026-08-15 13:53 | 20 | keep | rule: ALL of exchange/status/** |
| `exchange/status/ROTATION_LOG.md` | 2,744 | 2026-08-22 02:12 | 7 | keep | rule: ALL of exchange/status/** |
| `exchange/status/SECOND_ACCOUNT.md` | 2,941 | 2026-08-12 02:44 | 19 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-13.md` | 4,966 | 2026-08-13 07:05 | 9 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-14.md` | 5,064 | 2026-08-14 07:12 | 8 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-15.md` | 5,469 | 2026-08-15 13:14 | 7 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-17.md` | 6,962 | 2026-08-17 07:00 | 5 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-19.md` | 6,790 | 2026-08-19 07:00 | 3 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-20.md` | 6,363 | 2026-08-20 07:00 | 2 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/DAILY_2026-08-21.md` | 6,363 | 2026-08-21 07:00 | 1 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-13.json` | 23,755 | 2026-08-13 07:00 | 9 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-14.json` | 23,924 | 2026-08-14 07:00 | 8 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-15.json` | 24,039 | 2026-08-15 13:04 | 7 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-17.json` | 24,848 | 2026-08-17 07:00 | 5 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-19.json` | 24,906 | 2026-08-19 07:00 | 3 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-20.json` | 24,929 | 2026-08-20 07:00 | 2 | keep | rule: ALL of exchange/status/** |
| `exchange/status/daily/MANIFEST_2026-08-21.json` | 24,929 | 2026-08-21 07:00 | 1 | keep | rule: ALL of exchange/status/** |

---

## 3 · THE ROTATION LEDGER

**Method, per file, unchanged from the M4 precedent (`BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md` §3):**
`sha256` → `git mv` → `sha256` again at the destination → **require equal**, and halt the whole
sweep on any mismatch. The sweep was driven by importing `scripts/rotate_reports.py`'s own
primitives (`sha256_file`, `git`, `append_log`), so the hash discipline and the move-never-destroy
invariant are **the same code**, not a re-implementation of it.

| | |
|---|---|
| files moved | **86** |
| bytes moved off the bus | **1,420,757** |
| sha256 mismatches | **0** |
| source files left behind | **0** |
| delete calls executed | **0** — `rotate_reports.py` contains none, and this sweep added none |
| `ROTATION_LOG.md` rows appended | **86**, one per file, each carrying the destination path and the destination hash |
| destination | `docs/history/reports/2026-08/` (72) · `2026-07/` (5) · `docs/history/queue/` (9 work orders) |

The 86 sha256 values are **in `exchange/status/ROTATION_LOG.md`**, one row each, under a provenance
block that states what this named set was and why it was not the scheduled sweep. They are not
duplicated here: one fact, one home.

**History follows — the F-303-3 property, spot-checked on one file of each class after the commit:**

```
$ git log --follow --oneline -- docs/history/reports/2026-08/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_CLOSEOUT.md
98951cd box: named-set rotation, root sweep, and the MAILBOX
7552d65 exchange: auto-publish 2026-08-11
4479606 exchange: auto-publish 2026-08-12

$ git log --follow --oneline -- docs/history/queue/002_backup-and-publish-guards.md
98951cd box: named-set rotation, root sweep, and the MAILBOX
e835755 exchange: auto-publish 2026-08-11
7a9f999 exchange: auto-publish 2026-08-06
d223801 exchange: auto-publish 2026-08-06

$ git log --follow --oneline -- docs/history/reports/2026-07/REVIEWER_HANDOFF_2026-07-12.md
98951cd box: named-set rotation, root sweep, and the MAILBOX
7f1b4a9 hygiene: v11.3 manual v2.0 at root, ...
```

All 110 moves were recorded by git as **`R100`** — a rename at 100% similarity, which is the same
fact the sha256 pair asserts, arrived at independently.

**Why both halves of every move are in ONE commit.** `git mv` stages a deletion under `exchange/`
and an addition under `docs/`. Splitting them across two commits would have cost the
`git log --follow` property above, and leaving the `docs/` half staged when `publish()` runs is
exactly the failure M4 hit on 2026-08-15 — *"FLAG: publish aborted -- 8 staged path(s) outside
exchange/"*. So the rotation was committed first, whole, and the publish then carried only the
`exchange/` edits. This is a deliberate, precedent-backed reading of §3.4's "commit non-exchange
paths explicitly, in their own authorized commit": the commit is attended, named, and pushes no
evidence.

### 3.1 · Citation repointing — what was repointed and what was deliberately not

The brief: *"grep the STATUS layer only for moved paths and repoint; historical documents keep their
old citations per the history rule — note that in the log."*

Grepping `exchange/status/**` for all 110 moved basenames returned **19 references across 6 files**,
over 18 distinct moved names. (`ROTATION_LOG.md` matches 86 more; those are the rows this session
just wrote, and they already carry the new paths.) The 19 split two ways, and the split is a
judgment worth stating rather than burying:

| file | citation | action | why |
|---|---|---|---|
| `exchange/status/CONVENTIONS.md` | `ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | **REPOINTED** | A live rule asserting where its own probe evidence lives. A live assertion with a dead path is a false statement, not a historical one. |
| `exchange/status/CADENCE.md` | `SCHED_TEST_RESULT_2026-08-02.md` | **REPOINTED** | Same: a live cadence document telling a reader where the F4 result is. |
| `exchange/status/LEDGER_ATHENA.md` (12 refs / 11 names) | `004_*`, six `BUILDERS_REPORT_*2026-08-12*`, `M2-RESTORE`, `SS_Reassessment_*` | **left as written** | A lane ledger is an **append-only dated record**. Rewriting a 2026-08-12 entry to name a path that did not exist until 2026-08-22 falsifies what that entry said on the day. |
| `exchange/status/LEDGER_APOLLO.md` (2) | `MC1_tables.md` · `HANDOFF_2026-07-22_Census_to_Census1b.md` | **left as written** | Same. |
| `exchange/status/LEDGER_HEPHAESTUS.md` | `2026-08-02_HEPHAESTUS_report_exchange-v1-build.md` | **left as written** | Same. |
| `exchange/status/2026-08-02_DELTA_W1-rulings-and-exchange.md` (2) | `001_condensed-project-history.md` · `SCHED_TEST_RESULT_2026-08-02.md` | **left as written** | A dated snapshot. It sits under `status/` by location but it is a historical document by kind, and the history rule reaches it. |

**So the rule applied is: repoint what ASSERTS, leave what RECORDS.** Both repointed files name the
rotation date inline, so a reader meets the change rather than a silently different path.

**Anchor context, printed before writing, per queue-003 D-4** (which binds any paste editing
`CONVENTIONS.md`, and is applied to `CADENCE.md` too rather than reading the rule narrowly):

```
=== exchange/status/CONVENTIONS.md  (anchor occurs 1 time(s), line 854) ===
  851
  852   **RULE — A rule with no probe coverage is a rule on trust. Name the uncovered ones ...**
  853   BECAUSE rules covered only by operator inspection are ones you notice if a lane drops them ...
  854 >>EARNED-BY Memory-restructure acceptance, 2026-08-03. **Pass requires ≥5 of 6 behaviours ...
  855
  856
  857   **Who does what.** ATHENA drafts every change. You ratify it. HEPHAESTUS writes and publishes it.
--- WRITTEN: 67752 B -> 67814 B (+62) ---

=== exchange/status/CADENCE.md  (anchor occurs 1 time(s), line 122) ===
  119   Ruled at 2×/day (Q-4 A). Still not armed, but **the reason has changed** — and the change is worth
  120   reading before anyone arms it.
  121
  122 >>**F4 has a result** (`SCHED_TEST_RESULT_2026-08-02.md`, run 2026-08-02T15:00:50Z, unattended):
  123
  124   > **READ = yes · LIST = yes · WRITE = yes.** A scheduled Cowork run **does** see the mounted local
  125   > repo folder. The working assumption that "scheduled = remote = GitHub-only" is **wrong**.
--- WRITTEN: 10441 B -> 10503 B (+62) ---
```

Occurrence count asserted as **1** before each write, and the document re-read after (§6.4
corollary). `CONVENTIONS.md` is 67,814 B against F-CONV-4's 68,500 B ceiling — **686 B of headroom**,
and the fixture re-ran green after the edit.

> **Ownership, stated because CONVENTIONS §0 restricts it.** *"ATHENA drafts every change. You
> ratify it. HEPHAESTUS writes and publishes it."* This edit is a **path repoint, not a rule
> change** — no RULE, BECAUSE or EARNED-BY line was touched, the rule count held at 89, and the
> census is unchanged at 422→422. It was made under the operator's direct instruction to repoint the
> status layer. If ATHENA judges that even a repoint needs her draft, this is the line to revert.

### 3.2 · What the rotation did to the queue counters — say it, do not let it be discovered

`MANIFEST.json` counts work orders by globbing `exchange/queue/`. Nine of twelve moved, so:

| counter | before | after | why it moved |
|---|--:|--:|---|
| `queue_total` | 12 | **3** | 9 spent work orders relocated to `docs/history/queue/` |
| `queue_unratified` | 1 | **0** | the CENSUS-2A v0.3 contract rotated; it was spent in fact, unstamped in form |
| `queue_ratified_unbuilt` / `queue_open` | 5 | **3** | 003, 008, BR-2 remain — **but two of the two points lost are RELOCATION, NOT COMPLETION** |

**That last row is finding F-3 and it matters.** Queue 001 and 004 were rotated on the operator's
explicit naming while carrying **no `BUILT` stamp and no `WITHDRAWN` stamp**. The backlog counter
will read 3 from the next daily run onward and will not say that two of the five it used to count
are sitting in `docs/history/queue/` unfinished rather than done.


---

## 4 · THE ROOT SWEEP

**The gate, and it was never once loosened:** every docs-shaped root candidate was
`grep -rIlF`-searched by basename across `scripts/`, `fixtures/`, `tests/` and `engine/`. **A
reference found = the file stays.** No reference was rewritten to make a move possible. The gate was
then **re-asserted inside the mover, immediately before each `git mv`**, so the decision was made
against the state at move time and not against a listing taken earlier (§6.2, class B).

Every move was `sha256` → `git mv` → `sha256`, same as the rotation. **24 moved, 0 mismatches, 0
sources left behind.** Root went from **89 files to 62**, and from **60 loose documents to 36**.

**These moves are NOT in `ROTATION_LOG.md`,** and that is deliberate: that log's own header scopes it
to *"build documents moved off the exchange bus"*. These came off the repo root, not the bus, and
none of them was ever in the box. Their record is the table below.

**MOVED — 24 documents, zero code references, gate re-asserted immediately before each `git mv`.**

| file | destination | referenced by scripts/ fixtures/ tests/ engine/ |
|---|---|---|
| `"ORCHESTRATOR CONTROL CENTER \342\200\224 protocol & state of record.txt"` | `"docs/history/reports/2026-08/ORCHESTRATOR CONTROL CENTER \342\200\224 protocol & state of record.txt"` | none — 0 hits, re-checked at move time |
| `AMENDMENT_2_BRIEF2_RESHAPE_1.md` | `docs/history/reports/2026-08/AMENDMENT_2_BRIEF2_RESHAPE_1.md` | none — 0 hits, re-checked at move time |
| `ARGUS_REPRIME_2026-08-02.md` | `docs/history/reports/2026-08/ARGUS_REPRIME_2026-08-02.md` | none — 0 hits, re-checked at move time |
| `CENSUS_1b_Rescore_and_Anatomy_Builder_Contract.md` | `docs/history/reports/2026-07/CENSUS_1b_Rescore_and_Anatomy_Builder_Contract.md` | none — 0 hits, re-checked at move time |
| `CENSUS_DEFINITIONS.md` | `docs/history/reports/2026-07/CENSUS_DEFINITIONS.md` | none — 0 hits, re-checked at move time |
| `HANDOFF_2026-07-22_Census_to_Census1b.md` | `docs/history/reports/2026-07/HANDOFF_2026-07-22_Census_to_Census1b.md` | none — 0 hits, re-checked at move time |
| `PARITY_CAPTURE_PLAN.md` | `docs/history/reports/2026-08/PARITY_CAPTURE_PLAN.md` | none — 0 hits, re-checked at move time |
| `PARITY_READINGS_GUIDE.md` | `docs/history/reports/2026-08/PARITY_READINGS_GUIDE.md` | none — 0 hits, re-checked at move time |
| `Prometheus_Data_Collection_Design.md` | `docs/history/reports/2026-07/Prometheus_Data_Collection_Design.md` | none — 0 hits, re-checked at move time |
| `Prometheus_Paper_Analysis_Week1.md` | `docs/history/reports/2026-07/Prometheus_Paper_Analysis_Week1.md` | none — 0 hits, re-checked at move time |
| `Prometheus_Stop_Loss_Logic_Learnings.md` | `docs/history/reports/2026-07/Prometheus_Stop_Loss_Logic_Learnings.md` | none — 0 hits, re-checked at move time |
| `REVIEWER_HANDOFF_2026-07-12.md` | `docs/history/reports/2026-07/REVIEWER_HANDOFF_2026-07-12.md` | none — 0 hits, re-checked at move time |
| `REVIEWER_HANDOFF_2026-07-13_V3_FORENSICS.md` | `docs/history/reports/2026-07/REVIEWER_HANDOFF_2026-07-13_V3_FORENSICS.md` | none — 0 hits, re-checked at move time |
| `REVIEWER_HANDOFF_2026-07-15_V3_RECOMPUTE.md` | `docs/history/reports/2026-07/REVIEWER_HANDOFF_2026-07-15_V3_RECOMPUTE.md` | none — 0 hits, re-checked at move time |
| `REVIEWER_HANDOFF_2026-07-25_ENGINE_INGESTION.md` | `docs/history/reports/2026-07/REVIEWER_HANDOFF_2026-07-25_ENGINE_INGESTION.md` | none — 0 hits, re-checked at move time |
| `S1_Findings_Report_3_Winners_Losers_MTF_Map.md` | `docs/history/reports/2026-07/S1_Findings_Report_3_Winners_Losers_MTF_Map.md` | none — 0 hits, re-checked at move time |
| `SCHED_TEST_RESULT_2026-08-02.md` | `docs/history/reports/2026-08/SCHED_TEST_RESULT_2026-08-02.md` | none — 0 hits, re-checked at move time |
| `SSv11_3_Execution_Playbook_and_Field_Manual.md` | `docs/history/reports/2026-07/SSv11_3_Execution_Playbook_and_Field_Manual.md` | none — 0 hits, re-checked at move time |
| `SSv11_Field_Manual.md` | `docs/history/reports/2026-07/SSv11_Field_Manual.md` | none — 0 hits, re-checked at move time |
| `SSv12_SPEC_ERRATA.md` | `docs/history/reports/2026-07/SSv12_SPEC_ERRATA.md` | none — 0 hits, re-checked at move time |
| `State_of_Project_2026-07-22_Census_Findings_and_Implications.md` | `docs/history/reports/2026-07/State_of_Project_2026-07-22_Census_Findings_and_Implications.md` | none — 0 hits, re-checked at move time |
| `TC1_Design_Brief_Lifecycle_AsIs_vs_Proposed.md` | `docs/history/reports/2026-07/TC1_Design_Brief_Lifecycle_AsIs_vs_Proposed.md` | none — 0 hits, re-checked at move time |
| `TC5_Amendment_1.md` | `docs/history/reports/2026-07/TC5_Amendment_1.md` | none — 0 hits, re-checked at move time |
| `V3_Forensics_Report_2_Deep_Dive.md` | `docs/history/reports/2026-07/V3_Forensics_Report_2_Deep_Dive.md` | none — 0 hits, re-checked at move time |

**STAYS AT ROOT — by rule (7).**

| file | bytes | why |
|---|--:|---|
| `.DS_Store` | 14,340 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `.gitattributes` | 1,797 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `.gitignore` | 12,259 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `LEDGER.md` | 259,298 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `pytest.ini` | 596 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `README.md` | 9,683 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |
| `requirements.txt` | 88 | kept at root BY RULE (ledger · readme · git config · build file · lockfile) |

**STAYS AT ROOT — docs-shaped but code references them (36). A reference found = it stays; not one reference was rewritten to make a move possible.**

| file | bytes | referenced by |
|---|--:|---|
| `CENSUS.md` | 8,653 | `fixtures/test_v12_census.py`, `scripts/backup_estate.py`, `scripts/census.py`, `scripts/census_analyze.py`, `scripts/census_build.py`, `scripts/reviewer_manifest.py`, `scripts/v12_packet.py` |
| `Census_1_Amendment_1.md` | 9,659 | `scripts/census_build.py` |
| `Census_1_MTF_Signal_Stack_Builder_Contract.md` | 17,804 | `scripts/census_build.py` |
| `CENSUS_1b.md` | 16,797 | `scripts/census1b_analyze.py`, `scripts/census1b_report.py` |
| `CHANGELOG.md` | 34,431 | `engine/version.py`, `scripts/packet.py`, `scripts/v12_packet.py` |
| `DATA_CENSUS.md` | 11,483 | `fixtures/test_v12_census.py`, `scripts/backup_estate.py`, `scripts/census.py`, `scripts/census_build.py`, `scripts/reviewer_manifest.py`, `scripts/v12_packet.py` |
| `GAP_REPORT.md` | 1,214 | `scripts/census.py`, `scripts/v12_packet.py` |
| `Naiad_Phase0_Charter.md` | 20,584 | `scripts/packet.py` |
| `Naiad_Phase1_Build_Prompt.md` | 14,497 | `scripts/packet.py` |
| `RC7_Amendment_1.md` | 8,857 | `scripts/rc7_recompute.py` |
| `RC7_Amendment_2.md` | 7,158 | `scripts/rc7_recompute.py` |
| `RC7_PostS1_Recompute_Builder_Contract.md` | 14,139 | `scripts/rc7_recompute.py` |
| `RC7_RESULTS.md` | 24,824 | `scripts/rc7_recompute.py`, `scripts/s3_analyze.py` |
| `RC_RECOMPUTE_RC0_RC6.md` | 29,101 | `scripts/rc_recompute.py` |
| `RC_Recompute_RC0_RC6_Builder_Contract.md` | 16,298 | `scripts/rc_recompute.py` |
| `S1_Instrumented_Replay_Builder_Contract.md` | 21,307 | `scripts/s1_fixtures.py`, `scripts/s1_runner.py` |
| `S1_MEASUREMENT.md` | 20,651 | `scripts/s1_fixtures.py` |
| `S2_Instrumented_Pass_Builder_Contract.md` | 19,134 | `scripts/s2_fixtures.py`, `scripts/s2_runner.py` |
| `S2_MEASUREMENT.md` | 8,003 | `scripts/s2_fixtures.py` |
| `S2B_DECOMPOSITION.md` | 10,002 | `scripts/s2b_decompose.py`, `scripts/s3_analyze.py` |
| `S2b_Decomposition_Addendum_Builder_Contract.md` | 9,236 | `scripts/s2b_decompose.py` |
| `S3_ENRICHMENT.md` | 9,697 | `scripts/s3_analyze.py`, `scripts/s3_enrich.py` |
| `S3_Enrichment_Builder_Contract.md` | 14,792 | `scripts/s3_enrich.py` |
| `SPOT_CHECK.md` | 7,296 | `scripts/spot_check.py`, `scripts/v12_packet.py` |
| `TC1_DEFINITIONS.md` | 3,492 | `scripts/tc1_fixtures.py` |
| `TC1_Factorial_Builder_Contract.md` | 10,479 | `scripts/tc1_fixtures.py` |
| `TC1_RESULTS.md` | 3,899 | `scripts/tc1_fixtures.py` |
| `TC4_BASELINE.md` | 7,045 | `scripts/s3_analyze.py`, `scripts/tc4_fixtures.py` |
| `TC4_Engine_1_0_8_Builder_Contract.md` | 15,314 | `scripts/tc4_fixtures.py`, `scripts/tc4_runner.py` |
| `TC5_Intraday_Respec_Builder_Contract.md` | 8,341 | `scripts/tc5_fixtures.py`, `scripts/tc5_runner.py` |
| `TC5_RESULTS.md` | 4,205 | `scripts/tc5_fixtures.py` |
| `V12_Study_Charter_Addendum_v1.0.md` | 11,892 | `scripts/tierc2_baseline.py`, `scripts/tierc3_rules.py`, `scripts/v12_packet.py` |
| `V12_V1_Census_Build_Prompt.md` | 14,040 | `scripts/v12_packet.py` |
| `V3_RECOMPUTE_R1_R10.md` | 34,072 | `scripts/rc_recompute.py`, `scripts/v3_recompute.py` |
| `V3_Recompute_R1_R10_Builder_Contract.md` | 20,745 | `scripts/v3_recompute.py` |
| `V3_STOP_AND_EXIT_FORENSICS.md` | 8,943 | `scripts/v3_recompute.py` |

**STAYS AT ROOT — not docs-shaped, so outside this sweep's remit (22). Residency for these is the data-residency and zip-residency rulings, not a root tidy.**

| file | bytes | kind | referenced by |
|---|--:|---|---|
| `census.json` | 62,741 | results JSON | `fixtures/test_v12_census.py`, `scripts/backup_estate.py`, `scripts/census.py` +2 |
| `census1b_results.json` | 68,351 | results JSON | `scripts/census1b_analyze.py`, `scripts/census1b_det.py`, `scripts/census1b_report.py` |
| `census1b_termini_enriched.jsonl` | 33,641,414 | substrate JSONL | `scripts/census1b_analyze.py`, `scripts/census1b_det.py`, `scripts/census1b_report.py` +2 |
| `census_results.json` | 21,468 | results JSON | `scripts/census_analyze.py` |
| `data_starts.csv` | 4,955 | data CSV | `engine/data.py`, `scripts/census.py`, `scripts/first_candles.py` +2 |
| `engine_1.0.2_noshrink_packet_20260711.zip` | 17,371 | packet zip | **none** |
| `engine_1_0_3_input_parity_packet_20260712.zip` | 15,815 | packet zip | **none** |
| `rc7_results.json` | 57,394 | results JSON | `scripts/rc7_recompute.py`, `scripts/s3_analyze.py` |
| `rc_recompute.json` | 83,980 | results JSON | `scripts/rc_recompute.py` |
| `recompute.json` | 57,735 | results JSON | `scripts/rc_recompute.py`, `scripts/v3_recompute.py` |
| `s1_results.json` | 50,186 | results JSON | `scripts/s1_fixtures.py`, `scripts/s3_analyze.py`, `scripts/v3_scorer.py` |
| `s2_results.json` | 12,481 | results JSON | `scripts/s2_fixtures.py`, `scripts/v3_scorer.py` |
| `s2b_results.json` | 14,351 | results JSON | `scripts/s2b_decompose.py` |
| `s3_excursion_substrate.jsonl` | 6,007,227 | substrate JSONL | `scripts/census_analyze.py`, `scripts/s3_analyze.py`, `scripts/s3_enrich.py` +1 |
| `s3_results.json` | 60,679 | results JSON | `scripts/s3_analyze.py`, `scripts/s3_enrich.py` |
| `SS_Cascade_v11_0_2.pine` | 56,785 | pine source | `engine/signals.py` |
| `ssv11_3_grade_legibility_packet_20260711.zip` | 48,242 | packet zip | **none** |
| `tc1_results.json` | 8,140 | results JSON | `scripts/s3_analyze.py`, `scripts/tc1_fixtures.py` |
| `tc4_baseline.json` | 12,785 | results JSON | `scripts/tc4_fixtures.py` |
| `tc5_results.json` | 7,597 | results JSON | `scripts/tc5_fixtures.py` |
| `v12_v1_census_packet_20260711.zip` | 17,634 | packet zip | **none** |
| `v12_v3_anchor_packet_20260713.zip` | 45,537,070 | packet zip | `scripts/v3_scorer.py` |

**No new root folder was created except `MAILBOX/`,** as instructed. The 25 existing root
directories were enumerated and left untouched: `.claude .git .github .pytest_cache _reviewer_box
analytics briefs claude configs docs engine exchange fixtures journal logs naiad-backups ops pine
prompts research research_outputs scripts skills study tests`.

---

## 5 · THE MAILBOX

### 5.1 What it is

`~/Naiad/MAILBOX` is a flat folder of **symlinks**. Every entry points at a file that already lives
somewhere in the repo. Opening a link opens the real file; deleting a link deletes only the link.
Nothing is copied, and **no target is ever written to**.

It is **gitignored**, asserted rather than assumed:

```
$ git check-ignore -v MAILBOX/.probe
.gitignore:259:MAILBOX/	MAILBOX/.probe
$ git status --porcelain --untracked-files=all -- MAILBOX
            (no output — MAILBOX is invisible to git)
```

So its **BOX COST is zero by construction**, not by restraint. Committing it would publish the same
bytes twice under a second set of paths and would break for any reader whose clone sits elsewhere.

### 5.2 The two sets, and what is measured rather than maintained

| set | contents | how it is derived |
|---|---|---|
| **PINNED** | `LEDGER.md` · `exchange/status/CONVENTIONS.md` | constant `ALWAYS_PINNED` |
| | every lane ledger (6) | **globbed** `exchange/status/LEDGER_*.md` — a seventh lane appears on its own |
| | every queue item not stamped `BUILT` (3) | **read through `reviewer_manifest.queue_items()`** — the same parser `MANIFEST.json` uses, so the mailbox cannot disagree with the manifest about what is open |
| | the operator's named working set (7 of 8) | constant `WORKING_SET`, entries are **globs**, so `QUEUE-008-BUILD` joins itself the day it is filed |
| **ROLLING** | newest `ROLLING_N = 25` by mtime | across `exchange/reports/**`, `exchange/queue/**`, `docs/history/reports/**`, and `research_outputs/*.html` |

`research_outputs/*.html` and **not** `**/*.html` is what *"top-level report renders only"* means in
code: 4 top-level renders are in scope, the 30 nested payload renders under
`research_outputs/<study>/` are not.

**The one pinned entry that is not on disk is reported, never skipped silently** (§3.3):

```
mailbox: 43 link(s) in MAILBOX/ -- 0 created, 0 pruned, 43 unchanged
mailbox: 1 pinned entr(ies) not on disk -- exchange/reports/*QUEUE-008-BUILD*.md
```

### 5.3 Where it is wired, and the named-constant care in both places

| site | when it runs | note |
|---|---|---|
| `publish_exchange.publish()` — a **`finally:` block on the function's tail** | after **every** publish outcome | `finally`, not a line before `return`, because `publish()` has seven return paths — PUBLISHED, NOTHING, FLAGGED, REFUSED, two ERROR paths and the branch guard — and the operator's view must be current after all of them, not after the happy one |
| `daily_routine.main()` — after the heartbeat, before the publish | every routine run | **not redundant**: it is the leg that covers a registry with `"publish": false`, where `publish()` never runs. On a normal day it does the work and `publish()`'s call is the no-op that demonstrates idempotence |

**Named-constant care, both sites (§6.4).** Both sites **call `refresh()`**. `ROLLING_N`, the
rolling scopes, `WORKING_SET`, `MAILBOX_DIRNAME` and `ABOUT_NAME` have **exactly one definition
each**, in `scripts/mailbox_refresh.py`, and **no value is copied out of it** at either call site —
grep for `ROLLING_N` outside that module returns the fixture only, which imports it rather than
restating it. The import in `publish_exchange` is **guarded**: if the module is unreachable the
publish still runs and *says* the mailbox did not refresh, because a silent skip is the defect §3.3
names.

### 5.4 FIXTURE F-MB-1 — full transcript

```
F-MB-1 -- MAILBOX rebuild, seven legs
  repo   : /Users/luis/Naiad
  mailbox: MAILBOX/   ROLLING_N = 25

  PASS     L0 no-destroy
           FAILS IF: the module contains rmtree/os.remove, or its single unlink() is not inside the is_symlink() branch
           observed: forbidden calls=none  single-guarded-unlink=True
  PASS     L1 rebuild
           FAILS IF: refresh() errors, or the mailbox ends up empty
           observed: error=None total=43 created=0 pruned=0 kept=43
  PASS     L2 resolve
           FAILS IF: any entry in MAILBOX/ is a symlink whose target is missing or is not a file
           observed: 43 link(s), 0 broken []
  PASS     L3 count
           FAILS IF: the count refresh() reports differs from the number of symlinks on disk
           observed: reported=43 on-disk=43
  PASS     L4 prune-dead
           FAILS IF: the planted dead link survives the rebuild, or is not named in `pruned`
           observed: planted=True pruned=True still_present=False
  PASS     L5 idempotent
           FAILS IF: an immediately repeated rebuild creates or prunes anything, or `kept` does not account for every link
           observed: created=0 pruned=0 kept=43 total=43
  PASS     L6 foreign-safe
           FAILS IF: a non-symlink file in MAILBOX/ is deleted or altered, or is not reported as `foreign`
           observed: survived=True reported_foreign=True
  PASS     L7 targets-untouched
           FAILS IF: any link target's mtime or sha256 changed across four rebuilds
           observed: 43 target(s) compared, 0 changed []

F-MB-1: 8/8 PASS
```

**What F-MB-1 pins that matters most.** **L0** reads the module's own source and asserts that the
single `.unlink()` call sits inside the `if entry.is_symlink():` branch and that no `rmtree` /
`os.remove` / `os.rmdir` appears anywhere — the mechanical version of "no scheduled lane deletes
anything" (§4.1). **L6** proves it behaviourally: a real file planted in `MAILBOX/` survives a
rebuild byte-for-byte and is reported as `foreign` rather than swallowed. **L5** proves the rebuild
is a no-op the second time, which is what makes it safe to run twice on every routine day. **L7**
compares the mtime **and** sha256 of all 43 targets across four consecutive rebuilds: **0 changed**.

### 5.5 What the mailbox holds today

**43 links — 18 pinned + 25 rolling.** Pinned: `LEDGER.md` and `CONVENTIONS.md` (2), six lane
ledgers, three open work orders (`003`, `008`, `BR-2`), and the seven present members of the named
working set. Rolling: `ROLLING_N = 25` across the four report surfaces. Beside the links sits one
managed plain-text file, `000_README.txt`, which explains the folder in six lines for whoever opens
it in Finder; it is not counted among the 43 and is exempt from pruning. The rolling window reaches
into `docs/history/reports/` as well as the live bus, **so a document does not vanish from view the
day it is rotated** — `BRIEF_ARGUS_PINE_SSV12T_2026-08-16.md` rotated this session and is in the
mailbox right now, at its new path.

---

## 6 · PROOF

| check | result |
|---|---|
| **F-CONV** | **4/4 PASS** — after the `CONVENTIONS.md` repoint, not before |
| F-CONV-1 | 9 `«NAIAD-S*»` tokens, all count == 2; repo-unique outside CONVENTIONS |
| F-CONV-2 | §0 = 5,334 B of the 6,000 B budget (88.9%), headroom 666 B |
| F-CONV-3 | 5 memory-pointer tokens, 5 resolve to a real section header |
| F-CONV-4 | census 422 → 422, **LOST 0** · 67,814 B of the 68,500 B ceiling (headroom 686 B) · 27 CASELAW cases all backlinked · all `CL-n` resolve both ways · **89 top-level rules, floor 89 (+0)** |
| **F-MB-1** | **8/8 PASS** — transcript in §5.4 |
| **suite** | **334 passed, 1 skipped, 0 failed**, 14.67 s |
| suite scope | `pytest.ini` → `testpaths = fixtures tests` — both trees, so `tests/test_analytics.py`'s F-AN-1..14 guard is collected |
| `rotate_reports.py --dry-run` | **HALT, exit 2** — pre-existing, not caused by this session. Finding **F-2**. |

The suite baseline of record was **282 passed / 4 failed / 2 skipped** at the Mac crossing
(`LEDGER_ATHENA`, 2026-08-15). It is now **334 / 0 / 1** — the four failures and the count difference
were closed by sessions between then and now, not by this one; this session's only claim is that it
did not move the number.

---

## 7 · THE BOX — before and after

**Two different questions, two different numbers, and they must not be confused.** *What did the
rotation do?* is measured with this session's own documents excluded — otherwise the instrument is
measuring itself. *Where does the box stand now?* includes them, because they are on the bus. Both
are given.

| measure | before (`4c6211d`) | after the rotation, before this session wrote | **as published** |
|---|--:|--:|--:|
| **TICK SET** — `exchange/` + `LEDGER.md`, *the figure that governs* | **3,851,115 B** | **2,430,358 B** | **2,547,543 B** |
| **as % of the 16,000,000 B box** | **24.07%** | **15.19%** | **15.92%** |
| `exchange/` only — continuity with prior reports | 3,591,817 B (22.45%) | 2,171,060 B (13.57%) | 2,288,245 B (14.30%) |
| tracked files under `exchange/` | 186 | 100 | 101 |
| budget level | OK | OK | **OK** |

**The rotation released 1,420,757 B — 8.88 points.** This session then wrote 117,185 B back onto the
bus, so the published state is **15.92%**, a net **−8.15 points**. The reconciliation, because a
figure that cannot be reconciled is a figure to be doubted:

| | bytes |
|---|--:|
| tick set after the rotation | 2,430,358 |
| + this build document | +82,423 |
| + `ROTATION_LOG.md` — 86 rows and the F-2 provenance block | +20,271 |
| + this session's `LEDGER_ATHENA.md` entry | +7,718 |
| + the two repointed citations (`CONVENTIONS` +62, `CADENCE` +62) | +124 |
| + **another session's edits riding this publish — F-8** (`INCIDENT_ORACLE` +49/−2, `LEDGER_ARGUS` +34) | +6,649 |
| **= as published** | **2,547,543** |

That last row is F-8 arriving as a number rather than a caveat: 6,649 B of this publish is not this
session's work.

**The bus is 33.9% smaller than it was this morning**, and it is at **40% of the warn threshold**
rather than 60%. Per-folder — the *after the rotation* column, so the folder deltas isolate the
rotation:

| folder | before | after |
|---|--:|--:|
| `reports/` | 2,696,162 B · 139 files | **1,359,434 B · 62 files** |
| `queue/` | 157,550 B · 13 files | **73,521 B · 4 files** |
| `status/` | 513,317 B · 16 files | 513,317 B · 16 files (KEEP-HOT by rule) |
| `status/daily/` | 213,307 B · 14 files | 213,307 B · 14 files |
| `(root)` | 10,920 B · 3 files | 10,920 B · 3 files |
| `drops/` | 561 B · 1 file | 561 B · 1 file |

**The §3.2 naming trip-wire (`FLAG_BYTES` = 64,000 B, ABSOLUTE), read against the tick set after the
rotation — 9 files, unchanged from 9 before:** `LEDGER.md` 259,298 · `LEDGER_APOLLO.md` 174,090 ·
`LEDGER_ATHENA.md` 118,571 · `BUILD_2026-08-12_CENSUS2B_VULT1.md` 105,838 ·
`BUILD_2026-08-14_CENSUS2B_PARTA_WTB1.md` 97,369 · `BUILD_2026-08-16_TIERC4_MEANCARD.md` 69,480 ·
`BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md` 68,524 · `CONVENTIONS.md` 67,752 (67,814 after
the repoint) · `008_sail-skeleton.md` 64,058. **The rotation moved 1.42 MB and did not clear a single
file off the wire** — every one of the nine is either append-only, a live rule surface, an open work
order, or a study report inside the 14-day window. Rotation is a **volume** instrument; the wire is a
**sensitivity**, and this session is a clean demonstration that the two are not the same lever.

Both constants were **read from `publish_exchange`, never copied**: `BOX_BYTES = 16,000,000`,
`FLAG_BYTES = 64,000`, `WARN_FRACTION = 0.40`, `REFUSE_FRACTION = 0.70`, `TICK_EXTRA = ('LEDGER.md',)`.
**Not one was edited** — threshold custody is ATHENA's (§4.2).

---

## 8 · FINDINGS — reported, not fixed

### F-1 · `exchange/.DS_Store` is TRACKED, and it is in the box  *[verified]*

```
$ git ls-files --error-unmatch exchange/.DS_Store
exchange/.DS_Store
```

**8,196 B of binary macOS Finder metadata**, committed, pushed to GitHub, and metered into the
project box on every publish — it is the largest of the three files in the bus's `(root)` folder
(10,920 B total: `DIGEST.md` 561 + `README.md` 2,163 + `.DS_Store` 8,196). `.gitignore:209` lists
`.DS_Store`, but ignore rules never reach an already-tracked file, which is why its sibling
`exchange/queue/.DS_Store` is correctly invisible and this one is not. It is also a **§4.2
text-only breach** — the bus is text, and this is a binary blob.

**Not fixed, and the reason is the brief's own first line.** The remedy is `git rm --cached
exchange/.DS_Store`, which removes a path from the index — a deletion, and this session was
instructed **NO DELETIONS**. It costs 0.05% of the box, so it is not urgent; it is one word from the
operator whenever he wants it gone.

### F-2 · The scheduled rotation has been INOPERABLE since 2026-08-15  *[verified]*

```
$ ~/venvs/naiad/bin/python scripts/rotate_reports.py --dry-run
rotate_reports -- HALT: the unacted-inbox exemption has no source.
  exchange/DIGEST.md contains no heading naming an inbox, so the queue-003 unacted-inbox
  exemption has no input. It is RETIRED (ruling 007): the file at that path is a tombstone.
  Rotation cannot tell an unacted note from a spent one until the operator rules where that
  list lives, and it will not guess -- six unacted notes are unprotected, the first becoming
  a candidate 2026-09-03.
  Nothing was classified. Nothing was moved. Exit 2.
```

**This is the most important thing in this report.** Queue 003's D-1 selects rotation candidates and
exempts *"any `NOTE_*_to_*` file listed as unacted inbox in the newest DIGEST"*. **Ruling 007 retired
the DIGEST on 2026-08-15**; the exemption's only input died with it. The script is behaving
correctly — refusing to guess is exactly right, and it says so loudly — but the consequence is that
**no automatic rotation can run at all**, and nobody noticed for seven days because nothing calls it
on a schedule. Today's named-set sweep did by hand what D-1 can no longer do.

`AGE_DAYS = 30` was **not widened, not flagged and not touched.**

**Reported, not fixed** — the repair is an amendment to a ratified contract, which ATHENA drafts and
the operator ratifies. **The recommendation, offered because it is cheap and it is already written:**
the brief's own *"newest NOTE per lane pair"* clause is a **list-free** replacement for the DIGEST
inbox exemption. It protects exactly the notes that are still live, it needs no maintained index,
and it cannot go stale, because it is computed from the filenames that are already there. It was
applied successfully to all 15 notes in this sweep.

### F-3 · Two ratified-unbuilt work orders left the bus without a stamp  *[verified]*

`001_condensed-project-history.md` (RATIFIED operator 2026-08-06, **never built** — the closeout of
2026-08-12 recorded *"no condensed-history artifact exists anywhere on disk"*) and
`004_move-clone-out-of-onedrive.md` (Phase A accepted, Phase B never run and mooted when the machine
was replaced) were both rotated on the operator's explicit naming. **Neither carries a `BUILT` stamp
or a `WITHDRAWN` one**, and writing one is not this lane's to write.

The measurable consequence is in §3.2: `queue_ratified_unbuilt` reads **3** from the next daily run,
down from 5, and **two of the two points lost are relocation, not completion**. The counter will not
say that. **The remedy is one line each** — a `WITHDRAWN:` or `BUILT:` stamp appended in place at
`docs/history/queue/`, which the operator or ATHENA can authorise in a sentence.

### F-4 · A ruling was made on a premise that failed seven minutes later  *[verified]*

`RULES_OF_RECORD_VIZ_IRON_2026-08-15.md` (mtime **22:40**) records operator ruling F-1: the VIZ-3
design contract *"was sought and is **ABSENT** for a third cycle — not attached, not in
`exchange/reports/`, nowhere in the tree"*, and on that basis promotes VIZ-4's inline restatement,
closes V-10, and strikes the re-attach item.

`exchange/reports/DESIGN_CONTRACT_VIZ3_TRADE_CATHEDRAL_2026-08-15.md` is on the bus, **mtime 22:47**
— seven minutes after the ruling that declared it absent, in the same batch of five files dropped in
at 22:47 that evening. Both documents are KEEP-HOT and both are published, so a reader currently
meets a ruling and its own refutation side by side.

Nothing was changed. The ruling is APOLLO's and the operator's, and the iron rules it promoted are
identical in substance either way — but the correction rule (§0) says a superseded assertion is
**rewritten**, not left standing beside the fact that overtakes it.

### F-5 · Two Finder artifacts the law does not reach  *[verified]*

- `DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15_1.md` is **byte-identical** to
  `DESIGN_CONTRACT_VIZ4_EMA_MANTLE_2026-08-15.md` — both sha256
  `8e8b3264805c9dee92d4bd9ad79ba62e56f1f404175d9a60d82ae9d1b1cdec7c`, 3,857 B each.
- `NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` carries a Finder `" copy"` suffix and a
  `.txt` extension — **and it is the only edition of that note**, which makes it the newest
  ATHENA→ALL-LANES broadcast and therefore KEEP-HOT by rule.

**Both were kept, deliberately.** Each is under 14 days old and neither is *superseded* — a
byte-identical twin is redundant, not a successor — so **the retention law as written reaches
neither**, and inventing a rule to catch them would have been this lane deciding retention policy on
its own authority. They cost 10,228 B, 0.06% of the box. One word rotates the twin; renaming the
`copy.txt` is a move too, but it would break the citation in `LEDGER_ATHENA`, so it wants a decision
rather than a tidy.

### F-6 · Where the law's parenthetical and the law's rule disagreed, the RULE was applied  *[verified]*

The brief reads: *"queue items not BUILT-and-spent (003, 008 + README)"*. Machine-read stamps say
five items were not stamped `BUILT`, not three:

```
001_condensed-project-history.md                      ratified=True  built=False
003_report-rotation-and-provenance.md                 ratified=True  built=False
004_move-clone-out-of-onedrive.md                     ratified=True  built=False
008_sail-skeleton.md                                  ratified=True  built=False
2026-08-16_BR2_oracle_calibration_parity_R2_ARGUS.md  ratified=True  built=False
```

001 and 004 the operator named for rotation by number, so they went (F-3). **`BR-2` was NOT named in
either list**, and it is ratified 2026-08-16 with `BUILT: PENDING` — a live, authorised, unstarted
work order. Rotating it would have taken an open commission off the bus and out of the manifest's
backlog count. **It was kept hot on the rule**, and the divergence from the parenthetical is
declared here rather than executed quietly.

The mirror case: **`BR-1` looked unratified** — its header says *"Status: AWAITING RATIFIED STAMP"* —
but it carries `BUILT: exchange/reports/BUILD_2026-08-16_ORACLE_REBIRTH.md · code commit a36edc1 ·
F-BR-1..F-BR-10 10/10 green` at line 81. Built means spent, so it rotated. **A header read alone
would have got both of these backwards.**

### F-7 · Queue items 005 and 006 do not exist — enumerated, not assumed  *[verified]*

The brief's ROTATE list names *"spent queue items 001/002/004/005/006"*. Invariant 6 says a negative
from one lookup measures the lookup, so the set was enumerated:

| where it could live | result |
|---|---|
| `exchange/queue/` | 12 work orders + README; no `005_*`, no `006_*` |
| `docs/history/queue/` | did not exist before this session |
| `git log --all --diff-filter=ADR -- 'exchange/queue/**'` | **every record is an `A`** — nothing was ever deleted or renamed out of that folder |
| `find . -name '00[5-7]_*'` | 0 hits |
| repo-wide `grep -iE "queue[ _-]?00[5-7]"` | 20 hits, **all for "queue 005"**, all referring to the **M0–M4 machine-migration milestones** (`.gitignore`, `.gitattributes`, `CADENCE.md`, `ROTATION_LOG.md`, three `M2/M3/M4` build reports, `LEDGER_ATHENA`, `routine_jobs.json`). Zero hits for 006 or 007. |

**"Queue 005" is a label on a milestone series that was never filed as a contract; "006" has no
referent in this repository at all.** ("Ruling 007", which does exist, is a *ruling* — HERMES
dormancy and the DIGEST retirement — not a queue item; that is the likely source of the confusion.)
Nothing was rotated for either, and nothing is missing.

### F-8 · Two files another session left modified ride this publish  *[verified]*

`publish()` stages `exchange/**` as it stands in the working tree, not merely what this session
touched. Two files were already modified when this session began — `INCIDENT_ORACLE_2026-08-20_CRASH.md`
(+49/−2) and `LEDGER_ARGUS.md` (+34), both from the oracle work of 2026-08-22 01:24. They are
exchange-scope coordination files that belong on the bus, so they were left alone and they publish
here. Named so the diff is not a surprise. The four modified `scripts/oracle_*.py` files and
`research_outputs/oracle/topup_scope.json` are **outside** `exchange/` and were **not** committed —
they remain uncommitted working-tree changes for whoever owns them.


---

## 9 · FILE DISPOSITION

`PROTECTED BY` reads *GitHub* for everything here: this session touched no data file, so no phase
archive or estate zip is involved. `PUSHED` is *yes* for both commits — `publish()` pushes the
branch, which carries the rotation commit `98951cd` ahead of it.

**BOX COST is `n/a` for every path outside `exchange/`** — `docs/history/**` and `scripts/**` are in
the repo and on GitHub but are **not** in the tick set (`exchange/` + `LEDGER.md`), so a byte moved
from `exchange/reports/` to `docs/history/reports/` leaves the box entirely. That is the whole
mechanism of this session. Constants read from `publish_exchange`: `BOX_BYTES = 16,000,000`,
`FLAG_BYTES = 64,000`.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/mailbox_refresh.py` | yes | tracked (new) | `98951cd` | yes — `origin/v12-v1-census` | GitHub | n/a — outside `exchange/` |
| `scripts/mailbox_fixtures.py` | yes | tracked (new) | `98951cd` | yes | GitHub | n/a — outside `exchange/` |
| `scripts/publish_exchange.py` | yes | tracked | `98951cd` | yes | GitHub | n/a — outside `exchange/` |
| `scripts/daily_routine.py` | yes | tracked | `98951cd` | yes | GitHub | n/a — outside `exchange/` |
| `.gitignore` | yes | tracked | `98951cd` | yes | GitHub | n/a — outside `exchange/` |
| **86 rotated bus documents** → `docs/history/reports/2026-08/` (72), `2026-07/` (5), `docs/history/queue/` (9) | yes, at the new paths | tracked, `R100` | `98951cd` | yes | GitHub | **−1,420,757 B released from the box** |
| **24 root documents** → `docs/history/reports/2026-07/` (18) and `2026-08/` (6) | yes, at the new paths | tracked, `R100` | `98951cd` | yes | GitHub | n/a — never were in the box |
| `exchange/status/ROTATION_LOG.md` | yes | tracked | this publish | yes | GitHub | 2,744 B → **23,015 B**, 0.144% of box — 86 new rows + the F-2 provenance block |
| `exchange/status/CONVENTIONS.md` | yes | tracked | this publish | yes | GitHub | 67,752 → **67,814 B**, 0.42% — **already over the 64,000 B wire, +62 B** |
| `exchange/status/CADENCE.md` | yes | tracked | this publish | yes | GitHub | 10,441 → **10,503 B**, 0.066% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | this publish | yes | GitHub | 118,571 B + this session's entry, 0.74% — **over the wire (append-only, no moment of creation at this size)** |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md` *(this document)* | yes | tracked (new) | this publish | yes | GitHub | see the FLAG below |
| `exchange/reports/INCIDENT_ORACLE_2026-08-20_CRASH.md` | yes | tracked | this publish | yes | GitHub | pre-existing edit, not this session's — F-8 |
| `exchange/status/LEDGER_ARGUS.md` | yes | tracked | this publish | yes | GitHub | pre-existing edit, not this session's — F-8 |
| `MAILBOX/` — 43 symlinks + `000_README.txt` | yes | **ignored** — `.gitignore:259` `MAILBOX/` | never | never | **NOT PROTECTED — and correctly so** | **0 B — links, not copies; it holds no content to cost anything** |

> ### ⚑ §3.2 TRIP-WIRE FLAG — raised at creation, by name, as the rule requires
>
> **`exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md` is over the
> 64,000 B naming trip-wire.** Its intended home is `exchange/reports/`, on the bus, where the web
> lanes can retrieve it. The exact size is printed by the publish and by the next daily run's
> bus-health block; a file never contains its own measurements of itself.
>
> **Why it earns the size, stated rather than assumed:** the brief asked for *"the full inventory
> table with verdicts"* — 187 rows, one per file on the bus, each with the rule that reached it. That
> table alone is roughly 28 KB and it is the only artifact from which the retention decision can be
> **audited** rather than trusted. Compressing it to a summary would make this document smaller and
> the decision unreviewable, which is the trade §3.1 explicitly refuses (*"full result tables, not
> summaries"*).
>
> **The consequence, named:** the count of box-bound files over the wire goes from **9 to 10**. The
> rotation released 1,420,757 B and this document costs back a fraction of one percent of that. If
> the operator would rather the inventory table lived off the bus, the clean cut is to move the §2
> table to `docs/history/reports/2026-08/` and leave a pointer — one instruction, and it can be done
> without touching anything else.

---

## 10 · WHAT REMAINS OPEN, WITH ITS OWNER

| # | item | owner | why it is not closed here |
|--:|---|---|---|
| 1 | **`rotate_reports.py` halts — no automatic rotation can run (F-2)** | **ATHENA drafts · operator ratifies** | Repairing D-1's exemption input amends a ratified contract. Recommended fix is in F-2 and costs one clause. **This is the one that decays**: six unacted notes are unprotected and the first becomes a candidate on **2026-09-03**. |
| 2 | `001` and `004` sit in history with no `BUILT`/`WITHDRAWN` stamp (F-3) | operator or ATHENA | One line each. Until then the backlog counter under-reports by two, silently. |
| 3 | `exchange/.DS_Store` is tracked, 8,196 B of binary in the box (F-1) | operator | The fix is a deletion from the index; this session was instructed NO DELETIONS. |
| 4 | Ruling F-1's premise (VIZ-3 "absent") is contradicted on the same bus (F-4) | APOLLO / operator | Not this lane's ruling to rewrite. |
| 5 | Byte-identical VIZ-4 twin and the ` copy.txt` note (F-5) | operator | The law as written reaches neither; a retention call is not the builder's to invent. |
| 6 | `QUEUE-008-BUILD` is pinned in the mailbox and not yet on disk | HEPHAESTUS, next session | Correct state — 008 is ratified and unbuilt. The link appears by itself the day it is filed. |

## 11 · THE HONEST NEXT OPTIONS

1. **Repair the rotation (recommended).** Ratify the "newest NOTE per lane pair" rule as D-1's
   exemption input in place of the retired DIGEST. It is already written, already applied to 15
   notes today, and it removes the last hand-maintained list from the rotation path. *For:* the
   sweep becomes automatic again before 2026-09-03. *Against:* it amends a ratified contract, so it
   costs an ATHENA draft and a stamp.
2. **Stamp 001 and 004, then leave them.** *For:* the manifest's backlog stops lying. *Against:*
   deciding whether 001 is withdrawn or merely deferred is a real decision, not a formality — the
   condensed project history was judged the best-drafted contract in the queue and was never built.
3. **Do nothing more this cycle.** *For:* the box is at 15.19%, 38% of the way to a warning, with no
   pressure for weeks. *Against:* item 1 has a date on it, and the thing that decays is the
   machinery that would have prevented the next cleanup being manual too.

---

## 12 · SESSION CLOSE

```
=== STATUS_HEPHAESTUS — 2026-08-22 ===
NOW: The exchange bus is rotated, the root is swept and MAILBOX is live and self-refreshing.
110 files moved, zero deleted, every move sha256-verified and R100 to git. The rotation took the
box from 24.07% to 15.19% of its 16 MB ceiling; this session's own documents put the PUBLISHED
figure at 15.92%, a net -8.15 points.
LAST EVENT: 2026-08-22 — commit 98951cd (rotation + root sweep + mailbox wiring), then one
publish carrying ROTATION_LOG's 86 new rows, two repointed status citations and this report.
FACTS:
- 86 bus documents + 24 root documents moved to docs/history/**; 0 sha mismatches [verified]
- tick set 3,851,115 B (24.07%) -> 2,430,358 B (15.19%) on the rotation, -> 2,547,543 B
  (15.92%) as published once this session's own 117,185 B went on the bus [verified]
- MAILBOX = 43 symlinks, 18 pinned + 25 rolling, gitignored, 0 B box cost [verified]
- F-MB-1 8/8 · F-CONV 4/4 · suite 334 passed / 1 skipped / 0 failed [verified]
- rotate_reports.py --dry-run HALTS exit 2 since ruling 007 retired the DIGEST — the scheduled
  sweep has been dead for seven days and nothing was watching it [verified]
- queue_ratified_unbuilt 5 -> 3, but two of the two points lost are relocation, not
  completion: 001 and 004 carry no BUILT and no WITHDRAWN stamp [verified]
PENDING:
1. Rule where D-1's unacted-inbox list now lives — recommended: the newest-NOTE-per-lane-pair
   rule from this brief. Decays 2026-09-03.
2. Stamp 001 and 004 WITHDRAWN or BUILT in docs/history/queue/.
3. Untrack exchange/.DS_Store (git rm --cached) — a deletion, so it needs the word.
4. Ruling F-1 vs the VIZ-3 contract that is on the bus (F-4) — APOLLO's to reconcile.
NEXT: build queue 008 (SAIL) — the only ratified, unbuilt, unblocked work order. Owner: HEPHAESTUS.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===
```

**Drag `~/Naiad/MAILBOX` into the Finder sidebar once.** From then on everything current is one
click away, and it refreshes itself on every publish and every daily routine.

---

> ### CORRECTION 2026-08-22 — the box figure, and a second publish disclosed
>
> **§7's "after" column first read `15.19%` under the heading *after this session's publish*.** That
> is the rotation-only figure, measured with this session's own documents excluded. It is the right
> number for *"what did the rotation do"* and the **wrong** number for *"where does the box stand"* —
> the first publish printed **15.92%**, and a reader would have carried 15.19% away as the published
> state. The table is **rewritten**, not annotated, per the correction rule (§0), and it now gives
> both bases side by side with a reconciliation that closes to the byte. The STATUS block and the
> §7 headline carried the same defect and are rewritten with it.
>
> **This cost a SECOND PUBLISH, and it is a named deviation from the brief's "ONE publish".** The
> precedent is M4, 2026-08-15, recorded in `LEDGER_ATHENA`: a known-false line in a filed report is
> a defect under §3.1's forensic-record duty, and the remedy is to rewrite and re-publish rather
> than to protect a process count. Publish 1 = `34ec888`. Publish 2 carries this correction.
>
> **How it was caught:** by reading the publish's own output against the document that had just been
> written, rather than assuming the prediction and the measurement agreed. They differed by 0.73
> points, and 6,649 B of the difference was not even this session's (F-8).
