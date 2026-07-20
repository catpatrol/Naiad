# S-2b — Architecture Decomposition Addendum — Builder Contract

**Phase:** v12 Study · **Tier A** (arithmetic over the existing S-2 journals + sidecars; joins to S-1/pass-2 by `tranche_id`). **No engine execution, no config change, no network, no evidence spend.**
**Basis:** S-2 verified PASS (engine 1.0.10, completion `6fdab03`, pushed). In-session scan answers (a)–(d) of 2026-07-19 are the known-answer fixtures of this phase.
**Purpose in one line:** put the four surviving stop/exit architectures — baseline · corrected fold-in · F4-static-30m · F4-static-1h — on **one comparable footing** (per-mandate, strip-best, cost-decomposed, distributions), so the operator's D-2 re-ruling and the TC-1 re-scope read from a table instead of a headline.
**Standing caveats on every table:** in-sample · first-order (rail/halt/equity feedback ignored; entries fixed) · 1×-proxy costs · struct-book R is denominated in the **wider structural `one_r`** while baseline/fold-in R is baseline-denominated — every cross-architecture table states its denominator; the flatten-reason split remains the disclosed proxy.

---

## 0. Operator instructions

Save this file into the repo → `claude` → paste §7. Runtime: minutes. *What you should see:* definitions restatement → fixture table (five rows, all MATCH — they pin this phase to the in-session scan) → six deliverables → a five-row prediction scorecard → determinism hashes. Any MISMATCH: builder halts, reports, produces nothing downstream. Send back `s2b_results.json`, the fixture table, the scorecard.

## 1. What this phase is / is NOT

**Is:** eleven tables of journal arithmetic that decompose the two S-2 winners and mirror the same decomposition onto fold-in and baseline. **Is NOT:** a run (nothing executes) · TC-1 (no rule trades) · a pricing of the **ratcheting-structural variant** (named-unmeasured; it appears in the decision table as a labeled blank, never a number) · a joint struct+trail architecture estimate **unless** per-tranche exit prices/bars for both books are journaled (D6 carries the PARTIAL protocol) · a slot decision.

## 2. Definitions

Carried verbatim: cell-R, R/unit, signed `one_r`, 0×/1×-proxy, toll, fill_class, strip-best, dual coordinates. **New:** **struct-R** = R denominated in the structural stop's `one_r` (wider); **baseline-R** = the standing denominator; **denominator ratio** = struct stop distance ÷ baseline stop distance, per tranche, in bps; **m=2 overlap** = share of the bps-floor-flagged fills (stop_bps < 2×toll under the *baseline* anchor) whose *structural* stop distance clears 2×toll; **ride-to-death bucket** = the flatten-with-no-baseline-flatten-reason class from the in-session census.

## 3. Fixtures — known-answer gates from the verified record and the in-session scan

| # | Fixture | Expected |
|---|---|---|
| F1 | Baseline recompute (1× / 0× / campaigns / win) | −1,796.9930 / +275.9924 / 2,599 / 10.8503% |
| F2 | F4 exit-reason census totals reproduce the scan | 30m: 4,493/9/15/1,755/7 rows, book +363.5363 · 1h: 3,997/8/15/2,259/0, book +565.5794 |
| F3 | Cost stacks reproduce the scan | 30m 742.94 · 1h 606.99 · baseline 2,072.98; 1h decomposition +1,466.0 (62%) / +896.6 (38%) |
| F4 | Corrected fold-in reproduces R7-1′ | grid 0× +506.279 · position 1×-proxy +384.2388 (b0.5) |
| F5 | Determinism | double-run hashes identical |

## 4. Deliverables

**D1 — The architecture decision table (the phase's product).** Rows: baseline · fold-in corrected (b0.5) · F4-static-30m · F4-static-1h · *F4-ratcheting (named-unmeasured — blank row, present by design)*. Columns: grid and per-mandate {0×, 1×-proxy, strip-best 1×, win rate, campaigns/tranches, cost stack, denominator note}. **The per-mandate F4 books are the unseen heart of this phase** — especially whether intraday flips positive under the wider-bps anchor.
**D2 — Concentration:** per architecture per mandate, strip-best and the top-10 campaign share of Σ1×; flag any book whose sign flips on strip-best.
**D3 — Distributions:** per architecture, holding time (bars fill→exit, per mandate), win rate by exit reason, and for the F4 books the **denominator-ratio distribution** (struct÷baseline stop distance in bps) per mandate and per detection TF — the "how much wider, where" table.
**D4 — Fold-in mirror decomposition:** the same (b)+(d) treatment applied to corrected fold-in — exit-reason census (trail exit vs native stop vs flatten), cost stack, and its swing vs baseline split into cost-identity vs gross components (expected near-zero cost-identity: same entries, same denominator — the fixture-grade check that the decomposition method itself is sound).
**D5 — The same-lever quantification:** the m=2 overlap — of the 3,813 bps-floor-flagged fills, the share whose 30m / 1h structural distance clears 2×toll; plus the complement (fills the floor passes but the struct anchor still leaves under 2×toll). Purpose: states exactly how much of TC-2's floor the F4 anchor already owns.
**D6 — Joint first-passage estimate (optional, PARTIAL protocol):** *if and only if* per-tranche exit bars **and prices** are journaled for both the struct and corrected-trail books: the joint architecture (structural stop + gov-e200 trail exit + campaign flatten, first touch wins), denominated in struct-R. If prices are absent: mark PARTIAL, name the missing field, deliver nothing estimated. The real interaction is TC-1's fourth cell either way.
**D7 — One paragraph for the record:** the ride-to-death bucket's per-mandate anatomy (n, mean cell-R, mean bars) — the shape of what the doctrine actually buys.

## 5. Pre-registered predictions (scored on the genuinely-unseen cuts only)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-S2b-1 | F4-1h **intraday** book is positive at 1×-proxy | 60% | ≤ 0 |
| P-S2b-2 | F4-1h grid book survives strip-best positive | 65% | flips |
| P-S2b-3 | Fold-in's cost stack within ±15% of baseline's 2,072.98 (decomposition-method sanity) | 70% | outside |
| P-S2b-4 | ≥70% of the 3,813 m=2-flagged fills clear 2×toll under the 1h structural anchor | 60% | <70% |
| P-S2b-5 | F4-1h median holding time ≥ 3× baseline's, per mandate (the room is time, not just distance) | 60% | any mandate < 3× |

## 6. Verdict, artifacts, ledger

**PASS** — 5/5 fixtures; D1–D7 delivered (D6 PARTIAL allowed); 5/5 predictions scored, falsifications first; determinism proven. **HALT** — any fixture MISMATCH. Artifacts: `scripts/s2b_decompose.py` · `S2B_DECOMPOSITION.md` · `s2b_results.json` · ledger entry (Tier A, evidence spend NONE, "D-2 re-ruling reads from D1; TC-1 re-scope drafts against this table"). Commit; **do not push, do not merge.** Standing note recorded for S-3+: control strata drawn excluding pinned keys.

## 7. The go-paste

```
CONTRACT: S-2b — Architecture Decomposition Addendum (Tier A — journals only)

Read S2b_Decomposition_Addendum_Builder_Contract.md in the repo in full first. The
contract is the authority; this paste is the trigger.

Scope in one line: eleven tables putting baseline, corrected fold-in, F4-static-30m and
F4-static-1h on one comparable footing — per-mandate books, strip-best, cost
decompositions, distributions, the m=2 overlap, and the D-2 decision table. Read-only.
No engine execution, no config changes, no network.

Order of work — mandatory:

1. DEFINITIONS (contract §2). Restate in your own words: struct-R vs baseline-R and why
   every cross-architecture table must state its denominator; the ride-to-death bucket;
   the m=2 overlap; why the fold-in mirror decomposition should show near-zero
   cost-identity component (and what it means if it does not).

2. FIXTURES (contract §3, F1–F5) from raw journal bytes. The in-session scan of
   2026-07-19 is the known answer.

   *** ANY MISMATCH: HALT. Report computed vs expected. Produce nothing downstream. ***

3. DELIVERABLES D1–D7 (contract §4). D1 first — the decision table, with the
   F4-ratcheting row present and BLANK (named-unmeasured, by design). D6 only if
   per-tranche exit bars AND prices exist for both books; otherwise PARTIAL with the
   missing field named. Every table states its denominator.

4. PREDICTIONS (contract §5) — all five, falsifications first.

5. DETERMINISM (run twice, print both hashes), artifacts, ledger entry per §6. Commit.
   Do not push, do not merge.

Do NOT, even if it seems helpful: execute replay or any engine code · price the
ratcheting variant · estimate D6 without journaled prices · modify anything · touch the
lockbox · substitute estimates for missing fields.

Report back: definitions restatement, fixture table, D1 first then D2–D7, the five-row
scorecard, both hashes, s2b_results.json.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-19. The in-session scan answered (a)–(d); this phase makes those answers reproducible, extends them to the cuts nobody has seen, and produces the one table the next two rulings stand on. The ratcheting variant sits in D1 as a labeled blank — present so the operator rules on the full menu, blank so nothing unmeasured wears a number.*
