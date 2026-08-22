# CENSUS-1b — Re-score, Tradeability, and Move-Anatomy Census — Builder Contract

**Phase:** v12 Study · **Tier A** for the re-scores (arithmetic on the pinned CENSUS-1 substrate; no re-run, no new trades, no rule change) · **Tier A / bounded-Tier-B for the anatomy captures** (a join of pinned files, plus one contingent in-window re-walk — see §3.5). **Engine: 1.0.11, byte-untouched.** No trading occurs. The integrity spine is byte-identity to the CENSUS-1 substrate, derivation-fidelity, determinism, and the anti-fishing protocol (§7).
**Basis:** CENSUS-1 verified (`eb671df` build; reviewer verification and D8 correction on record, `770860b` + the correction entry committed with this phase's pre-registration). Same substrate, same exploration-classic window, same four candidate governor lenses {1H, 4H, 12H, 1D}. This phase reads the four CENSUS-1 substrate files; it does not re-walk price except where §3.5 explicitly scopes it, and it never touches the lockbox.
**Why this phase exists:** CENSUS-1's ATR-denominated ranking is a units artifact (report §3.2); its confluence-combination result has no downside partner; its pullback-outcome edge is underpowered per-lens; its dose-response is shallow under a collinear factor list; and its cascade rungs are **not** the "symmetric noise" the run summary claimed — the 1H and 4H rungs are favorable-skewed (MFE/|MAE| 1.19 and 1.33 in ATR terms; corrected on the ledger this phase). CENSUS-1b turns the census from *observed* into a **decision-grade specification**, in the units that decide whether a trade pays (basis points net of toll), and captures the **move-anatomy substrate** the operator asked for so later phases can mine cross/pullback relationships that this project has not yet looked at.

---

## 0. Operator instructions

Save this contract into the repo → `claude` → `git status` clean → paste §12. *What you should see, in order:* (a) the **schema-pin** — the builder pastes one record from each of the four substrate files, pins exact field names, and resolves the one contingency in §3.5; (b) the **G-7 pre-registration commit** — the four prediction rows with priors, the toll mapping, the bps-MAE derivation rule, the pooling method, the decorrelation threshold, **and** the two carried ledger-housekeeping entries (the D8 correction and your ratification), **before any analysis**; (c) the **byte-identity gate** — the four files re-hashed to the pinned sha256; (d) the re-scores and the anatomy captures; (e) the pre-registered scorecard (falsifications first) and — kept strictly separate — the exploratory annex. Any byte-identity MISMATCH or derivation fault → halt, report. Send back `census1b_results.json`, `census1b_termini_enriched.jsonl`, `CENSUS_1b.md`, the fixture table, the scorecard, the annex.

## 1. What this phase is

A re-expression and enrichment of the CENSUS-1 substrate, in five jobs:
1. **The units fix (D4/D8 re-rank).** Re-rank the decoupled-add candidates (D4) and the cascade rungs (D8) in **basis points net of toll**, on a **quality measure** (favorable vs adverse), with the **up-move-net-of-cost reported alongside**. This replaces the ATR ranking that was an accident of units, and it re-tests the corrected 1H/4H favorable asymmetry in the units that matter.
2. **The tradeability pairing (D5 + MAE).** Pair the pre-registered slow-stack combination (CENSUS-1 P-C5, +596.75 bps net-of-toll favorable) with its **downside** so we learn whether it is actually tradeable, not merely favorable on the peak.
3. **The powered pullback test (P-C7b, pooled).** Give the underpowered EMA-terminating-pullback edge a high-powered test by **pooling all four lenses**, scale-normalized, with a ≥2-lens sign-agreement gate.
4. **The framework's fair trial (D9 decorrelation).** Decorrelate the nine collinear confluence factors to a low-mutual-information core and re-run the dose-response, so the operator's flexible-entry framework is tested on independent signal rather than nine near-copies of "the trend is on."
5. **The move-anatomy capture (enriched substrate + adverse-zone).** Emit, per pullback terminus, the **full cross cascade bracketing it** — every EMA cross that fired before it and after it, on which timeframe, in which direction, at what lag — so later phases can mine the cross/pullback relationships this project has not examined; and test whether the **adverse** leg of a move also terminates on an EMA zone (the pocket's mechanism, applied to the drawdown). Jobs 1–4 join back to the S-3/CENSUS-1 comparison fabric; job 5 produces new exploratory substrate under strict anti-fishing quarantine.

## 2. What this phase is NOT

Not a re-run of the census (the four substrate files are read as-is and byte-verified; nothing is re-simulated except the one contingent re-walk in §3.5) · not a redesign (this phase *scores and describes*; a new arming/add/governor rule is a later Tier-C, pre-registered against what this phase and the census find) · not new evidence spend (exploration-classic window only; the lockbox is untouched; a re-walk in §3.5, if triggered, re-measures the same in-window price and consumes no lockbox) · **not a confirmation study for job 5** (the anatomy captures are exploratory data-generation — nothing in them counts as a validated finding; every pattern is a hypothesis for a following, separately pre-registered test) · not free of the multiple-comparison hazard (job 5 opens a wide search; the anti-fishing protocol §7 is the phase's spine and is non-negotiable) · not out-of-sample (anything found is a hypothesis for the lockbox, never a validated edge).

## 3. Construction

### 3.0 The pinned substrate (byte-identity gate)
The four CENSUS-1 files, re-hashed to `build_manifest.json` before any analysis; **any mismatch HALTS the phase** (a changed substrate invalidates every downstream number):

| file | rows | sha256 |
|---|---|---|
| `continuation.jsonl` | 38,552 | `9a7d186620ce7e92722c50a4268e13200756e8da53fabee826194473583b1594` |
| `census_ladder.jsonl` | 81,674 | `cc81b8978f81aa277ae38566f5b0fb89e76632b9ff97403f3767f6f3a611bf74` |
| `census_outcomes.jsonl` | 149,802 | `daf488acef40a2ab8f23a06d43a77ce2a8256856d635eb2f62bd985bff59385c` |
| `census_termini.jsonl` | 160,160 | `61a9b7a30cc2bb4b20e37def02e59ee74eef345292dd0e822aada83e16c06e4e` |

(`census_termini` = 14,560 real termini + 145,600 matched nulls at `null_mult=10`.)

### 3.1 The toll and the net-of-cost basis (pinned at step 0)
The per-asset round-trip toll is {14, 20, 30} bps by asset. **The exact asset→toll mapping is pinned at step 0 by reading it from `census_analyze` — CENSUS-1b must use the identical mapping CENSUS-1's D5 used** (D5 gross 614.16 → net 596.75 bps implies the same toll model; consistency is mandatory). Net-of-cost convention, applied uniformly and pinned before analysis:
- **net favorable** = `MFE_bps − T`
- **net adverse (magnitude)** = `|MAE_bps| + T`
- **quality ratio** = `(MFE_bps − T) / (|MAE_bps| + T)` — the discriminating statistic for jobs 1 and 2.

The toll is subtracted from the favorable leg and added to the adverse leg because a round-trip cost hurts you in both directions; a candidate that runs far but also bleeds far is a bad place to add, and this ratio is the number that says so.

### 3.2 The bps-MAE derivation (Fork 2 — the recoverable gap)
`census_ladder`, `continuation`, and `census_termini` store the **favorable** excursion in both bps and ATR but the **adverse** excursion in ATR only (termini carries no MAE at all — see §3.5). Within one record, bps and ATR are a fixed linear rescale (the shared per-record factor `ATR_anchor / price_anchor`), so:

> `rem_mae_bps = rem_mae_atr × (rem_mfe_bps / rem_mfe_atr)`

exact up to 6-decimal storage rounding. **Fixture F1b-DERIV** validates this against `census_outcomes` (where both bps and ATR MAE are stored) before it is trusted downstream. **Zero-carrier handling (Fork 2, Option A ratified):** where `rem_mfe = 0` the carrier vanishes and the record is **dropped and counted** — the excluded n is printed in the fixture (expected ≈0.367% of ladder rungs, 0.12–0.59% of continuation records). No estimate is substituted for a dropped record.

### 3.3 The four re-scores (jobs 1–4)
- **D4/D8 bps quality re-rank.** For each decoupled-add candidate (D4, at continuation moments) and each cascade rung (D8), report the **quality ratio** (§3.1) and, **alongside, the up-move net of cost** (`MFE_bps − T`), per lens, with bootstrap CIs (10,000 resamples, seed 20260721 — the pinned census seed). The D8 rungs re-test the corrected 1H/4H asymmetry (§1) in net-of-toll bps.
- **D5 + MAE tradeability.** The P-C5 slow-stack combination's forward outcome, now paired: the quality ratio (§3.1) at regime-scale, with CI. Reports whether the +596.75 bps favorable survives as a *tradeable* ratio once the drawdown is priced.
- **P-C7b pooled (Fork 1, Option A ratified).** Pool the four lenses' EMA-terminating-minus-non 100-bar forward MFE difference, **each lens normalized to its own ATR** (justified: P-C7a's landing held identically across all four lenses — the fractal signature — so the normalized effects are commensurable). Retain the **≥2-lens sign-agreement gate** as the pass condition so pooling cannot manufacture a false positive. Pool **within the 14,560 real termini** (the nulls carry no forward outcome). Report the pooled estimate with CI **and** the per-lens breakdown.
- **D9 decorrelation.** Build the factor-factor association matrix over the arming-moment factor vectors (F1–F9). Greedily prune to a **decorrelated core** with all pairwise association below a threshold **pinned at step 0 (default |φ / Cramér's V| < 0.30)**; re-run the dose-response ρ(k, MFE) on the core, per lens, against the collinear full-list baseline (ρ 0.012–0.038). Reports whether the flat dose-response was a collinearity artifact or a structural weakness of the framework.

### 3.4 The move-anatomy enriched dataset (job 5a — the pullback cross-cascade)
A **join** of `census_termini` (real termini only) × `census_outcomes` (the full 149,802-event cross catalogue). For each of the 14,560 real termini, emit one record to `census1b_termini_enriched.jsonl` carrying:
- terminus identity: asset, lens, regime, direction, timestamp, anchor price, anchor ATR; and its carried distances to the lens e89, lens e200, lens+1 e200 (from `census_termini`);
- forward outcome: 100-bar MFE (ATR and bps), and the derived bps-MAE where recoverable (§3.2);
- **prior cross context** — for **each of the seven timeframes × three cross types (9/89, 89/200, 9/200)**, the most recent same-asset cross *before* the terminus: its direction and its lag in exec (5m) bars;
- **forward cross context** — for the same 7×3 grid, the first same-asset cross *after* the terminus: its direction and its lag in exec bars.

This is a wide, purely descriptive table (14,560 rows). It is emitted so that later phases can cross-reference exhaustively — for example the operator's motivating pattern: *lower-timeframes fire a bull 9/89 → the 4H 9/89 fires → price pulls back to the 89/200 ribbon or the pocket → on the bounce, which LTF cross (5m / 15m / 30m) gives the best forward outcome?* **Nothing computed from this table in this phase is a finding** (§7); a small pre-declared set of demonstration cuts is run in the annex (§10), replication-gated and CI'd, purely to prove the substrate answers such questions.

### 3.5 The adverse-excursion zone-landing (job 5b — Q3a extension, CONTINGENT)
The question: does the **adverse** leg of a move (the drawdown before price resumes) also **terminate on an EMA zone / the pocket band**, as pullback lows do (D10)? If it does, the drawdown is not random noise — it is a pullback landing on structure, i.e., a natural add/re-entry location.

**Resolved at step 0 by the schema-pin:**
- **If `census_outcomes` stores the MAE bar-offset (or the MAE timestamp/price)** → this is a **join** (locate the adverse-leg low, compute its distance to the lens EMAs, test excess clustering against the same matched-null construction as D10). Tier A, zero re-walk.
- **If only the MAE *magnitude* is stored** → locating the adverse low requires a **scoped in-window re-walk** of exec price from each anchor to its MAE bar. This is new measurement (trade-independent, in-window, **no lockbox spend**), and to keep it bounded it is scoped to the **continuation and cascade-rung anchors only** (the anchors where an adverse-then-resume is an add decision), **not** all 149,802 events. If this branch triggers, job 5b is delivered as **PARTIAL-eligible** — if the re-walk is heavier than budget, deliver jobs 1–5a and name 5b as the deferred piece.

Either way, job 5b is **exploratory** (§7): its clustering claim is reported with a matched-null row beside it (D10 discipline), and nothing in it is a validated finding.

## 4. Candidate governors

Carried verbatim from CENSUS-1: four lenses {1H, 4H, 12H, 1D} as analysis filters over the single substrate; "long regime" = the lens's e9 > e89; outcomes conditioned within the lens's regime. The product is the **governor-per-mandate map**, not a single winner.

## 5. Definitions — pin before coding (schema-pin, step 0)

Carried: bps, ATR, MFE/MAE, dual coordinates, as-of mapping, toll (14/20/30 by asset, reference line only — no trades), cross-TF replication.
**Pinned this phase against the four `head -1` records:** the exact field names for favorable/adverse in bps and ATR per file (`rem_mfe_bps`, `rem_mae_atr`, etc. — confirm verbatim); whether `census_outcomes` stores the MAE bar-offset/timestamp/price (§3.5 branch); the asset→toll mapping read from `census_analyze`.
**New this phase:** the **net-of-cost quality ratio** (§3.1) · the **bps-MAE derivation** and drop-and-count rule (§3.2) · the **scale-normalized cross-lens pool** and its ≥2-lens gate (§3.3) · the **decorrelated factor core** and its association threshold (§3.3) · the **terminus cross-cascade join** (prior + forward 7×3 grid, exec-bar lags — §3.4) · the **adverse-excursion low** and its zone test (§3.5).

## 6. Fixtures — any MISMATCH halts

| # | Fixture | Expected |
|---|---|---|
| F1b-BYTE | The four substrate files re-hash to the `build_manifest.json` sha256 (§3.0) | 4/4 identical |
| F1b-DERIV | bps-MAE derivation (§3.2) validated on `census_outcomes` where both units exist: MFE-derived vs stored-MAE rescale agree | median \|Δ\| ≤ 1e-6; zero-carrier drop count printed |
| F1b-DET | Full analysis run twice → `census1b_results.json` + enriched jsonl byte-identical | identical |
| F1b-CFG | Toll mapping, decorrelation threshold, pooling method, drop-and-count rule, seed = the G-7 pre-registration | exact |
| F1b-JOIN | Terminus×cross join (§3.4): every real terminus resolves; row count = 14,560; no cross assigned across an asset boundary (spot-check pinned sample) | exact |

**F1b-BYTE and F1b-DERIV are the ones that poison everything** — a changed substrate or a wrong rescale invalidates every net-of-cost number. Any mismatch → HALT, report, produce nothing downstream.

## 7. Anti-fishing protocol — the phase's spine (non-negotiable, and load-bearing for job 5)

Jobs 1–4 re-score pre-specified quantities; job 5 opens a wide descriptive search, and most "edges" in such a space are chance. The discipline:
1. **Only the four §8 predictions are confirmatory.** Registered before any analysis; scored verbatim; nothing else may be reported as validated.
2. **Everything in job 5 is exploratory annex** (§10) — hypothesis-generation for a *following, separately pre-registered* test, labeled "not validated, generated in-sample, exploration-classic."
3. **The demonstration cuts on the enriched dataset are pre-declared** in the G-7 commit (their exact conditioning stated before they are run); no cut is added after seeing results, and no cut is reported as a finding. Cross-TF replication (sign holds across ≥2 timeframe pairs) is required for any cut to be flagged worth-pursuing; a single-pair pattern is recorded "single-instance, likely noise."
4. **No parameter is tuned to outcome.** The toll mapping, the decorrelation threshold, the pooling normalization, the drop-and-count rule, the continuation/cascade anchor set for §3.5 — all fixed at pre-registration; the phase does not search over them.
5. **Bootstrap CIs (10,000 resamples, seed 20260721) on every reported number.** An effect whose CI spans zero (or, for a ratio, spans 1.0) is reported as such, never as an edge.

## 8. Pre-registered predictions (the only confirmatory claims) — falsifications first

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-1b-D9 | A decorrelated factor core (pairwise assoc < 0.30) yields dose-response ρ(k, MFE) ≥ 0.10 on ≥2 lenses — materially steeper than the collinear full list (0.012–0.038) | 40% | core ρ < 0.10 on all but ≤1 lens (the flat dose-response is structural, not a collinearity artifact) |
| P-1b-C7b | Pooled across four lenses (own-ATR-normalized, ≥2-lens sign gate), EMA-terminating pullbacks show higher 100-bar forward MFE than non-EMA, pooled 95% CI excluding zero | 45% | pooled CI includes zero, or sign agreement holds on <2 lenses |
| P-1b-D5 | The P-C5 slow-stack combination's net-of-toll quality ratio (regime-scale) has 95% CI lower bound > 1.0 (genuinely tradeable, not just favorable-on-peak) | 55% | ratio CI includes or is below 1.0 |
| P-1b-D8 | **Primary:** the 4H cascade rung's net-of-toll quality ratio has 95% CI lower bound ≥ 1.05 (a real favorable add-edge at the slow confirmation rung). **Secondary:** the 1H rung's ratio CI includes 1.0 (marginal) | 55% | 4H CI lower bound < 1.05 (primary); recorded separately if the 1H secondary misses |

Priors are the reviewer's, set at pre-registration; scoring is falsifications-first. P-1b-D8's directional shape follows from the corrected ATR asymmetry (1H 1.19, 4H 1.33) surviving into toll-space at the 4H rung — where a fixed bps toll is a small slice of a large slow move — while being eaten at the faster 1H rung where the same toll is a larger share.

## 9. Deliverables

- **D1b — the net-of-cost re-rank.** D4 add-candidates and D8 rungs by quality ratio, with up-move-net-of-cost alongside, per lens, dual-coordinate, CIs; the P-1b-D8 verdict.
- **D2b — the tradeability pairing.** The P-C5 combination's quality ratio at regime-scale, per lens, CI; the P-1b-D5 verdict.
- **D3b — the powered pullback test.** The pooled EMA-terminating edge (scale-normalized, ≥2-lens gate) with per-lens breakdown, CI; the P-1b-C7b verdict.
- **D4b — the decorrelation table.** The factor association matrix, the decorrelated core, the core dose-response ρ per lens vs the full-list baseline; the P-1b-D9 verdict.
- **D5b — the enriched terminus dataset.** `census1b_termini_enriched.jsonl` (§3.4), with a schema note; **exploratory substrate, not a finding.**
- **D6b — the adverse-excursion zone test** (§3.5, contingent), with its matched-null row; **exploratory.**

## 10. Exploratory annex (kept strictly separate from §8/§9)

Everything from job 5 beyond the four predictions: the **pre-declared demonstration cuts** on the enriched dataset (including the operator's motivating pattern — termini preceded by a 4H 9/89 within a stated window AND landing within 0.35 lens-ATR of the 89/200, then forward outcome by the next 5m/15m/30m cross), each with CI and cross-TF replication status and the explicit label **"exploratory, in-sample, exploration-classic, not validated — candidate for a following pre-registered test."** Nothing here counts as a finding until a separate contract tests it.

## 11. Verdict, artifacts, ledger

**PASS** — 5/5 fixtures, 4/4 predictions scored falsifications-first, D1b–D6b delivered (D6b per its §3.5 branch), the enriched dataset emitted, the annex delivered and correctly separated, determinism proven. **HALT** — any byte-identity MISMATCH (F1b-BYTE) or derivation fault (F1b-DERIV); these poison everything downstream. **PARTIAL** — D6b's re-walk branch (§3.5) genuinely over budget: deliver D1b–D5b, name D6b as deferred. Artifacts: `scripts/census1b_analyze.py` · `census1b_results.json` · `census1b_termini_enriched.jsonl` · `CENSUS_1b.md` · **ledger entries: (a) the carried D8 correction, (b) the operator's ratification of the CENSUS-1 reconciliation, (c) this phase's G-7 pre-registration** (the four rows with priors, the toll mapping, the derivation and drop rule, the pooling method, the decorrelation threshold, the pre-declared annex cuts), and (d) completion (fixtures, scorecard, annex summary). Commit; **do not push, do not merge.**

## 12. The go-paste

```
CONTRACT: CENSUS-1b — Re-score, Tradeability, and Move-Anatomy Census (Tier A; engine 1.0.11 byte-untouched; measure-only, no trading; reads the pinned CENSUS-1 substrate)

Read CENSUS_1b_Rescore_and_Anatomy_Builder_Contract.md in the repo in full first. The
contract is the authority; this paste is the trigger.

Scope in one line: re-score CENSUS-1's add-trigger candidates (D4) and cascade rungs (D8)
in basis points net of toll on a favorable-vs-adverse quality measure (up-move-net-of-cost
reported alongside); pair the slow-stack combination (P-C5) with its downside; give the
underpowered pullback-outcome edge (P-C7b) a powered pooled test; decorrelate the nine
confluence factors and re-run the dose-response; and emit the move-anatomy substrate — the
full cross cascade bracketing each pullback, plus whether the adverse leg lands on a zone.
No trading, no rule change, no re-run of the census (the four substrate files are read and
byte-verified), no lockbox.

Order of work — mandatory:

0. SCHEMA-PIN. Paste one record (head -1) from each of continuation.jsonl,
   census_ladder.jsonl, census_outcomes.jsonl, census_termini.jsonl. Pin exact field names
   for favorable/adverse in bps and ATR per file. Resolve the §3.5 contingency: does
   census_outcomes store the MAE bar-offset/timestamp/price (join) or magnitude only
   (scoped re-walk)? Read the asset->toll mapping from census_analyze and pin it (must match
   CENSUS-1 D5). Restate the §5 definitions.

1. G-7 PRE-REGISTRATION. Commit the four §8 prediction rows with priors, the toll mapping,
   the bps-MAE derivation and drop-and-count rule, the cross-lens pooling method and >=2-lens
   gate, the decorrelation threshold (default assoc < 0.30), and the pre-declared annex cuts
   — BEFORE any analysis. Include in the SAME commit the two carried ledger entries: the D8
   correction and the operator's ratification of the CENSUS-1 reconciliation.

2. BYTE-IDENTITY GATE (F1b-BYTE). Re-hash the four files to build_manifest.json.
   *** ANY MISMATCH: HALT, report, produce nothing downstream. ***

3. DERIVE bps-MAE (§3.2). Validate against census_outcomes (F1b-DERIV, median |delta| <= 1e-6).
   Drop-and-count zero-carrier records; print the excluded n.

4. RE-SCORES (jobs 1-4): D4/D8 net-of-cost quality re-rank (up-move-net-of-cost alongside);
   D5+MAE tradeability; P-C7b pooled (scale-normalized, >=2-lens gate, within the 14,560 real
   termini); D9 decorrelation. Every number carries a CI; the four §8 predictions are the ONLY
   confirmatory claims.

5. ENRICHED DATASET (job 5a, §3.4): join census_termini x census_outcomes; emit
   census1b_termini_enriched.jsonl (prior + forward 7x3 cross grid, exec-bar lags).

6. ADVERSE-ZONE (job 5b, §3.5): per the step-0 branch (join or scoped re-walk on
   continuation+cascade anchors only). Report with its matched-null row. PARTIAL-eligible if
   the re-walk is over budget.

7. FIXTURES (§6). PREDICTIONS (§8, falsifications first). EXPLORATORY ANNEX (§10) — the
   pre-declared cuts incl the operator's 4H-9/89 -> 89/200 -> LTF-entry pattern, each labeled
   in-sample/not-validated with cross-TF replication status. Artifacts + all ledger entries
   (§11). Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: trade anything or touch the trading layer · re-run the
census or re-walk any price outside the §3.5-scoped anchors · tune the toll, threshold,
pooling, or drop rule to outcome · report any enriched-dataset or annex pattern as a
validated finding · promote a single-timeframe pattern without cross-TF replication · touch
the lockbox · substitute an estimate for any dropped zero-carrier record (drop-and-count).

Report back: schema-pin (the four records + the §3.5 resolution), fixture table (F1b-BYTE /
F1b-DERIV prominent), D1b-D6b, the four-row scorecard (falsifications first), the exploratory
annex (clearly separated), census1b_results.json, census1b_termini_enriched.jsonl.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-22. CENSUS-1b does four disciplined things and opens one wide door. The four re-scores are arithmetic on a byte-frozen substrate: they put the census's ranking, its confluence combination, its pullback edge, and its factor framework into the units that decide whether a trade pays, and they re-test the cascade asymmetry the run summary had flattened to noise. The wide door is the operator's move-anatomy substrate — the cross cascade bracketing every pullback, and whether drawdowns land on structure — and it is opened behind the phase's spine: everything through it is a hypothesis, quarantined, replication-gated, never a fact, until a separate pre-registered contract tests it against the lockbox. Whatever survives graduates to a Tier-C; whatever the anatomy captures generate is a map of where to look next, in a project whose central lesson is that the edge lives not in cleverer entry signals but in exits, toll-space, and structure.*
