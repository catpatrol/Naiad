# TIER-C11 · TC11-BOOKS — the two frozen books (control / descriptive)

as_of_last_closed_4h: 2026-09-25T00:00:00Z · latest closed 4h at fetch time (AS_OF_PIN.json latest_closed_4h_at_pin_run): 2026-09-25T00:00:00Z · substrate tc11_20260925 · corridor 2019-09-08T16:00:00Z → 2026-09-25T00:00:00Z · CLASSIC5 · seed 20260924

**These are CONTROL / DESCRIPTIVE numbers, not registration scores.** No CI, no p, no verdict word; every cut below is a SELECTION, not a result.  Every descriptive table carries the L-1.4 collar (tier = 'TIER-E', selection_not_a_result = 'a SELECTION, not a result', gates = 'nothing'); the anchor table is a set of control identities that gate this BUILD (a RED anchor writes nothing), so it carries no collar.

**Precision.** Every float column of the four parquet tables is rounded to 6 dp at write (tierc2_baseline._round_floats via TP.make_put).  Flags (r_over_atr_gt_2p2, tide_abs_gt206, bands, latch, eras) were computed at full precision before rounding.  An identity-law check must read the Trade objects (tierc11_books.v6_book / trg912_book), not re-derive from these tables.

**Stamps [L-R.5].** exit_event_ms is the exit's event stamp: a STOP exit is intrabar, stamped at its bar's OPEN (exit_event_stamp = 'intrabar_open'); a bell or corridor_end exit is stamped at its bar's close ('close').  exit_close_ms on an intrabar exit is the close-stamped twin — POST-EVENT.  latch_1r_open_ms (+1R, intrabar) is at its bar's OPEN.  window_end_i is the window end AS KNOWN at the as-of: an open window carries hi_i + 1, never a later bar.

## Readings built

- [LEAN-HEPHAESTUS] L-1.6 BASE v6 = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, CLASSIC5, lo, hi) over (lo, hi) = TP.corridor_n(CLASSIC5): the full TC11 corridor, hi + 1 == 1790294400000 (2026-09-25T00:00:00Z).
- [LEAN-HEPHAESTUS] L-1.6 9/12 = T9.replay9(s, TP.CONTROL_CARD, T9.SWEEP_CELLS[-1], lo, hi) per CLASSIC5 asset; SWEEP_CELLS[-1] must be Roles('trigger-9/12', trg_f=9, trg_s=12) or HALT; anchored by TP._book_sha over the TC10 window (hi + 1 = 2026-09-21T16:00:00Z) == P-TRG-2.scored.json full-arm book_sha256.
- [LEAN-HEPHAESTUS] L-1.7 F-CTRL(a) exact 0.000e+00 vs tierc6.run_cell(CARD_V6); F-CTRL(b) journal_frame(live) vs the filed TC10 control journal at 6 dp — closed campaigns exact on the 12 CTRL_COLS, corridor_end rows are continuations, entries after the TC10 pin listed as new.
- [LEAN-HEPHAESTUS] L-1.3 era = the entry bar's CLOSE (E.era_of(entry_close_ms)); tuning <= 2024-06-30T23:59:59Z; TP.in_era (bar OPEN) is not used; an entry bar straddling the cut is counted.
- [LEAN-HEPHAESTUS] L-G.1 tide age = tierc7_lab_regime.tide_streak at the ENTRY bar; band of record = trailing CLASSIC5 quartile edges over bars with open <= the entry bar (T9._trailing_edges, >= 30 bars), B4 OLD = streak >= trailing q75; shadow = streak > 206 as written; tierc9.tide_streak_age (arm bar) printed as disclosure.
- [LEAN-HEPHAESTUS] L-G.2 lag = entry_i - arm_i in 4h bars, bands 0 / 1-6 / 7-15 / >=16; L-G.3 r_over_atr = r_dist / ATR14_4h(entry), > 2.2 flagged.

## Anchors (held before any file was written)

| anchor | result |
|---|---|
| referees pinned by value | control_journal.parquet sha256 fcbf5db0480416b0… rows 200 == typed fcbf5db0480416b0… / 200; P-TRG-2 full arm b2276fa487119ef1… n 198 == typed b2276fa487119ef1… / 198; AS_OF_PIN.json close_ms 1790294400000 == 1790294400000 |
| F-CTRL(a) run_cell_n vs tierc6.run_cell(CARD_V6), TC11 corridor | n=200 worst=0.000e+00 exit_reasons_identical=True; window == TP.control_window(): True |
| F-CTRL(b) vs filed TC10 control_journal.parquet (sha256 fcbf5db0480416b0…, 70102 B) | filed 200 · live 200 · shared 200 · closed compared exact on 12 CTRL_COLS 199 · continuations 1 (entry/stop/r_dist exact; live exit bar opens at or after the TC10 pin; n_advances and mfe_r no smaller than filed) · new 0 |
| F-912-ANCHOR 9/12 over the TC10 window | TP._book_sha b2276fa487119ef12a8e0434e54f9b77efbfb7ee387b3cb35d2955043c371a8f n 198 == P-TRG-2 full arm b2276fa487119ef1… n 198 |
| F-912-ANCHOR base: v6 over the TC10 window | TP._book_sha 2bd244bfa0a1349ee73aa51e61619e3dda1257eafe3f613df4524a4d87909acd n 200 == the same arm's filed base_sha256 2bd244bfa0a1349e… |
| F-AGE-ANCHOR trailing bands, TC10 window | P_AGE_1_TIDE_YOUTH.parquet reproduced exactly (bands 01..04 + ALL) |
| trailing band prefix-stable | 200 TC10-window campaigns carry the same band in the TC11 table |

## Books

| book | n | ΣR (net) | mean R | win % | open at pin | book sha (TP._book_sha) | tier | selection_not_a_result | gates |
|---|---:|---:|---:|---:|---:|---|---|---|---|
| v6 | 200 | +40.8076 | +0.2040 | 34.50 | 0 | f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | 199 | +92.3184 | +0.4639 | 39.70 | 1 | 2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030 | TIER-E | a SELECTION, not a result | nothing |

### Per asset

| book | asset | n | ΣR | mean R | tier | selection_not_a_result | gates |
|---|---|---:|---:|---:|---|---|---|
| v6 | BTCUSDT | 39 | -4.9429 | -0.1267 | TIER-E | a SELECTION, not a result | nothing |
| v6 | ETHUSDT | 48 | +6.0656 | +0.1264 | TIER-E | a SELECTION, not a result | nothing |
| v6 | SOLUSDT | 36 | +9.7387 | +0.2705 | TIER-E | a SELECTION, not a result | nothing |
| v6 | NEARUSDT | 40 | -1.5676 | -0.0392 | TIER-E | a SELECTION, not a result | nothing |
| v6 | ZECUSDT | 37 | +31.5137 | +0.8517 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | BTCUSDT | 40 | +5.9142 | +0.1479 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | ETHUSDT | 48 | +20.5198 | +0.4275 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | SOLUSDT | 35 | +4.6823 | +0.1338 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | NEARUSDT | 39 | +8.2991 | +0.2128 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | ZECUSDT | 37 | +52.9031 | +1.4298 | TIER-E | a SELECTION, not a result | nothing |

### Per era (by the entry bar's CLOSE, L-1.3)

| book | era | n | ΣR | mean R | tier | selection_not_a_result | gates |
|---|---|---:|---:|---:|---|---|---|
| v6 | tuning | 123 | -1.3238 | -0.0108 | TIER-E | a SELECTION, not a result | nothing |
| v6 | holdout | 77 | +42.1314 | +0.5472 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | tuning | 132 | +23.4506 | +0.1777 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | holdout | 67 | +68.8678 | +1.0279 | TIER-E | a SELECTION, not a result | nothing |

- v6: entry bars straddling the era cut (open <= 2024-06-30T23:59:59Z < close): 0
- trg912: entry bars straddling the era cut (open <= 2024-06-30T23:59:59Z < close): 0

## Entered after the TC10 pin (entry close > 2026-09-21T16:00:00Z)

| book | asset | dir | entry (bar open) | exit (bar open) | exit_reason | net R | tier | selection_not_a_result | gates |
|---|---|---:|---|---|---|---:|---|---|---|
| v6 | (none) | | | | | | TIER-E | a SELECTION, not a result | nothing |
| trg912 | SOLUSDT | +1 | 2026-09-24T16:00:00Z | 2026-09-24T20:00:00Z | corridor_end | -0.031452 | TIER-E | a SELECTION, not a result | nothing |

## Continuations (entered at or before the TC10 pin, still open at it)

| book | asset | dir | entry (bar open) | exit now (bar open) | exit_reason | net R | tier | selection_not_a_result | gates |
|---|---|---:|---|---|---|---:|---|---|---|
| v6 | ETHUSDT | +1 | 2026-09-18T08:00:00Z | 2026-09-23T12:00:00Z | stop | +2.707180 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | (none) | | | | | | TIER-E | a SELECTION, not a result | nothing |

- v6 continuation vs the filed TC10 journal: ETHUSDT entered 2026-09-18T08:00:00Z — filed exit 2026-09-21T12:00:00Z corridor_end net +3.642965 · live exit 2026-09-23T12:00:00Z stop net +2.707180

## Counts (L-G.2 lag, L-G.3 structure distance, L-G.1 tide)

| book | lag 0 | lag 1-6 | lag 7-15 | lag >=16 | r_over_atr > 2.2 | B1 | B2 | B3 | B4 OLD | unbanded | streak > 206 (ABSOLUTE SHADOW, look-ahead) | left-censored | against tide at entry | tier | selection_not_a_result | gates |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| v6 | 52 | 81 | 4 | 63 | 53 | 25 | 60 | 56 | 59 | 0 | 120 | 4 | 0 | TIER-E | a SELECTION, not a result | nothing |
| trg912 | 43 | 32 | 7 | 117 | 59 | 22 | 54 | 61 | 62 | 0 | 125 | 5 | 0 | TIER-E | a SELECTION, not a result | nothing |

- **streak > 206 is L-G.1's ABSOLUTE SHADOW, printed as written: 206 is the whole-corridor MEDIAN edge, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4).**  Whole-corridor quartile edges of the pooled CLASSIC5 streak (LR.cuts, printed for the caveat only): TC10 window [88.0, 206.0, 396.0]; TC11 corridor [88.0, 206.0, 396.0].
- v6: tide streak at ENTRY (L-G.1 of record) median 249.0 bars; the arm-bar three-state age (tierc9.tide_streak_age, disclosure) median 97.0 bars, > 206 on 57; windows still open at the as-of 3; exits stamped intrabar_open 196 / close 4
- trg912: tide streak at ENTRY (L-G.1 of record) median 256.0 bars; the arm-bar three-state age (tierc9.tide_streak_age, disclosure) median 86.0 bars, > 206 on 56; windows still open at the as-of 2; exits stamped intrabar_open 191 / close 8

## Files

- `trg912_campaigns.parquet` content sha ff2b62cbebc657cdc57a6e80b9e393a5ed3b41633e499828de00525628f55fae (key ['symbol', 'entry_ms']; floats at 6 dp)
- `trg912_journal.parquet` content sha 42060018fbceee721fa76e271841b0f955b72adaa249ca93541936531d740536 (key ['asset', 'entry_ms']; floats at 6 dp)
- `v6_campaigns.parquet` content sha a5d0c57087c9b9bb95b61341e798b98eb41a8dc135d07c2eb279db8683ca96dd (key ['symbol', 'entry_ms']; floats at 6 dp)
- `v6_journal.parquet` content sha 5952563c9d8fdc689c37fe481aba00459762b3b54628b93b1ec6fe4c79414894 (key ['asset', 'entry_ms']; floats at 6 dp)
