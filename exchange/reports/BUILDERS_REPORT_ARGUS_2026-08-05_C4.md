# BUILDER'S REPORT — ARGUS lane — CYCLE 4 (CONSOLIDATED, THE CLOSING CYCLE)

**Builder:** HEPHAESTUS · **Date:** 2026-08-05 · **Branch:** `v12-v1-census`
**HEAD at start:** `897b8eb` · **HEAD at end:** see §9

Stages 0–8 executed in full. The scope valve was **not** invoked — stages 6 and
7 completed rather than deferring to cycle 5.

---

## 0 · GATE

`branch == v12-v1-census` · pwd contains `\Users\` **and** OneDrive ·
`analytics/` and `scripts/` present → **PASS**.

### 0.1 State probe

| | |
|---|---|
| `ANALYTICS_VERSION` at start | 1.3.0 → **1.4.0** at end |
| `analytics_sha` at start | `da81034d…c731` → **`e8a4959b…d20d66`** |
| suite at start | 248 passed / 1 skipped → **262 passed / 1 skipped** |
| stages E/F/G of the previous plan | **ALL BUILT** — `e127869`, `4239ef7`, `6a758f6` |

### ⚠ FINDING 1 — "none of them ran" is incorrect

The paste states the cycle-4 block, its replacement amendment and the parity
addendum "none of them ran." **They ran.**
`exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-03_C4.md` (267 lines) and
`SESSION_SUMMARY_ARGUS_2026-08-03_C4.md` (211 lines) exist, and the three
commits above are in history. The replacement amendment **executed in full on
2026-08-03**, including the 2.1 confirmation reading at 14/14.

What genuinely remained was the **reversion archetype** (explicitly deferred as
D4-2) and the **1h parity reading** (blocked on an operator capture, which
stage 2.2 supplied). This cycle delivered both.

### 0.2 GAP CHECK — three ratified features

| feature | verdict | evidence |
|---|---|---|
| (a) **RVOL** (B-7) | **ABSENT** | zero matches in `analytics/`, `scripts/`, `tests/`. Spec at `AMENDMENT_2_BRIEF2_RESHAPE_1.md:137` |
| (b) **{12,25} lattice** on 1D/1W (D-AR-16) | **PRESENT** | `scripts/brief2.py:68,69,428` · rendered `brief_render.py:243` · leak-guard `tests/test_brief2_report.py:500` |
| (c) **1m fast lattice** EMA(300)/(450) + 9/89/200 (§6.2) | **PRESENT** | `scripts/brief2.py:76,350,413–423`; 1m and 5m recorded side by side |

Only **RVOL** was owed. Built in stage 3.5.

### 0.3 Estate

BTCUSDT 1h ended **2026-08-04T00:00Z** — 41 hours short of what stage 2.2
requires. Topped up. All ten assets × six intervals now carry
**2026-08-05T17:00Z**, **0 gaps, 0 duplicates**.

### ⚠ FINDING 2 — R1 and R2 required no code change

Both were **already implemented**: `daily_brief.py:417` `vwap_series` is pinned
*"ALL rolling and anchored VWAPs are computed on 1h klines, typical price"*;
`brief2.py:212` `rvwap_layer(tf="1h")` with `W.hlc3`; `brief2.py:520`
`prior_anchored_vwaps` reads `klines["1h"]` with `W.hlc3`. **No returned number
moves under R1/R2.** Stage 1.1's premise that they change is false. What was
stale was the CONVENTIONS text.

### ⚠ FINDING 3 — the Python environment was gone

`site-packages` held only `pip`. numpy, pandas, pytest and pyarrow were all
missing though `requirements.txt` pins them and the suite last ran 2026-08-03.
Restored from the repo's own pin file (numpy 2.1.3, pandas 2.2.3, pytest 8.3.4,
pyarrow 18.1.0 — exactly the pins). Not a code finding, but it blocked every
stage and is recorded so a future session recognises it in one step.

---

## 1 · STAGE 1 — THE RECIPE RULINGS

### 1.1 R1/R2/R4 pinned · `ANALYTICS_VERSION` 1.3.0 → 1.4.0

The bump is taken on the **1.2.0 precedent**: the CONTRACT changed though no
number moved, and I-F identifies the recipe a stored capture was produced by.

**R2's reversal of the addendum's ohlc4 recommendation is on NEW INFORMATION,
not a change of mind** — the operator's ohlc4 chart setting was accidental, so
the addendum had been reasoning from a mis-set control. All four reasons
recorded verbatim in `analytics/vwap.py :: SOURCE_REASONING`:

(a) in a 24/7 perpetual a bar's open **is** the prior bar's close, so ohlc4
partly double-counts the prior bar and smears content across bar boundaries,
while hlc3 uses only what happened inside the bar; (b) hlc3 is the standard
"typical price" definition and TradingView's own Rolling VWAP default; (c) ONE
price definition across the whole family, so a disagreement between two VWAP
levels is a market fact and not a definitional artifact; (d) at hourly
resolution the difference is small and largely averages out — so the cost of
choosing correctly is near zero and the cost of choosing by accident is a
permanent unexplained offset.

**R4 — variance INFERRED → VERIFIED, with the EVIDENCE and not just the
verdict** (`analytics/__init__.py :: CONVENTIONS["anchored_vwap"]
["variance_evidence"]`): the 2026-08-01 Month anchor was **two bars** wide, the
smallest sample that discriminates — population and sample forms differ there by
√(n/(n−1)) = √2 = **41.4%** against a 0.02-ATR collapse tolerance. Population
landed within **0.003%**; sample would have missed by 41%. Read off a
measurement that could only come out one way.

### 1.2 R3 maturity floors — before / after

`LINE_MIN_BARS = 10`, `BAND_MIN_BARS = 30`, gated **separately** because the
line is a weighted mean (fast to stabilise) and σ is a dispersion estimate over
the same few points (slow).

| | before | after |
|---|---|---|
| immature line admitted to registry | yes | **withheld**, recorded |
| immature σ bands admitted | yes | **withheld**, recorded |
| below-floor value still printed | n/a | **yes**, `thin_sample` chip |

**MEASURED, ALL TEN ASSETS: 0 levels withheld.** The zero is real, not a dead
gate — the shallowest estimator anywhere on the estate is the developing W
anchor at **66 bars** against a band floor of 30 (n=109 estimators). It binds in
production every Monday 00:00–10:00 UTC (line) and to Tuesday 06:00 UTC (bands):
**30 of every 168 hours, 17.9% of the week.** That is where cycle 4's three
`thin_sample` flags came from. F-B37 proves the gate fires at 3 bars and at 15.

---

## 2 · STAGE 2 — PARITY, BOTH READINGS, ONE RUN

### 2.3 RAW BAR CHECK — first, before any indicator

**1h bar `2026-08-05T17:00Z`**

| field | ours | operator | delta |
|---|---|---|---|
| open | 64631.8000 | 64631.80 | **0.0000** |
| high | 64780.0000 | 64780.00 | **0.0000** |
| low | 64506.3000 | 64506.30 | **0.0000** |
| close | 64733.6000 | 64733.60 | **0.0000** |
| volume | 4461.8800 | "4.46K" (3 s.f.) | +1.88 |

Nothing downstream inherits a bad input. The 1D bar `2026-08-02T00:00Z` resolves
to O 62792.3 / H 63779.0 / L 62782.3 / C 63550.0 / V 84,040.407 — the operator
supplied no raw 1D OHLCV, so there is nothing to diff there.

### 2.1 CONFIRMATION READING — 1D / hlc3 / candle 2026-08-02

**Anchored Month VWAP** (anchor `2026-08-01T00:00Z`, 2 bars)

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 63112.267074 | 63112.3 | 63112.3 | −0.0329 | −0.0052 |
| +1σ | 63432.155499 | 63432.2 | 63432.2 | −0.0445 | −0.0070 |
| −1σ | 62792.378648 | 62792.4 | 62792.4 | −0.0214 | −0.0034 |
| +2σ | 63752.043925 | 63752.0 | 63752.0 | +0.0439 | +0.0069 |
| −2σ | 62472.490222 | 62472.5 | 62472.5 | −0.0098 | −0.0016 |
| +3σ | 64071.932351 | 64071.9 | 64071.9 | +0.0324 | +0.0050 |
| −3σ | 62152.601796 | 62152.6 | 62152.6 | +0.0018 | +0.0003 |

**PREDICTION CONFIRMED, EXPLICITLY.** The addendum computed hlc3 =
**63,112.2671** *before* the Source setting changed and predicted the reading
would move there. It did, to **−0.005 bps**. The earlier ohlc4/hlc3 discrepancy
is therefore **fully explained**, not patched over.

**RVWAP 365 (1D)** — VWAP 83686.712195 vs 83,686.7; worst band delta 0.0452.
**UNCHANGED from the ohlc4-era capture** (which recorded 83,686.7122) — rolling
was always hlc3, so it must not have moved, and it did not. **NO FINDING.**

**σ, reproduced with the ACTUAL 2026-08-01 bar:** ours **319.8884** against the
operator's observed band-1 distance 319.9 = **−0.0036%**. The reviewer's
back-solved 320.13 misses by **+0.072%** — so **the back-solve was slightly off,
not our arithmetic.** True volume weights: **0.394428 / 0.605572**.

### 2.2 RULED-SUBSTRATE READING — 1H / hlc3 / `2026-08-05T17:00Z`

**THE FIRST PARITY EVER RUN ON THE 1h PATH.**

| window | bars in window | our VWAP | operator | worst \|Δ\| across all 7 | worst bps |
|---|---|---|---|---|---|
| RVWAP 7d | 168 | 63737.732321 | 63737.7 | **0.0453** | 0.0070 |
| RVWAP 30d | 720 | 64026.473964 | 64026.5 | **0.0496** | 0.0079 |
| RVWAP 90d | 2,160 | 66248.839326 | 66248.8 | **0.0494** | 0.0068 |
| RVWAP 365d | 8,760 | 83430.771601 | 83430.8 | **0.0429** | 0.0056 |

**All 28 values agree within 0.0496** — the rounding half-step of the operator's
one-decimal display. The residual is his display precision, not our arithmetic.
Full tables in `research_outputs/parity/PARITY_C4_2026-08-05.txt`.

### 2.5 SYMMETRY AND IMPLIED σ

Every one of the 12 triples on the 1h path is **exactly symmetric** —
`midpoint − vwap = 0.00e+00` exactly — at **exact integer multiples** of σ
(residual ≤ 3.6e−12, float noise at 5-digit prices).

| window | our σ | reviewer-implied | delta |
|---|---|---|---|
| 7d | 658.9130 | 658.9 | +0.0130 (+0.20 bps) |
| 30d | 1014.3754 | 1014.35 | +0.0254 (+0.25 bps) |
| 90d | 6288.7101 | 6288.7 | +0.0101 (+0.02 bps) |
| 365d | 18858.6356 | 18858.65 | −0.0144 (−0.01 bps) |

### 2.6 ANCHORED ON 1h — and what is still open

| | ours | operator | delta |
|---|---|---|---|
| anchored Month (114 bars) | 63602.445234 | 63602.4 | +0.0452 |
| anchored Quarter (858 bars) | 63486.310922 | 63486.3 | +0.0109 |

**ANCHORED SIGMA ON THE 1h SUBSTRATE REMAINS UNVERIFIED.** The recipe and the
variance definition **are** verified (from the 2026-08-03 1D/hlc3 capture); only
the substrate is untested, and the Month-anchor substrate delta was measured at
up to **0.186 daily-ATR**. Our unverified values, for the record: M σ 583.3876
(+1σ 64185.8329 / −1σ 63019.0576); Q σ 1541.3212 (+1σ 65027.6321 / −1σ
61944.9897). **One 1H capture with anchored bands enabled closes it. NOT
BLOCKING.**

### 2.7 INSTRUMENT SENSITIVITY — now a standing warning in INTERFACE.md

| instrument | RVWAP 7d, same bar |
|---|---|
| `BINANCE:BTCUSDT.P` — what we compute | 63,737.7 |
| TradingView `BTCUSD` **INDEX** | 63,786.76 |
| **gap** | **49.06** |

BTC daily ATR 1,628.44 → collapse tolerance (0.02 ATR) = **32.57**. The gap is
**0.030 ATR = 1.51× the tolerance**, so the two readings would **not** collapse
into one level — they would enter the registry as **two separate members**. In a
system that scores by counting agreement, that is one tool counted twice.

**No pass/fail and no tolerance is asserted anywhere.** The reviewer judges what
counts as a match.

---

## 3 · STAGE 3 — EXCURSION LAYERS, RVOL, FIREWALL

### 3.1 / 3.2 Stretch — verified against the live parity bar

At price **64,733.6**, `2026-08-05T17:00Z`:

| window | mean | σ | σ-position |
|---|---|---|---|
| RVWAP 7d | 63,737.7323 | 658.9130 | **+1.51** |
| RVWAP 30d | 64,026.4740 | 1,014.3754 | **+0.70** |
| RVWAP 90d | 66,248.8393 | 6,288.7101 | **−0.24** |
| RVWAP 365d | 83,430.7716 | 18,858.6356 | **−0.99** |

Reproduces the contract exactly. Price is **above the 7d σ1 upper — a live
excursion** — and the shape is **non-monotonic**: stretched up against the week,
pulled down against the year, at the same instant. Fixtured (F-B39).

### ⚠ FINDING 4 — the excursion table was documented for a cycle and never built

Every capture claimed `since_last_touch` was *"DERIVED at panel-build time from
the stored `band_reached` series"*. **`brief_panel.py` had no excursions table
and no derivation.** The promise was prose.

**Both now exist.** `briefs/panel/excursions/<date>.parquet` (54 rows today)
stores per-capture OBSERVATIONS only; `since_last_touch()` derives recency on
demand via `--since-last-touch`. Nothing cross-capture is stored, because that
would break the rebuild-from-captures-alone guarantee F-B19/F-B32 protect. Panel
schema **2.0.0 → 2.1.0**, `briefs/panel/SCHEMA.md` documents all 11 columns.

### 3.4 FIREWALL — enforced on CODE, not promised in prose

F-B38 scans what `excursion_layer` and `since_last_touch` **do**. The line:
recency ("when was this band last touched") is a diary fact, the same class as a
naked POC's "untested since"; any statistic over the event history — rates,
reversion percentages, expectancy — is **H-VBR**, census work under G-7.

### ⚠ FINDING 5 — sixth and seventh instances of one recurring false positive

**F-B16 was carrying it.** The guard scanned RAW SOURCE, so a docstring stating
*which* statistics a function refuses to compute failed the firewall. F-B16 now
strips prose, with anti-vacuity **both ways** — a real assignment must still be
caught, and the stripper must not eat the code. Where the flagged text was
genuinely executable (a `print()` in `main()`), **the guard was right** and the
string was reworded instead of the guard weakened.

**The seventh instance was in this cycle's own new fixture**:
`contains_no_probability_claim` is a DISCLAIMER, and a scan reading it flags the
promise as the offence. F-B41 strips disclaimer keys and scans the payload.

Prior five: F-F3's prohibition text, F-B29's "not probability", F-B35's quoted
`n=3`, F-B36's `claims_nothing`, cycle 4's `stoch_rsi_k`.

### 3.5 RVOL — built (ruling B-7)

Bar volume ÷ mean of the **same time-of-day bucket** over the trailing 20 days,
**current bar excluded from its own baseline**. The bucket is the design: crypto
volume has a hard diurnal shape, so a flat 20-day mean would score every US-open
bar "high" and every Asian bar "low" — a clock reading, not a market reading.
Self-exclusion matters most on exactly the spikes the measure exists to find.
Sample selection is "the last 20 occurrences of this hour", not a time filter —
both agree on gapless data and diverge across an outage.

Live, all ten assets, 20/20 samples each. ETHUSDT **2.286**, SOLUSDT 1.340,
LITUSDT 0.464. **RVOL casts no vote and enters no registry** — it describes
participation, not price, so it locates nothing and can be confluent with
nothing.

---

## 4 · STAGE 4 — REGISTRY CONFIRMATION

All five families non-empty on all ten assets.

| asset | vwap_anchored | vwap_rolling | profile_windowed | structure | ss | total |
|---|---|---|---|---|---|---|
| BTCUSDT | 49 | 28 | 33 | 34 | 20 | **164** |
| ETHUSDT | 49 | 28 | 30 | 35 | 6 | 148 |
| FARTCOINUSDT | 49 | 28 | 39 | 37 | 16 | **169** |
| HYPEUSDT | 49 | 28 | 30 | 35 | 14 | 156 |
| JTOUSDT | 49 | 28 | 36 | 38 | 12 | 163 |
| LITUSDT | 49 | 21 | 16 | 35 | 10 | **131** |
| NEARUSDT | 49 | 28 | 21 | 38 | 18 | 154 |
| SOLUSDT | 49 | 28 | 30 | 38 | 12 | 157 |
| TAOUSDT | 49 | 28 | 30 | 33 | 22 | 162 |
| ZECUSDT | 49 | 28 | 27 | 37 | 24 | 165 |

LIT's 21 rolling levels are the 365d window still warming (222 days of history)
— warm-up honesty, not a defect.

**Prior M/Q/Y present on every asset**, bar counts showing real shape rather
than a uniform stamp: 744/2184/8760 for a full month/quarter/year on 1h, with
HYPE's prior_Y at 5,174 and LIT's at 199 — both younger than a year, carrying
what history exists rather than a fabricated anchor.

**Confirmed pivots on the 180-day lookback, NOT the display-capped path.**
F-3R-A regression check **PASSES**: totals are 17/18/19/21/22 across the ten
assets, not the uniform 13 that first exposed the cap.

### R6 — no distance filter, and what the overruled proposal would have cost

**567 of 1,381 scored levels (41.1%) sit beyond 3 ATR.** The furthest admitted
is **192.37 ATR** (FARTCOINUSDT, `vwap_anchored`). The ±3 ATR filter judged
levels by whether they could cluster NEAR price — an entry-side test — while the
R:R design defines targets as the next OPPOSING clusters, far by construction.
It would have truncated every target search at 3 ATR and **capped R:R by
construction**.

**Weekly-anchor cycle documented**: reopens Monday 00:00 UTC at 0 bars; crosses
the line floor Monday 10:00 UTC and the band floor Tuesday 06:00 UTC.

---

## 5 · STAGE 5 — THE REVERSION ARCHETYPE

The one item cycle 4 deferred (D4-2).

| | CONTINUATION | REVERSION (new) |
|---|---|---|
| entry | confluence cluster near price | σ2/σ3 band price has **ACTUALLY REACHED** |
| target | next opposing cluster | **the VWAP mean** |
| invalidation | beyond the next cluster back | σ2 → beyond σ3; σ3 → σ3 + one band width |

### Measured on the live capture

**12 drafts across 7 of 10 assets.**

| bucket | n | R:R values | median target ATR | median band score |
|---|---|---|---|---|
| NEAR (<2 ATR) | 6 | {2.0, 3.0} | 0.55 | 13.0 |
| MID (2–6) | 3 | {2.0, 3.0} | 4.29 | 13.0 |
| FAR (>6) | 3 | {2.0} | 15.52 | 3.0 |

**MID and FAR are populated for the first time.** Cycle 4 measured all 40
continuation targets in NEAR with MID and FAR both **empty**, and said plainly
that this was why the reversion archetype mattered. It does: the mean is where
the long distance lives.

### 5.3 — the reviewer's design decision, now backed by evidence

**R:R took exactly two values across the entire estate: 2.0 (×9) and 3.0 (×3),
in every bucket.** That is 5.3's premise turned into measurement — reversion R:R
is a **constant of the geometry** and sorting by it is sorting by a column with
two distinct values. Ranking is by the **confluence score of the band level
itself**, which ranged **2..16** on the same capture and does discriminate. The
band is already a registry member under R6, so that score is a **lookup**, not a
new computation.

**Flagged for operator veto**, as instructed.

### 5.4 — why identical geometry is not an identical trade

BTC's prior-Y draft travels **14.88 ATR** on a **7.44-ATR σ** — a position held
for months. ETH's anchored-W draft travels **0.6 ATR** — a day trade. Same 2:1,
same board. Every draft prints its anchor/window and σ-width in ATR.

**Thin-sample gate (D4-2):** a draft requires ≥30 bars, so a freshly-opened
anchor cannot manufacture a setup from a two-bar σ. Skips are recorded.

**5.9** every VWAP layer prints substrate (1h) and source (hlc3) **read from the
capture, never imported** — F-B10 forbids the render reaching into `analytics`,
and the stored value is the more honest chip: it reports what the capture was
BUILT with, not what today's code would do.

**5.5 / 5.6 / 5.7 / 5.8 / 5.10 / 5.11** were already built in cycle 4
(`4239ef7`) and are unchanged: target bucketing, target clusters, §4.2 prose,
chart planes, the parity banner, `brief_note.py`.

Render: **158,412 B**, 7 reversion boards.

---

## 6 · STAGE 6 — INTERFACE AND RETIREMENT

`analytics/INTERFACE.md` regenerated (42,702 chars). It predated 1.3.0, the
dedupe, the §7.2 fix, the pivot wiring and every ruling in this cycle.

**CERTIFICATION TABLE added as a required section** — "verified" and "certified"
are different claims and APOLLO had no way to tell them apart. The substrate
caveat section, which for four cycles warned the 1h path was untested, is
**superseded and rewritten with the result**. The 2.7 instrument warning is in.

**6.3 v1.1 RETIRED.** Ruling D-3's condition (a render exists) is met.
**Not deleted** — `daily_brief.py` is still imported by `brief_capture.py` for
the Part I layers, and its published numbers are the bridge to every pre-2026-08
archive. Marked `"retired": "2026-08-05"`, `"scheduled": false` in
`scripts/routine_jobs.json`, with the reason and successor recorded inline.

---

## 7 · STAGE 7 — RECALIBRATION

All cycle-2/3 numbers were void: three families empty, prior anchors missing,
pivots display-capped, measured at the weekly registry minimum.

| §9.2 item | result |
|---|---|
| 1 · level count by family | **131–169, median 160**, five families non-empty on all ten |
| 2 · score distribution | min 2 / median 2 / **p90 8** / max 18 over **625 clusters**; family cap binds **8.8%** |
| 3 · LIS stability 0.10/0.15/0.20 | 19 line moves off the 0.15 baseline, **median 0.213 ATR** |
| 4 · top-3 family composition | anchored 24.3% · ss 22.1% · profile 21.8% · structure 20.8% · rolling 11.0% — **no family dominates** |
| 5 · VA nesting states | nested_inside 15 · overlapping 9 · disjoint_below 3 · disjoint_above 2 · warming 1 |
| 6 · dual-scoring divergence | **see 7.2 below** |
| 7 · measured storage | capture **1.97 MB** (was 0.79 MB — 2.5×, the new layers); partitions **86 KB/day** |

§5.3's 180–200 forecast predates the layers. **The measured range is the fact;
the forecast is not a target to be reached.**

### 7.2 ITEM 6 RE-BUCKETED — it was overstated twice

| | count |
|---|---|
| **RELOCATIONS** (≥0.15 ATR, one cluster width) | **6** |
| refinements (<0.15 ATR, within one cluster) | **14** |
| line present in one view only | 0 |

Median move **0.044 ATR**, max 0.971. Cycle 2 headline: *"a line moved on 20 of
20 sides."* Cycle 4 re-bucketed it to 12. **On the full registry it is six.**
Seventy per cent of what was originally counted as movement is the same
structure re-centred inside its own cluster.

### New measurements this cycle

**`inval_atr` distribution** — n=100, **0.164 … 1.419**, median **0.396**, p90
0.493; 7 of 100 below `MIN_INVAL_ATR` 0.25 (caution chip, none excluded). Cycle
3 saw **0.244–0.276**, a 0.03 spread. An **8.6× wider spread** on a registry
three times the size — which vindicates demoting the floor to a caution chip
(D2-2): on the old spread the threshold was cutting on noise.

**Level-distance distribution by family**, bucketed <1.5 / 1.5–3 / 3–6 / 6–12 /
>12 ATR — **to describe, not to filter**:

| family | <1.5 | 1.5–3 | 3–6 | 6–12 | >12 | total |
|---|---|---|---|---|---|---|
| vwap_anchored | 176 | 64 | 81 | 66 | 73 | 460 |
| vwap_rolling | 101 | 49 | 35 | 41 | 42 | 268 |
| profile_windowed | 103 | 29 | 35 | 26 | 32 | 225 |
| structure | 131 | 44 | 66 | 59 | 11 | 311 |
| ss | 106 | 11 | 0 | 0 | 0 | 117 |
| **ALL** | **617** | **197** | **217** | **192** | **158** | **1381** |

`ss` levels are all within 3 ATR — a governor band is an entry-side object by
construction, which is exactly the asymmetry R6's overruled filter mistook for a
general rule.

**HOW OFTEN PRICE SITS BEYOND σ1/2/3** — 365 days of 1h bars, ten assets:

| beyond | measured | Gaussian |
|---|---|---|
| ±1σ | **~50%** (44.9–53.3) | 31.7% |
| ±2σ | **~9.5%** (6.7–12.4) | 4.6% |
| ±3σ | **~0.4%** (0.07–0.86) | 0.27% |

**The 1σ band holds far less than Gaussian intuition expects and the 2σ tail is
roughly double** — a "2σ is rare" prior is wrong by a factor of two. This is a
description of the DISTRIBUTION, not a statistic over excursion outcomes: it
says nothing about whether a touch pays.

**MATURITY STABILISATION — NOT DELIVERED.** The measured replacement for R3's
interim 10/30 floors requires a per-bar walk-forward of every anchor and window
across the estate. It is the one stage-7 item outstanding and is named as cycle-5
work in the Session Summary rather than quietly dropped.

### 7.3 Capture and partitions

`briefs/brief_2026-08-05_post_ny.json` — sha256
`a93998f3dc8b7ea73a4660ac204322471fa9a69cd80ad1a9ffdfacc7ee8185de`.
All **four** write-once partitions built: snapshots 10 · levels 2,269 · areas 80
· **excursions 54**.

---

## 8 · FIXTURES

| id | what it asserts | tests |
|---|---|---|
| **F-B37** | R3 floors bind, bind SEPARATELY (line 10 / bands 30), and every withholding is auditable; uncountable depth treated as immature | 1 |
| **F-B38** | excursion firewall on CODE; `since_last_touch` computes recency and no rate; the excursions table exists and round-trips | 3 |
| **F-B39** | stretch reproduces the 2026-08-05 ruled-substrate capture; non-monotonic disagreement | 1 |
| **F-B40** | RVOL compares like with like, excludes itself, reports warming honestly, never emits `inf`; casts no vote | 2 |
| **F-B41** | reversion R:R is exactly 2:1/3:1; ranking is by band score not R:R; entry requires price to have REACHED; thin-sample gate; σ-width discriminates; no probability or sizing; fills FAR bucket | 7 |

**Suite 248 → 262 passed, 1 skipped. Zero failures.**

The one skip is `fixtures/test_f8_journal.py:110` — "dry-run journal not
generated yet (D7)", pre-existing and unrelated.

---

## 9 · FILE DISPOSITION

| file | disposition | why | authorized | lines Δ | verified |
|---|---|---|---|---|---|
| `analytics/__init__.py` | MODIFIED | version 1.4.0; R2/R4 CONVENTIONS; RVOL convention | `analytics/*` | +68 | suite |
| `analytics/vwap.py` | MODIFIED | substrate/source pins, R2 reasoning, R3 floors, `maturity()` | `analytics/*` | +83 | F-B37 |
| `analytics/profile.py` | MODIFIED | `relative_volume` (RVOL) | `analytics/*` | +76 | F-B40 |
| `analytics/INTERFACE.md` | REGENERATED | stale; certification table, 2.7 warning, new schemas | `analytics/*` | +1464/−? | read |
| `scripts/brief2.py` | MODIFIED | R3 gate, `rvol_layer`, `reversion_drafts` | `scripts/*brief*` | +280 | F-B37/40/41 |
| `scripts/brief_panel.py` | MODIFIED | excursions table, `since_last_touch`, schema 2.1.0 | `scripts/*brief*` | +113 | F-B38 |
| `scripts/brief_render.py` | MODIFIED | reversion board, §5.9 provenance chip | `scripts/*brief*` | +82 | F-B10 |
| `scripts/parity_check.py` | MODIFIED | full σ1/2/3 triples; `avwap` measure | named explicitly | +57 | stage 2 |
| `scripts/brief_calibration_c4.py` | NEW | stage-7 recalibration harness | `scripts/*brief*` | +276 | ran |
| `scripts/brief_registry_audit.py` | NEW | stage-4 registry audit | `scripts/*brief*` | +114 | ran |
| `scripts/parity_c4_worksheet.py` | NEW | stage-2 both-readings worksheet | ⚠ adjacent to `parity_check.py`, not a literal `*brief*` match — **disclosed** | +197 | ran |
| `scripts/routine_jobs.json` | MODIFIED | 6.3 v1.1 retirement | ⚠ not a `*brief*` match — **directed by 6.3**, disclosed | +4 | read |
| `briefs/panel/SCHEMA.md` | MODIFIED | excursions table documented | `briefs/*` | +47 | F-B19 |
| `tests/test_brief2_confluence.py` | MODIFIED | F-B37, F-B41 | `tests/*` | +? | ran |
| `tests/test_brief2_report.py` | MODIFIED | F-B38, F-B39, F-B40 | `tests/*` | +? | ran |
| `tests/test_brief2_storage.py` | MODIFIED | F-B16 prose-strip; F-B32 keyed to `TABLES` | `tests/*` | +? | ran |
| `scripts/seq8_*.py` (5 files) | **UN-TRACKED** | ⚠ swept in by a wildcard `git add`, reverted with `git rm --cached`. Another lane's work. Files UNCHANGED on disk, back to untracked. | not authorized | 0 net | `git status` |
| `research_outputs/seq8/`, `seq8_run2/` (26 files, **3,567 MB**) | **NEVER TRACKED — history rebuilt** | ⚠⚠ **see §9.1** | not authorized | 0 net | tree = 25.5 MB |

**DO NOT MODIFY list respected:** `engine/*`, `configs/*`, `study/*`,
`publish_exchange.py`, `reviewer_manifest.py`, `backup_estate.py`,
`orchestrator_state.py` — all untouched.

### 9.1 ⚠ BUILDER ERROR — 3.5 GB of another lane's data, and a blocked push

**What happened.** Two commits used a wildcard `git add -A <dir>` instead of
naming files. Stage 4's `git add -A scripts …` swept in five
`scripts/seq8_*.py`; stage 5's `git add -A … research_outputs` swept in
`research_outputs/seq8/` and `seq8_run2/` — **26 files, 3,567 MB** of
SEQ8/DIONYSUS lane data that was untracked at session start.

**How it surfaced.** `publish_exchange.py` committed correctly and then **the
push was rejected outright by GitHub**: four of those files exceed the 100 MB
hard limit, the largest at **753 MB**. The pre-receive hook declined the whole
branch, so *nothing* could publish.

**Fix.** Nothing had ever reached the remote, so the local history was rebuilt
without those paths — `git reset --soft` to the last clean commit, re-stage by
explicit path, recommit. **No remote history was rewritten.** The two affected
commits changed SHA (`fd86aa9`→`9701b57`, `7af9ad4`→`4685232`); their content is
identical apart from the removed files. Tree is back to **25.5 MB**, largest
blob 6 MB. All 26 files are **unchanged on disk** and back to untracked.
Suite re-run after the rebuild: **262 passed / 1 skipped**.

**RECOMMENDATION, deliberately NOT applied** (`.gitignore` is outside this
cycle's authorized scope) — add:

```
research_outputs/seq8/**
research_outputs/seq8_run2/**
```

Every other lane's bulk output is already ignored there — `tc1/** tc4/** tc5/**
s1/** s2/** s3/** census/** census1b/**`. **`seq8` is the only one missing**,
which is exactly why a wildcard add could catch it. Two lines close it
permanently. Until then any `git add -A` in this repo re-breaks the remote.

### Commits (final, after the §9.1 rebuild)

```
38602a2  stage 1 — R1/R2/R4 pinned, R3 maturity floors (F-B37)
96f56e3  stage 2 — the 1h path passes parity, first time in five cycles
316d810  stage 3 — RVOL, excursion table, firewall enforced on code
c46bffb  stage 4 — registry confirmed by measurement, R6 vindicated
9701b57  stage 5 — the REVERSION archetype, and the far buckets finally fill
4685232  stages 6+7 — INTERFACE regenerated, v1.1 retired, recalibration
b99de62  chore — un-track scripts/seq8_*.py (+ the §9.1 disclosure)
71cb2ab  exchange: auto-publish 2026-08-05   ← PUSHED
```

**Repo is commit-no-push**, per standing rule. `exchange/**` published via
`scripts/publish_exchange.py`: status **PUBLISHED**, commit `71cb2ab`, 9 paths,
**pushed to `origin/v12-v1-census`**. `HEAD == origin/v12-v1-census`.

---

## 10 · FIREWALL — UNCHANGED

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Recording band excursions is **OPS**; aggregating
them is **census work under G-7**. **H-VBR** and **H-VBT** are routed to APOLLO
with their deflation gauges stated **in advance**. No sizing, no probability, no
lockbox read as evidence, no fitted weight anywhere in the scoring path.

`PARITY NOT CERTIFIED` still prints on every render. Rolling VWAP passing on
both substrates does not certify the instrument; the banner comes down when the
operator says so, not when a builder judges the deltas small.

— HEPHAESTUS, 2026-08-05
