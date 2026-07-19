# S-2 MEASUREMENT — corrected simulator + new families (engine 1.0.10)

> **IN-SAMPLE / FIRST-ORDER / RANKS-ONLY - TC-1 validates; cost proxies stated; JTO/TAO 1d void; intraday era caveat**

R7-1' delivered — TC-1 registers against this table.

## Fixtures (F-IDENT2 first)

- **F-IDENT2**: MATCH — `{"zero_advance_tranches": 4453, "violations": 0}`
- **F-BYTE**: MATCH — `{"cells": 20}`
- **F-P2REF**: MATCH — `{"sum_1x": -1796.993, "sum_0x": 275.9924, "campaigns": 2599, "win_rate_pct": 10.8503}`
- **F-REG**: MATCH — `{"found": true, "fold": 0.073892, "kind": "flatten"}`
- **F-DELTA**: MATCH — `{"pinned": 899, "fill_bar": 721, "tie_class": 4, "controls": 200, "mismatches": 0}`
- **F-F1N**: MATCH — `{"rows": 229963}`
- **F-GRID**: MATCH — `{"d1_cells": ["20_2.0", "20_3.0", "40_3.0"], "d4_cells": ["0.25_3", "0.25_5", "0.5_3", "0.5_5"], "f8_cells": ["(-1, 'e200')", "(-1, 'e89')", "(-2, 'e2`
- **F-EMIT**: MATCH — `{"rows_missing_s2": 0}`
- **F-DET**: MATCH — `{"manifest": true}`

## Scorecard

| # | verdict | measured |
|---|---|---|
| P-2L-a | **FALSIFIED** | `{"two_0x": -121.7099}` |
| P-2L-b | **FALSIFIED** | `{"position_two_1x_proxy": -81.6503}` |
| P-2L-c | **CONFIRMED** | `{"ge_share_pct": 94.0854}` |
| P-SD | **CONFIRMED** | `{"fold_0x_corrected": 506.279, "pinned": 584.4963}` |
| P-F1 | **CONFIRMED** | `{"reject_net": -1.205, "r1_net": -0.5767}` |
| P-F4 | **CONFIRMED** | `{"struct_30m_book": 363.5363}` |
| P-PD1 | **FALSIFIED** | `{"sep": 0.1715}` |
| P-PD2 | **FALSIFIED** | `{"d4_mean_bps": -0.4515}` |
| P-PD3 | **CONFIRMED** | `{"sep": -0.3302}` |
| P-PD4 | **FALSIFIED** | `{"d4_robust": 16.6667, "d4_replicates": false}` |
| P-F8 | **FALSIFIED/FALSIFIED** | `{"reclaim_mean": -0.1235, "failure_sep": 1.1841}` |
| P-F2 | **FALSIFIED** | `{"sep": 0.1715}` |
| P-NEST | **FALSIFIED** | `{}` |

## R7_1p_two_line

`{"table": {"ema200_gov_b0.5": {"GRID": {"fold_0x": 506.279, "fold_1x_proxy": -1566.7064, "two_0x": -121.7099, "two_1x_proxy": -2194.6953, "strip_best_two_1x": -2308.8764, "win_pct": 10.1962, "med_capture_pct": 1.2833, "noise_pct": 61.6977, "src_census": {"base": 1381, "both": 4705, "cand": 193}}, "swing": {"fold_0x": 262.3805, "fold_1x_proxy": -198.1107, "two_0x": 102.9716, "two_1x_proxy": -357.5196, "strip_best_two_1x": -471.7007, "win_pct": 12.069, "med_capture_pct": -3.4073, "noise_pct": 61.9327, "src_census": {"base": 448, "both": 1363, "cand": 62}}, "intraday": {"fold_0x": -214.0648, "fold_1x_proxy": -1752.8345, "two_0x": -216.7556, "two_1x_proxy": -1755.5253, "strip_best_two_1x": -1796.3056, "win_pct": 8.8127, "med_capture_pct": 4.8669, "noise_pct": 61.332, "src_census": {"base": 814, "both": 2950, "cand": 110}}, "position": {"fold_0x": 457.9633, "fold_1x_proxy": 384.2388, "two_0x": -7.9259, "two_1x_proxy": -81.6503, "strip_best_two_1x": -117.6462, "win_pct": 14.218, "med_capture_pct": 0.5771, "noise_pct": 63.5338, "src_census": {"both": 392, "base": 119, "cand": 21}}}, "ema200_gov_b0.0": {"GRID": {"fold_0x": 403.024, "fold_1x_proxy": -1669.9614, "two_0x": -114.1835, "two_1x_proxy": -2187.1689, "strip_best_two_1x": -2301.35, "win_pct": 10.3501, "med_capture_pct": 1.3106, "noise_pct": 61.6977, "src_census": {"base": 1359, "both": 4670, "cand": 250}}, "swing": {"fold_0x": 215.419, "fold_1x_proxy": -245.0722, "two_0x": 107.2207, "two_1x_proxy": -353.2705, "strip_best_two_1x": -467.4516, "win_pct": 12.5995, "med_capture_pct": -2.8618, "noise_pct": 62.0395, "src_census": {"base": 444, "both": 1352, "cand": 77}}, "intraday": {"fold_0x": -278.2283, "fold_1x_proxy": -1816.998, "two_0x": -217.2288, "two_1x_proxy": -1755.9985, "strip_best_two_1x": -1796.7787, "win_pct": 8.7515, "med_capture_pct": 4.078, "noise_pct": 61.332, "src_census": {"base": 796, "both": 2933, "cand": 145}}, "position": {"fold_0x": 465.8333, "fold_1x_proxy": 392.1088, "two_0x": -4.1755, "two_1x_pro`

## R7_12p_fill_bar_bias

`{"table": {"ema200_gov_b0.5": {"GRID": {"n": 721, "legacy_0x": -252.0828, "engine_truth_0x": -330.5, "bias": 78.4172, "recovery_ride_pct": 2.6352}, "swing": {"n": 191, "legacy_0x": -104.557, "engine_truth_0x": -90.0, "bias": -14.557, "recovery_ride_pct": 3.6649}, "intraday": {"n": 490, "legacy_0x": -126.5334, "engine_truth_0x": -222.5, "bias": 95.9666, "recovery_ride_pct": 2.449}, "position": {"n": 40, "legacy_0x": -20.9925, "engine_truth_0x": -18.0, "bias": -2.9925, "recovery_ride_pct": 0.0}}, "ema200_gov_b0.0": {"GRID": {"n": 721, "legacy_0x": -275.5101, "engine_truth_0x": -330.5, "bias": 54.9899, "recovery_ride_pct": 3.0513}, "swing": {"n": 191, "legacy_0x": -104.1407, "engine_truth_0x": -90.0, "bias": -14.1407, "recovery_ride_pct": 3.6649}, "intraday": {"n": 490, "legacy_0x": -150.5079, "engine_truth_0x": -222.5, "bias": 71.9921, "recovery_ride_pct": 2.8571}, "position": {"n": 40, "legacy_0x": -20.8615, "engine_truth_0x": -18.0, "bias": -2.8615, "recovery_ride_pct": 2.5}}, "ema89_gov_b0.0": {"GRID": {"n": 721, "legacy_0x": -278.3153, "engine_truth_0x": -330.5, "bias": 52.1847, "recovery_ride_pct": 1.6644}, "swing": {"n": 191, "legacy_0x": -99.0198, "engine_truth_0x": -90.0, "bias": -9.0198, "recovery_ride_pct": 1.5707}, "intraday": {"n": 490, "legacy_0x": -158.619, "engine_truth_0x": -222.5, "bias": 63.881, "recovery_ride_pct": 1.6327}, "position": {"n": 40, "legacy_0x": -20.6766, "engine_truth_0x": -18.0, "bias": -2.6766, "recovery_ride_pct": 2.5}}}, "footnote": "standing correction on every S-1 fold-in figure"}`

## F1_rejects

`{"n": 229963, "with_outcome": 229594, "per_unit_gross_mean": 0.0957, "per_unit_net_proxy_mean": -1.205, "admitted_r1_per_unit_net": -0.5767, "terminal_census": {"cap10": 16938, "horizon": 16071, "stop": 195035, "gap": 1550, "data_end": 1, "bad_unit": 368}, "per_mandate_net": {"swing": -0.4829, "intraday": -1.4265, "position": -0.2644}}`

## F2_headwind

`{"n_headwind": 315, "n_clear": 5964, "pu_headwind": -0.4893, "pu_clear": -0.6608, "separation": 0.1715}`

## F4_struct_stop

`{"table": {"exec": {"void": 95, "grid_1x_struct_book": -842.8373, "baseline_shakeouts": 4108, "shakeout_conversions": 1863}, "30m": {"void": 7, "grid_1x_struct_book": 363.5363, "baseline_shakeouts": 4167, "shakeout_conversions": 2153}, "1h": {"void": 0, "grid_1x_struct_book": 565.5794, "baseline_shakeouts": 4171, "shakeout_conversions": 2158}}, "baseline_grid_1x": -1796.993, "caveat": "first-order; rail/halt/equity feedback ignored; void tranches keep their baseline outcome"}`

## detectors

`{"d4_mean_fwd20_signed_bps": -0.4515, "d4_events": 1030659, "d4_sign_robust_cells": "2/12", "d4_1h_mean": 0.2064, "d4_4h_mean": -1.936, "d1_events": 17138, "d2_events": 3143, "d3_events": 32109}`

## entry_splits

`{"break_retest": {"n": 881, "pu": -0.7703}, "mid_range": {"n": 323, "pu": -0.9418}, "z2_in_range": {"n": 44, "pu": -1.2435}, "z2_out_range": {"n": 544, "pu": -0.9133}}`

## F7_pockets

`{"deciles": [{"decile": 1, "n": 103006, "mean_fwd20_bps": -2.2214}, {"decile": 2, "n": 103452, "mean_fwd20_bps": -1.0532}, {"decile": 3, "n": 103168, "mean_fwd20_bps": -0.1893}, {"decile": 4, "n": 106491, "mean_fwd20_bps": 0.6629}, {"decile": 5, "n": 103093, "mean_fwd20_bps": 0.0664}, {"decile": 6, "n": 103033, "mean_fwd20_bps": -0.9423}, {"decile": 7, "n": 103033, "mean_fwd20_bps": -1.8875}, {"decile": 8, "n": 103088, "mean_fwd20_bps": -0.4682}, {"decile": 9, "n": 103039, "mean_fwd20_bps": -0.0943}, {"decile": 10, "n": 103044, "mean_fwd20_bps": 1.3441}]}`

## F8_reclaim

`{"events": 6576, "reclaim_12_mean_rem_r": -0.1235, "unreclaimed_s1_e200_mean": 0.4536, "reclaimed_s1_e200_mean": -0.7305}`

## FH4_grid

`{"active_at_birth": {"n_cond": 29, "sep": 1.473, "exp_cond": 1.0422, "exp_uncond": -0.4308}, "born_within_6": {"n_cond": 153, "sep": -0.0284, "exp_cond": -0.3968, "exp_uncond": -0.3684}, "born_within_12": {"n_cond": 297, "sep": 0.0743, "exp_cond": -0.3291, "exp_uncond": -0.4034}, "born_within_24": {"n_cond": 417, "sep": -0.1098, "exp_cond": -0.4232, "exp_uncond": -0.3135}}`

*scripts/s2_fixtures.py; raw bytes only; s1 joined, not re-emitted.*
