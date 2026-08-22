# BUILDERS_REPORT — HEPHAESTUS — 2026-08-12 — ONEDRIVE-CENSUS

**Phase:** read-only safety audit after an accidental OneDrive "Free up space" on the repo tree,
with the OneDrive quota showing full.
**Lane commissioning:** ATHENA. **Repo:** naiad. **Branch:** v12-v1-census. **HEAD:** 7552d65.
**Nothing was written to the repo tree by the audit. No file CONTENTS were read except three files
verified HYDRATED first. No rehydration, pinning, or OneDrive action was taken.**

---

## 1 · What "Free up space" actually did, in plain language

OneDrive did not delete anything. It replaced the *contents* of some files with placeholders: the
name, the size and the icon stay in the folder, but the bytes now live only in Microsoft's cloud.
Windows calls this a **dehydrated** file. Opening one silently downloads it again — which is why
this audit read file *attributes* only and never opened a dehydrated file.

**164 of the 839 files in the repo tree are now placeholders, holding 299.4 MB that is no longer
on this disk.**

The question that matters is not "how many are dehydrated" — it is **"which of those has no second
copy anywhere else."** That is the whole audit.

---

## 2 · Gate and probe values, as printed

```
pwd=/c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad  branch=v12-v1-census  head=7552d65

=== 1 - GIT TRUTH: what is already safe on GitHub ===
  local HEAD : 7552d652eb3717a9d90466fc81f7cb5508a00924
  origin     : 7552d652eb3717a9d90466fc81f7cb5508a00924
  ## v12-v1-census...origin/v12-v1-census
   M .gitignore
  modified tracked files : 1
  untracked files        : 10
  7552d65 exchange: auto-publish 2026-08-11
  4479606 exchange: auto-publish 2026-08-12
  f83d321 close-out: unmask the routine (F-P6), truthful queue counters (F-Q1), F-AN-15 follows the moved contract

=== 2 - PLACEHOLDER CENSUS: attributes only, no content reads ===
  files walked: 839   DEHYDRATED (cloud-only): 164   (299.4 MB no longer on disk)
       82  research_outputs
       22  (root)
       22  _reviewer_box
       19  fixtures
        4  tests
        3  .github
        3  .pytest_cache
        3  journal
        3  study
        2  pine
  dehydrated TRACKED files: 112

=== 3 - THE LOCAL-ONLY EXPOSURE SET: is it still hydrated? ===
  research_outputs/seq8                    1783.5 MB    15 files  dehydrated: 0
  research_outputs/mc1                      155.3 MB    30 files  dehydrated: 0
  research_outputs/census                   208.1 MB     7 files  dehydrated: 6
  LEDGER.md                                   0.2 MB  on disk
  exchange/status/CONVENTIONS.md              0.0 MB  on disk
  exchange/status/LEDGER_ATHENA.md            0.0 MB  on disk
```

Section 3 raised exactly one flag — `research_outputs/census` — so the audit was extended to
classify **every** dehydrated file by whether a second copy exists.

---

## 3 · Full result table — all 164 placeholders classified by second copy

```
=== 5 - DEHYDRATED FILES CLASSIFIED BY SECOND COPY ===
  A. dehydrated + TRACKED (clean vs HEAD, HEAD==origin) -> recoverable from GitHub
     112 files, 12.2 MB
  B. dehydrated + untracked but MATCHED in D:/naiad mirror -> recoverable from D:
     0 files, 0.0 MB
  C. dehydrated + untracked + NO mirror match -> ONEDRIVE CLOUD IS THE ONLY COPY
     52 files, 287.2 MB
```

**Class A — 112 files, 12.2 MB — SAFE.** Tracked, and the working tree is clean against HEAD apart
from `.gitignore` (still on disk). Local HEAD is byte-identical to `origin/v12-v1-census`, so every
one of these is a `git checkout` away regardless of what OneDrive does.

**Class C — 52 files, 287.2 MB — the entire exposure set.** Untracked, dehydrated, and not matched
in the D: mirror. **98.7% of it is six files:**

| MB | path | what it is |
|---:|---|---|
| 110.92 | `research_outputs/census/census_outcomes.jsonl` | census substrate |
| 43.43 | `v12_v3_anchor_packet_20260713.zip` | packet, repo root |
| 43.23 | `research_outputs/census/census_ladder.jsonl` | census substrate |
| 35.94 | `research_outputs/census/census_termini.jsonl` | census substrate |
| 32.08 | `census1b_termini_enriched.jsonl` | census 1b, repo root |
| 17.97 | `research_outputs/census/continuation.jsonl` | census substrate |
| **283.6** | **six files** | **of 287.2 MB total** |

The remaining 46 files total 3.6 MB and are almost entirely `_reviewer_box/` mirrors of tracked
repo files and `.pytest_cache/` — reconstructible, not worth a rescue.

`research_outputs/census` in detail — the tracked/untracked split inside one directory:

```
  research_outputs/census/build_manifest.json      0.0 MB  on disk    tracked
  research_outputs/census/census_ladder.jsonl     43.2 MB  DEHYDRATED UNTRACKED
  research_outputs/census/census_outcomes.jsonl  110.9 MB  DEHYDRATED UNTRACKED
  research_outputs/census/census_termini.jsonl    35.9 MB  DEHYDRATED UNTRACKED
  research_outputs/census/continuation.jsonl      18.0 MB  DEHYDRATED UNTRACKED
  research_outputs/census/refetch_log.json         0.0 MB  DEHYDRATED tracked
  research_outputs/census/retrieval_meta.json      0.0 MB  DEHYDRATED tracked
```

The three tracked JSONs are Class A — on GitHub. The four `.jsonl` substrates, 208.1 MB, are the
single largest concentration of risk in the tree.

---

## 4 · What is NOT at risk — confirmed, not assumed

```
=== 3e - D: MIRROR TOTALS (attributes only) ===
  D:/naiad  ->  44 files  4.46 GB  dehydrated: 0
    research_outputs/_archive                    995.2 MB   18 files  dehydrated:0
    research_outputs/seq8                       1783.5 MB   15 files  dehydrated:0
    research_outputs/seq8_run2                  1783.5 MB   11 files  dehydrated:0

=== 3g - SEQ8 SIDE-BY-SIDE (sizes only; sha compare NOT run - it would rehydrate) ===
  research_outputs/seq8                         1783.5 MB  15 files  dehydrated:0
  D:/naiad/research_outputs/seq8                1783.5 MB  15 files  dehydrated:0
```

- **seq8 was not touched.** 1783.5 MB, 15 files, **zero** dehydrated in the repo copy, and the D:
  mirror matches file-for-file and byte-for-byte on size. Two full local copies survive.
- **mc1 was not touched.** 155.3 MB, 30 files, zero dehydrated.
- **`D:/naiad` is not a OneDrive path** and was completely unaffected — 44 files, 4.46 GB, zero
  dehydrated. It is the natural destination for any rescue.
- **`LEDGER.md`, `CONVENTIONS.md`, `LEDGER_ATHENA.md` are all on disk.** The governance surface is
  intact.
- **All uncommitted work survived on disk** — the one material with no protection at all:

```
   M .gitignore                                     0.00 MB  on disk
  ?? Cascade Rewire.html                            0.23 MB  on disk
  ?? Cascade_Atlas_CENSUS_1b.html                   0.02 MB  on disk
  ?? Cascade_Atlas_CENSUS_1b_v2_1.html              0.05 MB  on disk
  ?? HANDOFF_ATHENA_2026-08-03_FULL_STATE_1.md      0.03 MB  on disk
  ?? PRIMER_HERMES_2026-08-03_v2_FIRST_RUN.md       0.01 MB  on disk
  ?? SS_Reassessment_Synthesis_2026-08-03.md        0.01 MB  on disk
  ?? briefs/panel/excursions/2026-08-03.parquet     0.01 MB  on disk
  ?? research_outputs/wf1/                          0.11 MB  1 files  dehydrated:0
  ?? scripts/mc1_program.py                         0.10 MB  on disk
  ?? scripts/mc1_report.py                          0.01 MB  on disk
```

Free space, for sizing any rescue: **C: 35.6 GB free** (of 236.3 GB), **D: 3721.2 GB free** (of
3725.7 GB). Rehydrating the entire 287.2 MB exposure set costs under 1% of the C: headroom.

---

## 5 · Findings reported, NOT fixed

**F-OD-1 — the 208.1 MB census substrate has one copy, in a cloud account whose quota is full.**
Four `.jsonl` files, untracked (so not on GitHub), not in the D: mirror, and now dehydrated. This
is the finding of the session.

**F-OD-2 — the "is it really in the cloud?" question is reasoned, not verified. [open]**
OneDrive only dehydrates a file whose upload has *completed*; a file that failed to upload stays
hydrated and shows a sync error. On that mechanism, a placeholder is itself evidence that the cloud
holds the bytes — which is reassuring, because it means the full quota did **not** strand these
files. **This audit did not confirm it from the cloud side, and could not:** the only direct
confirmation is to open a file, which downloads it, which is precisely what the instruction
forbade. Treat F-OD-2 as unconfirmed-live until a deliberate rehydration proves it.

**F-OD-3 — the exposure is a gitignore consequence, not an accident.** Class B is *zero* files:
nothing dehydrated has a D: mirror copy. The mirror covers seq8 and the archives only. Everything
untracked outside those two areas has always had exactly one copy — "Free up space" did not create
that gap, it revealed it.

**F-OD-4 — `.pytest_cache/` is inside the sync selection** (3 dehydrated files). Harmless, but it
means transient build artifacts are consuming OneDrive quota that the census substrates need.

---

## 6 · Honest next options, with implications — operator's call, nothing done

1. **Copy the six Class-C files (283.6 MB) to `D:/naiad/`.** Ends the exposure permanently, and D:
   has 3.7 TB free. **Implication:** copying a dehydrated file *forces its download* — this spends
   287 MB of C: headroom and requires the cloud copy to actually be there, so it is also the test
   of F-OD-2. Do this first; it is the only option that removes risk rather than relocating it.
2. **Track the census substrates in git.** 208 MB of `.jsonl` in a repo is heavy and would need
   LFS; the ATHENA 2026-08-12 close-out already carries "decide whether `research_outputs/wf1/` and
   `mc1/` should be tracked" as an open item — this is the same decision, one directory wider.
3. **"Always keep on this device" on `research_outputs/`.** Stops future dehydration.
   **Implication:** it *increases* OneDrive quota pressure, and the quota is already full — this
   fights the condition that caused the event. Not recommended before option 1.
4. **Move `research_outputs/` out of the OneDrive tree entirely.** Cleanest long-term fix, largest
   blast radius: every script path, the backup estate and the D: mirror logic would need review.
5. **Do nothing.** Defensible for Class A (112 files, GitHub-backed). Not defensible for the six
   Class-C files while the quota is full.

**Recommendation: option 1 now, then rule on options 2 and 4 together.** Option 3 is the one to
avoid.

---

## 7 · Verdict

- **Every tracked file in this repo is safe.** HEAD equals origin, the tree is clean, and the 112
  dehydrated tracked files are recoverable from GitHub whatever OneDrive does.
- **seq8 is safe twice over** — untouched locally and mirrored on D: at matching size.
- **All uncommitted work is still on disk.**
- **The real exposure is 287.2 MB across 52 untracked placeholders, and 98.7% of it is six files** —
  four census substrates, one census-1b enriched file, one v3 anchor packet. For those six, the
  OneDrive cloud is the only copy that exists.

---

## 8 · File-disposition table (§3.2)

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-12_ONEDRIVE-CENSUS.md` | yes | untracked at time of writing | not committed | no | **NOT PROTECTED** until the next `exchange` publish | ~11.7 KB — ~0.18% of the 6.39 MB box (stated rounded: a file cannot carry its own exact final size, same reason §3.2 forbids its own sha256) |
| `exchange/status/LEDGER_ATHENA.md` | yes | tracked | last at 7552d65; this append not committed | append not pushed | GitHub once committed | **+3,738 B — +0.06% of the box**; 20,230 B → 23,968 B, 10 STATUS_ATHENA blocks |

No other file was created, modified or moved. The audit itself wrote nothing.
