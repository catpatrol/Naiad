# TC-1 — Stop × Exit Architecture Factorial — Builder Contract

**Phase:** v12 Study · **Tier C** (trading changes — pre-registered under G-7 before any run). **Engine: 1.0.11.**
**Operator rulings in force (2026-07-20):** D-2 re-ruled — TC-1 is the **2×2 factorial {stop anchor: bar-extreme vs structural-1h-static} × {exit: none vs gov-e200 trail b0.5}**, four cells, the joint included. The bps floor is **out** (owned 85.4% by the anchor; residual → TC-2). The 30m anchor is **out** (strip-best sign-flip). The **ratcheting-structural variant is a named follow-up, not a fifth cell.** TC-5 runs in parallel under its own contract.
**Prediction basis:** the S-2b decomposition table (`s2b_results.json` D1) — the 38% gross component and the per-mandate books, never the +2,360 headline. **These are real runs: path effects the first-order tables could not see (re-entry suppression, concurrency, funding, rail/halt feedback) are the point, not noise.**

---

## 0. Operator instructions

Save this contract into the repo → `claude` → `git status` clean → paste §10. *What you should see, in order:* (a) definitions restatement; (b) the **G-7 pre-registration commit** — config shas for cells B/C/D plus all eight prediction rows, committed **before** any implementation; (c) engine 1.0.11 implemented — trading-layer only — with unit tests; (d) cell-A byte-identity proof (minutes); (e) **three full-grid runs × 2 for determinism — the largest compute of the project so far; many hours; leave it running**; (f) fixtures, all MATCH; (g) the eight-row scorecard and the cell tables. Any fixture MISMATCH: halt, report, nothing downstream. Send back `tc1_results.json`, `TC1_RESULTS.md`, fixture table, scorecard.

## 1. The four cells

| Cell | Stop anchor | Exit overlay | Status |
|---|---|---|---|
| **A** | bar-extreme + event-ratchet (baseline) | none | **exists** — `journal_pass2`; re-run once under 1.0.11 with architecture keys absent, must be **byte-identical** (proves config-gating inert) |
| **B** | **structural-1h-static** | none | new run — the F4-1h form as measured |
| **C** | bar-extreme + event-ratchet | **gov-e200 trail, fold-in** | new run — the S-1/S-2 corrected form |
| **D** | **structural-1h-static** | **gov-e200 trail** | new run — **the joint; the 4,019-tranche interaction region's answer** |

## 2. Architecture definitions — pin before coding

- **Structural stop (B, D):** at fill, stop = nearest confirmed (5,5) pivot low (long) / high (short) on the **1h** frame, strictly beyond entry, confirmed by the fill bar, within a 200-bar 1h lookback, offset ∓ 0.5·ATR_exec(signal bar). **Static for the tranche's life** — no event-ratchet advances apply to it. If no confirmed pivot exists in lookback: the tranche is **not taken** (a birth-time architecture constraint, not a void — count and journal these as `no_struct_anchor` rejects; S-2b measured 0 voids at 1h so expect ≈0, but the rule must exist).
- **G-8c min-stop interaction:** the structural distance is by construction ≥ the 1h pivot distance; the 0.5·ATR_exec floor still applies as a lower bound (should never bind at 1h — assert, don't assume).
- **Trail (C, D):** engagement = first exec close beyond the governor e200 in the trade's favor after fill. Post-engagement stop = **one-way max** (long) of the trail line `gov_e200 ∓ 0.5·ATR_exec`, seeded at the standing stop at engagement — in C the standing stop is the native ratchet's value (fold-in frozen: native advances ignored after engagement); in **D the seed is the structural stop, and the post-engagement stop = max(trail, structural floor)** — the trail can only tighten from the structural floor upward, never below it. Never loosens. Exit on touch, engine wake order.
- **Everything else identical in all cells:** signal layer byte-untouched (architecture lives in the **trading layer**), G-8 guards, sizing, BE add-gate (tests the cell's own live stop), max_tranches, cooldowns, fee/slip model, window, seeds.
- **Expected path effects (write into the report, not away):** in B/D, long holds suppress while-flat re-entries (position occupies) — tranche counts should fall materially; the BE add-gate almost never passes under a static below-entry stop, so B is near-pyramid-free by construction; window-end open tranches will grow (1.0.8-frozen emission rule — report `fills_without_exit_row` per cell).

## 3. Engine 1.0.11 — change set

Trading-layer config keys: `stop_mode ∈ {native, struct_1h}` and `exit_trail ∈ {none, gov_e200_b0.5}`; **absent keys = baseline behavior exactly** (cell A's byte-identity is the proof). 1h pivot series computed from the already-loaded 1h frames. `signals.py` byte-untouched (git diff empty). J-1 carried a **fourth** time, disclosed (cell-A byte-identity requires it out).

## 4. Configs and runs

Four configs, sha-pinned at pre-registration: `tc1_A` (keys absent), `tc1_B`, `tc1_C`, `tc1_D`. Full 20-cell grid, exploration-classic window, $10k/cell, G-8 guards. Runs: A once (byte-identity), B/C/D each **twice** (determinism). Fresh roots `research_outputs/tc1/<cell>/`.

## 5. Fixtures — any MISMATCH halts

| # | Fixture | Expected |
|---|---|---|
| F-A-BYTE | Cell-A rerun vs `journal_pass2`, stamps normalized | byte-identical, all 20 cells |
| F-SIG-ALL | Signal rows identical across A/B/C/D after stamp normalization | identical |
| F-ARCH-B | Every B/D tranche's initial stop == its 1h structural level; **B: stop at exit == stop at entry** (static, every tranche) | 0 violations |
| F-TRAIL | C/D: post-engagement stop never loosens; engagement rule as §2; **D: stop ≥ structural floor always** | 0 violations |
| F-GUARDS | G-8 a–d hold in every cell | 0 violations |
| F-CFG | Config shas match the pre-registration commit | exact |
| F-DET | B/C/D double-run identity | identical |

## 6. Pre-registered predictions (mandate-stratified where stated; scored at 1× vs cell A unless noted)

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-A | Cell-A byte-identity holds | 90% | any diff |
| P-B-1 | B grid 1× ∈ [+100, +900] (struct-R) | 55% | outside |
| P-B-2 | B swing 1× > 0 | 65% | ≤ 0 |
| P-B-3 | B intraday 1× < 0 | 70% | ≥ 0 |
| P-C-1 | C grid 1× ∈ [−1,900, −1,300] | 55% | outside |
| P-C-2 | C position 1× ≥ +250 | 60% | below |
| **P-D** | **D grid 1× ≥ B grid 1× — the interaction** | **50%** | below |
| P-CNT | B and D tranche counts ≤ 70% of A's 6,304 (re-entry suppression) | 60% | either above |

## 7. Deliverables

Per cell: headline table (grid + per-mandate, 0×/1×/2×, strip-best, win rate, campaigns/tranches, cost stack, `fills_without_exit_row`), exit-reason census, holding-time medians, adds funnel (BE-gate passes per cell — expect ≈0 in B), halt calendar, equity paths. Cross-cell: the factorial main-effects and interaction table (stop effect, trail effect, D − B − C + A), mandate-stratified; funding-accrual note wherever holds exceed the proxy's assumptions. Every table: in-sample caveat, denominator stated (struct-R for B/D).

## 8. Verdict criteria

**PASS** — 7/7 fixtures, 8/8 predictions scored falsifications-first, all deliverables with caveats, determinism proven. **HALT** — any fixture MISMATCH; F-A-BYTE failure especially (the gating itself is broken — nothing else is trustworthy). **PARTIAL** — a deliverable blocked by a missing field: name it, no estimates.

## 9. Ledger (two entries: G-7 pre-registration before implementation; completion after)

Pre-registration: the four configs' shas, the eight rows verbatim, the §2 definitions hash. Completion: fixtures, scorecard, per-cell headlines, the interaction number, "prediction basis: s2b D1 — registered against the 38%, not the headline." Commit; **do not push, do not merge.**

## 10. The go-paste

```
CONTRACT: TC-1 — Stop × Exit Architecture Factorial (Tier C; engine 1.0.11)

Read TC1_Factorial_Builder_Contract.md in the repo in full first. The contract is the
authority; this paste is the trigger.

Scope in one line: four cells — A baseline (byte-identity rerun), B structural-1h
static stop, C gov-e200 fold-in trail, D the joint (trail seeded at the structural
floor) — full grid, real runs, path effects included; predictions registered against
the S-2b decomposition.

Order of work — mandatory:

1. DEFINITIONS (contract §2). Restate in your own words: the structural-stop birth rule
   incl. no_struct_anchor; static-for-life in B; engagement and the one-way trail; D's
   max(trail, structural floor); why the BE add-gate should almost never pass in B; why
   tranche counts should fall in B/D.

2. G-7 PRE-REGISTRATION — commit the four config shas + all eight prediction rows +
   the §2 definitions BEFORE implementing anything.

3. IMPLEMENT engine 1.0.11 per §3 — trading layer only; signals.py git diff EMPTY;
   unit tests for the structural anchor, the trail one-way property, and D's floor.
   J-1 stays out (fourth carry, disclosed).

4. CELL A first: rerun with keys absent; F-A-BYTE must pass before B/C/D get compute.

5. RUN B, C, D — each twice into research_outputs/tc1/. Largest compute yet; hours;
   do not trim the grid, do not skip the second runs.

6. FIXTURES (§5), then DELIVERABLES (§7), then PREDICTIONS (§6) falsifications first.

   *** F-A-BYTE OR F-SIG-ALL FAILURE: HALT — the config gating itself is broken. ***

7. ARTIFACTS + completion ledger per §9. Commit. Do not push, do not merge.

Do NOT, even if it seems helpful: touch signals.py · apply the bps floor · price or run
the ratcheting variant or the 30m anchor · alter guards, sizing, gates, or windows ·
touch the lockbox · reuse S-1/S-2 shadow numbers as if they were these runs.

Report back: definitions restatement, pre-registration confirmation, F-A-BYTE result,
fixture table, per-cell headlines, the factorial interaction table, the eight-row
scorecard, both hashes per run, tc1_results.json.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-20. Four cells, two levers, one interaction the journals could not price — and a byte-identity gate standing in front of the compute so the factorial's authority is never in doubt. The ratcheting variant waits, named; the floor moved to TC-2; the predictions are registered against the decomposition, because the day this project starts registering against headlines is the day it stops being worth running.*
