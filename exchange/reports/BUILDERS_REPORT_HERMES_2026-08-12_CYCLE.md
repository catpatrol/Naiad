# BUILDERS REPORT — HERMES — 2026-08-12 — CYCLE

**Lane:** HERMES · **Surface:** Claude Cowork, `naiad` folder attached · **Instruction:** `PRIMER_HERMES_2026-08-11_v4.md` §6
**Read cold, zero prior context.** Every term defined at first use.

---

## 0 · The headline, before anything else

**Your daily automation has been dead for three days, and the bus looks healthy — because a fix installed last week is masking it.**

On 2026-08-09 the daily routine's *required* first job halted: `HALT: F-M3, F-M4 failed; no partial adoption`. The run stopped there. Nothing has run since — no output for 08-10, 08-11 or 08-12.

You have not seen this because queue 002 made the **publish** step refresh `MANIFEST.json`, and eleven publishes ran on 08-11. So the file every lane reads to check the repo is six hours old and looks fine. **The signal that used to mean "the routine ran" now only means "someone published."** A fix that closed one defect is concealing a larger one.

Everything else in this report is smaller than that.

**Date note:** the primer is dated 2026-08-11; my sandbox clock reads 2026-08-12T01:04Z. I used the measured clock and am flagging the difference rather than silently picking. `[verified]`

---

## 1 · §6.0 — CONVENTIONS read

`exchange/status/CONVENTIONS.md`, **50,218 B**, modified 2026-08-11 21:09. Read end to end. `[verified]`

One rule found there, quoted because it governed how I wrote this document — **THE FIRST RULE**:

> *"Be elitist, clever, concise, efficient, and elegant… Signal-dense, never padded… Clever means the solution that makes the problem small, not the one that shows off. Elegant means the shortest version that loses nothing — detail and context are never the fat; ceremony is."*

**No primer/CONVENTIONS conflict found this cycle.** One correction to the primer, in §5 F-4.

**Closing my own prior finding:** H-1 from 2026-08-05 — CONVENTIONS asserting both a `LEDGER+exchange` tick set and a wider `docs/`+`prompts/` sync — **is fixed**. §4.3 now leads with the live tick set and records the correction in full, including the 21.2% / 109.7% implication. That is what a correction looks like. `[verified]`

---

## 2 · §6.2 — Budget, both figures

Against **6,390,000 B**. *(Derived, not given — the box figure back-solves from the primer's own percentages. Correct me if the true capacity differs.)*

| reading | bytes | % of box | state |
|---|---:|---:|---|
| **Guard-metered** — `exchange/` only, what `publish` enforces | 1,745,187 | **27.31%** | ⚠ **WARNING** (warn 25% / refuse 40%) |
| **Tick-set truth** — `exchange/` + `LEDGER.md` | 2,000,198 | **31.30%** | the real occupancy |
| metering gap | 255,011 | **3.99 pts** | `LEDGER.md`, invisible to the guard |

Primer v4 recorded ~26.4% guard / ~30.4% tick-set. Both have grown ~0.9 points since. The gap is exactly `LEDGER.md` and is structural, not drift.

| split | bytes | % | files |
|---|---:|---:|---:|
| prose (`.md`/`.txt`) | 1,186,879 | 18.57% | 89 |
| data (all other) | 558,308 | 8.74% | 10 |
| **`exchange/` total** | **1,745,187** | **27.31%** | **99** |

| folder | bytes | % |
|---|---:|---:|
| `exchange/reports/` | 1,376,681 | 21.54% |
| `exchange/status/daily/` | 183,665 | 2.87% |
| `exchange/status/` | 126,860 | 1.99% |
| `exchange/queue/` | 42,084 | 0.66% |
| `exchange/` root | 15,336 | 0.24% |
| `exchange/drops/` | 561 | 0.01% |

### Files over 1% — two, both data, both APOLLO's

| file | bytes | % box | proposed home | replaced by |
|---|---:|---:|---|---|
| `exchange/reports/MC1_results.json` | 261,072 | **4.09%** | `research_outputs/mc1/` | ~1 KB pointer stub (path + sha256 + bytes + box cost) |
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% | `research_outputs/wf1/` | ~1 KB pointer stub |

Together **374,427 B = 5.86% of the box, and 67% of all data in `exchange/`.**

**Moving both takes the guard from 27.31% → 21.5% — out of WARNING, back under the 25% line, for two files.** The template already exists and is exemplary: `docs/history/argus/CAPTURE_2026-08-03_post_ny.json.pointer.md`, 1,060 bytes standing in for 1.88 MB.

**I moved nothing.** These are proposals; `reports/` files belong to their lanes.

### The other eight data files — leave them

`status/MANIFEST.json` (24,164) and seven dated `status/daily/MANIFEST_*.json` (19,644–26,000 each). Total 183,881 B / 2.88%. Each under 0.5%, the rolling window caps the series, and their purpose *is* to be read off the bus. **Recommendation stands from last cycle: give the content guard a named exception for `status/**/MANIFEST*.json`.** A rule in permanent technical breach stops being enforced. ATHENA's to draft.

### §6.2 — Rotation candidates (queue 003, >30 days)

**ZERO.** Cutoff 2026-07-13. Checked two ways: no `exchange/reports/*.md` has an mtime older than the cutoff, and none carries a filename date older than it. The oldest four are dated 2026-07-28 — fifteen days inside the window.

**Queue 003's tooling is built and has nothing to move.** Not urgent; revisit ~2026-08-28 when the 07-28 set ages out.

---

## 3 · §6.1 — Inventory summary

99 tracked files under `exchange/`. **24 carry a filename date of 2026-08-06 or later** — the span primer §2f warned my DIGEST was blind to. I enumerated rather than trusting the list, and found items it did not name: `ARGUS_PANTHEON_REPORT_2026-08-06.md`, `SS_SYSTEM_SYNTHESIS_2026-08-06.md`, `BUILD_APOLLO_2026-08-06_MC1.md`, `MC1_results.json`, `queue/2026-08-06_MC1_may26_program_APOLLO.md`, two `STATUS_ATHENA_2026-08-11_*` files, and both 08-11 data-residency notes. All are now indexed in the DIGEST.

**D: residency.** I cannot see `D:/Naiad`. Indexed via repo-side witnesses only, all `[handoff]`: `research_outputs/_archive/POINTER.md` (511 B) plus **nine tracked `.sha256` sidecars**. The local `_archive/` folder holds those ten files and **zero `.zip`** — consistent with relocation, and the sidecars are the canonical GitHub-held fingerprints that never move. I assert nothing about D: contents.

---

## 4 · §6.4 — Ledger staleness sweep

| lane | ledger newest | entries | newest artifact | artifacts | gap |
|---|---|---:|---|---:|---|
| HEPHAESTUS | 2026-08-02 | **1** | 2026-08-11 | **26** | **9 d** |
| ARGUS | 2026-07-27 | **1** | 2026-08-06 | 5 | **10 d** |
| HERMES | 2026-08-04 | 2 | 2026-08-11 | 2 | 7 d |
| ATHENA | 2026-08-05 | 7 | 2026-08-11 | 9 | 6 d |
| DIONYSUS | 2026-08-02 | **1** | 2026-08-04 | 4 | 2 d |
| APOLLO | 2026-08-10 | 2 | 2026-08-06 | 2 | leads |

**Five of six trail. Three hold exactly one entry — their founding seed from 2026-08-02.** HEPHAESTUS has filed 26 reports against a single ledger line.

This is no longer six lanes being slow; it is **a mechanism that is not being used.** Work flows through `reports/`, which is well-populated and current. The per-lane ledger was meant to be the status layer, and in practice `reports/` is. Two honest options — retire the ledgers and let the DIGEST index `reports/` directly, or make appending one a step in the build document. **Either is fine; the present state, where the layer exists and is empty, is the one that misleads.** ATHENA's design call, not mine. I include myself: my own ledger is 7 days stale and this cycle's entry is in §8 below, not yet appended.

---

## 5 · §6.3 — Findings

**F-1 · The routine is dead and the fix is hiding it.** `[verified]`
Detailed in §0. Mechanism: F-M3 (two-build determinism) and F-M4 (read-only porcelain audit) both failed on 2026-08-09, halting a *required* job under a no-partial-adoption clause — the contract behaving correctly. But `HEARTBEAT.md` and `RETENTION.md` are frozen at 08-09 while `MANIFEST.json` reads 08-11, because publish now refreshes the manifest independently. **Freshness of `MANIFEST.json` is no longer evidence the routine ran.** Anything downstream of the routine — the brief, `brief2_capture`, `brief2_panel`, the daily window — has produced nothing for three days.
*Not diagnosed here:* I did not run the manifest job. Why F-M3/F-M4 fail is HEPHAESTUS's to determine.

**F-2 · New largest file on the bus: `MC1_results.json`, 261,072 B, 4.09%, data.** `[verified]` §2 above.

**F-3 · `queue_open` reports 0 against six queue items.** `[verified]`
Last cycle it reported 1 against four; now 0 against six. Degraded, not improved. Anyone trusting the manifest's queue count sees an empty queue. Flagged 2026-08-05, unresolved.

**F-4 · Correction to primer §2c: queue 003 is partly built.** `[verified]`
The primer says 003 is "RATIFIED, NOT BUILT — next build." But `scripts/rotate_reports.py` (13,423 B) is committed at `f3efb0f`, message *"queue 003 D-1: rotate_reports.py — move aged build documents off the bus."* Absent: `exchange/status/ROTATION_LOG.md`, `docs/history/reports/`. Reading: D-1 done, remainder pending. Combined with zero rotation candidates (§2), **nothing is blocked either way.**

**F-5 · Manifest HEAD trails live HEAD — third consecutive cycle.** `[verified]`
`11c3fb83` vs `04d05ab`: **10 commits behind**, nine of them `exchange: auto-publish`. Queue 002 closed the staleness class *at publish time*; between publishes it reopens. Naming it "a closed defect class" is one step stronger than the evidence — it is closed on the publish path, open on the commit path.

**F-6 · CONVENTIONS §8 still carries the mangled edit — second cycle.** `[verified]`
Line 764: `08:30. **Not armed:** the HERMES scheduled run. **Manual and staying manual:** Sync now.` — orphaned tail of a rewritten sentence. Cosmetic, but it sits in the file that binds all six lanes, and my structurally identical H-1 *was* fixed properly in §4.3 while this was left. ATHENA's file.

**F-7 · Six inbox notes, zero acknowledged by their recipients.** `[verified]`
Four addressed to APOLLO. The two oldest (ARGUS→APOLLO, ARGUS→ATHENA, both 2026-08-03) have been open **nine days**. Test used: does the recipient's own ledger reference the note. Given F-4's finding that ledgers are broadly unmaintained, **this test may be measuring the ledger rather than the recipient** — I state that limit rather than let the zero read as neglect.
*Correction to primer §4:* both 08-11 data-residency notes are **already on the bus**, not operator-held.

**F-8 · Backup posture, three days stale** `[handoff — DAILY_2026-08-09]`
`operator-exports` folder missing at `G:\My Drive\naiad-backups` · 3 of 3 operator-preference blocks uncaptured · **OneDrive.exe not running**, so the repo is not syncing to the cloud · second Google Drive upload outstanding (workflow archive 2026-08-09 vs last manual upload 2026-08-05). None verifiable by me, and all four are as of the last routine that completed.

**F-9 · `drops/` empty.** README only. `[verified]`

---

## 6 · What I did not do

Deleted nothing · moved nothing (all relocations are proposals) · re-authored no lane's content · instructed no lane · did not push · did not run the manifest job or diagnose F-M3/F-M4 · **did not verify my own executions** (duty D6): the two files below were written and hashed by me, and nobody has independently checked them.

---

## 7 · File-disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/DIGEST.md` | yes | tracked | not committed | no | none — worktree only | 13,135 B · **0.21%** |
| `exchange/reports/BUILDERS_REPORT_HERMES_2026-08-12_CYCLE.md` | yes | untracked (new) | not committed | no | none — worktree only | 13,888 B · **0.22%** |

**Combined 27,023 B = 0.42% of box.** Both prose, both far under the 1 MB per-file cap.
**`exchange/` after this cycle: 1,758,931 B = 27.53%** — still WARNING. Tick-set truth 2,013,942 B = **31.52%**. Only the §2 pointer stubs clear the line.

*Correction, same session: this table first carried estimated byte counts (11,489 and ~13,100). Both were wrong — the real values are above, measured after writing. A `[verified]` row that was never measured is exactly the Class C provenance error CONVENTIONS §6.2 names, and I made it in the table whose whole purpose is to be exact.*

*Per CONVENTIONS §3.1 neither row carries its own sha256 — that value is stale the moment it is written. Hashes are printed on screen at close.*

---

## 8 · STATUS

```
=== STATUS_HERMES — 2026-08-12 ===
NOW: Cycle run per primer v4 §6. DIGEST rebuilt over the 2026-08-05 edition, now indexing the
24 artifacts dated 08-06 or later. Nine findings; the routine's three-day outage is the one that
matters. Nothing moved, nothing deleted, nothing pushed.
LAST EVENT: 2026-08-12 — HERMES cycle; DIGEST.md and this report written.
FACTS:
- Daily routine HALTED 2026-08-09 (F-M3, F-M4, required job); no output 08-10/11/12. HEARTBEAT
  frozen at exit 1 while MANIFEST.json reads 08-11 via publish — the fix masks the outage [verified]
- Budget: guard-metered exchange/ 1,745,187 B = 27.31% (WARNING); tick-set truth with LEDGER.md
  2,000,198 B = 31.30%; metering gap is LEDGER.md, 3.99 pts [verified]
- Two files over 1%, both data, both APOLLO's: MC1_results.json 261,072 B (4.09%) and
  WF1_discriminants.json 113,355 B (1.77%) = 67% of all exchange/ data. Pointering both -> 21.5% [verified]
- Rotation candidates (>30d): ZERO. Queue 003 D-1 IS built (scripts/rotate_reports.py, f3efb0f) —
  correcting primer §2c; ROTATION_LOG.md and docs/history/reports/ absent [verified]
- Five of six lane ledgers trail their filed reports; three hold only their founding entry;
  HEPHAESTUS 26 reports against 1 [verified]
- Six inbox notes, zero acknowledged in recipient ledgers; two open 9 days. queue_open reports 0
  against six items [verified]
PENDING:
1. Repair the daily routine — F-M3/F-M4 fixture failure, blocking since 2026-08-09 (HEPHAESTUS)
2. Authorise pointer stubs for MC1_results.json + WF1_discriminants.json — clears the WARNING
3. Rule on the ledger layer: retire it, or make appending part of the build document
4. Publish these two files, then click Sync now — nothing reaches the web lanes until then
NEXT: Operator rules item 1. Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 · files re-ingested = 1
=== END STATUS ===
```
