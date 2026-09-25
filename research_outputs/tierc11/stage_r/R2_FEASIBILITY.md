as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE R · R2 FEASIBILITY

## R2 · FEASIBILITY PER LENS [L-R.4; TC10's Q-R3 law, the census's own functions]

Disclosure [L-R.4]: TC10's per-era Q-R3 verdicts for 5m, 4h and 1d were seen before this era was chosen (4h CLASSIC5 pooled passes only on the holdout, +0.0062 ATR; 1d passes ALL and tuning and fails the holdout). 1h, 12h and 1w were never measured. The holdout is of record because the scale is tuning-calibrated.

### THE LENS VERDICTS OF RECORD (POOLED:CLASSIC5 · holdout · calibrated · taker) — RECORD, not Tier-E

| lens | VERDICT | maker twin | charter twin | n_ranges | ratio_median | share<1 | edge_n | edge_n_ranges | median term H20 | toll ATR | net H20 | pick window | scale in-sample | fallback members | stability-changed members | Tier-E tuning word | Tier-E ALL word |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5m | **FAIL** | FAIL | FAIL | 10344 | 11.3326 | 0.0016 | 174726 | 9978 | +0.096495 | 0.712218 | -0.615724 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | SOLUSDT,NEARUSDT,ZECUSDT | FAIL | FAIL |
| 15m | **FAIL** | FAIL | FAIL | 3049 | 21.8723 | 0.0000 | 55971 | 2948 | +0.058852 | 0.361930 | -0.303078 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | BTCUSDT,SOLUSDT,NEARUSDT | FAIL | FAIL |
| 1h | **FAIL** | FAIL | FAIL | 816 | 46.2355 | 0.0000 | 12044 | 771 | +0.000000 | 0.167605 | -0.167605 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | BTCUSDT,SOLUSDT,NEARUSDT | FAIL | FAIL |
| 4h | **FAIL** | FAIL | FAIL | 191 | 103.5067 | 0.0000 | 2840 | 186 | -0.020693 | 0.082389 | -0.103083 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | NEARUSDT | FAIL | FAIL |
| 12h | **FAIL** | FAIL | FAIL | 66 | 199.1925 | 0.0000 | 1052 | 67 | -0.112893 | 0.045026 | -0.157919 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | BTCUSDT,ETHUSDT,SOLUSDT | FAIL | FAIL |
| 1d | **FAIL** | FAIL | FAIL | 33 | 276.2612 | 0.0000 | 504 | 35 | -0.655558 | 0.031950 | -0.687508 | tuning | OUT-OF-SAMPLE (holdout; the causal slice of a tuning pick) | — | BTCUSDT,SOLUSDT | PASS | FAIL |
| 1w | **FAIL (provisional, n<30)** | FAIL (provisional, n<30) | FAIL (provisional, n<30) | 6 | 1626.0737 | 0.0000 | 48 | 5 | +1.133907 | 0.010306 | +1.123600 | whole-tape (fallback) | IN-SAMPLE at every instant (whole-tape fallback pick) | BTCUSDT,ETHUSDT,SOLUSDT,NEARUSDT,ZECUSDT | — | FAIL (provisional, n<30) | FAIL (provisional, n<30) |

Word law: SR-3 THE WORD [L-R.4]: PASS iff the height leg (n_ranges >= 30, median(ratio) >= 3.0, share(ratio < 1) <= 0.10) AND the edge leg (edge_n >= 30, edge_n_ranges >= 30, net = round(median term H20, 8) - round(toll, 8) > 0) both pass within the row's era; a FAIL with any leg under its floor (n_ranges, edge_n_ranges or edge_n < 30) reads 'FAIL (provisional, n<30)'; else 'FAIL'. The census's own gate booleans are cross-checked (HALT on disagreement).

Record law: SR-4 THE LENS VERDICT OF RECORD [L-R.4] = the POOLED:CLASSIC5 row, HOLDOUT era, calibrated scale (each member at its FILED pick), taker toll; 'FAIL — maker twin PASSES (…)' when taker FAILs and the maker twin of the same row PASSES. Every other row is Tier-E, its word in `would_read`, collared.

### Every R2 row, WHOLE (1458 rows). Record rows carry `word` and `verdict`; every other row is Tier-E (collared) with NO verdict word: its word is printed as `would_read` [L-1.4, L-R.4]. TC10 continuity (AM-1) on 5m / 4h / 1d taker rows (`tc10_would_read`).

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

| panel | lens | era | scale_kind | toll | toll_bps_rt_min | toll_bps_rt_max | n_ranges | ratio_median | share_ratio_lt_1 | edge_n | edge_n_ranges | edge_median_term_h20 | edge_toll_atr | edge_net_h20 | word | verdict | would_read | pick_window | tc10_would_read | tc10_edge_net_h20 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ASSET:BTCUSDT | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 6468 | 6.7175 | 0.0042 | 104347 | 6141 | 0.264235 | 0.555925 | -0.291690 | — | — | FAIL | tuning | FAIL | -0.283764 |
| ASSET:BTCUSDT | 5m | ALL | calibrated | charter | 14.0 | 14.0 | 6468 | 4.7982 | 0.0130 | 104347 | 6141 | 0.264235 | 0.778295 | -0.514060 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 6468 | 16.7937 | 0.0003 | 104347 | 6141 | 0.264235 | 0.222370 | 0.041865 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2835 | 13.0675 | 0.0004 | 77482 | 2810 | 0.232896 | 0.541170 | -0.308274 | — | — | FAIL | frozen3.0 | FAIL | -0.309180 |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | charter | 14.0 | 14.0 | 2835 | 9.3340 | 0.0007 | 77482 | 2810 | 0.232896 | 0.757638 | -0.524742 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2835 | 32.6689 | 0.0000 | 77482 | 2810 | 0.232896 | 0.216468 | 0.016428 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 4067 | 7.5475 | 0.0037 | 68605 | 3873 | 0.333375 | 0.485336 | -0.151961 | — | — | FAIL | tuning | FAIL | -0.137499 |
| ASSET:BTCUSDT | 5m | tuning | calibrated | charter | 14.0 | 14.0 | 4067 | 5.3911 | 0.0101 | 68605 | 3873 | 0.333375 | 0.679471 | -0.346096 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 4067 | 18.8687 | 0.0000 | 68605 | 3873 | 0.333375 | 0.194135 | 0.139240 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1839 | 14.5918 | 0.0000 | 50569 | 1824 | 0.288889 | 0.465561 | -0.176673 | — | — | FAIL | frozen3.0 | FAIL | -0.176673 |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | charter | 14.0 | 14.0 | 1839 | 10.4227 | 0.0005 | 50569 | 1824 | 0.288889 | 0.651786 | -0.362897 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1839 | 36.4794 | 0.0000 | 50569 | 1824 | 0.288889 | 0.186225 | 0.102664 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 2401 | 5.6325 | 0.0050 | 35742 | 2268 | 0.102235 | 0.712218 | -0.609983 | — | — | FAIL | tuning | FAIL | -0.607815 |
| ASSET:BTCUSDT | 5m | holdout | calibrated | charter | 14.0 | 14.0 | 2401 | 4.0232 | 0.0179 | 35742 | 2268 | 0.102235 | 0.997106 | -0.894870 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 2401 | 14.0812 | 0.0008 | 35742 | 2268 | 0.102235 | 0.284887 | -0.182652 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 996 | 11.2301 | 0.0010 | 26913 | 986 | 0.112086 | 0.703420 | -0.591333 | — | — | FAIL | frozen3.0 | FAIL | -0.594256 |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | charter | 14.0 | 14.0 | 996 | 8.0215 | 0.0010 | 26913 | 986 | 0.112086 | 0.984787 | -0.872701 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 996 | 28.0753 | 0.0000 | 26913 | 986 | 0.112086 | 0.281368 | -0.169282 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 6092 | 9.4751 | 0.0039 | 97418 | 5799 | 0.192475 | 0.394698 | -0.202222 | — | — | FAIL | tuning | FAIL | -0.181604 |
| ASSET:ETHUSDT | 5m | ALL | calibrated | charter | 14.0 | 14.0 | 6092 | 6.7679 | 0.0072 | 97418 | 5799 | 0.192475 | 0.552577 | -0.360101 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 6092 | 23.6876 | 0.0003 | 97418 | 5799 | 0.192475 | 0.157879 | 0.034596 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2822 | 17.9021 | 0.0000 | 70272 | 2798 | 0.173673 | 0.402417 | -0.228744 | — | — | FAIL | frozen3.0 | FAIL | -0.228094 |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | charter | 14.0 | 14.0 | 2822 | 12.7872 | 0.0000 | 70272 | 2798 | 0.173673 | 0.563384 | -0.389711 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2822 | 44.7553 | 0.0000 | 70272 | 2798 | 0.173673 | 0.160967 | 0.012706 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 3844 | 10.0665 | 0.0049 | 63656 | 3651 | 0.227174 | 0.357065 | -0.129892 | — | — | FAIL | tuning | FAIL | -0.103370 |
| ASSET:ETHUSDT | 5m | tuning | calibrated | charter | 14.0 | 14.0 | 3844 | 7.1904 | 0.0078 | 63656 | 3651 | 0.227174 | 0.499892 | -0.272718 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 3844 | 25.1664 | 0.0005 | 63656 | 3651 | 0.227174 | 0.142826 | 0.084348 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1881 | 19.0576 | 0.0000 | 45443 | 1866 | 0.207038 | 0.367639 | -0.160602 | — | — | FAIL | frozen3.0 | FAIL | -0.160602 |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | charter | 14.0 | 14.0 | 1881 | 13.6126 | 0.0000 | 45443 | 1866 | 0.207038 | 0.514695 | -0.307657 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1881 | 47.6440 | 0.0000 | 45443 | 1866 | 0.207038 | 0.147056 | 0.059982 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 2248 | 8.5036 | 0.0022 | 33762 | 2148 | 0.119438 | 0.463857 | -0.344419 | — | — | FAIL | tuning | FAIL | -0.332207 |
| ASSET:ETHUSDT | 5m | holdout | calibrated | charter | 14.0 | 14.0 | 2248 | 6.0740 | 0.0062 | 33762 | 2148 | 0.119438 | 0.649399 | -0.529962 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 2248 | 21.2589 | 0.0000 | 33762 | 2148 | 0.119438 | 0.185543 | -0.066105 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 941 | 16.5203 | 0.0000 | 24829 | 932 | 0.103609 | 0.461592 | -0.357983 | — | — | FAIL | frozen3.0 | FAIL | -0.357131 |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | charter | 14.0 | 14.0 | 941 | 11.8002 | 0.0000 | 24829 | 932 | 0.103609 | 0.646229 | -0.542620 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 941 | 41.3007 | 0.0000 | 24829 | 932 | 0.103609 | 0.184637 | -0.081028 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 5127 | 16.2324 | 0.0000 | 87771 | 4978 | 0.149564 | 0.283352 | -0.133788 | — | — | FAIL | tuning | FAIL | -0.135412 |
| ASSET:SOLUSDT | 5m | ALL | calibrated | charter | 20.0 | 20.0 | 5127 | 8.1162 | 0.0010 | 87771 | 4978 | 0.149564 | 0.566703 | -0.417139 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 5127 | 40.5809 | 0.0000 | 87771 | 4978 | 0.149564 | 0.113341 | 0.036223 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2444 | 28.7014 | 0.0000 | 69103 | 2429 | 0.128109 | 0.284337 | -0.156228 | — | — | FAIL | frozen3.0 | FAIL | -0.157347 |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 2444 | 14.3507 | 0.0000 | 69103 | 2429 | 0.128109 | 0.568675 | -0.440565 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2444 | 71.7535 | 0.0000 | 69103 | 2429 | 0.128109 | 0.113735 | 0.014374 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 3170 | 19.4300 | 0.0000 | 54364 | 3071 | 0.157346 | 0.237829 | -0.080483 | — | — | FAIL | tuning | FAIL | -0.080483 |
| ASSET:SOLUSDT | 5m | tuning | calibrated | charter | 20.0 | 20.0 | 3170 | 9.7150 | 0.0003 | 54364 | 3071 | 0.157346 | 0.475658 | -0.318313 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 3170 | 48.5751 | 0.0000 | 54364 | 3071 | 0.157346 | 0.095132 | 0.062214 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1555 | 33.3502 | 0.0000 | 41387 | 1545 | 0.079200 | 0.236208 | -0.157009 | — | — | FAIL | frozen3.0 | FAIL | -0.157009 |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 1555 | 16.6751 | 0.0000 | 41387 | 1545 | 0.079200 | 0.472417 | -0.393217 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1555 | 83.3754 | 0.0000 | 41387 | 1545 | 0.079200 | 0.094483 | -0.015284 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 1957 | 11.9421 | 0.0000 | 33407 | 1907 | 0.132703 | 0.366942 | -0.234240 | — | — | FAIL | tuning | FAIL | -0.236669 |
| ASSET:SOLUSDT | 5m | holdout | calibrated | charter | 20.0 | 20.0 | 1957 | 5.9710 | 0.0020 | 33407 | 1907 | 0.132703 | 0.733885 | -0.601182 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 1957 | 29.8552 | 0.0000 | 33407 | 1907 | 0.132703 | 0.146777 | -0.014074 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 889 | 20.3556 | 0.0000 | 27716 | 884 | 0.191973 | 0.364943 | -0.172970 | — | — | FAIL | frozen3.0 | FAIL | -0.174972 |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 889 | 10.1778 | 0.0000 | 27716 | 884 | 0.191973 | 0.729887 | -0.537914 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 889 | 50.8890 | 0.0000 | 27716 | 884 | 0.191973 | 0.145977 | 0.045996 | — | — | PASS | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 4860 | 19.4397 | 0.0000 | 96272 | 4745 | 0.102460 | 0.239818 | -0.137358 | — | — | FAIL | tuning | FAIL | -0.137270 |
| ASSET:NEARUSDT | 5m | ALL | calibrated | charter | 20.0 | 20.0 | 4860 | 9.7199 | 0.0000 | 96272 | 4745 | 0.102460 | 0.479635 | -0.377175 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 4860 | 48.5993 | 0.0000 | 96272 | 4745 | 0.102460 | 0.095927 | 0.006533 | — | — | PASS | tuning | — | — |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2262 | 33.5396 | 0.0000 | 76300 | 2254 | 0.151447 | 0.235790 | -0.084343 | — | — | FAIL | frozen3.0 | FAIL | -0.086702 |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 2262 | 16.7698 | 0.0000 | 76300 | 2254 | 0.151447 | 0.471579 | -0.320132 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2262 | 83.8490 | 0.0000 | 76300 | 2254 | 0.151447 | 0.094316 | 0.057131 | — | — | PASS | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 3043 | 20.9615 | 0.0000 | 59469 | 2961 | 0.137320 | 0.224229 | -0.086909 | — | — | FAIL | tuning | FAIL | -0.086909 |
| ASSET:NEARUSDT | 5m | tuning | calibrated | charter | 20.0 | 20.0 | 3043 | 10.4808 | 0.0000 | 59469 | 2961 | 0.137320 | 0.448458 | -0.311138 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 3043 | 52.4038 | 0.0000 | 59469 | 2961 | 0.137320 | 0.089692 | 0.047628 | — | — | PASS | tuning | — | — |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1422 | 36.2904 | 0.0000 | 46731 | 1415 | 0.161702 | 0.222497 | -0.060795 | — | — | FAIL | frozen3.0 | FAIL | -0.060795 |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 1422 | 18.1452 | 0.0000 | 46731 | 1415 | 0.161702 | 0.444993 | -0.283291 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1422 | 90.7260 | 0.0000 | 46731 | 1415 | 0.161702 | 0.088999 | 0.072703 | — | — | PASS | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 1817 | 17.3913 | 0.0000 | 36803 | 1785 | 0.000000 | 0.260612 | -0.260612 | — | — | FAIL | tuning | FAIL | -0.261102 |
| ASSET:NEARUSDT | 5m | holdout | calibrated | charter | 20.0 | 20.0 | 1817 | 8.6957 | 0.0000 | 36803 | 1785 | 0.000000 | 0.521224 | -0.521224 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 1817 | 43.4783 | 0.0000 | 36803 | 1785 | 0.000000 | 0.104245 | -0.104245 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 840 | 29.3073 | 0.0000 | 29569 | 839 | 0.134539 | 0.254329 | -0.119790 | — | — | FAIL | frozen3.0 | FAIL | -0.125278 |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 840 | 14.6536 | 0.0000 | 29569 | 839 | 0.134539 | 0.508658 | -0.374119 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 840 | 73.2681 | 0.0000 | 29569 | 839 | 0.134539 | 0.101732 | 0.032807 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 5530 | 16.8690 | 0.0000 | 106579 | 5396 | 0.157455 | 0.269462 | -0.112006 | — | — | FAIL | tuning | FAIL | -0.113128 |
| ASSET:ZECUSDT | 5m | ALL | calibrated | charter | 20.0 | 20.0 | 5530 | 8.4345 | 0.0005 | 106579 | 5396 | 0.157455 | 0.538924 | -0.381468 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 5530 | 42.1724 | 0.0000 | 106579 | 5396 | 0.157455 | 0.107785 | 0.049671 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2676 | 28.9017 | 0.0000 | 83668 | 2654 | 0.148904 | 0.266956 | -0.118052 | — | — | FAIL | frozen3.0 | FAIL | -0.117025 |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 2676 | 14.4508 | 0.0000 | 83668 | 2654 | 0.148904 | 0.533912 | -0.385008 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2676 | 72.2542 | 0.0000 | 83668 | 2654 | 0.148904 | 0.106782 | 0.042122 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 3609 | 15.9297 | 0.0000 | 71567 | 3526 | 0.198106 | 0.285038 | -0.086932 | — | — | FAIL | tuning | FAIL | -0.086932 |
| ASSET:ZECUSDT | 5m | tuning | calibrated | charter | 20.0 | 20.0 | 3609 | 7.9648 | 0.0008 | 71567 | 3526 | 0.198106 | 0.570077 | -0.371970 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 3609 | 39.8242 | 0.0000 | 71567 | 3526 | 0.198106 | 0.114015 | 0.084091 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1744 | 27.6198 | 0.0000 | 55490 | 1732 | 0.211788 | 0.281282 | -0.069494 | — | — | FAIL | frozen3.0 | FAIL | -0.069494 |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 1744 | 13.8099 | 0.0000 | 55490 | 1732 | 0.211788 | 0.562564 | -0.350776 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1744 | 69.0496 | 0.0000 | 55490 | 1732 | 0.211788 | 0.112513 | 0.099275 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 1921 | 18.5806 | 0.0000 | 35012 | 1870 | 0.086444 | 0.243083 | -0.156639 | — | — | FAIL | tuning | FAIL | -0.159729 |
| ASSET:ZECUSDT | 5m | holdout | calibrated | charter | 20.0 | 20.0 | 1921 | 9.2903 | 0.0000 | 35012 | 1870 | 0.086444 | 0.486167 | -0.399723 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 1921 | 46.4516 | 0.0000 | 35012 | 1870 | 0.086444 | 0.097233 | -0.010789 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 932 | 30.7648 | 0.0000 | 28178 | 923 | 0.026418 | 0.243304 | -0.216886 | — | — | FAIL | frozen3.0 | FAIL | -0.210699 |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 932 | 15.3824 | 0.0000 | 28178 | 923 | 0.026418 | 0.486608 | -0.460190 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 932 | 76.9119 | 0.0000 | 28178 | 923 | 0.026418 | 0.097322 | -0.070904 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | taker | 10.0 | 10.0 | 28077 | 12.6548 | 0.0018 | 492387 | 27059 | 0.177254 | 0.555925 | -0.378671 | — | — | FAIL | tuning | FAIL | -0.377233 |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | charter | 14.0 | 20.0 | 28077 | 7.3256 | 0.0048 | 492387 | 27059 | 0.177254 | 0.778295 | -0.601041 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | maker | 4.0 | 4.0 | 28077 | 31.6370 | 0.0001 | 492387 | 27059 | 0.177254 | 0.222370 | -0.045116 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 13039 | 23.2558 | 0.0001 | 376825 | 12945 | 0.167420 | 0.541170 | -0.373749 | — | — | FAIL | frozen3.0 | FAIL | -0.374017 |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | charter | 14.0 | 20.0 | 13039 | 13.3239 | 0.0002 | 376825 | 12945 | 0.167420 | 0.757638 | -0.590217 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 13039 | 58.1395 | 0.0000 | 376825 | 12945 | 0.167420 | 0.216468 | -0.049048 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | taker | 10.0 | 10.0 | 17733 | 13.5556 | 0.0019 | 317661 | 17082 | 0.219412 | 0.485336 | -0.265924 | — | — | FAIL | tuning | FAIL | -0.261792 |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | charter | 14.0 | 20.0 | 17733 | 7.8458 | 0.0042 | 317661 | 17082 | 0.219412 | 0.679471 | -0.460059 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | maker | 4.0 | 4.0 | 17733 | 33.8890 | 0.0001 | 317661 | 17082 | 0.219412 | 0.194135 | 0.025277 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 8441 | 24.9345 | 0.0000 | 239620 | 8382 | 0.196802 | 0.465561 | -0.268759 | — | — | FAIL | frozen3.0 | FAIL | -0.268759 |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | charter | 14.0 | 20.0 | 8441 | 14.2520 | 0.0001 | 239620 | 8382 | 0.196802 | 0.651786 | -0.454984 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 8441 | 62.3362 | 0.0000 | 239620 | 8382 | 0.196802 | 0.186225 | 0.010578 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | taker | 10.0 | 10.0 | 10344 | 11.3326 | 0.0016 | 174726 | 9978 | 0.096495 | 0.712218 | -0.615724 | FAIL | FAIL | — | tuning | FAIL | -0.614783 |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | charter | 14.0 | 20.0 | 10344 | 6.5059 | 0.0059 | 174726 | 9978 | 0.096495 | 0.997106 | -0.900611 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | maker | 4.0 | 4.0 | 10344 | 28.3315 | 0.0002 | 174726 | 9978 | 0.096495 | 0.284887 | -0.188393 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 4598 | 20.6711 | 0.0002 | 137205 | 4564 | 0.116245 | 0.703420 | -0.587175 | — | — | FAIL | frozen3.0 | FAIL | -0.588450 |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | charter | 14.0 | 20.0 | 4598 | 11.6985 | 0.0002 | 137205 | 4564 | 0.116245 | 0.984787 | -0.868543 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 4598 | 51.6778 | 0.0000 | 137205 | 4564 | 0.116245 | 0.281368 | -0.165123 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 2030 | 13.7168 | 0.0000 | 31244 | 1936 | 0.221289 | 0.296674 | -0.075385 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | ALL | calibrated | charter | 14.0 | 14.0 | 2030 | 9.7977 | 0.0010 | 31244 | 1936 | 0.221289 | 0.415344 | -0.194055 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 2030 | 34.2920 | 0.0000 | 31244 | 1936 | 0.221289 | 0.118670 | 0.102619 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 918 | 24.6447 | 0.0000 | 23290 | 905 | 0.217599 | 0.288581 | -0.070982 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | charter | 14.0 | 14.0 | 918 | 17.6034 | 0.0000 | 23290 | 905 | 0.217599 | 0.404014 | -0.186415 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 918 | 61.6119 | 0.0000 | 23290 | 905 | 0.217599 | 0.115433 | 0.102167 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 1340 | 15.3089 | 0.0000 | 20778 | 1276 | 0.294331 | 0.265326 | 0.029004 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 15m | tuning | calibrated | charter | 14.0 | 14.0 | 1340 | 10.9349 | 0.0000 | 20778 | 1276 | 0.294331 | 0.371457 | -0.077126 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 1340 | 38.2721 | 0.0000 | 20778 | 1276 | 0.294331 | 0.106130 | 0.188200 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 611 | 27.6654 | 0.0000 | 15487 | 601 | 0.294081 | 0.263425 | 0.030656 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | charter | 14.0 | 14.0 | 611 | 19.7610 | 0.0000 | 15487 | 601 | 0.294081 | 0.368795 | -0.074714 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 611 | 69.1635 | 0.0000 | 15487 | 601 | 0.294081 | 0.105370 | 0.188711 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 690 | 11.4045 | 0.0000 | 10466 | 660 | 0.054541 | 0.361930 | -0.307388 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | holdout | calibrated | charter | 14.0 | 14.0 | 690 | 8.1460 | 0.0029 | 10466 | 660 | 0.054541 | 0.506702 | -0.452160 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 690 | 28.5111 | 0.0000 | 10466 | 660 | 0.054541 | 0.144772 | -0.090231 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 307 | 20.7766 | 0.0000 | 7803 | 304 | 0.028028 | 0.334177 | -0.306149 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | charter | 14.0 | 14.0 | 307 | 14.8404 | 0.0000 | 7803 | 304 | 0.028028 | 0.467847 | -0.439820 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 307 | 51.9415 | 0.0000 | 7803 | 304 | 0.028028 | 0.133671 | -0.105643 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 1627 | 22.0801 | 0.0000 | 27897 | 1565 | 0.147421 | 0.221388 | -0.073967 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | ALL | calibrated | charter | 14.0 | 14.0 | 1627 | 15.7715 | 0.0000 | 27897 | 1565 | 0.147421 | 0.309943 | -0.162522 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 1627 | 55.2003 | 0.0000 | 27897 | 1565 | 0.147421 | 0.088555 | 0.058866 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 865 | 33.5938 | 0.0000 | 23122 | 853 | 0.166173 | 0.217857 | -0.051684 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | charter | 14.0 | 14.0 | 865 | 23.9955 | 0.0000 | 23122 | 853 | 0.166173 | 0.305000 | -0.138827 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 865 | 83.9844 | 0.0000 | 23122 | 853 | 0.166173 | 0.087143 | 0.079030 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 1109 | 23.6379 | 0.0000 | 18475 | 1069 | 0.157572 | 0.209240 | -0.051669 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | tuning | calibrated | charter | 14.0 | 14.0 | 1109 | 16.8842 | 0.0000 | 18475 | 1069 | 0.157572 | 0.292936 | -0.135365 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 1109 | 59.0948 | 0.0000 | 18475 | 1069 | 0.157572 | 0.083696 | 0.073876 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 579 | 35.2849 | 0.0000 | 15535 | 570 | 0.195702 | 0.204497 | -0.008796 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | charter | 14.0 | 14.0 | 579 | 25.2035 | 0.0000 | 15535 | 570 | 0.195702 | 0.286296 | -0.090595 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 579 | 88.2123 | 0.0000 | 15535 | 570 | 0.195702 | 0.081799 | 0.113903 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 518 | 19.7961 | 0.0000 | 9422 | 496 | 0.132725 | 0.241434 | -0.108709 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | holdout | calibrated | charter | 14.0 | 14.0 | 518 | 14.1401 | 0.0000 | 9422 | 496 | 0.132725 | 0.338007 | -0.205282 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 518 | 49.4902 | 0.0000 | 9422 | 496 | 0.132725 | 0.096573 | 0.036151 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 286 | 30.6744 | 0.0000 | 7587 | 283 | 0.122994 | 0.240772 | -0.117779 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | charter | 14.0 | 14.0 | 286 | 21.9103 | 0.0000 | 7587 | 283 | 0.122994 | 0.337081 | -0.214087 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 286 | 76.6861 | 0.0000 | 7587 | 283 | 0.122994 | 0.096309 | 0.026685 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 1689 | 27.7524 | 0.0000 | 28351 | 1635 | 0.073786 | 0.155608 | -0.081822 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | ALL | calibrated | charter | 20.0 | 20.0 | 1689 | 13.8762 | 0.0000 | 28351 | 1635 | 0.073786 | 0.311216 | -0.237430 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 1689 | 69.3810 | 0.0000 | 28351 | 1635 | 0.073786 | 0.062243 | 0.011543 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 772 | 51.0736 | 0.0000 | 21633 | 765 | 0.078439 | 0.153220 | -0.074780 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 772 | 25.5368 | 0.0000 | 21633 | 765 | 0.078439 | 0.306440 | -0.228000 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 772 | 127.6839 | 0.0000 | 21633 | 765 | 0.078439 | 0.061288 | 0.017151 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 1072 | 32.8120 | 0.0000 | 16612 | 1034 | 0.050545 | 0.129752 | -0.079207 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | tuning | calibrated | charter | 20.0 | 20.0 | 1072 | 16.4060 | 0.0000 | 16612 | 1034 | 0.050545 | 0.259504 | -0.208959 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 1072 | 82.0300 | 0.0000 | 16612 | 1034 | 0.050545 | 0.051901 | -0.001356 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 483 | 62.4591 | 0.0000 | 13314 | 476 | 0.088282 | 0.133777 | -0.045494 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 483 | 31.2295 | 0.0000 | 13314 | 476 | 0.088282 | 0.267553 | -0.179271 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 483 | 156.1477 | 0.0000 | 13314 | 476 | 0.088282 | 0.053511 | 0.034772 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 617 | 20.2294 | 0.0000 | 11739 | 601 | 0.099994 | 0.195935 | -0.095941 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | holdout | calibrated | charter | 20.0 | 20.0 | 617 | 10.1147 | 0.0000 | 11739 | 601 | 0.099994 | 0.391870 | -0.291876 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 617 | 50.5734 | 0.0000 | 11739 | 601 | 0.099994 | 0.078374 | 0.021620 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 289 | 36.7293 | 0.0000 | 8319 | 289 | 0.056759 | 0.186424 | -0.129665 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 289 | 18.3647 | 0.0000 | 8319 | 289 | 0.056759 | 0.372849 | -0.316089 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 289 | 91.8233 | 0.0000 | 8319 | 289 | 0.056759 | 0.074570 | -0.017811 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 1629 | 33.6991 | 0.0000 | 31136 | 1588 | 0.046023 | 0.133148 | -0.087124 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | ALL | calibrated | charter | 20.0 | 20.0 | 1629 | 16.8495 | 0.0000 | 31136 | 1588 | 0.046023 | 0.266295 | -0.220272 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 1629 | 84.2476 | 0.0000 | 31136 | 1588 | 0.046023 | 0.053259 | -0.007236 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 740 | 57.5759 | 0.0000 | 24531 | 733 | 0.000000 | 0.133460 | -0.133460 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 740 | 28.7879 | 0.0000 | 24531 | 733 | 0.000000 | 0.266920 | -0.266920 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 740 | 143.9397 | 0.0000 | 24531 | 733 | 0.000000 | 0.053384 | -0.053384 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 1047 | 36.0775 | 0.0000 | 18881 | 1019 | 0.065608 | 0.125429 | -0.059821 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | tuning | calibrated | charter | 20.0 | 20.0 | 1047 | 18.0388 | 0.0000 | 18881 | 1019 | 0.065608 | 0.250859 | -0.185250 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 1047 | 90.1938 | 0.0000 | 18881 | 1019 | 0.065608 | 0.050172 | 0.015436 | — | — | PASS | tuning | — | — |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 466 | 63.1751 | 0.0000 | 15369 | 460 | 0.075327 | 0.121882 | -0.046555 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 466 | 31.5876 | 0.0000 | 15369 | 460 | 0.075327 | 0.243765 | -0.168438 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 466 | 157.9378 | 0.0000 | 15369 | 460 | 0.075327 | 0.048753 | 0.026574 | — | — | PASS | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 582 | 30.0710 | 0.0000 | 12255 | 570 | 0.000000 | 0.142773 | -0.142773 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | holdout | calibrated | charter | 20.0 | 20.0 | 582 | 15.0355 | 0.0000 | 12255 | 570 | 0.000000 | 0.285545 | -0.285545 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 582 | 75.1775 | 0.0000 | 12255 | 570 | 0.000000 | 0.057109 | -0.057109 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 274 | 51.9813 | 0.0000 | 9162 | 273 | -0.091353 | 0.148525 | -0.239878 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 274 | 25.9907 | 0.0000 | 9162 | 273 | -0.091353 | 0.297051 | -0.388404 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 274 | 129.9533 | 0.0000 | 9162 | 273 | -0.091353 | 0.059410 | -0.150763 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 1798 | 30.6526 | 0.0000 | 35302 | 1744 | 0.112388 | 0.146952 | -0.034564 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | ALL | calibrated | charter | 20.0 | 20.0 | 1798 | 15.3263 | 0.0000 | 35302 | 1744 | 0.112388 | 0.293904 | -0.181516 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 1798 | 76.6316 | 0.0000 | 35302 | 1744 | 0.112388 | 0.058781 | 0.053607 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 814 | 54.7801 | 0.0000 | 27783 | 808 | 0.057025 | 0.146237 | -0.089212 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | charter | 20.0 | 20.0 | 814 | 27.3901 | 0.0000 | 27783 | 808 | 0.057025 | 0.292474 | -0.235449 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 814 | 136.9503 | 0.0000 | 27783 | 808 | 0.057025 | 0.058495 | -0.001470 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 1156 | 29.2720 | 0.0000 | 23213 | 1124 | 0.172487 | 0.155435 | 0.017052 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 15m | tuning | calibrated | charter | 20.0 | 20.0 | 1156 | 14.6360 | 0.0000 | 23213 | 1124 | 0.172487 | 0.310870 | -0.138383 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 1156 | 73.1800 | 0.0000 | 23213 | 1124 | 0.172487 | 0.062174 | 0.110313 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 530 | 52.3165 | 0.0000 | 18793 | 526 | 0.101233 | 0.152393 | -0.051161 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | charter | 20.0 | 20.0 | 530 | 26.1582 | 0.0000 | 18793 | 526 | 0.101233 | 0.304786 | -0.203554 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 530 | 130.7911 | 0.0000 | 18793 | 526 | 0.101233 | 0.060957 | 0.040275 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 642 | 33.1217 | 0.0000 | 12089 | 621 | 0.000000 | 0.133141 | -0.133141 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | holdout | calibrated | charter | 20.0 | 20.0 | 642 | 16.5608 | 0.0000 | 12089 | 621 | 0.000000 | 0.266282 | -0.266282 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 642 | 82.8042 | 0.0000 | 12089 | 621 | 0.000000 | 0.053256 | -0.053256 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 284 | 57.8866 | 0.0000 | 8990 | 283 | -0.020194 | 0.135639 | -0.155833 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | charter | 20.0 | 20.0 | 284 | 28.9433 | 0.0000 | 8990 | 283 | -0.020194 | 0.271278 | -0.291472 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 284 | 144.7164 | 0.0000 | 8990 | 283 | -0.020194 | 0.054256 | -0.074449 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | taker | 10.0 | 10.0 | 8773 | 24.8201 | 0.0000 | 153930 | 8468 | 0.124683 | 0.296674 | -0.171991 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | charter | 14.0 | 20.0 | 8773 | 14.1410 | 0.0002 | 153930 | 8468 | 0.124683 | 0.415344 | -0.290661 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | maker | 4.0 | 4.0 | 8773 | 62.0502 | 0.0000 | 153930 | 8468 | 0.124683 | 0.118670 | 0.006013 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | taker | 10.0 | 10.0 | 4109 | 42.5055 | 0.0000 | 120359 | 4064 | 0.107349 | 0.288581 | -0.181233 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | charter | 14.0 | 20.0 | 4109 | 24.3610 | 0.0000 | 120359 | 4064 | 0.107349 | 0.404014 | -0.296665 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | maker | 4.0 | 4.0 | 4109 | 106.2638 | 0.0000 | 120359 | 4064 | 0.107349 | 0.115433 | -0.008084 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | taker | 10.0 | 10.0 | 5724 | 26.4308 | 0.0000 | 97959 | 5522 | 0.158074 | 0.265326 | -0.107252 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | charter | 14.0 | 20.0 | 5724 | 15.1689 | 0.0000 | 97959 | 5522 | 0.158074 | 0.371457 | -0.213382 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | maker | 4.0 | 4.0 | 5724 | 66.0771 | 0.0000 | 97959 | 5522 | 0.158074 | 0.106130 | 0.051944 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | taker | 10.0 | 10.0 | 2669 | 44.9591 | 0.0000 | 78498 | 2633 | 0.154333 | 0.263425 | -0.109093 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | charter | 14.0 | 20.0 | 2669 | 26.0257 | 0.0000 | 78498 | 2633 | 0.154333 | 0.368795 | -0.214463 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | maker | 4.0 | 4.0 | 2669 | 112.3978 | 0.0000 | 78498 | 2633 | 0.154333 | 0.105370 | 0.048963 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | taker | 10.0 | 10.0 | 3049 | 21.8723 | 0.0000 | 55971 | 2948 | 0.058852 | 0.361930 | -0.303078 | FAIL | FAIL | — | tuning | — | — |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | charter | 14.0 | 20.0 | 3049 | 12.4956 | 0.0007 | 55971 | 2948 | 0.058852 | 0.506702 | -0.447850 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | maker | 4.0 | 4.0 | 3049 | 54.6807 | 0.0000 | 55971 | 2948 | 0.058852 | 0.144772 | -0.085920 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1440 | 37.9076 | 0.0000 | 41861 | 1432 | 0.011479 | 0.334177 | -0.322697 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | charter | 14.0 | 20.0 | 1440 | 21.9892 | 0.0000 | 41861 | 1432 | 0.011479 | 0.467847 | -0.456368 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1440 | 94.7691 | 0.0000 | 41861 | 1432 | 0.011479 | 0.133671 | -0.122192 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 522 | 30.7389 | 0.0000 | 7750 | 491 | 0.216758 | 0.134821 | 0.081937 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | ALL | calibrated | charter | 14.0 | 14.0 | 522 | 21.9564 | 0.0000 | 7750 | 491 | 0.216758 | 0.188750 | 0.028008 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 522 | 76.8473 | 0.0000 | 7750 | 491 | 0.216758 | 0.053929 | 0.162829 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 223 | 54.0224 | 0.0000 | 6677 | 223 | 0.292410 | 0.132569 | 0.159841 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 223 | 38.5875 | 0.0000 | 6677 | 223 | 0.292410 | 0.185596 | 0.106813 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 223 | 135.0561 | 0.0000 | 6677 | 223 | 0.292410 | 0.053028 | 0.239382 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 347 | 33.2824 | 0.0000 | 5183 | 329 | 0.268374 | 0.120354 | 0.148020 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | tuning | calibrated | charter | 14.0 | 14.0 | 347 | 23.7731 | 0.0000 | 5183 | 329 | 0.268374 | 0.168495 | 0.099879 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 347 | 83.2059 | 0.0000 | 5183 | 329 | 0.268374 | 0.048142 | 0.220233 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 152 | 58.2240 | 0.0000 | 4619 | 152 | 0.323559 | 0.119332 | 0.204227 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 152 | 41.5886 | 0.0000 | 4619 | 152 | 0.323559 | 0.167064 | 0.156494 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 152 | 145.5600 | 0.0000 | 4619 | 152 | 0.323559 | 0.047733 | 0.275826 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 175 | 26.1343 | 0.0000 | 2567 | 162 | 0.081508 | 0.167605 | -0.086097 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 1h | holdout | calibrated | charter | 14.0 | 14.0 | 175 | 18.6673 | 0.0000 | 2567 | 162 | 0.081508 | 0.234647 | -0.153139 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 175 | 65.3357 | 0.0000 | 2567 | 162 | 0.081508 | 0.067042 | 0.014466 | — | — | PASS | tuning | — | — |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 71 | 46.3189 | 0.0000 | 2058 | 71 | 0.204552 | 0.159302 | 0.045250 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 71 | 33.0850 | 0.0000 | 2058 | 71 | 0.204552 | 0.223023 | -0.018471 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 71 | 115.7973 | 0.0000 | 2058 | 71 | 0.204552 | 0.063721 | 0.140831 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 441 | 45.9451 | 0.0000 | 6707 | 420 | 0.074413 | 0.105264 | -0.030851 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 1h | ALL | calibrated | charter | 14.0 | 14.0 | 441 | 32.8179 | 0.0000 | 6707 | 420 | 0.074413 | 0.147370 | -0.072957 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 441 | 114.8627 | 0.0000 | 6707 | 420 | 0.074413 | 0.042106 | 0.032307 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 231 | 65.7703 | 0.0000 | 5788 | 227 | 0.146450 | 0.105667 | 0.040784 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 231 | 46.9788 | 0.0000 | 5788 | 227 | 0.146450 | 0.147934 | -0.001483 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 231 | 164.4256 | 0.0000 | 5788 | 227 | 0.146450 | 0.042267 | 0.104184 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 301 | 49.5137 | 0.0000 | 4553 | 289 | 0.048887 | 0.099366 | -0.050479 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 1h | tuning | calibrated | charter | 14.0 | 14.0 | 301 | 35.3670 | 0.0000 | 4553 | 289 | 0.048887 | 0.139112 | -0.090225 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 301 | 123.7843 | 0.0000 | 4553 | 289 | 0.048887 | 0.039746 | 0.009140 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 153 | 69.5490 | 0.0000 | 4014 | 150 | 0.057969 | 0.100090 | -0.042121 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 153 | 49.6778 | 0.0000 | 4014 | 150 | 0.057969 | 0.140127 | -0.082157 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 153 | 173.8724 | 0.0000 | 4014 | 150 | 0.057969 | 0.040036 | 0.017933 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 140 | 41.9953 | 0.0000 | 2154 | 131 | 0.116207 | 0.113949 | 0.002258 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 1h | holdout | calibrated | charter | 14.0 | 14.0 | 140 | 29.9966 | 0.0000 | 2154 | 131 | 0.116207 | 0.159528 | -0.043321 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 140 | 104.9882 | 0.0000 | 2154 | 131 | 0.116207 | 0.045580 | 0.070628 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 78 | 60.5319 | 0.0000 | 1774 | 77 | 0.308841 | 0.113183 | 0.195658 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 78 | 43.2371 | 0.0000 | 1774 | 77 | 0.308841 | 0.158456 | 0.150385 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 78 | 151.3298 | 0.0000 | 1774 | 77 | 0.308841 | 0.045273 | 0.263568 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 441 | 59.1951 | 0.0000 | 6705 | 419 | 0.061200 | 0.075201 | -0.014001 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 441 | 29.5975 | 0.0000 | 6705 | 419 | 0.061200 | 0.150402 | -0.089203 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 441 | 147.9877 | 0.0000 | 6705 | 419 | 0.061200 | 0.030080 | 0.031119 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 203 | 99.8668 | 0.0000 | 6260 | 202 | -0.007467 | 0.077878 | -0.085344 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 203 | 49.9334 | 0.0000 | 6260 | 202 | -0.007467 | 0.155755 | -0.163222 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 203 | 249.6669 | 0.0000 | 6260 | 202 | -0.007467 | 0.031151 | -0.038618 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 261 | 72.8077 | 0.0000 | 4507 | 250 | 0.087478 | 0.066638 | 0.020840 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 261 | 36.4039 | 0.0000 | 4507 | 250 | 0.087478 | 0.133277 | -0.045798 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 261 | 182.0194 | 0.0000 | 4507 | 250 | 0.087478 | 0.026655 | 0.060823 | — | — | PASS | tuning | — | — |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 130 | 114.8659 | 0.0000 | 4107 | 129 | -0.086222 | 0.068600 | -0.154822 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 130 | 57.4329 | 0.0000 | 4107 | 129 | -0.086222 | 0.137201 | -0.223422 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 130 | 287.1647 | 0.0000 | 4107 | 129 | -0.086222 | 0.027440 | -0.113662 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 180 | 44.4872 | 0.0000 | 2198 | 170 | -0.018264 | 0.096452 | -0.114715 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 180 | 22.2436 | 0.0000 | 2198 | 170 | -0.018264 | 0.192903 | -0.211167 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 180 | 111.2181 | 0.0000 | 2198 | 170 | -0.018264 | 0.038581 | -0.056844 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 73 | 77.8241 | 0.0000 | 2153 | 74 | 0.188905 | 0.094505 | 0.094400 | — | — | PASS | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 73 | 38.9121 | 0.0000 | 2153 | 74 | 0.188905 | 0.189010 | -0.000105 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 73 | 194.5603 | 0.0000 | 2153 | 74 | 0.188905 | 0.037802 | 0.151103 | — | — | PASS | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 438 | 69.1910 | 0.0000 | 6896 | 419 | -0.096903 | 0.064751 | -0.161654 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 438 | 34.5955 | 0.0000 | 6896 | 419 | -0.096903 | 0.129502 | -0.226404 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 438 | 172.9775 | 0.0000 | 6896 | 419 | -0.096903 | 0.025900 | -0.122803 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 211 | 122.8561 | 0.0000 | 5987 | 211 | -0.135507 | 0.066128 | -0.201636 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 211 | 61.4281 | 0.0000 | 5987 | 211 | -0.135507 | 0.132257 | -0.267764 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 211 | 307.1404 | 0.0000 | 5987 | 211 | -0.135507 | 0.026451 | -0.161959 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 264 | 78.1620 | 0.0000 | 4483 | 252 | -0.053741 | 0.058961 | -0.112702 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 264 | 39.0810 | 0.0000 | 4483 | 252 | -0.053741 | 0.117922 | -0.171663 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 264 | 195.4051 | 0.0000 | 4483 | 252 | -0.053741 | 0.023585 | -0.077325 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 136 | 132.2423 | 0.0000 | 3412 | 136 | -0.257429 | 0.058189 | -0.315618 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 136 | 66.1211 | 0.0000 | 3412 | 136 | -0.257429 | 0.116379 | -0.373808 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 136 | 330.6057 | 0.0000 | 3412 | 136 | -0.257429 | 0.023276 | -0.280705 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 174 | 56.7640 | 0.0000 | 2413 | 167 | -0.166189 | 0.071917 | -0.238106 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 174 | 28.3820 | 0.0000 | 2413 | 167 | -0.166189 | 0.143833 | -0.310023 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 174 | 141.9099 | 0.0000 | 2413 | 167 | -0.166189 | 0.028767 | -0.194956 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 75 | 118.0977 | 0.0000 | 2575 | 75 | 0.000000 | 0.073960 | -0.073960 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 75 | 59.0488 | 0.0000 | 2575 | 75 | 0.000000 | 0.147920 | -0.147920 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 75 | 295.2442 | 0.0000 | 2575 | 75 | 0.000000 | 0.029584 | -0.029584 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 411 | 71.8808 | 0.0000 | 7883 | 391 | 0.009899 | 0.070463 | -0.060564 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 411 | 35.9404 | 0.0000 | 7883 | 391 | 0.009899 | 0.140927 | -0.131028 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 411 | 179.7020 | 0.0000 | 7883 | 391 | 0.009899 | 0.028185 | -0.018286 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 220 | 107.8701 | 0.0000 | 6354 | 218 | 0.117702 | 0.070179 | 0.047522 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 220 | 53.9350 | 0.0000 | 6354 | 218 | 0.117702 | 0.140358 | -0.022657 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 220 | 269.6752 | 0.0000 | 6354 | 218 | 0.117702 | 0.028072 | 0.089630 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 264 | 67.0953 | 0.0000 | 5171 | 251 | 0.029435 | 0.073903 | -0.044468 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 264 | 33.5476 | 0.0000 | 5171 | 251 | 0.029435 | 0.147805 | -0.118371 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 264 | 167.7382 | 0.0000 | 5171 | 251 | 0.029435 | 0.029561 | -0.000127 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 141 | 103.7114 | 0.0000 | 4017 | 141 | 0.150707 | 0.074060 | 0.076647 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 141 | 51.8557 | 0.0000 | 4017 | 141 | 0.150707 | 0.148120 | 0.002587 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 141 | 259.2785 | 0.0000 | 4017 | 141 | 0.150707 | 0.029624 | 0.121083 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 147 | 80.5825 | 0.0000 | 2712 | 141 | -0.021985 | 0.065378 | -0.087362 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 147 | 40.2913 | 0.0000 | 2712 | 141 | -0.021985 | 0.130755 | -0.152740 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 147 | 201.4563 | 0.0000 | 2712 | 141 | -0.021985 | 0.026151 | -0.048136 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 79 | 113.7101 | 0.0000 | 2337 | 78 | 0.072998 | 0.064677 | 0.008321 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 79 | 56.8550 | 0.0000 | 2337 | 78 | 0.072998 | 0.129354 | -0.056356 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 79 | 284.2752 | 0.0000 | 2337 | 78 | 0.072998 | 0.025871 | 0.047127 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 222 | 67.3701 | 0.0000 | 3851 | 208 | -0.157181 | 0.053648 | -0.210829 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 222 | 22.4567 | 0.0000 | 3851 | 208 | -0.157181 | 0.160945 | -0.318126 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 222 | 168.4252 | 0.0000 | 3851 | 208 | -0.157181 | 0.021459 | -0.178640 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 78 | 153.4566 | 0.0000 | 3551 | 78 | -0.070026 | 0.055198 | -0.125224 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 78 | 51.1522 | 0.0000 | 3551 | 78 | -0.070026 | 0.165593 | -0.235619 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 78 | 383.6416 | 0.0000 | 3551 | 78 | -0.070026 | 0.022079 | -0.092105 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 11 | 82.1003 | 0.0000 | 701 | 11 | -0.092268 | 0.043232 | -0.135500 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 11 | 27.3668 | 0.0000 | 701 | 11 | -0.092268 | 0.129696 | -0.221964 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 11 | 205.2508 | 0.0000 | 701 | 11 | -0.092268 | 0.017293 | -0.109561 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 6 | 203.7933 | 0.0000 | 768 | 6 | -0.234685 | 0.045576 | -0.280261 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 6 | 67.9311 | 0.0000 | 768 | 6 | -0.234685 | 0.136727 | -0.371412 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 6 | 509.4832 | 0.0000 | 768 | 6 | -0.234685 | 0.018230 | -0.252915 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 211 | 67.2451 | 0.0000 | 3150 | 197 | -0.171747 | 0.055812 | -0.227559 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 211 | 22.4150 | 0.0000 | 3150 | 197 | -0.171747 | 0.167435 | -0.339182 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 211 | 168.1128 | 0.0000 | 3150 | 197 | -0.171747 | 0.022325 | -0.194072 | — | — | FAIL | tuning | — | — |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 72 | 153.4566 | 0.0000 | 2783 | 72 | 0.000000 | 0.058067 | -0.058067 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 72 | 51.1522 | 0.0000 | 2783 | 72 | 0.000000 | 0.174200 | -0.174200 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 72 | 383.6416 | 0.0000 | 2783 | 72 | 0.000000 | 0.023227 | -0.023227 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 75 | 102.8996 | 0.0000 | 1631 | 73 | -0.086012 | 0.048970 | -0.134983 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 75 | 34.2999 | 0.0000 | 1631 | 73 | -0.086012 | 0.146911 | -0.232923 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 75 | 257.2489 | 0.0000 | 1631 | 73 | -0.086012 | 0.019588 | -0.105600 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 42 | 137.3070 | 0.0000 | 1386 | 42 | -0.048081 | 0.046729 | -0.094810 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 42 | 45.7690 | 0.0000 | 1386 | 42 | -0.048081 | 0.140186 | -0.188267 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 42 | 343.2676 | 0.0000 | 1386 | 42 | -0.048081 | 0.018691 | -0.066773 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 75 | 102.8996 | 0.0000 | 1631 | 73 | -0.086012 | 0.048970 | -0.134983 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 75 | 34.2999 | 0.0000 | 1631 | 73 | -0.086012 | 0.146911 | -0.232923 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 75 | 257.2489 | 0.0000 | 1631 | 73 | -0.086012 | 0.019588 | -0.105600 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 42 | 137.3070 | 0.0000 | 1386 | 42 | -0.048081 | 0.046729 | -0.094810 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 42 | 45.7690 | 0.0000 | 1386 | 42 | -0.048081 | 0.140186 | -0.188267 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 42 | 343.2676 | 0.0000 | 1386 | 42 | -0.048081 | 0.018691 | -0.066773 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 82 | 65.1540 | 0.0000 | 1358 | 79 | -0.263250 | 0.062813 | -0.326063 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 82 | 21.7180 | 0.0000 | 1358 | 79 | -0.263250 | 0.188438 | -0.451688 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 82 | 162.8850 | 0.0000 | 1358 | 79 | -0.263250 | 0.025125 | -0.288375 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 40 | 108.8245 | 0.0000 | 994 | 40 | -0.018762 | 0.073820 | -0.092583 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 40 | 36.2748 | 0.0000 | 994 | 40 | -0.018762 | 0.221461 | -0.240223 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 40 | 272.0613 | 0.0000 | 994 | 40 | -0.018762 | 0.029528 | -0.048290 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 82 | 65.1540 | 0.0000 | 1358 | 79 | -0.263250 | 0.062813 | -0.326063 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 82 | 21.7180 | 0.0000 | 1358 | 79 | -0.263250 | 0.188438 | -0.451688 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 82 | 162.8850 | 0.0000 | 1358 | 79 | -0.263250 | 0.025125 | -0.288375 | — | — | FAIL | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 40 | 108.8245 | 0.0000 | 994 | 40 | -0.018762 | 0.073820 | -0.092583 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 40 | 36.2748 | 0.0000 | 994 | 40 | -0.018762 | 0.221461 | -0.240223 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 40 | 272.0613 | 0.0000 | 994 | 40 | -0.018762 | 0.029528 | -0.048290 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 162 | 53.3859 | 0.0000 | 3000 | 156 | -0.243056 | 0.100713 | -0.343769 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 162 | 17.7953 | 0.0000 | 3000 | 156 | -0.243056 | 0.302139 | -0.545194 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 162 | 133.4647 | 0.0000 | 3000 | 156 | -0.243056 | 0.040285 | -0.283341 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 97 | 78.6316 | 0.0000 | 2783 | 97 | -0.292693 | 0.103031 | -0.395724 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 97 | 26.2105 | 0.0000 | 2783 | 97 | -0.292693 | 0.309092 | -0.601785 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 97 | 196.5791 | 0.0000 | 2783 | 97 | -0.292693 | 0.041212 | -0.333906 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 46 | 46.3112 | 0.0000 | 602 | 44 | -0.741392 | 0.104887 | -0.846279 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 46 | 15.4371 | 0.0000 | 602 | 44 | -0.741392 | 0.314662 | -1.056053 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 46 | 115.7779 | 0.0000 | 602 | 44 | -0.741392 | 0.041955 | -0.783347 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 28 | 80.7159 | 0.0000 | 573 | 28 | -1.196010 | 0.108374 | -1.304384 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 28 | 26.9053 | 0.0000 | 573 | 28 | -1.196010 | 0.325121 | -1.521131 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 28 | 201.7898 | 0.0000 | 573 | 28 | -1.196010 | 0.043349 | -1.239360 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 116 | 56.1547 | 0.0000 | 2398 | 113 | -0.149591 | 0.100132 | -0.249724 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 116 | 18.7182 | 0.0000 | 2398 | 113 | -0.149591 | 0.300397 | -0.449988 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 116 | 140.3868 | 0.0000 | 2398 | 113 | -0.149591 | 0.040053 | -0.189644 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 69 | 78.5542 | 0.0000 | 2210 | 70 | -0.023847 | 0.102323 | -0.126170 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 69 | 26.1847 | 0.0000 | 2210 | 70 | -0.023847 | 0.306969 | -0.330816 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 69 | 196.3854 | 0.0000 | 2210 | 70 | -0.023847 | 0.040929 | -0.064776 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 230 | 66.3626 | 0.0000 | 3680 | 221 | -0.140060 | 0.070614 | -0.210674 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 230 | 33.1813 | 0.0000 | 3680 | 221 | -0.140060 | 0.141228 | -0.281288 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 230 | 165.9066 | 0.0000 | 3680 | 221 | -0.140060 | 0.028246 | -0.168306 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 108 | 103.5694 | 0.0000 | 3020 | 106 | -0.200577 | 0.069449 | -0.270026 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 108 | 51.7847 | 0.0000 | 3020 | 106 | -0.200577 | 0.138898 | -0.339475 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 108 | 258.9236 | 0.0000 | 3020 | 106 | -0.200577 | 0.027780 | -0.228356 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 86 | 65.5000 | 0.0000 | 1334 | 81 | -0.253170 | 0.064526 | -0.317697 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 86 | 32.7500 | 0.0000 | 1334 | 81 | -0.253170 | 0.129053 | -0.382223 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 86 | 163.7499 | 0.0000 | 1334 | 81 | -0.253170 | 0.025811 | -0.278981 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 41 | 116.9902 | 0.0000 | 1275 | 39 | -0.255252 | 0.062737 | -0.317989 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 41 | 58.4951 | 0.0000 | 1275 | 39 | -0.255252 | 0.125474 | -0.380726 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 41 | 292.4756 | 0.0000 | 1275 | 39 | -0.255252 | 0.025095 | -0.280347 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 144 | 67.7077 | 0.0000 | 2346 | 140 | -0.037018 | 0.074295 | -0.111313 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 144 | 33.8539 | 0.0000 | 2346 | 140 | -0.037018 | 0.148589 | -0.185607 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 144 | 169.2693 | 0.0000 | 2346 | 140 | -0.037018 | 0.029718 | -0.066736 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 67 | 101.2371 | 0.0000 | 1745 | 67 | -0.120993 | 0.076951 | -0.197945 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 67 | 50.6185 | 0.0000 | 1745 | 67 | -0.120993 | 0.153902 | -0.274896 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 67 | 253.0927 | 0.0000 | 1745 | 67 | -0.120993 | 0.030780 | -0.151774 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 465 | 45.6237 | 0.0000 | 8302 | 433 | 0.100148 | 0.094198 | 0.005950 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 465 | 22.8119 | 0.0000 | 8302 | 433 | 0.100148 | 0.188395 | -0.088248 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 465 | 114.0593 | 0.0000 | 8302 | 433 | 0.100148 | 0.037679 | 0.062469 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 217 | 77.9979 | 0.0000 | 5984 | 216 | 0.139337 | 0.094262 | 0.045075 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 217 | 38.9989 | 0.0000 | 5984 | 216 | 0.139337 | 0.188525 | -0.049188 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 217 | 194.9946 | 0.0000 | 5984 | 216 | 0.139337 | 0.037705 | 0.101632 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 302 | 49.3281 | 0.0000 | 5575 | 279 | 0.185649 | 0.087119 | 0.098530 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 302 | 24.6640 | 0.0000 | 5575 | 279 | 0.185649 | 0.174238 | 0.011411 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 302 | 123.3201 | 0.0000 | 5575 | 279 | 0.185649 | 0.034848 | 0.150801 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 144 | 85.5215 | 0.0000 | 4059 | 143 | 0.255949 | 0.084790 | 0.171159 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 144 | 42.7607 | 0.0000 | 4059 | 143 | 0.255949 | 0.169581 | 0.086369 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 144 | 213.8037 | 0.0000 | 4059 | 143 | 0.255949 | 0.033916 | 0.222033 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 163 | 38.0780 | 0.0000 | 2727 | 154 | -0.062931 | 0.110704 | -0.173636 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 163 | 19.0390 | 0.0000 | 2727 | 154 | -0.062931 | 0.221409 | -0.284340 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 163 | 95.1949 | 0.0000 | 2727 | 154 | -0.062931 | 0.044282 | -0.107213 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 73 | 71.8213 | 0.0000 | 1925 | 74 | -0.077898 | 0.117838 | -0.195736 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 73 | 35.9107 | 0.0000 | 1925 | 74 | -0.077898 | 0.235675 | -0.313574 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 73 | 179.5533 | 0.0000 | 1925 | 74 | -0.077898 | 0.047135 | -0.125033 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 435 | 42.8274 | 0.0000 | 10423 | 421 | 0.272647 | 0.094668 | 0.177980 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 435 | 21.4137 | 0.0000 | 10423 | 421 | 0.272647 | 0.189335 | 0.083312 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 435 | 107.0685 | 0.0000 | 10423 | 421 | 0.272647 | 0.037867 | 0.234780 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 173 | 83.7279 | 0.0000 | 7806 | 173 | 0.204060 | 0.098997 | 0.105063 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 173 | 41.8640 | 0.0000 | 7806 | 173 | 0.204060 | 0.197994 | 0.006065 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 173 | 209.3198 | 0.0000 | 7806 | 173 | 0.204060 | 0.039599 | 0.164461 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 293 | 41.8773 | 0.0000 | 7117 | 282 | 0.285947 | 0.092617 | 0.193329 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 293 | 20.9387 | 0.0000 | 7117 | 282 | 0.285947 | 0.185235 | 0.100712 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 293 | 104.6933 | 0.0000 | 7117 | 282 | 0.285947 | 0.037047 | 0.248900 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 111 | 85.1713 | 0.0000 | 5285 | 111 | 0.313227 | 0.095676 | 0.217551 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 111 | 42.5857 | 0.0000 | 5285 | 111 | 0.313227 | 0.191352 | 0.121875 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 111 | 212.9283 | 0.0000 | 5285 | 111 | 0.313227 | 0.038270 | 0.274957 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 142 | 43.4804 | 0.0000 | 3306 | 140 | 0.235082 | 0.097534 | 0.137548 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 142 | 21.7402 | 0.0000 | 3306 | 140 | 0.235082 | 0.195068 | 0.040014 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 142 | 108.7010 | 0.0000 | 3306 | 140 | 0.235082 | 0.039014 | 0.196068 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 62 | 83.6174 | 0.0000 | 2521 | 63 | -0.003736 | 0.102286 | -0.106022 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 62 | 41.8087 | 0.0000 | 2521 | 63 | -0.003736 | 0.204572 | -0.208308 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 62 | 209.0435 | 0.0000 | 2521 | 63 | -0.003736 | 0.040914 | -0.044650 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 486 | 37.0951 | 0.0000 | 7442 | 464 | 0.024193 | 0.118699 | -0.094507 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 486 | 18.5476 | 0.0000 | 7442 | 464 | 0.024193 | 0.237399 | -0.213206 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 486 | 92.7378 | 0.0000 | 7442 | 464 | 0.024193 | 0.047480 | -0.023287 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 220 | 68.1960 | 0.0000 | 5613 | 218 | -0.018888 | 0.123557 | -0.142446 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 220 | 34.0980 | 0.0000 | 5613 | 218 | -0.018888 | 0.247115 | -0.266003 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 220 | 170.4901 | 0.0000 | 5613 | 218 | -0.018888 | 0.049423 | -0.068311 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 310 | 41.6709 | 0.0000 | 4899 | 295 | 0.030650 | 0.101598 | -0.070948 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 310 | 20.8355 | 0.0000 | 4899 | 295 | 0.030650 | 0.203196 | -0.172546 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 310 | 104.1773 | 0.0000 | 4899 | 295 | 0.030650 | 0.040639 | -0.009989 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 142 | 77.4426 | 0.0000 | 4011 | 140 | 0.025121 | 0.110423 | -0.085301 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 142 | 38.7213 | 0.0000 | 4011 | 140 | 0.025121 | 0.220846 | -0.195724 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 142 | 193.6064 | 0.0000 | 4011 | 140 | 0.025121 | 0.044169 | -0.019048 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 176 | 28.6000 | 0.0000 | 2543 | 170 | 0.006610 | 0.154755 | -0.148145 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 176 | 14.3000 | 0.0000 | 2543 | 170 | 0.006610 | 0.309509 | -0.302899 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 176 | 71.5001 | 0.0000 | 2543 | 170 | 0.006610 | 0.061902 | -0.055292 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 78 | 48.2008 | 0.0000 | 1602 | 79 | -0.185060 | 0.164459 | -0.349519 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 78 | 24.1004 | 0.0000 | 1602 | 79 | -0.185060 | 0.328917 | -0.513977 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 78 | 120.5021 | 0.0000 | 1602 | 79 | -0.185060 | 0.065783 | -0.250843 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 375 | 68.1297 | 0.0000 | 6435 | 361 | 0.071304 | 0.074330 | -0.003026 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 375 | 34.0649 | 0.0000 | 6435 | 361 | 0.071304 | 0.148660 | -0.077356 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 375 | 170.3243 | 0.0000 | 6435 | 361 | 0.071304 | 0.029732 | 0.041572 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 182 | 100.8202 | 0.0000 | 7002 | 182 | 0.208586 | 0.070298 | 0.138288 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 182 | 50.4101 | 0.0000 | 7002 | 182 | 0.208586 | 0.140596 | 0.067991 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 182 | 252.0505 | 0.0000 | 7002 | 182 | 0.208586 | 0.028119 | 0.180467 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 233 | 69.8131 | 0.0000 | 4164 | 223 | 0.117659 | 0.068695 | 0.048963 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 233 | 34.9065 | 0.0000 | 4164 | 223 | 0.117659 | 0.137391 | -0.019732 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 233 | 174.5327 | 0.0000 | 4164 | 223 | 0.117659 | 0.027478 | 0.090180 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 110 | 96.3987 | 0.0000 | 4784 | 110 | 0.212778 | 0.064721 | 0.148057 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 110 | 48.1994 | 0.0000 | 4784 | 110 | 0.212778 | 0.129441 | 0.083336 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 110 | 240.9969 | 0.0000 | 4784 | 110 | 0.212778 | 0.025888 | 0.186889 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 142 | 64.7364 | 0.0000 | 2271 | 138 | -0.011542 | 0.081727 | -0.093270 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 142 | 32.3682 | 0.0000 | 2271 | 138 | -0.011542 | 0.163455 | -0.174997 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 142 | 161.8411 | 0.0000 | 2271 | 138 | -0.011542 | 0.032691 | -0.044233 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 72 | 102.2300 | 0.0000 | 2218 | 73 | 0.205442 | 0.080985 | 0.124457 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 72 | 51.1150 | 0.0000 | 2218 | 73 | 0.205442 | 0.161970 | 0.043472 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 72 | 255.5749 | 0.0000 | 2218 | 73 | 0.205442 | 0.032394 | 0.173048 | — | — | PASS | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 224 | 64.1908 | 0.0000 | 4140 | 218 | 0.022622 | 0.064587 | -0.041965 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 224 | 21.3969 | 0.0000 | 4140 | 218 | 0.022622 | 0.193761 | -0.171138 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 224 | 160.4771 | 0.0000 | 4140 | 218 | 0.022622 | 0.025835 | -0.003212 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 104 | 118.9956 | 0.0000 | 3675 | 102 | -0.125283 | 0.072855 | -0.198138 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 104 | 39.6652 | 0.0000 | 3675 | 102 | -0.125283 | 0.218566 | -0.343849 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 104 | 297.4889 | 0.0000 | 3675 | 102 | -0.125283 | 0.029142 | -0.154425 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 76 | 79.4043 | 0.0000 | 1352 | 73 | 0.264646 | 0.052011 | 0.212634 | — | — | PASS | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 76 | 26.4681 | 0.0000 | 1352 | 73 | 0.264646 | 0.156033 | 0.108612 | — | — | PASS | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 76 | 198.5108 | 0.0000 | 1352 | 73 | 0.264646 | 0.020804 | 0.243841 | — | — | PASS | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 36 | 147.3739 | 0.0000 | 1066 | 34 | -0.110507 | 0.066145 | -0.176652 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 36 | 49.1246 | 0.0000 | 1066 | 34 | -0.110507 | 0.198435 | -0.308943 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 36 | 368.4348 | 0.0000 | 1066 | 34 | -0.110507 | 0.026458 | -0.136965 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 148 | 62.0862 | 0.0000 | 2788 | 146 | -0.082727 | 0.070637 | -0.153364 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 148 | 20.6954 | 0.0000 | 2788 | 146 | -0.082727 | 0.211910 | -0.294637 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 148 | 155.2156 | 0.0000 | 2788 | 146 | -0.082727 | 0.028255 | -0.110982 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 68 | 109.2987 | 0.0000 | 2609 | 68 | -0.137648 | 0.074631 | -0.212279 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 68 | 36.4329 | 0.0000 | 2609 | 68 | -0.137648 | 0.223893 | -0.361542 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 68 | 273.2468 | 0.0000 | 2609 | 68 | -0.137648 | 0.029852 | -0.167501 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 399 | 53.6179 | 0.0000 | 6423 | 385 | 0.150976 | 0.083481 | 0.067495 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | charter | 20.0 | 20.0 | 399 | 26.8090 | 0.0000 | 6423 | 385 | 0.150976 | 0.166961 | -0.015985 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 399 | 134.0449 | 0.0000 | 6423 | 385 | 0.150976 | 0.033392 | 0.117584 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 182 | 93.5651 | 0.0000 | 5521 | 180 | 0.300882 | 0.084317 | 0.216564 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 182 | 46.7826 | 0.0000 | 5521 | 180 | 0.300882 | 0.168635 | 0.132247 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 182 | 233.9128 | 0.0000 | 5521 | 180 | 0.300882 | 0.033727 | 0.267155 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 243 | 54.8727 | 0.0000 | 3958 | 234 | 0.165393 | 0.081251 | 0.084142 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | charter | 20.0 | 20.0 | 243 | 27.4363 | 0.0000 | 3958 | 234 | 0.165393 | 0.162503 | 0.002891 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 243 | 137.1817 | 0.0000 | 3958 | 234 | 0.165393 | 0.032501 | 0.132893 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 107 | 102.4758 | 0.0000 | 3766 | 106 | 0.191570 | 0.082516 | 0.109054 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 107 | 51.2379 | 0.0000 | 3766 | 106 | 0.191570 | 0.165033 | 0.026537 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 107 | 256.1896 | 0.0000 | 3766 | 106 | 0.191570 | 0.033007 | 0.158563 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 156 | 51.8086 | 0.0000 | 2465 | 152 | 0.087737 | 0.086716 | 0.001020 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | charter | 20.0 | 20.0 | 156 | 25.9043 | 0.0000 | 2465 | 152 | 0.087737 | 0.173432 | -0.085696 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 156 | 129.5216 | 0.0000 | 2465 | 152 | 0.087737 | 0.034686 | 0.053050 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 75 | 85.8830 | 0.0000 | 1755 | 75 | 0.626731 | 0.088996 | 0.537735 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 75 | 42.9415 | 0.0000 | 1755 | 75 | 0.626731 | 0.177992 | 0.448739 | — | — | PASS | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 75 | 214.7075 | 0.0000 | 1755 | 75 | 0.626731 | 0.035598 | 0.591132 | — | — | PASS | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 174 | 94.3147 | 0.0000 | 3614 | 172 | -0.256780 | 0.060308 | -0.317088 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | charter | 30.0 | 30.0 | 174 | 31.4382 | 0.0000 | 3614 | 172 | -0.256780 | 0.180923 | -0.437703 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 174 | 235.7868 | 0.0000 | 3614 | 172 | -0.256780 | 0.024123 | -0.280903 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 90 | 145.6863 | 0.0000 | 3065 | 89 | -0.120128 | 0.057606 | -0.177734 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 90 | 48.5621 | 0.0000 | 3065 | 89 | -0.120128 | 0.172818 | -0.292946 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 90 | 364.2158 | 0.0000 | 3065 | 89 | -0.120128 | 0.023042 | -0.143171 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 42 | 125.0080 | 0.0000 | 740 | 40 | -0.233073 | 0.044589 | -0.277661 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | charter | 30.0 | 30.0 | 42 | 41.6693 | 0.0000 | 740 | 40 | -0.233073 | 0.133766 | -0.366839 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 42 | 312.5199 | 0.0000 | 740 | 40 | -0.233073 | 0.017835 | -0.250908 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 22 | 174.7779 | 0.0000 | 596 | 22 | 0.277308 | 0.049267 | 0.228041 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 22 | 58.2593 | 0.0000 | 596 | 22 | 0.277308 | 0.147802 | 0.129507 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 22 | 436.9448 | 0.0000 | 596 | 22 | 0.277308 | 0.019707 | 0.257601 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 132 | 84.2757 | 0.0000 | 2874 | 133 | -0.265896 | 0.063461 | -0.329356 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | charter | 30.0 | 30.0 | 132 | 28.0919 | 0.0000 | 2874 | 133 | -0.265896 | 0.190381 | -0.456277 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 132 | 210.6893 | 0.0000 | 2874 | 133 | -0.265896 | 0.025384 | -0.291280 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 68 | 139.3024 | 0.0000 | 2469 | 68 | -0.199344 | 0.059837 | -0.259181 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 68 | 46.4341 | 0.0000 | 2469 | 68 | -0.199344 | 0.179511 | -0.378855 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 68 | 348.2559 | 0.0000 | 2469 | 68 | -0.199344 | 0.023935 | -0.223279 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 2253 | 51.5959 | 0.0000 | 35941 | 2140 | 0.059479 | 0.134821 | -0.075342 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | charter | 14.0 | 20.0 | 2253 | 30.1766 | 0.0000 | 35941 | 2140 | 0.059479 | 0.188750 | -0.129271 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 2253 | 128.9898 | 0.0000 | 35941 | 2140 | 0.059479 | 0.053929 | 0.005551 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 1088 | 84.7372 | 0.0000 | 31066 | 1081 | 0.085096 | 0.132569 | -0.047473 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | charter | 14.0 | 20.0 | 1088 | 49.6543 | 0.0000 | 31066 | 1081 | 0.085096 | 0.185596 | -0.100501 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 1088 | 211.8431 | 0.0000 | 31066 | 1081 | 0.085096 | 0.053028 | 0.032068 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 1437 | 55.5195 | 0.0000 | 23897 | 1371 | 0.083448 | 0.120354 | -0.036906 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | charter | 14.0 | 20.0 | 1437 | 32.5917 | 0.0000 | 23897 | 1371 | 0.083448 | 0.168495 | -0.085047 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 1437 | 138.7987 | 0.0000 | 23897 | 1371 | 0.083448 | 0.048142 | 0.035307 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 712 | 87.7624 | 0.0000 | 20169 | 708 | 0.057084 | 0.119332 | -0.062248 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | charter | 14.0 | 20.0 | 712 | 52.1662 | 0.0000 | 20169 | 708 | 0.057084 | 0.167064 | -0.109980 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 712 | 219.4059 | 0.0000 | 20169 | 708 | 0.057084 | 0.047733 | 0.009351 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 816 | 46.2355 | 0.0000 | 12044 | 771 | 0.000000 | 0.167605 | -0.167605 | FAIL | FAIL | — | tuning | — | — |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | charter | 14.0 | 20.0 | 816 | 26.2699 | 0.0000 | 12044 | 771 | 0.000000 | 0.234647 | -0.234647 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 816 | 115.5889 | 0.0000 | 12044 | 771 | 0.000000 | 0.067042 | -0.067042 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 376 | 80.1212 | 0.0000 | 10897 | 375 | 0.152500 | 0.159302 | -0.006802 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | charter | 14.0 | 20.0 | 376 | 46.1878 | 0.0000 | 10897 | 375 | 0.152500 | 0.223023 | -0.070523 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 376 | 200.3031 | 0.0000 | 10897 | 375 | 0.152500 | 0.063721 | 0.088779 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | ALL | calibrated | taker | 10.0 | 10.0 | 5582 | 53.6643 | 0.0000 | 96240 | 5331 | 0.047791 | 0.134821 | -0.087030 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | ALL | calibrated | charter | 14.0 | 30.0 | 5582 | 26.4129 | 0.0000 | 96240 | 5331 | 0.047791 | 0.302139 | -0.254347 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | ALL | calibrated | maker | 4.0 | 4.0 | 5582 | 134.1607 | 0.0000 | 96240 | 5331 | 0.047791 | 0.053929 | -0.006137 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2621 | 91.1430 | 0.0000 | 81466 | 2604 | 0.074342 | 0.132569 | -0.058227 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | charter | 14.0 | 30.0 | 2621 | 44.8080 | 0.0000 | 81466 | 2604 | 0.074342 | 0.309092 | -0.234750 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2621 | 227.8576 | 0.0000 | 81466 | 2604 | 0.074342 | 0.053028 | 0.021315 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | tuning | calibrated | taker | 10.0 | 10.0 | 3079 | 54.3181 | 0.0000 | 54339 | 2933 | 0.105922 | 0.120354 | -0.014432 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | tuning | calibrated | charter | 14.0 | 30.0 | 3079 | 28.6309 | 0.0000 | 54339 | 2933 | 0.105922 | 0.314662 | -0.208740 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | tuning | calibrated | maker | 4.0 | 4.0 | 3079 | 135.7953 | 0.0000 | 54339 | 2933 | 0.105922 | 0.048142 | 0.057781 | — | — | PASS | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1459 | 89.7553 | 0.0000 | 46352 | 1447 | 0.095083 | 0.119332 | -0.024249 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | charter | 14.0 | 30.0 | 1459 | 47.5352 | 0.0000 | 46352 | 1447 | 0.095083 | 0.325121 | -0.230039 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1459 | 224.3883 | 0.0000 | 46352 | 1447 | 0.095083 | 0.047733 | 0.047350 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | holdout | calibrated | taker | 10.0 | 10.0 | 2503 | 52.9644 | 0.0000 | 41901 | 2406 | -0.036039 | 0.167605 | -0.203645 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | holdout | calibrated | charter | 14.0 | 30.0 | 2503 | 24.0154 | 0.0000 | 41901 | 2406 | -0.036039 | 0.309509 | -0.345549 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | holdout | calibrated | maker | 4.0 | 4.0 | 2503 | 132.4111 | 0.0000 | 41901 | 2406 | -0.036039 | 0.067042 | -0.103081 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1162 | 93.0564 | 0.0000 | 35114 | 1166 | 0.047573 | 0.164459 | -0.116885 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | charter | 14.0 | 30.0 | 1162 | 41.7345 | 0.0000 | 35114 | 1166 | 0.047573 | 0.328917 | -0.281344 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1162 | 232.6409 | 0.0000 | 35114 | 1166 | 0.047573 | 0.065783 | -0.018210 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 111 | 69.4022 | 0.0000 | 1934 | 107 | -0.113206 | 0.067558 | -0.180764 | — | — | FAIL | tuning | FAIL | -0.180764 |
| ASSET:BTCUSDT | 4h | ALL | calibrated | charter | 14.0 | 14.0 | 111 | 49.5730 | 0.0000 | 1934 | 107 | -0.113206 | 0.094581 | -0.207787 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 111 | 173.5054 | 0.0000 | 1934 | 107 | -0.113206 | 0.027023 | -0.140230 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 63 | 98.1620 | 0.0000 | 1371 | 63 | -0.261823 | 0.066558 | -0.328381 | — | — | FAIL | frozen3.0 | FAIL | -0.298396 |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 63 | 70.1157 | 0.0000 | 1371 | 63 | -0.261823 | 0.093182 | -0.355004 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 63 | 245.4049 | 0.0000 | 1371 | 63 | -0.261823 | 0.026623 | -0.288446 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 77 | 72.7608 | 0.0000 | 1291 | 75 | -0.041446 | 0.059926 | -0.101372 | — | — | FAIL | tuning | FAIL | -0.101372 |
| ASSET:BTCUSDT | 4h | tuning | calibrated | charter | 14.0 | 14.0 | 77 | 51.9720 | 0.0000 | 1291 | 75 | -0.041446 | 0.083896 | -0.125343 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 77 | 181.9020 | 0.0000 | 1291 | 75 | -0.041446 | 0.023970 | -0.065417 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 40 | 106.5000 | 0.0000 | 878 | 40 | -0.187084 | 0.058167 | -0.245251 | — | — | FAIL | frozen3.0 | FAIL | -0.245251 |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 40 | 76.0714 | 0.0000 | 878 | 40 | -0.187084 | 0.081434 | -0.268517 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 40 | 266.2501 | 0.0000 | 878 | 40 | -0.187084 | 0.023267 | -0.210350 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 34 | 64.3650 | 0.0000 | 643 | 32 | -0.344028 | 0.082389 | -0.426417 | — | — | FAIL | tuning | FAIL | -0.426417 |
| ASSET:BTCUSDT | 4h | holdout | calibrated | charter | 14.0 | 14.0 | 34 | 45.9750 | 0.0000 | 643 | 32 | -0.344028 | 0.115345 | -0.459373 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 34 | 160.9125 | 0.0000 | 643 | 32 | -0.344028 | 0.032956 | -0.376983 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 23 | 91.2719 | 0.0000 | 493 | 23 | -0.361085 | 0.088386 | -0.449471 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.377101 |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 23 | 65.1942 | 0.0000 | 493 | 23 | -0.361085 | 0.123740 | -0.484825 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 23 | 228.1796 | 0.0000 | 493 | 23 | -0.361085 | 0.035354 | -0.396439 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 113 | 95.0860 | 0.0000 | 1714 | 105 | -0.109641 | 0.050751 | -0.160392 | — | — | FAIL | tuning | FAIL | -0.160392 |
| ASSET:ETHUSDT | 4h | ALL | calibrated | charter | 14.0 | 14.0 | 113 | 67.9185 | 0.0000 | 1714 | 105 | -0.109641 | 0.071051 | -0.180692 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 113 | 237.7149 | 0.0000 | 1714 | 105 | -0.109641 | 0.020300 | -0.129941 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 63 | 143.3778 | 0.0000 | 1563 | 61 | -0.050214 | 0.055113 | -0.105327 | — | — | FAIL | frozen3.0 | FAIL | -0.105327 |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 63 | 102.4127 | 0.0000 | 1563 | 61 | -0.050214 | 0.077158 | -0.127372 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 63 | 358.4445 | 0.0000 | 1563 | 61 | -0.050214 | 0.022045 | -0.072259 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 74 | 91.0243 | 0.0000 | 1219 | 69 | -0.211969 | 0.047803 | -0.259772 | — | — | FAIL | tuning | FAIL | -0.259772 |
| ASSET:ETHUSDT | 4h | tuning | calibrated | charter | 14.0 | 14.0 | 74 | 65.0174 | 0.0000 | 1219 | 69 | -0.211969 | 0.066924 | -0.278893 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 74 | 227.5607 | 0.0000 | 1219 | 69 | -0.211969 | 0.019121 | -0.231090 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 42 | 146.0934 | 0.0000 | 1174 | 40 | -0.265804 | 0.051731 | -0.317535 | — | — | FAIL | frozen3.0 | FAIL | -0.317535 |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 42 | 104.3524 | 0.0000 | 1174 | 40 | -0.265804 | 0.072423 | -0.338227 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 42 | 365.2335 | 0.0000 | 1174 | 40 | -0.265804 | 0.020692 | -0.286496 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 39 | 95.3059 | 0.0000 | 495 | 36 | 0.139605 | 0.055601 | 0.084005 | — | — | PASS | tuning | PASS | 0.084005 |
| ASSET:ETHUSDT | 4h | holdout | calibrated | charter | 14.0 | 14.0 | 39 | 68.0756 | 0.0000 | 495 | 36 | 0.139605 | 0.077841 | 0.061764 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 39 | 238.2647 | 0.0000 | 495 | 36 | 0.139605 | 0.022240 | 0.117365 | — | — | PASS | tuning | — | — |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 21 | 140.3066 | 0.0000 | 389 | 21 | 0.546805 | 0.058595 | 0.488210 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.488210 |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 21 | 100.2190 | 0.0000 | 389 | 21 | 0.546805 | 0.082033 | 0.464772 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 21 | 350.7665 | 0.0000 | 389 | 21 | 0.546805 | 0.023438 | 0.523367 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 88 | 146.3951 | 0.0000 | 1589 | 87 | -0.020184 | 0.038622 | -0.058806 | — | — | FAIL | tuning | FAIL | -0.058786 |
| ASSET:SOLUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 88 | 73.1975 | 0.0000 | 1589 | 87 | -0.020184 | 0.077244 | -0.097428 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 88 | 365.9877 | 0.0000 | 1589 | 87 | -0.020184 | 0.015449 | -0.035633 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 53 | 221.8464 | 0.0000 | 1122 | 51 | -0.360794 | 0.037716 | -0.398510 | — | — | FAIL | frozen3.0 | FAIL | -0.397375 |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 53 | 110.9232 | 0.0000 | 1122 | 51 | -0.360794 | 0.075433 | -0.436227 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 53 | 554.6160 | 0.0000 | 1122 | 51 | -0.360794 | 0.015087 | -0.375880 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 59 | 165.5595 | 0.0000 | 912 | 59 | -0.414787 | 0.033070 | -0.447857 | — | — | FAIL | tuning | FAIL | -0.447857 |
| ASSET:SOLUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 59 | 82.7798 | 0.0000 | 912 | 59 | -0.414787 | 0.066141 | -0.480928 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 59 | 413.8989 | 0.0000 | 912 | 59 | -0.414787 | 0.013228 | -0.428015 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 39 | 221.8464 | 0.0000 | 677 | 37 | -0.934628 | 0.032669 | -0.967297 | — | — | FAIL | frozen3.0 | FAIL | -0.967297 |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 39 | 110.9232 | 0.0000 | 677 | 37 | -0.934628 | 0.065338 | -0.999965 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 39 | 554.6160 | 0.0000 | 677 | 37 | -0.934628 | 0.013068 | -0.947695 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 29 | 96.0908 | 0.0000 | 677 | 29 | 0.582558 | 0.044215 | 0.538343 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.545373 |
| ASSET:SOLUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 29 | 48.0454 | 0.0000 | 677 | 29 | 0.582558 | 0.088431 | 0.494127 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 29 | 240.2269 | 0.0000 | 677 | 29 | 0.582558 | 0.017686 | 0.564872 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 14 | 218.5260 | 0.0000 | 445 | 14 | 0.582558 | 0.042900 | 0.539658 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.546705 |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 14 | 109.2630 | 0.0000 | 445 | 14 | 0.582558 | 0.085801 | 0.496757 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 14 | 546.3151 | 0.0000 | 445 | 14 | 0.582558 | 0.017160 | 0.565398 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 112 | 140.5561 | 0.0000 | 2077 | 110 | -0.286116 | 0.029942 | -0.316059 | — | — | FAIL | tuning | FAIL | -0.354517 |
| ASSET:NEARUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 112 | 70.2780 | 0.0000 | 2077 | 110 | -0.286116 | 0.059885 | -0.346001 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 112 | 351.3902 | 0.0000 | 2077 | 110 | -0.286116 | 0.011977 | -0.298093 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 58 | 229.5984 | 0.0000 | 1629 | 57 | -0.468364 | 0.031618 | -0.499982 | — | — | FAIL | frozen3.0 | FAIL | -0.499982 |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 58 | 114.7992 | 0.0000 | 1629 | 57 | -0.468364 | 0.063236 | -0.531600 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 58 | 573.9960 | 0.0000 | 1629 | 57 | -0.468364 | 0.012647 | -0.481011 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 64 | 163.8034 | 0.0000 | 1477 | 62 | -0.308357 | 0.028020 | -0.336376 | — | — | FAIL | tuning | FAIL | -0.371607 |
| ASSET:NEARUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 64 | 81.9017 | 0.0000 | 1477 | 62 | -0.308357 | 0.056039 | -0.364396 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 64 | 409.5084 | 0.0000 | 1477 | 62 | -0.308357 | 0.011208 | -0.319565 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 32 | 221.8571 | 0.0000 | 1134 | 31 | -0.398675 | 0.028256 | -0.426932 | — | — | FAIL | frozen3.0 | FAIL | -0.426932 |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 32 | 110.9286 | 0.0000 | 1134 | 31 | -0.398675 | 0.056513 | -0.455188 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 32 | 554.6428 | 0.0000 | 1134 | 31 | -0.398675 | 0.011303 | -0.409978 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 48 | 125.1540 | 0.0000 | 600 | 49 | -0.268458 | 0.032671 | -0.301129 | — | — | FAIL | tuning | FAIL | -0.309115 |
| ASSET:NEARUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 48 | 62.5770 | 0.0000 | 600 | 49 | -0.268458 | 0.065341 | -0.333799 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 48 | 312.8850 | 0.0000 | 600 | 49 | -0.268458 | 0.013068 | -0.281526 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 26 | 234.7141 | 0.0000 | 495 | 27 | -0.591082 | 0.033950 | -0.625032 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.625032 |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 26 | 117.3571 | 0.0000 | 495 | 27 | -0.591082 | 0.067900 | -0.658982 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 26 | 586.7853 | 0.0000 | 495 | 27 | -0.591082 | 0.013580 | -0.604662 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 112 | 148.6486 | 0.0000 | 1746 | 108 | -0.118932 | 0.033899 | -0.152831 | — | — | FAIL | tuning | FAIL | -0.152831 |
| ASSET:ZECUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 112 | 74.3243 | 0.0000 | 1746 | 108 | -0.118932 | 0.067798 | -0.186730 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 112 | 371.6216 | 0.0000 | 1746 | 108 | -0.118932 | 0.013560 | -0.132492 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 61 | 188.5332 | 0.0000 | 1760 | 60 | 0.181963 | 0.036681 | 0.145282 | — | — | PASS | frozen3.0 | PASS | 0.145282 |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 61 | 94.2666 | 0.0000 | 1760 | 60 | 0.181963 | 0.073362 | 0.108601 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 61 | 471.3329 | 0.0000 | 1760 | 60 | 0.181963 | 0.014672 | 0.167291 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 71 | 137.9655 | 0.0000 | 1321 | 69 | -0.106877 | 0.035629 | -0.142506 | — | — | FAIL | tuning | FAIL | -0.142506 |
| ASSET:ZECUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 71 | 68.9828 | 0.0000 | 1321 | 69 | -0.106877 | 0.071258 | -0.178135 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 71 | 344.9139 | 0.0000 | 1321 | 69 | -0.106877 | 0.014252 | -0.121129 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 43 | 172.4838 | 0.0000 | 1212 | 42 | 0.179349 | 0.040593 | 0.138756 | — | — | PASS | frozen3.0 | PASS | 0.138756 |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 43 | 86.2419 | 0.0000 | 1212 | 42 | 0.179349 | 0.081186 | 0.098163 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 43 | 431.2096 | 0.0000 | 1212 | 42 | 0.179349 | 0.016237 | 0.163112 | — | — | PASS | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 41 | 160.5810 | 0.0000 | 425 | 40 | -0.148811 | 0.030446 | -0.179257 | — | — | FAIL | tuning | FAIL | -0.179257 |
| ASSET:ZECUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 41 | 80.2905 | 0.0000 | 425 | 40 | -0.148811 | 0.060892 | -0.209703 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 41 | 401.4526 | 0.0000 | 425 | 40 | -0.148811 | 0.012178 | -0.160989 | — | — | FAIL | tuning | — | — |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 18 | 261.0938 | 0.0000 | 548 | 19 | 0.215526 | 0.033101 | 0.182425 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.182425 |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 18 | 130.5469 | 0.0000 | 548 | 19 | 0.215526 | 0.066203 | 0.149324 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 18 | 652.7344 | 0.0000 | 548 | 19 | 0.215526 | 0.013241 | 0.202286 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 28 | 240.9592 | 0.0000 | 553 | 28 | -0.058182 | 0.027882 | -0.086065 | — | — | FAIL (provisional, n<30) | tuning | PASS | 0.093449 |
| ASSET:ENAUSDT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 28 | 80.3197 | 0.0000 | 553 | 28 | -0.058182 | 0.083647 | -0.141829 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 28 | 602.3981 | 0.0000 | 553 | 28 | -0.058182 | 0.011153 | -0.069335 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 24 | 263.5248 | 0.0000 | 520 | 24 | -0.060177 | 0.027570 | -0.087748 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.081981 |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 24 | 87.8416 | 0.0000 | 520 | 24 | -0.060177 | 0.082711 | -0.142888 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 24 | 658.8121 | 0.0000 | 520 | 24 | -0.060177 | 0.011028 | -0.071206 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 4 | 254.8760 | 0.0000 | 45 | 4 | -1.418036 | 0.024621 | -1.442656 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -1.209781 |
| ASSET:ENAUSDT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 4 | 84.9587 | 0.0000 | 45 | 4 | -1.418036 | 0.073862 | -1.491897 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 4 | 637.1900 | 0.0000 | 45 | 4 | -1.418036 | 0.009848 | -1.427884 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 3 | 269.0928 | 0.0000 | 40 | 3 | -1.694200 | 0.024953 | -1.719154 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.719154 |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 3 | 89.6976 | 0.0000 | 40 | 3 | -1.694200 | 0.074860 | -1.769060 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 3 | 672.7319 | 0.0000 | 40 | 3 | -1.694200 | 0.009981 | -1.704182 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 24 | 236.7901 | 0.0000 | 508 | 24 | -0.041775 | 0.028101 | -0.069876 | — | — | FAIL (provisional, n<30) | tuning | PASS | 0.187284 |
| ASSET:ENAUSDT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 24 | 78.9300 | 0.0000 | 508 | 24 | -0.041775 | 0.084303 | -0.126078 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 24 | 591.9753 | 0.0000 | 508 | 24 | -0.041775 | 0.011240 | -0.053016 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 21 | 262.8594 | 0.0000 | 480 | 21 | -0.048575 | 0.027754 | -0.076329 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.069549 |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 21 | 87.6198 | 0.0000 | 480 | 21 | -0.048575 | 0.083261 | -0.131836 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 21 | 657.1484 | 0.0000 | 480 | 21 | -0.048575 | 0.011102 | -0.059676 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 21 | 202.9652 | 0.0000 | 189 | 20 | -0.832272 | 0.027656 | -0.859928 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.859928 |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 21 | 67.6551 | 0.0000 | 189 | 20 | -0.832272 | 0.082968 | -0.915240 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 21 | 507.4131 | 0.0000 | 189 | 20 | -0.832272 | 0.011062 | -0.843334 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 7 | 457.7144 | 0.0000 | 619 | 7 | 0.132662 | 0.033221 | 0.099441 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.099441 |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 7 | 152.5715 | 0.0000 | 619 | 7 | 0.132662 | 0.099663 | 0.032999 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 7 | 1144.2860 | 0.0000 | 619 | 7 | 0.132662 | 0.013288 | 0.119374 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | — |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 21 | 202.9652 | 0.0000 | 189 | 20 | -0.832272 | 0.027656 | -0.859928 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.859928 |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 21 | 67.6551 | 0.0000 | 189 | 20 | -0.832272 | 0.082968 | -0.915240 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 21 | 507.4131 | 0.0000 | 189 | 20 | -0.832272 | 0.011062 | -0.843334 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 7 | 457.7144 | 0.0000 | 619 | 7 | 0.132662 | 0.033221 | 0.099441 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.099441 |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 7 | 152.5715 | 0.0000 | 619 | 7 | 0.132662 | 0.099663 | 0.032999 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 7 | 1144.2860 | 0.0000 | 619 | 7 | 0.132662 | 0.013288 | 0.119374 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 22 | 117.4910 | 0.0000 | 320 | 20 | -0.067522 | 0.033259 | -0.100782 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.100782 |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 22 | 39.1637 | 0.0000 | 320 | 20 | -0.067522 | 0.099778 | -0.167300 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 22 | 293.7274 | 0.0000 | 320 | 20 | -0.067522 | 0.013304 | -0.080826 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 15 | 241.4730 | 0.0000 | 170 | 14 | -1.077666 | 0.033766 | -1.111431 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.111431 |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 15 | 80.4910 | 0.0000 | 170 | 14 | -1.077666 | 0.101297 | -1.178963 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 15 | 603.6825 | 0.0000 | 170 | 14 | -1.077666 | 0.013506 | -1.091172 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | — |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 22 | 117.4910 | 0.0000 | 320 | 20 | -0.067522 | 0.033259 | -0.100782 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.100782 |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 22 | 39.1637 | 0.0000 | 320 | 20 | -0.067522 | 0.099778 | -0.167300 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 22 | 293.7274 | 0.0000 | 320 | 20 | -0.067522 | 0.013304 | -0.080826 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 15 | 241.4730 | 0.0000 | 170 | 14 | -1.077666 | 0.033766 | -1.111431 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.111431 |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 15 | 80.4910 | 0.0000 | 170 | 14 | -1.077666 | 0.101297 | -1.178963 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 15 | 603.6825 | 0.0000 | 170 | 14 | -1.077666 | 0.013506 | -1.091172 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 49 | 107.3954 | 0.0000 | 778 | 49 | -0.182963 | 0.048478 | -0.231441 | — | — | FAIL | tuning | FAIL | -0.189785 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 49 | 35.7985 | 0.0000 | 778 | 49 | -0.182963 | 0.145435 | -0.328397 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 49 | 268.4885 | 0.0000 | 778 | 49 | -0.182963 | 0.019391 | -0.202354 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 31 | 135.0515 | 0.0000 | 712 | 31 | -0.278814 | 0.052625 | -0.331440 | — | — | FAIL | frozen3.0 | FAIL | -0.300013 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 31 | 45.0172 | 0.0000 | 712 | 31 | -0.278814 | 0.157876 | -0.436690 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 31 | 337.6289 | 0.0000 | 712 | 31 | -0.278814 | 0.021050 | -0.299865 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 15 | 76.0487 | 0.0000 | 123 | 15 | 0.192651 | 0.055230 | 0.137421 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.137421 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 15 | 25.3496 | 0.0000 | 123 | 15 | 0.192651 | 0.165691 | 0.026960 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 15 | 190.1217 | 0.0000 | 123 | 15 | 0.192651 | 0.022092 | 0.170559 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 8 | 148.8839 | 0.0000 | 153 | 8 | -0.099277 | 0.051102 | -0.150380 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.150380 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 8 | 49.6280 | 0.0000 | 153 | 8 | -0.099277 | 0.153307 | -0.252584 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 8 | 372.2097 | 0.0000 | 153 | 8 | -0.099277 | 0.020441 | -0.119718 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 34 | 113.1041 | 0.0000 | 655 | 35 | -0.334468 | 0.047346 | -0.381814 | — | — | FAIL | tuning | FAIL | -0.329325 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 34 | 37.7014 | 0.0000 | 655 | 35 | -0.334468 | 0.142039 | -0.476507 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 34 | 282.7603 | 0.0000 | 655 | 35 | -0.334468 | 0.018939 | -0.353406 | — | — | FAIL | tuning | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 23 | 132.4942 | 0.0000 | 559 | 23 | -0.376666 | 0.052692 | -0.429358 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.391345 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 23 | 44.1647 | 0.0000 | 559 | 23 | -0.376666 | 0.158077 | -0.534743 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 23 | 331.2355 | 0.0000 | 559 | 23 | -0.376666 | 0.021077 | -0.397743 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 52 | 152.3571 | 0.0000 | 1106 | 51 | -0.451617 | 0.034557 | -0.486174 | — | — | FAIL | tuning | FAIL | -0.323020 |
| ASSET:SUIUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 52 | 76.1785 | 0.0000 | 1106 | 51 | -0.451617 | 0.069115 | -0.520732 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 52 | 380.8926 | 0.0000 | 1106 | 51 | -0.451617 | 0.013823 | -0.465440 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 30 | 223.1137 | 0.0000 | 1076 | 30 | -0.365826 | 0.037934 | -0.403761 | — | — | FAIL | frozen3.0 | FAIL | -0.394411 |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 30 | 111.5569 | 0.0000 | 1076 | 30 | -0.365826 | 0.075869 | -0.441695 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 30 | 557.7843 | 0.0000 | 1076 | 30 | -0.365826 | 0.015174 | -0.381000 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 19 | 150.3001 | 0.0000 | 336 | 18 | -0.999444 | 0.034328 | -1.033772 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.588081 |
| ASSET:SUIUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 19 | 75.1500 | 0.0000 | 336 | 18 | -0.999444 | 0.068657 | -1.068101 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 19 | 375.7502 | 0.0000 | 336 | 18 | -0.999444 | 0.013731 | -1.013175 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 10 | 216.5387 | 0.0000 | 290 | 10 | -0.813184 | 0.039262 | -0.852446 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.852446 |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 10 | 108.2693 | 0.0000 | 290 | 10 | -0.813184 | 0.078524 | -0.891707 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 10 | 541.3466 | 0.0000 | 290 | 10 | -0.813184 | 0.015705 | -0.828888 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 33 | 154.4140 | 0.0000 | 770 | 33 | -0.189114 | 0.034977 | -0.224091 | — | — | FAIL | tuning | FAIL | -0.048713 |
| ASSET:SUIUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 33 | 77.2070 | 0.0000 | 770 | 33 | -0.189114 | 0.069953 | -0.259067 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 33 | 386.0351 | 0.0000 | 770 | 33 | -0.189114 | 0.013991 | -0.203105 | — | — | FAIL | tuning | — | — |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 20 | 256.5182 | 0.0000 | 786 | 20 | -0.076266 | 0.037515 | -0.113780 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.103947 |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 20 | 128.2591 | 0.0000 | 786 | 20 | -0.076266 | 0.075029 | -0.151295 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 20 | 641.2956 | 0.0000 | 786 | 20 | -0.076266 | 0.015006 | -0.091272 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 109 | 103.6665 | 0.0000 | 1751 | 104 | 0.085220 | 0.045691 | 0.039529 | — | — | PASS | tuning | PASS | 0.065953 |
| ASSET:LTCUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 109 | 51.8332 | 0.0000 | 1751 | 104 | 0.085220 | 0.091381 | -0.006161 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 109 | 259.1661 | 0.0000 | 1751 | 104 | 0.085220 | 0.018276 | 0.066944 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 64 | 163.7162 | 0.0000 | 1583 | 64 | 0.270660 | 0.046939 | 0.223721 | — | — | PASS | frozen3.0 | PASS | 0.243852 |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 64 | 81.8581 | 0.0000 | 1583 | 64 | 0.270660 | 0.093877 | 0.176783 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 64 | 409.2905 | 0.0000 | 1583 | 64 | 0.270660 | 0.018775 | 0.251885 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 72 | 114.6099 | 0.0000 | 1242 | 69 | 0.016862 | 0.042893 | -0.026032 | — | — | FAIL | tuning | FAIL | -0.026032 |
| ASSET:LTCUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 72 | 57.3049 | 0.0000 | 1242 | 69 | 0.016862 | 0.085787 | -0.068925 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 72 | 286.5247 | 0.0000 | 1242 | 69 | 0.016862 | 0.017157 | -0.000296 | — | — | FAIL | tuning | — | — |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 41 | 246.0094 | 0.0000 | 1161 | 41 | 0.199429 | 0.044374 | 0.155056 | — | — | PASS | frozen3.0 | PASS | 0.155056 |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 41 | 123.0047 | 0.0000 | 1161 | 41 | 0.199429 | 0.088747 | 0.110682 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 41 | 615.0235 | 0.0000 | 1161 | 41 | 0.199429 | 0.017749 | 0.181680 | — | — | PASS | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 37 | 92.5681 | 0.0000 | 509 | 36 | 0.183036 | 0.050117 | 0.132919 | — | — | PASS | tuning | PASS | 0.218156 |
| ASSET:LTCUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 37 | 46.2841 | 0.0000 | 509 | 36 | 0.183036 | 0.100234 | 0.082802 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 37 | 231.4203 | 0.0000 | 509 | 36 | 0.183036 | 0.020047 | 0.162990 | — | — | PASS | tuning | — | — |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 23 | 127.5891 | 0.0000 | 422 | 23 | 0.454152 | 0.052445 | 0.401706 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.470546 |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 23 | 63.7946 | 0.0000 | 422 | 23 | 0.454152 | 0.104891 | 0.349261 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 23 | 318.9728 | 0.0000 | 422 | 23 | 0.454152 | 0.020978 | 0.433173 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 97 | 103.6746 | 0.0000 | 2247 | 94 | 0.095830 | 0.047376 | 0.048454 | — | — | PASS | tuning | PASS | 0.042516 |
| ASSET:XMRUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 97 | 51.8373 | 0.0000 | 2247 | 94 | 0.095830 | 0.094752 | 0.001078 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 97 | 259.1866 | 0.0000 | 2247 | 94 | 0.095830 | 0.018950 | 0.076880 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 40 | 139.1847 | 0.0000 | 2370 | 40 | 0.040819 | 0.041062 | -0.000243 | — | — | FAIL | frozen3.0 | FAIL | -0.000243 |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 40 | 69.5924 | 0.0000 | 2370 | 40 | 0.040819 | 0.082124 | -0.041305 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 40 | 347.9618 | 0.0000 | 2370 | 40 | 0.040819 | 0.016425 | 0.024394 | — | — | PASS | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 73 | 103.6746 | 0.0000 | 1522 | 70 | 0.033832 | 0.046386 | -0.012555 | — | — | FAIL | tuning | FAIL | -0.021496 |
| ASSET:XMRUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 73 | 51.8373 | 0.0000 | 1522 | 70 | 0.033832 | 0.092773 | -0.058941 | — | — | FAIL | tuning | — | — |
| ASSET:XMRUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 73 | 259.1866 | 0.0000 | 1522 | 70 | 0.033832 | 0.018555 | 0.015277 | — | — | PASS | tuning | — | — |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 28 | 136.1738 | 0.0000 | 1670 | 28 | 0.039252 | 0.038996 | 0.000256 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.000256 |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 28 | 68.0869 | 0.0000 | 1670 | 28 | 0.039252 | 0.077991 | -0.038739 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 28 | 340.4346 | 0.0000 | 1670 | 28 | 0.039252 | 0.015598 | 0.023654 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 24 | 102.9715 | 0.0000 | 725 | 24 | 0.187349 | 0.048630 | 0.138719 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.135999 |
| ASSET:XMRUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 24 | 51.4857 | 0.0000 | 725 | 24 | 0.187349 | 0.097260 | 0.090088 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 24 | 257.4286 | 0.0000 | 725 | 24 | 0.187349 | 0.019452 | 0.167897 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 12 | 149.4917 | 0.0000 | 700 | 13 | 0.048647 | 0.048052 | 0.000594 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.000594 |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 12 | 74.7459 | 0.0000 | 700 | 13 | 0.048647 | 0.096104 | -0.047458 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 12 | 373.7293 | 0.0000 | 700 | 13 | 0.048647 | 0.019221 | 0.029426 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 94 | 96.0642 | 0.0000 | 1741 | 91 | -0.116294 | 0.060525 | -0.176819 | — | — | FAIL | tuning | FAIL | -0.115668 |
| ASSET:BNBUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 94 | 48.0321 | 0.0000 | 1741 | 91 | -0.116294 | 0.121050 | -0.237344 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 94 | 240.1606 | 0.0000 | 1741 | 91 | -0.116294 | 0.024210 | -0.140504 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 49 | 140.7277 | 0.0000 | 1848 | 49 | 0.239891 | 0.061532 | 0.178359 | — | — | PASS | frozen3.0 | PASS | 0.184345 |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 49 | 70.3639 | 0.0000 | 1848 | 49 | 0.239891 | 0.123064 | 0.116827 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 49 | 351.8193 | 0.0000 | 1848 | 49 | 0.239891 | 0.024613 | 0.215278 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 67 | 98.1705 | 0.0000 | 1056 | 65 | -0.323517 | 0.053575 | -0.377092 | — | — | FAIL | tuning | FAIL | -0.332824 |
| ASSET:BNBUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 67 | 49.0853 | 0.0000 | 1056 | 65 | -0.323517 | 0.107150 | -0.430667 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 67 | 245.4264 | 0.0000 | 1056 | 65 | -0.323517 | 0.021430 | -0.344947 | — | — | FAIL | tuning | — | — |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 30 | 178.9105 | 0.0000 | 1366 | 30 | 0.195260 | 0.058576 | 0.136684 | — | — | PASS | frozen3.0 | PASS | 0.136684 |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 30 | 89.4552 | 0.0000 | 1366 | 30 | 0.195260 | 0.117153 | 0.078107 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 30 | 447.2762 | 0.0000 | 1366 | 30 | 0.195260 | 0.023431 | 0.171830 | — | — | PASS | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 27 | 80.9208 | 0.0000 | 685 | 26 | 0.258898 | 0.073719 | 0.185179 | — | — | FAIL (provisional, n<30) | tuning | PASS | 0.187102 |
| ASSET:BNBUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 27 | 40.4604 | 0.0000 | 685 | 26 | 0.258898 | 0.147438 | 0.111460 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 27 | 202.3021 | 0.0000 | 685 | 26 | 0.258898 | 0.029488 | 0.229411 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 19 | 123.0428 | 0.0000 | 482 | 19 | 0.360990 | 0.068323 | 0.292667 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.372173 |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 19 | 61.5214 | 0.0000 | 482 | 19 | 0.360990 | 0.136645 | 0.224345 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 19 | 307.6071 | 0.0000 | 482 | 19 | 0.360990 | 0.027329 | 0.333661 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 93 | 149.7996 | 0.0000 | 2042 | 89 | 0.181667 | 0.034584 | 0.147083 | — | — | PASS | tuning | PASS | 0.147083 |
| ASSET:UNIUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 93 | 74.8998 | 0.0000 | 2042 | 89 | 0.181667 | 0.069168 | 0.112499 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 93 | 374.4990 | 0.0000 | 2042 | 89 | 0.181667 | 0.013834 | 0.167833 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 55 | 228.2787 | 0.0000 | 1743 | 55 | -0.178519 | 0.034485 | -0.213003 | — | — | FAIL | frozen3.0 | FAIL | -0.213003 |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 55 | 114.1394 | 0.0000 | 1743 | 55 | -0.178519 | 0.068969 | -0.247488 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 55 | 570.6968 | 0.0000 | 1743 | 55 | -0.178519 | 0.013794 | -0.192313 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 57 | 151.6234 | 0.0000 | 1366 | 54 | 0.460093 | 0.031725 | 0.428369 | — | — | PASS | tuning | PASS | 0.428369 |
| ASSET:UNIUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 57 | 75.8117 | 0.0000 | 1366 | 54 | 0.460093 | 0.063450 | 0.396644 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 57 | 379.0585 | 0.0000 | 1366 | 54 | 0.460093 | 0.012690 | 0.447404 | — | — | PASS | tuning | — | — |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 33 | 244.2461 | 0.0000 | 1159 | 33 | 0.351784 | 0.032120 | 0.319665 | — | — | PASS | frozen3.0 | PASS | 0.319665 |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 33 | 122.1231 | 0.0000 | 1159 | 33 | 0.351784 | 0.064239 | 0.287545 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 33 | 610.6153 | 0.0000 | 1159 | 33 | 0.351784 | 0.012848 | 0.338937 | — | — | PASS | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 36 | 141.6722 | 0.0000 | 676 | 36 | -0.479245 | 0.040447 | -0.519692 | — | — | FAIL | tuning | FAIL | -0.519692 |
| ASSET:UNIUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 36 | 70.8361 | 0.0000 | 676 | 36 | -0.479245 | 0.080894 | -0.560139 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 36 | 354.1806 | 0.0000 | 676 | 36 | -0.479245 | 0.016179 | -0.495423 | — | — | FAIL | tuning | — | — |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 22 | 225.2317 | 0.0000 | 584 | 23 | -1.074327 | 0.039500 | -1.113827 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.113827 |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 22 | 112.6159 | 0.0000 | 584 | 23 | -1.074327 | 0.079000 | -1.153327 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 22 | 563.0793 | 0.0000 | 584 | 23 | -1.074327 | 0.015800 | -1.090127 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 51 | 160.4605 | 0.0000 | 1030 | 49 | 0.011483 | 0.033311 | -0.021828 | — | — | FAIL | tuning | PASS | 0.021052 |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 51 | 53.4868 | 0.0000 | 1030 | 49 | 0.011483 | 0.099933 | -0.088450 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 51 | 401.1513 | 0.0000 | 1030 | 49 | 0.011483 | 0.013324 | -0.001841 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 30 | 272.4169 | 0.0000 | 1042 | 30 | -0.033818 | 0.031899 | -0.065717 | — | — | FAIL | frozen3.0 | FAIL (provisional, n<30) | -0.062548 |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 30 | 90.8056 | 0.0000 | 1042 | 30 | -0.033818 | 0.095697 | -0.129515 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 30 | 681.0423 | 0.0000 | 1042 | 30 | -0.033818 | 0.012760 | -0.046578 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 18 | 191.4389 | 0.0000 | 402 | 17 | 0.127031 | 0.029861 | 0.097171 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.039080 |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 18 | 63.8130 | 0.0000 | 402 | 17 | 0.127031 | 0.089582 | 0.037449 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 18 | 478.5973 | 0.0000 | 402 | 17 | 0.127031 | 0.011944 | 0.115087 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 9 | 313.8531 | 0.0000 | 351 | 9 | 0.104319 | 0.029251 | 0.075069 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.075069 |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 9 | 104.6177 | 0.0000 | 351 | 9 | 0.104319 | 0.087752 | 0.016567 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 9 | 784.6329 | 0.0000 | 351 | 9 | 0.104319 | 0.011700 | 0.092619 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 33 | 158.7415 | 0.0000 | 628 | 32 | -0.030757 | 0.035612 | -0.066369 | — | — | FAIL | tuning | PASS | 0.057624 |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 33 | 52.9138 | 0.0000 | 628 | 32 | -0.030757 | 0.106835 | -0.137592 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 33 | 396.8538 | 0.0000 | 628 | 32 | -0.030757 | 0.014245 | -0.045002 | — | — | FAIL | tuning | — | — |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 21 | 254.2540 | 0.0000 | 691 | 21 | -0.083320 | 0.033419 | -0.116739 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.103958 |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 21 | 84.7513 | 0.0000 | 691 | 21 | -0.083320 | 0.100256 | -0.183576 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 21 | 635.6349 | 0.0000 | 691 | 21 | -0.083320 | 0.013367 | -0.096688 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 92 | 109.5323 | 0.0000 | 2612 | 88 | -0.013542 | 0.036648 | -0.050190 | — | — | FAIL | tuning | FAIL | -0.046452 |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | charter | 20.0 | 20.0 | 92 | 54.7662 | 0.0000 | 2612 | 88 | -0.013542 | 0.073296 | -0.086838 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 92 | 273.8308 | 0.0000 | 2612 | 88 | -0.013542 | 0.014659 | -0.028201 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 46 | 179.6198 | 0.0000 | 1797 | 46 | -0.180312 | 0.044783 | -0.225095 | — | — | FAIL | frozen3.0 | FAIL | -0.223077 |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 46 | 89.8099 | 0.0000 | 1797 | 46 | -0.180312 | 0.089566 | -0.269878 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 46 | 449.0494 | 0.0000 | 1797 | 46 | -0.180312 | 0.017913 | -0.198225 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 49 | 117.4912 | 0.0000 | 1862 | 46 | -0.070791 | 0.034081 | -0.104871 | — | — | FAIL | tuning | FAIL | -0.104871 |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | charter | 20.0 | 20.0 | 49 | 58.7456 | 0.0000 | 1862 | 46 | -0.070791 | 0.068161 | -0.138952 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 49 | 293.7279 | 0.0000 | 1862 | 46 | -0.070791 | 0.013632 | -0.084423 | — | — | FAIL | tuning | — | — |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 24 | 258.7878 | 0.0000 | 1263 | 24 | -0.272201 | 0.042839 | -0.315040 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.315040 |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 24 | 129.3939 | 0.0000 | 1263 | 24 | -0.272201 | 0.085678 | -0.357879 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 24 | 646.9694 | 0.0000 | 1263 | 24 | -0.272201 | 0.017136 | -0.289337 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 43 | 103.4971 | 0.0000 | 750 | 43 | 0.138732 | 0.045580 | 0.093152 | — | — | PASS | tuning | PASS | 0.097925 |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | charter | 20.0 | 20.0 | 43 | 51.7485 | 0.0000 | 750 | 43 | 0.138732 | 0.091160 | 0.047572 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 43 | 258.7427 | 0.0000 | 750 | 43 | 0.138732 | 0.018232 | 0.120500 | — | — | PASS | tuning | — | — |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 22 | 163.3789 | 0.0000 | 534 | 23 | 0.138732 | 0.048652 | 0.090080 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.093309 |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 22 | 81.6895 | 0.0000 | 534 | 23 | 0.138732 | 0.097304 | 0.041428 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 22 | 408.4474 | 0.0000 | 534 | 23 | 0.138732 | 0.019461 | 0.119271 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 35 | 207.0010 | 0.0000 | 1213 | 33 | 0.071338 | 0.029812 | 0.041526 | — | — | PASS | tuning | FAIL | -0.303002 |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | charter | 30.0 | 30.0 | 35 | 69.0003 | 0.0000 | 1213 | 33 | 0.071338 | 0.089435 | -0.018098 | — | — | FAIL | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 35 | 517.5025 | 0.0000 | 1213 | 33 | 0.071338 | 0.011925 | 0.059413 | — | — | PASS | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 20 | 327.2325 | 0.0000 | 1032 | 20 | -0.003499 | 0.030887 | -0.034386 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.032224 |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | charter | 30.0 | 30.0 | 20 | 109.0775 | 0.0000 | 1032 | 20 | -0.003499 | 0.092662 | -0.096161 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 20 | 818.0813 | 0.0000 | 1032 | 20 | -0.003499 | 0.012355 | -0.015854 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 9 | 210.7095 | 0.0000 | 273 | 8 | 0.057739 | 0.022423 | 0.035316 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.129514 |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | charter | 30.0 | 30.0 | 9 | 70.2365 | 0.0000 | 273 | 8 | 0.057739 | 0.067268 | -0.009529 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 9 | 526.7737 | 0.0000 | 273 | 8 | 0.057739 | 0.008969 | 0.048770 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 4 | 607.9808 | 0.0000 | 201 | 4 | 0.327772 | 0.024811 | 0.302961 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.302961 |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | charter | 30.0 | 30.0 | 4 | 202.6603 | 0.0000 | 201 | 4 | 0.327772 | 0.074432 | 0.253340 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 4 | 1519.9519 | 0.0000 | 201 | 4 | 0.327772 | 0.009924 | 0.317848 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 26 | 187.0870 | 0.0000 | 940 | 26 | 0.076806 | 0.031459 | 0.045347 | — | — | FAIL (provisional, n<30) | tuning | FAIL | -0.363962 |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | charter | 30.0 | 30.0 | 26 | 62.3623 | 0.0000 | 940 | 26 | 0.076806 | 0.094378 | -0.017572 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 26 | 467.7174 | 0.0000 | 940 | 26 | 0.076806 | 0.012584 | 0.064222 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 16 | 274.5186 | 0.0000 | 831 | 17 | -0.087653 | 0.032303 | -0.119957 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.116858 |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | charter | 30.0 | 30.0 | 16 | 91.5062 | 0.0000 | 831 | 17 | -0.087653 | 0.096910 | -0.184564 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 16 | 686.2964 | 0.0000 | 831 | 17 | -0.087653 | 0.012921 | -0.100575 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 536 | 112.1398 | 0.0000 | 9060 | 517 | -0.148385 | 0.067558 | -0.215943 | — | — | FAIL | tuning | FAIL | -0.221070 |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | charter | 14.0 | 20.0 | 536 | 64.6173 | 0.0000 | 9060 | 517 | -0.148385 | 0.094581 | -0.242966 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 536 | 280.3495 | 0.0000 | 9060 | 517 | -0.148385 | 0.027023 | -0.175408 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 298 | 169.4957 | 0.0000 | 7445 | 292 | -0.163648 | 0.066558 | -0.230207 | — | — | FAIL | frozen3.0 | FAIL | -0.225675 |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | charter | 14.0 | 20.0 | 298 | 100.4048 | 0.0000 | 7445 | 292 | -0.163648 | 0.093182 | -0.256830 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 298 | 423.7392 | 0.0000 | 7445 | 292 | -0.163648 | 0.026623 | -0.190272 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 345 | 118.8701 | 0.0000 | 6220 | 334 | -0.202262 | 0.059926 | -0.262188 | — | — | FAIL | tuning | FAIL | -0.264391 |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | charter | 14.0 | 20.0 | 345 | 68.5807 | 0.0000 | 6220 | 334 | -0.202262 | 0.083896 | -0.286159 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 345 | 297.1751 | 0.0000 | 6220 | 334 | -0.202262 | 0.023970 | -0.226233 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 196 | 169.4957 | 0.0000 | 5075 | 190 | -0.275966 | 0.058167 | -0.334133 | — | — | FAIL | frozen3.0 | FAIL | -0.334133 |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | charter | 14.0 | 20.0 | 196 | 99.6913 | 0.0000 | 5075 | 190 | -0.275966 | 0.081434 | -0.357400 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 196 | 423.7392 | 0.0000 | 5075 | 190 | -0.275966 | 0.023267 | -0.299233 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 191 | 103.5067 | 0.0000 | 2840 | 186 | -0.020693 | 0.082389 | -0.103083 | FAIL | FAIL | — | tuning | FAIL | -0.106488 |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | charter | 14.0 | 20.0 | 191 | 59.4907 | 0.0000 | 2840 | 186 | -0.020693 | 0.115345 | -0.136038 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 191 | 258.7666 | 0.0000 | 2840 | 186 | -0.020693 | 0.032956 | -0.053649 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 102 | 172.3760 | 0.0000 | 2370 | 104 | 0.062926 | 0.088386 | -0.025459 | — | — | FAIL | frozen3.0 | PASS | 0.006179 |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | charter | 14.0 | 20.0 | 102 | 100.4048 | 0.0000 | 2370 | 104 | 0.062926 | 0.123740 | -0.060814 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 102 | 430.9400 | 0.0000 | 2370 | 104 | 0.062926 | 0.035354 | 0.027572 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | ALL | calibrated | taker | 10.0 | 10.0 | 1279 | 118.7719 | 0.0000 | 24642 | 1233 | -0.067821 | 0.067558 | -0.135379 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | FAIL | -0.130479 |
| POOLED:PANEL17 | 4h | ALL | calibrated | charter | 14.0 | 30.0 | 1279 | 59.3142 | 0.0000 | 24642 | 1233 | -0.067821 | 0.145435 | -0.213256 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | ALL | calibrated | maker | 4.0 | 4.0 | 1279 | 296.9297 | 0.0000 | 24642 | 1233 | -0.067821 | 0.027023 | -0.094844 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 709 | 184.3811 | 0.0000 | 21957 | 702 | -0.073927 | 0.066558 | -0.140486 | — | — | FAIL | frozen3.0 | FAIL | -0.135336 |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | charter | 14.0 | 30.0 | 709 | 92.4872 | 0.0000 | 21957 | 702 | -0.073927 | 0.157876 | -0.231803 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 709 | 460.9527 | 0.0000 | 21957 | 702 | -0.073927 | 0.026623 | -0.100551 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | tuning | calibrated | taker | 10.0 | 10.0 | 728 | 117.4379 | 0.0000 | 14447 | 700 | -0.093631 | 0.059926 | -0.153557 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | FAIL | -0.152601 |
| POOLED:PANEL17 | 4h | tuning | calibrated | charter | 14.0 | 30.0 | 728 | 61.7867 | 0.0000 | 14447 | 700 | -0.093631 | 0.165691 | -0.259321 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | tuning | calibrated | maker | 4.0 | 4.0 | 728 | 293.5946 | 0.0000 | 14447 | 700 | -0.093631 | 0.023970 | -0.117601 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 386 | 180.8851 | 0.0000 | 12729 | 380 | -0.090671 | 0.058576 | -0.149247 | — | — | FAIL | frozen3.0 | FAIL | -0.149247 |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | charter | 14.0 | 30.0 | 386 | 97.9947 | 0.0000 | 12729 | 380 | -0.090671 | 0.153307 | -0.243978 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 386 | 452.2127 | 0.0000 | 12729 | 380 | -0.090671 | 0.023431 | -0.114102 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | holdout | calibrated | taker | 10.0 | 10.0 | 551 | 122.5104 | 0.0000 | 10195 | 541 | -0.030691 | 0.082389 | -0.113080 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | FAIL | -0.106488 |
| POOLED:PANEL17 | 4h | holdout | calibrated | charter | 14.0 | 30.0 | 551 | 55.9772 | 0.0000 | 10195 | 541 | -0.030691 | 0.147438 | -0.178129 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | holdout | calibrated | maker | 4.0 | 4.0 | 551 | 306.2761 | 0.0000 | 10195 | 541 | -0.030691 | 0.032956 | -0.063647 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 323 | 189.0014 | 0.0000 | 9228 | 328 | -0.055517 | 0.088386 | -0.143903 | — | — | FAIL | frozen3.0 | FAIL | -0.130289 |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | charter | 14.0 | 30.0 | 323 | 88.5719 | 0.0000 | 9228 | 328 | -0.055517 | 0.158077 | -0.213594 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 323 | 472.5034 | 0.0000 | 9228 | 328 | -0.055517 | 0.035354 | -0.090871 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 34 | 128.9088 | 0.0000 | 602 | 32 | -0.174457 | 0.036763 | -0.211219 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 12h | ALL | calibrated | charter | 14.0 | 14.0 | 34 | 92.0777 | 0.0000 | 602 | 32 | -0.174457 | 0.051468 | -0.225924 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 34 | 322.2719 | 0.0000 | 602 | 32 | -0.174457 | 0.014705 | -0.189162 | — | — | FAIL | tuning | — | — |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 18 | 202.1418 | 0.0000 | 657 | 18 | -0.049229 | 0.034450 | -0.083679 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 18 | 144.3870 | 0.0000 | 657 | 18 | -0.049229 | 0.048230 | -0.097459 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 18 | 505.3545 | 0.0000 | 657 | 18 | -0.049229 | 0.013780 | -0.063009 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 23 | 149.8669 | 0.0000 | 359 | 22 | -0.225212 | 0.032504 | -0.257716 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | tuning | calibrated | charter | 14.0 | 14.0 | 23 | 107.0478 | 0.0000 | 359 | 22 | -0.225212 | 0.045505 | -0.270718 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 23 | 374.6673 | 0.0000 | 359 | 22 | -0.225212 | 0.013002 | -0.238214 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 10 | 272.4229 | 0.0000 | 520 | 10 | 0.145068 | 0.029509 | 0.115559 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 10 | 194.5878 | 0.0000 | 520 | 10 | 0.145068 | 0.041313 | 0.103755 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 10 | 681.0572 | 0.0000 | 520 | 10 | 0.145068 | 0.011804 | 0.133264 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 11 | 105.5616 | 0.0000 | 243 | 11 | -0.096916 | 0.045026 | -0.141942 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | holdout | calibrated | charter | 14.0 | 14.0 | 11 | 75.4011 | 0.0000 | 243 | 11 | -0.096916 | 0.063037 | -0.159953 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 11 | 263.9040 | 0.0000 | 243 | 11 | -0.096916 | 0.018010 | -0.114927 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 8 | 122.8061 | 0.0000 | 137 | 9 | -1.097911 | 0.048229 | -1.146140 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 8 | 87.7186 | 0.0000 | 137 | 9 | -1.097911 | 0.067520 | -1.165431 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 8 | 307.0151 | 0.0000 | 137 | 9 | -1.097911 | 0.019291 | -1.117203 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 44 | 125.2035 | 0.0000 | 805 | 41 | -0.147655 | 0.028134 | -0.175789 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 12h | ALL | calibrated | charter | 14.0 | 14.0 | 44 | 89.4311 | 0.0000 | 805 | 41 | -0.147655 | 0.039388 | -0.187043 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 44 | 313.0088 | 0.0000 | 805 | 41 | -0.147655 | 0.011254 | -0.158909 | — | — | FAIL | tuning | — | — |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 15 | 210.9399 | 0.0000 | 516 | 15 | -0.120319 | 0.027088 | -0.147406 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | charter | 14.0 | 14.0 | 15 | 150.6714 | 0.0000 | 516 | 15 | -0.120319 | 0.037923 | -0.158241 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 15 | 527.3498 | 0.0000 | 516 | 15 | -0.120319 | 0.010835 | -0.131154 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 27 | 133.1616 | 0.0000 | 632 | 26 | -0.147259 | 0.027749 | -0.175008 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | tuning | calibrated | charter | 14.0 | 14.0 | 27 | 95.1154 | 0.0000 | 632 | 26 | -0.147259 | 0.038849 | -0.186108 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 27 | 332.9041 | 0.0000 | 632 | 26 | -0.147259 | 0.011100 | -0.158359 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 8 | 260.1400 | 0.0000 | 348 | 8 | 0.086961 | 0.025336 | 0.061626 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | charter | 14.0 | 14.0 | 8 | 185.8143 | 0.0000 | 348 | 8 | 0.086961 | 0.035470 | 0.051491 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 8 | 650.3499 | 0.0000 | 348 | 8 | 0.086961 | 0.010134 | 0.076827 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 17 | 123.3257 | 0.0000 | 173 | 16 | -0.147655 | 0.029416 | -0.177071 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | holdout | calibrated | charter | 14.0 | 14.0 | 17 | 88.0898 | 0.0000 | 173 | 16 | -0.147655 | 0.041182 | -0.188837 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 17 | 308.3143 | 0.0000 | 173 | 16 | -0.147655 | 0.011766 | -0.159421 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 7 | 193.3227 | 0.0000 | 168 | 8 | -0.578756 | 0.031039 | -0.609796 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | charter | 14.0 | 14.0 | 7 | 138.0876 | 0.0000 | 168 | 8 | -0.578756 | 0.043455 | -0.622211 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 7 | 483.3067 | 0.0000 | 168 | 8 | -0.578756 | 0.012416 | -0.591172 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 32 | 281.6504 | 0.0000 | 405 | 31 | -0.435370 | 0.020633 | -0.456003 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 12h | ALL | calibrated | charter | 20.0 | 20.0 | 32 | 140.8252 | 0.0000 | 405 | 31 | -0.435370 | 0.041266 | -0.476635 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 32 | 704.1261 | 0.0000 | 405 | 31 | -0.435370 | 0.008253 | -0.443623 | — | — | FAIL | tuning | — | — |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 21 | 374.0090 | 0.0000 | 316 | 21 | -1.621259 | 0.021452 | -1.642711 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 21 | 187.0045 | 0.0000 | 316 | 21 | -1.621259 | 0.042903 | -1.664162 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 21 | 935.0225 | 0.0000 | 316 | 21 | -1.621259 | 0.008581 | -1.629840 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 21 | 322.0536 | 0.0000 | 235 | 20 | -0.679410 | 0.018689 | -0.698100 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | tuning | calibrated | charter | 20.0 | 20.0 | 21 | 161.0268 | 0.0000 | 235 | 20 | -0.679410 | 0.037379 | -0.716789 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 21 | 805.1341 | 0.0000 | 235 | 20 | -0.679410 | 0.007476 | -0.686886 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 14 | 388.8574 | 0.0000 | 161 | 14 | -1.984951 | 0.019082 | -2.004033 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 14 | 194.4287 | 0.0000 | 161 | 14 | -1.984951 | 0.038164 | -2.023115 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 14 | 972.1435 | 0.0000 | 161 | 14 | -1.984951 | 0.007633 | -1.992583 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 11 | 201.1567 | 0.0000 | 170 | 12 | -0.107096 | 0.023320 | -0.130416 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | holdout | calibrated | charter | 20.0 | 20.0 | 11 | 100.5784 | 0.0000 | 170 | 12 | -0.107096 | 0.046640 | -0.153736 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 11 | 502.8918 | 0.0000 | 170 | 12 | -0.107096 | 0.009328 | -0.116424 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 7 | 312.6893 | 0.0000 | 155 | 8 | -1.001835 | 0.024305 | -1.026140 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 7 | 156.3446 | 0.0000 | 155 | 8 | -1.001835 | 0.048610 | -1.050445 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 7 | 781.7231 | 0.0000 | 155 | 8 | -1.001835 | 0.009722 | -1.011557 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 36 | 288.4149 | 0.0000 | 509 | 35 | -0.639357 | 0.015216 | -0.654573 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 12h | ALL | calibrated | charter | 20.0 | 20.0 | 36 | 144.2074 | 0.0000 | 509 | 35 | -0.639357 | 0.030432 | -0.669789 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 36 | 721.0372 | 0.0000 | 509 | 35 | -0.639357 | 0.006086 | -0.645443 | — | — | FAIL | tuning | — | — |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 17 | 493.9385 | 0.0000 | 499 | 16 | -0.449784 | 0.013497 | -0.463281 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 17 | 246.9693 | 0.0000 | 499 | 16 | -0.449784 | 0.026993 | -0.476778 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 17 | 1234.8463 | 0.0000 | 499 | 16 | -0.449784 | 0.005399 | -0.455183 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 20 | 335.8176 | 0.0000 | 309 | 19 | -0.483813 | 0.014215 | -0.498028 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | tuning | calibrated | charter | 20.0 | 20.0 | 20 | 167.9088 | 0.0000 | 309 | 19 | -0.483813 | 0.028431 | -0.512243 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 20 | 839.5440 | 0.0000 | 309 | 19 | -0.483813 | 0.005686 | -0.489499 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 9 | 530.3491 | 0.0000 | 273 | 9 | -0.323803 | 0.011950 | -0.335753 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 9 | 265.1746 | 0.0000 | 273 | 9 | -0.323803 | 0.023900 | -0.347703 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 9 | 1325.8729 | 0.0000 | 273 | 9 | -0.323803 | 0.004780 | -0.328583 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 16 | 279.3830 | 0.0000 | 200 | 16 | -0.693089 | 0.018021 | -0.711110 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | holdout | calibrated | charter | 20.0 | 20.0 | 16 | 139.6915 | 0.0000 | 200 | 16 | -0.693089 | 0.036042 | -0.729131 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 16 | 698.4576 | 0.0000 | 200 | 16 | -0.693089 | 0.007208 | -0.700297 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 8 | 482.9595 | 0.0000 | 226 | 8 | -0.562324 | 0.015514 | -0.577839 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 8 | 241.4798 | 0.0000 | 226 | 8 | -0.562324 | 0.031029 | -0.593353 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 8 | 1207.3988 | 0.0000 | 226 | 8 | -0.562324 | 0.006206 | -0.568530 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 33 | 318.8312 | 0.0000 | 708 | 33 | 0.119981 | 0.018599 | 0.101382 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 12h | ALL | calibrated | charter | 20.0 | 20.0 | 33 | 159.4156 | 0.0000 | 708 | 33 | 0.119981 | 0.037197 | 0.082784 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 33 | 797.0779 | 0.0000 | 708 | 33 | 0.119981 | 0.007439 | 0.112542 | — | — | PASS | tuning | — | — |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 21 | 540.6491 | 0.0000 | 659 | 21 | 0.149308 | 0.017507 | 0.131801 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | charter | 20.0 | 20.0 | 21 | 270.3246 | 0.0000 | 659 | 21 | 0.149308 | 0.035014 | 0.114294 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 21 | 1351.6228 | 0.0000 | 659 | 21 | 0.149308 | 0.007003 | 0.142306 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 22 | 296.8930 | 0.0000 | 442 | 22 | -0.124810 | 0.019560 | -0.144370 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | tuning | calibrated | charter | 20.0 | 20.0 | 22 | 148.4465 | 0.0000 | 442 | 22 | -0.124810 | 0.039119 | -0.163929 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 22 | 742.2325 | 0.0000 | 442 | 22 | -0.124810 | 0.007824 | -0.132634 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 13 | 557.7337 | 0.0000 | 521 | 13 | -0.050443 | 0.018027 | -0.068470 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | charter | 20.0 | 20.0 | 13 | 278.8669 | 0.0000 | 521 | 13 | -0.050443 | 0.036055 | -0.086497 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 13 | 1394.3343 | 0.0000 | 521 | 13 | -0.050443 | 0.007211 | -0.057653 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 11 | 380.9880 | 0.0000 | 266 | 12 | 0.431446 | 0.017136 | 0.414310 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | holdout | calibrated | charter | 20.0 | 20.0 | 11 | 190.4940 | 0.0000 | 266 | 12 | 0.431446 | 0.034273 | 0.397174 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 11 | 952.4701 | 0.0000 | 266 | 12 | 0.431446 | 0.006855 | 0.424592 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 8 | 460.8186 | 0.0000 | 138 | 9 | 0.750394 | 0.015911 | 0.734483 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | charter | 20.0 | 20.0 | 8 | 230.4093 | 0.0000 | 138 | 9 | 0.750394 | 0.031821 | 0.718572 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 8 | 1152.0464 | 0.0000 | 138 | 9 | 0.750394 | 0.006364 | 0.744029 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | taker | 10.0 | 10.0 | 179 | 208.3818 | 0.0000 | 3029 | 172 | -0.212699 | 0.036763 | -0.249461 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | charter | 14.0 | 20.0 | 179 | 117.6007 | 0.0000 | 3029 | 172 | -0.212699 | 0.051468 | -0.264167 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | maker | 4.0 | 4.0 | 179 | 520.9546 | 0.0000 | 3029 | 172 | -0.212699 | 0.014705 | -0.227404 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | taker | 10.0 | 10.0 | 92 | 377.4985 | 0.0000 | 2647 | 91 | -0.178893 | 0.034450 | -0.213344 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | charter | 14.0 | 20.0 | 92 | 196.1020 | 0.0000 | 2647 | 91 | -0.178893 | 0.048230 | -0.227124 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | maker | 4.0 | 4.0 | 92 | 943.7463 | 0.0000 | 2647 | 91 | -0.178893 | 0.013780 | -0.192673 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | taker | 10.0 | 10.0 | 113 | 211.4430 | 0.0000 | 1977 | 109 | -0.267940 | 0.032504 | -0.300443 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | charter | 14.0 | 20.0 | 113 | 123.8663 | 0.0000 | 1977 | 109 | -0.267940 | 0.045505 | -0.313445 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | maker | 4.0 | 4.0 | 113 | 528.6076 | 0.0000 | 1977 | 109 | -0.267940 | 0.013002 | -0.280941 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | taker | 10.0 | 10.0 | 54 | 399.1984 | 0.0000 | 1823 | 54 | -0.110176 | 0.029509 | -0.139685 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | charter | 14.0 | 20.0 | 54 | 209.9373 | 0.0000 | 1823 | 54 | -0.110176 | 0.041313 | -0.151489 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | maker | 4.0 | 4.0 | 54 | 997.9959 | 0.0000 | 1823 | 54 | -0.110176 | 0.011804 | -0.121980 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | taker | 10.0 | 10.0 | 66 | 199.1925 | 0.0000 | 1052 | 67 | -0.112893 | 0.045026 | -0.157919 | FAIL | FAIL | — | tuning | — | — |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | charter | 14.0 | 20.0 | 66 | 114.1504 | 0.0000 | 1052 | 67 | -0.112893 | 0.063037 | -0.175929 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | maker | 4.0 | 4.0 | 66 | 497.9811 | 0.0000 | 1052 | 67 | -0.112893 | 0.018010 | -0.130903 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | taker | 10.0 | 10.0 | 38 | 274.7553 | 0.0000 | 824 | 42 | -0.329429 | 0.048229 | -0.377657 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | charter | 14.0 | 20.0 | 38 | 149.1502 | 0.0000 | 824 | 42 | -0.329429 | 0.067520 | -0.396949 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | maker | 4.0 | 4.0 | 38 | 686.8883 | 0.0000 | 824 | 42 | -0.329429 | 0.019291 | -0.348720 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 20 | 214.6702 | 0.0000 | 318 | 20 | 0.128050 | 0.027438 | 0.100612 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.118250 |
| ASSET:BTCUSDT | 1d | ALL | calibrated | charter | 14.0 | 14.0 | 20 | 153.3359 | 0.0000 | 318 | 20 | 0.128050 | 0.038413 | 0.089637 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 20 | 536.6756 | 0.0000 | 318 | 20 | 0.128050 | 0.010975 | 0.117075 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 11 | 263.1757 | 0.0000 | 341 | 11 | 0.234585 | 0.024895 | 0.209690 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.212120 |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | charter | 14.0 | 14.0 | 11 | 187.9827 | 0.0000 | 341 | 11 | 0.234585 | 0.034853 | 0.199732 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 11 | 657.9393 | 0.0000 | 341 | 11 | 0.234585 | 0.009958 | 0.224627 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 12 | 238.6143 | 0.0000 | 225 | 12 | 0.493344 | 0.024895 | 0.468449 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.468449 |
| ASSET:BTCUSDT | 1d | tuning | calibrated | charter | 14.0 | 14.0 | 12 | 170.4388 | 0.0000 | 225 | 12 | 0.493344 | 0.034853 | 0.458491 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 12 | 596.5359 | 0.0000 | 225 | 12 | 0.493344 | 0.009958 | 0.483386 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 8 | 268.0350 | 0.0000 | 270 | 8 | 0.545817 | 0.022085 | 0.523732 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.523732 |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | charter | 14.0 | 14.0 | 8 | 191.4536 | 0.0000 | 270 | 8 | 0.545817 | 0.030918 | 0.514898 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 8 | 670.0874 | 0.0000 | 270 | 8 | 0.545817 | 0.008834 | 0.536983 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 8 | 128.0256 | 0.0000 | 93 | 9 | -1.708106 | 0.031950 | -1.740056 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -1.543891 |
| ASSET:BTCUSDT | 1d | holdout | calibrated | charter | 14.0 | 14.0 | 8 | 91.4468 | 0.0000 | 93 | 9 | -1.708106 | 0.044730 | -1.752836 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 8 | 320.0639 | 0.0000 | 93 | 9 | -1.708106 | 0.012780 | -1.720886 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 3 | 209.5816 | 0.0000 | 71 | 4 | -1.123563 | 0.031150 | -1.154714 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.111767 |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | charter | 14.0 | 14.0 | 3 | 149.7011 | 0.0000 | 71 | 4 | -1.123563 | 0.043611 | -1.167174 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 3 | 523.9540 | 0.0000 | 71 | 4 | -1.123563 | 0.012460 | -1.136024 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 20 | 208.0272 | 0.0000 | 264 | 19 | -0.248860 | 0.018561 | -0.267421 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.267421 |
| ASSET:ETHUSDT | 1d | ALL | calibrated | charter | 14.0 | 14.0 | 20 | 148.5908 | 0.0000 | 264 | 19 | -0.248860 | 0.025985 | -0.274845 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 20 | 520.0680 | 0.0000 | 264 | 19 | -0.248860 | 0.007424 | -0.256284 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 9 | 355.7785 | 0.0000 | 178 | 9 | -0.648832 | 0.021016 | -0.669848 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.669848 |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | charter | 14.0 | 14.0 | 9 | 254.1275 | 0.0000 | 178 | 9 | -0.648832 | 0.029423 | -0.678255 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 9 | 889.4463 | 0.0000 | 178 | 9 | -0.648832 | 0.008406 | -0.657239 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 13 | 268.2691 | 0.0000 | 139 | 12 | 0.003756 | 0.018409 | -0.014653 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.014653 |
| ASSET:ETHUSDT | 1d | tuning | calibrated | charter | 14.0 | 14.0 | 13 | 191.6208 | 0.0000 | 139 | 12 | 0.003756 | 0.025772 | -0.022016 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 13 | 670.6727 | 0.0000 | 139 | 12 | 0.003756 | 0.007363 | -0.003608 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 6 | 352.8910 | 0.0000 | 140 | 6 | -0.252265 | 0.021960 | -0.274224 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.274224 |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | charter | 14.0 | 14.0 | 6 | 252.0650 | 0.0000 | 140 | 6 | -0.252265 | 0.030744 | -0.283008 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 6 | 882.2276 | 0.0000 | 140 | 6 | -0.252265 | 0.008784 | -0.261049 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 7 | 193.3227 | 0.0000 | 125 | 8 | -0.629284 | 0.018640 | -0.647924 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.647924 |
| ASSET:ETHUSDT | 1d | holdout | calibrated | charter | 14.0 | 14.0 | 7 | 138.0876 | 0.0000 | 125 | 8 | -0.629284 | 0.026096 | -0.655380 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 7 | 483.3067 | 0.0000 | 125 | 8 | -0.629284 | 0.007456 | -0.636740 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 3 | 544.0530 | 0.0000 | 38 | 4 | -2.057052 | 0.014013 | -2.071065 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -2.071065 |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | charter | 14.0 | 14.0 | 3 | 388.6093 | 0.0000 | 38 | 4 | -2.057052 | 0.019618 | -2.076670 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1360.1326 | 0.0000 | 38 | 4 | -2.057052 | 0.005605 | -2.062657 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 18 | 355.3771 | 0.0000 | 161 | 18 | -0.779675 | 0.014465 | -0.794140 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.776888 |
| ASSET:SOLUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 18 | 177.6885 | 0.0000 | 161 | 18 | -0.779675 | 0.028931 | -0.808606 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 18 | 888.4426 | 0.0000 | 161 | 18 | -0.779675 | 0.005786 | -0.785461 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 12 | 364.5075 | 0.0000 | 300 | 12 | -0.634342 | 0.013674 | -0.648016 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.638973 |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 12 | 182.2537 | 0.0000 | 300 | 12 | -0.634342 | 0.027349 | -0.661691 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 12 | 911.2686 | 0.0000 | 300 | 12 | -0.634342 | 0.005470 | -0.639812 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 11 | 359.5343 | 0.0000 | 83 | 11 | -1.213381 | 0.012138 | -1.225519 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.342585 |
| ASSET:SOLUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 11 | 179.7672 | 0.0000 | 83 | 11 | -1.213381 | 0.024275 | -1.237656 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 11 | 898.8358 | 0.0000 | 83 | 11 | -1.213381 | 0.004855 | -1.218236 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 6 | 455.7705 | 0.0000 | 173 | 6 | -0.591843 | 0.012170 | -0.604013 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.604013 |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 6 | 227.8853 | 0.0000 | 173 | 6 | -0.591843 | 0.024341 | -0.616184 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 6 | 1139.4263 | 0.0000 | 173 | 6 | -0.591843 | 0.004868 | -0.596711 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 7 | 319.5590 | 0.0000 | 78 | 7 | -0.087498 | 0.017131 | -0.104629 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.819022 |
| ASSET:SOLUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 7 | 159.7795 | 0.0000 | 78 | 7 | -0.087498 | 0.034263 | -0.121761 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 7 | 798.8974 | 0.0000 | 78 | 7 | -0.087498 | 0.006853 | -0.094351 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 6 | 342.7813 | 0.0000 | 127 | 6 | -0.852407 | 0.016703 | -0.869110 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.806750 |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 6 | 171.3907 | 0.0000 | 127 | 6 | -0.852407 | 0.033406 | -0.885813 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 6 | 856.9533 | 0.0000 | 127 | 6 | -0.852407 | 0.006681 | -0.859088 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 16 | 382.7558 | 0.0000 | 242 | 14 | -0.337406 | 0.009900 | -0.347306 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.347306 |
| ASSET:NEARUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 16 | 191.3779 | 0.0000 | 242 | 14 | -0.337406 | 0.019800 | -0.357206 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 16 | 956.8895 | 0.0000 | 242 | 14 | -0.337406 | 0.003960 | -0.341366 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 8 | 667.5462 | 0.0000 | 206 | 8 | 0.529435 | 0.010696 | 0.518739 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.518739 |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 8 | 333.7731 | 0.0000 | 206 | 8 | 0.529435 | 0.021393 | 0.508043 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 8 | 1668.8654 | 0.0000 | 206 | 8 | 0.529435 | 0.004279 | 0.525157 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 11 | 383.3987 | 0.0000 | 108 | 10 | -0.615270 | 0.008182 | -0.623452 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.623452 |
| ASSET:NEARUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 11 | 191.6994 | 0.0000 | 108 | 10 | -0.615270 | 0.016365 | -0.631634 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 11 | 958.4968 | 0.0000 | 108 | 10 | -0.615270 | 0.003273 | -0.618543 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 6 | 529.4842 | 0.0000 | 79 | 6 | 1.660360 | 0.011500 | 1.648860 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 1.648860 |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 6 | 264.7421 | 0.0000 | 79 | 6 | 1.660360 | 0.023000 | 1.637360 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 6 | 1323.7106 | 0.0000 | 79 | 6 | 1.660360 | 0.004600 | 1.655760 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 5 | 380.5584 | 0.0000 | 134 | 5 | -0.235201 | 0.010539 | -0.245740 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.245740 |
| ASSET:NEARUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 5 | 190.2792 | 0.0000 | 134 | 5 | -0.235201 | 0.021078 | -0.256279 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 5 | 951.3961 | 0.0000 | 134 | 5 | -0.235201 | 0.004216 | -0.239416 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 748.9509 | 0.0000 | 127 | 3 | 0.107230 | 0.010481 | 0.096749 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.096749 |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 2 | 374.4755 | 0.0000 | 127 | 3 | 0.107230 | 0.020963 | 0.086267 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1872.3774 | 0.0000 | 127 | 3 | 0.107230 | 0.004193 | 0.103038 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 19 | 418.4012 | 0.0000 | 298 | 18 | -0.256403 | 0.014806 | -0.271209 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.271209 |
| ASSET:ZECUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 19 | 209.2006 | 0.0000 | 298 | 18 | -0.256403 | 0.029612 | -0.286015 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 19 | 1046.0030 | 0.0000 | 298 | 18 | -0.256403 | 0.005922 | -0.262325 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 13 | 634.3795 | 0.0000 | 404 | 12 | 0.517285 | 0.011873 | 0.505412 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.505412 |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 13 | 317.1898 | 0.0000 | 404 | 12 | 0.517285 | 0.023746 | 0.493539 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 13 | 1585.9488 | 0.0000 | 404 | 12 | 0.517285 | 0.004749 | 0.512536 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 13 | 413.9918 | 0.0000 | 224 | 13 | -0.196887 | 0.016232 | -0.213119 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.213119 |
| ASSET:ZECUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 13 | 206.9959 | 0.0000 | 224 | 13 | -0.196887 | 0.032464 | -0.229351 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 13 | 1034.9794 | 0.0000 | 224 | 13 | -0.196887 | 0.006493 | -0.203380 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 9 | 511.9249 | 0.0000 | 320 | 9 | 0.406904 | 0.012237 | 0.394667 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.394667 |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 9 | 255.9624 | 0.0000 | 320 | 9 | 0.406904 | 0.024474 | 0.382430 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 9 | 1279.8122 | 0.0000 | 320 | 9 | 0.406904 | 0.004895 | 0.402009 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 6 | 592.0310 | 0.0000 | 74 | 6 | -1.540157 | 0.013843 | -1.553999 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -1.553999 |
| ASSET:ZECUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 6 | 296.0155 | 0.0000 | 74 | 6 | -1.540157 | 0.027686 | -1.567842 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 6 | 1480.0776 | 0.0000 | 74 | 6 | -1.540157 | 0.005537 | -1.545694 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 4 | 926.1491 | 0.0000 | 84 | 4 | 1.201394 | 0.010938 | 1.190455 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 1.190455 |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 4 | 463.0746 | 0.0000 | 84 | 4 | 1.201394 | 0.021877 | 1.179517 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 4 | 2315.3728 | 0.0000 | 84 | 4 | 1.201394 | 0.004375 | 1.197018 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 6 | 380.3142 | 0.0000 | 71 | 6 | 0.165212 | 0.010207 | 0.155004 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | 0.155004 |
| ASSET:ENAUSDT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 6 | 126.7714 | 0.0000 | 71 | 6 | 0.165212 | 0.030622 | 0.134589 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 6 | 950.7856 | 0.0000 | 71 | 6 | 0.165212 | 0.004083 | 0.161129 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 1 | 4397.7320 | 0.0000 | 110 | 1 | -0.450660 | 0.009364 | -0.460024 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.460024 |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 1 | 1465.9107 | 0.0000 | 110 | 1 | -0.450660 | 0.028093 | -0.478752 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 1 | 10994.3301 | 0.0000 | 110 | 1 | -0.450660 | 0.003746 | -0.454405 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 1 | 496.3339 | 0.0000 | 5 | 1 | -2.697716 | 0.007963 | -2.705679 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -2.705679 |
| ASSET:ENAUSDT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 1 | 165.4446 | 0.0000 | 5 | 1 | -2.697716 | 0.023889 | -2.721605 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 1 | 1240.8347 | 0.0000 | 5 | 1 | -2.697716 | 0.003185 | -2.700901 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | — |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 5 | 306.7083 | 0.0000 | 66 | 5 | 0.401665 | 0.010730 | 0.390935 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | 0.390935 |
| ASSET:ENAUSDT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 5 | 102.2361 | 0.0000 | 66 | 5 | 0.401665 | 0.032190 | 0.369475 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 5 | 766.7707 | 0.0000 | 66 | 5 | 0.401665 | 0.004292 | 0.397373 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1 | 4397.7320 | 0.0000 | 110 | 1 | -0.450660 | 0.009364 | -0.460024 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.460024 |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 1 | 1465.9107 | 0.0000 | 110 | 1 | -0.450660 | 0.028093 | -0.478752 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1 | 10994.3301 | 0.0000 | 110 | 1 | -0.450660 | 0.003746 | -0.454405 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 3 | 594.0707 | 0.0000 | 124 | 3 | -0.155302 | 0.011491 | -0.166794 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.166794 |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 3 | 198.0236 | 0.0000 | 124 | 3 | -0.155302 | 0.034474 | -0.189776 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 3 | 1485.1767 | 0.0000 | 124 | 3 | -0.155302 | 0.004596 | -0.159899 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2 | 926.8118 | 0.0000 | 39 | 2 | -1.923894 | 0.007166 | -1.931060 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.931060 |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 2 | 308.9373 | 0.0000 | 39 | 2 | -1.923894 | 0.021497 | -1.945391 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2 | 2317.0296 | 0.0000 | 39 | 2 | -1.923894 | 0.002866 | -1.926761 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | — |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 3 | 594.0707 | 0.0000 | 124 | 3 | -0.155302 | 0.011491 | -0.166794 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.166794 |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 3 | 198.0236 | 0.0000 | 124 | 3 | -0.155302 | 0.034474 | -0.189776 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 3 | 1485.1767 | 0.0000 | 124 | 3 | -0.155302 | 0.004596 | -0.159899 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 926.8118 | 0.0000 | 39 | 2 | -1.923894 | 0.007166 | -1.931060 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.931060 |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 2 | 308.9373 | 0.0000 | 39 | 2 | -1.923894 | 0.021497 | -1.945391 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 2317.0296 | 0.0000 | 39 | 2 | -1.923894 | 0.002866 | -1.926761 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 4 | 442.3397 | 0.0000 | 48 | 4 | -1.385221 | 0.009866 | -1.395086 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -1.395086 |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 4 | 147.4466 | 0.0000 | 48 | 4 | -1.385221 | 0.029597 | -1.414818 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 4 | 1105.8492 | 0.0000 | 48 | 4 | -1.385221 | 0.003946 | -1.389167 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2 | 458.9821 | 0.0000 | 4 | 2 | -4.342466 | 0.017554 | -4.360020 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -4.360020 |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 2 | 152.9940 | 0.0000 | 4 | 2 | -4.342466 | 0.052662 | -4.395128 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1147.4553 | 0.0000 | 4 | 2 | -4.342466 | 0.007022 | -4.349487 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | — |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 4 | 442.3397 | 0.0000 | 48 | 4 | -1.385221 | 0.009866 | -1.395086 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -1.395086 |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 4 | 147.4466 | 0.0000 | 48 | 4 | -1.385221 | 0.029597 | -1.414818 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 4 | 1105.8492 | 0.0000 | 48 | 4 | -1.385221 | 0.003946 | -1.389167 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 458.9821 | 0.0000 | 4 | 2 | -4.342466 | 0.017554 | -4.360020 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -4.360020 |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 2 | 152.9940 | 0.0000 | 4 | 2 | -4.342466 | 0.052662 | -4.395128 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1147.4553 | 0.0000 | 4 | 2 | -4.342466 | 0.007022 | -4.349487 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 8 | 388.7145 | 0.0000 | 213 | 7 | -0.206652 | 0.020288 | -0.226939 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -1.970656 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 8 | 129.5715 | 0.0000 | 213 | 7 | -0.206652 | 0.060863 | -0.267515 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 8 | 971.7864 | 0.0000 | 213 | 7 | -0.206652 | 0.008115 | -0.214767 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 5 | 394.1334 | 0.0000 | 241 | 5 | 0.037255 | 0.020214 | 0.017041 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.017041 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 5 | 131.3778 | 0.0000 | 241 | 5 | 0.037255 | 0.060642 | -0.023387 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 5 | 985.3336 | 0.0000 | 241 | 5 | 0.037255 | 0.008086 | 0.029170 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 3 | 227.3611 | 0.0000 | 23 | 3 | -2.769334 | 0.018234 | -2.787568 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -2.411389 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 3 | 75.7870 | 0.0000 | 23 | 3 | -2.769334 | 0.054702 | -2.824036 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 3 | 568.4027 | 0.0000 | 23 | 3 | -2.769334 | 0.007294 | -2.776627 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 2 | 267.2114 | 0.0000 | 12 | 2 | -5.166132 | 0.018285 | -5.184418 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -5.184418 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 2 | 89.0705 | 0.0000 | 12 | 2 | -5.166132 | 0.054856 | -5.220989 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 2 | 668.0285 | 0.0000 | 12 | 2 | -5.166132 | 0.007314 | -5.173447 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 5 | 426.3404 | 0.0000 | 190 | 4 | -0.129551 | 0.020547 | -0.150098 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -1.875185 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 5 | 142.1135 | 0.0000 | 190 | 4 | -0.129551 | 0.061641 | -0.191192 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 5 | 1065.8509 | 0.0000 | 190 | 4 | -0.129551 | 0.008219 | -0.137770 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 3 | 426.3404 | 0.0000 | 229 | 3 | 0.226058 | 0.020334 | 0.205724 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.205724 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 3 | 142.1135 | 0.0000 | 229 | 3 | 0.226058 | 0.061002 | 0.165056 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1065.8509 | 0.0000 | 229 | 3 | 0.226058 | 0.008134 | 0.217925 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 12 | 325.0741 | 0.0000 | 106 | 10 | -0.935391 | 0.010420 | -0.945811 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.876094 |
| ASSET:SUIUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 12 | 162.5371 | 0.0000 | 106 | 10 | -0.935391 | 0.020839 | -0.956230 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 12 | 812.6853 | 0.0000 | 106 | 10 | -0.935391 | 0.004168 | -0.939559 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 3 | 793.5954 | 0.0000 | 259 | 3 | -0.257605 | 0.014454 | -0.272059 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.290793 |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 3 | 396.7977 | 0.0000 | 259 | 3 | -0.257605 | 0.028907 | -0.286513 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1983.9885 | 0.0000 | 259 | 3 | -0.257605 | 0.005781 | -0.263387 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 4 | 310.0019 | 0.0000 | 38 | 4 | -1.492699 | 0.011706 | -1.504406 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -2.441694 |
| ASSET:SUIUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 4 | 155.0010 | 0.0000 | 38 | 4 | -1.492699 | 0.023413 | -1.516112 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 4 | 775.0048 | 0.0000 | 38 | 4 | -1.492699 | 0.004683 | -1.497382 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1 | 793.5954 | 0.0000 | 14 | 1 | -1.271389 | 0.009976 | -1.281366 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.281366 |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 1 | 396.7977 | 0.0000 | 14 | 1 | -1.271389 | 0.019953 | -1.291342 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1 | 1983.9885 | 0.0000 | 14 | 1 | -1.271389 | 0.003991 | -1.275380 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 8 | 345.2730 | 0.0000 | 68 | 6 | -0.608568 | 0.009583 | -0.618150 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.533022 |
| ASSET:SUIUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 8 | 172.6365 | 0.0000 | 68 | 6 | -0.608568 | 0.019165 | -0.627733 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 8 | 863.1825 | 0.0000 | 68 | 6 | -0.608568 | 0.003833 | -0.612401 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 1096.8280 | 0.0000 | 245 | 2 | -0.064873 | 0.014613 | -0.079486 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.093382 |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 2 | 548.4140 | 0.0000 | 245 | 2 | -0.064873 | 0.029225 | -0.094098 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 2742.0701 | 0.0000 | 245 | 2 | -0.064873 | 0.005845 | -0.070718 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 19 | 251.5346 | 0.0000 | 159 | 18 | -0.435040 | 0.015348 | -0.450388 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.450388 |
| ASSET:LTCUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 19 | 125.7673 | 0.0000 | 159 | 18 | -0.435040 | 0.030696 | -0.465736 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 19 | 628.8365 | 0.0000 | 159 | 18 | -0.435040 | 0.006139 | -0.441179 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 13 | 353.0904 | 0.0000 | 171 | 12 | -0.792210 | 0.015674 | -0.807885 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.807885 |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 13 | 176.5452 | 0.0000 | 171 | 12 | -0.792210 | 0.031348 | -0.823559 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 13 | 882.7261 | 0.0000 | 171 | 12 | -0.792210 | 0.006270 | -0.798480 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 12 | 299.5105 | 0.0000 | 122 | 11 | -0.411367 | 0.014960 | -0.426328 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.426328 |
| ASSET:LTCUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 12 | 149.7553 | 0.0000 | 122 | 11 | -0.411367 | 0.029920 | -0.441288 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 12 | 748.7763 | 0.0000 | 122 | 11 | -0.411367 | 0.005984 | -0.417352 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 7 | 512.0516 | 0.0000 | 74 | 7 | -0.278333 | 0.014060 | -0.292393 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.292393 |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 7 | 256.0258 | 0.0000 | 74 | 7 | -0.278333 | 0.028121 | -0.306454 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 7 | 1280.1289 | 0.0000 | 74 | 7 | -0.278333 | 0.005624 | -0.283957 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 7 | 227.7495 | 0.0000 | 37 | 8 | -0.783867 | 0.020345 | -0.804212 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.804212 |
| ASSET:LTCUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 7 | 113.8748 | 0.0000 | 37 | 8 | -0.783867 | 0.040691 | -0.824558 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 7 | 569.3738 | 0.0000 | 37 | 8 | -0.783867 | 0.008138 | -0.792005 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 6 | 299.9704 | 0.0000 | 97 | 5 | -1.067489 | 0.016827 | -1.084316 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.084316 |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 6 | 149.9852 | 0.0000 | 97 | 5 | -1.067489 | 0.033655 | -1.101143 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 6 | 749.9261 | 0.0000 | 97 | 5 | -1.067489 | 0.006731 | -1.074220 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 15 | 208.1526 | 0.0000 | 222 | 15 | 0.526449 | 0.014000 | 0.512448 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.512448 |
| ASSET:XMRUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 15 | 104.0763 | 0.0000 | 222 | 15 | 0.526449 | 0.028001 | 0.498448 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 15 | 520.3816 | 0.0000 | 222 | 15 | 0.526449 | 0.005600 | 0.520849 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 3 | 512.4439 | 0.0000 | 181 | 3 | 1.248462 | 0.013929 | 1.234533 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 1.234533 |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 3 | 256.2219 | 0.0000 | 181 | 3 | 1.248462 | 0.027858 | 1.220604 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1281.1097 | 0.0000 | 181 | 3 | 1.248462 | 0.005572 | 1.242890 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 10 | 234.4385 | 0.0000 | 164 | 10 | 1.246725 | 0.013593 | 1.233131 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 1.233131 |
| ASSET:XMRUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 10 | 117.2193 | 0.0000 | 164 | 10 | 1.246725 | 0.027187 | 1.219538 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 10 | 586.0963 | 0.0000 | 164 | 10 | 1.246725 | 0.005437 | 1.241287 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 2 | 551.0718 | 0.0000 | 153 | 2 | 1.473781 | 0.013278 | 1.460503 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 1.460503 |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 2 | 275.5359 | 0.0000 | 153 | 2 | 1.473781 | 0.026556 | 1.447225 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1377.6795 | 0.0000 | 153 | 2 | 1.473781 | 0.005311 | 1.468470 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 5 | 168.5554 | 0.0000 | 58 | 6 | -2.505912 | 0.018073 | -2.523985 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -2.523985 |
| ASSET:XMRUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 5 | 84.2777 | 0.0000 | 58 | 6 | -2.505912 | 0.036146 | -2.542058 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 5 | 421.3885 | 0.0000 | 58 | 6 | -2.505912 | 0.007229 | -2.513141 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1 | 396.1106 | 0.0000 | 28 | 2 | -6.200167 | 0.019275 | -6.219442 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -6.219442 |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 1 | 198.0553 | 0.0000 | 28 | 2 | -6.200167 | 0.038551 | -6.238718 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1 | 990.2764 | 0.0000 | 28 | 2 | -6.200167 | 0.007710 | -6.207877 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 23 | 213.2820 | 0.0000 | 375 | 23 | 0.225943 | 0.026500 | 0.199443 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.275718 |
| ASSET:BNBUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 23 | 106.6410 | 0.0000 | 375 | 23 | 0.225943 | 0.053000 | 0.172943 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 23 | 533.2051 | 0.0000 | 375 | 23 | 0.225943 | 0.010600 | 0.215343 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 8 | 230.3971 | 0.0000 | 251 | 8 | 0.129954 | 0.024237 | 0.105717 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.109344 |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 8 | 115.1986 | 0.0000 | 251 | 8 | 0.129954 | 0.048474 | 0.081480 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 8 | 575.9928 | 0.0000 | 251 | 8 | 0.129954 | 0.009695 | 0.120259 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 14 | 269.9284 | 0.0000 | 242 | 14 | 0.938301 | 0.024407 | 0.913894 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.702299 |
| ASSET:BNBUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 14 | 134.9642 | 0.0000 | 242 | 14 | 0.938301 | 0.048813 | 0.889487 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 14 | 674.8211 | 0.0000 | 242 | 14 | 0.938301 | 0.009763 | 0.928538 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 4 | 473.0999 | 0.0000 | 159 | 4 | 0.143950 | 0.020166 | 0.123784 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.123784 |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 4 | 236.5499 | 0.0000 | 159 | 4 | 0.143950 | 0.040332 | 0.103618 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 4 | 1182.7497 | 0.0000 | 159 | 4 | 0.143950 | 0.008066 | 0.135884 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 9 | 133.7953 | 0.0000 | 133 | 10 | -0.334433 | 0.028595 | -0.363028 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.228854 |
| ASSET:BNBUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 9 | 66.8976 | 0.0000 | 133 | 10 | -0.334433 | 0.057191 | -0.391624 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 9 | 334.4882 | 0.0000 | 133 | 10 | -0.334433 | 0.011438 | -0.345871 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 4 | 204.8700 | 0.0000 | 92 | 4 | 0.083217 | 0.030296 | 0.052921 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.062870 |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 4 | 102.4350 | 0.0000 | 92 | 4 | 0.083217 | 0.060591 | 0.022626 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 4 | 512.1751 | 0.0000 | 92 | 4 | 0.083217 | 0.012118 | 0.071099 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 13 | 319.7953 | 0.0000 | 539 | 12 | 0.018152 | 0.013384 | 0.004769 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.004769 |
| ASSET:UNIUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 13 | 159.8977 | 0.0000 | 539 | 12 | 0.018152 | 0.026767 | -0.008615 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 13 | 799.4883 | 0.0000 | 539 | 12 | 0.018152 | 0.005353 | 0.012799 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 9 | 405.3983 | 0.0000 | 504 | 9 | 0.031154 | 0.012763 | 0.018391 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.018391 |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 9 | 202.6991 | 0.0000 | 504 | 9 | 0.031154 | 0.025527 | 0.005627 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 9 | 1013.4956 | 0.0000 | 504 | 9 | 0.031154 | 0.005105 | 0.026049 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 9 | 332.8878 | 0.0000 | 214 | 8 | -0.250838 | 0.018182 | -0.269020 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.269020 |
| ASSET:UNIUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 9 | 166.4439 | 0.0000 | 214 | 8 | -0.250838 | 0.036364 | -0.287201 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 9 | 832.2196 | 0.0000 | 214 | 8 | -0.250838 | 0.007273 | -0.258111 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 7 | 621.9165 | 0.0000 | 183 | 7 | -0.486286 | 0.017199 | -0.503485 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.503485 |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 7 | 310.9583 | 0.0000 | 183 | 7 | -0.486286 | 0.034398 | -0.520684 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 7 | 1554.7913 | 0.0000 | 183 | 7 | -0.486286 | 0.006880 | -0.493166 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 4 | 300.8888 | 0.0000 | 325 | 5 | 0.163272 | 0.011808 | 0.151464 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | 0.151464 |
| ASSET:UNIUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 4 | 150.4444 | 0.0000 | 325 | 5 | 0.163272 | 0.023617 | 0.139656 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 4 | 752.2220 | 0.0000 | 325 | 5 | 0.163272 | 0.004723 | 0.158549 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 345.2699 | 0.0000 | 321 | 3 | 0.228712 | 0.011808 | 0.216903 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.216903 |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 2 | 172.6350 | 0.0000 | 321 | 3 | 0.228712 | 0.023617 | 0.205095 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 863.1748 | 0.0000 | 321 | 3 | 0.228712 | 0.004723 | 0.223988 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 7 | 669.9994 | 0.0000 | 175 | 7 | -0.698291 | 0.010560 | -0.708851 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.667209 |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 7 | 223.3331 | 0.0000 | 175 | 7 | -0.698291 | 0.031680 | -0.729970 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 7 | 1674.9985 | 0.0000 | 175 | 7 | -0.698291 | 0.004224 | -0.702515 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 7 | 669.9994 | 0.0000 | 175 | 7 | -0.698291 | 0.010560 | -0.708851 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.708851 |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 7 | 223.3331 | 0.0000 | 175 | 7 | -0.698291 | 0.031680 | -0.729970 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 7 | 1674.9985 | 0.0000 | 175 | 7 | -0.698291 | 0.004224 | -0.702515 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 3 | 669.9994 | 0.0000 | 12 | 3 | -0.311933 | 0.009803 | -0.321736 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -2.754935 |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 3 | 223.3331 | 0.0000 | 12 | 3 | -0.311933 | 0.029410 | -0.341343 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 3 | 1674.9985 | 0.0000 | 12 | 3 | -0.311933 | 0.003921 | -0.315854 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 3 | 669.9994 | 0.0000 | 12 | 3 | -0.311933 | 0.009803 | -0.321736 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.321736 |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 3 | 223.3331 | 0.0000 | 12 | 3 | -0.311933 | 0.029410 | -0.341343 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1674.9985 | 0.0000 | 12 | 3 | -0.311933 | 0.003921 | -0.315854 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 4 | 993.7426 | 0.0000 | 163 | 4 | -0.698291 | 0.011076 | -0.709367 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.489583 |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 4 | 331.2475 | 0.0000 | 163 | 4 | -0.698291 | 0.033229 | -0.731520 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 4 | 2484.3566 | 0.0000 | 163 | 4 | -0.698291 | 0.004431 | -0.702721 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 4 | 993.7426 | 0.0000 | 163 | 4 | -0.698291 | 0.011076 | -0.709367 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.709367 |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 4 | 331.2475 | 0.0000 | 163 | 4 | -0.698291 | 0.033229 | -0.731520 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 4 | 2484.3566 | 0.0000 | 163 | 4 | -0.698291 | 0.004431 | -0.702721 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 17 | 302.4538 | 0.0000 | 292 | 14 | -0.072243 | 0.014787 | -0.087030 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.087030 |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | charter | 20.0 | 20.0 | 17 | 151.2269 | 0.0000 | 292 | 14 | -0.072243 | 0.029574 | -0.101817 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 17 | 756.1345 | 0.0000 | 292 | 14 | -0.072243 | 0.005915 | -0.078158 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 10 | 386.7580 | 0.0000 | 293 | 9 | -0.687316 | 0.012978 | -0.700294 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.700294 |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | charter | 20.0 | 20.0 | 10 | 193.3790 | 0.0000 | 293 | 9 | -0.687316 | 0.025956 | -0.713272 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 10 | 966.8950 | 0.0000 | 293 | 9 | -0.687316 | 0.005191 | -0.692507 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 11 | 318.5276 | 0.0000 | 180 | 9 | -0.088070 | 0.014676 | -0.102746 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.102746 |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | charter | 20.0 | 20.0 | 11 | 159.2638 | 0.0000 | 180 | 9 | -0.088070 | 0.029352 | -0.117422 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 11 | 796.3191 | 0.0000 | 180 | 9 | -0.088070 | 0.005870 | -0.093941 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 7 | 385.0591 | 0.0000 | 171 | 6 | -1.078556 | 0.012263 | -1.090819 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -1.090819 |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | charter | 20.0 | 20.0 | 7 | 192.5295 | 0.0000 | 171 | 6 | -1.078556 | 0.024526 | -1.103082 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 7 | 962.6477 | 0.0000 | 171 | 6 | -1.078556 | 0.004905 | -1.083461 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 6 | 283.8088 | 0.0000 | 112 | 5 | -0.039932 | 0.014987 | -0.054919 | — | — | FAIL (provisional, n<30) | tuning | FAIL (provisional, n<30) | -0.054919 |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | charter | 20.0 | 20.0 | 6 | 141.9044 | 0.0000 | 112 | 5 | -0.039932 | 0.029974 | -0.069906 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 6 | 709.5220 | 0.0000 | 112 | 5 | -0.039932 | 0.005995 | -0.045927 | — | — | FAIL (provisional, n<30) | tuning | — | — |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 3 | 656.9948 | 0.0000 | 122 | 3 | 0.115558 | 0.014407 | 0.101151 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 0.101151 |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | charter | 20.0 | 20.0 | 3 | 328.4974 | 0.0000 | 122 | 3 | 0.115558 | 0.028814 | 0.086744 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1642.4870 | 0.0000 | 122 | 3 | 0.115558 | 0.005763 | 0.109795 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 7 | 576.4442 | 0.0000 | 204 | 7 | -0.396001 | 0.008875 | -0.404876 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.404876 |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | charter | 30.0 | 30.0 | 7 | 192.1481 | 0.0000 | 204 | 7 | -0.396001 | 0.026625 | -0.422626 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 7 | 1441.1106 | 0.0000 | 204 | 7 | -0.396001 | 0.003550 | -0.399551 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 5 | 636.0553 | 0.0000 | 209 | 5 | -0.458628 | 0.008720 | -0.467348 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.467348 |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | charter | 30.0 | 30.0 | 5 | 212.0184 | 0.0000 | 209 | 5 | -0.458628 | 0.026160 | -0.484789 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 5 | 1590.1384 | 0.0000 | 209 | 5 | -0.458628 | 0.003488 | -0.462116 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 2 | 1211.2199 | 0.0000 | 13 | 2 | 2.930182 | 0.009545 | 2.920637 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | 2.920637 |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | charter | 30.0 | 30.0 | 2 | 403.7400 | 0.0000 | 13 | 2 | 2.930182 | 0.028635 | 2.901547 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 2 | 3028.0496 | 0.0000 | 13 | 2 | 2.930182 | 0.003818 | 2.926364 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 2 | 1211.2199 | 0.0000 | 13 | 2 | 2.930182 | 0.009545 | 2.920637 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | 2.920637 |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | charter | 30.0 | 30.0 | 2 | 403.7400 | 0.0000 | 13 | 2 | 2.930182 | 0.028635 | 2.901547 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 2 | 3028.0496 | 0.0000 | 13 | 2 | 2.930182 | 0.003818 | 2.926364 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 5 | 339.1852 | 0.0000 | 191 | 6 | -0.554586 | 0.008859 | -0.563445 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | FAIL (provisional, n<30) | -0.563445 |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | charter | 30.0 | 30.0 | 5 | 113.0617 | 0.0000 | 191 | 6 | -0.554586 | 0.026577 | -0.581163 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 5 | 847.9629 | 0.0000 | 191 | 6 | -0.554586 | 0.003544 | -0.558130 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 3 | 576.4442 | 0.0000 | 196 | 4 | -0.783248 | 0.008719 | -0.791967 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.791967 |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | charter | 30.0 | 30.0 | 3 | 192.1481 | 0.0000 | 196 | 4 | -0.783248 | 0.026157 | -0.809405 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 3 | 1441.1106 | 0.0000 | 196 | 4 | -0.783248 | 0.003488 | -0.786735 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 93 | 319.5590 | 0.0000 | 1283 | 89 | -0.179500 | 0.027438 | -0.206938 | — | — | FAIL | tuning | FAIL | -0.202190 |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | charter | 14.0 | 20.0 | 93 | 181.5056 | 0.0000 | 1283 | 89 | -0.179500 | 0.038413 | -0.217913 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 93 | 798.8974 | 0.0000 | 1283 | 89 | -0.179500 | 0.010975 | -0.190475 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 53 | 413.9918 | 0.0000 | 1429 | 52 | 0.059454 | 0.024895 | 0.034558 | — | — | PASS | frozen3.0 | PASS | 0.044074 |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | charter | 14.0 | 20.0 | 53 | 227.8103 | 0.0000 | 1429 | 52 | 0.059454 | 0.034853 | 0.024600 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 53 | 1034.9794 | 0.0000 | 1429 | 52 | 0.059454 | 0.009958 | 0.049496 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 60 | 342.8890 | 0.0000 | 779 | 58 | 0.057878 | 0.024895 | 0.032983 | — | — | PASS | tuning | PASS | 0.046910 |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | charter | 14.0 | 20.0 | 60 | 190.0041 | 0.0000 | 779 | 58 | 0.057878 | 0.034853 | 0.023025 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 60 | 857.2226 | 0.0000 | 779 | 58 | 0.057878 | 0.009958 | 0.047920 | — | — | PASS | tuning | — | — |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 35 | 413.9918 | 0.0000 | 982 | 35 | 0.175796 | 0.022085 | 0.153711 | — | — | PASS | frozen3.0 | PASS | 0.153711 |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | charter | 14.0 | 20.0 | 35 | 227.8103 | 0.0000 | 982 | 35 | 0.175796 | 0.030918 | 0.144878 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 35 | 1034.9794 | 0.0000 | 982 | 35 | 0.175796 | 0.008834 | 0.166962 | — | — | PASS | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 33 | 276.2612 | 0.0000 | 504 | 35 | -0.655558 | 0.031950 | -0.687508 | FAIL | FAIL | — | tuning | FAIL | -0.694473 |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | charter | 14.0 | 20.0 | 33 | 149.7011 | 0.0000 | 504 | 35 | -0.655558 | 0.044730 | -0.700288 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 33 | 690.6531 | 0.0000 | 504 | 35 | -0.655558 | 0.012780 | -0.668338 | — | — | FAIL | tuning | — | — |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 18 | 459.3333 | 0.0000 | 447 | 21 | -0.461499 | 0.031150 | -0.492649 | — | — | FAIL (provisional, n<30) | frozen3.0 | FAIL (provisional, n<30) | -0.436030 |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | charter | 14.0 | 20.0 | 18 | 268.0081 | 0.0000 | 447 | 21 | -0.461499 | 0.043611 | -0.505109 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 18 | 1148.3334 | 0.0000 | 447 | 21 | -0.461499 | 0.012460 | -0.473959 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | ALL | calibrated | taker | 10.0 | 10.0 | 227 | 313.0883 | 0.0000 | 3811 | 215 | -0.163792 | 0.027438 | -0.191230 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | FAIL | -0.164374 |
| POOLED:PANEL17 | 1d | ALL | calibrated | charter | 14.0 | 30.0 | 227 | 158.9704 | 0.0000 | 3811 | 215 | -0.163792 | 0.060863 | -0.224656 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | ALL | calibrated | maker | 4.0 | 4.0 | 227 | 782.7207 | 0.0000 | 3811 | 215 | -0.163792 | 0.010975 | -0.174768 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | taker | 10.0 | 10.0 | 121 | 436.8702 | 0.0000 | 3866 | 118 | -0.099069 | 0.024895 | -0.123964 | — | — | FAIL | frozen3.0 | FAIL | -0.120793 |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | charter | 14.0 | 30.0 | 121 | 206.9959 | 0.0000 | 3866 | 118 | -0.099069 | 0.060642 | -0.159711 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | maker | 4.0 | 4.0 | 121 | 1092.1755 | 0.0000 | 3866 | 118 | -0.099069 | 0.009958 | -0.109027 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | tuning | calibrated | taker | 10.0 | 10.0 | 129 | 319.7953 | 0.0000 | 1792 | 123 | 0.034811 | 0.024895 | 0.009916 | — | — | PASS | MIXED: tuning / whole-tape (fallback) | PASS | 0.049039 |
| POOLED:PANEL17 | 1d | tuning | calibrated | charter | 14.0 | 30.0 | 129 | 170.2438 | 0.0000 | 1792 | 123 | 0.034811 | 0.054702 | -0.019891 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | tuning | calibrated | maker | 4.0 | 4.0 | 129 | 799.4883 | 0.0000 | 1792 | 123 | 0.034811 | 0.009958 | 0.024853 | — | — | PASS | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | taker | 10.0 | 10.0 | 70 | 446.2454 | 0.0000 | 1773 | 69 | 0.059034 | 0.022085 | 0.036949 | — | — | PASS | frozen3.0 | PASS | 0.036949 |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | charter | 14.0 | 30.0 | 70 | 225.5717 | 0.0000 | 1773 | 69 | 0.059034 | 0.054856 | 0.004178 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | maker | 4.0 | 4.0 | 70 | 1115.6135 | 0.0000 | 1773 | 69 | 0.059034 | 0.008834 | 0.050200 | — | — | PASS | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | holdout | calibrated | taker | 10.0 | 10.0 | 98 | 297.9168 | 0.0000 | 2019 | 101 | -0.384734 | 0.031950 | -0.416684 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | FAIL | -0.422491 |
| POOLED:PANEL17 | 1d | holdout | calibrated | charter | 14.0 | 30.0 | 98 | 141.3772 | 0.0000 | 2019 | 101 | -0.384734 | 0.061641 | -0.446375 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | holdout | calibrated | maker | 4.0 | 4.0 | 98 | 744.7920 | 0.0000 | 2019 | 101 | -0.384734 | 0.012780 | -0.397514 | — | — | FAIL | MIXED: tuning / whole-tape (fallback) | — | — |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | taker | 10.0 | 10.0 | 51 | 426.3404 | 0.0000 | 2093 | 56 | -0.289595 | 0.031150 | -0.320745 | — | — | FAIL | frozen3.0 | FAIL | -0.311827 |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | charter | 14.0 | 30.0 | 51 | 192.1481 | 0.0000 | 2093 | 56 | -0.289595 | 0.061002 | -0.350597 | — | — | FAIL | frozen3.0 | — | — |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | maker | 4.0 | 4.0 | 51 | 1065.8509 | 0.0000 | 2093 | 56 | -0.289595 | 0.012460 | -0.302055 | — | — | FAIL | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 3 | 780.2605 | 0.0000 | 37 | 3 | -2.420660 | 0.009289 | -2.429949 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | ALL | calibrated | charter | 14.0 | 14.0 | 3 | 557.3290 | 0.0000 | 37 | 3 | -2.420660 | 0.013005 | -2.433665 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 3 | 1950.6513 | 0.0000 | 37 | 3 | -2.420660 | 0.003716 | -2.424376 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2 | 632.0920 | 0.0000 | 22 | 2 | -2.442318 | 0.010566 | -2.452885 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | charter | 14.0 | 14.0 | 2 | 451.4943 | 0.0000 | 22 | 2 | -2.442318 | 0.014793 | -2.457111 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1580.2301 | 0.0000 | 22 | 2 | -2.442318 | 0.004226 | -2.446545 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 3 | 780.2605 | 0.0000 | 26 | 3 | -2.133999 | 0.007693 | -2.141692 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | tuning | calibrated | charter | 14.0 | 14.0 | 3 | 557.3290 | 0.0000 | 26 | 3 | -2.133999 | 0.010770 | -2.144770 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 3 | 1950.6513 | 0.0000 | 26 | 3 | -2.133999 | 0.003077 | -2.137077 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 2 | 632.0920 | 0.0000 | 11 | 2 | 0.069226 | 0.010974 | 0.058252 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | charter | 14.0 | 14.0 | 2 | 451.4943 | 0.0000 | 11 | 2 | 0.069226 | 0.015364 | 0.053863 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 2 | 1580.2301 | 0.0000 | 11 | 2 | 0.069226 | 0.004390 | 0.064837 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.010306 | -4.665427 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | holdout | calibrated | charter | 14.0 | 14.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.014429 | -4.669549 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.004123 | -4.659243 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.010306 | -4.665427 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | charter | 14.0 | 14.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.014429 | -4.669549 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 11 | 1 | -4.655120 | 0.004123 | -4.659243 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 3 | 1531.3320 | 0.0000 | 16 | 3 | -0.052915 | 0.004520 | -0.057435 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | ALL | calibrated | charter | 14.0 | 14.0 | 3 | 1093.8086 | 0.0000 | 16 | 3 | -0.052915 | 0.006327 | -0.059242 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 3 | 3828.3300 | 0.0000 | 16 | 3 | -0.052915 | 0.001808 | -0.054723 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 3 | 1531.3320 | 0.0000 | 16 | 3 | -0.052915 | 0.004520 | -0.057435 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | charter | 14.0 | 14.0 | 3 | 1093.8086 | 0.0000 | 16 | 3 | -0.052915 | 0.006327 | -0.059242 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 3 | 3828.3300 | 0.0000 | 16 | 3 | -0.052915 | 0.001808 | -0.054723 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 1 | 1181.3094 | 0.0000 | 1 | 1 | -1.653686 | 0.004084 | -1.657770 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | tuning | calibrated | charter | 14.0 | 14.0 | 1 | 843.7924 | 0.0000 | 1 | 1 | -1.653686 | 0.005718 | -1.659404 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 1 | 2953.2734 | 0.0000 | 1 | 1 | -1.653686 | 0.001634 | -1.655319 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1 | 1181.3094 | 0.0000 | 1 | 1 | -1.653686 | 0.004084 | -1.657770 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | charter | 14.0 | 14.0 | 1 | 843.7924 | 0.0000 | 1 | 1 | -1.653686 | 0.005718 | -1.659404 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1 | 2953.2734 | 0.0000 | 1 | 1 | -1.653686 | 0.001634 | -1.655319 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 2 | 1651.9408 | 0.0000 | 15 | 2 | 0.039693 | 0.004727 | 0.034965 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | holdout | calibrated | charter | 14.0 | 14.0 | 2 | 1179.9577 | 0.0000 | 15 | 2 | 0.039693 | 0.006618 | 0.033075 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 2 | 4129.8521 | 0.0000 | 15 | 2 | 0.039693 | 0.001891 | 0.037802 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 2 | 1651.9408 | 0.0000 | 15 | 2 | 0.039693 | 0.004727 | 0.034965 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | charter | 14.0 | 14.0 | 2 | 1179.9577 | 0.0000 | 15 | 2 | 0.039693 | 0.006618 | 0.033075 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 2 | 4129.8521 | 0.0000 | 15 | 2 | 0.039693 | 0.001891 | 0.037802 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 2 | 909.9101 | 0.0000 | 11 | 2 | 2.945774 | 0.007271 | 2.938503 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | ALL | calibrated | charter | 20.0 | 20.0 | 2 | 454.9550 | 0.0000 | 11 | 2 | 2.945774 | 0.014541 | 2.931233 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 2 | 2274.7752 | 0.0000 | 11 | 2 | 2.945774 | 0.002908 | 2.942866 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 1 | 1009.0863 | 0.0000 | 9 | 1 | 3.290282 | 0.007766 | 3.282517 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | charter | 20.0 | 20.0 | 1 | 504.5432 | 0.0000 | 9 | 1 | 3.290282 | 0.015531 | 3.274751 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 1 | 2522.7158 | 0.0000 | 9 | 1 | 3.290282 | 0.003106 | 3.287176 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 1 | 810.7338 | 0.0000 | 2 | 1 | -2.666338 | 0.003749 | -2.670087 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | tuning | calibrated | charter | 20.0 | 20.0 | 1 | 405.3669 | 0.0000 | 2 | 1 | -2.666338 | 0.007498 | -2.673836 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 1 | 2026.8346 | 0.0000 | 2 | 1 | -2.666338 | 0.001500 | -2.667837 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | charter | 20.0 | 20.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 1 | 1009.0863 | 0.0000 | 9 | 1 | 3.290282 | 0.007766 | 3.282517 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | holdout | calibrated | charter | 20.0 | 20.0 | 1 | 504.5432 | 0.0000 | 9 | 1 | 3.290282 | 0.015531 | 3.274751 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 1 | 2522.7158 | 0.0000 | 9 | 1 | 3.290282 | 0.003106 | 3.287176 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1 | 1009.0863 | 0.0000 | 9 | 1 | 3.290282 | 0.007766 | 3.282517 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | charter | 20.0 | 20.0 | 1 | 504.5432 | 0.0000 | 9 | 1 | 3.290282 | 0.015531 | 3.274751 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1 | 2522.7158 | 0.0000 | 9 | 1 | 3.290282 | 0.003106 | 3.287176 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 2 | 5853.8805 | 0.0000 | 34 | 2 | -0.591916 | 0.002131 | -0.594047 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | ALL | calibrated | charter | 20.0 | 20.0 | 2 | 2926.9402 | 0.0000 | 34 | 2 | -0.591916 | 0.004262 | -0.596178 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 2 | 14634.7012 | 0.0000 | 34 | 2 | -0.591916 | 0.000852 | -0.592768 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 2 | 5853.8805 | 0.0000 | 34 | 2 | -0.591916 | 0.002131 | -0.594047 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | charter | 20.0 | 20.0 | 2 | 2926.9402 | 0.0000 | 34 | 2 | -0.591916 | 0.004262 | -0.596178 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 2 | 14634.7012 | 0.0000 | 34 | 2 | -0.591916 | 0.000852 | -0.592768 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 1 | 5550.0457 | 0.0000 | 21 | 1 | -0.697999 | 0.001900 | -0.699900 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | tuning | calibrated | charter | 20.0 | 20.0 | 1 | 2775.0228 | 0.0000 | 21 | 1 | -0.697999 | 0.003801 | -0.701800 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 1 | 13875.1142 | 0.0000 | 21 | 1 | -0.697999 | 0.000760 | -0.698759 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 1 | 5550.0457 | 0.0000 | 21 | 1 | -0.697999 | 0.001900 | -0.699900 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | charter | 20.0 | 20.0 | 1 | 2775.0228 | 0.0000 | 21 | 1 | -0.697999 | 0.003801 | -0.701800 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 1 | 13875.1142 | 0.0000 | 21 | 1 | -0.697999 | 0.000760 | -0.698759 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 1 | 6157.7153 | 0.0000 | 13 | 1 | 1.858366 | 0.003328 | 1.855038 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | holdout | calibrated | charter | 20.0 | 20.0 | 1 | 3078.8576 | 0.0000 | 13 | 1 | 1.858366 | 0.006655 | 1.851710 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 1 | 15394.2882 | 0.0000 | 13 | 1 | 1.858366 | 0.001331 | 1.857035 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1 | 6157.7153 | 0.0000 | 13 | 1 | 1.858366 | 0.003328 | 1.855038 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | charter | 20.0 | 20.0 | 1 | 3078.8576 | 0.0000 | 13 | 1 | 1.858366 | 0.006655 | 1.851710 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1 | 15394.2882 | 0.0000 | 13 | 1 | 1.858366 | 0.001331 | 1.857035 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 3 | 877.5130 | 0.0000 | 12 | 1 | -1.279600 | 0.002731 | -1.282331 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | ALL | calibrated | charter | 20.0 | 20.0 | 3 | 438.7565 | 0.0000 | 12 | 1 | -1.279600 | 0.005462 | -1.285063 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 3 | 2193.7824 | 0.0000 | 12 | 1 | -1.279600 | 0.001092 | -1.280693 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 1 | 1101.9280 | 0.0000 | 1 | 1 | 1.684312 | 0.009311 | 1.675001 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | charter | 20.0 | 20.0 | 1 | 550.9640 | 0.0000 | 1 | 1 | 1.684312 | 0.018623 | 1.665690 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 1 | 2754.8199 | 0.0000 | 1 | 1 | 1.684312 | 0.003725 | 1.680588 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 1 | 877.5130 | 0.0000 | 12 | 1 | -1.279600 | 0.002731 | -1.282331 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | tuning | calibrated | charter | 20.0 | 20.0 | 1 | 438.7565 | 0.0000 | 12 | 1 | -1.279600 | 0.005462 | -1.285063 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 1 | 2193.7824 | 0.0000 | 12 | 1 | -1.279600 | 0.001092 | -1.280693 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | charter | 20.0 | 20.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 0 | — | — | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 2 | 1177.6344 | 0.0000 | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | holdout | calibrated | charter | 20.0 | 20.0 | 2 | 588.8172 | 0.0000 | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 2 | 2944.0859 | 0.0000 | 0 | 0 | — | — | — | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 1 | 1101.9280 | 0.0000 | 1 | 1 | 1.684312 | 0.009311 | 1.675001 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | charter | 20.0 | 20.0 | 1 | 550.9640 | 0.0000 | 1 | 1 | 1.684312 | 0.018623 | 1.665690 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 1 | 2754.8199 | 0.0000 | 1 | 1 | 1.684312 | 0.003725 | 1.680588 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | taker | 10.0 | 10.0 | 13 | 1009.0863 | 0.0000 | 110 | 11 | -0.696777 | 0.009289 | -0.706066 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | charter | 14.0 | 20.0 | 13 | 666.4396 | 0.0000 | 110 | 11 | -0.696777 | 0.014541 | -0.711318 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | maker | 4.0 | 4.0 | 13 | 2522.7158 | 0.0000 | 110 | 11 | -0.696777 | 0.003716 | -0.700492 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | taker | 10.0 | 10.0 | 9 | 1181.3094 | 0.0000 | 82 | 9 | -0.229337 | 0.010566 | -0.239904 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | charter | 14.0 | 20.0 | 9 | 843.7924 | 0.0000 | 82 | 9 | -0.229337 | 0.018623 | -0.247960 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | maker | 4.0 | 4.0 | 9 | 2953.2734 | 0.0000 | 82 | 9 | -0.229337 | 0.004226 | -0.233564 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | taker | 10.0 | 10.0 | 7 | 877.5130 | 0.0000 | 62 | 7 | -1.145453 | 0.007693 | -1.153146 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | charter | 14.0 | 20.0 | 7 | 557.3290 | 0.0000 | 62 | 7 | -1.145453 | 0.010770 | -1.156223 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | maker | 4.0 | 4.0 | 7 | 2193.7824 | 0.0000 | 62 | 7 | -1.145453 | 0.003077 | -1.148530 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | taker | 10.0 | 10.0 | 4 | 980.7850 | 0.0000 | 33 | 4 | -0.685288 | 0.010974 | -0.696262 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | charter | 14.0 | 20.0 | 4 | 700.5607 | 0.0000 | 33 | 4 | -0.685288 | 0.015364 | -0.700652 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | maker | 4.0 | 4.0 | 4 | 2451.9624 | 0.0000 | 33 | 4 | -0.685288 | 0.004390 | -0.689678 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | taker | 10.0 | 10.0 | 6 | 1626.0737 | 0.0000 | 48 | 5 | 1.133907 | 0.010306 | 1.123600 | FAIL (provisional, n<30) | FAIL (provisional, n<30) | — | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | charter | 14.0 | 20.0 | 6 | 977.1081 | 0.0000 | 48 | 5 | 1.133907 | 0.015531 | 1.118376 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | maker | 4.0 | 4.0 | 6 | 4065.1841 | 0.0000 | 48 | 5 | 1.133907 | 0.004123 | 1.129784 | — | — | FAIL (provisional, n<30) | whole-tape (fallback) | — | — |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | taker | 10.0 | 10.0 | 5 | 1531.3320 | 0.0000 | 49 | 6 | 1.184668 | 0.010306 | 1.174361 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | charter | 14.0 | 20.0 | 5 | 1093.8086 | 0.0000 | 49 | 6 | 1.184668 | 0.018623 | 1.166045 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | maker | 4.0 | 4.0 | 5 | 3828.3300 | 0.0000 | 49 | 6 | 1.184668 | 0.004123 | 1.180545 | — | — | FAIL (provisional, n<30) | frozen3.0 | — | — |

### The height ÷ round-trip toll DISTRIBUTION per row, WHOLE (1458 rows): the census's deciles d1..d9 of the per-range ratio, the median height and toll in ATR [contract R2: 'height ÷ round-trip toll (distribution)']

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

| panel | lens | era | scale_kind | toll | n_ranges | toll_atr_median | height_atr_median | share_ratio_lt_1 | ratio_d1 | ratio_d2 | ratio_d3 | ratio_d4 | ratio_d5 | ratio_d6 | ratio_d7 | ratio_d8 | ratio_d9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ASSET:BTCUSDT | 5m | ALL | calibrated | taker | 6468 | 0.481612 | 3.2177 | 0.0042 | 2.7758 | 3.8118 | 4.6861 | 5.6373 | 6.7175 | 8.1346 | 9.9712 | 12.6075 | 17.3700 |
| ASSET:BTCUSDT | 5m | ALL | calibrated | charter | 6468 | 0.674256 | 3.2177 | 0.0130 | 1.9827 | 2.7227 | 3.3472 | 4.0266 | 4.7982 | 5.8104 | 7.1223 | 9.0053 | 12.4072 |
| ASSET:BTCUSDT | 5m | ALL | calibrated | maker | 6468 | 0.192645 | 3.2177 | 0.0003 | 6.9394 | 9.5296 | 11.7153 | 14.0933 | 16.7937 | 20.3364 | 24.9280 | 31.5187 | 43.4251 |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | taker | 2835 | 0.504374 | 6.3306 | 0.0004 | 5.6563 | 7.4148 | 9.1435 | 10.9629 | 13.0675 | 15.4381 | 18.9928 | 24.2854 | 32.6426 |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | charter | 2835 | 0.706124 | 6.3306 | 0.0007 | 4.0402 | 5.2963 | 6.5311 | 7.8307 | 9.3340 | 11.0272 | 13.5663 | 17.3467 | 23.3162 |
| ASSET:BTCUSDT | 5m | ALL | frozen3.0 | maker | 2835 | 0.201750 | 6.3306 | 0.0000 | 14.1407 | 18.5371 | 22.8587 | 27.4073 | 32.6689 | 38.5952 | 47.4820 | 60.7135 | 81.6066 |
| ASSET:BTCUSDT | 5m | tuning | calibrated | taker | 4067 | 0.419938 | 3.1456 | 0.0037 | 3.0437 | 4.2446 | 5.2197 | 6.2813 | 7.5475 | 9.1822 | 10.9927 | 14.0020 | 19.8084 |
| ASSET:BTCUSDT | 5m | tuning | calibrated | charter | 4067 | 0.587913 | 3.1456 | 0.0101 | 2.1741 | 3.0319 | 3.7284 | 4.4866 | 5.3911 | 6.5587 | 7.8519 | 10.0014 | 14.1489 |
| ASSET:BTCUSDT | 5m | tuning | calibrated | maker | 4067 | 0.167975 | 3.1456 | 0.0000 | 7.6092 | 10.6116 | 13.0493 | 15.7032 | 18.8687 | 22.9555 | 27.4817 | 35.0050 | 49.5211 |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | taker | 1839 | 0.445624 | 6.2350 | 0.0000 | 6.0298 | 8.0662 | 9.8989 | 12.0773 | 14.5918 | 17.4185 | 21.1813 | 27.2299 | 36.1712 |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | charter | 1839 | 0.623874 | 6.2350 | 0.0005 | 4.3070 | 5.7616 | 7.0706 | 8.6266 | 10.4227 | 12.4418 | 15.1295 | 19.4499 | 25.8366 |
| ASSET:BTCUSDT | 5m | tuning | frozen3.0 | maker | 1839 | 0.178250 | 6.2350 | 0.0000 | 15.0746 | 20.1656 | 24.7472 | 30.1933 | 36.4794 | 43.5463 | 52.9533 | 68.0746 | 90.4280 |
| ASSET:BTCUSDT | 5m | holdout | calibrated | taker | 2401 | 0.607396 | 3.3450 | 0.0050 | 2.4886 | 3.2908 | 4.0094 | 4.7481 | 5.6325 | 6.6061 | 8.0183 | 10.2105 | 13.4234 |
| ASSET:BTCUSDT | 5m | holdout | calibrated | charter | 2401 | 0.850355 | 3.3450 | 0.0179 | 1.7776 | 2.3505 | 2.8639 | 3.3915 | 4.0232 | 4.7186 | 5.7273 | 7.2932 | 9.5881 |
| ASSET:BTCUSDT | 5m | holdout | calibrated | maker | 2401 | 0.242959 | 3.3450 | 0.0008 | 6.2214 | 8.2269 | 10.0235 | 11.8703 | 14.0812 | 16.5152 | 20.0457 | 25.5261 | 33.5585 |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | taker | 996 | 0.617987 | 6.5301 | 0.0010 | 5.2695 | 6.6616 | 8.0702 | 9.5228 | 11.2301 | 12.7760 | 15.1248 | 18.7873 | 25.3106 |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | charter | 996 | 0.865182 | 6.5301 | 0.0010 | 3.7639 | 4.7583 | 5.7644 | 6.8020 | 8.0215 | 9.1257 | 10.8034 | 13.4195 | 18.0790 |
| ASSET:BTCUSDT | 5m | holdout | frozen3.0 | maker | 996 | 0.247195 | 6.5301 | 0.0000 | 13.1736 | 16.6539 | 20.1754 | 23.8069 | 28.0753 | 31.9399 | 37.8119 | 46.9682 | 63.2765 |
| ASSET:ETHUSDT | 5m | ALL | calibrated | taker | 6092 | 0.347808 | 3.1968 | 0.0039 | 3.9939 | 5.3682 | 6.5839 | 7.8927 | 9.4751 | 11.2870 | 13.5390 | 17.1819 | 23.8174 |
| ASSET:ETHUSDT | 5m | ALL | calibrated | charter | 6092 | 0.486931 | 3.1968 | 0.0072 | 2.8528 | 3.8344 | 4.7028 | 5.6377 | 6.7679 | 8.0621 | 9.6707 | 12.2728 | 17.0125 |
| ASSET:ETHUSDT | 5m | ALL | calibrated | maker | 6092 | 0.139123 | 3.1968 | 0.0003 | 9.9848 | 13.4205 | 16.4598 | 19.7318 | 23.6876 | 28.2174 | 33.8475 | 42.9548 | 59.5436 |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | taker | 2822 | 0.365520 | 6.2571 | 0.0000 | 7.5463 | 10.2499 | 12.5696 | 14.9137 | 17.9021 | 21.2699 | 25.3713 | 31.0187 | 42.4173 |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | charter | 2822 | 0.511728 | 6.2571 | 0.0000 | 5.3902 | 7.3213 | 8.9783 | 10.6526 | 12.7872 | 15.1928 | 18.1224 | 22.1562 | 30.2981 |
| ASSET:ETHUSDT | 5m | ALL | frozen3.0 | maker | 2822 | 0.146208 | 6.2571 | 0.0000 | 18.8658 | 25.6247 | 31.4241 | 37.2842 | 44.7553 | 53.1748 | 63.4282 | 77.5468 | 106.0432 |
| ASSET:ETHUSDT | 5m | tuning | calibrated | taker | 3844 | 0.320363 | 3.1884 | 0.0049 | 4.1149 | 5.6895 | 6.9791 | 8.3922 | 10.0665 | 12.0823 | 14.5169 | 18.6570 | 25.7559 |
| ASSET:ETHUSDT | 5m | tuning | calibrated | charter | 3844 | 0.448508 | 3.1884 | 0.0078 | 2.9392 | 4.0639 | 4.9850 | 5.9944 | 7.1904 | 8.6302 | 10.3692 | 13.3264 | 18.3971 |
| ASSET:ETHUSDT | 5m | tuning | calibrated | maker | 3844 | 0.128145 | 3.1884 | 0.0005 | 10.2873 | 14.2237 | 17.4476 | 20.9804 | 25.1664 | 30.2058 | 36.2923 | 46.6424 | 64.3897 |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | taker | 1881 | 0.344643 | 6.2156 | 0.0000 | 7.3519 | 10.0474 | 12.6877 | 15.3214 | 19.0576 | 22.3689 | 27.1120 | 33.4213 | 45.0712 |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | charter | 1881 | 0.482500 | 6.2156 | 0.0000 | 5.2513 | 7.1767 | 9.0627 | 10.9439 | 13.6126 | 15.9778 | 19.3657 | 23.8724 | 32.1937 |
| ASSET:ETHUSDT | 5m | tuning | frozen3.0 | maker | 1881 | 0.137857 | 6.2156 | 0.0000 | 18.3796 | 25.1186 | 31.7193 | 38.3035 | 47.6440 | 55.9222 | 67.7801 | 83.5533 | 112.6781 |
| ASSET:ETHUSDT | 5m | holdout | calibrated | taker | 2248 | 0.394823 | 3.2095 | 0.0022 | 3.7883 | 4.9764 | 5.9477 | 7.1241 | 8.5036 | 10.1581 | 11.9810 | 14.7941 | 19.7479 |
| ASSET:ETHUSDT | 5m | holdout | calibrated | charter | 2248 | 0.552752 | 3.2095 | 0.0062 | 2.7060 | 3.5546 | 4.2484 | 5.0886 | 6.0740 | 7.2558 | 8.5579 | 10.5672 | 14.1056 |
| ASSET:ETHUSDT | 5m | holdout | calibrated | maker | 2248 | 0.157929 | 3.2095 | 0.0000 | 9.4708 | 12.4411 | 14.8693 | 17.8102 | 21.2589 | 25.3954 | 29.9526 | 36.9852 | 49.3697 |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | taker | 941 | 0.402684 | 6.3694 | 0.0000 | 7.8319 | 10.5386 | 12.2494 | 14.4727 | 16.5203 | 19.3701 | 22.5508 | 27.6773 | 34.9984 |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | charter | 941 | 0.563758 | 6.3694 | 0.0000 | 5.5942 | 7.5276 | 8.7496 | 10.3376 | 11.8002 | 13.8358 | 16.1077 | 19.7695 | 24.9989 |
| ASSET:ETHUSDT | 5m | holdout | frozen3.0 | maker | 941 | 0.161074 | 6.3694 | 0.0000 | 19.5797 | 26.3465 | 30.6236 | 36.1817 | 41.3007 | 48.4251 | 56.3770 | 69.1932 | 87.4961 |
| ASSET:SOLUSDT | 5m | ALL | calibrated | taker | 5127 | 0.249073 | 3.8503 | 0.0000 | 7.1423 | 9.3272 | 11.3814 | 13.7368 | 16.2324 | 19.1983 | 23.5261 | 28.8162 | 40.8121 |
| ASSET:SOLUSDT | 5m | ALL | calibrated | charter | 5127 | 0.498146 | 3.8503 | 0.0010 | 3.5712 | 4.6636 | 5.6907 | 6.8684 | 8.1162 | 9.5991 | 11.7630 | 14.4081 | 20.4061 |
| ASSET:SOLUSDT | 5m | ALL | calibrated | maker | 5127 | 0.099629 | 3.8503 | 0.0000 | 17.8558 | 23.3180 | 28.4536 | 34.3421 | 40.5809 | 47.9957 | 58.8152 | 72.0404 | 102.0304 |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | taker | 2444 | 0.248545 | 6.6769 | 0.0000 | 12.5522 | 16.3147 | 20.1662 | 24.1878 | 28.7014 | 33.5144 | 39.2827 | 47.9228 | 65.6573 |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | charter | 2444 | 0.497090 | 6.6769 | 0.0000 | 6.2761 | 8.1574 | 10.0831 | 12.0939 | 14.3507 | 16.7572 | 19.6414 | 23.9614 | 32.8287 |
| ASSET:SOLUSDT | 5m | ALL | frozen3.0 | maker | 2444 | 0.099418 | 6.6769 | 0.0000 | 31.3805 | 40.7868 | 50.4156 | 60.4695 | 71.7535 | 83.7859 | 98.2068 | 119.8070 | 164.1434 |
| ASSET:SOLUSDT | 5m | tuning | calibrated | taker | 3170 | 0.205496 | 3.8711 | 0.0000 | 8.7664 | 11.3753 | 13.9798 | 16.6036 | 19.4300 | 23.4675 | 27.3555 | 33.9518 | 47.6004 |
| ASSET:SOLUSDT | 5m | tuning | calibrated | charter | 3170 | 0.410993 | 3.8711 | 0.0003 | 4.3832 | 5.6877 | 6.9899 | 8.3018 | 9.7150 | 11.7337 | 13.6777 | 16.9759 | 23.8002 |
| ASSET:SOLUSDT | 5m | tuning | calibrated | maker | 3170 | 0.082199 | 3.8711 | 0.0000 | 21.9159 | 28.4383 | 34.9494 | 41.5090 | 48.5751 | 58.6687 | 68.3887 | 84.8795 | 119.0010 |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | taker | 1555 | 0.204677 | 6.6999 | 0.0000 | 15.6666 | 20.6711 | 25.4198 | 29.5558 | 33.3502 | 38.1392 | 45.2158 | 55.7921 | 76.1122 |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | charter | 1555 | 0.409354 | 6.6999 | 0.0000 | 7.8333 | 10.3356 | 12.7099 | 14.7779 | 16.6751 | 19.0696 | 22.6079 | 27.8961 | 38.0561 |
| ASSET:SOLUSDT | 5m | tuning | frozen3.0 | maker | 1555 | 0.081871 | 6.6999 | 0.0000 | 39.1664 | 51.6778 | 63.5496 | 73.8894 | 83.3754 | 95.3480 | 113.0395 | 139.4803 | 190.2806 |
| ASSET:SOLUSDT | 5m | holdout | calibrated | taker | 1957 | 0.331059 | 3.8230 | 0.0000 | 5.7836 | 7.4499 | 8.8363 | 10.3053 | 11.9421 | 14.1512 | 16.7022 | 20.0848 | 27.4520 |
| ASSET:SOLUSDT | 5m | holdout | calibrated | charter | 1957 | 0.662119 | 3.8230 | 0.0020 | 2.8918 | 3.7250 | 4.4181 | 5.1526 | 5.9710 | 7.0756 | 8.3511 | 10.0424 | 13.7260 |
| ASSET:SOLUSDT | 5m | holdout | calibrated | maker | 1957 | 0.132424 | 3.8230 | 0.0000 | 14.4590 | 18.6248 | 22.0907 | 25.7631 | 29.8552 | 35.3779 | 41.7555 | 50.2120 | 68.6300 |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | taker | 889 | 0.336074 | 6.6190 | 0.0000 | 10.3179 | 13.0239 | 15.4549 | 18.0439 | 20.3556 | 23.4538 | 28.5238 | 35.1936 | 45.5926 |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | charter | 889 | 0.672148 | 6.6190 | 0.0000 | 5.1589 | 6.5119 | 7.7275 | 9.0219 | 10.1778 | 11.7269 | 14.2619 | 17.5968 | 22.7963 |
| ASSET:SOLUSDT | 5m | holdout | frozen3.0 | maker | 889 | 0.134430 | 6.6190 | 0.0000 | 25.7947 | 32.5596 | 38.6373 | 45.1097 | 50.8890 | 58.6345 | 71.3096 | 87.9841 | 113.9816 |
| ASSET:NEARUSDT | 5m | ALL | calibrated | taker | 4860 | 0.211616 | 3.9577 | 0.0000 | 9.1438 | 11.7647 | 14.1999 | 16.5810 | 19.4397 | 22.6081 | 27.4322 | 33.4556 | 45.2715 |
| ASSET:NEARUSDT | 5m | ALL | calibrated | charter | 4860 | 0.423232 | 3.9577 | 0.0000 | 4.5719 | 5.8824 | 7.0999 | 8.2905 | 9.7199 | 11.3040 | 13.7161 | 16.7278 | 22.6357 |
| ASSET:NEARUSDT | 5m | ALL | calibrated | maker | 4860 | 0.084646 | 3.9577 | 0.0000 | 22.8595 | 29.4118 | 35.4996 | 41.4526 | 48.5993 | 56.5202 | 68.5804 | 83.6390 | 113.1787 |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | taker | 2262 | 0.209514 | 6.6735 | 0.0000 | 16.8187 | 20.4838 | 24.4971 | 28.4850 | 33.5396 | 38.7607 | 45.8306 | 55.0549 | 70.2734 |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | charter | 2262 | 0.419028 | 6.6735 | 0.0000 | 8.4094 | 10.2419 | 12.2485 | 14.2425 | 16.7698 | 19.3804 | 22.9153 | 27.5274 | 35.1367 |
| ASSET:NEARUSDT | 5m | ALL | frozen3.0 | maker | 2262 | 0.083806 | 6.6735 | 0.0000 | 42.0468 | 51.2095 | 61.2427 | 71.2125 | 83.8490 | 96.9018 | 114.5764 | 137.6372 | 175.6835 |
| ASSET:NEARUSDT | 5m | tuning | calibrated | taker | 3043 | 0.192494 | 3.9020 | 0.0000 | 9.3933 | 12.4353 | 15.1235 | 17.8179 | 20.9615 | 24.6594 | 29.7084 | 36.9340 | 48.9168 |
| ASSET:NEARUSDT | 5m | tuning | calibrated | charter | 3043 | 0.384987 | 3.9020 | 0.0000 | 4.6967 | 6.2177 | 7.5618 | 8.9090 | 10.4808 | 12.3297 | 14.8542 | 18.4670 | 24.4584 |
| ASSET:NEARUSDT | 5m | tuning | calibrated | maker | 3043 | 0.076997 | 3.9020 | 0.0000 | 23.4833 | 31.0883 | 37.8088 | 44.5448 | 52.4038 | 61.6486 | 74.2709 | 92.3349 | 122.2920 |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | taker | 1422 | 0.191067 | 6.6940 | 0.0000 | 17.0361 | 21.8756 | 26.5219 | 31.1118 | 36.2904 | 42.2836 | 49.0581 | 59.8531 | 76.5497 |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | charter | 1422 | 0.382134 | 6.6940 | 0.0000 | 8.5181 | 10.9378 | 13.2609 | 15.5559 | 18.1452 | 21.1418 | 24.5290 | 29.9265 | 38.2749 |
| ASSET:NEARUSDT | 5m | tuning | frozen3.0 | maker | 1422 | 0.076427 | 6.6940 | 0.0000 | 42.5903 | 54.6889 | 66.3047 | 77.7794 | 90.7260 | 105.7091 | 122.6452 | 149.6327 | 191.3743 |
| ASSET:NEARUSDT | 5m | holdout | calibrated | taker | 1817 | 0.240109 | 4.0289 | 0.0000 | 8.6811 | 11.0375 | 12.9052 | 15.1033 | 17.3913 | 20.2366 | 23.3219 | 28.9341 | 37.4118 |
| ASSET:NEARUSDT | 5m | holdout | calibrated | charter | 1817 | 0.480217 | 4.0289 | 0.0000 | 4.3406 | 5.5188 | 6.4526 | 7.5517 | 8.6957 | 10.1183 | 11.6609 | 14.4671 | 18.7059 |
| ASSET:NEARUSDT | 5m | holdout | calibrated | maker | 1817 | 0.096043 | 4.0289 | 0.0000 | 21.7028 | 27.5938 | 32.2631 | 37.7583 | 43.4783 | 50.5914 | 58.3047 | 72.3353 | 93.5296 |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | taker | 840 | 0.240367 | 6.6345 | 0.0000 | 16.5397 | 19.5943 | 22.2299 | 25.6158 | 29.3073 | 34.1310 | 39.1640 | 47.5069 | 58.5294 |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | charter | 840 | 0.480733 | 6.6345 | 0.0000 | 8.2699 | 9.7971 | 11.1149 | 12.8079 | 14.6536 | 17.0655 | 19.5820 | 23.7535 | 29.2647 |
| ASSET:NEARUSDT | 5m | holdout | frozen3.0 | maker | 840 | 0.096147 | 6.6345 | 0.0000 | 41.3494 | 48.9857 | 55.5746 | 64.0394 | 73.2681 | 85.3274 | 97.9099 | 118.7673 | 146.3235 |
| ASSET:ZECUSDT | 5m | ALL | calibrated | taker | 5530 | 0.239503 | 3.8693 | 0.0000 | 7.5914 | 9.8169 | 12.0457 | 14.2386 | 16.8690 | 19.8005 | 23.5356 | 29.0982 | 40.3831 |
| ASSET:ZECUSDT | 5m | ALL | calibrated | charter | 5530 | 0.479006 | 3.8693 | 0.0005 | 3.7957 | 4.9084 | 6.0228 | 7.1193 | 8.4345 | 9.9003 | 11.7678 | 14.5491 | 20.1916 |
| ASSET:ZECUSDT | 5m | ALL | calibrated | maker | 5530 | 0.095801 | 3.8693 | 0.0000 | 18.9786 | 24.5422 | 30.1142 | 35.5965 | 42.1724 | 49.5013 | 58.8390 | 72.7455 | 100.9579 |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | taker | 2676 | 0.236772 | 6.5566 | 0.0000 | 13.4499 | 17.4897 | 21.3530 | 24.9698 | 28.9017 | 33.5654 | 40.2009 | 49.1217 | 65.2570 |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | charter | 2676 | 0.473544 | 6.5566 | 0.0000 | 6.7250 | 8.7449 | 10.6765 | 12.4849 | 14.4508 | 16.7827 | 20.1004 | 24.5608 | 32.6285 |
| ASSET:ZECUSDT | 5m | ALL | frozen3.0 | maker | 2676 | 0.094709 | 6.5566 | 0.0000 | 33.6248 | 43.7243 | 53.3825 | 62.4246 | 72.2542 | 83.9135 | 100.5022 | 122.8042 | 163.1425 |
| ASSET:ZECUSDT | 5m | tuning | calibrated | taker | 3609 | 0.254321 | 3.8522 | 0.0000 | 6.9576 | 9.2367 | 11.1659 | 13.3554 | 15.9297 | 18.7776 | 22.5651 | 27.5253 | 38.0321 |
| ASSET:ZECUSDT | 5m | tuning | calibrated | charter | 3609 | 0.508642 | 3.8522 | 0.0008 | 3.4788 | 4.6183 | 5.5829 | 6.6777 | 7.9648 | 9.3888 | 11.2826 | 13.7627 | 19.0161 |
| ASSET:ZECUSDT | 5m | tuning | calibrated | maker | 3609 | 0.101728 | 3.8522 | 0.0000 | 17.3941 | 23.0916 | 27.9146 | 33.3886 | 39.8242 | 46.9440 | 56.4128 | 68.8133 | 95.0803 |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | taker | 1744 | 0.251441 | 6.6122 | 0.0000 | 12.4498 | 16.2224 | 20.2138 | 23.7585 | 27.6198 | 32.4729 | 38.5430 | 46.4884 | 60.9389 |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | charter | 1744 | 0.502881 | 6.6122 | 0.0000 | 6.2249 | 8.1112 | 10.1069 | 11.8792 | 13.8099 | 16.2364 | 19.2715 | 23.2442 | 30.4694 |
| ASSET:ZECUSDT | 5m | tuning | frozen3.0 | maker | 1744 | 0.100576 | 6.6122 | 0.0000 | 31.1244 | 40.5559 | 50.5344 | 59.3961 | 69.0496 | 81.1821 | 96.3576 | 116.2210 | 152.3472 |
| ASSET:ZECUSDT | 5m | holdout | calibrated | taker | 1921 | 0.219920 | 3.9049 | 0.0000 | 8.9935 | 11.4591 | 13.6445 | 15.9307 | 18.5806 | 21.5850 | 25.6024 | 32.0086 | 44.3148 |
| ASSET:ZECUSDT | 5m | holdout | calibrated | charter | 1921 | 0.439840 | 3.9049 | 0.0000 | 4.4968 | 5.7296 | 6.8222 | 7.9653 | 9.2903 | 10.7925 | 12.8012 | 16.0043 | 22.1574 |
| ASSET:ZECUSDT | 5m | holdout | calibrated | maker | 1921 | 0.087968 | 3.9049 | 0.0000 | 22.4838 | 28.6478 | 34.1111 | 39.8267 | 46.4516 | 53.9625 | 64.0060 | 80.0214 | 110.7869 |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | taker | 932 | 0.217710 | 6.4651 | 0.0000 | 15.9245 | 20.1496 | 23.5309 | 27.5751 | 30.7648 | 35.6524 | 43.4413 | 54.3232 | 73.3070 |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | charter | 932 | 0.435420 | 6.4651 | 0.0000 | 7.9622 | 10.0748 | 11.7654 | 13.7875 | 15.3824 | 17.8262 | 21.7207 | 27.1616 | 36.6535 |
| ASSET:ZECUSDT | 5m | holdout | frozen3.0 | maker | 932 | 0.087084 | 6.4651 | 0.0000 | 39.8112 | 50.3741 | 58.8271 | 68.9376 | 76.9119 | 89.1311 | 108.6033 | 135.8080 | 183.2675 |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | taker | 28077 | 0.292718 | 3.5948 | 0.0018 | 4.4833 | 6.3868 | 8.3078 | 10.3615 | 12.6548 | 15.4143 | 19.0355 | 24.3170 | 34.3459 |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | charter | 28077 | 0.505755 | 3.5948 | 0.0048 | 2.9461 | 4.0221 | 5.0133 | 6.0962 | 7.3256 | 8.7536 | 10.5707 | 13.3577 | 18.5669 |
| POOLED:CLASSIC5 | 5m | ALL | calibrated | maker | 28077 | 0.117087 | 3.5948 | 0.0001 | 11.2082 | 15.9670 | 20.7694 | 25.9038 | 31.6370 | 38.5356 | 47.5888 | 60.7925 | 85.8648 |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | taker | 13039 | 0.292654 | 6.4799 | 0.0001 | 8.6459 | 12.2586 | 15.5767 | 19.2477 | 23.2558 | 27.8932 | 33.5952 | 41.9766 | 57.1909 |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | charter | 13039 | 0.509054 | 6.4799 | 0.0002 | 5.5877 | 7.5945 | 9.3425 | 11.2023 | 13.3239 | 15.7343 | 18.8374 | 23.1361 | 31.0202 |
| POOLED:CLASSIC5 | 5m | ALL | frozen3.0 | maker | 13039 | 0.117062 | 6.4799 | 0.0000 | 21.6148 | 30.6465 | 38.9417 | 48.1192 | 58.1395 | 69.7329 | 83.9879 | 104.9416 | 142.9773 |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | taker | 17733 | 0.269687 | 3.5705 | 0.0019 | 4.8406 | 6.8804 | 8.9398 | 11.0411 | 13.5556 | 16.5511 | 20.5941 | 26.0933 | 37.3208 |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | charter | 17733 | 0.464764 | 3.5705 | 0.0042 | 3.1324 | 4.3064 | 5.3593 | 6.5513 | 7.8458 | 9.3939 | 11.4328 | 14.3665 | 20.1497 |
| POOLED:CLASSIC5 | 5m | tuning | calibrated | maker | 17733 | 0.107875 | 3.5705 | 0.0001 | 12.1014 | 17.2010 | 22.3495 | 27.6027 | 33.8890 | 41.3777 | 51.4851 | 65.2332 | 93.3019 |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | taker | 8441 | 0.273493 | 6.4553 | 0.0000 | 8.9513 | 12.8168 | 16.4331 | 20.5213 | 24.9345 | 29.7025 | 36.0063 | 44.6836 | 60.5510 |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | charter | 8441 | 0.472397 | 6.4553 | 0.0001 | 5.7653 | 7.8917 | 9.8661 | 11.9961 | 14.2520 | 16.9199 | 20.2317 | 24.6507 | 33.1181 |
| POOLED:CLASSIC5 | 5m | tuning | frozen3.0 | maker | 8441 | 0.109397 | 6.4553 | 0.0000 | 22.3781 | 32.0421 | 41.0826 | 51.3033 | 62.3362 | 74.2562 | 90.0158 | 111.7089 | 151.3775 |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | taker | 10344 | 0.331398 | 3.6332 | 0.0016 | 4.0158 | 5.7019 | 7.4061 | 9.2656 | 11.3326 | 13.6703 | 16.7539 | 21.0140 | 29.6303 |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | charter | 10344 | 0.581317 | 3.6332 | 0.0059 | 2.6947 | 3.6464 | 4.4884 | 5.4369 | 6.5059 | 7.7312 | 9.3238 | 11.5274 | 15.9297 |
| POOLED:CLASSIC5 | 5m | holdout | calibrated | maker | 10344 | 0.132559 | 3.6332 | 0.0002 | 10.0395 | 14.2547 | 18.5151 | 23.1640 | 28.3315 | 34.1757 | 41.8848 | 52.5351 | 74.0756 |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | taker | 4598 | 0.327645 | 6.5241 | 0.0002 | 8.1724 | 11.4753 | 14.4791 | 17.1601 | 20.6711 | 24.4529 | 29.5115 | 36.7494 | 50.2974 |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | charter | 4598 | 0.574138 | 6.5241 | 0.0002 | 5.3023 | 7.1677 | 8.5603 | 10.0851 | 11.6985 | 13.9146 | 16.4143 | 20.1413 | 26.8856 |
| POOLED:CLASSIC5 | 5m | holdout | frozen3.0 | maker | 4598 | 0.131058 | 6.5241 | 0.0000 | 20.4309 | 28.6883 | 36.1977 | 42.9002 | 51.6778 | 61.1324 | 73.7789 | 91.8734 | 125.7435 |
| ASSET:BTCUSDT | 15m | ALL | calibrated | taker | 2030 | 0.255208 | 3.5502 | 0.0000 | 5.9763 | 8.0435 | 9.8647 | 11.6743 | 13.7168 | 16.4328 | 20.4410 | 25.8032 | 36.3994 |
| ASSET:BTCUSDT | 15m | ALL | calibrated | charter | 2030 | 0.357291 | 3.5502 | 0.0010 | 4.2688 | 5.7454 | 7.0462 | 8.3388 | 9.7977 | 11.7377 | 14.6007 | 18.4309 | 25.9996 |
| ASSET:BTCUSDT | 15m | ALL | calibrated | maker | 2030 | 0.102083 | 3.5502 | 0.0000 | 14.9407 | 20.1088 | 24.6617 | 29.1858 | 34.2920 | 41.0821 | 51.1025 | 64.5081 | 90.9985 |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | taker | 918 | 0.255324 | 6.1250 | 0.0000 | 10.1266 | 14.0074 | 17.8375 | 21.2297 | 24.6447 | 29.2472 | 35.4879 | 44.3359 | 58.3948 |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | charter | 918 | 0.357454 | 6.1250 | 0.0000 | 7.2333 | 10.0053 | 12.7411 | 15.1641 | 17.6034 | 20.8908 | 25.3485 | 31.6685 | 41.7106 |
| ASSET:BTCUSDT | 15m | ALL | frozen3.0 | maker | 918 | 0.102130 | 6.1250 | 0.0000 | 25.3164 | 35.0185 | 44.5939 | 53.0742 | 61.6119 | 73.1179 | 88.7199 | 110.8397 | 145.9871 |
| ASSET:BTCUSDT | 15m | tuning | calibrated | taker | 1340 | 0.224970 | 3.4817 | 0.0000 | 6.6930 | 8.8841 | 10.8683 | 13.0077 | 15.3089 | 18.4458 | 22.4811 | 29.1473 | 39.8415 |
| ASSET:BTCUSDT | 15m | tuning | calibrated | charter | 1340 | 0.314958 | 3.4817 | 0.0000 | 4.7807 | 6.3458 | 7.7631 | 9.2912 | 10.9349 | 13.1756 | 16.0579 | 20.8195 | 28.4582 |
| ASSET:BTCUSDT | 15m | tuning | calibrated | maker | 1340 | 0.089988 | 3.4817 | 0.0000 | 16.7324 | 22.2104 | 27.1708 | 32.5192 | 38.2721 | 46.1145 | 56.2026 | 72.8684 | 99.6037 |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | taker | 611 | 0.227299 | 6.1090 | 0.0000 | 10.7106 | 14.9086 | 19.8314 | 23.3256 | 27.6654 | 32.5937 | 39.2021 | 47.9146 | 64.0666 |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | charter | 611 | 0.318219 | 6.1090 | 0.0000 | 7.6504 | 10.6490 | 14.1653 | 16.6612 | 19.7610 | 23.2812 | 28.0015 | 34.2247 | 45.7619 |
| ASSET:BTCUSDT | 15m | tuning | frozen3.0 | maker | 611 | 0.090920 | 6.1090 | 0.0000 | 26.7765 | 37.2716 | 49.5785 | 58.3141 | 69.1635 | 81.4843 | 98.0052 | 119.7864 | 160.1665 |
| ASSET:BTCUSDT | 15m | holdout | calibrated | taker | 690 | 0.333595 | 3.6767 | 0.0000 | 5.3806 | 6.8472 | 8.3731 | 9.8261 | 11.4045 | 13.1718 | 15.5943 | 20.4126 | 26.9222 |
| ASSET:BTCUSDT | 15m | holdout | calibrated | charter | 690 | 0.467033 | 3.6767 | 0.0029 | 3.8433 | 4.8908 | 5.9808 | 7.0187 | 8.1460 | 9.4084 | 11.1388 | 14.5804 | 19.2301 |
| ASSET:BTCUSDT | 15m | holdout | calibrated | maker | 690 | 0.133438 | 3.6767 | 0.0000 | 13.4515 | 17.1179 | 20.9327 | 24.5654 | 28.5111 | 32.9295 | 38.9858 | 51.0314 | 67.3054 |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | taker | 307 | 0.309788 | 6.2733 | 0.0000 | 9.3640 | 13.1537 | 15.7359 | 18.4939 | 20.7766 | 23.7561 | 29.5420 | 35.5441 | 46.7191 |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | charter | 307 | 0.433703 | 6.2733 | 0.0000 | 6.6886 | 9.3955 | 11.2399 | 13.2099 | 14.8404 | 16.9686 | 21.1014 | 25.3886 | 33.3708 |
| ASSET:BTCUSDT | 15m | holdout | frozen3.0 | maker | 307 | 0.123915 | 6.2733 | 0.0000 | 23.4099 | 32.8842 | 39.3397 | 46.2346 | 51.9415 | 59.3902 | 73.8550 | 88.8602 | 116.7977 |
| ASSET:ETHUSDT | 15m | ALL | calibrated | taker | 1627 | 0.192244 | 4.1439 | 0.0000 | 9.7608 | 13.0298 | 16.0658 | 19.0121 | 22.0801 | 25.8349 | 30.4977 | 38.3558 | 50.6266 |
| ASSET:ETHUSDT | 15m | ALL | calibrated | charter | 1627 | 0.269142 | 4.1439 | 0.0000 | 6.9720 | 9.3070 | 11.4756 | 13.5801 | 15.7715 | 18.4535 | 21.7841 | 27.3970 | 36.1619 |
| ASSET:ETHUSDT | 15m | ALL | calibrated | maker | 1627 | 0.076898 | 4.1439 | 0.0000 | 24.4020 | 32.5745 | 40.1645 | 47.5302 | 55.2003 | 64.5873 | 76.2443 | 95.8895 | 126.5666 |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | taker | 865 | 0.196392 | 6.2617 | 0.0000 | 14.8932 | 19.5532 | 23.8989 | 28.5453 | 33.5938 | 38.7816 | 47.4786 | 59.7103 | 77.6514 |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | charter | 865 | 0.274948 | 6.2617 | 0.0000 | 10.6380 | 13.9665 | 17.0706 | 20.3895 | 23.9955 | 27.7012 | 33.9133 | 42.6502 | 55.4653 |
| ASSET:ETHUSDT | 15m | ALL | frozen3.0 | maker | 865 | 0.078557 | 6.2617 | 0.0000 | 37.2329 | 48.8829 | 59.7472 | 71.3633 | 83.9844 | 96.9540 | 118.6964 | 149.2758 | 194.1285 |
| ASSET:ETHUSDT | 15m | tuning | calibrated | taker | 1109 | 0.179939 | 4.1467 | 0.0000 | 9.8735 | 13.6818 | 16.6803 | 19.9607 | 23.6379 | 27.4744 | 32.9294 | 41.4534 | 54.6968 |
| ASSET:ETHUSDT | 15m | tuning | calibrated | charter | 1109 | 0.251915 | 4.1467 | 0.0000 | 7.0525 | 9.7727 | 11.9145 | 14.2576 | 16.8842 | 19.6246 | 23.5210 | 29.6095 | 39.0691 |
| ASSET:ETHUSDT | 15m | tuning | calibrated | maker | 1109 | 0.071976 | 4.1467 | 0.0000 | 24.6838 | 34.2046 | 41.7007 | 49.9017 | 59.0948 | 68.6860 | 82.3234 | 103.6334 | 136.7420 |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | taker | 579 | 0.183135 | 6.3593 | 0.0000 | 15.0016 | 19.9961 | 24.6632 | 29.9951 | 35.2849 | 42.9354 | 51.8672 | 65.7723 | 86.6549 |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | charter | 579 | 0.256389 | 6.3593 | 0.0000 | 10.7154 | 14.2830 | 17.6166 | 21.4250 | 25.2035 | 30.6682 | 37.0480 | 46.9802 | 61.8963 |
| ASSET:ETHUSDT | 15m | tuning | frozen3.0 | maker | 579 | 0.073254 | 6.3593 | 0.0000 | 37.5039 | 49.9903 | 61.6581 | 74.9877 | 88.2123 | 107.3386 | 129.6680 | 164.4306 | 216.6371 |
| ASSET:ETHUSDT | 15m | holdout | calibrated | taker | 518 | 0.216302 | 4.1349 | 0.0000 | 9.3380 | 12.1089 | 14.8131 | 17.4865 | 19.7961 | 22.0831 | 25.8357 | 31.6461 | 41.3465 |
| ASSET:ETHUSDT | 15m | holdout | calibrated | charter | 518 | 0.302822 | 4.1349 | 0.0000 | 6.6700 | 8.6492 | 10.5808 | 12.4904 | 14.1401 | 15.7737 | 18.4540 | 22.6044 | 29.5332 |
| ASSET:ETHUSDT | 15m | holdout | calibrated | maker | 518 | 0.086521 | 4.1349 | 0.0000 | 23.3449 | 30.2723 | 37.0328 | 43.7163 | 49.4902 | 55.2079 | 64.5892 | 79.1153 | 103.3663 |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | taker | 286 | 0.216377 | 6.1378 | 0.0000 | 14.7544 | 19.0449 | 22.2793 | 26.6762 | 30.6744 | 35.5929 | 39.6908 | 48.0589 | 61.1613 |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | charter | 286 | 0.302928 | 6.1378 | 0.0000 | 10.5389 | 13.6035 | 15.9138 | 19.0544 | 21.9103 | 25.4235 | 28.3506 | 34.3278 | 43.6866 |
| ASSET:ETHUSDT | 15m | holdout | frozen3.0 | maker | 286 | 0.086551 | 6.1378 | 0.0000 | 36.8861 | 47.6124 | 55.6981 | 66.6906 | 76.6861 | 88.9822 | 99.2269 | 120.1473 | 152.9032 |
| ASSET:SOLUSDT | 15m | ALL | calibrated | taker | 1689 | 0.136057 | 3.6771 | 0.0000 | 12.9329 | 16.3863 | 19.9705 | 23.7755 | 27.7524 | 33.0741 | 39.8491 | 48.9585 | 69.3299 |
| ASSET:SOLUSDT | 15m | ALL | calibrated | charter | 1689 | 0.272113 | 3.6771 | 0.0000 | 6.4665 | 8.1931 | 9.9853 | 11.8878 | 13.8762 | 16.5371 | 19.9246 | 24.4792 | 34.6649 |
| ASSET:SOLUSDT | 15m | ALL | calibrated | maker | 1689 | 0.054423 | 3.6771 | 0.0000 | 32.3324 | 40.9657 | 49.9263 | 59.4388 | 69.3810 | 82.6853 | 99.6228 | 122.3962 | 173.3247 |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | taker | 772 | 0.138516 | 6.5853 | 0.0000 | 23.6122 | 29.7421 | 36.7417 | 42.2374 | 51.0736 | 61.2724 | 72.3066 | 90.7992 | 116.7381 |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | charter | 772 | 0.277031 | 6.5853 | 0.0000 | 11.8061 | 14.8710 | 18.3709 | 21.1187 | 25.5368 | 30.6362 | 36.1533 | 45.3996 | 58.3690 |
| ASSET:SOLUSDT | 15m | ALL | frozen3.0 | maker | 772 | 0.055406 | 6.5853 | 0.0000 | 59.0305 | 74.3552 | 91.8544 | 105.5936 | 127.6839 | 153.1810 | 180.7666 | 226.9979 | 291.8452 |
| ASSET:SOLUSDT | 15m | tuning | calibrated | taker | 1072 | 0.114362 | 3.6734 | 0.0000 | 15.5503 | 20.5295 | 24.0536 | 28.2794 | 32.8120 | 38.9648 | 45.5995 | 57.8717 | 80.8390 |
| ASSET:SOLUSDT | 15m | tuning | calibrated | charter | 1072 | 0.228724 | 3.6734 | 0.0000 | 7.7752 | 10.2648 | 12.0268 | 14.1397 | 16.4060 | 19.4824 | 22.7998 | 28.9359 | 40.4195 |
| ASSET:SOLUSDT | 15m | tuning | calibrated | maker | 1072 | 0.045745 | 3.6734 | 0.0000 | 38.8758 | 51.3238 | 60.1341 | 70.6985 | 82.0300 | 97.4120 | 113.9988 | 144.6793 | 202.0974 |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | taker | 483 | 0.115259 | 6.6936 | 0.0000 | 29.0273 | 37.9987 | 43.9664 | 52.7877 | 62.4591 | 72.2418 | 85.9615 | 103.2059 | 142.6665 |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | charter | 483 | 0.230517 | 6.6936 | 0.0000 | 14.5137 | 18.9994 | 21.9832 | 26.3938 | 31.2295 | 36.1209 | 42.9807 | 51.6030 | 71.3332 |
| ASSET:SOLUSDT | 15m | tuning | frozen3.0 | maker | 483 | 0.046103 | 6.6936 | 0.0000 | 72.5683 | 94.9968 | 109.9160 | 131.9692 | 156.1477 | 180.6045 | 214.9037 | 258.0148 | 356.6662 |
| ASSET:SOLUSDT | 15m | holdout | calibrated | taker | 617 | 0.185669 | 3.6859 | 0.0000 | 10.3702 | 13.1462 | 15.3077 | 17.6924 | 20.2294 | 24.0971 | 27.9166 | 35.8017 | 45.4002 |
| ASSET:SOLUSDT | 15m | holdout | calibrated | charter | 617 | 0.371337 | 3.6859 | 0.0000 | 5.1851 | 6.5731 | 7.6538 | 8.8462 | 10.1147 | 12.0485 | 13.9583 | 17.9009 | 22.7001 |
| ASSET:SOLUSDT | 15m | holdout | calibrated | maker | 617 | 0.074267 | 3.6859 | 0.0000 | 25.9255 | 32.8656 | 38.2692 | 44.2311 | 50.5734 | 60.2427 | 69.7915 | 89.5044 | 113.5005 |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | taker | 289 | 0.185669 | 6.4267 | 0.0000 | 17.7654 | 24.2243 | 27.1991 | 31.3128 | 36.7293 | 42.2025 | 51.0298 | 61.1599 | 80.8697 |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | charter | 289 | 0.371337 | 6.4267 | 0.0000 | 8.8827 | 12.1122 | 13.5995 | 15.6564 | 18.3647 | 21.1013 | 25.5149 | 30.5800 | 40.4349 |
| ASSET:SOLUSDT | 15m | holdout | frozen3.0 | maker | 289 | 0.074267 | 6.4267 | 0.0000 | 44.4134 | 60.5608 | 67.9977 | 78.2820 | 91.8233 | 105.5063 | 127.5745 | 152.8998 | 202.1743 |
| ASSET:NEARUSDT | 15m | ALL | calibrated | taker | 1629 | 0.116579 | 3.7570 | 0.0000 | 16.3128 | 20.9493 | 25.0219 | 29.1358 | 33.6991 | 39.6779 | 47.2514 | 57.0810 | 73.7451 |
| ASSET:NEARUSDT | 15m | ALL | calibrated | charter | 1629 | 0.233158 | 3.7570 | 0.0000 | 8.1564 | 10.4747 | 12.5109 | 14.5679 | 16.8495 | 19.8390 | 23.6257 | 28.5405 | 36.8726 |
| ASSET:NEARUSDT | 15m | ALL | calibrated | maker | 1629 | 0.046632 | 3.7570 | 0.0000 | 40.7820 | 52.3733 | 62.5547 | 72.8394 | 84.2476 | 99.1948 | 118.1285 | 142.7026 | 184.3628 |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | taker | 740 | 0.118881 | 6.4865 | 0.0000 | 30.1252 | 37.4365 | 43.9001 | 50.0663 | 57.5759 | 68.1525 | 80.6995 | 97.0390 | 126.7131 |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | charter | 740 | 0.237761 | 6.4865 | 0.0000 | 15.0626 | 18.7182 | 21.9500 | 25.0332 | 28.7879 | 34.0763 | 40.3498 | 48.5195 | 63.3566 |
| ASSET:NEARUSDT | 15m | ALL | frozen3.0 | maker | 740 | 0.047552 | 6.4865 | 0.0000 | 75.3130 | 93.5911 | 109.7502 | 125.1658 | 143.9397 | 170.3814 | 201.7488 | 242.5976 | 316.7828 |
| ASSET:NEARUSDT | 15m | tuning | calibrated | taker | 1047 | 0.107263 | 3.7473 | 0.0000 | 16.9204 | 22.0077 | 26.5844 | 30.8879 | 36.0775 | 42.5079 | 50.2068 | 61.4470 | 80.7655 |
| ASSET:NEARUSDT | 15m | tuning | calibrated | charter | 1047 | 0.214526 | 3.7473 | 0.0000 | 8.4602 | 11.0038 | 13.2922 | 15.4440 | 18.0388 | 21.2539 | 25.1034 | 30.7235 | 40.3827 |
| ASSET:NEARUSDT | 15m | tuning | calibrated | maker | 1047 | 0.042905 | 3.7473 | 0.0000 | 42.3011 | 55.0192 | 66.4610 | 77.2198 | 90.1938 | 106.2697 | 125.5171 | 153.6176 | 201.9137 |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | taker | 466 | 0.103219 | 6.4453 | 0.0000 | 30.5035 | 38.4749 | 45.9175 | 54.5353 | 63.1751 | 75.6518 | 89.4146 | 105.4986 | 141.5430 |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | charter | 466 | 0.206438 | 6.4453 | 0.0000 | 15.2518 | 19.2374 | 22.9588 | 27.2676 | 31.5876 | 37.8259 | 44.7073 | 52.7493 | 70.7715 |
| ASSET:NEARUSDT | 15m | tuning | frozen3.0 | maker | 466 | 0.041288 | 6.4453 | 0.0000 | 76.2588 | 96.1872 | 114.7938 | 136.3381 | 157.9378 | 189.1295 | 223.5364 | 263.7466 | 353.8574 |
| ASSET:NEARUSDT | 15m | holdout | calibrated | taker | 582 | 0.133178 | 3.7699 | 0.0000 | 15.4213 | 18.8483 | 22.9829 | 26.4772 | 30.0710 | 35.2363 | 41.7412 | 51.4353 | 62.1315 |
| ASSET:NEARUSDT | 15m | holdout | calibrated | charter | 582 | 0.266356 | 3.7699 | 0.0000 | 7.7107 | 9.4242 | 11.4914 | 13.2386 | 15.0355 | 17.6182 | 20.8706 | 25.7177 | 31.0658 |
| ASSET:NEARUSDT | 15m | holdout | calibrated | maker | 582 | 0.053271 | 3.7699 | 0.0000 | 38.5534 | 47.1209 | 57.4572 | 66.1931 | 75.1775 | 88.0908 | 104.3529 | 128.5883 | 155.3288 |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | taker | 274 | 0.133810 | 6.5234 | 0.0000 | 29.1640 | 35.7851 | 41.3578 | 46.1934 | 51.9813 | 58.0607 | 67.6499 | 81.8378 | 99.5608 |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | charter | 274 | 0.267619 | 6.5234 | 0.0000 | 14.5820 | 17.8925 | 20.6789 | 23.0967 | 25.9907 | 29.0303 | 33.8250 | 40.9189 | 49.7804 |
| ASSET:NEARUSDT | 15m | holdout | frozen3.0 | maker | 274 | 0.053524 | 6.5234 | 0.0000 | 72.9101 | 89.4627 | 103.3945 | 115.4834 | 129.9533 | 145.1517 | 169.1248 | 204.5945 | 248.9021 |
| ASSET:ZECUSDT | 15m | ALL | calibrated | taker | 1798 | 0.125768 | 3.6988 | 0.0000 | 14.7759 | 18.9970 | 22.9696 | 26.2477 | 30.6526 | 36.0805 | 42.6663 | 52.4152 | 69.2555 |
| ASSET:ZECUSDT | 15m | ALL | calibrated | charter | 1798 | 0.251536 | 3.6988 | 0.0000 | 7.3879 | 9.4985 | 11.4848 | 13.1239 | 15.3263 | 18.0402 | 21.3332 | 26.2076 | 34.6277 |
| ASSET:ZECUSDT | 15m | ALL | calibrated | maker | 1798 | 0.050307 | 3.6988 | 0.0000 | 36.9397 | 47.4926 | 57.4240 | 65.6193 | 76.6316 | 90.2012 | 106.6658 | 131.0380 | 173.1387 |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | taker | 814 | 0.125802 | 6.7046 | 0.0000 | 26.9686 | 34.1768 | 40.7379 | 47.1016 | 54.7801 | 62.4419 | 72.8908 | 85.9210 | 112.3651 |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | charter | 814 | 0.251603 | 6.7046 | 0.0000 | 13.4843 | 17.0884 | 20.3689 | 23.5508 | 27.3901 | 31.2209 | 36.4454 | 42.9605 | 56.1825 |
| ASSET:ZECUSDT | 15m | ALL | frozen3.0 | maker | 814 | 0.050321 | 6.7046 | 0.0000 | 67.4216 | 85.4421 | 101.8447 | 117.7540 | 136.9503 | 156.1046 | 182.2269 | 214.8026 | 280.9126 |
| ASSET:ZECUSDT | 15m | tuning | calibrated | taker | 1156 | 0.131762 | 3.7495 | 0.0000 | 13.7566 | 18.1452 | 22.2040 | 25.5086 | 29.2720 | 35.0008 | 40.5405 | 50.0156 | 65.4253 |
| ASSET:ZECUSDT | 15m | tuning | calibrated | charter | 1156 | 0.263525 | 3.7495 | 0.0000 | 6.8783 | 9.0726 | 11.1020 | 12.7543 | 14.6360 | 17.5004 | 20.2702 | 25.0078 | 32.7126 |
| ASSET:ZECUSDT | 15m | tuning | calibrated | maker | 1156 | 0.052705 | 3.7495 | 0.0000 | 34.3914 | 45.3629 | 55.5099 | 63.7714 | 73.1800 | 87.5019 | 101.3512 | 125.0389 | 163.5632 |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | taker | 530 | 0.128857 | 6.6790 | 0.0000 | 24.6798 | 31.6333 | 38.7132 | 44.5700 | 52.3165 | 60.9480 | 71.1003 | 82.7968 | 107.8622 |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | charter | 530 | 0.257713 | 6.6790 | 0.0000 | 12.3399 | 15.8167 | 19.3566 | 22.2850 | 26.1582 | 30.4740 | 35.5501 | 41.3984 | 53.9311 |
| ASSET:ZECUSDT | 15m | tuning | frozen3.0 | maker | 530 | 0.051543 | 6.6790 | 0.0000 | 61.6994 | 79.0834 | 96.7831 | 111.4250 | 130.7911 | 152.3699 | 177.7507 | 206.9919 | 269.6555 |
| ASSET:ZECUSDT | 15m | holdout | calibrated | taker | 642 | 0.115052 | 3.6257 | 0.0000 | 16.7201 | 20.5413 | 24.3770 | 27.8437 | 33.1217 | 38.4571 | 46.4025 | 57.1862 | 77.5962 |
| ASSET:ZECUSDT | 15m | holdout | calibrated | charter | 642 | 0.230105 | 3.6257 | 0.0000 | 8.3600 | 10.2707 | 12.1885 | 13.9219 | 16.5608 | 19.2285 | 23.2012 | 28.5931 | 38.7981 |
| ASSET:ZECUSDT | 15m | holdout | calibrated | maker | 642 | 0.046021 | 3.6257 | 0.0000 | 41.8002 | 51.3533 | 60.9425 | 69.6093 | 82.8042 | 96.1426 | 116.0061 | 142.9656 | 193.9904 |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | taker | 284 | 0.121172 | 6.8123 | 0.0000 | 31.7812 | 38.5457 | 45.6134 | 52.2242 | 57.8866 | 66.9421 | 76.9084 | 90.3176 | 119.3097 |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | charter | 284 | 0.242344 | 6.8123 | 0.0000 | 15.8906 | 19.2728 | 22.8067 | 26.1121 | 28.9433 | 33.4710 | 38.4542 | 45.1588 | 59.6548 |
| ASSET:ZECUSDT | 15m | holdout | frozen3.0 | maker | 284 | 0.048469 | 6.8123 | 0.0000 | 79.4530 | 96.3642 | 114.0335 | 130.5605 | 144.7164 | 167.3552 | 192.2711 | 225.7941 | 298.2742 |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | taker | 8773 | 0.156155 | 3.7556 | 0.0000 | 9.6808 | 13.4328 | 17.0338 | 20.9047 | 24.8201 | 29.5982 | 36.0956 | 45.0109 | 61.3550 |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | charter | 8773 | 0.273297 | 3.7556 | 0.0002 | 6.1188 | 8.1179 | 10.0038 | 12.0006 | 14.1410 | 16.8251 | 20.2004 | 25.1290 | 33.6344 |
| POOLED:CLASSIC5 | 15m | ALL | calibrated | maker | 8773 | 0.062462 | 3.7556 | 0.0000 | 24.2020 | 33.5820 | 42.5846 | 52.2618 | 62.0502 | 73.9955 | 90.2391 | 112.5272 | 153.3876 |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | taker | 4109 | 0.157368 | 6.4267 | 0.0000 | 16.4402 | 23.2419 | 29.2326 | 35.8502 | 42.5055 | 50.5964 | 61.4265 | 76.1330 | 101.5927 |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | charter | 4109 | 0.274572 | 6.4267 | 0.0000 | 10.6541 | 14.3082 | 17.5372 | 20.6250 | 24.3610 | 28.6292 | 34.1769 | 42.1380 | 54.9980 |
| POOLED:CLASSIC5 | 15m | ALL | frozen3.0 | maker | 4109 | 0.062947 | 6.4267 | 0.0000 | 41.1005 | 58.1047 | 73.0814 | 89.6255 | 106.2638 | 126.4910 | 153.5661 | 190.3326 | 253.9818 |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | taker | 5724 | 0.145645 | 3.7480 | 0.0000 | 10.3152 | 14.2788 | 18.3009 | 22.3739 | 26.4308 | 31.6028 | 38.3618 | 47.2730 | 64.4016 |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | charter | 5724 | 0.254505 | 3.7480 | 0.0000 | 6.4942 | 8.7586 | 10.8030 | 12.7948 | 15.1689 | 17.9996 | 21.5541 | 26.8541 | 36.2343 |
| POOLED:CLASSIC5 | 15m | tuning | calibrated | maker | 5724 | 0.058258 | 3.7480 | 0.0000 | 25.7879 | 35.6971 | 45.7523 | 55.9346 | 66.0771 | 79.0070 | 95.9045 | 118.1826 | 161.0040 |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | taker | 2669 | 0.147114 | 6.4424 | 0.0000 | 17.2175 | 24.4257 | 31.0447 | 37.7084 | 44.9591 | 54.7306 | 66.0687 | 81.4657 | 108.1027 |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | charter | 2669 | 0.255043 | 6.4424 | 0.0000 | 11.0846 | 15.1715 | 18.5904 | 22.0296 | 26.0257 | 30.9099 | 36.9262 | 45.5860 | 60.3244 |
| POOLED:CLASSIC5 | 15m | tuning | frozen3.0 | maker | 2669 | 0.058845 | 6.4424 | 0.0000 | 43.0438 | 61.0641 | 77.6118 | 94.2710 | 112.3978 | 136.8264 | 165.1717 | 203.6642 | 270.2567 |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | taker | 3049 | 0.177601 | 3.7649 | 0.0000 | 8.7263 | 12.1831 | 15.2600 | 18.3918 | 21.8723 | 26.0244 | 31.5963 | 39.8467 | 53.8269 |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | charter | 3049 | 0.312855 | 3.7649 | 0.0007 | 5.5444 | 7.3450 | 8.8569 | 10.5708 | 12.4956 | 14.6892 | 17.4967 | 21.9806 | 28.9456 |
| POOLED:CLASSIC5 | 15m | holdout | calibrated | maker | 3049 | 0.071041 | 3.7649 | 0.0000 | 21.8158 | 30.4578 | 38.1500 | 45.9796 | 54.6807 | 65.0609 | 78.9908 | 99.6166 | 134.5672 |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | taker | 1440 | 0.177531 | 6.3927 | 0.0000 | 15.6672 | 21.1091 | 26.8896 | 32.4752 | 37.9076 | 45.4455 | 53.3552 | 65.4635 | 87.1876 |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | charter | 1440 | 0.312266 | 6.3927 | 0.0000 | 10.1311 | 13.2195 | 15.7649 | 18.6058 | 21.9892 | 25.5487 | 29.3238 | 35.4709 | 46.6294 |
| POOLED:CLASSIC5 | 15m | holdout | frozen3.0 | maker | 1440 | 0.071012 | 6.3927 | 0.0000 | 39.1680 | 52.7728 | 67.2240 | 81.1879 | 94.7691 | 113.6139 | 133.3881 | 163.6588 | 217.9691 |
| ASSET:BTCUSDT | 1h | ALL | calibrated | taker | 522 | 0.124026 | 3.5491 | 0.0000 | 12.3337 | 16.9628 | 21.2544 | 25.1980 | 30.7389 | 36.2368 | 42.4338 | 50.8217 | 69.9107 |
| ASSET:BTCUSDT | 1h | ALL | calibrated | charter | 522 | 0.173636 | 3.5491 | 0.0000 | 8.8098 | 12.1163 | 15.1817 | 17.9986 | 21.9564 | 25.8834 | 30.3098 | 36.3012 | 49.9362 |
| ASSET:BTCUSDT | 1h | ALL | calibrated | maker | 522 | 0.049610 | 3.5491 | 0.0000 | 30.8343 | 42.4069 | 53.1360 | 62.9950 | 76.8473 | 90.5920 | 106.0844 | 127.0543 | 174.7769 |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | taker | 223 | 0.121157 | 6.1550 | 0.0000 | 27.1968 | 34.6372 | 40.4213 | 45.6327 | 54.0224 | 65.8617 | 77.1782 | 88.5266 | 112.4224 |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | charter | 223 | 0.169619 | 6.1550 | 0.0000 | 19.4263 | 24.7409 | 28.8723 | 32.5948 | 38.5875 | 47.0440 | 55.1273 | 63.2333 | 80.3017 |
| ASSET:BTCUSDT | 1h | ALL | frozen3.0 | maker | 223 | 0.048463 | 6.1550 | 0.0000 | 67.9920 | 86.5930 | 101.0532 | 114.0818 | 135.0561 | 164.6541 | 192.9456 | 221.3165 | 281.0559 |
| ASSET:BTCUSDT | 1h | tuning | calibrated | taker | 347 | 0.111261 | 3.5575 | 0.0000 | 12.2875 | 18.1746 | 22.5776 | 28.1173 | 33.2824 | 38.7423 | 45.2329 | 55.6470 | 76.0085 |
| ASSET:BTCUSDT | 1h | tuning | calibrated | charter | 347 | 0.155765 | 3.5575 | 0.0000 | 8.7768 | 12.9819 | 16.1269 | 20.0838 | 23.7731 | 27.6731 | 32.3092 | 39.7479 | 54.2918 |
| ASSET:BTCUSDT | 1h | tuning | calibrated | maker | 347 | 0.044504 | 3.5575 | 0.0000 | 30.7188 | 45.4366 | 56.4441 | 70.2934 | 83.2059 | 96.8558 | 113.0824 | 139.1175 | 190.0214 |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | taker | 152 | 0.111846 | 6.0642 | 0.0000 | 27.2075 | 35.1299 | 40.7936 | 48.9126 | 58.2240 | 69.3133 | 81.5250 | 97.8971 | 124.0174 |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | charter | 152 | 0.156584 | 6.0642 | 0.0000 | 19.4340 | 25.0928 | 29.1383 | 34.9376 | 41.5886 | 49.5095 | 58.2322 | 69.9265 | 88.5839 |
| ASSET:BTCUSDT | 1h | tuning | frozen3.0 | maker | 152 | 0.044738 | 6.0642 | 0.0000 | 68.0189 | 87.8247 | 101.9840 | 122.2815 | 145.5600 | 173.2834 | 203.8125 | 244.7429 | 310.0436 |
| ASSET:BTCUSDT | 1h | holdout | calibrated | taker | 175 | 0.139023 | 3.5233 | 0.0000 | 12.4528 | 15.9505 | 18.9745 | 21.9333 | 26.1343 | 30.2932 | 36.2440 | 43.8301 | 54.2075 |
| ASSET:BTCUSDT | 1h | holdout | calibrated | charter | 175 | 0.194632 | 3.5233 | 0.0000 | 8.8948 | 11.3932 | 13.5532 | 15.6666 | 18.6673 | 21.6380 | 25.8886 | 31.3072 | 38.7196 |
| ASSET:BTCUSDT | 1h | holdout | calibrated | maker | 175 | 0.055609 | 3.5233 | 0.0000 | 31.1320 | 39.8762 | 47.4362 | 54.8332 | 65.3357 | 75.7330 | 90.6101 | 109.5752 | 135.5187 |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | taker | 71 | 0.145946 | 6.9691 | 0.0000 | 27.4154 | 34.2272 | 39.1643 | 43.7612 | 46.3189 | 55.6902 | 59.7480 | 76.0021 | 93.6251 |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | charter | 71 | 0.204325 | 6.9691 | 0.0000 | 19.5824 | 24.4480 | 27.9745 | 31.2580 | 33.0850 | 39.7787 | 42.6772 | 54.2872 | 66.8751 |
| ASSET:BTCUSDT | 1h | holdout | frozen3.0 | maker | 71 | 0.058378 | 6.9691 | 0.0000 | 68.5385 | 85.5680 | 97.9107 | 109.4030 | 115.7973 | 139.2256 | 149.3701 | 190.0053 | 234.0627 |
| ASSET:ETHUSDT | 1h | ALL | calibrated | taker | 441 | 0.094027 | 4.1407 | 0.0000 | 20.6763 | 27.3461 | 33.3423 | 39.2719 | 45.9451 | 53.0737 | 60.3832 | 71.4028 | 94.4899 |
| ASSET:ETHUSDT | 1h | ALL | calibrated | charter | 441 | 0.131639 | 4.1407 | 0.0000 | 14.7688 | 19.5329 | 23.8159 | 28.0514 | 32.8179 | 37.9098 | 43.1309 | 51.0020 | 67.4928 |
| ASSET:ETHUSDT | 1h | ALL | calibrated | maker | 441 | 0.037611 | 4.1407 | 0.0000 | 51.6907 | 68.3651 | 83.3558 | 98.1798 | 114.8627 | 132.6842 | 150.9580 | 178.5071 | 236.2248 |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | taker | 231 | 0.094687 | 6.3092 | 0.0000 | 35.6497 | 44.0531 | 53.5723 | 58.8402 | 65.7703 | 77.6996 | 89.0259 | 112.8279 | 141.8992 |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | charter | 231 | 0.132562 | 6.3092 | 0.0000 | 25.4641 | 31.4665 | 38.2659 | 42.0287 | 46.9788 | 55.4997 | 63.5899 | 80.5914 | 101.3566 |
| ASSET:ETHUSDT | 1h | ALL | frozen3.0 | maker | 231 | 0.037875 | 6.3092 | 0.0000 | 89.1243 | 110.1328 | 133.9308 | 147.1004 | 164.4256 | 194.2490 | 222.5646 | 282.0698 | 354.7480 |
| ASSET:ETHUSDT | 1h | tuning | calibrated | taker | 301 | 0.089112 | 4.1407 | 0.0000 | 21.1363 | 27.7428 | 34.4893 | 41.7617 | 49.5137 | 56.5177 | 65.2280 | 77.6996 | 103.4585 |
| ASSET:ETHUSDT | 1h | tuning | calibrated | charter | 301 | 0.124757 | 4.1407 | 0.0000 | 15.0974 | 19.8163 | 24.6352 | 29.8298 | 35.3670 | 40.3698 | 46.5914 | 55.4997 | 73.8989 |
| ASSET:ETHUSDT | 1h | tuning | calibrated | maker | 301 | 0.035645 | 4.1407 | 0.0000 | 52.8408 | 69.3570 | 86.2233 | 104.4042 | 123.7843 | 141.2943 | 163.0700 | 194.2490 | 258.6463 |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | taker | 153 | 0.089249 | 6.2975 | 0.0000 | 37.4042 | 47.0716 | 54.7144 | 60.2717 | 69.5490 | 80.4423 | 97.5353 | 115.1334 | 165.3835 |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | charter | 153 | 0.124949 | 6.2975 | 0.0000 | 26.7173 | 33.6225 | 39.0817 | 43.0512 | 49.6778 | 57.4588 | 69.6680 | 82.2381 | 118.1310 |
| ASSET:ETHUSDT | 1h | tuning | frozen3.0 | maker | 153 | 0.035700 | 6.2975 | 0.0000 | 93.5105 | 117.6789 | 136.7860 | 150.6792 | 173.8724 | 201.1057 | 243.8381 | 287.8335 | 413.4587 |
| ASSET:ETHUSDT | 1h | holdout | calibrated | taker | 140 | 0.104482 | 4.1495 | 0.0000 | 19.1323 | 25.9185 | 31.0886 | 34.6373 | 41.9953 | 45.7926 | 53.6904 | 60.3551 | 82.2927 |
| ASSET:ETHUSDT | 1h | holdout | calibrated | charter | 140 | 0.146275 | 4.1495 | 0.0000 | 13.6659 | 18.5132 | 22.2061 | 24.7409 | 29.9966 | 32.7090 | 38.3503 | 43.1108 | 58.7805 |
| ASSET:ETHUSDT | 1h | holdout | calibrated | maker | 140 | 0.041793 | 4.1495 | 0.0000 | 47.8308 | 64.7962 | 77.7215 | 86.5933 | 104.9882 | 114.4815 | 134.2259 | 150.8879 | 205.7316 |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | taker | 78 | 0.106732 | 6.4292 | 0.0000 | 31.6455 | 41.7423 | 46.2901 | 54.8235 | 60.5319 | 67.7893 | 79.8165 | 99.1223 | 119.9129 |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | charter | 78 | 0.149425 | 6.4292 | 0.0000 | 22.6039 | 29.8159 | 33.0643 | 39.1596 | 43.2371 | 48.4210 | 57.0118 | 70.8016 | 85.6521 |
| ASSET:ETHUSDT | 1h | holdout | frozen3.0 | maker | 78 | 0.042693 | 6.4292 | 0.0000 | 79.1137 | 104.3558 | 115.7252 | 137.0587 | 151.3298 | 169.4733 | 199.5413 | 247.8057 | 299.7823 |
| ASSET:SOLUSDT | 1h | ALL | calibrated | taker | 441 | 0.068286 | 3.8198 | 0.0000 | 28.2630 | 36.6630 | 44.0233 | 50.9724 | 59.1951 | 68.0939 | 81.1142 | 98.0427 | 127.8857 |
| ASSET:SOLUSDT | 1h | ALL | calibrated | charter | 441 | 0.136572 | 3.8198 | 0.0000 | 14.1315 | 18.3315 | 22.0117 | 25.4862 | 29.5975 | 34.0470 | 40.5571 | 49.0214 | 63.9428 |
| ASSET:SOLUSDT | 1h | ALL | calibrated | maker | 441 | 0.027314 | 3.8198 | 0.0000 | 70.6574 | 91.6575 | 110.0583 | 127.4311 | 147.9877 | 170.2348 | 202.7856 | 245.1068 | 319.7142 |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | taker | 203 | 0.068264 | 6.1489 | 0.0000 | 48.8475 | 62.1916 | 73.3074 | 86.1154 | 99.8668 | 115.1344 | 141.6642 | 169.8921 | 214.0537 |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | charter | 203 | 0.136529 | 6.1489 | 0.0000 | 24.4238 | 31.0958 | 36.6537 | 43.0577 | 49.9334 | 57.5672 | 70.8321 | 84.9460 | 107.0269 |
| ASSET:SOLUSDT | 1h | ALL | frozen3.0 | maker | 203 | 0.027306 | 6.1489 | 0.0000 | 122.1188 | 155.4791 | 183.2684 | 215.2885 | 249.6669 | 287.8360 | 354.1604 | 424.7302 | 535.1343 |
| ASSET:SOLUSDT | 1h | tuning | calibrated | taker | 261 | 0.055166 | 3.7711 | 0.0000 | 34.5102 | 44.8873 | 54.2028 | 62.2185 | 72.8077 | 87.1742 | 97.0790 | 115.8858 | 145.5572 |
| ASSET:SOLUSDT | 1h | tuning | calibrated | charter | 261 | 0.110332 | 3.7711 | 0.0000 | 17.2551 | 22.4436 | 27.1014 | 31.1092 | 36.4039 | 43.5871 | 48.5395 | 57.9429 | 72.7786 |
| ASSET:SOLUSDT | 1h | tuning | calibrated | maker | 261 | 0.022066 | 3.7711 | 0.0000 | 86.2755 | 112.2182 | 135.5069 | 155.5462 | 182.0194 | 217.9354 | 242.6974 | 289.7144 | 363.8929 |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | taker | 130 | 0.056333 | 6.0061 | 0.0000 | 57.3513 | 71.0726 | 85.6755 | 104.9577 | 114.8659 | 131.8602 | 164.5393 | 188.3109 | 239.8550 |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | charter | 130 | 0.112665 | 6.0061 | 0.0000 | 28.6757 | 35.5363 | 42.8378 | 52.4788 | 57.4329 | 65.9301 | 82.2697 | 94.1555 | 119.9275 |
| ASSET:SOLUSDT | 1h | tuning | frozen3.0 | maker | 130 | 0.022533 | 6.0061 | 0.0000 | 143.3783 | 177.6815 | 214.1889 | 262.3942 | 287.1647 | 329.6504 | 411.3483 | 470.7773 | 599.6375 |
| ASSET:SOLUSDT | 1h | holdout | calibrated | taker | 180 | 0.089197 | 3.8750 | 0.0000 | 23.9560 | 30.4370 | 36.4607 | 40.9821 | 44.4872 | 50.0012 | 56.2820 | 66.3928 | 82.9407 |
| ASSET:SOLUSDT | 1h | holdout | calibrated | charter | 180 | 0.178394 | 3.8750 | 0.0000 | 11.9780 | 15.2185 | 18.2303 | 20.4910 | 22.2436 | 25.0006 | 28.1410 | 33.1964 | 41.4704 |
| ASSET:SOLUSDT | 1h | holdout | calibrated | maker | 180 | 0.035679 | 3.8750 | 0.0000 | 59.8901 | 76.0926 | 91.1517 | 102.4552 | 111.2181 | 125.0031 | 140.7050 | 165.9819 | 207.3518 |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | taker | 73 | 0.081611 | 6.5849 | 0.0000 | 42.4059 | 51.1891 | 61.4554 | 69.4818 | 77.8241 | 91.9615 | 99.3469 | 118.6077 | 157.5179 |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | charter | 73 | 0.163221 | 6.5849 | 0.0000 | 21.2029 | 25.5946 | 30.7277 | 34.7409 | 38.9121 | 45.9808 | 49.6734 | 59.3038 | 78.7589 |
| ASSET:SOLUSDT | 1h | holdout | frozen3.0 | maker | 73 | 0.032644 | 6.5849 | 0.0000 | 106.0147 | 127.9728 | 153.6386 | 173.7045 | 194.5603 | 229.9038 | 248.3672 | 296.5191 | 393.7947 |
| ASSET:NEARUSDT | 1h | ALL | calibrated | taker | 438 | 0.059451 | 3.6510 | 0.0000 | 32.5887 | 41.2246 | 47.8806 | 57.1800 | 69.1910 | 78.9666 | 91.4987 | 111.8451 | 146.7565 |
| ASSET:NEARUSDT | 1h | ALL | calibrated | charter | 438 | 0.118903 | 3.6510 | 0.0000 | 16.2944 | 20.6123 | 23.9403 | 28.5900 | 34.5955 | 39.4833 | 45.7494 | 55.9225 | 73.3783 |
| ASSET:NEARUSDT | 1h | ALL | calibrated | maker | 438 | 0.023781 | 3.6510 | 0.0000 | 81.4718 | 103.0615 | 119.7014 | 142.9501 | 172.9775 | 197.4165 | 228.7468 | 279.6127 | 366.8913 |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | taker | 211 | 0.059983 | 6.7859 | 0.0000 | 56.7537 | 72.2175 | 88.2905 | 102.0141 | 122.8561 | 141.4906 | 164.8163 | 200.5270 | 253.1501 |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | charter | 211 | 0.119967 | 6.7859 | 0.0000 | 28.3768 | 36.1088 | 44.1453 | 51.0070 | 61.4281 | 70.7453 | 82.4081 | 100.2635 | 126.5750 |
| ASSET:NEARUSDT | 1h | ALL | frozen3.0 | maker | 211 | 0.023993 | 6.7859 | 0.0000 | 141.8842 | 180.5438 | 220.7264 | 255.0352 | 307.1404 | 353.7266 | 412.0407 | 501.3174 | 632.8751 |
| ASSET:NEARUSDT | 1h | tuning | calibrated | taker | 264 | 0.049870 | 3.5257 | 0.0000 | 31.5839 | 42.8747 | 53.4584 | 66.4431 | 78.1620 | 88.4534 | 103.4142 | 128.0460 | 164.3937 |
| ASSET:NEARUSDT | 1h | tuning | calibrated | charter | 264 | 0.099741 | 3.5257 | 0.0000 | 15.7920 | 21.4373 | 26.7292 | 33.2215 | 39.0810 | 44.2267 | 51.7071 | 64.0230 | 82.1968 |
| ASSET:NEARUSDT | 1h | tuning | calibrated | maker | 264 | 0.019948 | 3.5257 | 0.0000 | 78.9598 | 107.1867 | 133.6459 | 166.1077 | 195.4051 | 221.1334 | 258.5355 | 320.1150 | 410.9842 |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | taker | 136 | 0.052580 | 6.4422 | 0.0000 | 54.8208 | 68.7870 | 83.7441 | 102.9698 | 132.2423 | 156.6742 | 187.0919 | 218.2005 | 261.7944 |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | charter | 136 | 0.105161 | 6.4422 | 0.0000 | 27.4104 | 34.3935 | 41.8720 | 51.4849 | 66.1211 | 78.3371 | 93.5460 | 109.1003 | 130.8972 |
| ASSET:NEARUSDT | 1h | tuning | frozen3.0 | maker | 136 | 0.021032 | 6.4422 | 0.0000 | 137.0519 | 171.9675 | 209.3602 | 257.4245 | 330.6057 | 391.6855 | 467.7298 | 545.5013 | 654.4861 |
| ASSET:NEARUSDT | 1h | holdout | calibrated | taker | 174 | 0.066227 | 3.7755 | 0.0000 | 33.7675 | 39.7312 | 43.7312 | 49.1328 | 56.7640 | 67.4724 | 75.9687 | 88.4065 | 114.7229 |
| ASSET:NEARUSDT | 1h | holdout | calibrated | charter | 174 | 0.132453 | 3.7755 | 0.0000 | 16.8837 | 19.8656 | 21.8656 | 24.5664 | 28.3820 | 33.7362 | 37.9844 | 44.2032 | 57.3614 |
| ASSET:NEARUSDT | 1h | holdout | calibrated | maker | 174 | 0.026491 | 3.7755 | 0.0000 | 84.4187 | 99.3280 | 109.3280 | 122.8320 | 141.9099 | 168.6811 | 189.9218 | 221.0162 | 286.8072 |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | taker | 75 | 0.067292 | 7.4399 | 0.0000 | 62.7632 | 75.9445 | 89.6209 | 94.9513 | 118.0977 | 129.8211 | 140.7015 | 168.8002 | 222.2605 |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | charter | 75 | 0.134584 | 7.4399 | 0.0000 | 31.3816 | 37.9722 | 44.8104 | 47.4756 | 59.0488 | 64.9105 | 70.3508 | 84.4001 | 111.1303 |
| ASSET:NEARUSDT | 1h | holdout | frozen3.0 | maker | 75 | 0.026917 | 7.4399 | 0.0000 | 156.9081 | 189.8612 | 224.0522 | 237.3782 | 295.2442 | 324.5527 | 351.7538 | 422.0006 | 555.6513 |
| ASSET:ZECUSDT | 1h | ALL | calibrated | taker | 411 | 0.062441 | 4.1484 | 0.0000 | 34.2185 | 43.3743 | 51.9384 | 61.7657 | 71.8808 | 82.3275 | 95.5607 | 118.6147 | 153.8567 |
| ASSET:ZECUSDT | 1h | ALL | calibrated | charter | 411 | 0.124882 | 4.1484 | 0.0000 | 17.1092 | 21.6871 | 25.9692 | 30.8828 | 35.9404 | 41.1637 | 47.7804 | 59.3074 | 76.9283 |
| ASSET:ZECUSDT | 1h | ALL | calibrated | maker | 411 | 0.024976 | 4.1484 | 0.0000 | 85.5462 | 108.4357 | 129.8459 | 154.4142 | 179.7020 | 205.8186 | 238.9018 | 296.5368 | 384.6417 |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | taker | 220 | 0.062924 | 6.3222 | 0.0000 | 51.0525 | 66.1828 | 79.6187 | 94.2817 | 107.8701 | 128.6198 | 144.5972 | 174.3937 | 209.0330 |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | charter | 220 | 0.125848 | 6.3222 | 0.0000 | 25.5263 | 33.0914 | 39.8094 | 47.1409 | 53.9350 | 64.3099 | 72.2986 | 87.1969 | 104.5165 |
| ASSET:ZECUSDT | 1h | ALL | frozen3.0 | maker | 220 | 0.025170 | 6.3222 | 0.0000 | 127.6313 | 165.4570 | 199.0468 | 235.7043 | 269.6752 | 321.5494 | 361.4931 | 435.9843 | 522.5826 |
| ASSET:ZECUSDT | 1h | tuning | calibrated | taker | 264 | 0.063847 | 4.0883 | 0.0000 | 31.5227 | 37.7361 | 48.7866 | 57.6891 | 67.0953 | 78.2453 | 94.3062 | 118.7274 | 152.1471 |
| ASSET:ZECUSDT | 1h | tuning | calibrated | charter | 264 | 0.127694 | 4.0883 | 0.0000 | 15.7614 | 18.8680 | 24.3933 | 28.8446 | 33.5476 | 39.1227 | 47.1531 | 59.3637 | 76.0735 |
| ASSET:ZECUSDT | 1h | tuning | calibrated | maker | 264 | 0.025539 | 4.0883 | 0.0000 | 78.8068 | 94.3402 | 121.9665 | 144.2229 | 167.7382 | 195.6133 | 235.7656 | 296.8185 | 380.3677 |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | taker | 141 | 0.065105 | 6.2669 | 0.0000 | 48.7870 | 58.3144 | 72.7546 | 87.6232 | 103.7114 | 121.9531 | 138.8271 | 165.1578 | 207.7001 |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | charter | 141 | 0.130209 | 6.2669 | 0.0000 | 24.3935 | 29.1572 | 36.3773 | 43.8116 | 51.8557 | 60.9766 | 69.4135 | 82.5789 | 103.8501 |
| ASSET:ZECUSDT | 1h | tuning | frozen3.0 | maker | 141 | 0.026042 | 6.2669 | 0.0000 | 121.9675 | 145.7859 | 181.8866 | 219.0581 | 259.2785 | 304.8828 | 347.0677 | 412.8944 | 519.2503 |
| ASSET:ZECUSDT | 1h | holdout | calibrated | taker | 147 | 0.059184 | 4.3713 | 0.0000 | 43.3633 | 52.0032 | 60.5797 | 69.9642 | 80.5825 | 89.8850 | 97.6937 | 116.0483 | 158.2046 |
| ASSET:ZECUSDT | 1h | holdout | calibrated | charter | 147 | 0.118368 | 4.3713 | 0.0000 | 21.6817 | 26.0016 | 30.2898 | 34.9821 | 40.2913 | 44.9425 | 48.8468 | 58.0241 | 79.1023 |
| ASSET:ZECUSDT | 1h | holdout | calibrated | maker | 147 | 0.023674 | 4.3713 | 0.0000 | 108.4084 | 130.0080 | 151.4492 | 174.9104 | 201.4563 | 224.7125 | 244.2342 | 290.1207 | 395.5116 |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | taker | 79 | 0.061641 | 6.5420 | 0.0000 | 68.2221 | 76.3656 | 90.3740 | 103.4839 | 113.7101 | 143.1536 | 166.4405 | 185.7730 | 206.6846 |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | charter | 79 | 0.123282 | 6.5420 | 0.0000 | 34.1110 | 38.1828 | 45.1870 | 51.7420 | 56.8550 | 71.5768 | 83.2203 | 92.8865 | 103.3423 |
| ASSET:ZECUSDT | 1h | holdout | frozen3.0 | maker | 79 | 0.024656 | 6.5420 | 0.0000 | 170.5552 | 190.9140 | 225.9351 | 258.7098 | 284.2752 | 357.8840 | 416.1013 | 464.4325 | 516.7115 |
| ASSET:ENAUSDT | 1h | ALL | calibrated | taker | 222 | 0.049890 | 3.0060 | 0.0000 | 30.3327 | 38.3233 | 47.0136 | 56.0772 | 67.3701 | 75.2038 | 86.0299 | 108.4074 | 147.7638 |
| ASSET:ENAUSDT | 1h | ALL | calibrated | charter | 222 | 0.149669 | 3.0060 | 0.0000 | 10.1109 | 12.7744 | 15.6712 | 18.6924 | 22.4567 | 25.0679 | 28.6766 | 36.1358 | 49.2546 |
| ASSET:ENAUSDT | 1h | ALL | calibrated | maker | 222 | 0.019956 | 3.0060 | 0.0000 | 75.8317 | 95.8081 | 117.5339 | 140.1931 | 168.4252 | 188.0095 | 215.0748 | 271.0184 | 369.4096 |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | taker | 78 | 0.049230 | 7.0577 | 0.0000 | 86.2426 | 106.4241 | 116.3839 | 135.8470 | 153.4566 | 174.9744 | 195.6582 | 237.9310 | 287.9590 |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | charter | 78 | 0.147690 | 7.0577 | 0.0000 | 28.7475 | 35.4747 | 38.7946 | 45.2823 | 51.1522 | 58.3248 | 65.2194 | 79.3103 | 95.9863 |
| ASSET:ENAUSDT | 1h | ALL | frozen3.0 | maker | 78 | 0.019692 | 7.0577 | 0.0000 | 215.6066 | 266.0602 | 290.9598 | 339.6175 | 383.6416 | 437.4360 | 489.1455 | 594.8276 | 719.8975 |
| ASSET:ENAUSDT | 1h | tuning | calibrated | taker | 11 | 0.053307 | 3.1479 | 0.0000 | 49.5627 | 51.2310 | 53.9314 | 65.6028 | 82.1003 | 89.8979 | 96.1907 | 101.2234 | 126.2554 |
| ASSET:ENAUSDT | 1h | tuning | calibrated | charter | 11 | 0.159921 | 3.1479 | 0.0000 | 16.5209 | 17.0770 | 17.9771 | 21.8676 | 27.3668 | 29.9660 | 32.0636 | 33.7411 | 42.0851 |
| ASSET:ENAUSDT | 1h | tuning | calibrated | maker | 11 | 0.021323 | 3.1479 | 0.0000 | 123.9067 | 128.0774 | 134.8285 | 164.0071 | 205.2508 | 224.7449 | 240.4768 | 253.0585 | 315.6385 |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | taker | 6 | 0.036626 | 7.3476 | 0.0000 | 99.5010 | 115.6839 | 128.0287 | 140.3735 | 203.7933 | 267.2131 | 270.8785 | 274.5439 | 288.9462 |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | charter | 6 | 0.109879 | 7.3476 | 0.0000 | 33.1670 | 38.5613 | 42.6762 | 46.7912 | 67.9311 | 89.0710 | 90.2928 | 91.5146 | 96.3154 |
| ASSET:ENAUSDT | 1h | tuning | frozen3.0 | maker | 6 | 0.014651 | 7.3476 | 0.0000 | 248.7525 | 289.2099 | 320.0718 | 350.9337 | 509.4832 | 668.0328 | 677.1962 | 686.3597 | 722.3654 |
| ASSET:ENAUSDT | 1h | holdout | calibrated | taker | 211 | 0.049854 | 3.0049 | 0.0000 | 30.3106 | 37.9990 | 46.8254 | 55.9396 | 67.2451 | 74.2197 | 83.4817 | 108.5029 | 147.8010 |
| ASSET:ENAUSDT | 1h | holdout | calibrated | charter | 211 | 0.149563 | 3.0049 | 0.0000 | 10.1035 | 12.6663 | 15.6085 | 18.6465 | 22.4150 | 24.7399 | 27.8272 | 36.1676 | 49.2670 |
| ASSET:ENAUSDT | 1h | holdout | calibrated | maker | 211 | 0.019942 | 3.0049 | 0.0000 | 75.7766 | 94.9976 | 117.0635 | 139.8490 | 168.1128 | 185.5493 | 208.7043 | 271.2572 | 369.5025 |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | taker | 72 | 0.049374 | 7.0577 | 0.0000 | 88.0781 | 106.0289 | 116.7208 | 135.7611 | 153.4566 | 172.8373 | 192.7788 | 223.0439 | 284.2813 |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | charter | 72 | 0.148121 | 7.0577 | 0.0000 | 29.3594 | 35.3430 | 38.9069 | 45.2537 | 51.1522 | 57.6124 | 64.2596 | 74.3480 | 94.7604 |
| ASSET:ENAUSDT | 1h | holdout | frozen3.0 | maker | 72 | 0.019749 | 7.0577 | 0.0000 | 220.1953 | 265.0724 | 291.8019 | 339.4029 | 383.6416 | 432.0932 | 481.9470 | 557.6097 | 710.7032 |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | taker | 75 | 0.045281 | 4.6278 | 0.0000 | 60.8823 | 67.4093 | 76.0933 | 87.6429 | 102.8996 | 120.4175 | 130.1206 | 158.0950 | 208.9744 |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | charter | 75 | 0.135844 | 4.6278 | 0.0000 | 20.2941 | 22.4698 | 25.3644 | 29.2143 | 34.2999 | 40.1392 | 43.3735 | 52.6983 | 69.6581 |
| ASSET:PUMPUSDT | 1h | ALL | calibrated | maker | 75 | 0.018113 | 4.6278 | 0.0000 | 152.2057 | 168.5233 | 190.2333 | 219.1072 | 257.2489 | 301.0438 | 325.3015 | 395.2376 | 522.4359 |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | taker | 42 | 0.046207 | 6.7734 | 0.0000 | 88.4507 | 108.3940 | 121.3557 | 126.2712 | 137.3070 | 152.3465 | 174.2665 | 227.2140 | 300.7940 |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | charter | 42 | 0.138620 | 6.7734 | 0.0000 | 29.4836 | 36.1313 | 40.4519 | 42.0904 | 45.7690 | 50.7822 | 58.0888 | 75.7380 | 100.2647 |
| ASSET:PUMPUSDT | 1h | ALL | frozen3.0 | maker | 42 | 0.018483 | 6.7734 | 0.0000 | 221.1268 | 270.9849 | 303.3892 | 315.6779 | 343.2676 | 380.8663 | 435.6663 | 568.0349 | 751.9850 |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | taker | 75 | 0.045281 | 4.6278 | 0.0000 | 60.8823 | 67.4093 | 76.0933 | 87.6429 | 102.8996 | 120.4175 | 130.1206 | 158.0950 | 208.9744 |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | charter | 75 | 0.135844 | 4.6278 | 0.0000 | 20.2941 | 22.4698 | 25.3644 | 29.2143 | 34.2999 | 40.1392 | 43.3735 | 52.6983 | 69.6581 |
| ASSET:PUMPUSDT | 1h | holdout | calibrated | maker | 75 | 0.018113 | 4.6278 | 0.0000 | 152.2057 | 168.5233 | 190.2333 | 219.1072 | 257.2489 | 301.0438 | 325.3015 | 395.2376 | 522.4359 |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | taker | 42 | 0.046207 | 6.7734 | 0.0000 | 88.4507 | 108.3940 | 121.3557 | 126.2712 | 137.3070 | 152.3465 | 174.2665 | 227.2140 | 300.7940 |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | charter | 42 | 0.138620 | 6.7734 | 0.0000 | 29.4836 | 36.1313 | 40.4519 | 42.0904 | 45.7690 | 50.7822 | 58.0888 | 75.7380 | 100.2647 |
| ASSET:PUMPUSDT | 1h | holdout | frozen3.0 | maker | 42 | 0.018483 | 6.7734 | 0.0000 | 221.1268 | 270.9849 | 303.3892 | 315.6779 | 343.2676 | 380.8663 | 435.6663 | 568.0349 | 751.9850 |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | taker | 82 | 0.069006 | 4.4562 | 0.0000 | 36.5753 | 45.1994 | 54.1251 | 60.5915 | 65.1540 | 73.1745 | 78.6190 | 89.9766 | 116.1720 |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | charter | 82 | 0.207019 | 4.4562 | 0.0000 | 12.1918 | 15.0665 | 18.0417 | 20.1972 | 21.7180 | 24.3915 | 26.2063 | 29.9922 | 38.7240 |
| ASSET:HYPEUSDT | 1h | ALL | calibrated | maker | 82 | 0.027603 | 4.4562 | 0.0000 | 91.4382 | 112.9986 | 135.3126 | 151.4787 | 162.8850 | 182.9362 | 196.5475 | 224.9415 | 290.4299 |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | taker | 40 | 0.069575 | 6.8525 | 0.0000 | 53.9295 | 67.4226 | 74.9255 | 96.2949 | 108.8245 | 120.9787 | 139.3234 | 173.0412 | 215.2607 |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | charter | 40 | 0.208724 | 6.8525 | 0.0000 | 17.9765 | 22.4742 | 24.9752 | 32.0983 | 36.2748 | 40.3262 | 46.4411 | 57.6804 | 71.7536 |
| ASSET:HYPEUSDT | 1h | ALL | frozen3.0 | maker | 40 | 0.027830 | 6.8525 | 0.0000 | 134.8238 | 168.5565 | 187.3137 | 240.7372 | 272.0613 | 302.4467 | 348.3086 | 432.6031 | 538.1517 |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | taker | 82 | 0.069006 | 4.4562 | 0.0000 | 36.5753 | 45.1994 | 54.1251 | 60.5915 | 65.1540 | 73.1745 | 78.6190 | 89.9766 | 116.1720 |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | charter | 82 | 0.207019 | 4.4562 | 0.0000 | 12.1918 | 15.0665 | 18.0417 | 20.1972 | 21.7180 | 24.3915 | 26.2063 | 29.9922 | 38.7240 |
| ASSET:HYPEUSDT | 1h | holdout | calibrated | maker | 82 | 0.027603 | 4.4562 | 0.0000 | 91.4382 | 112.9986 | 135.3126 | 151.4787 | 162.8850 | 182.9362 | 196.5475 | 224.9415 | 290.4299 |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | taker | 40 | 0.069575 | 6.8525 | 0.0000 | 53.9295 | 67.4226 | 74.9255 | 96.2949 | 108.8245 | 120.9787 | 139.3234 | 173.0412 | 215.2607 |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | charter | 40 | 0.208724 | 6.8525 | 0.0000 | 17.9765 | 22.4742 | 24.9752 | 32.0983 | 36.2748 | 40.3262 | 46.4411 | 57.6804 | 71.7536 |
| ASSET:HYPEUSDT | 1h | holdout | frozen3.0 | maker | 40 | 0.027830 | 6.8525 | 0.0000 | 134.8238 | 168.5565 | 187.3137 | 240.7372 | 272.0613 | 302.4467 | 348.3086 | 432.6031 | 538.1517 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | taker | 162 | 0.099171 | 4.8869 | 0.0000 | 25.3186 | 33.8307 | 41.4976 | 46.2051 | 53.3859 | 63.6587 | 75.0339 | 85.4111 | 128.6611 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | charter | 162 | 0.297512 | 4.8869 | 0.0000 | 8.4395 | 11.2769 | 13.8325 | 15.4017 | 17.7953 | 21.2196 | 25.0113 | 28.4704 | 42.8870 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | calibrated | maker | 162 | 0.039668 | 4.8869 | 0.0000 | 63.2966 | 84.5768 | 103.7441 | 115.5127 | 133.4647 | 159.1467 | 187.5848 | 213.5276 | 321.6528 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | taker | 97 | 0.096138 | 6.9585 | 0.0000 | 39.8188 | 48.9105 | 55.3842 | 62.6209 | 78.6316 | 92.2152 | 112.9146 | 135.4249 | 162.0580 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | charter | 97 | 0.288415 | 6.9585 | 0.0000 | 13.2729 | 16.3035 | 18.4614 | 20.8736 | 26.2105 | 30.7384 | 37.6382 | 45.1416 | 54.0193 |
| ASSET:MNTUSDT_BYBIT | 1h | ALL | frozen3.0 | maker | 97 | 0.038455 | 6.9585 | 0.0000 | 99.5470 | 122.2763 | 138.4605 | 156.5522 | 196.5791 | 230.5380 | 282.2864 | 338.5623 | 405.1449 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | taker | 46 | 0.096532 | 4.7320 | 0.0000 | 20.5458 | 27.9003 | 38.0091 | 43.5728 | 46.3112 | 51.1620 | 70.3774 | 80.9533 | 102.5266 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | charter | 46 | 0.289597 | 4.7320 | 0.0000 | 6.8486 | 9.3001 | 12.6697 | 14.5243 | 15.4371 | 17.0540 | 23.4591 | 26.9844 | 34.1755 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | calibrated | maker | 46 | 0.038613 | 4.7320 | 0.0000 | 51.3644 | 69.7507 | 95.0227 | 108.9319 | 115.7779 | 127.9051 | 175.9436 | 202.3833 | 256.3165 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | taker | 28 | 0.098421 | 7.0875 | 0.0000 | 44.9121 | 49.4038 | 57.7686 | 73.9359 | 80.7159 | 93.9585 | 130.6900 | 141.8744 | 152.1931 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | charter | 28 | 0.295264 | 7.0875 | 0.0000 | 14.9707 | 16.4679 | 19.2562 | 24.6453 | 26.9053 | 31.3195 | 43.5633 | 47.2915 | 50.7310 |
| ASSET:MNTUSDT_BYBIT | 1h | tuning | frozen3.0 | maker | 28 | 0.039369 | 7.0875 | 0.0000 | 112.2803 | 123.5094 | 144.4214 | 184.8398 | 201.7898 | 234.8963 | 326.7250 | 354.6861 | 380.4826 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | taker | 116 | 0.101018 | 4.9919 | 0.0000 | 27.9715 | 35.4974 | 42.1857 | 48.7751 | 56.1547 | 66.7392 | 75.5504 | 92.3960 | 133.6753 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | charter | 116 | 0.303054 | 4.9919 | 0.0000 | 9.3238 | 11.8325 | 14.0619 | 16.2584 | 18.7182 | 22.2464 | 25.1835 | 30.7987 | 44.5584 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | calibrated | maker | 116 | 0.040407 | 4.9919 | 0.0000 | 69.9287 | 88.7435 | 105.4644 | 121.9376 | 140.3868 | 166.8481 | 188.8760 | 230.9901 | 334.1884 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | taker | 69 | 0.094523 | 6.6964 | 0.0000 | 35.3178 | 49.1814 | 55.0667 | 61.4647 | 78.5542 | 90.4887 | 111.1952 | 128.6283 | 181.1908 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | charter | 69 | 0.283570 | 6.6964 | 0.0000 | 11.7726 | 16.3938 | 18.3556 | 20.4882 | 26.1847 | 30.1629 | 37.0651 | 42.8761 | 60.3969 |
| ASSET:MNTUSDT_BYBIT | 1h | holdout | frozen3.0 | maker | 69 | 0.037809 | 6.6964 | 0.0000 | 88.2945 | 122.9536 | 137.6668 | 153.6617 | 196.3854 | 226.2218 | 277.9881 | 321.5707 | 452.9770 |
| ASSET:SUIUSDT | 1h | ALL | calibrated | taker | 230 | 0.066185 | 4.0690 | 0.0000 | 35.1744 | 42.9007 | 48.6470 | 56.2003 | 66.3626 | 73.6394 | 87.6379 | 104.1005 | 134.6970 |
| ASSET:SUIUSDT | 1h | ALL | calibrated | charter | 230 | 0.132369 | 4.0690 | 0.0000 | 17.5872 | 21.4503 | 24.3235 | 28.1001 | 33.1813 | 36.8197 | 43.8190 | 52.0502 | 67.3485 |
| ASSET:SUIUSDT | 1h | ALL | calibrated | maker | 230 | 0.026474 | 4.0690 | 0.0000 | 87.9360 | 107.2516 | 121.6176 | 140.5007 | 165.9066 | 184.0985 | 219.0949 | 260.2511 | 336.7425 |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | taker | 108 | 0.063144 | 6.3928 | 0.0000 | 48.4190 | 65.0575 | 79.3888 | 94.2561 | 103.5694 | 117.1472 | 145.4751 | 168.3178 | 208.4762 |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | charter | 108 | 0.126287 | 6.3928 | 0.0000 | 24.2095 | 32.5287 | 39.6944 | 47.1281 | 51.7847 | 58.5736 | 72.7376 | 84.1589 | 104.2381 |
| ASSET:SUIUSDT | 1h | ALL | frozen3.0 | maker | 108 | 0.025257 | 6.3928 | 0.0000 | 121.0474 | 162.6437 | 198.4720 | 235.6403 | 258.9236 | 292.8679 | 363.6878 | 420.7944 | 521.1905 |
| ASSET:SUIUSDT | 1h | tuning | calibrated | taker | 86 | 0.061538 | 3.7354 | 0.0000 | 35.7220 | 45.4545 | 49.8912 | 55.8231 | 65.5000 | 74.9207 | 88.8073 | 98.4681 | 123.8119 |
| ASSET:SUIUSDT | 1h | tuning | calibrated | charter | 86 | 0.123075 | 3.7354 | 0.0000 | 17.8610 | 22.7273 | 24.9456 | 27.9115 | 32.7500 | 37.4604 | 44.4036 | 49.2340 | 61.9060 |
| ASSET:SUIUSDT | 1h | tuning | calibrated | maker | 86 | 0.024615 | 3.7354 | 0.0000 | 89.3051 | 113.6364 | 124.7279 | 139.5576 | 163.7499 | 187.3018 | 222.0182 | 246.1701 | 309.5298 |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | taker | 41 | 0.060102 | 6.1923 | 0.0000 | 55.1963 | 63.8759 | 89.7553 | 99.1389 | 116.9902 | 129.4381 | 147.8552 | 172.3866 | 195.3766 |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | charter | 41 | 0.120203 | 6.1923 | 0.0000 | 27.5982 | 31.9380 | 44.8777 | 49.5695 | 58.4951 | 64.7190 | 73.9276 | 86.1933 | 97.6883 |
| ASSET:SUIUSDT | 1h | tuning | frozen3.0 | maker | 41 | 0.024041 | 6.1923 | 0.0000 | 137.9908 | 159.6898 | 224.3883 | 247.8473 | 292.4756 | 323.5952 | 369.6380 | 430.9665 | 488.4415 |
| ASSET:SUIUSDT | 1h | holdout | calibrated | taker | 144 | 0.069191 | 4.1872 | 0.0000 | 34.5803 | 40.7779 | 48.5901 | 56.4000 | 67.7077 | 72.7324 | 86.6603 | 109.7313 | 145.1532 |
| ASSET:SUIUSDT | 1h | holdout | calibrated | charter | 144 | 0.138382 | 4.1872 | 0.0000 | 17.2901 | 20.3890 | 24.2950 | 28.2000 | 33.8539 | 36.3662 | 43.3302 | 54.8657 | 72.5766 |
| ASSET:SUIUSDT | 1h | holdout | calibrated | maker | 144 | 0.027676 | 4.1872 | 0.0000 | 86.4507 | 101.9448 | 121.4751 | 140.9999 | 169.2693 | 181.8309 | 216.6508 | 274.3284 | 362.8829 |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | taker | 67 | 0.067487 | 6.6926 | 0.0000 | 48.4151 | 66.6088 | 77.0915 | 93.6035 | 101.2371 | 114.1650 | 143.2832 | 162.5668 | 217.4087 |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | charter | 67 | 0.134973 | 6.6926 | 0.0000 | 24.2075 | 33.3044 | 38.5457 | 46.8018 | 50.6185 | 57.0825 | 71.6416 | 81.2834 | 108.7043 |
| ASSET:SUIUSDT | 1h | holdout | frozen3.0 | maker | 67 | 0.026995 | 6.6926 | 0.0000 | 121.0376 | 166.5220 | 192.7287 | 234.0089 | 253.0927 | 285.4125 | 358.2081 | 406.4171 | 543.5217 |
| ASSET:LTCUSDT | 1h | ALL | calibrated | taker | 465 | 0.082639 | 3.5816 | 0.0000 | 21.5829 | 27.2945 | 33.3825 | 38.0467 | 45.6237 | 53.5385 | 64.6149 | 79.7857 | 104.4498 |
| ASSET:LTCUSDT | 1h | ALL | calibrated | charter | 465 | 0.165277 | 3.5816 | 0.0000 | 10.7914 | 13.6473 | 16.6912 | 19.0233 | 22.8119 | 26.7692 | 32.3074 | 39.8929 | 52.2249 |
| ASSET:LTCUSDT | 1h | ALL | calibrated | maker | 465 | 0.033055 | 3.5816 | 0.0000 | 53.9572 | 68.2363 | 83.4562 | 95.1167 | 114.0593 | 133.8461 | 161.5372 | 199.4643 | 261.1246 |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | taker | 217 | 0.081044 | 6.3966 | 0.0000 | 45.4851 | 53.9556 | 60.9473 | 70.9051 | 77.9979 | 89.2542 | 102.6284 | 120.8236 | 158.6099 |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | charter | 217 | 0.162088 | 6.3966 | 0.0000 | 22.7426 | 26.9778 | 30.4736 | 35.4525 | 38.9989 | 44.6271 | 51.3142 | 60.4118 | 79.3049 |
| ASSET:LTCUSDT | 1h | ALL | frozen3.0 | maker | 217 | 0.032418 | 6.3966 | 0.0000 | 113.7129 | 134.8890 | 152.3682 | 177.2627 | 194.9946 | 223.1355 | 256.5711 | 302.0590 | 396.5247 |
| ASSET:LTCUSDT | 1h | tuning | calibrated | taker | 302 | 0.074796 | 3.5803 | 0.0000 | 22.8100 | 30.6147 | 36.2986 | 41.9240 | 49.3281 | 58.1470 | 71.6011 | 90.2568 | 125.8629 |
| ASSET:LTCUSDT | 1h | tuning | calibrated | charter | 302 | 0.149591 | 3.5803 | 0.0000 | 11.4050 | 15.3074 | 18.1493 | 20.9620 | 24.6640 | 29.0735 | 35.8005 | 45.1284 | 62.9314 |
| ASSET:LTCUSDT | 1h | tuning | calibrated | maker | 302 | 0.029918 | 3.5803 | 0.0000 | 57.0249 | 76.5368 | 90.7465 | 104.8101 | 123.3201 | 145.3675 | 179.0027 | 225.6421 | 314.6572 |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | taker | 144 | 0.076347 | 6.1202 | 0.0000 | 45.4917 | 57.2535 | 65.1286 | 72.6490 | 85.5215 | 93.5561 | 110.5999 | 130.6820 | 163.9730 |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | charter | 144 | 0.152694 | 6.1202 | 0.0000 | 22.7458 | 28.6268 | 32.5643 | 36.3245 | 42.7607 | 46.7781 | 55.2999 | 65.3410 | 81.9865 |
| ASSET:LTCUSDT | 1h | tuning | frozen3.0 | maker | 144 | 0.030539 | 6.1202 | 0.0000 | 113.7292 | 143.1339 | 162.8215 | 181.6224 | 213.8037 | 233.8903 | 276.4996 | 326.7051 | 409.9326 |
| ASSET:LTCUSDT | 1h | holdout | calibrated | taker | 163 | 0.098409 | 3.5816 | 0.0000 | 20.4450 | 24.0656 | 30.9117 | 33.5082 | 38.0780 | 46.8805 | 54.0090 | 61.4841 | 79.5881 |
| ASSET:LTCUSDT | 1h | holdout | calibrated | charter | 163 | 0.196819 | 3.5816 | 0.0000 | 10.2225 | 12.0328 | 15.4559 | 16.7541 | 19.0390 | 23.4403 | 27.0045 | 30.7421 | 39.7941 |
| ASSET:LTCUSDT | 1h | holdout | calibrated | maker | 163 | 0.039364 | 3.5816 | 0.0000 | 51.1125 | 60.1640 | 77.2793 | 83.7704 | 95.1949 | 117.2013 | 135.0225 | 153.7103 | 198.9703 |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | taker | 73 | 0.100216 | 7.1247 | 0.0000 | 45.6751 | 51.0395 | 57.1614 | 61.4507 | 71.8213 | 76.9271 | 89.9954 | 104.8014 | 121.6100 |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | charter | 73 | 0.200433 | 7.1247 | 0.0000 | 22.8375 | 25.5198 | 28.5807 | 30.7254 | 35.9107 | 38.4635 | 44.9977 | 52.4007 | 60.8050 |
| ASSET:LTCUSDT | 1h | holdout | frozen3.0 | maker | 73 | 0.040087 | 7.1247 | 0.0000 | 114.1877 | 127.5988 | 142.9034 | 153.6268 | 179.5533 | 192.3177 | 224.9886 | 262.0035 | 304.0250 |
| ASSET:XMRUSDT | 1h | ALL | calibrated | taker | 435 | 0.078550 | 3.1000 | 0.0000 | 19.5384 | 25.4583 | 30.5698 | 36.5595 | 42.8274 | 49.7758 | 59.8302 | 71.3530 | 92.6106 |
| ASSET:XMRUSDT | 1h | ALL | calibrated | charter | 435 | 0.157101 | 3.1000 | 0.0000 | 9.7692 | 12.7292 | 15.2849 | 18.2797 | 21.4137 | 24.8879 | 29.9151 | 35.6765 | 46.3053 |
| ASSET:XMRUSDT | 1h | ALL | calibrated | maker | 435 | 0.031420 | 3.1000 | 0.0000 | 48.8459 | 63.6458 | 76.4244 | 91.3986 | 107.0685 | 124.4394 | 149.5755 | 178.3826 | 231.5266 |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | taker | 173 | 0.083674 | 6.7213 | 0.0000 | 47.7717 | 58.3840 | 66.9549 | 74.3245 | 83.7279 | 94.0326 | 105.1449 | 125.9031 | 155.8283 |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | charter | 173 | 0.167347 | 6.7213 | 0.0000 | 23.8859 | 29.1920 | 33.4774 | 37.1623 | 41.8640 | 47.0163 | 52.5724 | 62.9515 | 77.9142 |
| ASSET:XMRUSDT | 1h | ALL | frozen3.0 | maker | 173 | 0.033469 | 6.7213 | 0.0000 | 119.4293 | 145.9599 | 167.3872 | 185.8113 | 209.3198 | 235.0815 | 262.8622 | 314.7577 | 389.5708 |
| ASSET:XMRUSDT | 1h | tuning | calibrated | taker | 293 | 0.076574 | 3.0771 | 0.0000 | 16.6609 | 24.1813 | 29.5991 | 35.4340 | 41.8773 | 50.1903 | 59.6142 | 72.4869 | 93.8674 |
| ASSET:XMRUSDT | 1h | tuning | calibrated | charter | 293 | 0.153149 | 3.0771 | 0.0000 | 8.3305 | 12.0906 | 14.7996 | 17.7170 | 20.9387 | 25.0952 | 29.8071 | 36.2435 | 46.9337 |
| ASSET:XMRUSDT | 1h | tuning | calibrated | maker | 293 | 0.030630 | 3.0771 | 0.0000 | 41.6524 | 60.4532 | 73.9978 | 88.5849 | 104.6933 | 125.4758 | 149.0355 | 181.2173 | 234.6684 |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | taker | 111 | 0.081054 | 6.4440 | 0.0000 | 47.1259 | 55.2399 | 64.9672 | 70.8241 | 85.1713 | 95.0704 | 112.0588 | 130.9079 | 166.7222 |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | charter | 111 | 0.162107 | 6.4440 | 0.0000 | 23.5629 | 27.6200 | 32.4836 | 35.4120 | 42.5857 | 47.5352 | 56.0294 | 65.4539 | 83.3611 |
| ASSET:XMRUSDT | 1h | tuning | frozen3.0 | maker | 111 | 0.032421 | 6.4440 | 0.0000 | 117.8147 | 138.0999 | 162.4179 | 177.0602 | 212.9283 | 237.6761 | 280.1470 | 327.2697 | 416.8055 |
| ASSET:XMRUSDT | 1h | holdout | calibrated | taker | 142 | 0.081662 | 3.1720 | 0.0000 | 23.1645 | 27.0349 | 32.6605 | 38.5031 | 43.4804 | 48.7857 | 59.8875 | 67.6929 | 87.7746 |
| ASSET:XMRUSDT | 1h | holdout | calibrated | charter | 142 | 0.163323 | 3.1720 | 0.0000 | 11.5823 | 13.5174 | 16.3303 | 19.2516 | 21.7402 | 24.3929 | 29.9438 | 33.8465 | 43.8873 |
| ASSET:XMRUSDT | 1h | holdout | calibrated | maker | 142 | 0.032665 | 3.1720 | 0.0000 | 57.9113 | 67.5872 | 81.6513 | 96.2578 | 108.7010 | 121.9644 | 149.7188 | 169.2323 | 219.4365 |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | taker | 62 | 0.085877 | 7.0413 | 0.0000 | 53.2918 | 66.4457 | 72.2097 | 76.2043 | 83.6174 | 88.3019 | 100.7061 | 115.3011 | 133.7361 |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | charter | 62 | 0.171753 | 7.0413 | 0.0000 | 26.6459 | 33.2228 | 36.1048 | 38.1021 | 41.8087 | 44.1509 | 50.3530 | 57.6506 | 66.8680 |
| ASSET:XMRUSDT | 1h | holdout | frozen3.0 | maker | 62 | 0.034351 | 7.0413 | 0.0000 | 133.2295 | 166.1142 | 180.5242 | 190.5107 | 209.0435 | 220.7547 | 251.7652 | 288.2528 | 334.3402 |
| ASSET:BNBUSDT | 1h | ALL | calibrated | taker | 486 | 0.105209 | 3.6477 | 0.0000 | 15.8396 | 20.8197 | 25.8774 | 30.4701 | 37.0951 | 41.9699 | 52.3297 | 64.7008 | 93.5846 |
| ASSET:BNBUSDT | 1h | ALL | calibrated | charter | 486 | 0.210419 | 3.6477 | 0.0000 | 7.9198 | 10.4098 | 12.9387 | 15.2351 | 18.5476 | 20.9850 | 26.1648 | 32.3504 | 46.7923 |
| ASSET:BNBUSDT | 1h | ALL | calibrated | maker | 486 | 0.042084 | 3.6477 | 0.0000 | 39.5991 | 52.0492 | 64.6934 | 76.1753 | 92.7378 | 104.9248 | 130.8242 | 161.7520 | 233.9615 |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | taker | 220 | 0.101548 | 6.6163 | 0.0000 | 33.0325 | 40.6214 | 47.8279 | 57.4807 | 68.1960 | 76.8059 | 90.9661 | 119.2592 | 155.2915 |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | charter | 220 | 0.203096 | 6.6163 | 0.0000 | 16.5162 | 20.3107 | 23.9140 | 28.7403 | 34.0980 | 38.4029 | 45.4830 | 59.6296 | 77.6458 |
| ASSET:BNBUSDT | 1h | ALL | frozen3.0 | maker | 220 | 0.040619 | 6.6163 | 0.0000 | 82.5812 | 101.5534 | 119.5698 | 143.7016 | 170.4901 | 192.0147 | 227.4152 | 298.1480 | 388.2288 |
| ASSET:BNBUSDT | 1h | tuning | calibrated | taker | 310 | 0.090138 | 3.6346 | 0.0000 | 18.3401 | 24.0907 | 29.1250 | 34.7862 | 41.6709 | 51.9885 | 60.9138 | 75.7043 | 105.6054 |
| ASSET:BNBUSDT | 1h | tuning | calibrated | charter | 310 | 0.180275 | 3.6346 | 0.0000 | 9.1701 | 12.0454 | 14.5625 | 17.3931 | 20.8355 | 25.9942 | 30.4569 | 37.8522 | 52.8027 |
| ASSET:BNBUSDT | 1h | tuning | calibrated | maker | 310 | 0.036055 | 3.6346 | 0.0000 | 45.8504 | 60.2268 | 72.8124 | 86.9654 | 104.1773 | 129.9712 | 152.2845 | 189.2608 | 264.0134 |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | taker | 142 | 0.085290 | 6.3201 | 0.0000 | 38.0092 | 48.6159 | 63.6441 | 69.8490 | 77.4426 | 87.8294 | 111.0775 | 134.0252 | 173.4887 |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | charter | 142 | 0.170579 | 6.3201 | 0.0000 | 19.0046 | 24.3079 | 31.8220 | 34.9245 | 38.7213 | 43.9147 | 55.5387 | 67.0126 | 86.7444 |
| ASSET:BNBUSDT | 1h | tuning | frozen3.0 | maker | 142 | 0.034116 | 6.3201 | 0.0000 | 95.0230 | 121.5397 | 159.1102 | 174.6226 | 193.6064 | 219.5735 | 277.6937 | 335.0629 | 433.7218 |
| ASSET:BNBUSDT | 1h | holdout | calibrated | taker | 176 | 0.133891 | 3.6590 | 0.0000 | 14.1274 | 17.3359 | 20.8127 | 24.6633 | 28.6000 | 34.8081 | 39.3672 | 43.3986 | 57.4710 |
| ASSET:BNBUSDT | 1h | holdout | calibrated | charter | 176 | 0.267782 | 3.6590 | 0.0000 | 7.0637 | 8.6679 | 10.4064 | 12.3317 | 14.3000 | 17.4040 | 19.6836 | 21.6993 | 28.7355 |
| ASSET:BNBUSDT | 1h | holdout | calibrated | maker | 176 | 0.053556 | 3.6590 | 0.0000 | 35.3185 | 43.3397 | 52.0318 | 61.6583 | 71.5001 | 87.0202 | 98.4180 | 108.4964 | 143.6774 |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | taker | 78 | 0.138147 | 7.0099 | 0.0000 | 29.9345 | 33.3990 | 36.4126 | 43.8294 | 48.2008 | 55.2816 | 62.4933 | 76.2966 | 111.6988 |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | charter | 78 | 0.276295 | 7.0099 | 0.0000 | 14.9673 | 16.6995 | 18.2063 | 21.9147 | 24.1004 | 27.6408 | 31.2466 | 38.1483 | 55.8494 |
| ASSET:BNBUSDT | 1h | holdout | frozen3.0 | maker | 78 | 0.055259 | 7.0099 | 0.0000 | 74.8364 | 83.4975 | 91.0316 | 109.5736 | 120.5021 | 138.2040 | 156.2332 | 190.7414 | 279.2471 |
| ASSET:UNIUSDT | 1h | ALL | calibrated | taker | 375 | 0.065234 | 4.3028 | 0.0000 | 36.2962 | 42.1885 | 52.9277 | 59.4555 | 68.1297 | 76.9263 | 93.3789 | 109.6223 | 144.0911 |
| ASSET:UNIUSDT | 1h | ALL | calibrated | charter | 375 | 0.130467 | 4.3028 | 0.0000 | 18.1481 | 21.0943 | 26.4639 | 29.7278 | 34.0649 | 38.4632 | 46.6895 | 54.8112 | 72.0456 |
| ASSET:UNIUSDT | 1h | ALL | calibrated | maker | 375 | 0.026093 | 4.3028 | 0.0000 | 90.7405 | 105.4713 | 132.3193 | 148.6388 | 170.3243 | 192.3159 | 233.4474 | 274.0558 | 360.2278 |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | taker | 182 | 0.064983 | 6.3587 | 0.0000 | 57.3024 | 65.8286 | 72.8142 | 83.7630 | 100.8202 | 113.0814 | 130.9928 | 165.1552 | 224.3631 |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | charter | 182 | 0.129966 | 6.3587 | 0.0000 | 28.6512 | 32.9143 | 36.4071 | 41.8815 | 50.4101 | 56.5407 | 65.4964 | 82.5776 | 112.1816 |
| ASSET:UNIUSDT | 1h | ALL | frozen3.0 | maker | 182 | 0.025993 | 6.3587 | 0.0000 | 143.2560 | 164.5715 | 182.0354 | 209.4076 | 252.0505 | 282.7036 | 327.4819 | 412.8881 | 560.9078 |
| ASSET:UNIUSDT | 1h | tuning | calibrated | taker | 233 | 0.061153 | 4.3677 | 0.0000 | 35.8080 | 44.3303 | 54.8344 | 62.3192 | 69.8131 | 79.3592 | 95.9609 | 121.9134 | 155.7109 |
| ASSET:UNIUSDT | 1h | tuning | calibrated | charter | 233 | 0.122307 | 4.3677 | 0.0000 | 17.9040 | 22.1651 | 27.4172 | 31.1596 | 34.9065 | 39.6796 | 47.9805 | 60.9567 | 77.8555 |
| ASSET:UNIUSDT | 1h | tuning | calibrated | maker | 233 | 0.024461 | 4.3677 | 0.0000 | 89.5200 | 110.8257 | 137.0859 | 155.7979 | 174.5327 | 198.3980 | 239.9023 | 304.7834 | 389.2774 |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | taker | 110 | 0.063446 | 6.2118 | 0.0000 | 56.0986 | 63.8280 | 72.0347 | 81.9349 | 96.3987 | 115.7971 | 142.6642 | 183.2336 | 251.7847 |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | charter | 110 | 0.126893 | 6.2118 | 0.0000 | 28.0493 | 31.9140 | 36.0173 | 40.9675 | 48.1994 | 57.8985 | 71.3321 | 91.6168 | 125.8923 |
| ASSET:UNIUSDT | 1h | tuning | frozen3.0 | maker | 110 | 0.025379 | 6.2118 | 0.0000 | 140.2464 | 159.5700 | 180.0867 | 204.8373 | 240.9969 | 289.4927 | 356.6604 | 458.0840 | 629.4617 |
| ASSET:UNIUSDT | 1h | holdout | calibrated | taker | 142 | 0.070321 | 4.2791 | 0.0000 | 36.7362 | 41.6686 | 49.9366 | 55.6144 | 64.7364 | 72.3913 | 83.8405 | 99.8785 | 126.3715 |
| ASSET:UNIUSDT | 1h | holdout | calibrated | charter | 142 | 0.140642 | 4.2791 | 0.0000 | 18.3681 | 20.8343 | 24.9683 | 27.8072 | 32.3682 | 36.1956 | 41.9202 | 49.9393 | 63.1858 |
| ASSET:UNIUSDT | 1h | holdout | calibrated | maker | 142 | 0.028128 | 4.2791 | 0.0000 | 91.8404 | 104.1716 | 124.8414 | 139.0360 | 161.8411 | 180.9782 | 209.6012 | 249.6964 | 315.9288 |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | taker | 72 | 0.067711 | 6.6104 | 0.0000 | 58.4027 | 68.1521 | 78.4636 | 97.0043 | 102.2300 | 111.4145 | 127.4965 | 140.8643 | 178.2504 |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | charter | 72 | 0.135422 | 6.6104 | 0.0000 | 29.2013 | 34.0760 | 39.2318 | 48.5021 | 51.1150 | 55.7073 | 63.7482 | 70.4321 | 89.1252 |
| ASSET:UNIUSDT | 1h | holdout | frozen3.0 | maker | 72 | 0.027084 | 6.6104 | 0.0000 | 146.0067 | 170.3802 | 196.1591 | 242.5107 | 255.5749 | 278.5363 | 318.7412 | 352.1607 | 445.6259 |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | taker | 224 | 0.059070 | 3.4777 | 0.0000 | 34.3510 | 42.5290 | 49.9071 | 57.7184 | 64.1908 | 73.5874 | 88.8521 | 107.4456 | 147.9195 |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | charter | 224 | 0.177211 | 3.4777 | 0.0000 | 11.4503 | 14.1763 | 16.6357 | 19.2395 | 21.3969 | 24.5291 | 29.6174 | 35.8152 | 49.3065 |
| ASSET:1000PEPEUSDT | 1h | ALL | calibrated | maker | 224 | 0.023628 | 3.4777 | 0.0000 | 85.8776 | 106.3226 | 124.7677 | 144.2959 | 160.4771 | 183.9685 | 222.1302 | 268.6141 | 369.7987 |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | taker | 104 | 0.056556 | 6.2984 | 0.0000 | 67.8673 | 79.7705 | 89.5978 | 104.9462 | 118.9956 | 137.1959 | 159.5379 | 182.5117 | 232.3305 |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | charter | 104 | 0.169668 | 6.2984 | 0.0000 | 22.6224 | 26.5902 | 29.8659 | 34.9821 | 39.6652 | 45.7320 | 53.1793 | 60.8372 | 77.4435 |
| ASSET:1000PEPEUSDT | 1h | ALL | frozen3.0 | maker | 104 | 0.022622 | 6.2984 | 0.0000 | 169.6683 | 199.4263 | 223.9946 | 262.3654 | 297.4889 | 342.9897 | 398.8447 | 456.2792 | 580.8262 |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | taker | 76 | 0.046633 | 3.4578 | 0.0000 | 35.9106 | 48.4464 | 55.4236 | 61.4598 | 79.4043 | 87.3954 | 101.1832 | 130.3194 | 200.6954 |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | charter | 76 | 0.139900 | 3.4578 | 0.0000 | 11.9702 | 16.1488 | 18.4745 | 20.4866 | 26.4681 | 29.1318 | 33.7277 | 43.4398 | 66.8985 |
| ASSET:1000PEPEUSDT | 1h | tuning | calibrated | maker | 76 | 0.018653 | 3.4578 | 0.0000 | 89.7765 | 121.1160 | 138.5589 | 153.6495 | 198.5108 | 218.4884 | 252.9580 | 325.7984 | 501.7385 |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | taker | 36 | 0.044669 | 5.5751 | 0.0000 | 61.1155 | 84.0900 | 114.2532 | 126.0011 | 147.3739 | 159.7550 | 179.3392 | 212.9368 | 264.0392 |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | charter | 36 | 0.134006 | 5.5751 | 0.0000 | 20.3718 | 28.0300 | 38.0844 | 42.0004 | 49.1246 | 53.2517 | 59.7797 | 70.9789 | 88.0131 |
| ASSET:1000PEPEUSDT | 1h | tuning | frozen3.0 | maker | 36 | 0.017868 | 5.5751 | 0.0000 | 152.7887 | 210.2251 | 285.6330 | 315.0027 | 368.4348 | 399.3875 | 448.3481 | 532.3419 | 660.0980 |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | taker | 148 | 0.064035 | 3.5463 | 0.0000 | 33.1892 | 40.4656 | 46.9940 | 54.5336 | 62.0862 | 69.3483 | 83.7460 | 98.9940 | 132.4253 |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | charter | 148 | 0.192106 | 3.5463 | 0.0000 | 11.0631 | 13.4885 | 15.6647 | 18.1779 | 20.6954 | 23.1161 | 27.9153 | 32.9980 | 44.1418 |
| ASSET:1000PEPEUSDT | 1h | holdout | calibrated | maker | 148 | 0.025614 | 3.5463 | 0.0000 | 82.9730 | 101.1639 | 117.4850 | 136.3340 | 155.2156 | 173.3709 | 209.3649 | 247.4851 | 331.0634 |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | taker | 68 | 0.061874 | 6.4090 | 0.0000 | 71.6446 | 78.8285 | 88.1000 | 97.3707 | 109.2987 | 120.5144 | 141.8489 | 166.4968 | 201.3343 |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | charter | 68 | 0.185623 | 6.4090 | 0.0000 | 23.8815 | 26.2762 | 29.3667 | 32.4569 | 36.4329 | 40.1715 | 47.2830 | 55.4989 | 67.1114 |
| ASSET:1000PEPEUSDT | 1h | holdout | frozen3.0 | maker | 68 | 0.024750 | 6.4090 | 0.0000 | 179.1115 | 197.0712 | 220.2499 | 243.4268 | 273.2468 | 301.2859 | 354.6222 | 416.2419 | 503.3358 |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | taker | 399 | 0.072396 | 3.7418 | 0.0000 | 24.6325 | 31.9060 | 39.3763 | 46.4097 | 53.6179 | 61.5592 | 72.7739 | 93.1330 | 150.5509 |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | charter | 399 | 0.144792 | 3.7418 | 0.0000 | 12.3162 | 15.9530 | 19.6881 | 23.2048 | 26.8090 | 30.7796 | 36.3869 | 46.5665 | 75.2755 |
| ASSET:DOGEUSDT | 1h | ALL | calibrated | maker | 399 | 0.028958 | 3.7418 | 0.0000 | 61.5812 | 79.7650 | 98.4407 | 116.0241 | 134.0449 | 153.8981 | 181.9347 | 232.8325 | 376.3773 |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | taker | 182 | 0.072718 | 6.2800 | 0.0000 | 46.3928 | 56.4700 | 65.8275 | 77.1916 | 93.5651 | 109.3607 | 124.3373 | 165.5129 | 242.9107 |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | charter | 182 | 0.145437 | 6.2800 | 0.0000 | 23.1964 | 28.2350 | 32.9137 | 38.5958 | 46.7826 | 54.6803 | 62.1687 | 82.7564 | 121.4553 |
| ASSET:DOGEUSDT | 1h | ALL | frozen3.0 | maker | 182 | 0.029087 | 6.2800 | 0.0000 | 115.9821 | 141.1749 | 164.5687 | 192.9791 | 233.9128 | 273.4017 | 310.8434 | 413.7822 | 607.2767 |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | taker | 243 | 0.066348 | 3.6558 | 0.0000 | 23.7048 | 32.0648 | 40.4333 | 47.3773 | 54.8727 | 68.6799 | 80.6916 | 113.1123 | 170.1659 |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | charter | 243 | 0.132696 | 3.6558 | 0.0000 | 11.8524 | 16.0324 | 20.2167 | 23.6886 | 27.4363 | 34.3399 | 40.3458 | 56.5562 | 85.0830 |
| ASSET:DOGEUSDT | 1h | tuning | calibrated | maker | 243 | 0.026539 | 3.6558 | 0.0000 | 59.2621 | 80.1619 | 101.0833 | 118.4431 | 137.1817 | 171.6997 | 201.7290 | 282.7808 | 425.4148 |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | taker | 107 | 0.061149 | 5.8193 | 0.0000 | 45.7868 | 56.1513 | 68.4374 | 83.0518 | 102.4758 | 117.0546 | 146.6894 | 195.2952 | 278.4502 |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | charter | 107 | 0.122298 | 5.8193 | 0.0000 | 22.8934 | 28.0757 | 34.2187 | 41.5259 | 51.2379 | 58.5273 | 73.3447 | 97.6476 | 139.2251 |
| ASSET:DOGEUSDT | 1h | tuning | frozen3.0 | maker | 107 | 0.024460 | 5.8193 | 0.0000 | 114.4671 | 140.3783 | 171.0935 | 207.6295 | 256.1896 | 292.6365 | 366.7234 | 488.2380 | 696.1254 |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | taker | 156 | 0.079773 | 3.9729 | 0.0000 | 25.0248 | 31.6775 | 38.5500 | 45.0753 | 51.8086 | 57.4590 | 65.7496 | 76.0116 | 110.1565 |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | charter | 156 | 0.159546 | 3.9729 | 0.0000 | 12.5124 | 15.8388 | 19.2750 | 22.5377 | 25.9043 | 28.7295 | 32.8748 | 38.0058 | 55.0782 |
| ASSET:DOGEUSDT | 1h | holdout | calibrated | maker | 156 | 0.031909 | 3.9729 | 0.0000 | 62.5619 | 79.1938 | 96.3751 | 112.6883 | 129.5216 | 143.6475 | 164.3741 | 190.0290 | 275.3912 |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | taker | 75 | 0.079371 | 6.7605 | 0.0000 | 51.2268 | 56.9419 | 63.1399 | 73.2425 | 85.8830 | 98.3597 | 113.5917 | 142.2244 | 177.4393 |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | charter | 75 | 0.158742 | 6.7605 | 0.0000 | 25.6134 | 28.4710 | 31.5700 | 36.6213 | 42.9415 | 49.1799 | 56.7958 | 71.1122 | 88.7197 |
| ASSET:DOGEUSDT | 1h | holdout | frozen3.0 | maker | 75 | 0.031748 | 6.7605 | 0.0000 | 128.0671 | 142.3549 | 157.8498 | 183.1064 | 214.7075 | 245.8993 | 283.9792 | 355.5610 | 443.5983 |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | taker | 174 | 0.051636 | 4.3591 | 0.0000 | 45.6968 | 56.0643 | 66.4999 | 80.1326 | 94.3147 | 106.4890 | 128.0243 | 152.1909 | 200.4683 |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | charter | 174 | 0.154909 | 4.3591 | 0.0000 | 15.2323 | 18.6881 | 22.1666 | 26.7109 | 31.4382 | 35.4963 | 42.6748 | 50.7303 | 66.8228 |
| ASSET:1000BONKUSDT | 1h | ALL | calibrated | maker | 174 | 0.020655 | 4.3591 | 0.0000 | 114.2420 | 140.1607 | 166.2497 | 200.3314 | 235.7868 | 266.2226 | 320.0607 | 380.4774 | 501.1708 |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | taker | 90 | 0.050864 | 7.1383 | 0.0000 | 70.8549 | 96.7774 | 116.3812 | 127.1416 | 145.6863 | 170.3881 | 187.8706 | 236.7077 | 275.9568 |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | charter | 90 | 0.152591 | 7.1383 | 0.0000 | 23.6183 | 32.2591 | 38.7937 | 42.3805 | 48.5621 | 56.7960 | 62.6235 | 78.9026 | 91.9856 |
| ASSET:1000BONKUSDT | 1h | ALL | frozen3.0 | maker | 90 | 0.020345 | 7.1383 | 0.0000 | 177.1373 | 241.9434 | 290.9529 | 317.8540 | 364.2158 | 425.9703 | 469.6765 | 591.7694 | 689.8919 |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | taker | 42 | 0.039926 | 4.3088 | 0.0000 | 61.5601 | 79.0765 | 97.3847 | 107.8111 | 125.0080 | 152.4298 | 170.2840 | 207.1237 | 248.0866 |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | charter | 42 | 0.119779 | 4.3088 | 0.0000 | 20.5200 | 26.3588 | 32.4616 | 35.9370 | 41.6693 | 50.8099 | 56.7613 | 69.0412 | 82.6955 |
| ASSET:1000BONKUSDT | 1h | tuning | calibrated | maker | 42 | 0.015971 | 4.3088 | 0.0000 | 153.9001 | 197.6913 | 243.4618 | 269.5277 | 312.5199 | 381.0745 | 425.7099 | 517.8094 | 620.2165 |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | taker | 22 | 0.039629 | 6.8201 | 0.0000 | 97.7220 | 116.7873 | 139.2052 | 170.3881 | 174.7779 | 207.2423 | 233.1664 | 259.2246 | 293.2764 |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | charter | 22 | 0.118888 | 6.8201 | 0.0000 | 32.5740 | 38.9291 | 46.4017 | 56.7960 | 58.2593 | 69.0808 | 77.7221 | 86.4082 | 97.7588 |
| ASSET:1000BONKUSDT | 1h | tuning | frozen3.0 | maker | 22 | 0.015852 | 6.8201 | 0.0000 | 244.3050 | 291.9684 | 348.0130 | 425.9703 | 436.9448 | 518.1057 | 582.9161 | 648.0615 | 733.1911 |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | taker | 132 | 0.055289 | 4.4290 | 0.0000 | 42.2771 | 53.3952 | 60.3159 | 70.7240 | 84.2757 | 97.7535 | 110.0631 | 135.0335 | 166.7212 |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | charter | 132 | 0.165867 | 4.4290 | 0.0000 | 14.0924 | 17.7984 | 20.1053 | 23.5747 | 28.0919 | 32.5845 | 36.6877 | 45.0112 | 55.5737 |
| ASSET:1000BONKUSDT | 1h | holdout | calibrated | maker | 132 | 0.022116 | 4.4290 | 0.0000 | 105.6928 | 133.4881 | 150.7899 | 176.8100 | 210.6893 | 244.3837 | 275.1579 | 337.5837 | 416.8031 |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | taker | 68 | 0.054810 | 7.7023 | 0.0000 | 68.8058 | 92.4789 | 112.2209 | 122.8505 | 139.3024 | 154.2082 | 178.1340 | 223.4087 | 268.9077 |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | charter | 68 | 0.164431 | 7.7023 | 0.0000 | 22.9353 | 30.8263 | 37.4070 | 40.9502 | 46.4341 | 51.4027 | 59.3780 | 74.4696 | 89.6359 |
| ASSET:1000BONKUSDT | 1h | holdout | frozen3.0 | maker | 68 | 0.021924 | 7.7023 | 0.0000 | 172.0146 | 231.1971 | 280.5524 | 307.1262 | 348.2559 | 385.5206 | 445.3349 | 558.5216 | 672.2692 |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | taker | 2253 | 0.077514 | 3.8820 | 0.0000 | 20.9303 | 29.1773 | 36.5811 | 43.5194 | 51.5959 | 61.3554 | 74.4024 | 91.4819 | 122.5322 |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | charter | 2253 | 0.134668 | 3.8820 | 0.0000 | 13.3432 | 17.4452 | 21.6069 | 25.4818 | 30.1766 | 35.3661 | 41.4918 | 50.1202 | 65.8592 |
| POOLED:CLASSIC5 | 1h | ALL | calibrated | maker | 2253 | 0.031005 | 3.8820 | 0.0000 | 52.3257 | 72.9432 | 91.4528 | 108.7985 | 128.9898 | 153.3884 | 186.0061 | 228.7048 | 306.3305 |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | taker | 1088 | 0.078004 | 6.3262 | 0.0000 | 38.4466 | 50.3248 | 60.1220 | 72.1416 | 84.7372 | 102.6829 | 121.9322 | 153.3788 | 199.7252 |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | charter | 1088 | 0.135543 | 6.3262 | 0.0000 | 24.4218 | 30.3160 | 36.2691 | 42.3687 | 49.6543 | 57.9682 | 69.1737 | 83.3721 | 108.2695 |
| POOLED:CLASSIC5 | 1h | ALL | frozen3.0 | maker | 1088 | 0.031202 | 6.3262 | 0.0000 | 96.1165 | 125.8119 | 150.3051 | 180.3539 | 211.8431 | 256.7072 | 304.8304 | 383.4471 | 499.3131 |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | taker | 1437 | 0.071549 | 3.8218 | 0.0000 | 21.3429 | 30.3231 | 37.6780 | 46.0746 | 55.5195 | 66.0532 | 79.9609 | 98.0280 | 131.6271 |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | charter | 1437 | 0.124792 | 3.8218 | 0.0000 | 13.5293 | 17.9452 | 22.7366 | 27.5515 | 32.5917 | 38.1049 | 44.8636 | 55.0822 | 72.1226 |
| POOLED:CLASSIC5 | 1h | tuning | calibrated | maker | 1437 | 0.028620 | 3.8218 | 0.0000 | 53.3573 | 75.8078 | 94.1949 | 115.1864 | 138.7987 | 165.1330 | 199.9023 | 245.0700 | 329.0678 |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | taker | 712 | 0.074436 | 6.1761 | 0.0000 | 38.3670 | 50.9540 | 60.9632 | 74.6677 | 87.7624 | 106.5978 | 128.7743 | 161.8738 | 213.4409 |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | charter | 712 | 0.125873 | 6.1761 | 0.0000 | 24.4711 | 30.5449 | 37.1094 | 43.8365 | 52.1662 | 60.6016 | 73.7762 | 87.1731 | 118.4144 |
| POOLED:CLASSIC5 | 1h | tuning | frozen3.0 | maker | 712 | 0.029774 | 6.1761 | 0.0000 | 95.9176 | 127.3850 | 152.4079 | 186.6693 | 219.4059 | 266.4944 | 321.9358 | 404.6844 | 533.6024 |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | taker | 816 | 0.086449 | 3.9403 | 0.0000 | 19.8962 | 28.1062 | 34.7004 | 41.6550 | 46.2355 | 53.7310 | 64.7407 | 80.2111 | 103.1556 |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | charter | 816 | 0.153598 | 3.9403 | 0.0000 | 12.7422 | 16.4781 | 20.1109 | 22.9162 | 26.2699 | 30.8452 | 35.7352 | 42.5371 | 56.3385 |
| POOLED:CLASSIC5 | 1h | holdout | calibrated | maker | 816 | 0.034579 | 3.9403 | 0.0000 | 49.7405 | 70.2656 | 86.7509 | 104.1376 | 115.5889 | 134.3276 | 161.8517 | 200.5277 | 257.8889 |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | taker | 376 | 0.083983 | 6.6092 | 0.0000 | 38.6912 | 46.5713 | 57.3442 | 69.5611 | 80.1212 | 94.4096 | 113.7758 | 138.2593 | 173.9942 |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | charter | 376 | 0.151277 | 6.6092 | 0.0000 | 23.9267 | 29.9774 | 35.1093 | 39.8565 | 46.1878 | 52.5347 | 61.3162 | 74.7237 | 89.4222 |
| POOLED:CLASSIC5 | 1h | holdout | frozen3.0 | maker | 376 | 0.033593 | 6.6092 | 0.0000 | 96.7280 | 116.4282 | 143.3604 | 173.9027 | 200.3031 | 236.0240 | 284.4394 | 345.6482 | 434.9854 |
| POOLED:PANEL17 | 1h | ALL | calibrated | taker | 5582 | 0.073842 | 3.8396 | 0.0000 | 22.2592 | 30.7950 | 37.8732 | 45.1642 | 53.6643 | 63.3453 | 75.6600 | 94.0451 | 128.8000 |
| POOLED:PANEL17 | 1h | ALL | calibrated | charter | 5582 | 0.148727 | 3.8396 | 0.0000 | 11.4712 | 15.4553 | 18.8487 | 22.3710 | 26.4129 | 31.1838 | 37.2675 | 45.8123 | 61.7390 |
| POOLED:PANEL17 | 1h | ALL | calibrated | maker | 5582 | 0.029537 | 3.8396 | 0.0000 | 55.6479 | 76.9874 | 94.6829 | 112.9105 | 134.1607 | 158.3633 | 189.1499 | 235.1128 | 321.9999 |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | taker | 2621 | 0.075222 | 6.4663 | 0.0000 | 42.7553 | 55.0147 | 65.8762 | 77.0862 | 91.1430 | 107.7229 | 126.3982 | 156.8595 | 207.5997 |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | charter | 2621 | 0.151411 | 6.4663 | 0.0000 | 22.1423 | 27.9579 | 33.2694 | 38.6021 | 44.8080 | 51.9120 | 61.3528 | 75.7855 | 98.2063 |
| POOLED:PANEL17 | 1h | ALL | frozen3.0 | maker | 2621 | 0.030089 | 6.4663 | 0.0000 | 106.8884 | 137.5368 | 164.6904 | 192.7155 | 227.8576 | 269.3073 | 315.9955 | 392.1487 | 518.9992 |
| POOLED:PANEL17 | 1h | tuning | calibrated | taker | 3079 | 0.070780 | 3.7395 | 0.0000 | 21.6735 | 30.2873 | 37.5081 | 45.6832 | 54.3181 | 65.1259 | 78.2161 | 97.4021 | 134.1134 |
| POOLED:PANEL17 | 1h | tuning | calibrated | charter | 3079 | 0.134668 | 3.7395 | 0.0000 | 11.8025 | 16.1004 | 19.9268 | 24.3222 | 28.6309 | 34.3262 | 40.8167 | 50.2860 | 68.0652 |
| POOLED:PANEL17 | 1h | tuning | calibrated | maker | 3079 | 0.028312 | 3.7395 | 0.0000 | 54.1838 | 75.7183 | 93.7704 | 114.2079 | 135.7953 | 162.8147 | 195.5401 | 243.5052 | 335.2834 |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | taker | 1459 | 0.072502 | 6.1964 | 0.0000 | 42.7860 | 54.8068 | 65.5243 | 76.9138 | 89.7553 | 107.8151 | 129.3376 | 160.7703 | 219.0810 |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | charter | 1459 | 0.137206 | 6.1964 | 0.0000 | 23.1420 | 29.0110 | 34.6340 | 40.5513 | 47.5352 | 56.0140 | 66.2552 | 82.0038 | 110.6223 |
| POOLED:PANEL17 | 1h | tuning | frozen3.0 | maker | 1459 | 0.029001 | 6.1964 | 0.0000 | 106.9651 | 137.0171 | 163.8109 | 192.2845 | 224.3883 | 269.5378 | 323.3440 | 401.9259 | 547.7025 |
| POOLED:PANEL17 | 1h | holdout | calibrated | taker | 2503 | 0.076667 | 3.9582 | 0.0000 | 22.8138 | 31.2524 | 38.1828 | 44.5067 | 52.9644 | 61.5178 | 73.1560 | 90.1446 | 120.6485 |
| POOLED:PANEL17 | 1h | holdout | calibrated | charter | 2503 | 0.165127 | 3.9582 | 0.0000 | 11.2565 | 14.7403 | 18.1144 | 20.9501 | 24.0154 | 27.6682 | 32.9805 | 40.2380 | 53.6389 |
| POOLED:PANEL17 | 1h | holdout | calibrated | maker | 2503 | 0.030667 | 3.9582 | 0.0000 | 57.0345 | 78.1311 | 95.4570 | 111.2667 | 132.4111 | 153.7944 | 182.8901 | 225.3615 | 301.6213 |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | taker | 1162 | 0.077155 | 6.8428 | 0.0000 | 42.7565 | 55.3657 | 67.0302 | 77.4181 | 93.0564 | 107.6776 | 124.2250 | 151.9182 | 196.2155 |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | charter | 1162 | 0.166671 | 6.8428 | 0.0000 | 21.0715 | 26.7745 | 31.5951 | 36.7382 | 41.7345 | 48.4374 | 56.4229 | 67.2403 | 86.7106 |
| POOLED:PANEL17 | 1h | holdout | frozen3.0 | maker | 1162 | 0.030862 | 6.8428 | 0.0000 | 106.8913 | 138.4142 | 167.5755 | 193.5454 | 232.6409 | 269.1939 | 310.5626 | 379.7955 | 490.5387 |
| ASSET:BTCUSDT | 4h | ALL | calibrated | taker | 111 | 0.064864 | 4.1489 | 0.0000 | 35.8418 | 42.5833 | 51.6130 | 61.5410 | 69.4022 | 79.4007 | 89.2030 | 102.4603 | 141.9375 |
| ASSET:BTCUSDT | 4h | ALL | calibrated | charter | 111 | 0.090810 | 4.1489 | 0.0000 | 25.6013 | 30.4166 | 36.8664 | 43.9579 | 49.5730 | 56.7148 | 63.7164 | 73.1859 | 101.3839 |
| ASSET:BTCUSDT | 4h | ALL | calibrated | maker | 111 | 0.025946 | 4.1489 | 0.0000 | 89.6046 | 106.4583 | 129.0324 | 153.8525 | 173.5054 | 198.5018 | 223.0075 | 256.1508 | 354.8437 |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | taker | 63 | 0.065108 | 6.5593 | 0.0000 | 57.9195 | 70.4646 | 80.1027 | 89.6178 | 98.1620 | 114.0531 | 144.1942 | 168.9234 | 223.5779 |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | charter | 63 | 0.091151 | 6.5593 | 0.0000 | 41.3711 | 50.3319 | 57.2162 | 64.0127 | 70.1157 | 81.4665 | 102.9959 | 120.6595 | 159.6985 |
| ASSET:BTCUSDT | 4h | ALL | frozen3.0 | maker | 63 | 0.026043 | 6.5593 | 0.0000 | 144.7988 | 176.1615 | 200.2568 | 224.0446 | 245.4049 | 285.1328 | 360.4856 | 422.3084 | 558.9448 |
| ASSET:BTCUSDT | 4h | tuning | calibrated | taker | 77 | 0.058277 | 4.1094 | 0.0000 | 37.3089 | 46.7932 | 57.4397 | 64.7911 | 72.7608 | 85.4676 | 92.2799 | 107.3138 | 144.1033 |
| ASSET:BTCUSDT | 4h | tuning | calibrated | charter | 77 | 0.081588 | 4.1094 | 0.0000 | 26.6492 | 33.4237 | 41.0284 | 46.2793 | 51.9720 | 61.0483 | 65.9142 | 76.6527 | 102.9310 |
| ASSET:BTCUSDT | 4h | tuning | calibrated | maker | 77 | 0.023311 | 4.1094 | 0.0000 | 93.2723 | 116.9830 | 143.5993 | 161.9777 | 181.9020 | 213.6690 | 230.6997 | 268.2846 | 360.2583 |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | taker | 40 | 0.061041 | 6.1367 | 0.0000 | 57.1945 | 76.4000 | 81.0576 | 96.0911 | 106.5000 | 144.1942 | 165.0235 | 204.4700 | 244.9255 |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | charter | 40 | 0.085457 | 6.1367 | 0.0000 | 40.8532 | 54.5714 | 57.8983 | 68.6365 | 76.0714 | 102.9959 | 117.8739 | 146.0500 | 174.9468 |
| ASSET:BTCUSDT | 4h | tuning | frozen3.0 | maker | 40 | 0.024416 | 6.1367 | 0.0000 | 142.9863 | 191.0001 | 202.6440 | 240.2277 | 266.2501 | 360.4856 | 412.5586 | 511.1751 | 612.3138 |
| ASSET:BTCUSDT | 4h | holdout | calibrated | taker | 34 | 0.077308 | 4.2782 | 0.0000 | 35.5186 | 37.6644 | 45.5757 | 54.0328 | 64.3650 | 74.3693 | 77.4981 | 83.3275 | 110.2363 |
| ASSET:BTCUSDT | 4h | holdout | calibrated | charter | 34 | 0.108232 | 4.2782 | 0.0000 | 25.3704 | 26.9031 | 32.5541 | 38.5949 | 45.9750 | 53.1210 | 55.3558 | 59.5196 | 78.7402 |
| ASSET:BTCUSDT | 4h | holdout | calibrated | maker | 34 | 0.030923 | 4.2782 | 0.0000 | 88.7965 | 94.1610 | 113.9392 | 135.0820 | 160.9125 | 185.9234 | 193.7452 | 208.3188 | 275.5908 |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | taker | 23 | 0.078848 | 7.0607 | 0.0000 | 59.3568 | 66.5291 | 75.7049 | 83.3680 | 91.2719 | 96.7216 | 103.2359 | 132.2204 | 163.2279 |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | charter | 23 | 0.110387 | 7.0607 | 0.0000 | 42.3977 | 47.5208 | 54.0749 | 59.5486 | 65.1942 | 69.0869 | 73.7400 | 94.4431 | 116.5913 |
| ASSET:BTCUSDT | 4h | holdout | frozen3.0 | maker | 23 | 0.031539 | 7.0607 | 0.0000 | 148.3920 | 166.3228 | 189.2622 | 208.4201 | 228.1796 | 241.8041 | 258.0898 | 330.5510 | 408.0697 |
| ASSET:ETHUSDT | 4h | ALL | calibrated | taker | 113 | 0.048349 | 4.0348 | 0.0000 | 48.4171 | 57.6437 | 69.8843 | 79.1540 | 95.0860 | 111.3530 | 126.3640 | 155.2133 | 194.4489 |
| ASSET:ETHUSDT | 4h | ALL | calibrated | charter | 113 | 0.067689 | 4.0348 | 0.0000 | 34.5836 | 41.1741 | 49.9174 | 56.5385 | 67.9185 | 79.5379 | 90.2600 | 110.8666 | 138.8921 |
| ASSET:ETHUSDT | 4h | ALL | calibrated | maker | 113 | 0.019340 | 4.0348 | 0.0000 | 121.0428 | 144.1093 | 174.7109 | 197.8849 | 237.7149 | 278.3826 | 315.9099 | 388.0331 | 486.1223 |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | taker | 63 | 0.051038 | 6.3054 | 0.0000 | 84.9727 | 106.0401 | 119.4314 | 131.3690 | 143.3778 | 158.7585 | 176.3501 | 200.3509 | 240.0623 |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | charter | 63 | 0.071454 | 6.3054 | 0.0000 | 60.6948 | 75.7430 | 85.3082 | 93.8350 | 102.4127 | 113.3989 | 125.9644 | 143.1078 | 171.4730 |
| ASSET:ETHUSDT | 4h | ALL | frozen3.0 | maker | 63 | 0.020415 | 6.3054 | 0.0000 | 212.4316 | 265.1004 | 298.5786 | 328.4226 | 358.4445 | 396.8963 | 440.8753 | 500.8773 | 600.1556 |
| ASSET:ETHUSDT | 4h | tuning | calibrated | taker | 74 | 0.044847 | 3.9783 | 0.0000 | 46.5313 | 59.7115 | 70.2836 | 76.4671 | 91.0243 | 112.3767 | 125.5289 | 161.9809 | 200.8960 |
| ASSET:ETHUSDT | 4h | tuning | calibrated | charter | 74 | 0.062786 | 3.9783 | 0.0000 | 33.2367 | 42.6511 | 50.2026 | 54.6193 | 65.0174 | 80.2691 | 89.6635 | 115.7007 | 143.4971 |
| ASSET:ETHUSDT | 4h | tuning | calibrated | maker | 74 | 0.017939 | 3.9783 | 0.0000 | 116.3284 | 149.2788 | 175.7090 | 191.1677 | 227.5607 | 280.9418 | 313.8222 | 404.9523 | 502.2400 |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | taker | 42 | 0.044847 | 5.8855 | 0.0000 | 84.5790 | 98.4927 | 113.8501 | 127.3252 | 146.0934 | 156.4320 | 172.1264 | 201.4255 | 250.8035 |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | charter | 42 | 0.062786 | 5.8855 | 0.0000 | 60.4136 | 70.3519 | 81.3215 | 90.9466 | 104.3524 | 111.7372 | 122.9474 | 143.8754 | 179.1454 |
| ASSET:ETHUSDT | 4h | tuning | frozen3.0 | maker | 42 | 0.017939 | 5.8855 | 0.0000 | 211.4475 | 246.2316 | 284.6251 | 318.3129 | 365.2335 | 391.0801 | 430.3160 | 503.5638 | 627.0089 |
| ASSET:ETHUSDT | 4h | holdout | calibrated | taker | 39 | 0.051298 | 4.1570 | 0.0000 | 50.1460 | 57.1395 | 66.1019 | 81.3677 | 95.3059 | 106.3800 | 125.4769 | 136.9059 | 178.3333 |
| ASSET:ETHUSDT | 4h | holdout | calibrated | charter | 39 | 0.071818 | 4.1570 | 0.0000 | 35.8186 | 40.8139 | 47.2156 | 58.1198 | 68.0756 | 75.9857 | 89.6264 | 97.7899 | 127.3809 |
| ASSET:ETHUSDT | 4h | holdout | calibrated | maker | 39 | 0.020519 | 4.1570 | 0.0000 | 125.3651 | 142.8487 | 165.2547 | 203.4193 | 238.2647 | 265.9501 | 313.6923 | 342.2648 | 445.8332 |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | taker | 21 | 0.055057 | 6.8158 | 0.0000 | 88.3537 | 117.7772 | 130.2661 | 138.4790 | 140.3066 | 161.6602 | 177.0096 | 178.8636 | 209.5803 |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | charter | 21 | 0.077080 | 6.8158 | 0.0000 | 63.1098 | 84.1265 | 93.0472 | 98.9136 | 100.2190 | 115.4716 | 126.4354 | 127.7597 | 149.7002 |
| ASSET:ETHUSDT | 4h | holdout | frozen3.0 | maker | 21 | 0.022023 | 6.8158 | 0.0000 | 220.8842 | 294.4429 | 325.6652 | 346.1975 | 350.7665 | 404.1506 | 442.5239 | 447.1590 | 523.9508 |
| ASSET:SOLUSDT | 4h | ALL | calibrated | taker | 88 | 0.033088 | 4.6090 | 0.0000 | 79.2996 | 90.9412 | 104.5959 | 124.6150 | 146.3951 | 166.2494 | 208.0497 | 244.5461 | 282.8490 |
| ASSET:SOLUSDT | 4h | ALL | calibrated | charter | 88 | 0.066176 | 4.6090 | 0.0000 | 39.6498 | 45.4706 | 52.2980 | 62.3075 | 73.1975 | 83.1247 | 104.0248 | 122.2730 | 141.4245 |
| ASSET:SOLUSDT | 4h | ALL | calibrated | maker | 88 | 0.013235 | 4.6090 | 0.0000 | 198.2489 | 227.3531 | 261.4898 | 311.5375 | 365.9877 | 415.6234 | 520.1242 | 611.3652 | 707.1224 |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | taker | 53 | 0.034940 | 6.2607 | 0.0000 | 112.8997 | 137.8720 | 169.8348 | 196.2068 | 221.8464 | 239.7639 | 268.7052 | 328.9758 | 396.7852 |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | charter | 53 | 0.069881 | 6.2607 | 0.0000 | 56.4499 | 68.9360 | 84.9174 | 98.1034 | 110.9232 | 119.8819 | 134.3526 | 164.4879 | 198.3926 |
| ASSET:SOLUSDT | 4h | ALL | frozen3.0 | maker | 53 | 0.013976 | 6.2607 | 0.0000 | 282.2493 | 344.6799 | 424.5870 | 490.5170 | 554.6160 | 599.4097 | 671.7630 | 822.4394 | 991.9629 |
| ASSET:SOLUSDT | 4h | tuning | calibrated | taker | 59 | 0.025789 | 5.2400 | 0.0000 | 92.0196 | 109.6582 | 132.0991 | 150.5640 | 165.5595 | 205.0608 | 240.3750 | 261.4777 | 296.5786 |
| ASSET:SOLUSDT | 4h | tuning | calibrated | charter | 59 | 0.051579 | 5.2400 | 0.0000 | 46.0098 | 54.8291 | 66.0495 | 75.2820 | 82.7798 | 102.5304 | 120.1875 | 130.7389 | 148.2893 |
| ASSET:SOLUSDT | 4h | tuning | calibrated | maker | 59 | 0.010316 | 5.2400 | 0.0000 | 230.0489 | 274.1455 | 330.2476 | 376.4100 | 413.8989 | 512.6521 | 600.9375 | 653.6943 | 741.4464 |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | taker | 39 | 0.031183 | 6.1258 | 0.0000 | 129.9204 | 151.8556 | 177.0658 | 201.5347 | 221.8464 | 241.7738 | 268.9340 | 329.4670 | 374.7231 |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | charter | 39 | 0.062366 | 6.1258 | 0.0000 | 64.9602 | 75.9278 | 88.5329 | 100.7674 | 110.9232 | 120.8869 | 134.4670 | 164.7335 | 187.3615 |
| ASSET:SOLUSDT | 4h | tuning | frozen3.0 | maker | 39 | 0.012473 | 6.1258 | 0.0000 | 324.8010 | 379.6390 | 442.6644 | 503.8368 | 554.6160 | 604.4344 | 672.3351 | 823.6674 | 936.8077 |
| ASSET:SOLUSDT | 4h | holdout | calibrated | taker | 29 | 0.044191 | 4.2034 | 0.0000 | 66.7411 | 75.0644 | 81.7495 | 87.3328 | 96.0908 | 110.2252 | 134.3131 | 161.9239 | 198.4967 |
| ASSET:SOLUSDT | 4h | holdout | calibrated | charter | 29 | 0.088383 | 4.2034 | 0.0000 | 33.3706 | 37.5322 | 40.8748 | 43.6664 | 48.0454 | 55.1126 | 67.1565 | 80.9620 | 99.2484 |
| ASSET:SOLUSDT | 4h | holdout | calibrated | maker | 29 | 0.017677 | 4.2034 | 0.0000 | 166.8528 | 187.6610 | 204.3739 | 218.3320 | 240.2269 | 275.5630 | 335.7827 | 404.8098 | 496.2418 |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | taker | 14 | 0.038998 | 7.3253 | 0.0000 | 92.1570 | 117.1728 | 132.0203 | 186.8286 | 218.5260 | 235.7078 | 248.1165 | 294.6923 | 479.3181 |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | charter | 14 | 0.077997 | 7.3253 | 0.0000 | 46.0785 | 58.5864 | 66.0101 | 93.4143 | 109.2630 | 117.8539 | 124.0582 | 147.3462 | 239.6591 |
| ASSET:SOLUSDT | 4h | holdout | frozen3.0 | maker | 14 | 0.015599 | 7.3253 | 0.0000 | 230.3924 | 292.9319 | 330.0507 | 467.0716 | 546.3151 | 589.2695 | 620.2912 | 736.7308 | 1198.2952 |
| ASSET:NEARUSDT | 4h | ALL | calibrated | taker | 112 | 0.027729 | 3.7012 | 0.0000 | 70.2517 | 84.6693 | 109.2864 | 125.1354 | 140.5561 | 160.3120 | 194.6089 | 240.1738 | 308.3686 |
| ASSET:NEARUSDT | 4h | ALL | calibrated | charter | 112 | 0.055458 | 3.7012 | 0.0000 | 35.1259 | 42.3346 | 54.6432 | 62.5677 | 70.2780 | 80.1560 | 97.3044 | 120.0869 | 154.1843 |
| ASSET:NEARUSDT | 4h | ALL | calibrated | maker | 112 | 0.011092 | 3.7012 | 0.0000 | 175.6294 | 211.6731 | 273.2160 | 312.8385 | 351.3902 | 400.7800 | 486.5222 | 600.4346 | 770.9215 |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | taker | 58 | 0.030335 | 6.6321 | 0.0000 | 121.8593 | 148.7264 | 172.7864 | 211.4465 | 229.5984 | 263.0576 | 285.6384 | 357.8208 | 473.5169 |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | charter | 58 | 0.060670 | 6.6321 | 0.0000 | 60.9297 | 74.3632 | 86.3932 | 105.7233 | 114.7992 | 131.5288 | 142.8192 | 178.9104 | 236.7584 |
| ASSET:NEARUSDT | 4h | ALL | frozen3.0 | maker | 58 | 0.012134 | 6.6321 | 0.0000 | 304.6483 | 371.8159 | 431.9660 | 528.6163 | 573.9960 | 657.6439 | 714.0959 | 894.5519 | 1183.7921 |
| ASSET:NEARUSDT | 4h | tuning | calibrated | taker | 64 | 0.023432 | 3.6360 | 0.0000 | 76.1470 | 94.8569 | 119.0503 | 143.6213 | 163.8034 | 202.1277 | 236.4539 | 262.3665 | 360.3555 |
| ASSET:NEARUSDT | 4h | tuning | calibrated | charter | 64 | 0.046865 | 3.6360 | 0.0000 | 38.0735 | 47.4284 | 59.5252 | 71.8107 | 81.9017 | 101.0638 | 118.2270 | 131.1833 | 180.1778 |
| ASSET:NEARUSDT | 4h | tuning | calibrated | maker | 64 | 0.009373 | 3.6360 | 0.0000 | 190.3676 | 237.1422 | 297.6259 | 359.0533 | 409.5084 | 505.3192 | 591.1348 | 655.9163 | 900.8888 |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | taker | 32 | 0.024936 | 6.2873 | 0.0000 | 108.2883 | 157.4410 | 172.9382 | 182.8439 | 221.8571 | 255.6704 | 273.1027 | 372.6436 | 457.6251 |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | charter | 32 | 0.049872 | 6.2873 | 0.0000 | 54.1442 | 78.7205 | 86.4691 | 91.4219 | 110.9286 | 127.8352 | 136.5514 | 186.3218 | 228.8126 |
| ASSET:NEARUSDT | 4h | tuning | frozen3.0 | maker | 32 | 0.009974 | 6.2873 | 0.0000 | 270.7208 | 393.6025 | 432.3454 | 457.1097 | 554.6428 | 639.1759 | 682.7568 | 931.6090 | 1144.0628 |
| ASSET:NEARUSDT | 4h | holdout | calibrated | taker | 48 | 0.032340 | 3.7226 | 0.0000 | 65.4457 | 75.5786 | 85.6143 | 115.3797 | 125.1540 | 128.1101 | 150.2305 | 166.9275 | 226.3328 |
| ASSET:NEARUSDT | 4h | holdout | calibrated | charter | 48 | 0.064679 | 3.7226 | 0.0000 | 32.7228 | 37.7893 | 42.8071 | 57.6899 | 62.5770 | 64.0550 | 75.1152 | 83.4638 | 113.1664 |
| ASSET:NEARUSDT | 4h | holdout | calibrated | maker | 48 | 0.012936 | 3.7226 | 0.0000 | 163.6141 | 188.9466 | 214.0357 | 288.4493 | 312.8850 | 320.2752 | 375.5762 | 417.3188 | 565.8320 |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | taker | 26 | 0.032697 | 7.8883 | 0.0000 | 129.8291 | 146.1402 | 182.7857 | 224.6108 | 234.7141 | 265.3440 | 287.2080 | 332.6199 | 452.9154 |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | charter | 26 | 0.065393 | 7.8883 | 0.0000 | 64.9145 | 73.0701 | 91.3929 | 112.3054 | 117.3571 | 132.6720 | 143.6040 | 166.3099 | 226.4577 |
| ASSET:NEARUSDT | 4h | holdout | frozen3.0 | maker | 26 | 0.013079 | 7.8883 | 0.0000 | 324.5727 | 365.3506 | 456.9643 | 561.5271 | 586.7853 | 663.3599 | 718.0199 | 831.5497 | 1132.2884 |
| ASSET:ZECUSDT | 4h | ALL | calibrated | taker | 112 | 0.030051 | 4.2050 | 0.0000 | 66.9907 | 92.1350 | 109.3189 | 125.8169 | 148.6486 | 167.6639 | 185.0663 | 215.5506 | 289.4241 |
| ASSET:ZECUSDT | 4h | ALL | calibrated | charter | 112 | 0.060103 | 4.2050 | 0.0000 | 33.4953 | 46.0675 | 54.6594 | 62.9085 | 74.3243 | 83.8320 | 92.5331 | 107.7753 | 144.7120 |
| ASSET:ZECUSDT | 4h | ALL | calibrated | maker | 112 | 0.012021 | 4.2050 | 0.0000 | 167.4766 | 230.3374 | 273.2972 | 314.5423 | 371.6216 | 419.1598 | 462.6657 | 538.8765 | 723.5602 |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | taker | 61 | 0.031324 | 6.0396 | 0.0000 | 119.3387 | 147.2019 | 158.5253 | 170.6980 | 188.5332 | 220.9533 | 288.9246 | 341.1019 | 486.9619 |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | charter | 61 | 0.062648 | 6.0396 | 0.0000 | 59.6694 | 73.6010 | 79.2627 | 85.3490 | 94.2666 | 110.4767 | 144.4623 | 170.5509 | 243.4810 |
| ASSET:ZECUSDT | 4h | ALL | frozen3.0 | maker | 61 | 0.012530 | 6.0396 | 0.0000 | 298.3468 | 368.0049 | 396.3134 | 426.7450 | 471.3329 | 552.3833 | 722.3114 | 852.7547 | 1217.4049 |
| ASSET:ZECUSDT | 4h | tuning | calibrated | taker | 71 | 0.032068 | 4.1408 | 0.0000 | 62.2222 | 84.8065 | 109.0974 | 119.5446 | 137.9655 | 166.6577 | 177.6049 | 195.5604 | 251.3246 |
| ASSET:ZECUSDT | 4h | tuning | calibrated | charter | 71 | 0.064137 | 4.1408 | 0.0000 | 31.1111 | 42.4033 | 54.5487 | 59.7723 | 68.9828 | 83.3288 | 88.8024 | 97.7802 | 125.6623 |
| ASSET:ZECUSDT | 4h | tuning | calibrated | maker | 71 | 0.012827 | 4.1408 | 0.0000 | 155.5556 | 212.0163 | 272.7434 | 298.8615 | 344.9139 | 416.6442 | 444.0122 | 488.9009 | 628.3116 |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | taker | 43 | 0.034290 | 5.8605 | 0.0000 | 118.4785 | 141.4339 | 154.0441 | 164.9269 | 172.4838 | 195.7387 | 228.9543 | 300.4178 | 472.0518 |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | charter | 43 | 0.068581 | 5.8605 | 0.0000 | 59.2393 | 70.7170 | 77.0221 | 82.4634 | 86.2419 | 97.8693 | 114.4772 | 150.2089 | 236.0259 |
| ASSET:ZECUSDT | 4h | tuning | frozen3.0 | maker | 43 | 0.013716 | 5.8605 | 0.0000 | 296.1963 | 353.5848 | 385.1104 | 412.3172 | 431.2096 | 489.3467 | 572.3858 | 751.0445 | 1180.1295 |
| ASSET:ZECUSDT | 4h | holdout | calibrated | taker | 41 | 0.028617 | 4.3264 | 0.0000 | 87.6664 | 96.8188 | 111.7647 | 142.3729 | 160.5810 | 173.0173 | 198.3285 | 235.2941 | 313.4367 |
| ASSET:ZECUSDT | 4h | holdout | calibrated | charter | 41 | 0.057234 | 4.3264 | 0.0000 | 43.8332 | 48.4094 | 55.8824 | 71.1864 | 80.2905 | 86.5086 | 99.1642 | 117.6471 | 156.7183 |
| ASSET:ZECUSDT | 4h | holdout | calibrated | maker | 41 | 0.011447 | 4.3264 | 0.0000 | 219.1660 | 242.0470 | 279.4118 | 355.9322 | 401.4526 | 432.5432 | 495.8212 | 588.2353 | 783.5917 |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | taker | 18 | 0.028155 | 6.2354 | 0.0000 | 151.2937 | 175.0574 | 189.3708 | 216.1445 | 261.0938 | 313.9616 | 347.1038 | 415.5338 | 502.6349 |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | charter | 18 | 0.056309 | 6.2354 | 0.0000 | 75.6468 | 87.5287 | 94.6854 | 108.0722 | 130.5469 | 156.9808 | 173.5519 | 207.7669 | 251.3175 |
| ASSET:ZECUSDT | 4h | holdout | frozen3.0 | maker | 18 | 0.011262 | 6.2354 | 0.0000 | 378.2342 | 437.6434 | 473.4269 | 540.3612 | 652.7344 | 784.9040 | 867.7596 | 1038.8345 | 1256.5873 |
| ASSET:ENAUSDT | 4h | ALL | calibrated | taker | 28 | 0.024106 | 5.2653 | 0.0000 | 154.2604 | 169.0543 | 201.9552 | 228.4187 | 240.9592 | 262.0302 | 265.4951 | 284.4921 | 327.4016 |
| ASSET:ENAUSDT | 4h | ALL | calibrated | charter | 28 | 0.072318 | 5.2653 | 0.0000 | 51.4201 | 56.3514 | 67.3184 | 76.1396 | 80.3197 | 87.3434 | 88.4984 | 94.8307 | 109.1339 |
| ASSET:ENAUSDT | 4h | ALL | calibrated | maker | 28 | 0.009642 | 5.2653 | 0.0000 | 385.6510 | 422.6359 | 504.8880 | 571.0466 | 602.3981 | 655.0755 | 663.7377 | 711.2303 | 818.5041 |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | taker | 24 | 0.024931 | 5.9186 | 0.0000 | 169.2844 | 197.6034 | 220.2710 | 241.6949 | 263.5248 | 268.4022 | 287.0042 | 318.4687 | 357.9469 |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | charter | 24 | 0.074793 | 5.9186 | 0.0000 | 56.4281 | 65.8678 | 73.4237 | 80.5650 | 87.8416 | 89.4674 | 95.6681 | 106.1562 | 119.3156 |
| ASSET:ENAUSDT | 4h | ALL | frozen3.0 | maker | 24 | 0.009972 | 5.9186 | 0.0000 | 423.2110 | 494.0086 | 550.6776 | 604.2373 | 658.8121 | 671.0056 | 717.5104 | 796.1717 | 894.8673 |
| ASSET:ENAUSDT | 4h | tuning | calibrated | taker | 4 | 0.021876 | 5.9381 | 0.0000 | 225.2210 | 231.8374 | 238.4538 | 246.3459 | 254.8760 | 263.4061 | 274.7623 | 291.7710 | 308.7798 |
| ASSET:ENAUSDT | 4h | tuning | calibrated | charter | 4 | 0.065629 | 5.9381 | 0.0000 | 75.0737 | 77.2791 | 79.4846 | 82.1153 | 84.9587 | 87.8020 | 91.5874 | 97.2570 | 102.9266 |
| ASSET:ENAUSDT | 4h | tuning | calibrated | maker | 4 | 0.008751 | 5.9381 | 0.0000 | 563.0526 | 579.5935 | 596.1344 | 615.8648 | 637.1900 | 658.5152 | 686.9059 | 729.4276 | 771.9494 |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | taker | 3 | 0.022459 | 6.7516 | 0.0000 | 246.3459 | 252.0326 | 257.7194 | 263.4061 | 269.0928 | 280.4319 | 291.7710 | 303.1102 | 314.4493 |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | charter | 3 | 0.067377 | 6.7516 | 0.0000 | 82.1153 | 84.0109 | 85.9065 | 87.8020 | 89.6976 | 93.4773 | 97.2570 | 101.0367 | 104.8164 |
| ASSET:ENAUSDT | 4h | tuning | frozen3.0 | maker | 3 | 0.008984 | 6.7516 | 0.0000 | 615.8648 | 630.0816 | 644.2984 | 658.5152 | 672.7319 | 701.0798 | 729.4276 | 757.7755 | 786.1233 |
| ASSET:ENAUSDT | 4h | holdout | calibrated | taker | 24 | 0.024931 | 5.2653 | 0.0000 | 151.0990 | 164.6409 | 189.3559 | 208.8108 | 236.7901 | 258.1458 | 264.3353 | 284.4291 | 325.8926 |
| ASSET:ENAUSDT | 4h | holdout | calibrated | charter | 24 | 0.074793 | 5.2653 | 0.0000 | 50.3663 | 54.8803 | 63.1186 | 69.6036 | 78.9300 | 86.0486 | 88.1118 | 94.8097 | 108.6309 |
| ASSET:ENAUSDT | 4h | holdout | calibrated | maker | 24 | 0.009972 | 5.2653 | 0.0000 | 377.7475 | 411.6022 | 473.3898 | 522.0270 | 591.9753 | 645.3646 | 660.8382 | 711.0726 | 814.7316 |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | taker | 21 | 0.024948 | 5.8605 | 0.0000 | 167.1795 | 191.2992 | 203.2955 | 241.2593 | 262.8594 | 265.6400 | 284.6182 | 313.5889 | 369.4246 |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | charter | 21 | 0.074844 | 5.8605 | 0.0000 | 55.7265 | 63.7664 | 67.7652 | 80.4198 | 87.6198 | 88.5467 | 94.8727 | 104.5296 | 123.1415 |
| ASSET:ENAUSDT | 4h | holdout | frozen3.0 | maker | 21 | 0.009979 | 5.8605 | 0.0000 | 417.9487 | 478.2479 | 508.2387 | 603.1482 | 657.1484 | 664.1001 | 711.5455 | 783.9721 | 923.5615 |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | taker | 21 | 0.025120 | 4.5596 | 0.0000 | 125.0000 | 141.4693 | 153.6842 | 158.2341 | 202.9652 | 226.7862 | 263.4069 | 294.9309 | 457.7144 |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | charter | 21 | 0.075359 | 4.5596 | 0.0000 | 41.6667 | 47.1564 | 51.2281 | 52.7447 | 67.6551 | 75.5954 | 87.8023 | 98.3103 | 152.5715 |
| ASSET:PUMPUSDT | 4h | ALL | calibrated | maker | 21 | 0.010048 | 4.5596 | 0.0000 | 312.5000 | 353.6733 | 384.2105 | 395.5853 | 507.4131 | 566.9656 | 658.5174 | 737.3272 | 1144.2860 |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | taker | 7 | 0.020782 | 7.1725 | 0.0000 | 240.0668 | 264.8739 | 278.8695 | 353.2065 | 457.7144 | 491.1636 | 514.5367 | 517.7576 | 578.3194 |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | charter | 7 | 0.062345 | 7.1725 | 0.0000 | 80.0223 | 88.2913 | 92.9565 | 117.7355 | 152.5715 | 163.7212 | 171.5122 | 172.5859 | 192.7731 |
| ASSET:PUMPUSDT | 4h | ALL | frozen3.0 | maker | 7 | 0.008313 | 7.1725 | 0.0000 | 600.1671 | 662.1847 | 697.1737 | 883.0164 | 1144.2860 | 1227.9090 | 1286.3417 | 1294.3939 | 1445.7984 |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | taker | 21 | 0.025120 | 4.5596 | 0.0000 | 125.0000 | 141.4693 | 153.6842 | 158.2341 | 202.9652 | 226.7862 | 263.4069 | 294.9309 | 457.7144 |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | charter | 21 | 0.075359 | 4.5596 | 0.0000 | 41.6667 | 47.1564 | 51.2281 | 52.7447 | 67.6551 | 75.5954 | 87.8023 | 98.3103 | 152.5715 |
| ASSET:PUMPUSDT | 4h | holdout | calibrated | maker | 21 | 0.010048 | 4.5596 | 0.0000 | 312.5000 | 353.6733 | 384.2105 | 395.5853 | 507.4131 | 566.9656 | 658.5174 | 737.3272 | 1144.2860 |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | taker | 7 | 0.020782 | 7.1725 | 0.0000 | 240.0668 | 264.8739 | 278.8695 | 353.2065 | 457.7144 | 491.1636 | 514.5367 | 517.7576 | 578.3194 |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | charter | 7 | 0.062345 | 7.1725 | 0.0000 | 80.0223 | 88.2913 | 92.9565 | 117.7355 | 152.5715 | 163.7212 | 171.5122 | 172.5859 | 192.7731 |
| ASSET:PUMPUSDT | 4h | holdout | frozen3.0 | maker | 7 | 0.008313 | 7.1725 | 0.0000 | 600.1671 | 662.1847 | 697.1737 | 883.0164 | 1144.2860 | 1227.9090 | 1286.3417 | 1294.3939 | 1445.7984 |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | taker | 22 | 0.031660 | 3.7506 | 0.0000 | 80.4291 | 90.6462 | 102.2578 | 107.0572 | 117.4910 | 146.7233 | 162.4573 | 190.6402 | 262.8606 |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | charter | 22 | 0.094980 | 3.7506 | 0.0000 | 26.8097 | 30.2154 | 34.0859 | 35.6857 | 39.1637 | 48.9078 | 54.1524 | 63.5467 | 87.6202 |
| ASSET:HYPEUSDT | 4h | ALL | calibrated | maker | 22 | 0.012664 | 3.7506 | 0.0000 | 201.0727 | 226.6154 | 255.6445 | 267.6430 | 293.7274 | 366.8083 | 406.1433 | 476.6004 | 657.1514 |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | taker | 15 | 0.032992 | 7.7820 | 0.0000 | 135.9131 | 175.7151 | 185.5032 | 189.5050 | 241.4730 | 280.1364 | 289.1256 | 298.4852 | 342.4892 |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | charter | 15 | 0.098975 | 7.7820 | 0.0000 | 45.3044 | 58.5717 | 61.8344 | 63.1683 | 80.4910 | 93.3788 | 96.3752 | 99.4951 | 114.1631 |
| ASSET:HYPEUSDT | 4h | ALL | frozen3.0 | maker | 15 | 0.013197 | 7.7820 | 0.0000 | 339.7828 | 439.2877 | 463.7579 | 473.7626 | 603.6825 | 700.3410 | 722.8140 | 746.2130 | 856.2229 |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | taker | 22 | 0.031660 | 3.7506 | 0.0000 | 80.4291 | 90.6462 | 102.2578 | 107.0572 | 117.4910 | 146.7233 | 162.4573 | 190.6402 | 262.8606 |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | charter | 22 | 0.094980 | 3.7506 | 0.0000 | 26.8097 | 30.2154 | 34.0859 | 35.6857 | 39.1637 | 48.9078 | 54.1524 | 63.5467 | 87.6202 |
| ASSET:HYPEUSDT | 4h | holdout | calibrated | maker | 22 | 0.012664 | 3.7506 | 0.0000 | 201.0727 | 226.6154 | 255.6445 | 267.6430 | 293.7274 | 366.8083 | 406.1433 | 476.6004 | 657.1514 |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | taker | 15 | 0.032992 | 7.7820 | 0.0000 | 135.9131 | 175.7151 | 185.5032 | 189.5050 | 241.4730 | 280.1364 | 289.1256 | 298.4852 | 342.4892 |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | charter | 15 | 0.098975 | 7.7820 | 0.0000 | 45.3044 | 58.5717 | 61.8344 | 63.1683 | 80.4910 | 93.3788 | 96.3752 | 99.4951 | 114.1631 |
| ASSET:HYPEUSDT | 4h | holdout | frozen3.0 | maker | 15 | 0.013197 | 7.7820 | 0.0000 | 339.7828 | 439.2877 | 463.7579 | 473.7626 | 603.6825 | 700.3410 | 722.8140 | 746.2130 | 856.2229 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | taker | 49 | 0.048389 | 4.5848 | 0.0000 | 68.1642 | 74.8368 | 81.6875 | 89.5162 | 107.3954 | 115.4167 | 129.2290 | 145.3800 | 184.5230 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | charter | 49 | 0.145168 | 4.5848 | 0.0000 | 22.7214 | 24.9456 | 27.2292 | 29.8387 | 35.7985 | 38.4722 | 43.0763 | 48.4600 | 61.5077 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | calibrated | maker | 49 | 0.019356 | 4.5848 | 0.0000 | 170.4105 | 187.0920 | 204.2187 | 223.7905 | 268.4885 | 288.5418 | 323.0726 | 363.4501 | 461.3074 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | taker | 31 | 0.050976 | 6.2523 | 0.0000 | 78.2907 | 113.3826 | 118.3988 | 129.3960 | 135.0515 | 159.1696 | 189.0014 | 246.6887 | 399.8137 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | charter | 31 | 0.152928 | 6.2523 | 0.0000 | 26.0969 | 37.7942 | 39.4663 | 43.1320 | 45.0172 | 53.0565 | 63.0005 | 82.2296 | 133.2712 |
| ASSET:MNTUSDT_BYBIT | 4h | ALL | frozen3.0 | maker | 31 | 0.020390 | 6.2523 | 0.0000 | 195.7268 | 283.4565 | 295.9971 | 323.4901 | 337.6289 | 397.9239 | 472.5034 | 616.7219 | 999.5343 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | taker | 15 | 0.053544 | 4.4778 | 0.0000 | 46.0626 | 63.8560 | 70.4489 | 74.7523 | 76.0487 | 82.0374 | 120.5145 | 145.6274 | 208.7856 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | charter | 15 | 0.160633 | 4.4778 | 0.0000 | 15.3542 | 21.2853 | 23.4830 | 24.9174 | 25.3496 | 27.3458 | 40.1715 | 48.5425 | 69.5952 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | calibrated | maker | 15 | 0.021418 | 4.4778 | 0.0000 | 115.1565 | 159.6399 | 176.1222 | 186.8807 | 190.1217 | 205.0935 | 301.2863 | 364.0686 | 521.9641 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | taker | 8 | 0.049866 | 6.9396 | 0.0000 | 109.5499 | 129.1499 | 132.1807 | 135.5305 | 148.8839 | 174.3277 | 219.9943 | 252.9501 | 320.8589 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | charter | 8 | 0.149599 | 6.9396 | 0.0000 | 36.5166 | 43.0500 | 44.0602 | 45.1768 | 49.6280 | 58.1092 | 73.3314 | 84.3167 | 106.9530 |
| ASSET:MNTUSDT_BYBIT | 4h | tuning | frozen3.0 | maker | 8 | 0.019946 | 6.9396 | 0.0000 | 273.8749 | 322.8747 | 330.4518 | 338.8263 | 372.2097 | 435.8194 | 549.9858 | 632.3752 | 802.1474 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | taker | 34 | 0.046663 | 4.8671 | 0.0000 | 74.9436 | 82.3609 | 95.3187 | 105.8054 | 113.1041 | 116.6793 | 129.9616 | 145.3800 | 165.3031 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | charter | 34 | 0.139990 | 4.8671 | 0.0000 | 24.9812 | 27.4536 | 31.7729 | 35.2685 | 37.7014 | 38.8931 | 43.3205 | 48.4600 | 55.1010 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | calibrated | maker | 34 | 0.018665 | 4.8671 | 0.0000 | 187.3589 | 205.9023 | 238.2968 | 264.5135 | 282.7603 | 291.6983 | 324.9039 | 363.4501 | 413.2577 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | taker | 23 | 0.050976 | 6.2523 | 0.0000 | 78.7336 | 94.2943 | 116.6247 | 124.0519 | 132.4942 | 146.7560 | 176.3596 | 225.8248 | 385.6921 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | charter | 23 | 0.152928 | 6.2523 | 0.0000 | 26.2445 | 31.4314 | 38.8749 | 41.3506 | 44.1647 | 48.9187 | 58.7865 | 75.2749 | 128.5640 |
| ASSET:MNTUSDT_BYBIT | 4h | holdout | frozen3.0 | maker | 23 | 0.020390 | 6.2523 | 0.0000 | 196.8341 | 235.7359 | 291.5617 | 310.1298 | 331.2355 | 366.8899 | 440.8990 | 564.5620 | 964.2302 |
| ASSET:SUIUSDT | 4h | ALL | calibrated | taker | 52 | 0.030885 | 4.6056 | 0.0000 | 98.2905 | 118.1912 | 129.7707 | 136.3248 | 152.3571 | 176.4281 | 181.8518 | 261.2245 | 327.3399 |
| ASSET:SUIUSDT | 4h | ALL | calibrated | charter | 52 | 0.061770 | 4.6056 | 0.0000 | 49.1452 | 59.0956 | 64.8854 | 68.1624 | 76.1785 | 88.2141 | 90.9259 | 130.6123 | 163.6700 |
| ASSET:SUIUSDT | 4h | ALL | calibrated | maker | 52 | 0.012354 | 4.6056 | 0.0000 | 245.7262 | 295.4780 | 324.4269 | 340.8119 | 380.8926 | 441.0703 | 454.6294 | 653.0613 | 818.3498 |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | taker | 30 | 0.030565 | 6.2825 | 0.0000 | 135.4987 | 150.0466 | 181.0606 | 200.1518 | 223.1137 | 266.0932 | 293.3683 | 320.2200 | 376.0801 |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | charter | 30 | 0.061131 | 6.2825 | 0.0000 | 67.7494 | 75.0233 | 90.5303 | 100.0759 | 111.5569 | 133.0466 | 146.6841 | 160.1100 | 188.0401 |
| ASSET:SUIUSDT | 4h | ALL | frozen3.0 | maker | 30 | 0.012226 | 6.2825 | 0.0000 | 338.7468 | 375.1164 | 452.6514 | 500.3795 | 557.7843 | 665.2331 | 733.4207 | 800.5500 | 940.2003 |
| ASSET:SUIUSDT | 4h | tuning | calibrated | taker | 19 | 0.030523 | 4.7994 | 0.0000 | 93.3899 | 110.9034 | 118.9899 | 128.4346 | 150.3001 | 168.2413 | 178.2639 | 214.8129 | 303.5796 |
| ASSET:SUIUSDT | 4h | tuning | calibrated | charter | 19 | 0.061046 | 4.7994 | 0.0000 | 46.6950 | 55.4517 | 59.4949 | 64.2173 | 75.1500 | 84.1206 | 89.1320 | 107.4064 | 151.7898 |
| ASSET:SUIUSDT | 4h | tuning | calibrated | maker | 19 | 0.012209 | 4.7994 | 0.0000 | 233.4748 | 277.2585 | 297.4747 | 321.0864 | 375.7502 | 420.6032 | 445.6598 | 537.0322 | 758.9491 |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | taker | 10 | 0.028281 | 6.5028 | 0.0000 | 119.0509 | 144.1475 | 182.2856 | 206.7763 | 216.5387 | 222.3135 | 245.1760 | 299.8076 | 359.3317 |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | charter | 10 | 0.056563 | 6.5028 | 0.0000 | 59.5254 | 72.0737 | 91.1428 | 103.3881 | 108.2693 | 111.1567 | 122.5880 | 149.9038 | 179.6658 |
| ASSET:SUIUSDT | 4h | tuning | frozen3.0 | maker | 10 | 0.011313 | 6.5028 | 0.0000 | 297.6272 | 360.3687 | 455.7139 | 516.9407 | 541.3466 | 555.7837 | 612.9399 | 749.5191 | 898.3292 |
| ASSET:SUIUSDT | 4h | holdout | calibrated | taker | 33 | 0.031160 | 4.5705 | 0.0000 | 103.0303 | 127.2155 | 136.0391 | 139.3729 | 154.4140 | 178.2114 | 194.5802 | 258.6672 | 323.5545 |
| ASSET:SUIUSDT | 4h | holdout | calibrated | charter | 33 | 0.062320 | 4.5705 | 0.0000 | 51.5151 | 63.6077 | 68.0196 | 69.6864 | 77.2070 | 89.1057 | 97.2901 | 129.3336 | 161.7773 |
| ASSET:SUIUSDT | 4h | holdout | calibrated | maker | 33 | 0.012464 | 4.5705 | 0.0000 | 257.5757 | 318.0387 | 340.0978 | 348.4322 | 386.0351 | 445.5286 | 486.4505 | 646.6679 | 808.8863 |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | taker | 20 | 0.031770 | 6.2825 | 0.0000 | 146.4942 | 171.3681 | 181.0606 | 198.9681 | 256.5182 | 279.0447 | 293.6476 | 320.2200 | 376.7038 |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | charter | 20 | 0.063539 | 6.2825 | 0.0000 | 73.2471 | 85.6841 | 90.5303 | 99.4841 | 128.2591 | 139.5224 | 146.8238 | 160.1100 | 188.3519 |
| ASSET:SUIUSDT | 4h | holdout | frozen3.0 | maker | 20 | 0.012708 | 6.2825 | 0.0000 | 366.2355 | 428.4203 | 452.6514 | 497.4204 | 641.2956 | 697.6118 | 734.1190 | 800.5500 | 941.7594 |
| ASSET:LTCUSDT | 4h | ALL | calibrated | taker | 109 | 0.041930 | 4.4625 | 0.0000 | 44.7129 | 64.8720 | 75.3395 | 90.7946 | 103.6665 | 121.7011 | 135.7285 | 161.4835 | 300.5748 |
| ASSET:LTCUSDT | 4h | ALL | calibrated | charter | 109 | 0.083861 | 4.4625 | 0.0000 | 22.3565 | 32.4360 | 37.6698 | 45.3973 | 51.8332 | 60.8505 | 67.8642 | 80.7417 | 150.2874 |
| ASSET:LTCUSDT | 4h | ALL | calibrated | maker | 109 | 0.016772 | 4.4625 | 0.0000 | 111.7823 | 162.1801 | 188.3488 | 226.9865 | 259.1661 | 304.2527 | 339.3212 | 403.7087 | 751.4370 |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | taker | 64 | 0.038890 | 6.6851 | 0.0000 | 106.0133 | 118.5448 | 127.7429 | 146.6827 | 163.7162 | 233.9753 | 282.6174 | 331.1732 | 370.7449 |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | charter | 64 | 0.077781 | 6.6851 | 0.0000 | 53.0066 | 59.2724 | 63.8715 | 73.3413 | 81.8581 | 116.9877 | 141.3087 | 165.5866 | 185.3724 |
| ASSET:LTCUSDT | 4h | ALL | frozen3.0 | maker | 64 | 0.015556 | 6.6851 | 0.0000 | 265.0332 | 296.3621 | 319.3573 | 366.7067 | 409.2905 | 584.9384 | 706.5434 | 827.9329 | 926.8622 |
| ASSET:LTCUSDT | 4h | tuning | calibrated | taker | 72 | 0.038598 | 4.4681 | 0.0000 | 50.5038 | 71.1659 | 86.5879 | 93.9781 | 114.6099 | 134.5352 | 156.0898 | 238.8675 | 313.1854 |
| ASSET:LTCUSDT | 4h | tuning | calibrated | charter | 72 | 0.077196 | 4.4681 | 0.0000 | 25.2519 | 35.5830 | 43.2940 | 46.9890 | 57.3049 | 67.2676 | 78.0449 | 119.4337 | 156.5927 |
| ASSET:LTCUSDT | 4h | tuning | calibrated | maker | 72 | 0.015439 | 4.4681 | 0.0000 | 126.2595 | 177.9149 | 216.4698 | 234.9452 | 286.5247 | 336.3380 | 390.2244 | 597.1686 | 782.9636 |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | taker | 41 | 0.037209 | 7.1882 | 0.0000 | 112.9603 | 131.4827 | 148.8333 | 166.6896 | 246.0094 | 285.1742 | 329.8969 | 351.4792 | 400.8597 |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | charter | 41 | 0.074419 | 7.1882 | 0.0000 | 56.4801 | 65.7413 | 74.4167 | 83.3448 | 123.0047 | 142.5871 | 164.9485 | 175.7396 | 200.4298 |
| ASSET:LTCUSDT | 4h | tuning | frozen3.0 | maker | 41 | 0.014884 | 7.1882 | 0.0000 | 282.4006 | 328.7067 | 372.0833 | 416.7240 | 615.0235 | 712.9356 | 824.7423 | 878.6979 | 1002.1491 |
| ASSET:LTCUSDT | 4h | holdout | calibrated | taker | 37 | 0.051386 | 4.2660 | 0.0000 | 44.6458 | 52.0256 | 71.5154 | 75.2021 | 92.5681 | 102.7482 | 116.6193 | 123.9154 | 142.1836 |
| ASSET:LTCUSDT | 4h | holdout | calibrated | charter | 37 | 0.102772 | 4.2660 | 0.0000 | 22.3229 | 26.0128 | 35.7577 | 37.6010 | 46.2841 | 51.3741 | 58.3097 | 61.9577 | 71.0918 |
| ASSET:LTCUSDT | 4h | holdout | calibrated | maker | 37 | 0.020554 | 4.2660 | 0.0000 | 111.6145 | 130.0640 | 178.7885 | 188.0052 | 231.4203 | 256.8706 | 291.5483 | 309.7886 | 355.4590 |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | taker | 23 | 0.049909 | 6.5143 | 0.0000 | 98.6422 | 106.8581 | 115.4483 | 120.8348 | 127.5891 | 142.0169 | 167.4340 | 232.3316 | 254.8522 |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | charter | 23 | 0.099817 | 6.5143 | 0.0000 | 49.3211 | 53.4290 | 57.7242 | 60.4174 | 63.7946 | 71.0084 | 83.7170 | 116.1658 | 127.4261 |
| ASSET:LTCUSDT | 4h | holdout | frozen3.0 | maker | 23 | 0.019963 | 6.5143 | 0.0000 | 246.6054 | 267.1452 | 288.6208 | 302.0871 | 318.9728 | 355.0422 | 418.5849 | 580.8289 | 637.1306 |
| ASSET:XMRUSDT | 4h | ALL | calibrated | taker | 97 | 0.037158 | 3.6160 | 0.0000 | 56.4460 | 69.5880 | 84.2819 | 91.4757 | 103.6746 | 113.7646 | 128.8353 | 148.3814 | 205.1092 |
| ASSET:XMRUSDT | 4h | ALL | calibrated | charter | 97 | 0.074316 | 3.6160 | 0.0000 | 28.2230 | 34.7940 | 42.1409 | 45.7378 | 51.8373 | 56.8823 | 64.4176 | 74.1907 | 102.5546 |
| ASSET:XMRUSDT | 4h | ALL | calibrated | maker | 97 | 0.014863 | 3.6160 | 0.0000 | 141.1151 | 173.9699 | 210.7047 | 228.6892 | 259.1866 | 284.4116 | 322.0882 | 370.9534 | 512.7731 |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | taker | 40 | 0.044611 | 6.0665 | 0.0000 | 71.6421 | 86.5759 | 106.8014 | 123.8690 | 139.1847 | 159.6775 | 197.4407 | 288.9110 | 385.7990 |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | charter | 40 | 0.089222 | 6.0665 | 0.0000 | 35.8211 | 43.2880 | 53.4007 | 61.9345 | 69.5924 | 79.8388 | 98.7203 | 144.4555 | 192.8995 |
| ASSET:XMRUSDT | 4h | ALL | frozen3.0 | maker | 40 | 0.017844 | 6.0665 | 0.0000 | 179.1053 | 216.4398 | 267.0035 | 309.6725 | 347.9618 | 399.1939 | 493.6017 | 722.2775 | 964.4976 |
| ASSET:XMRUSDT | 4h | tuning | calibrated | taker | 73 | 0.037292 | 3.6160 | 0.0000 | 56.1715 | 69.6796 | 82.4812 | 90.6624 | 103.6746 | 113.4811 | 126.1959 | 151.3495 | 195.3752 |
| ASSET:XMRUSDT | 4h | tuning | calibrated | charter | 73 | 0.074584 | 3.6160 | 0.0000 | 28.0857 | 34.8398 | 41.2406 | 45.3312 | 51.8373 | 56.7406 | 63.0979 | 75.6747 | 97.6876 |
| ASSET:XMRUSDT | 4h | tuning | calibrated | maker | 73 | 0.014917 | 3.6160 | 0.0000 | 140.4287 | 174.1990 | 206.2031 | 226.6559 | 259.1866 | 283.7028 | 315.4897 | 378.3737 | 488.4381 |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | taker | 28 | 0.047426 | 6.0665 | 0.0000 | 59.9872 | 77.1566 | 93.1418 | 107.5765 | 136.1738 | 148.1753 | 170.1702 | 265.9134 | 350.7227 |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | charter | 28 | 0.094852 | 6.0665 | 0.0000 | 29.9936 | 38.5783 | 46.5709 | 53.7882 | 68.0869 | 74.0877 | 85.0851 | 132.9567 | 175.3614 |
| ASSET:XMRUSDT | 4h | tuning | frozen3.0 | maker | 28 | 0.018970 | 6.0665 | 0.0000 | 149.9681 | 192.8916 | 232.8546 | 268.9411 | 340.4346 | 370.4383 | 425.4255 | 664.7836 | 876.8069 |
| ASSET:XMRUSDT | 4h | holdout | calibrated | taker | 24 | 0.037149 | 3.6794 | 0.0000 | 59.1313 | 71.1876 | 88.4722 | 97.4746 | 102.9715 | 126.2248 | 135.1027 | 141.7010 | 210.5752 |
| ASSET:XMRUSDT | 4h | holdout | calibrated | charter | 24 | 0.074298 | 3.6794 | 0.0000 | 29.5657 | 35.5938 | 44.2361 | 48.7373 | 51.4857 | 63.1124 | 67.5513 | 70.8505 | 105.2876 |
| ASSET:XMRUSDT | 4h | holdout | calibrated | maker | 24 | 0.014859 | 3.6794 | 0.0000 | 147.8283 | 177.9689 | 221.1804 | 243.6865 | 257.4286 | 315.5621 | 337.7567 | 354.2525 | 526.4379 |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | taker | 12 | 0.039290 | 6.1022 | 0.0000 | 109.3692 | 121.8183 | 124.5486 | 131.1773 | 149.4917 | 177.8625 | 228.8904 | 287.1924 | 443.1971 |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | charter | 12 | 0.078579 | 6.1022 | 0.0000 | 54.6846 | 60.9091 | 62.2743 | 65.5887 | 74.7459 | 88.9313 | 114.4452 | 143.5962 | 221.5985 |
| ASSET:XMRUSDT | 4h | holdout | frozen3.0 | maker | 12 | 0.015716 | 6.1022 | 0.0000 | 273.4230 | 304.5456 | 311.3716 | 327.9434 | 373.7293 | 444.6563 | 572.2260 | 717.9811 | 1107.9927 |
| ASSET:BNBUSDT | 4h | ALL | calibrated | taker | 94 | 0.047262 | 4.2111 | 0.0000 | 41.7886 | 53.2523 | 67.8326 | 79.5782 | 96.0642 | 107.7543 | 120.9446 | 140.4542 | 199.8662 |
| ASSET:BNBUSDT | 4h | ALL | calibrated | charter | 94 | 0.094525 | 4.2111 | 0.0000 | 20.8943 | 26.6262 | 33.9163 | 39.7891 | 48.0321 | 53.8772 | 60.4723 | 70.2271 | 99.9331 |
| ASSET:BNBUSDT | 4h | ALL | calibrated | maker | 94 | 0.018905 | 4.2111 | 0.0000 | 104.4714 | 133.1309 | 169.5815 | 198.9454 | 240.1606 | 269.3858 | 302.3616 | 351.1356 | 499.6654 |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | taker | 49 | 0.049056 | 6.8456 | 0.0000 | 76.4487 | 86.0802 | 108.8295 | 124.3443 | 140.7277 | 173.4577 | 199.6016 | 238.3757 | 285.4902 |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | charter | 49 | 0.098111 | 6.8456 | 0.0000 | 38.2243 | 43.0401 | 54.4147 | 62.1722 | 70.3639 | 86.7289 | 99.8008 | 119.1879 | 142.7451 |
| ASSET:BNBUSDT | 4h | ALL | frozen3.0 | maker | 49 | 0.019622 | 6.8456 | 0.0000 | 191.1217 | 215.2005 | 272.0737 | 310.8608 | 351.8193 | 433.6444 | 499.0039 | 595.9393 | 713.7254 |
| ASSET:BNBUSDT | 4h | tuning | calibrated | taker | 67 | 0.044070 | 4.1136 | 0.0000 | 45.3575 | 60.4465 | 72.1101 | 87.7032 | 98.1705 | 108.5479 | 125.3908 | 153.1408 | 198.5717 |
| ASSET:BNBUSDT | 4h | tuning | calibrated | charter | 67 | 0.088141 | 4.1136 | 0.0000 | 22.6787 | 30.2233 | 36.0551 | 43.8516 | 49.0853 | 54.2740 | 62.6954 | 76.5704 | 99.2859 |
| ASSET:BNBUSDT | 4h | tuning | calibrated | maker | 67 | 0.017628 | 4.1136 | 0.0000 | 113.3937 | 151.1163 | 180.2753 | 219.2579 | 245.4264 | 271.3698 | 313.4770 | 382.8521 | 496.4293 |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | taker | 30 | 0.043159 | 6.6915 | 0.0000 | 82.9619 | 105.1523 | 122.2654 | 142.0769 | 178.9105 | 196.4997 | 225.9486 | 255.0628 | 300.4947 |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | charter | 30 | 0.086318 | 6.6915 | 0.0000 | 41.4810 | 52.5761 | 61.1327 | 71.0385 | 89.4552 | 98.2498 | 112.9743 | 127.5314 | 150.2473 |
| ASSET:BNBUSDT | 4h | tuning | frozen3.0 | maker | 30 | 0.017264 | 6.6915 | 0.0000 | 207.4048 | 262.8807 | 305.6636 | 355.1923 | 447.2762 | 491.2491 | 564.8716 | 637.6571 | 751.2366 |
| ASSET:BNBUSDT | 4h | holdout | calibrated | taker | 27 | 0.066384 | 4.3867 | 0.0000 | 40.7096 | 46.4169 | 52.6608 | 69.2362 | 80.9208 | 105.2216 | 115.2795 | 124.7691 | 179.6745 |
| ASSET:BNBUSDT | 4h | holdout | calibrated | charter | 27 | 0.132768 | 4.3867 | 0.0000 | 20.3548 | 23.2085 | 26.3304 | 34.6181 | 40.4604 | 52.6108 | 57.6398 | 62.3845 | 89.8372 |
| ASSET:BNBUSDT | 4h | holdout | calibrated | maker | 27 | 0.026554 | 4.3867 | 0.0000 | 101.7739 | 116.0423 | 131.6520 | 173.0905 | 202.3021 | 263.0539 | 288.1988 | 311.9227 | 449.1861 |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | taker | 19 | 0.069316 | 7.3637 | 0.0000 | 59.7962 | 83.9224 | 92.3747 | 108.5912 | 123.0428 | 125.2409 | 148.8337 | 178.7998 | 267.3137 |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | charter | 19 | 0.138632 | 7.3637 | 0.0000 | 29.8981 | 41.9612 | 46.1873 | 54.2956 | 61.5214 | 62.6204 | 74.4168 | 89.3999 | 133.6569 |
| ASSET:BNBUSDT | 4h | holdout | frozen3.0 | maker | 19 | 0.027726 | 7.3637 | 0.0000 | 149.4906 | 209.8061 | 230.9367 | 271.4781 | 307.6071 | 313.1021 | 372.0842 | 446.9996 | 668.2843 |
| ASSET:UNIUSDT | 4h | ALL | calibrated | taker | 93 | 0.029899 | 4.1447 | 0.0000 | 70.5111 | 91.6503 | 102.1198 | 124.6616 | 149.7996 | 168.8085 | 190.4055 | 219.5745 | 313.5682 |
| ASSET:UNIUSDT | 4h | ALL | calibrated | charter | 93 | 0.059799 | 4.1447 | 0.0000 | 35.2556 | 45.8252 | 51.0599 | 62.3308 | 74.8998 | 84.4043 | 95.2028 | 109.7873 | 156.7841 |
| ASSET:UNIUSDT | 4h | ALL | calibrated | maker | 93 | 0.011960 | 4.1447 | 0.0000 | 176.2779 | 229.1259 | 255.2995 | 311.6540 | 374.4990 | 422.0213 | 476.0138 | 548.9363 | 783.9205 |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | taker | 55 | 0.030779 | 7.3250 | 0.0000 | 138.4292 | 159.9374 | 184.3186 | 211.5698 | 228.2787 | 251.3020 | 280.1427 | 310.3536 | 458.2617 |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | charter | 55 | 0.061559 | 7.3250 | 0.0000 | 69.2146 | 79.9687 | 92.1593 | 105.7849 | 114.1394 | 125.6510 | 140.0714 | 155.1768 | 229.1308 |
| ASSET:UNIUSDT | 4h | ALL | frozen3.0 | maker | 55 | 0.012312 | 7.3250 | 0.0000 | 346.0731 | 399.8435 | 460.7965 | 528.9245 | 570.6968 | 628.2551 | 700.3568 | 775.8841 | 1145.6542 |
| ASSET:UNIUSDT | 4h | tuning | calibrated | taker | 57 | 0.028851 | 4.1300 | 0.0000 | 68.0559 | 90.3584 | 102.2202 | 137.5150 | 151.6234 | 168.8412 | 199.3200 | 272.6145 | 337.1379 |
| ASSET:UNIUSDT | 4h | tuning | calibrated | charter | 57 | 0.057701 | 4.1300 | 0.0000 | 34.0280 | 45.1792 | 51.1101 | 68.7575 | 75.8117 | 84.4206 | 99.6600 | 136.3073 | 168.5690 |
| ASSET:UNIUSDT | 4h | tuning | calibrated | maker | 57 | 0.011540 | 4.1300 | 0.0000 | 170.1398 | 225.8961 | 255.5505 | 343.7874 | 379.0585 | 422.1031 | 498.3000 | 681.5363 | 842.8448 |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | taker | 33 | 0.029304 | 6.9543 | 0.0000 | 145.9528 | 157.9304 | 170.3896 | 188.3904 | 244.2461 | 264.7135 | 301.6269 | 365.5434 | 472.7791 |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | charter | 33 | 0.058607 | 6.9543 | 0.0000 | 72.9764 | 78.9652 | 85.1948 | 94.1952 | 122.1231 | 132.3567 | 150.8135 | 182.7717 | 236.3895 |
| ASSET:UNIUSDT | 4h | tuning | frozen3.0 | maker | 33 | 0.011721 | 6.9543 | 0.0000 | 364.8819 | 394.8259 | 425.9740 | 470.9760 | 610.6153 | 661.7837 | 754.0673 | 913.8585 | 1181.9477 |
| ASSET:UNIUSDT | 4h | holdout | calibrated | taker | 36 | 0.032294 | 4.3138 | 0.0000 | 83.1745 | 92.7622 | 102.0945 | 118.3614 | 141.6722 | 168.7964 | 183.5658 | 208.2380 | 243.7027 |
| ASSET:UNIUSDT | 4h | holdout | calibrated | charter | 36 | 0.064587 | 4.3138 | 0.0000 | 41.5873 | 46.3811 | 51.0473 | 59.1807 | 70.8361 | 84.3982 | 91.7829 | 104.1190 | 121.8513 |
| ASSET:UNIUSDT | 4h | holdout | calibrated | maker | 36 | 0.012917 | 4.3138 | 0.0000 | 207.9363 | 231.9056 | 255.2363 | 295.9036 | 354.1806 | 421.9911 | 458.9145 | 520.5950 | 609.2567 |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | taker | 22 | 0.033808 | 7.6944 | 0.0000 | 136.0440 | 173.2303 | 208.4909 | 212.1798 | 225.2317 | 232.1729 | 246.0306 | 278.0537 | 281.5901 |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | charter | 22 | 0.067616 | 7.6944 | 0.0000 | 68.0220 | 86.6152 | 104.2455 | 106.0899 | 112.6159 | 116.0865 | 123.0153 | 139.0269 | 140.7951 |
| ASSET:UNIUSDT | 4h | holdout | frozen3.0 | maker | 22 | 0.013523 | 7.6944 | 0.0000 | 340.1100 | 433.0758 | 521.2274 | 530.4495 | 563.0793 | 580.4323 | 615.0765 | 695.1343 | 703.9753 |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | taker | 51 | 0.026650 | 3.8456 | 0.0000 | 93.5202 | 115.0358 | 132.8402 | 145.0435 | 160.4605 | 188.8237 | 205.1204 | 227.8677 | 263.7139 |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | charter | 51 | 0.079951 | 3.8456 | 0.0000 | 31.1734 | 38.3453 | 44.2801 | 48.3478 | 53.4868 | 62.9412 | 68.3735 | 75.9559 | 87.9046 |
| ASSET:1000PEPEUSDT | 4h | ALL | calibrated | maker | 51 | 0.010660 | 3.8456 | 0.0000 | 233.8004 | 287.5894 | 332.1004 | 362.6088 | 401.1513 | 472.0592 | 512.8011 | 569.6693 | 659.2848 |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | taker | 30 | 0.025710 | 7.3991 | 0.0000 | 176.8969 | 204.4464 | 226.8886 | 252.3980 | 272.4169 | 312.4780 | 383.4746 | 420.5479 | 468.7624 |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | charter | 30 | 0.077129 | 7.3991 | 0.0000 | 58.9656 | 68.1488 | 75.6295 | 84.1327 | 90.8056 | 104.1593 | 127.8249 | 140.1826 | 156.2541 |
| ASSET:1000PEPEUSDT | 4h | ALL | frozen3.0 | maker | 30 | 0.010284 | 7.3991 | 0.0000 | 442.2421 | 511.1160 | 567.2216 | 630.9951 | 681.0423 | 781.1949 | 958.6864 | 1051.3698 | 1171.9059 |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | taker | 18 | 0.021547 | 3.4768 | 0.0000 | 97.7766 | 116.2180 | 140.1631 | 149.4206 | 191.4389 | 225.0203 | 250.7672 | 261.4370 | 272.3243 |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | charter | 18 | 0.064640 | 3.4768 | 0.0000 | 32.5922 | 38.7393 | 46.7210 | 49.8069 | 63.8130 | 75.0068 | 83.5891 | 87.1457 | 90.7748 |
| ASSET:1000PEPEUSDT | 4h | tuning | calibrated | maker | 18 | 0.008619 | 3.4768 | 0.0000 | 244.4415 | 290.5449 | 350.4078 | 373.5515 | 478.5973 | 562.5508 | 626.9180 | 653.5926 | 680.8107 |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | taker | 9 | 0.021308 | 7.8950 | 0.0000 | 210.0341 | 236.8415 | 272.3478 | 303.4674 | 313.8531 | 379.6752 | 409.2875 | 449.5641 | 499.3117 |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | charter | 9 | 0.063924 | 7.8950 | 0.0000 | 70.0114 | 78.9472 | 90.7826 | 101.1558 | 104.6177 | 126.5584 | 136.4292 | 149.8547 | 166.4372 |
| ASSET:1000PEPEUSDT | 4h | tuning | frozen3.0 | maker | 9 | 0.008523 | 7.8950 | 0.0000 | 525.0852 | 592.1037 | 680.8696 | 758.6685 | 784.6329 | 949.1880 | 1023.2188 | 1123.9102 | 1248.2792 |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | taker | 33 | 0.028299 | 3.8776 | 0.0000 | 94.2471 | 115.5170 | 132.6315 | 141.3893 | 158.7415 | 177.6385 | 190.4529 | 209.2242 | 236.7186 |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | charter | 33 | 0.084897 | 3.8776 | 0.0000 | 31.4157 | 38.5057 | 44.2105 | 47.1298 | 52.9138 | 59.2128 | 63.4843 | 69.7414 | 78.9062 |
| ASSET:1000PEPEUSDT | 4h | holdout | calibrated | maker | 33 | 0.011320 | 3.8776 | 0.0000 | 235.6177 | 288.7926 | 331.5788 | 353.4731 | 396.8538 | 444.0962 | 476.1321 | 523.0604 | 591.7964 |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | taker | 21 | 0.027141 | 6.8760 | 0.0000 | 160.4605 | 190.0302 | 218.0546 | 241.7488 | 254.2540 | 283.1156 | 375.9997 | 410.8239 | 462.2760 |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | charter | 21 | 0.081423 | 6.8760 | 0.0000 | 53.4868 | 63.3434 | 72.6849 | 80.5829 | 84.7513 | 94.3719 | 125.3332 | 136.9413 | 154.0920 |
| ASSET:1000PEPEUSDT | 4h | holdout | frozen3.0 | maker | 21 | 0.010856 | 6.8760 | 0.0000 | 401.1513 | 475.0756 | 545.1366 | 604.3721 | 635.6349 | 707.7890 | 939.9994 | 1027.0597 | 1155.6900 |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | taker | 92 | 0.036107 | 3.9286 | 0.0000 | 53.7346 | 73.8391 | 82.4671 | 99.3896 | 109.5323 | 133.8258 | 160.5477 | 223.3161 | 267.6209 |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | charter | 92 | 0.072214 | 3.9286 | 0.0000 | 26.8673 | 36.9195 | 41.2336 | 49.6948 | 54.7662 | 66.9129 | 80.2739 | 111.6581 | 133.8105 |
| ASSET:DOGEUSDT | 4h | ALL | calibrated | maker | 92 | 0.014443 | 3.9286 | 0.0000 | 134.3364 | 184.5977 | 206.1679 | 248.4739 | 273.8308 | 334.5645 | 401.3693 | 558.2904 | 669.0523 |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | taker | 46 | 0.035071 | 6.8917 | 0.0000 | 112.7513 | 132.1413 | 146.7458 | 166.7579 | 179.6198 | 262.3107 | 282.3178 | 331.7844 | 502.1760 |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | charter | 46 | 0.070142 | 6.8917 | 0.0000 | 56.3757 | 66.0706 | 73.3729 | 83.3789 | 89.8099 | 131.1553 | 141.1589 | 165.8922 | 251.0880 |
| ASSET:DOGEUSDT | 4h | ALL | frozen3.0 | maker | 46 | 0.014028 | 6.8917 | 0.0000 | 281.8783 | 330.3531 | 366.8645 | 416.8947 | 449.0494 | 655.7767 | 705.7946 | 829.4609 | 1255.4401 |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | taker | 49 | 0.032502 | 3.7209 | 0.0000 | 46.1493 | 66.0885 | 82.8675 | 101.8446 | 117.4912 | 140.1843 | 176.3068 | 253.7425 | 279.7168 |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | charter | 49 | 0.065004 | 3.7209 | 0.0000 | 23.0747 | 33.0442 | 41.4337 | 50.9223 | 58.7456 | 70.0922 | 88.1534 | 126.8713 | 139.8584 |
| ASSET:DOGEUSDT | 4h | tuning | calibrated | maker | 49 | 0.013001 | 3.7209 | 0.0000 | 115.3733 | 165.2212 | 207.1687 | 254.6116 | 293.7279 | 350.4608 | 440.7669 | 634.3563 | 699.2920 |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | taker | 24 | 0.027610 | 7.2571 | 0.0000 | 122.8845 | 141.6816 | 166.6208 | 192.8914 | 258.7878 | 279.5942 | 432.6264 | 492.4491 | 639.6864 |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | charter | 24 | 0.055219 | 7.2571 | 0.0000 | 61.4422 | 70.8408 | 83.3104 | 96.4457 | 129.3939 | 139.7971 | 216.3132 | 246.2246 | 319.8432 |
| ASSET:DOGEUSDT | 4h | tuning | frozen3.0 | maker | 24 | 0.011044 | 7.2571 | 0.0000 | 307.2112 | 354.2039 | 416.5521 | 482.2286 | 646.9694 | 698.9856 | 1081.5661 | 1231.1229 | 1599.2161 |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | taker | 43 | 0.038986 | 4.2091 | 0.0000 | 72.2960 | 78.7541 | 82.5060 | 95.8637 | 103.4971 | 117.9785 | 160.3130 | 200.5116 | 231.2320 |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | charter | 43 | 0.077972 | 4.2091 | 0.0000 | 36.1480 | 39.3771 | 41.2530 | 47.9319 | 51.7485 | 58.9892 | 80.1565 | 100.2558 | 115.6160 |
| ASSET:DOGEUSDT | 4h | holdout | calibrated | maker | 43 | 0.015594 | 4.2091 | 0.0000 | 180.7399 | 196.8853 | 206.2650 | 239.6594 | 258.7427 | 294.9462 | 400.7824 | 501.2789 | 578.0801 |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | taker | 22 | 0.040857 | 6.0713 | 0.0000 | 109.7604 | 130.8753 | 136.4927 | 152.8279 | 163.3789 | 179.1096 | 238.0170 | 281.6398 | 308.9804 |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | charter | 22 | 0.081714 | 6.0713 | 0.0000 | 54.8802 | 65.4376 | 68.2463 | 76.4139 | 81.6895 | 89.5548 | 119.0085 | 140.8199 | 154.4902 |
| ASSET:DOGEUSDT | 4h | holdout | frozen3.0 | maker | 22 | 0.016343 | 6.0713 | 0.0000 | 274.4009 | 327.1882 | 341.2317 | 382.0697 | 408.4474 | 447.7739 | 595.0425 | 704.0996 | 772.4511 |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | taker | 35 | 0.024037 | 3.8950 | 0.0000 | 101.5789 | 114.2641 | 171.3771 | 178.8414 | 207.0010 | 235.1540 | 265.3421 | 300.4095 | 363.0960 |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | charter | 35 | 0.072111 | 3.8950 | 0.0000 | 33.8596 | 38.0880 | 57.1257 | 59.6138 | 69.0003 | 78.3847 | 88.4474 | 100.1365 | 121.0320 |
| ASSET:1000BONKUSDT | 4h | ALL | calibrated | maker | 35 | 0.009615 | 3.8950 | 0.0000 | 253.9472 | 285.6602 | 428.4428 | 447.1035 | 517.5025 | 587.8850 | 663.3552 | 751.0237 | 907.7401 |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | taker | 20 | 0.028114 | 9.2109 | 0.0000 | 170.4932 | 200.0846 | 240.0278 | 278.2203 | 327.2325 | 362.6680 | 399.3624 | 475.0611 | 646.0631 |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | charter | 20 | 0.084341 | 9.2109 | 0.0000 | 56.8311 | 66.6949 | 80.0093 | 92.7401 | 109.0775 | 120.8893 | 133.1208 | 158.3537 | 215.3544 |
| ASSET:1000BONKUSDT | 4h | ALL | frozen3.0 | maker | 20 | 0.011246 | 9.2109 | 0.0000 | 426.2331 | 500.2115 | 600.0696 | 695.5508 | 818.0813 | 906.6699 | 998.4061 | 1187.6526 | 1615.1579 |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | taker | 9 | 0.013591 | 3.3097 | 0.0000 | 160.8425 | 192.1036 | 204.9471 | 207.7427 | 210.7095 | 298.3248 | 512.1152 | 674.1913 | 749.3000 |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | charter | 9 | 0.040772 | 3.3097 | 0.0000 | 53.6142 | 64.0345 | 68.3157 | 69.2476 | 70.2365 | 99.4416 | 170.7051 | 224.7304 | 249.7667 |
| ASSET:1000BONKUSDT | 4h | tuning | calibrated | maker | 9 | 0.005436 | 3.3097 | 0.0000 | 402.1063 | 480.2590 | 512.3678 | 519.3567 | 526.7737 | 745.8120 | 1280.2879 | 1685.4782 | 1873.2501 |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | taker | 4 | 0.019169 | 11.1490 | 0.0000 | 407.5733 | 479.7227 | 551.8722 | 588.7455 | 607.9808 | 627.2160 | 660.5181 | 721.9536 | 783.3891 |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | charter | 4 | 0.057507 | 11.1490 | 0.0000 | 135.8578 | 159.9076 | 183.9574 | 196.2485 | 202.6603 | 209.0720 | 220.1727 | 240.6512 | 261.1297 |
| ASSET:1000BONKUSDT | 4h | tuning | frozen3.0 | maker | 4 | 0.007668 | 11.1490 | 0.0000 | 1018.9333 | 1199.3069 | 1379.6805 | 1471.8638 | 1519.9519 | 1568.0401 | 1651.2951 | 1804.8840 | 1958.4728 |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | taker | 26 | 0.027095 | 4.7521 | 0.0000 | 97.7045 | 109.4561 | 155.2205 | 171.7493 | 187.0870 | 232.0819 | 249.6779 | 291.0542 | 304.4975 |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | charter | 26 | 0.081285 | 4.7521 | 0.0000 | 32.5682 | 36.4854 | 51.7402 | 57.2498 | 62.3623 | 77.3606 | 83.2260 | 97.0181 | 101.4992 |
| ASSET:1000BONKUSDT | 4h | holdout | calibrated | maker | 26 | 0.010838 | 4.7521 | 0.0000 | 244.2614 | 273.6402 | 388.0513 | 429.3733 | 467.7174 | 580.2048 | 624.1947 | 727.6356 | 761.2437 |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | taker | 16 | 0.030108 | 9.0543 | 0.0000 | 167.3300 | 178.0532 | 218.9390 | 243.3460 | 274.5186 | 319.0412 | 362.7028 | 391.6743 | 433.5736 |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | charter | 16 | 0.090324 | 9.0543 | 0.0000 | 55.7767 | 59.3511 | 72.9797 | 81.1153 | 91.5062 | 106.3471 | 120.9009 | 130.5581 | 144.5245 |
| ASSET:1000BONKUSDT | 4h | holdout | frozen3.0 | maker | 16 | 0.012043 | 9.0543 | 0.0000 | 418.3249 | 445.1330 | 547.3474 | 608.3650 | 686.2964 | 797.6030 | 906.7569 | 979.1858 | 1083.9340 |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | taker | 536 | 0.037909 | 4.0536 | 0.0000 | 50.9134 | 66.5458 | 80.8515 | 94.1895 | 112.1398 | 135.0571 | 159.1501 | 188.6050 | 252.8827 |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | charter | 536 | 0.066110 | 4.0536 | 0.0000 | 32.0441 | 41.2004 | 47.7456 | 55.8824 | 64.6173 | 75.7163 | 87.7107 | 106.5769 | 137.6930 |
| POOLED:CLASSIC5 | 4h | ALL | calibrated | maker | 536 | 0.015164 | 4.0536 | 0.0000 | 127.2835 | 166.3646 | 202.1288 | 235.4736 | 280.3495 | 337.6428 | 397.8752 | 471.5125 | 632.2068 |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | taker | 298 | 0.039006 | 6.3098 | 0.0000 | 81.0576 | 104.3025 | 133.2686 | 151.4340 | 169.4957 | 197.0132 | 231.6712 | 272.5296 | 366.6105 |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | charter | 298 | 0.069559 | 6.3098 | 0.0000 | 52.1179 | 65.8291 | 76.1557 | 86.7234 | 100.4048 | 113.5610 | 127.6806 | 157.2730 | 200.8115 |
| POOLED:CLASSIC5 | 4h | ALL | frozen3.0 | maker | 298 | 0.015603 | 6.3098 | 0.0000 | 202.6440 | 260.7562 | 333.1715 | 378.5851 | 423.7392 | 492.5330 | 579.1781 | 681.3240 | 916.5263 |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | taker | 345 | 0.035642 | 4.0791 | 0.0000 | 52.0589 | 66.9470 | 83.3398 | 98.4382 | 118.8701 | 142.7802 | 169.5328 | 207.3710 | 261.9391 |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | charter | 345 | 0.061222 | 4.0791 | 0.0000 | 32.2544 | 42.5446 | 50.3802 | 59.3435 | 68.5807 | 80.0799 | 92.8651 | 117.3034 | 142.4815 |
| POOLED:CLASSIC5 | 4h | tuning | calibrated | maker | 345 | 0.014257 | 4.0791 | 0.0000 | 130.1471 | 167.3675 | 208.3494 | 246.0955 | 297.1751 | 356.9504 | 423.8320 | 518.4275 | 654.8477 |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | taker | 196 | 0.037824 | 6.0378 | 0.0000 | 81.5218 | 108.5249 | 139.0622 | 154.0304 | 169.4957 | 196.4634 | 227.7182 | 268.2476 | 366.1219 |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | charter | 196 | 0.065695 | 6.0378 | 0.0000 | 52.4435 | 67.0906 | 76.9110 | 86.3553 | 99.6913 | 113.4550 | 126.6934 | 157.3390 | 198.7370 |
| POOLED:CLASSIC5 | 4h | tuning | frozen3.0 | maker | 196 | 0.015130 | 6.0378 | 0.0000 | 203.8046 | 271.3121 | 347.6555 | 385.0761 | 423.7392 | 491.1584 | 569.2954 | 670.6189 | 915.3048 |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | taker | 191 | 0.039956 | 4.0091 | 0.0000 | 49.0566 | 64.8308 | 77.2867 | 87.6664 | 103.5067 | 125.0611 | 142.3729 | 168.8281 | 211.1832 |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | charter | 191 | 0.071900 | 4.0091 | 0.0000 | 32.1174 | 37.9296 | 43.3014 | 52.9570 | 59.4907 | 68.1403 | 80.2905 | 94.0055 | 125.6503 |
| POOLED:CLASSIC5 | 4h | holdout | calibrated | maker | 191 | 0.015982 | 4.0091 | 0.0000 | 122.6414 | 162.0769 | 193.2167 | 219.1660 | 258.7666 | 312.6527 | 355.9322 | 422.0703 | 527.9581 |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | taker | 102 | 0.042066 | 6.8674 | 0.0000 | 79.3108 | 98.6498 | 128.3518 | 141.4034 | 172.3760 | 204.5118 | 236.6962 | 287.3965 | 385.8700 |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | charter | 102 | 0.073879 | 6.8674 | 0.0000 | 52.1230 | 63.1789 | 73.3831 | 91.6398 | 100.4048 | 114.7006 | 127.6177 | 154.6530 | 204.7246 |
| POOLED:CLASSIC5 | 4h | holdout | frozen3.0 | maker | 102 | 0.016827 | 6.8674 | 0.0000 | 198.2771 | 246.6244 | 320.8795 | 353.5084 | 430.9400 | 511.2795 | 591.7405 | 718.4913 | 964.6750 |
| POOLED:PANEL17 | 4h | ALL | calibrated | taker | 1279 | 0.035426 | 4.1345 | 0.0000 | 55.0008 | 72.9531 | 87.5698 | 102.9780 | 118.7719 | 140.5759 | 166.7020 | 206.0765 | 271.1747 |
| POOLED:PANEL17 | 4h | ALL | calibrated | charter | 1279 | 0.071811 | 4.1345 | 0.0000 | 28.6966 | 36.9724 | 44.5965 | 51.7495 | 59.3142 | 68.5664 | 81.0956 | 99.1299 | 132.8178 |
| POOLED:PANEL17 | 4h | ALL | calibrated | maker | 1279 | 0.014170 | 4.1345 | 0.0000 | 137.5019 | 182.3827 | 218.9244 | 257.4451 | 296.9297 | 351.4398 | 416.7549 | 515.1912 | 677.9367 |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | taker | 709 | 0.036448 | 6.5302 | 0.0000 | 88.8371 | 119.0255 | 140.8700 | 160.5882 | 184.3811 | 225.4939 | 262.9424 | 314.1831 | 413.3892 |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | charter | 709 | 0.074419 | 6.5302 | 0.0000 | 48.1579 | 60.0080 | 70.0539 | 80.3811 | 92.4872 | 109.4660 | 126.4323 | 149.5206 | 189.1927 |
| POOLED:PANEL17 | 4h | ALL | frozen3.0 | maker | 709 | 0.014579 | 6.5302 | 0.0000 | 222.0927 | 297.5638 | 352.1751 | 401.4705 | 460.9527 | 563.7348 | 657.3560 | 785.4578 | 1033.4729 |
| POOLED:PANEL17 | 4h | tuning | calibrated | taker | 728 | 0.035504 | 3.9607 | 0.0000 | 53.0702 | 69.4016 | 85.5603 | 101.1268 | 117.4379 | 140.6487 | 167.7856 | 208.9207 | 280.0247 |
| POOLED:PANEL17 | 4h | tuning | calibrated | charter | 728 | 0.066274 | 3.9607 | 0.0000 | 28.4326 | 37.5027 | 45.5320 | 53.8326 | 61.7867 | 72.7086 | 85.9524 | 106.6765 | 145.3757 |
| POOLED:PANEL17 | 4h | tuning | calibrated | maker | 728 | 0.014202 | 3.9607 | 0.0000 | 132.6756 | 173.5041 | 213.9008 | 252.8169 | 293.5946 | 351.6217 | 419.4640 | 522.3017 | 700.0618 |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | taker | 386 | 0.036622 | 6.4043 | 0.0000 | 88.4780 | 115.9184 | 142.3458 | 159.3205 | 180.8851 | 219.1126 | 260.3817 | 329.8969 | 434.2455 |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | charter | 386 | 0.068285 | 6.4043 | 0.0000 | 50.7319 | 63.4530 | 74.3596 | 84.4441 | 97.9947 | 114.2631 | 134.9017 | 166.5844 | 213.5011 |
| POOLED:PANEL17 | 4h | tuning | frozen3.0 | maker | 386 | 0.014649 | 6.4043 | 0.0000 | 221.1951 | 289.7960 | 355.8645 | 398.3014 | 452.2127 | 547.7816 | 650.9542 | 824.7423 | 1085.6137 |
| POOLED:PANEL17 | 4h | holdout | calibrated | taker | 551 | 0.035320 | 4.2856 | 0.0000 | 58.5330 | 77.3054 | 90.4185 | 105.4079 | 122.5104 | 140.0982 | 165.7133 | 201.1946 | 265.6400 |
| POOLED:PANEL17 | 4h | holdout | calibrated | charter | 551 | 0.077681 | 4.2856 | 0.0000 | 29.5001 | 36.8348 | 42.3497 | 49.6121 | 55.9772 | 64.9541 | 75.9559 | 89.2172 | 117.2499 |
| POOLED:PANEL17 | 4h | holdout | calibrated | maker | 551 | 0.014128 | 4.2856 | 0.0000 | 146.3326 | 193.2634 | 226.0462 | 263.5197 | 306.2761 | 350.2456 | 414.2834 | 502.9865 | 664.1001 |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | taker | 323 | 0.036160 | 6.6740 | 0.0000 | 91.3698 | 121.3084 | 139.8316 | 163.0327 | 189.0014 | 228.0551 | 263.9452 | 307.5774 | 391.3146 |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | charter | 323 | 0.079572 | 6.6740 | 0.0000 | 45.9661 | 58.1372 | 65.0981 | 75.3725 | 88.5719 | 101.7348 | 120.6921 | 137.6368 | 166.2264 |
| POOLED:PANEL17 | 4h | holdout | frozen3.0 | maker | 323 | 0.014464 | 6.6740 | 0.0000 | 228.4244 | 303.2711 | 349.5790 | 407.5819 | 472.5034 | 570.1377 | 659.8631 | 768.9436 | 978.2865 |
| ASSET:BTCUSDT | 12h | ALL | calibrated | taker | 34 | 0.033507 | 4.1915 | 0.0000 | 67.9504 | 89.2442 | 99.9250 | 116.7210 | 128.9088 | 149.0331 | 174.1226 | 214.9767 | 264.0398 |
| ASSET:BTCUSDT | 12h | ALL | calibrated | charter | 34 | 0.046910 | 4.1915 | 0.0000 | 48.5360 | 63.7459 | 71.3750 | 83.3722 | 92.0777 | 106.4522 | 124.3733 | 153.5548 | 188.5999 |
| ASSET:BTCUSDT | 12h | ALL | calibrated | maker | 34 | 0.013403 | 4.1915 | 0.0000 | 169.8759 | 223.1105 | 249.8124 | 291.8026 | 322.2719 | 372.5827 | 435.3066 | 537.4418 | 660.0995 |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | taker | 18 | 0.041891 | 7.0875 | 0.0000 | 112.2277 | 122.0897 | 148.0788 | 168.9850 | 202.1418 | 221.0872 | 268.8005 | 289.9856 | 388.0984 |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | charter | 18 | 0.058648 | 7.0875 | 0.0000 | 80.1627 | 87.2069 | 105.7706 | 120.7035 | 144.3870 | 157.9194 | 192.0003 | 207.1325 | 277.2131 |
| ASSET:BTCUSDT | 12h | ALL | frozen3.0 | maker | 18 | 0.016757 | 7.0875 | 0.0000 | 280.5693 | 305.2243 | 370.1970 | 422.4624 | 505.3545 | 552.7179 | 672.0012 | 724.9639 | 970.2459 |
| ASSET:BTCUSDT | 12h | tuning | calibrated | taker | 23 | 0.029096 | 4.2525 | 0.0000 | 72.5142 | 96.6131 | 112.7451 | 135.0693 | 149.8669 | 170.5537 | 209.7985 | 231.0645 | 294.6214 |
| ASSET:BTCUSDT | 12h | tuning | calibrated | charter | 23 | 0.040735 | 4.2525 | 0.0000 | 51.7958 | 69.0093 | 80.5322 | 96.4780 | 107.0478 | 121.8241 | 149.8561 | 165.0461 | 210.4439 |
| ASSET:BTCUSDT | 12h | tuning | calibrated | maker | 23 | 0.011638 | 4.2525 | 0.0000 | 181.2854 | 241.5326 | 281.8627 | 337.6731 | 374.6673 | 426.3843 | 524.4962 | 577.6613 | 736.5536 |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | taker | 10 | 0.030330 | 7.8147 | 0.0000 | 188.3064 | 207.7225 | 213.5931 | 248.5143 | 272.4229 | 284.5454 | 306.4757 | 365.2540 | 586.5381 |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | charter | 10 | 0.042462 | 7.8147 | 0.0000 | 134.5046 | 148.3732 | 152.5665 | 177.5102 | 194.5878 | 203.2467 | 218.9112 | 260.8957 | 418.9558 |
| ASSET:BTCUSDT | 12h | tuning | frozen3.0 | maker | 10 | 0.012132 | 7.8147 | 0.0000 | 470.7660 | 519.3063 | 533.9828 | 621.2858 | 681.0572 | 711.3634 | 766.1894 | 913.1350 | 1466.3454 |
| ASSET:BTCUSDT | 12h | holdout | calibrated | taker | 11 | 0.044187 | 4.1304 | 0.0000 | 69.6338 | 74.3764 | 84.2514 | 92.5728 | 105.5616 | 118.8633 | 125.1188 | 132.0368 | 170.3892 |
| ASSET:BTCUSDT | 12h | holdout | calibrated | charter | 11 | 0.061862 | 4.1304 | 0.0000 | 49.7384 | 53.1260 | 60.1796 | 66.1234 | 75.4011 | 84.9024 | 89.3705 | 94.3120 | 121.7066 |
| ASSET:BTCUSDT | 12h | holdout | calibrated | maker | 11 | 0.017675 | 4.1304 | 0.0000 | 174.0846 | 185.9409 | 210.6285 | 231.4319 | 263.9040 | 297.1583 | 312.7969 | 330.0919 | 425.9730 |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | taker | 8 | 0.044307 | 5.8723 | 0.0000 | 90.0342 | 105.5921 | 118.8994 | 119.1521 | 122.8061 | 131.7700 | 150.6078 | 165.0634 | 195.2478 |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | charter | 8 | 0.062030 | 5.8723 | 0.0000 | 64.3101 | 75.4230 | 84.9282 | 85.1086 | 87.7186 | 94.1214 | 107.5770 | 117.9025 | 139.4627 |
| ASSET:BTCUSDT | 12h | holdout | frozen3.0 | maker | 8 | 0.017723 | 5.8723 | 0.0000 | 225.0855 | 263.9803 | 297.2485 | 297.8803 | 307.0151 | 329.4250 | 376.5195 | 412.6586 | 488.1194 |
| ASSET:ETHUSDT | 12h | ALL | calibrated | taker | 44 | 0.025970 | 3.1989 | 0.0000 | 63.6169 | 77.6468 | 93.7320 | 112.4714 | 125.2035 | 146.0021 | 164.7930 | 197.1301 | 279.4184 |
| ASSET:ETHUSDT | 12h | ALL | calibrated | charter | 44 | 0.036358 | 3.1989 | 0.0000 | 45.4406 | 55.4620 | 66.9514 | 80.3367 | 89.4311 | 104.2872 | 117.7093 | 140.8072 | 199.5845 |
| ASSET:ETHUSDT | 12h | ALL | calibrated | maker | 44 | 0.010388 | 3.1989 | 0.0000 | 159.0422 | 194.1170 | 234.3300 | 281.1785 | 313.0088 | 365.0052 | 411.9825 | 492.8252 | 698.5459 |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | taker | 15 | 0.030193 | 6.7811 | 0.0000 | 129.0902 | 157.1584 | 189.7707 | 196.5718 | 210.9399 | 251.3895 | 324.5582 | 524.9902 | 960.4300 |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | charter | 15 | 0.042270 | 6.7811 | 0.0000 | 92.2073 | 112.2560 | 135.5505 | 140.4085 | 150.6714 | 179.5639 | 231.8273 | 374.9930 | 686.0214 |
| ASSET:ETHUSDT | 12h | ALL | frozen3.0 | maker | 15 | 0.012077 | 6.7811 | 0.0000 | 322.7255 | 392.8961 | 474.4268 | 491.4296 | 527.3498 | 628.4737 | 811.3954 | 1312.4755 | 2401.0750 |
| ASSET:ETHUSDT | 12h | tuning | calibrated | taker | 27 | 0.023685 | 3.2046 | 0.0000 | 63.5903 | 81.2574 | 93.4494 | 112.7565 | 133.1616 | 148.5008 | 169.8391 | 255.6587 | 312.7043 |
| ASSET:ETHUSDT | 12h | tuning | calibrated | charter | 27 | 0.033159 | 3.2046 | 0.0000 | 45.4216 | 58.0410 | 66.7496 | 80.5403 | 95.1154 | 106.0720 | 121.3136 | 182.6134 | 223.3602 |
| ASSET:ETHUSDT | 12h | tuning | calibrated | maker | 27 | 0.009474 | 3.2046 | 0.0000 | 158.9757 | 203.1435 | 233.6236 | 281.8912 | 332.9041 | 371.2520 | 424.5977 | 639.1468 | 781.7607 |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | taker | 8 | 0.028467 | 6.9033 | 0.0000 | 168.5868 | 197.7056 | 211.4847 | 215.2979 | 260.1400 | 309.0590 | 327.1414 | 846.1585 | 1192.3445 |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | charter | 8 | 0.039853 | 6.9033 | 0.0000 | 120.4191 | 141.2183 | 151.0605 | 153.7842 | 185.8143 | 220.7564 | 233.6724 | 604.3989 | 851.6747 |
| ASSET:ETHUSDT | 12h | tuning | frozen3.0 | maker | 8 | 0.011387 | 6.9033 | 0.0000 | 421.4670 | 494.2640 | 528.7117 | 538.2447 | 650.3499 | 772.6474 | 817.8534 | 2115.3962 | 2980.8613 |
| ASSET:ETHUSDT | 12h | holdout | calibrated | taker | 17 | 0.026367 | 3.1674 | 0.0000 | 66.1986 | 77.8281 | 97.7194 | 115.0710 | 123.3257 | 138.6861 | 163.9711 | 180.6904 | 189.1627 |
| ASSET:ETHUSDT | 12h | holdout | calibrated | charter | 17 | 0.036914 | 3.1674 | 0.0000 | 47.2847 | 55.5915 | 69.7996 | 82.1936 | 88.0898 | 99.0615 | 117.1222 | 129.0645 | 135.1162 |
| ASSET:ETHUSDT | 12h | holdout | calibrated | maker | 17 | 0.010547 | 3.1674 | 0.0000 | 165.4964 | 194.5704 | 244.2985 | 287.6775 | 308.3143 | 346.7151 | 409.9278 | 451.7259 | 472.9068 |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | taker | 7 | 0.032916 | 5.3073 | 0.0000 | 132.9383 | 144.9505 | 157.1584 | 174.0657 | 193.3227 | 196.5718 | 259.4677 | 441.6571 | 547.5935 |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | charter | 7 | 0.046082 | 5.3073 | 0.0000 | 94.9559 | 103.5361 | 112.2560 | 124.3327 | 138.0876 | 140.4085 | 185.3341 | 315.4694 | 391.1382 |
| ASSET:ETHUSDT | 12h | holdout | frozen3.0 | maker | 7 | 0.013166 | 5.3073 | 0.0000 | 332.3458 | 362.3762 | 392.8961 | 435.1643 | 483.3067 | 491.4296 | 648.6693 | 1104.1427 | 1368.9837 |
| ASSET:SOLUSDT | 12h | ALL | calibrated | taker | 32 | 0.019065 | 5.1064 | 0.0000 | 145.3286 | 182.1970 | 202.6591 | 243.9931 | 281.6504 | 326.7180 | 367.6485 | 400.1801 | 684.0356 |
| ASSET:SOLUSDT | 12h | ALL | calibrated | charter | 32 | 0.038131 | 5.1064 | 0.0000 | 72.6643 | 91.0985 | 101.3295 | 121.9965 | 140.8252 | 163.3590 | 183.8243 | 200.0900 | 342.0178 |
| ASSET:SOLUSDT | 12h | ALL | calibrated | maker | 32 | 0.007626 | 5.1064 | 0.0000 | 363.3216 | 455.4925 | 506.6477 | 609.9827 | 704.1261 | 816.7951 | 919.1213 | 1000.4502 | 1710.0891 |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | taker | 21 | 0.020464 | 7.6868 | 0.0000 | 235.6510 | 298.5852 | 322.0536 | 347.8120 | 374.0090 | 389.6734 | 473.9675 | 630.6463 | 666.1538 |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | charter | 21 | 0.040928 | 7.6868 | 0.0000 | 117.8255 | 149.2926 | 161.0268 | 173.9060 | 187.0045 | 194.8367 | 236.9837 | 315.3231 | 333.0769 |
| ASSET:SOLUSDT | 12h | ALL | frozen3.0 | maker | 21 | 0.008186 | 7.6868 | 0.0000 | 589.1276 | 746.4629 | 805.1341 | 869.5299 | 935.0225 | 974.1836 | 1184.9187 | 1576.6157 | 1665.3846 |
| ASSET:SOLUSDT | 12h | tuning | calibrated | taker | 21 | 0.018830 | 4.9974 | 0.0000 | 166.2305 | 206.1645 | 247.7327 | 250.6116 | 322.0536 | 347.8120 | 387.7027 | 464.7275 | 720.1860 |
| ASSET:SOLUSDT | 12h | tuning | calibrated | charter | 21 | 0.037660 | 4.9974 | 0.0000 | 83.1153 | 103.0823 | 123.8663 | 125.3058 | 161.0268 | 173.9060 | 193.8513 | 232.3638 | 360.0930 |
| ASSET:SOLUSDT | 12h | tuning | calibrated | maker | 21 | 0.007532 | 4.9974 | 0.0000 | 415.5763 | 515.4113 | 619.3316 | 626.5290 | 805.1341 | 869.5299 | 969.2567 | 1161.8188 | 1800.4651 |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | taker | 14 | 0.019296 | 7.8703 | 0.0000 | 305.6257 | 331.2387 | 346.7670 | 358.0825 | 388.8574 | 400.5742 | 632.8588 | 658.1242 | 703.9764 |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | charter | 14 | 0.038592 | 7.8703 | 0.0000 | 152.8128 | 165.6193 | 173.3835 | 179.0413 | 194.4287 | 200.2871 | 316.4294 | 329.0621 | 351.9882 |
| ASSET:SOLUSDT | 12h | tuning | frozen3.0 | maker | 14 | 0.007718 | 7.8703 | 0.0000 | 764.0642 | 828.0967 | 866.9175 | 895.2063 | 972.1435 | 1001.4356 | 1582.1469 | 1645.3105 | 1759.9409 |
| ASSET:SOLUSDT | 12h | holdout | calibrated | taker | 11 | 0.022494 | 5.2154 | 0.0000 | 139.1526 | 170.3354 | 177.8345 | 199.6470 | 201.1567 | 235.6510 | 312.6893 | 329.8276 | 379.4831 |
| ASSET:SOLUSDT | 12h | holdout | calibrated | charter | 11 | 0.044988 | 5.2154 | 0.0000 | 69.5763 | 85.1677 | 88.9173 | 99.8235 | 100.5784 | 117.8255 | 156.3446 | 164.9138 | 189.7415 |
| ASSET:SOLUSDT | 12h | holdout | calibrated | maker | 11 | 0.008998 | 5.2154 | 0.0000 | 347.8814 | 425.8384 | 444.5863 | 499.1174 | 502.8918 | 589.1276 | 781.7231 | 824.5691 | 948.7077 |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | taker | 7 | 0.025696 | 6.5229 | 0.0000 | 229.1703 | 242.9889 | 265.0024 | 288.4798 | 312.6893 | 349.4811 | 394.0007 | 453.9758 | 507.5969 |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | charter | 7 | 0.051392 | 6.5229 | 0.0000 | 114.5852 | 121.4944 | 132.5012 | 144.2399 | 156.3446 | 174.7406 | 197.0003 | 226.9879 | 253.7985 |
| ASSET:SOLUSDT | 12h | holdout | frozen3.0 | maker | 7 | 0.010278 | 6.5229 | 0.0000 | 572.9258 | 607.4722 | 662.5059 | 721.1995 | 781.7231 | 873.7028 | 985.0017 | 1134.9395 | 1268.9924 |
| ASSET:NEARUSDT | 12h | ALL | calibrated | taker | 36 | 0.017345 | 4.9689 | 0.0000 | 165.1749 | 208.3818 | 231.0877 | 263.8961 | 288.4149 | 378.3537 | 425.3769 | 447.6231 | 541.4916 |
| ASSET:NEARUSDT | 12h | ALL | calibrated | charter | 36 | 0.034691 | 4.9689 | 0.0000 | 82.5874 | 104.1909 | 115.5439 | 131.9481 | 144.2074 | 189.1768 | 212.6885 | 223.8115 | 270.7458 |
| ASSET:NEARUSDT | 12h | ALL | calibrated | maker | 36 | 0.006938 | 4.9689 | 0.0000 | 412.9372 | 520.9546 | 577.7193 | 659.7403 | 721.0372 | 945.8842 | 1063.4423 | 1119.0576 | 1353.7289 |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | taker | 17 | 0.016651 | 7.8588 | 0.0000 | 254.3509 | 388.2985 | 403.4449 | 454.9837 | 493.9385 | 535.9915 | 586.4096 | 858.5024 | 984.9083 |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | charter | 17 | 0.033301 | 7.8588 | 0.0000 | 127.1754 | 194.1492 | 201.7224 | 227.4919 | 246.9693 | 267.9958 | 293.2048 | 429.2512 | 492.4542 |
| ASSET:NEARUSDT | 12h | ALL | frozen3.0 | maker | 17 | 0.006660 | 7.8588 | 0.0000 | 635.8772 | 970.7461 | 1008.6122 | 1137.4594 | 1234.8463 | 1339.9788 | 1466.0239 | 2146.2561 | 2462.2708 |
| ASSET:NEARUSDT | 12h | tuning | calibrated | taker | 20 | 0.016254 | 4.2390 | 0.0000 | 152.8607 | 176.1490 | 200.6998 | 252.4182 | 335.8176 | 384.3954 | 444.2824 | 476.2312 | 609.6465 |
| ASSET:NEARUSDT | 12h | tuning | calibrated | charter | 20 | 0.032507 | 4.2390 | 0.0000 | 76.4303 | 88.0745 | 100.3499 | 126.2091 | 167.9088 | 192.1977 | 222.1412 | 238.1156 | 304.8233 |
| ASSET:NEARUSDT | 12h | tuning | calibrated | maker | 20 | 0.006501 | 4.2390 | 0.0000 | 382.1517 | 440.3725 | 501.7496 | 631.0456 | 839.5440 | 960.9886 | 1110.7059 | 1190.5780 | 1524.1164 |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | taker | 9 | 0.016036 | 7.6328 | 0.0000 | 355.9725 | 400.9482 | 421.0260 | 460.9919 | 530.3491 | 537.8723 | 745.9089 | 890.4830 | 996.8972 |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | charter | 9 | 0.032072 | 7.6328 | 0.0000 | 177.9862 | 200.4741 | 210.5130 | 230.4959 | 265.1746 | 268.9362 | 372.9545 | 445.2415 | 498.4486 |
| ASSET:NEARUSDT | 12h | tuning | frozen3.0 | maker | 9 | 0.006414 | 7.6328 | 0.0000 | 889.9312 | 1002.3704 | 1052.5649 | 1152.4797 | 1325.8729 | 1344.6808 | 1864.7723 | 2226.2074 | 2492.2429 |
| ASSET:NEARUSDT | 12h | holdout | calibrated | taker | 16 | 0.017788 | 5.5872 | 0.0000 | 217.7617 | 228.2282 | 245.1990 | 275.1652 | 279.3830 | 295.2341 | 398.3419 | 441.0786 | 470.7808 |
| ASSET:NEARUSDT | 12h | holdout | calibrated | charter | 16 | 0.035576 | 5.5872 | 0.0000 | 108.8808 | 114.1141 | 122.5995 | 137.5826 | 139.6915 | 147.6170 | 199.1710 | 220.5393 | 235.3904 |
| ASSET:NEARUSDT | 12h | holdout | calibrated | maker | 16 | 0.007115 | 5.5872 | 0.0000 | 544.4042 | 570.5706 | 612.9975 | 687.9129 | 698.4576 | 738.0852 | 995.8548 | 1102.6964 | 1176.9520 |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | taker | 8 | 0.017879 | 8.1237 | 0.0000 | 260.0558 | 321.1057 | 395.5057 | 454.9861 | 482.9595 | 503.7968 | 538.3009 | 672.7687 | 864.5360 |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | charter | 8 | 0.035758 | 8.1237 | 0.0000 | 130.0279 | 160.5528 | 197.7529 | 227.4931 | 241.4798 | 251.8984 | 269.1504 | 336.3843 | 432.2680 |
| ASSET:NEARUSDT | 12h | holdout | frozen3.0 | maker | 8 | 0.007152 | 8.1237 | 0.0000 | 650.1394 | 802.7642 | 988.7644 | 1137.4653 | 1207.3988 | 1259.4921 | 1345.7522 | 1681.9217 | 2161.3399 |
| ASSET:ZECUSDT | 12h | ALL | calibrated | taker | 33 | 0.016548 | 4.6281 | 0.0000 | 155.2789 | 176.1559 | 217.8842 | 288.2177 | 318.8312 | 383.9759 | 410.6649 | 550.8999 | 678.5098 |
| ASSET:ZECUSDT | 12h | ALL | calibrated | charter | 33 | 0.033097 | 4.6281 | 0.0000 | 77.6394 | 88.0780 | 108.9421 | 144.1089 | 159.4156 | 191.9880 | 205.3325 | 275.4499 | 339.2549 |
| ASSET:ZECUSDT | 12h | ALL | calibrated | maker | 33 | 0.006619 | 4.6281 | 0.0000 | 388.1972 | 440.3898 | 544.7104 | 720.5443 | 797.0779 | 959.9398 | 1026.6623 | 1377.2497 | 1696.2745 |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | taker | 21 | 0.015867 | 7.3832 | 0.0000 | 207.1291 | 312.7496 | 395.9276 | 419.0400 | 540.6491 | 680.5242 | 740.4726 | 806.8042 | 1259.9567 |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | charter | 21 | 0.031735 | 7.3832 | 0.0000 | 103.5645 | 156.3748 | 197.9638 | 209.5200 | 270.3246 | 340.2621 | 370.2363 | 403.4021 | 629.9784 |
| ASSET:ZECUSDT | 12h | ALL | frozen3.0 | maker | 21 | 0.006347 | 7.3832 | 0.0000 | 517.8227 | 781.8740 | 989.8190 | 1047.6000 | 1351.6228 | 1701.3106 | 1851.1816 | 2017.0104 | 3149.8918 |
| ASSET:ZECUSDT | 12h | tuning | calibrated | taker | 22 | 0.017519 | 4.7183 | 0.0000 | 132.6929 | 168.3440 | 210.5365 | 246.2708 | 296.8930 | 343.5155 | 397.1138 | 528.7628 | 734.2750 |
| ASSET:ZECUSDT | 12h | tuning | calibrated | charter | 22 | 0.035038 | 4.7183 | 0.0000 | 66.3464 | 84.1720 | 105.2683 | 123.1354 | 148.4465 | 171.7577 | 198.5569 | 264.3814 | 367.1375 |
| ASSET:ZECUSDT | 12h | tuning | calibrated | maker | 22 | 0.007008 | 4.7183 | 0.0000 | 331.7322 | 420.8601 | 526.3413 | 615.6770 | 742.2325 | 858.7887 | 992.7845 | 1321.9070 | 1835.6876 |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | taker | 13 | 0.017780 | 7.4802 | 0.0000 | 242.9623 | 398.5442 | 412.4116 | 420.3753 | 557.7337 | 693.6118 | 770.2988 | 846.9672 | 1182.7139 |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | charter | 13 | 0.035560 | 7.4802 | 0.0000 | 121.4811 | 199.2721 | 206.2058 | 210.1877 | 278.8669 | 346.8059 | 385.1494 | 423.4836 | 591.3569 |
| ASSET:ZECUSDT | 12h | tuning | frozen3.0 | maker | 13 | 0.007112 | 7.4802 | 0.0000 | 607.4057 | 996.3605 | 1031.0291 | 1050.9383 | 1394.3343 | 1734.0294 | 1925.7469 | 2117.4179 | 2956.7847 |
| ASSET:ZECUSDT | 12h | holdout | calibrated | taker | 11 | 0.013842 | 4.6281 | 0.0000 | 166.5139 | 208.5512 | 311.7823 | 332.0347 | 380.9880 | 409.1888 | 505.7255 | 540.6491 | 563.0397 |
| ASSET:ZECUSDT | 12h | holdout | calibrated | charter | 11 | 0.027684 | 4.6281 | 0.0000 | 83.2570 | 104.2756 | 155.8911 | 166.0173 | 190.4940 | 204.5944 | 252.8628 | 270.3246 | 281.5199 |
| ASSET:ZECUSDT | 12h | holdout | calibrated | maker | 11 | 0.005537 | 4.6281 | 0.0000 | 416.2848 | 521.3780 | 779.4557 | 830.0867 | 952.4701 | 1022.9720 | 1264.3138 | 1351.6228 | 1407.5993 |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | taker | 8 | 0.015267 | 7.0352 | 0.0000 | 233.4483 | 271.9366 | 319.5735 | 367.3403 | 460.8186 | 570.6920 | 675.8423 | 720.6291 | 976.6542 |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | charter | 8 | 0.030534 | 7.0352 | 0.0000 | 116.7241 | 135.9683 | 159.7867 | 183.6702 | 230.4093 | 285.3460 | 337.9212 | 360.3146 | 488.3271 |
| ASSET:ZECUSDT | 12h | holdout | frozen3.0 | maker | 8 | 0.006107 | 7.0352 | 0.0000 | 583.6207 | 679.8415 | 798.9336 | 918.3509 | 1152.0464 | 1426.7301 | 1689.6058 | 1801.5728 | 2441.6354 |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | taker | 179 | 0.021294 | 4.2717 | 0.0000 | 90.9178 | 118.6048 | 144.8712 | 170.3461 | 208.3818 | 249.5465 | 313.5122 | 389.2471 | 541.1653 |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | charter | 179 | 0.037079 | 4.2717 | 0.0000 | 58.7349 | 74.9720 | 87.0840 | 103.2827 | 117.6007 | 141.7614 | 169.6113 | 203.2764 | 273.0654 |
| POOLED:CLASSIC5 | 12h | ALL | calibrated | maker | 179 | 0.008517 | 4.2717 | 0.0000 | 227.2945 | 296.5120 | 362.1781 | 425.8653 | 520.9546 | 623.8663 | 783.7805 | 973.1178 | 1352.9132 |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | taker | 92 | 0.021268 | 7.4326 | 0.0000 | 154.0918 | 204.9828 | 238.3741 | 307.4112 | 377.4985 | 413.8006 | 540.3803 | 677.6502 | 899.4040 |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | charter | 92 | 0.039604 | 7.4326 | 0.0000 | 101.5185 | 118.7332 | 149.7062 | 174.4622 | 196.1020 | 219.9222 | 271.2279 | 359.8440 | 449.7020 |
| POOLED:CLASSIC5 | 12h | ALL | frozen3.0 | maker | 92 | 0.008507 | 7.4326 | 0.0000 | 385.2294 | 512.4569 | 595.9353 | 768.5281 | 943.7463 | 1034.5015 | 1350.9508 | 1694.1254 | 2248.5101 |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | taker | 113 | 0.020369 | 4.2485 | 0.0000 | 92.6685 | 119.3218 | 148.1993 | 176.1490 | 211.4430 | 266.9898 | 325.1220 | 394.9398 | 578.2640 |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | charter | 113 | 0.035987 | 4.2485 | 0.0000 | 59.5357 | 75.2780 | 89.6253 | 104.1667 | 123.8663 | 152.2928 | 188.5157 | 215.0051 | 309.9772 |
| POOLED:CLASSIC5 | 12h | tuning | calibrated | maker | 113 | 0.008148 | 4.2485 | 0.0000 | 231.6714 | 298.3044 | 370.4982 | 440.3725 | 528.6076 | 667.4745 | 812.8050 | 987.3495 | 1445.6601 |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | taker | 54 | 0.019817 | 7.6598 | 0.0000 | 203.4113 | 215.6383 | 303.5899 | 348.3681 | 399.1984 | 439.0639 | 632.8588 | 770.2988 | 971.5218 |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | charter | 54 | 0.038054 | 7.6598 | 0.0000 | 114.2243 | 152.3471 | 175.1574 | 196.9760 | 209.9373 | 234.0662 | 327.0547 | 396.2218 | 589.1702 |
| POOLED:CLASSIC5 | 12h | tuning | frozen3.0 | maker | 54 | 0.007927 | 7.6598 | 0.0000 | 508.5281 | 539.0956 | 758.9748 | 870.9204 | 997.9959 | 1097.6597 | 1582.1469 | 1925.7469 | 2428.8046 |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | taker | 66 | 0.022531 | 4.4832 | 0.0000 | 79.3139 | 118.8633 | 137.3348 | 170.3354 | 199.1925 | 228.2282 | 279.3830 | 379.4831 | 470.7808 |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | charter | 66 | 0.037345 | 4.4832 | 0.0000 | 56.6528 | 75.4011 | 85.2945 | 99.8235 | 114.1504 | 129.1145 | 148.4029 | 189.7415 | 235.3904 |
| POOLED:CLASSIC5 | 12h | holdout | calibrated | maker | 66 | 0.009012 | 4.4832 | 0.0000 | 198.2847 | 297.1583 | 343.3369 | 425.8384 | 497.9811 | 570.5706 | 698.4576 | 948.7077 | 1176.9520 |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | taker | 38 | 0.025293 | 6.9087 | 0.0000 | 120.4841 | 156.4704 | 199.5771 | 232.5451 | 274.7553 | 375.4048 | 473.7688 | 542.1977 | 705.7465 |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | charter | 38 | 0.043395 | 6.9087 | 0.0000 | 86.0601 | 105.9384 | 115.4290 | 133.6370 | 149.1502 | 187.7024 | 236.8844 | 276.0583 | 373.0346 |
| POOLED:CLASSIC5 | 12h | holdout | frozen3.0 | maker | 38 | 0.010117 | 6.9087 | 0.0000 | 301.2104 | 391.1761 | 498.9427 | 581.3629 | 686.8883 | 938.5120 | 1184.4220 | 1355.4941 | 1764.3661 |
| ASSET:BTCUSDT | 1d | ALL | calibrated | taker | 20 | 0.026489 | 5.1225 | 0.0000 | 97.9712 | 118.0154 | 165.4963 | 202.5264 | 214.6702 | 231.5359 | 250.3367 | 276.3616 | 331.4831 |
| ASSET:BTCUSDT | 1d | ALL | calibrated | charter | 20 | 0.037085 | 5.1225 | 0.0000 | 69.9795 | 84.2967 | 118.2116 | 144.6617 | 153.3359 | 165.3828 | 178.8120 | 197.4011 | 236.7736 |
| ASSET:BTCUSDT | 1d | ALL | calibrated | maker | 20 | 0.010596 | 5.1225 | 0.0000 | 244.9281 | 295.0385 | 413.7406 | 506.3159 | 536.6756 | 578.8397 | 625.8419 | 690.9040 | 828.7077 |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | taker | 11 | 0.025383 | 5.5362 | 0.0000 | 177.9749 | 190.8073 | 207.3699 | 209.5816 | 263.1757 | 272.8942 | 288.8750 | 308.8770 | 436.8702 |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | charter | 11 | 0.035536 | 5.5362 | 0.0000 | 127.1249 | 136.2909 | 148.1213 | 149.7011 | 187.9827 | 194.9245 | 206.3393 | 220.6264 | 312.0502 |
| ASSET:BTCUSDT | 1d | ALL | frozen3.0 | maker | 11 | 0.010153 | 5.5362 | 0.0000 | 444.9372 | 477.0181 | 518.4247 | 523.9540 | 657.9393 | 682.2356 | 722.1875 | 772.1924 | 1092.1755 |
| ASSET:BTCUSDT | 1d | tuning | calibrated | taker | 12 | 0.021296 | 5.3262 | 0.0000 | 179.7035 | 197.6829 | 211.0866 | 224.8131 | 238.6143 | 255.8392 | 269.9787 | 301.6804 | 512.3322 |
| ASSET:BTCUSDT | 1d | tuning | calibrated | charter | 12 | 0.029815 | 5.3262 | 0.0000 | 128.3597 | 141.2020 | 150.7761 | 160.5808 | 170.4388 | 182.7423 | 192.8419 | 215.4860 | 365.9516 |
| ASSET:BTCUSDT | 1d | tuning | calibrated | maker | 12 | 0.008519 | 5.3262 | 0.0000 | 449.2588 | 494.2071 | 527.7165 | 562.0327 | 596.5359 | 639.5979 | 674.9467 | 754.2010 | 1280.8306 |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | taker | 8 | 0.020547 | 5.4532 | 0.0000 | 186.9575 | 197.4323 | 212.9505 | 252.0146 | 268.0350 | 280.0908 | 305.2787 | 385.6729 | 473.2137 |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | charter | 8 | 0.028766 | 5.4532 | 0.0000 | 133.5411 | 141.0231 | 152.1075 | 180.0104 | 191.4536 | 200.0648 | 218.0562 | 275.4806 | 338.0098 |
| ASSET:BTCUSDT | 1d | tuning | frozen3.0 | maker | 8 | 0.008219 | 5.4532 | 0.0000 | 467.3939 | 493.5808 | 532.3762 | 630.0364 | 670.0874 | 700.2269 | 763.1967 | 964.1823 | 1183.0341 |
| ASSET:BTCUSDT | 1d | holdout | calibrated | taker | 8 | 0.031736 | 4.3635 | 0.0000 | 97.5016 | 103.4796 | 112.2182 | 118.0154 | 128.0256 | 151.0199 | 202.2614 | 222.4108 | 248.7438 |
| ASSET:BTCUSDT | 1d | holdout | calibrated | charter | 8 | 0.044431 | 4.3635 | 0.0000 | 69.6440 | 73.9140 | 80.1559 | 84.2967 | 91.4468 | 107.8713 | 144.4724 | 158.8649 | 177.6741 |
| ASSET:BTCUSDT | 1d | holdout | calibrated | maker | 8 | 0.012695 | 4.3635 | 0.0000 | 243.7541 | 258.6991 | 280.5456 | 295.0385 | 320.0639 | 377.5497 | 505.6535 | 556.0270 | 621.8595 |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | taker | 3 | 0.027965 | 5.7295 | 0.0000 | 140.8861 | 158.0600 | 175.2339 | 192.4077 | 209.5816 | 225.4403 | 241.2990 | 257.1576 | 273.0163 |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | charter | 3 | 0.039152 | 5.7295 | 0.0000 | 100.6330 | 112.9000 | 125.1671 | 137.4341 | 149.7011 | 161.0288 | 172.3564 | 183.6840 | 195.0117 |
| ASSET:BTCUSDT | 1d | holdout | frozen3.0 | maker | 3 | 0.011186 | 5.7295 | 0.0000 | 352.2154 | 395.1500 | 438.0847 | 481.0194 | 523.9540 | 563.6007 | 603.2474 | 642.8941 | 682.5408 |
| ASSET:ETHUSDT | 1d | ALL | calibrated | taker | 20 | 0.017755 | 3.9986 | 0.0000 | 116.1830 | 135.4965 | 148.7558 | 180.4847 | 208.0272 | 270.3080 | 295.2674 | 328.5751 | 507.3486 |
| ASSET:ETHUSDT | 1d | ALL | calibrated | charter | 20 | 0.024857 | 3.9986 | 0.0000 | 82.9878 | 96.7832 | 106.2542 | 128.9177 | 148.5908 | 193.0771 | 210.9053 | 234.6965 | 362.3919 |
| ASSET:ETHUSDT | 1d | ALL | calibrated | maker | 20 | 0.007102 | 3.9986 | 0.0000 | 290.4574 | 338.7413 | 371.8895 | 451.2118 | 520.0680 | 675.7700 | 738.1686 | 821.4376 | 1268.3715 |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | taker | 9 | 0.022434 | 7.5285 | 0.0000 | 260.8811 | 300.6535 | 331.3084 | 351.1585 | 355.7785 | 506.3981 | 606.1319 | 653.2188 | 707.9975 |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | charter | 9 | 0.031407 | 7.5285 | 0.0000 | 186.3436 | 214.7525 | 236.6488 | 250.8275 | 254.1275 | 361.7129 | 432.9513 | 466.5848 | 505.7125 |
| ASSET:ETHUSDT | 1d | ALL | frozen3.0 | maker | 9 | 0.008974 | 7.5285 | 0.0000 | 652.2027 | 751.6338 | 828.2710 | 877.8963 | 889.4463 | 1265.9953 | 1515.3297 | 1633.0470 | 1769.9937 |
| ASSET:ETHUSDT | 1d | tuning | calibrated | taker | 13 | 0.017516 | 3.9886 | 0.0000 | 113.8432 | 117.3529 | 138.4389 | 199.0840 | 268.2691 | 276.2191 | 297.8133 | 319.1285 | 344.8342 |
| ASSET:ETHUSDT | 1d | tuning | calibrated | charter | 13 | 0.024522 | 3.9886 | 0.0000 | 81.3166 | 83.8235 | 98.8849 | 142.2029 | 191.6208 | 197.2993 | 212.7238 | 227.9489 | 246.3102 |
| ASSET:ETHUSDT | 1d | tuning | calibrated | maker | 13 | 0.007006 | 3.9886 | 0.0000 | 284.6080 | 293.3824 | 346.0973 | 497.7101 | 670.6727 | 690.5477 | 744.5331 | 797.8213 | 862.0855 |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | taker | 6 | 0.023997 | 8.0355 | 0.0000 | 242.1531 | 273.3664 | 311.6850 | 350.0035 | 352.8910 | 355.7785 | 501.6481 | 647.5178 | 770.2120 |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | charter | 6 | 0.033596 | 8.0355 | 0.0000 | 172.9665 | 195.2617 | 222.6321 | 250.0025 | 252.0650 | 254.1275 | 358.3201 | 462.5127 | 550.1514 |
| ASSET:ETHUSDT | 1d | tuning | frozen3.0 | maker | 6 | 0.009599 | 8.0355 | 0.0000 | 605.3829 | 683.4159 | 779.2124 | 875.0089 | 882.2276 | 889.4463 | 1254.1204 | 1618.7945 | 1925.5300 |
| ASSET:ETHUSDT | 1d | holdout | calibrated | taker | 7 | 0.019156 | 4.4066 | 0.0000 | 141.0746 | 145.8282 | 157.3779 | 174.0657 | 193.3227 | 200.3977 | 264.5817 | 442.9836 | 522.0417 |
| ASSET:ETHUSDT | 1d | holdout | calibrated | charter | 7 | 0.026818 | 4.4066 | 0.0000 | 100.7676 | 104.1630 | 112.4128 | 124.3327 | 138.0876 | 143.1412 | 188.9870 | 316.4169 | 372.8869 |
| ASSET:ETHUSDT | 1d | holdout | calibrated | maker | 7 | 0.007662 | 4.4066 | 0.0000 | 352.6865 | 364.5705 | 393.4447 | 435.1643 | 483.3067 | 500.9944 | 661.4543 | 1107.4591 | 1305.1043 |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | taker | 3 | 0.022434 | 7.5285 | 0.0000 | 363.8866 | 408.9282 | 453.9698 | 499.0114 | 544.0530 | 567.5965 | 591.1399 | 614.6834 | 638.2268 |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | charter | 3 | 0.031407 | 7.5285 | 0.0000 | 259.9190 | 292.0916 | 324.2641 | 356.4367 | 388.6093 | 405.4261 | 422.2428 | 439.0596 | 455.8763 |
| ASSET:ETHUSDT | 1d | holdout | frozen3.0 | maker | 3 | 0.008974 | 7.5285 | 0.0000 | 909.7164 | 1022.3204 | 1134.9245 | 1247.5285 | 1360.1326 | 1418.9912 | 1477.8498 | 1536.7085 | 1595.5671 |
| ASSET:SOLUSDT | 1d | ALL | calibrated | taker | 18 | 0.014748 | 5.0582 | 0.0000 | 263.8958 | 300.0014 | 321.3393 | 337.9812 | 355.3771 | 365.3317 | 387.5597 | 536.1425 | 597.2202 |
| ASSET:SOLUSDT | 1d | ALL | calibrated | charter | 18 | 0.029497 | 5.0582 | 0.0000 | 131.9479 | 150.0007 | 160.6696 | 168.9906 | 177.6885 | 182.6658 | 193.7798 | 268.0712 | 298.6101 |
| ASSET:SOLUSDT | 1d | ALL | calibrated | maker | 18 | 0.005899 | 5.0582 | 0.0000 | 659.7395 | 750.0034 | 803.3482 | 844.9530 | 888.4426 | 913.3292 | 968.8992 | 1340.3562 | 1493.0504 |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | taker | 12 | 0.017586 | 5.9992 | 0.0000 | 280.2846 | 317.1076 | 331.5516 | 360.9251 | 364.5075 | 371.1697 | 496.3550 | 602.9647 | 638.5847 |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | charter | 12 | 0.035171 | 5.9992 | 0.0000 | 140.1423 | 158.5538 | 165.7758 | 180.4625 | 182.2537 | 185.5848 | 248.1775 | 301.4823 | 319.2924 |
| ASSET:SOLUSDT | 1d | ALL | frozen3.0 | maker | 12 | 0.007034 | 5.9992 | 0.0000 | 700.7114 | 792.7689 | 828.8789 | 902.3127 | 911.2686 | 927.9242 | 1240.8874 | 1507.4117 | 1596.4618 |
| ASSET:SOLUSDT | 1d | tuning | calibrated | taker | 11 | 0.013153 | 4.9541 | 0.0000 | 316.4947 | 337.3620 | 338.1360 | 351.2198 | 359.5343 | 363.0112 | 577.5924 | 592.1659 | 609.0135 |
| ASSET:SOLUSDT | 1d | tuning | calibrated | charter | 11 | 0.026305 | 4.9541 | 0.0000 | 158.2474 | 168.6810 | 169.0680 | 175.6099 | 179.7672 | 181.5056 | 288.7962 | 296.0829 | 304.5067 |
| ASSET:SOLUSDT | 1d | tuning | calibrated | maker | 11 | 0.005261 | 4.9541 | 0.0000 | 791.2368 | 843.4051 | 845.3399 | 878.0495 | 898.8358 | 907.5280 | 1443.9811 | 1480.4147 | 1522.5337 |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | taker | 6 | 0.015451 | 6.4856 | 0.0000 | 338.0145 | 359.5343 | 361.2728 | 363.0112 | 455.7705 | 548.5298 | 594.7801 | 641.0304 | 4375.2388 |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | charter | 6 | 0.030901 | 6.4856 | 0.0000 | 169.0073 | 179.7672 | 180.6364 | 181.5056 | 227.8853 | 274.2649 | 297.3901 | 320.5152 | 2187.6194 |
| ASSET:SOLUSDT | 1d | tuning | frozen3.0 | maker | 6 | 0.006180 | 6.4856 | 0.0000 | 845.0363 | 898.8358 | 903.1819 | 907.5280 | 1139.4263 | 1371.3246 | 1486.9503 | 1602.5760 | 10938.0970 |
| ASSET:SOLUSDT | 1d | holdout | calibrated | taker | 7 | 0.017990 | 5.1624 | 0.0000 | 231.5087 | 243.2868 | 268.0176 | 293.5803 | 319.5590 | 352.5918 | 377.4906 | 386.1212 | 422.9859 |
| ASSET:SOLUSDT | 1d | holdout | calibrated | charter | 7 | 0.035979 | 5.1624 | 0.0000 | 115.7544 | 121.6434 | 134.0088 | 146.7902 | 159.7795 | 176.2959 | 188.7453 | 193.0606 | 211.4929 |
| ASSET:SOLUSDT | 1d | holdout | calibrated | maker | 7 | 0.007196 | 5.1624 | 0.0000 | 578.7718 | 608.2169 | 670.0440 | 733.9508 | 798.8974 | 881.4795 | 943.7264 | 965.3031 | 1057.4647 |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | taker | 6 | 0.019422 | 5.7550 | 0.0000 | 254.0073 | 276.2612 | 297.9101 | 319.5590 | 342.7813 | 366.0037 | 370.3087 | 374.6137 | 495.5935 |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | charter | 6 | 0.038844 | 5.7550 | 0.0000 | 127.0037 | 138.1306 | 148.9550 | 159.7795 | 171.3907 | 183.0019 | 185.1543 | 187.3068 | 247.7968 |
| ASSET:SOLUSDT | 1d | holdout | frozen3.0 | maker | 6 | 0.007769 | 5.7550 | 0.0000 | 635.0183 | 690.6531 | 744.7752 | 798.8974 | 856.9533 | 915.0093 | 925.7717 | 936.5342 | 1238.9838 |
| ASSET:NEARUSDT | 1d | ALL | calibrated | taker | 16 | 0.012770 | 4.9958 | 0.0000 | 210.2142 | 269.8810 | 294.3033 | 380.5584 | 382.7558 | 404.0946 | 485.0015 | 708.0646 | 814.0837 |
| ASSET:NEARUSDT | 1d | ALL | calibrated | charter | 16 | 0.025541 | 4.9958 | 0.0000 | 105.1071 | 134.9405 | 147.1517 | 190.2792 | 191.3779 | 202.0473 | 242.5007 | 354.0323 | 407.0419 |
| ASSET:NEARUSDT | 1d | ALL | calibrated | maker | 16 | 0.005108 | 4.9958 | 0.0000 | 525.5354 | 674.7026 | 735.7583 | 951.3961 | 956.8895 | 1010.2364 | 1212.5037 | 1770.1616 | 2035.2093 |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | taker | 8 | 0.012526 | 7.0094 | 0.0000 | 349.4287 | 424.7050 | 470.3933 | 573.8024 | 667.5462 | 738.6270 | 762.7162 | 844.3168 | 1007.9440 |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | charter | 8 | 0.025052 | 7.0094 | 0.0000 | 174.7143 | 212.3525 | 235.1966 | 286.9012 | 333.7731 | 369.3135 | 381.3581 | 422.1584 | 503.9720 |
| ASSET:NEARUSDT | 1d | ALL | frozen3.0 | maker | 8 | 0.005010 | 7.0094 | 0.0000 | 873.5717 | 1061.7624 | 1175.9832 | 1434.5061 | 1668.8654 | 1846.5676 | 1906.7904 | 2110.7920 | 2519.8601 |
| ASSET:NEARUSDT | 1d | tuning | calibrated | taker | 11 | 0.012328 | 4.8779 | 0.0000 | 201.3423 | 278.0105 | 310.5961 | 382.1129 | 383.3987 | 404.0946 | 455.6206 | 708.0646 | 896.4230 |
| ASSET:NEARUSDT | 1d | tuning | calibrated | charter | 11 | 0.024656 | 4.8779 | 0.0000 | 100.6711 | 139.0052 | 155.2981 | 191.0564 | 191.6994 | 202.0473 | 227.8103 | 354.0323 | 448.2115 |
| ASSET:NEARUSDT | 1d | tuning | calibrated | maker | 11 | 0.004931 | 4.8779 | 0.0000 | 503.3557 | 695.0262 | 776.4903 | 955.2822 | 958.4968 | 1010.2364 | 1139.0514 | 1770.1616 | 2241.0575 |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | taker | 6 | 0.013214 | 5.6572 | 0.0000 | 312.9848 | 404.0946 | 429.8576 | 455.6206 | 529.4842 | 603.3479 | 749.8855 | 896.4230 | 1082.2914 |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | charter | 6 | 0.026427 | 5.6572 | 0.0000 | 156.4924 | 202.0473 | 214.9288 | 227.8103 | 264.7421 | 301.6739 | 374.9427 | 448.2115 | 541.1457 |
| ASSET:NEARUSDT | 1d | tuning | frozen3.0 | maker | 6 | 0.005286 | 5.6572 | 0.0000 | 782.4620 | 1010.2364 | 1074.6439 | 1139.0514 | 1323.7106 | 1508.3697 | 1874.7136 | 2241.0575 | 2705.7285 |
| ASSET:NEARUSDT | 1d | holdout | calibrated | taker | 5 | 0.014252 | 5.7672 | 0.0000 | 239.4040 | 259.7220 | 292.0165 | 336.2875 | 380.5584 | 434.0880 | 487.6176 | 557.8548 | 644.7996 |
| ASSET:NEARUSDT | 1d | holdout | calibrated | charter | 5 | 0.028505 | 5.7672 | 0.0000 | 119.7020 | 129.8610 | 146.0083 | 168.1437 | 190.2792 | 217.0440 | 243.8088 | 278.9274 | 322.3998 |
| ASSET:NEARUSDT | 1d | holdout | calibrated | maker | 5 | 0.005701 | 5.7672 | 0.0000 | 598.5101 | 649.3051 | 730.0413 | 840.7187 | 951.3961 | 1085.2200 | 1219.0440 | 1394.6370 | 1611.9990 |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | taker | 2 | 0.012048 | 9.0351 | 0.0000 | 735.1857 | 738.6270 | 742.0683 | 745.5096 | 748.9509 | 752.3922 | 755.8335 | 759.2749 | 762.7162 |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | charter | 2 | 0.024096 | 9.0351 | 0.0000 | 367.5929 | 369.3135 | 371.0342 | 372.7548 | 374.4755 | 376.1961 | 377.9168 | 379.6374 | 381.3581 |
| ASSET:NEARUSDT | 1d | holdout | frozen3.0 | maker | 2 | 0.004819 | 9.0351 | 0.0000 | 1837.9643 | 1846.5676 | 1855.1708 | 1863.7741 | 1872.3774 | 1880.9806 | 1889.5839 | 1898.1871 | 1906.7904 |
| ASSET:ZECUSDT | 1d | ALL | calibrated | taker | 19 | 0.012500 | 5.6389 | 0.0000 | 337.6024 | 355.9030 | 373.3407 | 392.9738 | 418.4012 | 556.4028 | 614.1518 | 651.9173 | 700.9513 |
| ASSET:ZECUSDT | 1d | ALL | calibrated | charter | 19 | 0.025000 | 5.6389 | 0.0000 | 168.8012 | 177.9515 | 186.6703 | 196.4869 | 209.2006 | 278.2014 | 307.0759 | 325.9586 | 350.4757 |
| ASSET:ZECUSDT | 1d | ALL | calibrated | maker | 19 | 0.005000 | 5.6389 | 0.0000 | 844.0059 | 889.7574 | 933.3517 | 982.4345 | 1046.0030 | 1391.0071 | 1535.3796 | 1629.7932 | 1752.3783 |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | taker | 13 | 0.012599 | 6.1467 | 0.0000 | 360.9120 | 415.7555 | 474.5154 | 595.6168 | 634.3795 | 650.3026 | 666.2665 | 994.3759 | 1220.1256 |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | charter | 13 | 0.025198 | 6.1467 | 0.0000 | 180.4560 | 207.8778 | 237.2577 | 297.8084 | 317.1898 | 325.1513 | 333.1333 | 497.1880 | 610.0628 |
| ASSET:ZECUSDT | 1d | ALL | frozen3.0 | maker | 13 | 0.005040 | 6.1467 | 0.0000 | 902.2800 | 1039.3889 | 1186.2885 | 1489.0419 | 1585.9488 | 1625.7565 | 1665.6664 | 2485.9398 | 3050.3140 |
| ASSET:ZECUSDT | 1d | tuning | calibrated | taker | 13 | 0.012500 | 4.9687 | 0.0000 | 348.0766 | 358.0083 | 374.8617 | 385.7562 | 413.9918 | 437.1059 | 551.3829 | 638.2848 | 675.7717 |
| ASSET:ZECUSDT | 1d | tuning | calibrated | charter | 13 | 0.025000 | 4.9687 | 0.0000 | 174.0383 | 179.0041 | 187.4308 | 192.8781 | 206.9959 | 218.5530 | 275.6915 | 319.1424 | 337.8858 |
| ASSET:ZECUSDT | 1d | tuning | calibrated | maker | 13 | 0.005000 | 4.9687 | 0.0000 | 870.1915 | 895.0206 | 937.1541 | 964.3904 | 1034.9794 | 1092.7649 | 1378.4573 | 1595.7121 | 1689.4292 |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | taker | 9 | 0.013293 | 6.1467 | 0.0000 | 347.3138 | 387.4519 | 415.7555 | 437.1059 | 511.9249 | 609.8886 | 647.8087 | 666.2665 | 789.2703 |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | charter | 9 | 0.026586 | 6.1467 | 0.0000 | 173.6569 | 193.7259 | 207.8778 | 218.5530 | 255.9624 | 304.9443 | 323.9043 | 333.1333 | 394.6351 |
| ASSET:ZECUSDT | 1d | tuning | frozen3.0 | maker | 9 | 0.005317 | 6.1467 | 0.0000 | 868.2844 | 968.6297 | 1039.3889 | 1092.7649 | 1279.8122 | 1524.7215 | 1619.5216 | 1665.6664 | 1973.1757 |
| ASSET:ZECUSDT | 1d | holdout | calibrated | taker | 6 | 0.011340 | 5.8668 | 0.0000 | 328.7027 | 359.9619 | 463.7421 | 567.5223 | 592.0310 | 616.5397 | 632.6138 | 648.6879 | 926.1491 |
| ASSET:ZECUSDT | 1d | holdout | calibrated | charter | 6 | 0.022681 | 5.8668 | 0.0000 | 164.3513 | 179.9809 | 231.8711 | 283.7612 | 296.0155 | 308.2699 | 316.3069 | 324.3439 | 463.0746 |
| ASSET:ZECUSDT | 1d | holdout | calibrated | maker | 6 | 0.004536 | 5.8668 | 0.0000 | 821.7567 | 899.9047 | 1159.3553 | 1418.8058 | 1480.0776 | 1541.3493 | 1581.5345 | 1621.7197 | 2315.3728 |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | taker | 4 | 0.008205 | 7.5080 | 0.0000 | 626.1842 | 635.8286 | 645.4731 | 759.6724 | 926.1491 | 1092.6259 | 1221.9171 | 1276.8374 | 1331.7577 |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | charter | 4 | 0.016411 | 7.5080 | 0.0000 | 313.0921 | 317.9143 | 322.7365 | 379.8362 | 463.0746 | 546.3129 | 610.9586 | 638.4187 | 665.8788 |
| ASSET:ZECUSDT | 1d | holdout | frozen3.0 | maker | 4 | 0.003282 | 7.5080 | 0.0000 | 1565.4604 | 1589.5715 | 1613.6827 | 1899.1809 | 2315.3728 | 2731.5647 | 3054.7928 | 3192.0935 | 3329.3942 |
| ASSET:ENAUSDT | 1d | ALL | calibrated | taker | 6 | 0.011432 | 3.8495 | 0.0000 | 294.0800 | 298.3901 | 302.5492 | 306.7083 | 380.3142 | 453.9202 | 475.1271 | 496.3339 | 562.6303 |
| ASSET:ENAUSDT | 1d | ALL | calibrated | charter | 6 | 0.034297 | 3.8495 | 0.0000 | 98.0267 | 99.4634 | 100.8497 | 102.2361 | 126.7714 | 151.3067 | 158.3757 | 165.4446 | 187.5434 |
| ASSET:ENAUSDT | 1d | ALL | calibrated | maker | 6 | 0.004573 | 3.8495 | 0.0000 | 735.2001 | 745.9753 | 756.3730 | 766.7707 | 950.7856 | 1134.8006 | 1187.8176 | 1240.8347 | 1406.5757 |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | taker | 1 | 0.007778 | 34.2044 | 0.0000 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | charter | 1 | 0.023333 | 34.2044 | 0.0000 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 |
| ASSET:ENAUSDT | 1d | ALL | frozen3.0 | maker | 1 | 0.003111 | 34.2044 | 0.0000 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 |
| ASSET:ENAUSDT | 1d | tuning | calibrated | taker | 1 | 0.007946 | 3.9440 | 0.0000 | 496.3339 | 496.3339 | 496.3339 | 496.3339 | 496.3339 | 496.3339 | 496.3339 | 496.3339 | 496.3339 |
| ASSET:ENAUSDT | 1d | tuning | calibrated | charter | 1 | 0.023839 | 3.9440 | 0.0000 | 165.4446 | 165.4446 | 165.4446 | 165.4446 | 165.4446 | 165.4446 | 165.4446 | 165.4446 | 165.4446 |
| ASSET:ENAUSDT | 1d | tuning | calibrated | maker | 1 | 0.003179 | 3.9440 | 0.0000 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 | 1240.8347 |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ENAUSDT | 1d | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ENAUSDT | 1d | holdout | calibrated | taker | 5 | 0.011749 | 3.7549 | 0.0000 | 293.2180 | 296.6661 | 300.0537 | 303.3810 | 306.7083 | 365.5930 | 424.4778 | 488.9215 | 558.9241 |
| ASSET:ENAUSDT | 1d | holdout | calibrated | charter | 5 | 0.035248 | 3.7549 | 0.0000 | 97.7393 | 98.8887 | 100.0179 | 101.1270 | 102.2361 | 121.8643 | 141.4926 | 162.9738 | 186.3080 |
| ASSET:ENAUSDT | 1d | holdout | calibrated | maker | 5 | 0.004700 | 3.7549 | 0.0000 | 733.0450 | 741.6652 | 750.1344 | 758.4525 | 766.7707 | 913.9826 | 1061.1946 | 1222.3038 | 1397.3103 |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | taker | 1 | 0.007778 | 34.2044 | 0.0000 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 | 4397.7320 |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | charter | 1 | 0.023333 | 34.2044 | 0.0000 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 | 1465.9107 |
| ASSET:ENAUSDT | 1d | holdout | frozen3.0 | maker | 1 | 0.003111 | 34.2044 | 0.0000 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 | 10994.3301 |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | taker | 3 | 0.005888 | 3.5411 | 0.0000 | 467.4636 | 499.1154 | 530.7671 | 562.4189 | 594.0707 | 624.5567 | 655.0427 | 685.5287 | 716.0148 |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | charter | 3 | 0.017663 | 3.5411 | 0.0000 | 155.8212 | 166.3718 | 176.9224 | 187.4730 | 198.0236 | 208.1856 | 218.3476 | 228.5096 | 238.6716 |
| ASSET:PUMPUSDT | 1d | ALL | calibrated | maker | 3 | 0.002355 | 3.5411 | 0.0000 | 1168.6589 | 1247.7884 | 1326.9178 | 1406.0473 | 1485.1767 | 1561.3918 | 1637.6068 | 1713.8219 | 1790.0369 |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | taker | 2 | 0.008458 | 5.7418 | 0.0000 | 560.2325 | 651.8773 | 743.5221 | 835.1670 | 926.8118 | 1018.4567 | 1110.1015 | 1201.7464 | 1293.3912 |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | charter | 2 | 0.025375 | 5.7418 | 0.0000 | 186.7442 | 217.2924 | 247.8407 | 278.3890 | 308.9373 | 339.4856 | 370.0338 | 400.5821 | 431.1304 |
| ASSET:PUMPUSDT | 1d | ALL | frozen3.0 | maker | 2 | 0.003383 | 5.7418 | 0.0000 | 1400.5812 | 1629.6933 | 1858.8054 | 2087.9175 | 2317.0296 | 2546.1417 | 2775.2538 | 3004.3659 | 3233.4780 |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | taker | 3 | 0.005888 | 3.5411 | 0.0000 | 467.4636 | 499.1154 | 530.7671 | 562.4189 | 594.0707 | 624.5567 | 655.0427 | 685.5287 | 716.0148 |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | charter | 3 | 0.017663 | 3.5411 | 0.0000 | 155.8212 | 166.3718 | 176.9224 | 187.4730 | 198.0236 | 208.1856 | 218.3476 | 228.5096 | 238.6716 |
| ASSET:PUMPUSDT | 1d | holdout | calibrated | maker | 3 | 0.002355 | 3.5411 | 0.0000 | 1168.6589 | 1247.7884 | 1326.9178 | 1406.0473 | 1485.1767 | 1561.3918 | 1637.6068 | 1713.8219 | 1790.0369 |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | taker | 2 | 0.008458 | 5.7418 | 0.0000 | 560.2325 | 651.8773 | 743.5221 | 835.1670 | 926.8118 | 1018.4567 | 1110.1015 | 1201.7464 | 1293.3912 |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | charter | 2 | 0.025375 | 5.7418 | 0.0000 | 186.7442 | 217.2924 | 247.8407 | 278.3890 | 308.9373 | 339.4856 | 370.0338 | 400.5821 | 431.1304 |
| ASSET:PUMPUSDT | 1d | holdout | frozen3.0 | maker | 2 | 0.003383 | 5.7418 | 0.0000 | 1400.5812 | 1629.6933 | 1858.8054 | 2087.9175 | 2317.0296 | 2546.1417 | 2775.2538 | 3004.3659 | 3233.4780 |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | taker | 4 | 0.015900 | 5.3056 | 0.0000 | 277.7688 | 290.4524 | 303.1360 | 361.3542 | 442.3397 | 523.3252 | 580.6440 | 590.6295 | 600.6150 |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | charter | 4 | 0.047700 | 5.3056 | 0.0000 | 92.5896 | 96.8175 | 101.0453 | 120.4514 | 147.4466 | 174.4417 | 193.5480 | 196.8765 | 200.2050 |
| ASSET:HYPEUSDT | 1d | ALL | calibrated | maker | 4 | 0.006360 | 5.3056 | 0.0000 | 694.4219 | 726.1309 | 757.8399 | 903.3854 | 1105.8492 | 1308.3129 | 1451.6100 | 1476.5737 | 1501.5374 |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | taker | 2 | 0.019371 | 8.7355 | 0.0000 | 337.6875 | 368.0112 | 398.3348 | 428.6585 | 458.9821 | 489.3058 | 519.6295 | 549.9531 | 580.2768 |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | charter | 2 | 0.058112 | 8.7355 | 0.0000 | 112.5625 | 122.6704 | 132.7783 | 142.8862 | 152.9940 | 163.1019 | 173.2098 | 183.3177 | 193.4256 |
| ASSET:HYPEUSDT | 1d | ALL | frozen3.0 | maker | 2 | 0.007748 | 8.7355 | 0.0000 | 844.2187 | 920.0279 | 995.8370 | 1071.6462 | 1147.4553 | 1223.2645 | 1299.0736 | 1374.8828 | 1450.6919 |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | tuning | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | taker | 4 | 0.015900 | 5.3056 | 0.0000 | 277.7688 | 290.4524 | 303.1360 | 361.3542 | 442.3397 | 523.3252 | 580.6440 | 590.6295 | 600.6150 |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | charter | 4 | 0.047700 | 5.3056 | 0.0000 | 92.5896 | 96.8175 | 101.0453 | 120.4514 | 147.4466 | 174.4417 | 193.5480 | 196.8765 | 200.2050 |
| ASSET:HYPEUSDT | 1d | holdout | calibrated | maker | 4 | 0.006360 | 5.3056 | 0.0000 | 694.4219 | 726.1309 | 757.8399 | 903.3854 | 1105.8492 | 1308.3129 | 1451.6100 | 1476.5737 | 1501.5374 |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | taker | 2 | 0.019371 | 8.7355 | 0.0000 | 337.6875 | 368.0112 | 398.3348 | 428.6585 | 458.9821 | 489.3058 | 519.6295 | 549.9531 | 580.2768 |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | charter | 2 | 0.058112 | 8.7355 | 0.0000 | 112.5625 | 122.6704 | 132.7783 | 142.8862 | 152.9940 | 163.1019 | 173.2098 | 183.3177 | 193.4256 |
| ASSET:HYPEUSDT | 1d | holdout | frozen3.0 | maker | 2 | 0.007748 | 8.7355 | 0.0000 | 844.2187 | 920.0279 | 995.8370 | 1071.6462 | 1147.4553 | 1223.2645 | 1299.0736 | 1374.8828 | 1450.6919 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | taker | 8 | 0.015616 | 6.4806 | 0.0000 | 188.9835 | 287.0234 | 377.0270 | 380.5969 | 388.7145 | 401.9179 | 423.2876 | 462.3088 | 596.7324 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | charter | 8 | 0.046849 | 6.4806 | 0.0000 | 62.9945 | 95.6745 | 125.6757 | 126.8656 | 129.5715 | 133.9726 | 141.0959 | 154.1029 | 198.9108 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | calibrated | maker | 8 | 0.006247 | 6.4806 | 0.0000 | 472.4588 | 717.5586 | 942.5675 | 951.4922 | 971.7864 | 1004.7946 | 1058.2189 | 1155.7720 | 1491.8310 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | taker | 5 | 0.019036 | 6.8755 | 0.0000 | 259.2413 | 291.1216 | 324.4760 | 359.3047 | 394.1334 | 407.0162 | 419.8990 | 608.0210 | 971.3824 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | charter | 5 | 0.057108 | 6.8755 | 0.0000 | 86.4138 | 97.0405 | 108.1587 | 119.7682 | 131.3778 | 135.6721 | 139.9663 | 202.6737 | 323.7941 |
| ASSET:MNTUSDT_BYBIT | 1d | ALL | frozen3.0 | maker | 5 | 0.007614 | 6.8755 | 0.0000 | 648.1033 | 727.8039 | 811.1901 | 898.2619 | 985.3336 | 1017.5405 | 1049.7474 | 1520.0526 | 2428.4560 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | taker | 3 | 0.015857 | 6.0857 | 0.0000 | 125.0210 | 150.6060 | 176.1910 | 201.7760 | 227.3611 | 261.0513 | 294.7415 | 328.4318 | 362.1220 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | charter | 3 | 0.047572 | 6.0857 | 0.0000 | 41.6737 | 50.2020 | 58.7303 | 67.2587 | 75.7870 | 87.0171 | 98.2472 | 109.4773 | 120.7073 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | calibrated | maker | 3 | 0.006343 | 6.0857 | 0.0000 | 312.5525 | 376.5150 | 440.4776 | 504.4401 | 568.4027 | 652.6282 | 736.8538 | 821.0794 | 905.3050 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | taker | 2 | 0.024638 | 6.3604 | 0.0000 | 235.3311 | 243.3012 | 251.2713 | 259.2413 | 267.2114 | 275.1814 | 283.1515 | 291.1216 | 299.0916 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | charter | 2 | 0.073915 | 6.3604 | 0.0000 | 78.4437 | 81.1004 | 83.7571 | 86.4138 | 89.0705 | 91.7271 | 94.3838 | 97.0405 | 99.6972 |
| ASSET:MNTUSDT_BYBIT | 1d | tuning | frozen3.0 | maker | 2 | 0.009855 | 6.3604 | 0.0000 | 588.3278 | 608.2530 | 628.1781 | 648.1033 | 668.0285 | 687.9536 | 707.8788 | 727.8039 | 747.7291 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | taker | 5 | 0.014082 | 7.9761 | 0.0000 | 378.5570 | 380.5969 | 390.5616 | 408.4510 | 426.3404 | 450.3193 | 474.2983 | 559.9175 | 707.1771 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | charter | 5 | 0.042248 | 7.9761 | 0.0000 | 126.1857 | 126.8656 | 130.1872 | 136.1503 | 142.1135 | 150.1064 | 158.0994 | 186.6392 | 235.7257 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | calibrated | maker | 5 | 0.005633 | 7.9761 | 0.0000 | 946.3924 | 951.4922 | 976.4039 | 1021.1274 | 1065.8509 | 1125.7983 | 1185.7456 | 1399.7938 | 1767.9428 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | taker | 3 | 0.013752 | 8.5037 | 0.0000 | 400.5748 | 407.0162 | 413.4576 | 419.8990 | 426.3404 | 608.0210 | 789.7017 | 971.3824 | 1153.0631 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | charter | 3 | 0.041255 | 8.5037 | 0.0000 | 133.5249 | 135.6721 | 137.8192 | 139.9663 | 142.1135 | 202.6737 | 263.2339 | 323.7941 | 384.3544 |
| ASSET:MNTUSDT_BYBIT | 1d | holdout | frozen3.0 | maker | 3 | 0.005501 | 8.5037 | 0.0000 | 1001.4371 | 1017.5405 | 1033.6440 | 1049.7474 | 1065.8509 | 1520.0526 | 1974.2543 | 2428.4560 | 2882.6577 |
| ASSET:SUIUSDT | 1d | ALL | calibrated | taker | 12 | 0.012648 | 4.0421 | 0.0000 | 253.8446 | 265.0073 | 280.0460 | 292.6334 | 325.0741 | 364.7262 | 393.7654 | 399.9677 | 528.3267 |
| ASSET:SUIUSDT | 1d | ALL | calibrated | charter | 12 | 0.025297 | 4.0421 | 0.0000 | 126.9223 | 132.5036 | 140.0230 | 146.3167 | 162.5371 | 182.3631 | 196.8827 | 199.9838 | 264.1633 |
| ASSET:SUIUSDT | 1d | ALL | calibrated | maker | 12 | 0.005059 | 4.0421 | 0.0000 | 634.6116 | 662.5182 | 700.1150 | 731.5835 | 812.6853 | 911.8154 | 984.4135 | 999.9192 | 1320.8167 |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | taker | 3 | 0.010199 | 8.0941 | 0.0000 | 462.1093 | 544.9808 | 627.8524 | 710.7239 | 793.5954 | 997.7600 | 1201.9246 | 1406.0891 | 1610.2537 |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | charter | 3 | 0.020399 | 8.0941 | 0.0000 | 231.0547 | 272.4904 | 313.9262 | 355.3619 | 396.7977 | 498.8800 | 600.9623 | 703.0446 | 805.1269 |
| ASSET:SUIUSDT | 1d | ALL | frozen3.0 | maker | 3 | 0.004080 | 8.0941 | 0.0000 | 1155.2733 | 1362.4521 | 1569.6309 | 1776.8097 | 1983.9885 | 2494.4000 | 3004.8114 | 3515.2229 | 4025.6343 |
| ASSET:SUIUSDT | 1d | tuning | calibrated | taker | 4 | 0.011644 | 3.4598 | 0.0000 | 266.8209 | 272.2618 | 277.7027 | 291.7106 | 310.0019 | 328.2933 | 346.4526 | 364.3478 | 382.2430 |
| ASSET:SUIUSDT | 1d | tuning | calibrated | charter | 4 | 0.023288 | 3.4598 | 0.0000 | 133.4105 | 136.1309 | 138.8514 | 145.8553 | 155.0010 | 164.1466 | 173.2263 | 182.1739 | 191.1215 |
| ASSET:SUIUSDT | 1d | tuning | calibrated | maker | 4 | 0.004658 | 3.4598 | 0.0000 | 667.0523 | 680.6546 | 694.2568 | 729.2765 | 775.0048 | 820.7332 | 866.1314 | 910.8695 | 955.6075 |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | taker | 1 | 0.010199 | 8.0941 | 0.0000 | 793.5954 | 793.5954 | 793.5954 | 793.5954 | 793.5954 | 793.5954 | 793.5954 | 793.5954 | 793.5954 |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | charter | 1 | 0.020399 | 8.0941 | 0.0000 | 396.7977 | 396.7977 | 396.7977 | 396.7977 | 396.7977 | 396.7977 | 396.7977 | 396.7977 | 396.7977 |
| ASSET:SUIUSDT | 1d | tuning | frozen3.0 | maker | 1 | 0.004080 | 8.0941 | 0.0000 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 | 1983.9885 |
| ASSET:SUIUSDT | 1d | holdout | calibrated | taker | 8 | 0.012869 | 4.1562 | 0.0000 | 245.2842 | 264.3172 | 284.1198 | 303.9850 | 345.2730 | 384.5653 | 397.4454 | 485.2561 | 849.7024 |
| ASSET:SUIUSDT | 1d | holdout | calibrated | charter | 8 | 0.025737 | 4.1562 | 0.0000 | 122.6421 | 132.1586 | 142.0599 | 151.9925 | 172.6365 | 192.2827 | 198.7227 | 242.6280 | 424.8512 |
| ASSET:SUIUSDT | 1d | holdout | calibrated | maker | 8 | 0.005147 | 4.1562 | 0.0000 | 613.2106 | 660.7929 | 710.2994 | 759.9624 | 863.1825 | 961.4133 | 993.6136 | 1213.1402 | 2124.2560 |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | taker | 2 | 0.009052 | 8.2925 | 0.0000 | 522.7558 | 666.2739 | 809.7919 | 953.3100 | 1096.8280 | 1240.3461 | 1383.8641 | 1527.3822 | 1670.9002 |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | charter | 2 | 0.018105 | 8.2925 | 0.0000 | 261.3779 | 333.1369 | 404.8960 | 476.6550 | 548.4140 | 620.1730 | 691.9321 | 763.6911 | 835.4501 |
| ASSET:SUIUSDT | 1d | holdout | frozen3.0 | maker | 2 | 0.003621 | 8.2925 | 0.0000 | 1306.8896 | 1665.6847 | 2024.4798 | 2383.2750 | 2742.0701 | 3100.8652 | 3459.6604 | 3818.4555 | 4177.2506 |
| ASSET:LTCUSDT | 1d | ALL | calibrated | taker | 19 | 0.017886 | 4.3437 | 0.0000 | 173.6608 | 198.5164 | 222.4578 | 231.5697 | 251.5346 | 294.5550 | 303.2226 | 429.3514 | 578.6265 |
| ASSET:LTCUSDT | 1d | ALL | calibrated | charter | 19 | 0.035771 | 4.3437 | 0.0000 | 86.8304 | 99.2582 | 111.2289 | 115.7848 | 125.7673 | 147.2775 | 151.6113 | 214.6757 | 289.3132 |
| ASSET:LTCUSDT | 1d | ALL | calibrated | maker | 19 | 0.007154 | 4.3437 | 0.0000 | 434.1519 | 496.2910 | 556.1444 | 578.9242 | 628.8365 | 736.3876 | 758.0564 | 1073.3786 | 1446.5661 |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | taker | 13 | 0.018730 | 5.4519 | 0.0000 | 191.7761 | 213.4924 | 234.2992 | 255.9774 | 353.0904 | 514.5085 | 532.1784 | 582.7217 | 610.1347 |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | charter | 13 | 0.037460 | 5.4519 | 0.0000 | 95.8880 | 106.7462 | 117.1496 | 127.9887 | 176.5452 | 257.2542 | 266.0892 | 291.3608 | 305.0674 |
| ASSET:LTCUSDT | 1d | ALL | frozen3.0 | maker | 13 | 0.007492 | 5.4519 | 0.0000 | 479.4401 | 533.7310 | 585.7481 | 639.9434 | 882.7261 | 1286.2712 | 1330.4461 | 1456.8041 | 1525.3368 |
| ASSET:LTCUSDT | 1d | tuning | calibrated | taker | 12 | 0.012813 | 4.2534 | 0.0000 | 209.7081 | 221.4999 | 243.5548 | 290.3156 | 299.5105 | 303.2226 | 471.9014 | 565.6999 | 604.8312 |
| ASSET:LTCUSDT | 1d | tuning | calibrated | charter | 12 | 0.025626 | 4.2534 | 0.0000 | 104.8541 | 110.7499 | 121.7774 | 145.1578 | 149.7553 | 151.6113 | 235.9507 | 282.8500 | 302.4156 |
| ASSET:LTCUSDT | 1d | tuning | calibrated | maker | 12 | 0.005125 | 4.2534 | 0.0000 | 524.2703 | 553.7497 | 608.8870 | 725.7890 | 748.7763 | 758.0564 | 1179.7536 | 1414.2498 | 1512.0780 |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | taker | 7 | 0.015409 | 5.4408 | 0.0000 | 194.9442 | 221.3897 | 249.0418 | 359.7761 | 512.0516 | 531.1858 | 556.8686 | 595.6482 | 665.2554 |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | charter | 7 | 0.030818 | 5.4408 | 0.0000 | 97.4721 | 110.6948 | 124.5209 | 179.8881 | 256.0258 | 265.5929 | 278.4343 | 297.8241 | 332.6277 |
| ASSET:LTCUSDT | 1d | tuning | frozen3.0 | maker | 7 | 0.006164 | 5.4408 | 0.0000 | 487.3604 | 553.4742 | 622.6044 | 899.4403 | 1280.1289 | 1327.9646 | 1392.1714 | 1489.1205 | 1663.1386 |
| ASSET:LTCUSDT | 1d | holdout | calibrated | taker | 7 | 0.022901 | 4.9999 | 0.0000 | 141.7001 | 180.9913 | 182.8987 | 201.2205 | 227.7495 | 239.2100 | 247.7872 | 250.5978 | 292.1038 |
| ASSET:LTCUSDT | 1d | holdout | calibrated | charter | 7 | 0.045801 | 4.9999 | 0.0000 | 70.8500 | 90.4956 | 91.4494 | 100.6103 | 113.8748 | 119.6050 | 123.8936 | 125.2989 | 146.0519 |
| ASSET:LTCUSDT | 1d | holdout | calibrated | maker | 7 | 0.009160 | 4.9999 | 0.0000 | 354.2502 | 452.4782 | 457.2468 | 503.0513 | 569.3738 | 598.0251 | 619.4681 | 626.4944 | 730.2596 |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | taker | 6 | 0.021613 | 5.5525 | 0.0000 | 201.0747 | 215.4725 | 231.1614 | 246.8504 | 299.9704 | 353.0904 | 438.7133 | 524.3361 | 567.4304 |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | charter | 6 | 0.043226 | 5.5525 | 0.0000 | 100.5374 | 107.7362 | 115.5807 | 123.4252 | 149.9852 | 176.5452 | 219.3566 | 262.1680 | 283.7152 |
| ASSET:LTCUSDT | 1d | holdout | frozen3.0 | maker | 6 | 0.008645 | 5.5525 | 0.0000 | 502.6868 | 538.6812 | 577.9036 | 617.1260 | 749.9261 | 882.7261 | 1096.7831 | 1310.8401 | 1418.5760 |
| ASSET:XMRUSDT | 1d | ALL | calibrated | taker | 15 | 0.013587 | 2.7778 | 0.0000 | 138.0060 | 145.4955 | 148.5342 | 163.6478 | 208.1526 | 231.7462 | 248.7149 | 333.4681 | 551.1970 |
| ASSET:XMRUSDT | 1d | ALL | calibrated | charter | 15 | 0.027175 | 2.7778 | 0.0000 | 69.0030 | 72.7477 | 74.2671 | 81.8239 | 104.0763 | 115.8731 | 124.3575 | 166.7340 | 275.5985 |
| ASSET:XMRUSDT | 1d | ALL | calibrated | maker | 15 | 0.005435 | 2.7778 | 0.0000 | 345.0150 | 363.7387 | 371.3356 | 409.1195 | 520.3816 | 579.3656 | 621.7873 | 833.6702 | 1377.9926 |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | taker | 3 | 0.012566 | 6.0771 | 0.0000 | 419.3772 | 442.6439 | 465.9106 | 489.1772 | 512.4439 | 527.8950 | 543.3462 | 558.7974 | 574.2485 |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | charter | 3 | 0.025132 | 6.0771 | 0.0000 | 209.6886 | 221.3219 | 232.9553 | 244.5886 | 256.2219 | 263.9475 | 271.6731 | 279.3987 | 287.1243 |
| ASSET:XMRUSDT | 1d | ALL | frozen3.0 | maker | 3 | 0.005026 | 6.0771 | 0.0000 | 1048.4431 | 1106.6097 | 1164.7764 | 1222.9431 | 1281.1097 | 1319.7376 | 1358.3655 | 1396.9934 | 1435.6213 |
| ASSET:XMRUSDT | 1d | tuning | calibrated | taker | 10 | 0.013079 | 2.8509 | 0.0000 | 142.9867 | 145.4955 | 153.1626 | 195.1008 | 234.4385 | 248.3074 | 268.3681 | 333.4681 | 452.0728 |
| ASSET:XMRUSDT | 1d | tuning | calibrated | charter | 10 | 0.026158 | 2.8509 | 0.0000 | 71.4934 | 72.7477 | 76.5813 | 97.5504 | 117.2193 | 124.1537 | 134.1841 | 166.7340 | 226.0364 |
| ASSET:XMRUSDT | 1d | tuning | calibrated | maker | 10 | 0.005232 | 2.8509 | 0.0000 | 357.4669 | 363.7387 | 382.9065 | 487.7520 | 586.0963 | 620.7686 | 670.9204 | 833.6702 | 1130.1820 |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | taker | 2 | 0.013147 | 7.1354 | 0.0000 | 520.1695 | 527.8950 | 535.6206 | 543.3462 | 551.0718 | 558.7974 | 566.5230 | 574.2485 | 581.9741 |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | charter | 2 | 0.026295 | 7.1354 | 0.0000 | 260.0847 | 263.9475 | 267.8103 | 271.6731 | 275.5359 | 279.3987 | 283.2615 | 287.1243 | 290.9871 |
| ASSET:XMRUSDT | 1d | tuning | frozen3.0 | maker | 2 | 0.005259 | 7.1354 | 0.0000 | 1300.4237 | 1319.7376 | 1339.0516 | 1358.3655 | 1377.6795 | 1396.9934 | 1416.3074 | 1435.6213 | 1454.9353 |
| ASSET:XMRUSDT | 1d | holdout | calibrated | taker | 5 | 0.014910 | 2.5663 | 0.0000 | 117.0861 | 136.7595 | 150.9880 | 159.7717 | 168.5554 | 184.3943 | 200.2332 | 295.2759 | 469.5225 |
| ASSET:XMRUSDT | 1d | holdout | calibrated | charter | 5 | 0.029820 | 2.5663 | 0.0000 | 58.5431 | 68.3798 | 75.4940 | 79.8859 | 84.2777 | 92.1971 | 100.1166 | 147.6380 | 234.7612 |
| ASSET:XMRUSDT | 1d | holdout | calibrated | maker | 5 | 0.005964 | 2.5663 | 0.0000 | 292.7154 | 341.8988 | 377.4701 | 399.4293 | 421.3885 | 460.9857 | 500.5829 | 738.1898 | 1173.8061 |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | taker | 1 | 0.012566 | 4.9775 | 0.0000 | 396.1106 | 396.1106 | 396.1106 | 396.1106 | 396.1106 | 396.1106 | 396.1106 | 396.1106 | 396.1106 |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | charter | 1 | 0.025132 | 4.9775 | 0.0000 | 198.0553 | 198.0553 | 198.0553 | 198.0553 | 198.0553 | 198.0553 | 198.0553 | 198.0553 | 198.0553 |
| ASSET:XMRUSDT | 1d | holdout | frozen3.0 | maker | 1 | 0.005026 | 4.9775 | 0.0000 | 990.2764 | 990.2764 | 990.2764 | 990.2764 | 990.2764 | 990.2764 | 990.2764 | 990.2764 | 990.2764 |
| ASSET:BNBUSDT | 1d | ALL | calibrated | taker | 23 | 0.017596 | 3.6645 | 0.0000 | 117.4414 | 145.2180 | 181.0449 | 201.3021 | 213.2820 | 250.3315 | 297.0239 | 342.7404 | 383.4025 |
| ASSET:BNBUSDT | 1d | ALL | calibrated | charter | 23 | 0.035193 | 3.6645 | 0.0000 | 58.7207 | 72.6090 | 90.5225 | 100.6511 | 106.6410 | 125.1657 | 148.5120 | 171.3702 | 191.7012 |
| ASSET:BNBUSDT | 1d | ALL | calibrated | maker | 23 | 0.007038 | 3.6645 | 0.0000 | 293.6034 | 363.0449 | 452.6123 | 503.2553 | 533.2051 | 625.8287 | 742.5598 | 856.8510 | 958.5062 |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | taker | 8 | 0.019812 | 5.1440 | 0.0000 | 171.3490 | 181.1037 | 189.9316 | 216.0738 | 230.3971 | 255.3391 | 318.6467 | 502.1817 | 641.6573 |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | charter | 8 | 0.039624 | 5.1440 | 0.0000 | 85.6745 | 90.5519 | 94.9658 | 108.0369 | 115.1986 | 127.6695 | 159.3233 | 251.0909 | 320.8287 |
| ASSET:BNBUSDT | 1d | ALL | frozen3.0 | maker | 8 | 0.007925 | 5.1440 | 0.0000 | 428.3726 | 452.7593 | 474.8291 | 540.1846 | 575.9928 | 638.3477 | 796.6166 | 1255.4543 | 1604.1433 |
| ASSET:BNBUSDT | 1d | tuning | calibrated | taker | 14 | 0.015503 | 3.3765 | 0.0000 | 179.0529 | 196.0181 | 205.2618 | 222.9724 | 269.9284 | 319.0119 | 352.1211 | 369.4560 | 408.3101 |
| ASSET:BNBUSDT | 1d | tuning | calibrated | charter | 14 | 0.031006 | 3.3765 | 0.0000 | 89.5265 | 98.0091 | 102.6309 | 111.4862 | 134.9642 | 159.5059 | 176.0605 | 184.7280 | 204.1550 |
| ASSET:BNBUSDT | 1d | tuning | calibrated | maker | 14 | 0.006201 | 3.3765 | 0.0000 | 447.6323 | 490.0453 | 513.1546 | 557.4310 | 674.8211 | 797.5297 | 880.3027 | 923.6401 | 1020.7751 |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | taker | 4 | 0.021324 | 9.7907 | 0.0000 | 222.7029 | 267.6976 | 312.6924 | 385.8543 | 473.0999 | 560.3455 | 626.2252 | 649.3734 | 672.5216 |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | charter | 4 | 0.042648 | 9.7907 | 0.0000 | 111.3514 | 133.8488 | 156.3462 | 192.9272 | 236.5499 | 280.1727 | 313.1126 | 324.6867 | 336.2608 |
| ASSET:BNBUSDT | 1d | tuning | frozen3.0 | maker | 4 | 0.008530 | 9.7907 | 0.0000 | 556.7572 | 669.2441 | 781.7309 | 964.6358 | 1182.7497 | 1400.8636 | 1565.5631 | 1623.4335 | 1681.3039 |
| ASSET:BNBUSDT | 1d | holdout | calibrated | taker | 9 | 0.024258 | 4.0427 | 0.0000 | 103.7973 | 111.1953 | 118.9341 | 125.4888 | 133.7953 | 178.4328 | 218.1876 | 241.3431 | 263.0598 |
| ASSET:BNBUSDT | 1d | holdout | calibrated | charter | 9 | 0.048516 | 4.0427 | 0.0000 | 51.8986 | 55.5976 | 59.4670 | 62.7444 | 66.8976 | 89.2164 | 109.0938 | 120.6715 | 131.5299 |
| ASSET:BNBUSDT | 1d | holdout | calibrated | maker | 9 | 0.009703 | 4.0427 | 0.0000 | 259.4932 | 277.9882 | 297.3352 | 313.7221 | 334.4882 | 446.0819 | 545.4690 | 603.3577 | 657.6494 |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | taker | 4 | 0.018434 | 3.8124 | 0.0000 | 165.4169 | 174.3227 | 183.2284 | 193.6662 | 204.8700 | 216.0738 | 224.9138 | 229.0263 | 233.1387 |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | charter | 4 | 0.036868 | 3.8124 | 0.0000 | 82.7084 | 87.1613 | 91.6142 | 96.8331 | 102.4350 | 108.0369 | 112.4569 | 114.5131 | 116.5694 |
| ASSET:BNBUSDT | 1d | holdout | frozen3.0 | maker | 4 | 0.007374 | 3.8124 | 0.0000 | 413.5422 | 435.8067 | 458.0711 | 484.1656 | 512.1751 | 540.1846 | 562.2846 | 572.5657 | 582.8469 |
| ASSET:UNIUSDT | 1d | ALL | calibrated | taker | 13 | 0.013027 | 4.6951 | 0.0000 | 269.2993 | 285.0571 | 303.7974 | 317.4390 | 319.7953 | 338.4469 | 370.0724 | 396.9016 | 715.4562 |
| ASSET:UNIUSDT | 1d | ALL | calibrated | charter | 13 | 0.026055 | 4.6951 | 0.0000 | 134.6497 | 142.5286 | 151.8987 | 158.7195 | 159.8977 | 169.2234 | 185.0362 | 198.4508 | 357.7281 |
| ASSET:UNIUSDT | 1d | ALL | calibrated | maker | 13 | 0.005211 | 4.6951 | 0.0000 | 673.2484 | 712.6428 | 759.4935 | 793.5976 | 799.4883 | 846.1171 | 925.1811 | 992.2541 | 1788.6405 |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | taker | 9 | 0.015963 | 6.5534 | 0.0000 | 281.2282 | 305.1692 | 343.1485 | 385.1515 | 405.3983 | 578.6129 | 724.5490 | 817.8111 | 961.3702 |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | charter | 9 | 0.031926 | 6.5534 | 0.0000 | 140.6141 | 152.5846 | 171.5742 | 192.5758 | 202.6991 | 289.3064 | 362.2745 | 408.9055 | 480.6851 |
| ASSET:UNIUSDT | 1d | ALL | frozen3.0 | maker | 9 | 0.006385 | 6.5534 | 0.0000 | 703.0705 | 762.9229 | 857.8712 | 962.8789 | 1013.4956 | 1446.5321 | 1811.3725 | 2044.5276 | 2403.4254 |
| ASSET:UNIUSDT | 1d | tuning | calibrated | taker | 9 | 0.011621 | 4.6988 | 0.0000 | 280.4734 | 304.4437 | 318.6826 | 322.4138 | 332.8878 | 355.1239 | 374.7672 | 547.6823 | 911.6894 |
| ASSET:UNIUSDT | 1d | tuning | calibrated | charter | 9 | 0.023243 | 4.6988 | 0.0000 | 140.2367 | 152.2219 | 159.3413 | 161.2069 | 166.4439 | 177.5619 | 187.3836 | 273.8412 | 455.8447 |
| ASSET:UNIUSDT | 1d | tuning | calibrated | maker | 9 | 0.004649 | 4.6988 | 0.0000 | 701.1836 | 761.1093 | 796.7065 | 806.0346 | 832.2196 | 887.8097 | 936.9180 | 1369.2058 | 2279.2235 |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | taker | 7 | 0.013792 | 6.5534 | 0.0000 | 297.3424 | 330.8347 | 367.7761 | 476.8205 | 621.9165 | 724.5490 | 805.3909 | 842.6514 | 1067.6687 |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | charter | 7 | 0.027584 | 6.5534 | 0.0000 | 148.6712 | 165.4173 | 183.8880 | 238.4103 | 310.9583 | 362.2745 | 402.6954 | 421.3257 | 533.8344 |
| ASSET:UNIUSDT | 1d | tuning | frozen3.0 | maker | 7 | 0.005517 | 6.5534 | 0.0000 | 743.3560 | 827.0867 | 919.4402 | 1192.0513 | 1554.7913 | 1811.3725 | 2013.4772 | 2106.6286 | 2669.1718 |
| ASSET:UNIUSDT | 1d | holdout | calibrated | taker | 4 | 0.014968 | 4.5026 | 0.0000 | 127.5604 | 195.6112 | 263.6621 | 292.1629 | 300.8888 | 309.6147 | 324.4285 | 351.4184 | 378.4083 |
| ASSET:UNIUSDT | 1d | holdout | calibrated | charter | 4 | 0.029937 | 4.5026 | 0.0000 | 63.7802 | 97.8056 | 131.8310 | 146.0815 | 150.4444 | 154.8073 | 162.2143 | 175.7092 | 189.2042 |
| ASSET:UNIUSDT | 1d | holdout | calibrated | maker | 4 | 0.005987 | 4.5026 | 0.0000 | 318.9010 | 489.0281 | 659.1551 | 730.4073 | 752.2220 | 774.0366 | 811.0713 | 878.5461 | 946.0209 |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | taker | 2 | 0.019623 | 6.6961 | 0.0000 | 297.1672 | 309.1929 | 321.2186 | 333.2442 | 345.2699 | 357.2956 | 369.3212 | 381.3469 | 393.3726 |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | charter | 2 | 0.039245 | 6.6961 | 0.0000 | 148.5836 | 154.5965 | 160.6093 | 166.6221 | 172.6350 | 178.6478 | 184.6606 | 190.6735 | 196.6863 |
| ASSET:UNIUSDT | 1d | holdout | frozen3.0 | maker | 2 | 0.007849 | 6.6961 | 0.0000 | 742.9181 | 772.9823 | 803.0464 | 833.1106 | 863.1748 | 893.2389 | 923.3031 | 953.3673 | 983.4315 |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | taker | 7 | 0.009832 | 7.7673 | 0.0000 | 500.4666 | 504.6762 | 510.3594 | 575.3520 | 669.9994 | 703.4236 | 875.6114 | 1325.3265 | 1560.7835 |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | charter | 7 | 0.029495 | 7.7673 | 0.0000 | 166.8222 | 168.2254 | 170.1198 | 191.7840 | 223.3331 | 234.4745 | 291.8705 | 441.7755 | 520.2612 |
| ASSET:1000PEPEUSDT | 1d | ALL | calibrated | maker | 7 | 0.003933 | 7.7673 | 0.0000 | 1251.1664 | 1261.6904 | 1275.8985 | 1438.3801 | 1674.9985 | 1758.5589 | 2189.0284 | 3313.3161 | 3901.9588 |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | taker | 7 | 0.009832 | 7.7673 | 0.0000 | 500.4666 | 504.6762 | 510.3594 | 575.3520 | 669.9994 | 703.4236 | 875.6114 | 1325.3265 | 1560.7835 |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | charter | 7 | 0.029495 | 7.7673 | 0.0000 | 166.8222 | 168.2254 | 170.1198 | 191.7840 | 223.3331 | 234.4745 | 291.8705 | 441.7755 | 520.2612 |
| ASSET:1000PEPEUSDT | 1d | ALL | frozen3.0 | maker | 7 | 0.003933 | 7.7673 | 0.0000 | 1251.1664 | 1261.6904 | 1275.8985 | 1438.3801 | 1674.9985 | 1758.5589 | 2189.0284 | 3313.3161 | 3901.9588 |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | taker | 3 | 0.009832 | 5.9307 | 0.0000 | 531.5949 | 566.1960 | 600.7971 | 635.3983 | 669.9994 | 681.1408 | 692.2822 | 703.4236 | 714.5650 |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | charter | 3 | 0.029495 | 5.9307 | 0.0000 | 177.1983 | 188.7320 | 200.2657 | 211.7994 | 223.3331 | 227.0469 | 230.7607 | 234.4745 | 238.1883 |
| ASSET:1000PEPEUSDT | 1d | tuning | calibrated | maker | 3 | 0.003933 | 5.9307 | 0.0000 | 1328.9873 | 1415.4901 | 1501.9929 | 1588.4957 | 1674.9985 | 1702.8519 | 1730.7054 | 1758.5589 | 1786.4124 |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | taker | 3 | 0.009832 | 5.9307 | 0.0000 | 531.5949 | 566.1960 | 600.7971 | 635.3983 | 669.9994 | 681.1408 | 692.2822 | 703.4236 | 714.5650 |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | charter | 3 | 0.029495 | 5.9307 | 0.0000 | 177.1983 | 188.7320 | 200.2657 | 211.7994 | 223.3331 | 227.0469 | 230.7607 | 234.4745 | 238.1883 |
| ASSET:1000PEPEUSDT | 1d | tuning | frozen3.0 | maker | 3 | 0.003933 | 5.9307 | 0.0000 | 1328.9873 | 1415.4901 | 1501.9929 | 1588.4957 | 1674.9985 | 1702.8519 | 1730.7054 | 1758.5589 | 1786.4124 |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | taker | 4 | 0.010662 | 8.5578 | 0.0000 | 505.6234 | 508.4650 | 511.3066 | 704.8494 | 993.7426 | 1282.6359 | 1496.6195 | 1560.7835 | 1624.9475 |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | charter | 4 | 0.031987 | 8.5578 | 0.0000 | 168.5411 | 169.4883 | 170.4355 | 234.9498 | 331.2475 | 427.5453 | 498.8732 | 520.2612 | 541.6492 |
| ASSET:1000PEPEUSDT | 1d | holdout | calibrated | maker | 4 | 0.004265 | 8.5578 | 0.0000 | 1264.0585 | 1271.1625 | 1278.2665 | 1762.1234 | 2484.3566 | 3206.5899 | 3741.5487 | 3901.9588 | 4062.3688 |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | taker | 4 | 0.010662 | 8.5578 | 0.0000 | 505.6234 | 508.4650 | 511.3066 | 704.8494 | 993.7426 | 1282.6359 | 1496.6195 | 1560.7835 | 1624.9475 |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | charter | 4 | 0.031987 | 8.5578 | 0.0000 | 168.5411 | 169.4883 | 170.4355 | 234.9498 | 331.2475 | 427.5453 | 498.8732 | 520.2612 | 541.6492 |
| ASSET:1000PEPEUSDT | 1d | holdout | frozen3.0 | maker | 4 | 0.004265 | 8.5578 | 0.0000 | 1264.0585 | 1271.1625 | 1278.2665 | 1762.1234 | 2484.3566 | 3206.5899 | 3741.5487 | 3901.9588 | 4062.3688 |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | taker | 17 | 0.012875 | 4.1165 | 0.0000 | 197.3489 | 247.9371 | 258.9929 | 268.1015 | 302.4538 | 323.2841 | 392.3870 | 420.2265 | 533.9779 |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | charter | 17 | 0.025750 | 4.1165 | 0.0000 | 98.6744 | 123.9686 | 129.4965 | 134.0508 | 151.2269 | 161.6421 | 196.1935 | 210.1133 | 266.9890 |
| ASSET:DOGEUSDT | 1d | ALL | calibrated | maker | 17 | 0.005150 | 4.1165 | 0.0000 | 493.3721 | 619.8429 | 647.4823 | 670.2538 | 756.1345 | 808.2103 | 980.9675 | 1050.5663 | 1334.9448 |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | taker | 10 | 0.016648 | 6.3943 | 0.0000 | 259.5196 | 285.9942 | 334.5685 | 372.3160 | 386.7580 | 495.8721 | 712.4568 | 966.0394 | 1463.0590 |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | charter | 10 | 0.033296 | 6.3943 | 0.0000 | 129.7598 | 142.9971 | 167.2842 | 186.1580 | 193.3790 | 247.9360 | 356.2284 | 483.0197 | 731.5295 |
| ASSET:DOGEUSDT | 1d | ALL | frozen3.0 | maker | 10 | 0.006659 | 6.3943 | 0.0000 | 648.7990 | 714.9855 | 836.4211 | 930.7901 | 966.8950 | 1239.6802 | 1781.1420 | 2415.0986 | 3657.6474 |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | taker | 11 | 0.012518 | 4.2416 | 0.0000 | 186.2468 | 204.7502 | 260.9455 | 272.5080 | 318.5276 | 390.3503 | 400.5339 | 425.1497 | 451.9667 |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | charter | 11 | 0.025036 | 4.2416 | 0.0000 | 93.1234 | 102.3751 | 130.4728 | 136.2540 | 159.2638 | 195.1751 | 200.2669 | 212.5749 | 225.9833 |
| ASSET:DOGEUSDT | 1d | tuning | calibrated | maker | 11 | 0.005007 | 4.2416 | 0.0000 | 465.6171 | 511.8755 | 652.3638 | 681.2701 | 796.3191 | 975.8757 | 1001.3347 | 1062.8743 | 1129.9167 |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | taker | 7 | 0.017138 | 6.2220 | 0.0000 | 241.2631 | 283.1244 | 335.6822 | 365.9445 | 385.0591 | 387.0978 | 479.1392 | 751.1858 | 1090.2108 |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | charter | 7 | 0.034275 | 6.2220 | 0.0000 | 120.6316 | 141.5622 | 167.8411 | 182.9723 | 192.5295 | 193.5489 | 239.5696 | 375.5929 | 545.1054 |
| ASSET:DOGEUSDT | 1d | tuning | frozen3.0 | maker | 7 | 0.006855 | 6.2220 | 0.0000 | 603.1578 | 707.8109 | 839.2055 | 914.8613 | 962.6477 | 967.7445 | 1197.8479 | 1877.9646 | 2725.5270 |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | taker | 6 | 0.013042 | 3.9822 | 0.0000 | 249.1541 | 251.1825 | 258.1732 | 265.1638 | 283.8088 | 302.4538 | 314.4544 | 326.4551 | 491.7249 |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | charter | 6 | 0.026084 | 3.9822 | 0.0000 | 124.5771 | 125.5912 | 129.0866 | 132.5819 | 141.9044 | 151.2269 | 157.2272 | 163.2275 | 245.8625 |
| ASSET:DOGEUSDT | 1d | holdout | calibrated | maker | 6 | 0.005217 | 3.9822 | 0.0000 | 622.8854 | 627.9562 | 645.4329 | 662.9096 | 709.5220 | 756.1345 | 786.1361 | 816.1377 | 1229.3124 |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | taker | 3 | 0.012875 | 8.4588 | 0.0000 | 364.2721 | 437.4528 | 510.6335 | 583.8141 | 656.9948 | 818.8090 | 980.6232 | 1142.4374 | 1304.2516 |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | charter | 3 | 0.025750 | 8.4588 | 0.0000 | 182.1361 | 218.7264 | 255.3167 | 291.9071 | 328.4974 | 409.4045 | 490.3116 | 571.2187 | 652.1258 |
| ASSET:DOGEUSDT | 1d | holdout | frozen3.0 | maker | 3 | 0.005150 | 8.4588 | 0.0000 | 910.6803 | 1093.6320 | 1276.5837 | 1459.5354 | 1642.4870 | 2047.0225 | 2451.5580 | 2856.0934 | 3260.6289 |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | taker | 7 | 0.011044 | 6.3664 | 0.0000 | 189.9204 | 242.0337 | 314.8973 | 434.0888 | 576.4442 | 612.2109 | 864.7536 | 1550.8482 | 1782.2816 |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | charter | 7 | 0.033133 | 6.3664 | 0.0000 | 63.3068 | 80.6779 | 104.9658 | 144.6963 | 192.1481 | 204.0703 | 288.2512 | 516.9494 | 594.0939 |
| ASSET:1000BONKUSDT | 1d | ALL | calibrated | maker | 7 | 0.004418 | 6.3664 | 0.0000 | 474.8011 | 605.0842 | 787.2432 | 1085.2220 | 1441.1106 | 1530.5272 | 2161.8839 | 3877.1205 | 4455.7040 |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | taker | 5 | 0.010789 | 6.8625 | 0.0000 | 415.6058 | 522.8314 | 588.3664 | 612.2109 | 636.0553 | 1096.1870 | 1556.3186 | 1792.9647 | 1806.1254 |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | charter | 5 | 0.032367 | 6.8625 | 0.0000 | 138.5353 | 174.2771 | 196.1221 | 204.0703 | 212.0184 | 365.3957 | 518.7729 | 597.6549 | 602.0418 |
| ASSET:1000BONKUSDT | 1d | ALL | frozen3.0 | maker | 5 | 0.004316 | 6.8625 | 0.0000 | 1039.0146 | 1307.0786 | 1470.9161 | 1530.5272 | 1590.1384 | 2740.4674 | 3890.7964 | 4482.4118 | 4515.3136 |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | taker | 2 | 0.007596 | 7.3640 | 0.0000 | 751.0882 | 866.1211 | 981.1541 | 1096.1870 | 1211.2199 | 1326.2528 | 1441.2857 | 1556.3186 | 1671.3515 |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | charter | 2 | 0.022788 | 7.3640 | 0.0000 | 250.3627 | 288.7070 | 327.0514 | 365.3957 | 403.7400 | 442.0843 | 480.4286 | 518.7729 | 557.1172 |
| ASSET:1000BONKUSDT | 1d | tuning | calibrated | maker | 2 | 0.003038 | 7.3640 | 0.0000 | 1877.7206 | 2165.3029 | 2452.8851 | 2740.4674 | 3028.0496 | 3315.6319 | 3603.2141 | 3890.7964 | 4178.3787 |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | taker | 2 | 0.007596 | 7.3640 | 0.0000 | 751.0882 | 866.1211 | 981.1541 | 1096.1870 | 1211.2199 | 1326.2528 | 1441.2857 | 1556.3186 | 1671.3515 |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | charter | 2 | 0.022788 | 7.3640 | 0.0000 | 250.3627 | 288.7070 | 327.0514 | 365.3957 | 403.7400 | 442.0843 | 480.4286 | 518.7729 | 557.1172 |
| ASSET:1000BONKUSDT | 1d | tuning | frozen3.0 | maker | 2 | 0.003038 | 7.3640 | 0.0000 | 1877.7206 | 2165.3029 | 2452.8851 | 2740.4674 | 3028.0496 | 3315.6319 | 3603.2141 | 3890.7964 | 4178.3787 |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | taker | 5 | 0.012073 | 4.5450 | 0.0000 | 176.0077 | 203.8331 | 242.0337 | 290.6094 | 339.1852 | 434.0888 | 528.9924 | 817.0647 | 1298.3055 |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | charter | 5 | 0.036218 | 4.5450 | 0.0000 | 58.6692 | 67.9444 | 80.6779 | 96.8698 | 113.0617 | 144.6963 | 176.3308 | 272.3549 | 432.7685 |
| ASSET:1000BONKUSDT | 1d | holdout | calibrated | maker | 5 | 0.004829 | 4.5450 | 0.0000 | 440.0194 | 509.5828 | 605.0842 | 726.5235 | 847.9629 | 1085.2220 | 1322.4810 | 2042.6616 | 3245.7638 |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | taker | 3 | 0.011044 | 6.3664 | 0.0000 | 361.9931 | 415.6058 | 469.2186 | 522.8314 | 576.4442 | 825.0126 | 1073.5810 | 1322.1494 | 1570.7178 |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | charter | 3 | 0.033133 | 6.3664 | 0.0000 | 120.6644 | 138.5353 | 156.4062 | 174.2771 | 192.1481 | 275.0042 | 357.8603 | 440.7165 | 523.5726 |
| ASSET:1000BONKUSDT | 1d | holdout | frozen3.0 | maker | 3 | 0.004418 | 6.3664 | 0.0000 | 904.9826 | 1039.0146 | 1173.0466 | 1307.0786 | 1441.1106 | 2062.5315 | 2683.9525 | 3305.3734 | 3926.7944 |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | taker | 93 | 0.015155 | 4.9541 | 0.0000 | 128.5489 | 200.1928 | 231.8221 | 277.6606 | 319.5590 | 360.5718 | 395.0367 | 544.8321 | 655.1467 |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | charter | 93 | 0.028199 | 4.9541 | 0.0000 | 87.8666 | 116.1062 | 147.4769 | 165.7916 | 181.5056 | 193.9875 | 221.8296 | 293.1683 | 364.4765 |
| POOLED:CLASSIC5 | 1d | ALL | calibrated | maker | 93 | 0.006062 | 4.9541 | 0.0000 | 321.3722 | 500.4819 | 579.5551 | 694.1516 | 798.8974 | 901.4294 | 987.5918 | 1362.0802 | 1637.8668 |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | taker | 53 | 0.017182 | 6.2372 | 0.0000 | 213.1269 | 274.5243 | 319.2734 | 358.7832 | 413.9918 | 544.9484 | 623.6958 | 659.7667 | 895.7197 |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | charter | 53 | 0.028306 | 6.2372 | 0.0000 | 140.1288 | 165.0678 | 185.5848 | 205.4809 | 227.8103 | 302.9931 | 322.0467 | 386.3971 | 575.9828 |
| POOLED:CLASSIC5 | 1d | ALL | frozen3.0 | maker | 53 | 0.006873 | 6.2372 | 0.0000 | 532.8173 | 686.3108 | 798.1834 | 896.9579 | 1034.9794 | 1362.3710 | 1559.2396 | 1649.4168 | 2239.2992 |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | taker | 60 | 0.014746 | 4.9160 | 0.0000 | 149.1535 | 210.2259 | 271.5067 | 309.9085 | 342.8890 | 365.9262 | 407.0637 | 561.9305 | 683.2783 |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | charter | 60 | 0.025752 | 4.9160 | 0.0000 | 98.2138 | 143.4968 | 163.6714 | 175.3289 | 190.0041 | 197.9759 | 224.8872 | 297.7677 | 383.0219 |
| POOLED:CLASSIC5 | 1d | tuning | calibrated | maker | 60 | 0.005898 | 4.9160 | 0.0000 | 372.8839 | 525.5648 | 678.7667 | 774.7712 | 857.2226 | 914.8156 | 1017.6593 | 1404.8262 | 1708.1957 |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | taker | 35 | 0.017182 | 6.2372 | 0.0000 | 215.3140 | 273.2719 | 346.3288 | 358.0320 | 413.9918 | 478.1423 | 594.2813 | 649.3665 | 895.0163 |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | charter | 35 | 0.028306 | 6.2372 | 0.0000 | 149.1414 | 173.6569 | 189.3710 | 205.0164 | 227.8103 | 263.2834 | 316.1618 | 351.9261 | 552.2814 |
| POOLED:CLASSIC5 | 1d | tuning | frozen3.0 | maker | 35 | 0.006873 | 6.2372 | 0.0000 | 538.2849 | 683.1799 | 865.8221 | 895.0800 | 1034.9794 | 1195.3557 | 1485.7033 | 1623.4163 | 2237.5408 |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | taker | 33 | 0.017990 | 5.0895 | 0.0000 | 123.0133 | 149.6781 | 207.7947 | 230.0123 | 276.2612 | 327.6395 | 383.9343 | 509.6098 | 606.7362 |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | charter | 33 | 0.030309 | 5.0895 | 0.0000 | 87.8666 | 104.6651 | 116.5780 | 138.1220 | 149.7011 | 181.4461 | 199.6226 | 273.1332 | 351.9836 |
| POOLED:CLASSIC5 | 1d | holdout | calibrated | maker | 33 | 0.007196 | 5.0895 | 0.0000 | 307.5331 | 374.1952 | 519.4869 | 575.0307 | 690.6531 | 819.0989 | 959.8358 | 1274.0245 | 1516.8406 |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | taker | 18 | 0.015925 | 6.4432 | 0.0000 | 225.1018 | 281.3067 | 318.9163 | 356.7148 | 459.3333 | 616.5465 | 645.4764 | 703.7548 | 897.3933 |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | charter | 18 | 0.029565 | 6.4432 | 0.0000 | 131.4544 | 153.7325 | 183.4323 | 202.5328 | 268.0081 | 311.4982 | 361.7194 | 386.3971 | 511.4267 |
| POOLED:CLASSIC5 | 1d | holdout | frozen3.0 | maker | 18 | 0.006370 | 6.4432 | 0.0000 | 562.7546 | 703.2668 | 797.2909 | 891.7869 | 1148.3334 | 1541.3661 | 1613.6911 | 1759.3869 | 2243.4833 |
| POOLED:PANEL17 | 1d | ALL | calibrated | taker | 227 | 0.014164 | 4.4066 | 0.0000 | 141.0746 | 204.3337 | 236.8096 | 276.9609 | 313.0883 | 354.4888 | 401.2460 | 541.0435 | 662.1966 |
| POOLED:PANEL17 | 1d | ALL | calibrated | charter | 227 | 0.028506 | 4.4066 | 0.0000 | 77.2007 | 102.1391 | 123.9081 | 141.2242 | 158.9704 | 176.2362 | 195.2026 | 230.2222 | 333.2033 |
| POOLED:PANEL17 | 1d | ALL | calibrated | maker | 227 | 0.005666 | 4.4066 | 0.0000 | 352.6865 | 510.8343 | 592.0240 | 692.4023 | 782.7207 | 886.2221 | 1003.1151 | 1352.6089 | 1655.4916 |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | taker | 121 | 0.015409 | 6.2806 | 0.0000 | 212.1723 | 272.8942 | 318.8449 | 374.6137 | 436.8702 | 548.5298 | 634.3795 | 731.7444 | 1334.7438 |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | charter | 121 | 0.031407 | 6.2806 | 0.0000 | 107.7362 | 138.1306 | 165.6646 | 189.6189 | 206.9959 | 256.2219 | 312.0502 | 396.4853 | 595.4615 |
| POOLED:PANEL17 | 1d | ALL | frozen3.0 | maker | 121 | 0.006164 | 6.2806 | 0.0000 | 530.4308 | 682.2356 | 797.1124 | 936.5342 | 1092.1755 | 1371.3246 | 1585.9488 | 1829.3611 | 3336.8594 |
| POOLED:PANEL17 | 1d | tuning | calibrated | taker | 129 | 0.013268 | 4.3727 | 0.0000 | 155.3613 | 208.0506 | 261.1193 | 286.3869 | 319.7953 | 358.7294 | 400.3756 | 538.5398 | 686.0323 |
| POOLED:PANEL17 | 1d | tuning | calibrated | charter | 129 | 0.026055 | 4.3727 | 0.0000 | 82.8165 | 109.4942 | 139.0278 | 156.8943 | 170.2438 | 190.6355 | 205.8817 | 245.2138 | 358.2535 |
| POOLED:PANEL17 | 1d | tuning | calibrated | maker | 129 | 0.005307 | 4.3727 | 0.0000 | 388.4031 | 520.1264 | 652.7983 | 715.9673 | 799.4883 | 896.8234 | 1000.9390 | 1346.3496 | 1715.0808 |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | taker | 70 | 0.016074 | 6.3145 | 0.0000 | 212.0491 | 271.4364 | 340.5076 | 373.2584 | 446.2454 | 552.3239 | 634.8823 | 701.6771 | 893.2579 |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | charter | 70 | 0.029786 | 6.3145 | 0.0000 | 125.5062 | 156.7322 | 178.8172 | 195.1268 | 225.5717 | 262.5216 | 311.2858 | 379.4077 | 475.8076 |
| POOLED:PANEL17 | 1d | tuning | frozen3.0 | maker | 70 | 0.006430 | 6.3145 | 0.0000 | 530.1227 | 678.5910 | 851.2689 | 933.1460 | 1115.6135 | 1380.8097 | 1587.2056 | 1754.1926 | 2233.1448 |
| POOLED:PANEL17 | 1d | holdout | calibrated | taker | 98 | 0.014906 | 4.4221 | 0.0000 | 122.2901 | 181.6271 | 227.3122 | 252.7128 | 297.9168 | 341.9397 | 404.7870 | 531.2949 | 645.2447 |
| POOLED:PANEL17 | 1d | holdout | calibrated | charter | 98 | 0.032926 | 4.4221 | 0.0000 | 69.6440 | 95.5136 | 113.0659 | 125.1526 | 141.3772 | 158.1287 | 186.5742 | 205.7981 | 322.6223 |
| POOLED:PANEL17 | 1d | holdout | calibrated | maker | 98 | 0.005963 | 4.4221 | 0.0000 | 305.7252 | 454.0677 | 568.2805 | 631.7821 | 744.7920 | 854.8492 | 1011.9674 | 1328.2372 | 1613.1117 |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | taker | 51 | 0.013752 | 6.2686 | 0.0000 | 215.4725 | 276.2612 | 308.3803 | 374.6137 | 426.3404 | 544.0530 | 616.5734 | 766.1575 | 1466.0657 |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | charter | 51 | 0.033133 | 6.2686 | 0.0000 | 102.7934 | 123.4252 | 145.5457 | 170.7513 | 192.1481 | 227.7464 | 324.3439 | 444.9146 | 601.8052 |
| POOLED:PANEL17 | 1d | holdout | frozen3.0 | maker | 51 | 0.005501 | 6.2686 | 0.0000 | 538.6812 | 690.6531 | 770.9506 | 936.5342 | 1065.8509 | 1360.1326 | 1541.4335 | 1915.3937 | 3665.1644 |
| ASSET:BTCUSDT | 1w | ALL | calibrated | taker | 3 | 0.006855 | 4.4511 | 0.0000 | 588.4162 | 636.3772 | 684.3383 | 732.2994 | 780.2605 | 810.8115 | 841.3625 | 871.9135 | 902.4645 |
| ASSET:BTCUSDT | 1w | ALL | calibrated | charter | 3 | 0.009597 | 4.4511 | 0.0000 | 420.2973 | 454.5552 | 488.8131 | 523.0710 | 557.3290 | 579.1511 | 600.9732 | 622.7954 | 644.6175 |
| ASSET:BTCUSDT | 1w | ALL | calibrated | maker | 3 | 0.002742 | 4.4511 | 0.0000 | 1471.0404 | 1590.9431 | 1710.8459 | 1830.7486 | 1950.6513 | 2027.0288 | 2103.4063 | 2179.7837 | 2256.1612 |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | taker | 2 | 0.011810 | 7.8623 | 0.0000 | 513.5572 | 543.1909 | 572.8246 | 602.4583 | 632.0920 | 661.7257 | 691.3594 | 720.9931 | 750.6268 |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | charter | 2 | 0.016534 | 7.8623 | 0.0000 | 366.8266 | 387.9935 | 409.1605 | 430.3274 | 451.4943 | 472.6612 | 493.8282 | 514.9951 | 536.1620 |
| ASSET:BTCUSDT | 1w | ALL | frozen3.0 | maker | 2 | 0.004724 | 7.8623 | 0.0000 | 1283.8931 | 1357.9774 | 1432.0616 | 1506.1458 | 1580.2301 | 1654.3143 | 1728.3986 | 1802.4828 | 1876.5671 |
| ASSET:BTCUSDT | 1w | tuning | calibrated | taker | 3 | 0.006855 | 4.4511 | 0.0000 | 588.4162 | 636.3772 | 684.3383 | 732.2994 | 780.2605 | 810.8115 | 841.3625 | 871.9135 | 902.4645 |
| ASSET:BTCUSDT | 1w | tuning | calibrated | charter | 3 | 0.009597 | 4.4511 | 0.0000 | 420.2973 | 454.5552 | 488.8131 | 523.0710 | 557.3290 | 579.1511 | 600.9732 | 622.7954 | 644.6175 |
| ASSET:BTCUSDT | 1w | tuning | calibrated | maker | 3 | 0.002742 | 4.4511 | 0.0000 | 1471.0404 | 1590.9431 | 1710.8459 | 1830.7486 | 1950.6513 | 2027.0288 | 2103.4063 | 2179.7837 | 2256.1612 |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | taker | 2 | 0.011810 | 7.8623 | 0.0000 | 513.5572 | 543.1909 | 572.8246 | 602.4583 | 632.0920 | 661.7257 | 691.3594 | 720.9931 | 750.6268 |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | charter | 2 | 0.016534 | 7.8623 | 0.0000 | 366.8266 | 387.9935 | 409.1605 | 430.3274 | 451.4943 | 472.6612 | 493.8282 | 514.9951 | 536.1620 |
| ASSET:BTCUSDT | 1w | tuning | frozen3.0 | maker | 2 | 0.004724 | 7.8623 | 0.0000 | 1283.8931 | 1357.9774 | 1432.0616 | 1506.1458 | 1580.2301 | 1654.3143 | 1728.3986 | 1802.4828 | 1876.5671 |
| ASSET:BTCUSDT | 1w | holdout | calibrated | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:BTCUSDT | 1w | holdout | calibrated | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:BTCUSDT | 1w | holdout | calibrated | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:BTCUSDT | 1w | holdout | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ETHUSDT | 1w | ALL | calibrated | taker | 3 | 0.004067 | 6.2274 | 0.0000 | 1251.3139 | 1321.3184 | 1391.3229 | 1461.3275 | 1531.3320 | 1579.5755 | 1627.8191 | 1676.0626 | 1724.3061 |
| ASSET:ETHUSDT | 1w | ALL | calibrated | charter | 3 | 0.005693 | 6.2274 | 0.0000 | 893.7956 | 943.7989 | 993.8021 | 1043.8053 | 1093.8086 | 1128.2682 | 1162.7279 | 1197.1876 | 1231.6472 |
| ASSET:ETHUSDT | 1w | ALL | calibrated | maker | 3 | 0.001627 | 6.2274 | 0.0000 | 3128.2848 | 3303.2961 | 3478.3074 | 3653.3187 | 3828.3300 | 3948.9388 | 4069.5476 | 4190.1565 | 4310.7653 |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | taker | 3 | 0.004067 | 6.2274 | 0.0000 | 1251.3139 | 1321.3184 | 1391.3229 | 1461.3275 | 1531.3320 | 1579.5755 | 1627.8191 | 1676.0626 | 1724.3061 |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | charter | 3 | 0.005693 | 6.2274 | 0.0000 | 893.7956 | 943.7989 | 993.8021 | 1043.8053 | 1093.8086 | 1128.2682 | 1162.7279 | 1197.1876 | 1231.6472 |
| ASSET:ETHUSDT | 1w | ALL | frozen3.0 | maker | 3 | 0.001627 | 6.2274 | 0.0000 | 3128.2848 | 3303.2961 | 3478.3074 | 3653.3187 | 3828.3300 | 3948.9388 | 4069.5476 | 4190.1565 | 4310.7653 |
| ASSET:ETHUSDT | 1w | tuning | calibrated | taker | 1 | 0.004084 | 4.8248 | 0.0000 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 |
| ASSET:ETHUSDT | 1w | tuning | calibrated | charter | 1 | 0.005718 | 4.8248 | 0.0000 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 |
| ASSET:ETHUSDT | 1w | tuning | calibrated | maker | 1 | 0.001634 | 4.8248 | 0.0000 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | taker | 1 | 0.004084 | 4.8248 | 0.0000 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 | 1181.3094 |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | charter | 1 | 0.005718 | 4.8248 | 0.0000 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 | 843.7924 |
| ASSET:ETHUSDT | 1w | tuning | frozen3.0 | maker | 1 | 0.001634 | 4.8248 | 0.0000 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 | 2953.2734 |
| ASSET:ETHUSDT | 1w | holdout | calibrated | taker | 2 | 0.003815 | 6.2716 | 0.0000 | 1555.4538 | 1579.5755 | 1603.6973 | 1627.8191 | 1651.9408 | 1676.0626 | 1700.1844 | 1724.3061 | 1748.4279 |
| ASSET:ETHUSDT | 1w | holdout | calibrated | charter | 2 | 0.005341 | 6.2716 | 0.0000 | 1111.0384 | 1128.2682 | 1145.4981 | 1162.7279 | 1179.9577 | 1197.1876 | 1214.4174 | 1231.6472 | 1248.8771 |
| ASSET:ETHUSDT | 1w | holdout | calibrated | maker | 2 | 0.001526 | 6.2716 | 0.0000 | 3888.6344 | 3948.9388 | 4009.2432 | 4069.5476 | 4129.8521 | 4190.1565 | 4250.4609 | 4310.7653 | 4371.0697 |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | taker | 2 | 0.003815 | 6.2716 | 0.0000 | 1555.4538 | 1579.5755 | 1603.6973 | 1627.8191 | 1651.9408 | 1676.0626 | 1700.1844 | 1724.3061 | 1748.4279 |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | charter | 2 | 0.005341 | 6.2716 | 0.0000 | 1111.0384 | 1128.2682 | 1145.4981 | 1162.7279 | 1179.9577 | 1197.1876 | 1214.4174 | 1231.6472 | 1248.8771 |
| ASSET:ETHUSDT | 1w | holdout | frozen3.0 | maker | 2 | 0.001526 | 6.2716 | 0.0000 | 3888.6344 | 3948.9388 | 4009.2432 | 4069.5476 | 4129.8521 | 4190.1565 | 4250.4609 | 4310.7653 | 4371.0697 |
| ASSET:SOLUSDT | 1w | ALL | calibrated | taker | 2 | 0.005856 | 5.5505 | 0.0000 | 830.5691 | 850.4043 | 870.2396 | 890.0748 | 909.9101 | 929.7453 | 949.5806 | 969.4158 | 989.2511 |
| ASSET:SOLUSDT | 1w | ALL | calibrated | charter | 2 | 0.011712 | 5.5505 | 0.0000 | 415.2845 | 425.2022 | 435.1198 | 445.0374 | 454.9550 | 464.8727 | 474.7903 | 484.7079 | 494.6255 |
| ASSET:SOLUSDT | 1w | ALL | calibrated | maker | 2 | 0.002342 | 5.5505 | 0.0000 | 2076.4227 | 2126.0108 | 2175.5989 | 2225.1870 | 2274.7752 | 2324.3633 | 2373.9514 | 2423.5395 | 2473.1277 |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | taker | 1 | 0.008093 | 8.1665 | 0.0000 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | charter | 1 | 0.016186 | 8.1665 | 0.0000 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 |
| ASSET:SOLUSDT | 1w | ALL | frozen3.0 | maker | 1 | 0.003237 | 8.1665 | 0.0000 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 |
| ASSET:SOLUSDT | 1w | tuning | calibrated | taker | 1 | 0.003619 | 2.9344 | 0.0000 | 810.7338 | 810.7338 | 810.7338 | 810.7338 | 810.7338 | 810.7338 | 810.7338 | 810.7338 | 810.7338 |
| ASSET:SOLUSDT | 1w | tuning | calibrated | charter | 1 | 0.007239 | 2.9344 | 0.0000 | 405.3669 | 405.3669 | 405.3669 | 405.3669 | 405.3669 | 405.3669 | 405.3669 | 405.3669 | 405.3669 |
| ASSET:SOLUSDT | 1w | tuning | calibrated | maker | 1 | 0.001448 | 2.9344 | 0.0000 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 | 2026.8346 |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:SOLUSDT | 1w | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:SOLUSDT | 1w | holdout | calibrated | taker | 1 | 0.008093 | 8.1665 | 0.0000 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 |
| ASSET:SOLUSDT | 1w | holdout | calibrated | charter | 1 | 0.016186 | 8.1665 | 0.0000 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 |
| ASSET:SOLUSDT | 1w | holdout | calibrated | maker | 1 | 0.003237 | 8.1665 | 0.0000 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | taker | 1 | 0.008093 | 8.1665 | 0.0000 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 | 1009.0863 |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | charter | 1 | 0.016186 | 8.1665 | 0.0000 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 | 504.5432 |
| ASSET:SOLUSDT | 1w | holdout | frozen3.0 | maker | 1 | 0.003237 | 8.1665 | 0.0000 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 | 2522.7158 |
| ASSET:NEARUSDT | 1w | ALL | calibrated | taker | 2 | 0.001754 | 10.4905 | 0.0000 | 5610.8126 | 5671.5796 | 5732.3465 | 5793.1135 | 5853.8805 | 5914.6474 | 5975.4144 | 6036.1813 | 6096.9483 |
| ASSET:NEARUSDT | 1w | ALL | calibrated | charter | 2 | 0.003507 | 10.4905 | 0.0000 | 2805.4063 | 2835.7898 | 2866.1733 | 2896.5568 | 2926.9402 | 2957.3237 | 2987.7072 | 3018.0907 | 3048.4742 |
| ASSET:NEARUSDT | 1w | ALL | calibrated | maker | 2 | 0.000701 | 10.4905 | 0.0000 | 14027.0316 | 14178.9490 | 14330.8664 | 14482.7838 | 14634.7012 | 14786.6186 | 14938.5360 | 15090.4534 | 15242.3708 |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | taker | 2 | 0.001754 | 10.4905 | 0.0000 | 5610.8126 | 5671.5796 | 5732.3465 | 5793.1135 | 5853.8805 | 5914.6474 | 5975.4144 | 6036.1813 | 6096.9483 |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | charter | 2 | 0.003507 | 10.4905 | 0.0000 | 2805.4063 | 2835.7898 | 2866.1733 | 2896.5568 | 2926.9402 | 2957.3237 | 2987.7072 | 3018.0907 | 3048.4742 |
| ASSET:NEARUSDT | 1w | ALL | frozen3.0 | maker | 2 | 0.000701 | 10.4905 | 0.0000 | 14027.0316 | 14178.9490 | 14330.8664 | 14482.7838 | 14634.7012 | 14786.6186 | 14938.5360 | 15090.4534 | 15242.3708 |
| ASSET:NEARUSDT | 1w | tuning | calibrated | taker | 1 | 0.001011 | 5.6113 | 0.0000 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 |
| ASSET:NEARUSDT | 1w | tuning | calibrated | charter | 1 | 0.002022 | 5.6113 | 0.0000 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 |
| ASSET:NEARUSDT | 1w | tuning | calibrated | maker | 1 | 0.000404 | 5.6113 | 0.0000 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | taker | 1 | 0.001011 | 5.6113 | 0.0000 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 | 5550.0457 |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | charter | 1 | 0.002022 | 5.6113 | 0.0000 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 | 2775.0228 |
| ASSET:NEARUSDT | 1w | tuning | frozen3.0 | maker | 1 | 0.000404 | 5.6113 | 0.0000 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 | 13875.1142 |
| ASSET:NEARUSDT | 1w | holdout | calibrated | taker | 1 | 0.002496 | 15.3697 | 0.0000 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 |
| ASSET:NEARUSDT | 1w | holdout | calibrated | charter | 1 | 0.004992 | 15.3697 | 0.0000 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 |
| ASSET:NEARUSDT | 1w | holdout | calibrated | maker | 1 | 0.000998 | 15.3697 | 0.0000 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | taker | 1 | 0.002496 | 15.3697 | 0.0000 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 | 6157.7153 |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | charter | 1 | 0.004992 | 15.3697 | 0.0000 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 | 3078.8576 |
| ASSET:NEARUSDT | 1w | holdout | frozen3.0 | maker | 1 | 0.000998 | 15.3697 | 0.0000 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 | 15394.2882 |
| ASSET:ZECUSDT | 1w | ALL | calibrated | taker | 3 | 0.004947 | 4.3414 | 0.0000 | 683.0653 | 731.6772 | 780.2891 | 828.9010 | 877.5130 | 1046.1734 | 1214.8339 | 1383.4944 | 1552.1548 |
| ASSET:ZECUSDT | 1w | ALL | calibrated | charter | 3 | 0.009895 | 4.3414 | 0.0000 | 341.5327 | 365.8386 | 390.1446 | 414.4505 | 438.7565 | 523.0867 | 607.4169 | 691.7472 | 776.0774 |
| ASSET:ZECUSDT | 1w | ALL | calibrated | maker | 3 | 0.001979 | 4.3414 | 0.0000 | 1707.6633 | 1829.1931 | 1950.7229 | 2072.2526 | 2193.7824 | 2615.4336 | 3037.0847 | 3458.7359 | 3880.3871 |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | taker | 1 | 0.009311 | 10.2604 | 0.0000 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | charter | 1 | 0.018623 | 10.2604 | 0.0000 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 |
| ASSET:ZECUSDT | 1w | ALL | frozen3.0 | maker | 1 | 0.003725 | 10.2604 | 0.0000 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 |
| ASSET:ZECUSDT | 1w | tuning | calibrated | taker | 1 | 0.004947 | 4.3414 | 0.0000 | 877.5130 | 877.5130 | 877.5130 | 877.5130 | 877.5130 | 877.5130 | 877.5130 | 877.5130 | 877.5130 |
| ASSET:ZECUSDT | 1w | tuning | calibrated | charter | 1 | 0.009895 | 4.3414 | 0.0000 | 438.7565 | 438.7565 | 438.7565 | 438.7565 | 438.7565 | 438.7565 | 438.7565 | 438.7565 | 438.7565 |
| ASSET:ZECUSDT | 1w | tuning | calibrated | maker | 1 | 0.001979 | 4.3414 | 0.0000 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 | 2193.7824 |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | taker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | charter | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ZECUSDT | 1w | tuning | frozen3.0 | maker | 0 | — | — | — | — | — | — | — | — | — | — | — | — |
| ASSET:ZECUSDT | 1w | holdout | calibrated | taker | 2 | 0.004248 | 4.1610 | 0.0000 | 743.0896 | 851.7258 | 960.3620 | 1068.9982 | 1177.6344 | 1286.2706 | 1394.9068 | 1503.5429 | 1612.1791 |
| ASSET:ZECUSDT | 1w | holdout | calibrated | charter | 2 | 0.008496 | 4.1610 | 0.0000 | 371.5448 | 425.8629 | 480.1810 | 534.4991 | 588.8172 | 643.1353 | 697.4534 | 751.7715 | 806.0896 |
| ASSET:ZECUSDT | 1w | holdout | calibrated | maker | 2 | 0.001699 | 4.1610 | 0.0000 | 1857.7240 | 2129.3145 | 2400.9050 | 2672.4955 | 2944.0859 | 3215.6764 | 3487.2669 | 3758.8573 | 4030.4478 |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | taker | 1 | 0.009311 | 10.2604 | 0.0000 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 | 1101.9280 |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | charter | 1 | 0.018623 | 10.2604 | 0.0000 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 | 550.9640 |
| ASSET:ZECUSDT | 1w | holdout | frozen3.0 | maker | 1 | 0.003725 | 10.2604 | 0.0000 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 | 2754.8199 |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | taker | 13 | 0.004084 | 4.8248 | 0.0000 | 663.6148 | 792.4498 | 850.8013 | 921.9150 | 1009.0863 | 1251.3139 | 1607.1253 | 1751.8559 | 4794.5465 |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | charter | 13 | 0.006679 | 4.8248 | 0.0000 | 389.9048 | 418.7227 | 478.2285 | 546.7718 | 666.4396 | 847.1155 | 953.7680 | 1197.1876 | 2473.2396 |
| POOLED:CLASSIC5 | 1w | ALL | calibrated | maker | 13 | 0.001634 | 4.8248 | 0.0000 | 1659.0371 | 1981.1246 | 2127.0033 | 2304.7874 | 2522.7158 | 3128.2848 | 4017.8133 | 4379.6398 | 11986.3662 |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | taker | 9 | 0.004084 | 6.3158 | 0.0000 | 720.9931 | 917.5560 | 1046.2230 | 1117.8042 | 1181.3094 | 1461.3275 | 1676.0626 | 3283.5481 | 5671.5796 |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | charter | 9 | 0.005718 | 6.3158 | 0.0000 | 472.7665 | 532.3956 | 553.5100 | 614.6216 | 843.7924 | 1043.8053 | 1197.1876 | 1869.6733 | 2835.7898 |
| POOLED:CLASSIC5 | 1w | ALL | frozen3.0 | maker | 9 | 0.001634 | 6.3158 | 0.0000 | 1802.4828 | 2293.8900 | 2615.5574 | 2794.5106 | 2953.2734 | 3653.3187 | 4190.1565 | 8208.8701 | 14178.9490 |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | taker | 7 | 0.004771 | 4.4511 | 0.0000 | 684.3383 | 786.3552 | 804.6392 | 837.4455 | 877.5130 | 910.8145 | 982.6743 | 1131.6506 | 2928.8039 |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | charter | 7 | 0.007239 | 4.4511 | 0.0000 | 397.6359 | 412.0448 | 432.0786 | 486.1855 | 557.3290 | 622.7954 | 701.9102 | 808.3219 | 1616.2846 |
| POOLED:CLASSIC5 | 1w | tuning | calibrated | maker | 7 | 0.001908 | 4.4511 | 0.0000 | 1710.8459 | 1965.8880 | 2011.5979 | 2093.6137 | 2193.7824 | 2277.0362 | 2456.6856 | 2829.1265 | 7322.0097 |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | taker | 4 | 0.006607 | 5.2181 | 0.0000 | 572.8246 | 661.7257 | 750.6268 | 860.4703 | 980.7850 | 1101.0996 | 1618.1830 | 2928.8039 | 4239.4248 |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | charter | 4 | 0.009250 | 5.2181 | 0.0000 | 409.1605 | 472.6612 | 536.1620 | 614.6216 | 700.5607 | 786.4997 | 1036.9155 | 1616.2846 | 2195.6537 |
| POOLED:CLASSIC5 | 1w | tuning | frozen3.0 | maker | 4 | 0.002643 | 5.2181 | 0.0000 | 1432.0616 | 1654.3143 | 1876.5671 | 2151.1758 | 2451.9624 | 2752.7490 | 4045.4575 | 7322.0097 | 10598.5619 |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | taker | 6 | 0.003815 | 6.2716 | 0.0000 | 821.7699 | 1009.0863 | 1270.2092 | 1531.3320 | 1626.0737 | 1720.8153 | 1746.6825 | 1772.5497 | 3965.1325 |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | charter | 6 | 0.005545 | 6.2716 | 0.0000 | 410.8849 | 504.5432 | 682.4754 | 860.4077 | 977.1081 | 1093.8086 | 1179.9577 | 1266.1069 | 2172.4823 |
| POOLED:CLASSIC5 | 1w | holdout | calibrated | maker | 6 | 0.001526 | 6.2716 | 0.0000 | 2054.4247 | 2522.7158 | 3175.5229 | 3828.3300 | 4065.1841 | 4302.0383 | 4366.7062 | 4431.3741 | 9912.8311 |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | taker | 5 | 0.004067 | 8.1665 | 0.0000 | 1046.2230 | 1083.3596 | 1187.8088 | 1359.5704 | 1531.3320 | 1627.8191 | 1724.3061 | 2649.5828 | 4403.6490 |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | charter | 5 | 0.005693 | 8.1665 | 0.0000 | 523.1115 | 541.6798 | 659.5329 | 876.6707 | 1093.8086 | 1162.7279 | 1231.6472 | 1628.6570 | 2353.7573 |
| POOLED:CLASSIC5 | 1w | holdout | frozen3.0 | maker | 5 | 0.001627 | 8.1665 | 0.0000 | 2615.5574 | 2708.3991 | 2969.5219 | 3398.9259 | 3828.3300 | 4069.5476 | 4310.7653 | 6623.9569 | 11009.1225 |
