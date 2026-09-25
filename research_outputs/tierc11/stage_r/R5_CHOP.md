as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE R · R5 CHOP

## R5 · THE CHOP TABLE [L-R.7] — v6 outcomes by 4h / 12h state x %-of-range decile at entry — Tier-E (printed first in §0)

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

SR-8 R5 BUCKETS [L-R.7]: IN_RANGE entries by pct-of-range (unclamped) decile [0,10) .. [90,100), '<0', '>=100'; not-in-range entries by state (NONE, BULL_EXP, BEAR_EXP); '__ALL__'. n, E[net R] (mean), P(win) (share net R > 0), sum R.

SCALE-IN-SAMPLE [L-R.2, AM-4]: a calibrated-scale range read at an instant <= the era cut (2024-06-30T23:59:59Z) is structurally IN-SAMPLE (the tuning pick saw those bars; a whole-tape fallback pick is in-sample at every instant; frozen 3.0 never is). Every row carries `lenses_read` (the lenses the cell consumes: L, and L+1 for a coincidence cell), their `pick_window` and `stability_changed_members` (first-half-of-tuning pick != tuning pick), `n_scale_in_sample` / `n_stability_changed` (the cell's entries whose read is in-sample / rides a stability-changed pick, on ANY consumed lens), and the HOLDOUT slice (entry close after the cut: n_holdout, mean_net_r_holdout, p_win_holdout, sum_net_r_holdout) — the causal slice of a tuning pick, printed beside every cell.

- v6 · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- v6 · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- v6 · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- v6 · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77

### 4h · calibrated (the scale of record — IN-SAMPLE on the tuning-era entries: 123 of 200; stability-changed 4h: NEARUSDT on 40 entries; the HOLDOUT slice beside is the causal one)

| bucket | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|
| [0,10) | 8 | -0.3976 | 0.2500 | -3.1804 | 6 | 2 | 2 | -0.6125 | 0.0000 | -1.2250 |
| [10,20) | 11 | -0.3649 | 0.1818 | -4.0137 | 6 | 2 | 5 | -0.3175 | 0.2000 | -1.5873 |
| [20,30) | 22 | 0.3058 | 0.3636 | 6.7278 | 12 | 5 | 10 | -0.2001 | 0.3000 | -2.0007 |
| [30,40) | 17 | 0.6809 | 0.4118 | 11.5760 | 10 | 3 | 7 | 2.1044 | 0.5714 | 14.7309 |
| [40,50) | 18 | 0.2844 | 0.3333 | 5.1197 | 11 | 4 | 7 | 0.3102 | 0.2857 | 2.1714 |
| [50,60) | 14 | -0.0411 | 0.3571 | -0.5758 | 9 | 1 | 5 | -0.5598 | 0.2000 | -2.7990 |
| [60,70) | 16 | -0.2869 | 0.3125 | -4.5909 | 10 | 6 | 6 | -0.6654 | 0.1667 | -3.9924 |
| [70,80) | 14 | 0.6588 | 0.3571 | 9.2226 | 9 | 3 | 5 | 1.9935 | 0.6000 | 9.9673 |
| [80,90) | 12 | 0.0333 | 0.3333 | 0.3997 | 7 | 2 | 5 | 1.1243 | 0.6000 | 5.6213 |
| [90,100) | 5 | 0.4527 | 0.4000 | 2.2635 | 5 | 1 | 0 | — | — | — |
| <0 | 2 | 0.3746 | 0.5000 | 0.7492 | 2 | 2 | 0 | — | — | — |
| >=100 | 2 | -0.0282 | 0.5000 | -0.0564 | 1 | 0 | 1 | 1.0160 | 1.0000 | 1.0160 |
| not-in-range:NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:BULL_EXP | 32 | 0.7114 | 0.4062 | 22.7648 | 20 | 1 | 12 | 2.1614 | 0.5000 | 25.9366 |
| not-in-range:BEAR_EXP | 27 | -0.2074 | 0.2963 | -5.5986 | 15 | 8 | 12 | -0.4756 | 0.2500 | -5.7078 |
| __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 40 | 77 | 0.5472 | 0.3636 | 42.1314 |

### 12h · calibrated (the scale of record — IN-SAMPLE on the tuning-era entries: 123 of 200; stability-changed 12h: BTCUSDT,ETHUSDT,SOLUSDT on 123 entries; the HOLDOUT slice beside is the causal one)

| bucket | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|
| [0,10) | 4 | -0.4013 | 0.2500 | -1.6052 | 4 | 1 | 0 | — | — | — |
| [10,20) | 11 | 0.1524 | 0.2727 | 1.6767 | 4 | 4 | 7 | -0.2362 | 0.2857 | -1.6535 |
| [20,30) | 21 | -0.4041 | 0.1905 | -8.4857 | 13 | 16 | 8 | -0.6005 | 0.1250 | -4.8037 |
| [30,40) | 13 | 0.7682 | 0.3077 | 9.9865 | 7 | 10 | 6 | 1.8134 | 0.3333 | 10.8806 |
| [40,50) | 13 | 0.1942 | 0.3077 | 2.5249 | 3 | 12 | 10 | 0.4547 | 0.4000 | 4.5471 |
| [50,60) | 13 | 0.3439 | 0.3846 | 4.4703 | 8 | 9 | 5 | -0.5625 | 0.2000 | -2.8127 |
| [60,70) | 12 | -0.1437 | 0.4167 | -1.7247 | 5 | 8 | 7 | -0.4116 | 0.2857 | -2.8810 |
| [70,80) | 11 | 0.3474 | 0.4545 | 3.8210 | 7 | 9 | 4 | -0.1620 | 0.5000 | -0.6481 |
| [80,90) | 3 | 0.5428 | 0.3333 | 1.6285 | 2 | 3 | 1 | 3.8512 | 1.0000 | 3.8512 |
| [90,100) | 2 | 1.0175 | 0.5000 | 2.0349 | 1 | 2 | 1 | 2.7072 | 1.0000 | 2.7072 |
| <0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| >=100 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:BULL_EXP | 58 | 0.4190 | 0.3621 | 24.3003 | 45 | 32 | 13 | 2.2197 | 0.3846 | 28.8562 |
| not-in-range:BEAR_EXP | 39 | 0.0559 | 0.3846 | 2.1801 | 24 | 17 | 15 | 0.2725 | 0.4667 | 4.0882 |
| __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 123 | 77 | 0.5472 | 0.3636 | 42.1314 |

### 4h · frozen3.0 (the fully causal twin)

| bucket | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|
| [0,10) | 8 | -0.1409 | 0.3750 | -1.1269 | 0 | 0 | 2 | 0.4039 | 0.5000 | 0.8078 |
| [10,20) | 14 | -0.3712 | 0.2143 | -5.1963 | 0 | 0 | 7 | -0.2439 | 0.2857 | -1.7070 |
| [20,30) | 11 | 0.1543 | 0.3636 | 1.6976 | 0 | 0 | 5 | 0.1232 | 0.4000 | 0.6158 |
| [30,40) | 13 | 0.4039 | 0.3077 | 5.2513 | 0 | 0 | 6 | 1.5910 | 0.5000 | 9.5460 |
| [40,50) | 9 | 1.2940 | 0.4444 | 11.6462 | 0 | 0 | 5 | 1.3660 | 0.4000 | 6.8301 |
| [50,60) | 11 | 0.0095 | 0.3636 | 0.1047 | 0 | 0 | 4 | -0.5002 | 0.2500 | -2.0010 |
| [60,70) | 7 | -0.3565 | 0.1429 | -2.4952 | 0 | 0 | 4 | -1.0321 | 0.0000 | -4.1285 |
| [70,80) | 7 | 0.7039 | 0.4286 | 4.9270 | 0 | 0 | 5 | 0.2211 | 0.4000 | 1.1053 |
| [80,90) | 8 | 0.7623 | 0.6250 | 6.0988 | 0 | 0 | 4 | 1.6602 | 0.7500 | 6.6410 |
| [90,100) | 4 | 1.2871 | 0.7500 | 5.1483 | 0 | 0 | 1 | 1.0160 | 1.0000 | 1.0160 |
| <0 | 1 | -0.1998 | 0.0000 | -0.1998 | 0 | 0 | 1 | -0.1998 | 0.0000 | -0.1998 |
| >=100 | 1 | 1.0934 | 1.0000 | 1.0934 | 0 | 0 | 1 | 1.0934 | 1.0000 | 1.0934 |
| not-in-range:NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:BULL_EXP | 66 | 0.2198 | 0.2879 | 14.5096 | 0 | 0 | 19 | 1.4696 | 0.3158 | 27.9220 |
| not-in-range:BEAR_EXP | 40 | -0.0163 | 0.3750 | -0.6510 | 0 | 0 | 13 | -0.4161 | 0.3077 | -5.4095 |
| __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 |

### 12h · frozen3.0 (the fully causal twin)

| bucket | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|
| [0,10) | 11 | -0.1274 | 0.3636 | -1.4011 | 0 | 0 | 3 | 0.3009 | 0.6667 | 0.9027 |
| [10,20) | 12 | 0.5312 | 0.4167 | 6.3749 | 0 | 0 | 8 | 0.1917 | 0.3750 | 1.5334 |
| [20,30) | 8 | 0.3507 | 0.1250 | 2.8059 | 0 | 0 | 6 | 0.8107 | 0.1667 | 4.8640 |
| [30,40) | 7 | -0.6851 | 0.1429 | -4.7957 | 0 | 0 | 1 | -1.0265 | 0.0000 | -1.0265 |
| [40,50) | 6 | 1.0391 | 0.5000 | 6.2346 | 0 | 0 | 4 | 1.5971 | 0.5000 | 6.3885 |
| [50,60) | 5 | -0.5414 | 0.2000 | -2.7069 | 0 | 0 | 4 | -0.4319 | 0.2500 | -1.7275 |
| [60,70) | 8 | 0.3768 | 0.5000 | 3.0141 | 0 | 0 | 2 | -0.0072 | 0.5000 | -0.0144 |
| [70,80) | 7 | -0.3825 | 0.2857 | -2.6777 | 0 | 0 | 3 | -1.0612 | 0.0000 | -3.1836 |
| [80,90) | 9 | 0.6570 | 0.5556 | 5.9133 | 0 | 0 | 5 | 0.8169 | 0.6000 | 4.0847 |
| [90,100) | 1 | -0.6723 | 0.0000 | -0.6723 | 0 | 0 | 0 | — | — | — |
| <0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| >=100 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| not-in-range:BULL_EXP | 76 | 0.4594 | 0.3816 | 34.9134 | 0 | 0 | 24 | 1.7344 | 0.5417 | 41.6250 |
| not-in-range:BEAR_EXP | 50 | -0.1239 | 0.2800 | -6.1949 | 0 | 0 | 17 | -0.6656 | 0.1176 | -11.3149 |
| __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 |

### R5 BY DIRECTION [SR-16; the trading review D-2] — collared Tier-E rows that DECIDE NOTHING

L-R.7's chop table above is direction-blind as frozen and is printed unchanged. A BULL_EXP / BEAR_EXP row there mixes longs riding the expansion with shorts fading it, so it can read as a market state when the effect is alignment. The rows below read the SAME v6 entries (R5_CHOP_DIRECTION.parquet) by alignment and by direction-adjusted pct-of-range. They gate nothing and are not results.

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

SR-16 R5 BY DIRECTION [the trading review D-2, research_outputs/tierc11/review/FINAL_REVIEW_2026-09-25.json: L-R.7's chop table is direction-blind as frozen, so a BULL_EXP / BEAR_EXP row mixes longs riding the expansion with shorts fading it — an alignment effect that reads as a market state]: BESIDE the R5 rows, which stay unchanged, R5_CHOP_DIRECTION prints collared Tier-E rows that DECIDE NOTHING, per scale (calibrated, frozen3.0) x lens {4h, 12h}, on the same v6 entries (direction = the book's own +1 long / -1 short). (i) 'alignment': the lens state at entry split EXP_ALIGNED (BULL_EXP for a long, BEAR_EXP for a short), EXP_COUNTER (the other expansion), IN_RANGE, NONE, and '__ALL__'. (ii) 'pct_dir_adj': the IN_RANGE entries by DIRECTION-ADJUSTED pct-of-range, unclamped (pct for a long, 100 - pct for a short, so 100 is the boundary the trade must break and 0 the one behind it), in terciles [0,33.33), [33.33,66.67), [66.67,100) (exact cuts 100/3 and 200/3) plus '<0' and '>=100'. This is SR-8's half-open law, one law for both sides. The commission's text ('[66.67,100]' beside '>=100') overlaps only at exactly 100, which this law sends to '>=100' as SR-8 does; R5_CHOP.md prints how many entries sit on a cut. Columns: n (n_long / n_short beside), E[net R], P(win), sum R, and SR-12's honesty labels with the holdout slice. Partitions (the build HALTs otherwise): EXP_ALIGNED + EXP_COUNTER == R5's not-in-range BULL_EXP + BEAR_EXP; NONE == R5's not-in-range:NONE; IN_RANGE == R5's deciles + '<0' + '>=100' == the five pct_dir_adj buckets; '__ALL__' == R5's.

Entries on a cut (the tercile text read another way would move them) — IN_RANGE entries whose adjusted pct is exactly 0, 100/3, 200/3 or 100, or lies between a printed label and its exact cut ([33.33, 100/3) or [200/3, 66.67)): calibrated|4h 0 on a cut, 0 between, of 141 in range · calibrated|12h 0 on a cut, 0 between, of 103 in range · frozen3.0|4h 0 on a cut, 0 between, of 94 in range · frozen3.0|12h 0 on a cut, 0 between, of 74 in range.

The honesty labels (lenses_read, pick_window, stability-changed members) are the R5 rows' own for the same lens; every row carries them and the HOLDOUT slice.

#### 4h · calibrated · alignment (the scale of record; IN-SAMPLE on the tuning-era entries, the HOLDOUT slice beside is the causal one)

Law: the lens state at entry by the trade's direction: EXP_ALIGNED = BULL_EXP for a long / BEAR_EXP for a short; EXP_COUNTER = the other expansion; IN_RANGE / NONE as read [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXP_ALIGNED | 47 | 24 | 23 | 0.4913 | 0.3830 | 23.0934 | 30 | 6 | 17 | 1.3416 | 0.4118 | 22.8067 |
| EXP_COUNTER | 12 | 4 | 8 | -0.4939 | 0.2500 | -5.9272 | 5 | 3 | 7 | -0.3683 | 0.2857 | -2.5779 |
| IN_RANGE | 141 | 69 | 72 | 0.1677 | 0.3404 | 23.6414 | 88 | 31 | 53 | 0.4133 | 0.3585 | 21.9025 |
| NONE | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| __ALL__ | 200 | 97 | 103 | 0.2040 | 0.3450 | 40.8076 | 123 | 40 | 77 | 0.5472 | 0.3636 | 42.1314 |

#### 4h · calibrated · pct_dir_adj (the scale of record; IN-SAMPLE on the tuning-era entries, the HOLDOUT slice beside is the causal one)

Law: IN_RANGE entries by direction-adjusted pct-of-range (pct for a long, 100 - pct for a short; 100 = the boundary the trade must break): [0,100/3), [100/3,200/3), [200/3,100), '<0', '>=100' [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| [0,33.33) | 1 | 0 | 1 | -1.0448 | 0.0000 | -1.0448 | 1 | 1 | 0 | — | — | — |
| [33.33,66.67) | 55 | 31 | 24 | 0.3537 | 0.4000 | 19.4536 | 34 | 11 | 21 | 0.5780 | 0.3333 | 12.1382 |
| [66.67,100) | 81 | 36 | 45 | 0.0560 | 0.2963 | 4.5397 | 50 | 17 | 31 | 0.2822 | 0.3548 | 8.7483 |
| >=100 | 4 | 2 | 2 | 0.1732 | 0.5000 | 0.6929 | 3 | 2 | 1 | 1.0160 | 1.0000 | 1.0160 |

#### 12h · calibrated · alignment (the scale of record; IN-SAMPLE on the tuning-era entries, the HOLDOUT slice beside is the causal one)

Law: the lens state at entry by the trade's direction: EXP_ALIGNED = BULL_EXP for a long / BEAR_EXP for a short; EXP_COUNTER = the other expansion; IN_RANGE / NONE as read [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXP_ALIGNED | 87 | 53 | 34 | 0.2925 | 0.3793 | 25.4447 | 60 | 45 | 27 | 1.0292 | 0.4074 | 27.7878 |
| EXP_COUNTER | 10 | 5 | 5 | 0.1036 | 0.3000 | 1.0358 | 9 | 4 | 1 | 5.1566 | 1.0000 | 5.1566 |
| IN_RANGE | 103 | 39 | 64 | 0.1391 | 0.3204 | 14.3271 | 54 | 74 | 49 | 0.1875 | 0.3265 | 9.1870 |
| NONE | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| __ALL__ | 200 | 97 | 103 | 0.2040 | 0.3450 | 40.8076 | 123 | 123 | 77 | 0.5472 | 0.3636 | 42.1314 |

#### 12h · calibrated · pct_dir_adj (the scale of record; IN-SAMPLE on the tuning-era entries, the HOLDOUT slice beside is the causal one)

Law: IN_RANGE entries by direction-adjusted pct-of-range (pct for a long, 100 - pct for a short; 100 = the boundary the trade must break): [0,100/3), [100/3,200/3), [200/3,100), '<0', '>=100' [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| [0,33.33) | 2 | 1 | 1 | -0.2099 | 0.5000 | -0.4199 | 1 | 2 | 1 | -1.0795 | 0.0000 | -1.0795 |
| [33.33,66.67) | 44 | 18 | 26 | 0.3250 | 0.3409 | 14.2986 | 21 | 34 | 23 | 0.4306 | 0.3043 | 9.9040 |
| [66.67,100) | 57 | 20 | 37 | 0.0079 | 0.2982 | 0.4484 | 32 | 38 | 25 | 0.0145 | 0.3600 | 0.3625 |
| >=100 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |

#### 4h · frozen3.0 · alignment (the fully causal twin)

Law: the lens state at entry by the trade's direction: EXP_ALIGNED = BULL_EXP for a long / BEAR_EXP for a short; EXP_COUNTER = the other expansion; IN_RANGE / NONE as read [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXP_ALIGNED | 92 | 55 | 37 | 0.2380 | 0.3370 | 21.8943 | 0 | 0 | 27 | 0.9376 | 0.3333 | 25.3144 |
| EXP_COUNTER | 14 | 3 | 11 | -0.5740 | 0.2143 | -8.0357 | 0 | 0 | 5 | -0.5604 | 0.2000 | -2.8019 |
| IN_RANGE | 94 | 39 | 55 | 0.2867 | 0.3723 | 26.9490 | 0 | 0 | 45 | 0.4360 | 0.4000 | 19.6189 |
| NONE | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| __ALL__ | 200 | 97 | 103 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 |

#### 4h · frozen3.0 · pct_dir_adj (the fully causal twin)

Law: IN_RANGE entries by direction-adjusted pct-of-range (pct for a long, 100 - pct for a short; 100 = the boundary the trade must break): [0,100/3), [100/3,200/3), [200/3,100), '<0', '>=100' [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| [0,33.33) | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| [33.33,66.67) | 36 | 17 | 19 | 0.4936 | 0.3611 | 17.7702 | 0 | 0 | 16 | 0.7950 | 0.3750 | 12.7204 |
| [66.67,100) | 56 | 21 | 35 | 0.1480 | 0.3750 | 8.2853 | 0 | 0 | 27 | 0.2224 | 0.4074 | 6.0050 |
| >=100 | 2 | 1 | 1 | 0.4468 | 0.5000 | 0.8935 | 0 | 0 | 2 | 0.4468 | 0.5000 | 0.8935 |

#### 12h · frozen3.0 · alignment (the fully causal twin)

Law: the lens state at entry by the trade's direction: EXP_ALIGNED = BULL_EXP for a long / BEAR_EXP for a short; EXP_COUNTER = the other expansion; IN_RANGE / NONE as read [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| EXP_ALIGNED | 108 | 62 | 46 | 0.1928 | 0.3056 | 20.8251 | 0 | 0 | 35 | 0.6848 | 0.2857 | 23.9673 |
| EXP_COUNTER | 18 | 4 | 14 | 0.4385 | 0.5556 | 7.8933 | 0 | 0 | 6 | 1.0571 | 0.8333 | 6.3427 |
| IN_RANGE | 74 | 31 | 43 | 0.1634 | 0.3514 | 12.0891 | 0 | 0 | 36 | 0.3284 | 0.3611 | 11.8213 |
| NONE | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| __ALL__ | 200 | 97 | 103 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 |

#### 12h · frozen3.0 · pct_dir_adj (the fully causal twin)

Law: IN_RANGE entries by direction-adjusted pct-of-range (pct for a long, 100 - pct for a short; 100 = the boundary the trade must break): [0,100/3), [100/3,200/3), [200/3,100), '<0', '>=100' [SR-16]

| bucket | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| <0 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |
| [0,33.33) | 1 | 0 | 1 | 0.6596 | 1.0000 | 0.6596 | 0 | 0 | 0 | — | — | — |
| [33.33,66.67) | 21 | 12 | 9 | 0.1630 | 0.3333 | 3.4238 | 0 | 0 | 9 | 0.4034 | 0.3333 | 3.6306 |
| [66.67,100) | 52 | 19 | 33 | 0.1540 | 0.3462 | 8.0058 | 0 | 0 | 27 | 0.3034 | 0.3704 | 8.1908 |
| >=100 | 0 | 0 | 0 | — | — | — | 0 | 0 | 0 | — | — | — |

### The anchor: TC10's five-row table (4h, frozen 3.0) beside the TC11 v6 book's own five rows — all eleven columns [L-R.7, SR-11]

#### tc11: the TC11 v6 book (books/v6_campaigns, the TC11 nest)

| macro_state_at_entry | tc11_n | tc11_n_assets | tc11_net_r_sum | tc11_expectancy_r | tc11_median_net_r | tc11_win_rate_pct | tc11_median_mfe_r | tc11_median_pct_of_range | tc11_median_dist_boundary_atr | tc11_n_in_range | tc11_provisional |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BEAR_EXP | 40 | 5 | -0.651001 | -0.016275 | -0.685164 | 37.500000 | 1.471179 | — | — | 0 | False |
| BULL_EXP | 66 | 5 | 14.509604 | 0.219842 | -0.816361 | 28.787879 | 0.678875 | — | — | 0 | False |
| NEUTRAL | 94 | 5 | 26.948963 | 0.286691 | -0.647350 | 37.234043 | 1.264361 | 40.496027 | 2.574482 | 94 | False |
| NONE | 0 | 0 | — | — | — | — | — | — | — | 0 | True |
| __ALL__ | 200 | 5 | 40.807566 | 0.204038 | -0.765597 | 34.500000 | 1.079642 | 40.496027 | 2.574482 | 94 | False |

#### tc10: TC10's filed stamps/control_entry_by_state.parquet (reproduced exactly on the filed journal)

| macro_state_at_entry | tc10_n | tc10_n_assets | tc10_net_r_sum | tc10_expectancy_r | tc10_median_net_r | tc10_win_rate_pct | tc10_median_mfe_r | tc10_median_pct_of_range | tc10_median_dist_boundary_atr | tc10_n_in_range | tc10_provisional |
|---|---|---|---|---|---|---|---|---|---|---|---|
| BEAR_EXP | 40 | 5 | -0.651001 | -0.016275 | -0.685164 | 37.500000 | 1.471179 | — | — | 0 | False |
| BULL_EXP | 66 | 5 | 14.509604 | 0.219842 | -0.816361 | 28.787879 | 0.678875 | — | — | 0 | False |
| NEUTRAL | 94 | 5 | 27.884748 | 0.296646 | -0.647350 | 37.234043 | 1.264361 | 40.496027 | 2.574482 | 94 | False |
| NONE | 0 | 0 | — | — | — | — | — | — | — | 0 | True |
| __ALL__ | 200 | 5 | 41.743351 | 0.208717 | -0.765597 | 34.500000 | 1.079642 | 40.496027 | 2.574482 | 94 | False |

