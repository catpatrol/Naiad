# REGIME-PRIOR — Tier-E tables (TIER-C10 · CLOSE)

> **TIER-E · REPORT-ONLY · a SELECTION, not a result · gates: nothing · in-sample.** No row below is a test. Neither table has a verdict, CI or p column; no registration and no verdict was read to build them; no cell may be promoted to a lane. m is logged on every row so a reader who later turns a cell into a claim can see how many ways the tape was cut first.

## Why this exists

The contract of record names the item and its form (`exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` line 113; sha256 `8a0bf279bcab0f27161a7d965535445807f4e713e77d045b0ba124bc7f803c7a`, equal to PROGRESS.json `contract_of_record`):

```
  P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only.
```

## The prior, quoted whole

`exchange/reports/NOTE_ARGUS_to_APOLLO_2026-08-22_P-RNG_slate.md` (sha256 `77dda285376a934f8f2dbcc356d3c00f33707c2775b4ebf1c993ebbc7c06e807`; git blob `0eda2821baf34ed97d816c56dd9e1512e6d85a0c`, equal to the committed blob at HEAD), item 2, verbatim:

> 2. **The regime prior**: the reference system's own thesis stat — ~80% of BTC daily time in-range — offered as a REGIME PRIOR for exit studies, not as a rule; our window measures 60.0% under the v0 reconstruction, resistance disclosed.

It is quoted, never parsed: nothing in this build reads a number out of it, no row of either table is compared with it, and neither table carries a column derived from it (F-RP-QUOTE holds Table 1's column set to the declared one).

## Inputs

Read-only. Each sha256 was held against its PROGRESS.json stage record before the file was read.

| input | PROGRESS stage | sha256 | rows |
|---|---|---|---|
| `research_outputs/tierc10/census/coverage.parquet` | CENSUS-R{4h,1d} | `f126eb24906ad27463cc68d99b3ef88edec55684f3b6d0c6af513cc94422677e` | 102 |
| `research_outputs/tierc10/stamps/control_v6_stamped.parquet` | A (stamps) | `6b5649b534d73a49469fac2cb5d41ada64571d4ed95e0d7c37a895ad6e5a6f20` | 5745 |
| `research_outputs/tierc10/stamps/control_entry_by_state.parquet` | A (stamps) | `e8a5df1cc233c6308907546373b1a3a6007279704c960a2b1a274a202ed27d47` | 5 |
| `research_outputs/tierc10/stamps/build_manifest.json` | A (stamps) | `026d80135ccaae1fa82953449a5b6c98c0e5aa455ede37a56f9a796106c46849` | (json) |
| `research_outputs/tierc10/panel/control_journal.parquet` | PANEL/gate | `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c` | 200 |

No bar is read by this build. Both tables are made from filed parquet; none of `tierc2_baseline`, `tierc10_data`, `tierc10_census`, `tierc10_panel`, `engine.data` is imported (the build checks `sys.modules` before it writes) and no kline file is opened.

## Table 1 — time-in-range per asset × lens × scale_kind

`close/REGIME_PRIOR_TIME_IN_RANGE.parquet` (sha256 `a2c3ed8e42e464c6b8bcd91b85788a2656ff11b1868dec7cdd5741e3f1034f8d`): 102 rows = 17 assets × 3 lenses × 2 scale kinds, copied verbatim from `census/coverage.parquet` (F-RP-VERBATIM holds every copied value exact). No new pooling: nothing is averaged, summed or ranked across assets, lenses or scale kinds.

Column laws:

- `coverage_pct`: close inside the alive CONFIRMED macro range's span (boundaries + deviation zones), % of ALL bars (the census's `coverage_law`, verbatim).
- `bars_in_live_range_pct`: bars_in_live_range_pct = 100 x the share of ALL bars of the tape at which a CONFIRMED macro range is alive in the census as-of view (confirm_i <= t < die_i; `in_range` of tierc10_census.asof_view, written by tierc10_census.compute_cell). coverage_pct follows its own coverage_law, copied verbatim on this row. Both are the census's numbers, not this build's.

### 5m · calibrated

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 2.0 | 297816 | 48.26 | 51.03318828 | 2023-11-22T14:00:00Z | 2026-09-21T16:00:00Z |
| 1000PEPEUSDT | 1.75 | 355674 | 56.73 | 59.55734746 | 2023-05-05T16:30:00Z | 2026-09-21T16:00:00Z |
| BNBUSDT | 2.0 | 695616 | 49.64 | 52.27999356 | 2020-02-10T08:00:00Z | 2026-09-21T16:00:00Z |
| BTCUSDT | 1.75 | 740137 | 60.62 | 63.08980635 | 2019-09-08T17:55:00Z | 2026-09-21T16:00:00Z |
| DOGEUSDT | 1.75 | 652116 | 59.07 | 61.80280809 | 2020-07-10T09:00:00Z | 2026-09-21T16:00:00Z |
| ENAUSDT | 1.75 | 259818 | 52.28 | 55.70283814 | 2024-04-02T12:30:00Z | 2026-09-21T16:00:00Z |
| ETHUSDT | 1.75 | 717219 | 59.94 | 62.31904063 | 2019-11-27T07:45:00Z | 2026-09-21T16:00:00Z |
| HYPEUSDT | 2.0 | 138018 | 50.93 | 53.97919112 | 2025-05-30T10:30:00Z | 2026-09-21T16:00:00Z |
| LTCUSDT | 1.75 | 704831 | 57.69 | 60.72264131 | 2020-01-09T08:05:00Z | 2026-09-21T16:00:00Z |
| MNTUSDT_BYBIT | 2.0 | 312593 | 47.58 | 50.17130902 | 2023-10-02T06:35:00Z | 2026-09-21T16:00:00Z |
| NEARUSDT | 1.75 | 624192 | 54.06 | 57.38971342 | 2020-10-15T08:00:00Z | 2026-09-21T16:00:00Z |
| PUMPUSDT | 2.0 | 126246 | 47.82 | 50.60120717 | 2025-07-10T07:30:00Z | 2026-09-21T16:00:00Z |
| SOLUSDT | 1.75 | 633132 | 53.35 | 56.56956211 | 2020-09-14T07:00:00Z | 2026-09-21T16:00:00Z |
| SUIUSDT | 1.75 | 356256 | 53.87 | 57.16058116 | 2023-05-03T16:00:00Z | 2026-09-21T16:00:00Z |
| UNIUSDT | 1.75 | 631980 | 54.19 | 57.58109434 | 2020-09-18T07:00:00Z | 2026-09-21T16:00:00Z |
| XMRUSDT | 1.75 | 697632 | 56.66 | 60.33682515 | 2020-02-03T08:00:00Z | 2026-09-21T16:00:00Z |
| ZECUSDT | 1.75 | 697056 | 55.33 | 58.53962953 | 2020-02-05T08:00:00Z | 2026-09-21T16:00:00Z |

### 5m · frozen3.0

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 3.0 | 297816 | 38.89 | 40.33900126 | 2023-11-22T14:00:00Z | 2026-09-21T16:00:00Z |
| 1000PEPEUSDT | 3.0 | 355674 | 43.92 | 45.10506812 | 2023-05-05T16:30:00Z | 2026-09-21T16:00:00Z |
| BNBUSDT | 3.0 | 695616 | 39.78 | 41.11765687 | 2020-02-10T08:00:00Z | 2026-09-21T16:00:00Z |
| BTCUSDT | 3.0 | 740137 | 45.84 | 46.8917241 | 2019-09-08T17:55:00Z | 2026-09-21T16:00:00Z |
| DOGEUSDT | 3.0 | 652116 | 45.59 | 46.70564746 | 2020-07-10T09:00:00Z | 2026-09-21T16:00:00Z |
| ENAUSDT | 3.0 | 259818 | 39.4 | 40.88862204 | 2024-04-02T12:30:00Z | 2026-09-21T16:00:00Z |
| ETHUSDT | 3.0 | 717219 | 42.73 | 43.8230164 | 2019-11-27T07:45:00Z | 2026-09-21T16:00:00Z |
| HYPEUSDT | 3.0 | 138018 | 40.82 | 42.5256126 | 2025-05-30T10:30:00Z | 2026-09-21T16:00:00Z |
| LTCUSDT | 3.0 | 704831 | 43.45 | 44.78236627 | 2020-01-09T08:05:00Z | 2026-09-21T16:00:00Z |
| MNTUSDT_BYBIT | 3.0 | 312593 | 39.01 | 40.42221035 | 2023-10-02T06:35:00Z | 2026-09-21T16:00:00Z |
| NEARUSDT | 3.0 | 624192 | 41.72 | 43.1578745 | 2020-10-15T08:00:00Z | 2026-09-21T16:00:00Z |
| PUMPUSDT | 3.0 | 126246 | 34.81 | 36.22530615 | 2025-07-10T07:30:00Z | 2026-09-21T16:00:00Z |
| SOLUSDT | 3.0 | 633132 | 39.51 | 40.80902561 | 2020-09-14T07:00:00Z | 2026-09-21T16:00:00Z |
| SUIUSDT | 3.0 | 356256 | 40.69 | 42.11802749 | 2023-05-03T16:00:00Z | 2026-09-21T16:00:00Z |
| UNIUSDT | 3.0 | 631980 | 40.05 | 41.51539606 | 2020-09-18T07:00:00Z | 2026-09-21T16:00:00Z |
| XMRUSDT | 3.0 | 697632 | 45.57 | 47.17415486 | 2020-02-03T08:00:00Z | 2026-09-21T16:00:00Z |
| ZECUSDT | 3.0 | 697056 | 41.15 | 42.52556466 | 2020-02-05T08:00:00Z | 2026-09-21T16:00:00Z |

### 4h · calibrated

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 1.75 | 6205 | 49.36 | 53.29572925 | 2023-11-22T12:00:00Z | 2026-09-21T16:00:00Z |
| 1000PEPEUSDT | 1.75 | 7410 | 47.41 | 50.44534413 | 2023-05-05T16:00:00Z | 2026-09-21T16:00:00Z |
| BNBUSDT | 1.75 | 14492 | 55.52 | 58.21832735 | 2020-02-10T08:00:00Z | 2026-09-21T16:00:00Z |
| BTCUSDT | 2.0 | 15420 | 46.6 | 49.05966278 | 2019-09-08T16:00:00Z | 2026-09-21T16:00:00Z |
| DOGEUSDT | 1.75 | 13586 | 63.76 | 65.76622994 | 2020-07-10T08:00:00Z | 2026-09-21T16:00:00Z |
| ENAUSDT | 2.25 | 5413 | 39.0 | 41.36338444 | 2024-04-02T12:00:00Z | 2026-09-21T16:00:00Z |
| ETHUSDT | 2.0 | 14943 | 44.32 | 46.59706886 | 2019-11-27T04:00:00Z | 2026-09-21T16:00:00Z |
| HYPEUSDT | 1.75 | 2876 | 47.6 | 52.01668985 | 2025-05-30T08:00:00Z | 2026-09-21T16:00:00Z |
| LTCUSDT | 2.0 | 14684 | 45.55 | 47.86842822 | 2020-01-09T08:00:00Z | 2026-09-21T16:00:00Z |
| MNTUSDT_BYBIT | 2.0 | 6513 | 38.91 | 40.82604023 | 2023-10-02T04:00:00Z | 2026-09-21T16:00:00Z |
| NEARUSDT | 2.0 | 13004 | 42.51 | 45.50907413 | 2020-10-15T08:00:00Z | 2026-09-21T16:00:00Z |
| PUMPUSDT | 2.25 | 2631 | 22.01 | 24.43937666 | 2025-07-10T04:00:00Z | 2026-09-21T16:00:00Z |
| SOLUSDT | 2.0 | 13191 | 43.84 | 46.15267986 | 2020-09-14T04:00:00Z | 2026-09-21T16:00:00Z |
| SUIUSDT | 1.75 | 7422 | 52.6 | 55.21422797 | 2023-05-03T16:00:00Z | 2026-09-21T16:00:00Z |
| UNIUSDT | 2.0 | 13167 | 51.04 | 53.21637427 | 2020-09-18T04:00:00Z | 2026-09-21T16:00:00Z |
| XMRUSDT | 1.5 | 14534 | 68.66 | 72.01733865 | 2020-02-03T08:00:00Z | 2026-09-21T16:00:00Z |
| ZECUSDT | 2.0 | 14522 | 42.36 | 45.12463848 | 2020-02-05T08:00:00Z | 2026-09-21T16:00:00Z |

### 4h · frozen3.0

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 3.0 | 6205 | 40.34 | 41.28928284 | 2023-11-22T12:00:00Z | 2026-09-21T16:00:00Z |
| 1000PEPEUSDT | 3.0 | 7410 | 42.55 | 43.81916329 | 2023-05-05T16:00:00Z | 2026-09-21T16:00:00Z |
| BNBUSDT | 3.0 | 14492 | 46.8 | 47.89539056 | 2020-02-10T08:00:00Z | 2026-09-21T16:00:00Z |
| BTCUSDT | 3.0 | 15420 | 29.98 | 31.23216602 | 2019-09-08T16:00:00Z | 2026-09-21T16:00:00Z |
| DOGEUSDT | 3.0 | 13586 | 43.01 | 43.94229354 | 2020-07-10T08:00:00Z | 2026-09-21T16:00:00Z |
| ENAUSDT | 3.0 | 5413 | 25.01 | 26.41788287 | 2024-04-02T12:00:00Z | 2026-09-21T16:00:00Z |
| ETHUSDT | 3.0 | 14943 | 33.21 | 34.15646122 | 2019-11-27T04:00:00Z | 2026-09-21T16:00:00Z |
| HYPEUSDT | 3.0 | 2876 | 25.7 | 27.39916551 | 2025-05-30T08:00:00Z | 2026-09-21T16:00:00Z |
| LTCUSDT | 3.0 | 14684 | 40.99 | 42.27730864 | 2020-01-09T08:00:00Z | 2026-09-21T16:00:00Z |
| MNTUSDT_BYBIT | 3.0 | 6513 | 33.67 | 34.79195455 | 2023-10-02T04:00:00Z | 2026-09-21T16:00:00Z |
| NEARUSDT | 3.0 | 13004 | 29.72 | 31.22116272 | 2020-10-15T08:00:00Z | 2026-09-21T16:00:00Z |
| PUMPUSDT | 3.0 | 2631 | 37.13 | 37.59026986 | 2025-07-10T04:00:00Z | 2026-09-21T16:00:00Z |
| SOLUSDT | 3.0 | 13191 | 32.68 | 34.00045486 | 2020-09-14T04:00:00Z | 2026-09-21T16:00:00Z |
| SUIUSDT | 3.0 | 7422 | 36.12 | 37.52357855 | 2023-05-03T16:00:00Z | 2026-09-21T16:00:00Z |
| UNIUSDT | 3.0 | 13167 | 37.6 | 38.71800714 | 2020-09-18T04:00:00Z | 2026-09-21T16:00:00Z |
| XMRUSDT | 3.0 | 14534 | 48.95 | 50.04816293 | 2020-02-03T08:00:00Z | 2026-09-21T16:00:00Z |
| ZECUSDT | 3.0 | 14522 | 32.42 | 33.59730065 | 2020-02-05T08:00:00Z | 2026-09-21T16:00:00Z |

### 1d · calibrated

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 2.0 | 1033 | 52.57 | 56.4375605 | 2023-11-23T00:00:00Z | 2026-09-21T00:00:00Z |
| 1000PEPEUSDT | 2.25 | 1234 | 30.06 | 30.87520259 | 2023-05-06T00:00:00Z | 2026-09-21T00:00:00Z |
| BNBUSDT | 2.0 | 2414 | 57.29 | 59.15492958 | 2020-02-11T00:00:00Z | 2026-09-21T00:00:00Z |
| BTCUSDT | 2.25 | 2569 | 33.79 | 35.53912028 | 2019-09-09T00:00:00Z | 2026-09-21T00:00:00Z |
| DOGEUSDT | 2.25 | 2263 | 38.62 | 40.38886434 | 2020-07-11T00:00:00Z | 2026-09-21T00:00:00Z |
| ENAUSDT | 2.0 | 901 | 20.53 | 24.97225305 | 2024-04-03T00:00:00Z | 2026-09-21T00:00:00Z |
| ETHUSDT | 2.0 | 2489 | 31.62 | 34.55202893 | 2019-11-28T00:00:00Z | 2026-09-21T00:00:00Z |
| HYPEUSDT | 2.25 | 478 | 19.04 | 21.9665272 | 2025-05-31T00:00:00Z | 2026-09-21T00:00:00Z |
| LTCUSDT | 2.25 | 2446 | 27.56 | 29.47669665 | 2020-01-10T00:00:00Z | 2026-09-21T00:00:00Z |
| MNTUSDT_BYBIT | 2.0 | 1084 | 34.41 | 35.97785978 | 2023-10-03T00:00:00Z | 2026-09-21T00:00:00Z |
| NEARUSDT | 2.0 | 2166 | 34.26 | 37.16528163 | 2020-10-16T00:00:00Z | 2026-09-21T00:00:00Z |
| PUMPUSDT | 1.75 | 437 | 47.14 | 50.80091533 | 2025-07-11T00:00:00Z | 2026-09-21T00:00:00Z |
| SOLUSDT | 2.5 | 2197 | 20.21 | 21.71142467 | 2020-09-15T00:00:00Z | 2026-09-21T00:00:00Z |
| SUIUSDT | 2.5 | 1236 | 23.95 | 24.43365696 | 2023-05-04T00:00:00Z | 2026-09-21T00:00:00Z |
| UNIUSDT | 2.25 | 2193 | 50.75 | 52.71317829 | 2020-09-19T00:00:00Z | 2026-09-21T00:00:00Z |
| XMRUSDT | 1.5 | 2421 | 62.78 | 65.79925651 | 2020-02-04T00:00:00Z | 2026-09-21T00:00:00Z |
| ZECUSDT | 2.5 | 2419 | 31.05 | 32.5754444 | 2020-02-06T00:00:00Z | 2026-09-21T00:00:00Z |

### 1d · frozen3.0

| asset | scale_mult | n_bars | coverage_pct | bars_in_live_range_pct | as_of_panel_start | as_of_last_closed_bar |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 3.0 | 1033 | 52.27 | 55.46950629 | 2023-11-23T00:00:00Z | 2026-09-21T00:00:00Z |
| 1000PEPEUSDT | 3.0 | 1234 | 28.36 | 29.57860616 | 2023-05-06T00:00:00Z | 2026-09-21T00:00:00Z |
| BNBUSDT | 3.0 | 2414 | 32.56 | 32.93289147 | 2020-02-11T00:00:00Z | 2026-09-21T00:00:00Z |
| BTCUSDT | 3.0 | 2569 | 36.05 | 36.86259245 | 2019-09-09T00:00:00Z | 2026-09-21T00:00:00Z |
| DOGEUSDT | 3.0 | 2263 | 25.76 | 26.99955811 | 2020-07-11T00:00:00Z | 2026-09-21T00:00:00Z |
| ENAUSDT | 3.0 | 901 | 23.53 | 24.08435072 | 2024-04-03T00:00:00Z | 2026-09-21T00:00:00Z |
| ETHUSDT | 3.0 | 2489 | 15.79 | 16.6733628 | 2019-11-28T00:00:00Z | 2026-09-21T00:00:00Z |
| HYPEUSDT | 3.0 | 478 | 1.67 | 1.88284519 | 2025-05-31T00:00:00Z | 2026-09-21T00:00:00Z |
| LTCUSDT | 3.0 | 2446 | 23.39 | 24.57072772 | 2020-01-10T00:00:00Z | 2026-09-21T00:00:00Z |
| MNTUSDT_BYBIT | 3.0 | 1084 | 47.6 | 48.33948339 | 2023-10-03T00:00:00Z | 2026-09-21T00:00:00Z |
| NEARUSDT | 3.0 | 2166 | 37.12 | 39.33518006 | 2020-10-16T00:00:00Z | 2026-09-21T00:00:00Z |
| PUMPUSDT | 3.0 | 437 | 17.39 | 18.76430206 | 2025-07-11T00:00:00Z | 2026-09-21T00:00:00Z |
| SOLUSDT | 3.0 | 2197 | 23.62 | 24.80655439 | 2020-09-15T00:00:00Z | 2026-09-21T00:00:00Z |
| SUIUSDT | 3.0 | 1236 | 30.02 | 30.82524272 | 2023-05-04T00:00:00Z | 2026-09-21T00:00:00Z |
| UNIUSDT | 3.0 | 2193 | 45.19 | 46.10123119 | 2020-09-19T00:00:00Z | 2026-09-21T00:00:00Z |
| XMRUSDT | 3.0 | 2421 | 50.31 | 50.64023131 | 2020-02-04T00:00:00Z | 2026-09-21T00:00:00Z |
| ZECUSDT | 3.0 | 2419 | 45.35 | 46.13476643 | 2020-02-06T00:00:00Z | 2026-09-21T00:00:00Z |

`in_sample`, verbatim from the census, by scale kind:

- calibrated: IN-SAMPLE BY CONSTRUCTION: SCALE fitted on this whole tape; no registered lane and no Stage-A stamp may read it [L2]
- frozen3.0: full history, frozen pins: descriptive of THIS tape; pins were calibrated on BTC only

## Table 2 — the v6 CLASSIC5 book by rf4h macro state at entry × at exit

`close/REGIME_PRIOR_V6_BY_STATE.parquet` (sha256 `ad7bed5953f4418a08168aaebc2e152bc4caa349c9fa86d59bb2b74db6984c41`). Book: card v6 · V6_ROLES · CLASSIC5 — panel/control_journal.parquet, 200 campaigns on BTCUSDT, ETHUSDT, NEARUSDT, SOLUSDT, ZECUSDT. States: the Stage-A stamps (`stamps/control_v6_stamped.parquet`) on lens `4h` at SCALE_MULT 3.0 (`stamps/build_manifest.json`). The entry stamp joins on (asset, instant_ms == entry_ms, instant_kind = 'entry'); the exit stamp joins on the same campaign_id with instant_kind = 'exit' (F-RP-JOIN). net_r is the journal's.

The declared grid is whole: 64 cells (4 states × 2 in_range values at entry × the same at exit) are filed, zeros included. 8 are non-empty and printed here; the other 56 are n = 0. Cells with n < 30 are flagged provisional (the lineage's PROVISIONAL_MIN_N, read from `scripts/tierc10_census.py`).

| entry state | entry in_range | exit state | exit in_range | n | n_assets | net_r_sum | expectancy_r | win_rate_pct | provisional |
|---|---|---|---|---|---|---|---|---|---|
| NEUTRAL | True | NEUTRAL | True | 68 | 5 | -31.751314 | -0.466931 | 17.647059 |  |
| NEUTRAL | True | BULL_EXP | False | 13 | 4 | 28.876722 | 2.221286 | 100.0 | yes |
| NEUTRAL | True | BEAR_EXP | False | 13 | 5 | 30.75934 | 2.366103 | 76.923077 | yes |
| BULL_EXP | False | NEUTRAL | True | 11 | 4 | -6.126051 | -0.556914 | 18.181818 | yes |
| BULL_EXP | False | BULL_EXP | False | 54 | 5 | 19.939913 | 0.369258 | 29.62963 |  |
| BULL_EXP | False | BEAR_EXP | False | 1 | 1 | 0.695742 | 0.695742 | 100.0 | yes |
| BEAR_EXP | False | NEUTRAL | True | 4 | 3 | 2.595786 | 0.648947 | 100.0 | yes |
| BEAR_EXP | False | BEAR_EXP | False | 36 | 5 | -3.246787 | -0.090189 | 30.555556 |  |

Entry-state marginal — equal on n, net_r_sum, expectancy_r and win_rate_pct to `stamps/control_entry_by_state.parquet` (F-RP-ANCHOR):

| cut | entry state | n | n_assets | net_r_sum | expectancy_r | win_rate_pct | provisional |
|---|---|---|---|---|---|---|---|
| ENTRY_STATE_MARGINAL | NONE | 0 | 0 | — | — | — | yes |
| ENTRY_STATE_MARGINAL | NEUTRAL | 94 | 5 | 27.884748 | 0.296646 | 37.234043 |  |
| ENTRY_STATE_MARGINAL | BULL_EXP | 66 | 5 | 14.509604 | 0.219842 | 28.787879 |  |
| ENTRY_STATE_MARGINAL | BEAR_EXP | 40 | 5 | -0.651001 | -0.016275 | 37.5 |  |
| ALL | __ALL__ | 200 | 5 | 41.743351 | 0.208717 | 34.5 |  |

Exit-state marginal:

| cut | exit state | n | n_assets | net_r_sum | expectancy_r | win_rate_pct | provisional |
|---|---|---|---|---|---|---|---|
| EXIT_STATE_MARGINAL | NONE | 0 | 0 | — | — | — | yes |
| EXIT_STATE_MARGINAL | NEUTRAL | 83 | 5 | -35.281579 | -0.425079 | 21.686747 |  |
| EXIT_STATE_MARGINAL | BULL_EXP | 67 | 5 | 48.816635 | 0.728606 | 43.283582 |  |
| EXIT_STATE_MARGINAL | BEAR_EXP | 50 | 5 | 28.208295 | 0.564166 | 44.0 |  |
| ALL | __ALL__ | 200 | 5 | 41.743351 | 0.208717 | 34.5 |  |

Disclosures (counted from the joined rows, not assumed):

- entry: rf4h_in_range == (macro_state == 'NEUTRAL') on 200/200 campaigns — the stamps' four-valued collapse [LEAN S-a] makes NEUTRAL mean a confirmed range is alive, so the in_range columns repeat the state here; they are carried as specified.
- exit: rf4h_in_range == (macro_state == 'NEUTRAL') on 200/200 campaigns — the stamps' four-valued collapse [LEAN S-a] makes NEUTRAL mean a confirmed range is alive, so the in_range columns repeat the state here; they are carried as specified.
- exit stamp bar lag (4h bars): 0: 200; exit instant_ms == journal exit_ms on 200/200.
- campaigns whose exit state equals their entry state: 158/200 (a count of the diagonal cells above, not a statistic).

## The collar, as filed on every row of both tables

- `tier`: Table 1 carries the census's own, verbatim (TIER-E MEASUREMENT — UNSCORED, GATES NOTHING); Table 2: TIER-E MEASUREMENT — UNSCORED, GATES NOTHING
- `selection_not_a_result`: a SELECTION, not a result — report-only; no row here is a test, a verdict or a lane, and no cell may be promoted to one
- `m_selections_this_table`: Table 1 102, Table 2 73 (every row is one cut)
- `in_sample`: Table 1 the census's, verbatim (above); Table 2: IN-SAMPLE: the KNOWN CONTROL (card v6, frozen pins, CLASSIC5) over the full corridor — ridden by nine tiers; the stamps are new, the book is not
- `gates`: nothing

## Fixtures

`scripts/tierc10_close_regime_prior_fixtures.py` → `close/FIXTURES_CLOSE_regime_prior.txt`. Legs: F-RP-SHA · F-RP-JOIN · F-RP-ANCHOR · F-RP-VERBATIM · F-RP-EXIT-ASOF · F-RP-COLLAR · F-RP-QUOTE · F-DET. Each states FAILS IF and carries a sabotage that must go RED. The build itself runs the same checks as HALT gates before it writes a byte.
