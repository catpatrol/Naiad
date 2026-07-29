# HANDOFF — BRIEF lane → the lane running the census · 2026-07-27
**From:** Claude (Project reviewer, BRIEF chat, Fable-mode) · **For:** ENGINE Claude (census execution) · **Relay:** operator via project box
**Status of this document:** a specification proposal, not a registration. Nothing here is pre-registered. G-7 registration happens in the lane that owns the census, by that lane's reviewer, with its own predictions and probabilities. Provenance tags: `[verified]` independently recomputed in the BRIEF lane · `[ledger]` on the append-only record · `[ratified]` operator ruling · `[proposal]` drafted here, not adopted · `[open]` unresolved.

---

## 1. Why you are receiving this

A parallel workstream has built a **location-confluence measurement instrument**, and it is now pointed at the wrong data.

The Daily Brief is an operations artifact: a script that computes the operator's morning market report from the repo's kline and funding estate. In the last two days it grew a component that is not really an ops feature at all — a **level registry and clustering engine**. Every layer it computes (VWAPs, volume profiles, pivots, period opens, Secret Sauce zone and governor band edges) emits its levels into one pool; near-identical levels collapse; the rest cluster in price space; each cluster is scored by how many *independent tool families* agree there.

That is a mechanical implementation of the operator's oldest discretionary instinct — *"74.1 is the 30m 89EMA and a single print and the 7d rolling VWAP, so price should react there"* — and, more importantly, it is a candidate implementation of the **CCL hypothesis** already sitting in the knowledge program: the reframe from *timing* confluence to *location* confluence, adopted after timing confluence was falsified at D9 `[ledger]`.

The instrument exists. It runs daily on live data, where it can never be evidence. What it has never done is run on the scorable partition and be joined to the signal population. **That is the ask.**

---

## 2. What the brief is, in one paragraph, in case you have no context

Ten Binance USDT-M perpetuals. Three times a day `[ratified 2026-07-27]` the script tops up klines and funding, imports the signal layer read-only with trading disabled, and computes: structure levels, volume profiles and naked POCs, a VWAP complex (anchored developing W/M/Q/Y plus prior M/Q/Y with σ1/σ2/σ3 bands, and rolling 7/30/90/365-day VWAPs with the same bands), MTF RSI / StochRSI / MACD / Awesome Oscillator with regular and hidden divergences on each, a volatility regime, funding and open-interest posture, session ranges, BTC beta, and a Secret Sauce governor dashboard across the 1h / 4h / 12h lenses. It emits a JSON capture (the record) and an HTML page (a disposable, regenerable view). It writes no engine state and modifies no engine file.

**The firewall it operates under, all four clauses `[ratified]`:** live data is operations-only and forbidden as study evidence · no journal reads and no signal- or trade-outcome statistics on any window · engine modules imported read-only and never modified · the accumulating archive may be mined for hypotheses but is never a scoring window.

---

## 3. How the brief and the trading system already interact

Read-only, in one direction, today:

- The brief **imports** `engine.signals` with trading disabled to read per-bar direction, stage, active zone and stop arrays, plus signal events carrying grade, zone, stage and tier. It reconstructs the playbook state machine (DORMANT / ARMED / ZONE_ACTIVE / ENTERED / DEFENSE / POST_X) as a readable table.
- It **constructs cells directly** from committed specs rather than patching anything, following the `tc5_runner.py` precedent `[verified]`.
- It **contributes nothing back.** No rule, no threshold, no parameter has ever flowed from the brief into the engine, and under clause 1 none may without independent pre-registration on exploration-classic data.

What changes with the build now going to the builder is that the indicator recipes move out of the brief script into a standalone tracked package, **`analytics/`**, deliberately placed *outside* `engine/` so ops iteration never shares a blast radius with frozen, hash-cited engine files. That package is pure arithmetic — no I/O, no network, no engine imports, deterministic, semantically versioned, with a `analytics_sha()` printed in every artifact that consumes it.

**`analytics/` is the shared surface.** The census can import the same RSI, the same rolling VWAP, the same clustering engine the operator reads every morning. That is the mechanism by which a measurement tool gets stress-tested by daily human use before it is ever trusted with a study claim — a bug hides inside a batch aggregate, but gets caught in a week when someone reads the number every morning and says "that's wrong."

---

## 4. Why the brief needs census data

Bluntly: **the brief cannot tell the operator whether any of this matters, and it must never pretend to.**

A confluence score is a statement that several tools agree at a price. Whether agreement *predicts* anything — whether price reacts more reliably at a score-13 area than a score-4 area, whether Secret Sauce zones that coincide with high-scoring areas outperform those that do not — is a question about outcomes on scorable data. The brief is structurally forbidden from answering it, and the danger is not that it will try but that a high-scoring area **feels** like a discovery. That feeling is the failure mode the firewall exists to prevent.

So the brief needs the census to answer three things:

1. **Does location confluence carry edge?** Do SS fills born at or near high-scoring confluence areas differ in expectancy from those born in level deserts?
2. **Which families carry it?** If the effect is entirely explained by the volume-profile POC, the "confluence engine" is an expensive POC detector and should be deflated to one.
3. **Does it survive cross-scale?** An effect on one governor lens only is a candidate, not a result.

Until those are answered the brief prints confluence as description, never prediction. After they are answered — either way — the brief's rendering changes: a confirmed effect earns emphasis, a falsified one gets demoted to a decoration the operator may still like looking at.

---

## 5. Proposal A — CENSUS-1c: the confluence matrix layer `[proposal]`

### 5.1 What it is

For every signal and fill in the census population on **exploration-classic** data, attach a fixed block of confluence coordinates computed **strictly as-of that bar**:

| Field | Meaning |
|---|---|
| `conf_dist_atr` | signed distance from the fill price to the nearest confluence area, in daily ATR |
| `conf_score` | that area's score |
| `conf_rank` | its rank among all areas for that asset at that time |
| `conf_families` | which tool families composed it |
| `conf_is_lis` | whether it was a line in the sand |
| `conf_n_within_1atr` | how many areas sat within 1 daily ATR — level density, the control variable |
| `stop_conf_*` | the same block computed at the **stop** price |
| `rvwap_cross_state` | the H-RVX layer (§6) |

That block, joined to the existing signal population, is **the confluence matrix**. Everything downstream is a conditional expectancy question over columns you already know how to score.

The control variable matters as much as the treatment. In a dense level environment everything is near something; `conf_n_within_1atr` is what separates "this fill sat at a real shelf" from "this asset has levels everywhere."

### 5.2 The single biggest technical risk — as-of contamination

The brief runs live, so its levels are naturally as-of: it cannot see tomorrow. **A historical batch job leaks future data almost by default.** Three specific traps, all of which would produce a beautiful and worthless result:

1. **Prior-day profiles.** At 14:00 on day *D*, "yesterday's value area" means day *D−1*. A naive backfill computes day *D*'s profile and attaches it to signals *inside* day *D* — using the day's own outcome to describe its own setup.
2. **Pivots.** `pivot(5,5)` requires five bars *after* the pivot bar to confirm. A pivot is only knowable five bars later. Historical level registries must apply the confirmation lag; the brief gets this right live because the future bars do not exist yet.
3. **Naked POCs.** "Untested" is a statement about the future of that level. As-of, a POC is untested only with respect to bars up to the signal bar.

**Recommendation:** make as-of correctness a numbered fixture, not a code review item. The cheapest robust construction is a single forward pass that maintains the registry incrementally and can only ever see history — never a vectorised whole-history computation sliced afterwards. If the effect size looks large on first run, suspect this before celebrating.

### 5.3 Cost `[verified estimate, BRIEF-lane arithmetic]`

- Confluence output ≈ **10 KB per asset per timepoint** in parquet (≈1 KB scalars, ≈7 KB for 110–125 level rows, ≈1.5 KB for ~25 area rows).
- Full exploration-classic history across ten assets at daily granularity, accounting for the shorter histories of newer listings: **≈150–250 MB**, untracked, regenerable, and it zips into the existing archive flow. Against a 633 MB kline estate and the 19.6 GB recently reclaimed, this is not a space problem.
- The **join table** — the matrix itself, a few scalars per signal — is tens of megabytes at S-1-scale signal counts. Negligible.
- Compute: the volume-profile layer from 1-minute klines dominates. A single streaming pass over history is a few hours as a one-off, not a standing load. Re-running the daily script ~1,800 times would be far worse and should not be the implementation.

### 5.4 Where the output goes — governance boundary `[ratified 2026-07-27]`

The operator overruled an earlier and too-broad reviewer rule that would have forbidden historical application entirely. The corrected three-way rule:

- **Exploration-classic — legitimate.** This is scorable census territory under G-7. Go.
- **Lockbox (July 2024 – October 2025) — sealed.** Computing confluence there and looking at it is first-look consumption of evidence that cannot be un-spent. Not in this phase, not incidentally, not "just to check the pipeline."
- **Never into `briefs/`.** Historical output goes to `research_outputs/census1c/` with an explicit provenance marker. If retrospectively-computed rows ever landed in the same tables as live daily captures, no later analysis could distinguish "computed on the morning of" from "computed afterwards with the outcome visible," and the operator's forward archive would be silently poisoned. Physical separation makes the mistake impossible rather than merely discouraged.

### 5.5 Suggested sequencing, cheapest first

**Phase 0 — free Tier-A proxy before spending anything.** CENSUS-1 already emitted an MTF cross substrate. Cluster those crosses in *price* space rather than time, attach distance-to-nearest-cluster to existing fills, and score. If location confluence has no signal in the cheap proxy, the expensive backfill is much harder to justify. This is the CCL hypothesis in its minimum-cost form and it needs no new computation.

**Phase 1 —** freeze `analytics_version`, build the as-of harness, emit the matrix over exploration-classic.
**Phase 2 —** pre-register predictions with probabilities, join, score, report falsifications.
**Phase 3 —** cross-scale replication across the 4h and 12h governors independently.

### 5.6 Deflation gauges, to be stated before running

Following the P-CCL-3 pattern already in the knowledge program `[ledger]`:

- **VP equivalence.** If the effect vanishes once the volume-profile family is removed, this is a POC detector wearing a costume. State the threshold in advance.
- **Density confound.** If `conf_score` predicts but `conf_n_within_1atr` predicts equally well, the finding is about level density, not agreement.
- **SS self-reference.** The `ss` family contributes zone and governor band edges to the registry, so a fill *born from* an SS zone sits near an SS level by construction. **Run the primary test with the `ss` family excluded from scoring.** If it is not excluded, the headline number is circular. This is the trap most likely to produce a false positive here, and it is worth building the exclusion in rather than remembering it later.

---

## 6. Proposal B — H-RVX: do rolling-VWAP crosses confluence with the Secret Sauce EMA crosses? `[proposal — operator-originated]`

The operator's question, and it is a good one. Secret Sauce's cascade is built on price EMAs. A rolling VWAP is a **volume-weighted mean over a trailing time window** — it responds to where volume traded, not merely where price went, and it has a hard window edge rather than exponential decay. So a 7d/30d rolling-VWAP cross and an EMA cross can disagree, and the disagreements are the interesting part.

**Pre-registered pairs:** 7d×30d, 7d×90d, 30d×90d, 90d×365d. **Agreement window:** fixed before running, not chosen after.

Four formulations, all reported, not merely the best:

1. **Co-incidence** — what fraction of SS governor regime flips occur within ±N governor bars of a rolling-VWAP cross, **against a matched random-timing baseline**? Without the baseline the number is uninterpretable: two trailing means of the same series co-move by construction.
2. **Lead / lag** — the distribution of (RVWAP cross − SS cross) in governor bars. Centred, early-skewed, or late-skewed?
3. **Conditional expectancy** — do fills whose birth carries cross agreement differ in expectancy from those without? This is the one with stakes.
4. **Cross-scale replication** — independently on 4h and 12h governors.

**Deflation gauge, stated in advance.** A 30-day rolling VWAP and a long EMA on a 4h governor are both trailing means of the same price series. If co-incidence exceeds the pre-stated threshold, the finding is filed as *"these two tools measure the same thing"* — a useful negative that must not be dressed as a discovery.

**Implementation note.** Rolling VWAP is not computed anywhere in the engine today. Adoption means importing `analytics.vwap`, which is precisely the shared-toolbox case that motivated the `analytics/` split — and the first real test of whether that split holds up under study use.

---

## 7. Technical notes for whoever implements this

- **The engine has no 1d or 30m timeframe.** `INTERVAL_MS` / `MTF_SET` stop at 12h `[verified, BRIEF-lane read of engine/cells.py]`. The brief resamples its own daily frame. Daily ATR — the confluence engine's normalisation unit throughout — is therefore **not** natively available engine-side and must be resampled with the same convention, or the distances will not mean the same thing across the two lanes.
- **Volume profile is an approximation.** Volume-at-price is built by spreading each 1-minute bar's volume uniformly across its range. It carries an `approximation` provenance chip in every brief artifact and should carry one in census output too. Real tick data would move POC/VAH/VAL somewhat.
- **Rolling-VWAP σ bands** use the volume-weighted *population* variance via the one-pass identity `max(Σ(vol·src²)/Σvol − VWAP², 0)`, with no (n−1) correction — pinned from TradingView's published Pine source, which the operator supplied. It is cancellation-prone at high price with low dispersion, which is exactly the BTC case; the toolbox reports the one-pass versus two-pass discrepancy for this reason.
- **Freeze before joining.** Pin and record `analytics_version` and `analytics_sha` in the phase's registration. If the toolbox changes mid-phase, the sample is void.
- **Price everything net.** Standing project discipline: cost-in-R = cost_bps ÷ stop_bps. A gross-only confluence finding is not a finding.
- **Nothing here touches engine bytes.** `analytics/` is additive and lives outside `engine/`; F-SIG-style byte guarantees are unaffected.

---

## 8. Open item this lane is escalating, unrelated to the above

**LIT floor contradiction `[open]`.** The charter's invariant I1 fixes LITUSDT's first valid candle at **2025-12-23 00:00 UTC** (Lighter listing; earlier history is Litentry, a different asset) `[ledger]`. The brief's bar counts back-solve to a first kline of **2025-12-01** (239 daily bars, 5,700 hourly), while LIT's own **funding** history starts 2025-12-23T20:00Z — agreeing with the charter, not the klines. A status document records the floor as 2025-12-01. The same back-solve method reproduces BTC's first bar as 2019-09-08, matching the ledger exactly, so the method is sound `[verified]`.

If the estate really holds 22 days of the other LIT token, that is study-evidence contamination rather than a display defect. One printed timestamp per interval settles it. This lane cannot resolve it and is not asking to.

**Also, a correction to an earlier handoff from this lane:** a previous version stated that the brief's reported `engine_version 1.0.11` was *"consistent with the ENGINE lane's frozen-version record; no discrepancy [verified]."* That was an overclaim — this lane has no access to your record. Correct statement: the brief's signal runs report 1.0.11; the BRIEF lane's last independent record is 1.0.10; probably a legitimate bump, unconfirmed `[open]`.

---

## 9. What this lane is asking for

Nothing urgent, and no dependency runs the other way — BRIEF-2 ships and runs regardless. Concretely:

1. **Consider Phase 0** (the free proxy at §5.5) as a cheap way to triage the CCL hypothesis before anyone builds a backfill harness.
2. **Take or reject CENSUS-1c and H-RVX** as census phases. Both are drafted for adoption by your lane's own registration process, not by this one.
3. **Note the shared `analytics/` package** once it lands, and the version-pinning discipline that comes with importing it.
4. **Rule on the LIT floor.**

The brief will keep printing confluence as description in the meantime. If the census falsifies it, that is a deliverable — the operator's standing posture is that a falsification on the record is worth more than an unexamined feature, and this one would cost the brief a section it can live without.

— end of handoff. Chats cannot read each other; route replies through the operator or the ORCHESTRATOR dashboard.
