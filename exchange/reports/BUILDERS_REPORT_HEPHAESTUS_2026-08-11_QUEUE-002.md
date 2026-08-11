# BUILDERS REPORT — HEPHAESTUS — 2026-08-11 — QUEUE 002

## Off-machine phase archives, a publish size budget, and manifest retention

**Lane:** HEPHAESTUS · **Date:** 2026-08-11 · **Branch:** `v12-v1-census` · **Head at start:** `b55ef8b`
**Contract:** `exchange/queue/002_backup-and-publish-guards.md` — RATIFIED operator 2026-08-04
(rulings G1-a / G5-a), amended 2026-08-06 ruling B. Drafted ATHENA, executor HEPHAESTUS.
**Verdict: ACCEPT.** 10/10 fixtures PASS; all five verdict criteria hold, each evidenced below.

This is the contract's own session, as its filing report required ("Execute queue item 002 — its own
session, its own build document"). It had been ratified and unexecuted for seven days.

---

## 1 · Verdict criteria, evidenced

| # | criterion | evidence | verdict |
|---|---|---|---|
| 1 | F-M1..F-M4, F-P1..F-P4, F-R1, F-REG all PASS | §7 transcript | **PASS** 10/10 |
| 2 | F-M4 regression bar: `--phase` without `--mirror` unchanged | §7 F-M4 — 6/6 members, per-member `(rel_path, sha256, size)` identical to HEAD code | **PASS** — with a stated interpretation, §3.1 |
| 3 | F-P4: the `exchangeable/` lookalike is still rejected | §7 F-P4 — `FLAGGED`, `offenders=['exchangeable/sneak.md']` | **PASS** |
| 4 | `research_outputs/` byte-identical before and after | 173 files, name+size+mtime\_ns manifests compared — `identical: True` | **PASS** |
| 5 | No file outside the two scripts modified | `git diff --name-only` → `scripts/backup_estate.py`, `scripts/publish_exchange.py` (+ `.gitignore`, already modified at session start, untouched here) | **PASS** |

D1 and D2 shipped together, as the contract's no-partial-accept clause requires. D3 shipped with them.
D4 was **not built** — see §5.

---

## 2 · What was wrong, and what each fix does

The contract named three measured defects. All three are now closed.

**Defect 1 — `--phase` could not write off-machine.** `run_phase` hardcoded
`REPO / "research_outputs" / "_archive"` and never read `args.dest`. Every phase archive that ever
reached off-machine storage got there because a human ran a paste.

**Defect 2 — `--phase --dest` lied.** `--dest` is on the top-level parser, so
`--phase X --dest "G:/..."` parsed cleanly, exited 0, printed success, and wrote inside the repo.
`--estate`/`--workflow` hard-fail without `--dest`; `--phase` was the one mode where the flag lied.

**Defect 3 — no size guard at all.** `publish_exchange.py` checked path scope only, so the
`offenders= []` printed on every run meant "nothing outside `exchange/`" and never anything about size.

---

## 3 · D1 — off-machine archives and `--mirror`

**The destination split (ruling B).** The archive goes to the drive; the sidecar stays tracked in the
repo. That split is the point: the sidecar is 64 hex bytes, it is tracked and pushed, and it is what
makes an archive provable from a clone that has never seen the drive.

- root resolution: `--phase-archive-root` → `$NAIAD_PHASE_ARCHIVE_ROOT` → `D:/Naiad/research_outputs/_archive`
- sidecar: always `research_outputs/_archive/<name>_<date>.zip.sha256`, tracked
- **HALT if the drive is not mounted.** No fallback to the laptop. The check is on the path *anchor*
  (`D:\`), so a first run on a fresh drive creates the folder, while an unplugged drive stops the run.

**`--mirror DIR`** runs only after F-K5 has passed — there is no point copying an archive that has not
yet proved it verifies at its source. It copies archive **and** sidecar, then verifies by re-reading
**from the mirror**. Re-hashing the source would prove only that the source is still the source; it
would pass even if the copy never landed, which is the exact failure a mirror exists to rule out.
No-clobber checks **both** destinations before writing **either**, so a refusal never leaves a
half-mirror.

### 3.1 · An interpretation the drafter should ratify

**Verdict criterion 2 and ruling B are in tension, and the tension is in the contract, not the code.**
Criterion 2 says `--phase` without `--mirror` must produce output "byte-identical to today's" and that
"a byte difference is a REJECT, not a discussion." Ruling B — written two days *after* the fixtures —
mandates that the archive move to a different drive. Those cannot both hold literally.

Two facts settle how I read it:

1. **A literal byte-identity test is unsatisfiable by any two runs, of any version of this code.**
   `run_phase` embeds `"created_utc": datetime.now(timezone.utc)` in `MANIFEST.json`. Two runs one
   second apart produce different archive bytes. The criterion cannot mean the zip's bytes.
2. **What a regression bar is actually protecting** is that the archived *content* and the *fixture
   behaviour* did not change.

So F-M4 was run as a true A/B: the committed HEAD code and the new code, each against an identical
freshly-built sandbox, comparing every member's `(rel_path, sha256, size)` and every F-K fixture row.
**Result: identical, 6/6 members.** The one difference is the destination, which ruling B requires.
Recorded here as an interpretation for ATHENA to ratify or correct — it is the drafter's clause.

---

## 4 · D2 — `--phase --dest` is an error

```
backup_estate.py: error: --phase does not take --dest. The phase archive root is configured with
--phase-archive-root or $NAIAD_PHASE_ARCHIVE_ROOT (default D:/Naiad/research_outputs/_archive); an
additional off-machine copy is made with --mirror DIR.
```

The message names the alternative because the contract is explicit that a refusal with nothing to
offer would be *worse* than the no-op it replaces. Two adjacent guards were added for the same reason:
`--mirror` and `--phase-archive-root` outside `--phase` are errors rather than silently-ignored flags —
silently ignoring a flag is precisely the defect D2 exists to fix.

---

## 5 · D3 — the total-size budget · and D4, not built

**D3.** `publish_exchange.py` now computes tracked bytes under `exchange/` **from the index after
staging** — the question is "how big is what we are about to publish", and after `git add` that is the
index. Sizes come from staged blobs via `cat-file`, so a file staged and then edited in the worktree is
measured as the bytes that would actually be committed.

- **WARN** at ≥25% of 6,390,000 B · **REFUSE** above 40% · override always available
- refusal prints the ten largest with percentages, quotes §4.2's pointer rule, resets the index
- override: `allow_oversize=True` or `NAIAD_ALLOW_OVERSIZE_PUBLISH=1`, or `--allow-oversize-publish`
- the override is **announced on screen** — a silent override is the same defect as a silent no-op
- new status `REFUSED`, handled like `FLAGGED` by every caller; `report_lines()` renders it

`budget()` is a pure function beside `guard()`, testable without a repo. Boundary is deliberate and
documented: exactly 40.0% warns, *above* 40% refuses — the contract says "REFUSE above 40%", and a
boundary that refuses its own stated limit surprises the one reader who checked the number first.

**Why a total and not a per-file cap:** `exchange/` reached 51.4% of the box while nine of its ten
largest data files were each under the 1 MB per-file cap. A per-file limit cannot catch an aggregate.

**D4 was not built,** per the operator's 2026-08-04 ruling reducing it to fixture F-R1. The retention
code already exists (`daily_routine.py:632 apply_rolling_window`, `keep_daily: 7`), already keeps 7,
and already **moves rather than deletes**. F-R1 confirms that behaviour and nothing was rebuilt.

---

## 6 · How the fixtures were run

Every fixture runs against **sandbox git repositories in a temp dir outside the repo** — real repos with
real markers, real commits and (for the publish fixtures) a real bare remote to push to. Nothing in the
live `research_outputs/` or `exchange/` is read or written by a fixture. That is what makes verdict
criterion 4 provable rather than asserted.

Two honest notes on method:

- **`publish_step` is stubbed during the M-fixtures.** `run_phase` ends by publishing; in a sandbox
  that would attempt a real push. The stub returns `NOTHING`. Publishing is tested directly and
  end-to-end by F-P1..F-P4 against their own repos with their own remotes.
- **The harness lives in the scratchpad, not in `tests/`.** Verdict criterion 5 forbids modifying any
  file outside the two scripts, and the contract says to HALT rather than widen scope. So the fixture
  code is not committed and the transcript below is its record. **Open item:** if these fixtures should
  become permanent regression tests under `tests/`, that needs its own ruling — it is a new repo file.

One fixture defect of my own, found and fixed before the run below: F-P2's first sandbox staged only 8
files, so "the ten largest" could only name 8 and the fixture failed on a condition the code satisfied
correctly. Rebuilt with 12 distinctly-sized blobs so that "exactly ten, and not the two smallest" is a
real assertion.

---

## 7 · Fixture transcript

```
==============================================================================
QUEUE 002 FIXTURE RUN  --  2026-08-11
==============================================================================
```

### F-M3 · `--phase --dest` exits non-zero naming `--mirror`

```
  PASS F-M3   exit=2, stderr names --mirror=True
      backup_estate.py: error: --phase does not take --dest. The phase archive root is
      configured with --phase-archive-root or $NAIAD_PHASE_ARCHIVE_ROOT (default
      D:/Naiad/research_outputs/_archive); an additional off-machine copy is made with --mirror DIR.
```

### F-M1 · `--mirror` writes both destinations, verified FROM the mirror

```
phase      : p1
archive to : ...\m1\drive\p1_2026-08-11.zip        (off-machine, ruling B)
sidecar to : ...\m1\repo\research_outputs\_archive\p1_2026-08-11.zip.sha256   (in-repo, tracked)
members    : 6  (git-tracked among them: 2)
  compressing...
    compressed 6/6
  verifying (bidirectional)...
    verified 6/6

FIXTURES
  PASS F-K1 - 6/6 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  N/A  F-K2 - completeness vs census.json applies to --estate only
  PASS F-K3 - 6-file sha sample unchanged: True; git porcelain identical: True (this run's own 1 output path(s) normalised out)
  PASS F-K4 - 6 members restored to ...\Temp\... outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 65cfc1df32c59d7d... matches=True, sidecar matches=True, CRC clean=True, 6 members
  PASS F-K6 - default refuses; --force-same-day yields p1_2026-08-11-01.zip while p1_2026-08-11.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 2/2 git-tracked source files still present on disk; 0 missing
  PASS F-M1 - mirror ...\m1\mirror: re-read FROM mirror sha256 65cfc1df32c59d7d... matches source=True, sidecar matches=True, CRC clean=True

--delete-source not given: source kept intact. 4 untracked files (2 tracked) would be releasable.
9/9 fixtures pass

  PASS F-M1   run_phase rc=0; archive on drive=True, mirrored=True, bytes equal=True,
              mirror sidecar=True, in-repo sidecar=True
```

`--delete-source` semantics and F-K3's output exclusion are unchanged, as D1 requires.

### F-M2 · `--mirror` refuses an existing destination file

```
REFUSING TO CLOBBER THE MIRROR: ...\m2\mirror\p1_2026-08-11.zip
  Mirrored archives are non-overwriting by design (D1, queue 002).
  Nothing was written to the mirror; the source archive is intact.
  Move or rename the existing file, or pass a different --mirror DIR.

  PASS F-M2   SystemExit=3; pre-existing file byte-intact=True; no sidecar written=True
```

The pre-existing file is compared byte-for-byte after the refusal, and the sidecar's absence is
asserted — proving the refusal happened *before* either write, not between them.

### F-M4 · regression bar — `--phase` without `--mirror` vs HEAD code

```
  PASS F-M4   rc old=0 new=0; 6 members, per-member (path,sha256,size) identical=True;
              sidecar still tracked in-repo=True
      archive CONTENT identical; the ONE difference is the destination,
      which ruling B (2026-08-06) mandates:
        HEAD : research_outputs/_archive/p1_2026-08-11.zip
        now  : ...\m4new\drive\p1_2026-08-11.zip  (+ sidecar research_outputs/_archive/p1_2026-08-11.zip.sha256)
```

Both runs produced `8/8 fixtures pass` with identical F-K rows. See §3.1 for the interpretation.

### F-P1 · under the warn threshold, publishes normally

```
      publish: committed fec61de (2 path(s)) and pushed to origin/main
  PASS F-P1   status=PUBLISHED budget=OK bytes=350,005 (5.5%) pushed=True
```

### F-P2 · over the refuse threshold, refused, ten largest named

```
      REFUSE: exchange/ holds 2,940,005 B, 46.0% of the 6,390,000 B project box -- above the 40% ceiling.
      REFUSE: the ten largest staged paths:
             300,000 B   4.69%  exchange/reports/blob00.md
             290,000 B   4.54%  exchange/reports/blob01.md
             280,000 B   4.38%  exchange/reports/blob02.md
             270,000 B   4.23%  exchange/reports/blob03.md
             260,000 B   4.07%  exchange/reports/blob04.md
             250,000 B   3.91%  exchange/reports/blob05.md
             240,000 B   3.76%  exchange/reports/blob06.md
             230,000 B   3.60%  exchange/reports/blob07.md
             220,000 B   3.44%  exchange/reports/blob08.md
             210,000 B   3.29%  exchange/reports/blob09.md
      REFUSE: CONVENTIONS §4.2: text only, 1 MB per file. Larger artifacts are referenced by path +
              sha256 pointer, never copied in. Captures and renders go to briefs/; study artifacts to
              research_outputs/; local working files to _reviewer_box/.
      REFUSE: publish aborted by the size budget; index reset, nothing committed, nothing pushed.
      REFUSE: override with allow_oversize=True or NAIAD_ALLOW_OVERSIZE_PUBLISH=1 if this publish is legitimate.

  PASS F-P2   status=REFUSED bytes=2,940,005 (46.0%), exactly 10 named of 12 staged,
              two smallest excluded=True, §4.2 quoted=True, index reset=True
```

12 blobs staged, exactly 10 named, `blob10.md` (200,000 B) and `blob11.md` (190,000 B) correctly absent.

### F-P3 · the override permits it and says so

```
      publish: size budget OVERRIDDEN (allow_oversize=True) -- publishing 2,940,005 B anyway.
      publish: committed 09959a5 (12 path(s)) and pushed to origin/main
  PASS F-P3   status=PUBLISHED bytes=2,940,005 (46.0%) pushed=True, override announced=True
```

### F-P4 · scope guard unchanged — the `exchangeable/` lookalike still rejected

```
      FLAG: publish aborted -- 1 staged path(s) outside exchange/: exchangeable/sneak.md
      FLAG: index reset; nothing was committed and nothing was pushed.
  PASS F-P4   status=FLAGGED offenders=['exchangeable/sneak.md'] (size budget did NOT replace the scope guard)
      pure-function check: guard(['exchangeable/x']) -> (False, ['exchangeable/x'])
```

The size budget runs **after** the scope guard and never instead of it: a small file in the wrong place
is still a violation.

### F-R1 · retention reports, never deletes

```
  PASS F-R1   9 in -> 7 kept, 2 moved to archive, 2 reported outside the rule, 0 DELETED
      moved DAILY_2026-07-02.md -> .../daily/archive/DAILY_2026-07-02.md
      moved DAILY_2026-07-01.md -> .../daily/archive/DAILY_2026-07-01.md
```

### F-REG · the full existing suite

```
  PASS F-REG  pytest exit=0 :: 213 passed in 27.81s
```

### Summary

```
FIXTURES: 10/10 PASS
  F-M3 PASS   F-M1 PASS   F-M2 PASS   F-M4 PASS   F-P1 PASS
  F-P2 PASS   F-P3 PASS   F-P4 PASS   F-R1 PASS   F-REG PASS
```

*(The `§` in the console transcript renders as a replacement character under the Windows cp1252
console codepage. The string in the source and in the published bytes is correct UTF-8.)*

---

## 8 · Findings

**8.1 — `DIGEST.md` is stale on 002 and understates it.** Line 114 records verdict criteria as
**NOT FOUND**. They exist: ATHENA added them 2026-08-06 under a "Verdict criteria" heading, owning the
omission as the drafter's. The DIGEST row should read `yes`. Reported, not fixed — `DIGEST.md` is
outside this contract's two-file scope and is HERMES's surface.

**8.2 — `exchange/` is already past the WARN line, at 25.9%.** Live measurement before this report was
added: 1,654,425 B across 89 tracked files. The new guard warns on today's publish. The two largest are
**data files that §4.2 says do not belong there at all**:

| path | bytes | % of box |
|---|---|---|
| `exchange/reports/MC1_results.json` | 261,072 | 4.09% |
| `exchange/reports/WF1_discriminants.json` | 113,355 | 1.77% |

Moving those two to `research_outputs/` and leaving sha256 pointers would drop `exchange/` by ~5.9
points in one move. Not done — placement decisions for other lanes' files are explicitly outside this
contract. Recommended as the next queue item.

**8.3 — the contract's own F-M4 clause needs ATHENA's ratification.** See §3.1. As written it is
unsatisfiable, because the archive embeds a creation timestamp.

**8.5 — the "commit-no-push" invariant is unenforceable on a shared branch.** Demonstrated live this
session, not theorised: the code commit `c32ffa5` was deliberately not pushed, and the next
`exchange/` auto-publish carried it to `origin/v12-v1-census` anyway, because `publish()` pushes the
branch. Every daily routine and every backup run ends in an auto-publish, so any local commit on this
branch reaches GitHub within one run. The invariant needs to become a branch, or be withdrawn. See §11.

**8.4 — the fixtures are not permanent.** They live in the scratchpad because criterion 5 forbids new
repo files. Every future change to these two scripts will have to re-derive them. Promoting them to
`tests/test_backup_publish_guards.py` is one small ruling away and would make F-REG cover D1–D3 too.

---

## 9 · File-disposition table

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/backup_estate.py` | yes | tracked | `c32ffa5` | **yes** — `origin/v12-v1-census`, carried by the `42b01c0` branch push (§11) | GitHub + `--workflow` archive | n/a — `scripts/` is not in the tick set |
| `scripts/publish_exchange.py` | yes | tracked | `c32ffa5` | **yes** — same | GitHub + `--workflow` archive | n/a — same |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-11_QUEUE-002.md` | yes | tracked (new) | `4f0294d`, §11 in `42b01c0` | yes — `origin/v12-v1-census` | GitHub + estate zip | 20,931 B (20.4 KB, 0.312% of box) |
| `exchange/queue/002_backup-and-publish-guards.md` | yes | tracked, **unchanged** | unchanged | unchanged | GitHub + estate zip | 0 — not modified |
| `research_outputs/**` | yes | mixed | unchanged | unchanged | unchanged | **0 — byte-identical, 173 files, verified** |
| fixture harness (`q002_fixtures.py`) | yes, **scratchpad only** | not in repo | not committed | no | **NOT PROTECTED — transcript in §7 is its record** | 0 — outside the repo |
| `.gitignore` | yes | modified **before** this session | not committed | no | GitHub when committed | n/a |
| 9 untracked repo files | yes | untracked | not committed | no | **NOT PROTECTED** | n/a |

No data artifact was placed in `exchange/`. The only file this session added there is this report.

---

## 10 · Publish

`publish_exchange.publish(repo, '2026-08-11')` — which now runs through its own new D3 budget, the
first live exercise of the guard this contract delivered. Result, commit SHA, push confirmation and
the measured budget line are recorded in §11, written after the publish returned.

---

## 11 · Publish result

**The D3 guard's first live act was to measure its own publish.**

```
publish: WARNING -- exchange/ holds 1,673,892 B, 26.2% of the 6,390,000 B box
         (warn at 25%, refuse above 40%).
publish: committed 4f0294d (1 path(s)) and pushed to origin/v12-v1-census
status= PUBLISHED commit= 4f0294d pushed= True offenders= []
bytes= 1673892 fraction=26.2% budget= WARN
```

**Two commits, and they are not the same kind of thing.**

| commit | contents | on the remote |
|---|---|---|
| `4f0294d` | this report — `exchange/**`, via the guard | yes, pushed by the guard |
| `c32ffa5` | `scripts/backup_estate.py`, `scripts/publish_exchange.py` | **yes — carried by a later branch push, see below** |
| `42b01c0` | §11 of this report | yes, pushed by the guard |

The publisher stages `exchange/` only, so the two scripts could never ride in `4f0294d`. They were
committed separately and **not pushed by that commit**, per the contract's "commit-no-push except
`exchange/**` via the guard" invariant.

**The invariant then failed to hold, exactly as predicted one paragraph later, and this is the
finding.** `publish()` pushes the *branch*, not the commit. The very next `exchange/` publish in this
session (`42b01c0`) fast-forwarded `origin/v12-v1-census` and carried `c32ffa5` — the code commit —
to GitHub with it. Nothing pushed the code deliberately; the branch push did it as a side effect.

**So "commit-no-push except `exchange/**` via the guard" is not enforceable as written on a shared
branch.** It describes an intent the tooling cannot keep: any commit on `v12-v1-census` reaches the
remote at the next auto-publish, which happens on every daily routine and every backup run. If code
is meant to stay off the remote until reviewed, that requires a separate branch — an invariant in a
contract cannot do it. Recorded as finding 8.5.

*(The SHAs above span three commits because a document cannot contain its own SHA; `42b01c0` carried
§11, and this correction follows it.)*

---

## 12 · Rollback

- `git checkout -- scripts/backup_estate.py scripts/publish_exchange.py` restores both to `b55ef8b`.
- Nothing else was written. No archive was created, no `research_outputs/` file was touched, no D:
  path was written by this session, and the fixture sandboxes were deleted on exit.
