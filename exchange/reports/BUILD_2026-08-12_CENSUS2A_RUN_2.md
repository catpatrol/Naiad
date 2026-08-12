# CENSUS-2A · RUN 2 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract (single source):** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` `sha256 b0da051b…`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (all scored tables ≤ 2024-07-01)

**Zero context assumed.** This document is complete on its own.

---

## 0 · WHAT RAN

Run 2 resumed at CEN-3, as sequenced. **One whole stage completed: CEN-3.** The session then stopped at a stage boundary per the budget rule, on a dependency I am not entitled to resolve unilaterally (§5).

| | State |
|---|---|
| Hard assertions (15) + **live pin check** | **PASS** — run-1 pins `{preflight, F-GUARD, F-PIN, CEN-0b, CEN-1, CEN-2}` all present *before* any work |
| **CEN-3 OUTCOMES** | **DONE** — R-1 ruler, dual-lens, held-in-time, fate-stratified, **P-REL-1 scored** |
| CEN-4 … CEN-9 | **REMAINING** — CEN-4 blocked on a forward dependency, §5 |

**F-PIN proved itself across sessions, not just in fixture.** Run 1's pins were present and intact at the start of run 2, and the CEN-3 run logged `merging into existing manifest (3 stages)`. I12 works in practice.

---

## 1 · FIXTURE TRANSCRIPT (full)

```
=== HARD ASSERTIONS ===
  HEAD   : 035eb2c
  PASS  remote contains catpatrol/Naiad
  PASS  pwd ends C:/Naiad or /c/Naiad                        C:/Naiad
  PASS  pwd does NOT contain OneDrive
  PASS  branch == v12-v1-census                              v12-v1-census
  PASS  test -f exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md
  PASS  test -f scripts/census2a_program.py
  PASS  test -f scripts/drive_wait.py
  PASS  DRIVE GATE PRESENT|WOKE    PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s
  PASS  test -f census2a_manifest.json

=== PIN CHECK (F-PIN live -- run-1 pins must survive) ===
  PASS  run-1 pin present: preflight (top-level)
  PASS  run-1 pin present: F-GUARD (fixtures)
  PASS  run-1 pin present: F-PIN (fixtures)
  PASS  run-1 pin present: CEN-0b (stages)
  PASS  run-1 pin present: CEN-1 (stages)
  PASS  run-1 pin present: CEN-2 (stages)

=== per-run gating (I11: guard BEFORE any sweep) ===
F-GUARD  NULL sweep    m=12 p_sel=0.6742 bar=0.00833 -> admissible=False   PASS (declines)
         (1/12 null candidates cleared a NAIVE CI -- why the guard exists)
         PLANTED sweep m=12 winner=plant5 p_sel=0.0007 -> admissible=True  PASS (admits, names it)
F-PIN    prior pins + artifacts + sections carried forward alongside the new pin  PASS
```

CEN-3 performs **no sweep-and-select** — P-REL-1 is a single pre-named comparison (12_25-triggered vs other), so the I11 guard has nothing to gate here. It ran anyway, as the gate on the stage, and passed.

---

## 2 · CEN-3 · OUTCOMES (complete)

Ruler per **R-1**: signed **terminal** return, ATR-normalised at the anchor. MFE, MAE, the MFE/|MAE| quality ratio and the toll line print beside it — never in place of it. Horizons are duration-fixed (H20 = 1h40m, H100 = 8h20m, H500 ≈ 1.74d), converted per timeframe.

### 2.1 · Toll line (I8 — beside every excursion table)

Global **10 bps round trip** (`fee_bps_side: 5.0`; per-mandate values do not exist). Converted to ATR units per asset, because an excursion in ATR cannot be compared to a cost in bps without it:

| BTC | ETH | ZEC | SOL | NEAR |
|---:|---:|---:|---:|---:|
| 0.0581 | 0.0458 | 0.0333 | 0.0277 | 0.0257 |

**This matters immediately.** Several per-asset terminal medians below are of the same order as the toll (BTC-down −0.0012, SOL-down −0.0175, NEAR-up +0.0577). An edge that does not clear its own toll line is not an edge, and the table says so on its face.

### 2.2 · Outcome panel, per asset × direction (terminal H100, ATR)

| Asset | Dir | n | terminal | MFE | MAE | Quality | toll |
|---|---|---:|---:|---:|---:|---:|---:|
| BTCUSDT | up | 97 | +0.1392 | 0.704 | 0.511 | 1.378 | 0.058 |
| BTCUSDT | down | 98 | −0.0012 | 0.694 | 0.497 | 1.394 | 0.058 |
| ETHUSDT | up | 89 | +0.1590 | 0.585 | 0.459 | 1.273 | 0.046 |
| ETHUSDT | down | 90 | +0.0590 | 0.594 | 0.462 | 1.285 | 0.046 |
| SOLUSDT | up | 75 | +0.2077 | 0.873 | 0.442 | **1.975** | 0.028 |
| SOLUSDT | down | 74 | −0.0175 | 0.588 | 0.408 | 1.443 | 0.028 |
| NEARUSDT | up | 73 | +0.0577 | 0.764 | 0.567 | 1.347 | 0.026 |
| NEARUSDT | down | 74 | **−0.2227** | 0.560 | 0.540 | 1.036 | 0.026 |
| ZECUSDT | up | 89 | +0.1846 | 0.567 | 0.601 | **0.943** | 0.033 |
| ZECUSDT | down | 89 | +0.1365 | 0.638 | 0.438 | 1.458 | 0.033 |

**Per-direction asymmetry is visible in every asset and is not uniform.** Longs beat shorts in 4 of 5; NEAR-down is the worst cell on the board (−0.2227) while NEAR-up is positive. ZEC is the only asset whose *up* quality ratio is below 1.0 (MFE < MAE) despite a positive terminal median — the move arrives, but it is paid for in adverse excursion first. **Reported, not fixed.**

### 2.3 · I6 DUAL-LENS — both always printed

Cascades built by **`seq8_views.build_cascades`**, the estate's own rule, over the lattice-A stream (151,718 events, 6 timeframes, 3 classes).

| | window_chained *(PRIMARY — entry claims)* | direction_consistent *(printed)* |
|---|---|---|
| cascades | 98,727 | 101,549 |
| max depth | 6 | 6 |
| arming depth (mean) | 3.21 | 2.99 |

Terminal H100 by arming depth:

| depth | window_chained | direction_consistent |
|---|---|---|
| 1 | −0.8955 *(n=5)* | +0.0605 *(n=101)* |
| 2 | +0.1025 *(n=358)* | +0.1083 *(n=304)* |
| 3 | +0.0577 *(n=148)* | +0.0876 *(n=135)* |
| 4+ | +0.0387 *(n=337)* | +0.0261 *(n=308)* |

The two lenses agree on shape (depth 2 best, decaying after) but **disagree sharply at depth 1** — where window_chained has only 5 armings and direction_consistent has 101. That is the lens doing exactly what MC-1 said it does: `direction_consistent` terminates chains at counter-crosses, so it produces many more shallow chains. Depth-1 under window_chained is n=5 and must not be read as a finding.

### 2.4 · Held-in-time split (I8)

Split at **2022-07-06 12:00** — early 424 / late 424 armings. Full table: `cen3_by_half.parquet`.

### 2.5 · Fate-stratified view *(clarification 1 of record)*

> **MECHANICAL SEPARATION — an ABORTED window is a regime flip INSIDE the horizon, so its terminal return is negative BY CONSTRUCTION. The sign of this split is NOT a finding.**

| Fate | n | terminal H100 | p25 | p75 | median width |
|---|---:|---:|---:|---:|---:|
| COMPLETED | 595 | +0.2421 | −0.155 | +0.704 | 48 |
| ABORTED | 252 | −0.4767 | −0.938 | −0.018 | 4 |
| ROTTED | 1 | +0.9820 | — | — | 151 |

The caveat is carried **in the table header, in the parquet (`_caveat` column) and in the manifest** — not in a footnote someone can quote around. What *is* informative is the spread: COMPLETED's interquartile range straddles zero (−0.155 → +0.704), so a completed window is not a good outcome, only a longer-lived one.

### 2.6 · P-REL-1 — SCORED (text before result, F-8)

> **P-REL-1 [prior 60%]** (entry lens = `24h|window_chained`): *"windows with an in-window 12_25 trigger → higher trigger-anchored terminal return than A-only windows."*

| 12_25-triggered | other | asset-cluster 90% CI on the difference | Criterion |
|---:|---:|---|---|
| 155 | 440 | **[+0.0933, +0.2876]** — excludes 0 | R-2 asset-cluster CI |

**VERDICT: SUPPORTED.** The first supported registration in the census. The effect (+0.19 ATR at the midpoint) clears every asset's toll line by 3–7×. Single pre-named comparison — no sweep, so no selection correction applies.

---

## 3 · A DEFECT IN MY OWN LENS IMPLEMENTATION, FOUND AND FIXED

I6 requires both lenses printed from CEN-3 onward. My first two attempts at the lens both **degenerated**, and each would have satisfied I6 in letter while printing a constant:

| Attempt | Result | Why it was wrong |
|---|---|---|
| 1 — chain the 4h 9/89 armings | `direction_consistent` **max_depth = 1 for all 848** | consecutive 9/89 crosses on one timeframe *strictly alternate* direction, so a direction-change rule breaks every chain immediately |
| 2 — chain the pooled lattice-A stream | `window_chained` **23 chains, mean depth 1,733** | with 5m events included, a 24h window never breaks — one giant chain per asset |
| 3 — **delegate to `seq8_views.build_cascades`** | both lenses vary, max depth 6 | ✅ |

The real rule has three properties not implied by its name, all of which I had missed: cascades are built per **(asset, event class)** rather than over a pooled lattice; **every rung must be a NEW timeframe** (a cascade is a ladder across timeframes); and chaining is **greedy and non-overlapping**.

**The lesson is the one this project already learned about detectors:** reimplementing a definition the estate owns is how two things stop being comparable. The fix was to import it. A third bug surfaced on the way — the join key `(asset, ts)` is not unique, because a 4h and a 12h bar can share an open_time of 00:00; the key needs the timeframe.

---

## 4 · FINDINGS REPORTED, NOT FIXED

1. **Several per-asset terminal medians do not clear their own toll line** (§2.1). BTC-down, SOL-down and NEAR-up are at or below 10 bps in ATR terms.
2. **NEAR-down is the worst cell on the board** (−0.2227 terminal H100) while NEAR-up is positive. Per-direction asymmetry is asset-specific, not a panel property.
3. **ZEC-up has quality ratio 0.943** — MFE below MAE despite a positive terminal median.
4. **COMPLETED's IQR straddles zero.** "Completed" means the window lived long enough to contain a trigger; it does not mean the outcome was good.
5. **Depth-1 under `window_chained` is n=5** and its −0.8955 median must not be read as a finding.
6. **CEN-4 is blocked on a forward dependency** — §5.

---

## 5 · WHY THE SESSION STOPPED HERE (a dependency, not just budget)

**CEN-4's chop composite has five components, and the fifth is `verdict-open` — a CEN-6 output.** The contract sequences CEN-4 before CEN-6, so as written the composite cannot be assembled at CEN-4 time.

Running CEN-4 on four of five components is **not** a safe workaround: P-CHOP-1 is registered as *"chop-composite **≥3** captures ≥40% of loser-decile births at TRG ≥85%"*, and a ≥3 threshold against a 4-component composite is a different hypothesis than ≥3 against a 5-component one. Changing it silently would be re-pinning a constant mid-run, which §N of the contract forbids ("a change is a new [VETO]-named amendment").

**Three clean resolutions, operator's call:**
- **(a)** run **CEN-6 before CEN-4** (the dependency direction the data implies), then CEN-4 with all five components — *recommended*;
- **(b)** amend P-CHOP-1's threshold by name for a 4-component composite;
- **(c)** define `verdict-open` independently of CEN-6.

**The population is ready either way:** WF1 holds **7,117 births / 7,094 resolved exits** — exactly the contract's R-7 figures — with `realized_r`, `mfe_r`, `mae_r`, `give_back_r`, `ts_open_epoch` and `resolved` per row. CEN-4 and CEN-5 are unblocked the moment the composite is settled.

---

## 6 · DISPOSITION (with BOX-COST)

| Artifact | Class | Home | Rows | Bytes | Disposition |
|---|---|---|---:|---:|---|
| `cen3_ledger_lensed.parquet` | EVIDENCE | `D:` | 848 | 118,411 | keep on D:, pointer here |
| `cen3_trigger_outcomes.parquet` | EVIDENCE | `D:` | 595 | 61,876 | keep on D:, pointer here |
| `cen3_by_asset.parquet` | EVIDENCE | `D:` | 10 | 10,960 | keep on D:, pointer here |
| `cen3_by_depth_window_chained.parquet` | EVIDENCE | `D:` | 4 | 9,833 | keep on D:, pointer here |
| `cen3_by_depth_direction_consistent.parquet` | EVIDENCE | `D:` | 4 | 9,833 | keep on D:, pointer here |
| `cen3_by_fate.parquet` | EVIDENCE | `D:` | 3 | 9,173 | keep on D:, pointer here |
| `cen3_by_half.parquet` | EVIDENCE | `D:` | 2 | 9,539 | keep on D:, pointer here |
| run-1 artifacts (5) | EVIDENCE / DISPLAY | `D:` | — | 40,153,600 | unchanged, pins intact |
| this build document | report | `exchange/reports/` | — | ~15 KB | **rides the publish** |
| `LEDGER_APOLLO.md` append | record | `exchange/status/` | — | ~2.5 KB | **rides the publish** |

**BOX-COST: bus additions this session ≈ 0.28% of the 6,390,000 B box — under the 1% rule (F-14).** No results JSON enters `exchange/`; everything is on `D:` by pointer. `exchange/` stands at **29.96%** (WARN band, below the 40% refuse line). Total D: footprint: **70 MB**.

**Pointers (full paths):** `D:\Naiad\research_outputs\census2a\cen3\` · `…\cen2\` · `…\cen1\` · `…\klines\PAXGUSDT\` · `…\census2a_manifest.json`

---

## 7 · CACHED vs REMAINING

**Cached (complete, on `D:`, hash-recorded, pins verified live this session):**
preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · **CEN-0(b)** · **CEN-1** · **CEN-2** · **CEN-3**.
Registrations scored: **P-ARM-1** (NOT SUPPORTED, confound disclosed — run 1) · **P-REL-1** (SUPPORTED — this run).

**Remaining:** **CEN-4** (blocked, §5) · CEN-5 · CEN-6 · CEN-7 *(incl. the i-b registry-levels completion and the two-limb reconciliation table — clarification 2, not started)* · CEN-8 · CEN-9.
Registrations unscored: P-iii-b, P-NEST-1, P-i′, P-iv′, P-CHOP-1, P-RAT-2, P-VBT-1 (**7 of 9**).

**Run 3 starts at the operator's answer on §5, then CEN-6 → CEN-4 → CEN-5 → CEN-7 → CEN-8 → CEN-9.**

---

## 8 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12d ===
NOW: CENSUS-2A run 2 complete. CEN-3 (outcomes) ran end to end under the R-1 ruler with both I6
lenses printed, the held-in-time split, the fate-stratified view carrying its mechanical-separation
caveat, and P-REL-1 scored SUPPORTED. Stopped at a stage boundary: CEN-4 is blocked on a forward
dependency, not on budget alone.
LAST EVENT: 2026-08-12 — run 2: CEN-3 done; P-REL-1 SUPPORTED; lens implementation corrected twice
before it was right
FACTS:
- F-PIN held ACROSS SESSIONS: run-1 pins {preflight, F-GUARD, F-PIN, CEN-0b, CEN-1, CEN-2} were all
  present before any run-2 work, and CEN-3 logged "merging into existing manifest (3 stages)" [verified]
- P-REL-1 SUPPORTED: 12_25-triggered windows n=155 vs other n=440, asset-cluster 90% CI
  [+0.0933, +0.2876] excludes zero. First supported registration in the census. The effect clears
  every asset's toll line by 3-7x [verified]
- MY OWN LENS IMPLEMENTATION WAS WRONG TWICE. Attempt 1 gave direction_consistent max_depth=1 for
  all 848 armings (4h 9/89 crosses strictly alternate direction); attempt 2 gave window_chained 23
  chains of mean depth 1,733 (a 24h window never breaks once 5m events are included). Fixed by
  DELEGATING to seq8_views.build_cascades -- cascades are per (asset, event_class), every rung must
  be a NEW timeframe, and chaining is greedy non-overlapping [verified]
- Several per-asset terminal medians do NOT clear the 10 bps toll line in ATR terms (BTC-down
  -0.0012, SOL-down -0.0175 vs tolls 0.058 / 0.028). NEAR-down is the worst cell at -0.2227 [verified]
- COMPLETED's interquartile range straddles zero (-0.155 to +0.704): a completed window is a
  longer-lived one, not a better one [verified]
PENDING:
1. PX-1 (PAXG disposition) — PENDING-OPERATOR. Carried from run 1: PAXG's perp begins 2025-03-27,
   nine months after the evidence wall, so it holds ZERO evidence-era bars and can never enter a
   scored table under I1. It cannot be the independent jury D-D intended. What PAXG is FOR is the
   operator's decision; the builder will not assume it
2. CEN-4 BLOCKED: its chop composite's fifth component (verdict-open) is a CEN-6 output, but the
   contract sequences CEN-4 first. Running on 4 of 5 components would silently change the >=3
   threshold P-CHOP-1 is registered against — a mid-run re-pin, which §N forbids. Options: (a) run
   CEN-6 before CEN-4 [recommended], (b) amend P-CHOP-1 by name, (c) define verdict-open
   independently
3. P-ARM-2 — FILED as a next-cycle registration, prior 55%, UNSCORED. It is the hazard / competing-
   risk successor to P-ARM-1's trigger-rate limb, which run 1 showed is confounded by exposure time
   (WALL-true windows median 8 bars vs 30; conditioned on width>=48 the trigger rates converge to
   1.000 vs 0.985). Builder's reading of the identifier; the operator should correct it if the
   intent differs, and the text is not final until the operator words it
4. CEN-7's i-b registry-levels completion (clarification 2) not started; run-1 covered long EMAs only
5. 7 of 9 registrations remain unscored
NEXT: Operator answers PENDING 2 (the CEN-4/CEN-6 ordering), then run 3 proceeds
CEN-6 -> CEN-4 -> CEN-5 -> CEN-7 -> CEN-8 -> CEN-9. Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (the run-2 sequencing paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 2 · CEN-3 complete; stopped on a named dependency, not silently
