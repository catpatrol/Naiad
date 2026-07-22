# CENSUS-1 — MTF Signal-Stack Census (Trade-Independent) — Builder Contract

**Phase:** v12 Study · **Tier B** (measure-only instrumentation — **generates no trades and changes no trading rule**; a pure signal-and-price census plus forward-outcome analysis). **Engine: 1.0.11, byte-untouched.** No trading occurs, so byte-identity-to-a-book does not apply; the integrity fixtures are determinism, cross-detection correctness, and forward-outcome completeness.
**Basis:** S-3 verified PASS (`f656dbd`), engine 1.0.11. Same OHLCV estate, same exploration-classic window, same resampled MTF frames. The census reads price; it does not read the trading layer at all.
**Why this phase exists (from S-3):** the confluence value is real but lives in the **slow** timeframes and only surfaced on a winning-stop book (D3: 8 conditions flipped positive, strongest at 12h/1d); the add gate is **structurally frozen** at winning moments (D4: 97.59% had no PRIME available); the retracement/pocket entry thesis is **dead** at full sample (D2). So this census questions the engine's three inherited cornerstones — **the governor timeframe, the single-cross arming, and the pullback-only add** — by observing the full multi-timeframe signal stack independent of the current entry logic, and by measuring what price does next.
**Operator purpose (2026-07-20):** "question the current trading engine and produce the clearest possible view of correlations and confluences we may have missed." All prior assumptions under scrutiny, governor and arming included.

---

## 0. Operator instructions

Save this contract into the repo → `claude` → `git status` clean → paste §12. *What you should see, in order:* (a) definitions restatement; (b) the **G-7 pre-registration commit** — the six prediction rows, the candidate-governor set, and the anti-fishing protocol, **before any analysis**; (c) the census run, twice for determinism (a full-history signal pass over all assets and all seven timeframes — sizeable, but no trading simulation; expect a while, not the TC-1 many-hours); (d) fixtures, all MATCH; (e) the deliverable tables, the pre-registered scorecard, and — kept strictly separate — the exploratory annex. Any fixture MISMATCH → halt, report. Send back `census_results.json`, `CENSUS.md`, the fixture table, the scorecard, the annex.

## 1. What this phase is

One trade-independent census that photographs the entire Secret Sauce signal stack across time, plus a disciplined analysis of what price does after each pattern. Five jobs: (1) **the cascade map** — every EMA cross on every timeframe, and how they cluster and sequence across the stack (the "confluences we may have missed"); (2) **the governor question** — re-analyze the same data under several candidate governor timeframes and compare; (3) **the arming question** — does slow-timeframe agreement gate outcomes better than a single fast cross; (4) **the decoupled-add discovery** — at the frozen winning moments S-3 identified, what non-pullback signal is firing; (5) **the confluence-combination scan** — which combinations of crosses and price-EMA states carry the best forward excursion, under strict anti-fishing discipline. Everything is emitted in the same bps+ATR basis as the S-3 substrate, so it joins the permanent comparison fabric (P-KEEP).

## 2. What this phase is NOT

Not a trading run (nothing is traded; no rule changes; no P&L is produced) · not a redesign (the census *discovers*; a new arming/add/governor rule is a later Tier-C, pre-registered against what the census finds) · not a confirmation study (it is exploratory by design — hence the hard separation between the small pre-registered prediction set and the exploratory annex) · not free of the multiple-comparison hazard (three crosses × seven timeframes × combinations is a haystack; the anti-fishing protocol in §7 is the phase's spine and is non-negotiable) · not out-of-sample (exploration-classic window; anything it finds is a hypothesis for the lockbox, never a validated edge).

## 3. The census construction

### 3.1 The signal stack (trade-independent)
For each asset, across the exploration-classic window, on each of the **seven timeframes** {5m, 15m, 30m, 1H, 4H, 12H, 1D} (5-minute floor; 1-minute excluded by ruling), compute the three EMAs (9, 89, 200) on that timeframe's own closed bars, then detect and journal **every cross event**:
- **9/89 cross** ("regime"), up and down — the current arming signal.
- **89/200 cross** ("stage"), up and down — the current structure gate.
- **9/200 cross** ("momentum-vs-trend"), up and down — **new**; the continuation-gap probe.
Each event carries: asset, timeframe, cross type, direction, timestamp, price, and that timeframe's ATR at the event.

### 3.2 The state vector (per exec bar)
At each 5-minute bar, snapshot the full stack state — for every one of the seven timeframes, the sign of {price−e9, price−e89, price−e200, e9−e89, e89−e200, e9−e200} and bars-since each of the three crosses. This is the confluence-state vector; it is the raw material for the combination scan. Mapped as-of (only closed higher-timeframe bars visible at the exec bar's open — the frozen live-governor convention; no lookahead).

### 3.3 Forward outcomes (the labeling)
Anchored on **cross events** and on **continuation moments** (§3.4), measure how far price travels each way — **MFE (peak favorable) and MAE (peak adverse), in BOTH basis points and ATR** — over horizons {20, 100, 500 exec bars} **and** a regime-scale horizon = *until the next 9/89 cross on the candidate governor* (bounded at 2,000 exec bars). The regime-scale horizon is the one that matches how the winning book actually earns (riding to the governor flip). All emitted in the substrate's basis for P-KEEP joins.

### 3.4 Continuation moments (for the decoupled-add discovery)
A bar qualifies as a continuation moment when, in the prevailing direction: price is beyond the exec e9, the exec ribbon is separated ≥ 1.0 ATR, and no pullback-reclaim (raw PRIME geometry) has occurred in the prior 20 bars — i.e., the trend is running cleanly with no pullback, the exact state S-3 found frozen 97.59% of the time. At each, record which cross events on which timeframes fired within the prior {5, 20} bars, and the forward outcome. Purpose: identify the non-pullback signal a decoupled add could key on.

## 4. The candidate governors

The census is analyzed under **four candidate governor lenses** — {1H, 4H (current), 12H, 1D} — applied as analysis filters on the single census (one run, four lenses; no re-simulation). For each candidate G, "long regime" = G's e9 > e89; events and continuation moments are partitioned by G's regime state, and forward outcomes conditioned within it. This answers "which timeframe, as governor, frames the cleanest signals" without running the trading engine four times. (12H and 1D are featured deliberately — S-3's D3 found the slow-timeframe conditions carried the strongest positive separation.)

## 5. Definitions — pin before coding

Carried: bps, ATR, MFE/MAE, steps-from-governor, dual coordinates, as-of mapping, toll (14/20/30 by asset — used only as a reference line, since the census produces no trades).
**New:** the three cross events (§3.1) · the state vector (§3.2) · continuation moment (§3.4) · governor lens (§4) · regime-scale horizon (§3.3) · **confluence combination** = a conjunction of state-vector conditions (e.g., "1D e89>e200 AND 12H e89>e200 AND 4H price>e89") · **cross-TF replication** = a pattern's forward-outcome sign holds when the same relative construction is evaluated on a different timeframe pair (the anti-fishing test).

## 6. Fixtures — any MISMATCH halts

| # | Fixture | Expected |
|---|---|---|
| F-DET | Full census run twice → journals + analysis byte-identical | identical |
| F-XDET | Cross-detection correctness: on a pinned sample cell, every journaled 9/89 cross re-verified against an independent recompute of the closed-bar EMA series | 0 discrepancies |
| F-ASOF | No-lookahead: for a pinned exec bar, every higher-TF state value equals the last-closed higher-TF bar's value (the frozen convention) | exact |
| F-FWD | Forward-outcome completeness: every anchored event carries MFE and MAE in both bps and ATR at all four horizons; regime-scale horizon terminates correctly at the governor cross or the 2,000-bar cap | 0 nulls |
| F-CFG | Data window, TF set, EMA params, candidate-governor set match the pre-registration | exact |

## 7. Anti-fishing protocol — the phase's spine (non-negotiable)

The census will surface thousands of candidate patterns; most "edges" in such a space are chance. The discipline:
1. **Only the six §8 predictions are confirmatory.** They are registered before any analysis; they are scored verbatim; nothing else in the census may be reported as a validated finding.
2. **Everything else is exploratory annex** (§10) — hypothesis-generation for a *following, separately pre-registered* test, explicitly labeled "not validated, generated in-sample."
3. **Cross-TF replication is required** for any annex pattern to be flagged worth-pursuing: its forward-outcome sign must hold across ≥ 2 timeframe pairs. A pattern that appears on one timeframe pair only is recorded as "single-instance, likely noise."
4. **No parameter is tuned to outcome.** Thresholds (ribbon-separation, horizons, the continuation-moment definition) are fixed in §3 at pre-registration; the census does not search over them.
5. **Bootstrap CIs on every reported number** (10,000 resamples, seed stated); an effect whose CI spans zero is reported as such, never as an edge.

## 8. Pre-registered predictions (the only confirmatory claims)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-C1 | A slower governor lens (12H or 1D) yields higher regime-scale forward MFE (ATR) for its aligned regime than the 4H lens does for its aligned regime | 55% | 4H ≥ both slow lenses |
| P-C2 | Conditioning on slow-stack agreement (12H **and** 1D both structurally aligned, e89>e200) lifts forward MFE materially (≥ +0.5 ATR at the 500-bar horizon) versus unconditioned | 60% | lift < +0.5 ATR |
| P-C3 | At continuation moments, at least one non-pullback cross event (candidate: 9/200 on an intermediate TF, or a faster-TF 9/89 re-cross) shows positive forward MFE (ATR) at the 100-bar horizon, sign-stable across ≥2 TFs | 55% | none sign-stable-positive |
| P-C4 | The new 9/200 cross fires at continuation moments (no-pullback) at a materially higher rate than the 9/89 cross does — i.e., it fills the gap the pullback-dependent signal misses | 55% | 9/200 not higher |
| P-C5 | Some pre-specified slow-stack confluence combination carries positive forward MFE **net of the reference toll** at the regime-scale horizon (the census's stiffest bar: a pattern that would pay) | 45% | none clears the toll |
| P-C6 | The cascade is ordered, not simultaneous: across a developing move, the three crosses fire in a consistent slow-to-fast or fast-to-slow sequence across TFs more often than chance | 60% | sequence no better than random |

*Pre-specified combination for P-C5 (registered now, from S-3's D3 flips): {1D e89>e200 AND 12H e89>e200 AND 4H price>e89 AND exec price>e9}, long; mirror for short.*

## 9. Deliverables

**D1 — The cascade map.** For each cross type on each timeframe: firing frequency, and the co-occurrence/sequence structure with the other crosses across the stack (which crosses tend to precede/accompany it, at what lag). The direct answer to "confluences we may have missed." Dual coordinates (absolute TF and governor-relative).
**D2 — The governor comparison.** Forward-outcome distributions (MFE/MAE, bps+ATR, all horizons) under each of the four candidate-governor lenses, side by side; the P-C1 verdict.
**D3 — The arming/slow-stack analysis.** Forward outcomes conditioned on slow-stack agreement versus unconditioned; the marginal value of each additional slow-TF alignment; the P-C2 verdict.
**D4 — The decoupled-add discovery.** At continuation moments: the frequency and forward outcome of each candidate non-pullback signal (per §3.4), the P-C3/P-C4 verdicts, and the ranked shortlist of add-trigger candidates for a future Tier-C. **This is the deliverable that feeds the redesign's add mechanism.**
**D5 — The confluence-combination scan.** Forward outcomes for the pre-specified combination (P-C5) and a disciplined sweep of related slow-stack conjunctions — every one reported with CI and cross-TF replication status; the P-C5 verdict. No cherry-picking; the full grid or a pre-declared enumeration.
**D6 — The cascade-order analysis.** The sequence structure of the three crosses across TFs; the P-C6 verdict.
**D7 — Cross-run join note.** Confirm the census outcomes are emitted in the substrate's bps+ATR basis and can join the S-3 substrate on the shared keys; deliver `census_outcomes.jsonl`.

## 10. Exploratory annex (kept strictly separate from §8/§9 confirmatory results)

Everything the census surfaces beyond the six predictions: the strongest un-predicted confluence combinations, the most persistent cross-cascade patterns, any governor lens that dominates unexpectedly — each with CI, cross-TF replication status, and the explicit label **"exploratory, in-sample, not validated — candidate for a following pre-registered test."** The annex is where the census earns its exploratory keep; the discipline is that nothing in it counts as a finding until a separate contract tests it.

## 11. Verdict, artifacts, ledger

**PASS** — 5/5 fixtures, 6/6 predictions scored falsifications-first, D1–D7 delivered, the annex delivered and correctly separated, determinism proven. **HALT** — any fixture MISMATCH; **F-XDET or F-ASOF especially — a cross-detection or lookahead fault poisons every downstream number.** **PARTIAL** — a deliverable genuinely blocked: name it, deliver the rest. Artifacts: `scripts/census_build.py` + `scripts/census_analyze.py` · `research_outputs/census/` roots (+`_run2`) · `census_results.json` · `census_outcomes.jsonl` · `CENSUS.md` · two ledger entries (G-7 pre-registration with the six rows, the candidate-governor set, and the anti-fishing protocol; completion with fixtures, scorecard, and the annex summary). Commit; **do not push, do not merge.**

## 12. The go-paste

```
CONTRACT: CENSUS-1 — MTF Signal-Stack Census (Tier B; engine 1.0.11 byte-untouched; measure-only, no trading)

Read Census_1_MTF_Signal_Stack_Builder_Contract.md in the repo in full first. The
contract is the authority; this paste is the trigger.

Scope in one line: a trade-independent census of all three EMA crosses (9/89, 89/200,
and the new 9/200) across all seven timeframes {5m,15m,30m,1H,4H,12H,1D}, with the full
price-EMA state vector, forward outcomes in bps AND ATR over set + regime-scale
horizons, analyzed under four candidate governors — to question the governor, the
arming, and the pullback-only add, and to surface the confluences we've missed. No
trading, no rule change.

Order of work — mandatory:

1. DEFINITIONS (contract §5). Restate in your own words: the three cross events, the
   state vector, the continuation moment and why it is the frozen winning state from
   S-3, the governor lens, the regime-scale horizon, and cross-TF replication.

2. G-7 PRE-REGISTRATION — the six prediction rows, the candidate-governor set {1H,4H,
   12H,1D}, the pre-specified P-C5 combination, and the anti-fishing protocol (§7).
   Commit BEFORE any analysis.

3. BUILD the census (§3): signal stack, state vector, forward outcomes, continuation
   moments — trade-independent, as-of mapped (no lookahead). Engine tree untouched.

4. RUN twice into research_outputs/census/.

5. FIXTURES (§6) — F-XDET and F-ASOF are the ones that would poison everything.

   *** ANY MISMATCH: HALT, report, produce nothing downstream. ***

6. ANALYSIS: deliverables D1–D7 (§9), under the four governor lenses. Every reported
   number carries a CI; the six §8 predictions are the ONLY confirmatory claims.

7. EXPLORATORY ANNEX (§10) — everything else, strictly separated, each item labeled
   in-sample/not-validated with its cross-TF replication status.

8. PREDICTIONS (§8), all six, falsifications first. Artifacts + both ledger entries
   (§11). Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: trade anything or touch the trading layer · tune any
threshold to outcome · report any annex pattern as a validated finding · promote a
single-timeframe pattern without cross-TF replication · touch the lockbox · substitute
estimates for missing fields.

Report back: definitions restatement, fixture table (F-XDET/F-ASOF prominent), D1–D7,
the six-row scorecard, the exploratory annex (clearly separated), both hashes,
census_results.json.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-20. The census is the widest-aperture instrument the project has built, and its discipline is proportional to its aperture: six confirmatory predictions, everything else quarantined, cross-TF replication mandatory, no threshold tuned to outcome. It carries the new 9/200 cross specifically to probe the continuation gap S-3 exposed, it features the slow governors S-3's confluence flips pointed at, and its single most important deliverable — D4, the decoupled-add discovery — hunts for the non-pullback signal that would let the pyramid form without the serpent eating its tail. Whatever survives the census graduates to a pre-registered Tier-C, and whatever the census generates in its annex is a hypothesis, never a fact. Every outcome joins back to the S-3 substrate.*
