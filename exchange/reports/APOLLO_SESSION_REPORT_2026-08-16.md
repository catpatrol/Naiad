# APOLLO — SESSION REPORT · 2026-08-16

**Lane** APOLLO (engine builds · repo operations · integrity & manifest) · **Branch** `v12-v1-census` · **Drafted** APOLLO · **Executor** HEPHAESTUS · **Seed** 20260816

**RATIFIED** operator 2026-08-16 — *"emit session report for Apollo lane"*.

**CLASS — reporting.** This document scores nothing, registers nothing and moves no number. Every figure in it is quoted from a filed table with its sha in §8, and the one place it speaks in its own voice is §4, where it is asked to.

---

## 0 · THE SESSION IN ONE PAGE

**Four things happened, and the fourth is the one that changes what the lane can do next.**

| | what it was | what it produced |
|---|---|---|
| **TIER-C4** | the mean card — LPS-trail ratchet + creek/ice harvest on the v3 card, 118 sealed days | **the mean did not move; the SHAPE did.** maxDD halved, tail share −21 pts, and the ex-best-trade result changed sign. 12 repairs from an adversarial review run before publication |
| **THE INTERVIEW REPLIES** | D12, D13(c), D15 and the seal-open ruling, enacted | **the box was opened.** D15 demoted from gate to diagnostic, by the operator's own word |
| **TIER-C5** | full water — 2,534 days, 195 campaigns, two registrations, a 25-cell fleet, three labs | **nothing was supported, including the card.** 16 repairs, one reversed verdict, two headline numbers changed |
| **TIER-C5-Q** | the queryable book + this report | **436 campaigns, 3,677 instants, zero holes, 195 ms a query.** Every trade in the book is now interrogable to the registry level. 9 repairs over two reviews — including a completeness check a book could pass having lost 64% of itself |

**THE ONE-LINE ARC.** A card that looked like **+0.6907 R per trade** over one quarter returns **+0.1724** over seven years, cannot be distinguished from zero at the estate's own bar, rests 84% on one asset — **and is now the first card in this estate that can be cross-examined trade by trade without a rebuild.** The measurement got worse and the instrumentation got very much better, and those are the same event: **you cannot find out that a number is thin without looking at it closely enough to find out.**

---

## 1 · TIER-C4 · THE MEAN CARD

**The operator asked for "a mean for the average trade". The card delivered one, and the price was the tail.**

| | v3 | **v4** |
|---|---:|---:|
| expectancy / trade | +0.7056 | **+0.6907** |
| maxDD (R) | 4.2697 | **2.0348** |
| tail concentration | 71.83% | **50.76%** |
| **net R without the best trade** | **−2.2912** | **+1.4184** |

**That last row was the deliverable.** Under v3 the yardstick was negative once you removed one trade of eleven. Under v4 it is positive. **The mean moved −0.1636 R; the distribution changed completely.**

### The ablation, and why the two amendments cannot be quoted apart

| cell | net R | marginal vs V3 |
|---|---:|---:|
| V3 (control) | +7.7614 | — |
| RATCHET only | +7.3262 | −0.4352 |
| HARVEST only | +4.5800 | −3.1814 |
| **BOTH (shipped)** | **+7.5978** | **−0.1636** |

**Interaction +3.4530 R.** The trail pre-empts the harvest — **9 fills when the harvest rides alone, 3 when the trail is on** — because a ratchet stop ends the campaign before the band is reached. **Any sentence of the form "the harvest is worth −3.18 R" is false about the shipped card**, and the ablation table carries the interaction column so that sentence cannot be written from it by accident.

### The ETH-10-29 narration — the estate's dominant trade, third card running

ETHUSDT short, entered 2025-10-29T16:00Z at 3903.54, R = 78.403688 = exactly 1.000 ATR (rail-bound).

- **v3** rode to the counter-12/89 bell on 2025-12-03 at 3126.78 — **+10.0526 R**, 210 bars.
- **v4** trailed four advances (0.497 → 0.058 → **3.992** → 1.122 ATR) and was stopped at **3419.423324** on 2025-11-07, bar 54 — **+6.1794 R**. The stop was placed at the close of 11-07T12:00Z and hit on the very next bar.
- **The harvest never fired.** Under HARVEST-only the band touch lands at bar 68 with a unit move of +3.5341 R. **The trail ended the campaign fourteen bars early, so the harvest never fired on the one campaign it was built for.** That single fact is the interaction term in miniature.
- **And the give-back is the honest frame.** v3's own peak was +16.3709 R at 2025-11-21 — a fortnight after v4 exited. But v4 did not merely miss a peak it never saw: **inside its own 54-bar ride it was +10.8227 R and it exited at +6.18.** The trail gave back 4.64 R of its own excursion, because a trail is a stop and a stop is behind price by construction.

*(Every one of those numbers is now one command away: `query_trade.py ETHUSDT:card:20251029T1600`.)*

---

## 2 · THE INTERVIEW REPLIES, ENACTED

**THE RULING, VERBATIM AND OF RECORD:**

> *"open the sealed box, we lose continuity otherwise… we will put it to paper trade the Prometheus route… another data stream"*
> *"D15 caveats not hard gates"*

| reply | what it said | how it was enacted |
|---|---|---|
| **the seal** | open the box | `sealed_mask` answers **False everywhere** — kept in the same shape, not deleted, so the ruling is one auditable function. 13,860 bars freed; **42 campaigns quote a formerly-sealed price** |
| **D12** | funding ceiling 1R | an ACCOUNTING rule that can move no price. **Bound 0 of 195 at unit size**, 2 at 2×, 4 at 3× |
| **D13(c)** | lead-in trades COUNTED never SCORED | enacted at every **slice** edge — three campaigns named in `d13c_counted_not_scored` |
| **D15** | *"caveats not hard gates"* — **the demotion** | the four diagnostic columns ride every scored and shadow line and **gate nothing**. They fired on the fleet's most attractive cell and it was still reported whole |

**THE SEAL-OPEN RULING CLOSED F-C3-a, AND NOT THE WAY IT WAS ARGUED.** Tier-C3 asked the operator to *ratify the seal floor or overturn it*. The operator did neither: **they removed the seal.** The three-build argument about whether an anchor is a price or a state is settled by not needing an answer.

**AND THE HONEST ACCOUNT OF THE D-BLOCK: only D12, D13(c) and D15 were ever stated.** `D1–D15` appears in exactly one place in the estate — `APOLLO_LANE_STATUS_2026-08-15.md:37-41` — which names four block titles and a count, **defines not one item**, and lists the interview as work *to be run*. **D1–D11 and D14 have no content anywhere; H3 and H6 have no content anywhere.** This session enacted the three the paste defined and reported the rest as absent rather than reconstructing them. Precedent: `BUILD_2026-08-15_VIZ2_CATHEDRAL.md:52`, finding V-6, on `fuzz` — named in the *same sentence* as D1–D15 and ruled anchorless. **Ruling needed: define them, or strike the labels and cite the pastes.**

---

## 3 · TIER-C5 · FULL WATER

### The lineage, all four, stated together

| | v1 | v3 | v4 | **v5** |
|---|---:|---:|---:|---:|
| corridor | 118 d sealed | 118 d sealed | 118 d sealed | **2,534 d OPEN** |
| n | 10 | 11 | 11 | **195** |
| **expectancy / trade** | −0.7762 | +0.7056 | +0.6907 | **+0.1724** |
| maxDD (R) | 9.5107 | 4.2697 | 2.0348 | **25.5353** |

**The 118-day number was not wrong. It was small.**

### By slice — and every R of the result is post-wall

| slice | n | net R | expectancy | tide mix (up/down/none) |
|---|---:|---:|---:|---|
| **pre-2024-07-01** | 123 | **−7.2687** | **−0.0591** | 45.2 / 42.4 / 12.4 |
| **post-2024-07-01** | 72 | **+40.8836** | **+0.5678** | 36.2 / 49.1 / 14.7 |
| the formerly SEALED span | 43 | +6.1866 | +0.1439 | 44.2 / 40.7 / 15.1 |
| **the operator's post-lockbox refresh** | 29 | +34.6970 | **+1.1964** | 24.3 / 61.4 / 14.3 |

**Four of seven scored years lose money.** The operator's own market-open read is the best slice by a factor of seven — **29 campaigns, PROVISIONAL, in-sample.**

### THE REFERENCE ROW — the bar, scored

**The single most consequential addition of the session.** Every registration was to be judged against a ruler; the reference row asks what that ruler says about **the card itself**:

| | n | expectancy | CI (asset-cluster 90%, mean) | p (1-sided) | verdict |
|---|---:|---:|---|---:|---|
| **THE CARD v5** | 195 | +0.1724 | **[−0.0271, +0.4336]** | 0.0912 | **NOT SUPPORTED** |

**On seven years, five assets and 195 campaigns, this card is not distinguishable from zero at q = 0.10.** That is F-C5-b, and it is the deepest open ruling in the estate.

### ZEC IS 84% OF THE BOOK

+28.2027 of +33.6149. BTC (−3.81) and NEAR (−2.98) are negative over seven years. **And ZEC is the asset whose removal flips every registration arm**: on all three arms the single leave-one-out panel that excludes zero is the one with ZEC dropped. **One asset is doing two contradictory jobs in this panel.**

### The three registration verdicts — and the reversal

| registration | arm | n | ruler | CI | verdict |
|---|---|---:|---|---|---|
| P-SPR-1 | standalone spring | 241 | own exp. vs 0 | [−0.0373, +0.2389] | NOT SUPPORTED |
| **P-SPR-1** | **card+spring UNION vs card** | 420 | **union − card** | [−0.2583, +0.0655] | **NOT SUPPORTED** |
| P-CASC-1 | card+adds (PAIRED) | 195 | paired Δ vs 0 | [−0.0100, +0.2532] | NOT SUPPORTED |

**THE UNION VERDICT WAS REVERSED IN REVIEW, AND IT IS THE session's sharpest catch.** The first draft named the arm *"vs card"* and scored it against **zero**. With 2.2× the card's campaigns a narrower interval passed — while the union was **per-campaign WORSE than the card, −0.0520 R**. Scored against the card, as its own name promises, it is nowhere near. **The union's apparent strength was never edge; it was n.**

**FDR applied, not merely recorded: m = 3 — the number of acceptance tests RUN, not the 2 registrations FILED.** Two registrations produced three tests (P-SPR-1 was scored twice), and a family counting filings gives the second bite of the same apple a free pass. Bar = 0.0333. **No arm clears it.**

### The fleet — the buffer siren and the arms-after-+1R cell

| grid | cell | net R | **paired Δexp** | **tail-exit ratio** | **max 1-trade Δ share** |
|---|---|---:|---:|---:|---:|
| card | v5 | +33.6149 | — | 1.0000 | — |
| **S-TRAIL** | **+0.25 ATR buffer** | **+69.2027** | **+0.1825** | **1.3383** | **1.1562** |
| S-TRAIL | arms after +1R | +39.9201 | +0.0323 | 1.0059 | 0.4833 |
| S-HARV | fixed +2R | +14.7445 | −0.0968 | **0.6708** | 0.6121 |
| S-CLOCK | no funding ceiling | +33.6149 | **0.0000** | **1.0000** | — |

**THE BUFFER SIREN.** `S-TRAIL +0.25 ATR buffer` doubles the book and cuts drawdown by a third — and its **max single-trade share of delta is 1.1562, GREATER THAN ONE**. The per-campaign deltas partly cancel and **one campaign's improvement exceeds the entire net improvement.** The number is real and the mechanism is one trade. **This is the cell that gets promoted if nobody reads the last column, and D15's demotion to diagnostic is exactly what lets it be printed whole instead of quietly filtered.**

**The arms-after-+1R cell is the quieter one worth a look:** +39.92 against +33.61, paired Δexp +0.0323, **tail-exit ratio 1.0059 and max-1-trade share 0.4833** — i.e. it improves the book *without* concentrating the improvement in one campaign. It is the only S-TRAIL cell whose diagnostics do not immediately disqualify its headline.

### The three labs

**H1 — THE HARVEST IS A DE-RISK, NEVER A PROFIT-TAKE.** 37 fills; **both** took (−9.1743) and would-have (−14.9127) are **negative**; delta **+5.7383 R**, positive in *every* slice, 32 of 37 helped. It fires when price rallies back into the band against the position, so the half it takes is always taken at a loss — **it earns its keep because the loss it takes is smaller than the loss the runner goes on to book.** ~17% of the result, from a rule that never once banked a gain.

**H2 / H7 — THE CHAMPION WALL IS EMA 889, ON BOTH SLOW CLOCKS INDEPENDENTLY.** 12h 62.71% rejection over 59 approaches; 1d 61.90% over 42. 4h → EMA 3618 (52.29%), 1h → EMA 4618 (48.36%). **And the league's floor: 12h EMA 316 rejects only 23.88% — the card's own tide-slow EMA is the weakest wall in the league on that clock.** The champion is a **named maximum, not a promotion**: an argmax over the eligible panel cells, no bar, no interval, no correction, and the 54 cells it is chosen from are in the logged selection surface.

**MID-BAND — the co-occurrence half is negative, and now honestly weighted.** Where the distinct-exit count is real, **v5 exits coinciding with mid-band traffic are v5's bad exits** (−0.55, −0.70, −0.70, −0.73). The n = 10 row with a +2,630 bps forward mean is printed as noise, because it is.

### THE AE CONSTANT — the most stable number in the estate

| population | winners reaching +1R | **mean AE** | median | p90 |
|---|---:|---:|---:|---:|
| **TC-BOOK** (whole v5 book) | 58 | **0.310491 R** | 0.2782 | 0.6391 |
| **CENSUS-ERA** (entries pre-2024-07-01) | 35 | **0.314526 R** | 0.2756 | 0.6572 |

**Over 2,534 days and two regimes, a winner goes about 0.31 R against you before it goes 1 R for you, and the two eras agree to four thousandths.** Nothing else in this session is that stable. It is now printed per campaign by the query tool, against this constant.

---

## 4 · THE REPAIR FORENSICS — the builder's account

*This section is written in my own voice because the card asks for it, and because a repair table that reads like a changelog teaches nothing. What follows is what I got wrong, how it was caught, and what the pattern is.*

**Four adversarial reviews ran BEFORE publication — six lenses on TC4, seven on TC5, then five and five again on TC5-Q — and between them they produced 37 NUMBERED repairs** (TC4 12 numbered plus 2 unnumbered · TC5 16 · TC5-Q 5 + 4). Tier-C3's seal breach was found *after* its draft was published and put a wrong number on the remote. That does not happen any more, and the reason it does not is that the audit moved in front of the publish.

### The 16 TC5 repairs, and the three that mattered

| # | what I got wrong | consequence |
|---|---|---|
| **1** | **The P-SPR-1 union arm was named "vs card" and scored against ZERO** | **A VERDICT REVERSED.** SUPPORTED → NOT SUPPORTED |
| **2** | The card was never scored through its own bar | added the reference row — **and it fails** (F-C5-b) |
| **3** | FDR declared m = 2 while 3 tests ran; I claimed a CI could not be BH-corrected | wrong — the bootstrap yields the tail. m = 3, correction applied |
| **4** | **No EMA warm-up.** `ind.ema` seeds at the series start, so at bar 0 every EMA equals the first close | **A HEADLINE NUMBER CHANGED.** 23 pre-warm armings, 4 scored campaigns; 199 → 195 |
| **5** | The spring's `sweep_extreme` omitted the reclaim bar | the stop sat inside a price the entry bar had traded, on 8 of 246 |
| **6** | S-LIMIT never tested the stop on the fill bar | every cell had a free bar of immunity |
| **7** | **S-SIZE scaled a capped book** — D12's 1R cap does not scale | **A HEADLINE NUMBER CHANGED.** `return ÷ maxDD` is not constant |
| 8 | `tail_exit_ratio` divided top-decile SUMS, so it scaled with n | load-bearing on exactly the rows where n differs |
| 9 | Mid-band co-occurrence was a triple mean-of-means over recycled exits | published as a statistic over EXITS |
| 10 | League panel rows pooled approaches but averaged penetration unweighted | two populations on one row |
| 11 | `is_champion_wall` was an argmax over 54 cells absent from the surface | surface 25 → 79 |
| 12 | The ratchet's seal call site was deleted, not answered | `seal_open=False` restored only half the mask |
| 13 | I counted sealed ANCHORS and not sealed RATCHET PIVOTS | understated my own box read: 41 → **42** campaigns |
| 14 | F-C5-GRID compared the built cards with the table written from them | the same object counted twice |
| 15 | Three F-C5-OPEN legs could not fail | including asserting a constant-false function is constant-false |
| 16 | F-C5-SPRING's picks were direction-blind; F-C5-LEAGUE rescanned a row that is never a champion | the mirrored branch and the published numbers were verified by nothing |

### THE PATTERN, AND IT IS ONE PATTERN

**Six of sixteen — and six of twelve in TC4 — are the same defect wearing different clothes: a check that re-derives a value the way the program derived it, and then compares it to itself.** `x is x`. An argmax compared with its own max. A coverage count taken from the list the tape was built from. A "trade by trade" claim implemented as a sum. **They all print PASS and they all test nothing**, and they are seductive precisely because writing one feels like writing a test.

**The second pattern is smaller and more embarrassing: a name that is almost right.** `dist_atr` collided with a tape column family and tripped the captured-not-consulted scan. `prior_extreme` did it again a build later. `half_move_r` reported a full-unit quantity. **Each was caught by a machine, none by reading.**

**The third is the one I would most want carried forward.** Four of the sixteen were not bugs in code but **claims stronger than the code established** — "exactly linear", "trade by trade", "a CI cannot be BH-corrected", "every call site still consults it". **Three of those four were sentences I wrote to explain why something was safe.** The explanation was the defect. When a docstring argues that a thing cannot go wrong, that is the paragraph to audit first.

**What actually caught things.** The single most productive fixture in the session was **F-C5-CTRL** — ride the parent's card through the child's code path and demand the parent's filed book trade-for-trade. It caught two real bugs on its first run that no other fixture could see, one of which (a seal-closed branch that had never been written) would have silently invalidated the control itself. **Every fork from here should carry one.**

---

## 5 · THE FIXTURE CONVENTION, ADOPTED

**From TC5 onward, every fixture leg states inline what would have to be true for it to FAIL.**

Adopted as F-C4-h's recommendation and made the house rule in TC5's transcript, where all 11 fixtures and every leg carry their own falsifier. TC5-Q's 8 fixtures carry them too. The convention is cheap and it is not cosmetic: **writing the failure condition is what exposed that three F-C5-OPEN legs did not have one** — a constant-false function asserted constant-false, and a "first sealed bar" that is the lockbox's own opening bar by construction. Both were replaced with legs that can fail: **the mask proved LIVE (11 campaigns box-open vs 10 box-closed over Tier-C4's corridor), and the first sealed bar the card actually QUOTES.**

**A leg with no answer to "what would break this?" is not a leg.**

---

## 6 · TIER-C5-Q · THE QUERYABLE BOOK

**Ruled 2026-08-16: *"projecting the analytics package… instantly queryable for every trade… ≥3 years"*.**

| | |
|---|---:|
| campaigns indexed | **436** (195 card + 241 spring; 60 add-carrying) |
| instants demanded · covered · **missing** | **3,677** · 3,677 · **0** |
| instant kinds | arming 436 · trigger 436 · exit 436 · **advance 680** · **pivot_bar 680** · **anchor_bar 436** · sweep 241 · add 117 · **retrace 117** · harvest 98 |
| tape rows | **13,861** — every instant plus a **DAILY 00:00Z spine** (11,232 rows) |
| corridor | 2019-09-08 → 2026-08-16 = **6.938 years** ⊇ the ruled 3 |
| **query latency** | **median 195 ms · worst 209 ms** cold subprocess · budget 2,000 ms · **9.6× headroom** |
| fixtures | **9/9 PASS** |

**THREE INSTANT KINDS THE COMMISSION DID NOT NAME WERE ADDED ANYWAY.** The card asked for arming / trigger / add / harvest / advance / exit. But **`anchor_bar`** is the bar the entry stop's price was quoted from — a published price that gets paid out — and **`pivot_bar`** is the same for every advance, and **`retrace`** is the bar that armed each add. **A book that prints those prices and cannot say what the walls looked like at the bar they came from is not queryable; it is nearly queryable.** Added on my own audit, not on the card's list: 1,233 extra instants, +591 tape rows.

**Level families, as ruled:** the AVWAP set (week/month/year anchors) · RVWAP ±1σ/±2σ at 7/30/90/365 d · prior day/week/month extremes — all three the estate's own `build_level_series`, bound not reimplemented — **plus the league champion distances, each read on its OWN clock**: EMA 4618 on 1h, EMA 3618 on 4h, EMA 889 on 12h and on 1d. Reading them all on the 4h lens would be a different quantity from the one the league scored.

**One command:**

```
$ python scripts/query_trade.py ETHUSDT:card:20251029T1600
```

prints identity, the D15 columns **rendered per campaign and labelled as such**, seal provenance, the AE path against the 0.310491 constant, the trail ledger with the binding side of every advance, the harvest took/would-have/delta, the adds, the wall context at **every** instant with signed ATR distances per family, the four champion distances, and the six-ribbon state. `--day`, `--random N` (seeded — *"an audit you cannot re-run is an anecdote"*), `--list ASSET`.

**THE TOOL COMPUTES NOTHING.** Everything it prints was written by Q1. That is why it is instant, and F-Q-4 measures the cold subprocess rather than an in-process timing, because that is what a user actually waits for.

### The five Q repairs — and the one I should have caught myself

A fifth adversarial review ran over TC5-Q. **Five repairs; two of them were mine to see and I did not.**

| what was wrong | what changed |
|---|---|
| **THE CHAMPION EMAs HAD NO WARM-UP FLOOR.** `ind.ema` seeds at the series start and never returns NaN — so a 4,618-length EMA published *the first close of the series* as a "wall". **This is verbatim TC5's own §9 repair #4, which I fixed in the decision path and then reintroduced here with EMAs 3–15× longer.** | a champion is emitted only from bar index ≥ its own length; NULL before, and the share is **filed**: 1h EMA4618 warm on 92.0% of rows, 4h EMA3618 74.4%, 12h EMA889 81.4%, **1d EMA889 61.9%** |
| **The champion was read as-of the bar's OPEN while every other column in the row is as-of its CLOSE** — four hours stale against the price it was differenced against | as-of is `ts + 4h`, the instant the card actually decided |
| **F-Q-5's causality counter was provably unreachable** — `searchsorted('right')−1` guarantees the condition it tested, and its value leg transcribed the function it was checking | replaced with **endpoint slicing**: the series is cut to the as-of bar and the EMA/ATR recomputed on the slice. A different computation path, and simultaneously the causality test — if any future bar contributed, the sliced value would differ |
| **F-Q-2's spring leg read no raw bar.** It loaded the frame, never used it, and ran Q1's own stored columns through a transcription of the program's own formula — proving that `r6()` preserves a min/max | the swept level and the sweep extreme are both **re-read from raw bars**; and the pick is now the **worst** spring, not the best |
| **F-Q-0 compared a manifest with its own git blob and never hashed a table** | two new legs: every filed parquet re-hashed from disk against the independent re-run, **and** against the committed manifest — with `corridor_and_seal` named as the one table whose dict-valued columns do not survive a parquet round-trip identically |

**AND TWO I CAUGHT BEFORE THE REVIEW RETURNED, WHICH ARE THE SAME TWO PATTERNS AGAIN.** The coverage assert was **circular** — the tape is built *from* the instant ledger, so of course the ledger is covered — so F-Q-1 now leads with a **completeness contract derived by introspection**: every `_ms` field across `Trade`, `Advance`, `Add` and `Spring` must map to an instant kind the ledger carries. Add a timestamped event and forget a kind, and it fails. The coverage count is still printed, **labelled as bookkeeping, not evidence.**

### The SIXTH review — and the leg that let a book lose 64% of itself

A sixth adversarial review ran over the finished TC5-Q. It confirmed eight findings; four were the repairs above, already applied while it worked. **Four were live, and one was a blocker.**

| what was wrong | what changed |
|---|---|
| **THE COMPLETENESS CONTRACT WAS ONLY HALF A CONTRACT — and it was the leg I had just written to replace a circular one.** It asks whether every `_ms` field maps to a kind **the ledger carries**, and that is satisfied by *one row of a kind*. The reviewer kept every arming/trigger/exit row and exactly **one each** of advance, harvest, add, anchor_bar, pivot_bar, retrace and sweep — **1,315 rows instead of 3,677**, leaving 1,483 real book bars with no snapshot — and **the whole file returned 8/8 PASS.** The coverage table read `0 missing` (it is seeded from the frame it checks) and the per-kind rows read `1 · 1 · 0` with an `[OK]` beside each | **F-Q-1 now carries a CARDINALITY contract**: every kind's row count re-derived from the campaigns table and the three ledgers — *never* from the instants frame — with dedup honoured exactly (what a source demands is its count of **distinct** `(campaign_id, ts)` pairs, not its rows). Replayed against the same sabotage it now **fails seven kinds and the total**, while the circular leg still cheerfully reports `0 missing` — which is the clearest statement of why both legs exist |
| **`slice_provisional` was the CARD lane's year count stamped onto SPRING rows.** 68 spring campaigns (33 in 2023, 35 in 2024) wore another lane's thinness verdict — a `True` on slices that hold 33 and 35 springs against a MIN_N of 30. The other three columns of that block are lane-scoped by construction; this one silently was not | lane-scoped, and `slice_n` is **filed beside the flag** so the count that produced the verdict is on the row. The screen now prints `slice 2023 · spring lane  n=33  PROVISIONAL False` |
| **`--day` filtered on arm/entry/exit only**, so **314 days** carrying 384 advances, 36 harvests and 18 adds printed `(nothing)` under a header reading THE BOOK ON *day*, and exited 0. Worse than the empty case: on 149 `(campaign, day)` pairs the day was *not* empty, so a table printed with no qualifier at all and the moving campaign simply was not in it | the filter is now the **instant ledger** — the same ledger the coverage contract is written against — so a day is empty here only when the book did nothing. It reports what each campaign *did*: `advanced, pivot bar` |
| **THE SEAL VERDICT WAS A NARROW TEST CARRYING A BROAD CLAIM** — two flags (the anchor's, and the pivots'), then the sentence *"Tier-C2, C3 and C4 could have taken it unchanged."* **False on 332 of the 343 screens that printed it.** 190 were SPRING campaigns, and P-SPR-1 registers that lane GENUINELY NEW — those builds have no such lane. And it missed campaigns whose **entry and harvest prices** are quoted inside the span while only the anchor sits outside: SOL 2024-07-07 paid out on two formerly-sealed closes and printed *"quotes no price from the old lockbox"* | the claim is replaced by two things that are **checked**. `sealed_instants` counts every bar of the campaign's *own* life inside the span, off the full ledger, against a window **read from `RC.LOCKBOX_WAS`** instead of a hard-coded copy the register could outrun in silence. `in_tc4_book` is a **membership test** against C4's filed journal on `(asset, entry, exit)` — it finds **11/11** of C4's rows. **96 campaigns** quote a formerly-sealed price, where the two-flag test found a fraction of that |

**And the fix for the last one moved the test out of the tool**, because `query_trade.py`'s stated property is that it **computes nothing** — re-deriving a seal window at render time was a quiet breach of it that no fixture could see.

**THE NEW FIXTURE IS THE ADMISSION.** F-Q-0..F-Q-6 check what the tool *computes*: hashes, coverage, determinism, latency, champions, closure. **Not one of them read a sentence the tool prints** — and all three tool defects lived in exactly that gap. **F-Q-7 · THE RENDERED CLAIM** now checks the assertions themselves against the source, including the named counterexamples by name. Its seal leg re-derives `sealed_instants` from the campaign row's own timestamps *and all three ledgers* — and its **first draft forgot the adds**, disagreeing with the filed column on exactly the 19 add-carrying campaigns whose add bars fall in the span. **The filed number was right and my check was short.** That is the second path earning its keep in the only way it can.

**AND A THIRD PATTERN, NAMED.** Both surviving TC5-Q defects of this round were **a check that is satisfied by one example** — one row of a kind, one flag out of six bars. It is the presence/cardinality confusion, and it is the sibling of the circularity defect: the first compares a thing to itself, the second asks *does this exist* when the question was *how many*.

**NO SCORED NUMBER MOVED.** F-Q-0 asserts every one of TC5's 21 tables byte-identical to the manifest **committed at HEAD**, read out of git — not argued from the fact that Q1 writes elsewhere. The card froze three tables; the fixture freezes all 21, because a stage that moved a fourth would still have moved the record. **The four repairs above moved exactly one file: `campaigns.parquet` (`f946fb57…` → `8680fe93…`).** Every other Q1 table — instants, advances, harvests, adds, tape_full, coverage — re-wrote byte-identical, which is itself the check that the repairs touched what they claimed to.

**THE QUERYABLE BOOK IS THE NEW FLOOR FOR REGISTRATION WORDING.** A registration whose predicate cannot be evaluated against `campaigns`, `instants` and `tape_full` is a registration nobody can score without a rebuild, and this estate has already lost two registrations to definitions the contract never carried (H-VBT, leap/stair arrival). **From here, wording a claim means naming the columns it will be scored on.**

---

## 7 · THE OPEN RULINGS REGISTER

### ⚑ TOP — THE UNIVERSE QUESTION

**ZEC is 84% of the book AND the asset whose removal flips every registration arm.** BTC and NEAR are negative over seven years. Every panel claim this session made is, on inspection, a claim about one or two assets with three witnesses that disagree.

**THREE OPTIONS, AND MY LEAN.** (a) Keep the five and accept that the panel result is a ZEC result — cheap, honest, and it makes every future registration harder to pass, which may be correct. (b) Expand the universe — the cache holds JTO, TAO, FARTCOIN, HYPE, LIT, but **the PAXG lesson stands**: an asset whose history begins after the wall can never enter a scored table under I1, and four of those five begin in 2023–2025. (c) Require per-asset replication as a registration predicate rather than a diagnostic. **MY LEAN IS (c) WITH (a):** keep the panel, and make "excludes zero on ≥ 3 of 5 leave-one-out panels" part of the registered text rather than a caveat printed beside it. **It would have failed all three arms this session, which is the point.** *This is the operator's call and it gates every future registration.*

### THE THREE TC4 LEANS THE CARD ASKS FOR

**F-C4-b · PIN THE TRAIL'S "BEYOND" AT 0.5 ATR — MY LEAN: RATIFY THE RE-POINTED INHERITANCE.** The card says *"advance the stop to beyond that pivot"*, and *beyond* is the v3 card's own word for its entry anchor's 0.5 ATR offset. The alternative reading (0.0 — the stop exactly at the pivot) parks a trailing stop on a known liquidity magnet. It is load-bearing: in TC4's book the pivot buffer, not the rail, set the stop on **14 of 21** advances, and the TC5 book carries 273. **Lean: ratify 0.5 as the card's own definition of "beyond", and record that the 0.0 reading was named and not taken.**

**F-C4-c / F-C5-e · THE BELL — MY LEAN: KEEP IT AS A BACKSTOP, DO NOT STRIKE.** It fires **once in seven years** (194 of 195 exits are stops). But it fires rarely because the trail is *faster*, not because the bell is wrong — and a regime in which no favourable fractal ever confirms would leave a campaign with no exit but its entry stop. **A rule that costs nothing to keep and whose absence is discovered only in the regime that needed it should be kept.** Record it as a backstop expected never to fire, so nobody later mistakes its silence for evidence it works.

**F-C4-d · A MINIMUM ADVANCE INCREMENT — MY LEAN: ADOPT THE PRINCIPLE, LET THE OPERATOR PIN THE NUMBER.** The smallest advance in the TC4 book was **0.002053 ATR and it was the one that was paid out**. An advance that small is arithmetic clearing zero, not a decision. **But I will not pin the threshold by looking at this book's outcomes** — that is a selection surface with one cell. Lean: adopt a minimum, and derive it from something outside the book (the instrument's tick, or the toll expressed in ATR), not from what would have improved the result.

### THE H-ANSWERS AWAITING OPERATOR WORD

| hook | status |
|---|---|
| **H1** harvest-vs-ride | **ANSWERED** — a de-risk, never a profit-take; +5.7383 R, positive in every slice. `harvest_lab` |
| **H2 / H7** resistance / walls | **ANSWERED** — EMA 889 champion on both slow clocks; EMA 316 the weakest wall on 12h. `resistance_league` |
| **H4 / H5** the trail lab | **MEASURED, NOT ANSWERED** — the S-TRAIL cells are on the table; the +0.25 buffer cell fails its own D15 column. Awaits the F-C4-b/d rulings above |
| **H3** | **NO DEFINITION ANYWHERE** — ruling needed |
| **H6** | **NO DEFINITION ANYWHERE** — ruling needed |

### CARRIED, FROM THE FULL REGISTER

**Closed this session:** F-C3-a (the seal floor — closed by ruling, not by argument).
**Blocking:** **F-C5-k** — the live paper line is three card versions behind **and the ruling just made it the out-of-sample instrument.** This moved from housekeeping to blocking the moment out-of-sample transferred forward.
**Open:** F-C5-a (which number is the yardstick — three candidates 7× apart) · **F-C5-b (the card does not clear the estate's own bar)** · F-C5-c (ZEC) · F-C5-d (D12 inert at unit size) · F-C5-g (S-LIMIT's avg-AE is fitted on the book it is scored against) · F-C5-h (D1–D15 and H1–H7 have no source) · F-C5-i (the spring's tide reading refuses 3,526 sweeps and admits 241) · F-C5-j (Tier-C4's `Trade` docstring is falsified by the open seal) · F-C3-b/c/e · F-C4-i.

---

## 8 · ARTIFACTS ATLAS

**Documents (published, `exchange/reports/`)** — sha256, first 12

| document | bytes | sha | commit |
|---|---:|---|---|
| `BUILD_2026-08-16_TIERC4_MEANCARD.md` | 69,480 | `792bbdea383a` | `098abe3` (superseding `5d4acdc`, `49cc242`) |
| `BUILD_2026-08-16_TIERC5_FULLWATER.md` | 45,902 | `c0c80b8de856` | `01f18ae` |
| `exchange/status/LEDGER_APOLLO.md` | 128,670 | `5e77b406d565` | appended 4× this session |
| `APOLLO_SESSION_REPORT_2026-08-16.md` | — | — | *this paste* |

**Programs (`scripts/`)**

| file | bytes | sha | commit |
|---|---:|---|---|
| `tierc4_rules.py` | 29,342 | `3e56420575d1` | `dc20923` |
| `tierc4_baseline.py` | 67,567 | `24186f9b285a` | `dc20923` |
| `tierc4_fixtures.py` | 82,468 | `784952e8dee9` | `dc20923` |
| `tierc4_independent.py` | 14,965 | `f15b974f4097` | `dc20923` |
| `tierc5_rules.py` | 34,173 | `c27a5ecb425f` | `a20c579` |
| `tierc5.py` | 101,988 | `ad912b385cc8` | `a20c579` |
| `tierc5_fixtures.py` | 49,549 | `3ec5758314f4` | `a20c579` |
| `tierc5q.py` | 37,568 | `43ebf7a0fecf` | *this paste* |
| `query_trade.py` | 21,393 | `a24b0ca8726f` | *this paste* |
| `tierc5q_fixtures.py` | 48,745 | `693fcb4351f8` | *this paste* |

**Tables (local, gitignored; manifests tracked)**

| root | tables | on disk | manifest commit |
|---|---:|---:|---|
| `research_outputs/tierc4{,_run2}/` | 17 | — | `d818144` |
| `research_outputs/tierc5{,_run2}/` | 21 | — | `88c48c3` |
| `research_outputs/tierc5q/` | **7** | **≈ 3.3 MB** | *this paste* |

**TC5's frozen scored tables** (F-Q-0 asserts these against `git show HEAD:…`): `headline` `4752d260368b` · `registrations` `57a539a80268` · `fleet` `d7b853b98f31` — **and the other 18 with them.**

**Content-shas of the queryable book** (`research_outputs/tierc5q/build_manifest.json`)

| table | rows | sha (12) |
|---|---:|---|
| `campaigns` | 436 | `8680fe93624c` |
| `instants` | **3,677** | `012ec8ffad…` |
| `advances` | 680 | `409b52c991e6` |
| `harvests` | 98 | `80cab8f04aba` |
| `adds` | 117 | `b145236af107` |
| `tape_full` | **13,861** | `b20ba3d2d0…` |
| `coverage` | 15 | `13deddd1c7…` |

**Fixture state at session close:** TC4 **10/10** · TC4 independent re-derivation **agrees on all 11 trades** · TC5 **11/11** · TC5-Q **9/9** · estate suite **334 passed, 1 skipped, exit 0**.

---

## 9 · THE LEDGER_APOLLO APPEND

```
=== STATUS_APOLLO — 2026-08-16d ===
NOW: SESSION CLOSE. Four stages: TIER-C4 (the mean card), the interview replies
     enacted (seal OPEN, D12, D13(c), D15 DEMOTED to diagnostic), TIER-C5
     (full water), TIER-C5-Q (the queryable book + this report).
THE ARC IN ONE LINE: a card that looked like +0.6907 R/trade over one sealed
     quarter returns +0.1724 over seven open years, CANNOT BE DISTINGUISHED
     FROM ZERO at the estate's own bar (CI [-0.0271,+0.4336], p 0.0912), rests
     84% on ZEC — and is now the first card in this estate that can be
     cross-examined trade by trade without a rebuild. The measurement got worse
     and the instrumentation got much better, and those are the same event.
TC5-Q IS LIVE: 436 campaigns indexed (195 card + 241 spring, 60 add-carrying),
     3,677 instants demanded and 3,677 covered, ZERO missing; tape_full 13,861
     rows = every arming/trigger/sweep/add/advance/harvest/exit PLUS the three
     kinds the commission did not name and a queryable book needs anyway —
     anchor_bar, pivot_bar, retrace, the bars PUBLISHED PRICES are quoted from —
     PLUS a DAILY 00:00Z spine over 6.938 years (the ruling asked for >=3).
     Families: AVWAP set, RVWAP +-1s/+-2s, period extremes, and the league
     champions each on its OWN clock (1h EMA4618, 4h EMA3618, 12h & 1d EMA889),
     each NULL until its EMA has seen its own length — warm on 92.0 / 74.4 /
     81.4 / 61.9 % of rows, FILED.
     `python scripts/query_trade.py <campaign_id>` — median 195 ms, worst 209,
     budget 2,000, 9.6x headroom. It COMPUTES NOTHING; that is why it is fast.
     8/8 fixtures. F-Q-0 asserts all 21 TC5 tables unchanged — the manifest
     against its git blob AND every parquet re-hashed FROM DISK against both
     the committed manifest and the independent re-run. NO SCORED NUMBER MOVED.
*** THE QUERYABLE BOOK IS THE NEW FLOOR FOR REGISTRATION WORDING. *** A
     registration whose predicate cannot be evaluated against campaigns,
     instants and tape_full is one nobody can score without a rebuild. This
     estate has already lost registrations to definitions the contract never
     carried (H-VBT, leap/stair arrival). From here, wording a claim means
     naming the columns it will be scored on.
REVIEWS: THREE adversarial reviews run BEFORE publication (6 lenses on TC4,
     7 on TC5, 5 on TC5-Q). 33 NUMBERED repairs across the session (TC4 12 +
     2 unnumbered, TC5 16, TC5-Q 5). TWO of the TC5-Q five were mine to see
     and I did not: THE CHAMPION EMAs HAD NO WARM-UP FLOOR — verbatim TC5's
     own repair #4, which I fixed in the decision path and then reintroduced
     with EMAs 3-15x longer. ONE VERDICT
     REVERSED (P-SPR-1's union arm was named "vs card" and scored against
     ZERO). TWO HEADLINE NUMBERS CHANGED (an EMA warm-up floor the full-water
     corridor needed and no parent did; S-SIZE re-capped because D12's 1R cap
     does not scale). SIX of sixteen TC5 repairs were ONE defect wearing
     different clothes: a check that re-derives a value the way the program
     derived it and compares it to itself.
FIXTURE CONVENTION ADOPTED AS HOUSE RULE: every leg states inline what would
     have to be true for it to FAIL. It is what exposed that three F-C5-OPEN
     legs had no answer.
PENDING (operator) — the register, TOP first:
  TOP  THE UNIVERSE QUESTION. ZEC is 84% of the book AND the asset whose
       removal flips every registration arm. LEAN: keep the five-asset panel
       AND make "excludes zero on >=3 of 5 leave-one-out panels" part of the
       REGISTERED TEXT rather than a caveat beside it. It would have failed all
       three arms this session, which is the point. Gates every future
       registration
  F-C5-b  THE CARD DOES NOT CLEAR THE ESTATE'S OWN BAR on 195 campaigns over
       seven years. Edge that is hard to measure, or a coin that flipped heads?
  F-C5-k  BLOCKING — the live paper line is THREE card versions behind and the
       seal-open ruling just made it the OUT-OF-SAMPLE INSTRUMENT
  F-C5-a  which number is the yardstick: +0.6907 / +0.1724 / +1.1964, 7x apart
  F-C4-b  LEAN: RATIFY 0.5 ATR as the trail's "beyond" — the card's own word
       for it at the entry anchor; the 0.0 reading parks a stop on a liquidity
       magnet. Buffer-bound on 14 of 21 TC4 advances
  F-C4-c  LEAN: KEEP THE BELL AS A BACKSTOP, do not strike. It fires once in
       seven years because the trail is faster, not because it is wrong
  F-C4-d  LEAN: ADOPT A MINIMUM ADVANCE INCREMENT in principle; the operator
       pins the number, and NOT from this book's outcomes (the smallest advance
       was 0.002053 ATR and it was the one paid out)
  H3, H6  NO DEFINITION ANYWHERE. Define, or strike the labels (precedent V-6)
  -- H1 ANSWERED (harvest = de-risk, +5.7383 R, positive in every slice);
     H2/H7 ANSWERED (champion wall EMA 889 on both slow clocks; EMA 316 the
     WEAKEST wall on 12h); H4/H5 MEASURED not answered, awaiting F-C4-b/d.
  -- also open: F-C5-c, F-C5-d, F-C5-g, F-C5-h, F-C5-i, F-C5-j, F-C3-b/c/e,
     F-C4-i. CLOSED this session: F-C3-a, by ruling.
PROBE LEDGER: card m = 0. TC5's logged selection surface 79, written BEFORE the
     look. TC5-Q registers nothing and scores nothing. EXPLORATION — ungated;
     promotion requires registration and declares its m first.
=== END STATUS ===
```

---

*End of session report. APOLLO · 2026-08-16 · four stages · four pre-publication reviews · 37 repairs · one reversed verdict · nothing supported, including the card · and the book is queryable — and now says only what it can show.*
