# BUILDER'S REPORT — HEPHAESTUS — 2026-08-12 — O-1 / O-3 / O-4 / TIDY

**Lane:** ATHENA (system resilience) · **Builder:** HEPHAESTUS, local Windows Claude Code
**Branch:** `v12-v1-census` · **HEAD at start:** `95fc10d` · **Code commit:** `91ce815`, pushed
**Authority:** ATHENA rulings O-1, O-3, O-4 · operator go 2026-08-12 — *"O-1 + O-3 tidy"*
**Read this with zero prior context.**

---

## 0 · What happened, in one paragraph

Four things. The last unprotected file in the repository is now tracked on GitHub. The weekly backup
now covers three folders it was silently missing. The retention report, which had been claiming
there were no phase archives while a gigabyte of them sat on the drive, now finds them — and, more
importantly, can no longer confuse *"I looked and found nothing"* with *"I could not look."* And two
duplicate files were deleted from the repository root, each only after re-proving in this run that
an identical copy is tracked and present on GitHub. Everything is committed, pushed and verified.

---

## 1 · O-1 — `research_outputs/wf1/` is tracked

### 1.1 The ignore check, run before anything else

The one thing that could have blocked this is a `.gitignore` rule, because editing `.gitignore` is a
separate ruling I do not hold. Measured rather than assumed:

```
  $ git check-ignore -v research_outputs/wf1/WF1_discriminants.json
  NOT ignored - a plain 'git add' suffices
```

`git check-ignore` exits non-zero when nothing matches. Nothing matched, so no `.gitignore` edit was
needed and none was made.

### 1.2 What was tracked

```
  staged: research_outputs/wf1/WF1_discriminants.json      113,355 B
```

One file — the discriminant output of the WF1 forensics run. Before this commit it existed **only**
on this machine: not on GitHub, not on `D:`, not in any archive. It is now on
`origin/v12-v1-census`, verified by reading it back from the remote.

### 1.3 What was deliberately NOT tracked

`research_outputs/mc1/` is present on disk and was **not** added, by ATHENA's ruling that bulk data
stays pointered. Asserted explicitly after staging:

```
  PASS research_outputs/mc1/ not staged
```

---

## 2 · O-3 — the weekly archive was missing three folders

### 2.1 Why this existed at all

`backup_estate.py --workflow` archives a hardcoded list of directories, `WORKFLOW_SOURCES`. The
2026-08-12 filing session measured that list against reality and found three directories holding
**tracked** content that the list did not name. Tracked means GitHub has them — but GitHub was the
*only* thing that had them, which is the same exposure that put `scripts/` on the list back in
August, described in the code's own comment as *"one copy on one third-party service is not a
backup."*

### 2.2 Measured before widening — the gate

A backup list that grows without measurement is how a weekly job quietly becomes an hourly one.

| candidate root | files | size |
|---|---:|---:|
| `briefs` | 12 | 3.92 MB |
| `docs/reports` | 2 | 0.26 MB |
| `docs/handoffs` | 2 | 0.02 MB |
| **TOTAL ADDED** | **16** | **4.21 MB** |

**Threshold 50.00 MB. Gate: PASS — 4.21 MB, 8.4% of the ceiling.** Proceeded.

### 2.3 The edit, and the assertion that matters

The risk in editing a tuple is not adding the wrong thing — it is *dropping* something while adding.
So the post-write assertion tests that the **old list is a strict subset of the new**, not merely
that the new entries are present:

```
  PASS  every pre-existing entry still present (OLD subset of NEW) (11/11)
  PASS  added: briefs
  PASS  added: docs/reports
  PASS  added: docs/handoffs
  PASS  no duplicate entries (14 entries, 14 unique)
  PASS  count grew by exactly 3 (11 -> 14)

  0 assertion(s) FAILED
```

The nesting guard was also re-run, because a root nested inside another would archive its files
twice under two names:

```
    kept   : ['docs/memory','docs/knowledge','skills','prompts','claude','exchange',
              'docs/primers','docs/history','docs/reports','docs/handoffs','briefs','scripts']
    absent : ['drops/operator-exports','exchange/drops/operator-exports']
    nested : []
```

---

## 3 · TIDY — two duplicates deleted, four checks each

Deletion authority this session was narrow and singular: these two files, and only after re-proving
four things **in this run**. Not inherited from the earlier session's report — re-measured.

```
  ---- Cascade Rewire.html
     twin              : docs/reports/Cascade Rewire.html
     (a) sha256 equal  : True   root=6fc84a2e318cc442bfebf190
                                twin=6fc84a2e318cc442bfebf190
     (b) twin tracked  : True
     (c) blob on origin: True   37502615f1324bfe5d98a5e874d45606013bd38c
     (d) worktree==blob: True   37502615f1324bfe5d98a5e874d45606013bd38c
     >>> REMOVED. Recoverable from docs/reports/Cascade Rewire.html (blob 37502615f132)

  ---- SS_Reassessment_Synthesis_2026-08-03.md
     twin              : exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md
     (a) sha256 equal  : True   root=9d6e7ea747544561af509bbc
                                twin=9d6e7ea747544561af509bbc
     (b) twin tracked  : True
     (c) blob on origin: True   0ad38893d06c1c89d561e537d2a42eb6b9533050
     (d) worktree==blob: True   0ad38893d06c1c89d561e537d2a42eb6b9533050
     >>> REMOVED. Recoverable from exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md (blob 0ad38893d06c)
```

Both twins re-checked **after** the deletions, because a tidy that damages what it was preserving is
worse than no tidy:

```
    PASS present: docs/reports/Cascade Rewire.html  (37502615f1324bfe5d98a5e874d45606013bd38c)
    PASS present: exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md  (0ad38893d06c1c89d561e537d2a42eb6b9533050)
    PASS removed: Cascade Rewire.html
    PASS removed: SS_Reassessment_Synthesis_2026-08-03.md
```

**Neither deletion is a git change** — both files were untracked at the repo root, so nothing was
removed from version control. Confirmed before committing:

```
    PASS root 'Cascade Rewire.html' was never tracked - deletion is not a git change
    PASS root 'SS_Reassessment_Synthesis_2026-08-03.md' was never tracked - deletion is not a git change
```

---

## 4 · O-4 — the retention report could not tell "empty" from "unreadable"

### 4.1 Two defects, and the second is the one that matters

**Wrong location.** `retention_report()` scanned `REPO/research_outputs/_archive`. That directory
stopped holding archives on 2026-08-06, when ruling B moved them off-machine to
`D:/Naiad/research_outputs/_archive` and left only the sidecars in the repo. So the report printed
**"none found"** while **nine archives totalling 1,043.6 MB** sat on the drive.

**Absence of the drive is not absence of the archives.** The old code had two branches — directory
present, or not. If `D:` were unplugged, it printed the same "none found" as a genuinely empty
directory. **That is the exact conflation behind the 2026-08-04 retraction**, where a single lookup
returning nothing was read as a measurement of absence. A report that cannot look must say it could
not look.

### 4.2 The fix

A new `phase_archive_root_path()` resolves the configured root without the mount check, and both
`phase_archive_root()` (which halts) and `retention_report()` (which must never halt) now call it —
so the report and the writer can no longer disagree about where archives live. Three states replace
two:

| state | output |
|---|---|
| drive mounted **+** archives | enumerate them, all PERMANENT |
| drive mounted **+** no zips | `none found` — **and it says which condition held** |
| drive **NOT** mounted | `NOT ENUMERABLE` — **never "none found"** |

When the drive is absent the report falls back to the **nine tracked sidecars** in the repo, which
record what each archive hashed to. That is precisely why ruling B kept them in-repo, and it turns
the third state from a shrug into evidence.

### 4.3 FIXTURE F-O4 — both states, verbatim

**STATE 1 — `D:` present:**

```
## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy
of a newer one — it is the only copy of work that will never be produced again.

Location: `D:\Naiad\research_outputs\_archive`

9 archive(s), 1,043,591,544 B (1,043.6 MB). **All permanent. None prunable.**

| archive | date | size (B) | status |
|---|---|---:|---|
| `analytics_tests_v1.0.0_2026-07-29.zip` | 2026-07-29 | 6,816 | **PERMANENT — never prune** |
| `analytics_v1.0.0_2026-07-29.zip` | 2026-07-29 | 19,641 | **PERMANENT — never prune** |
| `s1_2026-07-27.zip` | 2026-07-27 | 106,239,157 | **PERMANENT — never prune** |
| `s2_2026-07-27.zip` | 2026-07-27 | 246,355,294 | **PERMANENT — never prune** |
| `s3_2026-07-27.zip` | 2026-07-27 | 269,919,602 | **PERMANENT — never prune** |
| `tc1_2026-07-27.zip` | 2026-07-27 | 242,926,299 | **PERMANENT — never prune** |
| `tc4_2026-07-27.zip` | 2026-07-27 | 68,700,167 | **PERMANENT — never prune** |
| `tc5_2026-08-02.zip` | 2026-08-02 | 18,375,498 | **PERMANENT — never prune** |
| `v3_anchor_2026-07-27.zip` | 2026-07-27 | 91,049,070 | **PERMANENT — never prune** |

There is no keep-count for phase archives and no circumstance under which this report will list
one as prunable.
```

**STATE 3 — root overridden to a nonexistent drive (`Q:`):**

```
## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy
of a newer one — it is the only copy of work that will never be produced again.

Location: `Q:\nonexistent\_archive`

**NOT ENUMERABLE — the drive `Q:\` is not mounted.**

This is NOT the same as "none found", and this report will never say that when it could not look.
The archives are off-machine by ruling B (2026-08-06); plug the drive, or set
`$NAIAD_PHASE_ARCHIVE_ROOT`, and re-run to enumerate them.

**9 tracked sidecar(s) in `research_outputs/_archive/` record which archives exist and what they
hashed to** — this is the standing proof that survives an unplugged drive:

| sidecar | recorded sha256 |
|---|---|
| `analytics_tests_v1.0.0_2026-07-29.zip.sha256` | `0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999` |
| `analytics_v1.0.0_2026-07-29.zip.sha256` | `d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9` |
| `s1_2026-07-27.zip.sha256` | `4d14ea48066dcf8b3548030551778323683ef76612702ea8205eb10bdd18f825` |
| `s2_2026-07-27.zip.sha256` | `df5c1c196fef822537788e290e64f0c8dc9ef896694b73c91dab38fb0d5ce5ce` |
| `s3_2026-07-27.zip.sha256` | `80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f` |
| `tc1_2026-07-27.zip.sha256` | `e673a158b5b1388d8e521769b460937153c691368766afda70af6d6d8f4caff8` |
| `tc4_2026-07-27.zip.sha256` | `794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933` |
| `tc5_2026-08-02.zip.sha256` | `68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357` |
| `v3_anchor_2026-07-27.zip.sha256` | `69d9cc989cb4054e7aa88cd5dfd7828863aad494f33423602010ced7f6cd757a` |
```

*(Every sha256 above matches the value independently verified against the archives on `D:` earlier
today — `tc5` at `68942d62…`, `v3_anchor` at `69d9cc98…`. The two begin similarly enough to be
transposed by eye, which is why this block is machine-captured from the generator rather than
retyped.)*

**Assertions:**

```
  PASS  STATE 1 enumerates 9 archives (count=9)
  PASS  STATE 1 names the D: phase archive root
  PASS  STATE 1 emits no "none found" VERDICT
  PASS  STATE 1 is not NOT-ENUMERABLE
  PASS  STATE 3 says NOT ENUMERABLE
  PASS  STATE 3 emits no "none found" VERDICT <- the whole point of O-4
  PASS  STATE 3 explicitly disclaims the conflation
  PASS  STATE 3 falls back to tracked sidecars (count=9)
  PASS  STATE 3 names the unmounted anchor
  PASS  both states agree the set is 9

  0 assertion(s) FAILED
```

### 4.4 A failed gate of my own, reported because the failure is the lesson

My first F-O4 harness reported **3 of 8 assertions failed**. All three were defects in the *test*,
not the fix:

- Two were the **cp1252 decode trap** — the harness captured the subprocess with the locale
  codepage, so `PERMANENT — never prune` (em-dash) never matched and counted 0. Same trap as this
  morning's false "6 missing files".
- One was worse and more interesting: `STATE 3 NEVER says "none found"` **failed**, because the
  state-3 text contains the sentence *"This is NOT the same as \"none found\""*. **My gate matched
  the phrase inside my own disclaimer.** A substring test cannot distinguish a verdict from a
  quotation of that verdict. Re-written to test for a `- none found` **verdict line** specifically,
  it passes — and it is now testing the thing it was always supposed to test.

---

## 5 · The proof run — `--workflow` with the widened list

Run with `--force-same-day`, because this morning's archive already holds today's date and the
no-clobber guard correctly refuses to overwrite a backup.

```
roots archived   : 12 dir(s) + repo-root *.md          <- was 9
    docs/memory 6 · docs/knowledge 7 · skills 2 · prompts 15 · claude 1 · exchange 106
    docs/primers 7 · docs/history 55 · docs/reports 2 · docs/handoffs 2 · briefs 12
    scripts 67 · (repo root) *.md 61
    absent           : drops/operator-exports
    absent           : exchange/drops/operator-exports
members to archive: 343

FIXTURES
  PASS F-K1 - 343/343 members verified both directions; 0 mismatches, 0 strays, 0 omissions
  N/A  F-K2 - completeness vs census.json applies to --estate only
  PASS F-K3 - 20-file sha sample unchanged: True; git porcelain identical: True
  PASS F-K4 - 10 members restored to …Temp\… outside repo; 0 hash mismatches
  PASS F-K5 - re-read from destination: sha256 21056413e2bd00dc... matches=True,
              sidecar matches=True, CRC clean=True, 343 members
  PASS F-K6 - default refuses; --force-same-day yields naiad_workflow_2026-08-12-01-01.zip
              while naiad_workflow_2026-08-12-01.zip survives untouched
  PASS F-K6b - --force-same-day correctly does NOT apply to an older archive
  PASS F-K7 - 343/343 git-tracked source files still present on disk; 0 missing

archive   : D:\naiad-backups\naiad_workflow_2026-08-12-01.zip
size      : 3,579,058 B (3.4 MB, 25.0% of source)
sha256    : 21056413e2bd00dc09aa45c624f977b874e6a36923bfe9c18ea99cfb0d8afe59
members   : 343
source    : 14,330,757 B

8/8 fixtures pass

PUBLISH
  publish: routine last completed 2026-08-12 (4h ago)
  publish: committed 0b2a2b0 (1 path(s)) and pushed to origin/v12-v1-census
```

**F-K1's 0-mismatch line: `343/343 members verified both directions; 0 mismatches, 0 strays, 0
omissions`.**

### 5.1 The size delta, and what accounts for every file of it

| | members | size |
|---|---:|---:|
| before — `naiad_workflow_2026-08-12.zip` | 324 | 2,749,895 B (2.62 MB) |
| after — `naiad_workflow_2026-08-12-01.zip` | 343 | 3,579,058 B (3.41 MB) |
| **delta** | **+19** | **+829,163 B (+0.79 MB, +30.2%)** |

Net +19 is 22 added and 3 removed. Every one is accounted for:

| added, by root | n | why |
|---|---:|---|
| `briefs/panel` | 9 | **O-3** — newly covered |
| `briefs/` (brief JSONs, index) | 3 | **O-3** — newly covered |
| `docs/reports` | 2 | **O-3** — newly covered |
| `docs/handoffs` | 2 | **O-3** — newly covered |
| `docs/history` | 3 | the earlier filing session moved 3 files here |
| `docs/primers` | 1 | the earlier filing session moved 1 file here |
| `exchange/reports` | 2 | today's two build documents |

| removed | why |
|---|---|
| `HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md` | moved to `docs/history/` earlier today |
| `PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md` | moved to `docs/primers/` earlier today |
| `SS_Reassessment_Synthesis_2026-08-03.md` | **deleted by the TIDY** — its twin is in `exchange/reports/` and is in the archive |

**16 of the 22 additions are O-3 doing exactly what it was widened to do.**

### 5.2 The live retention report now finds the phase archives

```
  ## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE
  Location: `D:\Naiad\research_outputs\_archive`
  9 archive(s), 1,043,591,544 B (1,043.6 MB). **All permanent. None prunable.**
```

This is the same report that said **"none found"** this morning.

---

## 6 · File disposition

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/backup_estate.py` | yes | tracked | `91ce815` | yes, `origin/v12-v1-census` | GitHub + `--workflow` archive | 69,963 B · 1.04% *(code — outside the box)* |
| `research_outputs/wf1/WF1_discriminants.json` | yes | **tracked (O-1)** | `91ce815` | yes | GitHub only — `research_outputs/` is not a workflow source | `n/a` — lands in `research_outputs/`, outside the box *(would have been 1.69% in `exchange/`)* |
| `exchange/status/RETENTION.md` | yes | tracked | `0b2a2b0` | yes | GitHub + `--workflow` archive | 2,820 B · 0.04% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | pending publish | pending | GitHub + `--workflow` archive | 32,374 B · 0.48% *(+3,273 B for this session's STATUS entry)* |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md` | yes | tracked at publish | pending | pending | GitHub + `--workflow` archive | 23,133 B · 0.35% |
| `D:/naiad-backups/naiad_workflow_2026-08-12-01.zip` | yes | n/a — off-machine | n/a | n/a | the archive itself | `n/a` — `D:`, unsynced |
| `D:/naiad-backups/naiad_workflow_2026-08-12-01.zip.sha256` | yes | n/a | n/a | n/a | sidecar for the above | `n/a` — `D:` |
| ~~`Cascade Rewire.html`~~ *(repo root)* | **DELETED** | was untracked | n/a | n/a | its twin `docs/reports/Cascade Rewire.html`, tracked + pushed + archived | `n/a` |
| ~~`SS_Reassessment_Synthesis_2026-08-03.md`~~ *(repo root)* | **DELETED** | was untracked | n/a | n/a | its twin in `exchange/reports/`, tracked + pushed + archived | `n/a` |

`exchange/` total: **1,540,217 B ≈ 23.0%** of the 6.39 MB box.

---

## 7 · Open items

**O-5 (new) · The proof run pushed a workflow generation outside the keep-4 rule.** Writing
`naiad_workflow_2026-08-12-01.zip` as a same-day second copy means today occupies **two** of the
four kept generations, so `naiad_workflow_2026-08-04.zip` is now reported as outside the rule
alongside the two `2026-08-02` files. **Nothing was deleted — the retention report never deletes.**
But the keep-count treats a same-day `-NN` copy as a full generation, which is arguably wrong: it is
a re-run of today, not a distinct day's snapshot. Owner: **ATHENA** — either accept it, or teach
`_generations()` to group `-NN` siblings under their base date.

**O-6 (carried, unchanged) · The Sunday scheduled tasks still pass `--dest "G:\My Drive\naiad-backups"`.**
Next fire 2026-08-16 08:00 / 08:30. Untouched this session. Still awaiting the operator decision in
§8 of the backup-path-reroute report.

**O-7 (carried, unchanged) · The Google Drive mirror of `D:/naiad-backups` is registered but its
uploads are erroring** (`CreateHardLinkW failed`, exFAT has no hard links). Thirty seconds in the
Drive web UI under **Computers** settles it.

**O-8 (carried) · `research_outputs/` is still not in `WORKFLOW_SOURCES`**, so the newly tracked
`WF1_discriminants.json` has GitHub protection only. That is a real improvement on *nothing*, and
widening to `research_outputs/` was **not** in the O-3 ruling — it would pull in the multi-gigabyte
study estate and is a different decision entirely. Named here so it is not mistaken for an oversight.

---

## 8 · What I did not do

Nothing was deleted except the two files named in the deletion authority, each after four checks
passed in this run. `research_outputs/mc1/` was not added. `.gitignore` was not edited — it needed no
edit, and it remains modified from before this session and uncommitted, as it is not mine. No
scheduled task was touched. `G:/My Drive/naiad-backups` was not read or written this session.

**ROLLBACK:** `git revert 91ce815` restores the previous `WORKFLOW_SOURCES`, the previous
`retention_report()`, and un-tracks `WF1_discriminants.json` — note that un-tracking leaves the file
on disk, it does not delete it. The two deleted duplicates are recoverable from their twins at the
blobs recorded in §3. The new archive is additive; nothing was overwritten.

---

## 9 · STATUS

```
=== STATUS_ATHENA — 2026-08-12 ===
NOW: O-1, O-3 and O-4 are closed and the operator's tidy is done. WF1_discriminants.json is tracked
and pushed, so the repository has no unprotected file left. WORKFLOW_SOURCES covers briefs,
docs/reports and docs/handoffs — proved live at 343 members, 0 mismatches. The retention report now
finds the nine phase archives it had been reporting as absent, and can no longer confuse an
unmounted drive with an empty one.
LAST EVENT: 2026-08-12 — code commit 91ce815 pushed; proof run wrote naiad_workflow_2026-08-12-01.zip
(343 members, 8/8 fixtures); filed as
exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_O1-O3-O4-TIDY.md.
FACTS:
- O-1: research_outputs/wf1/WF1_discriminants.json verified NOT gitignored, tracked in 91ce815, confirmed present on origin/v12-v1-census. research_outputs/mc1/ deliberately not added [verified]
- O-3: WORKFLOW_SOURCES 11 -> 14 entries; old list asserted a strict subset of the new, no duplicates, no nested roots. Measured 4.21 MB against a 50 MB ceiling before widening [verified]
- O-3 proved live: 343 members vs 324, +829,163 B (+30.2%), 0 mismatches/strays/omissions; 16 of the 22 added members come from the three newly covered roots [verified]
- O-4: retention_report() now resolves the --phase root via a shared phase_archive_root_path() and prints 9 archives / 1,043.6 MB where it printed "none found" this morning [verified]
- O-4 third state: an unmounted drive prints "NOT ENUMERABLE" and falls back to the 9 tracked sidecars; fixture F-O4 asserts it never emits a "none found" verdict [verified]
- TIDY: both root duplicates removed only after four checks each passed IN THIS RUN (sha equal, twin tracked, blob on origin, worktree==blob). Both twins re-verified intact afterwards. Neither deletion was a git change [verified]
PENDING:
1. ATHENA: the keep-4 rule counts a same-day -NN archive as a full generation, so today occupies two slots and 2026-08-04 now reads as outside the rule. Report-only, nothing deleted — accept, or group -NN under the base date (O-5)
2. Operator: the two Sunday tasks still pass --dest "G:\My Drive\naiad-backups"; next fire 2026-08-16 (O-6, carried)
3. Operator: confirm or refute the Drive mirror of D:/naiad-backups — drive.google.com > Computers (O-7, carried)
4. ATHENA: research_outputs/ is still outside WORKFLOW_SOURCES, so WF1_discriminants.json is GitHub-only. Widening it pulls in the study estate and is a separate decision (O-8)
NEXT: Rule on O-5; it is the only item this session created. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===
```

**One action remaining: click Sync now.**
