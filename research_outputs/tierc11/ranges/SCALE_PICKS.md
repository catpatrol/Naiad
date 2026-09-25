# TIER-C11 · TC11-R · SCALE PICKS (L-R.2) — filed once, the picks are pins

as_of_last_closed_4h: 2026-09-25T00:00:00Z · substrate tc11_20260925 · seed 20260924

L-R.2: pick of record = C.calibrate(tape.head(C.era_cut(tape))) — the 11-cell grid 1.5..4.0, the density nearest 0.75 confirmed ranges / 100 bars, ties toward 3.0 then lower — on the TUNING era (bar CLOSE <= 2024-06-30T23:59:59Z); where the tuning era holds fewer than 400 bars of the lens the pick falls back to the WHOLE tape and is labelled IN-SAMPLE everywhere. calibrate()'s hard-coded calibrated_in_sample=True is overwritten with the true flag. The whole-tape pick, the first-half-of-tuning pick (stability) and the frozen 3.0 ride beside. The picks are PINS: every reader takes them from this file and never re-fits.

era cut: bar CLOSE <= 2024-06-30T23:59:59Z (1719791999000); fallback below 400 tuning bars; grid [1.5, 1.75, 2.0, 2.25, 2.5, 2.75, 3.0, 3.25, 3.5, 3.75, 4.0]; target 0.75 / 100 bars; tie-break: nearest density; then toward 3.0; then the lower SCALE.

## The 12 pins, key order of record

- LEG_MIN = 0.5
- REV_MIN = 1.75
- TOUCH_EPS = 0.6
- DEV_RETURN_BARS = 7
- BREAK_CONFIRM_N = 8
- BREAK_MARGIN = 1.5
- BOUNDARY_MODE = 'body'
- SCALE_MULT = 3.0
- FLIP_HOLD_MARGIN = 1.0
- FLIP_HOLD_BARS = 6
- MEM_TTL_BARS = 400
- ATR_LEN = 14

## Picks per asset x lens

| asset | lens | bars | tuning bars | PICK OF RECORD | window | tuning | whole tape | first half | stable | frozen | density@pick | edge | label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 5m | 741097 | 506088 | **1.5** | tuning | 1.5 | 1.75 | 1.5 | True | 3 | 0.8036 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 15m | 247033 | 168696 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.7943 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 1h | 61759 | 42174 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.8228 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 4h | 15440 | 10543 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7303 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 12h | 5147 | 3514 | **2** | tuning | 2 | 1.75 | 1.75 | False | 3 | 0.6545 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 1d | 2573 | 1756 | **2.25** | tuning | 2.25 | 2.25 | 2 | False | 3 | 0.6834 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BTCUSDT | 1w | 367 | 250 | **2.5** | whole-tape (fallback) | — | 2.5 | — | — | 3 | 0.8174 | False | IN-SAMPLE (fallback: the tuning era holds 250 < 400 bars of this lens; fit on the whole tape) |
| ETHUSDT | 5m | 718179 | 483170 | **1.5** | tuning | 1.5 | 1.75 | 1.5 | True | 3 | 0.7956 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 15m | 239393 | 161056 | **2** | tuning | 2 | 1.75 | 2 | True | 3 | 0.6886 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 1h | 59849 | 40264 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7476 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 4h | 14963 | 10066 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7351 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 12h | 4988 | 3355 | **1.5** | tuning | 1.5 | 2 | 2 | False | 3 | 0.8048 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 1d | 2493 | 1676 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7757 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ETHUSDT | 1w | 355 | 238 | **3** | whole-tape (fallback) | — | 3 | — | — | 3 | 0.8451 | False | IN-SAMPLE (fallback: the tuning era holds 238 < 400 bars of this lens; fit on the whole tape) |
| SOLUSDT | 5m | 634092 | 399083 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.7943 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 15m | 211364 | 133027 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.8059 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 1h | 52841 | 33256 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.7848 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 4h | 13211 | 8314 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7096 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 12h | 4404 | 2771 | **2.25** | tuning | 2.25 | 2.25 | 1.75 | False | 3 | 0.7578 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 1d | 2201 | 1384 | **2.25** | tuning | 2.25 | 2.5 | 2 | False | 3 | 0.7948 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SOLUSDT | 1w | 313 | 196 | **1.75** | whole-tape (fallback) | — | 1.75 | — | — | 3 | 0.6390 | False | IN-SAMPLE (fallback: the tuning era holds 196 < 400 bars of this lens; fit on the whole tape) |
| NEARUSDT | 5m | 625152 | 390143 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.7800 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 15m | 208384 | 130047 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.8051 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 1h | 52096 | 32511 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.8120 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 4h | 13024 | 8127 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.7875 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 12h | 4342 | 2709 | **2.25** | tuning | 2.25 | 2 | 2.25 | True | 3 | 0.7383 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 1d | 2170 | 1353 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.8130 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| NEARUSDT | 1w | 309 | 192 | **3** | whole-tape (fallback) | — | 3 | — | — | 3 | 0.6472 | False | IN-SAMPLE (fallback: the tuning era holds 192 < 400 bars of this lens; fit on the whole tape) |
| ZECUSDT | 5m | 698016 | 463007 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.7795 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 15m | 232672 | 154335 | **1.75** | tuning | 1.75 | 1.75 | 1.75 | True | 3 | 0.7490 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 1h | 58168 | 38583 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.6842 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 4h | 14542 | 9645 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7361 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 12h | 4848 | 3215 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.6843 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 1d | 2423 | 1606 | **2.5** | tuning | 2.5 | 2.5 | 2.5 | True | 3 | 0.8095 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ZECUSDT | 1w | 345 | 228 | **2.5** | whole-tape (fallback) | — | 2.5 | — | — | 3 | 0.8696 | False | IN-SAMPLE (fallback: the tuning era holds 228 < 400 bars of this lens; fit on the whole tape) |
| ENAUSDT | 1h | 21732 | 2147 | **1.5** | tuning | 1.5 | 1.75 | 2.5 | False | 3 | 0.5123 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ENAUSDT | 4h | 5433 | 536 | **2.75** | tuning | 2.75 | 2.25 | 2.75 | True | 3 | 0.7463 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| ENAUSDT | 1d | 905 | 88 | **2** | whole-tape (fallback) | — | 2 | — | — | 3 | 0.6630 | False | IN-SAMPLE (fallback: the tuning era holds 88 < 400 bars of this lens; fit on the whole tape) |
| PUMPUSDT | 1h | 10601 | 0 | **2** | whole-tape (fallback) | — | 2 | — | — | 3 | 0.7075 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| PUMPUSDT | 4h | 2651 | 0 | **2.25** | whole-tape (fallback) | — | 2.25 | — | — | 3 | 0.7922 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| PUMPUSDT | 1d | 441 | 0 | **1.75** | whole-tape (fallback) | — | 1.75 | — | — | 3 | 0.6803 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| HYPEUSDT | 1h | 11582 | 0 | **2** | whole-tape (fallback) | — | 2 | — | — | 3 | 0.7080 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| HYPEUSDT | 4h | 2896 | 0 | **1.75** | whole-tape (fallback) | — | 1.75 | — | — | 3 | 0.7597 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| HYPEUSDT | 1d | 482 | 0 | **2.25** | whole-tape (fallback) | — | 2.25 | — | — | 3 | 0.8299 | False | IN-SAMPLE (fallback: the tuning era holds 0 < 400 bars of this lens; fit on the whole tape) |
| MNTUSDT_BYBIT | 1h | 26130 | 6545 | **2.25** | tuning | 2.25 | 2 | 2 | False | 3 | 0.7028 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| MNTUSDT_BYBIT | 4h | 6533 | 1636 | **2** | tuning | 2 | 2 | 3 | False | 3 | 0.9169 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| MNTUSDT_BYBIT | 1d | 1088 | 271 | **2.25** | whole-tape (fallback) | — | 2.25 | — | — | 3 | 0.7353 | False | IN-SAMPLE (fallback: the tuning era holds 271 < 400 bars of this lens; fit on the whole tape) |
| SUIUSDT | 1h | 29768 | 10183 | **2** | tuning | 2 | 2 | 1.75 | False | 3 | 0.8445 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SUIUSDT | 4h | 7442 | 2545 | **2.25** | tuning | 2.25 | 1.75 | 2.25 | True | 3 | 0.7466 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| SUIUSDT | 1d | 1240 | 423 | **2.25** | tuning | 2.25 | 2.5 | 2.25 | True | 3 | 0.9456 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| LTCUSDT | 1h | 58816 | 39231 | **1.75** | tuning | 1.75 | 1.75 | 2 | False | 3 | 0.7698 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| LTCUSDT | 4h | 14704 | 9807 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7342 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| LTCUSDT | 1d | 2450 | 1633 | **2.25** | tuning | 2.25 | 2.25 | 2.25 | True | 3 | 0.7348 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| XMRUSDT | 1h | 58216 | 38631 | **1.5** | tuning | 1.5 | 1.5 | 1.75 | False | 3 | 0.7585 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| XMRUSDT | 4h | 14554 | 9657 | **1.75** | tuning | 1.75 | 1.5 | 2 | False | 3 | 0.7559 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| XMRUSDT | 1d | 2425 | 1608 | **1.5** | tuning | 1.5 | 1.5 | 2 | False | 3 | 0.6219 | True | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BNBUSDT | 1h | 58048 | 38463 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.8060 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BNBUSDT | 4h | 14512 | 9615 | **2** | tuning | 2 | 1.75 | 2 | True | 3 | 0.6968 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| BNBUSDT | 1d | 2418 | 1601 | **1.75** | tuning | 1.75 | 2 | 2 | False | 3 | 0.8745 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| UNIUSDT | 1h | 52745 | 33160 | **2** | tuning | 2 | 2 | 2 | True | 3 | 0.7027 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| UNIUSDT | 4h | 13187 | 8290 | **2** | tuning | 2 | 2 | 1.75 | False | 3 | 0.6876 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| UNIUSDT | 1d | 2197 | 1380 | **2.25** | tuning | 2.25 | 2.25 | 2.25 | True | 3 | 0.6522 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000PEPEUSDT | 1h | 29720 | 10135 | **1.75** | tuning | 1.75 | 1.75 | 1.75 | True | 3 | 0.7499 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000PEPEUSDT | 4h | 7430 | 2533 | **2** | tuning | 2 | 1.75 | 1.75 | False | 3 | 0.7106 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000PEPEUSDT | 1d | 1238 | 421 | **3** | tuning | 3 | 2.25 | 2 | False | 3 | 0.7126 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| DOGEUSDT | 1h | 54423 | 34838 | **1.75** | tuning | 1.75 | 1.75 | 1.75 | True | 3 | 0.6975 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| DOGEUSDT | 4h | 13606 | 8709 | **1.75** | tuning | 1.75 | 1.75 | 1.5 | False | 3 | 0.5626 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| DOGEUSDT | 1d | 2267 | 1450 | **2.25** | tuning | 2.25 | 2.25 | 2.75 | False | 3 | 0.7586 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000BONKUSDT | 1h | 24898 | 5313 | **2** | tuning | 2 | 1.75 | 2.5 | False | 3 | 0.7905 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000BONKUSDT | 4h | 6225 | 1328 | **2** | tuning | 2 | 1.75 | 2 | True | 3 | 0.6777 | False | OUT-OF-SAMPLE for holdout (tuning-era pick; IN-SAMPLE for tuning) |
| 1000BONKUSDT | 1d | 1037 | 220 | **2** | whole-tape (fallback) | — | 2 | — | — | 3 | 0.6750 | False | IN-SAMPLE (fallback: the tuning era holds 220 < 400 bars of this lens; fit on the whole tape) |

## Stability (CLASSIC5 x {1h, 4h, 12h}): first half of tuning vs the whole tuning era

- CHANGED: BTCUSDT 1h: first half 2.0 vs tuning 1.75
- CHANGED: BTCUSDT 12h: first half 1.75 vs tuning 2.0
- CHANGED: ETHUSDT 12h: first half 2.0 vs tuning 1.5
- CHANGED: SOLUSDT 1h: first half 2.0 vs tuning 1.75
- CHANGED: SOLUSDT 12h: first half 1.75 vs tuning 2.25
- CHANGED: NEARUSDT 1h: first half 2.0 vs tuning 1.75
- CHANGED: NEARUSDT 4h: first half 2.0 vs tuning 1.75

## The whole density grid (confirmed ranges per 100 bars; * = the window's pick)

| asset | lens | window | bars | 1.5 | 1.75 | 2 | 2.25 | 2.5 | 2.75 | 3 | 3.25 | 3.5 | 3.75 | 4 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 5m | tuning | 506088 | 0.8036* | 0.6746 | 0.5916 | 0.5197 | 0.4651 | 0.4187 | 0.3634 | 0.3201 | 0.2968 | 0.2632 | 0.2361 |
| BTCUSDT | 5m | whole | 741097 | 0.8728 | 0.7322* | 0.6350 | 0.5558 | 0.4920 | 0.4338 | 0.3825 | 0.3391 | 0.3113 | 0.2755 | 0.2449 |
| BTCUSDT | 5m | first_half | 253044 | 0.8082* | 0.6892 | 0.6153 | 0.5288 | 0.4624 | 0.4146 | 0.3671 | 0.3300 | 0.3007 | 0.2660 | 0.2276 |
| BTCUSDT | 15m | tuning | 168696 | 0.9307 | 0.7943* | 0.6740 | 0.5803 | 0.5086 | 0.4321 | 0.3622 | 0.3124 | 0.2751 | 0.2585 | 0.2205 |
| BTCUSDT | 15m | whole | 247033 | 0.9683 | 0.8218 | 0.6963* | 0.6015 | 0.5165 | 0.4400 | 0.3716 | 0.3247 | 0.2797 | 0.2583 | 0.2214 |
| BTCUSDT | 15m | first_half | 84348 | 0.9627 | 0.8311 | 0.7161* | 0.5999 | 0.5264 | 0.4458 | 0.3663 | 0.3082 | 0.2845 | 0.2573 | 0.2276 |
| BTCUSDT | 1h | tuning | 42174 | 0.9722 | 0.8228* | 0.6568 | 0.5525 | 0.4766 | 0.4173 | 0.3604 | 0.3343 | 0.2822 | 0.2490 | 0.2253 |
| BTCUSDT | 1h | whole | 61759 | 0.9990 | 0.8452 | 0.7044* | 0.5861 | 0.5036 | 0.4161 | 0.3611 | 0.3465 | 0.3060 | 0.2736 | 0.2477 |
| BTCUSDT | 1h | first_half | 21087 | 1.0670 | 0.9295 | 0.7588* | 0.5975 | 0.5169 | 0.4173 | 0.3557 | 0.3272 | 0.2703 | 0.2466 | 0.2276 |
| BTCUSDT | 4h | tuning | 10543 | 1.1097 | 0.8821 | 0.7303* | 0.6165 | 0.5312 | 0.4648 | 0.3794 | 0.3794 | 0.3415 | 0.3130 | 0.2845 |
| BTCUSDT | 4h | whole | 15440 | 1.0687 | 0.8938 | 0.7189* | 0.6153 | 0.5570 | 0.4987 | 0.4080 | 0.3692 | 0.3303 | 0.3238 | 0.2979 |
| BTCUSDT | 4h | first_half | 5271 | 1.0624 | 0.8348 | 0.6830* | 0.5122 | 0.4553 | 0.3794 | 0.3605 | 0.3415 | 0.3415 | 0.3035 | 0.2846 |
| BTCUSDT | 12h | tuning | 3514 | 0.9106 | 0.8822 | 0.6545* | 0.5976 | 0.4269 | 0.2561 | 0.2846 | 0.3699 | 0.2561 | 0.2846 | 0.2561 |
| BTCUSDT | 12h | whole | 5147 | 0.8354 | 0.8160* | 0.6606 | 0.6023 | 0.4857 | 0.3691 | 0.3497 | 0.4080 | 0.3109 | 0.2720 | 0.2526 |
| BTCUSDT | 12h | first_half | 1757 | 0.9106 | 0.8537* | 0.5122 | 0.5122 | 0.4553 | 0.2277 | 0.2846 | 0.3415 | 0.2277 | 0.2277 | 0.2277 |
| BTCUSDT | 1d | tuning | 1756 | 1.0820 | 0.9112 | 0.8542 | 0.6834* | 0.6264 | 0.4556 | 0.4556 | 0.3417 | 0.2847 | 0.2847 | 0.2278 |
| BTCUSDT | 1d | whole | 2573 | 1.0882 | 0.9716 | 0.9328 | 0.7773* | 0.6607 | 0.4664 | 0.4275 | 0.3109 | 0.2721 | 0.2721 | 0.2721 |
| BTCUSDT | 1d | first_half | 878 | 0.9112 | 0.7973 | 0.7973* | 0.4556 | 0.4556 | 0.3417 | 0.3417 | 0.3417 | 0.3417 | 0.3417 | 0.3417 |
| BTCUSDT | 1w | whole | 367 | 1.6349 | 1.0899 | 1.0899 | 0.8174 | 0.8174* | 0.5450 | 0.5450 | 0.2725 | 0.2725 | 0.2725 | 0.2725 |
| ETHUSDT | 5m | tuning | 483170 | 0.7956* | 0.6762 | 0.6279 | 0.5394 | 0.4936 | 0.4404 | 0.3893 | 0.3413 | 0.3078 | 0.2753 | 0.2471 |
| ETHUSDT | 5m | whole | 718179 | 0.8483 | 0.7099* | 0.6390 | 0.5468 | 0.4995 | 0.4458 | 0.3929 | 0.3467 | 0.3102 | 0.2749 | 0.2430 |
| ETHUSDT | 5m | first_half | 241585 | 0.7956* | 0.6722 | 0.6602 | 0.5650 | 0.4905 | 0.4359 | 0.3816 | 0.3336 | 0.2960 | 0.2707 | 0.2413 |
| ETHUSDT | 15m | tuning | 161056 | 0.9841 | 0.8215 | 0.6886* | 0.5979 | 0.4967 | 0.4110 | 0.3595 | 0.2993 | 0.2689 | 0.2453 | 0.2179 |
| ETHUSDT | 15m | whole | 239393 | 0.9766 | 0.8175* | 0.6796 | 0.5827 | 0.4879 | 0.4165 | 0.3613 | 0.3049 | 0.2724 | 0.2398 | 0.2126 |
| ETHUSDT | 15m | first_half | 80528 | 1.0419 | 0.8804 | 0.7016* | 0.6308 | 0.5091 | 0.4172 | 0.3676 | 0.3067 | 0.2769 | 0.2384 | 0.2123 |
| ETHUSDT | 1h | tuning | 40264 | 1.0158 | 0.8817 | 0.7476* | 0.6010 | 0.4868 | 0.4719 | 0.3800 | 0.3328 | 0.3055 | 0.2682 | 0.2434 |
| ETHUSDT | 1h | whole | 59849 | 0.9875 | 0.8672 | 0.7369* | 0.6149 | 0.5096 | 0.4645 | 0.3860 | 0.3358 | 0.3125 | 0.2724 | 0.2423 |
| ETHUSDT | 1h | first_half | 20132 | 1.0829 | 0.8991 | 0.7749* | 0.6507 | 0.5265 | 0.4719 | 0.3626 | 0.3129 | 0.2732 | 0.2533 | 0.2384 |
| ETHUSDT | 4h | tuning | 10066 | 1.2120 | 0.8941 | 0.7351* | 0.6060 | 0.5265 | 0.4769 | 0.4172 | 0.3378 | 0.2980 | 0.2682 | 0.2285 |
| ETHUSDT | 4h | whole | 14963 | 1.1629 | 0.8889 | 0.7552* | 0.6483 | 0.5480 | 0.4812 | 0.4210 | 0.3542 | 0.3208 | 0.2941 | 0.2406 |
| ETHUSDT | 4h | first_half | 5033 | 1.2915 | 1.0332 | 0.6954* | 0.4570 | 0.3974 | 0.4172 | 0.3974 | 0.3179 | 0.2384 | 0.2186 | 0.1391 |
| ETHUSDT | 12h | tuning | 3355 | 0.8048* | 0.8644 | 0.6557 | 0.5365 | 0.4769 | 0.3577 | 0.2385 | 0.2683 | 0.2683 | 0.2683 | 0.1788 |
| ETHUSDT | 12h | whole | 4988 | 0.8821 | 0.8621 | 0.6616* | 0.5213 | 0.4611 | 0.4010 | 0.3007 | 0.3208 | 0.3208 | 0.3208 | 0.2807 |
| ETHUSDT | 12h | first_half | 1677 | 0.8348 | 0.9541 | 0.7752* | 0.5367 | 0.4770 | 0.4770 | 0.2982 | 0.3578 | 0.3578 | 0.3578 | 0.2385 |
| ETHUSDT | 1d | tuning | 1676 | 1.3126 | 0.9547 | 0.7757* | 0.5967 | 0.4773 | 0.4177 | 0.3580 | 0.3580 | 0.3580 | 0.2387 | 0.2387 |
| ETHUSDT | 1d | whole | 2493 | 1.2435 | 0.9627 | 0.8022* | 0.6017 | 0.5215 | 0.4412 | 0.3610 | 0.3610 | 0.3610 | 0.3610 | 0.3209 |
| ETHUSDT | 1d | first_half | 838 | 1.4320 | 0.9547 | 0.8353* | 0.5967 | 0.4773 | 0.3580 | 0.3580 | 0.3580 | 0.2387 | 0.2387 | 0.2387 |
| ETHUSDT | 1w | whole | 355 | 2.5352 | 2.2535 | 1.6901 | 1.4085 | 1.1268 | 0.8451 | 0.8451* | 0.5634 | 0.2817 | 0.2817 | 0.2817 |
| SOLUSDT | 5m | tuning | 399083 | 0.9444 | 0.7943* | 0.6693 | 0.5813 | 0.5022 | 0.4383 | 0.3896 | 0.3420 | 0.3002 | 0.2686 | 0.2443 |
| SOLUSDT | 5m | whole | 634092 | 0.9667 | 0.8086* | 0.6849 | 0.5906 | 0.5043 | 0.4375 | 0.3854 | 0.3411 | 0.2963 | 0.2653 | 0.2400 |
| SOLUSDT | 5m | first_half | 199541 | 1.0574 | 0.8820 | 0.7342* | 0.6325 | 0.5493 | 0.4726 | 0.4114 | 0.3633 | 0.3212 | 0.2781 | 0.2521 |
| SOLUSDT | 15m | tuning | 133027 | 1.0126 | 0.8059* | 0.6668 | 0.5736 | 0.4916 | 0.4360 | 0.3631 | 0.3202 | 0.2826 | 0.2526 | 0.2300 |
| SOLUSDT | 15m | whole | 211364 | 1.0092 | 0.7991* | 0.6766 | 0.5701 | 0.4906 | 0.4329 | 0.3652 | 0.3208 | 0.2891 | 0.2522 | 0.2304 |
| SOLUSDT | 15m | first_half | 66513 | 1.1066 | 0.8901 | 0.7397* | 0.6495 | 0.5352 | 0.4721 | 0.3819 | 0.3293 | 0.2887 | 0.2556 | 0.2360 |
| SOLUSDT | 1h | tuning | 33256 | 0.9863 | 0.7848* | 0.7096 | 0.6164 | 0.5322 | 0.4631 | 0.3909 | 0.3578 | 0.3037 | 0.2736 | 0.2406 |
| SOLUSDT | 1h | whole | 52841 | 1.0352 | 0.8346 | 0.7418* | 0.6169 | 0.5223 | 0.4504 | 0.3842 | 0.3388 | 0.3009 | 0.2782 | 0.2441 |
| SOLUSDT | 1h | first_half | 16628 | 1.0645 | 0.8359 | 0.7638* | 0.6555 | 0.5172 | 0.4450 | 0.3608 | 0.3488 | 0.2766 | 0.2706 | 0.2285 |
| SOLUSDT | 4h | tuning | 8314 | 1.1186 | 0.9261 | 0.7096* | 0.5894 | 0.5172 | 0.4931 | 0.4691 | 0.3608 | 0.3368 | 0.2646 | 0.2406 |
| SOLUSDT | 4h | whole | 13211 | 1.0219 | 0.8705 | 0.6661* | 0.5374 | 0.4769 | 0.4315 | 0.4012 | 0.3179 | 0.2876 | 0.2498 | 0.2195 |
| SOLUSDT | 4h | first_half | 4157 | 1.1787 | 1.0344 | 0.6976* | 0.5052 | 0.5052 | 0.4571 | 0.3849 | 0.3127 | 0.2887 | 0.2165 | 0.1684 |
| SOLUSDT | 12h | tuning | 2771 | 0.8300 | 0.8300 | 0.7578 | 0.7578* | 0.6857 | 0.6135 | 0.5052 | 0.4691 | 0.4691 | 0.4331 | 0.3248 |
| SOLUSDT | 12h | whole | 4404 | 0.9083 | 0.7947 | 0.7266 | 0.7266* | 0.6358 | 0.5677 | 0.4768 | 0.4314 | 0.4541 | 0.4087 | 0.2952 |
| SOLUSDT | 12h | first_half | 1385 | 0.8664 | 0.7942* | 0.6498 | 0.5776 | 0.5776 | 0.5054 | 0.3610 | 0.3610 | 0.3610 | 0.3610 | 0.2166 |
| SOLUSDT | 1d | tuning | 1384 | 1.3728 | 1.2283 | 0.9393 | 0.7948* | 0.6503 | 0.5780 | 0.4335 | 0.3613 | 0.3613 | 0.2168 | 0.2168 |
| SOLUSDT | 1d | whole | 2201 | 1.2721 | 1.1358 | 0.9541 | 0.8178 | 0.7269* | 0.6361 | 0.5452 | 0.4998 | 0.4543 | 0.3180 | 0.2726 |
| SOLUSDT | 1d | first_half | 692 | 1.3006 | 1.0116 | 0.7225* | 0.5780 | 0.4335 | 0.4335 | 0.4335 | 0.4335 | 0.4335 | 0.2890 | 0.2890 |
| SOLUSDT | 1w | whole | 313 | 1.5974 | 0.6390* | 0.3195 | 0.3195 | 0.3195 | 0.3195 | 0.3195 | 0.3195 | 0.3195 | 0.3195 | 0.3195 |
| NEARUSDT | 5m | tuning | 390143 | 0.9363 | 0.7800* | 0.6610 | 0.5670 | 0.4847 | 0.4291 | 0.3645 | 0.3212 | 0.2860 | 0.2586 | 0.2233 |
| NEARUSDT | 5m | whole | 625152 | 0.9385 | 0.7774* | 0.6568 | 0.5631 | 0.4832 | 0.4207 | 0.3618 | 0.3217 | 0.2846 | 0.2590 | 0.2260 |
| NEARUSDT | 5m | first_half | 195071 | 1.0432 | 0.8684 | 0.7315* | 0.6177 | 0.5357 | 0.4614 | 0.3906 | 0.3389 | 0.3081 | 0.2732 | 0.2379 |
| NEARUSDT | 15m | tuning | 130047 | 0.9627 | 0.8051* | 0.6690 | 0.5659 | 0.4860 | 0.4206 | 0.3583 | 0.3068 | 0.2784 | 0.2368 | 0.2138 |
| NEARUSDT | 15m | whole | 208384 | 0.9511 | 0.7817* | 0.6622 | 0.5595 | 0.4823 | 0.4170 | 0.3551 | 0.3081 | 0.2807 | 0.2438 | 0.2135 |
| NEARUSDT | 15m | first_half | 65023 | 1.0273 | 0.8628 | 0.7182* | 0.5798 | 0.4783 | 0.4122 | 0.3583 | 0.3091 | 0.2891 | 0.2445 | 0.2199 |
| NEARUSDT | 1h | tuning | 32511 | 1.0120 | 0.8120* | 0.6644 | 0.6059 | 0.5444 | 0.4706 | 0.4183 | 0.3599 | 0.3168 | 0.2861 | 0.2645 |
| NEARUSDT | 1h | whole | 52096 | 1.0231 | 0.8408 | 0.6738* | 0.5931 | 0.5221 | 0.4588 | 0.4050 | 0.3474 | 0.3071 | 0.2783 | 0.2591 |
| NEARUSDT | 1h | first_half | 16255 | 1.0397 | 0.8490 | 0.7075* | 0.6398 | 0.5783 | 0.4799 | 0.3999 | 0.3322 | 0.3014 | 0.2645 | 0.2584 |
| NEARUSDT | 4h | tuning | 8127 | 1.0213 | 0.7875* | 0.6645 | 0.6152 | 0.5414 | 0.4307 | 0.3937 | 0.3076 | 0.2707 | 0.2338 | 0.2215 |
| NEARUSDT | 4h | whole | 13024 | 0.9982 | 0.8600 | 0.7141* | 0.6373 | 0.5605 | 0.4837 | 0.4453 | 0.3609 | 0.3302 | 0.2764 | 0.2611 |
| NEARUSDT | 4h | first_half | 4063 | 1.2060 | 0.8614 | 0.7138* | 0.5907 | 0.5907 | 0.4676 | 0.3938 | 0.2953 | 0.2707 | 0.2215 | 0.1969 |
| NEARUSDT | 12h | tuning | 2709 | 1.3289 | 1.0705 | 0.8121 | 0.7383* | 0.6275 | 0.4061 | 0.3322 | 0.3322 | 0.3322 | 0.3322 | 0.2953 |
| NEARUSDT | 12h | whole | 4342 | 1.1976 | 0.9673 | 0.7830* | 0.8291 | 0.6679 | 0.4376 | 0.3915 | 0.3915 | 0.3915 | 0.3685 | 0.3455 |
| NEARUSDT | 12h | first_half | 1354 | 1.4032 | 0.9601 | 0.8124 | 0.7386* | 0.6647 | 0.4431 | 0.3693 | 0.3693 | 0.2954 | 0.2954 | 0.2216 |
| NEARUSDT | 1d | tuning | 1353 | 1.1826 | 0.9608 | 0.8130* | 0.5913 | 0.5174 | 0.4435 | 0.4435 | 0.4435 | 0.2956 | 0.2217 | 0.2217 |
| NEARUSDT | 1d | whole | 2170 | 1.4286 | 1.1060 | 0.7373* | 0.5991 | 0.5530 | 0.4147 | 0.3687 | 0.3687 | 0.3687 | 0.3226 | 0.3226 |
| NEARUSDT | 1d | first_half | 676 | 1.3314 | 1.1834 | 0.7396* | 0.5917 | 0.4438 | 0.2959 | 0.2959 | 0.2959 | 0.2959 | 0.1479 | 0.1479 |
| NEARUSDT | 1w | whole | 309 | 1.2945 | 0.9709 | 0.9709 | 0.9709 | 0.6472 | 0.6472 | 0.6472* | 0.3236 | 0.3236 | 0.3236 | 0.3236 |
| ZECUSDT | 5m | tuning | 463007 | 0.9635 | 0.7795* | 0.6734 | 0.5743 | 0.4942 | 0.4307 | 0.3767 | 0.3343 | 0.2929 | 0.2633 | 0.2333 |
| ZECUSDT | 5m | whole | 698016 | 0.9778 | 0.7922* | 0.6809 | 0.5792 | 0.5029 | 0.4348 | 0.3834 | 0.3390 | 0.2968 | 0.2645 | 0.2367 |
| ZECUSDT | 5m | first_half | 231503 | 0.9952 | 0.8078 | 0.7037* | 0.5918 | 0.5114 | 0.4488 | 0.3922 | 0.3469 | 0.3063 | 0.2721 | 0.2432 |
| ZECUSDT | 15m | tuning | 154335 | 0.9032 | 0.7490* | 0.6376 | 0.5378 | 0.4574 | 0.3939 | 0.3434 | 0.3130 | 0.2721 | 0.2462 | 0.2255 |
| ZECUSDT | 15m | whole | 232672 | 0.9339 | 0.7728* | 0.6468 | 0.5497 | 0.4693 | 0.4040 | 0.3498 | 0.3137 | 0.2729 | 0.2458 | 0.2256 |
| ZECUSDT | 15m | first_half | 77167 | 0.9447 | 0.8060* | 0.6855 | 0.5754 | 0.4950 | 0.4108 | 0.3499 | 0.3266 | 0.2760 | 0.2462 | 0.2294 |
| ZECUSDT | 1h | tuning | 38583 | 1.0290 | 0.8164 | 0.6842* | 0.5728 | 0.4873 | 0.4199 | 0.3654 | 0.3292 | 0.2955 | 0.2695 | 0.2333 |
| ZECUSDT | 1h | whole | 58168 | 1.0212 | 0.8097 | 0.7066* | 0.6051 | 0.5020 | 0.4384 | 0.3782 | 0.3370 | 0.3129 | 0.2871 | 0.2458 |
| ZECUSDT | 1h | first_half | 19291 | 1.0316 | 0.8346 | 0.7154* | 0.6117 | 0.5391 | 0.4769 | 0.3784 | 0.3473 | 0.3318 | 0.3266 | 0.2696 |
| ZECUSDT | 4h | tuning | 9645 | 0.9746 | 0.8191 | 0.7361* | 0.5495 | 0.5184 | 0.4458 | 0.4458 | 0.3110 | 0.2696 | 0.1970 | 0.1866 |
| ZECUSDT | 4h | whole | 14542 | 1.0728 | 0.8596 | 0.7702* | 0.6051 | 0.4814 | 0.4264 | 0.4195 | 0.3301 | 0.2819 | 0.2063 | 0.1994 |
| ZECUSDT | 4h | first_half | 4822 | 1.0369 | 0.8088 | 0.7051* | 0.6014 | 0.5599 | 0.4770 | 0.5392 | 0.3318 | 0.3111 | 0.2074 | 0.2074 |
| ZECUSDT | 12h | tuning | 3215 | 1.2131 | 0.9953 | 0.6843* | 0.5910 | 0.4666 | 0.4044 | 0.4044 | 0.4355 | 0.2799 | 0.2799 | 0.2799 |
| ZECUSDT | 12h | whole | 4848 | 1.1964 | 0.9695 | 0.6807* | 0.5982 | 0.4950 | 0.4332 | 0.4332 | 0.4332 | 0.3094 | 0.3094 | 0.2888 |
| ZECUSDT | 12h | first_half | 1607 | 1.4312 | 1.1201 | 0.8090* | 0.6845 | 0.6223 | 0.4356 | 0.4356 | 0.5600 | 0.3111 | 0.3111 | 0.3111 |
| ZECUSDT | 1d | tuning | 1606 | 1.3699 | 1.0585 | 0.9340 | 0.8095 | 0.8095* | 0.6227 | 0.5604 | 0.4981 | 0.4359 | 0.3736 | 0.2491 |
| ZECUSDT | 1d | whole | 2423 | 1.4858 | 1.0730 | 0.8667 | 0.7842 | 0.7842* | 0.5778 | 0.5365 | 0.4127 | 0.3714 | 0.3302 | 0.2889 |
| ZECUSDT | 1d | first_half | 803 | 1.6189 | 1.3699 | 1.1208 | 0.8717 | 0.8717* | 0.4981 | 0.3736 | 0.3736 | 0.3736 | 0.2491 | 0.3736 |
| ZECUSDT | 1w | whole | 345 | 1.7391 | 1.4493 | 0.8696 | 0.8696 | 0.8696* | 0.2899 | 0.2899 | 0.2899 | 0.2899 | 0.2899 | 0.2899 |
| ENAUSDT | 1h | tuning | 2147 | 0.5123* | 0.4658 | 0.3726 | 0.3726 | 0.3726 | 0.3260 | 0.2795 | 0.2795 | 0.2795 | 0.2329 | 0.2329 |
| ENAUSDT | 1h | whole | 21732 | 1.0215 | 0.8559* | 0.6350 | 0.5338 | 0.4509 | 0.3957 | 0.3589 | 0.3267 | 0.2991 | 0.2761 | 0.2577 |
| ENAUSDT | 1h | first_half | 1073 | 0.1864 | 0.1864 | 0.1864 | 0.1864 | 0.1864* | 0.0932 | 0.0932 | 0.0932 | 0.0932 | 0.0932 | 0.0932 |
| ENAUSDT | 4h | tuning | 536 | 0.9328 | 0.9328 | 0.9328 | 0.7463 | 0.7463 | 0.7463* | 0.5597 | 0.5597 | 0.1866 | 0.1866 | 0.1866 |
| ENAUSDT | 4h | whole | 5433 | 1.0307 | 0.8467 | 0.8467 | 0.7178* | 0.5890 | 0.5154 | 0.4417 | 0.4233 | 0.3129 | 0.2577 | 0.2393 |
| ENAUSDT | 4h | first_half | 268 | 0.3731 | 0.7463 | 0.7463 | 0.7463 | 0.7463 | 0.7463* | 0.3731 | 0.3731 | 0.0000 | 0.0000 | 0.0000 |
| ENAUSDT | 1d | whole | 905 | 1.2155 | 1.1050 | 0.6630* | 0.4420 | 0.3315 | 0.1105 | 0.1105 | 0.2210 | 0.2210 | 0.2210 | 0.1105 |
| PUMPUSDT | 1h | whole | 10601 | 1.1320 | 0.9244 | 0.7075* | 0.6509 | 0.5283 | 0.4717 | 0.3962 | 0.2830 | 0.2547 | 0.3396 | 0.2358 |
| PUMPUSDT | 4h | whole | 2651 | 1.0562 | 0.8299 | 0.7922 | 0.7922* | 0.6035 | 0.4527 | 0.2641 | 0.3018 | 0.1886 | 0.1886 | 0.1509 |
| PUMPUSDT | 1d | whole | 441 | 0.9070 | 0.6803* | 0.4535 | 0.4535 | 0.4535 | 0.4535 | 0.4535 | 0.4535 | 0.2268 | 0.2268 | 0.2268 |
| HYPEUSDT | 1h | whole | 11582 | 1.0016 | 0.8202 | 0.7080* | 0.6217 | 0.4749 | 0.3713 | 0.3454 | 0.3367 | 0.3022 | 0.2677 | 0.2072 |
| HYPEUSDT | 4h | whole | 2896 | 1.0014 | 0.7597* | 0.7251 | 0.6561 | 0.5525 | 0.5180 | 0.5180 | 0.4489 | 0.2072 | 0.2072 | 0.1727 |
| HYPEUSDT | 1d | whole | 482 | 0.8299 | 1.2448 | 1.0373 | 0.8299* | 0.6224 | 0.4149 | 0.4149 | 0.4149 | 0.4149 | 0.2075 | 0.2075 |
| MNTUSDT_BYBIT | 1h | tuning | 6545 | 1.1001 | 0.9320 | 0.8098 | 0.7028* | 0.5653 | 0.4584 | 0.4278 | 0.3972 | 0.3820 | 0.3209 | 0.3056 |
| MNTUSDT_BYBIT | 1h | whole | 26130 | 1.0830 | 0.8840 | 0.7424* | 0.6200 | 0.5166 | 0.4171 | 0.3712 | 0.3444 | 0.3023 | 0.2679 | 0.2411 |
| MNTUSDT_BYBIT | 1h | first_half | 3272 | 1.1308 | 0.9169 | 0.8252* | 0.6724 | 0.5196 | 0.4279 | 0.3973 | 0.3973 | 0.3362 | 0.3362 | 0.3056 |
| MNTUSDT_BYBIT | 4h | tuning | 1636 | 1.2836 | 1.2225 | 0.9169* | 0.5501 | 0.5501 | 0.5501 | 0.4890 | 0.4279 | 0.3667 | 0.3667 | 0.2445 |
| MNTUSDT_BYBIT | 4h | whole | 6533 | 1.0868 | 0.9337 | 0.7500* | 0.6276 | 0.5970 | 0.5051 | 0.4745 | 0.4286 | 0.3980 | 0.3214 | 0.2908 |
| MNTUSDT_BYBIT | 4h | first_half | 818 | 1.3447 | 1.2225 | 1.1002 | 0.4890 | 0.6112 | 0.6112 | 0.6112* | 0.4890 | 0.4890 | 0.4890 | 0.3667 |
| MNTUSDT_BYBIT | 1d | whole | 1088 | 1.4706 | 1.0110 | 0.9191 | 0.7353* | 0.5515 | 0.5515 | 0.4596 | 0.4596 | 0.3676 | 0.2757 | 0.2757 |
| SUIUSDT | 1h | tuning | 10183 | 1.0802 | 0.8642 | 0.8445* | 0.6481 | 0.5401 | 0.4714 | 0.4026 | 0.3732 | 0.3535 | 0.3044 | 0.2455 |
| SUIUSDT | 1h | whole | 29768 | 1.0851 | 0.9137 | 0.7726* | 0.6282 | 0.5308 | 0.4367 | 0.3628 | 0.3359 | 0.3158 | 0.2788 | 0.2486 |
| SUIUSDT | 1h | first_half | 5091 | 0.9821 | 0.7661* | 0.8250 | 0.6482 | 0.5500 | 0.4714 | 0.3929 | 0.3339 | 0.3339 | 0.2554 | 0.1964 |
| SUIUSDT | 4h | tuning | 2545 | 1.1002 | 0.7466 | 0.7859 | 0.7466* | 0.6287 | 0.5894 | 0.3929 | 0.3929 | 0.3929 | 0.2750 | 0.2750 |
| SUIUSDT | 4h | whole | 7442 | 0.9944 | 0.7794* | 0.7928 | 0.6987 | 0.5778 | 0.5106 | 0.4031 | 0.3762 | 0.3628 | 0.3091 | 0.3091 |
| SUIUSDT | 4h | first_half | 1272 | 1.2579 | 0.7862 | 0.7075 | 0.7862* | 0.6289 | 0.5503 | 0.3931 | 0.3931 | 0.3931 | 0.3145 | 0.3145 |
| SUIUSDT | 1d | tuning | 423 | 1.4184 | 0.9456 | 0.9456 | 0.9456* | 0.4728 | 0.4728 | 0.2364 | 0.2364 | 0.2364 | 0.2364 | 0.2364 |
| SUIUSDT | 1d | whole | 1240 | 1.3710 | 0.8871 | 0.8871 | 0.9677 | 0.7258* | 0.3226 | 0.2419 | 0.2419 | 0.2419 | 0.2419 | 0.2419 |
| SUIUSDT | 1d | first_half | 211 | 1.8957 | 1.4218 | 1.4218 | 1.4218* | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |
| LTCUSDT | 1h | tuning | 39231 | 0.9329 | 0.7698* | 0.6653 | 0.5914 | 0.5022 | 0.4486 | 0.3671 | 0.3059 | 0.2702 | 0.2473 | 0.2039 |
| LTCUSDT | 1h | whole | 58816 | 0.9555 | 0.7906* | 0.7005 | 0.5951 | 0.5033 | 0.4506 | 0.3689 | 0.3111 | 0.2788 | 0.2550 | 0.2142 |
| LTCUSDT | 1h | first_half | 19615 | 0.9737 | 0.8310 | 0.6984* | 0.5914 | 0.5506 | 0.4639 | 0.3773 | 0.2957 | 0.2600 | 0.2498 | 0.1937 |
| LTCUSDT | 4h | tuning | 9807 | 1.0707 | 0.9177 | 0.7342* | 0.4996 | 0.4589 | 0.4589 | 0.4181 | 0.3263 | 0.3161 | 0.3059 | 0.2855 |
| LTCUSDT | 4h | whole | 14704 | 1.0949 | 0.9317 | 0.7413* | 0.4965 | 0.4625 | 0.4421 | 0.4353 | 0.3468 | 0.3196 | 0.2992 | 0.2856 |
| LTCUSDT | 4h | first_half | 4903 | 1.1218 | 0.9586 | 0.8158* | 0.5303 | 0.4895 | 0.4895 | 0.4487 | 0.4079 | 0.3875 | 0.3671 | 0.3263 |
| LTCUSDT | 1d | tuning | 1633 | 1.2247 | 1.0410 | 0.9186 | 0.7348* | 0.5511 | 0.4287 | 0.4287 | 0.3674 | 0.2449 | 0.1225 | 0.1225 |
| LTCUSDT | 1d | whole | 2450 | 1.2653 | 1.0204 | 0.8980 | 0.7755* | 0.5714 | 0.5306 | 0.5306 | 0.4490 | 0.3673 | 0.2449 | 0.2449 |
| LTCUSDT | 1d | first_half | 816 | 1.5931 | 1.3480 | 1.1029 | 0.6127* | 0.2451 | 0.2451 | 0.2451 | 0.3676 | 0.1225 | 0.1225 | 0.1225 |
| XMRUSDT | 1h | tuning | 38631 | 0.7585* | 0.6394 | 0.5436 | 0.4452 | 0.3572 | 0.3210 | 0.2873 | 0.2382 | 0.2174 | 0.1993 | 0.1916 |
| XMRUSDT | 1h | whole | 58216 | 0.7472* | 0.6390 | 0.5480 | 0.4535 | 0.3745 | 0.3315 | 0.2972 | 0.2491 | 0.2302 | 0.2061 | 0.1907 |
| XMRUSDT | 1h | first_half | 19315 | 0.8284 | 0.7093* | 0.5799 | 0.4867 | 0.4142 | 0.3572 | 0.3003 | 0.2382 | 0.2174 | 0.1967 | 0.1864 |
| XMRUSDT | 4h | tuning | 9657 | 0.9113 | 0.7559* | 0.6627 | 0.5488 | 0.4763 | 0.4453 | 0.2899 | 0.0932 | 0.0828 | 0.0828 | 0.0828 |
| XMRUSDT | 4h | whole | 14554 | 0.7833* | 0.6665 | 0.5703 | 0.4810 | 0.4260 | 0.3916 | 0.2748 | 0.1237 | 0.0962 | 0.0893 | 0.0893 |
| XMRUSDT | 4h | first_half | 4828 | 1.0771 | 0.8699 | 0.7249* | 0.6214 | 0.5178 | 0.4764 | 0.1657 | 0.1657 | 0.1450 | 0.1450 | 0.1450 |
| XMRUSDT | 1d | tuning | 1608 | 0.6219* | 0.4975 | 0.4975 | 0.3731 | 0.3731 | 0.2488 | 0.1244 | 0.1244 | 0.1244 | 0.1244 | 0.2488 |
| XMRUSDT | 1d | whole | 2425 | 0.6186* | 0.5361 | 0.4948 | 0.3299 | 0.3299 | 0.2474 | 0.1237 | 0.1237 | 0.1237 | 0.0825 | 0.1649 |
| XMRUSDT | 1d | first_half | 804 | 1.1194 | 0.8706 | 0.8706* | 0.6219 | 0.6219 | 0.3731 | 0.1244 | 0.1244 | 0.1244 | 0.1244 | 0.1244 |
| BNBUSDT | 1h | tuning | 38463 | 0.9464 | 0.8060* | 0.6708 | 0.5824 | 0.5200 | 0.4238 | 0.3692 | 0.3094 | 0.2704 | 0.2158 | 0.1924 |
| BNBUSDT | 1h | whole | 58048 | 1.0112 | 0.8372 | 0.6874* | 0.5771 | 0.5116 | 0.4341 | 0.3790 | 0.3170 | 0.2774 | 0.2412 | 0.2136 |
| BNBUSDT | 1h | first_half | 19231 | 1.0452 | 0.8892 | 0.7228* | 0.6396 | 0.5772 | 0.4524 | 0.3952 | 0.3224 | 0.2912 | 0.2236 | 0.2028 |
| BNBUSDT | 4h | tuning | 9615 | 1.0192 | 0.9048 | 0.6968* | 0.5408 | 0.4264 | 0.3432 | 0.3120 | 0.2600 | 0.2080 | 0.1768 | 0.1664 |
| BNBUSDT | 4h | whole | 14512 | 1.0061 | 0.8200* | 0.6477 | 0.5375 | 0.4686 | 0.3928 | 0.3377 | 0.2963 | 0.2619 | 0.2343 | 0.2136 |
| BNBUSDT | 4h | first_half | 4807 | 1.1234 | 1.0818 | 0.8321* | 0.6449 | 0.4785 | 0.4369 | 0.3953 | 0.3120 | 0.2496 | 0.1872 | 0.1872 |
| BNBUSDT | 1d | tuning | 1601 | 0.9994 | 0.8745* | 0.6246 | 0.4372 | 0.2498 | 0.2498 | 0.2498 | 0.2498 | 0.2498 | 0.2498 | 0.2498 |
| BNBUSDT | 1d | whole | 2418 | 1.1166 | 0.9512 | 0.7444* | 0.5790 | 0.4136 | 0.3309 | 0.3309 | 0.2895 | 0.2895 | 0.2481 | 0.2068 |
| BNBUSDT | 1d | first_half | 800 | 1.3750 | 1.2500 | 0.7500* | 0.5000 | 0.3750 | 0.3750 | 0.2500 | 0.2500 | 0.2500 | 0.2500 | 0.2500 |
| UNIUSDT | 1h | tuning | 33160 | 1.0283 | 0.8685 | 0.7027* | 0.6092 | 0.4493 | 0.3739 | 0.3317 | 0.2563 | 0.2352 | 0.2171 | 0.1930 |
| UNIUSDT | 1h | whole | 52745 | 1.0333 | 0.8607 | 0.7110* | 0.6067 | 0.4588 | 0.3944 | 0.3451 | 0.2749 | 0.2559 | 0.2275 | 0.1972 |
| UNIUSDT | 1h | first_half | 16580 | 1.0736 | 0.9168 | 0.7419* | 0.6212 | 0.3739 | 0.3076 | 0.2835 | 0.2111 | 0.1809 | 0.1749 | 0.1628 |
| UNIUSDT | 4h | tuning | 8290 | 1.0374 | 0.8444 | 0.6876* | 0.6152 | 0.4825 | 0.4343 | 0.3981 | 0.3257 | 0.2895 | 0.2895 | 0.2654 |
| UNIUSDT | 4h | whole | 13187 | 1.0844 | 0.8417 | 0.7052* | 0.6218 | 0.5308 | 0.4702 | 0.4171 | 0.3564 | 0.3261 | 0.3185 | 0.2882 |
| UNIUSDT | 4h | first_half | 4145 | 0.8444 | 0.6996* | 0.6273 | 0.5308 | 0.4343 | 0.4101 | 0.3860 | 0.3136 | 0.2895 | 0.2895 | 0.2413 |
| UNIUSDT | 1d | tuning | 1380 | 1.4493 | 1.0145 | 0.6522 | 0.6522* | 0.5797 | 0.5072 | 0.5072 | 0.2899 | 0.2899 | 0.2899 | 0.2899 |
| UNIUSDT | 1d | whole | 2197 | 1.5020 | 1.1834 | 0.5917 | 0.5917* | 0.5007 | 0.4096 | 0.4096 | 0.2276 | 0.2276 | 0.2276 | 0.2276 |
| UNIUSDT | 1d | first_half | 690 | 1.4493 | 1.0145 | 0.7246 | 0.7246* | 0.5797 | 0.4348 | 0.4348 | 0.2899 | 0.2899 | 0.2899 | 0.2899 |
| 1000PEPEUSDT | 1h | tuning | 10135 | 0.8189 | 0.7499* | 0.6611 | 0.5525 | 0.4637 | 0.3947 | 0.3552 | 0.3256 | 0.2861 | 0.2664 | 0.2269 |
| 1000PEPEUSDT | 1h | whole | 29720 | 0.9152 | 0.7537* | 0.6023 | 0.5249 | 0.4273 | 0.3869 | 0.3499 | 0.3096 | 0.2725 | 0.2490 | 0.2153 |
| 1000PEPEUSDT | 1h | first_half | 5067 | 0.7302 | 0.7302* | 0.6513 | 0.4934 | 0.4144 | 0.3947 | 0.3158 | 0.2960 | 0.2763 | 0.2763 | 0.2368 |
| 1000PEPEUSDT | 4h | tuning | 2533 | 1.0659 | 0.7896 | 0.7106* | 0.4737 | 0.5132 | 0.3553 | 0.3553 | 0.3158 | 0.2764 | 0.3158 | 0.2764 |
| 1000PEPEUSDT | 4h | whole | 7430 | 1.0094 | 0.7537* | 0.6864 | 0.5787 | 0.5249 | 0.4307 | 0.4038 | 0.3903 | 0.3365 | 0.3230 | 0.2961 |
| 1000PEPEUSDT | 4h | first_half | 1266 | 1.1058 | 0.7899* | 0.6319 | 0.4739 | 0.4739 | 0.3160 | 0.3160 | 0.3160 | 0.2370 | 0.2370 | 0.2370 |
| 1000PEPEUSDT | 1d | tuning | 421 | 1.6627 | 1.1876 | 0.9501 | 0.7126 | 0.7126 | 0.7126 | 0.7126* | 0.4751 | 0.2375 | 0.2375 | 0.2375 |
| 1000PEPEUSDT | 1d | whole | 1238 | 1.4540 | 1.0501 | 0.9693 | 0.8078* | 0.6462 | 0.5654 | 0.5654 | 0.4039 | 0.3231 | 0.3231 | 0.2423 |
| 1000PEPEUSDT | 1d | first_half | 210 | 1.4286 | 0.9524 | 0.9524* | 0.4762 | 0.4762 | 0.4762 | 0.4762 | 0.4762 | 0.0000 | 0.0000 | 0.0000 |
| DOGEUSDT | 1h | tuning | 34838 | 0.8755 | 0.6975* | 0.5167 | 0.4736 | 0.4277 | 0.3445 | 0.3071 | 0.2870 | 0.2612 | 0.2239 | 0.2153 |
| DOGEUSDT | 1h | whole | 54423 | 0.9151 | 0.7331* | 0.5788 | 0.5200 | 0.4594 | 0.3895 | 0.3344 | 0.3087 | 0.2775 | 0.2425 | 0.2315 |
| DOGEUSDT | 1h | first_half | 17419 | 0.8439 | 0.6774* | 0.4937 | 0.4708 | 0.4420 | 0.3445 | 0.2985 | 0.2698 | 0.2583 | 0.2354 | 0.2124 |
| DOGEUSDT | 4h | tuning | 8709 | 0.9416 | 0.5626* | 0.4363 | 0.3674 | 0.3560 | 0.4134 | 0.2756 | 0.2641 | 0.2296 | 0.2411 | 0.2411 |
| DOGEUSDT | 4h | whole | 13606 | 0.9702 | 0.6762* | 0.5365 | 0.4630 | 0.4263 | 0.4557 | 0.3381 | 0.3013 | 0.2719 | 0.2646 | 0.2572 |
| DOGEUSDT | 4h | first_half | 4354 | 0.8957* | 0.4364 | 0.4134 | 0.3904 | 0.3675 | 0.4364 | 0.3215 | 0.3215 | 0.2986 | 0.2986 | 0.3215 |
| DOGEUSDT | 1d | tuning | 1450 | 1.4483 | 0.9655 | 0.8276 | 0.7586* | 0.6897 | 0.5517 | 0.4828 | 0.4138 | 0.3448 | 0.2759 | 0.0690 |
| DOGEUSDT | 1d | whole | 2267 | 1.3674 | 0.8822 | 0.7940 | 0.7499* | 0.6176 | 0.5293 | 0.4411 | 0.3970 | 0.3529 | 0.3088 | 0.1323 |
| DOGEUSDT | 1d | first_half | 725 | 1.2414 | 0.8276 | 0.8276 | 0.8276 | 0.8276 | 0.6897* | 0.4138 | 0.2759 | 0.2759 | 0.2759 | 0.0000 |
| 1000BONKUSDT | 1h | tuning | 5313 | 1.1669 | 0.8093 | 0.7905* | 0.6964 | 0.6588 | 0.5082 | 0.4141 | 0.3388 | 0.2823 | 0.1882 | 0.1694 |
| 1000BONKUSDT | 1h | whole | 24898 | 0.9639 | 0.7591* | 0.6989 | 0.6025 | 0.5342 | 0.4418 | 0.3615 | 0.3414 | 0.2892 | 0.2651 | 0.2370 |
| 1000BONKUSDT | 1h | first_half | 2656 | 1.2425 | 0.7907 | 0.7530 | 0.7530 | 0.7530* | 0.4895 | 0.4518 | 0.3765 | 0.3012 | 0.1506 | 0.1506 |
| 1000BONKUSDT | 4h | tuning | 1328 | 1.0542 | 0.8283 | 0.6777* | 0.3765 | 0.3765 | 0.3012 | 0.3012 | 0.3012 | 0.3012 | 0.3012 | 0.3012 |
| 1000BONKUSDT | 4h | whole | 6225 | 0.8514 | 0.8514* | 0.5622 | 0.4659 | 0.4177 | 0.3534 | 0.3213 | 0.3052 | 0.2731 | 0.2249 | 0.2249 |
| 1000BONKUSDT | 4h | first_half | 664 | 1.5060 | 1.2048 | 0.9036* | 0.3012 | 0.3012 | 0.1506 | 0.1506 | 0.1506 | 0.1506 | 0.1506 | 0.1506 |
| 1000BONKUSDT | 1d | whole | 1037 | 1.3500 | 1.0608 | 0.6750* | 0.4822 | 0.4822 | 0.4822 | 0.4822 | 0.4822 | 0.4822 | 0.2893 | 0.2893 |

grid file: SCALE_GRID.parquet · 2035 rows · content sha256 d2b5ec141516d7bea1fe4ab296c97087233d7daa40044eebeeda730604ea2c2b
