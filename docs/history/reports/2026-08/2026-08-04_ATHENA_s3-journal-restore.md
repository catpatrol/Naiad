# ATHENA - s3 journal restore for W-F1 - 2026-08-04

## Why W-F1 halted
APOLLO's W-F1 contract reads scored journals from
`research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/`. That path had never existed:
`_unarchived` appears in zero commits across all refs. It is a STAGING path the contract
assumed would be populated by un-archiving the s3 phase. That step was never issued.

The s3 phase was compressed into `research_outputs/_archive/` during the 2026-07-27 OneDrive
reclamation and its source directories emptied. `research_outputs/s3/journal_s3/scored/`
still holds its 20 cell folders but **0 files** - it is gitignored at `.gitignore:29` and the
journals are untracked, so they are simply not in any clone.

## What was NOT done, deliberately
The empty `research_outputs/s3/journal_s3/scored` was **not** substituted. Running W-F1
against it would have produced a forensics study over an empty journal set - an answer-shaped
artifact with no data behind it. The builder refused the substitution; that refusal was correct.

## What was done
Only the `journal_s3/scored/` subtree was extracted, not the whole phase, because restoring
the full s3 tree into the OneDrive-synced repo risks re-triggering the quota exhaustion that
caused the 2026-07-27 outage (21.78 GB / 22,731 files).

Gates cleared before any write: file count == 753 - uncompressed size under the 2 GB ceiling -
free space at least 3x the payload - **zero case-insensitive collisions** (the documented s3
and tc5 restore hazard, where `MANIFEST.json` and `manifest.json` silently overwrite each
other on Windows) - destination did not already exist.

Verified after write: on-disk count == 753, and sampled members re-read from disk hash equal
to the same members read out of the archive.

## Disposition
| path | exists | tracked | committed | pushed | protected by |
|---|---|---|---|---|---|
| research_outputs/_unarchived/s3_2026-07-27/journal_s3/scored/ | yes | ignored | no | no | the phase archive it came from |
| .gitignore | yes | tracked | see this session | with exchange publish | GitHub |
| exchange/reports/ (this file) | yes | tracked | this session | yes | --workflow archive |

The restored files are **staging, not evidence**. The evidence is the phase archive, which
was opened read-only and is untouched. Deleting the staging directory loses nothing.

## Next
Re-issue the W-F1 contract **unchanged**. Its path is now correct on disk, and F-WF1's
reconciliation (3825 + 78 + 3214 = 7117 fills; 7094 resolved + 23 excluded) can be checked
against real journals rather than assumed.
