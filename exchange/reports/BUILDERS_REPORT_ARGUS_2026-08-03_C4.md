# BUILDER'S REPORT — ARGUS lane — CYCLE 4

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Branch:** `v12-v1-census`
Replacement amendment executed. **D.4 WITHDRAWN — no distance filter exists.**

---

## 0 · GATE AND STATUS

branch `v12-v1-census` · pwd contains `\Users\` + OneDrive · `analytics/`
`scripts/` present → **PASS**. HEAD at start `0b46458`.

Suite **248 passed / 1 skipped**. `analytics` **1.3.0** · `rules_version` 2.0.0 ·
`schema_version` 2.1.0. **PARITY NOT CERTIFIED — nothing adopted.**

---

## 1 · A.6 — hlc3 ANCHORED CONFIRMATION

### A.6.1 Anchored Month, 1D / hlc3

| level | ours | operator | delta | bps |
|---|---|---|---|---|
| VWAP | 63,112.2671 | 63,112.3 | −0.0329 | −0.01 |
| +1σ | 63,432.1555 | 63,432.2 | −0.0445 | −0.01 |
| −1σ | 62,792.3786 | 62,792.4 | −0.0214 | −0.00 |
| +2σ | 63,752.0439 | 63,752.0 | +0.0439 | +0.01 |
| −2σ | 62,472.4902 | 62,472.5 | −0.0098 | −0.00 |
| +3σ | 64,071.9324 | 64,071.9 | +0.0324 | +0.01 |
| −3σ | 62,152.6018 | 62,152.6 | +0.0018 | +0.00 |

**PREDICTION CONFIRMED.** The addendum computed hlc3 = 63,112.2671 *before* the
Source setting changed and predicted the reading would move there. It did, to
**−0.0329 (−0.005 bps)**. The earlier ohlc4/hlc3 discrepancy is therefore fully
explained rather than patched.

### A.6.2 RVWAP 365 — unchanged

| level | ours | operator | delta |
|---|---|---|---|
| VWAP | 83,686.7122 | 83,686.7 | +0.0122 |
| ±1σ | 102,555.3287 / 64,818.0957 | 102,555.3 / 64,818.1 | +0.0287 / −0.0043 |
| ±2σ | 121,423.9452 / 45,949.4792 | 121,423.9 / 45,949.5 | +0.0452 / −0.0208 |
| ±3σ | 140,292.5617 / 27,080.8627 | 140,292.6 / 27,080.9 | −0.0383 / −0.0373 |

Byte-identical to the ohlc4-era capture. Rolling VWAP was always hlc3 — **no
finding**. σ = 18,868.62 = **11.44 daily ATR**.

### A.6.3 Sigma and true weights

| | value |
|---|---|
| ours, volume-weighted population | **319.8884** |
| operator observed band-1 distance | 319.9 → **−0.004%** |
| reviewer back-solved | 320.13 → −0.075% |

**The back-solve was slightly off, not our arithmetic.** True weights on the two
bars: hlc3 62,715.9000 @ **0.394428** and 63,370.4333 @ **0.605572**.

### A.6.4 The untested path

**Every parity check across four cycles compared a 1D chart reading to a 1D
computation.** The ruled substrate is **1h**, where the rolling-VWAP gap reached
**0.377 daily-ATR** on the 7-day window. The path the instrument runs on is
externally unverified. Decision D4-1.

---

## 2 · D.4 — WITHDRAWN, ON THE RECORD

No registry admission filter by distance exists. All levels enter at any
distance. The withdrawn ±3 ATR rule judged levels by whether they could cluster
NEAR price — an entry-side test — while targets are far from price by
definition; it would have truncated every target search at 3 ATR and capped R:R
by construction.

**Evidence the far bands are structure, not ballast**, measured this cycle: one
sigma of BTC's 365d RVWAP is **11.44 daily ATR**, and the >12 ATR distance bucket
holds **68 vwap_anchored + 42 vwap_rolling against only 11 structure** levels.
The far region *is* VWAP-band structure.

`test_d72_target_clusters_are_not_distance_filtered` fixtures the withdrawal: a
cluster 85 ATR away must survive.

---

## 3 · D.5 / D.6 — STRETCH AND EXCURSION

Worked example reproduced exactly and fixtured (F-B36): at price 63,522.7,
Month (63,112.3 / 319.9) → **+1.28σ**; RVWAP365 (83,686.7 / 18,868.6) → **−1.07σ**.

Live on BTCUSDT, eleven means:

| anchor / window | mean | sigma | σ pos | ATR | flags |
|---|---|---|---|---|---|
| anchored W | 63,234.18 | 496.14 | +1.05 | +0.32 | THIN, past 1σ |
| anchored M | 63,165.19 | 427.38 | **+1.38** | +0.36 | past 1σ |
| anchored Q | 63,453.11 | 1,576.38 | +0.19 | +0.18 | |
| anchored Y | 71,380.23 | 8,750.78 | −0.87 | −4.62 | |
| prior M | 63,471.78 | 1,621.27 | +0.18 | +0.17 | |
| prior Q | 70,384.15 | 7,154.94 | −0.93 | −4.02 | |
| prior Y | 99,401.64 | 12,119.60 | **−2.94** | −21.61 | past 2σ |
| RVWAP 7d | 63,662.66 | 645.80 | +0.14 | +0.06 | |
| RVWAP 30d | 63,928.48 | 1,071.23 | −0.16 | −0.10 | |
| RVWAP 90d | 66,607.11 | 6,633.82 | −0.43 | −1.73 | |
| RVWAP 365d | 83,622.62 | 18,908.21 | −1.05 | −12.04 | past 1σ |

**D.5.1 disagreement:** max `anchored M` +1.38σ, min `prior Y` −2.94σ, spread
**4.32σ**, straddles ±1σ **true**.

**D.6:** 4 excursion events. `thin_sample` fires correctly on the weekly anchor
(21 bars < 30). No "captures since last touch" counter is stored — derived at
panel-build time so the capture stays self-describing.

---

## 4 · STAGE E — THE RENDER

`scripts/brief_render.py` (Part I + Part II, Atlas language, 144,574 B from a
stored capture) and `scripts/brief_note.py`.

**The render recomputes nothing** — F-B10 asserts it by AST: no `analytics`
import, no call to any computation function. Prose (§4.2), forming candle
(drawn, greyed, and the page says in words it reaches no computed value), the
parity banner in both directions, the full bias scorecard with every vote.

**F-B20:** a degraded Tier-2 block still renders, and dropping any of ten layers
— or all assets — must not raise.

**D.7.1** NEAR/MID/FAR bucketing, ranked within buckets; target distance in ATR
on every row. **D.7.2** target clusters at any distance, ranked by score.
**D.7.3** no sizing, no probability — asserted over the rendered HTML.

**NOT BUILT: the reversion archetype.** Continuation drafts exist; reversion
(entry at a σ2/σ3 band actually reached, target the VWAP mean) is deferred to
cycle 5. §5 below shows why it matters.

---

## 5 · STAGE G — RECALIBRATION

### Item 6 RE-BUCKETED

| | count |
|---|---|
| **relocations** (≥ 0.15 ATR cluster width) | **12** |
| refinements (< cluster width) | 8 |
| one view only | 0 |

Cycle 2 reported "moved on 20 of 20 sides" with a median move of 0.127 ATR —
**below one cluster width**. The honest headline is **12 relocations of 20
sides**; 40% was the same structure re-centred.

### D.8 level distance, by family (1,325 levels, ten assets)

| bucket | profile_w | ss | structure | vwap_anch | vwap_roll | total |
|---|---|---|---|---|---|---|
| <1.5 (LIS-eligible) | 128 | 115 | 92 | 147 | 98 | **580** |
| 1.5–3 | 24 | 15 | 44 | 55 | 53 | 191 |
| 3–6 | 36 | 2 | 70 | 69 | 36 | 213 |
| 6–12 | 20 | 0 | 49 | 77 | 41 | 187 |
| >12 | 33 | 0 | 11 | 68 | 42 | **154** |

### D.8 sigma excursion frequency

Every asset holds ≥2 VWAPs beyond 1σ. Extremes: LITUSDT **+2.76**, ZECUSDT
**+2.60**, BTCUSDT **−2.94**. **Nothing reaches 3σ.** Only **3 thin_sample flags
across 102 VWAPs**.

### D.8 R:R by target bucket

| bucket | n | min | median | max |
|---|---|---|---|---|
| NEAR (<2 ATR) | **40** | 0.57 | 1.35 | 3.53 |
| MID (2–6) | **0** | | | |
| FAR (>6) | **0** | | | |

**Every target is under 2 ATR.** With a 148-level median registry the next
opposing cluster scoring ≥4 is always close. The bucketing guard therefore does
not currently bind — and that is exactly the gap the reversion archetype fills,
since its target is the mean, 12–21 ATR away on the far anchors.

Registry: **min 126 / median 148 / max 173** against §5.3's ~180–200.

---

## 6 · FILE DISPOSITION

| file | disposition | why | tracked | pushed | fixture |
|---|---|---|---|---|---|
| `scripts/brief2.py` | MODIFIED | D.5 stretch, D.6 excursions | yes | yes | F-B36 |
| `scripts/brief_render.py` | NEW | stage E render | yes | yes | F-B10/F-B20 |
| `scripts/brief_note.py` | NEW | operator notes + guard | yes | yes | F-B10 file |
| `scripts/brief_calibration.py` | MODIFIED | item 6 re-bucket, D.8 | yes | yes | — |
| `analytics/INTERFACE.md` | REGENERATED | was stale; APOLLO cites it | yes | yes | — |
| `analytics/*.py` | **UNTOUCHED** | no recipe changed this cycle | yes | yes | F-AN-* |
| `scripts/daily_brief.py` | **UNTOUCHED** | — | yes | yes | F-B1..8 |
| `briefs/brief_2026-08-03_post_ny.json` | REGENERATED | stretch layer added | yes | yes | F-B9/17/23 |
| `briefs/panel/*` | REBUILT `--force` | capture changed | yes | yes | F-B19/32 |
| `tests/test_brief2_render.py` | NEW | F-B10, F-B20, D.7 | yes | yes | — |
| `exchange/reports/NOTE_ARGUS_to_APOLLO_*` | NEW | D.9 routing | yes | yes | — |
| `exchange/reports/BRIEF2_CALIBRATION_*` | REGENERATED | stage G | yes | yes | — |

---

## 7 · FIXTURES

```
tests/test_analytics.py            57 passed
tests/test_brief2_volume.py        21 passed
tests/test_brief2_confluence.py    18 passed
tests/test_brief2_report.py        27 passed    + F-B36 (6)
tests/test_brief2_render.py        12 passed    NEW  F-B10 / F-B20 / D.7
tests/test_brief2_storage.py       22 passed
tests/test_forward0.py             18 passed
-----------------------------------------------------------------
FULL SUITE                        248 passed, 1 skipped
```

**Fifth instance of the same fixture bug**, fixed the same way: the
recompute scan tripped on `stoch_rsi_k`, a capture KEY the render legitimately
READS. It now tests call syntax and imports by AST. The recurring rule, now
written into the fixtures: **scan what the code DOES, never what it mentions,
and never the prose that disclaims a thing.**

Two commits this cycle were made with a failing suite and then amended (the
partition rebuild after the capture was regenerated). Recorded rather than
hidden; the fix in both cases was to run the panel rebuild before committing.

---

## 8 · FINDINGS

| id | status |
|---|---|
| anchored source `hlc3` | **CONFIRMED** — prediction held to 0.005 bps |
| variance = volume-weighted population | **VERIFIED** (2-bar anchor, √2 separation) |
| RVWAP unchanged under Source switch | **CONFIRMED** — no finding |
| **1h substrate never externally checked** | **OPEN** — decision D4-1 |
| item 6 overstated in cycle 2 | **CORRECTED** — 12 relocations, not 20 |
| D.7.1 bucketing does not bind yet | **REPORTED** — reversion archetype fills it |
| DA-2 minimum-sample rule | **PROPOSED, NOT IMPLEMENTED** |
| CONVENTIONS still says "INFERRED" | **OPEN** — should now read VERIFIED |

---

## 9 · PROVENANCE

`ANALYTICS_VERSION` **1.3.0** · sha
`da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731` ·
capture `c60eac9a330ef9d51f2b41621a9f99caf4fe62f6f3cdbd9490cbfb15b0619bc2`.

Commits: `e127869` · `4239ef7` · `6a758f6`.

---

## 10 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No engine change.
No fitted weights. No estate mutation.

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Recording is OPS; **H-VBR** and **H-VBT** are
census work under **G-7**, routed to APOLLO with their deflation gauges stated in
advance. **Adoption remains gated on parity.**

— HEPHAESTUS, 2026-08-03
