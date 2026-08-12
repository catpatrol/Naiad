# RETENTION — archive estate vs the rule

Generated 2026-08-12T10:58:26Z by `scripts/backup_estate.py`.

**Rule:** keep the newest 4 estate generations and the newest 4 workflow generations. **Phase archives are permanent evidence and are never prunable.**
**This report never deletes anything.** It names what falls outside the generation rule; acting on it is the operator's call.

## Estate generations

Location: `D:\naiad-backups`

4 generation(s) present; 4 within the rule, 0 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_estate_2026-08-11.zip` | 495,619,988 | yes |
| `naiad_estate_2026-08-09.zip` | 495,130,299 | yes |
| `naiad_estate_2026-08-02.zip` | 493,542,600 | yes |
| `naiad_estate_2026-07-28.zip` | 492,306,779 | yes |

Nothing to consider: fewer than 5 generations exist.

## Workflow generations

Location: `D:\naiad-backups`

9 generation(s) present; 4 within the rule, 5 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_workflow_2026-08-12.zip` | 2,749,895 | yes |
| `naiad_workflow_2026-08-12-03.zip` | 3,664,349 | yes |
| `naiad_workflow_2026-08-12-02.zip` | 3,637,063 | yes |
| `naiad_workflow_2026-08-12-01.zip` | 3,579,058 | yes |
| `naiad_workflow_2026-08-11.zip` | 2,721,722 | **NO — outside the rule** |
| `naiad_workflow_2026-08-09.zip` | 2,529,667 | **NO — outside the rule** |
| `naiad_workflow_2026-08-04.zip` | 1,794,646 | **NO — outside the rule** |
| `naiad_workflow_2026-08-02.zip` | 1,132,236 | **NO — outside the rule** |
| `naiad_workflow_2026-08-02 (1).zip` | 1,132,236 | **NO — outside the rule** |

## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy of a newer one — it is the only copy of work that will never be produced again.

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

There is no keep-count for phase archives and no circumstance under which this report will list one as prunable.
