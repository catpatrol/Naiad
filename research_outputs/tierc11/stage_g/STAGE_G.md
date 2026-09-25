# TIER-C11 · STAGE G — admission gates (P-AGE-1, P-WIN-1) and the L-G.3 Tier-E structure

as_of_last_closed_4h: 2026-09-25T00:00:00Z · latest closed 4h at fetch time (AS_OF_PIN.json latest_closed_4h_at_pin_run): 2026-09-25T00:00:00Z · substrate tc11_20260925 · corridor 2019-09-08T16:00:00Z → 2026-09-25T00:00:00Z · CLASSIC5 · seed 20260924 · source scripts/tierc11_stage_g.py

**No verdict is printed here.** The scorer (`scripts/tierc11_score.py`) reads `research_outputs/tierc11/regbooks/P-AGE-1/` and `.../P-WIN-1/` and computes every interval and verdict. Book numbers below are labelled *book, not a verdict*. Every non-registered table carries the collar (tier = 'TIER-E', selection_not_a_result = 'a SELECTION, not a result', gates = 'nothing').

## Readings built

- [LEAN-HEPHAESTUS] L-G.1 tide age of record = tierc7_lab_regime.tide_streak (run length of sign(e89 - e316) on 4h, counted from warm bar 316) read at the campaign's ENTRY bar; trailing CLASSIC5 quartile edges over bars with open <= the entry bar (tierc9._trailing_edges, >= 30 bars; pool = tierc9._trailing_pool over the TC11 corridor); OLD = B4 = streak >= trailing q75; P-AGE-1 refuses OLD.
- [LEAN-HEPHAESTUS] L-G.1 shadow: refuse streak > 206 exactly as written (206 = the whole-corridor median edge, not the OLD edge; it reads the corridor ahead).  Disclosure: tierc9.tide_streak_age (arm bar, three-state tide), banded on the SAME trailing edges as the campaign's entry-bar band.
- [LEAN-HEPHAESTUS] L-G.2 lag = entry_i - arm_i (4h bars); P-WIN-1 refuses lag >= 16; the shadow refuses 7..15.
- [LEAN-HEPHAESTUS] L-G.3 r_over_atr = r_dist / ATR14_4h(entry); admission refuses > 2.2; the PRIORITY book is replay9's loop with the first-trigger pass and the in-window substitute (first later same-direction 12/26 cross with the asset flat and r_over_atr <= 2.2), ridden by tierc11_ride.ride11 from its 4h close; the cross-asset same-close collision count is a disclosure; the three gates crossed 2 x 2 x 2 (partition + gate books), whole.
- [LEAN-HEPHAESTUS] L-1.5 gates are POST-FILTERS: gated = v6 minus exactly the refused set, row-identical; the re-ride rival count is taken from the v6 ride's rejection log (first order), the re-ride book with a refusal hook printed beside (Tier-E).
- [LEAN-HEPHAESTUS] L-1.3 era = the entry bar's CLOSE (E.era_of); L-1.4 no verdict word here, every non-registered table collared; AM-7 haircut_net_r = net_r - fee_r x slip_bps_side / 5.0 (charter tier).
- [LEAN-HEPHAESTUS] L-R.5 named-event instants [AM-6; the lanes pass]: every regbook arm carries the extra column harvest_close_ms = the close of the 4h bar whose close slot fired the band harvest (Trade.harvest_ms + 4h, checked against harvest_i), NA when never harvested — a close event, stamped at its close; required columns, numbers, book_sha256 and sidecars unchanged.

## The registrations (texts of record, verified by sha)

**P-AGE-1** (payload sha256 `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879`)

```
 P-AGE-1 [50%] tide-age gate, TRAILING-quantile definition (refuse the OLD band) vs v6; the absolute
    definition (refuse age > 206 bars) printed as shadow.
```

- scored arm (operative spec): v6 book minus the campaigns whose ENTRY-bar tide streak (tierc7_lab_regime.tide_streak) is >= the trailing 75th-percentile edge (B4 OLD; tierc9._trailing_edges over CLASSIC5 4h bars with open <= the entry bar, >= 30 bars) [L-G.1]
- ruler: two-sample vs card-v6 · panel CLASSIC5 · era full corridor
- **pre_seen:** the scored cohort IS TC10 P_AGE_1_TIDE_YOUTH B4 (same function, same trailing edges, same 200 campaigns, anchored by F-CTRL(b)); point known before filing: gated n 141, +0.4567 vs +0.2087, delta ~ +0.2480 R; new information = the interval and campaigns entered after 2026-09-21T16:00Z (listed by count)
- honesty label for the §0 cell [L-1.4]: "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (<hazard>)"

**P-WIN-1** (payload sha256 `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084`)

```
 P-WIN-1 [50%] window-age gate: refuse triggers with arm→trigger lag ≥ 16 bars vs v6; lag 7–15
    printed as shadow cut.
```

- scored arm (operative spec): v6 book minus campaigns with entry_i - arm_i >= 16 (4h bars) [L-G.2]
- ruler: two-sample vs card-v6 · panel CLASSIC5 · era full corridor
- **selection_hazard:** direction informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149, 56-bar decile -0.5796); P-LAG-1 on the same question NOT MET (delta +0.0616 [-0.7819, +0.9566]); the 16 cut has no on-disk provenance; v6 lag 7-15 holds 4/200, so >=16 ~ >=7
- honesty label for the §0 cell [L-1.4]: "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (<hazard>)"

## Registered books (book, not a verdict)

| registration | arm | gate | n | sum_net_r | mean_net_r | win_pct | sum_haircut_net_r | book_sha_tp | label |
|---|---|---|---|---|---|---|---|---|---|
| P-AGE-1 | scored | P-AGE-1 | 141 | +63.4641 | +0.4501 | 40.4255 | +60.4969 | 4ccddc79a34afdf8511847a06175b202c8e8fb295fde7c3fe7095c6bf399bee3 | book, not a verdict |
| P-AGE-1 | base |  | 200 | +40.8076 | +0.2040 | 34.5000 | +36.6975 | f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132 | book, not a verdict |
| P-WIN-1 | scored | P-WIN-1 | 137 | +51.9740 | +0.3794 | 40.1460 | +49.1525 | aa0216e7cdd55da804f83af6682e9ea25ee7b0e99b95f68e85379e520b600bb1 | book, not a verdict |
| P-WIN-1 | base |  | 200 | +40.8076 | +0.2040 | 34.5000 | +36.6975 | f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132 | book, not a verdict |

## Gate rows [L-1.5] — refused cohort, both books' ΣR, the re-ride rival

The rival count of record is taken from the v6 ride's REJECTION LOG (T9.replay9 Arming.reject == 'position_open' whose blocking v6 campaign is refused), first order. `rival_count_self_refused` = rivals the same gate would refuse at their own trigger bar. The re-ride book (the gate evaluated on every candidate inside the replay, a refused trigger not occupying the slot) is printed beside it as a Tier-E book.

| gate | registration | rule | caveat | n_base | sum_net_r_base | n_gated | sum_net_r_gated | mean_net_r_gated | n_refused | mean_net_r_refused | sum_net_r_refused | forfeit_note | rival_count_rejection_log | rival_count_self_refused | reride_n | reride_sum_net_r | reride_mean_net_r | reride_admitted_not_in_v6 | reride_v6_not_taken | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-AGE-1 | P-AGE-1 | refuse ENTRY-bar tide streak >= trailing q75 (B4 OLD) |  | 200 | +40.8076 | 141 | +63.4641 | +0.4501 | 59 | -0.3840 | -22.6566 |  | 0 | 0 | 141 | +63.4641 | +0.4501 | 0 | 59 | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1/shadow_abs206 | P-AGE-1 | refuse ENTRY-bar tide streak > 206 (ABSOLUTE shadow, as written) | 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4) | 200 | +40.8076 | 80 | +48.8040 | +0.6100 | 120 | -0.0666 | -7.9964 |  | 0 | 0 | 80 | +48.8040 | +0.6100 | 0 | 120 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | P-WIN-1 | refuse lag = entry_i - arm_i >= 16 |  | 200 | +40.8076 | 137 | +51.9740 | +0.3794 | 63 | -0.1772 | -11.1665 |  | 0 | 0 | 137 | +51.9740 | +0.3794 | 0 | 63 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1/shadow_lag7_15 | P-WIN-1 | refuse lag 7..15 (shadow cut) |  | 200 | +40.8076 | 196 | +43.0857 | +0.2198 | 4 | -0.5695 | -2.2781 |  | 0 | 0 | 196 | +43.0857 | +0.2198 | 0 | 4 | TIER-E | a SELECTION, not a result | nothing |
| L-G.3/ratr_admission | P-WIN-1 | refuse r_over_atr = r_dist / ATR14_4h(entry) > 2.2 |  | 200 | +40.8076 | 147 | +19.1155 | +0.1300 | 53 | +0.4093 | +21.6921 | on per-campaign expectancy only; the gate forfeits +21.6921 R total | 0 | 0 | 147 | +19.1155 | +0.1300 | 0 | 53 | TIER-E | a SELECTION, not a result | nothing |

§0 gate disclosure per registration [L-1.5] (from the gate rows above; the scorer does not read them — the build doc takes them from here):

- **P-AGE-1**: refused n 59 · mean -0.384010 · ΣR -22.656566; ΣR base +40.807565 · gated +63.464131; re-ride rival count (rejection log) 0 · re-ride book n 141 ΣR +63.464131 · campaigns not in v6 0; forfeit note: (none — mean(refused) <= 0) (book, not a verdict)
- **P-WIN-1**: refused n 63 · mean -0.177245 · ΣR -11.166454; ΣR base +40.807565 · gated +51.974019; re-ride rival count (rejection log) 0 · re-ride book n 137 ΣR +51.974019 · campaigns not in v6 0; forfeit note: (none — mean(refused) <= 0) (book, not a verdict)

## Tier-E regbook arms

| registration | arm | ruler | era_scope | n | sum_net_r | mean_net_r | win_pct | sum_haircut_net_r | book_sha256 | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| P-AGE-1 | tierE__shadow_abs206 | two_sample | full | 80 | +48.8040 | +0.6100 | 46.2500 | +47.0946 | 2c1e47eec765be4a531205ff26dfb495d21efa42788fdea1c9d673b6e385d169 | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__tuning | two_sample | tuning | 81 | +11.4625 | +0.1415 | 38.2716 | +9.8112 | 4acc5b91b27e1a931480218f038ffe5749f04479d4dcd0add1a3b84b79bcf7c5 | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__holdout | two_sample | holdout | 60 | +52.0016 | +0.8667 | 43.3333 | +50.6858 | f7331ba52363642520df489500970333494bdf0f7ab90f4ce3ee342d74d91183 | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | tierE__refused_cohort | vs_zero | full | 59 | -22.6566 | -0.3840 | 20.3390 | -23.7994 | 0569170404a1d10cb80c1021278423e53b5c0a0ad26030940098c1770e2d9838 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__shadow_lag7_15 | two_sample | full | 196 | +43.0857 | +0.2198 | 34.6939 | +39.0521 | f624bffc3baea05741a1a94b61699997a0e4d615ce52649fb02b3277866d7fae | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__tuning | two_sample | tuning | 81 | +8.0226 | +0.0990 | 39.5062 | +6.4519 | 862fc6fd0a237ed4b6f84e250d4737048eedc58910911c05840606fbcb714218 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__holdout | two_sample | holdout | 56 | +43.9515 | +0.7848 | 41.0714 | +42.7006 | 7cdb206beff5ae4d8a45827e54f1450744fe3c6fc1b7cd06d801c0ec4afa07b3 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__refused_cohort | vs_zero | full | 63 | -11.1665 | -0.1772 | 22.2222 | -12.4550 | 7a97b32895c78324c22dacc563efdec38e98ffa8fe196f0e9629d5ed6b3bacf6 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_admission | two_sample | full | 147 | +19.1155 | +0.1300 | 29.9320 | +15.5706 | dcfffefbddad389657173b6458f5c88e9ec26865621742740bbd9f8f033201c8 | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | tierE__ratr_priority | two_sample | full | 165 | +18.3925 | +0.1115 | 30.3030 | +14.5015 | a10416bd49c47a08766078e075a1f4187f75aa36f3a29ef521cfc5698403a7f3 | TIER-E | a SELECTION, not a result | nothing |

- `P-AGE-1/tierE__holdout`: the scored arm's HOLDOUT slice (era by the entry bar's CLOSE, L-1.3); compare with `base` sliced to era == holdout
- `P-AGE-1/tierE__refused_cohort`: the REFUSED cohort of P-AGE-1 (B4 OLD at the entry bar): n / mean / ΣR printed on the gate row [L-1.5]
- `P-AGE-1/tierE__shadow_abs206`: SHADOW absolute: v6 minus ENTRY-bar tide streak > 206 bars, exactly as written; 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4)
- `P-AGE-1/tierE__tuning`: the scored arm's TUNING slice (era by the entry bar's CLOSE, L-1.3); compare with `base` sliced to era == tuning
- `P-WIN-1/tierE__holdout`: the scored arm's HOLDOUT slice (era by the entry bar's CLOSE, L-1.3); compare with `base` sliced to era == holdout
- `P-WIN-1/tierE__ratr_admission`: L-G.3 structure-distance ADMISSION: v6 minus r_over_atr = r_dist / ATR14_4h(entry) > 2.2 (a post-filter)
- `P-WIN-1/tierE__ratr_priority`: L-G.3 within-window PRIORITY book: replay9's loop; a window whose first 12/26 trigger has r_over_atr > 2.2 is passed and its entry is the first later same-direction 12/26 cross before the window closes with the asset flat and r_over_atr <= 2.2; ridden by tierc11_ride.ride11 from its 4h close; 18 substitutions (priority_substitute)
- `P-WIN-1/tierE__refused_cohort`: the REFUSED cohort of P-WIN-1 (lag >= 16): n / mean / ΣR printed on the gate row [L-1.5]
- `P-WIN-1/tierE__shadow_lag7_15`: SHADOW cut: v6 minus lag 7..15 [L-G.2]
- `P-WIN-1/tierE__tuning`: the scored arm's TUNING slice (era by the entry bar's CLOSE, L-1.3); compare with `base` sliced to era == tuning

## Era slices (by the entry bar's CLOSE, L-1.3)

| registration | book | era | n | mean_net_r | sum_net_r | win_pct | nan_reason | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|
| P-AGE-1 | scored | tuning | 81 | +0.1415 | +11.4625 | 38.2716 |  | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | scored | holdout | 60 | +0.8667 | +52.0016 | 43.3333 |  | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | scored | full | 141 | +0.4501 | +63.4641 | 40.4255 |  | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | base | tuning | 123 | -0.0108 | -1.3238 | 33.3333 |  | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | base | holdout | 77 | +0.5472 | +42.1314 | 36.3636 |  | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 | base | full | 200 | +0.2040 | +40.8076 | 34.5000 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | scored | tuning | 81 | +0.0990 | +8.0226 | 39.5062 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | scored | holdout | 56 | +0.7848 | +43.9515 | 41.0714 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | scored | full | 137 | +0.3794 | +51.9740 | 40.1460 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | base | tuning | 123 | -0.0108 | -1.3238 | 33.3333 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | base | holdout | 77 | +0.5472 | +42.1314 | 36.3636 |  | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 | base | full | 200 | +0.2040 | +40.8076 | 34.5000 |  | TIER-E | a SELECTION, not a result | nothing |

## F-DEF: both tide-age definitions, per band

Absolute-shadow label: 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4).

| measure | band | n_left_censored | caveat | n | mean_net_r | sum_net_r | win_pct | nan_reason | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| entry_bar_streak (L-G.1 of record) | B1 | 0 |  | 25 | +0.4708 | +11.7692 | 52.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak (L-G.1 of record) | B2 | 2 |  | 60 | +0.5773 | +34.6369 | 40.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak (L-G.1 of record) | B3 | 0 |  | 56 | +0.3046 | +17.0580 | 35.7143 |  | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak (L-G.1 of record) | B4 | 2 |  | 59 | -0.3840 | -22.6566 | 20.3390 |  | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak (L-G.1 of record) | unbanded | 0 |  | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges) | B1 | 0 |  | 96 | +0.1800 | +17.2761 | 36.4583 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges) | B2 | 0 |  | 48 | +0.5052 | +24.2516 | 35.4167 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges) | B3 | 0 |  | 41 | +0.0639 | +2.6193 | 34.1463 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges) | B4 | 0 |  | 15 | -0.2226 | -3.3394 | 20.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age (tierc9, disclosure; banded on the same trailing edges) | unbanded | 0 |  | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak > 206 (ABSOLUTE shadow) | >206 | 2 | 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4) | 120 | -0.0666 | -7.9964 | 26.6667 |  | TIER-E | a SELECTION, not a result | nothing |
| entry_bar_streak > 206 (ABSOLUTE shadow) | <=206 | 2 | 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4) | 80 | +0.6100 | +48.8040 | 46.2500 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age > 206 (disclosure) | >206 | 0 | 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4) | 57 | +0.0068 | +0.3893 | 29.8246 |  | TIER-E | a SELECTION, not a result | nothing |
| arm_bar_tide_streak_age > 206 (disclosure) | <=206 | 0 | 206 is the whole-corridor MEDIAN edge of the pooled CLASSIC5 streak, not the OLD edge, and it reads the corridor ahead (look-ahead); the OLD cut of record is the trailing q75 (B4) | 143 | +0.2826 | +40.4183 | 36.3636 |  | TIER-E | a SELECTION, not a result | nothing |

### Entry-bar band × arm-bar band (the cross-tab, 25 cells)

| cell | entry_band | arm_band | n | mean_net_r | sum_net_r | win_pct | nan_reason | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|
| entry:B1¦arm:B1 | B1 | B1 | 25 | +0.4708 | +11.7692 | 52.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B1¦arm:B2 | B1 | B2 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B1¦arm:B3 | B1 | B3 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B1¦arm:B4 | B1 | B4 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B1¦arm:unbanded | B1 | unbanded | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B2¦arm:B1 | B2 | B1 | 29 | +0.5069 | +14.7013 | 41.3793 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B2¦arm:B2 | B2 | B2 | 31 | +0.6431 | +19.9356 | 38.7097 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B2¦arm:B3 | B2 | B3 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B2¦arm:B4 | B2 | B4 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B2¦arm:unbanded | B2 | unbanded | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B3¦arm:B1 | B3 | B1 | 18 | +0.2744 | +4.9399 | 33.3333 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B3¦arm:B2 | B3 | B2 | 9 | +1.1072 | +9.9646 | 44.4444 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B3¦arm:B3 | B3 | B3 | 29 | +0.0743 | +2.1535 | 34.4828 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B3¦arm:B4 | B3 | B4 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B3¦arm:unbanded | B3 | unbanded | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:B4¦arm:B1 | B4 | B1 | 24 | -0.5889 | -14.1344 | 16.6667 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B4¦arm:B2 | B4 | B2 | 8 | -0.7061 | -5.6486 | 12.5000 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B4¦arm:B3 | B4 | B3 | 12 | +0.0388 | +0.4659 | 33.3333 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B4¦arm:B4 | B4 | B4 | 15 | -0.2226 | -3.3394 | 20.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| entry:B4¦arm:unbanded | B4 | unbanded | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:unbanded¦arm:B1 | unbanded | B1 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:unbanded¦arm:B2 | unbanded | B2 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:unbanded¦arm:B3 | unbanded | B3 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:unbanded¦arm:B4 | unbanded | B4 | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |
| entry:unbanded¦arm:unbanded | unbanded | unbanded | 0 | — | +0.0000 | — | n = 0: no campaign in the cell | TIER-E | a SELECTION, not a result | nothing |

## Lag bands (L-G.2)

| lag_band | n | mean_net_r | sum_net_r | win_pct | nan_reason | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|
| 0 | 52 | +0.4306 | +22.3888 | 48.0769 |  | TIER-E | a SELECTION, not a result | nothing |
| 1-6 | 81 | +0.3934 | +31.8633 | 35.8025 |  | TIER-E | a SELECTION, not a result | nothing |
| 7-15 | 4 | -0.5695 | -2.2781 | 25.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| >=16 | 63 | -0.1772 | -11.1665 | 22.2222 |  | TIER-E | a SELECTION, not a result | nothing |

## The three gates crossed 2 × 2 × 2 [L-G.3]

(a) the crossing: the v6 book partitioned by the three refusal flags (A = P-AGE-1 OLD, W = lag >= 16, S = r_over_atr > 2.2):

| cell | age_old | lag_ge16 | ratr_gt2p2 | n | mean_net_r | sum_net_r | win_pct | nan_reason | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A0¦W0¦S0 | no | no | no | 81 | +0.5405 | +43.7837 | 39.5062 |  | TIER-E | a SELECTION, not a result | nothing |
| A0¦W0¦S1 | no | no | yes | 29 | +0.4422 | +12.8236 | 51.7241 |  | TIER-E | a SELECTION, not a result | nothing |
| A0¦W1¦S0 | no | yes | no | 23 | -0.0048 | -0.1093 | 26.0870 |  | TIER-E | a SELECTION, not a result | nothing |
| A0¦W1¦S1 | no | yes | yes | 8 | +0.8708 | +6.9662 | 50.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| A1¦W0¦S0 | yes | no | no | 21 | -0.3051 | -6.4062 | 23.8095 |  | TIER-E | a SELECTION, not a result | nothing |
| A1¦W0¦S1 | yes | no | yes | 6 | +0.2955 | +1.7730 | 50.0000 |  | TIER-E | a SELECTION, not a result | nothing |
| A1¦W1¦S0 | yes | yes | no | 22 | -0.8251 | -18.1527 | 4.5455 |  | TIER-E | a SELECTION, not a result | nothing |
| A1¦W1¦S1 | yes | yes | yes | 10 | +0.0129 | +0.1293 | 30.0000 |  | TIER-E | a SELECTION, not a result | nothing |

(b) the eight gate books (v6 minus the union of the refused sets of the gates on):

| cell | age_gate_on | win_gate_on | ratr_gate_on | n | mean_net_r | sum_net_r | win_pct | nan_reason | n_refused | sum_net_r_refused | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| age:off¦win:off¦ratr:off | no | no | no | 200 | +0.2040 | +40.8076 | 34.5000 |  | 0 | +0.0000 | TIER-E | a SELECTION, not a result | nothing |
| age:off¦win:off¦ratr:on | no | no | yes | 147 | +0.1300 | +19.1155 | 29.9320 |  | 53 | +21.6921 | TIER-E | a SELECTION, not a result | nothing |
| age:off¦win:on¦ratr:off | no | yes | no | 137 | +0.3794 | +51.9740 | 40.1460 |  | 63 | -11.1665 | TIER-E | a SELECTION, not a result | nothing |
| age:off¦win:on¦ratr:on | no | yes | yes | 102 | +0.3664 | +37.3774 | 36.2745 |  | 98 | +3.4302 | TIER-E | a SELECTION, not a result | nothing |
| age:on¦win:off¦ratr:off | yes | no | no | 141 | +0.4501 | +63.4641 | 40.4255 |  | 59 | -22.6566 | TIER-E | a SELECTION, not a result | nothing |
| age:on¦win:off¦ratr:on | yes | no | yes | 104 | +0.4199 | +43.6744 | 36.5385 |  | 96 | -2.8668 | TIER-E | a SELECTION, not a result | nothing |
| age:on¦win:on¦ratr:off | yes | yes | no | 110 | +0.5146 | +56.6072 | 42.7273 |  | 90 | -15.7997 | TIER-E | a SELECTION, not a result | nothing |
| age:on¦win:on¦ratr:on | yes | yes | yes | 81 | +0.5405 | +43.7837 | 39.5062 |  | 119 | -2.9761 | TIER-E | a SELECTION, not a result | nothing |

## The within-window PRIORITY book [L-G.3]

- n 165 · ΣR +18.392480 (book, not a verdict) · substitutions **18** · windows 200 · outcomes {'entered': 147, 'passed_no_substitute': 35, 'passed_substituted': 18}
- vs v6: shared keys 147 · v6 campaigns not taken 53 · campaigns not in v6 18
- identity control: replay_g with no hook == the v6 book (TP._book_sha f3c68f544bcda52c… == f3c68f544bcda52c…)
- **the one-position rule, measured:** position_open rejections v6 0, priority 0; substitute crosses skipped for 'asset not flat' 0; campaigns exiting AFTER their window's end bar v6 0, priority 0. v6's BELL (12/89 against) exits a campaign at its window's counter cross at the latest — the next window's arm bar — so a slot can be held into a later window only by a bell bar that is also that window's lag-0 trigger. On this corridor 'asset flat' never binds and the re-ride rival is 0 for every gate (every count this sentence rests on is 0).

### Every window of the priority replay, by outcome (counts)

| outcome | n | tier | selection_not_a_result | gates |
|---|---|---|---|---|
| entered | 147 | TIER-E | a SELECTION, not a result | nothing |
| passed_no_substitute | 35 | TIER-E | a SELECTION, not a result | nothing |
| passed_substituted | 18 | TIER-E | a SELECTION, not a result | nothing |

### The priority window log (every window, whole)

| symbol | direction | arm_ms | first_trigger_ms | first_r_over_atr | window_end_i | outcome | entry_ms | entry_r_over_atr | n_scanned | n_scan_not_flat | n_scan_no_stop | n_scan_over_cut | v6_net_r_at_first_trigger | priority_net_r | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1 | 2020-01-26T20:00:00Z | 2020-01-27T00:00:00Z | 2.6466 | 972 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | +1.8131 | — | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-02-18T16:00:00Z | 2020-02-19T08:00:00Z | 1.1332 | 988 | entered | 2020-02-19T08:00:00Z | 1.1332 | 0 | 0 | 0 | 0 | -1.0710 | -1.0710 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2020-03-28T08:00:00Z | 2020-04-01T16:00:00Z | 2.2121 | 1238 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -1.0189 | — | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-05-28T12:00:00Z | 2020-06-07T20:00:00Z | 1.9366 | 1664 | entered | 2020-06-07T20:00:00Z | 1.9366 | 0 | 0 | 0 | 0 | -0.6723 | -0.6723 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-07-07T00:00:00Z | 2020-07-10T20:00:00Z | 1.0000 | 1859 | entered | 2020-07-10T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.1357 | -1.1357 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-07-21T08:00:00Z | 2020-08-14T04:00:00Z | 2.1369 | 2092 | entered | 2020-08-14T04:00:00Z | 2.1369 | 0 | 0 | 0 | 0 | -0.2358 | -0.2358 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-11-29T00:00:00Z | 2020-11-29T16:00:00Z | 1.0000 | 2747 | entered | 2020-11-29T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +1.2069 | +1.2069 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2020-12-13T04:00:00Z | 2021-01-14T08:00:00Z | 3.5182 | 3003 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | -0.5390 | — | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2021-03-28T12:00:00Z | 2021-04-05T20:00:00Z | 1.7933 | 3463 | entered | 2021-04-05T20:00:00Z | 1.7933 | 0 | 0 | 0 | 0 | -1.0870 | -1.0870 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2021-05-05T12:00:00Z | 2021-05-05T20:00:00Z | 1.0000 | 3672 | entered | 2021-05-05T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.1300 | -1.1300 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-06-18T16:00:00Z | 2021-06-25T08:00:00Z | 1.7600 | 3959 | entered | 2021-06-25T08:00:00Z | 1.7600 | 0 | 0 | 0 | 0 | -0.0628 | -0.0628 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-07-01T04:00:00Z | 2021-07-01T12:00:00Z | 1.9788 | 3987 | entered | 2021-07-01T12:00:00Z | 1.9788 | 0 | 0 | 0 | 0 | -0.7894 | -0.7894 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-07-05T12:00:00Z | 2021-07-05T16:00:00Z | 1.5015 | 4105 | entered | 2021-07-05T16:00:00Z | 1.5015 | 0 | 0 | 0 | 0 | -0.1772 | -0.1772 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2021-10-28T16:00:00Z | 2021-10-29T16:00:00Z | 1.0000 | 4738 | entered | 2021-10-29T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0655 | -1.0655 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2021-11-07T00:00:00Z | 2021-11-07T16:00:00Z | 1.0000 | 4797 | entered | 2021-11-07T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +3.1217 | +3.1217 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2021-12-28T20:00:00Z | 2022-01-17T08:00:00Z | 1.0000 | 5281 | entered | 2022-01-17T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.3716 | -0.3716 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-02-18T04:00:00Z | 2022-02-28T00:00:00Z | 1.3901 | 5425 | entered | 2022-02-28T00:00:00Z | 1.3901 | 0 | 0 | 0 | 0 | -1.0275 | -1.0275 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-09-27T16:00:00Z | 2022-09-28T08:00:00Z | 1.6257 | 6729 | entered | 2022-09-28T08:00:00Z | 1.6257 | 0 | 0 | 0 | 0 | -0.8874 | -0.8874 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-10-08T20:00:00Z | 2022-10-15T04:00:00Z | 1.7623 | 6812 | entered | 2022-10-15T04:00:00Z | 1.7623 | 0 | 0 | 0 | 0 | -0.7515 | -0.7515 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2022-12-17T00:00:00Z | 2022-12-25T12:00:00Z | 1.0000 | 7282 | entered | 2022-12-25T12:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.1690 | -1.1690 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2023-05-04T04:00:00Z | 2023-05-04T04:00:00Z | 1.0000 | 8024 | entered | 2023-05-04T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.8185 | -0.8185 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2023-08-08T16:00:00Z | 2023-08-14T12:00:00Z | 1.3237 | 8621 | entered | 2023-08-14T12:00:00Z | 1.3237 | 0 | 0 | 0 | 0 | -1.1627 | -1.1627 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2023-08-31T20:00:00Z | 2023-09-01T04:00:00Z | 1.0696 | 8798 | entered | 2023-09-01T04:00:00Z | 1.0696 | 0 | 0 | 0 | 0 | +0.0149 | +0.0149 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2023-10-16T08:00:00Z | 2023-11-15T20:00:00Z | 2.6090 | 9370 | passed_substituted | 2023-11-19T04:00:00Z | 1.0000 | 1 | 0 | 0 | 0 | -1.0290 | -0.7210 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2023-12-18T20:00:00Z | 2023-12-19T04:00:00Z | 1.0000 | 9423 | entered | 2023-12-19T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0724 | -1.0724 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2024-01-01T20:00:00Z | 2024-01-04T12:00:00Z | 1.0554 | 9525 | entered | 2024-01-04T12:00:00Z | 1.0554 | 0 | 0 | 0 | 0 | -1.0557 | -1.0557 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2024-10-12T12:00:00Z | 2024-10-24T20:00:00Z | 1.0000 | 11304 | entered | 2024-10-24T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0955 | -1.0955 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2024-11-05T12:00:00Z | 2024-11-06T00:00:00Z | 2.5707 | 11576 | passed_substituted | 2024-12-04T16:00:00Z | 1.6228 | 2 | 0 | 0 | 1 | +3.8512 | -1.1097 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2025-01-15T04:00:00Z | 2025-01-23T12:00:00Z | 2.7789 | 11808 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8405 | — | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-02-21T20:00:00Z | 2025-02-22T16:00:00Z | 1.0000 | 12118 | entered | 2025-02-22T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +9.1430 | +9.1430 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-04-02T20:00:00Z | 2025-04-03T08:00:00Z | 1.0000 | 12255 | entered | 2025-04-03T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0488 | -1.0488 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2025-06-25T04:00:00Z | 2025-07-02T12:00:00Z | 3.0663 | 12920 | passed_substituted | 2025-07-21T04:00:00Z | 2.0954 | 1 | 0 | 0 | 0 | +1.0934 | -1.0557 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-06T00:00:00Z | 2025-12-06T00:00:00Z | 2.1819 | 13703 | entered | 2025-12-06T00:00:00Z | 2.1819 | 0 | 0 | 0 | 0 | -0.8173 | -0.8173 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-29T08:00:00Z | 2025-12-29T20:00:00Z | 1.5751 | 13834 | entered | 2025-12-29T20:00:00Z | 1.5751 | 0 | 0 | 0 | 0 | -0.7982 | -0.7982 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2025-12-31T16:00:00Z | 2026-01-01T04:00:00Z | 1.1969 | 13844 | entered | 2026-01-01T04:00:00Z | 1.1969 | 0 | 0 | 0 | 0 | -0.9886 | -0.9886 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2026-03-20T12:00:00Z | 2026-03-24T16:00:00Z | 1.0587 | 14338 | entered | 2026-03-24T16:00:00Z | 1.0587 | 0 | 0 | 0 | 0 | -1.0562 | -1.0562 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2026-03-26T12:00:00Z | 2026-03-26T12:00:00Z | 1.3398 | 14410 | entered | 2026-03-26T12:00:00Z | 1.3398 | 0 | 0 | 0 | 0 | +0.8804 | +0.8804 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | -1 | 2026-06-17T16:00:00Z | 2026-06-18T04:00:00Z | 1.0000 | 14941 | entered | 2026-06-18T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +0.0132 | +0.0132 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 1 | 2026-09-14T16:00:00Z | 2026-09-14T16:00:00Z | 1.0000 | 15381 | entered | 2026-09-14T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.1055 | -1.1055 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-05-27T20:00:00Z | 2020-05-27T20:00:00Z | 2.3307 | 1204 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +2.7901 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-07-06T12:00:00Z | 2020-07-12T20:00:00Z | 2.1865 | 1394 | entered | 2020-07-12T20:00:00Z | 2.1865 | 0 | 0 | 0 | 0 | -0.9374 | -0.9374 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-07-20T04:00:00Z | 2020-08-08T08:00:00Z | 7.4653 | 1613 | passed_substituted | 2020-08-13T08:00:00Z | 1.5801 | 1 | 0 | 0 | 0 | -0.1891 | +1.4810 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2020-10-01T20:00:00Z | 2020-10-02T04:00:00Z | 1.1444 | 1905 | entered | 2020-10-02T04:00:00Z | 1.1444 | 0 | 0 | 0 | 0 | -1.0437 | -1.0437 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-11-02T00:00:00Z | 2020-11-02T00:00:00Z | 3.1075 | 2049 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8944 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-11-04T20:00:00Z | 2020-11-04T20:00:00Z | 1.0000 | 2268 | entered | 2020-11-04T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +4.3350 | +4.3350 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2020-12-13T08:00:00Z | 2020-12-13T08:00:00Z | 1.0000 | 2357 | entered | 2020-12-13T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +3.6422 | +3.6422 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2021-03-07T04:00:00Z | 2021-03-18T12:00:00Z | 1.1594 | 2890 | entered | 2021-03-18T12:00:00Z | 1.1594 | 0 | 0 | 0 | 0 | -1.0452 | -1.0452 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2021-03-29T12:00:00Z | 2021-04-08T20:00:00Z | 1.9678 | 3059 | entered | 2021-04-08T20:00:00Z | 1.9678 | 0 | 0 | 0 | 0 | +1.0215 | +1.0215 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2021-04-20T16:00:00Z | 2021-04-21T12:00:00Z | 1.9299 | 3224 | entered | 2021-04-21T12:00:00Z | 1.9299 | 0 | 0 | 0 | 0 | -1.0238 | -1.0238 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2021-06-08T00:00:00Z | 2021-06-08T00:00:00Z | 2.8740 | 3484 | passed_substituted | 2021-06-16T16:00:00Z | 1.0000 | 1 | 0 | 0 | 0 | +0.7859 | +6.7398 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2021-08-27T12:00:00Z | 2021-08-28T04:00:00Z | 2.0990 | 3908 | entered | 2021-08-28T04:00:00Z | 2.0990 | 0 | 0 | 0 | 0 | +1.7103 | +1.7103 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2021-12-28T04:00:00Z | 2021-12-28T04:00:00Z | 2.4105 | 4787 | passed_substituted | 2022-01-03T16:00:00Z | 1.7346 | 1 | 0 | 0 | 0 | +0.6596 | -1.0280 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-02-18T08:00:00Z | 2022-02-28T08:00:00Z | 1.0000 | 4949 | entered | 2022-02-28T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0267 | -1.0267 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-03-04T12:00:00Z | 2022-03-10T12:00:00Z | 1.6716 | 5043 | entered | 2022-03-10T12:00:00Z | 1.6716 | 0 | 0 | 0 | 0 | -0.7577 | -0.7577 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-09-07T00:00:00Z | 2022-09-07T04:00:00Z | 2.8952 | 6097 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -1.0180 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-10-07T12:00:00Z | 2022-10-08T04:00:00Z | 1.5166 | 6335 | entered | 2022-10-08T04:00:00Z | 1.5166 | 0 | 0 | 0 | 0 | +0.8031 | +0.8031 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2022-12-16T12:00:00Z | 2022-12-22T16:00:00Z | 1.0000 | 6799 | entered | 2022-12-22T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0727 | -1.0727 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2023-05-24T12:00:00Z | 2023-05-24T16:00:00Z | 1.9350 | 7665 | entered | 2023-05-24T16:00:00Z | 1.9350 | 0 | 0 | 0 | 0 | -1.0360 | -1.0360 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2023-07-13T12:00:00Z | 2023-07-13T12:00:00Z | 2.4343 | 7978 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.6132 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2023-08-31T16:00:00Z | 2023-09-01T04:00:00Z | 1.1959 | 8336 | entered | 2023-09-01T04:00:00Z | 1.1959 | 0 | 0 | 0 | 0 | -0.3978 | -0.3978 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2023-10-05T12:00:00Z | 2023-10-19T00:00:00Z | 2.0146 | 8541 | entered | 2023-10-19T00:00:00Z | 2.0146 | 0 | 0 | 0 | 0 | -1.0381 | -1.0381 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2023-11-19T16:00:00Z | 2023-11-20T08:00:00Z | 1.0000 | 8862 | entered | 2023-11-20T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0669 | -1.0669 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2023-12-13T16:00:00Z | 2023-12-14T16:00:00Z | 2.1530 | 8890 | entered | 2023-12-14T16:00:00Z | 2.1530 | 0 | 0 | 0 | 0 | -0.8374 | -0.8374 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2023-12-27T08:00:00Z | 2023-12-27T12:00:00Z | 3.3203 | 8993 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | -0.8097 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2024-03-31T04:00:00Z | 2024-03-31T04:00:00Z | 1.5778 | 9526 | entered | 2024-03-31T04:00:00Z | 1.5778 | 0 | 0 | 0 | 0 | -1.1095 | -1.1095 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-04-24T16:00:00Z | 2024-04-25T08:00:00Z | 1.0000 | 9683 | entered | 2024-04-25T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0481 | -1.0481 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-04-30T08:00:00Z | 2024-04-30T08:00:00Z | 2.2306 | 9731 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.3444 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-05-06T16:00:00Z | 2024-05-07T12:00:00Z | 1.4105 | 9801 | entered | 2024-05-07T12:00:00Z | 1.4105 | 0 | 0 | 0 | 0 | +1.3763 | +1.3763 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-09-15T16:00:00Z | 2024-09-16T00:00:00Z | 1.3721 | 10551 | entered | 2024-09-16T00:00:00Z | 1.3721 | 0 | 0 | 0 | 0 | -1.0476 | -1.0476 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2024-10-01T20:00:00Z | 2024-10-08T08:00:00Z | 1.0000 | 10697 | entered | 2024-10-08T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.3628 | -0.3628 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-01-26T20:00:00Z | 2025-01-26T20:00:00Z | 1.0000 | 11355 | entered | 2025-01-26T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +0.4907 | +0.4907 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-02-01T16:00:00Z | 2025-02-02T00:00:00Z | 2.9404 | 11490 | passed_substituted | 2025-02-13T12:00:00Z | 1.2666 | 1 | 0 | 0 | 0 | +1.5813 | -1.0285 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-02-24T12:00:00Z | 2025-02-24T12:00:00Z | 1.1693 | 11665 | entered | 2025-02-24T12:00:00Z | 1.1693 | 0 | 0 | 0 | 0 | +5.2363 | +5.2363 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-06-03T00:00:00Z | 2025-06-03T08:00:00Z | 2.4122 | 12107 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.5820 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-06-09T20:00:00Z | 2025-06-09T20:00:00Z | 2.1071 | 12155 | entered | 2025-06-09T20:00:00Z | 2.1071 | 0 | 0 | 0 | 0 | +0.4020 | +0.4020 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-06-16T16:00:00Z | 2025-06-16T16:00:00Z | 1.5567 | 12172 | entered | 2025-06-16T16:00:00Z | 1.5567 | 0 | 0 | 0 | 0 | -1.0334 | -1.0334 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-08-05T00:00:00Z | 2025-08-05T00:00:00Z | 1.0000 | 12558 | entered | 2025-08-05T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0521 | -1.0521 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-08-20T16:00:00Z | 2025-08-22T12:00:00Z | 2.6631 | 12615 | passed_no_substitute | — | — | 2 | 0 | 0 | 2 | +0.1414 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-09-11T08:00:00Z | 2025-09-18T00:00:00Z | 2.6236 | 12750 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.7758 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2025-10-01T20:00:00Z | 2025-10-08T20:00:00Z | 1.2676 | 12864 | entered | 2025-10-08T20:00:00Z | 1.2676 | 0 | 0 | 0 | 0 | -1.0463 | -1.0463 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2025-10-29T16:00:00Z | 2025-10-29T16:00:00Z | 1.0000 | 13191 | entered | 2025-10-29T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +6.1794 | +6.1794 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-02-27T12:00:00Z | 2026-02-28T04:00:00Z | 3.0633 | 13726 | passed_substituted | 2026-03-02T08:00:00Z | 1.3981 | 1 | 0 | 0 | 0 | -1.0148 | -1.0255 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-04-02T08:00:00Z | 2026-04-03T08:00:00Z | 1.1777 | 13932 | entered | 2026-04-03T08:00:00Z | 1.1777 | 0 | 0 | 0 | 0 | -0.4175 | -0.4175 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | -1 | 2026-06-18T12:00:00Z | 2026-06-18T16:00:00Z | 1.0000 | 14458 | entered | 2026-06-18T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0438 | -1.0438 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2026-08-05T16:00:00Z | 2026-08-05T16:00:00Z | 1.0000 | 14696 | entered | 2026-08-05T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0795 | -1.0795 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2026-08-17T08:00:00Z | 2026-08-30T12:00:00Z | 2.8049 | 14908 | passed_no_substitute | — | — | 3 | 0 | 0 | 3 | -1.0311 | — | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 1 | 2026-09-18T08:00:00Z | 2026-09-18T08:00:00Z | 1.7067 | 14963 | entered | 2026-09-18T08:00:00Z | 1.7067 | 0 | 0 | 0 | 0 | +2.7072 | +2.7072 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2020-12-04T16:00:00Z | 2020-12-04T16:00:00Z | 1.0000 | 640 | entered | 2020-12-04T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +4.4971 | +4.4971 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-03-07T08:00:00Z | 2021-03-07T20:00:00Z | 1.3163 | 1102 | entered | 2021-03-07T20:00:00Z | 1.3163 | 0 | 0 | 0 | 0 | -1.0391 | -1.0391 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-03-27T04:00:00Z | 2021-03-27T04:00:00Z | 3.8531 | 1435 | passed_substituted | 2021-05-09T08:00:00Z | 1.8142 | 3 | 0 | 0 | 2 | +2.2569 | -0.9378 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-05-11T20:00:00Z | 2021-05-12T08:00:00Z | 2.2502 | 1449 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.6498 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-05-16T00:00:00Z | 2021-05-16T00:00:00Z | 2.3587 | 1487 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8325 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2021-07-27T16:00:00Z | 2021-07-29T00:00:00Z | 1.0000 | 1910 | entered | 2021-07-29T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.7809 | -0.7809 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-09-18T16:00:00Z | 2021-09-19T00:00:00Z | 2.1302 | 2226 | entered | 2021-09-19T00:00:00Z | 2.1302 | 0 | 0 | 0 | 0 | -0.7784 | -0.7784 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-10-01T12:00:00Z | 2021-10-08T16:00:00Z | 1.0000 | 2350 | entered | 2021-10-08T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0249 | -1.0249 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2021-10-15T08:00:00Z | 2021-10-20T08:00:00Z | 1.5777 | 2572 | entered | 2021-10-20T08:00:00Z | 1.5777 | 0 | 0 | 0 | 0 | +4.7230 | +4.7230 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2021-12-29T04:00:00Z | 2022-01-17T08:00:00Z | 2.0324 | 3053 | entered | 2022-01-17T08:00:00Z | 2.0324 | 0 | 0 | 0 | 0 | +5.8468 | +5.8468 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-02-11T04:00:00Z | 2022-02-17T12:00:00Z | 1.0000 | 3197 | entered | 2022-02-17T12:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +0.8530 | +0.8530 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-09-15T12:00:00Z | 2022-09-23T08:00:00Z | 1.1400 | 4441 | entered | 2022-09-23T08:00:00Z | 1.1400 | 0 | 0 | 0 | 0 | -1.0307 | -1.0307 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-10-08T00:00:00Z | 2022-10-18T20:00:00Z | 2.7577 | 4632 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +0.9711 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-11-08T00:00:00Z | 2022-11-28T08:00:00Z | 1.0000 | 4928 | entered | 2022-11-28T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.1144 | -1.1144 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2022-12-16T12:00:00Z | 2022-12-16T16:00:00Z | 2.0638 | 5047 | entered | 2022-12-16T16:00:00Z | 2.0638 | 0 | 0 | 0 | 0 | +3.0396 | +3.0396 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2023-04-02T16:00:00Z | 2023-04-02T20:00:00Z | 1.9849 | 5598 | entered | 2023-04-02T20:00:00Z | 1.9849 | 0 | 0 | 0 | 0 | -0.7538 | -0.7538 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2023-07-27T04:00:00Z | 2023-07-27T04:00:00Z | 1.0000 | 6302 | entered | 2023-07-27T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.6097 | -0.6097 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2023-10-16T04:00:00Z | 2023-10-16T04:00:00Z | 1.2609 | 7253 | entered | 2023-10-16T04:00:00Z | 1.2609 | 0 | 0 | 0 | 0 | +0.6384 | +0.6384 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2024-01-28T00:00:00Z | 2024-02-02T00:00:00Z | 2.4501 | 7441 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.5133 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2024-02-07T20:00:00Z | 2024-02-08T00:00:00Z | 4.0629 | 7531 | passed_substituted | 2024-02-19T00:00:00Z | 1.8885 | 1 | 0 | 0 | 0 | +0.5237 | -0.6927 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2024-02-27T00:00:00Z | 2024-03-21T04:00:00Z | 1.6503 | 7794 | entered | 2024-03-21T04:00:00Z | 1.6503 | 0 | 0 | 0 | 0 | -1.0187 | -1.0187 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-04-24T20:00:00Z | 2024-04-25T08:00:00Z | 1.0855 | 7971 | entered | 2024-04-25T08:00:00Z | 1.0855 | 0 | 0 | 0 | 0 | +1.2210 | +1.2210 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2024-06-04T16:00:00Z | 2024-06-04T16:00:00Z | 1.8394 | 8177 | entered | 2024-06-04T16:00:00Z | 1.8394 | 0 | 0 | 0 | 0 | +0.0976 | +0.0976 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-07-04T04:00:00Z | 2024-07-07T16:00:00Z | 1.2499 | 8368 | entered | 2024-07-07T16:00:00Z | 1.2499 | 0 | 0 | 0 | 0 | -0.8402 | -0.8402 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-07-11T20:00:00Z | 2024-07-11T20:00:00Z | 1.0000 | 8393 | entered | 2024-07-11T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0316 | -1.0316 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2024-09-16T00:00:00Z | 2024-09-16T00:00:00Z | 2.1779 | 8797 | entered | 2024-09-16T00:00:00Z | 2.1779 | 0 | 0 | 0 | 0 | -1.0239 | -1.0239 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2024-11-06T00:00:00Z | 2024-11-06T00:00:00Z | 3.0084 | 9240 | passed_substituted | 2024-11-29T20:00:00Z | 1.0000 | 1 | 0 | 0 | 0 | +1.0160 | -1.0533 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2025-08-08T08:00:00Z | 2025-08-17T04:00:00Z | 1.6328 | 10800 | entered | 2025-08-17T04:00:00Z | 1.6328 | 0 | 0 | 0 | 0 | -1.0304 | -1.0304 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2025-08-22T12:00:00Z | 2025-08-22T16:00:00Z | 2.9303 | 11007 | passed_substituted | 2025-09-21T00:00:00Z | 2.1110 | 4 | 0 | 0 | 3 | -0.2568 | -1.0312 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2025-10-30T12:00:00Z | 2025-11-11T20:00:00Z | 2.7016 | 11440 | passed_substituted | 2025-11-29T16:00:00Z | 2.0339 | 1 | 0 | 0 | 0 | +0.8381 | -0.7625 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2025-12-05T16:00:00Z | 2025-12-05T20:00:00Z | 2.5520 | 11478 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8296 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2025-12-11T00:00:00Z | 2025-12-11T04:00:00Z | 2.6972 | 11615 | passed_substituted | 2025-12-23T00:00:00Z | 1.4693 | 2 | 0 | 0 | 1 | -0.1311 | +0.2354 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-02-27T16:00:00Z | 2026-02-28T04:00:00Z | 3.6783 | 11972 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8438 | — | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-03-26T16:00:00Z | 2026-04-07T00:00:00Z | 1.3336 | 12202 | entered | 2026-04-07T00:00:00Z | 1.3336 | 0 | 0 | 0 | 0 | -1.0550 | -1.0550 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | -1 | 2026-04-12T16:00:00Z | 2026-04-12T16:00:00Z | 1.4329 | 12226 | entered | 2026-04-12T16:00:00Z | 1.4329 | 0 | 0 | 0 | 0 | -1.0419 | -1.0419 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 1 | 2026-09-18T00:00:00Z | 2026-09-18T00:00:00Z | 1.7544 | 13211 | entered | 2026-09-18T00:00:00Z | 1.7544 | 0 | 0 | 0 | 0 | +1.4469 | +1.4469 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2020-12-27T16:00:00Z | 2020-12-27T16:00:00Z | 2.4511 | 629 | passed_substituted | 2021-01-22T12:00:00Z | 1.7694 | 2 | 0 | 0 | 1 | +1.4896 | +0.0821 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2021-02-25T16:00:00Z | 2021-02-25T16:00:00Z | 1.5476 | 818 | entered | 2021-02-25T16:00:00Z | 1.5476 | 0 | 0 | 0 | 0 | -1.0078 | -1.0078 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2021-03-29T08:00:00Z | 2021-04-04T20:00:00Z | 1.0611 | 1100 | entered | 2021-04-04T20:00:00Z | 1.0611 | 0 | 0 | 0 | 0 | -1.2828 | -1.2828 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-05-04T12:00:00Z | 2021-05-04T12:00:00Z | 1.8379 | 1224 | entered | 2021-05-04T12:00:00Z | 1.8379 | 0 | 0 | 0 | 0 | -0.9638 | -0.9638 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-06-16T08:00:00Z | 2021-06-18T00:00:00Z | 1.5549 | 1588 | entered | 2021-06-18T00:00:00Z | 1.5549 | 0 | 0 | 0 | 0 | -0.6224 | -0.6224 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2021-07-08T08:00:00Z | 2021-07-08T16:00:00Z | 1.0937 | 1692 | entered | 2021-07-08T16:00:00Z | 1.0937 | 0 | 0 | 0 | 0 | -0.4246 | -0.4246 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2021-10-02T12:00:00Z | 2021-10-06T12:00:00Z | 1.0000 | 2164 | entered | 2021-10-06T12:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +0.0776 | +0.0776 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2021-11-08T16:00:00Z | 2021-11-08T20:00:00Z | 1.8466 | 2383 | entered | 2021-11-08T20:00:00Z | 1.8466 | 0 | 0 | 0 | 0 | +0.1092 | +0.1092 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2022-01-11T00:00:00Z | 2022-01-11T00:00:00Z | 2.9914 | 2771 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +0.8129 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-02-10T20:00:00Z | 2022-02-17T16:00:00Z | 1.6725 | 3013 | entered | 2022-02-17T16:00:00Z | 1.6725 | 0 | 0 | 0 | 0 | +2.1736 | +2.1736 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2022-04-19T00:00:00Z | 2022-04-19T04:00:00Z | 1.7538 | 3325 | entered | 2022-04-19T04:00:00Z | 1.7538 | 0 | 0 | 0 | 0 | -0.7536 | -0.7536 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-06-28T04:00:00Z | 2022-06-28T04:00:00Z | 1.0000 | 3783 | entered | 2022-06-28T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +1.3659 | +1.3659 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-09-06T16:00:00Z | 2022-09-07T00:00:00Z | 1.6357 | 4157 | entered | 2022-09-07T00:00:00Z | 1.6357 | 0 | 0 | 0 | 0 | -0.8635 | -0.8635 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2022-12-07T12:00:00Z | 2022-12-07T20:00:00Z | 1.0000 | 4865 | entered | 2022-12-07T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0448 | -1.0448 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2023-02-02T00:00:00Z | 2023-02-02T16:00:00Z | 1.6009 | 5068 | entered | 2023-02-02T16:00:00Z | 1.6009 | 0 | 0 | 0 | 0 | -1.0315 | -1.0315 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2023-02-07T20:00:00Z | 2023-02-08T04:00:00Z | 2.6217 | 5087 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -1.0198 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-03-21T04:00:00Z | 2023-03-31T08:00:00Z | 2.0745 | 5391 | entered | 2023-03-31T08:00:00Z | 2.0745 | 0 | 0 | 0 | 0 | -1.0222 | -1.0222 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-04-02T16:00:00Z | 2023-04-03T00:00:00Z | 2.6074 | 5410 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -1.0167 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-06-05T12:00:00Z | 2023-06-05T12:00:00Z | 4.6008 | 5878 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +1.6496 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-07-24T08:00:00Z | 2023-07-31T16:00:00Z | 1.0000 | 6479 | entered | 2023-07-31T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0482 | -1.0482 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2023-10-03T20:00:00Z | 2023-10-17T16:00:00Z | 1.6264 | 6615 | entered | 2023-10-17T16:00:00Z | 1.6264 | 0 | 0 | 0 | 0 | -0.9004 | -0.9004 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2024-03-24T20:00:00Z | 2024-03-25T00:00:00Z | 1.0000 | 7586 | entered | 2024-03-25T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +0.4096 | +0.4096 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2024-05-04T04:00:00Z | 2024-05-13T20:00:00Z | 1.0868 | 7933 | entered | 2024-05-13T20:00:00Z | 1.0868 | 0 | 0 | 0 | 0 | -1.0367 | -1.0367 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2024-07-03T08:00:00Z | 2024-07-03T20:00:00Z | 2.9766 | 8199 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +0.7916 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2024-07-25T08:00:00Z | 2024-08-12T04:00:00Z | 2.0629 | 8441 | entered | 2024-08-12T04:00:00Z | 2.0629 | 0 | 0 | 0 | 0 | -1.0178 | -1.0178 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2024-10-20T20:00:00Z | 2024-10-20T20:00:00Z | 1.5709 | 8806 | entered | 2024-10-20T20:00:00Z | 1.5709 | 0 | 0 | 0 | 0 | -1.0349 | -1.0349 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-01-20T00:00:00Z | 2025-01-20T00:00:00Z | 1.2118 | 9347 | entered | 2025-01-20T00:00:00Z | 1.2118 | 0 | 0 | 0 | 0 | -1.0176 | -1.0176 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-02-23T12:00:00Z | 2025-02-24T12:00:00Z | 1.5698 | 9597 | entered | 2025-02-24T12:00:00Z | 1.5698 | 0 | 0 | 0 | 0 | +0.4262 | +0.4262 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-03-03T16:00:00Z | 2025-03-04T00:00:00Z | 2.9890 | 9707 | passed_substituted | 2025-03-07T00:00:00Z | 2.0762 | 1 | 0 | 0 | 0 | -0.1998 | +1.0449 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-03-29T04:00:00Z | 2025-04-15T12:00:00Z | 1.6149 | 9891 | entered | 2025-04-15T12:00:00Z | 1.6149 | 0 | 0 | 0 | 0 | -0.2898 | -0.2898 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2025-05-21T12:00:00Z | 2025-05-21T20:00:00Z | 1.0000 | 10097 | entered | 2025-05-21T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.2939 | -0.2939 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2025-05-29T00:00:00Z | 2025-05-29T00:00:00Z | 1.9688 | 10126 | entered | 2025-05-29T00:00:00Z | 1.9688 | 0 | 0 | 0 | 0 | -0.8324 | -0.8324 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-06-12T12:00:00Z | 2025-06-12T20:00:00Z | 1.8338 | 10313 | entered | 2025-06-12T20:00:00Z | 1.8338 | 0 | 0 | 0 | 0 | +0.4747 | +0.4747 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2025-08-08T08:00:00Z | 2025-08-12T16:00:00Z | 1.4205 | 10607 | entered | 2025-08-12T16:00:00Z | 1.4205 | 0 | 0 | 0 | 0 | -0.7008 | -0.7008 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2025-10-02T08:00:00Z | 2025-10-08T20:00:00Z | 1.0000 | 10929 | entered | 2025-10-08T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0418 | -1.0418 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-11-16T12:00:00Z | 2025-12-05T08:00:00Z | 3.1907 | 11400 | passed_substituted | 2025-12-11T04:00:00Z | 1.7997 | 1 | 0 | 0 | 0 | +0.2645 | +1.1629 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2025-12-29T16:00:00Z | 2025-12-30T20:00:00Z | 1.9132 | 11427 | entered | 2025-12-30T20:00:00Z | 1.9132 | 0 | 0 | 0 | 0 | -1.0161 | -1.0161 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2026-01-18T20:00:00Z | 2026-02-18T20:00:00Z | 2.4298 | 11757 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | -0.8950 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 1 | 2026-05-06T12:00:00Z | 2026-05-18T20:00:00Z | 2.4340 | 12355 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | +8.7450 | — | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | -1 | 2026-07-22T00:00:00Z | 2026-07-22T00:00:00Z | 1.0000 | 12807 | entered | 2026-07-22T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +2.0212 | +2.0212 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2020-06-22T08:00:00Z | 2020-06-22T12:00:00Z | 1.7658 | 866 | entered | 2020-06-22T12:00:00Z | 1.7658 | 0 | 0 | 0 | 0 | +0.4268 | +0.4268 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2020-07-06T16:00:00Z | 2020-07-21T08:00:00Z | 3.8684 | 1136 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +2.8952 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2020-12-07T00:00:00Z | 2020-12-07T12:00:00Z | 2.1696 | 1845 | entered | 2020-12-07T12:00:00Z | 2.1696 | 0 | 0 | 0 | 0 | -0.9399 | -0.9399 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2020-12-29T04:00:00Z | 2020-12-29T16:00:00Z | 1.9933 | 2022 | entered | 2020-12-29T16:00:00Z | 1.9933 | 0 | 0 | 0 | 0 | +0.1316 | +0.1316 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2021-03-09T00:00:00Z | 2021-03-18T00:00:00Z | 2.0673 | 2474 | entered | 2021-03-18T00:00:00Z | 2.0673 | 0 | 0 | 0 | 0 | -0.4239 | -0.4239 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2021-03-29T04:00:00Z | 2021-04-09T00:00:00Z | 3.2131 | 2657 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +0.9082 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2021-04-27T12:00:00Z | 2021-05-12T00:00:00Z | 3.2704 | 2797 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -1.0147 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2021-07-02T08:00:00Z | 2021-07-02T16:00:00Z | 1.0000 | 3220 | entered | 2021-07-02T16:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -0.8322 | -0.8322 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2021-12-28T04:00:00Z | 2021-12-28T08:00:00Z | 2.9999 | 4384 | passed_no_substitute | — | — | 5 | 0 | 0 | 5 | +0.0118 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2022-04-26T00:00:00Z | 2022-04-26T00:00:00Z | 1.0000 | 4869 | entered | 2022-04-26T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0313 | -1.0313 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-07-11T00:00:00Z | 2022-07-11T08:00:00Z | 1.1999 | 5352 | entered | 2022-07-11T08:00:00Z | 1.1999 | 0 | 0 | 0 | 0 | +1.1205 | +1.1205 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-06T16:00:00Z | 2022-09-06T20:00:00Z | 4.3440 | 5684 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | -0.8154 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-13T12:00:00Z | 2022-09-13T12:00:00Z | 3.0018 | 5788 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +0.6957 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-09-28T04:00:00Z | 2022-09-28T08:00:00Z | 1.1327 | 5838 | entered | 2022-09-28T08:00:00Z | 1.1327 | 0 | 0 | 0 | 0 | -1.0234 | -1.0234 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-10-06T16:00:00Z | 2022-10-07T00:00:00Z | 1.1141 | 5960 | entered | 2022-10-07T00:00:00Z | 1.1141 | 0 | 0 | 0 | 0 | +3.1047 | +3.1047 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-11-07T00:00:00Z | 2022-11-07T00:00:00Z | 1.3603 | 6134 | entered | 2022-11-07T00:00:00Z | 1.3603 | 0 | 0 | 0 | 0 | -1.0288 | -1.0288 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2022-11-27T20:00:00Z | 2022-11-27T20:00:00Z | 1.3631 | 6176 | entered | 2022-11-27T20:00:00Z | 1.3631 | 0 | 0 | 0 | 0 | -0.6165 | -0.6165 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2023-02-02T00:00:00Z | 2023-02-02T00:00:00Z | 2.0410 | 6578 | entered | 2023-02-02T00:00:00Z | 2.0410 | 0 | 0 | 0 | 0 | -1.0295 | -1.0295 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2023-08-15T00:00:00Z | 2023-08-15T08:00:00Z | 2.2113 | 7816 | passed_no_substitute | — | — | 0 | 0 | 0 | 0 | +4.7299 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2023-09-10T04:00:00Z | 2023-09-10T12:00:00Z | 2.0116 | 7898 | entered | 2023-09-10T12:00:00Z | 2.0116 | 0 | 0 | 0 | 0 | -0.7947 | -0.7947 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2024-04-24T16:00:00Z | 2024-04-25T08:00:00Z | 1.0000 | 9301 | entered | 2024-04-25T08:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0306 | -1.0306 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2024-06-04T16:00:00Z | 2024-06-05T04:00:00Z | 1.5898 | 9508 | entered | 2024-06-05T04:00:00Z | 1.5898 | 0 | 0 | 0 | 0 | -0.9794 | -0.9794 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2024-09-28T20:00:00Z | 2024-09-29T00:00:00Z | 1.2297 | 10235 | entered | 2024-09-29T00:00:00Z | 1.2297 | 0 | 0 | 0 | 0 | +2.7924 | +2.7924 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2024-10-28T00:00:00Z | 2024-10-28T08:00:00Z | 1.7251 | 10460 | entered | 2024-10-28T08:00:00Z | 1.7251 | 0 | 0 | 0 | 0 | -1.0214 | -1.0214 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2024-11-16T20:00:00Z | 2024-11-21T12:00:00Z | 1.0000 | 10621 | entered | 2024-11-21T12:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +1.0917 | +1.0917 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-01-18T16:00:00Z | 2025-01-19T04:00:00Z | 1.0000 | 11037 | entered | 2025-01-19T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0265 | -1.0265 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-04-13T20:00:00Z | 2025-04-13T20:00:00Z | 1.7699 | 11427 | entered | 2025-04-13T20:00:00Z | 1.7699 | 0 | 0 | 0 | 0 | +0.8287 | +0.8287 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2025-06-09T20:00:00Z | 2025-06-09T20:00:00Z | 1.6061 | 11724 | entered | 2025-06-09T20:00:00Z | 1.6061 | 0 | 0 | 0 | 0 | -0.9954 | -0.9954 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-08-11T20:00:00Z | 2025-08-12T00:00:00Z | 1.0000 | 12093 | entered | 2025-08-12T00:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | -1.0354 | -1.0354 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2025-08-14T20:00:00Z | 2025-08-14T20:00:00Z | 1.0956 | 12143 | entered | 2025-08-14T20:00:00Z | 1.0956 | 0 | 0 | 0 | 0 | -1.0252 | -1.0252 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2025-09-02T08:00:00Z | 2025-09-02T16:00:00Z | 2.5436 | 12703 | passed_substituted | 2025-09-21T04:00:00Z | 2.1824 | 2 | 0 | 0 | 1 | +0.8681 | -1.0234 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2025-12-24T16:00:00Z | 2025-12-24T20:00:00Z | 1.0000 | 12981 | entered | 2025-12-24T20:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +5.1566 | +5.1566 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2026-02-19T08:00:00Z | 2026-03-06T12:00:00Z | 2.3299 | 13383 | passed_no_substitute | — | — | 1 | 0 | 0 | 1 | -0.7735 | — | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | -1 | 2026-03-26T04:00:00Z | 2026-03-26T08:00:00Z | 1.0598 | 13476 | entered | 2026-03-26T08:00:00Z | 1.0598 | 0 | 0 | 0 | 0 | -0.3253 | -0.3253 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2026-04-23T16:00:00Z | 2026-04-23T16:00:00Z | 1.9658 | 13652 | entered | 2026-04-23T16:00:00Z | 1.9658 | 0 | 0 | 0 | 0 | +0.5087 | +0.5087 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2026-04-30T16:00:00Z | 2026-05-01T04:00:00Z | 1.0000 | 13821 | entered | 2026-05-01T04:00:00Z | 1.0000 | 0 | 0 | 0 | 0 | +25.0605 | +25.0605 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 1 | 2026-08-17T04:00:00Z | 2026-08-17T04:00:00Z | 1.4292 | 14542 | entered | 2026-08-17T04:00:00Z | 1.4292 | 0 | 0 | 0 | 0 | -1.0542 | -1.0542 | TIER-E | a SELECTION, not a result | nothing |

### The priority book vs v6, key by key (whole)

| symbol | entry_ms | in_v6 | in_priority | priority_substitute | v6_net_r | priority_net_r | r_over_atr | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-01-27T00:00:00Z | yes | no | no | +1.8131 | — | 2.6466 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-02-19T08:00:00Z | yes | yes | no | -1.0710 | -1.0710 | 1.1332 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-04-01T16:00:00Z | yes | no | no | -1.0189 | — | 2.2121 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-06-07T20:00:00Z | yes | yes | no | -0.6723 | -0.6723 | 1.9366 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-07-10T20:00:00Z | yes | yes | no | -1.1357 | -1.1357 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-08-14T04:00:00Z | yes | yes | no | -0.2358 | -0.2358 | 2.1369 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-11-29T16:00:00Z | yes | yes | no | +1.2069 | +1.2069 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-01-14T08:00:00Z | yes | no | no | -0.5390 | — | 3.5182 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-04-05T20:00:00Z | yes | yes | no | -1.0870 | -1.0870 | 1.7933 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-05-05T20:00:00Z | yes | yes | no | -1.1300 | -1.1300 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-06-25T08:00:00Z | yes | yes | no | -0.0628 | -0.0628 | 1.7600 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-07-01T12:00:00Z | yes | yes | no | -0.7894 | -0.7894 | 1.9788 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-07-05T16:00:00Z | yes | yes | no | -0.1772 | -0.1772 | 1.5015 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-10-29T16:00:00Z | yes | yes | no | -1.0655 | -1.0655 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-11-07T16:00:00Z | yes | yes | no | +3.1217 | +3.1217 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-01-17T08:00:00Z | yes | yes | no | -0.3716 | -0.3716 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-02-28T00:00:00Z | yes | yes | no | -1.0275 | -1.0275 | 1.3901 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-09-28T08:00:00Z | yes | yes | no | -0.8874 | -0.8874 | 1.6257 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-10-15T04:00:00Z | yes | yes | no | -0.7515 | -0.7515 | 1.7623 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-12-25T12:00:00Z | yes | yes | no | -1.1690 | -1.1690 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-05-04T04:00:00Z | yes | yes | no | -0.8185 | -0.8185 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-08-14T12:00:00Z | yes | yes | no | -1.1627 | -1.1627 | 1.3237 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-09-01T04:00:00Z | yes | yes | no | +0.0149 | +0.0149 | 1.0696 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-11-15T20:00:00Z | yes | no | no | -1.0290 | — | 2.6090 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-11-19T04:00:00Z | no | yes | yes | — | -0.7210 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-12-19T04:00:00Z | yes | yes | no | -1.0724 | -1.0724 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-01-04T12:00:00Z | yes | yes | no | -1.0557 | -1.0557 | 1.0554 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-10-24T20:00:00Z | yes | yes | no | -1.0955 | -1.0955 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-11-06T00:00:00Z | yes | no | no | +3.8512 | — | 2.5707 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-12-04T16:00:00Z | no | yes | yes | — | -1.1097 | 1.6228 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-01-23T12:00:00Z | yes | no | no | -0.8405 | — | 2.7789 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-02-22T16:00:00Z | yes | yes | no | +9.1430 | +9.1430 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-04-03T08:00:00Z | yes | yes | no | -1.0488 | -1.0488 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-07-02T12:00:00Z | yes | no | no | +1.0934 | — | 3.0663 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-07-21T04:00:00Z | no | yes | yes | — | -1.0557 | 2.0954 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-12-06T00:00:00Z | yes | yes | no | -0.8173 | -0.8173 | 2.1819 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-12-29T20:00:00Z | yes | yes | no | -0.7982 | -0.7982 | 1.5751 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-01-01T04:00:00Z | yes | yes | no | -0.9886 | -0.9886 | 1.1969 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-03-24T16:00:00Z | yes | yes | no | -1.0562 | -1.0562 | 1.0587 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-03-26T12:00:00Z | yes | yes | no | +0.8804 | +0.8804 | 1.3398 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-06-18T04:00:00Z | yes | yes | no | +0.0132 | +0.0132 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-09-14T16:00:00Z | yes | yes | no | -1.1055 | -1.1055 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-05-27T20:00:00Z | yes | no | no | +2.7901 | — | 2.3307 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-07-12T20:00:00Z | yes | yes | no | -0.9374 | -0.9374 | 2.1865 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-08-08T08:00:00Z | yes | no | no | -0.1891 | — | 7.4653 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-08-13T08:00:00Z | no | yes | yes | — | +1.4810 | 1.5801 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-10-02T04:00:00Z | yes | yes | no | -1.0437 | -1.0437 | 1.1444 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-11-02T00:00:00Z | yes | no | no | -0.8944 | — | 3.1075 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-11-04T20:00:00Z | yes | yes | no | +4.3350 | +4.3350 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-12-13T08:00:00Z | yes | yes | no | +3.6422 | +3.6422 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-03-18T12:00:00Z | yes | yes | no | -1.0452 | -1.0452 | 1.1594 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-04-08T20:00:00Z | yes | yes | no | +1.0215 | +1.0215 | 1.9678 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-04-21T12:00:00Z | yes | yes | no | -1.0238 | -1.0238 | 1.9299 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-06-08T00:00:00Z | yes | no | no | +0.7859 | — | 2.8740 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-06-16T16:00:00Z | no | yes | yes | — | +6.7398 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-08-28T04:00:00Z | yes | yes | no | +1.7103 | +1.7103 | 2.0990 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-12-28T04:00:00Z | yes | no | no | +0.6596 | — | 2.4105 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-01-03T16:00:00Z | no | yes | yes | — | -1.0280 | 1.7346 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-02-28T08:00:00Z | yes | yes | no | -1.0267 | -1.0267 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-03-10T12:00:00Z | yes | yes | no | -0.7577 | -0.7577 | 1.6716 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-09-07T04:00:00Z | yes | no | no | -1.0180 | — | 2.8952 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-10-08T04:00:00Z | yes | yes | no | +0.8031 | +0.8031 | 1.5166 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-12-22T16:00:00Z | yes | yes | no | -1.0727 | -1.0727 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-05-24T16:00:00Z | yes | yes | no | -1.0360 | -1.0360 | 1.9350 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-07-13T12:00:00Z | yes | no | no | -0.6132 | — | 2.4343 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-09-01T04:00:00Z | yes | yes | no | -0.3978 | -0.3978 | 1.1959 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-10-19T00:00:00Z | yes | yes | no | -1.0381 | -1.0381 | 2.0146 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-11-20T08:00:00Z | yes | yes | no | -1.0669 | -1.0669 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-12-14T16:00:00Z | yes | yes | no | -0.8374 | -0.8374 | 2.1530 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-12-27T12:00:00Z | yes | no | no | -0.8097 | — | 3.3203 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-03-31T04:00:00Z | yes | yes | no | -1.1095 | -1.1095 | 1.5778 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-04-25T08:00:00Z | yes | yes | no | -1.0481 | -1.0481 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-04-30T08:00:00Z | yes | no | no | -0.3444 | — | 2.2306 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-05-07T12:00:00Z | yes | yes | no | +1.3763 | +1.3763 | 1.4105 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-09-16T00:00:00Z | yes | yes | no | -1.0476 | -1.0476 | 1.3721 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-10-08T08:00:00Z | yes | yes | no | -0.3628 | -0.3628 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-01-26T20:00:00Z | yes | yes | no | +0.4907 | +0.4907 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-02-02T00:00:00Z | yes | no | no | +1.5813 | — | 2.9404 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-02-13T12:00:00Z | no | yes | yes | — | -1.0285 | 1.2666 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-02-24T12:00:00Z | yes | yes | no | +5.2363 | +5.2363 | 1.1693 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-03T08:00:00Z | yes | no | no | -0.5820 | — | 2.4122 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-09T20:00:00Z | yes | yes | no | +0.4020 | +0.4020 | 2.1071 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-16T16:00:00Z | yes | yes | no | -1.0334 | -1.0334 | 1.5567 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-08-05T00:00:00Z | yes | yes | no | -1.0521 | -1.0521 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-08-22T12:00:00Z | yes | no | no | +0.1414 | — | 2.6631 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-09-18T00:00:00Z | yes | no | no | -0.7758 | — | 2.6236 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-10-08T20:00:00Z | yes | yes | no | -1.0463 | -1.0463 | 1.2676 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-10-29T16:00:00Z | yes | yes | no | +6.1794 | +6.1794 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-02-28T04:00:00Z | yes | no | no | -1.0148 | — | 3.0633 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-03-02T08:00:00Z | no | yes | yes | — | -1.0255 | 1.3981 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-04-03T08:00:00Z | yes | yes | no | -0.4175 | -0.4175 | 1.1777 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-06-18T16:00:00Z | yes | yes | no | -1.0438 | -1.0438 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-08-05T16:00:00Z | yes | yes | no | -1.0795 | -1.0795 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-08-30T12:00:00Z | yes | no | no | -1.0311 | — | 2.8049 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-09-18T08:00:00Z | yes | yes | no | +2.7072 | +2.7072 | 1.7067 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2020-12-27T16:00:00Z | yes | no | no | +1.4896 | — | 2.4511 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-01-22T12:00:00Z | no | yes | yes | — | +0.0821 | 1.7694 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-02-25T16:00:00Z | yes | yes | no | -1.0078 | -1.0078 | 1.5476 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-04-04T20:00:00Z | yes | yes | no | -1.2828 | -1.2828 | 1.0611 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-05-04T12:00:00Z | yes | yes | no | -0.9638 | -0.9638 | 1.8379 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-06-18T00:00:00Z | yes | yes | no | -0.6224 | -0.6224 | 1.5549 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-07-08T16:00:00Z | yes | yes | no | -0.4246 | -0.4246 | 1.0937 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-10-06T12:00:00Z | yes | yes | no | +0.0776 | +0.0776 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-11-08T20:00:00Z | yes | yes | no | +0.1092 | +0.1092 | 1.8466 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-01-11T00:00:00Z | yes | no | no | +0.8129 | — | 2.9914 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-02-17T16:00:00Z | yes | yes | no | +2.1736 | +2.1736 | 1.6725 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-04-19T04:00:00Z | yes | yes | no | -0.7536 | -0.7536 | 1.7538 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-06-28T04:00:00Z | yes | yes | no | +1.3659 | +1.3659 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-09-07T00:00:00Z | yes | yes | no | -0.8635 | -0.8635 | 1.6357 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-12-07T20:00:00Z | yes | yes | no | -1.0448 | -1.0448 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-02-02T16:00:00Z | yes | yes | no | -1.0315 | -1.0315 | 1.6009 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-02-08T04:00:00Z | yes | no | no | -1.0198 | — | 2.6217 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-03-31T08:00:00Z | yes | yes | no | -1.0222 | -1.0222 | 2.0745 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-04-03T00:00:00Z | yes | no | no | -1.0167 | — | 2.6074 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-06-05T12:00:00Z | yes | no | no | +1.6496 | — | 4.6008 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-07-31T16:00:00Z | yes | yes | no | -1.0482 | -1.0482 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-10-17T16:00:00Z | yes | yes | no | -0.9004 | -0.9004 | 1.6264 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-03-25T00:00:00Z | yes | yes | no | +0.4096 | +0.4096 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-05-13T20:00:00Z | yes | yes | no | -1.0367 | -1.0367 | 1.0868 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-07-03T20:00:00Z | yes | no | no | +0.7916 | — | 2.9766 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-08-12T04:00:00Z | yes | yes | no | -1.0178 | -1.0178 | 2.0629 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-10-20T20:00:00Z | yes | yes | no | -1.0349 | -1.0349 | 1.5709 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-01-20T00:00:00Z | yes | yes | no | -1.0176 | -1.0176 | 1.2118 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-02-24T12:00:00Z | yes | yes | no | +0.4262 | +0.4262 | 1.5698 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-03-04T00:00:00Z | yes | no | no | -0.1998 | — | 2.9890 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-03-07T00:00:00Z | no | yes | yes | — | +1.0449 | 2.0762 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-04-15T12:00:00Z | yes | yes | no | -0.2898 | -0.2898 | 1.6149 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-05-21T20:00:00Z | yes | yes | no | -0.2939 | -0.2939 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-05-29T00:00:00Z | yes | yes | no | -0.8324 | -0.8324 | 1.9688 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-06-12T20:00:00Z | yes | yes | no | +0.4747 | +0.4747 | 1.8338 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-08-12T16:00:00Z | yes | yes | no | -0.7008 | -0.7008 | 1.4205 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-10-08T20:00:00Z | yes | yes | no | -1.0418 | -1.0418 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-12-05T08:00:00Z | yes | no | no | +0.2645 | — | 3.1907 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-12-11T04:00:00Z | no | yes | yes | — | +1.1629 | 1.7997 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-12-30T20:00:00Z | yes | yes | no | -1.0161 | -1.0161 | 1.9132 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-02-18T20:00:00Z | yes | no | no | -0.8950 | — | 2.4298 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-05-18T20:00:00Z | yes | no | no | +8.7450 | — | 2.4340 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-07-22T00:00:00Z | yes | yes | no | +2.0212 | +2.0212 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2020-12-04T16:00:00Z | yes | yes | no | +4.4971 | +4.4971 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-03-07T20:00:00Z | yes | yes | no | -1.0391 | -1.0391 | 1.3163 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-03-27T04:00:00Z | yes | no | no | +2.2569 | — | 3.8531 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-05-09T08:00:00Z | no | yes | yes | — | -0.9378 | 1.8142 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-05-12T08:00:00Z | yes | no | no | -0.6498 | — | 2.2502 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-05-16T00:00:00Z | yes | no | no | -0.8325 | — | 2.3587 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-07-29T00:00:00Z | yes | yes | no | -0.7809 | -0.7809 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-09-19T00:00:00Z | yes | yes | no | -0.7784 | -0.7784 | 2.1302 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-10-08T16:00:00Z | yes | yes | no | -1.0249 | -1.0249 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-10-20T08:00:00Z | yes | yes | no | +4.7230 | +4.7230 | 1.5777 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-01-17T08:00:00Z | yes | yes | no | +5.8468 | +5.8468 | 2.0324 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-02-17T12:00:00Z | yes | yes | no | +0.8530 | +0.8530 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-09-23T08:00:00Z | yes | yes | no | -1.0307 | -1.0307 | 1.1400 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-10-18T20:00:00Z | yes | no | no | +0.9711 | — | 2.7577 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-11-28T08:00:00Z | yes | yes | no | -1.1144 | -1.1144 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-12-16T16:00:00Z | yes | yes | no | +3.0396 | +3.0396 | 2.0638 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-04-02T20:00:00Z | yes | yes | no | -0.7538 | -0.7538 | 1.9849 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-07-27T04:00:00Z | yes | yes | no | -0.6097 | -0.6097 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-10-16T04:00:00Z | yes | yes | no | +0.6384 | +0.6384 | 1.2609 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-02-02T00:00:00Z | yes | no | no | -0.5133 | — | 2.4501 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-02-08T00:00:00Z | yes | no | no | +0.5237 | — | 4.0629 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-02-19T00:00:00Z | no | yes | yes | — | -0.6927 | 1.8885 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-03-21T04:00:00Z | yes | yes | no | -1.0187 | -1.0187 | 1.6503 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-04-25T08:00:00Z | yes | yes | no | +1.2210 | +1.2210 | 1.0855 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-06-04T16:00:00Z | yes | yes | no | +0.0976 | +0.0976 | 1.8394 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-07-07T16:00:00Z | yes | yes | no | -0.8402 | -0.8402 | 1.2499 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-07-11T20:00:00Z | yes | yes | no | -1.0316 | -1.0316 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-09-16T00:00:00Z | yes | yes | no | -1.0239 | -1.0239 | 2.1779 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-11-06T00:00:00Z | yes | no | no | +1.0160 | — | 3.0084 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-11-29T20:00:00Z | no | yes | yes | — | -1.0533 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-08-17T04:00:00Z | yes | yes | no | -1.0304 | -1.0304 | 1.6328 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-08-22T16:00:00Z | yes | no | no | -0.2568 | — | 2.9303 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-09-21T00:00:00Z | no | yes | yes | — | -1.0312 | 2.1110 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-11-11T20:00:00Z | yes | no | no | +0.8381 | — | 2.7016 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-11-29T16:00:00Z | no | yes | yes | — | -0.7625 | 2.0339 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-12-05T20:00:00Z | yes | no | no | -0.8296 | — | 2.5520 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-12-11T04:00:00Z | yes | no | no | -0.1311 | — | 2.6972 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-12-23T00:00:00Z | no | yes | yes | — | +0.2354 | 1.4693 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-02-28T04:00:00Z | yes | no | no | -0.8438 | — | 3.6783 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-04-07T00:00:00Z | yes | yes | no | -1.0550 | -1.0550 | 1.3336 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-04-12T16:00:00Z | yes | yes | no | -1.0419 | -1.0419 | 1.4329 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-09-18T00:00:00Z | yes | yes | no | +1.4469 | +1.4469 | 1.7544 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-06-22T12:00:00Z | yes | yes | no | +0.4268 | +0.4268 | 1.7658 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-07-21T08:00:00Z | yes | no | no | +2.8952 | — | 3.8684 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-12-07T12:00:00Z | yes | yes | no | -0.9399 | -0.9399 | 2.1696 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-12-29T16:00:00Z | yes | yes | no | +0.1316 | +0.1316 | 1.9933 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-03-18T00:00:00Z | yes | yes | no | -0.4239 | -0.4239 | 2.0673 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-04-09T00:00:00Z | yes | no | no | +0.9082 | — | 3.2131 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-05-12T00:00:00Z | yes | no | no | -1.0147 | — | 3.2704 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-07-02T16:00:00Z | yes | yes | no | -0.8322 | -0.8322 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-12-28T08:00:00Z | yes | no | no | +0.0118 | — | 2.9999 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-04-26T00:00:00Z | yes | yes | no | -1.0313 | -1.0313 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-07-11T08:00:00Z | yes | yes | no | +1.1205 | +1.1205 | 1.1999 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-06T20:00:00Z | yes | no | no | -0.8154 | — | 4.3440 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-13T12:00:00Z | yes | no | no | +0.6957 | — | 3.0018 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-28T08:00:00Z | yes | yes | no | -1.0234 | -1.0234 | 1.1327 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-10-07T00:00:00Z | yes | yes | no | +3.1047 | +3.1047 | 1.1141 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-11-07T00:00:00Z | yes | yes | no | -1.0288 | -1.0288 | 1.3603 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-11-27T20:00:00Z | yes | yes | no | -0.6165 | -0.6165 | 1.3631 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-02-02T00:00:00Z | yes | yes | no | -1.0295 | -1.0295 | 2.0410 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-08-15T08:00:00Z | yes | no | no | +4.7299 | — | 2.2113 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-09-10T12:00:00Z | yes | yes | no | -0.7947 | -0.7947 | 2.0116 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-04-25T08:00:00Z | yes | yes | no | -1.0306 | -1.0306 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-06-05T04:00:00Z | yes | yes | no | -0.9794 | -0.9794 | 1.5898 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-09-29T00:00:00Z | yes | yes | no | +2.7924 | +2.7924 | 1.2297 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-10-28T08:00:00Z | yes | yes | no | -1.0214 | -1.0214 | 1.7251 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-11-21T12:00:00Z | yes | yes | no | +1.0917 | +1.0917 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-01-19T04:00:00Z | yes | yes | no | -1.0265 | -1.0265 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-04-13T20:00:00Z | yes | yes | no | +0.8287 | +0.8287 | 1.7699 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-06-09T20:00:00Z | yes | yes | no | -0.9954 | -0.9954 | 1.6061 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-08-12T00:00:00Z | yes | yes | no | -1.0354 | -1.0354 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-08-14T20:00:00Z | yes | yes | no | -1.0252 | -1.0252 | 1.0956 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-09-02T16:00:00Z | yes | no | no | +0.8681 | — | 2.5436 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-09-21T04:00:00Z | no | yes | yes | — | -1.0234 | 2.1824 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-12-24T20:00:00Z | yes | yes | no | +5.1566 | +5.1566 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-03-06T12:00:00Z | yes | no | no | -0.7735 | — | 2.3299 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-03-26T08:00:00Z | yes | yes | no | -0.3253 | -0.3253 | 1.0598 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-04-23T16:00:00Z | yes | yes | no | +0.5087 | +0.5087 | 1.9658 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-05-01T04:00:00Z | yes | yes | no | +25.0605 | +25.0605 | 1.0000 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-08-17T04:00:00Z | yes | yes | no | -1.0542 | -1.0542 | 1.4292 | TIER-E | a SELECTION, not a result | nothing |

## Cross-asset same-close collisions (disclosure; cannot bind)

| book | n_campaigns | n_entry_closes | n_collision_closes | n_campaigns_in_collisions | max_assets_at_one_close | n_collisions_mixed_ratr_class | binds | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|
| v6 | 200 | 189 | 10 | 21 | 3 | 0 | no — one position per ASSET, no portfolio cap | TIER-E | a SELECTION, not a result | nothing |
| P-AGE-1 scored | 141 | 131 | 9 | 19 | 3 | 0 | no — one position per ASSET, no portfolio cap | TIER-E | a SELECTION, not a result | nothing |
| P-WIN-1 scored | 137 | 128 | 8 | 17 | 3 | 0 | no — one position per ASSET, no portfolio cap | TIER-E | a SELECTION, not a result | nothing |
| ratr admission | 147 | 138 | 8 | 17 | 3 | 0 | no — one position per ASSET, no portfolio cap | TIER-E | a SELECTION, not a result | nothing |
| ratr priority | 165 | 156 | 8 | 17 | 3 | 0 | no — one position per ASSET, no portfolio cap | TIER-E | a SELECTION, not a result | nothing |

v6 collisions, listed whole:

| entry_close_ms | entry_close | symbol | direction | r_over_atr | net_r | placeholder | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|
| 2022-01-17T12:00:00Z | 2022-01-17T12:00:00Z | BTCUSDT | -1 | 1.0000 | -0.3716 | no | TIER-E | a SELECTION, not a result | nothing |
| 2022-01-17T12:00:00Z | 2022-01-17T12:00:00Z | SOLUSDT | -1 | 2.0324 | +5.8468 | no | TIER-E | a SELECTION, not a result | nothing |
| 2022-09-28T12:00:00Z | 2022-09-28T12:00:00Z | BTCUSDT | -1 | 1.6257 | -0.8874 | no | TIER-E | a SELECTION, not a result | nothing |
| 2022-09-28T12:00:00Z | 2022-09-28T12:00:00Z | ZECUSDT | -1 | 1.1327 | -1.0234 | no | TIER-E | a SELECTION, not a result | nothing |
| 2023-09-01T08:00:00Z | 2023-09-01T08:00:00Z | BTCUSDT | -1 | 1.0696 | +0.0149 | no | TIER-E | a SELECTION, not a result | nothing |
| 2023-09-01T08:00:00Z | 2023-09-01T08:00:00Z | ETHUSDT | -1 | 1.1959 | -0.3978 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-04-25T12:00:00Z | 2024-04-25T12:00:00Z | ETHUSDT | -1 | 1.0000 | -1.0481 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-04-25T12:00:00Z | 2024-04-25T12:00:00Z | SOLUSDT | -1 | 1.0855 | +1.2210 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-04-25T12:00:00Z | 2024-04-25T12:00:00Z | ZECUSDT | -1 | 1.0000 | -1.0306 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-09-16T04:00:00Z | 2024-09-16T04:00:00Z | ETHUSDT | -1 | 1.3721 | -1.0476 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-09-16T04:00:00Z | 2024-09-16T04:00:00Z | SOLUSDT | -1 | 2.1779 | -1.0239 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-11-06T04:00:00Z | 2024-11-06T04:00:00Z | BTCUSDT | 1 | 2.5707 | +3.8512 | no | TIER-E | a SELECTION, not a result | nothing |
| 2024-11-06T04:00:00Z | 2024-11-06T04:00:00Z | SOLUSDT | 1 | 3.0084 | +1.0160 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-02-24T16:00:00Z | 2025-02-24T16:00:00Z | ETHUSDT | -1 | 1.1693 | +5.2363 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-02-24T16:00:00Z | 2025-02-24T16:00:00Z | NEARUSDT | -1 | 1.5698 | +0.4262 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-06-10T00:00:00Z | 2025-06-10T00:00:00Z | ETHUSDT | 1 | 2.1071 | +0.4020 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-06-10T00:00:00Z | 2025-06-10T00:00:00Z | ZECUSDT | 1 | 1.6061 | -0.9954 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-10-09T00:00:00Z | 2025-10-09T00:00:00Z | ETHUSDT | 1 | 1.2676 | -1.0463 | no | TIER-E | a SELECTION, not a result | nothing |
| 2025-10-09T00:00:00Z | 2025-10-09T00:00:00Z | NEARUSDT | 1 | 1.0000 | -1.0418 | no | TIER-E | a SELECTION, not a result | nothing |
| 2026-02-28T08:00:00Z | 2026-02-28T08:00:00Z | ETHUSDT | -1 | 3.0633 | -1.0148 | no | TIER-E | a SELECTION, not a result | nothing |
| 2026-02-28T08:00:00Z | 2026-02-28T08:00:00Z | SOLUSDT | -1 | 3.6783 | -0.8438 | no | TIER-E | a SELECTION, not a result | nothing |

## The re-ride rival log (every position_open rejection of the v6 ride)

A row with placeholder = yes means there is nothing to list: its key fields are sentinels ('(none)', -1, 0) and every other field is null.

| symbol | direction | trigger_ms | arm_ms | trigger_close_ms | blocker_entry_ms | blocker_exit_ms | blocker_net_r | placeholder | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|
| (none) | 0 | -1 | — | — | — | — | — | yes | TIER-E | a SELECTION, not a result | nothing |

## Campaigns entered after the TC10 pin (2026-09-21T16:00Z), and the continuation

continuation = entered at a close <= the TC10 pin, exit bar opening at or after it (open at the TC10 pin). A row with placeholder = yes means there is nothing of that kind: its key fields are sentinels ('(none)', -1) and every other field is empty or null.

| kind | symbol | entry_ms | entry | exit | exit_reason | net_r | tide_band | age_old_refused | lag | win_refused | placeholder | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| continuation | ETHUSDT | 2026-09-18T08:00:00Z | 2026-09-18T08:00:00Z | 2026-09-23T12:00:00Z | stop | +2.7072 | B3 | no | 0 | no | no | TIER-E | a SELECTION, not a result | nothing |
| entered_after_tc10_pin | (none) | -1 |  |  |  | — |  | — | — | — | yes | TIER-E | a SELECTION, not a result | nothing |

## Every v6 campaign's gate facts (200 rows, whole)

| symbol | entry_ms | direction | era | net_r | tide_streak_entry | tide_edge_q75 | tide_band | age_old_refused | age_abs206_refused | tide_streak_age_arm | arm_band_on_entry_edges | lag | win_refused | lag7_15_refused | r_over_atr | ratr_refused | grid_cell | tier | selection_not_a_result | gates |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-01-27T00:00:00Z | 1 | tuning | +1.8131 | 98 | 206.0000 | B3 | no | no | 97 | B3 | 1 | no | no | 2.6466 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-02-19T08:00:00Z | 1 | tuning | -1.0710 | 238 | 188.0000 | B4 | yes | yes | 234 | B4 | 4 | no | no | 1.1332 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-04-01T16:00:00Z | -1 | tuning | -1.0189 | 150 | 223.2500 | B3 | no | no | 124 | B3 | 26 | yes | no | 2.2121 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-06-07T20:00:00Z | 1 | tuning | -0.6723 | 250 | 214.0000 | B4 | yes | yes | 188 | B3 | 62 | yes | no | 1.9366 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-07-10T20:00:00Z | 1 | tuning | -1.1357 | 448 | 274.0000 | B4 | yes | yes | 6 | B1 | 23 | yes | no | 1.0000 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | -0.2358 | 654 | 353.0000 | B4 | yes | yes | 2 | B1 | 143 | yes | no | 2.1369 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | tuning | +1.2069 | 303 | 357.0000 | B3 | no | yes | 299 | B3 | 4 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-01-14T08:00:00Z | 1 | tuning | -0.5390 | 577 | 375.5000 | B4 | yes | yes | 384 | B4 | 193 | yes | no | 3.5182 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-04-05T20:00:00Z | 1 | tuning | -1.0870 | 1066 | 501.0000 | B4 | yes | yes | 1016 | B4 | 50 | yes | no | 1.7933 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-05-05T20:00:00Z | 1 | tuning | -1.1300 | 1246 | 577.0000 | B4 | yes | yes | 2 | B1 | 2 | no | no | 1.0000 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-06-25T08:00:00Z | -1 | tuning | -0.0628 | 252 | 585.5000 | B2 | no | yes | 212 | B2 | 40 | yes | no | 1.7600 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-07-01T12:00:00Z | -1 | tuning | -0.7894 | 289 | 580.0000 | B3 | no | yes | 287 | B3 | 2 | no | no | 1.9788 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-07-05T16:00:00Z | -1 | tuning | -0.1772 | 314 | 576.0000 | B3 | no | yes | 313 | B3 | 1 | no | no | 1.5015 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-10-29T16:00:00Z | 1 | tuning | -1.0655 | 158 | 476.0000 | B2 | no | no | 152 | B2 | 6 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | +3.1217 | 212 | 479.0000 | B2 | no | yes | 208 | B2 | 4 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-01-17T08:00:00Z | -1 | tuning | -0.3716 | 301 | 462.0000 | B3 | no | yes | 164 | B2 | 117 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-02-28T00:00:00Z | -1 | tuning | -1.0275 | 551 | 449.0000 | B4 | yes | yes | 5 | B1 | 59 | yes | no | 1.3901 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-09-28T08:00:00Z | -1 | tuning | -0.8874 | 238 | 445.0000 | B3 | no | yes | 86 | B1 | 4 | no | no | 1.6257 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-10-15T04:00:00Z | -1 | tuning | -0.7515 | 339 | 439.0000 | B3 | no | yes | 153 | B2 | 38 | yes | no | 1.7623 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2022-12-25T12:00:00Z | -1 | tuning | -1.1690 | 275 | 450.0000 | B3 | no | yes | 12 | B1 | 51 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-05-04T04:00:00Z | 1 | tuning | -0.8185 | 308 | 426.7500 | B3 | no | yes | 308 | B3 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-08-14T12:00:00Z | 1 | tuning | -1.1627 | 320 | 409.0000 | B3 | no | yes | 3 | B1 | 35 | yes | no | 1.3237 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-09-01T04:00:00Z | -1 | tuning | +0.0149 | 89 | 408.0000 | B1 | no | no | 87 | B1 | 2 | no | no | 1.0696 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-11-15T20:00:00Z | 1 | tuning | -1.0290 | 251 | 404.0000 | B3 | no | yes | 4 | B1 | 183 | yes | no | 2.6090 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2023-12-19T04:00:00Z | 1 | tuning | -1.0724 | 451 | 400.0000 | B4 | yes | yes | 385 | B3 | 2 | no | no | 1.0000 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-01-04T12:00:00Z | 1 | tuning | -1.0557 | 549 | 403.0000 | B4 | yes | yes | 469 | B4 | 16 | yes | no | 1.0554 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-10-24T20:00:00Z | 1 | holdout | -1.0955 | 200 | 407.0000 | B2 | no | no | 7 | B1 | 74 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | holdout | +3.8512 | 273 | 405.0000 | B3 | no | yes | 151 | B2 | 3 | no | no | 2.5707 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-01-23T12:00:00Z | 1 | holdout | -0.8405 | 744 | 403.0000 | B4 | yes | yes | 9 | B1 | 50 | yes | no | 2.7789 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | +9.1430 | 54 | 400.0000 | B1 | no | no | 2 | B1 | 5 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-04-03T08:00:00Z | -1 | holdout | -1.0488 | 292 | 402.0000 | B3 | no | yes | 242 | B3 | 3 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | holdout | +1.0934 | 419 | 399.0000 | B4 | yes | yes | 10 | B1 | 44 | yes | no | 3.0663 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-12-06T00:00:00Z | -1 | holdout | -0.8173 | 300 | 401.0000 | B3 | no | yes | 227 | B3 | 0 | no | no | 2.1819 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2025-12-29T20:00:00Z | -1 | holdout | -0.7982 | 443 | 403.0000 | B4 | yes | yes | 367 | B3 | 3 | no | no | 1.5751 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-01-01T04:00:00Z | -1 | holdout | -0.9886 | 457 | 404.0000 | B4 | yes | yes | 381 | B3 | 3 | no | no | 1.1969 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-03-24T16:00:00Z | -1 | holdout | -1.0562 | 371 | 406.0000 | B3 | no | yes | 14 | B1 | 25 | yes | no | 1.0587 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-03-26T12:00:00Z | -1 | holdout | +0.8804 | 382 | 406.0000 | B3 | no | yes | 50 | B1 | 0 | no | no | 1.3398 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-06-18T04:00:00Z | -1 | holdout | +0.0132 | 116 | 404.0000 | B2 | no | no | 113 | B2 | 3 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| BTCUSDT | 2026-09-14T16:00:00Z | 1 | holdout | -1.1055 | 153 | 396.0000 | B2 | no | no | 153 | B2 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | +2.7901 | 216 | 197.0000 | B4 | yes | yes | 216 | B4 | 0 | no | no | 2.3307 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-07-12T20:00:00Z | 1 | tuning | -0.9374 | 492 | 278.0000 | B4 | yes | yes | 50 | B1 | 38 | yes | no | 2.1865 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-08-08T08:00:00Z | 1 | tuning | -0.1891 | 651 | 335.0000 | B4 | yes | yes | 132 | B2 | 115 | yes | no | 7.4653 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-10-02T04:00:00Z | -1 | tuning | -1.0437 | 49 | 456.5000 | B1 | no | no | 3 | B1 | 2 | no | no | 1.1444 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-11-02T00:00:00Z | 1 | tuning | -0.8944 | 121 | 410.0000 | B2 | no | no | 121 | B2 | 0 | no | no | 3.1075 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | +4.3350 | 138 | 406.0000 | B2 | no | no | 10 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | +3.6422 | 369 | 347.0000 | B4 | yes | yes | 241 | B3 | 0 | no | no | 1.0000 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-03-18T12:00:00Z | 1 | tuning | -1.0452 | 940 | 462.0000 | B4 | yes | yes | 12 | B1 | 68 | yes | no | 1.1594 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | +1.0215 | 1068 | 510.0000 | B4 | yes | yes | 19 | B1 | 62 | yes | no | 1.9678 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-04-21T12:00:00Z | 1 | tuning | -1.0238 | 1144 | 545.0000 | B4 | yes | yes | 152 | B2 | 5 | no | no | 1.9299 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-06-08T00:00:00Z | -1 | tuning | +0.7859 | 53 | 602.0000 | B1 | no | no | 2 | B1 | 0 | no | no | 2.8740 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | tuning | +1.7103 | 163 | 526.0000 | B2 | no | no | 159 | B2 | 4 | no | no | 2.0990 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2021-12-28T04:00:00Z | -1 | tuning | +0.6596 | 86 | 474.7500 | B1 | no | no | 26 | B1 | 0 | no | no | 2.4105 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-02-28T08:00:00Z | -1 | tuning | -1.0267 | 459 | 450.0000 | B4 | yes | yes | 10 | B1 | 60 | yes | no | 1.0000 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-03-10T12:00:00Z | -1 | tuning | -0.7577 | 520 | 460.0000 | B4 | yes | yes | 13 | B1 | 36 | yes | no | 1.6716 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-09-07T04:00:00Z | -1 | tuning | -1.0180 | 47 | 452.0000 | B1 | no | no | 3 | B1 | 1 | no | no | 2.8952 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-10-08T04:00:00Z | -1 | tuning | +0.8031 | 131 | 441.0000 | B2 | no | no | 127 | B2 | 4 | no | no | 1.5166 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2022-12-22T16:00:00Z | -1 | tuning | -1.0727 | 248 | 449.0000 | B3 | no | yes | 10 | B1 | 37 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-05-24T16:00:00Z | -1 | tuning | -1.0360 | 44 | 421.0000 | B1 | no | no | 4 | B1 | 1 | no | no | 1.9350 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-07-13T12:00:00Z | 1 | tuning | -0.6132 | 107 | 411.0000 | B2 | no | no | 29 | B1 | 0 | no | no | 2.4343 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-09-01T04:00:00Z | -1 | tuning | -0.3978 | 174 | 408.0000 | B2 | no | no | 134 | B2 | 3 | no | no | 1.1959 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-10-19T00:00:00Z | -1 | tuning | -1.0381 | 461 | 407.0000 | B4 | yes | yes | 17 | B1 | 81 | yes | no | 2.0146 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-11-20T08:00:00Z | 1 | tuning | -1.0669 | 157 | 403.0000 | B2 | no | no | 153 | B2 | 4 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-12-14T16:00:00Z | 1 | tuning | -0.8374 | 303 | 399.0000 | B3 | no | yes | 297 | B3 | 6 | no | no | 2.1530 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2023-12-27T12:00:00Z | 1 | tuning | -0.8097 | 380 | 401.0000 | B3 | no | yes | 379 | B3 | 1 | no | no | 3.3203 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-03-31T04:00:00Z | 1 | tuning | -1.1095 | 948 | 423.0000 | B4 | yes | yes | 67 | B1 | 0 | no | no | 1.5778 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-04-25T08:00:00Z | -1 | tuning | -1.0481 | 51 | 427.0000 | B1 | no | no | 2 | B1 | 4 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-04-30T08:00:00Z | -1 | tuning | -0.3444 | 81 | 428.0000 | B1 | no | no | 9 | B1 | 0 | no | no | 2.2306 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-05-07T12:00:00Z | -1 | tuning | +1.3763 | 124 | 427.0000 | B2 | no | no | 47 | B1 | 5 | no | no | 1.4105 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-09-16T00:00:00Z | -1 | holdout | -1.0476 | 316 | 410.0000 | B3 | no | yes | 290 | B3 | 2 | no | no | 1.3721 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2024-10-08T08:00:00Z | -1 | holdout | -0.3628 | 450 | 408.0000 | B4 | yes | yes | 3 | B1 | 39 | yes | no | 1.0000 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | +0.4907 | 90 | 403.0000 | B2 | no | no | 14 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-02-02T00:00:00Z | -1 | holdout | +1.5813 | 127 | 402.0000 | B2 | no | no | 6 | B1 | 2 | no | no | 2.9404 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | +5.2363 | 262 | 400.0000 | B3 | no | yes | 143 | B2 | 0 | no | no | 1.1693 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-03T08:00:00Z | 1 | holdout | -0.5820 | 147 | 404.0000 | B2 | no | no | 145 | B2 | 2 | no | no | 2.4122 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-09T20:00:00Z | 1 | holdout | +0.4020 | 186 | 403.0000 | B2 | no | no | 186 | B2 | 0 | no | no | 2.1071 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-06-16T16:00:00Z | 1 | holdout | -1.0334 | 227 | 402.0000 | B3 | no | yes | 227 | B3 | 0 | no | no | 1.5567 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-08-05T00:00:00Z | 1 | holdout | -1.0521 | 523 | 401.0000 | B4 | yes | yes | 205 | B2 | 0 | no | no | 1.0000 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | +0.1414 | 628 | 402.7500 | B4 | yes | yes | 299 | B3 | 11 | no | yes | 2.6631 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-09-18T00:00:00Z | 1 | holdout | -0.7758 | 787 | 403.0000 | B4 | yes | yes | 429 | B4 | 40 | yes | no | 2.6236 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-10-08T20:00:00Z | 1 | holdout | -1.0463 | 912 | 404.0000 | B4 | yes | yes | 4 | B1 | 42 | yes | no | 1.2676 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | +6.1794 | 93 | 403.0000 | B2 | no | no | 12 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-02-28T04:00:00Z | -1 | holdout | -1.0148 | 222 | 407.0000 | B3 | no | yes | 218 | B3 | 4 | no | no | 3.0633 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-04-03T08:00:00Z | -1 | holdout | -0.4175 | 427 | 407.0000 | B4 | yes | yes | 90 | B2 | 6 | no | no | 1.1777 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-06-18T16:00:00Z | -1 | holdout | -1.0438 | 189 | 404.0000 | B2 | no | no | 188 | B2 | 1 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-08-05T16:00:00Z | 1 | holdout | -1.0795 | 96 | 399.0000 | B2 | no | no | 14 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-08-30T12:00:00Z | 1 | holdout | -1.0311 | 245 | 398.0000 | B3 | no | yes | 35 | B1 | 79 | yes | no | 2.8049 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | +2.7072 | 358 | 396.0000 | B3 | no | yes | 227 | B3 | 0 | no | no | 1.7067 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | +4.4971 | 174 | 348.0000 | B2 | no | no | 8 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-03-07T20:00:00Z | 1 | tuning | -1.0391 | 358 | 443.0000 | B3 | no | yes | 355 | B3 | 3 | no | no | 1.3163 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | +2.2569 | 474 | 477.0000 | B3 | no | yes | 474 | B3 | 0 | no | no | 3.8531 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-05-12T08:00:00Z | 1 | tuning | -0.6498 | 751 | 591.0000 | B4 | yes | yes | 748 | B4 | 3 | no | no | 2.2502 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-05-16T00:00:00Z | 1 | tuning | -0.8325 | 773 | 597.0000 | B4 | yes | yes | 773 | B4 | 0 | no | no | 2.3587 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-07-29T00:00:00Z | -1 | tuning | -0.7809 | 221 | 554.0000 | B2 | no | yes | 116 | B2 | 8 | no | yes | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-09-19T00:00:00Z | 1 | tuning | -0.7784 | 271 | 505.0000 | B3 | no | yes | 269 | B3 | 2 | no | no | 2.1302 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-10-08T16:00:00Z | 1 | tuning | -1.0249 | 389 | 488.0000 | B3 | no | yes | 346 | B3 | 43 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | tuning | +4.7230 | 459 | 479.0000 | B3 | no | yes | 429 | B3 | 30 | yes | no | 1.5777 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | +5.8468 | 227 | 462.0000 | B3 | no | yes | 5 | B1 | 115 | yes | no | 2.0324 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | +0.8530 | 414 | 447.0000 | B3 | no | yes | 269 | B3 | 38 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-09-23T08:00:00Z | -1 | tuning | -1.0307 | 207 | 446.0000 | B2 | no | yes | 13 | B1 | 47 | yes | no | 1.1400 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-10-18T20:00:00Z | -1 | tuning | +0.9711 | 360 | 438.0000 | B3 | no | yes | 148 | B2 | 65 | yes | no | 2.7577 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-11-28T08:00:00Z | -1 | tuning | -1.1144 | 603 | 439.0000 | B4 | yes | yes | 3 | B1 | 122 | yes | no | 1.0000 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | +3.0396 | 713 | 446.0000 | B4 | yes | yes | 234 | B3 | 1 | no | no | 2.0638 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-04-02T20:00:00Z | -1 | tuning | -0.7538 | 47 | 435.7500 | B1 | no | no | 3 | B1 | 1 | no | no | 1.9849 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-07-27T04:00:00Z | 1 | tuning | -0.6097 | 116 | 410.0000 | B2 | no | no | 116 | B2 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2023-10-16T04:00:00Z | 1 | tuning | +0.6384 | 81 | 407.0000 | B1 | no | no | 19 | B1 | 0 | no | no | 1.2609 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-02-02T00:00:00Z | 1 | tuning | -0.5133 | 734 | 415.0000 | B4 | yes | yes | 15 | B1 | 30 | yes | no | 2.4501 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-02-08T00:00:00Z | 1 | tuning | +0.5237 | 770 | 416.0000 | B4 | yes | yes | 80 | B1 | 1 | no | no | 4.0629 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-03-21T04:00:00Z | 1 | tuning | -1.0187 | 1023 | 421.7500 | B4 | yes | yes | 195 | B2 | 139 | yes | no | 1.6503 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-04-25T08:00:00Z | -1 | tuning | +1.2210 | 42 | 427.0000 | B1 | no | no | 3 | B1 | 3 | no | no | 1.0855 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-06-04T16:00:00Z | 1 | tuning | +0.0976 | 108 | 426.0000 | B2 | no | no | 108 | B2 | 0 | no | no | 1.8394 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-07-07T16:00:00Z | -1 | holdout | -0.8402 | 140 | 420.0000 | B2 | no | no | 7 | B1 | 21 | yes | no | 1.2499 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-07-11T20:00:00Z | -1 | holdout | -1.0316 | 165 | 419.0000 | B2 | no | no | 53 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-09-16T00:00:00Z | -1 | holdout | -1.0239 | 225 | 410.0000 | B3 | no | yes | 116 | B2 | 0 | no | no | 2.1779 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | holdout | +1.0160 | 147 | 405.0000 | B2 | no | no | 147 | B2 | 0 | no | no | 3.0084 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-08-17T04:00:00Z | 1 | holdout | -1.0304 | 221 | 402.0000 | B3 | no | yes | 12 | B1 | 53 | yes | no | 1.6328 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-08-22T16:00:00Z | 1 | holdout | -0.2568 | 254 | 403.0000 | B3 | no | yes | 97 | B2 | 1 | no | no | 2.9303 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | +0.8381 | 172 | 402.0000 | B2 | no | no | 21 | B1 | 74 | yes | no | 2.7016 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-12-05T20:00:00Z | -1 | holdout | -0.8296 | 316 | 401.0000 | B3 | no | yes | 238 | B3 | 1 | no | no | 2.5520 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2025-12-11T04:00:00Z | -1 | holdout | -0.1311 | 348 | 401.0000 | B3 | no | yes | 270 | B3 | 1 | no | no | 2.6972 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-02-28T04:00:00Z | -1 | holdout | -0.8438 | 235 | 407.0000 | B3 | no | yes | 232 | B3 | 3 | no | no | 3.6783 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-04-07T00:00:00Z | -1 | holdout | -1.0550 | 462 | 408.0000 | B4 | yes | yes | 59 | B1 | 68 | yes | no | 1.3336 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-04-12T16:00:00Z | -1 | holdout | -1.0419 | 496 | 409.0000 | B4 | yes | yes | 161 | B2 | 0 | no | no | 1.4329 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| SOLUSDT | 2026-09-18T00:00:00Z | 1 | holdout | +1.4469 | 178 | 396.0000 | B2 | no | no | 178 | B2 | 0 | no | no | 1.7544 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | tuning | +1.4896 | 125 | 360.0000 | B2 | no | no | 7 | B1 | 0 | no | no | 2.4511 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-02-25T16:00:00Z | 1 | tuning | -1.0078 | 485 | 426.0000 | B4 | yes | yes | 367 | B3 | 0 | no | no | 1.5476 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | -1.2828 | 714 | 498.7500 | B4 | yes | yes | 557 | B4 | 39 | yes | no | 1.0611 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-05-04T12:00:00Z | -1 | tuning | -0.9638 | 60 | 574.2500 | B1 | no | no | 4 | B1 | 0 | no | no | 1.8379 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-06-18T00:00:00Z | -1 | tuning | -0.6224 | 173 | 592.0000 | B2 | no | no | 163 | B2 | 10 | no | yes | 1.5549 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-07-08T16:00:00Z | -1 | tuning | -0.4246 | 297 | 573.0000 | B3 | no | yes | 295 | B3 | 2 | no | no | 1.0937 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-10-06T12:00:00Z | 1 | tuning | +0.0776 | 340 | 490.0000 | B3 | no | yes | 17 | B1 | 24 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2021-11-08T20:00:00Z | 1 | tuning | +0.1092 | 540 | 480.0000 | B4 | yes | yes | 159 | B2 | 1 | no | no | 1.8466 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | tuning | +0.8129 | 118 | 466.0000 | B2 | no | no | 118 | B2 | 0 | no | no | 2.9914 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | +2.1736 | 121 | 447.0000 | B2 | no | no | 6 | B1 | 41 | yes | no | 1.6725 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-04-19T04:00:00Z | 1 | tuning | -0.7536 | 153 | 459.0000 | B2 | no | no | 152 | B2 | 1 | no | no | 1.7538 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-06-28T04:00:00Z | -1 | tuning | +1.3659 | 350 | 429.0000 | B3 | no | yes | 350 | B3 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-09-07T00:00:00Z | -1 | tuning | -0.8635 | 84 | 452.0000 | B1 | no | no | 82 | B1 | 2 | no | no | 1.6357 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2022-12-07T20:00:00Z | -1 | tuning | -1.0448 | 508 | 443.0000 | B4 | yes | yes | 506 | B4 | 2 | no | no | 1.0000 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-02-02T16:00:00Z | 1 | tuning | -1.0315 | 108 | 453.0000 | B2 | no | no | 104 | B2 | 4 | no | no | 1.6009 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-02-08T04:00:00Z | 1 | tuning | -1.0198 | 141 | 452.0000 | B2 | no | no | 139 | B2 | 2 | no | no | 2.6217 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-03-31T08:00:00Z | -1 | tuning | -1.0222 | 150 | 436.0000 | B2 | no | no | 9 | B1 | 61 | yes | no | 2.0745 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-04-03T00:00:00Z | -1 | tuning | -1.0167 | 166 | 435.0000 | B2 | no | no | 84 | B1 | 2 | no | no | 2.6074 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-06-05T12:00:00Z | -1 | tuning | +1.6496 | 255 | 418.0000 | B3 | no | yes | 255 | B3 | 0 | no | no | 4.6008 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-07-31T16:00:00Z | -1 | tuning | -1.0482 | 592 | 410.0000 | B4 | yes | yes | 4 | B1 | 44 | yes | no | 1.0000 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2023-10-17T16:00:00Z | -1 | tuning | -0.9004 | 1060 | 407.0000 | B4 | yes | yes | 433 | B4 | 83 | yes | no | 1.6264 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-03-25T00:00:00Z | 1 | tuning | +0.4096 | 255 | 422.0000 | B3 | no | yes | 254 | B3 | 1 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-05-13T20:00:00Z | 1 | tuning | -1.0367 | 554 | 427.0000 | B4 | yes | yes | 5 | B1 | 58 | yes | no | 1.0868 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-07-03T20:00:00Z | -1 | holdout | +0.7916 | 136 | 421.0000 | B2 | no | no | 133 | B2 | 3 | no | no | 2.9766 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-08-12T04:00:00Z | -1 | holdout | -1.0178 | 372 | 413.0000 | B3 | no | yes | 6 | B1 | 107 | yes | no | 2.0629 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2024-10-20T20:00:00Z | 1 | holdout | -1.0349 | 158 | 408.0000 | B2 | no | no | 21 | B1 | 0 | no | no | 1.5709 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-01-20T00:00:00Z | -1 | holdout | -1.0176 | 164 | 403.0000 | B2 | no | no | 12 | B1 | 0 | no | no | 1.2118 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | +0.4262 | 377 | 400.0000 | B3 | no | yes | 219 | B3 | 6 | no | no | 1.5698 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-03-04T00:00:00Z | -1 | holdout | -0.1998 | 422 | 399.0000 | B4 | yes | yes | 268 | B3 | 2 | no | no | 2.9890 | yes | A1¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-04-15T12:00:00Z | -1 | holdout | -0.2898 | 677 | 403.0000 | B4 | yes | yes | 421 | B4 | 104 | yes | no | 1.6149 | no | A1¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | -0.2939 | 64 | 406.0000 | B1 | no | no | 62 | B1 | 2 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-05-29T00:00:00Z | 1 | holdout | -0.8324 | 107 | 404.0000 | B2 | no | no | 20 | B1 | 0 | no | no | 1.9688 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-06-12T20:00:00Z | -1 | holdout | +0.4747 | 66 | 402.0000 | B1 | no | no | 6 | B1 | 2 | no | no | 1.8338 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | -0.7008 | 171 | 402.0000 | B2 | no | no | 7 | B1 | 26 | yes | no | 1.4205 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-10-08T20:00:00Z | 1 | holdout | -1.0418 | 159 | 404.0000 | B2 | no | no | 7 | B1 | 39 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | +0.2645 | 314 | 401.0000 | B3 | no | yes | 1 | B1 | 113 | yes | no | 3.1907 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2025-12-30T20:00:00Z | -1 | holdout | -1.0161 | 467 | 404.0000 | B4 | yes | yes | 260 | B3 | 7 | no | yes | 1.9132 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-02-18T20:00:00Z | -1 | holdout | -0.8950 | 767 | 407.0000 | B4 | yes | yes | 7 | B1 | 186 | yes | no | 2.4298 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | +8.7450 | 232 | 408.0000 | B3 | no | yes | 3 | B1 | 74 | yes | no | 2.4340 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| NEARUSDT | 2026-07-22T00:00:00Z | -1 | holdout | +2.0212 | 26 | 401.0000 | B1 | no | no | 4 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | +0.4268 | 355 | 239.0000 | B4 | yes | yes | 223 | B3 | 1 | no | no | 1.7658 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | tuning | +2.8952 | 528 | 294.0000 | B4 | yes | yes | 309 | B4 | 88 | yes | no | 3.8684 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-12-07T12:00:00Z | 1 | tuning | -0.9399 | 109 | 345.0000 | B2 | no | no | 106 | B2 | 3 | no | no | 2.1696 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2020-12-29T16:00:00Z | -1 | tuning | +0.1316 | 26 | 361.0000 | B1 | no | no | 2 | B1 | 3 | no | no | 1.9933 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-03-18T00:00:00Z | 1 | tuning | -0.4239 | 400 | 461.0000 | B3 | no | yes | 47 | B1 | 54 | yes | no | 2.0673 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-04-09T00:00:00Z | 1 | tuning | +0.9082 | 532 | 510.0000 | B4 | yes | yes | 10 | B1 | 65 | yes | no | 3.2131 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-05-12T00:00:00Z | 1 | tuning | -1.0147 | 730 | 590.0000 | B4 | yes | yes | 186 | B2 | 87 | yes | no | 3.2704 | yes | A1¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-07-02T16:00:00Z | -1 | tuning | -0.8322 | 244 | 579.0000 | B2 | no | yes | 242 | B2 | 2 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2021-12-28T08:00:00Z | -1 | tuning | +0.0118 | 87 | 474.0000 | B1 | no | no | 86 | B1 | 1 | no | no | 2.9999 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-04-26T00:00:00Z | 1 | tuning | -1.0313 | 278 | 456.0000 | B3 | no | yes | 2 | B1 | 0 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-07-11T08:00:00Z | -1 | tuning | +1.1205 | 444 | 434.0000 | B4 | yes | yes | 442 | B4 | 2 | no | no | 1.1999 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-06T20:00:00Z | -1 | tuning | -0.8154 | 92 | 452.0000 | B1 | no | no | 75 | B1 | 1 | no | no | 4.3440 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | +0.6957 | 132 | 450.0000 | B2 | no | no | 22 | B1 | 0 | no | no | 3.0018 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-09-28T08:00:00Z | -1 | tuning | -1.0234 | 221 | 445.0000 | B2 | no | yes | 110 | B2 | 1 | no | no | 1.1327 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | +3.1047 | 273 | 442.0000 | B3 | no | yes | 161 | B2 | 2 | no | no | 1.1141 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-11-07T00:00:00Z | -1 | tuning | -1.0288 | 459 | 434.0000 | B4 | yes | yes | 349 | B3 | 0 | no | no | 1.3603 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2022-11-27T20:00:00Z | -1 | tuning | -0.6165 | 584 | 438.7500 | B4 | yes | yes | 474 | B4 | 0 | no | no | 1.3631 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-02-02T00:00:00Z | 1 | tuning | -1.0295 | 105 | 453.0000 | B2 | no | no | 3 | B1 | 0 | no | no | 2.0410 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | +4.7299 | 116 | 409.0000 | B2 | no | no | 8 | B1 | 2 | no | no | 2.2113 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2023-09-10T12:00:00Z | -1 | tuning | -0.7947 | 273 | 407.7500 | B3 | no | yes | 165 | B2 | 2 | no | no | 2.0116 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-04-25T08:00:00Z | -1 | tuning | -1.0306 | 96 | 427.0000 | B2 | no | no | 92 | B1 | 4 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-06-05T04:00:00Z | 1 | tuning | -0.9794 | 63 | 426.0000 | B1 | no | no | 60 | B1 | 3 | no | no | 1.5898 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | +2.7924 | 143 | 409.0000 | B2 | no | no | 52 | B1 | 1 | no | no | 1.2297 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-10-28T08:00:00Z | 1 | holdout | -1.0214 | 91 | 406.0000 | B2 | no | no | 89 | B2 | 2 | no | no | 1.7251 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | +1.0917 | 236 | 402.0000 | B3 | no | yes | 12 | B1 | 28 | yes | no | 1.0000 | no | A0¦W1¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-01-19T04:00:00Z | -1 | holdout | -1.0265 | 48 | 403.0000 | B1 | no | no | 5 | B1 | 3 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | +0.8287 | 2 | 403.0000 | B1 | no | no | 2 | B1 | 0 | no | no | 1.7699 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-06-09T20:00:00Z | 1 | holdout | -0.9954 | 207 | 403.0000 | B2 | no | yes | 207 | B2 | 0 | no | no | 1.6061 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-08-12T00:00:00Z | -1 | holdout | -1.0354 | 101 | 402.0000 | B2 | no | no | 87 | B1 | 1 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-08-14T20:00:00Z | -1 | holdout | -1.0252 | 118 | 402.0000 | B2 | no | no | 9 | B1 | 0 | no | no | 1.0956 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | +0.8681 | 40 | 403.0000 | B1 | no | no | 4 | B1 | 2 | no | no | 2.5436 | yes | A0¦W0¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | +5.1566 | 34 | 402.0000 | B1 | no | no | 2 | B1 | 1 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-03-06T12:00:00Z | -1 | holdout | -0.7735 | 311 | 407.0000 | B3 | no | yes | 213 | B3 | 91 | yes | no | 2.3299 | yes | A0¦W1¦S1 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | -0.3253 | 430 | 406.0000 | B4 | yes | yes | 47 | B1 | 1 | no | no | 1.0598 | no | A1¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | holdout | +0.5087 | 89 | 409.0000 | B2 | no | no | 89 | B2 | 0 | no | no | 1.9658 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | +25.0605 | 134 | 409.0000 | B2 | no | no | 131 | B2 | 3 | no | no | 1.0000 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |
| ZECUSDT | 2026-08-17T04:00:00Z | 1 | holdout | -1.0542 | 224 | 399.0000 | B3 | no | yes | 2 | B1 | 0 | no | no | 1.4292 | no | A0¦W0¦S0 | TIER-E | a SELECTION, not a result | nothing |

## Files

- `stage_g/g_age_crosstab.parquet` content sha 2f3d01b0158f9640b43eeaa8bb04c85a4a9d34f33d192373f0534e92100ec60a (key ['cell']; floats at 6 dp)
- `stage_g/g_arrivals.parquet` content sha b19b468c9192ca9e640a63efc13524915bdcd09e83c02e05b01c6083337be5b5 (key ['kind', 'symbol', 'entry_ms']; floats at 6 dp)
- `stage_g/g_campaign_gates.parquet` content sha 196ddc1c00bd4ac1c83a2eb2a30a4f986364aac783abc75c8c02f98b391762a5 (key ['symbol', 'entry_ms']; floats at 6 dp)
- `stage_g/g_collision_list_v6.parquet` content sha 3d210291125aeffb7d6892a11771dc304739c1297e55078fb735496fa5ebe845 (key ['entry_close_ms', 'symbol']; floats at 6 dp)
- `stage_g/g_collisions.parquet` content sha 3a3e9178b33de18ee7c39ca92ee95ce65543c7963600117f7daad88f1a4f1d31 (key ['book']; floats at 6 dp)
- `stage_g/g_era_slices.parquet` content sha d9643e3faaf9035d0e565e05aaeb7fdb7b3d982891a53bff340919c5732059cd (key ['registration', 'book', 'era']; floats at 6 dp)
- `stage_g/g_gate_rows.parquet` content sha 1f88b0a5c2818f97ec51360a818ba4eafe97c48c41ec528da45ba144bbf8fe9e (key ['gate']; floats at 6 dp)
- `stage_g/g_grid_books.parquet` content sha cce5f1ccc8ff61b390c6733a856909fd5cbbd873185cfa37ee9f939fde943683 (key ['cell']; floats at 6 dp)
- `stage_g/g_grid_partition.parquet` content sha d786f529981e8b496648ddf1f269acbc277f7b4d3c78114066b6d86fabb20abd (key ['cell']; floats at 6 dp)
- `stage_g/g_lag_bands.parquet` content sha f64f99670b8aebeaa97f41c7efbc408dbc70175b85ddeb295ed8fd33b5d68ce0 (key ['lag_band']; floats at 6 dp)
- `stage_g/g_priority_vs_v6.parquet` content sha 7b359c5679def52036ff571f105867285fa8a769ea9b11265c5c0fb76d6641b5 (key ['symbol', 'entry_ms']; floats at 6 dp)
- `stage_g/g_priority_windows.parquet` content sha 5de969792e571b7b48e40d8c216e44b802fb64b321131993da7e0e7e8bbde085 (key ['symbol', 'arm_ms', 'direction']; floats at 6 dp)
- `stage_g/g_registered_books.parquet` content sha 190a523c06f68f7d52f3732804c236e1472fb029cf094dcf89b51d436d51df32 (key ['registration', 'arm']; floats at 6 dp)
- `stage_g/g_rivals.parquet` content sha 2c6bb8c8778ac1a2dee835a69a01f7f5dc67dfb10900f7a2d065bdd71e96d380 (key ['symbol', 'trigger_ms', 'direction']; floats at 6 dp)
- `stage_g/g_tide_bands.parquet` content sha b2f32c84c17ecfe22aca4a504fbbe1cbf11e1d7bc3a1189b40ac64e97202e40d (key ['measure', 'band']; floats at 6 dp)
- `stage_g/g_tiere_books.parquet` content sha a1de44ac30a6c4c9793f9e8af2f7f4fd1c6023afa2c33c1ab83a4b221a94ad8a (key ['registration', 'arm']; floats at 6 dp)
- `regbooks/P-AGE-1/base.parquet` n 200 · ΣR +40.807565 · book_sha256 f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 · parquet file sha256 dbfe4788610b11cc70ef64be31aac95949b921f086eaeb66b4535fbbad7af4ce (base, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-AGE-1/scored.parquet` n 141 · ΣR +63.464131 · book_sha256 d008fa5086ce14f578403c083169e28c5870701fd37f3cb2b03c5474f04f22d8 · parquet file sha256 6440a6e0d14cfbf1c62df19246a066d0f7086a1e64aae3bb0ced8c2b2a624dca (scored, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-AGE-1/tierE__holdout.parquet` n 60 · ΣR +52.001614 · book_sha256 f7331ba52363642520df489500970333494bdf0f7ab90f4ce3ee342d74d91183 · parquet file sha256 e9e4bed0b1fe49b06f8b426065e8e5c8d24d968e1e71ee7c55a4cbdbd6843ba0 (tierE, two_sample, holdout; entry bars straddling the era cut 0)
- `regbooks/P-AGE-1/tierE__refused_cohort.parquet` n 59 · ΣR -22.656566 · book_sha256 0569170404a1d10cb80c1021278423e53b5c0a0ad26030940098c1770e2d9838 · parquet file sha256 71b6444b0dbc8cb87551bb2bc3676d78d987b6e791e49ff2a00cb376344edeb5 (tierE, vs_zero, full; entry bars straddling the era cut 0)
- `regbooks/P-AGE-1/tierE__shadow_abs206.parquet` n 80 · ΣR +48.803986 · book_sha256 2c1e47eec765be4a531205ff26dfb495d21efa42788fdea1c9d673b6e385d169 · parquet file sha256 f12cef30cad2f230010d07e2fe1a63fae47c0dbecad38576eb363c97a31726bb (tierE, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-AGE-1/tierE__tuning.parquet` n 81 · ΣR +11.462516 · book_sha256 4acc5b91b27e1a931480218f038ffe5749f04479d4dcd0add1a3b84b79bcf7c5 · parquet file sha256 0c2efa513e58aec3ee194333f0feba0f614a8d0299dcb371948822c04cb97600 (tierE, two_sample, tuning; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/base.parquet` n 200 · ΣR +40.807565 · book_sha256 f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 · parquet file sha256 dbfe4788610b11cc70ef64be31aac95949b921f086eaeb66b4535fbbad7af4ce (base, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/scored.parquet` n 137 · ΣR +51.974019 · book_sha256 fd3f407ad6b1867039bb24a42816678e4992b9204ed65971058e48fa2bdabbfe · parquet file sha256 824c5e08ca79511fea96b98d65b74e8e7209f36379d881a2ff02f927db08241c (scored, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__holdout.parquet` n 56 · ΣR +43.951452 · book_sha256 7cdb206beff5ae4d8a45827e54f1450744fe3c6fc1b7cd06d801c0ec4afa07b3 · parquet file sha256 797b440c1e7bf89c7a6dcde54a430de5d13fbf2a8d459ce24295cca935569b3b (tierE, two_sample, holdout; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__ratr_admission.parquet` n 147 · ΣR +19.115450 · book_sha256 dcfffefbddad389657173b6458f5c88e9ec26865621742740bbd9f8f033201c8 · parquet file sha256 92be97b10f21e81115c72f43d1cfca94c22662c7f8d0b16ab6c13e45266147b9 (tierE, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__ratr_priority.parquet` n 165 · ΣR +18.392480 · book_sha256 a10416bd49c47a08766078e075a1f4187f75aa36f3a29ef521cfc5698403a7f3 · parquet file sha256 50a2cc140c540f0030e28fbd9865c8a4e93802aca14ec8faada4a83c021befd9 (tierE, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__refused_cohort.parquet` n 63 · ΣR -11.166454 · book_sha256 7a97b32895c78324c22dacc563efdec38e98ffa8fe196f0e9629d5ed6b3bacf6 · parquet file sha256 a92c5589596490ee5a67cbc688a7a502164eb9a514332e1c201ee6387900d89b (tierE, vs_zero, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__shadow_lag7_15.parquet` n 196 · ΣR +43.085655 · book_sha256 f624bffc3baea05741a1a94b61699997a0e4d615ce52649fb02b3277866d7fae · parquet file sha256 4b308d854a30b49b4e7c53282243a41d676f71974439d36612261680778f589c (tierE, two_sample, full; entry bars straddling the era cut 0)
- `regbooks/P-WIN-1/tierE__tuning.parquet` n 81 · ΣR +8.022567 · book_sha256 862fc6fd0a237ed4b6f84e250d4737048eedc58910911c05840606fbcb714218 · parquet file sha256 d5dbd141007787c3b10fb37ef2aa25b91697f1315ed35c9b6cf845a76cee66b4 (tierE, two_sample, tuning; entry bars straddling the era cut 0)

Canonical CSV law of book_sha256: sha256 of the UTF-8 canonical CSV of the 16 required columns in interface order, rows sorted by (symbol, entry_close_ms) (mergesort), header = the column names joined by ',', one row per line joined by ',', '\n' after every line (the last included); int columns and direction as str(int), floats as repr(float), strings verbatim (no ',' or newline allowed).

Fixtures: `scripts/tierc11_stage_g_fixtures.py` (F-DEF · F-GATE · F-PRIORITY · F-GRID · F-KEY · F-DET); transcript of record `research_outputs/tierc11/stage_g/FIXTURES_STAGE_G.txt`.
