# DIGEST — the index of what exists in Project Naiad

Generated **2026-08-05T23:40Z** by HERMES · Manifest read: `2026-08-05T16:50:42Z` · Repo HEAD (live): `aa65905`

---

## 1 · How to use this

- The project knowledge box holds **`LEDGER.md` and `exchange/` only** (operator ruling 2026-08-06, CONVENTIONS §3.2). Everything else in the repo is *not* automatically visible to APOLLO, ARGUS or ATHENA.
- **If you need a file listed below, ask the operator to drag it into your chat.** A dragged file lives in that one conversation and never enters the box.
- It costs nothing permanent. That is the whole point — **you cannot request a file you do not know exists**, so this index is what makes "ask for what you need" work instead of "tick everything just in case".

> ⚠ **CONVENTIONS contradicts itself on this, and 88 percentage points of box budget hang on it.** §3.2 says the tick set is `LEDGER.md` + `exchange/` only. §4.3 says *"the sync reaches `exchange/`, `docs/`, `prompts/`"* (measured 2026-08-03, never revised). See §7 Finding H-1. **Do not treat the box as safe until the operator rules.**

---

## 2 · The box budget — measured 2026-08-05

Box capacity taken as **6,390,000 bytes**. *(Derived, not given: the primer's 4,024,198 B = "about 63%" implies 6.388e6; its 770 KB = "about 12%" implies 6.42e6.)*

**Scenario A — tick set is `LEDGER.md` + `exchange/` (CONVENTIONS §3.2):**

| item | bytes | % of box | files |
|---|---:|---:|---:|
| `LEDGER.md` | 255,011 | 3.99% | 1 |
| `exchange/` total | 1,098,162 | 17.19% | 74 |
| — prose (`.md`/`.txt`) | 872,848 | 13.66% | 68 |
| — data (all other) | 225,314 | 3.53% | 6 |
| **TOTAL** | **1,353,173** | **21.2%** | **75** |

**Scenario B — sync also reaches `docs/` + `prompts/` (CONVENTIONS §4.3):**

| item | bytes | % of box | files |
|---|---:|---:|---:|
| Scenario A subtotal | 1,353,173 | 21.2% | 75 |
| `docs/` (tracked) | 5,432,504 | 85.02% | 70 |
| `prompts/` (tracked) | 225,748 | 3.53% | 15 |
| **TOTAL** | **7,011,425** | **109.7% — OVERFLOWED** | **160** |

**Every file in `exchange/` over 1% of box (63,900 B) — there is exactly one:**

| file | bytes | % box | type | owner |
|---|---:|---:|---|---|
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% | **data** | APOLLO |

`exchange/` folder split: `reports/` 840,222 B (13.15%) · `status/` 113,532 B (1.78%) · `status/daily/` 107,048 B (1.68%) · `queue/` 23,724 B (0.37%) · root 13,075 B (0.20%) · `drops/` 561 B (0.01%).

**The law holds and is worth restating:** 68 prose files = 13.7% of the box. Two capture JSONs outside `exchange/` = 63.0%. **Documents are cheap. Data is not. Write more reports, never fewer.**

---

## 3 · By lane

### APOLLO — SSv12, census, Tier-C, the Pine indicator
- Ledger · `exchange/status/LEDGER_APOLLO.md` — **newest entry 2026-07-27, 9 days stale**, 2 entries. Marked stale at source by its own provenance note.
- `exchange/reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` (34,971 B) — WF1 winner forensics
- `exchange/reports/WF1_tables.md` (29,660 B) · `exchange/reports/WF1_discriminants.json` (113,355 B — **data, see §7 H-3**)
- Queue item · `exchange/queue/2026-08-03_WF1_winner_forensics_APOLLO.md` — RATIFIED
- Reference: `docs/memory/claude_project_memory_2026-08-03.md` Entries 19 & 25 (SS interview rulings; infra inventory) — *not in box under Scenario A; request it*

### ARGUS — analytics toolkit, daily brief, volume/VWAP instruments
- Ledger · `exchange/status/LEDGER_ARGUS.md` — **newest entry 2026-07-27, 9 days stale**, 2 entries. Stale at source. **The lane is not silent — its ledger is.** ARGUS has filed 20+ artifacts since.
- `exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` (10,714 B) — most recent
- `exchange/reports/SESSION_SUMMARY_ARGUS_2026-08-06_C6.md` (9,368 B)
- `exchange/reports/INTERFACE_2026-08-06_C6.md` (48,885 B) — the interface snapshot
- Outside the box, in `docs/history/argus/` — **request individually**: `BUILDERS_REPORT_ARGUS_2026-08-06_C6.md` (14,069 B) · `BUILDERS_REPORT_ARGUS_2026-08-06_C5.md` (16,906 B) · `BUILDERS_REPORT_ARGUS_2026-08-05_C4.md` (30,060 B) · `BRIEF2_CALIBRATION_2026-08-05.json` (3,769 B) · `INTERFACE_2026-08-06.md` (47,469 B) · plus 8 earlier BUILDERS_REPORTs from 08-02/08-03
- Charter · `exchange/status/CONVENTIONS.md` §5.1

### ATHENA — resilience, backups, integrity, workflow, the conventions
- Ledger · `exchange/status/LEDGER_ATHENA.md` — **newest 2026-08-05**, 8 entries. Freshest ledger in the project.
- **`exchange/status/CONVENTIONS.md` (41,564 B) — authoritative for all six lanes. Read it first.**
- `exchange/status/CADENCE.md` (6,190 B) · `RETENTION.md` (2,487 B) · `SECOND_ACCOUNT.md` (1,891 B) · `HEARTBEAT.md` (198 B)
- `exchange/reports/2026-08-04_ATHENA_handoff_orphan-data-files.md` (3,180 B) · `2026-08-04_ATHENA_s3-journal-restore.md` (2,588 B)
- `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-WORKSTREAM.md` (8,859 B) · `…MEMORY-SCOPING.md` (9,514 B)
- `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` (2,876 B) — probe labels B1–B6

### DIONYSUS — independent critique
- Ledger · `exchange/status/LEDGER_DIONYSUS.md` — newest 2026-08-02, **3 days stale**, 2 entries
- `exchange/reports/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` (6,705 B)
- Two open inbox items to APOLLO — see §4
- Queue item · `exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` — **no RATIFIED line, see §5**

### HEPHAESTUS — the builder
- Ledger · `exchange/status/LEDGER_HEPHAESTUS.md` — newest 2026-08-02, **3 days stale**, 2 entries. **Also not silent — 19 reports filed since.**
- Most recent · `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SIDECARS-AND-LANE-CLOSE.md` (18,014 B)
- `…2026-08-04_EXCHANGE-GUARD-ENFORCEMENT.md` (22,812 B) · `…_ARCHIVE-VERIFY-AND-QUEUE-002.md` (21,444 B) · `…_TC5-OFFSITE-AND-PHASE-MODE-READ.md` (35,526 B) · `…_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md` (19,934 B) · `…_ANALYTICS-ARCHIVES-AND-EXCHANGE-SIZING.md` (23,480 B) · `…_SEQ8.md` (33,748 B)
- Earlier: 7 `2026-08-02_HEPHAESTUS_report_*.md` and 3 `2026-08-03` reports, all in `exchange/reports/`

### HERMES — this lane
- Ledger · `exchange/status/LEDGER_HERMES.md` — newest 2026-08-04, 3 entries
- This file · `exchange/DIGEST.md`
- `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` — this run

---

## 4 · Inbox — `NOTE_<FROM>_to_<TO>_*`

| note | to | bytes | referenced elsewhere? | reads as |
|---|---|---:|---|---|
| `reports/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | APOLLO | 18,065 | 2 files (DIONYSUS range-scoping, ARGUS boxhygiene) | picked up **downstream**, no APOLLO reply on file |
| `reports/NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md` | ATHENA | 4,375 | 1 file (ARGUS boxhygiene) | **no ATHENA reply on file** |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | APOLLO | 7,275 | 2 files (HEPHAESTUS SEQ8, DIONYSUS SEQ8-findings) | acted on **by the builder**, not by APOLLO |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` | APOLLO | 5,645 | 1 file (HEPHAESTUS conventions-merge) | acted on **by the builder**, not by APOLLO |

**All four are addressed to a lane whose ledger has not moved since before the note arrived.** Three of four are to APOLLO, whose ledger is 9 days stale. A reference by a third party is not the recipient acting. **Nothing moved — these are APOLLO's and ATHENA's files, not mine.**

---

## 5 · The queue

| # | file | drafted by | RATIFIED | deliverable | fixtures | verdict criteria | "what this is not" |
|---|---|---|---|---|---|---|---|
| 001 | `queue/001_condensed-project-history.md` | ATHENA | **PENDING** | yes | F-H1..H6 | yes | yes |
| 002 | `queue/002_backup-and-publish-guards.md` | ATHENA | **yes** — operator 2026-08-04, G1-a/G5-a | yes | yes | **NOT FOUND** | yes |
| — | `queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | APOLLO | **yes** — operator 2026-08-03, "forensics" | **NOT FOUND** | yes | **NOT FOUND** | **NOT FOUND** |
| — | `queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | DIONYSUS | **NO STAMP AT ALL** | yes | yes | **NOT FOUND** | yes |

Three defects, **reported not fixed** (§7 H-4/H-5). Manifest reports `queue_open: 1`; four non-README items are present — the counter appears to track only `NNN_`-numbered items, so the two date-named ones are invisible to it.

---

## 6 · Staleness

| artifact | last changed | age at generation |
|---|---|---|
| `status/CONVENTIONS.md` | 2026-08-05 20:30 | ~3 h |
| `status/MANIFEST.json` | 2026-08-05 16:50 | ~7 h — **but its HEAD `c9e16e8` is behind live `aa65905`** |
| `status/HEARTBEAT.md` | 2026-08-05 13:58 | ~10 h · `overdue: 4` |
| `status/CADENCE.md` | 2026-08-04 03:34 | ~1.8 d |
| `status/RETENTION.md` | 2026-08-04 02:19 | ~1.8 d |
| `status/SECOND_ACCOUNT.md` | 2026-08-05 00:04 | ~23 h |
| Ledgers | APOLLO 07-27 · ARGUS 07-27 · DIONYSUS 08-02 · HEPHAESTUS 08-02 · HERMES 08-04 · ATHENA 08-05 | |

---

## 7 · Findings this cycle

**H-1 · CONVENTIONS contradicts itself about what is in the box. This is the one that matters.**
§3.2 (2026-08-06 ruling): *"Standing tick set: `LEDGER.md` and `exchange/` ONLY."* §4.3 (measured 2026-08-03, never revised): *"the sync reaches `exchange/`, `docs/`, `prompts/`."* Under the first the box is at **21.2%**; under the second **109.7% — overflowed**. This is a live instance of the failure CONVENTIONS names in its own opening rule: *"A correction REPLACES the assertion it corrects… rewrite every place that asserts it."* §3.2 changed the fact; §4.3 still states the old one, and a reader arriving at §4.3 believes it. **Flagged, not resolved — CONVENTIONS wins over the primer, and only the operator can say which of its two clauses is live.** `[verified]`

**H-2 · The two captures that caused the last overflow are still tracked and on origin.**
`docs/history/argus/CAPTURE_2026-08-05_post_ny.json` (1,973,883 B, 30.89%) and `CAPTURE_CERTIFIED_2026-08-05_post_ny.json` (2,050,315 B, 32.09%) = **4,024,198 B, 62.98%** — the exact figure the primer quotes. Both verified TRACKED and present on `origin/v12-v1-census`. They are outside `exchange/`, so under §3.2 they cost nothing; under §4.3 they alone are ~63% of the box. Their disposition is decided entirely by H-1. `[verified]`

**H-3 · The pointer discipline was applied to the symptom, not the process.**
`docs/history/argus/CAPTURE_2026-08-03_post_ny.json.pointer.md` is an exemplary stub — 1,060 B, naming path, sha256, bytes, box cost, and the tracked-and-pushed twin. It replaced a 1,879,133 B file on 2026-08-04. **Two days later the same lane wrote two larger captures into a synced tree with no pointer.** The instance was fixed; the thing that generates instances was not. `[verified]`

**H-4 · Three of four queue items are missing verdict criteria**, and `2026-08-03_WF1_winner_forensics_APOLLO.md` is missing named deliverables and a "what this phase is not" as well. Only item 001 is complete against the CONVENTIONS standard — and 001 is the one still unratified. `[verified]`

**H-5 · `queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` carries no RATIFIED line at all.** Not "PENDING" — absent. Per `queue/README.md` rule 5 it is a request, not work. Its content has nonetheless been acted on: `BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md` exists. **Work appears to have run ahead of the stamp.** Reported for the operator; I do not adjudicate. `[verified]`

**H-6 · CONVENTIONS §8 carries a mangled edit.** After the "Triggers armed" paragraph an orphan fragment survives: `08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.` — the tail of a superseded sentence whose head was rewritten. Cosmetic, but it is in the file that binds all six lanes, and it is the same class of half-applied correction as H-1. `[verified]`

**H-7 · Manifest HEAD is behind live HEAD again.** Manifest `c9e16e8` (2026-08-05T16:50:42Z) vs live `aa65905`. Same condition as my 2026-08-04 run: clock-fresh, content-stale. A lane reading the manifest for repo state is reading a superseded commit. `[verified]`

**H-8 · Two lanes look silent and are not.** ARGUS's ledger is 9 days old against 20+ filed artifacts; HEPHAESTUS's is 3 days old against 19 reports. Staleness stamps measure the ledger, not the lane — treat them as "this lane's status layer is unreliable", not "this lane is idle." `[verified]`

**H-9 · `drops/` is empty.** README only. No filing or G-11 naming owed. `[verified]`

---

## 8 · Pointers

Rules · `exchange/status/CONVENTIONS.md` — **authoritative, read first**
Ground truth · `exchange/status/MANIFEST.json` · `HEARTBEAT.md` · `status/daily/`
Lane state · `exchange/status/LEDGER_{APOLLO,ARGUS,ATHENA,DIONYSUS,HEPHAESTUS,HERMES}.md`
Cadence · `exchange/status/CADENCE.md` · Retention · `RETENTION.md` · `SECOND_ACCOUNT.md`
Queue · `exchange/queue/` (4 items + README)
This run · `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md`

*This file is an index. Where it points, the artifact it points at is authoritative.*
