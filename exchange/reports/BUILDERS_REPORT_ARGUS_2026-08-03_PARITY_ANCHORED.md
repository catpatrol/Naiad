# BUILDER'S REPORT — ARGUS lane — ANCHORED-VWAP BAND PARITY (addendum)

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Branch:** `v12-v1-census`
**Extends** ARGUS cycle-3 stage A.3. **MEASUREMENT ONLY** — no recipe changed, no
tolerance tuned, nothing fixed toward agreement.

---

## 0 · GATE

branch `v12-v1-census` · pwd contains `\Users\` + OneDrive · `analytics/`
present → **PASS**. Cycle 3 (stages A–D) had already run, so this is filed as an
addendum and folded into the same handback stream.

---

## 1 · THE OPERATOR'S READING

BTCUSDT.P, **1D chart**, candle 2026-08-02, chart TZ UTC. TradingView built-in
VWAP, Anchor Period presets, bands in **standard deviation** mode, multipliers
1/2/3.

| | VWAP | U1 | L1 | U2 | L2 | U3 | L3 |
|---|---|---|---|---|---|---|---|
| Month | 63,038.9 | 63,270.6 | 62,807.3 | 63,502.3 | 62,575.6 | 63,733.9 | 62,344.0 |
| Quarter | 63,505.6 | 65,036.1 | 61,975.1 | 66,566.5 | 60,444.7 | 68,097.0 | 58,914.2 |

Implied sigma: Month **231.65**, Quarter **1530.5**.

---

## 2 · SOURCE BARS (1D, auditable by hand)

| date | open | high | low | close | volume | hlc3 | ohlc4 |
|---|---|---|---|---|---|---|---|
| 2026-08-01 | 62,859.9 | 63,126.6 | 62,228.8 | 62,792.3 | 54,738.143 | 62,715.9000 | 62,751.9000 |
| 2026-08-02 | 62,792.3 | 63,779.0 | 62,782.3 | 63,550.0 | 84,040.407 | 63,370.4333 | 63,225.9000 |

---

## 3 · STEP 1 — VARIANCE DISCRIMINATOR

### 3.1 First pass, on our pinned `hlc3` — INCONCLUSIVE

| definition | Month sigma | miss vs 231.65 |
|---|---|---|
| (a) volume-weighted population | 319.8884 | **+38.09%** |
| (b) volume-weighted sample | 452.3906 | +95.29% |
| (c) unweighted population | 334.4822 | +44.39% |
| (d) unweighted sample | 473.0293 | +104.20% |

**No candidate was credible.** The cause was upstream: our Month VWAP *line* read
63,112.2671 against the operator's 63,038.9 — **+73.37 off**. A variance
definition cannot be discriminated while the mean it is measured about is
unmatched, because every candidate is dispersion *about that mean*.

### 3.2 Solving for the implied weighting

| | 08-01 | 08-02 |
|---|---|---|
| our volume weights | 0.3944 | 0.6056 |
| weights implied by 63,038.9 | **0.5065** | **0.4935** |

Near-equal weighting on volumes that are not near-equal → the discrepancy was in
the **source**, not the weighting. A sweep over
{hlc3, ohlc4, hl2, close} × {volume-weighted, equal} × {1D, 1h} isolated it.

### 3.3 Second pass, on `ohlc4` — DECISIVE

| definition | Month (n=2) sigma | miss | Quarter (n=33) sigma | miss |
|---|---|---|---|---|
| **(a) volume-weighted POPULATION** | **231.6568** | **+0.003%** | **1530.4690** | **+0.002%** |
| (b) volume-weighted SAMPLE (n−1) | 327.6122 | +41.43% | 1554.1986 | +1.55% |
| (c) unweighted population | 242.2253 | +4.57% | 1336.3731 | −12.68% |
| (d) unweighted sample | 342.5584 | +47.88% | 1357.0933 | −11.33% |

`(a)/(b)` ratio at n=2 measured **1.4142** — exactly √2, the separation the
two-bar anchor was chosen to produce. The Quarter anchor confirms weakly (1.55%
separation), as predicted.

---

## 4 · FULL BAND TABLE — ohlc4 / 1D / volume-weighted population

| anchor | level | ours | operator | delta | bps |
|---|---|---|---|---|---|
| MONTH | VWAP | 63,038.9411 | 63,038.9 | +0.0411 | +0.01 |
| | +1σ | 63,270.5980 | 63,270.6 | −0.0020 | −0.00 |
| | −1σ | 62,807.2843 | 62,807.3 | −0.0157 | −0.00 |
| | +2σ | 63,502.2548 | 63,502.3 | −0.0452 | −0.01 |
| | −2σ | 62,575.6275 | 62,575.6 | +0.0275 | +0.00 |
| | +3σ | 63,733.9116 | 63,733.9 | +0.0116 | +0.00 |
| | −3σ | 62,343.9707 | 62,344.0 | −0.0293 | −0.00 |
| QUARTER | VWAP | 63,505.5933 | 63,505.6 | −0.0067 | −0.00 |
| | +1σ | 65,036.0623 | 65,036.1 | −0.0377 | −0.01 |
| | −1σ | 61,975.1244 | 61,975.1 | +0.0244 | +0.00 |
| | +2σ | 66,566.5313 | 66,566.5 | +0.0313 | +0.00 |
| | −2σ | 60,444.6554 | 60,444.7 | −0.0446 | −0.01 |
| | +3σ | 68,097.0003 | 68,097.0 | +0.0003 | +0.00 |
| | −3σ | 58,914.1864 | 58,914.2 | −0.0136 | −0.00 |

**14 of 14 match. Max |delta| 0.0452, max 0.01 bps.**

---

## 5 · STEP 2 — SUBSTRATE DELTA

| anchor | level | 1D | 1h | 1D−1h | bps | ATR |
|---|---|---|---|---|---|---|
| MONTH | bars | **2** | **48** | | | |
| | VWAP | 63,038.9411 | 63,091.9665 | −53.03 | −8.4 | −0.032 |
| | +1σ | 63,270.5980 | 63,408.1612 | −137.56 | −21.7 | −0.083 |
| | +2σ | 63,502.2548 | 63,724.3558 | −222.10 | −34.9 | −0.135 |
| | +3σ | 63,733.9116 | 64,040.5504 | **−306.64** | −47.9 | **−0.186** |
| QUARTER | bars | **33** | **792** | | | |
| | VWAP | 63,505.5933 | 63,456.3830 | +49.21 | +7.8 | +0.030 |
| | −3σ | 58,914.1864 | 58,652.9623 | **+261.22** | +44.5 | **+0.158** |

Daily ATR 1,649.58. Same shape as the RVWAP substrate finding: largest where the
bar count is smallest. Feeds the same ruling (D3-1).

---

## 6 · STEP 3 — THE OBSCURED DIGIT

Our 2026-07-01-anchored VWAP, 1D/ohlc4 = **63,505.5933**.

| candidate | delta |
|---|---|
| 63,505.6 (built-in Quarter) | **−0.0067 → MATCHES** |
| 63,605.6 (the alternative reading) | −100.0067 |

**The obscured digit is 5.** The manual anchor and the built-in Quarter anchor
agree, as they must when both anchor at 2026-07-01T00:00Z. No discrepancy exists
there and none should be chased.

---

## 7 · STEP 4 — WARM-UP FINDING (report only)

**4.1 The predicate.** `scripts/daily_brief.py:406-407` — `vwap_series` returns
`(None, None)` **iff `len(d) == 0`**; assembled into the anchored block at
`:450-457`. It trips at **zero bars and nothing else. There is no
minimum-sample rule for anchored bands.**

**4.2 Bar counts, our 1h substrate, as-of 2026-08-03 20:00:**

| anchor | 1h bars | band levels | status |
|---|---|---|---|
| W | 21 | 6 | armed on a thin sample |
| M | 69 | 6 | armed |
| Q | 813 | 6 | armed |
| Y | 5,157 | 6 | armed |

**24 anchored band levels enter the confluence registry** (+4 VWAP lines). On a
1D chart the same anchors hold **1 / 2 / 33 / 214** bars — the Month's six bands
on **two data points** — and this recurs at every month, quarter and year start.

**4.3 Proposal, NOT implemented.** Require **≥ 30 bars on the 1h substrate**
before anchored **bands** emit; let the VWAP **line** print earlier with a
`thin_sample` chip. Rationale: it is the conventional floor at which a dispersion
estimate stops being dominated by its own sampling error; one number rather than
a per-anchor table; below every anchor except W on its first day. A VWAP line at
2 bars is still a true volume-weighted mean — a sigma at 2 bars is the spread
between two numbers.

---

## 8 · STEP 5 — MULTI-SCALE CROSS-CHECK

At price 63,653.2:

| anchor | VWAP | sigma | n | stretch |
|---|---|---|---|---|
| Month | 63,038.94 | 231.66 | **2** | **+2.65σ** |
| Quarter | 63,505.59 | 1,530.47 | 33 | **+0.10σ** |

**Reproduced exactly.** Same price, opposite stories — the multi-scale
disagreement the confluence engine exists to surface.

**Is the Month sigma worth printing at n=2?** The *line* yes; the *sigma* no. At
two bars the sigma is the spread between two numbers: arithmetically exact,
informationally empty as a dispersion estimate. "+2.65σ" reads as a strong
statement and is not one. This is precisely the case §4.3's proposal exists to
cover.

---

## 9 · FILE DISPOSITION

| file | disposition | why | tracked | pushed | fixture |
|---|---|---|---|---|---|
| `analytics/*` | **UNTOUCHED** | measurement cycle | yes | yes | F-AN-* |
| `scripts/daily_brief.py` | **UNTOUCHED** | read-only audit target | yes | yes | F-B1..8 |
| `scripts/brief2.py` | **UNTOUCHED** | — | yes | yes | F-B34/35 |
| `exchange/reports/PARITY_ANCHORED_2026-08-03.json` | NEW | 6,713 B, sha verified | yes | yes | — |
| `exchange/reports/BUILDERS_REPORT_…_PARITY_ANCHORED.md` | NEW | this file | yes | yes | — |
| `exchange/reports/SESSION_SUMMARY_…_PARITY_ANCHORED.md` | NEW | decision artifact | yes | yes | — |

**No source file was modified.** Suite unchanged at 230 passed / 1 skipped.

---

## 10 · FINDINGS

| id | finding | status |
|---|---|---|
| **DA-1** | anchored VWAP source is **ohlc4**, not `hlc3` | MEASURED, not applied — recipe change needs a ruling |
| **DA-2** | no minimum-sample rule for anchored bands; 24 band levels enter the registry, one anchor on a thin sample | REPORTED, proposal in §7 |
| **DA-3** | variance definition **verified** as volume-weighted population | ready to upgrade CONVENTIONS from INFERRED |
| **D3-1** | substrate question now spans rolling **and** anchored | still open |
| resolved | the 63,605.6 / 63,505.6 ambiguity | **63,505.6**; no discrepancy |

---

## 11 · FIREWALL

Not a signal service. Not sizing advice. Not study evidence. No engine change.
No fitted weights. No estate mutation.

Confluence measures **agreement between tools**, not edge. R:R measures
**geometry**, not probability. **Adoption remains gated on parity.**

— HEPHAESTUS, 2026-08-03
