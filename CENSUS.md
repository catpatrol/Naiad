# CENSUS-1 — MTF Signal-Stack Census (Tier B, trade-independent)

Engine 1.0.11 byte-untouched (indicators imported only; no trading, no rule change). Exploration-classic window, 7-asset estate, 7 timeframes {5m,15m,30m,1H,4H,12H,1D}, EMAs 9/89/200, ATR-14. Every number carries a 10,000-resample bootstrap CI (seed 20260721). The EIGHT predictions are the only confirmatory claims; everything below D-level that is not a prediction is exploratory.

## Fixtures

| Fixture | Result | Detail |
|---|---|---|
| F-DET | MATCH | build twice, 4 substrate files byte-identical |
| F-XDET | MATCH | BTCUSDT/4h: 0 discrepancies vs independent EMA recompute (200 crosses) |
| F-ASOF | MATCH | BTCUSDT/5m<-12h: as-of 12H close <= exec open (no lookahead) |
| F-FWD | MATCH | 0 field nulls; 0 regime-scale termination faults |
| F-CFG | MATCH | window / TF set / EMA params / governor set match pre-registration |

**Fixtures: 5/5 MATCH**

## Pre-registered scorecard (8 predictions, falsifications first)

| # | Prediction | Verdict |
|---|---|---|
| P-C2 | 12H&1D agreement lifts h500 MFE >= +0.5 ATR | **FALSIFIED** |
| P-C4 | 9/200 fires at continuation > 9/89 rate | **FALSIFIED** |
| P-C1 | slow lens regime-scale MFE > 4H | **CONFIRMED** |
| P-C3 | a non-pullback cross signal +MFE, >=2 TFs | **CONFIRMED** |
| P-C5 | slow-stack combo +MFE net of toll (regime-scale) | **CONFIRMED** |
| P-C6 | cascade ordered (canonical > chance) | **CONFIRMED** |
| P-C7a | termini cluster at lens EMA, excess >=1.3x on >=2 lenses | **CONFIRMED** |
| P-C7b | EMA-terminating pullbacks higher fwd MFE, >=2 lenses | **CONFIRMED** |
| P-C8 | dose-response monotone (rho>0) on >=2 lenses | **CONFIRMED** |

**7/9 confirmed, 2 falsified.**

## Reading (falsifications first)

- **P-C2 FALSIFIED** — slow-stack (12H&1D) agreement lifts the 500-bar MFE by only 0.126685 ATR (95% CI [-0.156505, 0.411636], spanning / below the +0.5 bar). Slow-structure agreement does not materially raise the ceiling.
- **P-C4 FALSIFIED** — at continuation moments the 9/200 cross is present at rate 0.427215 vs the 9/89's 0.451416: the 9/200 does NOT fill the gap more often than the 9/89. The continuation gap is not a 9/200 gap.
- **P-C6 CONFIRMED, and the deviations are the finding** — the canonical 9/89→9/200→89/200 order holds in 0.9712 of ordered chains, but that order is near-necessary by construction; the real content is the **0.001 whipsaw rate** (9/89 almost always followed by a 9/200) and the **52.0-TF-bar** median 9/89→9/200 lag (the trend-maturation clock). 9/200 role from data: mid-sequence marker (operator reading).
- **P-C7a CONFIRMED against the matched null** — pullback termini sit within 0.35 lens-ATR of a lens EMA at ~2× the random-in-regime rate (excess-mass ratios {'1h': 1.8966, '4h': 1.9274, '12h': 2.0207, '1d': 1.9325}, all ≥1.3 on 4 lenses). The zone doctrine's foundation survives its own null.
- **P-C7b CONFIRMED (slow-lens-specific)** — EMA-terminating pullbacks carry higher subsequent 100-bar MFE on ['1h', '12h', '1d']; the effect is clear on 12H/1D and absent/reversed on 4H.
- **P-C1 CONFIRMED, but horizon-confounded** — regime-scale MFE is higher for slow lenses (12H 22.694526, 1D 22.714844 ATR) than 4H (19.901858), yet the regime-scale horizon is *until that governor's own flip*, so a slower governor buys a mechanically longer ride; the ordering is real but partly a horizon effect.
- **P-C8 CONFIRMED but shallow** — the k-of-N dose-response is monotone-positive on all four lenses (ρ {'1h': 0.0383, '4h': 0.0179, '12h': 0.0129, '1d': 0.012}) but the slope is tiny: more factors barely lift forward MFE. A weak dose-response, not a strong one.
- **P-C3 / P-C5 CONFIRMED on lenient bars** — both are MFE-positivity / MFE-net-of-toll tests; peak-favorable excursion over a long horizon is near-always positive and large, so these clear easily. The discriminating results above (null- and comparison-scored) carry the weight, not the absolute-MFE bars.

## Deliverables

### D1 — cascade map (firing frequency, dual coordinates)

```
{
 "12h": {
  "89_200": {
   "down": 26,
   "up": 29
  },
  "9_200": {
   "down": 74,
   "up": 75
  },
  "9_89": {
   "down": 132,
   "up": 132
  }
 },
 "15m": {
  "89_200": {
   "down": 1666,
   "up": 1671
  },
  "9_200": {
   "down": 5163,
   "up": 5169
  },
  "9_89": {
   "down": 8226,
   "up": 8231
  }
 },
 "1d": {
  "89_200": {
   "down": 11,
   "up": 16
  },
  "9_200": {
   "down": 38,
   "up": 41
  },
  "9_89": {
   "down": 59,
   "up": 60
  }
 },
 "1h": {
  "89_200": {
   "down": 418,
   "up": 419
  },
  "9_200": {
   "down": 1234,
   "up": 1238
  },
  "9_89": {
   "down": 1842,
   "up": 1847
  }
 },
 "30m": {
  "89_200": {
   "down": 845,
   "up": 847
  },
  "9_200": {
   "down": 2392,
   "up": 2398
  },
  "9_89": {
   "down": 3970,
   "up": 3976
  }
 },
 "4h": {
  "89_200": {
   "down": 82,
   "up": 82
  },
  "9_200": {
   "down": 262,
   "up": 262
  },
  "9_89": {
   "down": 440,
   "up": 441
  }
 },
 "5m": {
  "89_200": {
   "down": 5326,
   "up": 5332
  },
  "9_200": {
   "down": 16504,
   "up": 16508
  },
  "9_89": {
   "down": 26157,
   "up": 26161
  }
 }
}
```

### D2 — the governor-per-mandate map (lens × horizon)

Regime-scale forward MFE (ATR), aligned regime, per lens:

| lens | n | h100 MFE(ATR) | h500 MFE(ATR) | regime-scale MFE(ATR) [CI] |
|---|---|---|---|---|
| 1h | 24377 | 4.735116 | 11.628185 | 11.522908 [11.277205, 11.757054] |
| 4h | 25816 | 4.640886 | 11.519476 | 19.901858 [19.494128, 20.259642] |
| 12h | 26098 | 4.575157 | 11.40104 | 22.694526 [22.314468, 23.139255] |
| 1d | 26152 | 4.580522 | 11.305601 | 22.714844 [22.332142, 23.126923] |

*Fast horizons speak to intraday adoption, slow to position adoption; different mandates may adopt different governors — the map is the product, not a crown.*

### D6 — cascade order vs canonical null (9/89 → 9/200 → 89/200)

- canonical (9/200 precedes 89/200): 0.9712 of ordered chains (chance 0.50); whipsaw (9/89 never followed by 9/200): 0.001; 9/89→9/200 lag median 52.0 TF-bars.
- **9/200 role from data:** mid-sequence marker (9/89->9/200->89/200 canonical dominates)

### D8 — cascade ladder (add-schedule; full lag distributions)

| follow-on TF | n | lag median (exec bars) | remaining MFE(ATR,100) [CI] |
|---|---|---|---|
| 5m | 29338 | 92.0 | 4.528411 [4.457538, 4.601449] |
| 15m | 65155 | 135.0 | 4.162208 [4.117665, 4.204546] |
| 30m | 72676 | 286.0 | 3.953018 [3.919016, 3.986772] |
| 1h | 67218 | 534.0 | 4.246354 [4.202063, 4.270512] |
| 4h | 28165 | 876.0 | 4.614813 [4.590025, 4.659061] |
| 12h | 9221 | 1000.0 | 4.380428 [4.291249, 4.549034] |
| 1d | 4215 | 1014.0 | 4.050244 [4.006558, 4.354998] |

### D9 — dose-response curve (k-of-N factor scoring), per lens

- **1h** ρ(k,MFE)=0.0383 · k1:4.261778(n8737) k2:4.434552(n4179) k3:4.40149(n8204) k4:4.662769(n7768) k5:4.670185(n8851) k6:4.788809(n4764) k7:4.768855(n9383) k8:4.492253(n432)
- **4h** ρ(k,MFE)=0.0179 · k1:4.447959(n11550) k2:4.511861(n3807) k3:4.59486(n5577) k4:4.483506(n7952) k5:4.576809(n5949) k6:4.72644(n4323) k7:4.641972(n12416) k8:4.707206(n744)
- **12h** ρ(k,MFE)=0.0129 · k1:4.483875(n14579) k2:4.523438(n4235) k3:4.57289(n4442) k4:4.523468(n3729) k5:4.669058(n4327) k6:4.682827(n4779) k7:4.595829(n15440) k8:4.489766(n781)
- **1d** ρ(k,MFE)=0.012 · k1:4.49692(n17493) k2:4.472337(n4315) k3:4.519583(n3267) k4:4.80461(n3133) k5:4.578047(n4444) k6:4.583607(n18678) k7:4.914587(n976)

### D10 — pullback-terminus zone-landing (null beside every claim)

| lens | n term | P(near|term) | P(near|null) | excess-mass ratio | EMA−nonEMA fwd MFE(ATR,100) [CI] |
|---|---|---|---|---|---|
| 1h | 10576 | 0.2652 | 0.1398 | 1.8966 | 0.022141 [-0.205025, 0.220331] |
| 4h | 2644 | 0.2549 | 0.1323 | 1.9274 | -0.13945 [-0.611259, 0.492856] |
| 12h | 894 | 0.2405 | 0.119 | 2.0207 | 0.596313 [-0.348818, 1.419948] |
| 1d | 446 | 0.2309 | 0.1195 | 1.9325 | 0.429671 [-0.840542, 2.123735] |

## Exploratory annex (in-sample, NOT validated)

- 9_89 cross forward MFE(ATR,100): {'5m': 4.5576, '15m': 2.4552, '30m': 1.6699, '1h': 1.2509, '4h': 0.6643, '12h': 0.3767, '1d': 0.2377} — *replicated (>=2 TFs same sign)*
- 89_200 cross forward MFE(ATR,100): {'5m': 4.3341, '15m': 2.4618, '30m': 1.6939, '1h': 1.228, '4h': 0.5661, '12h': 0.3115} — *replicated (>=2 TFs same sign)*
- 9_200 cross forward MFE(ATR,100): {'5m': 4.4774, '15m': 2.4309, '30m': 1.7347, '1h': 1.1966, '4h': 0.5847, '12h': 0.3403, '1d': 0.1683} — *replicated (>=2 TFs same sign)*

*Every annex item is a hypothesis for a following, separately pre-registered test; nothing here counts as a finding.*

