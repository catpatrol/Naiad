# BUILD · 2026-08-12 · CENSUS-2B / V-ULT-1 — the U-VHT data module

**Lane:** HEPHAESTUS (builder) · **Drafted:** APOLLO · **Class:** **substrate + DISPLAY-ONLY /
Tier-E first-look** · **Selection surface m = 0** · **Seed 20260812** ·
**Contract:** operator paste 2026-08-12, *"Secret Sauce is a momentum system"*.
**Programs:** `scripts/census2b_program.py` (new) · `scripts/census2b_firstlook.py` (new) ·
`scripts/census2b_report.py` (new). **`scripts/census2a_program.py` is BYTE-UNTOUCHED.**
**Bulk:** all outputs born on `D:/Naiad/research_outputs/census2b/`.

> **The one sentence that governs this document.** Stages 1–4 build a *substrate* — EMAs, ribbon
> state and cross events, with a warm-up law asserted rather than assumed — and Stage 5 *looks at
> it once*, descriptively. **No registration is made. No threshold is swept. No arm is ranked and
> kept.** Everything in §5 is stamped `EXPLORATION — ungated; promotion requires registration`
> and is logged as a probe with `m = 0`. Nothing here is a finding.

---

## 0 · GATES

All hard assertions printed and passed before any compute.

| gate | result |
|---|---|
| `git rev-parse --short HEAD` | `7a3e071` |
| remote contains `catpatrol/Naiad` | PASS — `https://github.com/catpatrol/Naiad.git` |
| IDENTITY (two-sided) | PASS — pwd `/c/Naiad`, and **no** `OneDrive` in the path |
| `git branch --show-current` | PASS — `v12-v1-census` |
| `test -f scripts/census2a_program.py` | PASS — 171,646 B |
| `test -f scripts/drive_wait.py` | PASS — 9,817 B |
| DRIVE GATE `wait_for_drive('D:/Naiad')` | **PRESENT** — `attempts=1 elapsed=0.00s budget=18.0s` |

`wait_for_drive` never raises by design; the HALT is the caller's, and it is coded as
`SystemExit(2)` on any state outside `{PRESENT, WOKE}`.

---

## 1 · THE ONE THING THE CONTRACT GOT AMBIGUOUS, SETTLED BEFORE ANY COMPUTE

The contract pins `warmfactor = 3.46`, `warm_bars = ceil(3.46*N)`, **and calls it "the SEQ8
rule"**. The SEQ8 rule as it actually exists in this estate
(`scripts/seq8_extract.py:114-119`) is a residual-decay expression:

```python
def warmup_bars(length, residual=SEED_RESIDUAL):   # SEED_RESIDUAL = 1e-3
    alpha = 2.0 / (length + 1.0)
    return int(math.ceil(math.log(residual) / math.log(1.0 - alpha)))
```

These are **not the same expression**, and the difference is not decorative: this estate has
twice been bitten by cold EMAs, and `warmup_bars(200) = 691` — not `692` — is the number the
existing machinery uses. A build that silently picks one loses either contract compliance or
parity.

**F-B0 settles it by arithmetic rather than by preference**, and runs before Stage 1's first
row. The contract's constant is the *conservative* one for every length in the slate — it
over-warms by 0 to 30 bars and **never under-warms**. It is therefore used **exactly as
written, by name**, and the estate's `warmup_bars` is used only as the thing F-B0 checks it
against.

<!--FB0-->

Had the comparison gone the other way for even one length, this build would have halted rather
than choose silently — `F-B0 FAIL` raises `SystemExit(2)` before Stage 1 loads its first frame.

The same reading is applied to two other places where the contract's prose and the estate's
code disagree, both recorded in §7:

- **`knot`.** The contract says *"knot threshold c = 0.5\*ATR"* and then *"knot flag (width <
  c\*ATR)"*, which composes to `width < 0.5*ATR²`. `census2a_program.py:92` settles it:
  `RIBBON_C = 0.5`, used as `spread < RIBBON_C * atr`. **Implemented as `width_atr < 0.5`.**
- **`width_delta_k` vs `±0.05*ATR`.** Implemented literally: the *raw* width change over `k=20`
  bars, divided by ATR at the current bar, thresholded at `±0.05`. That is algebraically the
  contract's sentence, and storing the ATR-normalised delta is what makes the threshold a bare
  number in the artifact.

---

## 2 · STAGE 1 — THE FEASIBILITY MATRIX

Printed **before any compute**, as required. 630 cells = 5 assets × 7 timeframes × 18 lengths.

**Verdict vocabulary, defined against the census's own constants, not new ones.** The evidence
era is `[ASSET_STARTS[asset], CEIL_MS)` where `CEIL_MS = 2024-07-01T00:00:00Z` —
`census_build.py:54-60`, imported, never restated.

| verdict | meaning |
|---|---|
| `FULL` | warm **before** the evidence era opens — coverage of the census window is 100 % |
| `PARTIAL(evidence)` | warms **inside** the evidence era, after it opened |
| `OPS-ONLY` | warms, but only **after** the evidence ceiling — exists for the live era, cannot speak to the census |
| `NEVER` | never warms at all — **skipped, not computed** |

<!--FRAGMENT-->

### F-B1 — three cells hand-recomputed from first principles

Three cells were re-derived from the raw parquet by an independent code path (an explicit
`ceil(3.46*L)`, a Python-level scan of the era window) and compared field-by-field against the
matrix. **3/3 MATCH.**

```
BTCUSDT   12h  N= 5000  bars=5,061    warm=17,300 warm_from=-          cov=0.000 -> NEVER
SOLUSDT   5m   N= 2618  bars=621,828  warm=9,059  warm_from=2020-10-15 cov=0.989 -> PARTIAL(evidence)
ZECUSDT   1h   N=  316  bars=57,146   warm=1,094  warm_from=2020-03-21 cov=0.987 -> PARTIAL(evidence)
```

### What the matrix says, against what the contract expected

The contract predicted *"UH/VH = LTF objects (never on 4h+); H comfortable ≤1h; MH ≤4h; M/FAST
everywhere."* The matrix **confirms the shape and sharpens every boundary**:

| contract's expectation | the matrix |
|---|---|
| UH/VH never on 4h+ | **UH: NEVER on 4h and 12h** (needs 17,300 bars; 4h has 12,768–15,184). **VH: NEVER on 12h**, and on 4h it is `OPS-ONLY` for 2618/3618 — it warms, but only after the evidence wall, so it can be drawn and cannot be scored |
| H comfortable ≤1h | H is `PARTIAL` from 15m to 4h, `OPS-ONLY` (BTC/ETH/ZEC) or `NEVER` (SOL/NEAR) on 12h. "Comfortable ≤1h" is right; 4h is usable at 55–79 % coverage |
| MH ≤4h | MH survives even 12h, at 55–73 % coverage. Slightly better than expected |
| M/FAST everywhere | Confirmed. FAST is `FULL` on every tf except 12h; M is `FULL` to 1h |
| — | **1m is `FULL` for all 18 lengths on all 5 assets.** UH(5000) needs 17,300 bars = 12 days of 1m tape against 5.9–6.9 years available |

**45 of 630 cells are `NEVER` and were skipped, not computed** — listed by name in the fragment
above. Their columns exist and are all-NaN so the schema stays uniform and nothing cold can be
read. **14 cells are `OPS-ONLY`.**

---

## 3 · STAGE 2 — EMAS + ATR

18 EMAs and ATR(14) per feasible cell, one pass, `float32` on disk, **NaN before warm, always**.
The recursion is `engine.indicators.ema` itself — the ratified implementation, not a fast
re-write. `pandas.ewm(adjust=False)` is 135× faster and is **not** bit-identical (it evaluates
`(1-α)·prev + α·x` where the engine evaluates `prev + α·(x-prev)`; max abs difference 1.24e-9 on
a 729k-bar series). Parity with census-2A and SEQ8 by construction was judged worth 12 minutes.

### Non-1m panel

```
asset     tf         bars  emas  skip    secs       MB
------------------------------------------------------
BTCUSDT   5m      728,833    18     0    70.1     88.7
ETHUSDT   5m      705,915    18     0    60.2     84.4
SOLUSDT   5m      621,828    18     0    70.6     73.6
NEARUSDT  5m      612,888    18     0    98.3     71.2
ZECUSDT   5m      685,752    18     0   128.8     77.4
BTCUSDT   15m     242,945    18     0    31.4     36.9
ETHUSDT   15m     235,305    18     0    26.4     35.0
SOLUSDT   15m     207,276    18     0    21.2     29.9
NEARUSDT  15m     204,296    18     0    18.9     28.7
ZECUSDT   15m     228,584    18     0    25.9     32.1
BTCUSDT   30m     121,473    18     0    10.6     18.1
ETHUSDT   30m     117,653    18     0    12.8     17.3
SOLUSDT   30m     103,638    18     0    11.7     14.7
NEARUSDT  30m     102,148    18     0    13.8     14.0
ZECUSDT   30m     114,292    18     0    16.2     15.7
BTCUSDT   1h       60,737    18     0     6.8      8.7
ETHUSDT   1h       58,827    18     0     6.6      8.3
SOLUSDT   1h       51,819    18     0     5.7      7.1
NEARUSDT  1h       51,074    18     0     5.6      6.7
ZECUSDT   1h       57,146    18     0     8.5      7.6
BTCUSDT   4h       15,184    16     2     3.8      1.7
ETHUSDT   4h       14,707    16     2     2.3      1.7
SOLUSDT   4h       12,955    15     3     1.8      1.4
NEARUSDT  4h       12,768    15     3     1.7      1.3
ZECUSDT   4h       14,286    15     3     1.7      1.5
BTCUSDT   12h       5,061    12     6     0.5      0.5
ETHUSDT   12h       4,902    12     6     0.6      0.5
SOLUSDT   12h       4,318    11     7     0.6      0.4
NEARUSDT  12h       4,256    11     7     0.6      0.4
ZECUSDT   12h       4,762    12     6     0.7      0.4

running totals: rows=5,405,628  bytes=685,889,690 (0.69 GB)  elapsed=681s
```

The `skip` column is the `NEVER` count for that cell — 0 on 5m/15m/30m/1h, 2–3 on 4h, 6–7 on 12h.

<!--STAGE2_1M-->

### F-B2 — NaN-before-warm, asserted rather than intended

The check the estate's own history demanded: count finite values inside each series' warm-up
region and require **zero**. It also asserts that every `NEVER` column is entirely NaN, so a
skipped cell cannot leak a value it was never supposed to have.

```
F-B2 PASS -- 0 cold-head values across 540 series
```

Because the cold head is NaN at the source, `crossover`/`crossunder` return `False` there **by
construction** — no downstream stage has to remember, and Stage 4 cannot emit a warm-up event
even if it tried.

### F-B3 — one EMA per family, hand-recomputed on 50 bars, bit-match

For each of the six families, the middle member's EMA was re-run as a literal Python recursion
over the whole prefix and compared to the stored `float32` column across bars
`[warm, warm+50)`. **Bit-match on all six.**

```
F-B3 PASS -- every family's middle EMA bit-matches the recursion
```

---

## 4 · STAGE 3 — THE RIBBON LIBRARY

`ribbon(a, b, df) -> {upper, lower, mid, width_atr}` is **general**, as the operator required:
it takes any two lengths on any frame that has a `close`. If `e{a}`/`e{b}` are already present
they are used as stored; otherwise they are computed on the fly **under the same warm-up law**,
so an ad-hoc pair on ad-hoc lookback data obeys identical rules to the canonical six.

The band of a named family is the envelope of its **extreme** members — `ribbon(fastest,
slowest)` — which is what makes F-B4a true by construction rather than by luck. The middle
member is not discarded: it is exactly what `orientation` reads.

Per-bar state, written to `ribbons/{asset}/{tf}.parquet`: `upper · lower · mid · width_atr ·
width_delta_k · state · orientation · knot · price-position`, for all six families. States,
orientations and positions are `int8` codes with the legend pinned in the manifest.

### F-B4 — four unit tests, all PASS

| test | what it proves | result |
|---|---|---|
| **F-B4a** | `ribbon(9,26)` reproduces the stored FAST band exactly — `upper`, `lower`, `mid`, `width_atr` all `array_equal(..., equal_nan=True)` | PASS |
| **F-B4b** | the general form works on a pair in **no** family: `ribbon(45,700)` on a frame carrying only OHLC+ATR; first finite width lands at bar 2,422 = `warm_bars(700)`, not earlier | PASS |
| **F-B4c** | orientation flips on a hand-built synthetic (a rising leg then a falling leg): **100.0 %** bull-fanned on the rise, **100.0 %** bear-fanned on the fall | PASS |
| **F-B4d** | state thresholds exercised in **both** directions, on the synthetic *and* on a real cell — a fixture that only ever saw one direction would be certifying half the classifier | PASS |

A separate check confirmed the `k`-shift cannot leak across the warm boundary: `width_delta_k`
stays NaN for exactly `k = 20` bars past the first warm bar, then becomes finite.

---

## 5 · STAGE 4 — CROSS EVENTS

The pared taxonomy, exactly as specified: **18 within-ribbon pairs** (`a_b`, `a_c`, `b_c` per
family) + **5 adjacent midline pairs** (`12_89`, `89_316`, `316_889`, `889_2618`, `2618_4618`)
+ **price↔band** per ribbon (`enter` / `exit` / `reject-at-band`).

`reject-at-band` uses the **ratified kiss grammar carried from census-2A** — approach within
`0.25·ATR`, veer `≥ 0.75·ATR` within `10` bars, break on the first genuine sign change — applied
with `series = close` and `level =` each band rail. The function is *restated* rather than
imported so `census2a_program.py` is never executed as a side effect; **F-B5c proves the copy is
element-for-element equal to the original**.

**F-KEY declared key:** `(asset, tf, pair_class, pair, event, dir, ts_ms)`, asserted at write
time for every cell. `dup = 0` on all 35 cells.

```
asset     tf         events     within   midline       band    secs      MB
---------------------------------------------------------------------------
BTCUSDT   5m        616,716    128,689    18,403    469,624    11.4     9.3
BTCUSDT   15m       198,178     42,362     5,787    150,029     6.1     3.7
BTCUSDT   30m        94,982     20,391     2,763     71,828     1.7     1.7
BTCUSDT   1h         45,436     10,051     1,281     34,104     0.9     0.8
BTCUSDT   4h         10,111      2,340       281      7,490     0.4     0.2
BTCUSDT   12h         2,977        713        87      2,177     0.5     0.1
ETHUSDT   5m        595,055    124,081    17,615    453,359    14.0     9.0
ETHUSDT   15m       191,378     40,121     5,585    145,672     3.4     3.5
ETHUSDT   30m        93,102     19,553     2,761     70,788     1.4     1.7
ETHUSDT   1h         43,907      9,687     1,278     32,942     0.6     0.8
ETHUSDT   4h         10,073      2,305       297      7,471     0.2     0.2
ETHUSDT   12h         2,905        703        78      2,124     0.1     0.1
SOLUSDT   5m        515,805    106,033    15,088    394,684    11.1     8.0
SOLUSDT   15m       166,904     34,334     4,818    127,752     4.1     3.1
SOLUSDT   30m        82,081     16,787     2,366     62,928     1.6     1.5
SOLUSDT   1h         39,447      8,224     1,165     30,058     0.8     0.7
SOLUSDT   4h          9,120      1,953       261      6,906     0.3     0.2
SOLUSDT   12h         2,646        639        81      1,926     0.1     0.1
NEARUSDT  5m        517,666    106,136    15,312    396,218     8.4     8.0
NEARUSDT  15m       168,556     35,119     4,937    128,500     2.8     3.1
NEARUSDT  30m        81,678     17,093     2,371     62,214     1.5     1.5
NEARUSDT  1h         39,157      8,368     1,131     29,658     0.6     0.7
NEARUSDT  4h          8,641      1,963       257      6,421     0.2     0.2
NEARUSDT  12h         2,487        619        66      1,802     0.1     0.0
ZECUSDT   5m        581,014    119,366    17,443    444,205    11.7     8.8
ZECUSDT   15m       191,766     39,450     5,456    146,860     3.3     3.5
ZECUSDT   30m        93,486     19,231     2,701     71,554     1.5     1.7
ZECUSDT   1h         45,450      9,307     1,301     34,842     0.6     0.8
ZECUSDT   4h         10,316      2,187       298      7,831     0.2     0.2
ZECUSDT   12h         3,066        711        94      2,261     0.1     0.1
```

<!--STAGE4_1M-->

### F-B5 — determinism, hand-verification, and grammar parity

**F-B5a — determinism.** `NEARUSDT 4h` re-run from the artifacts and re-hashed:
`stored=645dcb441e261fe2  rerun=645dcb441e261fe2  **IDENTICAL**`.

**F-B5b — three hand-verified events per new pair class.** Each event was re-checked against the
underlying series by an independent expression (not the detector), printing the operands:

```
within-ribbon (close-confirmed sign change)   (n=1,963)
  2020-10-22T20:00:00Z  9_12   cross_up   e9-e12: prev=-0.0004 now=+0.0000  OK
  2020-10-23T00:00:00Z  9_12   cross_down e9-e12: prev=+0.0000 now=-0.0008  OK
  2020-10-24T16:00:00Z  9_12   cross_up   e9-e12: prev=-0.0009 now=+0.0001  OK

adjacent midline   (n=257)
  2020-12-07T04:00:00Z  12_89  cross_down e12-e89: prev=+0.0029 now=-0.0019  OK
  2020-12-16T16:00:00Z  12_89  cross_up   e12-e89: prev=-0.0027 now=+0.0014  OK
  2020-12-24T04:00:00Z  12_89  cross_down e12-e89: prev=+0.0012 now=-0.0130  OK

price<->band enter/exit   (n=4,194)
  2020-11-01T00:00:00Z  FAST_band enter up   below -> inside  band=[0.6452,0.6749] c=0.6504  OK
  2020-11-01T04:00:00Z  FAST_band exit  down inside -> below  band=[0.6427,0.6718] c=0.6327  OK
  2020-11-01T20:00:00Z  FAST_band enter up   below -> inside  band=[0.6281,0.6570] c=0.6363  OK

reject-at-band (ratified kiss 0.25/0.75/10)   (n=2,227)
  2020-11-09T12:00:00Z  FAST_upper reject upper  touch=0.133ATR veer=1.233ATR gap=1  OK
  2020-11-12T04:00:00Z  FAST_upper reject upper  touch=0.215ATR veer=0.912ATR gap=1  OK
  2020-11-15T04:00:00Z  FAST_upper reject upper  touch=0.129ATR veer=0.948ATR gap=3  OK
```

**F-B5c — grammar parity.** `refusal_events` in this program vs the census-2A original, run on a
real series: `flags equal=True  confirms equal=True  n_events=251`. **PASS.**

---

## 6 · STAGE 5 — THE FIRST LOOK (DISPLAY-ONLY · Tier-E · m = 0)

Every artifact and every table carries the header:

> `CLASS: DISPLAY-ONLY / Tier-E — EXPLORATION, ungated; promotion requires registration.`
> `Nothing here is a finding. Selection surface m = 0.`

<!--FIRSTLOOK-->

---

## 7 · FINDINGS REPORTED, NOT FIXED

**1 · The campaign book has no exit timestamp, so "VH state at exit" cannot be computed.**
The contract asks for VH ribbon state *at entry and at exit*. `cen4_book` carries `ts_open` and
`ts_ms` — **both the entry**. `cen5_campaigns` carries no exit timestamp at all, only realised
outcomes (`ride_R`, `give_back_R`, `mfe_R`). `cen2_ledger.window_close_ts` is the *arming
window's* close, a different object; using it as an exit would be an invention. **The entry side
is computed in full; the exit side is left undone and named.**

**2 · `cen4_book.tranche_id` is not unique — 360 duplicates in 6,897 rows.** It is unique only
*within a cell*, exactly as `census2a_program.assert_key`'s own docstring warns. The whole key is
`cell|tranche_id`, which is what `cen5_campaigns.tranche_id` already stores. Joining the two
books on the bare `tranche_id` yields **zero** matches; on the composite it yields 6,643 with
`dup=0`. Not fixed in census-2A's artifacts; worked around here and declared.

**3 · `cen5_campaigns` has `dup=1` on `(asset, ts_ms)`.** A BTC intraday and a BTC swing campaign
share one instant. `mandate` belongs in the key. This is a declared-key defect, not a data
defect, and it is why F-KEY here asserts `(asset, ts_ms, mandate)`.

**4 · The state window `k = 20` is not scale-matched to the ultra ribbons.** UH's three lines
(4236/4618/5000) span only 1.18× in length, so the band width barely moves over 20 bars and the
classifier returns `flat` for **95.1 %** of warm bars — against **23.4 %** for VH. `UH state`
therefore carries far less information than `VH state`, and the two must not be read as the same
measurement. The constants are VETO by name and were **not** changed; the shares are printed as
the evidence.

**5 · `knot` and `expanding` are near-tautological for VH.** A knot run ends precisely when width
rises back through `0.5·ATR` — mechanically, a width that is increasing. So the next bar is
already `expanding`. Measured: **66–68 % of VH knot episodes "expand" on the very next bar**,
against **2.5–5.2 %** for UH. VH's `time-to-expansion ≈ 1 bar` is therefore two-thirds a
statement about the definitions and one-third about the tape. UH's ~500-bar figure is real.
Reported; the composed definitions are the contract's and were not altered.

**6 · The toll in ATR units grows sharply as the timeframe shortens.** Census-2A's quoted
0.026–0.059 ATR is a **4h** figure. On 5m the same 10 bps round trip is **0.29–0.35 ATR** —
roughly an order of magnitude larger — because ATR shrinks faster than price does. A first draft
of §6(d)(ii) quoted the 4h number beside 5m tables; it was corrected to measure the toll on each
population's own bars. **Any future LTF table must do the same.**

**7 · `float32` on disk costs precision at BTC-scale prices.** A `float32` mantissa gives ~7
significant digits, so a $100,000 print rounds to ~0.008. The contract specifies `float32`
columns and that is what is written; all arithmetic is done in `float64` and cast only at write.
Ribbon geometry is unaffected at ATR scale; tick-exact work must not read these columns.

**8 · A scoped run overwrote the feasibility matrix, and now merges.** `--tfs 1m` computed a
90-row matrix and wrote it over the 630-row one — the *exact* failure I12 exists to prevent,
reproduced in a new file. Fixed: the matrix now merges on `(asset, tf, family, length)` with the
scoped run's cells winning, and prints how many it carried.

**9 · F-B1's sample was hardcoded and crashed on a scoped matrix.** The three hand-recomputed
cells were fixed cell names; under `--tfs 1m` none of them exists and the fixture raised
`IndexError`. A fixture that cannot find its own sample must pick a new one deterministically —
it must never crash, and far more importantly must never quietly check nothing. Fixed with a
deterministic fallback drawn from the matrix's own sorted order.

**10 · The live cache grows daily, so `bars_available` drifts between runs.** BTC 1m read
3,644,162 bars at the start of this session and 3,645,602 an hour later. Evidence-era columns are
unaffected (they are bounded by `CEIL_MS = 2024-07-01`); only `bars_available` and `last_bar`
move. **No verdict changed.** Recorded so a re-run that prints different bar counts is not
mistaken for a defect.

---

## 8 · DISPOSITION & BOX-COST

<!--BOXCOST-->

**Residency (I2).** Every byte of substrate lives on `D:/Naiad/research_outputs/census2b/`.
**Not one is committed.** `publish_exchange` stages `exchange/**` only.

**Three program files added, none modified.** `scripts/census2b_program.py`,
`scripts/census2b_firstlook.py`, `scripts/census2b_report.py`. `engine/` is untouched.
`scripts/census2a_program.py` is **byte-untouched** and is never executed by this program —
F-B5c imports it in an isolated module spec purely to compare one function, and degrades to a
SKIP if that import is not clean.

**Manifest pinned** at `D:/Naiad/research_outputs/census2b/census2b_manifest.json` with
**pin-merge semantics (I12)**: an existing `pins` block survives untouched and artifact entries
merge by key, so a partial re-run never drops what an earlier stage recorded.

**No registration. No pin on the census-2A record. The census-2A manifest, artifacts and probe
ledger are untouched** — census-2B writes to its own `OUT` and its own manifest filename, which
is the specific trap §8 of the recon flagged.

---

## 9 · REPRODUCTION

```
python scripts/census2b_program.py --stage 1                    # feasibility matrix only
python scripts/census2b_program.py --stage 2,3,4 --skip-1m      # panel substrate, 1m deferred
python scripts/census2b_program.py --stage 2,3,4 --tfs 1m       # the 1m bulk, run LAST
python scripts/census2b_program.py --stage 5  --skip-1m         # the Tier-E first look
python scripts/census2b_report.py                               # build-document tables
```

Seed 20260812 throughout. Every stage is deterministic; F-B5a re-runs a cell and compares
sha256. Stage 1 always runs, because it is the gate every later stage reads its feasible-length
set from.

---

<!--LEDGER-->
