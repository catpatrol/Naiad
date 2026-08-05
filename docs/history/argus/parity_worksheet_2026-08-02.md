# PARITY WORKSHEET — analytics/ vs the chart

**Generated** 2026-08-02T22:50:58Z · `scripts/parity_worksheet.py`
**ANALYTICS_VERSION** `1.1.0` · **analytics_sha** `a7ff1911848bb30561e477186dc62ed1a4ff3daf39bfe9d42371f3353815e046`

## What to do with this sheet

1. Open TradingView. For each row, load the chart named in the **Chart** column — the canonical form is `BINANCE:<SYM>USDT.P`, the perpetual, **not** the spot pair. A spot chart will disagree and the disagreement will mean nothing.
2. **Set the chart timezone to UTC.** Everything below is UTC. A chart in local time reads a different candle and produces a false mismatch.
3. Go to the exact candle named in the **As-of (UTC)** column. Every row is the value at the CLOSE of that candle. Do not read the candle currently forming.
4. Write what the chart says into **Operator reads**. Leave it blank if you did not check that row — a blank is honest, a guess is not.
5. If you have your own RVWAP script, put its number in **Your script** so a three-way disagreement is visible.
6. Send the sheet back with the columns filled. **Nothing in `analytics/` is adopted until this comes back.** A row that disagrees is a finding, not a rounding argument — bring it back as it is.

### Settings that must match, or the comparison is void

| setting | value |
|---|---|
| Chart | `BINANCE:<SYM>USDT.P` (perpetual) |
| Timezone | UTC |
| Candles | **closed only** — never the forming one |
| RVWAP indicator | TradingView's official **Rolling VWAP** |
| RVWAP window | **Fixed**, set to the days in the row (7 / 30 / 90 / 365) |
| RVWAP source | `hlc3` |
| RVWAP bands | ×1 (one standard deviation) |
| RSI | length 14, Wilder smoothing, source close |
| ATR | length 14, Wilder smoothing |

> **Anchored-band variance — TO BE CONFIRMED BY READING.** Our anchored VWAP bands reuse the same volume-weighted *population* variance as the rolling form. That is a reasoned inference from shared TradingView band machinery, **not read from source**. It is not pinned and must not be cited as pinned. If you can read the indicator source, this is the single most valuable thing to confirm.

> **Closed-bar note (Amendment FAN8).** Resampled rows (4h, 1d) drop the still-forming bucket, so they show the last FINISHED period. Mid-candle, a chart shows the forming one — those two SHOULD differ, and that is not a parity failure. Compare at the named as-of candle.

## A. Current-bar rows (24)

| # | Asset | Chart | Measure | Convention | As-of (UTC) | Ours | Operator reads | Your script |
|---:|---|---|---|---|---|---:|---|---|
| 1 | BTCUSDT | `BINANCE:BTCUSDT.P` | close (1h) | last closed 1h candle close | 2026-08-02 19:00 UTC | **63,432.90** |  |  |
| 2 | BTCUSDT | `BINANCE:BTCUSDT.P` | RVWAP 7d | TradingView "Rolling VWAP", fixed 7 days, src hlc3 | 2026-08-02 19:00 UTC | **63,948.81** |  |  |
| 3 | BTCUSDT | `BINANCE:BTCUSDT.P` | RVWAP 30d | TradingView "Rolling VWAP", fixed 30 days, src hlc3 | 2026-08-02 19:00 UTC | **63,923.22** |  |  |
| 4 | BTCUSDT | `BINANCE:BTCUSDT.P` | RVWAP 90d | TradingView "Rolling VWAP", fixed 90 days, src hlc3 | 2026-08-02 19:00 UTC | **66,812.95** |  |  |
| 5 | BTCUSDT | `BINANCE:BTCUSDT.P` | RVWAP 365d | TradingView "Rolling VWAP", fixed 365 days, src hlc3 | 2026-08-02 19:00 UTC | **83,716.90** |  |  |
| 6 | BTCUSDT | `BINANCE:BTCUSDT.P` | RSI(14) 1h | native 1h, Wilder | 2026-08-02 19:00 UTC | **60.8375** |  |  |
| 7 | BTCUSDT | `BINANCE:BTCUSDT.P` | RSI(14) 4h | resampled 1h->4h, CLOSED buckets only | 2026-08-02 19:00 UTC | **49.1647** |  |  |
| 8 | BTCUSDT | `BINANCE:BTCUSDT.P` | ATR(14) 1d | resampled 1h->1d, CLOSED buckets only | 2026-08-02 19:00 UTC | **1,699.80** |  |  |
| 9 | ETHUSDT | `BINANCE:ETHUSDT.P` | close (1h) | last closed 1h candle close | 2026-08-02 19:00 UTC | **1,881.39** |  |  |
| 10 | ETHUSDT | `BINANCE:ETHUSDT.P` | RVWAP 7d | TradingView "Rolling VWAP", fixed 7 days, src hlc3 | 2026-08-02 19:00 UTC | **1,901.77** |  |  |
| 11 | ETHUSDT | `BINANCE:ETHUSDT.P` | RVWAP 30d | TradingView "Rolling VWAP", fixed 30 days, src hlc3 | 2026-08-02 19:00 UTC | **1,850.50** |  |  |
| 12 | ETHUSDT | `BINANCE:ETHUSDT.P` | RVWAP 90d | TradingView "Rolling VWAP", fixed 90 days, src hlc3 | 2026-08-02 19:00 UTC | **1,860.30** |  |  |
| 13 | ETHUSDT | `BINANCE:ETHUSDT.P` | RVWAP 365d | TradingView "Rolling VWAP", fixed 365 days, src hlc3 | 2026-08-02 19:00 UTC | **2,845.01** |  |  |
| 14 | ETHUSDT | `BINANCE:ETHUSDT.P` | RSI(14) 1h | native 1h, Wilder | 2026-08-02 19:00 UTC | **62.8401** |  |  |
| 15 | ETHUSDT | `BINANCE:ETHUSDT.P` | RSI(14) 4h | resampled 1h->4h, CLOSED buckets only | 2026-08-02 19:00 UTC | **50.8491** |  |  |
| 16 | ETHUSDT | `BINANCE:ETHUSDT.P` | ATR(14) 1d | resampled 1h->1d, CLOSED buckets only | 2026-08-02 19:00 UTC | **68.37** |  |  |
| 17 | SOLUSDT | `BINANCE:SOLUSDT.P` | close (1h) | last closed 1h candle close | 2026-08-02 19:00 UTC | **73.68** |  |  |
| 18 | SOLUSDT | `BINANCE:SOLUSDT.P` | RVWAP 7d | TradingView "Rolling VWAP", fixed 7 days, src hlc3 | 2026-08-02 19:00 UTC | **73.88** |  |  |
| 19 | SOLUSDT | `BINANCE:SOLUSDT.P` | RVWAP 30d | TradingView "Rolling VWAP", fixed 30 days, src hlc3 | 2026-08-02 19:00 UTC | **76.86** |  |  |
| 20 | SOLUSDT | `BINANCE:SOLUSDT.P` | RVWAP 90d | TradingView "Rolling VWAP", fixed 90 days, src hlc3 | 2026-08-02 19:00 UTC | **77.04** |  |  |
| 21 | SOLUSDT | `BINANCE:SOLUSDT.P` | RVWAP 365d | TradingView "Rolling VWAP", fixed 365 days, src hlc3 | 2026-08-02 19:00 UTC | **129.52** |  |  |
| 22 | SOLUSDT | `BINANCE:SOLUSDT.P` | RSI(14) 1h | native 1h, Wilder | 2026-08-02 19:00 UTC | **64.2885** |  |  |
| 23 | SOLUSDT | `BINANCE:SOLUSDT.P` | RSI(14) 4h | resampled 1h->4h, CLOSED buckets only | 2026-08-02 19:00 UTC | **52.7473** |  |  |
| 24 | SOLUSDT | `BINANCE:SOLUSDT.P` | ATR(14) 1d | resampled 1h->1d, CLOSED buckets only | 2026-08-02 19:00 UTC | **2.72** |  |  |

## B. Historical rows (4) — about 30 days back

These exist to catch an error that only shows up away from the right edge. Same instructions; scroll back to the named candle.

| # | Asset | Chart | Measure | Convention | As-of (UTC) | Ours | Operator reads | Your script |
|---:|---|---|---|---|---|---:|---|---|
| 25 | BTCUSDT | `BINANCE:BTCUSDT.P` | close (1h) | last closed 1h candle close | 2026-07-03 19:00 UTC | **62,178.40** |  |  |
| 26 | BTCUSDT | `BINANCE:BTCUSDT.P` | RVWAP 7d | TradingView "Rolling VWAP", fixed 7 days, src hlc3 | 2026-07-03 19:00 UTC | **60,060.63** |  |  |
| 27 | BTCUSDT | `BINANCE:BTCUSDT.P` | RSI(14) 1h | native 1h, Wilder | 2026-07-03 19:00 UTC | **64.1459** |  |  |
| 28 | BTCUSDT | `BINANCE:BTCUSDT.P` | ATR(14) 1d | resampled 1h->1d, CLOSED buckets only | 2026-07-03 19:00 UTC | **2,347.16** |  |  |

## C. Band geometry spot-check (RVWAP 7d, ×1)

| Asset | As-of (UTC) | Upper ×1 (ours) | Lower ×1 (ours) | Operator reads upper | Operator reads lower |
|---|---|---:|---:|---|---|
| BTCUSDT | 2026-08-02 19:00 UTC | **64,719.35** | **63,178.28** |  |  |
| ETHUSDT | 2026-08-02 19:00 UTC | **1,933.43** | **1,870.10** |  |  |
| SOLUSDT | 2026-08-02 19:00 UTC | **75.17** | **72.58** |  |  |

---

**Rows to read: 24 current + 4 historical = 28**, plus 3 band pairs.

**Adoption remains gated on this sheet coming back.** No partial adoption: CENSUS-2b, CENSUS-1d and H-RVX all wait behind it.
