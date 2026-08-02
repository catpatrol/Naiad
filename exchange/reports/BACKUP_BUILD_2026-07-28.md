# BACKUP BUILD REPORT — 2026-07-28

Environment: local Windows Claude Code, working Naiad clone.
Deliverable: `scripts/backup_estate.py`, built against the reference implementation recorded in `LEDGER.md:743-757` ("2026-07-27 — Estate protection established").

**One commit created. Nothing pushed. No source file was deleted by anything in this task.**

---

## STEP 0 — asserts

| assert | expected | actual | result |
|---|---|---|---|
| working directory | naiad repo root | `/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad` | **PASS** |
| `git status --porcelain` modified tracked files | none | none (12 untracked only) | **PASS** |

HEAD at start: `97f0eee`.

---

## The build

`scripts/backup_estate.py`, 614 lines, standard library only apart from the single `engine.data.cache_dir()` import that Mode A is explicitly permitted.

### How the reference run was reproduced

The ledger entry fixes the pattern, and each element is implemented literally:

| ledger element | implementation |
|---|---|
| estate resolves through `engine/data.py:39-48 cache_dir()`, `NAIAD_CACHE_DIR` honoured (`LEDGER.md:744`) | `run_estate()` imports and **calls** `cache_dir()`; no path is hardcoded. The override is read and recorded in the manifest as `naiad_cache_dir_override`. |
| census.json stores **relative** paths only, so it cannot pin a location (`LEDGER.md:744`, and the amendment demanded at `LEDGER.md:762` item 3) | census.json is used **only** for the F-K2 completeness check, resolving its relative `path` fields *through* the estate root. It is never consulted for location. |
| bidirectional verification — member re-read out of the zip hashed equal to source on disk, **and** each embedded pin agreeing with zip content (`LEDGER.md:745`) | `verify_archive()` performs exactly these two comparisons per member, plus a `testzip()` CRC pass. |
| set membership cross-checked in all directions, no strays, no omissions (`LEDGER.md:748`) | zip ↔ manifest ↔ disk compared three ways; `strays` and `omissions` are reported separately and any non-zero count fails F-K1. |
| per-phase atomic, sources freed before the next phase begins (`LEDGER.md:748`) | `--phase` handles exactly one phase per invocation; the source is released only after zero mismatches, and only when explicitly authorised (below). |
| tracked files preserved in place (`LEDGER.md:756`) | `git ls-files` drives F-K7; tracked files are archived **and** left on disk under every setting. |
| dated, non-overwriting archives (ruling R-B, `LEDGER.md:758`) | `assert_no_clobber()` halts on an existing target or sidecar; F-K6 proves the guard trips. |

### Stated deviation — deletion is opt-in

The spec's INVARIANTS say *"Never deletes; local deletion is a separate operator action"*, while MODE B says *"delete only untracked files, and only after zero mismatches."* These conflict. Resolution: deletion is gated behind an explicit **`--delete-source`** flag. Without it, `--phase` archives, verifies, and reports how many untracked files *would* be releasable. With it, and only after zero mismatches, untracked files are released while every git-tracked file is preserved.

This follows the project's own precedent: at `LEDGER.md:756` the builder "halted and asked rather than proceeding" when deletion would have touched tracked files. The estate is never deleted by this script under any flag. **No deletion path executed in this task** — no `--phase` run was performed.

### Defect found and fixed during the build

The first estate run failed immediately:

```
ModuleNotFoundError: No module named 'engine'
```

Running `python scripts/backup_estate.py` places `scripts/` on `sys.path`, not the repo root, so the Mode A import could not resolve. Fixed by adopting the convention already used at `scripts/daily_brief.py:57`, `scripts/census_build.py:47` and `scripts/tc5_runner.py:23` — `sys.path.insert(0, str(REPO))` immediately after `REPO` is defined. The failure occurred at the import, before any read or write, so nothing was written to the destination; verified the destination was still empty before re-running.

The `--verify` smoke test had already passed at that point because it never imports `engine` — which is why the gap did not surface earlier.

---

## Step 2 — live smoke test, `--verify` against `tc4_2026-07-27.zip`

```
archive : research_outputs\_archive\tc4_2026-07-27.zip
mode         : ?/tc4
created_utc  : 2026-07-27T07:01:43+00:00
members      : 1509
verified     : 1509
mismatches   : 0
strays       : 0
omissions    : 0
archive sha256: 794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933

VERIFIED
```

| check | expected | actual | result |
|---|---|---|---|
| members | **1,509** | **1,509** | **exact** |
| mismatches | **0** | **0** | **exact** |
| archive sha256 | `794036c2d6135285…` per `LEDGER.md:754` | `794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933` | **matches the ledger pin** |

This is stronger than the stated bar. The specification asked only for member count and mismatch count; the archive's own sha256 independently reproduces the value the ledger recorded on 2026-07-27, so the new verifier agrees with the manual run on a fifth independent path beyond the four already logged at `LEDGER.md:757`.

`mode : ?` is expected and harmless — the 2026-07-27 manual manifests carry `phase` but no `mode` key. The verifier reads foreign manifests without complaint, which is the desired backward compatibility.

---

## Step 3 — `--estate --dest "G:\My Drive\naiad-backups"`

Destination located per the previous task: `G:\My Drive` is a streaming Drive for Desktop mount; `naiad-backups` was created there and was empty before this run.

```
estate root      : C:\Users\luisf\AppData\Local\naiad\data_cache
NAIAD_CACHE_DIR  : (unset)
inside OneDrive  : False
destination      : G:\My Drive\naiad-backups\naiad_estate_2026-07-28.zip
members to archive: 73
```

| item | value |
|---|---|
| **archive** | `G:\My Drive\naiad-backups\naiad_estate_2026-07-28.zip` |
| **size** | **492,306,779 B** (469.5 MB, **75.5%** of source) |
| **sha256** | `ad94dc6e1e6750bb8c58e611f5bff11e877b1cc66ef7678efc3e8b252e63be12` |
| **members** | **73** |
| source bytes | 652,451,079 |
| sidecar | `naiad_estate_2026-07-28.zip.sha256` (95 B) |
| estate inside OneDrive | **False** — confirms the superseded risk note at `LEDGER.md:744` |

**Member composition:** 70 estate files (60 klines + 10 funding) plus the 3 required companions — `census.json`, `DATA_CENSUS.md`, `research_outputs/census/build_manifest.json`, stored under a `_repo/` prefix so they cannot collide with estate paths. The manifest records `estate_root` and `repo_root` separately so verification resolves each member against the right root.

**Reconciliation against the 2026-07-27 baseline.** The ledger records 71 estate files / 633.5 MB; today the tree holds 70 files / 622.2 MB. The difference is accounted for exactly: the orphaned `ZECUSDT_1m.parquet.4100.tmp` (12,563,190 B) was deleted during the 2026-07-27 cleanup (`LEDGER.md:747`), and daily top-ups have since added back roughly 0.7 MB. Compression ratio is stable at 75.5% against last run's 75.4%.

### Fixture transcript

```
FIXTURES
  PASS F-K1 - 73/73 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to C:\Users\luisf\AppData\Local\Temp\... outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 ad94dc6e1e6750bb... matches=True, sidecar matches=True, CRC clean=True, 73 members
  PASS F-K6 - guard refuses to overwrite the archive just written
  PASS F-K7 - 3 git-tracked source files still present on disk; 0 missing

7/7 fixtures pass
ESTATE_EXIT=0
```

**Reading note on the transcript.** The run's captured output opens with `REFUSING TO CLOBBER: …naiad_estate_2026-07-28.zip already exists.` That is **not an error** — it is F-K6 deliberately firing the no-clobber guard against the archive just written, to prove the guard works. It appears first only because stderr is unbuffered while stdout is not. F-K6 is recorded PASS on exactly that behaviour.

---

## Step 4 — post-upload re-read after 60 s

Slept 60 s to let Drive finish uploading, then re-verified from the Drive path:

```
-rw-r--r--  492306779  Jul 28 21:20  naiad_estate_2026-07-28.zip
-rw-r--r--         95  Jul 28 21:20  naiad_estate_2026-07-28.zip.sha256

archive : G:\My Drive\naiad-backups\naiad_estate_2026-07-28.zip
mode         : estate
created_utc  : 2026-07-29T00:18:45Z
members      : 73
verified     : 73
mismatches   : 0
strays       : 0
omissions    : 0
archive sha256: ad94dc6e1e6750bb8c58e611f5bff11e877b1cc66ef7678efc3e8b252e63be12

VERIFIED
```

The archive sha256 is **byte-identical to the value computed at write time**, and all 73 members re-verify against their embedded pins after the upload settled. The file on Drive is sound.

---

## Step 5 — commit

```
[v12-v1-census 837c635] ops: backup_estate.py — dated hashed estate/phase archives (F-K1..7 pass)
 1 file changed, 614 insertions(+)
 create mode 100644 scripts/backup_estate.py
```

**HEAD:** `837c6353f4410a55ae6d97bb6367a3dee769e670` (`837c635`)
**Not pushed** — `## v12-v1-census...origin/v12-v1-census [ahead 2]`

```
$ git status --porcelain
?? "# ORCHESTRATOR PRIMER \342\200\224 what a fresh orchestrator session needs to know.txt"
?? "12-25EMA Trend Scanner-Pinescript.txt"
?? CONTRACT_ANALYTICS1_BRIEF2_FORWARD0_draft.md
?? HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md
?? HANDOFF_2026-07-27_BRIEF_to_ENGINE.md
?? "Naiad \342\200\224 Orchestrator Control Center.html"
?? Naiad_Orchestration_and_Open_Questions.md
?? "ORCHESTRATOR CONTROL CENTER \342\200\224 protocol & state of record.txt"
?? "Rvwap pine code.txt"
?? "STATUS \342\200\224 BRIEF (daily market brief \302\267 Atlas HTML report \302\267 live laboratory).txt"
?? "STATUS \342\200\224 ENGINE (engine builds \302\267 repo operations \302\267 integrity & manifest).txt"
?? scripts/orchestrator_state.py
```

Only `scripts/backup_estate.py` was staged, by explicit path. The 11 pre-existing untracked root files and `scripts/orchestrator_state.py` were left alone. No tracked file is modified.

```
$ git log --oneline -3
837c635 ops: backup_estate.py — dated hashed estate/phase archives (F-K1..7 pass)
97f0eee ops: daily routine + venv repoint to C:\venvs\naiad + restore test fixture data
268cdf9 docs: estate protection, OneDrive quota root cause, 19.61 GB reclaimed, rulings R-A/R-B/R-C
```

---

## Observations

1. **This is the second offsite generation, and the first automated one.** Ruling R-B requires dated non-overwriting archives so generations accumulate; `naiad_estate_2026-07-28.zip` now sits beside the manual 2026-07-27 copies held on the two operator Drive accounts. The no-clobber guard makes accidental generation loss structurally impossible rather than merely discouraged.
2. **Drive headroom is the near-term constraint.** Each estate generation costs ~470 MB against 13.14 GB free, so roughly 27 generations fit before the account fills — fewer once phase archives (~1.0 GB) are copied across. A retention rule should be decided before this is scheduled, not after. Nothing in the script prunes anything, by design.
3. **`--phase` has been exercised for verification only.** Its archive-and-release path is implemented and fixtured but has not been run against a live phase directory in this task; the only phase interaction was the read-only `--verify` smoke test. First real use should be on a phase that is already archived, so the output can be diffed against a known-good zip.
4. **`scripts/orchestrator_state.py` is still untracked and still not mine** — the third foreign file to appear today, alongside the orphaned `index.lock` found in the previous task. Something else is writing to this working tree. F-K3 guards against it corrupting a run (git porcelain is compared before and after, and it was identical), but the underlying cause remains unresolved.
