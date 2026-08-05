# BUILDER'S REPORT — ARGUS lane — CYCLE 6 (THE CLOSING CYCLE)

**Builder:** HEPHAESTUS · **Date:** 2026-08-06 · **Branch:** `v12-v1-census`
**HEAD at start:** `cbca19d` (the C5 publish)

Six items. Four built, two routed. **`PARITY NOT CERTIFIED` is down.**

---

## 0 · GATE

`branch == v12-v1-census` · pwd contains `\Users\` **and** OneDrive ·
`analytics/` present → **PASS**.

---

## 1 · ITEM 1 — MATURITY FLOORS, RULED

| | interim (R3) | **ruled** | basis |
|---|---|---|---|
| LINE | 10 | **16** | median per-bar move falls below `COLLAPSE_ATR` at 16 bars |
| BANDS | 30 | **60** | σ first carries half its eventual dispersion at 60 bars |
| rolling | none | **none** | `warming` already refuses a window shorter than its own span |

`ANALYTICS_VERSION` **1.4.0 → 1.5.0**. Registry membership genuinely changes —
a 30-bar anchor was admitted under the interim floor and is withheld under the
ruled one — so I-F requires the bump. F-B37 pins that exact case.

### 1.3 The withdrawn argument, and why it was wrong

The period-relative floor (`period/4`) was proposed on the grounds that a young
σ **inflates the σ-label** and so manufactures false reversion signals.

**The reasoning does not hold.** An anchored σ grows roughly as √t — but price's
**displacement from the anchored mean grows as √t as well**. Both accumulate the
same walk from the same anchor, so their ratio — the z-score — is approximately
**scale-free in time**.

**Verified on the operator's own captures**, same asset, same Month anchor:

| bar | bars | σ | z |
|---|---|---|---|
| 2026-08-02T04:00Z | 29 | 313.3966 | **+2.0136** |
| 2026-08-05T17:00Z | 114 | 583.3876 | **+1.9389** |

**σ grew +86.1%** (√(114/29) = 1.983 predicted, 1.861 observed) while **the
reading moved −3.7%**. A young band's **WIDTH** is age-dependent; its **READING**
is not. The defect the period-relative floor aimed at does not exist, and the
floors that remain are justified by **sampling noise alone**.

Recorded in `CONVENTIONS["anchored_vwap"]["withdrawn_period_relative_floor"]`
and `vwap.FLOOR_BASIS`. **F-B37 asserts the √t reasoning stays on the record** —
losing it invites the same proposal back next cycle.

### 1.4 Consequence, enforced

Band **widths** are comparable only at comparable **ages**. Age in bars now
prints beside σ in the stretch table and beside σ-in-ATR on the reversion board,
with the caveat stated where the widths actually sit side by side.

### ⚠ MEASURED CONSEQUENCE, reported because it is not small

The W anchor reopens Monday 00:00 UTC. Under the ruled floors:

| floor | withheld until | share of week |
|---|---|---|
| line 16 | Mon 16:00 UTC | 9.5% |
| **bands 60** | **Wed 12:00 UTC** | **35.7%** (was 17.9% under 30) |

Today is Wednesday and the W anchor carries **66 bars** — it cleared the 60-bar
floor about six hours before this capture. Estate-wide withheld count is **0**
because every other anchor is far past 60.

---

## 2 · ITEM 2 — THE DE-PEG LAYER

**Operator ruling, and it replaces bar count as the redundancy test.** An anchor
is not grown up when its estimator settles — it is grown up **when it unpegs
from the next-shorter anchor**. Early in a period the longer anchor is literally
measuring the same bars.

**Maturity and de-peg answer different questions and both are needed:**

| | question |
|---|---|
| maturity | is this estimator's **sample** deep enough to trust its width? |
| de-peg | is this anchor **saying anything** the shorter one is not? |

An anchor can be fully mature and perfectly redundant at the same time.

### The redundancy is STRUCTURAL

**January 1 anchors Year, Quarter AND Month simultaneously** — so Y=Q until
April 1 and Y=M until February 1, every year, every asset, unavoidably. **July 1
makes M=Q for the whole of July**, which is exactly what the operator's
2026-07-26 capture showed. Both cases are fixtured on real values.

### 2.1 / 2.2 What is recorded

Per adjacent anchored pair (W↔M, M↔Q, Q↔Y) and per anchored↔rolling counterpart
(W↔7d, M↔30d, Q↔90d, Y↔365d):

`peg_state` ∈ {identical, pegged, de-pegged} · `line_separation` in bps **and**
daily-ATR · `sigma_ratio` · `bars_since_depeg` · `bars_since_anchor` for **both**
sides.

`identical` is decided on the **anchor bar**, never on the values — two anchors
that merely coincide numerically today are a different fact from two that *are*
the same anchor. F-B44 asserts the distinction.

**Live on BTC today:** all three adjacent pairs de-pegged. On the 2026-07-26
capture, M↔Q reads `identical` with separation exactly 0.0000 ATR and σ ratio
1.000.

**The counterpart view carries the operator's point:** while an anchored VWAP is
warming, its rolling counterpart is **already fully formed** over the same span
of market memory — so that view is never missing. The separation between them is
itself information: calendar-anchoring versus trailing-window on the same
horizon.

### 2.3 Redundancy is PRINTED, not suppressed

Operator, verbatim intent: *"project the monthly anyway with that added
observation … We want to be aware of what is redundant and remain open to what
could be signal."*

A pegged or identical anchor still renders, carrying a `redundant_with` chip and
a plain-language line naming which anchor it duplicates and stating that a
de-peg is what makes it informative. It contributes **no independent score** —
`collapse_same_family` already merges the levels; this makes the merge
**visible**, exactly as `anchor_degeneracy` does for the exact-anchor case.

### 2.4 A de-peg is an EVENT

A pegged/identical → de-pegged transition is logged with both anchors' ages and
the separation at transition. Anti-vacuity fixtured both ways: no transition
means no event, and an unchanged state emits nothing.

---

## 3 · ITEM 3 — THE HINGE

**Operator's trader framing.** A σ band is a **hinge** with two outcomes:
(a) pullback / mean-reversion before continuation, or (b) genuine **rejection**
of the level, sending price to auction toward the dominant volume POC and the
far side of traded value. The archetype captured only (a).

### 3.1 Both targets, on every draft

| | target | meaning |
|---|---|---|
| **A** | the VWAP mean | the pullback case |
| **B** | dominant POC + opposing VA edge | the rejection case |

each with its own distance in ATR and its own R:R.

**⚠ DIRECTION — I got this backwards first and fixed it before committing.** A
SHORT reversion sits at an **upper** band; the trade is a move *down* to the
mean, so **rejection is price continuing UP**, toward the VAH. A LONG at a lower
band mirrors it: rejection continues *down*, toward the VAL. My first version
picked VAL for shorts and VAH for longs — precisely inverted. **F-B45 asserts
the two sides never choose the same edge**, which is the assertion the inverted
version fails.

### 3.2 No preference — and this is why the refusal is right

Measured on the live capture across the twelve drafts:

| | range |
|---|---|
| target-A R:R | **2.00 or 3.00** — a constant of the geometry |
| target-B R:R | **0.31 → 24.73** |

Choosing between them on the numbers available today would be choosing on noise.

Operator, verbatim: *"our reaction to the level depends on how price is
behaving, and this definitions are sensitive as they will carry into range
detection. So let's measure before we set these decisions in stone."*

**F-B45 enforces the refusal**: the target payloads are scanned for
`prefer / likely / probability / expected / recommend / better / primary / rank /
weight / confidence` and must contain none; the two outcomes are structural
**peers**, neither carrying a field the other lacks that would order them.
**Anti-vacuity:** the *drafts* are still ranked by band confluence score, so the
absence of ranking is a property of the **targets** specifically, not of the
board.

### 3.3 Hinge geometry recorded

Per draft: where the mean, the POC and the opposing VA edge sit relative to the
band, in ATR — so the census has targets to score against. The geometry blob is
scanned for outcome vocabulary and carries none. **Which** outcome occurred is
outcome data and stays census-side.

**Anti-vacuity:** with no formed volume window there is nothing to auction
toward, so target B is **absent** rather than fabricated from a shorter window
wearing a longer window's name.

---

## 4 · ITEM 4 — PARITY VERDICT: ALL 42 MATCH

Re-run **fresh against the live estate**, not quoted from cycle 5.

| | |
|---|---|
| rows compared at the operator's displayed precision | **42** |
| rows where `round(ours,1) != operator` | **0** |
| worst absolute delta | **0.0495** |
| worst \|bps\| | **0.0083** |

**(A) `2026-07-26T20:00Z`**

| anchor | bars | our VWAP | operator | worst \|Δ\| | our σ | implied σ |
|---|---|---|---|---|---|---|
| Week | 165 | 65190.810716 | 65190.8 | 0.0445 | 798.4663 | 798.47 |
| Month | 621 | 63334.048643 | 63334.0 | 0.0486 | 1729.9887 | 1729.95 |
| Quarter | 621 | 63334.048643 | 63334.0 | 0.0486 | 1729.9887 | 1729.95 |

**(B) `2026-08-02T04:00Z`**

| anchor | bars | our VWAP | operator | worst \|Δ\| | our σ | implied σ |
|---|---|---|---|---|---|---|
| Week | 149 | 63949.740172 | 63949.7 | 0.0408 | 754.4595 | 754.45 |
| Month | **29** ⚠ | 62926.056254 | 62926.1 | 0.0495 | 313.3966 | 313.37 |
| Quarter | 773 | 63461.819547 | 63461.8 | 0.0488 | 1608.6236 | 1608.63 |

Full per-level tables (ours full-precision, rounded, operator, delta, bps) are
in `exchange/reports/PARITY_C6_VERIFY_2026-08-06.txt`.

### 4.2 CONDITION MET — THE BANNER IS DOWN

`parity_certified` is set. `PARITY NOT CERTIFIED` appears **zero times** in the
rendered page; the standing provenance block appears **once**.

**Certification is not silence.** With the warning gone, the recipes that were
never chart-certified become the ones most likely to be mistaken for verified,
so both lists print on every page:

| | |
|---|---|
| **CERTIFIED** | `rolling_vwap` (1D 14/14, 1h 28/28) · `anchored_vwap` incl. σ (1h 42/42) · `vw_sigma_bands` (54 triples) · oscillators + `atr` (72/72) · `resample_ohlcv` (40/40) |
| **FIXTURE-VERIFIED, NOT chart-certified** ⚠ | `volume_profile` / `windowed_profile` · `low_volume_nodes` · `va_nesting` — permanent `approximation` chip |

**The profile family was excluded BY DESIGN, and the reason is recorded** so a
later cycle does not read the exclusion as an oversight and "fix" it: our
profile spreads each bar's volume uniformly across its range — a declared
approximation over klines. TradingView's is a *different* approximation over
data we do not have. Comparing them certifies nothing: agreement would be a
coincidence of two approximations, disagreement uninformative about either.

Scope travels with it: **BINANCE perpetuals, substrate 1h, source hlc3.**

F-B46 asserts both directions of the flip, that the un-certified list is named,
that the **reason** is stated, and that the two lists are disjoint.

**4.4** INTERFACE.md certification table updated; `analytics_sha` `ea5f02f2…`.

---

## 5 · FIXTURES

| id | asserts | tests |
|---|---|---|
| **F-B37** (updated) | ruled floors 16/60; 30-bar case now band-withheld; the √t reasoning stays recorded | 1 |
| **F-B44** | July M=Q identical and January Y=Q=M; three peg states distinct; redundancy printed not suppressed; de-peg transition is an event; rolling counterpart formed while anchor warms; no aggregation | 7 |
| **F-B45** | both targets present; **rejection direction not inverted**; no preference expressed; hinge geometry recorded without outcome data; no profile → no fabricated target B | 5 |
| **F-B46** | banner↔provenance flip both ways; un-certified list named with its reason; lists disjoint; instrument and substrate travel with it | 3 |

**Suite 271 → 286 passed, 1 skipped. Zero failures.** The one skip is
`fixtures/test_f8_journal.py:110`, pre-existing and unrelated.

---

## 6 · FILE DISPOSITION

| file | disposition | why | authorized |
|---|---|---|---|
| `analytics/__init__.py` | MODIFIED | 1.5.0; withdrawn-floor record in CONVENTIONS | `analytics/*` |
| `analytics/vwap.py` | MODIFIED | floors 16/60; `FLOOR_BASIS` | `analytics/*` |
| `analytics/INTERFACE.md` | MODIFIED | certification table, item 4.4 | `analytics/*` |
| `scripts/brief2.py` | MODIFIED | `depeg_layer`, hinge targets, `PARITY_PROVENANCE` | `scripts/*brief*` |
| `scripts/brief_render.py` | MODIFIED | de-peg card, hinge table, certified block, age columns | `scripts/*brief*` |
| `tests/test_brief2_confluence.py` | MODIFIED | F-B37 update, F-B44, F-B45 | `tests/*` |
| `tests/test_brief2_report.py` | MODIFIED | F-B46 | `tests/*` |
| `briefs/**` | REBUILT | certified capture + 4 partitions | `briefs/*` |
| `exchange/reports/**` | NEW | handback + parity artifact | `exchange/reports/*` |

**DO NOT MODIFY respected:** `engine/*`, `configs/*`, `study/*`,
`publish_exchange.py`, `reviewer_manifest.py`, `backup_estate.py`. Nothing under
`research_outputs/seq8*` touched (now gitignored since C5).

### Commits

```
5f52b15  item 1 — floors RULED 16/60; period-relative floor withdrawn
01870b6  item 2 — the DE-PEG layer; redundancy printed, not suppressed
8a0d8aa  item 3 — the HINGE: a second target on every reversion draft
6d11e9c  item 4 — ALL 42 MATCH; PARITY CERTIFIED, banner flipped down
```

---

## 7 · FIREWALL — UNCHANGED

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. Recording a de-peg is **OPS**; whether it marks
or precedes anything is **H-VDP**, census work under G-7. Recording hinge
geometry is OPS; **which** outcome occurred is census work. `depeg_layer`'s code
is scanned for outcome statistics and its **data** for predictive language.

**Certification changes the banner, not the firewall.** The numbers may now be
trusted as *arithmetic that matches the operator's charts*. Nothing about
whether any of it predicts anything has been established, and nothing here
claims otherwise.

— HEPHAESTUS, 2026-08-06
