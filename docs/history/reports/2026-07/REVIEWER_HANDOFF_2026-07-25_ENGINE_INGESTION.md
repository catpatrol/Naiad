# Session Handoff — Naiad v12 / Secret Sauce · 2026-07-25
## Reviewer context box audited, engine source ingested, `cells.py` scrutinized — two material findings that change the next contract

**Read this first.** You are the reviewer (Claude, Fable-mode) on a quantitative crypto-trading research project. This session did no analysis and ran no phase. It did something that had never been done: **it read the engine's own source code into the reviewer's context** and checked the project's standing claims against it. Two of those claims did not survive. Your job is to carry the corrections forward into the next contract (CENSUS-1c) and the two Tier-C drafts queued behind it.

Everything below is self-contained. `userMemories` attached to this project carry the ratified long-term state and remain the durable record; this document supersedes them only where it says so explicitly, and every such point is flagged.

---

## 0. Who's who, and the operating discipline

- **Ludwig** — the operator. Discretionary crypto trader with **no programming background**. Owns every merge and every gate decision. Replies in one-word ratifications or explicit rulings. Write every operational instruction step-by-step, in plain language, with expected output.
- **Claude Code** — the builder. Executes locally on Windows/PowerShell. Never merges without operator sign-off. Has now caught **four** reviewer specification errors at execution time (TC-5 `tf_align` config infeasibility · the D8 ratio carried without recompute · the F1b-DERIV absolute tolerance · and, this session, an ambiguous file-copy instruction that produced 14 duplicate files). Treat builder pushback as signal.
- **You (reviewer, Fable-mode)** — independent verification. Recompute every headline from raw artifacts before believing it. Pre-register predictions with explicit probabilities. Own falsifications on the record. Maintain the append-only ledger. **Never let a cost-free or interval-free number stand alone; always print the strip-best line; treat falsification as a deliverable.**

**Standing operational rule (ratified 2026-07-19):** whenever you produce next steps containing commands, questions, or instructions for the builder or the terminal, give the **exact paste-ready text in a code block** — never a paraphrase. Ludwig pastes and goes.

**Standing rule added this session (proposed, needs ratification):** file-copy instructions to the builder must specify the destination filename explicitly, not just a naming *rule*. The ambiguous version produced every file twice.

---

## 1. What the project is, in plain terms

Ludwig trades crypto perpetual futures by hand using a TradingView indicator he wrote, called **Secret Sauce Cascade** (current frozen version SSv11.0.2). The v12 Study is the effort to turn that discretionary skill into a mechanical, rule-based system that can be tested honestly.

The mechanism, in one sentence: after a confirmed **9/89 EMA cross** on a slower "governor" timeframe establishes trend direction, pullbacks into zones built from the governor's own EMAs get absorbed by trend participants — so a faster "execution" timeframe reclaim of its 9 EMA inside such a zone should have positive expectancy net of costs.

**Jargon, defined once:**

| Term | Meaning |
|---|---|
| **EMA 9 / 89 / 200** | Exponential moving averages. 9 = momentum, 89 = trend, 200 = long trend. A "9/89 cross" is the fast line crossing the slow one |
| **governor** | The slower timeframe that sets trend direction for a cell |
| **exec** | The faster timeframe where entries actually fire |
| **align** | A third timeframe used to grade entry quality (A-grade requires alignment) |
| **lens** | The census's word for a *hypothetical* governor applied to price for measurement. **Not the same as the engine's governor — see §5.2** |
| **mandate** | One of three governor/exec pairings: swing, intraday, position |
| **cell** | One asset × one mandate. 10 assets × 3 mandates = the 30-cell pre-registered grid |
| **R** | One unit of planned risk = 0.5% of that cell's equity. All results are quoted in R |
| **cell-R** | Size-weighted realized R summed across the grid |
| **bps** | Basis points, 1/100th of a percent. The money unit |
| **toll** | Round-trip trading cost in bps (fees + slippage) |
| **MFE / MAE** | Maximum Favorable / Adverse Excursion — how far a trade went right / wrong before it ended |
| **quality ratio** | (favorable − toll) ÷ (adverse + toll). Above 1.0 = the move pays for itself |
| **terminus** | The turning point where a pullback stops and resumes |
| **campaign** | A coordinated multi-tranche trade sequence. An **add** increases size in an open position; a **re-entry** is a fill with nothing open |
| **exploration-classic** | Historical data free to mine (through 30 June 2024) |
| **lockbox** | Sealed data (July 2024 – Oct 2025), never touched. Looking at it is irreversible "evidence spend" |
| **strip-best** | Re-run the result with the single best trade removed, to show it isn't one lucky trade |

**The three work tiers:**

- **Tier A** — arithmetic on data already on disk. Free. No pre-registration required.
- **Tier B** — new measurement, trading logic unchanged. Byte-identity of the trading path enforced.
- **Tier C** — an actual rule change. **Must be pre-registered under rule G-7** (a ledger entry with config hash, hypothesis, and numeric prediction) *before* it runs.

**Standing governance rules:** G-7 (pre-register Tier-C) · G-8 (engine guards: equity floor 25%, notional cap 10×, min-stop 0.5 ATR) · **G-9** (fixture tolerances on derived quantities must be *relative*, never absolute — added 2026-07-22 after a mis-specified tolerance halted CENSUS-1b).

---

## 2. State of record at handoff

- **Engine version 1.0.11** *(verified — `version.py`, read this session)*
- **Branch** `v12-v1-census`, **origin HEAD `98fe613`** — the full CENSUS-1b arc is pushed *(from LEDGER; not re-verified this session, no git access)*
- **LEDGER.md** — 694 lines, append-only. Head of record: CENSUS-1b ratified **PASS**, 2 predictions confirmed / 2 falsified, standing rule G-9 added
- **Last completed phase:** CENSUS-1b (Tier A, re-score of the frozen CENSUS-1 substrate in bps net-of-toll)
- **Nothing is running.** No phase in flight, no builder task outstanding

### The arc that got us here, compressed

1. **V3 anchor run** — the faithful mechanical port lost heavily: grid −5,756.91 cell-R at 1× costs, all 20 cells negative, median harvest captured 6% of peak favorable move.
2. **The PROTECTED paradox** — 90.35% of trades that reached +1R favorable excursion still exited at a gross loss, with zero stop advances before the peak. The exit machinery, not entry quality, was the primary failure.
3. **S-2b** — the **structural stop** (place the stop beyond a real 1-hour swing pivot instead of a fixed distance from entry) is the dominant architecture: grid +565.58, strip-best +301.99; swing turns positive-and-robust for the first time.
4. **TC-1 factorial** — the trailing exit is *dominated* and anti-synergizes with the structural stop (interaction −703, negative in every mandate). The two-line exit architecture was **falsified**.
5. **TC-5** — the intraday 1H/5m re-spec: the *mechanical* fractal claim confirmed (excursion-to-toll ratio 0.65 → 1.79), the *economic* claim falsified (still net negative). Ruling: **entries are floored at the 5-minute chart, forever.**
6. **S-3** — the add-to-winner gate is frozen by a circular dependency: 97.59% of winning moments had no add signal available. Ludwig's "serpent eats its tail" diagnosis, proven.
7. **CENSUS-1 / CENSUS-1b** — a trade-independent photograph of price structure across 7 assets × 7 timeframes, then re-scored in money terms. Two durable findings survived their matched nulls; two framework hopes died.

### What CENSUS-1b actually concluded

**Confirmed (2):**
- **P-1b-D5** — the slow-stack-aligned combination is tradeable net of toll (quality ratio > 1.0 on the slow lenses)
- **P-1b-D8** — the 4H cascade rung is a real, modest add-edge: quality ratio **1.0711**, CI [1.0534, 1.0903], n = 28,113

**Falsified (2):**
- **P-1b-C7b** — the pullback *outcome* edge is dead under a powered test (+0.0379 ATR, CI [−0.143, +0.255] spans zero). Where price *stops* is structural (that survives); how far it then *runs* is not
- **P-1b-D9** — the nine-factor k-of-N confluence framework is four factors counted nine ways, with a gradient of ρ ≈ 0.02–0.05. Retired

**The macro-ruling carried forward:** entry-signal combinatorics do not tilt raw price. Measured edge lives in **exit asymmetry**, **toll-space scaling**, and **location structure** — not in cleverer entry signals.

---

## 3. What this session did

No analysis. Three things:

1. **Audited the reviewer's context box** against the real repository, by grepping every contract and ledger entry for file paths and diffing that against what was present.
2. **Ingested 41 files** the operator then supplied — the entire `engine/` package, all config YAMLs, the data-estate manifest, and `.gitignore`.
3. **Scrutinized `engine/cells.py`**, which arrived last and turned out to be the load-bearing file.

**Box state:** 119 files. 40 added in the first batch, `cells.py` added in the second, 2 removed. Both removals were correct: `Naiad_Phase0_Charter-0.md` (an **unratified v0.1 draft** whose `[VETO]` defaults were changed at ratification — an active mis-quotation hazard) and one half of a byte-identical playbook pair.

**Outstanding housekeeping:** 14 pairs of files are byte-identical duplicates *(verified by md5 this session)* — roughly 100 KB of dead weight. The plain-name and `engine_*`/`configs_*`/`scripts_*`/`research_outputs_*`-prefixed copies are the same bytes. **Recommend deleting the prefixed set** from the project box (a UI action, not a terminal one); the plain names are unambiguous in this box, and four engine files arrived in plain form only.

Affected pairs: `signals.py`, `trading.py`, `indicators.py`, `journal.py`, `s2b_decompose.py`, `build_manifest.json`, `v12_anchor.yaml`, `v12_anchor_g8.yaml`, `naiad_v0.yaml`, `v11_faithful.yaml`, `tc1_A/B/C/D.yaml`.

---

## 4. The verified machinery map

Everything in this section was read from source **this session**. Cite it freely; it is the first time the reviewer has had it.

### 4.1 The frozen grid — `engine/cells.py`

```
INTERVAL_MS = {1m, 5m, 15m, 1h, 4h, 12h}        # NO 30m.  NO 1d.
MTF_SET     = ["5m", "1h", "4h", "12h"]         # NO 30m.  NO 1d.
SLIPPAGE_TIER_BPS = {A: 2.0, B: 5.0, C: 10.0}   # bps per side

SYMBOLS: BTCUSDT=A  ETHUSDT=A
         SOLUSDT=B  NEARUSDT=B  ZECUSDT=B  JTOUSDT=B  TAOUSDT=B
         HYPEUSDT=C FARTCOINUSDT=C LITUSDT=C

MANDATES: swing    = gov 4h  / exec 5m  / align 1h
          intraday = gov 1h  / exec 1m  / align 5m
          position = gov 12h / exec 15m / align 4h

LIT_FLOOR_MS = 2025-12-01T00:00:00Z             # the two-token trap guard
Cell.zone_memory -> 3                            # hardcoded, Engine 1.0.3 Pine parity
```

`Cell` is a frozen dataclass carrying `cell_id, symbol, mandate, tf_gov, tf_exec, tf_align, slippage_bps`. `make_cell()` builds one; `all_cells()` builds 30; `cell_by_id()` parses `"{SYMBOL}_{mandate}"`.

The file header reads: *"Frozen at ratification. Any addition requires a ledger entry and fresh pre-registration — do not edit casually."*

### 4.2 The cost identity — an independent verification that landed clean

Round-trip toll = 2 × `fee_bps_side` + 2 × `slippage_bps`, with `fee_bps_side = 5.0` from `v12_anchor.yaml`:

| Tier | Assets | Computed round-trip | Census `TOLL_BPS` |
|---|---|---:|---:|
| A | BTC, ETH | **14.0 bps** | 14.0 ✓ |
| B | SOL, NEAR, ZEC, JTO, TAO | **20.0 bps** | 20.0 (`DEF_TOLL`) ✓ |
| C | HYPE, FARTCOIN, LIT | **30.0 bps** | 30.0 (comment only) ✓ |

*(computed this session from `cells.py` + `v12_anchor.yaml`; census values read from `census_analyze.py:39-41`)*

**This resolves an open disclosure.** The CENSUS-1b ledger entry noted that "no asset in the 7-asset exploration estate maps to the 30 bps C tier — the tier exists in the constant's comment only." That reading was correct but understated: **tier C is a real engine tier with three real assets** (HYPE, FARTCOIN, LIT). They contribute zero exploration-classic rows because their listing dates fall inside or after the lockbox window, which is why the census never used the tier. Worth a one-line ledger clarification.

**Also worth stating:** the census toll covers **fees and slippage only — no funding**. So CENSUS-1c's funding job is strictly *additive* to a cost basis that is otherwise exactly right.

### 4.3 The confirmed-HTF rule — `engine/htf.py`

The governor/MTF value visible to an exec bar is the value at the most recent higher-timeframe bar whose **close** time is ≤ that exec bar's **open** time. This replicates Pine's `expr[1] + lookahead_on` idiom, *"including the fact that an HTF event flag stays visible to every exec bar of the following HTF period."*

That last clause is backlog item **B-2** (the marker carpet) stated as a *logic* property, not a display quirk. Its width, computed this session:

| Mandate | Governor / exec | Exec bars a governor flag stays TRUE |
|---|---|---:|
| swing | 4h / 5m | **48** |
| intraday (v1) | 1h / 1m | **60** |
| position | 12h / 15m | **48** |
| TC-5 v2 intraday | 1h / 5m | **12** |

### 4.4 Where a new rule can enter — `engine/trading.py`

Two candidate hooks, one good and one insufficient:

- **`admit_entry(pe)` (line 142)** — a deliberately pure pass-through, built so fixture F5 can install a broken gate and prove the in-path assertions fire. **Insufficient on its own:** `PendingEntry` carries `{kind, family, dir, size_r, grade, tier, zone, retr, rc, signal_i, stop_at_signal, grade_uncapped, born_aligned, campaign}` — **no MTF state whatsoever**.
- **`arch_data` (line 165/170) — the right answer.** Already precedented by TC-1:

  > `arch_data` (1.0.11, TC-1): `{gov_e200, plow_conf, plow_1h, plow_val, phigh_conf, phigh_1h, phigh_val, exec_1h}` — computed in `replay.py` from the already-loaded governor and 1h frames, passed only when an architecture config key is present. **`None` on baseline configs.**

**Why this matters:** `SignalResult` exposes `g_atr`, `g_e89` and `stage` — governor-level only. The per-timeframe MTF tuples (`mtf[tf]["bx"]/["sx"]/["bull"]`) are computed inside `compute_signals` as **locals and discarded**. So neither a D5 nor a D8 gate can read what it needs from existing outputs. Extending `arch_data` — computed in `replay.py`, gated behind a config key — gives them the data while leaving **`signals.py` literally byte-untouched**, so fixture F-SIG holds as written and baseline configs are provably unaffected. **No fixture needs re-specifying.** This is the single most useful structural result of the session.

### 4.5 Funding data — `DATA_CENSUS.md`

All seven exploration-classic assets have funding history covering the census window:

| Asset | Records | Grid | Gaps |
|---|---:|---|---:|
| BTC | 7,478 | 8h uniform | 0 |
| ETH | 7,244 | 8h uniform | 0 |
| **SOL** | 6,443 | **8h×2360 → 4h×4 → 2h×99 → 8h×3983** | 0 |
| NEAR | 6,275 | 8h uniform | 0 |
| ZEC | 7,034 | 8h uniform | 0 |
| **JTO** | 5,654 | **4h throughout** | 1 |
| **TAO** | 4,903 | **4h throughout** | 1 |

**The trap:** the funding grid is **not uniform**. SOL changes cadence four times; JTO and TAO are on a 4-hour grid. A job assuming "three funding events per day" — the natural default — would misprice three of seven assets. **Any funding job must integrate the actual timestamped records.** `run_trading()` already takes a `funding_df`, so the loader exists; this is plumbing, not new machinery.

### 4.6 Census substrate pins — `build_manifest.json`

Engine 1.0.11 byte-untouched, indicators imported only. Window ceiling `2024-07-01T00:00:00Z`. Row counts: outcomes 149,802 · termini 160,160 · ladder 81,674 · continuation 38,552.

```
census_outcomes.jsonl   daf488acef40a2ab8f23a06d43a77ce2a8256856d635eb2f62bd985bff59385c
census_termini.jsonl    61a9b7a30cc2bb4b20e37def02e59ee74eef345292dd0e822aada83e16c06e4e
census_ladder.jsonl     cc81b8978f81aa277ae38566f5b0fb89e76632b9ff97403f3767f6f3a611bf74
continuation.jsonl      9a7d186620ce7e92722c50a4268e13200756e8da53fabee826194473583b1594
```

Cite these directly in the next contract's §Basis. No need to ask the operator to fetch them.

---

## 5. Findings — what changed, and what it costs

Ordered by impact. Provenance labelled throughout.

### 5.1 🔴 MATERIAL — The engine has no 1D timeframe, and the D5 graduation ruling leans on it

*(verified — grep for `'1d'` and `'30m'` across all nine engine modules returned **zero hits**)*

`INTERVAL_MS` stops at 12h. `MTF_SET` is `["5m","1h","4h","12h"]`. **1D and 30m do not exist anywhere in the engine.**

The CENSUS-1b ratification ruled: *"GRADUATE to a pre-registered Tier-C: (a) the slow-stack-aligned entry (D5 — **robust on 12h/1d**, net-of-cost tradeable)."* Half of that stated basis is on a lens the engine cannot currently represent.

Recomputed from `census1b_results.json` this session:

| Lens | Quality ratio | 95% CI | Per-record median | n | Engine-representable? |
|---|---:|---|---:|---:|---|
| 1h | 0.9442 | [0.9144, 0.9773] | 0.9546 | 13,299 | yes — but **below 1.0** |
| 4h | 1.0724 | [1.0363, 1.1089] | 0.9851 | 13,299 | yes — **skew-dependent** |
| **12h** | **1.0787** | **[1.0427, 1.1155]** | **1.0662** | 13,299 | **yes — robust** |
| 1d | 1.0788 | [1.0357, 1.1146] | 1.0572 | 13,299 | **NO** |

**The honest framing, after arguing against myself:** "un-implementable" is too strong. The census *resamples* 1d from 1h (`RESAMPLE = {"1d": ("1h", 86_400_000)}` in `census_build.py`), so the engine could do the same. But adding it means editing `INTERVAL_MS`, `MTF_SET`, and the loader — an **engine change that breaks fixture F-ENG and needs its own pre-registration**. It is not a config toggle.

**What this does NOT do:** it does not kill D5. **12H alone is robust on both statistics** (ratio-of-medians 1.0787 *and* per-record median 1.0662, both > 1.0) and 12H is the position mandate's governor, fully representable today.

**What it does do:** it narrows the Tier-C's scope. **Recommended scoping** — D5 primary arm on **12H = the position mandate**; 4H (swing) as a secondary arm carrying the skew-dependence caveat explicitly (its per-record median is 0.9851, i.e. the median trade does *not* pay — the edge lives entirely in the right tail); 1H excluded (below 1.0); **1D excluded from the basis and stated as excluded**, with a named follow-up if the operator ever wants the engine extended.

**A convergence worth noting:** scoping D5 to 12H means scoping to the position mandate — which is also where S-2b found the structural stop flips positive-and-robust (+488.19 grid / +224.61 strip-best). Two independent lines pointing at the same mandate is worth more than either alone.

**Action required:** a ledger entry recording that the D5 graduation basis is narrowed to 12H (implementable-robust) + 4H (implementable, skew-dependent), with the 1D evidence excluded and why.

### 5.1b 🟢 GOOD NEWS — D8 is untouched by the same gap, which isolates the problem to D5

The obvious worry is that the missing 1D and 30m timeframes damage the *other* graduated finding too. **They do not.** Recomputed from `census1b_results.json` this session:

| Cascade rung | Quality ratio | 95% CI | n | Engine-representable? |
|---|---:|---|---:|---|
| 5m | 0.8167 | [0.7944, 0.8380] | 29,141 | yes |
| 15m | 0.8104 | [0.7997, 0.8267] | 64,831 | yes |
| 30m | 0.8110 | [0.7874, 0.8248] | 72,424 | **NO** |
| 1h | 0.9688 | [0.9494, 0.9813] | 67,030 | yes |
| **4h** | **1.0711** | **[1.0534, 1.0903]** | **28,113** | **yes** |
| 12h | 0.8085 | [0.7726, 0.8436] | 9,221 | yes |
| 1d | 0.8804 | [0.8341, 1.0563] | 4,215 | **NO** |

**The only rung clearing 1.0 is 4H, and 4H is fully representable.** Both un-representable rungs (30m 0.8110, 1d 0.8804) are *below* 1.0, so the engine's gap costs D8 nothing. Note also that the edge is **4H-specific, not "slow rungs generally"** — the 12H rung is 0.8085, well below break-even.

**Reading:** the D8 Tier-C proceeds at full strength on implementable evidence. **D5 is the only graduated finding whose basis narrows.** That is a cleaner situation than it first appeared, and it should be stated that way in the ledger entry rather than leaving both findings under a general cloud.

### 5.2 🔴 MATERIAL — "Governor" means two different things

*(verified from `cells.py` and `census_build.py`)*

| | Engine | Census |
|---|---|---|
| What | `cell.tf_gov` — **one** governor per cell, fixed by mandate | `GOVERNORS = ["1h","4h","12h","1d"]` — **four** hypothetical lenses over the same price |
| Values | 4h (swing), 1h (intraday), 12h (position) | 1h, 4h, 12h, **1d** |

Every census result reported "per governor lens" is a *measurement frame*, not a trading configuration. Translating a lens result into a rule requires an explicit lens → mandate mapping, and the 1D column has no destination.

**Action required:** CENSUS-1c must state the lens → mandate mapping in §3 and mark 1D diagnostic-only. Every future MTF table should keep printing absolute *and* governor-relative coordinates (standing convention), but should now add a third column: **engine-representable yes/no.**

### 5.3 🟡 REGISTER ITEM — The frozen grid and the ratified 5m floor disagree

*(verified)* `cells.py` still defines `intraday = {gov 1h, exec 1m, align 5m}`. The operator's ruling after TC-5 was: **all future entries are floored at the 5-minute chart, no timeframe below 5m, ever.**

**Steelmanning the existing state first:** this is arguably *correct* behavior. The file declares itself frozen and says changes need a ledger entry plus fresh pre-registration. TC-5 respected that — `tc5_runner.py` builds its v2 cells by **monkey-patching `cell_by_id` at runtime inside the worker**, never editing the frozen file. That is disciplined, not sloppy.

**The actual gap:** nothing records the reconciliation plan. Any future run calling `make_cell(sym, "intraday")` without the patch silently produces a 1m-exec cell that contradicts a standing ruling. This is a **register item, not a defect** — but it should not stay silent.

**Recommended:** a ledger entry naming the discrepancy and pinning when it gets resolved (my suggestion: at the TC-2 contract, since TC-2 inherits the intraday mandate anyway).

### 5.4 🟡 DESIGN FORK — The D8 add rule needs an eligibility window, and nobody has chosen one

*(verified, §4.3)* "The 4H rung fired" is not a one-bar event at execution. At 5m exec it stays TRUE for **48 consecutive bars**. Left unpinned, a D8 gate admits adds across a four-hour window rather than at the rung.

Three candidate windows, all measurable cheaply on the frozen substrate: **first-bar-only** · **N-bar** (N to be pinned) · **full-period**. This is a genuine fork with different economics, not an implementation detail.

**Recommended:** measure all three in CENSUS-1c so the Tier-C inherits a measured answer instead of a coin flip. Costs one extra job; removes an arbitrary constant from a rule contract.

### 5.5 🟢 CONFIRMED — three standing claims survived contact with source

- **The TC-5 halt.** `signals.py:152` reads `align_bull = mtf[cell.tf_align]["bull"]`, populated from `MTF_SET` at line 144. With `MTF_SET = ["5m","1h","4h","12h"]`, a `tf_align=15m` spec raises `KeyError` exactly as the builder said. The ledger's account is precisely right.
- **The `tf_align` invariant.** Ledger: *"v1 `tf_align` = one MTF_SET rung BELOW governor in all three mandates."* Verified true for all three (swing 4h→1h, intraday 1h→5m, position 12h→4h). The TC-5 v2 compression finding — that at 1H/5m the exec and governor are adjacent rungs so the ladder collapses — follows directly and is correct.
- **The cost identity.** §4.2. The census's toll mapping is exactly the engine's fee + slippage round-trip, derived independently and agreeing to the decimal. Both trace to charter §5, so agreement is *expected* — the value of the check is proving no drift between charter, engine and census script across nine months of work.

### 5.6 ⚪ SCOPE CORRECTION carried from earlier this session

Before `cells.py` arrived, checking `census_build.py` produced a correction to a claim made in the previous session — that CENSUS-1c job 1 is *"arithmetic on files already on disk."* **That is half wrong.**

The ladder row schema (`census_build.py:455`) is:

```
{asset, init_tf, dir, init_ts, init_exec_idx, n_rungs,
 rungs:[{tf, lag_exec_bars, rem_mfe_bps_100, rem_mfe_atr_100, rem_mae_atr_100, trunc}]}
```

**There is no governor-lens field on a ladder row.** *(verified from source)*

- Split by **initiating TF** — free, `init_tf` is stored. True Tier-A arithmetic.
- Split by **governor lens** — not stored, and not fully recoverable by joining: the `gov[lens]` block in `census_outcomes.jsonl` is emitted only under the guard `is_exec_regime = (tf == EXEC_TF and ctype == "9_89")` at **line 274** — i.e. only on **5-minute 9/89 anchors**. Ladder initiating crosses span all seven timeframes, so a join covers only the 5m-initiated subset of a 28,113-rung result.

Full coverage needs a **re-walk** re-deriving lens regime state as-of each `init_exec_idx` — precedented (CENSUS-1b's §3.5 job-5b re-walk completed in 26.7 s), still trade-independent, still zero lockbox spend. But the contract must **declare** the re-walk, pin the anchor set, and carry a fixture proving the re-derived lens state reproduces the census's own. Written on the old claim, the builder would have halted. That would have been reviewer specification error number five.

---

## 6. Corrections needing ledger entries

Four, in priority order. None changes a result; all change a *reading* or a *scope*.

1. **D5 graduation basis narrowed** (§5.1) — 12H robust + 4H skew-dependent; 1D excluded as not engine-representable, with the extension named as a separate candidate.
2. **Lens ≠ governor** (§5.2) — the mapping stated, 1D marked diagnostic-only, and the "engine-representable" column added to the standing MTF reporting convention.
3. **Frozen grid vs 5m floor** (§5.3) — discrepancy named, resolution pinned to a phase.
4. **Toll tier C clarification** (§4.2) — the 30 bps tier is real and populated (HYPE/FARTCOIN/LIT); it went unused in the census because those assets have no exploration-classic rows, not because the tier is notional.

---

## 7. The queue

**Immediately next: CENSUS-1c** — a Tier-A/re-walk addendum on the frozen substrate, zero new evidence spend. Jobs:

1. Split D8 by **initiating TF** (free) and by **governor lens** (re-walk — declare it, §5.6).
2. **Price funding** at regime-scale horizons for the D5 combination — integrating real timestamped records, not an assumed 8h cadence (§4.5).
3. Test the **1H→4H gap-clearing binary** as an explicit conditioner, pre-registered, on the causal (prior-only) basis.
4. Add **MAE** to the frontier/depth cuts so the alignment gradient can be scored net-of-cost.
5. *(new, recommended)* Measure the **D8 eligibility window** at first-bar / N-bar / full-period (§5.4).

**Then, in order:**
- **Tier-C: D5 slow-stack-aligned entry** — scoped to 12H/position primary, 4H/swing secondary. Implemented via the **`arch_data` channel** (§4.4), `signals.py` byte-untouched.
- **Tier-C: D8 4H cascade add** — gate only, **no sizing change** (`size_for()` returns a flat `size_add: 0.5` for every add regardless of grade; grade-differentiated sizing is formally deferred to post-TC-1).
- **TC-2** — re-entry quality bar. Inherits the intraday mandate and the 5m-floor reconciliation.

**Parked, none blocking:** D-2 TC-1 adoption ruling (does arm B become the reference architecture?) · SSv11.4 display decisions D-SS-1..7 · the S-1/arm-A excursion back-fill · the exploratory D6b adverse-leg add-location *outcome* test (designed with the P-C7b cautionary precedent built in: location surviving does **not** imply the outcome pays).

---

## 8. What the reviewer still cannot verify

Stated plainly, so the next session knows the edges.

- **`engine/shadows.py`** — the four shadow exits (X-A through X-D) are configured in `v12_anchor.yaml` but only ever seen through the V3 forensics extract. Not on the critical path.
- **Provenance pinning.** The builder was asked to report `git rev-parse HEAD` and a sha256 table for the copied files. If that came back, pin it. If not, treat these as **"operator-supplied copies, commit unconfirmed"** — fine for drafting, **not citable in a contract's §Basis**. Get this before CENSUS-1c is registered.
- **`scripts/` beyond what's in the box** — `s1_runner`, `s2_runner`, `rc7_recompute`, `v3_recompute`, `tc4_*`, `packet.py`. Only matters for re-auditing completed phases.
- **Raw substrate** — the `.jsonl` files and trade journals are correctly fenced (33.6 MB for the enriched termini alone) and should stay out. The results JSONs plus sha-pinned manifests are the right granularity.

---

## 9. Options menu, with reasoning

Two rulings are wanted before CENSUS-1c is drafted, because each changes the contract's *shape*, not its wording.

**Q1 — Does the 1D lens stay in CENSUS-1c job 1?**
- **(a) Include, labelled diagnostic-only** *(my lean)* — nearly free, completes the picture, and a strong 1D result is a legitimate argument for a future engine extension. Risk: a compelling number with no home invites pressure to build one.
- **(b) Exclude** — prevents a finding that cannot be acted on. Risk: throws away information the substrate already contains.

**Q2 — Does CENSUS-1c pre-specify the D8 eligibility window (§5.4)?**
- **(a) Measure all three windows in 1c** *(my lean)* — the Tier-C then inherits a measured constant instead of an arbitrary one. Cost: widens 1c by one job.
- **(b) Defer to the Tier-C** — keeps 1c tight. Cost: a rule contract carrying an unmeasured constant, which is the pattern that produced the last several halts.

**Q3 — Housekeeping**, no reasoning needed: delete the 14 prefixed duplicate files from the project box, and confirm whether the builder's `HEAD` + sha256 table exists so provenance can be pinned.

---

## Appendix — verified constants, one place

*Everything here was read from source or recomputed during the 2026-07-25 session.*

| Constant | Value | Source |
|---|---|---|
| `ENGINE_VERSION` | `1.0.11` | `version.py` |
| `INTERVAL_MS` keys | 1m, 5m, 15m, 1h, 4h, 12h | `cells.py:9` |
| `MTF_SET` | `["5m","1h","4h","12h"]` | `cells.py:21` |
| `SLIPPAGE_TIER_BPS` | A 2.0 · B 5.0 · C 10.0 (per side) | `cells.py:24` |
| `fee_bps_side` | 5.0 | `v12_anchor.yaml` |
| Round-trip toll | A 14 · B 20 · C 30 bps | computed |
| Mandates | swing 4h/5m/1h · intraday 1h/1m/5m · position 12h/15m/4h | `cells.py:46` |
| `zone_memory` | 3 (hardcoded, Pine v11.0.2 parity) | `cells.py:69` |
| `LIT_FLOOR_MS` | 2025-12-01T00:00:00Z | `cells.py:42` |
| Grid | 10 symbols × 3 mandates = 30 cells | `cells.py:88` |
| HTF flag width | swing 48 · intraday 60 · position 48 · TC-5 v2 12 exec bars | computed |
| Census `GOVERNORS` | `["1h","4h","12h","1d"]` | `census_build.py:74` |
| Census `RESAMPLE` | 30m ← 15m · 1d ← 1h | `census_build.py:67` |
| Census toll | BTC/ETH 14.0 · default 20.0 | `census_analyze.py:40` |
| `arch_data` keys | gov_e200, plow_conf, plow_1h, plow_val, phigh_conf, phigh_1h, phigh_val, exec_1h | `trading.py:170` |
| Bootstrap seed | 20260721 | `build_manifest.json` |
| Exploration ceiling | 2024-07-01T00:00:00Z | `build_manifest.json` |

**Provenance key used throughout this document:** *verified* = read or computed this session · *measured* = taken from a results artifact read this session · *expect* = reasoned but unchecked · *open* = unknown.
