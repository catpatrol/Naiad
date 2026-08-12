# CENSUS-2A · RUN 5 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md`
 · ratified body `b0da051b…` (unchanged) · **+A1 +A2 +A3** → file `sha256 59363abab6c1ceec72efffe9139e5d9ad2800cdc2327e51b53cc0cd229d25e97`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (≤ 2024-07-01)

**Zero context assumed.**

---

## 0 · WHAT RAN

| | State |
|---|---|
| Hard assertions (15) + real F-PIN | **PASS** |
| **Amendment A3** appended | **DONE** — §1 |
| **CEN-4 CHOP-STATE** | **DONE** — P-iii-b and P-CHOP-1 scored, §2 |
| **A3-AUDIT** (v0.2→v0.3 compression diff) | **IN FLIGHT** — §5 |
| CEN-5 · CEN-7 · CEN-8 · CEN-9 | **REMAINING** |

---

## 1 · AMENDMENT A3

Appended to the queue item; **prior content byte-identical**, 0 CR bytes. Names three previously-unvalued `[VETO]`s (**A3-CHURN**, **A3-DECILE**, **A3-BAND**), confirms **A3-FAN-CONFIRM** — the FAN membership `{9,89,200,300,450,500}` that run 3 flagged as a builder's reading is now the reviewer's word — and orders **A3-AUDIT**. Re-pins nothing.

---

## 2 · CEN-4 · CHOP-STATE (complete)

Population: **7,117 births / 7,094 resolved**, I1-bounded, **panel 6,897 · annex 197 excluded** (R-F11).

### 2.1 · A3-DECILE did what it was named to do

| book | L n | `size_r=0.5` share | top asset share |
|---|---:|---:|---:|
| **A3-DECILE** (size-free, per-asset — **scored**) | 688 | **78.0%** | BTC **22.1%** |
| incumbent pooled-raw (**continuity only, never scored**) | 689 | **97.5%** | BTC **38.6%** |

The incumbent loser decile was **97.5% one position size** and **38.6% one asset** — substantially a position-size selector, as the run-4 scoping measured. The size-free per-asset ruling removes both biases. **This is the single most consequential ruling of the run**: every proportion delta below is computed against a cohort that is now a cohort of *outcomes*, not of *sizes*.

### 2.2 · The five components, counts only (I5), as-of the birth (I7)

| component | fires | of known | rate | NaN |
|---|---:|---:|---:|---:|
| churn (A3-CHURN, P80 expanding) | 1,642 | 6,657 | 24.7% | 240 |
| no-slow-arrival-yet (curtain-clean) | 5,182 | 6,897 | 75.1% | 0 |
| ribbon `c=0.5` (1h 9/89) | 2,170 | 6,897 | 31.5% | 0 |
| **verdict-open** (from CEN-6) | 1,673 | 6,897 | 24.3% | 0 |
| lens-concordance | 6,482 | 6,897 | 94.0% | 0 |

Composite distribution: `{0: 188, 1: 878, 2: 2,491, 3: 2,243, 4: 925, 5: 172}`.

**A3-CHURN's 240 NaNs are the rule working, not a gap** — the component is undefined until an asset has ≥90 days of its own history, and it is emitted as NaN rather than imputed.

### 2.3 · P-iii-b [65%] — text before result (F-8)

> *"Curtain-clean grind-at-birth over-represented in loser births (proportion delta, cluster CI), **both directions**."*

| | prevalence |
|---|---:|
| loser decile | 0.2209 |
| winner decile | 0.1526 |
| **delta** | **+0.0683** |

| | delta | cluster CI | |
|---|---:|---|---|
| pooled | +0.0683 | [+0.0362, +0.1020] | **EXCL-0** |
| long | +0.1013 | [+0.0590, +0.1643] | **EXCL-0** |
| **short** | +0.0393 | **[−0.0006, +0.0963]** | **straddles** |

**VERDICT: NOT SUPPORTED** — *pooled effect measured, but the registration's "both directions" clause is not met.*

**Short straddles zero by 0.0006.** That margin is reported, not rounded either way. The pooled effect is real and MC-1's direction is reproduced under a curtain-clean recut and a de-biased cohort; the registered text simply asks for more than the data gives. An earlier draft of my verdict logic checked only the pooled CI and would have returned SUPPORTED — the "both directions" clause is part of the hypothesis, not decoration.

### 2.4 · P-CHOP-1 [65%] — text before result (F-8)

> *"Chop-composite ≥3 captures ≥40% of loser-decile births at TRG ≥85%."*

| | value | needs |
|---|---:|---|
| loser-decile capture | **0.5814** | ≥ 0.40 ✅ |
| **TRG** (winner-decile profit retained) | **0.5466** | ≥ 0.85 ❌ |

**VERDICT: NOT SUPPORTED.**

**This is TRG earning its place in the frame.** The composite catches 58% of losers — comfortably past the capture bar — and would look like a good filter reported alone. It does that by deleting **45% of the winners' tail profit**. The contract requires both numbers printed together precisely so that a filter cannot be sold on the half that flatters it.

---

## 3 · TWO DEFECTS CAUGHT IN MY OWN DRAFT

**A median difference on a binary indicator is identically zero.** `cluster_ci` aggregates with the median, which is right for returns and wrong for a *proportion*: the median of a 0/1 vector is 0 or 1, so the delta was exactly 0 and P-iii-b's CI printed `[0.0, 0.0] straddles 0`. The registration says **proportion** delta — a mean. `cluster_ci` now takes an explicit `stat` selector and P-iii-b uses `mean`.

**`verdict-open` fired once in 6,897 births.** I had read it as `state == "NONE"` — "no verdict has ever occurred" — which is true of 0.75% of 4h bars. A component that never fires is not a component. Re-read as `state == "RESPECTED"` (the boundary is holding, no accepted break in force; 20.2% of bars), which is also the state `LEDGER.md:315` P-PD3 CONFIRMED points at — *"Z2's deficit concentrates in-range"*. **Flagged as a reading**, since the contract supplies the noun and not the mapping.

---

## 4 · FINDINGS REPORTED, NOT FIXED

1. **The incumbent loser decile was 97.5% one position size.** Every prior result scored against it inherits that; MC-1's P-iii figures are on the old book.
2. **P-iii-b fails only on the short side, by 0.0006.** A replication with more short births would likely settle it either way; it should not be re-scored on this book to chase the sign.
3. **The chop composite is a 45%-tail-cost filter.** Capture is not the problem; retention is.
4. **`verdict-open` and `lens-concordance` are readings**, not quotations — the contract names the components without defining the mapping.
5. **`lens-concordance` fires on 94.0%** of births. A component that is true of nearly everything contributes almost no discrimination to the composite — the same null-gate shape that got the TRAP stamp dropped by R-3.

---

## 5 · A3-AUDIT — IN FLIGHT

The v0.2→v0.3 compression diff (four slices: constants/invariants, CEN-0..4, CEN-5..9, registrations/fixtures) was launched at the start of this run and had not returned when the budget for whole stages was reached. **It is not reported here rather than reported thin.** Its seed case is already established and repaired: v0.2:135's `(close beyond + hold h bars [VETO] …)` was deleted by the compression and named by A2.

---

## 6 · CACHED vs REMAINING

**Cached:** preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · CEN-0b · CEN-1 · CEN-2 · CEN-3 · CEN-6 · **CEN-4**.

**Registrations of record:**

| | verdict |
|---|---|
| P-ARM-1 | NOT SUPPORTED (confounded by exposure time) |
| P-REL-1 | WITHDRAWN — unscoreable as written |
| **P-REL-1b** | **SUPPORTED-PROVISIONAL** (label permanent) |
| P-iii-b | NOT SUPPORTED — pooled measured, both-directions clause unmet |
| P-CHOP-1 | NOT SUPPORTED — capture passes, TRG fails |
| P-FAN-1 | filed next-cycle, unscored |

**Remaining:** CEN-5 · CEN-7 · CEN-8 · CEN-9; unscored P-NEST-1, P-i′, P-iv′, P-RAT-2, P-VBT-1; and the A3-AUDIT table.

---

## 7 · DISPOSITION (BOX-COST)

`cen4_book.parquet` (6,897 rows, `sha e5c1aefd3d74`) · `cen4_composition.parquet` (2, `3d6f116dc45e`) — both on `D:`. **Bus additions ≈ 0.15% of the box — under the 1% rule (F-14).** `exchange/` at **31.26%** (WARN, below refuse). census2a on `D:` = **47.2 MB**. Nothing named census2a on `C:`.

Pointers: `D:\Naiad\research_outputs\census2a\cen4\`

---

## 8 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12h ===
NOW: CENSUS-2A run 5. Amendment A3 named A3-CHURN, A3-DECILE, A3-BAND and confirmed the FAN
membership. CEN-4 ran to completion: five components as counts, P-iii-b and P-CHOP-1 both scored
NOT SUPPORTED for different and informative reasons. A3-AUDIT was launched and had not returned at
budget; it is not reported rather than reported thin.
LAST EVENT: 2026-08-12 — run 5: A3 named; CEN-4 complete; P-iii-b and P-CHOP-1 scored
FACTS:
- A3-DECILE MATTERS MORE THAN ANY SINGLE VERDICT. The incumbent pooled-raw loser decile is 97.5%
  size_r=0.5 and 38.6% BTC -- substantially a POSITION-SIZE selector. The size-free per-asset
  cohort is 78.0% / 22.1%. Every earlier result scored against the incumbent book inherits that
  bias, including MC-1's P-iii figures [verified]
- P-iii-b NOT SUPPORTED. Grind prevalence L 0.2209 vs W 0.1526, delta +0.0683, pooled cluster CI
  [+0.0362,+0.1020] EXCL-0; long +0.1013 EXCL-0; SHORT +0.0393 CI [-0.0006,+0.0963] STRADDLES BY
  0.0006. The registered text requires both directions, so the pooled effect being real does not
  carry it. The margin is reported, not rounded [verified]
- P-CHOP-1 NOT SUPPORTED, and this is TRG doing its job: capture 0.5814 (passes >=0.40) at TRG
  0.5466 (fails >=0.85). The composite catches 58% of losers by deleting 45% of the winners' tail
  profit. Reported alone, capture would have looked like a good filter [verified]
- TWO DEFECTS CAUGHT IN MY OWN DRAFT: (a) cluster_ci aggregated with the MEDIAN, which on a 0/1
  indicator is identically 0 -- P-iii-b's proportion delta printed CI [0.0,0.0] until the statistic
  was made explicit (mean for proportions, median for returns); (b) verdict-open was read as
  state=="NONE" and fired on 1 of 6,897 births -- re-read as state=="RESPECTED" (20.2% of bars),
  which is also the state LEDGER.md:315 P-PD3 CONFIRMED points at [verified]
- lens-concordance fires on 94.0% of births -- a component true of nearly everything adds almost no
  discrimination, the same null-gate shape that got the TRAP stamp dropped by R-3. Reported, not
  fixed [verified]
- A3-CHURN's 240 NaNs are the rule working: the component is undefined until an asset has >=90 days
  of its own expanding causal history, and is emitted NaN rather than imputed [verified]
PENDING:
1. A3-AUDIT table (v0.2 -> v0.3 compression diff) still in flight; report next run
2. P-NEST-2 [50%] FILED next-cycle, UNSCORED -- the FORWARD FALSE-POSITIVE question: given a nested
   LTF cross mid-bar, how often does the 4H actually confirm? Run 1 measured nesting prevalence
   backward from armings; the operator's question is the forward conditional, which is a different
   population and cannot be read off the run-1 table
3. THE D:-MOVED INCIDENT IS ROUTED TO ATHENA. On 2026-08-12 D:\\Naiad was moved to D:\\Archive\\Naiad
   by something outside the repo (daily_routine.py sweeps flat files only, skips directories, last
   ran 07:00). Restored on the operator's word, 123 files / 5,229,264,513 B verified identical. The
   census cannot survive its residency root vanishing mid-run; cause unidentified. ATHENA's lane
4. P-FAN-1 [60%] and P-ARM-2 [55%] still filed, unscored
5. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: CEN-5 -> CEN-7 -> CEN-8 -> CEN-9, then the A3-AUDIT table. Owner: HEPHAESTUS.
METRICS: operator actions this session = 1 (the A3 rulings paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 5 · A3 named, CEN-4 complete, two registrations scored honestly

---

# ⚠ ADDENDUM — A3-AUDIT RETURNED (same session, after §5 was written)

§5 said the audit was in flight and would be reported next run. It returned. **It found defects in this document**, so the correction lands here rather than a session later.

## A3-AUDIT · the headline

**The v0.2→v0.3 compression dropped operative content in more places than CEN-6's `h`.** Four slices produced **15 needs-word items**. Two of them had *already been silently substituted by builder readings inside a scored component*.

## P-CHOP-1 is WITHDRAWN

> ~~**VERDICT: NOT SUPPORTED.** capture 0.5814 at TRG 0.5466~~
> **VERDICT: WITHDRAWN — COMPUTED ON A MIS-SPECIFIED COMPONENT SET.**

Two of the five composite components were not the registered objects:

| component | registered | what I built |
|---|---|---|
| **lens-concordance** | v0.3:40 **pins** it: *"trailing-24h **same-rung-string agreement between the two chaining rules**; baseline 38.46%"* | count of 4h lattice-A events in a trailing 24h, firing at ≤1 — **an event-density proxy, a different quantity**. This is why it fired on 94.0% and read as a null gate. |
| **ribbon** | v0.2:40: *"0.5×ATR on **30m/1h** 9/89 spread"* (`mc2_program.py:162` swept both) | **1h only** — an unratified narrowing |

Both feed `composite ≥ 3`, so **0.5814 / 0.5466 are not the registered statistic in either direction**. The verdict is withdrawn rather than re-stated, because a number computed on the wrong component is not a finding whichever way it points.

**P-iii-b is NOT affected** — its predicate is `no_slow ∧ churn`, neither of which is implicated. **That verdict stands.**

## The other needs-word items, ranked

| # | Item | Halts |
|---|---|---|
| **NW-5** | **TRG's numerator under R-1.** v0.2 defined TRG on "top-decile **profit**" while the ruler was MFE−MAE. R-1 retired that ruler and **no text renamed the column**. Every TRG threshold (85/85/80%) rides on the answer. | P-CHOP-1, P-RAT-2, P-VBT-1, F-9 |
| **NW-2** | **Witness-correlation.** Defined only at v0.2:65-67 (pairwise sign-agreement across assets + panel return correlation). v0.3 keeps the obligation and drops the definition; **the term exists in no code**. | I8, F-16, CEN-8 |
| **NW-4** | **Sabotage fixture.** v0.2:62-63's defining parenthetical — *"one future bar → guard must REJECT"* — was dropped. **The identical failure shape as the `h` incident.** | F-10, CEN-8 |
| **NW-1** | **CEN-5 population.** v0.2:131 said "all **panel** assets"; v0.3:99 dropped the word, so annex would enter the 7,094 book against F-11. | CEN-5 |
| **—** | **P-NEST-1 is a live contradiction**: v0.3:124 scores it, while R-4 carries the nested object as UNCONFIRMED **columns-only**. | CEN-3/CEN-8 |
| **—** | **P-ARM-1's denominator**: v0.3:118 says "trigger-within-**151**"; CEN-2 computes `min(151, counter-arming)`, which closes 98.9% of windows. The phrase and the computation differ. | P-ARM-1 re-score |
| **—** | `no-slow-arrival-yet`, leap/stair (P-i′), ATR buckets + "survives" (P-iv′), H-VBT, the P-RAT-2 grid corner set | defined in **neither** draft — pre-existing, not compression losses |

Also flagged, and worth the operator's eye: **A1's `R-PAXG` contradicts the v0.3 body it claims not to alter** — the body orders "PAXG fetch NOW" (:71) and F-12 requires its classification printed (:139), while A1 orders the directory deleted. In practice F-12 *was* discharged before the deletion (run 3 printed first bar, evidence-era length and classification), so the contradiction is discharged in fact but not in text.

## What this changes about the run

The census now stands at **one supported registration** (P-REL-1b, SUPPORTED-PROVISIONAL) and **five withdrawn or not-supported**. The audit's deeper lesson is structural: **neither draft ever closed a register over its own `[VETO]`s** — three of v0.2's five `[VETO]` markers lived in module bodies, not §0, so compressing §0 could never have preserved `h`. That gap is unrepaired and will keep producing this failure until a closed VETO register exists.

