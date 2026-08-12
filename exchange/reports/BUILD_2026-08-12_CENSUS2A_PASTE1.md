# CENSUS-2A · PASTE #1 — MC-2 (EXTENDED) + CEN-0 · BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Contract:** `exchange/reports/CENSUS2A_CONTRACT_DRAFT_v0.2_2026-08-12.md`
**Class:** this document is EVIDENCE about the estate; the MC-2 constants it reports are **DISPLAY-ONLY — post-lockbox live-era data — hypothesis generation only, never evidence.**
**Seed:** 20260812 · **Programs:** `scripts/mc2_program.py` (new), `scripts/cen0_inventory.py` (new)

---

## 0 · WHAT THIS IS, AND WHAT IT IS NOT

The contract is stamped **DRAFT — NOT EXECUTABLE** and gates itself on three ordered conditions:

> (1) census paste #1 returns (MC-2 amended + CEN-0) and its outputs replace every ⟨MC2⟩ placeholder, diff-listed → (2) operator reviews the resolved text → (3) operator stamps **RATIFIED**

**This document is condition (1).** No scored census table appears here, no registration is scored, and no trading rule is adopted. The census remains un-run and un-runnable until (2) and (3) complete.

**The headline finding, stated before the evidence:** MC-2 did not exist. Not as a script, a queue item, or a `D:` artifact — `find` across both drives returned zero matches for `*mc2*`. The claim in the lane status note that it was "drafted, D:-resident" was not corroborated by `D:`, whose `research_outputs/` held exactly `{_archive, census, mc1, seq8, seq8_run2}`. Its entire specification of record was **one sentence** at `APOLLO_LANE_UPDATE_and_CENSUS2_STATUS_2026-08-12.md:22`. It has now been built and run.

**Second finding, structural:** MC-2 **as commissioned** could never have satisfied condition (1). Its commissioned scope — relay lag distributions, nested-cross scan, 25-observatory, +EMA500, two query cards — pins placeholders (iii), (iv) and (vi) and produces **nothing** for (i) kiss/refusal, (ii) TRAP counter-density, or (v) ribbon-compression `c`. The contract's line 3 promise that paste #1 "replace[s] **every** ⟨MC2⟩ placeholder" was false against the very commission it depended on. Five of the six placeholders sit inside D-CEN2a, the module the contract crowns. On operator decision (2026-08-12) MC-2's scope was **extended** to cover all six; all three additional measurements were computable from data already on disk, so the extension cost no fetch.

---

## 1 · THE ONE DESIGN DECISION THE CONTRACT DOES NOT MAKE

The contract's I1 bounds every **scored** table at the 2024-07-01 evidence wall. It says nothing about where the census's own **constants** may be measured — and that silence is load-bearing, because constants fitted on the same bars a study then scores are in-sample selection wearing a different hat.

**Decision taken:** every constant is pinned on the **live era** (`open_time >= CEIL_MS`), which is disjoint from the evidence era the census scores. The evidence-era value of each statistic is computed and printed beside it — measured, never used to pin. This is why MC-2's artifacts carry the DISPLAY-ONLY banner: that label is not a demotion here, it is what makes the constants admissible.

The decision is **reversible**: `python scripts/mc2_program.py --era evidence` re-pins everything in-sample and emits the same tables to a separate directory. Both runs were executed; §5 prints them side by side. **This is the single largest judgement call in paste #1 and is flagged for the condition-(2) review.**

---

## 2 · FIXTURES — all executed, all passing

| Fixture | What it proves | Result |
|---|---|---|
| **F-1** identity + `drive_wait` | I3 two-sided identity; I2 drive gate | **PASS 6/6** + `PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s` |
| **F-PARITY** loader | the frame builder agrees with `census_build.load_tf` on the warm overlap (`close`, `e9`, `e89`, `e200`, `atr`) | **PASS 6/6** cells — restricted to bars warm in *both*, with the excluded count printed; see §7A #1 for why the earlier form of this fixture was misleading |
| **F-PARITY-2** cold head *(new)* | zero crosses detected inside the EMA warm-up region — I4's "NaN before warm" is effective, not just asserted | **PASS** — 0 cold-head crosses across all assets × {9_89, 9_200, 89_200} |
| **F-KISS-PARITY** *(new)* | the parameterised kiss detector is bit-identical to `mc1_program.kiss_v0` at the ratified point, so the sweep confirms the ratified constant rather than a lookalike | **PASS** on all 5 panel assets; HALTs if it ever diverges |
| **F-3** feasibility matrix | 7 assets × 7 TFs × 8 EMAs warm/never, 3 cells hand-recomputed | **PASS** — 392 cells; hand cells ETH·1d·500, BTC·4h·500, SOL·12h·450 |
| **F-DET** determinism | one scored deliverable re-runs hash-identical | **PASS** — `obs25_table` `db339f22fc82`, `trap_sweep` `b50996a5aa4d` reproduced exactly |
| **F-12** PAXG classification | printed rather than assumed | **PASS** — printed as ABSENT, §4 |

**F-DET's limit, stated:** it hashes the emitted *table*, not the *pin*. When the selection guard flipped TRAP from `≥5` to NOT ESTABLISHED, `trap_sweep.parquet`'s hash was unchanged — the sweep is identical, only the decision drawn from it moved. A determinism fixture scoped to artifacts cannot catch a changed conclusion; the pins live in the manifest and need their own check.

I3 is prose in the contract and implemented **nowhere** in the estate — no code anywhere asserts branch, remote, or the OneDrive exclusion. It is therefore re-implemented inline in `mc2_program.stage_preflight`, which is the point: a gate that lives only in a document is not a gate. Note also that `wait_for_drive` **never raises by design**, so the HALT is the caller's; every entry point here wraps it in an explicit `SystemExit`.

---

## 3 · CEN-0(a) — PANEL READINESS

Read-only inventory of the candle estate at `%LOCALAPPDATA%\naiad\data_cache\klines` (60 series). Full table: `D:/Naiad/research_outputs/census2a/cen0_panel_inventory.parquet`.

| Asset | Role | State | Evidence-era 4h | EMA500 @4h | Gaps |
|---|---|---|---:|---|---:|
| BTCUSDT | panel | **READY** | 10,544 bars (4.81y) | WARM | **1** |
| ETHUSDT | panel | **READY** | 10,067 bars (4.60y) | WARM | 0 |
| ZECUSDT | panel | **READY** | 9,646 bars (4.40y) | WARM | 0 |
| SOLUSDT | panel | **READY** | 8,315 bars (3.80y) | WARM | 0 |
| NEARUSDT | panel | **READY** | 8,128 bars (3.71y) | WARM | 0 |
| JTOUSDT | annex | SHORT-HISTORY | 1,234 bars (0.56y) | NEVER | 0 |
| TAOUSDT | annex | SHORT-HISTORY | 483 bars (0.22y) | NEVER | 0 |
| PAXGUSDT | requested | **ABSENT** | — | — | — |

**Exactly one gap across all 42 present series, and zero duplicate bars.** The gap is a single missing 1m bar on BTCUSDT at 2019-09-08 19:00 (largest gap = 2 intervals), pre-wall and materially trivial — but it is *not* zero, and an earlier draft of this document claimed zero while the artifact it cites said otherwise. Every series is strictly monotonic. Live-era coverage runs to 2026-08-12.

Why one bar is worth a sentence: the census anchors outcome horizons in **bar counts**, so any horizon spanning a gap is silently shortened, and the shortening is invisible in every summary statistic. One bar changes nothing here; the discipline of counting them is what matters when PAXG or a TradFi panel with session breaks arrives.

## 4 · CEN-0(b) — PAXG

**ABSENT from the cache.** Acquisition requires a network fetch, which paste #1 was scoped to exclude by operator decision (2026-08-12). Two facts for the follow-up:

- PAXGUSDT is **not** in `engine/cells.py:SYMBOLS`. The contract's I10 forbids an engine change, so the fetch must pass the symbol explicitly and registration is a separate queue item.
- Its classification under CEN-0(b) (≥2y evidence-era → panel-eligible, else annex) **cannot be predicted** — PAXG's Binance perp listing date decides it, and that is unknown until fetched.

---

## 5 · THE SIX PLACEHOLDERS — RESOLUTION REGISTER

Method note: every promotion below requires a **measured** effect — a bootstrap 90% CI (2,000 resamples, seeded) on the median net-excursion difference that excludes zero — not merely a direction. A five-asset sign test at these sample sizes points somewhere on noise; the contract's own registrations use the "CI excl. 0" standard and so does this. Net excursion = MFE − MAE in ATR at the anchor, at horizon 100.

**Second method note, added after adversarial review of this build.** A CI is not a correction for having searched. Where a stage *sweeps* candidates and promotes a winner, the selection procedure itself is now tested: the statistic is **max |separation| across the swept candidates** — the quantity the promotion rule maximises — and its null is built by shuffling outcome labels. The stage declines to pin unless the selection-corrected p clears the contract's own FDR bar (I8, q = 0.10 over the family of m candidates). **This caught and withdrew two pins — (ii) TRAP `≥5` and (iv) `30m-in-4h`** — both of which looked significant uncorrected. Where a stage tests a **pre-named** constant instead, no search occurs and the guard does not apply.

**Third note: the unit of replication.** A five-asset panel claim asserts replication *across assets*, so promotions are decided by an **asset-cluster bootstrap** (resampling the five assets), not a row bootstrap that treats overlapping forward windows as independent. This changes conclusions: TRAP's effect vanishes under clustering, while (vi)'s `25_89` survives it in both eras.

| # | Placeholder | Fallback | **LIVE (pin)** | EVIDENCE (beside) | Verdict |
|---|---|---|---|---|---|
| i | kiss ε / δ / k | 0.25 / 0.75 / 10 | **0.25 / 0.75 / 10** | same | **CONFIRMED** (detector asserted == `mc1_program.kiss_v0`) |
| ii | TRAP counter-density | ≥2 | *not established* | *not established* | **FALLBACK REJECTED, no admissible replacement** |
| iii | window `W_max` | 90 4h bars | **151** CI [112.8, 186.0] | 160 | **FALLBACK REJECTED** (90 below the CI) |
| iv | nested pair set | {1h-in-4h, 30m-in-4h, 30m-in-1h} | *inconclusive* | *inconclusive* | **UNRESOLVED** |
| v | ribbon-compression `c` | 0.5×ATR | **0.5** (14.8% of 1h bars) | 0.5 (14.7%) | **CONFIRMED** |
| vi | 25-pair inclusion | included (both) | **`25_89` only** | `25_89` only | **REFINED** (survives asset-cluster CI) |

**Four of six resolved, two not.** (i), (v) confirmed; (iii) pinned; (vi) refined. (ii) and (iv) are **not established**, so the contract's condition (1) — "replace **every** ⟨MC2⟩ placeholder" — is **not met by this paste and is not represented as met.**

### (i) kiss ε/δ/k — CONFIRMED, not re-fitted
MC-1's ratified constants *are* the contract's fallback (`mc1_program.py:108-110`). A sandbox does not overturn a ratified constant, so the sweep (75 combinations) exists to show the point is stable rather than to move it: 545 refusal events panel-wide, minimum 92 per asset. **Honest caveat:** local stability is only moderate — the count spans **65.3%** of the centre value under a ±1-step perturbation of ε and k. The constant is defensible but sits on a gradient, not a plateau.
**Scope limit, filed not defaulted:** this pins the **EMA↔EMA limb only** (i-a). The price↔level limb (i-b) — D-B's SFP/deviation object — has **no detector anywhere in the estate** (`seq8_extract.py:97-98` records the gap). Inventing one inside a constants sandbox would be exactly the unregistered machinery the frame forbids. **It remains open work.**

### (ii) TRAP counter-density — the fallback is a null gate, and its replacement was a selection artifact
`≥2` fires on **91.5%** of live-era (744/813) and **92.1%** of evidence-era (1448/1573) 4h lattice-A armings. A stamp true of nearly the whole population cannot discriminate — it is a null gate in the costume of a filter, and it was feeding the crown's discriminant set. **Rejecting ≥2 is robust**: it rests on a fire rate, which is a descriptive fact about the population and requires no inference at all.

**Independent cross-validation of the substrate.** MC-2 recomputes lattice-A crosses from raw klines; MC-1 read them from the SEQ8 event stream. On the evidence era the two agree to **4 events in 1,569 (0.25%)** — MC-2 1,573 armings / 1,448 TRAP-true (92.05%) vs MC-1's `d4_similarity.parquet` 1,569 / 1,447 (92.22%). Two independent paths to the same population is a meaningful check on the new loader. **The 4-event delta is not explained**; the likely candidate is warmup/boundary treatment at series start (SEQ8 applies its own warmup gate), but that was not isolated and should not be asserted. It is filed for F-7-style reconciliation.

**The replacement does not survive, and this correction was found in our own work.** An earlier draft of this stage pinned `≥5` — the only threshold in the 10–85% fire-rate band whose separation CI excluded zero (fires 69.1%, separation −1.73 ATR, CI [−2.79, −0.14], 4/5 assets). That is a **multiple-comparisons artifact**. Twenty correlated thresholds were swept and the winner selected on the strength of its own interval; a CI is not a correction for having looked twenty times.

Three independent measurements of the *procedure* (label shuffles destroy any real association while preserving the `counter_n` structure) agree it fires on noise: **42.0%** (ad-hoc, seed A), **37.7%** (in-program, seed 20260812), **43.5%** (independent adversarial review). A rule with a ~40% false-positive rate has not measured anything.

The guard now reports a **selection-corrected p-value** rather than that cruder pass/fail rate, because the question is not "did *some* threshold pass" but "is the **winner's** effect bigger than the winner of a null sweep". Test statistic = max |median separation| over the in-band thresholds — the same quantity the pin rule maximises — with 2,000 shuffles:

```
selection test (max-statistic permutation, m=11 in-band thresholds, 2000 shuffles):
  winner >=5  |sep|=1.734334  null p95=2.625644
  p uncorrected (winner alone) = 0.0245
  p SELECTION-CORRECTED        = 0.2874
  I8 admissibility bar (BH, q=0.10 over m) = 0.00909
!! NOT ADMISSIBLE: selection-corrected p=0.2874 exceeds the I8 bar 0.00909.
   >= 5 is a SELECTION ARTIFACT, not a measurement. Declining to pin.
```

Note what the two p-values do: uncorrected, `≥5` looks significant (0.0245). Corrected for having searched eleven thresholds, it is **0.287 — inadmissible by 32× against the contract's own FDR standard** (I8, q=0.10 over a family of m=11). Evidence era is worse still: p = 0.528. **`≥5` is withdrawn; (ii) is NOT ESTABLISHED.**

**A fourth, independent reason to withdraw it.** Under an **asset-cluster bootstrap** — resampling the five assets rather than the 813 rows, which is what a five-asset panel claim actually asserts — the TRAP effect at `≥5` gives CI **[−2.333, +0.059]**, straddling zero. The row bootstrap treats overlapping forward windows as independent observations; they are not. The effect does not survive the correct unit of replication even before the multiplicity correction.

**Scoping the correction honestly.** The same question was asked of the other stages rather than applied only where it was first noticed:
- **(vi) 25-pair** — null rate **15.2%** *(ad-hoc scratch computation, 400 shuffles, **not** committed code — see the caveat under (vi) below; the guard is implemented only for (ii))*, consistent with ordinary 2-test multiplicity (1−0.9² = 19%). `25_89` and `9_25` were **pre-named by the contract**, not selected as the max of a sweep. The promotion stands, with multiplicity noted as a caveat.
- **(iv) nesting** — six pairs swept, but the stage returned INCONCLUSIVE, so no selection occurred and nothing needs withdrawing.
- **(i) kiss and (v) ribbon** — no sweep-selection: both CONFIRM a pre-ratified constant rather than choosing one.

**What remains true about TRAP:** the fallback ≥2 is unusable, and no replacement has been established on either era. The stamp should be dropped from D-CEN2a's discriminant set or re-scoped — not silently re-thresholded.

### (iii) `W_max` — pinned by survival analysis, because the naive quantile does not exist

The contract's rule is "relay-lag p90 decides". Executing that literally is a trap, and an earlier draft of this document fell into it.

**The window closes at the counter-arming, so the lag is censored — heavily.** Because 9/89 crossovers strictly alternate, the window *is* the 9/89 regime: median width **28 4h bars** (live). The 400-bar observation cap binds on **5 of 436** armings. So taking the p90 of the completed subset conditions on survival, and taking a p90 over all armings is worse — **survival never falls to 0.10, so that quantile does not exist.** Kaplan-Meier separates the two questions:

| | live | evidence |
|---|---:|---:|
| armings | 436 | 848 |
| fates (disjoint) | ABORTED 367 · COMPLETED 64 · ROTTED 5 | ABORTED 734 · COMPLETED 111 · ROTTED 3 |
| **never complete (KM S∞)** | **45.1%** | **41.6%** |
| naive p90, completed-only *(biased)* | 108 | 123 |
| **KM p90 among eventual completers** | **151** | **160** |
| 90% bootstrap CI on the KM p90 | **[112.8, 186.0]** | **[144.0, 171.0]** |

**`W_max` = 151 4h bars (live).** The fallback of 90 sits **below the CI lower bound of 112.8**, so its rejection is supported with an interval rather than a point. This matters: the *naive* p90's own CI is [91, 128], which excludes 90 by a single bar — an adversarial review flagged that as too thin to carry the word "rejected", and it was right. The KM estimate is what makes the rejection safe.

**Is 151 an artifact of the 400-bar cap?** No — tested directly. The KM conditional p90 is **151 for every observation cap ≥ 200** (150 → 126; 200, 300, 400, 600, 900 → 151), and `S∞` is likewise flat at 0.451. The estimator is not a readout of the cap. *(The naive estimator does collapse if you feed the pin back as the prescribed window — 400 → 108 → 90 → 75 → … — but that is the censoring bias, which is exactly what KM corrects.)*

**The blunter finding.** `W_max` is **near-non-binding in practice**: the counter-arming closes the window first in **98.9%** of armings, at a median width of 28 bars against any candidate `W_max` of 90–160. Whatever the operator pins, it will govern roughly one arming in a hundred. That is worth knowing before the constant is argued over.

And: **the full 9/89 → 9/200 → 12/25 relay completes on only 14.7% of armings** (64/436); 284 never reach even the second leg. The May-26 anatomy is not the common case — D-CEN2a should expect ABORTED to dominate its own crown table.

### (iv) nested pair set — UNRESOLVED, and the fallback stands unconfirmed
Six candidate pairs tested. Prevalence is usable everywhere (8.5%–13.8%).

- **Live:** no candidate's separation CI excludes zero. Inconclusive outright.
- **Evidence:** three candidates' CIs exclude zero — but two are *negative* (`15m-in-1h` −1.58, `5m-in-1h` −1.50) and the one positive winner, `30m-in-4h` (+1.78, 4/5 assets), has a CI lower bound of **0.024** — a hair from zero, selected as the best of six.

**`30m-in-4h` was withdrawn by the same selection guard that withdrew TRAP:** max-statistic permutation over the six candidates gives **p = 0.549 against an I8 bar (BH, q=0.10, m=6) of 0.0167** — inadmissible by 33×. It cleared the CI screen and failed the correction for having searched.

This is worth stating plainly because it is a live demonstration of the risk §7A names: `30m-in-4h` appeared only *after* the warm-up and horizon fixes changed the populations, in the one stage that was still unguarded at the time. Extending the guard to this stage was not a precaution — it caught something.

**Consequence:** the fallback set is carried forward **UNCONFIRMED**, and (iv) is *not* resolved by this paste. Either the census's own larger event population settles it, or the operator pins it by name [VETO]. An earlier draft of this stage also "pinned" `5m-in-1h` on a **+0.0198 ATR** separation — a sign test dressed as a result; that too was removed rather than shipped.

### (v) ribbon-compression `c` — CONFIRMED, with a stated limit
`c = 0.5×ATR` flags **14.8%** of 1h bars panel-wide (30m: 14.9%), inside a 10–25% admissible band. **Limit, stated plainly:** selectivity is the only property of `c` this sandbox can measure without a chop *label* to score against — and that label is CEN-4's output, not its input. Selectivity can **reject** a `c` (1.5×ATR flags 44% of the tape, adding a constant to the composite rather than a signal) but cannot **order** two admissible ones. The admissible set {0.35, 0.5, 0.65, 0.8} is equally defensible on the available evidence; the ratified 0.5 is retained because moving it to hit a rounder selectivity target would be fitting with extra steps.

### (vi) 25-pair inclusion — REFINED, and this one matters for the FDR family
Promotion is decided by the **asset-cluster** CI (resampling the five assets), not the row CI — a five-asset panel claim asserts replication across assets, and the row bootstrap treats overlapping forward windows as independent when they are not. Both are printed; where they disagree the cluster version governs.

**LIVE era:**

| Class | n | median net (ATR) | row CI | **cluster CI** | Excl. 0? | count vs 9_89 |
|---|---:|---:|---|---|---|---:|
| 9_89 (reference) | 436 | 0.962 | [0.158, 2.148] | **[0.545, 1.760]** | ✅ | 1.00× |
| **25_89** | 285 | 0.822 | [0.041, 1.892] | **[0.352, 1.527]** | ✅ | 0.65× |
| 12_25 (incumbent) | 862 | 0.271 | [−0.328, 0.723] | [−0.319, 0.639] | ❌ | 1.98× |
| **9_25** | 956 | 0.079 | [−0.366, 0.481] | [−0.231, 0.498] | ❌ | **2.19×** |

**EVIDENCE era** (populations differ; see the warm-up note in §6):

| Class | n | median net (ATR) | **cluster CI** | Excl. 0? |
|---|---:|---:|---|---|
| 9_89 (reference) | 848 | 0.224 | **[0.130, 0.332]** | ✅ |
| **25_89** | 500 | 0.862 | **[0.493, 1.287]** | ✅ |
| 12_25 (incumbent) | 1,566 | −0.025 | [−0.194, 0.456] | ❌ |
| **9_25** | 1,816 | 0.057 | [−0.179, 0.384] | ❌ |

**`25_89` earns inclusion; `9_25` does not.** `9_25` is the most numerous class on the board at 2.19× the reference and the weakest measured — admitting it unstratified would let one class set the discovery budget for nine registrations at q=0.10. Note in passing that the **incumbent `12_25` also fails** this bar; that is not a placeholder and is not decided here, but D-CEN2b should know it.

**The verdict replicates across eras and across bootstrap schemes; the magnitudes do not.** `25_89`'s median net is 0.822 live vs 0.862 evidence, but the reference class `9_89` moves from 0.962 to 0.224 and `12_25` flips sign. Only the include/exclude decision is stable — which is the claim being made, but the table should not be read as era-invariant.

**Multiplicity caveat, still standing.** Two pre-named classes were tested, so the family-wise false-positive rate is roughly 1−0.9² ≈ 19%; an ad-hoc permutation check (400 shuffles, scratch script, **not committed code**) gave 15.2%, consistent with that. This is ordinary multiplicity across hypotheses the *contract* named — materially different from (ii)'s selection from a 20-threshold sweep — but it is not nothing. `25_89`'s inclusion should be re-tested inside the census's own FDR family rather than treated as settled here.

### The diff-list hazard
The contract keys its diff on "every ⟨MC2⟩ placeholder" (L3). There are **9 placeholder tokens: 8 spelled `⟨MC2⟩`, and one spelled `⟨W_max⟩` at L99.** A token-keyed diff silently misses (iii) — the placeholder whose fallback is measurably wrong. Resolved tokens by line: L38 (i, ii, iv, v, vi), L91 (i), L93 (iv), L99 ⟨MC2⟩×2 (i, ii), **L99 ⟨W_max⟩ (iii)**, L105 (vi), L122 (v).

---

## 6 · CONTRACT DEFECTS FOUND

Ordered by consequence. Each is a claim the contract makes that the estate does not support.

1. **I4 is wrong as written.** `warmup_bars(500) = 1727`. Evidence-side on 1d: **BTC 31 bars; ETH, SOL, NEAR, ZEC — NEVER.** The `450_500` ribbon and cross class (L88, L94) are dead on 1d for four of five panel assets, not "marginal". 12h and 4h are fine (panel 983–8,817 warm bars). The cited warrant, `MC1_tables.md:5`, is a **7-EMA matrix with no EMA500 column** — the feasibility matrix was a thing to be built, not a citation. It now exists: `feasibility_matrix.parquet`, 392 cells.
2. **The AUTHORITY block overstates its basis.** It cites CD-1(d), CD-2(a), CD-3(a), CD-4(a), CD-5(a) as "operator ratifications"; the estate records all five as `[lean]` at `APOLLO…:65-70`, with `:74` listing CD-1..CD-6 as an **open** operator action. Confirmed as ratified by the operator on 2026-08-12 — **the block should cite that stamp, not the lean.**
3. **MC-2's own citation was dangling** — see §0.
4. **"Full 709 campaigns" (L131) misnames a decile.** 709 = `floor(0.1 × 7094)` (`BUILDERS_REPORT_APOLLO_2026-08-03_WF1.md:110-111`). The population is 7,117 fills / 7,094 resolved tranches. Should read "all 7,094 resolved campaigns".
5. **"Toll reference per mandate" (L35-36) has no backing.** No per-mandate fee object exists; there is one global `fee_bps_side: 5.0` (`configs/naiad_v0.yaml:58`), i.e. **10 bps round trip, invariant across mandates**. Either print the global line and say so, or supply per-mandate values.
6. **F-7's "286" is lens-ambiguous.** 286 is a union-over-8-views figure; under the contract's own entry lens (`24h|window_chained`, I6) the no-cascade cohort is **3,363**. The 286 key list is persisted nowhere, so D-CEN2d must recompute the cohort.
7. **D-C lens-concordance (L122-124) has no metric, window, or threshold** — and carries no ⟨MC2⟩ token, so nothing in the gating path will ever pin it, yet it is component five of the composite behind P-CHOP-1 [65%]. A measurable baseline exists: cross-view agreement `same_depth 40.04%` / `same_rung_string 38.46%`.
8. **Memory citations #13/#14/#16 (L21) do not resolve by number** — no snapshot on disk holds them, and `CONVENTIONS.md:317` uses #14/#16 for different content. Cite the bus notes by path instead.
9. **"Supersedes v0.1" (L2) is unverifiable** — no v0.1 is on disk.

**Also fixed this session (repo hazard, not a contract defect):** `research_outputs/census2a/**` and `research_outputs/mc2/**` were **not** gitignored. That is the exact shape of the 2026-08-05 incident in which a wildcard `git add -A` swept 3,567 MB of untracked-but-unignored bulk into a commit and GitHub rejected the branch push. Both rules were added to `.gitignore` **before** any directory of that name could exist. All MC-2 and CEN-0 bulk is born on `D:` per I2 regardless.

---

## 7 · WHAT REMAINS BEFORE THE CENSUS CAN BE RATIFIED

**Blocking:**
1. **(ii) TRAP has no established value.** The fallback ≥2 is unusable (fires on 91.5%) and the ≥5 replacement was withdrawn as a selection artifact (42.0% permutation-null rate). Decide: drop the TRAP stamp from D-CEN2a's discriminant set, or re-scope it as a pre-registered single hypothesis with one threshold named in advance — which is the only way a sweep of this shape can yield an admissible constant.
2. **(iv) nested pair set is unresolved.** No candidate's separation CI excludes zero in either era. Operator pins by name [VETO], or the question defers into the census population.
3. **Amend I4** for EMA500 (evidence-side {15m,30m,1h,4h,12h} only; 1d/500 and `450_500`-on-1d ops-only) rather than emitting NEVER cells into a scored table.
4. **Amend the AUTHORITY block** to cite the 2026-08-12 stamp.
5. **Operator review of the live-era pinning decision** (§1).

**Two of six placeholders therefore remain unresolved after paste #1** — (ii) and (iv). The contract's condition (1) requires that paste #1's outputs "replace every ⟨MC2⟩ placeholder". **It does not, and cannot be represented as doing so.** Four are resolved: (i) and (v) confirmed, (iii) pinned at 108, (vi) refined to `25_89` only.

**Non-blocking, filed:** PAXG fetch + classification (CEN-0(b)); the price↔level refusal detector (i-b); CD-6 TradFi provider; defects 4–9 above as editorial amendments.

---

## 7A · ADVERSARIAL REVIEW OF THIS BUILD — what it found and what changed

Paste #1 was reviewed against four independent lenses (causality, statistical validity, reuse fidelity, claim audit) before being handed over. It found **six defects in the build itself**, all now fixed in code rather than annotated in prose. They are listed because a paste that reports only its findings and not its own errors is not a record.

| # | Defect | Why it mattered | Fix |
|---|---|---|---|
| 1 | **F-PARITY concealed a bug.** It re-applied the `ASSET_STARTS` floor *inside the fixture only*, proving equality under a filter no production path used. Evidence-era EMAs were computed from the series' first byte — 50 of 1,573 armings were cold-seed artifacts | The contract's I4 requires "NaN before warm" and the program did not implement it; every downstream count inherited the artifacts | `frame()` now NaNs the cold head per the SEQ8 warm-up rule; new **F-PARITY-2** asserts zero crosses inside the warm-up region; parity now compares the warm overlap and prints the excluded count |
| 2 | **Lookahead in the query cards.** `stage_cards` reported the close/ATR/EMAs of the bar *containing* the timestamp — a bar still open | I7 mandates as-of slicing *everywhere*; up to +1.45% price error and 55% relative error on the ribbon. DISPLAY-ONLY does not exempt a leak — a query card exists so an operator can trust the photograph | Repointed to `census_build.asof_idx` (last **closed** bar), the primitive the docstring already claimed to reuse but never called |
| 3 | **`aborted` was not disjoint** — true of 431/436 windows including all 64 completed ones | The contract's arming-fate taxonomy (D-CEN2a) cannot be derived from a non-partitioning class | Replaced by a disjoint `fate` ∈ {COMPLETED, ABORTED, ROTTED} |
| 4 | **`W_max` reported a quantile that does not exist**, and the docstring claimed the distribution was untruncated when 99% of windows close early | The pin fed the contract's headline module | Kaplan-Meier; `S∞` and the conditional quantile reported separately; stability across observation caps verified |
| 5 | **Kiss detector reimplemented, not imported** — a subtly different detector losing 2.5% of events one-directionally | The stage claims to *confirm a ratified constant*; it was demonstrating a different detector's stability | Parameterised detector now **asserted identical** to `mc1_program.kiss_v0` at the ratified point (**F-KISS-PARITY**), halting if it ever diverges |
| 6 | **Horizon units silently redefined.** `CB.HORIZONS` are 5m exec bars; applied to HTF frames the same integer meant 16.7 days, and `stage_nesting` mixed two durations in one table | Rows of one table were not comparable | Horizon fixed as a **duration** (`HORIZON_MS`), converted per timeframe |

Two further process defects: a `--stage` re-run **rebuilt the manifest from scratch**, destroying five of six pins (now merges); and the `≥3 of 5` sign gate was a **no-op** — P = 0.50 under a fair coin, computed from the same observations as the CI, and it never once changed a decision across three stages and two eras. It is now reported but is not a criterion; the **asset-cluster bootstrap** replaced it.

**Known limitations not fixed, stated rather than buried:**
- **The discriminant is a position-in-range statistic.** `net = MFE − MAE` is algebraically `2·(midpoint of the forward range − anchor close)/ATR` — invariant to the terminal price, and its sign disagrees with the sign of the terminal 100-bar return on ~40% of anchors. Its magnitude correlates 0.909 with forward range/ATR, so it partly measures volatility. Under a scale-free version, the (already withdrawn) TRAP effect vanishes. **This should be re-specified before the census scores anything on it.**
- **The guard now covers (ii) and (iv); `stage_obs25` and `stage_ribbon` remain unguarded in code.** obs25's two classes were **pre-named by the contract** (not selected from a sweep) and its promotion additionally survives an asset-cluster bootstrap in both eras, so the exposure there is ordinary 2-test multiplicity rather than selection — quantified at ~15% by an uncommitted scratch check that should be moved into the program. `stage_ribbon` confirms a pre-ratified constant and promotes nothing new. *The review flagged this class of risk as "one lucky candidate away from an unguarded pin"; the very next run produced exactly that in `stage_nesting` (see (iv)), which is why the guard was extended there.*
- **The ribbon "confirmation" cannot meaningfully fail:** 4 of 9 swept `c` values land in the admissible band, and the band itself is a free parameter of the same type as the constant it certifies. The stage's own admission — selectivity cannot order two admissible `c`s — is the actual result; the pin adds nothing to it.
- **The kiss pin is a pass-through by construction** (the 75-row sweep cannot change it), and its own stability diagnostic reads 69.1% span against the program's stated "a constant on a cliff is a fitted constant" criterion. It is retained because it is *ratified*, not because this sandbox validated it.

---

## 8 · ARTIFACTS

All bulk on `D:` per I2 — 21 files, 5.3 MB, and **nothing named `census2a` or `mc2` exists on `C:`**. Bus carries pointers only; no results JSON enters `exchange/`. Box was at 28.51% of the 6,390,000 B budget before this paste and is **29.21%** after it (this document is 39,571 B), leaving 689,417 B below the refuse line — still past the 25% warn line, and rotation (queue 003) remains ratified-but-unbuilt with no candidates until ~2026-08-28.

`D:/Naiad/research_outputs/census2a/`
- `cen0_panel_inventory.parquet` (48 rows; 42 present + 6 absent PAXG) · `cen0_readiness.parquet` (8) · `cen0_manifest.json`
- `mc2/mc2_manifest_live.json` · `mc2/mc2_manifest_evidence.json` · run logs per era
- `mc2/live/` — `relay_chains` (436) · `nesting_table` (6) · `obs25_table` (4) · `trap_sweep` (20) · `ribbon_sweep` (18) · `kiss_sweep` (75)
- `mc2/evidence/` — same set, plus `feasibility_matrix` (392)

sha256 — see `mc2_manifest_{live,evidence}.json` for the authoritative per-artifact hashes. The feasibility matrix is emitted **evidence-side only** (warmth is a data fact, not an era choice), so it appears under `mc2/evidence/`, not `mc2/live/`.

Programs (uncommitted; `publish_exchange.py` stages only `exchange/**`): `scripts/mc2_program.py`, `scripts/cen0_inventory.py`.

**Query cards** (display-only, never priors — D-H): QC-1 2026-06-17 14:30Z **IN RANGE**; QC-2 2026-08-11 10:00Z **IN RANGE**. Both served offline from the live cache, which runs to 2026-08-12 — an earlier assessment that QC-2 needed a re-fetch was reading MC-1's frozen `ops_klines` snapshot (ends 2026-08-01), not the live cache. **No network call was made in this paste.**

---

## 9 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12 ===
NOW: CENSUS-2A paste #1 built and run. MC-2 did not exist in any form and has been written
(scripts/mc2_program.py), extended per operator word to pin all six placeholders rather than the
three its commission covered. Constants pinned OUT-OF-SAMPLE on the live era, evidence era printed
beside. The census remains NOT EXECUTABLE: conditions (2) and (3) are open, and placeholder (iv) is
unresolved.
LAST EVENT: 2026-08-12 — MC-2 (extended) + CEN-0(a) executed; F-1/F-PARITY/F-3/F-DET all pass
FACTS:
- MC-2 had no artifact on C: or D:; "drafted, D:-resident" was uncorroborated [verified]
- TRAP fallback >=2 fires on 91.5% live / 92.2% evidence of 4h lattice-A armings — a null gate;
  rejection replicates, the >=5 replacement does not [verified]
- W_max fallback 90 rejected: terminal-leg lag p90 = 108 live / 132 evidence; full relay completes
  on only 14.7% of armings [verified]
- 25_89 earns trigger inclusion, 9_25 does not (2.19x the reference count, net CI straddles 0);
  the incumbent 12_25 also fails the same bar [verified]
- I4 wrong as written: EMA500 evidence-side on 1d is NEVER for ETH/SOL/NEAR/ZEC, 30 bars for BTC;
  the cited MC1_tables.md feasibility matrix has no EMA500 column [verified]
- AUTHORITY block cited CD-1(d)..CD-5(a) as ratifications; estate recorded them as [lean] until the
  operator stamped them 2026-08-12 [ratified]
PENDING:
1. Placeholder (iv) nested pair set UNRESOLVED — no candidate's separation CI excludes 0 in either
   era; operator pins by name [VETO] or it defers into the census population
2. TRAP: adopt >=5 provisionally, drop the stamp from D-CEN2a's discriminants, or re-scope —
   its discriminative power is not established on the era the census scores
3. Amend I4 (EMA500 evidence-side <=12h only) and the AUTHORITY block (cite the stamp, not the lean)
4. Operator review of the live-era pinning decision — the largest judgement call in this paste
5. CEN-0(b) PAXG unfetched by scope decision; price<->level refusal detector (i-b) has no
   implementation anywhere and remains open work
NEXT: Operator performs condition (2) review of this document, then stamps or withholds (3).
Owner: operator.
METRICS: operator actions this session = 3 (scope, network, authority) — files re-ingested = 0
=== END STATUS ===
```

---

## 10 · SUPERSEDING LEDGER APPEND (F-17, second entry — same session)

The §9 entry above is reproduced **verbatim as landed**. `LEDGER_APOLLO.md` is append-only — "never edit a past entry; a correction is a NEW entry that names what it supersedes" — so the adversarial-review corrections land as a second entry rather than as an edit to the first. Both are in the ledger.

```
=== STATUS_APOLLO — 2026-08-12b ===
NOW: SUPERSEDES the 2026-08-12 entry above on three points, following adversarial review of the
paste-#1 build. The review found six defects in the build itself; all are fixed in code and the
affected numbers are restated here. The census remains NOT EXECUTABLE and two of six placeholders
remain unresolved.
LAST EVENT: 2026-08-12 — four-lens adversarial review of MC-2; six build defects fixed; both eras re-run
FACTS:
- SUPERSEDES "adopt >=5 provisionally": TRAP >=5 is WITHDRAWN as a selection artifact. Selection-
  corrected permutation p = 0.287 live / 0.528 evidence against an I8 bar (BH, q=0.10, m=11) of
  0.0091 — inadmissible by 32x. It also fails an asset-cluster bootstrap, CI [-2.333, +0.059].
  The rejection of the >=2 fallback stands: it fires on 91.5% of armings, a descriptive fact [verified]
- SUPERSEDES "W_max = 108": the naive completed-only p90 conditions on survival. Kaplan-Meier gives
  45.1% of armings NEVER completing, so the p90 over armings does not exist; conditional on eventual
  completion W_max = 151 live / 160 evidence, CI [112.8, 186.0], stable across observation caps
  >= 200. W_max is near-non-binding: the counter-arming closes 98.9% of windows first [verified]
- SUPERSEDES "92.2% evidence": that was MC-1's figure, not MC-2's. MC-2 evidence = 92.1%. The two
  populations are NOT the same (MC-1 7 assets floored at ASSET_STARTS; MC-2 5 assets) and the earlier
  claim that they agreed to 4 events was a coincidental cancellation of two differences [verified]
- Build defects fixed: cold-EMA armings (I4 "NaN before warm" was never implemented, and F-PARITY
  concealed it); a lookahead in the query cards (bar containing ts, not last closed bar); a
  non-disjoint arming fate; a reimplemented kiss detector now asserted == mc1_program.kiss_v0; a
  silently redefined outcome-horizon unit; and a manifest rebuild that destroyed 5 of 6 pins [verified]
- 25_89 inclusion SURVIVES the stronger test: asset-cluster CI [0.352,1.527] live / [0.493,1.287]
  evidence. 9_25 excluded in both eras [verified]
PENDING:
1. (ii) TRAP and (iv) nested pair set remain UNRESOLVED — condition (1) of the contract is NOT met
2. The discriminant (net = MFE - MAE) is a position-in-range statistic, invariant to the terminal
   price and ~0.91 correlated with forward range; it should be re-specified before the census scores
   on it. This is the largest open methodological item
3. The selection guard is implemented for (ii) only; three other sweep-and-select stages are unguarded
4. Amend I4 (EMA500 evidence-side <=12h only) and the AUTHORITY block (cite the stamp, not the lean)
5. Operator review of the live-era pinning decision
NEXT: Operator performs condition (2) review, then stamps or withholds (3). Owner: operator.
METRICS: operator actions this session = 3 (scope, network, authority) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · paste #1 of CENSUS-2A · the census is not ratified and did not run
