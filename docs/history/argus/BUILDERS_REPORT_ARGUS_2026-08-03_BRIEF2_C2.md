# BUILDER'S REPORT — ARGUS lane — BRIEF-2, CYCLE 2

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Contract:** CONTRACT v4 Amendment 2
**Branch:** `v12-v1-census` · **Reissued** to cover stages 0 through this cycle.

> The cycle-1 report covered stages 0–4 only and contradicted the Session Summary
> on whether a capture existed. It did not. **A capture exists now** and this
> report supersedes it. The two artifacts are paired from here on so they cannot
> drift again.

---

## 0 · STATUS

**Stages 0–6 of the original contract are built; this cycle's stages A–F are
complete.** The render (`brief_render.py`, `brief_note.py`, chart-plane HTML,
F-B10, F-B20) is the remaining work and is deferred to cycle 3 under the stage-G
scope valve.

Suite **229 passed / 1 skipped**, from a 114/1 baseline two cycles ago.
`analytics` **1.3.0** · `rules_version` **2.0.0** · `schema_version` **2.1.0**.

**PARITY NOT CERTIFIED. Nothing here is adopted.**

---

## 1 · ENVIRONMENT GATE

| check | result |
|---|---|
| branch == `v12-v1-census` | PASS |
| pwd contains `\Users\` AND OneDrive | PASS |
| `engine/ prompts/ analytics/` exist | PASS |
| HEAD at cycle start (reported, never gated) | `1018d8b` |

---

## 2 · STAGE A — AUDITS

### A.1 Mutation audit of the original 21 F-AN-13 cases

Uniform "borrow the next bar's value" mutant, one per case.

| result | count |
|---|---|
| CAUGHT | 19 |
| VACUOUS | 2 — `stoch_rsi_k`, `stoch_rsi_d` (one root cause) |

Under the gate (>3 ⇒ halt) this is **no halt**.

**The first harness run was WRONG and reported 3.** It reused stale
`__pycache__` between iterations, so some runs executed the previous mutant; the
`ema` "vacuity" was entirely an artifact. This is the **second** harness bug this
project has produced, so no verdict was reported until the harness was re-run
with bytecode caching disabled and every verdict re-derived.

Full table (post-fix): all 21 CAUGHT.

### A.1 FINDING F-2R-A — a shipped indicator that never produced a number

`stoch_rsi` returned **all-NaN on every input**. `sma` is cumsum-based, so one
leading NaN poisons everything after it, and the raw stochastic always has a NaN
prefix.

**Measured: 100% of `stoch_rsi` values in the 2026-08-03 capture were null**,
across all ten assets and all five timeframes. StochRSI is one of §6.1's four
commissioned oscillators and had never worked.

**Why F-AN-13 could not catch it:** the truncation assertion compares
`got[k-1] == ref[k-1]` with a NaN-equals-NaN branch. An all-NaN series satisfies
it at every k. *A guard that cannot fail is not a guard.*

**F-AN-6b** now asserts every series function is FINITE after warm-up — the
property F-AN-13 silently assumed — and it catches the original bug where
F-AN-13 remains structurally blind.

Fixed in `stoch_rsi` via `_sma_after_warmup`, **not** in `sma`: making `sma`
NaN-tolerant would move every other consumer including `awesome_oscillator`,
whose input has no NaNs and whose published numbers must not move. Interior NaNs
are not papered over. %D warm-up is 31, exactly `rsi+stoch+k+d-3` as CONVENTIONS
already recorded. `ANALYTICS_VERSION` 1.2.0 → **1.3.0** per I-F.

### A.2 / A.3 Lockbox disclosure — verified from the STORED artifacts

| location | value |
|---|---|
| `assets.*.volume_windows.windows.365d.lockbox_overlap` | `overlap_days 64.167`, `intersects true`, with `basis` |
| `assets.*.rvwap.windows.365d.lockbox_overlap` | `64.167` — **A.3 required no fix; already present** |
| `assets.*.partition_footprint.lockbox_overlap` | present |
| `doc.lockbox` | window + policy |
| panel `areas` partition | column `lockbox_overlap_days`: 365d **64.167**, all other windows **0.0** |

`levels` and `snapshots` carry no lockbox column — correct, they hold no windowed
record.

### A.4 LIT known-wrong marking — WITHDRAWN on evidence

| check | result |
|---|---|
| `LIT_FLOOR_MS` | 2025-12-23T00:00Z; data starts 2025-12-23T17:30Z — **after** |
| rows | 319,925 of 319,925 expected — **100.00%** minute coverage |
| gaps > 1 bar / duplicates / non-monotonic | **0 / 0 / 0** |
| zero-volume flat bars | 14 (0.004%) |

The 14 bars are **not padding**: scattered from 14.7% through the series, all 14
with `O=H=L=C` equal to the *previous close*, and 13 distinct prices between
them — the exchange reporting a no-trade minute. My first pass called this a
"padding signature"; that was too crude and is corrected here.

LIT therefore has **222 days of correct data**. A percentile over 222 days is a
correct percentile over a short sample, and marking correct data as known-wrong
trains the reader to ignore markers. `lit_known_wrong` is kept as a **named
no-op** so a reader of an archived capture can discover what happened to it. The
shortness is still disclosed — by the `warming` chip and by `percentile_rank`'s
sample size.

---

## 3 · STAGE B — D-1, capture size

| measurement | value |
|---|---|
| rules block | **1,077 B = 0.19%** of the capture |
| §B.2 threshold | >5% ⇒ externalise |
| **verdict** | **NOT material — left inline.** A capture stays fully self-describing at negligible cost; no `briefs/rules/` indirection introduced. |

| B.3 size delta (same content) | bytes | annual @ 3 slots |
|---|---|---|
| before | 794,451 | 870 MB/yr |
| after | 650,623 | 712 MB/yr |
| **saved** | **143,828 (18.10%)** | **157 MB/yr** |

`schema_version` 2.0.0 → **2.1.0**.

---

## 4 · STAGE C — R-1, the invalidation floor

Reviewer finding: R:R is inversely proportional to stop distance, so a board
sorted by R:R floats the **least survivable** stops to the top. The 2026-08-03
top row scored **11.23** on a stop of **0.096 ATR**.

- `inval_atr` printed on every row.
- `MIN_INVAL_ATR = 0.25` (v1 placeholder). Rows below it **still print**, in
  `excluded_too_tight`, flagged *"invalidation too tight to rank"*. Suppressing
  them would hide geometry the operator asked to see; **ranking** them is what
  made them look like the best ideas.
- **F-B34** asserts the floor, the flag, that `inval_atr` recomputes as
  `risk/ATR`, and — anti-vacuity — that a survivable invalidation **still ranks**,
  so the floor cannot pass by excluding everything.

---

## 5 · STAGE D — wiring

### D.1 `daily_brief.py` routed through `analytics` (finding F-1R-B)

The private pandas resample at `:216` is gone. **Disclosed value shift**, measured
before changing anything:

| measure | 4h | 12h | 1d |
|---|---|---|---|
| RSI(14) delta | −0.61 … +0.89 | **−6.40 … +1.19** | −5.98 … −1.25 |

ATR(14) 1d, BTCUSDT: **1,638.22 → 1,699.80**. BTCUSDT 1d last row moves from
2026-08-02 (forming) to 2026-08-01 (closed). This is the F-AN-8c diff class and
it is the correction: mid-period a resampled oscillator was reading a fraction of
a period as the whole one.

### D.4 Registry by family — all five populated

| asset | total | anchored | rolling | profile | structure | ss |
|---|---|---|---|---|---|---|
| NEARUSDT | 117 | 21 | 28 | 39 | 13 | 16 |
| BTCUSDT | 116 | 21 | 28 | 30 | 13 | 24 |
| JTOUSDT | 116 | 21 | 28 | 36 | 13 | 18 |
| SOLUSDT | 111 | 21 | 28 | 33 | 13 | 16 |
| TAOUSDT | 110 | 21 | 28 | 30 | 13 | 18 |
| FARTCOINUSDT | 108 | 21 | 28 | 30 | 13 | 16 |
| ZECUSDT | 105 | 21 | 28 | 33 | 13 | 10 |
| HYPEUSDT | 105 | 21 | 28 | 27 | 13 | 16 |
| ETHUSDT | 104 | 21 | 28 | 30 | 13 | 12 |
| LITUSDT | 93 | 21 | 21 | 22 | 13 | 16 |

Was 43–67 with three empty families. **Below §5.3's ~180–200**, which assumed
prior M/Q/Y anchors `daily_brief` does not compute. Reported, not padded.

`daily_brief`'s own `vwap.rolling` block is deliberately **not** read: brief2's
`rvwap_layer` is the pinned §3.2 recipe. Reading both would double-count one tool
as two agreeing voices.

### §7.2 conformance fix, found while measuring R-1

The spec says invalidation is **beyond** the cluster's far edge; it was
implemented **as** the far edge. Because clusters are bounded by `CLUSTER_ATR`
from their running mean, a far-edge stop can never exceed ~0.15 ATR and **could
never clear the 0.25 floor** — every row on every asset was excluded. *A floor no
geometry can satisfy is an off switch, not a filter.*

Invalidation now sits one cluster tolerance beyond the far edge, **reusing a
ratified threshold rather than inventing one**. Effect on real data: R:R falls
from 11.23 to **1.35–2.35**; `inval_atr` lands at 0.244–0.276; the floor excludes
2 of 12. The 11.23 was a *symptom* of the un-survivable stop.

---

## 6 · STAGE E — capture, calibration, parity tool

**Capture:** `briefs/brief_2026-08-03_post_ny.json`, ten assets, **199.2 s**
(inside the ~15 min budget), sha256 `3c65e44b…c7ad`, 1,425,913 B.
Partitions: **10 snapshots / 1,413 levels / 80 areas**.

Regenerated with `--force`: the prior capture was schema 2.0.0, carried 100% null
`stoch_rsi`, and had three empty families. It was never adopted.

### ITEM 6 — the headline

**A line in the sand moved on 10 of 10 assets, 20 of 20 sides.**
Median move **0.127 daily-ATR** (min 0.005, p90 0.681, max 0.946).

### Other items

| item | result |
|---|---|
| 1 registry | 93–117, median 109 (vs ~180–200 expected) |
| 2 scores | printed; family-cap bind rate reported |
| 3 stability | per-asset spread across 0.10 / 0.15 / 0.20 |
| 4 top-3 composition | largest-family tally printed |
| 5 nesting states | distribution over 10 assets × 3 pairs |
| 7 storage | **1,584 MB/yr** (captures 1,561 + partitions 23) vs a 150–250 MB estimate |
| extra | `inval_atr` distribution for re-ratifying the R-1 floor |

The report states in its own header that it **re-ratifies nothing** (ruling D-2).

**Parity tool** `scripts/parity_check.py` handles the two things that make a
parity check meaningless — comparing different **bars** (takes the candle open
time, computes on closed buckets only, names the bar it evaluated; a forming-bar
request returns `exact_candle_match: NO` with the reason) and comparing different
**recipes** (every measure prints its pinned recipe). It applies **no tolerance**
and emits no pass/fail: what counts as a match is the operator's call.

---

## 7 · FILE DISPOSITION

| file | disposition | why | tracked | pushed | fixture |
|---|---|---|---|---|---|
| `analytics/momentum.py` | MODIFIED | F-2R-A stoch_rsi fix | yes | yes | F-AN-6b, F-AN-13 |
| `analytics/__init__.py` | MODIFIED | v1.3.0, CONVENTIONS | yes | yes | F-AN-5 |
| `analytics/levels.py` | MODIFIED | D-1 dedupe | yes | yes | F-B27 |
| `analytics/nesting.py` | unchanged | — | yes | yes | F-B25 |
| `analytics/profile.py` | unchanged | — | yes | yes | F-B25/30 |
| `analytics/structure.py` | unchanged | — | yes | yes | F-AN-13b/14d |
| `analytics/INTERFACE.md` | STALE | predates 1.3.0 + D-1 | yes | yes | — |
| `scripts/daily_brief.py` | MODIFIED | D-3 resample routing | yes | yes | F-B1..8 |
| `scripts/brief2.py` | MODIFIED | R-1 floor, §7.2, registry | yes | yes | F-B29/34 |
| `scripts/brief_capture.py` | MODIFIED | Part I wiring, LIT | yes | yes | F-B9/15/24 |
| `scripts/brief_panel.py` | unchanged | — | yes | yes | F-B19/32 |
| `scripts/brief_calibration.py` | NEW | §9.2 report | yes | yes | — |
| `scripts/parity_check.py` | NEW | D-6 parity tool | yes | yes | — |
| `scripts/forward_log.py` | unchanged | — | yes | yes | F-F1..5 |
| `scripts/publish_exchange.py` | **UNTOUCHED** | DO-NOT-MODIFY; routed to ATHENA | yes | yes | — |
| `briefs/brief_2026-08-03_post_ny.json` | REGENERATED | schema 2.1.0 + Part I | yes | yes | F-B9/17/23 |
| `briefs/panel/*/2026-08-03.parquet` | REBUILT `--force` | capture changed | yes | yes | F-B19/32 |
| `ops/forward_log.jsonl` | unchanged | 1 entry | yes | yes | F-F1/5 |
| `exchange/reports/BRIEF2_CALIBRATION_*` | NEW | §9.2 | yes | yes | — |
| `tests/test_*.py` (6 files) | MODIFIED/NEW | see §8 | yes | yes | — |

---

## 8 · FIXTURE TRANSCRIPT

```
tests/test_analytics.py            57 passed    + F-AN-6b
tests/test_brief2_volume.py        21 passed
tests/test_brief2_confluence.py    16 passed    + F-B27 dedupe assertion
tests/test_brief2_report.py        22 passed    + F-B34 (5 tests)
tests/test_brief2_storage.py       22 passed    + F-B15 split, LIT withdrawal
tests/test_forward0.py             18 passed
-----------------------------------------------------------------
FULL REPO SUITE                   229 passed, 1 skipped   (46.4 s)
```

**F-B15 was split this cycle.** Wiring Part I brought `doctrine_chip` —
v1.1's ratified quotation of the operator's playbook, *'playbook 5.5: "half size,
Z1/Z2 only, grade ≤ B"'* — into the capture. The contract's literal F-B15 is
**zero KEYS**, and the key scan passes cleanly with **no exceptions**. My stricter
value scan now carries **two enumerated, justified exceptions** (the doctrine
quotation; the statistical phrase "sample size"), plus an anti-vacuity test that
the exception list still matches something, has not grown, and would still catch
a genuine sizing prescription. The regex was **not** widened to make the failure
disappear.

---

## 9 · FINDINGS REPORTED, NOT FIXED

| id | file:line | status |
|---|---|---|
| **F-2R-A** | `analytics/momentum.py` `stoch_rsi` | **FIXED** — §2 |
| **F-1R-A** | `analytics/structure.py:36-45` | FIXED cycle 1 |
| **F-1R-B** | `scripts/daily_brief.py:216` | **FIXED** — §5 |
| **F-1R-C** | `analytics/vwap.py:96-97, 128-129` | **REPORTED, NOT FIXED.** Ruling D-4: leave pinned until parity certifies. Touching pinned VWAP arithmetic while its parity is unverified would make a failure ambiguous between recipe and refactor. |
| **INTERFACE.md stale** | `analytics/INTERFACE.md` | **REPORTED.** Predates analytics 1.3.0, the D-1 dedupe and the §7.2 change. Regenerate next cycle. |
| **push scope** | `scripts/publish_exchange.py` | **ROUTED TO ATHENA** — see `NOTE_ARGUS_to_ATHENA_2026-08-03_publish_exchange_push_scope.md`. Operator has ACCEPTED the pushed state. |

---

## 10 · PROVENANCE

| | |
|---|---|
| `ANALYTICS_VERSION` | **1.3.0** |
| `analytics_sha()` | `da81034d86329a0e0e581e526ebe515f3d0f491a0c7ae329e3a9ce49c9c6c731` |
| `rules_version` / `schema_version` | **2.0.0** / **2.1.0** |
| capture sha256 | `3c65e44b885e75e60a7be31d07ac9205c6c27e70574c8fc6ce63c3326c9bc7ad` |
| amendment sha256 | `c502ecf471f8fab08d8a4077edfbb1860496c2fa80b1c9f02376816db532da9c` |

### Commits, this cycle

| commit | stage |
|---|---|
| `6313807` | A — mutation audit, F-2R-A, LIT withdrawal |
| `cc0003d` | B — D-1 dedupe, rules block measured |
| `9db5fc9` | C — R-1 invalidation floor |
| `d622b20` | D — Part I wired, daily_brief routed |
| `0ab827d` | E — capture, calibration, parity tool |

Cycle 1: `e355845 · 074ae2b · ffe775b · 70bd499 · b69572e · 53d7a8a · 9791b05 · e707d1e`.

---

## 11 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No Tier-C created or
implied. No engine change. No forward scoring. No lockbox read for scored
evidence. No fitted weights. No estate mutation.

Confluence scores measure **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Whether any of it predicts anything is census work
under G-7 — **CENSUS-1d, H-RVX, H-M1X, H-VAN** route to APOLLO.

**Adoption remains gated on the operator's parity readings.** Every render prints
`PARITY NOT CERTIFIED` until the flag is set; F-B33 asserts it in both directions.

— HEPHAESTUS, 2026-08-03
