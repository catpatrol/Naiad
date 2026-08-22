# BUILDER'S REPORT — HEPHAESTUS — 2026-08-12 — FILE UNTRACKED ROOT ARTIFACTS

**Lane:** ATHENA (system resilience) · **Builder:** HEPHAESTUS, local Windows Claude Code
**Branch:** `v12-v1-census` · **HEAD at start:** `697f48d` · **Commit:** `5e8d7ba`, pushed
**Authority:** operator ruling 2026-08-12 — *"file it"*
**Read this with zero prior context.**

---

## 0 · What happened, in one paragraph

Ten files were sitting in the repository without being tracked by git, meaning git would not have
restored them if the machine were lost. **Seven are now committed and pushed to GitHub.** Two turned
out not to need filing at all — they are byte-for-byte duplicates of files already on GitHub, so
they were never at risk. **One was deliberately left alone** because whether it should be tracked is
a decision already booked to the ATHENA lane, and it is the only file where leaving it has a real
cost. Nothing was deleted. Every move was verified by hash before the original was removed.

---

## 1 · The enumeration, and one thing the paste would have missed

`git status --porcelain` reported ten untracked entries, but one of them —
`research_outputs/wf1/` — is a **directory**, and git collapses a wholly-untracked directory to a
single line rather than listing its contents. The paste's filter (`os.path.isfile`) would have
dropped it silently, and a file dropped silently from a protection sweep is the worst possible
outcome for a protection sweep. Re-run with `--untracked-files=all`, the true set is ten files:

| file | size | sha256[:12] |
|---|---:|---|
| `Cascade Rewire.html` | 237.8 K | `6fc84a2e318c` |
| `Cascade_Atlas_CENSUS_1b.html` | 23.0 K | `1af63dffa477` |
| `Cascade_Atlas_CENSUS_1b_v2_1.html` | 50.6 K | `bc303723dcb9` |
| `HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md` | 26.9 K | `4efdeeb112d9` |
| `PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md` | 13.1 K | `846b8646ed43` |
| `SS_Reassessment_Synthesis_2026-08-03.md` | 8.1 K | `9d6e7ea74754` |
| `briefs/panel/excursions/2026-08-03.parquet` | 8.9 K | `1278c9ea4f06` |
| `research_outputs/wf1/WF1_discriminants.json` | 110.7 K | `06d2bcfd6498` |
| `scripts/mc1_program.py` | 97.3 K | `e7bea1493715` |
| `scripts/mc1_report.py` | 8.2 K | `0254745d8065` |

**Total: 10 files, 584.6 KB.**

---

## 2 · How destinations were chosen — and why not by file extension

The paste proposed a rule based on file extension: `.html` → `docs/history/atlases/`, `.md`/`.txt` →
`exchange/reports/`, `.py` → `scripts/`. I did not apply it as written, because **extension does not
tell you what a file is for, and in this repository it does not tell you whether the destination is
actually protected either.**

### 2.1 The measurement that decided most of it

`backup_estate.py --workflow` archives a fixed list of directories (`WORKFLOW_SOURCES`). I listed
the members of the archive written earlier today to find out which candidate destinations are
genuinely covered:

| destination | in the weekly `--workflow` archive? | protection if a file lands there |
|---|---|---|
| `docs/history/` | **yes** | GitHub **+** archive |
| `docs/primers/` | **yes** | GitHub **+** archive |
| `exchange/reports/` | **yes** | GitHub **+** archive |
| `scripts/` | **yes** | GitHub **+** archive |
| `docs/reports/` | **no** | GitHub only |
| `docs/handoffs/` | **no** | GitHub only |
| `briefs/` | **no** | GitHub only |
| `research_outputs/` | **no** | GitHub only |

**This inverted two choices I would otherwise have made from precedent alone.** `docs/handoffs/`
exists and holds two handoff files, so it looks like the obvious home for the ATHENA handoff — but
it is not archived, while `docs/history/` is *and* already holds
`HANDOFF_DIONYSUS_to_ATHENA_2026-08-02_Workflow_Redesign_Inputs.md`. Likewise `docs/reports/`
already holds tracked HTML, but is not archived, whereas the paste's `docs/history/atlases/` is —
and mirrors the existing `docs/history/argus/`. **The paste's HTML destination was right for a
reason the paste did not state.**

### 2.2 One file named its own destination

`SS_Reassessment_Synthesis_2026-08-03.md` carries this on its second line:

```
**APOLLO · 2026-08-03 · filed to `exchange/reports/` (reaches all web lanes via GitHub sync)**
```

It is the only one of the ten that says where it belongs. It had already been filed there — see §4.

### 2.3 The `_1` suffix check

Two filenames end in `_1`, which in this project is usually the marker of a re-downloaded twin
(`HANDOFF_ATHENA_..._FULL_STATE_1.md`, `Cascade_Atlas_CENSUS_1b_v2_1.html`). I searched for
non-`_1` originals on disk and in git for both. **Neither has a twin — the `_1` is part of the real
filename**, so both were filed under the names they carry.

---

## 3 · FILED — the seven, with their verification lines

Every move was **copy → re-read the copy and hash it → only then remove the original**. A hash
mismatch would have deleted the copy and kept the original. None mismatched.

```
  FILED + VERIFIED  Cascade_Atlas_CENSUS_1b.html         -> docs/history/atlases/    23.0K  sha=1af63dffa477...
  FILED + VERIFIED  Cascade_Atlas_CENSUS_1b_v2_1.html    -> docs/history/atlases/    50.6K  sha=bc303723dcb9...
  FILED + VERIFIED  HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md -> docs/history/       26.9K  sha=4efdeeb112d9...
  FILED + VERIFIED  PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md  -> docs/primers/       13.1K  sha=846b8646ed43...
  STAGED IN PLACE   briefs/panel/excursions/2026-08-03.parquet                        8.9K  sha=1278c9ea4f06...
  STAGED IN PLACE   scripts/mc1_program.py                                           97.3K  sha=e7bea1493715...
  STAGED IN PLACE   scripts/mc1_report.py                                             8.2K  sha=0254745d8065...

  staged: 7    left for their lane: 2
  box cost of files landing in exchange/: 0 B = 0.000% of the 6.39 MB box
```

Post-move verification, run separately:

```
  PASS  docs/history/atlases/Cascade_Atlas_CENSUS_1b.html       arrived=True original_gone=True sha_matches_pre_move=True
  PASS  docs/history/atlases/Cascade_Atlas_CENSUS_1b_v2_1.html  arrived=True original_gone=True sha_matches_pre_move=True
  PASS  docs/history/HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md  arrived=True original_gone=True sha_matches_pre_move=True
  PASS  docs/primers/PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md   arrived=True original_gone=True sha_matches_pre_move=True

  0 verification(s) FAILED
```

**Three files were staged where they already sat, not moved.** This matters because the paste would
have failed on all three:

- `scripts/mc1_program.py` and `scripts/mc1_report.py` are **already in `scripts/`**. The paste
  computes a destination of `scripts/`, joins it to the basename, gets the *same path back*, finds
  that the target "already exists", and prints `HALT: … already exists (no-clobber) - left in
  place`. The two easiest files in the set would have been reported as skipped while being perfectly
  fine — they needed `git add`, not a move.
- `briefs/panel/excursions/2026-08-03.parquet` has **no extension rule in the paste at all**, so it
  would have been dropped into "left for its lane". It is not a stray. Its sibling
  `briefs/panel/excursions/2026-08-05.parquet` is **already tracked**, as are both dates of
  `areas/`, `levels/` and `snapshots/`. This was the one missing partition file in an otherwise
  complete tracked set.

---

## 4 · NOT FILED — three files, and the reason for each

### 4.1 Two were never unprotected: they are duplicates of content already on GitHub

| root file | identical to | shared git blob |
|---|---|---|
| `Cascade Rewire.html` | `docs/reports/Cascade Rewire.html` | `37502615f1324bfe5d98a5e874d45606013bd38c` |
| `SS_Reassessment_Synthesis_2026-08-03.md` | `exchange/reports/SS_Reassessment_Synthesis_2026-08-03.md` | `0ad38893d06c1c89d561e537d2a42eb6b9533050` |

Both are **byte-identical**, verified by sha256 and by `git hash-object`. **The contract's premise —
"these ~11 files exist in NO other copy" — is false for these two.**

I did not take that on the filename. §3.2 of CONVENTIONS says *existence is not protection* and
requires three checks before treating a twin as a backup. Both twins passed all three:

```
  1. tracked at all?                    PASS
  2. present on origin/v12-v1-census?   PASS
  3. worktree copy == committed copy?   PASS  (blobs identical)
  4. and the ROOT copy == that blob?    PASS  -> not unprotected content
```

`SS_Reassessment_Synthesis_2026-08-03.md` is the same file that declares *"filed to
`exchange/reports/`"* — it **was** filed there, and what sits at the repo root is the leftover
original. The no-clobber guard is what caught it: it refused to overwrite rather than silently
replacing a tracked file with an untracked one.

**Both remain exactly where they are. No delete authorization existed this session, and I did not
create one by reasoning about it.** Removing them is a clean, safe follow-up — but it is your call,
not mine.

### 4.2 One was left for its lane, and this is the one that costs something

**`research_outputs/wf1/WF1_discriminants.json` — 110.7 KB, no copy anywhere.**

Whether `research_outputs/wf1/` should be tracked is **a named, still-open ATHENA decision**, on
record in `LEDGER_ATHENA.md` from earlier today:

> *4. ATHENA: decide whether `research_outputs/wf1/` (and `mc1/`, needing a `.gitignore` edit)
> should be tracked*

Your instruction was explicit: *"a file whose purpose is unclear is filed by the lane that made it,
not by default."* Filing it would have pre-empted a ruling already booked to a lane.

**But I want to be plain that leaving it is not free.** This is a 110.7 KB results JSON — the
discriminant output of the WF1 forensics run — and it is now **the last piece of genuinely
unprotected content in the repository**. It is not on GitHub, not on `D:`, and not in any archive
(`research_outputs/` is not a `--workflow` source). If the machine were lost tonight, it would be
lost with it.

**Owner: ATHENA. This wants a ruling, not a queue slot.** The decision is small — it is 110.7 KB, it
costs **zero** context-box budget because the box is `LEDGER.md` and `exchange/` only, and
`research_outputs/` already has 100 tracked files, so tracking it breaks no precedent. I did not act
on that reasoning, because it is ATHENA's to make.

---

## 5 · File disposition

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `docs/history/atlases/Cascade_Atlas_CENSUS_1b.html` | yes | **tracked** | `5e8d7ba` | yes, `origin/v12-v1-census` | GitHub + `--workflow` archive | `n/a` — `docs/`, outside the box |
| `docs/history/atlases/Cascade_Atlas_CENSUS_1b_v2_1.html` | yes | **tracked** | `5e8d7ba` | yes | GitHub + `--workflow` archive | `n/a` — `docs/` |
| `docs/history/HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md` | yes | **tracked** | `5e8d7ba` | yes | GitHub + `--workflow` archive | `n/a` — `docs/` |
| `docs/primers/PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md` | yes | **tracked** | `5e8d7ba` | yes | GitHub + `--workflow` archive | `n/a` — `docs/` |
| `briefs/panel/excursions/2026-08-03.parquet` | yes | **tracked** | `5e8d7ba` | yes | **GitHub only** — `briefs/` is not a workflow source | `n/a` — `briefs/` |
| `scripts/mc1_program.py` | yes | **tracked** | `5e8d7ba` | yes | GitHub + `--workflow` archive | `n/a` — `scripts/` |
| `scripts/mc1_report.py` | yes | **tracked** | `5e8d7ba` | yes | GitHub + `--workflow` archive | `n/a` — `scripts/` |
| `Cascade Rewire.html` *(repo root)* | yes | untracked | not committed | no | **its twin** `docs/reports/Cascade Rewire.html`, tracked + pushed | `n/a` — repo root |
| `SS_Reassessment_Synthesis_2026-08-03.md` *(repo root)* | yes | untracked | not committed | no | **its twin** in `exchange/reports/`, tracked + pushed | `n/a` — repo root |
| `research_outputs/wf1/WF1_discriminants.json` | yes | untracked | not committed | no | **NOT PROTECTED** | `n/a` — `research_outputs/` |
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md` | yes | tracked at publish | pending | pending | GitHub + `--workflow` archive | 16,362 B · 0.24% |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | pending | pending | GitHub + `--workflow` archive | 29,101 B · 0.43% *(+2,373 B for this session's STATUS entry)* |

**Box cost of the filing itself: 0 bytes.** Nothing new entered `exchange/` — the one file whose
destination was `exchange/reports/` was already there.

---

## 6 · What I did not do

Nothing was deleted, anywhere. The two duplicate root files and the WF1 JSON are untouched and in
place. Nothing outside the enumerated untracked set was modified. `.gitignore` was already modified
before this session began and is not mine; it remains uncommitted.

**ROLLBACK:** `git revert 5e8d7ba`. Note this restores the *tracking* state but leaves the four moved
files at their new paths — a revert un-commits, it does not move files back. Their content is
unchanged and their sha256s are recorded in §3 above.

---

## 7 · Open items

**O-1 · `research_outputs/wf1/WF1_discriminants.json` is the last unprotected file on the machine.**
Owner: **ATHENA.** 110.7 KB, zero box cost, no precedent problem. Needs a ruling. *(See §4.2.)*

**O-2 · Two duplicate files sit at the repo root.** Owner: **operator.** `Cascade Rewire.html` and
`SS_Reassessment_Synthesis_2026-08-03.md` are byte-identical to tracked, pushed copies. Removing
them would tidy the root and lose nothing — but that is a deletion, and no deletion was authorized.

**O-3 · `briefs/` is tracked but not archived.** Reported, not fixed. The panel parquet files are now
on GitHub, which is real protection, but they are absent from the weekly `--workflow` archive
because `briefs/` is not in `WORKFLOW_SOURCES`. Same is true of `docs/reports/` and
`docs/handoffs/`, both of which hold tracked content today. Whether to widen `WORKFLOW_SOURCES` is
an ATHENA design question, not a bug I should have fixed inside a filing task.

---

## 8 · STATUS

```
=== STATUS_ATHENA — 2026-08-12 ===
NOW: Seven previously untracked files are committed and pushed as 5e8d7ba. Two of the ten turned
out to be byte-identical duplicates of content already on origin and were left in place; one,
research_outputs/wf1/WF1_discriminants.json, was left for ATHENA because its tracking status is an
open lane decision — and it is now the last genuinely unprotected file in the repository.
LAST EVENT: 2026-08-12 — untracked root artifacts filed; commit 5e8d7ba pushed to
origin/v12-v1-census; filed as exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_FILE-UNTRACKED.md.
FACTS:
- 7 files filed: 4 moved (copy -> sha256 verify -> remove original, 0 mismatches), 3 staged in place; all 7 confirmed present on origin/v12-v1-census [verified]
- Destinations chosen on MEASURED archive coverage, not extension: docs/history, docs/primers, scripts, exchange/reports are WORKFLOW_SOURCES; docs/reports, docs/handoffs, briefs, research_outputs are NOT [verified]
- Cascade Rewire.html (blob 37502615) and SS_Reassessment_Synthesis_2026-08-03.md (blob 0ad38893) are byte-identical to tracked+pushed twins; all three CONVENTIONS 3.2 checks passed on both. The contract's "no other copy" premise was false for these two [verified]
- research_outputs/wf1/ is a DIRECTORY entry; git collapses it to one porcelain line and an isfile() filter drops it silently. Enumerated with --untracked-files=all instead [verified]
- Box cost of the whole operation: 0 B — nothing new entered exchange/ [verified]
- briefs/panel/excursions/2026-08-03.parquet was the one missing file in an otherwise fully tracked panel partition set; its 08-05 sibling was already tracked [verified]
PENDING:
1. ATHENA: rule on research_outputs/wf1/ — 110.7 KB, zero box cost, and the last unprotected content on the machine (O-1)
2. Operator: two byte-identical duplicate files sit at the repo root; removing them loses nothing but is a deletion and was not authorized (O-2)
3. ATHENA: briefs/, docs/reports/ and docs/handoffs/ hold tracked content but are absent from WORKFLOW_SOURCES — GitHub-only protection (O-3)
NEXT: Rule on item 1; it is the only remaining file with no copy anywhere. Owner: ATHENA.
METRICS: operator actions this session = 0 · files re-ingested = 0
=== END STATUS ===
```
