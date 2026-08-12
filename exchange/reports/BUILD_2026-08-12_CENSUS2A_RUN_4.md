# CENSUS-2A · RUN 4 — BUILD DOCUMENT
**Date:** 2026-08-12 · **Executor:** HEPHAESTUS · **Seed:** 20260812
**Contract:** `exchange/queue/2026-08-12_CENSUS2A_v0.3_RESOLVED_APOLLO.md`
 · ratified body `b0da051b…` (unchanged) · **+A1** · **+A2** → file `sha256 c0c6f01e30dc55a793d9fa87d12a6a7e97661c29bc731e0d1f2a247446e58cab`
**Program:** `scripts/census2a_program.py` · **Class:** EVIDENCE — exploration-classic (≤ 2024-07-01)

**Zero context assumed.**

---

## 0 · WHAT RAN

`h` was named, which unblocked the cascade run 3 stopped on. **One whole stage completed: CEN-6.**

| | State |
|---|---|
| Preflight (10 checks incl. real F-PIN) | **PASS** |
| **Amendment A2** — `h = 2 bars [VETO]` | **DONE** |
| **CEN-6 RANGE & VERDICT** | **DONE** — §2 |
| CEN-4 | **BLOCKED AGAIN** — a *new* unnamed `[VETO]`, §4 |
| CEN-5 · CEN-7 · CEN-8 · CEN-9 | **REMAINING** |

---

## 1 · AMENDMENT A2

```
h = 2 bars  [VETO, operator-named 2026-08-12]
```

Appended to the queue item; **prior content byte-identical**, 0 CR bytes. The acceptance rule is now complete: *an excursion beyond a range boundary is ACCEPTED on a close-set member when that member's close is beyond the boundary and holds beyond for h = 2 consecutive member bars; it is DEVIATION-RECLAIMED when price closes back inside first.* A2 names one previously-unvalued `[VETO]` and re-pins nothing.

---

## 2 · CEN-6 · RANGE & VERDICT (complete)

**Boundary object:** the prior completed **week's** high/low, via `analytics.structure.prior_period_extremes(..., period="W")` — *"causal by construction: a bar only ever sees periods that closed before its own period began."*

**Why not `engine/s2.py`'s D1/D3/D4 detectors** (which do exist and are gridded): `LEDGER.md:311` records **P-PD1 [60%] FALSIFIED · P-PD2 [60%] FALSIFIED · P-PD4 [60%] FALSIFIED — "the pattern detectors as gridded do not graduate."** They are admissible as a *location* object; reusing them as a promoted signal re-runs a falsified test. A prior-week envelope is a location, carries its own causality class, and asserts nothing. *(The counterweight that survived is the one CEN-4 wants: `LEDGER.md:315` P-PD3 CONFIRMED — "Z2's deficit concentrates in-range (−0.33R)".)*

**Not a sweep.** `h` is named, the close-set is pinned, the boundary is one object. The three members are printed head-to-head, not a grid a winner is drawn from — so no I11 promotion occurs. *If a later run promotes a member, that is a selection over m=3 and must clear the guard.*

### 2.1 · Acceptance head-to-head (h = 2)

| member | episodes | accepted | accept rate | deviation-reclaim | median depth |
|---|---:|---:|---:|---:|---:|
| 1H | 2,532 | 1,807 | 0.714 | 725 | 0.34 ATR |
| 4H | 1,425 | 1,044 | 0.733 | 381 | 0.39 ATR |
| 12H | 949 | 702 | 0.740 | 247 | 0.36 ATR |

**Accept rate is near-flat across the close-set (0.714 → 0.740).** Which clock rules changes *how many* excursions there are, barely *what fraction* survive two bars.

### 2.2 · Trap-rate — and a unit defect I introduced and caught

| member | trap rate, **10 member bars** | (that window in hours) | trap rate, **48h fixed** |
|---|---:|---|---:|
| 1H | 0.527 | 10h | **0.803** |
| 4H | 0.607 | 40h | **0.669** |
| 12H | **0.883** | 120h | **0.540** |

**The trend reverses.** A first draft reported only the bar-count column and read `0.527 → 0.607 → 0.883` as structure. It is not: 10 member bars is 10 hours on 1H and **five days** on 12H, so the rising rate was the *window growing*. On a window fixed at 48h for every member, the order inverts — **the 12H close is the least trap-prone**, which is the intuitive reading: a 12H close beyond a prior-week boundary is a stronger commitment than a 1H one.

This is the same duration-vs-bars defect the run-2 review found in the CEN-3 horizons, repeated by me in a new stage. **Both columns now ship, with the mechanism named in the code and the table.**

### 2.3 · Hysteresis prior

| member | P(next verdict == this verdict) | transitions |
|---|---:|---:|
| 1H | 0.598 | 2,527 |
| 4H | 0.620 | 1,420 |
| 12H | 0.635 | 944 |

Against 0.5 = memoryless. Modest, real, and rising with the clock. *(An earlier draft read 0.919 — that was the episode-counting artifact of §2.4, not memory.)*

### 2.4 · An episode is a transition, not a state

The first CEN-6 draft opened an episode at **every** bar whose close sat beyond the boundary, then advanced by `h`. A sustained 100-bar breakout therefore manufactured **50 "episodes" of the same excursion** — 28,816 on 1H against ~200,000 evidence bars. Fixed: an episode begins only when price closes beyond **having been inside**. Episodes fell 39,110 → **4,906**, and the counts now scale sensibly with the clock.

### 2.5 · Verdicts consume CEN-1's refusal events (I8 / D-B)

Refusals in the 10-member-bar window *before* each episode, per episode:

| member | i-a ACCEPTED | i-a RECLAIM | i-b ACCEPTED | i-b RECLAIM |
|---|---:|---:|---:|---:|
| 1H | 0.360 | **0.466** | 0.072 | **0.226** |
| 4H | 0.559 | 0.478 | 0.293 | 0.327 |
| 12H | **0.831** | 0.459 | 0.236 | 0.218 |

**On 1H, deviation-reclaims are preceded by ~3× the price↔level refusal density of acceptances** (0.226 vs 0.072) — the contract's own reading, now measured: *RESPECTED is largely a breakout that failed to be born.* The i-b limb built in run 1 is what makes this visible; it did not exist in the estate before. On 12H the relation inverts for i-a, which is not explained and is reported unexplained.

### 2.6 · `verdict-open` — the interface CEN-4 was blocked on

`cen6_verdict_state.parquet` — **249,062 rows**, one per (asset, member, bar), `verdict_state ∈ {NONE, RESPECTED, BROKEN}` carried forward as-of. This is CEN-4's fifth composite component. **That dependency is now discharged.**

---

## 3 · FINDINGS REPORTED, NOT FIXED

1. **Trap-rate direction depends entirely on the window's units** (§2.2). Any future statement about "which close traps most" must name the window.
2. **Accept rate is near-invariant across the close-set** (0.714–0.740) while episode counts fall 2.7×. The clock changes the sample, not the survival fraction.
3. **The 12H i-a refusal relation inverts** (§2.5) — acceptances are preceded by *more* EMA↔EMA refusal density than reclaims, unlike 1H. Unexplained.
4. **The prior-week envelope is one boundary choice.** A prior-day or value-area boundary would give a different episode population; nothing here establishes the week as privileged.

---

## 4 · CEN-4 IS BLOCKED AGAIN — ON A NEW UNNAMED `[VETO]`

`verdict-open` is discharged, so run 3's blocker is gone. A **different** one is now visible, found by scoping CEN-4 against the estate:

**The chop composite's first component — "churn density percentile" — has no window, no event set, and no reference distribution in the contract.** It is underspecified in exactly the way D-C lens-concordance was in v0.2 (which v0.3 later pinned explicitly). A firing threshold must be named, and choosing it by looking at loser-decile capture or TRG **is a sweep**, which I11 gates and §N forbids for a `[VETO]`.

Two further CEN-4 facts, both measured during scoping and both needing your word before P-iii-b can be scored honestly:

- **`realized_r` is not size-normalised.** The book is 66% `size_r=0.5` / 34% `size_r=0.25`, and the pooled bottom decile is **692/709 = 97.6% `size_r=0.5`**. **The incumbent "loser decile" is substantially a position-size selector.** A size-free ruler (`realized_r / size_r`) moves **145 of 709** members in and out of the decile.
- **The pooled decile is asset-concentrated** — BTC is **37.7%** of "losers" — so an asset-cluster CI computed against that denominator compares unequal panels.

MC-1's original curtain flaw was also reproduced exactly during scoping (W 0.1402 / L 0.5231, matching `BUILD_APOLLO_2026-08-06_MC1.md:485`), confirming what P-iii-b's recut must fix.

---

## 5 · CACHED vs REMAINING

**Cached:** preflight · F-GUARD · F-PIN · F-6-VEC · F-6 · F-PARITY-2 · CEN-0b *(PAXG dropped)* · CEN-1 *(A1-FAN)* · CEN-2 · CEN-3 *(R-F11, P-REL-1b)* · **CEN-6**.

**Registrations:** P-ARM-1 **NOT SUPPORTED** · P-REL-1 **WITHDRAWN** · **P-REL-1b SUPPORTED-PROVISIONAL** · P-FAN-1 filed · P-ARM-2 filed.

**Remaining:** **CEN-4** (blocked on the churn cut + the decile-ruler question) · CEN-5 · CEN-7 · CEN-8 · CEN-9. Unscored: P-iii-b, P-NEST-1, P-i′, P-iv′, P-CHOP-1, P-RAT-2, P-VBT-1.

---

## 6 · DISPOSITION (BOX-COST)

| Artifact | Rows | sha256 |
|---|---:|---|
| `cen6_episodes` | 4,906 | `0ac95a6e08f6` |
| `cen6_verdict_state` | 249,062 | `8c802ff66c62` |
| `cen6_head_to_head` | 3 | `d88b1e726a7a` |
| `cen6_hysteresis` | 15 | `284fb3aa74f5` |
| `cen6_refusal_join` | 12 | `b719082f7bb9` |

All on `D:`; nothing named census2a on `C:`. **Bus additions ≈ 0.16% of the box — under the 1% rule (F-14).** `exchange/` after this paste: see the push line. Pointers: `D:\Naiad\research_outputs\census2a\cen6\`.

---

## 7 · LEDGER_APOLLO APPEND (F-17 · I10 — this section IS the append, same session)

```
=== STATUS_APOLLO — 2026-08-12g ===
NOW: CENSUS-2A run 4. h named (Amendment A2, h=2 bars [VETO]), which unblocked CEN-6. CEN-6 ran to
completion: acceptance head-to-head on {1H,4H,12H}, deviation-reclaim branch, trap-rate both ways,
hysteresis, refusal join, and the verdict_state table CEN-4 was blocked on. CEN-4 is now blocked on
a DIFFERENT unnamed [VETO].
LAST EVENT: 2026-08-12 — run 4: A2 named h; CEN-6 complete; CEN-4 blocked on the churn-density cut
FACTS:
- A2 names h = 2 bars [VETO]. The acceptance rule is now complete and CEN-6 ran. Prior queue-item
  content byte-identical; nothing re-pinned [verified]
- CEN-6 accept rate is NEAR-FLAT across the close-set: 1H 0.714, 4H 0.733, 12H 0.740, on 2,532 /
  1,425 / 949 episodes. Which clock rules changes how many excursions exist, barely what fraction
  survive two bars [verified]
- TRAP-RATE DIRECTION DEPENDS ON THE WINDOW'S UNITS. At 10 MEMBER BARS it rises 0.527 -> 0.607 ->
  0.883; at a fixed 48h it FALLS 0.803 -> 0.669 -> 0.540. 10 bars is 10h on 1H and 5 DAYS on 12H,
  so the rising version measured the window growing. On a comparable window the 12H close is the
  LEAST trap-prone. Both columns ship. This is the same duration-vs-bars defect the run-2 review
  found in the CEN-3 horizons, repeated by the builder in a new stage and caught before publication
  [verified]
- AN EPISODE IS A TRANSITION, NOT A STATE. The first CEN-6 draft opened one at every bar closing
  beyond the boundary, so a sustained breakout manufactured 50 episodes of one excursion (28,816 on
  1H). Fixed: 39,110 -> 4,906 episodes. The 0.919 hysteresis it produced was that artifact; the
  real figures are 0.598 / 0.620 / 0.635 against 0.5 memoryless [verified]
- VERDICTS CONSUME REFUSALS: on 1H, deviation-reclaims are preceded by ~3x the price<->level (i-b)
  refusal density of acceptances (0.226 vs 0.072 per episode) -- the contract's "RESPECTED is
  largely a breakout that failed to be born", now measured. The i-b limb built in run 1 is what
  makes it visible. On 12H the i-a relation INVERTS and is reported unexplained [verified]
- CEN-6 used a prior-week H/L envelope, NOT engine/s2.py's D1/D3/D4, because LEDGER.md:311 records
  P-PD1/P-PD2/P-PD4 FALSIFIED -- those detectors are admissible as a LOCATION object but not as a
  promoted signal [verified]
PENDING:
1. CEN-4 BLOCKED on a NEW unnamed [VETO]: the chop composite's churn-density-percentile component
   has no window, no event set and no reference distribution in the contract. Naming the firing cut
   by looking at capture or TRG is a sweep, which §N forbids for a [VETO]. Operator must name it
2. CEN-4 decile ruler, operator's call: realized_r is NOT size-normalised. The book is 66%
   size_r=0.5 / 34% 0.25 and the pooled bottom decile is 692/709 = 97.6% size_r=0.5 -- the
   incumbent "loser decile" is substantially a POSITION-SIZE selector. A size-free ruler
   (realized_r / size_r) moves 145 of 709 members. The pooled decile is also 37.7% BTC, so an
   asset-cluster CI against that denominator compares unequal panels
3. P-FAN-1 [60%] and P-ARM-2 [55%] still filed, unscored; FAN's six-EMA membership still a
   builder's reading
4. ROTATION PROGRAM unchanged: Hyperliquid, own universe, own evidence wall, never pooled;
   portability battery = the tunable-variables question; funnel at census close
NEXT: Operator names the churn cut and rules on the decile ruler; then CEN-4 -> CEN-5 -> CEN-7 ->
CEN-8 -> CEN-9. Owner: operator, then HEPHAESTUS.
METRICS: operator actions this session = 1 (h = 2 bars) — files re-ingested = 0
=== END STATUS ===
```

— HEPHAESTUS, 2026-08-12 · CENSUS-2A run 4 · CEN-6 complete; blocked again, one constant further on
