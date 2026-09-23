# TIER-C10 · CLOSE · FORWARD STRIP

**REPORT-ONLY — FORWARD STRIP — NEVER SCORED.** TIER-C10 CLOSE item, contract of record `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`:114-115: the 5-asset v6 book from TC9's as-of to this corridor's end — printed, labelled, never scored. Counts and sums only: no CI, no p, no verdict, no LOAO, no FDR bar. No registration, score or verdict file was read to build it, and no kline file: every market number below is a column of the filed journal.

## The two as-ofs, as read from files this run

| as-of | value | read from |
|---|---|---|
| **TC9's as-of** (strip start) | `2026-08-22T00:00:00Z` (ms 1787356800000) | `research_outputs/tierc9/build_manifest.json` field `as_of` **and** `research_outputs/tierc9/trade_journal_control.parquet` column `as_of_last_closed_4h` (196 rows, 1 distinct value): equal |
| **this corridor's end** (strip end) | `2026-09-21T16:00:00Z` (last closed 4h bar, close ms 1790006400000) | `research_outputs/tierc10/PROGRESS.json` fields `as_of_of_record` and `as_of_last_closed_4h_close_ms`: agree with each other and with `research_outputs/tierc10/data/AS_OF_PIN.json` |
| contract literal (compared, never used) | `2026-08-22T00:00Z` | `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md`:115 (sha256 `8a0bf279bcab0f27…` == PROGRESS `contract_of_record`): equals TC9's as-of |

## Inputs

- **The book:** `research_outputs/tierc10/panel/control_journal.parquet`, sha256 `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c` == `research_outputs/tierc10/PROGRESS.json` stage `PANEL/gate` artifact_shas. 200 campaigns, panel `CLASSIC5`, 5 assets (BTCUSDT, ETHUSDT, NEARUSDT, SOLUSDT, ZECUSDT), lane `card`.
- **The anchor:** `research_outputs/tierc10/panel/FIXTURES_PANEL.txt` (sha256 `163f65bdf21a575c…` == the `PANEL/gate` record), line 35: F-CTRL/b lists 4 live-only campaign(s) against the filed tierc9 journal, all entered after the referee's last bar `2026-08-21T20:00:00Z`.

## Membership

- **ENTERED-IN-STRIP**: `entry_ms >= 1787356800000` (2026-08-22T00:00:00Z), 4 campaign(s).
- **CONTINUATION**: `entry_ms < 1787356800000 <= exit_ms`, 0 campaign(s). TC9's own journal carries 0 `corridor_end` row(s) (exit reasons {"bell_12_89": 4, "stop": 192}), so no v6 campaign was open at TC9's as-of.
- **OPEN-AT-CORRIDOR-END**: exit_reason `corridor_end`, marked to the pin, not realized: 1 campaign(s).
- Note: ETHUSDT long entered 2026-08-30T12:00:00Z was ARMED 2026-08-17T08:00:00Z, inside TC9's window. It is ENTERED-IN-STRIP by the entry predicate, and it is on F-CTRL/b's live-only list.

## The strip (REPORT-ONLY — FORWARD STRIP — NEVER SCORED)

R columns are verbatim from the journal (shortest round-trip repr). `net_r` is the TC-series accounting. `twin net_r` is the ADDED haircut twin.

| label | asset | dir | armed | entered | exited | exit_reason | bars | gross_r | fee_r | funding_r | net_r (TC-series) | twin net_r (ADDED) | twin tier |
|---|---|---|---|---|---|---|---:|---:|---:|---:|---:|---:|---|
| ENTERED-IN-STRIP / CLOSED — realized | ETHUSDT | long | 2026-08-17T08:00:00Z | 2026-08-30T12:00:00Z | 2026-08-30T20:00:00Z | stop | 2 | -1.0 | 0.029816 | 0.001248 | -1.031064 | -1.0417423396773202 | A |
| ENTERED-IN-STRIP / CLOSED — realized | BTCUSDT | long | 2026-09-14T16:00:00Z | 2026-09-14T16:00:00Z | 2026-09-14T20:00:00Z | stop | 1 | -1.0 | 0.10553 | 0.0 | -1.10553 | -1.1477424601980053 | A |
| ENTERED-IN-STRIP / CLOSED — realized | SOLUSDT | long | 2026-09-18T00:00:00Z | 2026-09-18T00:00:00Z | 2026-09-20T00:00:00Z | stop | 12 | 1.498796 | 0.032033 | 0.019861 | 1.446902 | 1.4347296114580608 | B |
| ENTERED-IN-STRIP / OPEN-AT-CORRIDOR-END — marked to the pin, not realized | ETHUSDT | long | 2026-09-18T08:00:00Z | 2026-09-18T08:00:00Z | 2026-09-21T12:00:00Z | corridor_end | 19 | 3.710075 | 0.039565 | 0.027544 | 3.642965 | 3.654683918882855 | A |

## Footer: counts and sums only (REPORT-ONLY — FORWARD STRIP — NEVER SCORED)

Sums are `math.fsum` over the rows above, printed to 6 dp. The rows are verbatim.

| subset | n | Σ gross_r | Σ fee_r | Σ funding_r | Σ net_r (TC-series) | Σ twin net_r (ADDED) |
|---|---:|---:|---:|---:|---:|---:|
| all rows | 4 | +3.208871 | +0.206944 | +0.048653 | +2.953273 | +2.899929 |
| ENTERED-IN-STRIP | 4 | +3.208871 | +0.206944 | +0.048653 | +2.953273 | +2.899929 |
| CONTINUATION | 0 | +0.000000 | +0.000000 | +0.000000 | +0.000000 | +0.000000 |
| CLOSED (realized) | 3 | -0.501204 | +0.167379 | +0.021109 | -0.689692 | -0.754755 |
| OPEN-AT-CORRIDOR-END (marked, not realized) | 1 | +3.710075 | +0.039565 | +0.027544 | +3.642965 | +3.654684 |

| asset | campaigns in strip |
|---|---:|
| BTCUSDT | 1 |
| ETHUSDT | 2 |
| NEARUSDT | 0 |
| SOLUSDT | 1 |
| ZECUSDT | 0 |

## Notes

- `net_r` is the TC-series row of record, carried verbatim. On these rows max |net_r − (gross_r − fee_r − funding_r)| = 1.000e-06. Every R value on these rows is a 6-dp figure, so a residue of up to 1e-6 is rounding in the journal as filed.
- The haircut twin is `tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px, exit_px, r_dist)["net_r_twin"]`. It is gross_r less (taker fee + charter slippage per side) × (entry_px + exit_px) / r_dist, with the stem mapped to the contract asset by the filed Stage D venue table. The filed function charges NO funding, so twin − net_r is not a pure slippage delta. It is an ADDED column and gates nothing.
- An OPEN-AT-CORRIDOR-END row is the journal's own mark at the pinned bar. Its gross_r, fee_r, funding_r, net_r and twin are not realized.
- Every as_of_* column and `warranty` is carried verbatim from the journal. Every row is stamped `as_of_last_closed_4h` = `2026-09-21T16:00:00Z`.
- This strip is not a verdict. It is a printed window of the control book.
