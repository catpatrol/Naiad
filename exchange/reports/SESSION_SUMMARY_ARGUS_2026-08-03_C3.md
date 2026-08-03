# ARGUS CYCLE 3 — INTERIM SESSION SUMMARY

**Builder:** HEPHAESTUS · **Date:** 2026-08-03 · **Reviewer:** ARGUS
**Scope valve EXERCISED at end of stage D.** Stages E–G become cycle 4.

---

## HOW TO READ THIS

Read §1 first. **Three findings this cycle, and one of them is that I was wrong
in cycle 2.** Four decisions are requested at the end; two are genuinely open,
two are close to self-answering once you see the numbers.

Nothing here is adopted. `PARITY NOT CERTIFIED` still prints on every render.

---

## §1 · THE THREE THINGS THAT MATTER

### 1.1 The RVWAP disagreement is a SUBSTRATE question, not a recipe question

You gave readings taken on a **1D chart**. TradingView computes rolling VWAP from
whatever bars the chart is showing. Our spec pins **1h**. Those are different
quantities, and I computed both before saying anything.

| | 1d substrate vs you | 1h substrate vs you |
|---|---|---|
| BTC rv7 (Aug-02) | **−0.03** | −81.27 |
| BTC rv7 (Jun-30) | **−0.04** | **−840.37** |
| BTC rv30 / rv90 / rv365 | −0.05 / −0.01 / +0.01 | −53.67 / +11.01 / +17.13 |
| ETH, all four | **−0.00 to +0.00** | +3.64 / −1.41 / +0.18 / +0.22 |

**Computed on daily bars, our RVWAP reproduces your readings to the cent — all
twelve triples.** The recipe is right. The substrate is the entire difference,
and it is worth up to **0.377 daily-ATR** on the 7-day window.

The pattern is exactly what you would predict if substrate were the cause: the
gap is largest on the **shortest** window (rv7, where each bar carries the most
weight) and vanishes by rv365. That is corroboration, not coincidence.

**This is decision D3-1 and it is yours.** It is not a bug to fix; it is a
question about what the instrument should mean.

### 1.2 Anchored VWAP misses on BOTH substrates — a real, separate discrepancy

| | you | 1h | 1d |
|---|---|---|---|
| BTC anchM | 63,038.90 | +56.78 | +73.37 |
| BTC anchQ | 63,605.60 | **−145.59** | −80.33 |
| ETH anchM | 1,860.39 | +2.17 | +3.00 |
| ETH anchQ | 1,827.03 | −0.20 | +1.85 |

Substrate does not explain this one — neither column matches. ETH is close
(≤ 3.00 on ~1,860, i.e. ~16 bps); BTC's quarterly anchor is off by 145 points
(23 bps). Something differs in the anchor convention itself — most likely whether
the anchor bar is included, or where TradingView places the period boundary.

**I did not chase it.** It is a measurement cycle finding and the anchored **σ
band** recipe is separately flagged UNVERIFIED (inferred from shared band
machinery, never read from source; you have not captured anchored bands yet).
Both belong in the same next round.

### 1.3 I was wrong about storage in cycle 2 — and the correction is total

In cycle 2 I reported **1,584 MB/yr** against a 150–250 MB estimate and
recommended compressing captures. **You were right to challenge it: that figure
was working-tree bytes, which is not what a git repository grows by.**

I built the experiment: 30 synthesised daily captures, real structure, values
drifted ±1.5%, committed one per day, `git gc --aggressive`, pack measured before
and after. Then the same 30 gzipped.

| | working tree | git pack | pack / WT |
|---|---|---|---|
| 30 raw captures | 42.3 MB | **2.91 MB** | 6.9% |
| 30 gzipped | 5.1 MB | **5.07 MB** | 99.9% |

**Gzipping makes the repository 1.74× LARGER**, despite an 88% smaller working
tree. Git delta-compresses similar blobs and daily captures are near the ideal
delta case; pre-gzipping destroys exactly the redundancy git exploits.

**Projected annual, 3 slots/day:**

```
working-tree bytes (my cycle-2 figure)   1,543 MB/yr
ACTUAL git pack growth, raw                106 MB/yr   <-- the real number
git pack growth if gzipped                 185 MB/yr
§8.2 contract estimate                 150-250 MB/yr
```

**There was never a storage problem.** Raw is *inside* the original estimate. The
measurement vindicates §8.2 rather than overturning it, and my recommendation
would have made things worse.

---

## §2 · THE OTHER WORK

### Parity, Setup A: 72/72 again, and 40/40 raw bars

Ten candles this time. **All 40 OHLC fields identical.** Eight are resampled from
1h, so `resample_ohlcv` again matches TradingView's own aggregation — now
including the Jun-30 daily bar. All four of your cross-checks hold on our
numbers, including the three-way `58,605.40` identity.

Band symmetry: **24/24 triples exactly symmetric.**

### The registry was missing a third of itself

Two findings, both yours, both confirmed:

**The uniform 13 was a display cap.** `daily_brief.py:527` returns
`last_pivots(conf, vals, n=3)` — the three most recent highs and lows, written
for the report. 3+3 pivots + 4 priors + 4 period opens = exactly 13, identical
for every asset because the *cap* set the number, not the market. Worse:
`analytics.confirmed_pivots` — the causality-disciplined entry point §5.1 actually
names — was **never in the registry at all**. Now wired, on a trailing 180-day
lookback rather than a count cap, and pivot counts finally differ per asset.

**The weekly-anchor effect is real.** `anchored W: bars=0` on Monday 2026-08-03 —
3 armed anchors × 7 lines = 21, exactly as observed. With today's bars the W
anchor arms and it goes to 28. **The registry has a weekly cycle, smallest on
Mondays, and cycle 2's calibration was taken at the weekly minimum.**

Prior M/Q/Y anchors added (ruling D2-3a). Registry now:

| asset | before | after |
|---|---|---|
| BTCUSDT | 116 | **165** |
| ETHUSDT | 104 | **157** |
| LITUSDT | 93 | **126** |

### Invalidation now comes from structure

R-1 demoted to a caution chip as you ruled — excluding on a 0.03-ATR spread was
an arbitrary cut. Invalidation is now the far edge of the **next cluster beyond**
the entry cluster, so dense structure gives a tight stop and a void gives a wide
one. Spread widened 2.3× (0.073 vs 0.032). When nothing lies beyond, the draft
prints with **no R:R and a reason** rather than a fabricated stop.

---

## §3 · DECISIONS

### **D3-1 · Which substrate does the RVWAP spec pin?** *(the real one)*

| option | consequence |
|---|---|
| **(a) Keep 1h** | Higher-resolution volume weighting; arguably the better measurement. But the operator's chart will never agree, so every future parity check on RVWAP fails by design and the numbers are permanently un-cross-checkable against the tool he actually uses. |
| **(b) Switch to the plane's own bars** | RVWAP on the 1D plane uses daily bars, on the 4H plane 4h bars — matching TradingView exactly. Parity becomes checkable everywhere. Costs: the same window means different numbers on different planes, and the confluence registry must decide which plane feeds it. |
| **(c) Compute both, publish both** | Honest and maximally informative; near-doubles the RVWAP layer and the registry, and forces a choice anyway at scoring time. |

**My recommendation: (b).** The instrument exists to be read alongside his chart.
A number that can never be reconciled with the tool the operator actually uses is
worth less than a slightly coarser number that can. And (b) makes every future
RVWAP parity run meaningful instead of pre-failed.

### **D3-2 · Anchored VWAP — chase the convention now, or with the σ bands?**

Real discrepancy, unexplained by substrate, largest on BTC's quarterly anchor
(−145.59, 23 bps).

| option | consequence |
|---|---|
| **(a) Chase it now** | Isolates the anchor convention (bar inclusion / period boundary) while it is fresh. |
| **(b) Wait for the anchored σ-band readings** | One round that settles level *and* bands together. The band recipe is UNVERIFIED anyway, so it must be revisited regardless. |

**Recommendation: (b).** Two unverified things in one recipe should be settled
in one measurement, not two.

### **D3-3 · Storage — confirm no action**

Measured: raw is **106 MB/yr**, inside the §8.2 estimate; gzip would be 185 MB/yr.

**Recommendation: keep raw tracked JSON. Do nothing.** I am asking you to confirm
because I recommended the opposite last cycle and you should see that reversal
explicitly rather than find it in a commit message.

### **D3-4 · Recalibration timing** *(stage G, deferred)*

Every cycle-2 calibration number is now void: three families were empty, prior
anchors were missing, pivots were display-capped, and the measurement was taken
at the weekly registry minimum.

Also queued for stage G: **Item 6 re-bucketed.** Cycle 2's "a line moved on 20 of
20 sides" had a **median move of 0.127 ATR — below one cluster width (0.15)**.
Most of those "moves" were refinements within a cluster, not relocations. The
split is the honest headline and I should have made it the first time.

**Recommendation: recalibrate in cycle 4 after the render**, and — per your D-2
ruling — re-ratify no threshold until then.

---

## §4 · WHAT REMAINS (cycle 4)

- **Stage E** the render: `brief_render.py`, `brief_note.py`, chart planes, §4.2
  disjoint-pair prose, F-B10, F-B20
- **Stage F** `analytics/INTERFACE.md` regeneration; v1.1 retirement
- **Stage G** recalibration on the completed registry, with Item 6 re-bucketed

---

## §5 · PROVENANCE

`analytics` **1.3.0** · sha `da81034d…c731` · `rules_version` 2.0.0 ·
`schema_version` 2.1.0 · suite **230 passed / 1 skipped**.

Commits: `88f131b` (A) · `c2af5f0` (B) · `8d4806a` (C) · `95420eb` (D).

Records: `PARITY_C3_2026-08-03.json` (54,427 B) ·
`STORAGE_MEASUREMENT_2026-08-03.json` · paired with
`BUILDERS_REPORT_ARGUS_2026-08-03_C3.md`.

**Firewall unchanged.** Confluence measures agreement between tools, not edge.
R:R measures geometry, not probability. Adoption remains gated on parity, and
**Setup B is not certified** — the substrate question is open.

— HEPHAESTUS, 2026-08-03
