# TC-4 — Engine 1.0.8 Guards + Re-Anchor — Builder Contract

**Phase:** v12 Study · **Tier C** (engine changes + full re-run) — **G-7 binds: the ledger pre-registration in §7/§10 must be committed BEFORE the run executes.**
**Baseline being superseded:** V3 anchor — engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5…`), 20 cells, exploration-classic. Scored-clean reference: **−5,093.7846** (F6, RC phase).
**Operator ratifications in force:** G-8 guards (2026-07-16, "a necessity"); TC-4-first-then-re-anchor (E.1); G-8a floor = **25% of initial** (2026-07-17); 1H/5m intraday re-spec **pre-registered only** (2026-07-17); 3-strike rescoped to a re-entry quality bar, **deferred to TC-2** (2026-07-17); `ext_before_exit` correctness fix folded into 1.0.8 (2026-07-16).

---

## 0. Operator instructions

1. **Save this contract file into the repo** (top level, next to `LEDGER.md`) before launching — last phase's contract lived in `~/Downloads` and origin couldn't see it. The builder commits it with the phase.
2. PowerShell → repo → `claude` → `git status` → expect `On branch v12-v1-census`, clean, up to date with origin (you pushed the RC phase).
3. Paste the go-paste (§11). Enter.
4. *What you should see, in order:* (a) a **pre-run expectation table** (floor-crossing dates computed from the old journals); (b) a **ledger pre-registration commit** — the run has not happened yet at this point; (c) the run itself (20 cells, full window — expect the longest compute of the project so far, tens of minutes to hours, not seconds); (d) a fixture table, **all MATCH**; (e) the prediction scorecard.
5. Any fixture MISMATCH → builder halts and reports. The run is not "mostly fine" — a guard that doesn't provably hold is a guard that doesn't exist.
6. Send back: pre-run expectation table, fixture table, prediction scorecard, `tc4_baseline.json`, and the new baseline's rollup. I verify before anything becomes "the baseline."

---

## 1. What this phase is

Engine **1.0.8**: four hard guards (G-8a–d), two journal-schema additions, one enrichment correctness fix — then one full 20-cell re-run of exploration-classic that becomes the project's **new baseline**. Everything downstream (S-1, TC-1/2/3/5) runs on these journals.

## 2. What this phase is NOT

- **Not S-1.** No candidate ratchets, no new shadow families, no MTF capture, no zone-geometry shadows. Instrumentation comes next, on top of this baseline, with a byte-identity acceptance test against it.
- **Not TC-2.** The re-entry quality bar is designed from S-1 measurements; nothing here gates re-entries beyond the four guards.
- **Not the 1H/5m re-spec.** That candidate is **registered** in the ledger this phase (§10) and **not run**.
- **Not a strategy redesign.** `signals.py` is untouched. The only behavioral deltas are the four guards. Anything else that changes a traded number is a defect.
- **Not the cost-aware bps floor.** Identified this cycle (cost-in-R = cost_bps/stop_bps; an ATR floor can still admit 3 bps stops on 1m charts) — that is an S1-8 sweep axis and a TC-2 candidate, explicitly out of scope here.
- **Not a maker/chase cost model.** Deferred per operator ruling 3.b.

## 3. The 1.0.8 change set

### G-8a — Equity floor (ratified: 25%)
`trading.equity_floor_frac: 0.25`. Evaluated whenever realized equity updates (exits, funding). On breach (`equity < 0.25 × initial_equity`): queue flatten of all open tranches at next bar open with `exit_reason="equity_floor"`; journal a HALT row with `scope="equity_floor"`; the cell takes **no new entries for the remainder of the run** (permanent, unlike day/week halts). The flatten itself may realize below the floor — that is correct behavior, then silence.

### G-8b — Notional cap (default: reject at 10× leverage)
`trading.max_notional_leverage: 10`. At entry sizing, if `|qty| × px_fill > 10 × equity`: **reject** the entry, `reject_reason="notional_cap"`. Reject, not resize — resizing would mint fractional-R tranches and break 1R semantics. **[A-priori choice, veto item V2.]**

### G-8c — Minimum stop distance (ratified: 0.5 ATR)
Extend the existing `unit_risk <= 0 → gap_through_stop` rejection (`trading.py:363–366`): if `|px_fill − stop| < 0.5 × atr_exec(signal bar)`: reject, `reject_reason="stop_too_tight"`. Signal-layer untouched — signals still fire and journal; only the fill is refused.

### G-8d — Unit sanity assert
`one_r <= 0` at any sizing computation → raise `GateViolation`. With G-8a in place this should be unreachable; the assert is the proof it stays unreachable.

### Schema additions (additive — no journal-key changes)
On every ENTRY_FILL/ADD_FILL row: `concurrent_open_at_fill` (int, per the RC definition: same-bar siblings count) and `fill_class` ∈ {`r1`, `v`, `true_add`, `re_entry`} (`true_add` = ADD_FILL with concurrent ≥ 1; `re_entry` = ADD_FILL with concurrent = 0). The `evt` value itself is **unchanged** — keys stay stable, the idempotent writer is undisturbed, old tooling keeps working. **[Additive-vs-rename is veto item V3.]**

### Enrichment correctness (shadows.py)
1. Fix `engagement_flags.ext_before_exit`: window `[tr.fill_i, tr.exit_i]` (this tranche's life), not `[fill_i, camp_end]`. The name becomes truthful.
2. Add `ext_i_offset` (bars from fill to first qualifying extension, null if none) and `mfe_at_ext_r` (running MFE at that bar) to the EXIT row's enrichment. These were R4's two named gaps; they ride the same code and the same regeneration. **[Veto item V4.]**

### Considered and excluded
A dollar-denominated halt floor (G-8e): the R-denominated day/week halts do shrink with equity, but the 25% equity floor bounds that pathology at 4:1; a second halt denominator adds config complexity for a tail the floor already covers. Excluded. **[Reinstate = veto item V5.]**

## 4. Invariants

1. `signals.py` untouched — enforced by fixture F-SIG, not by promise.
2. All engine changes behind config keys with the values above; config committed before the run; new config sha in the ledger pre-registration.
3. Journal schema additive only. Full regeneration into a fresh journal root (`journal_pass2/`); `journal_pass1/` is retained read-only as the historical record.
4. Byte-determinism: the full run executes twice; roll-up hashes identical.
5. No lockbox contact: run window ends 2024-06-30 23:59:59Z exactly, as before.
6. Append-only ledger; pre-registration committed **before** the run (G-7).
7. No pushes, no merges — operator-only, as always.

## 5. Order of work

1. **Pre-run expectation table (Tier-A, old journals):** per cell, the first date equity crosses $2,500 (if ever), from `journal_pass1` equity series. This sharpens P-TC4a from "which cells" to "which cells, by when" before anything runs.
2. **Ledger pre-registration** (§10 template): change set, config sha, hypotheses, predictions P-TC4a–d with priors. Commit.
3. Implement 1.0.8. Unit-test each guard in isolation (a synthetic cell that breaches each one).
4. Run the 20-cell grid twice → `journal_pass2/`. Confirm hash identity.
5. Compute fixtures (§6), score predictions (§7), produce `tc4_baseline.json` + `TC4_BASELINE.md` (rollup in the standard format: 0×/1×/2×, per-mandate, per-asset, CIs, strip-best, taxonomy, plus a `fill_class` census — the first baseline that has one).
6. Ledger completion entry. Commit artifacts. Do not push.

## 6. Fixtures — mechanical invariants of the new baseline

| # | Fixture | Expected |
|---|---|---|
| F-SIG | Signal-event rows (REGIME/PRIME/CONFIRM/V/TPW/X…) byte-identical to `journal_pass1` after normalizing `run_id` and `engine_version` fields only | identical |
| F-G8a | No ENTRY/ADD/REENTRY fill occurs in any cell after that cell's `equity_floor` HALT row | 0 violations |
| F-G8b | `max(|qty|·px_fill / equity_at_fill)` over all fills | ≤ 10.0 |
| F-G8c | `min(stop_dist/atr_exec)` over all fills | ≥ 0.5 |
| F-G8d | Tranches with `one_r ≤ 0` | **0** (vs 717 in pass 1) |
| F-EQ | Minimum equity across all cells and bars | ≥ 0 (vs −2,732.24) |
| F-CLS | Σ over `fill_class` census = total fills; `re_entry` ⟺ `concurrent_open_at_fill = 0` on ADD_FILLs | exact |
| F-EXT | `ext_before_exit` ⇒ `ext_i_offset ≤ (exit_i − fill_i)` on every EXIT row | 0 violations |
| F-DET | Double-run hash identity | identical |

F-SIG is the load-bearing one: it *proves* the strategy brain is unchanged and every delta below the signal layer is the guards.

## 7. Pre-registered predictions — committed before the run

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-TC4a | Halt set = the five intraday cells (halt dates within ±90 days of the pre-run expectation table, later permitted — C1 slows the bleed) | 85% | any intraday cell survives, or any non-listed cell besides ZEC_swing halts |
| P-TC4a′ | ZEC_swing halts | **50%** | — (registered as a genuine coin flip: its pass-1 minimum was $2,402.90, 4% under the floor, and the C1 guard improves its path) |
| P-TC4b | New baseline grid 1× ∈ **[−2,400, −800]** (reasoning: C1-at-0.5 first-order gave −2,035 on clean; floor truncation removes late negative-expectancy intraday history, a further positive delta; path-dependence widens the band) | 65% | outside the band |
| P-TC4c | New baseline campaigns ∈ [1,900, 2,700] (truncation vs C1-extended survival pull opposite ways) | 60% | outside |
| P-TC4d | Grid win rate ≥ 11% (pass-1 clean: 9.8% — removing decile-1 fills and post-collapse churn should lift it) | 65% | < 11% |

Falsifications are findings: P-TC4b outside its band means the path-dependence of C1 is much larger than first-order — itself worth knowing before S-1 trusts any first-order number again.

## 8. Verdict criteria

**PASS** — 9/9 fixtures; predictions scored; determinism proven; pre-registration demonstrably precedes the run in the commit history.
**HALT** — any fixture violation (a guard that doesn't hold), F-SIG mismatch (the brain moved), or `GateViolation` raised during the run (report the offending state, do not patch-and-continue).
**PARTIAL** — not applicable this phase: a guard either holds everywhere or the phase fails.

## 9. Output artifacts

`engine/` diffs (1.0.8) · `configs/v12_anchor_g8.yaml` (new sha) · `journal_pass2/` (not committed; sha manifest committed) · `scripts/tc4_fixtures.py` · `TC4_BASELINE.md` · `tc4_baseline.json` · two `LEDGER.md` entries (pre-registration + completion) · this contract file.

## 10. Ledger templates

**Pre-registration (before the run):**
```
[YYYY-MM-DD] TC-4 PRE-REGISTRATION — engine 1.0.8, Tier C (G-7)
Change set: G-8a floor 0.25 · G-8b notional reject 10x · G-8c min-stop 0.5 ATR ·
G-8d one_r>0 assert · schema {concurrent_open_at_fill, fill_class} · shadows.py
ext-window fix + {ext_i_offset, mfe_at_ext_r}
Config: v12_anchor_g8 sha [..]  Engine: 1.0.8 @ [commit]
Hypothesis: guards remove simulation-artifact loss and tight-bps donation without
touching the signal brain (F-SIG proves the latter)
Predictions: P-TC4a [85%] P-TC4a' [50%] P-TC4b [-2400,-800; 65%] P-TC4c [60%] P-TC4d [65%]
Pre-run expectation table: [floor-crossing dates per cell, from journal_pass1]
ALSO REGISTERED (not run): TC-5 candidate — intraday re-spec 1H/5m. Hypothesis:
median mfe_bps/cost_bps at 5m exec ≥ 2x the 1H/1m ratio. Runs after S-1. (Operator
ratification 2026-07-17.)
```

**Completion:** fixtures, prediction scores, hashes, new-baseline headline at 0×/1×/2× with CI and strip-best, `fill_class` census, halt table (cell → date), artifacts list, "supersedes journal_pass1 as baseline; pass 1 retained read-only."

---

## 11. The go-paste

```
CONTRACT: TC-4 — Engine 1.0.8 Guards + Re-Anchor (Tier C — G-7 binds)

Read TC4_Engine_1_0_8_Builder_Contract.md in the repo in full before anything else.
The contract is the authority; this paste is the trigger.

Scope in one line: four guards (equity floor 25%, notional reject 10x, min-stop 0.5 ATR,
one_r>0 assert), two additive journal fields (concurrent_open_at_fill, fill_class), the
ext_before_exit window fix + two enrichment fields — then the 20-cell re-run that becomes
the new baseline. signals.py is UNTOUCHED and fixture F-SIG proves it.

Order of work — G-7 makes this ordering mandatory, do not reorder:

1. PRE-RUN EXPECTATION TABLE (Tier A, journal_pass1): per cell, first date equity
   crosses $2,500, if ever. Print it.

2. LEDGER PRE-REGISTRATION (contract §10, first template) including the TC-5 1H/5m
   registration. COMMIT IT. The run must not start before this commit exists.

3. IMPLEMENT 1.0.8 per contract §3. Each guard behind its config key with the ratified
   value. Unit-test each guard with a synthetic breach case. Schema fields are ADDITIVE;
   journal keys and evt values unchanged.

4. RUN the 20-cell grid TWICE into journal_pass2/. journal_pass1/ is read-only history —
   do not touch it. Confirm double-run hash identity.

5. FIXTURES (contract §6, all nine). F-SIG compares signal-event rows to journal_pass1
   after normalizing run_id and engine_version ONLY.

   *** ANY FIXTURE VIOLATION OR ANY GateViolation DURING THE RUN: HALT AND REPORT.
       Do not patch and continue. A guard that does not provably hold does not exist. ***

6. SCORE P-TC4a/a'/b/c/d. Falsifications reported as prominently as confirmations.

7. ARTIFACTS per contract §9: TC4_BASELINE.md (standard rollup format + fill_class
   census + halt table), tc4_baseline.json, tc4_fixtures.py, completion ledger entry,
   sha manifest of journal_pass2. Commit. Do not push, do not merge.

Do NOT, even if it seems helpful:
 - modify signals.py, or any strategy parameter, zone geometry, or V threshold
 - implement the re-entry quality bar, the cost-aware bps floor, the 1H/5m re-spec
   (register only), any maker/chase model, or any S-1 shadow family
 - resize entries to fit the notional cap (reject them)
 - touch the lockbox, journal_pass1, or merge anything

Report back: pre-run expectation table, both ledger entries, fixture table, prediction
scorecard, tc4_baseline.json, the new headline with CI and strip-best. The reviewer
verifies before this becomes the baseline.
```

---

## Appendix — Veto table (defaults stand on silence)

| # | A-priori choice | Default |
|---|---|---|
| V1 | Floor breach handling | Flatten all open at next bar open, permanent cell halt |
| V2 | Notional cap semantics + level | **Reject** (not resize) at **10×** equity |
| V3 | Nomenclature mechanism | **Additive** `fill_class` field; `evt` values unchanged (keys stable) |
| V4 | Fold `ext_i_offset` / `mfe_at_ext_r` into 1.0.8 | **Yes** (rides the same regeneration) |
| V5 | G-8e dollar halt floor | **Excluded** (25% equity floor bounds the pathology) |
| V6 | ZEC_intraday cell membership | **Stays in the grid** (halts early under G-8a; no exclusions needed in the new baseline) |

*Contract prepared by the reviewer under Fable-mode, 2026-07-17. Guard values are operator-ratified; every mechanism cited (`trading.py:363–366`, the equity-update sites, `shadows.py:190–194`, the RC concurrency definitions) was source-verified this session or the last. The baseline this run supersedes remains on disk, read-only, forever — falsifiable history, not erased history.*
