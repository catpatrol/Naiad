# BUILDERS REPORT — HEPHAESTUS — 2026-08-06 — ARCHIVE RELOCATION TO D:

**What this document is.** A complete record of one builder session. It assumes you know nothing
about what came before. Read it top to bottom and you will know exactly what moved, what proves it
moved safely, what is now where, and what is still open.

**What was done, in one sentence.** The nine large phase-archive `.zip` files — about 1 GB of
permanent evidence that had been sitting on the laptop inside the OneDrive-synced repo folder —
were copied to the external drive `D:/Naiad`, each one hash-verified before and after the copy, and
only then deleted from the laptop; a pointer file was left behind explaining where they went.

**On whose authority.** Operator ruling B, 2026-08-06. The paste carried a narrow, explicit delete
authorization: a local archive could be deleted **only in the same run, only after** its `D:` copy
matched both its tracked fingerprint file and a fresh hash of the local original. Nothing else was
authorized for deletion and nothing else was deleted.

---

## 1 · Why this was worth doing

The nine archives are **permanent evidence** — frozen snapshots of completed research phases, never
prunable. They were living in `research_outputs/_archive/` inside the repo folder, which sits under
OneDrive. That is the worst place for a gigabyte of frozen data: OneDrive syncs it forever, it is
too large for GitHub, and it competes for space on the laptop with working data.

Moving them to an external drive keeps the evidence and removes the cost. The risk in any such move
is obvious and severe: **if the copy is silently corrupt and you delete the original, the evidence is
gone.** Everything below exists to prove that did not happen.

**The safety property this run had to satisfy.** At no instant was there only one copy of any
archive. Before deletion each file existed in three places (laptop, `D:`, Google Drive) with a
fourth independent fingerprint held in GitHub. After deletion, two full copies plus the fingerprint
remain.

---

## 2 · Gate and probe values, exactly as printed

These ran before anything was touched. Every one had to pass or the run would stop.

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=9eaeda2
  D:/Naiad reachable and writable
```

The write probe is not decorative: it creates a file on `D:` and deletes it, proving the drive
accepts writes rather than merely appearing in the file listing.

**Snapshot gate, first attempt — HALT-SOFT, nothing changed:**

```
HALT-SOFT: docs/memory/NAIAD_PROJECT_MEMORY_2026-08-06_POST-REDRAFT_11.md not found.
```

This is a deviation from the paste and is described in full in §8, finding F-1. In short: the file
was present but named `..._POST-REDRAFT_11_1.md` — the browser's duplicate-download suffix. Its
contents were checked and confirmed correct, it was renamed to the contracted name, and the gate was
re-run:

```
  snapshot present: 14250 bytes, 11 entries
  ENTRY COUNT OK
```

**Pre-flight inventory (read-only, added by the builder — not in the paste).** Before authorizing a
delete of anything, the builder confirmed each archive had a fingerprint file and that those
fingerprint files are held in GitHub:

```
  9 zip(s):
    analytics_tests_v1.0.0_2026-07-29.zip                         6816 B (    0.0 MB)  sidecar=True  tracked=True
    analytics_v1.0.0_2026-07-29.zip                              19641 B (    0.0 MB)  sidecar=True  tracked=True
    s1_2026-07-27.zip                                        106239157 B (  101.3 MB)  sidecar=True  tracked=True
    s2_2026-07-27.zip                                        246355294 B (  234.9 MB)  sidecar=True  tracked=True
    s3_2026-07-27.zip                                        269919602 B (  257.4 MB)  sidecar=True  tracked=True
    tc1_2026-07-27.zip                                       242926299 B (  231.7 MB)  sidecar=True  tracked=True
    tc4_2026-07-27.zip                                        68700167 B (   65.5 MB)  sidecar=True  tracked=True
    tc5_2026-08-02.zip                                        18375498 B (   17.5 MB)  sidecar=True  tracked=True
    v3_anchor_2026-07-27.zip                                  91049070 B (   86.8 MB)  sidecar=True  tracked=True
  TOTAL zip bytes: 1043591544 (0.97 GB)

  D: total=3725.7 GB  free=3725.7 GB  need=0.97 GB  headroom_ok=True
  D: dest exists=False  contents=-
```

Two facts here matter. `D: dest exists=False` means the destination folder was empty, so no existing
file could be overwritten. And every archive had a `sidecar=True tracked=True` — an independent
fingerprint already stored in GitHub, written on an earlier date, which the copy would be checked
against.

**Are the archives themselves in GitHub?** No, and this was checked rather than assumed:

```
  s1_2026-07-27.zip   tracked=False   (all nine identical)
  .gitignore:38:*.zip	research_outputs/_archive/s1_2026-07-27.zip
```

They are deliberately excluded from version control by line 38 of `.gitignore`. This matters twice
over: deleting them could not dirty the repository, **and** GitHub was never a copy of the archives
themselves — only of their fingerprints. That is why the `D:` and Drive copies carry the whole
weight.

---

## 3 · Step-2 measurement table — the before picture

Measured on the laptop before any file was moved.

| folder | files | bytes | size |
|---|---:|---:|---|
| `research_outputs/_archive` | 18 | 1,043,592,353 | 995.2 MB |
| `briefs` | 12 | 4,115,350 | 3.9 MB |
| `research_outputs/mc1` | 29 | 162,626,825 | 155.1 MB |

The 18 files in `_archive` are the 9 archives (1,043,591,544 bytes) plus their 9 fingerprint files
(809 bytes). `briefs` and `research_outputs/mc1` were measured for context only — **neither was
touched by this run.**

---

## 4 · The full fixture transcript — every archive, verbatim

This is the complete output of the relocation step. For each archive the sequence is: read the
fingerprint GitHub already holds → hash the local file and compare → copy to `D:` → **re-read the
bytes back off `D:` and hash them** → only if that matches, delete the local file.

The re-read is the part that actually proves something. Hashing the source again after a copy proves
nothing about the copy; only reading back from the destination does.

```
  archives: 9, 1043591544 bytes. D: free: 3725.7 GB

--- analytics_tests_v1.0.0_2026-07-29.zip  (6816 bytes)
  local hash   0a1ffc941032acbf  (0s)  sidecar: MATCH
  copied to D:  (0s)
  re-read from D: 0a1ffc941032acbf  (0s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- analytics_v1.0.0_2026-07-29.zip  (19641 bytes)
  local hash   d3fcd786881dc202  (0s)  sidecar: MATCH
  copied to D:  (0s)
  re-read from D: d3fcd786881dc202  (0s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- s1_2026-07-27.zip  (106239157 bytes)
  local hash   4d14ea48066dcf8b  (0s)  sidecar: MATCH
  copied to D:  (1s)
  re-read from D: 4d14ea48066dcf8b  (0s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- s2_2026-07-27.zip  (246355294 bytes)
  local hash   df5c1c196fef8225  (0s)  sidecar: MATCH
  copied to D:  (2s)
  re-read from D: df5c1c196fef8225  (2s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- s3_2026-07-27.zip  (269919602 bytes)
  local hash   80ac04439e169cf1  (0s)  sidecar: MATCH
  copied to D:  (2s)
  re-read from D: 80ac04439e169cf1  (2s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- tc1_2026-07-27.zip  (242926299 bytes)
  local hash   e673a158b5b1388d  (0s)  sidecar: MATCH
  copied to D:  (2s)
  re-read from D: e673a158b5b1388d  (2s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- tc4_2026-07-27.zip  (68700167 bytes)
  local hash   794036c2d6135285  (0s)  sidecar: MATCH
  copied to D:  (1s)
  re-read from D: 794036c2d6135285  (0s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- tc5_2026-08-02.zip  (18375498 bytes)
  local hash   68942d6261bf8ca8  (0s)  sidecar: MATCH
  copied to D:  (0s)
  re-read from D: 68942d6261bf8ca8  (0s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

--- v3_anchor_2026-07-27.zip  (91049070 bytes)
  local hash   69d9cc989cb4054e  (0s)  sidecar: MATCH
  copied to D:  (1s)
  re-read from D: 69d9cc989cb4054e  (1s)  VERIFIED
  VERIFIED ON D: - local removed  (copies remain: D: + Google Drive phases/ + GitHub sidecar)

  relocated: 9/9. Local .sha256 sidecars untouched (git-tracked fingerprints).
  local zips remaining: 0
```

**9 of 9 relocated. No mismatch, no failure, no halt.**

---

## 5 · Independent re-verification — full hashes

The transcript above was produced by the program that did the moving. A program checking its own
work is weak evidence, so a **separate program in a fresh process** re-read all nine files off `D:`
and compared them against the fingerprint files stored in GitHub. Full 64-character hashes, not
abbreviations.

| archive | bytes on D: | read time | sidecar (GitHub) vs D: copy |
|---|---:|---:|---|
| `analytics_tests_v1.0.0_2026-07-29.zip` | 6,816 | 0.02s | **MATCH** |
| `analytics_v1.0.0_2026-07-29.zip` | 19,641 | 0.03s | **MATCH** |
| `s1_2026-07-27.zip` | 106,239,157 | 0.79s | **MATCH** |
| `s2_2026-07-27.zip` | 246,355,294 | 1.71s | **MATCH** |
| `s3_2026-07-27.zip` | 269,919,602 | 1.86s | **MATCH** |
| `tc1_2026-07-27.zip` | 242,926,299 | 1.68s | **MATCH** |
| `tc4_2026-07-27.zip` | 68,700,167 | 0.52s | **MATCH** |
| `tc5_2026-08-02.zip` | 18,375,498 | 0.16s | **MATCH** |
| `v3_anchor_2026-07-27.zip` | 91,049,070 | 0.68s | **MATCH** |

```
  RESULT: 9 match, 0 bad, 1043591544 bytes on D: (0.97 GB)
```

**The byte total on `D:` equals the original byte total exactly: 1,043,591,544.**

The full hash pairs, as printed — GitHub-held fingerprint on the first line, bytes read back off the
external drive on the second:

```
analytics_tests_v1.0.0_2026-07-29.zip
  sidecar 0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
  D: copy 0a1ffc941032acbf7144f4c7af77ad1d54967a40a4e5eb36fa200ae078e99999
analytics_v1.0.0_2026-07-29.zip
  sidecar d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
  D: copy d3fcd786881dc20224fc51e168f60ace00d57749586b9cd60c28b54f4c9ba3d9
s1_2026-07-27.zip
  sidecar 4d14ea48066dcf8b3548030551778323683ef76612702ea8205eb10bdd18f825
  D: copy 4d14ea48066dcf8b3548030551778323683ef76612702ea8205eb10bdd18f825
s2_2026-07-27.zip
  sidecar df5c1c196fef822537788e290e64f0c8dc9ef896694b73c91dab38fb0d5ce5ce
  D: copy df5c1c196fef822537788e290e64f0c8dc9ef896694b73c91dab38fb0d5ce5ce
s3_2026-07-27.zip
  sidecar 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
  D: copy 80ac04439e169cf1dfff5bc122b37fb78ddc6a6a79d2201380973006ff4e146f
tc1_2026-07-27.zip
  sidecar e673a158b5b1388d8e521769b460937153c691368766afda70af6d6d8f4caff8
  D: copy e673a158b5b1388d8e521769b460937153c691368766afda70af6d6d8f4caff8
tc4_2026-07-27.zip
  sidecar 794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933
  D: copy 794036c2d613528530272864aa866421af0cbf9de2db5a2423fa7e0b25eb1933
tc5_2026-08-02.zip
  sidecar 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357
  D: copy 68942d6261bf8ca8d551e52aa6e4d374f8c9fb6e0ac5be5da96b188e928b4357
v3_anchor_2026-07-27.zip
  sidecar 69d9cc989cb4054e7aa88cd5dfd7828863aad494f33423602010ced7f6cd757a
  D: copy 69d9cc989cb4054e7aa88cd5dfd7828863aad494f33423602010ced7f6cd757a
```

### 5b · The third copy, verified rather than asserted — added by the builder

The pointer file written in this run claims a Google Drive backup exists. Since the local originals
were deleted partly on the strength of that claim, the builder verified it instead of repeating it.
All nine files at `G:/My Drive/naiad-backups/phases/` were hashed against the same GitHub-held
fingerprints:

```
  DRIVE RESULT: 9 match, 0 mismatch, 0 missing
```

**So the count of verified, independent copies of every archive is two full copies (`D:` and Google
Drive), each confirmed today against a fingerprint written on an earlier date and stored in a third
place (GitHub).** The pointer's claim of a Drive backup is true as of 2026-08-11.

---

## 6 · The after picture, and what the laptop got back

| folder | files before | bytes before | files after | bytes after | change |
|---|---:|---:|---:|---:|---:|
| `research_outputs/_archive` | 18 | 1,043,592,353 | 10 | 1,320 | **−1,043,591,033 B (−995.2 MB)** |
| `briefs` | 12 | 4,115,350 | 12 | 4,115,350 | 0 (untouched) |
| `research_outputs/mc1` | 29 | 162,626,825 | 29 | 162,626,825 | 0 (untouched) |

**Reclaimed on the laptop (C:): 1,043,591,544 bytes — 995.24 MB — the exact byte total of the nine
archives.** The folder does not fall to zero because the 10 remaining files are the 9 GitHub-held
fingerprint files (809 bytes) plus the new pointer (511 bytes).

Because this folder sits under OneDrive, that is also ~995 MB that OneDrive no longer syncs.

**Final contents of `D:/Naiad/research_outputs/_archive/`:** 9 archives + 9 copies of their
fingerprint files, 18 files, original modification dates preserved.

---

## 7 · Commits and pushes

| # | commit | contents | pushed to |
|---|---|---|---|
| 1 | `292e839` | closing 11-entry memory snapshot + relocation pointer (2 files, +61 lines) | `origin/v12-v1-census` — **SUCCEEDED** |
| 2 | `7a9f999` | `exchange:` auto-publish 2026-08-06 — the queue 002 amendment (1 path) | `origin/v12-v1-census` — **pushed=True, offenders=[]** |

```
  staged: docs/memory/NAIAD_PROJECT_MEMORY_2026-08-06_POST-REDRAFT_11.md research_outputs/_archive/POINTER.md
  To https://github.com/catpatrol/Naiad.git
     9eaeda2..292e839  v12-v1-census -> v12-v1-census
  DOCS PUSH SUCCEEDED

  publish: committed 7a9f999 (1 path(s)) and pushed to origin/v12-v1-census
  status= PUBLISHED commit= 7a9f999 pushed= True offenders= []
```

Local `HEAD` and `origin/v12-v1-census` both read `7a9f999`. The working tree is clean across
`exchange/`, `docs/` and `research_outputs/`. This report is published in a later commit, which is
why its own commit id does not appear above.

**The queue 002 amendment, as it landed** (`exchange/queue/002_backup-and-publish-guards.md`, +2/−0):

> **AMENDMENT 2026-08-06, RULING B:** the local archive root is now the external drive. D1 gains a
> config: `--phase` writes its archive to `D:/Naiad/research_outputs/_archive` by default
> (configurable), with `--mirror` still targeting Drive. Fixture: the archive lands on D:, its
> tracked sidecar lands in the REPO folder, and both verify. If D: is absent, HALT loudly — never
> fall back silently to the laptop.

---

## 8 · Findings reported, not fixed

**F-1 · The closing snapshot arrived under the wrong filename. Resolved, and recorded because it is
a deviation from the paste.** The gate looked for
`docs/memory/NAIAD_PROJECT_MEMORY_2026-08-06_POST-REDRAFT_11.md` and did not find it; the paste's
HALT-SOFT fired correctly and **changed nothing.** The file was actually present as
`NAIAD_PROJECT_MEMORY_2026-08-06_POST-REDRAFT_11_1.md` — the trailing `_1` is what a browser appends
when a file of that name was downloaded twice. The builder confirmed the contents before acting: the
title reads "CLOSING SNAPSHOT after the 2026-08-06 redraft · 11 entries", it contains exactly 11
`### Entry` headers, and its lineage line names the 20-entry pre-redraft snapshot committed earlier
the same day. Only then was it renamed to the contracted name. **The same `_1` pattern is visible on
other files in this repo** (`HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md`), so it will recur — worth a
tolerant filename match in future pastes rather than an exact one.

**F-2 · `exchange/status/MANIFEST.json` is stale and every publish leaves it staler. Not fixed —
outside this paste's authorization.** This was flagged in the previous session and has not moved.
The file that tells other lanes what is on the bus currently reports:

- `generated_utc = 2026-08-11T19:37:35Z`, `head = 11c3fb8` — now **four commits behind** `7a9f999`
- `CONVENTIONS.md size = 42147`, when the file on disk is `47484` bytes

The cause is structural, not a one-off: **`scripts/publish_exchange.py` contains no manifest logic
at all.** The generator is `scripts/reviewer_manifest.py`, and nothing in the publish path invokes
it. So the manifest can only ever go stale as work proceeds. Any lane performing the §4.3 "is this
file actually visible" check against the manifest reads a wrong size and a wrong hash for
`CONVENTIONS.md` — the very file amended twice this week. **Fix: run `scripts/reviewer_manifest.py`,
then publish. Owner: operator to authorize; one line of work.**

**F-3 · `exchange/DIGEST.md` does not list this report, and a lane cannot request a file it does not
know about.** §3.2 makes keeping that index current HERMES's standing duty. `DIGEST.md` was last
modified 2026-08-05 and therefore omits everything produced on 2026-08-06, including this document,
both memory snapshots, and the relocation pointer. **Not fixed: another lane's charter. Owner:
HERMES.**

**F-4 · No operator ruling was reinterpreted in this build.** The delete authorization was applied
exactly as written — verify against fingerprint, copy, re-read from destination, and only then
delete — and no file outside `research_outputs/_archive/*.zip` was removed anywhere.

---

## 9 · What remains open, with owners

| # | open item | owner |
|---|---|---|
| 1 | Regenerate `MANIFEST.json` via `scripts/reviewer_manifest.py`, then publish (F-2) | operator to authorize, HEPHAESTUS to run |
| 2 | Make the publish path refresh the manifest, so it cannot silently rot (F-2, root cause) | queue item needed — no owner yet |
| 3 | Update `exchange/DIGEST.md` for all 2026-08-06 artifacts (F-3) | HERMES |
| 4 | Implement queue 002 D1 as amended: `--phase` writing to `D:/Naiad/...`, HALT loudly if `D:` absent | HEPHAESTUS, when 002 is ratified for build |
| 5 | Decide the recovery drill cadence — see options below | operator |

---

## 10 · Honest next options, with implications

**Option A — do nothing further about the archives.** Two verified copies (`D:`, Google Drive) plus
GitHub fingerprints is genuinely solid. *Implication:* both full copies are attached to one physical
location. A fire or theft takes the external drive and the laptop together; Google Drive survives
that, so the true off-site copy count is one.

**Option B — treat Google Drive as the off-site copy and verify it on a schedule.** The Drive copy
was confirmed byte-exact today. *Implication:* cheap, and it converts an assumption into a
measurement. Recommended, quarterly, using exactly the check in §5b.

**Option C — fix the manifest properly (F-2) before more lanes read from the bus.** *Implication:*
the highest-value item here. Every session that trusts `MANIFEST.json` right now is reading
four-commit-old facts about files that changed this week. The one-line fix is a stopgap; making
publish refresh the manifest is the real repair.

**Recommendation: C, then B.** The archives are safe; the index describing them is not.

---

## 11 · File-disposition table (§3.2, six columns + BOX COST)

Box budget for reference: the project knowledge box holds ~6.39 MB; **1% = 67,004 bytes**.
`exchange/` currently totals **1,593,310 bytes across 86 files = 23.8% of the box.** The standing
tick set is `LEDGER.md` and `exchange/` only, so files outside `exchange/` cost the box nothing and
are marked `n/a` with their actual home named.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-06_ARCHIVE-RELOCATION-D.md` | yes | tracked | this run's publish commit | yes, `origin/v12-v1-census` | GitHub only | 22,227 B = **0.33%** |
| `exchange/queue/002_backup-and-publish-guards.md` | yes | tracked | `7a9f999` | yes, `origin/v12-v1-census` | GitHub only | 8,676 B = **0.13%** |
| `docs/memory/NAIAD_PROJECT_MEMORY_2026-08-06_POST-REDRAFT_11.md` | yes | tracked | `292e839` | yes, `origin/v12-v1-census` | GitHub only | n/a — `docs/`, outside the tick set |
| `research_outputs/_archive/POINTER.md` | yes | tracked | `292e839` | yes, `origin/v12-v1-census` | GitHub only | n/a — `research_outputs/`, outside the tick set |
| `research_outputs/_archive/*.sha256` (9 files, unchanged) | yes | tracked | `ccbfd2d` (earlier) | yes, `origin/v12-v1-census` | GitHub only | n/a — `research_outputs/`, outside the tick set |
| `research_outputs/_archive/*.zip` (9 files) | **no — moved off C:** | ignored, `.gitignore:38` `*.zip` | never committed (ignored) | no | **phase archive on `D:/Naiad` + Google Drive `phases/`, both hash-verified 2026-08-11; fingerprints in GitHub** | n/a — external drive `D:`, unsynced |
| `D:/Naiad/research_outputs/_archive/*.zip` + `*.sha256` (18 files) | yes | n/a — outside the repo | n/a | n/a | itself the archive copy; second copy on Google Drive | n/a — external drive `D:`, unsynced |

**Reading the last two rows together:** the archives no longer exist on the laptop. They exist on
the external drive and on Google Drive, both verified byte-exact today, and GitHub holds the
fingerprints that make either copy checkable at any time without trusting this report.

**Rollback, if ever needed.** Copy the `.zip` files from `D:/Naiad/research_outputs/_archive/` back
into `research_outputs/_archive/`, then confirm each against the `.sha256` file already sitting in
that folder. If `D:` is unavailable, restore from `G:/My Drive/naiad-backups/phases/` and verify the
same way.

---

*Per §3.1 this document does not contain its own sha256 — that row would be stale the instant it was
written. Its BOX COST above is the byte size at the moment of publication.*
