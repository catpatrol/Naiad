# RETENTION — archive estate vs the rule

Generated 2026-08-15T16:53:28Z by `scripts/backup_estate.py`.

**Rule:** keep the newest 4 estate generations and the newest 4 workflow generations. **Phase archives are permanent evidence and are never prunable.**
**This report never deletes anything.** It names what falls outside the generation rule; acting on it is the operator's call.

## Estate generations

Location: `/Volumes/LaCie/naiad-backups`

7 generation(s) present; 4 within the rule, 3 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_estate_2026-08-15.zip` | 495,635,403 | yes |
| `naiad_estate_2026-08-15-02.zip` | 497,146,734 | yes |
| `naiad_estate_2026-08-15-01.zip` | 497,146,713 | yes |
| `naiad_estate_2026-08-11.zip` | 495,619,988 | yes |
| `naiad_estate_2026-08-09.zip` | 495,130,299 | **NO — outside the rule** |
| `naiad_estate_2026-08-02.zip` | 493,542,600 | **NO — outside the rule** |
| `naiad_estate_2026-07-28.zip` | 492,306,779 | **NO — outside the rule** |

## Workflow generations

Location: `/Volumes/LaCie/naiad-backups`

10 generation(s) present; 4 within the rule, 6 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_workflow_2026-08-15.zip` | 4,183,212 | yes |
| `naiad_workflow_2026-08-12.zip` | 2,749,895 | yes |
| `naiad_workflow_2026-08-12-03.zip` | 3,664,349 | yes |
| `naiad_workflow_2026-08-12-02.zip` | 3,637,063 | yes |
| `naiad_workflow_2026-08-12-01.zip` | 3,579,058 | **NO — outside the rule** |
| `naiad_workflow_2026-08-11.zip` | 2,721,722 | **NO — outside the rule** |
| `naiad_workflow_2026-08-09.zip` | 2,529,667 | **NO — outside the rule** |
| `naiad_workflow_2026-08-04.zip` | 1,794,646 | **NO — outside the rule** |
| `naiad_workflow_2026-08-02.zip` | 1,132,236 | **NO — outside the rule** |
| `naiad_workflow_2026-08-02 (1).zip` | 1,132,236 | **NO — outside the rule** |

## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy of a newer one — it is the only copy of work that will never be produced again.

Location: `/Users/luis/Naiad/research_outputs/_archive`

**CURRENT CYCLE EMPTY — this is BY DESIGN and is NOT a finding.**

Under the zip-residency ruling (operator, 2026-08-15) *new zips are born local and older zips live on the LaCie*. An empty local `_archive` means every archive written so far has been aged out to the backup volume — which is the intended end state of a cycle, not a missing archive. The tracked sidecars below are the standing fingerprint set and are always present; the aged-out archives are enumerated further down when the volume is reachable.

**FINGERPRINT SET: 9 tracked sidecar(s) in `research_outputs/_archive/`.** These are committed, so they describe the archive set from any clone, with no volume attached and no zip present locally.

Aged-out archives: `/Volumes/LaCie/Naiad/research_outputs/_archive`
- **[backup] 9 archive(s), 1,043,591,544 B (1,043.6 MB)** on `/Volumes/LaCie`.

Backup copy: `/Volumes/LaCie/naiad-backups/phases`
- **[backup] 9 archive(s), 1,043,591,544 B** on `/Volumes/LaCie`.
