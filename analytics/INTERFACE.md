# `analytics/` — INTERFACE

**The census-facing contract.** APOLLO cites this file; it is the stable
description of what `analytics/` computes, under which conventions, with which
causality class, and in which record shape. Nothing here is evidence of edge —
see the firewall at the end.

- `ANALYTICS_VERSION` **1.3.0**
- `analytics_sha()` = `da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731`
  — sha256 over the package sources in fixed order, binary reads. Printed beside
  the version by every artifact that consumes this toolbox, so a stored capture
  can always name the exact code that produced it.
- Modules hashed, in order: `__init__ · momentum · vwap · volatility · profile ·
  structure · levels · stats · parity · nesting`
- The consuming capture envelope carries its own `rules_version` **2.0.0** and
  `schema_version` **2.1.0**. Those version the BRIEF's rules and record shapes;
  this file versions the arithmetic. A citation needs all three.

## Invariants

| id | invariant |
|---|---|
| I-A | No I/O. `analytics_sha()` is the one exception and is a PROVENANCE function, not a computation one; it uses `pathlib.Path.read_bytes()`, never the builtin `open(`. F-AN-4 scans for it. |
| I-B | No imports from `engine/` or `scripts/`. F-AN-3 asserts it. `resample_ohlcv` imports pandas locally and only to reproduce a groupby byte-for-byte; the equivalence to `scripts/s1_resample.aggregate()` is asserted from the TEST file (F-AN-14), which is what keeps I-B intact. |
| I-D | Warm-up honesty: a function returns NaN for exactly the documented number of leading positions and a FINITE value immediately after. It never seeds a number into the warm-up region to make a chart look continuous. |
| I-F | Any change to a returned NUMBER bumps at least the minor version. Archive comparability depends on it: two captures are comparable only if the recipe that produced them is identifiable. |

Version history that moved numbers: **1.1.0** dropped the unclosed resample
bucket; **1.2.0** made `resample_ohlcv` refuse an undecidable step and prove
closure from the data; **1.3.0** fixed `stoch_rsi`, which had returned all-NaN
on every input since it was written (F-2R-A, below).

## Causality classes

The class is part of the contract, not a comment. It is what tells a consumer
whether a value may be used at a historical decision bar.

| class | meaning | fixture |
|---|---|---|
| `causal` | output at `i` depends only on input `[0..i]` | F-AN-13 truncation-prefix |
| `lag:N` | output at `i` is knowable only at `i+N` | F-AN-13 at lag |
| `endpoint_only` | valid only at the end of the supplied array; MUST raise, or describe only the slice it was handed | exempt from F-AN-13; the raise is asserted |

**F-AN-13** is the fixture that matters most: `f(x[:k])[k-1] == f(x)[k-1]`,
exactly, at five truncation points, over every function in `SERIES_FUNCTIONS`.
It exists to abolish caller-contract dependencies as a CLASS rather than to fix
located instances.

**F-AN-13b** extends the discipline to five functions whose signatures the naive
form does not fit. The naive form is *vacuous* on all five — measured against
deliberately sabotaged implementations it certifies non-causal code as green —
so each is covered in the form its signature actually admits:

| function | form |
|---|---|
| `vw_sigma_bands` | COMPOSED: truncate the raw series, recompute the producer, then band. Truncating its own arguments is satisfied by any element-wise map, including one handed a look-ahead stdev. |
| `divergences` | lag:5 STRUCTURAL INVARIANTS, both regular and hidden. A prefix-vs-full equality is a tautology here: at N=5 both sides receive bit-identical pivot arrays. |
| `naked_poc_registry` | SET-MEMBERSHIP STABILITY on hand-built geometry. A random series does not discriminate a registry that reads one bar past the decision bar. |
| `confirmed_pivots` | SET STABILITY plus as-of at and BEYOND the array end, where the two real mutations bite. |
| `resample_ohlcv` | BUCKET-AXIS prefix: growing the input only APPENDS buckets, never revises one already emitted. |

All eleven behaviour-changing mutants tried against these fixtures are caught,
and every fixture carries an explicit non-emptiness precondition.

**F-AN-6b — a guard that cannot fail is not a guard.** Every function in
`SERIES_FUNCTIONS` must be FINITE immediately after its documented warm-up.
This fixture exists because F-AN-13 has a blind spot it cannot see past: its
assertion is `got[k-1] == ref[k-1]` with a NaN-equals-NaN branch, and an
**all-NaN series satisfies that at every truncation point**. F-2R-A (below) rode
through it green for the whole life of the function. F-AN-6b asserts the
property F-AN-13 had silently assumed.

## Signatures

Every function is pure. Arrays in, arrays or plain dicts out; nothing is read,
written or cached.

### `analytics` (package root)

```
ANALYTICS_VERSION : str
CONVENTIONS       : dict           # recipe + causality + warm-up, per function
SERIES_FUNCTIONS  : tuple[str]     # what F-AN-13 and F-AN-6b must exercise
analytics_sha()                                  -> str
lockbox_overlap(start_ms, end_ms)                -> dict
LOCKBOX_START_MS, LOCKBOX_END_MS : int
```

### `momentum`

```
sma(x, length)                                   -> ndarray
ema(x, length)                                   -> ndarray
rma(x, length)                                   -> ndarray
rsi(close, length=14)                            -> ndarray
stoch_rsi(close, rsi_length=14, stoch_length=14, k=3, d=3)
                                                 -> (k_line, d_line)
macd(close, fast=12, slow=26, signal=9)          -> (line, signal, hist)
awesome_oscillator(high, low, fast=5, slow=34)   -> ndarray
divergences(price_pivot_idx, price_pivot_val,
            osc_pivot_idx, osc_pivot_val, pivot_kind,
            kind="regular", max_pairs=2)         -> list[dict]
```

`divergences` requires `pivot_kind` — it is not optional and has no default —
because BOTH divergence classes are the same predicate `price_up != osc_up` and
only the pivot type separates regular from hidden.

### `vwap`

```
hlc3(high, low, close)                           -> ndarray
rolling_vwap(open_time_ms, src, volume, window_days, sigmas=(1,2,3))
                                                 -> {vwap, stdev, band_up_k, band_dn_k}
anchored_vwap(src, volume, anchor_index, sigmas=(1,2,3))
                                                 -> {vwap, stdev, band_up_k, band_dn_k}
vw_sigma_bands(vwap, stdev, sigmas=(1,2,3))      -> {band_up_k, band_dn_k}
two_pass_vw_variance(src, vol)                   -> float      # NOT the pinned path
MIN_BARS = 10 · DAY_MS = 86_400_000
```

`anchored_vwap` raises `ValueError` if `anchor_index` is outside the series.

### `volatility`

```
true_range(high, low, close)                     -> ndarray
atr(high, low, close, length=14)                 -> ndarray
realised_vol(close, fast=7, slow=30)             -> ndarray
percentile_rank(sample, value=None, as_of_index=None)   -> dict   # endpoint_only, RAISES
```

### `profile`

```
volume_profile(high, low, volume, bins=100, value_area=0.70)      -> dict
windowed_profile(open_time_ms, high, low, volume, window_days, as_of_ms,
                 bins=PROFILE_ROWS, value_area=VALUE_AREA,
                 substrate=None, min_bars=2)                      -> dict
low_volume_nodes(edges, hist, threshold=LVN_THRESHOLD, min_rows=LVN_MIN_ROWS)
                                                                  -> list[dict]
naked_poc_registry(period_pocs, high, low, as_of_index)           -> list[dict]
PROFILE_ROWS 120 · VALUE_AREA 0.70 · LVN_THRESHOLD 0.25 · LVN_MIN_ROWS 3
WINDOW_SUBSTRATE = {prior-day: 1m, 7d: 1m, 30d: 5m, 90d: 15m, 365d: 15m}
```

`substrate` is carried through untouched and RETURNED. It is used in no
computation; passing it is what stops the printed provenance and the real one
from drifting apart.

### `structure`

```
pivots(values, left=5, right=5, kind="high")     -> (idx, level, confirmed_at)
confirmed_pivots(values, as_of_index, left=5, right=5, kind="high")
                                                 -> (idx, level, confirmed_at)
period_opens(open_time_ms, open_, period="D")    -> (bucket_key, period_open)
prior_period_extremes(open_time_ms, high, low, period="D")  -> (prior_high, prior_low)
resample_ohlcv(open_time_ms, open_, high, low, close, volume, step_ms,
               drop_unclosed=True)               -> dict of ndarray  # RAISES
infer_step_ms(open_time_ms)                      -> int | None
CONFIRMATION_LAG = 5 · UndecidableStepError(ValueError)
```

`period` ∈ `D · W · M · Q · Y`; anything else raises. `confirmed_pivots` is the
as-of-safe entry point and should be preferred to `pivots` by every consumer.

### `nesting`

```
va_nesting(short_val, short_vah, long_val, long_vah)  -> dict
price_location(price, nest)                           -> str | None
nesting_levels(pair, nest)                            -> list[level records]
describe_nesting(pair, nest, dp=2)                    -> str
ADJACENT_PAIRS = (("7d","30d"), ("30d","90d"), ("90d","365d"))
```

`describe_nesting` is a FIRST-CLASS OUTPUT, not a formatting nicety: §4.2
requires that a disjoint state be stated in words, not only in a table.

### `levels`

```
LevelRegistry(levels=None)
  .add(family, label, level, source_layer, timeframe=None) -> self   # RAISES on
                                                    # unknown family; drops NaN
  .by_family() -> {family: count} · .as_list() -> list · len()
collapse_same_family(levels, atr, tol=COLLAPSE_ATR)     -> list[member]
cluster(members, atr, tol=CLUSTER_ATR)                  -> list[cluster]
score(members)                                          -> int
lines_in_sand(clusters, price, atr, reach=LIS_ATR, fallback_score=4) -> dict
sensitivity(members, atr, price, tolerances=(0.10, CLUSTER_ATR, 0.20)) -> dict
dual_score(levels, atr, price, tol=CLUSTER_ATR)         -> dict
lines_differ(lines_a, lines_b, atr)                     -> dict
FAMILIES · VOLUME_FAMILIES · SCALE_FAMILIES · WINDOW_ORDER
COLLAPSE_ATR 0.02 · CLUSTER_ATR 0.15 · LIS_ATR 1.5 · FAMILY_CAP 3
```

Every `atr`-taking function raises on a non-positive daily ATR rather than
producing a zero-width tolerance that would silently cluster nothing.

**`levels` has no time axis and cannot police one.** If a caller puts an
unconfirmed pivot or a future POC into the registry, the arithmetic will
faithfully cluster the future. Causality here is established UPSTREAM, by
slicing to the decision bar — see `structure.confirmed_pivots`.

### `stats`

```
zscore(x, length) · correlation(a, b, length) · beta(asset_returns, market_returns, length)
```

## Pinned conventions (`CONVENTIONS`)

Every entry is the exact variant, pinned, with its causality class and warm-up.
Highlights that consumers get wrong:

- **`rolling_vwap`** — TradingView RVWAP, pinned FROM SOURCE (Pine v5, MPL-2.0,
  supplied by the operator). Trailing **W milliseconds** (not a bar count)
  floored at the 10 most recent bars even when they fall outside W; `src =
  hlc3`; volume-weighted **POPULATION** variance via the one-pass identity
  `max(E[x²] − E[x]², 0)`; **no (n−1) correction**. Membership is
  `bar_open_time > current_bar_open_time − W`, current bar included. The
  zero-clamp is ALGORITHMIC, not defensive padding — the one-pass identity can
  go slightly negative through cancellation at high price with low dispersion,
  which is precisely the BTC-at-65,000 case.
- **`anchored_vwap`** — accumulated from the anchor bar; **`src = hlc3`**, same
  volume-weighted population variance, same bands.
- **`volume_profile`** — volume spread uniformly across each bar's range. This
  is an **APPROXIMATION** of tick data and every consumer carries the
  `approximation` provenance chip. Non-removable.
- **`percentile_rank`** — `endpoint_only`; RAISES if `as_of_index` is not the
  sample end. "Where does today rank" is only well posed at the end of a sample.
- **`naked_poc_registry`** — "untested" is a statement about the FUTURE of a
  level, so it is evaluated strictly over `(poc_index, as_of_index]` and never
  beyond. That is what makes it usable in an as-of historical walk, not only
  live.

### VWAP source and variance — VERIFIED by parity, no longer inferred

Through 1.2.0 this file said the anchored form's variance was a **REASONED
INFERENCE** from shared band machinery and must never be asserted as pinned.
That caveat has now been discharged by measurement, and it is worth recording
what discharged it, because reasoning could not have.

**The discriminator was a two-bar anchor.** Volume-weighted population and
volume-weighted sample (n−1) variance differ by exactly `sqrt(n/(n−1))`, which
at **n = 2** is **√2 = 41.4%** — a separation no rounding, no timezone slip and
no source ambiguity can imitate. The Month anchor on a 1D chart held exactly two
bars. Measured against the operator's reading of the same candle:

| definition | Month (n=2) | Quarter (n=33) |
|---|---|---|
| **volume-weighted POPULATION** | **+0.003%** | **+0.002%** |
| volume-weighted SAMPLE (n−1) | **+41.43%** | +1.55% |
| unweighted population | +4.57% | −12.68% |
| unweighted sample | +47.88% | −11.33% |

The `(a)/(b)` ratio measured **1.4142**. All twelve bands then matched: max
|delta| **0.0452**, max **0.01 bps**. The Quarter anchor, at n=33, confirms only
weakly — as it must, since the two definitions differ there by 1.5%. **A parity
test that can only be passed by the right answer is worth more than a dozen that
everything passes.**

Status of each element, plainly:

| element | status |
|---|---|
| rolling VWAP source `hlc3` | **VERIFIED** — matches TradingView to the cent on 1D bars |
| anchored VWAP source `hlc3` | **VERIFIED** — an earlier reading implied `ohlc4`; traced to a chart *Source* setting difference between the two indicators and now resolved. Both forms use `hlc3`. |
| volume-weighted POPULATION variance, one-pass, no (n−1) | **VERIFIED** by the two-bar Month anchor, both forms |

The `ohlc4` episode is on the record deliberately: an inference held honestly and
flagged in the worksheet is what made it findable. An inference asserted as
pinned would have become a permanent, invisible offset on every anchored band.

### The substrate caveat — CLOSED for rolling VWAP, 2026-08-05

**Superseded.** For four cycles this section warned that every parity reading
had been taken on a **1D chart** and compared against **1D computation**, while
the instrument publishes on **1h** — so the path that actually runs had no
external check. TradingView computes RVWAP from the CHART's bars, which is what
made the gap real rather than pedantic, and also what makes it closable: a 1H
chart uses the same 168 hourly bars we do.

**The operator supplied a 1H capture on 2026-08-05 and the 1h path passed.**
BTCUSDT.P, closed bar `2026-08-05T17:00Z`, hlc3:

| window | bars in window | worst \|delta\| | worst bps |
|---|---|---|---|
| RVWAP 7d | 168 | 0.0453 | 0.0070 |
| RVWAP 30d | 720 | 0.0496 | 0.0079 |
| RVWAP 90d | 2,160 | 0.0494 | 0.0068 |
| RVWAP 365d | 8,760 | 0.0429 | 0.0056 |

All **28 values** (4 means + 24 band levels) agree within **0.0496** — the
rounding half-step of the operator's one-decimal display, so the residual is
his display precision and not our arithmetic. The RAW BAR matched to every
decimal first, so nothing downstream inherited a bad input.

**Rolling VWAP is therefore CERTIFIED on both substrates**, 1D and the ruled 1h.
The earlier "0.377 daily-ATR" figure was never a defect: it measured 1h-vs-1D
disagreement, which is a real and expected property of bar-granularity
weighting. Both are now independently confirmed against their own charts, which
is the only way that number could ever have been interpreted.

**STILL OPEN — anchored sigma on 1h.** The anchored MEANS matched on the same
bar (Month 63,602.4452 vs 63,602.4; Quarter 63,486.3109 vs 63,486.3), but the
operator's 1H capture **did not have anchored bands enabled**, so the anchored
SIGMA on the 1h substrate remains **UNVERIFIED**. The recipe and the variance
definition are verified (from the 2026-08-03 1D/hlc3 capture, where a two-bar
anchor discriminated population from sample by 41.4% and population landed
within 0.003%); only the substrate is untested, and the Month-anchor substrate
delta was measured at up to **0.186 daily-ATR**. **One 1H capture with anchored
bands enabled closes it. NOT BLOCKING.**

### ⚠ INSTRUMENT SENSITIVITY — read the right symbol or get a different level

**A census consumer that reads the wrong instrument gets a DISTINCT registry
level, not a rounding error.** Measured on the same `2026-08-05T17:00Z` bar:

| instrument | RVWAP 7d |
|---|---|
| `BINANCE:BTCUSDT.P` — **what we compute** | 63,737.7 |
| TradingView `BTCUSD` **INDEX** | 63,786.76 |
| **gap** | **49.06** |

Against BTC's daily ATR of 1,628.44, the collapse tolerance (`COLLAPSE_ATR`
0.02 ATR) is **32.57 points**. The instrument gap is **49.06 = 0.030 ATR =
1.51× the collapse tolerance** — so the two readings would **not** collapse into
one level. They would enter the registry as **two separate members**, and in a
system that scores by counting agreement, that is a phantom confluence: one
tool counted twice.

**Every VWAP number published by this toolkit is `BINANCE:BTCUSDT.P` and its
per-asset equivalents.** Any parity reading, screenshot, or citation taken from
an index, a spot pair, or another venue is measuring a different instrument and
must not be compared to ours without saying so.

### `stoch_rsi` — FINDING F-2R-A, and why F-AN-6b exists

**`stoch_rsi` returned all-NaN on every input, for its entire life.** `sma` is
cumsum-based, so a SINGLE leading NaN poisons every later value. The raw
stochastic always has a NaN prefix (RSI's own warm-up plus the stochastic
window), so `sma(raw, k)` was NaN everywhere. StochRSI — one of the four
oscillators §6.1 commissions — had never produced a number. Measured before the
fix: **100% of `stoch_rsi` values null in the 2026-08-03 capture, across all ten
assets and all five timeframes.**

Fixed by `_sma_after_warmup`, which applies the SMA from the first finite value
onward. Two choices inside it are deliberate:

1. **Fixed at the call site, not in `sma`.** Making `sma` NaN-tolerant would
   change every other consumer — including `awesome_oscillator`, whose input has
   no NaNs and whose published numbers must not move.
2. **Interior NaNs are NOT papered over.** A gap inside the finite region is a
   real discontinuity; smoothing across it would invent data. The result stays
   NaN and the caller sees the gap.

**Why this is a contract-level entry and not a changelog line.** F-AN-13 passed
it, every day, for months. Its assertion has a NaN-equals-NaN branch, and an
all-NaN series satisfies `got[k-1] == ref[k-1]` at every truncation point — the
fixture was structurally incapable of failing on this defect. **A guard that
cannot fail is not a guard.** F-AN-6b now asserts that every series function is
FINITE after its documented warm-up, which is the property F-AN-13 had assumed
without checking. Any consumer relying on a `SERIES_FUNCTIONS` member is relying
on F-AN-6b, not on F-AN-13, for the claim that a number exists at all.

### `resample_ohlcv` — closed buckets only

Aggregation is byte-identical to `scripts/s1_resample.aggregate()`:
`key = open_time // step * step`, then `first/max/min/last/sum`. (Byte-identity
is why pandas appears in an otherwise numpy-pure package: a numpy pairwise sum
differs from pandas' accumulation by 1 ULP on real volume data — measured max
abs 3.6e-12. A tolerance would have quietly lowered the bar the project sets
everywhere else.)

Two refusals, both in the direction of not guessing:

1. **Raises `UndecidableStepError`** (a `ValueError` subclass) when the source
   spacing cannot be inferred at all — fewer than two timestamps, or all
   identical. Previously the bucket was kept, so a single 1h bar handed to a 1d
   resample returned a "day" holding 1/24 of a day.
2. **Emits only buckets PROVED closed** by a bar in a strictly later bucket, so
   the final bucket is always dropped.

Rule 2 closes finding **F-1R-A**: the previous median-reach rule published a
bucket and then REVISED it whenever the median was decidable but
unrepresentative, which rule 1 never catches. No prefix-local heuristic closes
this — a sparse 2h-spaced day is informationally identical to a complete one
(uniform spacing, fully tiled, correct bar count). Median, minimum, uniformity
and tiling tests all pass on the sabotaged prefix. **The distinction simply is
not present in the data**, so closure is proved by one thing only: a bar exists
in a strictly later bucket.

Measured before adopting: across all ten estate assets, 1h→4h and 1h→1d, **20
combinations, identical bucket counts**. Live data always carries a forming final
bucket that both rules drop, so no published number moved.

`_resample_ohlcv_legacy` (test-only, not in `__all__`) reinstates the old
behaviour so F-AN-8b can prove the dropped bar is the only difference, and so the
forming candle can be DRAWN while never being computed with. A fixture asserts
that `scripts/daily_brief.py` contains no reference to that name.

## Record schemas

### Level record — the confluence registry input

```
{family, label, level, source_layer, timeframe}
```

`family` ∈ `vwap_anchored · vwap_rolling · profile_windowed · structure · ss`.
Rolling VWAPs are split from anchored ones so that no single TOOL TYPE can
dominate the diversity term by being prolific. `timeframe` carries the WINDOW
for windowed families and is load-bearing: §4.3 scale confirmation is keyed on
it. `LevelRegistry.add` RAISES on an unknown family and silently DROPS a NaN
level — a NaN is an absent level, not a level at an unknown price.

After `collapse_same_family` a member also carries `collapsed_from`,
`collapsed_count`, and — for `SCALE_FAMILIES`, when the group spans more than one
window — `scale_confirmed: ["7d","30d"]`.

Registry size, measured 2026-08-03 after the M/Q/Y period anchors and
`confirmed_pivots` were wired in: **~126–165 levels per asset** across the five
families. A citation of a cluster score must name the registry size that
produced it; the score is a count, and counts scale with population.

### Cluster record

```
{cluster_id, mean, members, member_count, score, families}
```

`score = Σ over families of min(count, FAMILY_CAP) + number of distinct
families`. **Counted, never fitted.** F-B28 asserts no weight vector,
coefficient array or fitted parameter exists anywhere in the scoring path — by
source scan, by AST (`score()` may contain no multiplication and no float
constant), and behaviourally (doubling every family's membership cannot double
the score; scores are integers).

Clustering is against the **RUNNING cluster mean**, not the seed level: a chain
of levels each within tolerance of its predecessor would otherwise smear one
"cluster" across an arbitrarily wide band.

Thresholds — `COLLAPSE_ATR 0.02 · CLUSTER_ATR 0.15 · LIS_ATR 1.5 · FAMILY_CAP 3`
— are **v1 placeholders** to be re-ratified against the calibration report.

### `dual_score` output — after the D-1 dedupe

Every capture is scored TWICE, with and without the volume families
(`vwap_rolling`, `profile_windowed`), so the operator sees daily whether volume
evidence MOVES HIS LINES. The excluded set is dropped at the **REGISTRY level,
before collapse** — removing it after clustering would leave clusters whose
means had already been pulled by volume levels, which is not the without-volume
answer at all, merely a relabelled with-volume one.

```
{
  with_volume:    {levels_in, member_count, clusters[], lines, sensitivity,
                   by_family, excluded_families},
  without_volume: { …same shape…, excluded_families: [vwap_rolling, profile_windowed] },
  differ:         {above: {...}, below: {...}, any_changed}
}
```

**There is no flat `members` list.** D-1 (reviewer ruling 2026-08-03): every
member lands in exactly one cluster, so emitting both stored the collapsed
registry TWICE — measured at 100,872 B, **18.12% of the 2026-08-03 capture**, and
growing with the registry. `clusters[].members` is the **single source of
truth**; `member_count` is retained so a reader can check the partition without
walking clusters. **A consumer that reads `dual_score(...)["with_volume"]
["members"]` is reading a field that no longer exists** — iterate
`clusters[].members`.

`lines` is `{above, below}`, each either `None` or a cluster record plus
`source: "primary" | "fallback"`. Primary is the highest-scoring cluster within
`LIS_ATR` daily-ATR on that side, ties broken by proximity; fallback is the
NEAREST cluster scoring ≥ 4 when nothing scores inside the reach, and it is
flagged so the report can say the line came from the fallback rather than the
rule.

`differ[side]` = `{changed, delta, delta_atr, with_volume, without_volume}`,
with `delta_atr` reported so the number is comparable across assets. When a line
exists in one view only, `delta` is `None` and a `note` says so — an incomparable
pair is not a zero.

`sensitivity` recomputes the ranking at `{0.10, 0.15, 0.20}` ATR and returns
`{tolerances, top3_by_tolerance, instability_chip, clusters_by_tolerance}`. It is
a first-class output, not a diagnostic someone might remember to run: an engine
that cannot announce its own fragility is a machine for producing false
confidence.

### Structure-derived invalidation and the R:R board

Consumed by the brief (`scripts/brief2.py`), specified here because the census
will read the numbers and must know how they were formed.

**Invalidation is the far edge of the NEXT CLUSTER BEYOND the entry cluster.**
It is NOT a function of the entry cluster's own width. The level fails when
price is through the next piece of structure past it — so dense structure gives
a tight stop, a void gives a wide one, and **both are true information**, which
a width-derived stop could never express because it knew only how wide one
cluster happened to be.

- Search reach `INVAL_SEARCH_ATR = 3.0` daily-ATR.
- When no cluster lies beyond within reach, the draft prints **with no R:R** and
  says why. A fabricated stop to complete a ratio would be the worst of both: a
  number that looks measured and is invented.
- `MIN_INVAL_ATR = 0.25` is a **CAUTION CHIP, not an exclusion gate.** It began
  as a floor (finding R-1: R:R is inversely proportional to invalidation
  distance, so the tightest and least survivable stops float to the top of a
  board sorted by R:R). The §7.2 conformance fix solved R-1 structurally —
  with invalidation BEYOND the far edge a 0.096-ATR stop is geometrically
  impossible and the floor of the geometry is ~0.15 ATR. Measured `inval_atr`
  then spanned **0.244–0.276**, a 0.03 spread, so excluding 2 of 12 rows on it
  was an arbitrary cut wearing the appearance of a principle. Rows below the
  threshold now print ON the ranked board carrying a chip; nothing is excluded.
- `R:R = |target − entry| / |entry − invalidation|`, every component printed so
  the operator can recompute by hand. F-B29 asserts exactly that: no ratio prints
  without entry, invalidation and target all present, and every printed ratio
  recomputes from its own components.

**The board ranks STRUCTURAL QUALITY, not probability.** A high R:R means the
geometry is favourable and nothing more.

### Value-area / nesting record

```
{state, overlap_frac, consensus_band, gap_band, facing_edges,
 short_va, long_va}  +  price_location(price, nest)
```

`state` ∈ `nested_inside · nested_outside · overlapping · disjoint_above ·
disjoint_below`, or `None` when either value area is undefined — a warming 365d
window has no VA, and inventing one would be exactly the mislabelling the
warm-up rule forbids.

`overlap_frac` divides by the **SHORTER** value area, so it reads as "how much of
short-term value has long-term backing". Dividing by the union or by the longer
VA would make a tiny short VA nested inside a huge long VA look like weak
agreement rather than total agreement. A zero-width short VA touching the long VA
returns `1.0`, not NaN — the strongest possible case must not report as missing.

When disjoint, the `gap_band` edges are the FACING edges: the ones price meets
first coming from either side. `nesting_levels` emits consensus and gap edges
into the registry under `profile_windowed` with `timeframe = "7d<->30d"` form and
a `facing_edge` flag.

Pairs are ADJACENT SCALES only: `7d↔30d, 30d↔90d, 90d↔365d`. Comparing 7d to
365d directly would answer a question no one asked and double-count the
intermediate windows the confluence engine already sees.

**Scale confirmation does not add score.** Nested windows share data — the 30-day
window *contains* the 7-day window — so they are partially dependent voices.
Partial dependence deserves fractional credit, and the project's law is
counted-never-weighted, which forbids fractions. The mechanism by which it adds
nothing is STRUCTURAL rather than a special case: the coincident levels become
ONE member, so the family's member count is unchanged and `score` cannot see them
as two voices. Conservative scoring plus full visibility is the honest treatment
of a voice we cannot weigh.

### Windowed profile record

```
{poc, vah, val, edges, hist, lvns[], warming, bars, history_start_ms,
 window_days, window_start_ms, as_of_ms, bins, value_area, substrate,
 lockbox_overlap, approximation}
```

Window membership matches the RVWAP convention exactly — `bar_open_time >
as_of_ms − W`, bars after `as_of_ms` excluded outright — so a 30d VWAP and a 30d
profile never disagree about which bars are "the last 30 days". Sharing the
convention is the point; disagreement there would be an invisible and permanent
source of level drift.

**Warm-up honesty is COVERAGE, not bar count.** The check is whether the DATA
reaches back to the window start, not whether enough bars were selected. An asset
listed inside the window has plenty of bars and still cannot claim it;
`warming=True` prints a chip and **no number**, because a 365d profile computed on
200 days is a 200-day profile wearing the wrong label.

**Known gap, reported not fixed:** the anchored-VWAP warming predicate in the
consuming brief is `zero bars` and nothing else — there is **no minimum-sample
rule for anchored bands**. On 2026-08-03 the W anchor was armed on 21 bars and 24
anchored band levels entered the confluence registry; on a 1D chart the Month
anchor's six bands would rest on **two data points**. A VWAP *line* at 2 bars is
still a true volume-weighted mean; a *sigma* at 2 bars is arithmetically exact and
informationally empty. Decision DA-2 is open with the reviewer.

LVN threshold is relative to the **MEDIAN** row volume, not the mean — a profile
is strongly peaked at the POC, so a mean-relative threshold classifies ordinary
rows as low-volume on any well-formed profile. Runs touching either extreme are
discarded: the rows at a window's edges are always thin by construction, and
calling those LVNs would emit two guaranteed, information-free levels per window
per asset — ten per asset across five windows, inflating every score.

## Lockbox

`LOCKBOX_START_MS · LOCKBOX_END_MS` = `[2024-07-01, 2025-10-06)`.

`lockbox_overlap(start_ms, end_ms)` is a **DISCLOSURE utility, never a refusal.**
Operator ruling 2026-08-03: the seal governs **scored outcome evidence** — replay
journals, outcome statistics, anything the census may later grade — and not raw
price inside a display-only trailing indicator window. The ruling was granted ON
CONDITION that the overlap is disclosed, so every windowed layer carries the
record; a brief that silently read across the holdout would be exactly what the
condition forbids.

Measured 2026-08-03: of `{7,30,90,365}d`, only the **365d** window reaches the
holdout, by **64.115 days**, self-clearing **2026-10-06**. 7/30/90d are clear by
construction and will stay clear. The G-1 code guard on the replay path is
untouched.

## Firewall

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or
implied. No engine change. No forward scoring. No fitted weights. No estate
mutation. **No sizing, ever. No probability claims, ever.**

**Confluence scores measure AGREEMENT BETWEEN TOOLS, not edge. R:R measures
GEOMETRY, not probability.** Whether any of it predicts anything is census work
under G-7, and the four candidates — **CENSUS-1d, H-RVX, H-M1X, H-VAN** — are
routed to APOLLO, not answered here.

The daily brief is an OPS artifact and is **never** study evidence. The firewall
between them is the project's central discipline; a number's appearance in a
brief confers no evidentiary standing on it whatsoever.

Adoption is gated separately from build: nothing consumes these numbers until the
fixtures are green **and** the operator's parity readings match. Two recipes are
now verified by reading (rolling and anchored VWAP source, both variance
definitions) and the substrate they are computed on is not. Until certification,
every render prints **`PARITY NOT CERTIFIED`**.

---

## Capture-side layers APOLLO will cite (added 2026-08-03, cycle 4)

These live in `scripts/brief2.py`, not in `analytics/`, because they compose the
package's outputs rather than compute new arithmetic. They are documented here
because they are the SUBSTRATE for the census candidates routed to APOLLO, and a
census that cannot cite their shape cannot use them.

### Stretch record (D.5) — one row per volume-weighted mean

```
{name, kind, warming, mean, sigma, bars,
 sigma_position,        # (price - mean) / sigma, SIGNED
 bps, atr,              # the same distance in two other units
 thin_sample,           # True when bars < 30
 band_reached}          # outermost sigma band price has reached, signed; 0 if none
```

`kind` ∈ `anchored · prior_anchor · rolling`. Covers developing W/M/Q/Y, prior
M/Q/Y, and rolling 7/30/90/365 — every volume-weighted mean in the instrument on
one comparable scale.

**Why three units.** `bps` is scale-free, `atr` is volatility-relative, and
`sigma_position` is relative to that tool's OWN dispersion — which is the only
one of the three that makes two different anchors comparable to each other.

**`thin_sample` is not cosmetic.** A sigma over two bars is the spread between
two numbers: arithmetically exact, informationally empty as a dispersion
estimate. The value is FLAGGED, never silently suppressed and never silently
trusted. Any census use of `sigma_position` should filter or stratify on it.

The layer also records the MULTI-SCALE DISAGREEMENT: max and min
`sigma_position`, which two disagree most, the spread, and whether the pair
straddles ±1σ. Measured on BTCUSDT 2026-08-03: `anchored M` at +1.38σ while
`prior Y` sat at −2.94σ — overextended up against the month and down against the
year at the same instant. Both true; the disagreement is the object.

### Band-excursion record (D.6) — recording only

```
{name, kind, side, band_reached, sigma_position, bars, thin_sample,
 distance_to_mean_sigma, distance_to_mean_atr, returned_to_mean,
 recording_only: true}
```

**No "captures since last touch" counter is stored.** A capture is a point in
time and must stay self-describing; a stored counter is state the capture cannot
verify about itself, and `brief_panel.py` rebuilds every partition FROM CAPTURES
ALONE. The since-last-touch series is DERIVED at panel-build time from the stored
`band_reached` column, where it is reproducible from the archive rather than
trusted from a counter.

**RECORDING IS OPS.** Whether a band touch pays anything is **H-VBR** under G-7.
Nothing in this layer claims it does, and the deflation gauge for H-VBR is stated
in the routing note: a σ2 touch is BY CONSTRUCTION "price is far from its recent
volume-weighted mean", so it must beat a plain distance-from-mean or
ATR-extension baseline or be filed as a redundant dressing of a simpler fact.
