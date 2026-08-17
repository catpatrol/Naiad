# BUILD — TIER-C5 · FULL-WATER TUNING RUN

**Date** 2026-08-16 · **Branch** `v12-v1-census` · **HEAD at start** `098abe3` · **Seed** 20260816 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**RATIFIED** operator 2026-08-16. **THE RULING, VERBATIM AND OF RECORD:**

> *"open the sealed box, we lose continuity otherwise… we will put it to paper trade the Prometheus route… another data stream"*
> *"D15 caveats not hard gates"*

**CLASS — measurement + PRE-REGISTERED CLAIMS + PRE-NAMED SHADOW GRIDS.** Every grid reported WHOLE; no cell dropped, none promoted. The guard is **loaded, called, idle at m = 0**, and **THE SELECTION SURFACE IS LOGGED: 79 cells** — 25 shadow cells across 8 pre-named grids, plus the 54 eligible league cells a champion wall is argmaxed from. With a fleet on the table the honest statement is not *"we did not sweep"*, it is *"here is exactly how many cells were available to pick from, written down before anyone looked"*. No estate write. No live orders.

**Programs (local):** `scripts/tierc5_rules.py` (decision path) · `scripts/tierc5.py` (program) · `scripts/tierc5_fixtures.py` (transcript). **Tables local** at `research_outputs/tierc5/` — 21 parquet + `build_manifest.json`.

**THE CARD NAMED ONE FILE AND THIS BUILD SHIPS THREE**, for one reason: F-C5-6 requires the decision path to import no `analytics` member and the program must import several. One file could not be both. Named, not taken quietly.

**I9** — `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()` `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`. **BINANCE USDT-M perpetuals**, `{BTC,ETH,SOL,NEAR,ZEC}USDT.P`, offline cache.

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**The box is open, the corridor went from 118 days to 2,534, the yardstick fell by three quarters, and NOTHING WAS SUPPORTED — including the card.**

| | v1 (C2) | v3 (C3) | v4 (C4) | **v5 (C5)** |
|---|---:|---:|---:|---:|
| corridor | 118 d, **sealed** | 118 d, **sealed** | 118 d, **sealed** | **2,534 d, OPEN** |
| n | 10 | 11 | 11 | **195** |
| net R | −7.7620 | +7.7614 | +7.5978 | **+33.6149** |
| **expectancy / trade** | −0.7762 | **+0.7056** | **+0.6907** | **+0.1724** |
| win rate | 10.00% | 45.45% | 27.27% | **30.26%** |
| maxDD (R) | 9.5107 | 4.2697 | 2.0348 | **25.5353** |

**That is the finding, and it is not a disappointment — it is the reason the operator opened the box.** Tier-C3 and Tier-C4 measured **one quarter of one regime**, and every headline row since 2026-08-15 has said so. Ridden over seven years the same card returns **+0.1724 R per trade**. **The 118-day number was not wrong. It was small.**

**And the seven years are not one thing either:**

| slice | n | net R | expectancy | tide mix (up / down / neither) |
|---|---:|---:|---:|---|
| **pre-2024-07-01** | 123 | **−7.2687** | **−0.0591** | 45.2 / 42.4 / 12.4 |
| **post-2024-07-01** | 72 | **+40.8836** | **+0.5678** | 36.2 / 49.1 / 14.7 |
| the formerly SEALED span | 43 | +6.1866 | +0.1439 | 44.2 / 40.7 / 15.1 |
| **the operator's post-lockbox refresh** (2025-10-06→latest) | 29 | +34.6970 | **+1.1964** | 24.3 / 61.4 / 14.3 |

**Every R of the result is post-wall.** The first 1,757 days lose money over 123 campaigns. **The operator's own "market-open" read is the best slice in the book by a factor of seven — and it is 29 campaigns, PROVISIONAL, and in-sample.**

**AND THE SECOND HEADLINE: BOTH REGISTRATIONS FAILED, AND SO DID THE CARD.** Scored through one pre-declared ruler, **all three acceptance tests are NOT SUPPORTED** — and so is **the card itself**, printed as a reference row so nobody has to guess what the bar is worth. The card's own expectancy CI is **[−0.0271, +0.4336]**, one-sided p = 0.0912. **A seven-year, five-asset, 195-campaign book cannot distinguish this card from zero at the estate's own standing bar.**

**EVERYTHING HERE IS IN-SAMPLE BY CONSTRUCTION.** With the box open there is no held-out span left in the cache. The out-of-sample role does not vanish — **it transfers forward to live paper on the Prometheus route (Stage-B interim)**, exactly as the ruling says. Until that line runs, nothing in this document has been tested on data it did not see.

---

## 1 · THE SEAL IS OPEN — what that actually bought

| | |
|---|---|
| the mask | `sealed_mask` returns **False everywhere** — kept in the same shape, not deleted |
| formerly-sealed 4h bars now readable | **13,860** across the panel |
| campaigns quoting an **ANCHOR** from a formerly-sealed bar | **41 of 195** |
| advances quoting a **RATCHET PIVOT** from one | **60**, across 24 campaigns |
| …of which the advance was the **FINAL stop** | **24** — *the exit price came out of the old lockbox* |
| **campaigns quoting ANY formerly-sealed price** | **42** |
| the mask is **live, not decorative** | over Tier-C4's own corridor the same code path yields **11 campaigns box-open and 10 box-closed** |

**Two of those rows exist because the first draft counted only anchors.** An anchor is not the only price this card quotes from a named bar and pays out — **so is a ratchet pivot**, and on 24 campaigns the pivot that came out of the old lockbox *was the stop that closed the trade.* Counting anchors alone understated the build's own box read. §9.

**And the "mask is live" row exists because the first draft's leg could not fail.** Asserting that a constant-false function returns false proves nothing. **Turning the seal back ON and showing the book change** is what proves the ruling is wired to a switch and the switch does something — and F-C5-OPEN now asserts the switch reaches **both** published prices, as Tier-C4 masked both.

**F-C3-a IS CLOSED, AND NOT THE WAY IT WAS ARGUED.** Tier-C3 asked the operator to *ratify the seal floor or overturn it*. The operator did neither: **they removed the seal.** The three-build argument about whether an anchor is a price or a state is settled by not needing an answer.

---

## 2 · THE CARD v5 — one diff, and one rule the card did not name

v5 **is** v4: 4h anchor (800h pin) · rail 1.0 · tide 89/316 · d = 0.75 · 12/26 trigger · LPS-trail (2,2) · creek/ice 50% harvest · bell · net of 10 bps + funding. **The single card diff is `FUNDING_CEILING_R = 1.0` [D12].**

**AND IT NEVER BOUND AT UNIT SIZE. Not once in 195 campaigns.** `S-CLOCK no funding ceiling` reproduces the card **exactly** — paired Δ expectancy 0.000000, tail-exit-ratio 1.0000. *(It does bind above unit size: 2 campaigns at 2×, 4 at 3× — §5.)*

**ONE RULE HAD TO BE ADDED THAT THE CARD DID NOT NAME, AND IT IS NOT COSMETIC: A WARM-UP FLOOR.** Every parent corridor began hundreds of bars after its data did, so the slow EMAs were warm **by traversal** and nobody had to say so. **The full-water corridor starts at each asset's FIRST BAR, and `engine.indicators.ema` SEEDS at the series start rather than returning NaN** — so at bar 0, e12 = e26 = e89 = e316 = the first close, and the card's tide and window gates are evaluable from bar 1 and meaningless. Before the floor, **23 pre-warm armings entered the funnel and 4 became scored campaigns**, the earliest at bar 47 — where the 316-EMA still carries ~74% seed weight. **No arming is admitted before bar 316** (`WARMUP_BARS`, re-pointed from `TIDE_SLOW`). It cost 4 campaigns and the whole of the 2019 slice. Found by the post-build adversarial review; §9.

### F-C5-CTRL — the fork did not drift

**The v4 card, ridden through the v5 code path, reproduces Tier-C4's filed book campaign for campaign**: 11 of 11, **max |net R diff| 4.96e-07** (the 6-dp write rounding of the filed table puts a floor of 5e-07 under any such comparison), 0 exit / advance / harvest mismatches.

**It caught two real bugs on its first run, which is the whole point of having it:** a seal-closed branch that had never been written, and a harvest gate defaulting to `0.0` that imposed an in-profit condition the card never carried — silently suppressing all three of Tier-C4's harvests.

**D13(c) — lead-in trades COUNTED never SCORED — is enacted and is NOT vacuous.** With one unbroken corridor there is no lead-in at its left edge; it binds at every **slice** edge instead. **Three campaigns** (ZEC into 2021, SOL into 2023, NEAR into 2026), all named in `d13c_counted_not_scored.parquet`. Both books printed.

---

## 3 · THE HEADLINE, BY SLICE

> **YARDSTICK v5 — IN-SAMPLE BY CONSTRUCTION** · **2019-09-08 → 2026-08-16 · 5 assets · both directions · 195 campaigns**

| | value |
|---|---:|
| **net R** | **+33.6149** |
| **expectancy / trade** | **+0.1724** |
| win rate | 30.26% (59 of 195) |
| maxDD (R) | 25.5353 |
| tail concentration | **77.14%** |
| best trade · strip-best | **+25.0605** · **+8.5544** |
| gross · fee · funding (R) | +44.8273 · 6.1560 · +5.0563 |

| cut | key | n | net R | expectancy | win % |
|---|---|---:|---:|---:|---:|
| asset | BTCUSDT | 38 | **−3.8077** | −0.1002 | 21.05 |
| asset | ETHUSDT | 46 | +2.4849 | +0.0540 | 28.26 |
| asset | NEARUSDT | 40 | **−2.9840** | −0.0746 | 30.00 |
| asset | SOLUSDT | 35 | +9.7190 | +0.2777 | 37.14 |
| asset | **ZECUSDT** | 36 | **+28.2027** | **+0.7834** | 36.11 |
| direction | long | 92 | +22.4065 | +0.2435 | 29.35 |
| direction | short | 103 | +11.2084 | +0.1088 | 31.07 |
| exit | **stop** | **194** | +34.3907 | +0.1773 | 30.41 |
| exit | bell_12_89 | **1** | −0.7758 | −0.7758 | 0.00 |

**ZEC is 84% of the book** (+28.20 of +33.61); BTC and NEAR are negative over seven years. **A five-asset panel where one asset carries five sixths of the result is a one-asset result with four witnesses.**

**194 of 195 exits are stops. The bell fires ONCE in seven years.** Tier-C4 raised this as F-C4-c on 11 campaigns; at 195 it is settled.

### Per year, with the tide mix — because a slice is unreadable without it

| year | n | net R | expectancy | win % | up / down / neither tide |
|---|---:|---:|---:|---:|---|
| 2019 | **0** | — | — | — | 10.7 / 75.6 / 13.6 *(warm-up)* |
| 2020 | 20 | +10.4432 | +0.5222 | 35.0 | 58.3 / 29.8 / 11.9 |
| 2021 | 34 | −5.8809 | −0.1730 | 26.5 | 63.2 / 25.5 / 11.3 |
| 2022 | 30 | +4.2899 | +0.1430 | 36.7 | 11.7 / 77.0 / 11.3 |
| 2023 | 25 | **−11.7296** | **−0.4692** | 16.0 | 47.5 / 38.9 / 13.5 |
| 2024 | 28 | −2.8221 | −0.1008 | 35.7 | 53.3 / 31.1 / 15.5 |
| 2025 | 40 | +12.1576 | +0.3039 | 30.0 | 37.5 / 49.5 / 13.1 |
| 2026 | 18 | **+27.1569** | **+1.5087** | 33.3 | 25.5 / 58.4 / 16.1 |

**Four of seven scored years lose money.** The card's good years (2020, 2026) had a decisive tide; its worst (2023) the most balanced one. **A hypothesis the table generates, not a result** — nothing here is conditioned on the tide mix and nothing may be without declaring its own m.

---

## 4 · THE REGISTRATIONS — text before result, and all three failed

**THE RULER IS ADOPTED AND DECLARED, NOT ASSUMED.** Neither registration named an acceptance bar. Rather than invent one after seeing the number, the build adopts the estate's standing ruler for a panel claim — **asset-cluster 90% bootstrap CI, unit of replication the ASSET, stat = mean** — declared before scoring. Mean because both registrations are worded about **expectancy**, and expectancy is a mean. **A BUILDER'S READING; the operator should confirm or replace it.**

**AND THE ARM NAMED "vs card" IS TESTED AGAINST THE CARD.** The first draft tested the union's expectancy against **zero** while calling the arm "vs card" — and reported it SUPPORTED. It is not. Corrected, the union is scored by a **two-sample asset-cluster bootstrap resampling the same asset draw into both books**. §9.

| registration | arm | prior | n | expectancy | net R | ruler | CI | p (1-sided) | **verdict** |
|---|---|---:|---:|---:|---:|---|---|---:|---|
| *(reference)* | **THE CARD v5, same ruler** | — | 195 | +0.1724 | +33.61 | own exp. vs 0 | [−0.0271, **+0.4336**] | 0.0912 | **NOT SUPPORTED** |
| **P-SPR-1** | standalone spring lane | 55% | 241 | +0.0882 | +21.26 | own exp. vs 0 | [−0.0373, +0.2389] | 0.1397 | **NOT SUPPORTED** |
| **P-SPR-1** | card+spring UNION **vs card** | 55% | 420 | +0.1204 | +50.57 | **union − card** | [−0.2583, +0.0655] | 0.6718 | **NOT SUPPORTED** |
| **P-CASC-1** | card+adds vs card (PAIRED) | 50% | 195 | +0.3185 | +62.11 | paired Δ vs 0 | [−0.0100, +0.2532] | 0.0572 | **NOT SUPPORTED** |

**READ THE REFERENCE ROW FIRST.** The bar every arm is held to is one **the card itself does not clear**. That is not an argument that the arms should be excused — it is the context without which the table cannot be read.

**P-SPR-1 union — the corrected verdict, and how far it moved.** The union runs 420 campaigns (+225 over the card) for +50.57 R (+16.96). **Per campaign it is WORSE than the card: −0.0520 R.** Against zero it would still clear (lower bound +0.0148, printed on the row so both readings are visible); **against the card, which is what it is named against, it is nowhere near.** The union's apparent strength was never edge — it was **n rising 2.2× and narrowing the interval.**

**P-CASC-1 — the way it fails is the interesting part.** The adds add **+28.50 R** across **60 campaigns carrying 117 adds**, a paired delta of **+0.1461 R per campaign** — not small. But the **asset-cluster** CI straddles zero and the drop-largest check halves the point estimate. **A panel claim is a claim about replication, and this one is a claim about one or two campaigns.**

**FDR: APPLIED, NOT MERELY RECORDED. m = 3 — the number of acceptance tests ACTUALLY RUN, not the 2 registrations filed.** Two registrations produced three tests (P-SPR-1 was scored twice), and a family counting filings gives the second bite of the same apple a free pass. q = 0.10, **bar = q/m = 0.03333**. **No arm clears it** (0.1397, 0.6718, 0.0572). The first draft asserted *"a CI cannot be BH-corrected without inventing a p"* — **that was wrong**: the same bootstrap that produces the interval produces the one-sided tail. §9.

### The robustness block — three checks, every arm, through the arm's own ruler

`registration_robustness.parquet`. **LEAVE-ONE-ASSET-OUT** (replication), **DROP THE LARGEST CAMPAIGN** (a tail-heavy book can carry an interval on one trade), **SEED SENSITIVITY** (a verdict on a bootstrap's fourth decimal could be a verdict about a seed).

**LOAO scores: standalone spring 1 of 5 · union 1 of 5 · adds 1 of 5.** In each case the one panel that excludes zero is the one with **ZEC dropped**. **ZEC is 84% of the card's book AND the asset whose removal flips every arm** — one asset is doing two contradictory jobs in this panel, and that is a fact about the panel, not about the lanes.

*(The block scores each arm through the ruler its verdict used. The first draft scored the union against zero here while the verdict scored it against the card — the table would have "confirmed" a verdict it had never tested.)*

---

## 5 · THE SHADOW FLEET, IN FULL

**UNSCORED. Every cell pre-named, every cell reported, none promoted.**

| grid | cell | n | net R | expectancy | win % | maxDD | **paired Δexp** | **tail-exit ratio** | **max 1-trade Δ share** |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **card** | **v5** | 195 | **+33.6149** | **+0.1724** | 30.26 | 25.54 | — | 1.0000 | — |
| S-RAIL | 1.25 | 195 | +22.6914 | +0.1164 | 30.77 | 25.83 | −0.0560 | 0.8804 | 0.4588 |
| S-RAIL | 1.5 | 195 | +19.1925 | +0.0984 | 31.79 | 24.78 | −0.0740 | 0.7899 | 0.5792 |
| S-HARV | fixed +2R | 195 | **+14.7445** | +0.0756 | 34.36 | 24.55 | −0.0968 | **0.6708** | 0.6121 |
| S-HARV | in-profit-only (≥+1R) | 195 | +27.8766 | +0.1430 | 30.77 | 27.48 | −0.0294 | 1.0000 | 0.1296 |
| S-CLOCK | 60-bar time stop | 195 | +36.1264 | +0.1853 | 30.26 | 26.35 | +0.0129 | 1.0172 | 0.6367 |
| S-CLOCK | **no funding ceiling** | 195 | **+33.6149** | +0.1724 | 30.26 | 25.54 | **0.0000** | **1.0000** | — |
| S-TRAIL | (3,3) pivots | 195 | +21.5535 | +0.1105 | 28.21 | **33.46** | −0.0619 | 0.9638 | 0.3521 |
| S-TRAIL | **+0.25 ATR buffer** | 195 | **+69.2027** | **+0.3549** | 27.69 | **16.28** | **+0.1825** | **1.3383** | **1.1562** |
| S-TRAIL | arms after +1R | 195 | +39.9201 | +0.2047 | 34.36 | 27.41 | +0.0323 | 1.0059 | 0.4833 |

**READ THE LAST COLUMN BEFORE THE THIRD.** `S-TRAIL +0.25 ATR buffer` doubles the book and cuts drawdown by a third — and its **max single-trade share of delta is 1.1562, GREATER THAN ONE.** The per-campaign deltas partly cancel and **one campaign's improvement exceeds the entire net improvement.** The +35 R is one trade plus noise. **This is exactly the column D15 exists for, and it fires on the fleet's most attractive cell.**

**`S-HARV in-profit-only` fires ZERO harvests** — every band-touch harvest in this book is adverse at the fill, so requiring ≥+1R kills all 37. A clean natural experiment: **removing the de-risk costs −5.74 R**, which is the harvest lab's number to the decimal.

### S-SIZE — re-capped per size, not scaled

| unit | net R | maxDD R | **ceiling bound n** | max concurrent | R / year | return ÷ maxDD |
|---:|---:|---:|---:|---:|---:|---:|
| 1.0 | +33.6149 | 25.5353 | **0** | 3 | 4.85 | 1.3164 |
| 1.5 | +50.4224 | 38.3030 | **0** | 3 | 7.27 | 1.3164 |
| 2.0 | +67.7310 | 51.0707 | **2** | 3 | 9.76 | **1.3262** |
| 3.0 | +103.2790 | 76.4169 | **4** | 3 | 14.89 | **1.3515** |

**`return ÷ maxDD` is NOT constant, and that is the point.** The first draft scaled the unit-1 book by `s` and asserted exact linearity — **which was false, because D12 caps funding at an ABSOLUTE 1R while funding in R scales with the unit.** Scaling a capped book silently converts a 1R ceiling into an s×1R ceiling. Each size is now re-accounted from gross, fee and **uncapped** funding, and `ceiling_bound_n` says how often the cap caught: **0, 0, 2, 4.** §9.

**The genuinely measured column is `max concurrent campaigns = 3`** — over seven years, one-position-per-asset across five assets never had more than three open at once. **This is not a leverage study:** no margin, no liquidation, no compounding.

### S-ADDSIZE

| add tranche | campaigns w/ adds | adds | net R | maxDD R | add R | paired Δexp | max 1-trade Δ share |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1.0× | 60 | 117 | +62.11 | 42.10 | +28.50 | +0.1461 | 0.6304 |
| 1.5× | 60 | 117 | +76.53 | 51.39 | +42.74 | +0.2201 | 0.6279 |
| 2.0× | 60 | 117 | +91.07 | 61.38 | +56.99 | +0.2946 | 0.6253 |
| 3.0× | 60 | 117 | +120.15 | 81.37 | +85.49 | +0.4438 | 0.6227 |

**Net R nearly quadruples and so does the drawdown.** The max-single-trade share sits at ~0.63 at every size: **the same one campaign dominates however big the tranche.** Size does not fix replication.

### S-LIMIT — the AE study first, then the limits

**The AE study is the durable output of this whole grid.** Per WINNER, the deepest adverse excursion in R from entry until +1R is first reached:

| population | winners | reaching +1R | **mean AE** | median | p90 | max |
|---|---:|---:|---:|---:|---:|---:|
| **TC-BOOK** (whole v5 book) | 59 | 58 | **0.3105 R** | 0.2782 | 0.6391 | 0.9931 |
| **CENSUS-ERA** (entries pre-2024-07-01) | 36 | 35 | **0.3145 R** | 0.2756 | 0.6572 | 0.9013 |

**The two eras agree to four thousandths of an R.** Over 2,534 days and two regimes, **a winner goes about 0.31 R against you before it goes 1 R for you, and the p90 is 0.64 R.** That is the most stable number in this build.

*(A NAMED READING: "census winners" is **this card's** winners in that era, not CENSUS-2A's filed ride-only book, which rode a different card, ruler and denominator and is not comparable.)*

| k × avg-AE | offset (R) | filled | **missed** | **miss rate** | net R | expectancy | maxDD R |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.50 | 0.155 | 177 | 18 | **9.23%** | **+27.43** | +0.1549 | 25.94 |
| 0.75 | 0.233 | 169 | 26 | **13.33%** | +26.88 | +0.1591 | 28.88 |
| 1.00 | 0.310 | 158 | 37 | **18.97%** | +19.08 | +0.1208 | 36.23 |
| 1.50 | 0.466 | 139 | 56 | **28.72%** | +26.45 | +0.1903 | 25.38 |
| 2.00 | 0.621 | 124 | 71 | **36.41%** | +5.99 | +0.0483 | 18.13 |

**MISS RATE IS FIRST-CLASS AND IT IS THE COLUMN THAT MATTERS.** Net R is **non-monotonic** in k — 27.4, 26.9, 19.1, 26.5, 6.0 — the signature of noise, not a mechanism. **No level beats the card, and `avg-AE` is fitted on the very book the levels are scored against.** In-sample twice over, logged in the selection surface.

**AN OVERLAY, NOT A RE-RUN:** each level rides the card's own campaign set; a level that never fills books a MISS rather than freeing the slot. **And the ride now tests the stop on the FILL BAR** — a limit fills mid-bar, so the rest of that bar is real tradeable time, and discarding it gave every cell a free bar of immunity. §9.

---

## 6 · THE THREE LABS

### 6.1 THE HARVEST LAB — **H1**

| | |
|---|---:|
| harvests | **37** |
| **helped** (took > would-have) | **32 of 37** |
| took (sum) | −9.1743 R |
| would-have (sum) | −14.9127 R |
| **delta** | **+5.7383 R** |

**BOTH COLUMNS ARE NEGATIVE, AND THAT IS THE ANSWER TO H1.** The creek/ice harvest is **not a profit-take — it is a de-risk**, every time. It fires when price rallies back into the band against the position, so the half it takes is *always* taken at a loss; it earns its keep because **the loss it takes is smaller than the loss the runner goes on to book.** Positive in **every slice**: pre-wall +2.85, post-wall +2.89, the sealed span +1.03, the refresh +1.85, and every year it fires in. **The most consistent thing in this build — 17% of the result, from a rule that never once banked a gain.**

### 6.2 THE RESISTANCE LEAGUE — **H2 / H7** (Tier-E, 2025-10-01 → latest)

15 EMAs × 4 TFs × 5 assets; 313 rows filed. **APPROACH** = the bar's high comes within 0.25 ATR of the EMA **from below**; **REJECTION** = no close above within 3 bars.

| TF | **champion wall** | approaches | rejection rate | mean penetration (ATR) | longest rejected streak | chosen from |
|---|---:|---:|---:|---:|---:|---:|
| **12h** | **EMA 889** | 59 | **62.71%** | 0.439 | 11 | 13 cells |
| **1d** | **EMA 889** | 42 | **61.90%** | 0.287 | 9 | 11 cells |
| **4h** | EMA 3618 | 109 | 52.29% | 0.502 | 6 | 15 cells |
| **1h** | EMA 4618 | 304 | 48.36% | 0.495 | 14 | 15 cells |

**EMA 889 is the champion on BOTH slow clocks, independently.** The league's floor is as informative: **12h EMA 316 rejects only 23.88%** — and 316 is the estate's own tide-slow EMA. **The card's tide line is, on the 12h clock, the weakest wall in the league.**

**THE CHAMPION IS A NAMED MAXIMUM, NOT A PROMOTION**, and the row says so: an argmax over the eligible panel cells for its timeframe, **no acceptance bar, no interval, no multiplicity correction.** The **54 eligible cells it is chosen from are now in the logged selection surface** — they were not in the first draft, which is how an argmax over 54 uncounted cells came to be called the build's strongest Tier-E result. §9.

### 6.3 MID-BAND CONFLUENCE (Tier-E)

| tf | event | n | H20 net bps | H100 net bps | event-hits | **distinct v5 exits** | mean net R of those exits |
|---|---|---:|---:|---:|---:|---:|---:|
| 1h | price_x_127 | 1811 | +0.27 | −6.06 | 35 | **21** | −0.007 |
| 1h | price_x_200 | 1463 | −0.88 | −16.63 | 39 | **18** | −0.553 |
| 1h | price_x_300 | 1096 | −0.54 | −6.24 | 26 | **18** | −0.705 |
| 4h | price_x_127 | 399 | −12.58 | +45.18 | 22 | **12** | −0.704 |
| 4h | price_x_300 | 274 | +14.31 | +22.48 | 2 | **1** | −0.302 |
| **4h** | **cross_316_423** | **10** | +104.0 | **+2630.0** | 1 | **1** | +6.179 |

**THE BOTTOM ROW IS NOISE AND IS PRINTED AS NOISE.** n = 10, one distinct exit. A +2,630 bps forward mean on ten events is one move. **The rows worth anything have n in the hundreds, and there the forward edge is single-digit-to-low-double-digit bps against a 10 bps toll — i.e. nothing.**

**The co-occurrence half is negative and now honestly weighted.** The first draft computed a **triple mean-of-means over a recycled handful of exits** and published it under a column name claiming a statistic over EXITS. **`distinct_v5_exits_touched` is now a column**, and it shows the recycling directly: 39 event-hits on `1h price_x_200` resolve to **18** distinct exits; two 4h rows resolve to **one**. Where the count is real, **v5 exits coinciding with mid-band traffic are v5's bad exits** (−0.55, −0.70, −0.70, −0.73). **A hypothesis with a table behind it and no m declared.**

---

## 7 · THE INTERVIEW HOOKS H1–H7 — and the two that do not exist

| hook | what the paste names it | table |
|---|---|---|
| **H1** | harvest-vs-ride | `harvest_lab` — §6.1 |
| **H2** | resistance / walls | `resistance_league` — §6.2 |
| **H3** | **NOT DEFINED ANYWHERE** | — |
| **H4 / H5** | the S-TRAIL lab | `fleet_unscored` S-TRAIL rows — §5 |
| **H6** | **NOT DEFINED ANYWHERE** | — |
| **H7** | resistance / walls | as H2 |

**H3 AND H6 HAVE NO DEFINITION IN THE ESTATE OR IN THE PASTE, AND NEITHER DOES THE D-BLOCK THEY COME FROM.** A search of every branch finds `D1–D15` in exactly one place — `APOLLO_LANE_STATUS_2026-08-15.md:37-41` — which names four block titles and a count, defines not one item, and lists the interview as work **to be run**. `D12`, `D13`, `D15` and `H1`–`H7` appear nowhere else as content. **This build enacts D12, D13(c) and D15 solely because the operator's paste says what they are.** That is legitimate — a paste is a ratification — but the labels have no estate anchor.

**The estate has ruled on exactly this shape before.** `BUILD_2026-08-15_VIZ2_CATHEDRAL.md:52`, finding V-6: *"`fuzz` has no anchor in the estate — zero hits repo-wide… **Ruling needed, or drop the word.**"* — and `fuzz` is named in the **same sentence** as D1–D15.

---

## 8 · FINDINGS — NOT FIXED

**F-C5-a · THE 118-DAY YARDSTICK WAS A QUARTER OF ONE REGIME.** Expectancy +0.6907 → **+0.1724**; the first 1,757 days lose −7.27 R over 123 campaigns; every R is post-2024-07-01. **Ruling needed: which number is the yardstick a multiplier must beat?** Three candidates — +0.6907 (118 sealed days), +0.1724 (2,534 open ones), +1.1964 (the operator's 29) — differing by a factor of seven.

**F-C5-b · THE CARD ITSELF DOES NOT CLEAR THE ESTATE'S OWN BAR.** Scored through the same asset-cluster ruler as the registrations, the card's expectancy CI is **[−0.0271, +0.4336]**, one-sided p = 0.0912. **On seven years, five assets and 195 campaigns, this card is not distinguishable from zero at q = 0.10.** **Ruling needed, and it is the deepest one in this document: is the card an edge that is hard to measure, or a coin that has been flipping heads?**

**F-C5-c · ONE ASSET IS 84% OF THE BOOK, AND IT IS THE ASSET EVERY LOAO TURNS ON.** ZEC +28.20 of +33.61; BTC and NEAR negative over seven years; and **dropping ZEC is the single leave-one-out that flips every registration arm to excluding zero.** F-C3-d asked whether one-trade dominance at n = 11 was acceptable; **at n = 195 the concentration moved from one trade to one asset and got worse.**

**F-C5-d · D12 IS INERT AT UNIT SIZE AND LIVE ABOVE IT.** The funding ceiling bound on **0 of 195** at unit 1, **2 at 2×, 4 at 3×**. **Not a defect — a rule that costs nothing and buys nothing at the size the card is scored at.** **Ruling needed: keep it as insurance, or strike it.**

**F-C5-e · THE BELL FIRES ONCE IN SEVEN YEARS.** 194 of 195 exits are stops. **Ruling needed: backstop expected never to fire, or dead law to be struck from the card?**

**F-C5-f · THE FLEET'S MOST ATTRACTIVE CELL FAILS ITS OWN D15 COLUMN.** `S-TRAIL +0.25 ATR buffer` posts +69.20 against +33.61 and cuts maxDD by a third — with **max single-trade share of delta 1.1562, greater than one.** **The number is real and the mechanism is one trade.** Named loudly because this is the cell that gets promoted if nobody reads the last column.

**F-C5-g · S-LIMIT'S avg-AE IS FITTED ON THE BOOK IT IS SCORED AGAINST.** Net R is non-monotonic in k and **no level beats the card.** The **AE study itself is the durable output** (0.3105 R whole-book vs 0.3145 R census-era, agreeing to four thousandths); the grid on top of it is a selection surface with five cells and no held-out anything. **Not fixed: the honest fix — fit avg-AE on one era, score limits on another — is a new probe with its own m.**

**F-C5-h · THE INTERVIEW'S D-BLOCK AND HOOKS H3, H6 HAVE NO SOURCE.** §7. **Ruling needed: define D1–D15 and H1–H7 in the estate, or strike the labels and cite the pastes directly.** Precedent V-6, same sentence, same shape.

**F-C5-i · THE SPRING LANE'S TIDE READING REFUSES 3,526 SWEEPS AND ADMITS 241.** *"Closing back inside ≤3 bars, tide-aligned"* is read as: **THE reclaim is the FIRST close back inside, and the tide must agree AT IT.** The alternative — keep looking through the window for a later inside close whose tide agrees — is a different lane and is **not taken**. **The reading costs a 14:1 refusal ratio, is now counted, and needs a ruling.** Counts only; no R attached to either reading.

**F-C5-j · TIER-C4's `Trade` DOCSTRING IS NOW FALSE AND THIS BUILD DID NOT EDIT IT.** `scripts/tierc4_rules.py:475-479` justifies the no-outcome rule *"because … for the SCORED window that bar is sealed"*. The seal is open. **Not fixed — this build does not edit a predecessor's code** — but a stale justification in a parent that four generations import is a real rot risk.

**F-C5-k · THE LIVE PAPER LINE IS THREE CARD VERSIONS BEHIND, AND THE RULING JUST MADE IT THE OUT-OF-SAMPLE INSTRUMENT.** `configs/tierc2_paper.yaml` and `research_outputs/tierc2/heartbeat.json` still enact **v1**. F-C3-g raised this as housekeeping; **with out-of-sample transferred forward to the Prometheus route, the forward line IS the reserve, and it is running a card four generations old. This moves from housekeeping to BLOCKING.**

**F-C5-l · CARRIED.** **F-C3-a CLOSED by ruling.** Still open: F-C3-b (the Tier-C3 name), **F-C3-c** (the anchor lookback, bars vs hours — untouched, still 200 bars = 800 h), F-C3-e (two rails), F-C4-b (the trail's "beyond"), F-C4-i (the "new pivot" gate on the confirmation bar). **Card m = 0; the logged surface is 79 and it was written before the look.**

---

## 9 · FIXTURE TRANSCRIPT, AND THE REPAIRS THAT PRECEDED IT

**11/11 PASS**, exit 0. **F-C4-h's convention is adopted as the house rule: every leg states, inline, what would have to be true for it to FAIL.**

### THE REPAIRS — a seven-lens adversarial review, run BEFORE publication

Tier-C3's seal breach was found *after* its draft was published; Tier-C4 moved the audit before publication and repaired twelve findings. This build did the same at larger scale. **Sixteen findings were acted on. Two changed a headline number; one reversed a verdict.**

| # | what was wrong | what changed |
|---|---|---|
| 1 | **The P-SPR-1 union arm was named "vs card" and scored against ZERO.** With 2.2× the card's campaigns a narrower interval passed while the union was per-campaign *worse* than the card | scored by a **two-sample asset-cluster bootstrap, union − card**. **Verdict reversed: SUPPORTED → NOT SUPPORTED.** The vs-zero reading is printed beside it |
| 2 | **The card was never scored through its own bar**, so no reader could tell what the bar was worth | a **reference row** — **NOT SUPPORTED** (F-C5-b) |
| 3 | **FDR declared m = 2 (registrations filed) while 3 tests ran**, and the build claimed a CI could not be BH-corrected | **m = 3, bar 0.0333, CORRECTION APPLIED** — the bootstrap yields the tail, so no p was invented |
| 4 | **No EMA warm-up.** `ind.ema` seeds at the series start, so at bar 0 every EMA equals the first close; 23 pre-warm armings and 4 scored campaigns entered on seeded EMAs | **`WARMUP_BARS = 316`**; cost 4 campaigns and the whole 2019 slice |
| 5 | **The spring's `sweep_extreme` omitted the reclaim (entry) bar**, putting the stop inside a price the entry bar had already traded on 8 of 246 campaigns | the reclaim bar's extreme folded into the anchor |
| 6 | **S-LIMIT never tested the stop on the fill bar.** A limit fills mid-bar; the rest of that bar is real | `_ride` gains an entry-bar stop test for limit fills |
| 7 | **S-SIZE scaled a capped book** — D12 caps funding at an *absolute* 1R, so scaling converted it to s×1R and the "exactly linear" claim was false | **re-capped per size**; `ceiling_bound_n` = 0, 0, 2, 4 and `return ÷ maxDD` is no longer constant |
| 8 | **`tail_exit_ratio` divided top-decile SUMS**, so it scaled with n — harmless on the fleet, load-bearing on the registration rows where n differs | **MEAN of the top decile**, n-invariant |
| 9 | **Mid-band co-occurrence was a triple mean-of-means over recycled exits**, published as a statistic over EXITS | **distinct exits counted and reported**; panel rows n-weighted |
| 10 | **League panel rows pooled approaches but averaged penetration unweighted** — two populations on one row | approach-weighted |
| 11 | **`is_champion_wall` was an unadjusted argmax over 54 cells absent from the logged surface** | **the 54 cells added** (25 → 79); the row states it is a named maximum, not a promotion |
| 12 | **The ratchet's seal call site was deleted, not answered** — `seal_open=False` restored only the entry-anchor mask, while Tier-C4 masked both published prices | `forbidden` threaded through `trail_step` |
| 13 | **The build counted sealed ANCHORS and not sealed RATCHET PIVOTS**, understating its own box read | **60 advances / 24 campaigns / 42 campaigns quoting ANY sealed price** now counted and asserted (§1) |
| 14 | **F-C5-GRID compared the built cards with the table written from the built cards** — the same object counted twice | an **independent literal `GRID_SIZES`**; three things must now agree |
| 15 | **Three F-C5-OPEN legs could not fail**, including asserting a constant-false function is constant-false | a **live mask test** (11 campaigns open vs 10 closed) and the **first sealed bar this build actually QUOTES** |
| 16 | **F-C5-SPRING's picks were direction-blind and all landed on longs**; F-C5-LEAGUE rescanned the largest-population row, never a champion | picks forced direction-aware; the league rescans **champion** EMAs |

**Two findings were checked and NOT acted on, and they are findings rather than repairs: F-C5-i** (the spring's tide reading — a named reading, now counted at 3,526 refusals) and the observation that **the champion-wall re-check in F-C5-LEAGUE is an argmax compared with its own max and cannot fail** — retained, printed for the reader, and **explicitly labelled as not evidence.**

| fixture | verdict | evidence — and its failure condition |
|---|---|---|
| **F-C5-OPEN** | PASS | Ruling verbatim. **THE MASK IS LIVE**: over Tier-C4's corridor the same code path yields **11 campaigns box-open vs 10 box-closed**, and the switch reaches **both** published prices. 41 sealed anchors, 60 sealed ratchet pivots, **42 campaigns quoting any sealed price**, and the first one the card actually quotes named. **FAILS IF** the two campaign counts are equal, or the union is smaller than the anchor count. |
| **F-C5-CTRL** | PASS | 11 of 11, **max \|net R diff\| 4.96e-07 ≤ 1e-05**, 0 exit/advance/harvest mismatches. **It caught two real bugs on its first run.** |
| **F-C5-INHERIT** | PASS | 15 identities with `is`, three generations deep; the parameterised fractal builder proved to reduce to Tier-C4's at (2,2) on every asset's full history; the ribbon map asserted equal to the estate's. |
| **F-C5-RAIL** | PASS | 195 entry stops meet the rail; **273 advances**, min distance from the confirming close **1.000000 × ATR**; monotonicity across whole campaigns, 0 retreats. |
| **F-C5-HARV** | PASS | The harvest rule re-derived from raw bars on **all 195** campaigns — 0 disagreements — partition exhaustive. Halves-sum **named as the algebraic tautology it is**. |
| **F-C5-SPRING** | PASS | Three signals from raw bars, **direction-aware** so the mirrored branch is verified too: the prior 96-bar extreme strictly before the sweep, the sweep taking it out, the reclaim a CLOSE within 3 bars, the tide, entry = reclaim close, stop beyond the sweep extreme railed. |
| **F-C5-GRID** | PASS | The manifest's surface asserted equal to an **independent literal**, then both against the written tables: **79 declared before the run == 79 written.** |
| **F-C5-LEAGUE** | PASS | Each timeframe's **champion** EMA rescanned from raw bars on its largest contributor. **FAILS IF** an approach is counted from ABOVE. The champion re-check is labelled as an argmax that cannot fail. |
| **F-C5-DET** | PASS | **All 21 content hashes identical**, counts block identical, seal record identical, **corridor edges identical**. The wall clock is **out of the written table** — determinism that has to be excused is not determinism. |
| **F-C5-6** | PASS | AST import scan of **four** decision modules; transitive closure; tape column names scanned over **CODE, not text**. **It fired once**, on a `Spring` field named `prior_extreme` — a tape family name — renamed `swept_level`. |
| **F-KEY** | PASS | 21 tables, 0 duplicates; headline reconciles to the journal; ratchet ledger reconciles to advance counts; asset and direction cuts sum to ALL; **the year slices and the pre/post split each PARTITION the book** (195 == 195). |

**Suite:** `pytest fixtures tests -m "not slow"` → **333 passed, 1 skipped, 1 deselected, exit 0**. `grep -rl "tierc5" tests fixtures` returns nothing.

---

## 10 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/tierc5_rules.py` · `tierc5.py` · `tierc5_fixtures.py` | **new** — decision path, program, transcript |
| `research_outputs/tierc5{,_run2}/` | **built** — 21 parquet + manifest, local, gitignored |
| `.gitignore` | **modified** |
| **THE SEAL** | **OPEN by ruling** — 13,860 bars freed, **42 campaigns quote a formerly-sealed price**, **F-C3-a closed** |
| THE YARDSTICK | **+0.1724 R / trade over 195 campaigns, 2,534 days — IN-SAMPLE BY CONSTRUCTION** |
| THE REGISTRATIONS | **scored, ALL THREE NOT SUPPORTED** — and so is the card, printed as a reference |
| THE FLEET | **79 logged cells, all reported, none promoted** |
| THE LABS | **three, filed** — harvest (H1), league (H2/H7), mid-band |
| THE REVIEW | **run BEFORE publication** — seven lenses, **16 repairs**, one verdict reversed, two headline numbers changed |
| OUT-OF-SAMPLE | **transfers forward** to live paper, Prometheus route — **not built here, and now blocking (F-C5-k)** |
| `engine/` · `analytics/` · `scripts/tierc{2,3,4}_*` | **UNTOUCHED** — zero diff |

### BOX-COST

`exchange/**` measured **3,046,085 B = 19.04%** before this paste; the governing **tick set** **3,305,383 B = 20.66%** — state **OK** (warn 40% / refuse 70%). Constants read live from `publish_exchange`, not typed.

**This paste adds this document (45,902 B) plus the `LEDGER_APOLLO` append (6,105 B) = 52,007 B = 0.325% of the box** — **65% of the < 0.5% target**, against Tier-C4's 92%. The fixture transcript, the 3,118-row tape, the 313-row league, the 108-row mid-band table, the 195-row journal and the robustness block stay **local**.

**No file in this paste crosses the 64,000 B naming trip-wire.**

---

## 11 · THE LEDGER_APOLLO APPEND

```
=== STATUS_APOLLO — 2026-08-16c ===
NOW: TIER-C5 IS MEASURED, THE BOX IS OPEN, AND NOTHING WAS SUPPORTED.
RULING, VERBATIM: "open the sealed box, we lose continuity otherwise… we will
     put it to paper trade the Prometheus route… another data stream" ·
     "D15 caveats not hard gates"
     THE YARDSTICK LINEAGE, ALL FOUR, STATED TOGETHER:
       v1  TIER-C2  1H anchor, no rail       -0.7762 R/trade  n=10   118 d SEALED
       v3  TIER-C3  4h anchor + 1.0 rail     +0.7056 R/trade  n=11   118 d SEALED
       v4  TIER-C4  + LPS-trail + harvest    +0.6907 R/trade  n=11   118 d SEALED
       v5  TIER-C5  + funding ceiling 1R     +0.1724 R/trade  n=195  2534 d OPEN
     THE 118-DAY NUMBER WAS NOT WRONG, IT WAS SMALL. Every R is post-2024-07-01:
     pre-wall -7.2687 over 123, post-wall +40.8836 over 72. The operator's own
     post-lockbox read is +1.1964 over 29 — PROVISIONAL, and the best slice in
     the book by a factor of seven.
     *** AND THE CARD ITSELF DOES NOT CLEAR THE ESTATE'S OWN BAR. *** Scored
     through the same asset-cluster ruler as the registrations, the card's
     expectancy CI is [-0.0271, +0.4336], one-sided p 0.0912. On seven years,
     five assets and 195 campaigns this card is not distinguishable from zero
     at q = 0.10. That is F-C5-b and it is the deepest ruling in the document.
     EVERYTHING IS IN-SAMPLE BY CONSTRUCTION. Out-of-sample transfers FORWARD to
     live paper on the Prometheus route (Stage-B interim), which is NOT BUILT.
SEAL: 13,860 formerly-sealed 4h bars readable. 41 campaigns quote an ANCHOR from
     one; 60 ADVANCES quote a RATCHET PIVOT from one, and on 24 campaigns that
     advance is the FINAL stop — the EXIT PRICE came out of the old lockbox. 42
     campaigns quote ANY formerly-sealed price. THE MASK IS PROVED LIVE, not
     merely constant-false: over Tier-C4's corridor the same code path yields 11
     campaigns box-open and 10 box-closed. F-C3-a IS CLOSED — the operator did
     not ratify the seal floor, they removed the seal.
REGISTRATIONS (text before result; ruler DECLARED before scoring — asset-cluster
     90% CI, MEAN; a BUILDER'S READING the operator should confirm):
       (reference) THE CARD v5    n=195  exp +0.1724  CI [-0.0271,+0.4336] NOT SUPPORTED
       P-SPR-1 standalone spring  n=241  exp +0.0882  CI [-0.0373,+0.2389] NOT SUPPORTED
       P-SPR-1 UNION vs CARD      n=420  d   -0.0520  CI [-0.2583,+0.0655] NOT SUPPORTED
       P-CASC-1 card+adds PAIRED  n=195  d   +0.1461  CI [-0.0100,+0.2532] NOT SUPPORTED
     THE UNION VERDICT WAS REVERSED IN REVIEW. The first draft named the arm
     "vs card" and scored it against ZERO; with 2.2x the card's campaigns a
     narrower interval passed while the union was per-campaign WORSE than the
     card (-0.0520 R). FDR: m = 3 (tests RUN, not registrations FILED), q = 0.10,
     bar 0.03333, CORRECTION APPLIED — the bootstrap yields the tail, so no p
     was invented. No arm clears it.
     LOAO: 1 of 5 on every arm, and in each case the panel that excludes zero is
     the one with ZEC DROPPED. ZEC is 84% of the card's book AND the asset whose
     removal flips every arm.
FLEET: 79 LOGGED CELLS (25 shadow across 8 pre-named grids + 54 eligible league
     cells a champion is argmaxed from), ALL REPORTED, NONE PROMOTED. D12 bound
     0 of 195 at unit size, 2 at 2x, 4 at 3x. S-TRAIL +0.25 ATR posts +69.20 vs
     the card's +33.61 and its D15 max-single-trade-delta-share is 1.1562 —
     GREATER THAN ONE: one campaign exceeds the whole net improvement.
LABS: H1 — the harvest is a DE-RISK, never a profit-take: 37 fills, both took
     (-9.1743) and would-have (-14.9127) NEGATIVE, delta +5.7383 R, positive in
     EVERY slice. H2/H7 — the champion wall is EMA 889 on BOTH 12h (62.7%) and
     1d (61.9%); the estate's own tide-slow EMA 316 is the WEAKEST wall on 12h
     at 23.9%. AE STUDY, the most stable number here: a winner goes 0.3105 R
     against you before it goes 1 R for you, and the census era agrees at
     0.3145 — four thousandths apart across two regimes.
REVIEW: seven adversarial lenses run BEFORE publication. 16 REPAIRS. Two changed
     a headline number (an EMA WARM-UP FLOOR the full-water corridor needed and
     no parent did — `ind.ema` SEEDS at the series start, so 23 pre-warm armings
     and 4 scored campaigns had ridden on EMAs that were all the same number;
     and S-SIZE re-capped because D12's 1R cap does not scale). One REVERSED A
     VERDICT. Five fixture legs that could not fail were replaced.
FIXTURES: 11/11 PASS. F-C4-h's convention is the HOUSE RULE from here — every
     leg states what would make it FAIL.
PENDING (operator): 8 rulings, all in section 8 —
     F-C5-a  WHICH NUMBER IS THE YARDSTICK? +0.6907 / +0.1724 / +1.1964, 7x apart
     F-C5-b  THE CARD DOES NOT CLEAR THE ESTATE'S OWN BAR on 195 campaigns.
             Edge that is hard to measure, or a coin that flipped heads?
     F-C5-c  ONE ASSET IS 84% OF THE BOOK and flips every LOAO. Same ruling F-C3-d awaits
     F-C5-d  D12 inert at unit size, live above it — keep as insurance or strike
     F-C5-e  THE BELL FIRES ONCE IN SEVEN YEARS — backstop or dead law
     F-C5-g  S-LIMIT's avg-AE is fitted on the book it is scored against
     F-C5-h  D1-D15 AND H1-H7 HAVE NO SOURCE. H3 and H6 have no content at all.
             Define them or strike the labels (precedent V-6)
     F-C5-i  THE SPRING'S TIDE READING refuses 3,526 sweeps and admits 241.
             Pin "the reclaim is the FIRST inside close" or open the window
     F-C5-k  *** THE LIVE PAPER LINE IS THREE CARD VERSIONS BEHIND AND THE
             RULING JUST MADE IT THE OUT-OF-SAMPLE INSTRUMENT. This moves from
             housekeeping to BLOCKING. ***
     -- also filed: F-C5-f (the fleet's best cell fails its own D15 column),
     F-C5-j (Tier-C4's Trade docstring is falsified by the open seal),
     F-C5-l (F-C3-b/c/e, F-C4-b/i carried).
PROBE LEDGER: card m = 0. LOGGED SELECTION SURFACE 79, written BEFORE the look.
     EXPLORATION — ungated; promotion requires registration and declares its m.
=== END STATUS ===
```

---

*End of build document. TIER-C5 · full water · the box is open · 2,534 days · 195 campaigns · every grid reported whole and none promoted · nothing supported, including the card · in-sample by construction, and the out-of-sample is forward from here.*
