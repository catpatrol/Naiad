# CONTRACT — ANALYTICS-1 · BRIEF-2 · FORWARD-0
### Naiad BRIEF lane · drafted 2026-07-27 by reviewer (Fable-mode) · DRAFT — not yet issued to builder
### Every clause marked `[DEFAULT]` is a reviewer choice the operator may veto. Decision register at §Z.

---

## §0 What this is

One contract, three parts, executed as a decision tree that runs start-to-finish and halts only on a fixture failure or a genuine fork.

- **PART I — ANALYTICS-1.** Extract every indicator recipe out of the 2,760-line brief script into a small, versioned, tracked toolbox that the brief, future census work and any later tool can all import. Add the recipes we lack (StochRSI, Awesome Oscillator, a generalised divergence detector, the level-clustering engine). Emit a parity worksheet so the operator can certify the numbers against his own TradingView charts.
- **PART II — BRIEF-2.** Rebuild the daily brief on top of that toolbox in the operator's own grammar: levels → confluence areas → lines in the sand → if-then trade hypotheses. Migrate storage to a tracked, self-describing archive. Fix the twelve defects found in v1 acceptance. Add the notes, positions, render and export commands.
- **PART III — FORWARD-0.** Scaffolding only for virtual trading: a hash-chained, append-only diary of intended and hypothetical trades. **No scoring, no aggregation, no statistics of any kind** until the G-9 protocol at §G is separately ratified.

Tier: OPS. No Tier-C is created or implied. No engine module is modified.

---

## §1 Governing rules (read before anything else)

1. **The firewall, all four clauses, unchanged and re-printed in every artifact.** (i) Live data is operations-only and forbidden as study evidence; rules are born only under G-7 on exploration-classic data. (ii) No journal reads; no signal-outcome or trade-outcome statistics on any window. (iii) Engine modules imported read-only with trading disabled; `signals.py`, `trading.py`, `cells.py`, `replay.py`, `htf.py`, `indicators.py`, `cells.py` and every config are **not modified**. (iv) The archive may be mined for hypotheses; it is never a scoring window.
2. **Confluence scores describe agreement between tools, not validated edge.** Nothing in Part II may be phrased as predictive. Whether confluence areas carry edge is a study question (CCL / CENSUS-2) answerable only under G-7.
3. **`analytics/` lives OUTSIDE `engine/`.** Engine files are frozen, their hashes are cited in ledger entries and fixtures; ops iteration must never share a blast radius with study-critical code.
4. **Standing rules apply:** completion commits contain every file needed to reproduce from a clean checkout; commit, never push; halt and ask one precise question rather than improvise; environment assertion first, before any read or write.
5. **Machine-readable handback.** Every phase writes its report into `_reviewer_box/` as a file. No terminal screenshots.

---

# PART I — ANALYTICS-1

## §I.1 Purpose and placement

A pure-computation toolbox at repo root: `analytics/`. Tracked, versioned, importable by anything. It contains recipes only — arithmetic on arrays — and knows nothing about files, networks, the engine, or the brief.

## §I.2 Package layout `[DEFAULT — D-B17]`

```
analytics/
  __init__.py        ANALYTICS_VERSION, CONVENTIONS dict, analytics_sha()
  momentum.py        rsi, stoch_rsi, awesome_oscillator, ema, sma, divergences
  vwap.py            rolling_vwap, anchored_vwap, sigma_bands
  volatility.py      true_range, atr, realised_vol, percentile_rank
  profile.py         volume_profile (POC/VAH/VAL), naked_poc_registry
  structure.py       pivots, period_opens, prior_period_extremes
  levels.py          LevelRegistry, collapse_same_family, cluster, score, lines_in_sand
  stats.py           beta, correlation, zscore
  parity.py          worksheet generation
```

## §I.3 Invariants (each is a fixture)

- **I-A No I/O.** No `open(`, no `read_parquet`, no `requests`, no `urllib`, no filesystem or network access anywhere in the package.
- **I-B No engine imports.** No `from engine` / `import engine` anywhere.
- **I-C Deterministic.** Same input, same output, bit-for-bit, across runs.
- **I-D Warm-up honesty.** Values that cannot yet be computed return `NaN`, never a silently seeded number. Every function documents how many bars it needs.
- **I-E Convention printed.** `CONVENTIONS` is a dict naming the exact variant of every recipe (see §I.4). Any artifact using the package prints `ANALYTICS_VERSION` and the `analytics_sha()`.
- **I-F Semantic versioning.** Any change to a returned number bumps the minor version at minimum. Archive comparability depends on it.

## §I.4 Conventions to pin — the variant problem `[DEFAULT — D-B17/D-B18]`

Most indicators have several defensible definitions. A "correct" implementation of the wrong variant produces numbers that never match the operator's chart, which silently destroys trust. These are pinned to TradingView defaults and recorded in `CONVENTIONS`:

| Recipe | Pinned convention |
|---|---|
| RSI | length 14, **Wilder (RMA) smoothing**, source = close |
| StochRSI | RSI length 14, Stoch length 14, %K smooth 3, %D smooth 3, source = close |
| Awesome Oscillator | SMA(5) − SMA(34) of the **bar midpoint** (H+L)/2 |
| ATR | length 14, **Wilder smoothing**, true range = max(H−L, |H−C₋₁|, |L−C₋₁|) |
| VWAP (all) | typical price (H+L+C)/3, volume-weighted, computed on **1h klines** |
| VWAP σ bands | **standard deviation of typical price about the running VWAP**, volume-weighted (TradingView's "Standard Deviation" band mode, not the percentage mode) |
| Pivots | pivot(5,5) — five bars either side, matching census convention |
| Divergence | pivots(5,5) on both price and oscillator; last 2 pivot pairs per timeframe; regular = price extreme extends while oscillator does not; hidden = the converse |
| Realised vol | close-to-close log returns, 7d vs 30d ratio, annualisation not applied |
| Percentile rank | rank of the current value among the trailing sample, expressed 0–100, sample size printed |

## §I.5 Parity harness — the trust gate

`analytics/parity.py` + `scripts/parity_worksheet.py` emit `_reviewer_box/parity_worksheet_YYYY-MM-DD.md`: a table the operator fills in from his own charts, one row per reading.

Each row prints: **TradingView symbol string** (e.g. `BINANCE:BTCUSDT.P` `[DEFAULT — D-B18]`), timeframe, the **candle's open time in UTC**, the indicator with its full settings, **our computed value**, and an empty column for the operator's reading.

The worksheet opens with plain-language instructions: set the chart timezone to UTC, use the perpetual contract not spot, hover the named candle, read the indicator pane. Readings are taken on **closed** candles only.

Default worksheet `[DEFAULT — D-B19]`: 17 readings — RSI on BTC/ETH/SOL × 1h/4h/1d (9); StochRSI %K on BTC × 1h/4h/1d (3); AO on BTC × 4h/1d (2); ATR(14) on BTC 1d (1); anchored month-VWAP on BTC (1); anchored quarter-VWAP on ETH (1). Two of the RSI rows are drawn from ~30 days back to catch warm-up drift rather than only testing the newest bar.

**Known limitation, stated up front:** TradingView ships anchored/session VWAP but not rolling N-day VWAP. Rolling 7/30/90/365d VWAP is therefore **not parity-checkable** against stock TradingView `[D-B20]`. It is certified instead by arithmetic fixtures plus internal consistency, and the worksheet says so rather than pretending otherwise.

Acceptance rule: a reading matches if it agrees to the precision TradingView displays. Any mismatch halts adoption of that recipe and is reported, not patched around.

## §I.6 Fixtures — Part I

- **F-AN-1 Golden values.** Small hand-checkable input arrays with independently derived expected outputs for RSI, StochRSI, AO, ATR, VWAP, pivots. Assert equality to 1e-9.
- **F-AN-2 Determinism.** Every public function called twice on identical input returns bit-identical results.
- **F-AN-3 No engine imports.** Source scan of the whole package proves zero engine imports.
- **F-AN-4 No I/O.** Source scan proves no file, network or environment access (excluding `parity.py`'s string generation, which returns text and does not write).
- **F-AN-5 Version hash.** `analytics_sha()` equals a fresh recomputation over the package's source files, via Python `hashlib` on binary reads.
- **F-AN-6 Warm-up.** Each function returns `NaN` for exactly its documented warm-up length and a finite number immediately after.
- **F-AN-7 Edge cases.** Flat series (zero price change), zero-volume bars, and series shorter than the warm-up all behave as documented rather than raising or returning garbage.
- **F-AN-8 Brief equivalence.** For every recipe the current `daily_brief.py` already computes, the new package reproduces the v1.1 published values on the frozen fixture day to 1e-9. **This is the regression guard**: the refactor must not silently change any number that has already been accepted.
- **F-AN-9 Cluster reproducibility.** Given a fixed level registry, clustering and scoring reproduce exactly; scores recompute from their own member lists.

## §I.7 Deliverables — Part I

`analytics/` package · `tests/test_analytics.py` · `scripts/parity_worksheet.py` · `_reviewer_box/parity_worksheet_YYYY-MM-DD.md` · `_reviewer_box/ANALYTICS1_REPORT.json` (fixture results, version, sha, per-function warm-up lengths, F-AN-8 diff table).

---

# PART II — BRIEF-2

## §II.1 Storage migration `[ratified D-B9/D-B10]`

- New **tracked** folder `briefs/`. Daily capture at `briefs/brief_YYYY-MM-DD.json`; index appended at `briefs/index.jsonl`.
- `research_outputs/brief/` keeps HTML only, remains untracked. `.gitignore` uses **pattern-based** rules (`briefs/*.html`), never a directory exclusion — git cannot re-include a file inside an ignored directory.
- Every capture embeds: `schema_version`, `rules_version`, `rules_sha256`, `analytics_version`, `analytics_sha`, `engine_version`, the complete rule set, and every input's `last_bar_utc`.
- `/brief` **auto-commits** its capture with a fixed message (`ops: brief capture YYYY-MM-DD`). It never pushes.
- Same-date re-run: warns, shows what would be replaced, and requires confirmation `[DEFAULT]`.
- `scripts/brief_render.py --date YYYY-MM-DD` regenerates the HTML from any stored capture. This is what makes HTML disposable.
- `scripts/brief_export.py` writes a flat panel (`briefs/export/panel.parquet`) — one row per asset per day, all scalar fields, stable column names — so months of captures load in one line for later analysis `[DEFAULT — D-B25]`.

## §II.2 Level registry and confluence engine `[DEFAULT — D-B21]`

Every layer emits levels into a registry: `{family, label, level, source_layer, timeframe}`.

Families and members:
- **vwap** — anchored developing W/M/Q/Y **and prior M/Q/Y**, each with **1σ/2σ/3σ** bands (ratified D-B11); rolling 7/30/90/365d.
- **profile** — POC/VAH/VAL of prior-day, 5d and 20d composites; naked-POC registry.
- **structure** — pivot highs/lows, period opens, prior day/week/month extremes, session extremes.
- **ss** — armed zone edges (Z1/Z2/Z3) and governor band edges per lens.

Then, per printed rule:
1. **Collapse** same-family levels within **0.02 daily-ATR** into one member (this is where the July M≡Q anchor degeneracy merges instead of double-counting).
2. **Cluster** all remaining levels within **0.15 daily-ATR** of the running cluster mean.
3. **Score** = Σ min(members per family, **3**) + number of distinct families. Count-based, equal weights, **never fitted** (D9 discipline).
4. **Lines in the sand** = the highest-scoring cluster within **1.5 daily-ATR** on each side of price, ties broken by proximity; fallback to nearest cluster scoring ≥ 4.
5. **Sensitivity annex** — the capture also stores rankings at tolerance 0.10 and 0.20 ATR. If the top-3 ranking is unstable across tolerances, the report prints an instability chip. A fragile engine must announce its own fragility.

## §II.3 New indicator layers

- **StochRSI** on {1h, 4h, 12h, 1d}: %K, %D, overbought/oversold state, cross events.
- **Awesome Oscillator** on {4h, 12h, 1d}: value, zero-line side, saucer/twin-peak state.
- **Generalised divergence detector** — the same detector applied to RSI *and* AO on every timeframe, regular and hidden. Each divergence records the **price level of its pivot**, which is then matched to the confluence area containing it. This is what makes "is the same divergence printing on the AO, and is it landing where Secret Sauce has a level?" a computed line rather than an eyeball question.

## §II.4 Report structure — the operator's grammar

Sections, in order: masthead with verdicts → **actionable summary** (in-zone / watch / stand-aside, split by the positions file) → **confluence area maps** per asset with the level strip and the ranked table → **lines in the sand** → **trade hypothesis drafts** (mechanically derived from the two lines and the next areas, in if-then form, explicitly labelled drafts, **no sizing, ever**) → radar → bias scorecard with every vote → derivatives posture → calendar panel reserved for the reviewer → operator notes → provenance and firewall footer.

## §II.5 Commands

| Command | Does |
|---|---|
| `/brief` | Generate today's capture, auto-commit, report paths + headline lines |
| `/brief-render <date>` | Rebuild any archived day's HTML from its capture |
| `/brief-history …` | Existing archive search, extended with `--area-score`, `--divergence` |
| `/brief-note "<text>"` | Timestamp an operator note into today's capture and commit |
| `/brief-export` | Write the flat panel |
| `/trade-log …` | Part III — append a forward-log entry |
| `/trade-verify` | Part III — verify the hash chain |

`ops/positions.yaml` — hand-maintained by the operator, state only: symbol, lens, direction, entry, stop. **No P&L, no outcomes, no history — ever** (firewall clause ii). A fixture asserts the file's schema contains no forbidden keys.

## §II.6 The twelve accepted gap fixes

**G1** daily metrics anchor on the last *complete* day (today shown separately) — removes the 3–6% ATR understatement and the leak into the weekly momentum vote · **G2** session decomposition reports the prior completed day plus today-so-far · **G3** every distance prints in both bps and daily-ATR · **G4** zone occupancy becomes an orthogonal attribute; the summary splits entry from add · **G5** ENTERED labelled machine-side unless the positions file says otherwise · **G6** the actionability ranking is printed in the rules header · **G7** coincident anchors print a degeneracy note · **G8** LIT first-kline timestamps printed per interval (ENGINE owns the ruling; the brief simply reports what it loaded) · **G9** per-rule POI slot budget replacing the global cap of 12 · **G10** approximation chips retained on profile layers · **G11** same-date overwrite warning · **G12** a compact OHLC series (last 96 hourly bars per asset) stored in the capture so charts and sparklines become possible.

## §II.7 Fixtures — Part II

**F-B9** capture round-trip: index line rebuilds from the JSON alone; `json_sha256` verified by binary re-read · **F-B10** render fidelity: `brief_render.py` on the stored capture reproduces a byte-identical HTML modulo the render timestamp · **F-B11** registry traceability: every level in the registry names a source layer field that exists in the capture; zero orphans · **F-B12** cluster conformance: recompute scores and lines in the sand from the printed rules; assert equality on all 10 assets · **F-B13** sensitivity: rankings emitted at 0.10/0.15/0.20; instability chip fires when the top-3 changes · **F-B14** divergence symmetry: a synthetic series with a constructed divergence is detected on both RSI and AO · **F-B15** no-sizing: zero keys matching `size|qty|notional|leverage|contracts` anywhere in capture, positions file or HTML · **F-B16** firewall audit: source scan proves no journal import, no outcome join, no lockbox statistic · **F-B17** closed-bar: every layer's newest input bar is closed at `as_of`; assert no forming bar enters any computation · **F-B18** positions schema: forbidden keys rejected · **F-B19** export panel: column set stable and documented; row count = assets × days · **F-B20** degradation: Tier-2 fetch failures still render with chips.

## §II.8 Deliverables — Part II

`scripts/daily_brief.py` (rebuilt on `analytics/`) · `scripts/brief_render.py` · `scripts/brief_export.py` · `.claude/commands/{brief,brief-render,brief-history,brief-note,brief-export}.md` · `ops/positions.yaml.example` · updated `scripts/setup_brief_schedule.ps1` for **14:00 UTC** (11:00 Buenos Aires, ratified D-B15) · one real capture generated · `_reviewer_box/BRIEF2_REPORT.json`.

---

# PART III — FORWARD-0 (scaffolding only)

## §III.1 What this is, and emphatically is not

A **diary**, not a scoreboard. It records what was intended, when, and on what basis — nothing more. It exists now so that when a forward-validation hypothesis is eventually registered under §G, the record already has integrity rather than being reconstructed from memory.

**Prohibited until G-9 is separately ratified:** any aggregate, any win rate, any expectancy, any P&L summary, any "how did the flagged setups do", any statistic over the log whatsoever. A fixture enforces this by scanning for aggregation functions over log data.

## §III.2 Log structure

`ops/forward_log.jsonl` — tracked, append-only, one JSON object per line:

```
{ id, ts_utc, kind, symbol, lens, direction, trigger, entry_level, stop_level,
  targets[], brief_date, brief_json_sha256, rules_version, analytics_version,
  note, status, exit_ts_utc, exit_level, exit_reason, prev_sha256, entry_sha256 }
```

`kind` ∈ `mechanical` | `hypothetical` | `actual` `[DEFAULT — D-B22/D-B23]` — strictly separated, never mixed in any later sample.

**Hash chain.** `entry_sha256 = sha256(canonical_json(entry_without_own_sha) + prev_sha256)`. Any retroactive edit breaks the chain from that point forward and `/trade-verify` finds it. This is what makes "I recorded this before I knew the outcome" credible — including to yourself.

Exits are recorded as status transitions on the same entry. **Recording an exit is diary-keeping; aggregating exits is a statistic.** The line sits exactly there.

## §III.3 Fixtures — Part III

**F-F1** chain integrity: a deliberately mutated line is detected · **F-F2** append-only: rewriting history is refused · **F-F3** no aggregation: source scan proves no statistical function is applied to log data · **F-F4** kind isolation: no code path mixes kinds · **F-F5** capture linkage: every entry's `brief_json_sha256` matches an existing capture.

---

## §G  G-9 — Forward Validation Protocol (charter amendment, ratified separately, NOT built here)

Forward data may become evidence only under a written registration made **before the first qualifying entry**:

1. **Registration** states the hypothesis, the exact mechanical qualifying rule, the sample size **N**, the pre-committed statistic, the stopping rule, and the falsification criterion. Committed with a sha and logged in `LEDGER.md`.
2. **Log integrity** verified by `/trade-verify` at registration and at scoring.
3. **No mid-flight changes.** Altering the rule voids the sample and starts a new registration.
4. **No peeking.** Aggregate statistics are computed **once, at N** — never continuously. Interim looks void the sample. (Optional stopping is the most common way honest people fool themselves with forward data.)
5. **Kind isolation.** Only `mechanical` entries enter a mechanical sample. Discretionary and hypothetical entries are never mixed in.
6. **Falsification is a deliverable**, on the same terms as every other Naiad phase.

Rationale worth stating plainly: forward validation is the *strongest* evidence available anywhere in this project, because the data genuinely does not exist yet and cannot be peeked at. That strength is entirely destroyed by rule-drift or by looking early. The protocol is strict precisely because the prize is large.

---

## §X Verdict criteria

**PASS** = all F-AN-1..9 and F-B9..20 pass (and F-F1..5 if Part III is included) · the sample capture renders every section for all ten assets · the parity worksheet is emitted with our values populated · `_reviewer_box/` contains all three reports · reviewer independently reproduces the confluence scores and lines in the sand for at least three assets from the capture alone. Any FAIL → halt, report, no partial adoption.

**ADOPTION** is a separate gate from PASS: the toolbox is not trusted until the operator's parity readings are returned and matched.

## §Y What this phase is not

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or implied. No engine change. No forward scoring. Confluence scores are agreement measurements, not predictions. All thresholds (0.02 / 0.15 / 1.5 ATR, family cap 3, POI budgets) are v1 placeholders expected to be re-ratified after roughly a week of live use.

## §Z Decision register

| # | Decision | Default |
|---|---|---|
| D-B17 | Indicator scope for the toolbox | RSI, StochRSI, AO, VWAP complex, ATR/RV, pivots, levels/clustering, beta — no MACD/Bollinger/Keltner in v1 |
| D-B18 | Canonical TradingView chart for parity | `BINANCE:<SYM>USDT.P` (perpetual), chart timezone UTC |
| D-B19 | Parity worksheet size | 17 readings across BTC/ETH/SOL |
| D-B20 | Rolling-VWAP parity | Not checkable on stock TV; certified by arithmetic + consistency |
| D-B21 | Confluence parameters | collapse 0.02 · tolerance 0.15 · family cap 3 · LIS window 1.5 ATR · sensitivity annex |
| D-B22 | Forward-log scope | manual + mechanical, strictly tagged |
| D-B23 | Log actual trades too | yes, `kind=actual`, never aggregated |
| D-B24 | G-9 timing | scaffolding now, ratify G-9 when a real hypothesis exists |
| D-B25 | Data-mining interpretation | stable schema + flat panel export |
| D-B26 | Sequencing | Parts I+II in one paste; Part III after D-B22/23/24 |
