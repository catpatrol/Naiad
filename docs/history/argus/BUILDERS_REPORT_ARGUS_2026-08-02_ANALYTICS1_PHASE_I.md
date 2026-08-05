# BUILDER'S REPORT — ANALYTICS-1 Phase I

**Lane:** HEPHAESTUS (builder) · **Reviewer lane:** ARGUS · **Date:** 2026-08-02
**Contract:** `prompts/CONTRACT_v4_ANALYTICS1_BRIEF2_FORWARD0.md` + Amendment FAN8
**Commit:** `c1d8e668f7b6e178037b09f1f2d75b8e9e994ac9` (`c1d8e66`) — committed, NOT pushed

> **Status: PHASE I COMPLETE. ADOPTION GATED.** Nothing in `analytics/` is adopted until the
> operator returns the parity worksheet with chart readings. No partial adoption; CENSUS-2b,
> CENSUS-1d and H-RVX all wait behind it.

This document is written to be read with **zero prior context**. It is the record of the run;
the terminal output it replaces is not the record.

---

## (a) Environment gate and probe

| check | kind | value | result |
|---|---|---|---|
| branch | HARD | `v12-v1-census` | PASS |
| pwd | HARD | `C:\Users\luisf\OneDrive\Desktop\Midas-Claude Code Resources\naiad` | PASS |
| pwd contains `\Users\` | HARD | True | PASS |
| pwd contains `OneDrive` | HARD | True | PASS |
| `engine/` exists | HARD | True | PASS |
| `prompts/` exists | HARD | True | PASS |
| HEAD at gate | INFO | `c38a0ae` | reported, never gated |

**Probe — `analytics/` module set.** Required `{__init__, momentum, vwap, volatility, profile, structure, levels, stats, parity}.py`.

```
found    : __init__, levels, momentum, parity, profile, stats, structure, volatility, vwap
expected : __init__, levels, momentum, parity, profile, stats, structure, volatility, vwap
missing  : (none)      extra : (none)      MATCH : True
```

### Probe deviation, and how it was resolved

The paste described `analytics/` as *"uncommitted, v1.0.0, from the 2026-07-28 Phase I build"*.
**It is not uncommitted.** All nine files are git-TRACKED, committed earlier the same day by
`9470d04` ("base"), a commit made from this clone by another agent session.

Resolution: the probe's HARD condition is the **module set**, and that matched exactly — nine
of nine, nothing missing, nothing extra. Tracked-vs-untracked is a repository-state fact, not a
module-identity fact, and the paste itself said *"much repo work happened in other lanes since;
verify, never assume."* So the deviation was **reported and the build proceeded**, rather than
halting on a stale expectation about a file's git status. Had a module been missing or renamed,
that would have been a halt.

## (b) Amendment

| field | value |
|---|---|
| path | `prompts/CONTRACT_v4_Amendment_FAN8.md` |
| bytes | 826 |
| sha256 | `2017fe6636987afd39fa49197424482d5ec69661b8f2df6dd0e9b565da75987f` |

Saved verbatim, including its delimiter banners. Content, for the record:

```
==================== AMENDMENT FAN8 to CONTRACT v4 ====================
Ratified by operator (drop the unclosed bar; F-B17/G1 win) and by interview G-2 bundle 2026-08-02. F-AN-8 is restructured, not waived: 8a unchanged-conventions exact · 8b legacy-mode exact (test-only, production-unreachable) · 8c documented diff with verdict impact. Rationale on record: preserving the bucket would enshrine a known defect to protect a number now known to be wrong; closed-bar values are reproducible and parity-coherent (worksheet reads closed candles). Disclosed cost: the brief shows the last FINISHED 4h/12h/1d reading, not the live forming one the chart shows mid-candle. rules_version bumps to 2.0.0 at BRIEF-2 (ratified A-6); the 8c diff table is the bridge between eras.
==================== END AMENDMENT ====================
```

## (c) Fixture transcript — F-AN-1..14, all 41 items

Invocation: `python -m pytest tests/test_analytics.py -q`

```
PASSED  test_f_an_1_golden_values
PASSED  test_f_an_2_determinism
PASSED  test_f_an_3_no_engine_imports
PASSED  test_f_an_4_no_io
PASSED  test_f_an_5_analytics_sha_reproducible
PASSED  test_f_an_6_warmup_lengths
PASSED  test_f_an_7_edge_cases
PASSED  test_f_an_9_cluster_reproducibility
PASSED  test_f_an_10_rvwap_window_and_floor
PASSED  test_f_an_11_variance_stability
PASSED  test_f_an_12_pivot_confirmation_lag
PASSED  test_f_an_13_causality_truncation_prefix[sma]
PASSED  test_f_an_13_causality_truncation_prefix[ema]
PASSED  test_f_an_13_causality_truncation_prefix[rma]
PASSED  test_f_an_13_causality_truncation_prefix[rsi]
PASSED  test_f_an_13_causality_truncation_prefix[stoch_rsi_k]
PASSED  test_f_an_13_causality_truncation_prefix[stoch_rsi_d]
PASSED  test_f_an_13_causality_truncation_prefix[macd_line]
PASSED  test_f_an_13_causality_truncation_prefix[macd_signal]
PASSED  test_f_an_13_causality_truncation_prefix[macd_hist]
PASSED  test_f_an_13_causality_truncation_prefix[awesome_oscillator]
PASSED  test_f_an_13_causality_truncation_prefix[true_range]
PASSED  test_f_an_13_causality_truncation_prefix[atr]
PASSED  test_f_an_13_causality_truncation_prefix[realised_vol]
PASSED  test_f_an_13_causality_truncation_prefix[rolling_vwap]
PASSED  test_f_an_13_causality_truncation_prefix[rolling_vwap_sd]
PASSED  test_f_an_13_causality_truncation_prefix[anchored_vwap]
PASSED  test_f_an_13_causality_truncation_prefix[zscore]
PASSED  test_f_an_13_causality_truncation_prefix[correlation]
PASSED  test_f_an_13_causality_truncation_prefix[beta]
PASSED  test_f_an_13_causality_truncation_prefix[period_opens]
PASSED  test_f_an_13_causality_truncation_prefix[prior_period_extremes_h]
PASSED  test_f_an_13_endpoint_only_raises
PASSED  test_f_an_13_lag_functions_at_lag
PASSED  test_f_an_14_resample_parity
PASSED  test_f_an_14b_public_is_legacy_minus_unclosed
PASSED  test_f_an_14c_undecidable_closure_keeps_the_bucket
PASSED  test_f_an_8a_unchanged_conventions_reproduce_exactly
PASSED  test_f_an_8b_legacy_mode_reproduces_v1_1_exactly
PASSED  test_f_an_8b_legacy_is_unreachable_from_production
PASSED  test_f_an_8c_documented_diff
```

**41 passed, exit code 0.**

Whole-repo suite at the time of the Phase I commit: **73 passed, 1 skipped, 0 failed** — no
regression. (The single skip is pre-existing: `fixtures/test_f8_journal.py:110`, dry-run journal
not generated, D7.)

## (d) F-AN-8a — unchanged conventions reproduce v1.1 exactly · 12/12

A recipe's convention did NOT change where the brief sources it **natively** — no resampling is
involved, so the dropped bucket cannot affect it. Those are `rsi14@1h` and `atr14@1h/4h/12h`.

The three values named in the contract paste, reproduced:

| asset | recipe | ours | published v1.1 | match |
|---|---|---:|---:|---|
| BTCUSDT | rsi14 @ 1h | 52.470485 | 52.4705 | YES |
| ETHUSDT | rsi14 @ 1h | 56.992236 | 56.9922 | YES |
| SOLUSDT | rsi14 @ 1h | 50.775898 | 50.7759 | YES |

All twelve unchanged-convention comparisons:

| asset | tf | recipe | ours | published v1.1 | match |
|---|---|---|---:|---:|---|
| BTCUSDT | 1h | rsi14 | 52.470485 | 52.4705 | YES |
| BTCUSDT | 1h | atr14 | 335.714935 | 335.71493546 | YES |
| BTCUSDT | 4h | atr14 | 627.956348 | 627.95634802 | YES |
| BTCUSDT | 12h | atr14 | 1047.411676 | 1047.41167624 | YES |
| ETHUSDT | 1h | rsi14 | 56.992236 | 56.9922 | YES |
| ETHUSDT | 1h | atr14 | 16.771190 | 16.77119037 | YES |
| ETHUSDT | 4h | atr14 | 29.903735 | 29.90373524 | YES |
| ETHUSDT | 12h | atr14 | 45.275231 | 45.27523091 | YES |
| SOLUSDT | 1h | rsi14 | 50.775898 | 50.7759 | YES |
| SOLUSDT | 1h | atr14 | 0.568621 | 0.56862077 | YES |
| SOLUSDT | 4h | atr14 | 1.096100 | 1.09610017 | YES |
| SOLUSDT | 12h | atr14 | 1.779953 | 1.77995285 | YES |

**8a RESULT: 12/12 match. PASS.**

## (e) F-AN-8b — legacy mode reproduces v1.1 exactly · 12/12, PER RECIPE

This is the load-bearing fixture of the amendment. A **test-only** construction reinstates the
in-progress resample bucket and recomputes. If that reproduces the published number, then the
dropped bar is the **only** thing that changed. If it did not, something else moved and that
would be a finding, not a tolerance to widen.

| asset | tf | recipe | legacy (bucket reinstated) | published v1.1 | EXACT MATCH |
|---|---|---|---:|---:|---|
| BTCUSDT | 4h | rsi14 | 44.134105 | 44.1341 | **YES** |
| BTCUSDT | 12h | rsi14 | 46.232218 | 46.2322 | **YES** |
| BTCUSDT | 1d | rsi14 | 48.676588 | 48.6766 | **YES** |
| BTCUSDT | 1d | atr14 | 1689.205918 | 1689.2059176 | **YES** |
| ETHUSDT | 4h | rsi14 | 54.753564 | 54.7536 | **YES** |
| ETHUSDT | 12h | rsi14 | 56.846935 | 56.8469 | **YES** |
| ETHUSDT | 1d | rsi14 | 58.432884 | 58.4329 | **YES** |
| ETHUSDT | 1d | atr14 | 70.281379 | 70.28137933 | **YES** |
| SOLUSDT | 4h | rsi14 | 43.710369 | 43.7104 | **YES** |
| SOLUSDT | 12h | rsi14 | 42.662019 | 42.662 | **YES** |
| SOLUSDT | 1d | rsi14 | 44.664161 | 44.6642 | **YES** |
| SOLUSDT | 1d | atr14 | 2.827273 | 2.82727325 | **YES** |

**8b RESULT: 12/12 EXACT. ALL EXACT = True. PASS.**

**Production-unreachability, fixture-asserted.** Legacy mode is
`analytics/structure.py::_resample_ohlcv_legacy` — underscore-prefixed and absent from
`__all__`. `test_f_an_8b_legacy_is_unreachable_from_production` asserts that
`scripts/daily_brief.py` contains neither the name `_resample_ohlcv_legacy` nor the flag
`drop_unclosed`, so it cannot leak into production by drift.

## (f) F-AN-8c — the full documented diff, all 24 comparisons

**This table is the bridge between eras.** It is reproduced in full, not summarised: every
value the brief published on the frozen fixture day, beside what the corrected closed-bar
convention produces.

Legend — *convention changed* = the layer is resampled from 1h, so dropping the forming bucket
moves it. *unchanged* = natively sourced, unaffected by construction.

| # | asset | tf | recipe | source | v1.1 published | corrected | delta | verdict |
|---:|---|---|---|---|---:|---:|---:|---|
| 1 | BTCUSDT | 12h | atr14 | native | 1047.41167624 | 1047.411676 | +0.000000 | — |
| 2 | BTCUSDT | 1d | atr14 | resampled from 1h | 1689.2059176 | 1709.575604 | +20.369686 | — |
| 3 | BTCUSDT | 1h | atr14 | native | 335.71493546 | 335.714935 | +0.000000 | — |
| 4 | BTCUSDT | 4h | atr14 | native | 627.95634802 | 627.956348 | -0.000000 | — |
| 5 | BTCUSDT | 12h | rsi14 | resampled from 1h | 46.2322 | 41.912049 | -4.320151 | `rsi12h_bull_side` unchanged (False) |
| 6 | BTCUSDT | 1d | rsi14 | resampled from 1h | 48.6766 | 47.638606 | -1.037994 | — |
| 7 | BTCUSDT | 1h | rsi14 | native | 52.4705 | 52.470485 | -0.000015 | — |
| 8 | BTCUSDT | 4h | rsi14 | resampled from 1h | 44.1341 | 43.125094 | -1.009006 | `rsi4h_bull_side` unchanged (False) |
| 9 | ETHUSDT | 12h | atr14 | native | 45.27523091 | 45.275231 | -0.000000 | — |
| 10 | ETHUSDT | 1d | atr14 | resampled from 1h | 70.28137933 | 70.066101 | -0.215279 | — |
| 11 | ETHUSDT | 1h | atr14 | native | 16.77119037 | 16.771190 | +0.000000 | — |
| 12 | ETHUSDT | 4h | atr14 | native | 29.90373524 | 29.903735 | +0.000000 | — |
| 13 | ETHUSDT | 12h | rsi14 | resampled from 1h | 56.8469 | 49.611868 | -7.235032 | **FLIP** `rsi12h_bull_side` True → False |
| 14 | ETHUSDT | 1d | rsi14 | resampled from 1h | 58.4329 | 55.571813 | -2.861087 | — |
| 15 | ETHUSDT | 1h | rsi14 | native | 56.9922 | 56.992236 | +0.000036 | — |
| 16 | ETHUSDT | 4h | rsi14 | resampled from 1h | 54.7536 | 54.342723 | -0.410877 | `rsi4h_bull_side` unchanged (True) |
| 17 | SOLUSDT | 12h | atr14 | native | 1.77995285 | 1.779953 | -0.000000 | — |
| 18 | SOLUSDT | 1d | atr14 | resampled from 1h | 2.82727325 | 2.871679 | +0.044406 | — |
| 19 | SOLUSDT | 1h | atr14 | native | 0.56862077 | 0.568621 | -0.000000 | — |
| 20 | SOLUSDT | 4h | atr14 | native | 1.09610017 | 1.096100 | +0.000000 | — |
| 21 | SOLUSDT | 12h | rsi14 | resampled from 1h | 42.662 | 37.602192 | -5.059808 | `rsi12h_bull_side` unchanged (False) |
| 22 | SOLUSDT | 1d | rsi14 | resampled from 1h | 44.6642 | 44.786085 | +0.121885 | — |
| 23 | SOLUSDT | 1h | rsi14 | native | 50.7759 | 50.775898 | -0.000002 | — |
| 24 | SOLUSDT | 4h | rsi14 | resampled from 1h | 43.7104 | 44.896869 | +1.186469 | `rsi4h_bull_side` unchanged (False) |

### Headline

| measure | value |
|---|---:|
| comparisons | 24 |
| unchanged convention | 12 |
| changed convention | 12 |
| **published values that moved** | **12** |
| **verdict flips** | **1** |

### Verdict changes — the downstream consequence

Two momentum confluence votes read these layers (`daily_brief.py:1241-1242`):

```
fl["rsi4h_bull_side"]  = bool((r.get("4h",  {}).get("value") or 0) > 50)
fl["rsi12h_bull_side"] = bool((r.get("12h", {}).get("value") or 0) > 50)
```

so a corrected value crossing 50 flips a published vote.

| asset | flag | v1.1 | corrected | published value | corrected value |
|---|---|---|---|---:|---:|
| ETHUSDT | `rsi12h_bull_side` | True | **False** | 56.8469 | 49.6119 |

**Read this plainly:** ETHUSDT's 12h RSI was published as 56.85, computed from a 12h bar
that was still forming. The last *finished* 12h bar reads 49.61. The vote was true; it is
false. That is a live confluence flag changing on a live asset, and it is exactly the class
of thing the operator's ruling was made to stop producing.

### Why only these layers

`scripts/daily_brief.py` sources its timeframes two different ways, and that determines
precisely which numbers moved:

- **RSI** (`rsi_layer`, line 521-522): 1h is native; **2h/4h/12h/1d are resampled from 1h**.
- **ATR** (`volatility_layer` reading `load_all`, line 1513): 1h/4h/12h are **native loads**;
  **1d is resampled from 1h**.

So `rsi@4h/12h/1d` and `atr@1d` changed; `rsi@1h` and `atr@1h/4h/12h` did not. The v1.1 daily
bar was built from a **single 1h bar** and published as a day.

## (g) Version, hash, commit, files

| field | value |
|---|---|
| ANALYTICS_VERSION | `1.0.0` → **`1.1.0`** (I-F: returned numbers changed) |
| analytics_sha | `a7ff1911848bb30561e477186dc62ed1a4ff3daf39bfe9d42371f3353815e046` |
| commit | `c1d8e668f7b6e178037b09f1f2d75b8e9e994ac9` (`c1d8e66`) |
| author | `catpatrol <catpatrolling@gmail.com>` |
| pushed | **NO** — repo work is commit-no-push by standing rule |

Files in the commit — everything needed to reproduce from a clean checkout:

```
M  analytics/__init__.py                  version bump + CONVENTIONS entry
M  analytics/structure.py                 the drop, the closure predicate, legacy mode
M  tests/test_analytics.py                8a/8b/8c + F-AN-14b/14c
A  scripts/parity_worksheet.py            the worksheet generator
A  prompts/CONTRACT_v4_Amendment_FAN8.md  the amendment
M  LEDGER.md                              verbatim entry + builder record
6 files changed, 1426 insertions(+), 892 deletions(-)
```

### What the change actually is

`analytics/structure.py::resample_ohlcv` gained `drop_unclosed=True`. The final bucket is
dropped when the source data does not reach its end. Closure is decided by **time, not by bar
count** — see the verification answers filed alongside this report.

## (h) Findings — reported, not fixed

### 1. `pytest.ini` did not collect the analytics regression guard

`pytest.ini` read `testpaths = fixtures`. `tests/test_analytics.py` was therefore **never
collected by a bare `pytest` run** — the entire F-AN-1..14 guard existed and did not execute
unless a human named the file. That is why the repo suite reported 73 tests while F-AN has 41
of its own.

At Phase I this was **reported and left alone**, because changing repo-wide test collection is
not a Phase I change and "halt-and-ask beats improvisation." It was corrected in the following
cycle under an explicit operator gate that required proving the collection delta contained
nothing but the analytics tests.

### 2. `f_an_14b` failed on its first run — and the TEST was wrong, not the code

The new fixture asserted that 480 hourly bars form 20 complete days, so the final day should
survive the drop. It failed.

The code was right and the assumption was wrong: `_series()` starts at epoch
`1_600_000_000_000`, which is **12:26:40 UTC — not a day boundary**. No prefix of that series
can ever end on one, so the final day genuinely was incomplete and the drop was correct.

The fix was to **rebuild the assertion on a day-aligned span**, with the alignment itself
asserted so the fixture cannot silently rot:

```python
t2 = (np.arange(48) * 3_600_000) + (1_600_000_000_000 // DAY_MS) * DAY_MS
assert t2[0] % DAY_MS == 0 and (t2[-1] + 3_600_000) % DAY_MS == 0, \
    "the aligned fixture must start and end exactly on a day boundary"
```

Recorded because the alternative — relaxing the assertion until it passed — would have
destroyed the only fixture proving a *complete* bucket is never dropped.

## (i) Artifacts — exact repo paths

| artifact | path | bytes | sha256 |
|---|---|---:|---|
| Amendment | `prompts/CONTRACT_v4_Amendment_FAN8.md` | 826 | `2017fe6636987afd39fa49197424482d5ec69661b8f2df6dd0e9b565da75987f` |
| Parity worksheet | `_reviewer_box/parity_worksheet_2026-08-02.md` | 7,414 | `7025bf21c0816e1959e530af24284f8f95393e75da5717443b3905170c2b7fb5` |
| Parity worksheet (exchange) | `exchange/reports/parity_worksheet_2026-08-02.md` | 7,414 | `7025bf21c0816e1959e530af24284f8f95393e75da5717443b3905170c2b7fb5` |
| Phase I report | `_reviewer_box/ANALYTICS1_REPORT.json` | 11,549 | `258ec96f62c378c9378ad53826bc1a6ef7794732d6ae717f09b053afb0f6b3a2` |
| Phase I report (exchange) | `exchange/reports/ANALYTICS1_REPORT_2026-08-02.json` | 11,549 | `258ec96f62c378c9378ad53826bc1a6ef7794732d6ae717f09b053afb0f6b3a2` |
| 8c diff | `_reviewer_box/f_an_8_diff.json` | 10,870 | `4bdc51fa2e9378b1a67dfcf27e58c215410ca60356cd4edfba809eec2892f655` |
| 8c diff (exchange) | `exchange/reports/f_an_8_diff_2026-08-02.json` | 10,870 | `4bdc51fa2e9378b1a67dfcf27e58c215410ca60356cd4edfba809eec2892f655` |
| 8c diff (legacy name) | `_reviewer_box/_f_an_8_diff.json` | 10,870 | `4bdc51fa2e9378b1a67dfcf27e58c215410ca60356cd4edfba809eec2892f655` |
| Integrity manifest | `exchange/status/MANIFEST.json` | 19,853 | `205e7abba2f9f87027a85e3684190bcc3a48f5414c6e30e22631d49cb6af41ee` |
| This report | `exchange/reports/BUILDERS_REPORT_ARGUS_2026-08-02_ANALYTICS1_PHASE_I.md` | — | self-referential — hash it after writing; a file cannot contain its own digest |

**Note on the manifest location.** The Phase I paste expected
`_reviewer_box/MANIFEST.json`. `scripts/reviewer_manifest.py` writes to
**`exchange/status/MANIFEST.json`** — its `BOX_DIR` was migrated on 2026-08-02 under gate
A-3a, before this cycle. F-M1..F-M4 all PASS at the new location. Reported rather than
"corrected", because the migration is the newer decision.

---

## What the operator has to do

**Read the parity worksheet against a chart.** That is the gate. Until those readings come
back, `analytics/` is built, fixtured and committed — and adopted by nothing.

The worksheet carries 24 current-bar rows plus 4 historical (~30 days back), on
`BINANCE:<SYM>USDT.P` perpetuals, in UTC, closed candles only. RVWAP rows target TradingView's
official **Rolling VWAP** with a fixed window of 7/30/90/365 days, source `hlc3`, bands ×1.
The anchored-band variance is flagged **"to be confirmed by reading"** — it is a reasoned
inference from shared band machinery, not read from source, and it must never be cited as
pinned. There is a blank column for a private RVWAP script beside ours.

A row that disagrees is a finding. Bring it back as it is.
