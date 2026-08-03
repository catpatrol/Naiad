# BRIEF-2 CALIBRATION — 2026-08-03 (post_ny)

`brief_2026-08-03_post_ny.json` · schema 2.1.0 · rules 2.0.0 · analytics 1.3.0

> **PARITY NOT CERTIFIED.** Nothing here is adopted. **No threshold is re-ratified in this report** (reviewer ruling D-2) — it prints distributions so the operator and reviewer can rule on them.

## ITEM 6 — does volume evidence move the lines? *(the headline)*

**A line in the sand moved on 10 of 10 assets** (20 of 20 individual sides).

Where a line moved and both views had one, the move was **0.127 daily-ATR at the median** (min 0.005, p90 0.681, max 0.946, n=20).

| asset | side | with volume | without volume | Δ ATR |
|---|---|---|---|---|
| BTCUSDT | above | 63,803.92 | 63,851.58 | 0.028 |
| BTCUSDT | below | 63,199.60 | 63,302.82 | 0.061 |
| ETHUSDT | above | 1,931.93 | 1,885.38 | 0.681 |
| ETHUSDT | below | 1,868.32 | 1,868.88 | 0.008 |
| FARTCOINUSDT | above | 0.13 | 0.13 | 0.178 |
| FARTCOINUSDT | below | 0.12 | 0.13 | 0.220 |
| HYPEUSDT | above | 52.70 | 53.24 | 0.165 |
| HYPEUSDT | below | 51.85 | 52.56 | 0.217 |
| JTOUSDT | above | 0.49 | 0.51 | 0.313 |
| JTOUSDT | below | 0.48 | 0.49 | 0.168 |
| LITUSDT | above | 2.07 | 2.05 | 0.089 |
| LITUSDT | below | 2.02 | 1.85 | 0.844 |
| NEARUSDT | above | 1.76 | 1.71 | 0.488 |
| NEARUSDT | below | 1.67 | 1.68 | 0.072 |
| SOLUSDT | above | 73.86 | 73.84 | 0.005 |
| SOLUSDT | below | 73.17 | 73.19 | 0.008 |
| TAOUSDT | above | 195.66 | 195.44 | 0.021 |
| TAOUSDT | below | 192.88 | 192.93 | 0.005 |
| ZECUSDT | above | 494.12 | 494.56 | 0.014 |
| ZECUSDT | below | 456.50 | 486.13 | 0.946 |

*whether volume evidence MOVES THE OPERATOR'S LINES. It is display-only; whether the move helps is census work under G-7.*

## Item 1 — registry size by family

v1.1 reference: 46-62 (contract §5.3, not recomputed) · contract expectation ~180-200 (§5.3) · measured min 93 / median 109.0 / max 117

| asset | total | anchored | rolling | profile | structure | ss |
|---|---|---|---|---|---|---|
| BTCUSDT | 116 | 21 | 28 | 30 | 13 | 24 |
| ETHUSDT | 104 | 21 | 28 | 30 | 13 | 12 |
| FARTCOINUSDT | 108 | 21 | 28 | 30 | 13 | 16 |
| HYPEUSDT | 105 | 21 | 28 | 27 | 13 | 16 |
| JTOUSDT | 116 | 21 | 28 | 36 | 13 | 18 |
| LITUSDT | 93 | 21 | 21 | 22 | 13 | 16 |
| NEARUSDT | 117 | 21 | 28 | 39 | 13 | 16 |
| SOLUSDT | 111 | 21 | 28 | 33 | 13 | 16 |
| TAOUSDT | 110 | 21 | 28 | 30 | 13 | 18 |
| ZECUSDT | 105 | 21 | 28 | 33 | 13 | 10 |

## Item 2 — score distribution and the family cap

min 2 · median 2.0 · p90 7 · max 17 over 446 clusters.

The cap (=3) binds in **19 of 735** family-in-cluster opportunities (2.59%). the cap binds whenever one family contributes more members than FAMILY_CAP to a single cluster -- that is it doing its job, stopping one prolific tool manufacturing agreement with itself

## Item 3 — line-in-the-sand stability across tolerance

| asset | stable? | above spread | below spread |
|---|---|---|---|
| BTCUSDT | NO | 65.61 | 87.68 |
| ETHUSDT | NO | 21.35 | 3.89 |
| FARTCOINUSDT | NO | 0.00 | 0.00 |
| HYPEUSDT | NO | 4.23 | 0.45 |
| JTOUSDT | NO | 0.01 | 0.01 |
| LITUSDT | NO | 0.04 | 0.02 |
| NEARUSDT | NO | 0.02 | 0.02 |
| SOLUSDT | NO | 0.87 | 0.29 |
| TAOUSDT | NO | 2.49 | 6.19 |
| ZECUSDT | NO | 1.63 | 14.99 |

## Item 4 — family composition of the top-3 areas

Largest-family tally across all top-3 areas: `{'ss': 14, 'profile_windowed': 10, 'vwap_anchored': 5, 'vwap_rolling': 1}`

*does vwap_rolling or profile_windowed DOMINATE the top areas? if so the family split did not go far enough (§9.2 item 4)*

## Item 5 — VA nesting state distribution

Overall: `{'nested_inside': 15, 'overlapping': 10, 'disjoint_below': 2, 'disjoint_above': 2, 'unavailable(warming)': 1}`

- `30d<->90d` → {'nested_inside': 7, 'overlapping': 2, 'disjoint_above': 1}
- `7d<->30d` → {'nested_inside': 4, 'overlapping': 4, 'disjoint_below': 2}
- `90d<->365d` → {'nested_inside': 4, 'overlapping': 4, 'disjoint_above': 1, 'unavailable(warming)': 1}

## Item 7 — measured storage

| | bytes |
|---|---|
| capture (one slot) | 1,425,913 |
| partition `snapshots` | 17,535 |
| partition `levels` | 31,995 |
| partition `areas` | 13,597 |
| partitions per day | 63,127 |

Projected annual at 3 slots/day: **captures 1561.4 MB + partitions 23.0 MB = 1584.4 MB/yr** against a contract estimate of 150-250 (§8.2) MB.

## Extra — invalidation distance distribution (R-1, stage C.4)

floor **0.25** · min 0.186 · p25 0.256 · median 0.273 · p75 0.285 · max 0.321 (n=40)

30 rows ranked, 10 excluded as too tight. R-1 stage C.4 -- the floor is a v1 PLACEHOLDER and is re-ratified against this distribution, not against a guess

## Runtime

One full capture: **199.16s** (one capture must stay well under ~15 min; three slots per day).

---

Confluence scores measure **agreement between tools**, not edge. R:R measures **geometry**, not probability. Whether any of it predicts anything is census work under G-7.