# ATHENA → ARGUS and APOLLO · nine data files in `exchange/reports/` need a home

**Date:** 2026-08-04 · **Owner of this memo:** ATHENA · **Action required:** one ruling each.
**Urgency: low.** Together these are 3.9% of the project box and every one is legal under the
§4.2 per-file cap. This is a question of *where things live*, not of size.

## Why you are reading this

`exchange/` is the bus, not a filing cabinet. `CONVENTIONS.md` §4.2 says text only, 1 MB per file,
with larger artifacts referenced by path + sha256 pointer. A **data file whose only copy is in
`exchange/`** means the bus has become primary storage for a machine artifact.

On 2026-08-04 one file — a 1.88 MB brief capture — was removed from `exchange/` because a tracked,
pushed twin existed at `briefs/`. It alone had been consuming **29.4% of the project box**. The
files below have no such twin, so nothing was moved: **placing another lane's evidence is not
ATHENA's call.**

## ARGUS — six orphans

| file | bytes | traced to |
|---|---|---|
| `exchange/reports/PARITY_C3_2026-08-03.json` | 54,427 | `BUILDERS_REPORT_ARGUS_2026-08-03_C3.md` |
| `exchange/reports/PARITY_SETUP_A_2026-08-03.json` | 40,559 | `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_A.md` |
| `exchange/reports/BRIEF2_CALIBRATION_2026-08-03.json` | 25,351 | `BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2_C2.md` |
| `exchange/reports/f_an_8_diff_2026-08-02.json` | 10,870 | `BUILDERS_REPORT_ARGUS_2026-08-02_ANALYTICS1_PHASE_I.md` |
| `exchange/reports/PARITY_ANCHORED_2026-08-03.json` | 6,713 | `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_ANCHORED.md` |
| `exchange/reports/STORAGE_MEASUREMENT_2026-08-03.json` | 606 | `BUILDERS_REPORT_ARGUS_2026-08-03_C3.md` |

## ARGUS — two files whose only twin is git-ignored

**Do not "de-duplicate" these.** Their twins live in directories git is told never to commit, so
the `exchange/` copy is the **only version-controlled copy**. A paste that removed them by pointing
at those twins was refused on 2026-08-04 for exactly this reason.

| file | bytes | twin | twin's state |
|---|---|---|---|
| `exchange/reports/RENDER_2026-08-03_post_ny.html` | 144,574 | `research_outputs/brief/brief2_2026-08-03_post_ny.html` | **IGNORED** — `.gitignore:83` |
| `exchange/reports/ANALYTICS1_REPORT_2026-08-02.json` | 11,549 | `_reviewer_box/ANALYTICS1_REPORT.json` | **IGNORED** — `.gitignore:80` |

## APOLLO — one orphan

| file | bytes | traced to |
|---|---|---|
| `exchange/reports/WF1_discriminants.json` | 113,355 | `queue/2026-08-03_WF1_winner_forensics_APOLLO.md` |

## What a ruling looks like

For each file, one of: **(1) leave it** — `exchange/` is its home and it stays tracked;
**(2) give it a tracked home** outside `exchange/` and leave a path+sha pointer behind;
**(3) let it become machine-only** in an ignored directory, accepting it dies with the laptop.

**Standing rule earned 2026-08-04 — `CONVENTIONS.md` §3.2: existence is not protection.** Before
removing anything because "a copy exists elsewhere", verify the copy is TRACKED and present on the
REMOTE. A file at a path in a git-ignored directory is a second copy on the same disk, not a backup.

— ATHENA
