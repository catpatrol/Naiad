# V3 Recompute R1–R10 — Builder Contract

**Phase:** v12 Study · post-V3-anchor forensics · Tier A (journal arithmetic only)
**Basis:** V3 anchor run — engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5…`), 20 scored cells, 8,387 resolved tranches, 3,456 campaigns, exploration-classic (open time ≤ 2024-06-30 23:59:59Z).
**Charter authority:** VR-1 — exploration-classic is free to mine, plot, iterate. First look already consumed. No new evidence is spent by this phase.
**Operator ratification:** 2026-07-15. D1, D2, D4–D9 defaults accepted on silence. D3 (VS-Z3) **held** pending R6/R7.

---

## 0. Operator instructions — run this yourself, step by step

**What you're about to do:** hand Claude Code a contract to compute ten tables from the journal files already sitting on your machine. Nothing is re-run, no code changes, no downloads. It is arithmetic over files that already exist.

**Step 1 — open PowerShell** and go to the repo folder (the `naiad/` directory inside your "Midas-Claude Code Resources" folder).

**Step 2 — launch the builder.** Type:
```
claude
```
If PowerShell says it can't find the command, use the full path instead:
```
& "$env:USERPROFILE\.local\bin\claude.exe"
```
*What you should see:* the Claude Code prompt opens and shows the current folder.

**Step 3 — confirm you're on the right branch.** Type:
```
git status
```
*What you should see:* `On branch v12-v1-census`. If it says anything else, stop and tell me.

**Step 4 — paste the contract.** Copy everything in the grey block in §11 below (from `CONTRACT:` to the final line) and paste it into Claude Code. Press Enter.

**Step 5 — what happens next.** The builder will write one script, run it against the journals, and produce two files plus a ledger entry. This is read-only: it cannot change the engine, cannot fetch data, cannot touch the lockbox.

*What you should see:* a fixture table where all nine fixtures say `MATCH`. **If any fixture says `MISMATCH`, the builder must stop and report — do not let it proceed.** A mismatch means the script is reading the journals wrong, and every number after it would be garbage.

**Step 6 — send me the output.** Paste back the fixture table, the prediction scorecard, and `recompute.json`. I'll verify independently before either of us believes any of it.

**Roughly how long:** the journals are ~1.3 GB. Expect several minutes of compute, not seconds.

---

## 1. What this phase is

Ten measurements, each answering a question that is currently blocking a V4 design decision. All ten are computable from journal rows that already exist. No engine change, no re-run, no new data.

## 2. What this phase is NOT

- **Not a tuning exercise.** No config values change. No engine code changes. No replay is executed.
- **Not evidence about the future.** Every number here is in-sample on data already mined. It ranks candidates; it validates nothing.
- **Not a variant nomination.** Bounds inform the operator's five-slot decision. They do not make it.
- **Not a lockbox touch.** No row outside the scored partition enters any scored aggregate.
- **Not S-1.** S-1 (instrumented replay, new shadow columns, trading unchanged) is a separate Tier-B contract.
- **Does not answer aggressive mode.** Aggressive creates tranches that do not exist in these journals; it requires a Tier-C run. R9 covers defensive and neutral only.
- **Does not implement VS-Z3.** The z3Prox change is held pending R6/R7.

## 3. Invariants

1. **Read-only.** No writes to `engine/`, no config edits, no `replay.py` execution, no network calls.
2. **Scored partition only.** Every aggregate is exploration-classic, 20 scored cells. The annex (spent-BTC and contaminated partitions) is excluded from all scored aggregates. LIT remains excluded (G-2).
3. **Recompute from raw bytes.** Read the journal JSONL files. Do not read `ROLLUPS_AND_HYPOTHESES.md`, `V3_STOP_AND_EXIT_FORENSICS.md`, or any prior summary as an input. Report 1's numbers are cross-checks, not sources.
4. **No cost-free number stands alone.** Every R aggregate is reported at 0× / 1× / 2× using the manifest formula (§4).
5. **Strip-best by default.** Every campaign-level aggregate prints its strip-best-campaign line.
6. **Intervals on every expectancy.** 95% bootstrap CI, 10,000 resamples, campaign-level, seed pinned and stated.
7. **Falsification is a deliverable.** Every prediction in §7 is scored explicitly, including the ones that fail.
8. **Determinism.** The script must produce byte-identical output on a second run. State the hash.

## 4. Unit conventions — pin these before writing a line of code

Getting this wrong silently corrupts every table. From `trading.py:21–25` and the run manifest:

- `realized_r` on an EXIT row = net PnL ÷ 1R-dollars-at-entry. **It is already size-weighted.** A 0.5R tranche dying exactly at its stop yields `realized_r = −0.5`.
- **cell-R** = `realized_r` as journaled. **Σ(realized_r) over scored EXIT rows = the grid net.** This is fixture F2.
- **R/unit** (per-unit-risk basis) = `realized_r ÷ size_r`.
- `one_r` (dollar value of 1R) = from the **ENTRY** row: `|px_fill − stop| × qty ÷ size_r`.
- `cost` = `fees + funding_cum + slippage`, taken from the **EXIT** row (these are cumulative totals, not exit-leg only).
- Stress rows: `r_0x = realized_r + cost/one_r` · `r_2x = realized_r − cost/one_r`.
- **Shadow exit variants (`exit_XA`…`exit_XD`) are journaled as per-unit R.** To compare against the book: `cell-R = exit_X × size_r`. They carry no costs, so they are a **gross (0×) basis** quantity and must be compared against `Σ(r_0x × …)`, never against the 1× line.
- Stop distance for the C1 filter = `|px_fill − stop|` from the ENTRY row. Its ATR denominator **must** be `atr_exec` from that same ENTRY row (which `replay.py` writes as `sig.atr_x[tr.signal_i]` — the signal-bar ATR the stop was placed with). Using the exit-bar ATR makes the ratio uninterpretable.
- Row joins: ENTRY_FILL/ADD_FILL ↔ EXIT rows join on `tranche_id` within `cell_id`.
- Reject layer discriminator: a REJECT row whose `tranche_id` starts with `trade_` is a **trading-layer** reject; otherwise it is a **signal-layer** reject.

## 5. Numbered fixtures — known-answer gates

Compute each from raw journals. **Any MISMATCH halts the phase.**

| # | Fixture | Expected |
|---|---|---|
| F1 | Scored campaigns / resolved tranches | 3,456 / 8,387 |
| F2 | Σ(realized_r) scored, cell-R | −5,756.9093 (±0.0001) |
| F3 | Σ(r_0x) scored, cell-R | +1,345.3095 (±0.0001) |
| F4 | Σ(r_2x) scored, cell-R | −12,859.1281 (±0.0001) |
| F5 | Taxonomy census | PROTECTED 3,381 · STILLBORN 2,076 · NEVER_GREEN 1,830 · FADED 1,100 |
| F6 | Grade cohorts (campaigns) | A+ 39 · A 1,153 · B 1,954 · C 0 |
| F7 | Stop + stop_gap exits | 8,365 of 8,387 |
| F8 | V-initiated campaigns | 45 |
| F9 | Signal-layer `r_cap` REJECT count | **0** |

**F9 is a falsification fixture, not a formality.** `SS_Cascade_v11_3.pine:145` sets `maxRCount` default 0 (= unlimited), and `signals.py:368` mirrors it. If `r_cap` rejects exist, the anchor config set `max_r_count ≠ 0`, the signal layer *is* capping PRIMEs, and the reviewer's conclusion that "unlimited adds is a trading-config-only change" is **wrong** — which changes the cost of aggressive mode from cheap to Pine-parity-bound. Report the count and the config value side by side either way.

Additionally: paste `signal.z1_prox`, `signal.z2_prox`, `signal.z3_prox`, `signal.max_r_count`, `signal.cooldown_bars`, and the full `trading` block from `v12_anchor.yaml`, plus `cell.zone_memory` and `cell.tf_align` for one cell per mandate. The reviewer has been working from Pine defaults and needs the actual run values.

## 6. The ten deliverables

Each reports **grid-total and per-mandate** (swing / intraday / position) unless stated.

### R1 — Exit-variant ranking
Σ(`exit_XA` × size_r), and the same for XB, XC, XD, as cell-R. Compare each against the actual book **on the same gross basis**: `Σ(r_0x)` = +1,345.31 (F3). Also report each variant's per-mandate delta vs actual, its win rate, and its own 1×/2× lines (apply the row's actual `cost/one_r` as the counterfactual's cost proxy, and **state that this is a proxy** — the counterfactual exits at a different price and holds for a different duration, so its true exit fee and funding differ).
**Caveat to print in the table header:** these are first-order. A really-adopted exit rule changes which adds fire and when campaigns die. Rank, do not validate.

### R2 — V-cohort P&L
The 45 V-initiated campaigns: net cell-R (0×/1×/2×), expectancy + CI, win rate, share of Σwins, share of Σlosses, and their top-5 campaigns by cell-R. Compare their share of Σwins against their share of campaigns (45/3,456 = 1.30%).
**State the discriminator used to identify V-initiated campaigns** — F8 (=45) is its correctness check.

### R3 — MFE-before-death distributions
For tranches that exited at a **gross** loss: deciles of `mfe_r` (per-unit), split by stop class × mandate × grade. Stop class from the field lens: compare the EXIT row's `stop` (= the fill level) against the ENTRY row's `stop` (= stop_at_entry) for the same `tranche_id` → {initial, ratcheted-below-BE, ratcheted-≥-BE}. Report the count and Σ cell-R in each cell of the grid.
**Purpose:** this is the raw material for *fitting* a profit-arming threshold instead of guessing +1R.

### R4 — Harvest-doctrine timing test
Restricted to the 1,581 tranches that reached ≥ +1R MFE and exited at a gross loss: how many had a TPW event fire before their exit, and how many reached a ≥2-ATR extension beyond the exec EMA9 before their exit? Report the median MFE at the first such trigger.
**If TPW is not journaled as an event row**, say so explicitly and derive the answer from the `exit_XB` shadow (which is defined as X-A + 50% banked at first TPW) instead; state which route you took.

### R5 — Shaken-out, per exit event
Report 1's 2,899 resumption count is per-tranche. Because the stop is shared and all open tranches exit together, collapse stop-exit EXIT rows into **exit events** by `(cell_id, dir, ts_open)`, then recount: how many events resumed ≥1R within 20 exec bars, the forfeited-continuation pool in cell-R (10R/unit cap retained), and the per-event median `postexit_cont_20`. Report both the per-tranche and per-event numbers side by side.
**Purpose:** C6's re-entry trigger needs the per-event denominator, not the per-tranche one.

### R6 — Zone × stage cross-tab
Cross-tabulate `zone` (Z1/Z2/Z3/–) against `stage` (1/2) over all ENTRY_FILL and ADD_FILL rows. Report counts, and expectancy + Σ cell-R per cell of the table. Split by direction (long/short).
**Purpose:** tests P-R6 (§7). Also report, for stage-2 rows only, the count with `zone = Z2`.

### R7 — Reject funnel, split by layer
All REJECT rows, counted by `reject_reason`, split by layer per the §4 discriminator, per mandate:
- **Signal layer:** `no_zone`, `structure`, `bar_range`, `ribbon_sep`, `cooldown`, `r_cap`
- **Trading layer:** every distinct reason present — enumerate what you find, do not assume the list. Report `tranche_cap` and `add_ineligible` counts explicitly.

**Two numbers are load-bearing:** `r_cap` (fixture F9) and `tranche_cap` — the latter counts exactly how many adds the current 3-tranche ceiling turned away, which sizes the operator's aggressive-mode decision **before** any run is spent. Also report `no_zone` and `ribbon_sep` counts, which size VS-Z3.

### R8 — Expectancy by zone, including Z3
Per-tranche net/unit, Σ cell-R, and count by `zone` ∈ {Z1, Z2, Z3}, and campaign-level expectancy by the initiating tranche's zone. Report 1 published Z2 vs Z1 and **never published Z3** — Z3 is the governor 89–200 band retest cohort, and it is the operator's stated primary structural setup. Close the gap.

### R9 — Risk-mode first-order table (defensive + neutral only)
Neutral = the live line as journaled (the control). Defensive = tranche-level filters, journaled **decomposed** so the bundle can be taken apart:

| Column | Filter |
|---|---|
| `def_c1_only` | drop tranches with `stop_distance / atr_exec(ENTRY) < 0.5` |
| `def_c1_grade` | `def_c1_only` **+** drop tranches with `grade` ∉ {A, A+} |
| `def_full` | `def_c1_grade` **+** retracement size tilt: re-weight `size_r` × 1.5 for `retr ≥ 0.5`, × 0.5 for `retr < 0.25`, × 1.0 otherwise |

For each column: Σ cell-R at 0×/1×/2×, campaigns, win rate, expectancy + CI, strip-best.
**Print this caveat in the header:** first-order only. Removing or re-weighting a tranche does not change the stop path (the ratchet is signal-layer and independent of fills), but it *does* change the equity path, the 1R campaign rail, and the halt calendar — all of which gate admission. Faithful measurement is S-1's job.
**Aggressive mode is out of scope here** — it creates tranches that do not exist in these journals. Note that explicitly in the deliverable.

### R10 — Fee Stage A (maker-entry bound)
Recompute the grid assuming **maker entries (2 bps/side) and taker stops (5 bps/side)**, fills otherwise unchanged:
`cost_maker = cost_total − entry_fee × (3/5) − entry_slippage`, then `r_maker = realized_r + (cost_total − cost_maker) / one_r`.
Report Σ cell-R at the maker-entry basis, the delta vs the 1× line, and the fee/slippage/funding split before and after.
**Print this caveat:** this is the *optimistic* bound. It assumes every entry fills as a maker and none is missed. Chase orders miss most when price runs away immediately — which is disproportionately the character of the entries that become tail campaigns. The bound is a ceiling, not an estimate. Also print the ceiling on all execution improvement: the 0× line, +1,345.31.

## 7. Pre-registered predictions — register before running, score after

| # | Prediction | Prior | Falsified if |
|---|---|---|---|
| **P-R1** | X-A-family exits beat the actual book (gross basis) on swing **and** position; ambiguous-to-negative on intraday | 70% | X-A loses on swing or position, or wins clearly on intraday |
| **P-R2** | The 45 V campaigns are **not** disproportionately tail-carrying — their share of Σwins < 3× their share of campaigns (< 3.9%) | 50% | V's share of Σwins ≥ 3.9% |
| **P-R6** | ≥95% of Z2-active entries carry `stage = 1` | 85% | < 95% |
| **P-R7** | `tranche_cap` rejects > 500 (aggressive mode is a real axis, not a non-event) | 60% | ≤ 500 |
| **P-R9** | `def_full` remains **net negative** at 1× — no defensive bundle flips the grid sign in-sample on mined data | 60% | `def_full` 1× ≥ 0 |

Carried from Report 2, unchanged: **P-S1a** (de-ratchet / loosening-while-open events = 0) and **P-S1b** (non-advancement explains ≥⅓ of +1R-to-loss round-trips) are **S-1** items, not scored here.

## 8. Verdict criteria

- **PASS** — all nine fixtures MATCH; all ten deliverables produced; all five predictions scored; determinism hash stated; config values pasted.
- **HALT** — any fixture MISMATCH. Stop immediately, report the mismatch with the computed and expected values, do not produce downstream tables. A fixture mismatch means the reader is wrong, not the data.
- **PARTIAL** — a deliverable is not computable from journaled fields. Say which field is missing, name the row type it would live on, and stop that item. **Do not substitute an estimate.** A named gap is a better deliverable than a fabricated number.

## 9. Output artifacts

1. `scripts/v3_recompute.py` — the script, committed.
2. `V3_RECOMPUTE_R1_R10.md` — the tables, human-readable, each with its caveat header.
3. `recompute.json` — machine-readable, for reviewer verification.
4. `LEDGER.md` entry — builder-typed, appended, never edited in place.

## 10. Ledger entry template

```
[YYYY-MM-DD] V3 RECOMPUTE R1–R10 — Tier A, journals-only
Basis: engine 1.0.7 (2f260e1), config v12_anchor (a3917ea5…), scored partition, 20 cells
Evidence spend: NONE (VR-1 exploration-classic, first look already consumed)
Engine delta: NONE (read-only phase; no code, config, or replay touched)
Fixtures: F1–F9 [MATCH / MISMATCH — list any]
Predictions scored: P-R1 [..] P-R2 [..] P-R6 [..] P-R7 [..] P-R9 [..]
Determinism: script re-run hash [..] identical [Y/N]
Artifacts: scripts/v3_recompute.py, V3_RECOMPUTE_R1_R10.md, recompute.json
Operator ratification: 2026-07-15 (D1, D2, D4–D9 on silence; D3 VS-Z3 HELD)
Open: G-7 (in-sample iteration budget untracked) logged this phase
```

Also append the new register item:
```
G-7 [OPEN]: No counter — code-level or ledger-level — on tuned exploration-classic
re-runs. The five named-variant slots bind only at the lockbox; nothing tracks
Tier-C iteration on mined data. Mitigation: every Tier-C exploration-classic run
gets a pre-registered ledger line (config sha + hypothesis + prediction) BEFORE it
runs. Logged 2026-07-15 on operator ratification of D7.
```

---

## 11. The go-paste

```
CONTRACT: V3 Recompute R1–R10 (Tier A — journal arithmetic only)

Read the contract file V3_Recompute_R1_R10_Builder_Contract.md in full before writing
any code. It is the authority; this paste is only the trigger.

Scope in one line: compute ten tables from the existing V3 anchor journals. Read-only.
No engine changes, no config changes, no replay execution, no network.

Order of work — do not reorder:

1. UNIT CONVENTIONS (contract §4). State back to me, in your own words, what cell-R is,
   what R/unit is, which row one_r comes from, and why exit_XA must be compared against
   the 0x line and not the 1x line. Do not proceed until you have written this out.

2. CONFIG PASTE (contract §5). Print from v12_anchor.yaml: signal.z1_prox, signal.z2_prox,
   signal.z3_prox, signal.max_r_count, signal.cooldown_bars, and the entire trading block.
   Print cell.zone_memory and cell.tf_align for one cell per mandate. The reviewer has been
   working from Pine defaults and needs the real run values.

3. FIXTURES (contract §5, F1–F9). Compute all nine from raw journal bytes. Do NOT read
   ROLLUPS_AND_HYPOTHESES.md or V3_STOP_AND_EXIT_FORENSICS.md as inputs — they are
   cross-checks, not sources. Print a table: fixture / expected / computed / MATCH-MISMATCH.

   *** IF ANY FIXTURE MISMATCHES: STOP. Report it. Produce nothing downstream. ***
   A mismatch means the journal reader is wrong and every table after it is garbage.

   F9 especially: r_cap reject count should be 0. If it is not, say so loudly — it means
   max_r_count != 0 in the anchor config, and the reviewer's conclusion that "unlimited
   adds is a trading-config-only change" is FALSE. Print the count next to the config value.

4. DELIVERABLES R1–R10 (contract §6). Grid-total and per-mandate for each. Print each
   item's stated caveat in its table header — the caveats are part of the deliverable.
   If any item is not computable from journaled fields: name the missing field, name the
   row type it would live on, mark the item PARTIAL, and move on. DO NOT substitute an
   estimate. A named gap beats a fabricated number.

5. PREDICTIONS (contract §7). Score all five: P-R1, P-R2, P-R6, P-R7, P-R9. Report the
   falsified ones as prominently as the confirmed ones.

6. DETERMINISM. Run the script twice. State the output hash both times and whether they
   are identical.

7. ARTIFACTS. Commit scripts/v3_recompute.py, V3_RECOMPUTE_R1_R10.md, recompute.json.
   Append the ledger entry and the G-7 register item using the templates in contract §10.
   Builder-typed, appended, never edited in place.

Do NOT do any of the following, even if it seems helpful:
 - change any config value or engine file
 - execute replay.py or any backtest
 - fetch any data
 - touch the lockbox partition or include annex rows in scored aggregates
 - implement the z3_prox change (VS-Z3 is HELD by the operator)
 - attempt aggressive-mode numbers (those tranches do not exist in these journals)
 - merge anything (all merges are operator-only)

Report back: the config paste, the fixture table, the ten deliverables, the prediction
scorecard, the determinism hashes. Summaries will not be accepted without the artifacts —
the reviewer recomputes independently.
```

---

*Contract prepared by the reviewer under Fable-mode, 2026-07-15. Every field name, row type, and unit convention cited here was read from `replay.py`, `trading.py`, `signals.py`, `SS_Cascade_v11_3.pine`, or the run `manifest.json` this session. Fixture values F1–F8 restate the reviewer-verified record of 2026-07-13; F9 is a new falsification gate on the reviewer's own reading of the Pine. Nothing in this phase changes any rule.*
