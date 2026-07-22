/# RC Recompute RC-0–RC-6 — Builder Contract

**Phase:** v12 Study · post-R1–R10 forensics · **Tier A (journal arithmetic + filesystem inventory only)**
**Basis:** V3 anchor run — engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5…`), scored partition (exploration-classic), 20 cells, 8,387 resolved tranches, 3,456 campaigns.
**Charter authority:** VR-1 — exploration-classic is free to mine. First look consumed. **No new evidence is spent by this phase.** G-7 does not bind (nothing is tuned, nothing re-runs).
**Operator ratification:** 2026-07-16 — TC-4 jumps the queue after this phase; risk-mode interview follows RC-1/RC-3 delivery; add/re-entry nomenclature ratified ("an add only counts as such if it increases size in an open position, not if it opens one").

---

## 0. Operator instructions — same drill as last time

1. PowerShell → repo folder → `claude` (or the full-path launch if needed).
2. `git status` → *expect* `On branch v12-v1-census`, clean. If not, stop and report.
3. Paste the go-paste (§11) into Claude Code. Enter.
4. *What you should see:* a fixture table where **all ten fixtures say MATCH**. Any MISMATCH → the builder halts, produces nothing downstream, reports the mismatch. That rule is absolute.
5. Send back: the fixture table, the prediction scorecard, `rc_recompute.json`. Reviewer verifies independently before anything is believed.

Runtime expectation: minutes (1.3 GB of journals), not seconds.

---

## 1. What this phase is

Seven free measurements (RC-0…RC-6) from the existing anchor journals plus one filesystem inventory. They gate three things: the risk-mode interview (RC-1, RC-3), the S-1 parameter grids (RC-3, RC-4, RC-6), and the TC-4 predictions (RC-2). Nothing runs, nothing changes, nothing is fetched.

## 2. What this phase is NOT

- **Not a re-run.** No engine execution, no config edits, no network. RC-0 touches the filesystem read-only.
- **Not evidence about the future.** In-sample, on mined data. Ranks and sizes; validates nothing.
- **Not TC-4.** The guards, the schema fix, and the re-anchor are the next phase, separately contracted and pre-registered.
- **Not S-1.** Anything needing EMA values, counterfactual stop paths, or new shadow columns is out of scope here — those aren't in the journals.
- **Not a variant nomination.** Five slots, operator's call, later.

## 3. Invariants

1. **Read-only everywhere.** No writes outside `scripts/`, the two output artifacts, and the ledger append. No `replay.py`, no network, no config or engine edits.
2. **Primary basis = scored-clean.** Every deliverable reports **scored-clean (19 cells: scored minus ZECUSDT_intraday)** as the primary column and **scored-20** as a reference column. Reason: 717 of ZEC_intraday's 1,414 tranches carry inverted units (G-8); their R-denominated quantities are corrupted. Annex/spent/LIT remain excluded as before.
3. **Recompute from raw bytes.** Journals only. Prior reports (`ROLLUPS_AND_HYPOTHESES.md`, `V3_RECOMPUTE_R1_R10.md`, forensics docs) are cross-checks, never inputs.
4. **No cost-free number stands alone** — 0×/1×/2× on every R aggregate, per the §4 formulas.
5. **Strip-best on every campaign-level aggregate.**
6. **95% bootstrap CI on every expectancy** — 10,000 resamples, campaign-level, seed `20260716`, stated in output.
7. **Falsification is a deliverable** — all eight predictions in §7 scored, failures reported as prominently as passes.
8. **Determinism** — run twice, state both output hashes, assert identical.

## 4. Unit conventions and definitions — pin before coding

Carried unchanged from the R1–R10 contract (all confirmed by that phase): `realized_r` is size-weighted cell-R; Σ over scored EXIT rows = grid net; R/unit = `realized_r ÷ size_r`; `one_r` from the ENTRY row, **signed** (`|px_fill − stop| × qty ÷ size_r` — the signed form is what reproduced F3/F4 last phase); `cost = fees + funding_cum + slippage` from the EXIT row; `r_0x = realized_r + cost/one_r`; `r_2x = realized_r − cost/one_r`; stop-distance ATR denominator = `atr_exec` from the **ENTRY** row; joins on `tranche_id` within `cell_id`.

**New definitions this phase — these are the contract's load-bearing lines:**

- **Open interval of a tranche:** `[fill_ts, exit_ts)` — fill inclusive, exit exclusive.
- **`concurrent_open_at_fill(A)`** = count of sibling tranches B in the same `campaign_id` with `B.fill_ts ≤ A.fill_ts < B.exit_ts`, B ≠ A. **Same-bar siblings count as concurrent** (they were queued in the same wake and coexist).
- **True add** = an `ADD_FILL` row with `concurrent_open_at_fill ≥ 1`. **Re-entry** = an `ADD_FILL` row with `concurrent_open_at_fill = 0`. (Operator-ratified definition. R1 and V fills are neither.)
- **`max_concurrent(campaign)`** = max over the campaign's life of simultaneously open tranches (sweep fill/exit events in time order; same-bar fills before same-bar exits at equal timestamps — state this tie-break in the script header).
- **Direction-run** = maximal sequence of same-cell, same-direction campaigns uninterrupted by an opposite-direction campaign, in journal time order. **Attempt number** = 1-based index of a campaign-opening fill (R1 or re-entry) within its direction-run.
- **Cluster membership (RC-6):** an attempt is *in-cluster* if `|fill_px − first_attempt_fill_px| ≤ k × ATR_exec(first attempt's ENTRY row)`, k ∈ {0.5, 1.0, 1.5}.
- **Basis-point conversions (RC-3):** `mfe_bps = mfe_r × (stop_dist_px / px_fill) × 10⁴` where `stop_dist_px = |px_fill − stop|` from the ENTRY row; `cost_bps = cost_usd / (|qty| × px_fill) × 10⁴` (round-trip, from the EXIT row's cumulative fields); `realized_bps` analogous from `realized_r`. All per tranche.

## 5. Fixtures — known-answer gates. Any MISMATCH halts the phase.

| # | Fixture | Expected |
|---|---|---|
| F1 | Scored campaigns / resolved tranches | 3,456 / 8,387 |
| F2 | Σ realized_r, scored-20, 1× | −5,756.9093 (±0.0001) |
| F3 | Σ r_0x, scored-20 | +1,345.3095 (±0.0001) |
| F4 | ZECUSDT_intraday: tranches / negative-`one_r` tranches | 1,414 / 717 |
| F5 | ZECUSDT_intraday net 1× (cell-R) | −663.1247 (±0.001) |
| F6 | **Scored-clean grid 1×** (= F2 − F5) | **−5,093.7846 (±0.001)** |
| F7 | Stop-exit events (per `(cell_id, dir, ts_open)` collapse) | 7,057 |
| F8 | `tranche_cap` REJECT rows | 145,749 |
| F9 | V-initiated campaigns | 45 |
| F10 | Per-tranche resumption count (≥1R within 20 bars, stop exits) | 2,899 |

F1–F3, F7–F10 reproduce the verified record with a fresh reader; F4–F6 pin the scored-clean basis this phase introduces.

## 6. Deliverables

Every table: **scored-clean primary, scored-20 reference**, per-mandate splits, 0×/1×/2× on R aggregates.

### RC-0 — Data-estate inventory (filesystem only, no network)
For each of the 7 scored assets (plus HYPE, FARTCOIN, LIT for completeness): which kline caches exist per TF ∈ {1m, 5m, 15m, 30m, 1h, 4h, 12h, 1d}, row counts, first/last timestamps, gaps > 2× the TF interval. Flag which of {15m, 30m, 1d} are absent per asset, and state whether each absent TF is locally resamplable (30m from 15m or 1m; 1d from 1h or 1m) — resampling itself is **out of scope** (S-1 data prep), only the feasibility statement is in scope.
**Purpose:** B6 — sizes the S1-3 capture-set expansion before S-1 is contracted.

### RC-1 — Concurrency census + add/re-entry reclassification
(a) Classify every `ADD_FILL` as true-add or re-entry per §4; report counts, share, and per-unit gross/net for {R1, true add, re-entry, V} separately — this **decomposes report 1's "adds carry the edge (+0.47/unit)"** into its two populations for the first time.
(b) Campaign table by `max_concurrent` ∈ {1, 2, 3}: count, expectancy + CI, win rate, Σ cell-R, strip-best.
(c) The **real-pyramid population**: campaigns where ≥1 true add ever filled — count, expectancy, share of Σwins.
(d) Top-10 campaigns by cell-R: for each, tranche count, `max_concurrent`, and serial-vs-concurrent structure. Report 1 read "all top-10 are full 3-tranche ladders" as pyramids; this tests whether they were **stacked positions or serial re-entries**.
(e) Fill-spacing: distribution of bars between consecutive fills within a campaign, split by true-add vs re-entry.
**Caveat header:** classification is observational; selection effects (adds require ratchet-to-BE requires trend) mean cohort differences are NOT causal effects of adding.

### RC-2 — Equity trajectories + clean-basis certification
Per cell: initial equity, minimum equity (value + timestamp), final equity, zero-crossings, and near-misses (min < 20% of initial). Certify scored-clean: assert **no cell other than ZECUSDT_intraday crossed zero**; if any did, flag loudly — the scored-clean basis itself is then wrong and the phase halts after RC-2 reporting.
**Purpose:** G-8 blast radius; the TC-4 contract's predictions will be written against this table.

### RC-3 — Edge in basis points
Per-tranche distributions (deciles + mean) of `mfe_bps`, `cost_bps`, `realized_bps`, and the ratio `mfe_bps / cost_bps`, split by mandate and by grade. Report the fraction of tranches with `mfe_bps > cost_bps` (the trade *could* have paid its costs at its peak) per mandate.
**Purpose:** the project's most fundamental number — whether favourable price movement exceeds round-trip cost **in price terms**, before R-space amplification. Feeds the ratchet/harvest grids and the modes interview.

### RC-4 — Stop-distance decile table + floor curve
(a) Deciles of `stop_dist/ATR`: n, gross/unit, cost/unit, net/unit, Σ cell-R, win rate per decile.
(b) **Floor curve:** for X ∈ {0.30, 0.40, 0.50, 0.60, 0.75, 1.00, 1.25, 1.50}: the first-order book with all tranches of `stop_dist/ATR < X` removed — Σ cell-R at 0×/1×/2×, campaigns, expectancy.
**Purpose:** replaces the single C1 point (0.5) with the whole curve; directly pins the Y×ATR floor and the S1-8 sweep grid. First-order caveat as standard (removals change equity path, rail, halts — not the stop path).

### RC-5 — Z1 filter / tilt, first-order
Campaign zone = the initiating tranche's `zone`. (a) Drop Z1-initiated campaigns; (b) half-size Z1-initiated campaigns (`size_r × 0.5` re-weight). Each: Σ cell-R 0×/1×/2×, campaigns, expectancy + CI, win rate, strip-best.
**Purpose:** sizes the largest clean entry-side lever (Z1 = 70% of campaigns, 77% of the loss).

### RC-6 — Attempt-sequence census
Per §4's direction-run and attempt definitions: (a) distribution of attempts per direction-run; (b) expectancy + Σ cell-R by attempt number (1, 2, 3, 4+); (c) in-cluster share of attempts 2+ at k ∈ {0.5, 1.0, 1.5}; (d) expectancy by attempt number × in/out-of-cluster; (e) the counterfactual bound: Σ cell-R of in-cluster attempts 4+ (what a 3-strike cluster rule would have removed, first-order).
**Purpose:** sizes the operator's 3-strike rule with its actual mechanical definition before TC-2 designs it.

## 7. Pre-registered predictions — score all eight

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| P-RC1a | Re-entries are ≥70% of ADD_FILL rows | 75% | <70% |
| P-RC1b | True-add per-unit gross ≥ re-entry per-unit gross | 55% | otherwise |
| P-RC1c | Majority of top-10 campaigns are serial (max_concurrent < 3), not stacked pyramids | 60% | ≥5 of 10 have max_concurrent = 3 |
| P-RC2 | No cell besides ZEC_intraday crossed zero | 80% | any other zero-crossing |
| P-RC3 | Median `mfe_bps > cost_bps` on swing; median `mfe_bps < cost_bps` on intraday | 70% | either half fails |
| P-RC4 | Net/unit by stop-distance decile is non-monotone with its maximum in the 0.75–1.50 ATR band | 60% | max outside band or monotone |
| P-RC5 | Z1-drop improves scored-clean 1× by ≥ +1,500 cell-R first-order | 65% | < +1,500 |
| P-RC6 | Expectancy decays monotonically in attempt number (1 > 2 > 3) | 55% | any inversion |

## 8. Verdict criteria

**PASS** — 10/10 fixtures MATCH; RC-0…RC-6 delivered with caveat headers; 8/8 predictions scored; determinism hashes identical; scored-clean certification stated.
**HALT** — any fixture MISMATCH (report computed vs expected, produce nothing downstream), or RC-2 finds a second zero-crossing cell (report RC-0…RC-2, halt the rest — the basis is wrong).
**PARTIAL** — a deliverable needs a field the journals don't carry: name the field, name the row type it would live on, mark PARTIAL, move on. **No estimates substituted.**

## 9. Output artifacts

`scripts/rc_recompute.py` (committed) · `RC_RECOMPUTE_RC0_RC6.md` (tables + caveats) · `rc_recompute.json` (machine-readable, for reviewer verification) · `LEDGER.md` entry (builder-typed, appended).

## 10. Ledger entry template

```
[YYYY-MM-DD] RC RECOMPUTE RC-0–RC-6 — Tier A, journals + filesystem inventory
Basis: engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5…), scored partition;
primary basis scored-clean (19 cells, ZECUSDT_intraday excluded per G-8)
Evidence spend: NONE (VR-1). Engine delta: NONE.
Fixtures: F1–F10 [MATCH/MISMATCH — list any]
Predictions: P-RC1a [..] P-RC1b [..] P-RC1c [..] P-RC2 [..] P-RC3 [..] P-RC4 [..] P-RC5 [..] P-RC6 [..]
Scored-clean certification: [no other cell crossed zero / VIOLATION: <cell>]
Determinism: hashes [..]/[..] identical [Y/N]
Artifacts: scripts/rc_recompute.py, RC_RECOMPUTE_RC0_RC6.md, rc_recompute.json
Next: TC-4 contract (guards + schema/nomenclature fix + re-anchor), then modes interview, then S-1
```

---

## 11. The go-paste

```
CONTRACT: RC Recompute RC-0–RC-6 (Tier A — journal arithmetic + read-only filesystem inventory)

Read RC_Recompute_RC0_RC6_Builder_Contract.md in the repo in full before writing any
code. The contract is the authority; this paste is only the trigger.

Scope in one line: seven free measurements from the existing V3 anchor journals plus a
kline-cache inventory. Read-only. No engine changes, no config changes, no replay, no
network.

Order of work — do not reorder:

1. DEFINITIONS (contract §4). State back in your own words: the open-interval definition,
   concurrent_open_at_fill including the same-bar rule, true-add vs re-entry, direction-run
   and attempt number, and the bps conversion formulas. Do not proceed until written out.

2. FIXTURES (contract §5, F1–F10). Compute all ten from raw journal bytes. Do NOT read any
   prior report or rollup as input. Print fixture / expected / computed / MATCH-MISMATCH.

   *** ANY MISMATCH: STOP. Report it. Produce nothing downstream. ***

3. BASIS. Primary = scored-clean (19 cells, ZECUSDT_intraday excluded). Reference =
   scored-20. Every table carries both. RC-2 certifies the basis: if ANY other cell
   crossed zero equity, report RC-0..RC-2 and HALT the remainder.

4. DELIVERABLES RC-0..RC-6 (contract §6), each with its caveat header printed. PARTIAL
   protocol: name the missing field and row type, no estimates.

5. PREDICTIONS (contract §7). Score all eight; falsifications reported as prominently as
   confirmations.

6. DETERMINISM. Run twice, print both hashes, assert identical.

7. ARTIFACTS. Commit scripts/rc_recompute.py, RC_RECOMPUTE_RC0_RC6.md, rc_recompute.json;
   append the §10 ledger entry. Builder-typed, append-only. Do not push, do not merge.

Do NOT, even if it seems helpful:
 - execute replay.py or modify engine/, configs/, or any journal file
 - fetch anything over the network (RC-0 is a local listing only)
 - resample or create new kline files (feasibility statement only)
 - touch lockbox/annex rows in scored aggregates, or re-admit ZECUSDT_intraday to primary
 - substitute estimates for missing fields

Report back: the definitions restatement, the fixture table, RC-0..RC-6, the prediction
scorecard, both determinism hashes. The reviewer recomputes independently from
rc_recompute.json before anything is believed.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-16. Definitions in §4 implement the operator's ratified add/re-entry nomenclature. Fixtures F1–F3, F7–F10 restate the twice-verified record; F4–F6 pin the scored-clean basis introduced this phase. Sequencing per operator ruling: this phase now → TC-4 (guards + schema + re-anchor) → risk-mode interview (on RC-1/RC-3) → S-1 on clean journals.*
