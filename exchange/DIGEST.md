# DIGEST — the index of what exists in Project Naiad

Generated **2026-08-12T01:10Z** by HERMES · Manifest read `2026-08-11T19:37:35Z` · Live HEAD `04d05ab`

---

## 1 · How to use this

- The box holds **`LEDGER.md` and `exchange/` only** (operator, 2026-08-06; CONVENTIONS §3.2, §4.3). Nothing else is in it.
- **Need a file listed below? Ask the operator to drag it in.** It lives in that one conversation, costs nothing permanent.
- You cannot request what you don't know exists. That is what this index is for.
- **Bulk data lives on `D:/Naiad`, which I cannot see.** D: rows below are `[handoff]` — read from repo-side witnesses (`POINTER.md`, tracked `.sha256` sidecars, build-report disposition tables), never asserted as verified.

---

## 2 · Budget — both figures, measured 2026-08-12

Against 6,390,000 B.

| reading | bytes | % | state |
|---|---:|---:|---|
| **Guard-metered** (`exchange/` only — what `publish` enforces) | 1,745,187 | **27.31%** | ⚠ **WARNING** (warn 25 / refuse 40) |
| **Tick-set truth** (`exchange/` + `LEDGER.md`) | 2,000,198 | **31.30%** | the number that matters |
| metering gap | 255,011 | 3.99 pts | `LEDGER.md`, invisible to the guard |

99 files. Prose 1,186,879 B / 18.57% (89 files). Data 558,308 B / 8.74% (10 files).

**Files over 1% — both are data, both in `reports/`:**

| file | bytes | % box | owner |
|---|---:|---:|---|
| `exchange/reports/MC1_results.json` | 261,072 | **4.09%** | APOLLO |
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% | APOLLO |

Folders: `reports/` 1,376,681 (21.54%) · `status/daily/` 183,665 (2.87%) · `status/` 126,860 (1.99%) · `queue/` 42,084 (0.66%) · root 15,336 (0.24%) · `drops/` 561 (0.01%).

**Rotation candidates (queue 003, >30 days): ZERO.** Cutoff 2026-07-13. No `exchange/reports/*.md` is older by mtime or by filename date — the oldest are 2026-07-28, 15 days inside the window. **003's tooling is built and has nothing to move yet.**

---

## 3 · By lane

### APOLLO — SSv12 study, census, Tier-C, Pine indicator
`status/LEDGER_APOLLO.md` — newest **2026-08-10**, 2 entries. The only lane whose ledger leads its artifacts.
`reports/BUILD_APOLLO_2026-08-06_MC1.md` (38,482) · `reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md` (31,822) · `reports/BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md` (34,971) · `reports/WF1_tables.md` (29,660)
Data: `reports/MC1_results.json` (261,072 — **4.09%, see §5 F-2**) · `reports/WF1_discriminants.json` (113,355)
Queue: `queue/2026-08-06_MC1_may26_program_APOLLO.md` · `queue/2026-08-03_WF1_winner_forensics_APOLLO.md`

### ARGUS — analytics toolkit, daily brief, volume/VWAP
`status/LEDGER_ARGUS.md` — newest **2026-07-27**, 1 entry. **Trails its own artifacts by 10 days. Stalest ledger in the project.**
`reports/ARGUS_PANTHEON_REPORT_2026-08-06.md` (23,454) · `reports/INTERFACE_2026-08-06_C6.md` (48,885) · `reports/SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` (10,714) · `…_C6.md` (9,368)
Not in the box — request individually from `docs/history/argus/`: the 08-05/08-06 `BUILDERS_REPORT_ARGUS_*` set, `INTERFACE_2026-08-06.md`, `BRIEF2_CALIBRATION_*.json`, the two `CAPTURE_*` files
Charter: CONVENTIONS §5.1

### ATHENA — infrastructure, backups, integrity, workflow, the rules
`status/LEDGER_ATHENA.md` — newest **2026-08-05**, 7 entries. Trails by 6 days.
**`status/CONVENTIONS.md` (50,218 B, 2026-08-11) — authoritative, read first.** Now opens with THE FIRST RULE and a FIND IT FAST index.
`status/CADENCE.md` (6,190, 08-04) · `RETENTION.md` (2,656, 08-09) · `SECOND_ACCOUNT.md` (1,891, 08-05) · `HEARTBEAT.md` (198, **08-09 — see §5 F-1**)
`reports/STATUS_ATHENA_2026-08-11_LANE-CLOSEOUT.md` (8,744) · `…_LANE-CLOSE.md` (5,259) · `status/2026-08-11_DELTA_archive-relocation-memory-redraft.md`

### DIONYSUS — independent critique
`status/LEDGER_DIONYSUS.md` — newest **2026-08-02**, 1 entry. Trails by 2 days.
`reports/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` · two open notes to APOLLO (§4)
Queue: `queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` — **stamped 2026-08-06** ("stamp seq8"); verdict criteria still owed `[handoff, primer v4]`

### HEPHAESTUS — the builder
`status/LEDGER_HEPHAESTUS.md` — newest **2026-08-02**, 1 entry, against **26 filed reports**. **Trails by 9 days — the widest gap in the project.**
2026-08-11: `_QUEUE-002.md` (22,065) · `_BULK-RELOCATION-SEQ8-UNARCHIVED.md` (20,685) · `_QUEUE-003.md` (17,335) · `_R1-R2-R3.md` (17,277) · `_QUEUE-003-RATIFIED.md` (10,749) · `_QUEUE-003-FILED.md` (6,662)
2026-08-06: `_ARCHIVE-RELOCATION-D.md` (22,227) · plus 18 earlier reports 08-02→08-04
Built this cycle: `scripts/rotate_reports.py` (13,423 B, commit `f3efb0f`) — **queue 003 D-1 exists; the primer says 003 is unbuilt (§5 F-4)**

### HERMES — this lane
`status/LEDGER_HERMES.md` — newest 2026-08-04, 2 entries. Trails by 7 days; **this cycle's entry is owed and is in my report, not yet in the ledger.**
`exchange/DIGEST.md` (this file) · `reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` · `reports/PRIMER_HERMES_2026-08-11_v4.md` (6,991)

---

## 4 · Inbox — six notes, **zero acknowledged**

Acted = the recipient's own ledger carries an entry referencing it. A third-party mention is not the recipient acting.

| note | to | bytes | acted? |
|---|---|---:|---|
| `reports/NOTE_ATHENA_to_APOLLO_2026-08-11_data-residency.md` | APOLLO | 1,747 | no |
| `reports/NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md` | ARGUS | 4,028 | no |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` | APOLLO | 5,645 | no |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | APOLLO | 7,275 | no |
| `reports/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | APOLLO | 18,065 | no — **9 days** |
| `reports/NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md` | ATHENA | 4,375 | no — **9 days** |

**Correction to primer §4:** both 08-11 data-residency notes are already filed to the bus, not operator-held. Four of six are addressed to APOLLO. **Nothing moved — a note addressed to a lane is that lane's file.**

---

## 5 · Queue

| item | stamp | verdict criteria | execution |
|---|---|---|---|
| `queue/001_condensed-project-history.md` | ratified 2026-08-06 "ratify 001" | yes | **no execution artifact found** |
| `queue/002_backup-and-publish-guards.md` | ratified 2026-08-04, amended ×2 | yes | **EXECUTED — ACCEPT, 10/10, `c32ffa5`** `[handoff]` |
| `queue/003_report-rotation-and-provenance.md` | ratified 2026-08-11 "ratify 003" | yes | **D-1 BUILT** (`scripts/rotate_reports.py`, `f3efb0f`); no `ROTATION_LOG.md`, no `docs/history/reports/` |
| `queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | ratified 2026-08-03 "forensics" | **MISSING** | executed 2026-08-04 |
| `queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md` | ratified 2026-08-06 "stamp seq8" | owed `[handoff]` | executed |
| `queue/2026-08-06_MC1_may26_program_APOLLO.md` | ratified 2026-08-06 + amendment | **MISSING** | executed — `BUILD_APOLLO_2026-08-06_MC1.md` |

**`MANIFEST.json` reports `queue_open: 0` against six items.** Last cycle it reported 1 against four. The counter is worse, not better (§6 F-3).

---

## 6 · Findings

**F-1 · The daily routine has been dead for three days and the bus looks alive. This is the one that matters.** `[verified]`
`DAILY_2026-08-09.md`: the **required** manifest job exited 1 — *"HALT: F-M3, F-M4 failed; no partial adoption"*. F-M3 is the two-build determinism fixture; F-M4 the read-only porcelain audit. The run stopped there; brief, brief2_capture and brief2_panel never attempted. Newest `DAILY_*.md` is 2026-08-09; today is 2026-08-12. **No routine output for 08-10, 08-11, 08-12.** `HEARTBEAT.md` still reads the 08-09 failure — `exit: 1`.
Why nobody noticed: queue 002 made **publish** refresh `MANIFEST.json`, and eleven publishes ran on 08-11. The manifest is 6 h old and looks healthy. **A fix intended to close manifest staleness is now masking the death of the job that produces it.** The freshness signal no longer proves the routine ran.

**F-2 · `MC1_results.json` is the new largest file on the bus — 261,072 B, 4.09%, data.** `[verified]`
Unnamed in primer v4. Proposed home `research_outputs/mc1/`, replaced by a ~1 KB pointer stub on the exemplary pattern of `docs/history/argus/CAPTURE_2026-08-03_post_ny.json.pointer.md`. With `WF1_discriminants.json` (113,355) also unmoved since I flagged it 2026-08-05, the two are **374,427 B = 5.86%** of the box and **67% of all data in `exchange/`**. Moving both drops the guard from 27.31% to **21.5% — out of WARNING.** Propose only; nothing moved.

**F-3 · `queue_open` now reports 0 against six items.** `[verified]`
Last cycle: 1 against four. The counter appears to match a narrower pattern than the queue actually uses. Anyone trusting it sees an empty queue. Reported 2026-08-05, unresolved, degraded.

**F-4 · Queue 003 is partly built; the primer says it is not.** `[verified]`
`scripts/rotate_reports.py` (13,423 B) is committed at `f3efb0f` — *"queue 003 D-1"*. Absent: `exchange/status/ROTATION_LOG.md` and `docs/history/reports/`. Consistent with D-1 done and the rest pending — and with §2's zero rotation candidates, **nothing is waiting on it.**

**F-5 · Five of six lane ledgers trail their own filed reports.** `[verified]`

| lane | ledger newest | entries | newest artifact | artifacts | gap |
|---|---|---:|---|---:|---|
| HEPHAESTUS | 2026-08-02 | 1 | 2026-08-11 | 26 | **9 d** |
| ARGUS | 2026-07-27 | 1 | 2026-08-06 | 5 | **10 d** |
| HERMES | 2026-08-04 | 2 | 2026-08-11 | 2 | 7 d |
| ATHENA | 2026-08-05 | 7 | 2026-08-11 | 9 | 6 d |
| DIONYSUS | 2026-08-02 | 1 | 2026-08-04 | 4 | 2 d |
| APOLLO | 2026-08-10 | 2 | 2026-08-06 | 2 | — leads |

Three lanes hold exactly one entry — their founding seed. **The per-lane ledger layer is not being maintained; work flows through `reports/` instead.** Read a staleness stamp as "this lane's status layer is unreliable," never "this lane is idle." HEPHAESTUS filed 26 reports against one ledger entry.

**F-6 · Manifest HEAD still trails live HEAD — third consecutive cycle.** `[verified]`
Manifest `11c3fb83` (2026-08-11T19:37Z) vs live `04d05ab`; **10 commits behind**, nine of them `exchange: auto-publish`. Queue 002 closed staleness *for the publish path* — the manifest refreshes when publish runs, then every commit after the last publish leaves it behind again. Calling the class closed is one step too strong: it is closed at publish time, open between publishes.

**F-7 · CONVENTIONS §8 still carries the mangled edit — second cycle, unfixed.** `[verified]`
Line 764, an orphan fragment: `08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.` — the tail of a rewritten sentence. Cosmetic, in the file binding all six lanes. **My H-1 from 2026-08-05 was accepted and corrected properly in §4.3; this one was not carried across.**

**F-8 · Backup posture, from the last routine that ran** `[handoff, DAILY_2026-08-09]`
`operator-exports` folder missing at `G:\My Drive\naiad-backups` · 3 of 3 operator preference blocks still uncaptured · **OneDrive.exe not running** — the repo is inside the OneDrive tree and is not syncing · second Google Drive upload outstanding (newest workflow archive 2026-08-09 vs last manual upload 2026-08-05). All four unverifiable by me and three days stale.

**F-9 · `drops/` empty.** README only. No filing owed. `[verified]`

---

## 7 · Staleness

| artifact | last changed | age |
|---|---|---|
| `status/CONVENTIONS.md` | 2026-08-11 21:09 | ~4 h |
| `status/MANIFEST.json` | 2026-08-11 19:37 | ~6 h — **HEAD 10 commits behind** |
| `status/RETENTION.md` · `HEARTBEAT.md` | 2026-08-09 | **3 d — routine dead since** |
| `status/CADENCE.md` | 2026-08-04 | 8 d |
| `status/SECOND_ACCOUNT.md` | 2026-08-05 | 7 d |
| Ledgers | APOLLO 08-10 · ATHENA 08-05 · HERMES 08-04 · DIONYSUS 08-02 · HEPHAESTUS 08-02 · ARGUS 07-27 | |

**Cadence:** the HERMES scheduled run is still the last unarmed line in `CADENCE.md`. Recommend **~06:30**, so the 07:00 routine's auto-publish carries my output the same morning — I have no egress on a schedule. **Caveat sharpened by F-1: that arrangement depends on a routine that has not completed since 2026-08-09.** Fix the routine first; arming me behind a dead publisher buys nothing.

---

## 8 · Pointers

Rules · `exchange/status/CONVENTIONS.md` — authoritative, read first (THE FIRST RULE · FIND IT FAST)
Ground truth · `exchange/status/MANIFEST.json` · `HEARTBEAT.md` · `status/daily/`
Lanes · `exchange/status/LEDGER_{APOLLO,ARGUS,ATHENA,DIONYSUS,HEPHAESTUS,HERMES}.md`
Cadence · `CADENCE.md` · Retention · `RETENTION.md` · `SECOND_ACCOUNT.md`
Queue · `exchange/queue/` — 6 items + README
D: witnesses `[handoff]` · `research_outputs/_archive/POINTER.md` + 9 tracked `.sha256` sidecars
This cycle · `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md`

*An index. Where it points, the artifact is authoritative.*
