# LEDGER_ATHENA — append-only lane ledger

**Lane:** ATHENA — system/ops: scheduling, backups, environment, exchange design, integrity ritual.
**Adopted:** 2026-08-02, ruling Q-3 A (`FUNNEL_DIONYSUS_W1`). Append-only. Never edit a past entry; a
correction is a NEW entry that names what it supersedes. The central `LEDGER.md` remains the
*evidence* ledger and is untouched by this file — this one carries coordination state only.

**Entry template (naiad-eod format):**

```
=== STATUS_<LANE> — <date> ===
NOW: <2-3 sentences>
LAST EVENT: <date> — <one line>
FACTS: <up to 6 lines, each ending with [verified/ledger/ratified/handoff/unconfirmed-live/open]>
PENDING: <numbered items waiting on the operator>
NEXT: <single next action + owner>
METRICS: operator actions this session = <n> · files re-ingested = <n>
=== END STATUS ===
```

---

=== STATUS_ATHENA — 2026-07-28 ===
NOW: Optimization track resumed. Three operator rulings taken: re-test Cowork before building any scheduler, a local Google Drive sync folder exists so offsite archiving can be automated, and the daily routine runs every day at 07:00. The routine is being built; its trigger is deferred pending the Cowork capability test.
LAST EVENT: 2026-07-28 — interview rulings taken; .venv rebuild + routine build paste issued.
FACTS:
- Cowork settings show "Run new tasks in the cloud" OFF and Cowork files rooted at the naiad folder; the earlier cloud-only test result reflected a chat, not a folder-attached task [verified]
- A virtualenv cannot be relocated (absolute paths hardcoded); rebuild-then-delete is the only safe path, and a scheduled task must call python by full path [verified]
- Routine is composable by design: scripts/routine_jobs.json is a job registry, so new jobs are added by config, not code [ratified]
- ENGINE handoff drafted covering six archived phases, census_run2 deduplication, the narrowed D5 basis and the two blocking CENSUS-1c rulings [handoff]
- STATUS blocks are written to a status file via paste rather than emitted in chat, per operator request [ratified]
- s3_excursion_substrate.jsonl stays git-tracked as a documented exception; removing it would rewrite every commit hash the ledger cites [ratified]
PENDING:
1. Cowork re-test (new task, naiad folder attached) — decides scheduler vs Cowork
2. Register the trigger once that answer lands
3. backup_estate.py build — needs Amendment 1 filed to the repo plus the Drive path
4. Q-1 / Q-2 CENSUS-1c rulings — still gate the ENGINE lane
5. Deliver the ENGINE handoff into that lane's context
NEXT: Operator runs the Cowork re-test; the ops lane holds the backup_estate paste pending its result.
METRICS: operator actions this session = not recorded (predates Q-8) · files re-ingested = not recorded
=== END STATUS ===

**Provenance note (HEPHAESTUS, 2026-08-02):** seed synthesized from `claude/STATUS_SYSTEM.md`
(1,849 B, dated 2026-07-28), ops content only. Items 1–3 of its PENDING list were resolved after that
date — the routine and `backup_estate.py` both shipped, and the triggers were armed on 2026-08-02
(see the next entry). Retained verbatim in substance for provenance; **superseded in part by the
2026-08-02 entry below.** [handoff]

---

=== STATUS_ATHENA — 2026-08-02 ===
NOW: 2026-08-02 — W1 (Dionysus funnel) rulings ingested; FUNNEL_ATHENA_W2 answered defaults; exchange v1 built this session.
LAST EVENT: 2026-08-02 — HEPHAESTUS built the exchange v1 skeleton, migrated the reviewer box into it, amended the manifest to v1.1, armed both Windows triggers, and opened queue item 001.
FACTS:
- Rulings folded: Q-1 C (sync bus + digest) · Q-2 A (auto-push `exchange/**` and lane ledgers only) · Q-3 A (per-lane append-only ledgers) · Q-4 A (hybrid Hermes, 2x/day; CRONOS = the schedule itself, gate W-3 resolved, no seventh agent) · Q-5 drafting rights APOLLO/ATHENA/ARGUS · Q-6 A (Apollo stays a chat; HELIOS tripwire on record) · Q-7 A (non-blocking answer debt) · Q-8 A (two integers per session-end STATUS) [ratified]
- The reviewer box is retired as a location: reports, daily outputs and MANIFEST.json now live under `exchange/`; `_reviewer_box/README.md` is left as a pointer [verified]
- Auto-publish is live and scope-limited: the routine and the backup both stage `exchange/**` only, and refuse to push if anything else is staged [verified]
- Both Windows triggers are armed: "Naiad daily routine" daily 07:00 and "Naiad weekly backup" Sundays 08:00 [verified]
- The F4 experiment (does a scheduled Cowork run see the local folder?) remains open; it tunes the Hermes scheduled/on-demand split but blocks nothing built here [open]
PENDING:
1. Configure GitHub sync in the Claude project (one-time), then click Sync now — this is what makes the bus live for the web lanes
2. Ratify or reject queue item 001 (condensed project history) — it carries `RATIFIED: PENDING`
3. Hermes' first pass: DIGEST.md is a placeholder until he runs
4. Second Google Drive account remains browser-only and is not machine-verifiable — manual check
NEXT: Operator configures project GitHub sync and clicks Sync now. Owner: operator.
METRICS: operator actions this session = 1 · files re-ingested = 0
=== END STATUS ===

---

=== STATUS_ATHENA — 2026-08-03 ===
NOW: Memory workstream closed. CONVENTIONS.md is live and verified readable on the sync bus;
project memory went 30 -> 23 entries with eight rules relocated, one corrected and a session-start
pointer added. Opening and closing snapshots are both committed. Only the acceptance probe remains.
LAST EVENT: 2026-08-03 — orphans filed, false ARMED claims corrected, workflow backup run.
FACTS:
- exchange/status/CONVENTIONS.md published dde8523 and returns WITH its repo path (S-4 PASS) [verified]
- Memory 30 -> 23: removed #7 #8 #9 #14 #16 #25 #28 #29; corrected #24; added the pointer [verified]
- Box reconciled by sha256: 26 files, 23 identical, 3 orphans — now filed to docs/knowledge and docs/primers [verified]
- The weekly --workflow trigger was NEVER ARMED despite three documents claiming it; both corrected [verified]
- Memory does not reach Cowork; the sync does not reach repo root; both now written into CONVENTIONS [verified]
- boxrescue/ disappearance was an operator action, not OneDrive dehydration — hypothesis withdrawn [operator]
PENDING:
1. Operator: run the acceptance probe (one fresh chat, registered prompt) and return the reply
2. Operator: move boxrescue/ outside the repo tree; remove the 26 box copies
3. Operator: T-6 data export, settles the memory-in-export dispute
NEXT: Grade the acceptance probe, then the phase-boundary audit (#1 #15 #19 + four merges -> 16).
Owner: ATHENA.
METRICS: operator actions this session = 6 · files re-ingested = 3
=== END STATUS ===

---

=== STATUS_ATHENA — 2026-08-04 ===
NOW: Memory workstream CLOSED. Panel at 23 entries, CONVENTIONS.md live and verified, three
snapshots exist and two are inside the 2026-08-04 workflow archive on Drive. Stale ARMED
assertions replaced (not annotated). Lane paused with a clean handoff.
LAST EVENT: 2026-08-04 — assertions rewritten, workflow trigger arming attempted, report closed.
FACTS:
- CONVENTIONS.md section 2.1b ROLLBACK rule live; section 0 trigger claim corrected to ONE [verified]
- CADENCE.md and CONVENTIONS.md section 8: stale ARMED assertions REPLACED, not annotated [verified]
- Acceptance probe INCONCLUSIVE — every content discriminator confounded by the synced snapshot [verified]
- Enforcement hook is one trigger, not three; #1 #15 #19 therefore stay in memory [verified]
- New standing rule: a correction replaces the assertion; a note beneath a stale claim is a second claim [ratified]
- Workflow backup trigger: see the schtasks verification block in this session's output [open]
PENDING:
1. Operator: relay the custodian skill's path so trigger 2 can be built
2. Operator: remove the 26 box copies; move boxrescue/ outside the repo tree
3. Operator: T-6 data export — settles the memory-in-export dispute
NEXT: Build trigger 2, then re-probe against the ROLLBACK canary. Owner: ATHENA.
METRICS: operator actions this session = 2 · files re-ingested = 1
=== END STATUS ===

---

=== STATUS_ATHENA — 2026-08-04 (b) — CORRECTION, supersedes the two preceding entries in part ===
NOW: The "weekly --workflow trigger is NOT ARMED" finding was FALSE and is withdrawn. The task has
been registered and Ready since 2026-08-02, first fire 2026-08-09, never yet run. The two entries
above cite it; those citations are void. Everything else in them stands.
LAST EVENT: 2026-08-04 — assertions restored across CADENCE.md, CONVENTIONS.md, the session report
and project memory entry #19.
FACTS:
- "Naiad weekly workflow backup" ARMED since 2026-08-02, Ready, next 2026-08-09 08:30, never fired [verified by enumeration]
- Cause of the false finding: one task queried by name, the other's absence inferred, not measured [verified]
- Two rounds of document corrections were built on it; all reversed this session [verified]
- STILL TRUE: newest workflow archive was 2026-08-02 and predated the 08-03/08-04 files — the hand run was correct [verified]
- CONVENTIONS §0's one-trigger correction is about ENFORCEMENT triggers, unrelated, and stands [verified]
- §2.1b ROLLBACK rule and the corrections rule stand; the latter now cites a live instance [ratified]
PENDING:
1. Operator: relay the custodian skill's path so enforcement trigger 2 can be built
2. Operator: remove the 26 box copies; move boxrescue/ outside the repo tree
3. Operator: T-6 data export — settles the memory-in-export dispute
NEXT: Build enforcement trigger 2, then re-probe against the ROLLBACK canary. Owner: ATHENA.
METRICS: operator actions this session = 2 · files re-ingested = 1
=== END STATUS ===

---

=== STATUS_ATHENA — 2026-08-04 (close) ===
NOW: Lane closing on a clean handoff (ruling G1-a). Backup architecture is verified end to end for
the first time: all 9 phase archives hash-MATCH between laptop and Drive, and 7 of the 9 now carry
a fingerprint in two independent places. Workflow redesign is built, published and in use. Code work
is filed as ratified queue item 002 rather than crammed into a closing paste.
LAST EVENT: 2026-08-04 — six sidecars written and mirrored; queue 002 D4 reduced to a fixture.
FACTS:
- 9/9 phase archives hash-verified laptop vs Drive, 1,043,691,544 B, zero mismatches [verified]
- All 9 have a Drive sidecar; 7 of 9 also have a git-TRACKED local one, pushed as ccbfd2d
  (.gitignore:38 covers *.zip only, so sidecars travel to GitHub). The two analytics archives have
  a Drive sidecar but NO local/tracked one — their fingerprints are not on GitHub [verified]
- Legacy "naiad (local folder) BACKUP" deleted; contents preserved and verified in phases/ [verified]
- exchange/ 51.4% -> 22.8% of the project box; documents are only 15% [verified]
- Project memory 30 -> 24 entries; CONVENTIONS.md carries every relocated rule in full [verified]
- Queue 002 D4 found ALREADY IMPLEMENTED by the builder before code was written [handoff]
PENDING:
1. Operator: add the trigger-2 line to the naiad-custodian skill (Settings > Skills), then run the
   ROLLBACK-canary probe in one fresh chat; that unblocks the memory audit to 17 entries
2. ARGUS (8 files) and APOLLO (1) to rule on the orphan memo in exchange/reports/
3. HEPHAESTUS to execute queue 002 in its own session with its own build document
4. Operator: ~18.7 MB of redundant copies in naiad-backups/ (three "(1)" files plus top-level
   duplicates of phases/ content) — cosmetic, apply the §3.2 existence-is-not-protection rule first
5. Two local sidecars still missing: analytics_v1.0.0_2026-07-29.zip.sha256 and
   analytics_tests_v1.0.0_2026-07-29.zip.sha256. Both archives have a Drive sidecar, so they are
   verifiable ON Drive, but no fingerprint for either reaches GitHub. This session was authorised
   for exactly six sidecars, so the gap was reported rather than closed. One paste finishes it
NEXT: Hold for the probe, then execute the memory audit (3 moves + 4 merges -> 17). Owner: ATHENA.
METRICS: operator actions this session = 9 · files re-ingested = 4
=== END STATUS ===

---

=== STATUS_ATHENA — 2026-08-05 — PENDING 5 CLOSED ===
NOW: Fingerprint coverage complete. All 9 phase archives now carry a sha256 in two independent
places: a git-tracked local sidecar on GitHub, and a sidecar beside the archive on Drive. PENDING
item 5 of the closing entry is closed; nothing else in that entry changes.
LAST EVENT: 2026-08-05 — the two analytics sidecars written, verified, and confirmed to agree with
the Drive sidecars already present.
FACTS:
- 9/9 archives have a local git-tracked sidecar; 9/9 have a Drive sidecar [verified]
- Each new local hash was checked against the existing Drive sidecar and agreed [verified]
- No archive and no Drive file was created, modified, moved or deleted this session [verified]
- The builder declined to write these two in the prior session because its authorisation named
  exactly six files; the gap was reported rather than silently exceeded [handoff]
PENDING:
1. Operator: run the ROLLBACK-canary probe now that the naiad-custodian skill names CONVENTIONS.md
2. ARGUS (8 files) and APOLLO (1) to rule on the orphan memo
3. HEPHAESTUS to execute queue 002 in its own session
4. Operator: ~18.7 MB of redundant copies in naiad-backups/ — cosmetic
NEXT: Grade the probe, then execute the memory audit (3 moves + 4 merges -> 17). Owner: ATHENA.
METRICS: operator actions this session = 2 · files re-ingested = 1
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-11 ===
NOW: ARGUS maintenance cycle commissioned by NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY closed in one session: F-AN-15 interface byte-identity fixture built and demonstrated failing before being trusted, LEDGER_ARGUS acknowledgement appended, build document filed. Addendum folded into the same document and the same publish: the daily-routine outage was re-diagnosed from artifacts, and Ruling 'append' was installed in CONVENTIONS 3.1. This entry is that ruling's first application — the rule's own installer honours it.
LAST EVENT: 2026-08-11 — CONVENTIONS 3.1 gained Ruling 'append'; this STATUS entry is the byproduct it mandates.
FACTS:
- F-AN-15 added to tests/test_analytics.py: newest exchange/reports/INTERFACE_*.md must be byte-identical to analytics/INTERFACE.md. Both copies currently sha256 70c3f368…f6f93c61e, 48,885 B — no drift [verified]
- F-AN-15 watched to FAIL on a one-byte mutation at offset 20,000 with file length unchanged, and to SKIP (not pass) with the published copy absent; restore sha-verified. Suite 286 -> 287 passed, 1 skipped [verified]
- Daily routine did NOT fail four times: 08-09 TRIGGERED-AND-FAILED (HALT F-M3/F-M4, no manifest written), 08-10 NEVER-TRIGGERED (no artifacts; machine away), 08-11 TRIGGERED-THEN-KILLED at 16:36:33 with 0xC000013A STATUS_CONTROL_C_EXIT after MANIFEST_2026-08-11.json was written, 08-12 NOT YET DUE locally [verified]
- The F-M3/F-M4 repair is EVIDENCED WORKING: 08-09 wrote no manifest, 08-11 wrote 24,164 B. The 08-11 run died from session termination, not from a fixture [verified]
- StartWhenAvailable is ALREADY true on all three Naiad tasks; there is no HERMES task at all; TaskScheduler/Operational log is DISABLED, which is why this needed artifact forensics [verified]
- Both weekly backups last returned result 1 on 2026-08-09 and have not run since; next due 2026-08-16. Flagged, NOT diagnosed — outside cycle scope [open]
PENDING:
1. Operator: the CONVENTIONS 4.2 manifest exception arrived truncated mid-sentence; 4.2 is UNMODIFIED pending the remaining text
2. ATHENA: rule on the rotation conflict — INTERFACE_2026-08-06_C6.md leaves APOLLO's reading surface 2026-09-05; ARGUS proposes exchange/status/
3. ATHENA: diagnose the two failing weekly backups before 2026-08-16
4. Operator: WakeToRun (currently false) and InteractiveToken fragility — each implication stated in the build document, no setting changed
5. Operator: enable the TaskScheduler Operational log so the next outage is answerable from the log
NEXT: Rule on the rotation conflict and supply the truncated 4.2 text. Owner: ATHENA, then operator.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Close-out session executed under operator go 2026-08-12. Seven of nine items delivered in full, one delivered only after correcting a placement bug in the instruction that issued it, one HALT-SOFT needing an elevated shell. The daily routine is GREEN again — first clean end-to-end run since 2026-08-08, all four jobs exit 0, HEARTBEAT regenerated with exit: 0. The three-day "dead automation" reading is closed: one real failure, one away-day, one killed run.
LAST EVENT: 2026-08-12 — routine ran clean (4479606); F-P6 freshness line live in production; queue counters truthful for the first time.
FACTS:
- F-P6 built into publish_exchange.py: every publish now prints when the ROUTINE last completed, read from HEARTBEAT.md, never written by publish. Print-only, never blocks. 5/5 asserted cases including the 36h boundary and four MISSING modes [verified]
- F-P6 proved itself in PRODUCTION in both states on the day it was written: "routine last completed 2026-08-09 (56h ago) *** STALE >36h ***" on the backup publish, then "2026-08-12 (0h ago)" after the routine ran clean [verified]
- F-Q1: queue_open reported 0 against six work orders for two independent reasons — the NNN_*.md filter excluded the three date-named contracts, and a bare `RATIFIED:` startswith test could not see SEQ8's `**RATIFIED:**`. Both fixed; counters now 6 total / 0 unratified / 2 ratified-unbuilt, machine matching hand enumeration on all six rows [verified]
- BUILT: stamp convention added as queue/README.md rule 6 — "ratified but unbuilt" had no source of truth in the files. Four items stamped from artifacts verified on disk; 001 and 003 deliberately left unstamped and are now the visible backlog. SCOPE JUDGMENT, operator may veto [ledger]
- MC1_results.json and WF1_discriminants.json left the bus for pointer stubs after double sha256 verification: 374,427 B freed, 5.86% of the box. NEITHER safety copy is pushed — research_outputs/mc1/** is gitignored — so git history at 2604d5e is the durable protection, not the copies [verified]
- INTERFACE relocated to exchange/status/INTERFACE_PUBLISHED.md per the rotation ruling; git recorded a rename, sha unchanged 70c3f368…, F-AN-15 follows it, suite 287 passed / 1 skipped unchanged [verified]
- Weekly backups: destination healthy throughout — G: writable, Drive running, 08-09 archives intact. Both exit 0 today, 8/8 fixtures each, bidirectional verification 73/73 and 321 members. ROOT MECHANISM: backup_estate.py returns 1 when publish_step() is FLAGGED/REFUSED/ERROR, so a perfect verified archive reports failure for a git-step stumble. Size budget was 19.3% that day and all three publishes committed; concurrent index contention is the leading hypothesis, NOT proven [verified/open]
PENDING:
1. Operator: enable the scheduler log in an ADMIN shell — `wevtutil sl Microsoft-Windows-TaskScheduler/Operational /e:true` (exit 5, access denied from this session). Until then every scheduler question needs artifact archaeology
2. ATHENA: backup_estate.py exit-code conflation (§7.3 of the build document) — out of this session's scope, reported not fixed
3. ATHENA: F-P6 and F-Q1 are scratchpad harnesses, NOT in pytest — one line of scope for fixtures/ makes them permanent
4. ATHENA: decide whether research_outputs/wf1/ (and mc1/, needing a .gitignore edit) should be tracked
5. HEPHAESTUS: queue 001 and 003 are ratified_unbuilt; 003 is half-built — rotate_reports.py exists, ROTATION_LOG.md and docs/history/reports/ do not
6. Operator: WakeToRun is false and the task runs as InteractiveToken, so an away-day waits for wake and a logoff kills a running routine — both implications stated, no setting changed
NEXT: Enable the Operational log, then rule on items 2-4. Owner: operator, then ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: HEPHAESTUS ran a READ-ONLY safety audit after an accidental OneDrive "Free up space" on the repo tree with the quota showing full. Nothing was written by the audit and no dehydrated file was opened — attributes only, because opening a placeholder downloads it. 164 of 839 files are now cloud-only placeholders holding 299.4 MB, but almost all of it is protected: the true exposure is 287.2 MB across 52 untracked files, and 98.7% of that is SIX files. No rehydration, pinning or OneDrive action was taken; that decision is now the operator's, informed by these numbers.
LAST EVENT: 2026-08-12 — OneDrive "Free up space" dehydrated 164 repo files; audit filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md.
FACTS:
- Local HEAD == origin/v12-v1-census at 7552d652eb…508a00924, tree clean but for .gitignore, so all 112 dehydrated TRACKED files (12.2 MB) are recoverable from GitHub whatever OneDrive does [verified]
- seq8 was NOT touched: 1783.5 MB / 15 files, ZERO dehydrated, and D:/naiad/research_outputs/seq8 matches it file-for-file at identical total size. mc1 also untouched, 155.3 MB / 30 files, zero dehydrated. D:/naiad is not a OneDrive path and is 100% intact, 44 files / 4.46 GB [verified]
- F-OD-1 THE EXPOSURE: 52 files, 287.2 MB, are dehydrated AND untracked AND absent from the D: mirror — OneDrive cloud is their only copy. 283.6 MB of it is six files: census_outcomes.jsonl 110.92, v12_v3_anchor_packet_20260713.zip 43.43, census_ladder.jsonl 43.23, census_termini.jsonl 35.94, census1b_termini_enriched.jsonl 32.08, continuation.jsonl 17.97. The other 46 files are 3.6 MB of _reviewer_box mirrors and .pytest_cache [verified]
- F-OD-3: class B is ZERO — nothing dehydrated has a D: mirror copy. The mirror only ever covered seq8 and _archive, so "Free up space" did not create the single-copy gap, it exposed one that always existed [verified]
- F-OD-2: that the cloud actually holds those bytes is REASONED, not confirmed — OneDrive only dehydrates a file whose upload completed, so a placeholder implies a full quota did not strand it, but the only direct proof is to open a file, which downloads it, which the instruction forbade [unconfirmed-live]
- Governance surface and ALL uncommitted work survived on disk: LEDGER.md, CONVENTIONS.md, LEDGER_ATHENA.md, both Cascade Atlas HTMLs, HANDOFF_ATHENA, PRIMER_HERMES, the panel parquet, scripts/mc1_program.py, mc1_report.py and research_outputs/wf1/ are all hydrated. C: 35.6 GB free, D: 3721.2 GB free [verified]
PENDING:
1. Operator: rule on rescuing the six class-C files (283.6 MB) to D:/naiad — recommended FIRST because copying forces the download and so doubles as the test of F-OD-2. Costs <1% of C: headroom
2. Operator/ATHENA: "always keep on this device" on research_outputs/ is the tempting fix and is the WRONG one while the quota is full — it increases the pressure that caused this. Flagged against, not applied
3. ATHENA: whether the census substrates should be tracked is the same open decision already carried for research_outputs/wf1/ and mc1/ — one directory wider, and 208 MB of .jsonl would need LFS
4. ATHENA: moving research_outputs/ out of the OneDrive tree is the clean long-term fix with the largest blast radius — script paths, backup estate and mirror logic all need review before it is attempted
5. Operator: .pytest_cache/ sits inside the sync selection and is spending OneDrive quota on transient build artifacts
NEXT: Rule on item 1; the rescue is the only option that removes risk rather than relocating it. Owner: operator, then HEPHAESTUS to execute.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: The backup destination is repointed in code. Repo integrity is green where it now sits — fsck clean, 544/544 tracked files present, zero dehydrated — and all 20 archives on D:/naiad-backups verify against their sidecars with zero mismatches. --estate/--workflow now default to D:/naiad-backups and HALT if the drive is absent; explicit --dest still wins, which is why the two Sunday tasks still target G: and need an operator decision.
LAST EVENT: 2026-08-12 — live --workflow run wrote naiad_workflow_2026-08-12.zip to the new default, 324 members, 8/8 fixtures, 0 mismatches; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_BACKUP-PATH-REROUTE.md; published 44a2abc, code committed 0509912.
FACTS:
- Sync idle: repo and D:/naiad-backups byte-identical across a 60s double measurement; git fsck clean; HEAD == origin/v12-v1-census at 7552d652eb… [verified]
- 20/20 archives on D: verified against their sidecars, 0 mismatched; 3 unverifiable (1)-suffixed duplicates carry no sidecar and were left untouched [verified]
- G:/My Drive/naiad-backups is EMPTY, 0 files — the move was a move, not a copy. It was read-only this session and is exactly as found [verified]
- D:\naiad-backups IS a registered Google Drive mirror target, decoded from the DriveFS SyncTargets registry protobuf; D: is a physical LaCie exFAT disk, not a Drive mount — the two facts are compatible and both were measured [verified]
- Its uploads are ERRORING: 50 CreateHardLinkW failures naming these archives, no completion record in Drive's logs; exFAT has no hard links. Registered is not uploaded [verified]
- No provable copy of the four estate generations (1.85 GB) exists outside D:; the second-account upload is stale at 2026-08-05, predating both the 08-09 and 08-11 generations [verified]
PENDING:
1. Operator: check drive.google.com > Computers for naiad-backups — thirty seconds, and it settles whether the off-site copy exists (O-1)
2. Operator: rule on the two Sunday tasks, which still pass --dest "G:\My Drive\naiad-backups" explicitly; next fire 2026-08-16 08:00/08:30. Decision funnel in §8 of the build document (O-2)
3. ATHENA: both weekly backup tasks returned exit 1 on 2026-08-09 while writing valid archives — unexamined, reported not fixed (O-3)
4. ATHENA: retention_report() reports "PHASE ARCHIVES — none found" while nine exist at D:/Naiad/research_outputs/_archive; pre-existing, reported not fixed (O-4)
5. Operator: D:\Naid-GDRIVE is a second 4.2 GB Drive-mirrored copy of the tree — deliberate or stray? (O-7)
NEXT: Check Computers in the Drive web UI, then rule on item 2. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Seven previously untracked files are committed and pushed as 5e8d7ba. Two of the ten turned out to be byte-identical duplicates of content already on origin and were left in place; one, research_outputs/wf1/WF1_discriminants.json, was left for ATHENA because its tracking status is an open lane decision — and it is now the last genuinely unprotected file in the repository.
LAST EVENT: 2026-08-12 — untracked root artifacts filed; commit 5e8d7ba pushed to origin/v12-v1-census; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md.
FACTS:
- 7 files filed: 4 moved (copy -> sha256 verify -> remove original, 0 mismatches), 3 staged in place; all 7 confirmed present on origin/v12-v1-census [verified]
- Destinations chosen on MEASURED archive coverage, not on file extension: docs/history, docs/primers, scripts and exchange/reports are WORKFLOW_SOURCES; docs/reports, docs/handoffs, briefs and research_outputs are NOT [verified]
- Cascade Rewire.html (blob 37502615) and SS_Reassessment_Synthesis_2026-08-03.md (blob 0ad38893) are byte-identical to tracked+pushed twins; all three CONVENTIONS §3.2 checks passed on both. The contract's "exist in NO other copy" premise was false for these two [verified]
- research_outputs/wf1/ is a DIRECTORY entry; git collapses a wholly-untracked directory to one porcelain line, and an isfile() filter drops it silently. Enumerated with --untracked-files=all instead [verified]
- briefs/panel/excursions/2026-08-03.parquet was the one missing file in an otherwise fully tracked panel partition set — its 08-05 sibling was already tracked [verified]
- Box cost of the whole operation: 0 B — nothing new entered exchange/ [verified]
PENDING:
1. ATHENA: rule on research_outputs/wf1/ — 110.7 KB, zero box cost, no precedent problem, and the last unprotected content on the machine (O-1)
2. Operator: two byte-identical duplicate files sit at the repo root; removing them loses nothing but is a deletion and none was authorized (O-2)
3. ATHENA: briefs/, docs/reports/ and docs/handoffs/ hold tracked content but are absent from WORKFLOW_SOURCES — GitHub-only protection (O-3)
NEXT: Rule on item 1; it is the only remaining file with no copy anywhere. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: O-1, O-3 and O-4 are closed and the operator's tidy is done. WF1_discriminants.json is tracked and pushed, so the repository has no unprotected file left. WORKFLOW_SOURCES now covers briefs, docs/reports and docs/handoffs — proved live at 343 members, 0 mismatches. The retention report finds the nine phase archives it had been reporting as absent, and can no longer confuse an unmounted drive with an empty one.
LAST EVENT: 2026-08-12 — code commit 91ce815 pushed; proof run wrote naiad_workflow_2026-08-12-01.zip (343 members, 8/8 fixtures); filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md.
FACTS:
- O-1: research_outputs/wf1/WF1_discriminants.json verified NOT gitignored, tracked in 91ce815, confirmed present on origin/v12-v1-census. research_outputs/mc1/ deliberately NOT added, per the ruling that bulk data stays pointered [verified]
- O-3: WORKFLOW_SOURCES 11 -> 14 entries; the old list asserted a STRICT SUBSET of the new, no duplicates, no nested roots. Measured 4.21 MB (briefs 3.92, docs/reports 0.26, docs/handoffs 0.02) against a 50 MB ceiling BEFORE widening [verified]
- O-3 proved live: 343 members vs 324, +829,163 B (+30.2%), 0 mismatches/strays/omissions, 8/8 fixtures; 16 of the 22 added members come from the three newly covered roots, and the 3 removed are the files that left the repo root today [verified]
- O-4: retention_report() now resolves the --phase root through a shared phase_archive_root_path() and prints 9 archives / 1,043.6 MB where it printed "none found" this morning. It had been scanning REPO/research_outputs/_archive, which stopped holding archives when ruling B moved them off-machine on 2026-08-06 [verified]
- O-4 third state: an unmounted drive prints "NOT ENUMERABLE" and falls back to the 9 tracked sidecars; fixture F-O4 asserts that state never emits a "none found" verdict — the conflation behind the 2026-08-04 retraction [verified]
- TIDY: both repo-root duplicates removed only after four checks each passed IN THIS RUN (sha256 equal to twin, twin tracked, twin's blob on origin, twin's worktree bytes == that blob). Both twins re-verified intact afterwards. Neither file was tracked, so neither deletion is a git change [verified]
PENDING:
1. ATHENA: the keep-4 rule counts a same-day -NN archive as a full generation, so today occupies two slots and naiad_workflow_2026-08-04.zip now reads as outside the rule. Report-only, nothing deleted — accept it, or group -NN siblings under their base date (O-5, created this session)
2. Operator: the two Sunday tasks still pass --dest "G:\My Drive\naiad-backups"; next fire 2026-08-16 08:00/08:30 (O-6, carried)
3. Operator: confirm or refute the Google Drive mirror of D:/naiad-backups at drive.google.com > Computers — registered but its uploads log CreateHardLinkW failures on exFAT (O-7, carried)
4. ATHENA: research_outputs/ remains outside WORKFLOW_SOURCES, so WF1_discriminants.json has GitHub-only protection. Widening it would pull in the multi-GB study estate and is a separate decision, not an oversight (O-8)
NEXT: Rule on O-5; it is the only item this session created. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Queue 004 cannot be ratified because it does not exist in this repository. The operator's "ratify 004" is recorded as received and unexecuted — blocked on the contract text being filed, not refused. The amendment paste was checked against the code anyway, and its motivating premise does not survive the check.
LAST EVENT: 2026-08-12 — HEPHAESTUS halted on the paste's own gate (004 missing); no byte written to exchange/queue/; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-HALT.md.
FACTS:
- exchange/queue/004_move-clone-out-of-onedrive.md does not exist: absent from disk, untracked, and never committed on ANY branch (git log --all). Six independent checks incl. Downloads/Desktop for a _1-suffix twin; all negative. The queue runs 001-003 and stops [verified]
- The paste's stamp anchor is character-for-character the 003 stamp of 2026-08-11 with the date advanced, so 004 was drafted in a session whose output never reached this repo — same class as the 2026-08-12 "file it" ruling [verified]
- PREMISE REFUTED: the 2026-08-09 weekly backups did NOT fail on a sleeping LaCie. Both archives exist and re-verify, RETENTION.md shows no date gap; the tasks started 15:51:58 (StartWhenAvailable catch-up), never at 08:00; and the destination that day was G:\My Drive, not D: — D: became the target on 2026-08-12. Exit 1 came from backup_estate.py conflating archive success with the git publish step (CLOSEOUT 7.3) [verified]
- D-0b scope understated: 20 D: resolution/gate sites across 4 files, minimum correct wiring set is 9 points, not 3. backup_estate.py:980 (_generations) is UNGATED and still prints "none found" for an unmounted drive — O-4 fixed the phase half and left the estate/workflow half standing. daily_routine.py carries its own D: literal and gate, and is the job that runs unattended daily [verified]
- D-0b claim (b) gates on the WRONG DRIVE: both Sunday tasks pass --dest "G:\..." explicitly and backup_dest_root() honours --dest first, so a wait_for_drive wired there waits for Google Drive (open item O-6) [verified]
- D-0d targets the wrong document: CONVENTIONS section 2 is "How to build a paste for HEPHAESTUS" and contains no D: gate; literal D: appears only at lines 784/788/795 in section 8. The gate rule lives in NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md:19 and LEDGER_ARGUS.md:52 [verified]
- O-5 CONFIRMED and worse than described: _generations() has no day key at all (sorts on full filename, raw slice). NEW defect — the same-day sort is INVERTED ("." 0x2E > "-" 0x2D), so the newer -01 archive ranks as the older generation and is labelled prunable first. " (N)" OneDrive duplicates hit the same bug [verified]
- 287/1 is correct and current (287 passed, 1 skipped, plain pytest) [verified]
- C:/Naiad is unclaimed — zero repo references, absent from disk — so no collision, but the stated justification fails: the residency rule is repo-RELATIVE and the two trees are already parallel today. 23 breakages enumerated, 3 silent and outside the repo (3 Task Scheduler Start In values, the .claude/projects harness dir holding auto-memory, ~25 permission rules). Three HARD identity gates assert the path contains "OneDrive" — C:/Naiad fails both conjuncts, so every builder session would halt at pre-flight until they are amended in the same change [verified]
PENDING:
1. ATHENA: file the 004 contract text into exchange/queue/ — nothing can be stamped until it lands; the operator's ratification is held open against it
2. ATHENA: rule on the seven objections in section 6 of the report, then re-issue the amendment against the filed file — chiefly the refuted premise, D-0b's 9-point scope, and D-0d's target
3. ATHENA: widen O-5 to cover backup_estate.py:980 (unmounted-drive conflation in the estate/workflow half) and the same-day sort inversion
4. HEPHAESTUS: two stale REPO/research_outputs/_archive paths still live at daily_routine.py:537 and archive_dependencies.py:52 — the pre-O-4 bug in a second and third file
5. Operator: O-6 carried unchanged — both Sunday tasks still pass --dest "G:\My Drive\naiad-backups"
NEXT: File 004. Everything else in this lane is blocked behind it. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Queue 004 is filed and ratified, and D-0a is built. wait_for_drive() makes a sleeping disk distinguishable from a missing one, and logs its own wake latency so the timing constants get pinned by measurement instead of guessed. The contract asserts the operator disabled disk sleep and USB suspend; measured, neither is disabled.
LAST EVENT: 2026-08-12 — exchange/queue/004_move-clone-out-of-onedrive.md filed; scripts/drive_wait.py committed e16de8b and corrected 9f3747d; F-0-1 43/43, suite 287/1 unchanged; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-FILED-AND-D0A.md.
FACTS:
- 004 filed at 7,725 B / 121 lines, LF, UTF-8; all seven required fields present and the six queue README conventions met. BUILT stamp correctly ABSENT — ratified-and-partially-built is the truthful state [verified]
- The paste's own field check reported a FALSE MISSING on the RATIFIED stamp: grep without -F reads "**operator**" as a regex where ** is a quantifier. Third consecutive session in which a guard misreported a healthy artifact, and all three were checking strings containing markdown emphasis. Any paste grepping this project's prose must use grep -F [verified]
- D-0a built as scripts/drive_wait.py, 250 lines, ASCII-only, no side effects on import, REPO resolved from __file__ so it survives the Phase A move. Three states PRESENT/WOKE/UNREACHABLE, never raises; WOKE alone appends to exchange/status/DRIVE_WAKE_LOG.md [verified]
- DEFECT SHIPPED AND FIXED IN-SESSION: DriveWaitResult was a NamedTuple, so "%s" % result raised TypeError in the CALLER — the helper's NEVER-RAISES invariant reintroduced one layer up, with nine D-0b call sites pending. Found by this session's own cold probe. Now a frozen dataclass; F-0-1 gained six checks pinning it [verified]
- CONTRACT FACT REFUTED: Phase 0 says the operator "has since disabled USB selective suspend and disk-sleep on AC". Measured via powercfg: DISKIDLE = 30 SECONDS on AC and DC (units confirmed from powercfg's own output), USB selective suspend = ENABLED on both. Neither is disabled. Phase 0 is more necessary than the redraft claims, not less [verified]
- DEFAULTS STILL UNVALIDATED, and this session could not validate them. F-0-1's PRESENT reading is self-confounded — it probes D: on the line before measuring it. A cold probe idling 150s (5x the 30s timeout) with no D: access still returned PRESENT in 0.00s: the disk did not spin down. Zero WOKE observations; DRIVE_WAKE_LOG.md does not exist [verified]
- What IS established: the healthy path is free (PRESENT costs one stat call, 0.00s measured twice), so wiring nine call sites adds no cost when the drive is awake — D-0b's main risk is retired. The unhealthy path costs the full budget: drive_wait.py Q:/ returned UNREACHABLE at elapsed=18.00s, exit 2 [verified]
- The defaults can only be pinned from real unattended runs (the 07:00 daily after an overnight gap, the Sunday weeklies) — exactly the paths D-0b wires. An empty wake log today is the expected state, not a failure [verified]
PENDING:
1. ATHENA: D-0e (missed-run detector) is NEW and lands in Phase 0, which gates Phase A — it shares no code or failure mode with waking a disk. This is the same coupling that removing O-5 from Phase 0 was meant to break. Move it out, or let D-0b ship without it
2. ATHENA drafts / operator decides: strike or rewrite Phase 0's power-settings sentence to match the measurement. Cheaper alternative to the whole common case: powercfg /setacvalueindex SCHEME_CURRENT SUB_DISK DISKIDLE 0 — NOT run, it changes machine state and no authorization was given
3. HEPHAESTUS (D-0b session): add a per-process UNREACHABLE memo before wiring nine sites, or a cold-drive run pays 18s per gate and reads as a hang
4. HEPHAESTUS (D-0b session): commit F-0-1 into fixtures/, accepting the new suite count. drive_wait.py currently ships with 43 passing checks and NO permanent regression guard
5. ATHENA: the wake log records only WOKE, so an empty log cannot distinguish "never asleep" from "budget too short". D-0b's call sites should record UNREACHABLE where they halt
6. ATHENA: F-0-1 as drafted can pass without measuring anything — "PRESENT on a live root" is satisfiable by a probe that woke the drive itself. Respecify as a probe after a measured idle
7. Carried: O-5 widening (incl. backup_estate.py:980 and the same-day sort inversion), the two stale REPO/research_outputs/_archive paths, O-6's G: destinations
NEXT: Rule on item 1, then give the go for D-0b. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Queue 004 Phase 0 is complete and green in the current tree. Eight D: gates now wait for a sleeping disk before calling it absent, the missed-run detector is live, and the baseline Phase A must reproduce from C:/Naiad is recorded. Phase A was deliberately NOT begun.
LAST EVENT: 2026-08-12 — code commit 20ad593 pushed (D-0b 8 sites + 2 stale paths, D-0e); D-0d filed via 89c849f; proof runs 81fcc5f/e923850; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_PHASE-0.md.
FACTS:
- Step 0 found 004 and drive_wait.py ALREADY PRESENT and committed; neither was rewritten. drive_wait.py asserted still 250 lines and still a frozen dataclass [verified]
- D-0b wired 8 call sites: backup_estate assert_environment/phase_archive_root/backup_dest_root/_generations/retention phase half; daily_routine check_reminders + phase date; archive_dependencies membership. The 9th site from the earlier census (arch.is_dir()) is SUBSUMED — it sits downstream of an already-waited gate [verified]
- _generations() was UNGATED: an unmounted drive makes dest.glob() yield nothing (an empty glob is not an OSError), so the retention report printed "none found" for four good archives on an unplugged disk. O-4 fixed the phase half and left this one. Now prints NOT ENUMERABLE; the wait is resolved ONCE for both sections, not per-section [verified]
- G: exclusion is DECLARED, not detected, because detection does not work: GetDriveTypeW returns C:=3 FIXED, D:=3 FIXED, G:=3 FIXED — Windows reports the Drive mount as a fixed local disk, and an absent drive returns 1 NO_ROOT_DIR whatever it was. Overridable via NAIAD_NO_WAIT_ANCHORS [verified]
- TWO STALE PATHS FIXED, 3rd and 2nd copies of the defect O-4 fixed once. Measured live: HEARTBEAT read "phase: NONE" before and "phase: 2026-08-02" after — nine phase archives (1,043,591,544 B) were on the drive the whole time. The heartbeat had been calling the phase estate absent for six days. archive_dependencies had the same defect with a silent symptom [verified]
- D-0e live: banner above section 0, names every missing DAILY_<date> by name, report-only. Searches the daily ARCHIVE as well as the window, or the rolling window's own housekeeping reads as missed runs. Unreadable heartbeat prints UNKNOWN, never silence [verified]
- BASELINE for Phase A acceptance: suite 287 passed/1 skipped; --workflow 349/349 members verified both directions, 0 mismatches/strays/omissions, F-K1/F-K4/F-K5/F-K6b PASS, exit 0; daily routine exit 0 with all 4 jobs exit 0; F-0-1 43 checks 0 failed; F-0-3 28 checks 0 failed [verified]
- Provisional constants STILL unvalidated — every probe returned PRESENT at ~0.00s and DRIVE_WAKE_LOG.md does not exist. But the common-path cost is now retired as a risk: eight gates changed no measurable timing anywhere. The only real number is UNREACHABLE = the full 18.00s budget, confirmed live on Q:/ [verified]
PENDING:
1. ATHENA: O-5 is now WORSE by my own proof run — --force-same-day wrote a THIRD same-day workflow archive, so retention reads 8 generations with 4 outside the rule and three keep-slots held by one calendar day. Nothing deleted; the report never deletes
2. HEPHAESTUS: per-process UNREACHABLE memo, before anyone reports a cold-boot run as hung — eight gates can now each pay 18s in a single routine
3. HEPHAESTUS: mirror_phase_outputs() (backup_estate.py:538) is the one D:-capable site left unwaited — deliberate (interactive-only, arbitrary operator path) but an inconsistency
4. ATHENA: the wake log records only WOKE, so an empty log still cannot distinguish "never asleep" from "budget too short"
5. HEPHAESTUS: F-0-1 (43) and F-0-3 (28) are still NOT committed as regression tests — adding them moves the suite off 287/1, which is the number Phase A is measured against. Land them in the session AFTER Phase A
6. Operator: the publish budget WARNING could not be cleared — exchange/ is at 26.0% against a 25% warn line and the only mechanism that lowers it is queue 003 rotation, ratified 2026-08-11 and still unbuilt
7. Operator/ATHENA: Phase A blocking pre-work unchanged — A-2's three identity gates assert the path contains "OneDrive", so until they are amended NO post-move session can start
8. Carried: O-6 (Sunday tasks still pass --dest "G:\..."; Task Scheduler not modified by instruction), O-7, O-8
NEXT: Give the go for Phase A as its own session, or rule on item 1 first. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-12 ===
NOW: Queue 004 Phase A is ACCEPTED. The working clone now lives at C:/Naiad, outside every sync tree. The old OneDrive tree is INTACT and untouched — deleting it is Phase B, days from now. Every acceptance gate passed, so the single-rmdir rollback was not needed.
LAST EVENT: 2026-08-12 — A-2 amendments committed 75b7444 from the OLD tree before the copy; C:/Naiad created and verified; proof runs af86168 and b938e81 published FROM the new tree; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md.
FACTS:
- A-0 all five gates passed: HEAD==origin; untracked enumerated with --untracked-files=all; D: PRESENT 0.00s; C: free 44.24 GB vs 7.65 GB needed (3x a 2.55 GB tree); and ZERO dehydrated files of 2,452 — the 164 placeholders the 2026-08-12 census found have all been rehydrated. Attributes only; no file was opened [verified]
- A-1 swept 340 hits across 120 files and classified every one. 283 hits are PROSE-HISTORY and were LEFT — rewriting them would falsify the archive. Zero old-form absolute ROOT constants remain anywhere in the tree [verified]
- TWELVE AMENDMENTS committed 75b7444 FROM THE OLD TREE before the copy, so the new clone inherited corrected gates and history stayed linear. Three identity gates are now TWO-SIDED (HALT if the path contains OneDrive AND HALT unless it ends with C:/Naiad) because two complete clones coexist until Phase B; six ROOT constants use Path(__file__).resolve().parent.parent; three prose assertions corrected without rewriting any dated snapshot [verified]
- A-3 copied 2,482 files / 825 dirs / 2.373 GB in 26.4s, 0 failed 0 mismatched. __pycache__ removed from the COPY only: 6 dirs, 80 .pyc of which 79 embedded the old absolute path. The old tree still has its own 6, asserted [verified]
- A-4 ADOPT: 562 of 562 tracked files sha256-equal; HEAD identical; status --untracked-files=all byte-identical; untracked 3/3 equal; gitignored 213 vs 213 with a 0-byte delta; all five files >100 MB hashed equal; 5% sample equal [verified]
- A-4's FIRST pass said REJECT and was WRONG on all three counts — git ls-files emits raw path BYTES and text=True mangled the six filenames containing an em dash, and the gitignored comparison had not subtracted the 80 .pyc deliberately removed (293-213=80 exactly). Nothing was deleted on the strength of a failing check before the check itself was verified [verified]
- A-5 SIDE BY SIDE vs the Phase 0 baseline: suite 287/1 IDENTICAL; --workflow 0 mismatches / 0 strays / 0 omissions IDENTICAL with all 7 fixtures PASS; routine exit 0 with all 4 jobs exit 0 IDENTICAL; heartbeat phase 2026-08-02 IDENTICAL; publish pushed. Members 349->353 is +4 ADDITIONS with ZERO losses, proven by diffing the two archives' member lists [verified]
- NEGATIVE GATE TEST passes in three directions: OLD path HALTs (exit 1), C:/Naiad PASSes (exit 0), and an unrelated directory ALSO halts (exit 1) — the control proves the gate is genuinely two-sided rather than a single OneDrive test [verified]
- A-6 all three scheduled tasks repointed: only WorkingDirectory needed it, since Command is the venv (outside both trees) and the script paths are RELATIVE to Start In. Read back from XML, 18/18 assertions PASS — StartWhenAvailable, the principal SID and LogonType all preserved, and the two --dest "G:\..." arguments deliberately untouched (O-6). All Ready [verified]
- A-7 mirrored 37 files / 381.1 MB of census and mc1 to D:, copy-only, every file re-hashed AT THE DESTINATION, 0 mismatches. The harness project directory was COPIED to the C--Naiad key: 283 files and all six memory files in both, original left intact [verified]
PENDING:
1. Operator: RE-ATTACH the Cowork folder at C:\Naiad. HERMES and DIONYSUS lose their mount and CANNOT TELL YOU — a stale mount reads a frozen bus and reports it as current
2. Operator: from now on open Claude Code sessions in C:\Naiad, not the OneDrive folder
3. Operator/next tidy: I resurrected two files that the 2026-08-06 slimming had deliberately moved to docs/history/argus — importing the six worksheet modules to prove their ROOT executed them (no __main__ guard). No delete authorization, so they were left and a publish committed them in af86168. +12,850 B, +0.201% of the box; byte-identical copies remain in docs/history/argus
4. ATHENA: a FOURTH identity gate exists at prompts/PC1_...:55/:151/:155. It is a COMPLETED contract so it was classified prose-history and left, but re-running it would halt
5. ATHENA: O-5 is now FOUR-deep — -02 and -03 are this session's own proof runs, so one calendar day occupies all four workflow keep-slots and every distinct older generation reads as outside the rule
6. Operator, Phase B: the old tree's remote-tracking ref is STALE at 75b7444, so a session opening there sees 'up to date' while the true origin is b938e81 — a plausible, wrong picture
7. Operator: 28 of 138 permission rules in .claude/settings.local.json name the old path or slug and will stop matching. They degrade to fresh prompts, not failures. Reported, not edited
8. Carried: O-6, O-7, O-8, and the Phase 0 items (per-process UNREACHABLE memo; F-0-1/F-0-3 not committed as regression tests; the wake log records only WOKE)
NEXT: Re-attach Cowork at C:\Naiad, then run one clean scheduled day before Phase B. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===

=== STATUS ATHENA — 2026-08-14 — QUEUE 005 M2 RESTORE DRILL ===
NOW: M2 HALTED AT GATE 0. Nothing adopted, nothing written to any source, no Mac baseline recorded. The new Mac (Mac17,6 / M5 Max / macOS 26.3) is real and the clone is at the origin tip, but three Gate 0 preconditions failed independently and the drill never reached step 1.
LAST EVENT: 2026-08-14 — gate run on Luiss-MacBook-Pro.local; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-14_M2-RESTORE.md. One file written this session: that report. BOX COST ~11 KB.
FACTS:
- HALT 1: requirements-lock-2026-08-14-win.txt is absent from the working tree AND from all of git history (git log --all -- 'requirements-lock*' is empty). Not a fetch problem: fetch succeeded, HEAD==origin==db63b8c. M0's push did not cross; the file is still uncommitted on the Windows machine [verified]
- HALT 2: the LaCie is NOT ATTACHED. Four independent probes: /Volumes holds only Macintosh HD; diskutil list shows no external physical device; mount shows nine internal-only filesystems; system_profiler USB+Thunderbolt shows no external media. Then drive_wait itself returned UNREACHABLE root=/Volumes/LaCie attempts=6 elapsed=18.02s budget=18.0s — the one helper built to separate ASLEEP from ABSENT spent its full budget and said ABSENT [verified]
- HALT 3: ~/venvs does not exist, and the ONLY interpreter is /usr/bin/python3 = 3.9.6. engine/data.py:63 uses PEP 604 `dict | None` in a runtime signature, requiring 3.10+, so system Python CANNOT IMPORT THE CODEBASE. M1 step 6 is three blockers deep: install a modern Python, then build a venv, then pin against the lock file that does not exist [verified]
- ADOPTED LEDGER IS EMPTY: 0 files adopted, 0 folders entered, 0 mismatches, 0 single-witness adoptions. COPY-ONLY and NO-CLOBBER were never exercised because no copy was attempted. Rollback is deleting one report file [verified]
- THE TRACKED TREE NEEDS NO DRILL: 598 tracked files, 0 modified, 0 deleted, HEAD at origin tip. A clean status at the tip is cryptographic proof the tracked half is byte-correct — a STRONGER witness than any sidecar or two-witness pair, and it is free. The drill's real scope is the untracked artifacts plus the estate cache, nothing more [verified]
- THE TREE WAS ALREADY TRANSPLANTED, UNVERIFIED, BEFORE THIS SESSION. Home dir created 2026-08-14 22:46:37 and first boot 22:42:47 — a genuinely new Mac — yet git reflog still carries `clone:` from 2026-07-09 21:14:32. A fresh clone cannot hold a five-week-old reflog, so the whole ~/Naiad tree including .git and untracked files was bulk-copied in. The careful restore M2 was chartered to do HAS ALREADY HAPPENED CARELESSLY. It landed correct for the tracked half (proven after the fact by git); for the untracked half there is no evidence either way [verified]
- MATERIAL LOSS EXPOSED: of §2's list, _archive/seq8/mc1/census are present and tracked, but seq8_run2, census2a (29 manifest-pinned artifacts) and census2b are ABSENT and were NEVER TRACKED — git check-ignore returns nothing and git reports no deletions. They exist only on the LaCie mirror and carried clone. The LaCie is not a backup of this machine; for those three folders it is the SOLE ORIGINAL [verified]
- cache_dir() RESOLVES TO /Users/luis/.cache/naiad/data_cache on this platform (NAIAD_CACHE_DIR unset, os.name != 'nt'). It does not exist — estate cache is empty. Read from engine/data.py:39-48 rather than called, because line 47 mkdirs: ASKING WHERE THE CACHE IS CREATES IT. This session left no directory behind. The MANIFEST.json/manifest.json case-collision hazard is UNEXERCISED and still live on APFS [verified]
- naiad-backups/ (untracked, carried in): 15 of 15 sidecar'd archives re-hashed at rest, 0 mismatches; 3 ` (1)` browser-duplicate zips have no sidecar. NOT EXTRACTED, on two grounds: the sidecar sits beside the archive and was carried by the same unverified copy, so it is neither a repo-tracked sidecar nor a two-witness pair; and the newest estate is 2026-08-11, at least three days stale, predating the 2026-08-12 Phase A close and the 2026-08-14 M0/M1 work [verified]
- drive_wait IS NOT AN M3 ITEM. Given a POSIX path it resolved cleanly, polled six times across the full budget, poked for spin-up, never raised, and returned a well-formed UNREACHABLE that %-formats safely. No drive-letter assumption fired. Its docstring worries about surviving a move to C:/Naiad; the reverse crossing is already platform-neutral [verified]
- NO MAC BASELINE EXISTS. The suite was not run: under 3.9.6 it would SyntaxError at collection and produce a number that looks like a baseline and measures nothing. No failure is listed and nothing is tagged [expect-windows-ism], because nothing was observed. Classified nothing, fixed nothing, per the brief [verified]
- HALT 4, FOUND AT CLOSE: one publish() was attempted and got most of the way. It imports and runs fine under 3.9.6 (publish_exchange does not use the 3.10+ syntax that blocks engine/data.py), branch resolved, scope guard PASSED with exactly 2 staged paths both inside exchange/, D3 size budget not tripped, and it COMMITTED 35c293f. Then the push died: `fatal: could not read Username for 'https://github.com': Device not configured`. THIS MAC HAS NO GITHUB CREDENTIALS — HTTPS remote, no helper, no token, no TTY to prompt on. NOT a Windows-ism: publish() behaved correctly at every stage it controls and returned rather than raising, per its contract. THE BRANCH IS 1 COMMIT AHEAD OF ORIGIN and this report is NOT on the remote [verified]
- M3 NOTE ON INVOKING publish(): scripts/publish_exchange.py has NO __main__ guard. Running it as a script exits 0 and prints NOTHING — a silent no-op indistinguishable from success. It is a library; the entry point is publish(repo, date_str, remote="origin") at line 228 [verified]
PENDING:
1. Operator, BLOCKING: attach the LaCie. No external device is present at the USB or Thunderbolt layer. If you believe it is connected, the cable/port/enclosure has failed — check that before assuming data loss, and do NOT reformat or "repair" anything
2. Operator, BLOCKING: recover requirements-lock-2026-08-14-win.txt from the Windows machine before that machine is wiped. It exists only there
3. Operator, BLOCKING: install Python 3.10+ on this Mac. System 3.9.6 cannot import the codebase, so M1 step 6 cannot even begin
4. Operator: name the tool and source that bulk-copied ~/Naiad onto this Mac. If it truncated or skipped silently, none of its output can be trusted — and the untracked half has no independent proof
5. Operator, BLOCKING: configure GitHub credentials on this Mac (helper, PAT, or switch the remote to SSH) and push. 35c293f is local-only; the branch is 1 ahead of origin and this report exists nowhere else
6. Operator: NOTHING ON THE LACIE MAY BE REORGANISED UNTIL M3 ACCEPTS. This now guards three folders that exist in no other place
7. ATHENA: cache_dir() has a side effect on read (mkdir at engine/data.py:47). Any future gate that merely PRINTS the cache path will silently create it. Worth an amendment so resolution and creation are separable
8. Carried, untouched by this session: every Queue 004 PENDING item 1-8, including the stale remote-tracking ref in the old tree and the 28 stale permission rules
NEXT: Push 35c293f (PENDING 5), resolve PENDING 1-3, then RE-RUN M2 FROM GATE 0. Nothing was partially applied, so the re-run starts from a clean board. Owner: operator.
METRICS: operator actions this session = 0 · files adopted = 0 · sources touched = 0 · mismatches = 0 · halts = 4 · box cost = ~11 KB
=== END STATUS ===

=== STATUS ATHENA — 2026-08-14 — QUEUE 005 M2 AMENDMENT (supersedes parts of the entry above) ===
NOW: Same session, after the halt was filed. At OPERATOR DIRECTION the toolchain was installed, so HALT 3 is RESOLVED and the Mac suite baseline IS RECORDED. HALT 1 is DOWNGRADED. HALT 2 (no LaCie) and HALT 4 (no credentials) STAND. THE RESTORE DRILL ITSELF IS STILL NOT RUN AND NOTHING WAS ADOPTED — this amendment changes the environment around M2, not M2.
LAST EVENT: 2026-08-14 — uv + CPython 3.12.14 + venv installed; suite run twice; 31 stale Windows .pyc found; report amended and committed.
FACTS:
- SUPERSEDES the prior entry's claim that requirements.txt is unpinned. IT IS FULLY PINNED — pandas==2.2.3, numpy==2.1.3, pytest==8.3.4, PyYAML==6.0.2, requests==2.32.3, pyarrow==18.1.0. The environment is reproducible from the repo alone and the venv was built from it. HALT 1 drops from BLOCKING to DEGRADED: what the missing lock file costs is TRANSITIVE parity (11 packages resolved at 2026-08-14 current, not at whatever the Windows box held), not the ability to work [verified]
- NO PACKAGE MANAGER EXISTED: no brew at either path, no uv/pyenv/conda/mamba/asdf/MacPorts. `brew install python@3.12` fails at command-not-found, not at the install. Xcode CLT WAS already present with git/clang/gcc/make, so the slow prerequisite was already satisfied [verified]
- HALT 3 RESOLVED via the uv route (operator's choice, no sudo): uv 0.12.5 -> ~/.local/bin; CPython 3.12.14 in 1.79s; venv at ~/venvs/naiad; 6 direct + 11 transitive packages. ~/venvs/naiad/bin/python now exists, is executable, reports 3.12.14. NOTHING system-wide, NOTHING into ~/Naiad, /usr/bin/python3 untouched. Undo is one rm -rf of four paths [verified]
- MAC BASELINE RECORDED: 282 passed / 4 failed / 2 skipped in 11.30s. Windows reference (Queue 004 A-5) was 287/1. TOTALS MATCH EXACTLY — 287+1 = 288 and 282+4+2 = 288 — so NO TEST WAS LOST OR GAINED in the platform crossing; five changed state [verified]
- THE BASELINE IS PROVISIONAL AND MUST NOT BE COMPARED NAIVELY. It is a baseline of "Mac with an EMPTY ESTATE CACHE", because §3 could not run. All four failures are data starvation IN THEIR OWN WORDS: WarmupError "0 exec bars (need >= 2000), 0 governor bars (need >= 200)" at engine/replay.py:97, and 3x IndexError "index -1 is out of bounds for axis 0 with size 0" at tests/test_analytics.py:908. One skip literally reads "LITUSDT 1m not in the estate". RE-TAKE after the estate is restored [verified]
- ZERO FAILURES TAGGED [expect-windows-ism]. The brief's criterion is drive letters, schtasks, wevtutil, st_file_attributes — NOT ONE appears in any of the four tracebacks. Classified nothing further; cause is M3's [verified]
- THE ONE DRIVE LETTER SEEN WAS NOT A CODE DEFECT, AND THIS WAS PROVEN NOT ASSERTED. First run printed `SKIPPED [1] C:\Naiad\fixtures\test_f8_journal.py:110` ON MACOS. Re-running with PYTHONPYCACHEPREFIX pointed outside the repo (reads and writes bytecode elsewhere, modifies nothing in tree) returned IDENTICAL counts 4/282/2 and the path came back POSIX-relative. The drive letter came from STALE BYTECODE, not source [verified]
- 31 STALE WINDOWS .pyc IN THE TREE, of 73 total across six __pycache__ dirs, embedding literal C:\Naiad as co_filename. They are cpython-312 — MATCHING the 3.12.14 just installed — and the transplant preserved source mtimes, so CPython's staleness check PASSES and Python REUSES Windows-built bytecode. All 13 in scripts/ (drive_wait, publish_exchange, backup_estate, census2a/2b/mc1/mc2/seq8 programs), 3 in study/, 15 pytest-rewritten fixtures. DIRECT CONSEQUENCE of the unverified transplant. Queue 004 A-3 stripped __pycache__ deliberately during the OneDrive->C: move ("80 .pyc of which 79 embedded the old absolute path"); THE LESSON WAS LEARNED AND THEN LOST because this transplant skipped that process. NOT DELETED — that is a fix, and fixes are M3's. Impact is confined to reported paths; no outcome depends on them [verified]
- M3 INVOCATION NOTE: pytest.ini:9 sets `addopts = -q`. Passing -q again makes it DOUBLE-QUIET and SILENTLY SUPPRESSES THE FINAL COUNT LINE — the run ends on the FAILED list with no "N passed" anywhere. It looks like a crash and is not one. Use plain `python -m pytest` or -v [verified]
PENDING:
1. Operator, BLOCKING and now the ONLY thing standing between us and M2: ATTACH THE LACIE. Unchanged from the entry above
2. Operator, BLOCKING: configure GitHub credentials and push. Now THREE commits ahead of origin
3. Operator: RE-TAKE THE SUITE BASELINE after the estate is restored. The current 282/4/2 measures a machine with no data
4. Operator: recover requirements-lock-2026-08-14-win.txt for transitive parity — no longer urgent
5. Operator: add ~/.local/bin to PATH if you want `uv` available in a fresh shell
6. M3: 31 stale C:\Naiad .pyc left in place, deliberately. One find -exec rm -rf clears them whenever M3 wants
7. All other PENDING items from the entry above carry forward unchanged
NEXT: Attach the LaCie and re-run M2 from Gate 0. Owner: operator.
METRICS: operator actions this session = 1 (chose the install route) · files adopted = 0 · sources touched = 0 · mismatches = 0 · halts resolved = 1 · halts downgraded = 1 · halts standing = 2
=== END STATUS ===

---

=== STATUS ATHENA — 2026-08-15 — QUEUE 005 M3 PLATFORM SWEEP ===
NOW: M3 IS GREEN except two items neither of which is a code defect: F-M3-6 could not run because the LaCie was physically unmounted mid-session, and Spotlight exclusion needs GUI/sudo. The sweep found TWO REAL DEFECTS that were not path typos — a backup guard that was inert on macOS, and two residency gates that halted unconditionally — fixed both, cleared the live-code remainder to empty, and held the suite at 287/0/1. CENSUS WORK IS UNBLOCKED. Filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M3-SWEEP.md; ONE commit f403546, pushed.
LAST EVENT: 2026-08-15 — 116 hits re-enumerated live and classified; 50 mechanical edits applied by four parallel agents on disjoint file sets, every edit carrying both post-write assertions; residency core edited and smoke-proven by hand.
FACTS:
- DEFECT 1, THE SERIOUS ONE: backup_estate.drive_ready() was INERT on macOS. Every caller passed Path(root.anchor); on POSIX that is "/", the boot volume, ALWAYS MOUNTED — so the guard whose whole purpose is "a backup that lands on the machine it is backing up is not a backup" COULD NOT FAIL. Worse: the old default "D:/naiad-backups" is a RELATIVE path on POSIX, so --estate/--workflow would have written into ~/Naiad/D:/naiad-backups, INSIDE THE REPO BEING BACKED UP, and printed success. Fixed with volume_anchor() returning the mount point; proven to halt (SystemExit 2, truthful 18.03s measurement) with the LaCie absent [verified]
- DEFECT 2: census2a_program.py:185 and mc2_program.py:270 asserted OUT.drive.upper() == "D:". Path.drive is ALWAYS "" on POSIX, so both HALTED UNCONDITIONALLY — the gate was DEAD, not strict, and the identity limb (cwd endswith "c:/naiad") was equally unsatisfiable. Restated as containment under ROOT/research_outputs plus the v2 two-sided cloud-marker gate. BOTH NOW PRINT THEIR FIRST PASS LINES ON THIS MACHINE — census work is unblocked [verified]
- CLASSIFICATION REQUIRED A FOURTH BUCKET THE BRIEF DID NOT NAME. The pattern [A-Za-z]:[/\] also matches https://, "error:\n" and "^zone:\s*" — regex artifacts that are not defects in any category and editing one would be damage. Final: 45 FIX / 7 HISTORY / 2 ALREADY-DEAD / 8 NOT-A-HIT across the agent groups, plus 54 core hits classified directly. Two judgment calls went to ALREADY-DEAD not FIX and were verified live: daily_routine.py:573 cannot print (its alert fires only `if od is False`, and _onedrive_running() returns None off Windows), and engine/data.py:44 is correctly guarded and is the MODEL, not a defect [verified]
- CRLF SIDECARS FIXED, AND .gitattributes DELIBERATELY KEPT TO ONE LINE. All 9 tracked *.sha256 converted CRLF->LF with recorded digests asserted byte-identical; F-M3-3 native `shasum -a 256 -c` now 9/9 OK exit 0 with no tr workaround, which also re-verifies ~1.04 GB of phase archives. A first draft of .gitattributes also pinned *.py/*.json/*.sh and WAS REVERTED UNAPPLIED: eleven source files are still CRLF and the wider rule re-normalised them wholesale, a ~15,000-line diff that would have buried the sweep. Source EOL policy is its own commit; the eleven files are named in .gitattributes [verified]
- F-M3-6 HALTED, NOT SKIPPED, AND NOT CLAIMED AS PASSED. The LaCie was unmounted PARTWAY THROUGH this session — attached for M2 (~8.7 GB hashed across it), absent now at the device layer (mount empty, /Volumes holds only Macintosh HD, diskutil list external empty, no USB/Thunderbolt media). Same condition as HALT 2 on 2026-08-14. Diagnosed rather than assumed: the first symptom was Python reporting os.path.exists('/Volumes/LaCie')==False while an earlier ls had succeeded, which looks exactly like a macOS permissions problem and is not. The v2 backup WRITE path is fixed but UNPROVEN end-to-end; the HALT path is proven [verified]
- SUITE HELD AT 287 passed / 0 failed / 1 skipped BEFORE AND AFTER, zero delta, no fixtures added (F-M3-3 and F-M3-6 were specified as printed transcripts, so the count stays directly comparable to the M2 baseline). Live-code remainder verified EMPTY by Python tokenize — filtering by EXECUTABLE POSITION rather than text stripping — leaving 2 matches, both regex artifacts (an SVG namespace URI and the literal prose "result:\n"). One error my own edit introduced was caught by the smoke proof and fixed: removing wait_for_drive left both preflights returning r.state with r undefined [verified]
PENDING:
1. Operator, BLOCKING F-M3-6: reattach the LaCie and run `~/venvs/naiad/bin/python scripts/backup_estate.py --workflow`. Until then the v2 backup write path is fixed but unproven
2. Operator, READ TWICE: if ANY backup was taken on this Mac before today, check for a stray ~/Naiad/D:/naiad-backups directory — the old code would have written there and reported success. No such directory exists now, so there is no evidence it ever ran; treat any backup taken on this machine since the crossing as unverified until F-M3-6 passes
3. Operator, the one GUI/sudo item: 549 items under research_outputs are Spotlight-indexed and mdutil CANNOT target a subdirectory ("invalid operation"). Use System Settings -> Siri & Spotlight -> Spotlight Privacy and add ~/Naiad/research_outputs and ~/.cache/naiad. A .metadata_never_index marker was written as the only no-sudo lever, but its efficacy for a subdirectory is NOT PROVEN and is not claimed. Time Machine IS done and read back [Excluded]
4. Operator: exchange/ was at 38.7% of its 6,390,000 B budget at the last publish and publish() REFUSES above 40%. This report pushes it closer. ROTATION IS DUE BEFORE THE NEXT REPORT or the next publish fails closed
5. Operator, deferred not taken: eleven source files are still CRLF. Pinning *.py to LF is defensible policy and needs its own commit and its own before/after suite run
6. M4 is next. Neither outstanding item blocks M4, and neither blocks census work
NEXT: Reattach the LaCie and run F-M3-6; clear Spotlight via the privacy list. Owner: operator. Then M4.
METRICS: operator actions this session = 0 · hits classified = 116 · edits = 50 agent + core by hand · real defects found = 2 · files changed = 48 · suite delta = 0 · fixtures added = 0 · proofs halted = 1 (F-M3-6, hardware)
=== END STATUS ===

---

=== STATUS ATHENA — 2026-08-15 — QUEUE 005 M4 LAUNCHD ===
NOW: M4 IS DONE. Three launchd agents replace the three dead Task Scheduler entries and are PROVEN — bootstrapped into gui/501, schedules read back from launchd's own registry, two agents force-run and their logs read back. The named-set rotation moved eight spent CENSUS-2A run documents off the bus with all eight hashes verified equal at the destination and nothing deleted. F-M3-6 CLOSES FOR THE WRITE PATH and stays OPEN for the estate archive's shape. Suite held at 287/0/1. Filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_M4-LAUNCHD.md; ONE commit 4712ba1, pushed.
LAST EVENT: 2026-08-15 — rotation executed and committed; --workflow and --estate both run live on the attached LaCie; three agents armed and kickstarted.
FACTS:
- ROTATION DONE, AND rotate_reports.py WAS NOT TOUCHED. The eight BUILD_2026-08-12_CENSUS2A_RUN_*.md are dated three days ago and the scheduled sweep correctly selects NOTHING (--dry-run: 0 candidates, 93 too young). AGE_DAYS = 30 is a pinned constant and widening it — even behind a new flag — would have dismantled the guard 003 ratified in order to do a thing already authorised by name. The named set was driven through the SAME D-1 semantics by importing rotate_reports' own sha256_file/git/append_log, so the hash discipline is the same code, not a re-implementation. All 8 R100 renames, all 8 sha256 EQUAL at destination, git log --follow returns full history at the new path. CENSUS2A_CLOSEOUT stays — it is the pickup document [verified]
- THE 38.7% IN THE M3 PENDING WAS STALE, AND THE BOX WAS NOT REFUSING. Measured at gate 0: 2,504,112 B = 39.19%, level WARN. publish() warns at/above 25% and refuses only STRICTLY above 40%; the previous publish 6628a6d SUCCEEDED. Rotation freed 135,238 B -> 2,368,874 B = 37.07%, now 37.18% after this session's publishes [verified]
- THE PUBLISH IS NOT BELOW THE WARN THRESHOLD AND CANNOT BE. Getting under 25% needs 1,597,500 B, i.e. 778,508 B MORE must leave exchange/ — 5.8x the entire eight-file named set. The set was NOT widened to try: expanding an operator-named set to hit a number means rotating documents nobody judged spent. What the rotation did buy is headroom to REFUSE, doubled from 2.12 to 4.24 points. DIGEST §2's "two ratified mechanisms in arithmetic conflict" is resolved ONCE BY HAND for eight files and returns in the general case on 2026-08-27 [verified]
- F-M3-6, HONESTLY SPLIT. --workflow PASSED 8/8 exit 0: 391/391 members verified bidirectionally, 0 mismatches, archive + sidecar on the LaCie, no-clobber correct both directions. --estate is 6/8 exit 1, and the two failures are ONE fully-diagnosed defect that is NOT in the v2 write path. The estate zip holds 78 entries under 74 unique names: the M2 restore (Aug 15 02:16) unpacked a prior archive INTO the cache root, recreating _repo/ INSIDE the cache, so estate_members() emits _repo/census.json twice — once from the walk, once from the companion logic. Those two copies are BYTE-IDENTICAL. The failing fixture comes from the OTHER collision: the cache's own MANIFEST.json (11,589 B) and build_archive's generated manifest (12,121 B) share a name, zipfile.read() returns the LAST, so F-K4 compares the wrong one and reports 1 hash mismatch; the name collapse is what makes F-K1 report 1 omission. NO DATA IS LOST: klines 60/60, funding 10/10, F-K2 passes, testzip() returns None, F-K5 re-read clean from the LaCie. What is broken is the archive's SHAPE and therefore its self-verification. NOT FIXED — the remedy is deleting ~/.cache/naiad/data_cache/_repo/ and this session carries a no-deletions rule; same precedent as M3's 31 stale .pyc [verified]
- THE DAILY ROUTINE WAS ARMED-LOOKING AND WOULD NOT HAVE RUN AT ALL, AND THE CAUSE WAS OURS. routine_jobs.json said "python": "python". git log -L shows that bare name was introduced THREE COMMITS AGO by f403546 "M3 platform sweep", replacing a working C:\venvs\naiad\Scripts\python.exe — a regression FROM the port, not something the port failed to reach. main() guards with `if not Path(python).exists()`, and Path("python") is RELATIVE, so from WorkingDirectory /Users/luis/Naiad it resolves to /Users/luis/Naiad/python and the routine ABORTS AT STARTUP. It never reaches the per-job exit=126 path — an earlier draft and commit 4712ba1's message both said exit=126 and that is WRONG, corrected in the report. The guard is good design and the failure would have been LOUD; what made it dangerous is that no agent existed to read the log. Now the absolute venv path, version 4 -> 5, and PROVEN under launchd: the kickstarted run's process table shows PID 6714 (launchd's child) spawning PID 6834 running /Users/luis/venvs/naiad/bin/python scripts/daily_brief.py, which is precisely the value that was broken [verified]
- THE RETIRED BRIEF JOB STILL RUNS. That same kickstart exposed it: routine_jobs.json marks daily_brief.py "retired": "2026-08-05", "scheduled": false per ruling D-3, and `grep -n "scheduled\|retired" scripts/daily_routine.py` returns NOTHING. The job loop is unconditional `for job in reg["jobs"]`. Both keys are decorative; a job retired ten days ago runs on every execution and makes live network fetches. REPORTED NOT FIXED — honouring the flag changes what the routine DOES, which is ruling-level, not builder-level [verified]
- GOOGLE DRIVE IS UPLOADING THE SUBSTRATE AND THE BACKUP VAULT, FOUND NOT LOOKED FOR. `git add -A` aborted with `fatal: unable to stat '.tmp.driveupload/1915'` — git stat'd an entry Drive removed mid-scan, which is a NON-DETERMINISTIC failure that only occurs during an upload window. /Users/luis/Naiad/.tmp.driveupload sits in the REPO ROOT, untracked and unignored: 952 entries at 12:59, 137 at 13:14, 6 by 13:16 — it drains as Drive uploads. THE SIZE FRAMING IN THIS ENTRY'S FIRST DRAFT WAS WRONG AND AN ADVERSARIAL CHECK CAUGHT IT: the "7.8 GB" is not 7.8 GB of disk. Every large entry is a HARDLINK into the working tree (link count 2; inodes shared with research_outputs/seq8_run2/seq8_cascades.jsonl, research_outputs/seq8/seq8_outcomes.jsonl and naiad-backups/naiad_estate_2026-07-28.zip), so marginal disk cost is ~0 and any "N GB" figure double-counts the repo's own content. THE CORRECTED FINDING IS WORSE: those hardlinks name WHAT DRIVE IS UPLOADING — the study substrate that .gitignore keeps local precisely because it must stay local, and the operator's backup vault. That contradicts DATA RESIDENCY v2 directly. AND THE IDENTITY GATE CANNOT SEE IT: the two-sided v2 gate greps OneDrive / com~apple~CloudDocs / Mobile Documents and requires pwd == $HOME/Naiad; BOTH SIDES PASS, because the repo is not under CloudStorage — Drive reaches it via a sibling symlink and realpath('/Users/luis/Naiad') is unchanged. A marker-grep gate structurally cannot detect this class of sync. Added to .gitignore so git cannot sweep it; NOTHING DELETED — it is Drive's working state, not Naiad's [verified]
- LAUNCHD GAVE US StartWhenAvailable FOR FREE. The Windows tasks had to set it explicitly so a run missed while the machine was off or asleep fired at next wake. launchd does that BY DEFAULT for StartCalendarInterval, so none of the three plists carries an equivalent key — there is not one to carry. The stale --dest hazard was REMOVED rather than fixed: the Windows tasks passed --dest "G:\My Drive\naiad-backups" explicitly at a now-empty path; the agents pass no --dest, and the kickstart log confirms `(no --dest given; from built-in default)` [verified]
- THE KICKSTARTED WORKFLOW RUN REFUSED, TRUTHFULLY, AND THAT IS A STRONG PROOF. exit 3, log read back: "REFUSING TO CLOBBER: naiad_workflow_2026-08-15.zip already exists ... written TODAY". Today's archive existed because F-M3-6 wrote it an hour earlier. One refusal demonstrates launchd started the job, the absolute venv interpreter ran, WorkingDirectory was right, the LaCie was reachable, no-clobber fired instead of destroying today's archive, stdout reached the configured log, and exit 3 propagated back where launchctl print can see it [verified]
PENDING:
1. Operator, HIGHEST CONSEQUENCE: should Google Drive sync ~/Naiad at all? It is the only open item that can lose or corrupt data rather than merely block a publish, and it is one decision
2. Operator: the box is 37.18% and still WARN. Below-warn needs 778,508 B more out of exchange/. Either name a second, larger rotation set or accept WARN as the working state
3. Operator, then code lane: F-M3-6's estate half stays OPEN until ~/.cache/naiad/data_cache/_repo/ is removed and the MANIFEST.json name collision is decided. Nothing is lost meanwhile; the archive is complete and CRC-clean
4. Code lane: extend the identity gate to detect Google Drive alongside OneDrive / CloudDocs / Mobile Documents
5. Ruling needed: should daily_routine.py honour "scheduled": false? Today it ignores it and runs the retired daily_brief.py every time
6. Code lane: backup_estate.py has publish welded in with no --no-publish, so "one publish per session" is unachievable whenever a backup runs, and a backup run with anything staged outside exchange/ fails at publish and git-resets the operator's index
7. Operator's M5: the three slot-anchored brief triggers (london / ny_am / post_ny) have NO launchd counterpart. com.naiad.daily runs slotless so slot-aware jobs report SKIPPED by design. launchd's StartCalendarInterval has no timezone field and fires on machine local wall-clock, so an America/New_York anchor needs a regenerating installer or a wrapper
8. Carried unchanged from M3: Spotlight privacy list (GUI/sudo); eleven source files still CRLF
NEXT: Settle the Google Drive question. Owner: operator. The agents are armed and need nothing further — daily fires 07:00, estate Sundays 08:00, workflow Sundays 08:30.
METRICS: operator actions this session = 0 · files rotated = 8 · hash mismatches = 0 · deletions = 0 · agents armed = 3 · agents force-run = 2 · real defects found = 3 (interpreter, retired-job, Drive sync) · defects fixed = 1 · suite delta = 0 · fixtures added = 0 · commits = 1 (+1 correction, see report §8)
=== END STATUS ===

---

=== STATUS ATHENA — 2026-08-15 — ZIP RESIDENCY RULING + DEDUPE PASS ===
NOW: 5.98 GB deleted, every byte of it individually gated on a fresh sha256 match against its LaCie twin computed in the same run. ZERO mismatches, ZERO surprises, ONE file kept. ~/Naiad went 10G -> 4.6G. F-M3-6 IS NOW FULLY CLOSED: the estate half finally returns 8/8 exit 0, though NOT from bucket (d) alone — the fourth name collision was a reserved-name bug in backup_estate.py and needed code. Suite held at 287/0/1. Filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_ZIP-RESIDENCY.md; ONE commit a61a695, pushed.
LAST EVENT: 2026-08-15 — 71 files verified-then-deleted across four buckets; ~11.6 GB read to authorise 5.98 GB of removals.
FACTS:
- THE GATE WAS RUN STRONGER THAN SPECIFIED, DELIBERATELY. The authorization allowed "sidecar where one exists, direct twin-hash otherwise". BOTH SIDES WERE HASHED EVERY TIME and the sidecar was used only as an extra check, because a sidecar proves what a file WAS, not that the twin is still on the volume and still intact — and the twin was about to become the only copy. 33 files carried both-side sidecar cross-checks; 0 disagreed. Totals: (a) 9 files / 1,043,591,544 B, (b) 51 / 3,061,562,754 B, (c) 8 / 1,870,141,663 B, (d) 3 / 76,024 B. Grand total 5,975,371,985 B [verified]
- ONE FILE KEPT, AND THE RULE IS WHY. naiad-backups/.DS_Store has no LaCie twin, so the gate kept it exactly as instructed rather than making an exception for something obviously worthless. It is now the ONLY thing keeping naiad-backups/ alive, at 8.0 KB. Retiring the directory is `rm ~/Naiad/naiad-backups/.DS_Store && rmdir ~/Naiad/naiad-backups` and it is the operator's call. The three emptied subdirectories were rmdir'd — removing an empty directory destroys no data [verified]
- (c) CONFIRMED ITSELF TO THE BYTE. The 8 discarded seq8_run2 data files total 1,870,141,663 B against the brief's "~1.87 GB". The 3 KEPT manifests were identified from the record, not guessed: queue 003 line 38 accounts the folder as "8/8 data files identical, 3/3 manifests", and the 2026-08-11 R1-R2-R3 report §4a names them by hash as the only three files that DIFFER from seq8 — extract_manifest, outcomes_manifest, views_summary. That difference is precisely what makes them the run's unique provenance and the only thing a discard would cost. README_R3.md written naming the twins' path [verified]
- (e) CONDITION MET: ~/Naiad IS NO LONGER DRIVE-REGISTERED, established from Drive's own sqlite rather than from the absence of a folder. root_preference_sqlite.db roots = 0 rows; both accounts' mirror_sqlite.db root_config = 0, mirror_item = 0, pending_uploads = 0. The /Users/luis/Naiad strings still in those files are residue in freed pages. The M4 finding is closed — the operator unregistered it [verified]
- (e) NEARLY MATTERED ENORMOUSLY, AND THIS IS THE PART WORTH REMEMBERING. During the dry run naiad-backups/.tmp.driveupload/ held four entries with LINK COUNT 2 sharing inodes with the vault's estate zips (inode 417838 = naiad_estate_2026-07-28.zip, etc). DELETING A ZIP WHILE ITS STAGING HARDLINK SURVIVES FREES NOTHING — it only decrements the link count. Bucket (b) would have reported 3.06 GB freed while du barely moved. The tool was given an inode-identity gate for exactly that case (same inode is not "probably the same bytes", it IS the same bytes); in the event Drive drained them first and du confirms the space really came back [verified]
- F-M3-6 CLOSES, BUT (d) ALONE DID NOT DO IT — REPORTED, NOT QUIETLY RETRIED. The first estate run after (d) returned 5/8. Two causes. F-K3 was MY OWN FAULT: I edited POINTER.md while the archive was building, and F-K3 compares git porcelain before/after, so it correctly caught the tree changing mid-run; the second run on a quiet tree passed. F-K1 and F-K4 were the FOURTH collision, which (d) could never have fixed: build_archive() writes the member index as MANIFEST.json and verify_archive() reads it back by that name AND excludes it from the member set, while the estate cache has its own MANIFEST.json at its root. Measured in the 5/8 archive: 75 entries, 74 unique, MANIFEST.json twice — the cache's 11,589 B copy at offset 0 and the generated 11,658 B index at the end. zipfile returns the LAST, so F-K4 restored the wrong one (1 hash mismatch) and the excluded name left the cache's copy unmatched in pinned (1 omission) [verified]
- THE FIX PRESERVES THE DATA RATHER THAN DROPPING IT. Symmetric with the existing REPO_PREFIX rather than novel: RESERVED_ROOT_NAMES = {"MANIFEST.json"}, colliding members stored under ESTATE_PREFIX = "_estate/", resolve_member() maps it back. Dropping the cache manifest from the archive was the SMALLER change and would have quietly made restores incomplete — a silent hole in a backup is worse than the bug it fixes. Proven: 74 members / 74 unique / 0 duplicates, resolve_member('_estate/MANIFEST.json') round-trips to the real file, and --estate --force-same-day is 8/8 exit 0 with 74/74 verified both directions [verified]
- THE RETENTION SCAN NO LONGER CRIES WOLF. An empty local _archive is the NORMAL end state of a cycle under the new ruling, and the old scan printed "- none found" for it — the same sentence it prints when something is genuinely wrong. Now: "CURRENT CYCLE EMPTY — this is BY DESIGN and is NOT a finding"; the 9 tracked sidecars printed in EVERY branch as the FINGERPRINT SET, because they are the one part of the record needing no volume and no local zip; aged-out archives enumerated under ruling O-4's three states. What stays sharp: a sidecar with NO archive on either side is still reported in bold. Today that gap is empty, 9 for 9 [verified]
- RULING 4a IMPLEMENTED. daily_routine.py honours "scheduled": false — checked BEFORE script.exists(), since a retired job need not still be on disk. brief now reports SKIPPED(retired 2026-08-05) on the console and is named in the DAILY report ABOVE the failures, because "all jobs OK" printed beside a job that never ran is technically true and practically a lie. Worth 622.0s of the 623.2s the M4 launchd proof measured. daily_brief.py NOT deleted; brief_capture.py still imports it [verified]
- IDENTITY GATE LEARNS DRIVE, AND WAS TESTED IN BOTH DIRECTIONS. A path grep cannot see Google Drive — the repo is not under CloudStorage, Drive reached it via a sibling symlink, and realpath is unchanged. The third limb looks for the ARTEFACT: .tmp.driveupload plus Drive's two id-indexed shadow folders, at repo root and one level in, the two depths where real sightings occurred. Added identically to census2a_program.py and mc2_program.py. Passes clean now AND fires on a planted marker — a gate tested only on the passing case is untested [verified]
PENDING:
1. Operator: naiad-backups/.DS_Store is the one file the gate kept. rm + rmdir retires the vault directory entirely
2. Operator, M5 remainder and unchanged: Spotlight privacy list (GUI/sudo); Cowork remount; confirm the Drive mirror of /Volumes/LaCie/naiad-backups shows synced. That last one is now LOAD-BEARING rather than cosmetic: Drive no longer mirrors ~/Naiad, so the LaCie mirror is the ONLY cloud path for these archives and it is what closes 3-2-1 for the newest pair
3. Operator, carried from M4: the box is 38.5% and still WARN. This session freed DISK, not bus
4. Code lane, carried from M4: backup_estate.py still has publish welded in with no --no-publish, which is why this session produced three publishes rather than one
5. Code lane, trivial and new: exchange/.DS_Store is TRACKED despite the .gitignore rule — it predates the rule, so the rule never applied to it, and every auto-publish keeps committing it. `git rm --cached` fixes it
NEXT: Confirm the Drive mirror shows synced — it is what closes 3-2-1 for the 2026-08-15 archives. Owner: operator.
METRICS: operator actions this session = 0 · files verified = 71 · files deleted = 71 · bytes freed = 5,975,371,985 · hash mismatches = 0 · files kept by the gate = 1 · disk 10G -> 4.6G · code defects found = 1 (reserved-name collision) · defects fixed = 1 · rulings implemented = 2 (4a, zip residency) · suite delta = 0 · commits = 1
=== END STATUS ===

=== STATUS_ATHENA — 2026-08-15 (box governance accepted) ===
NOW: **Box governance accepted from APOLLO 2026-08-15; thresholds recalibrated warn 0.40 / refuse
0.70 on the 16 MB [operator] ceiling; D3 metering gap CLOSED (tick-set metering live);
named-constant protocol adopted into CONVENTIONS.**
CLASS: infrastructure / governance transfer. NO REGISTRATIONS.
LAST EVENT: 2026-08-15 -- APOLLO -> ATHENA box & publish-guard governance handoff, implemented
BASIS: exchange/reports/NOTE_APOLLO_2026-08-15_TO_ATHENA_box-governance-handoff.md
       sha256 e7cfae19d45983f3f7be06a4af660b9c032fc57f2afde313aa12ed7ea153b7af (filed verbatim
       this session, per the note's own Route line)
FACTS:
 1. THE NOTE'S FACTS WERE VERIFIED BEFORE BEING GOVERNED ON. BOX_BYTES = 16,000,000, warn 0.50,
    refuse 0.80 -- all three MATCH publish_exchange.py:86-88 exactly. The note's byte figure
    (2,568,320 B / 16.05%) reads 2,593,743 B today; the delta is bus growth from two later publishes
    (2925ebe, 6f2c79a) and is attributable commit by commit, not a discrepancy. Governing facts
    matched; the measurement had simply moved on. No HALT.
 2. THRESHOLDS RECALIBRATED warn 0.50 -> 0.40, refuse 0.80 -> 0.70. Reason on the record: the raise
    moved the ceiling but carried the fractions up proportionally, so the first warning would not
    have arrived until 8 MB -- the bus tripling with nothing said. 0.40/0.70 warns while there is
    still room to act. WARN 6.4 MB - REFUSE 11.2 MB - current tick set 2.85 MB.
 3. BOUNDARY SEMANTICS PRESERVED VERBATIM, and proved rather than asserted: the comparators are
    unchanged (`> REFUSE`, `>= WARN`), so exactly 70.0% WARNS and does not refuse, exactly as
    exactly 80.0% did. F-BOX-1 pins both edges and derives them from the constants, so the next
    re-pin re-tests itself instead of passing on stale numbers.
 4. THE D3 METERING GAP IS CLOSED -- open since my own queue-003 report of 2026-08-11 and
    transferred with the governance. The box holds LEDGER.md AND exchange/ (DIGEST section 1); the
    guard metered exchange/ alone and under-reported by the ledger's size. THE TICK SET NOW
    GOVERNS: TICK_EXTRA = ("LEDGER.md",), measured at HEAD because publish only ever commits
    exchange/. Today that is 2,593,743 + 255,011 = 2,848,754 B = 17.80% against
    16.21% exchange-only -- a 1.59-point correction.
 5. BOTH FIGURES PRINT ON EVERY PUBLISH, not only on warn/refuse, and every percentage carries its
    absolute MB beside it -- because a percentage against a ceiling that has just moved is exactly
    the number a reader mis-reads. The exchange-only figure is kept for continuity with every prior
    report; result["bytes"]/["fraction"] keep their old meaning and the governing values are new
    tick_* keys, so no existing consumer was handed a silent redefinition.
 6. THE NAMED-CONSTANT PROTOCOL IS ADOPTED AS CONVENTIONS 6.4 (TOC and body), credited "APOLLO
    handoff 2026-08-15", and IT GOVERNED THE SESSION THAT ADOPTED IT: all three legs run -- NAME,
    VALUE, THRESHOLD TEXT -- with a pin-vs-import decision recorded per site. It caught one live
    stale prose site (rotate_reports.py docstring, "warn 50%, refuse 80%") that a name-only grep
    would have missed. Its corollary, added from the same day's three defects: after editing a
    document, RE-READ THE DOCUMENT.
 7. THRESHOLD CUSTODY IS WRITTEN INTO CONVENTIONS 4.2: the ceiling, the fractions and the metered
    set are ATHENA's; changes route ATHENA-first; no lane edits them on its own authority.
 8. ROTATION UNTOUCHED, as the operator's ruling required: AGE_DAYS = 30, queue 003 next eligible
    ~2026-08-28. rotate_reports.py imports the live constants and needed no value change; only its
    docstring's stale prose was corrected.
 9. PINNED-VS-IMPORT, per site: publish_exchange.py = the one definition - census2b_report.py and
    rotate_reports.py IMPORT - census2b_oracle_report.py and mc1_report.py stay PINNED + labelled
    (they regenerate FILED documents; a historical report reproduces history, and both keep their
    self-consistent 6,390,000 / warn 25 / refuse 40 text).
10. SUITE 226 passed / 0 failed / 0 skipped, up from 214 -- delta +12, all F-BOX-1
    (tests/test_box_guard.py, new).
PENDING (operator): the ~1% naming trip-wire in CONVENTIONS 3.2 still moved with the box, from
~63,900 B to ~160,000 B. Left proportional, flagged in the conventions themselves; pin it absolute
at ~64,000 B if the intent was a sensitivity rather than a fraction. APOLLO raised it, it is now
mine to carry, and it is the one box question still open.
NEXT: the next all-lanes note carries the one-line acknowledgment to APOLLO. Owner: ATHENA.
METRICS: operator actions this session = 1 (the box-governance go) - constants changed = 2 -
dependents audited = 6 - fixtures added = 1 (F-BOX-1, 12 assertions) - suite delta = +12 - D3 gaps
closed = 1
=== END STATUS ===

=== STATUS_HEPHAESTUS — 2026-08-15 (filed to ATHENA's ledger; she commissioned it) ===
NOW: THE GREAT COLLAPSE landed. CONVENTIONS.md is restructured to a lane-scoped CORE model: a §0
     every lane reads every session (4,934 B of a 6,000 B budget), then eight addressed sections
     S1-S8, each opening "WHO READS THIS". Every rule is RULE / BECAUSE / EARNED-BY. 27 incident
     narratives extracted to docs/CASELAW.md (CL-1..CL-27), tracked and OFF the bus at zero box
     cost. Two TOCs at the head; nine «NAIAD-S*» tokens, each appearing exactly twice in the file
     and nowhere else in the repo. LEDGER.md gains STANDING VERDICTS. Memory's landing sites exist.
LAST EVENT: 2026-08-15 — F-CONV 4/4 PASS; suite 299 passed / 0 failed / 1 skipped.
FACTS:
- PRIME DIRECTIVE now reads, verbatim: "Naiad develops profitable momentum trading systems. Secret
  Sauce is such system." The 2026-08-01 wording is REPLACED, not annotated, with a dated note
  quoting the old text once [ratified]
- RULE CENSUS, measured not asserted: 422 rules before, 422 after, 0 lost. Nine agents enumerated
  the pre-collapse file; ten more hunted losses adversarially against the rewrite [verified]
- THE CENSUS EARNED ITS KEEP: it found EIGHT rules genuinely dropped by the rewrite, and no fixture
  would have caught any of them. All eight restored and re-verified by grep -F. Three of the eight
  came from one place - the old §9 list, distributed section by section [verified]
- IT ALSO CAUGHT A DEFECT I INTRODUCED: §0's identity-gate rationale was INVERTED (it said the
  marker side passes a cloud copy; the path side does). §0 and §2.1 now agree and both are correct
  [verified]
- CONVENTIONS 64,012 B -> 64,008 B. It SHRANK while absorbing ~12 KB of content it never carried
  (§2.1 GEOGRAPHY, §7 FRAMES, THE INDEX) plus ~1.5 KB of new dated corrections - after 46 machine-
  checked lossless compression edits. The margin is 4 B and that is thin [verified]
- 287-vs-214 RECONCILED ON THE RECORD: same tree, same moment, TWO SCOPES. fixtures/ = 74 (73 pass
  + 1 skip); tests/ = 214 pre-F-BOX-1; 74 + 214 = 288 = 287 passed + 1 skipped. 214 was tests/
  alone. The BOX-GOVERNANCE report's "different tree" explanation is wrong - a different SCOPE of
  the same tree - left uncorrected in that filed report per §6.4 leg 3 [verified]
- BACKUP_DEST_DEFAULT: CONVENTIONS asserted it was still Windows-era D:/naiad-backups. FALSE - it
  is /Volumes/LaCie/naiad-backups (backup_estate.py:328, read this session). The stale text was
  DANGEROUS: it told lanes to pass --dest explicitly, which outranks the default and re-enables the
  very override that kept Sunday runs writing to a dead Drive path (CL-27). Rewritten with a dated
  correction [verified]
- APOLLO's carried backlog (B-1/B-3, Q1c-Q11) MOVED to LEDGER_APOLLO.md - it is lane state, and §5
  already rules lane state lives in the lane ledger. Kept ON the bus deliberately: APOLLO reaches
  repo content only through the box, so docs/ would have hidden it from its own owner [ratified]
PENDING (operator):
 1. Sync now. Until then APOLLO/ARGUS/ATHENA read the pre-collapse file.
 2. The ~1% box trip-wire: fraction (~160,000 B) or sensitivity (~64,000 B)? Still yours; carried.
 3. Was the HALT gate meant as an operator checkpoint? The snapshot was in ~/Downloads, not
    docs/memory/; I placed it (byte-identical, original untouched) rather than halting. Flagged.
NEXT: DIGEST.md is now the FIRST pointer in §0 THE MAP and it is stale in a way that bites - it
    still carries "HALT unless it ends C:\Naiad", a gate that halts unconditionally on this host,
    and quotes the retired warn 50 / refuse 80. NOT edited: it is HERMES-only per §4.2 and a
    builder re-authoring the coordination lane's output is the HELIOS tripwire. Owner: HERMES,
    escalating to ATHENA.
METRICS: operator actions this session = 1 (Sync now) · rules censused = 422 · rules lost = 0 ·
    rules the census recovered = 8 · defects I introduced and it caught = 1 · narratives extracted
    = 27 · tokens minted = 9 · compression edits applied = 46 · fixtures added = 4 (F-CONV-1..4)
=== END STATUS ===
