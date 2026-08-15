# DIGEST — the index of what exists in Project Naiad

Generated **2026-08-12T11:40Z** by HERMES from **`C:\Naiad`** · Manifest read `2026-08-12T10:59:07Z` · Live HEAD `cc10d8f`

**Supersedes the 2026-08-12T01:10Z edition**, which was written from the now-abandoned OneDrive clone.

---

## 1 · How to use this

- The box holds **`LEDGER.md` and `exchange/` only**. Nothing else is in it.
- **Need a file listed below? Ask the operator to drag it in.** It lives in that one conversation and costs nothing permanent.
- You cannot request what you do not know exists. That is what this index is for.
- **Bulk data lives on `D:\Naiad`, which I cannot see.** D: rows are `[handoff]` — read from repo-side witnesses (`POINTER.md`, tracked `.sha256` sidecars, build-report disposition tables), never asserted as verified.

> ⚠ **TWO CLONES EXIST AND THE DEAD ONE LIES.** The live tree is `C:\Naiad`. The old
> `…OneDrive/Desktop/Midas-Claude Code Resources/naiad` tree is intact and awaiting Phase B.
> **Its remote-tracking ref is stale too, so `git status` there reports "clean, up to date" while
> sitting 4 commits behind.** Nothing inside that tree can tell you it is dead. Use the two-sided
> gate on every session: **HALT if the path contains `OneDrive`; HALT unless it ends `C:\Naiad`.**

---

## 2 · Budget — measured 2026-08-15T21:05Z, against 16,000,000 B

| reading | bytes | % | state |
|---|---:|---:|---|
| **Guard-metered** (`exchange/` — what `publish` enforces) | 2,576,034 | **16.10%** | **OK** (warn 50 / refuse 80) |
| **Tick-set truth** (`exchange/` + `LEDGER.md`) | 2,831,045 | **17.69%** | the real occupancy |
| metering gap | 255,011 | 1.59 pts | `LEDGER.md`, invisible to the guard |

141 files, **as of the measurement stamp above** — documents written later in the same session
(this cycle: the LEDGER_APOLLO 15e entry, ~6 KB) land after the reading, per the standing rule that
a file cannot carry its own final size. The guard's own figure at publish is authoritative.

**Prose 2,366,564 B / 14.79% (130 files) · Data 209,470 B / 1.31% (11 files).**
**No file exceeds 1% of the box** — though note 1% is now ~160,000 B rather than ~63,900 B, so this
statement is weaker than the same sentence was a cycle ago. See CONVENTIONS §4.2, where the
loosening is named.

Folders: `reports/` 1,915,772 (11.97%, 98 files) · `status/` 359,525 (2.25%) · `status/daily/` 198,774 (1.24%) · `queue/` 78,804 (0.49%) · root 22,598 (0.14%) · `drops/` 561 (0.00%).

### The refuse-before-rotation conflict is RESOLVED

```
headroom to REFUSE (80%)   10,223,966 B    63.9 points
```

**The box was raised 6.39 MB → 16 MB on 2026-08-15 by operator ruling `["box", VETO]`** (warn
25→50%, refuse 40→80%), after the guard did exactly what it was built to do: it REFUSED a paste at
40.2% whose artifacts were already built and local. The ruling is explicit that **the ceiling rises
and the housekeeping stays** — queue 003 rotation remains scheduled at `AGE_DAYS = 30`, next
eligible ~2026-08-28, and `rotate_reports.py` was not touched.

**The prior reading of this section — "⚠ the bus will refuse before rotation is allowed to fire",
"two ratified mechanisms are in arithmetic conflict" — is now VOID and is recorded here as
superseded rather than deleted.** It was correct when written on 2026-08-12: at 27.70% of a 6.39 MB
box with 785,732 B of headroom and 794,687 B added in a day, the arithmetic really did collide, and
saying so is what got the box raised. The conflict was dissolved by moving the ceiling, not by the
lanes writing less.

**And the standing law has inverted.** Data is now 3.05% of the box, down from 8.74%: the two pointer stubs worked. In the same ten hours prose grew ~389 KB and the bus got *bigger*. Per unit documents are still cheap; at twelve builder reports a day they are the binding constraint. `reports/` holds 77 files.

---

## 3 · Where everything lives `[handoff — ATHENA 2026-08-12]`

| what | location |
|---|---|
| **Working clone (live)** | **`C:\Naiad`** — GitHub `catpatrol/Naiad`, branch `v12-v1-census` |
| Old clone (abandoned, awaiting Phase B) | `…OneDrive\Desktop\Midas-Claude Code Resources\naiad` — **do not use** |
| Python interpreter | `C:\venvs\naiad\Scripts\python.exe` — did not move |
| Raw price estate (irreplaceable) | `C:\Users\luisf\AppData\Local\naiad\data_cache` |
| **Bulk data** — phase archives, `seq8`, `seq8_run2`, mirrors | **`D:\Naiad\…`** mirroring repo paths |
| 9 phase archives (1,043.6 MB, permanent evidence) | `D:\Naiad\research_outputs\_archive` + tracked `.sha256` sidecars |
| **Backups** — estate, workflow | **`D:\naiad-backups`** + Google Drive (Computers) |
| `census` + `mc1` substrates | local + `D:\Naiad\…` (37 files / 381.1 MB) |
| `MC1_results.json` | `research_outputs/mc1/` + pointer stub on the bus |
| `WF1_discriminants.json` | `research_outputs/wf1/` + pointer stub |
| Published analytics interface | `exchange/status/INTERFACE_PUBLISHED.md` — fixture F-AN-15 enforces byte-identity |
| Atlases · memory snapshots · old primers | `docs/history/atlases/` · `docs/memory/` · `docs/primers/` |

**Scheduled tasks** — all three repointed to `Start In: C:\Naiad`, 18/18 XML assertions pass. Next runs **13-Aug 07:00**, **16-Aug 08:00**, **16-Aug 08:30**. **The HERMES run still does not exist.**

**Five residuals, each owned** `[handoff]`: **R-1** a fourth identity gate in `prompts/PC1_…Contract.md` still asserts OneDrive — completed contract, would halt if re-run (ATHENA) · **R-2** old tree's stale remote ref (operator, Phase B) · **R-3** 28 of 138 permission rules name the old path — prompts, not failures (operator) · **R-4** two files resurrected into `reports/` by module import, +12,850 B, byte-identical twins in `docs/history/argus/` (needs delete-authorised tidy) · **R-5** O-5 four-deep on one calendar day, so genuinely distinct older generations read as out-of-rule (ATHENA).

---

## 4 · By lane

### APOLLO — SSv12 study, census, Tier-C, Pine indicator · **GREENLIT**
`status/LEDGER_APOLLO.md` — newest **2026-08-10**, 2 entries · artifacts to 08-12 (2 d gap)
`reports/APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md` (13,476) · `reports/BUILD_APOLLO_2026-08-06_MC1.md` (38,482) · `reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md` (31,822) · `reports/WF1_tables.md`
Data off-bus: `reports/MC1_results.json.pointer.md` · `reports/WF1_discriminants.json.pointer.md`
Queue: `queue/2026-08-06_MC1_may26_program_APOLLO.md` · `queue/2026-08-03_WF1_winner_forensics_APOLLO.md`
Session-start sources unchanged. Census-2 is the first contract native to `C:\Naiad` + `D:\Naiad`.

### ARGUS — analytics toolkit, daily brief, volume/VWAP
`status/LEDGER_ARGUS.md` — newest **2026-08-11**, 2 entries — **current** *(corrected: see §6 F-5)*
`reports/BUILDERS_REPORT_ARGUS_2026-08-11_MAINT.md` (30,800) · `reports/SESSION_SUMMARY_ARGUS_2026-08-06_BOXHYGIENE.md` · `…_C6.md`
`status/INTERFACE_PUBLISHED.md` (48,885) is the bus copy; **F-AN-15 fails the suite on drift**
R-4's two resurrected files are ARGUS-origin. Charter: CONVENTIONS §5.1

### ATHENA — infrastructure, backups, integrity, workflow, the rules
`status/LEDGER_ATHENA.md` — newest **2026-08-12**, 7 entries — **leads its artifacts**
**`status/CONVENTIONS.md` (53,679 B, 08-12) — authoritative, read first.** THE FIRST RULE + FIND IT FAST index
`status/CADENCE.md` (7,503, 08-12) · `RETENTION.md` (2,984, 08-12) · `SECOND_ACCOUNT.md` (2,941, 08-12) · `HEARTBEAT.md` (198, 08-12)
`reports/NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` (9,986) — **the move's record of truth** · `…_CROSS-LANE-RECONCILIATION.md` (6,638, superseded on conflicts)

### DIONYSUS — independent critique
`status/LEDGER_DIONYSUS.md` — newest **2026-08-02**, 1 entry (founding seed) · artifacts to 08-04
`reports/SESSION_SUMMARY_DIONYSUS_2026-08-04_SEQ_rulings.md` · two open notes to APOLLO (§5)
Queue: `queue/2026-08-04_SEQ8_…_DIONYSUS.md` — ratified 2026-08-06; **verdict criteria still owed**
Same mount warning: re-attach at `C:\Naiad`.

### HEPHAESTUS — the builder
`status/LEDGER_HEPHAESTUS.md` — newest **2026-08-02**, **1 entry against 35 filed reports — a 10-day gap, the widest in the project**
2026-08-12: `_QUEUE-004-FILED-AND-D0A.md` (42,181) · `_PHASE-0.md` (35,498) · `_BACKUP-PATH-REROUTE.md` (31,324) · `_CLOSEOUT.md` (33,372) · `_QUEUE-004-HALT.md` (28,705) · `_QUEUE-004-PHASE-A.md` (26,876) · `_O1-O3-O4-TIDY.md` (23,178) · `_FILE-UNTRACKED.md` (16,407) · `_ONEDRIVE-CENSUS.md` (11,834)
Built: `scripts/rotate_reports.py` (queue 003 D-1)

### HERMES — this lane
`status/LEDGER_HERMES.md` — newest **2026-08-04**, 2 entries — **8-day gap; entries owed for the 08-05 and 08-12 cycles**
`exchange/DIGEST.md` (this file) · `reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` (14,277) · `reports/BUILDERS_REPORT_HERMES_2026-08-05_FIRST_RUN.md` (18,973) · `reports/PRIMER_HERMES_2026-08-11_v4.md`
Scheduled run: **still unarmed**, the last such line in `CADENCE.md`.

---

## 5 · Inbox

Acted = the recipient's own ledger references it. A third-party mention is not the recipient acting.

| note | to | bytes | acted? |
|---|---|---:|---|
| `reports/NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md` | ARGUS | 4,728 | ✅ **ACTED** — LEDGER_ARGUS 2026-08-11 |
| `reports/NOTE_ATHENA_to_APOLLO_2026-08-11_data-residency.md` | APOLLO | 1,747 | open |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` | APOLLO | 5,645 | open |
| `reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md` | APOLLO | 7,275 | open |
| `reports/NOTE_ARGUS_to_APOLLO_2026-08-03_census_candidates.md` | APOLLO | 18,065 | open — **9 days** |
| `reports/NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md` | ATHENA | 4,375 | open — **9 days** |

Broadcasts (no single recipient): `NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` · `…_CROSS-LANE-RECONCILIATION.md`
**Five of six addressed notes are open; four of those are APOLLO's.** Nothing moved — a note addressed to a lane is that lane's file.

---

## 6 · Queue — 7 items, all ratified

| item | stamp | verdict criteria | execution |
|---|---|---|---|
| `queue/001_condensed-project-history.md` | 2026-08-06 "ratify 001" | yes | **ratified, unbuilt** |
| `queue/002_backup-and-publish-guards.md` | 2026-08-04, amended ×2 | yes | EXECUTED — ACCEPT 10/10, `c32ffa5` `[handoff]` |
| `queue/003_report-rotation-and-provenance.md` | 2026-08-11 "ratify 003" | yes | **D-1 built** (`scripts/rotate_reports.py`); no `ROTATION_LOG.md`, no `docs/history/reports/` |
| `queue/004_move-clone-out-of-onedrive.md` | 2026-08-12 "ratify 004" | yes | **Phase A ACCEPTED; Phase B not run** `[handoff]` |
| `queue/2026-08-03_WF1_winner_forensics_APOLLO.md` | 2026-08-03 "forensics" | **missing** | executed 08-04 |
| `queue/2026-08-04_SEQ8_…_DIONYSUS.md` | 2026-08-06 "stamp seq8" | **owed by DIONYSUS** | executed |
| `queue/2026-08-06_MC1_may26_program_APOLLO.md` | 2026-08-06 + amendment | **missing** | executed |

**Zero unratified.** `MANIFEST.json` reports `queue_open: 3`; ATHENA's note states 2 ratified-unbuilt (001, 003). Counting 004 Phase B as open reconciles to 3 — but the counter has now given 0, 1 and 3 across three cycles against different denominators. **Do not trust it; count the folder.**

---

## 7 · Findings

**F-1 · The bus refuses before rotation can fire. — CLOSED 2026-08-15, by raising the ceiling rather than shortening the rotation.** `[verified, resolved]` — §2. As filed 2026-08-12: headroom 785,732 B; last 24 h added 794,687 B; rotation ineligible until 2026-08-27; the proposed remedy was to lower the 30-day threshold to ~10 days, making ~40 reports eligible at once. **It went the other way.** The finding was proved live on 2026-08-15 when publish REFUSED a paste at 40.2%, and the operator ruled `["box", VETO]`: box 6.39 → 16 MB, warn 25→50%, refuse 40→80%, **rotation untouched at `AGE_DAYS = 30`**. Headroom is now 10,223,966 B. The 30-day threshold was never shortened, so no report was rotated off the bus earlier than the ratified window — which is the outcome the redraft would have cost. Nothing owed to ATHENA here any more.

**F-2 · The abandoned clone reports itself healthy.** `[verified]` Old tree HEAD `75b7444`, its own `origin/v12-v1-census` also `75b7444`, so `git status -sb` prints *up to date* while 4 commits behind. **No signal inside that tree distinguishes it from the live one.** Both mounts were simultaneously attached to this session. Two-sided gate is mandatory until Phase B.

**F-3 · Prior findings closed.** The 2026-08-09 routine outage is **fixed** — `HEARTBEAT` reads `exit: 0` at 2026-08-12T11:03:40Z and `DAILY_2026-08-12.md` exists. Both pointer stubs are **built and on the bus**, crediting the finding by name; data fell from 8.74% to 3.05% of the box. `[verified]`

**F-4 · Manifest still trails live HEAD — fourth consecutive cycle.** `[verified]` `af861682` vs `cc10d8f2`. Queue 002 closed staleness at publish time; between publishes it reopens.

**F-5 · I published a false staleness reading last cycle, and here is the correction.** `[verified]` My ledger reader matched only `=== STATUS_X — date ===` and missed `## date — …`. On that basis I reported ARGUS as *"stalest ledger in the project, trailing 10 days."* **False.** `LEDGER_ARGUS.md` carries a 2026-08-11 entry acknowledging the data-residency note in full. Corrected above. A second instance the same session: a `^RATIFIED:` grep missed `**RATIFIED:` and implied SEQ8 was unstamped. **Both are the same error — a pattern too strict, whose false negative reads as another lane's neglect.** Under CONVENTIONS §6.2 that is Class A: asserting what a file contains without reading it properly.

**F-6 · Real ledger gaps, measured correctly.** `[verified]` HEPHAESTUS **1 entry against 35 reports, 10-day gap** — the widest. HERMES 8 days, entries owed for two cycles (mine). DIONYSUS still on its founding seed. APOLLO 2 days. **ARGUS and ATHENA are current.** ATHENA's new ruling binds all of us: a build document that does not append its lane ledger in the same session is an incomplete deliverable.

**F-7 · CONVENTIONS §8 mangled edit — third cycle, unfixed.** `[verified]` An orphan fragment (`08:30. **Not armed:** …`) survives beneath the rewritten "Triggers armed" paragraph. Cosmetic, in the file binding all six lanes.

**F-8 · `drops/` empty.** README only. `[verified]`

---

## 8 · Staleness

| artifact | last changed |
|---|---|
| `status/CONVENTIONS.md` · `CADENCE.md` · `RETENTION.md` · `HEARTBEAT.md` · `SECOND_ACCOUNT.md` | **2026-08-12** — all current |
| `status/MANIFEST.json` | 2026-08-12T10:59Z — **HEAD 1 commit behind** |
| `status/INTERFACE_PUBLISHED.md` | 2026-08-11 |
| Ledgers | ATHENA 08-12 · ARGUS 08-11 · APOLLO 08-10 · HERMES 08-04 · DIONYSUS 08-02 · HEPHAESTUS 08-02 |

---

## 9 · Pointers

Rules · `exchange/status/CONVENTIONS.md` — authoritative, read first
The move · `exchange/reports/NOTE_ATHENA_2026-08-12_ALL-LANES_STATUS-REFRESH.md` · `…HEPHAESTUS_2026-08-12_QUEUE-004-PHASE-A.md`
Ground truth · `exchange/status/MANIFEST.json` · `HEARTBEAT.md` · `status/daily/DAILY_2026-08-12.md`
Lanes · `exchange/status/LEDGER_{APOLLO,ARGUS,ATHENA,DIONYSUS,HEPHAESTUS,HERMES}.md`
Cadence · `CADENCE.md` · Retention · `RETENTION.md` · `SECOND_ACCOUNT.md`
Queue · `exchange/queue/` — 7 items + README
D: witnesses `[handoff]` · `research_outputs/_archive/POINTER.md` + 9 tracked `.sha256` sidecars
This lane · `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md`

*An index. Where it points, the artifact is authoritative.*
