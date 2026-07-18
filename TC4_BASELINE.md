# TC-4 BASELINE — engine 1.0.8 re-anchor (v12 study, new baseline)

Engine **1.0.8** · config **v12_anchor_g8** (sha256 `97c24125310a5a58…`) · grid evidence hash `6c00f9b44d32a9d4…` · determinism double-run ALL IDENTICAL · bootstrap seed 20260718, 10000 resamples, campaign-level.

**Supersedes** journal_pass1 (engine 1.0.7 / v12_anchor); pass 1 retained read-only.

## Headline (scored 20-cell grid)

- Grid net R (1×): **-1796.993** over 2599 campaigns (pass 1: -5756.9093 over 3456)
- Expectancy (1×): **-0.6914 R/campaign**, CI95 [-0.8148, -0.5466]
- 0× (gross) 275.9924 · 2× (stress) -3869.9784 — the cost stack still decides the sign
- Win rate: **10.8503%** (pass-1 clean reference 11.28%)
- Strip-best: -1911.4449 (best campaign +114.4519)
- Tranches: 6304 total / 6279 resolved (pass 1: 8387)

## Fixtures (9/9 MATCH)

| # | result |
|---|---|
| F-SIG | MATCH — `{"rows_pass1": 967736, "rows_pass2": 967736, "mismatched_cells": [], "residual_is_config_id_only": true}` |
| F-G8a | MATCH — `{"violations": 0}` |
| F-G8b | MATCH — `{"max_notional_leverage": 9.186393, "worst_cell": "BTCUSDT_intraday", "fills_without_exit_row": 25}` |
| F-G8c | MATCH — `{"fills": 6304, "min_stop_dist_atr": 0.501208, "worst": ["BTCUSDT_position", "2024-02-07T17:00:00Z"]}` |
| F-G8d | MATCH — `{"tranches_one_r_le_0": 0, "pass1_reference": 717}` |
| F-EQ | MATCH — `{"min_equity": 2491.34, "worst": ["ETHUSDT_intraday", "2022-07-15T06:52:00Z"], "pass1_reference": -2732.24}` |
| F-CLS | MATCH — `{"census": {"r1": 2456, "true_add": 888, "re_entry": 2928, "v": 32}, "total_fills": 6304, "census_sum": 6304, "violations": 0}` |
| F-EXT | MATCH — `{"exit_rows_flagged": 1041, "violations": 0}` |
| F-DET | MATCH — `{"cells": 20, "mismatched": [], "manifest_flag": true}` |

## Prediction scorecard

| # | prior | verdict | measured |
|---|---|---|---|
| P-TC4a | 85% | **CONFIRMED** | `{"halt_set": ["BTCUSDT_intraday", "ETHUSDT_intraday", "NEARUSDT_intraday", "SOLUSDT_intraday", "ZECUSDT_intraday"], "halt_dates": {"BTCUSDT_intraday": "2022-04-11", "ETHUSDT_intraday": "2022-07-15", "` |
| P-TC4a' | 50% | **FALSIFIED** | `{"zec_swing_halted": false, "note": "registered as a genuine coin flip"}` |
| P-TC4b | 65% | **CONFIRMED** | `{"band": [-2400.0, -800.0], "grid_sum_1x": -1796.993}` |
| P-TC4c | 60% | **CONFIRMED** | `{"band": [1900, 2700], "campaigns": 2599}` |
| P-TC4d | 65% | **FALSIFIED** | `{"threshold_pct": 11.0, "win_rate_pct": 10.8503}` |

## Halt table (equity floor, permanent)

| cell | floor halt | equity at breach | final equity |
|---|---|---|---|
| BTCUSDT_intraday | 2022-04-11T06:04:00Z | 2493.124116 | 2493.12 |
| ETHUSDT_intraday | 2022-07-15T06:52:00Z | 2491.335373 | 2491.34 |
| NEARUSDT_intraday | 2023-01-21T10:26:00Z | 2499.932865 | 2499.93 |
| SOLUSDT_intraday | 2023-04-28T00:10:00Z | 2498.458544 | 2498.46 |
| ZECUSDT_intraday | 2022-06-01T23:47:00Z | 2492.123061 | 2492.12 |

## 0×/1×/2× by mandate and asset (campaign-level)

| slice | campaigns | 0× | 1× | 2× | expectancy 1× [CI95] | win | strip-best 1× | best |
|---|---|---|---|---|---|---|---|---|
| GRID | 2599 | 275.9924 | -1796.993 | -3869.9784 | -0.6914 [-0.8148, -0.5466] | 10.8503% | -1911.4449 | 114.4519 |
| swing | 754 | 178.3664 | -282.1248 | -742.616 | -0.3742 [-0.6713, 0.0217] | 12.8647% | -396.5767 | 114.4519 |
| intraday | 1634 | 97.6967 | -1441.073 | -2979.8427 | -0.8819 [-1.0055, -0.7529] | 9.3635% | -1482.1857 | 41.1127 |
| position | 211 | -0.0707 | -73.7952 | -147.5197 | -0.3497 [-0.6789, 0.1035] | 15.1659% | -109.9354 | 36.1402 |
| BTCUSDT | 507 | 264.8508 | -259.4408 | -783.7324 | -0.5117 [-0.9684, 0.1262] | 11.2426% | -373.8926 | 114.4519 |
| ETHUSDT | 519 | 58.6988 | -365.4655 | -789.6298 | -0.7042 [-0.9379, -0.4332] | 10.9827% | -399.8369 | 34.3715 |
| JTOUSDT | 78 | -13.9439 | -66.1859 | -118.428 | -0.8485 [-1.1105, -0.5554] | 11.5385% | -71.3559 | 5.17 |
| NEARUSDT | 474 | 18.2818 | -302.1031 | -622.488 | -0.6373 [-0.8467, -0.4001] | 11.1814% | -325.8717 | 23.7686 |
| SOLUSDT | 516 | 17.7748 | -357.2435 | -732.2619 | -0.6923 [-0.8724, -0.4999] | 11.4341% | -375.3312 | 18.0876 |
| TAOUSDT | 23 | -4.2432 | -22.2253 | -40.2073 | -0.9663 [-1.2985, -0.608] | 17.3913% | -23.1456 | 0.9203 |
| ZECUSDT | 482 | -65.4267 | -424.3289 | -783.2311 | -0.8804 [-1.0372, -0.6963] | 8.9212% | -451.6936 | 27.3647 |

## fill_class census (first baseline to carry one)

Census over ALL fills: `{"r1": 2456, "true_add": 888, "re_entry": 2928, "v": 32}` (Σ = 6304 = total fills; F-CLS).

| class | n (resolved) | Σsize_r | Σcell-R 1× | per-unit 0× | per-unit 1× | per-unit cost | win |
|---|---|---|---|---|---|---|---|
| r1 | 2447 | 849.0 | -489.6267 | 0.0758 | -0.5767 | 0.6525 | 19.9428% |
| v | 32 | 8.0 | 0.7366 | 0.2644 | 0.0921 | 0.1723 | 31.25% |
| true_add | 883 | 441.5 | -206.3256 | 0.21 | -0.4673 | 0.6773 | 13.59% |
| re_entry | 2917 | 1458.5 | -1101.7773 | 0.0801 | -0.7554 | 0.8355 | 13.7813% |

## Taxonomy

- Cohorts (resolved tranches): `{"PROTECTED": 2571, "FADED": 890, "NEVER_GREEN": 1094, "STILLBORN": 1724}`
- Grades (resolved tranches; '-' = ungraded/V): `{"B": 3239, "A": 2227, "-": 753, "A+": 60}`
- Rejects: `{"gap_through_stop": 20613, "not_positioned": 69395, "stop_too_tight": 670, "no_zone": 229963, "cooldown": 15451, "bar_range": 44771, "ribbon_sep": 43917, "add_ineligible": 551, "max_tranches": 113136, "c_gate_no_zone": 21091, "halted_day": 1572, "halted_week": 15638, "structure": 32, "c_gate_structure": 11, "notional_cap": 5, "equity_floor": 71320, "v_already_positioned": 1, "campaign_died_same_bar": 1}`

## Per-cell

| cell | campaigns | tranches | min equity | final equity | floor halt |
|---|---|---|---|---|---|
| BTCUSDT_intraday | 298 | 700 | 2493.12 | 2493.12 | 2022-04-11 |
| BTCUSDT_position | 44 | 121 | 8896.12 | 10553.53 | — |
| BTCUSDT_swing | 165 | 416 | 4903.62 | 8580.58 | — |
| ETHUSDT_intraday | 313 | 759 | 2491.34 | 2491.34 | 2022-07-15 |
| ETHUSDT_position | 46 | 123 | 8310.78 | 8885.88 | — |
| ETHUSDT_swing | 160 | 393 | 7380.84 | 7380.84 | — |
| JTOUSDT_intraday | 63 | 158 | 7488.09 | 7488.09 | — |
| JTOUSDT_position | 5 | 12 | 9742.83 | 9828.96 | — |
| JTOUSDT_swing | 10 | 30 | 9743.3 | 9743.3 | — |
| NEARUSDT_intraday | 319 | 741 | 2499.93 | 2499.93 | 2023-01-21 |
| NEARUSDT_position | 28 | 73 | 9202.57 | 9162.9 | — |
| NEARUSDT_swing | 127 | 303 | 8967.52 | 9242.3 | — |
| SOLUSDT_intraday | 341 | 814 | 2498.46 | 2498.46 | 2023-04-28 |
| SOLUSDT_position | 40 | 99 | 8964.46 | 9324.44 | — |
| SOLUSDT_swing | 135 | 348 | 7274.1 | 7274.1 | — |
| TAOUSDT_intraday | 21 | 54 | 9003.91 | 8925.54 | — |
| TAOUSDT_swing | 2 | 9 | 9873.99 | 10368.52 | — |
| ZECUSDT_intraday | 279 | 650 | 2492.12 | 2492.12 | 2022-06-01 |
| ZECUSDT_position | 48 | 118 | 9575.45 | 9578.43 | — |
| ZECUSDT_swing | 155 | 383 | 4898.37 | 4852.92 | — |

*Generated by scripts/tc4_fixtures.py from journal_pass2 raw bytes; journal_pass1 remains on disk, read-only — falsifiable history, not erased history.*
