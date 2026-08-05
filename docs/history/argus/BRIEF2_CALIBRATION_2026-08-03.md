# BRIEF-2 CALIBRATION — 2026-08-03 (post_ny)

`brief_2026-08-03_post_ny.json` · schema 2.1.0 · rules 2.0.0 · analytics 1.3.0

> **PARITY NOT CERTIFIED.** Nothing here is adopted. **No threshold is re-ratified in this report** (reviewer ruling D-2) — it prints distributions so the operator and reviewer can rule on them.

## ITEM 6 — does volume evidence move the lines? *(the headline)*

**A line in the sand moved on 10 of 10 assets** (20 of 20 individual sides).

Where a line moved and both views had one, the move was **0.199 daily-ATR at the median** (min 0.005, p90 0.945, max 1.283, n=20).

| asset | side | with volume | without volume | Δ ATR |
|---|---|---|---|---|
| BTCUSDT | above | 63,892.83 | 63,811.24 | 0.049 |
| BTCUSDT | below | 62,859.01 | 63,273.95 | 0.252 |
| ETHUSDT | above | 1,880.00 | 1,877.84 | 0.032 |
| ETHUSDT | below | 1,860.69 | 1,844.45 | 0.241 |
| FARTCOINUSDT | above | 0.13 | 0.13 | 0.182 |
| FARTCOINUSDT | below | 0.12 | 0.13 | 0.220 |
| HYPEUSDT | above | 52.64 | 56.88 | 1.283 |
| HYPEUSDT | below | 51.85 | 52.57 | 0.218 |
| JTOUSDT | above | 0.49 | 0.51 | 0.316 |
| JTOUSDT | below | 0.48 | 0.49 | 0.198 |
| LITUSDT | above | 2.07 | 2.05 | 0.100 |
| LITUSDT | below | 2.02 | 1.83 | 0.945 |
| NEARUSDT | above | 1.75 | 1.71 | 0.380 |
| NEARUSDT | below | 1.66 | 1.68 | 0.138 |
| SOLUSDT | above | 74.37 | 74.43 | 0.024 |
| SOLUSDT | below | 73.61 | 73.08 | 0.200 |
| TAOUSDT | above | 195.90 | 195.58 | 0.032 |
| TAOUSDT | below | 192.91 | 192.96 | 0.005 |
| ZECUSDT | above | 494.45 | 495.07 | 0.020 |
| ZECUSDT | below | 456.53 | 486.13 | 0.945 |

*whether volume evidence MOVES THE OPERATOR'S LINES. It is display-only; whether the move helps is census work under G-7.*

## Item 1 — registry size by family

v1.1 reference: 46-62 (contract §5.3, not recomputed) · contract expectation ~180-200 (§5.3) · measured min 126 / median 148.0 / max 173

| asset | total | anchored | rolling | profile | structure | ss |
|---|---|---|---|---|---|---|
| BTCUSDT | 165 | 49 | 28 | 30 | 34 | 24 |
| ETHUSDT | 157 | 49 | 28 | 33 | 35 | 12 |
| FARTCOINUSDT | 143 | 42 | 28 | 30 | 27 | 16 |
| HYPEUSDT | 140 | 42 | 28 | 27 | 27 | 16 |
| JTOUSDT | 153 | 42 | 28 | 36 | 29 | 18 |
| LITUSDT | 126 | 42 | 21 | 22 | 25 | 16 |
| NEARUSDT | 153 | 42 | 28 | 39 | 28 | 16 |
| SOLUSDT | 173 | 49 | 28 | 42 | 38 | 16 |
| TAOUSDT | 141 | 42 | 28 | 30 | 23 | 18 |
| ZECUSDT | 140 | 42 | 28 | 33 | 27 | 10 |

## Item 2 — score distribution and the family cap

min 2 · median 2 · p90 8 · max 18 over 599 clusters.

The cap (=3) binds in **28 of 965** family-in-cluster opportunities (2.9%). the cap binds whenever one family contributes more members than FAMILY_CAP to a single cluster -- that is it doing its job, stopping one prolific tool manufacturing agreement with itself

## Item 3 — line-in-the-sand stability across tolerance

| asset | stable? | above spread | below spread |
|---|---|---|---|
| BTCUSDT | NO | 1,034.65 | 859.19 |
| ETHUSDT | NO | 6.40 | 5.90 |
| FARTCOINUSDT | NO | 0.00 | 0.00 |
| HYPEUSDT | NO | 4.09 | 0.51 |
| JTOUSDT | NO | 0.02 | 0.01 |
| LITUSDT | NO | 0.04 | 0.02 |
| NEARUSDT | NO | 0.03 | 0.03 |
| SOLUSDT | NO | 1.14 | 0.30 |
| TAOUSDT | NO | 2.55 | 6.21 |
| ZECUSDT | NO | 1.39 | 14.97 |

## Item 4 — family composition of the top-3 areas

Largest-family tally across all top-3 areas: `{'ss': 10, 'structure': 2, 'vwap_anchored': 7, 'vwap_rolling': 2, 'profile_windowed': 9}`

*does vwap_rolling or profile_windowed DOMINATE the top areas? if so the family split did not go far enough (§9.2 item 4)*

## Item 5 — VA nesting state distribution

Overall: `{'nested_inside': 15, 'overlapping': 10, 'disjoint_below': 2, 'disjoint_above': 2, 'unavailable(warming)': 1}`

- `30d<->90d` → {'nested_inside': 7, 'overlapping': 2, 'disjoint_above': 1}
- `7d<->30d` → {'nested_inside': 4, 'overlapping': 4, 'disjoint_below': 2}
- `90d<->365d` → {'nested_inside': 4, 'overlapping': 4, 'disjoint_above': 1, 'unavailable(warming)': 1}

## Item 7 — measured storage

| | bytes |
|---|---|
| capture (one slot) | 1,879,133 |
| partition `snapshots` | 17,538 |
| partition `levels` | 43,793 |
| partition `areas` | 13,636 |
| partitions per day | 74,967 |

Projected annual at 3 slots/day: **captures 2057.7 MB + partitions 27.4 MB = 2085.0 MB/yr** against a contract estimate of 150-250 (§8.2) MB.

## Extra — invalidation distance distribution (R-1, stage C.4)

floor **0.25** · min 0.171 · p25 0.339 · median 0.352 · p75 0.382 · max 0.425 (n=40)

40 rows ranked, 0 excluded as too tight. R-1 stage C.4 -- the floor is a v1 PLACEHOLDER and is re-ratified against this distribution, not against a guess

## Runtime

One full capture: **217.41s** (one capture must stay well under ~15 min; three slots per day).

---

Confluence scores measure **agreement between tools**, not edge. R:R measures **geometry**, not probability. Whether any of it predicts anything is census work under G-7.