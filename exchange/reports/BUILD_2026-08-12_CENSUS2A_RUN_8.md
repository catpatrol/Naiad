# CENSUS-2A · RUN 8 — BUILD DOCUMENT · **THE CONTRACT IS SPENT**
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` — body `b0da051b…` + A1..A4 + register update → `sha256 5cd8ab57a1501607f43f6e60e2c702d2c0fe6fd85eef2e86187cb12f29189c2b`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (≤ 2024-07-01)

**Zero context assumed.**

---

## 0 · ALL TEN MODULES ARE RUN

| | |
|---|---|
| Hard assertions (20) + real F-PIN | **PASS** |
| Register update (ribbon operand) | **DONE** — §1 |
| **CEN-7 ANALYTICS SERIES** | **DONE** — §2 |
| **CEN-8 FRAME** | **DONE** — §3 |
| **CEN-9 SAMPLING-CLOCK CONTROL** | **DONE** — §4 |

`stages = [CEN-0b, CEN-1, CEN-2, CEN-3, CEN-6, CEN-4, CEN-5, CEN-7, CEN-8, CEN-9]` — **every module of CENSUS-2A has run. The contract is SPENT.**

**Fixture set at close:** F-GUARD · F-PIN · F-KEY · F-6 · F-6-VEC · F-PARITY-2 · **F-10** · **F-15** · **F-16** — all passing.

---

## 1 · REGISTER UPDATE

| # | Constant | Value | Source |
|---|---|---|---|
| 40 | ribbon operand | **OR over {30m, 1h} 9/89 spread < c×ATR** | reviewer-named, run 8 |

The register's last known-open entry is valued. **P-CHOP-1 remains WITHDRAWN this census** — it was scored on a 1h-only operand, and naming the operand afterwards does not revive a verdict computed before it.

---

## 2 · CEN-7 · ANALYTICS SERIES

Registry as-of **9,137** instants (1,357 event · 7,780 daily spine), read on the last **closed** bar — the same rule F-10 proves rejects a future bar. RVWAP families 7/30/90/365d **plus their ±1σ band edges** (a refusal against a band edge is as real as one against the mean). Dual-scored per I9; `assert_key` on every join.

### The two-limb reconciliation — D-B complete for the first time

| limb | level family | events | source |
|---|---|---:|---|
| i-a | EMA↔EMA (ratified kiss) | 175,696 | CEN-1 (run 1) |
| i-b | long EMAs {200,300,450,500} | 168,468 | CEN-1 (run 1) |
| **i-b** | **REGISTRY RVWAP 7/30/90/365d + σ-bands** | **14,759** | **CEN-7 (this run)** |
| | **i-b TOTAL** | **183,227** | |

The price↔level limb the estate never had — `seq8_extract.py:97-98` recorded the gap — is now complete against both long EMAs and registry levels.

**Co-location at the pinned 0.15×ATR: mean 0.137 of 12 levels within the band; only 0.7% of instants have ≥2.** Registry levels **rarely cluster** at armings on this tape. That is a finding about the confluence premise itself, and it is reported without a claim attached.

**Truncation watch (the run-2 m5 item): 0 rows flagged**, and the flag ships as a column regardless — never silent.

---

## 3 · CEN-8 · FRAME

### P-NEST-1 [45%] — scored per A4-NEST (text before result, F-8)

> *"Armings nested per the pre-named fallback set outperform un-nested on terminal return."* Pre-named set: {1h-in-4h, 30m-in-4h, 30m-in-1h}. **One comparison, not a sweep** — so A4-NEST's ruling stands and the selection guard's sweep logic does not apply.

| TREAT (nested) | CONTROL | cluster CI on terminal H100 | |
|---:|---:|---|---|
| 149 | 699 | **[−0.0513, +0.2292]**, point +0.1275 | **straddles 0** |

**A4-WITCORR beside the verdict:** pairwise sign-agreement **0.40** (only 2 of 5 asset pairs agree) against panel return correlation **0.6458**.

**VERDICT: NOT SUPPORTED.**

### P-i′ [50%] and P-iv′ [45%] — NOT SCORED

*"Leap-arrival"* vs *"stair-arrival"* is defined in **neither contract draft**. MC-1 defines a leap **family for CASCADES** (`BUILD_APOLLO_2026-08-06_MC1.md:448`); P-i′ is a **window** recut — a different object. The register carries it known-open. Inventing the split to score it would be the sweep §N forbids. P-iv′ depends on P-i′ and its ATR buckets are likewise undefined.

### Both time splits (R-SPLIT)

| split | cut | n early/late | days early/late | BTC share early/late |
|---|---|---|---|---|
| count-balanced | 2022-07-06 12:00 | 424 / 424 | **970.7 / 724.8** | 0.290 / 0.170 |
| **duration-balanced** | 2022-03-05 14:00 | 381 / 467 | **847.8 / 847.8** | 0.291 / 0.180 |

The duration split fixes the 246-day time imbalance run 2 found. **It does not fix the composition drift** — BTC is ~29% of the early half and ~18% of the late half under *both* splits. Era and panel composition remain entangled; R-SPLIT bought the first half of the fix, not the second.

### FDR families, declared

| family | m | BH bar |
|---|---:|---:|
| entry-lens registrations (P-ARM-1, P-iii-b, P-NEST-1) | 3 | 0.03333 |
| exit-lens registrations (P-RAT-2) | 1 | 0.10 |
| CEN-5 ratchet corners | 36 | 0.00278 |

**Withdrawn and not-scored registrations do NOT shrink m.** P-REL-1, P-CHOP-1, P-VBT-1, P-i′ and P-iv′ are excluded because they carry **no p-value**, not because they passed — a distinction that would otherwise inflate every surviving test.

---

## 4 · CEN-9 · SAMPLING-CLOCK CONTROL (registers nothing)

**14,871 control instants.** Same ruler (R-1 terminal ATR-return), same horizons, same toll lines. **F-15 re-draw reproducibility: PASS** on all tested assets — the N=200 quarter-stratified draw is identical under its seed.

| anchor | n | median terminal H100 | Δ vs EMA-anchored |
|---|---:|---:|---:|
| **EMA-anchored armings (CEN-2)** | **848** | **+0.0748** | — |
| prior-extreme sweep (low) | 892 | **+0.0845** | **+0.0097** |
| prior-day-L touch | 4,252 | +0.0560 | −0.0189 |
| prior-extreme sweep (high) | 1,482 | +0.0503 | −0.0245 |
| **random (quarter-stratified)** | **975** | **+0.0227** | **−0.0521** |
| prior-week-L touch | 1,289 | +0.0089 | −0.0659 |
| prior-day-H touch | 4,497 | +0.0000 | −0.0748 |
| prior-week-H touch | 1,484 | −0.0344 | −0.1093 |

**The EMA clock is not neutral, and it is not magic either.** Armings sit **+0.052 ATR** above stratified random instants — a real ordering. But the pinned toll line is **0.026–0.059 ATR per asset**, so *that entire edge is the same size as the round-trip cost*. And one non-EMA anchor — the prior-extreme sweep from below — **edges the EMA armings out** (+0.0845 vs +0.0748).

**Stated as the contract requires:** this module registers nothing, and these are **descriptive medians without intervals**. The ordering is real; its significance is unmeasured by design.

---

## 5 · THE CENSUS AT CLOSE — 14 REGISTRATION RECORDS

| registration | verdict |
|---|---|
| **P-REL-1b** | **SUPPORTED-PROVISIONAL** (label permanent) — witness-corr 0.60 / panel corr 0.6458 |
| P-ARM-1 | NOT SUPPORTED — confounded by exposure time |
| P-iii-b | NOT SUPPORTED — pooled measured; both-directions clause unmet by **0.0006** |
| P-RAT-2 | NOT SUPPORTED — 0/36 corners; **TRG limb VOID** (A4-TRG) |
| P-NEST-1 | NOT SUPPORTED — CI straddles; sign-agreement 0.40 |
| P-REL-1 | WITHDRAWN — unscoreable as written |
| P-CHOP-1 | WITHDRAWN — mis-specified component set |
| P-VBT-1 | NOT SCORED — H-VBT undefined |
| P-i′ · P-iv′ | NOT SCORED — leap/stair undefined |
| P-FAN-1 · P-ARM-2 · P-NEST-2 · P-RAT-3 · P-VBT-2 | filed next-cycle |

**One supported result out of nine scored hypotheses, and it is provisional with a correlation qualifier attached.** That is the census's honest yield, and the frame is what produced it: three registrations died to confounds the frame exposed (exposure time, mis-specified components, a mis-specified control arm), two died to definitions the contract never carried, and the one survivor is qualified by a print that had to be restored from a superseded draft.

---

## 6 · FINDINGS REPORTED, NOT FIXED

1. **Registry levels rarely co-locate** at armings (0.7% of instants with ≥2 within 0.15×ATR). The confluence premise is not supported by this tape's geometry.
2. **The EMA edge is toll-sized.** +0.052 ATR over random vs a 0.026–0.059 ATR toll.
3. **The prior-extreme sweep from below beats the EMA armings** on median terminal return. Descriptive, no interval, but it is the only anchor that does.
4. **Duration-balancing does not fix composition drift** — BTC ~29%/18% early/late under both splits.
5. **Two registrations died to undefined terms** (leap/stair, H-VBT) that were undefined in *both* drafts — pre-existing gaps, not compression losses.
6. **The register's closure is module-level only** (carried from run 7); a literal inside a function body would still slip through.

---

## 7 · DISPOSITION (BOX-COST)

**29 artifacts on `D:`, 53.3 MB.** New this run: `cen7_registry_series` (9,137) · `cen7_registry_refusals` (14,759) · `cen7_two_limb_reconciliation` (3) · `cen7_colocation` (9,137) · `cen8_fdr_families` (3) · `cen8_ledger_nested` (848) · `cen9_control_instants` (14,871) · `cen9_comparison` (7).

**Bus additions ≈ 0.30% of the 6,390,000 B box — under the 1% rule (F-14).** `exchange/` at **32.25%** (WARN, below the 40% refuse line). No results JSON in `exchange/`; nothing named census2a on `C:`.

Pointers: `D:\Naiad\research_outputs\census2a\{cen7,cen8,cen9}\` · `…\census2a_manifest.json`

---

## 8 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12l ===
NOW: CENSUS-2A IS COMPLETE. CEN-7, CEN-8 and CEN-9 all ran to completion this session. Every module
of the contract (CEN-0b, 1, 2, 3, 4, 5, 6, 7, 8, 9) is run and hash-recorded. THE CENSUS CONTRACT
IS SPENT.
LAST EVENT: 2026-08-12 — run 8: the final three stages; the contract closes
FACTS:
- ALL TEN MODULES RUN. Fixture set at close, all passing: F-GUARD, F-PIN, F-KEY, F-6, F-6-VEC,
  F-PARITY-2, F-10 (restored), F-15, F-16 (restored) [verified]
- CEN-7 COMPLETED THE D-B TWO-LIMB OBJECT for the first time: i-a 175,696 (EMA<->EMA), i-b 168,468
  (long EMAs) + 14,759 (registry RVWAP 7/30/90/365d and sigma bands) = 183,227 i-b total. The
  price<->level limb the estate never had is now complete against both families [verified]
- CO-LOCATION IS RARE: at the pinned 0.15x daily-ATR, a mean of 0.137 of 12 registry levels sit
  within the band, and only 0.7% of instants carry >=2. Registry levels do not cluster at armings
  on this tape -- a finding about the confluence premise itself [verified]
- P-NEST-1 NOT SUPPORTED: TREAT 149 vs CONTROL 699, terminal H100 cluster CI [-0.0513,+0.2292]
  straddles zero. A4-WITCORR beside it: pairwise sign-agreement 0.40 (2 of 5 pairs) against panel
  return correlation 0.6458 [verified]
- P-i' AND P-iv' NOT SCORED: leap-arrival vs stair-arrival is defined in NEITHER draft. MC-1's leap
  family is a CASCADE object; P-i' is a WINDOW recut. Register: known-open. Inventing the split to
  score it is the sweep §N forbids [verified]
- BOTH TIME SPLITS PRINTED (R-SPLIT): count-balanced gives 970.7/724.8 days; duration-balanced gives
  847.8/847.8. The duration split fixes the TIME imbalance and NOT the composition drift -- BTC is
  ~29% of the early half and ~18% of the late half under BOTH. Era and panel composition remain
  entangled [verified]
- FDR FAMILIES DECLARED: entry-lens m=3 (BH 0.03333), exit-lens m=1 (0.10), CEN-5 corners m=36
  (0.00278). WITHDRAWN and NOT-SCORED registrations do NOT shrink m -- they carry no p-value, which
  is not the same as passing [verified]
- CEN-9, THE INSTRUMENT'S OWN CONTROL: EMA-anchored armings median terminal H100 +0.0748 against
  stratified random instants +0.0227 -- an edge of +0.052 ATR. THE PINNED TOLL IS 0.026-0.059 ATR
  PER ASSET, so the entire EMA edge is the size of the round-trip cost. And the prior-extreme sweep
  from below EDGES IT OUT at +0.0845. Descriptive medians, no intervals, registers nothing -- by
  design [verified]
- F-15 PASS: the N=200 quarter-stratified draw reproduces identically under its seed [verified]
- THE CENSUS YIELD: one SUPPORTED-PROVISIONAL result (P-REL-1b, itself qualified by a
  witness-correlation print that had to be restored from a superseded draft) out of nine scored
  hypotheses. Three died to confounds the frame exposed; two to definitions the contract never
  carried. That is the honest yield and the frame is what produced it [verified]
PENDING (all next-cycle; none blocks this contract, which is spent):
1. Filed and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%], P-VBT-2 [45%],
   and P-CHOP-2 on the newly-valued ribbon operand
2. Needs-word before their registrations can ever be scored: leap/stair arrival (P-i'), ATR buckets
   and "survives" (P-iv'), H-VBT's band rule (P-VBT-2)
3. The register's closure is MODULE-LEVEL only; an AST scan of scoring paths for bare literals is
   the natural next hardening and is NOT implemented
4. The D:-moved incident remains routed to ATHENA; cause unidentified
5. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; the funnel opens NOW, at census close
NEXT: THE PATH's next step is the operator's -- Tier-C / EngineV2, or the rotation funnel. The
census has delivered what it can. Owner: operator.
METRICS: operator actions this session = 1 (the run-8 sequencing paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 8 · **the contract is spent; one provisional result, honestly qualified**
