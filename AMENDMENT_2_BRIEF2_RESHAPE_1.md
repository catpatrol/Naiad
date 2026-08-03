# AMENDMENT 2 to CONTRACT v4 — BRIEF-2 RESHAPE
### Naiad · ARGUS lane · drafted 2026-08-02 · supersedes CONTRACT v4 Phase II where they conflict
### Ratified inputs: interviews ARGUS-BRIEF-1 (A-1..A-6) and ARGUS-VOLF-1 (B-1..B-10), gates G-1..G-3, operator comments as rulings, 2026-08-02

---

## §0 · What this amends, and what it does not

CONTRACT v4 specified Phase II (BRIEF-2) before the volume filter was commissioned and before the two-stage report was ruled. This amendment **replaces v4 §II in full**. It does not touch:

- **v4 Phase I (ANALYTICS-1)** — complete, 41/41, commit `c1d8e66`, `analytics` v1.1.0 — except for the remediation in §1 below.
- **v4 Phase III (FORWARD-0)** — the trade diary, unchanged, still builds last.
- **v4 Phase IV** — handoff specs only, still not built here.
- **The firewall, all four clauses.** Unchanged, reprinted in every artifact.

**Adoption is unchanged and absolute:** nothing consumes `analytics/` numbers until the fixtures are green *and* the operator's parity readings match. This amendment may be **built** before parity returns; its output may not be **trusted** until parity returns. The two are separate gates and the build must say so on every render until the gate clears.

---

## §1 · PHASE I-R — causality remediation (builds first, before anything in §2+)

The builder's own audit found **five public functions outside the F-AN-13 truncation-prefix discipline**, two more than the reviewer identified. F-AN-13 exists to abolish caller-contract dependencies; five escapes is a hole in the instrument that the confluence engine is about to depend on.

### §1.1 Close the five gaps

| function | location | current state | required |
|---|---|---|---|
| `vw_sigma_bands` | `vwap.py:133` | untested, referenced nowhere | truncation-tested |
| `divergences` | `momentum.py:119` | untested, declared `lag:5` | tested **at lag**, both regular and hidden |
| `naked_poc_registry` | `profile.py:82` | untested | see §1.2 — classify first |
| `confirmed_pivots` | `structure.py:161` | F-AN-12 only | truncation-tested |
| `resample_ohlcv` | `structure.py:48` | F-AN-14/14b/14c only | truncation-tested |

`vw_sigma_bands` and `divergences` are the consequential pair: sigma bands feed the level registry the confluence engine scores on, and divergences are a headline feature of the commissioned report. An untested divergence detector that peeked at future pivots would produce beautiful, worthless signals.

**Fixture `F-AN-13b`:** extend the truncation-prefix parametrisation to cover all five. Dict- and list-returning functions are covered element-wise: for each returned array or record keyed by index, the prefix rule holds. `naked_poc_registry` returns a list of dicts, so the assertion is *set-membership stability* — the registry computed on `x[:k]` must equal the registry computed on `x` filtered to entries decided at or before `k−1`.

### §1.2 Rule F-2 — the undecidable branch

**Confirmed by the builder:** closure is decided by **time, not bar count** (`structure.py:45`) — a day missing five mid-session bars but holding its final bar is kept (19/24 → kept); a day missing only its last bar is dropped (23/24 → dropped). That rule is correct and stands.

But "undecidable" (`infer_step_ms` returns `None`, on fewer than 2 timestamps or all-identical stamps) currently **keeps** the bucket, and a single 1h bar handed to a 1d resample returns a "day" holding 1/24 of a day. The builder's own words: *the safety of the undecidable branch currently rests on callers, not on the function.*

**RULING: raise, do not keep.** `resample_ohlcv` raises a clear, named exception when step inference fails. Rationale: this amendment's founding lesson is that a forming bucket must never reach a published number; under uncertainty the safe default is to refuse, not to guess. A function whose safety depends on how it is called is exactly the hazard class F-AN-13 was installed to abolish, and it must not survive in the one function this whole correction was about.

**Cost, verified by the builder:** only the fixture asserting current behaviour changes. `scripts/parity_worksheet.py:92,96` passes ≥400 closed 1h bars — never undecidable. `daily_brief.py` does not call it. **No production caller changes behaviour.**

`test_f_an_14c` is rewritten to assert the raise. `CONVENTIONS` records the new contract.

### §1.3 Gate

**Phase I-R must be green before any §2+ work begins.** If any of the five newly-covered functions *fails* truncation testing, that is a **finding**: report the function, module and mechanism, halt, and do not fix it silently. A causality failure in `divergences` or `vw_sigma_bands` would invalidate design assumptions in §4 and §5.

---

## §2 · THE REPORT — two stages, both printed (ratified A-1)

The operator ruled explicitly: **print both.** He cannot judge the decision instrument without seeing the monitor it was distilled from, and trimming later is cheap while rebuilding later is not.

### §2.1 Part I — Market Monitor (generous by design)

Everything v1.1 printed, plus the new layers, presented for **reading and judgement** rather than for action. Per-asset: structure, windowed volume profiles, the VWAP complex, the momentum suite, volatility regime, funding and OI posture, sessions, BTC beta, the Secret Sauce governor dashboard, and the **full bias scorecard with every vote** (ratified A-4: keep it, be generous, tune later — it is too early to know whether it works).

Part I answers: *what is the state of this market?*

### §2.2 Part II — Decision Instrument

Derived from Part I under printed rules. Per asset, in order:

1. **Confluence area map** — the ranked level registry (§5).
2. **Lines in the sand** — the two decisive levels.
3. **Trade hypothesis drafts** — if-then form, mechanically derived (§7.1).
4. **R:R ranking** — the board sorted by structural quality (§7.2).
5. **Composite bias print** — counted, with dissent named (§7.3).

Part II answers: *where would I act, and what would prove me wrong?*

**Sequencing rule:** Part II must be derivable from Part I's printed numbers alone. No hidden inputs. A reader with Part I and the rules header must be able to reconstruct Part II by hand. This is what keeps the "intelligence" auditable rather than oracular.

### §2.3 Cadence (ratified A-3)

Both parts render at all three session-anchored slots — `london` 12:00 UTC, `ny_am` 15:00 UTC, `post_ny` 21:30 UTC, times held in `America/New_York` — **and** on command at any time. Uniform captures; no second species of artifact.

---

## §3 · THE VOLUME FILTER — objects and construction

### §3.1 What the windows are (ratified B-1, B-2)

**Trailing**, not anchored: the last N days, recomputed each capture, sliding forward with the clock. Confirmed against the operator's TradingView screenshots.

**These are not the parked composites of D-B12.** A judgment-merged composite encodes a decision about which balance areas belong together; a trailing window encodes a clock. The parked object stays parked. This distinction is recorded so the record cannot later read as self-contradictory.

**One vocabulary everywhere:** `{prior-day, 7d, 30d, 90d, 365d}` for both rolling VWAPs and windowed volume profiles. The v1.1 5d and 20d windows are **retired** — they near-duplicated 7d and 30d, and in a system that scores by counting agreement, near-duplicates inflate scores while adding nothing.

### §3.2 Rolling VWAP (pinned, unchanged from v4 §I.4)

TradingView's published algorithm, pinned from source: trailing millisecond window floored at 10 bars; `src = hlc3`; volume-weighted **population** variance via the one-pass identity `max(Σ(vol·src²)/Σvol − VWAP², 0)`, no (n−1) correction, zero-clamp algorithmic. Bands at **1σ / 2σ / 3σ** on all four windows (the operator: *"the key is executing the rvwap with std's on the 7, 30, 90 and 365 day"*).

**Warm-up honesty:** the 365-day window needs a year of data before its first honest value. Any asset without it prints a `warming` chip rather than a number. This is not optional — a 365d VWAP computed on 200 days is a 200-day VWAP wearing the wrong label.

### §3.3 Windowed volume profiles (ratified B-3 bundle)

| knob | value | why |
|---|---|---|
| slicing | **120 rows** across each window's range | adapts per asset; fine enough to resolve shelves, coarse enough to smooth noise |
| value area | **70%** of window volume | the near-universal standard and TradingView's default |
| substrate | **1m** for 7d · **5m** for 30d · **15m** for 90d and 365d | precision where short-window levels need it; broad structure elsewhere without ballooning compute |

All three printed in every capture. The `approximation` provenance chip is retained and non-removable: volume is spread uniformly across each candle's range, which is an approximation of tick data.

Each window emits **POC, VAH, VAL**, plus **LVNs** (§3.4).

### §3.4 Low-volume nodes (ratified B-6)

An LVN is a price shelf where the window's volume histogram is near-empty — the market moved through without doing business, and such gaps tend to be revisited. This is the mechanical equivalent of the "single print from April 13th" class of level the operator's manual reviews lean on.

**Definition, printed:** a contiguous run of profile rows whose volume is below `lvn_threshold` × the window's median row volume, at least `lvn_min_rows` wide, lying **inside** the window's traded range (not at its extremes). v1 defaults: `lvn_threshold = 0.25`, `lvn_min_rows = 3` — placeholders, re-ratified after a week of use. Each LVN emits its **midpoint** as a level and its **edges** as a band.

TPO single prints and judgment-composites remain parked.

### §3.5 Chart planes (ratified B-4)

| plane | default windows | all four toggleable |
|---|---|---|
| 4H | 7d, 30d | yes |
| 1D | 30d, 90d | yes |
| 1W | 90d, 365d | yes |
| 1M | 365d | yes |

**Value areas render as extended horizontal bands** carried forward across the plane, as in the operator's screenshots — not confined to the profile's own span.

**The forming-candle rule.** On weekly and monthly planes the current candle is unfinished most of the time. It is **drawn, greyed, and labelled "forming"** so the chart looks like the operator's chart — while **every computed number uses closed candles only.** Mid-week, the weekly RSI is last week's. That staleness is deliberate and is the founding law of this toolkit; a fixture asserts no forming bar reaches any computed value.

### §3.6 Volume-side additions (ratified B-7)

**RVOL** — current volume against the trailing 20-day average for the same time-of-day bucket. Computable now from the single volume column the estate stores.

**Parked with an explicit dependency: CVD / delta and volume-spread (VPA / effort-vs-result).** The estate persists one volume column; taker-buy fields exist in Binance's public candles but are **not stored**. This is a schema question, not a data-source question. Recorded here as a named parked item with its dependency so it cannot be silently lost or accidentally half-built; requisition sits with ATHENA.

### §3.7 The {12,25} lattice (ratified B-8)

The 1D and 1W planes draw the **EMA(12) / EMA(25)** pair as a display-only, toggleable lattice beside the volume layer. Rationale: the practitioner study landed this exact pair as XO's higher-timeframe filter, the census will measure it against `{9,89,200}` regardless, and rendering it now lets the operator's eye rehearse the comparison months before it is scored. **Display only. No signal, no vote, no score contribution.**

---

## §4 · VALUE-AREA NESTING (new layer — from the operator's screenshots)

The operator's request, precisely: *extend each value area, see where it superimposes with the one immediately after; where they do not overlap, watch price reaction at the VA edges.*

This is the classic market-profile value comparison — normally run across consecutive **days** — applied instead across **window scales**. It asks a sharper question: *does this week's business sit inside this month's, or has value migrated?*

### §4.1 Per adjacent pair

Pairs: **7d↔30d, 30d↔90d, 90d↔365d.** For each, every capture records:

- **`state`** ∈ `nested_inside` (shorter VA entirely within longer) · `nested_outside` · `overlapping` (partial) · `disjoint_above` (shorter value entirely above longer) · `disjoint_below`
- **`overlap_frac`** = |intersection| ÷ |shorter VA| — how much of short-term value has long-term backing
- **`consensus_band`** = `[max(VAL_a, VAL_b), min(VAH_a, VAH_b)]` when they intersect — ground where both timescales of business agree. Its edges emit as levels.
- **`gap_band`** when disjoint — the unclaimed space between them. Its edges emit as levels, flagged `facing_edge`.
- **`price_location`** — inside consensus · inside one only · in the gap · outside all

### §4.2 The prose the report must print

When disjoint, the report states it in words, not only in a table. Example of the required form:

> *7-day value sits entirely above 30-day value. The unclaimed gap runs 63,100–64,250. The facing edges are the 7d VAL at 64,250 and the 30d VAH at 63,100.*

That sentence is the deliverable the operator asked for; a table alone does not satisfy §4.

### §4.3 Scale confirmation (ratified B-10 option a)

When two windows' VA edges land within the same-family collapse tolerance (0.02 daily-ATR), the merged level carries `scale_confirmed: [7d, 30d]`.

**It merges for scoring and displays a badge.** It does **not** add score. Rationale, on the record: nested windows share data — the 30-day window *contains* the 7-day window — so they are partially dependent voices, and the project's law is *counted, never weighted*, which forbids the fractional credit that partial dependence would deserve. Conservative scoring plus full visibility is the honest treatment.

### §4.4 Census candidate

Whether price reacts differently at scale-confirmed edges is **H-VAN**, routed to APOLLO. The brief records the states daily; only the census may say whether they pay.

---

## §5 · CONFLUENCE ENGINE — updates

### §5.1 Families (revised)

| family | members |
|---|---|
| `vwap_anchored` | developing W/M/Q/Y + prior M/Q/Y, each with 1σ/2σ/3σ |
| `vwap_rolling` | 7/30/90/365d RVWAP, each with 1σ/2σ/3σ |
| `profile_windowed` | POC/VAH/VAL for {prior-day, 7, 30, 90, 365}; LVN midpoints and edges; consensus and gap band edges |
| `structure` | confirmed pivots, period opens, prior D/W/M extremes, session extremes |
| `ss` | armed zone edges (Z1/Z2/Z3), governor band edges per lens |

Splitting VWAPs into anchored and rolling, and giving windowed profiles their own family, prevents any single tool type from dominating the diversity term.

### §5.2 Rules (unchanged, printed in every capture)

Collapse same-family within **0.02 daily-ATR** → cluster within **0.15 daily-ATR** → score = Σ min(members per family, **3**) + distinct families → lines in the sand = highest-scoring cluster within **1.5 daily-ATR** each side of price, ties by proximity, fallback nearest scoring ≥ 4. **Counted, never fitted.**

**Sensitivity annex** at tolerance 0.10 / 0.20; an instability chip prints when the top-3 ranking changes between them.

### §5.3 Density warning — recalibrate, do not defend

v1.1 ran 46–62 levels per asset. With rolling bands (28), windowed profiles with LVNs (~20), prior anchors and σ2/σ3 (~21), and nesting bands (~8), expect **~180–200 levels per asset**. Every threshold above was calibrated against a registry a third that size. The calibration report (§9.2) is the basis for re-ratification; **no threshold is defended on intuition once measured numbers exist.**

### §5.4 Dual scoring — the toggle made real (ratified B-9)

Every capture computes areas and lines **twice**: once with `vwap_rolling` and `profile_windowed` included, once without. **Both are recorded.** The report's toggle switches views.

This is the filter's purpose made measurable: the operator sees daily whether volume evidence *moves his lines* — and when the census later asks whether volume confluence changes outcomes, the live instrument will have been rehearsing that exact comparison, in display-only form, for months.

---

## §6 · INDICATOR AND STATE LAYERS

### §6.1 Oscillators (ratified B-5)

RSI, StochRSI, MACD, Awesome Oscillator on `{1h, 4h, 12h, 1d, 1w}`. The **1M plane carries price and volume structure only** — a closed-bar monthly oscillator in late July is June's number and has almost no sample.

**Generalised divergences** on RSI, MACD-histogram and AO across every timeframe, regular and hidden. Each divergence records the **price level of its pivot**, matched to the confluence area containing it — this is what turns *"is the same divergence printing on the AO, and is it landing where Secret Sauce has a level?"* into a computed line. Requires Phase I-R's divergence causality test to pass first.

### §6.2 Cross-state layers (display-only, recorded as state)

- **RVWAP crosses:** pairs 7×30, 7×90, 30×90, 90×365 — which is above, bars since cross, spread in daily-ATR.
- **RVWAP ↔ SS-EMA distances** (operator's B-1 comment): for each of the four windows, distance to the 9/89/200 EMAs at each lens `{1h, 4h, 12h}`, in bps and daily-ATR. This makes *"the 30-day VWAP's evolving relationship to the 89"* a queryable time series from day one.
- **1m fast-lattice** (operator's gate comment): on the 1-minute frame, EMA(300) and EMA(450) plus the 9/89/200 set — which is above, bars since cross — recorded alongside the **5m 9/89/200** cross states for comparison.

All three are **observation layers**. Whether any of them predicts anything is census work: **H-RVX** (RVWAP × SS crosses) and **H-M1X** (1m lattice × 5m), both routed to APOLLO. **TC-5's permanent 5m entry floor is untouched** — measuring 1m crosses as context is measurement, not entry logic, and the candidates say so explicitly.

---

## §7 · THE DECISION INSTRUMENT

### §7.1 Trade hypothesis drafts

Mechanically derived from each asset's two lines and the next areas beyond them, in the operator's own if-then grammar. Explicitly labelled **drafts**. **No sizing, ever.**

### §7.2 R:R ranking — geometry, not prophecy

For each draft, printed with all components so the operator can recompute by hand:

- **entry** = the line's cluster mean
- **invalidation** = beyond the cluster's far edge (the price that says the level failed)
- **target 1** = the next opposing cluster scoring ≥ 4; **target 2** = the one beyond it
- **R:R** = |target − entry| ÷ |entry − invalidation|

The board sorts by R:R, and the report says plainly what this ranking is: **a ranking of structural quality, not of probability.** It contains no claim that any setup is likely to work — that would require outcome statistics the firewall reserves for the census. A high R:R here means *the geometry is favourable*, nothing more.

### §7.3 Composite bias print — counted, dissent named

Five families each declare a side {+1, 0, −1} under printed rules:

| family | rule |
|---|---|
| trend | SS governor direction majority across 1h/4h/12h |
| momentum | RSI + MACD + AO agreement on 4h and 12h |
| location | price vs anchored VWAP complex and prior-day value |
| volume location | price vs windowed value areas and consensus bands |
| crowding | funding percentile (≥90 votes against, ≤10 votes for) |

The print is **"N of 5 agree, dissenting: <names>"** plus the resulting band. **Equal weights, count-based, never fitted.** The compression flag demotes the final band one step toward neutral (it does not half-weight votes — that would contradict count-based purity).

**Both the bias print and the radar may disagree.** When they do, a disagreement chip prints and nothing is reconciled — they measure different things, and the disagreement is information.

### §7.4 The intelligence ladder — bounded on the record

The operator asked how to add intelligence. Three rungs, and honesty about which one we are on is part of the design:

1. **Counted composite** (§7.3) — ships now. Transparent, unfitted, dissent visible.
2. **Reviewer synthesis** — ARGUS's read on each capture in chat. Judgement-shaped intelligence, clearly attributed to a reviewer rather than to the machine. Ships now.
3. **Learned weights** — which layer combinations actually predicted anything. This is exactly what **CENSUS-1d** measures on exploration-classic data under G-7. **Only after that, and only pre-registered, may any weight enter a bias print.**

**Nothing in this build may implement rung 3.** A live display instrument that ships fitted weights is a machine flattering itself with its own history. A fixture asserts no weight vector exists in the scoring path.

---

## §8 · RECORD AND STORAGE

### §8.1 Captures

`briefs/brief_<date>_<slot>.json` — **tracked**. Index `briefs/index.jsonl`. Each capture embeds `schema_version`, `rules_version`, `rules_sha256`, `analytics_version`, `analytics_sha`, `engine_version`, `slot`, the complete rule set, and every input's `last_bar_utc`.

`rules_version` **→ 2.0.0** (ratified A-6): the closed-bar correction plus the volume filter move published numbers, and archive-comparability law requires a major bump. The `f_an_8_diff` table is the bridge between eras.

`/brief` auto-commits its capture, never pushes. Same-slot re-run warns and requires confirmation. `brief_render.py --date --slot` regenerates HTML from any stored capture — which is what makes HTML disposable.

### §8.2 Panel tables — **daily partitions** [REVIEWER DESIGN DECISION, open to veto]

**Changed from v4.** v4 specified three monolithic parquet files rebuilt each day. With the volume layers the levels table reaches roughly 5,000–6,000 rows per day, and a rewritten binary file stores a **complete new blob in git every single day** — growth compounds instead of accumulating.

**Therefore:** write **daily partition files**, each written once and never rewritten:

```
briefs/panel/snapshots/YYYY-MM-DD.parquet
briefs/panel/levels/YYYY-MM-DD.parquet
briefs/panel/areas/YYYY-MM-DD.parquet
```

`brief_panel.py` rebuilds any partition from its captures and can emit a consolidated view on demand (untracked, regenerable). Git growth becomes linear and additive. Estimated tracked growth ~150–250 MB/year; **the calibration report prints measured sizes so this estimate is replaced by fact.**

`briefs/panel/SCHEMA.md` documents every column, its units, its source layer, and the `schema_version` in which it appeared.

### §8.3 Operator surfaces

`/brief-note "<text>"` timestamps an observation into the current capture and commits. `ops/positions.yaml` — hand-maintained, **state only**: symbol, lens, direction, entry, stop. **No P&L, no outcomes, no history, ever.** A fixture asserts no forbidden keys.

### §8.4 Backfill

Forward-only. The generator refuses a target date earlier than the first capture without an explicit `--backfill` flag, which stamps a provenance marker. Historical confluence work is **census** work on exploration-classic, output to `research_outputs/census1d/`, never into `briefs/`. **The lockbox stays sealed**, and the partition-footprint guard (warm-ups included) is enforced.

---

## §9 · FIXTURES AND CALIBRATION

### §9.1 Fixtures

Carried from v4: **F-B9..F-B24**. New in this amendment:

- **F-AN-13b** — the five newly-covered functions pass truncation testing (§1.1).
- **F-AN-14c′** — `resample_ohlcv` **raises** on undecidable step inference (§1.2).
- **F-B25** — VA nesting: on synthetic profiles with known geometry, `state`, `overlap_frac`, consensus and gap bands are computed correctly for all five states.
- **F-B26** — scale confirmation: coincident edges merge, carry `scale_confirmed`, and **do not increase score** (asserts B-10a).
- **F-B27** — dual scoring: both scored sets present in every capture; the volume-excluded set contains zero members from `vwap_rolling` or `profile_windowed`.
- **F-B28** — no weights: no weight vector, coefficient array or fitted parameter exists anywhere in the scoring path (asserts §7.4).
- **F-B29** — R:R integrity: every printed ratio recomputes from its own printed components; no ratio prints without entry, invalidation and target all present.
- **F-B30** — warm-up honesty: an asset with under 365 days of data prints a `warming` chip for the 365d window and **no number**.
- **F-B31** — forming-candle isolation: on 1W and 1M planes, the forming candle is drawn but appears in **no** computed value.
- **F-B32** — partition integrity: daily partitions are written once, never rewritten; the panel rebuilds from captures alone; grain is (asset, slot, date).

### §9.2 Calibration report — required deliverable

`exchange/reports/BRIEF2_CALIBRATION_<date>.json` plus a markdown summary:

1. Level count per asset, v1.1 vs now, **by family**.
2. Score distribution before and after: min / median / p90 / max, and how often the family cap binds.
3. Line-in-the-sand stability across tolerance 0.10 / 0.15 / 0.20, per asset.
4. Family composition of the top-3 areas per asset — specifically whether `vwap_rolling` or `profile_windowed` now dominates, which would mean the family split did not go far enough.
5. VA nesting state distribution across the ten assets and three pairs.
6. Dual-scoring divergence: how often the volume-included and volume-excluded lines in the sand **differ**, and by how much. *This is the single most interesting number the build will produce.*
7. Measured storage: bytes per capture, per partition, projected annual.

---

## §10 · DELIVERABLES

`analytics/` remediated (§1) · `scripts/daily_brief.py` rebuilt · `scripts/brief_render.py` · `scripts/brief_panel.py` · `briefs/panel/SCHEMA.md` · `ops/brief_schedule.yaml` · `ops/positions.yaml.example` · `scripts/setup_brief_schedule.ps1` (three timezone-aware triggers on the existing `daily_routine.py --slot`, **no second scheduler**) · `.claude/commands/{brief,brief-render,brief-history,brief-note,brief-panel}.md` · `analytics/INTERFACE.md` (the census-facing contract: signatures, pinned conventions, causality classes, level and value-area record schema) · one real capture with all three partitions · **`exchange/reports/BUILDERS_REPORT_ARGUS_<date>_BRIEF2.md`** · `exchange/reports/BRIEF2_CALIBRATION_<date>.json` · published via `scripts/publish_exchange.py`.

**Every builder cycle ends with the Builder's Report file and the exchange publish.** No silent skips: if a directory is missing, create it and say so.

---

## §11 · WHAT THIS IS NOT

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or implied. No engine change. No forward scoring. No lockbox read. No fitted weights. No estate mutation.

Confluence scores measure **agreement between tools**, not edge. R:R measures **geometry**, not probability. Whether any of it predicts anything is census work under G-7, and the four candidates — **CENSUS-1d, H-RVX, H-M1X, H-VAN** — are routed to APOLLO, not answered here.

Every threshold in this amendment — 0.02 / 0.15 / 1.5 ATR, family cap 3, 120 rows, VA 70%, LVN 0.25 / 3 rows, slot times — is a **v1 placeholder** to be re-ratified against the calibration report and roughly a week of live use.

---

## §12 · LEDGER ENTRY

Append verbatim on completion, then add a completion bullet with fixture results, paths, calibration headline, runtime and commit hash:

> **## 2026-08-XX — BRIEF-2 built (CONTRACT v4 Amendment 2)**
> - Phase I-R first: five public functions brought under F-AN-13 truncation discipline (`vw_sigma_bands`, `divergences`, `naked_poc_registry`, `confirmed_pivots`, `resample_ohlcv`) — the builder's own audit found two more than the reviewer identified. `resample_ohlcv` now **raises** on undecidable step inference rather than keeping a possibly-forming bucket; verified cost was one fixture, no production caller. The hazard class F-AN-13 exists to abolish no longer survives in the function this correction was about.
> - BRIEF-2 built per interviews ARGUS-BRIEF-1 and ARGUS-VOLF-1: **two-stage report** (market monitor printed in full + decision instrument), R:R geometry ranking, counted 5-family bias print with dissent named, **dual scoring** with and without the volume families in every capture, **VA-nesting layer** (nested/overlapping/disjoint per adjacent window pair, consensus and gap bands, facing edges named in prose), LVN hunting, RVOL, {12,25} display lattice, RVWAP↔SS-EMA distance sequences, 1m 300/450 fast-lattice observation layer, unified windows {prior-day,7,30,90,365}, chart planes 4H/1D/1W/1M with the forming candle drawn but excluded from every computed value.
> - **B-10 ruled (a):** scale-confirmed VA edges merge for scoring and carry a badge; they do not add score, because nested windows are partially dependent and the project's law is counted-never-weighted.
> - **Intelligence ladder bounded on the record:** counted composite and reviewer synthesis ship; learned weights are census work under G-7 only, and F-B28 asserts no weight vector exists in the scoring path.
> - Panel storage changed to **daily partitions** (reviewer design decision): a rewritten monolithic parquet stores a full new blob in git daily, so growth compounds; write-once partitions make it linear. Measured sizes in the calibration report.
> - `rules_version` → **2.0.0**. Adoption remains gated on the operator's parity readings; CENSUS-1d, H-RVX, H-M1X and H-VAN wait behind it.
> - Reviewer: ARGUS. Operator: ratified by interview 2026-08-02.

— ARGUS, 2026-08-02
