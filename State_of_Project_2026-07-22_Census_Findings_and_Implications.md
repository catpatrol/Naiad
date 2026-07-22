# State of the Project — 2026-07-22
## What the census found, what it means, and how it reshapes the redesign — in plain language, from the ground up

**Author:** reviewer (Claude, Fable-mode). **Audience:** the operator, and any future reader with no prior context. **Provenance note:** every number here was recomputed from the raw census output file (`census_results.json`) before being trusted; where a headline from the run summary was softened or changed by that scrutiny, I say so explicitly. Nothing is taken on faith, including the builder's own summary.

---

# Part 0 — For a reader starting completely cold

This project is trying to turn a human trader's method into a set of mechanical rules a computer can run — and, having discovered the first mechanical version loses money, to redesign it into one that doesn't. We are deep into the *diagnosis* phase: figuring out precisely *why* it loses, so the redesign fixes causes rather than symptoms.

A few plain definitions you'll need:

- A **trade** is opened ("entry"), and closed either by a **stop-loss** (a price at which we admit the idea was wrong and get out) or by some exit rule. While it's open, it moves for us and against us; the furthest it gets **in our favor** is its **MFE** (maximum favorable excursion), and the furthest **against us** is its **MAE** (maximum adverse excursion).
- Everything is measured in **R** — one R is the amount of money we planned to risk on the trade (0.5% of the account). A trade that makes twice what we risked is "+2R"; one stopped out for a full loss is "−1R."
- Costs matter enormously. Every round trip (in and out) pays a **toll** — fees plus slippage — of roughly 14 to 30 **basis points** (a basis point is one hundredth of one percent of the price). The single most important idea in this whole project is that **how much the toll costs you, measured in R, equals the toll in basis points divided by your stop distance in basis points.** Put a stop too close, and the toll alone can eat the trade.
- The method reads several **moving averages** (smoothed price lines: a fast 9-period, a medium 89-period, a slow 200-period) across several **timeframes** (5-minute up to 1-day charts). When these lines cross, or when price crosses them, those are the **signals**. One timeframe is designated the **governor** — it sets the overall direction; the others refine timing.

That's the whole vocabulary. Now the state of things.

---

# Part 1 — Where the project stood *before* the census

Six phases of measurement had established a clear picture:

**The disease is on the entry side, not the management side.** The biggest experiment so far (called TC-1) ran the whole system four times over, testing a **wider, smarter stop-loss** — one placed just beyond a real swing high or low on the 1-hour chart, instead of a fixed tiny distance from entry. This "structural stop" was a massive improvement: it took the grid-wide result from −1,797 R to −351 R, made the medium-term "swing" style actually profitable, and roughly *quadrupled* the raw edge per trade. But — and this is the finding that set up everything since — **the improved version took *more* trades than the original and still lost money overall.** That single fact proved the operator's long-held intuition with a number: the problem is not that we manage trades badly; it's that we take **too many marginal trades**, and their accumulated tolls drown the good ones.

**The "add to a winner" mechanism is broken by a circular dependency.** The method's most powerful idea — and the operator's strongest edge in his own discretionary trading — is to *add* to a position that's working, building size while keeping risk flat (a "pyramid"). But in the mechanical version this was nearly impossible, and the operator diagnosed exactly why: the rule that permits an add requires the stop to have moved up to break-even first; the stop only moves up when a fresh entry signal fires; and a fresh entry signal requires price to pull *back* — which a strong, running trend simply doesn't do. So the gate that lets you add is frozen shut in exactly the trending conditions where adding is most valuable. The serpent eats its tail. A follow-up phase (S-3) **measured this precisely: at 97.59% of the moments a trade was winning by at least +1R, no add signal was available.** The circular freeze is near-total, and it is the single clearest thing the redesign must fix.

**The confluence value is real but was hiding.** "Confluence" means several independent conditions agreeing — for instance, multiple timeframes all pointing the same way. Earlier analysis had concluded that confluence conditions couldn't separate good trades from bad. But S-3 showed something important: those same conditions, re-measured on the *winning* (structural-stop) book, **flip positive** — and the strongest ones live in the **slow timeframes** (12-hour and 1-day). The earlier pessimism was an artifact of measuring on a book whose bad exits destroyed everything. Fix the exits, and the confluence signal reappears.

**Two guardrails were locked in.** Entries are now floored at the **5-minute chart** — nothing faster — because a separate phase proved that on the 1-minute chart the average trade's best move can't even cover its own toll, while at 5-minute it can. And no early-harvest trailing exits on a wide-stop system, because they clip the winners the wide stop is meant to let run.

So the redesign's mandate, going into the census, was: keep the structural stop, ban the unpayable timeframe, **fix the frozen add gate**, and figure out whether multi-timeframe confluence can throttle the flood of marginal entries. The census was built to answer the last two.

---

# Part 2 — What the census actually was

The census is different from everything before it: it **doesn't trade at all.** Previous phases ran the trading engine and measured the trades. The census instead walks through all the history and simply **records every signal on every timeframe** — every crossing of the moving averages — as a raw timeline, completely independent of any trading decision. Then it measures **what price did next** after each signal: how far it ran in each direction, over several time horizons.

Why build it this way? Because the goal was to **question the engine's oldest assumptions without the engine's blinders.** If you only look at the moments the current system chose to trade, you can never discover that a *different* governor timeframe, or a *different* entry rule, would have been better — you only ever see what the current rules let you see. By recording the entire signal landscape independent of trading, the census can ask: is the 4-hour governor even the right choice? Is a single crossing the right trigger, or should several timeframes have to agree? And, crucially, **what signal fires at those frozen winning moments** — the one that could become a new, pullback-free way to add to a winner?

Specifics of what it captured:
- **Three types of crossing**, on **seven timeframes** each: the fast-crosses-medium (9/89, the "regime" signal), the medium-crosses-slow (89/200, the "stage" signal), and — **new for this census** — the fast-crosses-slow (9/200, a "momentum-vs-trend" signal the operator asked to add and observe).
- **Forward outcomes** measured in *both* basis points and ATR (ATR = the market's typical bar-to-bar move, used as a volatility yardstick), over short/medium/long horizons and a special "regime-scale" horizon that runs until the governor flips direction — because we learned the winning book makes its money by *riding trends until the regime breaks*, so that's the horizon that matches how profit is actually made.
- **Four candidate governors compared** — 1-hour, 4-hour, 12-hour, 1-day — analyzed as four different "lenses" over the same data. This was deliberate: the operator's **fractal principle** holds that price structure repeats across timeframes, so different trading styles may each want their *own* governor. The census produces a **map** of which timeframe governs best for which horizon, not a single winner.
- Three operator-requested additions: a **cascade-ladder** analysis (does the natural time-sequence of crossings up the timeframes — 5-minute fires, then 15-minute, then 1-hour — constitute a ready-made schedule for entering and then adding?); a **factor-scoring** analysis (instead of requiring one perfect setup that ticks every box, score how many of several "confluence factors" are present and trade when *enough* are — a more flexible, less dogmatic framework); and a **pullback-landing** study answering the operator's specific question, in his capitals: *do pullbacks have a habit of landing on an EMA-related zone?* — with a rigorous "matched null" (comparing against random points, because with 21 moving-average lines on the chart, everything is near *some* line, so only clustering **beyond chance** counts).

The census ran with strict **anti-fishing discipline**: only six specific predictions were registered in advance as the things that would count as findings; everything else it turned up was quarantined as a "hypothesis for a later test," and no pattern was even flagged worth-pursuing unless it repeated across at least two timeframes. This matters because a search across three crossings times seven timeframes times many combinations *will* produce chance patterns if you let it; the discipline is what separates signal from noise.

---

# Part 3 — What the census found (after the reviewer's scrutiny)

The run reported PASS with 7 of 9 predictions confirmed. But the reviewer's job is to recompute before believing, and reading the raw output changed what several of those "confirmations" actually mean. Here is the honest picture, organized by what survived and what didn't.

## 3.1 The two findings that are solid — they survived their own null tests

**Pullbacks really do land on moving-average zones, at about twice the random rate, on every timeframe.** This is the operator's capitalized question, answered clearly: **yes.** When price pulls back and forms a bottom (during an uptrend), that bottom sits within a narrow band (0.35 ATR) of a governor moving average about **twice as often as a random point would** — and this held on all four candidate governors (ratios 1.90 to 2.02), on samples as large as 10,576 pullbacks against 105,760 random comparison points. That it holds *identically across every timeframe* is exactly the fractal signature the operator predicted. **The zone doctrine's foundation is confirmed from outside the trading system.** This is the single most robust thing the census produced.

**The "trend-age clock" is real and usable.** After the fast line crosses the medium line (a regime change), the fast line later crosses the slow line (the 9/200) — and the *time between* those two events forms a well-shaped distribution: a quarter of the time it happens within 10 timeframe-bars, half the time within 52, three-quarters within 150. This gives the redesign a way to estimate *how mature a trend is* — which matters for deciding when to enter versus when a move is already late. The operator's reading of the new 9/200 cross as a **mid-sequence marker** (it reliably falls between the other two crossings in a developing move) was assigned by the data, not assumed — the canonical order (9/89, then 9/200, then 89/200) held in 97.1% of chains.

## 3.2 The finding that was reported as confirmed but is really an artifact — and it matters most for the redesign

The census reported that all three crossing types show "positive forward moves" and used this to rank potential signals. **The reviewer found this is largely a measurement artifact, not a real ranking**, and the reason is worth understanding because it changes the next step.

Every forward move was measured over a **fixed window of exec-chart bars** (100 bars of the 5-minute chart, about 8 hours) but expressed in **each timeframe's own ATR.** A 1-day timeframe's ATR is huge; a 5-minute timeframe's ATR is tiny. So the same 8-hour window, divided by an ever-larger yardstick, *mechanically* produces a shrinking number as you go up the timeframes — 5-minute reads ~4.5, 15-minute ~2.4, 1-hour ~1.2, 1-day ~0.2 — regardless of whether the signal carries any real information. The proof it's an artifact: the three *different* crossing types produce **nearly identical numbers at every single timeframe** (at 5-minute, 4.56 versus 4.48; at 4-hour, 0.66 versus 0.58). If the crossing type mattered, they'd differ. They don't. **The yardstick is carrying all the apparent signal; the signal itself carries almost none.**

The consequence: **we cannot yet rank which signal would make the best "add to a winner" trigger** — the whole point of that part of the census — because the ranking as delivered is an accident of units. The fix is straightforward and cheap: re-rank everything in **basis points, net of the toll** (the units that actually determine whether a trade pays), which the raw data already contains. That re-scoring is the immediate next phase, **CENSUS-1b**.

## 3.3 The cascade-ladder: a possible *schedule*, but not an *edge*

The operator's hypothesis was elegant: maybe the natural sequence of crossings up the timeframes *is* the entry-and-add plan — 5-minute crossing enters, 30-minute crossing adds, 1-hour crossing adds again. The census measured the move *remaining* after each rung of that ladder. The result: the remaining favorable move and remaining adverse move at each rung are **almost exactly equal** (ratios ~0.98 to 1.01) — symmetric noise. So the ladder **survives as a possible *timing* structure** (the crossings do fire in an orderly sequence, and the lags are real: the 15-minute follow-on comes about 11 hours after the 5-minute, the slow ones days later) **but not as a source of *edge*** at this horizon — pending the same bps re-score, which might reveal a toll-space edge the ATR view hid.

## 3.4 Slow-timeframe agreement: falsified as one thing, confirmed as another — the key reconciliation

This is the subtlest and most useful result. The census **falsified** the idea that requiring the slow timeframes (12-hour and 1-day) to agree makes trades reach *further* — the lift to peak excursion was tiny (+0.13 ATR, and the statistical confidence interval spans zero), and the condition is true 43% of the time anyway (common, not selective). **Yet S-3 had shown these same slow-agreement conditions flipping the *realized outcome* positive on the winning book.** Both are true, and together they resolve into a precise statement: **slow-timeframe agreement doesn't predict how far price *can* go — it predicts how *long the ride lasts* before the regime break that the winning book cashes in on.** It is a **survival-and-holding variable, not an entry-size variable.** That tells the redesign exactly where to use it: as a condition for *staying in and adding*, not for sizing the initial entry.

## 3.5 The confluence-factor scoring: the framework is sound, but this factor list is redundant

The operator's flexible-entry idea — trade when *enough* factors are present, rather than demanding a perfect setup — was tested as a "dose-response curve": does the forward move increase as more factors line up? The curve came out **monotone but nearly flat** (it rises with factor count, but barely). The reviewer found why: the nine factors chosen are **collinear** — they mostly all say "the trend is on" at the same time, so there's little independent variation for the analysis to work with (the distribution of factor-counts is bimodal — trades tend to have either very few or very many factors true, rarely a spread). **The framework isn't disproven; this particular factor list is too redundant to give it a fair test.** CENSUS-1b will decorrelate the factor list so the idea gets a proper trial.

## 3.6 The pullback-outcome edge: mechanism proven, edge unproven (underpowered)

The zone-landing study had two halves. The first — do pullbacks cluster on EMAs? — is solidly **yes** (Part 3.1). The second — do the pullbacks that land *on* an EMA lead to *bigger subsequent moves* than those that don't? — came back "confirmed" in the summary, but the reviewer found **every confidence interval spans zero**: the point estimates lean positive (12-hour +0.60, 1-day +0.43) but the samples are thin (215 and 103 events) and the result is not statistically distinguishable from no-effect. So: **the landing mechanism is real; whether it confers an outcome edge is genuinely unknown**, limited by sample size, not disproven. CENSUS-1b will pool the timeframes to give this a powered test.

## 3.7 The one lesson that towers over the rest

Step back from the individual results and a single pattern dominates: **everywhere the census looked with only light conditioning — across governor timeframes, across ladder rungs, across factor counts — the gross forward move was nearly symmetric** (it went about as far against you as for you). In plain terms: **the combinatorics of entry signals do not, by themselves, tilt which way price goes.** This is a profound and disciplining finding. It says the edge this project has actually measured does **not** live in cleverer entry signals. It lives in three specific places: **exit asymmetry** (the structural stop caps losses while letting winners ride to the regime break), **toll-space scaling** (slower excursions clear a fixed basis-point toll that faster ones can't — the reason for the 5-minute floor), and **location-specific structure** (the EMA-terminus mechanism — pullbacks landing on zones). The census's greatest service was **telling the redesign where *not* to dig**: not in entry-signal combinatorics.

---

# Part 4 — How this reshapes the design guidelines we set yesterday

Yesterday's session set out to question the current engine and gather the correlations we might have missed. The census did that, and it moves several of yesterday's guidelines from *hypothesis* to *evidence-backed* — and corrects one or two.

**Guideline: "Fix the frozen add gate with a decoupled, non-pullback trigger."** *Reinforced, but the specific trigger is not yet chosen.* The census confirmed the freeze (via S-3's 97.59%) and set out to find the replacement signal — but the units artifact means the *ranking* of candidate triggers has to wait for CENSUS-1b's basis-point re-score. So the direction is firmer than ever; the specific mechanism is one short phase away. **What we can already say:** the trigger should be evaluated in basis points net of toll, not ATR, and the cascade sequence is a candidate *timing* structure even if not an edge on its own.

**Guideline: "Multi-timeframe confluence is the entry-quality throttle we've been missing."** *Refined in an important way.* The census showed confluence does **not** work as an *entry-magnitude* filter (it doesn't make trades reach further). It works as a **survival/holding filter** — slow-timeframe agreement predicts how long a trend lasts, which is what the winning book monetizes. So confluence belongs in the redesign as a **stay-in-and-add gate**, not an entry-sizing gate. This is a genuine correction to yesterday's framing, and it's exactly the kind of thing gathering the data was meant to reveal.

**Guideline: "The fractal principle should inform the system — different mandates may want different governors."** *Strongly supported.* The zone-landing mechanism holding *identically across all four candidate timeframes* is direct fractal evidence. The governor question now has a **map** rather than a single answer, and the redesign can legitimately assign intraday, swing, and position their own governors from that map. (One caveat: the "which governor is best" comparison was partly confounded by the same units issue — a slower governor mechanically buys a longer ride — so CENSUS-1b's basis-point view will sharpen the map.)

**Guideline: "The sniper-pocket entry is a cornerstone."** *Downgraded, but not eliminated — and the reviewer corrected himself here.* S-3 had found the pocket unremarkable at full sample, and the reviewer initially called it "dead." That was too strong, and it's corrected on the record: the honest statement is *unsupported as a standalone entry gate on the measured data, retained as a candidate confluence factor, with the operator's discretionary experience explicitly weighted as evidence of a different kind.* Critically, the census's zone-landing finding **resurrects the pocket's underlying mechanism** — pullbacks *do* land on structure at 2× chance — from *outside* the trading system. So the *idea* behind the pocket is vindicated even though the *specific grade* wasn't; the redesign can carry the mechanism (pullback-to-zone) as a factor without carrying the exact old definition.

**Guideline: "Keep the structural stop; no early-harvest exits."** *Untouched and reinforced.* The census's symmetry finding — that entry combinatorics don't tilt price — makes the exit-asymmetry of the structural stop the more clearly the real engine of edge. Nothing here challenges it.

**Guideline: "Gather data with an open mind; don't pre-condition the read."** *Honored, and it paid off.* The two things that survived (zone-landing, the maturation clock) were not the things the reviewer would have bet hardest on; the elegant hypotheses (the cascade-as-add-ladder, slow-stack as an entry filter) were the ones that fell or transformed. The open-minded census corrected the reviewer's priors in several places — which is precisely what it was for.

---

# Part 5 — The concrete path forward

**Immediately:** a small repository-hygiene commit is being finalized (making the repo's own history complete and auditable), then the census results get pushed. This is housekeeping, not analysis.

**Next phase — CENSUS-1b (a few minutes of compute):** re-score the census's trigger candidates and cascade rungs in **basis points net of toll** (fixing the units artifact and producing the honest ranking of decoupled-add candidates); pair the confluence-combination result with its downside (MAE) so we know if it's actually tradeable; run a **powered** test of the pullback-outcome edge by pooling timeframes; and **decorrelate the confluence-factor list** so the operator's flexible-entry framework gets a fair trial. This turns the census from "observed" into a decision-grade specification.

**Then — the first v12 logic candidate (a pre-registered rule change):** built from the two findings that survived their nulls. In plain terms, the redesign's first concrete shape is: **enter (and re-enter) on pullbacks that land on a slow-timeframe moving-average zone, while inside a trend-age window that says the move isn't over yet, protected by a structural stop, and held until the regime breaks — adding to the position via a decoupled trigger (chosen in CENSUS-1b) rather than the frozen pullback gate.** Every piece of that sentence is now backed by a measured finding rather than an inherited assumption.

**The through-line for the operator:** the project has moved from "the system loses money and we don't know why" to a precise, evidence-backed diagnosis — *too many marginal entries, a frozen add mechanism, and an edge that lives in exits and structure rather than entry signals* — and to a redesign whose every component is now traceable to a measurement. The census's job was to tell us where the edge is and is not; it did, and it disciplined the redesign by ruling out the tempting-but-empty direction (cleverer entry combinatorics) while confirming the two mechanisms worth building on (structure-landing and regime-scale holding).

---

*Prepared by the reviewer under Fable-mode, 2026-07-22. Every claim traces to a recomputed number in the census output or a prior verified phase; every place the run summary was softened by scrutiny is marked. The companion handoff document carries the operational state for continuing the work.*
