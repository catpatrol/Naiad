# BUILDER'S REPORT — HEPHAESTUS — QUEUE 005 M2 v2 — THE RESTORE, EXECUTED

**Date:** 2026-08-15
**Host:** Luiss-MacBook-Pro.local (Mac17,6 / M5 Max / macOS 26.3)
**Ruling in force:** DATA RESIDENCY v2 (operator, 2026-08-15) — everything local under `~/Naiad`;
the LaCie is BACKUP ONLY. This supersedes the earlier preamble's framing in which the substrate
resolved on `/Volumes/LaCie` and the local copy was a temporary arrangement.
**LaCie posture this session:** READ-ONLY. Nothing on it was written, moved, renamed, deleted or
reorganised. Ruling "NOTHING ON THE LACIE MAY BE REORGANISED UNTIL M3 ACCEPTS" was honoured.

---

## VERDICT IN ONE LINE

**M2 ran to completion for the first time.** All three prior blockers are gone, the full substrate
set is restored and hashed, the estate is live, and the Mac suite now reads **287 passed / 0 failed**
— but only **78.8% of the restored corpus carries external attestation**, and the headline
"0 mismatches" must not be read as "everything is verified."

---

## 0 — GATE 0: ALL THREE HALTS CLEARED

The 2026-08-14 drill halted at gate 0 with three standing blockers. Their status now:

| Halt | 2026-08-14 state | Now | How |
|---|---|---|---|
| HALT 1 — missing `requirements-lock-2026-08-14-win.txt` | DEGRADED | **still degraded, non-blocking** | `requirements.txt` is fully pinned; unchanged this session |
| HALT 2 — LaCie not attached | **BLOCKING** | ✅ **CLEARED** | Drive is mounted at `/Volumes/LaCie` (3.6 Ti, 111 Gi used) |
| HALT 3 — no Python ≥3.10 | RESOLVED 2026-08-14 | ✅ holds | `~/venvs/naiad/bin/python` = 3.12.14 |
| HALT 4 — no GitHub credentials | **BLOCKING** | ✅ **CLEARED** | `~/.ssh/known_hosts` did not exist; created with GitHub's three host keys after verifying all three fingerprints against the published set. Remote is SSH. Push succeeded: `db63b8c..a39508b` |

HALT 4's fix is worth one line of detail because it was diagnosed wrongly-shaped before: the failure
was never a *credential* failure at the HTTPS layer as first recorded — on this SSH remote it
presented as `Host key verification failed`, because the Mac had **no `known_hosts` file at all**.
Nothing was overwritten to fix it.

---

## 1 — `.PYC` PURGE (§1)

Executed as authorised: `find . -name '__pycache__' -type d -not -path './.git/*' -exec rm -rf {} +`

```
BEFORE:  6 __pycache__ dirs · 73 .pyc · 31 embedding literal C:\Naiad
AFTER :  0 __pycache__ dirs ·  0 .pyc
```

**31 confirmed by direct inspection** (`strings <f> | grep 'C:\Naiad'`), exactly matching the figure
recorded in commit `5a6cd74`. Git saw no change — all were already ignored.

After the suite run, **60 fresh `.pyc` regenerated, of which 0 embed `C:\Naiad`.** The stale-bytecode
defect that caused a Windows absolute path to print on macOS is closed, and closed *demonstrably*
rather than by assertion.

---

## 2 — SUBSTRATE RESTORE (§2) — THE ADOPTION TABLE (§3.1)

Direction: **FROM `/Volumes/LaCie` INTO `~/Naiad`**, permanent home per v2. Method: `rsync -rt
--ignore-existing` (COPY-ONLY, NO-CLOBBER). Verification order applied as issued:
**sidecar > manifest > two-witness > single-witness-flagged.**

| folder | local | LaCie | basis used | verified | mismatch | verdict |
|---|---|---|---|---|---|---|
| `_archive` | 19 | 18 | **sidecar** (9) + two-witness (9) + git (1) | 19 | 0 | ADOPTED FLAGGED |
| `census` | 7 | 7 | manifest (4) + two-witness (3) | 7 | 0 | **ADOPTED CLEAN** |
| `census2a` | 82 | 82 | manifest (44) + two-witness (38) | 82 | 0 | ADOPTED FLAGGED |
| `census2b` | 261 | 261 | manifest (260) + two-witness (1) | 261 | 0 | **ADOPTED CLEAN** |
| `mc1` | 30 | 30 | manifest (8) + two-witness (22) | 30 | 0 | ADOPTED FLAGGED |
| `seq8` | 15 | 15 | manifest (5) + two-witness (10) | 15 | 0 | ADOPTED FLAGGED |
| `seq8_run2` | 11 | 11 | manifest (5) + two-witness (6) | 11 | 0 | ADOPTED FLAGGED |
| **TOTAL** | **425** | **424** | — | **425** | **0** | 2 clean · 5 flagged · 0 incomplete · 0 failed |

**425 vs 424** is `_archive/POINTER.md`, git-tracked and correctly local-only. Not a missing file.

**The three folders the 2026-08-14 report called "unrecoverable without the LaCie" are recovered:**
`census2a` (82), `census2b` (261), `seq8_run2` (11). That was the material loss the halt existed to
protect. It is closed.

**Every one of the 425 files was hashed on both sides.** The >200 MB partial-hashing allowance was
available in four folders and declined in all four. ~7.45 GB (7,448,790,676 B) read locally, plus the
same again on the LaCie.

### `_archive` reached the gold standard — and it is the only folder that did

The 9 `.sha256` sidecars in `research_outputs/_archive/` are **git-tracked and byte-identical to
HEAD** (`git status --porcelain` on that path is empty). So git itself — clean tree at the origin tip
— proves the sidecars, and those sidecars attest the 9 restored zips. That is verification basis (1)
*repo-tracked sidecar*, the standard the 2026-08-14 report correctly said `naiad-backups` could not
reach. Using `--ignore-existing` is what made it possible: it preserved the tracked sidecars instead
of overwriting them with LaCie copies.

Corroborated three ways — sidecar attestation = local bytes = independently hashed LaCie bytes — on
all 9 archives.

---

## 3 — WHAT IS PROVEN vs WHAT IS MERELY PRESENT

**This is the section that matters, and it is the one a reader skimming for "0 mismatches" will
skip.** *Hashed* is not *attested*:

- **Externally pinned** — a document written independently of this restore records the expected
  digest and the local bytes match. Detects corruption **and substitution**.
- **Two-witness only** — two copies agree with each other. Detects transport/media corruption and
  **nothing else**, because both witnesses inherit any error present when the backup was made.

| proof class | files | share | what it rules out |
|---|---|---|---|
| sidecar/manifest-pinned **and** LaCie-corroborated | 335 | 78.8% | corruption, truncation, substitution |
| two-witness agreement only | 89 | 20.9% | transit/media corruption — nothing else |
| git HEAD (`POINTER.md`) | 1 | 0.2% | working-tree drift |

**By bytes it is worse than by count.** The largest artifact in the estate,
`seq8_cascades.jsonl` (789,501,107 B), is pinned by **neither** seq8 manifest — and it exists twice.
**At least ~1.58 GB of the 7.45 GB rests on two-witness agreement alone**, before counting mc1's 22
unpinned files or census2a's 38.

**⚠️ `basis: manifest` is a maximum, not a coverage claim.** In `mc1` it describes 8 of 30 files; in
`seq8`, 5 of 15. Anyone treating the folder-level basis as applying to the folder overstates the
evidence by a wide margin.

Per folder, plainly:

- **`census2b` — genuinely proven.** 260 of 261 pinned by a 92 KB manifest generated 2026-08-14. The
  manifest cannot self-attest; that one-file gap is irreducible, not a caveat about the data.
- **`census` — proven.** 4 data files (99.99% of 218 MB) pinned, row counts independently reconciled
  against actual line counts — truncation ruled out by a second mechanism.
- **`_archive` — proven, strongest chain in the set.** See above.
- **`census2a` — half proven.** 44 pinned (primary 29-artifact set 29/29). The other 38 —
  `viz/*.html` ×10, `viz_payloads/*.json` ×9, `DESIGN_HANDOFF/*` ×11, 4 manifests, run log, 3
  `mc2/*.txt` — are present and mutually consistent, **not attested**.
- **`seq8` — mostly present, not proven.** 5 of 15 pinned; the unpinned 10 include the largest file
  in the estate. Calling this folder "manifest-verified" would misrepresent it.
- **`seq8_run2` — trust root is circular.** Its 5 pinned digests come from manifests that nothing
  external attests; the manifests' own integrity is two-witness only. A manifest corrupted before
  the backup would validate its own payload happily.
- **`mc1` — largely present, thinly proven.** 8 of 30 pinned (the `ops_klines` parquets). Separately,
  the payload's own header reads **"DISPLAY-ONLY — lockbox-era data — hypothesis generation only,
  never evidence."** The restore is sound; **a verified restore does not launder provenance.**

### Cross-folder finding no single verifier could see

**`seq8_run2` is a strict subset of `seq8`.** All 11 of its files have digests identical to their
`seq8` counterparts (`seq8_cascades.jsonl` `13195287…3507c` in both; `seq8_arrivals.json`
`16fef0c4…` in both; all 5 pinned digests identical). `seq8` holds 4 extra files
(`atlas_replication`, `extract_run1.log`, `fixture_transcript.txt`, `fixtures.json`) accounting for
the entire 22,642-byte difference. **~1.87 GB of the working tree is a byte-exact duplicate of
another part of the working tree.** Observation only — no deletion proposed, none performed.

---

## 4 — MISMATCHES AND NEAR-MISSES

**0 hash mismatches · 0 files missing locally · 0 genuine extras**, across 425 files and ~7.45 GB.

Three things a careless reader would score as failures and which are not:

### 🔴 `shasum -a 256 -c` FAILS ALL 9 `_archive` SIDECARS — AND THE RESTORE IS PERFECT

All 9 sidecars are **CRLF-terminated** (confirmed by `xxd`: `…7a69 700d 0a` = `.zip\r\n`). `shasum`
therefore searches for a filename with a trailing `\r`:

```
$ shasum -a 256 -c s1_2026-07-27.zip.sha256
shasum: s1_2026-07-27.zip: No such file or directory
s1_2026-07-27.zip: FAILED open or read

$ tr -d '\r' < s1_2026-07-27.zip.sha256 | shasum -a 256 -c -
s1_2026-07-27.zip: OK
```

**This is a live trap in the restore runbook.** The obvious verification command reports total
corruption on a flawless restore. Not fixed — the sidecars are git-tracked evidence and rewriting
them is an operator decision. Same Windows-artifact contamination class as the 31 stale `.pyc`.

### `du -sh` disagrees in four folders — ExFAT, not data loss

census2a 57M/77M · census 208M/209M · mc1 159120K/164352K · seq8_run2 1.8G/1.7G. The LaCie is ExFAT
(`diskutil info`); its large allocation unit inflates on-disk block usage for many small files. Exact
`stat` byte sums are **equal in every case** — census2a is 59,757,249 B on both sides. The ledger's
"~77M" figure for census2a came from the ExFAT reading; real logical size is ~57 MiB.

### A hash that reads like a stub, and is genuine

`analytics_tests_v1.0.0_2026-07-29.zip` → `0a1ffc94…e99999`. Independently recomputed from LaCie
bytes to the identical digest. Coincidence, not a stubbed sidecar.

---

## 5 — ESTATE CACHE (§5)

`cache_dir()` resolution stands unchanged: `NAIAD_CACHE_DIR` unset, `os.name != 'nt'` →
**`/Users/luis/.cache/naiad/data_cache`**. (Note the side effect ATHENA flagged: `engine/data.py:47`
mkdirs on read. The directory already existed when this session began.)

Restored `naiad_estate_2026-08-11.zip` — **and the provenance chain here is complete**:

```
LaCie sidecar f0cfdb2a…9822  ──attests──▶  local archive bytes (recomputed: match)
                                    │
                                    └──contains──▶ MANIFEST.json ──attests──▶ 73/73 files ✅
```

The sidecar read was the **LaCie's**, the bytes hashed were the **local** copy's. That is a genuine
independent-witness check — precisely what the 2026-08-14 session correctly refused to claim.

```
Extracted: 74 files · 627 MB · 60 klines + 10 funding parquets
Manifest verification: 73/73 OK · 0 mismatches · 0 missing
```

**APFS case-collision hazard: PROBED AND DOES NOT FIRE.** ATHENA logged the
`MANIFEST.json`/`manifest.json` collision as "UNEXERCISED and still live on APFS." Case-folding all
74 entries yields zero duplicates; the only manifests are `MANIFEST.json` and
`_repo/research_outputs/census/build_manifest.json`. Extracted with `unzip -n` (never overwrite).
**This clears the hazard for this archive only** — it is not a general all-clear.

### 🟡 The estate is 64 commits stale, and nothing newer exists anywhere

The manifest self-reports `repo_head = e835755c…`, which **is** in our history: *"exchange:
auto-publish 2026-08-11"*. HEAD is **64 commits ahead of it**, spanning all the census2b work
(`c246d0c`, `5ad72b7`, `bbe47ed`, `db63b8c`).

The 2026-08-14 report reasoned that "the LaCie almost certainly holds a newer one." **It does not.**
An exhaustive search of the entire volume (`find /Volumes/LaCie -iname 'naiad_estate*'`) returns four
generations — 07-28, 08-02, 08-09, 08-11 — each in two locations. **2026-08-11 is the newest estate
that exists on any medium.** The prediction was reasonable and is now falsified; recording it so the
next session does not go looking again.

Manifest also records its build host as `C:\Users\luisf\AppData\Local\naiad\data_cache` and repo root
under OneDrive — provenance of where it was made, not a defect.

---

## 6 — THE BASELINE, RETAKEN (§6)

Run per the ledger's M3 invocation note — plain `python -m pytest`, **not** `-q` (pytest.ini already
sets `addopts = -q`; passing it again double-quiets and silently suppresses the count line).

```
$ source ~/venvs/naiad/bin/activate && python -m pytest
287 passed, 1 skipped in 14.91s
```

| Run | Result | Total |
|---|---|---|
| Windows reference (Queue 004 A-5) | 287 passed / **1 failed** | 288 |
| Mac, empty estate (2026-08-14) | 282 passed / **4 failed** / 2 skipped | 288 |
| **Mac, restored estate (2026-08-15)** | **287 passed / 0 failed** / 1 skipped | **288** |

**Totals hold at 288 across all three runs — no test lost or gained in the platform crossing.**

**All four data-starvation failures are resolved by the estate restore**, exactly as the provisional
baseline predicted they would be: the `WarmupError` "0 exec bars (need >= 2000)" at
`engine/replay.py:97` and the three `IndexError: index -1 … size 0` at `tests/test_analytics.py:908`.
The "LITUSDT 1m not in the estate" skip is also gone.

The one remaining skip is self-explaining and unrelated to the estate:
`fixtures/test_f8_journal.py:110 — dry-run journal not generated yet (D7)`.

**This Mac is now strictly better than the Windows reference** — Windows carried 1 failure, this host
carries 0. ATHENA PENDING #3 ("re-take the suite baseline after the estate is restored") is
discharged. The baseline is **no longer provisional.**

---

## 7 — §3: THE IN-REPO BACKUP VAULT — VERIFIED, NOT TOUCHED

The operator's condition was: *if it is the gigabyte-scale twin of the LaCie backup root, it violates
v2's one-role rule.*

**It is the twin — proven, not inferred.** `~/Naiad/naiad-backups` is **51/51 byte-identical** to
`/Volumes/LaCie/naiad-backups` across ~2.9 GB. Full-coverage SHA-256, nothing sampled, including all
four ~490 MB `naiad_estate_*.zip` files. Tree shape matches too — the local side **does** have
`phases/`, contrary to expectation.

**A third copy exists** at `/Volumes/LaCie/Repo Clone/naiad-backups` — also 51/51 identical, holding
**nothing unique**. A clean negative finding, stated because a negative is a real result.

Total audit: **153 files / ~8.7 GB hashed across three trees. 0 mismatches.**
Sidecar checks independent of the LaCie comparison: **33 checks, 0 mismatches** (24 vault + 9 `_archive`).

### What this proved that the 2026-08-14 check could not

That session verified 15 archives against their own sidecars and **correctly declined to call it
proof**: archive and sidecar arrived in the same unverified bulk copy, so they were *one witness
attesting to itself* — and a sidecar written from already-corrupt bytes verifies perfectly. This run
supplies the physically separate second witness, and it agrees on every byte. The earlier result is
**corroborated rather than merely self-consistent.** The earlier session's refusal to overclaim is
vindicated, not overturned.

### The three `" (1)"` redownloads — resolved

All three are byte-identical to their sidecar'd twins, so they inherit a verified fingerprint exactly:

| file | sha256 | bytes |
|---|---|---|
| `analytics_tests_v1.0.0_2026-07-29 (1).zip` | `0a1ffc94…99999` | 6,816 |
| `analytics_v1.0.0_2026-07-29 (1).zip` | `d3fcd786…a3d9` | 19,641 |
| `naiad_workflow_2026-08-02 (1).zip` | `fcc260f8…f4f8` | 1,132,236 |

Duplicates in the strict sense — zero unique information, ~1.16 MB total. Integrity not in doubt.

### 🔴 RECOMMENDATION — ADVICE ONLY. NOTHING DELETED. AWAITING THE OPERATOR'S WORD.

1. **The one-role question is answered affirmatively.** An in-repo gigabyte-scale backup vault is a
   v2 violation on its face. Retiring it is **safe on content**: every one of the 51 files provably
   exists byte-identically in at least two other places. Nothing there is unique.
2. **⚠️ BUT ONE-ROLE AND 3-2-1 POINT IN OPPOSITE DIRECTIONS HERE.** The two surviving copies are on
   **the same physical LaCie spindle**, and their matching directory mtimes (Aug 11 23:48) suggest
   one was copied from the other. Retiring the in-repo vault moves the estate from **3 copies on 2
   devices to 2 copies on 1 device** — a real loss of disaster resilience, not tidiness.
   **The sequence I would not reorder:** (a) establish a second-device copy → (b) verify it →
   (c) *only then* retire `~/Naiad/naiad-backups` → (d) leave `research_outputs/_archive` intact →
   (e) amend `POINTER.md`. **Step (a) before step (c).** This should be resolved deliberately, not as
   a side effect of a cleanup.
3. **`research_outputs/_archive` should be assessed separately and, on this evidence, KEPT** — it
   exists by operator ruling B, `POINTER.md` designates the archives permanent evidence and never
   prunable, and it is the target of the canonical tracked sidecars. If only one in-repo copy of the
   phase zips is wanted, `_archive` is the sanctioned one and the vault's `phases/` is redundant —
   the reverse would discard the copy with a mandate.
4. Advisory housekeeping, no action taken: ~19.6 MB of the vault is internal self-duplication (`tc5`
   and both analytics zips stored at both top level and in `phases/`), present identically on all
   three copies and therefore not local corruption.
5. **Neither pile is in git history** (`.gitignore` `naiad-backups/` and `*.zip`). ~3.9 GB of
   untracked bulk: no history rewrite would ever be needed to remove it, but it is equally **not
   protected by git** — there is no recovery path if it goes.

---

## 8 — §4: DRIVE-LITERAL SWEEP — M3'S INPUT

Read-only inventory across `scripts/`, `engine/ analytics/ study/`, `tests/ fixtures/`, and
`*.md docs/ exchange/ research_outputs/**/*.json`. **43 real defects · 38 doc-only (excluded).**
Per v2 the replacement is a **repo-relative path, NOT a `NAIAD_DRIVE` root.**

### 🔴 Blocking on POSIX — these halt unconditionally on this host

| file:line | literal | why it halts |
|---|---|---|
| `scripts/mc2_program.py:270` | `if OUT.drive.upper() != "D:"` | `Path.drive` is **always `""`** on POSIX → residency assert **can never pass** |
| `scripts/census2a_program.py:185` | `if OUT.drive.upper() != "D:"` | same |
| `scripts/mc2_program.py:236` | `cwd…endswith("c:/naiad")` | identity gate can never pass |
| `scripts/census2a_program.py:159` | `cwd…endswith(("c:/naiad","/c/naiad"))` | same |

Replace with an assert that `OUT` is under `ROOT/research_outputs`, and compare `Path.cwd()` to repo
ROOT.

### Hardcoded roots (repo-relative replacements)

| file:line | literal | → |
|---|---|---|
| `scripts/mc2_program.py:111` | `D_ROOT = Path("D:/Naiad/research_outputs/census2a")` | `research_outputs/census2a` |
| `scripts/mc2_program.py:263` | `wait_for_drive("D:/Naiad")` | `research_outputs` |
| `scripts/census2a_program.py:75` | `OUT = Path("D:/…/census2a")` | `research_outputs/census2a` |
| `scripts/census2a_program.py:181` | `wait_for_drive("D:/Naiad")` | `research_outputs` |
| `scripts/census2b_program.py:110` | `OUT = Path("D:/…/census2b")` | `research_outputs/census2b` |
| `scripts/census2b_program.py:112` | `CENSUS2A = Path("D:/…/census2a")` | `research_outputs/census2a` |
| `scripts/census2b_wtb1.py:102` | `C2A = Path("D:/…/census2a")` | `research_outputs/census2a` |
| `scripts/census2a_viz.py:28` | `B = Path("D:/…/census2a")` | `research_outputs/census2a` |
| `scripts/backup_estate.py:250` | `PHASE_ARCHIVE_ROOT_DEFAULT = "D:/…/_archive"` | `research_outputs/_archive` |
| `scripts/backup_estate.py:277` | `BACKUP_DEST_DEFAULT = "D:/naiad-backups"` | ⚠️ **must become an OFF-repo device path** — see §7; defaulting a backup target inside the repo is what created the one-role violation |
| `scripts/backup_estate.py:297` | `NO_WAIT_ANCHORS_DEFAULT = "G:\\"` | no POSIX equivalent; re-express or drop |
| `scripts/drive_wait.py:241` | `root = argv[0] if argv else "D:/Naiad"` | `research_outputs` |
| `scripts/routine_jobs.json:3` | `"python": "C:\\venvs\\naiad\\Scripts\\python.exe"` | venv-relative interpreter |
| `scripts/routine_jobs.json:9` | `"backup_dest": "D:\\naiad-backups"` | same caution as `backup_estate.py:277` |
| `scripts/setup_brief_schedule.ps1:66` | `$python = "C:\venvs\naiad\Scripts\python.exe"` | whole file is Windows-only |

### `%LOCALAPPDATA%` assumptions (7) — `KeyError` on macOS

`scripts/mc2_program.py:194` · `scripts/census2b_program.py:189` · `scripts/rc_recompute.py:1402` ·
`scripts/mc1_program.py:1968` · `scripts/backup_estate.py:431` (OneDrive probe) ·
`engine/data.py:43-44` — **`engine/data.py` is already correctly gated** behind `os.name == "nt"`
with a POSIX fallback; the four direct subscripts are **not** guarded.

### Windows-only APIs (7)

`scripts/setup_brief_schedule.ps1:169,171,181,190` (`schtasks`) ·
`scripts/reviewer_manifest.py:424` and `scripts/daily_routine.py:390`
(`tasklist /FI IMAGENAME eq OneDrive.exe`) · `tests/test_brief2_storage.py:450` (asserts on `.ps1`
contents) · `tests/test_analytics.py:1114,1155` (emit `copy analytics\INTERFACE.md …`; the `:1155`
case computes it at runtime via `rel.replace('/', chr(92))`).

### 🔴 THE 15 HITS INSIDE `research_outputs/**/*.json` ARE **NOT** M3 TARGETS

`census2b_manifest.json` (260 path fields), `census2a_manifest.json` (35 + `dest`),
`cen0_manifest.json`, `mc2_manifest_live.json`, `mc2_manifest_evidence.json` are **sealed evidence
artifacts**. Three reasons not to touch them:

1. They record the build host's real topology. **That is provenance — rewriting it falsifies a record.**
2. Nothing is actually broken: verification keyed off the manifests' POSIX-style dictionary keys,
   which already resolve correctly.
3. **Editing them would destroy the byte-equality with the LaCie copy that this drill just
   established**, invalidating the two-witness proof for census2b's only unpinned file and for 4 of
   census2a's manifests.

Fix the **consumers** to map `D:\Naiad\` → repo root at read time. If M3 must touch the manifests,
that is a separate operator decision with a fresh backup taken first.

### ⚠️ 38 doc-only hits — M3 MUST NOT "FIX" HISTORICAL RECORDS

Comments, docstring run-lines, `exchange/` ledgers (`DIGEST.md`, `CONVENTIONS.md`, `CADENCE.md`,
`RETENTION.md`), and recorded preflight blocks in closed manifests. A ledger line saying the repo
lived at `C:\Naiad` on 2026-08-12 **was true on 2026-08-12**; rewriting it makes the ledger lie about
the past and erases the migration evidence a future auditor needs. Docstring `Run:` lines are the one
defensible subset — and even those should be amended, not silently rewritten.

### One stale tracked doc found in passing

`research_outputs/_archive/POINTER.md` (tracked) still maps archives to `D:/Naiad/research_outputs/_archive/`
and the independent backup to `G:/My Drive/naiad-backups/phases/` — **neither exists on this host**.
Its substantive claims still hold (archives are permanent evidence; the sidecars here are canonical);
its path map would **actively misdirect the next restore**. Not edited.

---

## 9 — A DEFECT FOUND AND FIXED BEFORE IT COULD FIRE

`research_outputs/census2b/**` was **absent from `.gitignore`.** `census2a`, `seq8_run2`, `mc1` and
`mc2` were all covered; `census2b` was not — and the LaCie holds 2.1 GB / 261 files of it.

Restoring under v2 would have dropped **untracked-but-unignored bulk** into the working tree: the
precise condition `.gitignore:109` records as the 2026-08-05 incident, when *"a wildcard `git add -A`
swept 3,567 MB into a commit and GitHub rejected the whole branch push."*

**The rule was added BEFORE the restore ran, not after.** Verified after the fact: `git status
--porcelain` shows only `.gitignore` itself, with all ~6 GB of restored substrate correctly ignored.

Consistent with the census2a precedent, census2b's manifests land ignored too — the build document's
path+size+sha256 pointers are the intended surface. **If you want `census2b_manifest.json` tracked as
a committed surface (the `census1b` precedent does this with an explicit negation), say so** — I did
not newly track files on my own initiative.

---

## DISPOSITION TABLE

| item | disposition |
|---|---|
| §1 `.pyc` purge | ✅ DONE — 6 dirs / 73 files / 31 Windows-stale removed; 60 regenerated, 0 stale |
| §2 substrate restore | ✅ DONE — 425 files / 7.45 GB / 0 mismatches; 3 lost folders recovered |
| §3 `naiad-backups` audit | ✅ DONE — twin CONFIRMED, 51/51 × 3 copies; **NO DELETION — awaiting operator's word** |
| §4 drive-literal sweep | ✅ DONE — 43 real defects catalogued for M3; 38 doc-only excluded |
| §5 estate restore | ✅ DONE — 73/73 manifest-verified; case-collision hazard probed, does not fire |
| §6 baseline retaken | ✅ DONE — **287 passed / 0 failed / 1 skipped** |
| census2b ignore gap | ✅ FIXED before restore |
| CRLF sidecars | 🟠 REPORTED, NOT FIXED — operator's call |
| `POINTER.md` stale paths | 🟠 REPORTED, NOT FIXED — M3 |
| `seq8_run2` ⊂ `seq8` (~1.87 GB dupe) | 🟠 REPORTED — no deletion proposed |
| LaCie | ✅ READ-ONLY — nothing written, moved, renamed, deleted or reorganised |

**Rollback:** this session's only repo mutation is `.gitignore` plus this report. The restored bulk is
untracked and ignored; deleting `research_outputs/{census2a,census2b,seq8_run2}` and the 9 `_archive`
zips returns the tree to its pre-session state. The estate cache is reproducible from the archive.

---

## RESIDUAL RISK — WHAT YOU SHOULD **NOT** CONCLUDE

1. **"0 mismatches" ≠ "everything is verified."** 89 of 425 files (~21% by count, **≥1.58 GB**) have
   no external attestation at all. Any error present *before* the backup was taken is invisible to
   this entire exercise.
2. **`basis: manifest` is a maximum, not coverage.** 8 of 30 in `mc1`; 5 of 15 in `seq8`.
3. **The seq8 trust chain is circular** — its manifests are pinned by nothing external. Only an
   external `*.sha256` over the manifests closes this; it does not exist today.
4. **The LaCie is ONE failure domain, not two.** "Two independent backups agree" is false as to
   *independence*.
5. **Nothing about archive interiors was established.** No zip was opened. A uniformly-corrupt zip
   passes every check in this run.
6. **A verified restore does not launder provenance.** `mc1` is provably intact and still
   DISPLAY-ONLY, never evidence.
7. **`_archive` is not runbook-safe** until the CRLF trap is resolved.
8. **The estate is 64 commits stale** and nothing newer exists on any medium. The 287/0 baseline is a
   baseline of *this* estate.

---

## LEDGER — APPENDED

`exchange/status/LEDGER_HEPHAESTUS.md`, this date. Entry supersedes nothing; it records the first
completed run of M2.

---

# 🔴 BRIGHT COLOURS — WHAT THE OPERATOR MUST DO NEXT

## ✅ THE GOOD NEWS FIRST — M2 IS DONE

**The restore drill that halted twice has now run end to end.** The three folders declared
"unrecoverable without the LaCie" — `census2a`, `census2b`, `seq8_run2` — are back, hashed, and
ignored correctly. The estate is live. **The suite reads 287 passed / 0 failed, better than the
Windows machine it came from.** Nothing was lost in the crossing.

## 🔴 1 — THE DELETE WORD IS YOURS, AND I RECOMMEND YOU DO NOT GIVE IT YET

`~/Naiad/naiad-backups` **is** the twin — 51/51 byte-identical, proven across ~2.9 GB. It **is** a v2
one-role violation. Retiring it is safe *on content*.

**But both surviving copies are on the same LaCie spindle.** Delete the in-repo vault today and you
go from **3 copies on 2 devices to 2 copies on 1 device**. One drive failure then takes the estate.

**Do (a) before (c):** (a) make a second-device copy → (b) verify it → (c) then retire the in-repo
vault → (d) leave `research_outputs/_archive` alone → (e) amend `POINTER.md`.

**Nothing was deleted this session.**

## 🟠 2 — `shasum -c` WILL TELL YOU THE ARCHIVES ARE CORRUPT. THEY ARE NOT.

All 9 `_archive` sidecars are CRLF. The obvious verify command reports **9/9 FAILED** on a perfect
restore. Until this is fixed, **anyone auditing without reading this report will reach the wrong
conclusion.** Workaround: `tr -d '\r' < f.sha256 | shasum -a 256 -c -`. Rewriting the sidecars LF is
your call — they are tracked evidence.

## 🟠 3 — TWO PROGRAMS CANNOT RUN ON THIS MAC AT ALL

`scripts/census2a_program.py` and `scripts/mc2_program.py` both assert `OUT.drive.upper() == "D:"`.
On POSIX `Path.drive` is **always `""`**, so the residency gate **can never pass**. Not a subtle
portability wrinkle — an unconditional halt. First item for M3.

## 🟠 4 — DECIDE WHETHER `census2b_manifest.json` SHOULD BE TRACKED

I added `research_outputs/census2b/**` to `.gitignore` before restoring, which closed a real gap that
would have re-run the 2026-08-05 push rejection. Following the census2a precedent, the manifests land
ignored too. The `census1b` precedent instead keeps them via an explicit negation. **One line either
way — tell me which.**

## 🟡 5 — THE ESTATE IS 64 COMMITS OLD, AND THAT IS THE NEWEST THAT EXISTS

The last report guessed the LaCie held something newer. **It does not** — four generations exist
(07-28, 08-02, 08-09, 08-11) and 08-11 is the newest on any medium. Its `repo_head` is
*"exchange: auto-publish 2026-08-11"*, 64 commits behind HEAD, predating all the census2b work. The
287/0 baseline is a baseline of **that** estate. **If you want a current estate, one must be built on
this Mac — it cannot be restored from anywhere.**

## 🟡 6 — ~1.87 GB OF THE WORKING TREE IS A DUPLICATE OF ITSELF

`seq8_run2` is a strict byte-exact subset of `seq8`; only 4 small files differ (22,642 B total). Add
the phase zips held in both `_archive` and `naiad-backups/phases/` and the tree carries ~1 GB twice
more. **Reported only. Nothing deleted, nothing proposed as taken.**

## 🟢 7 — CARRIED FORWARD, NOW UNBLOCKED

HALT 4 is cleared (SSH host keys installed after fingerprint verification; the push went through).
HALT 1 remains degraded-not-blocking: `requirements-lock-2026-08-14-win.txt` is still worth
recovering from the Windows box **before that machine is wiped**, for transitive parity only.
ATHENA's note stands: `cache_dir()` still mkdirs on read at `engine/data.py:47` — any future gate
that merely *prints* the cache path will silently create it.
