# BUILDER'S REPORT — HEPHAESTUS · T-4 memory snapshot + scoping report + acceptance contract · 2026-08-03

Forensic record. Standalone: assumes zero prior context. Provenance tags:
[verified] = computed or read by the builder this session · [handoff] = asserted by
the contract that commissioned this work · [operator] = operator-reported.

---

## 1 · What this session was asked to do

ATHENA (the system-resilience reviewer lane) commissioned ticket **T-4**: take a
durable, verbatim copy of the 30 entries currently held in Claude's *project memory*
— which lives only in Anthropic's cloud and can be erased by a single settings
action — and commit it into the repository, together with two companion documents:
the session summary explaining what was decided, and a pre-registered acceptance
contract that fixes the pass/fail bar for the memory restructuring *before* any
memory is edited.

Three files were to be created, committed, and pushed under a one-time push
authorization (operator ruling **G-5(a)**, ratified 2026-08-03, scoped to this paste
only and explicitly non-transferable).

Nothing in memory was edited by this session. This session only *copied* memory into
the repo. [verified]

---

## 2 · Environment assertion — as printed

```
=== ENVIRONMENT ASSERTION (halts before any write) ===
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
branch=v12-v1-census head=afa5013
```

Both required conditions held: the working directory matched `*OneDrive*naiad*`
(the local Naiad working clone) and the branch was `v12-v1-census`. HEAD before any
write was `afa5013`. [verified]

**Directory creation:** neither `docs/memory` nor `exchange/reports` had to be
created — both already existed, so the contract's `CREATED missing directory:` line
did not print for either. [verified]

---

## 3 · DEVIATION — how the block was executed, and why

**The contract's bash block could not be executed as an inline command.** The
harness passes a bash block to the OS as a single spawn argument; at ~63 KB this
block exceeded the Windows argument-length limit and the spawn failed before any
shell existed:

```
ENAMETOOLONG: name too long, uv_spawn
```

This is an operating-system limit, not a syntax or content problem with the
contract. No shell ran, so nothing in the repository was touched by the failed
attempt. [verified]

**Resolution, and what was preserved.** The block was written byte-for-byte to a
file *outside the repository* — in this session's scratchpad directory, which is not
under version control and holds no project state — and then executed with `bash`.
This preserves the two properties the contract's design depends on:

1. **The block still ran as one unit, verbatim.** No step was reordered, skipped,
   paraphrased, or re-authored. The heredocs, the gates, the staged-set check, the
   commit message and the push all executed in the contract's own order.
2. **The environment assertion still halted before any repository write.** The only
   write that preceded the assertion was the scratchpad script itself, which lives
   outside the repo and outside OneDrive.

**Integrity check on the transcribed script, before running it** [verified]:

| Check | Value |
|---|---|
| Script size | 63,228 bytes |
| CR (`\r`) byte count | **0** |
| LF (`\n`) line count | 378 |

The CR count matters: a CRLF-line-ended script would have carried stray carriage
returns into the heredoc bodies and silently corrupted all three committed files
with invisible bytes. It was checked with a Python binary read, not with `grep`, per
the standing rule that msys `grep`/`sed` strip CR and cannot be trusted for byte
questions.

This deviation is reported, not hidden, because it changes *how* the contract ran.
It did not change *what* the contract wrote. Future ATHENA pastes above roughly
30 KB should expect the same limit and can pre-empt it by shipping the block as a
file-write plus a `bash <file>` line.

---

## 4 · Verification gates — full transcript as printed

```
=== VERIFICATION GATES (written from post-action state) ===
entry headers found: 30 / 30
docs/memory/claude_project_memory_2026-08-03.md : 48278 bytes
exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md : 9514 bytes
exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md : 2876 bytes
staged: docs/memory/claude_project_memory_2026-08-03.md exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md
```

| Gate | Requirement | Observed | Result |
|---|---|---|---|
| G-A entry count | exactly 30 `### Entry ` headers in the snapshot | 30 | **PASS** |
| G-B size floor · snapshot | > 1,500 bytes | 48,278 | **PASS** |
| G-C size floor · session summary | > 1,500 bytes | 9,514 | **PASS** |
| G-D size floor · acceptance contract | > 1,500 bytes | 2,876 | **PASS** |
| G-E staged set | exactly the three expected paths, sorted | exact match | **PASS** |

No gate printed `HALT`. No `git reset` was triggered. [verified]

---

## 5 · Commit and push — as printed

```
[v12-v1-census a58b2bb] docs+exchange: T-4 verbatim memory snapshot (30 entries), memory-scoping session summary, pre-registered acceptance contract (operator rulings Q-0,G-1..G-5 2026-08-03)
 3 files changed, 330 insertions(+)
 create mode 100644 docs/memory/claude_project_memory_2026-08-03.md
 create mode 100644 exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md
 create mode 100644 exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md
To https://github.com/catpatrol/Naiad.git
   afa5013..a58b2bb  v12-v1-census -> v12-v1-census
=== PUSH SUCCEEDED ===
a58b2bb docs+exchange: T-4 verbatim memory snapshot (30 entries), memory-scoping session summary, pre-registered acceptance contract (operator rulings Q-0,G-1..G-5 2026-08-03)
```

| Field | Value |
|---|---|
| Commit (short) | `a58b2bb` |
| Commit (full) | `a58b2bb5aacccea4760b2dc6692e215521534f48` |
| Parent | `afa5013` |
| Branch | `v12-v1-census` |
| Remote | `https://github.com/catpatrol/Naiad.git` |
| Remote ref after push | `origin/v12-v1-census` = `a58b2bb` (re-read after the push) |
| Push result | **PUSH SUCCEEDED** |
| Files changed | 3 files, 330 insertions, 0 deletions |
| Commit timestamp (local) | 2026-08-04T00:21:00−03:00 |

**A note on the dates, so nobody later reads a contradiction into them.** All three
artifacts carry the session date **2026-08-03** in their filenames and text, per the
contract. The machine clock had just passed midnight when the commit landed, so git
records the commit timestamp as 2026-08-04T00:21 local. The filenames are correct as
the session's date; the timestamp is correct as the clock's. They are not in
conflict. [verified]

Authorization basis for the push: operator ruling **G-5(a)**, 2026-08-03, scoped to
`docs/memory/*` and `exchange/reports/*` for this paste only. Note that
`docs/memory/` sits **outside** `exchange/**` and therefore outside the standing
auto-publish scope (ruling W1 Q-2); it rode this explicit one-time authorization, not
the routine publish path. The authorization is not treated as carrying forward to any
later paste or environment. [verified against the commissioning contract]

---

## 6 · Content hashes of the committed artifacts

Computed by Python `hashlib` on binary reads after the commit. This report's own
hash is deliberately absent — a file cannot contain its own sha256 without the row
being permanently wrong.

| File | Size (bytes) | sha256 |
|---|---|---|
| `docs/memory/claude_project_memory_2026-08-03.md` | 48,278 | `05f730e9370ef8c06255402e7f7647cac9f472a437c2a48c6fb5fcd00551c705` |
| `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` | 9,514 | `8fc41d535b9bde8fe65265b13379b930f9d6eddae626041491cbad85d1781d31` |
| `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | 2,876 | `39e700bdd0090b8eb545d7a033185397a6a9261ccbdb4a889ff59a32c3d06deb` |

All three are clean in `git status` after the commit — the working-tree bytes and
the committed blobs are the same bytes. [verified]

---

## 7 · Findings reported, not fixed

### FINDING 1 (material) · The armed weekly backup does not cover this snapshot's directory

The whole premise of T-4 is that `docs/memory/` is the durable copy of project
memory. That premise depends on `docs/memory/` actually reaching a backup archive.
It currently reaches one only when the operator runs the workflow backup by hand.

What was read this session [verified]:

| Fact | Source | Value |
|---|---|---|
| `--workflow` source list includes `docs/memory` and `exchange` | `scripts/backup_estate.py:140-152` (`WORKFLOW_SOURCES`) | yes, both present |
| Armed weekly Task Scheduler job | `schtasks /query /tn "Naiad weekly backup"` | `C:\venvs\naiad\Scripts\python.exe scripts\backup_estate.py --estate --dest "G:\My Drive\naiad-backups"` |
| — its mode | same | **`--estate` only. Not `--workflow`.** |
| Daily routine job registry | `scripts/routine_jobs.json` | four jobs (manifest, brief, brief2_capture, brief2_panel) — **no backup job of any mode** |
| Staleness reminder exists | `scripts/routine_jobs.json` → `reminders.workflow_max_days` | 8 days (report-only; it warns, it does not run anything) |
| Newest workflow archive on `G:\My Drive\naiad-backups` | directory listing | `naiad_workflow_2026-08-02.zip`, 1,132,236 bytes, written 2026-08-02 18:22 |

Consequence, stated plainly: the workflow archive that exists was written on
2026-08-02 and therefore **predates all three files this session created**. Until
someone runs `backup_estate.py --workflow`, the only off-machine copy of the memory
snapshot is GitHub. GitHub is one third-party service, and by the project's own
standing principle (memory entry #24: "sync is NOT backup", one copy on one provider
is not a backup), that is below the bar this snapshot was created to meet.

Not fixed here because arming or running a backup was outside this contract's scope
and would have been an unrequested change to the operator's scheduled tasks. The
remedy is one command, and it belongs to the operator or to ATHENA's next paste:

```
C:\venvs\naiad\Scripts\python.exe scripts\backup_estate.py --workflow --dest "G:\My Drive\naiad-backups"
```

Whether the weekly trigger should be changed to run both modes is an ATHENA design
decision, not a builder decision, so it is raised rather than made.

### FINDING 2 (informational) · Transcription fidelity is unverifiable from this side

The snapshot's own provenance section states it was transcribed by ATHENA from the
memory panel by hand. The builder can verify that 30 entry headers are present, that
the bytes committed are the bytes written, and that nothing was corrupted in transit
— all of which passed. The builder **cannot** verify that the transcribed text
matches what the memory panel actually holds, because the builder has no access to
the memory surface. That check is only available to a web lane reading the panel.
ATHENA already logs this as risk R-1 in the session summary, with the closing
snapshot as the intended second independent capture. Recorded here so the limit of
this session's verification is explicit rather than assumed. [verified as a scope
limit; not a defect]

### FINDING 3 (informational) · Pre-existing untracked files at repo root

`git status` shows six untracked files at the repository root that predate this
session and were left untouched: `Cascade Rewire.html`,
`Cascade_Atlas_CENSUS_1b.html`, `Cascade_Atlas_CENSUS_1b_v2_1.html`,
`HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md`,
`PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md`,
`SS_Reassessment_Synthesis_2026-08-03.md`. Two tracked files were also already
modified before this session began: `exchange/DIGEST.md` and
`exchange/status/LEDGER_HERMES.md`. None were staged, committed, or altered by this
paste — the staged-set gate would have halted if any had been. Noted only so the
next session is not surprised by them. [verified]

---

## 8 · What this session did NOT do

- Did not read, edit, delete or reorder any project-memory entry.
- Did not touch the data estate at `C:\Users\luisf\AppData\Local\naiad\data_cache`.
- Did not delete any file anywhere.
- Did not modify `exchange/DIGEST.md`, any lane ledger, or any pre-existing report.
- Did not run any backup.
- Did not treat the G-5(a) push authorization as extending beyond this paste.

---

## 9 · FILE DISPOSITION TABLE

Six columns per the standing rule. "At time of writing" means at the moment this
report file was written, before `scripts/publish_exchange.py` ran.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `docs/memory/claude_project_memory_2026-08-03.md` | yes (48,278 B) | tracked | yes — `a58b2bb` | yes — `origin/v12-v1-census` | **GitHub only.** Inside `WORKFLOW_SOURCES` but the newest archive (`naiad_workflow_2026-08-02.zip`) predates it — see Finding 1 |
| `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` | yes (9,514 B) | tracked | yes — `a58b2bb` | yes — `origin/v12-v1-census` | **GitHub only.** Same gap as above |
| `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` | yes (2,876 B) | tracked | yes — `a58b2bb` | yes — `origin/v12-v1-census` | **GitHub only.** Same gap as above |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md` (this file) | yes | untracked at time of writing | **not committed** at time of writing | **no** at time of writing — `scripts/publish_exchange.py` runs next; see §10 | **NOT PROTECTED** at time of writing |
| `…\scratchpad\t4_snapshot.sh` (contract block, executed copy) | yes | **outside the repository** — session scratchpad, not under version control | n/a — intentionally never committed | n/a | **NOT PROTECTED**, by design. Ephemeral; the contract text itself is preserved in ATHENA's conversation record |

Reminders that belong with this table: committed ≠ pushed; pushed ≠ backed up; and a
file that "isn't visible on GitHub" is usually the browser opening the default branch
`main` instead of `v12-v1-census`, which is where all project work lives.

---

## 10 · Publish step

`scripts/publish_exchange.py` was run after this file was written, per the standing
handback rule, so that this report rides the guarded `exchange/**` publish. Its
result is stated on screen in the session output and appended below by the operator's
transcript rather than pre-declared here — this file cannot honestly report the
outcome of a command that runs after it is written.

---

## 11 · Exact artifacts for the operator to carry

Repository root: `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`

| File | Full repo-relative path |
|---|---|
| Memory snapshot (the T-4 deliverable) | `docs/memory/claude_project_memory_2026-08-03.md` |
| Session summary (the decision artifact) | `exchange/reports/SESSION_SUMMARY_ATHENA_2026-08-03_MEMORY-SCOPING.md` |
| Acceptance contract (pre-registered) | `exchange/reports/ACCEPTANCE_MEMORY-RESTRUCTURE_2026-08-03.md` |
| This builder's report | `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-03_T4-SNAPSHOT.md` |

All four reach the web lanes through GitHub sync — no hand-uploads. The operator's
one remaining action is a single **Sync now** click in the Naiad project settings.

=== STATUS_HEPHAESTUS — 2026-08-03 ===
NOW: T-4 executed. The 30-entry verbatim memory snapshot, ATHENA's memory-scoping
session summary and the pre-registered acceptance contract are committed and pushed
to origin/v12-v1-census. All five verification gates passed; no HALT printed. No
memory entry was read or edited by this session.
LAST EVENT: 2026-08-03 — commit a58b2bb pushed under one-time authorization G-5(a).
FACTS:
- Gates 30/30 entry headers, three size floors, exact staged set — all PASS [verified]
- Commit a58b2bb, 3 files, 330 insertions; origin/v12-v1-census re-read = a58b2bb [verified]
- Contract block exceeded the OS argument limit (ENAMETOOLONG); run verbatim from a scratchpad file, 0 CR bytes verified before execution [verified]
- Armed weekly task runs --estate ONLY; no trigger runs --workflow, and the newest workflow archive (2026-08-02) predates these files [verified]
- Snapshot's off-machine copy is therefore GitHub alone until --workflow is run [verified]
- Transcription fidelity vs the live panel is not builder-verifiable — ATHENA's R-1 stands [open]
PENDING:
1. Operator: click Sync now in the Naiad project settings
2. Operator or ATHENA: run backup_estate.py --workflow so the snapshot exists off GitHub
NEXT: ATHENA drafts the CONVENTIONS.md paste. Owner: ATHENA.
METRICS: operator actions this session = 1 · files re-ingested = 0
=== END STATUS ===
