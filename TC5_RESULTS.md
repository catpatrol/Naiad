# TC-5 RESULTS — intraday re-spec 1H/5m (config-only, engine 1.0.10 byte-untouched)

> **in-sample; same-asset five-cell subset (never v1's full 7-cell book); compressed ladder — v2 align sits AT the governor, no strictly-between rung exists at this scale; 2022-23 chop inside the window (see era split).**

single-variable: re-spec only; architecture cross deferred.

## Fixtures (F-ENG first)

- **F-ENG**: MATCH — `{"engine_diff_vs_6fdab03": ["engine/s2.py"], "s2_hygiene_only": true, "engine_working_tree": "(clean)", "tc5_engine_changes": "(none)"}`
- **F-CFG**: MATCH — `{"five_shas_match_prereg": true}`
- **F-SPEC**: MATCH — `{"note": "tf_align not journaled; verified from the committed config spec (cell source of truth); MTF_SET unchanged proven by F-ENG"}`
- **F-GUARDS**: MATCH — `{}`
- **F-DET**: MATCH — `{"mismatched": [], "manifest": true}`

## Thesis table — mfe_bps vs toll (v2 beside pinned v1)

toll = median cost_bps (fees+funding+slippage / notional), pooled resolved tranches

| | median mfe_bps | toll | ratio | net 1× | campaigns | tranches |
|---|---|---|---|---|---|---|
| **v2 (1H/5m)** | 35.6603 | 19.9264 | **1.7896** | -1180.3234 | 2328 | 5261 |
| v1 pinned (1H/1m) | 13.0398 | 19.9615 | 0.6533 | -1362.5619 | 1550 | 3664 |

## Per-cell headlines (v2)

| cell | net 1× | gross 0× | camps | tr | win | strip-best | med mfe_bps | floor halt | final eq |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT_intraday_v2 | -273.2184 | -43.3861 | 378 | 871 | 11.6402% | -296.9311 | 21.2499 | 2022-11-19 | 2490.81 |
| ETHUSDT_intraday_v2 | -267.1306 | -5.8765 | 486 | 1106 | 13.1687% | -321.8483 | 30.1584 | 2023-11-29 | 2492.05 |
| SOLUSDT_intraday_v2 | -236.8758 | -30.1304 | 468 | 1065 | 15.3846% | -254.1536 | 45.157 | — | 3000.18 |
| NEARUSDT_intraday_v2 | -131.2404 | 69.307 | 487 | 1089 | 15.6057% | -155.5125 | 54.6117 | — | 5011.69 |
| ZECUSDT_intraday_v2 | -271.8581 | -13.4219 | 509 | 1130 | 12.9666% | -306.6771 | 30.1802 | 2024-02-24 | 2493.41 |

## Signal-mix per 100 gov bars (v2 · v1-intraday · swing)

`{"v2": {"PRIME": 22.5646, "CONFIRM": 8.3058, "V": 0.1511, "TPW": 0.063, "CLUSTER": 7.763, "TAG": 39.8675, "X": 1.3862}, "v1_intraday": {"PRIME": 94.0509, "CONFIRM": 34.2721, "V": 0.0603, "TPW": 0.0717, "CLUSTER": 11.8265, "TAG": 102.6953, "X": 1.5981}, "swing": {"PRIME": 83.5701, "CONFIRM": 29.3185, "V": 0.0773, "TPW": 2.9515, "CLUSTER": 31.2361, "TAG": 87.8913, "X": 1.4338}, "distance_to_swing": 87.3671, "distance_to_v1": 75.5585, "nearer": "v1"}`

## Era split (boundary 2023-01-01)

`{"boundary": "2023-01-01", "splits": {"pre_2023": {"v2_net_1x": -754.4338, "v2_med_mfe_bps": 38.0043, "v2_ratio": 1.9391, "v1_net_1x": -1319.9465}, "2023_plus": {"v2_net_1x": -425.8896, "v2_med_mfe_bps": 29.0161, "v2_ratio": 1.4527, "v1_net_1x": -42.6154}}}`

## Halt calendar (v2 vs v1)

`{"v2_halts": {"BTCUSDT_intraday_v2": "2022-11-19", "ETHUSDT_intraday_v2": "2023-11-29", "ZECUSDT_intraday_v2": "2024-02-24"}, "v1_halts": {"BTCUSDT_intraday": "2022-04-11", "ETHUSDT_intraday": "2022-07-15", "SOLUSDT_intraday": "2023-04-28", "NEARUSDT_intraday": "2023-01-21", "ZECUSDT_intraday": "2022-06-01"}, "v2_halt_count": 3, "v1_halt_count": 5}`

## A-grade share of fills

`{"v2": {"n": 5261, "a_grade_share_pct": 50.5797}, "v1_intraday": {"n": 3664, "a_grade_share_pct": 33.7063}}`

## Adds funnel

`{"v2_not_positioned_rejects": 9154, "v2_fill_class": {"r1": 2132, "re_entry": 2406, "true_add": 619, "v": 104}}`

## v1 self-consistency (reproduces pinned)

`{"med_mfe_bps": 13.0398, "toll": 19.9615, "net_1x": -1362.5619, "reproduces_pinned": true}`

## Scorecard

| # | verdict | measured |
|---|---|---|
| P-TC5-a | **CONFIRMED** | `{"v2_ratio": 1.7896, "bar": 1.3, "v1_ratio": 0.6533}` |
| P-TC5-b | **FALSIFIED** | `{"v2_net_1x": -1180.3234, "bar": -862.5619}` |
| P-TC5-c | **FALSIFIED** | `{"v2_campaigns": 2328, "band": [465, 930]}` |
| P-TC5-d | **CONFIRMED** | `{"v2_halt_count": 3, "fewer_than_5": true, "all_later": true}` |
| P-TC5-e | **FALSIFIED** | `{"nearer": "v1", "d_swing": 87.3671, "d_v1": 75.5585}` |
| P-TC5-f | **CONFIRMED** | `{"v2_ratio": 1.7896, "bar": 1.0}` |

*scripts/tc5_fixtures.py; raw journal bytes; read-only.*
