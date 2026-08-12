# CONTRACT v4 — ANALYTICS-1 · BRIEF-2 · FORWARD-0
### Naiad BRIEF lane · consolidated 2026-07-28 · supersedes CONTRACT v3 and its Amendment 1 (neither was executed)
### Ratified by operator interviews D-B9..D-B29 and Groups A–D (2026-07-28)

---

## §0 SCOPE

| Phase | What |
|---|---|
| **0 — PRE-FLIGHT** | Diagnostics, repo-root filing, archive-dependency audit. Read-mostly. |
| **I — ANALYTICS-1** | Versioned pure-computation toolbox `analytics/`, outside `engine/`. |
| **II — BRIEF-2** | The brief rebuilt on it: levels → confluence areas → lines in the sand → if-then drafts; tracked three-slot archive; twelve gap fixes; new commands. |
| **III — FORWARD-0** | Hash-chained append-only trade diary. No scoring until **G-10** is separately ratified. |
| **IV** | Handoff spec only (CENSUS-1d + H-RVX). **NOT BUILT.** |

Tier OPS. No Tier-C created or implied. No engine module modified.

**Execute as a decision tree:** run Phase 0 → I → II → III in order, halting **only** on a failed hard gate, a failed fixture, or a genuine fork. On halt: report the exact blocker with `file:line`, write nothing further. Never improvise past an ambiguity — halt and ask one precise question.

---

## §1 GOVERNING RULES

1. **Firewall, four clauses, reprinted in every artifact.** Live data is ops-only and forbidden as study evidence · no journal reads and no signal- or trade-outcome statistics on any window · engine modules imported read-only with trading disabled and never modified · the archive is a hypothesis mine, never a scoring window.
2. **Confluence scores measure agreement between tools, not edge.** No output may be phrased predictively.
3. **`analytics/` lives outside `engine/`.** Engine files are frozen and hash-cited.
4. **Do not modify:** `engine/*` (any file), `configs/*`, `study/*`, `scripts/backup_estate.py`, `scripts/reviewer_manifest.py`, `scripts/orchestrator_state.py`. Do not touch `LIT_FLOOR_MS`. Do not delete any parquet in the data cache. Commit, never push.
5. **Interpreter is `C:\venvs\naiad\Scripts\python.exe`** (POSIX form `C:/venvs/naiad/Scripts/python.exe`). `.venv` no longer exists. Every command file, scheduler entry and docstring this contract creates or edits uses the new path.
6. **Machine-readable handback** into `_reviewer_box/`. No terminal screenshots.

---

# PHASE 0 — PRE-FLIGHT

## §0.1 Environment gate — corrected design

**HARD gate (halt on failure), AMENDED 2026-08-12 (queue 004 Phase A):** branch is `v12-v1-census`; the working directory path **ends with `C:\Naiad`** (or `/c/Naiad`) **AND does NOT contain `OneDrive`**; the repo root contains `engine/` and `prompts/`. *Two-sided on purpose: until Phase B deletes the old tree, two complete clones exist side by side, and only checking both directions distinguishes the live clone from the abandoned one. The former wording required `\Users\` and `OneDrive`, which after the move would halt every valid session and admit every invalid one.*

**INFORMATIONAL (report, do not halt):** current HEAD. Expected to begin `837c635`; if it has advanced further that is normal and this contract does not depend on pre-commit state. *Rationale: the previous paste pinned an exact HEAD and produced a false halt when the operator's own authorised commits advanced it. Environment identity and state freshness are different questions and must not share a gate.*

## §0.2 Diagnostics — report only, no action

1. **Tier-2 reality check.** Does `research_outputs/brief/brief_2026-07-28.json` contain non-null open interest, basis and top-trader ratio for BTCUSDT? Quote the values. This settles whether `F-B6`'s "all Tier-2 fetches failed" message reflects the mocked fixture or a real fetch failure.
2. **Manifest scope.** `reviewer_manifest.py` reported *"worktree clean (tracked files): yes"* while three tracked files were modified. Print the exact predicate for that field and state whether its scope is the 46 SOURCES or the whole tracked tree.
3. **Google Drive.** `G:\My Drive\naiad-backups` **exists** — the operator confirms it, and reports naiad files there he did not place. The 2026-07-28 setup task concluded no Drive was present. Determine why: check `G:` from **both** a Windows-native call (`powershell -c "Test-Path 'G:\My Drive\naiad-backups'"`) and the bash/msys context, and report whether the drive is invisible to msys. List the directory's contents with sizes and mtimes.
4. **`backup_estate.py` scope.** It was built at `837c635` (F-K1..7 pass). Report its configured source scope and destination. State whether `briefs/` and `research_outputs/brief/` are inside that scope. **Report the one-line change needed if not — do not make it;** that script belongs to another lane.
5. **Provenance of arrivals.** Print sha256 for `scripts/orchestrator_state.py` and `scripts/daily_routine.py` and state whether either is byte-identical to anything under `_reviewer_box/` or `claude/`.

## §0.3 Repo-root discipline — **STANDING RULE, adopted (Group D)**

Contracts live in `prompts/`. Handoffs live in `docs/handoffs/`. Neither lives at the repo root. Create `docs/handoffs/` if absent, then move — verifying sha256 before and after each move and asserting equality:

```
CONTRACT_ANALYTICS1_BRIEF2_FORWARD0_draft.md  -> prompts/
HANDOFF_2026-07-27_BRIEF_to_ENGINE.md         -> docs/handoffs/
HANDOFF_2026-07-27_BRIEF_to_CENSUS_1.md       -> docs/handoffs/
```

If a byte-identical copy already exists at the destination, delete the root copy instead and say so explicitly. **Leave every other root file untouched** — orchestrator, status and Pine files are not this lane's to move. Commit: `docs: file brief-lane contracts and handoffs out of repo root`.

## §0.4 Archive-dependency audit — **STANDING RULE, adopted (Group D)**

The 2026-07-27 reclamation has now cost two retrievals: the `c141t213` regression fixture, and the S-3 journals the census Phase 0 needs. Both were avoidable with one grep.

Produce `docs/ARCHIVE_DEPENDENCIES.md`: every path under `research_outputs/` that is read by any file in `fixtures/`, `tests/` or `scripts/` — with the reading `file:line`, and whether the path currently resolves or exists only inside `research_outputs/_archive/*.zip`.

**The rule going forward:** no phase directory is archived until this document is regenerated and the archive's manifest records which readers depend on it. State the rule at the top of the file.

---

# PHASE I — ANALYTICS-1

## §I.1 Layout

Repo root `analytics/`. Pure arithmetic on arrays. No files, no network, no engine imports, no knowledge of the brief.

```
analytics/
  __init__.py     ANALYTICS_VERSION, CONVENTIONS, analytics_sha()
  momentum.py     rsi · stoch_rsi · macd · awesome_oscillator · ema · sma · divergences
  vwap.py         rolling_vwap · anchored_vwap · vw_sigma_bands
  volatility.py   true_range · atr · realised_vol · percentile_rank
  profile.py      volume_profile (POC/VAH/VAL) · naked_poc_registry
  structure.py    pivots · period_opens · prior_period_extremes
  levels.py       LevelRegistry · collapse_same_family · cluster · score · lines_in_sand
  stats.py        beta · correlation · zscore
  parity.py       worksheet text generation (returns strings, writes nothing)
```

## §I.2 Invariants (each a fixture)

**I-A** no I/O · **I-B** no engine imports · **I-C** deterministic bit-for-bit · **I-D** warm-up returns `NaN` for exactly the documented length, never a seeded number · **I-E** `CONVENTIONS` names the exact variant of every recipe **and its causality class** (§I.5); consumers print `ANALYTICS_VERSION` and `analytics_sha()` · **I-F** semantic versioning — any change to a returned number bumps at least the minor version, because archive comparability depends on it.

## §I.3 Pinned conventions

| Recipe | Convention |
|---|---|
| RSI | length 14, Wilder/RMA smoothing, source close |
| StochRSI | RSI 14, Stoch 14, %K smooth 3, %D smooth 3, source close |
| MACD | EMA(12) − EMA(26), signal EMA(9), hist = MACD − signal, source close |
| Awesome Oscillator | SMA(5) − SMA(34) of bar midpoint (H+L)/2 |
| ATR | length 14, Wilder, TR = max(H−L, abs(H−C₋₁), abs(L−C₋₁)) |
| Anchored VWAP | source hlc3, volume-weighted from the anchor bar, computed on 1h klines |
| Rolling VWAP | **exact TradingView RVWAP algorithm — §I.4** |
| σ bands, all VWAPs | volume-weighted **population** variance via §I.4; **no (n−1) correction** |
| Pivots | pivot(5,5); **a pivot is only confirmed 5 bars later** — the function must expose `confirmation_lag` so as-of callers cannot consume unconfirmed pivots |
| Divergence | pivots(5,5) on price and oscillator; last 2 pivot pairs per TF; regular = price extreme extends while oscillator does not; hidden = the converse |
| Realised vol | close-to-close log returns, 7d vs 30d ratio, not annualised |
| Percentile rank | rank among trailing sample, 0–100, sample size printed |
| Resampling | 30m and 1d **byte-identical to `scripts/s1_resample.py`** (F-AN-14) |

## §I.4 Rolling VWAP and σ bands — pinned from source

Pinned from TradingView's published Rolling VWAP Pine source (v5, MPL-2.0), supplied by the operator.

**Window:** a trailing window of **W milliseconds**, not a bar count, floored at the **10 most recent bars** even when they fall outside W. On gapless 24/7 perpetuals the two coincide; they diverge only across gaps, which is why the time form is implemented.

**Fixed periods:** W ∈ {7, 30, 90, 365} days.

With `src = hlc3`, over the window:

```
sumSrcVol    = Σ (src × volume)
sumVol       = Σ volume
sumSrcSrcVol = Σ (volume × src²)

RVWAP    = sumSrcVol / sumVol
variance = max( sumSrcSrcVol/sumVol − RVWAP² , 0 )
stdev    = sqrt(variance)
band(k)  = RVWAP ± k · stdev
```

Three things an implementer must not "improve":

1. This is the volume-weighted **population** variance via the one-pass identity E[x²] − E[x]². **No (n−1) correction.** An unweighted standard deviation of typical price, or a sample-form correction, yields plausible numbers that never match the operator's chart.
2. The **clamp at zero is algorithmic**, not defensive padding: the one-pass identity can go slightly negative through floating-point cancellation at high price with low dispersion — precisely the BTC-at-65,000 case.
3. Also compute the **two-pass** volume-weighted variance and assert the discrepancy is below a stated tolerance (F-AN-11). Matching TradingView requires the one-pass form; knowing its fragility at our price scales is a separate necessary fact.

**Anchored VWAP bands** use the same variance definition over the anchor-to-now window. This is a reasoned inference from shared TradingView band machinery, **not read from source** — flag it in the parity worksheet as *to be confirmed by reading*, never assert it.

**Boundary:** window membership = bars with `bar_open_time > current_bar_open_time − W`, inclusive of the current bar. If RVWAP parity fails by a small amount, test this boundary **first** and the min-bars floor at gaps **second**.

## §I.5 Causality classes — **the structural fix**

The ENGINE lane reports a **one-sided-window hazard** in the current `scripts/daily_brief.py`: code that is safe today only because the caller always passes data ending at "now", and which this extraction converts into an unguarded bug the moment a general-purpose function is handed a longer array. Neither lane located the specific instance. Rather than hunt one, install the test that finds the whole class.

Every entry in `CONVENTIONS` carries a `causality` field, one of:

- **`causal`** — output at index *i* depends only on input `[0..i]`. Must pass F-AN-13.
- **`lag:N`** — output at *i* is knowable only at *i+N* (pivots: N=5). Tested under F-AN-13 **at lag**.
- **`endpoint_only`** — the value is valid only at the end of the supplied array (e.g. a percentile against a trailing sample computed once at the tip). Exempt from F-AN-13, but **must raise a clear error** if called with an `as_of_index` pointing anywhere other than the array end.

*A caller contract living in a human's head becomes a property asserted in code, so a future refactor cannot silently void it.*

## §I.6 Parity harness — the trust gate

`scripts/parity_worksheet.py` emits `_reviewer_box/parity_worksheet_<date>.md` for the operator to fill from his own charts.

**Canonical instrument:** Binance USDT-M perpetuals, `BINANCE:<SYM>USDT.P`, chart timezone **UTC**, **closed** candles only. BTC-weighted; ETH and SOL rows marked *optional if not charted*.

**Rolling-VWAP parity target:** TradingView's **official "Rolling VWAP" (RVWAP)** indicator with *Use a fixed time period* checked, Days = 7/30/90/365, source hlc3, bands multiplier 1 — the indicator whose source we hold. The operator's **private** rolling-VWAP script is *not* the target; include an optional extra column for its reading, because a divergence between private and official is itself informative.

**24 current-bar rows:** RSI(14) BTC 1h/4h/12h/1d (4) · RSI ETH 4h/1d (2) · RSI SOL 4h (1) · StochRSI %K BTC 1h/4h/1d (3) · StochRSI %D BTC 4h (1) · MACD line + histogram BTC 4h (2) · AO BTC 4h/1d (2) · ATR(14) BTC 1d (1) · anchored M-VWAP BTC and its +1σ (2) · anchored Q-VWAP ETH (1) · RVWAP BTC 7d/30d/7d+1σ/365d (4) · RVWAP ETH 30d (1).

**Plus 4 historical rows ~30 days back** (BTC: RSI 4h, RVWAP 7d, anchored M-VWAP, AO 4h) to catch warm-up and window drift rather than testing only the newest value. Total 28 cells.

The worksheet opens with plain-language instructions: set the chart timezone to UTC, use the `.P` perpetual not spot, hover the named candle, read closed values only.

**Acceptance:** a reading matches if it agrees to the precision TradingView displays. **Any mismatch halts adoption of that recipe** and is reported with the observed difference — never patched around, never rounded into agreement.

## §I.7 Fixtures — Phase I

- **F-AN-1** golden values: hand-checkable arrays with independently derived expectations for RSI, StochRSI, MACD, AO, ATR, VWAP, pivots; equality 1e-9.
- **F-AN-2** determinism: every public function twice on identical input → bit-identical.
- **F-AN-3** no engine imports (source scan).
- **F-AN-4** no I/O (source scan): no `open(`, `read_parquet`, `requests`, `urllib`, `os.environ`.
- **F-AN-5** `analytics_sha()` equals a fresh recomputation over package sources via `hashlib` on binary reads.
- **F-AN-6** warm-up: `NaN` for exactly the documented length, finite immediately after.
- **F-AN-7** edge cases: flat series, zero-volume bars, series shorter than warm-up — documented behaviour, no exception, no garbage.
- **F-AN-8** **BRIEF EQUIVALENCE — the regression guard.** Every recipe `daily_brief.py` already computes reproduces its v1.1 **published** values on the frozen fixture day to 1e-9. Emit a full diff table. *A refactor that silently changes an already-accepted number is the worst available outcome.*
- **F-AN-9** cluster reproducibility: fixed registry → identical clusters and scores; scores recompute from their own member lists.
- **F-AN-10** RVWAP window semantics on a synthetic series with a deliberate gap; assert the 10-bar floor engages.
- **F-AN-11** variance stability: one-pass vs two-pass volume-weighted variance on a high-price / low-dispersion synthetic; **assert** the discrepancy is below a stated tolerance and carry the number into the calibration report.
- **F-AN-12** pivot `confirmation_lag` exposed and non-zero.
- **F-AN-13** **CAUSALITY / TRUNCATION PREFIX.** For every series-returning public function, at ≥5 truncation points *k* spread across the series (including one near the warm-up boundary and one near the end): assert `f(x[:k])[k-1] == f(x)[k-1]` exactly. `lag:N` functions are tested as `f(x[:k+N])[k-1] == f(x)[k-1]`. `endpoint_only` functions are exempt but must raise when misused. **A failure is a FINDING: report the function, module and mechanism before fixing it.**
- **F-AN-14** **RESAMPLE PARITY.** 30m and 1d resampling byte-identical to `scripts/s1_resample.py` on the same input. Asserted **from the test file** (tests may import both), so `analytics/` keeps invariant I-B. Basis: `engine/s1.py:70-73` already extends 30m and 1d outside the frozen `INTERVAL_MS`/`MTF_SET` map and is F-RESAMPLE PASS, so daily ATR is an existing fixtured capability — match the convention, do not invent one.

## §I.8 Deliverables — Phase I

`analytics/` · `tests/test_analytics.py` · `scripts/parity_worksheet.py` · `_reviewer_box/parity_worksheet_<date>.md` · `_reviewer_box/ANALYTICS1_REPORT.json` (fixtures, version, sha, warm-up lengths, causality class per function, F-AN-8 diff table, F-AN-11 discrepancy).

---

# PHASE II — BRIEF-2

## §II.1 Capture slots and scheduling — **one runner, three triggers (Group B)**

Three captures per day, session-anchored, times held in **America/New_York**:

| slot | New York | UTC | why |
|---|---|---|---|
| `london` | 08:00 | 12:00 | London active, NY pre-open |
| `ny_am` | 11:00 | 15:00 | 90 minutes after the NY open |
| `post_ny` | 17:30 | 21:30 | 90 minutes after the NY close |

**Do not build a second scheduler.** `scripts/daily_routine.py` and `scripts/routine_jobs.json` already exist as the job runner. Extend rather than duplicate:

1. `daily_routine.py` accepts `--slot {london,ny_am,post_ny}` and passes it to the brief job.
2. `routine_jobs.json` gains a `slots` array declaring which jobs run in which slot (manifest: all slots; brief: all slots).
3. `ops/brief_schedule.yaml` holds slot names and America/New_York times.
4. `scripts/setup_brief_schedule.ps1` **generates three Windows tasks** from that file, each invoking `daily_routine.py --slot <name>` with `C:\venvs\naiad\Scripts\python.exe`.

**DST hazard — resolve, never store an offset.** New York observes DST; Buenos Aires does not. From 2026-11-01 NY is UTC−5, so a schedule pinned to a stored UTC offset silently drifts an hour off the session anchors. Times must be resolved through the `America/New_York` zone at task-generation time, and the setup script must print the next four DST transition dates and instruct re-running after each. Every capture records **slot name, UTC time and New York local time**, so drift is visible rather than silent.

## §II.2 Storage and access

- Captures: `briefs/brief_<date>_<slot>.json` — **tracked**. Index: `briefs/index.jsonl`, one line per capture.
- HTML: `research_outputs/brief/` — **untracked**, with **pattern-based** ignore rules, never a directory exclusion (git cannot re-include a file inside an ignored directory).
- Every capture embeds `schema_version`, `rules_version`, `rules_sha256`, `analytics_version`, `analytics_sha`, `engine_version`, `slot`, the complete rule set, and every input's `last_bar_utc`.
- `/brief` **auto-commits** its capture (`ops: brief capture <date> <slot>`) and **never pushes**. A same-slot re-run warns, shows what would be replaced, and requires confirmation. *(This already bit us: on 2026-07-28 the brief ran twice and silently overwrote its own capture.)*
- `scripts/brief_render.py --date <d> [--slot <s>]` regenerates HTML from any stored capture. This is what makes HTML disposable.

**Three panel tables**, grain **(asset, capture_slot, date)**, rebuilt by `scripts/brief_panel.py` from captures alone:

| table | grain | contents |
|---|---|---|
| `briefs/panel/snapshots.parquet` | asset × capture | every scalar: prices, all indicator values per TF, RSI/StochRSI/MACD/AO states, RVWAP values and cross states, funding/OI, verdicts, votes, all confluence flags, radar state per lens |
| `briefs/panel/levels.parquet` | level × asset × capture | family, label, level, source_layer, timeframe, cluster_id, distance in bps and daily-ATR |
| `briefs/panel/areas.parquet` | area × asset × capture | mean level, score, family composition, member count, distance, is_lis, stability across tolerances |

`briefs/panel/SCHEMA.md` documents **every** column, its units, its source layer, and the `schema_version` it appeared in. A future session must understand the panel without reading the generator.

## §II.3 Backfill rule

The forward archive under `briefs/` accumulates **forward only**. The generator **refuses** a target date earlier than the first real capture unless an explicit `--backfill` override is passed, and the override stamps a loud provenance marker into the capture.

Applying the confluence engine to **historical** data is legitimate census work on exploration-classic under G-7 and is **not built here** — it is specified in Phase IV for the census lane, and its output goes to `research_outputs/census1d/`, **never** into `briefs/`, so live-computed and retrospectively-computed rows can never be joined by accident.

**The lockbox (2024-07-01 → 2025-10-06) stays sealed.** No layer of this build may read or compute over it.

## §II.4 Partition-footprint guard

Any historical or `--backfill` invocation must assert that the **full data footprint, including every warm-up window of every layer**, lies outside the sealed interval.

*Rationale, adopted verbatim from the ENGINE lane: **a rolling window is a silent lockbox-spending mechanism**. A trailing-window statistic extends an analysis's data footprint by the length of its window, and partition boundaries bind on the footprint, not the evaluation point. A 365-day rolling VWAP evaluated safely outside the seal can still read sealed bars through its warm-up. This applies equally to ATR percentile-vs-1y and the 20-day composite.*

Live forward operation is unaffected. **Fixture:** a synthetic invocation whose warm-up reaches into the interval must fail loudly.

## §II.5 Level registry and confluence engine

Levels: `{family, label, level, source_layer, timeframe}`.

**Families** — the VWAP family is split in two so one tool type cannot dominate diversity scoring:

- **`vwap_anchored`** — developing W/M/Q/Y **and prior M/Q/Y**, each with 1σ/2σ/3σ bands
- **`vwap_rolling`** — 7d/30d/90d/365d RVWAP, each with 1σ/2σ/3σ bands
- **`profile`** — POC/VAH/VAL for prior-day, 5d and 20d composites; naked-POC registry
- **`structure`** — pivot highs/lows (**confirmed only**), period opens, prior day/week/month extremes, session extremes
- **`ss`** — armed zone edges (Z1/Z2/Z3) and governor band edges per lens

**Density warning.** v1.1 ran 46–62 levels per asset. This roughly **doubles** it to ~110–125. Scores will inflate and the family cap becomes far more binding. Expected, not a fault — but every threshold below was calibrated against the *old* density and must be re-ratified from the calibration report (§II.8).

**Rules, printed in every capture; count-based, equal weights, never fitted (D9 discipline):**

1. Collapse same-family levels within **0.02 daily-ATR** into one member. *(This is where a July M ≡ Q anchor degeneracy merges instead of double-counting.)*
2. Cluster remaining levels within **0.15 daily-ATR** of the running cluster mean.
3. Score = Σ over families of min(members in family, **3**) + number of distinct families.
4. Lines in the sand = highest-scoring cluster within **1.5 daily-ATR** on each side of price; ties by proximity; fallback to the nearest cluster scoring ≥ 4.
5. **Sensitivity annex** — rankings also computed at tolerance 0.10 and 0.20 ATR; an **instability chip** prints when the top-3 changes between them. *An engine that cannot announce its own fragility is a machine for producing false confidence.*

## §II.6 Indicator layers

- **StochRSI** on {1h, 4h, 12h, 1d}: %K, %D, overbought/oversold state, cross events.
- **MACD** on {4h, 12h, 1d}: line, signal, histogram, zero-line side, signal-cross state, bars since.
- **Awesome Oscillator** on {4h, 12h, 1d}: value, zero-line side, saucer / twin-peak state.
- **Generalised divergence detector** applied to **RSI, MACD histogram and AO** on every timeframe, regular and hidden. Each divergence records the **price level of its pivot**, matched to the confluence area containing it — this is what turns *"is the same divergence printing on the AO, and is it landing where Secret Sauce has a level?"* into a computed line.
- **RVWAP cross-state layer** for pairs 7d×30d, 7d×90d, 30d×90d, 90d×365d: which is above, bars since last cross, spread in daily-ATR. Recorded as **state** into snapshots. *Recording is ops; whether crosses predict anything is a study question (Phase IV).*

> **Terminology note for Phase IV:** a rolling VWAP is **not** an EMA. It is a volume-weighted mean over a trailing time window — it responds to where volume traded, not merely where price went, and it has a hard window edge rather than exponential decay. That difference is exactly what makes the census question non-trivial.

## §II.7 Report structure — the operator's grammar

Masthead with verdicts → **actionable summary** (in-zone / watch / stand-aside, split by the positions file) → **confluence area maps** per asset (level strip + ranked table) → **lines in the sand** → **trade hypothesis drafts** (mechanically derived from the two lines and the next areas, if-then form, labelled **drafts**, **no sizing ever**) → radar → bias scorecard with every vote → momentum panel (RSI/StochRSI/MACD/AO + divergences + RVWAP cross states) → derivatives posture → calendar panel reserved for the reviewer → operator notes → provenance and firewall footer.

## §II.8 Calibration report — required deliverable

`_reviewer_box/BRIEF2_CALIBRATION.json` plus a short markdown summary:

1. Level count per asset, before (v1.1) and after, by family.
2. Cluster score distribution before and after: min / median / p90 / max, and how often the family cap binds.
3. Line-in-the-sand stability: how often the chosen lines change across tolerance 0.10 / 0.15 / 0.20, per asset.
4. Family composition of the top-3 areas per asset — specifically whether `vwap_rolling` now dominates, which would mean the family split did not go far enough.
5. The F-AN-11 one-pass vs two-pass variance discrepancy at real BTC price scales.

**Thresholds get re-ratified from this report.** Nobody defends them on intuition once real numbers exist.

## §II.9 Commands

| Command | Does |
|---|---|
| `/brief [--slot auto]` | Generate the capture, update the panel, auto-commit, report paths and headline lines |
| `/brief-render <date> [--slot]` | Rebuild HTML from a stored capture |
| `/brief-history …` | Archive search, extended with `--area-score`, `--divergence`, `--rvwap-cross`, `--slot` |
| `/brief-note "<text>"` | Timestamp an operator note into the current capture and commit |
| `/brief-panel` | Rebuild all three panel tables from captures |
| `/trade-log …` · `/trade-verify` | Phase III |

All command files use `C:\venvs\naiad\Scripts\python.exe`.

`ops/positions.yaml` — hand-maintained by the operator, **state only**: symbol, lens, direction, entry, stop. **No P&L, no outcomes, no history, ever** (firewall clause 2). A fixture asserts the schema contains no forbidden keys.

## §II.10 The twelve gap fixes

**G1** daily metrics anchor on the **last complete day**, today shown separately — removes the 3–6% ATR understatement and its leak into the weekly momentum vote · **G2** session decomposition reports the prior completed day **plus** today-so-far · **G3** every distance in both bps and daily-ATR · **G4** zone occupancy becomes an **orthogonal attribute**; the summary splits entry from add · **G5** ENTERED labelled machine-side unless `positions.yaml` says otherwise · **G6** actionability ranking printed in the rules header · **G7** coincident anchors print a degeneracy note · **G8** LIT first-kline timestamp printed **per interval** (ENGINE owns the ruling; the brief reports what it loaded) · **G9** per-rule POI slot budget replacing the global cap of 12 · **G10** approximation chips retained on profile layers · **G11** same-slot overwrite warning · **G12** **do not store an OHLC series** in the capture — at three captures a day it would dominate git growth (~250 MB/yr) duplicating the twice-backed-up kline estate; store only the window spec and let `brief_render.py` read the estate at render time. Charts degrade gracefully if the estate is absent; every computed number survives.

## §II.11 LIT known-wrong disclosure

Until the LIT estate remediation is separately authorised and executed, every capture and rendered report marks LITUSDT's **ATR-percentile, any rank field, and all bar-count fields** with a `known_wrong` flag and a one-line note.

**Measured basis** (ENGINE lane, verified there): the six LITUSDT kline stores begin exactly at `LIT_FLOOR_MS` = 2025-12-01T00:00:00Z and carry **40,832 rows of flat synthetic padding** — `open = high = low = close = 0.592`, `volume = 0.0`, zero rows with non-zero volume. **This is not another asset's price history.** Blast radius: ATR(14) **level** unchanged to five decimals (0.19983 both ways); ATR percentile-vs-1y moves 63.2 → 61.5 with 22 zero-true-range days entering the base; VWAP and volume-profile layers **unaffected**, because zero volume carries zero weight.

Therefore: mark percentile, rank and bar-count. **Do not mark levels or volume-weighted quantities** — over-marking is its own error.

**This contract does not authorise any estate change.** Do not delete parquet files. Do not edit `LIT_FLOOR_MS`.

## §II.12 Fixtures — Phase II

**F-B9** capture round-trip; `json_sha256` verified by binary re-read · **F-B10** render fidelity: `brief_render.py` reproduces byte-identical HTML modulo the render timestamp · **F-B11** registry traceability: every level names a source-layer field that exists in the capture; **zero orphans** · **F-B12** cluster conformance recomputed from the printed rules on all ten assets · **F-B13** sensitivity: rankings at 0.10/0.15/0.20 emitted; instability chip fires correctly · **F-B14** divergence symmetry: a synthetic constructed divergence detected on RSI, MACD-histogram **and** AO · **F-B15** no-sizing: zero keys matching `size|qty|quantity|notional|leverage|contracts` in capture, panel, positions file or HTML · **F-B16** firewall audit: no journal import, no outcome join, no lockbox read or statistic · **F-B17** closed-bar: every layer's newest input bar is **closed** at `as_of` · **F-B18** positions schema rejects forbidden keys · **F-B19** panel integrity: three tables rebuild from captures alone; grain is (asset, slot, date); levels and areas join back by key; `SCHEMA.md` documents every column present · **F-B20** Tier-2 fetch failures still render with degradation chips · **F-B21** backfill guard: a date earlier than the first capture is refused without `--backfill`; the override stamps a provenance marker · **F-B22** **schedule/DST**: resolving the three slots through `America/New_York` on a date after 2026-11-01 yields UTC times one hour later than today's — assert the generator uses zone resolution, not a stored offset · **F-B23** no capture contains a bar series (G12) · **F-B24** slot isolation: two captures on the same date with different slots coexist; neither overwrites the other; the index carries both.

## §II.13 Deliverables — Phase II

`scripts/daily_brief.py` (rebuilt on `analytics/`) · `scripts/brief_render.py` · `scripts/brief_panel.py` · `briefs/panel/SCHEMA.md` · `ops/brief_schedule.yaml` · `ops/positions.yaml.example` · extended `scripts/daily_routine.py` and `scripts/routine_jobs.json` · `scripts/setup_brief_schedule.ps1` (three tasks, timezone-aware, prints the next four DST transitions) · `.claude/commands/{brief,brief-render,brief-history,brief-note,brief-panel,trade-log,trade-verify}.md` · one real capture and all three panel tables · `_reviewer_box/BRIEF2_REPORT.json` · `_reviewer_box/BRIEF2_CALIBRATION.json`.

---

# PHASE III — FORWARD-0

## §III.1 What this is, and is not

A **diary**, not a scoreboard. It records what was intended, when, and on what basis, so that when a forward-validation hypothesis is eventually registered under **G-10** the record already has integrity instead of being reconstructed from memory.

**Prohibited until G-10 is separately ratified:** any aggregate, win rate, expectancy, P&L summary, "how did the flagged setups do", or any statistic whatsoever computed over the log. Fixture-enforced.

> **Renumber note.** The Forward Validation Protocol was drafted as G-9; **G-9 is already the ratified standing rule on relative fixture tolerances**, so it is renumbered **G-10** throughout. This rests on a cross-lane `[agent]`-tagged claim rather than a first-hand read of the G-register; it is cheap and reversible and the basis is recorded so the choice stays explicable.

## §III.2 Log structure

`ops/forward_log.jsonl` — tracked, append-only, one JSON object per line:

```
{ id, ts_utc, kind, symbol, lens, direction, trigger, entry_level, stop_level,
  targets[], brief_date, brief_slot, brief_json_sha256, rules_version,
  analytics_version, note, status, exit_ts_utc, exit_level, exit_reason,
  prev_sha256, entry_sha256 }
```

`kind` ∈ `mechanical` | `hypothetical` | `actual` — strictly separated, never mixed in any later sample.

**Hash chain.** `entry_sha256 = sha256(canonical_json(entry_without_own_sha) + prev_sha256)`. Any retroactive edit breaks the chain from that point forward and `/trade-verify` finds it. *This is what makes "I recorded this before I knew the outcome" credible — including to yourself, which is the harder audience.*

Exits are recorded as status transitions on the same entry. **Recording an exit is diary-keeping; aggregating exits is a statistic.** The line sits exactly there.

## §III.3 Fixtures — Phase III

**F-F1** chain integrity: a deliberately mutated line is detected · **F-F2** append-only: rewriting history is refused · **F-F3** no aggregation: source scan proves no statistical function is applied to log data · **F-F4** kind isolation: no code path mixes kinds · **F-F5** capture linkage: every entry's `brief_json_sha256` matches an existing capture.

---

# PHASE IV — HANDOFF SPEC ONLY, NOT BUILT

**CENSUS-1d** (confluence matrix over exploration-classic, as-of correct, joined to census signals) and **H-RVX** (do RVWAP crosses confluence with the Secret Sauce EMA crosses) are specified in the BRIEF lane's handoff to the census lane. **Do not implement either here.** If any part of Phases 0–III would incidentally read historical data outside its current trailing windows, **halt and ask**.

Two corrections carried from the ENGINE lane's reply, to be reflected wherever this contract's text touches study framing:

- **"CENSUS-1c" is an occupied phase slot.** The proposal is renamed **CENSUS-1d**, pending the operator's ruling on folding it into CENSUS-2/CCL instead.
- **Exploration-classic is a FIVE-asset panel** — BTC, ETH, ZEC, SOL, NEAR — with two thin annexes (JTO 205 days, TAO 80) and three assets at **zero** scorable days (FARTCOIN, HYPE, LIT). **The brief watches ten assets; the study can score five.** Any text implying a ten-asset scorable basket is wrong.

**As-of invariant** (replacing an earlier, over-strong reviewer formulation that conflated *causal* with *streaming* and would have discarded proven causal machinery):

> **Every emitted value must be reproducible from a build whose data ends at that value's decision timestamp.**

Vectorised implementations are acceptable when causal by construction. Streaming is mandated **only** for the clustering/scoring layer, where no as-of predicate exists.

---

## §X VERDICT

**PASS** = F-AN-1..14, F-B9..24 and F-F1..5 all pass · the sample capture renders every section for all ten assets · the three panel tables build and `SCHEMA.md` documents every column · the parity worksheet is emitted with our values populated · the calibration report is present · all reports in `_reviewer_box/` · the reviewer independently reproduces confluence scores and lines in the sand for at least three assets from the capture alone. Any FAIL → halt, report, **no partial adoption**.

**ADOPTION is a separate gate from PASS.** The toolbox is not trusted until the operator's parity readings return and match. A PASS with unreturned parity means the plumbing works, not that the numbers are right.

## §Y WHAT THIS IS NOT

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or implied. No engine change. No forward scoring. No lockbox read. No estate mutation. Confluence scores are agreement measurements, not predictions. Every threshold — 0.02 / 0.15 / 1.5 ATR, family cap 3, POI budgets, divergence pivot depth, slot times — is a v1 placeholder to be re-ratified against the calibration report and roughly a week of live use.

## §Z LEDGER ENTRY

Append verbatim on completion, then add a completion bullet with fixture results, paths, sizes, the calibration headline, runtime per phase and the commit hash:

> **## 2026-07-28 — ANALYTICS-1 + BRIEF-2 + FORWARD-0 (contract v4)**
> - Consolidated contract v4 supersedes v3 and its Amendment 1, neither of which was executed. Ratified by operator interviews D-B9..D-B29 and Groups A–D.
> - `analytics/` created **outside** `engine/`: versioned, hashed, pure-computation, no I/O, no engine imports. Rolling-VWAP algorithm **pinned from source** (operator-supplied TradingView RVWAP Pine v5): time-based millisecond window with a 10-bar floor; variance = max(Σ(vol·src²)/Σvol − VWAP², 0), volume-weighted **population** form with no (n−1) correction; the zero-clamp is algorithmic. The reviewer's earlier prose spec ("standard deviation of typical price") would have produced plausible numbers that never matched the operator's chart — caught before build and logged as a reviewer spec error.
> - **Causality classes** (`causal` / `lag:N` / `endpoint_only`) plus **F-AN-13 truncation-prefix** installed to catch the one-sided-window hazard class the ENGINE lane reported in `daily_brief.py` — safe today only by caller contract, and converted by extraction into an unguarded bug. Neither lane located the instance; the fixture finds all of them.
> - BRIEF-2: confluence engine (registry → 0.02 same-family collapse → 0.15 ATR clustering → count+diversity scoring → lines in the sand → mechanical if-then drafts); `vwap` family **split** into anchored/rolling because the registry roughly doubles to ~110–125 levels per asset; sensitivity annex at 0.10/0.20 with an instability chip; MACD + StochRSI + AO with generalised divergences; RVWAP cross-state layer; **three session-anchored captures** via the existing `daily_routine.py` extended with `--slot` (one runner, three triggers — no second scheduler); tracked `briefs/` archive plus a three-table panel at grain (asset, slot, date) with `SCHEMA.md`; twelve gap fixes.
> - **Partition-footprint guard** adopted from the ENGINE lane: *a rolling window is a silent lockbox-spending mechanism* — warm-ups extend an analysis's data footprint and partition bounds bind on the footprint, not the evaluation point.
> - **Standing rules adopted (Group D):** repo-root discipline (contracts to `prompts/`, handoffs to `docs/handoffs/`), and an archive-dependency audit (`docs/ARCHIVE_DEPENDENCIES.md`) required before any phase directory is archived — after the 2026-07-27 reclamation cost two retrievals.
> - **Google Drive correction:** `G:\My Drive\naiad-backups` **does** exist; the 2026-07-28 setup task's "no Drive on this machine" finding was a probe artifact. `backup_estate.py` (built at `837c635`, F-K1..7 pass) should carry `briefs/` in scope — reported, not edited, since it belongs to another lane.
> - **LIT disclosure:** percentile, rank and bar-count fields marked `known_wrong` pending estate remediation. Levels and volume-weighted quantities explicitly **not** marked. No estate change authorised or made here.
> - Forward Validation Protocol renumbered **G-9 → G-10** (G-9 is the ratified fixture-tolerance rule); basis is a cross-lane `[agent]` claim and is recorded as such.
> - Reviewer: Claude (Fable-mode), BRIEF lane. Operator: ratified by routed paste.
