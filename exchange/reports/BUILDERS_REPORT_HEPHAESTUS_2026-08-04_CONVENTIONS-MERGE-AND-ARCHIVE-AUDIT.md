# BUILDER'S REPORT — CONVENTIONS MERGE AND ARCHIVE AUDIT

**Contract:** operator paste, 2026-08-04 · **Executor:** HEPHAESTUS · **Branch:** `v12-v1-census` · **Environment:** local Windows Claude Code
**Status: COMPLETE.** `.gitignore` committed and pushed · CONVENTIONS §3 merged to one document · archive audit done (read-only).

**This is the first document written under the new single-document rule (§3.1) that this same run installed.**

Written zero-context. Every number is measured in this run.

---

## 1 · WHAT WAS DONE, AND ON WHOSE AUTHORITY

Three things, on the operator's 2026-08-04 paste, with push authorization for `.gitignore` in one commit and `exchange/**` via `publish_exchange.publish()`.

1. Committed the `.gitignore` change ATHENA left uncommitted on 2026-08-04.
2. Folded the two builder artifacts into ONE document in `exchange/status/CONVENTIONS.md` §3.
3. Enumerated where the phase archives actually exist — **read-only, list and stat only. Nothing was opened, copied, moved or deleted.**

**One operator decision was taken mid-build** (asked and answered before any edit landed): the §3 replacement block, as written, would have deleted two standing rules while asserting in the permanent record that nothing was dropped. The operator ruled: run the block, then carry the lost passages. That is what happened. Detail in §4.

---

## 2 · GATE AND PROBE VALUES, AS PRINTED

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=cc1d0bd
```

All four preflight gates passed: path contains `OneDrive…naiad`, branch is `v12-v1-census`, `exchange/status/CONVENTIONS.md` present.

---

## 3 · STEP 1 — THE STRANDED `.gitignore`

```
=== 1 - COMMIT THE STRANDED .gitignore (ATHENA left this uncommitted 2026-08-04) ===
   .gitignore | 3 +++
   1 file changed, 3 insertions(+)
  staged: .gitignore
[v12-v1-census a97fec3] chore: commit the research_outputs/_unarchived ignore rule left uncommitted by the 2026-08-04 s3 restore
 1 file changed, 3 insertions(+)
To https://github.com/catpatrol/Naiad.git
   cc1d0bd..a97fec3  v12-v1-census -> v12-v1-census
  GITIGNORE PUSH SUCCEEDED
```

**Commit `a97fec3`, pushed.** The staged set was exactly `.gitignore` — the block's own guard confirmed it before committing. The three lines are the `research_outputs/_unarchived/**` ignore rule from the 2026-08-04 s3 restore.

This closes a loop opened earlier the same day: that file had been the sole blocker on the `docs/knowledge` move (commit `cc1d0bd`), where it was stashed and restored byte-identically rather than committed, because no authorization for it existed at that time.

---

## 4 · STEP 2 — TWO ARTIFACTS FOLDED INTO ONE DOCUMENT

### 4.1 What the block did

```
=== 2 - CONVENTIONS section 3: TWO ARTIFACTS -> ONE DOCUMENT ===
  OK  section 3 replaced: two artifacts folded into one document
--- section 3 headings after the edit ---
  16:## §0 · What this file is, and why you are reading it
  56:## §1 · How to talk to the operator
  114:## §2 · How to build a paste for HEPHAESTUS
  196:## §3 · How to hand work back — ONE document
  203:### 3.1 The build document
  236:### 3.2 The file-disposition table — six columns, standing
  255:### 3.3 Publishing and the on-screen close
  267:### 3.4 The publish invocation — written out, because two wrong forms have shipped
  281:## §4 · Where things live, and who can see what
  346:## §5 · Lane charters
  421:## §6 · Evidence discipline
  481:## §7 · Carried backlogs and locked rulings
  519:## §8 · Infrastructure inventory — MOVED FROM MEMORY #25
  542:## §9 · Claude-optimization track — MOVED FROM MEMORY #9
  557:## §10 · MOVED-FROM-MEMORY REGISTER
  586:## §11 · Maintenance guide — step by step, plain language
--- the old two-artifact language must be gone ---
```

The heading scan found section 3 exactly once (line 195, 0-indexed) and section 4 exactly once (292), so the soft-halt did not fire. The two-artifact grep returned no matches — the old language is gone.

### 4.2 CONTRACT DEFECT — the merge was not content-preserving, and said it was

The replacement block's own preamble writes into the permanent record:

> *The required content is unchanged — nothing below was dropped in the merge.*

**That was false as written.** A dry-run diff of the replacement against the live section — performed before anything was written to disk — found three passages with no counterpart:

| lost passage | what it is |
|---|---|
| **Two §6.2 Class A cures** | (1) any Windows path inside a bash block uses forward slashes; (2) any "run the script" instruction is checked against the module *actually having an entry point* before it ships |
| **The §2.3 Class B cure** | a verification gate matches a **distinctive fragment**, case-insensitively — never a full sentence quoted from prose the same author is writing in the same act |
| Worked example + rationale | the `C:\venvs\naiad\Scripts\python.exe` → `C:venvsnaiadScriptspython.exe` collapse, and why a `__main__`-less module run as a script is the worst failure shape available |

A token-level diff after the replacement found one further substantive loss: the sentence tying the review content to the prime directive — *"everything the operator and reviewer need to discriminate the best path forward toward Naiad's objective of consistently profitable trading systems."*

**Handled, not silently patched.** The operator was asked before publish and ruled: run the block, then carry the lost passages. All four are now carried — the three into §3.4 with an explicit provenance note, the prime-directive framing into §3.1. Verification:

```
  Class A cures      : 1
  distinctive frag   : 1
  worked example     : 2
```

Residual token diff against the pre-merge section: **18 words, all of them two-artifact scaffolding or prose variance** — `artifacts`, `beside`, `mandatory`, `exceptions`, `package`, `sent`, `copied`→`written`, `runs`→`publishes`, `described`, `decision`, `memory`, `extended`, `already`, `here`, `each`, `reads`, `text`, `escape`. **No standing rule remains lost.** The preamble's claim is now true.

**Note the shape of this defect.** The rule most cleanly deleted by the merge was the rule about how verification gates must be written. Deleting it was self-undermining, and it is the reason the dry-run was run before the write rather than after.

### 4.3 A second defect in the block, found while running it — reported, not fixed

The block's own verification gate cannot report success:

```bash
grep -n "SESSION_SUMMARY_<LANE>\|TWO artifacts\|..." FILE | sed 's/^/  /' || echo "  none found - clean"
```

`sed` is the last stage of the pipe, so the pipeline's exit status is `sed`'s (always 0). When `grep` finds nothing it returns 1, but that status is discarded — so `|| echo "none found - clean"` can never fire. The gate silently produces empty output in both the pass case and a broken-grep case. It happens to be harmless here because empty output *is* the pass signal, but the gate does not prove what it claims to.

This is a **§2.3 Class B instance** — the same class as the rule the merge would have deleted. Cure for future pastes: capture `grep`'s status directly (`if grep -q ...; then ... else ... fi`), never through a pipe that ends in a formatter.

---

## 5 · STEP 3 — WHERE THE PHASE ARCHIVES ACTUALLY EXIST

**Read-only throughout. `os.listdir` / `os.walk` / `os.path.getsize` only. No archive was opened, copied, moved or deleted.**

### 5.1 The block's enumeration, as printed

```
THE QUESTION: do the phase archives exist anywhere other than this machine?

--- LOCAL phase archives
    research_outputs\_archive
    analytics_tests_v1.0.0_2026-07-29.zip                    6816
    analytics_v1.0.0_2026-07-29.zip                         19641
    s1_2026-07-27.zip                                   106239157
    s2_2026-07-27.zip                                   246355294
    s3_2026-07-27.zip                                   269919602
    tc1_2026-07-27.zip                                  242926299
    tc4_2026-07-27.zip                                   68700167
    tc5_2026-08-02.zip                                   18375498
    tc5_2026-08-02.zip.sha256                                  86
    v3_anchor_2026-07-27.zip                             91049070
    subtotal: 10 files, 1043591630 bytes

--- GOOGLE DRIVE backup folder
    G:/My Drive/naiad-backups
    naiad_estate_2026-07-28.zip                         492306779
    naiad_estate_2026-07-28.zip.sha256                         95
    naiad_estate_2026-08-02.zip                         493542600
    naiad_estate_2026-08-02.zip.sha256                         95
    naiad_workflow_2026-08-02.zip                         1132236
    naiad_workflow_2026-08-02.zip.sha256                       97
    naiad_workflow_2026-08-04.zip                         1794646
    naiad_workflow_2026-08-04.zip.sha256                       97
    subtotal: 8 files, 988776645 bytes

--- ALSO FOUND
    G:/My Drive/Naiad-backups
    [identical 8-file listing]
    subtotal: 8 files, 988776645 bytes

=== VERDICT ===
  local phase zips              : 9
  present in the Drive folder   : 0
  NOT in the Drive folder       : 9
     *** analytics_tests_v1.0.0_2026-07-29.zip                  6816 bytes ***
     *** analytics_v1.0.0_2026-07-29.zip                       19641 bytes ***
     *** s1_2026-07-27.zip                                 106239157 bytes ***
     *** s2_2026-07-27.zip                                 246355294 bytes ***
     *** s3_2026-07-27.zip                                 269919602 bytes ***
     *** tc1_2026-07-27.zip                                242926299 bytes ***
     *** tc4_2026-07-27.zip                                 68700167 bytes ***
     *** tc5_2026-08-02.zip                                 18375498 bytes ***
     *** v3_anchor_2026-07-27.zip                           91049070 bytes ***

  1043591544 bytes (995 MB) of PERMANENT STUDY EVIDENCE exists on this machine only,
  unless the browser-uploaded second Drive account holds it - which is NOT
  machine-verifiable and is recorded by hand in exchange/status/SECOND_ACCOUNT.md.
```

### 5.2 THAT VERDICT IS WRONG. Two probe defects, both corrected below.

**Defect 1 — `naiad-backups` and `Naiad-backups` are the same directory.** `os.path.samefile()` returns **True**. Windows paths are case-insensitive; the "ALSO FOUND" block is one folder listed twice. Anything summing the two subtotals double-counts by 988,776,645 bytes.

**Defect 2 — the probe looked in one folder and concluded from it.** `G:/My Drive` actually contains:

```
    'analytics_tests_v1.0.0_2026-07-29.zip'
    'analytics_v1.0.0_2026-07-29.zip'
    'desktop.ini'
    'naiad (local folder) BACKUP'   (dir)
    'naiad-backups'                 (dir)
```

Two of the nine "missing" zips sit at the **Drive root**, and the phase archives live in **`naiad (local folder) BACKUP`** — neither path was probed.

### 5.3 CORRECTED ENUMERATION — every local archive file vs the whole Drive

| LOCAL ARCHIVE FILE | LOCAL BYTES | DRIVE BYTES | DRIVE LOCATION |
|---|---:|---:|---|
| `analytics_tests_v1.0.0_2026-07-29.zip` | 6,816 | 6,816 | `analytics_tests_v1.0.0_2026-07-29.zip` (Drive root) |
| `analytics_v1.0.0_2026-07-29.zip` | 19,641 | 19,641 | `analytics_v1.0.0_2026-07-29.zip` (Drive root) |
| `s1_2026-07-27.zip` | 106,239,157 | 106,239,157 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |
| `s2_2026-07-27.zip` | 246,355,294 | 246,355,294 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |
| `s3_2026-07-27.zip` | 269,919,602 | 269,919,602 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |
| `tc1_2026-07-27.zip` | 242,926,299 | 242,926,299 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |
| `tc4_2026-07-27.zip` | 68,700,167 | 68,700,167 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |
| **`tc5_2026-08-02.zip`** | **18,375,498** | **ABSENT** | ***MACHINE-ONLY*** |
| **`tc5_2026-08-02.zip.sha256`** | **86** | **ABSENT** | ***MACHINE-ONLY*** |
| `v3_anchor_2026-07-27.zip` | 91,049,070 | 91,049,070 | `naiad (local folder) BACKUP/naiad/research_outputs/_archive/` |

```
local archive files          : 10
with a byte-identical copy   : 8
MACHINE-ONLY                 : 2
machine-only bytes           : 18,375,584  (17.5 MB)
```

### 5.4 CORRECTED VERDICT

**17.5 MB is machine-only, not 995 MB.** Eight of the ten local archive files have a byte-size-identical Drive counterpart. The single exposed phase archive is **`tc5_2026-08-02.zip`** and its `.sha256` — and the reason is chronological, not procedural: the `naiad (local folder) BACKUP` snapshot predates it. TC-5 was archived on 2026-08-02; every other phase archive dates from 2026-07-27 or 2026-07-29 and was captured by that snapshot.

Sizes match exactly, which is good evidence of integrity but **is not a hash check** — the `.sha256` sidecars were not opened, per the read-only instruction. A true integrity verification remains available and unperformed.

### 5.5 A third finding: the Drive mount contradicts the record

`SETUP_2026-07-28.md` Part B states, with a checked list: *"there is no Google Drive on this machine. Not a streaming mount, not a local folder, not installed."* It further flagged that this **contradicted a `[verified]` FACT line** claiming a local Drive sync folder existed, and concluded `backup_estate.py`'s offsite target was blocked.

**`G:` is mounted today** and holds 988 MB of estate/workflow archives plus the phase-archive snapshot. Between 2026-07-28 and 2026-08-04 the Drive was installed or reconnected. The 2026-07-28 finding is stale and the blocker it recorded is resolved. Recorded here so nobody re-derives the old conclusion from the old report.

### 5.6 The hand-recorded second account

```
last_manual_upload: 2026-07-28
```

`SECOND_ACCOUNT.md` is present and readable. **The date is stale against three artifacts that postdate it:** `naiad_workflow_2026-08-02.zip`, `naiad_workflow_2026-08-04.zip`, and `tc5_2026-08-02.zip`. By that file's own rule — *"If an archive is newer than the date, section 0 raises: manual upload to the second Google Drive account is outstanding"* — **the manual upload is outstanding.**

Note the file's own instruction: *"Phase archives in `research_outputs/_archive` are permanent evidence and are never pruned; if the second account does not hold them, upload those too."* `tc5_2026-08-02.zip` is exactly that case.

### 5.7 `boxrescue/`

```
--- is boxrescue/ still inside the repo tree? ---
  YES - 26 files. Operator: move it OUTSIDE the repo.
```

**Still inside the repo**, 26 entries, untracked. Not moved — the paste scoped step 3 read-only and moving it was not authorized.

---

## 6 · STEP 4 — PUBLISH

```
=== 4 - PUBLISH ===
   M exchange/status/CONVENTIONS.md
  ?? exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md
publish: committed 82538f9 (2 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= 82538f9 pushed= True offenders= []
```

**PUSH SUCCEEDED.** Two paths, zero offenders: the merged CONVENTIONS.md and the DIONYSUS note that arrived via OneDrive from another lane. This document is published in a second call whose commit id appears in the on-screen close.

---

## 7 · FINDINGS REPORTED, NOT FIXED

1. **The archive probe's verdict was wrong by a factor of 57** (995 MB claimed exposed vs 17.5 MB actual). Cause: it probed one hard-coded Drive folder and treated absence there as absence everywhere. Cure for future pastes: walk the Drive root, and compare on `(name, size)` across all locations rather than set-differencing one directory.
2. **`samefile` blindness.** Case-variant Windows paths were reported as two distinct locations. Any future backup audit should de-duplicate with `os.path.samefile` before summing.
3. **The block's grep gate cannot fail** (§4.3). Class B; cure stated there.
4. **`SETUP_2026-07-28.md` Part B is stale** (§5.5) and its recorded blocker on `backup_estate.py` no longer holds.
5. **`SECOND_ACCOUNT.md` is stale by three artifacts** (§5.6) — manual upload outstanding.
6. **`boxrescue/` remains inside the repo tree** (§5.7), 26 entries, untracked.
7. **`tc5_2026-08-02.zip` integrity is unverified.** Sizes match nothing for it — it has no Drive counterpart at all; and no `.sha256` sidecar anywhere was opened, so even the eight matched archives are size-matched, not hash-matched.

---

## 8 · WHAT REMAINS OPEN, WITH ITS OWNER

| # | item | owner |
|---|---|---|
| 1 | Upload `tc5_2026-08-02.zip` + `.sha256` to Drive, then to the second account | operator |
| 2 | Update `last_manual_upload` in `exchange/status/SECOND_ACCOUNT.md` after doing so | operator |
| 3 | Move `boxrescue/` outside the repo tree (needs an authorized paste) | operator → HEPHAESTUS |
| 4 | Correct or retire `SETUP_2026-07-28.md` Part B now that `G:` is mounted | ATHENA |
| 5 | Re-point `backup_estate.py`'s offsite target at `G:/My Drive/naiad-backups`, now unblocked | ARGUS or HEPHAESTUS |
| 6 | Decide whether `naiad (local folder) BACKUP` is a maintained destination or a one-off snapshot — nothing after 2026-07-29 is in it | operator |
| 7 | Hash-verify the eight matched archives against their `.sha256` sidecars | HEPHAESTUS, on authorization |

**The honest next option, with its implication:** item 6 is the one that decides whether this audit's good news holds. If `naiad (local folder) BACKUP` is a one-off snapshot rather than a maintained target, then every phase archive created from now on lands in the same position `tc5` is in today — machine-only — and the reassuring 8-of-10 becomes worse with each phase. If it is maintained, only `tc5` needs attention.

---

## 9 · VERSIONS, HASHES, COMMITS

```
python            3.12.10   (C:/venvs/naiad/Scripts/python.exe)
branch            v12-v1-census
head at start     cc1d0bd
commits this run  a97fec3  chore: commit the research_outputs/_unarchived ignore rule
                  82538f9  exchange: auto-publish 2026-08-04  (CONVENTIONS.md + DIONYSUS note)
remote            origin  https://github.com/catpatrol/Naiad.git
```

No hash is recorded for this file itself — §3.1: a file must never contain its own sha256.

---

## 10 · FILE DISPOSITION

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `.gitignore` | yes | tracked | `a97fec3` | yes — `origin/v12-v1-census` | GitHub only |
| `exchange/status/CONVENTIONS.md` | yes | tracked | `82538f9` | yes — `origin/v12-v1-census` | GitHub + workflow archive |
| `exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md` | yes | tracked | `82538f9` | yes — `origin/v12-v1-census` | GitHub + workflow archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_CONVENTIONS-MERGE-AND-ARCHIVE-AUDIT.md` | yes | untracked at write time | see on-screen close | see on-screen close | GitHub + workflow archive |
| `research_outputs/_archive/tc5_2026-08-02.zip` | yes | ignored — `.gitignore:24-32` research_outputs family | n/a | no | **NOT PROTECTED** |
| `research_outputs/_archive/tc5_2026-08-02.zip.sha256` | yes | ignored — same rule | n/a | no | **NOT PROTECTED** |
| `research_outputs/_archive/` (other 8 files) | yes | ignored — same rule | n/a | no | phase archive on `G:` (size-matched, not hash-verified) |
| `boxrescue/` | yes | untracked | not committed | no | **NOT PROTECTED** |
| `exchange/status/SECOND_ACCOUNT.md` | yes | tracked | pre-existing | yes | GitHub + workflow archive |

**Committed is not pushed. Pushed is not backed up.**

Nothing under `research_outputs/` was created, modified, moved or deleted by this run. The archive audit was list-and-stat only.
