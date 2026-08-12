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
