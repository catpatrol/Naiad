# CENSUS-2A · RUN 3 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract (single source):** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md`
 · ratified body `sha256 b0da051b894fc8586fab466fcf99cb0390763551d0d67bbac83743abc1547a6a` (unchanged)
 · **+ AMENDMENT A1** appended this session → file `sha256 0b87f7a33eb4e9cf57081098cf3ed5e050f0df033a6b040ae1a8a564d271c716`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (all scored tables ≤ 2024-07-01)

**Zero context assumed.** This document is complete on its own.

---

## 0 · WHAT RAN, AND WHERE IT STOPPED

Run 3 opened with an **infrastructure HALT**, executed the rulings block, re-ran the affected stages, scored the re-registered hypothesis, and then **stopped at a named blocker** — not at budget.

| | State |
|---|---|
| **Estate restore** (D: was displaced) | **DONE** — §1 |
| Hard assertions (17) + real F-PIN on the live manifest | **PASS** — §2 |
| **Amendment A1** written to the queue item + manifest | **DONE** — §3 |
| **PX-1(b)** PAXG DROP | **DONE** — 23,636,729 B freed |
| **A1-FAN** enacted (2 classes + FAN/KNOT columns) | **DONE** — CEN-1 re-run, §4 |
| **R-F11** annex-pooling slip fixed | **DONE** — §5 |
| **P-REL-1b** scored | **DONE** — **SUPPORTED-PROVISIONAL**, §6 |
| **CEN-6** | **BLOCKED** — an unnamed `[VETO]`, §7 |
| CEN-4 · CEN-5 · CEN-7 · CEN-8 · CEN-9 | **REMAINING** — §9 |

---

## 1 · THE SESSION OPENED ON A HALT: `D:\Naiad` HAD MOVED

The drive gate failed: `UNREACHABLE root=D:/Naiad attempts=6 elapsed=18.01s`. `D:` itself was mounted and healthy (LaCie Rugged USB-C, Online, 102.6 GB used) — **`D:\Naiad` had been moved to `D:\Archive\Naiad`** after the run-2 write at 17:16 UTC.

**The PIN CHECK's downstream failures were the missing drive, not lost data.** They read "P-ARM-1 present: FAIL" — because the manifest file lives on `D:`. That is precisely the conflation `drive_wait.py` exists to prevent (*"a single failed lookup measures that lookup, not absence"*), and it is why the correct response was to diagnose rather than announce data loss.

**Not the repo's doing.** `daily_routine.py` sweeps flat files only, explicitly skips directories, never references `D:/Naiad`, and last ran at 07:00 — hours before the census2a writes.

**Restored on the operator's word** (option (a)): `Move-Item D:\Archive\Naiad D:\Naiad` — a same-volume rename. **123 files / 5,229,264,513 bytes, verified identical before and after.**

**Deliberately not done under uncertainty:** PX-1(b)'s deletion was withheld while the estate was displaced. `D:\Naid-GDRIVE\...\census2a` → `False`, so the archived tree held the **only** copy of run 1–2 output. Deleting from a directory named *Archive*, for reasons unknown, was the one action least defensible at that moment. It was executed only after the restore (§3).

---

## 2 · FIXTURE TRANSCRIPT (post-restore)

```
=== HARD ASSERTIONS (re-run after the move) ===
  PASS  remote contains catpatrol/Naiad
  PASS  pwd ends C:/Naiad                     PASS  pwd NOT OneDrive
  PASS  branch v12-v1-census
  PASS  test -f exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md
  PASS  test -f scripts/census2a_program.py   PASS  test -f scripts/drive_wait.py
  PASS  DRIVE GATE PRESENT|WOKE   PRESENT root=D:/Naiad attempts=1 elapsed=0.00s budget=18.0s

=== PIN CHECK (real F-PIN: load_manifest on the LIVE manifest) ===
  PASS  live manifest exists
  PASS  section present: pins / artifacts / fixtures / stages / registrations
  PASS  P-ARM-1 present          PASS  P-ARM-1 confound text intact
  PASS  P-REL-1 present          PASS  P-REL-1 WITHDRAWN marker intact

=== per-stage gating (I11: guard BEFORE any sweep) ===
F-GUARD  NULL m=12 p_sel=0.6742 bar=0.00833 -> declines   PASS
         PLANTED m=12 winner=plant5 p_sel=0.0007 -> admits PASS
F-PIN    7 sections + coexistence                          PASS
F-6-VEC  vectorised refusal detector == scalar reference    PASS 18/18
F-6      i-a / i-b determinism + 3 hand-verified per limb   PASS
F-PARITY-2  cold-head events = 0                            PASS
```

**F-PIN is now a fixture that can fail.** It calls `load_manifest` on a real seeded manifest and asserts section-by-section survival; against run 2's code it would fail on `registrations`.

---

## 3 · AMENDMENT A1 + PX-1(b)

**A1 appended verbatim** to the queue item. The ratified body is **byte-identical up to the rule** (`after[:len(before)] == before` → True), 0 CR bytes. A1 amends **by name only**: it adds observation columns and two cross classes, fixes a pooling slip, adds a second split, re-registers a withdrawn hypothesis under a permanent label, sequences the stages, and disposes of an asset. **No pinned `[VETO]` constant is re-pinned and no scored definition in the v0.3 body is altered.**

**PX-1(b) — PAXG DROPPED:**

| file | bytes |
|---|---:|
| PAXGUSDT_1m | 16,567,078 |
| PAXGUSDT_5m | 4,634,808 |
| PAXGUSDT_15m | 1,791,678 |
| PAXGUSDT_1h | 476,642 |
| PAXGUSDT_4h | 122,841 |
| PAXGUSDT_12h | 43,682 |
| **FREED** | **23,636,729 B (23.6 MB)** |

The now-empty `klines/` parent was removed. Re-fetchable via `python scripts/census2a_program.py --stage cen0b` (explicit-symbol path; `engine/cells.py:SYMBOLS` untouched). Marked DROPPED in the manifest.

---

## 4 · A1-FAN ENACTED (columns only — nothing scored on them)

CEN-1 re-run: **529,061 events** (was 516,866; **+12,195** from the two new classes). Refusals unchanged at 356,315 (i-a 182,022 · i-b 174,293) — correct, since refusals do not depend on cross classes. **F-PARITY-2 = 0 cold-head events.**

| new class | events |
|---|---:|
| `200_500` | 6,715 |
| `300_500` | 5,480 |

| column | value |
|---|---|
| **FAN** true | 202,916 — **38.35%** of events (up 104,688 / down 98,228, near-symmetric) |
| **KNOT** true | 13,915 — **2.63%** |
| FAN **and** KNOT | **710** |
| `knot_spread_atr` | p10 1.057 · p50 3.567 · p90 8.784 |

**A reading I am flagging, not burying.** A1-FAN names KNOT's five EMAs explicitly (`{89,200,300,450,500}`) but says only *"six-EMA"* for FAN. I took the six as **`{9, 89, 200, 300, 450, 500}`** — KNOT's five plus the fast line, the only six-member set the ruling's own vocabulary supplies. **That is a reading, not a quotation.** Correct it by name if a different six was meant; `FAN_EMAS` is a single constant.

**And a correction to my own commentary:** the run log prints "*a fanned stack cannot also be knotted*". **710 events are both.** A stack can be monotone *and* tight. The data is right; the parenthetical was wrong.

---

## 5 · R-F11 — THE ANNEX-POOLING SLIP, FIXED

Run 2 printed a lattice-A cascade stream of **151,718** events. That figure pooled **JTOUSDT (3,812) + TAOUSDT (1,348)** into a panel-labelled total, against F-11's *"annex printed never pooled"*.

| | run 2 (pooled) | run 3 (R-F11) |
|---|---:|---:|
| lattice-A stream, **panel only** | 151,718 | **146,558** |
| annex, reported separately | — | **5,160** |

Cascades are built per `(asset, class)`, so **no panel arming's depth moved** — the defect was in the printed count, not the computation. The annex figure is now printed beside, never added.

---

## 6 · P-REL-1b — SCORED (text before result, F-8)

> **P-REL-1b [prior 50%, POST-HOC-INFORMED — LABEL PERMANENT]**
> *"Among windows with ≥1 in-window trigger: TREAT `has_in_window_12_25=true` vs CONTROL triggered without any in-window 12_25; anchor = FIRST in-window trigger of ANY class, identical rule both arms."*
> Ceiling this run = **SUPPORTED-PROVISIONAL**; only next-cycle replication can lift it.

**Arms are now explicit predicates, not a first-mover label.** That distinction is the whole reason P-REL-1 was withdrawn:

| | n |
|---|---:|
| TREAT — any in-window 12_25 | **301** |
| CONTROL — triggered, no 12_25 | **294** |
| *first-mover label `12_25`* | *155* |
| *…misfiled into run-2's control arm* | ***146*** |

`301 = 155 + 146` — the run-2 control arm was 33% contaminated with windows that did contain a 12_25.

### Result, with every mandated split

| Split | point | 90% cluster CI | |
|---|---:|---|---|
| **H100 (primary)** | **+0.1869** | **[+0.0638, +0.2887]** | **EXCL-0** |
| H20 | — | *infeasible on 4h — NaN, not substituted* | n/a |
| H500 | +0.6399 | [+0.4856, +0.8669] | **EXCL-0** |
| direction up | +0.1437 | [+0.0369, +0.4098] | **EXCL-0** |
| direction down | +0.2382 | [+0.1070, +0.2993] | **EXCL-0** |
| half early | +0.1515 | [−0.0285, +0.2737] | straddles |
| half late | +0.2211 | [+0.1256, +0.4895] | **EXCL-0** |

Per-asset deltas: BTC +0.2042 · ETH **−0.0923** · NEAR +0.4675 · SOL +0.3666 · ZEC +0.2254. **LOAO: 4 of 5** refits still exclude zero.

**VERDICT: SUPPORTED-PROVISIONAL.** *(Label permanent: the prior was informed by run 2's post-hoc look.)*

**Specifying the arms correctly did not merely fix a label — it produced a materially stronger result** than the mis-specified predecessor:

| | P-REL-1 (withdrawn) | **P-REL-1b** |
|---|---|---|
| H500 | −0.083 **straddles** | **+0.640 EXCL-0** |
| per-direction | not computed | **both EXCL-0** |
| LOAO excluding 0 | **1 / 5** | **4 / 5** |
| ETH reversal | −0.2418 | −0.0923 |

Only `half_early` straddles. **This is the census's first registration to survive its own mandated splits.**

---

## 7 · CEN-6 IS BLOCKED — v0.3's COMPRESSION DELETED THE TEST

R-ORDER resolved the CEN-4/CEN-6 ordering. **CEN-6 itself is blocked, on a different and previously unnoticed defect.**

| | text |
|---|---|
| **v0.2:135** | *"Acceptance head-to-head {1H, 4H, 12H} **(close beyond + hold h bars [VETO] vs deviation-reclaim)**; trap-rate per close-set member; hysteresis prior."* |
| **v0.3:104** (ratified) | *"Acceptance head-to-head {1H,4H,12H}; deviation-reclaim branch; trap-rate per member; hysteresis prior…"* |

**The compression from v0.2 to v0.3 kept the noun phrases and deleted the parenthetical that defines the test.** `grep` confirms: the string `h bars [VETO]` exists **only** in the superseded v0.2. The `[VETO]` constant `h` — the hold length that decides whether a close beyond a boundary is an acceptance — **appears nowhere in the ratified body and was never given a value.**

**Why I will not proceed anyway.** Sweeping `h ∈ {1,2,3}` and promoting a winner would be *selecting a `[VETO]` constant by search*. §N forbids it outright: *"no re-pinning of constants mid-run (a change is a new [VETO]-named amendment)"*. Choosing `h` is exactly the operator's reserved act.

**And it cascades:** CEN-6 → CEN-4's fifth composite component `verdict-open` → CEN-5(b)'s `v0 band`.

### What is ready the moment `h` is named

**REUSE (verified to exist):** `engine/s2.py:353-395` D4 sweep-reclaim with grid `D4_GRID` at `:43` (the deviation-reclaim branch is already committed code) · `engine/s2.py:275-297` D1 range-compression envelope · `analytics/structure.py:225-231` `confirmed_pivots(values, as_of_index, 5, 5)` and `:269+` `prior_period_extremes(..., 'D'|'W')`, both **causal by construction** · `census_build.py:401-405` the hold-beyond primitive, already vectorised and F-CFG-pinned · `mc1_program.py:1755-1762` TEST/RECLAIM/CONTINUATION with the contract's own pinned cushion grid.

**BUILD:** a queryable range-object table (Dionysus's G-RD1 is still open — `NOTE_DIONYSUS_to_APOLLO_2026-08-04_range_detection_scoping.md:29`); the acceptance verdict state machine (no `RESPECTED`/`DISRESPECTED` exists in any `.py`); trap-rate in the CEN-6 sense (**do not reuse the `TRAP` identifier** — MC-1's is counter-cross density, a different object, dropped by R-3); hysteresis.

### MANDATORY DISCLOSURE before CEN-6 runs

`LEDGER.md:311` — **P-PD1 [60%] FALSIFIED · P-PD2 [60%] FALSIFIED · P-PD4 [60%] FALSIFIED — "the pattern detectors as gridded do not graduate."** Reusing D1/D3/D4 as a **location object** is legitimate; reusing them as a promoted signal re-runs a falsified test. The counterweight that survived is the one CEN-4 actually wants: `LEDGER.md:315` — **P-PD3 [55%] CONFIRMED, "Z2's deficit concentrates in-range (−0.33R)"**.

---

## 8 · FINDINGS REPORTED, NOT FIXED

1. **`D:\Naiad` was moved by something outside the repo** (§1). It will recur unless the cause is identified; the census cannot survive its residency root vanishing mid-run.
2. **v0.3's compression dropped a test definition and a `[VETO]` constant** (§7). Worth auditing the other v0.2→v0.3 compressions for the same loss — CEN-6 was found only because it was reached.
3. **`half_early` straddles zero for P-REL-1b** (§6). The effect is carried by the late half.
4. **ETH remains the reversed asset** across both P-REL-1 and P-REL-1b, at reduced magnitude.
5. **FAN's six-EMA membership is a builder's reading** (§4), not a quotation.
6. **The I11 panel guard remains NOT ADMISSIBLE** (`m=10`, winner `NEARUSDT|down`, `p_sel=0.0135` vs BH bar `0.01`), so run-2 §4's extreme-cell statements stay **ungated observations**.

---

## 9 · CACHED vs REMAINING

**Cached** (on `D:`, hash-recorded, pins verified live): preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · CEN-0b *(PAXG dropped)* · **CEN-1 (A1-FAN)** · **CEN-2 (predicate columns)** · **CEN-3 (R-F11 + P-REL-1b)**.

**Registrations of record:** P-ARM-1 **NOT SUPPORTED** (confounded) · P-REL-1 **WITHDRAWN** · **P-REL-1b SUPPORTED-PROVISIONAL**.

**Remaining:** **CEN-6 BLOCKED on `h`** → CEN-4 blocked on `verdict-open` → CEN-5(b) blocked on the `v0 band`. CEN-5(a)/(c), CEN-7, CEN-8, CEN-9 are unblocked but unstarted. Unscored: P-iii-b, P-NEST-1, P-i′, P-iv′, P-CHOP-1, P-RAT-2, P-VBT-1 (**7 of 9**), plus filed-next-cycle **P-FAN-1** and **P-ARM-2**.

**Run 4 starts at:** name `h` → CEN-6 → CEN-4 → CEN-5 → CEN-7 → CEN-8 → CEN-9.

---

## 10 · DISPOSITION (with BOX-COST)

| Artifact | Rows | Bytes | sha256 | Home |
|---|---:|---:|---|---|
| `cen1_events` | 529,061 | 33,979,241 | `87906a966b21` | `D:` |
| `cen1_refusals` | 356,315 | 11,330,426 | `0f6442020aca` | `D:` |
| `cen1_counters` | 1,492 | 15,193 | `7eedad61cf2b` | `D:` |
| `cen2_ledger` | 848 | 92,177 | `5d3354f5132a` | `D:` |
| `cen2_fate_table` | 3 | 3,341 | `4f573c6f2eb8` | `D:` |
| `cen3_ledger_lensed` | 848 | 101,701 | `8e05a3ad36d4` | `D:` |
| `cen3_trigger_outcomes` | 595 | 45,082 | `99361ebfedc1` | `D:` |
| `cen3_by_asset` / `_half` / `_depth_wc` / `_depth_dc` / `_fate` | 10/2/4/4/3 | 49,353 | (in manifest) | `D:` |
| this build document + ledger append | — | ~19 KB | — | `exchange/` |

**BOX-COST: bus additions this session ≈ 0.30% of the 6,390,000 B box — under the 1% rule (F-14).** `exchange/` stands at **30.57%** (WARN band, below the 40% refuse line). No results JSON enters `exchange/`. **census2a on `D:` = 45,925,557 B (45.9 MB)** — down from 64.2 MB after the PAXG drop, up from the A1-FAN columns.

**Pointers:** `D:\Naiad\research_outputs\census2a\{cen1,cen2,cen3}\` · `…\census2a_manifest.json`

---

## 11 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12f ===
NOW: CENSUS-2A run 3. The session opened on an infrastructure HALT (D:\Naiad had been moved to
D:\Archive\Naiad); restored on the operator's word, 123 files / 5,229,264,513 B verified identical.
Amendment A1 written to the queue item verbatim, ratified body byte-identical. PX-1(b) executed.
A1-FAN enacted. R-F11 fixed. P-REL-1b scored SUPPORTED-PROVISIONAL — the census's first
registration to survive its own mandated splits. CEN-6 is BLOCKED on an unnamed [VETO].
LAST EVENT: 2026-08-12 — run 3: rulings block executed; CEN-1/2/3 re-run; CEN-6 blocked
FACTS:
- PX-1(b) EXECUTED: PAXGUSDT dropped from D:, 23,636,729 bytes (23.6 MB) freed, klines/ parent
  removed, marked DROPPED in the manifest, re-fetchable via --stage cen0b. The deletion was
  WITHHELD while the estate was displaced — the archived tree was the only copy [verified]
- A1-FAN ENACTED: cross classes 200_500 (6,715 events) and 300_500 (5,480) added; FAN true on
  38.35% of 529,061 events (up 104,688 / down 98,228), KNOT true on 2.63%, both together 710.
  Columns only, nothing scored. FAN's six-EMA membership {9,89,200,300,450,500} is the BUILDER'S
  READING — the ruling names only KNOT's five explicitly and says "six-EMA" for FAN; correct by
  name if a different six was meant [verified]
- P-FAN-1 [60%] FILED next-cycle, UNSCORED: "armings stamped FAN=true at the arming instant show
  higher terminal ATR-return than FAN=false armings, asset-cluster 90% CI excl. 0, both directions"
  — text filed here, to be worded finally by the operator before it is scored [filed]
- P-REL-1b [50%, POST-HOC-INFORMED, LABEL PERMANENT] = SUPPORTED-PROVISIONAL. TREAT 301 vs CONTROL
  294 on explicit predicates (the first-mover label had contaminated run-2's control arm by 33%:
  146 of 440). H100 +0.1869 CI [+0.0638,+0.2887] EXCL-0; H500 +0.6399 EXCL-0; BOTH directions
  EXCL-0; late half EXCL-0, early half straddles; LOAO 4/5. Materially stronger than the
  mis-specified predecessor (which had H500 straddling and LOAO 1/5) [verified]
- CEN-6 BLOCKED: the v0.2 -> v0.3 compression KEPT the noun phrases and DELETED the parenthetical
  "(close beyond + hold h bars [VETO] vs deviation-reclaim)". The [VETO] constant h appears nowhere
  in the ratified body and was never valued. Sweeping h and promoting a winner would be selecting a
  [VETO] by search, which §N forbids. It cascades: CEN-6 -> CEN-4's verdict-open -> CEN-5b's v0 band
  [verified]
- MANDATORY DISCLOSURE for CEN-6 when it runs: LEDGER.md:311 records P-PD1/P-PD2/P-PD4 FALSIFIED,
  "the pattern detectors as gridded do not graduate". Reusing D1/D3/D4 as a LOCATION object is
  legitimate; as a promoted signal it re-runs a falsified test. LEDGER.md:315 P-PD3 CONFIRMED —
  "Z2's deficit concentrates in-range (-0.33R)" — is the part CEN-4 actually wants [verified]
- R-F11 FIXED: run-2's 151,718 lattice-A stream pooled JTO 3,812 + TAO 1,348 into a panel-labelled
  count. Panel-only is 146,558; annex 5,160 printed separately, never added. No panel arming's
  depth moved [verified]
- INFRASTRUCTURE: D:\Naiad was moved outside the repo's doing (daily_routine.py sweeps flat files
  only, skips directories, last ran 07:00). The census cannot survive its residency root vanishing
  mid-run; cause unidentified [verified]
PENDING:
1. NAME h — the acceptance hold length, [VETO]. CEN-6, CEN-4 and CEN-5b are blocked until it is
   valued by the operator. Recommend also auditing the other v0.2->v0.3 compressions for the same
   kind of dropped definition; CEN-6's loss was found only because the stage was reached
2. P-FAN-1 [60%] filed, unscored; final wording is the operator's
3. P-ARM-2 [55%] still filed, unscored (hazard successor to P-ARM-1's confounded limb)
4. FAN's six-EMA membership is a builder's reading pending confirmation
5. ROTATION PROGRAM — filed as a HORIZON WORKSTREAM, not this contract: Hyperliquid as a venue
   candidate, carrying its OWN universe and its OWN evidence wall, NEVER pooled with the Binance
   panel (the PAXG lesson: an asset whose history begins after the wall cannot enter a scored
   table, and a venue is that problem multiplied). The portability battery is the operator's
   tunable-variables question — which constants are venue-invariant and which are fitted to this
   tape. Scoping funnel opens at census close, not before
NEXT: Operator names h; then run 4 proceeds CEN-6 -> CEN-4 -> CEN-5 -> CEN-7 -> CEN-8 -> CEN-9.
Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 2 (the run-3 rulings paste; the (a) restore authorisation)
  — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 3 · rulings executed, first registration standing, stopped on an unnamed constant
