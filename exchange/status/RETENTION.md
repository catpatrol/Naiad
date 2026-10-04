# RETENTION — archive estate vs the rule

Generated 2026-10-04T11:33:32Z by `scripts/backup_estate.py`.

**Rule:** keep the newest 4 estate generations and the newest 4 workflow generations. **Phase archives are permanent evidence and are never prunable.**
**This report never deletes anything.** It names what falls outside the generation rule; acting on it is the operator's call.

## Estate generations

Location: `/Volumes/LaCie/naiad-backups`

1 generation(s) present; 1 within the rule, 0 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_estate_2026-09-27.zip` | 633,529,440 | yes |

Nothing to consider: fewer than 5 generations exist.

## Workflow generations

Location: `/Volumes/LaCie/naiad-backups`

2 generation(s) present; 2 within the rule, 0 outside it.

| generation | size (B) | within rule |
|---|---:|---|
| `naiad_workflow_2026-10-04.zip` | 10,396,732 | yes |
| `naiad_workflow_2026-09-27.zip` | 10,395,500 | yes |

Nothing to consider: fewer than 5 generations exist.

## PHASE ARCHIVES — PERMANENT EVIDENCE, NEVER PRUNE

Each phase archive holds a DIFFERENT phase's evidence, so an older one is not a superseded copy of a newer one — it is the only copy of work that will never be produced again.

Location: `/Users/luis/Naiad/research_outputs/_archive`

**CURRENT CYCLE EMPTY — this is BY DESIGN and is NOT a finding.**

Under the zip-residency ruling (operator, 2026-08-15) *new zips are born local and older zips live on the LaCie*. An empty local `_archive` means every archive written so far has been aged out to the backup volume — which is the intended end state of a cycle, not a missing archive. The tracked sidecars below are the standing fingerprint set and are always present; the aged-out archives are enumerated further down when the volume is reachable.

**FINGERPRINT SET: 9 tracked sidecar(s) in `research_outputs/_archive/`.** These are committed, so they describe the archive set from any clone, with no volume attached and no zip present locally.

Aged-out archives: `/Volumes/LaCie/Naiad/research_outputs/_archive`
- **[backup] 9 archive(s), 1,043,591,544 B (1,043.6 MB)** on `/Volumes/LaCie`.

Backup copy: `/Volumes/LaCie/naiad-backups/phases`
- **[backup] volume mounted, `/Volumes/LaCie/naiad-backups/phases` does not exist** — the phase archives have never been mirrored there.
