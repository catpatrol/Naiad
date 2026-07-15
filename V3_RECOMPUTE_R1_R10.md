# V3 Recompute R1-R10 — Tier A (journal arithmetic only)

**Basis:** engine 1.0.7 (`2f260e1`), config `v12_anchor` (`a3917ea5...`), scored partition (exploration-classic), 20 cells.
**Journal root:** `research_outputs/v3_anchor/journal_pass1/scored`
**Evidence spend:** NONE (VR-1 exploration-classic; first look already consumed).  **Engine delta:** NONE (read-only).
**Bootstrap:** 95% CI, 10,000 resamples, campaign-level, seed `20260715` (pinned).

> **Scope.** Not tuning, not evidence about the future, not a variant nomination, not a lockbox touch, not S-1. Every number is in-sample on data already mined: it ranks candidates, it validates nothing.

## Config paste — actual run values (contract §5)

The reviewer has been working from Pine defaults. These are the real `v12_anchor.yaml` values.

### signal
| key | value |
|---|---|
| z1_prox | 0.25 |
| z2_prox | 0.35 |
| z3_prox | 0.35 |
| max_r_count | 0 |
| cooldown_bars | 5 |

### trading (entire block)
| key | value |
|---|---|
| enabled | True |
| initial_equity | 10000.0 |
| r_pct | 0.005 |
| size_r1_a_full | 0.5 |
| size_r1_b_full | 0.25 |
| size_r1_provisional | 0.25 |
| size_v | 0.25 |
| size_add | 0.5 |
| max_tranches | 3 |
| max_open_campaign_risk_r | 1.0 |
| halt_scope | per_cell |
| halt_day_r | -2.0 |
| halt_week_r | -4.0 |
| fee_bps_side | 5.0 |

### cell.zone_memory / cell.tf_align — one cell per mandate

Neither field lives in `v12_anchor.yaml`; both come from `engine/cells.py`. `zone_memory` is a constant property (=3, engine 1.0.3 Pine input-parity), identical for every cell.

| cell | mandate | zone_memory | tf_align | tf_gov | tf_exec |
|---|---|---|---|---|---|
| BTCUSDT_swing | swing | 3 | 1h | 4h | 5m |
| BTCUSDT_intraday | intraday | 3 | 5m | 1h | 1m |
| BTCUSDT_position | position | 3 | 4h | 12h | 15m |

## Fixtures F1-F9 — known-answer gates (contract §5)

Computed from raw journal bytes. `ROLLUPS_AND_HYPOTHESES.md` and `V3_STOP_AND_EXIT_FORENSICS.md` were **not** read as inputs.

| fixture | expected | computed | result |
|---|---|---|---|
| F1 campaigns | 3456 | 3456 | **MATCH** |
| F1 resolved tranches | 8387 | 8387 | **MATCH** |
| F2 sum(realized_r) cell-R | -5756.9093 | -5756.9093 | **MATCH** |
| F3 sum(r_0x) cell-R | 1345.3095 | 1345.3095 | **MATCH** |
| F4 sum(r_2x) cell-R | -12859.1281 | -12859.1281 | **MATCH** |
| F5 taxonomy census | {"PROTECTED": 3381, "STILLBORN": 2076, "NEVER_GREEN": 1830, "FADED": 1100} | {"PROTECTED": 3381, "STILLBORN": 2076, "NEVER_GREEN": 1830, "FADED": 1100} | **MATCH** |
| F6 grade cohorts (campaigns) | {"A+": 39, "A": 1153, "B": 1954, "C": 0} | {"A+": 39, "A": 1153, "B": 1954, "C": 0} | **MATCH** |
| F7 stop + stop_gap exits | 8365 | 8365 | **MATCH** |
| F8 V-initiated campaigns | 45 | 45 | **MATCH** |
| F9 signal-layer r_cap rejects | 0 | 0 | **MATCH** |

**Verdict: PASS** — 10/10 match.

### F9 next to the config value (contract §5)

| quantity | value |
|---|---|
| signal-layer `r_cap` REJECT count | 0 |
| `signal.max_r_count` in v12_anchor.yaml | 0 |
| `rcap_ok` (signals.py:368) | `max_rc == 0 or r_count < max_rc` |

**F9 MATCHES and the reviewer's reading is UPHELD.** `signal.max_r_count = 0` in the anchor config (= unlimited), and `signals.py:368` reads `rcap_ok = max_rc == 0 or r_count < max_rc`, so with max_rc = 0 the `r_cap` branch is unreachable by construction — consistent with the 0 observed. The signal layer is NOT capping PRIMEs, so unlimited adds remain a **trading-config-only** change (`trading.max_tranches`), not a Pine-parity-bound one.

## Data characteristic surfaced by the recompute — read before R9

**717 tranches carry a NEGATIVE `one_r`**, all in `ZECUSDT_intraday`.

> one_r = r_pct * equity at fill time (trading.py:367). A NEGATIVE one_r therefore means the cell's realized equity had gone BELOW ZERO and the book kept trading against it, with qty inverting sign. This is journaled faithfully and the §4 formula reproduces F3/F4 exactly with the signed value, so it is NOT a reader artifact and NOT a fixture failure -- but every R-denominated quantity on those rows is measured against a negative unit, which flips the sign of their cost adjustment. Downstream reader: treat this cell's contribution to any aggregate with suspicion, and note that a bankrupt-cell-keeps-trading path is itself a finding about the anchor run rather than about the strategy.

| cell | tranches total | tranches w/ negative one_r | Σ cell-R 1× |
|---|---|---|---|
| ZECUSDT_intraday | 1414 | 717 | -663.1247 |

## R1 — Exit-variant ranking

> **Caveat.** First-order. A really-adopted exit rule changes which adds fire and when campaigns die. Rank, do not validate. Variants carry no costs -> compared against the 0x line only. Their 1x/2x lines apply the row's ACTUAL cost/one_r as a PROXY: the counterfactual exits at a different price and holds for a different duration, so its true exit fee and funding differ.

| variant | scope | n | Σ cell-R (0×) | actual Σ r_0x | Δ vs actual (0×) | win rate % (0×) | Σ 1× (proxy) | Σ 2× (proxy) |
|---|---|---|---|---|---|---|---|---|
| X-A | GRID | 8387 | 1355.5319 | 1345.3095 | 10.2225 | 23.4649 | -5746.6869 | -12848.9057 |
| X-A | swing | 1885 | 812.5114 | 283.5952 | 528.9161 | 24.2971 | -248.4086 | -1309.3287 |
| X-A | intraday | 5951 | 626.8011 | 1048.2672 | -421.4661 | 23.1558 | -5222.655 | -11072.111 |
| X-A | position | 551 | -83.7805 | 13.4471 | -97.2276 | 23.9564 | -275.6233 | -467.466 |
| X-B | GRID | 8387 | 1355.6213 | 1345.3095 | 10.3118 | 23.4768 | -5746.5975 | -12848.8163 |
| X-B | swing | 1885 | 812.5584 | 283.5952 | 528.9632 | 24.2971 | -248.3616 | -1309.2816 |
| X-B | intraday | 5951 | 626.6461 | 1048.2672 | -421.6211 | 23.1558 | -5222.81 | -11072.266 |
| X-B | position | 551 | -83.5832 | 13.4471 | -97.0303 | 24.1379 | -275.4259 | -467.2687 |
| X-C | GRID | 8387 | 200.1224 | 1345.3095 | -1145.187 | 26.2668 | -6902.0964 | -14004.3151 |
| X-C | swing | 1885 | 486.219 | 283.5952 | 202.6238 | 26.6313 | -574.701 | -1635.621 |
| X-C | intraday | 5951 | -212.547 | 1048.2672 | -1260.8142 | 26.0628 | -6062.0031 | -11911.4591 |
| X-C | position | 551 | -73.5496 | 13.4471 | -86.9966 | 27.2232 | -265.3923 | -457.235 |
| X-D | GRID | 8387 | 777.8718 | 1345.3095 | -567.4376 | 24.8957 | -6324.347 | -13426.5657 |
| X-D | swing | 1885 | 649.3887 | 283.5952 | 365.7935 | 25.5703 | -411.5313 | -1472.4513 |
| X-D | intraday | 5951 | 207.0495 | 1048.2672 | -841.2177 | 24.6009 | -5642.4065 | -11491.8626 |
| X-D | position | 551 | -78.5664 | 13.4471 | -92.0135 | 25.7713 | -270.4091 | -462.2518 |

Actual book, gross basis, for reference:

| scope | n | Σ r_0x | win rate % (0×) |
|---|---|---|---|
| GRID | 8387 | 1345.3095 | 25.0984 |
| swing | 1885 | 283.5952 | 23.6074 |
| intraday | 5951 | 1048.2672 | 25.6932 |
| position | 551 | 13.4471 | 23.775 |

## R2 — V-cohort P&L

**Discriminator.** V-initiated campaign = campaign whose lowest-seq fill tranche is a V. V identified per-tranche by EXIT.shadow.ladder_unthrottled_grade == 'V' (shadows.py:240 sets it to 'V' iff Tranche.kind == 'V'; kind is not otherwise journaled -- ENTRY_FILL covers both R1 and V). Checked by F8 = 45.

| scope | campaigns | Σ 0× | Σ 1× | Σ 2× | expectancy 1× | 95% CI | win rate % | strip-best Σ 1× |
|---|---|---|---|---|---|---|---|---|
| GRID | 45 | 2.5685 | -13.1918 | -28.9521 | -0.2932 | [-0.6315, 0.0316] | 31.1111 | -15.9327 |
| swing | 17 | 0.9588 | -3.1774 | -7.3136 | -0.1869 | [-0.5829, 0.2724] | 35.2941 | -5.9184 |
| intraday | 25 | 2.1542 | -9.301 | -20.7563 | -0.372 | [-0.8903, 0.1195] | 28.0 | -11.5739 |
| position | 3 | -0.5445 | -0.7133 | -0.8822 | -0.2378 | [-0.8242, 0.3799] | 33.3333 | -1.0933 |

| quantity | value |
|---|---|
| V campaigns | 45 |
| share of campaigns % | 1.3021 |
| Σ wins (grid) | 1768.1509 |
| V Σ wins | 10.5717 |
| **V share of Σwins %** | **0.5979** |
| Σ losses (grid) | -7525.0602 |
| V Σ losses | -23.7634 |
| V share of Σlosses % | 0.3158 |

Top-5 V campaigns by cell-R:

| campaign | cell-R 1× | tranches |
|---|---|---|
| BTCUSDT_swing#c201 | 2.741 | 3 |
| ZECUSDT_intraday#c549 | 2.2728 | 3 |
| ZECUSDT_intraday#c607 | 1.9628 | 1 |
| BTCUSDT_intraday#c77 | 1.6835 | 1 |
| JTOUSDT_swing#c16 | 0.6342 | 3 |

## R3 — MFE-before-death distributions

> **Purpose.** Raw material for FITTING a profit-arming threshold instead of guessing +1R.

**Population:** tranches that exited at a GROSS loss (r_0x < 0) — n = 6,281.  **Deciles of:** mfe_r (per-unit R), numpy.percentile linear interpolation, 10th..90th.

**Stop class** (field lens): EXIT row `stop` (= the fill level) vs ENTRY row `stop` (= stop_at_entry) for the same `tranche_id`. `no_stop_row` = non-stop exits (failure_x / opposite_cross / campaign_died), which journal `stop = null` (replay.py:191) and therefore have no stop class.

> **Structural note.** The 'ratcheted_ge_BE' class is EMPTY BY CONSTRUCTION for this population, not by accident: a stop resting at or beyond the entry fill on the trade's side cannot produce a gross loss when it is the exit level (gross P&L is measured at raw prices, before the costs that r_0x adds back). Any tranche whose stop reached breakeven and then filled leaves this population by definition. Read the absence as a tautology of the population filter, NOT as evidence that the ratchet never reaches breakeven.

### Marginal by stop class

| stop class | n | Σ cell-R 1× | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| initial | 5711 | -4450.32 | 0.0 | 0.0 | 0.0169 | 0.1286 | 0.2856 | 0.4636 | 0.7458 | 1.2003 | 2.0369 |
| ratcheted_below_BE | 563 | -233.4798 | 0.1339 | 0.3411 | 0.4997 | 0.6743 | 0.837 | 1.0433 | 1.2774 | 1.6187 | 2.3328 |
| no_stop_row | 7 | -2.3148 | 0.0 | 0.0106 | 0.0423 | 0.0615 | 0.0744 | 0.6803 | 1.1222 | 1.2362 | 1.707 |

### Full grid — stop class × mandate × grade

| stop class | mandate | grade | n | Σ cell-R 1× | Σ cell-R 0× | MFE med | D1 | D2 | D3 | D4 | D5 | D6 | D7 | D8 | D9 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| initial | swing | A+ | 21 | -19.9682 | -8.5765 | 0.1114 | 0.0 | 0.0 | 0.0 | 0.0484 | 0.1114 | 0.1676 | 0.5875 | 1.2211 | 2.206 |
| initial | swing | A | 488 | -379.976 | -211.1052 | 0.3882 | 0.0 | 0.0061 | 0.0983 | 0.223 | 0.3882 | 0.577 | 0.8482 | 1.3975 | 2.2138 |
| initial | swing | B | 613 | -408.8836 | -202.3281 | 0.4235 | 0.0 | 0.0463 | 0.1319 | 0.2723 | 0.4235 | 0.5939 | 0.8608 | 1.3107 | 2.3509 |
| initial | intraday | A+ | 29 | -22.1393 | -11.9384 | 0.2915 | 0.0 | 0.0 | 0.0 | 0.0283 | 0.2915 | 0.3563 | 0.763 | 1.2658 | 2.4562 |
| initial | intraday | A | 1321 | -1198.2002 | -497.0197 | 0.1998 | 0.0 | 0.0 | 0.0 | 0.0621 | 0.1998 | 0.3766 | 0.6272 | 0.9629 | 1.8769 |
| initial | intraday | B | 2102 | -1545.0626 | -601.3904 | 0.1868 | 0.0 | 0.0 | 0.0 | 0.0536 | 0.1868 | 0.3658 | 0.5829 | 1.011 | 1.6318 |
| initial | position | A+ | 5 | -2.9667 | -2.3607 | 0.5001 | 0.0265 | 0.0391 | 0.1363 | 0.3182 | 0.5001 | 0.5877 | 0.6753 | 1.1699 | 2.0713 |
| initial | position | A | 147 | -109.1014 | -65.5251 | 0.5235 | 0.0184 | 0.127 | 0.2506 | 0.3582 | 0.5235 | 0.8047 | 1.2887 | 1.733 | 3.2666 |
| initial | position | B | 177 | -96.7512 | -64.9357 | 0.4419 | 0.0 | 0.0886 | 0.1908 | 0.2999 | 0.4419 | 0.6336 | 0.9118 | 1.2287 | 2.0385 |
| ratcheted_below_BE | swing | A+ | 3 | -0.8148 | -0.2359 | 0.8873 | 0.803 | 0.8241 | 0.8452 | 0.8662 | 0.8873 | 0.9079 | 0.9284 | 0.949 | 0.9696 |
| ratcheted_below_BE | swing | A | 58 | -25.59 | -11.8864 | 0.9616 | 0.2224 | 0.3819 | 0.481 | 0.7328 | 0.9616 | 1.1774 | 1.3504 | 1.4341 | 2.1636 |
| ratcheted_below_BE | swing | B | 74 | -21.4482 | -10.268 | 1.019 | 0.3436 | 0.4961 | 0.7047 | 0.8747 | 1.019 | 1.1794 | 1.4528 | 1.7147 | 2.3649 |
| ratcheted_below_BE | intraday | A+ | 3 | -0.8457 | -0.698 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.3756 | 0.7513 | 1.1269 | 1.5026 |
| ratcheted_below_BE | intraday | A | 144 | -82.1344 | -29.7662 | 0.7584 | 0.0927 | 0.3237 | 0.4334 | 0.6125 | 0.7584 | 1.0007 | 1.2796 | 1.6614 | 2.5766 |
| ratcheted_below_BE | intraday | B | 202 | -77.7578 | -28.5016 | 0.7455 | 0.1268 | 0.2966 | 0.4372 | 0.6043 | 0.7455 | 0.9711 | 1.0612 | 1.4156 | 1.9775 |
| ratcheted_below_BE | position | A+ | 1 | -0.2138 | -0.0667 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 | 0.8313 |
| ratcheted_below_BE | position | A | 16 | -5.6578 | -3.4809 | 0.992 | 0.5941 | 0.6946 | 0.7824 | 0.8636 | 0.992 | 1.1954 | 1.4076 | 1.6062 | 1.9914 |
| ratcheted_below_BE | position | B | 16 | -3.5388 | -2.0565 | 1.6322 | 0.527 | 0.6318 | 1.1572 | 1.4913 | 1.6322 | 1.7882 | 1.8767 | 1.999 | 2.2229 |
| no_stop_row | swing | B | 1 | -0.2635 | -0.122 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 | 1.2743 |
| no_stop_row | intraday | B | 3 | -1.2369 | -0.3169 | 1.0842 | 0.2168 | 0.4337 | 0.6505 | 0.8674 | 1.0842 | 1.3386 | 1.593 | 1.8474 | 2.1017 |
| no_stop_row | position | A | 1 | -0.4946 | -0.1902 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |

## R4 — Harvest-doctrine timing test

**Population:** tranches with mfe_r >= +1R that exited at a GROSS loss (r_0x < 0) — n = **1,581**.

**Route taken.** TPW IS journaled as an event row (evt='TPW'), but those rows are per-cell/per-bar and carry no tranche_id, so they do not answer 'before THIS tranche's exit'. The per-tranche answer is journaled on the EXIT row as engagement_flags.tpw_before_exit / .ext_before_exit (shadows.py:257-260) -- that is the route taken. The exit_XB fallback was NOT needed for the TPW count; it is used only to recover R-at-first-trigger (see below).

> **⚠ READ THIS BEFORE THE TABLE.** THE TWO FLAGS DO NOT MEASURE THE SAME WINDOW, despite their paired names. (a) tpw_before_exit derives from Tranche.first_tpw_i, which trading.py:412-415 sets ONLY for tranches in open_tranches at the close of the TPW bar -- so it is genuinely 'while THIS tranche was open'. STRICT, answers the question as asked. (b) ext_before_exit derives from shadows.py:190-194, whose loop is `for j in range(tr.fill_i, last + 1)` with last = camp_end -- the CAMPAIGN-DEATH bar, NOT this tranche's exit bar (the engine's own comment says 'within the campaign'). It is therefore true whenever an extension occurred anywhere between this tranche's fill and campaign death, INCLUDING after this tranche was already stopped out. It is misnamed: it reads 'ext_before_CAMPAIGN_DEATH'. The strict 'before their exit' reading is NOT computable -- see partial below.

| scope | n | TPW before **exit** (strict) | TPW % | ext ≥2·ATR before **campaign death** (loose) | ext % |
|---|---|---|---|---|---|
| GRID | 1581 | 2 | 0.1265 | 1340 | 84.7565 |
| swing | 441 | 0 | 0.0 | 357 | 80.9524 |
| intraday | 1006 | 0 | 0.0 | 876 | 87.0775 |
| position | 134 | 2 | 1.4925 | 107 | 79.8507 |

The two count columns are **not comparable** — the first is windowed on the tranche's own life, the second on the campaign's. An `either` column would mix windows and is deliberately omitted.

**Independent cross-check on the TPW result** (computed from raw row timestamps, not the flag): of the 2,999 `TPW` event rows in the scored partition, only **16** fall inside an open same-direction tranche window at all. The flag and the timestamp scan agree — **TPW essentially never fires while the book is positioned**, so a TPW-armed harvest rule would almost never trigger on this run.

### Extension, strict 'before their exit' reading — **PARTIAL**

> NOT COMPUTABLE from journaled fields. The extension's bar index (ext_i, shadows.py:190-194) is never journaled, and the only journaled flag (engagement_flags.ext_before_exit) is evaluated over [fill_i, camp_end] rather than [fill_i, exit_i], so it cannot be narrowed to 'before this tranche's exit' after the fact. MISSING FIELD: either the trigger bar index ('ext_i_offset', bars from fill) or a correctly-windowed boolean computed over [fill_i, exit_i]. ROW TYPE it would live on: the EXIT row, inside engagement_flags alongside the existing (mis-windowed) flag. No estimate substituted. The n_ext_recoverable count below is a genuine LOWER BOUND on the strict reading -- it counts only rows whose extension partial actually banked before the X-A shadow exit.

### Median MFE at the first trigger — **PARTIAL**

> NOT COMPUTABLE from journaled fields. mfe_r on the EXIT row is the tranche's WHOLE-LIFE maximum favorable excursion (shadows.py:167), not its value at the trigger bar; the trigger bar index (tpw_i / ext_i, shadows.py:188-193) is never journaled. MISSING FIELD: an MFE-at-trigger column -- e.g. 'mfe_at_tpw_r' and 'mfe_at_ext_r'. ROW TYPE it would live on: the EXIT row (alongside mfe_r / give_back_r), or equivalently a per-tranche TPW event row carrying tranche_id + running mfe_r. No estimate substituted.

**What IS recoverable** (reported instead, clearly labelled — not a substitute estimate for the above):

per-unit R realized at the open AFTER the first trigger, inverted from the shadow blend: tpw_r = 2*exit_XB - exit_XA ; ext_r = 2*exit_XC - exit_XA. This is R AT the trigger, NOT MFE at the trigger.

| scope | n (TPW recoverable) | median R at 1st TPW | n (ext recoverable) | median R at 1st ext |
|---|---|---|---|---|
| GRID | 2 | 0.3323 | 359 | 1.4922 |
| swing | 0 |  | 62 | 1.8918 |
| intraday | 0 |  | 275 | 1.4209 |
| position | 2 | 0.3323 | 22 | 2.0331 |

## R5 — Shaken-out, per exit event

> **Purpose.** C6's re-entry trigger needs the per-EVENT denominator, not the per-tranche one.

**Resumption definition.** postexit_cont_20 >= 1.0 (per-unit R at exactly +20 exec bars after the exit). NOTE: only postexit_cont_{1,5,20} are journaled, so this is the value AT bar 20, not the max WITHIN 20 bars -- a strict 'within' reading is not computable from journaled fields.

**Event key.** (cell_id, dir, ts_open) over stop/stop_gap EXIT rows. per-unit quantities (postexit_cont_20) differ across tranches in one event because unit_risk is per-tranche; the event's lowest-seq tranche is the representative.

| basis | n | resumed ≥1R within 20b | resumed % | forfeited-continuation pool (cell-R, 10R/unit cap) | median postexit_cont_20 |
|---|---|---|---|---|---|
| per-tranche | 8365 | 2899 | 34.6563 | 4429.1503 | 0.2117 |
| per-event | 7057 | 2461 | 34.8732 | 4395.1405 | 0.22 |

Mean tranches per exit event: **1.1853**.

| mandate | tranches | tranches resumed | events | events resumed | events resumed % | forfeited pool (per-event, cell-R) |
|---|---|---|---|---|---|---|
| swing | 1880 | 620 | 1592 | 536 | 33.6683 | 1036.531 |
| intraday | 5935 | 2093 | 5003 | 1768 | 35.3388 | 3056.4354 |
| position | 550 | 186 | 462 | 157 | 33.9827 | 302.1742 |

## R6 — Zone × stage cross-tab

> **Purpose.** Tests P-R6.

**Note.** Counts are over ALL ENTRY_FILL/ADD_FILL rows. Expectancy and sum cell-R use the joined EXIT row; fills whose EXIT is buffered (campaign open at data end) contribute to the count but not to R. Fills = 8,415; without a joined EXIT = 28.

### direction = both

| zone|stage | n | n w/ exit | Σ cell-R 1× | Σ cell-R 0× | expectancy 1× |
|---|---|---|---|---|---|
| Z1|stage1 | 3144 | 3132 | -1992.5733 | 461.3842 | -0.6362 |
| Z1|stage2 | 2665 | 2658 | -2380.6787 | 636.2255 | -0.8957 |
| Z2|stage1 | 817 | 812 | -469.6736 | 82.0542 | -0.5784 |
| Z3|stage2 | 996 | 996 | -681.2009 | 92.6317 | -0.6839 |
| -|stage1 | 415 | 414 | -150.5355 | 17.8338 | -0.3636 |
| -|stage2 | 378 | 375 | -82.2473 | 55.1801 | -0.2193 |

### direction = long

| zone|stage | n | n w/ exit | Σ cell-R 1× | Σ cell-R 0× | expectancy 1× |
|---|---|---|---|---|---|
| Z1|stage1 | 1499 | 1498 | -1010.6906 | 243.6099 | -0.6747 |
| Z1|stage2 | 1376 | 1375 | -1222.0867 | 275.4864 | -0.8888 |
| Z2|stage1 | 366 | 366 | -206.832 | 67.0097 | -0.5651 |
| Z3|stage2 | 528 | 528 | -308.6418 | 4.7605 | -0.5845 |
| -|stage1 | 212 | 212 | -45.0223 | 43.3056 | -0.2124 |
| -|stage2 | 179 | 178 | -68.3391 | 0.3937 | -0.3839 |

### direction = short

| zone|stage | n | n w/ exit | Σ cell-R 1× | Σ cell-R 0× | expectancy 1× |
|---|---|---|---|---|---|
| Z1|stage1 | 1645 | 1634 | -981.8827 | 217.7742 | -0.6009 |
| Z1|stage2 | 1289 | 1283 | -1158.592 | 360.739 | -0.903 |
| Z2|stage1 | 451 | 446 | -262.8416 | 15.0444 | -0.5893 |
| Z3|stage2 | 468 | 468 | -372.5591 | 87.8712 | -0.7961 |
| -|stage1 | 203 | 202 | -105.5131 | -25.4718 | -0.5223 |
| -|stage2 | 199 | 197 | -13.9082 | 54.7864 | -0.0706 |

### per mandate

| mandate | zone|stage | n | Σ cell-R 1× | expectancy 1× |
|---|---|---|---|---|
| swing | Z1|stage1 | 700 | -327.4464 | -0.4711 |
| swing | Z1|stage2 | 613 | -234.8602 | -0.385 |
| swing | Z2|stage1 | 163 | -91.1709 | -0.5593 |
| swing | Z3|stage2 | 241 | -165.6263 | -0.6872 |
| swing | -|stage1 | 91 | -5.1391 | -0.0565 |
| swing | -|stage2 | 86 | 46.918 | 0.552 |
| intraday | Z1|stage1 | 2226 | -1626.85 | -0.7312 |
| intraday | Z1|stage2 | 1869 | -2075.3874 | -1.1116 |
| intraday | Z2|stage1 | 605 | -364.396 | -0.6023 |
| intraday | Z3|stage2 | 686 | -484.0731 | -0.7056 |
| intraday | -|stage1 | 300 | -130.5198 | -0.4351 |
| intraday | -|stage2 | 269 | -119.9625 | -0.4476 |
| position | Z1|stage1 | 218 | -38.2769 | -0.1806 |
| position | Z1|stage2 | 183 | -70.4311 | -0.3891 |
| position | Z2|stage1 | 49 | -14.1067 | -0.3206 |
| position | Z3|stage2 | 69 | -31.5015 | -0.4565 |
| position | -|stage1 | 24 | -14.8766 | -0.6468 |
| position | -|stage2 | 23 | -9.2029 | -0.4183 |

**Stage-2 rows with zone = Z2: 0.** Z2 entries = 817; Z2 & stage-1 = 817 (**100.0%**).

### Zone × stage occupancy — the cross-tab is nearly degenerate

| zone | n | stage 1 | stage 2 |
|---|---|---|---|
| Z1 | 5809 | 3144 | 2665 |
| Z2 | 817 | 817 | 0 |
| Z3 | 996 | 0 | 996 |
| - | 793 | 415 | 378 |

> **Finding.** The cross-tab is NEARLY DEGENERATE: zone and stage are not independent in this run. Z2 fills are 100% stage-1 (0 stage-2) and Z3 fills are 100% stage-2 (0 stage-1) -- each of those zones occupies exactly ONE stage, so 2 of the 6 Z1/Z2/Z3 x stage cells are structurally empty rather than merely sparse. Only Z1 (and the no-zone '-' bucket) populate both stages. P-R6 is therefore CONFIRMED trivially at 100%, not marginally at >=95%: the prediction tested a coupling that appears to be enforced upstream, not a tendency. Zones with a single occupied stage: Z2, Z3. Anyone reading a Z2-vs-Z3 expectancy difference as a ZONE effect is also reading a STAGE effect -- the two are confounded here and cannot be separated from these journals.

## R7 — Reject funnel, split by layer

**Layer discriminator.** REJECT row whose tranche_id starts with 'trade_' is a TRADING-layer reject (replay.py:228); otherwise SIGNAL-layer (subkey 'prime'/'confirm').

> **Naming.** Contract §6 R7 calls the tranche ceiling 'tranche_cap'; the engine emits it as reject_reason='max_tranches' (trading.py:459). Same gate -- reported under both names.

| layer | rows |
|---|---|
| signal | 355,236 |
| trading | 290,791 |
| all REJECT rows | 646,027 |

### signal layer

| reject_reason | GRID | swing | intraday | position |
|---|---|---|---|---|
| `no_zone` | 229963 | 37783 | 179099 | 13081 |
| `bar_range` | 44771 | 5029 | 38409 | 1333 |
| `ribbon_sep` | 43917 | 8465 | 32888 | 2564 |
| `c_gate_no_zone` | 21091 | 3188 | 16803 | 1100 |
| `cooldown` | 15451 | 2559 | 12053 | 839 |
| `structure` | 32 | 25 | 7 | 0 |
| `c_gate_structure` | 11 | 9 | 2 | 0 |

### trading layer

| reject_reason | GRID | swing | intraday | position |
|---|---|---|---|---|
| `max_tranches` | 145749 | 32568 | 102974 | 10207 |
| `not_positioned` | 69082 | 11008 | 54762 | 3312 |
| `halted_week` | 41703 | 466 | 41221 | 16 |
| `gap_through_stop` | 27440 | 3785 | 22774 | 881 |
| `halted_day` | 6099 | 121 | 5962 | 16 |
| `add_ineligible` | 716 | 180 | 482 | 54 |
| `campaign_died_same_bar` | 1 | 0 | 1 | 0 |
| `v_already_positioned` | 1 | 1 | 0 | 0 |

### Load-bearing counts

| quantity | count | why it matters |
|---|---|---|
| `r_cap` (F9) | 0 | 0 ⇒ the signal layer is NOT capping PRIMEs |
| `tranche_cap` / `max_tranches` | **145,749** | exactly how many adds the 3-tranche ceiling turned away — sizes the aggressive-mode decision BEFORE any run is spent |
| `add_ineligible` | 716 | breakeven doctrine |
| `no_zone` | 229,963 | sizes VS-Z3 |
| `ribbon_sep` | 43,917 | sizes VS-Z3 |

## R8 — Expectancy by zone, including Z3

> **Gap closed.** Report 1 published Z2 vs Z1 and never published Z3. Z3 is the governor 89-200 band retest cohort and the operator's stated primary structural setup. Gap closed here.

### Tranche level

| zone | scope | n | Σ cell-R 0× | Σ cell-R 1× | Σ cell-R 2× | net R/unit | 95% CI | win rate % |
|---|---|---|---|---|---|---|---|---|
| Z1 | GRID | 5790 | 1097.6096 | -4373.252 | -9844.1136 | -1.5847 | [-2.0069, -1.2553] | 16.1313 |
| Z1 | swing | 1305 | 167.9328 | -562.3066 | -1292.546 | -0.9053 | [-1.2318, -0.5841] | 17.5479 |
| Z1 | intraday | 4092 | 873.9934 | -3702.2374 | -8278.4683 | -1.8997 | [-2.4803, -1.453] | 15.1026 |
| Z1 | position | 393 | 55.6834 | -108.7079 | -273.0992 | -0.5607 | [-1.0941, 0.0199] | 22.1374 |
| Z2 | GRID | 812 | 82.0542 | -469.6736 | -1021.4014 | -1.3807 | [-1.8132, -0.9971] | 16.8719 |
| Z2 | swing | 163 | 42.8312 | -91.1709 | -225.1729 | -1.224 | [-2.7759, -0.0037] | 15.9509 |
| Z2 | intraday | 605 | 47.642 | -364.396 | -776.434 | -1.4595 | [-1.8638, -1.0859] | 16.8595 |
| Z2 | position | 44 | -8.419 | -14.1067 | -19.7945 | -0.878 | [-1.1131, -0.6307] | 20.4545 |
| Z3 | GRID | 996 | 92.6317 | -681.2009 | -1455.0336 | -1.4127 | [-2.0712, -0.9499] | 17.0683 |
| Z3 | swing | 241 | -10.3486 | -165.6263 | -320.904 | -1.4184 | [-2.0835, -0.8752] | 14.9378 |
| Z3 | intraday | 686 | 119.071 | -484.0731 | -1087.2173 | -1.4554 | [-2.4157, -0.8358] | 18.0758 |
| Z3 | position | 69 | -16.0906 | -31.5015 | -46.9124 | -0.9673 | [-1.2146, -0.7015] | 14.4928 |

Other zone values on EXIT rows: `{"-": 789}`

### Campaign level, by the initiating tranche's zone

| zone | scope | campaigns | Σ 1× | expectancy 1× | 95% CI | win rate % | strip-best Σ 1× |
|---|---|---|---|---|---|---|---|
| Z1 | GRID | 2411 | -4456.794 | -1.8485 | [-2.362, -1.4391] | 11.1157 | -4571.2459 |
| Z1 | swing | 511 | -540.4164 | -1.0576 | [-1.5798, -0.4121] | 10.7632 | -654.8683 |
| Z1 | intraday | 1750 | -3793.9682 | -2.168 | [-2.8466, -1.6445] | 10.7429 | -3847.1601 |
| Z1 | position | 150 | -122.4095 | -0.8161 | [-1.4728, -0.0664] | 16.6667 | -158.5497 |
| Z2 | GRID | 496 | -545.3385 | -1.0995 | [-1.4004, -0.8309] | 8.0645 | -567.8803 |
| Z2 | swing | 101 | -60.4815 | -0.5988 | [-1.4513, 0.1577] | 12.8713 | -79.1446 |
| Z2 | intraday | 367 | -460.9175 | -1.2559 | [-1.588, -0.96] | 7.0845 | -483.4593 |
| Z2 | position | 28 | -23.9394 | -0.855 | [-1.0962, -0.6188] | 3.5714 | -24.5652 |
| Z3 | GRID | 504 | -741.585 | -1.4714 | [-2.1474, -0.9804] | 13.4921 | -768.0483 |
| Z3 | swing | 116 | -173.2495 | -1.4935 | [-2.3363, -0.8823] | 13.7931 | -182.4309 |
| Z3 | intraday | 358 | -537.0021 | -1.5 | [-2.4334, -0.8546] | 14.2458 | -563.4654 |
| Z3 | position | 30 | -31.3335 | -1.0444 | [-1.4609, -0.5881] | 3.3333 | -34.7696 |

Campaigns whose initiating zone is not Z1/Z2/Z3: `{"-": 45}`

## R9 — Risk-mode first-order table (defensive + neutral only)

> **Caveat.** FIRST-ORDER ONLY. Removing or re-weighting a tranche does not change the stop path (the ratchet is signal-layer and independent of fills), but it DOES change the equity path, the 1R campaign rail, and the halt calendar -- all of which gate admission. Faithful measurement is S-1's job.

> **Aggressive.** Aggressive mode is OUT OF SCOPE here: it creates tranches that do not exist in these journals. It requires a Tier-C run. R9 covers defensive and neutral only.

| column | filter |
|---|---|
| `neutral` | the live line as journaled (control) |
| `def_c1_only` | drop tranches with abs(px_fill - stop) / atr_exec (both from the ENTRY row) < 0.5 |
| `def_c1_grade` | def_c1_only + drop grade not in {A, A+} |
| `def_full` | def_c1_grade + size_r x1.5 if retr>=0.5, x0.5 if retr<0.25, x1.0 otherwise |

| column | scope | campaigns | tranches kept | Σ 0× | Σ 1× | Σ 2× | expectancy 1× | 95% CI | win rate % | strip-best Σ 1× |
|---|---|---|---|---|---|---|---|---|---|---|
| `neutral` | GRID | 3456 | 8387 | 1345.3095 | -5756.9093 | -12859.1281 | -1.6658 | [-2.0257, -1.3613] | 11.2847 | -5871.3612 |
| `neutral` | swing | 745 | 1885 | 283.5952 | -777.3248 | -1838.2448 | -1.0434 | [-1.44, -0.5726] | 12.0805 | -891.7767 |
| `neutral` | intraday | 2500 | 5951 | 1048.2672 | -4801.1889 | -10650.6449 | -1.9205 | [-2.3896, -1.5335] | 10.88 | -4854.3808 |
| `neutral` | position | 211 | 551 | 13.4471 | -178.3957 | -370.2384 | -0.8455 | [-1.3269, -0.3091] | 13.2701 | -214.5359 |
| `def_c1_only` | GRID | 3426 | 7667 | 426.3363 | -2264.2198 | -4954.7758 | -0.6609 | [-0.7646, -0.5424] | 10.8873 | -2378.6716 |
| `def_c1_only` | swing | 741 | 1712 | 184.5794 | -225.7699 | -636.1193 | -0.3047 | [-0.6071, 0.1027] | 12.5506 | -340.2218 |
| `def_c1_only` | intraday | 2474 | 5458 | 243.2424 | -1968.6662 | -4180.5747 | -0.7957 | [-0.8954, -0.6893] | 10.1455 | -2019.5064 |
| `def_c1_only` | position | 211 | 497 | -1.4855 | -69.7836 | -138.0818 | -0.3307 | [-0.6522, 0.1204] | 13.7441 | -105.9239 |
| `def_c1_grade` | GRID | 1483 | 2752 | 180.7474 | -892.0895 | -1964.9264 | -0.6015 | [-0.7254, -0.4652] | 17.06 | -933.339 |
| `def_c1_grade` | swing | 338 | 705 | 82.2316 | -106.1743 | -294.5803 | -0.3141 | [-0.6285, 0.0742] | 21.3018 | -147.4239 |
| `def_c1_grade` | intraday | 1056 | 1854 | 76.1222 | -776.6295 | -1629.3812 | -0.7354 | [-0.8538, -0.6125] | 15.3409 | -794.7171 |
| `def_c1_grade` | position | 89 | 193 | 22.3935 | -9.2857 | -40.9649 | -0.1043 | [-0.7298, 0.8855] | 21.3483 | -45.4259 |
| `def_full` | GRID | 1483 | 2752 | 93.4099 | -592.3839 | -1278.1777 | -0.3994 | [-0.4815, -0.3093] | 17.532 | -616.1525 |
| `def_full` | swing | 338 | 705 | 44.095 | -90.275 | -224.645 | -0.2671 | [-0.486, -0.0075] | 21.8935 | -114.0436 |
| `def_full` | intraday | 1056 | 1854 | 43.7901 | -485.3978 | -1014.5857 | -0.4597 | [-0.539, -0.3774] | 15.625 | -503.4855 |
| `def_full` | position | 89 | 193 | 5.5248 | -16.7111 | -38.947 | -0.1878 | [-0.5451, 0.3276] | 23.5955 | -34.4702 |

| note | value |
|---|---|
| tranches_with_null_atr_exec_on_entry | 0 |
| null_atr_handling | kept (cannot evaluate C1); count reported |
| tranches_with_null_retr | 1027 |
| null_retr_handling | weight x1.0 |
| reweight_semantics | realized_r is linear in size_r (pnl scales with qty, qty scales with size_r at fixed unit risk), so a size tilt scales the tranche's cell-R, its cost, and hence r_0x/r_2x by the same weight. |

## R10 — Fee Stage A (maker-entry bound)

> **Caveat.** This is the OPTIMISTIC bound. It assumes every entry fills as a maker and none is missed. Chase orders miss most when price runs away immediately -- which is disproportionately the character of the entries that become tail campaigns. The bound is a CEILING, not an estimate.

**Formula.** `cost_maker = cost_total - entry_fee*(3/5) - entry_slippage ; r_maker = realized_r + (cost_total - cost_maker)/one_r`  
**Assumption.** maker entries 2 bps/side, taker stops 5 bps/side (entry fee scaled 5->2 bps by removing 3/5 of it); fills otherwise unchanged

**Ceiling on ALL execution improvement — the 0× line: 1345.3095.** No execution change can beat it; it is the book with every cost removed.

| scope | n | Σ 1× actual | Σ maker-entry basis | Δ vs 1× |
|---|---|---|---|---|
| GRID | 8387 | -5756.9093 | -2940.6248 | 2816.2845 |
| swing | 1885 | -777.3248 | -375.932 | 401.3928 |
| intraday | 5951 | -4801.1889 | -2458.0874 | 2343.1015 |
| position | 551 | -178.3957 | -106.6054 | 71.7902 |

Cost split, USD (before → after):

| scope | fees before | fees after | slip before | slip after | funding before | funding after | total before | total after |
|---|---|---|---|---|---|---|---|---|
| GRID | 70052.498 | 49037.264 | 39906.0414 | 19952.898 | 316.704 | 316.704 | 110275.2434 | 69306.866 |
| swing | 20928.1398 | 14650.0372 | 13839.9191 | 6920.0535 | 171.0571 | 171.0571 | 34939.116 | 21741.1478 |
| intraday | 43922.6856 | 30745.8797 | 22660.4375 | 11330.0597 | 47.2148 | 47.2148 | 66630.3379 | 42123.1542 |
| position | 5201.6726 | 3641.3472 | 3405.6848 | 1702.7848 | 98.4321 | 98.4321 | 8705.7895 | 5442.5641 |

## Prediction scorecard (contract §7)

| # | prediction | prior | falsified if | verdict |
|---|---|---|---|---|
| P-R1 | X-A-family exits beat the actual book (gross basis) on swing AND position; ambiguous-to-negative on intraday | 70% | X-A loses on swing or position, or wins clearly on intraday | **FALSIFIED** |
| P-R2 | The 45 V campaigns are NOT disproportionately tail-carrying -- their share of sum(wins) < 3x their share of campaigns (< 3.9%) | 50% | V's share of sum(wins) >= 3.9% | **CONFIRMED** |
| P-R6 | >=95% of Z2-active entries carry stage = 1 | 85% | < 95% | **CONFIRMED** |
| P-R7 | tranche_cap rejects > 500 (aggressive mode is a real axis, not a non-event) | 60% | <= 500 | **CONFIRMED** |
| P-R9 | def_full remains NET NEGATIVE at 1x -- no defensive bundle flips the grid sign in-sample on mined data | 60% | def_full 1x >= 0 | **CONFIRMED** |

- **P-R1 — FALSIFIED.** Evidence: `{"xa_delta_swing_0x": 528.9161, "xa_delta_position_0x": -97.2276, "xa_delta_intraday_0x": -421.4661}`
- **P-R2 — CONFIRMED.** Evidence: `{"v_share_of_wins_pct": 0.5979, "v_share_of_campaigns_pct": 1.3021, "threshold_pct": 3.9}`
- **P-R6 — CONFIRMED.** Evidence: `{"z2_entries": 817, "z2_stage1": 817, "z2_stage1_pct": 100.0, "z2_stage2": 0}`
- **P-R7 — CONFIRMED.** Evidence: `{"tranche_cap_rejects": 145749, "threshold": 500, "engine_reason_name": "max_tranches"}`
- **P-R9 — CONFIRMED.** Evidence: `{"def_full_sum_1x": -592.3839}`

**Not scored here** (S-1 items, carried from Report 2 unchanged): P-S1a (de-ratchet / loosening-while-open events = 0), P-S1b (non-advancement explains >= 1/3 of +1R-to-loss round-trips).
