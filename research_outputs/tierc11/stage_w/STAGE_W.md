as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE W — early warnings from the 1h crosses

Contract: exchange/queue/2026-09-24_TC11_APOLLO.md (bb38e016…) STAGE W. Readings L-W.0..L-W.6, L-1.5, AM-3, AM-5, AM-6, AM-7. Seed 20260924 (sensitivity 20260816), N_BOOT 4000. Corridor 2019-09-08T16:00:00Z → 2026-09-25T00:00:00Z, CLASSIC5.

Every table below except the P-WARN-1 condition block and the regbook arms is Tier-E — tier TIER-E · a SELECTION, not a result · gates nothing — and carries no verdict word. Every grid is printed whole.

## Readings (executor)

- [LEAN-HEPHAESTUS] L-W.2 events = 1h engine-EMA-of-close crosses 9/12, 12/26, 12/89 (RD.cross_1h), known at the 1h close where the fast line changes side; with = the trade's direction, counter = against.
- [LEAN-HEPHAESTUS] L-W.1 visible at a 4h instant T iff the 1h close <= T.
- [LEAN-HEPHAESTUS] L-W.3 IN-TRADE = entry close < taken < the 1h-resolved exit (RD exit_close_ms); PRE-ENTRY = arm close < taken <= entry close; before +1R = taken < the L-W.3 latch (RD plus1r_1h_ms; none = any in-trade); after = >=.
- [LEAN-HEPHAESTUS] L-W.4 at-risk sets: before-+1R and pre-entry -> whole book; after-+1R -> reached +1R; 9/12 re-cross -> open 1h after entry; condition = T5.cluster_boot_diff(cohort C1, whole book, seed 20260924, n_boot 4000), MET iff cluster-90% hi < 0.
- [LEAN-HEPHAESTUS] L-W.5 rule book = RD.transform_book(v6, walk=True, warn_of=RD.warn_of(12/89)); L-1.5 identity law on every campaign the rule never acted on.
- [LEAN-HEPHAESTUS] L-W.6 relay evidence = the first 1h with-trend 12/26 cross with arm close < taken < the 4h trigger close, per v6 window.
- [LEAN-HEPHAESTUS] (w1) an event on a mismatch bar is TAKEN at the parent's close [L-W.0]; (w5) the mark = the campaign exited at the event, booked by tierc7._account_chain; (w6) 9/12 at-risk = exit > entry close + 1h; (w7) every v6 window = the campaign windows; the armed windows holding no v6 campaign are a twin.
- [LEAN-HEPHAESTUS] AM-7 haircut_net_r = net_r − fee_r × slip/taker per stem (E.fees()).
- [LEAN-HEPHAESTUS] (w10) C3 '9/12 re-cross with trend after entry' = ANY in-trade with-trend 1h 9/12 cross (the reading of the first build, disclosed); C3S, printed beside and deciding nothing = the STRICT reading: a with-trend 9/12 cross whose preceding 9/12 cross on the 1h tape is a counter cross closing after the entry close.
- [LEAN-HEPHAESTUS] (w11) AM-7's haircut twin beside every per-campaign net R (W1_CAMPAIGNS, W2_RELAY_WINDOWS) and the complement table's sums; L-1.3 entry bars straddling the era cut printed as a count (sidecars, STAGE_W.md).
- [LEAN-HEPHAESTUS] (w12) W1 on every 4h campaign (final-review MINOR-1): the 9/12 book, P-BRK-4H scored and P-RELAY-1 scored stamped Tier-E by the same event tape and classifiers as v6 (W1_EVENTS_OTHER, W1_CAMPAIGNS_OTHER, W1_OTHER_SUMMARY: counts and W2's cohort sizes only, no outcome statistic).
- [LEAN-HEPHAESTUS] (w13) window open = the 9/12 book's arm close; P-BRK-4H's 4h death close; P-RELAY-1's v6 window arm close.  A relay's entry = its 1h close: its in-trade window starts there.
- [LEAN-HEPHAESTUS] (w14) 1h resolution of the books ridden without the walk (9/12, P-BRK-4H) by the ride module's resolver (RD.transform_book / RD.ride11 with the walk), the book's WHAT reproduced exactly per campaign, else the 4h-close fallback, labelled with its reason; P-RELAY-1 by its path of record (RD.relay11 walk_after), reproduced exactly or HALT.

## Changes after first output (disclosed; no net_r moved)

(the builder's first-output files are not on disk; both changes are stated from the code's own law texts and the Stage W verifier's report (finding 2).)

| id | what | first output | now | why | what moved |
|---|---|---|---|---|---|
| CH-1 | the (w7) twin population | every triggered candidate window of v6's card, admission ignored | every ARMED window of v6's card (tide + displacement gates passed) holding no v6 campaign: triggered-not-entered (end = trigger close) or never triggered (end = the known window close, else the as-of) | on this corridor the first population IS the v6 campaign set (200 triggered gate-passing windows == the 200 v6 windows, none refused by an open position; relay_twin_check), so the twin duplicated the population it stands beside | W2_RELAY_WINDOWS_TWIN and the armed_windows_not_entered rows of W2_RELAY_SUMMARY / W2_RELAY_HIST only (Tier-E, gates nothing); no net_r moved |
| CH-2 | the regbook column exit_close_ms | the 1h-resolved exit instant (L-W.3) | the CLOSE of the 4h exit bar (the estate's v6 schema); the exact 1h instant is the extra column exit_instant_ms | books/v6_campaigns.parquet carries exit_close_ms as the 4h exit-bar close and the scorer's SC-7 F-BASE-IDENT compares the base arm to it column by column | that column and so each arm's book_sha256; no net_r / gross_r / fee_r / funding_r moved |

Repair of 2026-09-25 (the Stage W verifier's MINOR findings; no rule, cohort, condition number or registered figure moved): the (w7) docstring rewritten to the twin as built; this block; AM-7 haircut columns beside every per-campaign net R (w11); condition.json's collar `gates` set to 'nothing' with the gating statement moved to `condition_role`; `cohort_law_holds` computed by the frozen law (belltie keys listed separately, never absorbed); the C3 reading disclosed as (w10) with the strict reading C3S printed beside; the L-1.3 straddle count printed; fixtures extended (independent marks, relay leads and twin windows hand-walked, mismatch plants on every C1 first event and on latch / stop-exit bars, timeline columns).

Final-review repair G7 (2026-09-25; fidelity MINOR-1 "W1 stamps only v6"): the Tier-E W1 stamps of the other 4h books — the 9/12 book, P-BRK-4H scored, P-RELAY-1 scored — added as W1_EVENTS_OTHER, W1_CAMPAIGNS_OTHER and W1_OTHER_SUMMARY (readings w12..w14; section "W1 on the other 4h books" below). Every table above that section, the P-WARN-1 regbooks, condition.json and STATUS.json are byte-identical to the build before it; no registered number moved.

## P-WARN-1 · the condition block (the only Tier-E place a CI is printed)

- cohort (v6 campaigns with an IN-TRADE counter 12/89 1h cross before the +1R latch): n 42, mean net R -0.5246
- whole v6 book: n 200, mean net R +0.2040
- delta = mean(cohort) − mean(book) = -0.728647; cluster-90% [-0.964287, -0.527794] (seed 20260924, n_boot 4000)
- condition MET (ci_hi < 0): **True** → STATUS **BUILT**
- sensitivity seed 20260816: [-0.982843, -0.530065] (hi < 0: True) — decides nothing
- rival (cohort vs complement, w9): complement n 158, delta -0.922338, cluster-90% [-1.174333, -0.686751] — decides nothing
- cohort law (the frozen L-W.4 law; fixture F-WARN-COHORT): warn-exit keys 42, cohort keys 42, listed mismatch-bar keys none; cohort == warn ∪ mismatch: True. Belltie keys (listed separately, never absorbed): 0
- collar: tier TIER-E · a SELECTION, not a result · gates nothing; role: the registered condition of P-WARN-1 (L-W.4): `met` decides only whether P-WARN-1's rule book is the scored arm or a collared Tier-E arm; it decides nothing else

Per asset (cohort vs book):

| asset | cohort n | cohort mean | book n | book mean |
|---|---|---|---|---|
| BTCUSDT | 11 | -0.5842 | 39 | -0.1267 |
| ETHUSDT | 11 | -0.3497 | 48 | +0.1264 |
| SOLUSDT | 8 | -0.6407 | 36 | +0.2705 |
| NEARUSDT | 7 | -0.7001 | 40 | -0.0392 |
| ZECUSDT | 5 | -0.3470 | 37 | +0.8517 |

## P-WARN-1 · the regbook arms (book, not a verdict)

| arm | kind | era_scope | n | sum net R | mean net R | sum haircut R | entry bars straddling the era cut | book_sha256 |
|---|---|---|---|---|---|---|---|---|
| scored | scored | full | 200 | +41.9232 | +0.2096 | +37.8140 | 0 | 956e15390419f8ab… |
| base | base | full | 200 | +40.8076 | +0.2040 | +36.6975 | 0 | f41bfaf02b86dfb0… |
| tierE__tuning | tierE | tuning | 123 | +0.3410 | +0.0028 | -2.0887 | 0 | c41450b34294d820… |
| tierE__holdout | tierE | holdout | 77 | +41.5822 | +0.5400 | +39.9027 | 0 | 9dd70a94cb2b2923… |

All rows are books, not verdicts. The scorer (scripts/tierc11_score.py) reads the regbook dir.

- identity law (L-1.5) on the rule book: {'n': 200, 'acted': 42, 'unacted': 158, 'worst': 0.0}; walked v6 (no rule): {'n': 200, 'acted': 0, 'unacted': 200, 'worst': 0.0}, CTRL_COLS worst 0.000e+00
- mismatch bars ridden (AM-5): rule book 1, base 1: ['ZECUSDT 2024-10-28T20:00:00Z']
- re-ride rival (L-1.5 disclosure): 0 acted campaigns hold a freed-slot candidate (0 candidates, 0 with a valid stop); the rule book admits none
- the two +1R latch readings (AM-6) agree on 200/200; latch present == v6 reached_1r on 200/200
- events on mismatch bars (taken at the parent close, w1): 0; classifications the raw instant would change: 0
- W1 phase counts: {'AT-EXIT': 65, 'IN-TRADE': 1658, 'POST-EXIT': 50, 'PRE-ENTRY': 1914}; base exits resolved by {'1h': 196, 'close': 4}
- L-1.3 straddle counts (open <= the era cut < close): v6 campaign entry bars 0; twin-window end bars 0; per arm in the table above
- (w10) C3 vs its strict reading C3S: C3 members 109, C3S members 109; members whose FIRST C3 event is not a strict re-cross (the 9/12 counter-side at the entry close): 3 ['BTCUSDT 2025-02-22T16:00:00Z', 'ETHUSDT 2026-04-03T08:00:00Z', 'NEARUSDT 2021-10-06T12:00:00Z']; C3 members outside C3S: none — C3S decides nothing
- warn exits ON the close of v6's harvest bar (the last child of that bar; the ride books the child's warn exit before the 4h close's HARVEST slot, so the rule book books no harvest there; the last child's close is the parent's close, the harvest fill price): 2
  - BTCUSDT 2026-01-01T04:00:00Z: warn exit 2026-01-01T20:00:00Z at 88354.8; v6 harvest px 88354.8 (|diff| 0.000e+00); rule harvested False; rule net R -0.893352, v6 net R -0.988606
  - ZECUSDT 2020-12-07T12:00:00Z: warn exit 2020-12-08T12:00:00Z at 71.64; v6 harvest px 71.64 (|diff| 0.000e+00); rule harvested False; rule net R -0.846080, v6 net R -0.939888

## W1 · the 1h event tape inside the v6 campaign windows (Tier-E, whole)

Every 1h engine-EMA cross with arm close < taken <= the exit-bar close, by phase (L-W.3, w2) × pair × side (L-W.2); in-trade rows split by the +1R latch relation.

| phase | pair | side | latch | n events | n campaigns |
|---|---|---|---|---|---|
| PRE-ENTRY | 9/12 | counter | — | 527 | 71 |
| PRE-ENTRY | 9/12 | with | — | 523 | 69 |
| PRE-ENTRY | 12/26 | counter | — | 299 | 67 |
| PRE-ENTRY | 12/26 | with | — | 293 | 66 |
| PRE-ENTRY | 12/89 | counter | — | 133 | 66 |
| PRE-ENTRY | 12/89 | with | — | 139 | 73 |
| IN-TRADE | 9/12 | counter | before | 227 | 106 |
| IN-TRADE | 9/12 | counter | after | 336 | 99 |
| IN-TRADE | 9/12 | with | before | 161 | 62 |
| IN-TRADE | 9/12 | with | after | 250 | 76 |
| IN-TRADE | 12/26 | counter | before | 128 | 73 |
| IN-TRADE | 12/26 | counter | after | 196 | 92 |
| IN-TRADE | 12/26 | with | before | 85 | 41 |
| IN-TRADE | 12/26 | with | after | 116 | 55 |
| IN-TRADE | 12/89 | counter | before | 58 | 42 |
| IN-TRADE | 12/89 | counter | after | 44 | 32 |
| IN-TRADE | 12/89 | with | before | 40 | 27 |
| IN-TRADE | 12/89 | with | after | 17 | 14 |
| AT-EXIT | 9/12 | counter | — | 25 | 25 |
| AT-EXIT | 9/12 | with | — | 0 | 0 |
| AT-EXIT | 12/26 | counter | — | 21 | 21 |
| AT-EXIT | 12/26 | with | — | 0 | 0 |
| AT-EXIT | 12/89 | counter | — | 19 | 19 |
| AT-EXIT | 12/89 | with | — | 0 | 0 |
| POST-EXIT | 9/12 | counter | — | 9 | 9 |
| POST-EXIT | 9/12 | with | — | 2 | 2 |
| POST-EXIT | 12/26 | counter | — | 17 | 17 |
| POST-EXIT | 12/26 | with | — | 1 | 1 |
| POST-EXIT | 12/89 | counter | — | 21 | 21 |
| POST-EXIT | 12/89 | with | — | 0 | 0 |

## P_WARN_1_COMPLEMENT (Tier-E arm; v6 vs the rule book)

| cell | n | sum_v6_r | sum_rule_r | mean_v6_r | mean_rule_r | mean_delta_r | sum_delta_r | sum_v6_haircut_r | sum_rule_haircut_r | n_v6_win | n_rule_win |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cohort_C1\|ALL | 42 | -22.0336 | -20.9179 | -0.5246 | -0.4980 | +0.0266 | +1.1157 | -22.5990 | -21.4825 | 6 | 0 |
| cohort_C1\|tuning | 24 | -13.5914 | -11.9266 | -0.5663 | -0.4969 | +0.0694 | +1.6648 | -13.8817 | -12.2172 | 3 | 0 |
| cohort_C1\|holdout | 18 | -8.4421 | -8.9913 | -0.4690 | -0.4995 | -0.0305 | -0.5492 | -8.7173 | -9.2653 | 3 | 0 |
| complement_C1\|ALL | 158 | +62.8411 | +62.8411 | +0.3977 | +0.3977 | +0.0000 | +0.0000 | +59.2965 | +59.2965 | 63 | 63 |
| complement_C1\|tuning | 99 | +12.2676 | +12.2676 | +0.1239 | +0.1239 | +0.0000 | +0.0000 | +10.1285 | +10.1285 | 38 | 38 |
| complement_C1\|holdout | 59 | +50.5735 | +50.5735 | +0.8572 | +0.8572 | +0.0000 | +0.0000 | +49.1680 | +49.1680 | 25 | 25 |
| acted\|ALL | 42 | -22.0336 | -20.9179 | -0.5246 | -0.4980 | +0.0266 | +1.1157 | -22.5990 | -21.4825 | 6 | 0 |
| acted\|tuning | 24 | -13.5914 | -11.9266 | -0.5663 | -0.4969 | +0.0694 | +1.6648 | -13.8817 | -12.2172 | 3 | 0 |
| acted\|holdout | 18 | -8.4421 | -8.9913 | -0.4690 | -0.4995 | -0.0305 | -0.5492 | -8.7173 | -9.2653 | 3 | 0 |
| unacted\|ALL | 158 | +62.8411 | +62.8411 | +0.3977 | +0.3977 | +0.0000 | +0.0000 | +59.2965 | +59.2965 | 63 | 63 |
| unacted\|tuning | 99 | +12.2676 | +12.2676 | +0.1239 | +0.1239 | +0.0000 | +0.0000 | +10.1285 | +10.1285 | 38 | 38 |
| unacted\|holdout | 59 | +50.5735 | +50.5735 | +0.8572 | +0.8572 | +0.0000 | +0.0000 | +49.1680 | +49.1680 | 25 | 25 |
| ALL\|ALL | 200 | +40.8076 | +41.9232 | +0.2040 | +0.2096 | +0.0056 | +1.1157 | +36.6975 | +37.8140 | 69 | 63 |
| ALL\|tuning | 123 | -1.3238 | +0.3410 | -0.0108 | +0.0028 | +0.0135 | +1.6648 | -3.7532 | -2.0887 | 41 | 38 |
| ALL\|holdout | 77 | +42.1314 | +41.5822 | +0.5472 | +0.5400 | -0.0071 | -0.5492 | +40.4507 | +39.9027 | 28 | 25 |

## W2 · post-entry cohorts vs their at-risk sets (Tier-E, whole)

- whole_book: the whole v6 book (a 'before +1R' cohort) [L-W.4]
- open_1h_after_entry: campaigns still open 1h after entry: 1h-resolved exit > entry close + 1h [L-W.4; sub-reading w6]
- reached_1r: campaigns that reached +1R (L-W.3 latch present) [L-W.4]

| cell | n | n_win | p_win | mean_net_r | sum_net_r | mean_minus_at_risk_mean |
|---|---|---|---|---|---|---|
| C1_counter_12_89_before_1r\|cohort\|ALL | 42 | 6 | 14.3% | -0.5246 | -22.0336 | -0.7286 |
| C1_counter_12_89_before_1r\|at_risk\|ALL | 200 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| C1_counter_12_89_before_1r\|complement\|ALL | 158 | 63 | 39.9% | +0.3977 | +62.8411 | +0.1937 |
| C1_counter_12_89_before_1r\|cohort\|tuning | 24 | 3 | 12.5% | -0.5663 | -13.5914 | -0.5555 |
| C1_counter_12_89_before_1r\|at_risk\|tuning | 123 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| C1_counter_12_89_before_1r\|complement\|tuning | 99 | 38 | 38.4% | +0.1239 | +12.2676 | +0.1347 |
| C1_counter_12_89_before_1r\|cohort\|holdout | 18 | 3 | 16.7% | -0.4690 | -8.4421 | -1.0162 |
| C1_counter_12_89_before_1r\|at_risk\|holdout | 77 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| C1_counter_12_89_before_1r\|complement\|holdout | 59 | 25 | 42.4% | +0.8572 | +50.5735 | +0.3100 |
| C2_counter_12_26_before_1r\|cohort\|ALL | 73 | 14 | 19.2% | -0.4214 | -30.7620 | -0.6254 |
| C2_counter_12_26_before_1r\|at_risk\|ALL | 200 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| C2_counter_12_26_before_1r\|complement\|ALL | 127 | 55 | 43.3% | +0.5635 | +71.5696 | +0.3595 |
| C2_counter_12_26_before_1r\|cohort\|tuning | 46 | 11 | 23.9% | -0.2935 | -13.4992 | -0.2827 |
| C2_counter_12_26_before_1r\|at_risk\|tuning | 123 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| C2_counter_12_26_before_1r\|complement\|tuning | 77 | 30 | 39.0% | +0.1581 | +12.1754 | +0.1689 |
| C2_counter_12_26_before_1r\|cohort\|holdout | 27 | 3 | 11.1% | -0.6394 | -17.2629 | -1.1865 |
| C2_counter_12_26_before_1r\|at_risk\|holdout | 77 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| C2_counter_12_26_before_1r\|complement\|holdout | 50 | 25 | 50.0% | +1.1879 | +59.3942 | +0.6407 |
| C3_with_9_12_recross_after_entry\|cohort\|ALL | 109 | 64 | 58.7% | +1.1120 | +121.2105 | +0.9016 |
| C3_with_9_12_recross_after_entry\|at_risk\|ALL | 199 | 69 | 34.7% | +0.2105 | +41.8803 | +0.0000 |
| C3_with_9_12_recross_after_entry\|complement\|ALL | 90 | 5 | 5.6% | -0.8814 | -79.3302 | -1.0919 |
| C3_with_9_12_recross_after_entry\|cohort\|tuning | 69 | 38 | 55.1% | +0.6907 | +47.6617 | +0.6928 |
| C3_with_9_12_recross_after_entry\|at_risk\|tuning | 122 | 41 | 33.6% | -0.0021 | -0.2511 | +0.0000 |
| C3_with_9_12_recross_after_entry\|complement\|tuning | 53 | 3 | 5.7% | -0.9040 | -47.9128 | -0.9020 |
| C3_with_9_12_recross_after_entry\|cohort\|holdout | 40 | 26 | 65.0% | +1.8387 | +73.5488 | +1.2916 |
| C3_with_9_12_recross_after_entry\|at_risk\|holdout | 77 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| C3_with_9_12_recross_after_entry\|complement\|holdout | 37 | 2 | 5.4% | -0.8491 | -31.4174 | -1.3963 |
| C4_counter_12_89_after_1r\|cohort\|ALL | 32 | 20 | 62.5% | +1.0026 | +32.0840 | -0.2864 |
| C4_counter_12_89_after_1r\|at_risk\|ALL | 103 | 69 | 67.0% | +1.2890 | +132.7662 | +0.0000 |
| C4_counter_12_89_after_1r\|complement\|ALL | 71 | 49 | 69.0% | +1.4181 | +100.6822 | +0.1291 |
| C4_counter_12_89_after_1r\|cohort\|tuning | 16 | 11 | 68.8% | +1.2895 | +20.6317 | +0.3865 |
| C4_counter_12_89_after_1r\|at_risk\|tuning | 62 | 41 | 66.1% | +0.9030 | +55.9870 | +0.0000 |
| C4_counter_12_89_after_1r\|complement\|tuning | 46 | 30 | 65.2% | +0.7686 | +35.3553 | -0.1344 |
| C4_counter_12_89_after_1r\|cohort\|holdout | 16 | 9 | 56.2% | +0.7158 | +11.4523 | -1.1569 |
| C4_counter_12_89_after_1r\|at_risk\|holdout | 41 | 28 | 68.3% | +1.8727 | +76.7792 | +0.0000 |
| C4_counter_12_89_after_1r\|complement\|holdout | 25 | 19 | 76.0% | +2.6131 | +65.3269 | +0.7404 |
| C3S_with_9_12_recross_strict\|cohort\|ALL | 109 | 64 | 58.7% | +1.1120 | +121.2105 | +0.9016 |
| C3S_with_9_12_recross_strict\|at_risk\|ALL | 199 | 69 | 34.7% | +0.2105 | +41.8803 | +0.0000 |
| C3S_with_9_12_recross_strict\|complement\|ALL | 90 | 5 | 5.6% | -0.8814 | -79.3302 | -1.0919 |
| C3S_with_9_12_recross_strict\|cohort\|tuning | 69 | 38 | 55.1% | +0.6907 | +47.6617 | +0.6928 |
| C3S_with_9_12_recross_strict\|at_risk\|tuning | 122 | 41 | 33.6% | -0.0021 | -0.2511 | +0.0000 |
| C3S_with_9_12_recross_strict\|complement\|tuning | 53 | 3 | 5.7% | -0.9040 | -47.9128 | -0.9020 |
| C3S_with_9_12_recross_strict\|cohort\|holdout | 40 | 26 | 65.0% | +1.8387 | +73.5488 | +1.2916 |
| C3S_with_9_12_recross_strict\|at_risk\|holdout | 77 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| C3S_with_9_12_recross_strict\|complement\|holdout | 37 | 2 | 5.4% | -0.8491 | -31.4174 | -1.3963 |

## W2 · the forward leg E[final net R − R marked at the event] (Tier-E, whole)

| cell | n | mean_final_net_r | mean_mark_r | mean_fwd_r | sum_fwd_r | n_fwd_pos | p_fwd_pos |
|---|---|---|---|---|---|---|---|
| C1_counter_12_89_before_1r\|ALL | 42 | -0.5246 | -0.4980 | -0.0266 | -1.1157 | 9 | 21.4% |
| C1_counter_12_89_before_1r\|tuning | 24 | -0.5663 | -0.4969 | -0.0694 | -1.6648 | 4 | 16.7% |
| C1_counter_12_89_before_1r\|holdout | 18 | -0.4690 | -0.4995 | +0.0305 | +0.5492 | 5 | 27.8% |
| C2_counter_12_26_before_1r\|ALL | 73 | -0.4214 | -0.3761 | -0.0453 | -3.3044 | 17 | 23.3% |
| C2_counter_12_26_before_1r\|tuning | 46 | -0.2935 | -0.3682 | +0.0747 | +3.4371 | 12 | 26.1% |
| C2_counter_12_26_before_1r\|holdout | 27 | -0.6394 | -0.3897 | -0.2497 | -6.7415 | 5 | 18.5% |
| C3_with_9_12_recross_after_entry\|ALL | 109 | +1.1120 | +0.6791 | +0.4329 | +47.1909 | 43 | 39.4% |
| C3_with_9_12_recross_after_entry\|tuning | 69 | +0.6907 | +0.6941 | -0.0034 | -0.2312 | 25 | 36.2% |
| C3_with_9_12_recross_after_entry\|holdout | 40 | +1.8387 | +0.6532 | +1.1856 | +47.4221 | 18 | 45.0% |
| C4_counter_12_89_after_1r\|ALL | 32 | +1.0026 | +1.1684 | -0.1658 | -5.3045 | 5 | 15.6% |
| C4_counter_12_89_after_1r\|tuning | 16 | +1.2895 | +1.3769 | -0.0874 | -1.3980 | 2 | 12.5% |
| C4_counter_12_89_after_1r\|holdout | 16 | +0.7158 | +0.9599 | -0.2442 | -3.9066 | 3 | 18.8% |
| C3S_with_9_12_recross_strict\|ALL | 109 | +1.1120 | +0.6880 | +0.4240 | +46.2180 | 43 | 39.4% |
| C3S_with_9_12_recross_strict\|tuning | 69 | +0.6907 | +0.6942 | -0.0035 | -0.2400 | 25 | 36.2% |
| C3S_with_9_12_recross_strict\|holdout | 40 | +1.8387 | +0.6773 | +1.1614 | +46.4580 | 18 | 45.0% |

## W2 · PRE-ENTRY classes in (arm close, entry close] vs the whole book (Tier-E, whole)

| cell | n | n_events | n_win | p_win | mean_net_r | sum_net_r | mean_minus_whole_book_mean |
|---|---|---|---|---|---|---|---|
| P1_counter_12_89\|cohort\|ALL | 66 | 133 | 16 | 24.2% | -0.1700 | -11.2213 | -0.3741 |
| P1_counter_12_89\|whole_book\|ALL | 200 | 133 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| P1_counter_12_89\|complement\|ALL | 134 | 0 | 53 | 39.6% | +0.3883 | +52.0289 | +0.1842 |
| P1_counter_12_89\|cohort\|tuning | 43 | 85 | 9 | 20.9% | -0.2318 | -9.9688 | -0.2211 |
| P1_counter_12_89\|whole_book\|tuning | 123 | 85 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| P1_counter_12_89\|complement\|tuning | 80 | 0 | 32 | 40.0% | +0.1081 | +8.6450 | +0.1188 |
| P1_counter_12_89\|cohort\|holdout | 23 | 48 | 7 | 30.4% | -0.0545 | -1.2525 | -0.6016 |
| P1_counter_12_89\|whole_book\|holdout | 77 | 48 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| P1_counter_12_89\|complement\|holdout | 54 | 0 | 21 | 38.9% | +0.8034 | +43.3839 | +0.2562 |
| P2_counter_12_26\|cohort\|ALL | 67 | 299 | 15 | 22.4% | -0.2007 | -13.4445 | -0.4047 |
| P2_counter_12_26\|whole_book\|ALL | 200 | 299 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| P2_counter_12_26\|complement\|ALL | 133 | 0 | 54 | 40.6% | +0.4079 | +54.2521 | +0.2039 |
| P2_counter_12_26\|cohort\|tuning | 44 | 202 | 9 | 20.5% | -0.2443 | -10.7497 | -0.2335 |
| P2_counter_12_26\|whole_book\|tuning | 123 | 202 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| P2_counter_12_26\|complement\|tuning | 79 | 0 | 32 | 40.5% | +0.1193 | +9.4259 | +0.1301 |
| P2_counter_12_26\|cohort\|holdout | 23 | 97 | 6 | 26.1% | -0.1172 | -2.6948 | -0.6643 |
| P2_counter_12_26\|whole_book\|holdout | 77 | 97 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| P2_counter_12_26\|complement\|holdout | 54 | 0 | 22 | 40.7% | +0.8301 | +44.8262 | +0.2830 |
| P3_with_9_12\|cohort\|ALL | 69 | 523 | 16 | 23.2% | -0.1903 | -13.1337 | -0.3944 |
| P3_with_9_12\|whole_book\|ALL | 200 | 523 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| P3_with_9_12\|complement\|ALL | 131 | 0 | 53 | 40.5% | +0.4118 | +53.9413 | +0.2077 |
| P3_with_9_12\|cohort\|tuning | 46 | 362 | 10 | 21.7% | -0.2269 | -10.4389 | -0.2162 |
| P3_with_9_12\|whole_book\|tuning | 123 | 362 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| P3_with_9_12\|complement\|tuning | 77 | 0 | 31 | 40.3% | +0.1184 | +9.1151 | +0.1291 |
| P3_with_9_12\|cohort\|holdout | 23 | 161 | 6 | 26.1% | -0.1172 | -2.6948 | -0.6643 |
| P3_with_9_12\|whole_book\|holdout | 77 | 161 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| P3_with_9_12\|complement\|holdout | 54 | 0 | 22 | 40.7% | +0.8301 | +44.8262 | +0.2830 |
| P4_with_12_26\|cohort\|ALL | 66 | 293 | 15 | 22.7% | -0.1826 | -12.0514 | -0.3866 |
| P4_with_12_26\|whole_book\|ALL | 200 | 293 | 69 | 34.5% | +0.2040 | +40.8076 | +0.0000 |
| P4_with_12_26\|complement\|ALL | 134 | 0 | 54 | 40.3% | +0.3945 | +52.8590 | +0.1904 |
| P4_with_12_26\|cohort\|tuning | 42 | 197 | 9 | 21.4% | -0.2038 | -8.5584 | -0.1930 |
| P4_with_12_26\|whole_book\|tuning | 123 | 197 | 41 | 33.3% | -0.0108 | -1.3238 | +0.0000 |
| P4_with_12_26\|complement\|tuning | 81 | 0 | 32 | 39.5% | +0.0893 | +7.2346 | +0.1001 |
| P4_with_12_26\|cohort\|holdout | 24 | 96 | 6 | 25.0% | -0.1455 | -3.4930 | -0.6927 |
| P4_with_12_26\|whole_book\|holdout | 77 | 96 | 28 | 36.4% | +0.5472 | +42.1314 | +0.0000 |
| P4_with_12_26\|complement\|holdout | 53 | 0 | 22 | 41.5% | +0.8608 | +45.6244 | +0.3137 |

## W2 · relay evidence [L-W.6] (Tier-E, whole)

| cell | n_windows | n_lag0 | n_relay_cross | share_relay_cross | lead_1h_min | lead_1h_q25 | lead_1h_median | lead_1h_q75 | lead_1h_max | lead_1h_mean | lead_4h_min | lead_4h_q25 | lead_4h_median | lead_4h_q75 | lead_4h_max | lead_4h_mean |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v6_campaigns\|ALL\|ALL | 200 | 52 | 66 | 33.0% | 3.00 | 41.25 | 143.50 | 269.75 | 661.00 | 179.65 | 0.00 | 10.25 | 35.50 | 67.25 | 165.00 | 44.53 |
| v6_campaigns\|ALL\|0 | 52 | 52 | 0 | 0.0% | — | — | — | — | — | — | — | — | — | — | — | — |
| v6_campaigns\|ALL\|1-6 | 81 | 0 | 1 | 1.2% | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| v6_campaigns\|ALL\|7-15 | 4 | 0 | 4 | 100.0% | 6.00 | 9.00 | 12.00 | 14.00 | 14.00 | 11.00 | 1.00 | 1.75 | 2.50 | 3.00 | 3.00 | 2.25 |
| v6_campaigns\|ALL\|>=16 | 63 | 0 | 61 | 96.8% | 3.00 | 63.00 | 161.00 | 285.00 | 661.00 | 193.49 | 0.00 | 15.00 | 40.00 | 71.00 | 165.00 | 48.00 |
| v6_campaigns\|tuning\|ALL | 123 | 27 | 42 | 34.1% | 3.00 | 45.50 | 158.50 | 267.25 | 661.00 | 185.67 | 0.00 | 11.00 | 39.50 | 66.50 | 165.00 | 46.02 |
| v6_campaigns\|tuning\|0 | 27 | 27 | 0 | 0.0% | — | — | — | — | — | — | — | — | — | — | — | — |
| v6_campaigns\|tuning\|1-6 | 52 | 0 | 0 | 0.0% | — | — | — | — | — | — | — | — | — | — | — | — |
| v6_campaigns\|tuning\|7-15 | 2 | 0 | 2 | 100.0% | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 14.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 | 3.00 |
| v6_campaigns\|tuning\|>=16 | 42 | 0 | 40 | 95.2% | 3.00 | 56.00 | 161.50 | 276.00 | 661.00 | 194.25 | 0.00 | 13.25 | 40.00 | 68.75 | 165.00 | 48.17 |
| v6_campaigns\|holdout\|ALL | 77 | 25 | 24 | 31.2% | 5.00 | 35.25 | 112.00 | 268.00 | 658.00 | 169.12 | 1.00 | 8.75 | 27.50 | 67.00 | 164.00 | 41.92 |
| v6_campaigns\|holdout\|0 | 25 | 25 | 0 | 0.0% | — | — | — | — | — | — | — | — | — | — | — | — |
| v6_campaigns\|holdout\|1-6 | 29 | 0 | 1 | 3.4% | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 10.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 | 2.00 |
| v6_campaigns\|holdout\|7-15 | 2 | 0 | 2 | 100.0% | 6.00 | 7.00 | 8.00 | 9.00 | 10.00 | 8.00 | 1.00 | 1.25 | 1.50 | 1.75 | 2.00 | 1.50 |
| v6_campaigns\|holdout\|>=16 | 21 | 0 | 21 | 100.0% | 5.00 | 72.00 | 159.00 | 292.00 | 658.00 | 192.05 | 1.00 | 18.00 | 39.00 | 73.00 | 164.00 | 47.67 |
| armed_windows_not_entered\|ALL\|ALL | 150 | 0 | 81 | 54.0% | 5.00 | 42.00 | 103.00 | 189.00 | 815.00 | 153.94 | 1.00 | 10.00 | 25.00 | 47.00 | 203.00 | 38.07 |
| armed_windows_not_entered\|tuning\|ALL | 96 | 0 | 52 | 54.2% | 15.00 | 42.00 | 100.00 | 186.50 | 815.00 | 155.88 | 3.00 | 10.00 | 24.50 | 46.25 | 203.00 | 38.58 |
| armed_windows_not_entered\|holdout\|ALL | 54 | 0 | 29 | 53.7% | 5.00 | 43.00 | 103.00 | 189.00 | 642.00 | 150.45 | 1.00 | 10.00 | 25.00 | 47.00 | 160.00 | 37.17 |

Lead distributions, binned (whole):

| cell | n |
|---|---|
| v6_campaigns\|lead_1h\|1 | 0 |
| v6_campaigns\|lead_1h\|2-3 | 1 |
| v6_campaigns\|lead_1h\|4-7 | 2 |
| v6_campaigns\|lead_1h\|8-15 | 6 |
| v6_campaigns\|lead_1h\|16-31 | 7 |
| v6_campaigns\|lead_1h\|32-63 | 5 |
| v6_campaigns\|lead_1h\|64-127 | 10 |
| v6_campaigns\|lead_1h\|128-255 | 17 |
| v6_campaigns\|lead_1h\|>=256 | 18 |
| v6_campaigns\|lead_1h\|none | 134 |
| v6_campaigns\|lead_4h\|0 | 1 |
| v6_campaigns\|lead_4h\|1 | 2 |
| v6_campaigns\|lead_4h\|2-3 | 6 |
| v6_campaigns\|lead_4h\|4-7 | 7 |
| v6_campaigns\|lead_4h\|8-15 | 5 |
| v6_campaigns\|lead_4h\|16-31 | 10 |
| v6_campaigns\|lead_4h\|32-63 | 17 |
| v6_campaigns\|lead_4h\|>=64 | 18 |
| v6_campaigns\|lead_4h\|none | 134 |
| armed_windows_not_entered\|lead_1h\|1 | 0 |
| armed_windows_not_entered\|lead_1h\|2-3 | 0 |
| armed_windows_not_entered\|lead_1h\|4-7 | 1 |
| armed_windows_not_entered\|lead_1h\|8-15 | 3 |
| armed_windows_not_entered\|lead_1h\|16-31 | 10 |
| armed_windows_not_entered\|lead_1h\|32-63 | 17 |
| armed_windows_not_entered\|lead_1h\|64-127 | 19 |
| armed_windows_not_entered\|lead_1h\|128-255 | 16 |
| armed_windows_not_entered\|lead_1h\|>=256 | 15 |
| armed_windows_not_entered\|lead_1h\|none | 69 |
| armed_windows_not_entered\|lead_4h\|0 | 0 |
| armed_windows_not_entered\|lead_4h\|1 | 1 |
| armed_windows_not_entered\|lead_4h\|2-3 | 3 |
| armed_windows_not_entered\|lead_4h\|4-7 | 10 |
| armed_windows_not_entered\|lead_4h\|8-15 | 17 |
| armed_windows_not_entered\|lead_4h\|16-31 | 19 |
| armed_windows_not_entered\|lead_4h\|32-63 | 16 |
| armed_windows_not_entered\|lead_4h\|>=64 | 15 |
| armed_windows_not_entered\|lead_4h\|none | 69 |

Per v6 window (the whole distribution):

| symbol | entry | direction | era | lag | relay_cross | relay | relay_on_mismatch_bar | relay_lead_1h | relay_lead_4h |
|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2020-01-27T00:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| BTCUSDT | 2020-02-19T08:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| BTCUSDT | 2020-04-01T16:00:00Z | -1 | tuning | 26 | True | 2020-04-01T02:00:00Z | False | 18 | 4 |
| BTCUSDT | 2020-06-07T20:00:00Z | 1 | tuning | 62 | True | 2020-05-30T05:00:00Z | False | 211 | 52 |
| BTCUSDT | 2020-07-10T20:00:00Z | 1 | tuning | 23 | False | — | — | — | — |
| BTCUSDT | 2020-08-14T04:00:00Z | 1 | tuning | 143 | True | 2020-07-30T20:00:00Z | False | 348 | 87 |
| BTCUSDT | 2020-11-29T16:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| BTCUSDT | 2021-01-14T08:00:00Z | 1 | tuning | 193 | True | 2020-12-22T15:00:00Z | False | 549 | 137 |
| BTCUSDT | 2021-04-05T20:00:00Z | 1 | tuning | 50 | True | 2021-03-29T09:00:00Z | False | 183 | 45 |
| BTCUSDT | 2021-05-05T20:00:00Z | 1 | tuning | 2 | False | — | — | — | — |
| BTCUSDT | 2021-06-25T08:00:00Z | -1 | tuning | 40 | True | 2021-06-21T04:00:00Z | False | 104 | 26 |
| BTCUSDT | 2021-07-01T12:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| BTCUSDT | 2021-07-05T16:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| BTCUSDT | 2021-10-29T16:00:00Z | 1 | tuning | 6 | False | — | — | — | — |
| BTCUSDT | 2021-11-07T16:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| BTCUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 117 | True | 2021-12-31T00:00:00Z | False | 420 | 105 |
| BTCUSDT | 2022-02-28T00:00:00Z | -1 | tuning | 59 | True | 2022-02-21T11:00:00Z | False | 161 | 40 |
| BTCUSDT | 2022-09-28T08:00:00Z | -1 | tuning | 4 | False | — | — | — | — |
| BTCUSDT | 2022-10-15T04:00:00Z | -1 | tuning | 38 | True | 2022-10-09T23:00:00Z | False | 129 | 32 |
| BTCUSDT | 2022-12-25T12:00:00Z | -1 | tuning | 51 | True | 2022-12-19T04:00:00Z | False | 156 | 39 |
| BTCUSDT | 2023-05-04T04:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| BTCUSDT | 2023-08-14T12:00:00Z | 1 | tuning | 35 | True | 2023-08-12T17:00:00Z | False | 47 | 11 |
| BTCUSDT | 2023-09-01T04:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| BTCUSDT | 2023-11-15T20:00:00Z | 1 | tuning | 183 | True | 2023-10-19T11:00:00Z | False | 661 | 165 |
| BTCUSDT | 2023-12-19T04:00:00Z | 1 | tuning | 2 | False | — | — | — | — |
| BTCUSDT | 2024-01-04T12:00:00Z | 1 | tuning | 16 | False | — | — | — | — |
| BTCUSDT | 2024-10-24T20:00:00Z | 1 | holdout | 74 | True | 2024-10-14T04:00:00Z | False | 260 | 65 |
| BTCUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 3 | False | — | — | — | — |
| BTCUSDT | 2025-01-23T12:00:00Z | 1 | holdout | 50 | True | 2025-01-20T08:00:00Z | False | 80 | 20 |
| BTCUSDT | 2025-02-22T16:00:00Z | -1 | holdout | 5 | False | — | — | — | — |
| BTCUSDT | 2025-04-03T08:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| BTCUSDT | 2025-07-02T12:00:00Z | 1 | holdout | 44 | True | 2025-06-27T05:00:00Z | False | 131 | 32 |
| BTCUSDT | 2025-12-06T00:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| BTCUSDT | 2025-12-29T20:00:00Z | -1 | holdout | 3 | True | 2025-12-29T14:00:00Z | False | 10 | 2 |
| BTCUSDT | 2026-01-01T04:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| BTCUSDT | 2026-03-24T16:00:00Z | -1 | holdout | 25 | True | 2026-03-21T20:00:00Z | False | 72 | 18 |
| BTCUSDT | 2026-03-26T12:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| BTCUSDT | 2026-06-18T04:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| BTCUSDT | 2026-09-14T16:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2020-05-27T20:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2020-07-12T20:00:00Z | 1 | tuning | 38 | True | 2020-07-11T03:00:00Z | False | 45 | 11 |
| ETHUSDT | 2020-08-08T08:00:00Z | 1 | tuning | 115 | True | 2020-07-21T07:00:00Z | False | 437 | 109 |
| ETHUSDT | 2020-10-02T04:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ETHUSDT | 2020-11-02T00:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2020-11-04T20:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2020-12-13T08:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2021-03-18T12:00:00Z | 1 | tuning | 68 | True | 2021-03-11T22:00:00Z | False | 162 | 40 |
| ETHUSDT | 2021-04-08T20:00:00Z | 1 | tuning | 62 | True | 2021-03-31T16:00:00Z | False | 200 | 50 |
| ETHUSDT | 2021-04-21T12:00:00Z | 1 | tuning | 5 | False | — | — | — | — |
| ETHUSDT | 2021-06-08T00:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2021-08-28T04:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| ETHUSDT | 2021-12-28T04:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2022-02-28T08:00:00Z | -1 | tuning | 60 | True | 2022-02-21T13:00:00Z | False | 167 | 41 |
| ETHUSDT | 2022-03-10T12:00:00Z | -1 | tuning | 36 | True | 2022-03-10T05:00:00Z | False | 11 | 2 |
| ETHUSDT | 2022-09-07T04:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| ETHUSDT | 2022-10-08T04:00:00Z | -1 | tuning | 4 | False | — | — | — | — |
| ETHUSDT | 2022-12-22T16:00:00Z | -1 | tuning | 37 | True | 2022-12-19T05:00:00Z | False | 87 | 21 |
| ETHUSDT | 2023-05-24T16:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| ETHUSDT | 2023-07-13T12:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2023-09-01T04:00:00Z | -1 | tuning | 3 | False | — | — | — | — |
| ETHUSDT | 2023-10-19T00:00:00Z | -1 | tuning | 81 | True | 2023-10-07T19:00:00Z | False | 273 | 68 |
| ETHUSDT | 2023-11-20T08:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| ETHUSDT | 2023-12-14T16:00:00Z | 1 | tuning | 6 | False | — | — | — | — |
| ETHUSDT | 2023-12-27T12:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| ETHUSDT | 2024-03-31T04:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2024-04-25T08:00:00Z | -1 | tuning | 4 | False | — | — | — | — |
| ETHUSDT | 2024-04-30T08:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ETHUSDT | 2024-05-07T12:00:00Z | -1 | tuning | 5 | False | — | — | — | — |
| ETHUSDT | 2024-09-16T00:00:00Z | -1 | holdout | 2 | False | — | — | — | — |
| ETHUSDT | 2024-10-08T08:00:00Z | -1 | holdout | 39 | True | 2024-10-05T21:00:00Z | False | 63 | 15 |
| ETHUSDT | 2025-01-26T20:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2025-02-02T00:00:00Z | -1 | holdout | 2 | False | — | — | — | — |
| ETHUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2025-06-03T08:00:00Z | 1 | holdout | 2 | False | — | — | — | — |
| ETHUSDT | 2025-06-09T20:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2025-06-16T16:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2025-08-05T00:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2025-08-22T12:00:00Z | 1 | holdout | 11 | True | 2025-08-22T06:00:00Z | False | 10 | 2 |
| ETHUSDT | 2025-09-18T00:00:00Z | 1 | holdout | 40 | True | 2025-09-17T07:00:00Z | False | 21 | 5 |
| ETHUSDT | 2025-10-08T20:00:00Z | 1 | holdout | 42 | True | 2025-10-05T03:00:00Z | False | 93 | 23 |
| ETHUSDT | 2025-10-29T16:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2026-02-28T04:00:00Z | -1 | holdout | 4 | False | — | — | — | — |
| ETHUSDT | 2026-04-03T08:00:00Z | -1 | holdout | 6 | False | — | — | — | — |
| ETHUSDT | 2026-06-18T16:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| ETHUSDT | 2026-08-05T16:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ETHUSDT | 2026-08-30T12:00:00Z | 1 | holdout | 79 | True | 2026-08-18T12:00:00Z | False | 292 | 73 |
| ETHUSDT | 2026-09-18T08:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| SOLUSDT | 2020-12-04T16:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2021-03-07T20:00:00Z | 1 | tuning | 3 | False | — | — | — | — |
| SOLUSDT | 2021-03-27T04:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2021-05-12T08:00:00Z | 1 | tuning | 3 | False | — | — | — | — |
| SOLUSDT | 2021-05-16T00:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2021-07-29T00:00:00Z | -1 | tuning | 8 | True | 2021-07-28T14:00:00Z | False | 14 | 3 |
| SOLUSDT | 2021-09-19T00:00:00Z | 1 | tuning | 2 | False | — | — | — | — |
| SOLUSDT | 2021-10-08T16:00:00Z | 1 | tuning | 43 | True | 2021-10-07T14:00:00Z | False | 30 | 7 |
| SOLUSDT | 2021-10-20T08:00:00Z | 1 | tuning | 30 | True | 2021-10-17T04:00:00Z | False | 80 | 20 |
| SOLUSDT | 2022-01-17T08:00:00Z | -1 | tuning | 115 | True | 2021-12-31T19:00:00Z | False | 401 | 100 |
| SOLUSDT | 2022-02-17T12:00:00Z | -1 | tuning | 38 | True | 2022-02-16T15:00:00Z | False | 25 | 6 |
| SOLUSDT | 2022-09-23T08:00:00Z | -1 | tuning | 47 | True | 2022-09-18T17:00:00Z | False | 115 | 28 |
| SOLUSDT | 2022-10-18T20:00:00Z | -1 | tuning | 65 | True | 2022-10-10T09:00:00Z | False | 207 | 51 |
| SOLUSDT | 2022-11-28T08:00:00Z | -1 | tuning | 122 | True | 2022-11-11T20:00:00Z | False | 400 | 100 |
| SOLUSDT | 2022-12-16T16:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| SOLUSDT | 2023-04-02T20:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| SOLUSDT | 2023-07-27T04:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2023-10-16T04:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2024-02-02T00:00:00Z | 1 | tuning | 30 | True | 2024-02-02T01:00:00Z | False | 3 | 0 |
| SOLUSDT | 2024-02-08T00:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| SOLUSDT | 2024-03-21T04:00:00Z | 1 | tuning | 139 | True | 2024-02-28T08:00:00Z | False | 528 | 132 |
| SOLUSDT | 2024-04-25T08:00:00Z | -1 | tuning | 3 | False | — | — | — | — |
| SOLUSDT | 2024-06-04T16:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| SOLUSDT | 2024-07-07T16:00:00Z | -1 | holdout | 21 | True | 2024-07-07T15:00:00Z | False | 5 | 1 |
| SOLUSDT | 2024-07-11T20:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| SOLUSDT | 2024-09-16T00:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| SOLUSDT | 2024-11-06T00:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| SOLUSDT | 2025-08-17T04:00:00Z | 1 | holdout | 53 | True | 2025-08-10T17:00:00Z | False | 159 | 39 |
| SOLUSDT | 2025-08-22T16:00:00Z | 1 | holdout | 1 | False | — | — | — | — |
| SOLUSDT | 2025-11-11T20:00:00Z | -1 | holdout | 74 | True | 2025-11-02T13:00:00Z | False | 227 | 56 |
| SOLUSDT | 2025-12-05T20:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| SOLUSDT | 2025-12-11T04:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| SOLUSDT | 2026-02-28T04:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| SOLUSDT | 2026-04-07T00:00:00Z | -1 | holdout | 68 | True | 2026-03-31T00:00:00Z | False | 172 | 43 |
| SOLUSDT | 2026-04-12T16:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| SOLUSDT | 2026-09-18T00:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| NEARUSDT | 2020-12-27T16:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2021-02-25T16:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2021-04-04T20:00:00Z | 1 | tuning | 39 | True | 2021-04-02T13:00:00Z | False | 59 | 14 |
| NEARUSDT | 2021-05-04T12:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2021-06-18T00:00:00Z | -1 | tuning | 10 | True | 2021-06-17T14:00:00Z | False | 14 | 3 |
| NEARUSDT | 2021-07-08T16:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| NEARUSDT | 2021-10-06T12:00:00Z | 1 | tuning | 24 | True | 2021-10-05T09:00:00Z | False | 31 | 7 |
| NEARUSDT | 2021-11-08T20:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| NEARUSDT | 2022-01-11T00:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2022-02-17T16:00:00Z | -1 | tuning | 41 | True | 2022-02-16T16:00:00Z | False | 28 | 7 |
| NEARUSDT | 2022-04-19T04:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| NEARUSDT | 2022-06-28T04:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2022-09-07T00:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| NEARUSDT | 2022-12-07T20:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| NEARUSDT | 2023-02-02T16:00:00Z | 1 | tuning | 4 | False | — | — | — | — |
| NEARUSDT | 2023-02-08T04:00:00Z | 1 | tuning | 2 | False | — | — | — | — |
| NEARUSDT | 2023-03-31T08:00:00Z | -1 | tuning | 61 | True | 2023-03-22T09:00:00Z | False | 219 | 54 |
| NEARUSDT | 2023-04-03T00:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| NEARUSDT | 2023-06-05T12:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| NEARUSDT | 2023-07-31T16:00:00Z | -1 | tuning | 44 | True | 2023-07-30T20:00:00Z | False | 24 | 6 |
| NEARUSDT | 2023-10-17T16:00:00Z | -1 | tuning | 83 | True | 2023-10-05T15:00:00Z | False | 293 | 73 |
| NEARUSDT | 2024-03-25T00:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| NEARUSDT | 2024-05-13T20:00:00Z | 1 | tuning | 58 | True | 2024-05-09T13:00:00Z | False | 107 | 26 |
| NEARUSDT | 2024-07-03T20:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| NEARUSDT | 2024-08-12T04:00:00Z | -1 | holdout | 107 | True | 2024-07-28T01:00:00Z | False | 367 | 91 |
| NEARUSDT | 2024-10-20T20:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| NEARUSDT | 2025-01-20T00:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| NEARUSDT | 2025-02-24T12:00:00Z | -1 | holdout | 6 | False | — | — | — | — |
| NEARUSDT | 2025-03-04T00:00:00Z | -1 | holdout | 2 | False | — | — | — | — |
| NEARUSDT | 2025-04-15T12:00:00Z | -1 | holdout | 104 | True | 2025-03-30T17:00:00Z | False | 383 | 95 |
| NEARUSDT | 2025-05-21T20:00:00Z | 1 | holdout | 2 | False | — | — | — | — |
| NEARUSDT | 2025-05-29T00:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| NEARUSDT | 2025-06-12T20:00:00Z | -1 | holdout | 2 | False | — | — | — | — |
| NEARUSDT | 2025-08-12T16:00:00Z | 1 | holdout | 26 | True | 2025-08-11T04:00:00Z | False | 40 | 10 |
| NEARUSDT | 2025-10-08T20:00:00Z | 1 | holdout | 39 | True | 2025-10-05T03:00:00Z | False | 93 | 23 |
| NEARUSDT | 2025-12-05T08:00:00Z | -1 | holdout | 113 | True | 2025-11-19T06:00:00Z | False | 390 | 97 |
| NEARUSDT | 2025-12-30T20:00:00Z | -1 | holdout | 7 | True | 2025-12-30T18:00:00Z | False | 6 | 1 |
| NEARUSDT | 2026-02-18T20:00:00Z | -1 | holdout | 186 | True | 2026-01-22T14:00:00Z | False | 658 | 164 |
| NEARUSDT | 2026-05-18T20:00:00Z | 1 | holdout | 74 | True | 2026-05-10T10:00:00Z | False | 206 | 51 |
| NEARUSDT | 2026-07-22T00:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ZECUSDT | 2020-06-22T12:00:00Z | 1 | tuning | 1 | False | — | — | — | — |
| ZECUSDT | 2020-07-21T08:00:00Z | 1 | tuning | 88 | True | 2020-07-11T02:00:00Z | False | 250 | 62 |
| ZECUSDT | 2020-12-07T12:00:00Z | 1 | tuning | 3 | False | — | — | — | — |
| ZECUSDT | 2020-12-29T16:00:00Z | -1 | tuning | 3 | False | — | — | — | — |
| ZECUSDT | 2021-03-18T00:00:00Z | 1 | tuning | 54 | True | 2021-03-13T14:00:00Z | False | 110 | 27 |
| ZECUSDT | 2021-04-09T00:00:00Z | 1 | tuning | 65 | True | 2021-03-31T14:00:00Z | False | 206 | 51 |
| ZECUSDT | 2021-05-12T00:00:00Z | 1 | tuning | 87 | True | 2021-04-30T07:00:00Z | False | 285 | 71 |
| ZECUSDT | 2021-07-02T16:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ZECUSDT | 2021-12-28T08:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| ZECUSDT | 2022-04-26T00:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ZECUSDT | 2022-07-11T08:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ZECUSDT | 2022-09-06T20:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| ZECUSDT | 2022-09-13T12:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ZECUSDT | 2022-09-28T08:00:00Z | -1 | tuning | 1 | False | — | — | — | — |
| ZECUSDT | 2022-10-07T00:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ZECUSDT | 2022-11-07T00:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ZECUSDT | 2022-11-27T20:00:00Z | -1 | tuning | 0 | False | — | — | — | — |
| ZECUSDT | 2023-02-02T00:00:00Z | 1 | tuning | 0 | False | — | — | — | — |
| ZECUSDT | 2023-08-15T08:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ZECUSDT | 2023-09-10T12:00:00Z | -1 | tuning | 2 | False | — | — | — | — |
| ZECUSDT | 2024-04-25T08:00:00Z | -1 | tuning | 4 | False | — | — | — | — |
| ZECUSDT | 2024-06-05T04:00:00Z | 1 | tuning | 3 | False | — | — | — | — |
| ZECUSDT | 2024-09-29T00:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| ZECUSDT | 2024-10-28T08:00:00Z | 1 | holdout | 2 | False | — | — | — | — |
| ZECUSDT | 2024-11-21T12:00:00Z | 1 | holdout | 28 | True | 2024-11-21T07:00:00Z | False | 9 | 2 |
| ZECUSDT | 2025-01-19T04:00:00Z | -1 | holdout | 3 | False | — | — | — | — |
| ZECUSDT | 2025-04-13T20:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ZECUSDT | 2025-06-09T20:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ZECUSDT | 2025-08-12T00:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| ZECUSDT | 2025-08-14T20:00:00Z | -1 | holdout | 0 | False | — | — | — | — |
| ZECUSDT | 2025-09-02T16:00:00Z | 1 | holdout | 2 | False | — | — | — | — |
| ZECUSDT | 2025-12-24T20:00:00Z | 1 | holdout | 1 | False | — | — | — | — |
| ZECUSDT | 2026-03-06T12:00:00Z | -1 | holdout | 91 | True | 2026-02-21T16:00:00Z | False | 312 | 78 |
| ZECUSDT | 2026-03-26T08:00:00Z | -1 | holdout | 1 | False | — | — | — | — |
| ZECUSDT | 2026-04-23T16:00:00Z | 1 | holdout | 0 | False | — | — | — | — |
| ZECUSDT | 2026-05-01T04:00:00Z | 1 | holdout | 3 | False | — | — | — | — |
| ZECUSDT | 2026-08-17T04:00:00Z | 1 | holdout | 0 | False | — | — | — | — |

Twin population (w7) — armed windows of v6's card holding no v6 campaign: triggered gate-passing windows 200 vs v6 campaign windows 200 (identical sets: True; triggered, not entered: none); twin windows by end kind {'as_of': 1, 'window_close': 149}. Per twin window (the whole distribution):

| symbol | arm | direction | end | end_kind | window_bars | era | relay_cross | relay | relay_lead_1h | relay_lead_4h |
|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 2019-12-27T08:00:00Z | -1 | 2019-12-28T04:00:00Z | window_close | 4 | tuning | False | — | — | — |
| BTCUSDT | 2019-12-31T20:00:00Z | -1 | 2020-01-04T04:00:00Z | window_close | 19 | tuning | True | 2020-01-02T00:00:00Z | 52 | 13 |
| BTCUSDT | 2020-02-23T20:00:00Z | 1 | 2020-02-24T04:00:00Z | window_close | 1 | tuning | False | — | — | — |
| BTCUSDT | 2020-04-21T12:00:00Z | -1 | 2020-04-22T16:00:00Z | window_close | 6 | tuning | False | — | — | — |
| BTCUSDT | 2020-06-22T20:00:00Z | 1 | 2020-06-25T00:00:00Z | window_close | 12 | tuning | False | — | — | — |
| BTCUSDT | 2020-08-24T08:00:00Z | 1 | 2020-08-25T12:00:00Z | window_close | 6 | tuning | False | — | — | — |
| BTCUSDT | 2020-08-30T20:00:00Z | 1 | 2020-09-03T00:00:00Z | window_close | 18 | tuning | True | 2020-09-01T04:00:00Z | 44 | 11 |
| BTCUSDT | 2020-09-21T16:00:00Z | -1 | 2020-09-26T20:00:00Z | window_close | 30 | tuning | False | — | — | — |
| BTCUSDT | 2020-10-02T04:00:00Z | -1 | 2020-10-06T00:00:00Z | window_close | 22 | tuning | False | — | — | — |
| BTCUSDT | 2021-01-29T12:00:00Z | 1 | 2021-02-26T04:00:00Z | window_close | 165 | tuning | True | 2021-01-30T22:00:00Z | 630 | 157 |
| BTCUSDT | 2021-03-03T08:00:00Z | 1 | 2021-03-05T12:00:00Z | window_close | 12 | tuning | False | — | — | — |
| BTCUSDT | 2021-04-30T16:00:00Z | 1 | 2021-05-05T04:00:00Z | window_close | 26 | tuning | True | 2021-05-03T02:00:00Z | 50 | 12 |
| BTCUSDT | 2021-09-15T20:00:00Z | 1 | 2021-09-20T08:00:00Z | window_close | 26 | tuning | True | 2021-09-17T04:00:00Z | 76 | 19 |
| BTCUSDT | 2022-03-05T04:00:00Z | -1 | 2022-03-09T16:00:00Z | window_close | 26 | tuning | True | 2022-03-07T19:00:00Z | 45 | 11 |
| BTCUSDT | 2022-06-03T12:00:00Z | -1 | 2022-06-06T08:00:00Z | window_close | 16 | tuning | True | 2022-06-05T02:00:00Z | 30 | 7 |
| BTCUSDT | 2022-07-11T20:00:00Z | -1 | 2022-07-15T20:00:00Z | window_close | 23 | tuning | False | — | — | — |
| BTCUSDT | 2022-07-26T04:00:00Z | -1 | 2022-07-28T04:00:00Z | window_close | 11 | tuning | False | — | — | — |
| BTCUSDT | 2022-09-14T16:00:00Z | -1 | 2022-09-27T16:00:00Z | window_close | 77 | tuning | True | 2022-09-18T15:00:00Z | 217 | 54 |
| BTCUSDT | 2023-02-15T20:00:00Z | 1 | 2023-02-25T04:00:00Z | window_close | 55 | tuning | True | 2023-02-17T19:00:00Z | 177 | 44 |
| BTCUSDT | 2023-06-01T08:00:00Z | -1 | 2023-06-04T20:00:00Z | window_close | 20 | tuning | True | 2023-06-03T22:00:00Z | 22 | 5 |
| BTCUSDT | 2023-09-24T20:00:00Z | -1 | 2023-09-28T16:00:00Z | window_close | 22 | tuning | True | 2023-09-26T10:00:00Z | 54 | 13 |
| BTCUSDT | 2024-03-25T12:00:00Z | 1 | 2024-04-02T12:00:00Z | window_close | 47 | tuning | True | 2024-03-28T08:00:00Z | 124 | 31 |
| BTCUSDT | 2024-04-06T20:00:00Z | 1 | 2024-04-13T08:00:00Z | window_close | 38 | tuning | True | 2024-04-10T22:00:00Z | 58 | 14 |
| BTCUSDT | 2024-04-22T20:00:00Z | 1 | 2024-04-25T00:00:00Z | window_close | 12 | tuning | False | — | — | — |
| BTCUSDT | 2024-08-28T08:00:00Z | -1 | 2024-09-12T12:00:00Z | window_close | 90 | holdout | True | 2024-08-29T23:00:00Z | 325 | 81 |
| BTCUSDT | 2024-10-07T04:00:00Z | 1 | 2024-10-09T00:00:00Z | window_close | 10 | holdout | False | — | — | — |
| BTCUSDT | 2025-01-03T12:00:00Z | 1 | 2025-01-08T20:00:00Z | window_close | 31 | holdout | True | 2025-01-05T21:00:00Z | 71 | 17 |
| BTCUSDT | 2025-03-28T20:00:00Z | -1 | 2025-04-02T20:00:00Z | window_close | 29 | holdout | False | — | — | — |
| BTCUSDT | 2025-06-08T16:00:00Z | 1 | 2025-06-13T16:00:00Z | window_close | 29 | holdout | True | 2025-06-09T09:00:00Z | 103 | 25 |
| BTCUSDT | 2025-06-16T16:00:00Z | 1 | 2025-06-17T16:00:00Z | window_close | 5 | holdout | False | — | — | — |
| BTCUSDT | 2025-08-07T20:00:00Z | 1 | 2025-08-18T00:00:00Z | window_close | 60 | holdout | True | 2025-08-10T03:00:00Z | 189 | 47 |
| BTCUSDT | 2026-03-07T20:00:00Z | -1 | 2026-03-10T08:00:00Z | window_close | 14 | holdout | False | — | — | — |
| BTCUSDT | 2026-07-28T00:00:00Z | -1 | 2026-07-31T00:00:00Z | window_close | 17 | holdout | True | 2026-07-29T21:00:00Z | 27 | 6 |
| BTCUSDT | 2026-08-11T12:00:00Z | -1 | 2026-08-18T08:00:00Z | window_close | 40 | holdout | True | 2026-08-12T15:00:00Z | 137 | 34 |
| BTCUSDT | 2026-09-18T12:00:00Z | 1 | 2026-09-25T00:00:00Z | as_of | 38 | holdout | True | 2026-09-20T18:00:00Z | 102 | 25 |
| ETHUSDT | 2020-03-07T00:00:00Z | 1 | 2020-03-08T16:00:00Z | window_close | 9 | tuning | False | — | — | — |
| ETHUSDT | 2020-05-14T20:00:00Z | 1 | 2020-05-16T00:00:00Z | window_close | 6 | tuning | False | — | — | — |
| ETHUSDT | 2020-06-22T12:00:00Z | 1 | 2020-06-26T04:00:00Z | window_close | 21 | tuning | False | — | — | — |
| ETHUSDT | 2020-08-29T16:00:00Z | 1 | 2020-09-04T08:00:00Z | window_close | 33 | tuning | False | — | — | — |
| ETHUSDT | 2020-09-13T04:00:00Z | 1 | 2020-09-13T12:00:00Z | window_close | 1 | tuning | False | — | — | — |
| ETHUSDT | 2020-09-17T16:00:00Z | 1 | 2020-09-21T08:00:00Z | window_close | 21 | tuning | True | 2020-09-19T14:00:00Z | 42 | 10 |
| ETHUSDT | 2021-07-09T08:00:00Z | -1 | 2021-07-23T04:00:00Z | window_close | 82 | tuning | True | 2021-07-10T04:00:00Z | 312 | 78 |
| ETHUSDT | 2021-09-16T00:00:00Z | 1 | 2021-09-19T08:00:00Z | window_close | 19 | tuning | True | 2021-09-18T10:00:00Z | 22 | 5 |
| ETHUSDT | 2021-11-25T16:00:00Z | 1 | 2021-11-26T12:00:00Z | window_close | 4 | tuning | False | — | — | — |
| ETHUSDT | 2021-11-29T20:00:00Z | 1 | 2021-12-04T08:00:00Z | window_close | 26 | tuning | True | 2021-12-03T10:00:00Z | 22 | 5 |
| ETHUSDT | 2022-02-13T16:00:00Z | -1 | 2022-02-15T08:00:00Z | window_close | 9 | tuning | False | — | — | — |
| ETHUSDT | 2022-07-11T16:00:00Z | -1 | 2022-07-15T08:00:00Z | window_close | 21 | tuning | False | — | — | — |
| ETHUSDT | 2022-12-07T16:00:00Z | -1 | 2022-12-08T20:00:00Z | window_close | 6 | tuning | False | — | — | — |
| ETHUSDT | 2023-02-15T20:00:00Z | 1 | 2023-02-24T20:00:00Z | window_close | 53 | tuning | True | 2023-02-17T17:00:00Z | 171 | 42 |
| ETHUSDT | 2023-03-01T08:00:00Z | 1 | 2023-03-03T04:00:00Z | window_close | 10 | tuning | False | — | — | — |
| ETHUSDT | 2023-05-05T12:00:00Z | 1 | 2023-05-08T08:00:00Z | window_close | 16 | tuning | True | 2023-05-07T17:00:00Z | 15 | 3 |
| ETHUSDT | 2023-07-20T08:00:00Z | 1 | 2023-07-20T16:00:00Z | window_close | 1 | tuning | False | — | — | — |
| ETHUSDT | 2024-01-09T04:00:00Z | 1 | 2024-01-22T08:00:00Z | window_close | 78 | tuning | True | 2024-01-09T23:00:00Z | 297 | 74 |
| ETHUSDT | 2024-02-06T16:00:00Z | 1 | 2024-03-17T00:00:00Z | window_close | 235 | tuning | True | 2024-02-12T01:00:00Z | 815 | 203 |
| ETHUSDT | 2024-03-26T04:00:00Z | 1 | 2024-03-30T00:00:00Z | window_close | 22 | tuning | True | 2024-03-28T10:00:00Z | 38 | 9 |
| ETHUSDT | 2024-04-08T08:00:00Z | 1 | 2024-04-12T20:00:00Z | window_close | 26 | tuning | True | 2024-04-11T03:00:00Z | 41 | 10 |
| ETHUSDT | 2024-08-27T12:00:00Z | -1 | 2024-09-15T04:00:00Z | window_close | 111 | holdout | True | 2024-08-30T00:00:00Z | 388 | 97 |
| ETHUSDT | 2025-01-03T16:00:00Z | 1 | 2025-01-08T08:00:00Z | window_close | 27 | holdout | False | — | — | — |
| ETHUSDT | 2025-06-30T00:00:00Z | 1 | 2025-07-01T20:00:00Z | window_close | 10 | holdout | False | — | — | — |
| ETHUSDT | 2025-07-02T16:00:00Z | 1 | 2025-08-02T08:00:00Z | window_close | 183 | holdout | True | 2025-07-06T14:00:00Z | 642 | 160 |
| ETHUSDT | 2026-03-07T16:00:00Z | -1 | 2026-03-10T08:00:00Z | window_close | 15 | holdout | False | — | — | — |
| ETHUSDT | 2026-03-22T08:00:00Z | -1 | 2026-03-24T08:00:00Z | window_close | 11 | holdout | False | — | — | — |
| ETHUSDT | 2026-03-26T12:00:00Z | -1 | 2026-04-01T12:00:00Z | window_close | 35 | holdout | True | 2026-03-29T01:00:00Z | 83 | 20 |
| ETHUSDT | 2026-04-29T08:00:00Z | 1 | 2026-04-29T16:00:00Z | window_close | 1 | holdout | False | — | — | — |
| ETHUSDT | 2026-05-02T20:00:00Z | 1 | 2026-05-08T08:00:00Z | window_close | 32 | holdout | False | — | — | — |
| ETHUSDT | 2026-08-12T08:00:00Z | 1 | 2026-08-12T20:00:00Z | window_close | 2 | holdout | False | — | — | — |
| NEARUSDT | 2020-12-16T16:00:00Z | 1 | 2020-12-24T08:00:00Z | window_close | 45 | tuning | True | 2020-12-19T05:00:00Z | 123 | 30 |
| NEARUSDT | 2021-01-31T00:00:00Z | 1 | 2021-01-31T20:00:00Z | window_close | 4 | tuning | False | — | — | — |
| NEARUSDT | 2021-05-09T04:00:00Z | -1 | 2021-05-12T20:00:00Z | window_close | 21 | tuning | True | 2021-05-10T11:00:00Z | 57 | 14 |
| NEARUSDT | 2021-05-12T20:00:00Z | -1 | 2021-05-14T00:00:00Z | window_close | 6 | tuning | True | 2021-05-13T05:00:00Z | 19 | 4 |
| NEARUSDT | 2021-09-24T00:00:00Z | 1 | 2021-09-24T20:00:00Z | window_close | 4 | tuning | False | — | — | — |
| NEARUSDT | 2022-03-07T16:00:00Z | -1 | 2022-03-09T12:00:00Z | window_close | 10 | tuning | False | — | — | — |
| NEARUSDT | 2022-07-11T08:00:00Z | -1 | 2022-07-17T00:00:00Z | window_close | 33 | tuning | True | 2022-07-16T04:00:00Z | 20 | 5 |
| NEARUSDT | 2022-07-26T08:00:00Z | -1 | 2022-07-28T12:00:00Z | window_close | 12 | tuning | False | — | — | — |
| NEARUSDT | 2022-10-27T20:00:00Z | -1 | 2022-10-29T16:00:00Z | window_close | 10 | tuning | False | — | — | — |
| NEARUSDT | 2022-11-02T04:00:00Z | -1 | 2022-11-04T08:00:00Z | window_close | 12 | tuning | False | — | — | — |
| NEARUSDT | 2022-11-08T00:00:00Z | -1 | 2022-12-07T00:00:00Z | window_close | 173 | tuning | True | 2022-11-11T04:00:00Z | 620 | 155 |
| NEARUSDT | 2023-02-16T00:00:00Z | 1 | 2023-02-24T16:00:00Z | window_close | 51 | tuning | True | 2023-02-17T18:00:00Z | 166 | 41 |
| NEARUSDT | 2023-03-15T20:00:00Z | -1 | 2023-03-17T20:00:00Z | window_close | 11 | tuning | False | — | — | — |
| NEARUSDT | 2023-07-05T16:00:00Z | -1 | 2023-07-14T00:00:00Z | window_close | 49 | tuning | True | 2023-07-07T19:00:00Z | 149 | 37 |
| NEARUSDT | 2024-01-11T16:00:00Z | 1 | 2024-01-13T12:00:00Z | window_close | 10 | tuning | True | 2024-01-12T15:00:00Z | 21 | 5 |
| NEARUSDT | 2024-01-30T08:00:00Z | 1 | 2024-01-31T16:00:00Z | window_close | 7 | tuning | False | — | — | — |
| NEARUSDT | 2024-04-05T16:00:00Z | 1 | 2024-04-12T00:00:00Z | window_close | 37 | tuning | True | 2024-04-07T02:00:00Z | 118 | 29 |
| NEARUSDT | 2024-08-29T16:00:00Z | -1 | 2024-09-12T04:00:00Z | window_close | 80 | holdout | True | 2024-09-03T12:00:00Z | 208 | 52 |
| NEARUSDT | 2024-09-16T16:00:00Z | -1 | 2024-09-17T20:00:00Z | window_close | 6 | holdout | False | — | — | — |
| NEARUSDT | 2024-09-18T12:00:00Z | -1 | 2024-09-19T00:00:00Z | window_close | 2 | holdout | False | — | — | — |
| NEARUSDT | 2024-10-07T04:00:00Z | 1 | 2024-10-09T20:00:00Z | window_close | 15 | holdout | False | — | — | — |
| NEARUSDT | 2024-10-14T16:00:00Z | 1 | 2024-10-18T00:00:00Z | window_close | 19 | holdout | True | 2024-10-17T04:00:00Z | 20 | 5 |
| NEARUSDT | 2025-01-08T04:00:00Z | -1 | 2025-01-17T08:00:00Z | window_close | 54 | holdout | True | 2025-01-10T16:00:00Z | 160 | 40 |
| NEARUSDT | 2025-05-04T12:00:00Z | -1 | 2025-05-08T20:00:00Z | window_close | 25 | holdout | True | 2025-05-07T06:00:00Z | 38 | 9 |
| NEARUSDT | 2025-08-23T20:00:00Z | 1 | 2025-08-25T08:00:00Z | window_close | 8 | holdout | True | 2025-08-24T19:00:00Z | 13 | 3 |
| NEARUSDT | 2026-06-15T04:00:00Z | 1 | 2026-06-19T12:00:00Z | window_close | 25 | holdout | False | — | — | — |
| SOLUSDT | 2020-11-26T08:00:00Z | -1 | 2020-12-02T16:00:00Z | window_close | 37 | tuning | False | — | — | — |
| SOLUSDT | 2021-12-01T08:00:00Z | 1 | 2021-12-04T12:00:00Z | window_close | 18 | tuning | False | — | — | — |
| SOLUSDT | 2022-03-04T16:00:00Z | -1 | 2022-03-17T16:00:00Z | window_close | 77 | tuning | True | 2022-03-08T17:00:00Z | 215 | 53 |
| SOLUSDT | 2022-06-29T08:00:00Z | -1 | 2022-07-06T16:00:00Z | window_close | 43 | tuning | True | 2022-07-01T11:00:00Z | 125 | 31 |
| SOLUSDT | 2022-07-11T20:00:00Z | -1 | 2022-07-15T08:00:00Z | window_close | 20 | tuning | False | — | — | — |
| SOLUSDT | 2022-07-25T12:00:00Z | -1 | 2022-07-28T20:00:00Z | window_close | 19 | tuning | False | — | — | — |
| SOLUSDT | 2022-08-03T04:00:00Z | -1 | 2022-08-08T04:00:00Z | window_close | 29 | tuning | True | 2022-08-07T01:00:00Z | 27 | 6 |
| SOLUSDT | 2022-10-01T20:00:00Z | -1 | 2022-10-04T16:00:00Z | window_close | 16 | tuning | False | — | — | — |
| SOLUSDT | 2023-02-16T00:00:00Z | 1 | 2023-02-25T04:00:00Z | window_close | 54 | tuning | True | 2023-02-17T20:00:00Z | 176 | 44 |
| SOLUSDT | 2023-03-15T20:00:00Z | -1 | 2023-03-18T00:00:00Z | window_close | 12 | tuning | False | — | — | — |
| SOLUSDT | 2023-04-28T16:00:00Z | 1 | 2023-05-02T00:00:00Z | window_close | 19 | tuning | True | 2023-04-30T06:00:00Z | 42 | 10 |
| SOLUSDT | 2023-05-06T00:00:00Z | 1 | 2023-05-06T20:00:00Z | window_close | 4 | tuning | False | — | — | — |
| SOLUSDT | 2023-06-06T04:00:00Z | -1 | 2023-06-22T00:00:00Z | window_close | 94 | tuning | True | 2023-06-09T17:00:00Z | 295 | 73 |
| SOLUSDT | 2023-08-09T00:00:00Z | 1 | 2023-08-16T12:00:00Z | window_close | 44 | tuning | True | 2023-08-11T14:00:00Z | 118 | 29 |
| SOLUSDT | 2024-01-17T08:00:00Z | 1 | 2024-01-19T00:00:00Z | window_close | 9 | tuning | False | — | — | — |
| SOLUSDT | 2024-08-28T16:00:00Z | -1 | 2024-09-13T20:00:00Z | window_close | 96 | holdout | True | 2024-09-03T15:00:00Z | 245 | 61 |
| SOLUSDT | 2024-10-07T12:00:00Z | 1 | 2024-10-08T00:00:00Z | window_close | 2 | holdout | False | — | — | — |
| SOLUSDT | 2024-10-12T20:00:00Z | 1 | 2024-11-02T12:00:00Z | window_close | 123 | holdout | True | 2024-10-13T22:00:00Z | 470 | 117 |
| SOLUSDT | 2025-01-08T12:00:00Z | -1 | 2025-01-16T08:00:00Z | window_close | 46 | holdout | True | 2025-01-10T14:00:00Z | 138 | 34 |
| SOLUSDT | 2025-03-28T16:00:00Z | -1 | 2025-04-12T12:00:00Z | window_close | 88 | holdout | True | 2025-03-31T10:00:00Z | 290 | 72 |
| SOLUSDT | 2025-06-10T20:00:00Z | 1 | 2025-06-13T00:00:00Z | window_close | 12 | holdout | False | — | — | — |
| SOLUSDT | 2025-08-21T00:00:00Z | 1 | 2025-08-21T20:00:00Z | window_close | 4 | holdout | False | — | — | — |
| SOLUSDT | 2025-10-02T00:00:00Z | 1 | 2025-10-10T00:00:00Z | window_close | 47 | holdout | True | 2025-10-05T05:00:00Z | 115 | 28 |
| SOLUSDT | 2026-03-07T12:00:00Z | -1 | 2026-03-10T16:00:00Z | window_close | 18 | holdout | False | — | — | — |
| SOLUSDT | 2026-03-22T08:00:00Z | -1 | 2026-03-24T00:00:00Z | window_close | 9 | holdout | False | — | — | — |
| SOLUSDT | 2026-04-27T16:00:00Z | -1 | 2026-05-05T16:00:00Z | window_close | 47 | holdout | True | 2026-04-29T16:00:00Z | 144 | 36 |
| SOLUSDT | 2026-06-19T00:00:00Z | -1 | 2026-06-21T00:00:00Z | window_close | 11 | holdout | False | — | — | — |
| SOLUSDT | 2026-06-23T16:00:00Z | -1 | 2026-06-27T08:00:00Z | window_close | 21 | holdout | True | 2026-06-25T13:00:00Z | 43 | 10 |
| ZECUSDT | 2020-05-17T04:00:00Z | 1 | 2020-05-26T16:00:00Z | window_close | 56 | tuning | True | 2020-05-19T10:00:00Z | 174 | 43 |
| ZECUSDT | 2020-08-30T16:00:00Z | 1 | 2020-09-02T20:00:00Z | window_close | 18 | tuning | True | 2020-09-01T06:00:00Z | 38 | 9 |
| ZECUSDT | 2020-12-16T20:00:00Z | 1 | 2020-12-22T04:00:00Z | window_close | 31 | tuning | True | 2020-12-19T11:00:00Z | 65 | 16 |
| ZECUSDT | 2021-02-02T04:00:00Z | 1 | 2021-02-23T08:00:00Z | window_close | 126 | tuning | True | 2021-02-05T09:00:00Z | 431 | 107 |
| ZECUSDT | 2021-09-02T04:00:00Z | 1 | 2021-09-08T04:00:00Z | window_close | 35 | tuning | True | 2021-09-03T12:00:00Z | 112 | 28 |
| ZECUSDT | 2021-10-12T04:00:00Z | -1 | 2021-10-15T00:00:00Z | window_close | 16 | tuning | True | 2021-10-13T06:00:00Z | 42 | 10 |
| ZECUSDT | 2021-11-21T04:00:00Z | 1 | 2021-12-03T20:00:00Z | window_close | 75 | tuning | True | 2021-11-23T04:00:00Z | 256 | 64 |
| ZECUSDT | 2022-02-18T08:00:00Z | -1 | 2022-03-01T00:00:00Z | window_close | 63 | tuning | True | 2022-02-19T22:00:00Z | 218 | 54 |
| ZECUSDT | 2022-03-06T20:00:00Z | -1 | 2022-03-08T12:00:00Z | window_close | 9 | tuning | False | — | — | — |
| ZECUSDT | 2022-07-23T16:00:00Z | -1 | 2022-07-28T16:00:00Z | window_close | 29 | tuning | True | 2022-07-24T13:00:00Z | 99 | 24 |
| ZECUSDT | 2022-12-16T20:00:00Z | -1 | 2023-01-04T04:00:00Z | window_close | 109 | tuning | True | 2022-12-19T16:00:00Z | 372 | 93 |
| ZECUSDT | 2023-02-08T08:00:00Z | 1 | 2023-02-09T00:00:00Z | window_close | 3 | tuning | False | — | — | — |
| ZECUSDT | 2023-02-12T12:00:00Z | 1 | 2023-02-13T16:00:00Z | window_close | 6 | tuning | False | — | — | — |
| ZECUSDT | 2023-02-16T04:00:00Z | 1 | 2023-02-17T16:00:00Z | window_close | 8 | tuning | False | — | — | — |
| ZECUSDT | 2023-05-31T20:00:00Z | -1 | 2023-06-22T00:00:00Z | window_close | 126 | tuning | True | 2023-06-02T14:00:00Z | 466 | 116 |
| ZECUSDT | 2023-06-22T20:00:00Z | -1 | 2023-06-23T08:00:00Z | window_close | 2 | tuning | False | — | — | — |
| ZECUSDT | 2023-11-24T20:00:00Z | 1 | 2023-11-27T20:00:00Z | window_close | 17 | tuning | False | — | — | — |
| ZECUSDT | 2024-03-25T20:00:00Z | 1 | 2024-04-01T12:00:00Z | window_close | 39 | tuning | True | 2024-03-28T07:00:00Z | 101 | 25 |
| ZECUSDT | 2024-05-11T20:00:00Z | -1 | 2024-05-16T08:00:00Z | window_close | 26 | tuning | True | 2024-05-12T17:00:00Z | 87 | 21 |
| ZECUSDT | 2024-09-22T16:00:00Z | -1 | 2024-09-28T00:00:00Z | window_close | 31 | holdout | True | 2024-09-23T09:00:00Z | 111 | 27 |
| ZECUSDT | 2025-02-18T12:00:00Z | -1 | 2025-02-19T16:00:00Z | window_close | 6 | holdout | False | — | — | — |
| ZECUSDT | 2025-02-24T12:00:00Z | -1 | 2025-02-27T04:00:00Z | window_close | 15 | holdout | False | — | — | — |
| ZECUSDT | 2025-03-21T12:00:00Z | -1 | 2025-03-25T12:00:00Z | window_close | 23 | holdout | True | 2025-03-23T23:00:00Z | 37 | 9 |
| ZECUSDT | 2025-04-24T00:00:00Z | -1 | 2025-04-24T12:00:00Z | window_close | 2 | holdout | True | 2025-04-24T07:00:00Z | 5 | 1 |
| ZECUSDT | 2025-04-27T20:00:00Z | -1 | 2025-04-28T04:00:00Z | window_close | 1 | holdout | False | — | — | — |
| ZECUSDT | 2025-12-10T04:00:00Z | 1 | 2025-12-15T04:00:00Z | window_close | 29 | holdout | True | 2025-12-11T13:00:00Z | 87 | 21 |
| ZECUSDT | 2025-12-19T20:00:00Z | 1 | 2025-12-24T08:00:00Z | window_close | 26 | holdout | True | 2025-12-22T01:00:00Z | 55 | 13 |
| ZECUSDT | 2026-03-21T20:00:00Z | -1 | 2026-03-25T08:00:00Z | window_close | 20 | holdout | True | 2026-03-24T18:00:00Z | 14 | 3 |
| ZECUSDT | 2026-06-02T20:00:00Z | 1 | 2026-06-04T20:00:00Z | window_close | 11 | holdout | False | — | — | — |
| ZECUSDT | 2026-08-04T16:00:00Z | 1 | 2026-08-11T16:00:00Z | window_close | 41 | holdout | True | 2026-08-07T09:00:00Z | 103 | 25 |

## W1 on the other 4h books (Tier-E, whole; final-review fidelity MINOR-1)

The contract's W1 stamps every 4h campaign's timeline with the 1h events; the first build stamped v6 only. The 9/12 book, P-BRK-4H scored and P-RELAY-1 scored are stamped here by the same 1h event tape and the same classifiers as W1_EVENTS (w12): 1h 9/12, 12/26 and 12/89 crosses with / against the campaign, PRE-ENTRY / IN-TRADE / AT-EXIT / POST-EXIT and before / after the +1R latch (L-W.3), visibility (L-W.1) on every event row. Counts and W2's cohort sizes only — no outcome statistic, no mark, no forward leg. Every row: tier TIER-E · a SELECTION, not a result · gates nothing.

- **trg912** (n 199) — research_outputs/tierc11/books/trg912_campaigns.parquet — the TC11-BOOKS 9/12 book (B.trg912_book; filed book_sha asserted), re-ridden per campaign by RD.transform_book(walk=other_walk). Window open (w13): arm close (the 9/12 card's window arming). Source check: {'book_sha': '2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030', 'ctrl_cols_worst_walked': 0.0, 'ctrl_cols_ok': True}. 1h resolution (w14): {'1h-walk': 199}; exits resolved by {'1h': 191, 'close': 8}; 4h-close fallbacks 0; the two +1R latch readings (L-W.3 / L-W.5) agree on 199/199; latch present == the book's own reached_1r on 199/199; L-W.0 mismatch bars ridden 2 (BTCUSDT 2023-11-10T12:00:00Z, ZECUSDT 2024-10-28T20:00:00Z); W1 events 4153 by phase {'AT-EXIT': 64, 'IN-TRADE': 1849, 'POST-EXIT': 58, 'PRE-ENTRY': 2182}, on mismatch bars 0 (taken at the parent close, w1), classifications the raw instant would change 0; entry bars straddling the era cut 0.
- **P-BRK-4H** (n 322) — research_outputs/tierc11/regbooks/P-BRK-4H/scored.parquet — the scored book (sidecar book_sha256 == this stage's recomputation == the scorer's input), re-ridden per campaign by RD.ride11(walk=other_walk(sym)). Window open (w13): death close (the 4h macro death that opens the lane's candidacy). Source check: {'book_sha256': 'c76358dfaeb034ddc679f74f0f26f40eca9a88bcbb48c5c62bcac45f5b4ec311'}. 1h resolution (w14): {'1h-walk': 322}; exits resolved by {'1h': 269, 'close': 53}; 4h-close fallbacks 0; the two +1R latch readings (L-W.3 / L-W.5) agree on 322/322; latch present == the book's own reached_1r on 322/322; L-W.0 mismatch bars ridden 2 (BTCUSDT 2024-10-28T20:00:00Z, SOLUSDT 2024-10-28T20:00:00Z); W1 events 11585 by phase {'AT-EXIT': 54, 'IN-TRADE': 3537, 'POST-EXIT': 21, 'PRE-ENTRY': 7973}, on mismatch bars 1 (taken at the parent close, w1: SOLUSDT entry 2024-10-26T12:00:00Z 9/12 with 1h close 2024-10-28T22:00:00Z -> taken 2024-10-29T00:00:00Z (IN-TRADE before)), classifications the raw instant would change 0; entry bars straddling the era cut 0.
- **P-RELAY-1** (n 173) — research_outputs/tierc11/regbooks/P-RELAY-1/scored.parquet — the scored book (sidecar book_sha256 == this stage's recomputation == the scorer's input), its path of record re-run by RD.relay11(walk_after=True, moved=). Window open (w13): window arm close (the v6 window the relay entered). Source check: {'book_sha256': '57d8bbef8190492d1df83a137977463ee441508e20a57cd81499c60258a53361'}. 1h resolution (w14): {'1h-walk': 173}; exits resolved by {'1h': 162, 'close': 11}; 4h-close fallbacks 0; the two +1R latch readings (L-W.3 / L-W.5) agree on 173/173; latch present == the book's own reached_1r on 173/173; L-W.0 mismatch bars ridden 0 (none); W1 events 2190 by phase {'AT-EXIT': 57, 'IN-TRADE': 1608, 'POST-EXIT': 39, 'PRE-ENTRY': 486}, on mismatch bars 0 (taken at the parent close, w1), classifications the raw instant would change 0; entry bars straddling the era cut 0.

Mismatch-bar note (AM-5 and its ERRATUM, which were written of the books ridden on the walk before this repair): under the 1h resolution added here the other books ride 4 L-W.0 mismatch bar(s) (listed per book above; the parent decides STOP and the +1R latch there, AM-5) and hold 1 W1 event(s) on one, each taken at the parent close (w1); classifications the raw 1h instant would change: 0. Printed here; LEANS_AMENDMENTS.md is not this stage's file.

W1_OTHER_SUMMARY, whole. Event rows: n events (n campaigns holding one). Cohort rows (W2's cohorts vs their at-risk sets, w6): n campaigns (n events). Pre-entry rows (W2's classes in (window open, entry close] vs the whole book): n campaigns (n events).

| kind | class | group | trg912 ALL | trg912 tuning | trg912 holdout | P-BRK-4H ALL | P-BRK-4H tuning | P-BRK-4H holdout | P-RELAY-1 ALL | P-RELAY-1 tuning | P-RELAY-1 holdout |
|---|---|---|---|---|---|---|---|---|---|---|---|
| campaigns | all | book | 199 (4153 ev) | 132 (2777 ev) | 67 (1376 ev) | 322 (11585 ev) | 210 (7527 ev) | 112 (4058 ev) | 173 (2190 ev) | 114 (1466 ev) | 59 (724 ev) |
| events | PRE-ENTRY · 9/12 · counter · - | events | 602 (124) | 422 (83) | 180 (41) | 2297 (320) | 1491 (209) | 806 (111) | 173 (173) | 114 (114) | 59 (59) |
| events | PRE-ENTRY · 9/12 · with · - | events | 599 (124) | 419 (83) | 180 (41) | 2097 (307) | 1359 (201) | 738 (106) | 173 (173) | 114 (114) | 59 (59) |
| events | PRE-ENTRY · 12/26 · counter · - | events | 349 (124) | 245 (83) | 104 (41) | 1374 (322) | 870 (210) | 504 (112) | 81 (79) | 52 (51) | 29 (28) |
| events | PRE-ENTRY · 12/26 · with · - | events | 336 (119) | 236 (80) | 100 (39) | 1105 (277) | 690 (178) | 415 (99) | 33 (31) | 24 (23) | 9 (8) |
| events | PRE-ENTRY · 12/89 · counter · - | events | 138 (110) | 90 (70) | 48 (40) | 692 (316) | 429 (207) | 263 (109) | 18 (18) | 12 (12) | 6 (6) |
| events | PRE-ENTRY · 12/89 · with · - | events | 158 (130) | 103 (84) | 55 (46) | 408 (183) | 241 (112) | 167 (71) | 8 (7) | 5 (4) | 3 (3) |
| events | IN-TRADE · 9/12 · counter · before | events | 255 (113) | 179 (76) | 76 (37) | 442 (171) | 311 (115) | 131 (56) | 259 (115) | 183 (78) | 76 (37) |
| events | IN-TRADE · 9/12 · counter · after | events | 364 (107) | 219 (69) | 145 (38) | 521 (154) | 339 (100) | 182 (54) | 277 (91) | 185 (57) | 92 (34) |
| events | IN-TRADE · 9/12 · with · before | events | 190 (79) | 132 (55) | 58 (24) | 491 (211) | 351 (147) | 140 (64) | 187 (74) | 133 (50) | 54 (24) |
| events | IN-TRADE · 9/12 · with · after | events | 272 (86) | 162 (53) | 110 (33) | 394 (120) | 255 (80) | 139 (40) | 202 (71) | 139 (46) | 63 (25) |
| events | IN-TRADE · 12/26 · counter · before | events | 146 (82) | 104 (57) | 42 (25) | 257 (122) | 187 (84) | 70 (38) | 162 (81) | 114 (54) | 48 (27) |
| events | IN-TRADE · 12/26 · counter · after | events | 201 (97) | 120 (61) | 81 (36) | 297 (137) | 189 (90) | 108 (47) | 151 (76) | 87 (45) | 64 (31) |
| events | IN-TRADE · 12/26 · with · before | events | 103 (55) | 70 (38) | 33 (17) | 316 (162) | 231 (115) | 85 (47) | 148 (76) | 99 (46) | 49 (30) |
| events | IN-TRADE · 12/26 · with · after | events | 124 (63) | 74 (40) | 50 (23) | 222 (104) | 142 (69) | 80 (35) | 90 (42) | 54 (27) | 36 (15) |
| events | IN-TRADE · 12/89 · counter · before | events | 89 (63) | 61 (45) | 28 (18) | 154 (85) | 107 (56) | 47 (29) | 52 (33) | 35 (21) | 17 (12) |
| events | IN-TRADE · 12/89 · counter · after | events | 40 (32) | 20 (17) | 20 (15) | 120 (78) | 69 (48) | 51 (30) | 31 (26) | 16 (14) | 15 (12) |
| events | IN-TRADE · 12/89 · with · before | events | 48 (32) | 31 (21) | 17 (11) | 195 (113) | 139 (77) | 56 (36) | 37 (22) | 25 (13) | 12 (9) |
| events | IN-TRADE · 12/89 · with · after | events | 17 (15) | 8 (7) | 9 (8) | 128 (82) | 75 (51) | 53 (31) | 12 (12) | 7 (7) | 5 (5) |
| events | AT-EXIT · 9/12 · counter · - | events | 22 (22) | 13 (13) | 9 (9) | 17 (17) | 13 (13) | 4 (4) | 18 (18) | 11 (11) | 7 (7) |
| events | AT-EXIT · 9/12 · with · - | events | 1 (1) | 0 (0) | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| events | AT-EXIT · 12/26 · counter · - | events | 23 (23) | 16 (16) | 7 (7) | 24 (24) | 17 (17) | 7 (7) | 22 (22) | 18 (18) | 4 (4) |
| events | AT-EXIT · 12/26 · with · - | events | 1 (1) | 0 (0) | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| events | AT-EXIT · 12/89 · counter · - | events | 17 (17) | 12 (12) | 5 (5) | 13 (13) | 8 (8) | 5 (5) | 17 (17) | 13 (13) | 4 (4) |
| events | AT-EXIT · 12/89 · with · - | events | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| events | POST-EXIT · 9/12 · counter · - | events | 10 (10) | 7 (7) | 3 (3) | 1 (1) | 0 (0) | 1 (1) | 1 (1) | 1 (1) | 0 (0) |
| events | POST-EXIT · 9/12 · with · - | events | 3 (3) | 2 (2) | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 3 (3) | 1 (1) | 2 (2) |
| events | POST-EXIT · 12/26 · counter · - | events | 17 (17) | 12 (12) | 5 (5) | 5 (5) | 3 (3) | 2 (2) | 10 (10) | 8 (8) | 2 (2) |
| events | POST-EXIT · 12/26 · with · - | events | 2 (2) | 2 (2) | 0 (0) | 0 (0) | 0 (0) | 0 (0) | 1 (1) | 1 (1) | 0 (0) |
| events | POST-EXIT · 12/89 · counter · - | events | 26 (26) | 18 (18) | 8 (8) | 14 (14) | 10 (10) | 4 (4) | 24 (24) | 15 (15) | 9 (9) |
| events | POST-EXIT · 12/89 · with · - | events | 0 (0) | 0 (0) | 0 (0) | 1 (1) | 1 (1) | 0 (0) | 0 (0) | 0 (0) | 0 (0) |
| cohort | C1_counter_12_89_before_1r | cohort | 63 (89) | 45 (61) | 18 (28) | 85 (154) | 56 (107) | 29 (47) | 33 (52) | 21 (35) | 12 (17) |
| cohort | C1_counter_12_89_before_1r | at_risk | 199 (89) | 132 (61) | 67 (28) | 322 (154) | 210 (107) | 112 (47) | 173 (52) | 114 (35) | 59 (17) |
| cohort | C1_counter_12_89_before_1r | complement | 136 (0) | 87 (0) | 49 (0) | 237 (0) | 154 (0) | 83 (0) | 140 (0) | 93 (0) | 47 (0) |
| cohort | C2_counter_12_26_before_1r | cohort | 82 (146) | 57 (104) | 25 (42) | 122 (257) | 84 (187) | 38 (70) | 81 (162) | 54 (114) | 27 (48) |
| cohort | C2_counter_12_26_before_1r | at_risk | 199 (146) | 132 (104) | 67 (42) | 322 (257) | 210 (187) | 112 (70) | 173 (162) | 114 (114) | 59 (48) |
| cohort | C2_counter_12_26_before_1r | complement | 117 (0) | 75 (0) | 42 (0) | 200 (0) | 126 (0) | 74 (0) | 92 (0) | 60 (0) | 32 (0) |
| cohort | C3_with_9_12_recross_after_entry | cohort | 124 (462) | 85 (294) | 39 (168) | 234 (885) | 158 (606) | 76 (279) | 113 (389) | 76 (272) | 37 (117) |
| cohort | C3_with_9_12_recross_after_entry | at_risk | 197 (462) | 131 (294) | 66 (168) | 317 (885) | 206 (606) | 111 (279) | 172 (389) | 113 (272) | 59 (117) |
| cohort | C3_with_9_12_recross_after_entry | complement | 73 (0) | 46 (0) | 27 (0) | 83 (0) | 48 (0) | 35 (0) | 59 (0) | 37 (0) | 22 (0) |
| cohort | C4_counter_12_89_after_1r | cohort | 32 (40) | 17 (20) | 15 (20) | 78 (120) | 48 (69) | 30 (51) | 26 (31) | 14 (16) | 12 (15) |
| cohort | C4_counter_12_89_after_1r | at_risk | 112 (40) | 72 (20) | 40 (20) | 158 (120) | 103 (69) | 55 (51) | 95 (31) | 61 (16) | 34 (15) |
| cohort | C4_counter_12_89_after_1r | complement | 80 (0) | 55 (0) | 25 (0) | 80 (0) | 55 (0) | 25 (0) | 69 (0) | 47 (0) | 22 (0) |
| cohort | C3S_with_9_12_recross_strict | cohort | 123 (459) | 84 (291) | 39 (168) | 184 (725) | 125 (496) | 59 (229) | 113 (389) | 76 (272) | 37 (117) |
| cohort | C3S_with_9_12_recross_strict | at_risk | 197 (459) | 131 (291) | 66 (168) | 317 (725) | 206 (496) | 111 (229) | 172 (389) | 113 (272) | 59 (117) |
| cohort | C3S_with_9_12_recross_strict | complement | 74 (0) | 47 (0) | 27 (0) | 133 (0) | 81 (0) | 52 (0) | 59 (0) | 37 (0) | 22 (0) |
| pre_entry | P1_counter_12_89 | cohort | 110 (138) | 70 (90) | 40 (48) | 316 (692) | 207 (429) | 109 (263) | 18 (18) | 12 (12) | 6 (6) |
| pre_entry | P1_counter_12_89 | whole_book | 199 (138) | 132 (90) | 67 (48) | 322 (692) | 210 (429) | 112 (263) | 173 (18) | 114 (12) | 59 (6) |
| pre_entry | P1_counter_12_89 | complement | 89 (0) | 62 (0) | 27 (0) | 6 (0) | 3 (0) | 3 (0) | 155 (0) | 102 (0) | 53 (0) |
| pre_entry | P2_counter_12_26 | cohort | 124 (349) | 83 (245) | 41 (104) | 322 (1374) | 210 (870) | 112 (504) | 79 (81) | 51 (52) | 28 (29) |
| pre_entry | P2_counter_12_26 | whole_book | 199 (349) | 132 (245) | 67 (104) | 322 (1374) | 210 (870) | 112 (504) | 173 (81) | 114 (52) | 59 (29) |
| pre_entry | P2_counter_12_26 | complement | 75 (0) | 49 (0) | 26 (0) | 0 (0) | 0 (0) | 0 (0) | 94 (0) | 63 (0) | 31 (0) |
| pre_entry | P3_with_9_12 | cohort | 124 (599) | 83 (419) | 41 (180) | 307 (2097) | 201 (1359) | 106 (738) | 173 (173) | 114 (114) | 59 (59) |
| pre_entry | P3_with_9_12 | whole_book | 199 (599) | 132 (419) | 67 (180) | 322 (2097) | 210 (1359) | 112 (738) | 173 (173) | 114 (114) | 59 (59) |
| pre_entry | P3_with_9_12 | complement | 75 (0) | 49 (0) | 26 (0) | 15 (0) | 9 (0) | 6 (0) | 0 (0) | 0 (0) | 0 (0) |
| pre_entry | P4_with_12_26 | cohort | 119 (336) | 80 (236) | 39 (100) | 277 (1105) | 178 (690) | 99 (415) | 31 (33) | 23 (24) | 8 (9) |
| pre_entry | P4_with_12_26 | whole_book | 199 (336) | 132 (236) | 67 (100) | 322 (1105) | 210 (690) | 112 (415) | 173 (33) | 114 (24) | 59 (9) |
| pre_entry | P4_with_12_26 | complement | 80 (0) | 52 (0) | 28 (0) | 45 (0) | 32 (0) | 13 (0) | 142 (0) | 91 (0) | 51 (0) |

## Files

| table | content sha256 |
|---|---|
| P_WARN_1_COMPLEMENT | 12355b7ff5b09e55091dbbeaaabdf1330f73a8d15cf05604b773f72ef77f7b17 |
| W1_CAMPAIGNS | efd27667ea0afaf9618fb87771994e0cf735ad8432f5ae6e2882db2104c92e00 |
| W1_CAMPAIGNS_OTHER | f426c5be56ed982f64c4e5b17a8fb9e08b79603f340dec782e5ee388ee073d74 |
| W1_EVENTS | 4c8286410f330a6b76a729ea33bd66f586138c04bc6bfa2ff0255ea3c26b2c8d |
| W1_EVENTS_OTHER | 31ad8e88c673335b6077454b3dac303675399837b20bdbf6f90297ea69491cc1 |
| W1_OTHER_SUMMARY | 99ef17f02b8c6521c06695ca4c64b8ac049ef2a49ac91b17992f5f48d8286c0f |
| W1_TIMELINE | ebaff8ba4f712f8f86c82c395d729b5476d5b542a5c8cafeb40686bc01aae16f |
| W2_COHORTS | 2835ef0efa8248ee5564276c89a7aad00dba749f0ab906fbb7f8d6f6efd897e4 |
| W2_FORWARD | 6f3adc7101364ab62c2b7d5f75bd30d2916b022b855ef5f76a252a22cc36f4cb |
| W2_PREENTRY | 8f849d17a0c21aae1640e83682e4755ee728bbac7eb541fadbaab571e161ab98 |
| W2_RELAY_HIST | 25479e20075939542dc41f1d4b5bfa010b51fa04df5ef753b19085a3e61dbce4 |
| W2_RELAY_SUMMARY | 692146562c3e967d1561dd6b3d308fc49cf95d4384ab1345703c85144c1a32cf |
| W2_RELAY_WINDOWS | 3809a15900c1e609314fb54cf0c567fc167678447e8969a99dc4411b3cb9169b |
| W2_RELAY_WINDOWS_TWIN | 0f4da63a765374bff57a0a925d397482b2b874e227c0e4bfd78be048b1f42f3f |

| regbook arm | n | sum net R | book_sha256 |
|---|---|---|---|
| scored | 200 | +41.923243 | 956e15390419f8ab4a2f9e644f7a041f1b20708c83f41b744eec1d4965cf54e1 |
| base | 200 | +40.807565 | f41bfaf02b86dfb0b57dcffaf3c5f5e4bb05eda5c305b361322bc334369468a8 |
| tierE__tuning | 123 | +0.341015 | c41450b34294d820d841c68f17c7ee8b0648550dcc950506905adddf74270f04 |
| tierE__holdout | 77 | +41.582228 | 9dd70a94cb2b2923e977a4c5eb7e0089c65ea85c96710a792211af3c2529323f |

W1_EVENTS / W1_TIMELINE / W1_CAMPAIGNS / W2_RELAY_WINDOWS_TWIN / W1_EVENTS_OTHER / W1_CAMPAIGNS_OTHER are filed whole as parquet (row counts in the manifest keys); every row is collared.

