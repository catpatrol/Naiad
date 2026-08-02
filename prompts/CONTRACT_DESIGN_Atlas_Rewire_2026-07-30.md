# CONTRACT — Claude Design · Cascade Atlas Rewire ("New Angles" Annex)
**From:** APOLLO — reviewer chat of Project Naiad · **To:** a fresh Claude Design session
**Date:** 2026-07-30 · **Operator:** Ludwig · **Attachment required:** `Cascade_Atlas_CENSUS_1b_v2_1.html` (the incumbent report; your raw material)

---

## 0 · Mission in one line

Act as a **data scientist specialized in data visualization**. Take the attached Atlas report — a dense, competent, conventional display of an unusual dataset — and **rewire how its information is displayed** so that hidden correlations, relationships, and new insights become visible. Deliverable: **one self-contained HTML report** with your visual taste in composition and palette, whose *purpose* is not beauty but *new angles of sight* — and part of the commission is inventing what those angles should be.

## 1 · The project, from zero

**Project Naiad** is a research program converting a discretionary crypto trader's method — called **Secret Sauce** — into a mechanical, testable system. Everything runs on historical Binance perpetual-futures data under strict scientific discipline: hypotheses are pre-registered before measurement, a sealed holdout period is never touched, and failed predictions are published as prominently as confirmed ones. The operator is an experienced trader with no programming background; reports must be readable by an intelligent non-engineer.

**Secret Sauce** reads three exponential moving averages — the **9, 89, and 200 EMA** — across a ladder of timeframes: 5m, 15m, 30m, 1h, 4h, 12h, 1d. Slow EMAs describe the regime; fast-EMA pullback-and-reclaim events time entries. The system's next version (v12) rests on one core hypothesis, and it is the reason you are being commissioned:

> **Signals are multi-timeframe AND sequential.** A cross between two EMAs happens *at a rung* of the timeframe ladder — but the same underlying move makes crosses fire *rung after rung, in temporal order*, climbing the ladder. We call one such climb a **cascade**. The hypothesis: the *order and tempo* of a cascade — which rungs fire, in what sequence, how fast, how far up the ladder it gets before dying — carries information about whether price is ranging or breaking out, and where the "meat of the move" is.

A measurement campaign (**CENSUS-1/1b**) photographed ~150,000 cross events and identified **14,560 termini** — moments where a cascade's upward propagation stopped. The attached Atlas is the census's visual report. It is honest and information-dense, but its views are mostly *compositional* (which rungs, what shares, median outcomes). The operator wants views that show **propagation**: how signals stack across time through the entire ladder.

## 2 · Exactly what data you have (verified inventory — nothing else exists in the file)

The Atlas embeds all of its data in one JavaScript object, `const D = {…}`, inside the HTML. Its 18 datasets, all **pooled aggregates across 10 assets** (grains noted):

| key | what it is |
|---|---|
| `n_termini` | 14,560 — the terminus population |
| `curtain` | per lens (1h/4h/12h/1d): the decision-curtain geometry — `h` (lens bars), `exec` (minutes), `out_lo/out_hi` (the outcome window's span in hours). **This encodes the horizon mixture — see §4.** |
| `timeline` | per EMA pair (9/89, 89/200, 9/200) × per rung: when each rung's cross sits relative to the pullback anatomy |
| `transitions` | 7×~6 matrix: given a cross at rung X, where the cascade goes next (counts) |
| `sequences` | the 15-row table from the screenshot: first-3-rung signature, n, share%, median forward MFE in lens-ATR units. Total population `seq_total` = 2,378 cascades with ≥3 rungs |
| `depth` | how far up the ladder cascades reach |
| `front_pooled`, `front_by_lens` | the leading-edge/frontier rung composition, pooled and per lens |
| `lens_comp` | lens-composition table |
| `asset_rep_1h` | the ONLY per-asset dataset: a replication check at the 1h rung |
| `gapdist`, `gap_labels`, `interrung`, `bin_labels` | inter-rung timing: distributions and p25/median/p75 of bars between consecutive rung firings (e.g. 5m→15m: n=2,844, median 41 exec bars ≈ **3.4 hours** — cascades are slow in wall-clock) |
| `hist_prior`, `hist_fwd` | per rung: when each frame fires, counted strictly-before vs after the anchor (the `WN` string in the file explains the counting caveat — keep it attached) |
| `monotone_pct` | **83.6%** of cascades ascend the ladder in strict order — the canonical climb is the norm; deviations are the interesting minority |

Also in the file: the TF color map `C` (5m→1d palette), and `GHOST = {'30m':1,'1d':1}` — these two rungs render **dashed** because they exist in the measurement but **not in the trading engine's timeframe set**; preserve that visual distinction (measurement-only vs engine-representable) in anything you build.

**What is NOT in the file — and the rule about it:** no per-event rows, no per-cascade records, no per-asset splits (beyond `asset_rep_1h`), no timestamps, no price series. **You must never fabricate, simulate, or extrapolate data.** If a view you want needs granularity the file lacks (a per-cascade event stream, price-anchored episodes, per-asset splits), you do two things: (1) build the view's *concept* only if you can watermark it "ILLUSTRATIVE — NOT DATA", or better, skip it; (2) add it to a numbered **DATA REQUEST** list in your memo — exact fields, grain, and format — and APOLLO will commission the extract from the project's builder. That channel is fast; inventing data is forbidden.

## 3 · The seed observation (the operator's, and the reason this contract exists)

Sorting the sequence table by outcome instead of share, the top signatures all **reach the 4h/12h tier within three rungs**, and each is rare:

| signature | share | n | med MFE (ATR) |
|---|---:|---:|---:|
| 15m→30m→**12h** | 0.8% | 19 | 8.46 |
| 15m→30m→**4h** | 1.1% | 27 | 7.22 |
| 5m→15m→**12h** | 1.9% | 46 | 6.69 |
| 5m→15m→**4h** | 2.3% | 55 | 6.41 |
| 30m→1h→**4h** | 0.7% | 17 | 5.65 |
| *vs the workhorse* 5m→15m→30m | **60.6%** | 1,441 | 4.44 |

The motif family sums to n≈164, ~6.9% of cascades. And one counterpoint matters: 5m→15m→**1d** prints a *middling* 4.06 — touching the *slowest* rung is not what's elevated; specifically the **4h/12h tier** is. The market's most common behaviour and its most promising behaviour appear to be nearly disjoint sets. The operator's questions, which your report should make *visually explorable*: what happens if we filter the data to these rare signatures? What if such a sequence alone marks a trade? What does the full stacking of signals across time and the whole ladder look like?

## 4 · The epistemic guardrails (non-negotiable, and part of the design brief)

This project treats visual honesty as a design requirement, not a footnote. Three caveats are structural:

1. **Horizon mixture.** The outcome column mixes measurement windows from ~4 days to ~100 days depending on each terminus's lens (the `curtain` object encodes it). Outcomes are **indicative only**; the *ordering* of rungs and sequences is the trustworthy part.
2. **Post-curtain information.** The sequence outcome uses a 48-hour counting window that includes information after the decision moment. Same consequence: indicative, not tradeable.
3. **Small n + selection on a sorted statistic.** n=19 and n=27 at the top of an outcome-sorted list of 15 rows is exactly how chance manufactures heroes. The confirmatory test happens elsewhere (the project's next census, under a pre-registered anti-fishing protocol). Your report **surfaces hypotheses; it never certifies them.**

Design consequences you must implement: every outcome visual **encodes n and uncertainty** (whiskers, opacity, area — your choice, but visibly); caveat chips **travel with the view they qualify**, not on a separate page; no view captions an unvalidated number as edge, signal, or verdict; the words "indicative only" may appear as often as needed without shame. A reader should be *unable* to screenshot a chart out of its caveats.

## 5 · The commission — invent the angles

You are free to reorganize everything. Ideas to react against — **starters, not constraints**; the best deliverable will contain at least one view nobody listed:

- **Rarity-vs-outcome plane:** share (log-x) vs median MFE (y), bubble area = n, whiskers = uncertainty — the "disjoint sets" claim as one picture, with the tiny-n heroes visibly fragile.
- **Alluvial/Sankey of the ladder:** `transitions` as flows; where cascades die, which branches climb; motif-family flows (grind-tier vs jump-to-4h-tier) tinted.
- **Fingerprint glyphs:** a compact ladder-glyph per signature (lit rungs in sequence) usable as axis labels and legend atoms — make patterns scannable at a glance.
- **Tempo views:** `interrung`/`gapdist` as the cascade's *velocity profile* — a ladder where step height is rung and step width is median wall-clock time; the 3.4-hour first step will surprise people.
- **Survival/depth curves:** fraction of cascades alive by rung reached; stratified by starting rung and by motif family; `monotone_pct` deviations as their own small view.
- **The curtain made visible:** turn caveat #1 into a chart — draw the four lens windows to scale so the horizon mixture is *seen*, not read.
- **Prior-vs-forward firing:** `hist_prior`/`hist_fwd` as mirrored distributions per rung, `WN`'s counting caveat attached.
- **A what-if filter panel:** toggle motif families and watch the aggregate views re-filter — the operator's filtering question made interactive, honestly scoped to the aggregates the file contains.

## 6 · Deliverables

1. **One self-contained HTML file** (inline CSS/JS; CDN libraries acceptable). Dark incumbent aesthetic is the starting point; you have license over palette and typography — keep the TF color identities (`C`) and the dashed GHOST convention recognizable so the two reports stay cross-readable.
2. **A designer's memo** (short, in-chat or appended in the HTML): which angles you tried, which look promising and why, what you'd build next — and the **DATA REQUEST** list if any view wants granularity the file lacks.

The operator returns both to APOLLO; promising angles feed the next census's design, and any confirmed pattern eventually reaches a TradingView indicator the operator will trade with. Your report is the exploration deck of that pipeline — the place where being creative is the job, because the verification machinery downstream is already built.

— APOLLO, reviewer of record, 2026-07-30
