# Stop-Loss Logic: What Prometheus Learned
## The SSv10 ratchet failure, the committed trail, and transferable exit-design conclusions

*Companion to "Bootstrapping an Autonomous Trading Agent with Claude." That document transfers the
research process; this one transfers everything the project learned about one component — the stop
and trailing-exit logic — because it is the component where the original strategy was most wrong,
where the falsification was cleanest, and where the design patterns generalize most directly to any
next agent.*

*Provenance, stated up front: sections marked **[record]** come from the committed project record
(the Phase 3/3b/4b findings in the handoff brief and build prompts). Sections marked **[verified]**
were recomputed by Claude Fable directly from the raw Phase-5 trade journals (~110k trades) and the
forward/paper journals in the current session. Sections marked **[analysis]** are Fable's present
reasoning — hypotheses for the next agent, not established findings. Nothing below is
reconstructed from memory alone.*

---

## 1. The starting point: SSv10's native stop logic, and how it failed

The strategy as ported ("SS v10") shipped with an exit stack later designated **X0: an R1-armed
ratchet plus aging**. Its logic: the initial stop stands until the trade reaches +1R of open
profit; at that point the ratchet "arms" and begins stepping the stop up behind price at discrete
R-levels, never loosening; an aging rule times out stale trades. This is a very common retail
design — protect first, then lock in profit in fixed risk-unit increments once the trade has
"earned it."

**Phase 3 falsified it outright. [record]** Racing four entry arms over the study window with
identical exits exposed the exit stack itself:

- The system **located 25–113 R of favorable excursion and captured approximately none of it.**
- **Capture ratios ran −0.05 to −0.43** — trades were achieving positive maximum favorable
  excursion (MFE) and still finishing *negative*. The exit machinery was not merely leaving money
  on the table; it was converting winners-in-progress into losers.
- The mechanism of death: **51 of 77 trades died before the R1-armed ratchet ever engaged.** The
  arming threshold (+1R) sat *above where the strategy's trades actually live*. For two-thirds of
  all trades, the sophisticated ratchet was decorative — the trade ran on its wide initial stop
  alone until it was stopped out or aged out.

This is the single most transferable finding in the project, so it deserves restating as a
principle: **a harvest mechanism gated behind a threshold is worthless if the threshold exceeds
the typical excursion of the entry set it serves.** SSv10's ratchet was designed in money-space
(R-levels) without ever checking the MFE distribution of the trades it would manage. When the
distribution was finally measured, most trades never got within reach of the arming line.

The correct order of operations — the one the next agent should follow from day one — is the
reverse: **measure the MFE/MAE distribution of the entry set first, then design the exit to fit
it.** Two diagnostics should be standard columns in every exit report from the first backtest:
the **capture ratio** (realized R divided by MFE — how much of what the trade offered did the
exit take?) and the **pre-engagement death share** (what fraction of trades died before the
harvest mechanism ever activated?). X0 would have failed both at a glance, months earlier.

---

## 2. The horse race, and the architecture that won

Phase 3b raced six exit stacks over *frozen* entry sets on two contrasting windows (a crash window
and a non-crash window) — the methodology itself is a keeper: **exits varied as a family over
frozen entries, one mechanism axis per variant, with the incumbent as control. [record]**

The field: **X0** (the SSv10 R1-armed ratchet + aging, as control) · **X1** (same ratchet but
armed from entry, removing the +1R gate) · **X2** (breakeven-at-1R plus profit lock) · **X3/X4**
(a trail that follows the 200-period EMA with a 0.25× / 0.50×ATR buffer respectively, with an
engagement guard) · **X5** (trail plus breakeven lock).

The result was decisive: **the e200 structure trail won on both regimes.** On the crash window,
the E-gated entry set went from **−2.55 (X0) to +33.62 (X3) / +29.77 (X4)**; on the non-crash
window from **+8.18 to +26.37 / +26.94.** X4 was committed as the default by a marginal
commit-rule win, with X3 carried permanently as the reported alternative — both run in every
batch. **[record]**

Notice what *lost*: every variant that kept discrete R-level mechanics. Arming the ratchet from
entry (X1) didn't save it; breakeven locks (X2) didn't; even bolting a breakeven lock onto the
winning trail (X5) made it worse. The project's Phase-3 lesson — **mechanism subtraction beat
mechanism addition** — showed up here as clearly as anywhere: the winning exit was the *simplest*
one raced, and hybridizing it degraded it. **[record]**

**Anatomy of the committed stop logic** (the design worth carrying forward whole): **[record]**

1. **Initial structural stop, anchored to the trigger bar's extreme** (patch P1) — not the
   confirm bar's. The stop belongs to the structure that generated the signal, not to where the
   fill happened to land.
2. **Engagement guard:** the trail is *eligible only once a closed bar sits on the trade's side
   of the e200*. Until then, the initial structural stop stands untouched. This is a two-phase
   stop lifecycle — a **survival phase** governed by structure, then a **harvest phase** governed
   by the trail — and it is the architectural answer to X0's failure: instead of an arbitrary
   money-space arming line most trades never reach, engagement is defined by the same structural
   event the strategy itself trades on.
3. **The trail:** stop follows the e200 offset by an ATR buffer (0.50× for X4, 0.25× for X3),
   updated on closed bars only.
4. **The ratchet invariant: stops never loosen.** One-way, enforced as a hard system invariant
   with fixtures, in every phase.
5. **Operationally: stop-guarantee-and-repair is the first action of every wake.** Before the
   agent does anything else on a tick, it verifies the working stop exists and is correct, and
   repairs it if not. In any live descendant this ordering is non-negotiable.

---

## 3. What the data says about the committed trail — verified observations

These are the facts Fable recomputed from the raw journals this session, and what they imply for
exit logic specifically. **[verified]**

**The exit is now the minority owner of the loss — by 2.5×.** Phase 4b's cohort accounting
(every trade partitioned by MFE: NEVER_GREEN ≤0 · STILLBORN <0.5R · FADED 0.5–1R · PROTECTED
≥1R) put entry-attributable loss at **−4,164 R** versus exit-addressable (FADED) at **−1,679 R**.
**[record]** That ratio is why the project deprioritized further exit tuning in favor of entry
quality — and the discipline generalizes: **quantify each component's share of the loss before
spending effort on it.** An exit that owns ~17% of the problem caps what even a perfect exit
redesign can recover.

**The FADED share is astonishingly stable — ~17% everywhere.** Across both exit stacks, both
entry sets, and both depth cuts (76-month and 12-month), the share of trades that reach 0.5–1R
and then die stays in a band of roughly 16.9–17.5%. **[verified]** Two readings, both useful:
first, the trail's mid-trade give-back behaves like a **fixed tax, independent of entry
quality** — evidence that exits and entries are genuinely decoupled in this system (the same
cohort-mix invariance held across regimes in 4b **[record]**). That decoupling is what makes it
legitimate to tune the two independently. Second, it means the committed trail has a
**structural residual it cannot reduce from inside its own logic** — whatever fixes FADED, it
won't be a buffer tweak.

**For half the trades, the exit logic never matters at all.** Under E-gated + X4 the *median*
trade R is exactly **−1.000** — a full initial-stop-out. **[verified]** The engagement guard
means those trades die in the survival phase; the trail never touches them. Under E-birth the
median loser shrinks to −0.50, telling us the birth-anchored structural stops interact very
differently with the same trail. The implication is sharp: **in a low-hit system, initial stop
placement dominates trailing logic in loss-side importance** — which is exactly why the project's
own next-lever note points at "tighten the birth structural stop" as the first
mechanism-justified variant for the paper-data era, not another trail variant. **[record]**

**Buffer width is regime-sensitive, and the commit margin was thin.** X3 (tight buffer) beat X4
on the crash window (+33.62 vs +29.77) and lost narrowly on the non-crash window; X4 won the
commit rule marginally. **[record]** Then in the one virgin forward window — ranging tape — the
tight buffer again bled meaningfully less (E-birth: −2.84 vs −5.49; E-gated: −19.38 vs −29.97).
**[verified]** Pattern across three independent looks: **the wide buffer earns its keep only in
sustained trends; in crashes and chop the tight buffer dominates.** The honest response is not to
retro-tune a regime-switching buffer (that would spend data); it is what Prometheus already does —
**keep both arms running in every batch forever**, so the comparison accrues on virgin data for
free, and any future regime-conditional buffer rule can be set a priori and validated forward.

**The tail is everything, so the trail's prime directive is: don't choke it.** The system's
profile is ~18–22% hit with payoff ~4–5; in the live paper run, **one trade (+8.75R) out of 31
carried the entire result** — remove it and the other thirty net −9.3R. **[verified]** A trailing
stop for this distribution must be evaluated *asymmetrically*: an exit change that trims
give-back but clips even a small fraction of the right tail is a net destroyer. Any exit metric
suite for a tail-carried system needs a **tail-capture line** (of trades whose MFE exceeded, say,
5R, what share was realized above 3R?) sitting *above* the give-back line in priority.

---

## 4. Residual shortcomings and open questions on the committed trail

These are the known soft spots to probe with paper data — some from the record, some flagged now
as hypotheses. Each is phrased so the journal can answer it.

**The never-loosen invariant interacts badly with volatility expansion — in the regime that
matters most. [analysis]** The buffer is an ATR multiple evaluated as the trail ratchets. If
volatility expands *after* a ratchet step, the stop is now effectively tighter in
volatility-units and, by invariant, cannot widen. The system's entire raw edge concentrated in
the high-volatility regime (~93% of the 76-month total **[record]**), which is precisely where
expansion mid-trade is common — so the trail may systematically shake out tail trades early in
the best regime. This is measurable offline from the journaled candidate stops and MFE paths:
*of PROTECTED trades exited by the trail, how often did the exit bar's ATR exceed the
ratchet-time ATR, and what did post-exit continuation do?* The invariant itself should stay —
one-way stops are load-bearing for risk — but a vol-aware buffer *set at engagement time* (rather
than per-ratchet) is a legitimate a-priori variant to test forward.

**Some FADED deaths may be pre-engagement round-trips. [analysis]** A fast move to 0.5–1R that
reverses before any closed bar settles beyond the e200 dies on the initial stop with the trail
never engaged — counted as exit-addressable but actually untouchable by trail tuning. The next
autopsy should **partition FADED by whether the trail had engaged**; the journal schema supports
it. If a large share is pre-engagement, the true exit-addressable pool is even smaller than
−1,679R, and the case for entry-side/structural-stop work strengthens further.

**Whether X4 retained X0's aging rule is not stated in the record. [record gap]** If a time-stop
still exists, it needs the same MFE-distribution scrutiny the ratchet got; if it doesn't, stale
sub-engagement trades tie up the single position slot indefinitely — a real cost in a
one-position system. Worth one look at the code and one journal query (time-in-trade distribution
by cohort).

**Closed-bar updates and stop-price fills are honest in simulation but hide the live gap.
[analysis]** The trail moves once per closed 5m bar; simulated stop fills execute at the stop
price (or the open when gapped through). On a live venue, stop-market slippage in the high-vol
regime — again, the edge-carrying regime — is exactly where paper and live will diverge. This is
not a reason to change the model; it is *the* reason minimum-live exists as a measurement step,
and a reason to log intended-vs-filled stop prices from the first live order.

**The X4-over-X3 commit was marginal and the forward evidence since has favored X3. [verified]**
Not actionable retrospectively (that data is read), but the next agent should treat "committed
default" as a standing A/B, not a settled question — Prometheus's both-arms-in-every-batch
practice is the right template.

---

## 5. What transfers to the next agent — the exit-design playbook

Distilled to the patterns that are strategy-agnostic:

1. **MFE first, mechanism second.** Before designing any harvest logic, measure the entry set's
   MFE/MAE distribution. Every threshold in the exit (arming lines, breakeven triggers,
   engagement conditions) must be checked against where the trades actually live. This single
   check would have caught SSv10's ratchet before a line of it was ported.
2. **Ship capture ratio and pre-engagement death share as day-one metrics.** They are the two
   numbers that expose a decorative exit. Add the tail-capture line for any low-hit profile.
3. **Race exits as a family over frozen entries**, incumbent as control, one mechanism axis per
   variant, at least two contrasting regime windows. Expect the simplest variant to win; expect
   hybrids to lose (mechanism subtraction beat addition here, twice).
4. **Default hypothesis: a two-phase stop lifecycle.** Survival phase — structural stop anchored
   to the signal-generating bar, untouched. Harvest phase — a structure-following trail, entered
   via an engagement condition defined in *structure terms* (closed bar beyond the anchor), not
   in money terms (an R-level). Money-space geometry is arbitrary; structure-space geometry is
   the same geometry the entry trades.
5. **Keep the ratchet invariant (stops never loosen) as a hard, fixture-enforced rule in every
   execution mode** — replay, paper, live — and make stop-guarantee-and-repair the first action
   of every wake. Prometheus's circuit-breaker replay gap shows what happens when a risk rail is
   fixture-covered in one mode only.
6. **Journal shadow stops.** Record where every *candidate* exit variant would have exited, every
   trade, plus `mfe_r`/`mae_r`/`give_back_r` and post-exit continuation. This converts exit
   research from "collect new forward data per variant" (weeks per answer) into "re-simulate the
   existing journal offline" (minutes per answer) — the single highest-leverage schema decision
   in the whole project.
7. **Test decoupling before tuning independently.** Cohort-mix invariance across entry sets and
   regimes is the evidence that licenses treating exits as a separable module. Check it; don't
   assume it.
8. **Size the prize before every exit-tuning cycle.** Recompute the exit-addressable share of
   total loss (FADED-type cohorts, engagement-partitioned). If it's the minority owner, say so
   and point the effort at the majority owner — Prometheus's 2.5:1 finding redirected an entire
   phase, correctly.
9. **Evaluate every exit change asymmetrically on tail-carried profiles.** Pre-register the rule:
   a variant that reduces give-back is rejected if tail-capture falls by more than a stated
   tolerance. The one-trade-carries-thirty paper run is the standing reminder of why.

---

## 6. Conclusions

**Intermediate conclusions (established on Prometheus, spent data — characterization only):**
the SSv10 R1-armed ratchet was decorative for two-thirds of trades and value-destroying overall;
an engagement-guarded e200 structure trail dominated every R-level variant raced; buffer width is
regime-sensitive with a thin overall margin; the trail's mid-trade give-back is a stable ~17% tax
independent of entry quality; and half of all raw-entry trades never survive to meet the trail at
all.

**Final conclusions (the ones that travel):** exit logic must be fitted to the measured excursion
distribution of the entries it serves, not to a money-space aesthetic; two-phase
structural-survival → structure-trail architectures are the strongest starting hypothesis for
trend-following, tail-carried systems; the exit's importance is bounded — measure its share of
the loss before investing in it, and expect initial stop placement to matter more than trailing
mechanics in low-hit systems; and the journal, if it records shadow stops and excursion paths, is
a renewable laboratory for exit research that costs no new data. The open frontier Prometheus
hands to its successor is specific: the never-loosen/vol-expansion interaction in high-vol
regimes, engagement-partitioned FADED accounting, and the birth-structural-stop tightening that
the last characterization pointed at — all answerable from the paper journal now accruing,
provided the rules stay frozen while it does.

---

*Gaps a future session could close with source files: the exact race margins for X1/X2/X5 (only
X0 vs X3/X4 is quantified in the record), whether X4 retained X0's aging rule, and the original
SSv10 ratchet's full parameterization beyond its R1 arming. If the Phase 3/3b build notes are
attached to a future conversation, fold them in and reissue this document as v2.*
