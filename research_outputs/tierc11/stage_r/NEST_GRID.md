as_of_last_closed_4h: 2026-09-25T00:00:00Z

# TIER-C11 · STAGE R · R3 NESTING GRID

## R3 · THE NEST ON THE BOOKS [L-R.5, AM-6] — Tier-E

Collar on every table below unless marked RECORD: tier = 'TIER-E' · selection_not_a_result = 'a SELECTION, not a result' · gates = 'nothing'.

SR-6 R3 INSTANTS [L-R.5, AM-6]: every CLOSE of the campaign's own lens from its arm close (entry close for a book without arming) through its exit stamp of record; plus the named events — arm, entry, harvest, bell, add, a close exit at their CLOSE; +1R and an intrabar exit (stop / tp) at the OPEN of their bar for the 4h books (latch bar = latch_1r_open_ms, exit = exit_event_ms: the books' UNWALKED 4h ride) — their close-stamped twins are labelled 'post-event' (instant kinds plus_1r_post_event / exit_post_event); a campaign OPEN at the pin (corridor_end) is stamped 'as_of_pin', never 'exit'. Each row's stamp_law names its rule. The nest is N.nest_at(symbol, instants, scale) — per L read at the last CLOSED bar of L at or before the instant.

SR-7 COINCIDENCE AT ENTRY (NEST_GRID): per lens L the category from L's two side flags — 'both' (coin_top and coin_bot), 'top', 'bot', 'none'; 'NA' for 1w (no lens above). Record rule = the live L+1 boundaries (coin_*); twin = with L+1's live memory lines (coin_*_mem).

Two lawful +1R stamps [L-R.5, AM-6; verifier MINOR-9] — each row's `stamp_law` names its rule: NEST_v6 / NEST_trg912 (the books' UNWALKED 4h ride) stamp +1R and a stop exit at the OPEN of their 4h bar; the nest-book door on a 1h-walked regbook (latch_1h_ms / exit_stamp_ms) stamps them at the close of the resolving 1h child (a parent-decided event on a walk-mismatch bar at the parent's OPEN). The same campaign can therefore carry a +1R instant 1–4 h apart in the two tables.

SCALE-IN-SAMPLE [L-R.2, AM-4]: a calibrated-scale range read at an instant <= the era cut (2024-06-30T23:59:59Z) is structurally IN-SAMPLE (the tuning pick saw those bars; a whole-tape fallback pick is in-sample at every instant; frozen 3.0 never is). Every row carries `lenses_read` (the lenses the cell consumes: L, and L+1 for a coincidence cell), their `pick_window` and `stability_changed_members` (first-half-of-tuning pick != tuning pick), `n_scale_in_sample` / `n_stability_changed` (the cell's entries whose read is in-sample / rides a stability-changed pick, on ANY consumed lens), and the HOLDOUT slice (entry close after the cut: n_holdout, mean_net_r_holdout, p_win_holdout, sum_net_r_holdout) — the causal slice of a tuning pick, printed beside every cell.

- NEST_v6.parquet: 19386 rows (5 assets, 200 campaigns) — rows by (scale, kind): calibrated/arm 200 · calibrated/bar_close 8632 · calibrated/bell 4 · calibrated/entry 200 · calibrated/exit 200 · calibrated/exit_post_event 196 · calibrated/harvest 55 · calibrated/plus_1r 103 · calibrated/plus_1r_post_event 103 · frozen3.0/arm 200 · frozen3.0/bar_close 8632 · frozen3.0/bell 4 · frozen3.0/entry 200 · frozen3.0/exit 200 · frozen3.0/exit_post_event 196 · frozen3.0/harvest 55 · frozen3.0/plus_1r 103 · frozen3.0/plus_1r_post_event 103
- NEST_trg912.parquet: 21416 rows (5 assets, 199 campaigns) — rows by (scale, kind): calibrated/arm 199 · calibrated/as_of_pin 1 · calibrated/bar_close 9626 · calibrated/bell 7 · calibrated/entry 199 · calibrated/exit 198 · calibrated/exit_post_event 191 · calibrated/harvest 63 · calibrated/plus_1r 112 · calibrated/plus_1r_post_event 112 · frozen3.0/arm 199 · frozen3.0/as_of_pin 1 · frozen3.0/bar_close 9626 · frozen3.0/bell 7 · frozen3.0/entry 199 · frozen3.0/exit 198 · frozen3.0/exit_post_event 191 · frozen3.0/harvest 63 · frozen3.0/plus_1r 112 · frozen3.0/plus_1r_post_event 112

### Honesty at ENTRY per (book, scale, lens) [L-R.2, AM-4] — the calibrated rows read a tuning-era pick: in-sample on every tuning-era entry

- v6 · calibrated · 1h: 123 of 200 entries read IN-SAMPLE; 115 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 77
- v6 · calibrated · 4h: 123 of 200 entries read IN-SAMPLE; 40 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 77
- v6 · calibrated · 12h: 123 of 200 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 77
- v6 · calibrated · 1d: 123 of 200 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 77
- v6 · calibrated · 1w: 200 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 77
- v6 · frozen3.0 · 1h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 77
- v6 · frozen3.0 · 4h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 77
- v6 · frozen3.0 · 12h: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 77
- v6 · frozen3.0 · 1d: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 77
- v6 · frozen3.0 · 1w: 0 of 200 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 77
- trg912 · calibrated · 1h: 132 of 199 entries read IN-SAMPLE; 114 on a stability-changed pick (1h: BTCUSDT,SOLUSDT,NEARUSDT); pick window 1h: tuning; holdout slice n 67
- trg912 · calibrated · 4h: 132 of 199 entries read IN-SAMPLE; 39 on a stability-changed pick (4h: NEARUSDT); pick window 4h: tuning; holdout slice n 67
- trg912 · calibrated · 12h: 132 of 199 entries read IN-SAMPLE; 123 on a stability-changed pick (12h: BTCUSDT,ETHUSDT,SOLUSDT); pick window 12h: tuning; holdout slice n 67
- trg912 · calibrated · 1d: 132 of 199 entries read IN-SAMPLE; 75 on a stability-changed pick (1d: BTCUSDT,SOLUSDT); pick window 1d: tuning; holdout slice n 67
- trg912 · calibrated · 1w: 199 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: whole-tape (fallback); holdout slice n 67
- trg912 · frozen3.0 · 1h: 0 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (1h: none); pick window 1h: frozen3.0; holdout slice n 67
- trg912 · frozen3.0 · 4h: 0 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (4h: none); pick window 4h: frozen3.0; holdout slice n 67
- trg912 · frozen3.0 · 12h: 0 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (12h: none); pick window 12h: frozen3.0; holdout slice n 67
- trg912 · frozen3.0 · 1d: 0 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (1d: none); pick window 1d: frozen3.0; holdout slice n 67
- trg912 · frozen3.0 · 1w: 0 of 199 entries read IN-SAMPLE; 0 on a stability-changed pick (1w: none); pick window 1w: frozen3.0; holdout slice n 67

### Frequency at ENTRY: state x coincidence, per lens (both books, both scales — calibrated = the scale of record, IN-SAMPLE on tuning-era entries; frozen3.0 = the causal twin — both coincidence rules)

| book | scale_kind | lens | coin_rule | state | coin_cat | n | n_entries | share | n_scale_in_sample | n_stability_changed | n_holdout | lenses_read | pick_window |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v6 | calibrated | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 4 | 3 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | IN_RANGE | bot | 17 | 200 | 0.0850 | 12 | 11 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | IN_RANGE | none | 96 | 200 | 0.4800 | 61 | 57 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | record | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | IN_RANGE | both | 4 | 200 | 0.0200 | 2 | 2 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 5 | 4 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 200 | 0.0950 | 14 | 12 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | IN_RANGE | none | 93 | 200 | 0.4650 | 58 | 55 | 35 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BULL_EXP | none | 38 | 200 | 0.1900 | 27 | 23 | 11 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 1h | mem_twin | BEAR_EXP | none | 36 | 200 | 0.1800 | 17 | 19 | 19 | 1h+4h | 1h: tuning; 4h: tuning |
| v6 | calibrated | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | IN_RANGE | bot | 12 | 200 | 0.0600 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | IN_RANGE | none | 112 | 200 | 0.5600 | 75 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | record | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | IN_RANGE | both | 9 | 200 | 0.0450 | 7 | 8 | 2 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | IN_RANGE | top | 8 | 200 | 0.0400 | 1 | 7 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 6 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | IN_RANGE | none | 111 | 200 | 0.5550 | 74 | 90 | 37 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BULL_EXP | none | 32 | 200 | 0.1600 | 20 | 25 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 4h | mem_twin | BEAR_EXP | none | 27 | 200 | 0.1350 | 15 | 22 | 12 | 4h+12h | 4h: tuning; 12h: tuning |
| v6 | calibrated | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | IN_RANGE | both | 6 | 200 | 0.0300 | 4 | 3 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | IN_RANGE | top | 4 | 200 | 0.0200 | 1 | 2 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 5 | 8 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | IN_RANGE | none | 80 | 200 | 0.4000 | 44 | 61 | 36 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | record | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | IN_RANGE | both | 7 | 200 | 0.0350 | 4 | 4 | 3 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 3 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 200 | 0.0750 | 8 | 10 | 7 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 39 | 54 | 33 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BULL_EXP | none | 58 | 200 | 0.2900 | 45 | 32 | 13 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 12h | mem_twin | BEAR_EXP | none | 39 | 200 | 0.1950 | 24 | 17 | 15 | 12h+1d | 12h: tuning; 1d: tuning |
| v6 | calibrated | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 200 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | IN_RANGE | none | 72 | 200 | 0.3600 | 72 | 26 | 34 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BULL_EXP | none | 77 | 200 | 0.3850 | 77 | 29 | 18 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1d | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 50 | 19 | 24 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | record | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | record | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | record | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | record | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | mem_twin | NONE | NA | 30 | 200 | 0.1500 | 30 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | mem_twin | IN_RANGE | NA | 43 | 200 | 0.2150 | 43 | 0 | 31 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | mem_twin | BULL_EXP | NA | 29 | 200 | 0.1450 | 29 | 0 | 19 | 1w | 1w: whole-tape (fallback) |
| v6 | calibrated | 1w | mem_twin | BEAR_EXP | NA | 98 | 200 | 0.4900 | 98 | 0 | 27 | 1w | 1w: whole-tape (fallback) |
| v6 | frozen3.0 | 1h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 6 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | IN_RANGE | none | 115 | 200 | 0.5750 | 0 | 0 | 42 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | record | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 1 | 200 | 0.0050 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 10 | 200 | 0.0500 | 0 | 0 | 7 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 2 | 200 | 0.0100 | 0 | 0 | 1 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 114 | 200 | 0.5700 | 0 | 0 | 41 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 41 | 200 | 0.2050 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 32 | 200 | 0.1600 | 0 | 0 | 11 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | record | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 1 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 3 | 200 | 0.0150 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 13 | 200 | 0.0650 | 0 | 0 | 10 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 73 | 200 | 0.3650 | 0 | 0 | 34 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 66 | 200 | 0.3300 | 0 | 0 | 19 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 40 | 200 | 0.2000 | 0 | 0 | 13 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| v6 | frozen3.0 | 12h | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | IN_RANGE | both | 5 | 200 | 0.0250 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | IN_RANGE | bot | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | record | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 6 | 200 | 0.0300 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 9 | 200 | 0.0450 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 8 | 200 | 0.0400 | 0 | 0 | 3 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 51 | 200 | 0.2550 | 0 | 0 | 25 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 76 | 200 | 0.3800 | 0 | 0 | 24 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 50 | 200 | 0.2500 | 0 | 0 | 17 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| v6 | frozen3.0 | 1d | record | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | record | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 200 | 0.0200 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 2 | 200 | 0.0100 | 0 | 0 | 2 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 200 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 200 | 0.2750 | 0 | 0 | 25 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 74 | 200 | 0.3700 | 0 | 0 | 19 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 200 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 64 | 200 | 0.3200 | 0 | 0 | 30 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | record | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | record | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | record | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | mem_twin | NONE | NA | 37 | 200 | 0.1850 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 200 | 0.1450 | 0 | 0 | 25 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 40 | 200 | 0.2000 | 0 | 0 | 20 | 1w | 1w: frozen3.0 |
| v6 | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 94 | 200 | 0.4700 | 0 | 0 | 32 | 1w | 1w: frozen3.0 |
| trg912 | calibrated | 1h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | IN_RANGE | both | 5 | 199 | 0.0251 | 3 | 3 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | IN_RANGE | top | 7 | 199 | 0.0352 | 5 | 5 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | IN_RANGE | bot | 17 | 199 | 0.0854 | 12 | 13 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | IN_RANGE | none | 93 | 199 | 0.4673 | 68 | 57 | 25 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BULL_EXP | none | 43 | 199 | 0.2161 | 26 | 19 | 17 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | record | BEAR_EXP | none | 34 | 199 | 0.1709 | 18 | 17 | 16 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | IN_RANGE | both | 5 | 199 | 0.0251 | 3 | 3 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | IN_RANGE | top | 8 | 199 | 0.0402 | 6 | 6 | 2 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | IN_RANGE | bot | 19 | 199 | 0.0955 | 14 | 14 | 5 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | IN_RANGE | none | 90 | 199 | 0.4523 | 65 | 55 | 25 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BULL_EXP | none | 43 | 199 | 0.2161 | 26 | 19 | 17 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 1h | mem_twin | BEAR_EXP | none | 34 | 199 | 0.1709 | 18 | 17 | 16 | 1h+4h | 1h: tuning; 4h: tuning |
| trg912 | calibrated | 4h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | IN_RANGE | both | 7 | 199 | 0.0352 | 6 | 6 | 1 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | IN_RANGE | top | 8 | 199 | 0.0402 | 4 | 6 | 4 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | IN_RANGE | bot | 12 | 199 | 0.0603 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | IN_RANGE | none | 100 | 199 | 0.5025 | 69 | 82 | 31 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BULL_EXP | none | 43 | 199 | 0.2161 | 27 | 36 | 16 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | record | BEAR_EXP | none | 29 | 199 | 0.1457 | 21 | 21 | 8 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | IN_RANGE | both | 7 | 199 | 0.0352 | 6 | 6 | 1 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | IN_RANGE | top | 9 | 199 | 0.0452 | 4 | 7 | 5 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | IN_RANGE | bot | 12 | 199 | 0.0603 | 5 | 11 | 7 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | IN_RANGE | none | 99 | 199 | 0.4975 | 69 | 81 | 30 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BULL_EXP | none | 43 | 199 | 0.2161 | 27 | 36 | 16 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 4h | mem_twin | BEAR_EXP | none | 29 | 199 | 0.1457 | 21 | 21 | 8 | 4h+12h | 4h: tuning; 12h: tuning |
| trg912 | calibrated | 12h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | IN_RANGE | both | 6 | 199 | 0.0302 | 4 | 2 | 2 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | IN_RANGE | top | 6 | 199 | 0.0302 | 2 | 3 | 4 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | IN_RANGE | bot | 13 | 199 | 0.0653 | 5 | 9 | 8 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | IN_RANGE | none | 63 | 199 | 0.3166 | 38 | 45 | 25 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BULL_EXP | none | 64 | 199 | 0.3216 | 53 | 42 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | record | BEAR_EXP | none | 47 | 199 | 0.2362 | 30 | 22 | 17 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | IN_RANGE | both | 8 | 199 | 0.0402 | 4 | 4 | 4 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | IN_RANGE | top | 10 | 199 | 0.0503 | 4 | 6 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | IN_RANGE | bot | 15 | 199 | 0.0754 | 9 | 11 | 6 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | IN_RANGE | none | 55 | 199 | 0.2764 | 32 | 38 | 23 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BULL_EXP | none | 64 | 199 | 0.3216 | 53 | 42 | 11 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 12h | mem_twin | BEAR_EXP | none | 47 | 199 | 0.2362 | 30 | 22 | 17 | 12h+1d | 12h: tuning; 1d: tuning |
| trg912 | calibrated | 1d | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | IN_RANGE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | IN_RANGE | top | 1 | 199 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | IN_RANGE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | IN_RANGE | none | 64 | 199 | 0.3216 | 64 | 22 | 27 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BULL_EXP | none | 79 | 199 | 0.3970 | 79 | 34 | 16 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | record | BEAR_EXP | none | 55 | 199 | 0.2764 | 55 | 18 | 23 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | IN_RANGE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | IN_RANGE | top | 1 | 199 | 0.0050 | 1 | 1 | 1 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | IN_RANGE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | IN_RANGE | none | 64 | 199 | 0.3216 | 64 | 22 | 27 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BULL_EXP | none | 79 | 199 | 0.3970 | 79 | 34 | 16 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1d | mem_twin | BEAR_EXP | none | 55 | 199 | 0.2764 | 55 | 18 | 23 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | record | NONE | NA | 29 | 199 | 0.1457 | 29 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | record | IN_RANGE | NA | 42 | 199 | 0.2111 | 42 | 0 | 28 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | record | BULL_EXP | NA | 24 | 199 | 0.1206 | 24 | 0 | 14 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | record | BEAR_EXP | NA | 104 | 199 | 0.5226 | 104 | 0 | 25 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | mem_twin | NONE | NA | 29 | 199 | 0.1457 | 29 | 0 | 0 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | mem_twin | IN_RANGE | NA | 42 | 199 | 0.2111 | 42 | 0 | 28 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | mem_twin | BULL_EXP | NA | 24 | 199 | 0.1206 | 24 | 0 | 14 | 1w | 1w: whole-tape (fallback) |
| trg912 | calibrated | 1w | mem_twin | BEAR_EXP | NA | 104 | 199 | 0.5226 | 104 | 0 | 25 | 1w | 1w: whole-tape (fallback) |
| trg912 | frozen3.0 | 1h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | IN_RANGE | both | 2 | 199 | 0.0101 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | IN_RANGE | top | 6 | 199 | 0.0302 | 0 | 0 | 5 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | IN_RANGE | bot | 4 | 199 | 0.0201 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | IN_RANGE | none | 99 | 199 | 0.4975 | 0 | 0 | 30 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BULL_EXP | none | 53 | 199 | 0.2663 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | record | BEAR_EXP | none | 35 | 199 | 0.1759 | 0 | 0 | 13 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | IN_RANGE | both | 2 | 199 | 0.0101 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | IN_RANGE | top | 6 | 199 | 0.0302 | 0 | 0 | 5 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | IN_RANGE | bot | 4 | 199 | 0.0201 | 0 | 0 | 2 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | IN_RANGE | none | 99 | 199 | 0.4975 | 0 | 0 | 30 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BULL_EXP | none | 53 | 199 | 0.2663 | 0 | 0 | 17 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 1h | mem_twin | BEAR_EXP | none | 35 | 199 | 0.1759 | 0 | 0 | 13 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | IN_RANGE | both | 5 | 199 | 0.0251 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | IN_RANGE | top | 6 | 199 | 0.0302 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | IN_RANGE | bot | 8 | 199 | 0.0402 | 0 | 0 | 6 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | IN_RANGE | none | 67 | 199 | 0.3367 | 0 | 0 | 27 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BULL_EXP | none | 69 | 199 | 0.3467 | 0 | 0 | 18 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | record | BEAR_EXP | none | 44 | 199 | 0.2211 | 0 | 0 | 14 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | IN_RANGE | both | 5 | 199 | 0.0251 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | IN_RANGE | top | 6 | 199 | 0.0302 | 0 | 0 | 2 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | IN_RANGE | bot | 8 | 199 | 0.0402 | 0 | 0 | 6 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | IN_RANGE | none | 67 | 199 | 0.3367 | 0 | 0 | 27 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BULL_EXP | none | 69 | 199 | 0.3467 | 0 | 0 | 18 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 4h | mem_twin | BEAR_EXP | none | 44 | 199 | 0.2211 | 0 | 0 | 14 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | IN_RANGE | both | 2 | 199 | 0.0101 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | IN_RANGE | top | 12 | 199 | 0.0603 | 0 | 0 | 5 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | IN_RANGE | bot | 10 | 199 | 0.0503 | 0 | 0 | 5 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | IN_RANGE | none | 45 | 199 | 0.2261 | 0 | 0 | 21 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BULL_EXP | none | 75 | 199 | 0.3769 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | record | BEAR_EXP | none | 55 | 199 | 0.2764 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | NONE | none | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | IN_RANGE | both | 4 | 199 | 0.0201 | 0 | 0 | 2 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | IN_RANGE | top | 12 | 199 | 0.0603 | 0 | 0 | 5 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | IN_RANGE | bot | 10 | 199 | 0.0503 | 0 | 0 | 4 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | IN_RANGE | none | 43 | 199 | 0.2161 | 0 | 0 | 20 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BULL_EXP | none | 75 | 199 | 0.3769 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 12h | mem_twin | BEAR_EXP | none | 55 | 199 | 0.2764 | 0 | 0 | 18 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | NONE | none | 4 | 199 | 0.0201 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | IN_RANGE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | IN_RANGE | top | 1 | 199 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | IN_RANGE | bot | 1 | 199 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | IN_RANGE | none | 55 | 199 | 0.2764 | 0 | 0 | 21 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BULL_EXP | none | 81 | 199 | 0.4070 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | record | BEAR_EXP | none | 57 | 199 | 0.2864 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | NONE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | NONE | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | NONE | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | NONE | none | 4 | 199 | 0.0201 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | IN_RANGE | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | IN_RANGE | top | 1 | 199 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | IN_RANGE | bot | 1 | 199 | 0.0050 | 0 | 0 | 1 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | IN_RANGE | none | 55 | 199 | 0.2764 | 0 | 0 | 21 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BULL_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BULL_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BULL_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BULL_EXP | none | 81 | 199 | 0.4070 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BEAR_EXP | both | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BEAR_EXP | top | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BEAR_EXP | bot | 0 | 199 | 0.0000 | 0 | 0 | 0 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1d | mem_twin | BEAR_EXP | none | 57 | 199 | 0.2864 | 0 | 0 | 22 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | record | NONE | NA | 34 | 199 | 0.1709 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | record | IN_RANGE | NA | 29 | 199 | 0.1457 | 0 | 0 | 22 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | record | BULL_EXP | NA | 37 | 199 | 0.1859 | 0 | 0 | 16 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | record | BEAR_EXP | NA | 99 | 199 | 0.4975 | 0 | 0 | 29 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | mem_twin | NONE | NA | 34 | 199 | 0.1709 | 0 | 0 | 0 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | mem_twin | IN_RANGE | NA | 29 | 199 | 0.1457 | 0 | 0 | 22 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | mem_twin | BULL_EXP | NA | 37 | 199 | 0.1859 | 0 | 0 | 16 | 1w | 1w: frozen3.0 |
| trg912 | frozen3.0 | 1w | mem_twin | BEAR_EXP | NA | 99 | 199 | 0.4975 | 0 | 0 | 29 | 1w | 1w: frozen3.0 |

### Outcomes by L state at ENTRY (n, E[net R], P(win), ΣR; the HOLDOUT slice beside — the causal slice of a calibrated read)

| book | scale_kind | lens | state | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout | pick_window | stability_changed_members |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v6 | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| v6 | calibrated | 1h | IN_RANGE | 126 | 0.2210 | 0.3651 | 27.8457 | 79 | 73 | 47 | 0.6023 | 0.4255 | 28.3070 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| v6 | calibrated | 1h | BULL_EXP | 38 | -0.1829 | 0.2632 | -6.9504 | 27 | 23 | 11 | -0.3781 | 0.2727 | -4.1593 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| v6 | calibrated | 1h | BEAR_EXP | 36 | 0.5531 | 0.3611 | 19.9122 | 17 | 19 | 19 | 0.9465 | 0.2632 | 17.9836 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| v6 | calibrated | 1h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 115 | 77 | 0.5472 | 0.3636 | 42.1314 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| v6 | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| v6 | calibrated | 4h | IN_RANGE | 141 | 0.1677 | 0.3404 | 23.6414 | 88 | 31 | 53 | 0.4133 | 0.3585 | 21.9025 | 4h: tuning | 4h: NEARUSDT |
| v6 | calibrated | 4h | BULL_EXP | 32 | 0.7114 | 0.4062 | 22.7648 | 20 | 1 | 12 | 2.1614 | 0.5000 | 25.9366 | 4h: tuning | 4h: NEARUSDT |
| v6 | calibrated | 4h | BEAR_EXP | 27 | -0.2074 | 0.2963 | -5.5986 | 15 | 8 | 12 | -0.4756 | 0.2500 | -5.7078 | 4h: tuning | 4h: NEARUSDT |
| v6 | calibrated | 4h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 40 | 77 | 0.5472 | 0.3636 | 42.1314 | 4h: tuning | 4h: NEARUSDT |
| v6 | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 12h | IN_RANGE | 103 | 0.1391 | 0.3204 | 14.3271 | 54 | 74 | 49 | 0.1875 | 0.3265 | 9.1870 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 12h | BULL_EXP | 58 | 0.4190 | 0.3621 | 24.3003 | 45 | 32 | 13 | 2.2197 | 0.3846 | 28.8562 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 12h | BEAR_EXP | 39 | 0.0559 | 0.3846 | 2.1801 | 24 | 17 | 15 | 0.2725 | 0.4667 | 4.0882 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 12h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 123 | 77 | 0.5472 | 0.3636 | 42.1314 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1d | IN_RANGE | 73 | 0.1637 | 0.3562 | 11.9469 | 38 | 27 | 35 | 0.3332 | 0.3714 | 11.6636 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1d | BULL_EXP | 77 | 0.1009 | 0.3506 | 7.7669 | 59 | 29 | 18 | 1.0067 | 0.5556 | 18.1205 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1d | BEAR_EXP | 50 | 0.4219 | 0.3200 | 21.0938 | 26 | 19 | 24 | 0.5145 | 0.2083 | 12.3473 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1d | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 123 | 75 | 77 | 0.5472 | 0.3636 | 42.1314 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1w | NONE | 30 | 0.3600 | 0.4000 | 10.8012 | 30 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| v6 | calibrated | 1w | IN_RANGE | 43 | 0.1510 | 0.3488 | 6.4933 | 43 | 0 | 31 | 0.1066 | 0.3226 | 3.3061 | 1w: whole-tape (fallback) | 1w: none |
| v6 | calibrated | 1w | BULL_EXP | 29 | 1.2953 | 0.3448 | 37.5650 | 29 | 0 | 19 | 2.0242 | 0.4211 | 38.4590 | 1w: whole-tape (fallback) | 1w: none |
| v6 | calibrated | 1w | BEAR_EXP | 98 | -0.1434 | 0.3265 | -14.0520 | 98 | 0 | 27 | 0.0136 | 0.3704 | 0.3663 | 1w: whole-tape (fallback) | 1w: none |
| v6 | calibrated | 1w | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 200 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w: whole-tape (fallback) | 1w: none |
| v6 | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| v6 | frozen3.0 | 1h | IN_RANGE | 127 | 0.2742 | 0.3228 | 34.8204 | 0 | 0 | 49 | 0.9723 | 0.3878 | 47.6429 | 1h: frozen3.0 | 1h: none |
| v6 | frozen3.0 | 1h | BULL_EXP | 41 | -0.0365 | 0.3415 | -1.4978 | 0 | 0 | 17 | -0.3288 | 0.2353 | -5.5900 | 1h: frozen3.0 | 1h: none |
| v6 | frozen3.0 | 1h | BEAR_EXP | 32 | 0.2339 | 0.4375 | 7.4850 | 0 | 0 | 11 | 0.0071 | 0.4545 | 0.0785 | 1h: frozen3.0 | 1h: none |
| v6 | frozen3.0 | 1h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1h: frozen3.0 | 1h: none |
| v6 | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| v6 | frozen3.0 | 4h | IN_RANGE | 94 | 0.2867 | 0.3723 | 26.9490 | 0 | 0 | 45 | 0.4360 | 0.4000 | 19.6189 | 4h: frozen3.0 | 4h: none |
| v6 | frozen3.0 | 4h | BULL_EXP | 66 | 0.2198 | 0.2879 | 14.5096 | 0 | 0 | 19 | 1.4696 | 0.3158 | 27.9220 | 4h: frozen3.0 | 4h: none |
| v6 | frozen3.0 | 4h | BEAR_EXP | 40 | -0.0163 | 0.3750 | -0.6510 | 0 | 0 | 13 | -0.4161 | 0.3077 | -5.4095 | 4h: frozen3.0 | 4h: none |
| v6 | frozen3.0 | 4h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 4h: frozen3.0 | 4h: none |
| v6 | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| v6 | frozen3.0 | 12h | IN_RANGE | 74 | 0.1634 | 0.3514 | 12.0891 | 0 | 0 | 36 | 0.3284 | 0.3611 | 11.8213 | 12h: frozen3.0 | 12h: none |
| v6 | frozen3.0 | 12h | BULL_EXP | 76 | 0.4594 | 0.3816 | 34.9134 | 0 | 0 | 24 | 1.7344 | 0.5417 | 41.6250 | 12h: frozen3.0 | 12h: none |
| v6 | frozen3.0 | 12h | BEAR_EXP | 50 | -0.1239 | 0.2800 | -6.1949 | 0 | 0 | 17 | -0.6656 | 0.1176 | -11.3149 | 12h: frozen3.0 | 12h: none |
| v6 | frozen3.0 | 12h | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 12h: frozen3.0 | 12h: none |
| v6 | frozen3.0 | 1d | NONE | 4 | -0.4412 | 0.2500 | -1.7647 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| v6 | frozen3.0 | 1d | IN_RANGE | 58 | -0.1441 | 0.3276 | -8.3606 | 0 | 0 | 28 | 0.1158 | 0.4286 | 3.2411 | 1d: frozen3.0 | 1d: none |
| v6 | frozen3.0 | 1d | BULL_EXP | 74 | 0.2797 | 0.3514 | 20.7003 | 0 | 0 | 19 | 0.8025 | 0.3684 | 15.2472 | 1d: frozen3.0 | 1d: none |
| v6 | frozen3.0 | 1d | BEAR_EXP | 64 | 0.4724 | 0.3594 | 30.2327 | 0 | 0 | 30 | 0.7881 | 0.3000 | 23.6431 | 1d: frozen3.0 | 1d: none |
| v6 | frozen3.0 | 1d | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1d: frozen3.0 | 1d: none |
| v6 | frozen3.0 | 1w | NONE | 37 | 0.5083 | 0.4054 | 18.8077 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| v6 | frozen3.0 | 1w | IN_RANGE | 29 | 0.1704 | 0.3103 | 4.9413 | 0 | 0 | 25 | 0.2288 | 0.3200 | 5.7196 | 1w: frozen3.0 | 1w: none |
| v6 | frozen3.0 | 1w | BULL_EXP | 40 | 0.6888 | 0.2750 | 27.5520 | 0 | 0 | 20 | 1.8702 | 0.4000 | 37.4048 | 1w: frozen3.0 | 1w: none |
| v6 | frozen3.0 | 1w | BEAR_EXP | 94 | -0.1116 | 0.3617 | -10.4934 | 0 | 0 | 32 | -0.0310 | 0.3750 | -0.9930 | 1w: frozen3.0 | 1w: none |
| v6 | frozen3.0 | 1w | __ALL__ | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w: frozen3.0 | 1w: none |
| trg912 | calibrated | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| trg912 | calibrated | 1h | IN_RANGE | 122 | 0.3225 | 0.4262 | 39.3466 | 88 | 78 | 34 | 0.8432 | 0.5588 | 28.6680 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| trg912 | calibrated | 1h | BULL_EXP | 43 | 0.1080 | 0.3023 | 4.6441 | 26 | 19 | 17 | 0.6981 | 0.5294 | 11.8671 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| trg912 | calibrated | 1h | BEAR_EXP | 34 | 1.4214 | 0.4118 | 48.3278 | 18 | 17 | 16 | 1.7708 | 0.3125 | 28.3327 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| trg912 | calibrated | 1h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 132 | 114 | 67 | 1.0279 | 0.4925 | 68.8678 | 1h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT |
| trg912 | calibrated | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: tuning | 4h: NEARUSDT |
| trg912 | calibrated | 4h | IN_RANGE | 127 | 0.4083 | 0.4094 | 51.8586 | 84 | 31 | 43 | 0.6892 | 0.4651 | 29.6345 | 4h: tuning | 4h: NEARUSDT |
| trg912 | calibrated | 4h | BULL_EXP | 43 | 1.0872 | 0.4419 | 46.7515 | 27 | 3 | 16 | 2.1003 | 0.5625 | 33.6042 | 4h: tuning | 4h: NEARUSDT |
| trg912 | calibrated | 4h | BEAR_EXP | 29 | -0.2170 | 0.2759 | -6.2917 | 21 | 5 | 8 | 0.7036 | 0.5000 | 5.6291 | 4h: tuning | 4h: NEARUSDT |
| trg912 | calibrated | 4h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 132 | 39 | 67 | 1.0279 | 0.4925 | 68.8678 | 4h: tuning | 4h: NEARUSDT |
| trg912 | calibrated | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 12h | IN_RANGE | 88 | 0.5959 | 0.4432 | 52.4369 | 49 | 59 | 39 | 0.8558 | 0.4872 | 33.3771 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 12h | BULL_EXP | 64 | 0.6944 | 0.4062 | 44.4405 | 53 | 42 | 11 | 2.6964 | 0.5455 | 29.6601 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 12h | BEAR_EXP | 47 | -0.0970 | 0.2979 | -4.5589 | 30 | 22 | 17 | 0.3430 | 0.4706 | 5.8306 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 12h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 132 | 123 | 67 | 1.0279 | 0.4925 | 68.8678 | 12h: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 1d | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1d | IN_RANGE | 65 | 1.0661 | 0.5077 | 69.2958 | 37 | 23 | 28 | 1.6165 | 0.6071 | 45.2615 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1d | BULL_EXP | 79 | 0.1348 | 0.3797 | 10.6501 | 63 | 34 | 16 | 0.6346 | 0.6250 | 10.1530 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1d | BEAR_EXP | 55 | 0.2250 | 0.2909 | 12.3726 | 32 | 18 | 23 | 0.5849 | 0.2609 | 13.4532 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1d | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 132 | 75 | 67 | 1.0279 | 0.4925 | 68.8678 | 1d: tuning | 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1w | NONE | 29 | 0.0889 | 0.3793 | 2.5789 | 29 | 0 | 0 | — | — | — | 1w: whole-tape (fallback) | 1w: none |
| trg912 | calibrated | 1w | IN_RANGE | 42 | 0.2054 | 0.3095 | 8.6271 | 42 | 0 | 28 | 0.4885 | 0.3571 | 13.6781 | 1w: whole-tape (fallback) | 1w: none |
| trg912 | calibrated | 1w | BULL_EXP | 24 | 1.9487 | 0.5417 | 46.7689 | 24 | 0 | 14 | 2.8823 | 0.5714 | 40.3521 | 1w: whole-tape (fallback) | 1w: none |
| trg912 | calibrated | 1w | BEAR_EXP | 104 | 0.3302 | 0.4038 | 34.3435 | 104 | 0 | 25 | 0.5935 | 0.6000 | 14.8376 | 1w: whole-tape (fallback) | 1w: none |
| trg912 | calibrated | 1w | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 199 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w: whole-tape (fallback) | 1w: none |
| trg912 | frozen3.0 | 1h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1h: frozen3.0 | 1h: none |
| trg912 | frozen3.0 | 1h | IN_RANGE | 111 | 0.6196 | 0.4144 | 68.7743 | 0 | 0 | 37 | 1.1750 | 0.5135 | 43.4743 | 1h: frozen3.0 | 1h: none |
| trg912 | frozen3.0 | 1h | BULL_EXP | 53 | 0.2970 | 0.3774 | 15.7416 | 0 | 0 | 17 | 0.6633 | 0.4706 | 11.2765 | 1h: frozen3.0 | 1h: none |
| trg912 | frozen3.0 | 1h | BEAR_EXP | 35 | 0.2229 | 0.3714 | 7.8026 | 0 | 0 | 13 | 1.0859 | 0.4615 | 14.1170 | 1h: frozen3.0 | 1h: none |
| trg912 | frozen3.0 | 1h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1h: frozen3.0 | 1h: none |
| trg912 | frozen3.0 | 4h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 4h: frozen3.0 | 4h: none |
| trg912 | frozen3.0 | 4h | IN_RANGE | 86 | 0.5716 | 0.4651 | 49.1563 | 0 | 0 | 35 | 0.7153 | 0.5143 | 25.0349 | 4h: frozen3.0 | 4h: none |
| trg912 | frozen3.0 | 4h | BULL_EXP | 69 | 0.5791 | 0.3478 | 39.9586 | 0 | 0 | 18 | 1.8648 | 0.4444 | 33.5670 | 4h: frozen3.0 | 4h: none |
| trg912 | frozen3.0 | 4h | BEAR_EXP | 44 | 0.0728 | 0.3409 | 3.2036 | 0 | 0 | 14 | 0.7333 | 0.5000 | 10.2659 | 4h: frozen3.0 | 4h: none |
| trg912 | frozen3.0 | 4h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 4h: frozen3.0 | 4h: none |
| trg912 | frozen3.0 | 12h | NONE | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 12h: frozen3.0 | 12h: none |
| trg912 | frozen3.0 | 12h | IN_RANGE | 69 | 0.9956 | 0.5217 | 68.6962 | 0 | 0 | 31 | 1.2680 | 0.5161 | 39.3087 | 12h: frozen3.0 | 12h: none |
| trg912 | frozen3.0 | 12h | BULL_EXP | 75 | 0.4759 | 0.4000 | 35.6892 | 0 | 0 | 18 | 2.1458 | 0.7222 | 38.6243 | 12h: frozen3.0 | 12h: none |
| trg912 | frozen3.0 | 12h | BEAR_EXP | 55 | -0.2194 | 0.2364 | -12.0669 | 0 | 0 | 18 | -0.5036 | 0.2222 | -9.0652 | 12h: frozen3.0 | 12h: none |
| trg912 | frozen3.0 | 12h | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 12h: frozen3.0 | 12h: none |
| trg912 | frozen3.0 | 1d | NONE | 4 | -0.2329 | 0.2500 | -0.9315 | 0 | 0 | 0 | — | — | — | 1d: frozen3.0 | 1d: none |
| trg912 | frozen3.0 | 1d | IN_RANGE | 57 | 0.5507 | 0.4211 | 31.3903 | 0 | 0 | 23 | 0.7089 | 0.5217 | 16.3037 | 1d: frozen3.0 | 1d: none |
| trg912 | frozen3.0 | 1d | BULL_EXP | 81 | 0.4239 | 0.4444 | 34.3342 | 0 | 0 | 22 | 0.7298 | 0.5000 | 16.0550 | 1d: frozen3.0 | 1d: none |
| trg912 | frozen3.0 | 1d | BEAR_EXP | 57 | 0.4829 | 0.3158 | 27.5254 | 0 | 0 | 22 | 1.6595 | 0.4545 | 36.5091 | 1d: frozen3.0 | 1d: none |
| trg912 | frozen3.0 | 1d | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1d: frozen3.0 | 1d: none |
| trg912 | frozen3.0 | 1w | NONE | 34 | 0.2676 | 0.4118 | 9.0978 | 0 | 0 | 0 | — | — | — | 1w: frozen3.0 | 1w: none |
| trg912 | frozen3.0 | 1w | IN_RANGE | 29 | 0.4960 | 0.3103 | 14.3832 | 0 | 0 | 22 | 0.7308 | 0.3636 | 16.0773 | 1w: frozen3.0 | 1w: none |
| trg912 | frozen3.0 | 1w | BULL_EXP | 37 | 1.0306 | 0.3784 | 38.1321 | 0 | 0 | 16 | 2.4192 | 0.5000 | 38.7076 | 1w: frozen3.0 | 1w: none |
| trg912 | frozen3.0 | 1w | BEAR_EXP | 99 | 0.3102 | 0.4242 | 30.7053 | 0 | 0 | 29 | 0.4856 | 0.5862 | 14.0829 | 1w: frozen3.0 | 1w: none |
| trg912 | frozen3.0 | 1w | __ALL__ | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w: frozen3.0 | 1w: none |

### Outcomes by coincidence at ENTRY (the HOLDOUT slice beside)

| book | scale_kind | lens | coin_rule | coin_cat | n | mean_net_r | p_win | sum_net_r | n_scale_in_sample | n_stability_changed | n_holdout | mean_net_r_holdout | p_win_holdout | sum_net_r_holdout | lenses_read | pick_window | stability_changed_members |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| v6 | calibrated | 1h | record | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | record | top | 9 | 0.1857 | 0.3333 | 1.6713 | 4 | 3 | 5 | 0.5794 | 0.4000 | 2.8969 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | record | bot | 17 | 0.4327 | 0.5294 | 7.3565 | 12 | 11 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | record | none | 170 | 0.1293 | 0.3176 | 21.9835 | 105 | 99 | 65 | 0.3638 | 0.3231 | 23.6486 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | mem_twin | both | 4 | 2.4491 | 0.7500 | 9.7962 | 2 | 2 | 2 | 3.8599 | 0.5000 | 7.7198 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | mem_twin | top | 10 | 0.0623 | 0.3000 | 0.6231 | 5 | 4 | 5 | 0.5794 | 0.4000 | 2.8969 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | mem_twin | bot | 19 | 0.2695 | 0.4737 | 5.1206 | 14 | 12 | 5 | 1.5732 | 0.8000 | 7.8660 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 1h | mem_twin | none | 167 | 0.1513 | 0.3234 | 25.2676 | 102 | 97 | 65 | 0.3638 | 0.3231 | 23.6486 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| v6 | calibrated | 4h | record | both | 9 | 0.2610 | 0.4444 | 2.3489 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | record | top | 8 | 0.5771 | 0.5000 | 4.6172 | 1 | 7 | 7 | 0.7935 | 0.5714 | 5.5546 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | record | bot | 12 | 0.5730 | 0.2500 | 6.8764 | 5 | 11 | 7 | 0.8164 | 0.2857 | 5.7150 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | record | none | 171 | 0.1577 | 0.3392 | 26.9651 | 110 | 137 | 61 | 0.5403 | 0.3607 | 32.9588 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | mem_twin | both | 9 | 0.2610 | 0.4444 | 2.3489 | 7 | 8 | 2 | -1.0485 | 0.0000 | -2.0970 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | mem_twin | top | 8 | 0.5771 | 0.5000 | 4.6172 | 1 | 7 | 7 | 0.7935 | 0.5714 | 5.5546 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | mem_twin | bot | 13 | 0.7517 | 0.3077 | 9.7716 | 6 | 11 | 7 | 0.8164 | 0.2857 | 5.7150 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 4h | mem_twin | none | 170 | 0.1416 | 0.3353 | 24.0699 | 109 | 137 | 61 | 0.5403 | 0.3607 | 32.9588 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| v6 | calibrated | 12h | record | both | 6 | 0.5257 | 0.3333 | 3.1542 | 4 | 3 | 2 | -0.6436 | 0.0000 | -1.2872 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | record | top | 4 | -0.8505 | 0.0000 | -3.4018 | 1 | 2 | 3 | -0.8127 | 0.0000 | -2.4380 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | record | bot | 13 | 0.5526 | 0.4615 | 7.1839 | 5 | 8 | 8 | 0.9406 | 0.5000 | 7.5250 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | record | none | 177 | 0.1914 | 0.3446 | 33.8713 | 113 | 110 | 64 | 0.5989 | 0.3750 | 38.3316 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | mem_twin | both | 7 | 0.2941 | 0.2857 | 2.0588 | 4 | 4 | 3 | -0.7942 | 0.0000 | -2.3827 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | mem_twin | top | 9 | -0.8687 | 0.0000 | -7.8185 | 3 | 6 | 6 | -0.8929 | 0.0000 | -5.3574 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | mem_twin | bot | 15 | 0.4770 | 0.4667 | 7.1545 | 8 | 10 | 7 | 1.2315 | 0.5714 | 8.6205 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 12h | mem_twin | none | 169 | 0.2332 | 0.3550 | 39.4128 | 108 | 103 | 61 | 0.6762 | 0.3934 | 41.2510 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| v6 | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | record | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | record | none | 199 | 0.1857 | 0.3417 | 36.9564 | 199 | 74 | 76 | 0.5037 | 0.3553 | 38.2802 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | mem_twin | top | 1 | 3.8512 | 1.0000 | 3.8512 | 1 | 1 | 1 | 3.8512 | 1.0000 | 3.8512 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1d | mem_twin | none | 199 | 0.1857 | 0.3417 | 36.9564 | 199 | 74 | 76 | 0.5037 | 0.3553 | 38.2802 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| v6 | calibrated | 1w | record | NA | 200 | 0.2040 | 0.3450 | 40.8076 | 200 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w | 1w: whole-tape (fallback) | 1w: none |
| v6 | calibrated | 1w | mem_twin | NA | 200 | 0.2040 | 0.3450 | 40.8076 | 200 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w | 1w: whole-tape (fallback) | 1w: none |
| v6 | frozen3.0 | 1h | record | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | record | top | 9 | 0.3331 | 0.4444 | 2.9977 | 0 | 0 | 6 | 0.9315 | 0.6667 | 5.5889 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | record | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | record | none | 188 | 0.2115 | 0.3404 | 39.7703 | 0 | 0 | 70 | 0.5368 | 0.3429 | 37.5774 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | mem_twin | both | 1 | -0.9374 | 0.0000 | -0.9374 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | mem_twin | top | 10 | 0.9177 | 0.5000 | 9.1771 | 0 | 0 | 7 | 1.6812 | 0.7143 | 11.7683 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | mem_twin | bot | 2 | -0.5115 | 0.5000 | -1.0231 | 0 | 0 | 1 | -1.0349 | 0.0000 | -1.0349 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 1h | mem_twin | none | 187 | 0.1796 | 0.3369 | 33.5909 | 0 | 0 | 69 | 0.4550 | 0.3333 | 31.3980 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| v6 | frozen3.0 | 4h | record | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | record | top | 3 | 1.1348 | 1.0000 | 3.4045 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | record | bot | 13 | -0.6213 | 0.1538 | -8.0764 | 0 | 0 | 10 | -0.5285 | 0.2000 | -5.2854 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | record | none | 179 | 0.2696 | 0.3520 | 48.2519 | 0 | 0 | 66 | 0.7302 | 0.3939 | 48.1903 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | mem_twin | both | 5 | -0.5545 | 0.2000 | -2.7724 | 0 | 0 | 1 | -0.7735 | 0.0000 | -0.7735 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | mem_twin | top | 3 | 1.1348 | 1.0000 | 3.4045 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | mem_twin | bot | 13 | -0.6213 | 0.1538 | -8.0764 | 0 | 0 | 10 | -0.5285 | 0.2000 | -5.2854 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 4h | mem_twin | none | 179 | 0.2696 | 0.3520 | 48.2519 | 0 | 0 | 66 | 0.7302 | 0.3939 | 48.1903 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| v6 | frozen3.0 | 12h | record | both | 5 | 1.1024 | 0.6000 | 5.5118 | 0 | 0 | 3 | 2.3159 | 1.0000 | 6.9476 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | record | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | record | bot | 9 | 0.0990 | 0.4444 | 0.8913 | 0 | 0 | 4 | 0.8369 | 0.5000 | 3.3475 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | record | none | 177 | 0.2060 | 0.3390 | 36.4598 | 0 | 0 | 66 | 0.5120 | 0.3333 | 33.7951 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | mem_twin | both | 6 | 0.7360 | 0.5000 | 4.4163 | 0 | 0 | 4 | 1.4630 | 0.7500 | 5.8522 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | mem_twin | top | 9 | -0.2284 | 0.2222 | -2.0553 | 0 | 0 | 4 | -0.4897 | 0.2500 | -1.9588 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | mem_twin | bot | 8 | 0.2483 | 0.5000 | 1.9868 | 0 | 0 | 3 | 1.4810 | 0.6667 | 4.4430 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 12h | mem_twin | none | 177 | 0.2060 | 0.3390 | 36.4598 | 0 | 0 | 66 | 0.5120 | 0.3333 | 33.7951 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| v6 | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | record | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | record | none | 197 | 0.1827 | 0.3401 | 35.9873 | 0 | 0 | 74 | 0.5042 | 0.3514 | 37.3111 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | mem_twin | top | 2 | 1.3995 | 0.5000 | 2.7991 | 0 | 0 | 2 | 1.3995 | 0.5000 | 2.7991 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1d | mem_twin | none | 197 | 0.1827 | 0.3401 | 35.9873 | 0 | 0 | 74 | 0.5042 | 0.3514 | 37.3111 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| v6 | frozen3.0 | 1w | record | NA | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w | 1w: frozen3.0 | 1w: none |
| v6 | frozen3.0 | 1w | mem_twin | NA | 200 | 0.2040 | 0.3450 | 40.8076 | 0 | 0 | 77 | 0.5472 | 0.3636 | 42.1314 | 1w | 1w: frozen3.0 | 1w: none |
| trg912 | calibrated | 1h | record | both | 5 | 0.3645 | 0.6000 | 1.8224 | 3 | 3 | 2 | 0.5693 | 1.0000 | 1.1387 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | record | top | 7 | 0.2518 | 0.2857 | 1.7629 | 5 | 5 | 2 | 2.2340 | 0.5000 | 4.4679 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | record | bot | 17 | 0.8841 | 0.7059 | 15.0300 | 12 | 13 | 5 | 1.5044 | 1.0000 | 7.5222 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | record | none | 170 | 0.4335 | 0.3647 | 73.7031 | 112 | 93 | 58 | 0.9610 | 0.4310 | 55.7391 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | mem_twin | both | 5 | 0.3645 | 0.6000 | 1.8224 | 3 | 3 | 2 | 0.5693 | 1.0000 | 1.1387 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | mem_twin | top | 8 | 0.0916 | 0.2500 | 0.7328 | 6 | 6 | 2 | 2.2340 | 0.5000 | 4.4679 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | mem_twin | bot | 19 | 0.6763 | 0.6316 | 12.8503 | 14 | 14 | 5 | 1.5044 | 1.0000 | 7.5222 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 1h | mem_twin | none | 167 | 0.4606 | 0.3713 | 76.9129 | 109 | 91 | 58 | 0.9610 | 0.4310 | 55.7391 | 1h+4h | 1h: tuning; 4h: tuning | 1h: BTCUSDT,SOLUSDT,NEARUSDT; 4h: NEARUSDT |
| trg912 | calibrated | 4h | record | both | 7 | 1.4905 | 0.7143 | 10.4338 | 6 | 6 | 1 | -1.0347 | 0.0000 | -1.0347 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | record | top | 8 | -0.8879 | 0.1250 | -7.1029 | 4 | 6 | 4 | -0.7255 | 0.2500 | -2.9021 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | record | bot | 12 | 0.3951 | 0.5000 | 4.7415 | 5 | 11 | 7 | 0.7409 | 0.4286 | 5.1865 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | record | none | 172 | 0.4898 | 0.3895 | 84.2461 | 117 | 139 | 55 | 1.2294 | 0.5273 | 67.6182 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | mem_twin | both | 7 | 1.4905 | 0.7143 | 10.4338 | 6 | 6 | 1 | -1.0347 | 0.0000 | -1.0347 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | mem_twin | top | 9 | -0.9029 | 0.1111 | -8.1263 | 4 | 7 | 5 | -0.7851 | 0.2000 | -3.9255 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | mem_twin | bot | 12 | 0.3951 | 0.5000 | 4.7415 | 5 | 11 | 7 | 0.7409 | 0.4286 | 5.1865 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 4h | mem_twin | none | 171 | 0.4987 | 0.3918 | 85.2695 | 117 | 138 | 54 | 1.2711 | 0.5370 | 68.6416 | 4h+12h | 4h: tuning; 12h: tuning | 4h: NEARUSDT; 12h: BTCUSDT,ETHUSDT,SOLUSDT |
| trg912 | calibrated | 12h | record | both | 6 | 0.3637 | 0.6667 | 2.1823 | 4 | 2 | 2 | 1.5467 | 1.0000 | 3.0934 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | record | top | 6 | 3.7445 | 0.3333 | 22.4670 | 2 | 3 | 4 | 2.4000 | 0.2500 | 9.6001 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | record | bot | 13 | 1.7749 | 0.6923 | 23.0736 | 5 | 9 | 8 | 1.9216 | 0.7500 | 15.3726 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | record | none | 174 | 0.2563 | 0.3678 | 44.5955 | 121 | 109 | 53 | 0.7698 | 0.4528 | 40.8017 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | mem_twin | both | 8 | 0.4936 | 0.6250 | 3.9491 | 4 | 4 | 4 | 1.2150 | 0.7500 | 4.8602 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | mem_twin | top | 10 | 1.9996 | 0.3000 | 19.9961 | 4 | 6 | 6 | 1.2839 | 0.1667 | 7.7037 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | mem_twin | bot | 15 | 1.3684 | 0.6000 | 20.5256 | 9 | 11 | 6 | 2.2676 | 0.8333 | 13.6058 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 12h | mem_twin | none | 166 | 0.2882 | 0.3735 | 47.8476 | 115 | 102 | 51 | 0.8372 | 0.4706 | 42.6982 | 12h+1d | 12h: tuning; 1d: tuning | 12h: BTCUSDT,ETHUSDT,SOLUSDT; 1d: BTCUSDT,SOLUSDT |
| trg912 | calibrated | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | record | top | 1 | 7.0680 | 1.0000 | 7.0680 | 1 | 1 | 1 | 7.0680 | 1.0000 | 7.0680 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | record | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | record | none | 198 | 0.4306 | 0.3939 | 85.2504 | 198 | 74 | 66 | 0.9364 | 0.4848 | 61.7998 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | mem_twin | top | 1 | 7.0680 | 1.0000 | 7.0680 | 1 | 1 | 1 | 7.0680 | 1.0000 | 7.0680 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | mem_twin | bot | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1d | mem_twin | none | 198 | 0.4306 | 0.3939 | 85.2504 | 198 | 74 | 66 | 0.9364 | 0.4848 | 61.7998 | 1d+1w | 1d: tuning; 1w: whole-tape (fallback) | 1d: BTCUSDT,SOLUSDT; 1w: none |
| trg912 | calibrated | 1w | record | NA | 199 | 0.4639 | 0.3970 | 92.3184 | 199 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w | 1w: whole-tape (fallback) | 1w: none |
| trg912 | calibrated | 1w | mem_twin | NA | 199 | 0.4639 | 0.3970 | 92.3184 | 199 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w | 1w: whole-tape (fallback) | 1w: none |
| trg912 | frozen3.0 | 1h | record | both | 2 | -0.9525 | 0.0000 | -1.9050 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | record | top | 6 | 0.9423 | 0.6667 | 5.6540 | 0 | 0 | 5 | 1.3634 | 0.8000 | 6.8168 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | record | bot | 4 | 1.4830 | 1.0000 | 5.9318 | 0 | 0 | 2 | 1.6141 | 1.0000 | 3.2281 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | record | none | 187 | 0.4419 | 0.3797 | 82.6376 | 0 | 0 | 60 | 0.9804 | 0.4500 | 58.8229 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | mem_twin | both | 2 | -0.9525 | 0.0000 | -1.9050 | 0 | 0 | 0 | — | — | — | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | mem_twin | top | 6 | 0.9423 | 0.6667 | 5.6540 | 0 | 0 | 5 | 1.3634 | 0.8000 | 6.8168 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | mem_twin | bot | 4 | 1.4830 | 1.0000 | 5.9318 | 0 | 0 | 2 | 1.6141 | 1.0000 | 3.2281 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 1h | mem_twin | none | 187 | 0.4419 | 0.3797 | 82.6376 | 0 | 0 | 60 | 0.9804 | 0.4500 | 58.8229 | 1h+4h | 1h: frozen3.0; 4h: frozen3.0 | 1h: none; 4h: none |
| trg912 | frozen3.0 | 4h | record | both | 5 | 0.0236 | 0.6000 | 0.1180 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | record | top | 6 | 2.0416 | 0.8333 | 12.2495 | 0 | 0 | 2 | 0.9427 | 0.5000 | 1.8855 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | record | bot | 8 | 0.1227 | 0.6250 | 0.9818 | 0 | 0 | 6 | 0.2796 | 0.6667 | 1.6779 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | record | none | 180 | 0.4387 | 0.3667 | 78.9691 | 0 | 0 | 59 | 1.1069 | 0.4746 | 65.3044 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | mem_twin | both | 5 | 0.0236 | 0.6000 | 0.1180 | 0 | 0 | 0 | — | — | — | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | mem_twin | top | 6 | 2.0416 | 0.8333 | 12.2495 | 0 | 0 | 2 | 0.9427 | 0.5000 | 1.8855 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | mem_twin | bot | 8 | 0.1227 | 0.6250 | 0.9818 | 0 | 0 | 6 | 0.2796 | 0.6667 | 1.6779 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 4h | mem_twin | none | 180 | 0.4387 | 0.3667 | 78.9691 | 0 | 0 | 59 | 1.1069 | 0.4746 | 65.3044 | 4h+12h | 4h: frozen3.0; 12h: frozen3.0 | 4h: none; 12h: none |
| trg912 | frozen3.0 | 12h | record | both | 2 | 0.9489 | 1.0000 | 1.8979 | 0 | 0 | 0 | — | — | — | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | record | top | 12 | 1.7580 | 0.4167 | 21.0960 | 0 | 0 | 5 | -0.4198 | 0.2000 | -2.0991 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | record | bot | 10 | 0.6882 | 0.4000 | 6.8821 | 0 | 0 | 5 | 2.0144 | 0.6000 | 10.0718 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | record | none | 175 | 0.3568 | 0.3886 | 62.4424 | 0 | 0 | 57 | 1.0683 | 0.5088 | 60.8951 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | mem_twin | both | 4 | 0.9162 | 0.7500 | 3.6647 | 0 | 0 | 2 | 0.8834 | 0.5000 | 1.7668 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | mem_twin | top | 12 | 1.7580 | 0.4167 | 21.0960 | 0 | 0 | 5 | -0.4198 | 0.2000 | -2.0991 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | mem_twin | bot | 10 | 0.6932 | 0.4000 | 6.9321 | 0 | 0 | 4 | 2.0684 | 0.5000 | 8.2735 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 12h | mem_twin | none | 173 | 0.3504 | 0.3873 | 60.6257 | 0 | 0 | 56 | 1.0880 | 0.5179 | 60.9265 | 12h+1d | 12h: frozen3.0; 1d: frozen3.0 | 12h: none; 1d: none |
| trg912 | frozen3.0 | 1d | record | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | record | top | 1 | 7.0680 | 1.0000 | 7.0680 | 0 | 0 | 1 | 7.0680 | 1.0000 | 7.0680 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | record | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | record | none | 197 | 0.4225 | 0.3909 | 83.2292 | 0 | 0 | 65 | 0.9197 | 0.4769 | 59.7786 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | mem_twin | both | 0 | — | — | — | 0 | 0 | 0 | — | — | — | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | mem_twin | top | 1 | 7.0680 | 1.0000 | 7.0680 | 0 | 0 | 1 | 7.0680 | 1.0000 | 7.0680 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | mem_twin | bot | 1 | 2.0212 | 1.0000 | 2.0212 | 0 | 0 | 1 | 2.0212 | 1.0000 | 2.0212 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1d | mem_twin | none | 197 | 0.4225 | 0.3909 | 83.2292 | 0 | 0 | 65 | 0.9197 | 0.4769 | 59.7786 | 1d+1w | 1d: frozen3.0; 1w: frozen3.0 | 1d: none; 1w: none |
| trg912 | frozen3.0 | 1w | record | NA | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w | 1w: frozen3.0 | 1w: none |
| trg912 | frozen3.0 | 1w | mem_twin | NA | 199 | 0.4639 | 0.3970 | 92.3184 | 0 | 0 | 67 | 1.0279 | 0.4925 | 68.8678 | 1w | 1w: frozen3.0 | 1w: none |
