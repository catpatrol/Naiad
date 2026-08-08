# SECRET SAUCE — THE SYSTEM SYNTHESIS
**APOLLO · 2026-08-06 · destined for `exchange/reports/` (text, exchange-eligible; reaches every lane via GitHub sync + one Sync-now click)**

**What this document is.** Three things at once, by operator commission: **(I)** a plain-language **trade manual** — every stage of a Secret Sauce trade, what we know about it, and how a discretionary trader uses it today; **(II)** an exhaustive register of **what we know, what we don't, and what we want to find out**, including the full SSv12/EngineV2 rescoping; **(III)** a **pantheon update** — recent activity and the current state of the project. It is written to prime the next APOLLO chat from zero: a reader with no context can start here and continue where this chat leaves off.

**Provenance tags used throughout:** `[measured]` = on the evidence ledger, recomputed or fixture-verified · `[replicated]` = cleared a multi-asset replication bar · `[structural]` = a counting fact about the data, no outcome claim · `[operator]` = the operator's ruling or hypothesis, on the record · `[candidate]` = named, pre-registrable, unmeasured · `[parked]` = awaiting an operator stamp · `[KB]` = from the ingested trading literature · `[falsified]` = tested and killed, kept on the record so it stays dead.

---

# PART I — THE TRADE MANUAL

## 1.1 · The market model Secret Sauce trades

Secret Sauce (SS) reads the market through a small family of exponential moving averages computed on every timeframe from 1 minute to 1 week: the working trio **9 / 89 / 200** (breath, stride, posture), a shadow pair **12 / 25** (measured jointly and separately), and — new in this cycle — the long pair **300 / 450** for higher-timeframe orientation. When price and these lines interact, they emit **events**: crosses (one EMA through another), kisses (an approach that touches and rejects without crossing), price tests and bounces, and level break-and-flips.

The founding observation, now partially measured: these events **cascade across time AND across timeframes** `[operator, canonical definition; minability proven by fixture F-SEQ8]`. A real move tends to begin on fast frames and climb; the interesting question is *how* it climbs. Descriptive tier labels (labels only — no rule force `[operator]`): **FAST** 5m/15m/30m · **STAIR** 1h · **SLOW** 4h/12h · **TREND** 1d.

Three structural facts anchor the model:

1. **The leap, as seen from a pullback low.** Anchored at a turn, the SLOW tier activates mostly by *jumping* — 66% of 4h arrivals come directly from the fast tier, while 1h arrivals mostly climb in from the step below. This replicated on all seven assets in pure counts, no outcomes involved `[replicated — P-SEQ-ii; 5 solid assets + 2 thin]`. The qualifier is mandatory: unanchored, 1h feeds 4h more than the fast tier does — the leap is a property of *how turns look*, which is exactly the trading-relevant view, and now an honestly stated one `[structural]`.
2. **The episode, not the clock, is the natural unit.** A cascade bounded by direction-consistency (a counter-direction cross ends it) is essentially unaffected by any time-window choice; windows were a measurement convenience, not a market fact `[structural]`.
3. **Ranges and their traps.** The operator's frame, now the system's: ranges build; an apparent breakout traps traders; their forced exits fuel the reversal — **PO3** (accumulation → manipulation → distribution). The same anatomy under other names: Wyckoff's spring, AMT's failed auction, the practitioners' fake-out-and-reclaim `[KB — the vocabulary cross-map]`. This grammar applies to entries AND, mirrored, to exits `[operator]`.

## 1.2 · The five stages of a trade, and the rule set v0.2

The momentum literature's unified post-trigger framework — trigger → confirmation → risk definition → initiation style → early management `[KB]` — matches the operator's own four-stage system description almost exactly, and both agree with our measurements on where the money is: **confirmation and management carry more expectancy than the raw trigger** `[measured — D9/P-LAT killed timing confluence; the exit asymmetry findings]`. The rules below are v0.2 — v0.1 revised under the operator's replies. Changes from v0.1 are marked ⟨Δ⟩.

**C1 · TIDE — the slow tier arms the book.** The **4H regime cross is the arming event of record** ⟨Δ: promoted from "a slow-tier cross or kiss"⟩ — it marks the trade type our system demonstrably catches best `[measured: 4H is the only rung clearing its own toll, ratio 1.0711 CI [1.0534, 1.0903]; slow-tide alignment flips 8 conditions positive, 1d strongest at +0.229]`. The 9×200 kiss-and-reject is **demoted to a confluence element** ⟨Δ⟩: present in the May-26 case, not guaranteed present, never load-bearing until measured `[operator]`. 12H and 1D give context; 1D never executes `[engine design]`. *Trading it today:* watchlist = assets printing a fresh 4H trio cross in the prospective direction, with the 4H 89/200 side noted as regime seal.

**C2 · WHERE — business only at walls.** Entries admitted only where price meets structure: the deep zone (Z1 — the *deep* zone discriminates winners; Z2 does not `[measured — W-F1: Z1 Δ+0.209 CI [0.158, 0.258]; Z2 ≈ 0]`), a range extreme carrying a verdict, a scored confluence level. Mid-range is forbidden `[measured: in-range births bleed −1.24 vs −0.91; the no-zone counterfactual would have lost at −1.205/unit vs −0.577 admitted]`. **Range detection itself is not yet scoped** ⟨Δ: acknowledged as the open half of this rule⟩ — how we detect and verdict a range is a named census/module question (Part II, CQ-6..8) `[operator: "how will we measure and test it?"]`.

**C3 · THE TRAP — prefer the fake-out first, and mirror it at the exit.** ⟨Δ: PO3 symmetry added⟩ The highest-grade births follow a failed counter-move into the wall — the spring/fake-out — before igniting `[as stop-mechanic: 52% of shakeouts convert to ≥1R, measured; as entry precondition: candidate, stamped-not-law]`. **Mirrored:** when positioned and hoping to add on a range break, a *failed continuation plus reclaim of the prior range* is the symmetric exit/ratchet signal `[operator — the PO3 mirror; candidate]`.

**C4 · TRIGGER — LTF executes, first attempts only.** Direction from the mid-to-high timeframe; execution on the low ones. 5m is the permanent entry floor `[measured — TC-5: 1m economics falsified]`; first attempts strongly beat re-entries `[measured — W-F1: re_entry over-represented in losers, Δ −0.427, q=0.0006]`; the re-entry quality bar (TC-2) is the standing repair. *Openness clause* ⟨Δ⟩: this is the best version found so far, not the last one `[operator]`.

**C5 · STOP — structural at birth; the ratchet is an open problem.** ⟨Δ: status honestly split⟩ At birth the stop goes beyond the real structural pivot that defines the wall test — never a fixed distance `[measured: grid +565.58 / strip-best +301.99 vs baseline ≈ −1,800]`. But this is a **point of control with a low bar**: it only proves structure beats the old ATR line `[operator]`. The **ratchet** — how the stop advances so the trade breathes while protecting some profit — has no working mechanism: the first Tier-C's ratchet was mis-designed, and the naive trail was falsified decisively (it clipped the winners the system exists to catch) `[falsified — two-line: grid −121.71 vs predicted band [500, 650]]`. The live hypothesis: **test-and-reclaims of the long EMAs (200/300/450) on 15m/1H/4H, with a tunable n×ATR cushion, as the ratchet/add points** `[operator; candidate — must beat the ride-only control]`.

**C6 · RIDE & FEED — winners are fed at structure, and the feeding points may be the ratchet points.** The winning book's shape is unambiguous: winners never exit by stop (0%), they exit at regime break (63% opposite-cross, 37% failure-cross), and they hold three orders of magnitude longer than losers (median 128.5h vs one single 5-minute bar) `[measured — W-F1 anatomy]`. Adds are where the only positive cohort lived (3-add campaigns: +4.88, 72.6% win `[measured]`), and the old add gate was frozen precisely when adding was wanted (97.59% of winning moments offered no pullback-reclaim `[measured — P-CIRC]`). The v0.2 hypothesis unifying C5 and C6 ⟨Δ⟩: **a successful long-EMA test-and-reclaim in trend is simultaneously the add trigger and the ratchet anchor** — one structural event, two actions `[operator + reviewer synthesis; candidate]`.

**C7 · HARVEST — the exit is the entry system, mirrored.** ⟨Δ: the mirror principle replaces the candidate-list framing⟩ The exit logic is the **inverse, symmetric version of the entry logic** `[operator ruling]`: the opposing wall is the harvest zone (where shorts cover, longs trim); an opposing-direction arming event on the slow tier is the exit-arm; the mirrored trap (failed continuation + range reclaim) is the exit trigger; acceptance *the wrong way* through a level ends the campaign. Concrete TP candidates to test under that principle: opposing value edge / naked POC partial with a regime-break runner (the two-sink `[KB — recurs across AMT, CTA, and the practitioners]`), the measured move, σ-band hinge targets (H-VBT `[candidate — heads ARGUS's priority list, aimed at the open wound]`), and the 5m 300/450 ribbon flip as exit-*planning* tripwire `[candidate — H-M1X adjacent]`. The wound this must close: **73.67% of trades that reach +1R round-trip to a loss** `[measured]` — "our data shows that if we don't adjust stop and take profit as the trade exhausts, we risk giving it all back" `[operator]`.

**The standing law over all seven rules:** no single feature gates alone. Every naive single-feature filter kept at most 65% of the tail R, most kept ~40% `[measured — the W-F1 TRG table]`; admission and exit decisions are **composite** — counted votes across tide, location, class, trap — and every promoted rule prints its Tail-Retention Gauge beside strip-best `[ratified]`.

## 1.3 · The worked example — the May 26th short, stage by stage

The canonical illustration, from the operator's own charts (BTCUSDT.P), sitting inside the 2025-26 markdown from ~124k to the low 60s:

**Stage 1 — Arming.** Mid-May 2026, price rallies into the falling D/4H EMA band from below. The 4H trio prints a bear cross; the 4H 89/200 seal is bearish; 12H shows interleaved bull/bear crosses first — BALANCE in cross-space, the market deciding `[the 12H chop reads as the verdict forming, not as noise]`. A 9×200 kiss-and-reject on the way in adds a confluence count ⟨not a requirement⟩.

**Stage 2 — Location + trap.** The rally is the counter-move into the wall: LTF bull crosses fire *into* the underside of the band (the dark-green debris) and fail — the fake-out/spring, PO3's manipulation leg, trapping late longs whose exits will fuel the markdown.

**Stage 3 — Trigger + risk.** With tide bearish, price at the wall, and the trap sprung, the with-trend 5m cross after the band rejection is the trigger; the stop goes above the structural high that defined the test — wide enough that the shakeout converts through it.

**Stage 4 — Management.** As the move develops, each long-EMA underside retest that *holds* (15m, then 1H, then 4H — visible across the operator's October-onward frames as test-deviation-rejection-underside-retest sequences) is the candidate add-and-ratchet event: feed the winner at structure, trail the stop to the structure the market just validated — never to break-even for comfort `[the literature's own warning: early tightening truncates exactly the outcomes that pay — which our two-line falsification proved on our own book]`.

**Stage 5 — Exit.** The mirror: harvest a partial into the opposing wall / value edge when reached; end the campaign when the slow tier prints the opposing arming event or price accepts back above a broken level. This trade's profile — tide-aligned, Z1-born, first attempt, long hold, regime-break exit — **is the W-F1 winner profile feature for feature** `[measured correspondence]`.

**Honest caveat, always attached:** this is one asset, one episode, selected by eye in a bear year. It illustrates the grammar; it proves nothing. The May-26 program (Part III) exists to turn it into a measured family.

## 1.4 · The confluence stack — what a discretionary trader lays on the chart today

The certified analytics pack (v1.5.0 `[chart-certified against the operator's own TradingView on closed candles, BINANCE:<SYM>USDT.P]`) supplies, **display-only, never evidence**: the level registry (anchored + rolling VWAPs with σ-bands, volume-profile POC/VAH/VAL with a permanent approximation chip, period opens, prior extremes, SS zone edges — 131–169 levels/asset, collapsed and clustered, scored by counting only); the **hinge** at every σ-band (two targets, mean vs far value, both R:R printed, no preference); **de-peg chips** telling you which anchors currently say anything new; and dual scoring with/without the volume families so the volume filter's effect is visible daily. Use: before taking a C1-armed setup, check what *independent* families agree with the wall — and record it, because whether that agreement predicts anything is precisely what CENSUS-1d and H-VBT will score `[firewall unchanged]`.

## 1.5 · Where to look, where to avoid — the one-paragraph field guide

**Look:** fresh 4H arming in the tide's direction · price at a deep zone / range extreme / multi-family confluence wall · a spring or fake-out into that wall · first attempt · slow stack aligned behind you. **Avoid:** mid-range anything · re-entries without a bar · fast-frame births without slow cover (every rung below 4H fails its own toll `[measured]`) · the grind context (5m→15m→30m churn, 60.6% of all cascades, middling outcomes `[structural/indicative]`) · managing winners early — the winning book never did `[measured]`.

---

# PART II — WHAT WE KNOW, WHAT WE DON'T, WHAT WE WANT TO FIND OUT

## 2.1 · Known — measured anchors (the numbers that constrain all design)

| Fact | Number | Source |
|---|---|---|
| Structural stop dominates | grid +565.58 / strip-best +301.99; 52% shakeout conversion | ledger (S-2/S-2b) |
| Naive trail kills winners | two-line grid −121.71 vs band [500,650] | ledger `[falsified]` |
| Harvest wound | 73.67% of +1R-touchers round-trip; peak-capture −43.65% vs baseline | ledger (S-3) |
| Winning exits | opposite_cross 67% win; W book: 0% stop exits | ledger + W-F1 |
| Holding-time chasm | W median 128.5h vs L median 300s (1541.8×) | W-F1 |
| Re-entry disease | Δ −0.427 toward losers (q=0.0006); ~83% of clean-book loss | W-F1 + ledger |
| Deep zone only | Z1 Δ +0.209; Z2 ≈ 0 | W-F1 |
| 4H rung toll-positive | 1.0711 CI [1.0534, 1.0903] | ledger (D8) |
| Add cohort | mc=3: +4.88 expectancy, 72.6% win | ledger |
| Add gate frozen | 97.59% of winning moments had no PRIME | ledger (P-CIRC) |
| Slow tide flips conditions | 1d s2_aligned +0.229; 12h beyond_e200 +0.181 | ledger (D3) |
| Fast-frame economics | TC-5: mechanical fractal confirmed, net −1,180.32 falsified; 5m floor permanent | ledger |
| Funding drag | W 3.5% of pnl (position mandate 10.2%); L ≈ 0 | W-F1 first read |
| Single-feature filters condemned | best TRG 65% (with negative ΔExp); typical ~40-50% | W-F1 TRG |
| Discriminant harvest | 84 tests → 15 FDR-survive → 12 CANDIDATES (r1-only: 20) | W-F1 |

## 2.2 · Known — structural (counting facts, no outcome claims)

The SEQ8 substrate exists: **288,711 raw cross events** (7 TFs × both alphabets, per-event multiTF snapshot) and **950,145 cascades as eight derived views** — cascade definitions are queries now, never baked `[structural]`. P-SEQ-ii replicates 7/7 with the anchor qualifier `[replicated]`. The episode is the natural atom; windows are inert `[structural]`. **286 trade births sit inside no cascade at all** — unexamined `[structural, embargoed outcome side]`. Monotone share 83.01% (errata-corrected); 16.4% shuffles "not obviously worse" `[structural]`. EMA-300/450 warmup: 13 asset/TF cells never warm — the D6 gate `[structural]`. Journals carry **no slow-stack lattice** — tide features reach trades only through the SEQ8 bridge `[structural — the P-WF1 premise-false finding]`.

## 2.3 · Unknown — the honest register

**About entries:** the kiss's actual value (detector unbuilt; v0 derivable from SEQ8 snapshots) · the trap's discriminant power (stamped, unmeasured) · range detection end-to-end (definition, verdict, trap-rate) · the acceptance close-set (1H vs 4H vs 12H — unruled, DEF-5 open) · direction asymmetry (every studied example is a short in a bear tape — does the grammar mirror to longs?) · which exec/gov TF pairs are optimal (the operator's pairs are suggestions to test `[operator]`).

**About management:** a working ratchet (nothing measured; long-EMA reclaim hypothesis live) · the add trigger's precise definition (mini-range break? long-EMA reclaim? both?) · what each tier promotion licenses · whether the 1H stall (only 29.3% clear to 4H) is tradeable information or just attrition.

**About exits:** everything — the largest open surface. The mirror principle is ruled but nothing under it is measured; H-VBT, two-sink, measured-move, ribbon-flip are all candidates.

**About architecture:** whether the subsystem split (S1-S4) reflects real regime boundaries or taste · concurrency/margin/correlation costs of multiple books on one asset set · the downward fractal (1m-5m long EMAs; TWAP-split entries vs the cost identity) · the {12,25} pairing scope `[parked]` · what the 286 no-cascade births are.

## 2.4 · The census-2 question register (the operator's questions, made census-shaped)

CQ-1 Which ranges are best to trade (by regime, tier, width)? · CQ-2 Which TF best predicts the move we want? · CQ-3 Which TF best predicts the *execution* of that move? · CQ-4 What does the 1H stall mean — and can the 1H→4H clearance be caught specifically? · CQ-5 Can a tuned 5m-1H scalper survive its own toll (TC-5's heir)? · CQ-6 Range detection: level tested-and-reclaimed → range play / sniper-pocket setup — operationalized how? · CQ-7 Level broken-and-flipped → breakout setup — acceptance defined by which close? · CQ-8 Trap (PO3) detection in real time — with what trap-rate? · CQ-9 Long-EMA reclaims on 15m/1H/4H as ratchet/add points — do they beat ride-only? · CQ-10 The 5m/1m 300/450 ladder — entry/exit information or volatility proxy (H-M1X gauge)? · CQ-11 TWAP-split entries following an LTF long-EMA cascade — cost and survivability impact? · CQ-12 The turtle outlook (200/300/450 on 4H/1D/1W) — does slow PA interaction carry a book? · CQ-13 Which confluence layers survive their deflation gauges (the eight ARGUS candidates)? · CQ-14 Do May-26-similar births (defined curtain-clean) outperform — and on how many assets?

---

# PART III — THE SSv12 / ENGINEV2 RESCOPING

## 3.1 · The path (committed to memory, operator-ratified)

**Refining Secret Sauce is drafting EngineV2.** Sequence: define SSv12's entries and exits for the next Tier-C → design census-2 to capture exactly the data that design needs → run the census → run Tier-C with EngineV2. The inversion governs throughout: understand the winning trades to catch more of them and fewer losers.

## 3.2 · Subsystem candidates — hypotheses, not commitments `[operator intuition; each names its deciding data]`

**S1 · Scalper (5m-1H stack):** needs "lots of weeding" — lives or dies on CQ-5 and the re-entry bar. **S2 · Swing (4H-1D):** the demonstrated sweet spot — the May-26 type; first in line. **S3 · Long-cascade hunter (5m→1D):** rides range-to-range hops; treats 30m-1h chop as LTF ranges whose breaks are adds; decided by CQ-4/CQ-9 and the episode-level cascade data. **S4 · Turtle outlook (200/300/450 on 4H/1D/1W):** slow PA-interaction book; cheap to measure on existing logic (CQ-12) — with the warmup matrix (3.4, MC-1) bounding what "1W long EMAs" can even mean.

## 3.3 · The May-26 program (operator items 7a-7d) — with its one discipline

7a — define **similarity first, on curtain-clean birth features only** (the 4H bear cross, seal state, wall contact, trap presence, first-attempt), then find all similar births in the data and only then read outcomes. Defining similarity after peeking at outcomes would manufacture the conclusion — this ordering is the program's integrity `[reviewer, binding]`. 7b — project the full feasible EMA set + analytics pack onto the May-26 episode itself (the dossier). 7c — the same stack inspection on the known leap-family winners (15m→30m→4h / 5m→15m→12h / 5m→15m→4h birth sequences). 7d — the ratchet study: long-EMA reclaims as decision points (cut vs add), S/D and S/R detection feeding the DECIDE moments. The program **requires a partial embargo lift** (outcome tables + cascade→trade bridge) — the stamp menu rides the MC interview below.

## 3.4 · THE MC INTERVIEW — scoping the mini-census + mini-Tier-C (operator item 8)

Ruling per gate; defaults = my leans; one word each suffices. This cannot "just run" — four of its parameters are physically or statistically binding.

**MC-1 · The EMA × timeframe feasibility matrix, and the episode window.**
*What:* you asked for 12/25 + 9/89/200 + 300/450 on all TFs 1m→1M. Arithmetic binds this: with the estate starting 2019 (~90 monthly, ~360 weekly bars; late-listed alts far less), **EMA450 can never warm on 1W or 1M; EMA300 never on 1M and only marginally-late on 1W (BTC alone); 89/200 never on 1M; on 1M only {12,25} ever converge.** *Options:* **(a)** adopt the feasible matrix — everything computable where it warms, D6 table extended to prove per-cell convergence, 1M carrying {12,25} only, 1W carrying up to 200 — and pin the May-26 dossier window at ~Oct 2025–Aug 2026 with warmup runway before it; **(b)** trim to 1m-1D and drop 1W/1M from the program. *Lean:* **(a)**.

**MC-2 · The similarity definition (7a's core).**
*What:* what makes a birth "May-26-like." *Options:* **(a)** a pre-defined feature family: {fresh 4H trio cross in direction · 4H 89/200 seal agreeing or crossing within k bars · price in contact with the D/4H band (Z1-side) · counter-move trap present within the prior m bars · first attempt} — each element a stamp, similarity = count ≥ threshold, all constants [VETO]-flagged; **(b)** strict literal match (all five required) — cleaner, thinner; **(c)** nearest-neighbor similarity in feature space — recall-maximal and a fishing surface I recommend against as primary. *Lean:* **(a)** with (b) printed as the strict core.

**MC-3 · The comparison population and the stamps.**
*What:* 7a compares similar births against the last Tier-C's winners; 7c inspects the leap-family winners — both need the **embargoed** outcome tables and cascade→trade bridge opened, and the parked promotions carry placeholder priors awaiting your stamps. *Options:* **(a)** lift the embargo for this program's scope only (bridge + outcome tables on the named populations), stamping the three parked promotions now with my proposed priors (leap outcome edge 55% · grind↔loser join 60% · route-conditioned edge 45%); **(b)** full lift; **(c)** keep sealed and limit the program to birth-side anatomy. *Lean:* **(a)** — scoped lift, everything pre-registered before reading.

**MC-4 · The confluence layers on the dossier.**
*What:* which analytics families lay onto the May-26 episode and the winner set. *Options:* **(a)** full registry (VWAPs + σ + profile-with-chip + period levels + SS zones) in dual scoring, display + counted co-location stats, no predictive claims; **(b)** VWAP family only; **(c)** defer analytics to census-2 proper. *Lean:* **(a)** — this is exactly the rehearsal the dual-scoring machinery was built for.

**MC-5 · The 1m leg.**
*What:* 1m 89/200/300/450 (your restricted set) for the episode window and the winner birth-windows — bounded compute, answers the downward-fractal and TWAP-split questions at dossier scale before any census commitment. *Options:* **(a)** include, windowed; **(b)** exclude this pass. *Lean:* **(a)**.

**MC-6 · Deliverable shape.** *Options:* **(a)** one zero-context dossier document (your ratified reporting format) + machine tables filed to exchange, HTML render optional after; **(b)** HTML-first. *Lean:* **(a)**.

**MC-7 · Sequencing.** *Options:* **(a)** mini-program runs **now, before census-2 design closes** — it is the pathfinder that tells us which columns census-2 must carry (the operator's stated purpose); **(b)** fold it into census-2. *Lean:* **(a)**. On your MC rulings I draft the queue-item contract (fixtures, populations, [VETO] constants, TRG columns, disposition table) for Hephaestus.

## 3.5 · The momentum document, scrutinized (operator item 9)

**Adopted:** the five-stage post-trigger framework as the manual's spine (it *is* your four-stage system, independently derived) · the vocabulary cross-map as the nomenclature source (3.6) · Spring→SOS→LPS as the trap grammar's formal skeleton, with "jump across the creek" as the aggressive-add gate · acceptance operationalizations as the CQ-7 candidate list · chipping-in as the TWAP-split's practitioner precedent · the two-sink exit as C7's leading concrete form. **Flagged, four places where the literature must yield to our measurements:** (1) "tighter stop under the LPS if desired" — on our book, width *is* the edge (52% shakeout conversion); stop tightness is a measured question, not a preference. (2) Break-even moves stay on the literature's menu — our naive version is `[falsified]`; only the structural-reclaim ratchet earns a retest, against the ride-only control. (3) Elder's oscillator ripple — timing oscillators stay annex-only in this house (D9's grave). (4) Stefan's rapid risk-free is valid **as partial-then-risk-free** (realize, then protect the remainder) — not as a naive BE-trail; the distinction is load-bearing and both get measured under C7.

## 3.6 · The nomenclature program (item 10b — opened, not urgent)

Standing principle henceforth: **names point at the things they name.** Source: the cross-map. First candidates for the main moving parts (to be ratified only after their roles are measured): the 4H regime cross → *Initiation* or *Ignition* (its role — arming — is confirmed; its best name awaits the May-26 program's findings on what it actually predicts) · the fake-out → **Spring** (Wyckoff's term is exact and 100 years old) · the add-point pullback that holds → **LPS** · acceptance events → *Acceptance* (AMT's term, unimprovable) · the harvest structure → *Opposing value*. A ratification pass rides the Definition document.

## 3.7 · The questions you're forgetting (item 10a — the reviewer's additions)

1. **Direction asymmetry:** every example studied is a short in a bear year — the long-side mirror must be verified per-direction, not assumed. 2. **Regime dependence:** the May-26 family may be a bear-regime species; held-in-time and regime-split discipline applies. 3. **One asset:** the pattern is BTC-drawn; the five-asset panel decides whether it is a market fact or a BTC fact. 4. **The 286 no-cascade births** — what is the engine trading when no cascade exists? 5. **Multi-subsystem costs:** concurrent books share margin and correlate; the concurrency/funding feedback was the heaviest S-2b caveat and returns doubled with subsystems. 6. **Campaign end in EngineV2:** the mirror principle needs its falsifier — what *exactly* ends a campaign, and does inherited failure_x survive the redesign? 7. **TWAP-splits vs the cost identity:** more transactions = more toll unless maker-priced; the split-entry study must carry the fee model explicitly. 8. **1m data completeness:** verify the 1m parquet inventory per asset before promising 1m EMAs. 9. **The acceptance close-set (DEF-5)** is still unruled and half the program leans on it. 10. **Claude in the engine** (your stage-4 wondering): feasible now as a *batch screener* — Claude scores engine-emitted candidate states against the Definition document, pre-registered and measured against the mechanical baseline; not as a live executor (determinism, auditability, the operator-as-governor constitution). A named workstream when you want it.

---

# PART IV — PANTHEON UPDATE (activity + current state)

## 4.1 · What this lane did (2026-08-03 → 08-06)

Resumed SS on operator instruction · ratified the **inversion + discriminant frame + TRG** · commissioned and verified **W-F1** (9/9 fixtures; 12 candidates; four predictions confirmed, one premise-false honestly scored; the TRG table condemning single-feature gates; first realized-funding read) · issued the SEQ interview → all eight gates ruled → **SEQ8 extract built** by Hephaestus under Dionysus's drafting (288,711 events; 950,145 cascade-views; embargoed outcome layer; P-SEQ-ii replicated 7/7 with the anchor-relativity correction owned) · re-primed after context loss (2026-08-05; reachability verified, CONVENTIONS read, ARGUS pantheon report + Dionysus notes ingested) · two screenshot batches scrutinized (nine + four charts); EngineV2 core C1-C7 presented; operator replies folded → **rule set v0.2** (kiss demoted · PO3 symmetry · mirror principle · ratchet opened · subsystems named) · momentum deep-dive scrutinized (adopted spine + four flags) · **the path committed to memory** · this synthesis produced.

## 4.2 · Current state by lane

**APOLLO (here):** SS definition converging; DEF-1..8 and MC-1..7 interviews open; May-26 program scoped; LEDGER_APOLLO **9 days stale — append rides the next paste** together with the P-SEQ-ii ledger-entry text check. **HEPHAESTUS:** idle, queue empty pending MC rulings; W-F1 and SEQ8 delivered clean (two builder-refusal saves on record this cycle). **DIONYSUS:** delivered the Rewire and the SEQ8 drafting; hosts the deep-dive whose operator-side material this chat is producing; range-scoping note open. **ARGUS:** analytics 1.5.0 certified; brief 3×/day; eight census candidates routed with deflation gauges; awaiting operator parity readings (volume-overlay blocker). **ATHENA:** conventions + memory restructure landed; backups verified end-to-end; queue item 002 (--phase mirror fix) ratified; docs/history sync-selection question open. **HERMES:** DIGEST live; two ARGUS routing notes archivable per ARGUS ruling.

## 4.3 · Open items on the operator's desk (consolidated)

1. **MC-1..7** rulings (this document, §3.4) — unlocks the May-26 program paste. 2. **DEF-1..8** (previous session) — DEF-2 constants, DEF-5 close-set, DEF-6 ladder now partially absorbed into MC/C-rules; a reconciliation pass rides the Definition doc. 3. **Stamps** (MC-3): the three parked promotions + scoped embargo lift. 4. Parity readings (ARGUS blocker). 5. T-6 export inspection (ATHENA). 6. Filing this document to `exchange/reports/` (route below).

**Filing route (one drag):** drag this file into the LOCAL Claude Code with the one-liner: *save to `exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md`, byte-exact, record sha256, run publish_exchange, state push result, then append the owed LEDGER_APOLLO entry (re-priming 08-05 + rulings 08-06 + this filing) and grep the P-SEQ-ii ledger entry for its registration text + anomaly note, printing both.* I will produce that paste in full, per conventions, on your word — or fold it into the MC program's first paste.

— APOLLO, reviewer of record, 2026-08-06
