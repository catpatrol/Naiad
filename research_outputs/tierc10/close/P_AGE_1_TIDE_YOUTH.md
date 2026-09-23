# P-AGE-1 · tide-youth (Tier-E tables)

**TIER-E MEASUREMENT — UNSCORED, GATES NOTHING.** A SELECTION, not a result. In-sample. P-AGE-1 has no registration, no verdict, no p, no CI and no BH bar. m selections: 4 (P_AGE_1_TIDE_YOUTH band rows) · 8 (P_AGE_1_BAR_BANDS band rows) · 0 (P_AGE_1_EDGES, an edge table).

Contract of record: `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:113`: "P-AGE-1 (tide-youth), boundary-fade, regime-prior: Tier-E tables only."

## Definition (an executor reading, no new pin)

EXECUTOR READING, NO NEW PIN: tide-youth = tierc7_lab_regime.tide_streak(sym)[1] (the run length of sign(e89 - e316) on the 4h frame) at the campaign's ENTRY bar, counted from TIDE_WARM_BARS = 316. It is banded by STREAK_BAND_QUANTILES = (0.25, 0.5, 0.75) of the panel-pooled bar distribution into STREAK_LABELS = ('B1 YOUNG tide', 'B2 EARLY tide', 'B3 MATURE tide', 'B4 OLD tide') (B1 = 'B1 YOUNG tide'). The edges are TRAILING: causal, expanding and panel-pooled over the bars with open_ms <= the entry bar, inclusive. The prefix floor is n >= RC.PROVISIONAL_MIN_N = 30. This is exactly TC9's TC7-g (tierc9.tc7g_tables).

Book: the v6 control, `tierc7_lab_regime.books(lo, hi)['v6']`. It equals `research_outputs/tierc10/panel/control_journal.parquet` exactly on asset, entry_ms, direction, exit_ms, exit_reason, net_r (F-AGE-BOOK).

## Corridor and as-of

- panel CLASSIC5 (BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT), lens 4h
- corridor 2019-09-08T16:00:00Z → 2026-09-21T16:00:00Z (2570.0 d), substrate tc10_20260921
- as_of_last_closed_4h = 2026-09-21T16:00:00Z, which equals PROGRESS.json as_of_of_record (2026-09-21T16:00:00Z)

## Table 1: the v6 book by tide-youth band, TRAILING edges (`P_AGE_1_TIDE_YOUTH.parquet`)

| band | n | assets | net R | expectancy R | win % | max DD R | top-decile share % | best R | strip-best net R | share of card net R % | provisional | left-censored | streak bars at entry min / median / max |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|:-:|---:|---:|
| B1 YOUNG tide | 25 | 5 | +11.7692 | +0.4708 | 52.0 | 6.4292 | 65.1 | 9.1430 | +2.6262 | 28.2 | yes | 0 | 2 / 53.0 / 92 |
| B2 EARLY tide | 60 | 5 | +34.6369 | +0.5773 | 40.0 | 9.1230 | 71.6 | 25.0605 | +9.5764 | 83.0 | no | 2 | 89 / 142.0 / 252 |
| B3 MATURE tide | 56 | 5 | +17.9938 | +0.3213 | 35.7 | 8.7240 | 58.7 | 8.7450 | +9.2488 | 43.1 | no | 0 | 98 / 298.5 / 474 |
| B4 OLD tide | 59 | 5 | -22.6566 | -0.3840 | 20.3 | 28.1695 | 76.2 | 3.6422 | -26.2987 | -54.3 | no | 2 | 216 / 549.0 / 1246 |
| ALL (the whole book) | 200 | 5 | +41.7433 | +0.2087 | 34.5 | 27.4075 | 72.6 | 25.0605 | +16.6829 | 100.0 | no | 4 | 2 / 249.0 / 1246 |

`provisional` means n < RC.PROVISIONAL_MIN_N = 30 (the lineage's law). Band n's sum to 200; the ALL row holds 200 (F-AGE-WHOLE).

**D15 trio: GATES NOTHING. The v6 rows are self-paired against the v6 book restricted to the same band, so delta = 0 and the tail ratio = 1 by construction (the lab asserts this).**

| band | paired_delta_expectancy_r | tail_exit_ratio | max_single_trade_delta_share |
|---|---:|---:|---:|
| B1 YOUNG tide | 0.0000 | 1.0000 | — |
| B2 EARLY tide | 0.0000 | 1.0000 | — |
| B3 MATURE tide | 0.0000 | 1.0000 | — |
| B4 OLD tide | 0.0000 | 1.0000 | — |
| ALL (the whole book) | 0.0000 | 1.0000 | — |

## Look-ahead size: campaign counts under trailing edges vs whole-corridor edges

| band | n, TRAILING (of record) | n, WHOLE-CORRIDOR (TC7 original, look-ahead) |
|---|---:|---:|
| B1 YOUNG tide | 25 | 23 |
| B2 EARLY tide | 60 | 57 |
| B3 MATURE tide | 56 | 62 |
| B4 OLD tide | 59 | 58 |

## Table 2: the bar distribution (`P_AGE_1_BAR_BANDS.parquet`)

| basis | band | edge lo (bars) | edge hi (bars) | units | unit | share % | median streak (bars) | median streak (days) | n v6 campaigns (whole-corridor edges) | left-censored |
|---|---|---:|---:|---:|---|---:|---:|---:|---:|---:|
| bar-pooled — USED | B1 YOUNG tide | — | 88.0 | 17331 | panel 4h bars | 24.94 | 40.0 | 6.67 | 23 | 0 |
| bar-pooled — USED | B2 EARLY tide | 88.0 | 206.0 | 17338 | panel 4h bars | 24.95 | 142.0 | 23.67 | 57 | 2 |
| bar-pooled — USED | B3 MATURE tide | 206.0 | 396.0 | 17433 | panel 4h bars | 25.08 | 285.0 | 47.50 | 62 | 0 |
| bar-pooled — USED | B4 OLD tide | 396.0 | — | 17398 | panel 4h bars | 25.03 | 568.0 | 94.67 | 58 | 2 |
| episode-pooled — NOT USED (length-bias contrast) | B1 YOUNG tide | — | 78.0 | 57 | streak episodes | 24.89 | 34.0 | 5.67 | — | — |
| episode-pooled — NOT USED (length-bias contrast) | B2 EARLY tide | 78.0 | 223.0 | 56 | streak episodes | 24.45 | 135.5 | 22.58 | — | — |
| episode-pooled — NOT USED (length-bias contrast) | B3 MATURE tide | 223.0 | 430.0 | 58 | streak episodes | 25.33 | 300.5 | 50.08 | — | — |
| episode-pooled — NOT USED (length-bias contrast) | B4 OLD tide | 430.0 | — | 58 | streak episodes | 25.33 | 657.5 | 109.58 | — | — |

bar-pooled quartiles [88.0, 206.0, 396.0] against episode-pooled [78.0, 223.0, 430.0]. The bar sampling gives a long streak one vote per bar; the episode sampling gives it one. The bar basis is the one USED.

Columns dropped: ['n_campaigns_hybrid']. The hybrid is not printed.

## Table 3: edge evolution (`P_AGE_1_EDGES.parquet`)

| as of | streak edges, TRAILING | streak edges, WHOLE CORRIDOR | vol_rel edges, trailing | vol_rel edges, whole corridor |
|---|---|---|---|---|
| 2020-01-01 | [35.0, 107.0, 199.5] | [88.0, 206.0, 396.0] | [0.677507, 1.109087] | [0.841622, 1.151783] |
| 2021-01-01 | [86.0, 189.0, 363.5] | [88.0, 206.0, 396.0] | [0.875893, 1.207068] | [0.841622, 1.151783] |
| 2022-01-01 | [97.0, 233.0, 472.0] | [88.0, 206.0, 396.0] | [0.843222, 1.192938] | [0.841622, 1.151783] |
| 2023-01-01 | [102.0, 237.0, 453.0] | [88.0, 206.0, 396.0] | [0.834163, 1.140123] | [0.841622, 1.151783] |
| 2024-01-01 | [93.0, 217.0, 402.0] | [88.0, 206.0, 396.0] | [0.836517, 1.163285] | [0.841622, 1.151783] |
| 2025-01-01 | [89.0, 208.0, 402.0] | [88.0, 206.0, 396.0] | [0.843263, 1.168767] | [0.841622, 1.151783] |
| 2026-01-01 | [90.0, 210.0, 404.0] | [88.0, 206.0, 396.0] | [0.847949, 1.160251] | [0.841622, 1.151783] |

## What these tables are not

- They are not a registration, a score or a verdict. No p, CI or BH bar is computed, and no registration or its verdict was read.
- They are not a filter. No campaign is dropped, and every band is printed whole, including the provisional ones.
- They are not out of sample. The book, the bands and the edges all come from the same corridor.
- The lab's hybrid rows are not printed. Only card v6 is TC10's control.
- The dropped verdict/p/ci/clears_bh_bar columns: P_AGE_1_TIDE_YOUTH: none; P_AGE_1_EDGES: none; P_AGE_1_BAR_BANDS: none.

## Provenance

- `P_AGE_1_TIDE_YOUTH.parquet` content sha256 3fd85b3b94b3f23bf1881783061413746a41a4d3ea2284df06dca9a27c78dc75, 5 rows
- `P_AGE_1_BAR_BANDS.parquet` content sha256 89dad4fb277537d753c6f2e814422a7673b58f7395b0c2818f2813761df3013b, 8 rows
- `P_AGE_1_EDGES.parquet` content sha256 1770355966bf4c8b85e52c2c8c9593fcfeb57f9c81c252bcc814720f5403863b, 7 rows
- control_journal.parquet sha256: fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c
- scripts/tierc7_lab_regime.py sha256: 4d19cf0095ebf2593b3008caf9c9af032a75515dda8507da5154308e977682a5
- scripts/tierc9.py sha256: 663eef3107909221a6a651343363bad5c7d7730dd9adb92495d3f1e262c5b3c3
- scripts/tierc10_panel.py sha256: 40b660cdc943a947f199f2e59f38bfbda04866b44191506de2298d8474d79b0e
- scripts/tierc10_close_p_age_1_tide_youth.py sha256: 2995c27cc413158acb2cf32c774acaea51bc2f4778a9e66e25fe1b2f66dc353a
