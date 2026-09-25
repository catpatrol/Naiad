as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · §0 VERDICTS — the nine registrations, ONE family (m = 9, bar 0.10/9 = 0.011111)

regbooks root: `research_outputs/tierc11/regbooks` · registry head `6772568b31fcfb2d…` (verified) · seed 20260924 (sensitivity 20260816) · n_boot 4000 · asset-cluster bootstrap (T5) · CI = 5th..95th percentile · p = (#draws <= 0 + 1)/(B + 1)

## §0 table

| # · registration · prior · scored arm · panel · era · ruler | n | point | 90% CI | verdict under its own text (with labels) | p · clears bar | LOAO | haircut twin | D15 |
|---|---|---|---|---|---|---|---|---|
| 1 · P-WARN-1 · 40% · scored (CONDITIONAL exit rule) · CLASSIC5 · full · paired | 200 (base 200) | +0.0056 | [-0.0092, +0.0217] | NOT SUPPORTED | 0.303424 · clears bar: no | 0/5 above (bar 3/5; short) · sens 0/5 above | +0.0056 [-0.0092, +0.0217] p 0.303424 | tail 1.0 · paired n 200 · max Δ share 1.8856 |
| 2 · P-AGE-1 · 50% · scored (admission gate (post-filter)) · CLASSIC5 · full · two_sample | 141 (base 200); refused n 59, mean -0.3840, ΣR -22.6566; ΣR scored +63.4641 vs base +40.8076 | +0.2461 | [+0.1912, +0.2967] | SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same 200 campaigns, anchored by F-CTRL(b))) | 0.000250 · clears bar: yes | 5/5 above (bar 3/5; clears) · sens 5/5 above | +0.2456 [+0.1902, +0.2970] p 0.000250 | tail 1.1999 · paired n 141 · max Δ share None |
| 3 · P-WIN-1 · 50% · scored (admission gate (post-filter)) · CLASSIC5 · full · two_sample | 137 (base 200); refused n 63, mean -0.1772, ΣR -11.1665; ΣR scored +51.9740 vs base +40.8076 | +0.1753 | [+0.0030, +0.3393] | NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, 56-bar decile -0.5796)) | 0.036491 · clears bar: no | 2/5 above (bar 3/5; short) · sens 2/5 above | +0.1753 [+0.0041, +0.3389] p 0.036491 | tail 1.118 · paired n 137 · max Δ share None |
| 4 · P-BRK-4H · 45% · scored (lane) · CLASSIC5 · full · vs_zero | 322 | +0.0503 | [-0.0920, +0.2081] | NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272)) · SCALE-IN-SAMPLE (holdout slice, derived: n 112, +0.2234 [-0.0715, +0.5555] p 0.087728; 1 of 112 of its campaigns carry a range read <= the era cut (in-sample; scale_in_sample, die_close_ms<=cut); filed tierE__holdout: n 112, +0.2234 [-0.0715, +0.5555] p 0.087728; frozen-3.0 twin tierE__frozen3: n 232, +0.1651 [+0.0584, +0.2776] p 0.000250; pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (63 of 322 campaigns on a changed asset)) | 0.318170 · clears bar: no | 0/5 above (bar 3/5; short) · sens 0/5 above | +0.0321 [-0.1091, +0.1892] p 0.389653 | — (vs zero: no base) |
| 5 · P-RELAY-1 · 45% · scored (trigger lane) · CLASSIC5 · full · two_sample | 173 (base 200) | +0.2496 | [-0.4412, +1.2600] | NOT SUPPORTED | 0.308423 · clears bar: no | 0/5 above (bar 3/5; short) · sens 0/5 above | +0.2468 [-0.4456, +1.2547] p 0.308423 | tail 1.5076 · paired n 0 · max Δ share None |
| 6 · P-SCALP-2 · 30% · scored (lane (range trade)) · CLASSIC5 · holdout · vs_zero | — | — | — | CLOSED BY PRECONDITION: CLOSED BY R2 (1h: FAIL) — report-only · no number · no slot spent · beside, Tier-E [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL) | — | — | — | — |
| 7 · P-ADD-BRK · 40% · scored (add rule) · CLASSIC5 · full · paired | 200 (base 200); ΣΔ -4.0367, Σ add_r -4.1173, absorbed funding +0.0806 (AM-3) | -0.0202 | [-0.0741, +0.0348] | NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0453 [-0.1479, +0.0446] p 0.780055; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0453 [-0.1479, +0.0446] p 0.780055; frozen-3.0 twin tierE__frozen3: n 200, +0.0179 [-0.0510, +0.0962] p 0.363909; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset)) | 0.730817 · clears bar: no | 0/5 above, 1/5 BELOW (bar 3/5; short) · sens 0/5 above, 1/5 BELOW | -0.0234 [-0.0778, +0.0322] p 0.730817 | tail 1.125 · paired n 200 · max Δ share 0.7501 |
| 8 · P-ADD-SFP · 40% · scored (add rule) · CLASSIC5 · full · paired | 200 (base 200); ΣΔ -3.9956, Σ add_r -3.9956, absorbed funding +0.0000 (AM-3) | -0.0200 | [-0.0314, -0.0070] | NOT SUPPORTED — CI wholly below zero · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0324 [-0.0619, -0.0029] p 1.000000; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0324 [-0.0619, -0.0029] p 1.000000; frozen-3.0 twin tierE__frozen3: n 200, -0.0034 [-0.0071, +0.0000] p 1.000000; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset)) | 1.000000 · clears bar: no | 0/5 above, 2/5 BELOW (bar 3/5; short) · sens 0/5 above, 2/5 BELOW | -0.0205 [-0.0321, -0.0072] p 1.000000 | tail 0.9911 · paired n 200 · max Δ share 0.2482 |
| 9 · P-TP-RNG · 35% · scored (exit rule) · CLASSIC5 · full · paired | 200 (base 200) | -0.0200 | [-0.0813, +0.0500] | NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0426 [-0.1563, +0.0737] p 0.727068; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; scale_in_sample_12h); filed tierE__holdout: n 77, -0.0426 [-0.1563, +0.0737] p 0.727068; frozen-3.0 twin tierE__frozen3: n 200, +0.0243 [-0.0132, +0.0600] p 0.148963; pick stability (12h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5, SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset)) | 0.743064 · clears bar: no | 0/5 above (bar 3/5; short) · sens 0/5 above | -0.0200 [-0.0813, +0.0500] p 0.743064 | tail 0.9486 · paired n 200 · max Δ share 1.1428 · named risk: the wall-exit lesson: P-WALL-1 (TC6) delta -0.0331, tail ratio 0.9329 — loses by cutting the tail |

## Family

m = 9 · q = 0.1 · bar = 0.10/9 = 0.011111 (exact 1/90) · tests spent 8 · SUPPORTED: P-AGE-1

| # | registration | status | verdict_of_record | spent a test | p | clears bar |
|---|---|---|---|---|---|---|
| 1 | P-WARN-1 | BUILT | NOT SUPPORTED | yes | 0.303424 | no |
| 2 | P-AGE-1 | BUILT | SUPPORTED | yes | 0.000250 | yes |
| 3 | P-WIN-1 | BUILT | NOT SUPPORTED | yes | 0.036491 | no |
| 4 | P-BRK-4H | BUILT | NOT SUPPORTED | yes | 0.318170 | no |
| 5 | P-RELAY-1 | BUILT | NOT SUPPORTED | yes | 0.308423 | no |
| 6 | P-SCALP-2 | CLOSED_BY_PRECONDITION | CLOSED_BY_PRECONDITION | no | — | — |
| 7 | P-ADD-BRK | BUILT | NOT SUPPORTED | yes | 0.730817 | no |
| 8 | P-ADD-SFP | BUILT | NOT SUPPORTED — CI wholly below zero | yes | 1.000000 | no |
| 9 | P-TP-RNG | BUILT | NOT SUPPORTED | yes | 0.743064 | no |

Law: m = 9 in every case; bar = 0.10/9 fixed, no ranks, no step-up; a registration closed by its own precondition or condition spends no test and never loosens the bar; a HALTed or ABSENT row spends no test [L-1.4]

## Detail blocks

### 1 · P-WARN-1 [40%]

Text of record (the contract's own lines):

```
 P-WARN-1 [40%, CONDITIONAL]: IF W2's "1h counter-12/89 before +1R" cohort's E[net] is below the
    base by a cluster-90% interval excluding zero, score the rule "exit at the 1h counter-12/89 close
    while pre-+1R" paired vs v6; ELSE report-only, no slot spent, stated.
```

- kind: CONDITIONAL exit rule · panel CLASSIC5 · era full · ruler paired · payload sha `c6121ba9330a40bd…`
- status: BUILT — condition MET: delta -0.728647, cluster-90% [-0.964287, -0.527794] (hi < 0); the rule book is the scored arm, paired vs v6
- verdict cell: NOT SUPPORTED
- condition record (SC-17, L-W.4): P-WARN-1/condition.json `41670c5ac533253a…` · met True · delta -0.728646908214193 · cluster-90% hi -0.5277942972642365 · agrees with STATUS BUILT
- scored arm: book_sha256 `956e15390419f8ab…` · n 200 · sum_net_r 41.92324273608339 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_w.py · description (builder's): the WARN rule book [L-W.5]: every v6 campaign walked on its 1h children (L-W.0); per child STOP -> +1R latch -> at the child's close, if pre-+1R and a counter EMA12/EMA89 1h cross closed: exit at that 1h close; v6's BELL / HARVEST / TRAIL at 4h closes unchanged; the set kept (paired); identity law on untouched campaigns [L-1.5]
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.807564574147555 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_w.py · description (builder's): card v6 over the TC11 corridor (the paired base: the same campaigns, v6's exits; exit_close_ms the 4h exit-bar close as books/v6_campaigns.parquet, exit_instant_ms 1h-resolved by the walked identity ride; net_r identical at 0.000e+00) [L-1.6, L-1.5]
- seed 20260924: point +0.005578 · CI [-0.009193, +0.021675] · p 0.303424 = 1214/4001 (draws <= 0: 1213 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.014704 (p <= bar iff > 0) · numpy's 1.111th percentile -0.014704
- seed 20260816 (sensitivity): point +0.005578 · CI [-0.009193, +0.021675] · p 0.288678 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 200 · sum R +41.923243 · mean R +0.209616 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): +0.005582 [-0.009181, +0.021672] p 0.303424 · sens +0.005582 [-0.009181, +0.021672] p 0.288678
- D15: n_paired 200, paired_delta_expectancy_r 0.005578, tail_exit_ratio 1.0, max_single_trade_delta_share 1.8856, unpaired_cell_n 0, unpaired_base_n 0
- premise: ruler paired, key_sets_identical True, n 200, n_base 200, identity {'acted_by_carried': True, 'unacted': 158, 'acted': 42, 'law': 'L-1.5 identity law held (exact) on every unacted campaign'}

LOAO (seed 20260924): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | +0.0080 | [-0.0104, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | +0.0083 | [-0.0104, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | +0.0006 | [-0.0136, +0.0206] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0010 | [-0.0136, +0.0139] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | +0.0121 | [-0.0034, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | +0.0080 | [-0.0104, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | +0.0083 | [-0.0104, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | +0.0006 | [-0.0136, +0.0148] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0010 | [-0.0136, +0.0107] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | +0.0121 | [-0.0034, +0.0278] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-WARN-1 (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1 | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.0135 | [-0.0098, +0.0345] | 0.150212 | CI includes zero | 1/5 above (bar 3) | +0.0135 [-0.0098, +0.0345] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0071 | [-0.0472, +0.0253] | 0.606598 | CI includes zero | 0/5 above (bar 3) | -0.0071 [-0.0472, +0.0253] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0071 | [-0.0472, +0.0253] | 0.606598 | CI includes zero | 0/5 above (bar 3) | -0.0071 [-0.0472, +0.0253] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.0135 | [-0.0098, +0.0345] | 0.150212 | CI includes zero | 1/5 above (bar 3) | +0.0135 [-0.0098, +0.0345] | — | TIER-E | a SELECTION, not a result | nothing |

### 2 · P-AGE-1 [50%]

Text of record (the contract's own lines):

```
 P-AGE-1 [50%] tide-age gate, TRAILING-quantile definition (refuse the OLD band) vs v6; the absolute
    definition (refuse age > 206 bars) printed as shadow.
```

- kind: admission gate (post-filter) · panel CLASSIC5 · era full · ruler two_sample · payload sha `e01a89ea7e6fda86…`
- status: BUILT — every arm built by scripts/tierc11_stage_g.py on the TC11 corridor (as of 2026-09-25T00:00:00Z); gates are post-filters of the v6 book [L-1.5]
- verdict cell: SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same 200 campaigns, anchored by F-CTRL(b)))
- pre_seen (full text): the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same 200 campaigns, anchored by F-CTRL(b)); point known before filing: gated n 141, +0.4567 vs +0.2087, delta ~ +0.2480 R; new information = the interval and campaigns entered after 2026-09-21T16:00Z (listed by count)
- pre_seen: new information = the interval and the campaigns entered after 2026-09-21T16:00Z: scored 0, base 0
- scored arm: book_sha256 `d008fa5086ce14f5…` · n 141 · sum_net_r 63.464130732724186 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_g.py · description (builder's): v6 minus the campaigns whose ENTRY-bar tide streak (tierc7_lab_regime.tide_streak) >= the trailing q75 edge (B4 OLD; tierc9._trailing_edges over CLASSIC5 4h bars with open <= the entry bar, >= 30 bars) [L-G.1]; a post-filter [L-1.5]
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.80756457414756 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_g.py · description (builder's): the v6 book [L-1.6]: TP.CONTROL_CARD + T9.V6_ROLES on CLASSIC5 over the full TC11 corridor (TP._book_sha f3c68f544bcda52c…, n 200); the two-sample comparison book
- seed 20260924: point +0.246062 · CI [+0.191190, +0.296656] · p 0.000250 = 1/4001 (draws <= 0: 0 of 4000) · clears bar True · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = +0.183133 (p <= bar iff > 0) · numpy's 1.111th percentile +0.183133
- seed 20260816 (sensitivity): point +0.246062 · CI [+0.190119, +0.296379] · p 0.000250 · reads SUPPORTED · stable across seeds: True
- books: scored n 141 · sum R +63.464131 · mean R +0.450100 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): +0.245569 [+0.190183, +0.296962] p 0.000250 · sens +0.245569 [+0.189830, +0.296407] p 0.000250
- D15: n_paired 141, paired_delta_expectancy_r 0.0, tail_exit_ratio 1.1999, max_single_trade_delta_share None, unpaired_cell_n 0, unpaired_base_n 59
- premise: ruler two_sample, key_sets_identical False, n 141, n_base 200, n_shared_keys 141, n_only_scored 0, n_only_base 59
- gate (post-filter): refused n 59 · mean -0.384010 · sum -22.656566 R · scored sum +63.464131 R (n 141) · base sum +40.807565 R (n 200) · added 0

LOAO (seed 20260924): 5/5 above · bar 3/5 · clears True · zero-campaign panels none · above excl. zero-campaign 5

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 116 | +0.2145 | [+0.1795, +0.2494] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 110 | +0.2643 | [+0.1844, +0.3201] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 112 | +0.2389 | [+0.1795, +0.2994] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 114 | +0.2585 | [+0.1949, +0.3169] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 112 | +0.2494 | [+0.1886, +0.3169] | True | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 5/5 above · bar 3/5 · clears True · zero-campaign panels none · above excl. zero-campaign 5

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 116 | +0.2145 | [+0.1769, +0.2397] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 110 | +0.2643 | [+0.1844, +0.3169] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 112 | +0.2389 | [+0.1769, +0.2942] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 114 | +0.2585 | [+0.1949, +0.3169] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 112 | +0.2494 | [+0.1886, +0.3169] | True | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-AGE-1 (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-AGE-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1523 | [+0.0031, +0.2970] | 0.044239 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.1516 [+0.0019, +0.2967] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 60 (base 77) | +0.3195 | [+0.2095, +0.4075] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3194 [+0.2099, +0.4068] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__holdout | two_sample | holdout | CLASSIC5 | 60 (base 77) | +0.3195 | [+0.2095, +0.4075] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3194 [+0.2099, +0.4068] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__refused_cohort | vs_zero | full | CLASSIC5 | 59 | -0.3840 | [-0.6211, -0.0904] | 0.981005 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.4034 [-0.6425, -0.1111] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__shadow_abs206 | two_sample | full | CLASSIC5 | 80 (base 200) | +0.4060 | [+0.0582, +0.8087] | 0.022744 | CI above zero (lo > 0) | 2/5 above (bar 3) | +0.4052 [+0.0577, +0.8063] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1523 | [+0.0031, +0.2970] | 0.044239 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.1516 [+0.0019, +0.2967] | — | TIER-E | a SELECTION, not a result | nothing |

### 3 · P-WIN-1 [50%]

Text of record (the contract's own lines):

```
 P-WIN-1 [50%] window-age gate: refuse triggers with arm→trigger lag ≥ 16 bars vs v6; lag 7–15
    printed as shadow cut.
```

- kind: admission gate (post-filter) · panel CLASSIC5 · era full · ruler two_sample · payload sha `d19a42a329be3bfe…`
- status: BUILT — every arm built by scripts/tierc11_stage_g.py on the TC11 corridor (as of 2026-09-25T00:00:00Z); gates are post-filters of the v6 book [L-1.5]
- verdict cell: NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, 56-bar decile -0.5796))
- selection_hazard (full text): direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, 56-bar decile -0.5796); P-LAG-1 on the same question NOT MET (delta +0.0616 [-0.7819, +0.9566]); the 16 cut has no on-disk provenance; v6 lag 7-15 holds 4/200, so >=16 ~ >=7
- scored arm: book_sha256 `fd3f407ad6b18670…` · n 137 · sum_net_r 51.97401862719062 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_g.py · description (builder's): v6 minus campaigns with lag = entry_i - arm_i >= 16 (4h bars) [L-G.2]; a post-filter [L-1.5]
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.80756457414756 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_g.py · description (builder's): the v6 book [L-1.6]: TP.CONTROL_CARD + T9.V6_ROLES on CLASSIC5 over the full TC11 corridor (TP._book_sha f3c68f544bcda52c…, n 200); the two-sample comparison book
- seed 20260924: point +0.175335 · CI [+0.002964, +0.339256] · p 0.036491 = 146/4001 (draws <= 0: 145 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.021314 (p <= bar iff > 0) · numpy's 1.111th percentile -0.021314
- seed 20260816 (sensitivity): point +0.175335 · CI [+0.002964, +0.336375] · p 0.038990 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 137 · sum R +51.974019 · mean R +0.379372 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): +0.175290 [+0.004141, +0.338882] p 0.036491 · sens +0.175290 [+0.004141, +0.335671] p 0.038990
- D15: n_paired 137, paired_delta_expectancy_r 0.0, tail_exit_ratio 1.118, max_single_trade_delta_share None, unpaired_cell_n 0, unpaired_base_n 63
- premise: ruler two_sample, key_sets_identical False, n 137, n_base 200, n_shared_keys 137, n_only_scored 0, n_only_base 63
- gate (post-filter): refused n 63 · mean -0.177245 · sum -11.166454 R · scored sum +51.974019 R (n 137) · base sum +40.807565 R (n 200) · added 0

LOAO (seed 20260924): 2/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 2

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 116 | +0.0926 | [-0.0941, +0.2036] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 101 | +0.1442 | [-0.0941, +0.3639] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 111 | +0.2358 | [+0.0454, +0.3836] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 114 | +0.2302 | [+0.0354, +0.3836] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 106 | +0.1613 | [-0.0941, +0.3700] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 2/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 2

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 116 | +0.0926 | [-0.0941, +0.2020] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 101 | +0.1442 | [-0.0941, +0.3639] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 111 | +0.2358 | [+0.0454, +0.3836] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 114 | +0.2302 | [+0.0539, +0.3836] | True | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 106 | +0.1613 | [-0.0941, +0.3700] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-WIN-1 (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WIN-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1098 | [-0.0640, +0.2651] | 0.157461 | CI includes zero | 0/5 above (bar 3) | +0.1102 [-0.0657, +0.2652] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 56 (base 77) | +0.2377 | [-0.0143, +0.3686] | 0.068483 | CI includes zero | 1/5 above (bar 3) | +0.2372 [-0.0146, +0.3681] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__holdout | two_sample | holdout | CLASSIC5 | 56 (base 77) | +0.2377 | [-0.0143, +0.3686] | 0.068483 | CI includes zero | 1/5 above (bar 3) | +0.2372 [-0.0146, +0.3681] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_admission | two_sample | full | CLASSIC5 | 147 (base 200) | -0.0740 | [-0.2061, +0.0674] | 0.808548 | CI includes zero | 0/5 above (bar 3) | -0.0776 [-0.2092, +0.0632] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_priority | two_sample | full | CLASSIC5 | 165 (base 200) | -0.0926 | [-0.2069, +0.0587] | 0.859035 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0956 [-0.2096, +0.0559] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__refused_cohort | vs_zero | full | CLASSIC5 | 63 | -0.1772 | [-0.5531, +0.2834] | 0.736566 | CI includes zero | 0/5 above (bar 3) | -0.1977 [-0.5730, +0.2616] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__shadow_lag7_15 | two_sample | full | CLASSIC5 | 196 (base 200) | +0.0158 | [+0.0017, +0.0310] | 0.026243 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.0158 [+0.0017, +0.0311] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1098 | [-0.0640, +0.2651] | 0.157461 | CI includes zero | 0/5 above (bar 3) | +0.1102 [-0.0657, +0.2652] | — | TIER-E | a SELECTION, not a result | nothing |

### 4 · P-BRK-4H [45%]

Text of record (the contract's own lines):

```
 P-BRK-4H [45%] the 4h breakout-retest lane: 4h macro death → first HOLD retest on the 89 tap (memory-
    line printed beside); stop beyond retest extreme railed 1.0 ATR(4h); tide aligned; v6 management;
    vs zero, five assets (seventeen Tier-E).
```

- kind: lane · panel CLASSIC5 · era full · ruler vs_zero · payload sha `120939d9d4a20929…`
- status: BUILT — P-BRK-4H's scored arm and seven Tier-E books (the registration's six tier_e_arms; the memory-line lane carries its engine one-shot twin as its own book) built over the TC11 corridor; no precondition or condition applies (vs zero, full corridor) [L-T.1]
- verdict cell: NOT SUPPORTED — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (selection_hazard: the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272)) · SCALE-IN-SAMPLE (holdout slice, derived: n 112, +0.2234 [-0.0715, +0.5555] p 0.087728; 1 of 112 of its campaigns carry a range read <= the era cut (in-sample; scale_in_sample, die_close_ms<=cut); filed tierE__holdout: n 112, +0.2234 [-0.0715, +0.5555] p 0.087728; frozen-3.0 twin tierE__frozen3: n 232, +0.1651 [+0.0584, +0.2776] p 0.000250; pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (63 of 322 campaigns on a changed asset))
- selection_hazard (full text): the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272); every era and asset was seen; the scored event (first-HOLD scan, tuning-calibrated scale) differs from the one-shot frozen-3.0 row that was selected
- scale_in_sample: SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are structurally in-sample (tuning-era calibration); the holdout-slice statistic and the frozen-3.0 twin are printed beside the verdict; pick stability printed [L-R.2]
- scored arm: book_sha256 `c76358dfaeb034dd…` · n 322 · sum_net_r 16.185338266900267 · era_scope full · ruler vs_zero · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_t_brk.py · description (builder's): P-BRK-4H scored arm: 4h macro death (calibrated 4h pick) -> the FIRST retest that HOLDS on tap-89 (1.0 ATR / 3 bars / ttl 400) -> entry at the touch+hold close, direction = the death direction; tide aligned at the entry bar's close; stop BK.brk_stop (retest extreme touch..entry -/+ 0.5 ATR, railed R >= 1.0 ATR(4h)); BK.ride_leg_l(ribbon=None) pure v6; one position per asset; CLASSIC5, full corridor, vs zero [L-T.1]
- seed 20260924: point +0.050265 · CI [-0.092025, +0.208080] · p 0.318170 = 1273/4001 (draws <= 0: 1272 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.140369 (p <= bar iff > 0) · numpy's 1.111th percentile -0.140369
- seed 20260816 (sensitivity): point +0.050265 · CI [-0.085154, +0.208080] · p 0.312422 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 322 · sum R +16.185338 · mean R +0.050265
- haircut twin (same ruler on haircut_net_r, AM-7): +0.032111 [-0.109107, +0.189190] p 0.389653 · sens +0.032111 [-0.102635, +0.189190] p 0.384904
- D15: — (vs zero: no base)
- premise: ruler vs_zero
- SCALE-IN-SAMPLE beside: holdout slice (derived) n 112, +0.2234 [-0.0715, +0.5555] p 0.087728 · in-sample range reads in it 1 of 112 (scale_in_sample, die_close_ms<=cut) · holdout arm tierE__holdout n 112, +0.2234 [-0.0715, +0.5555] p 0.087728 · frozen-3.0 twin tierE__frozen3 n 232, +0.1651 [+0.0584, +0.2776] p 0.000250
- pick stability (4h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on NEARUSDT 2.0->1.75 (63 of 322 campaigns on a changed asset) · record research_outputs/tierc11/ranges/SCALE_PICKS.json `cb5319c975e44df6…`

LOAO (seed 20260924): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 253 | +0.1204 | [-0.0303, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 262 | -0.0128 | [-0.1354, +0.1239] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 259 | +0.0030 | [-0.1354, +0.1782] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 267 | +0.0700 | [-0.1014, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 247 | +0.0736 | [-0.1014, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 253 | +0.1204 | [-0.0303, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 262 | -0.0128 | [-0.1354, +0.1092] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 259 | +0.0030 | [-0.1354, +0.1481] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 267 | +0.0700 | [-0.1014, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 247 | +0.0736 | [-0.1014, +0.2642] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-BRK-4H (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-BRK-4H | derived__slice_tuning | vs_zero | tuning | CLASSIC5 | 210 | -0.0421 | [-0.1756, +0.0452] | 0.688578 | CI includes zero | 0/5 above (bar 3) | -0.0593 [-0.1911, +0.0284] | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_holdout | vs_zero | holdout | CLASSIC5 | 112 | +0.2234 | [-0.0715, +0.5555] | 0.087728 | CI includes zero | 0/5 above (bar 3) | +0.2034 [-0.0912, +0.5370] | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__frozen3 | vs_zero | full | CLASSIC5 | 232 | +0.1651 | [+0.0584, +0.2776] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.1467 [+0.0390, +0.2585] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__holdout | vs_zero | holdout | CLASSIC5 | 112 | +0.2234 | [-0.0715, +0.5555] | 0.087728 | CI includes zero | 0/5 above (bar 3) | +0.2034 [-0.0912, +0.5370] | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_first_hold | vs_zero | full | CLASSIC5 | 186 | +0.3587 | [+0.0352, +0.7016] | 0.015996 | CI above zero (lo > 0) | 3/5 above (bar 3) | +0.3438 [+0.0212, +0.6847] | pick stability 4h: CHANGED on NEARUSDT (28 of 186 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_oneshot_flip | vs_zero | full | CLASSIC5 | 166 | +0.2940 | [+0.0482, +0.5041] | 0.025994 | CI above zero (lo > 0) | 2/5 above (bar 3) | +0.2793 [+0.0350, +0.4881] | pick stability 4h: CHANGED on NEARUSDT (28 of 166 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__oneshot_first_touch | vs_zero | full | CLASSIC5 | 289 | +0.0650 | [-0.0631, +0.2089] | 0.222444 | CI includes zero | 0/5 above (bar 3) | +0.0471 [-0.0807, +0.1935] | pick stability 4h: CHANGED on NEARUSDT (59 of 289 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__panel17 | vs_zero | full | PANEL17 | 762 | +0.1171 | [+0.0208, +0.2311] | 0.019995 | CI above zero (lo > 0) | 15/17 above (bar 9) | +0.0923 [-0.0030, +0.2039] | pick stability 4h: CHANGED on NEARUSDT (63 of 762 campaigns) · IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): HYPEUSDT 4h, PUMPUSDT 4h (26 of 762 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__tuning | vs_zero | tuning | CLASSIC5 | 210 | -0.0421 | [-0.1756, +0.0452] | 0.688578 | CI includes zero | 0/5 above (bar 3) | -0.0593 [-0.1911, +0.0284] | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |

### 5 · P-RELAY-1 [45%]

Text of record (the contract's own lines):

```
 P-RELAY-1 [45%] ["relay"]: 4h window open+armed; ENTRY on the 1h 9/12 with-trend close inside it;
    stop = 4h pivot railed, R on 4h; miss column first-class (windows the relay never activates);
    vs the 12/26-triggered base, two-sample.
```

- kind: trigger lane · panel CLASSIC5 · era full · ruler two_sample · payload sha `e8f6d4595b449a18…`
- status: BUILT — the relay book and its base / Tier-E arms were built on the TC11 corridor exactly as L-T.2 reads (no precondition or condition)
- verdict cell: NOT SUPPORTED
- scored arm: book_sha256 `57d8bbef8190492d…` · n 173 · sum_net_r 78.47972576227235 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_t_relay.py · description (builder's): P-RELAY-1 scored arm: the 1h EMA9/12 with-trend relay entered inside the armed v6 4h window strictly before min(trigger, counter 12/89, 89/316-against) [L-T.2]; stop struct_stop_4h as of the last closed 4h bar, railed 1.0 ATR, R on 4h; ridden by RD.relay11 (walk_after=True) and booked by tierc7._account_chain; CLASSIC5, full corridor; two-sample vs the base arm.
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.807564574147555 · era_scope full · ruler two_sample · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_t_relay.py · description (builder's): card v6 (the 12/26-triggered base): TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, CLASSIC5) over the full TC11 corridor (tierc11_books.v6_book); entry_ms is v6's; exit_close_ms is the exit bar's close (SR-7).
- seed 20260924: point +0.249602 · CI [-0.441195, +1.260010] · p 0.308423 = 1234/4001 (draws <= 0: 1233 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.576527 (p <= bar iff > 0) · numpy's 1.111th percentile -0.576527
- seed 20260816 (sensitivity): point +0.249602 · CI [-0.465504, +1.252919] · p 0.319420 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 173 · sum R +78.479726 · mean R +0.453640 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): +0.246759 [-0.445569, +1.254654] p 0.308423 · sens +0.246759 [-0.466897, +1.251203] p 0.319420
- D15: n_paired 0, paired_delta_expectancy_r None, tail_exit_ratio 1.5076, max_single_trade_delta_share None, unpaired_cell_n 173, unpaired_base_n 200
- premise: ruler two_sample, key_sets_identical False, n 173, n_base 200, n_shared_keys 0, n_only_scored 173, n_only_base 200

LOAO (seed 20260924): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 126 | +0.2881 | [-0.5940, +1.6734] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 140 | -0.2539 | [-0.5940, +0.0599] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 141 | +0.3496 | [-0.5066, +1.6566] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 140 | +0.4046 | [-0.4761, +1.6566] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 145 | +0.4640 | [-0.2584, +1.6566] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 126 | +0.2881 | [-0.5940, +1.0852] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 140 | -0.2539 | [-0.5940, +0.0599] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 141 | +0.3496 | [-0.5066, +1.0921] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 140 | +0.4046 | [-0.4761, +1.0921] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 145 | +0.4640 | [-0.2584, +1.0921] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-RELAY-1 (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-RELAY-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 114 (base 123) | +0.3273 | [-0.1806, +0.8305] | 0.163459 | CI includes zero | 1/5 above (bar 3) | +0.3246 [-0.1830, +0.8277] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 59 (base 77) | +0.1714 | [-1.1332, +1.8449] | 0.433642 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | +0.1679 [-1.1319, +1.8420] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__holdout_slice | two_sample | holdout | CLASSIC5 | 59 (base 77) | +0.1714 | [-1.1332, +1.8449] | 0.433642 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | +0.1679 [-1.1319, +1.8420] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__late_relay | two_sample | full | CLASSIC5 | 283 (base 200) | +0.2611 | [-0.0943, +0.7290] | 0.208198 | CI includes zero | 0/5 above (bar 3) | +0.2602 [-0.0950, +0.7268] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__miss_v6 | vs_zero | full | CLASSIC5 | 131 | +0.4118 | [+0.1487, +0.6555] | 0.001500 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3911 [+0.1299, +0.6330] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__tuning_slice | two_sample | tuning | CLASSIC5 | 114 (base 123) | +0.3273 | [-0.1806, +0.8305] | 0.163459 | CI includes zero | 1/5 above (bar 3) | +0.3246 [-0.1830, +0.8277] | — | TIER-E | a SELECTION, not a result | nothing |

### 6 · P-SCALP-2 [30%]

Text of record (the contract's own lines):

```
 P-SCALP-2 [30%] vs zero, five assets, holdout era, taker; the maker twin and the 17-asset view Tier-E.
```

- kind: lane (range trade) · panel CLASSIC5 · era holdout · ruler vs_zero · payload sha `c4e7ea0064bf0355…`
- status: CLOSED_BY_PRECONDITION — CLOSED BY R2 (1h: FAIL)
- verdict cell: CLOSED BY PRECONDITION: CLOSED BY R2 (1h: FAIL) — report-only · no number · no slot spent · beside, Tier-E [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL)
- precondition record (SC-17, L-S.1): research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json `82cc3ec6ddd588c9…` · R2 1h lens word of record FAIL · agrees with STATUS CLOSED_BY_PRECONDITION
- beside, Tier-E [§10] (tier TIER-E · a SELECTION, not a result · gates nothing): the tuning-era R2 1h word FAIL (holdout word of record FAIL) · research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json `82cc3ec6ddd588c9…`

### 7 · P-ADD-BRK [40%]

Text of record (the contract's own lines):

```
 P-ADD-BRK [40%]: add when a range ONE LENS BELOW the trade (1h for a 4h campaign) DIES in the trade's
    direction after +1R has been touched.
```

- kind: add rule · panel CLASSIC5 · era full · ruler paired · payload sha `510e67de50923baf…`
- status: BUILT — paired add book built on the v6 campaign set (n 200); the identity law held on every campaign without an add (148 unacted, 0.000e+00) and the key sets are identical
- verdict cell: NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0453 [-0.1479, +0.0446] p 0.780055; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0453 [-0.1479, +0.0446] p 0.780055; frozen-3.0 twin tierE__frozen3: n 200, +0.0179 [-0.0510, +0.0962] p 0.363909; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset))
- scale_in_sample: SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are structurally in-sample (tuning-era calibration); the holdout-slice statistic and the frozen-3.0 twin are printed beside the verdict; pick stability printed [L-R.2]
- scored arm: book_sha256 `15ba415b7a30f20f…` · n 200 · sum_net_r 36.77086452045925 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_a.py · description (builder's): P-ADD-BRK · scored: the registration's scored arm: v6 campaigns plus <= 2 adds of 0.5 unit at the 1h close of the rule's event (calibrated 1h scale), IN-TRADE and after the +1R latch, booked by tierc7._account_chain [L-A.1]
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.807564574147555 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_a.py · description (builder's): P-ADD-BRK · base: the v6 book (walked v6 ride, hooks off; identical to v6 at 0.000e+00), the paired comparison book [L-1.5, SA-4]
- seed 20260924: point -0.020184 · CI [-0.074066, +0.034787] · p 0.730817 = 2924/4001 (draws <= 0: 2923 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.080800 (p <= bar iff > 0) · numpy's 1.111th percentile -0.080199
- seed 20260816 (sensitivity): point -0.020184 · CI [-0.074127, +0.034787] · p 0.734816 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 200 · sum R +36.770865 · mean R +0.183854 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): -0.023361 [-0.077804, +0.032181] p 0.730817 · sens -0.023361 [-0.077825, +0.032181] p 0.734816
- D15: n_paired 200, paired_delta_expectancy_r -0.020184, tail_exit_ratio 1.125, max_single_trade_delta_share 0.7501, unpaired_cell_n 0, unpaired_base_n 0
- premise: ruler paired, key_sets_identical True, n 200, n_base 200, identity {'acted_by_carried': True, 'unacted': 148, 'acted': 52, 'law': 'L-1.5 identity law held (exact) on every unacted campaign'}
- adds (AM-3): ΣΔ -4.036700 · Σ add_r -4.117335 · absorbed funding +0.080635 (v6-leg absorption subtracted: True, from scored.v6_funding_absorbed_r) · residual -0.000000 · campaigns with adds 52 · AM-3: the paired delta is scored on net_r (tierc7._account_chain); delta == add_r is never asserted
- SCALE-IN-SAMPLE beside: holdout slice (derived) n 77, -0.0453 [-0.1479, +0.0446] p 0.780055 · in-sample range reads in it 0 of 77 (n_adds_scale_in_sample) · holdout arm tierE__holdout n 77, -0.0453 [-0.1479, +0.0446] p 0.780055 · frozen-3.0 twin tierE__frozen3 n 200, +0.0179 [-0.0510, +0.0962] p 0.363909
- pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset) · record research_outputs/tierc11/ranges/SCALE_PICKS.json `cb5319c975e44df6…`

LOAO (seed 20260924): 0/5 above, 1/5 BELOW · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0207 | [-0.0914, +0.0659] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | -0.0226 | [-0.0914, +0.0659] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0029 | [-0.0566, +0.0671] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0517 | [-0.0914, -0.0164] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0027 | [-0.0542, +0.0659] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above, 1/5 BELOW · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0207 | [-0.0914, +0.0458] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | -0.0226 | [-0.0914, +0.0499] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0029 | [-0.0566, +0.0499] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0517 | [-0.0914, -0.0164] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0027 | [-0.0542, +0.0659] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-ADD-BRK (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-ADD-BRK | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0045 | [-0.0945, +0.1259] | 0.581105 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0067 [-0.0960, +0.1234] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0453 | [-0.1479, +0.0446] | 0.780055 | CI includes zero | 0/5 above (bar 3) | -0.0499 [-0.1532, +0.0404] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | +0.0179 | [-0.0510, +0.0962] | 0.363909 | CI includes zero | 1/5 above (bar 3) | +0.0153 [-0.0531, +0.0924] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | paired | full | CLASSIC5 | 200 (base 200) | -0.0002 | [-0.0447, +0.0494] | 0.533117 | CI includes zero | 0/5 above (bar 3) | -0.0029 [-0.0472, +0.0469] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0453 | [-0.1479, +0.0446] | 0.780055 | CI includes zero | 0/5 above (bar 3) | -0.0499 [-0.1532, +0.0404] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_below_entry | paired | full | CLASSIC5 | 200 (base 200) | -0.0202 | [-0.0741, +0.0348] | 0.730817 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0234 [-0.0778, +0.0322] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | -0.0202 | [-0.0744, +0.0419] | 0.727318 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0231 [-0.0774, +0.0386] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0045 | [-0.0945, +0.1259] | 0.581105 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0067 [-0.0960, +0.1234] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |

### 8 · P-ADD-SFP [40%]

Text of record (the contract's own lines):

```
 P-ADD-SFP [40%]: add when a swing-failure CONFIRMS at the trend-side boundary of the 1h range (the
    deviation back into range in the trade's favour) after +1R.
```

- kind: add rule · panel CLASSIC5 · era full · ruler paired · payload sha `ed4acdfe532b8c13…`
- status: BUILT — paired add book built on the v6 campaign set (n 200); the identity law held on every campaign without an add (191 unacted, 0.000e+00) and the key sets are identical
- verdict cell: NOT SUPPORTED — CI wholly below zero · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0324 [-0.0619, -0.0029] p 1.000000; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; n_adds_scale_in_sample); filed tierE__holdout: n 77, -0.0324 [-0.0619, -0.0029] p 1.000000; frozen-3.0 twin tierE__frozen3: n 200, -0.0034 [-0.0071, +0.0000] p 1.000000; pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset))
- scale_in_sample: SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are structurally in-sample (tuning-era calibration); the holdout-slice statistic and the frozen-3.0 twin are printed beside the verdict; pick stability printed [L-R.2]
- scored arm: book_sha256 `ee2d19250f3e3d74…` · n 200 · sum_net_r 36.81196856626967 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_a.py · description (builder's): P-ADD-SFP · scored: the registration's scored arm: v6 campaigns plus <= 2 adds of 0.5 unit at the 1h close of the rule's event (calibrated 1h scale), IN-TRADE and after the +1R latch, booked by tierc7._account_chain [L-A.1]
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.807564574147555 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_a.py · description (builder's): P-ADD-SFP · base: the v6 book (walked v6 ride, hooks off; identical to v6 at 0.000e+00), the paired comparison book [L-1.5, SA-4]
- seed 20260924: point -0.019978 · CI [-0.031354, -0.007020] · p 1.000000 = 4001/4001 (draws <= 0: 4000 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.033632 (p <= bar iff > 0) · numpy's 1.111th percentile -0.033632
- seed 20260816 (sensitivity): point -0.019978 · CI [-0.031585, -0.007020] · p 1.000000 · reads NOT SUPPORTED — CI wholly below zero · stable across seeds: True
- books: scored n 200 · sum R +36.811969 · mean R +0.184060 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): -0.020472 [-0.032097, -0.007232] p 1.000000 · sens -0.020472 [-0.032475, -0.007232] p 1.000000
- D15: n_paired 200, paired_delta_expectancy_r -0.019978, tail_exit_ratio 0.9911, max_single_trade_delta_share 0.2482, unpaired_cell_n 0, unpaired_base_n 0
- premise: ruler paired, key_sets_identical True, n 200, n_base 200, identity {'acted_by_carried': True, 'unacted': 191, 'acted': 9, 'law': 'L-1.5 identity law held (exact) on every unacted campaign'}
- adds (AM-3): ΣΔ -3.995596 · Σ add_r -3.995596 · absorbed funding +0.000000 (v6-leg absorption subtracted: True, from scored.v6_funding_absorbed_r) · residual -0.000000 · campaigns with adds 9 · AM-3: the paired delta is scored on net_r (tierc7._account_chain); delta == add_r is never asserted
- SCALE-IN-SAMPLE beside: holdout slice (derived) n 77, -0.0324 [-0.0619, -0.0029] p 1.000000 · in-sample range reads in it 0 of 77 (n_adds_scale_in_sample) · holdout arm tierE__holdout n 77, -0.0324 [-0.0619, -0.0029] p 1.000000 · frozen-3.0 twin tierE__frozen3 n 200, -0.0034 [-0.0071, +0.0000] p 1.000000
- pick stability (1h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 2.0->1.75, SOLUSDT 2.0->1.75, NEARUSDT 2.0->1.75 (115 of 200 campaigns on a changed asset) · record research_outputs/tierc11/ranges/SCALE_PICKS.json `cb5319c975e44df6…`

LOAO (seed 20260924): 0/5 above, 2/5 BELOW · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0248 | [-0.0340, -0.0103] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | -0.0157 | [-0.0288, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0183 | [-0.0340, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0244 | [-0.0340, -0.0098] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0165 | [-0.0287, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above, 2/5 BELOW · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0248 | [-0.0340, -0.0141] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | -0.0157 | [-0.0288, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0183 | [-0.0340, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0244 | [-0.0340, -0.0136] | False | True |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0165 | [-0.0287, +0.0000] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-ADD-SFP (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-ADD-SFP | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0122 | [-0.0331, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0123 [-0.0334, +0.0000] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0324 | [-0.0619, -0.0029] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0335 [-0.0640, -0.0030] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | -0.0034 | [-0.0071, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0035 [-0.0074, +0.0000] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__head_to_head_vs_p_add_brk | paired | full | CLASSIC5 | 200 (base 200) | +0.0002 | [-0.0494, +0.0447] | 0.467133 | CI includes zero | 0/5 above (bar 3) | +0.0029 [-0.0469, +0.0472] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0324 | [-0.0619, -0.0029] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0335 [-0.0640, -0.0030] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_below_entry | paired | full | CLASSIC5 | 200 (base 200) | -0.0190 | [-0.0295, -0.0070] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0194 [-0.0302, -0.0072] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | -0.0154 | [-0.0251, -0.0043] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0157 [-0.0255, -0.0044] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0122 | [-0.0331, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0123 [-0.0334, +0.0000] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |

### 9 · P-TP-RNG [35%]

Text of record (the contract's own lines):

```
 P-TP-RNG [35%]: take-profit of the remainder at the approach (0.25 ATR) of the NEXT-HIGHER lens's range
    boundary (12h boundary for a 4h campaign) when that lens is IN-RANGE; if the lens above is in
    EXPANSION, no take-profit (let the trail run) — paired vs v6; the wall-exit lesson (tail cut) is the
    named risk and the D15 tail ratio is printed on the row.
```

- kind: exit rule · panel CLASSIC5 · era full · ruler paired · payload sha `ad12a44cd8aeb27c…`
- status: BUILT — the paired premise and the identity law held on every paired arm (key sets identical to v6, n 200; every campaign the TP never filled carries v6's net_r / exit_ms / exit_reason exactly); books only — no CI, no p, no verdict word [L-1.4, L-1.5]
- verdict cell: NOT SUPPORTED · SCALE-IN-SAMPLE (holdout slice, derived: n 77, -0.0426 [-0.1563, +0.0737] p 0.727068; 0 of 77 of its campaigns carry a range read <= the era cut (in-sample; scale_in_sample_12h); filed tierE__holdout: n 77, -0.0426 [-0.1563, +0.0737] p 0.727068; frozen-3.0 twin tierE__frozen3: n 200, +0.0243 [-0.0132, +0.0600] p 0.148963; pick stability (12h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5, SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset))
- scale_in_sample: SCALE-IN-SAMPLE: calibrated-scale range reads at instants <= the era cut are structurally in-sample (tuning-era calibration); the holdout-slice statistic and the frozen-3.0 twin are printed beside the verdict; pick stability printed [L-R.2]
- named risk: the wall-exit lesson: P-WALL-1 (TC6) delta -0.0331, tail ratio 0.9329 — loses by cutting the tail
- scored arm: book_sha256 `a10c667b26932948…` · n 200 · sum_net_r 36.81646971905991 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_h.py · description (builder's): P-TP-RNG scored arm: every v6 campaign re-ridden with a resting take-profit limit for the remainder at the 12h far boundary ∓ 0.25 ATR_12h when the 12h as-of state at the 4h bar's open is IN_RANGE (calibrated 12h pick), live only with the prior 4h close on the near side and the level > 10 bps beyond entry; fill max(level, open) / min(level, open); STOP -> TP -> BELL -> HARVEST -> TRAIL; v6 harvest kept [L-H.1]. Paired vs base on (symbol, entry_ms).
- base arm: book_sha256 `f41bfaf02b86dfb0…` · n 200 · sum_net_r 40.80756457414756 · era_scope full · ruler paired · entry bars straddling the era cut 0 · entered after the TC10 pin 0 · source scripts/tierc11_stage_h.py · description (builder's): the v6 book (card v6, V6_ROLES, CLASSIC5, full TC11 corridor) in the regbook schema — the pairing base [L-1.5, L-1.6].
- seed 20260924: point -0.019955 · CI [-0.081295, +0.049965] · p 0.743064 = 2973/4001 (draws <= 0: 2972 of 4000) · clears bar False · clusters 5
- deciding bound: the draw of rank 44 (ascending) of 4000 = -0.096865 (p <= bar iff > 0) · numpy's 1.111th percentile -0.096865
- seed 20260816 (sensitivity): point -0.019955 · CI [-0.080146, +0.049965] · p 0.723319 · reads NOT SUPPORTED · stable across seeds: True
- books: scored n 200 · sum R +36.816470 · mean R +0.184082 · base n 200 · sum R +40.807565 · mean R +0.204038
- haircut twin (same ruler on haircut_net_r, AM-7): -0.019965 [-0.081288, +0.049968] p 0.743064 · sens -0.019965 [-0.080156, +0.049968] p 0.723319
- D15: n_paired 200, paired_delta_expectancy_r -0.019955, tail_exit_ratio 0.9486, max_single_trade_delta_share 1.1428, unpaired_cell_n 0, unpaired_base_n 0
- premise: ruler paired, key_sets_identical True, n 200, n_base 200, identity {'acted_by_carried': True, 'unacted': 164, 'acted': 36, 'law': 'L-1.5 identity law held (exact) on every unacted campaign'}
- SCALE-IN-SAMPLE beside: holdout slice (derived) n 77, -0.0426 [-0.1563, +0.0737] p 0.727068 · in-sample range reads in it 0 of 77 (scale_in_sample_12h) · holdout arm tierE__holdout n 77, -0.0426 [-0.1563, +0.0737] p 0.727068 · frozen-3.0 twin tierE__frozen3 n 200, +0.0243 [-0.0132, +0.0600] p 0.148963
- pick stability (12h, first half of tuning vs tuning, CLASSIC5 [L-R.2]): CHANGED on BTCUSDT 1.75->2.0, ETHUSDT 2.0->1.5, SOLUSDT 1.75->2.25 (123 of 200 campaigns on a changed asset) · record research_outputs/tierc11/ranges/SCALE_PICKS.json `cb5319c975e44df6…`

LOAO (seed 20260924): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0076 | [-0.0795, +0.0613] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | +0.0143 | [-0.0318, +0.0633] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0279 | [-0.1005, +0.0613] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0267 | [-0.0979, +0.0591] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0496 | [-0.1005, +0.0110] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

LOAO sens (seed 20260816): 0/5 above · bar 3/5 · clears False · zero-campaign panels none · above excl. zero-campaign 0

| dropped | n | point | 90% CI | above | below | note | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 161 | -0.0076 | [-0.0687, +0.0613] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 152 | +0.0143 | [-0.0318, +0.0633] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 160 | -0.0279 | [-0.1005, +0.0613] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 164 | -0.0267 | [-0.0979, +0.0591] | False | False |  | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 163 | -0.0496 | [-0.1005, +0.0110] | False | False |  | TIER-E | a SELECTION, not a result | nothing |

Tier-E rows of P-TP-RNG (collared; no verdict word):

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-TP-RNG | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0058 | [-0.0395, +0.0298] | 0.606098 | CI includes zero | 0/5 above (bar 3) | -0.0058 [-0.0395, +0.0298] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0426 | [-0.1563, +0.0737] | 0.727068 | CI includes zero | 0/5 above (bar 3) | -0.0426 [-0.1563, +0.0738] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | +0.0243 | [-0.0132, +0.0600] | 0.148963 | CI includes zero | 1/5 above (bar 3) | +0.0243 [-0.0132, +0.0601] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0426 | [-0.1563, +0.0737] | 0.727068 | CI includes zero | 0/5 above (bar 3) | -0.0426 [-0.1563, +0.0738] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tp_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | +0.0019 | [-0.0082, +0.0108] | 0.360160 | CI includes zero | 1/5 above (bar 3) | +0.0019 [-0.0082, +0.0108] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0058 | [-0.0395, +0.0298] | 0.606098 | CI includes zero | 0/5 above (bar 3) | -0.0058 [-0.0395, +0.0298] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__unguarded | paired | full | CLASSIC5 | 200 (base 200) | -0.0200 | [-0.0815, +0.0500] | 0.743064 | CI includes zero | 0/5 above (bar 3) | -0.0201 [-0.0815, +0.0500] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |

## Tier-E rows — a SELECTION, not a result · gates nothing · no verdict word

56 rows, every one collared (tier / selection_not_a_result / gates); would_read_ci_only is the CI-only reading.

| registration | arm | ruler | era_scope | panel | n | point | 90% CI | p | would_read_ci_only | LOAO | haircut twin | scale (L-R.2) | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-WARN-1 | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.0135 | [-0.0098, +0.0345] | 0.150212 | CI includes zero | 1/5 above (bar 3) | +0.0135 [-0.0098, +0.0345] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0071 | [-0.0472, +0.0253] | 0.606598 | CI includes zero | 0/5 above (bar 3) | -0.0071 [-0.0472, +0.0253] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0071 | [-0.0472, +0.0253] | 0.606598 | CI includes zero | 0/5 above (bar 3) | -0.0071 [-0.0472, +0.0253] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WARN-1 | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | +0.0135 | [-0.0098, +0.0345] | 0.150212 | CI includes zero | 1/5 above (bar 3) | +0.0135 [-0.0098, +0.0345] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1523 | [+0.0031, +0.2970] | 0.044239 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.1516 [+0.0019, +0.2967] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 60 (base 77) | +0.3195 | [+0.2095, +0.4075] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3194 [+0.2099, +0.4068] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__holdout | two_sample | holdout | CLASSIC5 | 60 (base 77) | +0.3195 | [+0.2095, +0.4075] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3194 [+0.2099, +0.4068] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__refused_cohort | vs_zero | full | CLASSIC5 | 59 | -0.3840 | [-0.6211, -0.0904] | 0.981005 | CI wholly below zero (hi < 0) | 0/5 above, 5/5 BELOW (bar 3) | -0.4034 [-0.6425, -0.1111] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__shadow_abs206 | two_sample | full | CLASSIC5 | 80 (base 200) | +0.4060 | [+0.0582, +0.8087] | 0.022744 | CI above zero (lo > 0) | 2/5 above (bar 3) | +0.4052 [+0.0577, +0.8063] | — | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1523 | [+0.0031, +0.2970] | 0.044239 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.1516 [+0.0019, +0.2967] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1098 | [-0.0640, +0.2651] | 0.157461 | CI includes zero | 0/5 above (bar 3) | +0.1102 [-0.0657, +0.2652] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 56 (base 77) | +0.2377 | [-0.0143, +0.3686] | 0.068483 | CI includes zero | 1/5 above (bar 3) | +0.2372 [-0.0146, +0.3681] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__holdout | two_sample | holdout | CLASSIC5 | 56 (base 77) | +0.2377 | [-0.0143, +0.3686] | 0.068483 | CI includes zero | 1/5 above (bar 3) | +0.2372 [-0.0146, +0.3681] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_admission | two_sample | full | CLASSIC5 | 147 (base 200) | -0.0740 | [-0.2061, +0.0674] | 0.808548 | CI includes zero | 0/5 above (bar 3) | -0.0776 [-0.2092, +0.0632] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_priority | two_sample | full | CLASSIC5 | 165 (base 200) | -0.0926 | [-0.2069, +0.0587] | 0.859035 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0956 [-0.2096, +0.0559] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__refused_cohort | vs_zero | full | CLASSIC5 | 63 | -0.1772 | [-0.5531, +0.2834] | 0.736566 | CI includes zero | 0/5 above (bar 3) | -0.1977 [-0.5730, +0.2616] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__shadow_lag7_15 | two_sample | full | CLASSIC5 | 196 (base 200) | +0.0158 | [+0.0017, +0.0310] | 0.026243 | CI above zero (lo > 0) | 1/5 above (bar 3) | +0.0158 [+0.0017, +0.0311] | — | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__tuning | two_sample | tuning | CLASSIC5 | 81 (base 123) | +0.1098 | [-0.0640, +0.2651] | 0.157461 | CI includes zero | 0/5 above (bar 3) | +0.1102 [-0.0657, +0.2652] | — | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_tuning | vs_zero | tuning | CLASSIC5 | 210 | -0.0421 | [-0.1756, +0.0452] | 0.688578 | CI includes zero | 0/5 above (bar 3) | -0.0593 [-0.1911, +0.0284] | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | derived__slice_holdout | vs_zero | holdout | CLASSIC5 | 112 | +0.2234 | [-0.0715, +0.5555] | 0.087728 | CI includes zero | 0/5 above (bar 3) | +0.2034 [-0.0912, +0.5370] | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__frozen3 | vs_zero | full | CLASSIC5 | 232 | +0.1651 | [+0.0584, +0.2776] | 0.000250 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.1467 [+0.0390, +0.2585] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__holdout | vs_zero | holdout | CLASSIC5 | 112 | +0.2234 | [-0.0715, +0.5555] | 0.087728 | CI includes zero | 0/5 above (bar 3) | +0.2034 [-0.0912, +0.5370] | pick stability 4h: CHANGED on NEARUSDT (24 of 112 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_first_hold | vs_zero | full | CLASSIC5 | 186 | +0.3587 | [+0.0352, +0.7016] | 0.015996 | CI above zero (lo > 0) | 3/5 above (bar 3) | +0.3438 [+0.0212, +0.6847] | pick stability 4h: CHANGED on NEARUSDT (28 of 186 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__memline_oneshot_flip | vs_zero | full | CLASSIC5 | 166 | +0.2940 | [+0.0482, +0.5041] | 0.025994 | CI above zero (lo > 0) | 2/5 above (bar 3) | +0.2793 [+0.0350, +0.4881] | pick stability 4h: CHANGED on NEARUSDT (28 of 166 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__oneshot_first_touch | vs_zero | full | CLASSIC5 | 289 | +0.0650 | [-0.0631, +0.2089] | 0.222444 | CI includes zero | 0/5 above (bar 3) | +0.0471 [-0.0807, +0.1935] | pick stability 4h: CHANGED on NEARUSDT (59 of 289 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__panel17 | vs_zero | full | PANEL17 | 762 | +0.1171 | [+0.0208, +0.2311] | 0.019995 | CI above zero (lo > 0) | 15/17 above (bar 9) | +0.0923 [-0.0030, +0.2039] | pick stability 4h: CHANGED on NEARUSDT (63 of 762 campaigns) · IN-SAMPLE everywhere (whole-tape pick fallback [L-R.2]): HYPEUSDT 4h, PUMPUSDT 4h (26 of 762 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-BRK-4H | tierE__tuning | vs_zero | tuning | CLASSIC5 | 210 | -0.0421 | [-0.1756, +0.0452] | 0.688578 | CI includes zero | 0/5 above (bar 3) | -0.0593 [-0.1911, +0.0284] | pick stability 4h: CHANGED on NEARUSDT (39 of 210 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | derived__slice_tuning | two_sample | tuning | CLASSIC5 | 114 (base 123) | +0.3273 | [-0.1806, +0.8305] | 0.163459 | CI includes zero | 1/5 above (bar 3) | +0.3246 [-0.1830, +0.8277] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | derived__slice_holdout | two_sample | holdout | CLASSIC5 | 59 (base 77) | +0.1714 | [-1.1332, +1.8449] | 0.433642 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | +0.1679 [-1.1319, +1.8420] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__holdout_slice | two_sample | holdout | CLASSIC5 | 59 (base 77) | +0.1714 | [-1.1332, +1.8449] | 0.433642 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | +0.1679 [-1.1319, +1.8420] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__late_relay | two_sample | full | CLASSIC5 | 283 (base 200) | +0.2611 | [-0.0943, +0.7290] | 0.208198 | CI includes zero | 0/5 above (bar 3) | +0.2602 [-0.0950, +0.7268] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__miss_v6 | vs_zero | full | CLASSIC5 | 131 | +0.4118 | [+0.1487, +0.6555] | 0.001500 | CI above zero (lo > 0) | 5/5 above (bar 3) | +0.3911 [+0.1299, +0.6330] | — | TIER-E | a SELECTION, not a result | nothing |
| P-RELAY-1 | tierE__tuning_slice | two_sample | tuning | CLASSIC5 | 114 (base 123) | +0.3273 | [-0.1806, +0.8305] | 0.163459 | CI includes zero | 1/5 above (bar 3) | +0.3246 [-0.1830, +0.8277] | — | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0045 | [-0.0945, +0.1259] | 0.581105 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0067 [-0.0960, +0.1234] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0453 | [-0.1479, +0.0446] | 0.780055 | CI includes zero | 0/5 above (bar 3) | -0.0499 [-0.1532, +0.0404] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | +0.0179 | [-0.0510, +0.0962] | 0.363909 | CI includes zero | 1/5 above (bar 3) | +0.0153 [-0.0531, +0.0924] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | paired | full | CLASSIC5 | 200 (base 200) | -0.0002 | [-0.0447, +0.0494] | 0.533117 | CI includes zero | 0/5 above (bar 3) | -0.0029 [-0.0472, +0.0469] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0453 | [-0.1479, +0.0446] | 0.780055 | CI includes zero | 0/5 above (bar 3) | -0.0499 [-0.1532, +0.0404] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_below_entry | paired | full | CLASSIC5 | 200 (base 200) | -0.0202 | [-0.0741, +0.0348] | 0.730817 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0234 [-0.0778, +0.0322] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__refuse_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | -0.0202 | [-0.0744, +0.0419] | 0.727318 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0231 [-0.0774, +0.0386] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-BRK | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0045 | [-0.0945, +0.1259] | 0.581105 | CI includes zero | 0/5 above, 1/5 BELOW (bar 3) | -0.0067 [-0.0960, +0.1234] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0122 | [-0.0331, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0123 [-0.0334, +0.0000] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0324 | [-0.0619, -0.0029] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0335 [-0.0640, -0.0030] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | -0.0034 | [-0.0071, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0035 [-0.0074, +0.0000] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__head_to_head_vs_p_add_brk | paired | full | CLASSIC5 | 200 (base 200) | +0.0002 | [-0.0494, +0.0447] | 0.467133 | CI includes zero | 0/5 above (bar 3) | +0.0029 [-0.0469, +0.0472] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0324 | [-0.0619, -0.0029] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0335 [-0.0640, -0.0030] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (43 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_below_entry | paired | full | CLASSIC5 | 200 (base 200) | -0.0190 | [-0.0295, -0.0070] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0194 [-0.0302, -0.0072] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__refuse_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | -0.0154 | [-0.0251, -0.0043] | 1.000000 | CI wholly below zero (hi < 0) | 0/5 above, 2/5 BELOW (bar 3) | -0.0157 [-0.0255, -0.0044] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (115 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-ADD-SFP | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0122 | [-0.0331, +0.0000] | 1.000000 | CI includes zero | 0/5 above (bar 3) | -0.0123 [-0.0334, +0.0000] | pick stability 1h: CHANGED on BTCUSDT, SOLUSDT, NEARUSDT (72 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0058 | [-0.0395, +0.0298] | 0.606098 | CI includes zero | 0/5 above (bar 3) | -0.0058 [-0.0395, +0.0298] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | derived__slice_holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0426 | [-0.1563, +0.0737] | 0.727068 | CI includes zero | 0/5 above (bar 3) | -0.0426 [-0.1563, +0.0738] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__frozen3 | paired | full | CLASSIC5 | 200 (base 200) | +0.0243 | [-0.0132, +0.0600] | 0.148963 | CI includes zero | 1/5 above (bar 3) | +0.0243 [-0.0132, +0.0601] | frozen 3.0: no calibrated pick consumed | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__holdout | paired | holdout | CLASSIC5 | 77 (base 77) | -0.0426 | [-0.1563, +0.0737] | 0.727068 | CI includes zero | 0/5 above (bar 3) | -0.0426 [-0.1563, +0.0738] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (45 of 77 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tp_post_harvest | paired | full | CLASSIC5 | 200 (base 200) | +0.0019 | [-0.0082, +0.0108] | 0.360160 | CI includes zero | 1/5 above (bar 3) | +0.0019 [-0.0082, +0.0108] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__tuning | paired | tuning | CLASSIC5 | 123 (base 123) | -0.0058 | [-0.0395, +0.0298] | 0.606098 | CI includes zero | 0/5 above (bar 3) | -0.0058 [-0.0395, +0.0298] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (78 of 123 campaigns) | TIER-E | a SELECTION, not a result | nothing |
| P-TP-RNG | tierE__unguarded | paired | full | CLASSIC5 | 200 (base 200) | -0.0200 | [-0.0815, +0.0500] | 0.743064 | CI includes zero | 0/5 above (bar 3) | -0.0201 [-0.0815, +0.0500] | pick stability 12h: CHANGED on BTCUSDT, ETHUSDT, SOLUSDT (123 of 200 campaigns) | TIER-E | a SELECTION, not a result | nothing |

## F-BASE-IDENT

OK — checked ['P-ADD-BRK', 'P-ADD-SFP', 'P-AGE-1', 'P-RELAY-1', 'P-TP-RNG', 'P-WARN-1', 'P-WIN-1']; absent []; books/v6: n 200, content sha a5d0c57087c9b9bb… == manifest

| registration | base book_sha256 |
|---|---|
| P-ADD-BRK | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-ADD-SFP | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-AGE-1 | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-RELAY-1 | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-TP-RNG | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-WARN-1 | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| P-WIN-1 | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |

## Registry verification

contract `bb38e016a8f3e55c…` · LEANS `655e1605165e7a66…` · REGISTRATIONS.json `648834bf30e20e92…` · head `6772568b31fcfb2d…` == REGISTRY_PIN.json · 0 findings · LEANS_AMENDMENTS.md (binding, hashed) `b1c6275b5008fa68…`

Records read beside the regbooks (plain JSON): r2_lens_verdicts research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json `82cc3ec6ddd588c9…` · scale_picks research_outputs/tierc11/ranges/SCALE_PICKS.json `cb5319c975e44df6…`

| seq | registration | text lines | re-cut == text | payload sha | chain line sha |
|---|---|---|---|---|---|
| 1 | P-WARN-1 | 40-42 | True | c6121ba9330a40bd… | 0db9a7e9d337ff55… |
| 2 | P-AGE-1 | 45-46 | True | e01a89ea7e6fda86… | cb05950509bae39e… |
| 3 | P-WIN-1 | 47-48 | True | d19a42a329be3bfe… | f324eefccc49d843… |
| 4 | P-BRK-4H | 52-54 | True | 120939d9d4a20929… | 627442c219dcb587… |
| 5 | P-RELAY-1 | 55-57 | True | e8f6d4595b449a18… | b1c9e3a04fbd59db… |
| 6 | P-SCALP-2 | 71-71 | True | c4e7ea0064bf0355… | c0e48c4cf4b6566d… |
| 7 | P-ADD-BRK | 75-76 | True | 510e67de50923baf… | cca5ef44ae93ccc1… |
| 8 | P-ADD-SFP | 77-78 | True | ed4acdfe532b8c13… | de17cd2bf73d1b29… |
| 9 | P-TP-RNG | 83-86 | True | ad12a44cd8aeb27c… | 6772568b31fcfb2d… |

## Readings (sub-readings of the scorer)

- [LEAN-HEPHAESTUS] L-1.4 rulers from the SPEC (paired: P-WARN-1, P-ADD-BRK, P-ADD-SFP, P-TP-RNG · two-sample: P-AGE-1, P-WIN-1, P-RELAY-1 · vs zero: P-BRK-4H, P-SCALP-2); T5.cluster_boot / cluster_boot_diff / _ci_from, asset clusters, seed 20260924 (20260816 beside), n_boot 4000 passed explicitly
- [LEAN-HEPHAESTUS] L-1.4 verdict_of_record = SUPPORTED iff ci_lo > 0 AND p <= 0.10/9, else NOT SUPPORTED ('— CI wholly below zero' when ci_hi < 0); m = 9 in every case
- [LEAN-HEPHAESTUS] SC-1 clause (b) exact: p = (k+1)/(B+1) <= 1/90 <=> 90(k+1) <= B+1; deciding bound = the floor((B+1)/90)-th smallest finite draw (44th of 4000); numpy's 1.111th percentile beside
- [LEAN-HEPHAESTUS] SC-2 LOAO = TP.loao_n's law keyed (symbol, entry_ms): N = declared panel, unbootstrappable panel counts against, above-only, bar ceil((N+1)/2); decides nothing
- [LEAN-HEPHAESTUS] SC-3 Tier-E paired / two-sample arm: vs the registration's base restricted to its era_scope, or the sidecar's optional base_arm
- [LEAN-HEPHAESTUS] SC-4 SCALE-IN-SAMPLE: holdout slice derived from the scored arm (a tierE 'holdout*' arm beside); frozen-3.0 twin = tierE arm slugged '*frozen*'; the holdout campaigns whose range read fell <= the era cut counted beside
- [LEAN-HEPHAESTUS] SC-5 refused cohort = base keys absent from the scored arm; 'on per-campaign expectancy only; the gate forfeits +X R total' iff mean(refused) > 0
- [LEAN-HEPHAESTUS] SC-6 two-sample on identical key sets: FLAGGED, not halted
- [LEAN-HEPHAESTUS] SC-7 F-BASE-IDENT: one book_sha256 across the base arms AND equal to books/v6_campaigns.parquet on 13 columns at its 6 dp; a row halts if its base fails v6 or the v6-equal bases split
- [LEAN-HEPHAESTUS] SC-8 honesty <hazard> = '<key>: <text up to its first top-level ;>'
- [LEAN-HEPHAESTUS] SC-9 Tier-E: would_read_ci_only in {CI above zero (lo > 0) | CI includes zero | CI wholly below zero (hi < 0) | no interval}; collar tier/selection_not_a_result/gates
- [LEAN-HEPHAESTUS] SC-10 registry mismatch halts the scorer before any write; a book / premise / identity failure halts its row only; exit = bit flags: +2 registered HALT, +4 Tier-E halted, +8 ABSENT, +16 no-clobber; every condition printed
- [LEAN-HEPHAESTUS] SC-11 era-full registrations: tuning + holdout slices beside, Tier-E [L-1.3]
- [LEAN-HEPHAESTUS] SC-12 sidecar sum_net_r at 1e-6; AM-7 haircut law at 1e-12 (HALT on scored/base, disclosure on Tier-E)
- [LEAN-HEPHAESTUS] SC-13 book_sha256 = sha256(canonical CSV of the 16 required columns sorted (symbol, entry_close_ms), floats repr)
- [LEAN-HEPHAESTUS] SC-14 pick stability [L-R.2]: lens consumed P-BRK-4H 4h, P-ADD-BRK / P-ADD-SFP 1h, P-TP-RNG 12h (texts of record); the per-CLASSIC5-asset change (SCALE_PICKS.json first half of tuning vs tuning) flagged on the §0 SCALE cell and every Tier-E row consuming the calibrated pick; whole-tape fallback cells labelled IN-SAMPLE
- [LEAN-HEPHAESTUS] SC-15 identity law [L-1.5]: paired arms vs their own base — rows with acted_by blank equal the base exactly on net_r, exit_close_ms, exit_reason, else HALT
- [LEAN-HEPHAESTUS] SC-16 gate = post-filter [L-1.5]: no key outside the base, every kept row equal to the base on the 16 columns, else HALT
- [LEAN-HEPHAESTUS] SC-17 gating status cross-checked: P-WARN-1 vs condition.json (met, ci_hi < 0), P-SCALP-2 vs R2_LENS_VERDICTS.json 1h; the tuning-era R2 1h word printed beside P-SCALP-2, collared [§10]
- [LEAN-HEPHAESTUS] SC-18 adds head-to-head: derived (paired, collared) when not filed with a base_arm
- [LEAN-HEPHAESTUS] SC-19 regbook strictness: int64 times, int8 direction, no ',', '"', CR, LF in a string field, 0 < entry_close_ms - entry_ms <= one lens step (4h unless the sidecar names a lens)

## Findings

- none
