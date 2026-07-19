# RC-7r RESULTS — post-S-1 recompute, re-scoped under Amendment 2

> **IN-SAMPLE / FIRST-ORDER / RANKS-ONLY - Tier-C validates. Counterfactual legs use the journaled cost/one_r proxy (funding understated on long holds). JTO/TAO 1d rows are seed-biased: flagged, excluded from 1d aggregates. The five long-history intraday cells floor out 2022-2023.**

Basis: S-1 journals engine 1.0.9; baseline = TC-4 pass2 · seed 20260720, 10000 resamples · Amendment 1 applied, then Amendment 2 re-scope: F3 family, R7-1 and R7-12 retired to S-2 as R7-1'/R7-12' with P-2L-a/b/c verbatim-unseen.

**721 of 6279 fills (11.4827%) exit on the bar they are born.**

## Fixtures

- **F1**: MATCH — `{"sum_1x": -1796.993, "sum_0x": 275.9924, "campaigns": 2599, "win_rate_pct": 10.8503}`
- **F2**: MATCH — `{"counts": {"reentry_ab": 69395, "add_trigger": 29270, "mtf_cross": 5267, "v_shadow": 3978}}`
- **F4**: MATCH — `{"aligned": {"n": 1650, "exp": -0.5492}, "not_aligned": {"n": 949, "exp": -0.9387}}`
- **F5**: MATCH — `{"census": {"r1": 2456, "true_add": 888, "re_entry": 2928, "v": 32}}`
- **F6**: MATCH — `{"share_pct": 90.3487, "grid_zero_advance_pct": 70.9189}`
- **F7**: MATCH — `{"mandate_rows": 63, "expected": 63, "dual_coordinates": true}`
- **F8**: determinism — double run, hashes printed by the runner (see ledger).

## Prediction scorecard (7 rows; falsifications first in prose)

| # | prior | verdict | measured |
|---|---|---|---|
| P-STRIP | 60 | **CONFIRMED** | `{"best_position_candidate": "ema200_gov_b0.0", "sum_1x_proxy": 389.2473, "strip_best": 156.2801}` |
| P-LAT | 60 | **FALSIFIED** | `{"halves": {"separation_ge_0.8": "FAIL (0.7687)", "triple_true_expectancy_ge_-0.2": "FAIL (-0.4557)"}, "triple_true": {"n": 394, "expectancy": -0.4557, "ci95": [-0.6532, -0.2318], ` |
| P-FH1 | 65 | **FALSIFIED** | `{"median_shift_retr_pct": 47.9863, "median_shift_depth_pct": 2.808}` |
| P-FH2 | 60 | **FALSIFIED** | `{"mfe_p50_dev_pct": 21.3115, "mfe_p75_dev_pct": 13.6925}` |
| P-FH3 | 55 | **CONFIRMED** | `{"peaks": {"swing": {"tf": "4h", "steps": 0, "separation": 0.2617}, "intraday": {"tf": "30m", "steps": -1, "separation": 0.2204}, "position": {"tf": "exec", "steps": -5, "separatio` |
| P-FH4 | [75, 55] | **enrichment:FALSIFIED / separation:CONFIRMED** | `{"enrichment_x": 1.7351, "separation_r": 1.5689}` |
| P-PRVW | [60, 55] | **reclaim:CONFIRMED / failure_depth:CONFIRMED** | `{"mean_15m30m_with": 0.0086, "sep_1h_against_minus_with": -0.207}` |

## R7-2 — per-candidate strip-best (position rows first)

> **CAVEAT (mandatory):** fold-in pinned-convention numbers; known bar-ordering infidelity (721-tranche fill-bar class + death-bar class, quantification deferred to S-2); valid for the concentration question only - not a TC-1 prediction basis.

| candidate | position Σ1×p | pos strip-best | swing Σ1×p | intraday Σ1×p | GRID Σ1×p | GRID strip-best |
|---|---|---|---|---|---|---|
| chand_k1.5 | -100.1293 | -105.5071 | -540.6455 | -1871.3582 | -2512.133 | -2518.8823 |
| chand_k2.0 | -94.6843 | -102.6973 | -489.5938 | -1873.6804 | -2457.9585 | -2467.4075 |
| chand_k3.0 | -92.3348 | -101.6149 | -479.4176 | -1805.9671 | -2377.7195 | -2390.7023 |
| ema200_exec_b0.0 | -102.8397 | -137.386 | -383.5001 | -1736.1527 | -2222.4926 | -2344.5586 |
| ema200_exec_b0.5 | -104.8243 | -138.7035 | -350.7409 | -1760.4452 | -2216.0104 | -2337.528 |
| ema200_gov_b0.0 | 389.2473 | 156.2801 | -259.2129 | -1745.4957 | -1615.4614 | -1848.4286 |
| ema200_gov_b0.5 | 381.2311 | 148.2639 | -212.6676 | -1657.0526 | -1488.4891 | -1721.4563 |
| ema89_1h_b0.0 | -65.0452 | -103.3882 | -223.4009 | -1839.9031 | -2128.3492 | -2269.0455 |
| ema89_1h_b0.5 | -35.9499 | -97.7498 | -255.9871 | -1838.7455 | -2130.6825 | -2270.7421 |
| ema89_gov_b0.0 | 281.2852 | 106.2983 | -188.1366 | -1839.9031 | -1746.7545 | -1921.7414 |
| ema89_gov_b0.5 | 272.3377 | 97.9933 | -202.7885 | -1838.7455 | -1769.1963 | -1943.5407 |
| gb_t1_g30 | -91.0142 | -92.7882 | -512.4068 | -1844.204 | -2447.625 | -2456.463 |
| gb_t1_g40 | -86.2169 | -91.7358 | -498.613 | -1843.7985 | -2428.6284 | -2438.5632 |
| gb_t1_g50 | -89.0338 | -93.5992 | -491.117 | -1867.4192 | -2447.5701 | -2476.3399 |
| gb_t2_g30 | -91.5198 | -98.5304 | -486.9422 | -1840.4358 | -2418.8978 | -2427.7358 |
| gb_t2_g40 | -91.4577 | -97.4801 | -468.6736 | -1843.0879 | -2403.2192 | -2426.8099 |
| gb_t2_g50 | -96.6535 | -102.5111 | -487.2919 | -1869.2683 | -2453.2137 | -2482.2538 |
| hyb_chand_k2 | -95.5156 | -103.5286 | -482.7604 | -1859.6673 | -2437.9433 | -2447.3923 |
| hyb_pivot_5_5_n2 | -87.1406 | -115.4511 | -463.0659 | -1703.3016 | -2253.508 | -2294.0034 |
| pivot_3_3_n2 | -79.6371 | -109.4194 | -445.8436 | -1683.9433 | -2209.424 | -2248.7217 |
| pivot_3_3_n3 | -80.6171 | -110.4387 | -456.6522 | -1674.5708 | -2211.8401 | -2250.9973 |
| pivot_5_5_n2 | -89.5945 | -117.905 | -469.1443 | -1692.8342 | -2251.573 | -2292.0684 |
| pivot_5_5_n3 | -86.2961 | -114.9185 | -487.6593 | -1687.2492 | -2261.2047 | -2300.6513 |
| rladder | -96.0399 | -104.1803 | -495.1657 | -1854.0771 | -2445.2826 | -2453.4256 |

## R7-3 — full symmetric confluence matrix (dual coordinates)

Ladder ['exec', '15m', '30m', '1h', '4h', '12h', '1d'] · governor index {"swing": 4, "intraday": 3, "position": 5}

| tf | steps | condition | mandate | n T/F | exp T | exp F | sep |
|---|---|---|---|---|---|---|---|
| exec | -4 | s2_aligned | swing | 559/195 | -0.3366 | -0.4818 | 0.1452 |
| exec | -3 | s2_aligned | intraday | 743/891 | -0.7894 | -0.9591 | 0.1696 |
| exec | -5 | s2_aligned | position | 141/70 | -0.2382 | -0.5745 | 0.3363 |
| exec | per-mandate | s2_aligned | POOLED | 1443/1156 | -0.5602 | -0.8553 | 0.2951 |
| exec | -4 | beyond_e200 | swing | 195/559 | -0.379 | -0.3725 | -0.0065 |
| exec | -3 | beyond_e200 | intraday | 283/1351 | -0.8098 | -0.897 | 0.0873 |
| exec | -5 | beyond_e200 | position | 52/159 | -0.2924 | -0.3685 | 0.0761 |
| exec | per-mandate | beyond_e200 | POOLED | 530/2069 | -0.6005 | -0.7147 | 0.1142 |
| exec | -4 | beyond_e89 | swing | 107/647 | -0.0835 | -0.4222 | 0.3388 |
| exec | -3 | beyond_e89 | intraday | 210/1424 | -0.7248 | -0.9051 | 0.1803 |
| exec | -5 | beyond_e89 | position | 20/191 | -0.3369 | -0.3511 | 0.0142 |
| exec | per-mandate | beyond_e89 | POOLED | 337/2262 | -0.4981 | -0.7202 | 0.2221 |
| 15m | -3 | s2_aligned | swing | 724/30 | -0.3663 | -0.5643 | 0.198 |
| 15m | -2 | s2_aligned | intraday | 1291/343 | -0.9268 | -0.7129 | -0.2139 |
| 15m | -4 | s2_aligned | position | 142/69 | -0.2435 | -0.5685 | 0.325 |
| 15m | per-mandate | s2_aligned | POOLED | 2157/442 | -0.6937 | -0.6803 | -0.0134 |
| 15m | -3 | beyond_e200 | swing | 688/66 | -0.3478 | -0.6492 | 0.3015 |
| 15m | -2 | beyond_e200 | intraday | 1525/109 | -0.8986 | -0.6484 | -0.2503 |
| 15m | -4 | beyond_e200 | position | 52/159 | -0.2924 | -0.3685 | 0.0761 |
| 15m | per-mandate | beyond_e200 | POOLED | 2265/334 | -0.7174 | -0.5153 | -0.2021 |
| 15m | -3 | beyond_e89 | swing | 370/384 | 0.0078 | -0.7423 | 0.7501 |
| 15m | -2 | beyond_e89 | intraday | 1537/97 | -0.8943 | -0.6859 | -0.2084 |
| 15m | -4 | beyond_e89 | position | 20/191 | -0.3369 | -0.3511 | 0.0142 |
| 15m | per-mandate | beyond_e89 | POOLED | 1927/672 | -0.7153 | -0.6229 | -0.0924 |
| 30m | -2 | s2_aligned | swing | 664/90 | -0.3584 | -0.4908 | 0.1324 |
| 30m | -1 | s2_aligned | intraday | 778/856 | -0.7665 | -0.9869 | 0.2204 |
| 30m | -3 | s2_aligned | position | 208/3 | -0.3456 | -0.6369 | 0.2913 |
| 30m | per-mandate | s2_aligned | POOLED | 1650/949 | -0.5492 | -0.9387 | 0.3895 |
| 30m | -2 | beyond_e200 | swing | 699/55 | -0.3432 | -0.7672 | 0.4239 |
| 30m | -1 | beyond_e200 | intraday | 1559/75 | -0.8884 | -0.7471 | -0.1413 |
| 30m | -3 | beyond_e200 | position | 161/50 | -0.2553 | -0.654 | 0.3987 |
| 30m | per-mandate | beyond_e200 | POOLED | 2419/180 | -0.6887 | -0.7274 | 0.0386 |
| 30m | -2 | beyond_e89 | swing | 672/82 | -0.3311 | -0.7268 | 0.3957 |
| 30m | -1 | beyond_e89 | intraday | 1519/115 | -0.9108 | -0.5011 | -0.4096 |
| 30m | -3 | beyond_e89 | position | 39/172 | -0.4159 | -0.3347 | -0.0812 |
| 30m | per-mandate | beyond_e89 | POOLED | 2230/369 | -0.7274 | -0.4737 | -0.2537 |
| 1h | -1 | s2_aligned | swing | 577/177 | -0.3792 | -0.3577 | -0.0216 |
| 1h | 0 | s2_aligned | intraday | 739/895 | -0.9848 | -0.797 | -0.1879 |
| 1h | -2 | s2_aligned | position | 199/12 | -0.3309 | -0.6619 | 0.331 |
| 1h | per-mandate | s2_aligned | POOLED | 1515/1084 | -0.6683 | -0.7237 | 0.0554 |
| 1h | -1 | beyond_e200 | swing | 692/62 | -0.3406 | -0.7488 | 0.4082 |
| 1h | 0 | beyond_e200 | intraday | 1105/529 | -0.9027 | -0.8385 | -0.0642 |
| 1h | -2 | beyond_e200 | position | 192/19 | -0.2938 | -0.9145 | 0.6207 |
| 1h | per-mandate | beyond_e200 | POOLED | 1989/610 | -0.6484 | -0.8318 | 0.1834 |
| 1h | -1 | beyond_e89 | swing | 702/52 | -0.3467 | -0.7448 | 0.3981 |
| 1h | 0 | beyond_e89 | intraday | 1569/65 | -0.8934 | -0.6056 | -0.2877 |
| 1h | -2 | beyond_e89 | position | 141/70 | -0.1927 | -0.6661 | 0.4734 |
| 1h | per-mandate | beyond_e89 | POOLED | 2412/187 | -0.6933 | -0.667 | -0.0263 |
| 4h | 0 | s2_aligned | swing | 358/396 | -0.2367 | -0.4984 | 0.2617 |
| 4h | 1 | s2_aligned | intraday | 815/819 | -0.9642 | -0.8001 | -0.1641 |
| 4h | -1 | s2_aligned | position | 139/72 | -0.3874 | -0.277 | -0.1104 |
| 4h | per-mandate | s2_aligned | POOLED | 1312/1287 | -0.7046 | -0.678 | -0.0266 |
| 4h | 0 | beyond_e200 | swing | 518/236 | -0.3387 | -0.4521 | 0.1135 |
| 4h | 1 | beyond_e200 | intraday | 877/757 | -0.9696 | -0.7803 | -0.1893 |
| 4h | -1 | beyond_e200 | position | 191/20 | -0.2866 | -0.9528 | 0.6662 |
| 4h | per-mandate | beyond_e200 | POOLED | 1586/1013 | -0.6813 | -0.7073 | 0.026 |
| 4h | 0 | beyond_e89 | swing | 722/32 | -0.3743 | -0.3723 | -0.002 |
| 4h | 1 | beyond_e89 | intraday | 935/699 | -0.9479 | -0.7937 | -0.1543 |
| 4h | -1 | beyond_e89 | position | 191/20 | -0.2913 | -0.9074 | 0.616 |
| 4h | per-mandate | beyond_e89 | POOLED | 1848/751 | -0.6559 | -0.7787 | 0.1228 |
| 12h | 1 | s2_aligned | swing | 373/381 | -0.448 | -0.3019 | -0.1461 |
| 12h | 2 | s2_aligned | intraday | 824/810 | -0.9613 | -0.8012 | -0.16 |
| 12h | 0 | s2_aligned | position | 101/110 | -0.3343 | -0.3639 | 0.0295 |
| 12h | per-mandate | s2_aligned | POOLED | 1298/1301 | -0.765 | -0.618 | -0.147 |
| 12h | 1 | beyond_e200 | swing | 407/347 | -0.4694 | -0.2625 | -0.2069 |
| 12h | 2 | beyond_e200 | intraday | 859/775 | -0.9901 | -0.7621 | -0.228 |
| 12h | 0 | beyond_e200 | position | 141/70 | -0.2515 | -0.5476 | 0.2961 |
| 12h | per-mandate | beyond_e200 | POOLED | 1407/1192 | -0.7654 | -0.6041 | -0.1614 |
| 12h | 1 | beyond_e89 | swing | 462/292 | -0.3225 | -0.4559 | 0.1333 |
| 12h | 2 | beyond_e89 | intraday | 867/767 | -0.9806 | -0.7704 | -0.2103 |
| 12h | 0 | beyond_e89 | position | 202/9 | -0.3204 | -1.0078 | 0.6874 |
| 12h | per-mandate | beyond_e89 | POOLED | 1531/1068 | -0.6949 | -0.6864 | -0.0086 |
| 1d | 2 | s2_aligned | swing | 374/368 | -0.3561 | -0.3872 | 0.0311 |
| 1d | 3 | s2_aligned | intraday | 771/779 | -0.9642 | -0.7948 | -0.1694 |
| 1d | 1 | s2_aligned | position | 101/105 | -0.3226 | -0.3598 | 0.0372 |
| 1d | per-mandate | s2_aligned | POOLED | 1246/1252 | -0.7296 | -0.6385 | -0.0911 |
| 1d | 2 | beyond_e200 | swing | 386/356 | -0.4528 | -0.2834 | -0.1693 |
| 1d | 3 | beyond_e200 | intraday | 801/749 | -1.0066 | -0.7427 | -0.2639 |
| 1d | 1 | beyond_e200 | position | 120/86 | -0.2905 | -0.4127 | 0.1222 |
| 1d | per-mandate | beyond_e200 | POOLED | 1307/1191 | -0.7773 | -0.5816 | -0.1957 |
| 1d | 2 | beyond_e89 | swing | 407/335 | -0.5314 | -0.1773 | -0.3541 |
| 1d | 3 | beyond_e89 | intraday | 813/737 | -0.9811 | -0.7666 | -0.2145 |
| 1d | 1 | beyond_e89 | position | 143/63 | -0.266 | -0.5131 | 0.2472 |
| 1d | per-mandate | beyond_e89 | POOLED | 1363/1135 | -0.7718 | -0.5786 | -0.1932 |

JTO/TAO 1d rows (flag `seed_biased`, EXCLUDED from aggregates): `[{"flag": "seed_biased", "tf": "1d", "condition": "s2_aligned", "mandate": "swing", "n_true": 5, "n_false": 7, "exp_true": -0.9751, "exp_false": -0.227}, {"flag": "seed_biased", "tf": "1d", "condition": "s2_aligned", "mandate": "intraday", "n_true": 42, "n_false": 42, "exp_true": -1.1499, "exp_false": -0.7194}, {"flag": "seed_biased", "tf": "1d", "condition": "s2_aligned", "mandate": "position", "n_true": 2, "n_false": 3, "exp_true": 0.2781, "exp_false": -1.3305}, {"flag": "seed_biased", "tf": "1d", "condition": "beyond_e200", "mandate": "swing", "n_true": 5, "n_false": 7, "exp_true": -0.6929,`

## R7-4 — FH-3 discriminator

`{"peaks": {"swing": {"tf": "4h", "steps": 0, "separation": 0.2617}, "intraday": {"tf": "30m", "steps": -1, "separation": 0.2204}, "position": {"tf": "exec", "steps": -5, "separation": 0.3363}}, "verdict": "RELATIVE", "rule_note": "precedence: ABSOLUTE (30m in all three) evaluated before the \u00b11-step RELATIVE test; RELATIVE = \u22652 of 3 mandate peaks within \u00b11 step of each other"}`

## R7-5 — joint lattice

### GRID

| cell | n | expectancy | CI95 | Σ | share of Σwins |
|---|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 394 | -0.4557 | [-0.6532, -0.2318] | -179.5376 | 12.5796 |
| 30m=1|1d_room=1|toll=0 | 315 | -0.3496 | [-0.9892, 0.59] | -110.1271 | 25.0566 |
| 30m=1|1d_room=0|toll=1 | 448 | -0.2989 | [-0.5737, 0.0045] | -133.9092 | 23.6899 |
| 30m=1|1d_room=0|toll=0 | 438 | -1.0154 | [-1.3009, -0.6654] | -444.7235 | 17.8619 |
| 30m=1|1d_room=void|toll=1 | 32 | -0.5515 | [-0.9641, -0.0378] | -17.6478 | 0.6743 |
| 30m=1|1d_room=void|toll=0 | 23 | -0.8782 | [-1.2853, -0.4018] | -20.1988 | 0.3183 |
| 30m=0|1d_room=1|toll=1 | 127 | -0.6744 | [-0.8731, -0.4255] | -85.6445 | 1.7947 |
| 30m=0|1d_room=1|toll=0 | 355 | -0.8939 | [-1.1337, -0.5943] | -317.3511 | 10.0273 |
| 30m=0|1d_room=0|toll=1 | 125 | -0.5988 | [-0.8791, -0.2291] | -74.8545 | 2.7561 |
| 30m=0|1d_room=0|toll=0 | 296 | -1.2244 | [-1.4014, -1.0431] | -362.4343 | 4.8973 |
| 30m=0|1d_room=void|toll=1 | 16 | -0.6549 | [-0.9569, -0.3517] | -10.4788 | 0.0708 |
| 30m=0|1d_room=void|toll=0 | 30 | -1.3362 | [-1.7193, -0.906] | -40.0858 | 0.2732 |

### swing

| cell | n | expectancy | CI95 | Σ | share of Σwins |
|---|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 231 | -0.5462 | [-0.7821, -0.2772] | -126.1667 | 17.0689 |
| 30m=1|1d_room=1|toll=0 | 98 | 0.313 | [-1.2954, 3.1313] | 30.6728 | 31.198 |
| 30m=1|1d_room=0|toll=1 | 213 | -0.2615 | [-0.6067, 0.119] | -55.71 | 28.6614 |
| 30m=1|1d_room=0|toll=0 | 110 | -0.7299 | [-1.3544, 0.0786] | -80.2862 | 14.6732 |
| 30m=1|1d_room=void|toll=1 | 9 | -0.1699 | [-0.6733, 0.3267] | -1.5295 | 0.4448 |
| 30m=1|1d_room=void|toll=0 | 3 | -1.6451 | [-2.2035, -1.1273] | -4.9352 | 0.0 |
| 30m=0|1d_room=1|toll=1 | 18 | 0.1004 | [-0.8547, 1.4679] | 1.8077 | 2.5942 |
| 30m=0|1d_room=1|toll=0 | 9 | -0.801 | [-1.6691, 0.2351] | -7.2088 | 0.5196 |
| 30m=0|1d_room=0|toll=1 | 40 | -0.2601 | [-0.9569, 0.7982] | -10.4023 | 4.5728 |
| 30m=0|1d_room=0|toll=0 | 23 | -1.2333 | [-1.6239, -0.8352] | -28.3666 | 0.2672 |

### intraday

| cell | n | expectancy | CI95 | Σ | share of Σwins |
|---|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 83 | -0.2597 | [-0.8096, 0.4251] | -21.5527 | 8.0436 |
| 30m=1|1d_room=1|toll=0 | 211 | -0.6499 | [-1.0834, -0.1588] | -137.1227 | 23.7998 |
| 30m=1|1d_room=0|toll=1 | 127 | -0.4721 | [-0.9333, 0.0975] | -59.9516 | 11.4835 |
| 30m=1|1d_room=0|toll=0 | 319 | -1.0963 | [-1.4061, -0.7091] | -349.7315 | 23.0849 |
| 30m=1|1d_room=void|toll=1 | 18 | -0.7046 | [-1.2899, 0.1409] | -12.6829 | 0.783 |
| 30m=1|1d_room=void|toll=0 | 20 | -0.7632 | [-1.2057, -0.2541] | -15.2636 | 0.6176 |
| 30m=0|1d_room=1|toll=1 | 109 | -0.8023 | [-0.9544, -0.6321] | -87.4521 | 1.4367 |
| 30m=0|1d_room=1|toll=0 | 346 | -0.8964 | [-1.1393, -0.5978] | -310.1423 | 19.0488 |
| 30m=0|1d_room=0|toll=1 | 82 | -0.7627 | [-0.9817, -0.5109] | -62.5415 | 1.7417 |
| 30m=0|1d_room=0|toll=0 | 273 | -1.2237 | [-1.4041, -1.0232] | -334.0676 | 9.2928 |
| 30m=0|1d_room=void|toll=1 | 16 | -0.6549 | [-0.9569, -0.3517] | -10.4788 | 0.1375 |
| 30m=0|1d_room=void|toll=0 | 30 | -1.3362 | [-1.7193, -0.906] | -40.0858 | 0.5301 |

### position

| cell | n | expectancy | CI95 | Σ | share of Σwins |
|---|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 80 | -0.3977 | [-0.6476, -0.0713] | -31.8183 | 19.1333 |
| 30m=1|1d_room=1|toll=0 | 6 | -0.6129 | [-1.383, 0.3098] | -3.6773 | 1.4324 |
| 30m=1|1d_room=0|toll=1 | 108 | -0.169 | [-0.752, 0.6866] | -18.2476 | 78.2559 |
| 30m=1|1d_room=0|toll=0 | 9 | -1.634 | [-2.1346, -1.0407] | -14.7058 | 0.0273 |
| 30m=1|1d_room=void|toll=1 | 5 | -0.6871 | [-1.3809, 0.2709] | -3.4354 | 1.151 |
| 30m=0|1d_room=1|toll=1 | 0 | None | [None, None] | 0.0 | 0.0 |
| 30m=0|1d_room=1|toll=0 | 0 | None | [None, None] | 0.0 | 0.0 |
| 30m=0|1d_room=0|toll=1 | 3 | -0.6369 | [-0.8242, -0.269] | -1.9107 | 0.0 |
| 30m=0|1d_room=0|toll=0 | 0 | None | [None, None] | 0.0 | 0.0 |

### R1_only_companion

| cell | n | expectancy | CI95 | Σ | share of Σwins |
|---|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 394 | -0.2636 (per-unit) | — | — | — |
| 30m=1|1d_room=1|toll=0 | 315 | -0.2889 (per-unit) | — | — | — |
| 30m=1|1d_room=0|toll=1 | 448 | -0.2422 (per-unit) | — | — | — |
| 30m=1|1d_room=0|toll=0 | 438 | -0.9785 (per-unit) | — | — | — |
| 30m=1|1d_room=void|toll=1 | 32 | -0.6848 (per-unit) | — | — | — |
| 30m=1|1d_room=void|toll=0 | 23 | -0.207 (per-unit) | — | — | — |
| 30m=0|1d_room=1|toll=1 | 127 | -0.624 (per-unit) | — | — | — |
| 30m=0|1d_room=1|toll=0 | 355 | -0.7622 (per-unit) | — | — | — |
| 30m=0|1d_room=0|toll=1 | 125 | -0.2914 (per-unit) | — | — | — |
| 30m=0|1d_room=0|toll=0 | 296 | -1.0375 (per-unit) | — | — | — |
| 30m=0|1d_room=void|toll=1 | 16 | -0.9247 (per-unit) | — | — | — |
| 30m=0|1d_room=void|toll=0 | 30 | -1.3116 (per-unit) | — | — | — |

## R7-6 — FH-1 signal-shape census

`{"swing": {"gov_bars": 46349, "per_100_gov_bars": {"REGIME": 1.862, "TAG": 87.1993, "PRIME": 83.3977, "CONFIRM": 29.2196, "V": 0.0777, "TPW": 2.9645, "X": 1.4218, "CLUSTER": 31.129}, "retr_quantiles_p25_50_75": [-1.1872, -0.2021, 0.1976], "depth_gov_atr_quantiles_p25_50_75": [0.2817, 0.9357, 2.0421]}, "intraday": {"gov_bars": 189857, "per_100_gov_bars": {"REGIME": 1.943, "TAG": 102.2491, "PRIME": 93.8749, "CONFIRM": 34.2321, "V": 0.0595, "TPW": 0.0695, "X": 1.5923, "CLUSTER": 11.6867}, "retr_quantiles_p25_50_75": [-0.9231, -0.1012, 0.2023], "depth_gov_atr_quantiles_p25_50_75": [0.334, 0.9721, 1.9243]}, "position": {"gov_bars": 14594, "per_100_gov_bars": {"REGIME": 1.7062, "TAG": 76.1135, "PRIME": 79.6834, "CONFIRM": 27.4565, "V": 0.0617, "TPW": 10.2302, "X": 1.2265, "CLUSTER": 43.2438}, "retr_quantiles_p25_50_75": [-0.7969, -0.1064, 0.2073], "depth_gov_atr_quantiles_p25_50_75": [0.3078, 0.9804, 2.0385]}, "_definition": "depth proxy = |px_signal - stop| / atr_gov on PRIME rows (stop anchors at the signal-bar extreme + 0.5 ATR_exec buffer); true zone-band depth needs engine columns -> S-2"}`

## R7-7 — FH-2 R-space anatomy

`{"swing": {"n": 1873, "mfe_deciles": [0.0, 0.0995, 0.2629, 0.4523, 0.7487, 1.1939, 1.7894, 2.7931, 5.167], "mae_deciles": [-1.7458, -1.4562, -1.2947, -1.1973, -1.1233, -1.0595, -1.0057, -0.7832, -0.4486], "protected_share_pct": 43.9402, "winner_capture_p25_50_75": [-0.6946, -0.2093, 0.2104]}, "intraday": {"n": 3874, "mfe_deciles": [0.0, 0.0, 0.1247, 0.3288, 0.5744, 0.9454, 1.4924, 2.4154, 4.6337], "mae_deciles": [-1.7371, -1.459, -1.3115, -1.2085, -1.1288, -1.0672, -1.0147, -0.8033, -0.4808], "protected_share_pct": 38.8745, "winner_capture_p25_50_75": [-0.7986, -0.208, 0.2013]}, "position": {"n": 532, "mfe_deciles": [0.031, 0.1517, 0.3266, 0.5478, 0.8668, 1.2693, 1.9057, 2.8689, 5.1099], "mae_deciles": [-1.8034, -1.5052, -1.3393, -1.2287, -1.1431, -1.0624, -1.0026, -0.7286, -0.4169], "protected_share_pct": 45.4887, "winner_capture_p25_50_75": [-0.5839, -0.0798, 0.2781]}}`

## R7-8 — FH-4 nesting census

`{"swing_given_intraday": {"births_in_overlap_era": 434, "same_dir_active_at_birth": 29, "observed_rate_pct": 6.682, "expected_rate_pct": 3.8511, "enrichment_x": 1.7351, "exp_conditioned": 1.0422, "exp_unconditioned": -0.5267, "separation_r": 1.5689, "per_asset": {"BTCUSDT": {"births_in_overlap": 95, "same_dir_active": 7}, "ETHUSDT": {"births_in_overlap": 85, "same_dir_active": 7}, "JTOUSDT": {"births_in_overlap": 10, "same_dir_active": 1}, "NEARUSDT": {"births_in_overlap": 73, "same_dir_active": 5}, "SOLUSDT": {"births_in_overlap": 90, "same_dir_active": 4}, "TAOUSDT": {"births_in_overlap": 2, "same_dir_active": 0}, "ZECUSDT": {"births_in_overlap": 79, "same_dir_active": 5}}, "caveat": "same tape - co-movement is not causality; overlap era only (intraday cells floor out 2022-2023)"}, "position_given_swing": {"births_in_overlap_era": 210, "same_dir_active_at_birth": 11, "observed_rate_pct": 5.2381, "expected_rate_pct": 3.6822, "enrichment_x": 1.4225, "exp_conditioned": 0.1985, "exp_unconditioned": -0.3729, "separation_r": 0.5714, "per_asset": {"BTCUSDT": {"births_in_overlap": 44, "same_dir_active": 2}, "ETHUSDT": {"births_in_overlap": 45, "same_dir_active": 2}, "JTOUSDT": {"births_in_overlap": 5, "same_dir_active": 0}, "NEARUSDT": {"births_in_overlap": 28, "same_dir_active": 1}, "SOLUSDT": {"births_in_overlap": 40, "same_dir_active": 3}, "TAOUSDT": {"births_in_overlap": 0, "same_dir_active": 0}, "ZECUSDT": {"births_in_overlap": 48, "same_dir_active": 3}}, "caveat": "same tape - co-movement is not causality; overlap era only (intraday cells floor out 2022-2023)"}}`

## R7-9 — sizing sweeps (first-order re-weights only)

> CAVEAT: re-weighting ignores rail/halt/equity-path feedback; the modes interview and a config-only Tier-C own adoption.

`{"mandate_multipliers": [{"m_intraday": 0.25, "m_position": 1.0, "grid_1x": -716.1882, "grid_1x_adds_x0.5": -452.839}, {"m_intraday": 0.25, "m_position": 1.5, "grid_1x": -753.0858, "grid_1x_adds_x0.5": -481.355}, {"m_intraday": 0.25, "m_position": 2.0, "grid_1x": -789.9834, "grid_1x_adds_x0.5": -509.8709}, {"m_intraday": 0.5, "m_position": 1.0, "grid_1x": -1076.4565, "grid_1x_adds_x0.5": -682.8732}, {"m_intraday": 0.5, "m_position": 1.5, "grid_1x": -1113.3541, "grid_1x_adds_x0.5": -711.3891}, {"m_intraday": 0.5, "m_position": 2.0, "grid_1x": -1150.2517, "grid_1x_adds_x0.5": -739.9051}, {"m_intraday": 1.0, "m_position": 1.0, "grid_1x": -1796.993, "grid_1x_adds_x0.5": -1142.9415}, {"m_intraday": 1.0, "m_position": 1.5, "grid_1x": -1833.8906, "grid_1x_adds_x0.5": -1171.4575}, {"m_intraday": 1.0, "m_position": 2.0, "grid_1x": -1870.7882, "grid_1x_adds_x0.5": -1199.9734}], "confluence_tiers": {"tier_census": {"0": 746, "1": 2400, "2": 2252, "3": 881}, "grid_1x_reweighted": -1915.6683, "per_mandate": {"swing": -373.2882, "intraday": -1415.897, "position": -126.4831}, "note": "1d condition VOID (not false) for JTO/TAO -> their max count is 2; weights registered {0.5,1.0,1.5,2.0}"}}`

## R7-10 — trigger previews (PROXY)

`{"30m_flip_with_trend_e9e89": {"n": 175, "mean_remaining_r": 0.0136, "per_mandate": {"swing": {"n": 20, "mean": -0.2056, "steps": [-2]}, "intraday": {"n": 22, "mean": 0.4498, "steps": [-1]}, "position": {"n": 133, "mean": -0.0256, "steps": [-3]}}}, "15m30m_flip_with_trend_e9e89": {"n": 675, "mean_remaining_r": 0.0086, "per_mandate": {"swing": {"n": 266, "mean": 0.252, "steps": [-3, -2]}, "intraday": {"n": 41, "mean": 0.1849, "steps": [-2, -1]}, "position": {"n": 368, "mean": -0.1869, "steps": [-4, -3]}}}, "1h_flip_against_e9e89": {"n": 8, "mean_remaining_r": -0.5181, "per_mandate": {"swing": {"n": 4, "mean": -0.1328, "steps": [-1]}, "intraday": {"n": 0, "mean": null, "steps": [0]}, "position": {"n": 4, "mean": -0.9034, "steps": [-2]}}}, "1h_flip_with_e9e89": {"n": 33, "mean_remaining_r": -0.3111, "per_mandate": {"swing": {"n": 7, "mean": -1.6679, "steps": [-1]}, "intraday": {"n": 1, "mean": 3.1439, "steps": [0]}, "position": {"n": 25, "mean": -0.0694, "steps": [-2]}}}, "_label": "PROXY - a cross is not a test-and-reclaim; S-2 F8 measures the real thing"}`

## R7-11 — adds-funnel dual print

`{"while_positioned_add_signal_rows": 3040, "filled": 1002, "gate_or_fill_rejected": 1020, "signal_no_fill_row": 1018, "reject_reasons": {"add_ineligible": 548, "max_tranches": 472}, "contract_reference": {"admitted": 984, "rejected": 716, "note": "Report-4 derivation; definitional differences reported, not forced"}, "per_candidate_adds_would_be_eligible_mean": {"ema200_gov_b0.5": 0.0631, "ema200_gov_b0.0": 0.0642, "ema89_gov_b0.0": 0.0104}, "two_line_column": "== baseline by construction: line 1 IS the native ratchet the BE-gate tests against; the trail only adds an exit, and an exited tranche gates nothing"}`

*Generated by scripts/rc7_recompute.py from raw journal/sidecar bytes. R7-1'/R7-12'/P-2L-a/b/c retired to S-2, verbatim-unseen.*
