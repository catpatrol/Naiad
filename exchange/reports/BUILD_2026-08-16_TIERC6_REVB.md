# BUILD — TIER-C6 rev B · ARMED TRAIL + WALLS + ZEC FORENSICS + THE LIMIT FRONTIER

**Lane** APOLLO · **Branch** `v12-v1-census` · **Drafted** APOLLO · **Executor** HEPHAESTUS · **Seed** 20260816

**RATIFIED** operator 2026-08-16 — the H-rulings, *"understand WHY ZEC"*, *"better/tighter limit entries, find the n×ATR sweet spot"*, and the F-C5-a…i words as recorded that turn. **Supersedes rev A in full; rev A never ran.**

**CLASS — measurement + registrations + pre-named labs.** D15 columns everywhere, **gates nowhere**. Every grid reported whole. Every fixture leg states its failure condition.

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**The card got better and it still cannot clear its own bar.**

Card v6 posts **+0.2043 R per campaign over 2,534 days** against v5's +0.1724 — an 18.5% improvement from two rules the operator ruled in. Scored through the estate's own asset-cluster ruler, its interval is **[−0.0132, +0.5085], p = 0.0740.** That is closer to the bar than v5's [−0.0271, +0.4336] and it is still on the wrong side of it. **F-C5-b survives into v6.**

**Both registrations failed.** P-TRAIL-1 (prior 65%) returns a paired Δ of **+0.0319 R**, interval [−0.0050, +0.0688] — the trail improves the mean and cannot be distinguished from noise. P-WALL-1 (prior 55%) returns **−0.0331 R**: the wall exit *costs* money, and it is the clearest negative result in the build.

**And the three headline questions have answers, none of them the hoped-for one:**

- **WHY ZEC — because of one trade.** Of 27 explanatory metrics ZEC sits *inside* the other four assets on 18, is degenerate on 3, and separates on 6 — of which 3 fail a materiality floor, 1 separates *the wrong way*, and 2 are economically nil. **+25.0605 R of ZEC's +32.5680 R is a single campaign.** There is no distribution to explain.
- **THE LIMIT SWEET SPOT — k\* = 0.40 ATR, and the pre-registration falsifies it.** The form was written before the look with three falsification clauses; clause (c) fires on its own winner: k\*'s `max_single_trade_delta_share` is **41.4008**. One trade again.
- **THE SUPPORT WALL IS A WEAKER WALL.** The league's new side names EMA **300** on 12h rejecting **54.5%** against resistance's EMA **889** at **62.7%**. Shorts have been scored against the wrong wall in every previous tier, because there was only one side.

---

## 1 · THE CARD v6 — TWO RULES, BOTH RULED, BOTH CITED

| | v5 | **v6** | ruling |
|---|---|---|---|
| trail arms | from the first confirming fractal | **after +1R, high-water latch** | **H5** |
| minimum advance | none | **0.05 ATR** | **F-C4-d** |
| trail offset | 0.5 ATR | 0.5 ATR *(ratified)* | **F-C4-b** |
| rail | 1.0 ATR | 1.0 ATR | card |
| bell | present, unruled | **kept as a backstop** | **F-C4-c / F-C5-e** |
| D12 funding ceiling | present, unruled | **kept as insurance** | **F-C5-d** |
| yardstick | three candidates 7× apart | **full-corridor expectancy** | **F-C5-a** |

**THE ARMING WAS A SCORED SHADOW CELL BEFORE IT WAS A CARD, AND THAT IS DISCLOSED ON THE HEADLINE TABLE'S FACE.** `S-TRAIL arms after +1R` was a cell of the Tier-C5 fleet; it posted +0.2047 and the session report called it *"the only S-TRAIL cell whose diagnostics do not immediately disqualify its headline"*. It is carded **by ruling H5**, not by that number — but the number existed first, the grid it came from contributed 3 cells to a logged selection surface, and a builder who promotes a cell it also scored without saying so is running the exact failure the idling guard exists to make visible.

**THE MINIMUM ADVANCE IS APPLIED WHERE IT CAN BE CHECKED.** `RC.trail_step` **calls** the parent's `trail_step` and applies one predicate to the returned `Advance` — measured on `abs(new_stop − prev_stop) / atr`, which is **exactly** the quantity the ratchet ledger publishes as `advance_atr`. A gate measured on one quantity and reported on another is a gate no reader can check, and this estate has already lost a fixture to a name that was almost right.

**A REFUSED ADVANCE DOES NOT PERSIST, AND THAT IS A CHOICE.** The pivot is not remembered; no later bar reconsiders it. The alternative — hold the refused pivot until the gap grows — would let a stop advance on a bar where nothing confirmed. It is a different rule and it is not taken.

**AND THE RULING TO KEEP THE BELL EARNED ITSELF INSIDE ONE BUILD.** Under v5 the bell fired **once in 195 campaigns**, which is what made F-C4-c/F-C5-e a live question — *backstop, or dead law?* The lean of record was *keep it: it fires rarely because the trail is faster, not because the bell is wrong.* Under v6 the trail sleeps until +1R, and the bell now fires **four times** (191 stops, 4 bells). **A rule ruled a backstop on the argument that the trail was out-competing it began firing four times as often the moment the trail was slowed** — which is the argument's own prediction, tested by accident, and it holds.

### F-C5-a, ruled and enacted

**The yardstick is the current card's full-corridor expectancy.** Not +0.6907 (118 sealed days), not +1.1964 (the operator's 29-campaign refresh) — **+0.2043**, the whole corridor. Every slice number in this build carries a **`window` column**, not a caption, because a caption does not survive a copy of the row into someone else's spreadsheet.

---

## 2 · THE HEADLINE — BOTH AGGREGATIONS, PER ASSET, AND THE ZEC ECHO

| label | aggregation | universe | n | net R | expectancy | win% | maxDD | ex-best |
|---|---|---|---:|---:|---:|---:|---:|---:|
| **CARD v6** | raw panel | panel | 195 | **+39.8443** | **+0.2043** | 34.36 | 27.4075 | +14.7838 |
| **CARD v6** | equal-asset-risk | panel | 195 | +42.7762 | **+0.2194** | 34.58 | 25.6560 | +15.6273 |
| v5 control | raw panel | panel | 195 | +33.6149 | +0.1724 | 30.26 | 25.5353 | +8.5544 |
| v5 control | equal-asset-risk | panel | 195 | +36.6721 | +0.1881 | 30.51 | 23.8365 | +9.5233 |
| **CARD v6** | raw panel | **minus ZEC** | 159 | **+7.2763** | **+0.0458** | 32.08 | 30.4796 | **−1.8667** |
| **CARD v6** | equal-asset-risk | **minus ZEC** | 159 | +7.6383 | +0.0480 | 32.11 | 29.5415 | −1.9257 |

**THE ECHO IS A RE-SCORE, NOT A FILTER.** Equal-asset-risk weights are `w_i = (N/K)/n_a` with **K = the assets present in this book** — dropping ZEC makes K = 4, and a filtered table would carry weights computed for five assets while claiming to describe four.

**AND THE TWO RULERS ARE NOT INDEPENDENT WITNESSES.** With the same seed the cluster bootstrap draws a **bit-identical asset sample** into both aggregations. The intervals are *paired*. Nowhere in this build is "both rulers agree" offered as corroboration, and it must not be read that way.

| asset | n | net R | expectancy | win% | ex-best |
|---|---:|---:|---:|---:|---:|
| BTCUSDT | 38 | −3.8374 | −0.1010 | 23.68 | −12.9804 |
| ETHUSDT | 46 | +4.3895 | +0.0954 | 32.61 | −1.7899 |
| NEARUSDT | 40 | −1.5676 | −0.0392 | 35.00 | −10.3126 |
| SOLUSDT | 35 | +8.2918 | +0.2369 | 37.14 | +2.4451 |
| **ZECUSDT** | 36 | **+32.5680** | **+0.9047** | 44.44 | +7.5075 |

**ZEC is 81.7% of the book.** Two of five assets lose money over seven years. **Strip ZEC and the card's expectancy falls to +0.0458 and its ex-best result goes negative.** F-C5-c is not merely open — it is the finding.

> ⚠ **ONE ARTEFACT, NAMED.** `top_decile_share_pct` under equal-asset-risk reads 260%–1123%. The formula is unchanged; the *denominator* is the weighted total, which is small when the rest of the book is negative. The number is arithmetically correct and semantically useless above 100%, and it is left in the table rather than suppressed, with this sentence attached.

---

## 3 · STAGE W — THE LEAGUE GREW A SECOND SIDE

| side | tf | champion EMA | approaches | rejection rate |
|---|---|---:|---:|---:|
| resistance | 12h | **889** | 59 | **62.71%** |
| resistance | 1d | 889 | 42 | 61.90% |
| resistance | 4h | 3618 | 109 | 52.29% |
| resistance | 1h | 4618 | 304 | 48.36% |
| **support** | **12h** | **300** | 99 | **54.55%** |
| support | 1d | 423 | 51 | 49.02% |
| support | 4h | 5000 | 102 | 57.84% |
| support | 1h | 3618 | 288 | 46.88% |

**SUPPORT IS THE WEAKER WALL, AND ITS CHAMPION IS A THIRD THE LENGTH.** 54.55% against 62.71% on the same clock, EMA 300 against EMA 889. Every prior tier scored shorts against a resistance champion — which measures the wall *behind* the position.

**THE MIRROR IS PROVEN TWO WAYS, AND THE SECOND WAY HAD TO BE REBUILT.** The resistance side reproduces Tier-C5's filed league **313/313 rows, zero differences on approaches, rejections, champion flags AND mean penetration** — parameterising a function by a `side` argument is exactly the edit that can change the original while adding the mirror, and the filed table is the only referee written down first.

Then F-C6-LEAGUE **calls `T6.league` itself on a negated tape** and demands `league(negated, "support")` equal `league(tape, "resistance")` — 330 rows, three count columns, **champions included**. Under `(h,l,c) → (−l,−h,−c)` a support approach *is* a resistance approach, so a sign error in the support branch shows up as a row mismatch. **0 disagree** — and, verified by sabotage, flipping one comparison in the support branch now produces **307 rejection mismatches and all four champions moving**. The first version of this leg could not have seen that; see §9.

**The champion is a NAMED MAXIMUM, not a promotion** — an argmax over the eligible panel cells with no bar, no interval and no correction. **P-WALL-1 then uses it as a decision input**, which makes it a selection surface feeding a registration. That is the single largest caveat on that claim and it rides the registration's own row.

---

## 4 · THE REGISTRATIONS — TEXT BEFORE RESULT, BOTH FAILED

| registration | prior | arm | n | Δ point | 90% CI | p | verdict |
|---|---:|---|---:|---:|---|---:|---|
| *(reference)* | — | CARD v6 vs zero | 195 | +0.2043 | [−0.0132, +0.5085] | 0.0740 | **NOT SUPPORTED** |
| **P-TRAIL-1** | 65% | v6 trail vs v5 trail (PAIRED) | 195 | **+0.0319** | [−0.0050, +0.0688] | 0.0817 | **NOT SUPPORTED** |
| **P-WALL-1** | 55% | v6+wall vs v6 (PAIRED) | 195 | **−0.0331** | [−0.0859, +0.0278] | 0.8318 | **NOT SUPPORTED** |

**BOTH ARMS ARE PAIRED, AND THE PAIRING IS THE POINT.** Tier-C5 shipped an arm named *"vs card"* scored against **zero**, and the post-build review reversed its verdict. Both arms here ride inside the same campaign set, so the paired delta exists and it is the only honest ruler: a campaign's v6 result minus **the same campaign's** v5 result, clustered on the asset. The key carries the **lane**, because two lanes can enter the same asset on the same bar and a key of (asset, entry_ms) would pair a spring with a card and call the difference a trail effect.

**m = 2 acceptance tests actually run**, q = 0.10, bar = 0.05. The reference row is not a test and is excluded from m. **Neither arm clears the BH bar**, and neither would have without it.

**THE D15 COLUMNS ARE MEASURED AGAINST THE THING EACH ARM IS NAMED AGAINST**, and every row now says which (`d15_measured_against`). That is a repair: the first draft measured P-TRAIL-1 against the v6 book, which *is* P-TRAIL-1's own book, and published a self-comparison — 0.0000 / 1.0000 / NaN — under column names a reader takes to mean the arm's diagnostics.

| registration | measured against | paired Δexp | tail-exit ratio | **max 1-trade share** |
|---|---|---:|---:|---:|
| P-TRAIL-1 | **v5 control** | +0.0319 | 1.0055 | **0.4892** |
| P-WALL-1 | card v6 | −0.0331 | 0.9329 | 0.7045 |

**And the corrected number is the most encouraging line in this build.** P-TRAIL-1's `max_single_trade_delta_share` is **0.4892 — under one.** In a document where the card is one asset, the asset is one trade, and the limit frontier's winner is one campaign at 41.4, **the trail's improvement is the only effect measured here that is not dominated by a single campaign.** It still does not clear the bar. It is the only thing that fails honestly.

**P-WALL-1 loses by cutting the tail** — `tail_exit_ratio` 0.9329 — which is the mechanism the whole card depends on. **16 wall exits fired in 195 campaigns (2 resistance, 14 support).**

---

## 5 · L-ZEC — THE ANSWER, IN THE LAB'S OWN WORDS

**Of 27 explanatory metrics** (8 further metrics are **outcome** metrics — net R, expectancy, era concentration — segregated by construction, because a metric computed *from* the result cannot explain ZEC, it **is** ZEC):

| | count | |
|---|---:|---|
| ZEC **interior** to the other four | **18** | no separation at all |
| **degenerate** | 3 | pivot gap is 7.0 bars and 200/7 = 28.5714 on *all five*; counter-armings in an open window are exactly 0 by construction |
| **exterior** | 6 | of which… |
| — fail the 20% materiality floor | 3 | |
| — separate **the wrong way** | 1 | |
| — clear every pinned gate | **2** | and both are economically nil |

**HYPOTHESIS BY HYPOTHESIS:**

- **H-Z1 trend persistence — NOT MERELY UNSUPPORTED, INVERTED.** ZEC has the **shortest** median tide streak of the five (7 bars against ETH's 12) and the **most** regime flips (15.80 per 1k bars). Sharpest line in the table: median tide streak orders the *other four* assets by net R at **rho = 0.8 on n = 4**, and ZEC sits at the wrong end of that ordering entirely. *That is what an exception looks like, not an explanation.*
- **H-Z2 relative toll — a real finding, but it is BTC's.** BTC pays **7.94%** of its median campaign reach in toll against ZEC's 1.68% — but NEAR is cheaper still at 1.67% and books negative R. An explanation for why *BTC* fails, not why ZEC wins. The funding ceiling bound **0 campaigns on all five assets**.
- **H-Z3 swing-scale match — degenerate in bars, null in ATR-time.** Strict (5,5) pivot spacing is 7.0 bars on every asset: a property of the fractal kernel, not of any market. ZEC ranks 2 of 5 in ATR-time.
- **H-Z4 whipsaw scarcity — degenerate as worded, and re-worded it produces this estate's cleanest FALSE separator.** As commissioned it is identically 0 for all five assets because `armings` *defines* the window to end at the first counter cross. Re-worded to counter 12/26 trigger crosses inside the window, ZEC posts a **robust z of −3.63 on a difference of 5.99%** from the pack median. **That is exactly why the materiality floor is a printed column and not a footnote.**
- **H-Z5 era concentration — overwhelming and circular.** A concentration computed from net R is the result wearing a different hat. (And "% of total" is undefined for BTC and NEAR — negative denominators — and returns 397% for ETH, so it is rebuilt as an HHI on positive mass.)

### THE ANSWER, ONE PARAGRAPH

> **None of the five named hypotheses explains ZEC, and the thing that does is one trade.** ZEC books **+32.5680 R of the panel's +39.8443 R (81.7%)** — and on the v5 control book it is +28.2027 of +33.6149, so this is a property of the **asset's history**, not of the card revision. **+25.0605 R of that — 76.95% of ZEC's net and 49.79% of its entire positive mass — is a SINGLE campaign** entered 2026-05-01T04:00Z and exited 2026-05-10T20:00Z: 58 bars, 7 ratchet advances, a 1.63× move in ten days. Strip that one trade and ZEC books **+7.5075 R**. Strip 2026 entirely and ZEC's expectancy is **+0.2531 R over 32 campaigns — second of five, behind SOL.** The question *"why ZEC"* presupposes a distribution of ZEC campaigns that beats the panel. **There is no such distribution.**

### THE SUITABILITY CARD — `[VETO]`, DISPLAY-ONLY

| rank | hypothesis | metric | threshold | ZEC | separation | admits |
|---:|---|---|---:|---:|---:|---|
| 1 | H-Z1 | `fan_M_med_atr_time` | ≥ 3.133338 | 3.241433 | 38.5% | **ZECUSDT only** |
| 2 | H-Z2 | `med_funding_r` | ≤ 0.001387 | 0.000904 | 80.0% | **ZECUSDT only** |

**Both screens admit exactly one asset, and that asset is the hypothesis.** Screen 1 clears its boundary by **3.45%** and *in bars rather than ATR-time ZEC is interior on the same family* — the separation lives in the volatility normalisation, not in the trend. Screen 2's absolute difference is **0.000483 R per campaign** against a ZEC expectancy of +0.9047 R: statistically clean, economically nil. **The card is display-only until registered, fitted in-sample on five assets one of which is the hypothesis, and is not a registration.**

---

## 6 · L-AE AND L-LIMIT-2 — THE FRONTIER, AND THE FORM THAT FALSIFIES ITSELF

### The hazard curve — the most usable number in the build

**P(win | maximum adverse excursion ≥ x):**

| x (R) | 0.05 | 0.10 | 0.20 | 0.30 | 0.40 | 0.50 | 0.60 |
|---|---:|---:|---:|---:|---:|---:|---:|
| **P(win)** | 32.98% | 31.18% | 27.59% | 22.36% | 17.12% | **11.19%** | **7.03%** |
| n at or beyond | 191 | 186 | 174 | 161 | 146 | 134 | 128 |

**Monotone, well-populated, and it does not depend on any registration.** A campaign that has been 0.5 R under water wins **one time in nine**. `mae_to_1r_r` could not produce this — it is `None` on **94 of 195** campaigns — so the excursion is recomputed post hoc for **every** campaign, winners and losers, with the exit bar clipped at the stop.

> ⚠ **CORRECTED BY THE TC6-V AUDIT (2026-08-17), TWICE.** *(a)* This paragraph originally read "105 of 195". **105 is the v5 CONTROL book's count; v6's is 94** — the sentence attributed the control's number to the card. *(b)* And the curve is **partly measuring the card's own stop.** The entry rail is 1.0 ATR = 1R, so a HELD excursion is censored at −1R by construction: its minimum is **exactly −1.0000** and **110 of 196 campaigns sit at or past −0.95R**, while the uncensored tape reading reaches **−4.5891 R** and **124 campaigns gap through their stop.** The hazard numbers are correct *as statements about campaigns under this card* — which is the operationally useful reading — but they are **not** statements about the market, and "the most usable number in the build" was a stronger claim than the censoring supports. `research_outputs/tc6v/campaign_features.parquet` publishes both readings side by side.

### The frontier

| k×ATR | fill% | E[R] offered | E[R] filled-only | paired Δ | missed-trades' would-have E[R] |
|---:|---:|---:|---:|---:|---:|
| 0.10 | 97.95% | 0.1593 | 0.1626 | −0.0450 | **+3.4042** |
| 0.20 | 95.38% | 0.1927 | 0.2020 | −0.0117 | +2.2650 |
| 0.30 | 91.79% | 0.1918 | 0.2090 | −0.0125 | +1.8668 |
| **0.40** | 87.69% | **0.2056** | **0.2344** | **+0.0013** | +2.0286 |
| 0.50 | 84.10% | 0.1200 | 0.1426 | −0.0844 | +2.4867 |

**k\* = 0.40 on both arms — and the pre-registration kills it.** The form was written before the look with three falsification clauses. **Clause (c) fires:** k\*'s `max_single_trade_delta_share` is **41.4008**, forty-one times the total delta in one campaign. **The sweet spot is one trade.**

**AND THE LIMIT MISSES THE BEST TRADES.** `missed_would_have_expectancy_r` is **+3.40 R at k = 0.10** and stays between +1.87 and +2.49 across the grid — the campaigns a tighter entry never gets are systematically the campaigns that pay. At k = 0.40 that is **48.69 R forgone against a 39.84 R book.**

**THE SPLIT ARM IS NOT A SECOND SEARCH.** With D12 inert, `net_r_split ≡ 0.5·net_r_card + 0.5·net_r_limit` **exactly**, so `E[R]_split(k)` is an affine increasing transform of `E[R]_full(k)` and **k\*(SPLIT) ≡ k\*(FULL)**. Pre-registration clause (b) — *"the two arms disagree on k\*"* — is therefore **unfalsifiable by construction**, and the effective selection surface for the argmax is **5 cells, not 10**. The declared m stays 10; the identity is proved as a lab fixture (error 6.5e-5).

**NO k IS PROMOTED.** Every row of the frontier carries `k_promoted = "NO — NOTHING IS PROMOTED IN-SAMPLE"` and the pre-registration text as columns, so the sentence cannot be separated from the numbers by a copy-paste.

> ⚠ **SAIL IS UNBOUND — BLOCKING.** The commission names SAIL as the out-of-sample validator. **Zero grep hits estate-wide.** The FORM is emitted and the instrument clause rides every frontier row, but there is nothing to validate against. **Ruling needed: bind SAIL, or name the validator.** (Binding it to the Prometheus paper route would validate v6's *entry* rule on v1's *entries* — named and not taken.)

---

## 7 · THE OTHER LABS

### L-FMH [H1] — the card book's zeros are the finding

On the **card book**, the three winner-protection arms fire 8 / 17 / 53 times and save **0 / 1 / 4** winners. That is not a null result to be tidied away: the card book exits `stop` **191 of 195 times**, so the (2,2) ratchet takes the campaign before any 12/89 counter-cross can speak. On the **union book** (414 campaigns, 147 winners) A2-containment fires 62 times with 37 winners — **17 saved, 19 killed.** Both books are printed side by side.

> ⚠ **CORRECTED BY THE TC6-V AUDIT (2026-08-17) — A SENTENCE HERE WAS FALSE.** This paragraph originally claimed **"every arm's Σ delta is negative"**. The counterfactual was booking an exit at the CLOSE of bars on which the stop had already been taken — **173 impossible exits** across the books — and adverse-first says the stop fills intrabar and the campaign is already out. With the signal search bounded one bar short of a stop exit, **the v5-control A3 arm reverses sign: Σ delta −3.1944 → +1.2276.** The claim "every arm's Σ delta is negative" is withdrawn; on the repaired tables it is false for A3 on the control book. The remaining arms stay negative. See §A of `BUILD_2026-08-17_TC6V_TIERC7.md`.

### L-WALLQ [H2] — a wall beyond the stop is a worse campaign

| alignment | n | win% | expectancy | reached +1R |
|---|---:|---:|---:|---:|
| `beyond_stop` | 129 | 28.68 | **+0.0085** | 46.51% |
| `blocks_2r` | 9 | 55.56 | +0.6801 | 77.78% |
| `neither` | 28 | 42.86 | +0.5637 | 60.71% |
| `no_wall` | 29 | 44.83 | +0.5810 | 58.62% |

Two-thirds of the book arms with the champion wall **behind** it, and those campaigns return roughly nothing. The buckets that pay are small (n = 9, 28, 29) and **provisional**. This is P-SIZE-W's evidence and it points the opposite way to the intuition that a wall behind you is protection.

### L-SPR-NT [F-C5-i] — the estate's own 3,526 is defective, four ways

| | |
|---|---:|
| **admitted signals** | **363** (127 long / 236 short) — *not* the 241 campaigns previously used as the comparator |
| **refused on tide** | **3,470** (1,313 / 2,157) — floored; the filed 3,526 counts 56 refusals inside the first 316 bars, where the tide gate is evaluable and wrong |
| **unreclaimed** | **1,374** (488 / 886) — a population counted nowhere in the estate |
| **partition** | **5,207** — and it does not close without the third row |
| episode-collapsed refusals | 2,916 — `spring_signals` emits once per sweep bar with no non-overlap guard |

**Four defects in one filed number**, each measured, and the refused leg is reconciled against the parent's own counter with a HALT rather than inferred by subtraction.

### The shadow fleet — 25 cells, reported whole

| cell | grid | net R | expectancy | paired Δ | **max 1-trade share** |
|---|---|---:|---:|---:|---:|
| **S-TRAIL +0.25 ATR buffer** | S-TRAIL | **+77.1027** | +0.3954 | +0.1911 | **1.1044** |
| S-OFFSET 0.25 × S-MINADV 0.00 | cross | +44.4536 | +0.2280 | +0.0236 | 0.2412 |
| S-BUF 0.35 | S-BUF | +44.3378 | +0.2274 | +0.0230 | 0.4154 |
| S-BUF 0.25 | S-BUF | +40.0279 | +0.2053 | +0.0009 | **32.7171** |
| S-HFRAC 67% | S-HFRAC | +40.2435 | +0.2064 | +0.0020 | 1.7963 |
| S-HFRAC 33% | S-HFRAC | +39.4451 | +0.2023 | −0.0021 | — |

**F-C5-f CARRIED FORWARD AND STILL TRUE.** `S-TRAIL +0.25 ATR buffer` posts **+77.10 R — 1.94× the card** — with a max single-trade share of **1.1044**. It is the cell that gets promoted if nobody reads the last column. **S-BUF 0.25 is worse: 32.7.** Named loudly, twice, for the same reason.

**H6's cross is reported whole:** S-OFFSET {0.25, 0.5, 0.75} × S-MINADV {0, 0.05, 0.10} = **9 cells**, none dropped. H3's ruled 50% sits between S-HFRAC 33% (+39.45) and 67% (+40.24) — a **0.80 R spread across the whole fraction range**, which is the useful finding: the harvest fraction barely matters.

---

## 8 · THE FIXTURE TRANSCRIPT

| fixture | verdict | evidence — and its failure condition |
|---|---|---|
| **F-C6-CTRL** | PASS | the v5 card through v6's forked `_ride`/`_account`/`replay` reproduces Tier-C5's **filed** journal: 195/195 campaigns, same rows in order, **worst absolute diff 0.000e+00** across 13 numeric columns, every `exit_reason` matching. *Fails if any column moves.* |
| **F-C6-INHERIT** | PASS | 21 objects bound by **identity** across four generations, 0 copies; `ratchet_step` reached through to Tier-C4's own object; Card v6 **subclasses** Card v5; **no inherited default drifted** outside the 6 declared fields. *Fails if a default changes without being declared.* |
| **F-C6-ARM** | PASS | **85 of 85** advance-carrying campaigns checked (cardinality, not a sample); 0 advances confirm before the campaign's first +1R bar **re-read from raw bars**; ledger 228 == 228. **And the converse has content: the v5 control shows 80 advances v6's rule would refuse.** *Fails if that is zero — then the leg measures the empty set.* |
| **F-C6-MINADV** | PASS | `advance_atr` **is** `abs(Δstop)/atr` on all 228 rows within a **derived** per-row rounding bound; 0 advances under 0.05 ATR; **the gate bites — 9 of Tier-C5's 273 filed advances would be refused.** |
| **F-C6-LEAGUE** | PASS | resistance reproduces the filed league **313/313, 0 differences including penetration**; the **mirror proof calls `T6.league`** on a negated tape — 330 rows, 3 count columns, champions included, 0 disagree. **Sabotage-tested: flipping one support comparison yields 307 mismatches and moves all four champions.** |
| **F-C6-WALL** | PASS | 5 wall exits hand-verified against an **independent** 12h rebuild (pandas groupby, not `wall_series_12h`), each within tolerance **and first in its ride** — 0 earlier qualifying bars. *Fails on membership without firstness.* |
| **F-C6-ZEC** | PASS | ZEC's share **re-derived from the filed journal** by a path that calls no lab function; outcome/explanatory segregation asserted; **the materiality gate is asserted to BITE**; the suitability card asserted display-only. |
| **F-C6-GRID** | PASS | the selection surface counted **three independent ways** — the hand-maintained literal, the cards the code builds, the rows the parquet holds. **41 cells across 12 grids; 8 checked three ways, 4 declared-only and NAMED as owned elsewhere** rather than passing because a count was `None`. *Fails on disagreement, and on a grid this module builds reporting no cards.* |
| **F-C6-DET** | PASS | two full runs → 27 tables, **0 build-sha moved, 0 parquet files differ on disk**; wall-clock fields absent from every written table. |
| **F-C6-CLOSURE** | PASS | 5 decision modules, 0 analytics imports, 0 tape column names, scanned on **AST-stripped source**. TIER-C6 raises the stakes: P-WALL-1 needs a 12h EMA as a **decision** input, built in `tierc6_rules` from raw bars so the league's resampler never enters a decision. |
| **F-KEY** | PASS | **TOTAL: 27 declared keys covering all 27 filed parquets**, read from the manifest the build wrote rather than a literal, 0 duplicates; ledger 228 == book 228; journal 195 == book 195 == manifest 195. |

**Suite:** `pytest` → **334 passed, 1 skipped, exit 0.**

---

## 9 · THE REPAIRS — AN ADVERSARIAL REVIEW RUN BEFORE PUBLICATION

**Eight lenses, 55 agents. It found a blocker, and the blocker was mine in the worst way available: a fixture leg I had advertised as "the leg with content" could not fail.**

| # | what was wrong | what changed |
|---|---|---|
| **C6-1** | **BLOCKER · F-C6-LEAGUE's MIRROR PROOF NEVER CALLED `league()`.** It defined a private `scan()` *inside the fixture* and ran that on the original and negated series. `grep -c "T6.league" tierc6_fixtures.py` returned **zero** — **no leg of any fixture ever executed the support branch of the function that builds the table.** Worse, the copy was an exact algebraic identity: ATR is invariant and EMA exactly equivariant under `(h,l,c)→(−l,−h,−c)`, so the reviewer swept the two constants it reads over **20 combinations — including `APPROACH_ATR = 0.0` and `RESOLVE_BARS = 0` — and it passed all 20.** It also scanned a different population: one EMA on two assets from bar 317, where `league()` scans fifteen EMAs on five assets. The reviewer then mutated the support branch, rebuilt the whole book, and got **10/10 PASS** while the 12h support champion moved **EMA 300 → 89**, the wall book went **16 exits → 4**, and P-WALL-1's interval moved | the leg now **negates the tape and calls `T6.league` itself**, demanding `league(negated, "support") == league(tape, "resistance")` over **330 rows, three count columns, champions included**. **Sabotage-tested after the repair: the same mutation now yields 307 rejection mismatches, 304 streak mismatches, and all four champions moving.** |
| **C6-2** | **`mean_penetration_atr` WAS SILENTLY REDEFINED UNDER A REPRODUCTION CLAIM.** Tier-C5 appends `max(pen, 0.0)` for **every** approach; this fork appended only on a break-through and kept the parent's column name. **290 of 313 rows differed**, plus 9 null mismatches — and the build said "zero differences" because leg (a) compared only approaches, rejections and champion flags. Same defect class as `dist_atr` and `prior_extreme`: a name that is almost right | the parent's definition is **restored exactly** (now 0 differ, max diff 0.0, 0 null mismatches), and the broke-only depth — which is the more useful statistic — is published beside it as **`mean_breakthrough_depth_atr`**, under its own name. Leg (a) now compares penetration too |
| **C6-3** | **P-TRAIL-1's D15 WAS A SELF-COMPARISON.** `_row` passed `d15(book, base)` for every arm, and P-TRAIL-1's `book` **is** `base` — so it published `d15(v6, v6)`: paired delta 0.0000, tail ratio 1.0000, NaN single-trade share, under column names a reader takes to mean the arm's diagnostics | the base is **named at every call site**, P-TRAIL-1's is the **v5 control**, and every row carries `d15_measured_against`. The corrected numbers are real — and `max_single_trade_delta_share = 0.4892` is the most encouraging line in the build |
| **C6-4** | **`top_decile_share_pct` CARRIED TWO DENOMINATORS UNDER ONE NAME** — 260% and 302% under equal-asset-risk sitting in the same column as 72.6% and 77.1% raw | the basis is now a column (`top_decile_share_basis`) and a flag says when the value may be compared across aggregations (`top_decile_share_comparable_to_raw`). Nothing suppressed, nothing silently rescaled |
| **C6-5** | **`wall_touch` ACCEPTED `direction` AND NEVER READ IT** — two paragraphs of docstring about which side the wall is on, over a signature that takes the side and ignores it. A reader checking whether the profit side is enforced *there* would conclude it is | the parameter is **removed**. The side is carried entirely by which champion length the caller passes; the geometry test is deliberately symmetric and now the signature says so |
| **C6-6** | **F-C6-GRID PASSED UNCONDITIONALLY ON ANY GRID THAT BUILT NO CARDS** — `None` satisfied both clauses, so **4 of 12 grids and 16 of the 41 declared cells were unchecked**, and the leg would have passed on a declared size of 5,800 | grids this module does not build must be **NAMED** as owned elsewhere; everything else must agree three ways. **8 of 12 checked three ways, 4 declared-only and named** |
| **C6-7** | **F-KEY NAMED 9 TABLES IN A LITERAL WHILE THE BUILD FILED 27** — eighteen tables, including every lab table, were never re-checked, and a new table would have joined them silently. `put()` also swallowed empty frames without record | the keys are **read from the manifest the build writes**, so the leg is total by construction: **27 declared keys covering all 27 filed parquets**. Skipped-empty tables are recorded in the manifest, so "absent" and "never attempted" are different facts |

**NO SCORED NUMBER MOVED.** Every repair was to a fixture, a column definition, or a diagnostic's base. Card v6 is still 195 campaigns at +39.8443 / +0.2043; the champions, the wall book and all three registration verdicts are unchanged.

> ⚠ **THE REVIEW DID NOT FINISH, AND THAT IS ON THE RECORD RATHER THAN IN A FOOTNOTE.** Of 55 agents, **31 verifiers failed to run** — the session hit its usage limit mid-pass. Eight findings were confirmed by a completed refuter and are repaired above. **Thirty-nine further findings were raised and never adjudicated**, and several were raised independently by three or four lenses — which is corroboration, not proof, but is not nothing. The unadjudicated set is carried into §10 rather than discarded. **A review that stopped early is not a review that passed**, and no one reading this should treat the fixture suite's 11/11 as though the full audit had cleared it.

---

## 10 · FINDINGS — NOT FIXED

**F-C6-a · THE CARD STILL DOES NOT CLEAR ITS OWN BAR.** +0.2043, CI [−0.0132, +0.5085], p = 0.0740 on 195 campaigns over seven years. Better than v5 and on the same side of the line. **F-C5-b is carried, not answered.**

**F-C6-b · ZEC IS NOW 81.7% OF THE BOOK AND THE ANSWER IS "ONE TRADE".** F-C5-c asked *why*; L-ZEC answers *there is no why*. **Ruling needed and it is the deepest one here: does a card whose result is one campaign on one asset constitute an edge?** My lean is that the panel stays, and that **"≥3 of 5 leave-one-out panels exclude zero" becomes part of the registered text** — it would have failed every arm this session, which is the point.

**F-C6-c · SAIL IS UNBOUND.** The pre-registered limit form has no validator. Zero hits estate-wide. **Blocking for L-LIMIT-2's (c).**

**F-C6-d · THE SPLIT ARM'S SECOND FALSIFICATION CLAUSE IS UNFALSIFIABLE.** Proved, not suspected: the split arm is an exact convex combination, so the two arms cannot disagree on k\*. The clause was written in good faith before the look and is void. **Declared m stays 10; the effective argmax surface is 5.**

**F-C6-e · `top_decile_share_pct` EXCEEDS 100% UNDER EQUAL-ASSET-RISK.** Arithmetically correct, semantically useless above 100%. Left in the table with its sentence attached. **Ruling needed: cap it, drop it, or rename it.**

**F-C6-f · L-FMH CANNOT BE RUN AS COMMISSIONED ON THE CARD BOOK.** 0 / 1 / 4 winners across three arms. The substitute (the union book) is reported beside it, and the zeros are printed rather than suppressed.

**F-C6-g · THE 12h CHAMPION IS AN IN-SAMPLE ARGMAX USED AS A DECISION INPUT.** Disclosed on the league rows, the registration text and the registration result. It is the largest caveat on P-WALL-1 — which failed anyway, so nothing rests on it this build. **It would matter if the wall ever passed.**

**F-C6-i · THE SUITABILITY CARD'S `assets_admitted` CANNOT TAKE ANY OTHER VALUE.** The screens are constructed *from* ZEC's separation, so "admits ZECUSDT only" is a tautology, not a result. Disclosed in §5 in words; the column itself should carry the caveat. **Not fixed — the card is display-only and registered nowhere, so nothing rests on it.**

**F-C6-j · L-SPR-NT DECLARES A BH FAMILY OF m = 8 WHILE PUBLISHING 12 p-VALUES, AND NEVER APPLIES THE CORRECTION.** `bh_family_m = 8`, and `h20_p_one_sided` / `h100_p_one_sided` are non-null on 12 rows. **The correct m is 12**, and no `clears_bh_bar` column exists on that table. The spring line is Tier-E measurement with no registration resting on it, so no verdict changes — **but the declared family is wrong and is recorded as wrong.**

**F-C6-k · THIRTY-NINE REVIEW FINDINGS WERE NEVER ADJUDICATED.** The verifier pass ran out of session before reaching them. Several recur across three or four independent lenses and deserve a pass before anything here is built on: *the pre-registration artifact is never written to disk (`write_prereg` has no caller)*, *the L-ZEC and L-LIMIT-2 self-check tables are never filed*, *`l_ae_deciles` may be publishing the card's own stop rail as an adverse-excursion statistic*, *L-FMH's counterfactual may exit at the close of a bar the stop had already closed*, and *the wall-aware S-BUF cell may read unfloored seeded EMAs*. **None is confirmed. None is refuted. Ruling needed: re-run the verifier pass before TIER-C7.**

**F-C6-h · TWO ATTACHED DOCUMENTS DID NOT ARRIVE.** STEP 0 asks for them to be filed with shas printed. They were not in the commission and are not in the estate. **The only deliverable of this build that is incomplete**, recorded rather than dropped.

---

## 11 · DISPOSITION + BOX-COST

| PATH | EXISTS | TRACKED | COMMITTED | PUSHED | PROTECTED BY | BOX COST |
|---|---|---|---|---|---|---|
| `scripts/tierc6_rules.py` | yes | yes | this push | yes | hand commit, explicit paths (CL-13) | 0 B, non-box |
| `scripts/tierc6.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_lab_zec.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_lab_limit.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_lab_misc.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `scripts/tierc6_fixtures.py` | yes | yes | this push | yes | same | 0 B, non-box |
| `research_outputs/tierc6/` | yes | **no — gitignored** (`.gitignore`) | — | — | **NOT PROTECTED — local only** | n/a, off-bus |
| `exchange/reports/BUILD_2026-08-16_TIERC6_REVB.md` | yes | yes | publish | yes | publish guard, `exchange/**` scope | *see below* |
| `exchange/reports/DEFINITIONS_D_H_2026-08-16.md` | yes | yes | publish | yes | same | *see below* |
| `exchange/status/LEDGER_APOLLO.md` | yes | yes | publish | yes | same, append-only | *see below* |

*(This build ships the CONVENTIONS §3.2 seven-column form. The TIER-C lineage has shipped a two-column condensation twice; that is a §3.2 breach and it is corrected here rather than inherited.)*

### BOX-COST

**`BOX_BYTES`, `WARN_FRACTION`, `REFUSE_FRACTION` and `FLAG_BYTES` were read LIVE from `publish_exchange` — never typed.**

| | before this paste | **after** |
|---|---:|---:|
| `exchange/**` | 3,168,632 B · 19.80% | **3,216,696 B · 20.10%** |
| **tick set** (`exchange/**` + `LEDGER.md`) — *governs* | 3,427,930 B · 21.42% | **3,475,994 B · 21.72%** |
| level | OK | **OK** (warn 40% / refuse 70%) · headroom to REFUSE ≈ **7.72 MB** |

**This paste's own three files: ≈ 36,989 B (this document) + 11,075 B (the definitions document) + ≈ 6,900 B (the `LEDGER_APOLLO` append) ≈ 54,964 B ≈ 0.34% of the box.**

**AGAINST THE < 0.5% TARGET (80,000 B) THAT IS 69% OF BUDGET.** The bytes went where the commission asked them to: the ZEC answer, the frontier, and a repair table that names a fixture which could not fail.

**THE NAMING TRIP-WIRE DID NOT FIRE FOR THIS BUILD'S OWN FILES** — the build document is 36,989 B and the definitions document 11,075 B, both under the 64,000 B flag. The wire continues to fire on eight pre-existing box-bound files (`LEDGER.md`, `LEDGER_APOLLO.md`, three earlier BUILD documents, `LEDGER_ATHENA.md`, the HEPHAESTUS builders' report and `CONVENTIONS.md`); each already has an intended home recorded under CONVENTIONS §3.2 and none is added to by this paste except `LEDGER_APOLLO.md`, which is append-only by design.

---

*End of build document. TIER-C6 rev B · 27 tables · 11 fixtures · two registrations, both refused · one card that still cannot clear its own bar · and the answer to "why ZEC" is one trade.*
