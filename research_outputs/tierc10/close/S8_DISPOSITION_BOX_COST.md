## 8 · DISPOSITION · BOX-COST

> **PRE-CLOSE SNAPSHOT — regenerate after the CLOSE commit/push.** Every git column below is true of HEAD `3d55988` and of the remote-tracking refs as last fetched; the CLOSE commit and push change TRACKED, COMMITTED, PUSHED and PROTECTED BY for most rows. Re-run `scripts/tierc10_close_close_box_cost.py` after them and file THAT table.
>
> **REPORT-ONLY · Tier-E bookkeeping — paths, bytes and git metadata; no bar read, nothing scored, no verdict consulted.** Every table in this section is REPORT-ONLY.

The CLOSE item `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:136` (· findings-not-fixed · BOX-COST), built to the seven-column standard at `exchange/status/CONVENTIONS.md:341`. Built by `scripts/tierc10_close_close_box_cost.py` — transcript `research_outputs/tierc10/close/FIXTURES_CLOSE_box_cost.txt`.

**Constants — read by `ast.literal_eval` of their assignments; the modules are never imported or executed (F-BC-CONST):**

- `BOX_BYTES` = 16,000,000 B — `scripts/publish_exchange.py:95`
- `FLAG_BYTES` = 64,000 B — `scripts/publish_exchange.py:160`
- `SCOPE` = `exchange/` — `scripts/publish_exchange.py:48` · `TICK_EXTRA` = `LEDGER.md` — `scripts/publish_exchange.py:128` (box-bound = either)
- `WORKFLOW_SOURCES` — 14 roots — `scripts/backup_estate.py:227`; `WORKFLOW_ROOT_GLOBS` `*.md` — `scripts/backup_estate.py:247` (PROTECTED BY prints `--workflow` SCOPE only)

**Git state (git-volatile):** HEAD `3d55988` on `v12-v1-census` · upstream `origin/v12-v1-census` at `088d475` · HEAD is **29 commits ahead** of it · **0 of 28** `tierc10` commits are contained in any remote-tracking ref · no fetch was made.

**How each column is read.** PATH — the four sets below. EXISTS — `os.stat` now. TRACKED — `git ls-files`; if untracked, `git check-ignore -v` names the `.gitignore` line; a tracked file a pattern would ignore is named *force-added past* that line. COMMITTED — `git log -1 --format=%h -- <path>`. PUSHED — `git branch -r --contains <COMMITTED>` (refs as last fetched). PROTECTED BY — *GitHub only* when pushed and unmodified, else **NOT PROTECTED**; `--workflow` *scope* is printed, never an archive (this table does not read the LaCie). BOX COST — bytes and % of `BOX_BYTES` for box-bound paths, **FLAGGED** when strictly over `FLAG_BYTES` (`scripts/publish_exchange.py:363`), else *n/a — unsynced*, naming the root. Git verbs used: `log` · `ls-files` · `check-ignore` · `branch -r --contains` · `rev-parse` — nothing else (F-BC-GIT).

**`.gitignore` lines cited in TRACKED:** `.gitignore:263` = `research_outputs/tierc10/**`

### 8.0 · At a glance — REPORT-ONLY

| | count |
|---|---:|
| (a) paths in `tierc10` commits (28 commits) | 53 |
| (b) PROGRESS.json artifacts not already in (a) | 102 |
| (b) cells directories, collapsed | 4 |
| (c) PLANNED build document | 1 |
| (d) the frozen snapshot | 1 |
| rows · TRACKED state `ignored` | 106 |
| rows · TRACKED state `outside-repo` | 1 |
| rows · TRACKED state `tracked` | 53 |
| rows · TRACKED state `untracked` | 1 |
| rows with a COMMITTED sha | 53 |
| rows PUSHED (a remote-tracking ref contains the sha) | 0 |
| OR-1 rows (listed read-only) | 3 |
| box-bound rows | 2 |
| box-bound bytes (these rows) | 444,261 B · 2.777% of the box |
| **FLAGGED** rows (> 64,000 B) | 1 |

### 8.1 · (a) every path in a `tierc10` commit — 53 paths, 28 commits — REPORT-ONLY

Subject re-checked to start `tierc10` (`--grep` also matches body lines; 0 grep-only commit(s) dropped). `+PROGRESS` = also a PROGRESS.json artifact.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `.gitignore` | yes · 12,411 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`.gitignore`) |
| `analytics/rangefinder_census.py` | yes · 48,328 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`analytics/`) |
| `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` | yes · 9,441 B | tracked | `c7b157d` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `exchange` | 9,441 B · 0.059% of 16,000,000 B · under the 64,000 B wire |
| `research_outputs/tierc10/BUILD_DRAFT.md` | yes · 111,105 B | tracked · MODIFIED in worktree · force-added past `.gitignore:263` | `f97cded` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/FIXTURES_RESUME.txt` | yes · 111,005 B | tracked · force-added past `.gitignore:263` | `2416a15` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/LEDGER_5M.json` · +PROGRESS | yes · 91,036 B | tracked · force-added past `.gitignore:263` | `899d3e7` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/OPERATOR_RULINGS.md` | yes · 8,696 B | tracked · force-added past `.gitignore:263` | `ffdffce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/PROGRESS.json` | yes · 267,607 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/REGISTRATION_PLAN.md` | yes · 7,242 B | tracked · force-added past `.gitignore:263` | `54cfd60` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/REGISTRATION_TEXTS.json` · +PROGRESS | yes · 178,729 B | tracked · force-added past `.gitignore:263` | `371123f` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/REGISTRY_PIN.json` · +PROGRESS | yes · 2,897 B | tracked · force-added past `.gitignore:263` | `371123f` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/_partial_20260922T0955Z/README.md` | yes · 1,694 B | tracked · force-added past `.gitignore:263` | `f97cded` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/_partial_20260922T0955Z/lanes/FIXTURES_LANES_partial.txt` | yes · 4,692 B | tracked · force-added past `.gitignore:263` | `f97cded` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/_partial_20260922T0955Z/panel/FIXTURES_PANEL_partial.txt` | yes · 6,552 B | tracked · force-added past `.gitignore:263` | `f97cded` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/DRYRUN.json` · +PROGRESS | yes · 77,280 B | tracked · force-added past `.gitignore:263` | `b29774e` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/DRYRUN.txt` · +PROGRESS | yes · 49,536 B | tracked · force-added past `.gitignore:263` | `b29774e` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/FAMILY.json` · +PROGRESS | yes · 113,715 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/FINISH.txt` · +PROGRESS | yes · 1,001 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/FIXTURES_SCORE.txt` · +PROGRESS | yes · 19,239 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-BE-1.rows.json` · +PROGRESS | yes · 84,044 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-BRK-I1.rows.json` · +PROGRESS | yes · 111,150 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-BRK-S1.rows.json` · +PROGRESS | yes · 118,556 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-GEN-1.rows.json` · +PROGRESS | yes · 123,091 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-SPR-2.rows.json` · +PROGRESS | yes · 111,310 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/P-TRG-2.rows.json` · +PROGRESS | yes · 102,709 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-BE-1.txt` · +PROGRESS | yes · 2,125 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-BRK-I1.txt` · +PROGRESS | yes · 1,529 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-BRK-S1.txt` · +PROGRESS | yes · 1,613 B | tracked · force-added past `.gitignore:263` | `08a6fce` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-GEN-1.txt` · +PROGRESS | yes · 1,391 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-SPR-2.txt` · +PROGRESS | yes · 1,588 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/scores/SCORE_P-TRG-2.txt` · +PROGRESS | yes · 1,598 B | tracked · force-added past `.gitignore:263` | `ab7306a` | no | NOT PROTECTED — committed, not pushed · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `scripts/rangefinder_fixtures.py` · OR-1, listed read-only | yes · 25,211 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/rangefinder_fixtures_v2.py` · OR-1, listed read-only | yes · 21,784 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/rangefinder_twin.py` · OR-1, listed read-only | yes · 27,577 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_brk.py` | yes · 226,417 B | tracked | `899d3e7` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_brk_fixtures.py` | yes · 310,326 B | tracked | `899d3e7` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_census.py` | yes · 247,368 B | tracked | `a58bafc` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_census_fixtures.py` | yes · 177,058 B | tracked | `a58bafc` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_data.py` | yes · 172,077 B | tracked | `54cfd60` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_data_fixtures.py` | yes · 128,888 B | tracked | `54cfd60` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_file_registrations.py` | yes · 10,128 B | tracked | `371123f` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_lanes.py` | yes · 111,123 B | tracked | `899d3e7` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_lanes_fixtures.py` | yes · 183,213 B | tracked | `899d3e7` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_null.py` | yes · 60,840 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_null_fixtures.py` | yes · 77,414 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_panel.py` | yes · 154,338 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_panel_fixtures.py` | yes · 169,883 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_resume_fixtures.py` | yes · 333,729 B | tracked | `899d3e7` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_rf_fixtures.py` | yes · 63,856 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_score.py` | yes · 80,773 B | tracked | `ab7306a` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_score_fixtures.py` | yes · 56,891 B | tracked | `ab7306a` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_stamps.py` | yes · 68,491 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |
| `scripts/tierc10_stamps_fixtures.py` | yes · 63,246 B | tracked | `d19f857` | no | NOT PROTECTED — committed, not pushed · `--workflow` scope `scripts` | n/a — unsynced (`scripts/`) |

### 8.2 · (b) PROGRESS.json artifacts not already in (a) — 102 paths — REPORT-ONLY

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `research_outputs/tierc10/FIXTURES_RF.txt` | yes · 16,039 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/REGISTRATION_TEXTS.md` | yes · 128,673 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/BRK_MECHANICS.json` | yes · 39,487 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/BRK_READY.json` | yes · 37,442 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/BRK_READY.txt` | yes · 4,588 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/BRK_READY_BOOKS.json` | yes · 2,586,367 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/FIXTURES_BRK.txt` | yes · 123,567 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/FIXTURES_BRK_partial.txt` | yes · 6,524 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/brk/build_manifest.json` | yes · 61,227 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/CENSUS_R_DIGEST.md` | yes · 206,251 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/FIXTURES_CENSUS.txt` | yes · 78,000 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/R34_MANIFEST.json` | yes · 37,038 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_GRID.md` | yes · 7,780 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_GRID.parquet` | yes · 33,938 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_GRID_1d.md` | yes · 8,682 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_GRID_1d.parquet` | yes · 33,274 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_RESULT.json` | yes · 1,819 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/TUNING_RESULT_1d.json` | yes · 2,327 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/acceptance_head_to_head.parquet` | yes · 211,125 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/build_manifest.json` | yes · 119,342 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/coverage.parquet` | yes · 31,427 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/edge_fade.parquet` | yes · 1,600,173 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/height_toll.parquet` | yes · 87,770 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/height_toll_verdict.parquet` | yes · 88,248 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/hold_tally.parquet` | yes · 31,482 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/leans.parquet` | yes · 17,481 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/outcome_grid.parquet` | yes · 675,998 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/scale_grid.parquet` | yes · 41,788 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/FIXTURES_CENSUS.txt` | yes · 26,137 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/build_manifest.json` | yes · 12,979 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/coverage.parquet` | yes · 24,965 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/hold_tally.parquet` | yes · 22,266 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/leans.parquet` | yes · 16,802 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/outcome_grid.parquet` | yes · 39,316 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/scale_grid.parquet` | yes · 22,443 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/spring_overlap.parquet` | yes · 19,983 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/spring_overlap.parquet` | yes · 24,581 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/ARCHIVE_FORMS_PROBE.json` | yes · 12,074 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/ARCHIVE_VS_SNAPSHOT_AUDIT.json` | yes · 96,438 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/AS_OF_PIN.json` | yes · 604 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/CONTRACT_SPECS.json` | yes · 57,157 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/DATA_SPEND_AUDIT.json` | yes · 249,025 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/FETCH_LOG.jsonl` | yes · 18,716 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/FIXTURES_STAGE_D.txt` | yes · 62,244 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/FIXTURES_STAGE_D_OFFLINE.txt` | yes · 42,546 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/PRE_STATE.json` | yes · 16,918 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/REST_VS_SNAPSHOT_AUDIT.json` | yes · 37,474 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | yes · 405,715 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.md` | yes · 65,336 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/VENUE_PROBE.json` | yes · 10,787 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/WRITE_ONCE_SEAL.json` | yes · 2,049 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/data/fee_schedule.json` | yes · 23,925 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/lanes/BE_LATCH_CENSUS.json` | yes · 83,030 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/lanes/FIXTURES_LANES.txt` | yes · 61,474 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/lanes/FIXTURES_LANES_partial.txt` | no | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/lanes/build_manifest.json` | yes · 15,387 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/FIXTURES_NULL.txt` | yes · 215,260 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/build_manifest.json` | yes · 121,643 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/leans.parquet` | yes · 18,099 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/null_coverage.parquet` | yes · 66,954 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/null_grid.parquet` | yes · 5,354,777 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/null_summary.parquet` | yes · 1,328,255 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/FIXTURES_NULL.txt` | yes · 215,256 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/build_manifest.json` | yes · 121,644 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/leans.parquet` | yes · 18,099 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/null_coverage.parquet` | yes · 64,115 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/null_grid.parquet` | yes · 5,390,827 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/null_summary.parquet` | yes · 1,326,876 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/FIXTURES_PANEL.txt` | yes · 63,265 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/FIXTURES_PANEL_partial.txt` | no | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/build_manifest.json` | yes · 9,636 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/control_headline.parquet` | yes · 31,449 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/control_journal.parquet` | yes · 70,102 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/control_loao.parquet` | yes · 13,407 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/control_reference.parquet` | yes · 45,392 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/leans.parquet` | yes · 10,618 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/panel_admission.parquet` | yes · 22,840 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/panel_corridor.parquet` | yes · 13,673 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/panel/panel_funding.parquet` | yes · 15,266 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BE-1.json` | yes · 33,967 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BE-1.scored.json` | yes · 1,243 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BRK-I1.json` | yes · 30,858 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BRK-I1.scored.json` | yes · 958 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BRK-S1.json` | yes · 31,750 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-BRK-S1.scored.json` | yes · 967 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-GEN-1.json` | yes · 33,012 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-GEN-1.scored.json` | yes · 949 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-SPR-2.json` | yes · 34,966 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-SPR-2.scored.json` | yes · 1,294 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-TRG-2.json` | yes · 31,674 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/P-TRG-2.scored.json` | yes · 1,475 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/registrations/REGISTRY.jsonl` | yes · 1,594 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/FIXTURES_STAMPS.txt` | yes · 18,774 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/build_manifest.json` | yes · 8,543 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/control_entry_by_state.parquet` | yes · 20,316 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/control_v6_stamped.parquet` | yes · 272,398 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/control_v6_units.parquet` | yes · 72,766 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/funnel_tally.parquet` | yes · 11,778 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/leans.parquet` | yes · 10,632 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/stamp_coverage.parquet` | yes · 10,820 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/stamp_defs.parquet` | yes · 12,125 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/stamps/stamp_nulls.parquet` | yes · 11,840 B | ignored — `.gitignore:263` | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |

### 8.3 · (b) the cells directories, collapsed per directory — 4 rows — REPORT-ONLY

The spec's `census/cells` and `null/*/cells`, by the rule *the path up to its `cells` segment under census/ or null/*; the same shape also collapses `census/smoke/cells` — stated here, not hidden. Count + bytes are the PROGRESS-recorded files; the covered cell directories are listed in the JSON.

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `research_outputs/tierc10/census/cells` | yes · 51 dirs · 357 files · 96,700,245 B | ignored — `.gitignore:263` · 0 of 357 tracked | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/census/smoke/cells` | yes · 2 dirs · 14 files · 435,058 B | ignored — `.gitignore:263` · 0 of 14 tracked | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_only/cells` | yes · 51 dirs · 306 files · 371,194,083 B | ignored — `.gitignore:263` · 0 of 306 tracked | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |
| `research_outputs/tierc10/null/gaps_order/cells` | yes · 51 dirs · 306 files · 373,767,503 B | ignored — `.gitignore:263` · 0 of 306 tracked | not committed | no — nothing committed | NOT PROTECTED — local disk only · outside `--workflow` | n/a — unsynced (`research_outputs/`) |

### 8.4 · (c) the PLANNED build document — REPORT-ONLY

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` | no — PLANNED · sized as the assembled draft: 434,820 B (13 parts) | untracked — PLANNED, not yet on disk | not committed | no — nothing committed | NOT PROTECTED — PLANNED; `publish_exchange.publish()` commits and pushes `exchange/**` at CLOSE (CONVENTIONS §3.4) · `--workflow` scope `exchange` | 434,820 B · 2.718% of 16,000,000 B · **FLAGGED** — over the 64,000 B trip-wire; name it to the operator |

Sized as the assembled draft — 434,820 B from:

- `research_outputs/tierc10/BUILD_DRAFT.md` — 111,105 B
- `research_outputs/tierc10/close/FORWARD_STRIP.md` — 5,786 B
- `research_outputs/tierc10/close/LEDGER_APOLLO_APPEND.draft.md` — 22,653 B
- `research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.md` — 7,589 B
- `research_outputs/tierc10/close/P_TRG_2_SEEN_SHARE.md` — 5,677 B
- `research_outputs/tierc10/close/R0_ADDENDUM.md` — 16,734 B
- `research_outputs/tierc10/close/REGIME_PRIOR.md` — 19,419 B
- `research_outputs/tierc10/close/S0_VERDICTS.md` — 16,670 B
- `research_outputs/tierc10/close/S2_CENSUS_R.md` — 64,492 B
- `research_outputs/tierc10/close/S3_STAGE_D.md` — 59,087 B
- `research_outputs/tierc10/close/S5_FINDINGS_NOT_FIXED.md` — 84,441 B
- `research_outputs/tierc10/close/STAGE_LOG.md` — 12,329 B
- `research_outputs/tierc10/close/V6_CONTROL_HAIRCUT_TWIN.md` — 8,838 B
- this section (`research_outputs/tierc10/close/S8_DISPOSITION_BOX_COST.md`) — **not counted**: a file does not measure itself; the post-CLOSE regeneration sizes the filed document from disk.

An ESTIMATE, not a measurement: the parts are summed as they stand at run time; a part that replaces a draft placeholder is not netted out, and no fixture transcript is counted. The flag decision is what the operator needs from it.

### 8.5 · (d) the frozen snapshot — REPORT-ONLY

Stat only — no bar is opened. Marked *n/a — outside repo; NOT PROTECTED until the LaCie mirror* (the vault named in `research_outputs/tierc10/OPERATOR_RULINGS.md:65`).

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `/Users/luis/.cache/naiad/snapshots/tc10_20260921` | yes · 176 files · 856,462,999 B | n/a — outside repo | n/a — outside repo | n/a — outside repo | NOT PROTECTED until the LaCie mirror | n/a — outside repo |

### 8.6 · BOX COST — REPORT-ONLY

| box-bound path | bytes | % of box | trip-wire |
|---|---:|---:|---|
| `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` | 9,441 | 0.059% | under |
| `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` (PLANNED) | 434,820 | 2.718% | **FLAGGED** |
| **these rows, together** | 444,261 | 2.777% | — |

Not a row, named because the CLOSE touches it: `exchange/status/LEDGER_APOLLO.md` receives the LEDGER_APOLLO append. It is **174,090 B now**, already over the trip-wire — an append-only file that grew across it, which §3.2's named cost says the duty-at-creation never binds; `publish()` names it on every publish (advisory, never a refusal). The append is not drafted, so it is not sized.

The whole-bus figure (`exchange/**` and the tick set, against warn/refuse) is **not computed here**: computing it the way the guard does would mean importing `publish_exchange`, which this table never does. `publish()` prints it at CLOSE.

### 8.7 · Findings — reported, not fixed — REPORT-ONLY

- **BC-1 · NOTHING OF TC10 IS ON GITHUB.** 0 of 28 `tierc10` commits are in any remote-tracking ref; HEAD is 29 ahead of `origin/v12-v1-census`. Every (a) row reads NOT PROTECTED. Push permission is on file (`research_outputs/tierc10/OPERATOR_RULINGS.md:37`); the push is a CLOSE act, not this table's.
- **BC-2 · THE EVIDENCE TREE IS GIT-IGNORED.** 102 file rows and 983 collapsed cell files sit under an ignore pattern — local disk only, outside `--workflow` scope. No `--phase tierc10` archive is verified by this table.
- **BC-3 · A BOX-BOUND FILE WAS COMMITTED BY HAND.** `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` last committed in `c7b157d` ("tierc10(STEP Q + rulings recovery): the contract and the ope…") — not by `publish()` (`SUBJECT` = "exchange: auto-publish {date}", `scripts/publish_exchange.py:49`). `exchange/status/CONVENTIONS.md:415` asks that exchange files ride only the guard. It will ride the next branch push.
- **BC-4 · TRACKED, BUT OUTSIDE `--workflow` SCOPE:** 30 (a) paths — `.gitignore` 1, `analytics/` 1, `research_outputs/tierc10/` 28. Once pushed, GitHub is their only copy.
- **BC-5 · THE SNAPSHOT IS NOT PROTECTED** (yes · 176 files · 856,462,999 B): every TC10 number was computed on it; the vault is named at `research_outputs/tierc10/OPERATOR_RULINGS.md:65` and the mirror awaits the operator's destination word.
- **BC-6 · FLAGGED FOR NAMING:** `exchange/reports/BUILD_2026-09-21_TIERC10_UNSEEN_RANGES.md` — over the trip-wire; §3.2 asks it be named to the operator with its home.

### 8.8 · Volatile fields — named (F-DET) — REPORT-ONLY

Two whole runs on an unchanged tree are byte-identical (F-DET compares two builds inside a window where every input held still). These fields move without any change to this script — a commit, a push, a fetch, or another CLOSE section landing:

- **git-volatile:** `COMMITTED`, `PATH`, `PROTECTED BY`, `PUSHED`, `TRACKED`, `git.ahead`, `git.branch`, `git.head`, `git.upstream`, `git.upstream_tip`, `rows[].in_tierc10_commits`, `summary.tierc10_commits_pushed`
- **disk-volatile:** `BOX COST`, `EXISTS`, `not_in_table.ledger_apollo_bytes`, `planned.components`, `rows[].bytes`
