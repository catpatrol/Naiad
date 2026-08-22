# HEPHAESTUS — tc5 archive and AI operating-system scaffolding

**Filed:** report named `2026-08-03`; the **machine clock read `2026-08-02` throughout**. The filename
is kept as instructed and every timestamp below is the real observed value. This matters more than
usual here — see step 2, where the paste names an archive by a date the script never wrote.

**Lane:** HEPHAESTUS (local Windows Claude Code, working Naiad clone).

---

## STEP 0 — ASSERT

| check | result |
|---|---|
| OS is Windows | PASS — `Windows_NT` |
| pwd is repo root | PASS — `…\Midas-Claude Code Resources\naiad`, `LEDGER.md` present |
| branch | PASS — `v12-v1-census` |
| **HEAD at start** | **`71b6700`** |
| **Porcelain count at start** | **0** — clean and synced with origin |

Assert satisfied; proceeded.

---

## 1 · FIRST LIVE `--phase` RUN — **7/7 after a fix; the first attempt exposed a real defect**

`research_outputs/tc5` held **506 files / 417,724,843 B**, of which exactly **2 are git-tracked**
(`manifest.json`, `run_log.txt`).

### The first attempt came in 6/7 — and the failure was the mode itself, not the data

```
PASS F-K1 - 506/506 members verified both directions; 0 mismatches, 0 strays, 0 omissions
FAIL F-K3 - 20-file sha sample unchanged: True; git porcelain identical: False
...
fixtures failed -- source kept, nothing released
```

The archive was sound. **F-K3 was unpassable by construction.** Diagnosis:

- `--phase` writes its output **inside the repo**, to `research_outputs/_archive/`.
- The `.zip` is ignored by `.gitignore:38 *.zip`. **The `.sha256` sidecar is not** —
  `git check-ignore` exits 1 for it.
- So every `--phase` run creates a new untracked entry, and F-K3 then asserts `git status` is
  byte-identical before and after. Those two facts cannot both hold.

**This was not a cosmetic failure.** Releasing sources is gated on `fx.ok`:

```python
if not fx.ok:
    print("\nfixtures failed -- source kept, nothing released")
elif args.delete_source:
    ...
```

So **`--delete-source` could never have fired**, on any phase, ever. The mode's entire purpose —
archive, verify, then reclaim — was blocked by its own fixture. It went unnoticed because this is the
first time the script's `--phase` mode has been run live; the 2026-07-27 phase archives predate it
and carry no sidecars (confirmed: `tc5_2026-08-02.zip.sha256` is the only `.sha256` in `_archive/`).

**Fix:** F-K3 now normalises out *this run's own output paths* — the archive and its sidecar — and
stays strict about everything else. Exactly the precedent set for F-M4 in `reviewer_manifest.py`
when the exchange migration made the manifest's output tracked. Two forms are dropped and only two:
a line naming an output exactly, and a collapsed `?? dir/` entry that contains an output (git prints
the directory rather than its contents when the whole directory is untracked). Anything the run did
not write still lands in the comparison and still fails the fixture.

`--estate` and `--workflow` were never affected — their destination is the Drive, outside the repo.

### The clean run

```
phase      : tc5
members    : 506  (git-tracked among them: 2)

PASS F-K1 - 506/506 members verified both directions; 0 mismatches, 0 strays, 0 omissions
N/A  F-K2 - completeness vs census.json applies to --estate only
PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
             (this run's own 2 output path(s) normalised out)
PASS F-K4 - 10 members restored outside repo; 0 hash mismatches
PASS F-K5 - re-read from destination: matches=True, sidecar matches=True, CRC clean=True, 506 members
PASS F-K6 - guard refuses to overwrite the archive just written
PASS F-K7 - 2/2 git-tracked source files still present on disk; 0 missing

--delete-source not given: source kept intact. 504 untracked files (2 tracked) would be releasable.

7/7 fixtures pass
```

| field | value |
|---|---|
| members | **506** |
| verified | **506** |
| mismatches | **0** |
| strays | **0** |
| omissions | **0** |
| archive | `research_outputs\_archive\tc5_2026-08-02.zip` (18,375,498 B) |
| **sha256** | **`68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357`** |
| **git-tracked files preserved** | **2 / 2** — `research_outputs/tc5/manifest.json`, `research_outputs/tc5/run_log.txt` |

`--delete-source` was **not** passed, as instructed. Mismatches were 0, so no halt.

The superseded 6/7 archive was removed before the re-run; its sha256 was
`7a7866ac41a65e4349df172a39322c142fa663c650099c9b0186158332a88258`, same 506 members, same 18,375,498
bytes. The hashes differ only because a zip embeds per-entry timestamps and the embedded manifest
carries a fresh `created_utc`; the member set and every member's own sha256 are identical.

### ⚠ This archive is exposed to the Windows case-collision hazard

`research_outputs/tc5/manifest.json` sits at the archive root, and every archive also carries an
embedded `MANIFEST.json` at its root. **On a case-insensitive filesystem, extracting this archive
silently overwrites `manifest.json` with `MANIFEST.json`** — the same defect found yesterday in the
s3 extraction, now confirmed to apply to tc5 as well. Restore case-sensitively, or rename one entry
first. Mitigating factor: `manifest.json` is git-tracked here, so it is independently recoverable.

## 2 · INDEPENDENT RE-VERIFY — **both runs agree exactly**

```
archive : research_outputs\_archive\tc5_2026-08-02.zip
mode    : phase/tc5 · created_utc : 2026-08-02T18:40:03Z
members : 506 · verified : 506 · mismatches : 0 · strays : 0 · omissions : 0
archive sha256: 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357
VERIFIED
```

| | build run | verify run | agree |
|---|---|---|---|
| members | 506 | 506 | ✓ |
| verified | 506 | 506 | ✓ |
| mismatches | 0 | 0 | ✓ |
| archive sha256 | `68942d6261bf8ca8…` | `68942d6261bf8ca8…` | ✓ |

**Exact agreement, zero mismatches — the step-3 precondition is met.**

### ⚠ Filename discrepancy — the paste names a file that does not exist

The instruction says to verify `research_outputs\_archive\tc5_2026-08-03.zip`. The script dates
archives from the machine clock, which reads **2026-08-02**, so the file it wrote is
**`tc5_2026-08-02.zip`**. `Test-Path` on the `08-03` name returns **False** — there is no such file.

I verified **the archive that was actually written**, since verifying a non-existent path would have
failed for a reason that says nothing about the data. If the intent was that today is the 3rd, the
machine clock disagrees, and that is worth resolving before any dated artifact is cited by name —
the report filename carries the same one-day offset.

## 3 · RELEASE — **504 files, 417,721,048 B freed, both tracked files preserved**

Both runs agreed with zero mismatches, so the release was authorized. **Each file was re-checked
against the archive's embedded manifest immediately before deletion** — it had to be pinned, and its
bytes on disk had to hash to the pinned value. A file failing either check would have been kept and
reported, and the script refuses to delete anything if even one fails.

```
git-tracked under research_outputs/tc5: 2
  PRESERVE  research_outputs/tc5/manifest.json
  PRESERVE  research_outputs/tc5/run_log.txt

archive pins: 506 members
files on disk: 506
verified-and-releasable : 504
KEPT (failed a check)   : 0

RELEASED 504 untracked files, 417,721,048 B
files remaining under research_outputs/tc5: 2
tracked files missing after release: 0
```

**Bytes freed: 417,721,048 (398.4 MB).**

**Preserved-file list — everything git-tracked, still in place:**

| file | status |
|---|---|
| `research_outputs/tc5/manifest.json` | present, untouched |
| `research_outputs/tc5/run_log.txt` | present, untouched |

`git status` shows **no deletion of any tracked file**. Empty directories left behind were removed;
no directory still holding a file was touched.

## 4 · `docs/primers/OPERATOR_PREFERENCES.md` — **ALREADY EXISTED; HEADINGS ALIGNED**

This file was created in the previous cycle and committed in `1563bff`. It was **not recreated** —
recreating it would have overwritten committed work for no gain. Its two headings were updated to
this paste's exact wording:

| was | now |
|---|---|
| `## PART 1 — Verbatim settings (operator pastes)` | `## PART 1 — Verbatim settings (operator fills by hand)` |
| `## PART 2 — Distilled working conventions (Athena, 2026-08-03)` | `## PART 2 — Distilled working conventions (ATHENA — TO BE FILLED NEXT CYCLE)` |

Content already matched the specification and is unchanged: three empty labelled blocks — **User
preferences · Project instructions · Custom style** — each an empty fenced block naming its source in
the settings UI, under a note stating these **exist only in Claude's cloud settings, are excluded
from data exports, and must be pasted manually**. Two guards remain: an empty block means *"not yet
captured"*, never "not set"; and paste **verbatim**, because Part 1 is a faithful copy and Part 2 is
where interpretation belongs.

**Still empty. Only you can fill it.**

## 5 · `docs/memory/README.md` — **ALREADY EXISTED; STALENESS NOTE UPDATED**

Also created last cycle, committed in `1563bff`, **not recreated**. It already states the full
convention: snapshots **append-only, dated, never edited**; the newest supersedes older ones **for
reading only, never by deletion**; discrepancies resolve to `LEDGER.md` first, then the newest
snapshot. And the reason the directory exists: **project memory is not included in Anthropic data
exports**, so **these snapshots are the only durable copy**.

### The entry count still does not match — now stated twice

| measure | value |
|---|---|
| numbered operator-ratified entries in `claude_project_memory_2026-07-26.md` | **19** |
| highest number used in Section 2 | **19** |
| last entry | *"Paste-routing convention (2026-07-26…)"*, file line 196 of 196 |
| live project memory | **29**, per the operator |

The instruction has now given the snapshot's count as **21** twice. Counted directly, it is **19**.

I did not silently overwrite the verified figure with the stated one, because the count is checkable
and was checked. Nor did I ignore the repetition: the README's note now records that **21 has been
stated twice**, keeps **19** as the verified content of Section 2, and offers the reconciliation that
costs nothing to accept — **21 may be the correct count of the *live* memory at export time, or may
count Section 1 items differently.** Both can be true at once. What is certain is what Section 2 of
this file holds.

**It changes the size of the gap, not its existence. A fresh export is due either way, and taking one
settles it permanently.**

## 6 · WORKFLOW BACKUP — **7/7 FIXTURES PASS**

```
roots archived   : 8
    docs/memory      2 · docs/knowledge  4 · skills       2 · prompts     13
    claude           1 · exchange       33 · docs/primers  4 · docs/history 8
    absent : drops/operator-exports · exchange/drops/operator-exports
members to archive: 67

PASS F-K1 - 67/67 members verified both directions; 0 mismatches, 0 strays, 0 omissions
N/A  F-K2 - completeness vs census.json applies to --estate only
PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
PASS F-K4 - 10 members restored outside repo; 0 hash mismatches
PASS F-K5 - re-read from destination: matches=True, sidecar matches=True, CRC clean=True, 67 members
PASS F-K6 - guard refuses to overwrite the archive just written
PASS F-K7 - 67/67 git-tracked source files still present on disk; 0 missing

archive : G:\My Drive\naiad-backups\naiad_workflow_2026-08-02.zip
size    : 409,086 B (26.9% of source) · members: 67 · source: 1,519,134 B
```

**Archive sha256: `f981cc3e17fe15afad08756426b38e09759aee7ba05ebd6df101cce2011cf112`**

**Both directories confirmed present**, read from the archive's own member list rather than inferred:

```
docs/memory/README.md
docs/memory/claude_project_memory_2026-07-26.md
docs/primers/# ORCHESTRATOR PRIMER — what a fresh orchestrator session needs to know.txt
docs/primers/About Apollo, Athena, Argus, Hermes and Dionysus.txt
docs/primers/About Apollo, Athena, Argus, Hermes, Hephaestus and Dionysus.txt
docs/primers/OPERATOR_PREFERENCES.md
```

### ⚠ Third same-day supersede — this is now a pattern, not an incident

Dated archive names mean **any same-day re-run must first have the existing archive removed by hand**.
That is by design (ruling R-B — generations accumulate, nothing is overwritten) and it is correct for
the weekly scheduled task, which fires once. But it has now cost three manual deletions in one day:

| # | archive | superseded sha256 | members |
|---|---|---|---|
| 1 | `naiad_workflow_2026-08-02.zip` | `a480625ae594edc1…` | 64 |
| 2 | `naiad_workflow_2026-08-02.zip` | `e7e76a5b006c1a44…` | 66 |
| 3 | `tc5_2026-08-02.zip` (the 6/7 run) | `7a7866ac41a65e43…` | 506 |

Each replacement was a superset or an exact re-make, and each was verified before the superseded copy
was reported gone — but **deleting backups by hand three times in a day to satisfy a naming rule is a
process smell.** Worth a ruling: a `--force`/`--suffix` option for same-day re-runs, or an
auto-incrementing `-2` suffix, would remove the need entirely.

## 7 · COMMIT AND PUSH — **DONE**

```
[v12-v1-census ec1317e] ops: tc5 archived; AI operating-system scaffolding
 4 files changed, 62 insertions(+), 13 deletions(-)
 create mode 100644 research_outputs/_archive/tc5_2026-08-02.zip.sha256
To https://github.com/catpatrol/Naiad.git
   6bac35d..ec1317e  v12-v1-census -> v12-v1-census
```

**The sidecar was committed deliberately.** It is 86 bytes and it is the durable integrity pin for an
18 MB archive that is intentionally *not* in git (`*.zip`). With it in the repo, anyone can verify
that archive later from the repository alone. Without it, porcelain would also carry a permanent
`?? research_outputs/_archive/`. Flagged rather than assumed: if archive hashes should stay out of
git, say so and it comes back out.

The 504 released files needed no staging — `research_outputs/tc5/**` is git-ignored, so their removal
is invisible to git. Both tracked files are unchanged.

```
$ git log --oneline -3
ec1317e ops: tc5 archived; AI operating-system scaffolding
6bac35d exchange: auto-publish 2026-08-02
71b6700 exchange: file the AI operating-system scaffolding report

$ git status -sb
## v12-v1-census...origin/v12-v1-census
```

**Synced, 0 tracked files dirty, 0 untracked.** `6bac35d` is the workflow backup's own publish step
firing between the two — `exchange/` paths only, guard clean.

### Tree size before / after

| measure | before | after | delta |
|---|---|---|---|
| "Midas-Claude Code Resources" files | 1,570 | **1,083** | −487 |
| tree bytes | 1,829,752,867 | **1,412,062,691** | **−417,690,176** |
| tree size | 1.704 GB | **1.315 GB** | **−0.389 GB** |
| C: free | 38.60 GB | **38.99 GB** | +0.39 GB |

(The file-count delta is −487 rather than −504 because the run also wrote the archive and sidecar,
and the earlier superseded copies were removed.)

Cumulative across the last two cycles: the tree has gone **5.655 GB → 1.315 GB**, a **77% reduction**,
with every released byte pinned in a verified archive first.

---

## SUMMARY OF VERDICTS

| step | verdict |
|---|---|
| 0 | **PASS** — Windows, repo root, `v12-v1-census`, HEAD `71b6700`, porcelain 0 |
| 1 | **DONE — 7/7** — 506/506, 0 mismatches, sha `68942d6261bf8ca8…`, 2/2 tracked preserved; **first attempt exposed an F-K3 defect that made `--delete-source` impossible on any phase** |
| 2 | **DONE** — independent verify agrees exactly: 506/506/0, same sha256; **paste's `tc5_2026-08-03.zip` does not exist** |
| 3 | **DONE** — 504 files released, **417,721,048 B freed**, every file re-checked against the archive first, both tracked files preserved |
| 4 | **ALREADY EXISTED** — headings aligned to this paste's wording; not recreated |
| 5 | **ALREADY EXISTED** — staleness note updated; **count is 19, not 21** |
| 6 | **DONE — 7/7** — 67 members, sha `f981cc3e17fe15af…`, both directories confirmed |
| 7 | **DONE** — `ec1317e` pushed; clean and synced; tree 1.704 → 1.315 GB |

## ITEMS FOR THE OPERATOR

1. **The machine clock says 2026-08-02, the paste says 2026-08-03.** Two reports and one archive now
   carry a one-day offset in their names. Worth settling before anything is cited by dated filename.
2. **Settle the 21-vs-19 memory count**, or simply take a fresh export — which resolves it permanently
   and is overdue regardless.
3. **Paste the three settings blocks.** `OPERATOR_PREFERENCES.md` is still an empty frame.
4. **Restoring `tc5_2026-08-02.zip` on Windows silently loses `manifest.json`** to case-collision.
   Same hazard as s3. Extract case-sensitively or rename first.
5. **Rule on same-day archive re-runs** — three manual backup deletions in one day is a process smell.
6. **Rule on committing archive sidecars** — done here deliberately; easily reversed.
7. **The `t <t@t>` committer** from the previous cycle is still unexplained.
8. **Configure GitHub sync and click Sync now** — still outstanding.

---

## METRICS (Q-8)

**Operator actions this session = 1** (one paste).
**Files re-ingested = 0.**
