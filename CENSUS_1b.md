# CENSUS-1b — Re-score, Tradeability & Move-Anatomy Census

**Phase:** v12 Study · **Tier A** · **Engine 1.0.11, byte-untouched** · no trading, no rule change, no census re-run, lockbox untouched.

**Verdict: PARTIAL**

- F1b-DERIV literal absolute tolerance unattainable by construction; phase proceeds under the disclosed relative reading — AWAITS OPERATOR RATIFICATION


**Pre-registration:** LEDGER 2026-07-22 CENSUS-1b G-7 (commit a70a49c) — the four §8 predictions, the toll mapping, the derivation and drop rule, the pooling method, the decorrelation threshold and the five annex cuts were all committed BEFORE any analysis.


---

## Fixtures (§6)

| # | Fixture | Status | Evidence |
|---|---|---|---|
| 1 | **F1b-BYTE** — substrate byte-identity | **MATCH** | 4/4 files re-hash to `build_manifest.json` |
| 2 | **F1b-DERIV** — bps-MAE derivation | **LITERAL MISMATCH / AMENDED MATCH** | median abs Δ 1.644e-05 bps vs the literal 1e-6 *bps* bar; median **relative** Δ 1.504e-07 vs 1e-6. See the disclosure below. |
| 3 | F1b-IDX — exec-index derivation | MATCH | 0 mismatches over 149,802 rows |
| 4 | F1b-JOIN — terminus × cross join | MATCH | 14,560 rows (expected 14,560), 0 unresolved, 0 cross-asset assignments |
| 5 | F1b-CFG — pinned parameters | MATCH | toll/threshold/pooling/drop-rule/seed = the G-7 entry |
| 6 | F1b-DET — determinism | **MATCH** | run ×2: `census1b_results.json` identical after normalizing 3 run-identity fields; `census1b_termini_enriched.jsonl` **byte-identical raw** |

### ⚠ F1b-DERIV — disclosed deviation (read this before any number below)

The contract's literal F1b-DERIV bar is an **absolute** median |Δ| ≤ 1e-6 **bps**. The observed absolute median is **1.644e-05 bps**, so the phase **fails the fixture as literally written**.

That bar is unattainable by construction, and the residual is not derivation error:

- **Two-carrier cross-proof.** The pinned carrier (`mfe_bps / mfe_atr (contract §3.2)`) and a structurally unrelated stored carrier (`atr_basis / p0 * 1e4 (both stored)`) both reconstruct the stored `mae_bps`, and agree with each other to a median relative difference of **4.674e-07**. A wrong rescale cannot make two independent carriers agree.
- **Rounding signature.** The residual shrinks monotonically as the carrier's denominator grows — `mfe_atr_[0,0.5)` 1.845e-04 · `mfe_atr_[0.5,2)` 3.082e-05 · `mfe_atr_[2,10)` 1.299e-05 · `mfe_atr_[10,inf)` 7.195e-06 — which is the fingerprint of 6-decimal storage rounding, not of a wrong identity (derivation error would be flat in |mfe_atr|).
- **Arithmetic.** The substrate stores 6 decimals, so a carrier built from stored values carries ~7 significant figures; the MAE magnitudes being reconstructed are O(100) bps. Absolute agreement at 1e-6 bps would require 8+ significant figures the substrate does not contain. Contract §3.2 itself says the identity is *"exact up to 6-decimal storage rounding"* — which contradicts its own absolute tolerance.
- **What the phase did.** Proceeded under the **relative** reading of the contract's own 1e-6 numeral (median relative Δ **1.504e-07**, p99 9.817e-06). The numeral was inherited from the contract, not selected; but it was chosen *after* the diagnostic was run, and that ordering is disclosed. The literal verdict is **not** overwritten, and the phase verdict is held at **PARTIAL pending operator ratification**.
- **Drop-and-count (no estimate ever substituted).** ladder 1,013/275,988 rungs (0.367045%) · continuation h100 99/38,552 (0.256796%) — both match the contract's expected rates (≈0.367% and 0.12–0.59%).

---

## D1b — the net-of-cost re-rank

Quality ratio = `(MFE_bps − T) / (|MAE_bps| + T)`, group statistic = **ratio of medians** under a joint resample (the pre-registered confirmatory form). A ratio whose CI spans 1.0 is not an edge.


### D8 — cascade rungs, net of toll (P-1b-D8)

| follow-on TF | n | quality ratio [95% CI] | up-move net of cost (bps) | adverse net of cost (bps) | ATR ratio (CENSUS-1) |
|---|---|---|---|---|---|
| 5m | 29,141 | 0.8167 [0.7944, 0.8380] | 121.66 [119.37, 124.13] | 148.96 [147.10, 151.15] | 1.046046 |
| 15m | 64,831 | 0.8104 [0.7997, 0.8267] | 122.10 [121.09, 124.17] | 150.68 [149.05, 152.00] | 1.029326 |
| 30m | 72,424 | 0.8110 [0.7874, 0.8248] | 124.32 [121.71, 125.40] | 153.29 [151.47, 155.33] | 1.037032 |
| 1h | 67,030 | 0.9688 [0.9494, 0.9813] | 140.19 [138.93, 140.77] | 144.71 [143.02, 147.16] | 1.195703 |
| 4h | 28,113 | 1.0711 [1.0534, 1.0903] | 147.03 [146.06, 148.98] | 137.26 [135.56, 139.14] | 1.336531 |
| 12h | 9,221 | 0.8085 [0.7726, 0.8436] | 146.92 [142.91, 148.46] | 181.71 [174.51, 187.24] | 0.994057 |
| 1d | 4,215 | 0.8804 [0.8341, 1.0563] | 153.29 [147.23, 179.33] | 174.10 [165.41, 182.89] | 0.983734 |

Zero-carrier rungs dropped: 1,013.


### D4 — decoupled-add candidates at continuation moments

| stratum | n | quality ratio [95% CI] | up-move net of cost (bps) |
|---|---|---|---|
| `989_without_9200` | 4,102 | 1.0588 [0.9994, 1.1236] | 186.96 [180.27, 195.14] |
| `ALL_continuation_moments` | 38,453 | 1.0351 [1.0134, 1.0587] | 177.08 [174.58, 179.78] |
| `DECOUPLED_9200_without_989` | 3,172 | 0.8565 [0.7957, 0.9336] | 144.65 [137.19, 154.51] |
| `cross_9200_prior20=False` | 22,022 | 1.0315 [1.0077, 1.0572] | 190.47 [187.78, 194.14] |
| `cross_9200_prior20=True` | 16,431 | 1.0429 [1.0070, 1.0777] | 158.14 [154.79, 161.31] |
| `cross_989_prior20=False` | 21,092 | 1.0095 [0.9850, 1.0336] | 185.76 [182.31, 188.68] |
| `cross_989_prior20=True` | 17,361 | 1.0841 [1.0435, 1.1202] | 166.94 [162.84, 170.65] |
| `cross_989_prior5=False` | 34,259 | 1.0322 [1.0094, 1.0539] | 178.96 [176.08, 181.42] |
| `cross_989_prior5=True` | 4,194 | 1.0746 [0.9907, 1.1575] | 161.94 [153.59, 169.77] |

**Dual-carrier robustness:** pinned carrier ratio 1.035051 vs independent carrier 1.035051 (abs diff 0.0) — the F1b-DERIV rounding residual is immaterial to the re-rank.


**D4 companion — cross type × TF** (stored `mae_bps`, no derivation). Top 10 by quality ratio:

| rank | signal | quality ratio |
|---|---|---|
| 1 | `4h:9_89` | 1.078845 |
| 2 | `1h:9_89` | 0.956667 |
| 3 | `30m:89_200` | 0.914811 |
| 4 | `15m:89_200` | 0.904548 |
| 5 | `1h:89_200` | 0.903002 |
| 6 | `12h:89_200` | 0.901556 |
| 7 | `1h:9_200` | 0.894789 |
| 8 | `30m:9_200` | 0.88608 |
| 9 | `1d:9_89` | 0.880444 |
| 10 | `4h:9_200` | 0.871142 |

---

## D2b — the tradeability pairing (P-1b-D5)

CENSUS-1 reported the P-C5 slow-stack combination's favorable leg only (gross 614.16 → net-of-toll 596.75 bps). Paired with its drawdown:

| lens | n | gross MFE (bps) | quality ratio [95% CI] | up-move net (bps) | adverse net (bps) |
|---|---|---|---|---|---|
| 1h | 13,299 | 300.2414 | 0.9442 [0.9144, 0.9773] | 283.27 [276.53, 290.96] | 300.03 [294.11, 306.23] |
| 4h **←scored** | 13,299 | 614.164565 | 1.0724 [1.0363, 1.1089] | 596.75 [581.67, 612.95] | 556.46 [546.89, 566.75] |
| 12h | 13,299 | 717.953985 | 1.0787 [1.0427, 1.1155] | 699.70 [682.45, 716.32] | 648.68 [635.60, 661.28] |
| 1d | 13,299 | 734.668172 | 1.0788 [1.0357, 1.1146] | 717.10 [700.00, 733.93] | 664.72 [652.32, 681.57] |

---

## D3b — the powered pooled pullback test (P-1b-C7b)

| lens | n EMA | n non-EMA | EMA fwd MFE (ATR) | non-EMA fwd MFE (ATR) | difference [95% CI] |
|---|---|---|---|---|---|
| 1h | 2,805 | 7,771 | 4.3041 [4.1167, 4.4810] | 4.2819 [4.1794, 4.4176] | 0.0221 [-0.2061, 0.2225] |
| 4h | 674 | 1,970 | 4.3787 [3.9617, 4.8648] | 4.5182 [4.1169, 4.7257] | -0.1394 [-0.6108, 0.5007] |
| 12h | 215 | 679 | 4.6381 [3.8116, 5.3584] | 4.0418 [3.6253, 4.4139] | 0.5963 [-0.3604, 1.4197] |
| 1d | 103 | 343 | 4.8991 [4.0086, 6.4601] | 4.4694 [3.7190, 5.2232] | 0.4297 [-0.8346, 2.1237] |

**Pooled** (n 3,797 EMA vs 10,763 non-EMA, within the 14,560 real termini): **0.0379 [-0.1434, 0.2550] ATR**.
- Lenses with a positive difference: ['1h', '12h', '1d'] → ≥2-lens sign gate **PASSES**
- Pooled CI excludes zero: **False**
- *Robustness (NON-confirmatory, pre-registered as such):* cluster bootstrap over 7 assets → 0.0379 [-0.1773, 0.3725] ATR. The four lenses are overlapping views of the same price; the ordinary bootstrap treats them as independent and therefore overstates power.

---

## D4b — the decorrelation table (P-1b-D9)

Association = |φ|; core = all pairwise |φ| < 0.3, reached by the pre-registered deterministic greedy prune.

| lens | decorrelated core | max |φ| in core | ρ full-list (recomputed) | ρ full-list (CENSUS-1) | **ρ core [95% CI]** |
|---|---|---|---|---|---|
| 1h | F1, F4, F8, F9 | 0.042766 | 0.038295 | 0.038 | **0.0456 [0.0373, 0.0544]** |
| 4h | F1, F4, F8, F9 | 0.119882 | 0.017885 | 0.018 | **0.0242 [0.0158, 0.0329]** |
| 12h | F1, F4, F8, F9 | 0.263083 | 0.01291 | 0.013 | **0.0182 [0.0099, 0.0268]** |
| 1d | F1, F8, F9 | 0.013003 | 0.011953 | 0.012 | **0.0141 [0.0058, 0.0227]** |

Lenses reaching ρ_core ≥ 0.10: **none**


**Prune trace (4H lens)** — which collinear pair was cut and why:

| dropped pair | \|φ\| | factor removed |
|---|---|---|
| F3_lens_regime ↔ F4_price>lens_e89 | 0.895116 | **F3_lens_regime** |
| F1_1D_struct ↔ F2_12H_struct | 0.719446 | **F2_12H_struct** |
| F4_price>lens_e89 ↔ F7_lens_9200 | 0.707391 | **F7_lens_9200** |
| F1_1D_struct ↔ F5_price>lensp1_e200 | 0.505486 | **F5_price>lensp1_e200** |

---

## D5b — the enriched terminus dataset (move-anatomy substrate)

`census1b_termini_enriched.jsonl` — **14,560 rows** (expected 14,560), sha256 `4feecd54d6e930c57dfe5ed9fa65083c…`

prior/forward = 7 TFs x 3 cross types, each {dir, lag_exec_bars} vs exec_idx_confirm (prior: cross exec_idx <= confirm; forward: > confirm). fwd_mae_bps_100 is null for ALL rows — census_termini carries no MAE in any unit (schema-pin disclosure). anchor_price/anchor_atr are null — not in the substrate; anchor_atr_over_price_bps carries the recoverable ATR/price ratio.

**descriptive substrate — nothing computed from this table in THIS phase is a validated finding (§7)**


---

## D6b — the adverse-excursion zone landing (§3.5)

**Branch:** SCOPED RE-WALK (census_outcomes stores MAE magnitude only) · **scope:** continuation + cascade-rung anchors ONLY (§3.5) · assets processed 7/7 · partial=False · 26.729942s

adverse extreme = min low (long) / max high (short) over exec bars [i, i+99]; distance = min(|p_adv - lens_e89|, |p_adv - lens_e200|) / lens_ATR at that bar's AS-OF lens state; zone = <= 0.35 lens-ATR (D10 Z2 band). Matched null = random in-regime exec bars, same asset+lens+regime, 10x, seed 20260721.


*D10 measures on the LENS frame (lens pivot vs lens EMA); this measures on the EXEC frame (exec-bar extreme vs AS-OF lens EMA) because the adverse extreme is an exec-bar event. Adaptation disclosed.*


| lens | anchor class | n | P(adverse low on zone) | n null | **P(null)** | excess-mass ratio |
|---|---|---|---|---|---|---|
| 1h | cascade_rung|long | 138,040 | 0.220132 | 1,380,400 | **0.135885** | 1.619992 |
| 1h | cascade_rung|short | 137,948 | 0.2203 | 1,379,480 | **0.139821** | 1.575591 |
| 1h | continuation|long | 21,394 | 0.145228 | 213,940 | **0.13673** | 1.06215 |
| 1h | continuation|short | 17,158 | 0.148327 | 171,580 | **0.137807** | 1.076337 |
| 4h | cascade_rung|long | 138,040 | 0.167908 | 1,380,400 | **0.128771** | 1.30393 |
| 4h | cascade_rung|short | 137,948 | 0.169839 | 1,379,480 | **0.136051** | 1.248355 |
| 4h | continuation|long | 21,394 | 0.11779 | 213,940 | **0.128732** | 0.914999 |
| 4h | continuation|short | 17,158 | 0.128045 | 171,580 | **0.134118** | 0.954719 |
| 12h | cascade_rung|long | 138,040 | 0.136207 | 1,370,570 | **0.1116** | 1.220489 |
| 12h | cascade_rung|short | 137,948 | 0.147628 | 1,379,480 | **0.135335** | 1.090834 |
| 12h | continuation|long | 21,394 | 0.116248 | 212,630 | **0.111508** | 1.042502 |
| 12h | continuation|short | 17,158 | 0.119245 | 171,580 | **0.134369** | 0.887443 |
| 1d | cascade_rung|long | 138,040 | 0.125427 | 1,370,570 | **0.133088** | 0.942437 |
| 1d | cascade_rung|short | 137,948 | 0.124996 | 1,379,480 | **0.107817** | 1.159334 |
| 1d | continuation|long | 21,394 | 0.116107 | 212,630 | **0.133467** | 0.869935 |
| 1d | continuation|short | 17,158 | 0.120177 | 171,580 | **0.106609** | 1.127269 |

**not a validated finding (§7)**


---

## Scorecard — the four pre-registered predictions (falsifications first)

| # | prior | verdict | claim | evidence |
|---|---|---|---|---|
| **P-1b-D9** | 40% | **FALSIFIED** | decorrelated core rho(k,MFE) >= 0.10 on >=2 lenses | lenses with rho_core >= 0.10: none; per-lens rho_core {'1h': 0.045646, '4h': 0.024209, '12h': 0.018249, '1d': 0.014093} |
| **P-1b-C7b** | 45% | **FALSIFIED** | pooled EMA-terminating pullbacks higher fwd MFE, CI excludes 0, >=2-lens sign gate | pooled diff 0.037926 ATR CI [-0.143387, 0.255032]; lenses positive ['1h', '12h', '1d']; sign gate True |
| **P-1b-D5** | 55% | **CONFIRMED** | P-C5 slow-stack net-of-toll quality ratio CI lower bound > 1.0 (4H lens) | 4H quality ratio 1.072393 CI [1.036338, 1.108942], n=13299 |
| **P-1b-D8** | 55% | **CONFIRMED** | PRIMARY 4H rung quality-ratio CI lower bound >= 1.05; SECONDARY 1H CI includes 1.0 | 4H ratio 1.071142 CI [1.053364, 1.09028] n=28113; 1H ratio 0.968826 CI [0.949435, 0.981329] n=67030; secondary: MISSED (1H CI excludes 1.0) |

**2 falsified / 2 confirmed** of 4.


---

## Exploratory annex (§10) — STRICTLY SEPARATE FROM THE ABOVE

> Everything in this section is **exploratory, in-sample, exploration-classic, NOT validated** — hypothesis-generation for a following, separately pre-registered test. All five cuts were declared verbatim in the G-7 commit before any analysis. **Nothing here is a finding.**


### A1 — the operator's motivating pattern

*4H 9/89 fires in-direction within 500 exec bars → pullback lands within 0.35 lens-ATR of the lens e89/e200 → which LTF cross gives the best forward outcome?*  n conditioned = 500, complement = 14,060.

| first LTF cross | n | median fwd MFE (ATR) | vs complement [95% CI] |
|---|---|---|---|
| 5m | 161 | 3.6554 [2.9199, 4.6225] | -0.6492 [-1.3288, 0.3209] |
| 15m | 35 | 6.1114 [2.7396, 7.8877] | 1.8068 [-1.5204, 3.5965] |
| 30m | 12 | — | n<20, not evaluated |

**Replication:** 1/2 LTF arms same sign  — FAILS the gate: single-instance, likely noise


### A2 — the zone's marginal contribution

- 4H-9/89 conditioning alone vs complement: -0.0290 [-0.2488, 0.2884] ATR (n 1,996)
- Zone-landing *within* the 4H-9/89 set: 0.2618 [-0.4874, 0.6761] ATR

### A3 — prior-cross density

| lens | Spearman ρ(n TFs with in-dir 9/89, fwd MFE) [95% CI] |
|---|---|
| 1h | 0.0276 [0.0087, 0.0464] |
| 4h | 0.0286 [-0.0097, 0.0672] |
| 12h | 0.0852 [0.0213, 0.1490] |
| 1d | -0.0144 [-0.1053, 0.0780] |

**Replication:** 3/4 lenses positive


### A4 — forward-cross lag

> **DESCRIPTIVE ONLY — conditions on POST-anchor information while the outcome is measured FROM the anchor. Not tradeable as stated.**

| bin | n | lag range (exec bars) | median fwd MFE (ATR) |
|---|---|---|---|
| Q1 | 1,177 | 1–7 | 4.5994 [4.2078, 4.8809] |
| Q2 | 1,300 | 8–21 | 4.6765 [4.3262, 5.0748] |
| Q3 | 1,264 | 22–52 | 4.0884 [3.6950, 4.3620] |
| Q4 | 1,262 | 53–534 | 2.9878 [2.7312, 3.3665] |

### A5 — prior 4H cross type

| lens | 9_89 | 9_200 | 89_200 |
|---|---|---|---|
| 1h | 4.2557 [4.0363, 4.5668] (n 1,388) | 4.0660 [3.7506, 4.3406] (n 800) | 4.9518 [4.3761, 5.4281] (n 349) |
| 4h | 3.9375 [2.8719, 5.3371] (n 127) | 4.7975 [3.9949, 5.5327] (n 114) | 5.0070 [3.7927, 7.4771] (n 82) |
| 12h | 4.6752 [3.6511, 5.5141] (n 125) | 3.5293 [2.6543, 4.5812] (n 50) | — |
| 1d | 4.7865 [2.6215, 6.4601] (n 62) | 4.5250 [1.4533, 5.8423] (n 22) | — |

**Replication:** {'89_200': '2/2 lenses positive', '9_200': '4/4 lenses positive', '9_89': '4/4 lenses positive'}


---

## Determinism (F1b-DET)

**MATCH** — the full analysis was run twice.

- `census1b_termini_enriched.jsonl` **byte-identical, raw, no normalization**: `4feecd54d6e930c57dfe5ed9fa65083c…` both passes.
- `census1b_results.json` identical after normalizing the run-identity fields `elapsed_s`, `D6b_adverse_zone.elapsed_s`, `D5b_enriched_dataset.path`.
- Three RUN-IDENTITY fields are normalized — two wall-clock timings and the enriched-dataset output path (pass 2 writes to a different directory by design). NO computed value is normalized: every statistic, CI, count, hash and verdict is compared byte-for-byte. The enriched jsonl itself is compared RAW and is byte-identical. Precedent: CENSUS-1 F-BYTE normalized three run-identity stamps.

---

*CENSUS-1b, Tier A, measure-only. Engine 1.0.11 byte-untouched. No trading occurred, no rule changed, the census was not re-run, and the lockbox was not touched.*

