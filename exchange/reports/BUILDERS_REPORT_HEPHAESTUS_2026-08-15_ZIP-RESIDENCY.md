# BUILDERS REPORT — HEPHAESTUS — 2026-08-15 — ZIP RESIDENCY RULING + DEDUPE PASS

**Ruling (operator, 2026-08-15):** *"older zips live on the LaCie; new zips are born local; backups
go to the LaCie only."* Supersedes the earlier DEDUPE brief.
**Branch:** `v12-v1-census`. **Host:** macOS, `~/Naiad`. **Gate 0:** passed — cwd `/Users/luis/Naiad`,
not a cloud tree, both LaCie twin trees reachable.

Written for a reader with **zero prior context**.

---

## 0 · WHAT HAPPENED

**5,975,371,985 bytes — 5.98 GB — were deleted, and every single one was gated on a fresh sha256
match computed this run against its twin. Zero mismatches. Zero surprises. One file kept.**

`du -sh ~/Naiad`: **10G → 4.6G.**

| bucket | verified + deleted | bytes freed | kept |
|---|---:|---:|---|
| (a) `research_outputs/_archive/*.zip` | 9 | 1,043,591,544 | 0 |
| (b) `naiad-backups/` entire in-repo vault | 51 | 3,061,562,754 | **1** — `.DS_Store`, no twin |
| (c) `research_outputs/seq8_run2` data | 8 | 1,870,141,663 | 0 |
| (d) `~/.cache/naiad/data_cache/_repo/` | 3 | 76,024 | 0 |
| (e) Drive staging debris | — | 0 | — |
| **TOTAL** | **71** | **5,975,371,985** | **1** |

And four things that had to follow in code:

| item | outcome |
|---|---|
| Retention/HEARTBEAT phase scan must not cry wolf | **DONE.** An empty local `_archive` now reads as by-design |
| Ruling 4a — `daily_routine` honours `scheduled: false` | **DONE.** `SKIPPED(retired 2026-08-05)` |
| Identity gate learns Drive staging markers | **DONE**, and proven both ways |
| Estate proof after (d), expect 8/8 | **8/8, exit 0** — but *not* from (d) alone; see §4 |

**One thing the brief did not anticipate, and it mattered:** (d) alone did **not** produce 8/8. It
fixed three of the four name collisions in the estate archive; the fourth was a **reserved-name**
collision in `backup_estate.py` itself and needed a code fix. §4.

---

## 1 · THE DELETION GATE, AND WHY IT IS STRONGER THAN ASKED FOR

The authorization was narrow: *every deletion individually gated on a FRESH sha256 match against its
LaCie twin THIS RUN (sidecar where one exists, direct twin-hash otherwise)*.

**Both sides were hashed, every time — the sidecar was used as an extra check, never as a
substitute.** The reasoning, stated because it is the whole safety argument:

> A sidecar proves what a file **was**. It does not prove the twin is still on the volume, still
> readable, and still intact. The twin is about to become the **only** copy. So the twin itself was
> read and hashed, fresh, immediately before each local file was removed.

Where a sidecar existed on either side it was compared too. **33 files carried both-side sidecar
cross-checks. 0 disagreed.**

Failure policy, as instructed: any mismatch, missing twin, or unreadable file → **KEEP that file,
report it, continue with the rest**. No bucket was abandoned because one member failed.

Total data read to authorise the deletions: roughly **11.6 GB** — every local file and every twin.

---

## 2 · THE PER-FILE LEDGER

Format: `sha256=<first 16 hex>` is the digest computed **this run**, identical on both sides.
`[local-sc=OK, twin-sc=OK]` means a sidecar on that side agreed as well.

### (a) `research_outputs/_archive/*.zip` — 9 archives, 1,043,591,544 B

Sidecars and `POINTER.md` **stayed**, as instructed.

```
DELETED   analytics_tests_v1.0.0_2026-07-29.zip         6,816 B  sha256=0a1ffc941032acbf VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   analytics_v1.0.0_2026-07-29.zip              19,641 B  sha256=d3fcd786881dc202 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   s1_2026-07-27.zip                       106,239,157 B  sha256=4d14ea48066dcf8b VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   s2_2026-07-27.zip                       246,355,294 B  sha256=df5c1c196fef8225 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   s3_2026-07-27.zip                       269,919,602 B  sha256=80ac04439e169cf1 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   tc1_2026-07-27.zip                      242,926,299 B  sha256=e673a158b5b1388d VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   tc4_2026-07-27.zip                       68,700,167 B  sha256=794036c2d6135285 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   tc5_2026-08-02.zip                       18,375,498 B  sha256=68942d6261bf8ca8 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   v3_anchor_2026-07-27.zip                 91,049,070 B  sha256=69d9cc989cb4054e VERIFIED==twin  [local-sc=OK, twin-sc=OK]
---
(a): 9 verified+deleted, 1,043,591,544 B freed, 0 kept
```

**All nine carried a full three-way agreement** — local file, LaCie twin, and both sidecars.

`research_outputs/_archive/` now contains exactly `POINTER.md` + 9 `*.sha256` — **40 KB**, and every
one of those sidecars is tracked in git.

### (b) `naiad-backups/` — the entire in-repo vault, 51 members, 3,061,562,754 B

Every member was verified: 4 estate zips (~1.98 GB), 8 workflow zips, 4 stray analytics copies, the
9-archive `phases/` sub-vault, and every `.sha256` alongside them. Representative lines — the four
estate generations, which are the bulk:

```
DELETED   naiad-backups/naiad_estate_2026-07-28.zip     492,306,779 B  sha256=ad94dc6e1e6750bb VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   naiad-backups/naiad_estate_2026-08-02.zip     493,542,600 B  sha256=f1e901d23fee7126 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   naiad-backups/naiad_estate_2026-08-09.zip     495,130,299 B  sha256=1b4b4c9f0fd92d45 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
DELETED   naiad-backups/naiad_estate_2026-08-11.zip     495,619,988 B  sha256=f0cfdb2a56ad4853 VERIFIED==twin  [local-sc=OK, twin-sc=OK]
```

and the one that was **not** deleted:

```
KEEP      naiad-backups/.DS_Store        6,148 B  NO TWIN at /Volumes/LaCie/naiad-backups/.DS_Store
---
(b): 51 verified+deleted, 3,061,562,754 B freed, 1 kept
```

**`.DS_Store` has no twin, so the gate kept it — as written.** It is macOS Finder metadata,
regenerable, already gitignored, and it is now the *only* thing keeping `naiad-backups/` alive at
8.0 KB. Removing it is one command and it is **the operator's call, not mine**:

```
rm ~/Naiad/naiad-backups/.DS_Store && rmdir ~/Naiad/naiad-backups
```

The three now-empty subdirectories (`phases/`, `.tmp.driveupload/`, `.tmp.drivedownload/`) **were**
removed — `rmdir` of an empty directory destroys no data.

**The 2026-08-15 pair was verified as present on the LaCie before any of this ran**, as required:
`naiad_estate_2026-08-15.zip` (495,635,403 B) and `naiad_workflow_2026-08-15.zip` (4,183,212 B),
both with sidecars.

### (c) `research_outputs/seq8_run2` — 8 data files, 1,870,141,663 B

```
DELETED   seq8_arrivals.json                 669,814 B  sha256=16fef0c4771633bb VERIFIED==twin
DELETED   seq8_cascade_birth_join.jsonl  122,363,043 B  sha256=63777ca872115ba0 VERIFIED==twin
DELETED   seq8_cascades.jsonl            789,501,107 B  sha256=13195287eceab160 VERIFIED==twin
DELETED   seq8_d4_route_matrix.json          193,545 B  sha256=f45b6d426e19c104 VERIFIED==twin
DELETED   seq8_event_counts.json              27,067 B  sha256=9584aaadf0454e1a VERIFIED==twin
DELETED   seq8_events.jsonl              167,105,389 B  sha256=2bdc5c56c054e27c VERIFIED==twin
DELETED   seq8_outcomes.jsonl            790,256,704 B  sha256=7f096222aac6f339 VERIFIED==twin
DELETED   seq8_warmup.json                    24,994 B  sha256=c9a68c6ca0654a53 VERIFIED==twin
---
(c): 8 verified+deleted, 1,870,141,663 B freed, 0 kept
```

**1,870,141,663 B is exactly the brief's "~1.87 GB"** — the arithmetic agrees to the byte, which is
the cheapest possible confirmation that the right set was selected.

**The 3 run-manifests were KEPT per rule R3, and they were identified from the record rather than
guessed.** Queue 003 line 38 accounts `seq8_run2` as *"8/8 data files identical, 3/3 manifests"*, and
`BUILDERS_REPORT_HEPHAESTUS_2026-08-11_R1-R2-R3.md` §4a names the three by hash — they are the only
files in `seq8_run2` that **differ** from `seq8`, which is what makes them the run's unique
provenance and the only thing a discard would cost:

| kept file | why |
|---|---|
| `seq8_extract_manifest.json` | R3 metadata, differs from `seq8` |
| `seq8_outcomes_manifest.json` | R3 metadata, differs from `seq8` |
| `seq8_views_summary.json` | R3 metadata, differs from `seq8` |

`research_outputs/seq8_run2/` now holds exactly those three, 20 KB, plus `README_R3.md` (§3).

### (d) `~/.cache/naiad/data_cache/_repo/` — the estate-shape fix, 3 files, 76,024 B

This one is outside the repo and has no LaCie twin, so the gate was applied against **the repo file
each copy duplicates** — the correct twin for a copy:

```
DELETED   DATA_CENSUS.md                              11,483 B  sha256=7d841b36a6875b76 VERIFIED==repo/DATA_CENSUS.md
DELETED   census.json                                 62,741 B  sha256=e31a6ed823e6e6f6 VERIFIED==repo/census.json
DELETED   research_outputs/census/build_manifest.json  1,800 B  sha256=d4820b1d1965eb1a VERIFIED==repo/research_outputs/census/build_manifest.json
RMDIR     research_outputs/census
RMDIR     research_outputs
RMDIR     _repo/  (now empty -- the estate shape is fixed)
---
(d): 76,024 B freed, 0 kept
```

The cache root is now exactly `MANIFEST.json`, `funding/`, `klines/` — the shape it should always
have had. The stray `_repo/` came from the M2 restore unpacking a prior estate archive *into* the
cache root.

### (e) Drive staging debris — **condition met, nothing left to delete**

The gate was *"only if `~/Naiad` is no longer Drive-registered; else HALT-SOFT."*

**It is no longer registered — established from Drive's own databases, not from the absence of the
staging folder:**

```
root_preference_sqlite.db   roots        -> 0 rows
<acct 1032617…>/mirror_sqlite.db  root_config -> 0 rows,  mirror_item -> 0,  pending_uploads -> 0
<acct 1033187…>/mirror_sqlite.db  root_config -> 0 rows,  mirror_item -> 0,  pending_uploads -> 0
```

`/Users/luis/Naiad` strings still appear in those files, but only as **residue in freed pages** — the
live tables are empty. So the M4 finding is closed: **the operator unregistered the repo.**

By the time the pass reached (e) there was nothing to remove — Drive had finished draining and the
staging folders were empty; the empty directories were `rmdir`'d under (b).

**But this bucket nearly mattered a great deal, and the reason belongs in the record.** During the
dry run, `naiad-backups/.tmp.driveupload/` held four entries with **link count 2, sharing inodes with
the vault's estate zips**:

```
165: links=2 size=492306779 inode=417838   <- same inode as naiad_estate_2026-07-28.zip
189: links=2 size=495130299 inode=417874
193: links=2 size=493542600 inode=417852
209: links=2 size=495619988 inode=417892
```

**Deleting a zip while its staging hardlink survives frees nothing** — it only decrements the link
count. Had those persisted, bucket (b) would have reported 3.06 GB freed and `du` would have barely
moved. The tool was given an inode-identity gate for exactly this case (same inode is not "probably
the same bytes", it *is* the same bytes); in the event Drive cleared them first, and `du` confirms
the space really was returned.

---

## 3 · `README_R3.md`

Written to `research_outputs/seq8_run2/README_R3.md`, naming the twins' path so the folder explains
itself. Contents in §9's disposition table.

---

## 4 · THE ESTATE PROOF — 8/8, BUT NOT FROM (d) ALONE

The brief said: *after (d), `backup_estate.py --estate --force-same-day` → expect 8/8.*

**The first run after (d) returned 5/8, not 8/8.** Reported rather than retried quietly:

```
FAIL F-K1 - 73/74 members verified both directions; 0 mismatches, 0 strays, 1 omissions
PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
FAIL F-K3 - 20-file sha sample unchanged: True; git porcelain identical: False
FAIL F-K4 - 10 members restored ... 1 hash mismatches
5/8 fixtures pass
```

Two distinct causes, one of them mine:

**F-K3 was my own fault, not a defect.** I edited `POINTER.md` *while the archive was building*.
F-K3 compares `git status --porcelain` before and after, so it correctly detected that the working
tree changed mid-run. The second run was performed on a quiet tree and F-K3 passed.

**F-K1 and F-K4 were the fourth collision, and (d) could never have fixed it.** M4 found the estate
zip carrying 78 entries under 74 names. Removing the stray `_repo/` fixed **three**. The fourth was
`MANIFEST.json`, and it is not stray data — it is a **reserved-name collision inside
`backup_estate.py`**:

- `build_archive()` writes the member index as `MANIFEST.json` at the archive root.
- `verify_archive()` reads it back with `zf.read("MANIFEST.json")` **and then excludes that name
  from the member set** with `n != "MANIFEST.json"`.
- The estate cache has **its own** `MANIFEST.json` at its root, which the walk picked up.

Measured in the 5/8 archive:

```
entries: 75  unique: 74   duplicated: {'MANIFEST.json': 2}
  MANIFEST.json offset 0          size 11589   sha c73fec06e38f2ef9   <- the cache's own
  MANIFEST.json offset 497137154  size 11658   sha 2bebe34dcbaff63f   <- the generated index
  cache on disk                   size 11589   sha c73fec06e38f2ef9
```

`zipfile` returns the **last** entry for a duplicated name, so F-K4 restored `MANIFEST.json`, got the
generated index, compared it against the cache's copy on disk, and reported **1 hash mismatch**. And
because the reserved name is excluded from `in_zip`, the cache's copy sat in `pinned` with nothing to
match — **1 omission** in F-K1.

**The fix, symmetric with what was already there rather than novel.** `REPO_PREFIX = "_repo/"`
already existed for repo companions. A member whose arcname would collide with a reserved root name
is now stored under `ESTATE_PREFIX = "_estate/"`, and `resolve_member()` maps it back:

```python
RESERVED_ROOT_NAMES = frozenset({"MANIFEST.json"})
ESTATE_PREFIX = "_estate/"

members = [((ESTATE_PREFIX + rel) if rel in RESERVED_ROOT_NAMES else rel, ap)
           for rel, ap in members]
```

**The cache's manifest is PRESERVED.** Dropping it from the archive was the smaller change and would
have quietly made restores incomplete — a silent hole in a backup is worse than the bug it fixes.
Round-trip proven:

```
members: 74  unique: 74  duplicates: NONE
reserved-name escape present: ['_estate/MANIFEST.json']
resolve_member('_estate/MANIFEST.json') -> /Users/luis/.cache/naiad/data_cache/MANIFEST.json  exists=True
```

### The clean run

```
FIXTURES
  PASS F-K1 - 74/74 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  PASS F-K2 - census 60/60 klines, 10/10 funding; 0 unresolved
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to /var/folders/.../T\... outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 f495ff721e787e3e... matches=True, sidecar matches=True, CRC clean=True, 74 members
  same-day re-run: naiad_estate_2026-08-15-02.zip exists and was written today; writing naiad_estate_2026-08-15-02-01.zip instead (both are kept)
  PASS F-K6 - default refuses; --force-same-day yields naiad_estate_2026-08-15-02-01.zip while naiad_estate_2026-08-15-02.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 3/3 git-tracked source files still present on disk; 0 missing

archive   : /Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15-02.zip
size      : 497,146,734 B (474.1 MB, 75.5% of source)
sha256    : f495ff721e787e3ee70e7f74686e18eb88a98b5454935fdbf9c8141865c39410
members   : 74
source    : 658,882,313 B
sidecar   : /Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15-02.zip.sha256

8/8 fixtures pass          EXIT=0
```

> **F-M3-6 IS NOW FULLY CLOSED.** M4 closed the write path and left the estate archive's *shape*
> open. Both halves are now proven: `--workflow` 8/8 (M4) and `--estate` 8/8 exit 0 (here), on real
> hardware, with the archive landing on the LaCie and verifying against its own sidecar.

---

## 5 · THE RETENTION SCAN NO LONGER CRIES WOLF

The local `_archive` is now empty by design, and the old scan printed `- none found` for that — the
same sentence it prints when something is genuinely wrong. **A scan that cries wolf is a scan an
operator learns to ignore.** Rendered live from the clean estate run:

```
## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy of
a newer one — it is the only copy of work that will never be produced again.

Location: `/Users/luis/Naiad/research_outputs/_archive`

**CURRENT CYCLE EMPTY — this is BY DESIGN and is NOT a finding.**

Under the zip-residency ruling (operator, 2026-08-15) *new zips are born local and older zips live
on the LaCie*. An empty local `_archive` means every archive written so far has been aged out to the
backup volume — which is the intended end state of a cycle, not a missing archive. The tracked
sidecars below are the standing fingerprint set and are always present; the aged-out archives are
enumerated further down when the volume is reachable.

**FINGERPRINT SET: 9 tracked sidecar(s) in `research_outputs/_archive/`.** These are committed, so
they describe the archive set from any clone, with no volume attached and no zip present locally.

Aged-out archives: `/Volumes/LaCie/Naiad/research_outputs/_archive`
- **[backup] 9 archive(s), 1,043,591,544 B (1,043.6 MB)** on `/Volumes/LaCie`.

Backup copy: `/Volumes/LaCie/naiad-backups/phases`
- **[backup] 9 archive(s), 1,043,591,544 B** on `/Volumes/LaCie`.
```

Exactly the shape asked for: **local zips as current-cycle; LaCie `_archive` as `[backup]` when
reachable and `NOT ENUMERABLE` when not; tracked sidecars as the always-present fingerprint set; an
empty local `_archive` is not a finding.**

**What still IS a finding, deliberately kept sharp:** a sidecar with no archive on either side. The
scan now computes `fingerprints − aged-out` and reports any gap in bold. Today the gap is empty —
9 sidecars, 9 archives on the volume.

`backup_estate --phase` is **unchanged**: born local, `--mirror` to the LaCie as a separate verified
step.

---

## 6 · RULING 4a — RETIRED JOBS ARE SKIPPED

M4 found that `routine_jobs.json`'s `"scheduled": false` and `"retired"` keys were **decorative**:
`run_job()` never read them and the job loop is unconditional. The operator ruled **YES**.

The gate is checked **before** `script.exists()` — a retired job is not required to still be on
disk, and reporting "script not found" for a job we have decided not to run would be a misleading
error rather than a clean skip. `daily_brief.py` is **not** deleted; `brief_capture.py` still imports
it for the Part I layers.

```
$ simulate the ruling against the real registry
  manifest         would RUN
  brief            SKIPPED(retired 2026-08-05)
  brief2_capture   would RUN
  brief2_panel     would RUN
```

Skips are **reported, never silent** — on the console as `SKIPPED(retired 2026-08-05)`, and named in
the DAILY report *above* the failures, because `all jobs OK` printed alongside a job that never ran
is technically true and practically a lie.

**What this buys:** on the M4 launchd proof run, `brief` took **622.0s of the routine's 623.2s** —
ten minutes of live network fetches every morning for an output nothing had read since 2026-08-05,
while its two replacements finished in 0.2s. The 07:00 agent now does its actual work in about a
second.

---

## 7 · THE IDENTITY GATE LEARNS DRIVE — GATE DIFF

M4's open item 4. The two existing limbs grep the **path**, and a path grep **cannot** see Google
Drive: measured 2026-08-15, Drive was uploading `research_outputs/seq8*` and the backup vault out of
`~/Naiad` while both limbs passed cleanly, because the repo is not under `CloudStorage` — Drive
reaches it via a sibling symlink and `realpath("~/Naiad")` is unchanged.

**So the new limb looks for the artefact, not the path.** Added identically to
`scripts/census2a_program.py` and `scripts/mc2_program.py`:

```diff
   checks.append(("pwd cloud-free",
                  not any(m in low for m in
                          ("onedrive", "com~apple~clouddocs", "mobile documents")), cwd))
+  # THIRD LIMB, added 2026-08-15 (M4 open item 4).
+  _found = _drive_staging_markers(Path.cwd())
+  checks.append(("no Drive staging in tree", not _found,
+                 ", ".join(_found) if _found else "none"))
```

with a shared helper scanning the repo root and one level in — the two depths where real sightings
occurred (`./.tmp.driveupload` and `./naiad-backups/.tmp.driveupload`) — for
`.tmp.driveupload`, `.shortcut-targets-by-id`, `.file-revisions-by-id`. It never raises: a gate that
dies on an unreadable directory is a gate that stops gating.

**Proven in both directions — a gate only tested on the passing case is untested:**

```
census2a_program     no Drive staging in tree = True   detail=none
mc2_program          no Drive staging in tree = True   detail=none

positive control (marker planted in a scratch tree):
  planted marker -> ['sub/.tmp.driveupload']   gate passes = False
```

---

## 8 · SUITE

```
$ ~/venvs/naiad/bin/python -m pytest
287 passed, 1 skipped in 14.53s
```

**287 / 0 / 1 — unchanged.** No fixtures added; the estate proof is a printed transcript, so the
count stays directly comparable to M3 and M4.

---

## 9 · FILE DISPOSITION TABLE (CONVENTIONS §3.2)

Box cost is against the 6,390,000 B box. `n/a` for anything outside `exchange/`.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-15_ZIP-RESIDENCY.md` | yes | tracked | final publish | yes | GitHub + next `--workflow` archive | ~19 KB · ~0.30% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | final publish | yes | GitHub + `--workflow` archive | +~6 KB · +0.09% |
| `exchange/status/RETENTION.md` | yes | tracked | `4605a65` + `7224d58` | yes | GitHub + `--workflow` archive | rewritten by the estate runs |
| `scripts/backup_estate.py` | yes | tracked | `a61a695` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `scripts/daily_routine.py` | yes | tracked | `a61a695` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `scripts/census2a_program.py` | yes | tracked | `a61a695` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `scripts/mc2_program.py` | yes | tracked | `a61a695` | yes | GitHub + `--workflow` archive | n/a — `scripts/` |
| `research_outputs/_archive/POINTER.md` | yes | tracked | `a61a695` | yes | GitHub + `--workflow` archive | n/a — `research_outputs/` |
| `research_outputs/_archive/*.sha256` (9) | yes | **tracked — untouched** | pre-existing | yes | GitHub + `--workflow` archive | n/a |
| `research_outputs/_archive/*.zip` (9) | **no — aged out** | ignored (`.gitignore:38` `*.zip`) | n/a | n/a | **LaCie `_archive` + LaCie `phases`, both verified this run** | n/a |
| `research_outputs/seq8_run2/README_R3.md` | yes | ignored — `.gitignore` `research_outputs/seq8_run2/**` | not committed | no | LaCie mirror | n/a |
| `research_outputs/seq8_run2/` 3 R3 manifests | yes | ignored | not committed | no | LaCie mirror (verified this run) | n/a |
| `research_outputs/seq8_run2/` 8 data files | **no — deleted** | ignored | n/a | n/a | **LaCie mirror, verified this run** | n/a |
| `naiad-backups/**` (51 members) | **no — deleted** | ignored — `.gitignore:162` | n/a | n/a | **`/Volumes/LaCie/naiad-backups`, every member verified this run** | n/a |
| `naiad-backups/.DS_Store` | **yes — KEPT** | ignored | n/a | n/a | **NOT PROTECTED** — no twin; Finder metadata | n/a |
| `~/.cache/naiad/data_cache/_repo/` | **no — removed** | outside repo | n/a | n/a | contents are copies of tracked repo files | n/a |
| `/Volumes/LaCie/naiad-backups/naiad_estate_2026-08-15-02.zip` (+`.sha256`) | yes | outside repo | n/a | n/a | **is itself the backup** | n/a |

**No artifact this session exceeds 1% of the box.** Per §3.1, this document does not contain its own
sha256.

---

## 10 · WHAT REMAINS OPEN

| # | item | owner |
|---|---|---|
| 1 | `naiad-backups/.DS_Store` — the one file the gate kept. `rm` + `rmdir` retires the vault directory entirely | **operator** |
| 2 | The box is at **38.5%**, still WARN — unchanged by this session, which freed disk, not bus | **operator** (carried from M4) |
| 3 | `backup_estate.py` still has publish welded in, no `--no-publish` | code lane (carried from M4) |
| 4 | The three slot-anchored brief triggers still have no launchd counterpart | operator's M5 (carried) |
| 5 | `exchange/.DS_Store` is **tracked** despite the `.gitignore` rule — it predates it, so the rule never applied. Auto-publishes keep committing it | code lane, trivial: `git rm --cached` |

### Publishes this session

The brief asked for one. **Three occurred**; two were tool-driven, exactly as reported in M4 §7.3 —
`backup_estate.py` calls `publish()` and has no way to opt out, so every estate run publishes:

| publish | origin | outcome |
|---|---|---|
| estate proof run 1 (5/8) | `backup_estate.py` | `4605a65` — RETENTION.md, 38.5% |
| estate proof run 2 (8/8) | `backup_estate.py` | `7224d58` — RETENTION.md, 38.5% |
| final, this report | **deliberate** | the only one that was a choice |

---

## 11 · BRIGHT COLOURS — THE M5 REMAINDER IS THE OPERATOR'S

> Recorded, **not** begun:
>
> - **Spotlight privacy list** — needs GUI/sudo. Carried unchanged from M3.
> - **Cowork remount.**
> - **Confirm the Drive mirror of `/Volumes/LaCie/naiad-backups` shows synced** — that closes 3-2-1
>   for the newest archives. Worth noting alongside §2(e): Drive no longer mirrors `~/Naiad`, so the
>   LaCie mirror is now the *only* cloud path for these archives, which makes this check load-bearing
>   rather than cosmetic.

---

*Filed by HEPHAESTUS, 2026-08-15. ONE commit `a61a695`, pushed. Ledger entry appended to
`exchange/status/LEDGER_ATHENA.md` in the same session, per CONVENTIONS §3.1 ruling 'append'.*
