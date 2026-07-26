# Trading Knowledge Foundation — v0
### The established canon, mapped against what Naiad has actually measured
**Reviewer, 2026-07-26 · living document · every claim graded**

**Grades used throughout:** `[verified]` = Naiad's own record (ledger/results, recomputed at some point by the reviewer) · `[established]` = broad agreement in the literature, replicated · `[contested]` = literature exists on both sides · `[synthesis]` = the reviewer connecting the two — a hypothesis, not a finding.

**Epistemic rules of this document.** (1) Nothing here enters the engine or the study without its own G-7 pre-registration on exploration-classic data. This document generates *candidates*, never rules. (2) Book knowledge is summarized in my own words at the concept level; no reproduced text. (3) Where the canon and Naiad's measurements disagree, **Naiad's measurements win for Naiad's market and timeframes** — the canon then owes us an explanation, not the other way round. (4) v0 is written from training knowledge of the standard literature; a search-enriched pass (recent crypto-microstructure and funding-carry work) is a named follow-up.

---

## 0. The headline convergence

Naiad's macro-ruling after CENSUS-1b — *edge lives in exit asymmetry, toll-space scaling, and location structure, not in entry combinatorics* `[verified]` — is not an anomaly. It is close to a restatement of the two most robust findings in the practitioner-plus-academic canon:

- **Trend-following returns are exit-shaped and tail-carried.** The managed-futures literature (time-series momentum: Moskowitz, Ooi & Pedersen 2012; decades of CTA track records) shows profitable trend systems with win rates routinely below 50%, whose entire expectancy sits in the right tail of holding-period returns `[established]`. Naiad independently rediscovered the same shape: the 4H cascade rung's quality ratio is 1.0724 while its **per-record median is 0.9851** — the median trade loses; the population pays `[verified]`. S-3's finding that winning book B "wins by riding to regime break, not by managing individual winners" `[verified]` is the classic trend-following exit expressed in Naiad's vocabulary.
- **Entry timing adds far less than entry *location* and exit policy.** Studies that permute entries against fixed exit rules repeatedly find expectancy is dominated by the exit/management stack `[established]`. Naiad: "no entry cohort positive under current exits" (RC-7r) and D9's falsification of nine-factor confluence (gradient ρ ≈ 0.02–0.05) `[verified]`.

The practical reading: the project's instincts are pointed where the durable literature says the money is. What follows is each school in turn, and what it *specifically* offers Naiad.

---

## 1. Auction Market Theory / Market Profile (Steidlmayer; Dalton's *Mind Over Markets* / *Markets in Profile*)

**Core claims** `[established as a descriptive framework]`: markets auction to facilitate trade; price spends most time in *balance* (value areas — the ~70% volume/time acceptance zone around a point of control) and trends only in *imbalance*; moves out of value are either *initiative* (new money extending) or *responsive* (fading back to value); structural tells like poor/unfinished highs-lows and single prints mark auctions likely to be revisited.

**Naiad resonance.** The census's strongest surviving structural fact — pullback termini land in SS zones at ~2× chance across all four lenses `[verified]` — is a location-structure result of exactly the kind AMT predicts: price organizes around accepted value, and reactions terminate at structurally meaningful shelves. The macro-ruling's "location structure" pillar and AMT's value framework are the same animal in different notation `[synthesis]`.

**What it offers, concretely:**
- *Report layers:* value area / POC / naked-POC registry, initiative-vs-responsive classification of the day's extension (already specced in the daily brief).
- *Candidate pre-registrable (D8 context):* condition the 4H-rung add on price being **outside the composite value area in trend direction** (initiative context) vs inside (responsive chop). Hypothesis: the add-edge concentrates in initiative context. Cheap to measure on the frozen substrate `[synthesis]`.
- *Candidate pre-registrable (terminus taxonomy):* tag termini by AMT structure (at VAL/VAH, at naked POC, at nothing) and test whether the 2× zone-landing enrichment stacks with value-edge confluence `[synthesis]`.

## 2. Wyckoff (accumulation/distribution, springs and upthrusts, effort vs result)

**Core claims** `[established as a descriptive framework]`: campaigns by larger operators leave phase structure; the *spring* — a stop-run below support that fails and reclaims — is the highest-quality long trigger because it converts trapped supply into fuel; *effort vs result* (volume vs progress divergence) flags absorption.

**Naiad resonance — the strongest single rhyme in this document.** The structural stop is a mechanized spring-survival policy: place the stop beyond real structure so the shakeout happens *without you being in it*. Measured: **52% of 4,167 shakeouts convert to ≥1R** under struct-1h `[verified]`, and the stop's protection comes from *width, not advance* (S-3: 100% zero-stop-advance on the winning book) `[verified]`. Ludwig's discretionary instinct here anticipated the canon before the canon was consulted — worth saying plainly.

**What it offers, concretely:**
- *Candidate pre-registrable (TC-2 — the sharpest bridge in v0):* the re-entry quality bar as a **spring test**. Re-entry after a stopout is admitted only when the stopout bar(s) show the spring signature — excursion beyond the prior structural low that closes back above it within N bars, optionally with a volume-climax filter (volume percentile on the flush bar). Hypothesis: spring-qualified re-entries carry positive expectancy while unqualified re-entries carry the 83%-of-loss cost identity `[synthesis]`. This gives TC-2 a *mechanism*, not just a threshold.
- *Effort-vs-result* as a report layer: flush-bar volume percentile printed at every new swing low/high.

## 3. Time-series momentum & trend following (TSMOM; turtle/CTA lineage; Covel's documentation of it)

**Core claims** `[established]`: past 1–12-month sign predicts continuation across asset classes; profits are tail-carried; **volatility-targeted sizing** materially improves risk-adjusted returns; performance degrades sharply at fast rebalance frequencies because costs are scale-invariant while signal decays — the fast end of the frequency spectrum belongs to market makers.

**Naiad resonance.** The cost identity — costs fixed in bps, excursions scaling with TF, "same animal, different tax bracket" `[verified]` — is the practitioner restatement of *why* the literature finds fast trend-following dies at costs. TC-5's half-result (mechanics repaired, economics still negative; intraday's disease is signal as well as scale) `[verified]` matches the literature's shape exactly: below some frequency floor, no amount of cost engineering rescues a trend signal `[established]`.

**What it offers, concretely:**
- *For the deferred sizing work (post-TC-1 "modes interview"):* volatility targeting — size ∝ 1/recent-ATR so each position contributes equal risk — is the single most defensible sizing upgrade in the literature and is count-based, not fitted `[established]`. Naiad's R-based sizing already half-implements it (stop distance in ATRs); the missing half is normalizing across cells/regimes. Park it as the leading candidate for the sizing interview `[synthesis]`.
- *A caution to keep:* the literature's skew evidence supports the operator's never-retire posture on *mandates* but not on *frequencies* — it argues the 1m/5m end may be structurally unwinnable for trend logic, which is consistent with everything intraday has measured so far.

## 4. Volume-at-price and order-flow (VSA lineage; delta/CVD; footprint)

**Core claims:** volume concentration marks acceptance `[established]`; bar-level volume-spread analysis (climax, no-demand, stopping volume) encodes absorption `[contested — descriptive value, weak standalone stats]`; cumulative volume delta and footprint imbalance add a participation dimension klines lack `[established as data, contested as signal]`.

**Naiad fit.** Volume is currently unused by the engine beyond `cap_vol_conf`. The honest sequencing: volume enters as *report context and TC-2 filter material* (the spring's volume-climax component, §2) before it earns any engine role. CVD requires aggTrades — heavy download, named-deferred in the brief spec. `[synthesis]`

## 5. Classical technical levels (Edwards & Magee; Murphy) and the calendar-level evidence

**Core claims:** prior extremes, round numbers, and period opens (W/M/Q/Y) attract and react price; the *academic* support is thin for patterns but real for **reference-level clustering** — orders demonstrably cluster at salient levels `[established for levels, contested for patterns]`.

**What it offers:** the brief's structure layer (period opens, prior H/L, distance table) is exactly the defensible subset. Chart patterns (flags, H&S) stay out of both report and engine — pattern-recognition literature is a graveyard of unreplicated claims `[established enough to exclude]`.

## 6. Oscillators and divergence (Wilder's RSI; the divergence folklore)

**Honest status:** RSI divergence as a standalone entry has weak, regime-dependent statistics `[contested]`. Naiad's own D9 result — confluence combinatorics do not tilt raw price `[verified]` — predicts exactly this. Therefore: divergences are a **context layer in the report** (they describe momentum decay, which is real) and are *not* engine candidates. If the operator ever wants them tested, the test is pre-registered like anything else — but the prior is low and should be stated as low.

## 7. Derivatives posture: funding, basis, open interest (the crypto-native layer)

**Core claims** `[established in the crypto-microstructure literature and desk practice]`: perp funding is a direct crowding/carry gauge; extreme funding percentiles precede mean-reversion risk in the crowded direction; OI expansion on a move = new positioning (trend fuel), OI contraction = covering (weaker continuation); basis encodes leverage demand.

**Naiad fit — the highest-value *new* confluence family.** The project already owns clean funding history for all seven exploration assets `[verified via DATA_CENSUS.md]`, and the cost work proved funding-scale effects matter at holding times the structural stop creates (days-to-weeks rides) `[verified]`. Candidates, in order:
- *Report layers (Tier 1/2, already specced):* funding percentile, OI change, basis.
- *Candidate pre-registrable:* funding-percentile as a **regime conditioner** on adds — the D8 add-edge measured separately in benign vs extreme-crowded funding states `[synthesis]`.
- *Candidate pre-registrable (position mandate):* net-of-funding re-scoring of the struct-1h ride population — the rides are long enough that funding drag/boost is first-order; this is CENSUS-1c job 2's natural extension `[synthesis]`.

## 8. Regime and volatility structure (vol clustering; trend/chop regimes)

**Core claims** `[established]`: volatility clusters; trend-quality regimes persist long enough to condition on; conditioning a trend system on a regime filter is one of the few conditioning families that replicates.

**Naiad resonance.** The governor *is* a regime filter — the architecture had this before the literature was consulted. The census's four-lens design and FH-3's "relative to governor" confirmation `[verified]` are regime-conditioning results. The addition worth naming: an explicit **volatility-regime coordinate** (ATR percentile) in the brief and, eventually, as a pre-registrable conditioner on entry admission — the literature says trend entries in compressed-vol regimes carry better follow-through `[established, worth testing here]`.

---

## 9. The anti-library (deliberately excluded, and why)

Elliott wave and harmonic patterns — unfalsifiable as usually stated; excluded until someone states a falsifiable version. Indicator stacking beyond what's above — D9 already falsified the genre in-house `[verified]`. Fitted/optimized parameter families of any kind — charter discipline forbids them and the overfitting literature agrees `[established]`. Social/sentiment scraping — data-quality swamp; revisit only with a specific, cheap, testable claim.

## 10. Reading list (titles only; for the operator's own shelf, in this order for this project)

1. Dalton, *Mind Over Markets* (auction theory, value areas) → §1
2. Pruden, *The Three Skills of Top Trading* or any faithful Wyckoff course text → §2
3. Moskowitz, Ooi & Pedersen, "Time Series Momentum" (JFE 2012) — the paper itself is readable → §3
4. Wilder, *New Concepts in Technical Trading Systems* (RSI/ATR at the source — ATR is already load-bearing in Naiad) → §6
5. Chan or Aronson (*Evidence-Based Technical Analysis*) for the discipline of testing claims — closest in spirit to this project's governance.

## 11. How this document evolves

v0 = training-knowledge pass (this file). v1 = search-enriched pass: recent crypto funding-carry and microstructure results, each added with citation and grade. v2+ = **operator knowledge extraction** — structured interviews that do to Ludwig's remaining tacit knowledge what the Secret Sauce port did to his chart-reading (the spring insight in §2 suggests there is more where that came from). Every version is committed to the repo (`docs/`) so it is versioned context, not chat exhaust; every candidate that graduates to a test gets its G-7 line and leaves this file for the ledger.
