# BUILD — MC-1 v2 · THE MAY-26 PROGRAM

**Contract:** `exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md` (written this run, STEP 1).
**Drafted:** APOLLO. **Executor:** HEPHAESTUS. **Ratified:** operator 2026-08-06
("MC defaults + 25ema in 1m") + amendment 2026-08-06 ("continuous queryability
before/after the cross"). **Seed** 20260806. **Run date** 2026-08-10.
**Repo:** branch `v12-v1-census`, HEAD `7a3a881`. Windows, Python 3.12.10,
numpy/pandas via the repo venv.

This document is zero-context: everything needed to audit the run is here or is
pointed at by path + sha256.

---

## 0 · HARD ASSERTIONS (all passed before any read or write)

```
git rev-parse --short HEAD   -> 7a3a881
pwd                          -> /c/Users/luisf/OneDrive/Desktop/Midas-Claude Code Resources/naiad
engine/                      OK      scripts/census_build.py      OK
exchange/queue               OK      exchange/reports             OK
exchange/status              OK      scripts/publish_exchange.py  OK
research_outputs/seq8        OK      python -c "from engine import data"  OK
```

**EXPLORATION CEILING — read from the census machinery's own constant, the same
source SEQ8's F-SEQ2 reads:**

```
scripts/census_build.py:59-60
  # exploration-classic ceiling: open_time < 2024-07-01T00:00:00Z (DATA_CENSUS.md).
  CEIL_MS = int(datetime(2024, 7, 1, tzinfo=timezone.utc).timestamp() * 1000)

CEIL_MS = 1719792000000   =   2024-07-01T00:00:00Z
RULE    = open_time < CEIL_MS
```

Every SCORED table below is bounded by this value (F-MC2). The D-3 dossier is
OPS-CLASS and sits deliberately outside it (I1).

---

## 1 · STEP 0 — SYNTHESIS FILING

**`SS_SYSTEM_SYNTHESIS_2026-08-06.md` was NOT attached to this paste.** Per the
contract's own instruction ("If not attached: note MISSING, continue"), the
status is **MISSING**, and the run continued.

A resident copy already exists in the repo and is git-tracked. It was hashed and
left **byte-identical — not overwritten**:

| field | value |
|---|---|
| path | `exchange/reports/SS_SYSTEM_SYNTHESIS_2026-08-06.md` |
| bytes | 31,822 |
| CR bytes | 0 (pure LF) |
| sha256 | `f184f105c0612128c9ed5819d72fe6ff0c2d123378b0923d08b90bc856c4c7f2` |

The contract's authority citation (§3.4, MC-1..7) resolves against this resident
copy, which was read in full for this run.

---

## 2 · STEP 1 — THE QUEUE ITEM

`exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md` was written containing
the contract verbatim. **No prior v1 of this queue item existed** (`ls
exchange/queue | grep -i mc1` → empty), so the "SUPERSEDES any unrun v1" clause
is moot and nothing was replaced.

---

## 3 · FIXTURE TRANSCRIPT — 11 of 11 PASS

Full, unedited, as emitted by `python scripts/mc1_program.py fixtures`.

```
--- F-MC1 : PASS ---
    SEQ8 D6 rows 98; applicable (overlap) 56; diffs 0
    D6 declines 42 cells (5m/15m/30m x 300/450, status NOT-APPLICABLE); D-1 computes them — declination, not divergence
    hand-recomputation, formula warm=ceil(ln(1e-3)/ln(1-2/(L+1))):
    BTCUSDT/4h/EMA450: warm=1555 n=10544 idx=134 j=1555 hand=2020-05-24T20:00:00Z program=2020-05-24T20:00:00Z MATCH
    ZECUSDT/1d/EMA200: warm=691 n=1608 idx=25 j=691 hand=2021-12-27T00:00:00Z program=2021-12-27T00:00:00Z MATCH
    TAOUSDT/12h/EMA300: warm=1037 n=161 idx=39 j=1037 hand=NEVER program=NEVER MATCH
--- F-MC2 : PASS ---
    exploration ceiling = 1719792000000 (2024-07-01T00:00:00+00:00) [census_build.CEIL_MS]
      D-1 first_warm: 1718442000000 (2024-06-15T09:00:00Z)  <= ceiling: True
      D-4 event ts: 1719734400000 (2024-06-30T08:00:00Z)  <= ceiling: True
      D-5 cascade term_ts: 1719788400000 (2024-06-30T23:00:00Z)  <= ceiling: True
      D-6 birth ts: 1719769980000 (2024-06-30T17:53:00Z)  <= ceiling: True
    estate byte-identical before/after: True (70 files, 656085646 B)
    D-3 dossier is OPS-CLASS and is DELIBERATELY outside the wall (I1): its timestamps are 2026 and it never touches the estate.
    DISPLAY-ONLY headers: d3a_manifest: OK | d3b_registry: OK | d3c_colocation: OK | d3e_event_card: OK
--- F-MC3 : PASS ---
    D-4 stamps content-sha  run1 72588105df6f88db  run2 72588105df6f88db  IDENTICAL
    D-5 tier table content-sha run1 b99db859d5268f8e  run2 b99db859d5268f8e  IDENTICAL
    seed 20260806
--- F-MC9 : PASS ---
    full re-run of D-5 hash-identical: True (b99db859d5268f8e4cc09e19adb1cfbe)
--- F-MC4 : PASS ---
    stamp windows, by construction, all terminate at or before the event bar:
      SEAL  : agrees on the event bar's own e89/e200, OR a 89_200 cross in [ts-6*4h, ts] (PRIOR window)
      WALL  : event_price vs e89(4h) on the event bar, and e200(1d) as-of the last 1d bar CLOSING at/before the event bar close
      TRAP  : counter-direction FAST crosses in [ts-24h, ts)
      FIRST : same-direction 4h lattice-A crosses in [ts-20*4h, ts)
    audited 200 sampled stamps; violations 0
    violations listed and demoted, never silently kept — none found
--- F-MC5 : PASS ---
    join rule (verbatim, SEQ8 seq8_fixtures.json:41):
      birth joins a cascade iff (a) cell symbol == cascade asset, (b) the cell's governor TF is a rung of the cascade (MANDATES: intraday->1h, swing->4h, position->12h), and (c) birth ts_open lies within [first rung bar_close, terminus bar_close]. Restricted to lattice A / 9_89 (the cross the engine trades).
    join key (verbatim): (cell_id, tranche_id) — tranche_id alone collides across cells
    join_rows 301018  births_total 7117  distinct_births_joined 6831
    orphans_join_to_journal = 0  births_never_joined = 286
    SEQ8's own stance, reproduced not overridden: 'Zero orphans both ways' is asserted in the direction that is falsifiable — every joined key must exist in the journals. The reverse is NOT an orphan condition: a birth falling in no cascade span is a real, correct outcome and is reported as births_never_joined rather than forced to zero.
--- F-MC6 : PASS ---
    P-i, P-iii and P-iv are printed VERBATIM in section D-6 of the build document strictly BEFORE any result table for them; the registration text is carried in MC1_results.json under P_i/P_iii/P_iv .registration.
--- F-MC7 : PASS ---
    tier-0 row: tier-0 (UNGATED)  gate=none  TRG=100.0%
    identity holds exactly: True
--- F-MC8 : PASS ---
    1W bucket 2022-01-31T00:00:00Z (7 1d members, weekday=Monday): O/H/L/C/V match = True
    1M bucket 2022-02-01T00:00:00Z (28 1d members): O/H/L/C/V match = True
--- F-MC10 : PASS ---
    query_dossier(2026-05-20T08:00:00Z, '4h') -> bar 2026-05-20T04:00:00Z .. 2026-05-20T08:00:00Z, close=77249.9, 8 nearest levels
        profile_windowed:poc_30d @ 77360.86 score=5 dist=110.96
        structure:period_open_D @ 76963.20 score=6 dist=286.70
        structure:prior_week_low @ 77601.80 score=5 dist=351.90
    query_dossier(2026-04-03T16:00:00Z, '4h') -> bar 2026-04-03T12:00:00Z .. 2026-04-03T16:00:00Z, close=66806.1, 8 nearest levels
        profile_windowed:val_30d @ 66626.47 score=4 dist=179.63
        structure:period_open_W @ 66334.80 score=4 dist=471.30
        vwap_anchored:avwap_week @ 67438.21 score=12 dist=632.11
        EMA9: dossier=76927.38755580566 direct-from-raw=76927.38755580566 EXACT
        EMA12: dossier=77004.27403149537 direct-from-raw=77004.27403149537 EXACT
        EMA25: dossier=77533.96011032692 direct-from-raw=77533.96011032692 EXACT
        EMA89: dossier=78702.59483478719 direct-from-raw=78702.59483478719 EXACT
        EMA200: dossier=77693.82493971751 direct-from-raw=77693.82493971751 EXACT
        EMA300: dossier=76699.52774075803 direct-from-raw=76699.52774075803 EXACT
        EMA450: dossier=76265.62476486099 direct-from-raw=76265.62476486099 EXACT
    Chart parity vs TradingView is NOT asserted. The operator may spot-check and relay; nothing here claims vendor agreement.
--- F-MC11 : PASS ---
    correctly sliced: 35 levels, price=77281.5, max bar close consumed 2026-05-26T00:00:00Z <= as-of 2026-05-26T00:00:00Z
    SABOTAGE (one future bar fed): guard REJECTED -> I7 VIOLATION in registry daily substrate: consumed a bar closing at 2026-05-27T00:00:00Z > as-of 2026-05-26T00:00:00Z
FIXTURES: 11/11 PASS
```

---

## 4 · D-1 · WARMUP / FEASIBILITY MATRIX (EVIDENCE, exploration-classic)

490 cells = 7 assets × 10 TFs × 7 EMAs. Full matrix in `MC1_tables.md`.

**I3 warmup convention — SEQ8's exact rule, cited:**

```
scripts/seq8_extract.py:114-119
  def warmup_bars(length, residual=SEED_RESIDUAL):
      alpha = 2.0 / (length + 1.0)
      return int(math.ceil(math.log(residual) / math.log(1.0 - alpha)))
scripts/seq8_extract.py:84    SEED_RESIDUAL = 1e-3
scripts/seq8_extract.py:179   v[:min(WARM[L], n)] = np.nan     # never backfilled
```

The function is **imported from SEQ8, not restated**. Bars required:

| EMA | 9 | 12 | 25 | 89 | 200 | 300 | 450 |
|---|---|---|---|---|---|---|---|
| warmup bars | 31 | 42 | 87 | 308 | 691 | 1037 | 1555 |

`engine.indicators.ema` seeds at the first finite value and is never NaN after
bar 0, so the ONLY source of NaN is SEQ8's mask. First-warm is therefore a
closed-form function of the mask width and the bar axis, not of the prices —
which is exactly what F-MC1's three hand-recomputed cells check.

**BTCUSDT (illustrative; all 7 assets in `MC1_tables.md`):**

| TF | EMA9 | EMA12 | EMA25 | EMA89 | EMA200 | EMA300 | EMA450 | bars |
|---|---|---|---|---|---|---|---|---|
| 1m | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2530442 |
| 5m | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 506089 |
| 15m | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 168697 |
| 30m | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-11 | 84349 |
| 1h | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-07 | 2019-10-21 | 2019-11-12 | 42175 |
| 4h | 2019-10-01 | 2019-10-01 | 2019-10-01 | 2019-10-30 | 2020-01-01 | 2020-02-28 | 2020-05-24 | 10544 |
| 12h | 2019-10-01 | 2019-10-01 | 2019-10-22 | 2020-02-09 | 2020-08-19 | 2021-02-08 | 2021-10-25 | 3515 |
| 1d | 2019-10-09 | 2019-10-20 | 2019-12-04 | 2020-07-12 | 2021-07-30 | 2022-07-11 | 2023-12-11 | 1758 |
| **1W** | 2020-04-06 | 2020-06-22 | 2021-05-03 | **NEVER** | **NEVER** | **NEVER** | **NEVER** | 252 |
| **1M** | 2022-04-01 | 2023-03-01 | **NEVER** | **NEVER** | **NEVER** | **NEVER** | **NEVER** | 58 |

Overall: 395 WARMED, 95 NEVER.

**I2 · 1W/1M convention, printed on every 1W/1M table:**
> 1W/1M derived from 1d via the existing s1 resampler algorithm
> (`scripts/s1_resample.aggregate`, mirrored byte-for-byte by
> `census_build._resample`). Weeks open **Monday 00:00 UTC**; months
> **calendar-UTC**. **NOT chart-parity-certified** — parity against a charting
> vendor is NOT asserted.
>
> 1W is produced by the s1 fixed-step resampler verbatim, with the time axis
> shifted by 4 days so the fixed-step floor lands on Monday (epoch day 0 is a
> Thursday) and shifted back afterwards. **1M is the one place the s1 fixed-step
> resampler cannot reach** — a calendar month is not a fixed step. The
> AGGREGATION is s1's unchanged (first/max/min/last/sum); only the bucket KEY is
> calendar. No new resampler was written.

---

## 5 · D-3 · THE MAY-26 QUERYABLE OPS DOSSIER — **DISPLAY-ONLY**

> **DISPLAY-ONLY — lockbox-era data — hypothesis generation only, never evidence**
>
> Instrument: **BTCUSDT perpetual (USDT-M)**. Endpoint:
> `https://fapi.binance.com/fapi/v1/klines`.

### 5.1 Fetch (D-3 FETCH, dates [VETO])

314 requests, **peak observed `x-mbx-used-weight-1m` = 870 of the documented
2400/min cap** (paced to a 840 target). Every series is gap-free and
duplicate-free: bar counts equal `days × bars-per-day` exactly.

| TF | requested from | bars | first | last | MB |
|---|---|---|---|---|---|
| 1m | 2026-02-01 | 262,080 | 2026-02-01T00:00Z | 2026-08-01T23:59Z | 8.14 |
| 5m | 2025-06-01 | 122,976 | 2025-06-01T00:00Z | 2026-08-01T23:55Z | 4.83 |
| 15m | 2025-06-01 | 40,992 | 2025-06-01T00:00Z | 2026-08-01T23:45Z | 1.70 |
| 30m | 2025-06-01 | 20,496 | 2025-06-01T00:00Z | 2026-08-01T23:30Z | 0.86 |
| 1h | 2025-06-01 | 10,248 | 2025-06-01T00:00Z | 2026-08-01T23:00Z | 0.43 |
| 4h | 2024-06-01 | 4,752 | 2024-06-01T00:00Z | 2026-08-01T20:00Z | 0.20 |
| 12h | 2024-06-01 | 1,584 | 2024-06-01T00:00Z | 2026-08-01T12:00Z | 0.07 |
| 1d | 2019-01-01 | 2,520 | 2019-09-08T00:00Z | 2026-08-01T00:00Z | 0.11 |

*"through 2026-08-01" convention:* the whole of 2026-08-01 is covered, i.e.
`open_time < 2026-08-02T00:00:00Z`. 1d begins 2019-09-08 because that is the
first bar the venue has for this instrument.

### 5.2 (a) Per-bar series + (d) long-pair ribbon state

`research_outputs/mc1/ops_series/perbar_{tf}.parquet`, study window
2026-02-01 → 2026-08-01: ts, OHLCV, ATR(14), all seven EMAs (NaN before warm),
ribbon spreads 9/89 · 89/200 · 300/450 in ATR units, cross flags for
9_89 · 89_200 · 9_200 · 12_25 · 300_450, and kiss-v0 flags.

Rows: 1m 262,080 · 5m 52,416 · 15m 17,472 · 30m 8,736 · 1h 4,368 · 4h 1,092 ·
12h 364 · 1d 182.

**I6 kiss-v0 [VETO ×3], with its limitation printed:** `|eA-eB| <= 0.25*ATR`,
then re-expansion `>= 0.75*ATR` within 10 bars, no sign change. It is
**derived and event-sampled**, and it is **not knowable on the touch bar** — a
touch is only confirmed by a re-expansion up to 10 bars later. Every kiss column
therefore ships with a companion `kiss_*_known_ts` carrying the confirmation
instant, so a query as-of T can filter to what was knowable at T (I7).

(d) `ops_series/ribbon_long_{5m,1m}.parquet` — spreads and a
compressed/transitional/expanded/unwarmed state for the long pairs 200/300,
300/450, 200/450. *Interpretation stated:* "long pairs" is read as the pairs
among the long EMA set {200,300,450}; all three are emitted.

**Two feasibility facts that follow from the [VETO] fetch dates:**
1. **1m has no pre-roll.** The 1m fetch starts on the study window's first day,
   so 1m EMAs warm *inside* the window: e9 at 2026-02-01T00:31Z … e450 not until
   **2026-02-02T01:55Z**. The first ~26 h of 1m long-EMA data is NaN. Correct
   under I3, and it does not touch the May-26 event.
2. **12h EMA450 does not warm until 2026-07-18T12:00Z** — *after* the May-26
   cross. The 12h 300/450 ribbon is therefore **unavailable at the event
   instant**, and the event card says so rather than showing a warm-looking
   number.

### 5.3 (b) Analytics registry series — dual-scored

`research_outputs/mc1/ops_series/registry/registry_series.parquet` —
**20,056 rows over 407 as-of instants** (every 00:00 UTC across the study
window, plus every 4H close 2026-05-01 → 2026-06-15), each row
`(as_of, variant, family, label, level, cluster_id, cluster_mean, score)`.

Citation: `ANALYTICS_VERSION` **1.5.0**, `analytics_sha()`
`ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91`.

**A structural fact worth stating plainly:** the package has **no
`(family, level, score)` record**. `score` lives on a *cluster*, not a level
(`analytics/levels.py:175-177`); a level is
`{family, label, level, source_layer, timeframe}`. The series is built by
iterating `clusters[].members` and attaching the cluster's score to each member —
`clusters[].members` is the single source of truth, and note that a member's
`level` post-collapse is the group mean.

Dual scoring is `analytics.levels.dual_score(...)`, emitting both the
`with_volume` and `without_volume` variants. Volume families are
`("vwap_rolling", "profile_windowed")` (`analytics/levels.py:39`).

**`volume_profile` approximation chip, carried on every profile artifact:**
> `volume spread uniformly across each bar's range (not tick data)`

**Family `ss` is absent by construction, not omission** — it is a capture-layer
product (brief2 radar rows), not an analytics-package product.

### 5.4 (c) Co-location counts

EMA cross events within **0.15 × daily ATR [VETO]** of a registry level, by
family, across the window: **40,713 co-locations over 30 (tf, family) cells**.
Detail: `ops_series/colocation_detail.parquet`. At the slower TFs:

| TF | profile_windowed | structure | vwap_anchored | vwap_rolling |
|---|---|---|---|---|
| 4h | 52 | 45 | 27 | 29 |
| 1d | 5 | 2 | — | — |

### 5.5 (e) THE MAY-26 EVENT CARD

**The 2026-05-26 4H bear cross is `cross_12_25_dn` at 2026-05-26T16:00:00Z,
close 76,028.3.** It is a **lattice-B (Trader XO 12/25) cross, not a lattice-A
trio cross** — an identification the contract's phrasing does not make, and one
that matters for reading the D-4 population.

It sits inside a lattice-A bear sequence on 4H: `9_89 dn` 2026-05-16T00:00Z →
`9_200 dn` 2026-05-18T04:00Z → `89_200 dn` 2026-05-27T20:00Z (the trio's seal
completing the day *after* the 12/25 cross).

**The four D-4 stamps applied to it (display-only):**

| stamp | value | why |
|---|---|---|
| SEAL | **false** | 4H 89/200 was not yet bearish, and no 89/200 cross in the prior 6 4H bars — it crossed 28 h *later* |
| WALL | **false** | neither limb: not within 0.5·ATR(4h) of e89(4h), nor within 0.5·ATR(1d) of e200(1d) |
| TRAP | **true** | 19 counter-direction FAST-tier up-crosses in the prior 24 h |
| FIRST | **true** | no same-direction 4H trio cross in the prior 20 4H bars |
| **similarity_score** | **2 / 4** | **not strict core** |

**This is a substantive finding: the archetype event does not itself satisfy the
similarity family built to describe it.** It is a FIRST-and-TRAP event without
seal or wall confirmation. Any reading of D-4's 4/4 strict core as "May-26-like"
should be re-examined against this.

**BEFORE-CHRONOLOGY** — every cross/kiss event on every TF in the prior 14 days
[VETO], timestamped, with the registry levels each occurred at: **2,356 events**
(1m 1,787 · 5m 348 · 15m 113 · 30m 60 · 1h 32 · 4h 9 · 12h 6 · 1d 1). The first
50 are inlined in `MC1_results.json`; the full table is in the event-card
checkpoint and reproducible from the per-bar series.

### 5.6 (f) QUERY HELPER

`query_dossier(ts, tf)` in `scripts/mc1_program.py` returns the full stack plus
the nearest registry levels for any instant. Both proof cards are printed in
F-MC10 above, and the 2026-05-20 EMA values match a direct recomputation from
the raw fetched klines **exactly, all seven EMAs**.

One-line pandas recipe:

```python
pd.read_parquet("research_outputs/mc1/ops_series/perbar_4h.parquet").query("open_time <= @ts").iloc[-1]
```

---

## 6 · D-4 · SIMILARITY FAMILY (EVIDENCE, exploration-classic)

**RULING PRINTED, because the contract's term has no referent in SEQ8.** The
word "trio" appears nowhere in any SEQ8 artifact, script or fixture. Its
definition of record is `SS_SYSTEM_SYNTHESIS_2026-08-06.md:14` — "the working
trio **9 / 89 / 200**". The D-4 population is therefore taken as **lattice A,
all three of its pairs** (`9_89`, `89_200`, `9_200`), tf = 4h, both directions,
7 assets, from the SEQ8 D1 stream `seq8_events.jsonl`: **1,569 events**.

Per-asset: BTC 332 · ETH 334 · JTO 34 · NEAR 254 · SOL 267 · TAO 12 · ZEC 336.
These reconcile exactly with `seq8_event_counts.json`.

**Degeneracy flagged, not hidden:** for the 164 `89_200` events the SEAL stamp
("4H 89/200 agrees or crosses within 6 bars") is *self-referential*. Those rows
carry `seal_degenerate = true` and the pyramid is printed both with and without
them. The alternative reading — 9_89 only, 881 events — is what SEQ8's own
bridge restricts to, and is consequently what D-6's scored join operates on.

**Stamps [VETO], all curtain-clean (windows terminate at or before the event bar):**

| stamp | fired | definition as implemented |
|---|---|---|
| SEAL | 708 | 4H 89/200 agrees with the direction on the event bar, OR a same-direction 89/200 4H cross within the **prior** 6 4H bars |
| WALL | 282 | `\|price − e89(4h)\| ≤ 0.5·ATR(4h)` **OR** `\|price − e200(1d)\| ≤ 0.5·ATR(1d)`; the firing limb is recorded per row |
| TRAP | 1,447 | ≥ 2 counter-direction FAST-tier (5m/15m/30m) lattice-A crosses in the prior 24 h |
| FIRST | 930 | no same-direction 4H lattice-A cross in the prior 20 4H bars |

WALL limbs: none 1,287 · 4h 238 · 1d 38 · both 6. WALL is the scarcest stamp —
only 282 of 1,569 events are in contact with either band.

**Strict core (4/4): 105 of 1,569.** Full population pyramid per score per asset,
with and without the degenerate subpopulation, is in `MC1_tables.md`.

---

## 7 · D-5 · OUTCOMES BY TIER (lift, curtain-cut)

Scoped embargo lift applies. Population: the 949,897 outcome-available cascade
rows of `seq8_outcomes.jsonl` (of 950,145; the 248 short rows are excluded — when
`outcome_available == false` SEQ8 writes the row *without* the outcome keys at
all, so filtering on that flag is mandatory).

Cascades ↔ outcomes were verified **positionally 1:1 with 0 alignment
mismatches** across all 950,145 rows during the scan.

Per-lens fixed-horizon MFE **and** MAE per tier per asset, with the held-in-time
split at the median event ts (**2022-07-01T23:15:00Z**), across lenses
{1h, 4h, 12h, 1d} × tiers {FAST, STAIR, SLOW, TREND} × 7 assets × horizons
{20, 100, 500}: **336 table rows**, all in `MC1_tables.md`.

MFE is signed positive and MAE signed negative, both already direction-flipped
for shorts, so "MFE net of matched MAE" is their **sum**.

**TRG (Tail-Retention Gauge) tail table — F-MC7 identity holds exactly:**

| tier | gate | n kept | tail n | TRG % |
|---|---|---|---|---|
| **tier-0 (UNGATED)** | none | 949,897 | 94,992 | **100.0** |
| FAST | `term_tier == FAST` | 421,444 | 37,470 | 40.0 |
| STAIR | `term_tier == STAIR` | 312,262 | 31,409 | 32.6 |
| SLOW | `term_tier == SLOW` | 184,452 | 21,015 | 21.0 |
| TREND | `term_tier == TREND` | 31,739 | 5,098 | 6.5 |

*TRG definition used:* share of the ungated tail mass retained by a gate; tail =
the top decile of `mfe_bps_h100`; tail mass = the sum of `mfe_bps_h100` over that
decile. tier-0 is the ungated population and retains 100.0% by identity. No
single tier gate retains even 40% of the tail — the same shape W-F1 found.

---

## 8 · D-6 · TRADE JOIN + PROMOTIONS

### 8.1 The join

`birth joins a cascade iff (a) cell symbol == cascade asset, (b) the cell's governor TF is a rung of the cascade (MANDATES: intraday->1h, swing->4h, position->12h), and (c) birth ts_open lies within [first rung bar_close, terminus bar_close]. Restricted to lattice A / 9_89 (the cross the engine trades).`

Join key: `(cell_id, tranche_id) — tranche_id alone collides across cells`.

Both strings are quoted verbatim from `seq8_fixtures.json:41` / `:39`. **This run
consumes SEQ8's own bridge table (`seq8_cascade_birth_join.jsonl`) rather than
re-deriving it**, so the rule applied is byte-identically SEQ8's. 301,018 join
rows; 7,117 births; 6,831 distinct births joined; **0 orphans join→journal**;
286 births never joined (SEQ8's own figure, reproduced).

Bridge→cascade attribute match: **301,018 / 301,018**.

### 8.2 Tier membership vs W-F1 deciles

**W-F1 materialises only the top and bottom deciles** — 709 each of 7,094
resolved tranches. There is no 1..10 decile label anywhere in the repo; W is
`realized_r >= 0.067318`, L is `realized_r <= -0.852774`, everything between is
unclassified. Cross-tab in `MC1_results.json` under `D6.tier_vs_wf1_decile`.

### 8.3 REGISTRATIONS — VERBATIM, BEFORE THEIR RESULT TABLES (F-MC6)

> **P-i [55%]** Leap-family cascades (4h-tier arrival from the FAST tier, pullback-anchored frame) carry higher curtain-cut per-lens MFE net of matched MAE than stair-arrival cascades, sign-consistent on >=3 of 5 panel assets.
>
> **P-iii [60%]** Grind-signature births (5m->15m->30m context, no slow-tier arrival within the episode) are over-represented in the W-F1 bottom decile vs top, CI excl. 0.
>
> **P-iv [45%]** Among 4h arrivals, leap-source outperforms stair-source AFTER conditioning on ATR-percentile at arrival (vol-matched buckets), >=3 of 5 assets.

Panel = BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT (`scripts/wf1_forensics.py:72`).
Primary view = `24h|window_chained`; all 8 views reported as sensitivity.

**Construction, stated before the numbers.** "Leap" and "stair" are resolved by
SEQ8's own `classify_arrival` at destination 4h: leap ⇔ source ∈ FAST
{5m,15m,30m}; stair ⇔ "adjacent" ⇔ source = 1h. Metric is
`median(mfe_bps_h100 + mae_bps_h100)`.

**Caveat carried, not silently dropped:** *"pullback-anchored frame"* has **no
representation in the SEQ8 cascade substrate** — no pullback/continuation flag
exists on a cascade (the census `NOPULLBACK_LOOKBACK` / `RIBBON_SEP_ATR`
machinery is census-1b, not SEQ8). The qualifier was **not applied as a filter**.

### 8.4 RESULTS — all rows printed, including failures

**P-i — per panel asset, primary view:**

| asset | n leap | n stair | net leap | net stair | delta | sign + |
|---|---|---|---|---|---|---|
| BTCUSDT | 2,105 | 2,555 | 20.79 | −5.72 | **+26.51** | yes |
| ETHUSDT | 2,132 | 2,324 | 23.74 | 9.73 | **+14.01** | yes |
| SOLUSDT | 1,674 | 1,805 | 19.40 | 63.22 | −43.82 | no |
| NEARUSDT | 1,746 | 1,765 | 32.38 | −7.95 | **+40.34** | yes |
| ZECUSDT | 2,023 | 2,160 | −9.89 | 3.07 | −12.97 | no |

**3 of 5 positive → threshold met → VERDICT: SUPPORTED (at the threshold).**

**P-iii:**

| n W | n L | prevalence W | prevalence L | delta (L−W) | 95% CI | excl. 0 |
|---|---|---|---|---|---|---|
| 214 | 476 | 0.1402 | 0.5231 | **+0.3829** | [0.3159, 0.4476] | **yes** |

**VERDICT: SUPPORTED.** Grind-signature births are 52.3% of the bottom decile
against 14.0% of the top — the clearest of the three results.

**P-iv — mean vol-bucket delta (5 equal-count ATR buckets per asset):**

| asset | buckets used | mean bucket delta | sign + |
|---|---|---|---|
| BTCUSDT | 5 | **+27.54** | yes |
| ETHUSDT | 5 | **+18.32** | yes |
| NEARUSDT | 5 | **+39.31** | yes |
| SOLUSDT | 5 | −65.45 | no |
| ZECUSDT | 5 | −10.13 | no |

**3 of 5 positive → threshold met → VERDICT: SUPPORTED (at the threshold).**

### 8.5 THE VIEW-DEPENDENCY — read this before using P-i or P-iv

The registrations name no cascade view. SEQ8 has eight. Scored across all of
them, the assets-positive count is:

| view | P-i | P-iv |
|---|---|---|
| 24h\|window_chained *(primary)* | **3** | **3** |
| 48h\|window_chained | **3** | **4** |
| 72h\|window_chained | **4** | **4** |
| 1W\|window_chained | 2 | **4** |
| 24h\|direction_consistent | 2 | 2 |
| 48h\|direction_consistent | 2 | 2 |
| 72h\|direction_consistent | 2 | 2 |
| 1W\|direction_consistent | 2 | 2 |

**Both verdicts flip on the view axis.** On every `direction_consistent` view
both fail (2/5); on `window_chained` views they pass. P-i and P-iv are supported
at exactly the ">=3 of 5" threshold on the primary view — one asset either way
changes the verdict. **These two results should be treated as
view-contingent and threshold-marginal, not as established.** P-iii is not
affected: it is well clear of its threshold on the primary view.

---

## 9 · D-7 · WINNER STACKS + RATCHET SUBSTRATE

### (a) Winner stacks

Bridge-joined **W-class (top-decile) births whose joined cascade has
`cascade_family == "leap"`**, primary view: **36 births** (34 distinct cascades;
`event_ts` recovered for 34/34 by a targeted stream over `seq8_cascades.jsonl`).

Each row carries the full multi-TF stack at birth (SEQ8's own 7-bit orientation
string per TF, bit order imported from `seq8_extract.py:125-126`:
`e9>e89 · e89>e200 · e9>e200 · e12>e25 · close>e89 · close>e200 · e300>e450`),
inter-cross spacings in minutes, and realized_r. Example row: BTCUSDT birth
2021-07-01T06:12:00Z, cascade `5m>30m>1h`, spacings [80.0, 150.0] min, 4h stack
`1001000`.

1m ladders ±3 days (estate 1m, exploration era, EMAs {25,89,200,300,450}):
**311,076 rows**, `research_outputs/mc1/d7a_1m_ladders.parquet` (19.9 MB).

### (b) Ratchet substrate — RIDE-ONLY CONTROL FIRST (I5)

**RIDE-ONLY CONTROL (printed first):** 709 winning campaigns, median gross
**3.09 R**, mean gross **10.95 R**.

Counterfactual stop-to-reclaim-structure figures are emitted per campaign per
`(tf, ema, cushion)` in `MC1_results.json` under `D7.b_ratchet.campaigns`.

**Test-and-reclaim events during campaign life: 98,395** across
{200,300,450} × {15m,1h,4h} × cushions {0.25, 0.5, 1.0}·ATR. Sample of the
summary (full table in `MC1_results.json`):

| tf | ema | cushion | n events | median bars to reclaim | median subsequent MFE (ATR) | p75 |
|---|---|---|---|---|---|---|
| 15m | 200 | 0.25 | 16,313 | 1.0 | 1.922 | 3.541 |
| 15m | 200 | 0.50 | 12,517 | 2.0 | 1.943 | 3.609 |
| 15m | 200 | 1.00 | 8,385 | 4.0 | 1.974 | 3.722 |
| 15m | 300 | 0.25 | 11,336 | 1.0 | 1.905 | 3.468 |

**Definitions are DERIVED for this run and are NOT [VETO] constants** — TEST =
bar low ≤ EMA (long) / high ≥ EMA (short); RECLAIM = a close ≥ EMA + n·ATR within
10 bars with no intervening close ≤ EMA − n·ATR; CONTINUATION = max favourable
excursion over the following 20 bars in ATR units. **Tables only. No rule is
adopted.**

---

## 10 · D-8 · HYGIENE

### 10.1 The P-SEQ-ii check — a NEGATIVE finding

The contract says: *"grep LEDGER.md for the P-SEQ-ii entry: print registration
text + in-entry ordering-anomaly note verbatim; state CONFORMS or itemize the
diff."*

```
grep -c "P-SEQ" LEDGER.md   ->   0        (over 871 lines)
```

**The entry does not exist.** The verdict is therefore neither CONFORMS nor a
diff — it is an **absence**. `LEDGER.md` ends at line 871 and its last heading is
`## 2026-08-03 — BRIEF-2 built (CONTRACT v4 Amendment 2)`; nothing from 2026-08-04
onward was ever appended, so the entire SEQ8 cycle is unrecorded in the evidence
ledger.

The texts the contract expected to find in-entry exist only *outside* the ledger.
Reproduced verbatim so they are not lost again:

**Proposed registration text** — `exchange/reports/SESSION_SUMMARY_HEPHAESTUS_2026-08-04_SEQ8.md:75`:
> **Reviewer — LEDGER entry:** P-SEQ-ii is **not** registered in `LEDGER.md` (`grep` → 0 hits). The contract commissioned scoring it and the SEQ-7 ruling registered it, so it was scored; but the standing rule wants the verdict to postdate a registration commit. **Proposed entry:** `P-SEQ-ii`, prior **75%**, falsified if the leap is not the largest 4h arrival category, or adjacency not the largest at 1h, on fewer than 5 of 7 assets. **Measured: replicates, 7/7 both limbs, Atlas frame.** The builder does not write to `LEDGER.md`; this is yours to land.

**The ordering-anomaly note** — `exchange/reports/NOTE_DIONYSUS_to_APOLLO_2026-08-04_SEQ8_findings_and_agreements.md:22`:
> - **APOLLO:** verify the P-SEQ-ii ledger entry (ordering anomaly recorded in-entry: registration and verdict land together, same day; the contract carries the pre-run registration text); fold the §2 qualifiers into the synthesis; own final priors when parked promotions return; carry the errata.

The governance rule it is measured against — `LEDGER.md:812`:
> - **STANDING CLARIFICATION** … For Tier-A and Tier-B census phases, the G-7 pre-registration binds the ANALYSIS. Building or instrumenting a trade-independent substrate BEFORE the pre-registration is PERMITTED - the substrate is measurement, not a hypothesis test. What must follow the registration commit is every scored deliverable, prediction verdict and scorecard.

**This absence is folded into the LEDGER_APOLLO append as PENDING item 1.** The
builder does not write to `LEDGER.md`; landing the entry remains the reviewer's.

### 10.2 LEDGER_APOLLO append

`exchange/status/LEDGER_APOLLO.md` — one `=== STATUS_APOLLO — 2026-08-10 ===`
entry appended in the file's own naiad-eod template, closing the 9-day
staleness and recording: the 08-05 re-priming, the 08-06 rulings (MC defaults,
rule set v0.2, the path), the continuous-queryability amendment, the **declined**
lockbox change, the synthesis filing with its sha256, this run's headline
numbers, and four PENDING items.

---

## 11 · FINDINGS — REPORTED, NOT FIXED

1. **MC-1's feasibility premise does not survive the exploration ceiling.**
   §3.4 MC-1 states "1M carrying {12,25} only, 1W carrying up to 200", derived
   from "~90 monthly, ~360 weekly bars". Under the ceiling BTCUSDT has **252**
   weekly and **58** monthly bars, so D-1 measures **1W warm to EMA25 only** and
   **1M to EMA12 only**. The synthesis figure is a full-estate count; D-1 is
   ceiling-bound because F-MC1 requires it to reconcile with SEQ8 D6. Both are
   right about different windows. No constant was changed.
2. **P-i and P-iv are view-contingent and threshold-marginal** (§8.5). The
   registrations name no view; the verdict flips between SEQ8's `window_chained`
   and `direction_consistent` families. Operator ruling wanted.
3. **The May-26 archetype scores 2/4 on its own similarity family** (§5.5) — and
   it is a lattice-B 12/25 cross, not a lattice-A trio cross.
4. **"pullback-anchored frame" (P-i) has no referent in the SEQ8 substrate** and
   was not applied as a filter (§8.3).
5. **"trio" has no referent in SEQ8**; the population ruling is printed in §6,
   along with the SEAL degeneracy on the 89_200 subpopulation.
6. **The dossier header says "lockbox-era data" but the study window is
   post-lockbox.** `analytics.LOCKBOX_END_MS` = 2025-10-06; the window is
   2026-02-01 → 2026-08-01. The header string is contract-mandated verbatim and
   was **not altered**; the factual mismatch is reported here instead.
7. **"25ema in 1m" is not in the synthesis.** §3.4 MC-5 says "1m 89/200/300/450
   (your restricted set)" — no 25. The contract's ratification line carries it as
   a post-synthesis operator amendment, and the contract's I3 set
   {25,89,200,300,450} was used. Flagged so the lineage is not lost.
8. **"memory #20" could not be confirmed.** The string appears nowhere in the
   repo. Best evidence is Entry 20 of
   `docs/memory/claude_project_memory_2026-08-03.md:81-82` (the prime directive),
   but the panel was renumbered 30 → 23 entries on 2026-08-03, so the index is
   not stable. Treated as inferred, not confirmed; nothing in this run depends on it.
9. **SEQ8 F-SEQ3 prose vs code differ by one bar on the left edge.** The prose
   says the span starts at "first rung bar_close"; `seq8_outcomes.py:257-261`
   compares against `init_ts` (bar OPEN). This run **consumes SEQ8's own bridge
   table**, so it inherits the code's behaviour; the discrepancy is SEQ8's to
   resolve and is recorded here because F-MC5 asks for the rule verbatim.
10. **`publish_exchange.py` still has no size guard** — queue item 002 D3
    remains unbuilt. Its only check is path scope.

---

## 12 · FILE DISPOSITION (six columns, with BOX-COST)

Box capacity **6,390,000 B** (derived; `exchange/DIGEST.md:19`). 1% = 63,900 B.
**BOX-COST is only realised for files that are actually pushed**; the gitignored
bulk shows what it *would* cost, and its realised cost is zero.

| File | Class | Bytes | Disposition | Home | BOX-COST |
|---|---|---|---|---|---|
| `exchange/reports/BUILD_APOLLO_2026-08-06_MC1.md` | TEXT deliverable | 38,817 | **PUSHED** | `exchange/reports/` | 0.61% |
| `exchange/reports/MC1_tables.md` | TEXT deliverable | 18,887 | **PUSHED** | `exchange/reports/` | 0.30% |
| `exchange/reports/MC1_results.json` | TEXT deliverable | 261,072 | **PUSHED** | `exchange/reports/` | **4.09%** ⚠ |
| `exchange/queue/2026-08-06_MC1_may26_program_APOLLO.md` | COORDINATION | 9,386 | **PUSHED** | `exchange/queue/` | 0.15% |
| `exchange/status/LEDGER_APOLLO.md` | COORDINATION | 6,557 | **PUSHED** | `exchange/status/` | 0.10% |
| `research_outputs/mc1/**` (28 files: ops_klines, ops_series, registry, SEQ8 compacts, D4–D7 tables, 1m ladders) | OPS + EVIDENCE bulk | 162,626,825 | NOT pushed (gitignored) | `research_outputs/mc1/` | 2545% (notional) |
| `scripts/mc1_program.py` | CODE | 99,653 | **NOT pushed** — outside `exchange/` scope guard | repo worktree (uncommitted) | 1.56% ⚠ |
| `scripts/mc1_report.py` | CODE | 8,392 | **NOT pushed** — outside scope guard | repo worktree (uncommitted) | 0.13% |
| `.gitignore` | CODE | 4,542 | **NOT pushed** — outside scope guard | repo worktree (uncommitted) | 0.07% |

Total pushed this run: **334,719 B = 5.24% of the box.** Total bulk withheld:
**162,626,825 B**, of which the largest single artifacts are
`seq8_cascades_compact.parquet` (41.2 MB), `d7a_1m_ladders.parquet` (19.9 MB) and
`seq8_events_compact.parquet` (17.2 MB). Per-file sizes and sha256 are in
`MC1_results.json`.

**Over ~1% of the box, with intended home:**
- `MC1_results.json` (4.09%) — the machine-readable record. Intended home is
  `exchange/reports/`; it is the one artifact the web lanes need in full. If the
  box tightens, the `D7.b_ratchet.campaigns` array (already truncated to 200 of
  709) is the first thing to move to `research_outputs/mc1/`.
- `scripts/mc1_program.py` (1.56%) — code, and **not pushed at all**, so its box
  cost is not realised.
- The `research_outputs/mc1/**` bulk is 25× the whole box and is exactly why it
  is gitignored; its realised box cost is **zero**.

`.gitignore` was extended this run (**stated, as the contract requires**) with
`research_outputs/mc1/**`, so none of the bulk can be swept into a commit.

---

## 13 · VERSIONS, HASHES, COMMITS

| item | value |
|---|---|
| branch / HEAD at run | `v12-v1-census` / `7a3a881` |
| Python | 3.12.10 |
| `ANALYTICS_VERSION` | 1.5.0 |
| `analytics_sha()` | `ea5f02f21ca43b6b71e450b540ff09c807b305971e3eb8cff50bea84c985dc91` |
| exploration ceiling | 1719792000000 (`census_build.py:60`) |
| seed | 20260806 |
| SS synthesis sha256 | `f184f105c0612128c9ed5819d72fe6ff0c2d123378b0923d08b90bc856c4c7f2` |
| SEQ8 events consumed | 288,711 rows |
| SEQ8 cascades/outcomes consumed | 950,145 rows each, 0 alignment mismatches |
| SEQ8 bridge consumed | 301,018 rows |
| fixtures | **11 / 11 PASS** |

Per-file sha256 for every bulk artifact is in `MC1_results.json` under
`D3.*.sha256`, `D4.sha256`, `D5.sha256`, `D6.sha256`, `D7.*_sha256`.

---

## 14 · WHAT THIS RUN DID NOT DO

No lockbox or seal modification (the operator's conditional authorization was
**declined as unnecessary** and is recorded as such) · no lockbox row in any
scored table · no engine change · no trading rule adopted · no estate write
(byte-identical before/after, 70 files / 656,085,646 B) · no new resampler · no
analytics claim beyond counting.

— HEPHAESTUS, executor, 2026-08-10
