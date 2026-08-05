# BUILDERS REPORT — HEPHAESTUS — 2026-08-04
## First full integrity check of every phase archive; SETUP marked historical; queue item 002 filed with a pre-execution finding

**Lane:** HEPHAESTUS (local Windows Claude Code)
**Repo:** naiad · **Branch:** `v12-v1-census` · **HEAD at start:** `81f847d`
**Python:** 3.12.10 (`C:/venvs/naiad/Scripts/python.exe`)
**Operator rulings carried:** G1-a, G2-a, G3-a, G4-a, G5-a, G6-a.
**Scope honoured:** `research_outputs/`, `G:` and `scripts/` were **read only**. No script was
edited — that is queue item 002.

---

## 0 · What this session was for, in plain language

Five jobs.

1. **Verify the archives by hash.** The operator has been copying phase archives to Google Drive.
   Until now nobody had checked whether the copies were *correct* — only that files of the right
   size existed. This is the first true integrity check: every archive, every destination, full
   sha256, no shortcuts.
2. **Mark the 2026-07-28 setup report historical.** Three of its findings are now false. It had
   been annotated twice already. A third annotation was worse than a banner.
3. **Read the daily-manifest retention code.** Queue item 002 proposes building it. This session
   read it first — as 002's own text instructs — to see what already exists.
4. **Write the ARGUS/APOLLO handoff memo** about nine data files in `exchange/reports/` that need a
   home ruling.
5. **File queue item 002** as a ratified contract for the next session.

**Jargon, defined once.** *Phase archive* = a `.zip` holding one research phase's evidence.
*Sidecar* = a `.sha256` file beside an archive holding its fingerprint. *sha256* = a 64-character
fingerprint; identical hashes mean byte-identical files, and one flipped bit changes the hash
entirely. *MATCH* below always means hash equality, never size equality. *Rolling window* = keeping
the newest N files and moving older ones elsewhere.

---

## 1 · Gates and probes, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=81f847d
  guards passed
```

---

## 2 · THE DELIVERABLE — full hash verification of every phase archive, verbatim

```
=== 2+3 - HASH-VERIFY EVERY PHASE ARCHIVE, BOTH DESTINATIONS (read-only) ===
  local archives: 9

--- phases (script-managed)
    G:/My Drive/naiad-backups/phases
    analytics_tests_v1.0.0_2026-07-29.zip    MATCH            sidecar OK                 6816 B
      0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
    analytics_v1.0.0_2026-07-29.zip          MATCH            sidecar OK                 19641 B
      d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
    s1_2026-07-27.zip                        MATCH            no sidecar                 106239157 B
      4d14ea48066dcf8b3548030551778323683ef76612702ea8205eb10bdd18f825
    s2_2026-07-27.zip                        MATCH            no sidecar                 246355294 B
      df5c1c196fef822537788e290e64f0c8dc9ef896694b73c91dab38fb0d5ce5ce
    s3_2026-07-27.zip                        MATCH            no sidecar                 269919602 B
      80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
    tc1_2026-07-27.zip                       MATCH            no sidecar                 242926299 B
      e673a158b5b1388d8e521769b460937153c691368766afda70af6d6d8f4caff8
    tc4_2026-07-27.zip                       MATCH            no sidecar                 68700167 B
      794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933
    tc5_2026-08-02.zip                       MATCH            sidecar OK                 18375498 B
      68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357
    v3_anchor_2026-07-27.zip                 MATCH            no sidecar                 91049070 B
      69d9cc989cb4054e7aa88cd5dfd7828863aad494f33423602010ced7f6cd757a

--- legacy one-off snapshot
    G:/My Drive/naiad (local folder) BACKUP/naiad/research_outputs/_archive
    NOT PRESENT

  MATCH = local and destination are byte-identical (hash, not size).
  Any MISMATCH or SIDECAR DISAGREES line is a real finding - report it, do not re-copy blindly.
```

### 2a · The headline

**All nine phase archives are on Drive, and all nine are byte-identical to their local originals.
Zero mismatches. Zero sidecar disagreements.** Total verified: **1,043,691,544 B ≈ 1,043 MB.**

This is the first time the full set has been checked by content rather than by presence. Previous
sessions verified `tc5` and the two `analytics` archives at copy time and spot-checked one legacy
archive (`tc4`); the other six had only ever been compared on **file size**, which catches truncation
but not corruption.

**What changed since this morning, and it is the operator's doing:** `phases/` held 3 archives at the
end of the previous session. It now holds **all 9**. The operator copied `s1`, `s2`, `s3`, `tc1`,
`tc4` and `v3_anchor` across. **Every one of those six copies verifies clean.**

| archive | bytes | sidecar | verdict |
|---|---|---|---|
| `s1_2026-07-27.zip` | 106,239,157 | — | **MATCH** |
| `s2_2026-07-27.zip` | 246,355,294 | — | **MATCH** |
| `s3_2026-07-27.zip` | 269,919,602 | — | **MATCH** |
| `tc1_2026-07-27.zip` | 242,926,299 | — | **MATCH** |
| `tc4_2026-07-27.zip` | 68,700,167 | — | **MATCH** |
| `v3_anchor_2026-07-27.zip` | 91,049,070 | — | **MATCH** |
| `tc5_2026-08-02.zip` | 18,375,498 | OK | **MATCH** |
| `analytics_v1.0.0_2026-07-29.zip` | 19,641 | OK | **MATCH** |
| `analytics_tests_v1.0.0_2026-07-29.zip` | 6,816 | OK | **MATCH** |

### 2b · The legacy snapshot is gone — investigated, and nothing was lost

The script reported `NOT PRESENT`. That is a change from this morning, when the same folder existed
and `tc4` was hashed from it. I investigated rather than reporting a bare absence:

```
--- G:/My Drive top level ---
  Analytics ZIPs
  desktop.ini
  naiad
  naiad-backups

--- does the legacy root still exist? ---
  ls: cannot access 'G:/My Drive/naiad (local folder) BACKUP': No such file or directory
```

`G:/My Drive/naiad (local folder) BACKUP` **has been deleted outright** — not moved, not renamed,
not merely unmaterialised by Drive streaming. Two nearby folders were checked and are unrelated:
`G:/My Drive/naiad` is a **documents** folder (markdown, contracts, HTML atlases), and
`G:/My Drive/Analytics ZIPs` is **empty**.

**No data was lost.** All six archives the legacy snapshot held are now in `phases/` and every one
verified MATCH above. This is a **net improvement**: the six moved from an unverified, explicitly
unmaintained one-off snapshot into the script-managed folder, and are now hash-proven. Consistent
with the standing ruling that the legacy snapshot was a one-off, not maintained.

**Reported, not fixed:** deleting it was outside this contract, and `G:` was read-only this session.
Recording it because a prior report cited that snapshot as protection for the 2026-07-27 set. **That
citation is now stale — `phases/` is the protection.**

### 2c · Findings on Drive hygiene — reported, not fixed (`G:` was read-only)

**Six of nine archives in `phases/` have no sidecar.** `s1`, `s2`, `s3`, `tc1`, `tc4` and
`v3_anchor` were copied without one. They verify today only because the local originals still exist
to compare against. **If this laptop were lost, those six could not be verified at all** — the exact
gap closed for the `analytics` pair in the previous session by writing sidecars at the destination.
Generating six sidecars is a minute's work but requires a write to `G:`, which this contract forbids.
**Recommend folding into queue 002 as part of D1's mirror behaviour, or a one-line paste.**

**`naiad-backups/` has accumulated redundant copies.** Three `(1)`-suffixed files — Drive's
re-upload artifact — were hashed and are **byte-identical** to their originals:

```
  analytics_tests_v1.0.0_2026-07-29 (1).zip  vs analytics_tests_v1.0.0_2026-07-29.zip  IDENTICAL - redundant
      0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
  analytics_v1.0.0_2026-07-29 (1).zip        vs analytics_v1.0.0_2026-07-29.zip        IDENTICAL - redundant
      d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
  naiad_workflow_2026-08-02 (1).zip          vs naiad_workflow_2026-08-02.zip          IDENTICAL - redundant
      fcc260f8c50daeb94bf2470614634feb1b714d78a53671925f25df5a72adf4f8
```

Additionally, `analytics_v1.0.0`, `analytics_tests_v1.0.0` and `tc5` exist **both** at the
`naiad-backups/` top level **and** inside `phases/`.

| redundancy | bytes |
|---|---|
| three `(1)`-suffixed duplicates | 1,158,693 |
| top-level copies of files already in `phases/` | 18,401,955 |
| **total redundant** | **19,560,648 B ≈ 18.7 MB** |

Harmless for now — Drive is not capacity-constrained the way the project box is — but it makes the
folder harder to read, and a future de-duplication pass must apply **§3.2's "existence is not
protection"** rule before removing any of it.

---

## 3 · SETUP_2026-07-28.md marked historical — with CR-pair proof

```
  OK  banner prepended to exchange\reports\SETUP_2026-07-28.md
  CR pairs before=0 after=0 (must be equal)
```

| measurement | value |
|---|---|
| CR pairs **before** | **0** |
| CR pairs **after** | **0** |
| verdict | **equal — no line-ending reflow** |

The banner as stored (first 15 lines, verified UTF-8 with the typographic apostrophe intact):

```
> # DOCUMENT STATUS: HISTORICAL — do not act on this document
>
> Marked 2026-08-04. Written 2026-07-28; three of its findings are now false and it has been
> annotated twice. Rather than a third annotation, the whole document is marked historical.
>
> **Superseded by measurement:** `G:` **is** mounted and holds ~988 MB across `naiad-backups/`
> (estate, workflow, and a script-managed `phases/` folder). This document states there is no
> Google Drive on this machine, its evidence table reads "Google Drive path: none found", and
> its conclusion declares `backup_estate.py`’s offsite target blocked. **All three are false.**
>
> **What is still true and worth reading:** the reasoning about why sync is not backup, and the
> setup narrative as a record of what was believed on 2026-07-28.
>
> **Current state of record:** `exchange/status/RETENTION.md` (archive inventory),
> `exchange/status/CADENCE.md` (triggers), `exchange/status/CONVENTIONS.md` §8 (infrastructure).
```

**Cross-reference verified before publishing:** the banner cites `CONVENTIONS.md §8`. That section
exists — `## §8 · Infrastructure inventory — MOVED FROM MEMORY #25` at line 598. A banner pointing
at a non-existent section would be its own defect, so it was checked rather than assumed.

This closes the open item carried since the morning session, which flagged that the document's
evidence table at lines 133–137 still read "Google Drive path: none found". Rather than annotate a
third line, the whole document now declares itself historical at the top.

---

## 4 · The daily-manifest retention code, as read

```
--- who writes daily/MANIFEST_<date>.json and DAILY_<date>.md ---
  2:"""daily_routine.py -- run the day's jobs, stage their outputs, write one report.
  17:  * a ROLLING WINDOW keeps the newest `keep_daily` DAILY_*.md and
  18:    MANIFEST_*.json in output_dir and MOVES older ones to daily_archive_dir --
  20:  * the report is written to <output_dir>/DAILY_<yyyy-mm-dd>.md
  61:    ("_reviewer_box/daily", "exchange/status/daily"),
  409:    is no keep-count for them here and no `keep_phase_sets` key is read.
  412:    for pattern, keep, label in (
  413:        ("naiad_estate_*.zip", cfg.get("keep_estate", 4), "estate"),
  414:        ("naiad_workflow_*.zip", cfg.get("keep_workflow", 4), "workflow"),
  417:            gens = sorted((p for p in dest.glob(pattern) if p.is_file()),
  421:        for p in gens[keep:]:
  532:            alerts.append("**retention — generations outside the rule** (listed, never pruned): "
  564:    # files of exchange/status/ only: daily/ is an append-only archive whose
  620:    `daily_archive_dir` is operator-configurable, so it can legitimately point
  632:def apply_rolling_window(out_dir, archive_dir, keep):
  633:    """Keep the newest `keep` DAILY_*.md and MANIFEST_*.json; MOVE the rest out.
  647:    if keep is None or keep < 0:
  654:    for pattern in ("DAILY_*.md", "MANIFEST_*.json"):
  656:            files = sorted(out_dir.glob(pattern), key=lambda p: p.name, reverse=True)
  660:        for old in files[keep:]:
  681:def window_lines(moved, out_dir, keep, archive_dir):
  684:    lines = [f"- window: newest **{keep}** of each of `DAILY_*.md` and `MANIFEST_*.json` stay in "
  779:        p for p in out_dir.glob("MANIFEST_*.json")
  926:    staged_manifest = out_dir / f"MANIFEST_{today}.json"

--- how many daily artifacts exist today ---
  DAILY_2026-07-28.md
  DAILY_2026-08-02.md
  DAILY_2026-08-03.md
  MANIFEST_2026-07-28.json
  MANIFEST_2026-08-02.json
  MANIFEST_2026-08-03.json
  count: 6
```

Configuration, as read:

```
  scripts/routine_jobs.json:7:  "daily_archive_dir": "research_outputs/_daily_archive",
  scripts/routine_jobs.json:8:  "keep_daily": 7,
  scripts/daily_routine.py:1025: archive_dir = ROOT / reg.get("daily_archive_dir", "research_outputs/_daily_archive")
  scripts/daily_routine.py:1026: keep = reg.get("keep_daily", 7)
```

The function itself, `daily_routine.py:632–678`:

```python
def apply_rolling_window(out_dir, archive_dir, keep):
    """Keep the newest `keep` DAILY_*.md and MANIFEST_*.json; MOVE the rest out.

    MOVED, never deleted.  The point is to stop exchange/ growing without bound
    -- it is tracked, auto-pushed and synced into a capacity-constrained project
    box -- not to lose the history.  Older reports land in archive_dir, still on
    disk, still readable.

    Names carry an ISO date (DAILY_2026-08-02.md), so a lexical sort is a
    chronological sort; no filesystem timestamps are trusted.

    Every move is guarded: a failure is recorded and the run continues, because
    this happens after the day's real work and must never cost it.
    """
```

### 4a · Finding: queue 002's D4 is already built

**D4 asks for exactly what already exists, at exactly the number it specifies.** The reading was
performed because D4 itself says *"read it first, do not assume"*; this is that reading's result.

| D4 asks for | what exists today |
|---|---|
| keep the newest **7** daily artifacts | `routine_jobs.json:8` → `"keep_daily": 7`, and 7 is also the code default at line 1026 |
| applies to `exchange/status/daily/` | yes — `("_reviewer_box/daily", "exchange/status/daily")` at line 61 |
| covers both artifact kinds | yes — `("DAILY_*.md", "MANIFEST_*.json")` at line 654 |
| older ones not auto-deleted | **stronger** — they are **moved** to `research_outputs/_daily_archive`, off the sync bus, still on disk |

Three details that make the existing implementation better than a naive one, and worth preserving:
it sorts **lexically on the ISO date in the filename** rather than trusting filesystem timestamps;
it **dedups by sha256** when an identical copy is already archived; and it **renames on collision**
(`__1`, `__2`) rather than overwriting. Every move is individually guarded so a failure records an
error and the run continues.

**The one `unlink()` is safe.** Line 665 deletes only when `_sha256(old) == _sha256(target)` — an
identical copy is already in the archive. That is deduplication, not loss.

**The window has never fired.** `exchange/status/daily/` holds 3 `DAILY_*.md` and 3
`MANIFEST_*.json` — 6 files against a window of 7 *each*. Nothing has aged out yet, which is why the
duplication noted yesterday (`MANIFEST.json` and `MANIFEST_2026-08-03.json` both 21,115 B) is not a
retention failure: retention has not yet had anything to do.

**Disposition:** recorded as a `PRE-EXECUTION FINDING` block inside queue item 002 under D4, so the
002 executor reads it before writing code. **I did not alter D4's ratified text.** Recommend the
operator close D4 as ALREADY SATISFIED or reduce it to fixture F-R1 as a confirmation. **D1, D2 and
D3 are unaffected and stand as written.**

---

## 5 · Artifacts written this session

| artifact | purpose |
|---|---|
| `exchange/reports/2026-08-04_ATHENA_handoff_orphan-data-files.md` | ARGUS/APOLLO ruling request on nine data files — six ARGUS orphans, two ARGUS files with git-ignored twins, one APOLLO orphan |
| `exchange/queue/002_backup-and-publish-guards.md` | ratified contract: `--mirror` for `--phase`, `--phase --dest` becomes an error, publish size budget, manifest retention — plus the D4 pre-execution finding |
| `exchange/reports/SETUP_2026-07-28.md` | historical banner prepended |
| this document | the build record |

---

## 6 · Fixture-equivalent transcript

| # | assertion | result |
|---|---|---|
| G1 | working directory is the local clone | **PASS** |
| G2 | branch is `v12-v1-census` | **PASS** |
| G3 | all 9 local archives hash-verified against `phases/` | **PASS — 9/9 MATCH, 0 mismatches** |
| G4 | sidecars, where present, agree with content | **PASS — 3/3 OK; 6 archives have none** |
| G5 | legacy snapshot absence investigated, not assumed | **PASS — confirmed deleted; contents preserved and verified in `phases/`** |
| G6 | `(1)`-suffixed Drive files checked for content difference | **PASS — all 3 byte-identical, redundant** |
| G7 | banner CR pairs preserved | **PASS — 0 before, 0 after** |
| G8 | banner's `§8` cross-reference exists | **PASS — line 598** |
| G9 | retention code read before 002 filed | **PASS — D4 found already implemented** |
| G10 | no script edited | **PASS** — `scripts/` porcelain shows only pre-existing untracked `seq8_*.py` |
| G11 | `research_outputs/` unmodified | **PASS** — only pre-existing untracked `seq8/` entries |
| G12 | `G:` not written | **PASS** — read-only; six missing sidecars reported, not created |
| G13 | no literal backslash in any path used | **PASS** |

---

## 7 · Rollback

- **Pre-publish:** `git checkout -- exchange/` reverts the banner; delete the two new files
  (`exchange/queue/002_backup-and-publish-guards.md`,
  `exchange/reports/2026-08-04_ATHENA_handoff_orphan-data-files.md`).
- **Post-publish:** `git revert <publish sha>`.
- **Nothing on `G:`, in `research_outputs/` or in `scripts/` needs rolling back** — all read-only.

---

## 8 · FILE DISPOSITION TABLE

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY |
|---|---|---|---|---|---|
| `exchange/reports/SETUP_2026-07-28.md` | yes | tracked | see publish sha in on-screen close | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/queue/002_backup-and-publish-guards.md` | yes | tracked on publish | see publish sha | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/2026-08-04_ATHENA_handoff_orphan-data-files.md` | yes | tracked on publish | see publish sha | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_ARCHIVE-VERIFY-AND-QUEUE-002.md` | yes | tracked on publish | see publish sha | yes (`origin/v12-v1-census`) | GitHub + `--workflow` archive |
| `research_outputs/_archive/*.zip` (9 archives) | yes | **ignored** — `.gitignore:38:*.zip` | never | no | **`G:/My Drive/naiad-backups/phases/` — all 9 hash-verified this session** |
| `research_outputs/_archive/tc5_2026-08-02.zip.sha256` | yes | tracked | unchanged | yes | GitHub |
| `G:/My Drive/naiad-backups/phases/*` (9 zips + 3 sidecars) | yes | n/a — **outside the repo** | n/a | n/a | **Google Drive — the off-machine copy** |
| `G:/My Drive/naiad (local folder) BACKUP/` | **no — deleted** | n/a | n/a | n/a | **gone; contents preserved and verified in `phases/`** |
| `scripts/daily_routine.py` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |
| `scripts/routine_jobs.json` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |
| `scripts/backup_estate.py` | yes | tracked | unchanged this run | unchanged | GitHub + `--workflow` archive |

**Read this table as:** *committed is not pushed, pushed is not backed up.* The nine local archives
are git-ignored by design; their protection is entirely the Drive `phases/` folder, which is why
this session's hash verification is the first evidence that protection is real.

**Per §3.1, this document does not state its own sha256** — that value is stale the moment it is
written.

---

## 9 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | **Rule on D4**: close as ALREADY SATISFIED or reduce to fixture F-R1 (§4a) | operator — **blocks the 002 session from wasting effort** |
| 2 | Six archives in `phases/` have no sidecar; unverifiable if the laptop is lost (§2c) | operator — fold into 002 D1, or a one-line paste |
| 3 | 18.7 MB of redundant copies in `naiad-backups/` — three `(1)` files plus top-level duplicates of `phases/` content (§2c) | operator |
| 4 | Nine data files in `exchange/reports/` need a home ruling | ARGUS (8), APOLLO (1) — memo filed |
| 5 | Execute queue item 002 — **its own session, its own build document** | HEPHAESTUS |
| 6 | Prior reports citing the legacy snapshot as protection are now stale; `phases/` is the protection (§2b) | operator |
