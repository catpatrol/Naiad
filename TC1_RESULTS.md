# TC-1 RESULTS — Stop × Exit Architecture Factorial (engine 1.0.11)

> **in-sample; REAL runs (path effects — re-entry suppression, concurrency, funding, rail/halt feedback — are measured, not noise); B/D denominated in struct-R, A/C in baseline-R; prediction basis s2b D1 (the 38% gross, not the +2360 headline).**

prediction basis: s2b D1 — registered against the 38%, not the headline.

## Fixtures (F-A-BYTE first)

- **F-A-BYTE**: MATCH — `{"mismatched_cells": []}`
- **F-SIG-ALL**: MATCH — `{"mismatched": []}`
- **F-ARCH-B**: MATCH — `{"struct_recompute_violations": 0, "B_nonstatic_intrabar_exits": 0, "B_stopgap_wrong_side": 0}`
- **F-TRAIL**: MATCH — `{"loosening_violations": 0, "stop_gap_exits_excluded": 75}`
- **F-GUARDS**: MATCH — `{"all_hold": true}`
- **F-CFG**: MATCH — `{}`
- **F-DET**: MATCH — `{"mismatched": [], "manifest": true}`

## Per-arm headlines (GRID; denominator noted)

| arm | denom | 0× | 1× | 2× | camps | tr | win | strip-best | cost stack | fills_no_exit |
|---|---|---|---|---|---|---|---|---|---|---|
| A | baseline-R | 275.9924 | -1796.993 | -3869.9784 | 758 | 6279 | 14.248% | -1913.765 | 2072.9854 | 25 |
| B | struct-R | 1164.4202 | -351.1542 | -1866.7286 | 1186 | 7094 | 21.3322% | -542.751 | 1515.5744 | 23 |
| C | baseline-R | 697.4821 | -1357.8778 | -3413.2377 | 839 | 5579 | 11.0846% | -1572.6369 | 2055.3599 | 25 |
| D | struct-R | 1068.1723 | -614.6116 | -2297.3955 | 1140 | 8813 | 17.0175% | -789.9527 | 1682.7839 | 27 |

### Per-mandate 1× (denominators as above)

| arm | swing | intraday | position |
|---|---|---|---|
| A | -282.1248 | -1441.073 | -73.7952 |
| B | 81.5251 | -383.6233 | -49.056 |
| C | -227.8177 | -1409.7884 | 279.7283 |
| D | -15.609 | -546.3205 | -52.682 |

## Factorial main-effects + interaction

> B/D are struct-R, A/C baseline-R; the interaction mixes denominators — read directional, not additive-exact (contract §7).

| scope | A | B | C | D | stop(B−A) | trail(C−A) | interaction(D−B−C+A) |
|---|---|---|---|---|---|---|---|
| GRID | -1796.993 | -351.1542 | -1357.8778 | -614.6116 | 1445.8388 | 439.1152 | -702.5726 |
| swing | -282.1248 | 81.5251 | -227.8177 | -15.609 | 363.6499 | 54.3071 | -151.4412 |
| intraday | -1441.073 | -383.6233 | -1409.7884 | -546.3205 | 1057.4497 | 31.2846 | -193.9818 |
| position | -73.7952 | -49.056 | 279.7283 | -52.682 | 24.7392 | 353.5235 | -357.1495 |

## Scorecard

| # | verdict | measured |
|---|---|---|
| P-A | **CONFIRMED** | `{"byte_identical": true}` |
| P-B-1 | **FALSIFIED** | `{"B_grid_1x": -351.1542, "band": [100, 900]}` |
| P-B-2 | **CONFIRMED** | `{"B_swing_1x": 81.5251}` |
| P-B-3 | **CONFIRMED** | `{"B_intraday_1x": -383.6233}` |
| P-C-1 | **CONFIRMED** | `{"C_grid_1x": -1357.8778, "band": [-1900, -1300]}` |
| P-C-2 | **CONFIRMED** | `{"C_position_1x": 279.7283}` |
| P-D | **FALSIFIED** | `{"D_grid_1x": -614.6116, "B_grid_1x": -351.1542}` |
| P-CNT | **FALSIFIED** | `{"B_tranches": 7094, "D_tranches": 8813, "cap": 4412.8, "A_tranches": 6304}` |

## Halt calendars + fill_class

- **A**: halts `{"BTCUSDT_intraday": "2022-04-11", "ETHUSDT_intraday": "2022-07-15", "NEARUSDT_intraday": "2023-01-21", "SOLUSDT_intraday": "2023-04-28", "ZECUSDT_intraday": "2022-06-01"}` · fill_class `{"r1": 2447, "true_add": 883, "re_entry": 2917, "v": 32}`
- **B**: halts `{}` · fill_class `{"re_entry": 3202, "r1": 3814, "v": 78}`
- **C**: halts `{"BTCUSDT_intraday": "2021-06-01", "ETHUSDT_intraday": "2022-08-29", "NEARUSDT_intraday": "2022-09-06", "SOLUSDT_intraday": "2023-09-13", "ZECUSDT_intraday": "2022-12-19"}` · fill_class `{"r1": 2376, "re_entry": 2885, "true_add": 289, "v": 29}`
- **D**: halts `{"ZECUSDT_intraday": "2024-03-04"}` · fill_class `{"re_entry": 4212, "r1": 3753, "true_add": 771, "v": 77}`

*scripts/tc1_fixtures.py; raw journal bytes; 1h frame reloaded per B/D cell to recompute the structural stop.*
