# BUILDER'S REPORT — HEPHAESTUS — QUEUE 005 M3 — THE PLATFORM SWEEP

**Date:** 2026-08-15 · **Host:** Luiss-MacBook-Pro.local · **Branch:** v12-v1-census
**Ruling in force:** DATA RESIDENCY v2 — everything local under `~/Naiad`; the LaCie is BACKUP ONLY.
**Commit:** `f403546` (one commit, pushed) · **Rollback:** `git revert f403546`

---

## VERDICT IN ONE LINE

The sweep found **two defects that were not path typos** — a backup guard that was **inert on
macOS** and two residency gates that **halted unconditionally** — fixed both, cleared the live-code
remainder to empty, and held the suite at **287 / 0 / 1**.

---

## 0 — IDENTITY GATE

```
pwd=/Users/luis/Naiad  head=bab7e90  os=Darwin arm64
GATE: PASS - at origin tip, correct branch, non-cloud tree
```

Cloud-marker limb (`OneDrive`, `com~apple~CloudDocs`, `Mobile Documents`) clean; `pwd ==
$HOME/Naiad`; branch `v12-v1-census`; `git fetch` succeeded and HEAD == `origin/v12-v1-census`.

---

## 1 — RE-ENUMERATION (fresh, not the M2 copy)

The M2 §4 catalogue was **not** trusted. The grep was re-run live and returned **116 raw hits** —
more than M2's 43, because this pattern also sweeps `PYTHONIOENCODING` and casts wider across
`fixtures/` and `study/`.

Classifying 116 required a **fourth bucket the brief did not name**: the pattern `[A-Za-z]:[/\\]`
also matches `https://`, `error:\n`, and `^zone:\s*`. Those are not defects in any category — they
are **regex artifacts**, and editing one would be damage. They are reported so the count reconciles.

### Classification table

| verdict | count | meaning |
|---|---:|---|
| **FIX** | 45 | live code or a live instruction, wrong on this platform |
| **HISTORY** | 7 | dated records — left verbatim, correction note added where load-bearing |
| **ALREADY-DEAD** | 2 | unreachable on POSIX, cannot misfire |
| **NOT-A-HIT** | 8 | regex artifact, not a defect |
| *(agent-classified subtotal)* | *62* | *disjoint file groups* |
| **operator-core, classified by me** | 54 | `backup_estate` / `census2a_program` / `mc2_program` / `drive_wait` / `routine_jobs` |
| **TOTAL** | **116** | |

**50 mechanical edits across 28 files** were applied by four parallel agents on disjoint file sets,
every one carrying both post-write assertions (old absent, new present). All four groups reported
`assertions_passed=true`; I re-verified the two highest-risk diffs by hand (below).

### Notable per-class decisions

- **`drive_wait.py:9`** — `[ -d "D:/Naiad" ] || HALT` is **HISTORY, not a defect**. It is the module
  docstring quoting the *broken pattern the module exists to replace*. Rewriting it would delete the
  rationale for the file.
- **Docstring `Run:` lines are FIX, not HISTORY.** They are instructions a reader follows *today*.
  22 were rewritten from `C:\venvs\naiad\Scripts\python.exe` to `python`. Where a line also passed
  `-q`, the `-q` was dropped in the same edit — `pytest.ini` already sets `addopts = -q`, and
  passing it twice suppresses the final count line, which looks like a crash.
- **`daily_routine.py:573` — ALREADY-DEAD, not FIX.** The message names `C:/Naiad`, but
  `_onedrive_running()` returns `None` off Windows (guarded at line 387) and the alert fires only
  `if od is False`. Verified live: returns `None`. It cannot print.
- **`engine/data.py:44` — ALREADY-DEAD, correct as written.** The `LOCALAPPDATA` subscript sits
  behind `os.name == "nt"` with a POSIX fallback. It is the *model*, not a defect.
- **`setup_brief_schedule.ps1` — ALREADY-DEAD.** Windows-only artifact; not ported, and deliberately
  left CRLF.

---

## 2 — RESIDENCY v2 — AND THE TWO REAL DEFECTS

### 🔴 DEFECT 1 — the backup guard was INERT on macOS, and worse than inert

`backup_estate.drive_ready()` took its anchor from `Path(root.anchor)`. On Windows that is `D:\` —
correct. **On POSIX `Path("/Volumes/LaCie/naiad-backups").anchor` is `"/"`** — the boot volume,
always mounted. The guard whose entire purpose is *"a backup that lands on the machine it is backing
up is not a backup"* **could not fail**.

It is worse than that. With the old `BACKUP_DEST_DEFAULT = "D:/naiad-backups"`, `Path("D:/…")` is
**relative** on POSIX. Demonstrated live, no writes:

```
Path('D:/naiad-backups')
  .is_absolute() = False
  .anchor        = ''
  .parts         = ('D:', 'naiad-backups')
  -> old guard: anchor='' -> "no drive anchor to check" -> ok=True
  -> dest resolves to: /Users/luis/Naiad/D:/naiad-backups
```

**The backup would have been written inside the repo it was backing up, into a directory literally
named `D:`, and the guard would have reported success.**

Fix: new `volume_anchor()` returns the **mount point** (`/Volumes/LaCie`), or `None` when the path
is on the boot volume and there is genuinely nothing external to wait for.

**Proven live, with the LaCie absent:**

```
=== NEW CODE, LACIE ABSENT ===
BACKUP DESTINATION UNREACHABLE: /Volumes/LaCie/naiad-backups
  /Volumes/LaCie UNREACHABLE after 18.03s (6 attempt(s), budget 18.0s)
  The volume /Volumes/LaCie is not mounted.
  SystemExit( 2 ) -- HALTED correctly

=== --phase root, LACIE ABSENT (must still work: born local under v2) ===
  phase_archive_root(): /Users/luis/Naiad/research_outputs/_archive
```

### 🔴 DEFECT 2 — two residency gates halted unconditionally

`census2a_program.py:185` and `mc2_program.py:270` both asserted `OUT.drive.upper() != "D:"` →
HALT. **`Path.drive` is always `""` on POSIX**, so the assertion could never pass: the gate was
**dead, not strict**. The identity limb was equally dead — `cwd.endswith("c:/naiad")` cannot be true
here.

Restated with the **same intent** (bulk lands where residency says) and a new definition of *where*:
containment under `ROOT/research_outputs`, plus the v2 two-sided identity gate.

**§7(c) SMOKE PROOF — both print their first PASS lines on this machine:**

```
[05:50:12] PREFLIGHT -- I3 identity (in code) + I2 residency gate
[05:50:12]     PASS  pwd == $HOME/Naiad             /Users/luis/Naiad
[05:50:12]     PASS  pwd cloud-free                 /Users/luis/Naiad
[05:50:12]     PASS  branch v12-v1-census           v12-v1-census
[05:50:12]     PASS  remote catpatrol/Naiad         git@github.com:catpatrol/Naiad.git
[05:50:12]     residency OK -> /Users/luis/Naiad/research_outputs/census2a
  -> RETURNED OK  drive = LOCAL

[05:50:12] S0 preflight -- identity (I3) + residency (I2)
[05:50:12]     PASS  pwd == $HOME/Naiad           /Users/luis/Naiad
[05:50:12]     PASS  pwd cloud-free               /Users/luis/Naiad
[05:50:12]     residency OK -> /Users/luis/Naiad/research_outputs/census2a/mc2
  -> RETURNED OK  drive = LOCAL
```

**An error my own edit introduced, caught by the smoke proof and fixed:** removing `wait_for_drive`
left both preflights returning `{"drive": {"state": r.state …}}` with `r` undefined — `NameError` at
`census2a_program.py:218`. This is exactly why the smoke step exists rather than a bare import
check. The key is retained as `"state": "LOCAL"` so downstream manifest readers need not branch.

### The rest of the residency rule, as issued

| target | change |
|---|---|
| `census2a_program.OUT`, `mc2_program.D_ROOT` | `Path("D:/…")` → `ROOT / "research_outputs" / …` |
| `census2b_program`, `census2b_wtb1`, `census2a_viz`, `census2b_parta` | same, repo-relative from the existing `Path(__file__)` anchor |
| `backup_estate --phase` | **born local**: default is now `REPO/research_outputs/_archive`; `--mirror` (already wired) carries the verified second copy to the LaCie; sidecar stays tracked in-repo |
| `backup_estate --estate/--workflow` | default `/Volumes/LaCie/naiad-backups`, through `drive_wait` — same physical disk as `D:/naiad-backups`, new address |
| `NO_WAIT_ANCHORS_DEFAULT` | `"G:\\"` → `""`. Mechanism kept (a virtual mount is still not a sleeping disk); the Windows `GetDriveTypeW` measurement is retained as the *reason the list exists*, not as a live claim |
| retention / HEARTBEAT phase scan | scans the **local** `_archive` (always present); the LaCie is reported separately as `[backup]` — enumerated when reachable, **`NOT ENUMERABLE`** when not, never "none found" |
| `drive_wait` USAGE + bare default | `D:/Naiad` → `/Volumes/LaCie`; docstring now warns to pass a **mount point**, not a path inside it |
| `LOCALAPPDATA` ×4 | resolved through `engine.data.cache_dir()` — one definition of where the estate lives |
| `routine_jobs.json` | `C:\venvs\…\python.exe` → `python`; `D:\naiad-backups` → `/Volumes/LaCie/naiad-backups`; JSON re-parsed OK |

**A latent bug the `rc_recompute` agent found while porting:** the old inline cache default
evaluated the `LOCALAPPDATA` leg **eagerly**, as `os.environ.get`'s fallback argument — so it raised
`KeyError` off Windows *even when `NAIAD_CACHE_DIR` was set*. Now a guarded `_cache_root()` that
mirrors `cache_dir()` **without** its `mkdir`, because that module is read-only.

---

## 3 — CRLF SIDECARS → LF (F-M3-3)

All 9 tracked `*.sha256` were CRLF, so `shasum` searched for a filename ending `\r`:

```
BEFORE:  shasum: s1_2026-07-27.zip: No such file or directory
         s1_2026-07-27.zip: FAILED open or read
```

Converted whole-file, CRLF→LF. **Recorded digests asserted byte-identical before and after** —
content preserved, EOL only.

### F-M3-3 TRANSCRIPT — native, no `tr` workaround

```
$ shasum -a 256 -c *.sha256
analytics_tests_v1.0.0_2026-07-29.zip: OK
analytics_v1.0.0_2026-07-29.zip: OK
s1_2026-07-27.zip: OK
s2_2026-07-27.zip: OK
s3_2026-07-27.zip: OK
tc1_2026-07-27.zip: OK
tc4_2026-07-27.zip: OK
tc5_2026-08-02.zip: OK
v3_anchor_2026-07-27.zip: OK

exit code: 0
F-M3-3 RESULT: 9/9 OK, exit 0 — PASS
```

This also re-verifies ~1.04 GB of phase archives against their tracked sidecars as a side effect.

### ⚠️ `.gitattributes` was deliberately kept to ONE line

`*.sha256 text eol=lf` — the class rule, as issued. A first draft also pinned `*.py`, `*.json`,
`*.sh`. **It was reverted unapplied**: eleven source files in this repo are still CRLF, and the
wider rule re-normalised them wholesale, producing a **~15,000-line diff** that would have buried
every real change in this commit. Source line-ending policy deserves its own commit and its own
before/after suite run. The eleven files are named in `.gitattributes` for whoever takes it.

---

## 4 — MANIFEST TRACKING (operator ruling, census1b precedent)

Negations added; `mc2/` re-included **first**, because a negation cannot rescue a file under a
directory git was told not to descend into.

```
research_outputs/census2a/cen0_manifest.json               visible OK
research_outputs/census2a/census2a_manifest.json           visible OK
research_outputs/census2a/mc2/mc2_manifest_evidence.json   visible OK
research_outputs/census2a/mc2/mc2_manifest_live.json       visible OK
research_outputs/census2b/census2b_manifest.json           visible OK

BULK still ignored:
  census2a/cen1/cen1_events.parquet                        ignored OK
  census2b/cen2b_feasibility.parquet                       ignored OK
  census2a/mc2/evidence/feasibility_matrix.parquet         ignored OK
  census2b/crosses/x.parquet                               ignored OK

git status --porcelain -uall on both trees: exactly 5 files. GUARD_OK=1
```

**The manifests were TRACKED, never EDITED.** M2 established that their `D:\Naiad\…` path fields are
sealed provenance and that rewriting them would destroy the byte-equality with the LaCie copy which
is the two-witness proof for census2b's only unpinned file. Tracking changes none of that.

---

## 5 — POINTER.md + CONVENTIONS GEOGRAPHY

**`POINTER.md`** rewritten for v2: archives are working copies at
`~/Naiad/research_outputs/_archive`, backups on `/Volumes/LaCie/naiad-backups` + Drive cloud,
sidecars tracked, attestation chain stated in two lines (*git proves the tracked sidecars → the
sidecars attest the zips → basis (1), the strongest tier*). Permanent-evidence claim retained. The
old `D:`/`G:` map is preserved as an explicit *(Superseded: …)* line.

**`CONVENTIONS.md`**, three amendments, all following the standing correction-note rule — **the old
text is never deleted**:

- **§ "Local"** → `$HOME/Naiad`, with the two-sided gate restated for three cloud markers. The
  reason is now written down: *a cloud-synced tree corrupts bulk writes* — the sync client rewrites,
  relocates and locks files underneath a run.
- **§ residency** → v2 (local-first, LaCie backup-only, `drive_wait` on backup writes).
- **§ PowerShell / Git-Bash hazards** → dated 2026-08-15 note. Native bash, `chr(92)` and
  `PYTHONIOENCODING` hazards **retired on this platform**; hazard text kept verbatim as the
  Windows-era record. **What is NOT retired is stated explicitly:** `publish_exchange.py` still has
  no `__main__` block, so "call the function, never run the script" stands. The invocation line
  itself was corrected to `~/venvs/naiad/bin/python`.

---

## 6 — TIME MACHINE + SPOTLIGHT

### ✅ Time Machine — applied and READ BACK

```
BEFORE:  /Users/luis/Naiad/research_outputs   [Included]
         /Users/luis/.cache/naiad             [Included]
AFTER :  /Users/luis/Naiad/research_outputs   [Excluded]
         /Users/luis/.cache/naiad             [Excluded]
xattr com.apple.metadata:com_apple_backup_excludeItem present on both.
```

No sudo required. (`tmutil destinationinfo` reports no destinations configured — the exclusions are
in place for whenever one is.)

### 🟠 Spotlight — HALT-SOFT, needs the operator

`mdutil` **cannot target a subdirectory**:

```
$ mdutil -i off ~/Naiad/research_outputs
/System/Volumes/Data/Users/luis/Naiad/research_outputs:
Error: invalid operation.
	Error: unknown indexing state.
```

Current state, measured: **549 items under `research_outputs` are indexed.**

A `.metadata_never_index` marker was written in both directories (no sudo, reversible, gitignored) —
but **its efficacy for a subdirectory is not proven**, and I will not claim otherwise. The
authoritative exclusion needs the GUI privacy list or root.

**Operator, one of these:**

- **GUI (recommended):** System Settings → Siri & Spotlight → Spotlight Privacy… → `+` →
  add `~/Naiad/research_outputs` and `~/.cache/naiad`.
- **CLI, needs sudo:**
  ```
  sudo mdutil -i off -d /System/Volumes/Data && sudo mdutil -E /System/Volumes/Data
  ```
  ⚠️ that disables indexing for the **whole data volume**, which is almost certainly not what you
  want — the per-folder privacy list is the correct instrument. **Undo:**
  `sudo mdutil -i on /System/Volumes/Data`
- **Undo for the markers:** `rm ~/Naiad/research_outputs/.metadata_never_index
  ~/.cache/naiad/.metadata_never_index`
- **Undo for Time Machine:** `tmutil removeexclusion ~/Naiad/research_outputs ~/.cache/naiad`

---

## 7 — PROVE

### (a) Suite — 287 / 0 / 1, before and after

```
BEFORE (pre-edit, this session):  287 passed, 1 skipped in 14.64s
AFTER  (pre-commit):              287 passed, 1 skipped in 14.64s
```

**Delta: none. No fixtures added, and that is deliberate** — F-M3-3 and F-M3-6 were specified as
printed transcripts, not pytest fixtures, so the count is unchanged and directly comparable to the
M2 baseline. The single skip is `fixtures/test_f8_journal.py:110 — dry-run journal not generated yet
(D7)`, unrelated to this work.

### (b) 🔴 F-M3-6 — HALTED, NOT SKIPPED. THE LACIE IS DISCONNECTED.

**The LaCie was unmounted partway through this session.** It was attached for M2 (~8.7 GB was hashed
across it) and is now gone at the device layer:

```
$ mount | grep -i lacie          -> (nothing)
$ ls /Volumes                    -> Macintosh HD
$ diskutil list external         -> (empty)
$ system_profiler SPUSB/SPThunderbolt | grep -i lacie -> (nothing)
```

This is the same condition as HALT 2 on 2026-08-14: **no external device at the USB or Thunderbolt
layer.** It was diagnosed carefully rather than assumed — the first symptom was Python reporting
`os.path.exists('/Volumes/LaCie') == False` while an earlier `ls` had succeeded, which looks exactly
like a macOS permissions problem. It is not; the volume is genuinely absent.

**Consequence: the v2 backup WRITE path could not be proven live.** `--workflow` end-to-end,
bidirectional verification, 0 mismatches — none of it ran. **I am not reporting it as passed.**

What *was* proven, and is not nothing: the **negative** half of the same path, which is the half
that was broken. `backup_dest_root()` now halts correctly with a truthful 18.03 s measurement
instead of silently writing into the repo. The old code's failure mode is demonstrated above.

**F-M3-6 remains OUTSTANDING and is the first thing to run when the drive is reattached:**
```
~/venvs/naiad/bin/python scripts/backup_estate.py --workflow
```

### (c) Gate smoke — both PASS. Transcript in §2 above.

### (d) Live-code remainder — EMPTY

`116 → 74` raw matches. Filtering by **executable position** (Python `tokenize`, excluding COMMENT
and STRING tokens) rather than by crude text stripping:

```
=== LIVE-CODE HITS (executable position, comments/strings excluded) ===
  scripts/census2a_viz.py:145: f'xmlns="http://www.w3.org/2000/svg" style="background:{BG}">'
  scripts/census2b_wtb1.py:1251: f"result:\n  a 4-gram over this grammar is very nearly a campaign "

LIVE-CODE REMAINDER: 2
```

**Both are regex artifacts, not paths** — an SVG XML namespace URI, and the literal prose
`result:\n`. There is no live drive-letter path, no unguarded `LOCALAPPDATA`, and no `OUT.drive`
comparison left in executable position anywhere in `scripts/ engine/ fixtures/ tests/ study/
analytics/`.

The other 72 are comments and docstrings — **including several written by this session** that quote
the retired forms deliberately, so the next reader knows what changed and why.

---

## DISPOSITION TABLE

| item | disposition |
|---|---|
| §1 re-enumeration | ✅ 116 hits, classified 45 FIX / 7 HISTORY / 2 ALREADY-DEAD / 8 NOT-A-HIT + 54 core |
| §2 residency v2 | ✅ DONE — **2 real defects fixed**, both smoke-proven |
| §3 CRLF → LF + `.gitattributes` | ✅ DONE — F-M3-3 PASS 9/9, digests unchanged |
| §4 manifest tracking | ✅ DONE — exactly 5 files, bulk still ignored |
| §5 POINTER + CONVENTIONS | ✅ DONE — correction-note rule honoured throughout |
| §6 Time Machine | ✅ APPLIED and read back `[Excluded]` |
| §6 Spotlight | 🟠 **HALT-SOFT** — needs GUI or sudo; commands + undo above |
| §7a suite | ✅ 287 / 0 / 1 before **and** after, no delta |
| §7b F-M3-6 backup write | 🔴 **HALTED — LaCie physically disconnected.** Not run, not claimed |
| §7c gate smoke | ✅ both PASS |
| §7d empty remainder | ✅ EMPTY of defects (2 regex artifacts, printed) |
| commit / push | ✅ ONE commit `f403546`, 48 paths, pushed |
| `.gitattributes` over-reach | ✅ caught and reverted before commit |

**BOX COST:** this report ~19 KB + the CONVENTIONS/ledger deltas. ⚠️ `exchange/` measured **38.7 %**
of its 6,390,000 B budget at the last publish, and `publish()` **REFUSES above 40 %**. This report
pushes it closer. **Rotation is due before the next report lands.**

---

## LEDGER — APPENDED

`exchange/status/LEDGER_ATHENA.md`, this date, per the brief.

---

# 🔴 BRIGHT COLOURS — WHAT THE OPERATOR MUST DO NEXT

## 🟢 CENSUS WORK IS UNBLOCKED

Both census programs run their gates to PASS on this Mac. `census2a_program.py` and
`mc2_program.py` could not previously reach step 1 — their residency assertions were unsatisfiable.
The substrate is local and verified, the estate is live, the suite is green. **Nothing in the sweep
is blocking census work.**

## 🔴 1 — REATTACH THE LACIE, THEN RUN F-M3-6

The drive was unmounted partway through this session. It is not a permissions problem — there is no
external device at the USB or Thunderbolt layer. **One proof did not run because of it**, and it is
the one that matters most for backups:

```
~/venvs/naiad/bin/python scripts/backup_estate.py --workflow
```

Until that runs, **the v2 backup write path is fixed but unproven end-to-end.** The halt path *is*
proven.

## 🔴 2 — YOUR BACKUPS COULD HAVE BEEN LANDING INSIDE THE REPO

This is the finding to read twice. On macOS the old guard could not fail, and the old default
`D:/naiad-backups` is a **relative** path on POSIX — so `--estate`/`--workflow` would have written
**into `~/Naiad/D:/naiad-backups`**, inside the repo they were backing up, and printed success.

Nothing indicates this ever ran on this Mac (no such directory exists). But **if any backup was
taken on this machine before today, check for it** — and treat any backup taken here since the
crossing as unverified until F-M3-6 passes.

## 🟠 3 — SPOTLIGHT NEEDS YOU (the one sudo/GUI item)

549 items under `research_outputs` are indexed. `mdutil` cannot exclude a subdirectory. Use
**System Settings → Siri & Spotlight → Spotlight Privacy…** and add `~/Naiad/research_outputs` and
`~/.cache/naiad`. Time Machine is already done and verified.

## 🟠 4 — EXCHANGE BOX IS AT ~40 % AND `publish()` REFUSES ABOVE IT

`publish()` warned at 38.7 % last run. Rotation is due **before** the next report, or the next
publish fails closed.

## 🟡 5 — A DECISION I DEFERRED RATHER THAN TOOK

Eleven source files are still CRLF. Pinning `*.py` to LF would re-normalise all eleven — a
15,000-line diff. I kept `.gitattributes` to `*.sha256` only and listed the eleven files there.
**Line-ending policy for source is your call, in its own commit.**

## 🟢 6 — M4 IS NEXT

M3 is green apart from the two items above (F-M3-6 blocked on hardware, Spotlight blocked on
sudo/GUI). Neither blocks M4 and neither blocks census work.
