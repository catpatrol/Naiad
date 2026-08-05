# BUILDER'S REPORT — ARGUS lane — PARITY RUN, SETUP A (oscillator pack)

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Branch:** `v12-v1-census`
**Source:** operator TradingView readings, `BINANCE:<SYM>USDT.P`, chart TZ = UTC, closed candles

> **MEASUREMENT CYCLE.** No recipe was changed, no tolerance applied, no value
> tuned toward agreement, and **no pass/fail is emitted**. What counts as a match
> is the reviewer's call.

---

## 0 · HEADLINE

| | |
|---|---|
| Raw bars | **36 / 36 fields IDENTICAL** across all 9 candles |
| Indicator comparisons | **72 / 72 agree** at the operator's displayed precision |
| Largest absolute delta | **0.0491** (A8 ATR, on 798.6) |
| Largest relative delta | **0.838%** (A7 AO, on −0.33 — a tiny denominator, absolute delta 0.0028) |
| Disagreements | **none** |

Every delta is a rounding artifact of TradingView's fixed display precision.

---

## 1 · ENVIRONMENT GATE

branch `v12-v1-census` · pwd contains `\Users\` + OneDrive · `analytics/` and
`scripts/` present → **PASS**. HEAD at start `4e0f253` (reported, never gated).

---

## 2 · STEP 1 — DATA SUFFICIENCY

Wall clock at run: **2026-08-03 21:38:24 UTC**. Several requested candles were
newer than the cycle-1 probe's last bar (2026-08-02 21:34 UTC), so 1h klines were
topped up through the existing loader (`engine.data.backfill_klines`, which
already clamps to the last CLOSED bar). **`engine/` was not modified.**

| symbol | rows | first bar UTC | last bar UTC |
|---|---|---|---|
| BTCUSDT | 60,508 | 2019-09-08 17:00 | **2026-08-03 20:00** |
| ETHUSDT | 58,598 | 2019-11-27 07:00 | **2026-08-03 20:00** |
| SOLUSDT | 51,590 | 2020-09-14 07:00 | **2026-08-03 20:00** |

The 20:00 1h bar is what makes the 16:00–20:00 4h bucket *provably closed* — it
sits in a strictly later bucket, which is the emission condition.

| id | symbol | tf | candle UTC | present | source |
|---|---|---|---|---|---|
| A1 | BTCUSDT | 1h | 2026-08-03T19:00Z | YES | native 1h |
| A2 | BTCUSDT | 4h | 2026-08-03T16:00Z | YES | resampled 1h→4h |
| A3 | BTCUSDT | 12h | 2026-08-03T00:00Z | YES | resampled 1h→12h |
| A4 | BTCUSDT | 1d | 2026-08-02T00:00Z | YES | resampled 1h→1d |
| A5 | ETHUSDT | 4h | 2026-08-03T16:00Z | YES | resampled 1h→4h |
| A6 | ETHUSDT | 1d | 2026-08-02T00:00Z | YES | resampled 1h→1d |
| A7 | SOLUSDT | 4h | 2026-08-03T16:00Z | YES | resampled 1h→4h |
| A8 | BTCUSDT | 4h | 2026-06-30T20:00Z | YES | resampled 1h→4h |
| A9 | BTCUSDT | 1d | 2026-07-01T00:00Z | YES | resampled 1h→1d |

**All 9 present. No computation ran on an absent bar.**

---

## 3 · STEP 2 — RAW BAR CHECK (the discriminator)

Run **before** any indicator, because every indicator inherits a bar difference
and the cause would then be the data, not the recipes.

| id | field | ours | operator | delta |
|---|---|---|---|---|
| A1 | O/H/L/C | 63835.6 / 64058.8 / 63807.3 / 63836.9 | identical | 0 / 0 / 0 / 0 |
| A2 | O/H/L/C | 63659.5 / 64058.8 / 63626.2 / 63836.9 | identical | 0 / 0 / 0 / 0 |
| A3 | O/H/L/C | 63550.0 / 63575.6 / 62268.2 / 62534.1 | identical | 0 / 0 / 0 / 0 |
| A4 | O/H/L/C | 62792.3 / 63779.0 / 62782.3 / 63550.0 | identical | 0 / 0 / 0 / 0 |
| A5 | O/H/L/C | 1862.54 / 1875.98 / 1860.74 / 1869.26 | identical | 0 / 0 / 0 / 0 |
| A6 | O/H/L/C | 1844.17 / 1898.50 / 1843.03 / 1884.37 | identical | 0 / 0 / 0 / 0 |
| A7 | O/H/L/C | 73.58 / 74.27 / 73.20 / 73.99 | identical | 0 / 0 / 0 / 0 |
| A8 | O/H/L/C | 58794.0 / 58850.0 / 58472.3 / 58605.4 | identical | 0 / 0 / 0 / 0 |
| A9 | O/H/L/C | 58605.4 / 61322.0 / 57758.6 / 59999.6 | identical | 0 / 0 / 0 / 0 |

**36 of 36 fields identical to the full stored precision.** `exact_candle_match`
= YES on all nine.

### Why this row matters beyond parity

**Eight of the nine candles are RESAMPLED from 1h.** They match TradingView's own
aggregation exactly — bucket boundaries, first/max/min/last, and the closed-bar
emission rule. This is **the first external check `resample_ohlcv` has ever
had**, and it covers the function that finding F-1R-A rewrote and that D-3 later
routed `daily_brief.py` through.

---

## 4 · STEP 3 — 72 COMPARISONS

9 candles × 8 measures. Full table with per-row deltas, full precision, rounded
value, evaluated bar and `exact_candle_match` is in
`PARITY_SETUP_A_2026-08-03.json`.

**Agreeing at the operator's displayed precision: 72 / 72.**

Distribution of |delta| as a share of the operator's value:

| band | count |
|---|---|
| < 0.01% | 22 |
| 0.01 – 0.05% | 36 |
| 0.05 – 0.10% | 11 |
| 0.10 – 1.00% | 3 |
| ≥ 1.00% | **0** |

The three above 0.10% are A7 ATR (0.251%, on 0.93), A7 AO (0.838%, on −0.33) and
A7 macd_hist (0.084%) — all SOLUSDT rows where the operator's displayed value has
only two decimals against a small magnitude, so one display digit is worth a
large percentage. Their **absolute** deltas are 0.0023, 0.0028 and 0.0001.

---

## 5 · STEP 4 — TARGETED NOTES

### 4.1 ATR — the flagged candidate discrepancy is NOT a recipe finding

| | |
|---|---|
| A4 ours, full precision | **1649.577820** |
| A4 rounded to 1 dp | **1649.6** |
| operator | **1649.6** |
| verdict | **MATCH** |

- **Last input bar: the 2026-08-02 daily bar.** `exact_candle_match = True`.
- **The 2026-08-03 daily bucket is not emitted at all** — no 1h bar exists in a
  later bucket, so the forming daily bar cannot reach the calculation. Excluded
  by construction, not by a filter.
- Daily buckets emitted, last three: `2026-07-31 · 2026-08-01 · 2026-08-02`.

**Where ~1,700 came from:**

```
ATR14 as-of 2026-08-01  = 1,699.7992     <- the earlier builder figure
ATR14 as-of 2026-08-02  = 1,649.5778     <- A4, matches the operator
```

The ~3% gap is **a different as-of bar, not a different recipe.** 1,699.80 was
ATR at the last closed daily bar when that capture ran; the operator read the
Aug-02 bar. Same Wilder recipe, one bar apart. **No recipe finding to report.**

### 4.2 StochRSI — first external test since the F-2R-A repair

Warm-up: `rsi_length + stoch_length + k + d − 3` = 14+14+3+3−3 = **31 bars of the
evaluated timeframe**, exactly as CONVENTIONS records.

| id | tf | bars available | warm-up | %K ours | %D ours | operator %K / %D |
|---|---|---|---|---|---|---|
| A1 | 1h | 60,508 | 31 | 88.8450 | 87.6146 | 88.85 / 87.61 |
| A2 | 4h | 15,127 | 31 | 77.4547 | 57.6477 | 77.45 / 57.65 |
| A3 | 12h | 5,042 | 31 | 19.8918 | 15.4934 | 19.89 / 15.49 |
| A4 | 1d | 2,521 | 31 | 7.2648 | 11.0919 | 7.26 / 11.09 |
| A5 | 4h | 14,650 | 31 | 66.7949 | 54.4700 | 66.79 / 54.47 |
| A6 | 1d | 2,441 | 31 | 9.3042 | 11.9985 | 9.30 / 12.00 |
| A7 | 4h | 12,898 | 31 | 86.0955 | 74.1309 | 86.10 / 74.13 |
| A8 | 4h | 15,127 | 31 | 18.3389 | 11.8657 | 18.34 / 11.87 |
| A9 | 1d | 2,521 | 31 | 32.7373 | 19.6413 | 32.74 / 19.64 |

Every timeframe is far past warm-up. **All 18 values finite and matching.**
Before F-2R-A every one of them was NaN — this is the strongest available
evidence the repair is correct, because it agrees with an independent
implementation on nine candles across four timeframes and three assets.

### 4.3 Resample cross-check

| identity | ours | holds |
|---|---|---|
| A2 close == A1 close (4h 16:00–20:00 and 1h 19:00–20:00 both end 20:00) | 63,836.9000 == 63,836.9000 | **YES** |
| A3 open == A4 close | 63,550.0000 == 63,550.0000 | **YES** |

Both hold exactly, matching the operator's readings.

---

## 6 · FILE DISPOSITION

| file | disposition | why | tracked | pushed | fixture |
|---|---|---|---|---|---|
| `<cache>/klines/BTCUSDT_1h.parquet` | TOPPED UP | needed 2026-08-03 candles | no (estate) | no | — |
| `<cache>/klines/ETHUSDT_1h.parquet` | TOPPED UP | same | no (estate) | no | — |
| `<cache>/klines/SOLUSDT_1h.parquet` | TOPPED UP | same | no (estate) | no | — |
| `engine/data.py` | **UNTOUCHED** | DO-NOT-MODIFY; called only | yes | yes | — |
| `analytics/*` | **UNTOUCHED** | measurement cycle — no recipe changed | yes | yes | F-AN-* |
| `scripts/parity_check.py` | **UNTOUCHED** | used as built | yes | yes | — |
| `exchange/reports/PARITY_SETUP_A_2026-08-03.json` | NEW | full 72-row record | yes | yes | — |
| `exchange/reports/BUILDERS_REPORT_…_PARITY_A.md` | NEW | this file | yes | yes | — |
| `exchange/reports/SESSION_SUMMARY_…_PARITY_A.md` | NEW | decision artifact | yes | yes | — |

**No source file was modified in this cycle.** The only writes were estate
top-up (uncommitted, outside the repo) and the exchange artifacts.

---

## 7 · PROVENANCE

| | |
|---|---|
| `ANALYTICS_VERSION` | **1.3.0** |
| `analytics_sha()` | `da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731` |
| `rules_version` | 2.0.0 |
| parity JSON | `PARITY_SETUP_A_2026-08-03.json`, 40,559 B |

---

## 8 · WHAT THIS CERTIFIES, AND WHAT IT DOES NOT

**Certifies, on these nine candles:** RSI(14), StochRSI %K/%D, MACD line/signal/
histogram, Awesome Oscillator, ATR(14) — and `resample_ohlcv` against
TradingView's own aggregation on real bars.

**Does NOT certify:** **Setup B, the VWAP/volume pack** — rolling VWAP, the σ
bands, windowed volume profiles, POC/VAH/VAL, LVNs, VA nesting. Those carry the
recipes most likely to diverge (the population-variance RVWAP and the
uniform-spread profile approximation), and none of them was exercised here.

**Adoption does not open on Setup A alone.** The `PARITY NOT CERTIFIED` banner
stays until Setup B is returned and matched.

---

## 9 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No engine change.
No forward scoring. No fitted weights. No estate mutation beyond an additive
kline top-up through the sanctioned loader.

Confluence scores measure **agreement between tools**, not edge. R:R measures
**geometry**, not probability.

— HEPHAESTUS, 2026-08-03
