# Phase A — input-parity audit (Engine 1.0.3 gate)

Every input constant in the engine's cell/config layer vs the deployed Pine
input default (`pine/SS_Cascade_v11.0.2.pine`, operator-verified capture).
**Result: `zone_memory` was the SOLE unratified drift → gate passed, proceeded to Phase B.**

## Signal constants (both configs — v11_faithful & naiad_v0; identical signal blocks)

| engine key | value | Pine input (line) | default | verdict |
|---|---|---|---|---|
| len_fast | 9 | lenFast (79) | 9 | MATCH |
| len_slow | 89 | lenSlow (80) | 89 | MATCH |
| len_trend | 200 | lenTrend (81) | 200 | MATCH |
| atr_len | 14 | atrLen (82) | 14 | MATCH |
| structure_gate | true | structureGate (88) | true | MATCH |
| provisional_arming | true | provisionalArming (93) | true | MATCH |
| prov_zones | "Z1+Z2" | provZones (99) | "Z1+Z2" | MATCH |
| whipsaw_bars | 10 | whipsawBars (112) | 10 | MATCH |
| z1_prox | 0.25 | z1Prox (118) | 0.25 | MATCH |
| z2_prox | 0.35 | z2Prox (119) | 0.35 | MATCH |
| z3_prox | 0.35 | z3Prox (120) | 0.35 | MATCH |
| min_bar_range_atr | 0.5 | minBarRangeATR (125) | 0.5 | MATCH |
| min_ribbon_sep_atr | 0.5 | minRibbonSepATR (126) | 0.5 | MATCH |
| cooldown_bars | 5 | cooldownBars (128) | 5 | MATCH |
| max_r_count | 0 | maxRCount (129) | 0 | MATCH |
| snipe_on | true | snipeOn (132) | true | MATCH |
| snipe_lookback | 55 | snipeLookback (133) | 55 | MATCH |
| fib1 | 0.5 | fib1 (134) | 0.5 | MATCH |
| fib2 | 0.786 | fib2 (135) | 0.786 | MATCH |
| cap_on | true | capOn (140) | true | MATCH |
| climax_mult | 3.5 | climaxMult (141) | 3.5 | MATCH |
| cap_ext_atr | 1.0 | capExtATR (142) | 1.0 | MATCH |
| cap_window | 10 | capWindow (144) | 10 | MATCH |
| cap_vol_conf | 1.2 | capVolConf (145) | 1.2 | MATCH |
| vol_len | 20 | volLen (146) | 20 | MATCH |
| tpw_on | true | tpwOn (149) | true | MATCH |
| cluster_n | 2 | clusterN (150) | 2 | MATCH |
| cluster_win | 12 | clusterWin (151) | 12 | MATCH |
| stop_buf_atr | 0.5 | stopBufATR (154) | 0.5 | MATCH |
| fail_win | 3 | failWin (158) | 3 | MATCH |

## Cell-layer constant (all mandates)

| mandate (exec) | engine `zone_memory` pre-fix | Pine default | verdict |
|---|---|---|---|
| swing (5m) | **5** | zoneMemory=3 (121) | **UNRATIFIED DRIFT** → fixed to 3 |
| intraday (1m) | 3 | 3 | MATCH |
| position (15m) | 3 | 3 | MATCH |

## Charter-ratified NON-input divergences (not asserted; per I1)

| item | v11_faithful | naiad_v0 | citation |
|---|---|---|---|
| v_births_provisional | false (Pine literal) | true | charter §3.2 (logic policy, not an input constant) |
| tf_gov / tf_exec / tf_align | swing = 4h/5m/1h = Pine defaults (240/chart/60) | per-mandate | charter §4 (the three mandates ARE their TF triples; intraday/position deliberately override the Pine defaults) |

## Display-only Pine inputs with no engine counterpart (N/A)

`boxBorderTr`, `boxFillTr`, `showStops`, `showEMAs`, `showZones`, `showRegArrows`,
`showBgTint`, `showGrades`, `show1mArrows`, `mtf{5,1h,4h,12}On` — the engine has no
display layer; nothing to conform.

## Gate verdict

Sole unratified input-constant divergence = **`zone_memory` (swing, 5 vs 3)**.
No drift beyond it → Phase-B stop rule NOT triggered → proceeded to the fix.
