# RC Recompute RC-0..RC-6 — Tier A (journal arithmetic + kline inventory)

**Basis:** engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5...`), scored partition, 20 cells.
**Primary basis:** scored-clean (19 cells; `ZECUSDT_intraday` excluded, G-8). **Reference:** scored-20.
**Journal root:** `research_outputs/v3_anchor/journal_pass1/scored`
**Evidence spend:** NONE (VR-1). **Engine delta:** NONE (read-only).
**Bootstrap:** 95% CI, 10,000 resamples, campaign-level, seed `20260716` (pinned).

> **Scope.** In-sample, on mined data. Ranks and sizes; validates nothing. Not a re-run, not TC-4, not S-1, not a variant nomination.

## Definitions restatement (contract §4)

- Open interval of a tranche = [fill_ts, exit_ts): fill row ts_open inclusive, EXIT row ts_open exclusive; exit_ts None => open at data end.
- concurrent_open_at_fill(A) = # siblings B in same (cell,campaign), B!=A, with B.fill_ts <= A.fill_ts and (A.fill_ts < B.exit_ts or B.fill_ts == A.fill_ts). Same-bar siblings count as concurrent.
- True add = ADD_FILL with concurrent >=1; re-entry = ADD_FILL with concurrent ==0; R1 = ENTRY_FILL non-V; V = ENTRY_FILL with is_v (EXIT.shadow.ladder_unthrottled_grade == 'V').
- max_concurrent(campaign) = peak simultaneously-open tranches via event sweep; SAME-BAR FILLS BEFORE SAME-BAR EXITS at equal ts_open.
- Direction-run = maximal same-cell same-direction campaign run in journal time order (by opener fill_ts); attempt number = 1-based index in run.
- Cluster: attempt in-cluster at k iff |opener.px_fill - attempt1.px_fill| <= k * atr_exec(attempt1 fill row).
- bps: mfe_bps = mfe_r*(|px_fill-stop|/px_fill)*1e4; cost_bps = cost_usd/(|qty|*px_fill)*1e4; realized_bps = (realized_r/size_r)*(|px_fill-stop|/px_fill)*1e4 (ENTRY-row prices, cumulative cost from EXIT).

## Fixtures F1–F10 — known-answer gates (contract §5)

Computed from raw journal bytes; no prior report read as input.

| # | fixture | expected | computed | result |
|---|---|---|---|---|
| F1 | Scored campaigns | 3456 | 3456 | **MATCH** |
| F1 | Resolved tranches | 8387 | 8387 | **MATCH** |
| F2 | Σ realized_r scored-20 1× | -5756.9093 | -5756.9093 | **MATCH** |
| F3 | Σ r_0x scored-20 | 1345.3095 | 1345.3095 | **MATCH** |
| F4 | ZEC_intraday tranches | 1414 | 1414 | **MATCH** |
| F4 | ZEC_intraday negative-one_r | 717 | 717 | **MATCH** |
| F5 | ZEC_intraday net 1× | -663.1247 | -663.1247 | **MATCH** |
| F6 | Scored-clean grid 1× | -5093.7846 | -5093.7846 | **MATCH** |
| F7 | Stop-exit events (cell,dir,ts collapse) | 7057 | 7057 | **MATCH** |
| F8 | tranche_cap (max_tranches) REJECT rows | 145749 | 145749 | **MATCH** |
| F9 | V-initiated campaigns | 45 | 45 | **MATCH** |
| F10 | Per-tranche resumption (≥1R/20b, stop exits) | 2899 | 2899 | **MATCH** |

**Fixture verdict: PASS** — 12/12 match.

## RC-0 — Data-estate inventory (filesystem only)

> **Caveat.** Filesystem-only inventory, no network. Row counts / bounds / gaps read from the local parquet caches (open_time column). Resamplability is a FEASIBILITY statement only; resampling is S-1 data-prep, out of scope. Absence here = absent from THIS machine's cache, not necessarily un-fetchable upstream.

Kline cache root: `C:\Users\luisf\AppData\Local\naiad\data_cache\klines`

| asset | TFs present | TFs absent |
|---|---|---|
| BTCUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| ETHUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| JTOUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| NEARUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| SOLUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| TAOUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| ZECUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| HYPEUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| FARTCOINUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |
| LITUSDT | 1m, 5m, 15m, 1h, 4h, 12h | 30m, 1d |

Per-TF detail (rows / first / last / gaps>2×TF):

| asset | TF | rows | first UTC | last UTC | gaps>2×TF |
|---|---|---|---|---|---|
| BTCUSDT | 1m | 3594603 | 2019-09-08 17:57:00 | 2026-07-10 00:00:00 | 0 |
| BTCUSDT | 5m | 718633 | 2019-09-08 17:55:00 | 2026-07-08 23:55:00 | 0 |
| BTCUSDT | 15m | 239642 | 2019-09-08 17:45:00 | 2026-07-10 00:00:00 | 0 |
| BTCUSDT | 1h | 59887 | 2019-09-08 17:00:00 | 2026-07-08 23:00:00 | 0 |
| BTCUSDT | 4h | 14972 | 2019-09-08 16:00:00 | 2026-07-08 20:00:00 | 0 |
| BTCUSDT | 12h | 4991 | 2019-09-08 12:00:00 | 2026-07-08 12:00:00 | 0 |
| ETHUSDT | 1m | 3480016 | 2019-11-27 07:45:00 | 2026-07-10 00:00:00 | 0 |
| ETHUSDT | 5m | 696004 | 2019-11-27 07:45:00 | 2026-07-10 00:00:00 | 0 |
| ETHUSDT | 15m | 232002 | 2019-11-27 07:45:00 | 2026-07-10 00:00:00 | 0 |
| ETHUSDT | 1h | 58002 | 2019-11-27 07:00:00 | 2026-07-10 00:00:00 | 0 |
| ETHUSDT | 4h | 14519 | 2019-11-27 04:00:00 | 2026-07-12 20:00:00 | 0 |
| ETHUSDT | 12h | 4835 | 2019-11-27 00:00:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 1m | 1360200 | 2023-12-08 10:01:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 5m | 272041 | 2023-12-08 10:00:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 15m | 90681 | 2023-12-08 10:00:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 1h | 22671 | 2023-12-08 10:00:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 4h | 5669 | 2023-12-08 08:00:00 | 2026-07-10 00:00:00 | 0 |
| JTOUSDT | 12h | 1891 | 2023-12-08 00:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 1m | 3014881 | 2020-10-15 08:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 5m | 602977 | 2020-10-15 08:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 15m | 200993 | 2020-10-15 08:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 1h | 50249 | 2020-10-15 08:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 4h | 12563 | 2020-10-15 08:00:00 | 2026-07-10 00:00:00 | 0 |
| NEARUSDT | 12h | 4189 | 2020-10-15 00:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 1m | 3059581 | 2020-09-14 07:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 5m | 611917 | 2020-09-14 07:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 15m | 203973 | 2020-09-14 07:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 1h | 50994 | 2020-09-14 07:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 4h | 12750 | 2020-09-14 04:00:00 | 2026-07-10 00:00:00 | 0 |
| SOLUSDT | 12h | 4251 | 2020-09-14 00:00:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 1m | 1179931 | 2024-04-11 14:30:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 5m | 235987 | 2024-04-11 14:30:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 15m | 78663 | 2024-04-11 14:30:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 1h | 19667 | 2024-04-11 14:00:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 4h | 4918 | 2024-04-11 12:00:00 | 2026-07-10 00:00:00 | 0 |
| TAOUSDT | 12h | 1640 | 2024-04-11 12:00:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 1m | 3379200 | 2020-02-05 08:01:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 5m | 675841 | 2020-02-05 08:00:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 15m | 225281 | 2020-02-05 08:00:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 1h | 56321 | 2020-02-05 08:00:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 4h | 14081 | 2020-02-05 08:00:00 | 2026-07-10 00:00:00 | 0 |
| ZECUSDT | 12h | 4695 | 2020-02-05 00:00:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 1m | 584011 | 2025-05-30 10:30:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 5m | 116803 | 2025-05-30 10:30:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 15m | 38935 | 2025-05-30 10:30:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 1h | 9735 | 2025-05-30 10:00:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 4h | 2435 | 2025-05-30 08:00:00 | 2026-07-10 00:00:00 | 0 |
| HYPEUSDT | 12h | 813 | 2025-05-30 00:00:00 | 2026-07-10 00:00:00 | 0 |
| FARTCOINUSDT | 1m | 815356 | 2024-12-20 18:45:00 | 2026-07-10 00:00:00 | 0 |
| FARTCOINUSDT | 5m | 163072 | 2024-12-20 18:45:00 | 2026-07-10 00:00:00 | 0 |
| FARTCOINUSDT | 15m | 54358 | 2024-12-20 18:45:00 | 2026-07-10 00:00:00 | 0 |
| FARTCOINUSDT | 1h | 13591 | 2024-12-20 18:00:00 | 2026-07-10 00:00:00 | 0 |
| FARTCOINUSDT | 4h | 3416 | 2024-12-20 16:00:00 | 2026-07-12 20:00:00 | 0 |
| FARTCOINUSDT | 12h | 1134 | 2024-12-20 12:00:00 | 2026-07-10 00:00:00 | 0 |
| LITUSDT | 1m | 317191 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 1 |
| LITUSDT | 5m | 63439 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 1 |
| LITUSDT | 15m | 21147 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 1 |
| LITUSDT | 1h | 5288 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 1 |
| LITUSDT | 4h | 1323 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 1 |
| LITUSDT | 12h | 442 | 2025-12-01 00:00:00 | 2026-07-10 00:00:00 | 0 |

Absent focus TFs {15m,30m,1d} and local resamplability (feasibility only):

| asset | absent TF | resamplable? |
|---|---|---|
| BTCUSDT | 30m | resamplable from 15m/1m |
| BTCUSDT | 1d | resamplable from 1h/1m |
| ETHUSDT | 30m | resamplable from 15m/1m |
| ETHUSDT | 1d | resamplable from 1h/1m |
| JTOUSDT | 30m | resamplable from 15m/1m |
| JTOUSDT | 1d | resamplable from 1h/1m |
| NEARUSDT | 30m | resamplable from 15m/1m |
| NEARUSDT | 1d | resamplable from 1h/1m |
| SOLUSDT | 30m | resamplable from 15m/1m |
| SOLUSDT | 1d | resamplable from 1h/1m |
| TAOUSDT | 30m | resamplable from 15m/1m |
| TAOUSDT | 1d | resamplable from 1h/1m |
| ZECUSDT | 30m | resamplable from 15m/1m |
| ZECUSDT | 1d | resamplable from 1h/1m |
| HYPEUSDT | 30m | resamplable from 15m/1m |
| HYPEUSDT | 1d | resamplable from 1h/1m |
| FARTCOINUSDT | 30m | resamplable from 15m/1m |
| FARTCOINUSDT | 1d | resamplable from 1h/1m |
| LITUSDT | 30m | resamplable from 15m/1m |
| LITUSDT | 1d | resamplable from 1h/1m |

## RC-1 — Concurrency census + add/re-entry — scored-clean (primary)

> **Caveat.** Classification is OBSERVATIONAL. Selection effects (an add requires ratchet-to-BE which requires a trend) mean cohort differences are NOT causal effects of adding. Ranks/sizes only. Same-bar siblings count as concurrent; exit interval is half-open [fill_ts, exit_ts).

**(a) ADD_FILL classification.** 4,335 ADD_FILL rows: true-add 984 (22.699%), re-entry 3,351 (77.301%).

| fill class | fills | resolved | Σ cell-R 1× | per-unit net 1× | per-unit gross 0× | win rate % |
|---|---|---|---|---|---|---|
| R1 | 2628 | 2617 | -582.3963 | -0.6446 | 0.1436 | 18.8002 |
| true_add | 984 | 967 | -292.1361 | -0.6042 | 0.2341 | 12.9266 |
| re_entry | 3351 | 3351 | -4218.6667 | -2.5179 | 0.4325 | 12.0561 |
| V | 38 | 38 | -0.5855 | -0.0616 | 0.1188 | 31.5789 |

**(b) Campaigns by max_concurrent.**

| max_concurrent | campaigns | Σ 1× | expectancy 1× | 95% CI | win rate % | strip-best Σ 1× |
|---|---|---|---|---|---|---|
| 1 | 1885 | -4806.6904 | -2.55 | [-2.9252, -2.2349] | 2.4934 | -4842.8307 |
| 2 | 879 | -838.0595 | -0.9534 | [-1.3711, -0.5905] | 17.2924 | -879.1722 |
| 3 | 113 | 550.9653 | 4.8758 | [2.9803, 7.4619] | 72.5664 | 436.5135 |

**(c) Real-pyramid population** (≥1 true add ever): 862 campaigns, expectancy -0.1689, share of Σwins 79.6176%.

**(d) Top-10 campaigns by cell-R:**

| campaign | cell-R 1× | tranches | max_concurrent | structure | fill classes |
|---|---|---|---|---|---|
| BTCUSDT_swing#c197 | 114.4519 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| BTCUSDT_intraday#c631 | 50.8402 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| BTCUSDT_intraday#c22 | 41.1127 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| BTCUSDT_position#c55 | 36.1402 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |
| ETHUSDT_intraday#c386 | 29.747 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| BTCUSDT_swing#c191 | 26.6233 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |
| ETHUSDT_swing#c185 | 25.5854 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| ETHUSDT_intraday#c197 | 24.1637 | 3 | 2 | partial-stack | {"R1": 1, "true_add": 1, "re_entry": 1} |
| ETHUSDT_intraday#c732 | 23.9614 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| NEARUSDT_swing#c124 | 23.7686 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |

Serial (max_concurrent<3): **5/10**; stacked (=3): 5/10.

**(e) Fill-spacing (bars between consecutive fills), by class:**

| class | n gaps | median bars | mean bars | min | max |
|---|---|---|---|---|---|
| true_add | 967 | 16.0 | 51.9917 | 0.0 | 760.0 |
| re_entry | 3113 | 35.0 | 248.1748 | 5.0 | 11576.0 |

## RC-1 — Concurrency census + add/re-entry — scored-20 (reference)

**(a) ADD_FILL classification.** 5,192 ADD_FILL rows: true-add 1,147 (22.0917%), re-entry 4,045 (77.9083%).

| fill class | fills | resolved | Σ cell-R 1× | per-unit net 1× | per-unit gross 0× | win rate % |
|---|---|---|---|---|---|---|
| R1 | 3178 | 3167 | -655.4416 | -0.5999 | 0.1179 | 19.2611 |
| true_add | 1147 | 1130 | -323.9788 | -0.5734 | 0.2138 | 12.8319 |
| re_entry | 4045 | 4045 | -4778.8448 | -2.3628 | 0.5402 | 13.869 |
| V | 45 | 45 | 1.356 | 0.1205 | 0.2734 | 33.3333 |

**(b) Campaigns by max_concurrent.**

| max_concurrent | campaigns | Σ 1× | expectancy 1× | 95% CI | win rate % | strip-best Σ 1× |
|---|---|---|---|---|---|---|
| 1 | 2283 | -5573.7825 | -2.4414 | [-2.9652, -2.0403] | 3.7232 | -5626.9744 |
| 2 | 1044 | -769.5863 | -0.7372 | [-1.1115, -0.4234] | 20.2107 | -810.699 |
| 3 | 129 | 586.4594 | 4.5462 | [2.8024, 6.8326] | 72.8682 | 472.0076 |

**(c) Real-pyramid population** (≥1 true add ever): 1010 campaigns, expectancy -0.0384, share of Σwins 73.5246%.

**(d) Top-10 campaigns by cell-R:**

| campaign | cell-R 1× | tranches | max_concurrent | structure | fill classes |
|---|---|---|---|---|---|
| BTCUSDT_swing#c197 | 114.4519 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| ZECUSDT_intraday#c570 | 53.1919 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |
| BTCUSDT_intraday#c631 | 50.8402 | 3 | 3 | stacked (pyramid) | {"R1": 1, "true_add": 2} |
| BTCUSDT_intraday#c22 | 41.1127 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| BTCUSDT_position#c55 | 36.1402 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |
| ETHUSDT_intraday#c386 | 29.747 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| ZECUSDT_intraday#c740 | 29.5205 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |
| ZECUSDT_intraday#c577 | 28.9191 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| ZECUSDT_intraday#c112 | 27.3647 | 3 | 2 | partial-stack | {"R1": 1, "re_entry": 1, "true_add": 1} |
| BTCUSDT_swing#c191 | 26.6233 | 3 | 1 | serial (re-entries) | {"R1": 1, "re_entry": 2} |

Serial (max_concurrent<3): **8/10**; stacked (=3): 2/10.

**(e) Fill-spacing (bars between consecutive fills), by class:**

| class | n gaps | median bars | mean bars | min | max |
|---|---|---|---|---|---|
| true_add | 1130 | 16.0 | 51.4381 | 0.0 | 760.0 |
| re_entry | 3780 | 34.0 | 234.9307 | 5.0 | 11576.0 |

## RC-2 — Equity trajectories + clean-basis certification

> **Caveat.** Equity path reconstructed from EXIT-row equity_after (the only rows carrying it), in journal file order per cell. initial_equity = 10000.0 (v12_anchor.yaml). Zero-crossing = the equity_after series reaches <= 0. Certifies the scored-clean basis.

| cell | exits | min equity | min ts | final equity | zero-crossings | crossed/near |
|---|---|---|---|---|---|---|
| BTCUSDT_intraday | 1103 | 56.65 | 2024-06-12T18:45:00Z | 56.81 | 0 | near |
| BTCUSDT_position | 121 | 7415.84 | 2024-02-05T14:45:00Z | 8623.98 | 0 | no |
| BTCUSDT_swing | 410 | 3304.17 | 2023-06-18T20:10:00Z | 4325.38 | 0 | no |
| ETHUSDT_intraday | 1121 | 2.36 | 2024-06-27T20:48:00Z | 2.36 | 0 | near |
| ETHUSDT_position | 126 | 7214.49 | 2024-06-21T06:15:00Z | 7214.49 | 0 | no |
| ETHUSDT_swing | 399 | 4397.2 | 2024-06-09T10:30:00Z | 4397.2 | 0 | no |
| JTOUSDT_intraday | 144 | 6579.46 | 2024-06-26T23:29:00Z | 6579.46 | 0 | no |
| JTOUSDT_position | 13 | 9712.36 | 2024-05-05T06:00:00Z | 9798.22 | 0 | no |
| JTOUSDT_swing | 30 | 9194.84 | 2024-05-28T01:35:00Z | 9194.84 | 0 | no |
| NEARUSDT_intraday | 1042 | 94.81 | 2024-06-24T04:34:00Z | 95.32 | 0 | near |
| NEARUSDT_position | 75 | 8910.39 | 2024-05-08T14:45:00Z | 8910.39 | 0 | no |
| NEARUSDT_swing | 305 | 6940.36 | 2024-02-09T21:30:00Z | 6970.68 | 0 | no |
| SOLUSDT_intraday | 1079 | 43.48 | 2024-06-25T08:40:00Z | 45.15 | 0 | near |
| SOLUSDT_position | 98 | 8572.52 | 2023-08-24T01:30:00Z | 9005.57 | 0 | no |
| SOLUSDT_swing | 353 | 5102.04 | 2024-06-28T10:15:00Z | 5102.04 | 0 | no |
| TAOUSDT_intraday | 48 | 8686.7 | 2024-06-27T00:16:00Z | 8686.7 | 0 | no |
| TAOUSDT_swing | 6 | 9873.99 | 2024-06-06T07:30:00Z | 9935.64 | 0 | no |
| ZECUSDT_intraday | 1414 | -2732.24 | 2024-06-28T02:03:00Z | -2719.97 | 1 | YES |
| ZECUSDT_position | 118 | 8038.26 | 2024-04-04T17:45:00Z | 8060.81 | 0 | no |
| ZECUSDT_swing | 382 | 2402.92 | 2024-06-05T18:15:00Z | 2402.92 | 0 | no |

> **Certification.** CERTIFIED: no cell other than ZECUSDT_intraday crossed zero

## RC-3 — Edge in basis points — scored-clean (primary)

> **Caveat.** The most fundamental number: does favourable excursion exceed round-trip cost IN PRICE TERMS, before R-space amplification. Per-tranche. bps use ENTRY-row prices; cost is round-trip cumulative from the EXIT row. Negative-one_r rows (bankrupt-cell) keep valid price ratios but corrupted R sign -- excluded already in scored-clean.

| scope | n | mfe_bps med | cost_bps med | realized_bps med | mfe/cost med | frac mfe>cost % |
|---|---|---|---|---|---|---|
| GRID | 6973 | 15.4274 | 19.8474 | -28.3541 | 0.9245 | 48.6304 |
| swing | 1885 | 27.8076 | 19.9106 | -37.1085 | 1.6533 | 60.1061 |
| intraday | 4537 | 10.031 | 19.6166 | -25.1404 | 0.6079 | 41.0403 |
| position | 551 | 56.8527 | 19.093 | -54.9309 | 3.1851 | 71.8693 |

By grade (median bps):

| grade | n | mfe_bps med | cost_bps med | mfe/cost med | frac mfe>cost % |
|---|---|---|---|---|---|
| A+ | 70 | 20.4756 | 19.8893 | 1.1908 | 57.1429 |
| A | 2491 | 16.2268 | 19.899 | 0.9855 | 49.7391 |
| B | 3570 | 13.9037 | 19.834 | 0.8115 | 46.9468 |
| - | 804 | 17.4113 | 19.4847 | 1.0383 | 50.6219 |
| V | 38 | 68.0067 | 15.9266 | 4.6175 | 76.3158 |

## RC-3 — Edge in basis points — scored-20 (reference)

| scope | n | mfe_bps med | cost_bps med | realized_bps med | mfe/cost med | frac mfe>cost % |
|---|---|---|---|---|---|---|
| GRID | 8387 | 13.7972 | 19.7884 | -26.5682 | 0.8429 | 49.2071 |
| swing | 1885 | 27.8076 | 19.9106 | -37.1085 | 1.6533 | 60.1061 |
| intraday | 5951 | 9.2674 | 19.0436 | -23.9 | 0.5504 | 43.6565 |
| position | 551 | 56.8527 | 19.093 | -54.9309 | 3.1851 | 71.8693 |

By grade (median bps):

| grade | n | mfe_bps med | cost_bps med | mfe/cost med | frac mfe>cost % |
|---|---|---|---|---|---|
| A+ | 83 | 20.9589 | 19.0255 | 1.1664 | 59.0361 |
| A | 2952 | 14.8969 | 19.8891 | 0.9165 | 50.1355 |
| B | 4361 | 12.3436 | 19.6133 | 0.7441 | 47.8101 |
| - | 946 | 15.2434 | 19.5412 | 0.97 | 50.4228 |
| V | 45 | 75.9971 | 14.1187 | 4.9841 | 80.0 |

## RC-4 — Stop-distance decile table + floor curve — scored-clean (primary)

> **Caveat.** First-order: removing tranches by stop-distance does NOT change the stop path (ratchet is signal-layer), but DOES change the equity path, the 1R campaign rail and the halt calendar -- faithful measurement is S-1's job. Null atr_exec rows are KEPT (cannot evaluate) and counted.

Null-atr tranches kept (unevaluable): 0.

**(a) Deciles of stop_dist/ATR:**

| decile | stop/ATR range | n | gross/unit | cost/unit | net/unit | Σ cell-R 1× | win % |
|---|---|---|---|---|---|---|---|
| 1 | [0.0018, 0.5857) | 698 | 1.8254 | 10.7177 | -8.8924 | -3085.6463 | 3.8682 |
| 2 | [0.5857, 0.8815) | 697 | 0.03 | 1.1944 | -1.1644 | -382.5073 | 9.6126 |
| 3 | [0.8815, 1.0335) | 697 | 0.2305 | 0.9239 | -0.6934 | -210.9657 | 12.6255 |
| 4 | [1.0335, 1.1471) | 697 | 0.1173 | 0.8325 | -0.7152 | -215.8245 | 16.6428 |
| 5 | [1.1471, 1.2553) | 697 | 0.0346 | 0.7898 | -0.7552 | -229.1994 | 20.8034 |
| 6 | [1.2553, 1.3677) | 698 | 0.2522 | 0.8126 | -0.5604 | -168.3969 | 14.4699 |
| 7 | [1.3677, 1.5042) | 697 | 0.0405 | 0.8069 | -0.7664 | -228.0143 | 17.2166 |
| 8 | [1.5042, 1.6781) | 697 | 0.1131 | 0.8057 | -0.6926 | -202.75 | 18.6514 |
| 9 | [1.6781, 1.9687) | 697 | 0.2144 | 0.8122 | -0.5979 | -177.4141 | 16.4993 |
| 10 | [1.9687, 7.4304) | 698 | 0.0831 | 0.7278 | -0.6446 | -193.0661 | 17.765 |

**(b) Floor curve** (remove tranches with stop/ATR < X, first-order):

| floor X | tranches removed | campaigns | Σ 0× | Σ 1× | Σ 2× | expectancy 1× |
|---|---|---|---|---|---|---|
| 0.30 | 361 | 2856 | 432.9983 | -2314.0478 | -5061.0939 | -0.8102 |
| 0.40 | 486 | 2854 | 428.3639 | -2138.714 | -4705.792 | -0.7494 |
| 0.50 | 610 | 2848 | 397.784 | -2035.0591 | -4467.9022 | -0.7146 |
| 0.60 | 717 | 2844 | 329.9354 | -1993.6299 | -4317.1951 | -0.701 |
| 0.75 | 998 | 2828 | 299.308 | -1841.4804 | -3982.2687 | -0.6512 |
| 1.00 | 1914 | 2699 | 269.643 | -1471.3737 | -3212.3903 | -0.5452 |
| 1.25 | 3451 | 2268 | 216.9775 | -973.7942 | -2164.5659 | -0.4294 |
| 1.50 | 4853 | 1592 | 121.945 | -582.0754 | -1286.0958 | -0.3656 |

## RC-4 — Stop-distance decile table + floor curve — scored-20 (reference)

Null-atr tranches kept (unevaluable): 0.

**(a) Deciles of stop_dist/ATR:**

| decile | stop/ATR range | n | gross/unit | cost/unit | net/unit | Σ cell-R 1× | win % |
|---|---|---|---|---|---|---|---|
| 1 | [0.0018, 0.5909) | 839 | 2.3414 | 10.8415 | -8.5002 | -3544.5717 | 9.7735 |
| 2 | [0.5909, 0.8917) | 839 | 0.0549 | 1.1392 | -1.0843 | -427.2041 | 10.3695 |
| 3 | [0.8917, 1.0472) | 838 | 0.2151 | 0.8803 | -0.6652 | -243.9643 | 13.9618 |
| 4 | [1.0472, 1.1673) | 839 | 0.1196 | 0.7744 | -0.6549 | -237.2357 | 16.9249 |
| 5 | [1.1673, 1.279) | 838 | -0.0208 | 0.7543 | -0.775 | -281.7276 | 18.7351 |
| 6 | [1.279, 1.4033) | 839 | 0.1788 | 0.7614 | -0.5827 | -211.948 | 15.1371 |
| 7 | [1.4033, 1.5467) | 839 | 0.0958 | 0.752 | -0.6563 | -232.6437 | 19.6663 |
| 8 | [1.5467, 1.7336) | 838 | 0.3153 | 0.7414 | -0.4261 | -149.684 | 18.6158 |
| 9 | [1.7336, 2.0279) | 839 | -0.0039 | 0.6559 | -0.6597 | -236.8493 | 16.8057 |
| 10 | [2.0279, 7.5339) | 839 | 0.0678 | 0.5997 | -0.5319 | -191.0809 | 18.7128 |

**(b) Floor curve** (remove tranches with stop/ATR < X, first-order):

| floor X | tranches removed | campaigns | Σ 0× | Σ 1× | Σ 2× | expectancy 1× |
|---|---|---|---|---|---|---|
| 0.30 | 430 | 3434 | 464.3433 | -2572.0524 | -5608.4481 | -0.749 |
| 0.40 | 572 | 3432 | 456.5959 | -2381.3413 | -5219.2786 | -0.6939 |
| 0.50 | 720 | 3426 | 426.3363 | -2264.2198 | -4954.7758 | -0.6609 |
| 0.60 | 856 | 3422 | 360.745 | -2203.609 | -4767.963 | -0.644 |
| 0.75 | 1177 | 3401 | 335.0951 | -2027.7996 | -4390.6943 | -0.5962 |
| 1.00 | 2219 | 3252 | 274.8418 | -1647.9625 | -3570.7668 | -0.5068 |
| 1.25 | 3970 | 2783 | 239.782 | -1082.9482 | -2405.6783 | -0.3891 |
| 1.50 | 5618 | 2021 | 151.8426 | -641.3403 | -1434.5231 | -0.3173 |

## RC-5 — Z1 filter / tilt (first-order) — scored-clean (primary)

> **Caveat.** First-order Z1 lever. Campaign zone = the initiating tranche's zone. Drop / half-size re-weights realized_r linearly (pnl scales with qty scales with size_r at fixed unit risk). Equity-path / rail / halt effects are S-1's job.

Z1-initiated campaigns: 2038 (70.8377% of campaigns).

| variant | campaigns | Σ 0× | Σ 1× | Σ 2× | expectancy 1× | 95% CI | win % | strip-best Σ 1× |
|---|---|---|---|---|---|---|---|---|
| neutral (live) | 2877 | 968.7735 | -5093.7846 | -11156.3427 | -1.7705 | [-2.0614, -1.5113] | 9.7671 | -5208.2365 |
| drop Z1-initiated | 839 | 156.4323 | -1204.1174 | -2564.6671 | -1.4352 | [-1.8528, -1.1042] | 10.4887 | -1226.6592 |
| half-size Z1-initiated | 2877 | 562.6029 | -3148.951 | -6860.5049 | -1.0945 | [-1.2728, -0.9366] | 9.7671 | -3206.177 |

First-order drop-Z1 Δ vs neutral (1×): **3889.6672** cell-R.

## RC-5 — Z1 filter / tilt (first-order) — scored-20 (reference)

Z1-initiated campaigns: 2411 (69.7627% of campaigns).

| variant | campaigns | Σ 0× | Σ 1× | Σ 2× | expectancy 1× | 95% CI | win % | strip-best Σ 1× |
|---|---|---|---|---|---|---|---|---|
| neutral (live) | 3456 | 1345.3095 | -5756.9093 | -12859.1281 | -1.6658 | [-2.0334, -1.3619] | 11.2847 | -5871.3612 |
| drop Z1-initiated | 1045 | 195.705 | -1300.1153 | -2795.9355 | -1.2441 | [-1.5984, -0.9624] | 11.6746 | -1326.5786 |
| half-size Z1-initiated | 3456 | 770.5072 | -3528.5123 | -7827.5318 | -1.021 | [-1.2215, -0.8492] | 11.2847 | -3585.7382 |

First-order drop-Z1 Δ vs neutral (1×): **4456.794** cell-R.

## RC-6 — Attempt-sequence census — scored-clean (primary)

> **Caveat.** Attempt = campaign opener within its direction-run (maximal same-cell same-direction run, journal time order). Cluster distance uses the attempt-1 opener's fill price and ATR. Expectancy is campaign cell-R. First-order counterfactual only.

Direction-runs: 2346. Attempts-per-run distribution: `{"1": 1935, "2": 318, "3": 70, "4": 19, "5": 4}`

**(b) By attempt number:**

| attempt | campaigns | Σ cell-R 1× | expectancy 1× | 95% CI | win % |
|---|---|---|---|---|---|
| 1 | 2346 | -4026.0386 | -1.7161 | [-2.0335, -1.4426] | 9.5908 |
| 2 | 411 | -876.8285 | -2.1334 | [-3.1753, -1.1668] | 10.7056 |
| 3 | 93 | -151.5285 | -1.6293 | [-2.1371, -1.1365] | 7.5269 |
| 4+ | 27 | -39.389 | -1.4589 | [-2.2545, -0.7115] | 18.5185 |

**(c) In-cluster share of attempts 2+:**

| k×ATR | attempts 2+ | evaluable | in-cluster | in-cluster % |
|---|---|---|---|---|
| 0.5 | 531 | 531 | 13 | 2.4482 |
| 1.0 | 531 | 531 | 24 | 4.5198 |
| 1.5 | 531 | 531 | 35 | 6.5913 |

**(d) Expectancy by attempt × cluster (k=1.0):**

| attempt | in-cluster n | in-cluster exp | out-cluster n | out-cluster exp |
|---|---|---|---|---|
| 1 | 2346 | -1.7161 | 0 |  |
| 2 | 21 | -2.345 | 390 | -2.122 |
| 3 | 3 | -2.6801 | 90 | -1.5943 |
| 4+ | 0 |  | 27 | -1.4589 |

**(e) Counterfactual: Σ cell-R of in-cluster attempts 4+ (what a 3-strike rule would remove, first-order):**

| k×ATR | campaigns | Σ cell-R 1× removed |
|---|---|---|
| 0.5 | 0 | 0.0 |
| 1.0 | 0 | 0.0 |
| 1.5 | 0 | 0.0 |

## RC-6 — Attempt-sequence census — scored-20 (reference)

Direction-runs: 2806. Attempts-per-run distribution: `{"1": 2308, "2": 379, "3": 91, "4": 23, "5": 5}`

**(b) By attempt number:**

| attempt | campaigns | Σ cell-R 1× | expectancy 1× | 95% CI | win % |
|---|---|---|---|---|---|
| 1 | 2806 | -4580.005 | -1.6322 | [-2.0737, -1.2887] | 11.1903 |
| 2 | 498 | -971.8546 | -1.9515 | [-2.8015, -1.1384] | 11.4458 |
| 3 | 119 | -162.8882 | -1.3688 | [-1.8088, -0.9473] | 10.9244 |
| 4+ | 33 | -42.1615 | -1.2776 | [-1.9449, -0.6666] | 18.1818 |

**(c) In-cluster share of attempts 2+:**

| k×ATR | attempts 2+ | evaluable | in-cluster | in-cluster % |
|---|---|---|---|---|
| 0.5 | 650 | 650 | 17 | 2.6154 |
| 1.0 | 650 | 650 | 29 | 4.4615 |
| 1.5 | 650 | 650 | 43 | 6.6154 |

**(d) Expectancy by attempt × cluster (k=1.0):**

| attempt | in-cluster n | in-cluster exp | out-cluster n | out-cluster exp |
|---|---|---|---|---|
| 1 | 2806 | -1.6322 | 0 |  |
| 2 | 25 | -1.9369 | 473 | -1.9523 |
| 3 | 4 | -2.3014 | 115 | -1.3364 |
| 4+ | 0 |  | 33 | -1.2776 |

**(e) Counterfactual: Σ cell-R of in-cluster attempts 4+ (what a 3-strike rule would remove, first-order):**

| k×ATR | campaigns | Σ cell-R 1× removed |
|---|---|---|
| 0.5 | 0 | 0.0 |
| 1.0 | 0 | 0.0 |
| 1.5 | 0 | 0.0 |

## Prediction scorecard (contract §7)

| # | prediction | prior | falsified if | verdict |
|---|---|---|---|---|
| P-RC1a | Re-entries are >=70% of ADD_FILL rows | 75% | < 70% | **CONFIRMED** |
| P-RC1b | True-add per-unit gross (0x) >= re-entry per-unit gross (0x) | 55% | true_add < re_entry | **FALSIFIED** |
| P-RC1c | Majority of top-10 campaigns are serial (max_concurrent<3) | 60% | >=5 of 10 have max_concurrent = 3 | **FALSIFIED** |
| P-RC2 | No cell besides ZECUSDT_intraday crossed zero | 80% | any other zero-crossing | **CONFIRMED** |
| P-RC3 | Median mfe_bps>cost_bps on swing; median mfe_bps<cost_bps on intraday | 70% | either half fails | **CONFIRMED** |
| P-RC4 | Net/unit by stop-distance decile is non-monotone; max in 0.75-1.50 ATR band | 60% | max outside band or monotone | **CONFIRMED** |
| P-RC5 | Z1-drop improves scored-clean 1x by >= +1500 cell-R first-order | 65% | < +1500 | **CONFIRMED** |
| P-RC6 | Expectancy decays monotonically in attempt number (1>2>3) | 55% | any inversion | **FALSIFIED** |

- **P-RC1a — CONFIRMED.** Evidence: `{"re_entry_pct": 77.301, "add_fills_total": 4335}`
- **P-RC1b — FALSIFIED.** Evidence: `{"true_add_per_unit_gross": 0.2341, "re_entry_per_unit_gross": 0.4325}`
- **P-RC1c — FALSIFIED.** Evidence: `{"serial_count": 5, "stacked_count": 5}`
- **P-RC2 — CONFIRMED.** Evidence: `{"other_crossers": []}`
- **P-RC3 — CONFIRMED.** Evidence: `{"swing_mfe_med": 27.8076, "swing_cost_med": 19.9106, "intraday_mfe_med": 10.031, "intraday_cost_med": 19.6166}`
- **P-RC4 — CONFIRMED.** Evidence: `{"argmax_decile": 6, "argmax_edge_lo": 1.2553, "argmax_edge_hi": 1.3677, "monotone": false, "net_per_unit_by_decile": [-8.8924, -1.1644, -0.6934, -0.7152, -0.7552, -0.5604, -0.7664, -0.6926, -0.5979, -0.6446]}`
- **P-RC5 — CONFIRMED.** Evidence: `{"drop_z1_delta_1x": 3889.6672}`
- **P-RC6 — FALSIFIED.** Evidence: `{"exp_att1": -1.7161, "exp_att2": -2.1334, "exp_att3": -1.6293}`
