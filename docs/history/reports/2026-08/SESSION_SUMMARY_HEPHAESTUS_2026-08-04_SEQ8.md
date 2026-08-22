# SESSION SUMMARY — HEPHAESTUS · the cascade extract is built; the registered claim replicates; the window turns out not to be the thing that defines a cascade

**Date:** 2026-08-04 · **Lane:** HEPHAESTUS (local Windows Claude Code, repo read/write) · **For:** the whole pantheon, zero context assumed
**Companion:** `exchange/reports/BUILDERS_REPORT_HEPHAESTUS_2026-08-04_SEQ8.md`
**Contract:** `exchange/queue/2026-08-04_SEQ8_cascade_event_extract_DIONYSUS.md`, stamped **"extract"**

---

## 1 · What was built, in plain language

The contract asked for the raw material that lets Naiad study *sequences* of Secret Sauce events — across time and across timeframes — **without deciding in advance what a "cascade" is**. That is what now exists.

- **The atom layer (D1).** Every EMA cross the census machinery knows how to find, on all seven timeframes, for both alphabets — the familiar `{9,89,200}` and the newly-added `{12,25}` — written out one event per row, with **no chaining at all**. 288,711 events. Each row also carries a small snapshot of what *every other* timeframe looked like at that instant, so a question like "5m crossed up, then 15m, then 4h, and was the 12H trend aligned?" can be answered by reading this one file. No re-extraction, ever.
- **The cascade layer (D2).** Eight different definitions of "a cascade" — four time windows × two chaining rules — all computed *on top of* the atoms. 950,145 cascades. Because nothing is baked in, a ninth definition is a query, not a rebuild.
- **The outcome layer (D3/D4)** and the **bridge to the trade journals** — built, hashed, filed, and **deliberately not looked at**, per the embargo.
- **The replication panel (D5)** — the one claim we were allowed to score this run.
- **A warmup table (D6)** so no future study quietly uses a half-converged EMA.

**All eight fixtures pass**, including a full independent re-run that reproduced every table byte-for-byte.

## 2 · The headline: the registered claim replicates

**P-SEQ-ii — "the leap into 4H is the dominant way 4H activates, and 1H arrivals mostly climb in from the step below" — REPLICATES.** Both halves, on **all seven assets**, against a bar that required five.

Two honest qualifications, stated up front rather than buried:

- **Two of the seven assets are thin.** TAO contributes 2 observations and JTO 7. They point the same way, but this should be read as *five solid assets plus two thin ones*, not seven independent confirmations. It clears the bar on the five majors alone.
- **The claim was scored in the frame it was made in.** P-SEQ-ii is a *replication* claim about a finding from the Cascade Atlas. Scoring it on the new cascade objects instead would have been testing something else while calling it a replication. So the Atlas's own construction was rebuilt from scratch and its published numbers reproduced **exactly** — 2,378 cascades, every signature count, every frontier cell, the 83.6% monotone figure — and the claim scored there. The other frames are reported beside it, including the two where it fails.

## 3 · The finding that matters more than the claim

**The "leap" is not a property of cascades. It is a property of where you stand when you look.**

The Atlas counts forward from a pullback low. Only crosses *after* that low count — so if the 1H cross happened just **before** the low, 1H is simply missing from the ladder, and the 4H arrival looks like a jump straight from the fast timeframes. Chain the same events without an anchor and that gap fills in: across the whole substrate, the rung actually feeding 4H is **1H in 5,736 cases** versus 3,344 from the fast tier.

The mirror image also holds: cutting cascades off at three rungs — which the Atlas does — *manufactures* leaps at 4H and *destroys* adjacency at 1H, both from the same cause. A cascade that visits 30m before 1H pushes 1H out of the top three, so the 1H arrivals that survive the cut are disproportionately the leaping ones.

None of this makes the Atlas wrong. It makes the leap **anchor-relative**, and it means "how did price get to 4H?" has two different true answers depending on whether you are asking from a pullback low or from an open-ended sequence. That distinction is worth having before it becomes a trading rule. It is reported as counts; it carries no stamp and is not a promotion.

## 4 · The operator's standing question, answered with numbers

The SEQ-1 gate was: *is a time-based definition of a cascade a good definition at all? does the data suggest a less arbitrary one?*

**The counts say a time window is a poor primary definition — because within the ranges we were asked to test, it barely does anything.**

Under the **direction-consistent** rule (a cross the other way ends the cascade), stretching the window from 24 hours to a full week changes the cascade count by **95 out of ~65,200 — one seventh of one percent** — and leaves 99.98% of events sitting in an identically-shaped cascade. Under the **window-chained** rule the same stretch changes everything: singletons collapse from 28,800 to 940. And the two rules agree with each other on only about **8%** of events.

The reason is simple once seen: counter-direction crosses on fast timeframes arrive every few hours, so a direction-consistent cascade nearly always ends on price behaviour long before any of these windows runs out. **The window is not doing the work — it is never even reached.**

So the less arbitrary object the data points at is *the direction-consistent episode*, whose boundary is set by what price does rather than by a number of hours we chose. **This is an observation from counts, not a claim, and it is not registered.** It is offered because it is exactly what the gate asked for.

## 5 · What we could not do as written, and what was done instead

Four places where the contract could not be executed literally. All were handled in the open and none was quietly patched.

- **Fixture F-SEQ4 assumed the Atlas's 2,378 was a window-chained count of crosses. It is not** — it counts pullback lows and looks forward from each. Those are different objects over different populations, and making them equal would have meant breaking something. The fixture's own escape clause was used: the Atlas was rebuilt under *its* recipe, matched exactly on all 20 published values, and the difference from the new cascades itemised on five axes.
- **"Zero orphans both ways" on the trade join is not a symmetric condition.** Every joined trade does exist in the journals — zero orphans. But **286 births fall inside no cascade at all**, which is a real result (the engine traded when no cascade was open), not an error. Forcing that to zero would have meant inventing cascades.
- **"NaN until full warmup" had no definition in this repo** — the engine's EMA never returns NaN, and three different conventions exist elsewhere. A rule was stated arithmetically and printed: an EMA is warm once its starting guess accounts for less than 0.1% of its value (1,037 bars for EMA300, 1,555 for EMA450). **13 asset/timeframe cells never warm at all** and say so with the word `NEVER`.
- **"Tier grammar" does not exist anywhere in the repo.** It was built from the operator's own words in the SEQ-2 ruling (30m-chop · 1H-stair · 4h-12h-slow) plus the trend tier, and is labelled **builder-defined, pending your stamp**.

Also worth knowing: of the five event types in the Q1c taxonomy, **only one — the EMA cross — is emitted**, because only that one has a detector in the census machinery and the contract forbade building new ones. Test-and-reject, test-and-bounce, S/R flip and ribbon-state episodes are **not in this substrate**. That gap list is a deliverable, and a scoping question for you.

## 6 · Things you should know that nobody asked about

- **The bulk artifacts (3.5 GB across two runs) are not gitignored.** Nothing pushes them today, but nothing stops them either. No ignore rule was added without your say-so.
- **The trade journals this build joined against exist on this machine only.** They are gitignored staging, 1.4 GB, explicitly "not evidence". If this machine is lost, the cascade→trade bridge is not reproducible without re-running S-3.
- **Two small errors in the published Atlas** turned up while reproducing it: the "48 hours after the low" label actually measures from the confirmation bar (5 bars later), and the 83.6% monotone figure belongs to a different population than the prose attaches it to (for the 2,378 it is 83.01%). Reported, not edited.
- **The 1D governor has no trade counterpart** — the engine's mandates stop at 12H — so 1D cascades can never join a trade. Empty by design, not by fault.

## 7 · Open items and owners

1. **Operator — ruling requested:** should `research_outputs/seq8/**` get a `.gitignore` rule? (Precedent says these land under a named authorization; none was assumed.)
2. **Operator — stamp requested:** the builder-defined **tier grammar** (FAST 5m/15m/30m · STAIR 1h · SLOW 4h/12h · TREND 1d).
3. **Operator — scoping question:** the four unemitted Q1c event classes. Are they in scope for a follow-on, and is `{12,25}` meant to generate only 12×25, or also 12×200 / 25×200?
4. **Reviewer — LEDGER entry:** P-SEQ-ii is **not** registered in `LEDGER.md` (`grep` → 0 hits). The contract commissioned scoring it and the SEQ-7 ruling registered it, so it was scored; but the standing rule wants the verdict to postdate a registration commit. **Proposed entry:** `P-SEQ-ii`, prior **75%**, falsified if the leap is not the largest 4h arrival category, or adjacency not the largest at 1h, on fewer than 5 of 7 assets. **Measured: replicates, 7/7 both limbs, Atlas frame.** The builder does not write to `LEDGER.md`; this is yours to land.
5. **Operator + DIONYSUS:** the outcome tables (D3/D4) and the cascade→trade join are built and waiting. They stay embargoed until the Secret Sauce deep-dive returns the parked stamps.
6. **Anyone reading the Atlas:** treat the leap as anchor-relative until §3 above is either confirmed or overturned by a stamped study.

---

*Filed by HEPHAESTUS. Rides the `exchange/**` auto-publish scope; the five `scripts/seq8_*.py` files are deliberately left uncommitted, because W-F1 §18 proved commit-no-push cannot be honoured on this branch and that choice is the operator's, not the builder's.*
