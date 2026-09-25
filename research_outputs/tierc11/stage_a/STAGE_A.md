# TIER-C11 · STAGE A · ADDS, DECIDED — P-ADD-BRK and P-ADD-SFP

as_of_last_closed_4h: 2026-09-25T00:00:00Z · substrate tc11_20260925 · seed 20260924 · corridor 2019-09-08T16:00:00Z → 2026-09-25T00:00:00Z · panel CLASSIC5 · v6 n 200 (book sha f3c68f544bcda52c…)

Registered books are printed as **book, not a verdict** (no CI, no p, no verdict word: the scorer, scripts/tierc11_score.py, decides). Every other table carries the collar tier = TIER-E · selection_not_a_result = 'a SELECTION, not a result' · gates = nothing.

## Readings (executor sub-readings of this stage)

- [LEAN-HEPHAESTUS] SA-1 EVENTS [L-A.2, L-A.3]: from N.range_facts(stem, '1h', scale) (plain arrays): P-ADD-BRK = die_* rows (machine 'breakout-die' of a CONFIRMED range), trade direction = die_dir (+1 top death -> long, -1 bottom -> short); P-ADD-SFP = harden_* rows, trade direction = harden_dir (+1 bottom harden = spring -> long, -1 top harden = upthrust -> short). Known at the event bar's 1h close (known_at == event bar holds by the nest's construction, so its assert cannot fail; the as-of guard is F-ADD's prefix run of the machine); a confirmed range of the same rid alive at the prior 1h close (asserted); a death leaves it dead at its bar, a harden leaves it alive (asserted).
- [LEAN-HEPHAESTUS] SA-2 CANDIDATES: per campaign, the same-direction events whose 1h close lies in (entry close, close of the exit 4h bar]; handed as (1h close ms, None) to RD.transform_book(walk=True, adds_of=...) -> RD.admit_adds, which decides in-trade (> entry close, < the 1h-resolved exit), after the +1R latch (latch child counts), the twins, then the 2-add cap (AM-6 s4), the tape's 1h close as the price (s5), a mismatch-bar event taken at the parent's close (L-W.0).
- [LEAN-HEPHAESTUS] SA-3 SCALE [L-R.2]: the calibrated 1h pick of record (SCALE_PICKS.json, tuning-era calibration) for the scored arm and every twin but tierE__frozen3 (frozen 3.0, fully causal). Every add row carries scale_in_sample (a calibrated read at an instant <= 2024-06-30T23:59:59Z), pick_window and stability_changed.
- [LEAN-HEPHAESTUS] SA-4 BASE ARM: the v6 book in the regbook schema = RD.transform_book(v6, walk=True) with every hook off, asserted identical to v6 (TP.ctrl_diff worst 0.000e+00, identity helper acted 0) AND to books/v6_campaigns.parquet on its 13 regbook columns at that file's 6 dp. exit_close_ms = the v6 book of record's exit_close_ms (the exit bar's 4h close; for a stop exit the L-R.5 post-event twin) on EVERY arm (the add books keep the v6 leg); the 1h-RESOLVED exit instant (L-W.3: a stop at the close of the first 1h child touching it, a bell at the 4h close, a mismatch-bar stop at the parent's close) rides beside as exit_close_1h_ms and is the instant the in-trade test uses; entry_ms = v6's entry_ms (the pairing key); entry_close_ms = entry_ms + 4h.
- [LEAN-HEPHAESTUS] SA-5 ERA SLICES [L-1.3]: tierE__tuning / tierE__holdout = the scored book's rows with E.era_of(entry_close_ms) == the slice; paired against the base arm restricted to the same keys.
- [LEAN-HEPHAESTUS] SA-6 HAIRCUT [AM-7]: haircut_net_r = net_r - fee_r x (slip_bps_side / 5.0), slip = the stem's charter tier (E.fees(): A 2 / B 5 / C 10 bps per side); fee_r is the ride's taker fee over every fill incl. the adds' entries and exits.
- [LEAN-HEPHAESTUS] SA-7 Δ [AM-3]: delta_net_r = net_r(add book) - net_r(v6), the paired statistic; add_r (tierc7._account_chain) and the cap-absorbed funding (funding_r_uncapped - funding_r) printed beside; Δ - add_r == absorbed(book) - absorbed(v6) asserted to 1e-9; never Δ == add_r.
- [LEAN-HEPHAESTUS] SA-8 FLAGS [L-A.1]: below_entry = (add_px - entry_px) x d < 0; post_harvest = the harvest fired and the add's 4h bar >= the harvest bar (after it, or inside its 4h bar). The twins refuse each class; the scored arm is unchanged. The 'inside its 4h bar' clause refuses an add whose 1h close precedes the harvest's decision at that bar's close — look-ahead at reading level inside a Tier-E twin; the count of such adds is printed (finding F7).
- [LEAN-HEPHAESTUS] SA-9 COLLARS [L-1.4]: every stage table but REGISTERED_BOOKS carries tier 'TIER-E', selection_not_a_result 'a SELECTION, not a result', gates 'nothing' and no verdict word; registered books are labelled 'book, not a verdict'. Head-to-head: 'neither promoted by the other's failure'.
- [LEAN-HEPHAESTUS] SA-10 SCALE-IN-SAMPLE [L-R.2]: calibrated-scale range reads at instants <= the era cut are structurally in-sample (tuning-era calibration); the holdout slice (tierE__holdout) and the frozen-3.0 twin (tierE__frozen3) are the statistics printed beside the verdict.
- [LEAN-HEPHAESTUS] SA-11 HEAD-TO-HEAD [registrations' tier_e_arms, scorer SC-3]: tierE__head_to_head_vs_p_add_sfp (under P-ADD-BRK) / tierE__head_to_head_vs_p_add_brk (under P-ADD-SFP) = the registration's scored book, row for row (the same book sha), with ruler 'paired' and sidecar base_arm '<the other registration>/scored'; both are the v6 key set, so the paired premise holds by construction. Extras opponent_net_r and delta_vs_opponent_net_r (= net_r - opponent_net_r). The head-to-head is a SELECTION, not a result: 'neither promoted by the other's failure'.

## 1 · Registered books (book, not a verdict)

| registration | arm | n | n_acted | n_adds | sum_net_r | mean_net_r | sum_haircut_net_r | sum_delta_vs_base | mean_delta_vs_base | era_scope | ruler | label |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-ADD-BRK | base | 200 | 0 | 0 | +40.807565 | +0.204038 | +36.697549 | +0.000000 | +0.000000 | full | paired | book, not a verdict |
| P-ADD-BRK | scored | 200 | 52 | 66 | +36.770865 | +0.183854 | +32.025302 | -4.036700 | -0.020184 | full | paired | book, not a verdict |
| P-ADD-SFP | base | 200 | 0 | 0 | +40.807565 | +0.204038 | +36.697549 | +0.000000 | +0.000000 | full | paired | book, not a verdict |
| P-ADD-SFP | scored | 200 | 9 | 12 | +36.811969 | +0.184060 | +32.603119 | -3.995596 | -0.019978 | full | paired | book, not a verdict |

SCALE-IN-SAMPLE [L-R.2]: the calibrated 1h scale is fit on the tuning era, so every range read at an instant ≤ 2024-06-30T23:59:59Z is structurally in-sample (outcome-free look-ahead). The holdout slice (tierE__holdout) and the frozen-3.0 twin (tierE__frozen3) below are the statistics to print beside each verdict.

## 2 · Tier-E arms (a SELECTION, not a result)

| registration | arm | era_scope | n | n_acted | n_adds | sum_net_r | mean_net_r | ruled_against | ruled_base_sum_net_r | sum_delta_vs_ruled_base | mean_delta_vs_ruled_base | base_sum_net_r | sum_delta_net_r | mean_delta_net_r | sum_add_r | n_adds_below_entry | n_adds_post_harvest | n_adds_moved | tier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-ADD-BRK | tierE__frozen3 | full | 200 | 49 | 51 | +44.391987 | +0.221960 | base | +40.807565 | +3.584422 | +0.017922 | +40.807565 | +3.584422 | +0.017922 | +3.584422 | 0 | 6 | 0 | TIER-E |
| P-ADD-BRK | tierE__head_to_head_vs_p_add_sfp | full | 200 | 52 | 66 | +36.770865 | +0.183854 | P-ADD-SFP/scored | +36.811969 | -0.041104 | -0.000206 | +40.807565 | -4.036700 | -0.020184 | -4.117335 | 0 | 10 | 0 | TIER-E |
| P-ADD-BRK | tierE__holdout | holdout | 77 | 27 | 34 | +38.645247 | +0.501886 | base | +42.131386 | -3.486140 | -0.045275 | +42.131386 | -3.486140 | -0.045275 | -3.486140 | 0 | 6 | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | full | 200 | 52 | 66 | +36.770865 | +0.183854 | base | +40.807565 | -4.036700 | -0.020184 | +40.807565 | -4.036700 | -0.020184 | -4.117335 | 0 | 10 | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | full | 200 | 45 | 56 | +36.768779 | +0.183844 | base | +40.807565 | -4.038785 | -0.020194 | +40.807565 | -4.038785 | -0.020194 | -4.119421 | 0 | 0 | 0 | TIER-E |
| P-ADD-BRK | tierE__tuning | tuning | 123 | 25 | 32 | -1.874382 | -0.015239 | base | -1.323822 | -0.550560 | -0.004476 | -1.323822 | -0.550560 | -0.004476 | -0.631196 | 0 | 4 | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | full | 200 | 2 | 3 | +40.129503 | +0.200648 | base | +40.807565 | -0.678062 | -0.003390 | +40.807565 | -0.678062 | -0.003390 | -0.678062 | 0 | 0 | 0 | TIER-E |
| P-ADD-SFP | tierE__head_to_head_vs_p_add_brk | full | 200 | 9 | 12 | +36.811969 | +0.184060 | P-ADD-BRK/scored | +36.770865 | +0.041104 | +0.000206 | +40.807565 | -3.995596 | -0.019978 | -3.995596 | 1 | 5 | 0 | TIER-E |
| P-ADD-SFP | tierE__holdout | holdout | 77 | 7 | 10 | +39.634377 | +0.514732 | base | +42.131386 | -2.497010 | -0.032429 | +42.131386 | -2.497010 | -0.032429 | -2.497010 | 1 | 5 | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | full | 200 | 8 | 11 | +37.006164 | +0.185031 | base | +40.807565 | -3.801400 | -0.019007 | +40.807565 | -3.801400 | -0.019007 | -3.801400 | 0 | 4 | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | full | 200 | 6 | 7 | +37.733492 | +0.188667 | base | +40.807565 | -3.074073 | -0.015370 | +40.807565 | -3.074073 | -0.015370 | -3.074073 | 0 | 0 | 0 | TIER-E |
| P-ADD-SFP | tierE__tuning | tuning | 123 | 2 | 2 | -2.822408 | -0.022946 | base | -1.323822 | -1.498586 | -0.012184 | -1.323822 | -1.498586 | -0.012184 | -1.498586 | 0 | 0 | 0 | TIER-E |

ruled_against = the book each Tier-E arm is paired against (the base restricted to the arm's keys, or the head-to-head arm's base_arm, the other registration's scored book); base_sum_net_r / sum_delta_net_r are always vs v6 (the base).

## 3 · HEAD-TO-HEAD — P-ADD-BRK vs P-ADD-SFP (neither promoted by the other's failure)

| arm | registration | n_campaigns | n_campaigns_acted | n_adds | sum_add_r | sum_delta_net_r | mean_delta_net_r | mean_delta_net_r_acted | n_adds_below_entry | n_adds_post_harvest | n_adds_moved | n_adds_scale_in_sample | tier |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| scored | P-ADD-BRK | 200 | 52 | 66 | -4.117335 | -4.036700 | -0.020184 | -0.077629 | 0 | 10 | 0 | 32 | TIER-E |
| scored | P-ADD-SFP | 200 | 9 | 12 | -3.995596 | -3.995596 | -0.019978 | -0.443955 | 1 | 5 | 0 | 2 | TIER-E |
| tierE__frozen3 | P-ADD-BRK | 200 | 49 | 51 | +3.584422 | +3.584422 | +0.017922 | +0.073151 | 0 | 6 | 0 | 0 | TIER-E |
| tierE__frozen3 | P-ADD-SFP | 200 | 2 | 3 | -0.678062 | -0.678062 | -0.003390 | -0.339031 | 0 | 0 | 0 | 0 | TIER-E |
| tierE__holdout | P-ADD-BRK | 77 | 27 | 34 | -3.486140 | -3.486140 | -0.045275 | -0.129116 | 0 | 6 | 0 | 0 | TIER-E |
| tierE__holdout | P-ADD-SFP | 77 | 7 | 10 | -2.497010 | -2.497010 | -0.032429 | -0.356716 | 1 | 5 | 0 | 0 | TIER-E |
| tierE__refuse_below_entry | P-ADD-BRK | 200 | 52 | 66 | -4.117335 | -4.036700 | -0.020184 | -0.077629 | 0 | 10 | 0 | 32 | TIER-E |
| tierE__refuse_below_entry | P-ADD-SFP | 200 | 8 | 11 | -3.801400 | -3.801400 | -0.019007 | -0.475175 | 0 | 4 | 0 | 2 | TIER-E |
| tierE__refuse_post_harvest | P-ADD-BRK | 200 | 45 | 56 | -4.119421 | -4.038785 | -0.020194 | -0.089751 | 0 | 0 | 0 | 28 | TIER-E |
| tierE__refuse_post_harvest | P-ADD-SFP | 200 | 6 | 7 | -3.074073 | -3.074073 | -0.015370 | -0.512345 | 0 | 0 | 0 | 2 | TIER-E |
| tierE__tuning | P-ADD-BRK | 123 | 25 | 32 | -0.631196 | -0.550560 | -0.004476 | -0.022022 | 0 | 4 | 0 | 32 | TIER-E |
| tierE__tuning | P-ADD-SFP | 123 | 2 | 2 | -1.498586 | -1.498586 | -0.012184 | -0.749293 | 0 | 0 | 0 | 2 | TIER-E |

**neither promoted by the other's failure.** mean_delta_net_r is over the arm's campaigns (the paired statistic's point value); _acted over the campaigns that took an add. The direct paired head-to-head is the Tier-E arm tierE__head_to_head_vs_p_add_sfp (under P-ADD-BRK, base_arm P-ADD-SFP/scored) / tierE__head_to_head_vs_p_add_brk (under P-ADD-SFP, base_arm P-ADD-BRK/scored) in §2 (sum_delta_vs_ruled_base).

### Overlap of the acted campaigns

| arm | n_campaigns | acted_brk | acted_sfp | acted_both | acted_either | acted_brk_only | acted_sfp_only | tier |
|---|---|---|---|---|---|---|---|---|
| scored | 200 | 52 | 9 | 8 | 53 | 44 | 1 | TIER-E |
| tierE__frozen3 | 200 | 49 | 2 | 1 | 50 | 48 | 1 | TIER-E |
| tierE__holdout | 77 | 27 | 7 | 6 | 28 | 21 | 1 | TIER-E |
| tierE__refuse_below_entry | 200 | 52 | 8 | 7 | 53 | 45 | 1 | TIER-E |
| tierE__refuse_post_harvest | 200 | 45 | 6 | 5 | 46 | 40 | 1 | TIER-E |
| tierE__tuning | 123 | 25 | 2 | 2 | 25 | 23 | 0 | TIER-E |

## 4 · Event dispositions (every candidate event handed to the add hook; the grid whole)

| registration | arm | disposition | n_events | tier |
|---|---|---|---|---|
| P-ADD-BRK | scored | admitted | 66 | TIER-E |
| P-ADD-BRK | scored | refused: before the +1R latch | 33 | TIER-E |
| P-ADD-BRK | scored | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-BRK | scored | refused: cap 2 reached | 4 | TIER-E |
| P-ADD-BRK | scored | refused: not before the 1h-resolved exit | 0 | TIER-E |
| P-ADD-BRK | scored | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-BRK | scored | refused: pre-entry | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | admitted | 51 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: before the +1R latch | 17 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: cap 2 reached | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: not before the 1h-resolved exit | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | refused: pre-entry | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | admitted | 66 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: before the +1R latch | 33 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: cap 2 reached | 4 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: not before the 1h-resolved exit | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | refused: pre-entry | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | admitted | 56 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: before the +1R latch | 33 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: cap 2 reached | 3 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: not before the 1h-resolved exit | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: post-harvest (twin) | 11 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | refused: pre-entry | 0 | TIER-E |
| P-ADD-SFP | scored | admitted | 12 | TIER-E |
| P-ADD-SFP | scored | refused: before the +1R latch | 5 | TIER-E |
| P-ADD-SFP | scored | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-SFP | scored | refused: cap 2 reached | 0 | TIER-E |
| P-ADD-SFP | scored | refused: not before the 1h-resolved exit | 8 | TIER-E |
| P-ADD-SFP | scored | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-SFP | scored | refused: pre-entry | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | admitted | 3 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: before the +1R latch | 1 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: cap 2 reached | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: not before the 1h-resolved exit | 3 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | refused: pre-entry | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | admitted | 11 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: before the +1R latch | 5 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: below entry (twin) | 1 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: cap 2 reached | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: not before the 1h-resolved exit | 8 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: post-harvest (twin) | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | refused: pre-entry | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | admitted | 7 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: before the +1R latch | 5 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: below entry (twin) | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: cap 2 reached | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: not before the 1h-resolved exit | 8 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: post-harvest (twin) | 5 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | refused: pre-entry | 0 | TIER-E |

## 5 · Acted campaigns — Δ decomposition [AM-3] (every row)

Δ = net_r(add book) − net_r(v6); add_r and the cap-absorbed funding beside; am3_residual = Δ − add_r − (absorbed − v6 absorbed), asserted |·| ≤ 1e-9.

### P-ADD-BRK · scored (52 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | 1 | -0.235827 | -1.188058 | -0.952231 | -0.952231 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | tuning | 1 | +1.206869 | +0.061501 | -1.145368 | -1.145368 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | 1 | +3.121717 | +3.126078 | +0.004361 | +0.004361 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +3.851193 | +4.709870 | +0.858677 | +0.858677 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | 2 | +9.142996 | +9.430394 | +0.287398 | +0.287398 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | holdout | 2 | +1.093368 | +1.337336 | +0.243969 | +0.243969 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | 1 | +2.790095 | +1.751467 | -1.038628 | -1.038628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 2 | +4.334979 | +4.915707 | +0.580728 | +0.580728 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | 1 | +3.642155 | +2.117045 | -1.525110 | -1.525110 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 2 | +1.021518 | +0.998330 | -0.023188 | -0.103823 | +0.080635 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-06-08T00:00:00Z | -1 | tuning | 2 | +0.785948 | +0.261229 | -0.524719 | -0.524719 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | tuning | 1 | +1.710331 | +2.569616 | +0.859285 | +0.859285 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ETHUSDT | 2024-10-08T08:00:00Z | -1 | holdout | 1 | -0.362807 | -1.665940 | -1.303133 | -1.303133 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | 1 | +0.490661 | -0.463789 | -0.954450 | -0.954450 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +5.236268 | +6.799651 | +1.563383 | +1.563383 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | -0.301315 | -0.442685 | -0.442685 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | 1 | +6.179393 | +8.385265 | +2.205873 | +2.205873 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | 1 | +2.707180 | +2.712587 | +0.005406 | +0.005406 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | tuning | 1 | +1.489613 | +1.759527 | +0.269914 | +0.269914 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | 1 | -1.282760 | -3.954308 | -2.671548 | -2.671548 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | tuning | 1 | +0.812897 | +0.640418 | -0.172479 | -0.172479 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | 1 | +2.173604 | +1.320845 | -0.852759 | -0.852759 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +0.426185 | -0.464914 | -0.891100 | -0.891100 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 1 | -0.293939 | -1.591336 | -1.297396 | -1.297396 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-06-12T20:00:00Z | -1 | holdout | 1 | +0.474739 | +0.224561 | -0.250178 | -0.250178 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | 1 | -0.700837 | -1.779603 | -1.078767 | -1.078767 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 2 | +0.264459 | -0.054001 | -0.318460 | -0.318460 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | 1 | +8.744969 | +11.772946 | +3.027977 | +3.027977 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2026-07-22T00:00:00Z | -1 | holdout | 1 | +2.021208 | +2.675546 | +0.654338 | +0.654338 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | 2 | +4.497064 | +7.141538 | +2.644474 | +2.644474 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | 2 | +2.256855 | +2.798420 | +0.541566 | +0.541566 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | tuning | 1 | +4.722981 | +4.919739 | +0.196758 | +0.196758 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 1 | +5.846761 | +7.738611 | +1.891850 | +1.891850 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | 1 | +0.853013 | +0.966025 | +0.113012 | +0.113012 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | 2 | +3.039578 | +4.444330 | +1.404753 | +1.404753 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +1.016032 | +0.206051 | -0.809981 | -0.809981 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | 2 | +0.838065 | -0.187324 | -1.025388 | -1.025388 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-12-11T04:00:00Z | -1 | holdout | 1 | -0.131149 | -0.642419 | -0.511270 | -0.511270 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | 1 | +0.426764 | -1.249259 | -1.676023 | -1.676023 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | tuning | 2 | +2.895209 | +3.922795 | +1.027586 | +1.027586 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-12-29T16:00:00Z | -1 | tuning | 1 | +0.131591 | -0.230342 | -0.361933 | -0.361933 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | 1 | +0.695742 | +0.424384 | -0.271358 | -0.271358 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | 1 | +3.104660 | +2.888815 | -0.215845 | -0.215845 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | 1 | +4.729894 | +6.076236 | +1.346342 | +1.346342 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | 1 | +2.792394 | +2.564096 | -0.228299 | -0.228299 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.711677 | -0.379981 | -0.379981 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-01-19T04:00:00Z | -1 | holdout | 1 | -1.026488 | -2.017125 | -0.990638 | -0.990638 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | 1 | +0.828704 | +0.560821 | -0.267883 | -0.267883 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 1 | +0.868059 | +1.483272 | +0.615214 | +0.615214 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | 1 | +5.156631 | +6.334478 | +1.177847 | +1.177847 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | 1 | -0.325329 | -0.827193 | -0.501864 | -0.501864 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | 1 | +25.060483 | +22.185734 | -2.874748 | -2.874748 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |

### P-ADD-BRK · tierE__frozen3 (49 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | 1 | -0.235827 | -1.188058 | -0.952231 | -0.952231 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | 1 | +3.121717 | +3.126078 | +0.004361 | +0.004361 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2023-09-01T04:00:00Z | -1 | tuning | 1 | +0.014904 | -0.663295 | -0.678200 | -0.678200 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | 1 | +9.142996 | +11.140685 | +1.997689 | +1.997689 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | holdout | 1 | +1.093368 | +1.846444 | +0.753076 | +0.753076 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| BTCUSDT | 2026-03-26T12:00:00Z | -1 | holdout | 1 | +0.880421 | +0.459818 | -0.420603 | -0.420603 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | 1 | +2.790095 | +1.751467 | -1.038628 | -1.038628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 1 | +4.334979 | +5.921644 | +1.586665 | +1.586665 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | 1 | +3.642155 | +2.117045 | -1.525110 | -1.525110 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 1 | +1.021518 | +1.000990 | -0.020529 | -0.020529 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-06-08T00:00:00Z | -1 | tuning | 1 | +0.785948 | +0.444186 | -0.341762 | -0.341762 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | tuning | 1 | +1.710331 | +2.569616 | +0.859285 | +0.859285 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ETHUSDT | 2023-07-13T12:00:00Z | 1 | tuning | 1 | -0.613184 | -1.488705 | -0.875521 | -0.875521 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2023-09-01T04:00:00Z | -1 | tuning | 1 | -0.397763 | -1.419658 | -1.021894 | -1.021894 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | 1 | +0.490661 | -0.000820 | -0.491481 | -0.491481 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +5.236268 | +6.774567 | +1.538299 | +1.538299 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | 1 | +6.179393 | +6.741066 | +0.561673 | +0.561673 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | 1 | +2.707180 | +3.318386 | +0.611206 | +0.611206 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | 1 | -1.282760 | -3.954308 | -2.671548 | -2.671548 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2021-11-08T20:00:00Z | 1 | tuning | 1 | +0.109233 | -0.327897 | -0.437129 | -0.437129 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | 2 | +2.173604 | +1.632484 | -0.541120 | -0.541120 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-06-28T04:00:00Z | -1 | tuning | 1 | +1.365862 | +0.602534 | -0.763328 | -0.763328 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2023-02-08T04:00:00Z | 1 | tuning | 1 | -1.019766 | -1.871132 | -0.851366 | -0.851366 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2024-07-03T20:00:00Z | -1 | holdout | 1 | +0.791599 | +0.498564 | -0.293036 | -0.293036 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +0.426185 | -0.464914 | -0.891100 | -0.891100 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 1 | -0.293939 | -1.591336 | -1.297396 | -1.297396 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | 1 | -0.700837 | -1.779603 | -1.078767 | -1.078767 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 1 | +0.264459 | +0.185551 | -0.078907 | -0.078907 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | 1 | +8.744969 | +11.772946 | +3.027977 | +3.027977 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | 1 | +4.497064 | +5.114234 | +0.617170 | +0.617170 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | 1 | +2.256855 | +2.423390 | +0.166535 | +0.166535 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 1 | +5.846761 | +7.738611 | +1.891850 | +1.891850 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | 1 | +0.853013 | -0.262990 | -1.116003 | -1.116003 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-10-18T20:00:00Z | -1 | tuning | 1 | +0.971114 | +0.801674 | -0.169441 | -0.169441 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | 2 | +3.039578 | +4.444330 | +1.404753 | +1.404753 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2024-04-25T08:00:00Z | -1 | tuning | 1 | +1.221031 | +0.373761 | -0.847270 | -0.847270 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-12-11T04:00:00Z | -1 | holdout | 1 | -0.131149 | -0.642419 | -0.511270 | -0.511270 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | 1 | +0.426764 | -1.249259 | -1.676023 | -1.676023 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | 1 | +0.695742 | +0.424384 | -0.271358 | -0.271358 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | 1 | +3.104660 | +2.888815 | -0.215845 | -0.215845 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | 1 | +4.729894 | +6.076236 | +1.346342 | +1.346342 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | 1 | +2.792394 | +2.564096 | -0.228299 | -0.228299 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-10-28T08:00:00Z | 1 | holdout | 1 | -1.021374 | -2.223958 | -1.202585 | -1.202585 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | -0.372558 | -1.464217 | -1.464217 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | 1 | +0.828704 | +0.560821 | -0.267883 | -0.267883 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 1 | +0.868059 | +1.152047 | +0.283988 | +0.283988 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | 1 | +5.156631 | +6.334478 | +1.177847 | +1.177847 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | 1 | -0.325329 | -0.827193 | -0.501864 | -0.501864 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | 1 | +25.060483 | +35.557902 | +10.497419 | +10.497419 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |

### P-ADD-BRK · tierE__refuse_below_entry (52 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | 1 | -0.235827 | -1.188058 | -0.952231 | -0.952231 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | tuning | 1 | +1.206869 | +0.061501 | -1.145368 | -1.145368 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | 1 | +3.121717 | +3.126078 | +0.004361 | +0.004361 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +3.851193 | +4.709870 | +0.858677 | +0.858677 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | 2 | +9.142996 | +9.430394 | +0.287398 | +0.287398 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | holdout | 2 | +1.093368 | +1.337336 | +0.243969 | +0.243969 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | 1 | +2.790095 | +1.751467 | -1.038628 | -1.038628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 2 | +4.334979 | +4.915707 | +0.580728 | +0.580728 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | 1 | +3.642155 | +2.117045 | -1.525110 | -1.525110 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 2 | +1.021518 | +0.998330 | -0.023188 | -0.103823 | +0.080635 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-06-08T00:00:00Z | -1 | tuning | 2 | +0.785948 | +0.261229 | -0.524719 | -0.524719 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | tuning | 1 | +1.710331 | +2.569616 | +0.859285 | +0.859285 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ETHUSDT | 2024-10-08T08:00:00Z | -1 | holdout | 1 | -0.362807 | -1.665940 | -1.303133 | -1.303133 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | 1 | +0.490661 | -0.463789 | -0.954450 | -0.954450 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +5.236268 | +6.799651 | +1.563383 | +1.563383 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | -0.301315 | -0.442685 | -0.442685 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | 1 | +6.179393 | +8.385265 | +2.205873 | +2.205873 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | 1 | +2.707180 | +2.712587 | +0.005406 | +0.005406 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | tuning | 1 | +1.489613 | +1.759527 | +0.269914 | +0.269914 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | 1 | -1.282760 | -3.954308 | -2.671548 | -2.671548 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | tuning | 1 | +0.812897 | +0.640418 | -0.172479 | -0.172479 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | 1 | +2.173604 | +1.320845 | -0.852759 | -0.852759 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +0.426185 | -0.464914 | -0.891100 | -0.891100 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 1 | -0.293939 | -1.591336 | -1.297396 | -1.297396 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-06-12T20:00:00Z | -1 | holdout | 1 | +0.474739 | +0.224561 | -0.250178 | -0.250178 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | 1 | -0.700837 | -1.779603 | -1.078767 | -1.078767 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 2 | +0.264459 | -0.054001 | -0.318460 | -0.318460 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | 1 | +8.744969 | +11.772946 | +3.027977 | +3.027977 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2026-07-22T00:00:00Z | -1 | holdout | 1 | +2.021208 | +2.675546 | +0.654338 | +0.654338 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | 2 | +4.497064 | +7.141538 | +2.644474 | +2.644474 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | 2 | +2.256855 | +2.798420 | +0.541566 | +0.541566 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | tuning | 1 | +4.722981 | +4.919739 | +0.196758 | +0.196758 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 1 | +5.846761 | +7.738611 | +1.891850 | +1.891850 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | 1 | +0.853013 | +0.966025 | +0.113012 | +0.113012 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | 2 | +3.039578 | +4.444330 | +1.404753 | +1.404753 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +1.016032 | +0.206051 | -0.809981 | -0.809981 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | 2 | +0.838065 | -0.187324 | -1.025388 | -1.025388 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-12-11T04:00:00Z | -1 | holdout | 1 | -0.131149 | -0.642419 | -0.511270 | -0.511270 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | 1 | +0.426764 | -1.249259 | -1.676023 | -1.676023 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | tuning | 2 | +2.895209 | +3.922795 | +1.027586 | +1.027586 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-12-29T16:00:00Z | -1 | tuning | 1 | +0.131591 | -0.230342 | -0.361933 | -0.361933 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | 1 | +0.695742 | +0.424384 | -0.271358 | -0.271358 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | 1 | +3.104660 | +2.888815 | -0.215845 | -0.215845 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | 1 | +4.729894 | +6.076236 | +1.346342 | +1.346342 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | 1 | +2.792394 | +2.564096 | -0.228299 | -0.228299 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.711677 | -0.379981 | -0.379981 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-01-19T04:00:00Z | -1 | holdout | 1 | -1.026488 | -2.017125 | -0.990638 | -0.990638 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | 1 | +0.828704 | +0.560821 | -0.267883 | -0.267883 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 1 | +0.868059 | +1.483272 | +0.615214 | +0.615214 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 1 | 0 |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | 1 | +5.156631 | +6.334478 | +1.177847 | +1.177847 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | 1 | -0.325329 | -0.827193 | -0.501864 | -0.501864 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | 1 | +25.060483 | +22.185734 | -2.874748 | -2.874748 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |

### P-ADD-BRK · tierE__refuse_post_harvest (45 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | 1 | -0.235827 | -1.188058 | -0.952231 | -0.952231 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | tuning | 1 | +1.206869 | +0.061501 | -1.145368 | -1.145368 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | 1 | +3.121717 | +3.126078 | +0.004361 | +0.004361 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +3.851193 | +4.709870 | +0.858677 | +0.858677 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | 2 | +9.142996 | +9.430394 | +0.287398 | +0.287398 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | 1 | +2.790095 | +1.751467 | -1.038628 | -1.038628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 2 | +4.334979 | +4.915707 | +0.580728 | +0.580728 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | 1 | +3.642155 | +2.117045 | -1.525110 | -1.525110 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 2 | +1.021518 | +0.998330 | -0.023188 | -0.103823 | +0.080635 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2024-10-08T08:00:00Z | -1 | holdout | 1 | -0.362807 | -1.665940 | -1.303133 | -1.303133 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | 1 | +0.490661 | -0.463789 | -0.954450 | -0.954450 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +5.236268 | +6.799651 | +1.563383 | +1.563383 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | -0.301315 | -0.442685 | -0.442685 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | 1 | +6.179393 | +8.385265 | +2.205873 | +2.205873 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | 1 | +2.707180 | +2.712587 | +0.005406 | +0.005406 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | tuning | 1 | +1.489613 | +1.759527 | +0.269914 | +0.269914 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | 1 | -1.282760 | -3.954308 | -2.671548 | -2.671548 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | tuning | 1 | +0.812897 | +0.640418 | -0.172479 | -0.172479 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | 1 | +2.173604 | +1.320845 | -0.852759 | -0.852759 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +0.426185 | -0.464914 | -0.891100 | -0.891100 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 1 | -0.293939 | -1.591336 | -1.297396 | -1.297396 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2025-06-12T20:00:00Z | -1 | holdout | 1 | +0.474739 | +0.224561 | -0.250178 | -0.250178 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | 1 | -0.700837 | -1.779603 | -1.078767 | -1.078767 | +0.000000 | +0.000000 | -0.000000 | yes | 0 | 0 | 0 |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | 1 | +8.744969 | +11.772946 | +3.027977 | +3.027977 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2026-07-22T00:00:00Z | -1 | holdout | 1 | +2.021208 | +2.675546 | +0.654338 | +0.654338 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | 2 | +4.497064 | +7.141538 | +2.644474 | +2.644474 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | 2 | +2.256855 | +2.798420 | +0.541566 | +0.541566 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | tuning | 1 | +4.722981 | +4.919739 | +0.196758 | +0.196758 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 1 | +5.846761 | +7.738611 | +1.891850 | +1.891850 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | 1 | +0.853013 | +0.966025 | +0.113012 | +0.113012 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | 2 | +3.039578 | +4.444330 | +1.404753 | +1.404753 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 2 | +1.016032 | +0.206051 | -0.809981 | -0.809981 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | 2 | +0.838065 | -0.187324 | -1.025388 | -1.025388 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | 1 | +0.426764 | -1.249259 | -1.676023 | -1.676023 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | tuning | 2 | +2.895209 | +3.922795 | +1.027586 | +1.027586 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | 1 | +0.695742 | +0.424384 | -0.271358 | -0.271358 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | 1 | +3.104660 | +2.888815 | -0.215845 | -0.215845 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | 1 | +4.729894 | +6.076236 | +1.346342 | +1.346342 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | 1 | +2.792394 | +2.564096 | -0.228299 | -0.228299 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.711677 | -0.379981 | -0.379981 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-01-19T04:00:00Z | -1 | holdout | 1 | -1.026488 | -2.017125 | -0.990638 | -0.990638 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | 1 | +0.828704 | +0.560821 | -0.267883 | -0.267883 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | 1 | +5.156631 | +6.334478 | +1.177847 | +1.177847 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | 1 | -0.325329 | -0.827193 | -0.501864 | -0.501864 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | 1 | +25.060483 | +22.185734 | -2.874748 | -2.874748 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |

### P-ADD-SFP · scored (9 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 1 | +4.334979 | +3.343351 | -0.991628 | -0.991628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 1 | +1.021518 | +0.514560 | -0.506958 | -0.506958 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | +0.028853 | -0.112517 | -0.112517 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +0.426185 | -0.234447 | -0.660632 | -0.660632 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 1 | -0.293939 | -0.488135 | -0.194196 | -0.194196 | +0.000000 | +0.000000 | +0.000000 | yes | 1 | 1 | 0 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 2 | +0.264459 | +0.047552 | -0.216906 | -0.216906 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.473936 | -0.617722 | -0.617722 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 2 | +0.868059 | +0.357637 | -0.510421 | -0.510421 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | holdout | 1 | +0.508657 | +0.324041 | -0.184616 | -0.184616 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |

### P-ADD-SFP · tierE__frozen3 (2 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 1 | +0.426185 | +0.188382 | -0.237803 | -0.237803 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | 2 | +0.838065 | +0.397806 | -0.440259 | -0.440259 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |

### P-ADD-SFP · tierE__refuse_below_entry (8 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 1 | +4.334979 | +3.343351 | -0.991628 | -0.991628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 1 | +1.021518 | +0.514560 | -0.506958 | -0.506958 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | +0.028853 | -0.112517 | -0.112517 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +0.426185 | -0.234447 | -0.660632 | -0.660632 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 2 | +0.264459 | +0.047552 | -0.216906 | -0.216906 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.473936 | -0.617722 | -0.617722 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 2 | +0.868059 | +0.357637 | -0.510421 | -0.510421 | +0.000000 | +0.000000 | +0.000000 | yes | 0 | 2 | 0 |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | holdout | 1 | +0.508657 | +0.324041 | -0.184616 | -0.184616 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |

### P-ADD-SFP · tierE__refuse_post_harvest (6 campaigns)

| symbol | entry_ms | direction | era | n_adds | v6_net_r | net_r | delta_net_r | add_r | funding_absorbed_r | v6_funding_absorbed_r | am3_residual | harvested | n_adds_below_entry | n_adds_post_harvest | n_adds_moved |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 1 | +4.334979 | +3.343351 | -0.991628 | -0.991628 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 1 | +1.021518 | +0.514560 | -0.506958 | -0.506958 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 1 | +0.141369 | +0.028853 | -0.112517 | -0.112517 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 2 | +0.426185 | -0.234447 | -0.660632 | -0.660632 | +0.000000 | +0.000000 | +0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 1 | +1.091659 | +0.473936 | -0.617722 | -0.617722 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | holdout | 1 | +0.508657 | +0.324041 | -0.184616 | -0.184616 | +0.000000 | +0.000000 | -0.000000 | no | 0 | 0 | 0 |

(The era slices' acted rows are the scored rows of that era; ACTED.parquet carries them under arm tierE__tuning / tierE__holdout.)

## 6 · Every admitted add (every row)

### P-ADD-BRK · scored (66 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | 1 | 2020-08-17T16:00:00Z | 8254 | 167 | 2020-08-17T16:00:00Z | +12443.990000 | 2020-08-17T12:00:00Z | 2020-08-17T14:00:00Z | 2020-08-19T05:00:00Z | no | no | no | yes |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | 1 | 2020-12-03T16:00:00Z | 10846 | 224 | 2020-12-03T16:00:00Z | +19560.910000 | 2020-12-03T12:00:00Z | 2020-11-30T01:00:00Z | 2020-12-04T23:00:00Z | no | no | no | yes |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | 1 | 2021-11-08T01:00:00Z | 18991 | 405 | 2021-11-08T01:00:00Z | +65097.190000 | 2021-11-08T00:00:00Z | 2021-11-08T00:00:00Z | 2021-11-10T21:00:00Z | no | no | no | yes |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T05:00:00Z | 45347 | 946 | 2024-11-10T05:00:00Z | +79273.700000 | 2024-11-10T04:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-13T15:00:00Z | 45429 | 950 | 2024-11-13T15:00:00Z | +91563.000000 | 2024-11-13T12:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 1 | -1 | 2025-02-25T00:00:00Z | 47910 | 989 | 2025-02-25T00:00:00Z | +91514.500000 | 2025-02-24T20:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 47953 | 991 | 2025-02-26T19:00:00Z | +84204.900000 | 2025-02-26T16:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | 1 | 2025-07-09T20:00:00Z | 51146 | 1070 | 2025-07-09T20:00:00Z | +111718.800000 | 2025-07-09T16:00:00Z | 2025-07-09T20:00:00Z | 2025-07-15T05:00:00Z | no | no | yes | no |
| BTCUSDT | 2025-07-02T12:00:00Z | 2 | 1 | 2025-07-13T21:00:00Z | 51243 | 1074 | 2025-07-13T21:00:00Z | +119028.700000 | 2025-07-13T20:00:00Z | 2025-07-09T20:00:00Z | 2025-07-15T05:00:00Z | no | no | yes | no |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | 1 | 2020-06-02T07:00:00Z | 4511 | 88 | 2020-06-02T07:00:00Z | +248.150000 | 2020-06-02T04:00:00Z | 2020-05-28T23:00:00Z | 2020-06-02T15:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-05T22:00:00Z | 8270 | 155 | 2020-11-05T22:00:00Z | +413.950000 | 2020-11-05T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 2 | 1 | 2020-11-11T08:00:00Z | 8400 | 158 | 2020-11-11T08:00:00Z | +462.520000 | 2020-11-11T04:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | 1 | 2020-12-17T11:00:00Z | 9267 | 166 | 2020-12-17T11:00:00Z | +670.420000 | 2020-12-17T08:00:00Z | 2020-12-16T13:00:00Z | 2020-12-20T22:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-10T05:00:00Z | 11997 | 216 | 2021-04-10T05:00:00Z | +2199.110000 | 2021-04-10T04:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 2 | 1 | 2021-04-13T12:00:00Z | 12076 | 218 | 2021-04-13T12:00:00Z | +2235.430000 | 2021-04-13T08:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-06-08T00:00:00Z | 1 | -1 | 2021-06-22T14:00:00Z | 13758 | 237 | 2021-06-22T14:00:00Z | +1726.490000 | 2021-06-22T12:00:00Z | 2021-06-18T19:00:00Z | 2021-06-27T23:00:00Z | no | no | yes | yes |
| ETHUSDT | 2021-06-08T00:00:00Z | 2 | -1 | 2021-06-25T15:00:00Z | 13831 | 242 | 2021-06-25T15:00:00Z | +1823.650000 | 2021-06-25T12:00:00Z | 2021-06-18T19:00:00Z | 2021-06-27T23:00:00Z | no | no | yes | yes |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | 1 | 2021-09-01T13:00:00Z | 15461 | 277 | 2021-09-01T13:00:00Z | +3537.600000 | 2021-09-01T12:00:00Z | 2021-08-31T09:00:00Z | 2021-09-07T09:00:00Z | no | no | yes | yes |
| ETHUSDT | 2024-10-08T08:00:00Z | 1 | -1 | 2024-10-09T21:00:00Z | 42685 | 822 | 2024-10-09T21:00:00Z | +2355.010000 | 2024-10-09T20:00:00Z | 2024-10-08T16:00:00Z | 2024-10-11T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-01-26T20:00:00Z | 1 | -1 | 2025-01-27T07:00:00Z | 45311 | 868 | 2025-01-27T07:00:00Z | +3082.750000 | 2025-01-27T04:00:00Z | 2025-01-27T03:00:00Z | 2025-01-30T04:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T06:00:00Z | 46006 | 875 | 2025-02-25T06:00:00Z | +2505.040000 | 2025-02-25T04:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 46043 | 877 | 2025-02-26T19:00:00Z | +2291.640000 | 2025-02-26T16:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-24T19:00:00Z | 50339 | 953 | 2025-08-24T19:00:00Z | +4932.840000 | 2025-08-24T16:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| ETHUSDT | 2025-10-29T16:00:00Z | 1 | -1 | 2025-10-30T14:00:00Z | 51942 | 989 | 2025-10-30T14:00:00Z | +3764.660000 | 2025-10-30T12:00:00Z | 2025-10-30T13:00:00Z | 2025-11-07T19:00:00Z | no | no | no | no |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | 1 | 2026-09-21T01:00:00Z | 59753 | 1165 | 2026-09-21T01:00:00Z | +2688.100000 | 2026-09-21T00:00:00Z | 2026-09-18T14:00:00Z | 2026-09-23T15:00:00Z | no | no | no | no |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | 1 | 2020-12-31T10:00:00Z | 1849 | 57 | 2020-12-31T10:00:00Z | +1.296300 | 2020-12-31T08:00:00Z | 2020-12-31T10:00:00Z | 2021-01-04T08:00:00Z | no | no | no | yes |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | 1 | 2021-04-06T15:00:00Z | 4158 | 109 | 2021-04-06T15:00:00Z | +7.198900 | 2021-04-06T12:00:00Z | 2021-04-06T05:00:00Z | 2021-04-07T12:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | 1 | 2022-01-13T15:00:00Z | 10926 | 239 | 2022-01-13T15:00:00Z | +19.338600 | 2022-01-13T12:00:00Z | 2022-01-13T14:00:00Z | 2022-01-17T17:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-02-17T16:00:00Z | 1 | -1 | 2022-02-24T04:00:00Z | 11923 | 265 | 2022-02-24T04:00:00Z | +7.784000 | 2022-02-24T00:00:00Z | 2022-02-19T12:00:00Z | 2022-02-26T01:00:00Z | no | no | no | yes |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T14:00:00Z | 38261 | 862 | 2025-02-25T14:00:00Z | +2.903000 | 2025-02-25T12:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | 1 | 2025-05-22T15:00:00Z | 40326 | 906 | 2025-05-22T15:00:00Z | +3.031000 | 2025-05-22T12:00:00Z | 2025-05-22T08:00:00Z | 2025-05-25T00:00:00Z | no | no | no | no |
| NEARUSDT | 2025-06-12T20:00:00Z | 1 | -1 | 2025-06-13T01:00:00Z | 40840 | 918 | 2025-06-13T01:00:00Z | +2.238000 | 2025-06-13T00:00:00Z | 2025-06-13T01:00:00Z | 2025-06-16T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | 1 | 2025-08-13T10:00:00Z | 42313 | 951 | 2025-08-13T10:00:00Z | +2.917000 | 2025-08-13T08:00:00Z | 2025-08-13T10:00:00Z | 2025-08-15T16:00:00Z | no | no | no | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 1 | -1 | 2025-12-15T16:00:00Z | 45295 | 1032 | 2025-12-15T16:00:00Z | +1.532000 | 2025-12-15T12:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 2 | -1 | 2025-12-18T01:00:00Z | 45352 | 1033 | 2025-12-18T01:00:00Z | +1.482000 | 2025-12-18T00:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | 1 | 2026-05-21T20:00:00Z | 49067 | 1106 | 2026-05-21T20:00:00Z | +1.923000 | 2026-05-21T16:00:00Z | 2026-05-21T02:00:00Z | 2026-05-26T19:00:00Z | no | no | no | no |
| NEARUSDT | 2026-07-22T00:00:00Z | 1 | -1 | 2026-07-22T13:00:00Z | 50548 | 1138 | 2026-07-22T13:00:00Z | +1.883000 | 2026-07-22T12:00:00Z | 2026-07-22T08:00:00Z | 2026-07-27T00:00:00Z | no | no | no | no |
| SOLUSDT | 2020-12-04T16:00:00Z | 1 | -1 | 2020-12-04T23:00:00Z | 1959 | 54 | 2020-12-04T23:00:00Z | +1.846800 | 2020-12-04T20:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2020-12-04T16:00:00Z | 2 | -1 | 2020-12-08T09:00:00Z | 2041 | 56 | 2020-12-08T09:00:00Z | +1.735400 | 2020-12-08T08:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | 1 | 2021-03-30T03:00:00Z | 4723 | 122 | 2021-03-30T03:00:00Z | +19.856100 | 2021-03-30T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 2 | 1 | 2021-04-03T04:00:00Z | 4820 | 125 | 2021-04-03T04:00:00Z | +21.106400 | 2021-04-03T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | 1 | 2021-10-21T01:00:00Z | 9641 | 198 | 2021-10-21T01:00:00Z | +185.717000 | 2021-10-21T00:00:00Z | 2021-10-20T16:00:00Z | 2021-10-24T12:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-01-17T08:00:00Z | 1 | -1 | 2022-01-21T00:00:00Z | 11848 | 241 | 2022-01-21T00:00:00Z | +127.450000 | 2022-01-20T20:00:00Z | 2022-01-18T15:00:00Z | 2022-01-25T19:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-02-17T12:00:00Z | 1 | -1 | 2022-02-17T19:00:00Z | 12515 | 264 | 2022-02-17T19:00:00Z | +95.120000 | 2022-02-17T16:00:00Z | 2022-02-17T19:00:00Z | 2022-02-21T02:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 1 | -1 | 2022-12-17T02:00:00Z | 19770 | 445 | 2022-12-17T02:00:00Z | +12.100000 | 2022-12-17T00:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 2 | -1 | 2022-12-24T06:00:00Z | 19942 | 447 | 2022-12-24T06:00:00Z | +11.354000 | 2022-12-24T04:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T12:00:00Z | 36436 | 763 | 2024-11-10T12:00:00Z | +206.780000 | 2024-11-10T08:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-11T15:00:00Z | 36463 | 765 | 2024-11-11T15:00:00Z | +218.930000 | 2024-11-11T12:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 1 | -1 | 2025-11-16T17:00:00Z | 45345 | 977 | 2025-11-16T17:00:00Z | +135.640000 | 2025-11-16T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 2 | -1 | 2025-11-17T19:00:00Z | 45371 | 978 | 2025-11-17T19:00:00Z | +130.440000 | 2025-11-17T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-12-11T04:00:00Z | 1 | -1 | 2025-12-18T20:00:00Z | 46116 | 1004 | 2025-12-18T20:00:00Z | +117.470000 | 2025-12-18T16:00:00Z | 2025-12-18T18:00:00Z | 2025-12-22T01:00:00Z | no | no | yes | no |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | 1 | 2020-06-23T17:00:00Z | 3344 | 58 | 2020-06-23T17:00:00Z | +58.500000 | 2020-06-23T16:00:00Z | 2020-06-23T13:00:00Z | 2020-06-27T16:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | 1 | 2020-07-29T16:00:00Z | 4207 | 79 | 2020-07-29T16:00:00Z | +72.900000 | 2020-07-29T12:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 2 | 1 | 2020-08-01T00:00:00Z | 4263 | 80 | 2020-08-01T00:00:00Z | +75.000000 | 2020-07-31T20:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-12-29T16:00:00Z | 1 | -1 | 2021-01-01T19:00:00Z | 7954 | 151 | 2021-01-01T19:00:00Z | +57.080000 | 2021-01-01T16:00:00Z | 2021-01-01T19:00:00Z | 2021-01-03T15:00:00Z | no | no | yes | yes |
| ZECUSDT | 2022-09-13T12:00:00Z | 1 | -1 | 2022-09-18T22:00:00Z | 22957 | 421 | 2022-09-18T22:00:00Z | +53.190000 | 2022-09-18T20:00:00Z | 2022-09-18T22:00:00Z | 2022-09-21T19:00:00Z | no | no | no | yes |
| ZECUSDT | 2022-10-07T00:00:00Z | 1 | -1 | 2022-10-11T01:00:00Z | 23488 | 436 | 2022-10-11T01:00:00Z | +52.080000 | 2022-10-11T00:00:00Z | 2022-10-07T13:00:00Z | 2022-10-16T06:00:00Z | no | no | no | yes |
| ZECUSDT | 2023-08-15T08:00:00Z | 1 | -1 | 2023-08-15T20:00:00Z | 30899 | 596 | 2023-08-15T20:00:00Z | +27.540000 | 2023-08-15T16:00:00Z | 2023-08-15T20:00:00Z | 2023-08-20T21:00:00Z | no | no | no | yes |
| ZECUSDT | 2024-09-29T00:00:00Z | 1 | -1 | 2024-10-01T23:00:00Z | 40814 | 737 | 2024-10-01T23:00:00Z | +26.440000 | 2024-10-01T20:00:00Z | 2024-09-30T01:00:00Z | 2024-10-04T14:00:00Z | no | no | no | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-23T09:00:00Z | 42072 | 763 | 2024-11-23T09:00:00Z | +48.200000 | 2024-11-23T08:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-01-19T04:00:00Z | 1 | -1 | 2025-01-19T12:00:00Z | 43443 | 797 | 2025-01-19T12:00:00Z | +47.790000 | 2025-01-19T08:00:00Z | 2025-01-19T10:00:00Z | 2025-01-19T16:00:00Z | no | no | no | no |
| ZECUSDT | 2025-04-13T20:00:00Z | 1 | -1 | 2025-04-15T03:00:00Z | 45498 | 841 | 2025-04-15T03:00:00Z | +30.430000 | 2025-04-15T00:00:00Z | 2025-04-14T16:00:00Z | 2025-04-20T04:00:00Z | no | no | no | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | 1 | 2025-09-06T20:00:00Z | 48971 | 902 | 2025-09-06T20:00:00Z | +43.810000 | 2025-09-06T16:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | 1 | 2025-12-27T10:00:00Z | 51649 | 944 | 2025-12-27T10:00:00Z | +486.020000 | 2025-12-27T08:00:00Z | 2025-12-27T02:00:00Z | 2025-12-31T13:00:00Z | no | no | no | no |
| ZECUSDT | 2026-03-26T08:00:00Z | 1 | -1 | 2026-03-27T18:00:00Z | 53817 | 989 | 2026-03-27T18:00:00Z | +215.340000 | 2026-03-27T16:00:00Z | 2026-03-27T12:00:00Z | 2026-03-30T05:00:00Z | no | no | no | no |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | 1 | 2026-05-09T03:00:00Z | 54834 | 1009 | 2026-05-09T03:00:00Z | +618.490000 | 2026-05-09T00:00:00Z | 2026-05-01T16:00:00Z | 2026-05-10T21:00:00Z | no | no | no | no |

### P-ADD-BRK · tierE__frozen3 (51 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | 1 | 2020-08-17T16:00:00Z | 8254 | 73 | 2020-08-17T16:00:00Z | +12443.990000 | 2020-08-17T12:00:00Z | 2020-08-17T14:00:00Z | 2020-08-19T05:00:00Z | no | no | no | no |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | 1 | 2021-11-08T01:00:00Z | 18991 | 158 | 2021-11-08T01:00:00Z | +65097.190000 | 2021-11-08T00:00:00Z | 2021-11-08T00:00:00Z | 2021-11-10T21:00:00Z | no | no | no | no |
| BTCUSDT | 2023-09-01T04:00:00Z | 1 | -1 | 2023-09-01T18:00:00Z | 34896 | 284 | 2023-09-01T18:00:00Z | +25467.200000 | 2023-09-01T16:00:00Z | 2023-09-01T16:00:00Z | 2023-09-06T18:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 1 | -1 | 2025-02-25T00:00:00Z | 47910 | 425 | 2025-02-25T00:00:00Z | +91514.500000 | 2025-02-24T20:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | 1 | 2025-07-09T20:00:00Z | 51146 | 459 | 2025-07-09T20:00:00Z | +111718.800000 | 2025-07-09T16:00:00Z | 2025-07-09T20:00:00Z | 2025-07-15T05:00:00Z | no | no | yes | no |
| BTCUSDT | 2026-03-26T12:00:00Z | 1 | -1 | 2026-03-27T11:00:00Z | 57401 | 517 | 2026-03-27T11:00:00Z | +66456.400000 | 2026-03-27T08:00:00Z | 2026-03-27T10:00:00Z | 2026-03-30T06:00:00Z | no | no | no | no |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | 1 | 2020-06-02T07:00:00Z | 4511 | 52 | 2020-06-02T07:00:00Z | +248.150000 | 2020-06-02T04:00:00Z | 2020-05-28T23:00:00Z | 2020-06-02T15:00:00Z | no | no | no | no |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-05T22:00:00Z | 8270 | 92 | 2020-11-05T22:00:00Z | +413.950000 | 2020-11-05T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | no |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | 1 | 2020-12-17T11:00:00Z | 9267 | 99 | 2020-12-17T11:00:00Z | +670.420000 | 2020-12-17T08:00:00Z | 2020-12-16T13:00:00Z | 2020-12-20T22:00:00Z | no | no | no | no |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-10T05:00:00Z | 11997 | 128 | 2021-04-10T05:00:00Z | +2199.110000 | 2021-04-10T04:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | no |
| ETHUSDT | 2021-06-08T00:00:00Z | 1 | -1 | 2021-06-22T14:00:00Z | 13758 | 137 | 2021-06-22T14:00:00Z | +1726.490000 | 2021-06-22T12:00:00Z | 2021-06-18T19:00:00Z | 2021-06-27T23:00:00Z | no | no | yes | no |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | 1 | 2021-09-01T13:00:00Z | 15461 | 164 | 2021-09-01T13:00:00Z | +3537.600000 | 2021-09-01T12:00:00Z | 2021-08-31T09:00:00Z | 2021-09-07T09:00:00Z | no | no | yes | no |
| ETHUSDT | 2023-07-13T12:00:00Z | 1 | 1 | 2023-07-13T18:00:00Z | 31786 | 313 | 2023-07-13T18:00:00Z | +1988.750000 | 2023-07-13T16:00:00Z | 2023-07-13T18:00:00Z | 2023-07-17T11:00:00Z | no | no | no | no |
| ETHUSDT | 2023-09-01T04:00:00Z | 1 | -1 | 2023-09-01T18:00:00Z | 32986 | 324 | 2023-09-01T18:00:00Z | +1605.500000 | 2023-09-01T16:00:00Z | 2023-09-01T15:00:00Z | 2023-09-06T18:00:00Z | no | no | no | no |
| ETHUSDT | 2025-01-26T20:00:00Z | 1 | -1 | 2025-01-27T06:00:00Z | 45310 | 468 | 2025-01-27T06:00:00Z | +3139.760000 | 2025-01-27T04:00:00Z | 2025-01-27T03:00:00Z | 2025-01-30T04:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T06:00:00Z | 46006 | 473 | 2025-02-25T06:00:00Z | +2505.040000 | 2025-02-25T04:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-10-29T16:00:00Z | 1 | -1 | 2025-11-04T13:00:00Z | 52061 | 521 | 2025-11-04T13:00:00Z | +3509.560000 | 2025-11-04T12:00:00Z | 2025-10-30T13:00:00Z | 2025-11-07T19:00:00Z | no | no | no | no |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | 1 | 2026-09-18T18:00:00Z | 59698 | 615 | 2026-09-18T18:00:00Z | +2606.240000 | 2026-09-18T16:00:00Z | 2026-09-18T14:00:00Z | 2026-09-23T15:00:00Z | no | no | no | no |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | 1 | 2021-04-06T15:00:00Z | 4158 | 41 | 2021-04-06T15:00:00Z | +7.198900 | 2021-04-06T12:00:00Z | 2021-04-06T05:00:00Z | 2021-04-07T12:00:00Z | no | no | no | no |
| NEARUSDT | 2021-11-08T20:00:00Z | 1 | 1 | 2021-11-10T01:00:00Z | 9376 | 100 | 2021-11-10T01:00:00Z | +11.333800 | 2021-11-10T00:00:00Z | 2021-11-09T18:00:00Z | 2021-11-10T21:00:00Z | no | no | no | no |
| NEARUSDT | 2022-02-17T16:00:00Z | 1 | -1 | 2022-02-20T06:00:00Z | 11829 | 127 | 2022-02-20T06:00:00Z | +9.549000 | 2022-02-20T04:00:00Z | 2022-02-19T12:00:00Z | 2022-02-26T01:00:00Z | no | no | no | no |
| NEARUSDT | 2022-02-17T16:00:00Z | 2 | -1 | 2022-02-24T04:00:00Z | 11923 | 129 | 2022-02-24T04:00:00Z | +7.784000 | 2022-02-24T00:00:00Z | 2022-02-19T12:00:00Z | 2022-02-26T01:00:00Z | no | no | no | no |
| NEARUSDT | 2022-06-28T04:00:00Z | 1 | -1 | 2022-06-30T14:00:00Z | 14957 | 151 | 2022-06-30T14:00:00Z | +3.142000 | 2022-06-30T12:00:00Z | 2022-06-28T18:00:00Z | 2022-07-04T13:00:00Z | no | no | no | no |
| NEARUSDT | 2023-02-08T04:00:00Z | 1 | 1 | 2023-02-08T13:00:00Z | 20308 | 212 | 2023-02-08T13:00:00Z | +2.719000 | 2023-02-08T12:00:00Z | 2023-02-08T13:00:00Z | 2023-02-09T20:00:00Z | no | no | no | no |
| NEARUSDT | 2024-07-03T20:00:00Z | 1 | -1 | 2024-07-05T01:00:00Z | 32608 | 343 | 2024-07-05T01:00:00Z | +4.474000 | 2024-07-05T00:00:00Z | 2024-07-05T00:00:00Z | 2024-07-10T12:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T14:00:00Z | 38261 | 385 | 2025-02-25T14:00:00Z | +2.903000 | 2025-02-25T12:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | 1 | 2025-05-22T15:00:00Z | 40326 | 407 | 2025-05-22T15:00:00Z | +3.031000 | 2025-05-22T12:00:00Z | 2025-05-22T08:00:00Z | 2025-05-25T00:00:00Z | no | no | no | no |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | 1 | 2025-08-13T10:00:00Z | 42313 | 429 | 2025-08-13T10:00:00Z | +2.917000 | 2025-08-13T08:00:00Z | 2025-08-13T10:00:00Z | 2025-08-15T16:00:00Z | no | no | no | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 1 | -1 | 2025-12-15T16:00:00Z | 45295 | 475 | 2025-12-15T16:00:00Z | +1.532000 | 2025-12-15T12:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | 1 | 2026-05-21T20:00:00Z | 49067 | 512 | 2026-05-21T20:00:00Z | +1.923000 | 2026-05-21T16:00:00Z | 2026-05-21T02:00:00Z | 2026-05-26T19:00:00Z | no | no | no | no |
| SOLUSDT | 2020-12-04T16:00:00Z | 1 | -1 | 2020-12-08T10:00:00Z | 2042 | 19 | 2020-12-08T10:00:00Z | +1.676000 | 2020-12-08T08:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | no |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | 1 | 2021-04-03T04:00:00Z | 4820 | 67 | 2021-04-03T04:00:00Z | +21.106400 | 2021-04-03T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | no |
| SOLUSDT | 2022-01-17T08:00:00Z | 1 | -1 | 2022-01-21T00:00:00Z | 11848 | 117 | 2022-01-21T00:00:00Z | +127.450000 | 2022-01-20T20:00:00Z | 2022-01-18T15:00:00Z | 2022-01-25T19:00:00Z | no | no | no | no |
| SOLUSDT | 2022-02-17T12:00:00Z | 1 | -1 | 2022-02-20T06:00:00Z | 12574 | 125 | 2022-02-20T06:00:00Z | +86.550000 | 2022-02-20T04:00:00Z | 2022-02-17T19:00:00Z | 2022-02-21T02:00:00Z | no | no | no | no |
| SOLUSDT | 2022-10-18T20:00:00Z | 1 | -1 | 2022-10-21T00:00:00Z | 18400 | 185 | 2022-10-21T00:00:00Z | +28.000000 | 2022-10-20T20:00:00Z | 2022-10-20T01:00:00Z | 2022-10-23T04:00:00Z | no | no | no | no |
| SOLUSDT | 2022-12-16T16:00:00Z | 1 | -1 | 2022-12-17T02:00:00Z | 19770 | 207 | 2022-12-17T02:00:00Z | +12.100000 | 2022-12-17T00:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | no |
| SOLUSDT | 2022-12-16T16:00:00Z | 2 | -1 | 2022-12-24T06:00:00Z | 19942 | 210 | 2022-12-24T06:00:00Z | +11.354000 | 2022-12-24T04:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | no |
| SOLUSDT | 2024-04-25T08:00:00Z | 1 | -1 | 2024-04-30T10:00:00Z | 31778 | 338 | 2024-04-30T10:00:00Z | +130.061000 | 2024-04-30T08:00:00Z | 2024-04-26T23:00:00Z | 2024-05-02T12:00:00Z | no | no | no | no |
| SOLUSDT | 2025-12-11T04:00:00Z | 1 | -1 | 2025-12-18T20:00:00Z | 46116 | 493 | 2025-12-18T20:00:00Z | +117.470000 | 2025-12-18T16:00:00Z | 2025-12-18T18:00:00Z | 2025-12-22T01:00:00Z | no | no | yes | no |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | 1 | 2020-06-23T17:00:00Z | 3344 | 38 | 2020-06-23T17:00:00Z | +58.500000 | 2020-06-23T16:00:00Z | 2020-06-23T13:00:00Z | 2020-06-27T16:00:00Z | no | no | no | no |
| ZECUSDT | 2022-09-13T12:00:00Z | 1 | -1 | 2022-09-18T22:00:00Z | 22957 | 227 | 2022-09-18T22:00:00Z | +53.190000 | 2022-09-18T20:00:00Z | 2022-09-18T22:00:00Z | 2022-09-21T19:00:00Z | no | no | no | no |
| ZECUSDT | 2022-10-07T00:00:00Z | 1 | -1 | 2022-10-11T01:00:00Z | 23488 | 237 | 2022-10-11T01:00:00Z | +52.080000 | 2022-10-11T00:00:00Z | 2022-10-07T13:00:00Z | 2022-10-16T06:00:00Z | no | no | no | no |
| ZECUSDT | 2023-08-15T08:00:00Z | 1 | -1 | 2023-08-15T20:00:00Z | 30899 | 311 | 2023-08-15T20:00:00Z | +27.540000 | 2023-08-15T16:00:00Z | 2023-08-15T20:00:00Z | 2023-08-20T21:00:00Z | no | no | no | no |
| ZECUSDT | 2024-09-29T00:00:00Z | 1 | -1 | 2024-10-01T23:00:00Z | 40814 | 404 | 2024-10-01T23:00:00Z | +26.440000 | 2024-10-01T20:00:00Z | 2024-09-30T01:00:00Z | 2024-10-04T14:00:00Z | no | no | no | no |
| ZECUSDT | 2024-10-28T08:00:00Z | 1 | 1 | 2024-10-29T03:00:00Z | 41466 | 413 | 2024-10-29T03:00:00Z | +40.890000 | 2024-10-29T00:00:00Z | 2024-10-29T03:00:00Z | 2024-10-29T06:00:00Z | no | no | no | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-24T02:00:00Z | 42089 | 419 | 2024-11-24T02:00:00Z | +52.470000 | 2024-11-24T00:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-04-13T20:00:00Z | 1 | -1 | 2025-04-15T03:00:00Z | 45498 | 465 | 2025-04-15T03:00:00Z | +30.430000 | 2025-04-15T00:00:00Z | 2025-04-14T16:00:00Z | 2025-04-20T04:00:00Z | no | no | no | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | 1 | 2025-09-06T22:00:00Z | 48973 | 498 | 2025-09-06T22:00:00Z | +45.450000 | 2025-09-06T20:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | 1 | 2025-12-27T10:00:00Z | 51649 | 526 | 2025-12-27T10:00:00Z | +486.020000 | 2025-12-27T08:00:00Z | 2025-12-27T02:00:00Z | 2025-12-31T13:00:00Z | no | no | no | no |
| ZECUSDT | 2026-03-26T08:00:00Z | 1 | -1 | 2026-03-27T18:00:00Z | 53817 | 552 | 2026-03-27T18:00:00Z | +215.340000 | 2026-03-27T16:00:00Z | 2026-03-27T12:00:00Z | 2026-03-30T05:00:00Z | no | no | no | no |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | 1 | 2026-05-01T18:00:00Z | 54657 | 560 | 2026-05-01T18:00:00Z | +385.510000 | 2026-05-01T16:00:00Z | 2026-05-01T16:00:00Z | 2026-05-10T21:00:00Z | no | no | no | no |

### P-ADD-BRK · tierE__refuse_below_entry (66 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | 1 | 2020-08-17T16:00:00Z | 8254 | 167 | 2020-08-17T16:00:00Z | +12443.990000 | 2020-08-17T12:00:00Z | 2020-08-17T14:00:00Z | 2020-08-19T05:00:00Z | no | no | no | yes |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | 1 | 2020-12-03T16:00:00Z | 10846 | 224 | 2020-12-03T16:00:00Z | +19560.910000 | 2020-12-03T12:00:00Z | 2020-11-30T01:00:00Z | 2020-12-04T23:00:00Z | no | no | no | yes |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | 1 | 2021-11-08T01:00:00Z | 18991 | 405 | 2021-11-08T01:00:00Z | +65097.190000 | 2021-11-08T00:00:00Z | 2021-11-08T00:00:00Z | 2021-11-10T21:00:00Z | no | no | no | yes |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T05:00:00Z | 45347 | 946 | 2024-11-10T05:00:00Z | +79273.700000 | 2024-11-10T04:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-13T15:00:00Z | 45429 | 950 | 2024-11-13T15:00:00Z | +91563.000000 | 2024-11-13T12:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 1 | -1 | 2025-02-25T00:00:00Z | 47910 | 989 | 2025-02-25T00:00:00Z | +91514.500000 | 2025-02-24T20:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 47953 | 991 | 2025-02-26T19:00:00Z | +84204.900000 | 2025-02-26T16:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | 1 | 2025-07-09T20:00:00Z | 51146 | 1070 | 2025-07-09T20:00:00Z | +111718.800000 | 2025-07-09T16:00:00Z | 2025-07-09T20:00:00Z | 2025-07-15T05:00:00Z | no | no | yes | no |
| BTCUSDT | 2025-07-02T12:00:00Z | 2 | 1 | 2025-07-13T21:00:00Z | 51243 | 1074 | 2025-07-13T21:00:00Z | +119028.700000 | 2025-07-13T20:00:00Z | 2025-07-09T20:00:00Z | 2025-07-15T05:00:00Z | no | no | yes | no |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | 1 | 2020-06-02T07:00:00Z | 4511 | 88 | 2020-06-02T07:00:00Z | +248.150000 | 2020-06-02T04:00:00Z | 2020-05-28T23:00:00Z | 2020-06-02T15:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-05T22:00:00Z | 8270 | 155 | 2020-11-05T22:00:00Z | +413.950000 | 2020-11-05T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 2 | 1 | 2020-11-11T08:00:00Z | 8400 | 158 | 2020-11-11T08:00:00Z | +462.520000 | 2020-11-11T04:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | 1 | 2020-12-17T11:00:00Z | 9267 | 166 | 2020-12-17T11:00:00Z | +670.420000 | 2020-12-17T08:00:00Z | 2020-12-16T13:00:00Z | 2020-12-20T22:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-10T05:00:00Z | 11997 | 216 | 2021-04-10T05:00:00Z | +2199.110000 | 2021-04-10T04:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 2 | 1 | 2021-04-13T12:00:00Z | 12076 | 218 | 2021-04-13T12:00:00Z | +2235.430000 | 2021-04-13T08:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-06-08T00:00:00Z | 1 | -1 | 2021-06-22T14:00:00Z | 13758 | 237 | 2021-06-22T14:00:00Z | +1726.490000 | 2021-06-22T12:00:00Z | 2021-06-18T19:00:00Z | 2021-06-27T23:00:00Z | no | no | yes | yes |
| ETHUSDT | 2021-06-08T00:00:00Z | 2 | -1 | 2021-06-25T15:00:00Z | 13831 | 242 | 2021-06-25T15:00:00Z | +1823.650000 | 2021-06-25T12:00:00Z | 2021-06-18T19:00:00Z | 2021-06-27T23:00:00Z | no | no | yes | yes |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | 1 | 2021-09-01T13:00:00Z | 15461 | 277 | 2021-09-01T13:00:00Z | +3537.600000 | 2021-09-01T12:00:00Z | 2021-08-31T09:00:00Z | 2021-09-07T09:00:00Z | no | no | yes | yes |
| ETHUSDT | 2024-10-08T08:00:00Z | 1 | -1 | 2024-10-09T21:00:00Z | 42685 | 822 | 2024-10-09T21:00:00Z | +2355.010000 | 2024-10-09T20:00:00Z | 2024-10-08T16:00:00Z | 2024-10-11T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-01-26T20:00:00Z | 1 | -1 | 2025-01-27T07:00:00Z | 45311 | 868 | 2025-01-27T07:00:00Z | +3082.750000 | 2025-01-27T04:00:00Z | 2025-01-27T03:00:00Z | 2025-01-30T04:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T06:00:00Z | 46006 | 875 | 2025-02-25T06:00:00Z | +2505.040000 | 2025-02-25T04:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 46043 | 877 | 2025-02-26T19:00:00Z | +2291.640000 | 2025-02-26T16:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-24T19:00:00Z | 50339 | 953 | 2025-08-24T19:00:00Z | +4932.840000 | 2025-08-24T16:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| ETHUSDT | 2025-10-29T16:00:00Z | 1 | -1 | 2025-10-30T14:00:00Z | 51942 | 989 | 2025-10-30T14:00:00Z | +3764.660000 | 2025-10-30T12:00:00Z | 2025-10-30T13:00:00Z | 2025-11-07T19:00:00Z | no | no | no | no |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | 1 | 2026-09-21T01:00:00Z | 59753 | 1165 | 2026-09-21T01:00:00Z | +2688.100000 | 2026-09-21T00:00:00Z | 2026-09-18T14:00:00Z | 2026-09-23T15:00:00Z | no | no | no | no |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | 1 | 2020-12-31T10:00:00Z | 1849 | 57 | 2020-12-31T10:00:00Z | +1.296300 | 2020-12-31T08:00:00Z | 2020-12-31T10:00:00Z | 2021-01-04T08:00:00Z | no | no | no | yes |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | 1 | 2021-04-06T15:00:00Z | 4158 | 109 | 2021-04-06T15:00:00Z | +7.198900 | 2021-04-06T12:00:00Z | 2021-04-06T05:00:00Z | 2021-04-07T12:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | 1 | 2022-01-13T15:00:00Z | 10926 | 239 | 2022-01-13T15:00:00Z | +19.338600 | 2022-01-13T12:00:00Z | 2022-01-13T14:00:00Z | 2022-01-17T17:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-02-17T16:00:00Z | 1 | -1 | 2022-02-24T04:00:00Z | 11923 | 265 | 2022-02-24T04:00:00Z | +7.784000 | 2022-02-24T00:00:00Z | 2022-02-19T12:00:00Z | 2022-02-26T01:00:00Z | no | no | no | yes |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T14:00:00Z | 38261 | 862 | 2025-02-25T14:00:00Z | +2.903000 | 2025-02-25T12:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | 1 | 2025-05-22T15:00:00Z | 40326 | 906 | 2025-05-22T15:00:00Z | +3.031000 | 2025-05-22T12:00:00Z | 2025-05-22T08:00:00Z | 2025-05-25T00:00:00Z | no | no | no | no |
| NEARUSDT | 2025-06-12T20:00:00Z | 1 | -1 | 2025-06-13T01:00:00Z | 40840 | 918 | 2025-06-13T01:00:00Z | +2.238000 | 2025-06-13T00:00:00Z | 2025-06-13T01:00:00Z | 2025-06-16T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | 1 | 2025-08-13T10:00:00Z | 42313 | 951 | 2025-08-13T10:00:00Z | +2.917000 | 2025-08-13T08:00:00Z | 2025-08-13T10:00:00Z | 2025-08-15T16:00:00Z | no | no | no | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 1 | -1 | 2025-12-15T16:00:00Z | 45295 | 1032 | 2025-12-15T16:00:00Z | +1.532000 | 2025-12-15T12:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 2 | -1 | 2025-12-18T01:00:00Z | 45352 | 1033 | 2025-12-18T01:00:00Z | +1.482000 | 2025-12-18T00:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | 1 | 2026-05-21T20:00:00Z | 49067 | 1106 | 2026-05-21T20:00:00Z | +1.923000 | 2026-05-21T16:00:00Z | 2026-05-21T02:00:00Z | 2026-05-26T19:00:00Z | no | no | no | no |
| NEARUSDT | 2026-07-22T00:00:00Z | 1 | -1 | 2026-07-22T13:00:00Z | 50548 | 1138 | 2026-07-22T13:00:00Z | +1.883000 | 2026-07-22T12:00:00Z | 2026-07-22T08:00:00Z | 2026-07-27T00:00:00Z | no | no | no | no |
| SOLUSDT | 2020-12-04T16:00:00Z | 1 | -1 | 2020-12-04T23:00:00Z | 1959 | 54 | 2020-12-04T23:00:00Z | +1.846800 | 2020-12-04T20:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2020-12-04T16:00:00Z | 2 | -1 | 2020-12-08T09:00:00Z | 2041 | 56 | 2020-12-08T09:00:00Z | +1.735400 | 2020-12-08T08:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | 1 | 2021-03-30T03:00:00Z | 4723 | 122 | 2021-03-30T03:00:00Z | +19.856100 | 2021-03-30T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 2 | 1 | 2021-04-03T04:00:00Z | 4820 | 125 | 2021-04-03T04:00:00Z | +21.106400 | 2021-04-03T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | 1 | 2021-10-21T01:00:00Z | 9641 | 198 | 2021-10-21T01:00:00Z | +185.717000 | 2021-10-21T00:00:00Z | 2021-10-20T16:00:00Z | 2021-10-24T12:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-01-17T08:00:00Z | 1 | -1 | 2022-01-21T00:00:00Z | 11848 | 241 | 2022-01-21T00:00:00Z | +127.450000 | 2022-01-20T20:00:00Z | 2022-01-18T15:00:00Z | 2022-01-25T19:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-02-17T12:00:00Z | 1 | -1 | 2022-02-17T19:00:00Z | 12515 | 264 | 2022-02-17T19:00:00Z | +95.120000 | 2022-02-17T16:00:00Z | 2022-02-17T19:00:00Z | 2022-02-21T02:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 1 | -1 | 2022-12-17T02:00:00Z | 19770 | 445 | 2022-12-17T02:00:00Z | +12.100000 | 2022-12-17T00:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 2 | -1 | 2022-12-24T06:00:00Z | 19942 | 447 | 2022-12-24T06:00:00Z | +11.354000 | 2022-12-24T04:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T12:00:00Z | 36436 | 763 | 2024-11-10T12:00:00Z | +206.780000 | 2024-11-10T08:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-11T15:00:00Z | 36463 | 765 | 2024-11-11T15:00:00Z | +218.930000 | 2024-11-11T12:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 1 | -1 | 2025-11-16T17:00:00Z | 45345 | 977 | 2025-11-16T17:00:00Z | +135.640000 | 2025-11-16T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 2 | -1 | 2025-11-17T19:00:00Z | 45371 | 978 | 2025-11-17T19:00:00Z | +130.440000 | 2025-11-17T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-12-11T04:00:00Z | 1 | -1 | 2025-12-18T20:00:00Z | 46116 | 1004 | 2025-12-18T20:00:00Z | +117.470000 | 2025-12-18T16:00:00Z | 2025-12-18T18:00:00Z | 2025-12-22T01:00:00Z | no | no | yes | no |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | 1 | 2020-06-23T17:00:00Z | 3344 | 58 | 2020-06-23T17:00:00Z | +58.500000 | 2020-06-23T16:00:00Z | 2020-06-23T13:00:00Z | 2020-06-27T16:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | 1 | 2020-07-29T16:00:00Z | 4207 | 79 | 2020-07-29T16:00:00Z | +72.900000 | 2020-07-29T12:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 2 | 1 | 2020-08-01T00:00:00Z | 4263 | 80 | 2020-08-01T00:00:00Z | +75.000000 | 2020-07-31T20:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-12-29T16:00:00Z | 1 | -1 | 2021-01-01T19:00:00Z | 7954 | 151 | 2021-01-01T19:00:00Z | +57.080000 | 2021-01-01T16:00:00Z | 2021-01-01T19:00:00Z | 2021-01-03T15:00:00Z | no | no | yes | yes |
| ZECUSDT | 2022-09-13T12:00:00Z | 1 | -1 | 2022-09-18T22:00:00Z | 22957 | 421 | 2022-09-18T22:00:00Z | +53.190000 | 2022-09-18T20:00:00Z | 2022-09-18T22:00:00Z | 2022-09-21T19:00:00Z | no | no | no | yes |
| ZECUSDT | 2022-10-07T00:00:00Z | 1 | -1 | 2022-10-11T01:00:00Z | 23488 | 436 | 2022-10-11T01:00:00Z | +52.080000 | 2022-10-11T00:00:00Z | 2022-10-07T13:00:00Z | 2022-10-16T06:00:00Z | no | no | no | yes |
| ZECUSDT | 2023-08-15T08:00:00Z | 1 | -1 | 2023-08-15T20:00:00Z | 30899 | 596 | 2023-08-15T20:00:00Z | +27.540000 | 2023-08-15T16:00:00Z | 2023-08-15T20:00:00Z | 2023-08-20T21:00:00Z | no | no | no | yes |
| ZECUSDT | 2024-09-29T00:00:00Z | 1 | -1 | 2024-10-01T23:00:00Z | 40814 | 737 | 2024-10-01T23:00:00Z | +26.440000 | 2024-10-01T20:00:00Z | 2024-09-30T01:00:00Z | 2024-10-04T14:00:00Z | no | no | no | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-23T09:00:00Z | 42072 | 763 | 2024-11-23T09:00:00Z | +48.200000 | 2024-11-23T08:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-01-19T04:00:00Z | 1 | -1 | 2025-01-19T12:00:00Z | 43443 | 797 | 2025-01-19T12:00:00Z | +47.790000 | 2025-01-19T08:00:00Z | 2025-01-19T10:00:00Z | 2025-01-19T16:00:00Z | no | no | no | no |
| ZECUSDT | 2025-04-13T20:00:00Z | 1 | -1 | 2025-04-15T03:00:00Z | 45498 | 841 | 2025-04-15T03:00:00Z | +30.430000 | 2025-04-15T00:00:00Z | 2025-04-14T16:00:00Z | 2025-04-20T04:00:00Z | no | no | no | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | 1 | 2025-09-06T20:00:00Z | 48971 | 902 | 2025-09-06T20:00:00Z | +43.810000 | 2025-09-06T16:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | 1 | 2025-12-27T10:00:00Z | 51649 | 944 | 2025-12-27T10:00:00Z | +486.020000 | 2025-12-27T08:00:00Z | 2025-12-27T02:00:00Z | 2025-12-31T13:00:00Z | no | no | no | no |
| ZECUSDT | 2026-03-26T08:00:00Z | 1 | -1 | 2026-03-27T18:00:00Z | 53817 | 989 | 2026-03-27T18:00:00Z | +215.340000 | 2026-03-27T16:00:00Z | 2026-03-27T12:00:00Z | 2026-03-30T05:00:00Z | no | no | no | no |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | 1 | 2026-05-09T03:00:00Z | 54834 | 1009 | 2026-05-09T03:00:00Z | +618.490000 | 2026-05-09T00:00:00Z | 2026-05-01T16:00:00Z | 2026-05-10T21:00:00Z | no | no | no | no |

### P-ADD-BRK · tierE__refuse_post_harvest (56 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | 1 | 2020-08-17T16:00:00Z | 8254 | 167 | 2020-08-17T16:00:00Z | +12443.990000 | 2020-08-17T12:00:00Z | 2020-08-17T14:00:00Z | 2020-08-19T05:00:00Z | no | no | no | yes |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | 1 | 2020-12-03T16:00:00Z | 10846 | 224 | 2020-12-03T16:00:00Z | +19560.910000 | 2020-12-03T12:00:00Z | 2020-11-30T01:00:00Z | 2020-12-04T23:00:00Z | no | no | no | yes |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | 1 | 2021-11-08T01:00:00Z | 18991 | 405 | 2021-11-08T01:00:00Z | +65097.190000 | 2021-11-08T00:00:00Z | 2021-11-08T00:00:00Z | 2021-11-10T21:00:00Z | no | no | no | yes |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T05:00:00Z | 45347 | 946 | 2024-11-10T05:00:00Z | +79273.700000 | 2024-11-10T04:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-13T15:00:00Z | 45429 | 950 | 2024-11-13T15:00:00Z | +91563.000000 | 2024-11-13T12:00:00Z | 2024-11-10T05:00:00Z | 2024-11-17T23:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 1 | -1 | 2025-02-25T00:00:00Z | 47910 | 989 | 2025-02-25T00:00:00Z | +91514.500000 | 2025-02-24T20:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| BTCUSDT | 2025-02-22T16:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 47953 | 991 | 2025-02-26T19:00:00Z | +84204.900000 | 2025-02-26T16:00:00Z | 2025-02-23T15:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | 1 | 2020-06-02T07:00:00Z | 4511 | 88 | 2020-06-02T07:00:00Z | +248.150000 | 2020-06-02T04:00:00Z | 2020-05-28T23:00:00Z | 2020-06-02T15:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-05T22:00:00Z | 8270 | 155 | 2020-11-05T22:00:00Z | +413.950000 | 2020-11-05T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-11-04T20:00:00Z | 2 | 1 | 2020-11-11T08:00:00Z | 8400 | 158 | 2020-11-11T08:00:00Z | +462.520000 | 2020-11-11T04:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | 1 | 2020-12-17T11:00:00Z | 9267 | 166 | 2020-12-17T11:00:00Z | +670.420000 | 2020-12-17T08:00:00Z | 2020-12-16T13:00:00Z | 2020-12-20T22:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-10T05:00:00Z | 11997 | 216 | 2021-04-10T05:00:00Z | +2199.110000 | 2021-04-10T04:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 2 | 1 | 2021-04-13T12:00:00Z | 12076 | 218 | 2021-04-13T12:00:00Z | +2235.430000 | 2021-04-13T08:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2024-10-08T08:00:00Z | 1 | -1 | 2024-10-09T21:00:00Z | 42685 | 822 | 2024-10-09T21:00:00Z | +2355.010000 | 2024-10-09T20:00:00Z | 2024-10-08T16:00:00Z | 2024-10-11T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-01-26T20:00:00Z | 1 | -1 | 2025-01-27T07:00:00Z | 45311 | 868 | 2025-01-27T07:00:00Z | +3082.750000 | 2025-01-27T04:00:00Z | 2025-01-27T03:00:00Z | 2025-01-30T04:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T06:00:00Z | 46006 | 875 | 2025-02-25T06:00:00Z | +2505.040000 | 2025-02-25T04:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-26T19:00:00Z | 46043 | 877 | 2025-02-26T19:00:00Z | +2291.640000 | 2025-02-26T16:00:00Z | 2025-02-24T23:00:00Z | 2025-03-02T16:00:00Z | no | no | no | no |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-24T19:00:00Z | 50339 | 953 | 2025-08-24T19:00:00Z | +4932.840000 | 2025-08-24T16:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| ETHUSDT | 2025-10-29T16:00:00Z | 1 | -1 | 2025-10-30T14:00:00Z | 51942 | 989 | 2025-10-30T14:00:00Z | +3764.660000 | 2025-10-30T12:00:00Z | 2025-10-30T13:00:00Z | 2025-11-07T19:00:00Z | no | no | no | no |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | 1 | 2026-09-21T01:00:00Z | 59753 | 1165 | 2026-09-21T01:00:00Z | +2688.100000 | 2026-09-21T00:00:00Z | 2026-09-18T14:00:00Z | 2026-09-23T15:00:00Z | no | no | no | no |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | 1 | 2020-12-31T10:00:00Z | 1849 | 57 | 2020-12-31T10:00:00Z | +1.296300 | 2020-12-31T08:00:00Z | 2020-12-31T10:00:00Z | 2021-01-04T08:00:00Z | no | no | no | yes |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | 1 | 2021-04-06T15:00:00Z | 4158 | 109 | 2021-04-06T15:00:00Z | +7.198900 | 2021-04-06T12:00:00Z | 2021-04-06T05:00:00Z | 2021-04-07T12:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | 1 | 2022-01-13T15:00:00Z | 10926 | 239 | 2022-01-13T15:00:00Z | +19.338600 | 2022-01-13T12:00:00Z | 2022-01-13T14:00:00Z | 2022-01-17T17:00:00Z | no | no | no | yes |
| NEARUSDT | 2022-02-17T16:00:00Z | 1 | -1 | 2022-02-24T04:00:00Z | 11923 | 265 | 2022-02-24T04:00:00Z | +7.784000 | 2022-02-24T00:00:00Z | 2022-02-19T12:00:00Z | 2022-02-26T01:00:00Z | no | no | no | yes |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-25T14:00:00Z | 38261 | 862 | 2025-02-25T14:00:00Z | +2.903000 | 2025-02-25T12:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | 1 | 2025-05-22T15:00:00Z | 40326 | 906 | 2025-05-22T15:00:00Z | +3.031000 | 2025-05-22T12:00:00Z | 2025-05-22T08:00:00Z | 2025-05-25T00:00:00Z | no | no | no | no |
| NEARUSDT | 2025-06-12T20:00:00Z | 1 | -1 | 2025-06-13T01:00:00Z | 40840 | 918 | 2025-06-13T01:00:00Z | +2.238000 | 2025-06-13T00:00:00Z | 2025-06-13T01:00:00Z | 2025-06-16T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | 1 | 2025-08-13T10:00:00Z | 42313 | 951 | 2025-08-13T10:00:00Z | +2.917000 | 2025-08-13T08:00:00Z | 2025-08-13T10:00:00Z | 2025-08-15T16:00:00Z | no | no | no | no |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | 1 | 2026-05-21T20:00:00Z | 49067 | 1106 | 2026-05-21T20:00:00Z | +1.923000 | 2026-05-21T16:00:00Z | 2026-05-21T02:00:00Z | 2026-05-26T19:00:00Z | no | no | no | no |
| NEARUSDT | 2026-07-22T00:00:00Z | 1 | -1 | 2026-07-22T13:00:00Z | 50548 | 1138 | 2026-07-22T13:00:00Z | +1.883000 | 2026-07-22T12:00:00Z | 2026-07-22T08:00:00Z | 2026-07-27T00:00:00Z | no | no | no | no |
| SOLUSDT | 2020-12-04T16:00:00Z | 1 | -1 | 2020-12-04T23:00:00Z | 1959 | 54 | 2020-12-04T23:00:00Z | +1.846800 | 2020-12-04T20:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2020-12-04T16:00:00Z | 2 | -1 | 2020-12-08T09:00:00Z | 2041 | 56 | 2020-12-08T09:00:00Z | +1.735400 | 2020-12-08T08:00:00Z | 2020-12-04T23:00:00Z | 2020-12-13T13:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | 1 | 2021-03-30T03:00:00Z | 4723 | 122 | 2021-03-30T03:00:00Z | +19.856100 | 2021-03-30T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-03-27T04:00:00Z | 2 | 1 | 2021-04-03T04:00:00Z | 4820 | 125 | 2021-04-03T04:00:00Z | +21.106400 | 2021-04-03T00:00:00Z | 2021-03-28T13:00:00Z | 2021-04-06T15:00:00Z | no | no | no | yes |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | 1 | 2021-10-21T01:00:00Z | 9641 | 198 | 2021-10-21T01:00:00Z | +185.717000 | 2021-10-21T00:00:00Z | 2021-10-20T16:00:00Z | 2021-10-24T12:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-01-17T08:00:00Z | 1 | -1 | 2022-01-21T00:00:00Z | 11848 | 241 | 2022-01-21T00:00:00Z | +127.450000 | 2022-01-20T20:00:00Z | 2022-01-18T15:00:00Z | 2022-01-25T19:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-02-17T12:00:00Z | 1 | -1 | 2022-02-17T19:00:00Z | 12515 | 264 | 2022-02-17T19:00:00Z | +95.120000 | 2022-02-17T16:00:00Z | 2022-02-17T19:00:00Z | 2022-02-21T02:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 1 | -1 | 2022-12-17T02:00:00Z | 19770 | 445 | 2022-12-17T02:00:00Z | +12.100000 | 2022-12-17T00:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2022-12-16T16:00:00Z | 2 | -1 | 2022-12-24T06:00:00Z | 19942 | 447 | 2022-12-24T06:00:00Z | +11.354000 | 2022-12-24T04:00:00Z | 2022-12-16T23:00:00Z | 2023-01-02T08:00:00Z | no | no | no | yes |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | 1 | 2024-11-10T12:00:00Z | 36436 | 763 | 2024-11-10T12:00:00Z | +206.780000 | 2024-11-10T08:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2024-11-06T00:00:00Z | 2 | 1 | 2024-11-11T15:00:00Z | 36463 | 765 | 2024-11-11T15:00:00Z | +218.930000 | 2024-11-11T12:00:00Z | 2024-11-08T01:00:00Z | 2024-11-13T05:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 1 | -1 | 2025-11-16T17:00:00Z | 45345 | 977 | 2025-11-16T17:00:00Z | +135.640000 | 2025-11-16T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 2 | -1 | 2025-11-17T19:00:00Z | 45371 | 978 | 2025-11-17T19:00:00Z | +130.440000 | 2025-11-17T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | 1 | 2020-06-23T17:00:00Z | 3344 | 58 | 2020-06-23T17:00:00Z | +58.500000 | 2020-06-23T16:00:00Z | 2020-06-23T13:00:00Z | 2020-06-27T16:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | 1 | 2020-07-29T16:00:00Z | 4207 | 79 | 2020-07-29T16:00:00Z | +72.900000 | 2020-07-29T12:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2020-07-21T08:00:00Z | 2 | 1 | 2020-08-01T00:00:00Z | 4263 | 80 | 2020-08-01T00:00:00Z | +75.000000 | 2020-07-31T20:00:00Z | 2020-07-27T01:00:00Z | 2020-08-04T12:00:00Z | no | no | no | yes |
| ZECUSDT | 2022-09-13T12:00:00Z | 1 | -1 | 2022-09-18T22:00:00Z | 22957 | 421 | 2022-09-18T22:00:00Z | +53.190000 | 2022-09-18T20:00:00Z | 2022-09-18T22:00:00Z | 2022-09-21T19:00:00Z | no | no | no | yes |
| ZECUSDT | 2022-10-07T00:00:00Z | 1 | -1 | 2022-10-11T01:00:00Z | 23488 | 436 | 2022-10-11T01:00:00Z | +52.080000 | 2022-10-11T00:00:00Z | 2022-10-07T13:00:00Z | 2022-10-16T06:00:00Z | no | no | no | yes |
| ZECUSDT | 2023-08-15T08:00:00Z | 1 | -1 | 2023-08-15T20:00:00Z | 30899 | 596 | 2023-08-15T20:00:00Z | +27.540000 | 2023-08-15T16:00:00Z | 2023-08-15T20:00:00Z | 2023-08-20T21:00:00Z | no | no | no | yes |
| ZECUSDT | 2024-09-29T00:00:00Z | 1 | -1 | 2024-10-01T23:00:00Z | 40814 | 737 | 2024-10-01T23:00:00Z | +26.440000 | 2024-10-01T20:00:00Z | 2024-09-30T01:00:00Z | 2024-10-04T14:00:00Z | no | no | no | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-23T09:00:00Z | 42072 | 763 | 2024-11-23T09:00:00Z | +48.200000 | 2024-11-23T08:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-01-19T04:00:00Z | 1 | -1 | 2025-01-19T12:00:00Z | 43443 | 797 | 2025-01-19T12:00:00Z | +47.790000 | 2025-01-19T08:00:00Z | 2025-01-19T10:00:00Z | 2025-01-19T16:00:00Z | no | no | no | no |
| ZECUSDT | 2025-04-13T20:00:00Z | 1 | -1 | 2025-04-15T03:00:00Z | 45498 | 841 | 2025-04-15T03:00:00Z | +30.430000 | 2025-04-15T00:00:00Z | 2025-04-14T16:00:00Z | 2025-04-20T04:00:00Z | no | no | no | no |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | 1 | 2025-12-27T10:00:00Z | 51649 | 944 | 2025-12-27T10:00:00Z | +486.020000 | 2025-12-27T08:00:00Z | 2025-12-27T02:00:00Z | 2025-12-31T13:00:00Z | no | no | no | no |
| ZECUSDT | 2026-03-26T08:00:00Z | 1 | -1 | 2026-03-27T18:00:00Z | 53817 | 989 | 2026-03-27T18:00:00Z | +215.340000 | 2026-03-27T16:00:00Z | 2026-03-27T12:00:00Z | 2026-03-30T05:00:00Z | no | no | no | no |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | 1 | 2026-05-09T03:00:00Z | 54834 | 1009 | 2026-05-09T03:00:00Z | +618.490000 | 2026-05-09T00:00:00Z | 2026-05-01T16:00:00Z | 2026-05-10T21:00:00Z | no | no | no | no |

### P-ADD-SFP · scored (12 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-12T22:00:00Z | 8438 | 160 | 2020-11-12T22:00:00Z | +462.820000 | 2020-11-12T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-17T19:00:00Z | 12179 | 221 | 2021-04-17T19:00:00Z | +2364.050000 | 2021-04-17T16:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-25T02:00:00Z | 50346 | 954 | 2025-08-25T02:00:00Z | +4729.990000 | 2025-08-25T00:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-27T03:00:00Z | 38298 | 864 | 2025-02-27T03:00:00Z | +3.053000 | 2025-02-27T00:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-27T12:00:00Z | 38307 | 864 | 2025-02-27T12:00:00Z | +3.125000 | 2025-02-27T08:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | 1 | 2025-05-24T20:00:00Z | 40379 | 907 | 2025-05-24T20:00:00Z | +2.793000 | 2025-05-24T16:00:00Z | 2025-05-22T08:00:00Z | 2025-05-25T00:00:00Z | no | yes | yes | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 1 | -1 | 2025-12-18T18:00:00Z | 45369 | 1034 | 2025-12-18T18:00:00Z | +1.524000 | 2025-12-18T16:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 2 | -1 | 2025-12-22T06:00:00Z | 45453 | 1039 | 2025-12-22T06:00:00Z | +1.523000 | 2025-12-22T04:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-25T21:00:00Z | 42132 | 766 | 2024-11-25T21:00:00Z | +49.210000 | 2024-11-25T20:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | 1 | 2025-09-10T01:00:00Z | 49048 | 905 | 2025-09-10T01:00:00Z | +48.440000 | 2025-09-10T00:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 2 | 1 | 2025-09-10T22:00:00Z | 49069 | 905 | 2025-09-10T22:00:00Z | +47.870000 | 2025-09-10T20:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | 1 | 2026-04-27T17:00:00Z | 54560 | 1001 | 2026-04-27T17:00:00Z | +353.200000 | 2026-04-27T16:00:00Z | 2026-04-24T12:00:00Z | 2026-04-28T04:00:00Z | no | no | no | no |

### P-ADD-SFP · tierE__frozen3 (3 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-03-01T06:00:00Z | 38349 | 388 | 2025-03-01T06:00:00Z | +3.121000 | 2025-03-01T04:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 1 | -1 | 2025-11-18T18:00:00Z | 45394 | 492 | 2025-11-18T18:00:00Z | +139.960000 | 2025-11-18T16:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |
| SOLUSDT | 2025-11-11T20:00:00Z | 2 | -1 | 2025-11-19T04:00:00Z | 45404 | 492 | 2025-11-19T04:00:00Z | +139.700000 | 2025-11-19T00:00:00Z | 2025-11-13T20:00:00Z | 2025-11-20T06:00:00Z | no | no | no | no |

### P-ADD-SFP · tierE__refuse_below_entry (11 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-12T22:00:00Z | 8438 | 160 | 2020-11-12T22:00:00Z | +462.820000 | 2020-11-12T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-17T19:00:00Z | 12179 | 221 | 2021-04-17T19:00:00Z | +2364.050000 | 2021-04-17T16:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-25T02:00:00Z | 50346 | 954 | 2025-08-25T02:00:00Z | +4729.990000 | 2025-08-25T00:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-27T03:00:00Z | 38298 | 864 | 2025-02-27T03:00:00Z | +3.053000 | 2025-02-27T00:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-27T12:00:00Z | 38307 | 864 | 2025-02-27T12:00:00Z | +3.125000 | 2025-02-27T08:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 1 | -1 | 2025-12-18T18:00:00Z | 45369 | 1034 | 2025-12-18T18:00:00Z | +1.524000 | 2025-12-18T16:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| NEARUSDT | 2025-12-05T08:00:00Z | 2 | -1 | 2025-12-22T06:00:00Z | 45453 | 1039 | 2025-12-22T06:00:00Z | +1.523000 | 2025-12-22T04:00:00Z | 2025-12-14T22:00:00Z | 2025-12-22T09:00:00Z | no | no | yes | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-25T21:00:00Z | 42132 | 766 | 2024-11-25T21:00:00Z | +49.210000 | 2024-11-25T20:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | 1 | 2025-09-10T01:00:00Z | 49048 | 905 | 2025-09-10T01:00:00Z | +48.440000 | 2025-09-10T00:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2025-09-02T16:00:00Z | 2 | 1 | 2025-09-10T22:00:00Z | 49069 | 905 | 2025-09-10T22:00:00Z | +47.870000 | 2025-09-10T20:00:00Z | 2025-09-06T20:00:00Z | 2025-09-11T13:00:00Z | no | no | yes | no |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | 1 | 2026-04-27T17:00:00Z | 54560 | 1001 | 2026-04-27T17:00:00Z | +353.200000 | 2026-04-27T16:00:00Z | 2026-04-24T12:00:00Z | 2026-04-28T04:00:00Z | no | no | no | no |

### P-ADD-SFP · tierE__refuse_post_harvest (7 adds)

| symbol | entry_ms | seq | direction | event_ms | event_i | event_rid | add_ms | add_px | add_4h_open_ms | latch_1h_ms | exit_close_1h_ms | moved_to_parent_close | below_entry | post_harvest | scale_in_sample |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | 1 | 2020-11-12T22:00:00Z | 8438 | 160 | 2020-11-12T22:00:00Z | +462.820000 | 2020-11-12T20:00:00Z | 2020-11-05T14:00:00Z | 2020-11-15T18:00:00Z | no | no | no | yes |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | 1 | 2021-04-17T19:00:00Z | 12179 | 221 | 2021-04-17T19:00:00Z | +2364.050000 | 2021-04-17T16:00:00Z | 2021-04-10T05:00:00Z | 2021-04-18T01:00:00Z | no | no | no | yes |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | 1 | 2025-08-25T02:00:00Z | 50346 | 954 | 2025-08-25T02:00:00Z | +4729.990000 | 2025-08-25T00:00:00Z | 2025-08-24T18:00:00Z | 2025-08-25T07:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 1 | -1 | 2025-02-27T03:00:00Z | 38298 | 864 | 2025-02-27T03:00:00Z | +3.053000 | 2025-02-27T00:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| NEARUSDT | 2025-02-24T12:00:00Z | 2 | -1 | 2025-02-27T12:00:00Z | 38307 | 864 | 2025-02-27T12:00:00Z | +3.125000 | 2025-02-27T08:00:00Z | 2025-02-24T23:00:00Z | 2025-03-01T18:00:00Z | no | no | no | no |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | 1 | 2024-11-25T21:00:00Z | 42132 | 766 | 2024-11-25T21:00:00Z | +49.210000 | 2024-11-25T20:00:00Z | 2024-11-22T05:00:00Z | 2024-11-25T23:00:00Z | no | no | no | no |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | 1 | 2026-04-27T17:00:00Z | 54560 | 1001 | 2026-04-27T17:00:00Z | +353.200000 | 2026-04-27T16:00:00Z | 2026-04-24T12:00:00Z | 2026-04-28T04:00:00Z | no | no | no | no |

(The era slices' adds are the scored adds of campaigns of that era; ADDS.parquet carries them under arm tierE__tuning / tierE__holdout.)

## 7 · 1h pick stability (CLASSIC5) [L-R.2]

| asset | pick_of_record | pick_window | first_half_pick | whole_tape_pick | frozen_scale | stability_changed | in_sample_tuning | in_sample_holdout | tier |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | +1.750000 | tuning | +2.000000 | +2.000000 | +3.000000 | yes | yes | no | TIER-E |
| ETHUSDT | +2.000000 | tuning | +2.000000 | +2.000000 | +3.000000 | no | yes | no | TIER-E |
| NEARUSDT | +1.750000 | tuning | +2.000000 | +2.000000 | +3.000000 | yes | yes | no | TIER-E |
| SOLUSDT | +1.750000 | tuning | +2.000000 | +2.000000 | +3.000000 | yes | yes | no | TIER-E |
| ZECUSDT | +2.000000 | tuning | +2.000000 | +2.000000 | +3.000000 | no | yes | no | TIER-E |

Every add row carries stability_changed of its asset (ADDS.parquet).

## 8 · The 1h event tape (counts; EVENTS_1H.parquet holds every event)

| asset | scale_kind | event_kind | n | n_long | n_short | n_scale_in_sample | tier |
|---|---|---|---|---|---|---|---|
| BTCUSDT | calibrated | death | 522 | 284 | 238 | 347 | TIER-E |
| BTCUSDT | calibrated | harden | 541 | 252 | 289 | 343 | TIER-E |
| BTCUSDT | frozen3.0 | death | 223 | 128 | 95 | 0 | TIER-E |
| BTCUSDT | frozen3.0 | harden | 232 | 125 | 107 | 0 | TIER-E |
| ETHUSDT | calibrated | death | 441 | 244 | 197 | 300 | TIER-E |
| ETHUSDT | calibrated | harden | 430 | 211 | 219 | 287 | TIER-E |
| ETHUSDT | frozen3.0 | death | 231 | 133 | 98 | 0 | TIER-E |
| ETHUSDT | frozen3.0 | harden | 222 | 111 | 111 | 0 | TIER-E |
| SOLUSDT | calibrated | death | 441 | 221 | 220 | 260 | TIER-E |
| SOLUSDT | calibrated | harden | 492 | 257 | 235 | 316 | TIER-E |
| SOLUSDT | frozen3.0 | death | 203 | 105 | 98 | 0 | TIER-E |
| SOLUSDT | frozen3.0 | harden | 242 | 123 | 119 | 0 | TIER-E |
| NEARUSDT | calibrated | death | 437 | 229 | 208 | 264 | TIER-E |
| NEARUSDT | calibrated | harden | 549 | 265 | 284 | 329 | TIER-E |
| NEARUSDT | frozen3.0 | death | 211 | 108 | 103 | 0 | TIER-E |
| NEARUSDT | frozen3.0 | harden | 246 | 115 | 131 | 0 | TIER-E |
| ZECUSDT | calibrated | death | 410 | 211 | 199 | 263 | TIER-E |
| ZECUSDT | calibrated | harden | 559 | 272 | 287 | 351 | TIER-E |
| ZECUSDT | frozen3.0 | death | 219 | 118 | 101 | 0 | TIER-E |
| ZECUSDT | frozen3.0 | harden | 284 | 122 | 162 | 0 | TIER-E |

## 9 · Mismatch bars [L-W.0, AM-5]

| registration | arm | n_mismatch_bars_ridden | n_campaigns_on_mismatch | mismatch_bars | n_events_moved | n_adds_moved | tier |
|---|---|---|---|---|---|---|---|
| P-ADD-BRK | base | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-BRK | scored | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-BRK | tierE__frozen3 | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_below_entry | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-BRK | tierE__refuse_post_harvest | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-SFP | base | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-SFP | scored | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-SFP | tierE__frozen3 | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_below_entry | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |
| P-ADD-SFP | tierE__refuse_post_harvest | 1 | 1 | 2024-10-28T20:00:00Z | 0 | 0 | TIER-E |

The corridor's mismatch bars (a 4h bar whose four 1h children do not reproduce its H/L/C; 1h-only events on them are taken at the parent's close):

| asset | bar_open | reason | tier |
|---|---|---|---|
| BTCUSDT | 2019-09-08T16:00:00Z | 3 native 1h children, expected 4 | TIER-E |
| BTCUSDT | 2019-09-09T00:00:00Z | 4h high 10316.68 not reproduced (1h max 10391.63) | TIER-E |
| BTCUSDT | 2019-09-24T16:00:00Z | 4h high 8689.49 not reproduced (1h max 9598) | TIER-E |
| BTCUSDT | 2023-11-10T12:00:00Z | 4h close 37118.4 not reproduced (last 1h close 37092.6) | TIER-E |
| BTCUSDT | 2024-10-28T20:00:00Z | 4h low 69480.3 not reproduced (1h min 69389) | TIER-E |
| ETHUSDT | 2019-11-27T04:00:00Z | 1 native 1h children, expected 4 | TIER-E |
| ETHUSDT | 2019-12-11T16:00:00Z | 4h high 142.87 not reproduced (1h max 143.33) | TIER-E |
| ETHUSDT | 2023-11-10T12:00:00Z | 4h close 2085.32 not reproduced (last 1h close 2091.11) | TIER-E |
| ETHUSDT | 2024-10-28T20:00:00Z | 4h low 2516.54 not reproduced (1h min 2504.13) | TIER-E |
| NEARUSDT | 2023-11-10T12:00:00Z | 4h close 1.43 not reproduced (last 1h close 1.436) | TIER-E |
| NEARUSDT | 2024-10-28T20:00:00Z | 4h low 4.238 not reproduced (1h min 4.217) | TIER-E |
| SOLUSDT | 2020-09-14T04:00:00Z | 1 native 1h children, expected 4 | TIER-E |
| SOLUSDT | 2023-11-10T12:00:00Z | 4h close 51.151 not reproduced (last 1h close 50.914) | TIER-E |
| SOLUSDT | 2024-10-28T20:00:00Z | 4h low 176.22 not reproduced (1h min 175.63) | TIER-E |
| ZECUSDT | 2023-11-10T12:00:00Z | 4h close 29.32 not reproduced (last 1h close 29.6) | TIER-E |
| ZECUSDT | 2024-10-28T20:00:00Z | 4h low 38.04 not reproduced (1h min 37.95) | TIER-E |

## 10 · Findings (derived in-build; findings-not-fixed for the build doc)

- F1 [AM-5, L-W.0] mismatch bars ridden by the v6 set: 1 bar(s) in 1 campaign(s) — ZECUSDT entered 2024-10-28T08:00:00Z rides 2024-10-28T20:00:00Z; add events moved to a parent close: 0, adds moved: 0 (every arm). Decided by the parent per L-W.0; the walk-or-defer choice reads later prices of the same 4h bar (AM-5 disclosure).
- F2 [AM-3] P-ADD-BRK scored: 1 acted campaign(s) where the D12 ceiling absorbs tranche funding (Δ != add_r): ETHUSDT 2021-04-08T20:00:00Z Δ -0.023188 = add_r -0.103823 + absorbed 0.080635 − v6 absorbed 0.000000; the paired Δ is scored on net_r (AM-3), never on add_r.
- F2 [AM-3] P-ADD-SFP scored: 0 acted campaign(s) where the D12 ceiling absorbs tranche funding (Δ != add_r): none; the paired Δ is scored on net_r (AM-3), never on add_r.
- F3 P-ADD-BRK: the Tier-E arm(s) ['tierE__refuse_below_entry'] are byte-identical to the scored book (the twin's class holds no admitted add on the data).
- F4 P-ADD-SFP: the 2-add cap never binds on the scored arm (0 events refused at the cap), so a 3rd-add sabotage on it must be a planted row.
- F5 [L-R.2] 1h pick stability: the first-half-of-tuning pick differs from the tuning pick for ['BTCUSDT', 'NEARUSDT', 'SOLUSDT']; every add row of those assets carries stability_changed = True. Scale-in-sample adds on the scored arms: P-ADD-BRK 32/66, P-ADD-SFP 2/12 (all in the tuning era).
- F6 [SA-4] exit_close_ms of every arm is the v6 book of record's (the exit bar's 4h close), so the base arm is the ONE base book the scorer's F-BASE-IDENT demands; the 1h-resolved exit instant is exit_close_1h_ms.
- F7 [L-A.1, SA-8] P-ADD-BRK: the post-harvest twin's 'inside its 4h bar' clause reads the harvest before its bar's close for an add at an earlier 1h close of that bar — 0 such add(s) on the scored arm, 0 event(s) refused by that clause on tierE__refuse_post_harvest (look-ahead at reading level, inside a Tier-E twin).
- F7 [L-A.1, SA-8] P-ADD-SFP: the post-harvest twin's 'inside its 4h bar' clause reads the harvest before its bar's close for an add at an earlier 1h close of that bar — 0 such add(s) on the scored arm, 0 event(s) refused by that clause on tierE__refuse_post_harvest (look-ahead at reading level, inside a Tier-E twin).
- F8 [SA-11] P-ADD-BRK head-to-head arm tierE__head_to_head_vs_p_add_sfp: paired vs P-ADD-SFP/scored on 200 identical keys, ΣΔ -0.041104 (mean -0.000206) — a SELECTION, not a result; neither promoted by the other's failure.
- F8 [SA-11] P-ADD-SFP head-to-head arm tierE__head_to_head_vs_p_add_brk: paired vs P-ADD-BRK/scored on 200 identical keys, ΣΔ +0.041104 (mean +0.000206) — a SELECTION, not a result; neither promoted by the other's failure.

## 11 · Files

| file | rows | key | content sha256 | book sha256 |
|---|---|---|---|---|
| regbooks/P-ADD-BRK/base.parquet | 200 | symbol, entry_ms | ee8f06605b9bc0ad… | f41bfaf02b86dfb0… |
| regbooks/P-ADD-BRK/scored.parquet | 200 | symbol, entry_ms | 0f642194049fa400… | 15ba415b7a30f20f… |
| regbooks/P-ADD-BRK/tierE__frozen3.parquet | 200 | symbol, entry_ms | a4d68ded0e6d0936… | b854c1c6ef8903d6… |
| regbooks/P-ADD-BRK/tierE__head_to_head_vs_p_add_sfp.parquet | 200 | symbol, entry_ms | 9da47ef7a82bb293… | 15ba415b7a30f20f… |
| regbooks/P-ADD-BRK/tierE__holdout.parquet | 77 | symbol, entry_ms | 060e2dad360a2c26… | a4854282ba7253e0… |
| regbooks/P-ADD-BRK/tierE__refuse_below_entry.parquet | 200 | symbol, entry_ms | 0f642194049fa400… | 15ba415b7a30f20f… |
| regbooks/P-ADD-BRK/tierE__refuse_post_harvest.parquet | 200 | symbol, entry_ms | f153928dde6fc8a7… | dbd4dbac8f4f28dc… |
| regbooks/P-ADD-BRK/tierE__tuning.parquet | 123 | symbol, entry_ms | f9d3ec50b8a64033… | a8dc8371e22a4f28… |
| regbooks/P-ADD-SFP/base.parquet | 200 | symbol, entry_ms | ee8f06605b9bc0ad… | f41bfaf02b86dfb0… |
| regbooks/P-ADD-SFP/scored.parquet | 200 | symbol, entry_ms | 98332199920f1fb8… | ee2d19250f3e3d74… |
| regbooks/P-ADD-SFP/tierE__frozen3.parquet | 200 | symbol, entry_ms | d5478ecdef997eab… | 227a062b2ed99c28… |
| regbooks/P-ADD-SFP/tierE__head_to_head_vs_p_add_brk.parquet | 200 | symbol, entry_ms | 480105bdb11e025a… | ee2d19250f3e3d74… |
| regbooks/P-ADD-SFP/tierE__holdout.parquet | 77 | symbol, entry_ms | ee359ab9562936fe… | fb0f47b8604ac1ee… |
| regbooks/P-ADD-SFP/tierE__refuse_below_entry.parquet | 200 | symbol, entry_ms | d66adbcc20ae8bc3… | eccbbcbd9afbaa55… |
| regbooks/P-ADD-SFP/tierE__refuse_post_harvest.parquet | 200 | symbol, entry_ms | 68f1b0e0ad09aabe… | 80276294f3ce4cbd… |
| regbooks/P-ADD-SFP/tierE__tuning.parquet | 123 | symbol, entry_ms | 86309a990f7a1dde… | 011c58ba0964a713… |
| stage_a/ACTED.parquet | 284 | registration, arm, symbol, entry_ms | d1fdfc2b9f98b0cb… | — |
| stage_a/ADDS.parquet | 350 | registration, arm, symbol, entry_ms, seq | c48cbb97128c26d1… | — |
| stage_a/DISPOSITIONS.parquet | 459 | registration, arm, symbol, entry_ms, event_ms, event_rid | fdc096198a681b0f… | — |
| stage_a/DISPOSITION_COUNTS.parquet | 56 | registration, arm, disposition | 09611bd0e94cdbfe… | — |
| stage_a/EVENTS_1H.parquet | 7135 | asset, scale_kind, event_kind, event_i | e8f7c254c73e92f3… | — |
| stage_a/HEAD_TO_HEAD.parquet | 12 | arm, registration | b3e238b8fed06dd9… | — |
| stage_a/MISMATCH_BARS.parquet | 16 | asset, bar_open_ms | f687c7f080feffb9… | — |
| stage_a/MISMATCH_BOOKS.parquet | 10 | registration, arm | b2a1206d7a8dd6d7… | — |
| stage_a/OVERLAP.parquet | 6 | arm | 05916ed78becc492… | — |
| stage_a/PICK_STABILITY_1H.parquet | 5 | asset | 79b1ef182d09fb80… | — |
| stage_a/REGISTERED_BOOKS.parquet | 4 | registration, arm | b32fa5ac6b54d016… | — |
| stage_a/TIER_E_ARMS.parquet | 12 | registration, arm | 7c9a237960d48ea5… | — |

