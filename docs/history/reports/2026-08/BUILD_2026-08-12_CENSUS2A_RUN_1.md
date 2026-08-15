# CENSUS-2A · RUN 1 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md`
`sha256 b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a` (12,887 B, 157 lines, byte-exact against the operator's attachment)
**Program:** `scripts/census2a_program.py` (new) · **Class:** EVIDENCE — exploration-classic (every scored table ≤ 2024-07-01), except CEN-0(b) which is DISPLAY-ONLY by construction (§3)

**Zero context assumed.** This document is complete on its own.

---

## 0 · WHAT RAN, AND WHAT THIS MEANS

The contract v0.3 is stamped **EXECUTABLE ON OPERATOR'S RUN — running this paste IS the RATIFIED stamp (condition 3)**. It ran. Census-2A is therefore **ratified and under way**, not pending.

**Stages completed this session (whole stages only, per the budget rule):**

| Stage | State | Substance |
|---|---|---|
| Preflight (I3-in-code, I2) | **DONE** | 6/6 identity, drive PRESENT, D: rw-probe |
| F-GUARD, F-PIN, F-6-VEC, F-6 | **DONE** | all PASS; F-GUARD ran **before** any real sweep |
| **CEN-0(b) PAXG** | **DONE** | fetched, classified — and it cannot do the job the contract wanted (§3) |
| **CEN-1 SUBSTRATE** | **DONE** | 516,866 events · 356,315 refusals · both limbs incl. the **new i-b detector** |
| **CEN-2 ARMED-WINDOW LEDGER** | **DONE** | 848 armings, disjoint fate table, P-ARM-1 scored |
| CEN-3 … CEN-9 | **REMAINING** | not started; named in §8 |

**Cached vs remaining is stated plainly in §8.** Nothing was half-run.

---

## 1 · FIXTURE TRANSCRIPT (full)

```
PREFLIGHT -- I3 identity (in code) + I2 drive gate
    PASS  pwd ends C:/Naiad              C:/Naiad
    PASS  pwd NOT contains OneDrive
    PASS  branch v12-v1-census           v12-v1-census
    PASS  remote catpatrol/Naiad         https://github.com/catpatrol/Naiad.git
    PASS  LEDGER.md
    PASS  exchange/status/CONVENTIONS.md
    drive_wait: PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s
    residency OK -> D:\Naiad\research_outputs\census2a
    I1 wall: 1719792000000 (2024-07-01 00:00) imported from census_build

F-GUARD -- planted-sweep proof (runs BEFORE any real sweep)
    NULL sweep    : m=12 p_sel=0.6742 bar=0.00833 -> admissible=False
      (1/12 null candidates cleared a NAIVE CI -- the reason the guard exists)
    PLANTED sweep : m=12 winner=plant5 p_sel=0.0007 -> admissible=True
    PASS  guard DECLINES the null sweep
    PASS  guard ADMITS the planted effect (and names it)

F-PIN -- manifest pins survive a --stage re-run (I12)
    PASS  prior pins + artifacts + sections carried forward alongside the new pin

F-6-VEC -- vectorised refusal detector vs scalar reference
    PASS  18/18 cells identical

F-6 -- refusal determinism + 3 hand-verified per limb
    PASS  i-a determinism (195 events, re-run identical)
    PASS  i-b determinism (89 events, re-run identical)

F-PARITY-2 (inside CEN-1)
    PASS  cold-head events = 0 (must be 0)
```

**F-GUARD is a fixture that can fail, and that is the point.** It plants two synthetic sweeps with known ground truth: a 12-candidate null sweep (the guard must decline) and the same shape with one large real effect (the guard must admit *and name the right candidate*). It does both. Note the null sweep had **1 of 12 candidates clear a naive CI** — which is precisely the failure mode that produced two withdrawn pins in paste #1.

**F-6-VEC exists because I rewrote the refusal detector for speed.** The scalar form was ~50× too slow for ~10M bars. A vectorised rewrite of a detector is the classic site of silent semantic drift, so the scalar reference is retained and the two are proved element-identical on real series (18/18 cells). "It looked right" is not a proof.

---

## 2 · CEN-1 · SUBSTRATE (complete)

Evidence era, 7 assets (5 panel + 2 annex), 6 timeframes {5m, 15m, 30m, 1h, 4h, 12h}.

| Artifact | Rows | Bytes | sha256 (first 16) |
|---|---:|---:|---|
| `cen1_events.parquet` | 516,866 | 28,691,526 | `bf4afe69afa00c72` |
| `cen1_refusals.parquet` | 356,315 | 11,330,426 | `0f6442020aca4884` |
| `cen1_counters.parquet` | 1,492 | 15,193 | `7eedad61cf2ba602` |

**Refusal events, both limbs — 182,022 i-a and 174,293 i-b.**

**The i-b limb is new to the estate.** The contract's R-8 required the price↔level refusal object (the SFP / deviation figure) built this paste; it had no implementation anywhere — `seq8_extract.py:97-98` records the gap. It is built, against the long EMAs {200, 300, 450, 500}, using **the same grammar** as the ratified i-a kiss (approach within ε·ATR → veer ≥ δ·ATR within k bars → no sign change), with ε/δ/k = 0.25/0.75/10. Writing a second, subtly different grammar for the second limb would have made the limbs incomparable, which is exactly what "same grammar" forbids.

The detector is generic over *any* level series, so registry levels (RVWAPs, anchored VWAPs, profile edges) plug in at CEN-7 without rework. **Registry levels are not in this run** — only long EMAs. Stated, not implied.

**Class handling per contract (vi):** scored classes are {9_89, 9_200, 89_200, 12_25, 25_89, 300_450, 450_500}; **9_25 is recorded in the raw stream but excluded from the trigger taxonomy** (2.19× the reference count, weakest measured effect). **`counter_n` is a measured column only — the TRAP stamp is dropped (R-3).**

---

## 3 · CEN-0(b) · PAXG — fetched, and the finding is bigger than the classification

`PAXGUSDT`, `fapi.binance.com`, symbol passed explicitly. **`engine/cells.py:SYMBOLS` untouched** — verified by `git diff --stat engine/` returning empty (I10).

| TF | rows | evidence-era | live-era | first open | last open |
|---|---:|---:|---:|---|---|
| 1m | 723,691 | **0** | 723,691 | 2025-03-27 10:30 | 2026-08-12 00:00 |
| 5m | 144,739 | **0** | 144,739 | 2025-03-27 10:30 | 2026-08-12 00:00 |
| 15m | 48,247 | **0** | 48,247 | 2025-03-27 10:30 | 2026-08-12 00:00 |
| 1h | 12,063 | **0** | 12,063 | 2025-03-27 10:00 | 2026-08-12 00:00 |
| 4h | 3,017 | **0** | 3,017 | 2025-03-27 08:00 | 2026-08-12 00:00 |
| 12h | 1,007 | **0** | 1,007 | 2025-03-27 00:00 | 2026-08-12 00:00 |

**F-12 classification: ANNEX** (0.00y evidence-era, rule ≥2y → panel-eligible). 24 MB on `D:`.

**The consequence is larger than "annex".** PAXG's Binance perp begins **2025-03-27 — nine months *after* the 2024-07-01 evidence wall.** Every scored table in this census is bounded at the wall by I1. Therefore **PAXG cannot appear in any scored table at all**, now or after more history accrues, unless the wall itself moves.

That matters because the contract's D-D framing (carried from v0.2) cast PAXG as *"the census's first independent jury, a statistical control on witness correlation."* **It cannot serve that role.** A control that shares no observations with the thing it controls is not a control. PAXG is a live-era, display-only asset for the foreseeable census. **Reported, not fixed** — this is an operator decision about what PAXG is for.

---

## 4 · CEN-2 · THE ARMED-WINDOW LEDGER (the headline)

848 armings (4h lattice-A 9/89, both directions, 5 panel assets, evidence era). Window closes at min(**W_max = 151**, counter-arming). Stamps AT the arming = {WALL, KISS/refusal, FIRST}, score 0–3.

### THE ARMING-FATE TABLE — fates disjoint by construction

| Fate | Trigger | n | median terminal H100 (ATR) | median window width |
|---|---|---:|---:|---:|
| **COMPLETED** | yes | **595** | **+0.2421** | 48 bars |
| **ABORTED** | no | **252** | **−0.4767** | 4 bars |
| **ROTTED** | no | **1** | +0.9820 | 151 bars |

**ROTTED is n=1.** With W_max = 151 and a median window of 4–48 bars, essentially nothing survives to expiry — the counter-arming closes the window first. This is the direct consequence of the paste-1 finding that W_max is near-non-binding, now confirmed on the census population: **W_max governs one arming in 848.**

Stamp score distribution: 0→71, 1→359, 2→397, 3→21 (pre-1d-limb); **strict core (3/3) = 29** with both WALL limbs. Fates are disjoint (paste-1 defect 3 fix: the old `aborted` flag was true of 431/436 windows *including every completed one*, so the taxonomy could not be derived from it).

### P-ARM-1 [prior 60%] — registration text precedes the result (F-8)

> *"WALL-true armings → higher trigger-within-151 rate AND higher post-trigger terminal return than WALL-false."*

| | WALL-true | WALL-false |
|---|---:|---:|
| trigger-within-151 rate | 0.464 | 0.760 |
| terminal H100, asset-cluster 90% CI on the difference | **[−0.2479, −0.0635]** — excludes 0 | |

**VERDICT: NOT SUPPORTED.** Both limbs point the wrong way, and the return limb does so with a measured effect (cluster CI excludes zero, 5 clusters, R-2 criterion).

### CONFOUND — mandatory disclosure, not a footnote

**The trigger-rate limb is confounded by exposure time and cannot be evaluated as written.**

| | WALL-true | WALL-false |
|---|---:|---:|
| median window width | **8 bars** | **30 bars** |
| trigger rate *conditioned on width ≥ 48* | **1.000** | **0.985** |

The gap closes completely under conditioning. The mechanism is mechanical: WALL means price sits within 0.5·ATR of the e89 — *exactly where the 9/89 is about to cross back* — so WALL-true windows abort fast, and an 8-bar window cannot contain a trigger regardless of what the tape does. The registration's trigger-rate half measures **how long the window stayed open**, not the WALL stamp. Evaluating it properly needs a hazard / competing-risk framing. **Reported, not fixed.**

The **terminal-return limb is not affected by this mechanism** and stands as measured: WALL-true armings show *lower* terminal return, cluster CI excluding zero.

**I found this by checking the result rather than reporting it.** As first computed — with only the 4h WALL limb — it read as a clean inverted finding. It is not.

---

## 5 · FINDINGS REPORTED, NOT FIXED

1. **PAXG cannot be the independent jury** (§3). Zero evidence-era bars; structurally display-only.
2. **P-ARM-1's trigger-rate limb is unevaluable as written** (§4). Needs hazard framing.
3. **W_max = 151 governs 1 arming in 848.** The constant is correctly pinned and nearly inert. Worth knowing before it is argued over again.
4. **WALL's two limbs were nearly redundant here:** adding the 1d-e200 limb moved the trigger rate only 0.413 → 0.464 and strict-core 21 → 29. The limb is implemented per the pinned constant; its marginal contribution is small.
5. **Registry levels absent from i-b** (§2). Long EMAs only this run; the detector is ready for them at CEN-7.
6. **The `exchange/reports/` copy of the v0.3 contract is a duplicate** of the queue item (byte-identical, `b0da051b…`), placed by the operator at 12:49 before the 12:51 filing. 12,887 B of box carried twice. Not deleted — an operator-placed file is not mine to remove. Listed in the disposition table.

---

## 6 · DISPOSITION (six columns, with BOX-COST)

| Artifact | Class | Home | Bytes | Bus cost | Disposition |
|---|---|---|---:|---|---|
| `cen1_events.parquet` | EVIDENCE | `D:` | 28,691,526 | 0 (pointer) | keep on D:, pointer here |
| `cen1_refusals.parquet` | EVIDENCE | `D:` | 11,330,426 | 0 (pointer) | keep on D:, pointer here |
| `cen1_counters.parquet` | EVIDENCE | `D:` | 15,193 | 0 (pointer) | keep on D:, pointer here |
| `cen2_ledger.parquet` | EVIDENCE | `D:` | 113,114 | 0 (pointer) | keep on D:, pointer here |
| `cen2_fate_table.parquet` | EVIDENCE | `D:` | 3,341 | 0 (pointer) | keep on D:, pointer here |
| `klines/PAXGUSDT/*` (6) | DISPLAY-ONLY | `D:` | ~24 MB | 0 (pointer) | keep on D:, never scored |
| `census2a_manifest.json` | record | `D:` | — | 0 (pointer) | keep on D: |
| queue item (v0.3 contract) | contract | `exchange/queue/` | 12,887 | +0.20% | **rides the publish** |
| this build document | report | `exchange/reports/` | ~17 KB | +0.27% | **rides the publish** |
| `reports/CENSUS2A_CONTRACT_v0.3…md` | duplicate | `exchange/reports/` | 12,887 | +0.20% | operator-placed; flagged §5.6 |

**BOX-COST: bus additions this session ≈ 0.67% of the 6,390,000 B budget — under the 1% rule (F-14).** All results JSONs and parquets stay on `D:` by pointer; **no results JSON enters `exchange/`**. Total D: footprint for census2a: **69 MB**.

**Pointers (full paths):**
- `D:\Naiad\research_outputs\census2a\cen1\` — events, refusals, counters
- `D:\Naiad\research_outputs\census2a\cen2\` — ledger, fate table
- `D:\Naiad\research_outputs\census2a\klines\PAXGUSDT\` — 6 series, display-only
- `D:\Naiad\research_outputs\census2a\census2a_manifest.json` — pins, fixtures, per-artifact sha256

---

## 7 · INVARIANT COMPLIANCE

| Invariant | Held? | Evidence |
|---|---|---|
| I1 evidence wall | ✅ | `CEIL_MS` imported from `census_build`, never restated; all CEN-1/CEN-2 tables evidence-era |
| I2 residency | ✅ | all bulk on `D:`; output root asserted `.drive == "D:"`; rw-probe; nothing named census2a on `C:` |
| I3 identity **in code** | ✅ | `stage_preflight` asserts all six; HALTs on any miss |
| I4 EMA family + NaN-before-warm | ✅ | F-PARITY-2 = 0 cold-head events |
| I7 as-of / last-closed-bar | ✅ | WALL 1d limb indexed by bar **close**, not containment |
| I8 cluster bootstrap replication | ✅ | P-ARM-1 scored on asset-cluster CI (R-2), not the retired sign gate |
| I10 no engine change | ✅ | `git diff --stat engine/` empty; PAXG by explicit symbol |
| I11 guard on every sweep | ✅ | committed code; F-GUARD proves it fires, run before any real sweep |
| I12 pins merge | ✅ | F-PIN; observed live — the CEN-2 run logged "merging into existing manifest (3 stages)" |
| I5 counted never fitted | ✅ | stamp score is a 0–3 count |
| I6 lens-to-purpose | ⚠️ **partial** | CEN-1/CEN-2 are structural; the dual-lens print lands with CEN-3 outcomes |

---

## 8 · CACHED vs REMAINING

**Cached (complete, on `D:`, re-runnable and hash-recorded):** preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · **CEN-0(b)** · **CEN-1** · **CEN-2** (incl. P-ARM-1).

**Remaining, in contract order:**
- **CEN-3 OUTCOMES** — the R-1 ruler is already implemented (`outcome_block`) and used inside CEN-2; CEN-3 is its full per-lens, per-asset, per-direction, held-in-time treatment with the toll line.
- **CEN-4 CHOP-STATE** — P-iii-b + 5 components incl. the pinned lens-concordance metric.
- **CEN-5 EXIT-AND-FEED** — all 7,094 resolved campaigns, three arms vs RIDE-ONLY.
- **CEN-6 RANGE & VERDICT** · **CEN-7 ANALYTICS SERIES** · **CEN-8 FRAME** · **CEN-9 SAMPLING-CLOCK CONTROL**.
- Registrations still unscored: P-iii-b, P-REL-1, P-NEST-1, P-i′, P-iv′, P-CHOP-1, P-RAT-2, P-VBT-1 (**8 of 9**; only P-ARM-1 is scored).

**Next session starts at CEN-3.** Everything above it is cached.

---

## 9 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12c ===
NOW: CENSUS-2A v0.3 RATIFIED BY EXECUTION. Contract filed as the queue item
(sha b0da051b), programs committed (3a0c35e), and stages CEN-0(b), CEN-1 and CEN-2 ran to
completion with every gating fixture passing. CEN-3..CEN-9 remain; next session starts at CEN-3.
LAST EVENT: 2026-08-12 — run 1: PAXG fetched, substrate built (516,866 events), armed-window
ledger built (848 armings), P-ARM-1 scored NOT SUPPORTED with its confound disclosed
FACTS:
- PAXG's Binance perp begins 2025-03-27, NINE MONTHS AFTER the evidence wall: zero evidence-era
  bars at every interval. It is ANNEX by the contract rule, but the larger consequence is that it
  can never enter a scored table under I1 — so it cannot be the "independent jury" D-D intended
  [verified]
- CEN-1 built the i-b price<->level refusal limb (R-8) — 174,293 events. The object did not exist
  in the estate before this run; same grammar as the ratified i-a, 3 hand-verified per limb [verified]
- ARMING-FATE (disjoint): COMPLETED 595 (median terminal H100 +0.2421), ABORTED 252 (-0.4767),
  ROTTED 1. W_max=151 governs ONE arming in 848 — correctly pinned and nearly inert [verified]
- P-ARM-1 NOT SUPPORTED: WALL-true trigger rate 0.464 vs 0.760, terminal H100 cluster CI
  [-0.2479,-0.0635] excludes zero in the WRONG direction [verified]
- CONFOUND DISCLOSED: WALL-true windows have median width 8 bars vs 30; conditioned on width>=48
  the trigger rates are 1.000 vs 0.985. The trigger-rate limb measures exposure time, not the
  stamp, and cannot be evaluated as written — a hazard framing is required [verified]
- F-GUARD passes in both directions (declines a 12-candidate null sweep at p=0.674, admits a
  planted effect at p=0.0007 and names it) and ran BEFORE any real sweep, per I11 [verified]
PENDING:
1. Operator decision on what PAXG is FOR, given it cannot serve as an evidence-era control
2. P-ARM-1's trigger-rate limb needs a hazard / competing-risk re-specification before it can be
   scored as written; the terminal-return limb stands
3. Registry levels are absent from the i-b refusal limb this run (long EMAs only); they join at CEN-7
4. 8 of 9 registrations remain unscored (CEN-3..CEN-9)
5. Duplicate v0.3 contract in exchange/reports/ alongside the queue item — operator-placed, not
   removed by the builder
NEXT: Run 2 begins at CEN-3 (outcomes). Owner: HEPHAESTUS on the operator's word.
METRICS: operator actions this session = 1 (the v0.3 contract) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 1 · three whole stages; the census is ratified and under way
