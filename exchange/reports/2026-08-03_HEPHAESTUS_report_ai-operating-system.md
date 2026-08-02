# HEPHAESTUS — AI operating-system scaffolding

**Filed:** report named `2026-08-03`; **the machine clock read `2026-08-02 15:25` local throughout
this run.** The filename is kept exactly as instructed; every timestamp below is the real observed
value. Flagged so nobody later reconciles a one-day gap that is only a label.

**Lane:** HEPHAESTUS (local Windows Claude Code, working Naiad clone).

---

## STEP 0 — ASSERT

| check | result |
|---|---|
| OS is Windows | PASS — `Windows_NT`, Win 11 Home 10.0.26200 |
| pwd is repo root | PASS — `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`, `LEDGER.md` present |
| branch | PASS — `v12-v1-census` |
| **HEAD at start** | **`014434f`** |

Working tree clean, 0 tracked files dirty, synced with `origin/v12-v1-census`. Assert satisfied;
proceeded.

### ⚠ A commit landed on this branch that I did not make

Noticed while reading repo state, and reported because it is repo truth rather than a detail of this
task:

```
commit 9470d0436b26ec17361d7276425b45226cf051c8
Author: t <t@t>
Date:   Sun Aug 2 13:57:59 2026 -0300
    base
```

It is **on `origin/v12-v1-census`**, and it committed exactly the six paths I had deliberately left
untracked during the previous build: `ARGUS_REPRIME_2026-08-02.md`,
`ORCHESTRATOR CONTROL CENTER — protocol & state of record.txt`, `SCHED_TEST_RESULT_2026-08-02.md`,
`analytics/` (8 modules), `scripts/orchestrator_state.py`, and `tests/test_analytics.py` — 2,193
insertions.

Nothing here is damaged, and the content is plausibly wanted. Three things make it worth your
attention anyway:

1. **The author is `t <t@t>`** — a placeholder identity, not `catpatrol`. Whatever produced it had an
   unconfigured git identity.
2. **It landed mid-session and was pushed**, so another actor writes to this branch concurrently with
   the builder. That is the condition under which two processes race on `.git/index` — and this repo
   already lost a publish step to a stale `index.lock` on 2026-08-01.
3. **It silently resolved a decision I had left open for you.** The previous report listed those three
   root files as "unmatched — left at repo root, untouched" precisely so you could rule on where they
   belong. They are now tracked at repo root, which is an answer, but not one you gave.

No action taken. Reported for a ruling on what that actor is and whether it should be committing here.

---

## 1 · `docs/primers/OPERATOR_PREFERENCES.md` — **CREATED**

Skeleton exactly as specified.

**PART 1 — Verbatim settings (operator pastes)** carries three empty labelled blocks — **User
preferences**, **Project instructions**, **Custom style** — each an empty fenced `text` block with a
one-line note naming where in the settings UI it comes from.

The note above them states the constraint plainly: these settings **exist only in Claude's cloud
settings, are excluded from Anthropic data exports, and must be pasted by hand.** No script, backup or
sync can reach them. Two further guards are written in, because an empty block is ambiguous and
ambiguity is what rots a file like this:

- an empty block means **"not yet captured"**, never "not set";
- paste **verbatim** — no summarising or tidying. Part 1 is a faithful copy; interpretation belongs in
  Part 2.

**PART 2 — Distilled working conventions (Athena, 2026-08-03)** is a placeholder marked
**`TO BE FILLED BY ATHENA IN THE NEXT CYCLE`**, with one line stating that its emptiness records an
absent *written distillation*, not an absence of conventions.

## 2 · `docs/memory/README.md` — **CREATED**

States the convention in three numbered rules:

1. snapshots are **append-only, dated, never edited** — a correction is a new dated file, because a
   wrong snapshot was wrong *on that date* and that is part of the record;
2. **the newest snapshot supersedes older ones for reading only — never by deletion**; older
   snapshots stay forever, as the means of reconstructing what was believed and when;
3. discrepancies resolve to `LEDGER.md` first, then the newest snapshot.

And the reason the directory exists at all: **project memory is not included in Anthropic data
exports**, comes out by no automated route, and would be lost with the project — so **these snapshots
are the only durable copy.** The README notes they are themselves covered by
`backup_estate.py --workflow`, and cross-links `docs/primers/OPERATOR_PREFERENCES.md` as the same
problem with the same manual limitation.

### ⚠ The staleness figure does not match — reported, not silently picked

The instruction gave the snapshot's size as **21 entries**. I counted the file directly before writing
the claim:

| measure | value |
|---|---|
| numbered operator-ratified entries in `claude_project_memory_2026-07-26.md` | **19** |
| highest number used in Section 2 | **19** |
| last entry | *"Paste-routing convention (2026-07-26…)"*, file line 196 of 196 |
| entries in live project memory | **29**, per the operator (not machine-verifiable from here) |

So the file holds **19**, not 21. The README records 19 as the verified count, 29 as the
operator-reported live figure, and carries a short note that the instruction said 21 — flagged for you
to settle rather than resolved by me picking a number. **The gap's existence is not in doubt on any
reading; only its size is.** A fresh export is due either way.

The snapshot's own structure, for reference: Section 1 is the auto-generated project memory, Section 2
the numbered operator-ratified edits. The README tells a future exporter to keep that two-section shape.

## 3 · Workflow backup — **7/7 FIXTURES PASS, both new files confirmed as members**

```
roots archived   : 8
    docs/memory      2 · docs/knowledge  4 · skills       2 · prompts     13
    claude           1 · exchange       32 · docs/primers  4 · docs/history 8
    absent : drops/operator-exports · exchange/drops/operator-exports
members to archive: 66

PASS F-K1 - 66/66 members verified both directions; 0 mismatches, 0 strays, 0 omissions
N/A  F-K2 - completeness vs census.json applies to --estate only
PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
PASS F-K4 - 10 members restored outside repo; 0 hash mismatches
PASS F-K5 - re-read from destination: matches=True, sidecar matches=True, CRC clean=True, 66 members
PASS F-K6 - guard refuses to overwrite the archive just written
PASS F-K7 - 64/64 git-tracked source files still present on disk; 0 missing

archive : G:\My Drive\naiad-backups\naiad_workflow_2026-08-02.zip
size    : 403,265 B (26.8% of source) · members: 66 · source: 1,506,808 B
sha256  : e7e76a5b006c1a4471d703cd196439df323a333dbeb8c01b071a0db1057bf9b8
```

**Member count went 64 → 66 — exactly the two new files, nothing else moved.**

Pickup confirmed by reading the archive's own member list rather than inferring it from the counts:

```
docs/memory/README.md                                    ← new
docs/memory/claude_project_memory_2026-07-26.md
docs/primers/# ORCHESTRATOR PRIMER — what a fresh orchestrator session needs to know.txt
docs/primers/About Apollo, Athena, Argus, Hermes and Dionysus.txt
docs/primers/About Apollo, Athena, Argus, Hermes, Hephaestus and Dionysus.txt
docs/primers/OPERATOR_PREFERENCES.md                     ← new
```

`docs/primers/` went 3 → 4 files and `docs/memory/` 1 → 2, both as expected. Note the archive captured
the two files **before** they were committed — the workflow mode archives worktree state, which is the
correct behaviour for a backup and worth knowing.

### Same-day re-run required removing the earlier archive

`naiad_workflow_2026-08-02.zip` already existed from the delta build, and the no-clobber guard
correctly refused to overwrite it. To produce a current archive containing the new scaffolding I
**removed the earlier same-day archive and its sidecar**, then re-ran. Disclosed because it was a
deletion on the backup destination:

- superseded: `a480625ae594edc16a6802771a028b3eed40f5a2bc1ca5d1e249c04ba6b5009a`, 393,420 B, 64 members
- replacement: `e7e76a5b006c1a4471d703cd196439df323a333dbeb8c01b071a0db1057bf9b8`, 403,265 B, 66 members

The replacement is a **strict superset** — the same 64 members plus the two new files — and was
verified 66/66 before this report was written, so nothing was traded away.

**Ops friction worth knowing:** dated archive names mean **any same-day re-run needs a manual
removal first.** This is by design (ruling R-B, generations must accumulate) and it does not affect
the armed Sunday 08:30 task, which fires once a week. It affects humans re-running by hand — as
happened twice today.

## 4 · `G:\My Drive\naiad-backups\operator-exports\` — **CONFIRMED PRESENT**

Already existed (created during the delta build); nothing to create. Currently **0 items** — it is
waiting for the operator's Claude data export.

Worth restating in one line, since this directory is the reason both files above exist: **the data
export will not contain project memory, user preferences, project instructions or the custom style.**
Those four are exactly what `docs/memory/` and `docs/primers/OPERATOR_PREFERENCES.md` capture by hand.
The export covers conversations and account data; the scaffolding covers what it leaves behind.

## 5 · Commit and push — **DONE**

Staged exactly the two new files, verified before committing, nothing else.

```
[v12-v1-census 1563bff] ops: AI operating-system scaffolding — preferences, memory convention
 2 files changed, 102 insertions(+)
 create mode 100644 docs/memory/README.md
 create mode 100644 docs/primers/OPERATOR_PREFERENCES.md
To https://github.com/catpatrol/Naiad.git
   ae7948f..1563bff  v12-v1-census -> v12-v1-census
```

```
$ git log --oneline -3
1563bff ops: AI operating-system scaffolding — preferences, memory convention
ae7948f exchange: auto-publish 2026-08-02
014434f exchange: file the HEPHAESTUS delta build report (workflow backup, sweep, filing, reclaim)

$ git status -sb
## v12-v1-census...origin/v12-v1-census
```

`ae7948f` is the workflow backup's own publish step firing between the two — it committed the
regenerated `exchange/status/RETENTION.md`, guard clean, `exchange/` paths only.

**Final state: synced with origin, 0 tracked files dirty, 0 untracked.**

---

## SUMMARY OF VERDICTS

| step | verdict |
|---|---|
| 0 | **PASS** — Windows, repo root, `v12-v1-census`, HEAD `014434f`; unexplained commit `9470d04` flagged |
| 1 | **DONE** — `OPERATOR_PREFERENCES.md`, three empty verbatim blocks + Athena placeholder |
| 2 | **DONE** — `docs/memory/README.md`; staleness count corrected from 21 to a verified **19** |
| 3 | **DONE — 7/7** — archive `e7e76a5b006c1a44…`, 66 members, both new files confirmed present |
| 4 | **CONFIRMED** — `operator-exports\` exists, empty, awaiting the export |
| 5 | **DONE** — `1563bff` committed and pushed; clean and synced |

## ITEMS FOR THE OPERATOR

1. **Paste the three settings blocks into `OPERATOR_PREFERENCES.md`.** Nothing automated can do it,
   and until it happens the file records an absence rather than a copy.
2. **Take a fresh memory snapshot.** The one on file is a week old and short by ten entries on your
   own count.
3. **Settle the 21-vs-19 count** — the file holds 19; the instruction said 21.
4. **Rule on the `t <t@t>` committer.** Anonymous identity, pushed to this branch mid-session,
   committed the three root files that were deliberately left for your decision.
5. **Configure GitHub sync and click Sync now** — still outstanding, still the only thing that makes
   any of this visible to the web lanes.
6. **Queue item 001 remains unratified** (`queue_open = 1`).

---

## METRICS (Q-8)

**Operator actions this session = 1** (one paste).
**Files re-ingested = 0.**
