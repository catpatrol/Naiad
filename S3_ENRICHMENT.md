# S-3 ENRICHMENT — Cell-B Anatomy, Retracement, Confluence, P-CIRC & Cross-Run Excursion Substrate (engine 1.0.11, capture on)

> **in-sample / first-order (exploration-classic window, current entries; ranks & reveals, does not validate out-of-sample); B denominated in struct-R (engine sizes qty on the structural distance, so realized_r is natively risk-normalized to the wider static stop); baseline = S-1, native ratchet, baseline-R.**

> Trading is UNCHANGED (F-BYTE proves it); this is instrumentation only. J-1 out a fifth time, disclosed.

## Fixtures (F-BYTE first)

- **F-BYTE**: MATCH — `{"mismatched_cells": []}`
- **F-P2REF**: MATCH — `{"measured": {"sum_1x": -351.1542, "sum_0x": 1164.4202, "tranches": 7094, "win_rate_pct": 21.3322}, "target": {"sum_1x": -351.1542, "sum_0x": 1164.4202, "tranches": 7094, "win_rate_pct": 21.3322}}`
- **F-CIRC-N**: MATCH — `{"pcirc_snapshots": 3114, "reached_1r_tranches": 3114}`
- **F-SUB**: MATCH — `{"substrate_rows": 7094, "resolved_tranches": 7094, "nonretr_nulls": 0}`
- **F-DET**: MATCH — `{"mismatched": [], "manifest": true}`

## Headline (cell-B, struct-R; recomputed traded, = F-P2REF)

- GRID 1x **-351.1542** | 0x 1164.4202 | 2x -1866.7286 | 7094 tranches | 1186 campaigns | win 21.3322% (campaign-level)

## D1 — Per-trade anatomy (cell-B) beside the S-1 baseline

Reached-profit tier histogram (MFE, struct-R on B / baseline-R on S-1); PROTECTED-paradox on both books.

| MFE tier | B n | B % | S-1 (cohort-coarse) |
|---|---|---|---|
| <0 | 0 | 0.0 | NEVER_GREEN 17.42% |
| 0-0.5 | 2865 | 40.3862 | STILLBORN 27.46% |
| 0.5-1 | 1115 | 15.7175 | FADED 14.17% |
| 1-2 | 1085 | 15.2946 |  |
| 2-3 | 515 | 7.2597 |  |
| >=3 | 1514 | 21.342 | PROTECTED 40.95% (>=1R total) |

> Note: MFE (peak favorable excursion) is ≥0 by construction, so the `<0` tier is always empty; the never-green population (MFE exactly 0) sits in the `0-0.5` bucket and is reported separately as the NEVER_GREEN cohort below.

- **Cohort mix (B)**: NEVER_GREEN 9.9944% | STILLBORN 30.3919% | FADED 15.7175% | PROTECTED 43.8963%  vs  baseline NEVER_GREEN 17.42% | STILLBORN 27.46% | FADED 14.17% | PROTECTED 40.95%
- **PROTECTED paradox**: of 3114 B tranches reaching >=+1R MFE, 2294 reversed to a 0x (gross) loss (73.6673% of PROTECTED); of those, **100.0%** had zero stop advance before the peak (baseline 90.3487%). B's stop is STATIC by construction.
- **Median peak-capture (B, realized/MFE, reached-profit)**: -43.6543% (baseline published p50: swing -20.93 / intraday -20.8 / position -7.98; contract soft ref ~6%).

Win rate by exit reason (B, tranche-level):

| exit reason | B n | B win% | S-1 n | S-1 win% |
|---|---|---|---|---|
| stop | 4995 | 0.0 | 6223 | 16.2301 |
| failure_x | 1352 | 23.5947 | 9 | 33.3333 |
| opposite_cross | 719 | 67.0376 | 3 | 66.6667 |
| stop_gap | 21 | 0.0 | 40 | 10.0 |
| campaign_died | 4 | 25.0 | 4 | 25.0 |
| v_reversal | 3 | 33.3333 | — | — |

## D2 — Retracement-depth expectancy (cell-B, struct-R)

| decile | retr range | n | expectancy R | ci95 | strip-best | MFE_r med |
|---|---|---|---|---|---|---|
| 1 | -5.4884-0.0704 | 697 | -0.2153 | [-0.3574, -0.034] | -0.2729 | 0.6515 |
| 2 | 0.0704-0.1308 | 697 | 0.0286 | [-0.2258, 0.4125] | -0.1222 | 0.747 |
| 3 | 0.1308-0.1719 | 696 | -0.1244 | [-0.3099, 0.1235] | -0.2019 | 0.6973 |
| 4 | 0.1719-0.2037 | 697 | -0.0169 | [-0.253, 0.3436] | -0.1572 | 0.8273 |
| 5 | 0.2037-0.2365 | 696 | -0.2064 | [-0.3186, -0.06] | -0.2551 | 0.831 |
| 6 | 0.2365-0.2708 | 697 | 0.2751 | [-0.1996, 0.9828] | -0.0025 | 0.838 |
| 7 | 0.2708-0.3096 | 697 | -0.0257 | [-0.2039, 0.1827] | -0.0875 | 0.8649 |
| 8 | 0.3096-0.3644 | 696 | -0.0857 | [-0.2518, 0.1065] | -0.1298 | 0.916 |
| 9 | 0.3644-0.4612 | 697 | -0.0868 | [-0.2534, 0.1177] | -0.1329 | 0.7119 |
| 10 | 0.4612-1.571 | 697 | 0.0117 | [-0.3186, 0.4859] | -0.1618 | 0.6859 |

- **Pocket question (0.5-0.8 band)**: mid-band expectancy -0.2244 (n 470) vs shallowest -0.2153 / deepest 0.0117; mid-band beats both ends, sign-stable: **False**.
- A+ overlay (reference, tiny n): n 359, expectancy -0.2324 — NOT the estimator.

## D3 — Confluence re-scored on the winning (B) book

RC-7r joint lattice (30m-aligned x 1d-room x toll-payable), GRID slice, camp-R (1x). Cell key `30m|1d_room|toll`.

| lattice cell | n | expectancy | ci95 | S-1 ref |
|---|---|---|---|---|
| 30m=1|1d_room=1|toll=1 | 902 | -0.1284 | [-0.2953, 0.0582] | -0.4557 |
| 30m=0|1d_room=0|toll=0 | 174 | -1.2151 | [-1.5153, -0.8307] | -1.2244 |

- **P-S3-3 flips** (conditions negative-separating on S-1, positive on B): **8**. 15m|s2_aligned (S-1 -0.0134 -> B 0.1417); 15m|beyond_e200 (S-1 -0.2021 -> B 0.1584); 30m|beyond_e89 (S-1 -0.2537 -> B 0.1135); 12h|s2_aligned (S-1 -0.147 -> B 0.1172); 12h|beyond_e200 (S-1 -0.1614 -> B 0.1814); 1d|s2_aligned (S-1 -0.0911 -> B 0.2294)
- Triple-true lattice: S-1 -0.4557 -> B -0.1284.

## D4 — P-CIRC decoupled-add evidence (+1R-moment snapshots)

- **97.5915%** of the 3114 +1R winning moments had NO pullback-reclaim PRIME available that bar — the circular freeze, measured directly. (PRIME available 2.4085%, CONFIRM available 4.9775%, either 7.2897%.)
- Why unavailable — gate pass-rates at winning moments: raw-reclaim 5.7161% | zone>0 47.7521% | range-ok 99.4541% | ribsep-ok 89.4348%.
- Independent state a non-PRIME add could key on: price beyond exec-e9 (in dir) 99.0045% | beyond exec-e89 80.3147% | beyond gov-e89 95.5363% | 9/89 aligned 64.6114% | median ribbon-sep 1.9827 ATR.

## D5 — Cross-run excursion substrate (P-KEEP)

- `s3_excursion_substrate.jsonl` — 7094 rows (sha256 `a2cf6f2739e3a2ee...`), one per resolved tranche, keyed `trigger_type x grade x entry_zone x dir`, MFE/MAE in BOTH bps and entry-ATR at horizons {10,20,50,100 exec bars} and at exit.
- §8: S-1 / arm-A journals do NOT carry joinable fixed-horizon dual-basis excursion -> substrate ships **cell-B-only**; back-fill re-emission (S-1 + arm-A with this substrate on, byte-safe) is the named P-KEEP follow-up.

Pivot — median MFE/MAE (entry-ATR) at h100 by trigger_type x grade x entry_zone (top rows by n):

| trigger | grade | zone | n | MFE atr h100 | MAE atr h100 | MFE atr exit |
|---|---|---|---|---|---|---|
| PRIME-R1 | B | Z1 | 1558 | 4.0095 | -4.3805 | 7.0515 |
| PRIME-add | B | Z1 | 1130 | 4.3566 | -3.8757 | 2.2588 |
| PRIME-R1 | A | Z1 | 989 | 4.0677 | -4.0279 | 7.7186 |
| PRIME-add | B | Z3 | 676 | 3.2169 | -4.1613 | 1.3993 |
| PRIME-R1 | B | Z2 | 605 | 3.989 | -4.7334 | 2.8982 |
| PRIME-R1 | A | Z3 | 454 | 3.7682 | -4.4208 | 3.0753 |
| PRIME-add | A | Z1 | 438 | 3.8227 | -4.4664 | 2.3857 |
| PRIME-add | B | Z2 | 396 | 3.8007 | -4.3076 | 1.6655 |
| PRIME-add | A+ | Z3 | 312 | 2.8799 | -4.0186 | 1.3978 |
| PRIME-add | A | Z3 | 250 | 3.6645 | -3.9055 | 1.6312 |
| PRIME-R1 | B | Z3 | 161 | 4.2954 | -4.3624 | 2.2763 |
| V | V | - | 78 | 2.6574 | -2.9125 | 1.1027 |
| PRIME-R1 | A+ | Z3 | 43 | 1.9268 | -5.0365 | 1.0436 |
| PRIME-R1 | A+ | Z1 | 4 | 3.5502 | -4.4947 | 43.1451 |

## D6 — The anatomy delta (one paragraph)

Did the structural stop change the SHAPE of how trades win and lose, or just widen the graveyard? BOTH — and the shape change is the deeper finding. It widened the graveyard (STILLBORN rose 27.46% -> 30.3919%, 7094 tranches vs the baseline's 6279), but it also re-plumbed the win/loss machinery. The static struct stop sits BELOW entry and never advances, so on B a `stop` exit is a loss with probability ~1 (stop win-rate 0.0% vs the baseline ratchet's 16.2301%, where the ratchet could climb above entry). B's wins therefore MIGRATE off the stop entirely: they come from flatten exits — opposite_cross (719 exits, 67.0376% win) and failure_x (1352, 23.5947%) — the stop is now a pure loss-cap, not a profit gate. The PROTECTED paradox also inverted in CAUSE: baseline had 90.35% zero-advance among reached-then-lost (a ratchet that could move but was frozen by the pullback coupling); B is 100.0% zero-advance because the stop is static by construction — it protects by initial WIDTH, never by advancing — and the reversal share of PROTECTED rose to 73.6673% (baseline 47.96%): the wider stop lets +1R winners round-trip further, so median peak-capture is -43.6543% (worse, not better). B does not 'fix' the paradox; it swaps a frozen-ratchet pathology for a no-ratchet architecture whose 2294 reached-then-gross-loss tranches ARE the decoupled-add prize P-CIRC sizes: 97.5915% of winning moments had no pullback-reclaim PRIME available to add on. The winning book wins by holding a wide static stop through the reversal — the residual value lives in adding to those winners the current gate structurally cannot touch.

## Scorecard (falsifications first)

| # | prior | verdict | measured |
|---|---|---|---|
| P-S3-1 | 60% | **FALSIFIED** | `{"B_zero_advance_share_pct": 100.0, "baseline_pct": 90.3487, "reached1r_then_grossloss_n": 2294}` |
| P-S3-2 | 55% | **FALSIFIED** | `{"mid_band_0p5_0p8_exp_r": -0.2244, "shallowest": -0.2153, "deepest": 0.0117, "mid_band_beats_both_ends": false}` |
| P-S3-5 | 60% | **FALSIFIED** | `{"B_median_peak_capture_pct": -43.6543, "soft_baseline_ref_pct": 6.0, "published_baseline_p50_pct": {"swing": -20.93, "intraday": -20.8, "position": -7.98}}` |
| P-S3-3 | 60% | **CONFIRMED** | `{"n_conditions_flipping_positive": 8, "flips": [{"cell": "15m|s2_aligned", "s1_sep": -0.0134, "b_sep": 0.1417, "b_exp_true": -0.0586}, {"cell": "15m|beyond_e200` |
| P-S3-4 | 65% | **CONFIRMED** | `{"prime_unavailable_share_pct": 97.5915, "n_winning_moments": 3114}` |

*scripts/s3_enrich.py (run) + scripts/s3_analyze.py (analyze); raw journal bytes + in-process signal/trade recompute; engine byte-untouched.*
