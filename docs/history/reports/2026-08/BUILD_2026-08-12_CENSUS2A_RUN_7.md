# CENSUS-2A · RUN 7 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md` — body `b0da051b…` + A1 + A2 + A3 + **A4** → file `sha256 bed8615cdacf665882fb38b6f4de6bd8d94b005d80a3f925f2997f0edb562561`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (≤ 2024-07-01)

**Zero context assumed.**

---

## 0 · WHAT RAN

| | State |
|---|---|
| Hard assertions (18) + real F-PIN | **PASS** |
| **Amendment A4** + the closed `[VETO]` register | **DONE** — §1 |
| **F-KEY** (A4-KEY) implemented and exercised | **PASS** — §2 |
| **F-10 sabotage** restored verbatim | **PASS** — §2 |
| **A4-WITCORR** implemented and exercised (F-16) | **PASS** — §3 |
| CEN-7 · CEN-8 · CEN-9 | **REMAINING** — §5 |

Run 7 completed the **A4 repair block** as a whole unit and stopped at a stage boundary before CEN-7. Nothing was half-run.

---

## 1 · AMENDMENT A4 — AND THE REGISTER IS NOW CLOSED

Appended; **prior content byte-identical**, 0 CR bytes. A4 restores two definitions the compression deleted, repairs one metric that was undecidable as written, resolves the P-NEST-1 contradiction, files three next-cycle registrations, adds one fixture, and closes the register.

### The `[VETO]` register — 39 rows

**Why it exists:** neither v0.2 nor v0.3 ever closed a register over its own `[VETO]`s. Three of v0.2's five markers lived in module *bodies* rather than §0 — which is precisely why compressing §0 could not preserve `h`, and CEN-6 stalled a whole session. The register enumerates every constant, its value, and its source (v0.3 §0 / A1 / A2 / A3 / A4).

**A4-REGISTER's HALT check, executed:**

```
=== A4-REGISTER HALT CHECK ===
  scored constants covered by the register : 23
  machinery exempt (named, non-VETO)       : 39
  IN CODE BUT ABSENT FROM THE REGISTER     : 0
  PASS -- the register is closed over the code
```

Every module-level constant in `census2a_program.py` and `mc2_program.py` is either a register row or an explicitly named machinery exemption. **No constant is governing a scored table from outside the register.**

The register also carries a **known-open** list — items deliberately *not* valued, each halting only its dependent stage: the ribbon operand's timeframe set (v0.2 said 30m **and** 1h; the code used 1h only — P-CHOP-1 is already WITHDRAWN for it), `no-slow-arrival-yet`, leap/stair arrival, the ATR buckets and "survives", H-VBT's band rule, and "net terminal R" as median-or-mean.

### A4-TRG — the metric repair

TRG is now defined **for filters only**: summed positive terminal ATR-R of the unfiltered top decile. Alternative-exit arms get **TAIL-EXIT-RATIO** = (arm top-decile R) ÷ (RIDE-ONLY top-decile R), explicitly unbounded above, **no pass-bar this cycle**.

**P-RAT-2's recorded verdict stands; its TRG limb is now VOID by definition**, and the manifest says so. That closes the loop opened in run 6, where TRG returned >1 for 30+ corners because a ratchet is not a filter.

---

## 2 · TWO FIXTURES THAT CAN FAIL

### F-KEY (A4-KEY) — the defect that appeared three times

```
F-KEY  cen3_ledger_lensed        key=['asset','arming_ts']         rows=848  dup=0
F-KEY  cen3_trigger_outcomes     key=['asset','dir','arming_ts']   rows=595  dup=0
```

`assert_key()` declares a join's key and asserts uniqueness **before** the join, halting the stage on violation. It exists because the non-unique-key defect appeared **three times** in this census and each was caught by reading a count, never by a fixture:

| where | key | consequence |
|---|---|---|
| CEN-3 lens join | `(asset, ts)` | a 4h and a 12h bar share an open_time → lookup returned a Series |
| CEN-5 campaigns | `tranche_id` | unique only *within* a cell → **432 of 7,094 dropped (6.1%)** |
| CEN-3 depth map | cascade membership | non-unique under `window_chained` → silent last-write-wins |

### F-10 sabotage — restored verbatim from v0.2

```
F-10 -- sabotage: one future bar must be REJECTED (A4-SAB, v0.2 verbatim)
    clean as-of 2022-02-03 08:00 -> close 36995.50  (last CLOSED bar)
    sabotage REJECTED: CAUSALITY VIOLATION: bar closing 2022-02-03 12:00 is in the
                       future of the as-of instant 2022-02-03 08:00
    PASS  the guard rejects one future bar
```

v0.3 kept *"sabotage fixture mandatory"* and deleted the parenthetical that said what the test **is**. A fixture whose test is unstated cannot fail — the same defect shape as the missing `h`. It now recomputes one registry read twice, once correctly sliced and once deliberately fed one future bar, and **HALTs the census if the second is accepted**.

---

## 3 · A4-WITCORR — RESTORED, AND IT IMMEDIATELY QUALIFIES OUR ONE SUPPORTED RESULT

v0.2's I8 defined witness-correlation in two parts; v0.3 kept the obligation and deleted the definition, and the term existed **in no code**. Restored verbatim and exercised on the census's only promoted discriminant, **P-REL-1b**:

| | value |
|---|---|
| per-asset delta | BTC +0.2042 · ETH **−0.0923** · NEAR +0.4675 · SOL +0.3666 · ZEC +0.2254 |
| **pairwise sign-agreement across assets** | **0.60** (6 of 10 pairs) |
| **panel return correlation over the window** | **0.6458** |

**This is the print doing its job.** P-REL-1b's headline replication is "LOAO 4 of 5" — but the five assets are **0.65 correlated**, so they are not five independent witnesses, and only 60% of asset pairs agree on the sign. Sign-agreement counts witnesses; the correlation says how much they are really *one* witness. **P-REL-1b remains SUPPORTED-PROVISIONAL — and the provisional half of that label just got more load-bearing.**

Recorded on P-REL-1b in the manifest under F-16.

---

## 4 · FINDINGS REPORTED, NOT FIXED

1. **P-REL-1b's five witnesses are 0.65 correlated** with only 0.60 pairwise sign-agreement (§3). Its replication is weaker than the LOAO count suggests.
2. **The ribbon operand remains open** — v0.2 named 30m **and** 1h; the code used 1h. P-CHOP-1 is already withdrawn for it, but the constant is still unvalued and sits in the register's known-open list.
3. **The register's closure is over *module-level* constants.** A literal buried inside a function body would not be caught. A stricter check (AST scan for bare numeric literals in scoring paths) is the natural next hardening and is **not** implemented.
4. **A4-WITCORR is exercised on one discriminant only.** CEN-8 must print it beside every promoted verdict; that has not run.

---

## 5 · CACHED vs REMAINING

**Cached:** preflight · F-GUARD · F-PIN · **F-KEY** · **F-10** · **F-16** · F-6-VEC · F-6 · F-PARITY-2 · CEN-0b · CEN-1 · CEN-2 · CEN-3 · CEN-6 · CEN-4 · CEN-5.

| registration | verdict |
|---|---|
| P-ARM-1 | NOT SUPPORTED (confounded by exposure time) |
| P-REL-1 | WITHDRAWN — unscoreable as written |
| **P-REL-1b** | **SUPPORTED-PROVISIONAL** — now with witness-correlation 0.60 / 0.6458 |
| P-iii-b | NOT SUPPORTED — both-directions clause unmet by 0.0006 |
| P-CHOP-1 | WITHDRAWN — mis-specified component set |
| P-RAT-2 | NOT SUPPORTED — 0/36 corners; **TRG limb VOID under A4-TRG** |
| P-VBT-1 | NOT SCORED — H-VBT undefined |
| P-NEST-1 | **PENDING — scores at CEN-8 (A4-NEST resolves the contradiction)** |
| P-FAN-1 · P-NEST-2 · P-ARM-2 · **P-RAT-3** · **P-VBT-2** | filed next-cycle, unscored |

**Remaining:** CEN-7 · CEN-8 · CEN-9; CEN-5 arms (b)/(c); unscored P-NEST-1, P-i′, P-iv′.

**Run 8 starts at CEN-7.** Everything above it is cached and hash-recorded.

---

## 6 · DISPOSITION (BOX-COST)

No new bulk artifacts this run — A4 is contract + fixtures + manifest. **Bus additions ≈ 0.28% of the 6,390,000 B box** (the amended queue item + this document + the ledger append), under the 1% rule (F-14). census2a on `D:` unchanged at **47.2 MB**. Nothing named census2a on `C:`.

Pointers: `D:\Naiad\research_outputs\census2a\census2a_manifest.json` (A4, F-KEY, F-10, F-16 recorded)

---

## 7 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12k ===
NOW: CENSUS-2A run 7. Amendment A4 appended and the [VETO] REGISTER IS CLOSED -- 39 rows, and the
HALT check finds zero constants in code absent from it. F-KEY and the restored F-10 sabotage both
implemented and passing. A4-WITCORR restored and exercised, and it qualifies the census's one
supported result. CEN-7/8/9 remain.
LAST EVENT: 2026-08-12 — run 7: A4 repair block complete; register closed; three fixtures live
FACTS:
- THE REGISTER IS CLOSED. 39 rows covering every pinned constant and its source (v0.3 §0 / A1 / A2 /
  A3 / A4). The A4-REGISTER HALT check scans every module-level constant in census2a_program.py and
  mc2_program.py: 23 scored constants covered, 39 machinery exemptions named, ZERO absent. The
  structural gap that let h vanish is closed [verified]
- A4-TRG REPAIRS THE METRIC: TRG is for FILTERS only (summed positive terminal ATR-R of the
  unfiltered top decile). Alternative-exit arms print TAIL-EXIT-RATIO, unbounded, no pass-bar this
  cycle. P-RAT-2's NOT SUPPORTED verdict STANDS on its delta limb; its TRG limb is now VOID BY
  DEFINITION and the manifest says so. This closes the run-6 loop where TRG returned >1 [verified]
- F-10 RESTORED VERBATIM AND PASSING: clean as-of 2022-02-03 08:00 -> 36995.50; sabotage rejected
  with "bar closing 2022-02-03 12:00 is in the future of the as-of instant". v0.3 had kept
  "sabotage fixture mandatory" and deleted the parenthetical that said what the test IS -- a
  fixture whose test is unstated cannot fail [verified]
- F-KEY LIVE: assert_key() declares a join's key and asserts uniqueness BEFORE the join, halting on
  violation. Exercised: cen3_ledger_lensed (asset,arming_ts) 848 rows dup=0; cen3_trigger_outcomes
  (asset,dir,arming_ts) 595 rows dup=0. It exists because the non-unique-key defect appeared THREE
  times and every one was caught by reading a count, never by a fixture [verified]
- A4-WITCORR RESTORED AND IT QUALIFIES P-REL-1b. Pairwise sign-agreement across assets 0.60 (6 of
  10 pairs; ETH dissents at -0.0923) against a PANEL RETURN CORRELATION OF 0.6458. The headline
  "LOAO 4 of 5" overstates the replication: five assets correlated at 0.65 are closer to one
  witness than to five. P-REL-1b remains SUPPORTED-PROVISIONAL and the provisional half of that
  label is now load-bearing. This is precisely the print v0.2's I8 required and the v0.3
  compression deleted [verified]
- A4-NEST resolves the contradiction on the record: P-NEST-1 SCORES at CEN-8 as registered on the
  pre-named set; R-4 governs the flags' use as composite stamps only [ratified]
PENDING:
1. CEN-7 -> CEN-8 -> CEN-9 remain; run 8 starts at CEN-7
2. The register's closure is over MODULE-LEVEL constants only. A bare literal inside a function
   body would not be caught; an AST scan of scoring paths is the natural next hardening and is NOT
   implemented
3. The ribbon operand (30m and 1h vs 1h only) is still unvalued and sits in the register's
   known-open list; P-CHOP-1 stays withdrawn until it is named
4. A4-WITCORR is exercised on ONE discriminant; CEN-8 must print it beside every promoted verdict
5. Filed next-cycle and unscored: P-FAN-1 [60%], P-ARM-2 [55%], P-NEST-2 [50%], P-RAT-3 [40%],
   P-VBT-2 [45%]
6. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: CEN-7 (registry as-of + i-b registry-levels completion + two-limb reconciliation), then
CEN-8, then CEN-9. Owner: HEPHAESTUS.
METRICS: operator actions this session = 1 (the A4 rulings paste) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 7 · the register is closed; the deleted definitions are back and one of them already changed a reading
