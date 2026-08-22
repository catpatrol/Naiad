# S-1 Findings — Report 3: Winners, Losers, and the Multi-Timeframe Map
## A plain-language account of what the instrumented replay measured, what it overturned, and what it suggests — for the engine, and for the chart

**Date:** 2026-07-18 · **Author:** reviewer (Claude, Fable-mode) · **Status:** delivered for operator review; not yet committed.
**Evidence base:** S-1 instrumented replay (engine 1.0.9, config `v12_anchor_g8` unchanged, seed 20260719), verified PASS — 8/8 fixtures, byte-identity to the TC-4 baseline across all 20 cells, determinism 20/20 on journal *and* sidecar, chain of custody pre-registration `e459bca` → implementation `17c927f` → completion `7c546c5`, `git diff` empty on the strategy files. Artifacts: `s1_results.json`, `S1_MEASUREMENT.md`, run manifest. Reviewer verification: internal-consistency recomputation inside the JSON (mandate splits sum to grid totals exactly on spot-checked candidates; sidecar row totals reconcile to the per-cell manifest at 107,910 = 69,395 + 29,270 + 5,267 + 3,978).
**Provenance convention:** *[measured]* = read from the verified S-1 artifacts. *[verified]* = additionally recomputed or source-confirmed this session. *[expect]* = reasoned, unmeasured. *[open]* = named unknown.
**Standing caveats that apply to every number here:** all figures are **in-sample** on mined data (VR-1); candidate exits are **first-order** (computed on the trades the baseline actually took — a really-adopted rule changes the trade set); candidate "1× proxy" applies each trade's journaled costs to the counterfactual exit and is a proxy, not a fill simulation. These tables **rank**; only a Tier-C run **validates**.

---

# Part 0 — For a reader arriving cold: what happened here

A mechanical trading system ("Naiad") was replayed over 4.5 years of cryptocurrency history, taking **exactly the same trades** as its current baseline — and, alongside every trade, the engine wrote down what a few dozen candidate rule-changes *would have done instead*: eight families of alternative stop-trailing and profit-taking rules, alternative entry filters, alternative "add to the position" triggers, alternative re-entry triggers, alternative zone geometries, looser reversal-detector settings, and a full multi-timeframe snapshot (what the moving averages on seven different chart speeds were doing around every trade). Nothing traded differently — a byte-for-byte comparison against the baseline proves it — so every difference in the tables below is measurement, not accident.

The baseline being measured against: **−1,796.99 R net over 2,599 campaigns** (gross +275.99 before costs; win rate 10.85%), with the swing and position mandates already statistically indistinguishable from breakeven and the intraday mandate carrying 80% of the loss. The purpose of S-1 was to find, with numbers, which levers move that book — before spending any of the study's five precious validation slots.

Nine predictions were registered before the run. **Four were falsified.** As always in this project, the falsifications are the most valuable rows.

---

# Part I — The scorecard, and what each falsification teaches

| # | Registered claim | Prior | Verdict | The lesson |
|---|---|---|---|---|
| P-S1-RAT | Some trailing-stop candidate achieves ≥25% median capture at ≤20% noise-stopouts (the "beacon") | 60% | **FALSIFIED** | The beacon is unachievable *as posed* — see Part II. Noise-stopout barely varies across all 24 candidates (60–66%); it is a property of the market at these exits, not of the rule. |
| P-S1-DG | Killing/halving campaigns whose stop hasn't reached breakeven by N hours is worth ≥ +200 | 55% | **FALSIFIED** | Best variant (kill at 12h) is worth **+24.98**; the 24h/48h variants are *negative* (−42.75 kill@24h). The G-8 guards already ate this lever — the mc=1 debris was mostly tight-stop donation, now gone. Dead-gate is dropped. *[measured]* |
| P-S1-AB | The refused re-entry trigger (CONFIRM-while-flat) performs no worse than the traded one | 55% | **FALSIFIED decisively** | It would have done **−2.87/unit** (CI [−3.62, −2.20]) vs −0.755 traded — and the terminal census shows why: **74% (51,661 of 69,395) are geometrically invalid** — the would-be fill sits on the wrong side of its own stop. The charter's "while positioned" clause is vindicated with numbers. TC-2 keeps that door closed. *[measured]* |
| P-S1-MTF | Some registered multi-timeframe confluence separates outcomes by ≥ 0.5R | 50% | **FALSIFIED** | Best registered form separates by **+0.39R** (30-minute structure aligned at entry) — real, large, but under the bar. The bar was too ambitious for a single marginal condition; the *joint* conditions are unmeasured (Part IV). |
| P-S1b | Non-advancement explains ≥⅓ of the +1R-touched-then-lost population | 75% | **CONFIRMED overwhelmingly** | **90.35%** of ≥1R-MFE gross losers had *zero* stop advances before their peak; grid median advances = 0; and when the stop does advance, it does so within a median of **11 bars**. The PROTECTED paradox is now a measured fact, not an inference. *[measured]* |
| P-S1-RAT2 | The two-axis winner is not the X-A-style exec-e200 trail | 55% | CONFIRMED | Winner `pivot_5_5_n3` — but by the min-noise tiebreak on an **empty qualifying set**, which is the beacon's failure restated, not a victory for pivots (their totals are negative). |
| P-S1-ADD | Some mid-trend add trigger averages ≥2 admissible firings per multi-tranche campaign | 60% | CONFIRMED | Three do (brk20, brk55, pull-to-e9); the drought is solvable — Part VI. |
| P-S1-V | Loosening V fires ≥5× more, and the incremental firings are not better | 70%/55% | CONFIRMED both halves | All-loose fires 12.2× (1,929 vs 158) and the incremental events are *worse* (median forward-20: −0.026R vs +0.185R). TC-3 as a sweep is dead — with one small asterisk (Part VII). |
| P-S1-Z3 | The asymmetric 200-centered Z3 labels a smaller, better cohort | 55% | CONFIRMED | Labels 14.7% of the current Z3 population at **−0.555/unit vs −0.743** — and the full zone tables reveal something bigger (Part V). |

---

# Part II — The ratchet paradox: the two goals we set are enemies

This is the central finding of S-1, and it falsifies the frame both of us were working in — my beacon, and the intuition that "a good trail protects the typical winner."

Twenty-four candidate trailing/harvest rules were priced on every trade. Two numbers describe each: **median capture** (of the trades that reached +1R, what fraction of their peak did this rule keep, for the *typical* one?) and **total gross** (summing everything, did the rule make more than the current all-or-nothing?). The table below is the grid summary; the full 24×4 tables are in `s1_results.json`. *[measured]*

| Rule family (grid) | Median capture of the typical winner | Total gross vs baseline (+275.99) |
|---|---|---|
| Giveback trails (arm at +1R/+2R, exit on 30–50% giveback) | **+31% to +37%** — best protection of the typical winner | **−330 to −380** — worst totals in the set |
| Chandeliers, R-ladder, hybrid | +6% to +19% | −305 to −439 |
| Pivot trails (the operator's 5m two-lower-highs practice, mechanized) | −11% to +4% | −136 to −188 |
| Exec-timeframe e200 (X-A / Prometheus's winner) | +2% to +7% | −143 to −150 |
| 1h e89 (the operator's multiday practice) | ≈ −35% | −55 to −58 |
| **Governor-timeframe e89/e200 trails** | **−31% to −37% — the typical winner exits at a loss** | **+304 to +584 — the only family that beats the baseline** |

Read that last row twice, because it is the uncomfortable truth of the whole system: **the only exits that make more money are the ones that sacrifice the typical winner entirely.** The governor-e200 trail (the slowest structural line available — the 200-period average of the 4H chart on swing, the 12H chart on position) lets the median +1R trade round-trip all the way to a loss — and still more than **doubles** the grid's gross (+584.50 vs +275.99 for the best variant, `ema200_gov` with a half-ATR cushion; 1× proxy −1,488 vs −1,797). Every rule fast enough to protect the median winner amputates the tail, and the tail is worth more than every median winner combined.

**Why the beacon was unachievable:** the noise-stopout axis turned out to be nearly constant — 60% to 66% across *all* 24 candidates, fast or slow. At any exit this system takes, price resumes ≥1R within 20 bars roughly two-thirds of the time. That is a statement about how these markets move around this system's exits, not about the rule. So the two-axis card degenerated: no candidate qualified, and the "winner" fell through to a min-noise tiebreak that means nothing. The beacon gets renegotiated by this evidence, not defended: **the objective is total net (with strip-best printed), and median capture is reported as context, never as a target.** *[verified against the scorecard; renegotiation proposed, operator's call]*

**The mandate split makes it sharper** *[measured]*:

| Mandate | Baseline (0× / 1×) | Best candidate | Candidate (0× / 1× proxy) |
|---|---|---|---|
| **Position** | −0.07 / −73.80 | ema200_gov b0.0 | **+462.97 / +389.25** |
| Swing | +178.37 / −282.12 | ema89_gov b0.0 (gross) · ema200_gov b0.5 (net proxy) | +272.35 / **−212.67** |
| Intraday | +97.70 / −1,441.07 | *(none — every candidate is worse than baseline)* | best is −118.28 / −1,657.05 |

**Position is the headline.** A mandate whose gross was exactly zero becomes **+389 net at the 1× proxy** — the first large positive net number in this project's history — simply by exiting on the 12H-chart 200-EMA cross instead of the campaign stop. The 12H trends run for weeks; the current stop surrenders all of it; the slow trail keeps it. Three honest caveats ride with that number before anyone celebrates: it is first-order (same entries), it is a cost *proxy* (longer holds accrue more funding than the proxy credits — funding measured ~0–1% of costs, so small, but real), and **no per-candidate strip-best exists yet** — on 211 campaigns the concentration question is live and must be answered before TC-1 trusts it. *[open — strip-best per candidate queued]*

**Intraday confirms its diagnosis a third way.** Nothing helps — every one of 24 exit rules loses to all-or-nothing, because the median intraday excursion (10 bps at peak against a ~19.6 bps toll) has nothing for any exit rule to harvest. The fix remains the denominator (TC-5's 1H/5m re-spec; the bps floor), not the exit.

**And one deep design tension is now quantified.** The winning exits are precisely the ones under which adds never unlock: mean adds-would-be-eligible per tranche under the governor trails is **0.01–0.06**, versus ~0.29 under the fast (losing) chandeliers — because a slow trail almost never carries the stop to breakeven, and breakeven-on-everything is the add gate. **Tail-riding exits and pyramid-building ratchets are opposite ends of the same dial.** Part VIII lays out the three ways to resolve that, including one that may already be measured pending a one-line semantics confirm from the builder.

---

# Part III — Winners vs losers: the comparative anatomy (ask *a*)

Pooling S-1's new columns with the RC/TC-4 record, here is the cleanest side-by-side the data supports. "Winners" is proxied three ways that agree: the 390-ish positive campaigns, the mc≥2/mc=3 concurrency cohorts (the only positive population), and the PROTECTED tranches that kept their excursions.

**What winners share** *[measured unless noted]*:

1. **The stop advanced early.** When a campaign's stop advances at all, the first advance comes at a **median of 11 bars** after fill. Winners are campaigns where the market volunteered a second signal almost immediately; the pyramid cohort (mc=3, +4.88 expectancy) is the extreme of this.
2. **Fast-timeframe structure agreed at birth.** 30-minute structure aligned at entry: **63.5%** of all campaigns → **67.7%** of mc≥2 → **72.0%** of mc=3. The corresponding outcome separation is the largest single marginal effect found: aligned −0.549 vs not-aligned −0.939 per campaign (**+0.39R**, n=1,650 vs 949, CIs disjoint). Exec-timeframe structure alignment behaves the same (+0.30R).
3. **The slow timeframes had room left.** Winners were *not* entered beyond the daily/12H 200-EMA. Entering with price already beyond the 1d e200 costs −0.20R (−0.788 vs −0.585); beyond the 12h e200, −0.16R; beyond the 1d e89, −0.20R.
4. **Their stops were payable.** Stop distance ≥ 2× round-trip cost in bps. The complement — stops under 2× cost — carried −1,436 of the grid's −1,797 (Part IX).
5. **Stage-2 enriched in the pyramid cohort** (55.9% of mc=3 vs 46.1% of all): the deepest winners trade *with* the governor's structure.
6. **Mid-trend continuation signals were available to them**: the ribbon re-cross *while positioned* averaged **+0.174R** forward per firing (n=1,809) — the best raw add-trigger measured (Part VI).

**What losers share:**

1. **The stop never moved.** 90.35% of trades that touched +1R and still died at a loss had zero stop advances before their peak. This is the single most common fingerprint of a losing trade that once looked good.
2. **They were re-entries with tiny stops in price terms** — the serial machine's fills, now down to −0.755/unit after the guards but still the largest loss class.
3. **They were mid-band entries.** Under every counterfactual zone geometry, the cohort entering *around the governor e89* — deep enough to leave Z1, not deep enough to reach the 200 — is the **worst-performing structured cohort**: −0.84 to −0.94 per unit (Part V).
4. **They chased mature moves** — entered beyond the daily 200/89 (−0.20R), or with 30m structure still against them (−0.94 cohort).
5. **They were intraday** — where the median trade's best moment can't pay the toll regardless of any other property.
6. **The refused population deserves honorable mention:** the CONFIRM-while-flat "re-entries" the engine never took would have been the worst cohort ever measured (−2.87/unit, 74% geometrically invalid). Sometimes the system's best trades are the ones it refuses.

**What surprised us — things S-1 wasn't designed to find:**

- **The engine's own quality instrument doesn't predict the pyramid.** Grade-A share is *flat* across all → mc≥2 → mc3 (38.6% → 40.2% → 35.5%), and zone is nearly flat too. The two birth features that *do* enrich the winning cohort — 30m alignment and stage — are one the engine ignores entirely and one it uses only as a size modifier. The quality signal the system needs is one it already computes and throws away. *[measured]*
- **The winners-vs-losers axis is not "which trades" nearly as much as "which exits."** The same entry stream, exit-swapped to the governor trail, moves the grid gross from +276 to +584. Entry surgery (Part IX) then removes the unpayable tail. The two levers are different terms of the same sum and, unusually, they don't obviously overlap.

**The joint fingerprint is unmeasured and free to measure.** Every marginal above is a one-variable split. The natural composite — *30m-aligned AND not-beyond-1d-e200 AND stop ≥ 2× cost in bps* — is exactly the kind of cell the annex can't show. Since the S-1 journals now carry every ingredient per tranche, this is a **Tier-A pass (RC-7)** costing nothing. Proposed deliverable: the 2×2×2 lattice of those three conditions, per mandate, with campaign expectancy, n, CI, and share of Σwins per cell — plus the same lattice restricted to R1s only (birth decisions), so it reads as an admission policy. *[proposed]*

---

# Part IV — The multi-timeframe map (ask *b*)

The capture set recorded, for every trade, the position of price against the 9/89/200 EMAs and the structure state on seven timeframes: the execution chart, 15m, 30m, 1h, 4h, 12h, and the daily. Fourteen marginal splits were computed. Arranged by timeframe, they form a **gradient** — and the gradient is the finding *[measured]*:

| Timeframe | "Structure aligned at entry" effect | "Price beyond the 200-EMA at entry" effect |
|---|---|---|
| exec (1m/5m/15m) | **+0.30R** | +0.11R |
| 30m | **+0.39R** | +0.04R |
| 1h | +0.06R | **+0.18R** |
| 4h (swing governor) | −0.03R | +0.03R |
| 12h | −0.15R | **−0.16R** |
| 1d | −0.10R | **−0.20R** |

Read down the columns: **below the governor, agreement helps; above the governor, extension hurts.** The best entries in this system have the *fast* structure already turned in the trade's favor (the 30m and execution charts confirming) while the *slow* structure still has room (price not yet stretched beyond the 12H/daily 200). That is the mechanical fingerprint of **"early in the big move, confirmed on the small"** — and its mirror image, entering when the daily is already extended, is the fingerprint of chasing, worth −0.20R per campaign across 1,361 trades.

Three sharper points inside the gradient:

1. **The 30m chart is the most informative timeframe in the entire stack** — more than the governor itself (whose own alignment effect is ~zero, because arming already conditions on it). The engine computes 30m structure nowhere today; S-1 had to resample the bars to see it. +0.39R separation, disjoint CIs, and monotone enrichment into the pyramid cohort make it the strongest *new* birth-quality candidate in the study. Two honest cautions before it becomes a rule: it was measured as a marginal, not jointly with grade/zone/mandate (RC-7 resolves this), and one of fourteen annex splits clearing +0.39 carries some multiple-look risk even at these n's — which is exactly why it must survive a pre-registered Tier-C, not be adopted from an annex. *[measured; caution stated]*
2. **The 1h e200 is a meaningful line for every mandate.** Price above it at entry: +0.18R. Holding above it for ≥80% of the trade: +0.34R — though that second number is partly outcome (staying above the line *is* winning), so treat it as an in-flight health monitor, not a birth predictor.
3. **The registered-vs-exploratory discipline held.** All three pre-registered confluences landed under the 0.5R bar (hence P-S1-MTF's falsification), and everything else in this Part is **hypothesis-generating annex material under VR-1** — it informs the next pre-registration; it gates nothing today.

**Can EMA behavior across timeframes advance the system?** On this evidence: yes, in three specific, testable ways — as a **birth filter/size-tilt** (30m alignment; not-beyond-1d-e200), as an **exit reference** (the governor-timeframe 200, Part II — technically an at-governor line, discovered through the same capture), and as an **in-flight monitor** (the 1h e200 hold). And one specific way it does *not*: as a universal "more alignment is better" doctrine — above the governor, alignment shades negative and extension is outright harmful. Confluence has a direction.

---

# Part V — Zones: the U-shape nobody predicted

The zone-geometry shadow relabeled every signal and fill under nine counterfactual geometries. Two results *[measured]*:

**The operator's asymmetric 200-pocket works as designed.** Z3 redefined as a band hugging the governor 200-EMA (0.25·ATR beyond it, 0.5·ATR toward the 89) labels a small, selective cohort — 105 fills, 1.7% of the book — at **−0.555/unit, the least-bad structured cohort in any geometry**, versus −0.743 for the current Z3. Widening the near-side pad (b→0.75, 1.0) degrades it monotonically (−0.854, −0.888): the value is *at the 200*, and dilution destroys it. P-S1-Z3 confirmed; VS-Z3 is now decidable with the deep-narrow variant as the evidence-backed form.

**The unpredicted finding: zone quality is U-shaped, not monotone.** Once Z2 and Z3 are separated (which every counterfactual geometry does), the picture across all nine variants is consistent:

| Location of entry | Per-unit net (range across geometries) |
|---|---|
| Z1 — shallow, at the fast EMA | −0.62 to −0.65 |
| **Z2 — the mid-band, around the governor e89** | **−0.81 to −0.94 (always the worst)** |
| Z3 — deep, at the governor e200 pocket | −0.56 to −0.74 (best when narrow) |
| No zone / ungraded | −0.50 |

The retracement-depth story ("deeper is better") was monotone in *pullback fraction*; in *EMA-location* space it bends: shallow entries are mediocre, **entries at the mean (the e89) are the worst place on the map**, and entries at the deep structural line (the e200) are the best. A plain-language reading a discretionary trader will recognize: the first touch of the fast average is a scalp, the deep flush into the 200 is a gift, and the half-hearted dip to the 89 — the "kiss of the mean" — is where trends chop hardest. The design implication is inverted from anything previously proposed: the candidate isn't "widen Z3," it's **prefer the 200-pocket, and demote or size-down the e89 mid-band**. *[measured; joint confirmation with stage/mandate belongs in RC-7]*

---

# Part VI — Adds and re-entries: one family, two verdicts (and the drought has a solution)

The same signal family — the ribbon re-cross (CONFIRM) — received both the best and the worst verdicts of the phase, split entirely by *when it fires*:

- **While positioned** (the "recross" add trigger): mean forward outcome **+0.174R** per firing, 1,809 firings, and **59% already admissible under the baseline stop** — no ratchet change needed. The best raw add signal measured. *[measured]*
- **While flat** (the refused not_positioned population): **−2.87/unit**, 74% geometrically invalid. The worst cohort ever measured. *[measured]*

Momentum continuation is information when you're in the move and noise when you're not. The charter's asymmetry — which none of us could justify with numbers until today — is exactly right.

The drought verdict: the pyramid's binding constraint (add-signal scarcity mid-trend, ~0.6 opportunities per campaign) is **solvable**. Pull-to-e9 fires 7.7 admissible times per multi-tranche campaign under the fast-stop candidates; brk20 4.4; and recross needs no stop change at all. Mean outcomes are positive across all five triggers (+0.07 to +0.17 gross). Supply is not the problem anymore — **integration is** (Part VIII), because the triggers are most admissible under exactly the stop candidates whose exits lose money.

**TC-2's design consequently simplifies to two planks, both evidence-forced:** keep the CONFIRM-while-flat door closed (A/B, decisive), and put the re-entry quality bar in **basis points, not ATR** (Part IX). The gov-ATR cluster re-measure came back with a real population this time (median re-attempt distance 2.05 gov-ATR; **32.8% in-cluster at k=1.0** vs ~5% at exec scale) — so the operator's "same area" concept is now *measurable* — but with attempt-number expectancy flat (RC-6) there's still no evidence a count cap adds value over the quality bar. Parked, not dead. *[measured]*

---

# Part VII — The V reversal: the sweep is dead; one knob blinks

The loosened-threshold shadow generated 1,929 hypothetical V firings against the baseline's 158 — a 12.2× frequency increase — and the incremental events are *worse* than the baseline's (median forward-20: −0.026R vs +0.185R). Wholesale loosening manufactures junk; **TC-3 as a sweep is struck, by pre-registered prediction.** *[measured]*

One honest asterisk before the file closes: the knobs are not equal. The *window* loosenings produce clearly negative increments (−0.12, −0.13); the *extension* loosenings ~zero; but the **volume-confirmation** loosenings (vol_1.0 / vol_1.1) produce incremental firings at **+0.68R median forward-20** — better than baseline V itself — on **17–26 events**. That n is far too small to act on, and after nine variants it may simply be the lucky cell. It is logged as a **forward-paper watch item** (Naiad's collector flags vol-loosened V candidates live, evidence accrues for free), not a Tier-C run. The correct amount of hope here is a bookmark. *[measured; explicitly underpowered]*

---

# Part VIII — What this does to the Tier-C queue (the design fork, stated plainly)

**TC-1 is redefined by falsification.** It was chartered as "rebuild the ratchet around the two-axis winner." The two-axis card collapsed; the pivot family lost money; the winner is a family we called an exit, not a ratchet. The evidence-led TC-1 is a **2×2 factorial, four pre-registered runs**: {exit: baseline all-or-nothing **vs** governor-e200 trail (b=0.5 grid form; b=0 on position)} × {admission: none **vs** bps floor m=2}. Four cells because the two levers attack different terms (exit-side capture; entry-side toll) and their interaction is the thing no first-order table can show. Mandate-stratified predictions to be registered: position strongly positive, swing mildly positive, intraday unmoved-or-worse on the exit axis and strongly improved on the floor axis. Every run gets its G-7 ledger line. *[proposed — operator ratification required]*

**The adds tension needs one ruling, and possibly zero new code.** Three resolutions exist for "the winning exit never frees adds":

- **(i) Two-line architecture:** the campaign stop keeps its event-driven ratchet (so breakeven, and therefore add-eligibility, still happens) while the governor trail acts as a separate *harvest line* — the position exits at whichever is touched first. This preserves the operator's ratified BE-gate principle *and* the tail-riding exit. Crucially, it may **already be measured**: if the builder implemented the EMA candidates as "stop = max(native stop *as it continues to advance*, trail line)", the candidate *is* the two-line union and the Part II numbers already price it. If instead the native stop was frozen at engagement, two-line is a cheap S-1b mini-shadow. **One-line builder confirm required before TC-1 is contracted.** *[open]*
- (ii) Re-key add-eligibility to open profit (j×ATR) instead of stop-at-BE — measurable, but it abandons the operator's stated principle and re-couples adds to price noise.
- (iii) Accept the trade-off: run the slow exit, let the pyramid stay rare, and take the recross trigger's 59% baseline admissibility as the add channel. Zero new mechanisms.

My lean, flagged as a lean: **(i)** — it is the only resolution that honors both ratified principles at once, and its measurement status is one question away.

**Also settled by this phase:** dead-gate dropped (+25 best, negative beyond 12h) · TC-3 struck (vol-knob → forward watch) · CONFIRM-while-flat stays closed · VS-Z3's evidence-backed form is the **deep-narrow asymmetric pocket (0.25, 0.5)** — proposed to enter the five-slot competition as a candidate, alongside the **30m-alignment birth filter/tilt** (new, needs a name — proposed **C13**) pending RC-7's joint table.

---

# Part IX — Entry admission: the basis-point floor dominates

The flag books priced two floor philosophies on the same fills *[measured]*:

| Floor | Fills removed | Loss removed | Removed per fill | Remaining book (1×) |
|---|---|---|---|---|
| bps, m=0.5 (stop ≥ ½× round-trip cost) | 193 | −187.80 | **−2.08/unit** | −1,609 |
| bps, m=1.0 | 1,429 | −777.03 | −1.21 | −1,020 |
| **bps, m=2.0** | 3,813 | **−1,436.23** | −0.85 | **−361** |
| ATR (structure anchor), Y=1.0 | 4,302 | −1,384.35 | −0.73 | −413 |
| ATR, Y=1.25 | 5,190 | −1,546.45 | −0.68 | −251 |

At every operating point, the **cost-denominated floor removes more loss per fill removed** than the volatility-denominated one — because the disease was always cost-vs-stop-in-price-terms, and the bps floor measures the disease directly while the ATR floor measures a correlate. The m=2 point is striking: 60% of fills carry 80% of the remaining loss, and the surviving 2,491-fill book stands at **−361 at 1× before any exit change**. (The pure fill-anchored ATR floor at 0.5 flags zero fills — the G-8c guard already owns that region — a tidy internal consistency check.) The floor's m is an operator dial with a visible curve; **m=2 for the TC-1 factorial, m as TC-2's re-entry bar** are the proposed defaults. First-order caveats as always: removed fills change the equity path, rail, and halts; the factorial measures the truth.

---

# Part X — For the chart, not the machine: SSv11.4 suggestions (ask *c*)

Everything below is **display-only** — overlays for discretionary judgment on TradingView, in the spirit of the v11.3 patch: no logic changes, parity untouched, the trader stays the decision-maker. Each item cites the measurement that earns it a place on the chart.

1. **The Confluence Dashboard (two lamps).** A small corner table: **FAST** lamp green when 30m *and* exec structure are aligned with the intended direction (+0.39R / +0.30R cohorts); **ROOM** lamp red when price is beyond the 1d or 12h e200/e89 (−0.16 to −0.20R cohorts). Green-and-not-red is the measured fingerprint of the pyramid cohort; red is the measured fingerprint of chasing. This is the single highest-value addition — it surfaces the two birth features the engine provably ignores and your eye currently has to assemble from three charts.
2. **The Toll Meter.** At any prospective entry, print stop distance in basis points next to the estimated round-trip toll for the asset's tier (14/20/30 bps), with the ratio. Under 2×: the label says what the data says — *donation*. This is the cost identity made visible; it would have flagged 3,813 fills carrying −1,436.
3. **The Harvest Line.** Plot the governor-timeframe e200 (with an optional 0.5-ATR cushion) as a distinct, heavy line labeled as the exit reference — the only exit family that beat all-or-nothing (+584 vs +276 grid gross; position transformed). Worth an honest on-chart note to yourself: your 5m two-lower-highs trail and the 1h-e89, mechanized, both *lost* to doing nothing at grid level — mechanically, without your discretionary partials layered on top, the slow line wins because the tail pays for everything. The line on the chart is the machine's advice; your partials remain yours.
4. **The 200-Pocket.** Draw the asymmetric deep zone — [gov e200 − 0.25·ATR, gov e200 + 0.5·ATR] — as the highlighted band (−0.555 cohort, best structured location), and *fade* the e89 mid-band, the measured worst place on the map (−0.84 to −0.94). This literally repaints the chart's emphasis from where the current Z2/Z3 point to where the money is.
5. **The Add Cue / Anti-Cue.** Mark ribbon re-crosses **only while positioned** (+0.174R mean, 59% admissible) as an add glyph; suppress or grey the same glyph when flat (74% geometrically invalid, −2.87/unit). Same signal, opposite meanings — the chart should say so.
6. **The Stale-Protection Timer.** When open profit ≥ +1R and the working stop hasn't advanced, print bars-since-last-advance. The 90.35% finding, as a live nag: median first advance comes by bar 11 — a counter reading 40 while up 2R is the PROTECTED paradox happening to you in real time.
7. **Watch-only: V-lite markers** at the volume-loosened threshold (hollow triangles, explicitly experimental) — 17–26 events at +0.68R median forward-20 is a bookmark, not a signal; the chart can help you accumulate the discretionary sample the data can't yet supply.

Items 1–2 are near-trivial Pine; 3–5 are modest; all are parity-safe. Proposed as the SSv11.4 backlog (B-4…B-10) for a display-only patch cycle, sequenced after the current Tier-C work so the chart and the engine learn from the same evidence.

---

# Part XI — Next steps

1. **Operator:** accept the phase; push (completion `7c546c5` and predecessors).
2. **One-line builder confirm** (gates TC-1's design): *"In the S-1 EMA-trail candidates, after engagement does the candidate stop take the max of the trail and the native stop as the native stop continues to advance on later signals — or is the native stop frozen at its engagement value?"* Union ⇒ two-line is already measured; frozen ⇒ a cheap S-1b mini-shadow first.
3. **RC-7 (Tier-A, free):** the joint-confluence lattice (30m-aligned × not-beyond-1d-e200 × bps≥2×cost), per mandate, R1-only companion table, plus per-candidate strip-best for the governor-trail exits (closes the position-concentration question). I draft the contract on your word.
4. **TC-1 factorial ratification:** the 2×2 (exit × floor), four pre-registered runs, mandate-stratified predictions — plus your ruling on the adds resolution (i/ii/iii above).
5. **Slot bookkeeping:** VS-Z3 (deep-narrow form) and C13 (30m alignment) proposed *into the candidate list* for the five slots — competing, not consuming, until RC-7 and TC-1 report.
6. **Registered strikes to the ledger:** dead-gate dropped, TC-3 struck (vol-knob → forward-paper watch item), CONFIRM-while-flat permanently closed.

---

*Prepared by the reviewer under Fable-mode, 2026-07-18. Every number restates the verified S-1 artifacts or the twice-verified baseline record; internal-consistency recomputation performed on the scorecard's mandate/grid sums and the sidecar/manifest reconciliation. Four predictions died and each one redirected a Tier-C run before it was spent — which is the entire point of measuring first. The tables rank; the factorial validates; the slots remain the operator's.*
