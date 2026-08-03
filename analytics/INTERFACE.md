# `analytics/` — INTERFACE

**The census-facing contract.** APOLLO cites this file; it is the stable
description of what `analytics/` computes, under which conventions, and with
which causality class. Nothing here is evidence of edge — see the firewall at
the end.

- `ANALYTICS_VERSION` **1.2.0**
- `analytics_sha()` — sha256 over the package sources in fixed order, binary
  reads. Printed beside the version by every artifact that consumes this
  toolbox, so a stored capture can always name the exact code that produced it.
- Modules hashed: `__init__ · momentum · vwap · volatility · profile ·
  structure · levels · stats · parity · nesting`

## Invariants

| id | invariant |
|---|---|
| I-A | No I/O. `analytics_sha()` is the one exception and is a PROVENANCE function, not a computation one; it uses `pathlib.Path.read_bytes()`, never the builtin `open(`. F-AN-4 scans for it. |
| I-B | No imports from `engine/` or `scripts/`. F-AN-3 asserts it. |
| I-D | Warm-up honesty: a function returns NaN for exactly the documented number of leading positions and a finite value immediately after. It never seeds a number into the warm-up region to make a chart look continuous. |
| I-F | Any change to a returned NUMBER bumps at least the minor version. Archive comparability depends on it. |

## Causality classes

The class is part of the contract, not a comment. It is what tells a consumer
whether a value may be used at a historical decision bar.

| class | meaning | fixture |
|---|---|---|
| `causal` | output at `i` depends only on input `[0..i]` | F-AN-13 truncation-prefix |
| `lag:N` | output at `i` is knowable only at `i+N` | F-AN-13 at lag |
| `endpoint_only` | valid only at the end of the supplied array; MUST raise if asked for a mid-array value | exempt, but the raise is asserted |

**F-AN-13** is the fixture that matters most: `f(x[:k])[k-1] == f(x)[k-1]`,
exactly, at five truncation points, over every series-returning public function.
It exists to abolish caller-contract dependencies as a CLASS rather than to fix
located instances.

**F-AN-13b** (Amendment 2 §1.1) extends the discipline to five functions whose
signatures the naive form does not fit. The naive form is *vacuous* on all five —
measured against deliberately sabotaged implementations it certifies non-causal
code as green — so each is covered in the form its signature actually admits:

| function | form |
|---|---|
| `vw_sigma_bands` | COMPOSED: truncate the raw series, recompute the producer, then band. Truncating its own arguments is satisfied by any element-wise map, including one handed a look-ahead stdev. |
| `divergences` | lag:5 STRUCTURAL INVARIANTS, both regular and hidden. A prefix-vs-full equality is a tautology here: at N=5 both sides receive bit-identical pivot arrays. |
| `naked_poc_registry` | SET-MEMBERSHIP STABILITY on hand-built geometry. A random series does not discriminate a registry that reads one bar past the decision bar. |
| `confirmed_pivots` | SET STABILITY plus as-of at and BEYOND the array end, where the two real mutations bite. |
| `resample_ohlcv` | BUCKET-AXIS prefix: growing the input only APPENDS buckets, never revises one already emitted. |

All eleven behaviour-changing mutants tried against these fixtures are caught,
and every fixture carries an explicit non-emptiness precondition.

## Recipes (`CONVENTIONS`)

Every entry is the exact variant, pinned. Highlights that consumers get wrong:

- **`rolling_vwap`** — TradingView RVWAP, pinned from source. Trailing **W
  milliseconds** (not a bar count) floored at the 10 most recent bars; `src =
  hlc3`; volume-weighted **POPULATION** variance via the one-pass identity
  `max(E[x²] − E[x]², 0)`. **No (n−1) correction.** The zero-clamp is
  ALGORITHMIC, not defensive padding — the one-pass identity can go slightly
  negative through cancellation at high price with low dispersion.
- **`anchored_vwap`** — same band machinery, but that sharing is a REASONED
  INFERENCE, not read from source. Flagged in the parity worksheet; never assert
  it as pinned.
- **`volume_profile`** — volume spread uniformly across each bar's range. This
  is an **APPROXIMATION** of tick data and every consumer carries the
  `approximation` provenance chip. Non-removable.
- **`percentile_rank`** — `endpoint_only`; raises if `as_of_index` is not the
  sample end.

### `resample_ohlcv` — closed buckets only

Aggregation is byte-identical to `scripts/s1_resample.aggregate()`:
`key = open_time // step * step`, then `first/max/min/last/sum`.

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
(uniform spacing, fully tiled, correct bar count).

Measured before adopting: across all ten estate assets, 1h→4h and 1h→1d, **20
combinations, identical bucket counts**. Live data always carries a forming final
bucket that both rules drop.

`_resample_ohlcv_legacy` (test-only, not in `__all__`) reinstates the old
behaviour so F-AN-8b can prove the dropped bar is the only difference, and so the
forming candle can be DRAWN while never being computed with.

## Level and value-area record schema

### Level record — the confluence registry input

```
{family, label, level, source_layer, timeframe}
```

`family` ∈ `vwap_anchored · vwap_rolling · profile_windowed · structure · ss`
(Amendment 2 §5.1). `timeframe` carries the WINDOW for windowed families and is
load-bearing: §4.3 scale confirmation is keyed on it.

After `collapse_same_family` a member also carries `collapsed_from`,
`collapsed_count`, and — for `SCALE_FAMILIES`, when the group spans more than one
window — `scale_confirmed: ["7d","30d"]`.

### Cluster record

```
{cluster_id, mean, members, member_count, score, families}
```

`score = Σ over families of min(count, FAMILY_CAP) + number of distinct families`.
**Counted, never fitted.** F-B28 asserts no weight vector, coefficient array or
fitted parameter exists anywhere in the scoring path — by source scan, by AST
(`score()` may contain no multiplication and no float constant), and
behaviourally (doubling every family's membership cannot double the score;
scores are integers).

Thresholds — `COLLAPSE_ATR 0.02 · CLUSTER_ATR 0.15 · LIS_ATR 1.5 · FAMILY_CAP 3`
— are **v1 placeholders** to be re-ratified against the calibration report.

### Value-area / nesting record

```
{state, overlap_frac, consensus_band, gap_band, facing_edges, price_location}
```

`state` ∈ `nested_inside · nested_outside · overlapping · disjoint_above ·
disjoint_below`. `overlap_frac` divides by the **SHORTER** value area, so it
reads as "how much of short-term value has long-term backing"; a zero-width short
VA touching the long VA returns `1.0`, not NaN.

Pairs are ADJACENT SCALES only: `7d↔30d, 30d↔90d, 90d↔365d`.

**Scale confirmation does not add score.** Nested windows share data — the 30-day
window *contains* the 7-day window — so they are partially dependent voices.
Partial dependence deserves fractional credit, and the project's law is
counted-never-weighted, which forbids fractions. Conservative scoring plus full
visibility is the honest treatment of a voice we cannot weigh.

### Windowed profile record

```
{poc, vah, val, lvns[], warming, bars, substrate, window_start_ms,
 lockbox_overlap, approximation}
```

**Warm-up honesty is COVERAGE, not bar count.** An asset listed inside the window
has plenty of bars and still cannot claim it; `warming=True` prints a chip and
**no number**, because a 365d VWAP computed on 200 days is a 200-day VWAP wearing
the wrong label.

LVN threshold is relative to the **MEDIAN** row volume, not the mean — a profile
is strongly peaked at the POC, so a mean-relative threshold classifies ordinary
rows as low-volume on any well-formed profile. Runs touching either extreme are
discarded: the rows at a window's edges are always thin by construction.

## Lockbox

`LOCKBOX_START_MS · LOCKBOX_END_MS` = `[2024-07-01, 2025-10-06)`.

`lockbox_overlap(start_ms, end_ms)` is a **DISCLOSURE utility, never a refusal.**
Operator ruling 2026-08-03: the seal governs **scored outcome evidence** — replay
journals, outcome statistics, anything the census may later grade — and not raw
price inside a display-only trailing indicator window. The ruling was granted ON
CONDITION that the overlap is disclosed, so every windowed layer carries the
record.

Measured 2026-08-03: of `{7,30,90,365}d`, only the **365d** window reaches the
holdout, by **64.115 days**, self-clearing **2026-10-06**. The G-1 code guard on
the replay path is untouched.

## Firewall

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or
implied. No engine change. No forward scoring. No fitted weights. No estate
mutation.

**Confluence scores measure AGREEMENT BETWEEN TOOLS, not edge. R:R measures
GEOMETRY, not probability.** Whether any of it predicts anything is census work
under G-7, and the four candidates — **CENSUS-1d, H-RVX, H-M1X, H-VAN** — are
routed to APOLLO, not answered here.

Adoption is gated separately from build: nothing consumes these numbers until the
fixtures are green **and** the operator's parity readings match. Until then every
render prints `PARITY NOT CERTIFIED`.
