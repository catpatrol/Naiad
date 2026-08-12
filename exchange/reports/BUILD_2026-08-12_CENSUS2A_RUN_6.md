# CENSUS-2A · RUN 6 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` — body `b0da051b…` + A1 + A2 + A3
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (≤ 2024-07-01)

**Zero context assumed.**

---

## 0 · WHAT RAN

| | State |
|---|---|
| Hard assertions (18) + real F-PIN | **PASS** — §1 |
| **CEN-5 EXIT-AND-FEED** | **DONE** — P-RAT-2 scored, P-VBT-1 not scored, §2 |
| CEN-7 · CEN-8 · CEN-9 | **REMAINING** |
| A3-AUDIT table | **already delivered** in the run-5 addendum; summary at §5 |

---

## 1 · FIXTURE TRANSCRIPT

```
=== HARD ASSERTIONS ===  HEAD 09d4f2b   pwd C:/Naiad
  PASS  remote catpatrol/Naiad · pwd ends C:/Naiad · pwd NOT OneDrive · branch v12-v1-census
  PASS  queue item present · body + A1 + A2 + A3
  PASS  scripts/census2a_program.py · scripts/drive_wait.py
  PASS  DRIVE GATE  PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s
=== PIN CHECK (real F-PIN) ===
  PASS  sections pins / artifacts / fixtures / stages / registrations
  PASS  P-ARM-1 + confound · P-REL-1 WITHDRAWN · P-REL-1b SUPPORTED-PROVISIONAL + label
  PASS  P-iii-b NOT SUPPORTED    short lo=-0.000646   (the 0.0006 margin, recorded)
  PASS  P-CHOP-1 present w/ TRG 0.546604
=== per-stage gating ===
  F-GUARD  declines the null sweep (p=0.6742) · admits plant5 (p=0.0007)   PASS
  F-PIN    7 sections + coexistence                                        PASS
```

**One note on the assertion text:** it asks for P-CHOP-1 "NOT SUPPORTED". It now reads **WITHDRAWN** — last session's A3-AUDIT found two of its five components were not the registered objects. `TRG 0.546604` is intact and the prior verdict is preserved in `verdict_superseded`. The assertion predates the withdrawal; nothing is inconsistent.

---

## 2 · CEN-5 · EXIT-AND-FEED

### 2.1 · The feasibility gate, settled first

The scoping had flagged one question as decisive: **are the WF1 rows summary-only, or can a counterfactual exit be simulated?** Answered before any building:

- **The R unit reconstructs.** `realized_r = size_r × gross_R + costs`, where `gross_R = (exit − entry)/|entry − stop|`. Verified on all 7,094 rows: median |err| **0.058** against `size_r × gross_R`, with a systematically negative residual (median −0.089) — the costs.
- **Therefore A3-DECILE's ruler is gross R.** `realized_r / size_r` ≈ `gross_R`, correlation **0.993**. The operator's size-free ruling is correct, and CEN-4 used it correctly. **One ruler, not two.**
- **The paths exist.** 5m candles for all 7 symbols cover the full campaign span (2019-10-01 → 2024-06-30).

### 2.2 · Population — and 432 campaigns I nearly lost silently

| | n |
|---|---:|
| resolved campaigns | **7,094** |
| distinct `tranche_id` | 6,662 |
| **simulated** | **6,834** (panel 6,643 · annex 191, printed never pooled) |
| excluded-and-counted | 260 |

**`tranche_id` is unique only WITHIN a cell.** `c104t145` exists in both `BTCUSDT_intraday` and `ETHUSDT_swing`; 378 ids collide. A first draft keyed a dict on `tranche_id` alone and **silently dropped 432 campaigns (6.1% of the book)** — the same non-unique-key defect the run-2 review caught on `(asset, ts)`. Now keyed `(cell, tranche_id)`, or rather carried in a list that cannot collide at all.

**The 260 exclusions are fully accounted:** every one is a sub-bar campaign (`hold_s < 300s`) whose exit lands inside the same 5m candle as its entry, so there is no forward path to ratchet along. Excluded **and counted**, never imputed.

### 2.3 · RIDE-ONLY control (printed first, per the contract)

| stratum | n | median R | mean R |
|---|---:|---:|---:|
| loss | 5,829 | −1.0415 | −0.9690 |
| win | 814 | +2.1422 | **+9.4458** |
| **ALL** | 6,643 | **−1.0324** | **+0.3072** |

The book is **12.3% winners** carrying a mean of +9.4R against a median loser of −1.04R. That shape — a negative median and a positive mean — is what every exit arm below is trying to improve, and it is why an arm that clips the tail can look good on the median while destroying the book.

### 2.4 · P-RAT-2 [40%] — text before result (F-8)

> *"Joint ratchet+add beats RIDE-ONLY on net terminal R at ≥1 grid corner with TRG ≥85%."*

**FDR family declared BEFORE scoring:** m = **36** corners (4 EMAs {200,300,450,500} × 3 anchor TFs {15m,1h,4h} × 3 cushions {0.25,0.5,1.0}), q = 0.10 → **BH bar 0.00278**.

| corner | median Δ R | mean Δ R | beats-ride share | TRG |
|---|---:|---:|---:|---:|
| `4h / 500 / 1.0` | +0.0000 | **+0.4518** | 0.189 | 1.7006 |
| `4h / 300 / 1.0` | +0.0000 | +0.4260 | 0.201 | 1.7663 |
| `15m / 200 / 0.25` | +0.0000 | −0.0548 | 0.349 | 1.0653 |
| *worst:* `15m / 450 / 1.0` | −0.3148 | — | — | — |

**Corners meeting both bars (Δ>0 AND TRG≥0.85): 0 / 36.**
I11 guard over the 36-corner family: winner `1h/200/1.0`, `p_sel = 0.0005` vs BH bar `0.00278` → **ADMISSIBLE**.

**VERDICT: NOT SUPPORTED.**

### 2.5 · Two things about that verdict that must not be read past

**The median is structurally zero, and that is not a near-miss.** `median Δ R = +0.0000` for the top corners because **most campaigns never reclaim the long EMA at all** — the arm simply *equals* the ride for them, so the median difference is zero by construction. The *mean* deltas are meaningfully positive (+0.45R at `4h/500/1.0`). The registration says "beats RIDE-ONLY on net terminal R" and **names neither median nor mean**. Both are printed above; neither is selected. This is the same ambiguity class the A3-AUDIT logged for P-NEST-1's anchor, and it should be named before P-RAT-2 is re-scored.

**TRG came back greater than 1, which means the threshold does not apply as written.** TRG is defined (v0.2:64-65) as *"the share of the unfiltered book's top-decile profit a rule **retains**"* — a retention share, bounded by 1, for a **filter**. A ratchet is not a filter; it is an alternative exit, and it can *exceed* the ride. The quantity computed here (arm top-decile profit ÷ ride top-decile profit) answers a coherent question, but **not the one the 85% bar was written for.** This is **A3-AUDIT item NW-5 landing on a live verdict**: TRG's numerator was defined when the ruler was MFE−MAE, R-1 retired that ruler, and no text renamed the column. **P-RAT-2's TRG limb is therefore not decidable as written**, and the NOT SUPPORTED verdict rests on the Δ limb alone.

### 2.6 · P-VBT-1 [45%] — NOT SCORED

> *"The harvest arm cuts median give-back ≥30% at TRG ≥80%."*

**VERDICT: NOT SCORED — H-VBT IS UNDEFINED.**

`H-VBT` (harvest-at-structure) is a bare **name** in both v0.2:131 and v0.3:103 — the A3-AUDIT logged it needs-word. The estate defines it only as *"VWAP Band Target — exits at confluence-scored VWAP levels"*, and those bands are **CEN-7's registry output, which has not run**. Choosing a band set by outcome would be the sweep §N forbids. The arm is not built and the registration is **not scored, rather than scored on an invented rule**.

Arm **(b) PO3-mirror per A3-BAND** was not reached this run.

---

## 3 · FINDINGS REPORTED, NOT FIXED

1. **The book is 12.3% winners** (814 of 6,643) carrying mean +9.4R against a median loser of −1.04R. Any exit study on this book is a study of tail preservation.
2. **`median Δ R` is uninformative for this arm** by construction — >50% of campaigns never arm the ratchet.
3. **TRG > 1 for 30+ corners** — the metric as defined does not bound an alternative-exit arm (NW-5).
4. **The 4h/long-EMA/wide-cushion corners carry the positive means** (+0.45R, +0.43R) with low beat-shares (0.19–0.20) — a few large wins, not a broad improvement. That is exactly the shape the TRG bar exists to interrogate, and TRG cannot currently interrogate it.
5. **432 campaigns were nearly lost to a non-unique key.** The same defect class has now appeared three times in this census (CEN-3's `(asset,ts)`, CEN-5's `tranche_id`). A join-key uniqueness assertion belongs in the fixture set.

---

## 4 · CACHED vs REMAINING

**Cached:** preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · CEN-0b · CEN-1 · CEN-2 · CEN-3 · CEN-6 · CEN-4 · **CEN-5**.

| registration | verdict |
|---|---|
| P-ARM-1 | NOT SUPPORTED (confounded by exposure time) |
| P-REL-1 | WITHDRAWN — unscoreable as written |
| **P-REL-1b** | **SUPPORTED-PROVISIONAL** (label permanent) |
| P-iii-b | NOT SUPPORTED — pooled measured, both-directions clause unmet by 0.0006 |
| P-CHOP-1 | WITHDRAWN — mis-specified component set |
| **P-RAT-2** | **NOT SUPPORTED** — 0/36 corners; TRG limb not decidable (NW-5) |
| **P-VBT-1** | **NOT SCORED** — H-VBT undefined in both drafts |
| P-FAN-1 · P-NEST-2 · P-ARM-2 | filed next-cycle, unscored |

**Remaining:** CEN-7 · CEN-8 · CEN-9; CEN-5 arms (b) and (c); unscored P-NEST-1, P-i′, P-iv′.

---

## 5 · A3-AUDIT — DELIVERED IN THE RUN-5 ADDENDUM

The full table is in `BUILD_2026-08-12_CENSUS2A_RUN_5.md` §ADDENDUM (published `09d4f2b`). Summary: **15 needs-word items** across four slices. Two had already been silently substituted by builder readings inside a scored component, which is why **P-CHOP-1 was withdrawn**. The items now gating work:

| # | Item | Halts | Status this run |
|---|---|---|---|
| **NW-5** | TRG's numerator under R-1 | P-CHOP-1 re-score, **P-RAT-2**, P-VBT-1, F-9 | **landed live** — §2.5 |
| NW-2 | witness-correlation (defined only in v0.2; in no code) | I8, F-16, CEN-8 | blocks CEN-8 |
| NW-4 | sabotage fixture's defining parenthetical | F-10, CEN-8 | blocks CEN-8 |
| — | P-NEST-1 scored (v0.3:124) vs R-4 columns-only | CEN-8 | contradiction, unresolved |
| — | H-VBT | P-VBT-1 | **landed live** — §2.6 |

**The structural root remains unrepaired:** neither draft closed a register over its own `[VETO]`s.

---

## 6 · DISPOSITION (BOX-COST)

`cen5_campaigns.parquet` (6,834 rows, `sha 6925f06818a3`) · `cen5_corners.parquet` (36, `3f659c2e1ff4`) — both on `D:`. **Bus additions ≈ 0.16% of the box — under the 1% rule (F-14).** `exchange/` at **31.61%** (WARN, below the 40% refuse line). Nothing named census2a on `C:`.

Pointers: `D:\Naiad\research_outputs\census2a\cen5\`

---

## 7 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12j ===
NOW: CENSUS-2A run 6. CEN-5 ran to completion on 6,834 of 7,094 resolved campaigns. P-RAT-2 scored
NOT SUPPORTED (0 of 36 corners); P-VBT-1 NOT SCORED because H-VBT is undefined in both contract
drafts. CEN-7, CEN-8, CEN-9 remain.
LAST EVENT: 2026-08-12 — run 6: CEN-5 complete; two exit registrations resolved
FACTS:
- THE R UNIT RECONSTRUCTS: realized_r = size_r x gross_R + costs, verified on all 7,094 rows
  (median |err| 0.058 vs size_r x gross_R, residual systematically negative = costs). THEREFORE
  A3-DECILE's realized_r/size_r IS gross R, correlation 0.993 -- the operator's size-free ruling is
  correct and CEN-4 used it correctly. One ruler, not two [verified]
- 432 CAMPAIGNS WERE NEARLY LOST SILENTLY. tranche_id is unique only WITHIN a cell (c104t145 exists
  in both BTCUSDT_intraday and ETHUSDT_swing; 378 ids collide). A first draft keyed a dict on
  tranche_id alone and dropped 6.1% of the book. Now carried in a list that cannot collide. This is
  the THIRD appearance of the non-unique-key defect in this census -- a join-key uniqueness
  assertion belongs in the fixture set [verified]
- 260 campaigns excluded AND COUNTED: every one is sub-bar (hold_s < 300s), exiting inside the same
  5m candle it entered, so there is no forward path to ratchet along. Never imputed [verified]
- RIDE-ONLY control: the book is 12.3% winners (814 of 6,643) carrying mean +9.4R against a median
  loser of -1.04R; ALL median -1.0324, mean +0.3072. Any exit study on this book is a study of tail
  preservation [verified]
- P-RAT-2 NOT SUPPORTED: 0 of 36 corners meet both bars. FDR family m=36 DECLARED BEFORE SCORING,
  BH bar 0.00278; the I11 guard is ADMISSIBLE (p_sel 0.0005). TWO CAVEATS THAT MUST NOT BE READ
  PAST: (a) median delta R is +0.0000 for the best corners BY CONSTRUCTION, because most campaigns
  never reclaim the long EMA -- the mean deltas are +0.45R and +0.43R at the 4h/long/wide corners,
  and the registration names neither median nor mean; (b) TRG came back >1 for 30+ corners, because
  TRG is defined as a retention SHARE for a FILTER and a ratchet is an alternative EXIT that can
  exceed the ride. So P-RAT-2's TRG limb IS NOT DECIDABLE AS WRITTEN and the verdict rests on the
  delta limb alone [verified]
- NW-5 HAS NOW LANDED ON A LIVE VERDICT. TRG's numerator was defined (v0.2:64-65) while the ruler
  was MFE-MAE; R-1 retired that ruler and no text renamed the column. It gates P-RAT-2, P-VBT-1,
  P-CHOP-1's re-score and F-9 [verified]
- P-VBT-1 NOT SCORED: H-VBT is a bare NAME in both v0.2:131 and v0.3:103. The estate defines it
  only as "VWAP Band Target -- exits at confluence-scored VWAP levels", and those bands are CEN-7's
  registry output, which has not run. Choosing a band set by outcome is the sweep §N forbids, so
  the arm is not built and the registration is not scored rather than scored on an invented rule
  [verified]
PENDING:
1. NW-5 TRG numerator -- now blocking THREE registrations and one fixture. Highest-value word
2. P-RAT-2's "net terminal R": median or mean? The registration names neither and they disagree in
   sign at the 4h/long/wide corners
3. H-VBT's definition (band set + confluence cut), or drop P-VBT-1 to a printed column
4. NW-2 witness-correlation and NW-4 sabotage fixture both block CEN-8
5. P-NEST-1 scored-vs-columns-only contradiction must be resolved before CEN-8
6. RECOMMEND (repeat): close a [VETO] register over the whole contract, and add a join-key
   uniqueness assertion to the fixture set -- the same key defect has now appeared three times
NEXT: Operator rules on NW-5 and the median/mean question; then CEN-7 -> CEN-8 -> CEN-9.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (the run-6 sequencing paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 6 · CEN-5 complete; the exit arms answered, one of them unanswerable as written
