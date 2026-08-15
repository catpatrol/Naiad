# BUILD — TIER-C2 · THE FORWARD BASELINE

**Date** 2026-08-15 · **Branch** `v12-v1-census` · **HEAD at start** `90d143e` · **Seed** 20260815 · **Drafted** APOLLO · **Executor** HEPHAESTUS

**CLASS — measurement, not registration. m = 0.** No registration. No lockbox spend. No estate write. No live orders. F-KEY on every join. The population is a *complete* replay of one ratified rule card over one corridor: nothing was selected, swept or promoted, so there is no family to correct over. Any future selection **from** these tables is a new probe and declares its own *m* before it looks.

**Programs (local, this repo):** `scripts/tierc2_rules.py` (the decision path) · `scripts/tierc2_baseline.py` (the program) · `scripts/tierc2_fixtures.py` (the transcript) · `configs/tierc2_paper.yaml` (the Stage-B profile). **Tables live local** at `research_outputs/tierc2/` — `funnel`, `headline`, `monthly_equity`, `stop_geometry`, `trade_journal`, `strip_d_unscored`, `display_only_strips`, `analytics_tape`, `tape_inventory` (all `.parquet`), `build_manifest.json`, `heartbeat.json`.

**I9** — `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()` `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`. Instrument: **BINANCE USDT-M perpetuals**, `{BTC,ETH,SOL,NEAR,ZEC}USDT.P`, offline kline cache `~/.cache/naiad/data_cache/klines`.

---

## 0 · THE ONE THING THE OPERATOR MUST READ FIRST

**The ratified STAGE A corridor was 79.7% sealed lockbox, and the corridor was changed rather than the seal.**

`2024-07-01 → 2026-01-31` was the corridor as written. Its first **462 of 580 days** are the sealed lockbox — `V12_Study_Charter_Addendum_v1.0.md` VR-1 pins it at `2024-07-01T00:00:00Z → 2025-10-05T23:59:59Z`; `engine/replay.py:48-49` encodes the same bounds; `engine/replay.py:152` refuses any replay window touching it without `NAIAD_LOCKBOX_ACK`, because *"unlocking is an operator act."* The corridor's start date **is** `LOCKBOX_START_MS`. `LEDGER.md:865` rules that the seal governs **scored outcome evidence** — which is exactly what THE HEADLINE is — and not raw price in a display-only window. The paste's own CLASS line says *"no lockbox"*, and under the literal corridor that line cannot be true.

Raised to the operator mid-build with the arithmetic. **Ruling: SEAL INTACT — score the post-lockbox remainder.** Four windows, not two:

| window | span | class | days |
|---|---|---|---:|
| **SCORED** | 2025-10-06 → 2026-01-31 | **the yardstick** | 118 |
| SEALED LOCKBOX | 2024-07-01 → 2025-10-05 | **NOT COMPUTED** | 462 |
| census-scored era | exploration-classic, < 2024-07-01 | DISPLAY-ONLY | — |
| pinning window | 2026-02-01 → 2026-08-11 | DISPLAY-ONLY | 192 |

The lockbox strip is **NOT COMPUTED**, not display-only: a strip of net R over sealed bars is scored outcome evidence wearing a label. The other two strips carry outcomes because neither is sealed.

**Warm-up traversal is disclosed, not hidden.** `e316` on 4h needs ~316 bars, so the EMA recursion reads bars before the scored window — lockbox bars among them — to arrive warm. That is the **F4-a posture already on the record** (`LEDGER.md:121`: *"lockbox warm-up traversal disclosed per cell in manifest; zero journal rows with lockbox open times"*). Traversal is not emission. **F-C2-5 proves by min/max ts that no row of any scored table carries a lockbox timestamp.**

---

## 1 · THE RULE CARD, VERBATIM

```
UNIVERSE ["universe"]: {BTC,ETH,SOL,NEAR,ZEC}USDT · LENS ["lens"]: 4h only
TIDE: long iff e89>e316 AND close>e316 on 4h (mirror short)
WINDOW: 4h 12/89 cross in direction, no counter yet; displacement |close−e89|/ATR
  at the cross ≥ d=0.75 ["d"]; sensitivity strip {0.50,1.00} printed UNSCORED
TRIGGER: first in-window 4h 12/26 cross → enter at that bar close
STOP ["stop"]: structural beyond nearest 1H swing pivot (architecture of record);
  R = entry−stop distance; one unit; one position per asset
RIDE: no management of any kind
BELL: counter 4h 12/89 OR 4h 89/316 against → exit at close
ACCOUNTING ["accounting"]: net of 10 bps round-trip + journaled funding; R units
```

**Every constant is cited, none invented (F-C2-3).** The register is `tierc2_rules.REGISTER`, printed in full in the transcript and re-read from source at run time: `ATR_LEN = 14`, `FEE_BPS_SIDE = 5.0` (→ **10 bps round trip, derived not typed**) and `STOP_BUF_ATR = 0.5` from `configs/naiad_v0.yaml`; `PIVOT_L/R = 5,5`, `PIVOT_LOOKBACK_1H = 200`, `TRAIL_B = 0.5` from `engine/trading.py:206-222`. The fixture re-reads `engine/trading.py` and HALTs if `TRAIL_B = 0.5` or the 200-bar lookback has moved.

**Three readings the rule card did not settle, decided and named:**

- **The stop executes.** *"RIDE: no management of any kind"* was read as *no trail, no scaling, no break-even* — not as *the stop is decorative*. `struct_1h` stops execute in the architecture of record. **The bell-only alternative is computed for every trade and printed beside the headline, unscored**, so the reading costs nothing if it is wrong (§3).
- **Adverse-first within a bar.** A bar that touches the stop exits at the stop, even if the same bar also travelled favourably. No intrabar path is modelled.
- **The ride truncates at the window's right edge** (`corridor_end`), so no scored number is computed from a bar outside the scored window. Zero trades hit this in the scored window.

---

## 2 · THE FUNNEL — where the system leaks, counted

Per asset × direction. Cumulative by construction: each column is a subset of the one before it, so the `leak_*` columns are exact differences and every row reconciles.

| asset | dir | armings seen | passed tide | passed d | triggered | entered | leak tide | leak d | leak no-trigger |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| BTCUSDT | long | 6 | 0 | 0 | 0 | 0 | **6** | 0 | 0 |
| BTCUSDT | short | 7 | 5 | 3 | 3 | 3 | 2 | 2 | 0 |
| ETHUSDT | long | 3 | 0 | 0 | 0 | 0 | **3** | 0 | 0 |
| ETHUSDT | short | 4 | 2 | 1 | 1 | 1 | 2 | 1 | 0 |
| NEARUSDT | long | 3 | 0 | 0 | 0 | 0 | **3** | 0 | 0 |
| NEARUSDT | short | 4 | 3 | 3 | 2 | 2 | 1 | 0 | 1 |
| SOLUSDT | long | 4 | 0 | 0 | 0 | 0 | **4** | 0 | 0 |
| SOLUSDT | short | 5 | 3 | 3 | 3 | 3 | 2 | 0 | 0 |
| ZECUSDT | long | 3 | 3 | 3 | 1 | 1 | 0 | 0 | 2 |
| ZECUSDT | short | 4 | 0 | 0 | 0 | 0 | **4** | 0 | 0 |
| **ALL** | | **43** | **16** | **13** | **10** | **10** | **27** | **3** | **3** |

**The tide is the whole funnel.** It removes **27 of 43** armings — 63% — and it removes them *by direction, wholesale*: every long on BTC/ETH/NEAR/SOL, and every short on ZEC. That is not a filter discriminating between setups; it is a regime stamp, and over these 118 days the regime was one-way on all five assets. **`d` removes 3 more. Nothing else leaks at all** — no trigger was refused for an open position, none for a missing structural anchor, none for a degenerate R. The 3 "no-trigger" armings are windows that closed on their counter cross before a 12/26 cross arrived.

**The `d` sensitivity strip — UNSCORED, counts only.** Of the 16 armings that passed tide:

| d | passed d | pass % | |
|---:|---:|---:|---|
| 0.50 | 15 | 93.75% | |
| **0.75** | **13** | **81.25%** | **ratified** |
| 1.00 | 10 | 62.50% | |

No R is attached to any row of this strip. A swept threshold with an outcome beside it is a selection surface; this one has *m* = 0 because nothing was selected.

---

## 3 · THE HEADLINE — the yardstick number, stated plainly

**SCORED 2025-10-06 → 2026-01-31 · 5 assets · both directions · 10 trades**

| | value |
|---|---:|
| **net R** | **−7.7620 R** |
| **expectancy / trade** | **−0.7762 R** |
| **win rate** | **10.00%** (1 of 10) |
| **maxDD (R)** | **9.5107 R** |
| tail concentration (top-decile share of winning mass) | 100.00% — **degenerate, see below** |
| gross R · fee R · funding R | −7.4998 · 0.5877 · −0.3255 |
| best trade · strip-best net R | +1.7487 · −9.5107 |

**The yardstick is −0.7762 R per trade, and it is negative.** Stated positive or not, as commissioned.

**Per asset · per direction · per exit**

| cut | key | n | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|
| asset | BTCUSDT | 3 | −3.2945 | −1.0982 | 0.0 | 3.2945 |
| asset | ETHUSDT | 1 | −1.0954 | −1.0954 | 0.0 | 1.0954 |
| asset | NEARUSDT | 2 | −2.0331 | −1.0166 | 0.0 | 2.0331 |
| asset | SOLUSDT | 3 | −3.0876 | −1.0292 | 0.0 | 3.0876 |
| asset | ZECUSDT | 1 | **+1.7487** | +1.7487 | 100.0 | 0.0000 |
| direction | long | 1 | **+1.7487** | +1.7487 | 100.0 | 0.0000 |
| direction | short | 9 | −9.5107 | −1.0567 | 0.0 | 9.5107 |
| exit | stop | 9 | −9.5107 | −1.0567 | 0.0 | 9.5107 |
| exit | bell_12_89 | 1 | +1.7487 | +1.7487 | 100.0 | 0.0000 |
| exit | bell_89_316 · corridor_end | 0 | — | — | — | — |

**Monthly equity (R), exit-stamped**

| month | n | net R | cumulative |
|---|---:|---:|---:|
| 2025-10 | 1 | −1.0954 | −1.0954 |
| 2025-11 | 1 | −1.0310 | −2.1264 |
| 2025-12 | 5 | −5.1892 | −7.3156 |
| 2026-01 | 3 | −0.4464 | **−7.7620** |

**Read this headline with three caveats, all structural:**

1. **n = 10.** Ten trades over 118 days across five assets. Every per-asset row is n ≤ 3. **No confidence interval is printed, deliberately** — a bootstrap CI on ten campaigns would dress an anecdote as a measurement. The number is the number; its error bars are the width of the whole result.
2. **The tail metric is degenerate and is printed anyway.** With n = 10 the top decile is one trade, and there is exactly one winner — so "top-decile share of winning mass" is 100% by arithmetic, not by finding. Named rather than suppressed, because the estate has four incompatible tail metrics and quoting one silently is how they get crossed.
3. **Nine of ten trades are shorts, and all nine died at the stop.** The single long is the single winner. This baseline measures one regime.

### The lineage row, printed beside — CENSUS RIDE-ONLY

*(Pinned + labelled historical per CONVENTIONS §6.4 leg 3: it reproduces a filed record and must never track a live value.)*

> **Source** CENSUS-2A CEN-5, `BUILD_2026-08-12_CENSUS2A_RUN_6.md` §2.3 (restated `CENSUS2A_CLOSEOUT_2026-08-12.md:59-61` F1)
> **Era** 2019-10-01T01:13Z → 2024-06-30T17:53Z (exploration-classic) · **Ruler** gross R = (exit−entry)/|entry−stop|, **size-free, NOT net of toll**
>
> | stratum | n | median R | mean R |
> |---|---:|---:|---:|
> | loss | 5,829 | −1.0415 | −0.9690 |
> | win | 814 | +2.1422 | **+9.4458** |
> | **ALL** | 6,643 | **−1.0324** | **+0.3072** |
>
> 12.25% winners carrying a mean of +9.4R against a median loser of −1.04R.

**These two numbers are NOT comparable, and the reasons are load-bearing.** Different corridor (exploration-classic vs post-lockbox). Different rule card (the SSv11/v12 cascade book vs this one). Different ruler — RIDE-ONLY is **size-free gross R and is not net of toll** (`TOLL_R` is computed at `census2a_program.py:2445` and never used), while every number in §3 is net of a 10 bps round trip and journaled funding. And different denominators: CEN-5's 6,643 are TC-1 *tranches*, not campaigns. The row is printed **for lineage**, as commissioned — it is the ancestor of the ruler, not a benchmark this baseline beat or lost to.

### The stop, priced — the largest single finding in this build

The rule card sets R from a **1H** swing pivot but enters on a **4h** bar. R and the entry bar's own noise are therefore unrelated quantities, and the fixed 10 bps toll is charged against whichever R happens to result.

| | median | min | max |
|---|---:|---:|---:|
| R ÷ ATR(4h) at entry | 1.293 | **0.525** | 2.164 |
| toll as % of 1R | 3.28% | 1.70% | **19.36%** |

**The bell-only counterfactual — UNSCORED, printed because the ambiguity is real:** riding every trade to its bell and honouring no stop gives **+14.8733 R** against the headline's **−7.7620 R**. The stop costs **22.6353 R** over ten trades.

**But that number is one trade.** ETHUSDT short, 2025-10-29: entered at 3903.54 with R = 41.13 = **0.52 × ATR**, stopped on the *very next bar* — whose low was 3871.17, i.e. the trade was right and the stop sat inside one bar's noise. Its bell-only outcome is **+19.16 R**, which is 89.5% of the whole 22.64 R gap. Strip that one trade and the stop costs 2.38 R across the other nine. **Do not read "+14.87 beats −7.76" as a result. Read it as: one stop placed 0.52 ATR from entry converted a +19 R trade into a −1 R trade, and the rule card contains no rail that would have prevented it.**

The architecture of record does contain that rail — `min_stop_atr: 0.5` (`configs/tc1_B.yaml:53`, engine guard G-8c, `engine/trading.py:555-560`). **The Tier-C2 rule card names no such rail.** No trade here fell below it, but the two tightest (0.525, 0.585) sit within 20% of it, and they are the two worst net R in the book. Reported, not fixed — adding a rail is a rule change, and this is a measurement.

---

## 4 · THREE TRADES, HAND-VERIFIED END TO END (F-C2-2)

Chosen adversarially, not conveniently: the earliest, the best net R, and the widest bell-only gap. Every leg is re-derived from raw bars — arming cross, tide, `d`, trigger cross, stop price from the 1h pivot grid, exit trigger, and net R reconciled from raw prices plus the register's toll and journaled funding. Full transcript in §7.

| | ETHUSDT short | ZECUSDT long | BTCUSDT short |
|---|---|---|---|
| arming (12/89) | 2025-10-29T16:00Z | 2025-12-24T16:00Z | 2025-12-31T16:00Z |
| | e12 4035.52→4015.22 crosses e89 4019.40→4016.83 | e12 422.43→425.68 crosses e89 422.67→423.13 | e12 88239.75→88128.25 crosses e89 88195.35→88180.23 |
| tide | e89 4016.83 **<** e316 4115.92, close 3903.54 ✓ | e89 423.13 **>** e316 416.47, close 443.54 ✓ | e89 88180.23 **<** e316 92282.31, close 87515.00 ✓ |
| d at cross | \|3903.54−4016.83\|/78.4037 = **1.444952** ≥ 0.75 ✓ | \|443.54−423.13\|/13.6938 = **1.490507** ≥ 0.75 ✓ | \|87515.00−88180.23\|/849.9367 = **0.782684** ≥ 0.75 ✓ |
| trigger (12/26) | **same bar**¹ ✓ | 2025-12-24T20:00Z ✓ | 2026-01-01T04:00Z ✓ |
| entry = that bar's close | 3903.540000 | 448.450000 | 87603.700000 |
| stop = 1h (5,5) pivot ∓ 0.5·ATR | 3905.47 + 0.5×78.4037 = **3944.671844** | 441.18 − 0.5×13.3628 = **434.498581** | 87669.70 + 0.5×775.1140 = **88057.256986** |
| R = \|entry−stop\| | 41.131844 | 13.951419 | 453.556986 |
| exit | stop, bar 10-29T20:00 high **3962.55** ≥ stop | **bell 12/89** 2026-01-07T20:00, close 469.38 | stop, bar 01-01T12:00 high **88079.30** ≥ stop |
| **net R** | −1.000000 − 0.095403 − 0.000000 = **−1.095403** | +1.500206 − 0.032894 − (−0.281388) = **+1.748700** | −1.000000 − 0.193648 − (−0.019315) = **−1.174333** |

¹ *arming and trigger on the same bar is legal under the rule card ("first in-window cross", the opening bar included) and occurred twice in ten trades. Note also BTC's `d` = 0.782684 — it cleared the 0.75 floor by 4%.*

All three reconcile to the journal at 1e-6. **7/7 fixtures PASS.**

---

## 5 · THE ANALYTICS TAPE (Amendment B1) — captured, never consulted

**643 rows**, one per `(asset, ts)`, over the scored corridor: **43 arming · 8 trigger · 9 exit · 583 daily-00:00Z spine** (an instant that is both an arming and a spine bar collapses, arming winning — F-KEY depends on it). Local at `research_outputs/tierc2/analytics_tape.parquet`; the four RECORDED-ONLY columns (`wall_family_at_arming`, `dist_atr_at_arming`, `dist_atr_at_trigger`, `coloc_n`) are joined onto `trade_journal.parquet` by ts.

**F-C2-6 — no consultation — is a property, not a promise.** The decision path is a separate module, `scripts/tierc2_rules.py`, and it is proved four ways: (i) an **AST import scan** shows its every import node — `['__future__', 'dataclasses', 'engine', 'engine.s1', 'numpy']` — zero analytics; (ii) its **transitive import closure** over 239 modules contains no `analytics` member; (iii) `engine/` itself imports no analytics module (invariant I-B), so the closure **cannot reach a registry symbol by any path**; (iv) no tape column name appears anywhere in the decision path. *(The line-grep the amendment asks for is printed too — and it failed on its first run, matching this module's own prose about not importing analytics. That false positive is exactly why the AST scan is the test of record and the grep rides beside it.)*

**Tape inventory — instants × families × nulls. No analysis, no conditioning.**

| instant | n | avwap | rvwap | prior-extreme | nearest | coloc_n | atr_1d | 6-ribbon state | wall_dist_atr |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| arming | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 4 (9.30%) |
| trigger | 8 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| exit | 9 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| spine | 583 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 22 (3.77%) |

*(counts are NULLS; every family is complete except `wall_dist_atr`, which is null exactly where `wall_family = "none"`.)*

**Single-wall identity, counted — the one inventory fact worth stating as raw material.** Across the 583 spine instants: `multi` **427 (73.2%)**, `FAST` 108, `none` 22, and MH/H/UH/VH/M 26 between them. At armings: `multi` 35 of 43. **The single-wall stamp is mostly non-identifying at the 4h lens with six ribbons** — three-quarters of the time more than one ribbon band is within 0.5 × daily-ATR of the close, so there is no single wall to name. That is the tape's shape, stated as raw. **It is not a finding about the rule card, and nothing in this build conditions on it.**

**Level families** (`analytics/vwap.py`, `analytics/structure.py`, via the published interface): AVWAP week/month/year · RVWAP {7,30,90,365}d with **±1σ and ±2σ** band edges · prior-day/week/month extremes. Signed distance in ATR, positive = price above the level — **built here, not reused**: the estate's two existing as-of distances (`mc1_program.py:983`, `census2a_program.py:2615`) are both `abs()`. Co-location counts registry levels within **0.15 × daily-ATR** of price (`COLOCATION_ATR`, `census2a_program.py:2531`, register row 13). The six-ribbon state columns are **joined, never recomputed**, from `research_outputs/census2b/oracle/state_v2/<asset>/4h.parquet`.

**F-C2-7 — endpoint-only, honoured and proved.** Every level series is causal, so `series[k]` must equal what a caller gets by slicing to `k` and reading `[-1]`. That identity is not assumed: the fixture rebuilds **all 30 level series from a truncated array** at one probe instant (BTCUSDT 4h, 2025-12-04T00:00Z) and asserts exact equality on every one; then hand-calls `AW.rolling_vwap(...)[-1]` and `AS.prior_period_extremes(...)[0][-1]` with no tape code in the path. **Sabotage re-proven on this corridor:** the F-10 lever with `extra_bars=1` is REJECTED — *"CAUSALITY VIOLATION: bar closing 2025-12-04T08:00:00Z is in the future of the as-of instant 2025-12-04T04:00:00Z"* — and, against the real level path, a 7d RVWAP built one bar into the future reads 89,859.14 against the stored 89,828.12, so the stored value provably did not see it.

**Q6c is why this tape exists and why it is inert.** The ruling is *stillbirth counterfactual first — rescore all historical fills by range-position before any location gate becomes law.* Conditioning here would destroy the unconditioned population that makes the later counterfactual answerable. **The next TC's raw material is raw.**

---

## 6 · DISPLAY-ONLY STRIPS — for continuity, never evidence

> **DISPLAY-ONLY — hypothesis generation only, never evidence**

| window | span | armings | trades | net R | expectancy | win % | maxDD R |
|---|---|---:|---:|---:|---:|---:|---:|
| census-scored era | exploration-classic → 2024-06-30 | 745 | 128 | +34.8898 | +0.2726 | 14.84% | 39.0462 |
| pinning window | 2026-02-01 → 2026-08-11 | 103 | 16 | +37.4521 | +2.3408 | 18.75% | 9.7721 |
| **SEALED LOCKBOX** | 2024-07-01 → 2025-10-05 | **—** | **—** | **NOT COMPUTED** | | | |

Both strips are positive where the scored window is negative. **Do not read that as the rule card working elsewhere** — read it as n = 10 against n = 128, over different regimes, with the census-era strip carrying its own +65.5 R best trade against a −30.6 strip-best. Neither is scored. Neither may be cited.

**The pinning-window strip crosses a ratified fence and it is named here.** VR-1 puts everything after **2026-07-07 23:59:59** in the **forward** partition — *"Naiad's domain. The v12 Study never reads it."* The strip's last 35 days sit past that edge. It is printed because the operator commissioned it explicitly, headed display-only, for continuity; it is disclosed because printing it silently would be the defect.

---

## 7 · FIXTURE TRANSCRIPT

**7/7 PASS** — `{"F-C2-1": true, "F-C2-2": true, "F-C2-3": true, "F-C2-4": true, "F-C2-5": true, "F-C2-6": true, "F-C2-7": true}`. Reproduce with `~/venvs/naiad/bin/python scripts/tierc2_fixtures.py`; the full multi-hundred-line transcript prints there and is not duplicated into the box (§8).

| fixture | verdict | evidence |
|---|---|---|
| **F-C2-1** gates | PASS | HEAD `90d143e` · remote `catpatrol/Naiad` · pwd `/Users/luis/Naiad` == `$HOME/Naiad` · no cloud-sync token · branch `v12-v1-census` · venv present. **ESTATE READY**: all 5 assets × {1h, 4h} over the scored corridor — 1h 2,832 rows, 4h 708 rows per asset, **gaps = 0**, monotonic, `2025-10-06T00:00Z → 2026-01-31T2*:00Z`. |
| **F-C2-2** rule card + 3 trades | PASS | Rule card echoed verbatim; three trades reconciled leg by leg to 1e-6 (§4). |
| **F-C2-3** closed register | PASS | **16** register rows printed with source; `ATR_LEN`, `FEE_BPS_SIDE`, `STOP_BUF_ATR` **re-read live** from `configs/naiad_v0.yaml` and matched; `engine/trading.py` re-read and confirmed to still carry `TRAIL_B = 0.5` and the 200-bar 1h lookback; toll **derived** as 2 × 5.0 = 10.0 bps, never typed. |
| **F-C2-4** determinism | PASS | Full re-run into `research_outputs/tierc2_run2/`; **all 9 table content-hashes identical** (`funnel c3d82945…`, `headline b896756b…`, `journal 58071cf2…`, `tape 74df8437…`, …). **NORMALIZATION DISCLOSURE**: normalized fields are `['elapsed_s']` (wall clock) and the output root path. *No computed value is normalized* — every table, count, hash and R figure is compared content-for-content. Seed 20260815 is printed and **unused**: no stochastic step exists, so determinism here is structural. |
| **F-C2-5** era exclusions | PASS | Per scored table, min/max ts: `trade_journal.entry_ms` 2025-10-29T16:00Z → 2026-01-01T04:00Z · `.exit_ms` 2025-10-29T20:00Z → 2026-01-07T20:00Z · `.arm_ms` 2025-10-29T16:00Z → 2025-12-31T16:00Z · `analytics_tape.ts` 2025-10-06T00:00Z → 2026-01-31T00:00Z. All **in-scored**, all **lockbox-free**, all **after the census ceiling** `2024-07-01T00:00:00Z` (`scripts/census_build.py` `CEIL_MS`). Display-only strips live in their own table and are never pooled into `headline.parquet`. |
| **F-C2-6** no consultation | PASS | AST import scan · 239-module transitive closure · `engine/`↛`analytics/` · zero tape column names in the decision path (§5). |
| **F-C2-7** endpoint + sabotage | PASS | 30/30 level series equal under actual endpoint slicing; two hand-called analytics functions matched; sabotage `extra_bars=1` REJECTED with the causality message; future-bar level provably differs (§5). |
| **F-KEY** | PASS | Asserted before **every** join and logged even on success: `funnel(asset,direction)` · `headline(group,key)` · `monthly_equity(month)` · `stop_geometry(asset,entry_ms)` · `trade_journal(asset,entry_ms)` · `display_only_strips(window,group,key)` · `analytics_tape(asset,ts)` · `tape_inventory(instant,column)` · `ribbon_state(ts)` × 5 assets. **0 duplicates anywhere.** |

**Suite:** `pytest fixtures tests -q -m "not slow"` → **288 passed, 1 skipped, exit 0**, unchanged from session start. No existing test was touched.

---

## 8 · STAGE B — LIVE PAPER ARMED

**One heartbeat, executed now.** `~/venvs/naiad/bin/python scripts/tierc2_baseline.py --stage heartbeat`

> **DISPLAY-ONLY — live-era ops state — hypothesis generation only, never evidence**

```
BAR STATE — last provably-closed 4h bar per asset
  BTCUSDT   2026-08-15T12:00:00Z  close=63068.0
  ETHUSDT   2026-08-15T12:00:00Z  close=1884.09
  SOLUSDT   2026-08-15T12:00:00Z  close=75.49
  NEARUSDT  2026-08-15T12:00:00Z  close=1.635
  ZECUSDT   2026-08-15T12:00:00Z  close=489.51

POSITIONS: 1 OPEN
  OPEN  NEARUSDT  short  entry 2026-07-22T00:00:00Z @ 1.911  stop 1.959687
        held 147 bars  mark 1.635  unrealised +5.6688 R

ARMED WINDOWS AWAITING TRIGGER: 1
  ARMED BTCUSDT  short  since 2026-08-11T12:00:00Z  d=1.601421  awaiting first 4h 12/26 cross
```

The newest cached bar is dropped unconditionally — a forming bucket must never reach a published number (the `_provably_closed_count` law).

**`configs/tierc2_paper.yaml` is committed. The `com.naiad.daily` 07:00 agent is UNTOUCHED**, exactly as instructed: `agent_modified: false`, `registered_in_routine_jobs: false`. Subsequent heartbeats will ride that agent **only after** it is wired into `scripts/routine_jobs.json`, which is a separate operator-authorised act and was **not taken here**. Until then the heartbeat is the hand command above. Every value in the profile is asserted against `tierc2_rules.REGISTER` on load and HALTs on drift, and `trading.enabled: false` is enforced in code — the profile **cannot** place a live order.

**What "engine paper profile" could and could not mean — stated because it is a real limit, not a shortcut.** The rule card is **not expressible in `engine/signals.py`**, for two independent structural reasons: **(a) `e316` exists nowhere in `engine/`** — `grep -rn 316 engine/*.py` returns zero; the frozen signal path is the SSv11/v12 cascade on {9, 89, 200}, and teaching it the 316 leg forks it from the Pine port and breaks **F-SIG** byte-identity, which is an engine change this class of work is explicitly not; **(b) G-1** would refuse the drafted corridor anyway. So the profile follows the engine's config grammar exactly (`config_id` / `signal` / `trading`, ready for a future contracted engine touch) while its **executor is `scripts/tierc2_rules.py` — bit for bit the same module Stage A replayed.** That is the property that actually matters here: **Stage A and Stage B cannot disagree, because they are one implementation.**

---

## 9 · FINDINGS — NOT FIXED

Named, measured, left alone. Each needs an operator ruling, not a patch.

**F-1 · The ratified corridor was 79.7% sealed lockbox, and "clean corridor" is not an estate object.** §0. `"clean corridor"`, `2026-01-31`, and the pinning window `2026-02-01 → 2026-08-11` appear **nowhere** in the repo before this paste; `2024-07-01` is `LOCKBOX_START_MS` exactly. The seal was kept by operator ruling mid-build. **Ruling needed: is the ratified corridor to be re-drawn permanently (post-lockbox only), or is a lockbox spend intended at a future gate?** The 462 sealed days remain unspent and unread.

**F-2 · The yardstick rests on ten trades, and the tide is the reason.** §2–3. The tide removed 27 of 43 armings *by direction, wholesale* — every long on four assets, every short on the fifth. Over 118 days the panel was one-way, so this baseline measures one regime and cannot distinguish "the rule card is negative" from "shorts were wrong in Q4-2025". **Ruling needed: is 118 days an acceptable yardstick window, or should the baseline wait for a longer post-lockbox corridor before the number is treated as a bar to beat?**

**F-3 · The stop's geometry is unrailed, and one trade carries 89.5% of the counterfactual.** §3. R ranges 0.52–2.16 × ATR because R comes from a 1H pivot and the entry from a 4h bar. The architecture of record carries `min_stop_atr = 0.5` (G-8c); the rule card names no rail. The ETHUSDT trade at R = 0.52 ATR turned +19.16 R into −1.10 R. **Ruling needed: adopt the G-8c rail into the rule card, re-derive R on the entry lens, or accept the current geometry and say so.** Not taken here — a rail is a rule change, and this is a measurement.

**F-4 · The rule card does not say whether the stop executes.** §1. *"RIDE: no management of any kind"* admits both readings and they differ by 22.6 R over ten trades. Read as *the stop executes*; the bell-only alternative is computed and printed unscored so the reading costs nothing if wrong. **Ruling needed: confirm the reading, in the rule card's own words, before any multiplier is measured against this number.**

**F-5 · The funnel undercounts by a left edge, measured.** §2. Armings are counted only if the arming bar falls inside the scored window. In the **30 days before** it, **4 armings passed tide + d and 2 of them triggered inside the scored window** — trades this baseline does not contain. Against n = 10 that is a potential 20% undercount. **Ruling needed: prepend a warm-arming lead-in to future corridors, or keep the arming-in-window definition and treat the edge as a known bias.**

**F-6 · The single-wall stamp is mostly non-identifying at this lens.** §5. `multi` on 73.2% of spine instants and 35 of 43 armings. Inventory only — the tape is not conditioned on anywhere. **Ruling needed for the NEXT TC, not this one: narrow the wall test (fewer ribbons, tighter than 0.5 ATR, or per-lens ribbons) before any location gate is built on it, or the gate will be built on a label that says "several".**

**F-7 · The pinning-window strip crosses VR-1's forward edge.** §6. Its last 35 days are in the **forward** partition the v12 Study never reads. Printed as commissioned, headed display-only, disclosed here. **Ruling needed: truncate future continuity strips at 2026-07-07, or ratify that Tier-C forward baselines may read the forward partition for display.**

**F-8 · Two neighbouring names now collide, and only one is renamed.** `TC-2` (the parked re-entry-quality bar) and `Tier-C2` (this baseline) are **distinct objects** with no equivalence stated anywhere. The rename to **TC-RE** is taken in the ledger append below, per `["tc-name"]`. The parked item's text lives at `HANDOFF_2026-07-22_Census_to_Census1b.md:96` and `docs/memory/claude_project_memory_2026-07-26.md:84-85`; **60 occurrences of `TC-2` across 25 files are NOT swept** — the instruction was a ledger touch, and a repo-wide rename is its own authorised act.

**F-9 · Nothing here is a registration, and these tables must not be mined as if they were.** m = 0 holds because the replay is a complete, unranked pass over one ratified rule card. The moment a cut is picked out of §2 or §3 on its R, the selection surface is the number of cells that were available to pick from, and that *m* has to be declared **before** the look, not after.

---

## 10 · DISPOSITION + BOX-COST

| item | disposition |
|---|---|
| `scripts/tierc2_rules.py` | **new** — the decision path, analytics-free by import closure (F-C2-6) |
| `scripts/tierc2_baseline.py` | **new** — the program: replay · tape · tables · heartbeat |
| `scripts/tierc2_fixtures.py` | **new** — the transcript, 7/7 PASS, HALTs non-zero |
| `configs/tierc2_paper.yaml` | **new** — Stage-B profile, asserted against the register on load |
| `research_outputs/tierc2/` | **built** — 9 parquet tables + manifest + heartbeat state, local, gitignored |
| `research_outputs/tierc2_run2/` | **built, hashed, DATA DISCARDED** per rule R3; its `build_manifest.json` retained per refinement D-3 |
| `.gitignore` | **modified** — `research_outputs/tierc2{,_run2}/**` added, matching the per-phase convention; manifests stay tracked by the standing negation |
| THE HEADLINE | **−0.7762 R / trade over 10 trades**, stated plainly, negative |
| THE FUNNEL | **built and printed whole**, 43 → 10, leaks counted |
| THE TAPE | **captured, never consulted**, 643 rows, proved four ways |
| sealed lockbox | **NOT COMPUTED, NOT READ for outcomes** — seal intact |
| `engine/` · `analytics/` · `com.naiad.daily` | **UNTOUCHED** — zero diff |
| registrations | **none**, as classed |

### BOX-COST

`exchange/**` measured **2,608,293 B = 16.30%** of the 16,000,000 B box **before this paste**; the governing **tick set** (`exchange/**` + `LEDGER.md`, per the D3 closure) **2,863,304 B = 17.90%** — state **OK** (warn 40% / refuse 70%), headroom to REFUSE **8,336,696 B**.

**This paste adds 45,692 B = 0.286% of the box** — this document (37,122 B) plus the `LEDGER_APOLLO` append (~8,570 B) — taking `exchange/**` to **2,653,985 B = 16.59%** and the tick set to **2,908,996 B = 18.18%**, level **OK**. **Against the < 0.5% target (80,000 B) that is 57% of budget, with ~34 KB unspent.**

That is deliberate and it cost something, named at the moment of creation. The full fixture transcript runs to several hundred lines and is **not** in the box — §7 carries its verdicts, its evidence values and the one command that reproduces it, and the transcript itself stays local. Same for the 643-row tape, the 30-series endpoint reconciliation, and the per-trade journal beyond the three verified in §4. **What is printed whole is what a reader cannot re-derive from a pointer: the funnel, the headline, the strips, and the findings.** The tables are local at `research_outputs/tierc2/` and are one `read_parquet` away.

**Constants: pin-vs-import per site, per CONVENTIONS §6.4.** `tierc2_rules.py` **defines** the rule card's own constants and **re-reads** the estate's from source at fixture time (never copies them silently). `tierc2_baseline.py` **imports** from `tierc2_rules`. The CENSUS RIDE-ONLY row in §3 is **pinned and labelled historical** — it reproduces a document filed 2026-08-12 and must not track a live value. `BOX_BYTES`/`WARN_FRACTION`/`REFUSE_FRACTION` were **read live from `publish_exchange`**, not typed.

---

## 11 · THE LEDGER_APOLLO APPEND

Per the 2026-08-12 `append` ruling — *a report without its ledger entry is an incomplete deliverable* — this document ends by appending the session's STATUS entry to `exchange/status/LEDGER_APOLLO.md`, **in this session**. Quoted here by its spine only; the complete block lives in the ledger, and duplicating it into the box a second time would pay twice for one piece of prose (§10).

```
=== STATUS_APOLLO — 2026-08-15 ===
NOW: TIER-C2 IS MEASURED. The forward baseline — the number every multiplier must
     beat — is -0.7762 R per trade over 10 trades, 2025-10-06 -> 2026-01-31.
     It is NEGATIVE, and it is stated as commissioned.
     THE SEAL WAS KEPT: the ratified corridor was 79.7% sealed lockbox; the
     corridor moved, the seal did not. 462 days remain unspent and unread.
CLASS: measurement, not registration. m = 0. No lockbox spend. No estate write.
       No live orders. engine/ and analytics/ byte-untouched.
LAST EVENT: 2026-08-15 — TIER-C2 BASELINE + Amendment B1 tape, one build document
FACTS: [9 — the yardstick is negative and thin (n=10) · the TIDE is the whole funnel,
       27 of 43 armings removed by direction wholesale · 9 of 10 trades were shorts
       and all nine died at the stop · the stop is unrailed and one trade carries
       89.5% of the 22.6 R bell-only gap · the toll takes up to 19.4% of R when R is
       0.52 ATR · the tape is captured-not-consulted, proved by import closure not
       by grep · sabotage REJECT re-proven on this corridor · the single-wall stamp
       is 'multi' 73% of the time and is raw material, not a finding · 7/7 fixtures,
       suite 288 passed unchanged]
Q6 DECISION RULE INVOKED: Q6c — 'stillbirth counterfactual first; rescore all
     historical fills by range-position BEFORE any location gate becomes law.'
     This baseline IS that unconditioned population of fills, and the analytics
     tape IS the location record it must be rescored against. Nothing in the rule
     card read a registry symbol; that is why the counterfactual is still
     answerable. No location gate is proposed, and none may be until it is.
NAMING ["tc-name"]: the parked TC-2 re-entry-quality bar is RENAMED **TC-RE** from
     this entry forward (HANDOFF_2026-07-22_Census_to_Census1b.md:96;
     docs/memory/claude_project_memory_2026-07-26.md:84-85). It is a DIFFERENT
     object from Tier-C2, this baseline; no equivalence was ever stated and the
     collision is now removed at the name. 60 prior occurrences across 25 files are
     NOT swept — a repo-wide rename is its own authorised act.
PENDING: [7 operator rulings — F-1 the corridor's permanent shape · F-2 whether 118
         days is an acceptable yardstick window · F-3 the G-8c stop rail · F-4 does
         the stop execute · F-5 the funnel's left edge · F-6 the wall test before any
         location gate · F-7 the VR-1 forward edge on continuity strips]
NEXT: the operator reads §0 (the seal), §3 (the number, and what the stop cost),
      and §9 F-3/F-4. Owner: operator.
PROBE LEDGER: m = 0. EXPLORATION — ungated; promotion requires registration.
```

---

*End of build document. TIER-C2 · measurement, not registration · m = 0 · seal intact, 462 sealed days unspent · no registrations · no rule adopted. The tape is raw material for the next TC and is stated as raw.*
