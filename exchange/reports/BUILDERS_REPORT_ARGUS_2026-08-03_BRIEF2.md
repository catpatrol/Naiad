# BUILDER'S REPORT — ARGUS lane — BRIEF-2 RESHAPE

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Contract:** CONTRACT v4 Amendment 2
**Branch:** `v12-v1-census` · **Repo work: COMMIT-NO-PUSH** · **exchange/** published via `scripts/publish_exchange.py`

> Readable with zero context. Everything needed to audit this cycle is in this file.

---

## 0 · STATUS IN ONE PARAGRAPH — READ THIS FIRST

**Stages 0–4 are built, fixtured and committed. Stages 5–8 are NOT built.** This
cycle ran out of session capacity, not out of road: there is no unresolved
blocker. One genuine **FINDING (F-1R-A)** was raised at the Stage 1 gate and
closed under operator ruling; one genuine **FORK** (365d window × sealed lockbox)
was raised and resolved by operator ruling. Both rulings are enacted in code, not
merely recorded in prose. The suite is **181 passed / 1 skipped**, up from a
114/1 baseline. **No capture has been generated and no calibration report exists**
— those are Stage 7 and are listed as outstanding in §9.

---

## 1 · ENVIRONMENT GATE

| check | result |
|---|---|
| branch == `v12-v1-census` | PASS |
| pwd contains `\Users\` AND OneDrive | PASS — `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` |
| `engine/` `prompts/` `analytics/` all exist | PASS |
| HEAD at start (**reported, never gated**) | `a6d9f64` |
| `exchange/` subdirs present | `drops · queue · reports · status` (+ `DIGEST.md`, `README.md`) |

---

## 2 · STAGE 0 — CONTRACT AND PROBES

### 2.1 Amendment hash

| | |
|---|---|
| size | **29850 bytes** — matches required |
| sha256 | **`c502ecf471f8fab08d8a4077edfbb1860496c2fa80b1c9f02376816db532da9c`** — matches required |
| line endings | LF-only (0 CRLF, 376 LF) — no CRLF-conversion damage |
| after move to `prompts/CONTRACT_v4_Amendment_2.md` | hash **unchanged**, asserted equal |

A byte-identical duplicate `AMENDMENT_2_BRIEF2_RESHAPE_1.md` (same 29850 bytes,
same sha256) was present at repo root — a re-download. Left untouched, reported.

### 2.2 PROBE 0.3 — KLINE SUBSTRATE

Intervals actually stored, **all ten basket assets**: `1m · 5m · 15m · 1h · 4h · 12h`.

**15m IS stored.** Amendment §3.3's substrate tiers (1m for 7d, 5m for 30d, 15m
for 90d and 365d) are therefore fully satisfiable with **no substitution and no
silent resampling**. `prior-day` is not named in the §3.3 table; it is shorter
than 7d and takes the finest substrate (1m). The substrate actually used is
recorded per window in every capture, and any substitution is disclosed
explicitly rather than applied quietly.

| symbol | 1m rows | history start (UTC) | span (days) |
|---|---|---|---|
| BTCUSDT | 3,629,016 | 2019-09-08 | 2520.4 |
| ETHUSDT | 3,514,429 | 2019-11-27 | 2440.9 |
| ZECUSDT | 3,413,614 | 2020-02-05 | 2370.9 |
| SOLUSDT | 3,093,994 | 2020-09-14 | 2148.9 |
| NEARUSDT | 3,049,295 | 2020-10-15 | 2117.9 |
| JTOUSDT | 1,394,614 | 2023-12-08 | 968.9 |
| TAOUSDT | 1,214,345 | 2024-04-11 | 843.4 |
| FARTCOINUSDT | 849,770 | 2024-12-20 | 590.4 |
| HYPEUSDT | 618,425 | 2025-05-30 | 429.9 |
| LITUSDT | 319,925 | 2025-12-23 | 222.4 |

Estate last bar: **2026-08-02 21:34 UTC**.

### 2.3 PROBE 0.4 — 365d COVERAGE

**`LITUSDT` (222.4 days) is the only asset short of 365 days.** It gets a
`warming` chip and **no number** for the 365d window (F-B30). No asset is short
of 90 days. Verified on real data: LITUSDT 365d returns `warming=True` with
`poc/vah/val = None`, while its 7/30/90d windows are honest.

### 2.4 Operator-ratified decisions enacted, on the record

- **§1.2** — `resample_ohlcv` **RAISES** on undecidable step inference. Ratified.
- **§8.2** — panel tables are **WRITE-ONCE DAILY PARTITIONS**. Ratified. *(Not yet
  implemented — Stage 5, outstanding.)*

---

## 3 · FINDING F-1R-A — reported, ruled, closed

**Function:** `resample_ohlcv` — `analytics/structure.py:48`
**Mechanism site:** closure test at `analytics/structure.py:36-45`, decision at `:110-113`

### What was wrong

`_bucket_is_closed` decided closure from `infer_step_ms`, the **median** positive
spacing. When that median was **decidable but unrepresentative of the last bar's
true reach**, the test returned a confident `True`, the bucket was **published —
and later revised**. The §1.2 raise fires only when `infer_step_ms` returns
`None`, so **the ruled remedy never saw this door.**

Verified against live, unpatched code. Both inputs are well-formed: strictly
monotonic, duplicate-free, every stamp on the hour.

```
A. sparse-then-dense feed
   infer_step_ms(t[:12]) = 7_200_000      <- NOT None: no raise
   k=12 published bucket 1599955200000  volume=120.0  close=12.0
   full run,  same bucket               volume=130.0  close=13.0   REVISED

B. duplicate final timestamp
   infer_step_ms = 3_600_000 both sides   <- NOT None: no raise
   k=24  volume=24.0   high=10.0
   k=25  volume=1023.0 high=777.0                                 REVISED
```

### The counter-fact, measured

On **real estate data the hazard does not currently fire**: 1h→1d, 4,000 sampled
prefixes × 10 assets = **0 publish-then-revise events**. The estate's 1h series
are dense enough that the median is always right. The defect was **latent, not
live** — and it sat under a function the whole volume layer was about to depend on.

### The ruling and why the literal reading was insufficient

Operator ruled: **extend §1.2 — refuse unless closure is provable.**

No prefix-local heuristic can close this door. At k=12 the prefix is
**informationally identical** to a complete 2h-bar day: uniform spacing, fully
tiled, correct bar count. Median, minimum, uniformity and tiling checks all pass
on it. The distinction is not present in the data.

Closure is therefore proved by exactly one thing: **a bar exists in a strictly
later bucket.** Buckets `[0..m-1]` have that witness; the final bucket never can.
The final bucket is dropped unconditionally rather than guessed at.

### Cost, measured before adopting

**Zero on the estate.** 1h→4h and 1h→1d across all ten assets, **20 combinations,
identical bucket counts.** Live data always carries a forming final bucket that
both rules drop. No published number moves; F-AN-8 is intact; the parity
worksheet is unaffected.

One ratified assertion **inverted**, with its rationale recorded in the fixture:
F-AN-14b's *"a fully-populated final bucket must NOT be dropped"* becomes *"closure
must be PROVED by a later bar, never inferred from appearance"* — because "fully
populated" is not decidable from the data.

**§1.2 cost claim independently verified:** `scripts/parity_worksheet.py:116,205`
force ≥400 bars (never undecidable); `scripts/daily_brief.py` never calls
`resample_ohlcv` — it has its **own** private `resample()` at
`daily_brief.py:216`. The claim holds literally. The duplicate implementation is
noted below as an outstanding risk.

---

## 4 · FORK — 365d window × sealed lockbox

The 365d trailing window runs **2025-08-03 → today**; the lockbox is
**`[2024-07-01, 2025-10-06)`**. Overlap **64 days**, self-clearing **2026-10-06**.
7/30/90d are clear by construction.

The amendment **mandates** the 365d window (§3.2, §3.3) and **also** says "No
lockbox read" (§11, §8.4). It conflicts with itself, so it could not be resolved
by the builder.

**Operator ruled:** the seal governs **scored outcome evidence**, not raw price in
a display-only trailing window — consistent with `LEDGER:698` (the brief's
firewall is about *outcome statistics*) and `LEDGER:220` (the G-1 guard sits on
the *replay* path). Build 365d as specified, **disclose the overlap footprint**.

**The condition is enforced in code, not prose.** `analytics.lockbox_overlap()` is
a disclosure utility — deliberately never a refusal — and every windowed layer
carries the record. Measured on real BTCUSDT: **365d → 64.115 days, 90d → 0.0**.
The G-1 replay-path guard is untouched.

---

## 5 · WHAT WAS BUILT, PER STAGE

### STAGE 1 — Phase I-R (commit `e355845`)

All five functions **PASS** truncation testing. **No causality violation** — the
§1.3 gate did not halt the build.

| function | location | verdict | form used |
|---|---|---|---|
| `vw_sigma_bands` | `vwap.py:133` | PASS | composed producer path |
| `divergences` | `momentum.py:119` | PASS (lag:5) | structural invariants, regular + hidden |
| `naked_poc_registry` | `profile.py:82` | PASS | set-membership stability |
| `confirmed_pivots` | `structure.py:161` | PASS | set stability + as-of at/beyond array end |
| `resample_ohlcv` | `structure.py:48` | PASS | bucket-axis prefix |

**The naive prefix form is VACUOUS on all five.** Measured against deliberately
sabotaged implementations, the obvious fixtures certify non-causal code as green.
Every assertion was therefore mutation-tested:

```
MUTATION BATTERY — 11/11 behaviour-changing mutants CAUGHT
  vwap.py       bands borrow NEXT bar's dispersion            CAUGHT
  momentum.py   report AGREEMENTS as divergences              CAUGHT
  momentum.py   emit from_index 5 bars in the FUTURE          CAUGHT
  momentum.py   price_level = EARLIER pivot                   CAUGHT
  momentum.py   read oscillator at the WRONG pivot            CAUGHT
  profile.py    read ONE bar past the decision bar            CAUGHT
  profile.py    DELETE the as-of guard                        CAUGHT
  structure.py  confirm pivots from TRUNCATED windows         CAUGHT
  structure.py  admit pivots BEFORE their window closes       CAUGHT
  structure.py  confirmation lag off by one                   CAUGHT
  structure.py  publish the UNPROVEN final bucket             CAUGHT
```

A first harness run reported 4 spurious results; it was **rebuilt with
applies/behaves validity checks** after a `%%` escaping bug produced a false
CAUGHT. The table above is from the validated harness.

The divergence fixture uses **seed 2, not the file default** — on seed 7 only two
of the four `(pivot_kind, kind)` combinations ever produce a record at any k, so
half the parametrisation would have asserted over an empty set. Every fixture
carries an explicit non-emptiness precondition.

`ANALYTICS_VERSION` **1.1.0 → 1.2.0**. Suite **129 passed, 1 skipped**.

### STAGE 2 — volume layer (commit `074ae2b`)

`analytics/nesting.py` (new) · `windowed_profile` · `low_volume_nodes` · §3.3 knobs.

- Windows `{prior-day, 7d, 30d, 90d, 365d}`; **5d and 20d RETIRED** (near-duplicates
  inflate scores in a system that counts agreement).
- 120 rows, VA 70%, substrate tiers as probed.
- **LVN threshold is relative to the MEDIAN**, not the mean — a profile peaked at
  the POC drags the mean up, so a mean-relative threshold classifies ordinary rows
  as low-volume on any well-formed profile. Runs touching either extreme are
  discarded: edge rows are always thin by construction, and emitting them would
  manufacture ten meaningless levels per asset across five windows.
- **Warm-up honesty is COVERAGE, not bar count.** Fixtured: 40 days of 1m data
  (>10,000 bars) still cannot claim a 90d window.
- **F-B25**: all five nesting states on geometry known by construction,
  `overlap_frac`, consensus and gap bands, facing edges, the §4.2 prose, warming,
  `price_location`, emitted levels.

Suite **150 passed, 1 skipped**.

### STAGE 3 — confluence engine (commit `ffe775b`)

- §5.1 families → `vwap_anchored · vwap_rolling · profile_windowed · structure · ss`.
- §5.2 rules **unchanged** and asserted: 0.02 / 0.15 / 1.5 ATR, family cap 3.
- **§4.3 scale confirmation (B-10a)**: coincident window edges merge, carry
  `scale_confirmed` in scale order, and **do not add score** — structurally, because
  the two levels become ONE member so `score()` cannot see them as two voices.
  Badged only where SCALES differ; one window firing twice is not two timescales
  agreeing.
- **§5.4 dual scoring**: exclusion happens at the **REGISTRY level, before collapse**.
  Dropping volume levels after clustering would leave cluster means already pulled
  by them — a relabelled with-volume answer. F-B27 asserts this directly
  (64000.5 vs 64000.0).
- `lines_differ()` computes **calibration §9.2 item 6** so it is computed, not eyeballed.
- **F-B28**: no weight vector, coefficient array or fitted parameter in the scoring
  path — by source scan (with `volume-weighted` excluded by name as the one
  legitimate use), by AST (`score()` may contain no multiplication and no float
  constant), and behaviourally (doubling every family's membership cannot double
  the score; scores are integers).

Suite **165 passed, 1 skipped**.

### STAGE 4 — report layers, PARTIAL (commit `70bd499`)

`scripts/brief2.py` (new), deliberately kept OUT of `daily_brief.py` so the v1.1
monitor and its F-B1..F-B8 fixtures keep working while the new layers are built
beside them.

**Built:** windowed profiles with substrate recorded per window · RVWAP 1/2/3σ on
7/30/90/365d · VA nesting with §4.2 prose · oscillators on `{1h,4h,12h,1d,1w}`
with generalised divergences on RSI/MACD-hist/AO (regular and hidden, each
carrying its pivot's price level) · §6.2 cross-state (RVWAP pairs, RVWAP↔SS-EMA
distances, 1m 300/450 fast lattice) · §3.7 {12,25} display lattice · §3.5 chart
planes · **Part II** in the §2.2 order (area map → lines → drafts → R:R → composite
bias) · §8.1 capture envelope with `rules_version 2.0.0` and canonical
`rules_sha256`.

**Computed planes route through `analytics.structure.resample_ohlcv`**, so the
§1.2 closure discipline reaches every plane the report prints.

**The forming candle** is built from the LEGACY keep-the-bucket path on purpose —
the public path now refuses to emit an unproven bucket, which is right for
computation and wrong for a candle we intend to draw and label unfinished. It is
`draw_only`/greyed and emitted in a separate branch from every computed value.

Fixtures **F-B29** (every ratio recomputes from its own printed components; no
ratio without entry/invalidation/target; predictive language banned from rows),
**F-B31** (forming-candle isolation — the weekly oscillator's last bar is strictly
BEFORE the forming bar, so mid-week the weekly RSI really is last week's),
**F-B33** (parity banner asserted in BOTH directions, so it cannot pass as a
constant), plus §7.1 no-sizing and §7.3 dissent-as-invariant.

**NOT built in Stage 4:** wiring into `daily_brief.py`, and the Part I / Part II
**HTML render**. The layers compute; nothing renders them yet.

Suite **181 passed, 1 skipped**.

---

## 6 · FIXTURE TRANSCRIPT

```
tests/test_analytics.py            56 passed
tests/test_brief2_volume.py        21 passed
tests/test_brief2_confluence.py    15 passed
tests/test_brief2_report.py        16 passed
------------------------------------------------
FULL REPO SUITE                   181 passed, 1 skipped   (44.6 s)
BASELINE AT START                 114 passed, 1 skipped
```

Fixtures delivered: **F-AN-13b** (five functions) · **F-AN-14c′** (raises) ·
**F-AN-14d** (published bucket never revised — the F-1R-A regression guard) ·
**F-B25** · **F-B26** · **F-B27** · **F-B28** · **F-B29** · **F-B30** (mechanism) ·
**F-B31** · **F-B33**.

---

## 7 · REAL-DATA VERIFICATION (BTCUSDT, full layer stack)

```
price 63,477.20   daily ATR 1,699.80

  volume_layer              0.86s
  rvwap_layer               3.85s
  nesting_layer             0.00s
  oscillator_layer          5.54s
  cross_state_layer         8.44s      <- slowest: 1m EMAs over 3.6M bars
  lattice_layer             0.02s
  build_registry            0.00s
  confluence                0.00s
  decision_instrument       0.00s
  ---------------------------------
  TOTAL, one asset         18.92s
  estimated, ten assets     3.2 min
```

**No runtime FINDING.** One full capture is projected at ~3.2 min against the
~15 min threshold, ×3 slots/day.

Nesting prose actually produced (§4.2 deliverable):

> *7d value sits entirely inside 30d value (100% of 7d value has 30d backing). Both timescales agree between 62,912.98 and 64,747.18.*

R:R board top row: `short  entry 64,849.80  inval 65,012.95  target 63,017.29  R:R 11.23  score 7`.
24 divergences detected. 58 volume-family levels (the other three families were
empty in this isolated harness because Part I's `a` dict was stubbed).

---

## 8 · FINDINGS REPORTED, NOT FIXED

| id | file:line | status |
|---|---|---|
| **F-1R-A** | `analytics/structure.py:36-45` | **FIXED** under operator ruling (§3 above) |
| **F-1R-B** | `scripts/daily_brief.py:216` | **REPORTED, NOT FIXED.** `daily_brief.py` carries its own private `resample()` and therefore does **not** inherit the §1.2 closure discipline. Harmless while the v1.1 brief is display-only, but it must be routed through `analytics` when Stage 4's wiring lands, or the two briefs will disagree about which bar is the last closed one. |
| **F-1R-C** | `analytics/vwap.py:96-97, 128-129` | **REPORTED, NOT FIXED.** The σ bands that actually ship are duplicated inline in `rolling_vwap` and `anchored_vwap`; `vw_sigma_bands` is referenced nowhere in production. F-AN-13b pins the three copies as byte-identical so the duplication cannot drift silently, but the duplication itself remains. |

Class-(b) caller-contract risks surfaced by the Stage 1 analysis and recorded
rather than repaired: `vw_sigma_bands` never checks `len(vwap) == len(stdev)` and
numpy broadcasts a length-1 operand silently; `confirmed_pivots`' `as_of_index` is
an unvalidated free parameter; `naked_poc_registry` returns `naked=True` for an
empty evidence window.

---

## 9 · NOT BUILT — outstanding scope

**Stage 4 (remainder)** — wiring into `daily_brief.py`; Part I / Part II HTML render.

**Stage 5 — RECORD AND STORAGE.** Tracked captures `briefs/brief_<date>_<slot>.json`;
write-once daily partitions `briefs/panel/{snapshots,levels,areas}/YYYY-MM-DD.parquet`;
`brief_panel.py`; `briefs/panel/SCHEMA.md`; commands `/brief`, `/brief-render`,
`/brief-history`, `/brief-note`, `/brief-panel`; `daily_routine.py --slot` +
`routine_jobs.json` slots array; `setup_brief_schedule.ps1` (three DST-aware
triggers from `ops/brief_schedule.yaml`); `ops/positions.yaml.example`; §8.4
backfill refusal and partition-footprint guard; LIT known-wrong marking; fixtures
**F-B9..F-B24** and **F-B32**.

**Stage 6 — FORWARD-0.** Hash-chained `ops/forward_log.jsonl`; `/trade-log`,
`/trade-verify`; fixtures **F-F1..F-F5**. (Note the G-9 → G-10 renumber; no
aggregation until G-10 is separately ratified.)

**Stage 7 — REAL RUN + CALIBRATION.** **No capture has been generated. No
calibration report exists.** All seven §9.2 items outstanding, including item 6
(how often the volume-included and volume-excluded lines differ) — though
`levels.lines_differ()` is built and ready to produce it.

`analytics/INTERFACE.md` **was written** and is published with this report.

---

## 10 · PROVENANCE

| | |
|---|---|
| `ANALYTICS_VERSION` | **1.2.0** |
| `analytics_sha()` | `054ff35c6e23c6702b4fd4bb75f6a6c8bc7ba88eebb3df84fa63a20eea268932` |
| `rules_version` | **2.0.0** (§8.1, ratified A-6) |
| `schema_version` | 2.0.0 |
| modules hashed | 10 |
| amendment sha256 | `c502ecf471f8fab08d8a4077edfbb1860496c2fa80b1c9f02376816db532da9c` |

### Commits — all COMMIT-NO-PUSH, branch `v12-v1-census`

| commit | stage |
|---|---|
| `e355845` | Phase I-R — five functions under F-AN-13; `resample_ohlcv` raises |
| `074ae2b` | Stage 2 — windowed volume layer, LVN hunting, VA-nesting (F-B25) |
| `ffe775b` | Stage 3 — confluence engine, scale confirmation, dual scoring |
| `70bd499` | Stage 4 (layers) — volume/oscillator/cross-state, Part II instrument |

HEAD at start: `a6d9f64`.

### Artifacts produced — exact repo paths

| path | note |
|---|---|
| `prompts/CONTRACT_v4_Amendment_2.md` | the amendment, hash-verified in place |
| `analytics/nesting.py` | NEW — VA nesting + §4.2 prose |
| `analytics/profile.py` | `windowed_profile`, `low_volume_nodes`, §3.3 knobs |
| `analytics/structure.py` | `UndecidableStepError`, `_provably_closed_count` |
| `analytics/levels.py` | families, scale confirmation, `dual_score`, `lines_differ` |
| `analytics/__init__.py` | v1.2.0, CONVENTIONS, lockbox disclosure |
| `analytics/INTERFACE.md` | NEW — the census-facing contract APOLLO cites |
| `scripts/brief2.py` | NEW — BRIEF-2 layers + Part II instrument |
| `tests/test_analytics.py` | F-AN-13b, F-AN-14c′, F-AN-14d |
| `tests/test_brief2_volume.py` | NEW — F-B25, LVN, warming |
| `tests/test_brief2_confluence.py` | NEW — F-B26, F-B27, F-B28 |
| `tests/test_brief2_report.py` | NEW — F-B29, F-B31, F-B33 |
| `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-03_BRIEF2.md` | this file |
| `exchange/reports/INTERFACE_2026-08-03.md` | copy, sha-verified |

---

## 11 · FIREWALL — reprinted, all four clauses

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or
implied. No engine change. No forward scoring. No lockbox read for scored
evidence. No fitted weights. No estate mutation.

Confluence scores measure **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Whether any of it predicts anything is census work
under G-7 — **CENSUS-1d, H-RVX, H-M1X, H-VAN** are routed to APOLLO, not answered
here.

**Adoption remains gated on the operator's parity readings.** Every render prints
`PARITY NOT CERTIFIED — numbers not yet adopted` until the certification flag is
set; F-B33 asserts it in both directions. This amendment may be **built** before
parity returns; its output may not be **trusted** until it does.

— HEPHAESTUS, 2026-08-03
