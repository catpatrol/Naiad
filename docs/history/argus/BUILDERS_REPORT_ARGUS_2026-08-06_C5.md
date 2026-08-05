# BUILDER'S REPORT — ARGUS lane — CYCLE 5 (SHORT)

**Builder:** HEPHAESTUS · **Date:** 2026-08-06 · **Branch:** `v12-v1-census`
**HEAD at start:** `76981e4` (after the C4 publish `71cb2ab`)

Five items, all executed. Cycle 4 was not re-run.

---

## 0 · GATE

`branch == v12-v1-census` · pwd contains `\Users\` **and** OneDrive ·
`analytics/` present → **PASS**.

---

## 1 · ITEM 1 — `.gitignore`

Appended exactly the authorised comment plus two patterns. **Nothing else in
the file was touched** — the diff is `4 insertions(+), 0 deletions(-)`.

**One correction en route, disclosed:** the first write used Python's default
text mode, which on Windows converted the whole file LF→CRLF and produced a
`105 insertions / 101 deletions` diff. That would have rewritten every line of a
file I was authorised to append to. Rebuilt from the original bytes in binary
mode and amended before anything was pushed.

### Proof of effect

| | before | after |
|---|---|---|
| `git status --porcelain` entries | **13** | **12** (only addition is `.gitignore` itself) |
| `?? research_outputs/seq8/` | present | **gone** |
| `?? research_outputs/seq8_run2/` | present | **gone** |

```
git check-ignore -v research_outputs/seq8/seq8_outcomes.jsonl
  .gitignore:104:research_outputs/seq8/**

git check-ignore -v research_outputs/seq8_run2/seq8_cascades.jsonl
  .gitignore:105:research_outputs/seq8_run2/**

git add -A -n research_outputs   →  0 seq8 paths staged
```

**Still untracked and still visible, deliberately:** the five
`scripts/seq8_*.py`. The authorisation covered the two `research_outputs`
patterns only, and those are small source files that block nothing — unlike the
data, they are plausibly meant to be tracked by their own lane.

**OWED — a routing note to the SEQ8/DIONYSUS lane, via the operator:** their
bulk outputs are now ignored in this repo, and their scripts remain untracked.

---

## 2 · ITEM 2 — ANCHORED-BAND PARITY, 1h SUBSTRATE

### 2.1 RAW BAR CHECK — first, before any indicator

| bar | field | ours | operator | delta |
|---|---|---|---|---|
| **2026-07-26T20:00Z** | open | 64665.6000 | 64665.60 | **0.0000** |
| | high | 64676.2000 | 64676.20 | **0.0000** |
| | low | 64606.3000 | 64606.30 | **0.0000** |
| | close | 64621.3000 | 64621.30 | **0.0000** |
| | volume | 748.2680 | 748.27 | −0.0020 |
| **2026-08-02T04:00Z** | open | 63436.8000 | 63436.80 | **0.0000** |
| | high | 63600.0000 | 63600.00 | **0.0000** |
| | low | 63436.7000 | 63436.70 | **0.0000** |
| | close | 63557.1000 | 63557.10 | **0.0000** |
| | volume | 3013.8230 | "3.01K" (3 s.f.) | +3.8230 |

**All four prices match to every decimal on both bars.** Volumes agree at the
precision displayed. Nothing downstream inherits a bad input.

### 2.2 ALL 42 VALUES

Exact bar evaluated, both: `exact_candle_match = True`, substrate `1h`.

**(A) `2026-07-26T20:00Z` — VWAP Week**, anchor `2026-07-20T00:00Z`, 165 bars

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 65190.810716 | 65190.8 | 65190.8 | +0.0107 | +0.0016 |
| +1σ | 65989.276967 | 65989.3 | 65989.3 | −0.0230 | −0.0035 |
| −1σ | 64392.344465 | 64392.3 | 64392.3 | +0.0445 | +0.0069 |
| +2σ | 66787.743218 | 66787.7 | 66787.7 | +0.0432 | +0.0065 |
| −2σ | 63593.878214 | 63593.9 | 63593.9 | −0.0218 | −0.0034 |
| +3σ | 67586.209469 | 67586.2 | 67586.2 | +0.0095 | +0.0014 |
| −3σ | 62795.411963 | 62795.4 | 62795.4 | +0.0120 | +0.0019 |

**(A) VWAP Month AND Quarter** — anchor `2026-07-01T00:00Z`, 621 bars, **byte-identical to each other** (see §3.1)

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 63334.048643 | 63334.0 | 63334.0 | +0.0486 | +0.0077 |
| +1σ | 65064.037334 | 65064.0 | 65064.0 | +0.0373 | +0.0057 |
| −1σ | 61604.059952 | 61604.1 | 61604.1 | −0.0400 | −0.0065 |
| +2σ | 66794.026025 | 66794.0 | 66794.0 | +0.0260 | +0.0039 |
| −2σ | 59874.071262 | 59874.1 | 59874.1 | −0.0287 | −0.0048 |
| +3σ | 68524.014716 | 68524.0 | 68524.0 | +0.0147 | +0.0021 |
| −3σ | 58144.082571 | 58144.1 | 58144.1 | −0.0174 | −0.0030 |

**(B) `2026-08-02T04:00Z` — VWAP Week**, anchor `2026-07-27T00:00Z`, 149 bars

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 63949.740172 | 63949.7 | 63949.7 | +0.0402 | +0.0063 |
| +1σ | 64704.199673 | 64704.2 | 64704.2 | −0.0003 | −0.0001 |
| −1σ | 63195.280670 | 63195.3 | 63195.3 | −0.0193 | −0.0031 |
| +2σ | 65458.659175 | 65458.7 | 65458.7 | −0.0408 | −0.0062 |
| −2σ | 62440.821168 | 62440.8 | 62440.8 | +0.0212 | +0.0034 |
| +3σ | 66213.118677 | 66213.1 | 66213.1 | +0.0187 | +0.0028 |
| −3σ | 61686.361666 | 61686.4 | 61686.4 | −0.0383 | −0.0062 |

**(B) VWAP Month** — anchor `2026-08-01T00:00Z`, **29 bars ⚠ below the R3 band floor**

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 62926.056254 | 62926.1 | 62926.1 | −0.0437 | −0.0070 |
| +1σ | 63239.452901 | 63239.5 | 63239.5 | −0.0471 | −0.0074 |
| −1σ | 62612.659606 | 62612.7 | 62612.7 | −0.0404 | −0.0065 |
| +2σ | 63552.849549 | 63552.8 | 63552.8 | +0.0495 | +0.0078 |
| −2σ | 62299.262959 | 62299.3 | 62299.3 | −0.0370 | −0.0059 |
| +3σ | 63866.246197 | 63866.2 | 63866.2 | +0.0462 | +0.0072 |
| −3σ | 61985.866311 | 61985.9 | 61985.9 | −0.0337 | −0.0054 |

**(B) VWAP Quarter** — anchor `2026-07-01T00:00Z`, 773 bars

| level | ours (full) | rounded | operator | delta | bps |
|---|---|---|---|---|---|
| VWAP | 63461.819547 | 63461.8 | 63461.8 | +0.0195 | +0.0031 |
| +1σ | 65070.443136 | 65070.4 | 65070.4 | +0.0431 | +0.0066 |
| −1σ | 61853.195958 | 61853.2 | 61853.2 | −0.0040 | −0.0007 |
| +2σ | 66679.066724 | 66679.1 | 66679.1 | −0.0333 | −0.0050 |
| −2σ | 60244.572369 | 60244.6 | 60244.6 | −0.0276 | −0.0046 |
| +3σ | 68287.690313 | 68287.7 | 68287.7 | −0.0097 | −0.0014 |
| −3σ | 58635.948780 | 58635.9 | 58635.9 | +0.0488 | +0.0083 |

**WORST ABSOLUTE DELTA ACROSS ALL 42: 0.0495.** No pass/fail and no tolerance
asserted — the reviewer judges what counts as a match.

### 2.3 SYMMETRY AND IMPLIED σ

**All 18 triples exactly symmetric** — `midpoint − vwap = 0.00e+00` exactly — at
**exact integer multiples** of σ.

| capture | anchor | our σ | reviewer-implied | delta | bps |
|---|---|---|---|---|---|
| A | Week | 798.4663 | 798.47 | −0.0037 | −0.05 |
| A | Month = Quarter | 1729.9887 | 1729.95 | +0.0387 | +0.22 |
| B | Week | 754.4595 | 754.45 | +0.0095 | +0.13 |
| B | Month | 313.3966 | 313.37 | +0.0266 | +0.85 |
| B | Quarter | 1608.6236 | 1608.63 | −0.0064 | −0.04 |

### 2.4 CERTIFICATION TABLE UPDATED

`anchored_vwap` — σ on the 1h substrate: **UNVERIFIED → CERTIFIED**, 42/42.
The stale "STILL OPEN" prose block in INTERFACE.md was replaced, not annotated.

**Nothing in the VWAP family is now unverified.**

---

## 3 · ITEM 3 — TWO REAL-DATA BOUNDARY CASES

### 3.1 G7 ANCHOR DEGENERACY — capture (A)

July opens Q3, so Month and Quarter both anchor at `2026-07-01`. **All seven
levels are byte-identical, and so is σ** (1729.988691 both).

**Collapse verified on the real case: 14 raw levels → 7 members**, each with
`collapsed_count = 2`, each keeping both contributing labels so the merge stays
auditable.

Fourteen identical levels entering uncollapsed would have counted **one tool as
two agreeing voices** at every one of seven prices, in the family that already
contributes the most members.

**⚠ THE NOTE DID NOT PREVIOUSLY FIRE.** The collapse was correct but
**invisible** — only source comments mentioned it. `anchor_degeneracy()` now
reports coinciding anchors into the capture and the render prints them. A reader
seeing a 2-member cluster must be able to tell whether two tools agreed or one
tool was counted twice; those are opposite facts wearing the same shape.

**FOUND WHILE FIXTURING, recorded as its own case:** on the same bar the **Week
+2σ (66,787.75)** sits 6.28 from Month/Quarter +2σ (66,794.03) — inside the
32.57 collapse width — so the *full* capture merges **three**, not two. That is
not calendar degeneracy, but the scoring consequence is identical and correct.
The first version of the fixture asserted "exactly 2" against the full capture
and was **wrong**; it now tests the degeneracy in isolation and the three-way
merge separately.

### 3.2 MATURITY FLOOR — capture (B)

**Exact bar count: 29** (the brief said ~28). `line_ok=True`, `band_ok=False`.
The line prints with a `thin_sample` chip; **the six band levels are withheld
from the registry.**

| anchor | bars | σ | σ in daily ATR |
|---|---|---|---|
| Week | 149 | 754.4595 | **0.463** |
| **Month** | **29** | **313.3966** | **0.192** |
| Quarter | 773 | 1608.6236 | **0.988** |

**⚠ CORRECTION TO THE REVIEWER'S NOTE.** The arithmetic is exact — 313.40 is
41.5% of 754.46, well under half. **The word "backwards" is not.** At that bar
the **Week anchor was five days OLDER than the Month anchor** (149 bars vs 29),
so the developing Month was the **shorter** lookback and a smaller σ is
arithmetically **expected**, not anomalous. Calendar names invert against
calendar ages at the start of every month.

**The hazard is real anyway, and it is a PRESENTATION hazard rather than an
arithmetic one:** a level labelled "Month" printed narrower than one labelled
"Week" misleads any reader whose intuition says a month contains a week. That is
a sound justification for the chip and the floor — just not the one given.

Tested properly, **σ orders with an anchor's ACTUAL AGE in 93.4% of 5,294
comparisons**, so the estimator is sane.

Note the band VALUES are not wrong — they match the chart to 0.0495. They are
*arithmetically exact and informationally empty*, which is precisely the failure
a floor catches and a parity check never could.

---

## 4 · ITEM 4 — EXCURSION EPISODES

### 4.1 The C4 comparison is WITHDRAWN and REMOVED

C4 §5.3 compared time beyond ±1σ/±2σ/±3σ (~50 / ~9.5 / ~0.4%) to a normal
distribution's 31.7 / 4.6 / 0.27 and concluded the tails were "roughly double"
and a "2σ is rare" prior "wrong by a factor of two".

**Category error.** Those figures describe **independent draws**. Price relative
to a VWAP is a **persistent, autocorrelated** series — once beyond a band it
tends to *stay* there, because trending is what carried it there. A time-fraction
measures **persistence**, not tail fatness, and the conclusion does not follow.
Deleted from INTERFACE.md, with a fixture asserting it stays out.

### 4.2 Episodes — the decision-relevant unit

One entry beyond the band until price returns inside it is **one decision**,
however many bars it spans. Trailing 8,760 1h bars, ten assets:

| band | episodes / asset-window / year | median length | p90 length | median max \|z\| |
|---|---|---|---|---|
| ±2σ | **~122** (51–218) | **2 bars** | 8–28 | ~2.2σ |
| ±3σ | **~12** (2–26) | **1.5 bars** | 1–20 | ~3.2σ |

**2,436 σ2 episodes and 244 σ3 episodes** across 20 asset-windows in a year.

### 4.3 Firewall — unchanged, and now covered

**F-B38d** scans `episode_runs`' CODE for outcome statistics and additionally
forbids it looking **past** a run (`returned`, `revert`, `after`, `outcome`,
`target`, `exit`). One implementation in `brief_panel.episode_runs`; the
calibration imports it, so the fixture scans the code that actually ran.

Counting episodes is OPS. What fraction **revert**, any hit rate, any expectancy
— **H-VBR**, census work under G-7.

### 4.4 Effect on H-VBR's deflation gauge

**8.82% of bars is ~122 events a year, not 772 opportunities — and at σ3 it is
about twelve.** The baseline must be **per-episode**, and the usable sample is
far smaller than the bar fraction implies. **This RAISES the evidential bar
H-VBR must clear, not lowers it.**

---

## 5 · ITEM 5 — MATURITY STABILISATION

Three criteria tried. **Two rejected, and the rejections are the finding.**

| criterion | result | verdict |
|---|---|---|
| per-bar movement ("has it stopped changing") | line 16, bands **3** | **REJECTED** |
| convergence to the mature value | line 236, bands 231 | **REJECTED — circular** |
| fraction of mature value | see below | **basis of the proposal** |

**1 — per-bar movement is the wrong question for σ.** A volume-weighted
population variance over few bars is biased **low** and creeps upward, so it is
nearly motionless while badly wrong. Item 3.2 is the counter-example: at 29 bars
the estimate had "stabilised" 26 bars earlier by this test. **A 3-bar band floor
would be worse than the interim 30.**

**2 — convergence-to-mature is circular.** Distance to the 240-bar value is zero
*at* 240 by construction, so it reports the tracking horizon. And an anchored σ
converges to nothing: as price wanders from the anchor, dispersion-so-far
genuinely grows.

**3 — what the ratio actually shows**, non-circular. An anchored σ as a fraction
of its 240-bar value:

| bars | 10 | 30 | 60 | 120 | 180 |
|---|---|---|---|---|---|
| σ / mature | ~15% | **~33%** | **~50%** | ~77% | ~91% |

### PROPOSED — NOT APPLIED

```
line   >= 10 bars    UNCHANGED from R3
bands  >= 60 bars    RAISED from 30
```

Sixty is where σ first carries **half** the dispersion it ends with. Thirty is
one **third** — thin enough that the 2026-08-02 Month band printed at 0.19 ATR
beside a Week band at 0.46.

**No floor makes a developing anchor's σ "correct"**, because the quantity keeps
growing by construction. A floor can only decide how misleading a young band is
allowed to be before it stops being **scored**. That is a judgement about
presentation, not a fact recoverable from the data — which is why it is proposed
and not applied. **R3's 10/30 stand until the reviewer rules.**

**Rolling windows need no floor.** Every window is orders of magnitude inside
tolerance at steady state, and `warming` already refuses a window shorter than
its own span.

---

## 6 · FIXTURES

| id | asserts | tests |
|---|---|---|
| **F-B42** | July M=Q identity; 14→7 collapse with both labels kept; the note fires and names the calendar; anti-vacuity on non-degenerate anchors; the separate Week +2σ three-way merge | 4 |
| **F-B43** | 29-bar Month withholds six bands and prints the line; one more bar admits all seven; the σ ladder and its ordering | 2 |
| **F-B38d** | episode view computes no outcome statistic and never looks past a run; `episode_runs` correct on hand-built geometry; the withdrawn normal comparison stays out of INTERFACE.md | 3 |

**Suite 268 → 271 passed, 1 skipped. Zero failures.** The one skip is
`fixtures/test_f8_journal.py:110`, pre-existing and unrelated.

---

## 7 · FILE DISPOSITION

| file | disposition | why | authorized | verified |
|---|---|---|---|---|
| `.gitignore` | MODIFIED | item 1, 4 insertions only | **item 1 explicitly** | `check-ignore` |
| `analytics/INTERFACE.md` | MODIFIED | 2.4 certification; 3.2 floor justification; 4.1 removal | `analytics/*` | F-B38d |
| `scripts/brief2.py` | MODIFIED | `anchor_degeneracy()` + wiring | `scripts/*brief*` | F-B42 |
| `scripts/brief_render.py` | MODIFIED | degeneracy note printed | `scripts/*brief*` | suite |
| `scripts/brief_panel.py` | MODIFIED | `episode_runs()` | `scripts/*brief*` | F-B38d |
| `scripts/brief_episodes_c5.py` | NEW | item 4 measurement | `scripts/*brief*` | ran |
| `scripts/brief_maturity_c5.py` | NEW | item 5 measurement | `scripts/*brief*` | ran |
| `scripts/parity_c5_worksheet.py` | NEW | item 2 worksheet | ⚠ not a literal `*brief*` match — **disclosed** | ran |
| `tests/test_brief2_confluence.py` | MODIFIED | F-B42, F-B43 | `tests/*` | ran |
| `tests/test_brief2_report.py` | MODIFIED | F-B38d | `tests/*` | ran |

**DO NOT MODIFY respected:** `engine/*`, `configs/*`, `study/*`,
`publish_exchange.py`, `reviewer_manifest.py`, `backup_estate.py`,
`orchestrator_state.py`, and **nothing under `research_outputs/seq8*`** — those
26 files were neither read nor written, only ignored.

### Commits

```
d6cf09d  item 1 — gitignore SEQ8 bulk outputs (4 insertions, amended for LF)
765db4b  items 2+3 — anchored σ on 1h CERTIFIED; G7 degeneracy; maturity floor
ea837eb  items 4+5 — episodes replace the bar fraction; two floor criteria rejected
```

---

## 8 · FIREWALL — UNCHANGED

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Counting episodes is **OPS**; what fraction
revert is **census work under G-7**. **H-VBR** and **H-VBT** stay routed to
APOLLO with their deflation gauges stated in advance — item 4.4 tightens
H-VBR's.

`PARITY NOT CERTIFIED` still prints on every render. The VWAP family being fully
verified does not certify the instrument; that call is the operator's.

— HEPHAESTUS, 2026-08-06
