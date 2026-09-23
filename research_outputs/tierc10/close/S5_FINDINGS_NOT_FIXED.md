# TIER-C10 · CLOSE · §5 FINDINGS — REPORTED, NOT FIXED

> **REPORT-ONLY · Tier-E — findings harvested verbatim and measured at build time; nothing here is scored, no registration verdict is read, no bar is read, and nothing is fixed.**
>
> Every finding's status is 'REPORTED, NOT FIXED': it records what THIS build did (report, never fix); it does not claim the item is still open. Harvested texts are VERBATIM with their source path and field; measured values are recomputed on every run and never typed. Built by `scripts/tierc10_close_close_findings.py`; fixture transcript `FIXTURES_CLOSE_findings.txt` beside this file.

- **Contract of record:** `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a` (equal to PROGRESS.json `contract_of_record.sha256`, or the preamble would have HALTed)
- **Clause:** line 136 — `· findings-not-fixed · BOX-COST`
- **Clause:** line 110 — `governs, and the gap is filed as a finding.`
- **AS-OF OF RECORD:** 2026-09-21T16:00:00Z (PROGRESS.json `as_of_of_record`)
- **The contract's PANEL PIN gap ('the gap is filed as a finding'):** filed here as `FN-RUL-L1-1`; OPERATOR_RULINGS.md settles it at its `## R8` heading (line 101).
- **Order of the two 'Still blocked' lists:** list 1 is headed at line 69, BEFORE `# RULINGS OF 2026-09-22 (R7–R10)` at line 82; list 2 is headed at line 139. List 1 is printed because the spec harvests both; where R7–R10 settled an item, list 2 is the later word.
- **Harvested texts that record their own repair:** `FN-PROG-01-B8` — read those beside the items they repair.
- **Owners assigned by the DEFAULT RULE (no declared rule matched):** `FN-PROG-15-B1`, `FN-PROG-15-N1`, `FN-PROG-15-N2`.

## 0 · Inputs, read-only

*REPORT-ONLY · Tier-E — every file this build reads; F-FN-READONLY proves none changed.*

| input | bytes | sha256 |
|---|---:|---|
| `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` | 9441 | `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a` |
| `research_outputs/tierc10/BUILD_DRAFT.md` | 111105 | `244ad5a46a4f73c522361990638499206c9ef3c341d436e2aa67bdd898791149` |
| `research_outputs/tierc10/OPERATOR_RULINGS.md` | 8696 | `a0a08f8761ce9eab678d42d609d7e6563e749c07a6c33b7b17f9a5c4f31ca907` |
| `research_outputs/tierc10/PROGRESS.json` | 287206 | `1789f57e40f13e4930cd778e7b604c990dc16db4e6c90c6577352378913ebb3f` |
| `research_outputs/tierc10/REGISTRATION_PLAN.md` | 7242 | `cbb85a214de536598d7e06575b32eac6e266b051cf279f244988245829b2a5e8` |
| `research_outputs/tierc10/REGISTRATION_TEXTS.json` | 178729 | `3afce077146807127072ae68f9c816e0263505aa625cf1610763ea37eb91ca94` |
| `research_outputs/tierc10/REGISTRATION_TEXTS.md` | 128673 | `eef76eedda56aef32da1cb5656f5c0a93ffb878f0ad09fa37898efe0a3da40b1` |
| `research_outputs/tierc10/census/leans.parquet` | 17481 | `a93dc1dbad3c7593c8257f378e60b44d4a9b186565eae68e639d26e9804a0ab7` |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | 405715 | `de2e8663bbf101dfb46ad9f77a4969ca73648e78373646c0d17b81b9f9a87421` |
| `research_outputs/tierc10/panel/leans.parquet` | 10618 | `faf0c986b232e150d7dfa375ba2400b185eddee3178fe1c2a6371af0ac7d2920` |
| `research_outputs/tierc10/scores/DRYRUN.json` | 77280 | `13958abb0c75ee2cfaa8bf2df9d0f7569bbb286d85fa49a32339d8b90c15672c` |
| `research_outputs/tierc10/scores/FAMILY.json` | 113715 | `aa0e8c496fd6b883a3c01947047c4845eb72935ca17368cffee9c8593a7bc4a2` |
| `research_outputs/tierc10/scores/P-BE-1.rows.json` | 84044 | `b40af065177695e36e755d183ef74e7328d77eb799ed3abbb668ff7d69b6b678` |
| `research_outputs/tierc10/scores/P-BRK-I1.rows.json` | 111150 | `f3ae88d0be366f127bacfe0f8092cdef07d17559ea3b3db6d6c1edd6c306111a` |
| `research_outputs/tierc10/scores/P-BRK-S1.rows.json` | 118556 | `994bcaa69906aae8a1659d953c0984da636cb496808dd17ab91ddf3ea3c33ff0` |
| `research_outputs/tierc10/scores/P-GEN-1.rows.json` | 123091 | `047097ec5aeefbe8aa63cf2b1a677015540497a41e43b0152e609426a2baf87d` |
| `research_outputs/tierc10/scores/P-SPR-2.rows.json` | 111310 | `febff33a1ad91e3663cb75fc7db54fe7901d7a8493503e3e6e6aa065da6bc23e` |
| `research_outputs/tierc10/scores/P-TRG-2.rows.json` | 102709 | `9fa07a0fa1b832ef7a1012a796cfd7fdd73ab2e1275d4faa4340666493c340c8` |
| `research_outputs/tierc10/stamps/leans.parquet` | 10632 | `91ee065223f58d9197396abfeb7444b07de2aac3628ae6d9a0479bcd425e6c67` |

## 1 · Counts and index

*REPORT-ONLY · Tier-E — counts of this file's findings by class and owner.*

| class | operator | executor | total |
|---|---:|---:|---:|
| HARVESTED | 30 | 17 | 47 |
| MEASURED | 2 | 4 | 6 |
| LEAN | 0 | 31 | 31 |
| **all** | **32** | **52** | **84** |

*REPORT-ONLY · Tier-E — the index: one row per finding, in document order.*

| id | class | owner | source | field |
|---|---|---|---|---|
| `FN-PROG-01-B1` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[0]` |
| `FN-PROG-01-B2` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[1]` |
| `FN-PROG-01-B3` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[2]` |
| `FN-PROG-01-B4` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[3]` |
| `FN-PROG-01-B5` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[4]` |
| `FN-PROG-01-B6` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[5]` |
| `FN-PROG-01-B7` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[6]` |
| `FN-PROG-01-B8` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[1].blockers[7]` |
| `FN-PROG-07-N1` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[7].notes[0]` |
| `FN-PROG-08-N1` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[8].notes[0]` |
| `FN-PROG-10-B1` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[10].blockers[0]` |
| `FN-PROG-13-N1` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[13].notes[0]` |
| `FN-PROG-13-N2` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[13].notes[1]` |
| `FN-PROG-14-N1` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[14].notes[0]` |
| `FN-PROG-14-N2` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[14].notes[1]` |
| `FN-PROG-15-B1` | HARVESTED | operator | `research_outputs/tierc10/PROGRESS.json` | `stages[15].blockers[0]` |
| `FN-PROG-15-N1` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[15].notes[0]` |
| `FN-PROG-15-N2` | HARVESTED | executor | `research_outputs/tierc10/PROGRESS.json` | `stages[15].notes[1]` |
| `FN-RUL-L1-1` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 71-71` |
| `FN-RUL-L1-2` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 72-72` |
| `FN-RUL-L1-3` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 73-74` |
| `FN-RUL-L1-4` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 75-76` |
| `FN-RUL-L1-5` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 77-77` |
| `FN-RUL-L1-6` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 78-78` |
| `FN-RUL-L2-1` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 141-144` |
| `FN-RUL-L2-2` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 145-147` |
| `FN-RUL-L2-3` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 148-149` |
| `FN-RUL-L2-4` | HARVESTED | operator | `research_outputs/tierc10/OPERATOR_RULINGS.md` | `lines 150-151` |
| `FN-SDM-ORN-1` | HARVESTED | operator | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `operator_rulings_needed[0]` |
| `FN-SDM-ORN-2` | HARVESTED | operator | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `operator_rulings_needed[1]` |
| `FN-SDM-ORN-3` | HARVESTED | operator | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `operator_rulings_needed[2]` |
| `FN-SDM-ORN-4` | HARVESTED | operator | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `operator_rulings_needed[3]` |
| `FN-SDM-HAZ-funding_files_with_a_print_stamped_after_the_as_of_close` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.funding_files_with_a_print_stamped_after_the_as_of_close` |
| `FN-SDM-HAZ-funding_floor_hour_equals_nearest_hour_on_every_file` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.funding_floor_hour_equals_nearest_hour_on_every_file` |
| `FN-SDM-HAZ-funding_law` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.funding_law` |
| `FN-SDM-HAZ-funding_ms_past_hour_max_over_panel` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.funding_ms_past_hour_max_over_panel` |
| `FN-SDM-HAZ-kline_files_holding_rows_after_as_of` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.kline_files_holding_rows_after_as_of` |
| `FN-SDM-HAZ-kline_law` | HARVESTED | executor | `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | `as_of_hazards.kline_law` |
| `FN-FAM-HALT-P-BE-1` | HARVESTED | operator | `research_outputs/tierc10/scores/FAMILY.json` | `scored_slots_halted.P-BE-1` |
| `FN-TOLL-DRYRUN-1` | HARVESTED | operator | `research_outputs/tierc10/scores/DRYRUN.json` | `beside_registration.P-BRK-I1.brk_sealed_row.toll_accounting_status` |
| `FN-TOLL-DRYRUN-2` | HARVESTED | operator | `research_outputs/tierc10/scores/DRYRUN.json` | `beside_registration.P-BRK-S1.brk_sealed_row.toll_accounting_status` |
| `FN-TOLL-P-BRK-I1-1` | HARVESTED | operator | `research_outputs/tierc10/scores/P-BRK-I1.rows.json` | `beside_registration.brk_sealed_row.toll_accounting_status` |
| `FN-TOLL-P-BRK-I1-2` | HARVESTED | operator | `research_outputs/tierc10/scores/P-BRK-I1.rows.json` | `rows[0].beside.brk_sealed_row.toll_accounting_status` |
| `FN-TOLL-P-BRK-S1-1` | HARVESTED | operator | `research_outputs/tierc10/scores/P-BRK-S1.rows.json` | `beside_registration.brk_sealed_row.toll_accounting_status` |
| `FN-TOLL-P-BRK-S1-2` | HARVESTED | operator | `research_outputs/tierc10/scores/P-BRK-S1.rows.json` | `rows[0].beside.brk_sealed_row.toll_accounting_status` |
| `FN-PLAN-DRAFTERR` | HARVESTED | operator | `research_outputs/tierc10/REGISTRATION_PLAN.md` | `lines 95-98` |
| `FN-DRAFT-SMOKE` | HARVESTED | operator | `research_outputs/tierc10/BUILD_DRAFT.md` | `lines 481-487` |
| `FN-M-i` | MEASURED | executor | `research_outputs/tierc10/REGISTRATION_TEXTS.json, research_outputs/tierc10/REGISTRATION_TEXTS.md` | `measured.i` |
| `FN-M-ii` | MEASURED | operator | `research_outputs/tierc10/scores` | `measured.ii` |
| `FN-M-iii` | MEASURED | operator | `analytics` | `measured.iii` |
| `FN-M-iv` | MEASURED | executor | `research_outputs/tierc10/PROGRESS.json, .git` | `measured.iv` |
| `FN-M-v` | MEASURED | executor | `.git` | `measured.v` |
| `FN-M-vi` | MEASURED | executor | `research_outputs/tierc10/PROGRESS.json, research_outputs/tierc10/BUILD_DRAFT.md` | `measured.vi` |
| `LEAN-CENSUS-00` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 0 · column text` |
| `LEAN-CENSUS-01` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 1 · column text` |
| `LEAN-CENSUS-02` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 2 · column text` |
| `LEAN-CENSUS-03` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 3 · column text` |
| `LEAN-CENSUS-04` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 4 · column text` |
| `LEAN-CENSUS-05` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 5 · column text` |
| `LEAN-CENSUS-06` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 6 · column text` |
| `LEAN-CENSUS-07` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 7 · column text` |
| `LEAN-CENSUS-08` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 8 · column text` |
| `LEAN-CENSUS-09` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 9 · column text` |
| `LEAN-CENSUS-10` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 10 · column text` |
| `LEAN-CENSUS-11` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 11 · column text` |
| `LEAN-CENSUS-12` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 12 · column text` |
| `LEAN-CENSUS-13` | LEAN | executor | `research_outputs/tierc10/census/leans.parquet` | `row 13 · column text` |
| `LEAN-PANEL-L1` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 0 · column text` |
| `LEAN-PANEL-L2` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 1 · column text` |
| `LEAN-PANEL-L3` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 2 · column text` |
| `LEAN-PANEL-L4` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 3 · column text` |
| `LEAN-PANEL-L5` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 4 · column text` |
| `LEAN-PANEL-L6` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 5 · column text` |
| `LEAN-PANEL-L7` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 6 · column text` |
| `LEAN-PANEL-L8` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 7 · column text` |
| `LEAN-PANEL-panel-verdict` | LEAN | executor | `research_outputs/tierc10/panel/leans.parquet` | `row 8 · column text` |
| `LEAN-STAMPS-1` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 0 · column lean` |
| `LEAN-STAMPS-2` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 1 · column lean` |
| `LEAN-STAMPS-3` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 2 · column lean` |
| `LEAN-STAMPS-4` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 3 · column lean` |
| `LEAN-STAMPS-5` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 4 · column lean` |
| `LEAN-STAMPS-6` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 5 · column lean` |
| `LEAN-STAMPS-7` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 6 · column lean` |
| `LEAN-STAMPS-8` | LEAN | executor | `research_outputs/tierc10/stamps/leans.parquet` | `row 7 · column lean` |

## 2 · Measured at build time — (i) to (vi)

*REPORT-ONLY · Tier-E — recomputed on every run, never typed; F-FN-MEASURED re-derives each by an independent path. (iv) and (v) are git-volatile and are printed in marked blocks.*

| # | measure | value | owner |
|---|---|---|---|
| (i) | REGISTRATION_TEXTS.json texts found verbatim in REGISTRATION_TEXTS.md | verbatim 0 / total 6 | executor |
| (ii) | arms where beside.haircut_twin.twin_expectancy_r > tc_expectancy_r | twin_above_tc 8 / arms_with_twin 20 / arms_total 21 | operator |
| (iii) | os.path.exists for analytics/rangefinder.py and analytics/rangefinder_census.py | `analytics/rangefinder.py` False; `analytics/rangefinder_census.py` True | operator |
| (iv) | PROGRESS.json head vs `git rev-parse HEAD` | git-volatile — see §2.iv | executor |
| (v) | `git worktree list` HEADs vs the tierc10 commits reachable from HEAD | git-volatile — see §2.v | executor |
| (vi) | PROGRESS.json stages absent from BUILD_DRAFT.md §1 | absent 16 / stages 16 | executor |

### 2.i

*Method:* Python `text in md` over every <reg>.text of the JSON.

#### FN-M-i

- **MEASURED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/REGISTRATION_TEXTS.json`, `research_outputs/tierc10/REGISTRATION_TEXTS.md` · `measured.i` · text form: rendered from measured values recomputed this run
- owner basis: `research_outputs/tierc10/REGISTRATION_TEXTS.md` — "These are the exact bytes" — *the document asserts byte-identity with the filing; re-rendering it is the executor's*

~~~text
0 of 6 REGISTRATION_TEXTS.json texts are found verbatim in REGISTRATION_TEXTS.md. P-GEN-1: NOT verbatim — only its first 274 of 26,111 characters occur in the .md; P-SPR-2: NOT verbatim — only its first 129 of 32,179 characters occur in the .md; P-BE-1: NOT verbatim — only its first 95 of 30,811 characters occur in the .md; P-TRG-2: NOT verbatim — only its first 1,373 of 23,317 characters occur in the .md; P-BRK-I1: NOT verbatim — only its first 418 of 28,082 characters occur in the .md; P-BRK-S1: NOT verbatim — only its first 772 of 29,113 characters occur in the .md.
~~~

### 2.ii

*Method:* rows[].beside.haircut_twin of every scores/P-*.rows.json; float compare.

#### FN-M-ii

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores` · `measured.ii` · text form: rendered from measured values recomputed this run
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "the slippage-twin question named for the autopsy" — *the contract routes the slippage-twin question to the autopsy*

~~~text
8 of 20 arms that carry a haircut twin show beside.haircut_twin.twin_expectancy_r > tc_expectancy_r: P-BE-1 rows[1] 'be-floor-1R vs card-v6 (CLASSIC5, tuning) [Tier-E]': tc -0.0250 R, twin -0.0002 R; P-BE-1 rows[3] 'be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) [Tier-E]': tc +0.1889 R, twin +0.1979 R; P-BRK-I1 rows[0] 'CLASSIC5-memory-line': tc +0.7183 R, twin +0.8946 R; P-BRK-I1 rows[1] 'CLASSIC5-tierE-band': tc +0.3518 R, twin +0.5100 R; P-BRK-I1 rows[2] 'PANEL17-tierE-memory-line': tc +0.4219 R, twin +0.5172 R; P-TRG-2 rows[0] 'trg-9/12 vs card v6 · CLASSIC5 · full': tc +0.4664 R, twin +0.4756 R; P-TRG-2 rows[1] 'trg-9/12 vs zero · CLASSIC5 · full': tc +0.4664 R, twin +0.4756 R; P-TRG-2 rows[2] 'trg-9/12 vs card v6 · CLASSIC5 · tuning era': tc +0.1777 R, twin +0.1989 R. 1 of 21 arms carry no haircut twin: P-BE-1 rows[0] 'be-floor-1R vs card-v6 (CLASSIC5, full)'.
~~~

*REPORT-ONLY · Tier-E — the haircut-twin arms; values read from each file's `rows[n].beside.haircut_twin`; no verdict field is read.*

| file | row | arm | tc_expectancy_r | twin_expectancy_r | twin − tc | twin > tc |
|---|---:|---|---:|---:|---:|---|
| `P-BE-1.rows.json` | 1 | be-floor-1R vs card-v6 (CLASSIC5, tuning) [Tier-E] | -0.0250 | -0.0002 | +0.0248 | True |
| `P-BE-1.rows.json` | 2 | be-floor-1R vs card-v6 (CLASSIC5, holdout) [Tier-E] | +0.5111 | +0.4937 | -0.0174 | False |
| `P-BE-1.rows.json` | 3 | be-floor-2R sensitivity vs card-v6 (CLASSIC5, full) [Tier-E] | +0.1889 | +0.1979 | +0.0090 | True |
| `P-BRK-I1.rows.json` | 0 | CLASSIC5-memory-line | +0.7183 | +0.8946 | +0.1763 | True |
| `P-BRK-I1.rows.json` | 1 | CLASSIC5-tierE-band | +0.3518 | +0.5100 | +0.1583 | True |
| `P-BRK-I1.rows.json` | 2 | PANEL17-tierE-memory-line | +0.4219 | +0.5172 | +0.0953 | True |
| `P-BRK-S1.rows.json` | 0 | P-BRK-S1 vs zero | -0.2111 | -0.3728 | -0.1617 | False |
| `P-BRK-S1.rows.json` | 1 | P-BRK-S1 17-asset view | -0.1702 | -0.4277 | -0.2575 | False |
| `P-BRK-S1.rows.json` | 2 | P-BRK-S1 memory-line anchor | -0.1989 | -0.3253 | -0.1264 | False |
| `P-GEN-1.rows.json` | 0 | unseen12-card-v6 | +0.0998 | +0.0846 | -0.0152 | False |
| `P-GEN-1.rows.json` | 1 | panel17-card-v6 | +0.1446 | +0.1391 | -0.0055 | False |
| `P-GEN-1.rows.json` | 2 | never-touched-card-v6 | -0.2328 | -0.2659 | -0.0331 | False |
| `P-SPR-2.rows.json` | 0 | standalone vs zero · full corridor | -0.0059 | -0.0243 | -0.0184 | False |
| `P-SPR-2.rows.json` | 1 | standalone vs zero · tuning era | -0.1490 | -0.1690 | -0.0200 | False |
| `P-SPR-2.rows.json` | 2 | standalone vs zero · holdout era | +0.2400 | +0.2243 | -0.0157 | False |
| `P-SPR-2.rows.json` | 3 | union with card v6 vs card v6 | +0.0976 | +0.0907 | -0.0069 | False |
| `P-TRG-2.rows.json` | 0 | trg-9/12 vs card v6 · CLASSIC5 · full | +0.4664 | +0.4756 | +0.0092 | True |
| `P-TRG-2.rows.json` | 1 | trg-9/12 vs zero · CLASSIC5 · full | +0.4664 | +0.4756 | +0.0092 | True |
| `P-TRG-2.rows.json` | 2 | trg-9/12 vs card v6 · CLASSIC5 · tuning era | +0.1777 | +0.1989 | +0.0213 | True |
| `P-TRG-2.rows.json` | 3 | trg-9/12 vs card v6 · CLASSIC5 · holdout era | +1.0439 | +1.0289 | -0.0151 | False |
| `P-BE-1.rows.json` | 0 | be-floor-1R vs card-v6 (CLASSIC5, full) | — | — | — | no twin on the row |

### 2.iii

*Method:* os.path.exists.

#### FN-M-iii

- **MEASURED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `analytics` · `measured.iii` · text form: rendered from measured values recomputed this run
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "twin module-ized as analytics/rangefinder.py" — *the contract names analytics/rangefinder.py; the executor's lean L3 names analytics/rangefinder_census.py; accepting the lean or ordering the rename is the operator's*

~~~text
os.path.exists(analytics/rangefinder.py) = False; os.path.exists(analytics/rangefinder_census.py) = True.
~~~

### 2.iv

<!-- git-volatile:begin -->
*Method:* git rev-parse HEAD; git merge-base --is-ancestor; git log ph..HEAD.

#### FN-M-iv

- **MEASURED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/PROGRESS.json`, `.git` · `measured.iv` · text form: rendered from measured values recomputed this run
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "after EVERY stage: commit + update research_outputs/tierc10/PROGRESS.json" — *LAW 6 puts the ledger update on the executor*

~~~text
PROGRESS.json head 6b15def66f73e3fcd05b6dc5a0516fcd2ac1d1c7 vs git rev-parse HEAD 22a1c065a0a7799391ed0cc997c0f98a0b19994d: equal = False; the ledger's head is an ancestor of HEAD = True; commits on HEAD after the ledger's head = 23.
~~~

*REPORT-ONLY · Tier-E — commits on HEAD after the ledger's recorded head.*

| sha | subject |
|---|---|
| `22a1c06` | exchange: auto-publish 2026-09-23 |
| `fea73bd` | exchange: auto-publish 2026-09-23 |
| `4c896a3` | tierc10(F-C10-RESUME): transcript of record after CLOSE prep — 9 GREEN, 0 RED |
| `d575a7d` | tierc10(CLOSE prep): verdicts verified under their own texts, the missing report-only items built, the build doc drafted |
| `ff74a90` | or1: step F — the edition word follows the verb and the Buenos Aires hour (A-OR1-1 vii) |
| `3d55988` | or1: step D — range module to scripts/rangefinder_core.py; range records to tape_ranges/; F-BR-14 re-pointed (A-OR1-1 iv, v) |
| `2416a15` | tierc10(F-C10-RESUME): transcript of record after B-5M — 9 GREEN, 0 RED |
| `08a6fce` | tierc10(B-5M): P-BRK-S1 scored, the family finished at m = 6 — P-TRG-2 alone clears all three clauses |
| `dc30015` | tierc10(F-C10-RESUME): transcript of record after B-CORE — 9 GREEN, 0 RED |
| `ab7306a` | tierc10(B-CORE): five registrations scored against the pinned dry-run — one SUPPORTED on (a), one prescribed HALT |
| `b29774e` | tierc10(B-CORE): the reviewed dry-run, pinned BEFORE any score — 21 arms, one prescribed HALT |
| `be157e9` | tierc10(F-C10-RESUME): transcript of record after the Stage B mech ledger — 9 GREEN, 0 RED |
| `899d3e7` | tierc10(STAGE B mech): F-C10-HOLD real, F-C10-BE NOT RUN per P-BE-1 §9, the scoring driver |
| `371123f` | tierc10(STAGE B): the six registrations are FILED — text before result |
| `74d9b39` | tierc10(F-C10-RESUME): transcript of record — 9 GREEN, 0 RED |
| `fa205c8` | tierc10(F-C10-RESUME): leg 1 accuses instead of raising when a stage records no artifact |
| `83f5e29` | tierc10(F-C10-RESUME): transcript of record after the re-pin |
| `41a5070` | tierc10(F-C10-RESUME): re-pin onto the ledger that drops the circular self-record |
| `2e92972` | tierc10(LAW 6): the resume stage records no artifact sha — the self-reference does not converge |
| `ad34e6e` | tierc10(F-C10-RESUME): re-file the transcript after the re-pin — 9 GREEN, 0 RED |
| `54c519d` | tierc10(F-C10-RESUME): move the anchor to the post-repair ledger, deliberately |
| `2e4d959` | tierc10(LAW 2): restore the quarantined kill-partial's ledger record |
| `3453c87` | tierc10(LAW 6): the ledger after the repair phase, rebuilt from the committed R0 base |

<!-- git-volatile:end -->

### 2.v

<!-- git-volatile:begin -->
*Method:* git worktree list --porcelain; tierc10 commits = commits reachable from HEAD whose subject starts with 'tierc10'; per worktree HEAD, |that set ∩ git rev-list <head>|.

#### FN-M-v

- **MEASURED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `.git` · `measured.v` · text form: rendered from measured values recomputed this run
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "Read-only worktrees for review" — *the contract's worktree attestation is the executor's*

~~~text
28 worktree(s) besides the main one; 28 of them reach 0 of the 30 tierc10 commits reachable from HEAD, 0 reach all of them. Their HEADs: a6da1b97e95c × 28. The main working tree reaches 30 of 30.
~~~

*REPORT-ONLY · Tier-E — every worktree `git worktree list` names.*

| path | head | branch | tierc10 commits reachable |
|---|---|---|---:|
| `.` | `22a1c065a0a7` | `v12-v1-census` | 30 |
| `.claude/worktrees/wf_8995cf0d-ab5-1` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-1` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-10` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-10` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-11` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-11` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-12` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-12` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-13` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-13` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-15` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-15` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-16` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-16` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-17` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-17` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-18` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-18` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-19` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-19` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-2` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-2` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-20` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-20` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-22` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-22` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-23` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-23` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-24` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-24` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-25` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-25` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-26` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-26` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-27` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-27` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-28` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-28` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-29` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-29` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-3` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-3` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-30` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-30` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-4` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-4` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-5` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-5` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-6` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-6` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-7` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-7` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-8` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-8` | 0 |
| `.claude/worktrees/wf_8995cf0d-ab5-9` | `a6da1b97e95c` | `worktree-wf_8995cf0d-ab5-9` | 0 |

<!-- git-volatile:end -->

### 2.vi

*Method:* a stage is PRESENT iff its PROGRESS `stage` string occurs inside the bold label that opens a §1 bullet ('- **label**'); §1 = the text after the '## 1 · STAGE LOG' heading up to the next '## ' heading.

#### FN-M-vi

- **MEASURED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/PROGRESS.json`, `research_outputs/tierc10/BUILD_DRAFT.md` · `measured.vi` · text form: rendered from measured values recomputed this run
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "+ one line to the draft" — *LAW 6 puts the draft line on the executor*

~~~text
16 of 16 PROGRESS.json stages have no stage line in BUILD_DRAFT.md §1: STEP 0, D-CORE, CENSUS-R{4h,1d}, NULL/gaps-only, NULL/gaps+order, A (stamps), PANEL/gate, LANES (B mech), BRK (B mech), F-C10-RESUME, D-5M, CENSUS-R{5m}, B-REG (the six filed), B-CORE, B-5M, CLOSE. §1's bullet labels are: .
~~~

## 3 · Harvested — verbatim, by source

### 3.1 · PROGRESS.json — every stages[].blockers and stages[].notes string

#### FN-PROG-01-B1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "RESUME CLAUSE F-D-4 (TWO-TOKEN TRAP)" — *a Stage D report clause the executor builds*

~~~text
RESUME CLAUSE F-D-4 (TWO-TOKEN TRAP) — no artifact, no fixture leg. LEGS[] in scripts/tierc10_data_fixtures.py has no F-D-4 entry. STAGE_D_MANIFEST.json/.md contain zero occurrences of 'two-token', 'first_valid', 'hard_floor', 'hard-floor', 'continuity', 'price_continuity', 'predates', 'intended'. Verdict PARTIAL-in-substance / ABSENT-as-artifact: listing date + source ARE printed per file row (137 'listing' occurrences; every kline row carries listing + source + publication) and PUMPBTCUSDT IS rejected by name in venue_rejections with LEAN D-d, but the hard-floor check, the price-continuity-at-the-floor check and the F-D-4 table itself do not exist. The contract demands it (resume paste line 135: 'Stage D manifest incl. the F-D-4 / F-D-5 tables'); research_outputs/tierc10/BUILD_DRAFT.md:86 carries only the placeholder '*Including the F-D-4 two-token-trap table and the F-D-5 data-spend audit.*'
~~~

#### FN-PROG-01-B2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[1]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "RESUME CLAUSE F-D-5 (DATA-SPEND AUDIT)" — *a Stage D report clause the executor builds*

~~~text
RESUME CLAUSE F-D-5 (DATA-SPEND AUDIT) — ABSENT outright. No fixture leg in LEGS[]. Zero occurrences of 'never-touched', 'display-only', 'data-spend', 'spend' in STAGE_D_MANIFEST.json and .md. Nothing under research_outputs/tierc10/ carries the classification except the BUILD_DRAFT.md placeholder line. No {never-touched / display-only / scored} table exists per asset for the 17, so PUMPFUN and HYPE are neither read nor assumed — they are simply unclassified.
~~~

#### FN-PROG-01-B3

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[2]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "RESUME CLAUSE COSTS HAIRCUT TWIN" — *a Stage D report clause the executor builds*

~~~text
RESUME CLAUSE COSTS HAIRCUT TWIN (tiered slippage per side, A/B/C = 2/5/10 bps) — ABSENT from Stage D. fee_schedule.json carries zero occurrences of 'slip', 'Slip', 'SLIP', 'haircut', 'Haircut', 'multiplier'; its per-asset key set is exactly ['asset','funding_interval_hours_observed_modal','funding_interval_hours_observed_tail','funding_spacing_hours_histogram','kind','round_trip_bps_used','source','stem','symbol','taker_bps_side_used','venue','venue_note'] with a FLAT taker_bps_side_used=5.0 and round_trip_bps_used=10.0 for all 17 assets and no slippage column at all. The tier concept exists elsewhere in the estate but for a DIFFERENT roster: Naiad_Phase0_Charter.md:114 reads 'tier A (BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE, FARTCOIN, LIT) 10 bps' and scripts/v3_scorer.py:309 repeats '2/5/10 bps' as a modeled-note string. The resume paste's TC10 assignment (tier B += LTC BNB DOGE UNI SUI XMR; tier C = ENA PUMPFUN HYPE MNT PEPE BONK) appears nowhere on disk outside the contract text itself.
~~~

#### FN-PROG-01-B4

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[3]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "RESUME CLAUSE CONTRACT MULTIPLIERS" — *a Stage D report clause the executor builds*

~~~text
RESUME CLAUSE CONTRACT MULTIPLIERS (1000PEPE, 1000BONK) printed and normalized — ABSENT. Zero occurrences of 'multiplier', 'contractSize', 'contract_size', 'quantity_multiplier', 'notional', 'per_unit' in STAGE_D_MANIFEST.json; zero of 'multiplier'/'normali' in STAGE_D_MANIFEST.md; zero of 'multiplier'/'contractSize'/'quantityPrecision'/'filters' in VENUE_PROBE.json (the probe never captured the field). The manifest prints the symbols (venues rows: asset PEPE -> symbol 1000PEPEUSDT; asset BONK -> symbol 1000BONKUSDT) and their prices, but never states that the contract is per 1000 tokens and never normalizes. Any downstream cross-asset price or height comparison will be off by 1000x for these two.
~~~

#### FN-PROG-01-B5

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[4]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "pending an operator ruling that does not yet exist" — *the text names an operator ruling as the dependency*

~~~text
F-D-1 STAYS RED pending an operator ruling that does not yet exist. Re-run NOW it is RED (exit 1). Operator ruling R5 of 2026-09-21 ('The USDT pair, either on Binance or Bybit', recovered verbatim in research_outputs/tierc10/OPERATOR_RULINGS.md) does not distinguish the venue's REST API from its BULK ARCHIVE, which is the actual disagreement. This is the designed red, not a break — but it is an open operator dependency on the stage.
~~~

#### FN-PROG-01-B6

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[5]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "CARRIED AS-OF HAZARD" — *a load-path trap for executor code, not a question for the operator*

~~~text
CARRIED AS-OF HAZARD: 14 of the 102 kline files hold rows past the pin — every 5m file except PUMPUSDT, MNTUSDT_BYBIT and SUIUSDT, 6 rows each (opens 16:00, 16:05, 16:10, 16:15, 16:20, 16:25Z). Item 3's literal law ('no kline file holds a row after 1790006400000') is FALSE at file level. It holds at loader level. The manifest discloses this itself (as_of_hazards.kline_law, LEAN D-e) and warns that tierc2_baseline.load_klines reads the WHOLE file, so any TC10 lane loading through it instead of tierc10_data.load_asof reads past the pin. Not repairable in this stage (no deletion primitive, prefixes are never rewritten) but it is a live trap for Stage A and downstream.
~~~

#### FN-PROG-01-B7

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL) · the same list's REPAIRED line: `FN-PROG-01-B8`
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[6]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "TRANSCRIPT BYTE-REPRODUCIBILITY IS DISPROVEN" — *a property of the executor's fixture transcripts against a backfilling venue*

~~~text
TRANSCRIPT BYTE-REPRODUCIBILITY IS DISPROVEN, and could not be tested directly. FIXTURES_STAGE_D.txt is only rewritten by a FULL online run with no leg arguments; --offline writes FIXTURES_STAGE_D_OFFLINE.txt instead and a named-leg run writes nothing (main() guards on `if not want`). So my two runs left it byte-identical (69a22de8... before and after) without exercising the builders' claim. But F-D-1b's own census moved between the filed run and mine — {'archive-only': 74, 'both': 215, 'rest': 28, 'rest-only': 105} became {'archive-only': 74, 'both': 223, 'rest': 20, 'rest-only': 105} — so 8 bars the venue's bulk archive did not publish on 2026-09-21 it does publish on 2026-09-22. A full re-run's transcript CANNOT be byte-identical to the filed one, because the venue's archive backfills.
~~~

#### FN-PROG-01-B8

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **D-CORE** (PARTIAL)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[1].blockers[7]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "What remains is F-D-1's operator ruling: REST or ARCHIVE." — *the text names the operator's REST-or-ARCHIVE word as what remains*

~~~text
REPAIRED 2026-09-22: F-D-4, F-D-5, the tiered haircut twin and contract multipliers are built and filed; those four clauses no longer block. What remains is F-D-1's operator ruling: REST or ARCHIVE.
~~~

#### FN-PROG-07-N1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **LANES (B mech)** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[7].notes[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "Not a defect and not an operator question" — *the text itself rules the operator out; disclosure of prescribed mechanics*

~~~text
F-C10-BE is NOT RUN — PRESCRIBED by P-BE-1's filed §9 ('if P-BE-1's filed book contains no tie and no 4h/5m mismatch latch bar, the leg must report NOT RUN with that reason. It must NOT substitute a synthetic bar or relabel a dip_first case to reach three.'). BE_LATCH_CENSUS.json (outcome-free) on A1: 200 campaigns, 103 latch bars — dip_before 36, dip_after 0, print_no_dip 67, tie 0, mismatch 0; journal == module == hand walk 103/103. Not a defect and not an operator question: the text decided it before the look.
~~~

#### FN-PROG-08-N1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **BRK (B mech)** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[8].notes[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the text names the operator as the one who settles it*

~~~text
OPEN, for the operator: P-BRK-S1's 'NET OF MEASURED 5m TOLL' is carried as a PRINT beside the book (TOLL_ACCOUNTING on every row), not as a deduction from net_r. The toll is a census-measured median in ATR units and net_r is R-denominated, so deducting one from the other is a unit question, not a code change.
~~~

#### FN-PROG-10-B1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **D-5M** (PARTIAL)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[10].blockers[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "pending the operator's REST-or-ARCHIVE word" — *the text names the operator's word as the dependency*

~~~text
F-D-1 (online) stays RED pending the operator's REST-or-ARCHIVE word (R5's narrower question); one of its three differing bars is XMRUSDT 5m. Does NOT reach B-5M: P-BRK-S1 pins substrate tc10_20260921.
~~~

#### FN-PROG-13-N1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **B-CORE** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[13].notes[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "that filing is the OPERATOR's to order" — *the text names the operator as the one who orders the new filing*

~~~text
P-BE-1's SCORED arm A1 HALTed at TP.score, as its filed §4 prescribes: the two-sample premise failed (200/200 campaign keys shared with card v6; the floor moves exits only). P-BE-1 has NO verdict and does not become the paired row. §11: 'a new id must be filed under set_change and the reason disclosed' — adding a registration is outside the contract ('no registration re-worded or added'), so that filing is the OPERATOR's to order. Its three Tier-E arms (A2 tuning, A3 holdout, A4 2R) were scored as report-only views, registered for that purpose; none may stand in for A1 (§11).
~~~

#### FN-PROG-13-N2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **B-CORE** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[13].notes[1]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "finish_family runs after B-5M" — *an executor sequencing note (B-5M has since run: see PROGRESS stage B-5M)*

~~~text
The family bar q/m = 0.1/6 is not on these rows yet; finish_family runs after B-5M. (Lettered clauses (a)(b)(c) are P-BE-1's structure; P-TRG-2's text makes the CI its only deciding clause.)
~~~

#### FN-PROG-14-N1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **B-5M** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[14].notes[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "finish_family ran with P-BE-1's slot HALTed" — *disclosure of the executor's finish_family invocation, prescribed by the texts*

~~~text
finish_family ran with P-BE-1's slot HALTed (--allow-halted-slot P-BE-1). This is PRESCRIBED by the filed texts, not an executor choice: P-BE-1 §7 'CLAUSE (c) RESOLVES ON THIS ROW ALONE and does not wait for siblings… if a sibling registration HALTs or is never filed, this row still reads clears_bh_bar against 0.016667'; P-TRG-2 §5 'at that one fixed bar to EVERY scored row it is handed, whatever number of the declared six actually run'. m stays 6 DECLARED (5 run): fewer tests never loosen the bar.
~~~

#### FN-PROG-14-N2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **B-5M** (COMPLETE-VERIFIED)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[14].notes[1]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "names the print-vs-deduction question OPEN for the operator" — *the text names the operator as the one who settles it*

~~~text
P-BRK-S1's net_r is net of FEE and FUNDING only; the measured 5m toll is a PRINT beside it (TOLL_ACCOUNTING), per its filed §7 which names the print-vs-deduction question OPEN for the operator. The row is already significantly negative before any toll.
~~~

#### FN-PROG-15-B1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED** · stage **CLOSE** (PARTIAL)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[15].blockers[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPERATOR: push + the LaCie destination (R6 granted push but " — *DEFAULT RULE: no declared owner rule matched; owner is 'operator' iff the word 'operator' occurs in the text*

~~~text
OPERATOR: push + the LaCie destination (R6 granted push but the operator said they would be asked again at CLOSE; the destination is unnamed — '/Volumes/LaCie/Repo Clone/naiad-backups' is an EXECUTOR LEAN). Until then: the build doc stays at research_outputs/tierc10/BUILD_DRAFT.md (LAW 5 — it moves to exchange/reports/ only at close, and exchange/** auto-publishes, which pushes the branch), LEDGER_APOLLO_APPEND.md is NOT appended, publish_exchange is NOT run.
~~~

#### FN-PROG-15-N1

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **CLOSE** (PARTIAL)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[15].notes[0]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "All 13 CLOSE builder suites (14 scripts; one is regime_prior" — *DEFAULT RULE: no declared owner rule matched; owner is 'operator' iff the word 'operator' occurs in the text*

~~~text
All 13 CLOSE builder suites (14 scripts; one is regime_prior's fixture twin) re-run by the orchestrator: exit 0. FIXTURES_CLOSE_box_cost and _ledger_append_root read LIVE repo/git state and move with every commit by design; they are regenerated in the CLOSE commit sequence.
~~~

#### FN-PROG-15-N2

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED** · stage **CLOSE** (PARTIAL)
- source: `research_outputs/tierc10/PROGRESS.json` · `stages[15].notes[1]`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "P-AGE-1 (tide-youth) and regime-prior had NO definition anyw" — *DEFAULT RULE: no declared owner rule matched; owner is 'operator' iff the word 'operator' occurs in the text*

~~~text
P-AGE-1 (tide-youth) and regime-prior had NO definition anywhere in the estate; both tables are Tier-E, gate nothing, and carry their definition as an EXECUTOR READING, NO NEW PIN.
~~~

### 3.2 · OPERATOR_RULINGS.md — the first 'Still blocked' list

*Heading (line 69):* `## Still blocked on the operator (no text exists on disk)`

#### FN-RUL-L1-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 71-71`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- The PANEL conflict (R2 "all 17" vs the resume contract's PANEL PIN "5-asset book").
~~~

#### FN-RUL-L1-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 72-72`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- The P-SPR-2 population conflict (R3 "full corridor" vs the contract's "exploration-classic").
~~~

#### FN-RUL-L1-3

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 73-74`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- Which NULL variant is the record (`gaps-only`, the contract-literal design, vs `gaps+order`,
  which reduces a measured own-window leak from 25.62% to 7.97%). Both are filed side by side.
~~~

#### FN-RUL-L1-4

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 75-76`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- Whether the 5m HOLD RATE is part of P-BRK-S1's scoring ground (if so it needs the same
  era collar the outcome rows have).
~~~

#### FN-RUL-L1-5

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 77-77`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- PUMPFUN → PUMPUSDT and MNT → Bybit are printed LEANS, not rulings; they need the nod at CLOSE.
~~~

#### FN-RUL-L1-6

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 78-78`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- The LaCie destination.
~~~

### 3.3 · OPERATOR_RULINGS.md — the second 'Still blocked' list (after R7–R10)

*Heading (line 139):* `## Still blocked on the operator after R7–R10`

#### FN-RUL-L2-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 141-144`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- **F-D-1 / R5.** "The USDT pair, either on Binance or Bybit" names the pair and permits the venue,
  but the actual disagreement is the venue's **REST API vs its BULK ARCHIVE**, which publish
  different bars on incident stamps. F-D-1 stays RED and is **printed RED**; F-D-1b carries. No bar
  is rewritten either way without the narrower word: **REST or ARCHIVE?**
~~~

#### FN-RUL-L2-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 145-147`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- **The 5m HOLD RATE.** If it is part of P-BRK-S1's scoring ground it needs the same holdout-era
  collar the outcome rows carry. Executor is proceeding on the **conservative** reading (collar it),
  and will say so on the row.
~~~

#### FN-RUL-L2-3

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 148-149`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- **PUMPFUN → PUMPUSDT** and **MNT → Bybit** remain printed LEANS, not rulings; they need the nod at
  CLOSE.
~~~

#### FN-RUL-L2-4

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/OPERATOR_RULINGS.md` · `lines 150-151`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "Still blocked on the operator" — *the list's own heading assigns every bullet to the operator*

~~~text
- **The LaCie destination** (R6 granted permission to push; the destination is still unnamed, and the
  default would create an empty vault — the real one is `/Volumes/LaCie/Repo Clone/naiad-backups`).
~~~

### 3.4 · STAGE_D_MANIFEST.json — operator_rulings_needed

#### FN-SDM-ORN-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `operator_rulings_needed[0]`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "RULING NEEDED" — *the manifest files it under operator_rulings_needed*

~~~text
F-D-1 IS RED and stays RED: the venue's REST API and its BULK ARCHIVE publish different bars on incident stamps and the panel is publication-heterogeneous on them (see venue_publications_disagree). RULING NEEDED: which publication is the record. Ruling ARCHIVE makes the REST-carrying files the odd ones out; ruling REST the ARCHIVE-carrying ones. The archive is no clean alternative: it lacks whole days, publishes nothing before 2020, and its monthly and daily zips disagree with each other on BTC incident bars. No bar is rewritten either way without the operator's word.
~~~

#### FN-SDM-ORN-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `operator_rulings_needed[1]`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "Needs the operator's" — *the manifest files it under operator_rulings_needed*

~~~text
PUMPFUN -> PUMPUSDT [LEAN D-d]: a printed lean, not a ruling. The roster probe recorded the near-match and explicitly did NOT map it; TC10 maps it because baseAsset PUMP is a TRADING perpetual and PUMPBTCUSDT is rejected by name. Needs the operator's nod at CLOSE.
~~~

#### FN-SDM-ORN-3

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `operator_rulings_needed[2]`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "Needs the operator's" — *the manifest files it under operator_rulings_needed*

~~~text
MNT -> Bybit v5 linear, whole tape, stem MNTUSDT_BYBIT [LEAN D-c]: a printed lean, not a ruling (no Binance USDT-M contract exists). The fee charged to it is the estate's flat Binance-era taker figure — an ASSUMPTION; Bybit's own base taker rate is widely quoted higher [UNVERIFIED]. Needs the operator's nod at CLOSE, or a named exclusion.
~~~

#### FN-SDM-ORN-4

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `operator_rulings_needed[3]`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "Needs the operator's" — *the manifest files it under operator_rulings_needed*

~~~text
LaCie mirror [LEAN L5]: not done. Every file TC10 fetched exists only in the snapshot on this laptop; the mirror command PUSHES and its default destination would create an empty vault. Needs the operator's destination and consent at CLOSE.
~~~

### 3.5 · STAGE_D_MANIFEST.json — as_of_hazards

#### FN-SDM-HAZ-funding_files_with_a_print_stamped_after_the_as_of_close

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.funding_files_with_a_print_stamped_after_the_as_of_close` · text form: canonical JSON of a non-string value
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
["funding/BTCUSDT.parquet", "funding/ETHUSDT.parquet", "funding/SOLUSDT.parquet", "funding/NEARUSDT.parquet", "funding/ZECUSDT.parquet", "funding/ENAUSDT.parquet", "funding/PUMPUSDT.parquet", "funding/HYPEUSDT.parquet", "funding/SUIUSDT.parquet", "funding/LTCUSDT.parquet", "funding/XMRUSDT.parquet", "funding/BNBUSDT.parquet", "funding/UNIUSDT.parquet", "funding/1000PEPEUSDT.parquet", "funding/DOGEUSDT.parquet", "funding/1000BONKUSDT.parquet"]
~~~

#### FN-SDM-HAZ-funding_floor_hour_equals_nearest_hour_on_every_file

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.funding_floor_hour_equals_nearest_hour_on_every_file` · text form: canonical JSON of a non-string value
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
true
~~~

#### FN-SDM-HAZ-funding_law

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.funding_law`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
[LEAN D-g] a print belongs to the hour its stamp FLOORS to; load_funding_asof returns funding_hour_ms and cuts on it; an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp
~~~

#### FN-SDM-HAZ-funding_ms_past_hour_max_over_panel

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.funding_ms_past_hour_max_over_panel` · text form: canonical JSON of a non-string value
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
47
~~~

#### FN-SDM-HAZ-kline_files_holding_rows_after_as_of

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.kline_files_holding_rows_after_as_of` · text form: canonical JSON of a non-string value
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "a TC10 lane that loads one of these files through it without an as-of cut reads past the pin" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
[{"path": "klines/BTCUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/ETHUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/SOLUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/NEARUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/ZECUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/ENAUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/HYPEUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/LTCUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/XMRUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/BNBUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/UNIUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/1000PEPEUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/DOGEUSDT_5m.parquet", "rows_after_as_of": 6}, {"path": "klines/1000BONKUSDT_5m.parquet", "rows_after_as_of": 6}]
~~~

#### FN-SDM-HAZ-kline_law

- **HARVESTED** · owner **executor** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` · `as_of_hazards.kline_law`
- owner basis: `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` — "a TC10 lane that loads one of these files through it without an as-of cut reads past the pin" — *an as-of hazard binds the executor's load path; the manifest's own law says how*

~~~text
these rows PRE-DATE TC10 and are never deleted [LEAN D-e]; tierc10_data.load_asof cuts them, but tierc2_baseline.load_klines reads the WHOLE file — a TC10 lane that loads one of these files through it without an as-of cut reads past the pin
~~~

### 3.6 · FAMILY.json — scored_slots_halted

#### FN-FAM-HALT-P-BE-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/FAMILY.json` · `scored_slots_halted.P-BE-1`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "that filing is the OPERATOR's to order" — *the ledger's B-CORE note assigns the new set_change filing to the operator*

~~~text
HALT: P-BE-1 — the arm shares the WHOLE campaign set with its base; the commissioned two-sample ruler's premise failed. File a NEW id under ruler='set_change' and disclose.
~~~

### 3.7 · Every brk_sealed_row.toll_accounting_status under scores/

#### FN-TOLL-DRYRUN-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/DRYRUN.json` · `beside_registration.P-BRK-I1.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

#### FN-TOLL-DRYRUN-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/DRYRUN.json` · `beside_registration.P-BRK-S1.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

#### FN-TOLL-P-BRK-I1-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/P-BRK-I1.rows.json` · `beside_registration.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

#### FN-TOLL-P-BRK-I1-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/P-BRK-I1.rows.json` · `rows[0].beside.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

#### FN-TOLL-P-BRK-S1-1

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/P-BRK-S1.rows.json` · `beside_registration.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

#### FN-TOLL-P-BRK-S1-2

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/scores/P-BRK-S1.rows.json` · `rows[0].beside.brk_sealed_row.toll_accounting_status`
- owner basis: `research_outputs/tierc10/PROGRESS.json` — "OPEN, for the operator" — *the ledger's BRK note leaves print-vs-deduction OPEN for the operator*

~~~text
PRINT, NOT A DEDUCTION — reported, not changed. The contract reads 'NET OF MEASURED 5m TOLL'; today's net_r is net of FEE and FUNDING only.
~~~

### 3.8 · REGISTRATION_PLAN.md — the 'drafting error' paragraph

#### FN-PLAN-DRAFTERR

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/REGISTRATION_PLAN.md` · `lines 95-98`
- owner basis: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` — "no registration re-worded or added" — *the error sits in the contract paste, which the executor may not re-word; amending it is the operator's*

~~~text
**The resume paste's "(FLIP_HOLD pins)" is a drafting error** — FLIP_HOLD (1.0 ATR / 6 bars) is
P-BRK-I1's *memory-line* pin set. The band set actually built and tuned per R1 is
`{ribbon89_127, ribbon127_200, tap89, tap127, tap200}`, tuned to **ribbon127_200 / margin 1.0 ATR /
hold 3 bars / ttl 400**. No text may quote FLIP_HOLD for S1.
~~~

### 3.9 · BUILD_DRAFT.md §R0.3 — the smoke-roots paragraph (DISCLOSED ONLY: nothing is moved or deleted, LAW 2)

#### FN-DRAFT-SMOKE

- **HARVESTED** · owner **operator** · status **REPORTED, NOT FIXED**
- source: `research_outputs/tierc10/BUILD_DRAFT.md` · `lines 481-487`
- owner basis: `research_outputs/tierc10/BUILD_DRAFT.md` — "operator chooses; nothing is deleted (§5.12)." — *rebuild or quarantine under _partial_<ts>/ is the operator's choice; THIS build discloses only and moves or deletes nothing (LAW 2)*

~~~text
**Disclosed, not moved:** `census/smoke/` and `null/smoke/`.
- They are legitimate smoke roots with their own manifests, but they carry full lookalike filenames.
- They were built before the R1 bands and the era split, so their contents are now wrong in substance.
- Both suites fall back to a smoke root only when the full root has no manifest, so the default resolves correctly
  today.
- **Still in place at this draft.** At CLOSE: rebuild them, or quarantine them under `_partial_<ts>/` per LAW 2. The
  operator chooses; nothing is deleted (§5.12).
~~~

## 4 · LEANS — labelled as leans

> **LEAN — an executor operationalisation, labelled as such; not a ruling, not a defect, not a result.** OPERATOR_RULINGS.md: "the lean is marked as such and is NOT the ruling."

### 4.census · `research_outputs/tierc10/census/leans.parquet`

#### LEAN-CENSUS-00

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `00` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 0 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L1 1d = exactly SIX complete native-4h bars per UTC day (the twin's law); 1w = seven such complete days, MONDAY-anchored UTC, complete weeks only. Source = native 4h, never 1h/5m aggregates.
~~~

#### LEAN-CENSUS-01

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `01` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 1 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L2 SCALE_MULT: every registered lane and every Stage-A stamp uses the FROZEN 3.0 (Pine/twin pin of record). CENSUS-R prints the self-calibrated SCALE tables WITH the frozen-3.0 tables beside. Calibrator = grid 1.5..4.0 step 0.25 (Pine minval/step), nearest confirmed-macro-range density to 0.75 per 100 bars, tie-break toward 3.0 then lower; the whole grid printed (F-GRID: every grid whole).
~~~

#### LEAN-CENSUS-02

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `02` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 2 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L3 analytics module = analytics/rangefinder_census.py: a PURE numpy port (no engine import, no IO, ATR passed IN as an argument), NOT added to analytics._MODULES (analytics_sha stays put) — printed as a finding.
~~~

#### LEAN-CENSUS-03

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `03` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 3 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L4 Outcome horizons H20/H100 = BARS OF THE LENS; censor (require k+H <= n-1), never shorten; anchor = close of the bar the event is KNOWN (known_at); signs and toll law per map_critic.md §4.6.
~~~

#### LEAN-CENSUS-04

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `04` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 4 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L6 Panels: CLASSIC5 = BTC ETH SOL NEAR ZEC; UNSEEN12 = the contract's twelve; PANEL17 = CLASSIC5 + admitted UNSEEN12.
~~~

#### LEAN-CENSUS-05

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `05` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 5 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-a BOUNDARY AGE = bars since the AS-OF boundary VALUE on that side last changed: set at the confirm bar, moved by each same-side harden's redraw FROM the harden bar; 0 on the bar it changes. bnd_age = the NEAREST boundary's (tie -> top, the snapshot's law). range_age = t - confirm_i rides beside. Never from backdated_from: the back-dated left edge is render-only and lies in the past of its own knowledge.
~~~

#### LEAN-CENSUS-06

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `06` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 6 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-b with NO live confirmed macro range (most bars at SCALE 3.0) %-of-range, dist-to-boundary, ages and deviations read NaN / -1 — never the last corpse's box; in_range says which.
~~~

#### LEAN-CENSUS-07

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `07` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 7 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-c memory-touch is filed under BOTH definitions: `memory-touch-v1` (the machine's one-sided first touch per side) and `memory-touch-2s` (the first two-sided touch of the leash line, verdict unread, anchored at the touch bar).
~~~

#### LEAN-CENSUS-08

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `08` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 8 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-d retest-hold rides the OPERATOR's five R1 bands — ribbon 89/127, ribbon 127/200, tap 89, tap 127, tap 200 — EMAs of CLOSE on the lens's own bars, the warm-up NaN and never imputed. The hold pins (margin_atr, hold_bars) are TUNED under the R1 protocol on the 5m lens, TUNING ERA ONLY, and ONE pin pair rules all five bands and all three lenses; the 1d tuning is filed SEPARATELY for the Tier-E P-BRK-I1 print and never mixed into this grid. The candidacy TTL (400 bars, superseded at the next macro DIE) and the band warm-up remain executor pins.
~~~

#### LEAN-CENSUS-09

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `09` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 9 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-h THE ERA SPLIT [R1]: every ledger and grid row carries the era of its ANCHOR bar's close — 'tuning' <= 2024-06-30T23:59:59Z, 'holdout' after. The grid is filed three ways per class: 'ALL' (the contract's full-history row) with 'tuning' and 'holdout' BESIDE it. They are not addends: an anchor is in exactly one era, and ALL is the union, but a median of a union is not a function of the parts' medians.
~~~

#### LEAN-CENSUS-10

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `10` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 10 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-i THE COLLAR ON P-BRK-S1's SCORING GROUND [LAW 4 + R1]: the 5m retest-hold rows outside the TUNING era are FILED and never printed, summarised or quoted — not in a digest, not in a log line, not in a report field. printable(lens, cls, era) is the one gate and F-C10-COLLAR scans every artifact this build writes.
~~~

#### LEAN-CENSUS-11

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `11` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 11 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-e the leash runs LEAN (retests=False) on EVERY lens: the two per-bar spam classes feed none of the six classes and the port's fixture proves the lean log is the full log minus them. The micro scale is not run: it writes no state, line or flip.
~~~

#### LEAN-CENSUS-12

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `12` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 12 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-f the toll bps is READ per asset from Stage D's fee_schedule.json (round_trip_bps_used) and, absent that file, from tierc2_rules.FEE_BPS_ROUND_TRIP; the source rides every row. toll_atr on a row = median over THAT row's uncensored anchors; toll_atr_all = median over all of the class's anchors; pooled rows print the BINDING (max) per-asset toll.
~~~

#### LEAN-CENSUS-13

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `13` (column `lean`)
- source: `research_outputs/tierc10/census/leans.parquet` · `row 13 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] C-g n below PROVISIONAL_MIN_N (30) is PRINTED and flagged provisional, the lineage's law; a statistic is NaN only when n = 0, and then nan_reason says why (no events / all anchors censored).
~~~

### 4.panel · `research_outputs/tierc10/panel/leans.parquet`

#### LEAN-PANEL-L1

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L1` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 0 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
1d = exactly SIX complete native-4h bars per UTC day (the twin's law); 1w = seven such complete days, MONDAY-anchored UTC, complete weeks only. Source = native 4h, never 1h/5m aggregates.
~~~

#### LEAN-PANEL-L2

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L2` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 1 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
SCALE_MULT: every registered lane and every Stage-A stamp uses the FROZEN 3.0 (Pine/twin pin of record). CENSUS-R prints the self-calibrated SCALE tables WITH the frozen-3.0 tables beside. Calibrator = grid 1.5..4.0 step 0.25 (Pine minval/step), nearest confirmed-macro-range density to 0.75 per 100 bars, tie-break toward 3.0 then lower; the whole grid printed (F-GRID: every grid whole).
~~~

#### LEAN-PANEL-L3

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L3` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 2 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
analytics module = analytics/rangefinder_census.py: a PURE numpy port (no engine import, no IO, ATR passed IN as an argument), NOT added to analytics._MODULES (analytics_sha stays put) — printed as a finding.
~~~

#### LEAN-PANEL-L4

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L4` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 3 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
Outcome horizons H20/H100 = BARS OF THE LENS; censor (require k+H <= n-1), never shorten; anchor = close of the bar the event is KNOWN (known_at); signs and toll law per map_critic.md §4.6.
~~~

#### LEAN-PANEL-L5

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L5` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 4 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
All TC10 fetching lands in the snapshot only; promotion to the live cache and the LaCie mirror happen at CLOSE (the mirror command pushes — map_critic §4.2).
~~~

#### LEAN-PANEL-L6

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L6` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 5 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
Panels: CLASSIC5 = BTC ETH SOL NEAR ZEC; UNSEEN12 = the contract's twelve; PANEL17 = CLASSIC5 + admitted UNSEEN12. LOAO "above-half": 3/5 generalises to strict majority ceil((N+1)/2) → 7/12.
~~~

#### LEAN-PANEL-L7

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L7` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 6 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
FDR: ONE fixed bar q/m = 0.10/6 = 0.016667 per scored row (no step-up) — that is what makes the six independently failable.
~~~

#### LEAN-PANEL-L8

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `L8` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 7 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
Rulers seeded 20260921; a sensitivity block re-runs with the lineage seed 20260816.
~~~

#### LEAN-PANEL-panel-verdict

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `panel-verdict` (column `lean`)
- source: `research_outputs/tierc10/panel/leans.parquet` · `row 8 · column text`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
the SCORED statistic (verdict, p vs the BH bar) is the RAW panel expectancy — the lineage's ruler since TIER-C5; the equal-asset-risk co-headline carries its own NEW cluster-bootstrap CI and a would-be verdict beside it and gates nothing; disagreement is flagged on the row.
~~~

### 4.stamps · `research_outputs/tierc10/stamps/leans.parquet`

#### LEAN-STAMPS-1

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `1` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 0 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L2 SCALE_MULT: every Stage-A stamp uses the FROZEN 3.0 (Pine/twin pin of record), read BY OBJECT from tierc10_census.FROZEN_SCALE. The self-calibrated SCALE is a CENSUS-R report-only object and may not reach a stamp.
~~~

#### LEAN-STAMPS-2

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `2` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 1 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L4 as-of anchoring: an instant is stamped at the close of ITS OWN bar (instant_ms + the LANE lens's step), and the stamp bar is the last bar of the STAMP lens closed at or before that instant. A bar still forming at the instant is never read.
~~~

#### LEAN-STAMPS-3

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `3` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 2 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L6 Panels: the control is card v6 on CLASSIC5 = BTC ETH SOL NEAR ZEC; the twelve unseen assets are NOT ridden here and no lane but the known control is ridden anywhere in this module.
~~~

#### LEAN-STAMPS-4

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `4` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 3 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] L8 seed 20260921 threaded explicitly; sensitivity echo 20260816. Nothing in Stage A draws at random — the seeds ride the manifest so a later consumer cannot invent one.
~~~

#### LEAN-STAMPS-5

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `5` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 4 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] S-a MACRO STATE IS FOUR-VALUED. The contract says the stamps are explicit nulls with macro_state='NONE' when no macro range is alive. Taken to the letter that would collapse BULL_EXP and BEAR_EXP — the machine's post-DIE expansion latch, a genuine as-of fact and the most useful half of the column — into 'NONE', because at SCALE 3.0 the latch is non-zero on exactly the bars where no range is alive. So: every GEOMETRY stamp is null the moment no range is alive (the forward-fill ban in full), and macro_state reads 'NONE' only when no range is alive AND the machine has sealed no pivot — nothing known. `in_range` is filed beside it, so the strict two-valued reading is one filter away and nothing is lost either way.
~~~

#### LEAN-STAMPS-6

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `6` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 5 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] S-b THE +1R INSTANT is the card's OWN latch bar, not a breakeven floor: the first bar j in (entry_i, exit_i] whose FAVOURABLE extreme reaches entry + 1R — the bar `trail_arm_after_r = 1.0` arms the ratchet on. It is re-derived from the raw 4h bars because the ride records the latch (`reached_1r`) and not its bar, and the extractor HALTS if its re-derivation and the ride's latch ever disagree on one campaign.
~~~

#### LEAN-STAMPS-7

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `7` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 6 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] S-c A REJECT IS STAMPED WHERE IT BECAME KNOWABLE, not at the arming bar: tide/d at the arming bar, no_trigger at the last bar the window searched, position_open at the trigger bar. REJECT_BAR_LAW carries the rule per reason and rides every reject row.
~~~

#### LEAN-STAMPS-8

- **LEAN** · owner **executor** · status **REPORTED, NOT FIXED** · lean id `8` (column `n`)
- source: `research_outputs/tierc10/stamps/leans.parquet` · `row 7 · column lean`
- owner basis: `research_outputs/tierc10/OPERATOR_RULINGS.md` — "the lean is marked as such and is NOT the ruling" — *a lean is the executor's operationalisation; the operator may overrule it*

~~~text
[LEAN-HEPHAESTUS] S-d `window_open` is emitted as its own instant although card v6 opens the window AT the arming bar (the 12/89 cross is both). The two rows are equal BY CONSTRUCTION on v6 and a fixture leg demands it; they are kept apart so a later card whose arming and window differ needs no new vocabulary.
~~~

## 5 · The git-volatile fields — named, and excluded from F-DET

- `git`
- `measured.iv`
- `measured.v`
- `findings[id=FN-M-iv].text`
- `findings[id=FN-M-v].text`
- in this Markdown: every block between `<!-- git-volatile:begin -->` and `<!-- git-volatile:end -->`

## 6 · What this document is not

- Not a fix. No input is edited; F-FN-READONLY proves it on every run.
- Not a score. No registration is scored or re-scored and no verdict field is read; the only values read out of the scores/ files are `arm`, `beside.haircut_twin.{tc,twin}_expectancy_r`, `brk_sealed_row.toll_accounting_status` and FAMILY.json `scored_slots_halted`.
- Not a read of bars. No kline or funding file is opened.
- Not a claim that every item is open: the status says what this build did, not what the item is. The texts that record their own repair are listed above.
- Not a ruling. Every owner is the executor's reading, and its basis is quoted verbatim so it can be checked.
