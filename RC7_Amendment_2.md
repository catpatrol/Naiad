# RC-7 — Amendment 2 (post-F3′ halt): the re-scope

**Date:** 2026-07-19 · **Authority:** the Amendment-1 fallback is **in force by its own terms** ("if the algebra is still wrong on the amended population, the reviewer is wrong twice and two-line pricing moves to S-2 — Path 3 by falsification"). The builder honored it: priced nothing, committed nothing, and posed the one question the fallback did not pre-decide — re-scope RC-7's simulator-independent tables, or hold the whole phase for engine 1.0.10. This document is that ruling. Operator veto stands on the usual silence basis.

---

## 1. Second halt, on the record

1. **F3′ violated by exactly one tranche:** BTCUSDT_intraday `c141t213` under `ema89_gov_b0.0` — a V-short whose campaign died the same wake; real book flattened at the next open (+0.0739R); the candidate's trail sat inside the death bar's range and the pinned simulator priced an intra-bar exit (−0.1961R) **the engine could never take**, because the wake flattens at the open (step 3a) before the intra-bar check (step 4).
2. **Root cause, now complete:** *the candidate simulator's bar-event ordering is not the engine's wake order.* Three faces, one defect: fill-bar coverage (halt 1), tie chronology (the 60), death-bar flatten precedence (this). Ordering defects are fixed by ordering, not by conventions.
3. **Everything else on the amended population satisfied the identity** — tie_stop_cand 10,894 · cand_earlier 197 · gap-ties 93 (0 assert failures) · open-flatten ties 11 of 12 — and the accounting closes exactly (3,732 × 3 = 11,196 = 11,184 + 12; fill-bar class 721 unique = 11.48%, candidate-invariant ×3 = 2,163; the 738/746/739 spread = the engagement-dependent tie class 17/25/18).
4. **Two reviewer errors recorded this halt:** the `campaign_died` reason was omitted from Amendment 1's open-flatten enumeration (it is a queued open-flatten, shipped at engine 1.0.5/G-4), and the §3.4 expected-cause guess for the count spread was wrong (it was the tie class, not data-edge resolution). Both stand in the ledger.
5. **Explicitly not ruled here:** whether the two-line rule itself priced `c141t213` correctly (plausible) — that claim is a third derivation from a reviewer 0-for-2 on this family, with no independent fixture left to check it. It gets **verified at S-2**, not asserted here.

## 2. The re-scope: RC-7r

**RC-7r delivers now (simulator-independent):**
- **Deliverables:** R7-2 … R7-11. R7-2 carries this mandatory caveat header: *"fold-in pinned-convention numbers; known bar-ordering infidelity (721-tranche fill-bar class + death-bar class, quantification deferred to S-2); valid for the concentration question only — not a TC-1 prediction basis."* All other tables are pure journal/sidecar tabulations.
- **Fixtures:** F1, F2, F4, F5, F6, F7, F8 (the F3 family is retired with its deliverable).
- **Predictions scored:** P-STRIP, P-LAT, P-FH1, P-FH2, P-FH3, P-FH4, P-PRVW — seven rows, verbatim from the original registration, still unseen.
- Print the standing descriptive line: **721 of 6,279 fills (11.48%) exit on the bar they are born.**

**Retired to S-2, carrying verbatim-unseen:** R7-1 (two-line pricing) → **R7-1′** · R7-12 (fill-bar bias) → **R7-12′** · predictions **P-2L-a / P-2L-b / P-2L-c** (registered, never scored, never seen — they transfer as-is and are scored against the corrected simulator's table).

## 3. S-2 scope accretion (third item this cycle — recorded now, executed there)

Engine **1.0.10** (S-2's instrumentation touch) now carries the full **simulator wake-order fidelity fix**: candidate exits derived under the engine's own event ordering — open-flattens first (all five reasons: `failure_x`, `opposite_cross`, `v_reversal`, `equity_floor`, **`campaign_died`**), then gap, then intra-bar, with fill-bar coverage from `fill_i`. Plus:
- The **semantics-delta fixture**: re-price a pinned set of known tranches under old vs corrected semantics and reconcile the difference to R7-12′'s measured bias.
- **`c141t213` becomes a permanent named regression tranche**: the corrected simulator must price it +0.0739R (the open-flatten), forever.
- R7-1′ (two-line, corrected) becomes **TC-1's prediction basis**; sequencing is now **RC-7r → S-2 → TC-1**.

## 4. Ledger entries (builder-typed, append-only)

```
[2026-07-19] RC-7 HALT 2 — F3′ violated by one tranche (BTCUSDT_intraday c141t213,
ema89_gov_b0.0): death-bar precedence — simulator priced an intra-bar trail exit on a
bar the engine had flattened at the open. Root cause complete: simulator bar-event
ordering ≠ engine wake order (fill-bar coverage, tie chronology, death-bar precedence —
three faces, one defect). Amendment-1 fallback IN FORCE: two-line pricing to S-2 by
falsification. Reviewer errors logged: campaign_died omitted from open-flatten
enumeration; §3.4 spread guess wrong (tie class, per builder's accounting). Amended-
population accounting closes exactly (11,196 = 11,184 + 12; 721 unique fill-bar =
11.48%). Priced: nothing.

[2026-07-19] RC-7 AMENDMENT 2 — re-scope ruling: RC-7r delivers R7-2..R7-11 now
(R7-2 under pinned-convention caveat), fixtures F1/F2/F4–F8, predictions P-STRIP/
P-LAT/P-FH1..4/P-PRVW verbatim. Retired to S-2 carrying verbatim-unseen: R7-1′,
R7-12′, P-2L-a/b/c. S-2 (engine 1.0.10) gains the wake-order fidelity fix (five
open-flatten reasons incl. campaign_died), the semantics-delta fixture, and c141t213
as a permanent regression tranche. Sequence: RC-7r → S-2 → TC-1 (TC-1 registers
against S-2's R7-1′).
```

## 5. The go-paste

```
CONTRACT: RC-7r — re-scoped re-run under Amendment 2

Read RC7_Amendment_2.md, then Amendment 1, then the original contract. Amendment 2
governs scope; everything it does not name carries unchanged.

Order of work:

1. Append the two §4 ledger entries, halt record first.
2. Drop the F3 family and R7-1/R7-12 from this run (retired to S-2 per §2-§3;
   P-2L-a/b/c transfer verbatim-unseen — do not score, do not peek).
3. Re-run fixtures F1, F2, F4–F8. Any MISMATCH: halt and report.
4. Deliverables R7-2..R7-11. R7-2 must print the §2 caveat header verbatim. Print the
   11.48% fill-bar death-rate line. Dual coordinates, JTO/TAO 1d handling, completeness
   rule — all per the original contract.
5. Score the seven surviving prediction rows, falsifications first.
6. Determinism (both hashes), artifacts, commit: scripts/rc7_recompute.py,
   RC7_RESULTS.md, rc7_results.json, ledger. Do not push, do not merge.

Report back: fixture table, the ten tables, the seven-row scorecard, both hashes,
rc7_results.json.
```

---

*Amendment prepared by the reviewer under Fable-mode, 2026-07-19. Two halts, two falsified reviewer claims, zero corrupted numbers — the fixtures spent days to keep the record clean, which is the exchange rate this project was built to pay. The plausible-but-unverifiable claim about two-line's faithfulness is left on the table deliberately: S-2's corrected simulator will test it, and `c141t213` will sit in the fixture set forever as the tranche that taught the simulator what order a bar happens in.*
