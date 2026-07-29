# ARCHIVE DEPENDENCIES

**THE RULE (standing, adopted 2026-07-28, contract v4 §0.4).** No phase directory under `research_outputs/` is archived until this document is regenerated and the archive's manifest records which readers depend on it.

The 2026-07-27 reclamation cost two retrievals -- the `c141t213` regression fixture and the S-3 journals the census Phase 0 needs. Both were avoidable with one grep. This file is that grep, made durable.

Regenerate with `scripts/archive_dependencies.py`. Scan scope: `fixtures`, `tests`, `scripts` for `*.py` and `*.ps1`.

## Summary

| path under `research_outputs/` | state on disk | archived in | referencing sites |
|---|---|---|---:|
| `_archive/` | resolves (6 files) | - | 2 |
| `brief/` | resolves (5 files) | - | 5 |
| `census/` | resolves (7 files) | - | 15 |
| `census1b/` | resolves (4 files) | - | 3 |
| `census1b_run2/` | resolves (1 files) | - | 3 |
| `census_run2/` | resolves (1 files) | - | 1 |
| `coverage/` | resolves (1 files) | - | 2 |
| `dryrun/` | **MISSING** | - | 3 |
| `dryrun_autopsy/` | resolves (file) | - | 1 |
| `packets/` | resolves (6 files) | - | 3 |
| `parity/` | resolves (27 files) | - | 5 |
| `s1/` | THIN SHELL -- 5 of 1563 archived files on disk; the rest are only inside the zip | s1_2026-07-27.zip | 25 |
| `s2/` | THIN SHELL -- 2 of 1548 archived files on disk; the rest are only inside the zip | s2_2026-07-27.zip | 8 |
| `s3/` | THIN SHELL -- 4 of 1550 archived files on disk; the rest are only inside the zip | s3_2026-07-27.zip | 3 |
| `tc1/` | THIN SHELL -- 3 of 5274 archived files on disk; the rest are only inside the zip | tc1_2026-07-27.zip | 7 |
| `tc4/` | THIN SHELL -- 3 of 1509 archived files on disk; the rest are only inside the zip | tc4_2026-07-27.zip | 14 |
| `tc5/` | resolves (506 files) | - | 7 |
| `v3_anchor/` | THIN SHELL -- 10 of 2058 archived files on disk; the rest are only inside the zip | v3_anchor_2026-07-27.zip | 7 |

### Archives present

| archive | entries |
|---|---:|
| `s1_2026-07-27.zip` | 1564 |
| `s2_2026-07-27.zip` | 1549 |
| `s3_2026-07-27.zip` | 1551 |
| `tc1_2026-07-27.zip` | 5275 |
| `tc4_2026-07-27.zip` | 1510 |
| `v3_anchor_2026-07-27.zip` | 2059 |

## Detail -- every referencing site

### `research_outputs/_archive/` — resolves (6 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/archive_dependencies.py` | 50 | ref | `arch_dir = REPO / "research_outputs" / "_archive"` |
| `scripts/backup_estate.py` | 482 | ref | `dest = REPO / "research_outputs" / "_archive"` |

### `research_outputs/brief/` — resolves (5 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/brief_lookup.py` | 5 | ref | `Reads research_outputs/brief/brief_index.jsonl — one line per date — and prints` |
| `scripts/brief_lookup.py` | 23 | ref | `DEFAULT_INDEX = ROOT / "research_outputs" / "brief" / "brief_index.jsonl"` |
| `scripts/daily_brief.py` | 73 | write | `OUT_DIR = ROOT / "research_outputs" / "brief"` |
| `scripts/setup_brief_schedule.ps1` | 8 | ref | `venv and appends output to research_outputs/brief/brief_run.log.` |
| `scripts/setup_brief_schedule.ps1` | 45 | ref | `$logDir = Join-Path $repo "research_outputs\brief"` |

### `research_outputs/census/` — resolves (7 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/archive_dependencies.py` | 15 | ref | `# "research_outputs" / "census" / ...   \|   research_outputs/census/...` |
| `scripts/backup_estate.py` | 186 | ref | `"research_outputs/census/build_manifest.json"]` |
| `scripts/backup_estate.py` | 428 | ref | `"research_outputs/census/build_manifest.json"}` |
| `scripts/census.py` | 12 | ref | `refetch_log.json) in research_outputs/census/. All scans are timestamp-and-` |
| `scripts/census.py` | 32 | ref | `SIDECARS = ROOT / "research_outputs" / "census"` |
| `scripts/census1b_analyze.py` | 3 | ref | `Consumes the BYTE-FROZEN CENSUS-1 substrate (research_outputs/census/) and` |
| `scripts/census1b_analyze.py` | 40 | ref | `CENSUS = ROOT / "research_outputs" / "census"` |
| `scripts/census1b_det.py` | 112 | ref | `(ROOT / "research_outputs" / "census" / "build_manifest.json")` |
| `scripts/census_analyze.py` | 34 | ref | `CENSUS = ROOT / "research_outputs" / "census"` |
| `scripts/census_analyze.py` | 405 | ref | `"artifact": "research_outputs/census/census_outcomes.jsonl"}` |
| `scripts/census_build.py` | 9 | ref | `research_outputs/census[_run2]/` |
| `scripts/reviewer_manifest.py` | 78 | ref | `"research_outputs/census/build_manifest.json",` |
| `scripts/v12_packet.py` | 50 | ref | `"research_outputs/census/retrieval_meta.json",` |
| `scripts/v12_packet.py` | 51 | ref | `"research_outputs/census/refetch_log.json")]` |
| `scripts/v12_packet.py` | 77 | ref | `"  GAP_REPORT.md, SPOT_CHECK.md; sidecars research_outputs/census/.",` |

### `research_outputs/census1b/` — resolves (4 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/census1b_analyze.py` | 41 | write | `OUT_DIR = ROOT / "research_outputs" / "census1b"` |
| `scripts/census1b_det.py` | 24 | write | `OUT = ROOT / "research_outputs" / "census1b"` |
| `scripts/census1b_report.py` | 66 | ref | `det_p = ROOT / "research_outputs" / "census1b" / "determinism.json"` |

### `research_outputs/census1b_run2/` — resolves (1 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/census1b_analyze.py` | 1120 | ref | `help="F1b-DET second pass into research_outputs/census1b_run2/")` |
| `scripts/census1b_analyze.py` | 1126 | write | `OUT_DIR = ROOT / "research_outputs" / "census1b_run2"` |
| `scripts/census1b_det.py` | 23 | ref | `R2 = ROOT / "research_outputs" / "census1b_run2"` |

### `research_outputs/census_run2/` — resolves (1 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/census_analyze.py` | 35 | ref | `CENSUS2 = ROOT / "research_outputs" / "census_run2"` |

### `research_outputs/coverage/` — resolves (1 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/backfill.py` | 9 | write | `Writes a coverage report to research_outputs/coverage/.` |
| `scripts/backfill.py` | 57 | read | `out = Path(__file__).resolve().parent.parent / "research_outputs" / "coverage" / "coverage.json"` |

### `research_outputs/dryrun/` — MISSING

| reader | line | kind | source |
|---|---:|---|---|
| `fixtures/test_f8_journal.py` | 21 | ref | `DRYRUN = ROOT / "research_outputs" / "dryrun" / "journal"` |
| `scripts/dryrun_autopsy.py` | 5 | ref | `research_outputs/dryrun/journal/, then answers every question in` |
| `scripts/dryrun_autopsy.py` | 26 | ref | `JROOT = ROOT / "research_outputs" / "dryrun" / "journal"` |

### `research_outputs/dryrun_autopsy/` — resolves (file)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/dryrun_autopsy.py` | 7 | ref | `research_outputs/dryrun_autopsy.md. F8 scans both artifacts.` |

### `research_outputs/packets/` — resolves (6 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/packet.py` | 39 | write | `out_dir = ROOT / "research_outputs" / "packets"` |
| `scripts/v12_packet.py` | 8 | ref | `documents, and a one-page manifest. Lands in research_outputs/packets/` |
| `scripts/v12_packet.py` | 31 | write | `out_dir = ROOT / "research_outputs" / "packets"` |

### `research_outputs/parity/` — resolves (27 files)

| reader | line | kind | source |
|---|---:|---|---|
| `fixtures/test_f6_parity.py` | 18 | ref | `PARITY = ROOT / "research_outputs" / "parity"` |
| `fixtures/test_i_input_parity.py` | 29 | ref | `PARITY_JOURNAL = ROOT / "research_outputs" / "parity" / "journal" / "BTCUSDT_swing"` |
| `scripts/parity_pack.py` | 3 | ref | `Produces, under research_outputs/parity/:` |
| `scripts/parity_pack.py` | 35 | write | `OUT = ROOT / "research_outputs" / "parity"` |
| `scripts/parity_pack.py` | 168 | ref | `ap.add_argument("--journal-root", default=str(ROOT / "research_outputs" / "parity" / "journal"))` |

### `research_outputs/s1/` — THIN SHELL -- 5 of 1563 archived files on disk; the rest are only inside the zip

Archived in `s1_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `fixtures/test_s2_sim.py` | 69 | read | `s2_resampled_dir=Path("research_outputs/s1/resampled"))` |
| `scripts/rc7_recompute.py` | 10 | ref | `research_outputs/s1/ (engine 1.0.9 run, verified PASS). No engine` |
| `scripts/rc7_recompute.py` | 35 | ref | `S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"` |
| `scripts/rc7_recompute.py` | 36 | ref | `S1E = ROOT / "research_outputs" / "s1" / "s1_events"` |
| `scripts/rc7_recompute.py` | 37 | ref | `MANIFEST = ROOT / "research_outputs" / "s1" / "manifest.json"` |
| `scripts/s1_fixtures.py` | 35 | ref | `S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"` |
| `scripts/s1_fixtures.py` | 36 | ref | `S1J2 = ROOT / "research_outputs" / "s1" / "journal_s1_run2" / "scored"` |
| `scripts/s1_fixtures.py` | 37 | ref | `S1E = ROOT / "research_outputs" / "s1" / "s1_events"` |
| `scripts/s1_fixtures.py` | 38 | ref | `S1E2 = ROOT / "research_outputs" / "s1" / "s1_events_run2"` |
| `scripts/s1_fixtures.py` | 39 | ref | `MANIFEST = ROOT / "research_outputs" / "s1" / "manifest.json"` |
| `scripts/s1_fixtures.py` | 40 | ref | `RESAMPLE_REPORT = ROOT / "research_outputs" / "s1" / "resampled" / \` |
| `scripts/s1_fixtures.py` | 42 | write | `OUT_DIR = ROOT / "research_outputs" / "s1"` |
| `scripts/s1_resample.py` | 4 | ref | `OFFLINE (no network). Output goes to research_outputs/s1/resampled/ —` |
| `scripts/s1_resample.py` | 36 | write | `OUT = ROOT / "research_outputs" / "s1" / "resampled"` |
| `scripts/s1_runner.py` | 5 | ref | `research_outputs/s1/journal_s1/scored/<cell>/       + s1_events/` |
| `scripts/s1_runner.py` | 6 | ref | `research_outputs/s1/journal_s1_run2/scored/<cell>/  + s1_events_run2/` |
| `scripts/s1_runner.py` | 26 | write | `OUT = ROOT / "research_outputs" / "s1"` |
| `scripts/s1_runner.py` | 115 | ref | `"data_source": "census estate + research_outputs/s1/resampled, "` |
| `scripts/s2_fixtures.py` | 29 | ref | `S1J = ROOT / "research_outputs" / "s1" / "journal_s1" / "scored"` |
| `scripts/s2_runner.py` | 5 | ref | `research_outputs/s1/journal_s2/scored/<cell>/       + s2_events/` |
| `scripts/s2_runner.py` | 6 | ref | `research_outputs/s1/journal_s2_run2/scored/<cell>/  + s2_events_run2/` |
| `scripts/s2_runner.py` | 27 | ref | `RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"` |
| `scripts/s2_runner.py` | 115 | ref | `"data_source": "census estate + research_outputs/s1/resampled, "` |
| `scripts/s3_analyze.py` | 30 | ref | `RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"` |
| `scripts/s3_enrich.py` | 36 | ref | `RESAMPLED = ROOT / "research_outputs" / "s1" / "resampled"` |

### `research_outputs/s2/` — THIN SHELL -- 2 of 1548 archived files on disk; the rest are only inside the zip

Archived in `s2_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/s2_fixtures.py` | 25 | ref | `S2J = ROOT / "research_outputs" / "s2" / "journal_s2" / "scored"` |
| `scripts/s2_fixtures.py` | 26 | ref | `S2J2 = ROOT / "research_outputs" / "s2" / "journal_s2_run2" / "scored"` |
| `scripts/s2_fixtures.py` | 27 | ref | `S2E = ROOT / "research_outputs" / "s2" / "s2_events"` |
| `scripts/s2_fixtures.py` | 28 | ref | `S2E2 = ROOT / "research_outputs" / "s2" / "s2_events_run2"` |
| `scripts/s2_fixtures.py` | 31 | ref | `MAN = ROOT / "research_outputs" / "s2" / "manifest.json"` |
| `scripts/s2_runner.py` | 26 | write | `OUT = ROOT / "research_outputs" / "s2"` |
| `scripts/s2b_decompose.py` | 4 | ref | `arithmetic over research_outputs/s2/journal_s2 (engine 1.0.10, PASS at` |
| `scripts/s2b_decompose.py` | 29 | ref | `S2J = ROOT / "research_outputs" / "s2" / "journal_s2" / "scored"` |

### `research_outputs/s3/` — THIN SHELL -- 4 of 1550 archived files on disk; the rest are only inside the zip

Archived in `s3_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/s3_analyze.py` | 29 | write | `OUT = ROOT / "research_outputs" / "s3"` |
| `scripts/s3_enrich.py` | 12 | ref | `determinism, capture on, into research_outputs/s3/.` |
| `scripts/s3_enrich.py` | 35 | write | `OUT = ROOT / "research_outputs" / "s3"` |

### `research_outputs/tc1/` — THIN SHELL -- 3 of 5274 archived files on disk; the rest are only inside the zip

Archived in `tc1_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/s3_analyze.py` | 31 | ref | `REF = ROOT / "research_outputs" / "tc1" / "B_run1" / "scored"   # F-BYTE baseline` |
| `scripts/s3_enrich.py` | 37 | ref | `REF = ROOT / "research_outputs" / "tc1" / "B_run1" / "scored"   # F-BYTE baseline` |
| `scripts/s3_enrich.py` | 148 | ref | `"baseline_for_F_BYTE": "research_outputs/tc1/B_run1 (engine 1.0.11, "` |
| `scripts/tc1_fixtures.py` | 5 | ref | `over research_outputs/tc1/{A, B_run1, C_run1, D_run1} with journal_pass2 as` |
| `scripts/tc1_fixtures.py` | 30 | ref | `TC1 = ROOT / "research_outputs" / "tc1"` |
| `scripts/tc1_runner.py` | 4 | ref | `Roots research_outputs/tc1/{A, B_run1, B_run2, C_run1, C_run2, D_run1,` |
| `scripts/tc1_runner.py` | 23 | write | `OUT = ROOT / "research_outputs" / "tc1"` |

### `research_outputs/tc4/` — THIN SHELL -- 3 of 1509 archived files on disk; the rest are only inside the zip

Archived in `tc4_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/s1_fixtures.py` | 34 | ref | `P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |
| `scripts/s1_runner.py` | 112 | ref | `"baseline": "research_outputs/tc4/journal_pass2 (engine 1.0.8)",` |
| `scripts/s2_fixtures.py` | 30 | ref | `P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |
| `scripts/s2_runner.py` | 112 | ref | `"baseline": "research_outputs/tc4/journal_pass2 (engine 1.0.8); s1 joined from journal_s1, not re-emitted",` |
| `scripts/tc1_fixtures.py` | 31 | ref | `PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |
| `scripts/tc1_runner.py` | 22 | ref | `PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |
| `scripts/tc4_fixtures.py` | 35 | ref | `PASS2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |
| `scripts/tc4_fixtures.py` | 36 | ref | `RUN2 = ROOT / "research_outputs" / "tc4" / "journal_pass2_run2" / "scored"` |
| `scripts/tc4_fixtures.py` | 37 | write | `OUT_DIR = ROOT / "research_outputs" / "tc4"` |
| `scripts/tc4_runner.py` | 8 | ref | `research_outputs/tc4/journal_pass2/scored/<cell>/        (deliverable)` |
| `scripts/tc4_runner.py` | 9 | ref | `research_outputs/tc4/journal_pass2_run2/scored/<cell>/   (determinism twin)` |
| `scripts/tc4_runner.py` | 30 | write | `OUT = ROOT / "research_outputs" / "tc4"` |
| `scripts/tc5_fixtures.py` | 5 | ref | `swing same-asset subsets joined from research_outputs/tc4/journal_pass2.` |
| `scripts/tc5_fixtures.py` | 31 | ref | `P2 = ROOT / "research_outputs" / "tc4" / "journal_pass2" / "scored"` |

### `research_outputs/tc5/` — resolves (506 files)

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/tc5_fixtures.py` | 4 | ref | `Read-only over research_outputs/tc5/journal_tc5 (v2) with v1-intraday and` |
| `scripts/tc5_fixtures.py` | 29 | ref | `TC5 = ROOT / "research_outputs" / "tc5" / "journal_tc5" / "scored"` |
| `scripts/tc5_fixtures.py` | 30 | ref | `TC5B = ROOT / "research_outputs" / "tc5" / "journal_tc5_run2" / "scored"` |
| `scripts/tc5_fixtures.py` | 32 | ref | `MAN = ROOT / "research_outputs" / "tc5" / "manifest.json"` |
| `scripts/tc5_runner.py` | 9 | ref | `Roots research_outputs/tc5/{journal_tc5, journal_tc5_run2}; prior roots` |
| `scripts/tc5_runner.py` | 65 | ref | `root = ROOT / "research_outputs" / "tc5" / name / "scored"` |
| `scripts/tc5_runner.py` | 87 | write | `out = ROOT / "research_outputs" / "tc5"` |

### `research_outputs/v3_anchor/` — THIN SHELL -- 10 of 2058 archived files on disk; the rest are only inside the zip

Archived in `v3_anchor_2026-07-27.zip`.

| reader | line | kind | source |
|---|---:|---|---|
| `scripts/rc_recompute.py` | 1398 | ref | `default=here / "research_outputs" / "v3_anchor"` |
| `scripts/tc4_fixtures.py` | 34 | ref | `PASS1 = ROOT / "research_outputs" / "v3_anchor" / "journal_pass1" / "scored"` |
| `scripts/tc4_runner.py` | 11 | ref | `journal_pass1 (research_outputs/v3_anchor/) is READ-ONLY history and is` |
| `scripts/v3_recompute.py` | 1544 | ref | `default=here / "research_outputs" / "v3_anchor"` |
| `scripts/v3_scorer.py` | 4 | ref | `research_outputs/v3_anchor/: manifest.json/md, cards.json + CELL_CARDS.md,` |
| `scripts/v3_scorer.py` | 34 | write | `OUT = ROOT / "research_outputs" / "v3_anchor"` |
| `scripts/v3_scorer.py` | 387 | ref | `- Data: census estate, offline, zero fetches. Hypothesis scorecard H-A1..H-A5 in research_outputs/v3_anchor/ (numbers not restated here pending review` |

