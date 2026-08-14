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

| family | N | ceil(3.46·N) | exact SEQ8 | delta | safe |
|---|---|---|---|---|---|
| FAST | 9 | 32 | 31 | +1 | yes |
| FAST | 12 | 42 | 42 | +0 | yes |
| FAST | 26 | 90 | 90 | +0 | yes |
| M | 62 | 215 | 215 | +0 | yes |
| M | 89 | 308 | 308 | +0 | yes |
| M | 127 | 440 | 439 | +1 | yes |
| MH | 262 | 907 | 905 | +2 | yes |
| MH | 316 | 1,094 | 1,092 | +2 | yes |
| MH | 423 | 1,464 | 1,461 | +3 | yes |
| H | 616 | 2,132 | 2,128 | +4 | yes |
| H | 889 | 3,076 | 3,071 | +5 | yes |
| H | 1272 | 4,402 | 4,394 | +8 | yes |
| VH | 1618 | 5,599 | 5,589 | +10 | yes |
| VH | 2618 | 9,059 | 9,043 | +16 | yes |
| VH | 3618 | 12,519 | 12,497 | +22 | yes |
| UH | 4236 | 14,657 | 14,631 | +26 | yes |
| UH | 4618 | 15,979 | 15,951 | +28 | yes |
| UH | 5000 | 17,300 | 17,270 | +30 | yes |

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

### The verdict grid — worst verdict across each family's three members

**BTCUSDT**

| family | 1m | 5m | 15m | 30m | 1h | 4h | 12h |
|---|---|---|---|---|---|---|---|
| FAST | FULL | FULL | FULL | FULL | FULL | FULL | PART |
| M | FULL | FULL | FULL | FULL | FULL | PART | PART |
| MH | FULL | FULL | FULL | PART | PART | PART | PART |
| H | FULL | FULL | PART | PART | PART | PART | OPS |
| VH | FULL | PART | PART | PART | PART | OPS | NEVER |
| UH | FULL | PART | PART | PART | PART | NEVER | NEVER |

**ETHUSDT**

| family | 1m | 5m | 15m | 30m | 1h | 4h | 12h |
|---|---|---|---|---|---|---|---|
| FAST | FULL | FULL | FULL | FULL | FULL | FULL | PART |
| M | FULL | FULL | FULL | FULL | FULL | PART | PART |
| MH | FULL | FULL | FULL | FULL | PART | PART | PART |
| H | FULL | FULL | PART | PART | PART | PART | OPS |
| VH | FULL | PART | PART | PART | PART | OPS | NEVER |
| UH | FULL | PART | PART | PART | PART | NEVER | NEVER |

**SOLUSDT**

| family | 1m | 5m | 15m | 30m | 1h | 4h | 12h |
|---|---|---|---|---|---|---|---|
| FAST | FULL | FULL | FULL | FULL | FULL | FULL | PART |
| M | FULL | FULL | FULL | FULL | PART | PART | PART |
| MH | FULL | FULL | FULL | PART | PART | PART | PART |
| H | FULL | FULL | PART | PART | PART | PART | NEVER |
| VH | FULL | PART | PART | PART | PART | OPS | NEVER |
| UH | FULL | PART | PART | PART | PART | NEVER | NEVER |

**NEARUSDT**

| family | 1m | 5m | 15m | 30m | 1h | 4h | 12h |
|---|---|---|---|---|---|---|---|
| FAST | FULL | FULL | FULL | FULL | FULL | FULL | PART |
| M | FULL | FULL | FULL | FULL | PART | PART | PART |
| MH | FULL | FULL | FULL | PART | PART | PART | PART |
| H | FULL | FULL | PART | PART | PART | PART | NEVER |
| VH | FULL | PART | PART | PART | PART | OPS | NEVER |
| UH | FULL | PART | PART | PART | PART | NEVER | NEVER |

**ZECUSDT**

| family | 1m | 5m | 15m | 30m | 1h | 4h | 12h |
|---|---|---|---|---|---|---|---|
| FAST | FULL | FULL | FULL | FULL | FULL | FULL | PART |
| M | FULL | FULL | FULL | FULL | FULL | PART | PART |
| MH | FULL | FULL | FULL | PART | PART | PART | PART |
| H | FULL | FULL | PART | PART | PART | PART | OPS |
| VH | FULL | PART | PART | PART | PART | OPS | NEVER |
| UH | FULL | PART | PART | PART | PART | NEVER | NEVER |

### NEVER cells — skipped, not computed

**45 of 630** (asset × tf × length) cells never warm at all. No EMA recursion is run for them; the column exists and is all-NaN so the schema stays uniform and nothing cold can be read.

| tf | family | lengths | assets |
|---|---|---|---|
| 12h | UH | 4236, 4618, 5000 | BTC, ETH, NEAR, SOL, ZEC |
| 12h | VH | 1618, 2618, 3618 | BTC, ETH, NEAR, SOL, ZEC |
| 4h | UH | 4236, 4618, 5000 | BTC, ETH, NEAR, SOL, ZEC |
| 12h | H | 1272 | NEAR, SOL |

### OPS-ONLY cells — computed, zero evidence-era coverage

**14 cells.** These warm, but only *after* the evidence ceiling (2024-07-01). They exist for the live era and cannot speak to the census.

| tf | family | lengths | assets |
|---|---|---|---|
| 12h | H | 889, 1272 | BTC, ETH, NEAR, SOL, ZEC |
| 4h | UH | 4236 | BTC, ETH |
| 4h | VH | 2618, 3618 | BTC, ETH, NEAR, SOL, ZEC |

### The feasibility matrix, verbatim — all 630 cells

The contract's five columns are all here. Two of them are pure functions of a single
factor and are factored out once rather than repeated 630 times, which is what keeps
this document inside the 1 % bus budget without dropping a cell:

- **`warm_bars`** depends only on `N` — `ceil(3.46·N)`, the 18 values below.
- **`bars available`** depends only on (asset, tf) — the 35 values below.

Per-cell, the remaining content is **warm-from date · evidence-era coverage · verdict**.

**`warm_bars = ceil(3.46·N)`**

```
FAST  N=9: 32   N=12: 42   N=26: 90
M     N=62: 215   N=89: 308   N=127: 440
MH    N=262: 907   N=316: 1,094   N=423: 1,464
H     N=616: 2,132   N=889: 3,076   N=1272: 4,402
VH    N=1618: 5,599   N=2618: 9,059   N=3618: 12,519
UH    N=4236: 14,657   N=4618: 15,979   N=5000: 17,300
```

**`bars available` (full history, both eras)**

| asset | 1m | 5m | 15m | 30m | 1h | 4h | 12h | first bar | last bar |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| BTCUSDT | 3,645,602 | 729,121 | 243,041 | 121,521 | 60,761 | 15,190 | 5,063 | 2019-09-08 | 2026-08-13 |
| ETHUSDT | 3,531,016 | 706,203 | 235,401 | 117,701 | 58,851 | 14,713 | 4,904 | 2019-11-27 | 2026-08-13 |
| SOLUSDT | 3,110,581 | 622,116 | 207,372 | 103,686 | 51,843 | 12,961 | 4,320 | 2020-09-14 | 2026-08-13 |
| NEARUSDT | 3,065,881 | 613,176 | 204,392 | 102,196 | 51,098 | 12,774 | 4,258 | 2020-10-15 | 2026-08-13 |
| ZECUSDT | 3,430,200 | 686,040 | 228,680 | 114,340 | 57,170 | 14,292 | 4,764 | 2020-02-05 | 2026-08-13 |

**Per cell — `N: warm-from  coverage  verdict`** — `F`=FULL · `P`=PARTIAL(evidence) · `O`=OPS-ONLY · `N`=NEVER

```
BTCUSDT @ 1m  (3,645,602 bars)
  FAST 9:19-09-08 1.000 F  12:19-09-08 1.000 F  26:19-09-08 1.000 F
  M    62:19-09-08 1.000 F  89:19-09-08 1.000 F  127:19-09-09 1.000 F
  MH   262:19-09-09 1.000 F  316:19-09-09 1.000 F  423:19-09-09 1.000 F
  H    616:19-09-10 1.000 F  889:19-09-10 1.000 F  1272:19-09-11 1.000 F
  VH   1618:19-09-12 1.000 F  2618:19-09-15 1.000 F  3618:19-09-17 1.000 F
  UH   4236:19-09-18 1.000 F  4618:19-09-19 1.000 F  5000:19-09-20 1.000 F
BTCUSDT @ 5m  (729,121 bars)
  FAST 9:19-09-08 1.000 F  12:19-09-08 1.000 F  26:19-09-09 1.000 F
  M    62:19-09-09 1.000 F  89:19-09-09 1.000 F  127:19-09-10 1.000 F
  MH   262:19-09-11 1.000 F  316:19-09-12 1.000 F  423:19-09-13 1.000 F
  H    616:19-09-16 1.000 F  889:19-09-19 1.000 F  1272:19-09-24 1.000 F
  VH   1618:19-09-28 1.000 F  2618:19-10-10 0.995 P  3618:19-10-22 0.988 P
  UH   4236:19-10-29 0.984 P  4618:19-11-03 0.981 P  5000:19-11-07 0.978 P
BTCUSDT @ 15m  (243,041 bars)
  FAST 9:19-09-09 1.000 F  12:19-09-09 1.000 F  26:19-09-09 1.000 F
  M    62:19-09-10 1.000 F  89:19-09-11 1.000 F  127:19-09-13 1.000 F
  MH   262:19-09-18 1.000 F  316:19-09-20 1.000 F  423:19-09-23 1.000 F
  H    616:19-09-30 1.000 F  889:19-10-10 0.994 P  1272:19-10-24 0.986 P
  VH   1618:19-11-06 0.979 P  2618:19-12-12 0.958 P  3618:20-01-17 0.938 P
  UH   4236:20-02-08 0.925 P  4618:20-02-22 0.917 P  5000:20-03-06 0.909 P
BTCUSDT @ 30m  (121,521 bars)
  FAST 9:19-09-09 1.000 F  12:19-09-09 1.000 F  26:19-09-10 1.000 F
  M    62:19-09-13 1.000 F  89:19-09-15 1.000 F  127:19-09-17 1.000 F
  MH   262:19-09-27 1.000 F  316:19-10-01 1.000 P  423:19-10-09 0.995 P
  H    616:19-10-23 0.987 P  889:19-11-11 0.976 P  1272:19-12-09 0.960 P
  VH   1618:20-01-03 0.946 P  2618:20-03-15 0.904 P  3618:20-05-26 0.863 P
  UH   4236:20-07-10 0.837 P  4618:20-08-06 0.821 P  5000:20-09-03 0.805 P
BTCUSDT @ 1h  (60,761 bars)
  FAST 9:19-09-10 1.000 F  12:19-09-10 1.000 F  26:19-09-12 1.000 F
  M    62:19-09-17 1.000 F  89:19-09-21 1.000 F  127:19-09-27 1.000 F
  MH   262:19-10-16 0.991 P  316:19-10-24 0.987 P  423:19-11-08 0.978 P
  H    616:19-12-06 0.962 P  889:20-01-14 0.939 P  1272:20-03-10 0.907 P
  VH   1618:20-04-29 0.878 P  2618:20-09-20 0.795 P  3618:21-02-11 0.712 P
  UH   4236:21-05-11 0.661 P  4618:21-07-05 0.629 P  5000:21-08-29 0.597 P
BTCUSDT @ 4h  (15,190 bars)
  FAST 9:19-09-14 1.000 F  12:19-09-15 1.000 F  26:19-09-23 1.000 F
  M    62:19-10-14 0.992 P  89:19-10-30 0.983 P  127:19-11-21 0.971 P
  MH   262:20-02-06 0.926 P  316:20-03-09 0.908 P  423:20-05-09 0.872 P
  H    616:20-08-29 0.808 P  889:21-02-02 0.717 P  1272:21-09-11 0.590 P
  VH   1618:22-03-29 0.475 P  2618:23-10-27 0.143 P  3618:25-05-26 0.000 O
  UH   4236:26-05-17 0.000 O  4618:-------- 0.000 N  5000:-------- 0.000 N
BTCUSDT @ 12h  (5,063 bars)
  FAST 9:19-09-24 1.000 F  12:19-09-29 1.000 F  26:19-10-23 0.987 P
  M    62:19-12-25 0.951 P  89:20-02-09 0.924 P  127:20-04-15 0.886 P
  MH   262:20-12-05 0.752 P  316:21-03-08 0.698 P  423:21-09-09 0.591 P
  H    616:22-08-09 0.399 P  889:23-11-24 0.127 P  1272:25-09-17 0.000 O
  VH   1618:-------- 0.000 N  2618:-------- 0.000 N  3618:-------- 0.000 N
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
ETHUSDT @ 1m  (3,531,016 bars)
  FAST 9:19-11-27 1.000 F  12:19-11-27 1.000 F  26:19-11-27 1.000 F
  M    62:19-11-27 1.000 F  89:19-11-27 1.000 F  127:19-11-27 1.000 F
  MH   262:19-11-27 1.000 F  316:19-11-28 1.000 F  423:19-11-28 1.000 F
  H    616:19-11-28 1.000 F  889:19-11-29 1.000 F  1272:19-11-30 1.000 F
  VH   1618:19-12-01 1.000 F  2618:19-12-03 1.000 F  3618:19-12-06 1.000 F
  UH   4236:19-12-07 1.000 F  4618:19-12-08 1.000 F  5000:19-12-09 1.000 F
ETHUSDT @ 5m  (706,203 bars)
  FAST 9:19-11-27 1.000 F  12:19-11-27 1.000 F  26:19-11-27 1.000 F
  M    62:19-11-28 1.000 F  89:19-11-28 1.000 F  127:19-11-28 1.000 F
  MH   262:19-11-30 1.000 F  316:19-12-01 1.000 F  423:19-12-02 1.000 F
  H    616:19-12-04 1.000 F  889:19-12-08 1.000 F  1272:19-12-12 1.000 F
  VH   1618:19-12-16 1.000 F  2618:19-12-28 1.000 F  3618:20-01-09 0.995 P
  UH   4236:20-01-17 0.990 P  4618:20-01-21 0.987 P  5000:20-01-26 0.985 P
ETHUSDT @ 15m  (235,401 bars)
  FAST 9:19-11-27 1.000 F  12:19-11-27 1.000 F  26:19-11-28 1.000 F
  M    62:19-11-29 1.000 F  89:19-11-30 1.000 F  127:19-12-01 1.000 F
  MH   262:19-12-06 1.000 F  316:19-12-08 1.000 F  423:19-12-12 1.000 F
  H    616:19-12-19 1.000 F  889:19-12-29 1.000 F  1272:20-01-12 0.993 P
  VH   1618:20-01-24 0.986 P  2618:20-02-29 0.964 P  3618:20-04-05 0.942 P
  UH   4236:20-04-28 0.928 P  4618:20-05-11 0.920 P  5000:20-05-25 0.911 P
ETHUSDT @ 30m  (117,701 bars)
  FAST 9:19-11-27 1.000 F  12:19-11-28 1.000 F  26:19-11-29 1.000 F
  M    62:19-12-01 1.000 F  89:19-12-03 1.000 F  127:19-12-06 1.000 F
  MH   262:19-12-16 1.000 F  316:19-12-20 1.000 F  423:19-12-27 1.000 F
  H    616:20-01-10 0.994 P  889:20-01-30 0.982 P  1272:20-02-27 0.965 P
  VH   1618:20-03-22 0.950 P  2618:20-06-03 0.906 P  3618:20-08-14 0.862 P
  UH   4236:20-09-27 0.835 P  4618:20-10-25 0.819 P  5000:20-11-21 0.802 P
ETHUSDT @ 1h  (58,851 bars)
  FAST 9:19-11-28 1.000 F  12:19-11-29 1.000 F  26:19-12-01 1.000 F
  M    62:19-12-06 1.000 F  89:19-12-10 1.000 F  127:19-12-15 1.000 F
  MH   262:20-01-04 0.998 P  316:20-01-11 0.993 P  423:20-01-27 0.984 P
  H    616:20-02-24 0.967 P  889:20-04-03 0.943 P  1272:20-05-28 0.909 P
  VH   1618:20-07-17 0.879 P  2618:20-12-08 0.791 P  3618:21-05-01 0.704 P
  UH   4236:21-07-30 0.649 P  4618:21-09-23 0.616 P  5000:21-11-17 0.582 P
ETHUSDT @ 4h  (14,713 bars)
  FAST 9:19-12-02 1.000 F  12:19-12-04 1.000 F  26:19-12-12 1.000 F
  M    62:20-01-02 0.999 P  89:20-01-17 0.990 P  127:20-02-08 0.977 P
  MH   262:20-04-26 0.929 P  316:20-05-27 0.910 P  423:20-07-28 0.873 P
  H    616:20-11-16 0.805 P  889:21-04-22 0.709 P  1272:21-11-29 0.575 P
  VH   1618:22-06-17 0.453 P  2618:24-01-15 0.102 P  3618:25-08-13 0.000 O
  UH   4236:26-08-05 0.000 O  4618:-------- 0.000 N  5000:-------- 0.000 N
ETHUSDT @ 12h  (4,904 bars)
  FAST 9:19-12-13 1.000 F  12:19-12-18 1.000 F  26:20-01-11 0.994 P
  M    62:20-03-13 0.956 P  89:20-04-29 0.928 P  127:20-07-04 0.887 P
  MH   262:21-02-22 0.745 P  316:21-05-27 0.688 P  423:21-11-28 0.576 P
  H    616:22-10-28 0.372 P  889:24-02-12 0.085 P  1272:25-12-06 0.000 O
  VH   1618:-------- 0.000 N  2618:-------- 0.000 N  3618:-------- 0.000 N
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
SOLUSDT @ 1m  (3,110,581 bars)
  FAST 9:20-09-14 1.000 F  12:20-09-14 1.000 F  26:20-09-14 1.000 F
  M    62:20-09-14 1.000 F  89:20-09-14 1.000 F  127:20-09-14 1.000 F
  MH   262:20-09-14 1.000 F  316:20-09-15 1.000 F  423:20-09-15 1.000 F
  H    616:20-09-15 1.000 F  889:20-09-16 1.000 F  1272:20-09-17 1.000 F
  VH   1618:20-09-18 1.000 F  2618:20-09-20 1.000 F  3618:20-09-22 1.000 F
  UH   4236:20-09-24 1.000 F  4618:20-09-25 1.000 F  5000:20-09-26 1.000 F
SOLUSDT @ 5m  (622,116 bars)
  FAST 9:20-09-14 1.000 F  12:20-09-14 1.000 F  26:20-09-14 1.000 F
  M    62:20-09-15 1.000 F  89:20-09-15 1.000 F  127:20-09-15 1.000 F
  MH   262:20-09-17 1.000 F  316:20-09-18 1.000 F  423:20-09-19 1.000 F
  H    616:20-09-21 1.000 F  889:20-09-24 1.000 F  1272:20-09-29 1.000 F
  VH   1618:20-10-03 0.998 P  2618:20-10-15 0.989 P  3618:20-10-27 0.981 P
  UH   4236:20-11-04 0.975 P  4618:20-11-08 0.972 P  5000:20-11-13 0.968 P
SOLUSDT @ 15m  (207,372 bars)
  FAST 9:20-09-14 1.000 F  12:20-09-14 1.000 F  26:20-09-15 1.000 F
  M    62:20-09-16 1.000 F  89:20-09-17 1.000 F  127:20-09-18 1.000 F
  MH   262:20-09-23 1.000 F  316:20-09-25 1.000 F  423:20-09-29 1.000 F
  H    616:20-10-06 0.996 P  889:20-10-16 0.989 P  1272:20-10-30 0.979 P
  VH   1618:20-11-11 0.970 P  2618:20-12-17 0.943 P  3618:21-01-22 0.917 P
  UH   4236:21-02-13 0.901 P  4618:21-02-27 0.891 P  5000:21-03-13 0.881 P
SOLUSDT @ 30m  (103,686 bars)
  FAST 9:20-09-14 1.000 F  12:20-09-15 1.000 F  26:20-09-16 1.000 F
  M    62:20-09-18 1.000 F  89:20-09-20 1.000 F  127:20-09-23 1.000 F
  MH   262:20-10-03 0.998 P  316:20-10-07 0.996 P  423:20-10-14 0.990 P
  H    616:20-10-28 0.980 P  889:20-11-17 0.965 P  1272:20-12-15 0.945 P
  VH   1618:21-01-08 0.927 P  2618:21-03-22 0.874 P  3618:21-06-02 0.822 P
  UH   4236:21-07-16 0.789 P  4618:21-08-13 0.769 P  5000:21-09-09 0.749 P
SOLUSDT @ 1h  (51,843 bars)
  FAST 9:20-09-15 1.000 F  12:20-09-16 1.000 F  26:20-09-18 1.000 F
  M    62:20-09-23 1.000 F  89:20-09-27 1.000 F  127:20-10-02 0.999 P
  MH   262:20-10-22 0.985 P  316:20-10-29 0.979 P  423:20-11-14 0.968 P
  H    616:20-12-12 0.947 P  889:21-01-20 0.919 P  1272:21-03-16 0.878 P
  VH   1618:21-05-05 0.842 P  2618:21-09-26 0.737 P  3618:22-02-17 0.631 P
  UH   4236:22-05-18 0.566 P  4618:22-07-12 0.526 P  5000:22-09-05 0.486 P
SOLUSDT @ 4h  (12,961 bars)
  FAST 9:20-09-19 1.000 F  12:20-09-21 1.000 F  26:20-09-29 1.000 F
  M    62:20-10-20 0.986 P  89:20-11-04 0.975 P  127:20-11-26 0.959 P
  MH   262:21-02-12 0.902 P  316:21-03-15 0.879 P  423:21-05-16 0.834 P
  H    616:21-09-04 0.753 P  889:22-02-08 0.638 P  1272:22-09-17 0.476 P
  VH   1618:23-04-05 0.331 P  2618:24-11-02 0.000 O  3618:26-06-01 0.000 O
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
SOLUSDT @ 12h  (4,320 bars)
  FAST 9:20-09-30 1.000 F  12:20-10-05 0.997 P  26:20-10-29 0.980 P
  M    62:20-12-30 0.934 P  89:21-02-15 0.900 P  127:21-04-22 0.852 P
  MH   262:21-12-11 0.681 P  316:22-03-15 0.613 P  423:22-09-16 0.478 P
  H    616:23-08-16 0.234 P  889:24-11-30 0.000 O  1272:-------- 0.000 N
  VH   1618:-------- 0.000 N  2618:-------- 0.000 N  3618:-------- 0.000 N
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
NEARUSDT @ 1m  (3,065,881 bars)
  FAST 9:20-10-15 1.000 F  12:20-10-15 1.000 F  26:20-10-15 1.000 F
  M    62:20-10-15 1.000 F  89:20-10-15 1.000 F  127:20-10-15 1.000 F
  MH   262:20-10-15 1.000 F  316:20-10-16 1.000 F  423:20-10-16 1.000 F
  H    616:20-10-16 1.000 F  889:20-10-17 1.000 F  1272:20-10-18 1.000 F
  VH   1618:20-10-19 1.000 F  2618:20-10-21 1.000 F  3618:20-10-24 1.000 F
  UH   4236:20-10-25 1.000 F  4618:20-10-26 1.000 F  5000:20-10-27 1.000 F
NEARUSDT @ 5m  (613,176 bars)
  FAST 9:20-10-15 1.000 F  12:20-10-15 1.000 F  26:20-10-15 1.000 F
  M    62:20-10-16 1.000 F  89:20-10-16 1.000 F  127:20-10-16 1.000 F
  MH   262:20-10-18 1.000 F  316:20-10-19 1.000 F  423:20-10-20 1.000 F
  H    616:20-10-22 1.000 F  889:20-10-26 1.000 F  1272:20-10-30 1.000 F
  VH   1618:20-11-03 0.998 P  2618:20-11-15 0.989 P  3618:20-11-27 0.980 P
  UH   4236:20-12-05 0.974 P  4618:20-12-09 0.971 P  5000:20-12-14 0.968 P
NEARUSDT @ 15m  (204,392 bars)
  FAST 9:20-10-15 1.000 F  12:20-10-15 1.000 F  26:20-10-16 1.000 F
  M    62:20-10-17 1.000 F  89:20-10-18 1.000 F  127:20-10-19 1.000 F
  MH   262:20-10-24 1.000 F  316:20-10-26 1.000 F  423:20-10-30 1.000 F
  H    616:20-11-06 0.996 P  889:20-11-16 0.989 P  1272:20-11-30 0.978 P
  VH   1618:20-12-12 0.969 P  2618:21-01-17 0.942 P  3618:21-02-22 0.915 P
  UH   4236:21-03-17 0.898 P  4618:21-03-30 0.888 P  5000:21-04-13 0.878 P
NEARUSDT @ 30m  (102,196 bars)
  FAST 9:20-10-16 1.000 F  12:20-10-16 1.000 F  26:20-10-17 1.000 F
  M    62:20-10-19 1.000 F  89:20-10-21 1.000 F  127:20-10-24 1.000 F
  MH   262:20-11-03 0.998 P  316:20-11-07 0.995 P  423:20-11-14 0.990 P
  H    616:20-11-28 0.979 P  889:20-12-18 0.965 P  1272:21-01-15 0.944 P
  VH   1618:21-02-08 0.925 P  2618:21-04-22 0.871 P  3618:21-07-03 0.818 P
  UH   4236:21-08-16 0.784 P  4618:21-09-13 0.764 P  5000:21-10-10 0.743 P
NEARUSDT @ 1h  (51,098 bars)
  FAST 9:20-10-16 1.000 F  12:20-10-17 1.000 F  26:20-10-19 1.000 F
  M    62:20-10-24 1.000 F  89:20-10-28 1.000 F  127:20-11-02 0.999 P
  MH   262:20-11-22 0.984 P  316:20-11-29 0.978 P  423:20-12-15 0.967 P
  H    616:21-01-12 0.946 P  889:21-02-20 0.917 P  1272:21-04-16 0.875 P
  VH   1618:21-06-05 0.838 P  2618:21-10-27 0.730 P  3618:22-03-20 0.623 P
  UH   4236:22-06-18 0.556 P  4618:22-08-12 0.515 P  5000:22-10-06 0.474 P
NEARUSDT @ 4h  (12,774 bars)
  FAST 9:20-10-20 1.000 F  12:20-10-22 1.000 F  26:20-10-30 1.000 F
  M    62:20-11-20 0.986 P  89:20-12-05 0.974 P  127:20-12-27 0.958 P
  MH   262:21-03-15 0.899 P  316:21-04-15 0.876 P  423:21-06-16 0.830 P
  H    616:21-10-05 0.747 P  889:22-03-12 0.629 P  1272:22-10-19 0.464 P
  VH   1618:23-05-06 0.315 P  2618:24-12-03 0.000 O  3618:26-07-02 0.000 O
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
NEARUSDT @ 12h  (4,258 bars)
  FAST 9:20-10-31 1.000 F  12:20-11-05 0.997 P  26:20-11-29 0.979 P
  M    62:21-01-30 0.932 P  89:21-03-18 0.898 P  127:21-05-23 0.848 P
  MH   262:22-01-11 0.674 P  316:22-04-15 0.604 P  423:22-10-17 0.466 P
  H    616:23-09-16 0.216 P  889:24-12-31 0.000 O  1272:-------- 0.000 N
  VH   1618:-------- 0.000 N  2618:-------- 0.000 N  3618:-------- 0.000 N
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
ZECUSDT @ 1m  (3,430,200 bars)
  FAST 9:20-02-05 1.000 F  12:20-02-05 1.000 F  26:20-02-05 1.000 F
  M    62:20-02-05 1.000 F  89:20-02-05 1.000 F  127:20-02-05 1.000 F
  MH   262:20-02-05 1.000 F  316:20-02-06 1.000 F  423:20-02-06 1.000 F
  H    616:20-02-06 1.000 F  889:20-02-07 1.000 F  1272:20-02-08 1.000 F
  VH   1618:20-02-09 1.000 F  2618:20-02-11 1.000 F  3618:20-02-14 1.000 F
  UH   4236:20-02-15 1.000 F  4618:20-02-16 1.000 F  5000:20-02-17 1.000 F
ZECUSDT @ 5m  (686,040 bars)
  FAST 9:20-02-05 1.000 F  12:20-02-05 1.000 F  26:20-02-05 1.000 F
  M    62:20-02-06 1.000 F  89:20-02-06 1.000 F  127:20-02-06 1.000 F
  MH   262:20-02-08 1.000 F  316:20-02-09 1.000 F  423:20-02-10 1.000 F
  H    616:20-02-12 1.000 F  889:20-02-16 1.000 F  1272:20-02-20 1.000 F
  VH   1618:20-02-24 1.000 F  2618:20-03-07 0.996 P  3618:20-03-19 0.988 P
  UH   4236:20-03-27 0.983 P  4618:20-03-31 0.981 P  5000:20-04-05 0.978 P
ZECUSDT @ 15m  (228,680 bars)
  FAST 9:20-02-05 1.000 F  12:20-02-05 1.000 F  26:20-02-06 1.000 F
  M    62:20-02-07 1.000 F  89:20-02-08 1.000 F  127:20-02-09 1.000 F
  MH   262:20-02-14 1.000 F  316:20-02-16 1.000 F  423:20-02-20 1.000 F
  H    616:20-02-27 1.000 F  889:20-03-08 0.995 P  1272:20-03-22 0.987 P
  VH   1618:20-04-03 0.979 P  2618:20-05-09 0.956 P  3618:20-06-14 0.933 P
  UH   4236:20-07-07 0.919 P  4618:20-07-20 0.910 P  5000:20-08-03 0.902 P
ZECUSDT @ 30m  (114,340 bars)
  FAST 9:20-02-06 1.000 F  12:20-02-06 1.000 F  26:20-02-07 1.000 F
  M    62:20-02-09 1.000 F  89:20-02-11 1.000 F  127:20-02-14 1.000 F
  MH   262:20-02-24 1.000 F  316:20-02-28 1.000 F  423:20-03-06 0.996 P
  H    616:20-03-20 0.988 P  889:20-04-09 0.975 P  1272:20-05-07 0.958 P
  VH   1618:20-05-31 0.942 P  2618:20-08-12 0.896 P  3618:20-10-23 0.851 P
  UH   4236:20-12-06 0.823 P  4618:21-01-03 0.805 P  5000:21-01-30 0.788 P
ZECUSDT @ 1h  (57,170 bars)
  FAST 9:20-02-06 1.000 F  12:20-02-07 1.000 F  26:20-02-09 1.000 F
  M    62:20-02-14 1.000 F  89:20-02-18 1.000 F  127:20-02-23 1.000 F
  MH   262:20-03-14 0.992 P  316:20-03-21 0.987 P  423:20-04-06 0.977 P
  H    616:20-05-04 0.960 P  889:20-06-12 0.935 P  1272:20-08-06 0.900 P
  VH   1618:20-09-25 0.868 P  2618:21-02-16 0.777 P  3618:21-07-10 0.686 P
  UH   4236:21-10-08 0.630 P  4618:21-12-02 0.595 P  5000:22-01-26 0.560 P
ZECUSDT @ 4h  (14,292 bars)
  FAST 9:20-02-10 1.000 F  12:20-02-12 1.000 F  26:20-02-20 1.000 F
  M    62:20-03-12 0.993 P  89:20-03-27 0.983 P  127:20-04-18 0.969 P
  MH   262:20-07-05 0.920 P  316:20-08-05 0.900 P  423:20-10-06 0.861 P
  H    616:21-01-25 0.791 P  889:21-07-02 0.692 P  1272:22-02-08 0.552 P
  VH   1618:22-08-26 0.426 P  2618:24-03-25 0.062 P  3618:25-10-22 0.000 O
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
ZECUSDT @ 12h  (4,764 bars)
  FAST 9:20-02-21 1.000 F  12:20-02-26 1.000 F  26:20-03-21 0.987 P
  M    62:20-05-22 0.948 P  89:20-07-08 0.918 P  127:20-09-12 0.877 P
  MH   262:21-05-03 0.729 P  316:21-08-05 0.670 P  423:22-02-06 0.553 P
  H    616:23-01-06 0.342 P  889:24-04-22 0.044 P  1272:26-02-14 0.000 O
  VH   1618:-------- 0.000 N  2618:-------- 0.000 N  3618:-------- 0.000 N
  UH   4236:-------- 0.000 N  4618:-------- 0.000 N  5000:-------- 0.000 N
```

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

### 1m — THE SKIP, NAMED

**1m was computed for Stage 1 and skipped for Stages 2–4, on budget, and the budget was RAM.**

The contract makes 1m the last thing to run and explicitly skippable *with the skip named*.
This is the naming. The matrix says 1m is `FULL` for all 18 lengths on all 5 assets — it is the
one timeframe on which even UH(5000) is fully warm inside the evidence era — so this is a real
loss and not a cell that had nothing in it.

The measurement that forced it: this machine carries **7.6 GB of RAM with ~0.8 GB free**. A 1m
cell is 3.65 M bars; Stage 2 alone held ~400 MB per asset and ran at **57 % CPU efficiency**
(479 CPU-seconds against 14 minutes of wall clock) — paging, not computing — without finishing
its first asset. Stage 3 assembles 57 columns × 3.65 M rows ≈ **1.2 GB peak per asset**, which
does not fit in what is free. Extrapolated cost was ~2 hours with a likely `MemoryError` in
Stage 3.

**What that costs, precisely:** 5 cells of the 35 (`1m` × 5 assets) have no `emas/`, `ribbons/`
or `crosses/` artifact. Stages 3–5 never read 1m, so **no table in this document is affected**;
§6 ran on 5m/15m/30m/1h throughout. The 1m rows of the feasibility matrix are present and
complete.

**To land it later**, on a machine with headroom or after making Stage 3 write per-family
instead of assembling all 57 columns at once:

```
python scripts/census2b_program.py --stage 2,3,4 --tfs 1m
```

The I12 merge added to the matrix in this build means that run will *add* its 90 cells rather
than overwrite the other 540.

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
+ **price↔band** per ribbon (`enter` / `exit` / `reject-at-band`), **plus `traverse`** —
see the taxonomy note below.

`reject-at-band` uses the **ratified kiss grammar carried from census-2A** — approach within
`0.25·ATR`, veer `≥ 0.75·ATR` within `10` bars, break on the first genuine sign change — applied
with `series = close` and `level =` each band rail. The function is *restated* rather than
imported so `census2a_program.py` is never executed as a side effect; **F-B5c proves the copy is
element-for-element equal to the original**.

**F-KEY declared key:** `(asset, tf, pair_class, pair, event, dir, ts_ms)`, asserted at write
time for every cell. `dup = 0` on all 35 cells.

```
asset     tf         events     within   midline       band    secs      MB
----------------------------------------------------------------------------------------------------
BTCUSDT   5m        688,963    128,689    18,403    541,871     9.7    10.0
BTCUSDT   15m       221,036     42,362     5,787    172,887     3.8     4.0
BTCUSDT   30m       105,527     20,391     2,763     82,373     1.4     1.9
BTCUSDT   1h         50,454     10,051     1,281     39,122     0.9     0.9
BTCUSDT   4h         11,146      2,340       281      8,525     0.2     0.2
BTCUSDT   12h         3,289        713        87      2,489     0.1     0.1
ETHUSDT   5m        664,252    124,081    17,615    522,556     9.9     9.6
ETHUSDT   15m       213,073     40,121     5,585    167,367     3.1     3.8
ETHUSDT   30m       103,074     19,553     2,761     80,760     1.3     1.8
ETHUSDT   1h         48,801      9,687     1,278     37,836     0.4     0.8
ETHUSDT   4h         11,108      2,305       297      8,506     0.3     0.2
ETHUSDT   12h         3,218        703        78      2,437     0.2     0.1
SOLUSDT   5m        572,880    106,033    15,088    451,759     8.3     8.5
SOLUSDT   15m       184,996     34,334     4,818    145,844     2.7     3.3
SOLUSDT   30m        90,591     16,787     2,366     71,438     1.1     1.6
SOLUSDT   1h         43,626      8,224     1,165     34,237     0.6     0.8
SOLUSDT   4h         10,012      1,953       261      7,798     0.2     0.2
SOLUSDT   12h         2,936        639        81      2,216     0.1     0.1
NEARUSDT  5m        577,967    106,136    15,312    456,519     8.2     8.5
NEARUSDT  15m       187,894     35,119     4,937    147,838     2.6     3.3
NEARUSDT  30m        90,874     17,093     2,371     71,410     1.1     1.6
NEARUSDT  1h         43,533      8,368     1,131     34,034     0.6     0.8
NEARUSDT  4h          9,535      1,963       257      7,315     0.2     0.2
NEARUSDT  12h         2,770        619        66      2,085     0.2     0.1
ZECUSDT   5m        649,788    119,366    17,443    512,979     9.3     9.4
ZECUSDT   15m       214,150     39,450     5,456    169,244     3.5     3.8
ZECUSDT   30m       104,049     19,231     2,701     82,117     1.4     1.8
ZECUSDT   1h         50,372      9,307     1,301     39,764     0.7     0.9
ZECUSDT   4h         11,380      2,187       298      8,895     0.2     0.2
ZECUSDT   12h         3,396        711        94      2,591     0.1     0.1

====================================================================================================
```

_1m: skipped — see §3, “1m — the skip, named”._

### One class was added to the taxonomy, and it is not a small one

The contract's band grammar names `{enter, exit, reject-at-band}`. All three are defined against
`inside`: enter is *outside → inside*, exit is *inside → outside*. **A bar whose close moves from
below the band to above it in a single bar is none of them** — it never closes inside — so it
matched no rule and was emitted nowhere.

That is not a corner case on this panel. Measured directly off the `pos` column before any fix:

```
single-bar band traversals dropped : 510,584
enter + exit events emitted        : 2,262,743
traversals as a share of transitions : 18.411 %

worst cells
  BTCUSDT   5m   FAST   traverse= 50,932   enter+exit= 151,892
  ETHUSDT   5m   FAST   traverse= 48,983   enter+exit= 146,472
  ZECUSDT   5m   FAST   traverse= 47,300   enter+exit= 138,296
  NEARUSDT  5m   FAST   traverse= 42,027   enter+exit= 123,942
  SOLUSDT   5m   FAST   traverse= 40,899   enter+exit= 126,341
```

Nearly one band transition in five, concentrated in exactly the fast-ribbon cells where the band
is narrow relative to a bar — which is to say, where a band crossing carries the most meaning.
A first-look "price↔band" count built on the un-fixed taxonomy would have understated FAST band
activity by 18 % and said nothing about it.

`traverse` is therefore emitted as **its own event class**, `dir` ∈ {`up`, `down`}, rather than
folded into `exit`. Folding would have kept the contract's three names while quietly changing
what `exit` counts. **This is an addition to a taxonomy the contract called "pared by design",
and it is flagged here for the operator to veto by name.** Totals after the fix: FAST 363,810 ·
M 97,046 · MH 34,942 · H 8,133 · UH 4,549 · VH 2,104 — **510,584**, matching the pre-fix
measurement exactly.

### F-B5 — determinism, hand-verification, and grammar parity

**F-B5a — determinism.** `NEARUSDT 4h` re-run from the artifacts and re-hashed:
`stored=3288281ea7ce2f57  rerun=3288281ea7ce2f57  **IDENTICAL**`.

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

### 6(a) · EVENT-DENSITY MAP — where does each ribbon even move?

```
counts are of CLOSE-CONFIRMED events over the FULL available series (both eras),
over a fixed complete population; nothing is selected.

WITHIN-RIBBON crosses per 1,000 bars -- panel total, by family x tf
(a ribbon that never moves at a tf is where that tf stops being its home)

  family         5m       15m       30m        1h        4h       12h
----------------------------------------------------------------------------------------------------
  FAST       221.08    218.08    211.89    207.06    199.07    190.48
  M           33.06     31.57     31.13     31.90     27.75     26.02
  MH           8.38      8.59      8.27      7.54      6.81      5.73
  H            3.15      2.87      2.70      2.76      2.06      0.72
  VH           1.04      0.97      0.91      0.82      0.26         -
  UH           0.53      0.51      0.45      0.40         -         -

  (per-pair average: family total / 3 pairs / bars of the cell)

PER-DIRECTION SPLIT -- within-ribbon, panel total
  family            up         down   up share
----------------------------------------------------------------------------------------------------
  FAST         384,617      384,614     0.5000
  M             57,060       57,050     0.5000
  MH            14,685       14,683     0.5000
  H              5,283        5,296     0.4994
  VH             1,724        1,747     0.4967
  UH               867          890     0.4935

V-ULT DENSITY -- VH and UH within-ribbon crosses, per asset per tf
  asset     fam        5m      15m      30m       1h       4h      12h
----------------------------------------------------------------------------------------------------
  BTCUSDT   VH        512      153       62       29        4        -
  BTCUSDT   UH        236       65       37        9        -        -
  ETHUSDT   VH        446      146       56       29        5        -
  ETHUSDT   UH        236       74       29       27        -        -
  SOLUSDT   VH        433      123       63       26        1        -
  SOLUSDT   UH        227       71       27       12        -        -
  NEARUSDT  VH        415      137       67       20        1        -
  NEARUSDT  UH        207       67       24        8        -        -
  ZECUSDT   VH        463      150       84       45        1        -
  ZECUSDT   UH        245       92       48       16        -        -

MIDLINE + PRICE<->BAND totals, panel

  midline: 131,362 events
    12_89          cross_down       51,748
    12_89          cross_up       51,751
    2618_4618      cross_down          399
    2618_4618      cross_up          391
    316_889        cross_down        2,940
    316_889        cross_up        2,930
    889_2618       cross_down          964
    889_2618       cross_up          955
    89_316         cross_down        9,643
    89_316         cross_up        9,641

  price_band: 3,914,812 events
    FAST_band      enter         554,212
    FAST_band      exit          554,206
    FAST_band      traverse      363,810
    FAST_lower     reject        305,564
    FAST_upper     reject        308,173
    H_band         enter          90,433
    H_band         exit           90,431
    H_band         traverse        8,133
    H_lower        reject         35,118
    H_upper        reject         35,314
    MH_band        enter         137,722
    MH_band        exit          137,722
    MH_band        traverse       34,942
    MH_lower       reject         62,393
    MH_upper       reject         62,258
    M_band         enter         266,300
    M_band         exit          266,299
    M_band         traverse       97,046
    M_lower        reject        133,983
    M_upper        reject        134,974
    UH_band        enter          30,998
    UH_band        exit           30,998
    UH_band        traverse        4,549
    UH_lower       reject         12,725
    UH_upper       reject         12,610
    VH_band        enter          51,708
    VH_band        exit           51,714
    VH_band        traverse        2,104
    VH_lower       reject         19,309
    VH_upper       reject         19,064
```

### 6(b) · EQUIVALENCE TABLE — the “one chart, all horizons” card

```
The card the operator asked for.  An EMA's identity is a DURATION, not a
number: EMA(N) on tf T spans N*T of tape.  Two (N, tf) pairs with the same
product are the same object drawn on different axes.  `centre of mass` is
(N-1)/2 bars -- where the weight of the average actually sits.

  family      N        5m       15m       30m        1h        4h       12h   <- memory, in DAYS
----------------------------------------------------------------------------------------------------
  FAST        9     0.031     0.094     0.188     0.375     1.500     4.500
  FAST       12     0.042     0.125     0.250     0.500     2.000     6.000
  FAST       26     0.090     0.271     0.542     1.083     4.333    13.000
  M          62     0.215     0.646     1.292     2.583    10.333    31.000
  M          89     0.309     0.927     1.854     3.708    14.833    44.500
  M         127     0.441     1.323     2.646     5.292    21.167    63.500
  MH        262     0.910     2.729     5.458    10.917    43.667   131.000
  MH        316     1.097     3.292     6.583    13.167    52.667   158.000
  MH        423     1.469     4.406     8.812    17.625    70.500   211.500
  H         616     2.139     6.417    12.833    25.667   102.667   308.000
  H         889     3.087     9.260    18.521    37.042   148.167   444.500
  H        1272     4.417    13.250    26.500    53.000   212.000   636.000
  VH       1618     5.618    16.854    33.708    67.417   269.667   809.000
  VH       2618     9.090    27.271    54.542   109.083   436.333    1309.0
  VH       3618    12.562    37.688    75.375   150.750   603.000    1809.0
  UH       4236    14.708    44.125    88.250   176.500   706.000    2118.0
  UH       4618    16.035    48.104    96.208   192.417   769.667    2309.0
  UH       5000    17.361    52.083   104.167   208.333   833.333    2500.0

NEAREST HTF EQUIVALENT -- 'this line, drawn on a slower chart'
          N @ tf       memory        5m      15m      30m       1h       4h      12h
----------------------------------------------------------------------------------------------------
          9 @ 5m      0.03 d       9.0      3.0      1.5    0.750    0.188    0.062
         9 @ 15m      0.09 d      27.0      9.0      4.5      2.2    0.562    0.188
          9 @ 1h      0.38 d     108.0     36.0     18.0      9.0      2.2    0.750
         12 @ 5m      0.04 d      12.0      4.0      2.0      1.0    0.250    0.083
        12 @ 15m      0.12 d      36.0     12.0      6.0      3.0    0.750    0.250
         12 @ 1h      0.50 d     144.0     48.0     24.0     12.0      3.0      1.0
         26 @ 5m      0.09 d      26.0      8.7      4.3      2.2    0.542    0.181
        26 @ 15m      0.27 d      78.0     26.0     13.0      6.5      1.6    0.542
         26 @ 1h      1.08 d     312.0    104.0     52.0     26.0      6.5      2.2
         62 @ 5m      0.22 d      62.0     20.7     10.3      5.2      1.3    0.431
        62 @ 15m      0.65 d     186.0     62.0     31.0     15.5      3.9      1.3
         62 @ 1h      2.58 d     744.0    248.0    124.0     62.0     15.5      5.2
         89 @ 5m      0.31 d      89.0     29.7     14.8      7.4      1.9    0.618
        89 @ 15m      0.93 d     267.0     89.0     44.5     22.2      5.6      1.9
         89 @ 1h      3.71 d    1068.0    356.0    178.0     89.0     22.2      7.4
        127 @ 5m      0.44 d     127.0     42.3     21.2     10.6      2.6    0.882
       127 @ 15m      1.32 d     381.0    127.0     63.5     31.8      7.9      2.6
        127 @ 1h      5.29 d    1524.0    508.0    254.0    127.0     31.8     10.6
        262 @ 5m      0.91 d     262.0     87.3     43.7     21.8      5.5      1.8
       262 @ 15m      2.73 d     786.0    262.0    131.0     65.5     16.4      5.5
        262 @ 1h     10.92 d    3144.0   1048.0    524.0    262.0     65.5     21.8
        316 @ 5m      1.10 d     316.0    105.3     52.7     26.3      6.6      2.2
       316 @ 15m      3.29 d     948.0    316.0    158.0     79.0     19.8      6.6
        316 @ 1h     13.17 d    3792.0   1264.0    632.0    316.0     79.0     26.3
        423 @ 5m      1.47 d     423.0    141.0     70.5     35.2      8.8      2.9
       423 @ 15m      4.41 d    1269.0    423.0    211.5    105.8     26.4      8.8
        423 @ 1h     17.62 d    5076.0   1692.0    846.0    423.0    105.8     35.2
        616 @ 5m      2.14 d     616.0    205.3    102.7     51.3     12.8      4.3
       616 @ 15m      6.42 d    1848.0    616.0    308.0    154.0     38.5     12.8
        616 @ 1h     25.67 d    7392.0   2464.0   1232.0    616.0    154.0     51.3
        889 @ 5m      3.09 d     889.0    296.3    148.2     74.1     18.5      6.2
       889 @ 15m      9.26 d    2667.0    889.0    444.5    222.2     55.6     18.5
        889 @ 1h     37.04 d   10668.0   3556.0   1778.0    889.0    222.2     74.1
       1272 @ 5m      4.42 d    1272.0    424.0    212.0    106.0     26.5      8.8
      1272 @ 15m     13.25 d    3816.0   1272.0    636.0    318.0     79.5     26.5
       1272 @ 1h     53.00 d   15264.0   5088.0   2544.0   1272.0    318.0    106.0
       1618 @ 5m      5.62 d    1618.0    539.3    269.7    134.8     33.7     11.2
      1618 @ 15m     16.85 d    4854.0   1618.0    809.0    404.5    101.1     33.7
       1618 @ 1h     67.42 d   19416.0   6472.0   3236.0   1618.0    404.5    134.8
       2618 @ 5m      9.09 d    2618.0    872.7    436.3    218.2     54.5     18.2
      2618 @ 15m     27.27 d    7854.0   2618.0   1309.0    654.5    163.6     54.5
       2618 @ 1h    109.08 d   31416.0  10472.0   5236.0   2618.0    654.5    218.2
       3618 @ 5m     12.56 d    3618.0   1206.0    603.0    301.5     75.4     25.1
      3618 @ 15m     37.69 d   10854.0   3618.0   1809.0    904.5    226.1     75.4
       3618 @ 1h    150.75 d   43416.0  14472.0   7236.0   3618.0    904.5    301.5
       4236 @ 5m     14.71 d    4236.0   1412.0    706.0    353.0     88.2     29.4
      4236 @ 15m     44.12 d   12708.0   4236.0   2118.0   1059.0    264.8     88.2
       4236 @ 1h    176.50 d   50832.0  16944.0   8472.0   4236.0   1059.0    353.0
       4618 @ 5m     16.03 d    4618.0   1539.3    769.7    384.8     96.2     32.1
      4618 @ 15m     48.10 d   13854.0   4618.0   2309.0   1154.5    288.6     96.2
       4618 @ 1h    192.42 d   55416.0  18472.0   9236.0   4618.0   1154.5    384.8
       5000 @ 5m     17.36 d    5000.0   1666.7    833.3    416.7    104.2     34.7
      5000 @ 15m     52.08 d   15000.0   5000.0   2500.0   1250.0    312.5    104.2
       5000 @ 1h    208.33 d   60000.0  20000.0  10000.0   5000.0   1250.0    416.7

F-B6  arithmetic check -- equivalence must conserve the span exactly
      324 equivalences checked, span mismatches = 0
      EMA5000 @ 5m = 5000*300000ms = 1,500,000,000ms = EMA104.2 @ 4h   OK
      EMA2618 @ 15m = 2618*900000ms = 2,356,200,000ms = EMA54.54 @ 12h   OK
      F-B6 PASS

WARM-UP COST -- days of tape consumed before the line is readable
  family      N        5m       15m       30m        1h        4h       12h
----------------------------------------------------------------------------------------------------
  FAST        9      0.11      0.33      0.67      1.33      5.33     16.00
  FAST       12      0.15      0.44      0.88      1.75      7.00     21.00
  FAST       26      0.31      0.94      1.88      3.75     15.00     45.00
  M          62      0.75      2.24      4.48      8.96     35.83    107.50
  M          89      1.07      3.21      6.42     12.83     51.33    154.00
  M         127      1.53      4.58      9.17     18.33     73.33    220.00
  MH        262      3.15      9.45     18.90     37.79    151.17    453.50
  MH        316      3.80     11.40     22.79     45.58    182.33    547.00
  MH        423      5.08     15.25     30.50     61.00    244.00    732.00
  H         616      7.40     22.21     44.42     88.83    355.33   1066.00
  H         889     10.68     32.04     64.08    128.17    512.67   1538.00
  H        1272     15.28     45.85     91.71    183.42    733.67   2201.00
  VH       1618     19.44     58.32    116.65    233.29    933.17   2799.50
  VH       2618     31.45     94.36    188.73    377.46   1509.83   4529.50
  VH       3618     43.47    130.41    260.81    521.62   2086.50   6259.50
  UH       4236     50.89    152.68    305.35    610.71   2442.83   7328.50
  UH       4618     55.48    166.45    332.90    665.79   2663.17   7989.50
  UH       5000     60.07    180.21    360.42    720.83   2883.33   8650.00
```

### 6(c) · V-ULT OCCUPANCY — what VH and UH spend their time doing

```
timeframes: ['5m', '15m', '30m']   families: ['VH', 'UH']
shares are over WARM bars only (orientation != n/a); knot = width_atr < 0.5

asset     tf   fam        warm   knot%   comp%   flat%    exp%   bull%    mix%   bear%   w_p50
--------------------------------------------------------------------------------------------------------------
BTCUSDT   5m   VH      716,314    2.86   40.30   22.96   36.74   48.95    9.02   42.02   7.390
BTCUSDT   5m   UH      711,533   10.18    4.12   92.85    3.03   51.98    1.94   46.08   2.283
BTCUSDT   15m  VH      230,426    3.33   41.78   22.92   35.28   48.56   12.17   39.27   8.268
BTCUSDT   15m  UH      225,645    8.10    3.84   93.31    2.85   56.86    1.24   41.90   2.723
BTCUSDT   30m  VH      108,954    1.74   42.84   21.23   35.91   54.30    7.47   38.23   9.442
BTCUSDT   30m  UH      104,173    9.44    4.81   92.92    2.26   60.04    2.72   37.24   2.787
ETHUSDT   5m   VH      693,396    2.76   41.25   22.86   35.88   46.80    9.60   43.60   7.716
ETHUSDT   5m   UH      688,615   10.06    3.77   94.07    2.16   51.26    2.33   46.40   2.293
ETHUSDT   15m  VH      222,786    3.27   40.14   23.27   36.58   49.17   11.20   39.63   7.686
ETHUSDT   15m  UH      218,005    9.61    3.21   95.07    1.71   55.62    2.89   41.49   2.458
ETHUSDT   30m  VH      105,134    2.91   42.00   20.00   37.99   49.54   11.60   38.87   8.285
ETHUSDT   30m  UH      100,353    6.56    3.04   94.23    2.70   53.53    1.83   44.64   2.463
SOLUSDT   5m   VH      609,309    3.57   39.22   24.48   36.30   44.80   10.19   45.01   6.978
SOLUSDT   5m   UH      604,528   13.08    3.03   95.91    1.06   47.36    2.52   50.12   2.063
SOLUSDT   15m  VH      194,757    3.11   41.36   22.61   36.02   43.88    9.18   46.95   7.039
SOLUSDT   15m  UH      189,976   14.45    2.69   96.03    1.27   47.68    2.59   49.73   2.055
SOLUSDT   30m  VH       91,119    3.56   42.51   23.41   34.05   41.39   10.15   48.46   7.092
SOLUSDT   30m  UH       86,338   11.64    3.42   94.82    1.74   42.57    1.18   56.25   2.481
NEARUSDT  5m   VH      600,369    3.73   39.37   25.08   35.55   40.33   10.37   49.31   6.752
NEARUSDT  5m   UH      595,588   11.59    1.79   97.09    1.11   44.20    2.17   53.62   2.090
NEARUSDT  15m  VH      191,777    3.58   40.37   24.63   34.99   37.05   10.50   52.45   6.797
NEARUSDT  15m  UH      186,996   12.38    3.27   95.41    1.31   40.01    1.84   58.15   2.050
NEARUSDT  30m  VH       89,629    3.75   40.98   23.40   35.60   33.70   10.62   55.68   7.333
NEARUSDT  30m  UH       84,848    9.30    2.50   95.13    2.35   35.26    1.45   63.29   2.664
ZECUSDT   5m   VH      673,233    3.97   39.37   24.32   36.32   43.25   11.22   45.53   6.470
ZECUSDT   5m   UH      668,452   12.92    2.00   96.41    1.60   48.15    2.47   49.38   2.009
ZECUSDT   15m  VH      216,065    3.75   40.04   24.14   35.80   42.11   11.20   46.69   6.395
ZECUSDT   15m  UH      211,284   13.85    2.20   96.63    1.16   44.67    2.56   52.77   1.645
ZECUSDT   30m  VH      101,773    4.90   38.53   25.07   36.38   39.17   11.85   48.98   5.707
ZECUSDT   30m  UH       96,992   17.50    2.30   96.21    1.47   43.41    1.47   55.12   1.568

OBSERVED -- the state window is not scale-matched to the ultra ribbons.
`state` is pinned at k = 20 bars with a +-0.05 ATR threshold. Twenty bars is
a large fraction of a VH ribbon's own movement and a negligible one of UH's:
the UH lines (4236/4618/5000) span only 1.18x in length, so their band width
barely changes over 20 bars and the classifier returns `flat` almost always.
The shares below are the evidence for that statement; the constants are VETO
by name and are NOT changed here. What it means is that `UH state` carries
much less information than `VH state` does, and the two must not be read as
if they were the same measurement.

  family    flat% (panel mean)   width_atr p50
----------------------------------------------
  VH                     23.36           7.290
  UH                     95.07           2.242

STATE x ORIENTATION cross-tab, % of warm bars (panel mean over assets)

  VH @ 5m   (5 assets, 3,292,621 warm bars)
                      bull    mixed     bear      row
    compressing      17.24     3.99    18.67    39.90
    flat             10.99     2.07    10.88    23.94
    expanding        16.59     4.02    15.54    36.16

  VH @ 15m   (5 assets, 1,055,811 warm bars)
                      bull    mixed     bear      row
    compressing      16.82     4.46    19.47    40.74
    flat             10.60     1.99    10.93    23.51
    expanding        16.73     4.40    14.60    35.74

  VH @ 30m   (5 assets, 496,609 warm bars)
                      bull    mixed     bear      row
    compressing      17.04     4.39    19.94    41.37
    flat             10.08     1.94    10.60    22.62
    expanding        16.49     4.00    15.49    35.99

  UH @ 5m   (5 assets, 3,268,716 warm bars)
                      bull    mixed     bear      row
    compressing       1.14     0.10     1.70     2.94
    flat             46.62     2.13    46.51    95.26
    expanding         0.82     0.06     0.91     1.79

  UH @ 15m   (5 assets, 1,031,906 warm bars)
                      bull    mixed     bear      row
    compressing       1.04     0.08     1.92     3.04
    flat             47.32     2.09    45.87    95.29
    expanding         0.59     0.06     1.01     1.66

  UH @ 30m   (5 assets, 472,704 warm bars)
                      bull    mixed     bear      row
    compressing       1.40     0.13     1.68     3.21
    flat             45.03     1.50    48.13    94.66
    expanding         0.51     0.09     1.50     2.10
```

### 6(d)(i) · FAST-ribbon crosses conditioned on VH+UH orientation

```
The operator's question, made descriptive.  For every FAST within-ribbon cross
on ['5m', '15m'], the joint orientation of the two ULTRA ribbons at that same bar is
read off, and the forward terminal return is tabulated inside each stratum.

  ruler       signed terminal return over H100, ATR-normalised AT THE ANCHOR
              (census-2A R-1: MFE-MAE is retired as a discriminant)
  H100        DURATION-fixed at 100 x 5m = 500 minutes, so the
              5m and 15m tables answer the same question
  sign        + means price went the way the cross pointed; up and down crosses
              are ALSO split out separately, never pooled silently
  toll        the round-trip toll measured on THIS population, printed beside
              every row.  A stratum whose median sits inside the toll band has
              produced nothing a trader could have kept.

NOTHING IS PROMOTED.  Every stratum of a complete partition is printed; no
threshold is swept, no arm is ranked and kept.  m = 0.

FAST pair 12_26 @ 5m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     47,788  -4.1455  -0.0875   3.9647  -0.0094   49.26  0.3529      YES
  bull-fanned   up       23,855  -3.9841  -0.0967   4.1689   0.3400   49.28  0.3529      YES
  bull-fanned   down     23,933  -4.3044  -0.0877   3.7543  -0.3577   49.24  0.3529      YES
  mixed         both     25,871  -4.1485  -0.0984   3.9988  -0.0053   49.22  0.3927      YES
  mixed         up       12,914  -4.1548  -0.1869   3.9301   0.0684   48.63  0.3926      YES
  mixed         down     12,957  -4.1678  -0.0014   4.1078  -0.0787   49.80  0.3928      YES
  bear-fanned   both     48,067  -4.1158  -0.1006   3.9938  -0.0075   49.05  0.3662      YES
  bear-fanned   up       24,092  -4.0357   0.0160   3.9354  -0.0718   50.00  0.3662      YES
  bear-fanned   down     23,975  -4.1960  -0.2393   4.0789   0.0571   48.08  0.3661      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.

FAST pair 9_12 @ 5m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     82,246  -4.0676  -0.0951   3.8875  -0.0337   49.18  0.3451      YES
  bull-fanned   up       41,096  -3.8859  -0.0497   4.0694   0.3435   49.63  0.3451      YES
  bull-fanned   down     41,150  -4.2407  -0.1476   3.7085  -0.4104   48.72  0.3451      YES
  mixed         both     43,949  -4.0881  -0.0524   3.9536  -0.0035   49.39  0.3842      YES
  mixed         up       21,957  -4.0902  -0.0842   3.9020   0.1233   49.15  0.3842      YES
  mixed         down     21,992  -4.0855  -0.0146   4.0172  -0.1301   49.63  0.3842      YES
  bear-fanned   both     82,186  -4.0837  -0.0770   3.9741  -0.0141   49.25  0.3570      YES
  bear-fanned   up       41,133  -3.9806   0.0446   3.9833  -0.0520   50.10  0.3571      YES
  bear-fanned   down     41,053  -4.1690  -0.2049   3.9728   0.0240   48.38  0.3570      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.

FAST pair 9_26 @ 5m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     55,527  -4.1156  -0.0909   3.9255  -0.0257   49.24  0.3530      YES
  bull-fanned   up       27,725  -3.9206  -0.0774   4.1165   0.3401   49.54  0.3530      YES
  bull-fanned   down     27,802  -4.2741  -0.1227   3.7147  -0.3905   48.95  0.3530      YES
  mixed         both     29,851  -4.1478  -0.1078   4.0177  -0.0022   49.07  0.3925      YES
  mixed         up       14,910  -4.1672  -0.1643   3.9550   0.1020   48.71  0.3925      YES
  mixed         down     14,941  -4.1494  -0.0475   4.1144  -0.1062   49.44  0.3926      YES
  bear-fanned   both     55,735  -4.1418  -0.1147   3.9810  -0.0143   48.96  0.3659      YES
  bear-fanned   up       27,919  -4.0103   0.0006   3.9386  -0.0303   49.97  0.3660      YES
  bear-fanned   down     27,816  -4.2349  -0.2680   4.0190   0.0018   47.95  0.3659      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.

FAST pair 12_26 @ 15m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     14,201  -2.3087  -0.0500   2.2839   0.0172   49.20  0.1969      YES
  bull-fanned   up        7,088  -2.2861  -0.0320   2.3898   0.1750   49.66  0.1969      YES
  bull-fanned   down      7,113  -2.3407  -0.0776   2.1749  -0.1401   48.74  0.1969      YES
  mixed         both      9,026  -2.2867  -0.0791   2.2033  -0.0159   48.60  0.2141      YES
  mixed         up        4,515  -2.1766   0.0062   2.2536   0.0989   49.90  0.2141      YES
  mixed         down      4,511  -2.3611  -0.1887   2.1271  -0.1308   47.31  0.2140      YES
  bear-fanned   both     14,470  -2.2953  -0.0708   2.2954   0.0107   49.14  0.1966      YES
  bear-fanned   up        7,246  -2.2601  -0.0263   2.2831   0.0434   49.61  0.1966      YES
  bear-fanned   down      7,224  -2.3014  -0.1051   2.3046  -0.0221   48.67  0.1966      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.

FAST pair 9_12 @ 15m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     24,848  -2.3027  -0.0718   2.1811  -0.0350   48.87  0.1912      YES
  bull-fanned   up       12,413  -2.2854  -0.0428   2.2076   0.0839   49.37  0.1911      YES
  bull-fanned   down     12,435  -2.3100  -0.1223   2.1486  -0.1537   48.37  0.1912      YES
  mixed         both     15,654  -2.2461  -0.0829   2.1112  -0.0248   48.64  0.2112      YES
  mixed         up        7,836  -2.1349  -0.0498   2.1409   0.0552   49.30  0.2112      YES
  mixed         down      7,818  -2.3452  -0.1313   2.0966  -0.1050   47.98  0.2112      YES
  bear-fanned   both     25,291  -2.2941  -0.0814   2.2308  -0.0027   48.69  0.1950      YES
  bear-fanned   up       12,648  -2.2856  -0.0650   2.1925  -0.0253   48.87  0.1950      YES
  bear-fanned   down     12,643  -2.3033  -0.1038   2.2665   0.0199   48.51  0.1950      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.

FAST pair 9_26 @ 15m -- panel, by VH+UH orientation
  orient        dir           n      p25      p50      p75     mean     %>0    toll  in toll
----------------------------------------------------------------------------------------------------
  bull-fanned   both     16,489  -2.3290  -0.0488   2.2776  -0.0031   49.19  0.1962      YES
  bull-fanned   up        8,230  -2.2978  -0.0650   2.4121   0.1382   49.34  0.1962      YES
  bull-fanned   down      8,259  -2.3773  -0.0837   2.1675  -0.1439   49.03  0.1962      YES
  mixed         both     10,426  -2.2927  -0.0850   2.1816  -0.0287   48.63  0.2138      YES
  mixed         up        5,217  -2.2660  -0.0096   2.2221   0.0667   49.78  0.2138      YES
  mixed         down      5,209  -2.3408  -0.1888   2.1170  -0.1243   47.48  0.2138      YES
  bear-fanned   both     16,751  -2.2437  -0.0590   2.2348   0.0190   49.06  0.1962      YES
  bear-fanned   up        8,386  -2.2370  -0.0695   2.2083   0.0101   49.01  0.1962      YES
  bear-fanned   down      8,365  -2.2356  -0.0472   2.2591   0.0279   49.12  0.1962      YES
  TOLL LINE: round-trip 10 bps, measured on each stratum's own rows. 'in toll' = |median| <= toll.
```

### 6(d)(ii) · VH/UH knot episodes — the knot→fan, at ultra scale, counted

```
episode      a maximal run of bars with width_atr < 0.5 (the pinned knot)
expansion    the FIRST bar after the run whose state is `expanding`
             (|width_delta_20| > 0.05 ATR), searched at most
             2,000 bars forward; episodes that never expand are
             counted as such and are NOT dropped
direction    the ribbon's own orientation at the expansion bar
magnitude    peak width_atr reached before the next knot, minus width at the
             knot's last bar
displacement price move from the knot's last bar to that peak, in ATR at the knot

asset     tf   fam   episodes  expanded   never  len_p50  ttl_p50  ttl_p90  mag_p50  disp_p50
--------------------------------------------------------------------------------------------------------------
BTCUSDT   15m  UH         304       220      84     13.0    472.5   1537.3    1.708    12.237
BTCUSDT   15m  VH         139       139       0     24.0      1.0    179.4    0.348    -1.235
BTCUSDT   1h   UH          69        59      10      9.0    417.0   1379.6    4.718    -6.170
BTCUSDT   1h   VH          29        29       0     19.0      1.0    243.0    0.226     2.724
BTCUSDT   30m  UH         158       151       7      9.0    577.0   1668.0    0.405    10.005
BTCUSDT   30m  VH          35        35       0     56.0      1.0     76.2    1.990    -0.882
BTCUSDT   5m   UH       1,136       715     421     11.0    486.0   1511.8    0.701     1.904
BTCUSDT   5m   VH         362       362       0     30.0      1.0    137.9    0.897     0.009
ETHUSDT   15m  UH         311       224      87     11.0    601.5   1521.8    1.703   -27.424
ETHUSDT   15m  VH         124       124       0     21.0      1.0    102.4    0.204     0.583
ETHUSDT   1h   UH         141        88      53      8.0    750.5   1291.5   -0.066   -16.952
ETHUSDT   1h   VH          18        18       0     42.0      1.0     72.5    6.096     1.031
ETHUSDT   30m  UH         125       123       2     11.0    358.0    827.2    1.232     4.992
ETHUSDT   30m  VH          55        55       0     14.0      1.0    103.8    0.327    -1.647
ETHUSDT   5m   UH         981       609     372      9.0    461.0   1496.8    0.558     0.637
ETHUSDT   5m   VH         333       329       4     36.0      1.0    138.4    0.536     0.072
NEARUSDT  15m  UH         294       134     160     10.0    649.5   1379.1    3.013   -13.438
NEARUSDT  15m  VH          89        89       0     63.0      1.0     92.6    0.495    -0.794
NEARUSDT  1h   UH          36        11      25      9.5    653.0   1637.0   -0.383   -15.244
NEARUSDT  1h   VH          13        13       0     42.0      1.0     75.0   10.877    -8.766
NEARUSDT  30m  UH          93        46      47      9.0    879.5   1884.5    2.226   -17.700
NEARUSDT  30m  VH          54        54       0     16.0      1.5    238.4    0.059    -2.815
NEARUSDT  5m   UH         913       416     497      9.0    620.5   1561.5    1.963    -2.622
NEARUSDT  5m   VH         321       321       0     29.0      1.0    230.0    0.752    -0.323
SOLUSDT   15m  UH         309       136     173     12.0    637.0   1642.0    3.649    -8.193
SOLUSDT   15m  VH          88        88       0     27.0      1.0     99.6    0.844    -2.158
SOLUSDT   1h   UH          52        32      20     10.5    370.0   1639.4    1.679    34.402
SOLUSDT   1h   VH          23        23       0      7.0      1.0    160.4    0.037     8.149
SOLUSDT   30m  UH         136        83      53     11.0    843.0   1807.4    2.667     1.222
SOLUSDT   30m  VH          58        58       0     14.0      1.0    417.9    0.115    -0.537
SOLUSDT   5m   UH       1,022       368     654      9.0    662.5   1747.3    0.395     0.451
SOLUSDT   5m   VH         304       304       0     44.0      1.0    129.1    1.158    -0.613
ZECUSDT   15m  UH         406       185     221      8.0    643.0   1666.8    1.320    -1.691
ZECUSDT   15m  VH         116       116       0     19.5      1.0    103.0    0.425     0.697
ZECUSDT   1h   UH         115        10     105      8.0    500.0   1125.9    0.064     2.810
ZECUSDT   1h   VH          28        28       0     73.5      1.0    110.4    3.238     3.109
ZECUSDT   30m  UH         241        83     158      7.0    618.0   1484.4    2.425     1.827
ZECUSDT   30m  VH          79        79       0     10.0      1.0    177.2    0.077     0.159
ZECUSDT   5m   UH       1,212       586     626      8.0    620.5   1588.0    1.824    -1.766
ZECUSDT   5m   VH         362       358       4     20.5      1.0    193.9    0.265    -0.576

EXPANSION DIRECTION -- the per-direction split, on a complete partition
  fam  tf         bull       bear      mixed      never  bull share
----------------------------------------------------------------------
  UH   15m         290        519         90        725      0.3585
  UH   1h           64        119         17        213      0.3497
  UH   30m         235        199         52        267      0.5415
  UH   5m        1,191      1,156        347      2,570      0.5075
  VH   15m          41         46        469          0      0.4713
  VH   1h           11          8         92          0      0.5789
  VH   30m          33         16        232          0      0.6735
  VH   5m          153        207      1,314          8      0.4250

CAVEAT -- READ THIS BEFORE THE TIME-TO-EXPANSION COLUMN.
`knot` and `expanding` are two SEPARATELY pinned constants (c = 0.5 ATR;
|width_delta_20| > 0.05 ATR) and they are not scale-matched to each other.
A knot run ENDS precisely when the width rises back through 0.5 ATR -- which
is, mechanically, a width that is increasing. So for a ribbon whose width
moves at all on a 20-bar scale, the bar after the knot is ALREADY `expanding`
and time-to-expansion is 1 by construction, not by anything in the tape.
The share of episodes for which that happens is printed below. Where it is
near 100%, the time-to-expansion column is measuring the definition.

  fam  tf    episodes  expanded  immediate  immediate share
--------------------------------------------------------------
  UH   15m      1,624       899         36           0.0400
  UH   1h         413       200          5           0.0250
  UH   30m        753       486         16           0.0329
  UH   5m       5,264     2,694        139           0.0516
  VH   15m        556       556        378           0.6799
  VH   1h         111       111         75           0.6757
  VH   30m        281       281        170           0.6050
  VH   5m       1,682     1,674      1,111           0.6637

DISPLACEMENT vs THE TOLL -- knot-to-peak move, in ATR
  NOTE: displacement is measured over the WHOLE span from the knot's last
  bar to the peak-width bar. That span is long and variable (`span_p50`),
  so this is a SPAN statistic, not a per-trade edge; the toll is a FLOOR
  it must clear, not a benchmark it can be compared to directly.

  fam  tf         n  span_p50  |d| p25  |d| p50  |d| p75  signed p50     toll  toll/|d|p50
-----------------------------------------------------------------------------------------------
  UH   15m      899      2000    8.776   22.512   42.536      -3.670   0.1499       0.0067
  UH   1h       200      1054    8.198   22.400   40.920      -7.852   0.0862       0.0039
  UH   30m      486      1498    6.213   16.840   30.983      +3.616   0.0985       0.0059
  UH   5m     2,694      1309    7.743   20.267   40.191      +0.075   0.2919       0.0144
  VH   15m      556       184    2.256    6.878   17.037      -0.584   0.1718       0.0250
  VH   1h       111       240    2.162    8.323   14.528      +2.220   0.0901       0.0108
  VH   30m      281       231    1.937    5.080   15.658      -1.042   0.1003       0.0197
  VH   5m     1,674       306    2.725    7.823   17.537      -0.358   0.2879       0.0368

  TOLL LINE: 10 bps round trip, measured on EACH population's own bars.
  It is NOT the census-2A 4h figure (0.026-0.059 ATR): the toll in ATR units GROWS as
  the timeframe shortens, because ATR shrinks faster than price does. Quoting a 4h toll
  beside a 5m table would understate the cost by roughly an order of magnitude.
```

### 6(d)(iii) · census-2A campaign book × VH ribbon state

```
  cen5_campaigns 6,834 rows  D:\Naiad\research_outputs\census2a\cen5\cen5_campaigns.parquet   <- THE campaign book
  cen4_book      6,897 rows  D:\Naiad\research_outputs\census2a\cen4\cen4_book.parquet   <- realised-R side
  join tf        5m   (census EXEC_TF; VH state read at the bar CONTAINING the entry)

  F-KEY -- declared keys asserted BEFORE the join, never after
    F-KEY  cen5_campaigns                 key=['tranche_id'] rows=6,834 dup=0
    F-KEY  cen5_campaigns composite       key=['asset', 'ts_ms', 'mandate'] rows=6,834 dup=0
    F-KEY  cen4_book (cell|tranche_id)    key=['ckey'] rows=6,897 dup=0
    NOTE  (asset, ts_ms) alone has dup=1 in cen5_campaigns -- a BTC intraday
          and a BTC swing campaign share one instant. `mandate` is part of the key
          for that reason; it is not a defect.
    joined rows = 6,834  matched = 6,643  unmatched = 191 (['JTOUSDT', 'TAOUSDT'] -- the ANNEX assets, absent from the panel-only cen4_book)

  REPORTED, NOT FIXED -- 'ribbon state at EXIT' cannot be computed.
  The contract asks for VH state at entry AND at exit.  cen4_book carries
  ts_open / ts_ms (both the ENTRY) and cen5_campaigns carries no exit
  timestamp at all -- only realised outcomes (ride_R, give_back_R, mfe_R).
  cen2_ledger's window_close_ts is the ARMING WINDOW's close, a different
  object, and using it as an exit would be an invention.  The ENTRY side is
  computed in full below; the exit side is left undone and named here.

  campaigns placed on a 5m bar: 6,643   of which VH is WARM at entry: 6,571 (98.9%)
  the cold remainder is NOT dropped silently -- it is 72 campaigns whose entry predates VH's warm-up on 5m, and it is excluded from the state tables below by construction, not by choice.

  winners 800  losers 5,771   (census-2A `outcome_sign`, defined on ride_R -- not a cut made here)
  toll on this population = 0.2878 ATR

WINNERS vs LOSERS BY VH RIBBON STATE AT ENTRY (occupancy shares, %)

  VH state
    value             winners%   losers%      all%    n_win    n_los
    compressing          53.50     53.91     53.86      428    3,111
    expanding            19.25     13.19     13.92      154      761
    flat                 27.25     32.91     32.22      218    1,899

  VH orientation
    value             winners%   losers%      all%    n_win    n_los
    bear-fanned          40.38     42.37     42.12      323    2,445
    bull-fanned          46.12     43.79     44.07      369    2,527
    mixed                13.50     13.85     13.80      108      799

  VH+UH joint orientation
    value             winners%   losers%      all%    n_win    n_los
    bear-fanned          34.25     36.06     35.84      274    2,081
    bull-fanned          38.62     37.57     37.70      309    2,168
    mixed                26.12     25.44     25.52      209    1,468
    n/a                   1.00      0.94      0.94        8       54

  knot at entry: winners 6.12%  losers 5.06%  all 5.19%

RIDE-R BY VH ORIENTATION AT ENTRY -- with the per-direction split
  vh_orient      dir           n      p25      p50      p75     mean    %win  mfe_p50    toll
----------------------------------------------------------------------------------------------------
  bear-fanned    both      2,768  -1.0951  -1.0348  -0.6220   0.0967   11.67   0.9227  0.3045
  bear-fanned    long      1,099  -1.0875  -1.0233  -0.4341   0.5454   12.65   0.8534  0.3120
  bear-fanned    short     1,669  -1.1016  -1.0404  -1.0067  -0.1988   11.02   0.9919  0.2988
  bull-fanned    both      2,896  -1.0776  -1.0311  -0.6444   0.5663   12.74   1.0044  0.2745
  bull-fanned    long      1,689  -1.0751  -1.0332  -1.0083   0.8518   11.96   1.0142  0.2661
  bull-fanned    short     1,207  -1.0827  -1.0270  -0.4040   0.1667   13.84   0.9860  0.2827
  mixed          both        907  -1.0801  -1.0311  -0.7154   0.0523   11.91   0.9866  0.2844
  mixed          long        456  -1.0753  -1.0288  -0.7196   0.3852   11.40   0.9312  0.2653
  mixed          short       451  -1.0814  -1.0343  -0.7154  -0.2844   12.42   1.0446  0.3033

  --- by vult_orient ---
  bear-fanned    both      2,355  -1.0996  -1.0345  -0.6190   0.1123   11.63   0.8966  0.3131
  bear-fanned    long        927  -1.0898  -1.0218  -0.4282   0.5693   12.41   0.8203  0.3209
  bear-fanned    short     1,428  -1.1048  -1.0406  -1.0073  -0.1843   11.13   0.9712  0.3070
  bull-fanned    both      2,477  -1.0772  -1.0305  -0.6397   0.5376   12.47   0.9998  0.2669
  bull-fanned    long      1,463  -1.0751  -1.0330  -1.0084   0.8564   11.83   0.9969  0.2581
  bull-fanned    short     1,014  -1.0807  -1.0235  -0.3854   0.0777   13.41   1.0037  0.2793
  mixed          both      1,677  -1.0809  -1.0338  -0.7014   0.1956   12.46   1.0122  0.2889
  mixed          long        817  -1.0776  -1.0320  -0.6865   0.4759   12.36   1.0187  0.2826
  mixed          short       860  -1.0824  -1.0363  -0.7108  -0.0706   12.56   0.9998  0.2973
  n/a            both         62  -1.0949  -1.0223  -0.4525   0.4945   12.90   1.0466  0.2762
  n/a            long         37  -1.0980  -1.0220  -0.4360   1.1983   10.81   0.7710  0.3186
  n/a            short        25  -1.0855  -1.0252  -0.5320  -0.5472   16.00   1.1753  0.2481

  --- by vh_state ---
  compressing    both      3,539  -1.0859  -1.0314  -0.5380   0.2808   12.09   0.9195  0.2923
  compressing    long      1,703  -1.0837  -1.0289  -0.5279   0.7293   12.57   0.8783  0.3004
  compressing    short     1,836  -1.0879  -1.0334  -0.5469  -0.1352   11.66   0.9632  0.2893
  expanding      both        915  -1.0520  -1.0193  -0.6875   0.4751   16.83   1.1117  0.3051
  expanding      long        454  -1.0456  -1.0174  -0.7326   0.6545   15.86   1.1425  0.2837
  expanding      short       461  -1.0601  -1.0206  -0.6663   0.2984   17.79   1.0178  0.3207
  flat           both      2,117  -1.0933  -1.0428  -1.0058   0.2487   10.30   0.9909  0.2743
  flat           long      1,087  -1.0842  -1.0394  -1.0098   0.6207    9.84   0.9578  0.2526
  flat           short     1,030  -1.1101  -1.0472  -0.8139  -0.1439   10.78   1.0454  0.2980

  TOLL LINE: 10 bps round trip = 0.2878 ATR median on this population.
  ride_R is already R-normalised by census-2A; the toll column is printed in ATR,
  so the two rulers sit side by side and are never silently mixed.

  THIS IS A DESCRIPTIVE OVERLAY. No comparison above is promoted; the strata are a
  COMPLETE partition of a fixed population, printed whole. m = 0.
```

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
3,644,162 bars at the start of this session and 3,645,602 an hour later; SOL, NEAR and ZEC each
gained exactly 1,440 bars — one day of 1m tape. Evidence-era columns are unaffected (they are
bounded by `CEIL_MS = 2024-07-01`); only `bars_available` and `last_bar` move. Verified against
the pre-drift snapshot: **verdict changed on 0 of 90 cells, coverage changed on 0 of 90.**
Recorded so a re-run that prints different bar counts is not mistaken for a defect.

**11 · A killed run leaves a corrupt parquet that looks like a valid artifact. FIXED.** Stopping
the 1m pass left `emas/BTCUSDT/1m.parquet` at 10,889,472 B — a stump of a ~400 MB file, with no
parquet footer (`ArrowInvalid: Parquet magic bytes not found`). It is unreadable, but it is
still a *file*: `p.exists()` is `True`, and the manifest recorded its size and sha256 as though
it were real. Fixed twice over — every artifact now writes through `to_parquet_atomic` (temp
file + `os.replace`, atomic on both platforms), so a killed run leaves either a complete file or
none; and the manifest now calls `parquet_rows()`, which reads the footer and **HALTs** rather
than record a file it cannot open.

**12 · Pin-merge resurrected a deleted artifact. FIXED.** Having deleted the corrupt file by
hand, the next manifest write brought it straight back — with its stale byte count and sha —
because I12 merge semantics carry prior entries forward unconditionally. The manifest claimed
101 artifacts and 696,766,971 B of `emas/` for a file that was not on disk. I12 says pins
*merge*; it does not license the manifest to assert a file that is not there. `write_manifest`
now prunes entries whose `path` no longer exists and prints what it dropped. Verified: 101 → 100
artifacts, and all 18 pins survive the prune.

**13 · The manifest was recording `rows: 0` for every artifact.** `len(pd.read_parquet(p,
columns=[]))` returns a zero-row frame for *any* file — it is not a row count and it is not a
readability check. Replaced with the parquet footer's `num_rows`. The corrected manifest records
**15,296,185 rows**; the previous one recorded zero for all 100.

---

---

## 7b · WHAT AN ADVERSARIAL REVIEW OF THIS PROGRAM FOUND

The program was put through a 53-agent adversarial review across six lenses (the warm-up law,
contract compliance, the ribbon algebra, the event schema, whether the fixtures actually test
anything, and resource/failure behaviour). Every raised finding was then handed to a separate
agent whose only instruction was to **refute** it, defaulting to *refuted* under uncertainty.
**Nine survived.** All nine are fixed above or below; none is left open.

The one that mattered is **#14 — the 510,584 dropped band traversals**, which no fixture in this
build would have caught, because every fixture asked "is what we emitted correct?" and none asked
"is there something we should have emitted and did not?" That is the gap worth carrying forward:
**F-B5b hand-verifies three events per class and cannot see an entire missing class.** A
completeness check — partition every `pos` transition and assert the taxonomy covers all of them
— is the fixture this build lacked, and is named here rather than retrofitted silently.

Two further findings are recorded as **fixed** rather than reported, since they change behaviour:

**14 · The band grammar dropped single-bar traversals. FIXED.** 510,584 events, 18.4 % of all
band transitions. See §5.

**15 · The manifest stamped Tier-E tables as `SUBSTRATE`. FIXED.** `write_manifest` swept every
`*.parquet` under `OUT` and gave them all `"class": "SUBSTRATE -- census-2B V-ULT-1"`, including
the eight display-only Stage-5 tables. The manifest is what a later reader cites; a Tier-E probe
labelled substrate in the record of record is precisely how a probe becomes evidence without
anyone deciding that it should. `firstlook/` now stamps `DISPLAY-ONLY / Tier-E exploration —
m = 0`.

**16 · `knot` was a bare bool, so "not computed" and "never knotted" were the same byte. FIXED.**
`state`, `orient` and `pos` all carried a `-9` sentinel; `knot` alone did not, so a `NEVER` cell
wrote `False` for every bar and `df.UH_knot.mean()` on BTC 12h returned a confident `0.00 %` for
a family that was never computed. Absent data presented as a definite negative is this estate's
signature wound. `knot` is now `int8` with `{0: no, 1: knot, -9: n/a}`, and the legend is in the
manifest's `pins.codes` beside the other three.

**17 · `--stage 34` — a missing comma — ran nothing and exited 0. FIXED.** Unrecognised tokens
now HALT with the valid set named, instead of silently matching no guard and looking like success.

**18 · Fixture cells were hardcoded, so any scoped run crashed or read stale artifacts. FIXED.**
F-B3, F-B4a and F-B5a pinned `BTCUSDT 1h`, `ETHUSDT 1h` and `NEARUSDT 4h`. Under `--assets
BTCUSDT` the fixtures raised `FileNotFoundError` against a clean tree — and against a *dirty*
one they would have read a cell an earlier run wrote, silently certifying artifacts this run
never produced. That is the worse failure. All three now go through `pick_cell`, which keeps the
preferred cell for reproducibility, falls back to the largest cell **this run** actually wrote,
and skips loudly when there is none.

---

## 8 · DISPOSITION & BOX-COST

### Artifact inventory — all bulk on `D:`, none committed

| group | files | rows | bytes | MB |
|---|---:|---:|---:|---:|
| `cen2b_feasibility.parquet` | 1 | 630 | 12,402 | 0.0 |
| `emas/` | 30 | 5,405,628 | 685,877,499 | 685.9 |
| `ribbons/` | 30 | 5,405,628 | 941,191,268 | 941.2 |
| `crosses/` | 30 | 4,974,690 | 78,211,567 | 78.2 |
| `firstlook/` (Tier-E) | 9 | 20,501 | 1,006,285 | 1.0 |
| **total** | **100** | **15,807,077** | **1,706,299,021** | **1,706.3** |

Manifest: `D:\Naiad\research_outputs\census2b\census2b_manifest.json` — **100 artifacts**, each carrying `{path, rows, bytes, sha256, class}`. **9** carry `DISPLAY-ONLY / Tier-E exploration — m = 0`; the rest carry `SUBSTRATE — census-2B V-ULT-1`. The `pins` block holds 18 keys (the six ribbons, tfs, panel, annex, warmfactor, all 18 `warm_bars` values, k_window, state_eps_atr, knot_c_atr, atr_len, kiss, midline_pairs, toll, the four int8 code legends, and three provenance notes). Pins survived both the merge and the prune intact.

### BOX-COST

| item | value |
|---|---:|
| `exchange/**` before this build | 2,137,089 B |
| box budget (`publish_exchange.BOX_BYTES`) | 6,390,000 B |
| occupancy before | 33.44 % |
| this build adds | **115,730 B** |
| occupancy after | **35.26 %** |
| WARN line / REFUSE line | 25 % / 40 % |
| bulk on `D:` (not committed) | 1,706,299,021 B |

**The addition is 1.81 % of the bus, against the contract's `<1 %`.** Stated plainly rather than met by quiet subtraction. The overage is almost entirely the two blocks the contract required *verbatim* and *in full*: the 630-cell feasibility matrix (~24 KB, already compressed by factoring out `warm_bars`, which depends only on `N`, and `bars available`, which depends only on `(asset, tf)` — **no cell was dropped**) and the complete Stage-5 transcript (~41 KB). Occupancy lands at 35.26 %, above the 25 % WARN line — which it already was at 33.44 % — and **well below the 40 % REFUSE line**, so `publish_exchange` will not refuse.

**The lever, named rather than pulled:** moving the per-cell matrix block to a `D:` pointer stub would cut ~17 KB. It is not done unilaterally, because the contract asked for that matrix verbatim in this document, and trading a stated content requirement for a byte target is the operator's call, not the builder's.

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

## 10 · LEDGER_APOLLO APPEND (F-17 · same session)

The following was appended to `exchange/status/LEDGER_APOLLO.md` in this same session:

```
=== STATUS_APOLLO — 2026-08-14a ===
NOW: CENSUS-2B / V-ULT-1 IS BUILT. Six EMA ribbons x seven timeframes x five assets are on D: as
a substrate, with the warm-up law asserted rather than assumed, and the operator's question has
had its first descriptive look. CLASS: substrate + DISPLAY-ONLY / Tier-E. Selection surface
m = 0 — this build registers nothing, scores nothing and claims nothing. The census-2A record is
untouched.
LAST EVENT: 2026-08-14 — census-2B V-ULT-1: the U-VHT data module (contract ratified 2026-08-12)
FACTS:
- THE FEASIBILITY MATRIX RAN FIRST, 630 cells, before one EMA was computed. 45 cells are NEVER
  and were SKIPPED not computed; 14 are OPS-ONLY. The contract's expectation is confirmed and
  sharpened: UH is NEVER on 4h and 12h, VH is NEVER on 12h and OPS-ONLY on 4h. 1m is FULL for
  all 18 lengths on all 5 assets [verified]
- F-B0, A FIXTURE THE CONTRACT DID NOT ASK FOR, settles a real ambiguity: the contract pins
  warm_bars = ceil(3.46*N) and calls it "the SEQ8 rule", but the SEQ8 rule in this estate is
  ceil(log(1e-3)/log(1-alpha)) and they are different expressions. ceil(3.46*N) is >= the exact
  rule for all 18 lengths (delta 0..+30, never negative), so the contract constant is the
  CONSERVATIVE one and is used as written, by name. A FAIL would have halted before stage 1
  [verified]
- WARM-UP ASSERTED, NOT INTENDED. F-B2: 0 cold-head values across 540 series, and every NEVER
  column proved all-NaN. Because the cold head is NaN at the source, crossover/crossunder return
  False there BY CONSTRUCTION — the defect that produced ~50 phantom 4h armings on 2026-08-12
  cannot recur here. F-B3: every family's middle EMA bit-matches a hand-run recursion [verified]
- FIXTURES ALL PASS: F-B0, F-B1 (3/3 hand-recomputed), F-B2, F-B3, F-B4a/b/c/d, F-B5a (re-run
  hash-IDENTICAL), F-B5b (3 hand-verified events per pair class), F-B5c (the copied kiss grammar
  is element-equal to census-2A's original), F-B6 (324 equivalences, 0 span mismatches), F-KEY
  dup=0 on all 35 cross cells and all three census-2A joins [verified]
- A 53-AGENT ADVERSARIAL REVIEW OF THIS PROGRAM RAISED FINDINGS AND A SECOND AGENT PER FINDING
  TRIED TO REFUTE EACH; NINE SURVIVED AND ALL NINE ARE FIXED. The one that mattered: the band
  grammar {enter, exit, reject} is defined entirely against `inside`, so a bar clearing the
  whole band in one move matched nothing and was dropped — 510,584 events, 18.4% of all band
  transitions, concentrated in the FAST cells. `traverse` is now its own class. NO FIXTURE IN
  THIS BUILD COULD HAVE CAUGHT IT: every one asked "is what we emitted correct", none asked "is
  a class missing" [verified]
- THE ENQUIRY CARD RETURNED A CLEAN NULL, AND IT IS NOT A FINDING. Conditioning FAST-ribbon
  crosses on VH+UH orientation: across all 18 strata (3 pairs x 3 orientations x 2 tfs) every
  median terminal-H100 sits INSIDE the measured toll band and %>0 stays within 47.9-50.1%. One
  measurement, one ruler, one horizon, m = 0. Promotion needs the Tier-P ceremony [verified]
- TWO STRUCTURAL OBSERVATIONS, REPORTED NOT FIXED, BOTH ABOUT THE PINNED CONSTANTS RATHER THAN
  THE TAPE: UH returns `flat` for 95.1% of warm bars against VH's 23.4% (k=20 is not scale-
  matched to lines spanning 1.18x in length); and 66-68% of VH knot episodes "expand" on the
  very next bar against 2.5-5.2% for UH, because a knot run ends precisely when width is rising.
  The constants are VETO by name and were NOT changed; the shares are printed as the evidence
  [verified]
- THE TOLL IN ATR UNITS IS TIMEFRAME-DEPENDENT and census-2A's 0.026-0.059 is a 4h figure. On 5m
  the same 10 bps round trip is 0.29-0.35 ATR. A first draft quoted the 4h number beside 5m
  tables and was corrected to measure the toll on each population's own bars [verified]
- 1m IS THE NAMED SKIP, AND THE BUDGET WAS RAM. This machine has 7.6 GB with ~0.8 GB free; a 1m
  cell is 3.65M bars, stage 2 ran at 57% CPU efficiency (paging) without finishing its first
  asset, and stage 3 needs ~1.2 GB peak per asset. Stages 3-5 never read 1m, so no table in the
  build document is affected; the 1m rows of the feasibility matrix are complete [verified]
- SEVEN DEFECTS IN THIS BUILD'S OWN MACHINERY, FOUND AND FIXED: a scoped run overwrote the
  feasibility matrix (now I12-merges); F-B1's sample was hardcoded and crashed on a scoped
  matrix; a killed run left a footer-less parquet the manifest recorded as valid (now atomic
  writes + a readability HALT); pin-merge resurrected that deleted artifact with its stale sha
  (now pruned); the manifest recorded rows: 0 for every artifact (now 15,807,077); it stamped the
  Tier-E tables as SUBSTRATE (now 9 carry the Tier-E class); and `--stage 34`, a missing
  comma, ran nothing and exited 0 [verified]
- BOX-COST: exchange/** was 2,137,089 B = 33.44%; this build adds 115,730 B to
  35.26%, above the contract's <1% target and well below the 40% REFUSE
  line. The overage is the two blocks the contract required verbatim — the 630-cell matrix and
  the full first-look transcript. All 1.71 GB of substrate is on D:, not one byte
  committed [verified]
PENDING (none blocks this contract):
1. THE V-ULT SLATE IS NOT WORDED. Per the paste, no registrations this build; the slate is
   written after the operator reads the first look. Owner: operator
2. `traverse` IS AN ADDITION TO A TAXONOMY THE CONTRACT CALLED "pared by design". Emitted as its
   own class and flagged for veto by name. Owner: operator
3. THE MISSING FIXTURE CLASS: nothing here asserts the event taxonomy is COMPLETE over the
   transitions it claims to cover. A partition check on `pos` would have caught the traverse gap
   on day one. Named, not retrofitted
4. 1m stages 2-4 remain unrun. `--stage 2,3,4 --tfs 1m` on a machine with headroom
5. Whether `k = 20` should be scale-matched per family is an OPERATOR question — changing a VETO
   constant is a ruling, not an edit
6. The annex (JTO/TAO) was not run; the contract made it optional and the budget went to 1m
7. Census-2A's cen4_book tranche_id defect (360 dups; the whole key is cell|tranche_id) is
   recorded but NOT repaired in census-2A's artifacts
NEXT: the operator reads §6 and words the V-ULT slate, rules on `traverse`, or rules on the k=20
scale-match. Owner: operator.
METRICS: operator actions this session = 1 (the CENSUS-2B V-ULT-1 paste) — files re-ingested = 0
=== END STATUS ===
```

