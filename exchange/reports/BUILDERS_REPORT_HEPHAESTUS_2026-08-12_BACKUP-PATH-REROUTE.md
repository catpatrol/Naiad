# BUILDER'S REPORT — HEPHAESTUS — 2026-08-12 — BACKUP PATH REROUTE

**Lane:** ATHENA (system resilience) · **Builder:** HEPHAESTUS, local Windows Claude Code
**Branch:** `v12-v1-census` · **HEAD at start:** `7552d652eb…508a00924` · **Repo:**
`C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad`
**Read this with zero prior context.** Every term is defined where it first appears.

---

## 0 · What this session was for, in one paragraph

You told me you had moved the `naiad-backups` folder off the Google Drive letter (`G:`) onto the
`D:` drive, and that both were still updating. My job was to check nothing had broken during the
move, and then to make the project's code write its backups to the new place. I did both. The
repository is intact, all 20 archives on `D:` verify byte-for-byte against their recorded
fingerprints, and the code now defaults to `D:/naiad-backups`. **Two things are not fixed and are
yours to decide** — the Sunday scheduled backups still point at the old folder, and I found
evidence that Google Drive's upload of the new folder is failing. Both are explained in plain
language in §7.

---

## 1 · Section A — the read-only integrity check

Section A wrote nothing. It only measured.

### 1.1 A1 — was the sync still running?

Measuring a folder while a sync client is still copying into it gives a false reading, so I
measured every file twice, sixty seconds apart, and compared.

```
  first measurement taken in 6.8s; waiting 60s ...
  .                      files 840->840  bytes 2404435867->2404435867  STABLE
      max mtime_ns 1786505867284450600 -> 1786505867284450600
  D:/naiad-backups       files 43->43  bytes 3047931992->3047931992  STABLE
      max mtime_ns 1786502814000000000 -> 1786502814000000000
  OneDrive.exe running : yes
  GoogleDriveFS running: yes
  BUSY_FLAG=0
```

**Both trees were byte-identical across the sixty seconds — file count, total size, and the newest
modification timestamp on any file.** The sync clients are running but idle. This is the gate the
rest of the session depended on.

### 1.2 A2 — is the repository itself healthy?

```
  git fsck --no-progress --no-dangling   ->  no output, exit 0   (zero errors)
  local HEAD  : 7552d652eb3717a9d90466fc81f7cb5508a00924
  origin      : 7552d652eb3717a9d90466fc81f7cb5508a00924
  ahead/behind: 0  0
  modified tracked: 2   untracked: 11
```

`git fsck` inspects every stored object for corruption; it printed nothing, which is what a clean
repository looks like. Local and remote were at the identical commit.

**The eleven untracked files — these exist in no other copy** and are listed because that is
precisely what makes them fragile:

```
  "Cascade Rewire.html"                    Cascade_Atlas_CENSUS_1b.html
  Cascade_Atlas_CENSUS_1b_v2_1.html        HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md
  PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md SS_Reassessment_Synthesis_2026-08-03.md
  briefs/panel/excursions/2026-08-03.parquet
  exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md
  research_outputs/wf1/                    scripts/mc1_program.py   scripts/mc1_report.py
```

### 1.3 A2b — a false alarm I raised and then corrected, because the correction is the finding

My first pass reported **6 tracked files missing from disk**:

```
  tracked files: 544   MISSING FROM DISK: 6
    MISSING: ORCHESTRATOR CONTROL CENTER â€” protocol & state of record.txt
    MISSING: docs/history/STATUS â€” BRIEF (…).txt
    …
```

Every one of those names contains `â€”` where an em-dash `—` belongs. That is the signature of
UTF-8 bytes being read as Windows-1252. My probe asked Python to decode git's output using the
system's default encoding rather than UTF-8, so it looked for files under mangled names and did
not find them. **This repository already documents this exact trap** — `scripts/backup_estate.py`
lines 252-266 record fixture F-K7 failing the same way on 2026-08-02, on the same three em-dash
files. Re-measured with explicit UTF-8:

```
  tracked files: 544   MISSING FROM DISK: 0

  the six em-dash paths, checked individually by exact UTF-8 name:
    exists=True   ORCHESTRATOR CONTROL CENTER — protocol & state of record.txt
    exists=True   docs/history/STATUS — BRIEF (daily market brief · Atlas HTML report · live laboratory).txt
    exists=True   docs/history/STATUS — ENGINE (engine builds · repo operations · integrity & manifest).txt
    exists=True   docs/primers/# ORCHESTRATOR PRIMER — what a fresh orchestrator session needs to know.txt
    exists=True   docs/reports/Naiad — Orchestrator Control Center.html
    exists=True   research_outputs/# Handoff — BTCUSDT 5m1h cache trun.txt
```

**Nothing is missing. 544 of 544 tracked files are present. Zero dehydrated files** (a "dehydrated"
file is a cloud-only placeholder that looks like a file but holds no bytes — the 2026-08-12
OneDrive census found 164 of them; the count is now zero across the whole tree).

### 1.4 A3 — the archives, and whether they survived the move

```
  D: (new)   D:/naiad-backups          ->  43 files, 2906.7 MB
  G: (old)   G:/My Drive/naiad-backups ->   0 files,    0.0 MB
```

**`G:/My Drive/naiad-backups` still exists as a folder but is empty.** The move was a move, not a
copy. I did not touch it; it was read-only this session by your instruction, and it remains
exactly as I found it.

Every `.zip` on `D:` was hashed and compared against its `.sha256` sidecar — a sidecar being a
small text file holding the fingerprint recorded when the archive was written. A match proves the
archive is byte-for-byte what it was at write time.

| archive | size | verdict |
|---|---:|---|
| `naiad_estate_2026-07-28.zip` | 469.5 MB | **VERIFIED** |
| `naiad_estate_2026-08-02.zip` | 470.7 MB | **VERIFIED** |
| `naiad_estate_2026-08-09.zip` | 472.2 MB | **VERIFIED** |
| `naiad_estate_2026-08-11.zip` | 472.7 MB | **VERIFIED** |
| `naiad_workflow_2026-08-02.zip` | 1.1 MB | **VERIFIED** |
| `naiad_workflow_2026-08-04.zip` | 1.7 MB | **VERIFIED** |
| `naiad_workflow_2026-08-09.zip` | 2.4 MB | **VERIFIED** |
| `naiad_workflow_2026-08-11.zip` | 2.6 MB | **VERIFIED** |
| `tc5_2026-08-02.zip` | 17.5 MB | **VERIFIED** |
| `analytics_tests_v1.0.0_2026-07-29.zip` | 0.0 MB | **VERIFIED** |
| `analytics_v1.0.0_2026-07-29.zip` | 0.0 MB | **VERIFIED** |
| `phases/s1_2026-07-27.zip` | 101.3 MB | **VERIFIED** |
| `phases/s2_2026-07-27.zip` | 234.9 MB | **VERIFIED** |
| `phases/s3_2026-07-27.zip` | 257.4 MB | **VERIFIED** |
| `phases/tc1_2026-07-27.zip` | 231.7 MB | **VERIFIED** |
| `phases/tc4_2026-07-27.zip` | 65.5 MB | **VERIFIED** |
| `phases/tc5_2026-08-02.zip` | 17.5 MB | **VERIFIED** |
| `phases/v3_anchor_2026-07-27.zip` | 86.8 MB | **VERIFIED** |
| `phases/analytics_tests_v1.0.0_2026-07-29.zip` | 0.0 MB | **VERIFIED** |
| `phases/analytics_v1.0.0_2026-07-29.zip` | 0.0 MB | **VERIFIED** |
| `analytics_tests_v1.0.0_2026-07-29 (1).zip` | 0.0 MB | *no sidecar — unverifiable* |
| `analytics_v1.0.0_2026-07-29 (1).zip` | 0.0 MB | *no sidecar — unverifiable* |
| `naiad_workflow_2026-08-02 (1).zip` | 1.1 MB | *no sidecar — unverifiable* |

**verified: 20 · mismatched: 0 · no sidecar: 3**

The three unverifiable files carry a ` (1)` suffix, the shape Windows and Drive give a duplicate.
Each is byte-identical in size to its unsuffixed twin, which *is* verified. They are almost
certainly copy artifacts. **I deleted nothing** — no delete authorization existed this session.

### 1.5 The gate

```
  BUSY=0  BAD=0   ->  GREEN - Section B proceeds.
```

---

## 2 · YOUR QUESTION, ANSWERED: is `D:/naiad-backups` Google-Drive-managed?

**Short answer: YES, it is registered with Google Drive as a mirrored folder — and NO, I cannot
confirm the archives have actually reached the cloud. There is active evidence that the upload is
failing.** Those are two different questions and the honest answer differs between them.

### 2.1 What `D:` is

| probe | `D:` | `G:` |
|---|---|---|
| `fsutil fsinfo drivetype` | Fixed Drive | Fixed Drive |
| `Get-Volume` | exFAT, label **LaCie**, 4,000,491,503,616 B | **no volume object** |
| `Get-Partition` | Disk 1, Partition 2, LaCie Rugged USB-C | **no partition object** |
| `Win32_LogicalDisk` VolumeName | LaCie | **Google Drive** (FAT32, synthetic) |

**`D:` is real hardware — a 4 TB LaCie Rugged USB-C external disk. `G:` is the Google Drive
virtual mount**, which is why the same two commands that succeed for `D:` fail outright for `G:`.

**This does not answer the question by itself, and that is the trap.** Google Drive's "Folders from
your computer" feature *mirrors a local folder* — a physical disk is entirely compatible with being
Drive-managed. Concluding "D: is a real disk, therefore not synced" would have been wrong.

### 2.2 The decisive evidence — Drive's own configuration

Google Drive stores its mirrored-folder list in the registry at
`HKCU\Software\Google\DriveFS\Share`, value `SyncTargets`, as a binary protobuf. Decoded:

```
  field 1  len 63   NESTED:
      field 1  len 23   NESTED:
          field 1  len 21   STRING  '103318730532797253152'      <- the signed-in account
      field 2  len 2    STRING  'G:'                             <- the mount point
      field 3  len 16   STRING  'D:\naiad-backups'               <- MIRRORED FOLDER
      field 3  len 14   STRING  'D:\Naid-GDRIVE'                 <- MIRRORED FOLDER
```

Corroborated in Drive's own database, read as raw bytes:

```
  root_preference_sqlite.db-wal   164832 bytes -> naiad-backups: ascii x15; Naid-GDRIVE: ascii x20
```

And `PerAccountPreferences` carries a `machine_root_doc_id`, which only exists when a "Folders from
your computer" machine root has been created for the account.

**This is measured, not inferred.** Google Drive's configuration explicitly names
`D:\naiad-backups` as a folder it mirrors. **The independent-provider property is intended to
survive the move.** Mirrored folders appear in the Drive web UI under **Computers**, not under
*My Drive* — which is also why `G:/My Drive/naiad-backups` being empty is consistent with a
working mirror rather than proof of one.

### 2.3 The finding that stops me short of "yes"

Drive's logs record what happened when it tried to upload those files:

```
2026-08-12T04:42:10.686Z E [mirror_103318730532797253152_COM] content_sync_manager.cc:255:RegisterUpload
  Creating hard link to D:\naiad-backups\naiad_workflow_2026-08-02.zip returned with
  UNKNOWN: CreateHardLinkW failed during CreateHardLink
2026-08-12T04:42:10.717Z E … D:\naiad-backups\naiad_estate_2026-08-02.zip.sha256 … CreateHardLinkW failed
2026-08-12T04:42:10.978Z E … D:\naiad-backups\tc5_2026-08-02.zip … CreateHardLinkW failed
```

**50 such failures naming `naiad-backups` paths**, timestamped today. Alongside them, at every
client start:

```
root_preference_manager.cc:1831:PushRoots  Pushing MirrorRoots had a non-success status:
  UNIMPLEMENTED: From legacy status ['UNSUPPORTED']
```

**And no upload-completion record for any `naiad-backups` file appears in any log.**

The cause is almost certainly the filesystem: **`D:` is exFAT, and exFAT does not support hard
links.** Drive stages a mirrored upload by hard-linking the file so the bytes cannot change
mid-transfer. On exFAT that call cannot succeed.

**So: registered, yes — provably. Uploaded, unproven, with active errors pointing the wrong way.
Registered is not uploaded.** I cannot settle this from the machine, because a mirrored folder is
not browsable locally. **It takes you thirty seconds in a browser** — see §7, O-1.

---

## 3 · Section B — every path reference, before and after

I searched the whole repository, not only the folders the contract named. **43 files mention the
old path. All but three are prose or dated history and were left alone.**

### 3.1 Changed — configuration and operational instructions

| file | line | before | after |
|---|---|---|---|
| `scripts/backup_estate.py` | 1349-1355 | `ap.error("--estate requires --dest")` / `"--workflow requires --dest"` — **no default at all** | resolves via `backup_dest_root(args)`, default `D:/naiad-backups` |
| `scripts/backup_estate.py` | 208+ | *(no such constant)* | `BACKUP_DEST_DEFAULT = "D:/naiad-backups"`, `BACKUP_DEST_ENV = "NAIAD_BACKUP_DEST"` |
| `scripts/routine_jobs.json` | 9 | `"backup_dest": "G:\\My Drive\\naiad-backups"` | `"backup_dest": "D:\\naiad-backups"` |
| `exchange/status/SECOND_ACCOUNT.md` | 33 | ``The newest generations from `G:\My Drive\naiad-backups`:`` | ``The newest generations from `D:\naiad-backups` — the LaCie external disk:`` + dated correction |
| `exchange/status/CONVENTIONS.md` | §8 | *(named no destination at all)* | new dated **"Backup destination — CHANGED 2026-08-12"** paragraph |
| `exchange/status/CADENCE.md` | after §3 | — | dated NOTE; the three original `G:` command lines **left verbatim** |

**A drafting defect in the contract, reported not silently worked around.** The instruction said
CONVENTIONS "§8 has its destination sentence rewritten". **There was no destination sentence.**
`grep` returned **0** hits for `My Drive` or `naiad-backups` in the entire file. That absence is
itself the story — §8 is the infrastructure inventory, and it never recorded where backups go,
which is exactly why the folder could move with nothing in the repo contradicting it. I **added** a
sentence rather than rewriting one, and said so in the text.

**Why CADENCE.md was annotated, not rewritten.** Its lines 31, 39 and 52 quote the scheduled tasks
as passing `--dest "G:\My Drive\naiad-backups"`. I re-enumerated Task Scheduler: **that is still
exactly what the tasks contain.** Those lines are a *true record of a stale configuration*.
Rewriting them to say `D:` would have made the file false. Verified after writing — the three
originals are intact at lines 31, 39, 52; the fourth occurrence at line 65 is my own note quoting
the live task.

### 3.2 Left alone — 40 files of prose and dated history

`docs/history/*` (2 files), `docs/memory/*` (3), `exchange/reports/*` (24, all dated build reports),
`exchange/status/daily/*` (6), `prompts/CONTRACT_v4_*`, `exchange/DIGEST.md`,
`exchange/status/LEDGER_ATHENA.md`, `HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md`,
`.claude/settings.local.json` (2 permission-allowlist entries naming old one-off probe commands —
inert strings, they grant permission for a command nobody will run again).

`exchange/status/RETENTION.md` needed no edit: it is **regenerated** by every backup run and now
reports `Location: D:\naiad-backups` on its own.

### 3.3 What the code change actually does

Precedence, verified by executing each path:

```
  PASS  backup_dest_root: no --dest -> the new default            D:\naiad-backups
  PASS  backup_dest_root: explicit --dest STILL WINS
  PASS  backup_dest_root: $NAIAD_BACKUP_DEST beats the default
  PASS  backup_dest_root: --dest beats $NAIAD_BACKUP_DEST
  PASS  backup_dest_root: HALTS on an unmounted drive             (SystemExit 2)
```

The halt reproduces the behaviour queue 002 gave `--phase` — it refuses rather than quietly writing
the backup onto the laptop it is backing up:

```
BACKUP DESTINATION UNREACHABLE: Q:\definitely-not-mounted
  The drive Q:\ is not mounted.
  --estate and --workflow write off-machine and will NOT fall back to
  the laptop -- a backup that lands on the machine it is backing up is not a backup.
```

**The `--phase` default is untouched** — still `D:/Naiad/research_outputs/_archive`, asserted.

**One gate of mine failed and the failure is instructive.** I asserted CADENCE.md would contain the
`G:` task string exactly 3 times. It contains 4 — because *my own note* quotes it a fourth time. I
wrote the gate from the state before my edit, which is the Class B error §2.3 names. Corrected
gate: the three originals are present at their original line numbers, and the fourth is accounted
for. (Three earlier assertion failures in the same block were escaping artifacts in my own test
string — `\n` inside `D:\naiad-backups` became a newline — and were re-run from a file with no
nested escaping, all green.)

---

## 4 · B3 — the live run that proves it

`backup_estate.py --workflow`, **with no `--dest` passed**, so the new default is what is being
tested.

```
destination      : D:\naiad-backups   (no --dest given; from built-in default)
destination      : D:\naiad-backups\naiad_workflow_2026-08-12.zip
roots archived   : 9 dir(s) + repo-root *.md
    docs/memory 6 · docs/knowledge 7 · skills 2 · prompts 15 · claude 1 · exchange 104
    docs/primers 6 · docs/history 52 · scripts 67 · (repo root) *.md 64
    absent           : drops/operator-exports
    absent           : exchange/drops/operator-exports
members to archive: 324
  compressing...      compressed 324/324
  verifying (bidirectional)...   verified 324/324

FIXTURES
  PASS F-K1 - 324/324 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  N/A  F-K2 - completeness vs census.json applies to --estate only
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to …Temp\… outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 b083ccd066bc8d53... matches=True,
              sidecar matches=True, CRC clean=True, 324 members
  PASS F-K6 - default refuses; --force-same-day yields naiad_workflow_2026-08-12-01.zip
              while naiad_workflow_2026-08-12.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 318/318 git-tracked source files still present on disk; 0 missing

archive   : D:\naiad-backups\naiad_workflow_2026-08-12.zip
size      : 2,749,895 B (2.6 MB, 28.1% of source)
sha256    : b083ccd066bc8d5383b5c567407edbadefe7a48ede219797d6a70f8be7b7992a
members   : 324
sidecar   : D:\naiad-backups\naiad_workflow_2026-08-12.zip.sha256

8/8 fixtures pass

PUBLISH
  publish: routine last completed 2026-08-12 (3h ago)
  publish: committed 44a2abc (6 path(s)) and pushed to origin/v12-v1-census
```

**Member count 324. The 0-mismatch line: `0 mismatches, 0 strays, 0 omissions`.**
"Bidirectional" means each member was hashed twice — once streamed out of the zip, once re-read
fresh from the source on disk — and both had to equal the fingerprint recorded in the archive's own
manifest.

Re-verified afterwards in a **separate process**, reading only the destination:

```
  members: 324 · verified: 324 · mismatches: 0 · strays: 0 · omissions: 0
  archive sha256: b083ccd066bc8d5383b5c567407edbadefe7a48ede219797d6a70f8be7b7992a
  VERIFIED
```

**Two lines in that transcript look alarming and are not.** `REFUSING TO CLOBBER` appeared twice —
that is fixture **F-K6 deliberately testing the no-clobber guard** against the archive it just
wrote, plus a probe file it creates, back-dates, tests and removes. Both passed. They print first
only because error output is unbuffered. I confirmed no probe file and no `-01` file were left
behind.

`--estate` was **not** run this session, by instruction. `--workflow` proves the path in seconds;
`--estate` would move 472 MB.

---

## 5 · The publish and the commit

- **Publish:** `44a2abc`, 6 paths, **pushed to `origin/v12-v1-census`** — succeeded. F-P6 freshness
  line present (`routine last completed 2026-08-12 (3h ago)`). **No budget WARNING.**
- **Code commit:** `0509912`, exactly 2 files. **Committed, not pushed** — standing commit-no-push
  rule for code; only `exchange/**` auto-pushes. `.gitignore` was already modified before this
  session began and is not mine; I left it uncommitted.
- This report and the ledger entry are published by a second `publish()` after this file is
  written. Two publishes, because the `--workflow` run performs one of its own.

---

## 6 · File disposition

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/backup_estate.py` | yes | tracked | `0509912` | **no** — commit-no-push | GitHub *(after push)* + `naiad_workflow_2026-08-12.zip` | 65,440 B · 0.98% |
| `scripts/routine_jobs.json` | yes | tracked | `0509912` | **no** — commit-no-push | GitHub *(after push)* + workflow archive | 1,773 B · 0.03% |
| `exchange/status/CONVENTIONS.md` | yes | tracked | `44a2abc` | yes, `origin/v12-v1-census` | GitHub + workflow archive | 52,994 B · 0.79% |
| `exchange/status/CADENCE.md` | yes | tracked | `44a2abc` | yes | GitHub + workflow archive | 7,503 B · 0.11% |
| `exchange/status/SECOND_ACCOUNT.md` | yes | tracked | `44a2abc` | yes | GitHub + workflow archive | 2,941 B · 0.04% |
| `exchange/status/RETENTION.md` | yes | tracked | `44a2abc` | yes | GitHub + workflow archive | 1,766 B · 0.03% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | pending 2nd publish | pending | GitHub + workflow archive | 26,728 B · 0.40% *(was 23,968 B; +2,760 B for this session's STATUS entry)* |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_BACKUP-PATH-REROUTE.md` | yes | untracked → tracked at 2nd publish | pending | pending | GitHub after publish | 30,463 B · 0.45% |
| `D:/naiad-backups/naiad_workflow_2026-08-12.zip` | yes | n/a — off-machine | n/a | n/a | **the archive itself; off-repo** | `n/a` — lands on `D:`, unsynced by the box |
| `D:/naiad-backups/naiad_workflow_2026-08-12.zip.sha256` | yes | n/a | n/a | n/a | sidecar for the above | `n/a` — `D:` |

`exchange/` total after this session: **1,486,299 B ≈ 22.2%** of the 6.39 MB box. No artifact this
session exceeds 1% except `backup_estate.py`, which is code and does not enter the box.

---

## 7 · OPEN ITEMS — and the answer you asked me to state plainly

### **Do the estate archives have any copy OUTSIDE `D:`?**

> **No copy that I can prove. Treat the four `naiad_estate_*.zip` generations — 1.85 GB of
> irreplaceable price data — as existing in exactly one place right now: the LaCie disk on your
> desk.**
>
> Three routes off that disk, and all three are currently unproven or stale:
> 1. **`G:/My Drive/naiad-backups` — empty. 0 files.** Measured. The old cloud copy is gone.
> 2. **The Drive mirror of `D:/naiad-backups` — registered but erroring.** §2.3. Fifty
>    `CreateHardLinkW failed` entries, no completion record, exFAT cannot do hard links.
> 3. **The second Google account — stale.** `SECOND_ACCOUNT.md` records
>    `last_manual_upload: 2026-08-05`. The two newest estate generations, **`2026-08-09` and
>    `2026-08-11`, postdate it and have never been manually uploaded.**
>
> The archives themselves are healthy — all 20 verified this session. The risk is not corruption.
> **It is that there is one copy, on one external disk, in one room.**

**O-1 · Confirm or refute the Drive mirror. Owner: operator. Thirty seconds, and it settles §2.**
Open `drive.google.com` → left sidebar → **Computers** → your machine. If `naiad-backups` is there
with the archives, the mirror works and item O-1 closes. If it is absent or partial, the exFAT
hard-link failure is real and the fix is a decision: reformat `D:` to NTFS (destructive, needs the
archives moved first — **not something I will do without an explicit instruction**), or keep `G:`
as a second destination, or rely on the second-account upload.

**O-2 · The Sunday backups still write to the old folder. Owner: operator.** Both tasks pass
`--dest "G:\My Drive\naiad-backups"` explicitly, and an explicit `--dest` outranks the new default
by design. Next fire **2026-08-16 08:00 and 08:30**. Left unchanged because editing Windows
scheduled tasks is outside the repository, outside the contract's stated edit list, and outside its
`git revert` rollback — and because, if O-1 comes back negative, keeping `G:` as a destination may
be the *safer* configuration, not the stale one. **This is a genuine fork and it is yours.** The
decision funnel is in §8.

**O-3 · Both weekly tasks last ran 2026-08-09 and returned exit code 1 — a failure — and nobody
looked.** The archives were written (both dated 08-09 exist and verify), so the failure came after
the fixtures, most likely in the publish step. Unexamined; out of this session's scope.

**O-4 · `RETENTION.md` reports "PHASE ARCHIVES — none found" while nine exist.** Reported, not
fixed. `retention_report()` looks in `research_outputs/_archive` inside the repo, but ruling B
(2026-08-06) moved phase archives to `D:/Naiad/research_outputs/_archive`, where I confirmed nine
are present. The retention report tells the truth about estate and workflow generations and is
blind about phases. Pre-existing; I did not introduce it and did not touch it.

**O-5 · `D:/naiad-backups/operator-exports` does not exist**, so `daily_routine.py` will now raise
*"operator-exports folder missing"* against the new destination. Correct behaviour, newly visible.
Create the folder or accept the alert.

**O-6 · Three `(1)`-suffixed duplicate zips on `D:` have no sidecar** and cannot be verified. Each
matches its verified twin in size. No delete authorization existed; nothing was removed.

**O-7 · `D:\Naid-GDRIVE` is the *second* Drive-mirrored folder** named in the registry — a 4.2 GB,
9,522-file copy of the naiad tree, complete with `.git`. Unexplained, and worth a decision: it is
either a deliberate second clone or a stray duplicate consuming mirror bandwidth. Note its name is
`Naid`, not `Naiad`. I read it only; `git` refuses to report its branch because exFAT records no
ownership, and I declined to add a global `safe.directory` exception to find out.

---

## 8 · The decision in front of you — O-2, in the §1.1 format

**WHAT IS IT.** Your two automatic Sunday backups still name the old folder. The code now defaults
to the new one, but the tasks override the default by naming a destination outright — that override
is deliberate, so that changing a default can never silently redirect somebody's backup.

**WHY IT MATTERS.** On Sunday 2026-08-16 the estate backup writes ~472 MB into
`G:/My Drive/naiad-backups` and the workflow backup follows. Nothing is lost — but from then on your
archives live in two places and the retention counts in both are wrong. It needs your judgment
rather than mine because the right answer depends on O-1, which only you can check.

**OPTIONS.**
1. **Check O-1 first, then decide** *(my recommendation)*. If the mirror works, drop `--dest` from
   both tasks and everything follows the new default. If it does not, `G:` is currently your only
   working cloud path and you may want to keep it.
2. **Repoint both tasks to `D:` now.** Everything consolidates immediately. If the mirror is broken,
   you have consolidated onto a single un-backed-up external disk.
3. **Keep both destinations** — leave the tasks on `G:` and let manual runs use the `D:` default.
   Belt and braces, at the cost of two divergent archive sets and a retention report that describes
   neither completely.
4. **Change nothing.** Sunday writes to `G:`, and you decide later with more information.

**IMPLICATIONS.** Option 1 costs thirty seconds and removes the guesswork; it is the only option
that decides on evidence rather than on assumption. Option 2 is right *if and only if* the mirror
uploads. Option 3 is the most robust against being wrong and the most confusing to read later.
Option 4 is safe for one week and then this same decision returns, with an extra 472 MB attached.

**I need one instruction to act on any of these**, and I will not touch Task Scheduler without it.

---

## 9 · What I did not do

No file, archive or folder was deleted, moved or renamed anywhere, on any drive.
`G:/My Drive/naiad-backups` was read only, and is exactly as I found it — empty.
`--estate` was not run. Task Scheduler was read, never modified. The three `(1)` duplicates and the
two `D:` mirror folders are untouched.

**ROLLBACK.** `git revert 0509912` restores the previous script behaviour. The new archive
`D:/naiad-backups/naiad_workflow_2026-08-12.zip` is additive — nothing was overwritten to create it.

---

## 10 · STATUS

```
=== STATUS_ATHENA — 2026-08-12 ===
NOW: The backup destination is repointed in code. Repo integrity is green where it now sits — fsck
clean, 544/544 tracked files present, zero dehydrated — and all 20 archives on D:/naiad-backups
verify against their sidecars with zero mismatches. --estate/--workflow now default to
D:/naiad-backups and HALT if the drive is absent; explicit --dest still wins, which is why the two
Sunday tasks still target G: and need an operator decision.
LAST EVENT: 2026-08-12 — live --workflow run wrote naiad_workflow_2026-08-12.zip to the new default,
324 members, 8/8 fixtures, 0 mismatches; published 44a2abc, code committed 0509912.
FACTS:
- Sync idle: repo and D:/naiad-backups byte-identical across a 60s double measurement; git fsck clean; HEAD == origin at 7552d652eb… [verified]
- 20/20 archives on D: verified against sidecars, 0 mismatched, 3 unverifiable (1)-suffixed duplicates with no sidecar [verified]
- G:/My Drive/naiad-backups is EMPTY, 0 files — the move was a move, not a copy [verified]
- D:\naiad-backups IS a registered Google Drive mirror target, decoded from the DriveFS SyncTargets registry protobuf, and D: is a physical LaCie exFAT disk, not a Drive mount [verified]
- Its uploads are ERRORING: 50 CreateHardLinkW failures naming these archives, no completion record; exFAT has no hard links. Registered is not uploaded [verified]
- No provable copy of the four estate generations exists outside D:; second-account upload is stale at 2026-08-05, predating the 08-09 and 08-11 generations [verified]
PENDING:
1. Operator: check drive.google.com > Computers for naiad-backups — settles whether the off-site copy exists (O-1)
2. Operator: rule on the two Sunday tasks, which still pass --dest "G:\My Drive\naiad-backups"; next fire 2026-08-16 (O-2, funnel in §8)
3. ATHENA: both weekly tasks returned exit 1 on 2026-08-09, unexamined (O-3)
4. ATHENA: retention_report() reports "no phase archives" while nine exist at D:/Naiad/research_outputs/_archive (O-4)
5. Operator: D:\Naid-GDRIVE — a second 4.2 GB Drive-mirrored copy of the tree; deliberate or stray? (O-7)
NEXT: Check Computers in the Drive web UI, then rule on item 2. Owner: operator.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===
```

**Operator action after this: click Sync now.**
