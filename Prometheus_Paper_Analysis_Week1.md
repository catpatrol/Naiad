# PROMETHEUS — Forward Paper Analysis, Week 1
## Health check + characterization of the first virgin paper window (2026-07-08 → 07-14)

*Prepared under Fable mode from the live `paper-data` journals and the committed engine
source. Every performance figure below was **recomputed this session from the raw `r` column**
and reconciles to `state.json` exactly (integrity pass). Provenance tags: **[record]** = committed
project record; **[verified]** = recomputed this session from raw journals or read directly from
the engine source; **[analysis]** = present hypothesis, not established.*

---

## 0. Scope, caveats, and data-spend ledger

**What this is.** A ~6-day, 33-trade, three-coin (BTC/ETH/SOL) forward-paper window. Per the
mission and the record, this is a **health-check + characterization + hypothesis pass — explicitly
NOT a go/no-go.** Six days is roughly one regime and is far below the ~8–12 multi-regime window
floor any deployment verdict would require. Every conclusion below carries that caveat.

**Bright lines respected.** Nothing was tuned against this window. No parameter was changed. The
window is treated as spent-for-characterization only; any improvement named in §8 must be built
offline as a named frozen variant and validated on *new* paper data. Report HTML was not trusted
for any number — all recomputed from raw.

**Data-spend ledger (updated). [record→verified]**
- 2020–2026 retrospective (76-mo OOS): **spent for validation** (unchanged).
- Forward-walk 2026-05-25 → 06-24 range window: **spent** (unchanged).
- **Forward paper 2026-07-08 → 07-14 (this window): now marked characterization-spent** for the
  current frozen ruleset. Reading it here does not license tuning against it.

**One structural limitation to name up front. [verified]** The live paper journal persists only a
subset of the engine's per-trade fields (`paper_live.py` `_JOURNAL_COLS`). It carries `grade` and
`kind` but **drops** the full birth-evidence dict (`base_present`, `sweep_context`,
`spring_linked`, `sep_atr_confirm`, `bars_to_confirm`, `birth_status`, `wyckoff_score`) and the
engine's stop counterfactuals (`r_sig_only`, `r_struct_only`). Those are exactly the fields the
Phase-4b autopsy found most predictive and the fields needed to A/B stop variants on live data.
Consequence: the structure-detection deep dive (§5) is limited to what `grade` and `kind` reveal —
`grade` is a clean proxy for `base_present` (see §9), but the sharper predictors cannot be tested
forward until they are logged. **Fixing this is the single highest-leverage change for the next
iteration's ability to learn (see §8.0).**

---

## 1. Executive summary — lead with the answer

**The week printed +16.65 R and +0.126% account across 33 trades. It is entirely tail-carried, and
half of the tail is an open, unrealized position.** Two trades supply the whole result: BTC
+8.42 R (closed) and **SOL +8.81 R (still open, marked-to-market at the last bar)**. The other 31
trades net **−0.58 R**. Strip the open SOL position and realized pooled is +7.84 R over 32 closed
trades — a number one closed lottery ticket (the BTC trade) makes positive. This is the
**expected** shape for a low-hit, fat-right-tail system — say so plainly and do not over-read the
green headline. [verified]

The five findings that matter for the next iteration:

1. **Tail-carried, twice, one unrealized.** BTC and SOL are each positive on the strength of a
   single trade; ETH is simply negative. Underneath the two tails the system is flat-to-slightly-
   negative. [verified]
2. **The cohort mix looks *better* than the retrospective baseline (STILLBORN 30.3% vs 39.1%,
   PROTECTED 45.5% vs 40.5%) — but this is almost certainly the regime, not a fix.** All three coins
   ran mildly directional weeks; more trades reached +1R because the tape trended, not because the
   structure problem was solved. [verified + analysis]
3. **The "thin births outperform" and "capitulations outperform" headlines are the *same two
   trades* and collapse under tail-removal.** On central tendency, base-graded (A/B) births are far
   more reliable (46% hit, −0.09 R median) than thin (25% hit, −0.67 R median). The base-detection
   thesis holds; the tails are a separate capitulation-lottery phenomenon. [verified]
4. **Cross-origin births are the weak entry path; the capitulation path carries the system.**
   `kind=birth` (EMA-cross-origin) has a −0.80 R median and 27.8% hit — most cross births die.
   Capitulations have a −0.23 R median, 40% hit, and own both tails. [verified]
5. **The biggest *realized* leak is on the win side: the system captures only ~39% of the favorable
   excursion on its largest trades.** The e200 trail (0.5×ATR) lags a fast move so far that big
   winners give back 2.7–6.9 R; one SOL trade rode +6.86 R MFE all the way back to −0.04 R. Because
   the tails *are* the edge, better tail capture is nearly pure upside — but any change here is
   asymmetric-risk and must be proven not to clip the right tail. [verified + analysis]

A note against the record's pointed-at next lever: **the data does not support tightening the birth
structural stop** as a first move (§6, §8). Winner MAE is shallow (−0.24 R median), so a tighter
stop would mostly convert current winners into stop-outs.

---

## 2. Step 1 — Integrity & health

- **All three coins are alive and reconcile.** 26 ticks each, last tick 2026-07-14 16:55, latest
  bar 16:50, `status: running`. Each coin's journal row count equals its `state.json` `n_taken`
  (BTC 11, ETH 8, SOL 14), and recomputed hit/ΣR/final% match state to the reported precision. [verified]
- **Heartbeat is sparse but harmless.** 26 ticks over a ~157-hour span ≈ **17% of the intended
  hourly cadence (~1 tick per 6.1 h)** — GitHub throttles free-tier scheduled jobs heavily. The
  rolling re-scan window (~5.5 days) dwarfs the inter-tick gap, so the idempotent merge loses no
  trades; the durable journal is complete. Cosmetic, not functional. [verified]
- **No coin halted; the circuit breaker remains untested live.** All `halted: false`, and no coin
  drew past ±0.07% — nowhere near the −5% halt. So the pre-run's breaker-enforcement anomaly (equity
  rode to −8.5% in the replay path) **cannot be resolved by this window**; it stays an open task.
  Confirming the live breaker actually blocks new entries at −5% still requires either a forced-halt
  test or reading the enforcement path against a drawdown scenario. [verified]
- **Deployment matches the intended design.** Workflow on `main`, agent code checked out from
  `phase-5-birth-on`, pinned start 2026-07-08, coins BTC/ETH/SOL, X4 exit stack, state persisted to
  `paper-data`. Trade IDs are `p2_asbuilt-X4-###` (the E-birth arm + X4), as expected. [verified]

---

## 3. Step 2 — Performance, recomputed from raw

All figures recomputed from the `r` column; account % from `pnl_pct`; maxDD from the cumulative
`pnl_pct` curve. "Payoff" = avg win / |avg loss| (R); "PF" = Σwins / |Σlosses|.

| Set | n | hit | ΣR | mean R | median R | avg win | avg loss | payoff | PF | account % | maxDD % |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **BTC** | 11 | 36.4% | +8.64 | +0.785 | −0.382 | +3.37 | −0.69 | 4.88 | 2.79 | +0.066 | −0.016 |
| **ETH** | 8 | 25.0% | −0.94 | −0.118 | −0.316 | +1.29 | −0.59 | 2.20 | 0.73 | −0.007 | −0.012 |
| **SOL** | 14 | 35.7% | +8.96 | +0.640 | −0.487 | +3.19 | −0.78 | 4.11 | 2.28 | +0.067 | −0.026 |
| **POOLED** | 33 | 33.3% | **+16.65** | +0.505 | −0.382 | +2.91 | −0.70 | 4.18 | 2.09 | **+0.126** | −0.041 |
| *Pre-run BTC (ref)* | 31 | 25.8% | −0.54 | −0.017 | −0.504 | +1.91 | −0.69 | 2.78 | 0.97 | −0.003 | −0.079 |
| *E-birth X4 76-mo baseline [record]* | 9,920 | 21.9% | — | +0.082 | −0.500 | — | — | — | — | — | — |

Reading: pooled mean R **+0.505** is ~6× the retrospective baseline (+0.082) — but that gap *is* the
tail (see §4). Median R **−0.382** is close to baseline (−0.500) and is the more honest central-
tendency number: **the median trade is a partial-to-full loss**, exactly as expected. Winners hold a
median of **83 bars** vs losers **10 bars** — the system does let winners run and cuts losers fast;
the leak is give-back at the *end* of the winners, not premature loser-cutting (§6). [verified]

---

## 4. Step 3 — Tail dependence (the mandatory honesty line)

Results with the single best trade removed, per coin and pooled:

| Set | full ΣR | full mean R | drop best (R) | ΣR after | mean R after | hit after |
|---|---|---|---|---|---|---|
| BTC | +8.64 | +0.785 | +8.42 (closed) | **+0.22** | +0.022 | 30.0% |
| ETH | −0.94 | −0.118 | +2.41 | **−3.35** | −0.479 | 14.3% |
| SOL | +8.96 | +0.640 | +8.81 (**open**) | **+0.15** | +0.011 | 30.8% |
| POOLED | +16.65 | +0.505 | +8.81 (open) | **+7.84** | +0.245 | 31.2% |

**The decomposition. [verified]** Pooled +16.65 R = BTC tail **+8.42 R (closed)** + SOL tail
**+8.81 R (OPEN, `window_end` at 07-14 16:50, MFE 10.63 R)** = +17.23 R, and the **other 31 trades
net −0.58 R.** So:
- Strip the open SOL position: realized pooled = **+7.84 R over 32 closed trades**, carried by BTC's
  single closed tail.
- Strip both tails: the 31 remaining trades are **−0.58 R** — flat-negative.

This is not a failure; it is the profile. But the operative caveat is sharp: **one of the two trades
holding up the week is unrealized and could still reverse before it closes.** Any read of "SOL is
working" or "the week is green" that ignores this is unsafe. [verified]

---

## 5. Step 4 — Cohort census (by max favorable excursion)

Cohorts per the frozen diagnostics: NEVER_GREEN (MFE ≤ 0), STILLBORN (0 < MFE < 0.5R), FADED
(0.5 ≤ MFE < 1.0R), PROTECTED (MFE ≥ 1.0R).

| Cohort | BTC | ETH | SOL | **POOLED** | pooled ΣR | Pre-run | Baseline [record] |
|---|---|---|---|---|---|---|---|
| NEVER_GREEN | 0.0% | 0.0% | 7.1% | **3.0%** | −1.00 | 3.2% | ~3.9% |
| STILLBORN | 27.3% | 37.5% | 28.6% | **30.3%** | −9.08 | 38.7% | **39.1%** |
| FADED | 27.3% | 37.5% | 7.1% | **21.2%** | −2.11 | 29.0% | ~17.4% |
| PROTECTED | 45.5% | 25.0% | 57.1% | **45.5%** | +28.84 | 29.0% | **40.5%** |

**What it says. [verified + analysis]** Pooled STILLBORN (30.3%) is *lower* than the retrospective
E-birth baseline (39.1%), and PROTECTED (45.5%) is *higher* (40.5%). Taken at face value this looks
like the inverted-STILLBORN signature has softened. **But the more likely explanation is the regime:
all three coins ran mildly directional weeks (§7), so more entries reached +1R.** The baseline's
elevated STILLBORN was measured across all regimes including the ranging tape this system bleeds in.
One trending-ish week cannot distinguish "the structure problem is easing" from "the tape happened
to trend." **Do not claim the STILLBORN problem is fixed.** The loss remains entry-concentrated:
STILLBORN alone is −9.08 R of the −12.19 R gross loss across all losing cohorts; PROTECTED supplies
the entire +28.84 R of gross profit. [verified]

---

## 6. Step 5 — Structure-detection deep dive (focus area #1)

### 6.1 Grade and the base-detection bottleneck

Grade distribution across 33 trades: **thin 20 (60.6%), B 7 (21.2%), A 6 (18.2%).** Thin dominates
— less extremely than the old E-gated set (~88% thin) but still a clear majority.

| grade | n | hit | ΣR | mean R | median R |
|---|---|---|---|---|---|
| A | 6 | 33.3% | +3.28 | +0.547 | −0.234 |
| B | 7 | **57.1%** | +1.04 | +0.149 | **+0.090** |
| thin | 20 | 25.0% | +12.33 | +0.617 | **−0.671** |
| **based (A/B)** | 13 | **46.2%** | +4.32 | +0.332 | **−0.085** |

**The critical read. [verified]** A naive glance says "thin has the highest ΣR (+12.33) — thin is
fine." **That is a tail artifact.** Both week-defining tails (BTC +8.42, SOL +8.81) are thin-grade
capitulations; thin's ΣR ex-those-two is **−4.90 R across the other 18 thin trades.** On central
tendency, thin is the *worst* grade: lowest hit (25%) and worst median (−0.671 R). Base-graded
(A/B) births are far more reliable — **46% hit, −0.085 R median, and B specifically is the only
positive-median cohort (+0.090 R).** This directly validates the base-detection thesis: **base
presence buys per-trade reliability; its absence produces low-hit lottery tickets.**

Grade is gated on `base_present` at the code level (`birth_filter.py` L391–397: grade "A" =
`base AND premium`, "B" = `base`, else thin), and `base_present` depends on the lagging cover
mechanic (40-bar lookback, 50% cover, pivot-confirmation delay). So **thin-grade dominance is
mechanically downstream of base-detection lag, not a grading choice.** [verified]

### 6.2 A grading gap: spring-linked-but-baseless births are mislabeled thin

Of the 20 thin trades, 3 have a structural stop that differs from the signal stop — meaning they are
**spring-linked but have no detected base** (`build_entries` re-anchors only when
`base is None AND not spring_linked`). These have genuine structure (a swept-and-reclaimed level)
but are graded thin because grade keys on `base_present` alone; spring linkage only elevates grade
when a base is *also* present. Given base detection lags, some legitimately-structured spring setups
are being sized at 0.5× (thin budget) and admitted only through the aggressive/sweep-context side
door. [verified] This is a second facet of the base-detection bottleneck and a clean grading
hypothesis (§8).

### 6.3 Entry path: cross-births die, capitulations carry

| kind | n | hit | ΣR | mean R | median R |
|---|---|---|---|---|---|
| birth (EMA-cross origin) | 18 | 27.8% | +3.27 | +0.182 | **−0.799** |
| capitulation (gate-exempt) | 15 | 40.0% | +13.38 | +0.892 | −0.226 |

**[verified]** `kind=birth` — the whipsaw-filtered, gate-passing EMA-cross path — has a **−0.799 R
median and 27.8% hit. Most cross-origin births are losers.** The capitulation path (climax events,
gate-exempt) is both more reliable (40% hit, −0.226 median) *and* owns both tails. As with grade,
capitulation's +13.38 ΣR is the same two tail trades; ex-tails it is −3.85 R over 13 trades — so
capitulation is not "profitable underneath" either, but it is clearly the *less-bad and tail-
bearing* path. The uncomfortable implication: **the elaborate cross-birth funnel is the weak entry
link this week, and the simple capitulation trigger is doing the work.** Note the two tails are the
intersection — **thin-grade AND capitulation-kind** — so §6.1 and §6.3 are describing the same two
lottery tickets from two angles.

### 6.4 Per-coin structure mix

| coin | A | B | thin | birth | cap |
|---|---|---|---|---|---|
| BTC | 3 | 3 | 5 | 4 | 7 |
| ETH | 1 | 3 | 4 | 4 | 4 |
| SOL | 2 | 1 | 11 | 10 | 4 |

SOL is 11/14 thin and 10/14 cross-origin births — and **SOL has no Wyckoff context at all**
(`wyckoff_eligible: ["BTC","ETH"]`), so SOL births can only reach grade "A" via spring linkage,
never via `wyckoff_watch`. SOL is structurally biased toward lower grades, yet is the top ΣR coin —
because its one big thin capitulation tail dominates. This is the tail-artifact warning in miniature
and a reason to treat cross-coin grade comparisons cautiously. [verified]

---

## 7. Step 6 — Stop-placement deep dive (focus area #2)

### 7.1 Engagement and exit reasons

`exit_reason` encodes the stop source (`stop_{source}`), so it partitions cleanly:

| exit_reason | n | share | meaning |
|---|---|---|---|
| stop_ema_trail | 13 | 39.4% | trail engaged and was the exit stop (trail-protected) |
| opposite_cross | 10 | 30.3% | 9/89 EMA crossed back → hard-exit next open |
| stop_structural | 9 | 27.3% | died on the initial structural/signal stop (trail never protected) |
| window_end | 1 | 3.0% | still open at last bar (the open SOL position) |

**The trail engaged on ~39% of trades** — a healthy engagement rate versus the retrospective profile
where the median trade was a full stop-out. **Full stop-outs (r ≤ −0.95) are 33.3%** (11/33) — a
third of trades die at the initial stop, consistent with the low hit rate. There were **zero
`x_failure` exits** and no aging/time-stop exits (X4 has `aging=False` — confirmed no time-stop in
`replay.py` L67). [verified]

### 7.2 Are the initial stops mis-sized? Evidence says roughly well-calibrated

| MAE (R) | mean | median |
|---|---|---|
| on winners (r>0) | −0.278 | **−0.235** |
| on losers (r≤0) | −0.547 | −0.599 |

**[verified]** Winners dip only ~0.24 R against the position before working, and losers reach
~0.60 R adverse (median) before exiting — many via opposite_cross/trail *before* the full −1R stop.
Two implications: (a) stops are **not systematically too tight** — winners are not being shaken out
after digging near the stop and reversing (their MAE is shallow); (b) the loss side is already
partly managed below full-stop size (median loser −0.60 R, not −1.0). **This argues against the
record's "tighten the structural stop" as a first lever** — a tighter stop would mostly convert
shallow-MAE winners into stop-outs while only modestly helping the 33% that full-stop-out (§8.7).

Stop distances (initial risk as % of entry) confirm the base-anchored stop is materially **wider**
than the signal stop, and that width tracks grade:

| stop | median dist | | grade | median chosen-stop dist |
|---|---|---|---|---|
| signal | 0.193% | | A | 0.620% |
| structural | 0.359% | | B | 0.401% |
| chosen (= structural, always) | 0.359% | | thin | 0.244% |

`stop_chosen == stop_struct` on all 33 trades (`replay.py` L440 — the chosen stop is *always* the
structural stop; for thin births structural collapses to the signal stop). Based (A/B) births carry
0.40–0.62% stops (base-boundary-anchored); thin carry 0.24% (tight signal stop). This is the wider-
stop mechanic Phase 5 predicted, now confirmed per-trade. [verified]

### 7.3 The real leak: tail capture and give-back

| give_back_r (pooled) | min | median | mean | max |
|---|---|---|---|---|
| | +0.71 | +1.23 | +1.97 | +6.89 |

On the 8 trades with MFE ≥ 2R, the **mean capture ratio (realized R / MFE R) is 0.386** — the system
banks under 40% of the favorable excursion on its biggest movers. Concrete examples [verified]:

- BTC #11 (the tail): MFE **+14.14 R → +8.42 R** realized (gave back 5.72 R), exited opposite_cross.
- SOL #9: MFE **+12.08 R → +5.90 R** (gave back 6.18 R), opposite_cross.
- SOL #10: MFE **+6.86 R → −0.04 R** (gave back 6.89 R — the *entire* excursion), stop_ema_trail.

Mechanism: the e200 trail sits 0.5×ATR off a 200-EMA that lags **far** behind a fast directional
move. On a 10–14 R excursion, e200 is so far from price that when price reverses, the trail is only
reached after most of the move is surrendered — or, on SOL #10, the reversal never triggered the
opposite cross and the trail gave everything back. And **opposite_cross (30.3% of exits) hard-cuts
deeply-profitable trades**: BTC #11 and SOL #9 both exited on the 9/89 reversal while still far above
e200, forcing a give-back the trail would also not have prevented. [verified]

The asymmetry to respect: **the tails are the edge**, so the give-back is partly the *price* of
letting winners run, and any give-back reduction that clips the right tail is a net destroyer
[record]. But the win-side capture gap is the largest realized-vs-potential gap in the data, and
improving it does **not** touch entries or the survival-phase stop — making it a comparatively safe
place to look (§8.5).

### 7.4 FADED partitioned by engagement, and post-exit continuation

FADED (n=7) by exit: trail 4 / opposite_cross 2 / structural 1. STILLBORN (n=10) by exit:
structural 5 / trail 4 / opposite_cross 1. So about half of FADED/STILLBORN trades **did** engage
the trail before dying — this window does **not** strongly support the "FADED is mostly pre-
engagement round-trips" hypothesis (the trail was reached in ~half of cases). [verified, small n]

**Post-exit continuation: mean −0.198 ATR, median −0.321 ATR** (pre-run was +0.37). Negative — on
average price *reverses* after exit rather than continuing. So in this window exits are **not
systematically early**; if anything they land near local extremes (dominated by the opposite_cross
exits, which by construction fire when momentum turns). Another reason not to prioritize "exit
later" or "tighter survival stop" — the data doesn't show money left on the table after exit. [verified]

### 7.5 Account-sizing note

The paper account equity (`pnl_pct`, and therefore the −5% circuit breaker) is computed at **flat
0.75% risk per trade** — `paper.py` uses `r × risk_pct × deploy_scale` and omits the `grade_risk_mult`
budget (A 1.00 / B 0.75 / thin 0.50) that the journal's `weighted_r` column *does* apply. So the
live account treats every trade as full risk regardless of grade. This makes the equity path and the
breaker **more conservative** (larger swings) than a grade-weighted book, and means grade-based
position sizing is not currently reflected in the live account. Worth a decision for the next
iteration: should the paper account apply grade sizing (matching `weighted_r`), or is flat-risk the
intended conservative default? [verified]

---

## 8. Step 7 & 8 — Regime tag and synthesis (ranked hypotheses, no changes)

### Regime (coarse — no candle data in-session, so realized-vol/drift labels cannot be computed exactly)

From trade-level drift and direction mix [analysis]:

| coin | entry drift across trades | price range | L/S mix | read |
|---|---|---|---|---|
| BTC | +1.74% | ~4% | 6/5 | mild up / chop, balanced |
| ETH | +3.21% | ~4.4% | 6/2 | up-drift, long-biased |
| SOL | −2.09% | ~5% | 2/12 | down-drift, short-biased |

The three coins ran **different mild directional regimes** (BTC chop-up, ETH up, SOL down), each
with modest ~4–5% ranges over ~6 days — low-to-moderate volatility, mildly trending, **no strong
trend and no pure range.** Encouragingly, each coin's directional bias matched its drift (ETH longs
in an uptrend, SOL shorts in a downtrend), i.e. the gate is aligning direction correctly. Caveat:
this is inferred from trades, not measured from candles; and a mildly-trending week tells us little
about strong-trend or ranging behavior. [analysis]

### Ranked improvement hypotheses for the next iteration

Each is mechanism-justified, phrased so the journal can test it, and marked as a **future a-priori
frozen variant** — none is implemented against this window. All carry the n=33, one-week, one-regime
caveat.

**8.0 — [META, do first] Persist the full evidence dict + stop counterfactuals into the paper
journal.** This is a pure logging change — it does **not** touch the frozen strategy, so it can be
done immediately without spending virgin data. Add `base_present`, `sweep_context`, `spring_linked`,
`birth_status` (CONFIRMED/EXPIRED), `admitted_by`, `sep_atr_confirm`, `bars_to_confirm`,
`wyckoff_score`, and the engine-computed `r_sig_only` / `r_struct_only` counterfactuals to
`_JOURNAL_COLS`. **Rationale:** the 4b autopsy's strongest predictors (birth_status EXPIRED +40pp,
admission +22pp, base +19pp) and any stop-variant A/B are currently un-testable on forward data
because these fields are dropped. Every hypothesis below becomes measurable forward only once this
lands. **Highest leverage for learning; lowest risk to strategy.**

**8.1 — [Structure] Re-test the base-detection cover mechanic (v1_detection → v2_span_credit).**
*Evidence:* 60.6% thin; based births hit 46% vs thin 25%; grade is gated on `base_present` which
lags. *Mechanism:* `v2_span_credit` back-credits a detected box's full span, recognizing bases the
pivot-confirmation delay currently misses, moving cross-births from thin→B/A. *Forward test:* does
A/B share rise and thin's low-hit population shrink, **without** losing the capitulation tails (which
are thin+cap and independent of base)? *Caveat:* the audit already tried rewires that "mostly didn't
help," and a Phase-3 v2 variant underperformed by ~11 R — so this is a re-test on new data, not a
confident fix. [record + analysis]

**8.2 — [Structure/grading] Let spring-linkage alone qualify for grade B.** *Evidence:* 3 thin
births are spring-linked-but-baseless — real structure graded thin and sized at 0.5×. *Mechanism:*
change the grade-B condition from `base` to `base OR spring_linked`. *Forward test:* do promoted
spring-thin births improve in hit/median and does their 0.75× sizing help ΣR? *Caveat:* small
population; verify it doesn't admit low-quality springs. [analysis]

**8.3 — [Entry] Tighten the cross-birth path; leave capitulations alone.** *Evidence:* cross-births
−0.80 R median, 27.8% hit; capitulations carry reliability and the tails. *Mechanism:* require a
stronger confirmation for cross-origin births (e.g. `base_present` or a `birth_status` gate), while
the gate-exempt capitulation path is untouched. *Forward test (needs 8.0):* does gating out the
weakest cross-births raise pooled hit/median without reducing PROTECTED or the tails? *Caveat:*
killing weak crosses may not raise ΣR if it also removes occasional cross tails — test, don't assume.
[analysis]

**8.4 — [Entry] Investigate the 5 immediate stop-outs (bars_held ≤ 2, all −1R).** *Evidence:* five
entries were wrong within two bars, several thin. *Mechanism:* likely over-extended entries taken at
a local extreme. *Forward test (needs 8.0):* correlate immediate stop-outs with `sep_atr_confirm` —
if they cluster at high separation, the `birth_sep_atr_max` guard (currently 2.0, un-verifiable from
this journal) may want lowering as an a-priori variant. [analysis]

**8.5 — [Stop, win-side] Profit-scaled / faster trail hand-off to capture more of the tail.**
*Evidence:* capture ratio 0.386; give-backs of 5.7–6.9 R on the biggest movers; SOL #10 gave back
its entire +6.86 R. *Mechanism:* once a trade is deep in profit (e.g. MFE > 3R), hand the trail off
from e200 to a faster reference (the parked [FUTURE] e89 idea) or tighten the buffer, so a lagging
200-EMA doesn't surrender most of a fast move. *Forward test:* on trail-exited PROTECTED trades, does
the variant raise capture ratio **without reducing PROTECTED count**? *Caveat (critical):* asymmetric
risk — must be proven not to clip the right tail, since the tails are the edge. This is win-side, so
it does not touch entries or the survival stop. [record + analysis]

**8.6 — [Stop] Relax the opposite_cross hard-exit when deep in profit.** *Evidence:* opposite_cross
is 30.3% of exits and cut BTC #11 (+14.14 MFE → +8.42) and SOL #9 (+12.08 → +5.90) far above e200.
*Mechanism:* for trades with MFE above a threshold, suppress the opposite-cross hard-exit and defer
to the trail. *Forward test:* does deferring on deep-profit trades increase tail capture? *Caveat:*
opposite_cross is a legitimate invalidation for shallow trades — only relax it deep in profit. Ties
to 8.5. [analysis]

**8.7 — [Stop, LOW priority / flagged against the record] Do NOT aggressively tighten the birth
structural stop.** *Evidence:* winner MAE is shallow (−0.235 R median); post-exit continuation is
negative; median loser is already −0.60 R (not −1.0). *Assessment:* tightening would convert shallow-
MAE winners into stop-outs for only a modest reduction of the 33% full-stop-out tax. If tested at
all, it must be **moderate** (not aggressive) and validated that winner survival is preserved. This
explicitly disagrees, with reasoning, with the record's pointed-at next lever. [analysis]

**Deprioritized (unchanged from the record):** 4H MTF gate (~1pp stillbirth signal); broad exit-
timing retuning on the loss side (exit is the minority owner of loss, and post-exit continuation is
negative here).

### Top candidate to A/B forward

**8.0 (instrumentation) is the prerequisite; 8.1 (base cover) is the top *strategy* candidate.**
Sketch: build `phase-6-base-cover-v2` as a named frozen variant flipping `base_cover_mode` to
`v2_span_credit`, run it in **parallel paper alongside the current frozen X4 agent** (a genuine
shadow collection — the thing this project currently lacks), and after enough virgin windows compare
grade distribution, per-trade hit/median by grade, and pooled tail-adjusted ΣR. Pre-register the bar
and the sample floor before reading. The parallel-agent design also finally gives the alternative-
mechanics shadow record the operator asked about.

---

## 9. Appendix A — Architecture map (resolved from source)

Reading `structure.py`, `sfp_engine.py`, `wyckoff.py`, `birth_filter.py`, `replay.py`,
`paper.py`, `paper_live.py`, and `strategy_params.yaml` closed the handoff's open tags: [verified]

- **Pipeline:** trigger (whipsaw-filtered gated 9/89 cross, or gate-exempt capitulation) → birth FSM
  (PENDING→CONFIRMED on `sep_atr ≥ 0.50` with ribbon aligned inside a 6-bar window; else EXPIRED) →
  grade → admission → E-birth = admitted CONFIRMED births. (`birth_filter.py`)
- **Grade rule:** "A" = `base_present AND (spring_linked OR wyckoff_watch)`; "B" = `base_present`;
  else **thin**. Grade ∈ {A,B} ⟺ base detected — so **journal `grade` is a proxy for `base_present`**.
  (L391–397)
- **Admission:** thin (no-base) births admitted **only** under `aggressive` mode **and only with a
  same-direction MSB `sweep_context`**; `defensive`/`neutral` reject thin. (`admitted_modes`)
- **Base detection:** ≥50% of a 40-bar lookback is consolidation-or-rectangle-active; lags because
  pivots confirm `pivot_strength`(=3) bars late — the documented thin-grade lag. (`structure.py`,
  `base_lookback: 40`, `base_min_cover: 0.50`)
- **Stop selection:** `stop_chosen = stop_struct` **always**; for thin births structural collapses to
  the signal stop (trigger-bar extreme − 0.5×ATR under P1); based/spring use base-boundary or spring
  sweep-extreme ∓ 0.5×ATR. (`replay.py` L440, L245–260; `birth_filter.py` L400–424)
- **Exit lifecycle (X4):** initial structural stop stands until the e200 trail engages; trail arms
  only when a closed bar's close is on the trade's side of e200, then trails at `e200 ∓ 0.5×ATR`,
  never-loosen. No ratchet, no BE/lock, **no aging/time-stop**. Exits: `stop_structural`,
  `stop_ema_trail`, `x_failure`, `opposite_cross`, `window_end`. (`replay.py` L288–418, L401–409)
- **Wyckoff eligibility:** BTC and ETH only — **SOL gets no Wyckoff context**, so SOL grade "A"
  requires spring linkage. (`wyckoff_eligible: ["BTC","ETH"]`)
- **Not resolvable from the paper journal:** the full birth-evidence dict and the engine-computed
  `r_sig_only`/`r_struct_only` counterfactuals exist in `ReplayTrade` but are dropped by
  `paper_live.py` `_JOURNAL_COLS` (see §8.0).

---

## 10. Appendix B — Complete paper-trade data (all trades)

*Columns: L/S = long/short; risk_pct = initial stop distance as % of entry; exit reasons abbreviated
(`s_` = stop_); R / MFE / MAE / give-back in R units. Times UTC (MM-DD HH:MM).*

### BTC — 11 trades (live)

| # | L/S | kind | grade | entry_t | entry_px | risk% | exit_t | exit | R | MFE | MAE | give-back | bars | pnl% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | birt | thin | 07-08 21:20 | 62001.00 | 0.181 | 07-08 21:30 | s_structural | −1.00 | +0.03 | −0.81 | +1.03 | 2 | −0.0075 |
| 2 | S | capi | B | 07-09 02:00 | 61895.00 | 0.776 | 07-09 04:30 | s_ema_trail | −0.68 | +0.42 | −0.44 | +1.10 | 30 | −0.0051 |
| 3 | L | capi | thin | 07-09 14:25 | 62756.00 | 0.440 | 07-09 16:25 | s_ema_trail | −0.53 | +1.78 | −0.23 | +2.31 | 24 | −0.0040 |
| 4 | L | capi | A | 07-09 23:25 | 63269.00 | 0.135 | 07-09 23:30 | s_structural | −1.00 | +0.64 | −0.50 | +1.64 | 1 | −0.0067 |
| 5 | L | birt | A | 07-10 01:35 | 63326.00 | 0.270 | 07-10 14:30 | opposite_cross | **+4.75** | +7.97 | +0.00 | +3.22 | 155 | +0.0356 |
| 6 | L | birt | B | 07-10 22:15 | 64040.00 | 0.401 | 07-11 02:00 | s_ema_trail | −0.23 | +1.00 | −0.23 | +1.23 | 45 | −0.0017 |
| 7 | L | capi | B | 07-11 08:00 | 64146.00 | 0.277 | 07-11 10:25 | opposite_cross | +0.09 | +0.80 | −0.04 | +0.71 | 29 | +0.0007 |
| 8 | L | birt | thin | 07-11 17:40 | 64354.00 | 0.129 | 07-11 19:25 | s_structural | −1.00 | +0.43 | −0.80 | +1.44 | 21 | −0.0075 |
| 9 | S | capi | thin | 07-11 22:50 | 64166.00 | 0.244 | 07-12 03:30 | opposite_cross | +0.20 | +2.90 | −0.59 | +2.70 | 56 | +0.0015 |
| 10 | S | capi | A | 07-12 21:50 | 63944.00 | 0.504 | 07-13 00:10 | s_ema_trail | −0.38 | +0.83 | −0.33 | +1.22 | 28 | −0.0029 |
| 11 | S | capi | thin | 07-13 11:15 | 63082.00 | 0.141 | 07-14 00:00 | opposite_cross | **+8.42** | +14.14 | −0.23 | +5.72 | 153 | +0.0632 |

### ETH — 8 trades (live)

| # | L/S | kind | grade | entry_t | entry_px | risk% | exit_t | exit | R | MFE | MAE | give-back | bars | pnl% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L | capi | thin | 07-09 01:10 | 1755.10 | 1.075 | 07-09 01:40 | s_ema_trail | −0.81 | +0.03 | −0.80 | +0.84 | 6 | −0.0061 |
| 2 | S | birt | thin | 07-09 02:05 | 1733.80 | 0.900 | 07-09 04:35 | s_ema_trail | −0.40 | +0.76 | −0.35 | +1.16 | 30 | −0.0030 |
| 3 | L | capi | thin | 07-09 17:50 | 1748.10 | 0.880 | 07-09 21:40 | s_ema_trail | −0.23 | +0.73 | −0.22 | +0.95 | 46 | −0.0017 |
| 4 | L | capi | B | 07-11 01:30 | 1795.10 | 0.411 | 07-11 01:45 | s_ema_trail | −0.98 | +0.20 | −0.89 | +1.19 | 3 | −0.0074 |
| 5 | L | birt | B | 07-11 03:10 | 1795.10 | 0.424 | 07-11 10:05 | opposite_cross | +0.16 | +1.00 | −0.29 | +0.84 | 83 | +0.0012 |
| 6 | L | birt | B | 07-11 11:45 | 1799.50 | 0.286 | 07-11 22:20 | s_ema_trail | **+2.41** | +5.75 | −0.31 | +3.33 | 127 | +0.0181 |
| 7 | L | birt | thin | 07-12 11:50 | 1805.00 | 0.089 | 07-12 12:00 | s_structural | −1.00 | +0.19 | −1.00 | +1.19 | 2 | −0.0075 |
| 8 | S | capi | A | 07-12 21:55 | 1811.50 | 0.735 | 07-13 00:00 | s_ema_trail | −0.09 | +1.09 | −0.09 | +1.18 | 25 | −0.0006 |

### SOL — 14 trades (live) — *trade #14 is OPEN (window_end, unrealized)*

| # | L/S | kind | grade | entry_t | entry_px | risk% | exit_t | exit | R | MFE | MAE | give-back | bars | pnl% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | S | birt | thin | 07-08 21:15 | 76.97 | 0.390 | 07-08 21:45 | s_structural | −1.00 | +0.22 | −0.90 | +1.22 | 6 | −0.0075 |
| 2 | S | birt | thin | 07-09 02:55 | 77.12 | 0.558 | 07-09 04:30 | s_structural | −1.00 | +1.10 | −0.64 | +2.10 | 19 | −0.0075 |
| 3 | S | capi | A | 07-10 14:05 | 78.60 | 1.170 | 07-10 22:20 | opposite_cross | +0.63 | +1.64 | −0.08 | +1.01 | 99 | +0.0047 |
| 4 | S | birt | thin | 07-11 00:35 | 77.88 | 0.116 | 07-11 01:20 | s_structural | −1.00 | +1.47 | −0.65 | +2.47 | 9 | −0.0075 |
| 5 | S | capi | B | 07-11 01:35 | 77.94 | 0.359 | 07-11 06:00 | opposite_cross | +0.28 | +1.80 | −0.08 | +1.52 | 53 | +0.0021 |
| 6 | L | capi | thin | 07-11 06:25 | 77.97 | 0.154 | 07-11 07:05 | s_ema_trail | −0.34 | +0.82 | −0.60 | +1.16 | 8 | −0.0026 |
| 7 | S | birt | thin | 07-11 10:20 | 77.78 | 0.116 | 07-11 10:20 | s_structural | −1.00 | +0.00 | +0.00 | +1.00 | 0 | −0.0075 |
| 8 | S | birt | thin | 07-11 16:45 | 77.80 | 0.463 | 07-11 17:35 | s_ema_trail | −0.97 | +0.37 | −0.81 | +1.33 | 10 | −0.0072 |
| 9 | S | birt | thin | 07-11 22:30 | 77.92 | 0.244 | 07-12 09:50 | opposite_cross | **+5.90** | +12.08 | −0.59 | +6.18 | 136 | +0.0443 |
| 10 | S | birt | thin | 07-12 21:40 | 77.22 | 0.142 | 07-13 00:00 | s_ema_trail | −0.04 | +6.86 | −0.50 | +6.89 | 28 | −0.0003 |
| 11 | S | birt | thin | 07-13 01:50 | 76.76 | 0.534 | 07-13 07:35 | opposite_cross | +0.32 | +3.30 | −0.09 | +2.98 | 69 | +0.0024 |
| 12 | S | birt | A | 07-14 03:15 | 74.69 | 1.192 | 07-14 04:05 | opposite_cross | −0.63 | +0.18 | −0.66 | +0.81 | 10 | −0.0047 |
| 13 | S | birt | thin | 07-14 09:55 | 75.04 | 0.160 | 07-14 10:05 | s_structural | −1.00 | +0.43 | −0.60 | +1.43 | 2 | −0.0075 |
| 14 | L | capi | thin | 07-14 10:50 | 75.36 | 0.305 | 07-14 16:50 | **window_end (OPEN)** | **+8.81** | +10.63 | −0.75 | +1.82 | 72 | +0.0661 |

### Pre-run BTC replay — 31 trades (2026-06-10 → 07-07, reference only)

| # | L/S | kind | grade | entry_t | entry_px | risk% | exit_t | exit | R | MFE | MAE | give-back | bars | pnl% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | L | capi | B | 06-11 12:50 | 62940.40 | 0.748 | 06-11 15:00 | s_ema_trail | −0.91 | +0.55 | −0.63 | +1.46 | 26 | −0.0068 |
| 2 | L | birt | A | 06-11 17:45 | 63302.40 | 1.714 | 06-12 01:45 | opposite_cross | +0.04 | +0.56 | −0.06 | +0.53 | 96 | +0.0003 |
| 3 | L | birt | thin | 06-12 15:00 | 63971.10 | 0.668 | 06-12 15:55 | s_structural | −1.00 | +0.92 | −0.77 | +1.92 | 11 | −0.0075 |
| 4 | L | birt | thin | 06-14 08:25 | 64463.40 | 0.350 | 06-14 09:15 | s_ema_trail | −0.80 | +0.07 | −0.37 | +0.87 | 10 | −0.0060 |
| 5 | S | capi | thin | 06-16 13:15 | 66173.80 | 0.819 | 06-16 18:00 | s_ema_trail | +0.02 | +1.56 | −0.12 | +1.54 | 57 | +0.0001 |
| 6 | L | birt | thin | 06-17 02:15 | 65865.10 | 0.102 | 06-17 02:35 | s_ema_trail | −0.51 | +3.37 | −0.41 | +3.88 | 4 | −0.0039 |
| 7 | L | capi | thin | 06-17 15:30 | 65304.60 | 0.320 | 06-17 18:00 | s_ema_trail | +0.36 | +5.33 | −0.37 | +4.97 | 30 | +0.0027 |
| 8 | S | birt | thin | 06-18 14:00 | 63952.40 | 0.170 | 06-18 14:20 | s_structural | −1.00 | +2.52 | −0.88 | +3.52 | 4 | −0.0075 |
| 9 | S | birt | thin | 06-20 08:45 | 63422.80 | 0.503 | 06-20 09:35 | x_failure | −0.50 | +0.20 | −0.52 | +0.70 | 10 | −0.0038 |
| 10 | S | birt | thin | 06-20 13:25 | 63302.90 | 0.795 | 06-20 14:40 | s_ema_trail | −0.39 | +0.33 | −0.33 | +0.72 | 15 | −0.0029 |
| 11 | L | birt | thin | 06-21 19:25 | 64202.70 | 0.161 | 06-21 20:15 | s_structural | −1.00 | +0.39 | −0.96 | +1.39 | 10 | −0.0075 |
| 12 | L | birt | B | 06-22 05:20 | 64254.60 | 1.163 | 06-22 06:35 | s_ema_trail | −0.32 | +0.08 | −0.29 | +0.40 | 15 | −0.0024 |
| 13 | S | birt | thin | 06-24 03:20 | 62436.90 | 0.436 | 06-24 03:30 | s_structural | −1.00 | +0.00 | −0.78 | +1.00 | 2 | −0.0075 |
| 14 | S | birt | B | 06-25 11:00 | 61245.40 | 0.936 | 06-25 11:15 | s_ema_trail | −0.24 | +0.37 | −0.17 | +0.61 | 3 | −0.0018 |
| 15 | S | capi | B | 06-25 12:50 | 61314.80 | 0.901 | 06-25 21:45 | opposite_cross | +2.50 | +5.94 | −0.13 | +3.45 | 107 | +0.0187 |
| 16 | S | birt | thin | 06-27 11:45 | 60240.00 | 0.072 | 06-27 11:45 | s_structural | −1.00 | +0.00 | +0.00 | +1.00 | 0 | −0.0072 |
| 17 | S | birt | thin | 06-28 13:20 | 60070.00 | 0.065 | 06-28 13:20 | s_structural | −1.00 | +0.19 | +0.00 | +1.19 | 0 | −0.0065 |
| 18 | S | capi | thin | 06-28 22:10 | 59649.10 | 0.456 | 06-29 02:40 | s_ema_trail | −0.39 | +2.94 | −0.63 | +3.33 | 54 | −0.0029 |
| 19 | L | capi | A | 06-29 03:00 | 59731.80 | 0.975 | 06-29 05:05 | s_ema_trail | −0.12 | +0.84 | −0.12 | +0.96 | 25 | −0.0009 |
| 20 | L | capi | A | 06-29 05:50 | 59899.90 | 1.274 | 06-29 08:30 | s_ema_trail | −0.19 | +0.56 | −0.15 | +0.75 | 32 | −0.0014 |
| 21 | S | birt | B | 06-29 11:55 | 59785.20 | 0.675 | 06-29 12:00 | s_structural | −1.00 | +0.58 | −0.48 | +1.58 | 1 | −0.0075 |
| 22 | S | birt | B | 06-29 13:50 | 59371.00 | 1.581 | 06-29 15:45 | s_ema_trail | −0.59 | +0.41 | −0.52 | +0.99 | 23 | −0.0044 |
| 23 | S | birt | A | 06-30 21:30 | 58567.70 | 0.559 | 06-30 22:20 | opposite_cross | −0.57 | +0.25 | −0.65 | +0.81 | 10 | −0.0043 |
| 24 | L | capi | A | 07-01 02:15 | 58774.00 | 1.193 | 07-01 06:15 | s_ema_trail | +0.10 | +0.96 | −0.03 | +0.85 | 48 | +0.0008 |
| 25 | S | birt | thin | 07-01 06:35 | 58622.30 | 0.352 | 07-01 08:55 | s_structural | −1.00 | +0.83 | −0.85 | +1.83 | 28 | −0.0075 |
| 26 | L | birt | thin | 07-03 01:40 | 61700.00 | 0.363 | 07-03 02:25 | s_structural | −1.00 | +0.10 | −0.96 | +1.09 | 9 | −0.0075 |
| 27 | L | birt | B | 07-03 05:25 | 61609.50 | 0.549 | 07-04 01:50 | opposite_cross | +2.34 | +3.99 | −0.38 | +1.65 | 245 | +0.0175 |
| 28 | L | birt | B | 07-04 03:35 | 62637.70 | 0.887 | 07-04 05:35 | opposite_cross | −0.27 | +0.17 | −0.34 | +0.44 | 24 | −0.0020 |
| 29 | L | birt | thin | 07-04 12:30 | 62560.40 | 0.089 | 07-04 23:25 | opposite_cross | **+8.75** | +15.92 | −0.91 | +7.18 | 131 | +0.0656 |
| 30 | L | birt | thin | 07-05 07:55 | 62987.10 | 0.231 | 07-05 09:10 | s_structural | −1.00 | +0.67 | −0.94 | +1.67 | 15 | −0.0075 |
| 31 | L | capi | A | 07-05 21:25 | 62849.40 | 0.478 | 07-06 03:30 | opposite_cross | +1.16 | +3.80 | −0.05 | +2.63 | 73 | +0.0087 |

---

*Analysis by chat Claude under Fable mode, 2026-07-14. All performance figures recomputed this
session from the raw `paper-data` journals and reconciled to `state.json`. No parameter was changed;
this window is characterization-spent. Companion to the process retrospective and stop-loss companion
already in project knowledge.*
