# BUILD — CENSUS-2B · ORACLE  (Mac-native rev C)

**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `e018ba5` · **Seed** 20260814 · **Executor** HEPHAESTUS · **Drafted** APOLLO

**CLASS — Tier-E + instrument re-pins; m=0.** No registrations. F-KEY on every table. The grid is a *complete partition* of the filed event substrate under one ruler: no cell was selected, ranked or promoted, so there is no family to correct over. Any future selection **from** this grid is a new probe and declares its own *m* before it looks.

**Programs (local, this repo):** `scripts/census2b_oracle.py` · `scripts/census2b_oracle_report.py`. Every ratified helper is **imported, not restated** — the grammar and the crossover rule from `census2b_program.py`, the R-1 ruler / duration-fixed horizon law / toll line from `census2b_parta.py`. This pass adds no constant that is not printed below.

**Tables live local** at `research_outputs/census2b/oracle/` (`oracle_grid.parquet`, `oracle_ledger.parquet`, `r1_pinned_scales.parquet`, `r1_rerun_inert.parquet`, `r2_knot_occupancy.parquet`, `r3_state_occupancy.parquet`, `state_v2/<asset>/<tf>.parquet`, `oracle_manifest.json`). The document carries the grid whole and points at the rest.

**STEP 0 — the indicator is filed.** `pine/SS_v12_0_1.pine`, byte-exact from the operator's attachment, sha256 `af166d92035a3981da0926b589dec6135d5c57a4a4bc49ed833f6b217c068ad9`, committed as *SSv12.0.1 indicator of record*. It ships direct to TradingView; the filing is for the record.

---

## 1 · STAGE R-1 — [VETO 'kiss-scale']

`delta = min(0.75, 0.6 x p95 |spread|/ATR)` per pair, `eps = delta/3`, `k = 10` unchanged. The grammar itself is untouched; only its two scale arguments are re-pinned, from each pair's own pooled spread distribution (panel x 5 lenses).

```
class      pair         bars pooled  med|s|/ATR  p95|s|/ATR   d v1    d v2  eps v2  rescaled
within_sr  12_26          5,380,079      0.4350      1.2478  0.750  0.7487  0.2496       YES
within_sr  89_127         5,371,329      0.5421      1.6037  0.750  0.7500  0.2500        no
within_sr  316_423        5,345,729      0.8945      2.7293  0.750  0.7500  0.2500        no
within_sr  889_1272       5,272,279      2.0096      6.3182  0.750  0.7500  0.2500        no
within_sr  2618_3618      5,069,354      3.3568     10.9609  0.750  0.7500  0.2500        no
within_sr  4618_5000      4,966,429      1.0722      3.6672  0.750  0.7500  0.2500        no
sr_median  12_89          5,374,629      1.5344      4.2149  0.750  0.7500  0.2500        no
sr_median  89_316         5,354,979      2.4470      7.2927  0.750  0.7500  0.2500        no
sr_median  316_889        5,305,429      3.8889     11.8025  0.750  0.7500  0.2500        no
sr_median  889_2618       5,155,854      7.2686     23.0910  0.750  0.7500  0.2500        no
sr_median  2618_4618      4,992,849      6.3212     20.8342  0.750  0.7500  0.2500        no
```

**Previously inert under v1** (0 refusals across panel x 5 lenses): `2618_3618`, `2618_4618`, `316_423`, `4618_5000`, `889_1272`. The grammar was re-run **on these only**; live pairs keep their filed v1 rows, so nothing already published moves.

```
pair         cells    d v2  eps v2   touches v2  refusals v1  refusals v2
2618_3618       25  0.7500  0.2500      198,693            0            0
2618_4618       20  0.7500  0.2500      102,102            0            0
316_423         25  0.7500  0.2500      775,661            0            0
4618_5000       20  0.7500  0.2500      581,916            0            0
889_1272        25  0.7500  0.2500      346,398            0            0
```

**THE RE-PIN IS INERT — 0 refusals recovered, 0 of 5 pairs woken.** This is a finding, not a failure, and the reason is arithmetic: `min(0.75, 0.6 x p95)` can only *lower* delta, and only for a pair whose p95 spread is under 1.25 ATR. Every inert pair is inert because it is **wide**, so the cap binds and nothing moves. Exactly one pair (`12_26`, p95 = 1.2478) falls under the cap at all, and it moves delta by 0.0013.

**The limb that actually fails is the veer limb, and it is measured here.** Touches are abundant; separation is not. `reach` is the best `|spread|/ATR` attainable within k=10 bars of a touch — the quantity delta thresholds.

```
  pair             touches  reach p50  reach p95  reach MAX  delta pinned  clears?
  2618_3618        198,693     0.1366     0.3116     0.4658        0.7500    NEVER
  2618_4618        102,102     0.1470     0.3214     0.5143        0.7500    NEVER
  316_423          775,661     0.1523     0.3334     0.6112        0.7500    NEVER
  4618_5000        581,916     0.1389     0.2808     0.4225        0.7500    NEVER
  889_1272         346,398     0.1519     0.3153     0.5469        0.7500    NEVER
```

**MEASURED, NOT APPLIED.** No constant above is pinned by this pass. The reading: across the whole panel and all five lenses the maximum reach any of these pairs ever attains is 0.6112 ATR, so **no delta at or above ~0.62 can ever wake them**, and a delta sized off the *spread* p95 will never be that low. A working re-pin has to be sized off the **reach** distribution (p95 ~ 0.28-0.33 ATR), which is a different law from the one ratified. That ruling is the operator's; this pass does not take it.

## 2 · STAGE R-2 — [VETO 'knot-scale']

`KNOT = per-SR (width < 0.5 x ATR)`; BR-dispersion demoted to a **column**.

**F-R2 — PASS, 0 violations.** Verified against the filed substrate rather than re-derived: `<SR>_knot` already thresholds *that family's own* `<SR>_width_atr` at 0.5, element for element, on every cell. **The per-SR reading was already the filed reading** — this veto ratifies what the substrate does, and the only change is that the Big-Ribbon envelope is now a reported column and never a knot definition.

```
KNOT OCCUPANCY (share of warm bars with width < 0.5 ATR; panel mean)
  SR            5m      15m      30m       1h       4h
  FAST      0.4585   0.4702   0.4609   0.4538   0.4306
  M         0.2675   0.2617   0.2483   0.2488   0.2122
  MH        0.1908   0.1888   0.1750   0.1597   0.1557
  H         0.0741   0.0677   0.0608   0.0656   0.0583
  VH        0.0338   0.0341   0.0337   0.0333   0.0227
  UH        0.1156   0.1168   0.1089   0.1280       --

BR-DISPERSION  median (max upper - min lower)/ATR over all 6 SRs -- COLUMN ONLY
  disp      20.249   19.918   19.618   18.092    8.583
```

The gradient is the point: a knot is common in FAST (~46% of bars) and rare in VH (~3%). A single Big-Ribbon threshold would have read 18-20 ATR of dispersion as *never knotted* and erased the FAST knot entirely. UH at 4h is blank because UH is not warm there (§6).

## 3 · STAGE R-3 — [VETO 'state-scale']

`k = max(20, round(median_len/8))` per SR. `_v2` columns are written **beside** the originals (`oracle/state_v2/<asset>/<tf>.parquet`); nothing is overwritten. `eps` stays 0.05 ATR and the three state codes are unchanged — k is the width-delta lookback only.

```
SR         (fast,median,slow)  median_len   k v1   k v2  changed
FAST              (9, 12, 26)          12     20     20       no
M               (62, 89, 127)          89     20     20       no
MH            (262, 316, 423)         316     20     40      YES
H            (616, 889, 1272)         889     20    111      YES
VH         (1618, 2618, 3618)        2618     20    327      YES
UH         (4236, 4618, 5000)        4618     20    577      YES
```

**Occupancy, v1 (global k=20) -> v2 (per-SR k), panel mean.** Only the `flat` share is printed here — it is the one the mis-scale destroys; the full three-state grid at all five lenses is in `r3_state_occupancy.parquet`.

```
  SR       k v2                5m              15m              30m               1h               4h
  FAST       20    0.0652->0.0652   0.0657->0.0657   0.0648->0.0648   0.0631->0.0631   0.0604->0.0604
  M          20    0.0814->0.0814   0.0813->0.0813   0.0777->0.0777   0.0780->0.0780   0.0696->0.0696
  MH         40    0.1756->0.0964   0.1749->0.0962   0.1712->0.0933   0.1615->0.0849   0.1401->0.0753
  H         111    0.1714->0.0368   0.1663->0.0343   0.1596->0.0318   0.1519->0.0320   0.0952->0.0227
  VH        327    0.2349->0.0169   0.2219->0.0165   0.2007->0.0145   0.1497->0.0111   0.0149->0.0012
  UH        577    0.9279->0.0607   0.8788->0.0543   0.7994->0.0451   0.6367->0.0359   0.0000->0.0000
```

**This is the largest single correction in the pass.** Under the global k=20, UH read **92.8% flat** at 5m — a 4236/5000 band does not change width measurably in 20 bars of a 5-minute chart, so the state column was reporting the lookback, not the ribbon. At k=577 it becomes 6.1% flat and the three states separate. FAST and M are unchanged by construction (their k floors at 20), so the correction lands exactly where the mis-scale was and nowhere else.

## 4 · THE ORACLE GRID

**856,877 anchors**, complete partition, m = 0, toll-honest. `oracle_ledger.parquet` (row-level) · `oracle_grid.parquet` (this grid).

**Ruler** — R-1: signed *terminal* return over the duration-fixed horizon, ATR-normalised **at the anchor**; MFE/MAE window `[i+1, i+bars]`. **Horizons are durations, not bar counts**: H20 = 1h40m, H100 = 8h20m, so `bars = round(h_ms / TF_MS)` — 20/100 at 5m, 7/33 at 15m, 3/17 at 30m, 2/8 at 1h, and at 4h **H20 is INFEASIBLE (bars = 0), emitted as NaN and never substituted with one bar**. **Toll** — 10 bps round trip in ATR units, median over *that cell's own anchor population*; `NET = median - toll`. **Orient** — `with` = VH **and** UH both fanned the way the event points; `against` = both fanned opposite; `mixed` = anything else, including any `mixed(0)` or `n/a(-9)` limb, because a not-yet-warm ultra-high ribbon is not evidence of agreement.

### lens 5m

```
class        cut           n   med20  NET20  med100 NET100   toll   H20 IQR         H100 IQR
12_26 IN-WIN ALL     124,822  -0.085 -0.362  -0.101 -0.379 0.2779   [-1.803, 1.674] [-4.138, 3.990]
              up      62,407  -0.050 -0.328  -0.079 -0.357
              down    62,415  -0.121 -0.399  -0.122 -0.400
              o:with  47,833  -0.078 -0.356  -0.164 -0.442
              o:agst  48,028  -0.070 -0.348  -0.026 -0.304
              o:mixed 28,961  -0.114 -0.392  -0.112 -0.389
12_26 bare   ALL          42  -0.260 -0.459  -0.476 -0.675 0.1989   [-1.020, 0.897] [-4.329, 2.805]
              up          21  -0.298 -0.497  -3.797 -3.996
              down        21  -0.064 -0.263   1.334  1.135
              o:mixed     42  -0.260 -0.459  -0.476 -0.675
26_89        ALL      44,646  -0.137 -0.415  -0.155 -0.432 0.2777   [-1.858, 1.676] [-4.132, 4.079]
              up      22,325  -0.122 -0.400  -0.107 -0.385
              down    22,321  -0.152 -0.429  -0.192 -0.470
              o:with  16,942  -0.155 -0.433  -0.248 -0.526
              o:agst  17,269  -0.081 -0.358  -0.026 -0.303
              o:mixed 10,435  -0.190 -0.467  -0.185 -0.463
12_89        ALL      66,140  -0.134 -0.411  -0.147 -0.424 0.2778   [-1.860, 1.667] [-4.193, 4.046]
              up      33,071  -0.110 -0.388  -0.114 -0.391
              down    33,069  -0.157 -0.435  -0.180 -0.458
              o:with  25,257  -0.135 -0.413  -0.194 -0.472
              o:agst  25,579  -0.120 -0.398  -0.096 -0.374
              o:mixed 15,304  -0.158 -0.436  -0.162 -0.440
89_127       ALL      19,819  -0.162 -0.426  -0.126 -0.390 0.2640   [-1.788, 1.640] [-3.879, 3.986]
              up       9,910  -0.096 -0.360   0.000 -0.264
              down     9,909  -0.232 -0.496  -0.243 -0.507
              o:with   7,451  -0.167 -0.431  -0.211 -0.475
              o:agst   7,876  -0.170 -0.435  -0.075 -0.339
              o:mixed  4,492  -0.139 -0.403  -0.065 -0.329
89_316       ALL      12,163  -0.153 -0.407  -0.117 -0.371 0.2541   [-1.735, 1.600] [-3.705, 3.894]
              up       6,082  -0.109 -0.363  -0.001 -0.255
              down     6,081  -0.200 -0.454  -0.197 -0.451
              o:with   4,491  -0.143 -0.397  -0.068 -0.322
              o:agst   5,003  -0.199 -0.453  -0.178 -0.432
              o:mixed  2,669  -0.106 -0.360  -0.019 -0.273
316_423      ALL       5,446  -0.089 -0.341  -0.109 -0.362 0.2524   [-1.639, 1.574] [-3.453, 3.619]
              up       2,725  -0.011 -0.264  -0.095 -0.348
              down     2,721  -0.156 -0.408  -0.120 -0.372
              o:with   1,861  -0.043 -0.296  -0.151 -0.404
              o:agst   2,427  -0.086 -0.339  -0.170 -0.422
              o:mixed  1,158  -0.116 -0.368   0.172 -0.080
316_889      ALL       3,763  -0.225 -0.476  -0.133 -0.384 0.2517   [-1.705, 1.440] [-3.380, 3.655]
              up       1,881  -0.136 -0.388   0.201 -0.051
              down     1,882  -0.284 -0.535  -0.402 -0.654
              o:with   1,195  -0.275 -0.527  -0.265 -0.517
              o:agst   1,769  -0.184 -0.435  -0.077 -0.329
              o:mixed    799  -0.236 -0.488  -0.220 -0.472
889_2618     ALL       1,271  -0.090 -0.373   0.260 -0.022 0.2822   [-1.656, 1.615] [-3.229, 4.300]
              up         635  -0.090 -0.373   0.322  0.039
              down       636  -0.099 -0.381   0.242 -0.040
              o:with     249  -0.111 -0.393   1.085  0.803
              o:agst     739  -0.082 -0.364   0.161 -0.122
              o:mixed    283  -0.071 -0.353   0.226 -0.056
2618_4618    ALL         524   0.189 -0.083   0.112 -0.161 0.2722   [-1.397, 1.787] [-3.482, 3.910]
              up         262   0.333  0.061   0.287  0.015
              down       262   0.049 -0.223  -0.099 -0.371
              o:with      12   0.371  0.099   0.590  0.318
              o:agst       1  -1.475 -1.747   5.457  5.185
              o:mixed    511   0.214 -0.059   0.073 -0.200
knot->fan    ALL     123,411  -0.133 -0.403  -0.091 -0.361 0.2699   [-1.794, 1.626] [-3.967, 3.975]
              up      62,169  -0.098 -0.368  -0.059 -0.329
              down    61,242  -0.168 -0.437  -0.120 -0.390
              o:with  47,249  -0.129 -0.398  -0.119 -0.389
              o:agst  47,553  -0.125 -0.395  -0.062 -0.332
              o:mixed 28,609  -0.153 -0.423  -0.096 -0.366
spring       ALL     142,470   0.226 -0.007   0.203 -0.029 0.2329   [-1.591, 1.795] [-3.730, 3.735]
              up      68,003   0.267  0.034   0.291  0.058
              down    74,467   0.186 -0.047   0.121 -0.112
              o:with  52,816   0.270  0.037   0.213 -0.020
              o:agst  56,941   0.185 -0.048   0.165 -0.068
              o:mixed 32,713   0.218 -0.015   0.245  0.012
```

### lens 15m

```
class        cut           n   med20  NET20  med100 NET100   toll   H20 IQR         H100 IQR
12_26 IN-WIN ALL      40,630  -0.079 -0.231  -0.088 -0.240 0.1522   [-1.042, 0.926] [-2.262, 2.212]
              up      20,317  -0.070 -0.222  -0.049 -0.201
              down    20,313  -0.085 -0.237  -0.133 -0.285
              o:with  14,314  -0.102 -0.254  -0.056 -0.208
              o:agst  14,361  -0.062 -0.214  -0.080 -0.232
              o:mixed 11,955  -0.073 -0.225  -0.134 -0.286
12_26 bare   ALL          50  -0.184 -0.332   0.236  0.088 0.1483   [-0.586, 0.981] [-2.803, 2.299]
              up          25  -0.506 -0.655  -0.848 -0.996
              down        25   0.291  0.143   1.116  0.968
              o:mixed     50  -0.184 -0.332   0.236  0.088
26_89        ALL      14,381  -0.101 -0.248  -0.064 -0.211 0.1474   [-1.018, 0.925] [-2.161, 2.167]
              up       7,191  -0.082 -0.229   0.019 -0.129
              down     7,190  -0.116 -0.263  -0.141 -0.289
              o:with   5,043  -0.068 -0.215  -0.079 -0.226
              o:agst   5,135  -0.097 -0.245  -0.054 -0.201
              o:mixed  4,203  -0.150 -0.298  -0.053 -0.201
12_89        ALL      20,914  -0.093 -0.243  -0.072 -0.222 0.1503   [-1.044, 0.932] [-2.189, 2.134]
              up      10,458  -0.060 -0.210  -0.017 -0.167
              down    10,456  -0.126 -0.276  -0.121 -0.271
              o:with   7,323  -0.085 -0.236  -0.050 -0.200
              o:agst   7,416  -0.080 -0.230  -0.025 -0.175
              o:mixed  6,175  -0.120 -0.270  -0.140 -0.290
89_127       ALL       6,189  -0.083 -0.229  -0.051 -0.197 0.1456   [-0.945, 0.932] [-1.969, 2.133]
              up       3,094  -0.071 -0.216  -0.012 -0.157
              down     3,095  -0.092 -0.238  -0.075 -0.220
              o:with   2,124  -0.055 -0.201   0.040 -0.106
              o:agst   2,248  -0.099 -0.245  -0.108 -0.254
              o:mixed  1,817  -0.084 -0.229  -0.081 -0.226
89_316       ALL       3,900  -0.101 -0.246  -0.084 -0.229 0.1452   [-0.989, 0.877] [-1.934, 2.046]
              up       1,950  -0.088 -0.233  -0.012 -0.158
              down     1,950  -0.122 -0.267  -0.158 -0.303
              o:with   1,311  -0.114 -0.260  -0.084 -0.229
              o:agst   1,479  -0.091 -0.237  -0.090 -0.235
              o:mixed  1,110  -0.106 -0.251  -0.061 -0.206
316_423      ALL       1,863  -0.074 -0.218  -0.075 -0.218 0.1433   [-0.968, 0.876] [-2.120, 2.082]
              up         932  -0.008 -0.151   0.077 -0.066
              down       931  -0.122 -0.265  -0.205 -0.348
              o:with     583   0.020 -0.123   0.012 -0.132
              o:agst     765  -0.107 -0.250  -0.131 -0.274
              o:mixed    515  -0.077 -0.220  -0.140 -0.284
316_889      ALL       1,229  -0.039 -0.191  -0.043 -0.195 0.1515   [-0.972, 0.848] [-1.793, 2.282]
              up         614  -0.018 -0.170  -0.002 -0.154
              down       615  -0.066 -0.218  -0.094 -0.246
              o:with     355  -0.139 -0.291  -0.021 -0.173
              o:agst     538  -0.054 -0.205  -0.160 -0.311
              o:mixed    336   0.119 -0.032   0.021 -0.131
889_2618     ALL         373   0.000 -0.157  -0.137 -0.294 0.1567   [-0.994, 0.909] [-1.989, 1.838]
              up         187  -0.024 -0.181   0.033 -0.123
              down       186   0.000 -0.157  -0.420 -0.577
              o:with      61   0.027 -0.130  -0.655 -0.812
              o:agst     222   0.000 -0.157  -0.286 -0.443
              o:mixed     90  -0.178 -0.335   0.593  0.436
2618_4618    ALL         167  -0.015 -0.191   0.110 -0.066 0.1758   [-0.931, 1.050] [-1.995, 2.139]
              up          82  -0.084 -0.260   0.275  0.099
              down        85   0.106 -0.070  -0.163 -0.339
              o:with       2   0.395  0.219   2.841  2.665
              o:mixed    165  -0.015 -0.191   0.110 -0.066
knot->fan    ALL      39,345  -0.085 -0.231  -0.104 -0.250 0.1458   [-1.028, 0.906] [-2.172, 2.157]
              up      19,796  -0.074 -0.220  -0.083 -0.229
              down    19,549  -0.099 -0.245  -0.129 -0.275
              o:with  13,952  -0.095 -0.241  -0.072 -0.218
              o:agst  13,808  -0.065 -0.211  -0.118 -0.263
              o:mixed 11,585  -0.103 -0.249  -0.120 -0.265
spring       ALL      47,788   0.099 -0.031   0.163  0.034 0.1292   [-0.941, 1.006] [-2.053, 2.062]
              up      22,067   0.140  0.010   0.222  0.093
              down    25,721   0.062 -0.067   0.107 -0.022
              o:with  16,359   0.134  0.005   0.224  0.094
              o:agst  17,899   0.065 -0.064   0.080 -0.049
              o:mixed 13,530   0.097 -0.032   0.180  0.051
```

### lens 30m

```
class        cut           n   med20  NET20  med100 NET100   toll   H20 IQR         H100 IQR
12_26 IN-WIN ALL      19,688  -0.062 -0.168  -0.048 -0.154 0.1055   [-0.662, 0.607] [-1.537, 1.544]
              up       9,845  -0.046 -0.151   0.021 -0.084
              down     9,843  -0.075 -0.180  -0.108 -0.214
              o:with   6,632  -0.034 -0.139  -0.028 -0.133
              o:agst   6,659  -0.073 -0.179  -0.063 -0.169
              o:mixed  6,397  -0.079 -0.185  -0.053 -0.158
12_26 bare   ALL          54  -0.162 -0.276  -0.434 -0.548 0.1147   [-1.042, 0.239] [-1.880, 0.758]
              up          28  -0.090 -0.205  -0.496 -0.611
              down        26  -0.277 -0.392  -0.269 -0.384
              o:mixed     54  -0.162 -0.276  -0.434 -0.548
26_89        ALL       6,816  -0.051 -0.153  -0.041 -0.144 0.1028   [-0.636, 0.591] [-1.424, 1.456]
              up       3,409  -0.038 -0.141   0.000 -0.102
              down     3,407  -0.061 -0.164  -0.091 -0.193
              o:with   2,279  -0.066 -0.169  -0.050 -0.153
              o:agst   2,324  -0.062 -0.165  -0.056 -0.159
              o:mixed  2,213  -0.023 -0.126  -0.015 -0.118
12_89        ALL      10,103  -0.084 -0.188  -0.059 -0.163 0.1040   [-0.681, 0.588] [-1.580, 1.558]
              up       5,052  -0.084 -0.188  -0.096 -0.200
              down     5,051  -0.081 -0.185  -0.029 -0.133
              o:with   3,393  -0.087 -0.191  -0.146 -0.250
              o:agst   3,438  -0.076 -0.180   0.000 -0.104
              o:mixed  3,272  -0.087 -0.191  -0.048 -0.152
89_127       ALL       3,126  -0.051 -0.156  -0.035 -0.139 0.1047   [-0.639, 0.580] [-1.349, 1.427]
              up       1,563   0.000 -0.105   0.068 -0.037
              down     1,563  -0.083 -0.188  -0.134 -0.239
              o:with   1,047  -0.105 -0.210  -0.140 -0.244
              o:agst   1,104   0.000 -0.105   0.000 -0.105
              o:mixed    975  -0.041 -0.146   0.001 -0.104
89_316       ALL       2,035  -0.014 -0.118  -0.067 -0.172 0.1049   [-0.568, 0.569] [-1.377, 1.453]
              up       1,018   0.000 -0.105   0.016 -0.089
              down     1,017  -0.043 -0.148  -0.143 -0.248
              o:with     657   0.007 -0.098  -0.037 -0.142
              o:agst     727  -0.018 -0.123  -0.035 -0.139
              o:mixed    651  -0.032 -0.137  -0.086 -0.191
316_423      ALL         866  -0.005 -0.106  -0.164 -0.264 0.1009   [-0.615, 0.584] [-1.542, 1.410]
              up         433  -0.111 -0.212  -0.296 -0.397
              down       433   0.030 -0.071  -0.062 -0.163
              o:with     252  -0.047 -0.148  -0.251 -0.351
              o:agst     336   0.041 -0.060  -0.062 -0.163
              o:mixed    278  -0.053 -0.154  -0.231 -0.332
316_889      ALL         562  -0.020 -0.123  -0.135 -0.239 0.1035   [-0.626, 0.662] [-1.486, 1.336]
              up         280  -0.022 -0.126  -0.120 -0.223
              down       282  -0.009 -0.113  -0.144 -0.248
              o:with     156  -0.041 -0.144   0.001 -0.103
              o:agst     241   0.040 -0.063  -0.187 -0.291
              o:mixed    165  -0.032 -0.136  -0.114 -0.218
889_2618     ALL         192  -0.081 -0.190  -0.353 -0.462 0.1090   [-0.752, 0.466] [-1.395, 1.640]
              up          95   0.066 -0.043  -0.218 -0.327
              down        97  -0.160 -0.269  -0.470 -0.579
              o:with      36   0.029 -0.080   0.156  0.047
              o:agst     109  -0.021 -0.130  -0.370 -0.479
              o:mixed     47  -0.470 -0.579  -0.440 -0.549
2618_4618    ALL          70  -0.059 -0.168  -0.166 -0.275 0.1094   [-0.765, 0.605] [-1.893, 1.212]
              up          33  -0.196 -0.306   0.141  0.032
              down        37   0.094 -0.015  -0.566 -0.675
              o:with       2   2.272  2.163   4.500  4.391
              o:mixed     68  -0.110 -0.219  -0.374 -0.484
knot->fan    ALL      19,296  -0.074 -0.177  -0.069 -0.171 0.1022   [-0.677, 0.589] [-1.535, 1.548]
              up       9,526  -0.068 -0.170  -0.021 -0.123
              down     9,770  -0.082 -0.184  -0.107 -0.209
              o:with   6,415  -0.068 -0.171  -0.075 -0.177
              o:agst   6,538  -0.074 -0.176  -0.063 -0.165
              o:mixed  6,343  -0.084 -0.186  -0.068 -0.170
spring       ALL      24,509   0.028 -0.063   0.096  0.004 0.0915   [-0.677, 0.645] [-1.505, 1.463]
              up      11,078   0.057 -0.034   0.154  0.063
              down    13,431   0.000 -0.092   0.052 -0.039
              o:with   8,058   0.043 -0.049   0.183  0.092
              o:agst   8,630   0.036 -0.055   0.041 -0.051
              o:mixed  7,821   0.002 -0.089   0.076 -0.016
```

### lens 1h

```
class        cut           n   med20  NET20  med100 NET100   toll   H20 IQR         H100 IQR
12_26 IN-WIN ALL       9,573  -0.054 -0.127  -0.018 -0.091 0.0731   [-0.526, 0.463] [-1.005, 1.057]
              up       4,787  -0.041 -0.114   0.000 -0.073
              down     4,786  -0.066 -0.139  -0.027 -0.100
              o:with   2,650  -0.068 -0.141  -0.116 -0.190
              o:agst   2,659  -0.062 -0.135   0.059 -0.014
              o:mixed  4,264  -0.038 -0.111  -0.013 -0.086
12_26 bare   ALL          74  -0.249 -0.354  -0.157 -0.262 0.1052   [-0.517, 0.242] [-1.075, 0.517]
              up          37  -0.309 -0.414  -0.177 -0.283
              down        37  -0.168 -0.273  -0.027 -0.132
              o:mixed     74  -0.249 -0.354  -0.157 -0.262
26_89        ALL       3,391  -0.047 -0.120  -0.054 -0.127 0.0726   [-0.499, 0.467] [-0.922, 0.976]
              up       1,696  -0.014 -0.086  -0.014 -0.086
              down     1,695  -0.088 -0.161  -0.084 -0.156
              o:with     951  -0.059 -0.131  -0.096 -0.169
              o:agst     969  -0.043 -0.116  -0.036 -0.109
              o:mixed  1,471  -0.042 -0.114  -0.054 -0.126
12_89        ALL       4,884  -0.052 -0.125  -0.009 -0.081 0.0724   [-0.513, 0.492] [-0.985, 1.072]
              up       2,443  -0.048 -0.120   0.000 -0.072
              down     2,441  -0.056 -0.128  -0.028 -0.100
              o:with   1,355  -0.085 -0.158  -0.026 -0.098
              o:agst   1,373  -0.034 -0.106   0.000 -0.072
              o:mixed  2,156  -0.051 -0.123   0.000 -0.072
89_127       ALL       1,653  -0.039 -0.110   0.014 -0.056 0.0707   [-0.498, 0.478] [-0.998, 1.053]
              up         827  -0.013 -0.084   0.034 -0.037
              down       826  -0.073 -0.143  -0.008 -0.078
              o:with     462  -0.059 -0.129  -0.006 -0.077
              o:agst     490  -0.042 -0.113  -0.016 -0.087
              o:mixed    701  -0.028 -0.099   0.067 -0.003
89_316       ALL         911  -0.025 -0.099  -0.094 -0.167 0.0735   [-0.507, 0.481] [-1.045, 1.053]
              up         455  -0.035 -0.108  -0.129 -0.203
              down       456   0.000 -0.074  -0.069 -0.142
              o:with     234  -0.039 -0.113   0.010 -0.063
              o:agst     266  -0.032 -0.106  -0.161 -0.235
              o:mixed    411  -0.009 -0.083  -0.094 -0.167
316_423      ALL         401  -0.119 -0.198  -0.185 -0.264 0.0791   [-0.495, 0.387] [-0.985, 0.815]
              up         201  -0.097 -0.176  -0.197 -0.276
              down       200  -0.153 -0.232  -0.150 -0.229
              o:with      98  -0.020 -0.100  -0.279 -0.358
              o:agst     134  -0.162 -0.241  -0.117 -0.196
              o:mixed    169  -0.134 -0.213  -0.197 -0.276
316_889      ALL         256   0.054 -0.015   0.066 -0.003 0.0689   [-0.466, 0.527] [-0.830, 1.227]
              up         127   0.142  0.073  -0.097 -0.166
              down       129  -0.052 -0.121   0.192  0.123
              o:with      63  -0.050 -0.119   0.048 -0.021
              o:agst      98   0.091  0.022   0.131  0.062
              o:mixed     95   0.089  0.021   0.062 -0.007
889_2618     ALL          76  -0.049 -0.131  -0.098 -0.180 0.0820   [-0.476, 0.599] [-0.807, 1.044]
              up          36  -0.066 -0.148  -0.151 -0.233
              down        40  -0.003 -0.085   0.187  0.105
              o:with       9  -0.205 -0.287  -0.061 -0.143
              o:agst      42   0.152  0.070   0.275  0.193
              o:mixed     25  -0.221 -0.303  -0.157 -0.239
2618_4618    ALL          29   0.004 -0.075  -0.667 -0.746 0.0793   [-0.603, 0.332] [-1.251, 0.516]
              up          14   0.012 -0.067  -0.538 -0.617
              down        15  -0.179 -0.258  -0.824 -0.903
              o:with       1  -1.466 -1.545  -1.782 -1.862
              o:mixed     28   0.012 -0.067  -0.580 -0.659
knot->fan    ALL       9,512  -0.073 -0.144  -0.082 -0.154 0.0713   [-0.548, 0.449] [-1.048, 0.985]
              up       4,785  -0.060 -0.132  -0.088 -0.160
              down     4,727  -0.088 -0.159  -0.072 -0.143
              o:with   2,594  -0.072 -0.144  -0.117 -0.188
              o:agst   2,617  -0.090 -0.161  -0.010 -0.081
              o:mixed  4,301  -0.070 -0.141  -0.097 -0.168
spring       ALL      12,501  -0.004 -0.068   0.062 -0.002 0.0636   [-0.567, 0.510] [-1.049, 0.989]
              up       5,418   0.022 -0.042   0.127  0.063
              down     7,083  -0.025 -0.089   0.000 -0.064
              o:with   3,406  -0.017 -0.081   0.115  0.052
              o:agst   3,384  -0.009 -0.072   0.021 -0.043
              o:mixed  5,711   0.005 -0.058   0.054 -0.010
```

### lens 4h

```
class        cut           n   med20  NET20  med100 NET100   toll   H20 IQR         H100 IQR
12_26 IN-WIN ALL       2,328      --     --  -0.022 -0.057 0.0352   [    --,    --] [-0.436, 0.495]
              up       1,164      --     --   0.000 -0.035
              down     1,164      --     --  -0.040 -0.075
              o:mixed  2,328      --     --  -0.022 -0.057
12_26 bare   ALL          44      --     --  -0.084 -0.126 0.0422   [    --,    --] [-0.338, 0.526]
              up          23      --     --   0.129  0.087
              down        21      --     --  -0.254 -0.296
              o:mixed     44      --     --  -0.084 -0.126
26_89        ALL         767      --     --  -0.012 -0.050 0.0381   [    --,    --] [-0.490, 0.527]
              up         383      --     --  -0.036 -0.074
              down       384      --     --   0.010 -0.028
              o:mixed    767      --     --  -0.012 -0.050
12_89        ALL       1,116      --     --   0.054  0.016 0.0378   [    --,    --] [-0.436, 0.519]
              up         557      --     --   0.056  0.018
              down       559      --     --   0.051  0.013
              o:mixed  1,116      --     --   0.054  0.016
89_127       ALL         332      --     --  -0.101 -0.141 0.0406   [    --,    --] [-0.525, 0.357]
              up         166      --     --  -0.133 -0.173
              down       166      --     --  -0.077 -0.117
              o:mixed    332      --     --  -0.101 -0.141
89_316       ALL         218      --     --  -0.007 -0.042 0.0348   [    --,    --] [-0.394, 0.505]
              up         108      --     --   0.155  0.120
              down       110      --     --  -0.035 -0.070
              o:mixed    218      --     --  -0.007 -0.042
316_423      ALL          88      --     --  -0.207 -0.245 0.0379   [    --,    --] [-0.629, 0.297]
              up          43      --     --  -0.360 -0.398
              down        45      --     --  -0.005 -0.043
              o:mixed     88      --     --  -0.207 -0.245
316_889      ALL          53      --     --  -0.051 -0.092 0.0410   [    --,    --] [-0.566, 0.264]
              up          26      --     --   0.026 -0.015
              down        27      --     --  -0.252 -0.293
              o:mixed     53      --     --  -0.051 -0.092
889_2618     ALL           7      --     --   0.383  0.336 0.0472   [    --,    --] [ 0.160, 0.583]
              up           2      --     --   0.192  0.145
              down         5      --     --   0.385  0.338
              o:mixed      7      --     --   0.383  0.336
2618_4618    --            0 NO EVENTS AT THIS LENS
knot->fan    --            0 NO EVENTS AT THIS LENS
spring       --            0 NO EVENTS AT THIS LENS
```

**F-O1 — counts reconcile to the filed inventories: PASS.** Every native cross class, both halves of `12_26`, and `spring` reconcile **exactly** (delta = 0) against `crosses/`, `windows/` and `springs/`. `knot->fan` is a join and is bounded by both parents (191,564 <= min(262,086 knots, 318,427 fans)). `26_89` is derived this pass and is excluded from reconciliation by construction — see §6.

**F-O1b — the derivation rule reproduces a filed class: PASS.** Re-deriving `12_26` from the pinned `emas/` substrate with the same `crossover` expression gives **197,305 events against 197,305 filed, 0 mismatched cells**. That is what licenses `26_89`.

## 5 · STAGE W-E+ — the three full cards

Straight from the campaign rows in `_reviewer_box/wf1/*USDT_*.json`. **No recomputation.** `gross_R` is the stored `ride_R` from `research_outputs/census2a/cen5/cen5_campaigns.parquet` — read, not recomputed. `realized_r`, `mfe_r`, `mae_r`, `give_back_r` are in the journal's own R units (size-scaled); `gross_R` is the size-free ruler.

```
                                      c61t75                    c554t720                    c186t225
                               ETHUSDT_swing            ETHUSDT_intraday            ETHUSDT_intraday
mandate / dir                   swing / long             intraday / long             intraday / long
size_r                              0.500000                    0.250000                    0.500000
grade / zone                          A / Z3                      B / Z1                      B / Z3
entry ts                2020-12-26T11:30:00Z        2023-01-02T06:56:00Z        2021-01-02T10:09:00Z
entry px_fill                     621.834342                 1200.660084                  728.075586
stop                              619.754229                 1199.855501                  726.722050
exit px                          1677.744384                 1524.375064                 1102.029550
exit ts                 2021-02-23T04:10:00Z        2023-01-18T21:02:00Z        2021-01-11T03:24:00Z
exit_reason                   opposite_cross              opposite_cross                   failure_x
realized_r                        193.463416                   97.697795                  120.806991
gross_R                           507.621415                  402.338641                  276.279214
mfe_r                             685.619229                  552.161444                  462.923957
mae_r                              -0.848195                   -0.298395                   -0.750320
give_back_r                       177.997814                  149.822803                  186.644744
funding_cum                      3509.703566                  139.254302                  931.850038
hold (s)                             5071200                     1433160                      753300
```

All three are ETH **longs** and all three resolved on a **directional exit, never a stop** — `failure_x` / `opposite_cross` — after 9 to 59 days open, spread across 2020, 2021 and 2023. The shape they share is the one worth naming: **`mae_r` never exceeds 0.85** — the stop was never seriously threatened on any of them — while `give_back_r` runs 150 to 187, a give-back of 177-220x the initial risk unit handed back from the high-water mark. **What decided these campaigns was give-back, not the stop.** Read alongside the grid with care: §4 conditions on nothing that resembles a hold of 9-59 days, so it does not speak to these arms directly. It is the mark-default surface they are drawn from, not a model of them.

## 6 · FINDINGS — NOT FIXED

Named, measured, left alone. Each needs an operator ruling, not a patch.

**F-1 · The kiss-scale veto as ratified cannot do its job.** §1. `min(0.75, 0.6 x p95 spread)` is a *ceiling-lowering* law aimed at tight pairs; the five inert pairs are inert because they are **wide**. Measured veer reach never exceeds 0.61 ATR on any of them, anywhere on the panel. **Ruling needed: re-size delta off the reach distribution, or accept these five as permanently inert and say so.** Not taken here — a different law is a different veto.

**F-2 · `26_89` is not in the filed crosses taxonomy.** The taxonomy is 18 within-family pairs + 5 midlines + price/band; `26_89` is a **cross-family** adjacency (FAST-slow vs M-mid) nobody emitted. Rather than fabricate or drop the class, it is **derived this pass** from the pinned `emas/` substrate with the same `crossover` expression and the same feasibility gate, labelled `derived<emas>` on every row, and **excluded from F-O1**. F-O1b licenses the rule by reproducing `12_26` exactly. 70,001 events. **Ruling needed: promote `26_89` into the pinned taxonomy and re-run stage 4, or keep it derived-at-query.**

**F-3 · The `12_26 IN-WINDOW` / `bare` split is structurally degenerate.** A window is armed by a `12_89` cross and **closed by the counter `12_89` cross — the same cross that arms the next one**. Measured: the union of windows covers **100.0000% of the armed span on every one of the 25 cells**. So `bare` cannot mean 'outside a regime'; it can only be the pre-first-arming warm-up head — **264 events against 197,041** panel-wide. Both rows are printed as specified. **Ruling needed: if IN-WINDOW is to discriminate, it has to mean something narrower — e.g. inside a TRIGGERED window and before its trigger bar. That is a new predicate, not a re-read.**

**F-4 · The 4h lens is three-quarters of a lens, and the grid says so per cell.** Three structural absences, three different causes, none of them fixable by this pass: **(a) H20 is INFEASIBLE at 4h** (bars = 0) — the whole H20 half of the 4h grid is NaN by the pinned horizon law; **(b) `knot->fan` and `spring` do not exist at 4h** — `transitions/`, `springs/` and `refusals/` stop at 1h because Part A pins its lens lists to [5m,15m,30m,1h]; **(c) `2618_4618` is unrealizable at 4h** — EMA-4618 needs more warm bars than 4h history provides, verdict NEVER on all five assets. Each prints `NO EVENTS AT THIS LENS` rather than an empty-looking zero.

**F-5 · VH/UH orientation conditioning is vacuous at 4h.** UH is never warm at 4h and VH barely, so `with` and `against` are unreachable and **100% of 4h rows fall to `mixed`**. That is the correct behaviour of the stated rule, not a defect in it — but it means the 4h orientation cut carries no information and must not be read as 'orientation did not matter'. It is the only lens where the conditioning is undefined rather than measured.

**F-6 · The toll is not comparable across assets and this grid pools them.** `toll_atr` is `median(10bps x close / ATR)` on each cell's own anchors, so it tracks each instrument's close/ATR level, not any market property: it runs roughly 2.5x between the panel's extremes. The NET column is therefore honest **within** a cell and only indicative **across** assets. A per-asset NET is one groupby away in `oracle_ledger.parquet` and is deliberately not printed here — it would be five times the grid for a distinction no cell in this pass turns on.

**F-7 · The rev-B document does not exist in the estate.** The paste supersedes 'P0/P1 rev B'; a repo-wide search finds no rev-B contract, and the three veto *names* (`kiss-scale`, `knot-scale`, `state-scale`) appear nowhere before this paste. What exists is the four scale-mismatch findings raised in the 2026-08-14 build and the standing LEDGER_APOLLO ask that the operator *'rule on the four scale-mismatched constants as one question rather than four'*. **This pass reads rev C as that ruling** and executes it as ratified text. Three of the four are now answered; the fourth — `state_eps_atr = 0.05` — was not named in rev C and is **still unscaled**.

**F-8 · Nothing here is a registration, and the grid must not be mined as if it were.** m = 0 holds only because the partition is complete and unranked. The moment a cell is picked out of §4 on its NET, the selection surface is the number of cells that were available to pick from — 313 non-empty rows — and that *m* has to be declared before the look, not after.

## 7 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `pine/SS_v12_0_1.pine` | **filed**, byte-exact, sha `af166d92035a3981…`, committed |
| R-1 per-pair scales | **pinned and printed**; re-pin **inert**, cause measured (F-1) |
| R-2 per-SR knot | **verified PASS**, 0 violations; BR demoted to column |
| R-3 per-SR state k | **applied**, `_v2` beside originals, originals untouched |
| THE ORACLE GRID | **built whole**, printed whole, m = 0, F-O1 + F-O1b PASS |
| W-E+ three cards | **printed from source rows**, no recomputation |
| registrations | **none**, as classed |

### BOX-COST

`exchange/**` measured **2,497,681 B = 39.09%** of the 6,390,000 B box **before this paste** — already **WARN** (warn 25% / refuse 40%), and 58,319 B from the REFUSE line.

**This paste adds ~52,341 B** — this document plus the LEDGER_APOLLO append and the probe-ledger entry — taking `exchange/**` to **~2,550,022 B = ~39.91%**. Still below REFUSE.

**Against the <0.5% target (31,950 B) this is an overage of ~20,391 B, and it has one cause: STAGE O says the grid is printed *whole*.** The grid alone is 313 non-empty rows across five lenses. Everything else was compressed to the bone to pay for it: the R-1 re-run table is aggregated per pair (the 115-cell version is in `r1_rerun_inert.parquet`), R-3 prints only the `flat` share (the full three-state grid is in `r3_state_occupancy.parquet`), the window-tiling diagnostic is one measured sentence instead of its 25-row table, and no per-asset cut is printed anywhere. Those four decisions saved roughly 20 KB. The full transcripts and the uncompressed tables stay local.

**Named at the moment of creation, per the BOX COST ruling — two things.**

*First,* **5,978 B is all the room left before REFUSE.** At ~39.91% the bus is one ordinary build document from aborting its own publish. This lane cannot fix that by writing less — §4 is the deliverable. **It needs an operator decision on the bus, not on this paste**: archive the closed census-2A cycle off the bus, or raise `BOX_BYTES`, or accept that the next lane to publish gets REFUSED. Flagging it now rather than after it trips.

*Second,* one artifact in this publish is not this lane's work: `exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` (5,975 B), untracked. It is **not** a stray duplicate — it is ATHENA's Mac-era note of record, and the ` copy.txt` name is the only form it exists in anywhere in the repo. `publish_exchange` is path-scoped to `exchange/**` and stages the whole bus, so it goes with this push, which is the right outcome: the note belongs on the bus. It is counted here so the next BOX-COST line reconciles, and ATHENA may want to re-file it under a `.md` name it chose.

## 8 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 'append' ruling — *a report without its ledger entry is an incomplete deliverable* — this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, **in this session**. The entry is quoted here by its spine only: the complete block lives in the ledger, and duplicating it into the box a second time would pay twice for one piece of prose (§7).

```
=== STATUS_APOLLO — 2026-08-15 ===
NOW: THE ORACLE IS BUILT — one grid, complete partition, 856,877 anchors, m = 0, toll-honest.
     knot-scale VERIFIED · state-scale APPLIED (and it was the real defect) · kiss-scale
     RUN AND INERT, with the reason measured rather than guessed.
CLASS: Tier-E + instrument re-pins. NO REGISTRATIONS. m = 0.
LAST EVENT: 2026-08-15 — CENSUS-2B ORACLE rev C, one build document
FACTS: [11 — Mac-era rules v2 acknowledged in-lane and ATHENA's crossing saluted · Pine
       v12.0.1 filed byte-exact · the grid is the per-lens mark-default authority for the
       indicator's next revision · R-3 was the real defect · R-2 changed nothing because
       nothing was wrong · R-1 is inert and needs a ruling · 26_89 derived, not fabricated ·
       IN-WINDOW/bare is degenerate · the 4h lens is three-quarters of a lens · F-O1 and
       F-O1b PASS · BOX-COST]
PENDING: [6 operator rulings — the kiss re-size · 26_89's taxonomy · the IN-WINDOW
         predicate · the 4h lens set · state_eps_atr, the fourth unscaled constant · three
         items carried from 2026-08-14]
NEXT: the operator reads §1 (the kiss re-pin is inert, and the measurement that says why),
§4 (the grid), and §6 F-3. Owner: operator.
METRICS: operator actions this session = 1 — files re-ingested = 0 — indicator filed = 1
=== END STATUS ===
```

---

*End of build document. Class: Tier-E + instrument re-pins; m=0. No registrations. Selection surface m = 0, declared in the probe ledger. The ORACLE grid is the per-lens mark-default authority for the next revision of SS v12.*
