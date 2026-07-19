# RC-7 — Amendment 1 (post-F3 halt)

**Date:** 2026-07-19 · **Authority:** builder halted per contract §8 (F3 MISMATCH, 2,223 violations, nothing priced, nothing committed); amendment paths were explicitly the reviewer's call. This document is that ruling. Operator veto applies as always; defaults stand on silence.
**Status of the original contract:** `RC7_PostS1_Recompute_Builder_Contract.md` remains the authority for everything not amended here. This document changes **one fixture, one convention, adds one deliverable and one required explanation** — nothing else.

---

## 1. What the halt established (for the record)

1. **Falsified: the reviewer's identity algebra.** The claim "two-line = fold-in on the zero-advance population" assumed the baseline and candidate exit processes cover the same bars. They do not: the live book checks the intra-bar stop **on the fill bar itself** (`trading.py` step 4), while the S-1 candidate simulator (`engine/s1.py::simulate_exit`, deliberately inheriting `shadows._sim_stop_exit`'s pinned semantics) begins at `fill_i + 1` and **cannot represent a fill-bar exit**. 2,163 of 2,223 violations are that single mechanical class (~740 tranches × 3 candidates); the remaining 60 are same-bar both-hit ties the original convention resolved against engine chronology.
2. **Unimpeached: the S-1 data.** F1/F2/F4–F7 reconcile exactly. The fold-in scorecard numbers stand *as fold-in numbers under their pinned convention* — with a now-identified infidelity to engine semantics on the fill-bar class, to be quantified (R7-12) rather than hand-waved.
3. **Verified: the implementation tested the registered spec faithfully** (`rc7_recompute.py:226–246`, reviewer-read). The falsification is of the specification's algebra, not of the builder's code. Third reviewer claim falsified by the project's own instruments; the fixtures exist precisely so these die in contracts instead of in runs.
4. **Free descriptive finding:** ~740 of 6,279 resolved tranches (**≈11.8% of fills die on the bar they are born**). Print as a standing line in the amended report.

## 2. The ruling

**Amendment Path 1 is adopted, modified:** re-scope the fixture population **and** flip the tie convention (which dissolves the 60-tranche tie class into the identity instead of excluding it). Path 2 (re-pin the simulator now) is **rejected for sequencing** — it is an engine change (1.0.10) forcing a fresh instrumented run for a Tier-A pricing job; it is **re-homed into S-2's engine touch** with a semantics-delta fixture (§5). Path 3 (hold all two-line pricing) is **rejected**: under this amendment the two-line rule is engine-faithful on exactly the class that broke — a fill-bar stopout resolving to baseline *is* "the native line exited first."

## 3. Contract deltas (exhaustive — nothing else changes)

**3.1 — Pricing rule (§4 of the original), one-character class change + one edge:**
- `use_cand = (co is not None) and (co ≤ base_off)` — ties now resolve to **candidate** (for a long, a falling bar reaches the higher trail before the lower native stop; a gap below the trail fills at the open — candidate either way).
- **Edge (learned this phase, pinned now):** a tie where the baseline exit is a queued **open-flatten** (`failure_x`, `opposite_cross`, `v_reversal`, `equity_floor`) resolves to **baseline** — the open executes before any intra-bar path. Ties where the baseline is `stop_gap` (both lines gapped at the open) should price identically either way; **assert** equality there rather than choosing.
- The fill-bar class needs no special case in the pricing rule: `co ≥ 1 > 0 = base_off`, so those tranches fall to baseline automatically — which is engine truth.

**3.2 — Fixture F3′ (replaces F3):**
- Population: zero-advance (`n_stop_advances = 0`) **AND `base_off ≥ 1`**.
- Claim: two-line = fold-in **exactly** (same exit bar, same R at 1e-4) on this population, per candidate. Expected violations: **0**.
- Additionally report: the excluded fill-bar class size (expect ~740 unique tranches) and the tie-class size now satisfying identity under 3.1.

**3.3 — New deliverable R7-12 — fill-bar bias quantification.** For the excluded class, per candidate and per mandate: n, Σ(candidate `exit_r` × size) vs Σ(baseline realized), the delta in cell-R, and the share of the class where the candidate exit was *better* than the stop (the simulator rode a recovery). **Purpose:** prices how far the S-1 fold-in scorecard (+584.50 Σ0× etc.) sits from what a real fold-in run would show, and becomes the correction lens for every fold-in figure in Report 3.

**3.4 — Required explanation (report text, not a fixture):** the per-candidate violation counts (738/746/739) for a candidate-independent class — account for the spread exactly (expected cause: per-candidate exit-resolution differences at the data edge; do not assert, show).

**3.5 — Veto table V1 (original contract §11) is amended** to the 3.1 convention. All other vetoes stand.

## 4. What carries verbatim

All deliverables R7-1…R7-11 · all ten prediction rows **unchanged and unseen** (nothing was priced before the halt; the registrations remain honest — this is the governance point: amendments after a halt-with-no-data touch definitions only; predictions re-registered after a peek would be worthless) · fixtures F1, F2, F4–F8 (already MATCH; re-run and re-print) · invariants, bases, seeds, coordinate conventions, JTO/TAO handling · verdict criteria (§8), including: **any F3′ violation halts again** — if the algebra is still wrong on the amended population, the reviewer is wrong twice and two-line pricing moves to S-2 (Path 3 becomes the ruling by falsification).

## 5. S-2 scope addendum (recorded now, executed there)

The S-2 engine touch (1.0.10) gains: **candidate-simulator fill-bar coverage** (exit checks from `fill_i`, engine-faithful), plus a **semantics-delta fixture** re-pricing a pinned set of known tranches under both conventions and reconciling the difference to R7-12's measured bias. Until then, every fold-in number cited anywhere carries the R7-12 correction as a footnote.

## 6. Ledger entries (builder-typed, append-only — two entries)

```
[2026-07-19] RC-7 HALT — F3 identity falsified (2,223 violations; 2,163 fill-bar-exit
class, 60 tie class). Root cause: reviewer's derivation assumed identical bar coverage
between live book (fill-bar stop check, trading.py step 4) and candidate simulator
(begins fill_i+1, pinned S-1 semantics). Implementation verified faithful to spec.
Nothing priced, nothing committed. S-1 data unimpeached (F1/F2/F4–F7 exact).
Finding: ~11.8% of fills exit on their fill bar. Reviewer claim falsified — 3rd of
project; fixtures functioning as designed.

[2026-07-19] RC-7 AMENDMENT 1 — ruling: Path 1 modified. F3′ population excludes
base_off=0; tie convention flipped to candidate (co ≤ base_off) with open-flatten
edge; +R7-12 fill-bar bias table; per-candidate count spread explained; predictions
carry verbatim (unseen). Simulator fill-bar fix re-homed to S-2 (1.0.10) with
semantics-delta fixture. Re-run authorized.
```

## 7. The amended go-paste

```
CONTRACT: RC-7 — re-run under Amendment 1

Read RC7_Amendment_1.md, then the original RC7_PostS1_Recompute_Builder_Contract.md.
The amendment overrides §4's tie convention, replaces F3 with F3′, adds R7-12 and one
required explanation. Everything else — deliverables R7-1..R7-11, all ten predictions
(verbatim, still unseen), fixtures F1/F2/F4–F8, invariants, seeds — carries unchanged.

Order of work:

1. Append the two §6 ledger entries (halt record first — the falsification is part of
   the permanent record, not something the amendment erases).
2. Apply the deltas: pricing rule co ≤ base_off with the open-flatten tie edge and the
   stop_gap equality assert; fixture F3′ (zero-advance AND base_off ≥ 1; expect 0).
3. Re-run fixtures F1–F8. *** ANY F3′ VIOLATION: HALT AGAIN — the reviewer is wrong
   twice, and two-line pricing moves to S-2 by falsification. Report, price nothing. ***
4. Deliverables R7-1..R7-12, including the fill-bar bias table and the count-spread
   explanation. Print the 11.8% fill-bar death-rate line.
5. Predictions, determinism, artifacts, commit — exactly per the original §§7–9.
   Do not push, do not merge.

Report back: fixture table (F3′ prominent), the twelve tables, the scorecard, both
hashes, rc7_results.json.
```

---

*Amendment prepared by the reviewer under Fable-mode, 2026-07-19. The original derivation, its falsification, and the amended claim all stay on the record side by side — that is the point of the record. The amended identity is narrower and should be exactly true; if it is not, the fixture will say so, and the fallback is already ruled.*
