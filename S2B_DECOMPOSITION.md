# S-2b — Architecture Decomposition (Tier A, journals only)

> **in-sample; first-order (rail/halt/equity feedback ignored, entries fixed); 1x-proxy costs; struct books denominated in the wider structural one_r; flatten-reason split is the disclosed proxy**

Every table states its denominator. baseline & fold-in = baseline-R (native one_r); F4 struct books = struct-R (wider structural one_r). Not comparable across denominators without that note.

## Fixtures

- **F1**: MATCH — `{"sum_1x": -1796.993, "sum_0x": 275.9924, "campaigns": 2599, "win_pct": 10.8503}`
- **F2**: MATCH — `{"30m": {"stop": 4493, "gap": 9, "baseline_death": 15, "ride_to_death": 1755, "void": 7, "book_1x": 363.5363, "match": true}, "1h": {"stop": 3997, "ga`
- **F3**: MATCH — `{"cost_30m": 742.9377, "cost_1h": 606.9916, "baseline_cost": 2072.9854, "1h_swing": 2362.5724, "1h_cost_identity": 1465.9938, "1h_gross": 896.5785, "1`
- **F4**: MATCH — `{"fold_grid_0x": 506.279, "fold_position_1x_proxy": 384.2388}`

## D1 — Architecture decision table (GRID)

| architecture (denom) | 0x | 1x-proxy | strip-best 1x | win | camps/tr | cost stack |
|---|---|---|---|---|---|---|
| baseline (baseline-R) | 275.9924 | -1796.993 | -1911.4449 | 10.8503% | 2599/6279 | 2072.9854 |
| fold (baseline-R) | 506.279 | -1566.7064 | -1799.6736 | 6.1562% | 2599/6279 | 2072.9854 |
| struct30 (struct-R) | 1106.4739 | 363.5363 | -133.4928 | 11.4275% | 2599/6279 | 742.9377 |
| struct1h (struct-R) | 1172.5709 | 565.5794 | 301.9922 | 13.7745% | 2599/6279 | 606.9916 |
| struct_ratcheting | *NAMED-UNMEASURED (blank by design): re-anchors the structural stop to each newer confirmed pivot; not priced this phase — TC-1's cell* | | | | | | |

### D1 per-mandate 1x-proxy (denominators as above)

| architecture | swing | intraday | position |
|---|---|---|---|
| baseline | -282.1248 | -1441.073 | -73.7952 |
| fold | -198.1107 | -1752.8345 | 384.2388 |
| struct30 | 200.7093 | -655.7449 | 818.5718 |
| struct1h | 384.8154 | -307.4303 | 488.1942 |

## D2 — Concentration

`{"baseline": {"GRID": {"sum_1x_proxy": -1796.993, "strip_best_1x": -1911.4449, "top10_share_of_sum_wins_pct": 28.585, "sign_flip_on_strip": false}, "swing": {"sum_1x_proxy": -282.1248, "strip_best_1x": -396.5767, "top10_share_of_sum_wins_pct": 52.0922, "sign_flip_on_strip": false}, "intraday": {"sum_1x_proxy": -1441.073, "strip_best_1x": -1482.1857, "top10_share_of_sum_wins_pct": 33.2633, "sign_flip_on_strip": false}, "position": {"sum_1x_proxy": -73.7952, "strip_best_1x": -109.9354, "top10_share_of_sum_wins_pct": 84.0269, "sign_flip_on_strip": false}}, "fold": {"GRID": {"sum_1x_proxy": -1566.7064, "strip_best_1x": -1799.6736, "top10_share_of_sum_wins_pct": 50.9925, "sign_flip_on_strip": false}, "swing": {"sum_1x_proxy": -198.1107, "strip_best_1x": -352.9225, "top10_share_of_sum_wins_pct": 75.6524, "sign_flip_on_strip": false}, "intraday": {"sum_1x_proxy": -1752.8345, "strip_best_1x": -1895.633, "top10_share_of_sum_wins_pct": 67.3485, "sign_flip_on_strip": false}, "position": {"sum_1x_proxy": 384.2388, "strip_best_1x": 151.2716, "top10_share_of_sum_wins_pct": 98.1902, "sign_flip_on_strip": false}}, "struct30": {"GRID": {"sum_1x_proxy": 363.5363, "strip_best_1x": -133.4928, "top10_share_of_sum_wins_pct": 50.6222, "sign_flip_on_strip": true}, "swing": {"sum_1x_proxy": 200.7093, "strip_best_1x": 40.5996, "top10_share_of_sum_wins_pct": 67.2252, "sign_flip_on_strip": false}, "intraday": {"sum_1x_proxy": -655.7449, "strip_best_1x": -707.0426, "top10_share_of_sum_wins_pct": 30.2363, "sign_flip_on_strip": false}, "position": {"sum_1x_proxy": 818.5718, "strip_best_1x": 321.5427, "top10_share_of_sum_wins_pct": 99.4213, "sign_flip_on_strip": false}}, "struct1h": {"GRID": {"sum_1x_proxy": 565.5794, "strip_best_1x": 301.9922, "top10_share_of_sum_wins_pct": 38.0054, "sign_flip_on_strip": false}, "swing": {"sum_1x_proxy": 384.8154, "strip_best_1x": 250.6203, "top10_share_of_sum_wins_pct": 59.881, "sign_flip_on_strip": false}, "intraday": {"sum_1x_proxy": -307.4303, "strip_best_1x": -401.8457, "top10_share_of_sum_wins_pct": 30.412, "sign_flip_on_strip": false}, "position": {"sum_1x_proxy": 488.1942, "strip_best_1x": 224.6071, "top10_share_of_sum_wins_pct": 93.5143, "sign_flip_on_strip": false}}}`

## D3 — Distributions

`{"holding_bars_median": {"baseline": {"swing": 8.0, "intraday": 7.0, "position": 8.0}, "fold": {"swing": 8.0, "intraday": 7.0, "position": 8.0}, "struct30": {"swing": 55.0, "intraday": 252.0, "position": 11.5}, "struct1h": {"swing": 128.0, "intraday": 347.0, "position": 29.0}}, "win_rate_by_exit_reason": {"baseline": {"campaign_died": {"n": 4, "win_pct": 25.0}, "failure_x": {"n": 9, "win_pct": 33.3333}, "opposite_cross": {"n": 3, "win_pct": 66.6667}, "stop": {"n": 6223, "win_pct": 16.2301}, "stop_gap": {"n": 40, "win_pct": 10.0}}, "fold": {"flatten": {"n": 93, "win_pct": 84.9462}, "gap": {"n": 36, "win_pct": 2.7778}, "stop": {"n": 6150, "win_pct": 5.2683}}, "struct30": {"flatten_baseline_death": {"n": 15, "win_pct": 33.3333}, "flatten_ride_to_death": {"n": 1755, "win_pct": 43.0769}, "gap": {"n": 9, "win_pct": 0.0}, "stop": {"n": 4493, "win_pct": 0.0}, "void_baseline_kept": {"n": 7, "win_pct": 0.0}}, "struct1h": {"flatten_baseline_death": {"n": 15, "win_pct": 33.3333}, "flatten_ride_to_death": {"n": 2259, "win_pct": 40.5046}, "gap": {"n": 8, "win_pct": 0.0}, "stop": {"n": 3997, "win_pct": 0.0}}}, "denominator_ratio_bps": {"30m": {"swing": {"n": 1871, "p25_50_75": [1.4791, 2.6359, 4.5745]}, "intraday": {"n": 3874, "p25_50_75": [2.7732, 6.0039, 11.2595]}, "position": {"n": 527, "p25_50_75": [0.7409, 1.2264, 1.9974]}}, "1h": {"swing": {"n": 1873, "p25_50_75": [2.1827, 4.1165, 6.9858]}, "intraday": {"n": 3874, "p25_50_75": [3.2384, 7.3679, 15.0017]}, "position": {"n": 532, "p25_50_75": [1.0572, 1.9199, 3.2432]}}}}`

## D4 — Fold-in mirror decomposition

`{"exit_census": {"trail_exit_post_engage": 4662, "native_stop_pre_engage": 1524, "flatten": 93}, "cost_stack": 2072.9854, "baseline_cost_stack": 2072.9854, "cost_identity_component": 0.0, "gross_component": 230.2866, "swing_vs_baseline": 230.2866, "note": "cost-identity component should be ~0 (same entries, same baseline denominator, cost_r unchanged) \u2014 the decomposition-method sanity check; nonzero would mean the cost split is mis-derived"}`

## D5 — m=2 overlap

`{"m2_flagged_fills": 3801, "denominator": "baseline stop_bps < 2xtoll; struct clears iff struct stop_dist_bps >= 2xtoll", "clears_2xtoll_under_30m": {"n": 3133, "pct": 82.4257, "still_under_or_void": 668, "void_in_flagged": 0}, "clears_2xtoll_under_1h": {"n": 3247, "pct": 85.4249, "still_under_or_void": 554, "void_in_flagged": 0}, "floor_passes_but_30m_under": 171, "floor_passes_but_1h_under": 98}`

## D6 — Joint first-passage (PARTIAL)

`{"status": "PARTIAL", "missing_field": "the gov-e200 trail re-seeded/re-walked under the STRUCTURAL stop as phase-1 floor. Journals carry the native-seeded trail (fold book) and the fixed structural stop (struct book) but NOT their interaction: the joint's trail would seed at the wider structural stop, so the native-seeded fold trail is not a faithful substitute. A naive first-touch min() over the two journaled books would misprice exactly the pre-engagement region (fold native-stop exits the joint replaces with the wider structural floor). No joint R priced.", "diagnostic_interaction_region_1h": 4019, "diagnostic_note": "tranches where the post-engagement fold trail exits strictly before the 1h structural stop \u2014 the region where the two lines genuinely interact and TC-1's re-simulation is required. Descriptive only.", "reviewer_ruling": "the real interaction is TC-1's fourth cell either way (contract 4.D6)"}`

## D7 — Ride-to-death anatomy

`{"denominator": "struct-R", "per_mandate": {"30m": {"swing": {"n": 297, "mean_cell_r": 3.754, "mean_bars": 3524.7003}, "intraday": {"n": 1422, "mean_cell_r": 0.5916, "mean_bars": 3329.7848}, "position": {"n": 36, "mean_cell_r": 30.5832, "mean_bars": 4743.0833}}, "1h": {"swing": {"n": 518, "mean_cell_r": 2.1958, "mean_bars": 3180.9865}, "intraday": {"n": 1679, "mean_cell_r": 0.6003, "mean_bars": 3443.0191}, "position": {"n": 62, "mean_cell_r": 11.9713, "mean_bars": 4550.3871}}}, "note": "the shape of what the doctrine actually buys: baseline stopped these out, the structural stop rode them to campaign death"}`

## Prediction scorecard

| # | verdict | measured |
|---|---|---|
| P-S2b-1 | **FALSIFIED** | `{"f4_1h_intraday_1x": -307.4303, "denominator": "struct-R"}` |
| P-S2b-2 | **CONFIRMED** | `{"f4_1h_grid_strip_best": 301.9922}` |
| P-S2b-3 | **CONFIRMED** | `{"fold_cost_stack": 2072.9854, "deviation_pct": 0.0}` |
| P-S2b-4 | **CONFIRMED** | `{"clears_1h_pct": 85.4249}` |
| P-S2b-5 | **CONFIRMED** | `{"hold_ratio_1h_vs_baseline": {"swing": 16.0, "intraday": 49.5714, "position": 3.625}}` |

*scripts/s2b_decompose.py; raw journal bytes; read-only.*

## F5 (determinism) — appended post-generation

Manual annotation (the generated body above hashes to `886bb7de…`; this
section is appended by hand, so the committed file's hash differs from the
generation hash — both are recorded in the ledger).

`scripts/s2b_decompose.py` run twice, output hashes IDENTICAL:
- `sha256(s2b_results.json)` = `0a892053d8148c7af2c2b2eca880e3844f38d74e3ace599bff2289f20e2b3bf9` (both runs)
- `sha256(S2B_DECOMPOSITION.md, generated)` = `886bb7dedb57eb093ae8cbcb9697ba49105c3a368bef7b131cdb4d68c10da6f6` (both runs)

F5 MATCH.

**D5 reconciliation (m=2-flagged fills):** 3,813 flagged of 6,304 total
fills = 3,801 of 6,279 resolved + 12 of the 25 buffered/open fills (fills
whose EXIT row is unresolved at window end, absent from every architecture
book). Verified from raw bytes: total 6,304 / resolved 6,279 / unresolved
25; flagged all 3,813 / resolved 3,801 / unresolved 12. The 12 are exactly
among the 25. S-2b's D5 percentages are computed on the resolved 3,801;
the count difference is the 12 unresolved-and-flagged, not a discrepancy.
