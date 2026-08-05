# ANCHORED-VWAP BAND PARITY — SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Reviewer:** ARGUS
**Addendum to ARGUS cycle 3, stage A.3.** Measurement only — no recipe changed,
no tolerance tuned, nothing fixed toward agreement.

---

## THE RESULT IN THREE LINES

1. **Our anchored VWAP used the wrong source.** It is **`ohlc4`**, not `hlc3`.
2. Once the source is corrected, **all 14 values match — 2 VWAPs and 12 bands,
   every one inside 0.05 (≤0.01 bps).**
3. **The variance definition we had only inferred is now VERIFIED**: volume-weighted
   **population**, one-pass, no (n−1) correction.

---

## §1 · WHAT THE DISCRIMINATOR ACTUALLY DID

Your design for this test was the right one, and it worked — but not on the
first pass, and the reason is worth stating.

Run against our pinned `hlc3`, **the test was inconclusive**: the closest of the
four variance definitions missed the operator's 231.65 by **38%**, and none was
credible. That was not a variance problem. Our Month VWAP *line* was **+73.37**
off, and **you cannot discriminate a variance definition while the mean it is
measured about is unmatched** — sigma is dispersion *about the mean*, so an
error in the mean contaminates all four candidates at once.

So I solved for what weights the operator's number implied: near-**equal**
weighting (0.5065 / 0.4935), against our volume weights of 0.394 / 0.606. That
pointed at the source rather than the weighting, and a sweep over
{hlc3, ohlc4, hl2, close} × {volume-weighted, equal} × {1D, 1h} landed on it:

| anchor | recipe | ours | operator | delta |
|---|---|---|---|---|
| MONTH | 1D / **ohlc4** / volume-weighted | 63,038.9411 | 63,038.9 | **+0.0411** |
| QUARTER | 1D / **ohlc4** / volume-weighted | 63,505.5933 | 63,505.6 | **−0.0067** |

**With the source corrected, the test became decisive on the very same data:**

| definition | Month (n=2) | Quarter (n=33) |
|---|---|---|
| **(a) volume-weighted POPULATION** | **+0.0068 → 0.003%** | **−0.031 → 0.002%** |
| (b) volume-weighted SAMPLE (n−1) | +95.96 → **+41.43%** | +1.55% |
| (c) unweighted population | +10.58 → +4.57% | −12.68% |
| (d) unweighted sample | +110.91 → +47.88% | −11.33% |

The two-bar Month anchor delivered exactly the **√2 = 41.4%** separation you
predicted, and (a) lands to **three decimal places**. The Quarter anchor confirms
it weakly, as you said it would.

**All 12 bands then match:** max |delta| 0.0452, max 0.01 bps.

---

## §2 · WHAT THIS CHANGES

`CONVENTIONS` has always flagged the anchored recipe honestly:

> *"same variance definition (INFERRED from shared band machinery, not read from
> source — flagged in the parity worksheet)"*

That caveat has now paid for itself twice over. **The inference was half right and
half wrong**, and only a reading could have told us which half:

- **variance definition — right**, and now *verified* rather than inferred
- **source — wrong.** `hlc3` was carried over from the rolling VWAP, where it is
  correct: cycle 3 proved rolling VWAP matches on `hlc3` to the cent. **The two
  TradingView indicators simply use different defaults.** That is not something
  reasoning could have produced; it had to be read off a chart.

---

## §3 · THE OTHER MEASUREMENTS

### Substrate delta (same question as RVWAP's D3-1)

| | Month | Quarter |
|---|---|---|
| bars, 1D vs 1h | **2 vs 48** | 33 vs 792 |
| VWAP line delta | −53.03 (−0.032 ATR) | +49.21 (+0.030 ATR) |
| worst band delta | −306.64 (**−0.186 ATR**) | +261.22 (+0.158 ATR) |

Same shape as the RVWAP finding: the substrate matters, and it matters most where
the bar count is smallest. This feeds the same operator ruling.

### The obscured digit — settled

Our 2026-07-01-anchored VWAP on 1D/ohlc4 is **63,505.5933**. It matches
**63,505.6** exactly and misses the alternative reading by **−100.0067** — a clean
digit misread in the hundreds place. **The manual anchor and the built-in Quarter
anchor agree, as they must.** No discrepancy there.

### Multi-scale disagreement — reproduced

At price 63,653.2: **+2.65σ** above the Month VWAP, **+0.10σ** above the Quarter.
Same price, opposite stories. This is exactly the disagreement the confluence
engine exists to surface — and exactly where a 2-bar sigma would mislead.

---

## §4 · FINDING — WARM-UP HONESTY DOES NOT COVER ANCHORED BANDS

**The warming predicate is `zero bars` and nothing else.**
`scripts/daily_brief.py:406-407` — `vwap_series` returns `(None, None)` iff
`len(d) == 0`; assembled at `:450-457`. There is **no minimum-sample rule**.

That is why the W anchor is suppressed (0 bars) and the M anchor is not.

Bar counts behind every anchored band on our 1h substrate, as of 2026-08-03 20:00:

| anchor | 1h bars | band levels | status |
|---|---|---|---|
| W | 21 | 6 | **armed on a thin sample** |
| M | 69 | 6 | armed |
| Q | 813 | 6 | armed |
| Y | 5,157 | 6 | armed |

**24 band levels enter the confluence registry**, and on a 1D chart the same
anchors would rest on **1 / 2 / 33 / 214** bars — the Month's six bands on **two
data points**. This recurs at the start of every month, quarter and year.

### Proposal — NOT implemented, yours to rule

**Require ≥ 30 bars on the 1h substrate before anchored BANDS emit; let the VWAP
LINE print earlier carrying a `thin_sample` chip.**

Why 30 and not something cleverer: it is the conventional floor at which a
dispersion estimate stops being dominated by its own sampling error, it is one
number rather than a per-anchor table, and it sits naturally below every anchor
except W in its first day. I would rather propose a defensible round number than
a tuned one — and per D-2, thresholds get re-ratified against the calibration
report anyway.

The line/band split matters: a VWAP line at 2 bars is still a true
volume-weighted mean. A *sigma* at 2 bars is the spread between two numbers —
arithmetically exact, informationally empty.

---

## §5 · DECISIONS

| id | decision | owner | note |
|---|---|---|---|
| **D3-1** (open) | which substrate the VWAP spec pins | reviewer | now spans rolling **and** anchored; both match on 1D |
| **DA-1** | adopt `ohlc4` for anchored VWAP | reviewer | measured, not applied — this is a recipe change and I do not make those unilaterally |
| **DA-2** | minimum-sample rule for anchored bands | reviewer | proposal in §4; not implemented |
| **DA-3** | upgrade the variance definition from INFERRED to VERIFIED in CONVENTIONS | reviewer | a documentation change that records a fact now established |

**I changed nothing.** `analytics/` and `scripts/` are untouched by this
addendum; the only new file is the parity record.

---

## §6 · PROVENANCE

`analytics` **1.3.0** · sha `da81034d…c731`. Record:
`exchange/reports/PARITY_ANCHORED_2026-08-03.json` (6,713 B).
Paired with `BUILDERS_REPORT_ARGUS_2026-08-03_PARITY_ANCHORED.md`.

**Firewall unchanged. Adoption still gated on parity — and Setup B is now
*closer* to certified, not certified: the anchored recipe needs a ruling before
it can be corrected.**

— HEPHAESTUS, 2026-08-03
