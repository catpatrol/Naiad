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
