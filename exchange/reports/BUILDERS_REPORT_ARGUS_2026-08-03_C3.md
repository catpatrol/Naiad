# BUILDER'S REPORT — ARGUS lane — CYCLE 3 (stages A–D)

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Branch:** `v12-v1-census`
**Scope valve EXERCISED at end of stage D.** Stages E–G → cycle 4.

---

## 0 · GATE AND STATUS

branch `v12-v1-census` · pwd contains `\Users\` + OneDrive · `analytics/`
`scripts/` present → **PASS**. HEAD at start `5c7dd7f`.

Suite **230 passed / 1 skipped**. `analytics` **1.3.0** · `rules_version` 2.0.0 ·
`schema_version` 2.1.0. **PARITY NOT CERTIFIED — nothing adopted.**

---

## 1 · STAGE A — PARITY, BOTH SETUPS

### Data sufficiency

Wall clock 2026-08-03 21:50 UTC. 1h klines topped up via
`engine.data.backfill_klines` (self-clamping to the last closed bar); `engine/`
untouched.

| symbol | rows | first bar | last bar |
|---|---|---|---|
| BTCUSDT | 60,508 | 2019-09-08 17:00 | **2026-08-03 20:00** |
| ETHUSDT | 58,598 | 2019-11-27 07:00 | **2026-08-03 20:00** |
| SOLUSDT | 51,590 | 2020-09-14 07:00 | **2026-08-03 20:00** |

All ten requested candles present. No computation ran on an absent bar.

### A.1 Raw bars — 40/40 IDENTICAL

Every OHLC field on all ten candles matched to stored precision, deltas exactly
`0.0000`. Eight of ten are RESAMPLED from 1h, so this again externally validates
`resample_ohlcv` against TradingView's aggregation — now including the 2026-06-30
daily bar.

### A.5 Cross-checks — all hold on our numbers

| identity | value | holds |
|---|---|---|
| A2 close == A1 close | 63,836.9000 | YES |
| A3 open == A4 close | 63,550.0000 | YES |
| 06-30 daily close == A8 4h close | 58,605.4000 | YES |
| 06-30 daily close == A9 daily open | 58,605.4000 | YES |

### A.2 Setup A — 72/72 at displayed precision

Max |delta| 0.0491; max 83.8 bps (SOL AO, on a −0.33 magnitude). No mismatches.

### A.3 Setup B — RVWAP, both substrates

| id | row | operator | 1h substrate | 1d substrate | 1h−op | 1d−op | 1h vs 1d (ATR) |
|---|---|---|---|---|---|---|---|
| B1 BTC Aug-02 | rv7 | 63,990.10 | 63,908.83 | **63,990.07** | −81.27 | **−0.03** | −0.049 |
| | rv30 | 63,986.50 | 63,932.83 | **63,986.45** | −53.67 | **−0.05** | −0.033 |
| | rv90 | 66,787.80 | 66,798.81 | **66,787.79** | +11.01 | **−0.01** | +0.007 |
| | rv365 | 83,686.70 | 83,703.83 | **83,686.71** | +17.13 | **+0.01** | +0.010 |
| B2 BTC Jun-30 | rv7 | 60,792.00 | 59,951.63 | **60,791.96** | **−840.37** | **−0.04** | **−0.377** |
| | rv30 | 63,089.30 | 63,150.94 | **63,089.30** | +61.64 | −0.00 | +0.028 |
| | rv90 | 70,409.30 | 70,405.97 | **70,409.27** | −3.33 | −0.03 | −0.001 |
| | rv365 | 87,806.20 | 87,823.72 | **87,806.23** | +17.52 | +0.03 | +0.008 |
| B3 ETH Aug-02 | rv7 | 1,896.31 | 1,899.95 | **1,896.31** | +3.64 | −0.00 | +0.054 |
| | rv30 | 1,852.66 | 1,851.25 | **1,852.66** | −1.41 | +0.00 | −0.021 |
| | rv90 | 1,859.85 | 1,860.03 | **1,859.85** | +0.18 | −0.00 | +0.003 |
| | rv365 | 2,844.22 | 2,844.44 | **2,844.22** | +0.22 | −0.00 | +0.003 |

**FINDING — SUBSTRATE, NOT RECIPE.** The 1d substrate reproduces the operator to
the cent on all twelve triples (max |delta| 0.05, ≤ 0.02 bps). The pinned 1h
substrate differs by up to **0.377 daily-ATR**, largest on the shortest window
and vanishing by rv365 — exactly the signature of bar-granularity weighting.
Reported as a measurement; the spec question is decision **D3-1**.

### Anchored VWAP — separate finding

| | operator | 1h | 1d |
|---|---|---|---|
| BTC anchM | 63,038.90 | +56.78 | +73.37 |
| BTC anchQ | 63,605.60 | **−145.59** | −80.33 |
| ETH anchM | 1,860.39 | +2.17 | +3.00 |
| ETH anchQ | 1,827.03 | −0.20 | +1.85 |

Neither substrate matches, so substrate does not explain it. Likely the anchor
convention (bar inclusion / period boundary). The anchored **σ-band** recipe
remains **UNVERIFIED** — inferred from shared band machinery, never read from
source; the operator has not captured anchored bands. Both go in one round.

### A.6 Band symmetry — 24/24 exactly symmetric.

---

## 2 · STAGE B — REGISTRY COMPLETION

### B.2 Pivot audit — CONFIRMED, worse than suspected

`scripts/daily_brief.py:527` — `last_pivots(conf, vals, n=3)`. A **display** cap
of the three most recent highs and lows. 3+3 pivots + 4 priors + 4 period opens =
**13**, identical for all ten assets because the cap set the number.

`analytics.structure.confirmed_pivots` was **never emitted into the registry** —
it appeared only in `oscillator_layer` for divergences (`brief2.py:320-321`),
despite §5.1 naming confirmed pivots as a structure member. Now wired on a
trailing **180-day lookback** (self-limiting, varies per asset) rather than a
count cap. Measured H9/L9, H10/L9, H10/L8.

Also observed: `sessions` contributed **zero** structure levels because sessions
computes for `day_utc` = capture date and no bars existed for it yet — a recency
artifact, not a wiring bug.

### B.3 Weekly-anchor effect — CONFIRMED both directions

`anchored W: vwap=None, bars=0, anchor=2026-08-03T00:00Z`. 2026-08-03 is a
Monday. 3 armed anchors × 7 lines = 21, exactly as observed. With today's bars
present the W anchor arms → **28**.

**The registry has a weekly cycle, smallest on Mondays. Cycle 2's calibration was
taken at the weekly minimum.**

### B.1 / B.4 Prior anchors added; registry by family

| asset | | total | anchored | rolling | profile | structure | ss |
|---|---|---|---|---|---|---|---|
| BTCUSDT | old | 116 | 21 | 28 | 30 | 13 | 24 |
| | **new** | **165** | **49** | 28 | 30 | **34** | 24 |
| ETHUSDT | old | 104 | 21 | 28 | 30 | 13 | 12 |
| | **new** | **157** | **49** | 28 | 33 | **35** | 12 |
| LITUSDT | old | 93 | 21 | 21 | 22 | 13 | 16 |
| | **new** | **126** | **42** | 21 | 22 | **25** | 16 |

---

## 3 · STAGE C — R-1 DEMOTION, STRUCTURE-DERIVED INVALIDATION

`MIN_INVAL_ATR` demoted from exclusion gate to **caution chip**. Invalidation is
now the far edge of the **next cluster beyond** the entry cluster
(`INVAL_SEARCH_ATR = 3.0`).

| inval_atr | min | p25 | p50 | p75 | max | spread |
|---|---|---|---|---|---|---|
| OLD (width-derived) | 0.244 | 0.257 | 0.263 | 0.272 | 0.276 | 0.032 |
| **NEW (structure-derived)** | 0.345 | 0.349 | 0.371 | 0.382 | 0.418 | **0.073** |

Spread widened **2.3×**. Reported honestly: with the completed registry every
stop lands above 0.25, so **zero caution chips currently fire** — the threshold is
decorative in practice, which costs nothing now that it is a chip.

C.3: 20 ranked rows, 0 drafts without R:R in this sample; the no-structure path
is fixtured rather than merely available.

---

## 4 · STAGE D — STORAGE, MEASURED

### D.1 Git pack growth

30 synthesised daily captures (structure identical, values drifted ±1.5%),
committed one per day, `core.autocrlf=false`, `git gc --aggressive`.

| | working tree | git pack | pack / WT |
|---|---|---|---|
| 30 raw | 42.3 MB | **2.91 MB** | 6.9% |
| 30 gzipped | 5.1 MB | **5.07 MB** | 99.9% |

**Gzip is 1.74× LARGER in the repository** (+2.16 MB over 30 captures).

```
working-tree bytes (cycle-2 figure)   1,543 MB/yr
ACTUAL git pack growth, raw             106 MB/yr   <-- the real number
git pack growth if gzipped              185 MB/yr
§8.2 contract estimate              150-250 MB/yr
```

**My cycle-2 recommendation was wrong.** 1,584 MB/yr was working-tree bytes, not
repository growth. Raw is *inside* the original estimate.

### D.2 Per-layer breakdown (one asset block, 133,121 B = 98.1% of a 1-asset capture)

| key | bytes | % asset |
|---|---|---|
| confluence | 69,415 | 52.1% |
| decision_instrument | 20,772 | 15.6% |
| oscillators | 5,492 | 4.1% |
| cross_state | 5,011 | 3.8% |
| radar | 4,471 | 3.4% |
| volume_windows | 3,266 | 2.5% |

`confluence` splits with_volume 41,244 / without_volume 27,317.

### D.3 Rules block — **1,077 B = 0.79%**, NOT material. Left inline.

### D.4 Recommendation

Keep raw tracked JSON. Do not compress. Do not externalise the rule set. If
trimming is ever wanted, D.2 says the only worthwhile target is `confluence`, and
the honest lever is storing one view plus a diff — a schema change, not a
compression trick.

---

## 5 · FILE DISPOSITION

| file | disposition | why | tracked | pushed | fixture |
|---|---|---|---|---|---|
| `scripts/brief2.py` | MODIFIED | prior anchors, confirmed pivots, R-1 demotion, structure invalidation | yes | yes | F-B34, F-B35 |
| `tests/test_brief2_confluence.py` | MODIFIED | F-B35 | yes | yes | — |
| `tests/test_brief2_report.py` | MODIFIED | F-B34 rewrite | yes | yes | — |
| `analytics/*` | **UNTOUCHED** | no recipe changed this cycle | yes | yes | F-AN-* |
| `scripts/daily_brief.py` | **UNTOUCHED** | read-only audit target | yes | yes | F-B1..8 |
| `engine/data.py` | **UNTOUCHED** | DO-NOT-MODIFY; called only | yes | yes | — |
| `<cache>/klines/{BTC,ETH,SOL}USDT_1h.parquet` | TOPPED UP | 2026-08-03 candles | no (estate) | no | — |
| `exchange/reports/PARITY_C3_2026-08-03.json` | NEW | 54,427 B | yes | yes | — |
| `exchange/reports/STORAGE_MEASUREMENT_2026-08-03.json` | NEW | D.1 record | yes | yes | — |
| `exchange/reports/BUILDERS_REPORT_…_C3.md` | NEW | this file | yes | yes | — |
| `exchange/reports/SESSION_SUMMARY_…_C3.md` | NEW | decision artifact | yes | yes | — |

---

## 6 · FIXTURES

```
tests/test_analytics.py            57 passed
tests/test_brief2_volume.py        21 passed
tests/test_brief2_confluence.py    18 passed   + F-B35 (2)
tests/test_brief2_report.py        21 passed   + F-B34 rewritten (5)
tests/test_brief2_storage.py       22 passed
tests/test_forward0.py             18 passed
-----------------------------------------------------------
FULL SUITE                        230 passed, 1 skipped
```

Three fixture repairs this cycle, all the **same false-positive class** seen
before: a scan flagging the prose that *explains or forbids* a defect as if it
were the defect. F-B35's count-cap scan now reads code not docstring; F-B29's
banned-word scan no longer trips on "far **edge** of the next cluster"; F-B34's
tight case needed a cluster genuinely beyond it, because absence is C.3's path.

---

## 7 · FINDINGS

| id | status |
|---|---|
| **RVWAP substrate** | MEASURED, not fixed — decision D3-1 |
| **Anchored VWAP convention** | REPORTED, not chased — decision D3-2 |
| **Anchored σ-band recipe** | UNVERIFIED (inferred, never read from source) |
| **F-3R-A pivot display cap** | **FIXED** + fixtured |
| **Weekly-anchor cycle** | CONFIRMED; calibration caveat recorded |
| **Storage measurement error (mine, cycle 2)** | **CORRECTED** |
| **F-1R-C σ-band duplication** | NOT FIXED — ruling D-4, pinned until parity |
| **`analytics/INTERFACE.md` stale** | NOT FIXED — cycle 4 |

---

## 8 · PROVENANCE

`ANALYTICS_VERSION` **1.3.0** · `analytics_sha()`
`da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731` ·
`rules_version` 2.0.0 · `schema_version` 2.1.0 ·
`MIN_INVAL_ATR` 0.25 (chip) · `INVAL_SEARCH_ATR` 3.0.

Commits: `88f131b` · `c2af5f0` · `8d4806a` · `95420eb`.

---

## 9 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No engine change.
No forward scoring. No fitted weights. No estate mutation beyond an additive
kline top-up through the sanctioned loader.

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. **Adoption remains gated on parity, and Setup B is
NOT certified — the substrate question is open.**

— HEPHAESTUS, 2026-08-03
