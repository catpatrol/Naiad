# CENSUS-1 — Amendment 1 (pre-execution): the operator's four observations, folded in

**Date:** 2026-07-20 · **Status:** the original contract has **not** been executed — no G-7 pre-registration exists yet, so these are clean pre-registration amendments, not post-hoc changes. The original `Census_1_MTF_Signal_Stack_Builder_Contract.md` remains the authority for everything not amended here.
**Origin:** four operator observations (2026-07-20) on the census design, each scrutinized; three produced genuine enrichments, two produced framing corrections, and one produced a correction to the reviewer's own verdict, recorded in §1.

---

## 1. Corrections to the record (reviewer)

1. **The pocket verdict is downgraded from my "dead" to the accurate form:** *unsupported as a standalone gate on both measured books as currently defined (baseline: best-of-a-losing-field at n=60; B book: unremarkable at n=359, no sign-stable retracement band); retained as a candidate confluence factor; the operator's discretionary evidence explicitly noted as evidence of a different kind.* Two book-conditional measurements do not license "confidently irrelevant." Also for precision: **TC-1 never measured grades** (capture was off); the best-cohort result was S-1-era, on the old book.
2. **The 9/200 cross is stripped of its pre-assigned role.** The original §3.1 called it "the continuation-gap probe" — that was the reviewer's hypothesis wearing a definition's clothes. Both candidate roles are recorded — operator: mid-sequence reversal marker (canonically 9/89 → 9/200 → 89/200); reviewer: pullback-free continuation confirmer — and **D6 assigns its role from data.** The canonical ordering becomes D6's null expectation (§3.3 below).
3. **The governor question is per-mandate, not single-winner.** The fractal lens (standing frame) says different trading styles may want different governors; the census's product is a **map**, not a crown.

## 2. New deliverables (D8–D10)

**D8 — The cascade-ladder analysis (the add-ladder hypothesis).** Anchored on each *initiating* cross (any of the three types, any TF): the empirical chain of follow-on crosses across the stack — which cross, which TF, at what lag distribution — and, per rung of the chain, the **remaining forward MFE/MAE** (bps + ATR of the rung's TF) measured *from the follow-on event*. The question it answers, in the operator's words: does the time-based cascade itself constitute an entry-and-add schedule — 5m cross = entry, 30m cross = add, 1h cross = add — with meaningful move remaining at each rung? Report per governor lens, dual coordinates, CIs. (No new capture: computable from the §3.1 events + §3.3 outcomes as drafted; this amendment adds the missing *question*.)

**D9 — The confluence-factor scoring analysis (k-of-N).** The registered factor list — each computable trade-independently from the state vector and events, fixed here, never tuned:
F1 · 1D structurally aligned (e89>e200, direction-signed) · F2 · 12H structurally aligned · F3 · lens-governor regime aligned (e9>e89) · F4 · price beyond lens e89 · F5 · price beyond lens+1 e200 · F6 · a faster-TF 9/89 cross in-direction within the last 20 lens bars · F7 · 9/200 state aligned on the lens · F8 · exec ribbon separated ≥ 1.0 ATR in-direction · F9 · pullback-terminus-at-EMA flag (from D10, where applicable).
For each anchored moment: the count k of true factors, and forward MFE/MAE by k — the **dose-response curve**, per lens. This is the evidence base for the operator's flexible-entry framework ("enough of them present → trade"), and it is statistically kinder than conjunction-hunting: one monotonicity test instead of a combinatorial haystack. The fib pocket proper is *not* a factor here (it requires an arming leg, a trading construct); D10 tests its underlying mechanism instead, and the pocket competes as a factor in the v12 framework.

**D10 — The pullback-terminus zone-landing census (the operator's capitalized question).** Definitions: a **pullback terminus** = a confirmed (5,5) pivot low occurring while the lens governor is in long regime (mirror for shorts). For each terminus: distance to the lens's e89 and e200 (in lens-ATR), and to the lens+1's e200. **The null model, mandatory:** the same distances measured at random in-regime bars (matched by lens and regime, n ≥ 10× the terminus count, seed pinned) — because with 21 EMA lines on the field, *every* price point is near some line, and only excess clustering against the matched null is a finding. Deliverables: (a) the excess-mass ratio within 0.35 lens-ATR of each specific EMA (the Z2 width, used as the reference band); (b) the conditional outcome — subsequent 100-bar forward MFE for EMA-terminating vs non-EMA-terminating pullbacks. This tests the zone doctrine's foundation from *outside* the trading system, at census scale — and it is the trade-independent test of the pocket's underlying mechanism.

## 3. Amendments to existing sections

**3.1 — D2 is reframed as "the governor-per-mandate map":** for each candidate lens {1H, 4H, 12H, 1D}, outcomes at every horizon {20, 100, 500, regime-scale}, presented as a lens × horizon grid with the explicit reading: *fast horizons speak to intraday adoption, slow horizons to position adoption; different mandates may adopt different governors, and the map is the product.* P-C1 stands as registered — one row of the map, not its verdict.
**3.2 — §3.1's 9/200 line is replaced** with the role-neutral form per §1.2 above.
**3.3 — D6 gains its null:** the canonical reversal ordering 9/89 → 9/200 → 89/200 (mathematically near-necessary for a sustained monotone reversal) is the null expectation; the *deviations* are the findings — 9/89 crosses never followed by 9/200 (the whipsaw signature), and the 9/89→9/200 lag distribution (a trend-maturation clock).
**3.4 — §7 anti-fishing protocol extends to the new deliverables:** the D9 factor list is fixed above (rule 4 applies); D10's null seed and sample multiple are pinned in F-CFG; D8's chain analysis reports full lag distributions, never cherry-picked chains.

## 4. New predictions (pre-registered with the original six; the confirmatory set is now eight)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-C7a | Pullback termini cluster at the lens e89/e200 beyond the matched null: excess-mass ratio ≥ 1.3× within 0.35 lens-ATR, on ≥ 2 lenses | 60% | < 1.3× or single-lens only |
| P-C7b | EMA-terminating pullbacks carry higher subsequent 100-bar MFE (ATR) than non-EMA-terminating, sign-stable across ≥ 2 lenses | 55% | not sign-stable |
| P-C8 | The D9 dose-response is monotone: forward MFE (ATR, 100-bar) increases with factor count k (positive rank correlation, sign-stable across ≥ 2 lenses) | 60% | non-monotone or single-lens |

## 5. Fixture and artifact deltas

F-CFG additionally pins: the D9 factor list verbatim, the D10 null seed and ≥10× sample rule, the (5,5) pivot convention. F-FWD extends to D8's per-rung outcomes and D10's conditional outcomes (0 nulls on resolved anchors). Artifacts gain `census_ladder.jsonl` (D8 chains) and `census_termini.jsonl` (D10 events + null sample). Everything else — fixtures, the original six predictions, D1–D7, the annex discipline — carries verbatim.

## 6. The amended go-paste

```
CONTRACT: CENSUS-1 — execute under Amendment 1

Read Census_1_Amendment_1.md, then the original Census_1_MTF_Signal_Stack_Builder_
Contract.md, in full. The amendment adds D8 (cascade-ladder), D9 (k-of-N factor
scoring, list fixed), D10 (pullback-terminus zone-landing with matched null), reframes
D2 as the governor-per-mandate map, strips the 9/200's pre-assigned role (D6 assigns it
from data, canonical ordering 9/89→9/200→89/200 as the null), and extends the
predictions to eight. Everything else carries verbatim.

Order of work — as the original §12, with these deltas:

1. DEFINITIONS now also restate: the cascade chain and per-rung remaining move; the
   factor list and the dose-response question; the pullback terminus, the matched null,
   and WHY the null is mandatory (21 EMA lines — everything is near some line).

2. G-7 PRE-REGISTRATION commits all EIGHT prediction rows, the factor list verbatim,
   the null seed and sample rule, and the candidate-governor set — BEFORE any analysis.

3–5. Build, run twice, fixtures — as the original, with the §5 extensions.

6. DELIVERABLES D1–D10. D2 as the lens × horizon map. D6 against its canonical null.
   D8 with full lag distributions. D9 as the dose-response curve per lens. D10 with the
   null comparison printed beside every excess-mass claim.

7. ANNEX, PREDICTIONS (eight, falsifications first), artifacts, both ledger entries.
   Commit. Do not push, do not merge.

The original's Do-NOT list stands, plus: do not add, remove, or reweight any D9 factor ·
do not report a D10 clustering claim without its matched-null row beside it.

Report back: as the original, plus census_ladder.jsonl and census_termini.jsonl.
```

---

*Amendment prepared by the reviewer under Fable-mode, 2026-07-20. The operator's observations did what review is for: the ladder question the capture could answer but the contract never asked; the scoring framework that replaces dogma with a dose-response curve; the zone-landing test that takes the pocket's mechanism out of the trading system's shadow and puts it against a proper null; and a reviewer verdict corrected before it calcified into fact. The census now observes first everywhere — and every role it assigns, it assigns from data.*
