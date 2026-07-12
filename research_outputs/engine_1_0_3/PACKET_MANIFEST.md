# Engine 1.0.3 "Input Parity" — packet manifest (2026-07-12)

Branch `engine-1.0.3-input-parity` (off v12-v1-census head `1d3e498`), commit
`0c51660`. Operator owns the merge. Root cause of record: engine hardcoded
`zone_memory=5`; deployed Pine runs `zoneMemory=3` (operator-verified on the
deployed chart AND the v11.3 layout). Parity target = the deployed chart.

## Phase A — audit (gate)
Sole unratified input-constant drift = `zone_memory` (swing/5m, 5 vs 3). All 29
signal constants MATCH the Pine defaults in both configs; TFs + v_births_provisional
are charter items. **Gate passed** (`A_input_parity_audit.md`).

## The fix (D1)
`engine/cells.py` `Cell.zone_memory` → 3 (all mandates; was 5 for 5m). Version
1.0.2 → 1.0.3. Zero signal-logic change. Manifest `fixtures/pine_defaults_manifest.yaml`
committed as the fixture's source of truth (extracted from the .pine).

## Fixtures (D2)
- **Added (I4 family, `fixtures/test_i_input_parity.py`, 8 tests):** signal-constant
  parity ×2 configs; `zone_memory` parity ×3 mandates; behavioral pins at mem=3 —
  no PRIME (May 23 16:20), no grade-C (May 27 12:45), no CONFIRMs (Jun 23 17:00/17:45/20:45).
- **Changed-anchor list: EMPTY.** No existing fixture pins a mem=5 journal anchor —
  the synthetic F1–F8 suite runs on **intraday** cells (`make_cell("BTCUSDT","intraday")`,
  exec=1m → zone_memory=3 before and after, byte-identical), and F6 is structural.
- **One count change, not an anchor:** `test_f8_journal::test_dryrun_journal_no_dead_columns`
  flips **pass → skip** because D3 archived the dryrun journal (the test is `skipif(not DRYRUN.exists())`,
  unmodified). No other existing fixture modified.

## Journals (D3)
- Archived (regenerate-never-merge): `research_outputs/parity/journal_mem5_archive/`
  (mem=5 parity + `dryrun_naiad_v0/`) + README = the zoneMemory-5 v12 seed.
- Regenerated parity journal (mem=3, engine 1.0.3):

  | | old (mem=5) | new (mem=3) |
  |---|---|---|
  | run_id | 20711045f738b7c7 | **1869ff707385dc4e** |
  | journal SHA256 | (archived) | **4c7343178af89dc14cd25933a3d5ab76c6b21211d090aad578d81e7413ce92de** |
  | rows | 5309 | **5446** |
  | PRIME / CONFIRM / TAG | 1314 / 475 / 1083 | **1308 / 463 / 1219** |

  Full census (new): CLUSTER 504, CONFIRM 463, PRIME 1308, REGIME 30, REJECT 1845,
  STAGE 5, TAG 1219, TPW 53, V 1, X 18 = 5446.

## I3 — shadow equivalence (gate)
Regenerated journal vs the validated shadow-at-3 (instrumented Pine port,
bit-validated against the engine): **1790 load-bearing entry events (PRIME/CONFIRM/V/X),
0 missing / 0 extra / 0 field-mismatch → I3 DIFF = ZERO.** (`I3_diff.txt`.)

## Case windows (D4)
All six tables regenerated from the mem=3 journal (`case_windows.md`); the mem=5
break events are gone (May 23 16:20 PRIME, May 27 12:45 C, Jun 23 CONFIRMs). The
F6 sign-off note now states the verified inputs (Zone memory = 3 et al.).

## Suite
**47 passed, 1 skipped** (was 40 passed). Δ = +8 input-parity fixtures; F8b dryrun
scan pass→skip (D3 archive). Nothing else changed.

## Blast radius (mem=5 → mem=3, informational; measured pre-fix)
18 entries removed (6 PRIME + 12 CONFIRM), 2 CONFIRM regrades, 4,360 stop-divergent
bars over 2025-10-06 → 2026-07-07. One-way: the mem=3 chart loses entries the mem=5
engine took. Archived as the zoneMemory-5 seed's headline.

## Contents
`A_input_parity_audit.md`, `PACKET_MANIFEST.md`, `fix.diff`, `ledger.diff`,
`I3_diff.txt`, `fixtures/pine_defaults_manifest.yaml`, `fixtures/test_i_input_parity.py`,
`case_windows.md`.
