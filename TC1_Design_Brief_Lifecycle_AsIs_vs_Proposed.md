# TC-1 Design Brief — The Trade Lifecycle, As-Is vs Proposed
## Every step from signal to exit: what the engine does today, and exactly what the next Tier-C run would change

**Date:** 2026-07-18 · **Author:** reviewer (Claude, Fable-mode) · **Status:** decision brief — TC-1 is **proposed, not ratified**; this document is the thing you rule on.
**"As-is" =** engine 1.0.8, config `v12_anchor_g8` — the TC-4 baseline (grid −1,796.99 net / +275.99 gross / 2,599 campaigns), which is also cell A of the proposed factorial, already run.
**"Proposed" =** the TC-1 2×2 factorial from Report 3: {exit: baseline vs governor-e200 trail} × {admission: none vs basis-point floor m=2}. Four cells, four pre-registered runs (one already exists), each with its own G-7 ledger line.
**Provenance:** every as-is mechanism below was read from `trading.py` / `signals.py` / `replay.py` source this cycle (line references given), or from the ratified charter §3.4 and the TC-4/S-1 verified artifacts. Worked-example prices are **invented round numbers for clarity** — every evidence number lives in Report 3 and the phase artifacts.

---

## §0 How to read this

The life of a trade is told as twelve sequential stages. Each stage has three parts: **AS IS** (what happens today, in plain language, with the mechanism), **UNDER TC-1** (unchanged, or changed exactly how), and **why** (the measurement that earns the change). Most stages are **UNCHANGED** — that is the point of a surgical factorial: two levers move, everything else is held still so the run can attribute what it finds.

One term used throughout: **a "close" vs a "touch."** Bars are candles. A level is *touched* if the candle's range reaches it mid-bar; a *close* beyond a level means the candle finished past it. Stops fire on touches; the proposed trail engages and exits on closes plus a level, as specified below.

---

## §1 The lifecycle at one glance

| # | Stage | As-is (1.0.8) | Under TC-1 |
|---|---|---|---|
| 1 | Campaign birth (arming) | governor EMA9/EMA89 cross | **unchanged** |
| 2 | Signal generation (PRIME / CONFIRM / V) | zone tag + reclaim; ribbon re-cross; climax reversal | **unchanged** |
| 3 | Grading (A+ / A / B; C never trades) | snipe pocket / HTF alignment / else | **unchanged** |
| 4 | Signal-close gates | zone, ribbon, cooldown, direction, CONFIRM-needs-position | **unchanged** |
| 5 | Fill-time gates | halts, max 3 tranches, 1R rail, BE add-gate, gap-through-stop, G-8 guards | **+ one new gate: the basis-point floor (m=2)** |
| 6 | Sizing | grade table; 1R = 0.5% equity | **unchanged** |
| 7 | Initial stop placement | signal-bar extreme ∓ 0.5×ATR; one shared stop per direction | **unchanged** |
| 8 | In-trade protection | event-driven ratchet only (advances on new signals; never on price/profit) | **stop logic unchanged; a harvest line is added** (form pending one ruling — §6) |
| 9 | Adds and re-entries | BE-gate for adds; PRIME-while-flat trades as re-entry; CONFIRM-while-flat refused | **unchanged in rules; the new floor applies to these fills too** |
| 10 | Exit triggers | stop touch (all tranches together) · gap · failure-X · opposite cross · V-reversal · equity-floor flatten | **+ one new exit: close beyond the governor-e200 trail, after engagement** |
| 11 | Costs at exit | taker fees both sides, slippage by tier, funding | **unchanged** |
| 12 | Accounting, halts, journaling | realized R; −2R day / −4R week halts; 25% equity floor; full journal | **unchanged** (new gate/exit journal under namespaced reasons) |

---

## §2 The twelve stages in detail

### Stage 1 — Campaign birth *(unchanged)*
**AS IS.** The governor chart (4H on swing, 1H on intraday, 12H on position) computes three moving averages. When the fast one (EMA9) crosses the medium one (EMA89) upward, the system "arms long" — it is now willing to buy; downward, arms short. Each arming starts a numbered **campaign**. If the arming direction disagrees with the larger backdrop (EMA89 vs EMA200), the campaign is born **provisional** — second-class: smaller size, grade capped at B. *[verified — signals.py arming block; provisional semantics per E-1 record]*
**UNDER TC-1.** Untouched. The signal brain is byte-frozen; the run's F-SIG-style fixture will prove it.

### Stage 2 — Signal generation *(unchanged)*
**AS IS.** Three ways a trade idea is minted: **PRIME** — price pulls back into an active zone (bands draped around the governor EMAs) and then reclaims it in the campaign's direction on the execution chart; the campaign's first PRIME is the **R1**, later ones are add-class. **CONFIRM** — the execution ribbon re-crosses in the campaign's favor; add-class only. **V** — a climax flush that snaps back; can birth a campaign against the prior direction. *[verified — signals.py]*
**UNDER TC-1.** Untouched — including V (the S-1 sweep showed loosening manufactures junk: 12.2× the firings, worse forward returns; TC-3 struck).

### Stage 3 — Grading *(unchanged)*
**AS IS.** Each PRIME is stamped **A+** (entry sits inside a swept-and-reclaimed "snipe" pocket), **A** (the alignment timeframe's ribbon agrees — the 1h for swing cells), or **B** (neither). Provisional campaigns cap at B. **C-grade confirms are journaled and never trade, by design.** Grade sets position size (Stage 6). *[verified — signals.py:491–559]*
**UNDER TC-1.** Untouched — with an honest note for later: S-1 found grade does *not* predict the pyramid cohort, while 30m alignment (which the engine ignores) does. That is candidate **C13** for a *future* slot, deliberately **not** smuggled into this factorial.

### Stage 4 — Signal-close gates *(unchanged)*
**AS IS.** At the signal bar's close, before anything is queued: the zone gate (`no_zone` if no active zone), the ribbon-separation chop filter (waived when the active zone is Z3), cooldown, bar-range sanity, direction agreement — and the charter's **"while positioned" clause**: a CONFIRM add arriving while the book is flat is refused (`not_positioned`, `trading.py:439–444`). Every refusal is journaled with its reason. *[verified]*
**UNDER TC-1.** Untouched. S-1 vindicated the while-positioned clause decisively: the refused population would have run −2.87/unit, 74% geometrically invalid.

### Stage 5 — Fill-time gates *(ONE ADDITION — factorial axis 2)*
**AS IS.** A queued entry fills at the **next bar's open** (plus modeled slippage), but only after passing, in order: the halt calendar (−2R day / −4R week, per cell), **max 3 tranches per campaign**, the **1.0R open-campaign risk rail**, the **breakeven add-gate** (an add is admitted only if the current shared stop is at breakeven-or-better for every open tranche, `trading.py:274–281`), and the guards: `gap_through_stop` (fill at/through its own stop → reject, `:363–366`), **G-8c** minimum stop distance 0.5×ATR, **G-8b** notional ≤ 10× equity, **G-8d** unit-sanity assert. *[verified — wake order per trading.py header; guards per TC-4]*
**UNDER TC-1 (axis 2, cells C and D).** One new rejection, sitting beside G-8c: **the basis-point floor.** At fill time compute the stop distance as a fraction of price, in basis points, and the round-trip toll for the asset's cost tier (fees + slippage both sides: 14 / 20 / 30 bps). If **stop distance < 2× the toll**, reject the fill — journaled `stop_below_cost`, namespaced. Plain language: *if the trade's entire risk budget is smaller than twice what the broker charges to get in and out, the trade cannot pay for itself; refuse it.* It applies to **every** fill — R1s, adds, re-entries — one dial, no special cases in this run.
**Why.** The cost identity (cost-in-R = cost_bps ÷ stop_bps) is the study's proven disease mechanism; S-1's flag books show the bps floor **dominates** the ATR floor at every operating point, and m=2 flags 3,813 fills carrying **−1,436** of the grid's −1,797, leaving a −361 book first-order. The factorial turns that first-order number into a real one. *[measured — S-1 entry_flag_books]*

### Stage 6 — Sizing *(unchanged)*
**AS IS.** 1R = 0.5% of the cell's current equity, priced at the stop distance at fill. Grade table: A+/A full-campaign R1 risks 0.50R; B and provisional R1s and V entries 0.25R; adds 0.50R. Quantity = risk dollars ÷ stop distance. *[keys verified trading.py:144–177; values per ratified charter §3.4 + manifest]*
**UNDER TC-1.** Untouched. (Note the pleasant side-effect of Stage 5's floor: by construction it removes exactly the fills whose tiny stop distance would have produced outsized notionals — the same pathology G-8b/G-8c bound, now bounded in the units that matter.)

### Stage 7 — Initial stop placement *(unchanged)*
**AS IS.** On any entry signal the stop for that direction moves to the **signal bar's own extreme** (low for longs, high for shorts) cushioned by **0.5×ATR** of the execution chart — and there is **one stop per direction, shared by every open tranche**. A stop hit exits all of them together. *[verified — signals.py:475–482; shared-stop architecture]*
**UNDER TC-1.** Untouched. The campaign stop remains the risk backbone in every cell of the factorial.

### Stage 8 — In-trade protection *(stop unchanged; A HARVEST LINE IS ADDED — factorial axis 1)*
**AS IS.** The stop advances **only when a new entry signal prints** — the same formula on the new signal bar, taken one-way (`max` for longs, `min` for shorts; it can never loosen — a standing fixture now). Between signals it is frozen. It never watches price, never watches profit. This is the measured heart of the PROTECTED paradox: **90.35%** of trades that touched +1R and died at a loss had *zero* advances before their peak; when advances happen at all, the first comes at a median of **11 bars**. There is no take-profit, no partial exit, no trail on the traded book. *[verified mechanism; measured magnitudes — S-1 advancement]*
**UNDER TC-1 (axis 1, cells B and D).** A **governor-timeframe harvest line** is added: the 200-EMA of the governor chart, cushioned by 0.5×ATR of the execution chart (`ema200_gov_b0.5`, the grid-best measured form — see §6 for the b/uniformity veto). Its lifecycle: **dormant** at entry → **engages** on the first execution-bar *close* beyond the line in the trade's favor → thereafter the line **trails, never loosening** (it steps when the governor bar closes), and the position **exits when price closes back through the cushioned line against the trade**. Whether this line *replaces* the stop after engagement (fold-in, as S-1 measured it) or runs *beside* the stop as a second, independent exit (two-line) is the one open ruling — §6, D-2. Either way, Stage 7's stop keeps guarding the downside throughout.
**Why.** The S-1 ratchet grid's central result: the governor trails are the **only** exit family that beats all-or-nothing — grid gross +584.50 vs +275.99, position transformed from −73.80 net to **+389.25** (1× proxy) — precisely *because* they sacrifice the median winner (−32% capture) and let the tail run. Every faster rule, including the mechanized versions of the operator's own 5m-pivot and 1h-e89 practices, lost money against doing nothing. *[measured — S-1 ratchet_scorecard; first-order + proxy caveats standing]*

### Stage 9 — Adds and re-entries *(rules unchanged; the new floor applies)*
**AS IS.** A PRIME firing **while positioned** may add — if the BE-gate passes (Stage 5) and the rail has room. A PRIME firing **while flat** mid-campaign trades as a **re-entry** (the vacuously-true gate; the May-26 signature path), journaled with `fill_class="re_entry"` since 1.0.8. A CONFIRM while flat is refused (Stage 4). Max three fills per campaign, total. *[verified]*
**UNDER TC-1.** No rule changes — but note the interaction the factorial is built to expose: re-entries are the densest tight-bps population, so **axis 2's floor bites them hardest** (that is TC-2's quality bar arriving early, in its simplest form); and under the fold-in exit, add-eligibility becomes rarer still (mean would-be-eligible 0.01–0.06 under gov trails), while under two-line it is preserved. The adds question is decided by your ruling, not by this run's code.

### Stage 10 — Exit triggers *(ONE ADDITION)*
**AS IS.** In priority as the engine walks each bar: queued flattens at the open (failure-X — price closing beyond the far side of the governor band for N bars kills the campaign; opposite governor cross; V-reversal), gap-through-stop fills at the open, then the **intra-bar stop touch** (all open tranches fill at the stop, or at the open if gapped), and — since TC-4 — the **equity-floor flatten** (cell equity < 25% of initial → flatten everything, halt the cell permanently). 99.7% of historical exits are the stop. *[verified — replay/trading wake order; measured share]*
**UNDER TC-1 (cells B, D).** One trigger added to the list: **the harvest-line close** (Stage 8). Everything else keeps its place and priority; the stop still guards every bar of every tranche's life.

### Stage 11 — Costs *(unchanged)*
**AS IS.** Taker fee 5 bps per side, slippage 2/5/10 bps per side by asset tier, funding accrued at each timestamp and realized at exit. Results always at 0×/1×/2×. *[verified — manifest cost_semantics]*
**UNDER TC-1.** Untouched — the limit-chase/maker work stays sequenced *after* demonstrable edge, per your standing ruling. One honesty note carried from Report 3: trail exits hold longer, so realized funding will run slightly above the S-1 proxy; the factorial measures it truly.

### Stage 12 — Accounting, halts, journaling *(unchanged)*
**AS IS.** Realized R per tranche; per-cell halt calendar; append-only journals; determinism double-run; the full fixture discipline. *[verified across four phases]*
**UNDER TC-1.** Unchanged, plus: the new gate and the new exit journal under namespaced reasons (`stop_below_cost`, `harvest_trail`), and the contract will carry a signal-parity fixture and pre-registered predictions per cell, per G-7.

---

## §3 One trade, told twice (invented numbers, real mechanics)

*BTC swing cell (4H governor / 5m execution). Equity $10,000, so 1R = $50. All prices illustrative.*

**Birth and entry (identical in both worlds).** The 4H EMA9 crosses above the EMA89 → campaign 218 arms long, stage-2 (structure agrees). Price pulls back into a zone and reclaims it; a PRIME prints, grade A. Signal bar low $59,700; 5m ATR $120; stop = 59,700 − 60 = **$59,640**. Next 5m bar opens at **$60,000** → fill. Stop distance $360 = **60 bps** of price; the toll (tier A) is 14 bps round-trip; 60 ≥ 2×14 → **passes the new floor** (in the baseline world the floor doesn't exist; same fill either way). Size: 0.50R = $25 risk ÷ $360 → 0.0694 BTC (~$4,167 notional; leverage 0.42× — G-8b untroubled).

**Path 1 — the tail trade.** BTC runs to **$63,000** over three days. Open profit per unit of risk: (63,000−60,000)/360 ≈ **+8.3R** — a monster. No new PRIME prints during the run (price never revisits a zone), so the shared stop **never moves off $59,640** — the 90.35% pattern, live.
- **As-is:** price finally rolls over, falls all the way back, touches $59,640 → exit. Eight-plus R of open profit, realized: **−0.5R** (a full loss on the half-R position). This is the PROTECTED paradox in one sentence.
- **Under TC-1 (cells B/D):** at entry, price was already above the 4H e200 (≈ $58,800) → the harvest line **engaged on day one** and has been stair-stepping up with each 4H close. By the peak it sits at ≈ $61,200; cushioned line $61,140. On the rollover, a 5m bar **closes** at $61,100 — through the line → exit at ≈ $61,140. Realized: (61,140−60,000)/360 ≈ +3.17R per unit → **+1.58R** on the position. The trail kept ~38% of the peak; the baseline kept −6%.

**Path 2 — the ordinary winner (why the median capture is negative, and why we accept it).** Same entry; BTC pokes to **$60,504** (+1.4R), stalls, dies. The 4H e200 is still down at ~$58,900 — *below the campaign stop*. Fold-in takes the tighter of the two, so in **both** worlds the exit is the same: stop touch at $59,640, **−0.5R**. The trail did nothing for the modest winner — and that is precisely the measured trade-off: the governor trail abandons the median +1R trade to buy the whole of Path 1. The factorial's bet, in one line: *there are enough Path 1s to pay for all the Path 2s* — grid-wide, S-1 priced that bet at +308 gross; TC-1 checks it with real paths.

**Where the two exit architectures would differ** (not in these two paths): if a *second PRIME* had printed during Path 1, the event-ratchet would advance the campaign stop — possibly above the trail. **Fold-in** (as measured) takes the max, so the stop and the trail are one line. **Two-line** keeps them separate: the advanced stop restores add-eligibility (the BE-gate can pass; the pyramid can form) while the trail keeps harvesting. Same exits almost always; different *add futures*. That is the entire content of ruling D-2.

---

## §4 The factorial: four cells, what each isolates

| Cell | Exit | Floor | Status | What it isolates |
|---|---|---|---|---|
| **A** | baseline | none | **exists** (TC-4 baseline: −1,796.99 / +275.99) | the control |
| **B** | gov-e200 trail | none | to run | the exit effect, alone, path-true |
| **C** | baseline | bps m=2 | to run | the admission effect, alone (vs the −361 first-order claim) |
| **D** | gov-e200 trail | bps m=2 | to run | the interaction — the number no shadow can produce |

Predictions to be registered in the TC-1 contract before any run (directional statement now; bands set at contract time against A): position strongly positive in B and D; swing improved in B/C/D; **intraday unmoved-or-worse on the exit axis** (every S-1 candidate lost there) and strongly improved on the floor axis; D's interaction not merely additive (the floor removes tight-bps fills whose trail outcomes were priced into B's shadow). Each cell: G-7 pre-registration, signal-parity fixture, determinism double-run, strip-best and CIs mandatory — including, this time, **per-cell strip-best on the trail exits**, closing Report 3's open concentration question.

## §5 What TC-1 deliberately does not touch

The signal brain, zones and their geometry (VS-Z3 competes for a slot separately), grading (C13 likewise), V thresholds (struck), the BE add-gate rule, sizing, the rail and halts, the G-8 guards, the cost model, the lockbox. Two levers. Everything else is the control.

## §6 Decisions on your desk (defaults stand on silence, except D-2)

| # | Decision | Default / status |
|---|---|---|
| D-1 | Ratify the 2×2 factorial as §4 | **Default: yes** |
| **D-2** | **Adds resolution — fold-in (as measured) vs two-line (stop + independent harvest line)** | **No default — needs your word.** Reviewer's lean: two-line, because it is the only form honoring both your BE-gate principle and the tail-riding exit. **Gated on the builder's pending semantics confirm** (whether S-1's candidates already priced the two-line union). If the confirm says "frozen-at-engagement," a one-day S-1b mini-shadow prices two-line before the contract is written. |
| D-3 | Trail form: `ema200_gov`, cushion b = 0.5×ATR_exec, **one form grid-wide** | Default: yes (grid-best single form; avoids per-mandate cherry-picking — position's b=0 edge over b=0.5 was 8 gross points, noise) |
| D-4 | Floor m = 2.0, applied to all fill classes | Default: yes (the flag-book knee; TC-2 refines per-class later) |
| D-5 | Engagement rule: first execution-close beyond the raw line; exits on close through the cushioned line | Default: yes (matches the S-1 measured spec) |
| D-6 | RC-7 (free joint-confluence lattice + per-candidate strip-best) runs while TC-1 is contracted | Default: yes |

## §7 What happens next, in order

1. You rule on D-1…D-6 (one line each; D-2 explicitly).
2. Builder answers the one-line semantics question (already posed in Report 3 §XI-2).
3. If needed: S-1b mini-shadow (two-line pricing) — a day, not a phase.
4. I draft the TC-1 contract: four cells, predictions with bands against cell A, fixtures (signal parity, floor holds everywhere, trail never loosens, determinism), operator §0 steps, go-paste — the standing procedure.
5. RC-7 runs in parallel; its lattice feeds the slot decision (VS-Z3, C13) but touches nothing in TC-1.

---

*Prepared by the reviewer under Fable-mode, 2026-07-18. As-is mechanics: source-verified this cycle (`signals.py:475–482` ratchet; `trading.py:274–281` add-gate, `:363–366` gap guard, `:439–444` while-positioned clause; wake order per the module header; guards per the TC-4 record). Proposed mechanics: the measured S-1 forms, with the single open semantics fork stated rather than assumed. The worked example is illustrative; the evidence is Report 3's. Two levers, four cells, everything else frozen — so that whatever the factorial finds, we know exactly what found it.*
