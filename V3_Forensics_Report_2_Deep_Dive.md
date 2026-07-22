# V3 Forensics — Report 2: The Deep Dive
## A plain-language account of what Naiad is, how it works, what the V3 anchor test found, and what we could do about it

**Date:** 2026-07-14 · **Author:** reviewer (Claude, Fable-mode) · **Status:** delivered for operator review; not yet committed.
**Evidence base:** V3 anchor run artifacts (engine 1.0.7 @ `2f260e1`, config `v12_anchor` sha `a3917ea5…`), `ROLLUPS_AND_HYPOTHESES.md`, `V3_STOP_AND_EXIT_FORENSICS.md` (report 1), the run `manifest.json`, engine source (`signals.py`, `trading.py`, `replay.py`) read directly this session, the operator's six interview answers (2026-07-14), the two Prometheus reports, and web research on execution mechanics (Insilico Terminal documentation; Binance fee schedule), all dated 2026-07.
**Provenance convention:** *[verified]* = recomputed or read directly from an artifact/source this session, or reviewer-recomputed from raw journals during the 2026-07-13 verification and restated from that record. *[measured, report 1]* = a report-1 figure the prior reviewer session recomputed from raw journals; not re-derived today. *[expect]* = reasoned but unmeasured. *[open]* = named unknown, queued for measurement.

---

# Part I — The project, explained from zero

## I.1 What we are trying to find out

Ludwig is a discretionary cryptocurrency trader. Over years of trading he has developed a method — the "Secret Sauce" — for reading trend structure on price charts and deciding when to enter, add to, and exit leveraged positions. The method lives partly in a TradingView indicator (a script that draws signals on a chart) and partly in his judgment.

The project asks a deceptively simple question: **how much of this method survives being turned into rules a machine can follow?** A machine cannot "read the tape," weigh a hunch, or notice that a level "looks heavy." It can only follow written instructions. So we wrote the instructions down as faithfully as possible, built an engine that follows them mechanically, and are now testing that engine against history — under laboratory rules strict enough that we can trust the answers.

Two workstreams run side by side:

- **The v12 Study** — a structured backtesting program. We replay the mechanical ruleset over years of historical price data and measure what it would have done. This report is about the study's third gate, the "V3 anchor run."
- **Project Naiad** — a forward paper-trading system that will run the same engine on live incoming prices, with no real money, to see how it behaves on data nobody has seen yet. Its data collector is built but currently parked on an infrastructure decision (where to run it from, decision CD-2).

No live capital moves until Ludwig makes a confidence call, and the evidence rules below exist so that when that call comes, the numbers behind it are honest.

## I.2 Who does what

Three roles, deliberately separated so no one marks their own homework:

- **Ludwig — the operator.** Owns every decision that matters: what gets merged into the code, what gets tested, when a gate opens or closes. The system is his method; the judgment calls are his.
- **Claude Code — the builder.** A coding agent running on Ludwig's machine. It writes and runs the code, executes the backtests, and reports results.
- **Claude (this document's author) — the reviewer.** Checks the builder's work, recomputes every headline number from the raw output files before believing it, argues against its own conclusions, and keeps the governance ledger. The reviewer proposes; the operator disposes.

## I.3 The rules of evidence (why we are so strict)

Backtesting has a famous failure mode: if you tune a strategy against the same historical data you then use to judge it, you get a strategy that memorized the past rather than one that understands markets. It will look brilliant in the test and lose money live. The whole methodology here is built to prevent that, and three rules do most of the work:

**1. Data is partitioned, and reading it spends it.** Think of historical data as exam papers. Some are practice papers you may study freely; one is the real exam, sealed, that you may sit exactly once. Our partitions:

| Partition | What it is | What it may be used for |
|---|---|---|
| **Exploration-classic** — everything up to 2024-06-30 | The practice papers | Free to mine, plot, and iterate on. The V3 anchor ran here. |
| **Lockbox** — 2024-07-01 to 2025-10-05, all assets | The sealed exam | Nothing. Opened once, at gate V8, against a bar we register in advance. |
| **Spent BTC window** — 2025-10-06 to 2026-07-07 | A used exam | The nine months already consumed developing and verifying the engine. Never again valid as an honest test. |
| **Forward paper** — live data from Naiad | Fresh exams, printed daily | Honest exactly once per frozen ruleset. |

**2. Predictions are registered before looking.** Before each test we write down what we expect and at what threshold we'd call it confirmed or falsified. Then the numbers decide. When we register a prediction badly (it has happened — twice in this run), we own the registration flaw rather than quietly re-scoring.

**3. Nothing is believed until recomputed.** Every headline number in this report was either recomputed by the reviewer from the raw output files during the 2026-07-13 verification, or read directly from source code or primary documentation this session. Summaries are never trusted on their own.

One more phrase you will meet: a **named variant slot**. The study charter allows exactly **five** named rule-changes to be tested against the lockbox. This scarcity is deliberate — every variant you test against the sealed exam consumes some of its power to surprise you. Choosing which five is one of the most consequential decisions ahead, and it is the operator's.

## I.4 What came before: Prometheus

Before Naiad, an earlier project — **Prometheus** — ported a previous version of the method (SSv10) into an autonomous single-position paper trader on three coins. It taught hard lessons that shaped everything here: its profits were carried entirely by a few large winning trades ("tail-carried"); its stop-ratchet mechanism turned out to be decorative for two-thirds of trades because most died before the ratchet ever engaged; and its take-profit machinery was the silent failure point. Prometheus also produced a recent forward-paper analysis and a data-collection design whose lessons we fold in at Part V.4. Its numbers come from a different system on different data and are **inputs to hypothesis design here, never evidence** for Naiad's gates.

---

# Part II — How the machine actually works

This part explains the engine's governing logic, piece by piece, in plain language. Every mechanism described was read directly from the engine source (`signals.py`, `trading.py`, `replay.py`) this session — not from documentation about the code. *[verified]*

## II.1 The signal brain: how the system decides a trend exists

The engine watches two chart timeframes at once for each trading configuration:

- The **governor** timeframe (for example the 4-hour chart) decides *direction* — whether we are hunting longs, shorts, or nothing.
- The **execution** timeframe (for example the 5-minute chart) decides *timing* — the exact bars on which entries and exits happen.

On each timeframe the engine computes three **exponential moving averages (EMAs)** — smoothed lines that track price at fast (9-bar), medium (89-bar), and slow (200-bar) speeds — plus the **ATR (Average True Range)**, a running measure of how far price typically moves per bar. ATR is the system's volatility yardstick: "0.5 ATR" means half a typical bar's range, so distances scale automatically with how wild the market currently is.

From these, the engine builds a small vocabulary of events:

- **Arming / governor cross.** When the fast EMA crosses the medium EMA on the governor chart, the system "arms" in that direction — it is now willing to take trades that way. Each arming starts a numbered **campaign**.
- **Regime.** The relationship between the medium and slow EMAs on the governor chart describes the larger backdrop (roughly: established uptrend, established downtrend, or transition). A campaign that arms *against* the backdrop is born **provisional** — a second-class citizen that trades smaller and is capped at grade B until the backdrop confirms.
- **Zones.** Around the governor EMAs the engine drapes proximity bands (Z1 near the fast average, Z2 near the medium, Z3 around the band of both). A pullback into a zone is where the system hunts entries — the mechanical stand-in for "price returning to value."
- **PRIME.** The workhorse entry signal: price pulls back into an active zone and then reclaims it in the campaign direction on the execution chart. The first PRIME of a campaign is **R1** (the initial position); later PRIMEs are **adds** (R2, R3 …).
- **CONFIRM.** A secondary signal — the execution-chart ribbon re-crossing in the campaign's favor — that can add to an existing position. A gate-failing confirm is journaled as a reject rather than silently dropped.
- **V (capitulation).** A climax-reversal detector: an extended, high-volume flush that snaps back, defined by five tunable thresholds (extension in ATRs, a volume multiple, a confirmation window, and switches). A V can *birth a campaign in the opposite direction on its own* — the mechanical version of catching a blow-off reversal.
- **Grades.** Each PRIME is graded **A+** (the entry sits inside a swept-and-reclaimed structure pocket — the "snipe" logic), **A** (higher-timeframe alignment agrees), or **B** (neither), with provisional campaigns capped at B. Grade determines position size. **C-grade confirms are journaled but never trade, by design.**
- **TPW (warning) and CLUSTER.** Multi-timeframe momentum turning against the position. In this engine version TPW *only writes a diary timestamp* — it triggers nothing (this matters enormously; see II.4 and Part IV).
- **X (failure).** Price closing beyond the far side of the governor EMA band for a set number of consecutive bars kills the campaign — the "this idea is wrong" exit.

## II.2 The grid: what was tested where

The strategy runs as a **grid** of independent cells: one asset × one *mandate* (a governor/execution timeframe pairing — **swing** 4H/5m, **intraday** 1H/1m, **position** 12H/15m). Each cell has its own paper account and its own risk limits; nothing is shared between cells.

The V3 anchor scored **20 cells**: the seven assets with enough pre-mid-2024 history (BTC, ETH, SOL, NEAR, ZEC, JTO, TAO) × three mandates, minus TAO-swing (insufficient sample by design — TAO listed too recently for that mandate's warm-up). *[verified — manifest]* The newer listings (HYPE, FARTCOIN) have no exploration-classic history at all, and LIT was excluded by a known data-contamination issue (G-2: its cache still holds bars from the *previous* token that owned the ticker — a trap we identified early and fence off). A further 27 cell-runs were produced as a **characterization annex** (the spent BTC window and the newer-era assets) — context only, excluded from all scoring.

Scale of the scored test: **3,456 campaigns** containing **8,387 filled tranches** across roughly **4.5 years** of exploration-classic data, replayed twice end-to-end with byte-identical results (the determinism proof — same inputs, same outputs, to the last digit, 47 of 47 runs). *[verified]*

## II.3 The stop system — the single most important mechanism in this report

Read this section slowly; almost every finding in Part III traces back to it.

**There is one stop per direction, shared by the whole campaign.** The engine keeps a single "long stop" level and a single "short stop" level. Every open tranche in a direction — the R1 and all adds — lives or dies by the *same* line. When that line is hit, **all open tranches exit together**. There is no per-tranche stop. *[verified — `signals.py` keeps one `stop_long`/`stop_short` series; `trading.py` closes all open tranches on one hit]*

**Where the stop is placed.** On any entry signal (PRIME, CONFIRM, or V), the stop moves to the *signal bar's own extreme* — its low for longs, its high for shorts — cushioned by **0.5 × ATR** of the execution chart. In trader language: just beyond the trigger bar, with half a typical bar's breathing room. All three entry kinds use the identical formula. *[verified — `signals.py:475–482`]*

**When the stop moves — and, critically, when it does not.** The stop advances **only when a new entry signal prints.** Each fresh PRIME/CONFIRM/V re-runs the same formula on the new signal bar and takes the tighter of old and new (`max` for longs, `min` for shorts — it can *never loosen*). Between entry signals the stop is **frozen**. It does not watch price. It does not watch profit. A position can run five, ten, fourteen R of open profit and, if no new entry signal happens to print during the excursion, the stop stays exactly where the last signal left it. We call this the **event-driven ratchet**, and its blind spot — profit earns no protection unless the market volunteers another signal — is the mechanical heart of the biggest leak found in Part III. *[verified at source]*

**When the stop is cleared.** Only on a direction change (the opposite side arming, or an opposite-direction V) or on campaign death (failure-X) — and every clear is paired with a flatten of any open position. A guard in the trading layer (`GateViolation`, `trading.py:313–318`) makes it a hard, run-stopping error for any open tranche to ever wake up without a working stop; the sole exemption is the one bar of an in-flight death transition, a case ratified as G-3. The anchor run completed without this guard ever firing — so, empirically as well as by construction, **no open position ever ran with a loosened or missing stop**. *[verified]*

**What does not exist:** any minimum stop distance. If the signal bar's extreme sits a hair from the fill price, the stop sits a hair from the fill price. The only distance-aware behavior is a *rejection*: an entry whose fill would land at or through its stop is dropped (`gap_through_stop`). Nothing widens a too-tight stop. *[verified — `trading.py:363–366`; grep of the engine found no floor]*

## II.4 The trading layer: what happens on every bar

Each execution bar is a "wake," processed in a fixed order (from the `trading.py` header, verified against the loop):

1. **Stop guarantee.** Assert every open tranche has a working stop (the guard above).
2. **Funding.** Perpetual futures charge/pay a small periodic funding rate; it accrues here.
3. **Fills at the open.** Queued flattens first (failure-X, opposite governor cross, V-reversal — all exit the whole position at the bar's open), then gap-through-stop exits, then queued entries — each entry re-checked at fill time against the halt calendar and the campaign's survival.
4. **Intra-bar stop check.** If the bar's range touches the stop, all open tranches fill at the stop price (or at the open if price gapped through).
5. **At the close.** Excursion tracking updates, and this bar's fresh signals become *pending* entries for the next bar's open — after passing the gates below.

**The gates an entry must pass** (each failure is journaled as a reject with its reason — the funnel is fully auditable):

- **Halts:** each cell stops taking new entries for the rest of the UTC day after −2R of realized losses that day, and for the week after −4R that week. (Positions already open still run to their stops.)
- **Max 3 tranches per campaign**, counting same-bar queued siblings.
- **Open-campaign risk ≤ 1R** projected including the newcomer.
- **Add eligibility:** an add is admitted only if the *current* stop is at breakeven-or-better for **every** already-open tranche. In plain terms: you may only add when everything you already hold can no longer lose. This makes adds structurally late-and-safe — a fact with large interpretive consequences (Part III.4).
- **Sizing** by the ratified table: grade and kind set the fraction of 1R each tranche risks (A-grade R1s largest, provisional R1s and adds smaller, V entries their own size). 1R itself is 0.5% of the cell's current equity.

**One deliberate subtlety:** a PRIME that fires *while the campaign is flat* (because the R1 was stopped out, or was never filled) trades as an ADD. The code comment states why: the May-26 marquee chart signature — a validation case from the parity work — **requires post-stopout re-entries to trade**. The same open door also admits the "orphan" pattern (adds into a campaign whose R1 never filled), which Part III finds to be the single worst cohort in the study. The re-entry we want and the orphan we don't **enter through the same door**. *[verified — `trading.py` header lines 27–30 and the vacuously-true eligibility check]*

## II.5 The cost model

Every fill pays realistic costs, recorded per tranche *[verified — manifest `cost_semantics`]*:

- **Fees:** 5 basis points (0.05%) per side — Binance's standard *taker* rate, i.e. the price of demanding immediate execution with market orders.
- **Slippage:** 2 / 5 / 10 basis points per side by asset liquidity tier (majors cheapest).
- **Funding:** accrued at each funding timestamp, realized at exit.

Deliberately **not** modeled: order-book depth, partial fills, any maker/taker split (everything pays taker), sub-bar stop paths, fee tiers, liquidation mechanics. To expose how sensitive results are to these assumptions, every result is reported at three cost levels: **0×** (all costs refunded), **1×** (as modeled — the headline), and **2×** (costs doubled — a stress line).

## II.6 The diary — and the counterfactual columns

The engine journals everything: every signal, entry, exit, reject, and halt, with prices, sizes, fees, and identifiers. Two features of the diary matter for what comes next:

**Excursion tracking.** For each tranche: **MFE** (maximum favorable excursion — the best the trade ever looked, in R) and **MAE** (the worst), plus post-exit continuation at 1/5/20 bars (what price did *after* we exited — the "were we shaken out?" instrument).

**Shadow counterfactuals.** For each tranche the engine also records what *other, untraded* rules would have done — columns in the diary, never a separate book *[verified — manifest `shadows_statement`, `shadows.py` via the logic extract]*:

- **X-A:** a two-phase exit — keep the native stop until price closes beyond the execution 200-EMA in the trade's favor ("engagement"), then trail that EMA at a 0.5-ATR cushion, never loosening. This is precisely the exit that Prometheus's testing crowned, ported as a shadow.
- **X-B:** X-A plus banking 50% of the position at the first TPW warning.
- **X-C:** X-A plus banking 50% at the first 2-ATR extension beyond the fast EMA.
- **X-D:** the operator's own Playbook §7 harvest doctrine, mechanized — 25% banked at first TPW, 25% at first extension, remainder on the X-A trail.
- **Two alternate stop families** (a prior-bar anchor variant; a volatility-frozen buffer variant), an **alternate entry** (the ribbon cross instead of the zone reclaim), and **ladder sizing counterfactuals**.

In other words: the current book is all-or-nothing, but the diary already contains, for every tranche, what four harvest-style exits and two alternative stops *would* have returned. Ranking them requires no new backtest — only arithmetic over existing files (queued; Part III.6).

## II.7 What deliberately does not exist

To a newcomer these look like omissions; they are the experiment's design. The V3 anchor tested the **v11 mechanical ruleset exactly as written** — the point was to measure the faithful port before improving it. So the traded book has: **no take-profit of any kind, no partial exits** (every exit is all-or-nothing — a source grep confirms no partial-exit path exists anywhere in the trading layer *[verified]*), **no price- or profit-following trail** (the only trail in the codebase is the untraded X-A shadow), **no time stop**, and **no minimum stop distance**. Part IV names which of these absences the evidence now indicts.

---

# Part III — What the V3 anchor test found

## III.1 The headline, and how to read it honestly

Over 3,456 campaigns in exploration-classic *[verified — rollups artifact, reviewer-recomputed 2026-07-13]*:

| Cost level | Grid net R | Per campaign |
|---|---|---|
| 0× (costs refunded) | **+1,345.31** | +0.39 |
| **1× (as modeled — headline)** | **−5,756.91** | **−1.6658** (95% CI −2.04 to −1.36) |
| 2× (stress) | −12,859.13 | −3.72 |

Win rate **11.28%** (390 winning campaigns). All 20 cells negative at 1×. Removing the single best campaign (BTC swing, August 2023, +114.45R) makes the total **−5,871.36** — the "strip-best" line we always print so no single lottery ticket can flatter a total. Costs sum to **≈7,102 cell-R (≈2.05R per campaign)** — the distance between the 0× and 1× rows.

Read that table as one sentence: **the signals find a small real edge (+0.39R per campaign before costs), and the execution structure then spends that edge roughly five times over in costs.** The strategy loses not because it is blind but because it pays a fortune to act on what it sees, and captures almost nothing when it is right (III.4).

Three framing rules, chartered before the run, that the numbers must be read under:

1. **This measures the mechanical ruleset only** — not Ludwig's discretionary trading (he supplies judgment the machine doesn't have), and not the signal layer alone (the 0× line shows the signals themselves carry weak positive edge).
2. **Everything here is in-sample.** Exploration-classic is the practice paper; these numbers guide design and prove nothing about the future. Validation happens later, on the lockbox and forward paper.
3. **The machinery verdict was PASS** — deterministic, gate-clean, arithmetic verified. The *strategy result* is negative; the *instrument that measured it* is sound. Those are different facts, and the second is what the study set out to establish at this gate.

## III.2 The five pre-registered hypotheses

| # | We predicted… | Verdict | What happened |
|---|---|---|---|
| H-A1 | The single best campaign carries ≥25% of a positive total | **INDETERMINATE** | Registered assuming a positive total; the total is negative, so the percentage is undefined. Registration flaw, owned. |
| H-A2 | Grade ordering A-or-better > B > C in expectancy | **PASS (partial)** | A-or-better (−1.49) beats B (−1.61); the C leg is unevaluable because C never trades *by design* — a second registration flaw, owned. Within A: A+ (−1.03, n=39) > A (−1.50) > B (−1.61) — the grading instrument orders quality correctly even inside a losing book. |
| H-A3 | ≥2 of {ETH, SOL, NEAR, ZEC} positive in their diagonal mandate | **FAIL** | Zero of four are positive in *any* mandate. |
| H-A4 | Expectancy ordering position ≥ swing ≥ intraday | **PASS** | −0.85 ≥ −1.04 ≥ −1.92. Slower mandates lose least — consistent with costs scaling against tighter, busier timeframes. |
| H-A5 | STILLBORN (died before ever reaching +0.5R) is the largest cohort | **FAIL** | PROTECTED (reached ≥+1R) is largest: 3,381 of 8,387 tranches. The system gets paid *looks* at profit far more often than predicted — it just doesn't keep any (III.4). |

Running tally across the project: 18 predictions confirmed, 6 falsified, each falsification converted to a finding. Falsification is a deliverable here, not an embarrassment.

## III.3 The forensic findings, one by one

**F1 — Exit logic *is* stop logic.** 8,365 of 8,387 exits (99.7%) were stop or stop-gap fills. Failure-X fired 12 times, opposite-cross 5, V-reversal essentially never. Whatever we conclude about exits, we are concluding about the stop. *[measured, report 1]*

**F2 — The stop-movement census, and a reconciliation found this session.** By the diary's field lens, 72% of stop exits died on a stop that never moved from entry, 8% on a stop ratcheted but still below breakeven, 20% on a stop ratcheted to breakeven-or-better. Yet economically, only **1%** of stop exits paid the full −1R; 74% were partial losses; 25% of stop exits were actually *profitable*. Report 1 flagged these two lenses as a discrepancy needing code excavation. This session resolved it, and both lenses stand: *[verified at source]*

- The 20% ratcheted-to-breakeven class plus the campaign-shared stop (later tranches inherit an already-tightened line) account for most of the profitable and shallow-loss stop exits.
- The remaining puzzle — "unmoved" stops showing a median gross loss of −0.83 rather than −1.00 — is an artifact of how gross R is computed. The risk denominator is measured from the *slipped* fill price, but "gross" adds slippage back; a trade that dies exactly on its entry stop therefore shows a gross loss slightly better than −1R, and the effect is largest where stops are tightest (the intraday mandate, 2,500 of 3,456 campaigns). No timing mystery, no bug — but it leaves a standing caveat: **gross-basis comparisons systematically flatter tight-stop configurations**, so exit-variant rankings must be run on a net basis (III.6).

**F3 — The shaken-out population.** 35% of all stop-outs (2,899) saw price resume ≥+1R in the trade's direction within 20 execution bars of the exit; the median stop-out resumes +0.23R. The forfeited continuation pool is **≈+4,429 cell-R** (capped at 10R per unit) — 77% the size of the entire grid loss. The operator ratified the shaken-out definition as-is (interview Q4). In plain terms: **one in three stops died inside ordinary noise, and the move it was positioned for then happened without it.** *[measured, report 1]*

**F4 — The harvest gap (the centerpiece).** 3,381 tranches — 40% of everything filled — reached at least +1R of open profit. The median such tranche kept **6% of its peak**. 62% kept under a quarter. **1,581 tranches (47% of the PROTECTED cohort) touched +1R and still exited at a gross loss.** The PROTECTED cohort — the trades that *worked* — is net **negative** (−649 cell-R). An oracle that exited every tranche at its peak would have made +9,225 gross versus the actual −5,757 net: **roughly fifteen thousand cell-R of excursion was touched and not kept.** *[measured, report 1]*

The mechanism is II.3's blind spot, confirmed at source this session: protection is event-driven, so a trade that runs +1R, +2R, +5R without a fresh entry signal printing is still guarded only by its original, distant stop — and when the excursion ends, price returns all the way to that line. "PROTECTED" was named for *entitlement* (the trade earned protection); the engine grants no such thing. This is Prometheus's decorative-ratchet failure in new clothing — there the gate was "+1R arms the trail"; here the gate is "the market prints another PRIME." Both gates fail the same way: **most winners never trip them.**

**F5 — The left tail: tiny stops are donations.** Median stop distances are healthy — 1.22 / 1.36 / 1.14 ATR by mandate (this **corrects the operator's working premise** that the system was running ~0.25-ATR stops; it is not, on the median). The damage is concentrated in the tail: 739 tranches (9%) carried stops **under 0.5 ATR** — cases where the fill landed barely above the signal bar's extreme — and they average **−9.16 net per unit, Σ −3,388 cell-R: 59% of the entire grid loss from 9% of the tranches.** At taker costs, risk geometry that tight cannot pay for its own execution. Notably, 47% of even these tranches touched +1R first — they weren't wrong, they were priced to die. *[measured, report 1]*

**F6 — Entries: the leak is geometry and timing, not price.** The alternate-entry shadow (entering on the ribbon cross instead of the zone reclaim) is *worse* than actual entries — fill prices are not the problem. Retracement depth is cleanly monotone: the deeper the pullback bought, the better the outcome (−0.69 per unit for the shallowest quartile → −0.18 for the deepest). Adds carry the gross edge (+0.47/unit vs the R1's +0.11) but pay ~2.4R/unit in costs. The **orphan cohort** — adds taken into a campaign whose R1 never filled — is the worst population in the study: 265 campaigns, Σ −817, **−3.08 per campaign**. And every one of the top-10 campaigns used the full three-tranche ladder. *[measured, report 1]*

A source-level caution on that last, appealing fact *[verified mechanism; interpretive]*: the add-eligibility gate (II.4) only admits adds once the stop is at breakeven-or-better for everything already held — which requires new signals to have fired, which happens in trends. Full ladders therefore don't simply *cause* winning; they are largely *selected by* the trending conditions that produce winners. "The edge lives in full ladders" is true as a description and unproven as a lever.

**F7 — Cost anatomy.** Of the ≈7,102 cell-R cost stack: fees 60–66%, slippage ~34–40%, funding ~0–1%. Median cost per unit per tranche: swing 0.47R, intraday 0.82R, position 0.27R. Fees dominate, funding is a rounding error, and the busiest mandate pays the most — intraday's 2,500 campaigns contributed −4,801 of the −5,757. *[measured, report 1; fee/slippage parameters verified against the manifest]*

## III.4 Mechanism findings made at source this session

Four things the code itself settled, beyond what the journals could show:

1. **Hypothesis H-S1 is falsified.** Report 1 hypothesized that campaign re-arms might *clear and re-place* stops non-monotonically ("de-ratcheting"), explaining the +1R-to-loss round-trips. The source refutes it three ways: the ratchet is one-way by construction; same-direction re-arms leave the in-direction stop untouched and tightening; and every clearing path is paired with a flatten, enforced by a guard that never fired across the whole run. Loosening-while-open events: **zero, by construction and empirically.** The round-trips are explained by *non-advancement* (F4's mechanism), not de-ratcheting. The scenario H-S1 feared was, in fact, the G-4 bug — found and fixed at engine 1.0.5 *before* the anchor ran. *[verified]*
2. **The C4/May-26 collision.** The orphan cohort (kill it: +817) and the post-stopout re-entry (keep it: a validated chart signature and the operator's own practice, interview Q3) **enter through the same code door.** Any orphan-kill rule must distinguish "R1 filled, then stopped, then re-entry signal" (keep) from "R1 never filled at all" (kill). Report 1 called C4 "clean"; it is not — it needs a fork, and it interacts with the add-eligibility gate. *[verified]*
3. **The add gate is a selection filter** (F6's caution) — relevant to how much of the ladder edge is causal.
4. **The gross-R slippage bias** (F2) — a measurement caveat for all upcoming shadow-exit rankings.

## III.5 The grading instrument works; the capitulation path barely exists

Two structural observations worth separating from the loss:

- **Grades order outcomes correctly** (A+ > A > B in expectancy) even inside a losing system — the quality-recognition layer is real. 310 campaigns went ungraded: 265 orphans plus **45 V-initiated campaigns**.
- **Forty-five V campaigns in 3,456 (1.3%)** is a strikingly small capitulation cohort — an order of magnitude rarer than the corresponding path in Prometheus, where capitulation entries were ~45% of trades *and owned both tail winners*. Whether v11's V thresholds filtered out the very cohort that carries the discretionary edge is an open, consequential question (Part V.4). *[verified counts; interpretation open]*

## III.6 What remains unmeasured (the recompute queue)

These require only arithmetic over the existing anchor journals — no new backtest, no new evidence spend (exploration-classic is chartered free-to-mine and its first look is already consumed):

1. **Rank the four exit shadows**: Σ(exit_XA/XB/XC/XD × size) across the grid, per mandate, **net basis** (F2 caveat). This directly answers "would a trail, or the operator's own harvest doctrine, have beaten all-or-nothing?" — the question V4 hinges on.
2. **P&L of the 45 V-initiated campaigns** — do they carry disproportionate tail profit, Prometheus-style, or are they 45 more losers?
3. **MFE-before-death distributions** by stop class × mandate × grade — the raw material for *fitting* any profit-arming threshold rather than guessing it (the Prometheus principle: distribution first, mechanism second).
4. **TPW/extension doctrine test**: using the journaled flags, how often did the operator's own banking triggers fire before the exit on trades that gave everything back?
5. **Per-direction-run shaken-out counts** (the current 2,899 is per-tranche; multi-tranche campaigns exit together, so the campaign-level count is what a re-entry rule needs).

One honest caveat rides with items 1 and 4: shadow exits are computed against the *actual* entry stream. A really-adopted exit rule would change which adds fire and when campaigns die (the shared stop drives campaign death). Shadow rankings are for **ordering candidates, not validating them**; the faithful measurement is Study S-1's instrumented replay.

---

# Part IV — The limitations of the system as-is, named plainly

**L1 — Profit earns no protection.** The stop advances only on new entry signals. This is the mechanical root of the study's largest measured leak (the ~15,000 cell-R excursion-vs-kept gap) and of PROTECTED being net-negative. *[verified mechanism + measured magnitude]*

**L2 — There is no harvest.** No take-profit, no partials, no trail on the real book. The operator's own documented exit doctrine (Playbook §7) was journaled as shadow columns and never traded. Harvest is *absent*, not deficient. *[verified]*

**L3 — No minimum stop distance.** 9% of tranches carried sub-half-ATR stops and produced 59% of the loss. The system will cheerfully accept risk geometry that cannot pay its own costs. *[measured]*

**L4 — One shared stop per campaign.** Per-tranche stop logic (wide on the R1, tight on adds, or vice versa) is architecturally impossible without redesign. This bounds what a "charter-light" V4 can do. *[verified]*

**L5 — Everything pays taker.** 5 bps/side fees plus crossing slippage, twice per tranche, ~2.05R per campaign. Fees alone are ~60–66% of a cost stack that flips the sign of the whole grid. *[verified parameters + measured shares]*

**L6 — The gross edge is thin.** Even with all costs refunded, +0.39R per campaign at an 11% hit rate is a fragile foundation: every point above amplifies or erodes it, none replaces it. Execution fixes can stop the edge being spent twice; they cannot make the edge large. *[measured]*

**L7 — The re-entry door is unguarded.** The same pathway serves the deliberate post-stopout re-entry and the destructive orphan add, with no counter, no cap, no distinction. *[verified]*

**L8 — The capitulation cohort may have been filtered away.** 1.3% V-initiation versus Prometheus's tail-carrying ~45% capitulation share. If the discretionary edge is partly a capitulation edge, v11's thresholds may have tuned it out. *[open]*

---

# Part V — The improvement menu

Everything below is an **option**, not a change. The pipeline every mechanical candidate must survive: **S-1 measurement** (an instrumented replay of exploration-classic with trading untouched, journaling richer shadow columns) → **a pre-registered named variant slot** (five exist) → **lockbox and/or forward validation**. Discretionary-tier insights can go straight to the operator's manual with no code at all.

## V.1 The candidate register, updated with everything now known

Bounds are in-sample ceilings on mined data, **not additive** (the same tranches overlap across candidates), and mix gross/net bases as noted. No sign-flip is promised by any row or any sum of rows.

| # | Rule (plain language) | Measured bound | Interview mapping | Reviewer's assessment and reasoning |
|---|---|---|---|---|
| **C1** | Refuse entries whose stop sits closer than 0.5 ATR | **+3,388 net** | Q1 endorses ATR-based systematization directly | **Strong candidate.** Largest net bound; a one-line extension of an existing rejection (`gap_through_stop`); attacks a measured, mechanically-understood pathology (F5). Costs it forfeited winners (47% of the filtered set touched +1R) and is path-dependent (removing an entry changes the campaign's stop path) — so its *realized* benefit needs S-1's replay, pre-registered as P-S3 (within ±40% of the bound). |
| **C2** | Bank half the position at +2R | +587 gross | Q2: partials are core practice | Real but modest; superseded in spirit by the richer X-B/X-C/X-D shadows already journaled. Rank those first (III.6.1). |
| **C3** | Move stop to breakeven once +1R is touched | +509 gross | Q2: ratcheting on progress is core practice | The simplest profit-arming rule. The bound looks small against F4's giant gap because breakeven protects *cost*, not *gain* — it converts the 1,581 round-trippers to ~0 instead of capturing their peaks. Its real value is as the floor of the profit-armed family (with the giveback trail and the fitted arming line above it). Beware re-touch dynamics: a breakeven stop parked inside noise re-creates F3's shakeout at a different level. S-1's path-aware measurement (P-S2) decides. |
| **C4** | No adds unless the R1 actually filled | +817 net | Q3: but re-entries after stop-outs are deliberate practice | **Needs redesign before slotting** (III.4.2): must kill only the never-filled-R1 orphan while preserving the post-stopout re-entry. The natural unified fix is Q3's own **3-strike rule** (below), which caps the pathway rather than closing it. |
| **C5** | Swing-mandate-only alternative stop buffer (volatility-frozen) | +192 gross, swing only | Q1's structure-scepticism supports EMA/ATR-only framings | Niche enrichment; keep as a swing-book line in S-1, low priority. |
| **C6** | Re-enter after a stop-out when the move resumes | pool +4,429 | Q3 defines the trigger doctrine (PO3 + reclaim) and the 3-strike cap | **Biggest pool, least-designed trigger.** The operator ranked it last on gut (V.2) — a meaningful signal about implementability. The codeable core of Q3's answer is *reclaim of the stopped level within N bars* plus the strike cap; the full "power-of-three + HTF/LTF structure" read is exactly the kind of structure detection Q1 warns against coding. S-1 measures the cheap proxy; the rich version stays discretionary. |
| **C7** | Prefer (or size up) deeper retracements | monotone table | Q5: operator's #1 gut pick | Cleanest *conditioning* evidence in the study (perfectly monotone) but the bound was never computed as a single number, and as a *filter* it trades campaign count for quality on an already thin book. Most attractive as a **sizing tilt** (risk more on deep pullbacks, less on chases) rather than a veto. S-1 should compute its bound both ways so the gut-vs-instrument comparison (V.2) is scored fairly. |

**New candidates from the interview (named a-priori, per the mapping rule):**

| # | Rule | Origin | Reviewer's reasoning |
|---|---|---|---|
| **C8 — Y×ATR initial stop family** | Stop = anchor − Y×ATR, sweeping Y and two anchors: (a) keep the structure anchor (signal-bar extreme) with a *floor* — C1's sibling; (b) pure fill-price − Y×ATR — structure-free | Q1's explicit request | The two anchors answer different philosophies: (a) keeps the Pine's structural logic and just refuses unpayable geometry; (b) is the fully-systematized form Q1 asks for. Prometheus's evidence (simplest beat hybrids; buffer regime-sensitivity — tight wins chop, wide wins trends) argues for sweeping both with at least two Y values each and *keeping both arms journaled* rather than crowning one early. Y calibration must come from the S-1 MFE/MAE distributions, not from a guess. |
| **C9 — Governor-timeframe trail** | X-A's logic but trailing the *governor* 200-EMA (e.g. the 1H e200 for multiday positions) instead of the execution e200 | Q2, verbatim ("on multiday positions I trail it on the 1H 200 EMA") | X-A on a 5m chart hugs price too closely for a multiday runner; the operator's own practice already solves this by switching reference timeframe. Not currently journaled — a genuinely new shadow family for S-1, cheap to add. |
| **C10 — Ribbon-compression exit** | Exit (or tighten hard) when the execution ribbon, after expansion, interweaves — the mechanical form of "EMAs closing down into chop" | Q2 | Codeable from data already computed (e9/e89 separation in ATRs, its slope). The microstructure judgment layered on top of it in discretionary practice ("pause or top?") stays human, per Q1's own verdict. Measure the crude version first; it may be enough. |
| **C11 — 3-strike rule** | Per direction-run, cap entry attempts at 3; after the third stop-out, stand down until the direction re-arms | Q3, verbatim | **The most elegant fix in the menu**: one counter resolves L7 — it bounds orphan bleed *and* legitimizes re-entries (C6) *and* preserves May-26 — without closing the door C4 would slam. Cheap to measure in S-1 (count what strikes 4+ cost historically). |

## V.2 Your gut against the instruments — now on the record

Per interview Q5, ranked **before** S-1 measures anything (this is itself a pre-registered prediction; we score it when S-1 reports):

| Rank | Operator's gut | Measured in-sample bound (context, not truth) |
|---|---|---|
| 1 | C7 deep-retracement preference | smallest/uncomputed bound (monotone table only) |
| 2 | C4 orphan kill | +817 net — but needs the May-26 fork (→ C11) |
| 3 | C1 min-stop gate | **+3,388 net — the largest** |
| 4 | C3 breakeven floor | +509 gross |
| 5 | C2 half-harvest at +2R | +587 gross |
| 6 | C5 swing volbuf | +192 gross (swing) |
| 7 | C6 resumption re-entry | **pool +4,429 — the largest pool** |
| — | (C8–C11 arrived after the ranking; unranked by design) | — |

The divergences are the interesting part, and neither side should be presumed right. The gut favors *entry quality and discipline* (C7, C4) over *exit surgery and re-entry* (C6 last despite the biggest pool). Two readings coexist: the instruments may be seeing money the trader's intuition discounts because he knows how hard the trigger is to define (C6's pool is real but its trigger is undesigned — his skepticism is information); or the intuition may be anchored on entry-side craft while the measured leaks (F4, F3) live on the exit side, where discretionary habit already compensates invisibly. S-1 scores this. Either outcome teaches something.

## V.3 Harvest: the operator's doctrine is already in the diary

The single luckiest fact in this study: II.6's shadow columns mean the operator's own exit doctrine (X-D: 25% at warning, 25% at extension, trail the rest) and its three simpler siblings are **already recorded for all 8,387 tranches**. Before any design debate, run III.6.1 and look. My expectation, flagged as such *[expect]*: X-A-family exits will show a large improvement over all-or-nothing on the swing/position books and an ambiguous-to-negative result on intraday (where the e200 trail's lag meets 1m-chart costs) — because that is the pattern both alternate-stop shadows already showed, and it is the pattern Prometheus's forward week showed for the identical X4 exit (trail engaged ~39% of trades, captured ~40% of peak on big movers — versus this book's 6% median capture). If the recompute contradicts that expectation, the expectation loses.

A design principle from Prometheus to hold onto when the numbers arrive: **fit the arming condition to the measured MFE distribution** (how far do winners actually run before dying?) rather than adopting +1R or the e200 because they are round. That is what recompute item III.6.3 is for.

## V.4 Prometheus deltas — what transfers, what doesn't

- **Transfers, as method:** shadow-stop journaling as the highest-leverage schema decision (already ours); size the exit's share of loss before tuning it (done — F1); distribution-first fitting; the no-behavior-change acceptance test for logging changes (identical in spirit to our pinned-stamp parity gate).
- **Transfers, as forward evidence:** Prometheus's live week is the only *forward* observation of the X-A exit in this ecosystem: engagement ~39%, capture ~40% on big movers, and its two failure cases (a lagging e200 surrendering 6R; a hard opposite-cross cutting a +14R trade) are precisely C9's and C10's motivations. A 33-trade, one-week, different-system number — a prior, not proof.
- **Does not transfer:** its base-cover/grade mechanics (v11's grade is HTF-alignment + snipe logic, a different machine — verified at source this session); its opposite-cross concerns (0.06% of Naiad exits); its "don't tighten the initial stop" caution *as stated* — Naiad's F5 shows the harm is specifically the sub-0.5-ATR tail, which C1/C8 address as a floor, not a general tightening.
- **The open question it forces (L8):** Prometheus's edge is capitulation-carried; Naiad's V fires 45 times in 4.5 years. Recompute III.6.2 is the falsification test: if those 45 carry outsized tail P&L, the **V-entry-filter variant seed** (already logged) jumps the queue and the v11-vs-v10 capitulation thresholds get compared line by line; if they are 45 more losers, the loudest Prometheus headline is formally inapplicable and a variant slot is saved. Either result is progress.
- **A standing guard for Naiad's collector:** Prometheus's forward journal saved 22 of the 53 fields its engine computed and crippled its own ability to learn. When the Naiad collector goes live (post-CD-2), **the forward schema must equal the full backtest schema, shadows included.** Two Prometheus collector-design ideas are worth adopting outright: log signals that fire while a position is already open, with their counterfactual outcomes (multiplies labeled observations per day for free — directly attacks our slow accumulation rate); and stamp a BTC market-context snapshot on every alt-asset entry (the fine-grained version of our BTC-anchored regime taxonomy).

## V.5 Execution: the limit-chase question

**What the modeled costs assume.** Every fill pays the taker fee (5 bps/side) plus crossing slippage (2/5/10 bps/side by tier) — the price of market orders. *[verified — manifest]*

**What a chase order is** (researched this session from Insilico Terminal's documentation). A **limit chase** places a passive limit order at the best bid (buying) or ask (selling) and continuously re-pegs it to follow the quote until it fills, is cancelled, or reaches a maximum adverse distance — the "Chase To" bound, e.g. 0.5% from the starting price. Variants: an unlimited chase (until fill/cancel); "stalking" at a fixed distance behind the quote; and an aggressive mode pegging to the *opposite* side of the book. The point of all of them: get filled as a **maker** — earning the passive fee rate and avoiding the crossing cost — while accepting that the fill is not guaranteed and may happen at a slightly worse price after a chase.

**The arithmetic** *(computed this session)*: Binance USDT-M maker is 2 bps vs taker 5 bps — a 60% fee cut per converted side. Fees are 60–66% of the ≈7,102 cost stack (≈4,260–4,690 cell-R), so **full maker conversion bounds at ≈2,560–2,810 cell-R saved**, before any slippage improvement (slippage is another ≈2,400–2,840). The hard ceiling on *all* execution improvement combined is the 0× line: **+1,345**. Read that ceiling honestly: perfect, free execution still leaves a thin book. **Execution repair is a complement to the stop/harvest work, not a substitute** — it stops the edge being spent twice; only the exit work can grow what's kept.

**The asymmetry that forbids assuming the savings.** A chase order can miss. It misses most when price runs away from the quote immediately — which is disproportionately the character of the entries that become the tail campaigns carrying all the profit. A naive "assume maker fees on every fill" study would bank the fee savings *and* silently keep the tail winners, some of which the chase would have missed. Missed adds also perturb the ladder (F6). The non-fill cost must be *measured against the same data*, never assumed away. Exits are even less negotiable: a stop is a guarantee, and a chased stop is not a stop — **stops stay taker in every variant**. Chase applies to entries (and possibly to non-urgent flatten exits) only.

**How to test it — a three-stage design (proposed):**

1. **Stage A — bounding table (free, journals only).** Recompute the grid at maker-fee entries/taker stops with unchanged fills — the *optimistic* bound — alongside the current all-taker line. If even the optimistic bound doesn't materially matter after the exit work, stop here.
2. **Stage B — simulated chase on 1-minute data (a pre-registered S-2 style measure-only study).** The census estate already holds full 1m history for every asset. For the 5m and 15m exec cells, 1m bars give 5–15× sub-bar resolution: simulate "place at the prior close/quote proxy, chase up to distance D, cancel after T minutes," and count a fill only when a subsequent 1m bar **trades through** the limit level (touching is not enough — we have no queue-position data, so demand strict penetration; this biases the simulation *against* the chase, the honest direction). Unfilled entries either lapse (missed trade) or convert to taker at market — test both policies. Pre-register the fill model and run a **sensitivity sweep** over its assumptions; report the grid at the pessimistic and optimistic corners, not a point estimate. Honest limits: the 1m-exec intraday cells have no finer data (bound-only there), and no kline-level simulation sees the order book — Stage B ranks and bounds, it does not prove.
3. **Stage C — live paper measurement.** The final arbiter is the Naiad collector placing real (paper) chase orders and recording actual fill/miss/chase-distance outcomes. This slots naturally into the Phase-2 protocol after CD-2 and is the only stage that produces evidence rather than modeling.

**On the dynamic distance** (the operator's suggestion — endorsed, with reasoning): a fixed percentage cannot be right across BTC and JTO, or across a quiet Sunday and a CPI print; the system already denominates every other distance in ATR, and the chase bound should speak the same language. Candidate parameterization for Stage B: **D = k × ATR(1m)** with k ∈ {0.05, 0.1, 0.25} and a per-tier floor in ticks; timeout T ∈ {1, 3, 5} minutes. The sweep says which corner of that box matters; there is no need to pick today.

## V.6 The V4 fork

The operator's stated lean (interview Q6): **same signal brain, rebuilt stop/risk shell, plus a real harvest** — the "charter-light" path — with the final call deferred until after this report and the recomputes. The evidence pattern, for and against, as the reviewer reads it:

**For the lean:** the 0× line says the brain finds real (if thin) edge; the grading instrument orders quality correctly; every mechanically-diagnosed pathology in Part IV lives in the shell (stop geometry, protection engagement, harvest absence, execution costs, the unguarded door) — and every one has a named candidate with a measured bound. The architecture constraint (L4: one shared stop) is compatible with a shell rebuild that keeps campaign-level stops but adds profit-arming, a floor, a harvest overlay, and the 3-strike counter.

**The two open items that could enlarge the scope:** the capitulation question (III.6.2 — if the V cohort is where the tail lives, the signal layer *is* on the table after all, via the already-logged V-entry-filter seed); and the intraday mandate (−1.92/campaign at 2.05R costs may be unrescuable by any shell at taker economics — a mandate-retirement decision, which is portfolio design, not code).

**A prioritization reality:** variant seeds now well exceed the five chartered slots (zoneMemory-5, provisional-Z1-only, zone-gated CONFIRM adds, V-entry-filter, one-add-per-bar dedupe, plus C1–C11's survivors). S-1's job is to shrink that list with measurements; the operator's job at V4 design is to spend the five slots. Nothing in this report pre-spends one.

---

# Part VI — What happens next

**Awaiting the operator's word (one-line vetoes suffice):**

1. **Ratify the P-S1 reframe.** Old P-S1 predicted de-ratchet events explain the round-trips; the source falsified the mechanism before S-1 runs. Proposed split — **P-S1a:** de-ratchet (loosening-while-open) events = 0 (S-1 confirms empirically); **P-S1b:** non-advancement (≥+1R MFE with zero ratchet steps during the excursion) explains ≥⅓ of +1R-to-loss round-trips. P-S2 (path-aware BE/giveback beats static bounds) and P-S3 (C1 realized within ±40% of +3,388) stand as registered.
2. **Approve the recompute go-paste** (III.6 items 1–5; journals-only, zero new evidence spend) — the X-A…X-D ranking and the V-cohort P&L gate both the harvest design and the capitulation question.
3. **Approve the S-1 contract update** to fold in the interview families: C8 both-anchor ATR sweep, C9 governor-TF trail, C10 ribbon compression, C11 3-strike counter, C6-proxy (stopped-level reclaim within N bars), the §7-harvest family — with the semantics pins reduced by the two closed this session (exit-row stop field: settled, it is the fill level; H-S1 monotonicity: settled at source).
4. **Decide the fee-study Stage A** (free) and whether Stage B gets scoped now or after the exit recomputes.

**Standing queue, unchanged:** CD-2 (collector egress — VPS lean) → collector go-live with the full-schema guard (V.4) → Phase-2 protocol; engine 1.0.8 (G-1 lockbox guard + J-1) at next engine touch; G-2 LIT estate remediation; Pine backlog B-1/B-2.

**The one-paragraph takeaway.** The instrument is sound, the test was honest, and the result is a clear diagnosis rather than a verdict on the method: the mechanical v11 ruleset finds a thin real edge, prices its risk with no floor, never protects its profits unless the market volunteers a signal, harvests nothing, and pays taker rates twice per tranche — and each clause of that sentence now has a measured size, a mechanical explanation verified in source, and at least one named, testable candidate fix. What stands between here and V4 is not more theory; it is the recompute queue, S-1's measurements, and the operator's five slots.

---

## Appendix — Plain-language glossary

**R** — one unit of planned risk: the dollars lost if a trade dies exactly at its initial stop (here, 0.5% of the cell's equity). All results are quoted in R so different account sizes and assets compare fairly. · **cell-R** — R summed at the tranche-size weighting of a grid cell. · **ATR** — Average True Range; the market's typical per-bar travel, used as a volatility yardstick. · **EMA** — exponential moving average; a smoothed price line weighting recent bars more. · **Governor / execution timeframe** — the slow chart that sets direction / the fast chart that times fills. · **Campaign** — one armed directional episode; **tranche** — one filled entry within it (R1 = first, adds = later). · **Mandate** — a governor/execution pairing (swing 4H/5m, intraday 1H/1m, position 12H/15m). · **MFE / MAE** — the best / worst a trade looked while open, in R. · **Expectancy** — average result per campaign. · **95% CI (bootstrap)** — the range the average would plausibly land in if the same campaigns were re-drawn thousands of times; a width gauge, not a guarantee. · **Win rate** — share of campaigns ending positive. · **Strip-best** — the same total with the single best campaign removed; an anti-lottery-ticket disclosure. · **0× / 1× / 2×** — results with costs refunded / as modeled / doubled. · **Maker / taker** — passive limit orders that rest on the book pay the lower *maker* fee; orders demanding instant execution pay the higher *taker* fee plus crossing slippage. · **Shadow / counterfactual** — a rule the engine *records* the result of without trading it. · **Oracle** — a hindsight-perfect bound (e.g. exiting every trade at its exact peak); a ceiling for context, never a target. · **In-sample** — measured on data that was allowed to influence design; flattering by construction. · **Lockbox** — the sealed data partition, opened once, at a pre-registered bar. · **Named variant slot** — one of five chartered chances to test a rule change against the lockbox. · **Determinism** — same inputs, byte-identical outputs; proven by running everything twice. · **Taxonomy cohorts** — NEVER_GREEN (never showed profit), STILLBORN (peaked below +0.5R), FADED (+0.5 to +1R), PROTECTED (reached ≥+1R — an entitlement label, not an outcome).

*Prepared by the reviewer under Fable-mode, 2026-07-14. Every mechanism claim in Part II–III.4 was read from engine source this session; every V3 number restates the reviewer-recomputed record of 2026-07-13; execution research cites Insilico Terminal documentation and the Binance fee schedule as of 2026-07. Nothing in this document changes any rule; Part V is a menu, and the kitchen is the operator's.*
