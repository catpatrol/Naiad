# TIER-C11 · STAGE R-b · R4 — THE TWO TRADES PER LENS (TIER-E, WHOLE)

as_of_last_closed_4h: 2026-09-25T00:00:00Z · substrate tc11_20260925 · seed 20260924 (null sensitivity seed 20260816) · K = 20 draws · schedule gaps+order (ruling R10)

**TIER-E · a SELECTION, not a result · gates nothing.** No row of this stage is a test or a verdict; no cell may be promoted to one. Every table below is WHOLE over the scope its caption declares; the parquets hold every asset row.

## 0 · Scope — which file is the grid of record

- **The grid of record is `R4_GRID.parquet`** (180,684 rows = exactly the declared cells, F-GRID) with its base rate `R4_BASE.parquet` (67,140) and null `R4_NULL.parquet` (100,764). The markdown tables are WHOLE only over the scope each caption declares; a build document that quotes this stage quotes the parquets for anything outside those scopes.
- Printed here: §4 POOLED:CLASSIC5 · calibrated · law record (every lens x event x L+1 cell x direction); §5 POOLED:UNSEEN12 · calibrated · law record; §6 base POOLED:CLASSIC5 · calibrated · law record; §7 null POOLED:CLASSIC5 · calibrated · NET · eras ALL and holdout; §9 scan ledger per panel; §10 every ASSET (and both pools) · calibrated · law record · cell ALL (every lens x event x direction). `R4_GRID.md` prints POOLED:CLASSIC5 at both scales and every cell law.
- In the parquets only: per-asset L+1-partitioned rows; POOLED:UNSEEN12 at frozen3.0 and its twin laws; every frozen3.0 per-asset row; the base twins (mem_twin, topside, botside, own_side_*) and every per-asset base row; the null's tuning era, its frozen3.0 scale, its per-asset rows and every statistic but NET; mean / q25 / q75 / hit rates / MFE / MAE / tolls / censoring on every row; the scan ledger per asset (R4_SCAN, R4_DEATHS).

## Readings (lean block)

- [LEAN-HEPHAESTUS] R4-1 COMMISSION [L-R.6]: CLASSIC5 x {1h, 4h, 12h, 1d} and UNSEEN12 x {1h, 4h, 1d}, per asset and pooled (POOLED:CLASSIC5, POOLED:UNSEEN12 — the pools never mix), x {calibrated (the filed pick of record, N.scale_of), frozen3.0 (the twin)} x eras {ALL, tuning, holdout} by the anchor bar's CLOSE [L-1.3] x directions {both, long, short} x {H20, H100} in bars of L. Everything is TIER-E.
- [LEAN-HEPHAESTUS] R4-2 EVENTS [L-R.6(a)(b)]: BREAKOUT = N's first-retest-that-HOLDS scan (rule 'first') on tap89 / tap127 / tap200 (C.RETEST_PINS 1.0 ATR / 3 bars / ttl 400) and the memory line (1.0 ATR / 6 bars), each beside its one-shot twin (rule 'oneshot': C.retest_holds' hold rows; the engine's one-shot flip for the memory line). Direction = the death side (top -> long). SWING-FAILURE = the machine's harden (bottom -> spring, long; top -> upthrust, short). Every event is anchored at N's known_at (touch + hold; the harden bar) and never recomputed here.
- [LEAN-HEPHAESTUS] R4-3 L+1 CELL [L-R.6, R-CELL]: N.l1_cell at the event's known_at CLOSE — record = coincidence of the event's boundary of L (BREAKOUT: the broken side as-of die_i - 1; SFP: the deviated side as-of harden_i - 1) with a LIVE L+1 boundary within 0.25 x ATR_L; twins: 'mem_twin' (L+1 live memory lines admitted, N's cell_mem) and, for SFP, 'post_redraw' (the boundary as-of harden_i; 'n/a' where no post-redraw boundary exists). Cells: EXP_ALIGNED*, EXP_COUNTER, IN_RANGE_COINCIDENT*, IN_RANGE_MID*, IN_RANGE_OTHER, NONE (the contract's three starred); 'ALL' = unconditioned; 'NA' where the ladder lacks L+1 in the commission (UNSEEN12 4h and 1d, whose 12h / 1w are not built).
- [LEAN-HEPHAESTUS] R4-4 OUTCOMES: C.outcome_ledger (the census's own road, unforked): term = sgn x (c[k+H] - c[k]) / ATR_L[k] from the known_at close k, MFE / MAE likewise; CENSORED when k + H > n - 1 (never shortened); toll_atr_evt = (10 bps / 10^4) x c[k] / ATR_L[k] with the bps read from TC11's fee schedule (C.toll_bps_for). Statistics = C.grid_rows ITSELF on each cell's ledger slice (n_events, n, n_censored, median_term, mean_term, q25/q75, hit_rate, hit_rate_net, median MFE / MAE, toll_atr, net = median_term - toll_atr) fed the FILED (8 dp) ledger as the census feeds it (tierc10_census.compute_cell canons first); a pooled row quotes the BINDING max of its members' toll_atr (C.grid_rows' tolls= law, TC10's). Cells are packed up to eleven per C.grid_rows call under its eleven class labels; the label changes only the dropped metadata columns, never the arithmetic.
- [LEAN-HEPHAESTUS] R4-5 BASE RATE [L-R.6, AM-6 R-BASE-COIN]: C.outcome_ledger anchored at EVERY closed bar k of L, long and short; direction 'both' = the union of the two anchored sets (a cell that depends on direction — EXP_ALIGNED — takes each bar under its own direction). Cells from N.range_facts: record = coin_top OR coin_bot of L at k with L+1 read as-of close_k; twins topside / botside (one side alone), own_side_brk (long@topside + short@botside: a BREAKOUT's broken side), own_side_sfp (long@botside + short@topside: an SFP's deviated side), mem_twin (L's nest coin_*_mem), and the memory-line own-side twins own_side_brk_mem / own_side_sfp_mem (the same composites on coin_top_mem / coin_bot_mem). Each event row carries its cell-base row (law record; mem_twin for mem_twin rows), its own-side base (BRK own_side_brk, SFP own_side_sfp; the _mem composite for mem_twin rows; post_redraw rows the record composite) and the unconditional base (cell ALL), with event NET - base NET.
- [LEAN-HEPHAESTUS] R4-6 NULL [L-R.6, ruling R10]: gaps+order, K = 20, per (asset, lens, scale) at the filed pick — NL.real_box_set, NL.draw_rng (default_rng([seed + draw, crc32('asset|lens|scale_kind')]); 'kind' read as the scale kind, TC10's key), NL.schedule(keep_order=False), NL.static_box_machine, RC.flips_and_leash on the corpses; events through N's scan and the null's hardens; the null box's static edge is the event boundary; the L+1 cell read from the REAL L+1 machine at the null event's known_at. Pooled null draw d = draw d of every member (TC10's law). One null row per real grid cell of law record: real beside the null's median / q25 / q75 / IQR / min / max over the valid draws and the mid-rank percentile — a DESCRIPTION, never a p-value; every draw's n and NET filed; the sensitivity seed 20260816 re-draws the null and prints its NET median and percentile beside. Built at both scales (calibrated of record; frozen3.0 = TC10's null scale).
- [LEAN-HEPHAESTUS] R4-7 CONTINUITY [AM-1]: at frozen3.0, one-shot, 4h, POOLED:CLASSIC5, tap89, H20 NET, TC11's value is printed beside TC10's census/outcome_grid.parquet row (read by absolute main-tree path), and the TC10 window is REPLAYED in TC11 code (the tapes cut at 2026-09-21T16:00Z, C.run_scale at 3.0, C.retest_holds, C.outcome_ledger, C.grid_rows): the replay must equal the filed row at its 8 dp; the difference to TC11 is then decomposed event by event over the 20 extra 4h bars.
- [LEAN-HEPHAESTUS] R4-8 LABELS [L-R.2, AM-4]: every event row carries l_ / u_ pick_window, scale_in_sample and stability_changed; every grid / base / null row carries the pick windows and stability flags of L and L+1 (a pool: the distinct values joined) and the counts of its anchors whose L or L+1 read is scale-in-sample. l_scale_in_sample is keyed to the known instant; every event row also carries the EXTRA label l_anchor_scale_in_sample [causality review MINOR-2] = N.scale_in_sample at the close of the bar its anchor rests on (a BREAKOUT's death bar die_i, an SFP's harden bar) OR at the known close (a tuning pick: that close <= the era cut; a whole-tape fallback True; frozen3.0 False). It is a label only: every grid / base / null count stays on l_scale_in_sample, and the rows where the two differ are counted in §2.
- [LEAN-HEPHAESTUS] R4-9 PARALLELISM [AM-2]: the runner starts no process; units run in-process (serial) or in fresh interpreters started by the caller; the merge alone writes the files of record.
- [LEAN-HEPHAESTUS] R4-10 SCAN LEDGER [L-R.6(a) 'every evaluated touch is a row']: R4_SCAN files N's first-retest scan rows verbatim (N.first_retest_scan: tap89 / tap127 / tap200 and the memory line; seq, touch, known_at = touch + 3 / + 6, verdict, first hold; era by the known_at close, 'beyond_pin' where a truncated row's known_at passes the tape); R4_DEATHS files every death of N.events with, per band, its evaluated-touch count and its END: hold (a first hold), truncated, failed-out (every touch in the candidacy window failed), no-touch.

## Files

| file | rows | content sha256 (parquet: canonical csv) |
|---|---|---|
| R4_EVENTS.parquet | 71889 | 25b72fdb7a9f5c166a2e40d5645524e30f553e3c23017286b0c83e891d9fadb7 |
| R4_GRID.parquet | 180684 | 4eab273ecf28ce147d6ae148a712710f4f58f5d8e01a4c7a45ace627065576ac |
| R4_BASE.parquet | 67140 | fd55ce37c316a2329b901b5b5f03706fa5c4f7ad8886d8fb34b9f1f3804bfdb4 |
| R4_NULL.parquet | 100764 | cd03d8d6c53071671748e01db1dd78a4936b301b33594ee65683f54ff785d541 |
| R4_NULL_BOXES.parquet | 216200 | fea807c11c867f4262daf01b064cd4407ba8756791507cde4c20a6a0ed3609b8 |
| R4_SCAN.parquet | 47403 | 7545b95ce075ee0d81a29b71b59d7c4d9b3a6066debe4457d30e1e0c177fd057 |
| R4_DEATHS.parquet | 10796 | dd362766de146554fe480b10d0ff450d61a036754d6d9b531498a7df15429c00 |

## 1 · TC10 continuity [AM-1] — frozen3.0 · one-shot · 4h · POOLED:CLASSIC5 · tap89 · H20 NET

| era | TC10 filed n | TC10 filed NET | TC10 window replayed in TC11 code n | replay NET | TC11 n | TC11 NET | TC11 − TC10 |
|---|---|---|---|---|---|---|---|
| ALL | 236 | +0.680674 | 236 | +0.680674 | 236 | +0.680674 | +0.000000 |
| tuning | 148 | +0.670740 | 148 | +0.670740 | 148 | +0.670740 | +0.000000 |
| holdout | 88 | +0.705605 | 88 | +0.705605 | 88 | +0.705605 | +0.000000 |

- replay == filed (n, n_events, median, toll, NET at 8 dp, every era): **True**.
- extra 4h bars per asset (TC11 pin 2026-09-25T00:00Z vs TC10 pin 2026-09-21T16:00Z): {'BTCUSDT': 20, 'ETHUSDT': 20, 'SOLUSDT': 20, 'NEARUSDT': 20, 'ZECUSDT': 20}.
- events: TC10 window 236, TC11 236; in both 236 (H20 term identical or censored in both: 236; censored in the TC10 window and uncensored now: 0; term moved: 0); only in TC11 0 (known after the TC10 window: 0); only in the TC10 window 0.
  - last_hold: BTCUSDT: last tap89 one-shot hold known at bar 15344 = 75 bars before the TC10 window's last bar
  - last_hold: ETHUSDT: last tap89 one-shot hold known at bar 14591 = 351 bars before the TC10 window's last bar
  - last_hold: SOLUSDT: last tap89 one-shot hold known at bar 12742 = 448 bars before the TC10 window's last bar
  - last_hold: NEARUSDT: last tap89 one-shot hold known at bar 12824 = 179 bars before the TC10 window's last bar
  - last_hold: ZECUSDT: last tap89 one-shot hold known at bar 14479 = 42 bars before the TC10 window's last bar
  - new_deaths: none
  - uncensored: none
  - only_tc11: none
  - only_tc10: none
  - moved: none
- explanation: the 20 extra 4h bars move nothing in this cell — no tap89 one-shot hold becomes known in them (only-TC11: none), no CLASSIC5 macro death (frozen 3.0) falls in them, and every hold of the TC10 window was known at least 42 bars before its edge (uncensored at H20 then) — so the event set, every H20 term and every toll are the same; TC11 == TC10 at 8 dp.

## 2 · Honesty labels per lens [L-R.2, AM-4]

| asset | lens | pick of record | window | stability changed | L+1 | L+1 pick | L+1 window | L+1 stability changed |
|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | 1.75 | tuning | True | 4h | 2.0 | tuning | False |
| BTCUSDT | 4h | 2.0 | tuning | False | 12h | 2.0 | tuning | True |
| BTCUSDT | 12h | 2.0 | tuning | True | 1d | 2.25 | tuning | True |
| BTCUSDT | 1d | 2.25 | tuning | True | 1w | 2.5 | whole-tape (fallback) | None |
| ETHUSDT | 1h | 2.0 | tuning | False | 4h | 2.0 | tuning | False |
| ETHUSDT | 4h | 2.0 | tuning | False | 12h | 1.5 | tuning | True |
| ETHUSDT | 12h | 1.5 | tuning | True | 1d | 2.0 | tuning | False |
| ETHUSDT | 1d | 2.0 | tuning | False | 1w | 3.0 | whole-tape (fallback) | None |
| SOLUSDT | 1h | 1.75 | tuning | True | 4h | 2.0 | tuning | False |
| SOLUSDT | 4h | 2.0 | tuning | False | 12h | 2.25 | tuning | True |
| SOLUSDT | 12h | 2.25 | tuning | True | 1d | 2.25 | tuning | True |
| SOLUSDT | 1d | 2.25 | tuning | True | 1w | 1.75 | whole-tape (fallback) | None |
| NEARUSDT | 1h | 1.75 | tuning | True | 4h | 1.75 | tuning | True |
| NEARUSDT | 4h | 1.75 | tuning | True | 12h | 2.25 | tuning | False |
| NEARUSDT | 12h | 2.25 | tuning | False | 1d | 2.0 | tuning | False |
| NEARUSDT | 1d | 2.0 | tuning | False | 1w | 3.0 | whole-tape (fallback) | None |
| ZECUSDT | 1h | 2.0 | tuning | False | 4h | 2.0 | tuning | False |
| ZECUSDT | 4h | 2.0 | tuning | False | 12h | 2.0 | tuning | False |
| ZECUSDT | 12h | 2.0 | tuning | False | 1d | 2.5 | tuning | False |
| ZECUSDT | 1d | 2.5 | tuning | False | 1w | 2.5 | whole-tape (fallback) | None |
| ENAUSDT | 1h | 1.5 | tuning | True | 4h | 2.75 | tuning | False |
| ENAUSDT | 4h | 2.75 | tuning | False | NA | — | — | — |
| ENAUSDT | 1d | 2.0 | whole-tape (fallback) | None | NA | — | — | — |
| PUMPUSDT | 1h | 2.0 | whole-tape (fallback) | None | 4h | 2.25 | whole-tape (fallback) | None |
| PUMPUSDT | 4h | 2.25 | whole-tape (fallback) | None | NA | — | — | — |
| PUMPUSDT | 1d | 1.75 | whole-tape (fallback) | None | NA | — | — | — |
| HYPEUSDT | 1h | 2.0 | whole-tape (fallback) | None | 4h | 1.75 | whole-tape (fallback) | None |
| HYPEUSDT | 4h | 1.75 | whole-tape (fallback) | None | NA | — | — | — |
| HYPEUSDT | 1d | 2.25 | whole-tape (fallback) | None | NA | — | — | — |
| MNTUSDT_BYBIT | 1h | 2.25 | tuning | True | 4h | 2.0 | tuning | True |
| MNTUSDT_BYBIT | 4h | 2.0 | tuning | True | NA | — | — | — |
| MNTUSDT_BYBIT | 1d | 2.25 | whole-tape (fallback) | None | NA | — | — | — |
| SUIUSDT | 1h | 2.0 | tuning | True | 4h | 2.25 | tuning | False |
| SUIUSDT | 4h | 2.25 | tuning | False | NA | — | — | — |
| SUIUSDT | 1d | 2.25 | tuning | False | NA | — | — | — |
| LTCUSDT | 1h | 1.75 | tuning | True | 4h | 2.0 | tuning | False |
| LTCUSDT | 4h | 2.0 | tuning | False | NA | — | — | — |
| LTCUSDT | 1d | 2.25 | tuning | False | NA | — | — | — |
| XMRUSDT | 1h | 1.5 | tuning | True | 4h | 1.75 | tuning | True |
| XMRUSDT | 4h | 1.75 | tuning | True | NA | — | — | — |
| XMRUSDT | 1d | 1.5 | tuning | True | NA | — | — | — |
| BNBUSDT | 1h | 1.75 | tuning | True | 4h | 2.0 | tuning | False |
| BNBUSDT | 4h | 2.0 | tuning | False | NA | — | — | — |
| BNBUSDT | 1d | 1.75 | tuning | True | NA | — | — | — |
| UNIUSDT | 1h | 2.0 | tuning | False | 4h | 2.0 | tuning | True |
| UNIUSDT | 4h | 2.0 | tuning | True | NA | — | — | — |
| UNIUSDT | 1d | 2.25 | tuning | False | NA | — | — | — |
| 1000PEPEUSDT | 1h | 1.75 | tuning | False | 4h | 2.0 | tuning | True |
| 1000PEPEUSDT | 4h | 2.0 | tuning | True | NA | — | — | — |
| 1000PEPEUSDT | 1d | 3.0 | tuning | True | NA | — | — | — |
| DOGEUSDT | 1h | 1.75 | tuning | False | 4h | 1.75 | tuning | True |
| DOGEUSDT | 4h | 1.75 | tuning | True | NA | — | — | — |
| DOGEUSDT | 1d | 2.25 | tuning | True | NA | — | — | — |
| 1000BONKUSDT | 1h | 2.0 | tuning | True | 4h | 2.0 | tuning | False |
| 1000BONKUSDT | 4h | 2.0 | tuning | False | NA | — | — | — |
| 1000BONKUSDT | 1d | 2.0 | whole-tape (fallback) | None | NA | — | — | — |

- **l_anchor_scale_in_sample** (R4_EVENTS, an EXTRA label [R4-8; causality review MINOR-2]) differs from l_scale_in_sample on **75** of 71,889 event rows (75 of them anchor-label True where l_scale_in_sample is False); CLASSIC5 · calibrated · BREAKOUT: 29 of 15,535. A row differs only when the bar its anchor rests on closes at or before the era cut and its known_at closes after it, under a tuning pick. It is a label only: no grid / base / null figure is keyed to it (n_l_scale_in_sample counts l_scale_in_sample).

| panel | lens | scale | family | event rows | rows where the two labels differ |
|---|---|---|---|---|---|
| CLASSIC5 | 1h | calibrated | BRK | 11396 | 11 |
| CLASSIC5 | 1h | calibrated | SFP | 2571 | 0 |
| CLASSIC5 | 1h | frozen3.0 | BRK | 6581 | 0 |
| CLASSIC5 | 1h | frozen3.0 | SFP | 1226 | 0 |
| CLASSIC5 | 4h | calibrated | BRK | 2828 | 10 |
| CLASSIC5 | 4h | calibrated | SFP | 627 | 0 |
| CLASSIC5 | 4h | frozen3.0 | BRK | 1797 | 0 |
| CLASSIC5 | 4h | frozen3.0 | SFP | 289 | 0 |
| CLASSIC5 | 12h | calibrated | BRK | 860 | 1 |
| CLASSIC5 | 12h | calibrated | SFP | 198 | 0 |
| CLASSIC5 | 12h | frozen3.0 | BRK | 546 | 0 |
| CLASSIC5 | 12h | frozen3.0 | SFP | 105 | 0 |
| CLASSIC5 | 1d | calibrated | BRK | 451 | 7 |
| CLASSIC5 | 1d | calibrated | SFP | 77 | 0 |
| CLASSIC5 | 1d | frozen3.0 | BRK | 275 | 0 |
| CLASSIC5 | 1d | frozen3.0 | SFP | 55 | 0 |
| UNSEEN12 | 1h | calibrated | BRK | 17247 | 18 |
| UNSEEN12 | 1h | calibrated | SFP | 4390 | 0 |
| UNSEEN12 | 1h | frozen3.0 | BRK | 9545 | 0 |
| UNSEEN12 | 1h | frozen3.0 | SFP | 1931 | 0 |
| UNSEEN12 | 4h | calibrated | BRK | 3894 | 17 |
| UNSEEN12 | 4h | calibrated | SFP | 930 | 0 |
| UNSEEN12 | 4h | frozen3.0 | BRK | 2395 | 0 |
| UNSEEN12 | 4h | frozen3.0 | SFP | 488 | 0 |
| UNSEEN12 | 1d | calibrated | BRK | 648 | 11 |
| UNSEEN12 | 1d | calibrated | SFP | 120 | 0 |
| UNSEEN12 | 1d | frozen3.0 | BRK | 357 | 0 |
| UNSEEN12 | 1d | frozen3.0 | SFP | 62 | 0 |

## 3 · Event counts, per panel (per-asset counts in R4_EVENTS.parquet)

| panel | lens | scale | event | n ALL | n tuning | n holdout | long | short |
|---|---|---|---|---|---|---|---|---|
| CLASSIC5 | 1h | calibrated | BRK_tap89_first | 1790 | 1146 | 644 | 955 | 835 |
| CLASSIC5 | 1h | calibrated | BRK_tap89_oneshot | 1508 | 964 | 544 | 816 | 692 |
| CLASSIC5 | 1h | calibrated | BRK_tap127_first | 1588 | 1020 | 568 | 839 | 749 |
| CLASSIC5 | 1h | calibrated | BRK_tap127_oneshot | 1372 | 889 | 483 | 732 | 640 |
| CLASSIC5 | 1h | calibrated | BRK_tap200_first | 1296 | 821 | 475 | 675 | 621 |
| CLASSIC5 | 1h | calibrated | BRK_tap200_oneshot | 1142 | 724 | 418 | 593 | 549 |
| CLASSIC5 | 1h | calibrated | BRK_mem_first | 1390 | 903 | 487 | 759 | 631 |
| CLASSIC5 | 1h | calibrated | BRK_mem_oneshot | 1310 | 852 | 458 | 710 | 600 |
| CLASSIC5 | 1h | calibrated | SFP_harden | 2571 | 1626 | 945 | 1257 | 1314 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap89_first | 1021 | 672 | 349 | 558 | 463 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap89_oneshot | 812 | 536 | 276 | 447 | 365 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap127_first | 971 | 631 | 340 | 536 | 435 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap127_oneshot | 787 | 518 | 269 | 441 | 346 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap200_first | 879 | 562 | 317 | 486 | 393 |
| CLASSIC5 | 1h | frozen3.0 | BRK_tap200_oneshot | 715 | 455 | 260 | 398 | 317 |
| CLASSIC5 | 1h | frozen3.0 | BRK_mem_first | 752 | 485 | 267 | 410 | 342 |
| CLASSIC5 | 1h | frozen3.0 | BRK_mem_oneshot | 644 | 416 | 228 | 352 | 292 |
| CLASSIC5 | 1h | frozen3.0 | SFP_harden | 1226 | 797 | 429 | 596 | 630 |
| CLASSIC5 | 4h | calibrated | BRK_tap89_first | 450 | 287 | 163 | 230 | 220 |
| CLASSIC5 | 4h | calibrated | BRK_tap89_oneshot | 392 | 250 | 142 | 208 | 184 |
| CLASSIC5 | 4h | calibrated | BRK_tap127_first | 403 | 257 | 146 | 212 | 191 |
| CLASSIC5 | 4h | calibrated | BRK_tap127_oneshot | 358 | 225 | 133 | 194 | 164 |
| CLASSIC5 | 4h | calibrated | BRK_tap200_first | 333 | 214 | 119 | 178 | 155 |
| CLASSIC5 | 4h | calibrated | BRK_tap200_oneshot | 295 | 193 | 102 | 160 | 135 |
| CLASSIC5 | 4h | calibrated | BRK_mem_first | 310 | 203 | 107 | 153 | 157 |
| CLASSIC5 | 4h | calibrated | BRK_mem_oneshot | 287 | 187 | 100 | 144 | 143 |
| CLASSIC5 | 4h | calibrated | SFP_harden | 627 | 396 | 231 | 315 | 312 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap89_first | 281 | 180 | 101 | 145 | 136 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap89_oneshot | 236 | 148 | 88 | 127 | 109 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap127_first | 266 | 168 | 98 | 141 | 125 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap127_oneshot | 221 | 138 | 83 | 123 | 98 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap200_first | 234 | 152 | 82 | 127 | 107 |
| CLASSIC5 | 4h | frozen3.0 | BRK_tap200_oneshot | 191 | 128 | 63 | 108 | 83 |
| CLASSIC5 | 4h | frozen3.0 | BRK_mem_first | 196 | 126 | 70 | 97 | 99 |
| CLASSIC5 | 4h | frozen3.0 | BRK_mem_oneshot | 172 | 110 | 62 | 84 | 88 |
| CLASSIC5 | 4h | frozen3.0 | SFP_harden | 289 | 189 | 100 | 150 | 139 |
| CLASSIC5 | 12h | calibrated | BRK_tap89_first | 137 | 87 | 50 | 79 | 58 |
| CLASSIC5 | 12h | calibrated | BRK_tap89_oneshot | 115 | 74 | 41 | 66 | 49 |
| CLASSIC5 | 12h | calibrated | BRK_tap127_first | 118 | 73 | 45 | 70 | 48 |
| CLASSIC5 | 12h | calibrated | BRK_tap127_oneshot | 101 | 63 | 38 | 58 | 43 |
| CLASSIC5 | 12h | calibrated | BRK_tap200_first | 99 | 59 | 40 | 54 | 45 |
| CLASSIC5 | 12h | calibrated | BRK_tap200_oneshot | 86 | 55 | 31 | 49 | 37 |
| CLASSIC5 | 12h | calibrated | BRK_mem_first | 100 | 63 | 37 | 58 | 42 |
| CLASSIC5 | 12h | calibrated | BRK_mem_oneshot | 104 | 66 | 38 | 58 | 46 |
| CLASSIC5 | 12h | calibrated | SFP_harden | 198 | 105 | 93 | 90 | 108 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap89_first | 84 | 46 | 38 | 51 | 33 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap89_oneshot | 69 | 39 | 30 | 41 | 28 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap127_first | 79 | 43 | 36 | 49 | 30 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap127_oneshot | 64 | 35 | 29 | 38 | 26 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap200_first | 69 | 38 | 31 | 42 | 27 |
| CLASSIC5 | 12h | frozen3.0 | BRK_tap200_oneshot | 62 | 35 | 27 | 37 | 25 |
| CLASSIC5 | 12h | frozen3.0 | BRK_mem_first | 61 | 33 | 28 | 36 | 25 |
| CLASSIC5 | 12h | frozen3.0 | BRK_mem_oneshot | 58 | 32 | 26 | 34 | 24 |
| CLASSIC5 | 12h | frozen3.0 | SFP_harden | 105 | 56 | 49 | 49 | 56 |
| CLASSIC5 | 1d | calibrated | BRK_tap89_first | 71 | 42 | 29 | 43 | 28 |
| CLASSIC5 | 1d | calibrated | BRK_tap89_oneshot | 64 | 37 | 27 | 40 | 24 |
| CLASSIC5 | 1d | calibrated | BRK_tap127_first | 60 | 37 | 23 | 40 | 20 |
| CLASSIC5 | 1d | calibrated | BRK_tap127_oneshot | 54 | 35 | 19 | 38 | 16 |
| CLASSIC5 | 1d | calibrated | BRK_tap200_first | 51 | 29 | 22 | 37 | 14 |
| CLASSIC5 | 1d | calibrated | BRK_tap200_oneshot | 41 | 26 | 15 | 33 | 8 |
| CLASSIC5 | 1d | calibrated | BRK_mem_first | 56 | 31 | 25 | 29 | 27 |
| CLASSIC5 | 1d | calibrated | BRK_mem_oneshot | 54 | 32 | 22 | 29 | 25 |
| CLASSIC5 | 1d | calibrated | SFP_harden | 77 | 40 | 37 | 46 | 31 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap89_first | 43 | 26 | 17 | 23 | 20 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap89_oneshot | 35 | 22 | 13 | 21 | 14 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap127_first | 38 | 24 | 14 | 22 | 16 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap127_oneshot | 31 | 22 | 9 | 20 | 11 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap200_first | 35 | 19 | 16 | 21 | 14 |
| CLASSIC5 | 1d | frozen3.0 | BRK_tap200_oneshot | 28 | 17 | 11 | 19 | 9 |
| CLASSIC5 | 1d | frozen3.0 | BRK_mem_first | 35 | 21 | 14 | 17 | 18 |
| CLASSIC5 | 1d | frozen3.0 | BRK_mem_oneshot | 30 | 19 | 11 | 15 | 15 |
| CLASSIC5 | 1d | frozen3.0 | SFP_harden | 55 | 34 | 21 | 35 | 20 |
| UNSEEN12 | 1h | calibrated | BRK_tap89_first | 2690 | 1314 | 1376 | 1370 | 1320 |
| UNSEEN12 | 1h | calibrated | BRK_tap89_oneshot | 2326 | 1147 | 1179 | 1206 | 1120 |
| UNSEEN12 | 1h | calibrated | BRK_tap127_first | 2393 | 1176 | 1217 | 1237 | 1156 |
| UNSEEN12 | 1h | calibrated | BRK_tap127_oneshot | 2105 | 1044 | 1061 | 1096 | 1009 |
| UNSEEN12 | 1h | calibrated | BRK_tap200_first | 2000 | 976 | 1024 | 1055 | 945 |
| UNSEEN12 | 1h | calibrated | BRK_tap200_oneshot | 1741 | 851 | 890 | 936 | 805 |
| UNSEEN12 | 1h | calibrated | BRK_mem_first | 2089 | 1045 | 1044 | 1118 | 971 |
| UNSEEN12 | 1h | calibrated | BRK_mem_oneshot | 1903 | 951 | 952 | 1013 | 890 |
| UNSEEN12 | 1h | calibrated | SFP_harden | 4390 | 2142 | 2248 | 2177 | 2213 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap89_first | 1468 | 707 | 761 | 746 | 722 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap89_oneshot | 1210 | 593 | 617 | 638 | 572 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap127_first | 1397 | 678 | 719 | 723 | 674 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap127_oneshot | 1135 | 569 | 566 | 597 | 538 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap200_first | 1283 | 626 | 657 | 679 | 604 |
| UNSEEN12 | 1h | frozen3.0 | BRK_tap200_oneshot | 1041 | 506 | 535 | 548 | 493 |
| UNSEEN12 | 1h | frozen3.0 | BRK_mem_first | 1107 | 534 | 573 | 574 | 533 |
| UNSEEN12 | 1h | frozen3.0 | BRK_mem_oneshot | 904 | 440 | 464 | 477 | 427 |
| UNSEEN12 | 1h | frozen3.0 | SFP_harden | 1931 | 918 | 1013 | 914 | 1017 |
| UNSEEN12 | 4h | calibrated | BRK_tap89_first | 619 | 320 | 299 | 339 | 280 |
| UNSEEN12 | 4h | calibrated | BRK_tap89_oneshot | 524 | 278 | 246 | 294 | 230 |
| UNSEEN12 | 4h | calibrated | BRK_tap127_first | 535 | 275 | 260 | 301 | 234 |
| UNSEEN12 | 4h | calibrated | BRK_tap127_oneshot | 465 | 243 | 222 | 268 | 197 |
| UNSEEN12 | 4h | calibrated | BRK_tap200_first | 452 | 241 | 211 | 262 | 190 |
| UNSEEN12 | 4h | calibrated | BRK_tap200_oneshot | 388 | 206 | 182 | 233 | 155 |
| UNSEEN12 | 4h | calibrated | BRK_mem_first | 470 | 246 | 224 | 257 | 213 |
| UNSEEN12 | 4h | calibrated | BRK_mem_oneshot | 441 | 235 | 206 | 244 | 197 |
| UNSEEN12 | 4h | calibrated | SFP_harden | 930 | 455 | 475 | 468 | 462 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap89_first | 378 | 172 | 206 | 191 | 187 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap89_oneshot | 300 | 142 | 158 | 161 | 139 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap127_first | 357 | 166 | 191 | 183 | 174 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap127_oneshot | 285 | 136 | 149 | 158 | 127 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap200_first | 311 | 155 | 156 | 169 | 142 |
| UNSEEN12 | 4h | frozen3.0 | BRK_tap200_oneshot | 248 | 128 | 120 | 148 | 100 |
| UNSEEN12 | 4h | frozen3.0 | BRK_mem_first | 277 | 134 | 143 | 153 | 124 |
| UNSEEN12 | 4h | frozen3.0 | BRK_mem_oneshot | 239 | 113 | 126 | 136 | 103 |
| UNSEEN12 | 4h | frozen3.0 | SFP_harden | 488 | 221 | 267 | 228 | 260 |
| UNSEEN12 | 1d | calibrated | BRK_tap89_first | 102 | 51 | 51 | 55 | 47 |
| UNSEEN12 | 1d | calibrated | BRK_tap89_oneshot | 83 | 43 | 40 | 48 | 35 |
| UNSEEN12 | 1d | calibrated | BRK_tap127_first | 90 | 44 | 46 | 47 | 43 |
| UNSEEN12 | 1d | calibrated | BRK_tap127_oneshot | 71 | 37 | 34 | 38 | 33 |
| UNSEEN12 | 1d | calibrated | BRK_tap200_first | 70 | 36 | 34 | 34 | 36 |
| UNSEEN12 | 1d | calibrated | BRK_tap200_oneshot | 58 | 30 | 28 | 31 | 27 |
| UNSEEN12 | 1d | calibrated | BRK_mem_first | 92 | 46 | 46 | 51 | 41 |
| UNSEEN12 | 1d | calibrated | BRK_mem_oneshot | 82 | 41 | 41 | 48 | 34 |
| UNSEEN12 | 1d | calibrated | SFP_harden | 120 | 60 | 60 | 66 | 54 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap89_first | 57 | 31 | 26 | 29 | 28 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap89_oneshot | 43 | 24 | 19 | 25 | 18 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap127_first | 55 | 29 | 26 | 29 | 26 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap127_oneshot | 39 | 22 | 17 | 20 | 19 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap200_first | 43 | 24 | 19 | 25 | 18 |
| UNSEEN12 | 1d | frozen3.0 | BRK_tap200_oneshot | 31 | 18 | 13 | 20 | 11 |
| UNSEEN12 | 1d | frozen3.0 | BRK_mem_first | 51 | 25 | 26 | 26 | 25 |
| UNSEEN12 | 1d | frozen3.0 | BRK_mem_oneshot | 38 | 17 | 21 | 21 | 17 |
| UNSEEN12 | 1d | frozen3.0 | SFP_harden | 62 | 29 | 33 | 47 | 15 |

## 4 · The grid of record — POOLED:CLASSIC5 · calibrated · cell law record (whole over lens x event x L+1 cell x direction; frozen3.0 and the twin laws in R4_GRID.md)

| lens | scale | event | law | L+1 cell | dir | n ALL H20 | NET ALL H20 | Δcell ALL H20 | n ALL H100 | NET ALL H100 | Δcell ALL H100 | n tuning H20 | NET tuning H20 | Δcell tuning H20 | n tuning H100 | NET tuning H100 | Δcell tuning H100 | n holdout H20 | NET holdout H20 | Δcell holdout H20 | n holdout H100 | NET holdout H100 | Δcell holdout H100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1h | calibrated | BRK_tap89_first | record | ALL | both | 1789 | -0.086 | +0.048 | 1784 | -0.167 | -0.033 | 1146 | +0.010 | +0.132 | 1146 | -0.097 | +0.025 | 643 | -0.289 | -0.128 | 638 | -0.308 | -0.147 |
| 1h | calibrated | BRK_tap89_first | record | ALL | long | 954 | -0.087 | +0.009 | 951 | +0.117 | +0.046 | 622 | +0.098 | +0.171 | 622 | +0.377 | +0.249 | 332 | -0.485 | -0.342 | 329 | -0.400 | -0.363 |
| 1h | calibrated | BRK_tap89_first | record | ALL | short | 835 | -0.105 | +0.068 | 833 | -0.481 | -0.141 | 524 | -0.058 | +0.113 | 524 | -0.615 | -0.243 | 311 | -0.183 | -0.005 | 309 | -0.248 | +0.036 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | both | 712 | -0.228 | -0.073 | 709 | -0.229 | -0.057 | 456 | -0.138 | -0.009 | 456 | -0.259 | -0.176 | 256 | -0.345 | -0.133 | 253 | -0.142 | +0.193 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | long | 392 | -0.134 | -0.025 | 389 | +0.540 | +0.419 | 260 | +0.033 | +0.095 | 260 | +0.653 | +0.263 | 132 | -0.349 | -0.140 | 129 | +0.153 | +0.513 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | short | 320 | -0.419 | -0.215 | 320 | -0.824 | -0.349 | 196 | -0.429 | -0.224 | 196 | -1.162 | -0.589 | 124 | -0.339 | -0.134 | 124 | -0.215 | +0.083 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | both | 349 | +0.003 | +0.104 | 347 | -0.698 | -0.614 | 217 | +0.125 | +0.228 | 217 | -0.608 | -0.461 | 132 | -0.067 | +0.039 | 130 | -0.984 | -1.000 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | long | 171 | +0.005 | +0.044 | 171 | -0.912 | -1.144 | 104 | +0.229 | +0.255 | 104 | -0.133 | -0.476 | 67 | -0.106 | -0.034 | 67 | -1.461 | -1.482 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | short | 178 | -0.003 | +0.155 | 176 | -0.675 | -0.288 | 113 | -0.051 | +0.120 | 113 | -0.640 | -0.017 | 65 | +0.002 | +0.137 | 63 | -0.753 | -0.765 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | both | 4 | -0.436 | -0.275 | 4 | +0.943 | +1.105 | 3 | -0.408 | -0.254 | 3 | +0.712 | +0.867 | 1 | -0.437 | -0.265 | 1 | +1.202 | +1.374 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | long | 2 | -1.668 | -1.527 | 2 | +0.171 | +0.555 | 2 | -1.668 | -1.542 | 2 | +0.171 | +0.588 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | short | 2 | -0.078 | +0.104 | 2 | +0.964 | +0.903 | 1 | +0.288 | +0.470 | 1 | +0.733 | +0.625 | 1 | -0.437 | -0.266 | 1 | +1.202 | +1.286 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | both | 518 | -0.125 | +0.017 | 518 | +0.100 | +0.242 | 334 | +0.212 | +0.339 | 334 | +0.308 | +0.435 | 184 | -0.585 | -0.425 | 184 | -0.171 | -0.011 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | long | 289 | -0.273 | -0.189 | 289 | +0.148 | -0.089 | 189 | +0.146 | +0.234 | 189 | +0.602 | +0.571 | 100 | -0.689 | -0.623 | 100 | -0.631 | -1.247 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | short | 229 | -0.019 | +0.182 | 229 | -0.028 | +0.493 | 145 | +0.393 | +0.559 | 145 | -0.022 | +0.263 | 84 | -0.315 | -0.060 | 84 | -0.026 | +0.912 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | both | 204 | +0.149 | +0.280 | 204 | -0.237 | -0.106 | 134 | +0.155 | +0.275 | 134 | -0.077 | +0.043 | 70 | +0.112 | +0.274 | 70 | -0.311 | -0.149 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | long | 98 | +0.060 | +0.192 | 98 | -0.177 | +0.019 | 65 | +0.097 | +0.199 | 65 | -0.216 | -0.067 | 33 | -0.020 | +0.196 | 33 | -0.181 | +0.097 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | short | 106 | +0.170 | +0.300 | 106 | -0.276 | -0.209 | 69 | +0.143 | +0.281 | 69 | +0.042 | +0.132 | 37 | +0.286 | +0.394 | 37 | -0.294 | -0.248 |
| 1h | calibrated | BRK_tap89_first | record | NONE | both | 2 | +0.471 | +0.637 | 2 | -3.864 | -3.697 | 2 | +0.471 | +0.637 | 2 | -3.864 | -3.697 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_first | record | NONE | long | 2 | +0.471 | +1.021 | 2 | -3.864 | -2.590 | 2 | +0.471 | +1.021 | 2 | -3.864 | -2.590 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 1508 | -0.066 | +0.068 | 1503 | -0.172 | -0.037 | 964 | +0.046 | +0.168 | 964 | -0.003 | +0.119 | 544 | -0.296 | -0.135 | 539 | -0.652 | -0.492 |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 816 | -0.081 | +0.014 | 813 | +0.196 | +0.125 | 533 | +0.163 | +0.236 | 533 | +0.621 | +0.493 | 283 | -0.513 | -0.369 | 280 | -0.719 | -0.682 |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 692 | -0.060 | +0.113 | 690 | -0.629 | -0.290 | 431 | -0.051 | +0.120 | 431 | -0.643 | -0.272 | 261 | -0.125 | +0.053 | 259 | -0.648 | -0.363 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | both | 624 | -0.227 | -0.072 | 621 | -0.229 | -0.056 | 397 | -0.130 | -0.002 | 397 | -0.273 | -0.189 | 227 | -0.342 | -0.129 | 224 | -0.141 | +0.193 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | long | 348 | -0.111 | -0.002 | 345 | +0.572 | +0.451 | 229 | -0.016 | +0.046 | 229 | +0.624 | +0.233 | 119 | -0.299 | -0.090 | 116 | +0.440 | +0.800 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | short | 276 | -0.416 | -0.212 | 276 | -0.911 | -0.436 | 168 | -0.390 | -0.186 | 168 | -1.250 | -0.676 | 108 | -0.466 | -0.260 | 108 | -0.373 | -0.075 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | both | 284 | -0.016 | +0.085 | 282 | -0.816 | -0.732 | 175 | +0.126 | +0.229 | 175 | -0.080 | +0.067 | 109 | -0.126 | -0.020 | 107 | -1.486 | -1.502 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | long | 142 | -0.016 | +0.023 | 142 | -1.018 | -1.249 | 85 | +0.247 | +0.274 | 85 | +0.012 | -0.331 | 57 | -0.565 | -0.493 | 57 | -2.462 | -2.482 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | short | 142 | -0.012 | +0.145 | 140 | -0.673 | -0.286 | 90 | -0.048 | +0.123 | 90 | -0.273 | +0.350 | 52 | -0.036 | +0.099 | 50 | -1.119 | -1.131 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | both | 3 | -0.408 | -0.247 | 3 | +0.712 | +0.873 | 3 | -0.408 | -0.254 | 3 | +0.712 | +0.867 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | long | 2 | -1.668 | -1.527 | 2 | +0.171 | +0.555 | 2 | -1.668 | -1.542 | 2 | +0.171 | +0.588 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | +0.288 | +0.469 | 1 | +0.733 | +0.671 | 1 | +0.288 | +0.470 | 1 | +0.733 | +0.625 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | both | 414 | +0.034 | +0.176 | 414 | +0.155 | +0.297 | 269 | +0.389 | +0.517 | 269 | +0.328 | +0.455 | 145 | -0.591 | -0.430 | 145 | -0.806 | -0.645 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | long | 236 | -0.241 | -0.158 | 236 | +0.353 | +0.115 | 157 | +0.248 | +0.336 | 157 | +0.909 | +0.878 | 79 | -0.733 | -0.668 | 79 | -0.995 | -1.611 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | short | 178 | +0.211 | +0.411 | 178 | -0.061 | +0.460 | 112 | +0.495 | +0.662 | 112 | -0.385 | -0.100 | 66 | -0.266 | -0.011 | 66 | +0.098 | +1.036 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | both | 181 | +0.205 | +0.336 | 181 | -0.109 | +0.022 | 118 | +0.200 | +0.319 | 118 | +0.199 | +0.319 | 63 | +0.168 | +0.329 | 63 | -0.330 | -0.168 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | long | 86 | +0.060 | +0.192 | 86 | +0.099 | +0.296 | 58 | +0.222 | +0.323 | 58 | +0.479 | +0.629 | 28 | -0.156 | +0.060 | 28 | -0.601 | -0.323 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | short | 95 | +0.290 | +0.420 | 95 | -0.248 | -0.182 | 60 | +0.191 | +0.329 | 60 | +0.152 | +0.242 | 35 | +0.440 | +0.547 | 35 | -0.287 | -0.242 |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | both | 2 | +0.471 | +0.637 | 2 | -3.864 | -3.697 | 2 | +0.471 | +0.637 | 2 | -3.864 | -3.697 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | long | 2 | +0.471 | +1.021 | 2 | -3.864 | -2.590 | 2 | +0.471 | +1.021 | 2 | -3.864 | -2.590 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | ALL | both | 1587 | -0.248 | -0.113 | 1585 | -0.237 | -0.103 | 1020 | -0.175 | -0.053 | 1020 | -0.133 | -0.011 | 567 | -0.342 | -0.181 | 565 | -0.471 | -0.310 |
| 1h | calibrated | BRK_tap127_first | record | ALL | long | 838 | -0.211 | -0.115 | 836 | -0.059 | -0.129 | 544 | -0.114 | -0.040 | 544 | +0.457 | +0.330 | 294 | -0.468 | -0.325 | 292 | -0.982 | -0.945 |
| 1h | calibrated | BRK_tap127_first | record | ALL | short | 749 | -0.277 | -0.104 | 749 | -0.439 | -0.100 | 476 | -0.304 | -0.134 | 476 | -0.729 | -0.357 | 273 | -0.259 | -0.080 | 273 | +0.043 | +0.328 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | both | 576 | -0.270 | -0.115 | 574 | -0.080 | +0.092 | 375 | -0.212 | -0.084 | 375 | +0.030 | +0.114 | 201 | -0.344 | -0.132 | 199 | -0.399 | -0.065 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | long | 315 | -0.101 | +0.008 | 313 | +0.095 | -0.026 | 212 | -0.029 | +0.033 | 212 | +0.632 | +0.241 | 103 | -0.147 | +0.063 | 101 | -1.209 | -0.850 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | short | 261 | -0.559 | -0.355 | 261 | -0.486 | -0.012 | 163 | -0.457 | -0.253 | 163 | -0.977 | -0.403 | 98 | -0.614 | -0.409 | 98 | +0.248 | +0.545 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | both | 337 | -0.557 | -0.456 | 337 | -0.691 | -0.607 | 206 | -0.462 | -0.359 | 206 | -0.743 | -0.596 | 131 | -0.663 | -0.556 | 131 | -0.731 | -0.747 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | long | 170 | -0.542 | -0.503 | 170 | -0.933 | -1.164 | 101 | -0.168 | -0.142 | 101 | -0.170 | -0.513 | 69 | -1.033 | -0.961 | 69 | -1.743 | -1.763 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | short | 167 | -0.598 | -0.440 | 167 | -0.674 | -0.287 | 105 | -0.648 | -0.478 | 105 | -1.070 | -0.447 | 62 | -0.063 | +0.072 | 62 | -0.272 | -0.284 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | both | 3 | +0.365 | +0.527 | 3 | +2.288 | +2.449 | 2 | +0.115 | +0.269 | 2 | +3.352 | +3.506 | 1 | +0.379 | +0.552 | 1 | +2.302 | +2.474 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | long | 1 | -0.408 | -0.267 | 1 | +5.845 | +6.229 | 1 | -0.408 | -0.282 | 1 | +5.845 | +6.262 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | short | 2 | +0.516 | +0.697 | 2 | +1.587 | +1.525 | 1 | +0.658 | +0.841 | 1 | +0.878 | +0.770 | 1 | +0.379 | +0.550 | 1 | +2.302 | +2.387 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | both | 528 | -0.134 | +0.008 | 528 | +0.109 | +0.251 | 342 | +0.009 | +0.136 | 342 | +0.046 | +0.173 | 186 | -0.352 | -0.191 | 186 | +0.149 | +0.309 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | long | 290 | -0.362 | -0.279 | 290 | +0.159 | -0.079 | 191 | -0.158 | -0.070 | 191 | +0.704 | +0.673 | 99 | -0.634 | -0.568 | 99 | -0.166 | -0.783 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | short | 238 | +0.029 | +0.230 | 238 | +0.063 | +0.584 | 151 | +0.138 | +0.305 | 151 | -0.110 | +0.175 | 87 | -0.184 | +0.071 | 87 | +0.348 | +1.285 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | both | 141 | +0.018 | +0.149 | 141 | -0.840 | -0.708 | 93 | -0.022 | +0.097 | 93 | -0.717 | -0.597 | 48 | +0.178 | +0.339 | 48 | -0.881 | -0.719 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | long | 60 | -0.192 | -0.059 | 60 | -0.543 | -0.347 | 37 | -0.192 | -0.091 | 37 | -0.291 | -0.142 | 23 | -0.192 | +0.024 | 23 | -0.825 | -0.547 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | short | 81 | +0.098 | +0.228 | 81 | -0.883 | -0.817 | 56 | +0.063 | +0.201 | 56 | -0.851 | -0.761 | 25 | +0.547 | +0.655 | 25 | -0.897 | -0.852 |
| 1h | calibrated | BRK_tap127_first | record | NONE | both | 2 | -0.192 | -0.025 | 2 | -6.974 | -6.807 | 2 | -0.192 | -0.025 | 2 | -6.974 | -6.807 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | NONE | long | 2 | -0.192 | +0.359 | 2 | -6.974 | -5.700 | 2 | -0.192 | +0.359 | 2 | -6.974 | -5.700 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 1371 | -0.314 | -0.180 | 1369 | -0.303 | -0.169 | 889 | -0.221 | -0.099 | 889 | -0.110 | +0.012 | 482 | -0.491 | -0.330 | 480 | -0.678 | -0.518 |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 731 | -0.264 | -0.169 | 729 | -0.144 | -0.215 | 481 | -0.119 | -0.046 | 481 | +0.523 | +0.395 | 250 | -0.687 | -0.544 | 248 | -1.198 | -1.161 |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 640 | -0.360 | -0.187 | 640 | -0.564 | -0.224 | 408 | -0.368 | -0.198 | 408 | -0.834 | -0.462 | 232 | -0.319 | -0.141 | 232 | -0.015 | +0.269 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | both | 525 | -0.313 | -0.158 | 523 | -0.081 | +0.091 | 345 | -0.216 | -0.087 | 345 | -0.018 | +0.065 | 180 | -0.409 | -0.197 | 178 | -0.365 | -0.030 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | long | 288 | -0.105 | +0.004 | 286 | +0.171 | +0.051 | 195 | -0.018 | +0.043 | 195 | +0.642 | +0.251 | 93 | -0.229 | -0.019 | 91 | -1.157 | -0.798 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | short | 237 | -0.573 | -0.368 | 237 | -0.544 | -0.069 | 150 | -0.555 | -0.351 | 150 | -1.045 | -0.471 | 87 | -0.822 | -0.616 | 87 | +0.135 | +0.433 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | both | 284 | -0.647 | -0.546 | 284 | -0.922 | -0.838 | 174 | -0.552 | -0.449 | 174 | -0.738 | -0.591 | 110 | -0.863 | -0.756 | 110 | -1.205 | -1.221 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | long | 144 | -0.817 | -0.777 | 144 | -1.634 | -1.866 | 86 | -0.377 | -0.351 | 86 | -0.558 | -0.901 | 58 | -1.395 | -1.323 | 58 | -2.424 | -2.445 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | short | 140 | -0.571 | -0.413 | 140 | -0.448 | -0.061 | 88 | -0.625 | -0.455 | 88 | -0.901 | -0.279 | 52 | -0.150 | -0.014 | 52 | -0.176 | -0.188 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | both | 2 | +0.115 | +0.276 | 2 | +3.352 | +3.513 | 2 | +0.115 | +0.269 | 2 | +3.352 | +3.506 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | long | 1 | -0.408 | -0.267 | 1 | +5.845 | +6.229 | 1 | -0.408 | -0.282 | 1 | +5.845 | +6.262 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | +0.658 | +0.840 | 1 | +0.878 | +0.817 | 1 | +0.658 | +0.841 | 1 | +0.878 | +0.770 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | both | 434 | -0.269 | -0.127 | 434 | +0.038 | +0.180 | 285 | +0.020 | +0.148 | 285 | +0.309 | +0.436 | 149 | -0.535 | -0.374 | 149 | -0.656 | -0.495 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | long | 243 | -0.381 | -0.297 | 243 | +0.350 | +0.113 | 165 | -0.005 | +0.083 | 165 | +0.811 | +0.781 | 78 | -0.903 | -0.838 | 78 | -0.968 | -1.585 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | short | 191 | -0.012 | +0.189 | 191 | -0.076 | +0.445 | 120 | +0.096 | +0.262 | 120 | -0.505 | -0.220 | 71 | -0.299 | -0.044 | 71 | +0.198 | +1.136 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | both | 124 | -0.033 | +0.098 | 124 | -0.858 | -0.726 | 81 | -0.175 | -0.055 | 81 | -0.852 | -0.733 | 43 | +0.061 | +0.223 | 43 | -0.854 | -0.692 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | long | 53 | -0.375 | -0.243 | 53 | -0.794 | -0.598 | 32 | -0.319 | -0.218 | 32 | -0.584 | -0.435 | 21 | -0.407 | -0.191 | 21 | -0.825 | -0.547 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | short | 71 | +0.089 | +0.219 | 71 | -0.955 | -0.889 | 49 | -0.057 | +0.081 | 49 | -0.960 | -0.870 | 22 | +0.697 | +0.805 | 22 | -0.937 | -0.892 |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | both | 2 | -0.192 | -0.025 | 2 | -6.974 | -6.807 | 2 | -0.192 | -0.025 | 2 | -6.974 | -6.807 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | long | 2 | -0.192 | +0.359 | 2 | -6.974 | -5.700 | 2 | -0.192 | +0.359 | 2 | -6.974 | -5.700 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | ALL | both | 1295 | -0.104 | +0.030 | 1295 | -0.039 | +0.096 | 821 | +0.010 | +0.132 | 821 | +0.043 | +0.165 | 474 | -0.388 | -0.228 | 474 | -0.360 | -0.199 |
| 1h | calibrated | BRK_tap200_first | record | ALL | long | 674 | -0.143 | -0.047 | 674 | +0.157 | +0.086 | 429 | +0.005 | +0.079 | 429 | +0.832 | +0.705 | 245 | -0.545 | -0.401 | 245 | -0.776 | -0.739 |
| 1h | calibrated | BRK_tap200_first | record | ALL | short | 621 | -0.065 | +0.109 | 621 | -0.407 | -0.067 | 392 | +0.014 | +0.185 | 392 | -0.461 | -0.089 | 229 | -0.196 | -0.018 | 229 | +0.105 | +0.390 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | both | 427 | +0.110 | +0.265 | 427 | +0.156 | +0.328 | 258 | +0.250 | +0.379 | 258 | +0.189 | +0.273 | 169 | -0.283 | -0.070 | 169 | +0.122 | +0.456 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | long | 223 | +0.174 | +0.283 | 223 | +0.616 | +0.495 | 138 | +0.233 | +0.294 | 138 | +0.999 | +0.608 | 85 | -0.063 | +0.147 | 85 | -0.103 | +0.256 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | short | 204 | -0.187 | +0.017 | 204 | -0.223 | +0.252 | 120 | +0.298 | +0.503 | 120 | -0.692 | -0.119 | 84 | -0.615 | -0.410 | 84 | +0.729 | +1.027 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | both | 302 | -0.295 | -0.194 | 302 | -0.840 | -0.756 | 190 | -0.098 | +0.005 | 190 | -0.636 | -0.489 | 112 | -0.579 | -0.473 | 112 | -0.936 | -0.951 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | long | 151 | -0.143 | -0.104 | 151 | -0.640 | -0.871 | 92 | +0.330 | +0.356 | 92 | +0.560 | +0.217 | 59 | -1.009 | -0.937 | 59 | -0.938 | -0.958 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | short | 151 | -0.480 | -0.322 | 151 | -0.879 | -0.492 | 98 | -0.605 | -0.435 | 98 | -1.016 | -0.393 | 53 | -0.151 | -0.016 | 53 | -0.775 | -0.787 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | both | 3 | +0.359 | +0.521 | 3 | +2.282 | +2.443 | 2 | +2.464 | +2.619 | 2 | +2.828 | +2.983 | 1 | +0.379 | +0.552 | 1 | +2.302 | +2.474 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | long | 1 | -0.408 | -0.267 | 1 | +5.845 | +6.229 | 1 | -0.408 | -0.282 | 1 | +5.845 | +6.262 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | short | 2 | +2.851 | +3.033 | 2 | +1.050 | +0.988 | 1 | +5.343 | +5.526 | 1 | -0.182 | -0.290 | 1 | +0.379 | +0.550 | 1 | +2.302 | +2.387 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | both | 473 | -0.279 | -0.137 | 473 | +0.268 | +0.410 | 308 | -0.238 | -0.111 | 308 | +0.335 | +0.462 | 165 | -0.395 | -0.234 | 165 | +0.110 | +0.270 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | long | 257 | -0.513 | -0.429 | 257 | +0.376 | +0.139 | 171 | -0.298 | -0.210 | 171 | +0.733 | +0.703 | 86 | -0.756 | -0.690 | 86 | -0.022 | -0.638 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | short | 216 | +0.023 | +0.223 | 216 | +0.233 | +0.754 | 137 | +0.117 | +0.283 | 137 | +0.236 | +0.521 | 79 | -0.064 | +0.191 | 79 | +0.293 | +1.231 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | both | 89 | +0.213 | +0.345 | 89 | -0.715 | -0.584 | 62 | +0.711 | +0.831 | 62 | +0.336 | +0.456 | 27 | -0.773 | -0.611 | 27 | -3.813 | -3.651 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | long | 41 | +0.006 | +0.139 | 41 | +0.165 | +0.361 | 26 | +0.280 | +0.381 | 26 | +0.942 | +1.092 | 15 | -2.418 | -2.202 | 15 | -4.571 | -4.293 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | short | 48 | +0.445 | +0.576 | 48 | -0.827 | -0.761 | 36 | +0.962 | +1.099 | 36 | -0.240 | -0.150 | 12 | +0.079 | +0.187 | 12 | -3.736 | -3.690 |
| 1h | calibrated | BRK_tap200_first | record | NONE | both | 1 | -0.948 | -0.781 | 1 | -7.992 | -7.825 | 1 | -0.948 | -0.781 | 1 | -7.992 | -7.825 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | NONE | long | 1 | -0.948 | -0.397 | 1 | -7.992 | -6.718 | 1 | -0.948 | -0.397 | 1 | -7.992 | -6.718 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 1141 | -0.105 | +0.029 | 1141 | -0.090 | +0.044 | 724 | +0.011 | +0.133 | 724 | -0.045 | +0.077 | 417 | -0.467 | -0.306 | 417 | -0.338 | -0.177 |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 592 | -0.112 | -0.017 | 592 | +0.184 | +0.113 | 376 | +0.017 | +0.090 | 376 | +0.861 | +0.733 | 216 | -0.674 | -0.530 | 216 | -0.801 | -0.764 |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 549 | -0.102 | +0.071 | 549 | -0.460 | -0.120 | 348 | -0.022 | +0.148 | 348 | -0.679 | -0.307 | 201 | -0.187 | -0.009 | 201 | +0.105 | +0.390 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | both | 396 | +0.083 | +0.239 | 396 | +0.126 | +0.298 | 238 | +0.206 | +0.334 | 238 | +0.253 | +0.336 | 158 | -0.229 | -0.017 | 158 | +0.089 | +0.423 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | long | 208 | +0.140 | +0.249 | 208 | +0.550 | +0.429 | 127 | +0.191 | +0.252 | 127 | +1.007 | +0.616 | 81 | -0.062 | +0.147 | 81 | -0.103 | +0.257 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | short | 188 | -0.108 | +0.096 | 188 | -0.222 | +0.253 | 111 | +0.382 | +0.586 | 111 | -0.740 | -0.166 | 77 | -0.573 | -0.368 | 77 | +0.821 | +1.119 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | both | 267 | -0.420 | -0.319 | 267 | -0.894 | -0.810 | 165 | -0.118 | -0.015 | 165 | -1.104 | -0.957 | 102 | -0.986 | -0.880 | 102 | -0.827 | -0.843 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | long | 133 | -0.146 | -0.106 | 133 | -0.643 | -0.874 | 79 | +0.383 | +0.409 | 79 | -0.611 | -0.954 | 54 | -1.157 | -1.085 | 54 | -0.926 | -0.947 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | short | 134 | -0.615 | -0.458 | 134 | -1.026 | -0.639 | 86 | -0.692 | -0.521 | 86 | -1.245 | -0.623 | 48 | -0.359 | -0.224 | 48 | -0.583 | -0.595 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | both | 2 | +2.464 | +2.626 | 2 | +2.828 | +2.990 | 2 | +2.464 | +2.619 | 2 | +2.828 | +2.983 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | long | 1 | -0.408 | -0.267 | 1 | +5.845 | +6.229 | 1 | -0.408 | -0.282 | 1 | +5.845 | +6.262 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | +5.343 | +5.524 | 1 | -0.182 | -0.244 | 1 | +5.343 | +5.526 | 1 | -0.182 | -0.290 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | both | 390 | -0.279 | -0.137 | 390 | +0.196 | +0.338 | 260 | -0.209 | -0.082 | 260 | +0.486 | +0.613 | 130 | -0.443 | -0.283 | 130 | +0.057 | +0.217 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | long | 210 | -0.578 | -0.494 | 210 | +0.669 | +0.432 | 144 | -0.302 | -0.214 | 144 | +0.820 | +0.789 | 66 | -0.869 | -0.803 | 66 | -0.805 | -1.422 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | short | 180 | +0.142 | +0.342 | 180 | +0.046 | +0.567 | 116 | +0.150 | +0.316 | 116 | -0.453 | -0.169 | 64 | +0.055 | +0.310 | 64 | +0.457 | +1.395 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | both | 85 | +0.181 | +0.312 | 85 | -0.784 | -0.653 | 58 | +0.572 | +0.692 | 58 | +0.046 | +0.166 | 27 | -0.773 | -0.611 | 27 | -3.813 | -3.651 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | long | 39 | -0.209 | -0.076 | 39 | +0.165 | +0.361 | 24 | +0.280 | +0.381 | 24 | +0.942 | +1.092 | 15 | -2.418 | -2.202 | 15 | -4.571 | -4.293 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | short | 46 | +0.416 | +0.546 | 46 | -1.232 | -1.166 | 34 | +0.847 | +0.985 | 34 | -0.293 | -0.203 | 12 | +0.079 | +0.187 | 12 | -3.736 | -3.690 |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | both | 1 | -0.948 | -0.781 | 1 | -7.992 | -7.825 | 1 | -0.948 | -0.781 | 1 | -7.992 | -7.825 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | long | 1 | -0.948 | -0.397 | 1 | -7.992 | -6.718 | 1 | -0.948 | -0.397 | 1 | -7.992 | -6.718 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_first | record | ALL | both | 1389 | -0.314 | -0.179 | 1388 | -0.410 | -0.275 | 903 | -0.355 | -0.233 | 903 | -0.359 | -0.237 | 486 | -0.276 | -0.116 | 485 | -0.526 | -0.365 |
| 1h | calibrated | BRK_mem_first | record | ALL | long | 759 | -0.328 | -0.232 | 758 | -0.102 | -0.173 | 504 | -0.280 | -0.207 | 504 | +0.217 | +0.090 | 255 | -0.386 | -0.243 | 254 | -0.683 | -0.646 |
| 1h | calibrated | BRK_mem_first | record | ALL | short | 630 | -0.298 | -0.124 | 630 | -0.734 | -0.394 | 399 | -0.422 | -0.251 | 399 | -0.856 | -0.484 | 231 | -0.144 | +0.035 | 231 | -0.348 | -0.063 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | both | 452 | -0.441 | -0.286 | 451 | -0.402 | -0.230 | 303 | -0.439 | -0.311 | 303 | -0.482 | -0.399 | 149 | -0.446 | -0.234 | 148 | -0.166 | +0.168 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | long | 255 | -0.332 | -0.223 | 254 | +0.154 | +0.033 | 178 | -0.316 | -0.254 | 178 | +0.141 | -0.250 | 77 | -0.376 | -0.167 | 76 | +0.331 | +0.690 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | short | 197 | -0.697 | -0.493 | 197 | -0.901 | -0.426 | 125 | -0.782 | -0.578 | 125 | -1.178 | -0.604 | 72 | -0.588 | -0.383 | 72 | -0.298 | -0.001 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | both | 271 | -0.239 | -0.138 | 271 | -0.625 | -0.541 | 174 | -0.151 | -0.048 | 174 | -0.639 | -0.492 | 97 | -0.318 | -0.212 | 97 | -0.361 | -0.376 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | long | 140 | -0.257 | -0.218 | 140 | -0.178 | -0.410 | 94 | +0.060 | +0.086 | 94 | +0.013 | -0.330 | 46 | -1.215 | -1.143 | 46 | -0.597 | -0.617 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | short | 131 | -0.110 | +0.047 | 131 | -0.734 | -0.347 | 80 | -0.314 | -0.143 | 80 | -1.186 | -0.563 | 51 | +0.223 | +0.359 | 51 | -0.279 | -0.291 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | both | 31 | -1.202 | -1.041 | 31 | +0.276 | +0.437 | 16 | -1.386 | -1.231 | 16 | -2.569 | -2.414 | 15 | -0.291 | -0.118 | 15 | +1.730 | +1.902 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | long | 16 | -1.426 | -1.285 | 16 | +0.246 | +0.630 | 10 | -1.497 | -1.371 | 10 | -1.175 | -0.758 | 6 | -0.205 | -0.031 | 6 | +0.975 | +1.235 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | short | 15 | -0.265 | -0.083 | 15 | +0.484 | +0.422 | 6 | -0.410 | -0.227 | 6 | -2.912 | -3.019 | 9 | -0.295 | -0.124 | 9 | +2.637 | +2.722 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | both | 362 | -0.380 | -0.238 | 362 | -0.444 | -0.302 | 238 | -0.347 | -0.220 | 238 | -0.335 | -0.207 | 124 | -0.449 | -0.288 | 124 | -1.004 | -0.844 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | long | 213 | -0.318 | -0.234 | 213 | -0.434 | -0.671 | 140 | -0.213 | -0.125 | 140 | -0.256 | -0.286 | 73 | -0.439 | -0.373 | 73 | -0.886 | -1.503 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | short | 149 | -0.537 | -0.337 | 149 | -0.552 | -0.031 | 98 | -0.550 | -0.384 | 98 | -0.367 | -0.082 | 51 | -0.536 | -0.280 | 51 | -1.211 | -0.273 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | both | 270 | -0.108 | +0.023 | 270 | -0.235 | -0.104 | 169 | -0.358 | -0.238 | 169 | +0.534 | +0.654 | 101 | +0.162 | +0.323 | 101 | -0.954 | -0.792 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | long | 133 | -0.277 | -0.144 | 133 | -0.091 | +0.106 | 80 | -0.640 | -0.538 | 80 | +2.173 | +2.323 | 53 | +0.138 | +0.354 | 53 | -1.739 | -1.461 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | short | 137 | +0.002 | +0.132 | 137 | -0.371 | -0.305 | 89 | -0.113 | +0.025 | 89 | -0.265 | -0.176 | 48 | +0.345 | +0.452 | 48 | -0.815 | -0.769 |
| 1h | calibrated | BRK_mem_first | record | NONE | both | 3 | -1.525 | -1.358 | 3 | -3.884 | -3.717 | 3 | -1.525 | -1.358 | 3 | -3.884 | -3.717 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_first | record | NONE | long | 2 | -1.428 | -0.877 | 2 | -10.168 | -8.895 | 2 | -1.428 | -0.877 | 2 | -10.168 | -8.895 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_first | record | NONE | short | 1 | -1.501 | -1.718 | 1 | -3.860 | -4.800 | 1 | -1.501 | -1.718 | 1 | -3.860 | -4.800 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 1309 | -0.289 | -0.154 | 1308 | -0.380 | -0.245 | 852 | -0.304 | -0.183 | 852 | -0.298 | -0.176 | 457 | -0.283 | -0.123 | 456 | -0.528 | -0.367 |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 710 | -0.248 | -0.153 | 709 | -0.185 | -0.255 | 475 | -0.218 | -0.145 | 475 | +0.330 | +0.202 | 235 | -0.380 | -0.236 | 234 | -1.011 | -0.974 |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 599 | -0.320 | -0.146 | 599 | -0.585 | -0.245 | 377 | -0.418 | -0.248 | 377 | -0.845 | -0.473 | 222 | -0.165 | +0.013 | 222 | -0.105 | +0.179 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | both | 479 | -0.315 | -0.160 | 478 | -0.293 | -0.121 | 319 | -0.360 | -0.232 | 319 | -0.392 | -0.309 | 160 | -0.249 | -0.037 | 159 | -0.163 | +0.172 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | long | 266 | -0.166 | -0.057 | 265 | +0.237 | +0.116 | 185 | -0.161 | -0.100 | 185 | +0.346 | -0.045 | 81 | -0.225 | -0.015 | 80 | -0.203 | +0.156 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | short | 213 | -0.486 | -0.282 | 213 | -0.841 | -0.366 | 134 | -0.553 | -0.348 | 134 | -1.123 | -0.550 | 79 | -0.345 | -0.139 | 79 | -0.162 | +0.135 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | both | 250 | -0.192 | -0.090 | 250 | -0.545 | -0.461 | 153 | -0.001 | +0.102 | 153 | -0.615 | -0.468 | 97 | -0.318 | -0.211 | 97 | -0.468 | -0.484 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | long | 128 | -0.186 | -0.147 | 128 | -0.406 | -0.638 | 81 | +0.420 | +0.447 | 81 | -0.177 | -0.520 | 47 | -0.546 | -0.474 | 47 | -0.509 | -0.529 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | short | 122 | -0.163 | -0.005 | 122 | -0.681 | -0.294 | 72 | -0.311 | -0.141 | 72 | -0.781 | -0.158 | 50 | +0.093 | +0.229 | 50 | -0.319 | -0.331 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | both | 30 | -1.025 | -0.864 | 30 | +0.246 | +0.407 | 16 | -1.386 | -1.231 | 16 | -2.569 | -2.414 | 14 | -0.268 | -0.096 | 14 | +1.824 | +1.996 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | long | 16 | -1.426 | -1.285 | 16 | +0.246 | +0.630 | 10 | -1.497 | -1.371 | 10 | -1.175 | -0.758 | 6 | -0.205 | -0.031 | 6 | +0.975 | +1.235 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | short | 14 | -0.242 | -0.061 | 14 | -0.195 | -0.256 | 6 | -0.410 | -0.227 | 6 | -2.912 | -3.019 | 8 | -0.272 | -0.101 | 8 | +2.781 | +2.866 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | both | 325 | -0.347 | -0.205 | 325 | -0.438 | -0.297 | 215 | -0.269 | -0.142 | 215 | -0.348 | -0.220 | 110 | -0.469 | -0.308 | 110 | -0.622 | -0.461 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | long | 187 | -0.280 | -0.197 | 187 | -0.561 | -0.798 | 127 | -0.159 | -0.071 | 127 | +0.484 | +0.453 | 60 | -0.438 | -0.372 | 60 | -2.090 | -2.707 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | short | 138 | -0.469 | -0.269 | 138 | -0.360 | +0.161 | 88 | -0.407 | -0.241 | 88 | -0.649 | -0.364 | 50 | -0.655 | -0.399 | 50 | +0.122 | +1.060 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | both | 222 | -0.251 | -0.119 | 222 | -0.161 | -0.030 | 146 | -0.454 | -0.334 | 146 | +0.484 | +0.604 | 76 | +0.103 | +0.265 | 76 | -1.873 | -1.711 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | long | 111 | -0.319 | -0.187 | 111 | -0.318 | -0.121 | 70 | -0.687 | -0.586 | 70 | +2.148 | +2.298 | 41 | +0.121 | +0.337 | 41 | -2.137 | -1.859 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | short | 111 | -0.136 | -0.006 | 111 | -0.110 | -0.044 | 76 | -0.390 | -0.252 | 76 | -0.015 | +0.074 | 35 | -0.012 | +0.095 | 35 | -0.912 | -0.867 |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | both | 3 | -1.525 | -1.358 | 3 | -3.884 | -3.717 | 3 | -1.525 | -1.358 | 3 | -3.884 | -3.717 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | long | 2 | -1.428 | -0.877 | 2 | -10.168 | -8.895 | 2 | -1.428 | -0.877 | 2 | -10.168 | -8.895 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | short | 1 | -1.501 | -1.718 | 1 | -3.860 | -4.800 | 1 | -1.501 | -1.718 | 1 | -3.860 | -4.800 | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | ALL | both | 2571 | -0.103 | +0.031 | 2567 | -0.007 | +0.128 | 1626 | +0.013 | +0.135 | 1626 | +0.162 | +0.284 | 945 | -0.309 | -0.148 | 941 | -0.387 | -0.226 |
| 1h | calibrated | SFP_harden | record | ALL | long | 1257 | -0.040 | +0.056 | 1257 | -0.164 | -0.235 | 763 | +0.159 | +0.232 | 763 | +0.154 | +0.026 | 494 | -0.408 | -0.265 | 494 | -0.820 | -0.783 |
| 1h | calibrated | SFP_harden | record | ALL | short | 1314 | -0.130 | +0.043 | 1310 | +0.152 | +0.492 | 863 | -0.094 | +0.076 | 863 | +0.162 | +0.534 | 451 | -0.228 | -0.050 | 447 | +0.204 | +0.488 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | both | 707 | -0.240 | -0.085 | 707 | -0.054 | +0.119 | 445 | -0.147 | -0.018 | 445 | -0.058 | +0.026 | 262 | -0.392 | -0.180 | 262 | -0.069 | +0.265 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | long | 391 | -0.393 | -0.284 | 391 | -0.363 | -0.483 | 244 | -0.365 | -0.303 | 244 | -0.133 | -0.524 | 147 | -0.491 | -0.282 | 147 | -0.746 | -0.386 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | short | 316 | -0.079 | +0.125 | 316 | +0.576 | +1.051 | 201 | +0.128 | +0.332 | 201 | +0.483 | +1.056 | 115 | -0.247 | -0.041 | 115 | +0.615 | +0.912 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | both | 666 | +0.097 | +0.198 | 662 | +0.643 | +0.727 | 427 | +0.082 | +0.185 | 427 | +0.512 | +0.660 | 239 | +0.116 | +0.223 | 235 | +0.982 | +0.966 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | long | 313 | +0.158 | +0.197 | 313 | +0.558 | +0.326 | 179 | +0.298 | +0.325 | 179 | +0.926 | +0.583 | 134 | -0.034 | +0.038 | 134 | -0.543 | -0.563 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | short | 353 | +0.064 | +0.221 | 349 | +0.649 | +1.036 | 248 | -0.041 | +0.129 | 248 | +0.220 | +0.842 | 105 | +0.502 | +0.637 | 101 | +1.635 | +1.623 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | both | 151 | -0.014 | +0.147 | 151 | +0.078 | +0.240 | 97 | +0.238 | +0.393 | 97 | +1.040 | +1.194 | 54 | -0.825 | -0.653 | 54 | -1.091 | -0.919 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | long | 62 | -0.269 | -0.128 | 62 | +0.025 | +0.409 | 40 | -0.078 | +0.049 | 40 | +1.024 | +1.441 | 22 | -0.941 | -0.768 | 22 | -2.652 | -2.392 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | short | 89 | +0.044 | +0.225 | 89 | +0.078 | +0.017 | 57 | +0.370 | +0.553 | 57 | +0.974 | +0.866 | 32 | -0.649 | -0.477 | 32 | -0.493 | -0.409 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | both | 461 | -0.157 | -0.015 | 461 | -0.276 | -0.134 | 294 | -0.057 | +0.071 | 294 | -0.152 | -0.025 | 167 | -0.225 | -0.064 | 167 | -0.386 | -0.225 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | long | 200 | +0.136 | +0.219 | 200 | -0.243 | -0.480 | 124 | +0.393 | +0.481 | 124 | +0.288 | +0.257 | 76 | -0.303 | -0.237 | 76 | -0.827 | -1.444 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | short | 261 | -0.648 | -0.448 | 261 | -0.283 | +0.238 | 170 | -0.661 | -0.494 | 170 | -0.265 | +0.020 | 91 | -0.222 | +0.033 | 91 | -0.286 | +0.652 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | both | 579 | -0.123 | +0.008 | 579 | -0.551 | -0.420 | 356 | +0.102 | +0.222 | 356 | -0.254 | -0.135 | 223 | -0.654 | -0.492 | 223 | -1.270 | -1.109 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | long | 287 | +0.000 | +0.133 | 287 | -0.569 | -0.373 | 172 | +0.440 | +0.541 | 172 | -0.478 | -0.329 | 115 | -0.533 | -0.317 | 115 | -0.824 | -0.546 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | short | 292 | -0.297 | -0.167 | 292 | -0.556 | -0.489 | 184 | -0.071 | +0.067 | 184 | +0.105 | +0.195 | 108 | -0.911 | -0.803 | 108 | -1.417 | -1.372 |
| 1h | calibrated | SFP_harden | record | NONE | both | 7 | +0.407 | +0.574 | 7 | +4.035 | +4.201 | 7 | +0.407 | +0.574 | 7 | +4.035 | +4.201 | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | NONE | long | 4 | +0.769 | +1.319 | 4 | +3.324 | +4.598 | 4 | +0.769 | +1.319 | 4 | +3.324 | +4.598 | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | NONE | short | 3 | -1.830 | -2.047 | 3 | +4.624 | +3.684 | 3 | -1.830 | -2.047 | 3 | +4.624 | +3.684 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | ALL | both | 450 | +0.129 | +0.194 | 446 | +0.281 | +0.345 | 287 | +0.103 | +0.161 | 287 | +0.441 | +0.499 | 163 | +0.137 | +0.215 | 159 | -0.069 | +0.009 |
| 4h | calibrated | BRK_tap89_first | record | ALL | long | 230 | +0.025 | +0.008 | 227 | -0.053 | -0.192 | 153 | +0.101 | +0.058 | 153 | -0.154 | -0.338 | 77 | -0.407 | -0.371 | 74 | +0.020 | -0.008 |
| 4h | calibrated | BRK_tap89_first | record | ALL | short | 220 | +0.277 | +0.424 | 219 | +0.431 | +0.699 | 134 | +0.151 | +0.310 | 134 | +1.037 | +1.337 | 86 | +0.393 | +0.514 | 85 | -0.302 | -0.118 |
| 4h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | both | 190 | +0.376 | +0.409 | 187 | -0.297 | -0.158 | 128 | +0.502 | +0.478 | 128 | -0.072 | -0.057 | 62 | +0.332 | +0.519 | 59 | -0.317 | +0.112 |
| 4h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | long | 106 | +0.627 | +0.600 | 103 | -0.295 | -0.228 | 77 | +0.694 | +0.593 | 77 | -0.388 | -0.511 | 29 | +0.219 | +0.420 | 26 | -0.240 | +0.398 |
| 4h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | short | 84 | +0.342 | +0.437 | 84 | +0.278 | +0.482 | 51 | +0.336 | +0.402 | 51 | +0.554 | +0.743 | 33 | +0.354 | +0.519 | 33 | -0.426 | -0.177 |
| 4h | calibrated | BRK_tap89_first | record | EXP_COUNTER | both | 85 | +0.061 | +0.148 | 85 | +0.711 | +0.692 | 58 | +0.053 | +0.192 | 58 | +0.662 | +0.761 | 27 | +0.722 | +0.694 | 27 | +1.555 | +1.283 |
| 4h | calibrated | BRK_tap89_first | record | EXP_COUNTER | long | 35 | +0.031 | +0.061 | 35 | +0.531 | +0.452 | 24 | -0.069 | -0.008 | 24 | -0.095 | -0.157 | 11 | +0.915 | +0.868 | 11 | +2.678 | +2.547 |
| 4h | calibrated | BRK_tap89_first | record | EXP_COUNTER | short | 50 | +0.182 | +0.327 | 50 | +1.038 | +1.089 | 34 | +0.183 | +0.394 | 34 | +1.039 | +1.271 | 16 | +0.143 | +0.117 | 16 | +0.933 | +0.468 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | both | 2 | -2.672 | -2.608 | 2 | -4.343 | -4.279 | 2 | -2.672 | -2.622 | 2 | -4.343 | -4.293 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | long | 1 | -3.732 | -3.765 | 1 | -3.774 | -3.817 | 1 | -3.732 | -3.744 | 1 | -3.774 | -4.362 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | short | 1 | -1.593 | -1.432 | 1 | -4.893 | -4.721 | 1 | -1.593 | -1.480 | 1 | -4.893 | -4.204 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | both | 132 | -0.039 | +0.034 | 131 | +0.313 | +0.386 | 72 | +0.100 | +0.162 | 72 | +1.194 | +1.256 | 60 | -0.733 | -0.652 | 59 | -0.820 | -0.739 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | long | 69 | -0.182 | -0.260 | 69 | +0.312 | -0.164 | 39 | +0.208 | +0.014 | 39 | +1.971 | +1.715 | 30 | -1.142 | -1.081 | 30 | -0.339 | -1.120 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | short | 63 | +0.278 | +0.501 | 62 | +0.320 | +0.942 | 33 | -0.283 | +0.035 | 33 | +0.927 | +1.307 | 30 | +0.741 | +0.843 | 29 | -1.674 | -0.731 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | both | 41 | +0.129 | +0.199 | 41 | +0.416 | +0.485 | 27 | +0.059 | +0.121 | 27 | -0.822 | -0.759 | 14 | +0.361 | +0.439 | 14 | +2.168 | +2.246 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | long | 19 | +0.002 | -0.015 | 19 | -0.986 | -1.700 | 12 | -0.811 | -0.826 | 12 | -2.518 | -3.142 | 7 | +1.295 | +1.249 | 7 | +2.681 | +1.701 |
| 4h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | short | 22 | +0.217 | +0.374 | 22 | +1.193 | +2.046 | 15 | +0.328 | +0.468 | 15 | +1.970 | +2.720 | 7 | -1.405 | -1.202 | 7 | -0.657 | +0.478 |
| 4h | calibrated | BRK_tap89_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 392 | +0.245 | +0.310 | 388 | +0.398 | +0.462 | 250 | +0.206 | +0.264 | 250 | +0.565 | +0.623 | 142 | +0.334 | +0.412 | 138 | +0.152 | +0.230 |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 208 | +0.065 | +0.047 | 205 | +0.269 | +0.130 | 134 | +0.109 | +0.067 | 134 | +0.233 | +0.050 | 74 | -0.281 | -0.245 | 71 | +0.275 | +0.246 |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 184 | +0.358 | +0.505 | 183 | +0.449 | +0.717 | 116 | +0.283 | +0.442 | 116 | +1.065 | +1.365 | 68 | +0.705 | +0.825 | 67 | -0.308 | -0.124 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | both | 172 | +0.496 | +0.529 | 169 | -0.145 | -0.006 | 119 | +0.361 | +0.337 | 119 | -0.297 | -0.281 | 53 | +0.690 | +0.877 | 50 | -0.115 | +0.314 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | long | 100 | +0.738 | +0.712 | 97 | -0.295 | -0.228 | 73 | +0.775 | +0.674 | 73 | -0.566 | -0.688 | 27 | +0.690 | +0.891 | 24 | -0.115 | +0.524 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | short | 72 | +0.407 | +0.501 | 72 | +0.478 | +0.682 | 46 | +0.258 | +0.324 | 46 | +0.811 | +1.000 | 26 | +0.661 | +0.825 | 26 | -0.275 | -0.027 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | both | 65 | +0.098 | +0.185 | 65 | +1.038 | +1.019 | 44 | +0.093 | +0.231 | 44 | +0.875 | +0.974 | 21 | +0.846 | +0.818 | 21 | +1.555 | +1.283 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | long | 28 | +0.037 | +0.068 | 28 | +2.087 | +2.007 | 17 | +0.029 | +0.090 | 17 | +1.702 | +1.640 | 11 | +0.915 | +0.868 | 11 | +2.678 | +2.547 |
| 4h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | short | 37 | +0.378 | +0.523 | 37 | +0.610 | +0.661 | 27 | +0.379 | +0.590 | 27 | +0.611 | +0.844 | 10 | +0.280 | +0.254 | 10 | +0.860 | +0.396 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | both | 1 | -3.732 | -3.668 | 1 | -3.774 | -3.710 | 1 | -3.732 | -3.681 | 1 | -3.774 | -3.723 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | long | 1 | -3.732 | -3.765 | 1 | -3.774 | -3.817 | 1 | -3.732 | -3.744 | 1 | -3.774 | -4.362 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | both | 121 | +0.073 | +0.146 | 120 | +0.423 | +0.496 | 65 | +0.108 | +0.170 | 65 | +1.495 | +1.557 | 56 | -0.451 | -0.370 | 55 | -0.336 | -0.255 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | long | 63 | -0.190 | -0.267 | 63 | +1.012 | +0.536 | 34 | +0.159 | -0.034 | 34 | +2.010 | +1.753 | 29 | -1.107 | -1.046 | 29 | -0.338 | -1.120 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | short | 58 | +0.470 | +0.693 | 57 | +0.397 | +1.019 | 31 | -0.214 | +0.104 | 31 | +0.927 | +1.307 | 27 | +0.906 | +1.007 | 26 | -1.246 | -0.302 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | both | 33 | +0.303 | +0.372 | 33 | +1.079 | +1.148 | 21 | +0.316 | +0.379 | 21 | -0.822 | -0.759 | 12 | +0.361 | +0.439 | 12 | +2.353 | +2.431 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | long | 16 | +0.701 | +0.684 | 16 | -0.912 | -1.627 | 9 | +0.019 | +0.004 | 9 | -4.764 | -5.388 | 7 | +1.295 | +1.249 | 7 | +2.681 | +1.701 |
| 4h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | short | 17 | +0.284 | +0.440 | 17 | +1.966 | +2.820 | 12 | +0.620 | +0.760 | 12 | +2.296 | +3.046 | 5 | -1.405 | -1.202 | 5 | -3.361 | -2.225 |
| 4h | calibrated | BRK_tap89_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_first | record | ALL | both | 403 | +0.179 | +0.244 | 398 | +0.130 | +0.195 | 257 | +0.117 | +0.175 | 257 | -0.286 | -0.228 | 146 | +0.322 | +0.400 | 141 | +0.277 | +0.355 |
| 4h | calibrated | BRK_tap127_first | record | ALL | long | 212 | +0.016 | -0.001 | 209 | -0.298 | -0.437 | 143 | +0.056 | +0.013 | 143 | -0.314 | -0.498 | 69 | -0.213 | -0.177 | 66 | -0.100 | -0.129 |
| 4h | calibrated | BRK_tap127_first | record | ALL | short | 191 | +0.278 | +0.424 | 189 | +0.447 | +0.715 | 114 | +0.155 | +0.314 | 114 | +0.212 | +0.511 | 77 | +0.667 | +0.787 | 75 | +0.971 | +1.156 |
| 4h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | both | 163 | +0.351 | +0.384 | 161 | -0.282 | -0.142 | 114 | +0.088 | +0.063 | 114 | -0.301 | -0.285 | 49 | +0.700 | +0.887 | 47 | -0.051 | +0.378 |
| 4h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | long | 95 | +0.526 | +0.500 | 93 | -0.412 | -0.346 | 71 | +0.512 | +0.410 | 71 | -0.273 | -0.396 | 24 | +0.803 | +1.004 | 22 | -0.725 | -0.087 |
| 4h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | short | 68 | +0.079 | +0.173 | 68 | +0.448 | +0.652 | 43 | -0.193 | -0.127 | 43 | -0.331 | -0.142 | 25 | +0.651 | +0.816 | 25 | +0.977 | +1.225 |
| 4h | calibrated | BRK_tap127_first | record | EXP_COUNTER | both | 74 | +0.078 | +0.165 | 73 | +0.453 | +0.434 | 50 | +0.082 | +0.220 | 50 | -0.390 | -0.291 | 24 | +0.111 | +0.083 | 23 | +1.984 | +1.712 |
| 4h | calibrated | BRK_tap127_first | record | EXP_COUNTER | long | 31 | +0.024 | +0.054 | 31 | +0.687 | +0.607 | 22 | -0.434 | -0.373 | 22 | -0.308 | -0.370 | 9 | +0.275 | +0.227 | 9 | +2.047 | +1.917 |
| 4h | calibrated | BRK_tap127_first | record | EXP_COUNTER | short | 43 | +0.169 | +0.314 | 42 | +0.325 | +0.376 | 28 | +0.211 | +0.422 | 28 | -0.817 | -0.584 | 15 | -0.567 | -0.593 | 14 | +2.579 | +2.114 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | both | 2 | -1.670 | -1.606 | 2 | -1.003 | -0.939 | 1 | -3.383 | -3.333 | 1 | -3.384 | -3.334 | 1 | +0.043 | +0.115 | 1 | +1.379 | +1.451 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | long | 2 | -1.670 | -1.703 | 2 | -1.003 | -1.046 | 1 | -3.383 | -3.396 | 1 | -3.384 | -3.973 | 1 | +0.043 | -0.033 | 1 | +1.379 | +1.996 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | both | 127 | -0.036 | +0.037 | 126 | -0.222 | -0.150 | 69 | +0.046 | +0.108 | 69 | +0.327 | +0.389 | 58 | -0.739 | -0.658 | 57 | -0.381 | -0.300 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | long | 64 | -0.143 | -0.220 | 64 | -0.222 | -0.699 | 37 | +0.133 | -0.060 | 37 | +0.332 | +0.076 | 27 | -1.182 | -1.121 | 27 | -0.384 | -1.166 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | short | 63 | +0.226 | +0.449 | 62 | -0.265 | +0.357 | 32 | -0.246 | +0.072 | 32 | +0.007 | +0.387 | 31 | +0.666 | +0.767 | 30 | -0.878 | +0.066 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | both | 37 | +0.964 | +1.033 | 36 | +0.731 | +0.801 | 23 | +0.422 | +0.485 | 23 | +0.378 | +0.441 | 14 | +1.230 | +1.309 | 13 | +2.087 | +2.165 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | long | 20 | +0.100 | +0.083 | 19 | -0.982 | -1.697 | 12 | -1.485 | -1.499 | 12 | -2.250 | -2.874 | 8 | +1.134 | +1.088 | 7 | +0.765 | -0.214 |
| 4h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | short | 17 | +1.156 | +1.313 | 17 | +2.528 | +3.381 | 11 | +0.963 | +1.103 | 11 | +2.608 | +3.358 | 6 | +1.603 | +1.806 | 6 | +2.312 | +3.447 |
| 4h | calibrated | BRK_tap127_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 358 | +0.208 | +0.272 | 353 | +0.289 | +0.353 | 225 | +0.239 | +0.297 | 225 | +0.224 | +0.282 | 133 | +0.037 | +0.115 | 128 | +0.329 | +0.407 |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 194 | +0.047 | +0.030 | 191 | +0.126 | -0.013 | 128 | +0.298 | +0.255 | 128 | -0.024 | -0.207 | 66 | -0.185 | -0.149 | 63 | +0.113 | +0.084 |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 164 | +0.287 | +0.433 | 162 | +0.451 | +0.718 | 97 | +0.174 | +0.333 | 97 | +0.370 | +0.670 | 67 | +0.644 | +0.765 | 65 | +0.971 | +1.156 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | both | 146 | +0.349 | +0.382 | 144 | -0.304 | -0.164 | 104 | +0.264 | +0.240 | 104 | -0.401 | -0.385 | 42 | +0.666 | +0.853 | 40 | +0.036 | +0.465 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | long | 90 | +0.745 | +0.719 | 88 | -0.396 | -0.330 | 67 | +0.530 | +0.429 | 67 | -0.275 | -0.398 | 23 | +0.913 | +1.114 | 21 | -0.429 | +0.209 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | short | 56 | -0.191 | -0.097 | 56 | +0.720 | +0.924 | 37 | -0.193 | -0.127 | 37 | -0.484 | -0.295 | 19 | +0.272 | +0.437 | 19 | +1.027 | +1.275 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | both | 62 | +0.075 | +0.162 | 61 | +0.691 | +0.672 | 41 | +0.119 | +0.258 | 41 | -0.299 | -0.200 | 21 | +0.008 | -0.020 | 20 | +2.012 | +1.740 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | long | 25 | +0.040 | +0.071 | 25 | +2.011 | +1.932 | 16 | -0.282 | -0.221 | 16 | +2.138 | +2.076 | 9 | +0.275 | +0.227 | 9 | +2.047 | +1.917 |
| 4h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | short | 37 | +0.111 | +0.256 | 36 | +0.070 | +0.121 | 25 | +0.169 | +0.380 | 25 | -0.895 | -0.663 | 12 | -0.919 | -0.945 | 11 | +3.174 | +2.710 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | both | 2 | -1.670 | -1.606 | 2 | -1.003 | -0.939 | 1 | -3.383 | -3.333 | 1 | -3.384 | -3.334 | 1 | +0.043 | +0.115 | 1 | +1.379 | +1.451 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | long | 2 | -1.670 | -1.703 | 2 | -1.003 | -1.046 | 1 | -3.383 | -3.396 | 1 | -3.384 | -3.973 | 1 | +0.043 | -0.033 | 1 | +1.379 | +1.996 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | both | 113 | -0.033 | +0.039 | 112 | +0.160 | +0.233 | 58 | +0.214 | +0.276 | 58 | +0.683 | +0.746 | 55 | -0.758 | -0.677 | 54 | -0.257 | -0.176 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | long | 58 | -0.143 | -0.220 | 58 | +0.212 | -0.264 | 33 | +0.133 | -0.060 | 33 | +0.575 | +0.318 | 25 | -1.180 | -1.120 | 25 | -0.148 | -0.930 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | short | 55 | +0.423 | +0.645 | 54 | +0.053 | +0.675 | 25 | +0.294 | +0.611 | 25 | +0.791 | +1.172 | 30 | +0.551 | +0.653 | 29 | -1.667 | -0.723 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | both | 35 | +0.978 | +1.048 | 34 | +0.731 | +0.801 | 21 | +0.900 | +0.963 | 21 | +0.378 | +0.441 | 14 | +1.230 | +1.309 | 13 | +2.087 | +2.165 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | long | 19 | +0.409 | +0.391 | 18 | -0.302 | -1.016 | 11 | -1.147 | -1.162 | 11 | -2.284 | -2.908 | 8 | +1.134 | +1.088 | 7 | +0.765 | -0.214 |
| 4h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | short | 16 | +1.275 | +1.432 | 16 | +2.312 | +3.165 | 10 | +1.174 | +1.314 | 10 | +1.647 | +2.397 | 6 | +1.603 | +1.806 | 6 | +2.312 | +3.447 |
| 4h | calibrated | BRK_tap127_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap127_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | ALL | both | 333 | +0.010 | +0.074 | 331 | -0.277 | -0.213 | 214 | -0.233 | -0.175 | 214 | -0.504 | -0.446 | 119 | +0.230 | +0.308 | 117 | -0.108 | -0.030 |
| 4h | calibrated | BRK_tap200_first | record | ALL | long | 178 | +0.017 | -0.001 | 176 | -0.632 | -0.771 | 116 | +0.318 | +0.276 | 116 | -0.808 | -0.992 | 62 | -0.118 | -0.082 | 60 | -0.202 | -0.231 |
| 4h | calibrated | BRK_tap200_first | record | ALL | short | 155 | -0.050 | +0.097 | 155 | -0.039 | +0.229 | 98 | -0.698 | -0.539 | 98 | -0.189 | +0.111 | 57 | +0.781 | +0.902 | 57 | +0.767 | +0.951 |
| 4h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | both | 115 | -0.312 | -0.279 | 113 | -0.494 | -0.354 | 78 | -0.558 | -0.582 | 78 | -0.379 | -0.363 | 37 | -0.017 | +0.170 | 35 | -1.167 | -0.738 |
| 4h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | long | 68 | -0.252 | -0.278 | 66 | -1.910 | -1.844 | 48 | -0.262 | -0.364 | 48 | -1.933 | -2.056 | 20 | -0.291 | -0.090 | 18 | -1.960 | -1.322 |
| 4h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | short | 47 | -0.407 | -0.313 | 47 | +0.879 | +1.083 | 30 | -0.960 | -0.894 | 30 | +0.780 | +0.969 | 17 | +0.648 | +0.813 | 17 | +0.891 | +1.140 |
| 4h | calibrated | BRK_tap200_first | record | EXP_COUNTER | both | 64 | +0.384 | +0.472 | 64 | +1.135 | +1.116 | 46 | -0.413 | -0.274 | 46 | +1.116 | +1.215 | 18 | +0.953 | +0.925 | 18 | +2.758 | +2.487 |
| 4h | calibrated | BRK_tap200_first | record | EXP_COUNTER | long | 27 | +0.679 | +0.709 | 27 | +2.211 | +2.132 | 19 | -0.426 | -0.365 | 19 | +2.211 | +2.149 | 8 | +0.885 | +0.837 | 8 | +3.107 | +2.976 |
| 4h | calibrated | BRK_tap200_first | record | EXP_COUNTER | short | 37 | +0.023 | +0.168 | 37 | +1.137 | +1.188 | 27 | -0.587 | -0.376 | 27 | +1.102 | +1.334 | 10 | +1.108 | +1.082 | 10 | +2.758 | +2.293 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | both | 119 | +0.083 | +0.155 | 119 | -0.783 | -0.711 | 67 | +0.062 | +0.124 | 67 | -1.676 | -1.614 | 52 | +0.215 | +0.296 | 52 | -0.167 | -0.086 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | long | 64 | -0.020 | -0.097 | 64 | -0.576 | -1.053 | 37 | +0.485 | +0.291 | 37 | -0.799 | -1.056 | 27 | -1.196 | -1.136 | 27 | -0.195 | -0.977 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | short | 55 | +0.289 | +0.512 | 55 | -0.781 | -0.159 | 30 | -0.782 | -0.464 | 30 | -3.029 | -2.649 | 25 | +0.919 | +1.021 | 25 | -0.083 | +0.861 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | both | 35 | -0.161 | -0.091 | 35 | -0.904 | -0.835 | 23 | -0.048 | +0.014 | 23 | -0.929 | -0.867 | 12 | -0.330 | -0.251 | 12 | -0.311 | -0.233 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | long | 19 | +1.079 | +1.062 | 19 | +0.193 | -0.522 | 12 | +1.217 | +1.202 | 12 | +1.049 | +0.424 | 7 | +0.339 | +0.293 | 7 | -0.041 | -1.020 |
| 4h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | short | 16 | -0.694 | -0.538 | 16 | -1.395 | -0.541 | 11 | -0.247 | -0.106 | 11 | -1.949 | -1.199 | 5 | -1.118 | -0.914 | 5 | -0.581 | +0.555 |
| 4h | calibrated | BRK_tap200_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 295 | +0.030 | +0.094 | 293 | -0.136 | -0.072 | 193 | -0.048 | +0.010 | 193 | -0.273 | -0.215 | 102 | +0.179 | +0.257 | 100 | -0.090 | -0.012 |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 160 | +0.100 | +0.082 | 158 | -0.296 | -0.435 | 106 | +0.482 | +0.439 | 106 | -0.408 | -0.592 | 54 | -0.116 | -0.080 | 52 | -0.206 | -0.235 |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 135 | -0.062 | +0.084 | 135 | +0.430 | +0.698 | 87 | -0.717 | -0.558 | 87 | -0.140 | +0.160 | 48 | +0.774 | +0.894 | 48 | +0.914 | +1.098 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | both | 106 | -0.293 | -0.260 | 104 | -0.554 | -0.414 | 73 | -0.413 | -0.437 | 73 | -0.727 | -0.712 | 33 | -0.017 | +0.170 | 31 | -0.401 | +0.027 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | long | 67 | -0.243 | -0.270 | 65 | -1.884 | -1.818 | 47 | -0.209 | -0.310 | 47 | -1.804 | -1.927 | 20 | -0.291 | -0.090 | 18 | -1.960 | -1.322 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | short | 39 | -0.410 | -0.315 | 39 | +1.019 | +1.223 | 26 | -0.960 | -0.894 | 26 | +0.720 | +0.909 | 13 | +0.648 | +0.813 | 13 | +2.115 | +2.364 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | both | 60 | +0.648 | +0.736 | 60 | +1.106 | +1.086 | 42 | -0.415 | -0.276 | 42 | +0.890 | +0.988 | 18 | +0.953 | +0.925 | 18 | +2.758 | +2.487 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | long | 25 | +0.690 | +0.720 | 25 | +2.201 | +2.122 | 17 | +0.690 | +0.751 | 17 | +2.201 | +2.139 | 8 | +0.885 | +0.837 | 8 | +3.107 | +2.976 |
| 4h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | short | 35 | +0.018 | +0.163 | 35 | +1.095 | +1.146 | 25 | -0.587 | -0.376 | 25 | +0.704 | +0.936 | 10 | +1.108 | +1.082 | 10 | +2.758 | +2.293 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | both | 98 | +0.291 | +0.363 | 98 | -0.133 | -0.060 | 58 | +0.291 | +0.353 | 58 | +0.128 | +0.190 | 40 | +0.201 | +0.282 | 40 | -0.182 | -0.101 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | long | 52 | +0.028 | -0.050 | 52 | -0.132 | -0.609 | 32 | +0.480 | +0.287 | 32 | +0.133 | -0.123 | 20 | -0.954 | -0.893 | 20 | -0.191 | -0.973 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | short | 46 | +0.307 | +0.530 | 46 | -0.270 | +0.352 | 26 | -1.095 | -0.777 | 26 | +0.053 | +0.434 | 20 | +0.978 | +1.079 | 20 | -0.442 | +0.501 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | both | 31 | -0.161 | -0.091 | 31 | -0.856 | -0.787 | 20 | +0.095 | +0.158 | 20 | -0.906 | -0.844 | 11 | -0.490 | -0.412 | 11 | -0.576 | -0.498 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | long | 16 | +1.217 | +1.199 | 16 | +1.049 | +0.334 | 10 | +1.217 | +1.202 | 10 | +2.564 | +1.940 | 6 | +0.852 | +0.806 | 6 | -0.390 | -1.369 |
| 4h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | short | 15 | -0.482 | -0.325 | 15 | -0.931 | -0.078 | 10 | -0.147 | -0.007 | 10 | -3.551 | -2.801 | 5 | -1.118 | -0.914 | 5 | -0.581 | +0.555 |
| 4h | calibrated | BRK_tap200_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap200_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | ALL | both | 310 | +0.058 | +0.122 | 309 | +0.493 | +0.557 | 203 | +0.200 | +0.258 | 203 | +0.501 | +0.559 | 107 | -0.237 | -0.159 | 106 | +0.777 | +0.854 |
| 4h | calibrated | BRK_mem_first | record | ALL | long | 153 | +0.439 | +0.421 | 153 | +0.831 | +0.692 | 104 | +0.520 | +0.477 | 104 | +0.739 | +0.555 | 49 | -0.006 | +0.030 | 49 | +0.815 | +0.786 |
| 4h | calibrated | BRK_mem_first | record | ALL | short | 157 | -0.228 | -0.082 | 156 | +0.082 | +0.350 | 99 | -0.195 | -0.036 | 99 | +0.180 | +0.480 | 58 | -0.346 | -0.226 | 57 | -0.017 | +0.168 |
| 4h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | both | 106 | +0.356 | +0.389 | 106 | -0.320 | -0.180 | 79 | +0.438 | +0.414 | 79 | +0.335 | +0.351 | 27 | -0.183 | +0.004 | 27 | -1.927 | -1.498 |
| 4h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | long | 58 | +0.457 | +0.430 | 58 | -0.531 | -0.465 | 47 | +0.674 | +0.573 | 47 | +0.340 | +0.217 | 11 | -1.005 | -0.805 | 11 | -2.542 | -1.904 |
| 4h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | short | 48 | +0.290 | +0.384 | 48 | +0.115 | +0.319 | 32 | +0.245 | +0.312 | 32 | +0.107 | +0.296 | 16 | +0.876 | +1.041 | 16 | -0.256 | -0.007 |
| 4h | calibrated | BRK_mem_first | record | EXP_COUNTER | both | 60 | -0.008 | +0.079 | 60 | +1.538 | +1.518 | 41 | -0.070 | +0.069 | 41 | +0.873 | +0.972 | 19 | +1.317 | +1.289 | 19 | +2.489 | +2.218 |
| 4h | calibrated | BRK_mem_first | record | EXP_COUNTER | long | 21 | +1.429 | +1.459 | 21 | +3.720 | +3.640 | 15 | -0.061 | -0.000 | 15 | +3.160 | +3.098 | 6 | +2.200 | +2.153 | 6 | +4.168 | +4.037 |
| 4h | calibrated | BRK_mem_first | record | EXP_COUNTER | short | 39 | -0.189 | -0.045 | 39 | +0.134 | +0.185 | 26 | -0.587 | -0.376 | 26 | -0.239 | -0.006 | 13 | +0.035 | +0.009 | 13 | +1.773 | +1.308 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | both | 2 | -1.694 | -1.630 | 2 | +9.533 | +9.597 | 2 | -1.694 | -1.644 | 2 | +9.533 | +9.583 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | long | 2 | -1.694 | -1.728 | 2 | +9.533 | +9.489 | 2 | -1.694 | -1.707 | 2 | +9.533 | +8.944 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | both | 80 | -0.373 | -0.300 | 79 | +0.173 | +0.245 | 48 | -0.023 | +0.039 | 48 | +0.258 | +0.320 | 32 | -0.810 | -0.729 | 31 | -0.731 | -0.650 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | long | 42 | +0.239 | +0.162 | 42 | +0.240 | -0.236 | 23 | +0.265 | +0.071 | 23 | +0.167 | -0.090 | 19 | -0.370 | -0.309 | 19 | +2.604 | +1.822 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | short | 38 | -0.988 | -0.766 | 37 | -0.138 | +0.484 | 25 | -0.377 | -0.059 | 25 | +0.514 | +0.895 | 13 | -1.110 | -1.009 | 12 | -1.265 | -0.321 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | both | 62 | -0.071 | -0.001 | 62 | +1.403 | +1.472 | 33 | -0.156 | -0.093 | 33 | +1.320 | +1.383 | 29 | +0.014 | +0.092 | 29 | +1.485 | +1.564 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | long | 30 | +0.903 | +0.885 | 30 | +3.951 | +3.236 | 17 | +1.159 | +1.145 | 17 | +3.847 | +3.223 | 13 | +0.641 | +0.595 | 13 | +5.127 | +4.148 |
| 4h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | short | 32 | -0.624 | -0.467 | 32 | +0.269 | +1.122 | 16 | -0.567 | -0.427 | 16 | +0.556 | +1.305 | 16 | -0.943 | -0.740 | 16 | -0.054 | +1.081 |
| 4h | calibrated | BRK_mem_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 287 | +0.017 | +0.082 | 286 | +0.350 | +0.415 | 187 | +0.025 | +0.083 | 187 | +0.498 | +0.556 | 100 | -0.107 | -0.029 | 99 | +0.292 | +0.369 |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 144 | +0.254 | +0.236 | 144 | +0.756 | +0.617 | 98 | +0.330 | +0.287 | 98 | +0.526 | +0.342 | 46 | +0.171 | +0.207 | 46 | +2.020 | +1.991 |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 143 | -0.390 | -0.244 | 142 | -0.153 | +0.115 | 89 | -0.388 | -0.229 | 89 | +0.184 | +0.484 | 54 | -0.347 | -0.227 | 53 | -0.708 | -0.524 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | both | 113 | +0.222 | +0.255 | 113 | -0.426 | -0.286 | 83 | +0.224 | +0.200 | 83 | -0.169 | -0.153 | 30 | +0.171 | +0.358 | 30 | -1.834 | -1.405 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | long | 64 | +0.232 | +0.205 | 64 | -0.216 | -0.149 | 50 | +0.460 | +0.359 | 50 | +0.024 | -0.099 | 14 | -0.221 | -0.020 | 14 | -1.172 | -0.534 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | short | 49 | +0.073 | +0.167 | 49 | -1.030 | -0.826 | 33 | +0.009 | +0.075 | 33 | -0.214 | -0.025 | 16 | +0.876 | +1.041 | 16 | -1.989 | -1.740 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | both | 59 | +0.771 | +0.859 | 59 | +1.785 | +1.765 | 39 | +0.277 | +0.415 | 39 | +1.344 | +1.443 | 20 | +1.396 | +1.369 | 20 | +2.345 | +2.074 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | long | 22 | +2.168 | +2.198 | 22 | +3.454 | +3.375 | 14 | +1.927 | +1.988 | 14 | +2.578 | +2.516 | 8 | +2.302 | +2.254 | 8 | +4.156 | +4.026 |
| 4h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | short | 37 | -0.188 | -0.044 | 37 | +0.873 | +0.924 | 25 | -0.179 | +0.032 | 25 | +0.882 | +1.115 | 12 | -0.099 | -0.125 | 12 | +1.281 | +0.816 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | both | 2 | -1.694 | -1.630 | 2 | +9.533 | +9.597 | 2 | -1.694 | -1.644 | 2 | +9.533 | +9.583 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | long | 2 | -1.694 | -1.728 | 2 | +9.533 | +9.489 | 2 | -1.694 | -1.707 | 2 | +9.533 | +8.944 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | both | 64 | -0.454 | -0.382 | 63 | -0.708 | -0.636 | 36 | -0.370 | -0.308 | 36 | +0.259 | +0.321 | 28 | -0.902 | -0.821 | 27 | -1.181 | -1.100 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | long | 33 | +0.076 | -0.001 | 33 | -0.785 | -1.262 | 17 | +0.257 | +0.063 | 17 | -0.773 | -1.029 | 16 | -0.627 | -0.567 | 16 | +0.910 | +0.128 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | short | 31 | -1.101 | -0.878 | 30 | -0.432 | +0.190 | 19 | -2.005 | -1.687 | 19 | +0.517 | +0.898 | 12 | -1.047 | -0.946 | 11 | -1.171 | -0.227 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | both | 49 | -0.624 | -0.555 | 49 | +1.316 | +1.385 | 27 | -1.105 | -1.042 | 27 | +0.489 | +0.552 | 22 | +0.459 | +0.537 | 22 | +1.905 | +1.983 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | long | 23 | +0.492 | +0.474 | 23 | +4.842 | +4.127 | 15 | +0.181 | +0.167 | 15 | +3.838 | +3.214 | 8 | +0.902 | +0.856 | 8 | +9.806 | +8.827 |
| 4h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | short | 26 | -1.474 | -1.318 | 26 | -0.514 | +0.340 | 12 | -1.597 | -1.457 | 12 | -0.535 | +0.215 | 14 | -0.166 | +0.037 | 14 | -1.452 | -0.317 |
| 4h | calibrated | BRK_mem_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_mem_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | SFP_harden | record | ALL | both | 627 | +0.103 | +0.167 | 625 | +0.228 | +0.292 | 396 | -0.013 | +0.045 | 396 | -0.454 | -0.396 | 231 | +0.282 | +0.360 | 229 | +1.123 | +1.200 |
| 4h | calibrated | SFP_harden | record | ALL | long | 315 | +0.240 | +0.222 | 313 | +0.374 | +0.234 | 190 | +0.281 | +0.238 | 190 | -0.586 | -0.769 | 125 | +0.084 | +0.119 | 123 | +2.015 | +1.986 |
| 4h | calibrated | SFP_harden | record | ALL | short | 312 | -0.024 | +0.122 | 312 | +0.011 | +0.279 | 206 | -0.163 | -0.004 | 206 | -0.141 | +0.159 | 106 | +0.647 | +0.767 | 106 | +0.633 | +0.817 |
| 4h | calibrated | SFP_harden | record | EXP_ALIGNED* | both | 159 | +0.239 | +0.272 | 157 | +0.238 | +0.378 | 110 | +0.236 | +0.212 | 110 | +0.643 | +0.659 | 49 | +0.266 | +0.453 | 47 | -0.913 | -0.484 |
| 4h | calibrated | SFP_harden | record | EXP_ALIGNED* | long | 89 | -0.146 | -0.173 | 87 | -0.900 | -0.833 | 58 | +0.264 | +0.162 | 58 | -0.733 | -0.856 | 31 | -0.930 | -0.729 | 29 | -0.913 | -0.275 |
| 4h | calibrated | SFP_harden | record | EXP_ALIGNED* | short | 70 | +0.366 | +0.460 | 70 | +1.230 | +1.434 | 52 | +0.154 | +0.220 | 52 | +1.364 | +1.553 | 18 | +1.105 | +1.269 | 18 | -2.243 | -1.995 |
| 4h | calibrated | SFP_harden | record | EXP_COUNTER | both | 152 | +0.437 | +0.525 | 152 | +0.340 | +0.321 | 107 | +0.190 | +0.329 | 107 | -0.479 | -0.380 | 45 | +0.917 | +0.890 | 45 | +3.187 | +2.916 |
| 4h | calibrated | SFP_harden | record | EXP_COUNTER | long | 75 | +0.453 | +0.483 | 75 | +1.145 | +1.065 | 47 | +0.435 | +0.496 | 47 | -0.492 | -0.554 | 28 | +0.466 | +0.419 | 28 | +3.939 | +3.809 |
| 4h | calibrated | SFP_harden | record | EXP_COUNTER | short | 77 | +0.320 | +0.465 | 77 | -0.566 | -0.515 | 60 | -0.141 | +0.070 | 60 | -0.709 | -0.477 | 17 | +1.548 | +1.522 | 17 | +1.020 | +0.556 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | both | 46 | +0.463 | +0.527 | 46 | +1.532 | +1.596 | 25 | +0.264 | +0.314 | 25 | +0.027 | +0.078 | 21 | +0.710 | +0.782 | 21 | +3.080 | +3.152 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | long | 24 | +0.691 | +0.658 | 24 | +1.900 | +1.856 | 15 | +0.658 | +0.645 | 15 | +0.129 | -0.460 | 9 | +0.723 | +0.647 | 9 | +3.544 | +4.160 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | short | 22 | -1.597 | -1.435 | 22 | +1.488 | +1.660 | 10 | -2.128 | -2.015 | 10 | -5.381 | -4.692 | 12 | -0.168 | +0.051 | 12 | +2.269 | +1.796 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_MID* | both | 106 | -0.474 | -0.401 | 106 | -0.866 | -0.794 | 64 | -0.454 | -0.392 | 64 | -2.646 | -2.584 | 42 | -0.849 | -0.768 | 42 | -0.418 | -0.337 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_MID* | long | 44 | -0.656 | -0.733 | 44 | -1.092 | -1.569 | 25 | -0.271 | -0.465 | 25 | -2.540 | -2.796 | 19 | -0.961 | -0.901 | 19 | -0.953 | -1.735 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_MID* | short | 62 | -0.483 | -0.260 | 62 | -0.660 | -0.038 | 39 | -0.456 | -0.139 | 39 | -3.943 | -3.562 | 23 | -0.492 | -0.390 | 23 | -0.144 | +0.800 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_OTHER | both | 164 | +0.264 | +0.333 | 164 | +0.507 | +0.576 | 90 | +0.075 | +0.138 | 90 | -1.225 | -1.162 | 74 | +0.434 | +0.513 | 74 | +2.190 | +2.268 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_OTHER | long | 83 | +0.290 | +0.273 | 83 | +1.161 | +0.446 | 45 | +0.290 | +0.276 | 45 | -0.808 | -1.433 | 38 | +0.331 | +0.285 | 38 | +4.293 | +3.314 |
| 4h | calibrated | SFP_harden | record | IN_RANGE_OTHER | short | 81 | +0.188 | +0.345 | 81 | -1.585 | -0.732 | 45 | -0.001 | +0.139 | 45 | -2.187 | -1.437 | 36 | +0.639 | +0.842 | 36 | -0.396 | +0.739 |
| 4h | calibrated | SFP_harden | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | SFP_harden | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 4h | calibrated | SFP_harden | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | ALL | both | 137 | -0.052 | -0.017 | 136 | +0.259 | +0.293 | 87 | +0.352 | +0.384 | 87 | +0.565 | +0.597 | 50 | -0.437 | -0.394 | 49 | -0.429 | -0.387 |
| 12h | calibrated | BRK_tap89_first | record | ALL | long | 79 | +0.155 | +0.050 | 79 | +1.306 | +0.710 | 57 | +0.411 | +0.295 | 57 | +2.497 | +1.612 | 22 | -0.541 | -0.619 | 22 | -0.363 | -0.419 |
| 12h | calibrated | BRK_tap89_first | record | ALL | short | 58 | -0.207 | -0.033 | 57 | -0.844 | -0.179 | 30 | +0.200 | +0.379 | 30 | -0.460 | +0.489 | 28 | -0.343 | -0.180 | 27 | -0.848 | -0.709 |
| 12h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | both | 83 | -0.079 | -0.033 | 83 | -0.221 | +0.219 | 53 | +0.161 | +0.104 | 53 | +1.788 | +1.296 | 30 | -0.539 | -0.271 | 30 | -1.930 | -0.081 |
| 12h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | long | 51 | +0.097 | -0.084 | 51 | +0.502 | -0.259 | 38 | +0.292 | +0.028 | 38 | +2.668 | +1.131 | 13 | -0.554 | -0.504 | 13 | -0.544 | +0.785 |
| 12h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | short | 32 | -0.289 | +0.008 | 32 | -1.976 | -0.179 | 15 | +0.079 | +0.274 | 15 | +0.292 | +1.666 | 17 | -0.348 | +0.135 | 17 | -3.021 | -0.737 |
| 12h | calibrated | BRK_tap89_first | record | EXP_COUNTER | both | 27 | -0.182 | -0.163 | 26 | +1.896 | +1.522 | 18 | -0.280 | -0.165 | 18 | -0.157 | +0.393 | 9 | -0.189 | -0.375 | 8 | +2.980 | +1.212 |
| 12h | calibrated | BRK_tap89_first | record | EXP_COUNTER | long | 16 | +0.267 | +0.038 | 16 | +2.326 | +0.596 | 12 | +0.532 | +0.391 | 12 | +0.865 | -0.455 | 4 | -0.359 | -0.761 | 4 | +4.097 | +1.892 |
| 12h | calibrated | BRK_tap89_first | record | EXP_COUNTER | short | 11 | -0.479 | -0.234 | 10 | +1.065 | +1.890 | 6 | -0.640 | -0.316 | 6 | -0.340 | +1.257 | 5 | -0.166 | -0.129 | 4 | +2.753 | +1.511 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | both | 16 | +1.328 | +1.363 | 16 | -0.862 | -0.827 | 9 | +2.891 | +2.925 | 9 | -1.953 | -1.919 | 7 | +1.182 | +1.221 | 7 | +3.233 | +3.272 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | long | 9 | -0.271 | +0.359 | 9 | -0.855 | +1.055 | 5 | -0.271 | +0.550 | 5 | -0.855 | +2.086 | 4 | -0.768 | -0.448 | 4 | +0.172 | +1.184 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | short | 7 | +2.891 | +2.330 | 7 | -0.845 | -2.686 | 4 | +3.192 | +2.439 | 4 | -6.741 | -9.613 | 3 | +1.733 | +1.490 | 3 | +3.233 | +2.299 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | both | 11 | -0.953 | -0.915 | 11 | -1.481 | -1.444 | 7 | +0.427 | +0.463 | 7 | +5.253 | +5.290 | 4 | -3.241 | -3.197 | 4 | -3.294 | -3.253 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | long | 3 | +3.940 | +3.838 | 3 | -1.481 | -0.037 | 2 | +1.494 | +1.299 | 2 | +2.650 | +3.608 | 1 | +4.348 | +4.375 | 1 | -1.456 | +0.484 |
| 12h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | short | 8 | -1.747 | -1.569 | 8 | -1.193 | -2.563 | 5 | +0.435 | +0.703 | 5 | +5.262 | +4.376 | 3 | -4.028 | -3.967 | 3 | -5.112 | -6.970 |
| 12h | calibrated | BRK_tap89_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 115 | +0.180 | +0.215 | 115 | -0.211 | -0.176 | 74 | +0.469 | +0.501 | 74 | +0.749 | +0.781 | 41 | -0.521 | -0.479 | 41 | -1.120 | -1.079 |
| 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 66 | +0.416 | +0.312 | 66 | +1.546 | +0.950 | 48 | +0.527 | +0.411 | 48 | +2.710 | +1.825 | 18 | -0.541 | -0.619 | 18 | -0.486 | -0.543 |
| 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 49 | -0.179 | -0.005 | 49 | -1.233 | -0.567 | 26 | +0.246 | +0.425 | 26 | -1.207 | -0.258 | 23 | -0.344 | -0.181 | 23 | -2.991 | -2.852 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | both | 74 | -0.060 | -0.014 | 74 | -0.340 | +0.099 | 48 | +0.297 | +0.241 | 48 | +1.365 | +0.873 | 26 | -0.548 | -0.280 | 26 | -2.461 | -0.612 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | long | 44 | +0.129 | -0.052 | 44 | +0.376 | -0.385 | 34 | +0.461 | +0.198 | 34 | +2.670 | +1.133 | 10 | -0.557 | -0.507 | 10 | -1.059 | +0.270 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | short | 30 | -0.287 | +0.010 | 30 | -2.870 | -1.072 | 14 | -0.067 | +0.128 | 14 | -0.439 | +0.935 | 16 | -0.648 | -0.164 | 16 | -3.311 | -1.027 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | both | 20 | +0.186 | +0.205 | 20 | +2.275 | +1.901 | 13 | +0.510 | +0.625 | 13 | +0.569 | +1.119 | 7 | +0.164 | -0.021 | 7 | +3.893 | +2.125 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | long | 12 | +0.518 | +0.290 | 12 | +3.104 | +1.374 | 9 | +0.549 | +0.408 | 9 | +2.585 | +1.265 | 3 | +0.187 | -0.215 | 3 | +6.126 | +3.921 |
| 12h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | short | 8 | -0.328 | -0.083 | 8 | +1.068 | +1.894 | 4 | -1.660 | -1.336 | 4 | -0.337 | +1.261 | 4 | +0.011 | +0.048 | 4 | +2.753 | +1.511 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | both | 12 | +1.328 | +1.363 | 12 | -1.012 | -0.978 | 7 | +3.179 | +3.213 | 7 | -3.925 | -3.891 | 5 | +0.460 | +0.498 | 5 | +3.367 | +3.405 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | long | 7 | +0.409 | +1.040 | 7 | +3.678 | +5.588 | 3 | +0.409 | +1.231 | 3 | +10.856 | +13.797 | 4 | -0.768 | -0.448 | 4 | +0.172 | +1.184 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | short | 5 | +3.179 | +2.618 | 5 | -4.980 | -6.821 | 4 | +3.192 | +2.439 | 4 | -6.741 | -9.613 | 1 | +1.512 | +1.270 | 1 | +3.367 | +2.432 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | both | 9 | +0.427 | +0.465 | 9 | -3.546 | -3.509 | 6 | +0.609 | +0.646 | 6 | +0.854 | +0.890 | 3 | -2.455 | -2.410 | 3 | -5.112 | -5.071 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | long | 3 | +3.940 | +3.838 | 3 | -1.481 | -0.037 | 2 | +1.494 | +1.299 | 2 | +2.650 | +3.608 | 1 | +4.348 | +4.375 | 1 | -1.456 | +0.484 |
| 12h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | short | 6 | -1.012 | -0.833 | 6 | -5.105 | -6.474 | 4 | +0.618 | +0.885 | 4 | +0.084 | -0.802 | 2 | -3.241 | -3.180 | 2 | -9.496 | -11.354 |
| 12h | calibrated | BRK_tap89_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap89_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_first | record | ALL | both | 118 | +0.164 | +0.199 | 117 | -0.416 | -0.382 | 73 | +0.069 | +0.101 | 73 | -0.287 | -0.255 | 45 | +0.329 | +0.372 | 44 | -0.477 | -0.435 |
| 12h | calibrated | BRK_tap127_first | record | ALL | long | 70 | +0.090 | -0.014 | 70 | +0.422 | -0.174 | 48 | -0.009 | -0.124 | 48 | +1.335 | +0.450 | 22 | +0.795 | +0.718 | 22 | -1.563 | -1.620 |
| 12h | calibrated | BRK_tap127_first | record | ALL | short | 48 | +0.222 | +0.397 | 47 | -0.552 | +0.113 | 25 | +0.257 | +0.437 | 25 | -2.849 | -1.900 | 23 | +0.158 | +0.321 | 22 | +0.208 | +0.347 |
| 12h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | both | 67 | -0.051 | -0.005 | 67 | +0.214 | +0.653 | 45 | -0.068 | -0.125 | 45 | +1.378 | +0.886 | 22 | +0.152 | +0.420 | 22 | -3.218 | -1.369 |
| 12h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | long | 43 | -0.357 | -0.538 | 43 | +1.292 | +0.530 | 32 | -0.409 | -0.673 | 32 | +4.232 | +2.695 | 11 | -0.014 | +0.036 | 11 | -3.367 | -2.038 |
| 12h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | short | 24 | +0.168 | +0.465 | 24 | -0.241 | +1.556 | 13 | +0.064 | +0.259 | 13 | +0.212 | +1.586 | 11 | +0.327 | +0.811 | 11 | -0.680 | +1.604 |
| 12h | calibrated | BRK_tap127_first | record | EXP_COUNTER | both | 24 | +0.045 | +0.064 | 23 | +0.219 | -0.155 | 15 | +0.480 | +0.595 | 15 | -0.873 | -0.323 | 9 | -0.666 | -0.852 | 8 | +2.059 | +0.290 |
| 12h | calibrated | BRK_tap127_first | record | EXP_COUNTER | long | 13 | +2.325 | +2.097 | 13 | +1.128 | -0.602 | 9 | +2.333 | +2.192 | 9 | +1.136 | -0.184 | 4 | +2.534 | +2.132 | 4 | +3.188 | +0.983 |
| 12h | calibrated | BRK_tap127_first | record | EXP_COUNTER | short | 11 | -0.956 | -0.711 | 10 | -0.166 | +0.659 | 6 | -0.537 | -0.213 | 6 | -3.341 | -1.744 | 5 | -1.422 | -1.385 | 4 | +2.079 | +0.837 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | both | 1 | +1.241 | +1.286 | 1 | +14.022 | +14.066 | 0 | — | — | 0 | — | — | 1 | +1.241 | +1.286 | 1 | +14.022 | +14.066 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | long | 1 | +1.241 | +1.149 | 1 | +14.022 | +14.028 | 0 | — | — | 0 | — | — | 1 | +1.241 | +1.305 | 1 | +14.022 | +14.790 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | both | 18 | +0.762 | +0.796 | 18 | -0.818 | -0.784 | 8 | +0.741 | +0.775 | 8 | -2.644 | -2.610 | 10 | +0.763 | +0.802 | 10 | +0.948 | +0.987 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | long | 8 | -0.225 | +0.405 | 8 | -0.830 | +1.079 | 4 | -0.225 | +0.596 | 4 | -0.830 | +2.110 | 4 | -0.768 | -0.448 | 4 | +0.172 | +1.184 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | short | 10 | +1.291 | +0.730 | 10 | -0.826 | -2.666 | 4 | +2.133 | +1.380 | 4 | -10.021 | -12.894 | 6 | +1.298 | +1.056 | 6 | +0.948 | +0.014 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | both | 8 | +0.617 | +0.655 | 8 | -2.522 | -2.485 | 5 | +0.024 | +0.061 | 5 | -3.546 | -3.509 | 3 | +2.963 | +3.007 | 3 | -1.497 | -1.457 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | long | 5 | +0.016 | -0.087 | 5 | -1.489 | -0.045 | 3 | +0.024 | -0.171 | 3 | -3.546 | -2.587 | 2 | +0.975 | +1.002 | 2 | +1.258 | +3.198 |
| 12h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | short | 3 | +1.232 | +1.410 | 3 | -5.098 | -6.467 | 2 | +0.445 | +0.713 | 2 | -2.017 | -2.903 | 1 | +2.984 | +3.045 | 1 | -6.823 | -8.681 |
| 12h | calibrated | BRK_tap127_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 101 | +0.305 | +0.340 | 101 | +0.213 | +0.247 | 63 | +0.281 | +0.313 | 63 | +0.218 | +0.250 | 38 | +0.379 | +0.422 | 38 | -0.110 | -0.068 |
| 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 58 | +0.390 | +0.285 | 58 | +1.340 | +0.744 | 39 | +0.377 | +0.262 | 39 | +4.222 | +3.337 | 19 | +0.434 | +0.356 | 19 | -0.430 | -0.486 |
| 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 43 | +0.272 | +0.446 | 43 | -0.666 | -0.000 | 24 | +0.167 | +0.346 | 24 | -2.873 | -1.924 | 19 | +0.327 | +0.490 | 19 | +0.212 | +0.352 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | both | 61 | -0.003 | +0.043 | 61 | +0.927 | +1.367 | 41 | -0.044 | -0.100 | 41 | +1.585 | +1.093 | 20 | +0.152 | +0.420 | 20 | -1.870 | -0.021 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | long | 37 | -0.047 | -0.228 | 37 | +1.308 | +0.547 | 28 | -0.199 | -0.463 | 28 | +4.662 | +3.125 | 9 | -0.014 | +0.036 | 9 | -3.050 | -1.720 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | short | 24 | +0.168 | +0.465 | 24 | -0.241 | +1.556 | 13 | +0.064 | +0.259 | 13 | +0.212 | +1.586 | 11 | +0.327 | +0.811 | 11 | -0.680 | +1.604 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | both | 17 | +0.173 | +0.192 | 17 | +0.227 | -0.147 | 11 | +0.479 | +0.593 | 11 | -0.874 | -0.324 | 6 | -0.249 | -0.435 | 6 | +5.950 | +4.182 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | long | 9 | +3.266 | +3.038 | 9 | +8.004 | +6.274 | 6 | +2.818 | +2.677 | 6 | +4.700 | +3.380 | 3 | +3.836 | +3.434 | 3 | +8.004 | +5.799 |
| 12h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | short | 8 | -1.196 | -0.951 | 8 | -0.892 | -0.067 | 5 | -0.956 | -0.632 | 5 | -5.415 | -3.818 | 3 | -1.422 | -1.385 | 3 | +3.916 | +2.674 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | both | 1 | +1.241 | +1.286 | 1 | +14.022 | +14.066 | 0 | — | — | 0 | — | — | 1 | +1.241 | +1.286 | 1 | +14.022 | +14.066 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | long | 1 | +1.241 | +1.149 | 1 | +14.022 | +14.028 | 0 | — | — | 0 | — | — | 1 | +1.241 | +1.305 | 1 | +14.022 | +14.790 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | both | 15 | +1.071 | +1.105 | 15 | -1.140 | -1.105 | 7 | +1.073 | +1.107 | 7 | -3.913 | -3.879 | 8 | +0.763 | +0.802 | 8 | +1.592 | +1.630 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | long | 7 | +0.409 | +1.039 | 7 | -1.375 | +0.535 | 3 | +0.409 | +1.230 | 3 | -1.375 | +1.566 | 4 | -0.768 | -0.448 | 4 | +0.172 | +1.184 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | short | 8 | +1.289 | +0.728 | 8 | -0.828 | -2.668 | 4 | +2.133 | +1.380 | 4 | -10.021 | -12.894 | 4 | +1.298 | +1.056 | 4 | +2.157 | +1.222 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | both | 7 | +1.219 | +1.257 | 7 | -1.489 | -1.452 | 4 | +0.424 | +0.460 | 4 | -1.261 | -1.225 | 3 | +2.963 | +3.007 | 3 | -1.497 | -1.457 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | long | 4 | +1.485 | +1.383 | 4 | +1.266 | +2.710 | 2 | +1.494 | +1.299 | 2 | +2.650 | +3.608 | 2 | +0.975 | +1.002 | 2 | +1.258 | +3.198 |
| 12h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | short | 3 | +1.232 | +1.410 | 3 | -5.098 | -6.467 | 2 | +0.445 | +0.713 | 2 | -2.017 | -2.903 | 1 | +2.984 | +3.045 | 1 | -6.823 | -8.681 |
| 12h | calibrated | BRK_tap127_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap127_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_first | record | ALL | both | 99 | +0.147 | +0.182 | 98 | -0.249 | -0.214 | 59 | +0.286 | +0.318 | 59 | -0.866 | -0.834 | 40 | +0.087 | +0.130 | 39 | -0.223 | -0.182 |
| 12h | calibrated | BRK_tap200_first | record | ALL | long | 54 | +0.183 | +0.079 | 54 | -1.020 | -1.616 | 34 | +0.455 | +0.340 | 34 | -0.175 | -1.061 | 20 | -0.112 | -0.190 | 20 | -1.550 | -1.606 |
| 12h | calibrated | BRK_tap200_first | record | ALL | short | 45 | +0.137 | +0.311 | 44 | +0.010 | +0.676 | 25 | -0.086 | +0.093 | 25 | -1.235 | -0.286 | 20 | +0.223 | +0.386 | 19 | +0.071 | +0.210 |
| 12h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | both | 47 | +0.664 | +0.709 | 47 | +1.001 | +1.440 | 32 | +0.394 | +0.338 | 32 | +2.245 | +1.753 | 15 | +1.304 | +1.572 | 15 | -1.616 | +0.233 |
| 12h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | long | 31 | +0.664 | +0.483 | 31 | +1.131 | +0.370 | 22 | +0.580 | +0.316 | 22 | +2.245 | +0.708 | 9 | +0.677 | +0.727 | 9 | -1.722 | -0.392 |
| 12h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | short | 16 | +0.506 | +0.803 | 16 | +0.569 | +2.366 | 10 | +0.101 | +0.296 | 10 | +3.184 | +4.558 | 6 | +1.392 | +1.876 | 6 | -0.049 | +2.235 |
| 12h | calibrated | BRK_tap200_first | record | EXP_COUNTER | both | 19 | -0.553 | -0.534 | 18 | -1.053 | -1.427 | 12 | -1.029 | -0.915 | 12 | -4.493 | -3.943 | 7 | -0.444 | -0.630 | 6 | +2.751 | +0.983 |
| 12h | calibrated | BRK_tap200_first | record | EXP_COUNTER | long | 9 | -0.104 | -0.332 | 9 | -0.878 | -2.608 | 6 | -0.315 | -0.456 | 6 | -5.952 | -7.272 | 3 | -0.104 | -0.506 | 3 | +4.099 | +1.893 |
| 12h | calibrated | BRK_tap200_first | record | EXP_COUNTER | short | 10 | -0.666 | -0.421 | 9 | -1.238 | -0.412 | 6 | -1.055 | -0.731 | 6 | -2.744 | -1.147 | 4 | -0.593 | -0.556 | 3 | -0.034 | -1.276 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | both | 3 | +1.001 | +1.045 | 3 | +0.805 | +0.850 | 2 | +0.448 | +0.491 | 2 | +0.133 | +0.177 | 1 | +1.001 | +1.046 | 1 | +0.805 | +0.850 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | long | 2 | +1.122 | +1.031 | 2 | -1.172 | -1.165 | 1 | +1.283 | +1.111 | 1 | -3.109 | -3.616 | 1 | +1.001 | +1.064 | 1 | +0.805 | +1.574 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | short | 1 | -0.371 | -0.190 | 1 | +3.392 | +3.475 | 1 | -0.371 | -0.112 | 1 | +3.392 | +3.987 | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | both | 22 | +0.177 | +0.212 | 22 | -0.833 | -0.799 | 9 | +2.884 | +2.918 | 9 | -3.932 | -3.898 | 13 | -0.101 | -0.062 | 13 | -0.205 | -0.167 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | long | 9 | -0.385 | +0.246 | 9 | -3.038 | -1.128 | 4 | +0.010 | +0.831 | 4 | -2.641 | +0.300 | 5 | -1.355 | -1.035 | 5 | -3.035 | -2.023 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | short | 13 | +1.598 | +1.037 | 13 | +0.065 | -1.776 | 5 | +8.312 | +7.559 | 5 | -4.988 | -7.860 | 8 | +0.196 | -0.047 | 8 | +0.575 | -0.359 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | both | 8 | +0.314 | +0.352 | 8 | -4.331 | -4.294 | 4 | +0.157 | +0.193 | 4 | -4.304 | -4.268 | 4 | +0.610 | +0.654 | 4 | -4.727 | -4.686 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | long | 3 | -0.579 | -0.681 | 3 | -3.540 | -2.096 | 1 | -0.922 | -1.117 | 1 | -3.515 | -2.557 | 2 | +1.875 | +1.903 | 2 | -4.714 | -2.774 |
| 12h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | short | 5 | +1.220 | +1.399 | 5 | -5.109 | -6.479 | 3 | +1.247 | +1.515 | 3 | -5.082 | -5.968 | 2 | -0.189 | -0.127 | 2 | -4.815 | -6.674 |
| 12h | calibrated | BRK_tap200_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 86 | +0.301 | +0.336 | 86 | -0.754 | -0.719 | 55 | +0.286 | +0.318 | 55 | -1.178 | -1.146 | 31 | +0.309 | +0.352 | 31 | -0.295 | -0.253 |
| 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 49 | +0.411 | +0.306 | 49 | -1.176 | -1.772 | 32 | +0.455 | +0.340 | 32 | -0.175 | -1.061 | 17 | -0.105 | -0.183 | 17 | -1.611 | -1.667 |
| 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 37 | +0.272 | +0.447 | 37 | -0.223 | +0.442 | 23 | -0.086 | +0.093 | 23 | -2.100 | -1.151 | 14 | +0.810 | +0.972 | 14 | +0.010 | +0.150 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | both | 42 | +0.580 | +0.625 | 42 | +0.574 | +1.013 | 30 | +0.126 | +0.069 | 30 | +1.874 | +1.382 | 12 | +1.377 | +1.645 | 12 | -1.667 | +0.182 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | long | 27 | +0.664 | +0.483 | 27 | +1.131 | +0.370 | 21 | +0.496 | +0.233 | 21 | +2.219 | +0.682 | 6 | +1.146 | +1.196 | 6 | -2.741 | -1.412 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | short | 15 | +0.287 | +0.583 | 15 | +0.549 | +2.346 | 9 | -0.084 | +0.111 | 9 | +1.366 | +2.739 | 6 | +1.392 | +1.876 | 6 | -0.049 | +2.235 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | both | 14 | -0.434 | -0.414 | 14 | -1.053 | -1.427 | 10 | -0.795 | -0.680 | 10 | -4.493 | -3.943 | 4 | -0.439 | -0.624 | 4 | +2.751 | +0.983 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | long | 8 | +0.711 | +0.483 | 8 | +0.263 | -1.467 | 5 | +1.728 | +1.587 | 5 | -4.765 | -6.084 | 3 | -0.104 | -0.506 | 3 | +4.099 | +1.893 |
| 12h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | short | 6 | -1.137 | -0.892 | 6 | -2.718 | -1.893 | 5 | -1.510 | -1.186 | 5 | -4.209 | -2.612 | 1 | -0.736 | -0.698 | 1 | -0.012 | -1.255 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | both | 3 | +1.001 | +1.045 | 3 | +0.805 | +0.850 | 2 | +0.448 | +0.491 | 2 | +0.133 | +0.177 | 1 | +1.001 | +1.046 | 1 | +0.805 | +0.850 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | long | 2 | +1.122 | +1.031 | 2 | -1.172 | -1.165 | 1 | +1.283 | +1.111 | 1 | -3.109 | -3.616 | 1 | +1.001 | +1.064 | 1 | +0.805 | +1.574 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | -0.371 | -0.190 | 1 | +3.392 | +3.475 | 1 | -0.371 | -0.112 | 1 | +3.392 | +3.987 | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | both | 19 | +0.313 | +0.348 | 19 | -1.376 | -1.341 | 9 | +2.884 | +2.918 | 9 | -3.932 | -3.898 | 10 | -0.739 | -0.700 | 10 | -0.252 | -0.213 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | long | 9 | -0.385 | +0.246 | 9 | -3.038 | -1.128 | 4 | +0.010 | +0.831 | 4 | -2.641 | +0.300 | 5 | -1.355 | -1.035 | 5 | -3.035 | -2.023 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | short | 10 | +3.776 | +3.215 | 10 | -0.083 | -1.923 | 5 | +8.312 | +7.559 | 5 | -4.988 | -7.860 | 5 | +0.316 | +0.074 | 5 | +0.078 | -0.856 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | both | 8 | +0.314 | +0.352 | 8 | -4.331 | -4.294 | 4 | +0.157 | +0.193 | 4 | -4.304 | -4.268 | 4 | +0.610 | +0.654 | 4 | -4.727 | -4.686 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | long | 3 | -0.579 | -0.681 | 3 | -3.540 | -2.096 | 1 | -0.922 | -1.117 | 1 | -3.515 | -2.557 | 2 | +1.875 | +1.903 | 2 | -4.714 | -2.774 |
| 12h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | short | 5 | +1.220 | +1.399 | 5 | -5.109 | -6.479 | 3 | +1.247 | +1.515 | 3 | -5.082 | -5.968 | 2 | -0.189 | -0.127 | 2 | -4.815 | -6.674 |
| 12h | calibrated | BRK_tap200_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_tap200_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_first | record | ALL | both | 100 | +0.274 | +0.309 | 100 | -0.635 | -0.600 | 63 | +0.346 | +0.377 | 63 | -0.359 | -0.327 | 37 | +0.089 | +0.132 | 37 | -1.111 | -1.070 |
| 12h | calibrated | BRK_mem_first | record | ALL | long | 58 | +0.215 | +0.110 | 58 | +0.004 | -0.592 | 40 | +0.239 | +0.124 | 40 | +0.205 | -0.680 | 18 | +0.076 | -0.002 | 18 | -1.026 | -1.083 |
| 12h | calibrated | BRK_mem_first | record | ALL | short | 42 | +0.543 | +0.717 | 42 | -1.290 | -0.624 | 23 | +0.694 | +0.873 | 23 | -1.823 | -0.874 | 19 | +0.102 | +0.265 | 19 | -1.098 | -0.959 |
| 12h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | both | 52 | +0.336 | +0.382 | 52 | -0.393 | +0.047 | 34 | +0.468 | +0.411 | 34 | +0.568 | +0.076 | 18 | -0.143 | +0.125 | 18 | -1.636 | +0.213 |
| 12h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | long | 31 | -0.191 | -0.372 | 31 | +0.600 | -0.161 | 24 | -0.036 | -0.300 | 24 | +0.686 | -0.851 | 7 | -0.183 | -0.133 | 7 | -1.270 | +0.059 |
| 12h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | short | 21 | +0.844 | +1.141 | 21 | -1.385 | +0.412 | 10 | +0.878 | +1.073 | 10 | +0.098 | +1.471 | 11 | +0.631 | +1.115 | 11 | -1.887 | +0.397 |
| 12h | calibrated | BRK_mem_first | record | EXP_COUNTER | both | 22 | -0.015 | +0.005 | 22 | -1.164 | -1.538 | 16 | -0.460 | -0.346 | 16 | -2.466 | -1.916 | 6 | +0.262 | +0.076 | 6 | +4.394 | +2.626 |
| 12h | calibrated | BRK_mem_first | record | EXP_COUNTER | long | 13 | +0.521 | +0.293 | 13 | -0.074 | -1.804 | 10 | +1.087 | +0.947 | 10 | -0.336 | -1.656 | 3 | +0.520 | +0.118 | 3 | +4.865 | +2.660 |
| 12h | calibrated | BRK_mem_first | record | EXP_COUNTER | short | 9 | -0.388 | -0.143 | 9 | -1.814 | -0.989 | 6 | -0.925 | -0.601 | 6 | -3.470 | -1.873 | 3 | +0.007 | +0.045 | 3 | +3.926 | +2.684 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | both | 4 | -0.417 | -0.372 | 4 | +2.217 | +2.261 | 1 | -1.009 | -0.965 | 1 | +3.288 | +3.332 | 3 | +0.206 | +0.251 | 3 | +1.176 | +1.221 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | long | 3 | +0.206 | +0.114 | 3 | +1.176 | +1.182 | 0 | — | — | 0 | — | — | 3 | +0.206 | +0.270 | 3 | +1.176 | +1.945 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | short | 1 | -1.009 | -0.828 | 1 | +3.288 | +3.371 | 1 | -1.009 | -0.750 | 1 | +3.288 | +3.883 | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | both | 9 | +1.474 | +1.508 | 9 | -1.039 | -1.004 | 5 | +1.474 | +1.508 | 5 | +1.530 | +1.564 | 4 | -0.322 | -0.284 | 4 | -1.075 | -1.036 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | long | 5 | -1.588 | -0.958 | 5 | -1.140 | +0.769 | 2 | -0.051 | +0.770 | 2 | -0.765 | +2.176 | 3 | -2.621 | -2.301 | 3 | -1.132 | -0.120 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | short | 4 | +1.993 | +1.432 | 4 | +0.239 | -1.602 | 3 | +2.037 | +1.284 | 3 | +1.523 | -1.349 | 1 | +1.983 | +1.740 | 1 | -1.011 | -1.945 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | both | 13 | +0.421 | +0.459 | 13 | -0.868 | -0.831 | 7 | +0.421 | +0.457 | 7 | -0.662 | -0.625 | 6 | +0.710 | +0.754 | 6 | -0.973 | -0.932 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | long | 6 | +1.558 | +1.455 | 6 | -0.765 | +0.679 | 4 | +0.353 | +0.158 | 4 | +2.860 | +3.819 | 2 | +3.590 | +3.618 | 2 | -2.008 | -0.068 |
| 12h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | short | 7 | +0.104 | +0.283 | 7 | -1.096 | -2.466 | 3 | +1.549 | +1.816 | 3 | -6.713 | -7.598 | 4 | -0.121 | -0.060 | 4 | +0.297 | -1.561 |
| 12h | calibrated | BRK_mem_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 104 | +0.224 | +0.259 | 104 | -0.538 | -0.503 | 66 | +0.275 | +0.307 | 66 | -0.219 | -0.187 | 38 | -0.031 | +0.012 | 38 | -1.080 | -1.038 |
| 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 58 | +0.265 | +0.161 | 58 | +0.004 | -0.592 | 41 | +0.288 | +0.173 | 41 | +0.319 | -0.566 | 17 | -0.055 | -0.132 | 17 | -1.166 | -1.223 |
| 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 46 | +0.042 | +0.216 | 46 | -1.075 | -0.410 | 25 | +0.219 | +0.398 | 25 | -1.737 | -0.788 | 21 | -0.007 | +0.155 | 21 | -1.041 | -0.902 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | both | 51 | +0.264 | +0.310 | 51 | -0.387 | +0.052 | 35 | +0.400 | +0.343 | 35 | +0.773 | +0.281 | 16 | -0.372 | -0.104 | 16 | -2.202 | -0.353 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | long | 31 | -0.191 | -0.372 | 31 | +0.090 | -0.672 | 25 | +0.267 | +0.004 | 25 | +0.773 | -0.764 | 6 | -0.517 | -0.467 | 6 | -2.822 | -1.492 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | short | 20 | +0.765 | +1.061 | 20 | -0.954 | +0.843 | 10 | +0.782 | +0.977 | 10 | +1.152 | +2.526 | 10 | +0.487 | +0.970 | 10 | -1.681 | +0.603 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | both | 24 | -0.011 | +0.009 | 24 | -1.124 | -1.499 | 18 | -0.454 | -0.339 | 18 | -1.765 | -1.215 | 6 | +0.262 | +0.076 | 6 | +4.394 | +2.626 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | long | 12 | +0.536 | +0.308 | 12 | +0.123 | -1.607 | 9 | +0.556 | +0.415 | 9 | -0.069 | -1.389 | 3 | +0.520 | +0.118 | 3 | +4.865 | +2.660 |
| 12h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | short | 12 | -0.604 | -0.359 | 12 | -1.771 | -0.946 | 9 | -1.022 | -0.698 | 9 | -3.125 | -1.527 | 3 | +0.007 | +0.045 | 3 | +3.926 | +2.684 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | both | 4 | -0.417 | -0.372 | 4 | +2.217 | +2.261 | 1 | -1.009 | -0.965 | 1 | +3.288 | +3.332 | 3 | +0.206 | +0.251 | 3 | +1.176 | +1.221 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | long | 3 | +0.206 | +0.114 | 3 | +1.176 | +1.182 | 0 | — | — | 0 | — | — | 3 | +0.206 | +0.270 | 3 | +1.176 | +1.945 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | -1.009 | -0.828 | 1 | +3.288 | +3.371 | 1 | -1.009 | -0.750 | 1 | +3.288 | +3.883 | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | both | 9 | -1.824 | -1.789 | 9 | -1.148 | -1.114 | 5 | -1.596 | -1.562 | 5 | -4.859 | -4.825 | 4 | -2.214 | -2.176 | 4 | -1.075 | -1.036 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | long | 4 | -2.109 | -1.479 | 4 | -2.996 | -1.086 | 2 | -0.051 | +0.770 | 2 | -0.765 | +2.176 | 2 | -4.232 | -3.912 | 2 | -3.122 | -2.110 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | short | 5 | -1.837 | -2.398 | 5 | -1.048 | -2.888 | 3 | -2.330 | -3.083 | 3 | -9.206 | -12.079 | 2 | +0.089 | -0.154 | 2 | +1.130 | +0.196 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | both | 16 | +0.353 | +0.391 | 16 | +0.094 | +0.131 | 7 | +0.421 | +0.457 | 7 | +3.411 | +3.448 | 9 | +0.113 | +0.157 | 9 | -0.853 | -0.813 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | long | 8 | +0.638 | +0.536 | 8 | +0.636 | +2.080 | 5 | +0.421 | +0.226 | 5 | +6.382 | +7.340 | 3 | +2.579 | +2.606 | 3 | -0.850 | +1.090 |
| 12h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | short | 8 | -0.131 | +0.047 | 8 | -0.120 | -1.490 | 2 | +0.270 | +0.537 | 2 | -1.658 | -2.544 | 6 | -0.125 | -0.063 | 6 | -0.114 | -1.972 |
| 12h | calibrated | BRK_mem_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | BRK_mem_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | SFP_harden | record | ALL | both | 197 | -0.028 | +0.007 | 197 | +0.854 | +0.889 | 105 | -0.186 | -0.154 | 105 | +1.149 | +1.181 | 92 | +0.088 | +0.131 | 92 | +0.558 | +0.600 |
| 12h | calibrated | SFP_harden | record | ALL | long | 90 | +0.168 | +0.064 | 90 | +1.413 | +0.817 | 47 | +0.143 | +0.028 | 47 | +0.745 | -0.140 | 43 | +0.259 | +0.182 | 43 | +1.644 | +1.587 |
| 12h | calibrated | SFP_harden | record | ALL | short | 107 | -0.414 | -0.240 | 107 | +0.661 | +1.326 | 58 | -0.738 | -0.559 | 58 | +1.278 | +2.227 | 49 | -0.029 | +0.134 | 49 | +0.253 | +0.393 |
| 12h | calibrated | SFP_harden | record | EXP_ALIGNED* | both | 48 | +0.158 | +0.204 | 48 | +0.561 | +1.000 | 24 | +0.191 | +0.135 | 24 | +1.307 | +0.815 | 24 | +0.144 | +0.412 | 24 | -0.888 | +0.961 |
| 12h | calibrated | SFP_harden | record | EXP_ALIGNED* | long | 25 | +0.276 | +0.096 | 25 | +2.062 | +1.301 | 15 | +0.276 | +0.013 | 15 | +1.974 | +0.437 | 10 | +0.401 | +0.451 | 10 | +2.451 | +3.780 |
| 12h | calibrated | SFP_harden | record | EXP_ALIGNED* | short | 23 | -0.774 | -0.478 | 23 | -2.534 | -0.737 | 9 | -1.418 | -1.223 | 9 | -4.528 | -3.154 | 14 | +0.045 | +0.529 | 14 | -2.471 | -0.187 |
| 12h | calibrated | SFP_harden | record | EXP_COUNTER | both | 59 | +0.161 | +0.181 | 59 | +1.171 | +0.796 | 42 | -0.195 | -0.081 | 42 | +1.256 | +1.806 | 17 | +1.201 | +1.016 | 17 | +1.167 | -0.602 |
| 12h | calibrated | SFP_harden | record | EXP_COUNTER | long | 21 | +0.585 | +0.356 | 21 | +1.651 | -0.079 | 13 | +0.161 | +0.021 | 13 | +0.160 | -1.159 | 8 | +0.976 | +0.574 | 8 | +4.634 | +2.429 |
| 12h | calibrated | SFP_harden | record | EXP_COUNTER | short | 38 | -0.106 | +0.139 | 38 | +0.765 | +1.591 | 29 | -0.506 | -0.182 | 29 | +1.411 | +3.008 | 9 | +1.272 | +1.309 | 9 | -0.921 | -2.163 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | both | 28 | -0.252 | -0.208 | 28 | +0.206 | +0.251 | 17 | -0.430 | -0.386 | 17 | -0.887 | -0.843 | 11 | -0.065 | -0.020 | 11 | +0.953 | +0.998 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | long | 13 | -0.059 | -0.151 | 13 | -0.907 | -0.901 | 9 | -0.281 | -0.453 | 9 | -1.334 | -1.841 | 4 | +0.742 | +0.806 | 4 | -0.535 | +0.234 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | short | 15 | -0.956 | -0.775 | 15 | +2.006 | +2.089 | 8 | -1.950 | -1.691 | 8 | +0.580 | +1.174 | 7 | -0.687 | -0.661 | 7 | +6.476 | +5.798 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_MID* | both | 21 | -1.321 | -1.286 | 21 | -0.740 | -0.705 | 5 | -1.067 | -1.033 | 5 | +9.141 | +9.175 | 16 | -1.452 | -1.413 | 16 | -2.195 | -2.157 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_MID* | long | 8 | -0.904 | -0.274 | 8 | -2.195 | -0.286 | 1 | -1.030 | -0.209 | 1 | +18.005 | +20.945 | 7 | -0.740 | -0.420 | 7 | -2.827 | -1.815 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_MID* | short | 13 | -1.381 | -1.942 | 13 | +0.576 | -1.265 | 4 | -0.049 | -0.802 | 4 | +8.512 | +5.640 | 9 | -1.555 | -1.798 | 9 | -0.715 | -1.650 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_OTHER | both | 41 | -0.060 | -0.022 | 41 | +1.461 | +1.498 | 17 | -0.487 | -0.451 | 17 | +1.698 | +1.734 | 24 | +0.029 | +0.073 | 24 | +1.404 | +1.445 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_OTHER | long | 23 | -0.320 | -0.422 | 23 | +1.890 | +3.334 | 9 | -0.964 | -1.159 | 9 | +6.583 | +7.541 | 14 | -0.155 | -0.128 | 14 | +1.675 | +3.615 |
| 12h | calibrated | SFP_harden | record | IN_RANGE_OTHER | short | 18 | -0.021 | +0.157 | 18 | +1.328 | -0.041 | 8 | -0.263 | +0.005 | 8 | +1.391 | +0.506 | 10 | +0.224 | +0.285 | 10 | +1.328 | -0.530 |
| 12h | calibrated | SFP_harden | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | SFP_harden | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 12h | calibrated | SFP_harden | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | ALL | both | 71 | -0.063 | -0.039 | 67 | -0.738 | -0.714 | 42 | +0.017 | +0.038 | 42 | +1.843 | +1.864 | 29 | -0.248 | -0.219 | 25 | -1.455 | -1.427 |
| 1d | calibrated | BRK_tap89_first | record | ALL | long | 43 | +0.088 | +0.035 | 41 | -0.745 | -1.217 | 28 | +0.145 | +0.049 | 28 | +0.739 | -0.033 | 15 | -0.697 | -0.656 | 13 | -1.470 | -1.139 |
| 1d | calibrated | BRK_tap89_first | record | ALL | short | 28 | -0.154 | -0.052 | 26 | +1.496 | +2.015 | 14 | -0.428 | -0.290 | 14 | +3.504 | +4.319 | 14 | -0.148 | -0.132 | 12 | -1.232 | -1.509 |
| 1d | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | both | 20 | -0.870 | -0.881 | 20 | -1.709 | -1.368 | 13 | +0.445 | +0.441 | 13 | +2.679 | +2.880 | 7 | -1.424 | -1.452 | 7 | -1.962 | -1.100 |
| 1d | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | long | 7 | -0.933 | -0.874 | 7 | -1.955 | -0.369 | 2 | -0.559 | -1.061 | 2 | +6.298 | +4.396 | 5 | -0.941 | -0.662 | 5 | -1.962 | +0.923 |
| 1d | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | short | 13 | -0.806 | -0.841 | 13 | +0.319 | +0.477 | 11 | +0.440 | +0.484 | 11 | +2.673 | +3.062 | 2 | -2.749 | -3.159 | 2 | -2.763 | -3.715 |
| 1d | calibrated | BRK_tap89_first | record | EXP_COUNTER | both | 22 | +0.224 | +0.285 | 22 | +0.736 | +0.444 | 16 | +0.226 | +0.273 | 16 | +0.738 | +0.580 | 6 | -0.232 | -0.146 | 6 | +1.386 | +0.579 |
| 1d | calibrated | BRK_tap89_first | record | EXP_COUNTER | long | 19 | +0.225 | +0.315 | 19 | +0.447 | +0.344 | 16 | +0.226 | +0.237 | 16 | +0.738 | +0.404 | 3 | -0.677 | -0.230 | 3 | -1.440 | -0.451 |
| 1d | calibrated | BRK_tap89_first | record | EXP_COUNTER | short | 3 | +0.625 | +0.612 | 3 | +4.226 | +2.685 | 0 | — | — | 0 | — | — | 3 | +0.625 | +0.404 | 3 | +4.226 | +1.397 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | both | 12 | -0.115 | -0.094 | 11 | -1.177 | -1.157 | 4 | -0.422 | -0.401 | 4 | -3.205 | -3.185 | 8 | +0.196 | +0.217 | 7 | -1.173 | -1.151 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | long | 6 | -0.424 | -0.349 | 6 | -1.186 | -2.156 | 3 | -0.674 | +0.704 | 3 | -5.671 | +0.176 | 3 | +0.433 | +0.239 | 3 | +4.066 | +1.777 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | short | 6 | -0.049 | -0.083 | 5 | -1.176 | -0.164 | 1 | -0.056 | -1.394 | 1 | +5.398 | -0.409 | 5 | -0.042 | +0.196 | 4 | -1.840 | +0.492 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | both | 10 | -0.479 | -0.456 | 7 | -1.279 | -1.256 | 2 | -4.071 | -4.050 | 2 | +5.090 | +5.111 | 8 | -0.125 | -0.097 | 5 | -1.365 | -1.336 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | long | 4 | -0.941 | -0.938 | 2 | -3.590 | -2.403 | 0 | — | — | 0 | — | — | 4 | -0.941 | -1.660 | 2 | -3.590 | -5.434 |
| 1d | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | short | 6 | -0.479 | -0.437 | 5 | +3.856 | +2.714 | 2 | -4.071 | -4.518 | 2 | +5.090 | +3.201 | 4 | -0.125 | +0.651 | 3 | -1.279 | +0.622 |
| 1d | calibrated | BRK_tap89_first | record | NONE | both | 7 | +0.212 | +0.234 | 7 | +8.143 | +8.165 | 7 | +0.212 | +0.234 | 7 | +8.143 | +8.165 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | NONE | long | 7 | +0.212 | -0.636 | 7 | +8.143 | +3.388 | 7 | +0.212 | -0.636 | 7 | +8.143 | +3.388 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 64 | -0.056 | -0.032 | 60 | -0.771 | -0.747 | 37 | -0.059 | -0.037 | 37 | +0.450 | +0.471 | 27 | -0.052 | -0.024 | 23 | -1.455 | -1.427 |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 40 | +0.088 | +0.035 | 38 | -0.770 | -1.242 | 26 | +0.145 | +0.049 | 26 | -0.143 | -0.916 | 14 | -0.309 | -0.268 | 12 | -1.555 | -1.224 |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 24 | -0.154 | -0.052 | 22 | -0.432 | +0.087 | 11 | -0.800 | -0.662 | 11 | +2.679 | +3.494 | 13 | -0.050 | -0.034 | 11 | -1.184 | -1.460 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | both | 18 | -1.139 | -1.150 | 18 | -2.028 | -1.687 | 11 | -0.800 | -0.804 | 11 | -2.094 | -1.892 | 7 | -1.424 | -1.452 | 7 | -1.962 | -1.100 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | long | 7 | -0.933 | -0.874 | 7 | -1.955 | -0.369 | 2 | -0.559 | -1.061 | 2 | +6.298 | +4.396 | 5 | -0.941 | -0.662 | 5 | -1.962 | +0.923 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | short | 11 | -1.343 | -1.378 | 11 | -2.099 | -1.942 | 9 | -0.806 | -0.762 | 9 | -2.099 | -1.710 | 2 | -2.749 | -3.159 | 2 | -2.763 | -3.715 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | both | 21 | +0.224 | +0.285 | 21 | +0.445 | +0.153 | 15 | +0.225 | +0.273 | 15 | +0.447 | +0.288 | 6 | -0.232 | -0.146 | 6 | +1.386 | +0.579 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | long | 18 | +0.076 | +0.166 | 18 | -0.145 | -0.247 | 15 | +0.225 | +0.236 | 15 | +0.447 | +0.113 | 3 | -0.677 | -0.230 | 3 | -1.440 | -0.451 |
| 1d | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | short | 3 | +0.625 | +0.612 | 3 | +4.226 | +2.685 | 0 | — | — | 0 | — | — | 3 | +0.625 | +0.404 | 3 | +4.226 | +1.397 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | both | 11 | -0.059 | -0.038 | 10 | -0.959 | -0.938 | 4 | -0.422 | -0.401 | 4 | -3.205 | -3.185 | 7 | +0.432 | +0.454 | 6 | +1.446 | +1.468 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | long | 6 | -0.424 | -0.349 | 6 | -1.186 | -2.156 | 3 | -0.674 | +0.704 | 3 | -5.671 | +0.176 | 3 | +0.433 | +0.239 | 3 | +4.066 | +1.777 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | short | 5 | -0.042 | -0.075 | 4 | +2.111 | +3.122 | 1 | -0.056 | -1.394 | 1 | +5.398 | -0.409 | 4 | +0.810 | +1.048 | 3 | -1.176 | +1.157 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | both | 8 | -0.125 | -0.103 | 5 | -1.279 | -1.256 | 1 | -7.198 | -7.177 | 1 | +4.608 | +4.629 | 7 | -0.007 | +0.022 | 4 | -3.560 | -3.531 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | long | 3 | +0.085 | +0.089 | 1 | -5.833 | -4.646 | 0 | — | — | 0 | — | — | 3 | +0.085 | -0.634 | 1 | -5.833 | -7.676 |
| 1d | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | short | 5 | -0.244 | -0.202 | 4 | +1.289 | +0.147 | 1 | -7.198 | -7.646 | 1 | +4.608 | +2.718 | 4 | -0.125 | +0.651 | 3 | -1.279 | +0.622 |
| 1d | calibrated | BRK_tap89_oneshot | record | NONE | both | 6 | +0.321 | +0.343 | 6 | +4.963 | +4.985 | 6 | +0.321 | +0.343 | 6 | +4.963 | +4.985 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | NONE | long | 6 | +0.321 | -0.527 | 6 | +4.963 | +0.209 | 6 | +0.321 | -0.527 | 6 | +4.963 | +0.209 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap89_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | ALL | both | 60 | -0.069 | -0.045 | 59 | -0.043 | -0.019 | 37 | +0.299 | +0.321 | 37 | +0.364 | +0.385 | 23 | -0.560 | -0.531 | 22 | -2.075 | -2.048 |
| 1d | calibrated | BRK_tap127_first | record | ALL | long | 40 | -0.012 | -0.065 | 39 | -0.119 | -0.591 | 27 | +0.203 | +0.107 | 27 | -0.043 | -0.815 | 13 | -0.697 | -0.657 | 12 | -1.597 | -1.266 |
| 1d | calibrated | BRK_tap127_first | record | ALL | short | 20 | -0.068 | +0.033 | 20 | +1.387 | +1.905 | 10 | +0.516 | +0.655 | 10 | +3.409 | +4.225 | 10 | -0.326 | -0.310 | 10 | -2.849 | -3.126 |
| 1d | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | both | 17 | -1.280 | -1.291 | 17 | +0.594 | +0.935 | 11 | +0.729 | +0.725 | 11 | +2.748 | +2.949 | 6 | -3.207 | -3.236 | 6 | -2.231 | -1.368 |
| 1d | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | long | 6 | -2.040 | -1.980 | 6 | -2.087 | -0.501 | 2 | -0.954 | -1.456 | 2 | +5.704 | +3.802 | 4 | -2.371 | -2.093 | 4 | -2.096 | +0.789 |
| 1d | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | short | 11 | +0.299 | +0.264 | 11 | +2.446 | +2.604 | 9 | +0.729 | +0.773 | 9 | +2.748 | +3.137 | 2 | -4.977 | -5.388 | 2 | -3.598 | -4.550 |
| 1d | calibrated | BRK_tap127_first | record | EXP_COUNTER | both | 20 | +0.158 | +0.219 | 20 | -0.044 | -0.336 | 14 | +0.500 | +0.548 | 14 | -0.043 | -0.202 | 6 | -0.405 | -0.318 | 6 | +1.493 | +0.686 |
| 1d | calibrated | BRK_tap127_first | record | EXP_COUNTER | long | 17 | -0.117 | -0.027 | 17 | -0.123 | -0.225 | 14 | +0.500 | +0.512 | 14 | -0.043 | -0.377 | 3 | -0.677 | -0.230 | 3 | -1.535 | -0.546 |
| 1d | calibrated | BRK_tap127_first | record | EXP_COUNTER | short | 3 | +0.625 | +0.613 | 3 | +4.535 | +2.994 | 0 | — | — | 0 | — | — | 3 | +0.625 | +0.405 | 3 | +4.535 | +1.706 |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | both | 12 | -0.133 | -0.112 | 12 | -3.217 | -3.196 | 3 | -0.674 | -0.654 | 3 | -5.671 | -5.651 | 9 | -0.040 | -0.019 | 9 | -3.207 | -3.185 |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | long | 8 | -0.424 | -0.349 | 8 | -2.421 | -3.390 | 3 | -0.674 | +0.704 | 3 | -5.671 | +0.176 | 5 | +0.437 | +0.242 | 5 | -1.615 | -3.904 |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | short | 4 | -0.067 | -0.100 | 4 | -10.161 | -9.150 | 0 | — | — | 0 | — | — | 4 | -0.067 | +0.171 | 4 | -10.161 | -7.829 |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | both | 4 | -0.041 | -0.018 | 3 | +3.678 | +3.700 | 2 | -0.245 | -0.224 | 2 | +2.582 | +2.603 | 2 | -0.041 | -0.012 | 1 | +3.678 | +3.706 |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | long | 2 | +0.959 | +0.963 | 1 | -1.432 | -0.245 | 1 | +1.448 | +1.937 | 1 | -1.432 | +0.500 | 1 | +0.481 | -0.238 | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | short | 2 | -1.247 | -1.205 | 2 | +5.134 | +3.992 | 1 | -1.938 | -2.385 | 1 | +6.596 | +4.706 | 1 | -0.550 | +0.226 | 1 | +3.678 | +5.579 |
| 1d | calibrated | BRK_tap127_first | record | NONE | both | 7 | +0.214 | +0.236 | 7 | +1.785 | +1.807 | 7 | +0.214 | +0.236 | 7 | +1.785 | +1.807 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | NONE | long | 7 | +0.214 | -0.634 | 7 | +1.785 | -2.969 | 7 | +0.214 | -0.634 | 7 | +1.785 | -2.969 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 54 | -0.078 | -0.054 | 53 | +0.042 | +0.066 | 35 | +0.203 | +0.224 | 35 | +0.044 | +0.066 | 19 | -0.561 | -0.533 | 18 | -0.620 | -0.593 |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 38 | -0.012 | -0.065 | 37 | -0.119 | -0.591 | 26 | +0.148 | +0.052 | 26 | -0.079 | -0.851 | 12 | -0.410 | -0.370 | 11 | -1.555 | -1.224 |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 16 | -0.297 | -0.196 | 16 | +2.596 | +3.115 | 9 | +0.302 | +0.440 | 9 | +2.750 | +3.565 | 7 | -0.558 | -0.542 | 7 | +0.315 | +0.038 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | both | 16 | -2.033 | -2.045 | 16 | +0.459 | +0.801 | 10 | +0.514 | +0.510 | 10 | +2.598 | +2.799 | 6 | -3.207 | -3.236 | 6 | -2.231 | -1.368 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | long | 6 | -2.040 | -1.980 | 6 | -2.087 | -0.501 | 2 | -0.954 | -1.456 | 2 | +5.704 | +3.802 | 4 | -2.371 | -2.093 | 4 | -2.096 | +0.789 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | short | 10 | -1.327 | -1.362 | 10 | +1.385 | +1.542 | 8 | +0.514 | +0.558 | 8 | +2.598 | +2.987 | 2 | -4.977 | -5.388 | 2 | -3.598 | -4.550 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | both | 20 | +0.158 | +0.219 | 20 | -0.044 | -0.336 | 14 | +0.500 | +0.548 | 14 | -0.043 | -0.202 | 6 | -0.405 | -0.318 | 6 | +1.493 | +0.686 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | long | 17 | -0.117 | -0.027 | 17 | -0.123 | -0.225 | 14 | +0.500 | +0.512 | 14 | -0.043 | -0.377 | 3 | -0.677 | -0.230 | 3 | -1.535 | -0.546 |
| 1d | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | short | 3 | +0.625 | +0.613 | 3 | +4.535 | +2.994 | 0 | — | — | 0 | — | — | 3 | +0.625 | +0.405 | 3 | +4.535 | +1.706 |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | both | 8 | -0.110 | -0.089 | 8 | -2.068 | -2.048 | 3 | -0.674 | -0.654 | 3 | -5.671 | -5.651 | 5 | +0.433 | +0.455 | 5 | -1.619 | -1.597 |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | long | 7 | -0.174 | -0.099 | 7 | -1.629 | -2.598 | 3 | -0.674 | +0.704 | 3 | -5.671 | +0.176 | 4 | +0.472 | +0.277 | 4 | +2.341 | +0.052 |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | short | 1 | -0.033 | -0.066 | 1 | -2.495 | -1.483 | 0 | — | — | 0 | — | — | 1 | -0.033 | +0.205 | 1 | -2.495 | -0.162 |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | both | 4 | -0.041 | -0.018 | 3 | +3.678 | +3.700 | 2 | -0.245 | -0.224 | 2 | +2.582 | +2.603 | 2 | -0.041 | -0.012 | 1 | +3.678 | +3.706 |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | long | 2 | +0.959 | +0.963 | 1 | -1.432 | -0.245 | 1 | +1.448 | +1.937 | 1 | -1.432 | +0.500 | 1 | +0.481 | -0.238 | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | short | 2 | -1.247 | -1.205 | 2 | +5.134 | +3.992 | 1 | -1.938 | -2.385 | 1 | +6.596 | +4.706 | 1 | -0.550 | +0.226 | 1 | +3.678 | +5.579 |
| 1d | calibrated | BRK_tap127_oneshot | record | NONE | both | 6 | +0.159 | +0.181 | 6 | +5.225 | +5.248 | 6 | +0.159 | +0.181 | 6 | +5.225 | +5.248 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | NONE | long | 6 | +0.159 | -0.688 | 6 | +5.225 | +0.471 | 6 | +0.159 | -0.688 | 6 | +5.225 | +0.471 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap127_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | ALL | both | 51 | -0.238 | -0.215 | 51 | -1.631 | -1.607 | 29 | -0.176 | -0.155 | 29 | -0.049 | -0.028 | 22 | -0.625 | -0.597 | 22 | -4.462 | -4.434 |
| 1d | calibrated | BRK_tap200_first | record | ALL | long | 37 | -0.345 | -0.398 | 37 | -0.071 | -0.543 | 24 | -0.172 | -0.267 | 24 | +0.484 | -0.289 | 13 | -1.113 | -1.072 | 13 | -4.413 | -4.081 |
| 1d | calibrated | BRK_tap200_first | record | ALL | short | 14 | -0.078 | +0.024 | 14 | -4.259 | -3.740 | 5 | -1.222 | -1.083 | 5 | -0.192 | +0.624 | 9 | +0.088 | +0.104 | 9 | -7.160 | -7.437 |
| 1d | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | both | 11 | -0.942 | -0.953 | 11 | -2.057 | -1.716 | 7 | -0.122 | -0.126 | 7 | -0.172 | +0.030 | 4 | -1.033 | -1.062 | 4 | -5.430 | -4.568 |
| 1d | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | long | 5 | -0.937 | -0.877 | 5 | -2.672 | -1.086 | 2 | +1.989 | +1.487 | 2 | +3.712 | +1.810 | 3 | -1.117 | -0.839 | 3 | -4.764 | -1.879 |
| 1d | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | short | 6 | -0.682 | -0.717 | 6 | -1.132 | -0.974 | 5 | -1.222 | -1.178 | 5 | -0.192 | +0.198 | 1 | +0.651 | +0.240 | 1 | -8.813 | -9.765 |
| 1d | calibrated | BRK_tap200_first | record | EXP_COUNTER | both | 20 | -0.178 | -0.117 | 20 | -0.167 | -0.459 | 13 | -0.240 | -0.192 | 13 | -0.069 | -0.227 | 7 | -0.119 | -0.033 | 7 | -4.799 | -5.606 |
| 1d | calibrated | BRK_tap200_first | record | EXP_COUNTER | long | 17 | -1.548 | -1.458 | 17 | -0.072 | -0.175 | 13 | -0.240 | -0.229 | 13 | -0.069 | -0.403 | 4 | -2.173 | -1.726 | 4 | -4.600 | -3.612 |
| 1d | calibrated | BRK_tap200_first | record | EXP_COUNTER | short | 3 | +2.299 | +2.287 | 3 | -6.005 | -7.546 | 0 | — | — | 0 | — | — | 3 | +2.299 | +2.079 | 3 | -6.005 | -8.834 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | both | 11 | -0.093 | -0.072 | 11 | -4.403 | -4.382 | 2 | -0.057 | -0.037 | 2 | -3.898 | -3.877 | 9 | -0.093 | -0.071 | 9 | -4.403 | -4.381 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | long | 7 | -0.165 | -0.090 | 7 | -1.620 | -2.590 | 2 | -0.057 | +1.320 | 2 | -3.898 | +1.950 | 5 | -1.093 | -1.287 | 5 | -1.620 | -3.909 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | short | 4 | -0.067 | -0.100 | 4 | -10.161 | -9.150 | 0 | — | — | 0 | — | — | 4 | -0.067 | +0.171 | 4 | -10.161 | -7.829 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | both | 3 | -3.188 | -3.165 | 3 | -2.267 | -2.244 | 1 | -3.180 | -3.159 | 1 | -2.259 | -2.238 | 2 | -5.129 | -5.101 | 2 | -2.292 | -2.263 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | long | 2 | -1.741 | -1.738 | 2 | -2.218 | -1.031 | 1 | -3.180 | -2.691 | 1 | -2.259 | -0.327 | 1 | -0.297 | -1.016 | 1 | -2.171 | -4.015 |
| 1d | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | short | 1 | -9.962 | -9.921 | 1 | -2.412 | -3.554 | 0 | — | — | 0 | — | — | 1 | -9.962 | -9.186 | 1 | -2.412 | -0.511 |
| 1d | calibrated | BRK_tap200_first | record | NONE | both | 6 | -0.241 | -0.218 | 6 | +2.017 | +2.039 | 6 | -0.241 | -0.218 | 6 | +2.017 | +2.039 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | NONE | long | 6 | -0.241 | -1.088 | 6 | +2.017 | -2.737 | 6 | -0.241 | -1.088 | 6 | +2.017 | -2.737 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 41 | -0.309 | -0.285 | 41 | -0.183 | -0.160 | 26 | -0.209 | -0.187 | 26 | -0.060 | -0.038 | 15 | -0.954 | -0.926 | 15 | -2.426 | -2.398 |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 33 | -0.308 | -0.361 | 33 | -0.068 | -0.540 | 22 | -0.175 | -0.271 | 22 | +0.480 | -0.293 | 11 | -1.105 | -1.064 | 11 | -2.183 | -1.851 |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 8 | -0.683 | -0.582 | 8 | -2.251 | -1.733 | 4 | -2.014 | -1.875 | 4 | -1.132 | -0.316 | 4 | +1.114 | +1.130 | 4 | -2.478 | -2.754 |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | both | 8 | -1.165 | -1.176 | 8 | -2.373 | -2.032 | 5 | -1.211 | -1.215 | 5 | -2.060 | -1.859 | 3 | -1.117 | -1.146 | 3 | -4.764 | -3.901 |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | long | 4 | -1.026 | -0.967 | 4 | -3.717 | -2.131 | 1 | +0.022 | -0.480 | 1 | -2.670 | -4.572 | 3 | -1.117 | -0.839 | 3 | -4.764 | -1.879 |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | short | 4 | -2.014 | -2.049 | 4 | -1.132 | -0.974 | 4 | -2.014 | -1.970 | 4 | -1.132 | -0.742 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | both | 16 | -0.011 | +0.050 | 16 | +1.206 | +0.914 | 12 | -0.072 | -0.025 | 12 | +1.207 | +1.049 | 4 | +1.081 | +1.168 | 4 | +0.309 | -0.498 |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | long | 14 | -0.178 | -0.088 | 14 | +1.207 | +1.105 | 12 | -0.072 | -0.061 | 12 | +1.207 | +0.873 | 2 | -1.430 | -0.983 | 2 | +1.955 | +2.944 |
| 1d | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | short | 2 | +2.876 | +2.863 | 2 | +0.309 | -1.232 | 0 | — | — | 0 | — | — | 2 | +2.876 | +2.655 | 2 | +0.309 | -2.520 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | both | 8 | -0.102 | -0.081 | 8 | -2.060 | -2.039 | 2 | -0.057 | -0.037 | 2 | -3.898 | -3.877 | 6 | -0.565 | -0.544 | 6 | -2.060 | -2.038 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | long | 7 | -0.165 | -0.090 | 7 | -1.620 | -2.590 | 2 | -0.057 | +1.320 | 2 | -3.898 | +1.950 | 5 | -1.093 | -1.287 | 5 | -1.620 | -3.909 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | short | 1 | -0.033 | -0.066 | 1 | -2.495 | -1.483 | 0 | — | — | 0 | — | — | 1 | -0.033 | +0.205 | 1 | -2.495 | -0.162 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | both | 3 | -3.188 | -3.165 | 3 | -2.267 | -2.244 | 1 | -3.180 | -3.159 | 1 | -2.259 | -2.238 | 2 | -5.129 | -5.101 | 2 | -2.292 | -2.263 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | long | 2 | -1.741 | -1.738 | 2 | -2.218 | -1.031 | 1 | -3.180 | -2.691 | 1 | -2.259 | -0.327 | 1 | -0.297 | -1.016 | 1 | -2.171 | -4.015 |
| 1d | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | short | 1 | -9.962 | -9.921 | 1 | -2.412 | -3.554 | 0 | — | — | 0 | — | — | 1 | -9.962 | -9.186 | 1 | -2.412 | -0.511 |
| 1d | calibrated | BRK_tap200_oneshot | record | NONE | both | 6 | -0.241 | -0.218 | 6 | +2.017 | +2.039 | 6 | -0.241 | -0.218 | 6 | +2.017 | +2.039 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | NONE | long | 6 | -0.241 | -1.088 | 6 | +2.017 | -2.737 | 6 | -0.241 | -1.088 | 6 | +2.017 | -2.737 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_tap200_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | ALL | both | 56 | +0.352 | +0.376 | 53 | -1.357 | -1.333 | 31 | +0.264 | +0.285 | 31 | +0.464 | +0.486 | 25 | +0.396 | +0.424 | 22 | -3.437 | -3.410 |
| 1d | calibrated | BRK_mem_first | record | ALL | long | 29 | +0.922 | +0.869 | 28 | -0.143 | -0.615 | 19 | +1.171 | +1.075 | 19 | +1.126 | +0.353 | 10 | +0.044 | +0.085 | 9 | -2.190 | -1.859 |
| 1d | calibrated | BRK_mem_first | record | ALL | short | 27 | +0.345 | +0.447 | 25 | -3.337 | -2.818 | 12 | -0.196 | -0.058 | 12 | -1.570 | -0.755 | 15 | +0.683 | +0.699 | 13 | -4.315 | -4.592 |
| 1d | calibrated | BRK_mem_first | record | EXP_ALIGNED* | both | 17 | +0.262 | +0.251 | 17 | -3.339 | -2.998 | 9 | +0.145 | +0.141 | 9 | -3.159 | -2.957 | 8 | +0.565 | +0.536 | 8 | -5.878 | -5.016 |
| 1d | calibrated | BRK_mem_first | record | EXP_ALIGNED* | long | 3 | +1.168 | +1.228 | 3 | -5.018 | -3.432 | 1 | +1.176 | +0.674 | 1 | +24.964 | +23.062 | 2 | +0.420 | +0.698 | 2 | -6.167 | -3.282 |
| 1d | calibrated | BRK_mem_first | record | EXP_ALIGNED* | short | 14 | +0.205 | +0.170 | 14 | -3.248 | -3.091 | 8 | -0.141 | -0.097 | 8 | -3.246 | -2.857 | 6 | +0.583 | +0.172 | 6 | -4.757 | -5.709 |
| 1d | calibrated | BRK_mem_first | record | EXP_COUNTER | both | 16 | +0.870 | +0.931 | 15 | -0.069 | -0.361 | 11 | +1.392 | +1.439 | 11 | +0.451 | +0.293 | 5 | +0.353 | +0.440 | 4 | -2.393 | -3.199 |
| 1d | calibrated | BRK_mem_first | record | EXP_COUNTER | long | 13 | +1.392 | +1.482 | 13 | +0.451 | +0.349 | 11 | +1.392 | +1.403 | 11 | +0.451 | +0.117 | 2 | +0.770 | +1.217 | 2 | +1.544 | +2.532 |
| 1d | calibrated | BRK_mem_first | record | EXP_COUNTER | short | 3 | +0.353 | +0.341 | 2 | -6.874 | -8.414 | 0 | — | — | 0 | — | — | 3 | +0.353 | +0.132 | 2 | -6.874 | -9.702 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_MID* | both | 9 | +0.345 | +0.366 | 8 | -3.437 | -3.416 | 1 | -4.297 | -4.277 | 1 | -7.707 | -7.687 | 8 | +0.717 | +0.739 | 7 | -3.285 | -3.264 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_MID* | long | 4 | +0.065 | +0.140 | 4 | -3.614 | -4.584 | 1 | -4.297 | -2.920 | 1 | -7.707 | -1.860 | 3 | +0.295 | +0.100 | 3 | -2.876 | -5.165 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_MID* | short | 5 | +1.402 | +1.369 | 4 | -3.437 | -2.425 | 0 | — | — | 0 | — | — | 5 | +1.402 | +1.640 | 4 | -3.437 | -1.104 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | both | 7 | +0.024 | +0.047 | 6 | +2.587 | +2.610 | 3 | +0.038 | +0.059 | 3 | +3.537 | +3.558 | 4 | +0.179 | +0.208 | 3 | -2.170 | -2.141 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | long | 3 | -0.312 | -0.308 | 2 | +1.350 | +2.537 | 0 | — | — | 0 | — | — | 3 | -0.312 | -1.031 | 2 | +1.350 | -0.494 |
| 1d | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | short | 4 | +0.362 | +0.404 | 4 | +2.587 | +1.446 | 3 | +0.038 | -0.409 | 3 | +3.537 | +1.648 | 1 | +0.689 | +1.465 | 1 | -9.638 | -7.737 |
| 1d | calibrated | BRK_mem_first | record | NONE | both | 7 | +0.939 | +0.962 | 7 | +1.921 | +1.943 | 7 | +0.939 | +0.962 | 7 | +1.921 | +1.943 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | NONE | long | 6 | +2.199 | +1.351 | 6 | +5.725 | +0.971 | 6 | +2.199 | +1.351 | 6 | +5.725 | +0.971 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_first | record | NONE | short | 1 | -0.612 | +0.280 | 1 | -20.985 | -16.186 | 1 | -0.612 | +0.280 | 1 | -20.985 | -16.186 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 53 | +0.400 | +0.424 | 50 | -1.470 | -1.446 | 32 | +0.222 | +0.244 | 32 | +0.240 | +0.261 | 21 | +0.671 | +0.700 | 18 | -3.961 | -3.933 |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 29 | +0.290 | +0.236 | 28 | -0.347 | -0.818 | 20 | +1.049 | +0.954 | 20 | +0.791 | +0.018 | 9 | -0.187 | -0.146 | 8 | -2.543 | -2.212 |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 24 | +0.495 | +0.596 | 22 | -3.601 | -3.082 | 12 | -0.193 | -0.055 | 12 | -1.656 | -0.841 | 12 | +1.077 | +1.092 | 10 | -5.515 | -5.791 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | both | 16 | +0.494 | +0.483 | 16 | -4.313 | -3.971 | 10 | -0.143 | -0.147 | 10 | -1.659 | -1.458 | 6 | +0.963 | +0.934 | 6 | -7.019 | -6.157 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | long | 3 | +1.168 | +1.228 | 3 | -5.018 | -3.432 | 1 | +1.176 | +0.674 | 1 | +24.964 | +23.062 | 2 | +0.420 | +0.698 | 2 | -6.167 | -3.282 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | short | 13 | +0.404 | +0.369 | 13 | -3.615 | -3.458 | 9 | -0.428 | -0.384 | 9 | -3.334 | -2.945 | 4 | +1.180 | +0.770 | 4 | -7.222 | -8.174 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | both | 16 | +0.318 | +0.380 | 15 | -0.206 | -0.498 | 12 | +0.841 | +0.888 | 12 | +0.188 | +0.030 | 4 | +0.047 | +0.134 | 3 | -4.316 | -5.122 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | long | 13 | +0.290 | +0.380 | 13 | -0.075 | -0.177 | 12 | +0.841 | +0.852 | 12 | +0.188 | -0.146 | 1 | -1.723 | -1.276 | 1 | -0.463 | +0.525 |
| 1d | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | short | 3 | +0.353 | +0.341 | 2 | -6.874 | -8.414 | 0 | — | — | 0 | — | — | 3 | +0.353 | +0.132 | 2 | -6.874 | -9.702 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | both | 8 | +0.692 | +0.713 | 7 | -3.283 | -3.262 | 1 | -4.297 | -4.277 | 1 | -7.707 | -7.687 | 7 | +1.091 | +1.113 | 6 | -3.079 | -3.058 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | long | 4 | +0.065 | +0.140 | 4 | -3.614 | -4.584 | 1 | -4.297 | -2.920 | 1 | -7.707 | -1.860 | 3 | +0.295 | +0.100 | 3 | -2.876 | -5.165 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | short | 4 | +1.452 | +1.418 | 3 | -3.283 | -2.271 | 0 | — | — | 0 | — | — | 4 | +1.452 | +1.690 | 3 | -3.283 | -0.950 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | both | 6 | +0.347 | +0.370 | 5 | +1.637 | +1.659 | 2 | +4.079 | +4.100 | 2 | +2.895 | +2.916 | 4 | +0.179 | +0.208 | 3 | -2.170 | -2.141 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | long | 3 | -0.312 | -0.308 | 2 | +1.350 | +2.537 | 0 | — | — | 0 | — | — | 3 | -0.312 | -1.031 | 2 | +1.350 | -0.494 |
| 1d | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | short | 3 | +0.687 | +0.728 | 3 | +1.638 | +0.496 | 2 | +4.079 | +3.632 | 2 | +2.895 | +1.005 | 1 | +0.689 | +1.465 | 1 | -9.638 | -7.737 |
| 1d | calibrated | BRK_mem_oneshot | record | NONE | both | 7 | +0.939 | +0.962 | 7 | +1.921 | +1.943 | 7 | +0.939 | +0.962 | 7 | +1.921 | +1.943 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | NONE | long | 6 | +2.199 | +1.351 | 6 | +5.725 | +0.971 | 6 | +2.199 | +1.351 | 6 | +5.725 | +0.971 | 0 | — | — | 0 | — | — |
| 1d | calibrated | BRK_mem_oneshot | record | NONE | short | 1 | -0.612 | +0.280 | 1 | -20.985 | -16.186 | 1 | -0.612 | +0.280 | 1 | -20.985 | -16.186 | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | ALL | both | 77 | -0.781 | -0.757 | 73 | +0.999 | +1.023 | 40 | -0.789 | -0.768 | 40 | +1.600 | +1.622 | 37 | -0.783 | -0.754 | 33 | -0.112 | -0.084 |
| 1d | calibrated | SFP_harden | record | ALL | long | 46 | -0.280 | -0.333 | 45 | -0.104 | -0.576 | 23 | -0.268 | -0.364 | 23 | +1.568 | +0.795 | 23 | -0.504 | -0.463 | 22 | -3.037 | -2.706 |
| 1d | calibrated | SFP_harden | record | ALL | short | 31 | -1.509 | -1.408 | 28 | +3.035 | +3.553 | 17 | -1.850 | -1.712 | 17 | +2.393 | +3.208 | 14 | -1.397 | -1.381 | 11 | +3.800 | +3.523 |
| 1d | calibrated | SFP_harden | record | EXP_ALIGNED* | both | 18 | -0.796 | -0.807 | 18 | -3.923 | -3.582 | 9 | -0.807 | -0.811 | 9 | +3.165 | +3.366 | 9 | -0.508 | -0.537 | 9 | -5.667 | -4.805 |
| 1d | calibrated | SFP_harden | record | EXP_ALIGNED* | long | 9 | -0.508 | -0.448 | 9 | -5.667 | -4.081 | 0 | — | — | 0 | — | — | 9 | -0.508 | -0.229 | 9 | -5.667 | -2.782 |
| 1d | calibrated | SFP_harden | record | EXP_ALIGNED* | short | 9 | -0.807 | -0.842 | 9 | +3.165 | +3.322 | 9 | -0.807 | -0.763 | 9 | +3.165 | +3.554 | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | EXP_COUNTER | both | 29 | -0.254 | -0.193 | 29 | +1.471 | +1.179 | 14 | -0.280 | -0.233 | 14 | +1.173 | +1.015 | 15 | -0.072 | +0.014 | 15 | +1.466 | +0.659 |
| 1d | calibrated | SFP_harden | record | EXP_COUNTER | long | 25 | -0.268 | -0.178 | 25 | +1.006 | +0.903 | 14 | -0.280 | -0.269 | 14 | +1.173 | +0.839 | 11 | -0.126 | +0.321 | 11 | +1.010 | +1.998 |
| 1d | calibrated | SFP_harden | record | EXP_COUNTER | short | 4 | +0.817 | +0.805 | 4 | +4.554 | +3.013 | 0 | — | — | 0 | — | — | 4 | +0.817 | +0.596 | 4 | +4.554 | +1.725 |
| 1d | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | both | 1 | +3.244 | +3.275 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | +3.244 | +3.275 | 0 | — | — |
| 1d | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | long | 1 | +3.244 | +3.294 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | +3.244 | +3.294 | 0 | — | — |
| 1d | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | IN_RANGE_MID* | both | 8 | -1.474 | -1.453 | 6 | +1.246 | +1.267 | 2 | -1.843 | -1.823 | 2 | +1.258 | +1.278 | 6 | -1.474 | -1.453 | 4 | -1.809 | -1.787 |
| 1d | calibrated | SFP_harden | record | IN_RANGE_MID* | long | 4 | -1.223 | -1.148 | 4 | +1.248 | +0.278 | 2 | -1.843 | -0.466 | 2 | +1.258 | +7.105 | 2 | -1.223 | -1.417 | 2 | +1.316 | -0.973 |
| 1d | calibrated | SFP_harden | record | IN_RANGE_MID* | short | 4 | -1.501 | -1.534 | 2 | -55.873 | -54.861 | 0 | — | — | 0 | — | — | 4 | -1.501 | -1.263 | 2 | -55.873 | -53.541 |
| 1d | calibrated | SFP_harden | record | IN_RANGE_OTHER | both | 7 | -1.505 | -1.482 | 6 | +3.976 | +3.999 | 1 | +0.575 | +0.596 | 1 | +5.686 | +5.707 | 6 | -2.277 | -2.249 | 5 | +3.849 | +3.878 |
| 1d | calibrated | SFP_harden | record | IN_RANGE_OTHER | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | IN_RANGE_OTHER | short | 7 | -1.505 | -1.463 | 6 | +3.976 | +2.834 | 1 | +0.575 | +0.127 | 1 | +5.686 | +3.797 | 6 | -2.277 | -1.501 | 5 | +3.849 | +5.750 |
| 1d | calibrated | SFP_harden | record | NONE | both | 14 | -1.041 | -1.019 | 14 | -1.072 | -1.050 | 14 | -1.041 | -1.019 | 14 | -1.072 | -1.050 | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | NONE | long | 7 | -0.157 | -1.005 | 7 | +1.572 | -3.182 | 7 | -0.157 | -1.005 | 7 | +1.572 | -3.182 | 0 | — | — | 0 | — | — |
| 1d | calibrated | SFP_harden | record | NONE | short | 7 | -4.339 | -3.447 | 7 | -34.137 | -29.339 | 7 | -4.339 | -3.447 | 7 | -34.137 | -29.339 | 0 | — | — | 0 | — | — |

## 5 · POOLED:UNSEEN12 · calibrated · cell law record (whole; 4h / 1d have no L+1 in the commission: cells ALL + NA)

| lens | scale | event | law | L+1 cell | dir | n ALL H20 | NET ALL H20 | Δcell ALL H20 | n ALL H100 | NET ALL H100 | Δcell ALL H100 | n tuning H20 | NET tuning H20 | Δcell tuning H20 | n tuning H100 | NET tuning H100 | Δcell tuning H100 | n holdout H20 | NET holdout H20 | Δcell holdout H20 | n holdout H100 | NET holdout H100 | Δcell holdout H100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1h | calibrated | BRK_tap89_first | record | ALL | both | 2687 | -0.120 | -0.007 | 2680 | -0.156 | -0.042 | 1314 | +0.003 | +0.104 | 1314 | -0.121 | -0.020 | 1373 | -0.282 | -0.136 | 1366 | -0.211 | -0.065 |
| 1h | calibrated | BRK_tap89_first | record | ALL | long | 1368 | -0.115 | -0.006 | 1361 | -0.344 | -0.149 | 691 | +0.089 | +0.136 | 691 | -0.161 | -0.127 | 677 | -0.385 | -0.194 | 670 | -0.653 | -0.270 |
| 1h | calibrated | BRK_tap89_first | record | ALL | short | 1319 | -0.126 | -0.007 | 1319 | +0.097 | +0.129 | 623 | -0.073 | +0.081 | 623 | -0.002 | +0.166 | 696 | -0.169 | -0.068 | 696 | +0.208 | +0.117 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | both | 958 | -0.070 | +0.089 | 951 | -0.356 | -0.002 | 489 | +0.097 | +0.214 | 489 | -0.338 | -0.183 | 469 | -0.262 | -0.028 | 462 | -0.401 | +0.184 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | long | 506 | -0.096 | +0.077 | 499 | -0.562 | -0.085 | 287 | +0.154 | +0.254 | 287 | -0.335 | -0.217 | 219 | -0.486 | -0.186 | 212 | -0.855 | +0.031 |
| 1h | calibrated | BRK_tap89_first | record | EXP_ALIGNED* | short | 452 | +0.012 | +0.160 | 452 | -0.211 | +0.027 | 202 | +0.045 | +0.187 | 202 | -0.351 | -0.161 | 250 | -0.043 | +0.125 | 250 | -0.059 | +0.234 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | both | 519 | -0.153 | -0.119 | 519 | +0.041 | -0.119 | 236 | -0.285 | -0.203 | 236 | -0.411 | -0.366 | 283 | -0.145 | -0.134 | 283 | +0.593 | +0.253 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | long | 262 | -0.177 | -0.124 | 262 | -0.428 | -0.465 | 112 | -0.152 | -0.094 | 112 | -1.196 | -1.186 | 150 | -0.197 | -0.134 | 150 | +0.186 | +0.123 |
| 1h | calibrated | BRK_tap89_first | record | EXP_COUNTER | short | 257 | -0.131 | -0.114 | 257 | +0.622 | +0.334 | 124 | -0.421 | -0.321 | 124 | +0.118 | +0.200 | 133 | -0.076 | -0.120 | 133 | +0.955 | +0.326 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | both | 3 | -1.164 | -1.022 | 3 | -1.448 | -1.306 | 1 | -1.187 | -1.049 | 1 | -1.471 | -1.332 | 2 | -1.801 | -1.645 | 2 | -5.874 | -5.718 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_COINCIDENT* | short | 3 | -1.164 | -0.960 | 3 | -1.448 | -1.282 | 1 | -1.187 | -0.827 | 1 | -1.471 | -0.780 | 2 | -1.801 | -1.753 | 2 | -5.874 | -6.229 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | both | 853 | -0.168 | -0.027 | 853 | -0.200 | -0.059 | 399 | -0.021 | +0.097 | 399 | +0.108 | +0.226 | 454 | -0.361 | -0.192 | 454 | -0.586 | -0.417 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | long | 442 | -0.143 | -0.014 | 442 | -0.307 | -0.151 | 206 | +0.051 | +0.128 | 206 | +0.287 | +0.265 | 236 | -0.551 | -0.362 | 236 | -1.063 | -0.704 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_MID* | short | 411 | -0.168 | -0.015 | 411 | -0.135 | -0.007 | 193 | -0.134 | +0.024 | 193 | +0.036 | +0.293 | 218 | -0.255 | -0.106 | 218 | -0.199 | -0.220 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | both | 348 | -0.091 | +0.031 | 348 | +0.248 | +0.370 | 185 | +0.029 | +0.133 | 185 | +0.120 | +0.224 | 163 | -0.256 | -0.106 | 163 | +0.296 | +0.446 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | long | 152 | -0.034 | +0.057 | 152 | +0.058 | +0.263 | 82 | +0.176 | +0.215 | 82 | +0.078 | +0.287 | 70 | -0.118 | +0.045 | 70 | +0.205 | +0.411 |
| 1h | calibrated | BRK_tap89_first | record | IN_RANGE_OTHER | short | 196 | -0.218 | -0.066 | 196 | +0.259 | +0.297 | 103 | -0.089 | +0.080 | 103 | +0.226 | +0.224 | 93 | -0.319 | -0.183 | 93 | +0.295 | +0.388 |
| 1h | calibrated | BRK_tap89_first | record | NONE | both | 6 | +1.266 | +1.446 | 6 | +6.617 | +6.797 | 4 | +4.819 | +4.999 | 4 | +14.890 | +15.070 | 2 | -1.767 | -1.714 | 2 | -2.094 | -2.041 |
| 1h | calibrated | BRK_tap89_first | record | NONE | long | 6 | +1.266 | +1.603 | 6 | +6.617 | +8.520 | 4 | +4.819 | +5.152 | 4 | +14.890 | +16.880 | 2 | -1.767 | -1.548 | 2 | -2.094 | -0.653 |
| 1h | calibrated | BRK_tap89_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 2325 | -0.115 | -0.001 | 2318 | -0.183 | -0.070 | 1147 | +0.009 | +0.110 | 1147 | -0.156 | -0.055 | 1178 | -0.282 | -0.136 | 1171 | -0.236 | -0.090 |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 1206 | -0.112 | -0.003 | 1199 | -0.423 | -0.228 | 613 | +0.096 | +0.144 | 613 | -0.232 | -0.199 | 593 | -0.379 | -0.188 | 586 | -0.676 | -0.292 |
| 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 1119 | -0.114 | +0.004 | 1119 | +0.108 | +0.139 | 534 | -0.056 | +0.098 | 534 | +0.040 | +0.208 | 585 | -0.169 | -0.068 | 585 | +0.163 | +0.072 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | both | 858 | -0.100 | +0.059 | 851 | -0.360 | -0.005 | 444 | +0.056 | +0.174 | 444 | -0.352 | -0.197 | 414 | -0.227 | +0.007 | 407 | -0.393 | +0.192 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | long | 470 | -0.121 | +0.051 | 463 | -0.650 | -0.173 | 269 | +0.081 | +0.181 | 269 | -0.486 | -0.367 | 201 | -0.611 | -0.311 | 194 | -1.008 | -0.122 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_ALIGNED* | short | 388 | +0.009 | +0.157 | 388 | -0.168 | +0.070 | 175 | +0.019 | +0.161 | 175 | -0.340 | -0.150 | 213 | -0.016 | +0.151 | 213 | +0.017 | +0.310 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | both | 448 | -0.162 | -0.127 | 448 | -0.002 | -0.162 | 204 | -0.139 | -0.057 | 204 | -0.424 | -0.380 | 244 | -0.225 | -0.213 | 244 | +0.352 | +0.012 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | long | 226 | -0.164 | -0.111 | 226 | -0.637 | -0.674 | 95 | -0.067 | -0.009 | 95 | -1.126 | -1.117 | 131 | -0.255 | -0.193 | 131 | +0.037 | -0.027 |
| 1h | calibrated | BRK_tap89_oneshot | record | EXP_COUNTER | short | 222 | -0.198 | -0.180 | 222 | +0.617 | +0.330 | 109 | -0.390 | -0.290 | 109 | +0.040 | +0.121 | 113 | -0.182 | -0.225 | 113 | +0.670 | +0.042 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | both | 3 | -1.164 | -1.022 | 3 | -1.448 | -1.306 | 1 | -1.187 | -1.049 | 1 | -1.471 | -1.332 | 2 | -1.801 | -1.645 | 2 | -5.874 | -5.718 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_COINCIDENT* | short | 3 | -1.164 | -0.960 | 3 | -1.448 | -1.282 | 1 | -1.187 | -0.827 | 1 | -1.471 | -0.780 | 2 | -1.801 | -1.753 | 2 | -5.874 | -6.229 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | both | 704 | -0.089 | +0.053 | 704 | -0.191 | -0.049 | 331 | +0.035 | +0.153 | 331 | +0.263 | +0.380 | 373 | -0.316 | -0.147 | 373 | -0.534 | -0.365 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | long | 370 | -0.082 | +0.047 | 370 | -0.308 | -0.152 | 173 | +0.096 | +0.173 | 173 | +0.311 | +0.289 | 197 | -0.441 | -0.251 | 197 | -0.913 | -0.554 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_MID* | short | 334 | -0.111 | +0.043 | 334 | +0.012 | +0.140 | 158 | -0.001 | +0.158 | 158 | +0.204 | +0.461 | 176 | -0.182 | -0.034 | 176 | -0.298 | -0.320 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | both | 307 | -0.103 | +0.018 | 307 | +0.196 | +0.317 | 164 | -0.051 | +0.053 | 164 | +0.095 | +0.199 | 143 | -0.259 | -0.110 | 143 | +0.300 | +0.449 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | long | 135 | -0.022 | +0.069 | 135 | -0.121 | +0.084 | 73 | +0.083 | +0.121 | 73 | -0.098 | +0.111 | 62 | -0.061 | +0.103 | 62 | -0.090 | +0.117 |
| 1h | calibrated | BRK_tap89_oneshot | record | IN_RANGE_OTHER | short | 172 | -0.237 | -0.085 | 172 | +0.349 | +0.387 | 91 | -0.092 | +0.077 | 91 | +0.226 | +0.224 | 81 | -0.317 | -0.181 | 81 | +0.590 | +0.683 |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | both | 5 | -0.547 | -0.367 | 5 | -0.290 | -0.110 | 3 | +6.558 | +6.738 | 3 | +16.256 | +16.436 | 2 | -1.767 | -1.714 | 2 | -2.094 | -2.041 |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | long | 5 | -0.547 | -0.210 | 5 | -0.290 | +1.613 | 3 | +6.558 | +6.891 | 3 | +16.256 | +18.246 | 2 | -1.767 | -1.548 | 2 | -2.094 | -0.653 |
| 1h | calibrated | BRK_tap89_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | ALL | both | 2390 | -0.155 | -0.042 | 2384 | -0.182 | -0.068 | 1176 | -0.083 | +0.017 | 1176 | -0.167 | -0.066 | 1214 | -0.217 | -0.071 | 1208 | -0.225 | -0.079 |
| 1h | calibrated | BRK_tap127_first | record | ALL | long | 1235 | -0.080 | +0.029 | 1229 | -0.300 | -0.105 | 631 | +0.084 | +0.132 | 631 | -0.077 | -0.044 | 604 | -0.338 | -0.147 | 598 | -0.545 | -0.162 |
| 1h | calibrated | BRK_tap127_first | record | ALL | short | 1155 | -0.210 | -0.092 | 1155 | -0.044 | -0.012 | 545 | -0.285 | -0.131 | 545 | -0.183 | -0.015 | 610 | -0.124 | -0.023 | 610 | +0.172 | +0.081 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | both | 800 | -0.057 | +0.102 | 794 | -0.418 | -0.064 | 416 | +0.140 | +0.258 | 416 | -0.310 | -0.155 | 384 | -0.226 | +0.008 | 378 | -0.547 | +0.039 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | long | 433 | +0.096 | +0.268 | 427 | -0.406 | +0.071 | 247 | +0.291 | +0.391 | 247 | +0.059 | +0.178 | 186 | -0.243 | +0.058 | 180 | -0.740 | +0.147 |
| 1h | calibrated | BRK_tap127_first | record | EXP_ALIGNED* | short | 367 | -0.214 | -0.065 | 367 | -0.459 | -0.221 | 169 | -0.243 | -0.100 | 169 | -0.558 | -0.367 | 198 | -0.164 | +0.004 | 198 | -0.068 | +0.226 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | both | 463 | -0.074 | -0.039 | 463 | +0.085 | -0.075 | 209 | -0.149 | -0.067 | 209 | -0.290 | -0.246 | 254 | -0.022 | -0.011 | 254 | +0.763 | +0.423 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | long | 237 | -0.045 | +0.008 | 237 | -0.186 | -0.222 | 102 | -0.210 | -0.153 | 102 | -1.085 | -1.076 | 135 | +0.116 | +0.179 | 135 | +0.463 | +0.400 |
| 1h | calibrated | BRK_tap127_first | record | EXP_COUNTER | short | 226 | -0.080 | -0.063 | 226 | +0.518 | +0.230 | 107 | -0.062 | +0.038 | 107 | +0.046 | +0.127 | 119 | -0.164 | -0.208 | 119 | +1.103 | +0.474 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | both | 3 | -0.788 | -0.645 | 3 | -0.353 | -0.210 | 1 | -0.828 | -0.689 | 1 | -0.393 | -0.255 | 2 | -1.137 | -0.981 | 2 | -6.069 | -5.913 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_COINCIDENT* | short | 3 | -0.788 | -0.583 | 3 | -0.353 | -0.187 | 1 | -0.828 | -0.468 | 1 | -0.393 | +0.298 | 2 | -1.137 | -1.089 | 2 | -6.069 | -6.424 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | both | 848 | -0.235 | -0.093 | 848 | -0.156 | -0.015 | 393 | -0.224 | -0.107 | 393 | +0.097 | +0.214 | 455 | -0.225 | -0.057 | 455 | -0.399 | -0.230 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | long | 443 | -0.211 | -0.081 | 443 | -0.254 | -0.099 | 211 | +0.003 | +0.079 | 211 | +0.438 | +0.416 | 232 | -0.555 | -0.366 | 232 | -0.962 | -0.603 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_MID* | short | 405 | -0.241 | -0.088 | 405 | -0.097 | +0.030 | 182 | -0.515 | -0.356 | 182 | -0.043 | +0.214 | 223 | -0.078 | +0.070 | 223 | -0.177 | -0.198 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | both | 273 | -0.214 | -0.093 | 273 | -0.129 | -0.008 | 156 | -0.016 | +0.088 | 156 | -0.342 | -0.238 | 117 | -0.409 | -0.259 | 117 | +0.123 | +0.272 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | long | 120 | -0.220 | -0.129 | 120 | -0.818 | -0.614 | 71 | +0.182 | +0.221 | 71 | -0.813 | -0.603 | 49 | -1.186 | -1.023 | 49 | -0.180 | +0.027 |
| 1h | calibrated | BRK_tap127_first | record | IN_RANGE_OTHER | short | 153 | -0.208 | -0.056 | 153 | +0.115 | +0.153 | 85 | -0.129 | +0.040 | 85 | -0.138 | -0.140 | 68 | -0.245 | -0.110 | 68 | +0.240 | +0.333 |
| 1h | calibrated | BRK_tap127_first | record | NONE | both | 3 | -0.405 | -0.225 | 3 | -0.246 | -0.066 | 1 | -0.405 | -0.225 | 1 | +3.858 | +4.038 | 2 | -1.373 | -1.321 | 2 | -3.099 | -3.046 |
| 1h | calibrated | BRK_tap127_first | record | NONE | long | 2 | -1.373 | -1.037 | 2 | -3.099 | -1.196 | 0 | — | — | 0 | — | — | 2 | -1.373 | -1.154 | 2 | -3.099 | -1.657 |
| 1h | calibrated | BRK_tap127_first | record | NONE | short | 1 | -0.405 | -0.382 | 1 | +3.858 | +2.315 | 1 | -0.405 | -0.378 | 1 | +3.858 | +2.228 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 2103 | -0.123 | -0.009 | 2097 | -0.192 | -0.079 | 1044 | -0.034 | +0.067 | 1044 | -0.172 | -0.071 | 1059 | -0.216 | -0.070 | 1053 | -0.272 | -0.125 |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 1095 | -0.071 | +0.038 | 1089 | -0.300 | -0.105 | 559 | +0.145 | +0.193 | 559 | -0.038 | -0.004 | 536 | -0.366 | -0.175 | 530 | -0.590 | -0.206 |
| 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 1008 | -0.162 | -0.044 | 1008 | -0.127 | -0.095 | 485 | -0.227 | -0.073 | 485 | -0.297 | -0.130 | 523 | -0.118 | -0.017 | 523 | +0.126 | +0.035 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | both | 723 | -0.028 | +0.131 | 717 | -0.500 | -0.145 | 386 | +0.160 | +0.277 | 386 | -0.497 | -0.341 | 337 | -0.157 | +0.077 | 331 | -0.533 | +0.052 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | long | 397 | +0.100 | +0.273 | 391 | -0.529 | -0.052 | 228 | +0.321 | +0.421 | 228 | +0.001 | +0.119 | 169 | -0.191 | +0.110 | 163 | -0.757 | +0.129 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_ALIGNED* | short | 326 | -0.175 | -0.027 | 326 | -0.500 | -0.262 | 158 | -0.225 | -0.082 | 158 | -0.678 | -0.488 | 168 | -0.119 | +0.048 | 168 | +0.037 | +0.331 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | both | 405 | -0.077 | -0.043 | 405 | +0.088 | -0.072 | 186 | -0.171 | -0.088 | 186 | -0.323 | -0.278 | 219 | -0.037 | -0.026 | 219 | +0.700 | +0.360 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | long | 211 | -0.089 | -0.036 | 211 | -0.255 | -0.291 | 91 | -0.224 | -0.166 | 91 | -1.068 | -1.058 | 120 | +0.055 | +0.118 | 120 | +0.346 | +0.283 |
| 1h | calibrated | BRK_tap127_oneshot | record | EXP_COUNTER | short | 194 | -0.078 | -0.061 | 194 | +0.611 | +0.324 | 95 | -0.079 | +0.021 | 95 | -0.084 | -0.002 | 99 | -0.084 | -0.128 | 99 | +1.122 | +0.494 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | both | 3 | -0.788 | -0.645 | 3 | -0.353 | -0.210 | 1 | -0.828 | -0.689 | 1 | -0.393 | -0.255 | 2 | -1.137 | -0.981 | 2 | -6.069 | -5.913 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_COINCIDENT* | short | 3 | -0.788 | -0.583 | 3 | -0.353 | -0.187 | 1 | -0.828 | -0.468 | 1 | -0.393 | +0.298 | 2 | -1.137 | -1.089 | 2 | -6.069 | -6.424 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | both | 728 | -0.185 | -0.044 | 728 | -0.180 | -0.039 | 334 | -0.104 | +0.013 | 334 | +0.104 | +0.221 | 394 | -0.249 | -0.081 | 394 | -0.426 | -0.257 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | long | 378 | -0.203 | -0.073 | 378 | -0.263 | -0.107 | 180 | +0.087 | +0.163 | 180 | +0.391 | +0.369 | 198 | -0.707 | -0.518 | 198 | -0.905 | -0.546 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_MID* | short | 350 | -0.176 | -0.022 | 350 | -0.158 | -0.030 | 154 | -0.265 | -0.106 | 154 | -0.046 | +0.211 | 196 | -0.095 | +0.053 | 196 | -0.224 | -0.245 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | both | 241 | -0.202 | -0.081 | 241 | -0.129 | -0.008 | 136 | +0.045 | +0.149 | 136 | -0.137 | -0.033 | 105 | -0.553 | -0.404 | 105 | -0.170 | -0.020 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | long | 107 | -0.077 | +0.013 | 107 | -0.127 | +0.077 | 60 | +0.285 | +0.323 | 60 | -0.089 | +0.121 | 47 | -1.174 | -1.011 | 47 | -0.168 | +0.039 |
| 1h | calibrated | BRK_tap127_oneshot | record | IN_RANGE_OTHER | short | 134 | -0.246 | -0.094 | 134 | -0.161 | -0.123 | 76 | -0.196 | -0.027 | 76 | -0.177 | -0.179 | 58 | -0.265 | -0.129 | 58 | -0.061 | +0.031 |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | both | 3 | -0.405 | -0.225 | 3 | -0.246 | -0.066 | 1 | -0.405 | -0.225 | 1 | +3.858 | +4.038 | 2 | -1.373 | -1.321 | 2 | -3.099 | -3.046 |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | long | 2 | -1.373 | -1.037 | 2 | -3.099 | -1.196 | 0 | — | — | 0 | — | — | 2 | -1.373 | -1.154 | 2 | -3.099 | -1.657 |
| 1h | calibrated | BRK_tap127_oneshot | record | NONE | short | 1 | -0.405 | -0.382 | 1 | +3.858 | +2.315 | 1 | -0.405 | -0.378 | 1 | +3.858 | +2.228 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | ALL | both | 1998 | -0.106 | +0.008 | 1997 | -0.079 | +0.035 | 976 | -0.061 | +0.040 | 976 | +0.084 | +0.185 | 1022 | -0.189 | -0.042 | 1021 | -0.271 | -0.125 |
| 1h | calibrated | BRK_tap200_first | record | ALL | long | 1053 | -0.250 | -0.141 | 1052 | -0.337 | -0.142 | 521 | -0.070 | -0.023 | 521 | +0.162 | +0.196 | 532 | -0.480 | -0.289 | 531 | -0.767 | -0.383 |
| 1h | calibrated | BRK_tap200_first | record | ALL | short | 945 | +0.058 | +0.176 | 945 | +0.161 | +0.193 | 455 | +0.005 | +0.159 | 455 | -0.134 | +0.034 | 490 | +0.060 | +0.161 | 490 | +0.345 | +0.254 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | both | 563 | -0.234 | -0.075 | 562 | +0.029 | +0.383 | 291 | -0.073 | +0.045 | 291 | +0.193 | +0.348 | 272 | -0.414 | -0.180 | 271 | -0.090 | +0.496 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | long | 321 | -0.331 | -0.159 | 320 | -0.085 | +0.393 | 176 | -0.118 | -0.018 | 176 | +0.384 | +0.503 | 145 | -0.606 | -0.305 | 144 | -0.563 | +0.323 |
| 1h | calibrated | BRK_tap200_first | record | EXP_ALIGNED* | short | 242 | +0.017 | +0.165 | 242 | +0.162 | +0.399 | 115 | +0.128 | +0.271 | 115 | -0.773 | -0.583 | 127 | -0.087 | +0.080 | 127 | +0.387 | +0.680 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | both | 426 | -0.310 | -0.275 | 426 | -0.138 | -0.298 | 188 | -0.409 | -0.326 | 188 | -0.209 | -0.164 | 238 | -0.163 | -0.152 | 238 | +0.032 | -0.309 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | long | 222 | -0.502 | -0.449 | 222 | -0.466 | -0.503 | 89 | -0.529 | -0.472 | 89 | -0.367 | -0.357 | 133 | -0.440 | -0.377 | 133 | -0.542 | -0.605 |
| 1h | calibrated | BRK_tap200_first | record | EXP_COUNTER | short | 204 | +0.013 | +0.030 | 204 | +0.396 | +0.108 | 99 | -0.232 | -0.132 | 99 | +0.012 | +0.093 | 105 | +0.061 | +0.018 | 105 | +0.711 | +0.082 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | both | 4 | +0.606 | +0.749 | 4 | +1.040 | +1.183 | 3 | +1.001 | +1.140 | 3 | +1.638 | +1.776 | 1 | +0.064 | +0.220 | 1 | +0.444 | +0.600 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | long | 3 | +0.214 | +0.295 | 3 | +1.638 | +1.757 | 2 | +0.608 | +0.524 | 2 | +2.218 | +1.804 | 1 | +0.064 | +0.328 | 1 | +0.444 | +1.111 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_COINCIDENT* | short | 1 | +1.414 | +1.619 | 1 | -2.439 | -2.273 | 1 | +1.414 | +1.774 | 1 | -2.439 | -1.749 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | both | 797 | -0.094 | +0.047 | 797 | -0.034 | +0.108 | 375 | -0.075 | +0.042 | 375 | +0.225 | +0.342 | 422 | -0.129 | +0.039 | 422 | -0.485 | -0.316 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | long | 413 | -0.173 | -0.043 | 413 | -0.351 | -0.196 | 199 | +0.031 | +0.107 | 199 | +0.231 | +0.209 | 214 | -0.499 | -0.309 | 214 | -1.111 | -0.752 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_MID* | short | 384 | +0.083 | +0.237 | 384 | +0.124 | +0.252 | 176 | -0.168 | -0.009 | 176 | +0.100 | +0.357 | 208 | +0.323 | +0.472 | 208 | +0.109 | +0.087 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | both | 208 | +0.172 | +0.294 | 208 | -0.609 | -0.488 | 119 | +0.393 | +0.497 | 119 | -1.030 | -0.926 | 89 | -0.044 | +0.106 | 89 | -0.175 | -0.025 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | long | 94 | +0.074 | +0.164 | 94 | -0.724 | -0.520 | 55 | +0.166 | +0.204 | 55 | -1.478 | -1.268 | 39 | -0.063 | +0.100 | 39 | -0.218 | -0.012 |
| 1h | calibrated | BRK_tap200_first | record | IN_RANGE_OTHER | short | 114 | +0.210 | +0.362 | 114 | -0.401 | -0.363 | 64 | +0.473 | +0.642 | 64 | -0.557 | -0.559 | 50 | -0.095 | +0.041 | 50 | +0.043 | +0.136 |
| 1h | calibrated | BRK_tap200_first | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 1739 | -0.070 | +0.044 | 1738 | -0.034 | +0.080 | 851 | +0.015 | +0.116 | 851 | +0.083 | +0.184 | 888 | -0.166 | -0.020 | 887 | -0.204 | -0.057 |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 934 | -0.184 | -0.075 | 933 | -0.344 | -0.149 | 460 | -0.030 | +0.018 | 460 | +0.172 | +0.206 | 474 | -0.460 | -0.269 | 473 | -0.736 | -0.352 |
| 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 805 | +0.155 | +0.273 | 805 | +0.239 | +0.271 | 391 | +0.066 | +0.219 | 391 | -0.050 | +0.118 | 414 | +0.167 | +0.269 | 414 | +0.571 | +0.481 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | both | 509 | -0.152 | +0.007 | 508 | +0.140 | +0.494 | 264 | -0.049 | +0.068 | 264 | +0.357 | +0.512 | 245 | -0.387 | -0.153 | 244 | -0.053 | +0.532 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | long | 296 | -0.318 | -0.146 | 295 | -0.238 | +0.239 | 163 | -0.121 | -0.021 | 163 | +0.366 | +0.485 | 133 | -0.532 | -0.232 | 132 | -0.558 | +0.328 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_ALIGNED* | short | 213 | +0.064 | +0.212 | 213 | +0.397 | +0.635 | 101 | +0.196 | +0.339 | 101 | -0.054 | +0.136 | 112 | -0.047 | +0.120 | 112 | +0.720 | +1.014 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | both | 367 | -0.235 | -0.200 | 367 | -0.159 | -0.319 | 167 | -0.246 | -0.164 | 167 | -0.156 | -0.111 | 200 | -0.179 | -0.167 | 200 | -0.204 | -0.545 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | long | 201 | -0.546 | -0.493 | 201 | -0.507 | -0.544 | 82 | -0.522 | -0.464 | 82 | -0.279 | -0.269 | 119 | -0.681 | -0.618 | 119 | -0.805 | -0.868 |
| 1h | calibrated | BRK_tap200_oneshot | record | EXP_COUNTER | short | 166 | +0.219 | +0.237 | 166 | +0.543 | +0.256 | 85 | +0.184 | +0.284 | 85 | +0.009 | +0.091 | 81 | +0.684 | +0.641 | 81 | +1.334 | +0.705 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | both | 4 | +0.606 | +0.749 | 4 | +1.040 | +1.183 | 3 | +1.001 | +1.140 | 3 | +1.638 | +1.776 | 1 | +0.064 | +0.220 | 1 | +0.444 | +0.600 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | long | 3 | +0.214 | +0.295 | 3 | +1.638 | +1.757 | 2 | +0.608 | +0.524 | 2 | +2.218 | +1.804 | 1 | +0.064 | +0.328 | 1 | +0.444 | +1.111 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_COINCIDENT* | short | 1 | +1.414 | +1.619 | 1 | -2.439 | -2.273 | 1 | +1.414 | +1.774 | 1 | -2.439 | -1.749 | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | both | 672 | -0.060 | +0.082 | 672 | -0.021 | +0.120 | 307 | -0.018 | +0.100 | 307 | +0.216 | +0.333 | 365 | -0.104 | +0.065 | 365 | -0.387 | -0.219 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | long | 344 | -0.140 | -0.010 | 344 | -0.170 | -0.015 | 162 | +0.108 | +0.185 | 162 | +0.232 | +0.210 | 182 | -0.400 | -0.211 | 182 | -0.916 | -0.557 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_MID* | short | 328 | +0.078 | +0.231 | 328 | +0.100 | +0.228 | 145 | -0.130 | +0.028 | 145 | +0.107 | +0.364 | 183 | +0.193 | +0.341 | 183 | +0.075 | +0.053 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | both | 187 | +0.200 | +0.321 | 187 | -0.875 | -0.754 | 110 | +0.357 | +0.460 | 110 | -1.220 | -1.116 | 77 | -0.018 | +0.131 | 77 | +0.253 | +0.402 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | long | 90 | +0.104 | +0.195 | 90 | -0.724 | -0.520 | 51 | +0.347 | +0.386 | 51 | -1.464 | -1.255 | 39 | -0.063 | +0.100 | 39 | -0.218 | -0.012 |
| 1h | calibrated | BRK_tap200_oneshot | record | IN_RANGE_OTHER | short | 97 | +0.215 | +0.367 | 97 | -1.011 | -0.973 | 59 | +0.455 | +0.624 | 59 | -1.122 | -1.124 | 38 | +0.013 | +0.149 | 38 | +1.473 | +1.565 |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | both | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_tap200_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_first | record | ALL | both | 2086 | -0.186 | -0.072 | 2081 | -0.498 | -0.385 | 1045 | -0.042 | +0.059 | 1045 | -0.317 | -0.216 | 1041 | -0.327 | -0.181 | 1036 | -0.683 | -0.536 |
| 1h | calibrated | BRK_mem_first | record | ALL | long | 1116 | -0.062 | +0.047 | 1111 | -0.521 | -0.326 | 586 | +0.063 | +0.110 | 586 | -0.176 | -0.143 | 530 | -0.272 | -0.081 | 525 | -1.041 | -0.657 |
| 1h | calibrated | BRK_mem_first | record | ALL | short | 970 | -0.281 | -0.163 | 970 | -0.469 | -0.437 | 459 | -0.226 | -0.072 | 459 | -0.618 | -0.450 | 511 | -0.353 | -0.252 | 511 | -0.435 | -0.526 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | both | 612 | -0.174 | -0.015 | 607 | -0.636 | -0.281 | 331 | -0.140 | -0.023 | 331 | -0.487 | -0.332 | 281 | -0.227 | +0.007 | 276 | -0.968 | -0.382 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | long | 343 | -0.158 | +0.014 | 338 | -0.662 | -0.185 | 206 | -0.154 | -0.054 | 206 | -0.431 | -0.312 | 137 | -0.228 | +0.073 | 132 | -1.331 | -0.445 |
| 1h | calibrated | BRK_mem_first | record | EXP_ALIGNED* | short | 269 | -0.186 | -0.037 | 269 | -0.641 | -0.403 | 125 | +0.001 | +0.143 | 125 | -1.033 | -0.843 | 144 | -0.221 | -0.054 | 144 | -0.622 | -0.328 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | both | 417 | -0.396 | -0.361 | 417 | -0.231 | -0.391 | 180 | -0.388 | -0.305 | 180 | -1.212 | -1.167 | 237 | -0.369 | -0.357 | 237 | +0.430 | +0.090 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | long | 206 | +0.032 | +0.085 | 206 | -0.930 | -0.967 | 87 | +0.012 | +0.070 | 87 | -1.587 | -1.578 | 119 | +0.054 | +0.116 | 119 | +0.664 | +0.600 |
| 1h | calibrated | BRK_mem_first | record | EXP_COUNTER | short | 211 | -0.651 | -0.633 | 211 | +0.029 | -0.259 | 93 | -0.859 | -0.759 | 93 | -0.658 | -0.576 | 118 | -0.537 | -0.581 | 118 | +0.367 | -0.262 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | both | 31 | -0.283 | -0.140 | 31 | -0.113 | +0.030 | 20 | +0.103 | +0.241 | 20 | -0.656 | -0.518 | 11 | -0.728 | -0.573 | 11 | +0.366 | +0.522 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | long | 20 | -0.375 | -0.295 | 20 | +0.023 | +0.142 | 14 | +1.825 | +1.742 | 14 | +0.023 | -0.391 | 6 | -0.919 | -0.655 | 6 | -0.305 | +0.362 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_COINCIDENT* | short | 11 | -0.302 | -0.097 | 11 | -0.665 | -0.499 | 6 | -1.154 | -0.794 | 6 | -1.544 | -0.853 | 5 | +0.443 | +0.491 | 5 | +0.366 | +0.010 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | both | 571 | -0.050 | +0.091 | 571 | -0.491 | -0.350 | 279 | +0.049 | +0.166 | 279 | -0.146 | -0.028 | 292 | -0.365 | -0.196 | 292 | -0.759 | -0.591 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | long | 326 | +0.000 | +0.130 | 326 | -0.297 | -0.141 | 158 | +0.105 | +0.181 | 158 | +0.208 | +0.186 | 168 | -0.318 | -0.129 | 168 | -0.933 | -0.574 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_MID* | short | 245 | -0.109 | +0.045 | 245 | -0.580 | -0.452 | 121 | -0.016 | +0.143 | 121 | -0.846 | -0.589 | 124 | -0.414 | -0.266 | 124 | -0.577 | -0.599 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | both | 451 | -0.189 | -0.067 | 451 | -0.524 | -0.403 | 232 | +0.057 | +0.161 | 232 | +0.191 | +0.294 | 219 | -0.393 | -0.243 | 219 | -1.471 | -1.322 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | long | 217 | -0.025 | +0.066 | 217 | -0.541 | -0.336 | 118 | +0.435 | +0.474 | 118 | +0.194 | +0.403 | 99 | -0.589 | -0.426 | 99 | -1.877 | -1.670 |
| 1h | calibrated | BRK_mem_first | record | IN_RANGE_OTHER | short | 234 | -0.233 | -0.081 | 234 | -0.575 | -0.537 | 114 | -0.175 | -0.006 | 114 | +0.082 | +0.080 | 120 | -0.239 | -0.103 | 120 | -0.998 | -0.905 |
| 1h | calibrated | BRK_mem_first | record | NONE | both | 4 | +0.602 | +0.782 | 4 | +1.767 | +1.947 | 3 | +0.980 | +1.160 | 3 | +6.330 | +6.510 | 1 | +0.288 | +0.341 | 1 | -2.732 | -2.679 |
| 1h | calibrated | BRK_mem_first | record | NONE | long | 4 | +0.602 | +0.939 | 4 | +1.767 | +3.670 | 3 | +0.980 | +1.313 | 3 | +6.330 | +8.319 | 1 | +0.288 | +0.508 | 1 | -2.732 | -1.290 |
| 1h | calibrated | BRK_mem_first | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 1901 | -0.147 | -0.034 | 1897 | -0.461 | -0.347 | 951 | -0.012 | +0.088 | 951 | -0.274 | -0.173 | 950 | -0.336 | -0.189 | 946 | -0.687 | -0.541 |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 1012 | -0.069 | +0.040 | 1008 | -0.550 | -0.355 | 529 | +0.115 | +0.163 | 529 | -0.191 | -0.157 | 483 | -0.336 | -0.145 | 479 | -1.141 | -0.757 |
| 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 889 | -0.258 | -0.140 | 889 | -0.353 | -0.321 | 422 | -0.177 | -0.024 | 422 | -0.612 | -0.444 | 467 | -0.333 | -0.232 | 467 | -0.092 | -0.183 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | both | 612 | -0.136 | +0.023 | 608 | -0.459 | -0.104 | 323 | -0.103 | +0.015 | 323 | -0.414 | -0.259 | 289 | -0.226 | +0.008 | 285 | -0.607 | -0.021 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | long | 341 | -0.156 | +0.017 | 337 | -0.461 | +0.017 | 200 | -0.110 | -0.010 | 200 | -0.261 | -0.143 | 141 | -0.421 | -0.121 | 137 | -1.285 | -0.399 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_ALIGNED* | short | 271 | -0.073 | +0.076 | 271 | -0.429 | -0.191 | 123 | +0.029 | +0.172 | 123 | -1.033 | -0.843 | 148 | -0.180 | -0.012 | 148 | -0.038 | +0.256 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | both | 379 | -0.280 | -0.245 | 379 | -0.612 | -0.772 | 170 | -0.280 | -0.197 | 170 | -1.434 | -1.389 | 209 | -0.334 | -0.323 | 209 | -0.014 | -0.354 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | long | 184 | +0.081 | +0.134 | 184 | -1.260 | -1.297 | 74 | +0.108 | +0.166 | 74 | -1.935 | -1.925 | 110 | +0.062 | +0.125 | 110 | -0.604 | -0.667 |
| 1h | calibrated | BRK_mem_oneshot | record | EXP_COUNTER | short | 195 | -0.552 | -0.535 | 195 | -0.361 | -0.649 | 96 | -0.481 | -0.381 | 96 | -0.704 | -0.623 | 99 | -0.793 | -0.836 | 99 | +0.191 | -0.438 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | both | 33 | -0.041 | +0.101 | 33 | -0.113 | +0.030 | 21 | +0.076 | +0.214 | 21 | -0.104 | +0.034 | 12 | -0.607 | -0.451 | 12 | -0.204 | -0.048 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | long | 19 | -0.033 | +0.048 | 19 | -0.104 | +0.015 | 14 | +1.825 | +1.742 | 14 | +0.023 | -0.391 | 5 | -1.077 | -0.813 | 5 | -3.437 | -2.770 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_COINCIDENT* | short | 14 | -0.127 | +0.078 | 14 | -0.158 | +0.008 | 7 | -0.289 | +0.071 | 7 | -1.246 | -0.555 | 7 | +0.159 | +0.206 | 7 | +0.303 | -0.053 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | both | 502 | -0.027 | +0.115 | 502 | -0.325 | -0.183 | 241 | +0.105 | +0.223 | 241 | -0.021 | +0.097 | 261 | -0.374 | -0.205 | 261 | -0.878 | -0.709 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | long | 289 | +0.028 | +0.158 | 289 | -0.540 | -0.384 | 140 | +0.191 | +0.267 | 140 | +0.034 | +0.012 | 149 | -0.377 | -0.188 | 149 | -1.137 | -0.778 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_MID* | short | 213 | -0.110 | +0.043 | 213 | -0.167 | -0.039 | 101 | -0.018 | +0.141 | 101 | -0.145 | +0.111 | 112 | -0.349 | -0.201 | 112 | -0.055 | -0.076 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | both | 371 | -0.256 | -0.135 | 371 | -0.613 | -0.492 | 193 | -0.080 | +0.024 | 193 | -0.098 | +0.006 | 178 | -0.496 | -0.347 | 178 | -1.081 | -0.932 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | long | 175 | -0.181 | -0.091 | 175 | -0.540 | -0.336 | 98 | +0.217 | +0.256 | 98 | +0.164 | +0.373 | 77 | -0.590 | -0.427 | 77 | -1.785 | -1.579 |
| 1h | calibrated | BRK_mem_oneshot | record | IN_RANGE_OTHER | short | 196 | -0.324 | -0.172 | 196 | -0.666 | -0.628 | 95 | -0.220 | -0.051 | 95 | -0.629 | -0.631 | 101 | -0.382 | -0.246 | 101 | -0.674 | -0.581 |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | both | 4 | +0.602 | +0.782 | 4 | +1.767 | +1.947 | 3 | +0.980 | +1.160 | 3 | +6.330 | +6.510 | 1 | +0.288 | +0.341 | 1 | -2.732 | -2.679 |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | long | 4 | +0.602 | +0.939 | 4 | +1.767 | +3.670 | 3 | +0.980 | +1.313 | 3 | +6.330 | +8.319 | 1 | +0.288 | +0.508 | 1 | -2.732 | -1.290 |
| 1h | calibrated | BRK_mem_oneshot | record | NONE | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | ALL | both | 4386 | +0.025 | +0.139 | 4370 | -0.060 | +0.054 | 2142 | +0.118 | +0.219 | 2142 | -0.082 | +0.018 | 2244 | -0.051 | +0.095 | 2228 | -0.062 | +0.084 |
| 1h | calibrated | SFP_harden | record | ALL | long | 2175 | -0.027 | +0.082 | 2172 | -0.220 | -0.025 | 1038 | +0.217 | +0.265 | 1038 | +0.064 | +0.098 | 1137 | -0.242 | -0.051 | 1134 | -0.461 | -0.077 |
| 1h | calibrated | SFP_harden | record | ALL | short | 2211 | +0.068 | +0.186 | 2198 | +0.086 | +0.118 | 1104 | -0.019 | +0.135 | 1104 | -0.260 | -0.092 | 1107 | +0.069 | +0.170 | 1094 | +0.297 | +0.207 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | both | 1137 | +0.125 | +0.284 | 1134 | +0.035 | +0.390 | 528 | +0.262 | +0.379 | 528 | +0.020 | +0.175 | 609 | -0.041 | +0.193 | 606 | +0.020 | +0.605 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | long | 595 | -0.010 | +0.162 | 593 | -0.170 | +0.307 | 311 | +0.228 | +0.328 | 311 | +0.128 | +0.247 | 284 | -0.366 | -0.065 | 282 | -0.688 | +0.199 |
| 1h | calibrated | SFP_harden | record | EXP_ALIGNED* | short | 542 | +0.251 | +0.399 | 541 | +0.278 | +0.516 | 217 | +0.332 | +0.475 | 217 | +0.002 | +0.192 | 325 | +0.159 | +0.326 | 324 | +0.538 | +0.832 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | both | 975 | -0.013 | +0.022 | 970 | +0.526 | +0.365 | 483 | -0.064 | +0.019 | 483 | +0.551 | +0.596 | 492 | +0.043 | +0.054 | 487 | +0.328 | -0.012 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | long | 491 | -0.163 | -0.110 | 491 | +0.405 | +0.369 | 222 | -0.022 | +0.036 | 222 | +0.492 | +0.502 | 269 | -0.250 | -0.188 | 269 | +0.247 | +0.184 |
| 1h | calibrated | SFP_harden | record | EXP_COUNTER | short | 484 | +0.051 | +0.069 | 479 | +0.588 | +0.301 | 261 | -0.146 | -0.046 | 261 | +0.807 | +0.889 | 223 | +0.245 | +0.202 | 218 | +0.454 | -0.175 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | both | 227 | -0.059 | +0.084 | 226 | -0.588 | -0.445 | 115 | -0.179 | -0.040 | 115 | -1.141 | -1.002 | 112 | -0.036 | +0.119 | 111 | +0.140 | +0.295 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | long | 100 | +0.080 | +0.161 | 100 | -0.809 | -0.690 | 38 | +0.530 | +0.446 | 38 | -0.881 | -1.295 | 62 | -0.041 | +0.222 | 62 | -0.730 | -0.063 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_COINCIDENT* | short | 127 | -0.254 | -0.049 | 126 | -0.430 | -0.264 | 77 | -0.444 | -0.084 | 77 | -1.351 | -0.661 | 50 | +0.212 | +0.259 | 49 | +0.914 | +0.558 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | both | 957 | -0.003 | +0.139 | 956 | -0.409 | -0.267 | 430 | +0.130 | +0.248 | 430 | -0.496 | -0.379 | 527 | -0.074 | +0.095 | 526 | -0.303 | -0.134 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | long | 436 | +0.010 | +0.140 | 435 | -0.372 | -0.216 | 194 | +0.358 | +0.434 | 194 | -0.391 | -0.413 | 242 | -0.154 | +0.036 | 241 | -0.401 | -0.042 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_MID* | short | 521 | -0.020 | +0.133 | 521 | -0.461 | -0.333 | 236 | -0.012 | +0.147 | 236 | -0.697 | -0.440 | 285 | -0.042 | +0.106 | 285 | -0.304 | -0.326 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | both | 1074 | -0.047 | +0.074 | 1068 | -0.332 | -0.211 | 570 | +0.088 | +0.192 | 570 | -0.251 | -0.148 | 504 | -0.194 | -0.044 | 498 | -0.409 | -0.260 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | long | 548 | -0.134 | -0.043 | 548 | -0.535 | -0.330 | 268 | +0.219 | +0.258 | 268 | -0.078 | +0.132 | 280 | -0.385 | -0.222 | 280 | -0.905 | -0.698 |
| 1h | calibrated | SFP_harden | record | IN_RANGE_OTHER | short | 526 | +0.016 | +0.168 | 520 | -0.091 | -0.053 | 302 | -0.138 | +0.031 | 302 | -0.415 | -0.418 | 224 | +0.052 | +0.188 | 218 | +0.188 | +0.281 |
| 1h | calibrated | SFP_harden | record | NONE | both | 16 | +0.181 | +0.361 | 16 | +0.755 | +0.935 | 16 | +0.181 | +0.361 | 16 | +0.755 | +0.935 | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | NONE | long | 5 | +0.600 | +0.937 | 5 | +0.116 | +2.019 | 5 | +0.600 | +0.933 | 5 | +0.116 | +2.106 | 0 | — | — | 0 | — | — |
| 1h | calibrated | SFP_harden | record | NONE | short | 11 | -0.239 | -0.216 | 11 | +1.399 | -0.144 | 11 | -0.239 | -0.213 | 11 | +1.399 | -0.231 | 0 | — | — | 0 | — | — |
| 4h | calibrated | BRK_tap89_first | record | ALL | both | 619 | +0.052 | +0.106 | 611 | +0.457 | +0.511 | 320 | +0.038 | +0.086 | 320 | +0.633 | +0.681 | 299 | +0.048 | +0.118 | 291 | +0.061 | +0.131 |
| 4h | calibrated | BRK_tap89_first | record | ALL | long | 339 | +0.200 | +0.278 | 333 | -0.016 | +0.222 | 187 | +0.431 | +0.437 | 187 | +0.623 | +0.656 | 152 | -0.146 | +0.022 | 146 | -0.712 | -0.222 |
| 4h | calibrated | BRK_tap89_first | record | ALL | short | 280 | -0.082 | -0.052 | 278 | +0.617 | +0.486 | 133 | -0.636 | -0.547 | 133 | +0.642 | +0.705 | 147 | +0.291 | +0.263 | 145 | +0.496 | +0.146 |
| 4h | calibrated | BRK_tap89_first | record | NA | both | 619 | +0.052 | +0.106 | 611 | +0.457 | +0.511 | 320 | +0.038 | +0.086 | 320 | +0.633 | +0.681 | 299 | +0.048 | +0.118 | 291 | +0.061 | +0.131 |
| 4h | calibrated | BRK_tap89_first | record | NA | long | 339 | +0.200 | +0.278 | 333 | -0.016 | +0.222 | 187 | +0.431 | +0.437 | 187 | +0.623 | +0.656 | 152 | -0.146 | +0.022 | 146 | -0.712 | -0.222 |
| 4h | calibrated | BRK_tap89_first | record | NA | short | 280 | -0.082 | -0.052 | 278 | +0.617 | +0.486 | 133 | -0.636 | -0.547 | 133 | +0.642 | +0.705 | 147 | +0.291 | +0.263 | 145 | +0.496 | +0.146 |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 524 | -0.006 | +0.048 | 516 | +0.308 | +0.362 | 278 | -0.016 | +0.032 | 278 | +0.501 | +0.549 | 246 | +0.003 | +0.072 | 238 | -0.145 | -0.075 |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 294 | +0.198 | +0.276 | 288 | -0.193 | +0.045 | 161 | +0.383 | +0.390 | 161 | +0.497 | +0.530 | 133 | -0.185 | -0.017 | 127 | -0.703 | -0.213 |
| 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 230 | -0.207 | -0.177 | 228 | +0.669 | +0.538 | 117 | -0.639 | -0.550 | 117 | +0.639 | +0.702 | 113 | +0.232 | +0.204 | 111 | +0.820 | +0.470 |
| 4h | calibrated | BRK_tap89_oneshot | record | NA | both | 524 | -0.006 | +0.048 | 516 | +0.308 | +0.362 | 278 | -0.016 | +0.032 | 278 | +0.501 | +0.549 | 246 | +0.003 | +0.072 | 238 | -0.145 | -0.075 |
| 4h | calibrated | BRK_tap89_oneshot | record | NA | long | 294 | +0.198 | +0.276 | 288 | -0.193 | +0.045 | 161 | +0.383 | +0.390 | 161 | +0.497 | +0.530 | 133 | -0.185 | -0.017 | 127 | -0.703 | -0.213 |
| 4h | calibrated | BRK_tap89_oneshot | record | NA | short | 230 | -0.207 | -0.177 | 228 | +0.669 | +0.538 | 117 | -0.639 | -0.550 | 117 | +0.639 | +0.702 | 113 | +0.232 | +0.204 | 111 | +0.820 | +0.470 |
| 4h | calibrated | BRK_tap127_first | record | ALL | both | 535 | -0.109 | -0.055 | 528 | +0.536 | +0.590 | 275 | +0.117 | +0.165 | 275 | +0.797 | +0.845 | 260 | -0.291 | -0.221 | 253 | -0.022 | +0.048 |
| 4h | calibrated | BRK_tap127_first | record | ALL | long | 301 | -0.037 | +0.041 | 296 | +0.206 | +0.445 | 165 | +0.431 | +0.437 | 165 | +0.838 | +0.871 | 136 | -0.417 | -0.249 | 131 | -0.969 | -0.479 |
| 4h | calibrated | BRK_tap127_first | record | ALL | short | 234 | -0.157 | -0.127 | 232 | +0.943 | +0.812 | 110 | -0.187 | -0.098 | 110 | +0.722 | +0.785 | 124 | -0.049 | -0.078 | 122 | +1.066 | +0.716 |
| 4h | calibrated | BRK_tap127_first | record | NA | both | 535 | -0.109 | -0.055 | 528 | +0.536 | +0.590 | 275 | +0.117 | +0.165 | 275 | +0.797 | +0.845 | 260 | -0.291 | -0.221 | 253 | -0.022 | +0.048 |
| 4h | calibrated | BRK_tap127_first | record | NA | long | 301 | -0.037 | +0.041 | 296 | +0.206 | +0.445 | 165 | +0.431 | +0.437 | 165 | +0.838 | +0.871 | 136 | -0.417 | -0.249 | 131 | -0.969 | -0.479 |
| 4h | calibrated | BRK_tap127_first | record | NA | short | 234 | -0.157 | -0.127 | 232 | +0.943 | +0.812 | 110 | -0.187 | -0.098 | 110 | +0.722 | +0.785 | 124 | -0.049 | -0.078 | 122 | +1.066 | +0.716 |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 465 | -0.043 | +0.011 | 458 | +0.513 | +0.568 | 243 | +0.101 | +0.148 | 243 | +0.677 | +0.725 | 222 | -0.181 | -0.111 | 215 | +0.061 | +0.131 |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 268 | +0.009 | +0.088 | 263 | +0.393 | +0.632 | 148 | +0.518 | +0.525 | 148 | +0.990 | +1.023 | 120 | -0.290 | -0.122 | 115 | -0.901 | -0.411 |
| 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 197 | -0.167 | -0.137 | 195 | +0.695 | +0.565 | 95 | -0.242 | -0.153 | 95 | +0.409 | +0.471 | 102 | +0.313 | +0.285 | 100 | +1.066 | +0.716 |
| 4h | calibrated | BRK_tap127_oneshot | record | NA | both | 465 | -0.043 | +0.011 | 458 | +0.513 | +0.568 | 243 | +0.101 | +0.148 | 243 | +0.677 | +0.725 | 222 | -0.181 | -0.111 | 215 | +0.061 | +0.131 |
| 4h | calibrated | BRK_tap127_oneshot | record | NA | long | 268 | +0.009 | +0.088 | 263 | +0.393 | +0.632 | 148 | +0.518 | +0.525 | 148 | +0.990 | +1.023 | 120 | -0.290 | -0.122 | 115 | -0.901 | -0.411 |
| 4h | calibrated | BRK_tap127_oneshot | record | NA | short | 197 | -0.167 | -0.137 | 195 | +0.695 | +0.565 | 95 | -0.242 | -0.153 | 95 | +0.409 | +0.471 | 102 | +0.313 | +0.285 | 100 | +1.066 | +0.716 |
| 4h | calibrated | BRK_tap200_first | record | ALL | both | 452 | +0.194 | +0.248 | 444 | +0.209 | +0.263 | 241 | +0.292 | +0.339 | 241 | +0.676 | +0.724 | 211 | +0.085 | +0.155 | 203 | -0.275 | -0.205 |
| 4h | calibrated | BRK_tap200_first | record | ALL | long | 262 | +0.240 | +0.318 | 256 | +0.165 | +0.403 | 147 | +0.521 | +0.527 | 147 | +0.947 | +0.979 | 115 | -0.100 | +0.068 | 109 | -1.317 | -0.827 |
| 4h | calibrated | BRK_tap200_first | record | ALL | short | 190 | +0.127 | +0.157 | 188 | +0.421 | +0.290 | 94 | -0.102 | -0.013 | 94 | +0.208 | +0.271 | 96 | +0.362 | +0.334 | 94 | +0.666 | +0.315 |
| 4h | calibrated | BRK_tap200_first | record | NA | both | 452 | +0.194 | +0.248 | 444 | +0.209 | +0.263 | 241 | +0.292 | +0.339 | 241 | +0.676 | +0.724 | 211 | +0.085 | +0.155 | 203 | -0.275 | -0.205 |
| 4h | calibrated | BRK_tap200_first | record | NA | long | 262 | +0.240 | +0.318 | 256 | +0.165 | +0.403 | 147 | +0.521 | +0.527 | 147 | +0.947 | +0.979 | 115 | -0.100 | +0.068 | 109 | -1.317 | -0.827 |
| 4h | calibrated | BRK_tap200_first | record | NA | short | 190 | +0.127 | +0.157 | 188 | +0.421 | +0.290 | 94 | -0.102 | -0.013 | 94 | +0.208 | +0.271 | 96 | +0.362 | +0.334 | 94 | +0.666 | +0.315 |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 388 | +0.149 | +0.203 | 380 | +0.183 | +0.237 | 206 | +0.301 | +0.349 | 206 | +0.666 | +0.713 | 182 | +0.034 | +0.104 | 174 | -0.511 | -0.442 |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 233 | +0.214 | +0.292 | 227 | +0.162 | +0.400 | 128 | +0.581 | +0.588 | 128 | +0.954 | +0.986 | 105 | -0.095 | +0.073 | 99 | -1.317 | -0.827 |
| 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 155 | +0.039 | +0.069 | 153 | +0.207 | +0.077 | 78 | -0.115 | -0.026 | 78 | +0.176 | +0.239 | 77 | +0.291 | +0.263 | 75 | +0.421 | +0.071 |
| 4h | calibrated | BRK_tap200_oneshot | record | NA | both | 388 | +0.149 | +0.203 | 380 | +0.183 | +0.237 | 206 | +0.301 | +0.349 | 206 | +0.666 | +0.713 | 182 | +0.034 | +0.104 | 174 | -0.511 | -0.442 |
| 4h | calibrated | BRK_tap200_oneshot | record | NA | long | 233 | +0.214 | +0.292 | 227 | +0.162 | +0.400 | 128 | +0.581 | +0.588 | 128 | +0.954 | +0.986 | 105 | -0.095 | +0.073 | 99 | -1.317 | -0.827 |
| 4h | calibrated | BRK_tap200_oneshot | record | NA | short | 155 | +0.039 | +0.069 | 153 | +0.207 | +0.077 | 78 | -0.115 | -0.026 | 78 | +0.176 | +0.239 | 77 | +0.291 | +0.263 | 75 | +0.421 | +0.071 |
| 4h | calibrated | BRK_mem_first | record | ALL | both | 469 | -0.190 | -0.136 | 464 | -0.021 | +0.033 | 246 | -0.100 | -0.052 | 246 | +0.105 | +0.153 | 223 | -0.224 | -0.154 | 218 | -0.296 | -0.226 |
| 4h | calibrated | BRK_mem_first | record | ALL | long | 256 | -0.089 | -0.010 | 254 | +0.122 | +0.360 | 145 | +0.349 | +0.356 | 145 | +0.807 | +0.839 | 111 | -0.486 | -0.318 | 109 | -0.746 | -0.256 |
| 4h | calibrated | BRK_mem_first | record | ALL | short | 213 | -0.225 | -0.195 | 210 | -0.067 | -0.197 | 101 | -0.404 | -0.315 | 101 | -0.633 | -0.570 | 112 | +0.004 | -0.024 | 109 | +0.623 | +0.273 |
| 4h | calibrated | BRK_mem_first | record | NA | both | 469 | -0.190 | -0.136 | 464 | -0.021 | +0.033 | 246 | -0.100 | -0.052 | 246 | +0.105 | +0.153 | 223 | -0.224 | -0.154 | 218 | -0.296 | -0.226 |
| 4h | calibrated | BRK_mem_first | record | NA | long | 256 | -0.089 | -0.010 | 254 | +0.122 | +0.360 | 145 | +0.349 | +0.356 | 145 | +0.807 | +0.839 | 111 | -0.486 | -0.318 | 109 | -0.746 | -0.256 |
| 4h | calibrated | BRK_mem_first | record | NA | short | 213 | -0.225 | -0.195 | 210 | -0.067 | -0.197 | 101 | -0.404 | -0.315 | 101 | -0.633 | -0.570 | 112 | +0.004 | -0.024 | 109 | +0.623 | +0.273 |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 440 | -0.206 | -0.152 | 435 | +0.036 | +0.090 | 235 | -0.244 | -0.197 | 235 | -0.023 | +0.025 | 205 | -0.197 | -0.127 | 200 | +0.457 | +0.527 |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 243 | -0.092 | -0.013 | 241 | +0.195 | +0.434 | 136 | +0.332 | +0.338 | 136 | +0.512 | +0.545 | 107 | -0.409 | -0.242 | 105 | -0.407 | +0.083 |
| 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 197 | -0.268 | -0.238 | 194 | -0.035 | -0.166 | 99 | -0.469 | -0.380 | 99 | -0.672 | -0.609 | 98 | -0.010 | -0.038 | 95 | +1.869 | +1.518 |
| 4h | calibrated | BRK_mem_oneshot | record | NA | both | 440 | -0.206 | -0.152 | 435 | +0.036 | +0.090 | 235 | -0.244 | -0.197 | 235 | -0.023 | +0.025 | 205 | -0.197 | -0.127 | 200 | +0.457 | +0.527 |
| 4h | calibrated | BRK_mem_oneshot | record | NA | long | 243 | -0.092 | -0.013 | 241 | +0.195 | +0.434 | 136 | +0.332 | +0.338 | 136 | +0.512 | +0.545 | 107 | -0.409 | -0.242 | 105 | -0.407 | +0.083 |
| 4h | calibrated | BRK_mem_oneshot | record | NA | short | 197 | -0.268 | -0.238 | 194 | -0.035 | -0.166 | 99 | -0.469 | -0.380 | 99 | -0.672 | -0.609 | 98 | -0.010 | -0.038 | 95 | +1.869 | +1.518 |
| 4h | calibrated | SFP_harden | record | ALL | both | 929 | +0.094 | +0.149 | 922 | +0.333 | +0.387 | 455 | -0.005 | +0.043 | 455 | -0.098 | -0.050 | 474 | +0.162 | +0.232 | 467 | +0.918 | +0.988 |
| 4h | calibrated | SFP_harden | record | ALL | long | 468 | +0.208 | +0.287 | 463 | +0.042 | +0.281 | 201 | +0.394 | +0.401 | 201 | -0.090 | -0.057 | 267 | +0.118 | +0.286 | 262 | +0.046 | +0.536 |
| 4h | calibrated | SFP_harden | record | ALL | short | 461 | -0.027 | +0.003 | 459 | +0.802 | +0.671 | 254 | -0.210 | -0.121 | 254 | -0.098 | -0.035 | 207 | +0.243 | +0.215 | 205 | +1.557 | +1.206 |
| 4h | calibrated | SFP_harden | record | NA | both | 929 | +0.094 | +0.149 | 922 | +0.333 | +0.387 | 455 | -0.005 | +0.043 | 455 | -0.098 | -0.050 | 474 | +0.162 | +0.232 | 467 | +0.918 | +0.988 |
| 4h | calibrated | SFP_harden | record | NA | long | 468 | +0.208 | +0.287 | 463 | +0.042 | +0.281 | 201 | +0.394 | +0.401 | 201 | -0.090 | -0.057 | 267 | +0.118 | +0.286 | 262 | +0.046 | +0.536 |
| 4h | calibrated | SFP_harden | record | NA | short | 461 | -0.027 | +0.003 | 459 | +0.802 | +0.671 | 254 | -0.210 | -0.121 | 254 | -0.098 | -0.035 | 207 | +0.243 | +0.215 | 205 | +1.557 | +1.206 |
| 1d | calibrated | BRK_tap89_first | record | ALL | both | 101 | +0.081 | +0.102 | 93 | -0.254 | -0.233 | 51 | +0.089 | +0.108 | 51 | -0.040 | -0.021 | 50 | -0.115 | -0.089 | 42 | -1.359 | -1.334 |
| 1d | calibrated | BRK_tap89_first | record | ALL | long | 55 | -0.037 | +0.044 | 53 | -0.945 | -0.515 | 33 | +0.311 | +0.306 | 33 | -0.105 | -0.276 | 22 | -1.268 | -1.100 | 20 | -2.891 | -1.698 |
| 1d | calibrated | BRK_tap89_first | record | ALL | short | 46 | +0.514 | +0.475 | 40 | +0.038 | -0.352 | 18 | +0.031 | +0.072 | 18 | -0.002 | +0.207 | 28 | +1.047 | +0.930 | 22 | +1.273 | +0.129 |
| 1d | calibrated | BRK_tap89_first | record | NA | both | 101 | +0.081 | +0.102 | 93 | -0.254 | -0.233 | 51 | +0.089 | +0.108 | 51 | -0.040 | -0.021 | 50 | -0.115 | -0.089 | 42 | -1.359 | -1.334 |
| 1d | calibrated | BRK_tap89_first | record | NA | long | 55 | -0.037 | +0.044 | 53 | -0.945 | -0.515 | 33 | +0.311 | +0.306 | 33 | -0.105 | -0.276 | 22 | -1.268 | -1.100 | 20 | -2.891 | -1.698 |
| 1d | calibrated | BRK_tap89_first | record | NA | short | 46 | +0.514 | +0.475 | 40 | +0.038 | -0.352 | 18 | +0.031 | +0.072 | 18 | -0.002 | +0.207 | 28 | +1.047 | +0.930 | 22 | +1.273 | +0.129 |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 82 | +0.029 | +0.050 | 76 | -0.135 | -0.115 | 43 | +0.308 | +0.327 | 43 | +0.041 | +0.059 | 39 | -0.390 | -0.364 | 33 | -1.336 | -1.311 |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 48 | -0.108 | -0.027 | 46 | -0.789 | -0.359 | 27 | +0.914 | +0.910 | 27 | +0.106 | -0.066 | 21 | -1.024 | -0.856 | 19 | -2.440 | -1.247 |
| 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 34 | +0.513 | +0.473 | 30 | +0.723 | +0.333 | 16 | +0.109 | +0.150 | 16 | -0.002 | +0.207 | 18 | +0.881 | +0.765 | 14 | +2.905 | +1.762 |
| 1d | calibrated | BRK_tap89_oneshot | record | NA | both | 82 | +0.029 | +0.050 | 76 | -0.135 | -0.115 | 43 | +0.308 | +0.327 | 43 | +0.041 | +0.059 | 39 | -0.390 | -0.364 | 33 | -1.336 | -1.311 |
| 1d | calibrated | BRK_tap89_oneshot | record | NA | long | 48 | -0.108 | -0.027 | 46 | -0.789 | -0.359 | 27 | +0.914 | +0.910 | 27 | +0.106 | -0.066 | 21 | -1.024 | -0.856 | 19 | -2.440 | -1.247 |
| 1d | calibrated | BRK_tap89_oneshot | record | NA | short | 34 | +0.513 | +0.473 | 30 | +0.723 | +0.333 | 16 | +0.109 | +0.150 | 16 | -0.002 | +0.207 | 18 | +0.881 | +0.765 | 14 | +2.905 | +1.762 |
| 1d | calibrated | BRK_tap127_first | record | ALL | both | 88 | +0.030 | +0.050 | 81 | -0.123 | -0.103 | 44 | +0.034 | +0.053 | 44 | +0.304 | +0.322 | 44 | -0.043 | -0.017 | 37 | -1.338 | -1.313 |
| 1d | calibrated | BRK_tap127_first | record | ALL | long | 47 | -0.178 | -0.096 | 44 | -0.599 | -0.169 | 26 | +0.417 | +0.412 | 26 | -0.072 | -0.244 | 21 | -1.021 | -0.853 | 18 | -1.531 | -0.338 |
| 1d | calibrated | BRK_tap127_first | record | ALL | short | 41 | +0.591 | +0.551 | 37 | +0.257 | -0.132 | 18 | -0.713 | -0.671 | 18 | +0.587 | +0.796 | 23 | +1.415 | +1.299 | 19 | -1.335 | -2.478 |
| 1d | calibrated | BRK_tap127_first | record | NA | both | 88 | +0.030 | +0.050 | 81 | -0.123 | -0.103 | 44 | +0.034 | +0.053 | 44 | +0.304 | +0.322 | 44 | -0.043 | -0.017 | 37 | -1.338 | -1.313 |
| 1d | calibrated | BRK_tap127_first | record | NA | long | 47 | -0.178 | -0.096 | 44 | -0.599 | -0.169 | 26 | +0.417 | +0.412 | 26 | -0.072 | -0.244 | 21 | -1.021 | -0.853 | 18 | -1.531 | -0.338 |
| 1d | calibrated | BRK_tap127_first | record | NA | short | 41 | +0.591 | +0.551 | 37 | +0.257 | -0.132 | 18 | -0.713 | -0.671 | 18 | +0.587 | +0.796 | 23 | +1.415 | +1.299 | 19 | -1.335 | -2.478 |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 71 | -0.182 | -0.161 | 65 | -0.123 | -0.102 | 37 | +0.061 | +0.079 | 37 | +0.345 | +0.364 | 34 | -0.420 | -0.394 | 28 | -1.674 | -1.649 |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 38 | -0.282 | -0.201 | 36 | -0.788 | -0.358 | 20 | +0.670 | +0.665 | 20 | -0.263 | -0.435 | 18 | -1.085 | -0.917 | 16 | -1.531 | -0.338 |
| 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 33 | +0.590 | +0.550 | 29 | +0.341 | -0.048 | 17 | -0.418 | -0.377 | 17 | +0.832 | +1.041 | 16 | +1.477 | +1.361 | 12 | -1.675 | -2.818 |
| 1d | calibrated | BRK_tap127_oneshot | record | NA | both | 71 | -0.182 | -0.161 | 65 | -0.123 | -0.102 | 37 | +0.061 | +0.079 | 37 | +0.345 | +0.364 | 34 | -0.420 | -0.394 | 28 | -1.674 | -1.649 |
| 1d | calibrated | BRK_tap127_oneshot | record | NA | long | 38 | -0.282 | -0.201 | 36 | -0.788 | -0.358 | 20 | +0.670 | +0.665 | 20 | -0.263 | -0.435 | 18 | -1.085 | -0.917 | 16 | -1.531 | -0.338 |
| 1d | calibrated | BRK_tap127_oneshot | record | NA | short | 33 | +0.590 | +0.550 | 29 | +0.341 | -0.048 | 17 | -0.418 | -0.377 | 17 | +0.832 | +1.041 | 16 | +1.477 | +1.361 | 12 | -1.675 | -2.818 |
| 1d | calibrated | BRK_tap200_first | record | ALL | both | 67 | +0.218 | +0.239 | 63 | -0.479 | -0.459 | 36 | +0.319 | +0.338 | 36 | +0.248 | +0.266 | 31 | +0.114 | +0.140 | 27 | -1.053 | -1.028 |
| 1d | calibrated | BRK_tap200_first | record | ALL | long | 33 | +0.238 | +0.319 | 32 | -0.655 | -0.225 | 19 | +0.422 | +0.417 | 19 | +0.102 | -0.069 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| 1d | calibrated | BRK_tap200_first | record | ALL | short | 34 | +0.139 | +0.099 | 31 | -0.475 | -0.865 | 17 | +0.087 | +0.128 | 17 | +1.147 | +1.355 | 17 | +0.218 | +0.101 | 14 | -0.914 | -2.058 |
| 1d | calibrated | BRK_tap200_first | record | NA | both | 67 | +0.218 | +0.239 | 63 | -0.479 | -0.459 | 36 | +0.319 | +0.338 | 36 | +0.248 | +0.266 | 31 | +0.114 | +0.140 | 27 | -1.053 | -1.028 |
| 1d | calibrated | BRK_tap200_first | record | NA | long | 33 | +0.238 | +0.319 | 32 | -0.655 | -0.225 | 19 | +0.422 | +0.417 | 19 | +0.102 | -0.069 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| 1d | calibrated | BRK_tap200_first | record | NA | short | 34 | +0.139 | +0.099 | 31 | -0.475 | -0.865 | 17 | +0.087 | +0.128 | 17 | +1.147 | +1.355 | 17 | +0.218 | +0.101 | 14 | -0.914 | -2.058 |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 57 | +0.219 | +0.239 | 53 | -0.475 | -0.454 | 30 | +0.328 | +0.346 | 30 | +0.936 | +0.955 | 27 | +0.048 | +0.074 | 23 | -1.053 | -1.028 |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 30 | +0.149 | +0.231 | 29 | -0.834 | -0.404 | 16 | +0.328 | +0.323 | 16 | +0.023 | -0.149 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 27 | +0.218 | +0.178 | 24 | +0.939 | +0.550 | 14 | +0.605 | +0.646 | 14 | +2.359 | +2.568 | 13 | +0.217 | +0.101 | 10 | -0.915 | -2.058 |
| 1d | calibrated | BRK_tap200_oneshot | record | NA | both | 57 | +0.219 | +0.239 | 53 | -0.475 | -0.454 | 30 | +0.328 | +0.346 | 30 | +0.936 | +0.955 | 27 | +0.048 | +0.074 | 23 | -1.053 | -1.028 |
| 1d | calibrated | BRK_tap200_oneshot | record | NA | long | 30 | +0.149 | +0.231 | 29 | -0.834 | -0.404 | 16 | +0.328 | +0.323 | 16 | +0.023 | -0.149 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| 1d | calibrated | BRK_tap200_oneshot | record | NA | short | 27 | +0.218 | +0.178 | 24 | +0.939 | +0.550 | 14 | +0.605 | +0.646 | 14 | +2.359 | +2.568 | 13 | +0.217 | +0.101 | 10 | -0.915 | -2.058 |
| 1d | calibrated | BRK_mem_first | record | ALL | both | 89 | +0.601 | +0.622 | 84 | -0.176 | -0.155 | 46 | +0.137 | +0.156 | 46 | +0.560 | +0.579 | 43 | +0.731 | +0.757 | 38 | -0.563 | -0.538 |
| 1d | calibrated | BRK_mem_first | record | ALL | long | 49 | +0.138 | +0.219 | 48 | -0.147 | +0.283 | 29 | +0.138 | +0.133 | 29 | +0.763 | +0.591 | 20 | +0.230 | +0.399 | 19 | -0.850 | +0.343 |
| 1d | calibrated | BRK_mem_first | record | ALL | short | 40 | +0.807 | +0.767 | 36 | -0.215 | -0.605 | 17 | -0.173 | -0.132 | 17 | +0.216 | +0.425 | 23 | +1.227 | +1.110 | 19 | -0.337 | -1.480 |
| 1d | calibrated | BRK_mem_first | record | NA | both | 89 | +0.601 | +0.622 | 84 | -0.176 | -0.155 | 46 | +0.137 | +0.156 | 46 | +0.560 | +0.579 | 43 | +0.731 | +0.757 | 38 | -0.563 | -0.538 |
| 1d | calibrated | BRK_mem_first | record | NA | long | 49 | +0.138 | +0.219 | 48 | -0.147 | +0.283 | 29 | +0.138 | +0.133 | 29 | +0.763 | +0.591 | 20 | +0.230 | +0.399 | 19 | -0.850 | +0.343 |
| 1d | calibrated | BRK_mem_first | record | NA | short | 40 | +0.807 | +0.767 | 36 | -0.215 | -0.605 | 17 | -0.173 | -0.132 | 17 | +0.216 | +0.425 | 23 | +1.227 | +1.110 | 19 | -0.337 | -1.480 |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 80 | +0.616 | +0.637 | 76 | +0.229 | +0.249 | 41 | +0.136 | +0.154 | 41 | +0.357 | +0.376 | 39 | +0.757 | +0.783 | 35 | +0.004 | +0.029 |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 46 | +0.137 | +0.218 | 45 | -0.291 | +0.139 | 26 | +0.076 | +0.071 | 26 | +0.159 | -0.013 | 20 | +0.609 | +0.777 | 19 | -0.814 | +0.379 |
| 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 34 | +0.946 | +0.907 | 31 | +1.276 | +0.887 | 15 | +0.630 | +0.672 | 15 | +0.424 | +0.632 | 19 | +1.590 | +1.474 | 16 | +1.743 | +0.600 |
| 1d | calibrated | BRK_mem_oneshot | record | NA | both | 80 | +0.616 | +0.637 | 76 | +0.229 | +0.249 | 41 | +0.136 | +0.154 | 41 | +0.357 | +0.376 | 39 | +0.757 | +0.783 | 35 | +0.004 | +0.029 |
| 1d | calibrated | BRK_mem_oneshot | record | NA | long | 46 | +0.137 | +0.218 | 45 | -0.291 | +0.139 | 26 | +0.076 | +0.071 | 26 | +0.159 | -0.013 | 20 | +0.609 | +0.777 | 19 | -0.814 | +0.379 |
| 1d | calibrated | BRK_mem_oneshot | record | NA | short | 34 | +0.946 | +0.907 | 31 | +1.276 | +0.887 | 15 | +0.630 | +0.672 | 15 | +0.424 | +0.632 | 19 | +1.590 | +1.474 | 16 | +1.743 | +0.600 |
| 1d | calibrated | SFP_harden | record | ALL | both | 120 | -0.526 | -0.505 | 117 | +0.216 | +0.236 | 60 | +0.064 | +0.082 | 60 | +0.224 | +0.243 | 60 | -1.113 | -1.087 | 57 | +0.212 | +0.237 |
| 1d | calibrated | SFP_harden | record | ALL | long | 66 | -0.381 | -0.300 | 65 | +0.930 | +1.360 | 27 | +0.287 | +0.282 | 27 | -0.002 | -0.174 | 39 | -0.915 | -0.747 | 38 | +1.089 | +2.282 |
| 1d | calibrated | SFP_harden | record | ALL | short | 54 | -1.039 | -1.078 | 52 | +0.198 | -0.191 | 33 | -0.421 | -0.380 | 33 | +0.232 | +0.441 | 21 | -2.023 | -2.140 | 19 | -2.293 | -3.437 |
| 1d | calibrated | SFP_harden | record | NA | both | 120 | -0.526 | -0.505 | 117 | +0.216 | +0.236 | 60 | +0.064 | +0.082 | 60 | +0.224 | +0.243 | 60 | -1.113 | -1.087 | 57 | +0.212 | +0.237 |
| 1d | calibrated | SFP_harden | record | NA | long | 66 | -0.381 | -0.300 | 65 | +0.930 | +1.360 | 27 | +0.287 | +0.282 | 27 | -0.002 | -0.174 | 39 | -0.915 | -0.747 | 38 | +1.089 | +2.282 |
| 1d | calibrated | SFP_harden | record | NA | short | 54 | -1.039 | -1.078 | 52 | +0.198 | -0.191 | 33 | -0.421 | -0.380 | 33 | +0.232 | +0.441 | 21 | -2.023 | -2.140 | 19 | -2.293 | -3.437 |

## 6 · Base rate — POOLED:CLASSIC5 · calibrated · law record (every bar of L; whole over lens x cell x direction)

| lens | L+1 cell | dir | n ALL H20 | median ALL H20 | NET ALL H20 | n ALL H100 | median ALL H100 | NET ALL H100 | n tuning H20 | median tuning H20 | NET tuning H20 | n tuning H100 | median tuning H100 | NET tuning H100 | n holdout H20 | median holdout H20 | NET holdout H20 | n holdout H100 | median holdout H100 | NET holdout H100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1h | ALL | both | 569220 | +0.000 | -0.135 | 568420 | +0.000 | -0.134 | 373570 | +0.000 | -0.122 | 373570 | +0.000 | -0.122 | 195650 | +0.000 | -0.161 | 194850 | +0.000 | -0.161 |
| 1h | ALL | long | 284610 | +0.039 | -0.096 | 284210 | +0.205 | +0.071 | 186785 | +0.049 | -0.073 | 186785 | +0.250 | +0.128 | 97825 | +0.017 | -0.143 | 97425 | +0.124 | -0.037 |
| 1h | ALL | short | 284610 | -0.039 | -0.174 | 284210 | -0.205 | -0.340 | 186785 | -0.049 | -0.170 | 186785 | -0.250 | -0.372 | 97825 | -0.017 | -0.178 | 97425 | -0.124 | -0.284 |
| 1h | EXP_ALIGNED* | both | 149629 | -0.027 | -0.155 | 149229 | -0.044 | -0.172 | 95776 | -0.013 | -0.128 | 95776 | +0.032 | -0.084 | 53853 | -0.053 | -0.212 | 53453 | -0.175 | -0.334 |
| 1h | EXP_ALIGNED* | long | 77909 | +0.024 | -0.109 | 77509 | +0.254 | +0.121 | 50272 | +0.055 | -0.061 | 50272 | +0.507 | +0.391 | 27637 | -0.037 | -0.210 | 27237 | -0.186 | -0.359 |
| 1h | EXP_ALIGNED* | short | 71720 | -0.082 | -0.204 | 71720 | -0.353 | -0.475 | 45504 | -0.089 | -0.204 | 45504 | -0.458 | -0.574 | 26216 | -0.067 | -0.205 | 26216 | -0.159 | -0.298 |
| 1h | EXP_COUNTER | both | 149629 | +0.027 | -0.101 | 149229 | +0.044 | -0.084 | 95776 | +0.013 | -0.103 | 95776 | -0.032 | -0.148 | 53853 | +0.053 | -0.106 | 53453 | +0.175 | +0.016 |
| 1h | EXP_COUNTER | long | 71720 | +0.082 | -0.039 | 71720 | +0.353 | +0.231 | 45504 | +0.089 | -0.026 | 45504 | +0.458 | +0.343 | 26216 | +0.067 | -0.072 | 26216 | +0.159 | +0.020 |
| 1h | EXP_COUNTER | short | 77909 | -0.024 | -0.158 | 77509 | -0.254 | -0.387 | 50272 | -0.055 | -0.170 | 50272 | -0.507 | -0.623 | 27637 | +0.037 | -0.135 | 27237 | +0.186 | +0.012 |
| 1h | IN_RANGE_COINCIDENT* | both | 50102 | +0.000 | -0.161 | 50102 | +0.000 | -0.161 | 36930 | +0.000 | -0.154 | 36930 | +0.000 | -0.154 | 13172 | +0.000 | -0.172 | 13172 | +0.000 | -0.172 |
| 1h | IN_RANGE_COINCIDENT* | long | 25051 | +0.020 | -0.141 | 25051 | -0.223 | -0.384 | 18465 | +0.028 | -0.126 | 18465 | -0.262 | -0.417 | 6586 | -0.001 | -0.173 | 6586 | -0.088 | -0.260 |
| 1h | IN_RANGE_COINCIDENT* | short | 25051 | -0.020 | -0.181 | 25051 | +0.223 | +0.062 | 18465 | -0.028 | -0.183 | 18465 | +0.262 | +0.108 | 6586 | +0.001 | -0.171 | 6586 | +0.088 | -0.085 |
| 1h | IN_RANGE_MID* | both | 116568 | +0.000 | -0.142 | 116568 | +0.000 | -0.142 | 75368 | +0.000 | -0.127 | 75368 | +0.000 | -0.127 | 41200 | +0.000 | -0.161 | 41200 | +0.000 | -0.161 |
| 1h | IN_RANGE_MID* | long | 58284 | +0.058 | -0.084 | 58284 | +0.379 | +0.237 | 37684 | +0.039 | -0.088 | 37684 | +0.158 | +0.031 | 20600 | +0.095 | -0.066 | 20600 | +0.777 | +0.617 |
| 1h | IN_RANGE_MID* | short | 58284 | -0.058 | -0.200 | 58284 | -0.379 | -0.521 | 37684 | -0.039 | -0.166 | 37684 | -0.158 | -0.285 | 20600 | -0.095 | -0.255 | 20600 | -0.777 | -0.938 |
| 1h | IN_RANGE_OTHER | both | 101986 | +0.000 | -0.131 | 101986 | +0.000 | -0.131 | 68414 | +0.000 | -0.120 | 68414 | +0.000 | -0.120 | 33572 | +0.000 | -0.162 | 33572 | +0.000 | -0.162 |
| 1h | IN_RANGE_OTHER | long | 50993 | -0.001 | -0.132 | 50993 | -0.065 | -0.196 | 34207 | +0.018 | -0.102 | 34207 | -0.030 | -0.150 | 16786 | -0.054 | -0.216 | 16786 | -0.116 | -0.278 |
| 1h | IN_RANGE_OTHER | short | 50993 | +0.001 | -0.130 | 50993 | +0.065 | -0.066 | 34207 | -0.018 | -0.138 | 34207 | +0.030 | -0.090 | 16786 | +0.054 | -0.107 | 16786 | +0.116 | -0.045 |
| 1h | NONE | both | 1306 | +0.000 | -0.167 | 1306 | +0.000 | -0.167 | 1306 | +0.000 | -0.167 | 1306 | +0.000 | -0.167 | 0 | — | — | 0 | — | — |
| 1h | NONE | long | 653 | -0.384 | -0.551 | 653 | -1.107 | -1.274 | 653 | -0.384 | -0.551 | 653 | -1.107 | -1.274 | 0 | — | — | 0 | — | — |
| 1h | NONE | short | 653 | +0.384 | +0.217 | 653 | +1.107 | +0.940 | 653 | +0.384 | +0.217 | 653 | +1.107 | +0.940 | 0 | — | — | 0 | — | — |
| 4h | ALL | both | 142158 | +0.000 | -0.064 | 141358 | +0.000 | -0.064 | 93388 | +0.000 | -0.058 | 93388 | +0.000 | -0.058 | 48770 | +0.000 | -0.078 | 47970 | +0.000 | -0.078 |
| 4h | ALL | long | 71079 | +0.082 | +0.018 | 70679 | +0.204 | +0.139 | 46694 | +0.101 | +0.043 | 46694 | +0.242 | +0.184 | 24385 | +0.042 | -0.036 | 23985 | +0.107 | +0.029 |
| 4h | ALL | short | 71079 | -0.082 | -0.146 | 70679 | -0.204 | -0.268 | 46694 | -0.101 | -0.159 | 46694 | -0.242 | -0.300 | 24385 | -0.042 | -0.120 | 23985 | -0.107 | -0.184 |
| 4h | EXP_ALIGNED* | both | 39031 | +0.027 | -0.033 | 38667 | -0.079 | -0.139 | 27258 | +0.081 | +0.024 | 27258 | +0.042 | -0.016 | 11773 | -0.107 | -0.187 | 11409 | -0.350 | -0.429 |
| 4h | EXP_ALIGNED* | long | 21850 | +0.086 | +0.027 | 21486 | -0.008 | -0.066 | 15807 | +0.156 | +0.101 | 15807 | +0.178 | +0.123 | 6043 | -0.113 | -0.201 | 5679 | -0.551 | -0.638 |
| 4h | EXP_ALIGNED* | short | 17181 | -0.032 | -0.094 | 17181 | -0.142 | -0.204 | 11451 | -0.003 | -0.066 | 11451 | -0.125 | -0.189 | 5730 | -0.106 | -0.165 | 5730 | -0.190 | -0.248 |
| 4h | EXP_COUNTER | both | 39031 | -0.027 | -0.087 | 38667 | +0.079 | +0.020 | 27258 | -0.081 | -0.139 | 27258 | -0.042 | -0.099 | 11773 | +0.107 | +0.028 | 11409 | +0.350 | +0.271 |
| 4h | EXP_COUNTER | long | 17181 | +0.032 | -0.030 | 17181 | +0.142 | +0.079 | 11451 | +0.003 | -0.061 | 11451 | +0.125 | +0.062 | 5730 | +0.106 | +0.047 | 5730 | +0.190 | +0.131 |
| 4h | EXP_COUNTER | short | 21850 | -0.086 | -0.145 | 21486 | +0.008 | -0.051 | 15807 | -0.156 | -0.211 | 15807 | -0.178 | -0.232 | 6043 | +0.113 | +0.026 | 5679 | +0.551 | +0.465 |
| 4h | IN_RANGE_COINCIDENT* | both | 16244 | +0.000 | -0.064 | 16244 | +0.000 | -0.064 | 9838 | +0.000 | -0.050 | 9838 | +0.000 | -0.050 | 6406 | +0.000 | -0.072 | 6406 | +0.000 | -0.072 |
| 4h | IN_RANGE_COINCIDENT* | long | 8122 | +0.097 | +0.033 | 8122 | +0.108 | +0.044 | 4919 | +0.063 | +0.013 | 4919 | +0.639 | +0.589 | 3203 | +0.147 | +0.076 | 3203 | -0.545 | -0.617 |
| 4h | IN_RANGE_COINCIDENT* | short | 8122 | -0.097 | -0.161 | 8122 | -0.108 | -0.172 | 4919 | -0.063 | -0.113 | 4919 | -0.639 | -0.689 | 3203 | -0.147 | -0.219 | 3203 | +0.545 | +0.473 |
| 4h | IN_RANGE_MID* | both | 24578 | +0.000 | -0.073 | 24554 | +0.000 | -0.073 | 14204 | +0.000 | -0.062 | 14204 | +0.000 | -0.062 | 10374 | +0.000 | -0.081 | 10350 | +0.000 | -0.081 |
| 4h | IN_RANGE_MID* | long | 12289 | +0.150 | +0.078 | 12277 | +0.549 | +0.477 | 7102 | +0.256 | +0.194 | 7102 | +0.319 | +0.256 | 5187 | +0.020 | -0.061 | 5175 | +0.863 | +0.782 |
| 4h | IN_RANGE_MID* | short | 12289 | -0.150 | -0.223 | 12277 | -0.549 | -0.622 | 7102 | -0.256 | -0.318 | 7102 | -0.319 | -0.381 | 5187 | -0.020 | -0.101 | 5175 | -0.863 | -0.944 |
| 4h | IN_RANGE_OTHER | both | 22592 | +0.000 | -0.070 | 22544 | +0.000 | -0.069 | 14148 | +0.000 | -0.063 | 14148 | +0.000 | -0.063 | 8444 | +0.000 | -0.078 | 8396 | +0.000 | -0.078 |
| 4h | IN_RANGE_OTHER | long | 11296 | +0.087 | +0.018 | 11272 | +0.784 | +0.715 | 7074 | +0.077 | +0.015 | 7074 | +0.687 | +0.624 | 4222 | +0.125 | +0.046 | 4198 | +1.057 | +0.979 |
| 4h | IN_RANGE_OTHER | short | 11296 | -0.087 | -0.157 | 11272 | -0.784 | -0.853 | 7074 | -0.077 | -0.140 | 7074 | -0.687 | -0.750 | 4222 | -0.125 | -0.203 | 4198 | -1.057 | -1.135 |
| 4h | NONE | both | 682 | +0.000 | -0.065 | 682 | +0.000 | -0.065 | 682 | +0.000 | -0.065 | 682 | +0.000 | -0.065 | 0 | — | — | 0 | — | — |
| 4h | NONE | long | 341 | -0.393 | -0.458 | 341 | -6.159 | -6.224 | 341 | -0.393 | -0.458 | 341 | -6.159 | -6.224 | 0 | — | — | 0 | — | — |
| 4h | NONE | short | 341 | +0.393 | +0.328 | 341 | +6.159 | +6.094 | 341 | +0.393 | +0.328 | 341 | +6.159 | +6.094 | 0 | — | — | 0 | — | — |
| 12h | ALL | both | 47258 | +0.000 | -0.035 | 46458 | +0.000 | -0.035 | 31128 | +0.000 | -0.032 | 31128 | +0.000 | -0.032 | 16130 | +0.000 | -0.043 | 15330 | +0.000 | -0.042 |
| 12h | ALL | long | 23629 | +0.139 | +0.104 | 23229 | +0.631 | +0.596 | 15564 | +0.147 | +0.115 | 15564 | +0.917 | +0.885 | 8065 | +0.120 | +0.077 | 7665 | +0.098 | +0.057 |
| 12h | ALL | short | 23629 | -0.139 | -0.174 | 23229 | -0.631 | -0.666 | 15564 | -0.147 | -0.179 | 15564 | -0.917 | -0.949 | 8065 | -0.120 | -0.163 | 7665 | -0.098 | -0.140 |
| 12h | EXP_ALIGNED* | both | 15588 | -0.013 | -0.046 | 15314 | -0.407 | -0.439 | 11006 | +0.085 | +0.056 | 11006 | +0.521 | +0.492 | 4582 | -0.227 | -0.268 | 4308 | -1.809 | -1.849 |
| 12h | EXP_ALIGNED* | long | 8702 | +0.213 | +0.181 | 8500 | +0.793 | +0.761 | 6636 | +0.294 | +0.264 | 6636 | +1.567 | +1.537 | 2066 | -0.006 | -0.050 | 1864 | -1.286 | -1.329 |
| 12h | EXP_ALIGNED* | short | 6886 | -0.262 | -0.297 | 6814 | -1.764 | -1.797 | 4370 | -0.168 | -0.195 | 4370 | -1.347 | -1.374 | 2516 | -0.443 | -0.484 | 2444 | -2.245 | -2.284 |
| 12h | EXP_COUNTER | both | 15588 | +0.013 | -0.020 | 15314 | +0.407 | +0.374 | 11006 | -0.085 | -0.114 | 11006 | -0.521 | -0.550 | 4582 | +0.227 | +0.186 | 4308 | +1.809 | +1.768 |
| 12h | EXP_COUNTER | long | 6886 | +0.262 | +0.228 | 6814 | +1.764 | +1.730 | 4370 | +0.168 | +0.141 | 4370 | +1.347 | +1.320 | 2516 | +0.443 | +0.402 | 2444 | +2.245 | +2.205 |
| 12h | EXP_COUNTER | short | 8702 | -0.213 | -0.245 | 8500 | -0.793 | -0.825 | 6636 | -0.294 | -0.324 | 6636 | -1.567 | -1.597 | 2066 | +0.006 | -0.037 | 1864 | +1.286 | +1.242 |
| 12h | IN_RANGE_COINCIDENT* | both | 6388 | +0.000 | -0.045 | 6388 | +0.000 | -0.045 | 3530 | +0.000 | -0.044 | 3530 | +0.000 | -0.044 | 2858 | +0.000 | -0.045 | 2858 | +0.000 | -0.045 |
| 12h | IN_RANGE_COINCIDENT* | long | 3194 | +0.136 | +0.092 | 3194 | +0.038 | -0.006 | 1765 | +0.216 | +0.172 | 1765 | +0.551 | +0.507 | 1429 | -0.019 | -0.064 | 1429 | -0.724 | -0.768 |
| 12h | IN_RANGE_COINCIDENT* | short | 3194 | -0.136 | -0.181 | 3194 | -0.038 | -0.083 | 1765 | -0.216 | -0.259 | 1765 | -0.551 | -0.594 | 1429 | +0.019 | -0.026 | 1429 | +0.724 | +0.679 |
| 12h | IN_RANGE_MID* | both | 3812 | +0.000 | -0.035 | 3744 | +0.000 | -0.035 | 2004 | +0.000 | -0.034 | 2004 | +0.000 | -0.034 | 1808 | +0.000 | -0.039 | 1740 | +0.000 | -0.039 |
| 12h | IN_RANGE_MID* | long | 1906 | -0.596 | -0.630 | 1872 | -1.875 | -1.910 | 1002 | -0.787 | -0.821 | 1002 | -2.906 | -2.941 | 904 | -0.281 | -0.320 | 870 | -0.973 | -1.012 |
| 12h | IN_RANGE_MID* | short | 1906 | +0.596 | +0.561 | 1872 | +1.875 | +1.841 | 1002 | +0.787 | +0.753 | 1002 | +2.906 | +2.872 | 904 | +0.281 | +0.242 | 870 | +0.973 | +0.934 |
| 12h | IN_RANGE_OTHER | both | 5450 | +0.000 | -0.038 | 5266 | +0.000 | -0.037 | 3150 | +0.000 | -0.036 | 3150 | +0.000 | -0.036 | 2300 | +0.000 | -0.044 | 2116 | +0.000 | -0.041 |
| 12h | IN_RANGE_OTHER | long | 2725 | +0.141 | +0.103 | 2633 | -1.407 | -1.444 | 1575 | +0.231 | +0.195 | 1575 | -0.922 | -0.959 | 1150 | +0.017 | -0.027 | 1058 | -1.899 | -1.940 |
| 12h | IN_RANGE_OTHER | short | 2725 | -0.141 | -0.179 | 2633 | +1.407 | +1.370 | 1575 | -0.231 | -0.268 | 1575 | +0.922 | +0.886 | 1150 | -0.017 | -0.061 | 1058 | +1.899 | +1.858 |
| 12h | NONE | both | 432 | +0.000 | -0.037 | 432 | +0.000 | -0.037 | 432 | +0.000 | -0.037 | 432 | +0.000 | -0.037 | 0 | — | — | 0 | — | — |
| 12h | NONE | long | 216 | -1.385 | -1.422 | 216 | -1.385 | -1.422 | 216 | -1.385 | -1.422 | 216 | -1.385 | -1.422 | 0 | — | — | 0 | — | — |
| 12h | NONE | short | 216 | +1.385 | +1.348 | 216 | +1.385 | +1.348 | 216 | +1.385 | +1.348 | 216 | +1.385 | +1.348 | 0 | — | — | 0 | — | — |
| 1d | ALL | both | 23520 | +0.000 | -0.024 | 22720 | +0.000 | -0.024 | 15550 | +0.000 | -0.021 | 15550 | +0.000 | -0.021 | 7970 | +0.000 | -0.028 | 7170 | +0.000 | -0.027 |
| 1d | ALL | long | 11760 | +0.077 | +0.053 | 11360 | +0.495 | +0.472 | 7775 | +0.117 | +0.096 | 7775 | +0.794 | +0.773 | 3985 | -0.012 | -0.041 | 3585 | -0.304 | -0.331 |
| 1d | ALL | short | 11760 | -0.077 | -0.101 | 11360 | -0.495 | -0.519 | 7775 | -0.117 | -0.138 | 7775 | -0.794 | -0.815 | 3985 | +0.012 | -0.016 | 3585 | +0.304 | +0.277 |
| 1d | EXP_ALIGNED* | both | 7356 | +0.036 | +0.011 | 7276 | -0.317 | -0.341 | 5082 | +0.026 | +0.004 | 5082 | -0.180 | -0.201 | 2274 | +0.058 | +0.029 | 2194 | -0.834 | -0.863 |
| 1d | EXP_ALIGNED* | long | 1567 | -0.036 | -0.060 | 1487 | -1.563 | -1.586 | 525 | +0.520 | +0.502 | 525 | +1.920 | +1.902 | 1042 | -0.250 | -0.278 | 962 | -2.857 | -2.885 |
| 1d | EXP_ALIGNED* | short | 5789 | +0.063 | +0.035 | 5789 | -0.130 | -0.157 | 4557 | -0.016 | -0.044 | 4557 | -0.362 | -0.389 | 1232 | +0.429 | +0.411 | 1232 | +0.970 | +0.952 |
| 1d | EXP_COUNTER | both | 7356 | -0.036 | -0.061 | 7276 | +0.317 | +0.292 | 5082 | -0.026 | -0.047 | 5082 | +0.180 | +0.158 | 2274 | -0.058 | -0.087 | 2194 | +0.834 | +0.806 |
| 1d | EXP_COUNTER | long | 5789 | -0.063 | -0.090 | 5789 | +0.130 | +0.102 | 4557 | +0.016 | -0.011 | 4557 | +0.362 | +0.334 | 1232 | -0.429 | -0.447 | 1232 | -0.970 | -0.989 |
| 1d | EXP_COUNTER | short | 1567 | +0.036 | +0.012 | 1487 | +1.563 | +1.541 | 525 | -0.520 | -0.538 | 525 | -1.920 | -1.938 | 1042 | +0.250 | +0.221 | 962 | +2.857 | +2.829 |
| 1d | IN_RANGE_COINCIDENT* | both | 128 | +0.000 | -0.031 | 88 | +0.000 | -0.031 | 0 | — | — | 0 | — | — | 128 | +0.000 | -0.031 | 88 | +0.000 | -0.031 |
| 1d | IN_RANGE_COINCIDENT* | long | 64 | -0.019 | -0.051 | 44 | +3.842 | +3.811 | 0 | — | — | 0 | — | — | 64 | -0.019 | -0.051 | 44 | +3.842 | +3.811 |
| 1d | IN_RANGE_COINCIDENT* | short | 64 | +0.019 | -0.012 | 44 | -3.842 | -3.873 | 0 | — | — | 0 | — | — | 64 | +0.019 | -0.012 | 44 | -3.842 | -3.873 |
| 1d | IN_RANGE_MID* | both | 2108 | +0.000 | -0.021 | 1842 | +0.000 | -0.021 | 308 | +0.000 | -0.020 | 308 | +0.000 | -0.020 | 1800 | +0.000 | -0.022 | 1534 | +0.000 | -0.022 |
| 1d | IN_RANGE_MID* | long | 1054 | -0.054 | -0.075 | 921 | +0.991 | +0.970 | 154 | -1.358 | -1.378 | 154 | -5.827 | -5.847 | 900 | +0.216 | +0.194 | 767 | +2.311 | +2.289 |
| 1d | IN_RANGE_MID* | short | 1054 | +0.054 | +0.033 | 921 | -0.991 | -1.012 | 154 | +1.358 | +1.337 | 154 | +5.827 | +5.807 | 900 | -0.216 | -0.238 | 767 | -2.311 | -2.332 |
| 1d | IN_RANGE_OTHER | both | 3020 | +0.000 | -0.023 | 2686 | +0.000 | -0.023 | 1526 | +0.000 | -0.021 | 1526 | +0.000 | -0.021 | 1494 | +0.000 | -0.029 | 1160 | +0.000 | -0.029 |
| 1d | IN_RANGE_OTHER | long | 1510 | +0.019 | -0.004 | 1343 | -1.164 | -1.187 | 763 | -0.468 | -0.489 | 763 | -1.911 | -1.932 | 747 | +0.748 | +0.719 | 580 | +1.872 | +1.844 |
| 1d | IN_RANGE_OTHER | short | 1510 | -0.019 | -0.042 | 1343 | +1.164 | +1.142 | 763 | +0.468 | +0.447 | 763 | +1.911 | +1.890 | 747 | -0.748 | -0.776 | 580 | -1.872 | -1.901 |
| 1d | NONE | both | 3552 | +0.000 | -0.022 | 3552 | +0.000 | -0.022 | 3552 | +0.000 | -0.022 | 3552 | +0.000 | -0.022 | 0 | — | — | 0 | — | — |
| 1d | NONE | long | 1776 | +0.870 | +0.848 | 1776 | +4.777 | +4.754 | 1776 | +0.870 | +0.848 | 1776 | +4.777 | +4.754 | 0 | — | — | 0 | — | — |
| 1d | NONE | short | 1776 | -0.870 | -0.892 | 1776 | -4.777 | -4.799 | 1776 | -0.870 | -0.892 | 1776 | -4.777 | -4.799 | 0 | — | — | 0 | — | — |

## 7 · Null (gaps+order, K = 20) — POOLED:CLASSIC5 · calibrated · law record · NET (whole over lens x event x cell x direction; eras ALL and holdout; tuning, every other statistic and the frozen twin in R4_NULL.parquet). The percentile is a DESCRIPTION, never a p-value.

| lens | event | L+1 cell | dir | real NET ALL H20 | null med [q25, q75] ALL H20 | pctile ALL H20 | real NET ALL H100 | null med [q25, q75] ALL H100 | pctile ALL H100 | real NET holdout H20 | null med [q25, q75] holdout H20 | pctile holdout H20 | real NET holdout H100 | null med [q25, q75] holdout H100 | pctile holdout H100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1h | BRK_tap89_first | ALL | both | -0.086 | -0.162 [-0.197, -0.098] | 75.0 | -0.167 | -0.250 [-0.410, -0.184] | 80.0 | -0.289 | -0.274 [-0.315, -0.197] | 45.0 | -0.308 | -0.234 [-0.562, -0.062] | 40.0 |
| 1h | BRK_tap89_first | ALL | long | -0.087 | -0.152 [-0.211, -0.127] | 80.0 | +0.117 | -0.006 [-0.185, +0.132] | 75.0 | -0.485 | -0.305 [-0.447, -0.219] | 25.0 | -0.400 | -0.113 [-0.480, +0.300] | 30.0 |
| 1h | BRK_tap89_first | ALL | short | -0.105 | -0.197 [-0.235, -0.081] | 70.0 | -0.481 | -0.481 [-0.714, -0.347] | 55.0 | -0.183 | -0.234 [-0.279, -0.132] | 60.0 | -0.248 | -0.349 [-0.677, -0.110] | 60.0 |
| 1h | BRK_tap89_first | EXP_ALIGNED* | both | -0.228 | -0.204 [-0.262, -0.159] | 45.0 | -0.229 | -0.250 [-0.442, -0.138] | 55.0 | -0.345 | -0.387 [-0.532, -0.314] | 60.0 | -0.142 | -0.704 [-0.897, -0.326] | 85.0 |
| 1h | BRK_tap89_first | EXP_ALIGNED* | long | -0.134 | -0.120 [-0.211, -0.033] | 50.0 | +0.540 | +0.489 [+0.106, +0.567] | 65.0 | -0.349 | -0.395 [-0.631, -0.259] | 60.0 | +0.153 | -0.195 [-0.646, +0.157] | 75.0 |
| 1h | BRK_tap89_first | EXP_ALIGNED* | short | -0.419 | -0.389 [-0.441, -0.283] | 45.0 | -0.824 | -0.906 [-1.107, -0.529] | 55.0 | -0.339 | -0.324 [-0.641, -0.248] | 50.0 | -0.215 | -0.763 [-1.160, -0.362] | 85.0 |
| 1h | BRK_tap89_first | EXP_COUNTER | both | +0.003 | -0.016 [-0.107, +0.082] | 60.0 | -0.698 | -0.278 [-0.503, +0.077] | 5.0 | -0.067 | -0.123 [-0.187, +0.001] | 60.0 | -0.984 | +0.267 [-0.247, +0.413] | 0.0 |
| 1h | BRK_tap89_first | EXP_COUNTER | long | +0.005 | -0.068 [-0.182, +0.153] | 70.0 | -0.912 | -0.323 [-0.591, -0.061] | 15.0 | -0.106 | -0.249 [-0.459, +0.021] | 65.0 | -1.461 | -0.525 [-0.856, +0.168] | 15.0 |
| 1h | BRK_tap89_first | EXP_COUNTER | short | -0.003 | -0.013 [-0.048, +0.095] | 55.0 | -0.675 | +0.125 [-0.604, +0.553] | 15.0 | +0.002 | +0.114 [-0.182, +0.370] | 40.0 | -0.753 | +0.935 [-0.002, +1.616] | 5.0 |
| 1h | BRK_tap89_first | IN_RANGE_COINCIDENT* | both | -0.436 | +0.078 [-1.862, +0.442] | 47.1 | +0.943 | -3.303 [-6.572, -0.834] | 82.4 | -0.437 | -0.587 [-1.224, +0.050] | 50.0 | +1.202 | -3.566 [-4.846, -2.287] | 100.0 |
| 1h | BRK_tap89_first | IN_RANGE_COINCIDENT* | long | -1.668 | -0.022 [-1.568, +0.809] | 30.0 | +0.171 | -4.885 [-7.478, +3.331] | 70.0 | — | -0.587 [-1.224, +0.050] | — | — | -3.566 [-4.846, -2.287] | — |
| 1h | BRK_tap89_first | IN_RANGE_COINCIDENT* | short | -0.078 | +0.078 [-2.548, +0.442] | 44.4 | +0.964 | -2.335 [-3.621, -2.335] | 100.0 | -0.437 | — [—, —] | — | +1.202 | — [—, —] | — |
| 1h | BRK_tap89_first | IN_RANGE_MID* | both | -0.125 | -0.158 [-0.264, -0.051] | 60.0 | +0.100 | -0.383 [-0.653, +0.054] | 80.0 | -0.585 | -0.318 [-0.555, -0.177] | 20.0 | -0.171 | +0.002 [-0.607, +0.463] | 40.0 |
| 1h | BRK_tap89_first | IN_RANGE_MID* | long | -0.273 | -0.212 [-0.374, +0.009] | 30.0 | +0.148 | -0.426 [-0.741, +0.202] | 70.0 | -0.689 | -0.188 [-0.581, -0.115] | 10.0 | -0.631 | +0.001 [-0.623, +0.392] | 25.0 |
| 1h | BRK_tap89_first | IN_RANGE_MID* | short | -0.019 | -0.112 [-0.270, +0.074] | 60.0 | -0.028 | -0.239 [-0.720, +0.209] | 60.0 | -0.315 | -0.442 [-0.719, -0.169] | 55.0 | -0.026 | -0.235 [-0.836, +0.274] | 60.0 |
| 1h | BRK_tap89_first | IN_RANGE_OTHER | both | +0.149 | -0.150 [-0.294, -0.057] | 90.0 | -0.237 | -0.383 [-0.559, -0.091] | 60.0 | +0.112 | -0.157 [-0.263, +0.034] | 85.0 | -0.311 | -0.445 [-1.158, +0.115] | 55.0 |
| 1h | BRK_tap89_first | IN_RANGE_OTHER | long | +0.060 | -0.315 [-0.657, -0.107] | 85.0 | -0.177 | -0.015 [-0.486, +0.917] | 45.0 | -0.020 | -0.595 [-0.729, -0.148] | 90.0 | -0.181 | +1.180 [-0.672, +2.490] | 35.0 |
| 1h | BRK_tap89_first | IN_RANGE_OTHER | short | +0.170 | +0.004 [-0.236, +0.137] | 80.0 | -0.276 | -0.587 [-0.773, -0.347] | 80.0 | +0.286 | +0.021 [-0.265, +0.305] | 70.0 | -0.294 | -1.642 [-1.919, -1.036] | 85.0 |
| 1h | BRK_tap89_first | NONE | both | +0.471 | +0.776 [+0.384, +1.410] | 32.4 | -3.864 | -0.909 [-2.875, -0.759] | 14.7 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_first | NONE | long | +0.471 | +0.384 [-0.361, +1.410] | 61.1 | -3.864 | -3.864 [-6.861, -0.759] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_first | NONE | short | — | +0.776 [+0.591, +2.501] | — | — | -0.780 [-1.792, +1.269] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_oneshot | ALL | both | -0.066 | -0.133 [-0.167, -0.075] | 80.0 | -0.172 | -0.204 [-0.440, -0.029] | 55.0 | -0.296 | -0.256 [-0.300, -0.243] | 30.0 | -0.652 | -0.404 [-0.668, -0.150] | 25.0 |
| 1h | BRK_tap89_oneshot | ALL | long | -0.081 | -0.142 [-0.189, -0.094] | 80.0 | +0.196 | +0.154 [-0.001, +0.393] | 65.0 | -0.513 | -0.344 [-0.418, -0.223] | 20.0 | -0.719 | -0.216 [-0.534, +0.328] | 20.0 |
| 1h | BRK_tap89_oneshot | ALL | short | -0.060 | -0.075 [-0.137, -0.006] | 65.0 | -0.629 | -0.569 [-0.772, -0.437] | 40.0 | -0.125 | -0.232 [-0.297, -0.096] | 70.0 | -0.648 | -0.636 [-0.754, -0.363] | 50.0 |
| 1h | BRK_tap89_oneshot | EXP_ALIGNED* | both | -0.227 | -0.145 [-0.260, -0.125] | 35.0 | -0.229 | -0.235 [-0.325, -0.080] | 55.0 | -0.342 | -0.332 [-0.466, -0.247] | 50.0 | -0.141 | -0.378 [-0.672, -0.242] | 85.0 |
| 1h | BRK_tap89_oneshot | EXP_ALIGNED* | long | -0.111 | +0.000 [-0.169, +0.080] | 40.0 | +0.572 | +0.581 [+0.184, +0.765] | 50.0 | -0.299 | -0.263 [-0.360, -0.200] | 40.0 | +0.440 | -0.053 [-0.374, +0.734] | 70.0 |
| 1h | BRK_tap89_oneshot | EXP_ALIGNED* | short | -0.416 | -0.362 [-0.441, -0.231] | 45.0 | -0.911 | -0.895 [-1.339, -0.596] | 50.0 | -0.466 | -0.462 [-0.648, -0.271] | 50.0 | -0.373 | -0.836 [-1.148, -0.454] | 80.0 |
| 1h | BRK_tap89_oneshot | EXP_COUNTER | both | -0.016 | -0.034 [-0.106, +0.072] | 55.0 | -0.816 | -0.310 [-0.663, +0.226] | 15.0 | -0.126 | -0.215 [-0.474, -0.099] | 65.0 | -1.486 | -0.719 [-0.805, +0.296] | 10.0 |
| 1h | BRK_tap89_oneshot | EXP_COUNTER | long | -0.016 | -0.060 [-0.254, +0.109] | 55.0 | -1.018 | -0.217 [-0.736, +0.369] | 5.0 | -0.565 | -0.228 [-0.466, -0.139] | 20.0 | -2.462 | -0.665 [-1.710, +0.063] | 15.0 |
| 1h | BRK_tap89_oneshot | EXP_COUNTER | short | -0.012 | +0.009 [-0.040, +0.170] | 40.0 | -0.673 | -0.650 [-0.903, +0.202] | 45.0 | -0.036 | -0.082 [-0.377, +0.007] | 70.0 | -1.119 | +0.501 [-1.241, +1.615] | 30.0 |
| 1h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | both | -0.408 | +0.078 [-1.043, +0.442] | 42.3 | +0.712 | -3.303 [-6.572, -0.834] | 76.9 | — | +0.687 [+0.687, +0.687] | — | — | -6.126 [-6.126, -6.126] | — |
| 1h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | long | -1.668 | -0.408 [-1.393, +0.526] | 28.6 | +0.171 | -5.501 [-8.138, +0.788] | 71.4 | — | +0.687 [+0.687, +0.687] | — | — | -6.126 [-6.126, -6.126] | — |
| 1h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | short | +0.288 | +0.442 [-1.235, +0.442] | 42.9 | +0.733 | -2.335 [-4.454, -1.584] | 85.7 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_oneshot | IN_RANGE_MID* | both | +0.034 | -0.148 [-0.249, +0.093] | 70.0 | +0.155 | -0.316 [-0.640, +0.186] | 75.0 | -0.591 | -0.350 [-0.559, -0.214] | 20.0 | -0.806 | -0.262 [-0.787, +0.485] | 25.0 |
| 1h | BRK_tap89_oneshot | IN_RANGE_MID* | long | -0.241 | -0.234 [-0.426, -0.081] | 45.0 | +0.353 | -0.167 [-0.626, +0.342] | 80.0 | -0.733 | -0.321 [-0.641, -0.172] | 20.0 | -0.995 | +0.117 [-0.860, +0.402] | 20.0 |
| 1h | BRK_tap89_oneshot | IN_RANGE_MID* | short | +0.211 | -0.081 [-0.210, +0.212] | 75.0 | -0.061 | -0.296 [-0.855, +0.204] | 60.0 | -0.266 | -0.221 [-0.771, +0.095] | 45.0 | +0.098 | -0.491 [-0.853, +0.271] | 70.0 |
| 1h | BRK_tap89_oneshot | IN_RANGE_OTHER | both | +0.205 | -0.081 [-0.200, +0.007] | 95.0 | -0.109 | -0.053 [-0.356, +0.208] | 45.0 | +0.168 | -0.176 [-0.371, -0.061] | 95.0 | -0.330 | -0.940 [-1.548, +0.231] | 57.5 |
| 1h | BRK_tap89_oneshot | IN_RANGE_OTHER | long | +0.060 | -0.552 [-0.700, -0.051] | 80.0 | +0.099 | +0.340 [-0.408, +1.227] | 40.0 | -0.156 | -0.708 [-0.996, -0.156] | 75.0 | -0.601 | +0.374 [-0.383, +2.403] | 25.0 |
| 1h | BRK_tap89_oneshot | IN_RANGE_OTHER | short | +0.290 | +0.115 [-0.043, +0.406] | 65.0 | -0.248 | -0.150 [-0.740, +0.221] | 45.0 | +0.440 | +0.104 [-0.212, +0.340] | 80.0 | -0.287 | -1.872 [-2.488, -1.129] | 85.0 |
| 1h | BRK_tap89_oneshot | NONE | both | +0.471 | +0.227 [-0.361, +0.705] | 70.8 | -3.864 | -1.847 [-6.861, -0.438] | 37.5 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_oneshot | NONE | long | +0.471 | +0.384 [-0.361, +1.410] | 61.1 | -3.864 | -3.864 [-6.861, -0.759] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap89_oneshot | NONE | short | — | -0.736 [-1.111, -0.180] | — | — | +5.793 [+1.429, +6.419] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_first | ALL | both | -0.248 | -0.133 [-0.215, -0.109] | 10.0 | -0.237 | -0.244 [-0.429, -0.098] | 55.0 | -0.342 | -0.163 [-0.291, -0.112] | 20.0 | -0.471 | -0.349 [-0.567, -0.158] | 40.0 |
| 1h | BRK_tap127_first | ALL | long | -0.211 | -0.152 [-0.186, -0.071] | 25.0 | -0.059 | -0.105 [-0.213, +0.134] | 55.0 | -0.468 | -0.194 [-0.266, -0.132] | 0.0 | -0.982 | -0.333 [-0.854, -0.149] | 10.0 |
| 1h | BRK_tap127_first | ALL | short | -0.277 | -0.165 [-0.250, -0.029] | 20.0 | -0.439 | -0.454 [-0.626, -0.297] | 55.0 | -0.259 | -0.185 [-0.342, -0.015] | 45.0 | +0.043 | -0.338 [-0.513, +0.065] | 70.0 |
| 1h | BRK_tap127_first | EXP_ALIGNED* | both | -0.270 | -0.196 [-0.281, -0.139] | 30.0 | -0.080 | -0.237 [-0.412, -0.055] | 70.0 | -0.344 | -0.186 [-0.310, -0.137] | 25.0 | -0.399 | -0.643 [-0.928, -0.431] | 75.0 |
| 1h | BRK_tap127_first | EXP_ALIGNED* | long | -0.101 | -0.104 [-0.164, -0.048] | 55.0 | +0.095 | +0.067 [-0.188, +0.293] | 60.0 | -0.147 | -0.140 [-0.179, -0.116] | 35.0 | -1.209 | -0.931 [-1.208, -0.169] | 25.0 |
| 1h | BRK_tap127_first | EXP_ALIGNED* | short | -0.559 | -0.391 [-0.466, -0.344] | 10.0 | -0.486 | -0.536 [-0.688, -0.436] | 60.0 | -0.614 | -0.292 [-0.389, -0.244] | 15.0 | +0.248 | -0.505 [-0.633, -0.388] | 100.0 |
| 1h | BRK_tap127_first | EXP_COUNTER | both | -0.557 | -0.175 [-0.289, -0.057] | 5.0 | -0.691 | -0.327 [-0.650, -0.146] | 10.0 | -0.663 | -0.250 [-0.460, -0.058] | 5.0 | -0.731 | +0.208 [-0.584, +0.532] | 15.0 |
| 1h | BRK_tap127_first | EXP_COUNTER | long | -0.542 | -0.045 [-0.245, +0.195] | 5.0 | -0.933 | -0.240 [-0.620, +0.077] | 5.0 | -1.033 | -0.493 [-0.604, -0.037] | 5.0 | -1.743 | -0.679 [-1.229, +0.048] | 10.0 |
| 1h | BRK_tap127_first | EXP_COUNTER | short | -0.598 | -0.394 [-0.601, -0.112] | 30.0 | -0.674 | -0.504 [-0.842, -0.127] | 35.0 | -0.063 | +0.036 [-0.436, +0.438] | 45.0 | -0.272 | +1.015 [-0.172, +1.811] | 20.0 |
| 1h | BRK_tap127_first | IN_RANGE_COINCIDENT* | both | +0.365 | -0.340 [-1.300, +0.489] | 62.5 | +2.288 | -2.720 [-3.866, -1.195] | 93.8 | +0.379 | -0.294 [-0.860, -0.032] | 80.0 | +2.302 | -2.587 [-2.854, -1.605] | 100.0 |
| 1h | BRK_tap127_first | IN_RANGE_COINCIDENT* | long | -0.408 | -0.860 [-2.423, -0.294] | 55.6 | +5.845 | -2.854 [-5.240, -1.459] | 100.0 | — | -0.577 [-0.978, +0.039] | — | — | -2.720 [-2.959, -2.305] | — |
| 1h | BRK_tap127_first | IN_RANGE_COINCIDENT* | short | +0.516 | +0.442 [-0.340, +0.669] | 66.7 | +1.587 | -2.335 [-3.423, +1.794] | 66.7 | +0.379 | -0.032 [-0.032, -0.032] | 100.0 | +2.302 | -1.605 [-1.605, -1.605] | 100.0 |
| 1h | BRK_tap127_first | IN_RANGE_MID* | both | -0.134 | -0.049 [-0.131, -0.001] | 20.0 | +0.109 | -0.058 [-0.404, +0.248] | 65.0 | -0.352 | -0.141 [-0.453, +0.011] | 35.0 | +0.149 | +0.195 [-0.242, +0.626] | 45.0 |
| 1h | BRK_tap127_first | IN_RANGE_MID* | long | -0.362 | -0.141 [-0.232, -0.065] | 15.0 | +0.159 | -0.293 [-0.437, +0.121] | 80.0 | -0.634 | -0.277 [-0.473, -0.097] | 15.0 | -0.166 | +0.248 [-0.560, +0.776] | 45.0 |
| 1h | BRK_tap127_first | IN_RANGE_MID* | short | +0.029 | +0.071 [-0.052, +0.201] | 45.0 | +0.063 | -0.011 [-0.549, +0.310] | 60.0 | -0.184 | -0.296 [-0.440, +0.208] | 55.0 | +0.348 | +0.107 [-0.496, +0.350] | 75.0 |
| 1h | BRK_tap127_first | IN_RANGE_OTHER | both | +0.018 | -0.064 [-0.279, +0.098] | 65.0 | -0.840 | -0.504 [-0.672, -0.376] | 20.0 | +0.178 | +0.152 [-0.199, +0.437] | 55.0 | -0.881 | -0.612 [-1.203, +0.639] | 30.0 |
| 1h | BRK_tap127_first | IN_RANGE_OTHER | long | -0.192 | -0.510 [-0.786, -0.369] | 85.0 | -0.543 | +0.541 [-0.396, +1.029] | 15.0 | -0.192 | -0.024 [-0.390, +0.358] | 45.0 | -0.825 | +3.632 [+2.533, +4.755] | 15.0 |
| 1h | BRK_tap127_first | IN_RANGE_OTHER | short | +0.098 | +0.157 [+0.055, +0.313] | 45.0 | -0.883 | -0.845 [-1.116, -0.572] | 45.0 | +0.547 | +0.074 [-0.462, +0.665] | 70.0 | -0.897 | -1.623 [-2.177, -0.984] | 75.0 |
| 1h | BRK_tap127_first | NONE | both | -0.192 | -0.361 [-1.724, +0.079] | 65.6 | -6.974 | -3.810 [-6.889, -2.721] | 21.9 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_first | NONE | long | -0.192 | +0.079 [-0.361, +0.079] | 38.9 | -6.974 | -6.974 [-6.985, -6.861] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_first | NONE | short | — | -1.724 [-1.724, -1.601] | — | — | -2.721 [-2.721, -1.500] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_oneshot | ALL | both | -0.314 | -0.157 [-0.225, -0.092] | 0.0 | -0.303 | -0.207 [-0.423, +0.043] | 40.0 | -0.491 | -0.277 [-0.369, -0.185] | 5.0 | -0.678 | -0.354 [-0.621, -0.269] | 20.0 |
| 1h | BRK_tap127_oneshot | ALL | long | -0.264 | -0.123 [-0.161, -0.078] | 5.0 | -0.144 | +0.049 [-0.121, +0.258] | 25.0 | -0.687 | -0.237 [-0.367, -0.140] | 0.0 | -1.198 | -0.329 [-0.609, -0.039] | 10.0 |
| 1h | BRK_tap127_oneshot | ALL | short | -0.360 | -0.206 [-0.336, -0.117] | 25.0 | -0.564 | -0.452 [-0.799, -0.348] | 40.0 | -0.319 | -0.299 [-0.395, -0.244] | 45.0 | -0.015 | -0.375 [-0.620, -0.109] | 85.0 |
| 1h | BRK_tap127_oneshot | EXP_ALIGNED* | both | -0.313 | -0.201 [-0.270, -0.136] | 17.5 | -0.081 | -0.052 [-0.167, +0.079] | 40.0 | -0.409 | -0.209 [-0.336, -0.151] | 20.0 | -0.365 | -0.383 [-0.561, -0.030] | 50.0 |
| 1h | BRK_tap127_oneshot | EXP_ALIGNED* | long | -0.105 | -0.057 [-0.121, +0.031] | 35.0 | +0.171 | +0.324 [+0.209, +0.478] | 20.0 | -0.229 | -0.120 [-0.145, -0.035] | 20.0 | -1.157 | -0.124 [-0.724, +0.024] | 10.0 |
| 1h | BRK_tap127_oneshot | EXP_ALIGNED* | short | -0.573 | -0.433 [-0.494, -0.411] | 15.0 | -0.544 | -0.549 [-0.983, -0.383] | 50.0 | -0.822 | -0.448 [-0.575, -0.387] | 15.0 | +0.135 | -0.512 [-0.657, -0.338] | 85.0 |
| 1h | BRK_tap127_oneshot | EXP_COUNTER | both | -0.647 | -0.254 [-0.384, +0.039] | 0.0 | -0.922 | -0.470 [-0.726, -0.289] | 10.0 | -0.863 | -0.518 [-0.595, -0.244] | 0.0 | -1.205 | -0.152 [-0.704, +0.560] | 10.0 |
| 1h | BRK_tap127_oneshot | EXP_COUNTER | long | -0.817 | -0.132 [-0.484, +0.167] | 5.0 | -1.634 | -0.615 [-1.020, -0.100] | 5.0 | -1.395 | -0.610 [-0.874, -0.320] | 0.0 | -2.424 | -1.226 [-1.655, -0.609] | 10.0 |
| 1h | BRK_tap127_oneshot | EXP_COUNTER | short | -0.571 | -0.282 [-0.470, -0.086] | 20.0 | -0.448 | -0.267 [-0.712, +0.170] | 40.0 | -0.150 | -0.184 [-0.514, +0.252] | 50.0 | -0.176 | +1.190 [-0.016, +1.807] | 20.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | both | +0.115 | -0.317 [-1.604, +0.495] | 58.3 | +3.352 | -2.595 [-3.866, -1.195] | 100.0 | — | -0.032 [-0.163, +0.504] | — | — | -2.854 [-3.064, -2.229] | — |
| 1h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | long | -0.408 | -1.359 [-2.901, +0.417] | 50.0 | +5.845 | -3.064 [-4.748, -1.655] | 100.0 | — | +0.373 [+0.039, +0.707] | — | — | -3.064 [-3.169, -2.959] | — |
| 1h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | short | +0.658 | +0.442 [-0.815, +0.442] | 85.7 | +0.878 | -2.335 [-3.212, -1.673] | 85.7 | — | -0.032 [-0.032, -0.032] | — | — | -1.605 [-1.605, -1.605] | — |
| 1h | BRK_tap127_oneshot | IN_RANGE_MID* | both | -0.269 | -0.142 [-0.180, -0.023] | 10.0 | +0.038 | -0.131 [-0.544, +0.177] | 65.0 | -0.535 | -0.303 [-0.567, -0.185] | 30.0 | -0.656 | -0.407 [-0.986, +0.386] | 35.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_MID* | long | -0.381 | -0.131 [-0.300, -0.086] | 10.0 | +0.350 | -0.097 [-0.472, +0.149] | 75.0 | -0.903 | -0.450 [-0.761, -0.101] | 10.0 | -0.968 | -0.320 [-1.130, +0.708] | 30.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_MID* | short | -0.012 | -0.080 [-0.271, +0.046] | 60.0 | -0.076 | -0.260 [-0.845, +0.111] | 55.0 | -0.299 | -0.349 [-0.737, +0.047] | 55.0 | +0.198 | -0.293 [-1.221, +0.207] | 75.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_OTHER | both | -0.033 | +0.012 [-0.191, +0.181] | 45.0 | -0.858 | +0.024 [-0.637, +0.451] | 20.0 | +0.061 | -0.021 [-0.297, +0.613] | 55.0 | -0.854 | -0.119 [-0.897, +1.695] | 35.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_OTHER | long | -0.375 | -0.400 [-0.665, -0.204] | 50.0 | -0.794 | +1.155 [+0.523, +1.515] | 5.0 | -0.407 | -0.095 [-0.543, +0.532] | 30.0 | -0.825 | +4.098 [+1.952, +5.364] | 15.0 |
| 1h | BRK_tap127_oneshot | IN_RANGE_OTHER | short | +0.089 | +0.187 [+0.000, +0.424] | 40.0 | -0.955 | -0.767 [-1.069, -0.090] | 40.0 | +0.697 | +0.428 [-0.478, +0.736] | 65.0 | -0.937 | -1.648 [-2.287, -1.019] | 75.0 |
| 1h | BRK_tap127_oneshot | NONE | both | -0.192 | -0.361 [-1.724, +0.079] | 65.6 | -6.974 | -3.810 [-6.889, -2.721] | 21.9 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_oneshot | NONE | long | -0.192 | +0.079 [-0.361, +0.079] | 38.9 | -6.974 | -6.974 [-6.985, -6.861] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap127_oneshot | NONE | short | — | -1.724 [-1.724, -1.601] | — | — | -2.721 [-2.721, -1.500] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_first | ALL | both | -0.104 | -0.105 [-0.191, -0.062] | 50.0 | -0.039 | -0.029 [-0.195, +0.056] | 50.0 | -0.388 | -0.233 [-0.338, -0.158] | 25.0 | -0.360 | +0.110 [-0.280, +0.190] | 25.0 |
| 1h | BRK_tap200_first | ALL | long | -0.143 | -0.100 [-0.146, -0.066] | 25.0 | +0.157 | +0.243 [-0.012, +0.411] | 45.0 | -0.545 | -0.261 [-0.385, -0.169] | 15.0 | -0.776 | -0.058 [-0.358, +0.180] | 10.0 |
| 1h | BRK_tap200_first | ALL | short | -0.065 | -0.137 [-0.237, -0.048] | 70.0 | -0.407 | -0.462 [-0.649, -0.281] | 60.0 | -0.196 | -0.214 [-0.365, -0.066] | 55.0 | +0.105 | +0.069 [-0.362, +0.449] | 55.0 |
| 1h | BRK_tap200_first | EXP_ALIGNED* | both | +0.110 | +0.028 [-0.040, +0.076] | 80.0 | +0.156 | +0.199 [+0.011, +0.409] | 45.0 | -0.283 | -0.123 [-0.256, +0.052] | 20.0 | +0.122 | +0.176 [-0.085, +0.640] | 40.0 |
| 1h | BRK_tap200_first | EXP_ALIGNED* | long | +0.174 | +0.095 [+0.005, +0.208] | 65.0 | +0.616 | +0.898 [+0.768, +1.074] | 10.0 | -0.063 | -0.022 [-0.068, +0.076] | 25.0 | -0.103 | +0.093 [+0.002, +0.605] | 10.0 |
| 1h | BRK_tap200_first | EXP_ALIGNED* | short | -0.187 | -0.391 [-0.460, -0.020] | 60.0 | -0.223 | -0.761 [-0.972, -0.465] | 80.0 | -0.615 | -0.258 [-0.480, +0.179] | 20.0 | +0.729 | +0.074 [-0.716, +0.761] | 70.0 |
| 1h | BRK_tap200_first | EXP_COUNTER | both | -0.295 | -0.265 [-0.408, -0.108] | 50.0 | -0.840 | -0.738 [-0.845, -0.298] | 25.0 | -0.579 | -0.449 [-0.780, -0.181] | 40.0 | -0.936 | -0.327 [-0.585, +0.216] | 10.0 |
| 1h | BRK_tap200_first | EXP_COUNTER | long | -0.143 | -0.194 [-0.440, -0.023] | 55.0 | -0.640 | -0.720 [-0.874, -0.255] | 55.0 | -1.009 | -0.596 [-1.054, -0.523] | 30.0 | -0.938 | -0.869 [-1.002, -0.587] | 25.0 |
| 1h | BRK_tap200_first | EXP_COUNTER | short | -0.480 | -0.429 [-0.542, -0.270] | 45.0 | -0.879 | -0.641 [-0.945, -0.224] | 35.0 | -0.151 | -0.127 [-0.473, -0.023] | 45.0 | -0.775 | +1.154 [+0.041, +1.520] | 10.0 |
| 1h | BRK_tap200_first | IN_RANGE_COINCIDENT* | both | +0.359 | -0.947 [-1.550, -0.239] | 80.0 | +2.282 | -1.519 [-4.122, +0.311] | 85.0 | +0.379 | +0.218 [-1.167, +0.802] | 66.7 | +2.302 | -3.079 [-5.605, -1.566] | 100.0 |
| 1h | BRK_tap200_first | IN_RANGE_COINCIDENT* | long | -0.408 | -1.167 [-2.283, -0.219] | 66.7 | +5.845 | +0.311 [-1.566, +0.594] | 88.9 | — | -3.342 [-4.504, -2.254] | — | — | -1.566 [-3.585, -0.771] | — |
| 1h | BRK_tap200_first | IN_RANGE_COINCIDENT* | short | +2.851 | -0.340 [-1.462, +0.669] | 100.0 | +1.050 | -2.335 [-3.423, -1.011] | 88.2 | +0.379 | +0.545 [+0.235, +1.335] | 50.0 | +2.302 | -3.365 [-7.668, -2.868] | 100.0 |
| 1h | BRK_tap200_first | IN_RANGE_MID* | both | -0.279 | -0.162 [-0.268, -0.127] | 20.0 | +0.268 | +0.023 [-0.262, +0.091] | 95.0 | -0.395 | -0.210 [-0.391, -0.100] | 25.0 | +0.110 | +0.260 [-0.357, +0.682] | 45.0 |
| 1h | BRK_tap200_first | IN_RANGE_MID* | long | -0.513 | -0.264 [-0.325, -0.198] | 0.0 | +0.376 | -0.068 [-0.363, +0.084] | 85.0 | -0.756 | -0.226 [-0.371, -0.162] | 15.0 | -0.022 | +0.465 [-0.257, +0.922] | 40.0 |
| 1h | BRK_tap200_first | IN_RANGE_MID* | short | +0.023 | -0.058 [-0.212, +0.020] | 75.0 | +0.233 | +0.079 [-0.246, +0.127] | 85.0 | -0.064 | -0.321 [-0.480, -0.019] | 70.0 | +0.293 | +0.086 [-0.634, +0.524] | 65.0 |
| 1h | BRK_tap200_first | IN_RANGE_OTHER | both | +0.213 | +0.051 [-0.043, +0.134] | 85.0 | -0.715 | -0.420 [-0.544, +0.183] | 20.0 | -0.773 | -0.077 [-0.497, +0.136] | 20.0 | -3.813 | -2.747 [-3.683, -0.582] | 10.0 |
| 1h | BRK_tap200_first | IN_RANGE_OTHER | long | +0.006 | -0.226 [-0.987, -0.017] | 80.0 | +0.165 | +0.735 [+0.112, +0.967] | 30.0 | -2.418 | -1.166 [-1.975, +0.830] | 20.0 | -4.571 | -4.508 [-5.575, +1.874] | 50.0 |
| 1h | BRK_tap200_first | IN_RANGE_OTHER | short | +0.445 | +0.233 [+0.115, +0.420] | 85.0 | -0.827 | -0.790 [-1.429, -0.272] | 45.0 | +0.079 | -0.114 [-0.454, +0.096] | 75.0 | -3.736 | -2.306 [-3.397, -1.274] | 10.0 |
| 1h | BRK_tap200_first | NONE | both | -0.948 | +9.091 [-0.948, +9.091] | 19.2 | -7.992 | +6.837 [-7.992, +6.837] | 19.2 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_first | NONE | long | -0.948 | -0.948 [-0.948, -0.948] | 50.0 | -7.992 | -7.992 [-7.992, -7.992] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_first | NONE | short | — | +9.091 [+9.091, +9.091] | — | — | +6.837 [+6.837, +6.837] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_oneshot | ALL | both | -0.105 | -0.088 [-0.147, -0.041] | 45.0 | -0.090 | -0.017 [-0.222, +0.089] | 45.0 | -0.467 | -0.154 [-0.230, -0.098] | 5.0 | -0.338 | +0.141 [-0.056, +0.236] | 10.0 |
| 1h | BRK_tap200_oneshot | ALL | long | -0.112 | -0.120 [-0.155, -0.058] | 55.0 | +0.184 | +0.369 [+0.128, +0.525] | 30.0 | -0.674 | -0.188 [-0.383, -0.140] | 0.0 | -0.801 | +0.022 [-0.179, +0.252] | 0.0 |
| 1h | BRK_tap200_oneshot | ALL | short | -0.102 | -0.087 [-0.268, +0.044] | 45.0 | -0.460 | -0.597 [-0.674, -0.326] | 60.0 | -0.187 | -0.065 [-0.258, +0.077] | 35.0 | +0.105 | +0.154 [-0.046, +0.654] | 40.0 |
| 1h | BRK_tap200_oneshot | EXP_ALIGNED* | both | +0.083 | +0.006 [-0.103, +0.071] | 75.0 | +0.126 | +0.328 [-0.019, +0.594] | 40.0 | -0.229 | -0.085 [-0.205, +0.071] | 20.0 | +0.089 | +0.189 [-0.023, +0.703] | 35.0 |
| 1h | BRK_tap200_oneshot | EXP_ALIGNED* | long | +0.140 | +0.059 [-0.015, +0.151] | 65.0 | +0.550 | +0.888 [+0.739, +1.061] | 15.0 | -0.062 | -0.046 [-0.102, +0.073] | 45.0 | -0.103 | +0.081 [-0.099, +1.009] | 25.0 |
| 1h | BRK_tap200_oneshot | EXP_ALIGNED* | short | -0.108 | -0.037 [-0.455, +0.137] | 35.0 | -0.222 | -0.690 [-0.883, -0.035] | 55.0 | -0.573 | -0.185 [-0.465, +0.242] | 20.0 | +0.821 | +0.318 [-0.704, +0.619] | 80.0 |
| 1h | BRK_tap200_oneshot | EXP_COUNTER | both | -0.420 | -0.393 [-0.442, -0.191] | 30.0 | -0.894 | -0.728 [-0.851, -0.210] | 10.0 | -0.986 | -0.467 [-0.752, -0.203] | 15.0 | -0.827 | -0.142 [-0.410, +0.619] | 10.0 |
| 1h | BRK_tap200_oneshot | EXP_COUNTER | long | -0.146 | -0.322 [-0.450, -0.053] | 60.0 | -0.643 | -0.704 [-0.943, -0.129] | 55.0 | -1.157 | -0.951 [-1.070, -0.497] | 20.0 | -0.926 | -0.460 [-0.897, -0.290] | 20.0 |
| 1h | BRK_tap200_oneshot | EXP_COUNTER | short | -0.615 | -0.458 [-0.676, -0.236] | 30.0 | -1.026 | -0.641 [-0.935, -0.185] | 10.0 | -0.359 | -0.288 [-0.491, +0.010] | 45.0 | -0.583 | +0.887 [-0.104, +1.317] | 15.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | both | +2.464 | -0.925 [-1.813, -0.006] | 88.2 | +2.828 | -1.566 [-3.792, +1.113] | 76.5 | — | +0.164 [-0.848, +0.656] | — | — | -3.224 [-5.116, -1.874] | — |
| 1h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | long | -0.408 | -0.587 [-2.996, +0.467] | 50.0 | +5.845 | +1.038 [-2.485, +2.012] | 87.5 | — | -3.417 [-4.542, -2.292] | — | — | -3.585 [-4.595, -2.576] | — |
| 1h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | short | +5.343 | -0.559 [-1.786, +0.442] | 100.0 | -0.182 | -2.335 [-3.494, -1.057] | 78.6 | — | +0.510 [+0.191, +0.980] | — | — | -3.224 [-4.990, -1.922] | — |
| 1h | BRK_tap200_oneshot | IN_RANGE_MID* | both | -0.279 | -0.150 [-0.207, -0.040] | 15.0 | +0.196 | -0.005 [-0.223, +0.155] | 75.0 | -0.443 | -0.058 [-0.238, +0.080] | 15.0 | +0.057 | +0.460 [-0.136, +0.800] | 30.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_MID* | long | -0.578 | -0.241 [-0.298, -0.116] | 0.0 | +0.669 | +0.114 [-0.037, +0.413] | 100.0 | -0.869 | -0.197 [-0.348, +0.075] | 5.0 | -0.805 | +0.264 [-0.441, +1.091] | 0.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_MID* | short | +0.142 | -0.089 [-0.218, +0.130] | 80.0 | +0.046 | -0.039 [-0.526, +0.140] | 65.0 | +0.055 | -0.041 [-0.184, +0.236] | 65.0 | +0.457 | +0.172 [-0.246, +0.659] | 55.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_OTHER | both | +0.181 | +0.109 [+0.037, +0.212] | 65.0 | -0.784 | -0.277 [-0.469, +0.153] | 10.0 | -0.773 | -0.029 [-0.599, +0.222] | 25.0 | -3.813 | -1.687 [-2.915, -0.286] | 5.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_OTHER | long | -0.209 | -0.223 [-0.868, +0.167] | 55.0 | +0.165 | +1.120 [+0.706, +1.207] | 20.0 | -2.418 | -0.533 [-2.152, +0.280] | 20.0 | -4.571 | -0.521 [-3.258, +1.990] | 25.0 |
| 1h | BRK_tap200_oneshot | IN_RANGE_OTHER | short | +0.416 | +0.193 [+0.093, +0.418] | 75.0 | -1.232 | -0.788 [-1.020, -0.477] | 25.0 | +0.079 | +0.010 [-0.756, +0.300] | 55.0 | -3.736 | -1.935 [-3.394, -0.913] | 5.0 |
| 1h | BRK_tap200_oneshot | NONE | both | -0.948 | +9.091 [-0.948, +9.091] | 19.2 | -7.992 | +6.837 [-7.992, +6.837] | 19.2 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_oneshot | NONE | long | -0.948 | -0.948 [-0.948, -0.948] | 50.0 | -7.992 | -7.992 [-7.992, -7.992] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_tap200_oneshot | NONE | short | — | +9.091 [+9.091, +9.091] | — | — | +6.837 [+6.837, +6.837] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_first | ALL | both | -0.314 | -0.161 [-0.234, -0.127] | 0.0 | -0.410 | -0.355 [-0.429, -0.179] | 35.0 | -0.276 | -0.277 [-0.402, -0.118] | 50.0 | -0.526 | -0.291 [-0.633, -0.198] | 30.0 |
| 1h | BRK_mem_first | ALL | long | -0.328 | -0.105 [-0.144, -0.045] | 0.0 | -0.102 | -0.054 [-0.245, +0.003] | 40.0 | -0.386 | -0.306 [-0.480, -0.106] | 30.0 | -0.683 | -0.421 [-0.747, -0.035] | 30.0 |
| 1h | BRK_mem_first | ALL | short | -0.298 | -0.274 [-0.323, -0.184] | 40.0 | -0.734 | -0.650 [-0.795, -0.303] | 35.0 | -0.144 | -0.221 [-0.465, -0.054] | 60.0 | -0.348 | -0.461 [-0.788, +0.141] | 60.0 |
| 1h | BRK_mem_first | EXP_ALIGNED* | both | -0.441 | -0.138 [-0.216, -0.030] | 0.0 | -0.402 | -0.450 [-0.571, -0.300] | 60.0 | -0.446 | -0.156 [-0.442, -0.017] | 25.0 | -0.166 | -0.847 [-1.035, -0.363] | 80.0 |
| 1h | BRK_mem_first | EXP_ALIGNED* | long | -0.332 | -0.084 [-0.196, +0.023] | 15.0 | +0.154 | -0.253 [-0.348, -0.153] | 80.0 | -0.376 | -0.281 [-0.515, -0.096] | 45.0 | +0.331 | -0.637 [-1.548, -0.216] | 95.0 |
| 1h | BRK_mem_first | EXP_ALIGNED* | short | -0.697 | -0.201 [-0.415, +0.005] | 0.0 | -0.901 | -0.742 [-0.917, -0.408] | 30.0 | -0.588 | -0.026 [-0.416, +0.286] | 15.0 | -0.298 | -0.720 [-1.147, +0.567] | 55.0 |
| 1h | BRK_mem_first | EXP_COUNTER | both | -0.239 | -0.192 [-0.358, +0.002] | 45.0 | -0.625 | -0.266 [-0.536, +0.064] | 25.0 | -0.318 | -0.306 [-0.436, +0.157] | 50.0 | -0.361 | -0.326 [-0.770, +0.041] | 45.0 |
| 1h | BRK_mem_first | EXP_COUNTER | long | -0.257 | -0.273 [-0.392, +0.041] | 50.0 | -0.178 | +0.027 [-0.460, +0.569] | 40.0 | -1.215 | -0.242 [-0.558, +0.145] | 0.0 | -0.597 | -0.232 [-1.184, +0.605] | 35.0 |
| 1h | BRK_mem_first | EXP_COUNTER | short | -0.110 | -0.253 [-0.353, -0.053] | 70.0 | -0.734 | -0.459 [-0.758, -0.015] | 30.0 | +0.223 | -0.220 [-0.643, +0.381] | 65.0 | -0.279 | +0.486 [-0.821, +0.911] | 35.0 |
| 1h | BRK_mem_first | IN_RANGE_COINCIDENT* | both | -1.202 | -0.484 [-1.179, +0.233] | 25.0 | +0.276 | -0.320 [-3.332, +1.187] | 60.0 | -0.291 | -1.215 [-2.372, +0.332] | 58.3 | +1.730 | +0.295 [-2.317, +1.304] | 75.0 |
| 1h | BRK_mem_first | IN_RANGE_COINCIDENT* | long | -1.426 | -0.872 [-1.875, +0.046] | 35.0 | +0.246 | -0.168 [-2.906, +2.553] | 60.0 | -0.205 | -0.928 [-2.711, +0.212] | 63.6 | +0.975 | -0.736 [-2.722, +1.381] | 72.7 |
| 1h | BRK_mem_first | IN_RANGE_COINCIDENT* | short | -0.265 | -0.171 [-0.997, +0.501] | 50.0 | +0.484 | -0.978 [-3.740, +0.417] | 81.2 | -0.295 | -0.669 [-3.207, +0.734] | 50.0 | +2.637 | +0.007 [-1.895, +3.926] | 66.7 |
| 1h | BRK_mem_first | IN_RANGE_MID* | both | -0.380 | -0.162 [-0.238, -0.017] | 10.0 | -0.444 | -0.298 [-0.639, +0.077] | 35.0 | -0.449 | -0.363 [-0.601, -0.063] | 45.0 | -1.004 | -0.278 [-0.696, +0.452] | 15.0 |
| 1h | BRK_mem_first | IN_RANGE_MID* | long | -0.318 | -0.040 [-0.162, +0.144] | 5.0 | -0.434 | -0.131 [-0.436, +0.212] | 25.0 | -0.439 | -0.291 [-0.527, -0.019] | 30.0 | -0.886 | +0.220 [-0.390, +0.734] | 15.0 |
| 1h | BRK_mem_first | IN_RANGE_MID* | short | -0.537 | -0.294 [-0.434, -0.130] | 15.0 | -0.552 | -0.408 [-1.110, +0.025] | 45.0 | -0.536 | -0.402 [-0.863, -0.103] | 45.0 | -1.211 | -0.635 [-1.631, -0.175] | 30.0 |
| 1h | BRK_mem_first | IN_RANGE_OTHER | both | -0.108 | -0.157 [-0.259, -0.001] | 55.0 | -0.235 | -0.130 [-0.264, -0.019] | 30.0 | +0.162 | -0.296 [-0.436, +0.210] | 70.0 | -0.954 | -0.148 [-0.520, +0.055] | 15.0 |
| 1h | BRK_mem_first | IN_RANGE_OTHER | long | -0.277 | -0.016 [-0.288, +0.183] | 30.0 | -0.091 | -0.094 [-0.255, +0.502] | 50.0 | +0.138 | -0.380 [-0.781, +0.387] | 60.0 | -1.739 | -0.241 [-0.746, +0.141] | 10.0 |
| 1h | BRK_mem_first | IN_RANGE_OTHER | short | +0.002 | -0.279 [-0.428, -0.036] | 80.0 | -0.371 | -0.477 [-0.729, -0.178] | 60.0 | +0.345 | -0.053 [-0.597, +0.183] | 85.0 | -0.815 | -0.126 [-0.604, +0.354] | 20.0 |
| 1h | BRK_mem_first | NONE | both | -1.525 | -0.505 [-0.906, -0.338] | 5.6 | -3.884 | -3.024 [-3.860, -1.266] | 22.2 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_first | NONE | long | -1.428 | +0.004 [-0.538, +0.470] | 0.0 | -10.168 | -3.183 [-7.168, -1.701] | 0.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_first | NONE | short | -1.501 | -0.879 [-1.501, -0.344] | 22.7 | -3.860 | -3.666 [-3.783, +4.031] | 13.6 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_oneshot | ALL | both | -0.289 | -0.161 [-0.191, -0.095] | 5.0 | -0.380 | -0.234 [-0.362, -0.007] | 20.0 | -0.283 | -0.277 [-0.385, -0.093] | 45.0 | -0.528 | -0.186 [-0.510, +0.181] | 25.0 |
| 1h | BRK_mem_oneshot | ALL | long | -0.248 | -0.115 [-0.199, +0.011] | 5.0 | -0.185 | +0.026 [-0.253, +0.179] | 35.0 | -0.380 | -0.315 [-0.557, -0.151] | 40.0 | -1.011 | -0.314 [-0.640, +0.032] | 15.0 |
| 1h | BRK_mem_oneshot | ALL | short | -0.320 | -0.211 [-0.291, -0.146] | 20.0 | -0.585 | -0.485 [-0.643, -0.265] | 40.0 | -0.165 | -0.183 [-0.377, +0.038] | 55.0 | -0.105 | -0.182 [-0.601, +0.396] | 55.0 |
| 1h | BRK_mem_oneshot | EXP_ALIGNED* | both | -0.315 | -0.028 [-0.209, +0.065] | 5.0 | -0.293 | -0.386 [-0.510, -0.100] | 65.0 | -0.249 | -0.098 [-0.258, +0.173] | 40.0 | -0.163 | -0.407 [-0.785, -0.020] | 70.0 |
| 1h | BRK_mem_oneshot | EXP_ALIGNED* | long | -0.166 | +0.015 [-0.111, +0.244] | 15.0 | +0.237 | -0.102 [-0.366, +0.232] | 75.0 | -0.225 | -0.165 [-0.375, +0.265] | 35.0 | -0.203 | -0.810 [-1.640, -0.043] | 65.0 |
| 1h | BRK_mem_oneshot | EXP_ALIGNED* | short | -0.486 | -0.198 [-0.414, +0.052] | 10.0 | -0.841 | -0.685 [-1.054, -0.439] | 40.0 | -0.345 | +0.087 [-0.243, +0.344] | 25.0 | -0.162 | -0.135 [-1.125, +0.377] | 50.0 |
| 1h | BRK_mem_oneshot | EXP_COUNTER | both | -0.192 | -0.280 [-0.392, -0.122] | 60.0 | -0.545 | -0.319 [-0.489, -0.076] | 20.0 | -0.318 | -0.312 [-0.640, +0.141] | 50.0 | -0.468 | -0.250 [-0.490, +0.440] | 30.0 |
| 1h | BRK_mem_oneshot | EXP_COUNTER | long | -0.186 | -0.220 [-0.465, -0.055] | 50.0 | -0.406 | +0.082 [-0.576, +0.535] | 35.0 | -0.546 | -0.415 [-0.708, -0.158] | 35.0 | -0.509 | -0.313 [-1.011, +0.546] | 40.0 |
| 1h | BRK_mem_oneshot | EXP_COUNTER | short | -0.163 | -0.288 [-0.418, -0.099] | 70.0 | -0.681 | -0.587 [-0.922, +0.028] | 40.0 | +0.093 | -0.292 [-0.668, +0.522] | 60.0 | -0.319 | +0.541 [-0.768, +1.286] | 30.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | both | -1.025 | +0.003 [-0.627, +0.477] | 20.0 | +0.246 | +0.604 [-3.242, +2.680] | 45.0 | -0.268 | -1.190 [-1.511, +0.690] | 53.8 | +1.824 | -0.855 [-3.185, +1.636] | 76.9 |
| 1h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | long | -1.426 | -0.512 [-1.254, +0.366] | 25.0 | +0.246 | -0.182 [-3.318, +2.350] | 55.0 | -0.205 | +0.211 [-1.429, +0.609] | 46.2 | +0.975 | -1.847 [-3.253, +2.659] | 69.2 |
| 1h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | short | -0.242 | +0.070 [-0.453, +1.395] | 43.8 | -0.195 | -1.046 [-3.095, +1.499] | 50.0 | -0.272 | -0.165 [-1.591, +0.732] | 42.9 | +2.781 | +0.899 [-2.341, +6.590] | 57.1 |
| 1h | BRK_mem_oneshot | IN_RANGE_MID* | both | -0.347 | -0.169 [-0.239, -0.019] | 10.0 | -0.438 | -0.236 [-0.543, +0.257] | 35.0 | -0.469 | -0.390 [-0.665, -0.161] | 45.0 | -0.622 | +0.076 [-0.766, +0.909] | 30.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_MID* | long | -0.280 | -0.033 [-0.187, +0.173] | 15.0 | -0.561 | -0.184 [-0.512, +0.307] | 20.0 | -0.438 | -0.255 [-0.657, +0.138] | 40.0 | -2.090 | +0.286 [-0.726, +1.057] | 0.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_MID* | short | -0.469 | -0.175 [-0.365, -0.082] | 5.0 | -0.360 | -0.355 [-0.815, +0.182] | 45.0 | -0.655 | -0.302 [-0.656, -0.053] | 25.0 | +0.122 | -0.428 [-0.915, +0.156] | 75.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_OTHER | both | -0.251 | -0.093 [-0.277, +0.076] | 30.0 | -0.161 | +0.007 [-0.153, +0.219] | 25.0 | +0.103 | -0.321 [-0.696, -0.124] | 80.0 | -1.873 | -0.021 [-0.248, +0.363] | 5.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_OTHER | long | -0.319 | -0.165 [-0.296, +0.138] | 20.0 | -0.318 | +0.059 [-0.165, +0.644] | 15.0 | +0.121 | -0.449 [-1.123, +0.133] | 70.0 | -2.137 | -0.050 [-0.457, +0.255] | 5.0 |
| 1h | BRK_mem_oneshot | IN_RANGE_OTHER | short | -0.136 | -0.297 [-0.373, +0.185] | 65.0 | -0.110 | +0.057 [-0.501, +0.512] | 45.0 | -0.012 | -0.131 [-0.502, +0.394] | 55.0 | -0.912 | -0.204 [-0.921, +0.507] | 25.0 |
| 1h | BRK_mem_oneshot | NONE | both | -1.525 | -0.544 [-1.501, +0.010] | 6.2 | -3.884 | -3.024 [-3.860, -1.382] | 18.8 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_oneshot | NONE | long | -1.428 | -0.170 [-0.541, +0.352] | 0.0 | -10.168 | -2.874 [-6.922, -1.670] | 0.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | BRK_mem_oneshot | NONE | short | -1.501 | -1.501 [-1.501, -1.066] | 37.5 | -3.860 | -3.363 [-3.860, +2.131] | 25.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | SFP_harden | ALL | both | -0.103 | -0.075 [-0.118, -0.040] | 40.0 | -0.007 | -0.131 [-0.329, +0.106] | 60.0 | -0.309 | -0.159 [-0.237, -0.039] | 10.0 | -0.387 | -0.126 [-0.459, +0.012] | 35.0 |
| 1h | SFP_harden | ALL | long | -0.040 | -0.064 [-0.096, -0.015] | 65.0 | -0.164 | +0.091 [-0.095, +0.356] | 25.0 | -0.408 | -0.142 [-0.280, -0.055] | 5.0 | -0.820 | -0.092 [-0.408, +0.250] | 10.0 |
| 1h | SFP_harden | ALL | short | -0.130 | -0.082 [-0.215, -0.037] | 45.0 | +0.152 | -0.169 [-0.519, +0.053] | 90.0 | -0.228 | -0.153 [-0.349, -0.046] | 35.0 | +0.204 | -0.171 [-0.542, +0.163] | 80.0 |
| 1h | SFP_harden | EXP_ALIGNED* | both | -0.240 | -0.071 [-0.192, +0.115] | 25.0 | -0.054 | -0.098 [-0.484, +0.180] | 55.0 | -0.392 | -0.148 [-0.464, +0.190] | 30.0 | -0.069 | -0.368 [-0.843, +0.386] | 60.0 |
| 1h | SFP_harden | EXP_ALIGNED* | long | -0.393 | -0.105 [-0.144, +0.045] | 10.0 | -0.363 | +0.347 [-0.298, +0.588] | 25.0 | -0.491 | -0.297 [-0.618, +0.029] | 30.0 | -0.746 | -0.496 [-0.979, +0.497] | 40.0 |
| 1h | SFP_harden | EXP_ALIGNED* | short | -0.079 | -0.158 [-0.357, +0.240] | 60.0 | +0.576 | -0.423 [-0.729, +0.144] | 85.0 | -0.247 | -0.082 [-0.393, +0.325] | 45.0 | +0.615 | -0.543 [-1.273, +0.393] | 75.0 |
| 1h | SFP_harden | EXP_COUNTER | both | +0.097 | -0.023 [-0.087, +0.139] | 70.0 | +0.643 | +0.201 [-0.309, +0.324] | 95.0 | +0.116 | -0.018 [-0.175, +0.076] | 85.0 | +0.982 | +0.228 [-0.067, +0.631] | 90.0 |
| 1h | SFP_harden | EXP_COUNTER | long | +0.158 | -0.035 [-0.255, +0.198] | 70.0 | +0.558 | +0.200 [-0.179, +0.510] | 80.0 | -0.034 | -0.164 [-0.382, +0.159] | 65.0 | -0.543 | -0.345 [-0.879, +0.318] | 45.0 |
| 1h | SFP_harden | EXP_COUNTER | short | +0.064 | +0.034 [-0.080, +0.213] | 55.0 | +0.649 | +0.025 [-0.624, +0.212] | 95.0 | +0.502 | -0.105 [-0.289, +0.402] | 85.0 | +1.635 | +0.681 [+0.061, +1.375] | 85.0 |
| 1h | SFP_harden | IN_RANGE_COINCIDENT* | both | -0.014 | +0.151 [-0.488, +0.494] | 45.0 | +0.078 | -0.320 [-1.810, +1.266] | 60.0 | -0.825 | -0.767 [-1.196, +0.281] | 50.0 | -1.091 | -0.684 [-2.046, +0.723] | 35.0 |
| 1h | SFP_harden | IN_RANGE_COINCIDENT* | long | -0.269 | -0.044 [-0.580, +0.203] | 40.0 | +0.025 | +0.023 [-1.455, +1.308] | 50.0 | -0.941 | -0.832 [-1.132, +0.251] | 42.1 | -2.652 | -0.552 [-3.407, +4.579] | 31.6 |
| 1h | SFP_harden | IN_RANGE_COINCIDENT* | short | +0.044 | +0.272 [-0.380, +1.303] | 45.0 | +0.078 | +0.030 [-3.050, +2.296] | 50.0 | -0.649 | -0.387 [-1.815, +0.632] | 42.9 | -0.493 | -1.490 [-4.231, +1.348] | 64.3 |
| 1h | SFP_harden | IN_RANGE_MID* | both | -0.157 | -0.158 [-0.317, -0.065] | 50.0 | -0.276 | +0.006 [-0.356, +0.090] | 30.0 | -0.225 | -0.218 [-0.375, +0.049] | 45.0 | -0.386 | -0.284 [-0.442, +0.279] | 30.0 |
| 1h | SFP_harden | IN_RANGE_MID* | long | +0.136 | -0.065 [-0.192, +0.171] | 70.0 | -0.243 | +0.052 [-0.171, +0.419] | 25.0 | -0.303 | +0.097 [-0.285, +0.484] | 25.0 | -0.827 | +0.393 [-0.545, +1.409] | 10.0 |
| 1h | SFP_harden | IN_RANGE_MID* | short | -0.648 | -0.306 [-0.473, -0.150] | 10.0 | -0.283 | -0.338 [-0.759, +0.050] | 55.0 | -0.222 | -0.434 [-0.812, -0.046] | 65.0 | -0.286 | -0.713 [-1.448, +0.233] | 60.0 |
| 1h | SFP_harden | IN_RANGE_OTHER | both | -0.123 | -0.063 [-0.175, +0.041] | 30.0 | -0.551 | -0.061 [-0.705, +0.182] | 35.0 | -0.654 | -0.155 [-0.327, +0.012] | 5.0 | -1.270 | -0.729 [-1.157, +0.307] | 25.0 |
| 1h | SFP_harden | IN_RANGE_OTHER | long | +0.000 | -0.060 [-0.174, +0.106] | 60.0 | -0.569 | -0.238 [-0.592, +0.228] | 25.0 | -0.533 | -0.035 [-0.493, +0.183] | 25.0 | -0.824 | -0.354 [-1.473, +0.301] | 30.0 |
| 1h | SFP_harden | IN_RANGE_OTHER | short | -0.297 | -0.109 [-0.335, +0.043] | 35.0 | -0.556 | -0.243 [-0.796, +0.298] | 45.0 | -0.911 | -0.230 [-0.666, +0.350] | 5.0 | -1.417 | -0.599 [-1.873, -0.437] | 35.0 |
| 1h | SFP_harden | NONE | both | +0.407 | -0.142 [-0.811, +0.499] | 70.0 | +4.035 | -0.338 [-2.098, +1.178] | 100.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | SFP_harden | NONE | long | +0.769 | -0.321 [-0.919, +0.272] | 84.2 | +3.324 | -0.617 [-3.205, +1.409] | 100.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1h | SFP_harden | NONE | short | -1.830 | +0.433 [-0.303, +1.234] | 8.3 | +4.624 | -0.180 [-1.200, +2.700] | 91.7 | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_first | ALL | both | +0.129 | +0.205 [+0.113, +0.275] | 35.0 | +0.281 | +0.164 [-0.070, +0.446] | 60.0 | +0.137 | +0.005 [-0.046, +0.161] | 65.0 | -0.069 | -0.013 [-0.348, +0.389] | 50.0 |
| 4h | BRK_tap89_first | ALL | long | +0.025 | +0.257 [+0.146, +0.549] | 20.0 | -0.053 | +0.001 [-0.282, +0.385] | 50.0 | -0.407 | -0.205 [-0.476, +0.118] | 30.0 | +0.020 | +0.097 [-0.318, +0.683] | 45.0 |
| 4h | BRK_tap89_first | ALL | short | +0.277 | +0.150 [-0.088, +0.302] | 70.0 | +0.431 | +0.211 [-0.091, +0.702] | 60.0 | +0.393 | +0.145 [-0.002, +0.530] | 65.0 | -0.302 | -0.280 [-1.062, +0.485] | 50.0 |
| 4h | BRK_tap89_first | EXP_ALIGNED* | both | +0.376 | +0.570 [+0.345, +0.664] | 30.0 | -0.297 | +0.176 [-0.291, +0.443] | 22.5 | +0.332 | +0.535 [+0.210, +0.723] | 35.0 | -0.317 | -0.115 [-0.558, +0.610] | 40.0 |
| 4h | BRK_tap89_first | EXP_ALIGNED* | long | +0.627 | +0.710 [+0.370, +0.767] | 45.0 | -0.295 | -0.217 [-0.567, +0.658] | 45.0 | +0.219 | +0.122 [-0.337, +0.709] | 50.0 | -0.240 | -0.237 [-0.849, +0.338] | 45.0 |
| 4h | BRK_tap89_first | EXP_ALIGNED* | short | +0.342 | +0.364 [+0.328, +0.589] | 35.0 | +0.278 | +0.779 [-0.163, +1.153] | 40.0 | +0.354 | +0.678 [+0.402, +0.996] | 20.0 | -0.426 | +0.362 [-1.109, +1.144] | 30.0 |
| 4h | BRK_tap89_first | EXP_COUNTER | both | +0.061 | -0.187 [-0.300, +0.032] | 80.0 | +0.711 | +0.222 [-0.277, +0.962] | 65.0 | +0.722 | -0.377 [-1.129, +0.153] | 95.0 | +1.555 | +0.437 [-0.337, +1.512] | 75.0 |
| 4h | BRK_tap89_first | EXP_COUNTER | long | +0.031 | -0.001 [-0.176, +0.284] | 55.0 | +0.531 | -0.032 [-0.365, +0.513] | 75.0 | +0.915 | -0.196 [-0.702, +1.061] | 70.0 | +2.678 | -0.070 [-0.678, +0.668] | 95.0 |
| 4h | BRK_tap89_first | EXP_COUNTER | short | +0.182 | -0.240 [-0.592, -0.114] | 90.0 | +1.038 | +0.976 [+0.223, +1.776] | 50.0 | +0.143 | -1.039 [-1.940, +0.102] | 75.0 | +0.933 | +0.795 [+0.183, +1.834] | 55.0 |
| 4h | BRK_tap89_first | IN_RANGE_COINCIDENT* | both | -2.672 | -0.700 [-3.236, +0.641] | 36.4 | -4.343 | -1.211 [-3.313, +0.978] | 9.1 | — | +0.369 [-0.165, +2.239] | — | — | -1.198 [-1.204, +1.022] | — |
| 4h | BRK_tap89_first | IN_RANGE_COINCIDENT* | long | -3.732 | -1.959 [-3.236, -0.471] | 11.1 | -3.774 | -2.853 [-3.774, +1.889] | 22.2 | — | -0.700 [-0.700, -0.700] | — | — | +3.241 [+3.241, +3.241] | — |
| 4h | BRK_tap89_first | IN_RANGE_COINCIDENT* | short | -1.593 | +2.239 [+1.304, +3.174] | 0.0 | -4.893 | -1.204 [-1.208, -1.201] | 0.0 | — | +2.239 [+1.304, +3.174] | — | — | -1.204 [-1.208, -1.201] | — |
| 4h | BRK_tap89_first | IN_RANGE_MID* | both | -0.039 | +0.129 [-0.002, +0.256] | 20.0 | +0.313 | +0.277 [-0.288, +0.435] | 55.0 | -0.733 | -0.199 [-0.492, +0.065] | 10.0 | -0.820 | -0.070 [-0.660, +0.267] | 20.0 |
| 4h | BRK_tap89_first | IN_RANGE_MID* | long | -0.182 | +0.272 [+0.000, +0.464] | 0.0 | +0.312 | +0.908 [+0.444, +1.806] | 25.0 | -1.142 | -0.712 [-1.122, -0.042] | 25.0 | -0.339 | +0.272 [-0.339, +1.804] | 25.0 |
| 4h | BRK_tap89_first | IN_RANGE_MID* | short | +0.278 | +0.121 [-0.228, +0.199] | 85.0 | +0.320 | -0.171 [-1.304, +0.224] | 80.0 | +0.741 | +0.062 [-0.389, +0.498] | 80.0 | -1.674 | -1.026 [-1.892, -0.531] | 35.0 |
| 4h | BRK_tap89_first | IN_RANGE_OTHER | both | +0.129 | +0.250 [-0.306, +0.349] | 45.0 | +0.416 | +0.423 [-1.059, +0.868] | 50.0 | +0.361 | +0.369 [-0.504, +1.188] | 50.0 | +2.168 | +1.248 [-1.292, +2.378] | 70.0 |
| 4h | BRK_tap89_first | IN_RANGE_OTHER | long | +0.002 | +0.190 [-0.540, +0.700] | 40.0 | -0.986 | -0.846 [-2.156, +0.793] | 40.0 | +1.295 | +1.250 [+0.359, +2.355] | 50.0 | +2.681 | +3.841 [+2.074, +10.543] | 50.0 |
| 4h | BRK_tap89_first | IN_RANGE_OTHER | short | +0.217 | +0.270 [-0.370, +0.450] | 40.0 | +1.193 | +0.561 [-1.794, +1.291] | 70.0 | -1.405 | -0.388 [-1.594, +0.512] | 30.0 | -0.657 | -2.379 [-6.494, -0.478] | 75.0 |
| 4h | BRK_tap89_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | ALL | both | +0.245 | +0.276 [+0.154, +0.340] | 35.0 | +0.398 | +0.409 [+0.222, +0.562] | 45.0 | +0.334 | +0.186 [+0.059, +0.412] | 70.0 | +0.152 | +0.190 [-0.252, +0.350] | 50.0 |
| 4h | BRK_tap89_oneshot | ALL | long | +0.065 | +0.259 [+0.162, +0.693] | 15.0 | +0.269 | +0.308 [-0.104, +0.554] | 40.0 | -0.281 | -0.044 [-0.316, +0.348] | 30.0 | +0.275 | +0.279 [-0.257, +1.002] | 45.0 |
| 4h | BRK_tap89_oneshot | ALL | short | +0.358 | +0.270 [+0.028, +0.348] | 85.0 | +0.449 | +0.427 [+0.252, +0.733] | 55.0 | +0.705 | +0.403 [+0.116, +0.709] | 70.0 | -0.308 | +0.210 [-0.357, +0.680] | 30.0 |
| 4h | BRK_tap89_oneshot | EXP_ALIGNED* | both | +0.496 | +0.573 [+0.349, +0.749] | 45.0 | -0.145 | +0.218 [+0.035, +0.608] | 15.0 | +0.690 | +0.698 [+0.466, +0.817] | 42.5 | -0.115 | +0.320 [-0.512, +0.750] | 40.0 |
| 4h | BRK_tap89_oneshot | EXP_ALIGNED* | long | +0.738 | +0.756 [+0.240, +0.903] | 45.0 | -0.295 | -0.196 [-0.397, +0.456] | 35.0 | +0.690 | +0.265 [-0.008, +0.947] | 60.0 | -0.115 | -0.077 [-0.586, +0.504] | 45.0 |
| 4h | BRK_tap89_oneshot | EXP_ALIGNED* | short | +0.407 | +0.422 [+0.356, +0.650] | 50.0 | +0.478 | +1.091 [+0.435, +1.439] | 30.0 | +0.661 | +0.899 [+0.647, +1.235] | 30.0 | -0.275 | +0.539 [-0.978, +1.533] | 30.0 |
| 4h | BRK_tap89_oneshot | EXP_COUNTER | both | +0.098 | -0.109 [-0.205, +0.140] | 65.0 | +1.038 | +0.354 [-0.207, +0.851] | 75.0 | +0.846 | -0.282 [-1.126, +0.402] | 80.0 | +1.555 | +0.334 [-0.471, +1.324] | 75.0 |
| 4h | BRK_tap89_oneshot | EXP_COUNTER | long | +0.037 | +0.179 [-0.130, +0.406] | 35.0 | +2.087 | +0.454 [-0.431, +0.721] | 90.0 | +0.915 | +0.116 [-0.666, +1.344] | 70.0 | +2.678 | -0.387 [-1.556, +0.499] | 95.0 |
| 4h | BRK_tap89_oneshot | EXP_COUNTER | short | +0.378 | -0.130 [-0.832, +0.112] | 85.0 | +0.610 | +0.943 [-0.078, +1.412] | 40.0 | +0.280 | -0.644 [-2.275, +0.314] | 70.0 | +0.860 | +0.555 [-0.090, +1.737] | 60.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | both | -3.732 | -3.236 [-3.484, -1.215] | 14.3 | -3.774 | -2.853 [-3.774, -1.393] | 28.6 | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | long | -3.732 | -3.236 [-3.484, -1.215] | 14.3 | -3.774 | -2.853 [-3.774, -1.393] | 28.6 | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | IN_RANGE_MID* | both | +0.073 | +0.195 [+0.017, +0.371] | 35.0 | +0.423 | +0.445 [+0.311, +0.804] | 45.0 | -0.451 | -0.110 [-0.386, +0.197] | 25.0 | -0.336 | +0.117 [-0.445, +0.774] | 35.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_MID* | long | -0.190 | +0.212 [+0.022, +0.391] | 10.0 | +1.012 | +1.930 [+0.374, +2.104] | 35.0 | -1.107 | -0.534 [-1.125, -0.060] | 27.5 | -0.338 | +0.673 [-0.342, +2.347] | 30.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_MID* | short | +0.470 | +0.300 [+0.004, +0.548] | 65.0 | +0.397 | +0.268 [-1.273, +0.628] | 55.0 | +0.906 | +0.316 [-0.109, +0.791] | 85.0 | -1.246 | -0.044 [-1.019, +0.213] | 25.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_OTHER | both | +0.303 | +0.248 [-0.385, +0.526] | 50.0 | +1.079 | +0.261 [-1.056, +1.929] | 60.0 | +0.361 | -0.122 [-0.860, +1.382] | 55.0 | +2.353 | +1.851 [-1.694, +2.667] | 60.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_OTHER | long | +0.701 | +0.561 [-0.506, +0.806] | 70.0 | -0.912 | -0.442 [-2.592, +1.953] | 35.0 | +1.295 | +1.364 [+0.084, +3.015] | 45.0 | +2.681 | +5.417 [+2.053, +10.543] | 40.0 |
| 4h | BRK_tap89_oneshot | IN_RANGE_OTHER | short | +0.284 | +0.137 [-0.327, +0.510] | 60.0 | +1.966 | +1.048 [-2.484, +1.726] | 80.0 | -1.405 | -0.571 [-1.618, +1.685] | 37.5 | -3.361 | -2.973 [-6.494, +0.677] | 50.0 |
| 4h | BRK_tap89_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap89_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_first | ALL | both | +0.179 | +0.125 [+0.059, +0.349] | 60.0 | +0.130 | +0.156 [-0.076, +0.402] | 40.0 | +0.322 | +0.076 [-0.204, +0.169] | 80.0 | +0.277 | +0.022 [-0.403, +0.165] | 90.0 |
| 4h | BRK_tap127_first | ALL | long | +0.016 | +0.100 [-0.062, +0.284] | 40.0 | -0.298 | -0.049 [-0.318, +0.257] | 30.0 | -0.213 | -0.213 [-0.440, +0.308] | 50.0 | -0.100 | -0.051 [-0.706, +0.123] | 40.0 |
| 4h | BRK_tap127_first | ALL | short | +0.278 | +0.281 [+0.182, +0.372] | 50.0 | +0.447 | +0.461 [-0.073, +0.623] | 45.0 | +0.667 | +0.331 [+0.033, +0.650] | 80.0 | +0.971 | +0.113 [-0.496, +0.723] | 90.0 |
| 4h | BRK_tap127_first | EXP_ALIGNED* | both | +0.351 | +0.309 [+0.173, +0.739] | 55.0 | -0.282 | +0.195 [-0.191, +0.579] | 25.0 | +0.700 | +0.747 [+0.173, +0.989] | 45.0 | -0.051 | -1.273 [-2.259, -0.116] | 80.0 |
| 4h | BRK_tap127_first | EXP_ALIGNED* | long | +0.526 | +0.443 [+0.076, +0.820] | 55.0 | -0.412 | -0.325 [-0.976, +0.323] | 45.0 | +0.803 | +0.743 [-0.306, +0.916] | 60.0 | -0.725 | -1.855 [-2.465, -0.706] | 65.0 |
| 4h | BRK_tap127_first | EXP_ALIGNED* | short | +0.079 | +0.274 [-0.033, +0.512] | 35.0 | +0.448 | +0.562 [+0.442, +0.861] | 25.0 | +0.651 | +0.928 [+0.132, +1.144] | 40.0 | +0.977 | +0.338 [-2.243, +1.061] | 75.0 |
| 4h | BRK_tap127_first | EXP_COUNTER | both | +0.078 | +0.006 [-0.369, +0.241] | 60.0 | +0.453 | +0.141 [-0.430, +1.029] | 55.0 | +0.111 | -0.688 [-1.224, -0.154] | 90.0 | +1.984 | +0.927 [-0.470, +2.200] | 65.0 |
| 4h | BRK_tap127_first | EXP_COUNTER | long | +0.024 | +0.168 [-0.731, +0.400] | 40.0 | +0.687 | -0.332 [-0.668, +0.269] | 85.0 | +0.275 | -0.795 [-1.423, +0.422] | 65.0 | +2.047 | -0.436 [-2.049, +2.040] | 75.0 |
| 4h | BRK_tap127_first | EXP_COUNTER | short | +0.169 | -0.013 [-0.473, +0.187] | 70.0 | +0.325 | +0.972 [+0.114, +1.989] | 30.0 | -0.567 | -0.636 [-1.244, +0.000] | 55.0 | +2.579 | +2.229 [+0.112, +4.497] | 50.0 |
| 4h | BRK_tap127_first | IN_RANGE_COINCIDENT* | both | -1.670 | -2.082 [-2.966, -1.127] | 61.5 | -1.003 | -3.335 [-5.280, -2.408] | 83.3 | +0.043 | -0.234 [-1.123, +1.857] | 50.0 | +1.379 | -2.598 [-2.687, +0.275] | 66.7 |
| 4h | BRK_tap127_first | IN_RANGE_COINCIDENT* | long | -1.670 | -2.267 [-2.966, -1.121] | 55.6 | -1.003 | -3.335 [-3.384, -2.019] | 75.0 | +0.043 | -0.700 [-0.914, +2.383] | 66.7 | +1.379 | +0.322 [-1.138, +1.782] | 50.0 |
| 4h | BRK_tap127_first | IN_RANGE_COINCIDENT* | short | — | -2.082 [-2.082, -1.362] | — | — | -10.211 [-17.645, -2.074] | — | — | +0.464 [-0.329, +1.257] | — | — | +0.159 [-1.308, +1.627] | — |
| 4h | BRK_tap127_first | IN_RANGE_MID* | both | -0.036 | +0.071 [-0.033, +0.259] | 25.0 | -0.222 | +0.041 [-0.150, +0.207] | 25.0 | -0.739 | -0.151 [-0.319, +0.200] | 5.0 | -0.381 | +0.090 [-0.092, +0.344] | 20.0 |
| 4h | BRK_tap127_first | IN_RANGE_MID* | long | -0.143 | +0.008 [-0.159, +0.444] | 35.0 | -0.222 | +0.431 [+0.051, +1.911] | 15.0 | -1.182 | -0.472 [-0.768, +0.047] | 5.0 | -0.384 | +0.151 [-0.029, +1.329] | 15.0 |
| 4h | BRK_tap127_first | IN_RANGE_MID* | short | +0.226 | +0.174 [-0.031, +0.413] | 55.0 | -0.265 | -0.544 [-1.971, +0.124] | 50.0 | +0.666 | +0.312 [-0.329, +0.613] | 80.0 | -0.878 | -0.630 [-2.079, +0.154] | 45.0 |
| 4h | BRK_tap127_first | IN_RANGE_OTHER | both | +0.964 | +0.382 [+0.007, +0.847] | 80.0 | +0.731 | +0.880 [-0.245, +1.768] | 45.0 | +1.230 | +1.060 [+0.615, +1.256] | 75.0 | +2.087 | +1.247 [+0.247, +1.818] | 80.0 |
| 4h | BRK_tap127_first | IN_RANGE_OTHER | long | +0.100 | +0.033 [-0.888, +0.497] | 70.0 | -0.982 | -0.107 [-2.332, +0.851] | 35.0 | +1.134 | +1.178 [-0.218, +2.748] | 50.0 | +0.765 | +1.315 [+0.057, +2.157] | 35.0 |
| 4h | BRK_tap127_first | IN_RANGE_OTHER | short | +1.156 | +0.704 [+0.428, +1.001] | 95.0 | +2.528 | +1.665 [+0.279, +2.531] | 72.5 | +1.603 | +1.077 [+0.806, +1.116] | 92.5 | +2.312 | +0.715 [-0.667, +2.098] | 80.0 |
| 4h | BRK_tap127_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_oneshot | ALL | both | +0.208 | +0.161 [+0.057, +0.299] | 55.0 | +0.289 | +0.352 [-0.104, +0.494] | 45.0 | +0.037 | +0.039 [-0.214, +0.440] | 50.0 | +0.329 | +0.014 [-0.372, +0.166] | 90.0 |
| 4h | BRK_tap127_oneshot | ALL | long | +0.047 | +0.085 [-0.142, +0.428] | 45.0 | +0.126 | +0.241 [-0.273, +0.558] | 45.0 | -0.185 | -0.193 [-0.366, +0.240] | 55.0 | +0.113 | +0.079 [-0.329, +0.162] | 50.0 |
| 4h | BRK_tap127_oneshot | ALL | short | +0.287 | +0.269 [+0.079, +0.346] | 55.0 | +0.451 | +0.293 [-0.081, +0.819] | 55.0 | +0.644 | +0.395 [-0.011, +0.634] | 85.0 | +0.971 | +0.021 [-0.884, +0.645] | 90.0 |
| 4h | BRK_tap127_oneshot | EXP_ALIGNED* | both | +0.349 | +0.348 [+0.234, +0.777] | 50.0 | -0.304 | +0.259 [-0.294, +0.788] | 25.0 | +0.666 | +0.626 [+0.238, +1.074] | 60.0 | +0.036 | -0.715 [-1.899, -0.006] | 75.0 |
| 4h | BRK_tap127_oneshot | EXP_ALIGNED* | long | +0.745 | +0.636 [+0.347, +0.875] | 55.0 | -0.396 | -0.324 [-0.809, +0.225] | 40.0 | +0.913 | +0.898 [+0.317, +1.006] | 55.0 | -0.429 | -1.271 [-1.902, -0.336] | 70.0 |
| 4h | BRK_tap127_oneshot | EXP_ALIGNED* | short | -0.191 | +0.027 [-0.311, +0.598] | 40.0 | +0.720 | +0.986 [+0.532, +2.485] | 35.0 | +0.272 | +0.452 [-0.366, +1.225] | 50.0 | +1.027 | +0.136 [-3.163, +1.604] | 60.0 |
| 4h | BRK_tap127_oneshot | EXP_COUNTER | both | +0.075 | -0.206 [-0.550, +0.096] | 70.0 | +0.691 | +0.576 [-0.339, +0.957] | 55.0 | +0.008 | -0.620 [-1.310, +0.251] | 70.0 | +2.012 | +0.804 [-0.389, +2.702] | 65.0 |
| 4h | BRK_tap127_oneshot | EXP_COUNTER | long | +0.040 | -0.007 [-0.784, +0.541] | 50.0 | +2.011 | -0.086 [-0.440, +0.746] | 95.0 | +0.275 | -0.411 [-1.256, +0.638] | 65.0 | +2.047 | +0.704 [-0.439, +2.303] | 70.0 |
| 4h | BRK_tap127_oneshot | EXP_COUNTER | short | +0.111 | -0.048 [-0.555, +0.192] | 60.0 | +0.070 | +0.596 [-0.176, +1.304] | 40.0 | -0.919 | -0.562 [-1.655, +0.058] | 45.0 | +3.174 | +2.718 [-0.604, +3.458] | 65.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | both | -1.670 | -1.697 [-2.966, -1.121] | 50.0 | -1.003 | -3.335 [-3.384, -2.598] | 77.8 | +0.043 | -0.234 [-1.123, +1.857] | 50.0 | +1.379 | -2.598 [-2.687, +0.275] | 66.7 |
| 4h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | long | -1.670 | -2.267 [-2.966, -1.121] | 55.6 | -1.003 | -3.335 [-3.384, -2.019] | 75.0 | +0.043 | -0.700 [-0.914, +2.383] | 66.7 | +1.379 | +0.322 [-1.138, +1.782] | 50.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | short | — | +0.464 [-0.329, +1.257] | — | — | +0.159 [-1.308, +1.627] | — | — | +0.464 [-0.329, +1.257] | — | — | +0.159 [-1.308, +1.627] | — |
| 4h | BRK_tap127_oneshot | IN_RANGE_MID* | both | -0.033 | +0.008 [-0.046, +0.141] | 45.0 | +0.160 | +0.140 [-0.100, +0.318] | 50.0 | -0.758 | -0.173 [-0.590, +0.011] | 10.0 | -0.257 | -0.039 [-0.519, +0.535] | 30.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_MID* | long | -0.143 | -0.106 [-0.301, +0.169] | 40.0 | +0.212 | +0.627 [+0.139, +1.400] | 35.0 | -1.180 | -0.745 [-1.035, -0.327] | 15.0 | -0.148 | +0.871 [-0.135, +1.846] | 25.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_MID* | short | +0.423 | +0.244 [-0.052, +0.448] | 65.0 | +0.053 | -0.404 [-2.062, +0.058] | 75.0 | +0.551 | +0.141 [-0.262, +0.620] | 65.0 | -1.667 | -1.099 [-2.334, +0.112] | 40.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_OTHER | both | +0.978 | +0.714 [+0.146, +0.948] | 85.0 | +0.731 | +1.284 [-0.102, +1.893] | 40.0 | +1.230 | +1.091 [+0.770, +1.599] | 60.0 | +2.087 | +1.229 [-0.006, +2.091] | 70.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_OTHER | long | +0.409 | +0.027 [-0.774, +0.897] | 60.0 | -0.302 | +0.489 [-2.723, +1.404] | 45.0 | +1.134 | +1.178 [-0.039, +2.749] | 50.0 | +0.765 | +1.369 [-0.938, +2.157] | 35.0 |
| 4h | BRK_tap127_oneshot | IN_RANGE_OTHER | short | +1.275 | +0.745 [+0.446, +1.067] | 100.0 | +2.312 | +1.913 [+0.539, +2.318] | 72.5 | +1.603 | +1.088 [+1.017, +1.126] | 87.5 | +2.312 | +0.579 [-0.667, +2.090] | 85.0 |
| 4h | BRK_tap127_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap127_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_first | ALL | both | +0.010 | -0.008 [-0.082, +0.193] | 60.0 | -0.277 | -0.047 [-0.337, +0.062] | 25.0 | +0.230 | +0.028 [-0.189, +0.312] | 70.0 | -0.108 | -0.094 [-0.344, +0.010] | 45.0 |
| 4h | BRK_tap200_first | ALL | long | +0.017 | +0.064 [-0.040, +0.311] | 45.0 | -0.632 | -0.241 [-0.639, -0.152] | 25.0 | -0.118 | -0.090 [-0.357, +0.096] | 45.0 | -0.202 | -0.277 [-0.422, +0.069] | 55.0 |
| 4h | BRK_tap200_first | ALL | short | -0.050 | -0.092 [-0.197, +0.212] | 55.0 | -0.039 | +0.085 [-0.216, +0.537] | 40.0 | +0.781 | +0.467 [+0.002, +0.685] | 95.0 | +0.767 | -0.023 [-0.582, +0.447] | 85.0 |
| 4h | BRK_tap200_first | EXP_ALIGNED* | both | -0.312 | -0.278 [-0.412, +0.020] | 45.0 | -0.494 | -0.744 [-1.276, -0.310] | 65.0 | -0.017 | -0.206 [-0.394, +0.141] | 70.0 | -1.167 | -1.777 [-2.482, -0.867] | 67.5 |
| 4h | BRK_tap200_first | EXP_ALIGNED* | long | -0.252 | -0.237 [-0.478, +0.133] | 45.0 | -1.910 | -1.630 [-1.934, -1.133] | 30.0 | -0.291 | -0.142 [-0.315, +0.118] | 30.0 | -1.960 | -1.932 [-2.409, -1.173] | 40.0 |
| 4h | BRK_tap200_first | EXP_ALIGNED* | short | -0.407 | -0.273 [-0.796, +0.583] | 45.0 | +0.879 | +0.433 [-0.230, +0.566] | 80.0 | +0.648 | +0.648 [-1.188, +1.114] | 50.0 | +0.891 | -2.171 [-3.589, +0.774] | 85.0 |
| 4h | BRK_tap200_first | EXP_COUNTER | both | +0.384 | +0.042 [-0.050, +0.227] | 90.0 | +1.135 | +0.715 [-0.414, +1.086] | 75.0 | +0.953 | -0.063 [-0.335, +0.253] | 85.0 | +2.758 | +0.968 [-0.183, +4.114] | 60.0 |
| 4h | BRK_tap200_first | EXP_COUNTER | long | +0.679 | +0.149 [-0.265, +0.434] | 95.0 | +2.211 | -0.534 [-0.756, +0.423] | 95.0 | +0.885 | +0.083 [-0.203, +0.447] | 95.0 | +3.107 | +1.066 [-1.692, +4.862] | 65.0 |
| 4h | BRK_tap200_first | EXP_COUNTER | short | +0.023 | +0.137 [-0.170, +0.343] | 45.0 | +1.137 | +1.086 [-0.451, +1.433] | 55.0 | +1.108 | -0.122 [-0.661, +0.356] | 80.0 | +2.758 | +1.965 [-0.472, +4.418] | 55.0 |
| 4h | BRK_tap200_first | IN_RANGE_COINCIDENT* | both | — | +0.090 [-1.234, +0.993] | — | — | -2.585 [-8.122, +1.206] | — | — | +0.824 [+0.796, +0.986] | — | — | +0.899 [+0.200, +2.802] | — |
| 4h | BRK_tap200_first | IN_RANGE_COINCIDENT* | long | — | +0.824 [-2.304, +3.776] | — | — | -0.885 [-2.960, +1.638] | — | — | +0.824 [+0.824, +0.824] | — | — | +4.705 [+4.705, +4.705] | — |
| 4h | BRK_tap200_first | IN_RANGE_COINCIDENT* | short | — | +0.090 [-1.677, +1.446] | — | — | -8.481 [-13.498, +0.781] | — | — | +0.959 [+0.864, +1.053] | — | — | +0.200 [-0.150, +0.550] | — |
| 4h | BRK_tap200_first | IN_RANGE_MID* | both | +0.083 | +0.126 [+0.076, +0.341] | 35.0 | -0.783 | -0.267 [-0.859, +0.098] | 25.0 | +0.215 | +0.052 [-0.153, +0.405] | 65.0 | -0.167 | -0.256 [-0.616, +0.204] | 55.0 |
| 4h | BRK_tap200_first | IN_RANGE_MID* | long | -0.020 | +0.239 [-0.193, +0.469] | 30.0 | -0.576 | +0.261 [-0.656, +1.620] | 30.0 | -1.196 | -0.636 [-1.056, +0.159] | 20.0 | -0.195 | +0.227 [-1.391, +1.441] | 35.0 |
| 4h | BRK_tap200_first | IN_RANGE_MID* | short | +0.289 | +0.225 [+0.046, +0.297] | 65.0 | -0.781 | -0.692 [-0.924, +0.009] | 40.0 | +0.919 | +0.482 [+0.345, +0.870] | 85.0 | -0.083 | -0.627 [-0.877, +0.064] | 65.0 |
| 4h | BRK_tap200_first | IN_RANGE_OTHER | both | -0.161 | +0.153 [-0.177, +0.309] | 25.0 | -0.904 | +0.259 [-0.006, +0.863] | 5.0 | -0.330 | -0.187 [-1.745, +0.836] | 50.0 | -0.311 | +0.077 [+0.011, +0.175] | 15.0 |
| 4h | BRK_tap200_first | IN_RANGE_OTHER | long | +1.079 | +0.964 [+0.262, +1.304] | 60.0 | +0.193 | +0.884 [+0.253, +1.683] | 20.0 | +0.339 | +0.335 [-2.120, +1.370] | 50.0 | -0.041 | +0.031 [-0.153, +0.147] | 35.0 |
| 4h | BRK_tap200_first | IN_RANGE_OTHER | short | -0.694 | -0.355 [-0.863, -0.150] | 30.0 | -1.395 | -0.659 [-1.561, +0.649] | 30.0 | -1.118 | -0.486 [-1.115, +0.706] | 25.0 | -0.581 | +0.491 [-0.328, +1.503] | 10.0 |
| 4h | BRK_tap200_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_oneshot | ALL | both | +0.030 | -0.043 [-0.111, +0.224] | 60.0 | -0.136 | +0.292 [-0.040, +0.442] | 25.0 | +0.179 | -0.059 [-0.157, +0.272] | 65.0 | -0.090 | -0.051 [-0.226, +0.229] | 45.0 |
| 4h | BRK_tap200_oneshot | ALL | long | +0.100 | +0.089 [-0.099, +0.241] | 50.0 | -0.296 | -0.088 [-0.420, +0.306] | 35.0 | -0.116 | -0.129 [-0.323, +0.026] | 50.0 | -0.206 | -0.196 [-0.812, +0.168] | 45.0 |
| 4h | BRK_tap200_oneshot | ALL | short | -0.062 | -0.098 [-0.175, +0.195] | 55.0 | +0.430 | +0.366 [-0.031, +0.842] | 60.0 | +0.774 | +0.426 [-0.046, +0.674] | 90.0 | +0.914 | -0.001 [-0.480, +0.975] | 70.0 |
| 4h | BRK_tap200_oneshot | EXP_ALIGNED* | both | -0.293 | -0.358 [-0.378, -0.252] | 70.0 | -0.554 | -0.541 [-1.293, -0.253] | 50.0 | -0.017 | +0.040 [-0.114, +0.306] | 47.5 | -0.401 | -1.222 [-1.973, -0.249] | 75.0 |
| 4h | BRK_tap200_oneshot | EXP_ALIGNED* | long | -0.243 | -0.324 [-0.597, -0.193] | 65.0 | -1.884 | -1.747 [-1.961, -1.109] | 45.0 | -0.291 | -0.142 [-0.315, +0.118] | 30.0 | -1.960 | -1.932 [-2.409, -1.173] | 40.0 |
| 4h | BRK_tap200_oneshot | EXP_ALIGNED* | short | -0.410 | -0.339 [-0.928, +0.867] | 35.0 | +1.019 | +0.436 [-0.171, +1.090] | 65.0 | +0.648 | +0.974 [-0.226, +1.561] | 45.0 | +2.115 | +1.798 [-1.548, +2.510] | 52.5 |
| 4h | BRK_tap200_oneshot | EXP_COUNTER | both | +0.648 | +0.056 [-0.031, +0.316] | 90.0 | +1.106 | +0.767 [+0.463, +1.042] | 80.0 | +0.953 | -0.001 [-0.091, +0.545] | 90.0 | +2.758 | +2.610 [+0.721, +4.537] | 50.0 |
| 4h | BRK_tap200_oneshot | EXP_COUNTER | long | +0.690 | +0.134 [-0.382, +0.294] | 90.0 | +2.201 | -0.046 [-0.597, +0.586] | 95.0 | +0.885 | +0.128 [-0.209, +0.454] | 95.0 | +3.107 | +1.195 [-1.759, +5.456] | 65.0 |
| 4h | BRK_tap200_oneshot | EXP_COUNTER | short | +0.018 | +0.284 [+0.011, +0.506] | 25.0 | +1.095 | +1.138 [+0.270, +1.429] | 45.0 | +1.108 | -0.029 [-0.252, +1.119] | 72.5 | +2.758 | +3.735 [+0.918, +4.650] | 45.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | both | — | +0.848 [-0.663, +1.055] | — | — | -1.346 [-9.494, +1.422] | — | — | +0.824 [+0.796, +0.986] | — | — | +0.899 [+0.200, +2.802] | — |
| 4h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | long | — | +1.500 [-2.018, +4.575] | — | — | +0.377 [-2.722, +1.638] | — | — | +0.824 [+0.824, +0.824] | — | — | +4.705 [+4.705, +4.705] | — |
| 4h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | short | — | +0.871 [-1.677, +1.449] | — | — | -10.071 [-13.498, +0.781] | — | — | +0.959 [+0.864, +1.053] | — | — | +0.200 [-0.150, +0.550] | — |
| 4h | BRK_tap200_oneshot | IN_RANGE_MID* | both | +0.291 | +0.141 [-0.009, +0.301] | 75.0 | -0.133 | -0.008 [-0.613, +0.579] | 35.0 | +0.201 | +0.030 [-0.327, +0.413] | 60.0 | -0.182 | -0.029 [-0.428, +0.475] | 40.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_MID* | long | +0.028 | +0.181 [-0.021, +0.448] | 30.0 | -0.132 | +0.637 [-0.152, +2.577] | 30.0 | -0.954 | -0.149 [-1.044, +0.408] | 35.0 | -0.191 | +0.780 [-1.251, +1.971] | 30.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_MID* | short | +0.307 | +0.108 [-0.182, +0.311] | 75.0 | -0.270 | -0.465 [-1.064, +0.255] | 55.0 | +0.978 | +0.219 [-0.153, +0.731] | 80.0 | -0.442 | -1.140 [-1.786, -0.003] | 60.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_OTHER | both | -0.161 | +0.173 [-0.150, +0.461] | 25.0 | -0.856 | +1.061 [+0.144, +1.134] | 0.0 | -0.490 | -0.790 [-1.490, +1.330] | 50.0 | -0.576 | +0.123 [-0.047, +0.645] | 10.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_OTHER | long | +1.217 | +1.013 [+0.172, +1.427] | 70.0 | +1.049 | +1.565 [+0.678, +1.724] | 35.0 | +0.852 | -0.330 [-1.925, +0.947] | 70.0 | -0.390 | +0.019 [-0.579, +0.191] | 35.0 |
| 4h | BRK_tap200_oneshot | IN_RANGE_OTHER | short | -0.482 | -0.308 [-1.185, -0.112] | 35.0 | -0.931 | -0.552 [-0.782, +0.899] | 20.0 | -1.118 | -0.480 [-0.682, +0.706] | 25.0 | -0.581 | +1.097 [-0.328, +1.503] | 10.0 |
| 4h | BRK_tap200_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_tap200_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_first | ALL | both | +0.058 | -0.016 [-0.074, +0.049] | 75.0 | +0.493 | +0.096 [-0.117, +0.357] | 85.0 | -0.237 | -0.042 [-0.238, +0.159] | 25.0 | +0.777 | -0.116 [-0.513, +0.973] | 65.0 |
| 4h | BRK_mem_first | ALL | long | +0.439 | -0.067 [-0.246, +0.044] | 95.0 | +0.831 | +0.067 [-0.153, +0.497] | 85.0 | -0.006 | -0.355 [-0.706, +0.056] | 70.0 | +0.815 | +0.526 [-0.790, +1.662] | 60.0 |
| 4h | BRK_mem_first | ALL | short | -0.228 | +0.007 [-0.131, +0.186] | 10.0 | +0.082 | -0.016 [-0.411, +0.384] | 55.0 | -0.346 | +0.145 [-0.031, +0.455] | 20.0 | -0.017 | -0.319 [-1.361, +0.497] | 55.0 |
| 4h | BRK_mem_first | EXP_ALIGNED* | both | +0.356 | -0.004 [-0.408, +0.312] | 80.0 | -0.320 | -0.210 [-0.752, +0.366] | 40.0 | -0.183 | -0.095 [-0.569, +0.296] | 50.0 | -1.927 | -0.887 [-1.747, +0.136] | 20.0 |
| 4h | BRK_mem_first | EXP_ALIGNED* | long | +0.457 | -0.062 [-0.475, +0.288] | 80.0 | -0.531 | -0.419 [-1.345, +0.525] | 45.0 | -1.005 | -0.145 [-0.863, +0.325] | 25.0 | -2.542 | -0.386 [-2.440, +0.948] | 25.0 |
| 4h | BRK_mem_first | EXP_ALIGNED* | short | +0.290 | +0.113 [-0.162, +0.361] | 70.0 | +0.115 | -0.250 [-0.919, +0.628] | 60.0 | +0.876 | -0.043 [-0.569, +0.612] | 80.0 | -0.256 | -0.175 [-1.676, +0.566] | 50.0 |
| 4h | BRK_mem_first | EXP_COUNTER | both | -0.008 | +0.096 [-0.279, +0.401] | 40.0 | +1.538 | +0.399 [-0.107, +1.689] | 70.0 | +1.317 | -0.144 [-0.837, +0.626] | 95.0 | +2.489 | -0.065 [-1.186, +1.105] | 80.0 |
| 4h | BRK_mem_first | EXP_COUNTER | long | +1.429 | -0.417 [-0.642, -0.008] | 100.0 | +3.720 | +0.105 [-1.055, +0.763] | 100.0 | +2.200 | -0.356 [-1.003, +0.185] | 100.0 | +4.168 | +0.192 [-1.321, +1.770] | 85.0 |
| 4h | BRK_mem_first | EXP_COUNTER | short | -0.189 | +0.365 [-0.031, +0.814] | 20.0 | +0.134 | +1.266 [-0.093, +1.873] | 30.0 | +0.035 | -0.285 [-0.756, +1.026] | 55.0 | +1.773 | +1.062 [-1.091, +2.806] | 65.0 |
| 4h | BRK_mem_first | IN_RANGE_COINCIDENT* | both | -1.694 | +0.347 [-2.811, +1.114] | 38.5 | +9.533 | -1.436 [-6.268, +4.402] | 76.9 | — | +6.047 [+5.128, +6.967] | — | — | +3.065 [+2.397, +3.734] | — |
| 4h | BRK_mem_first | IN_RANGE_COINCIDENT* | long | -1.694 | -2.811 [-4.434, +0.347] | 55.6 | +9.533 | -3.230 [-4.782, +0.282] | 77.8 | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_first | IN_RANGE_COINCIDENT* | short | — | +2.640 [+0.704, +6.967] | — | — | -2.270 [-6.649, +3.734] | — | — | +6.047 [+5.128, +6.967] | — | — | +3.065 [+2.397, +3.734] | — |
| 4h | BRK_mem_first | IN_RANGE_MID* | both | -0.373 | -0.016 [-0.299, +0.175] | 20.0 | +0.173 | -0.460 [-1.283, +0.329] | 70.0 | -0.810 | +0.046 [-0.272, +0.372] | 5.0 | -0.731 | +0.753 [-0.221, +1.740] | 20.0 |
| 4h | BRK_mem_first | IN_RANGE_MID* | long | +0.239 | +0.145 [-0.280, +0.289] | 70.0 | +0.240 | +0.197 [-0.864, +1.476] | 50.0 | -0.370 | -0.046 [-0.381, +0.533] | 25.0 | +2.604 | +2.072 [-0.263, +4.128] | 60.0 |
| 4h | BRK_mem_first | IN_RANGE_MID* | short | -0.988 | -0.173 [-0.345, +0.116] | 0.0 | -0.138 | -1.445 [-2.700, -0.272] | 80.0 | -1.110 | +0.044 [-0.293, +0.653] | 5.0 | -1.265 | -0.539 [-1.723, +0.655] | 35.0 |
| 4h | BRK_mem_first | IN_RANGE_OTHER | both | -0.071 | +0.045 [-0.417, +0.226] | 35.0 | +1.403 | +0.328 [-0.220, +0.608] | 80.0 | +0.014 | -0.085 [-0.646, +0.355] | 60.0 | +1.485 | +0.154 [-2.197, +2.735] | 65.0 |
| 4h | BRK_mem_first | IN_RANGE_OTHER | long | +0.903 | -0.067 [-0.313, +0.586] | 80.0 | +3.951 | +0.146 [-0.395, +1.985] | 95.0 | +0.641 | -0.740 [-1.084, +0.742] | 70.0 | +5.127 | +0.012 [-2.610, +4.701] | 80.0 |
| 4h | BRK_mem_first | IN_RANGE_OTHER | short | -0.624 | -0.017 [-0.701, +0.309] | 25.0 | +0.269 | +0.367 [-1.150, +1.076] | 40.0 | -0.943 | -0.193 [-1.122, +0.684] | 35.0 | -0.054 | +0.353 [-1.862, +2.201] | 40.0 |
| 4h | BRK_mem_first | NONE | both | — | +0.055 [-1.962, +0.056] | — | — | -2.673 [-6.996, +2.198] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_first | NONE | long | — | -1.961 [-2.970, -0.953] | — | — | -6.996 [-9.157, -4.834] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_first | NONE | short | — | +0.055 [+0.055, +0.055] | — | — | +7.069 [+7.069, +7.069] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_oneshot | ALL | both | +0.017 | -0.088 [-0.183, +0.070] | 65.0 | +0.350 | -0.076 [-0.172, +0.010] | 85.0 | -0.107 | -0.033 [-0.284, +0.120] | 40.0 | +0.292 | -0.046 [-0.688, +1.130] | 50.0 |
| 4h | BRK_mem_oneshot | ALL | long | +0.254 | -0.051 [-0.273, +0.168] | 95.0 | +0.756 | -0.148 [-0.655, +0.784] | 70.0 | +0.171 | -0.142 [-0.527, +0.319] | 65.0 | +2.020 | +0.633 [-0.641, +1.826] | 80.0 |
| 4h | BRK_mem_oneshot | ALL | short | -0.390 | -0.048 [-0.295, +0.093] | 5.0 | -0.153 | -0.040 [-0.500, +0.379] | 45.0 | -0.347 | +0.126 [-0.198, +0.364] | 20.0 | -0.708 | -0.331 [-1.666, +0.545] | 40.0 |
| 4h | BRK_mem_oneshot | EXP_ALIGNED* | both | +0.222 | -0.072 [-0.360, +0.201] | 75.0 | -0.426 | -0.291 [-0.798, +0.401] | 40.0 | +0.171 | +0.004 [-0.373, +0.264] | 65.0 | -1.834 | -0.718 [-1.997, +0.096] | 30.0 |
| 4h | BRK_mem_oneshot | EXP_ALIGNED* | long | +0.232 | +0.076 [-0.426, +0.318] | 65.0 | -0.216 | -0.157 [-1.514, +0.532] | 45.0 | -0.221 | +0.076 [-0.728, +0.608] | 40.0 | -1.172 | -0.353 [-1.822, +0.924] | 40.0 |
| 4h | BRK_mem_oneshot | EXP_ALIGNED* | short | +0.073 | -0.065 [-0.552, +0.305] | 65.0 | -1.030 | +0.101 [-0.691, +0.576] | 20.0 | +0.876 | -0.160 [-0.565, +0.375] | 80.0 | -1.989 | -1.228 [-3.214, +0.247] | 35.0 |
| 4h | BRK_mem_oneshot | EXP_COUNTER | both | +0.771 | +0.325 [-0.159, +0.484] | 90.0 | +1.785 | +0.770 [-0.116, +1.972] | 65.0 | +1.396 | -0.108 [-0.670, +0.539] | 95.0 | +2.345 | +0.588 [-0.947, +1.886] | 80.0 |
| 4h | BRK_mem_oneshot | EXP_COUNTER | long | +2.168 | +0.002 [-0.443, +0.405] | 100.0 | +3.454 | +0.766 [-0.720, +1.299] | 100.0 | +2.302 | +0.001 [-0.535, +0.505] | 100.0 | +4.156 | -0.145 [-1.226, +2.220] | 90.0 |
| 4h | BRK_mem_oneshot | EXP_COUNTER | short | -0.188 | +0.553 [+0.232, +0.846] | 15.0 | +0.873 | +1.123 [+0.259, +2.101] | 40.0 | -0.099 | +0.069 [-1.058, +1.445] | 50.0 | +1.281 | +1.757 [-0.281, +3.606] | 40.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | both | -1.694 | -0.313 [-2.581, +1.093] | 46.7 | +9.533 | -1.436 [-7.183, +2.449] | 93.3 | — | +0.800 [-0.313, +4.208] | — | — | +1.728 [+1.583, +2.107] | — |
| 4h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | long | -1.694 | -1.448 [-3.491, +0.687] | 50.0 | +9.533 | -0.949 [-4.258, +1.431] | 80.0 | — | +0.244 [-0.035, +0.522] | — | — | +0.755 [+0.079, +1.431] | — |
| 4h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | short | — | -0.625 [-2.712, +3.424] | — | — | -6.013 [-10.617, +1.692] | — | — | +4.208 [+0.204, +6.047] | — | — | +1.728 [+1.656, +3.065] | — |
| 4h | BRK_mem_oneshot | IN_RANGE_MID* | both | -0.454 | -0.185 [-0.398, -0.005] | 20.0 | -0.708 | -0.624 [-1.206, -0.219] | 45.0 | -0.902 | -0.252 [-0.470, +0.181] | 15.0 | -1.181 | +0.092 [-0.880, +1.557] | 20.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_MID* | long | +0.076 | -0.178 [-0.448, +0.149] | 65.0 | -0.785 | +0.102 [-1.167, +2.019] | 35.0 | -0.627 | -0.360 [-0.687, +0.236] | 30.0 | +0.910 | +2.983 [-0.715, +4.835] | 35.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_MID* | short | -1.101 | -0.225 [-0.545, -0.055] | 10.0 | -0.432 | -0.982 [-2.912, -0.219] | 65.0 | -1.047 | -0.080 [-0.464, +0.699] | 5.0 | -1.171 | -0.457 [-2.074, +0.240] | 40.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_OTHER | both | -0.624 | -0.022 [-0.614, +0.129] | 25.0 | +1.316 | -0.262 [-0.499, +0.084] | 85.0 | +0.459 | -0.056 [-0.787, +0.617] | 65.0 | +1.905 | +0.646 [-2.020, +2.519] | 65.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_OTHER | long | +0.492 | +0.039 [-0.691, +0.625] | 70.0 | +4.842 | -0.265 [-1.442, +1.869] | 100.0 | +0.902 | +0.293 [-0.792, +0.987] | 65.0 | +9.806 | +2.691 [-2.066, +4.430] | 95.0 |
| 4h | BRK_mem_oneshot | IN_RANGE_OTHER | short | -1.474 | -0.587 [-1.028, +0.215] | 5.0 | -0.514 | -0.013 [-0.948, +0.412] | 30.0 | -0.166 | -0.598 [-1.388, +0.268] | 60.0 | -1.452 | -0.239 [-2.913, +3.061] | 40.0 |
| 4h | BRK_mem_oneshot | NONE | both | — | +0.055 [-1.962, +0.056] | — | — | -2.673 [-6.996, +2.198] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_oneshot | NONE | long | — | -1.961 [-2.970, -0.953] | — | — | -6.996 [-9.157, -4.834] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | BRK_mem_oneshot | NONE | short | — | +0.055 [+0.055, +0.055] | — | — | +7.069 [+7.069, +7.069] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | SFP_harden | ALL | both | +0.103 | +0.050 [-0.041, +0.168] | 60.0 | +0.228 | +0.013 [-0.530, +0.785] | 60.0 | +0.282 | +0.065 [-0.047, +0.176] | 80.0 | +1.123 | +0.244 [-0.415, +0.973] | 75.0 |
| 4h | SFP_harden | ALL | long | +0.240 | +0.146 [+0.023, +0.234] | 75.0 | +0.374 | +0.489 [-0.399, +0.852] | 40.0 | +0.084 | +0.100 [-0.149, +0.260] | 45.0 | +2.015 | +0.492 [-0.569, +1.323] | 85.0 |
| 4h | SFP_harden | ALL | short | -0.024 | +0.003 [-0.303, +0.131] | 45.0 | +0.011 | -0.198 [-0.872, +1.016] | 60.0 | +0.647 | +0.036 [-0.188, +0.440] | 80.0 | +0.633 | -0.009 [-1.275, +1.110] | 65.0 |
| 4h | SFP_harden | EXP_ALIGNED* | both | +0.239 | +0.058 [-0.020, +0.366] | 60.0 | +0.238 | +0.309 [-0.215, +1.284] | 50.0 | +0.266 | +0.112 [-0.225, +0.419] | 60.0 | -0.913 | +0.303 [-0.924, +1.559] | 25.0 |
| 4h | SFP_harden | EXP_ALIGNED* | long | -0.146 | +0.138 [-0.166, +0.413] | 30.0 | -0.900 | +0.555 [-0.276, +1.159] | 10.0 | -0.930 | +0.202 [-0.409, +0.435] | 15.0 | -0.913 | +0.547 [-0.795, +1.583] | 25.0 |
| 4h | SFP_harden | EXP_ALIGNED* | short | +0.366 | +0.280 [-0.026, +0.514] | 60.0 | +1.230 | +0.935 [-0.305, +1.532] | 55.0 | +1.105 | +0.106 [-0.624, +0.689] | 85.0 | -2.243 | -0.771 [-1.528, +1.902] | 15.0 |
| 4h | SFP_harden | EXP_COUNTER | both | +0.437 | +0.200 [-0.097, +0.420] | 75.0 | +0.340 | +0.131 [-0.494, +0.724] | 60.0 | +0.917 | +0.566 [-0.143, +0.767] | 85.0 | +3.187 | +0.453 [-0.363, +2.246] | 90.0 |
| 4h | SFP_harden | EXP_COUNTER | long | +0.453 | +0.167 [-0.035, +0.508] | 70.0 | +1.145 | +0.585 [-0.003, +1.181] | 75.0 | +0.466 | +0.477 [-0.322, +1.046] | 50.0 | +3.939 | +1.308 [-0.278, +2.268] | 85.0 |
| 4h | SFP_harden | EXP_COUNTER | short | +0.320 | +0.141 [-0.357, +0.456] | 70.0 | -0.566 | -0.114 [-0.989, +0.794] | 45.0 | +1.548 | +0.080 [-0.414, +0.844] | 100.0 | +1.020 | +0.691 [-1.796, +2.402] | 50.0 |
| 4h | SFP_harden | IN_RANGE_COINCIDENT* | both | +0.463 | +0.593 [+0.021, +1.300] | 36.8 | +1.532 | +0.595 [-0.211, +2.472] | 63.2 | +0.710 | +0.769 [+0.473, +1.551] | 50.0 | +3.080 | +2.350 [-0.240, +7.592] | 55.6 |
| 4h | SFP_harden | IN_RANGE_COINCIDENT* | long | +0.691 | +0.895 [+0.472, +1.487] | 41.2 | +1.900 | +1.374 [+0.126, +5.743] | 58.8 | +0.723 | +0.856 [+0.524, +1.448] | 46.7 | +3.544 | +6.450 [+1.220, +10.243] | 40.0 |
| 4h | SFP_harden | IN_RANGE_COINCIDENT* | short | -1.597 | -0.006 [-1.329, +1.426] | 20.0 | +1.488 | -0.294 [-3.169, +0.663] | 80.0 | -0.168 | +0.471 [-1.404, +1.965] | 45.5 | +2.269 | -0.585 [-3.220, +0.948] | 81.8 |
| 4h | SFP_harden | IN_RANGE_MID* | both | -0.474 | -0.157 [-0.335, +0.040] | 15.0 | -0.866 | -0.249 [-0.895, +0.261] | 30.0 | -0.849 | -0.078 [-0.440, +0.548] | 10.0 | -0.418 | -0.276 [-1.047, +0.383] | 45.0 |
| 4h | SFP_harden | IN_RANGE_MID* | long | -0.656 | -0.012 [-0.229, +0.113] | 0.0 | -1.092 | +0.003 [-0.664, +1.500] | 25.0 | -0.961 | -0.213 [-0.491, +0.250] | 20.0 | -0.953 | +0.211 [-1.024, +1.228] | 25.0 |
| 4h | SFP_harden | IN_RANGE_MID* | short | -0.483 | -0.331 [-0.761, +0.307] | 35.0 | -0.660 | -0.768 [-2.022, -0.128] | 55.0 | -0.492 | -0.236 [-0.673, +0.870] | 30.0 | -0.144 | -0.382 [-1.680, +1.211] | 70.0 |
| 4h | SFP_harden | IN_RANGE_OTHER | both | +0.264 | -0.017 [-0.366, +0.188] | 80.0 | +0.507 | -0.390 [-0.927, +0.226] | 75.0 | +0.434 | +0.092 [-0.521, +0.529] | 70.0 | +2.190 | -0.129 [-1.274, +1.607] | 80.0 |
| 4h | SFP_harden | IN_RANGE_OTHER | long | +0.290 | +0.177 [-0.426, +0.504] | 65.0 | +1.161 | -0.311 [-0.782, +0.878] | 80.0 | +0.331 | +0.116 [-0.682, +0.635] | 60.0 | +4.293 | +0.288 [-2.514, +2.086] | 85.0 |
| 4h | SFP_harden | IN_RANGE_OTHER | short | +0.188 | -0.051 [-0.505, +0.140] | 75.0 | -1.585 | -0.707 [-1.257, +0.508] | 20.0 | +0.639 | -0.543 [-0.873, +0.477] | 80.0 | -0.396 | +0.637 [-2.398, +1.526] | 40.0 |
| 4h | SFP_harden | NONE | both | — | -0.241 [-0.369, +0.202] | — | — | -0.497 [-7.066, +2.346] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | SFP_harden | NONE | long | — | -0.234 [-0.247, +0.546] | — | — | -8.742 [-13.302, -2.037] | — | — | — [—, —] | — | — | — [—, —] | — |
| 4h | SFP_harden | NONE | short | — | -0.330 [-0.382, -0.161] | — | — | +2.816 [+0.936, +6.177] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_first | ALL | both | -0.052 | -0.096 [-0.284, +0.143] | 65.0 | +0.259 | +0.265 [-0.251, +0.729] | 50.0 | -0.437 | -0.282 [-0.529, +0.208] | 35.0 | -0.429 | -0.024 [-0.963, +0.950] | 45.0 |
| 12h | BRK_tap89_first | ALL | long | +0.155 | -0.058 [-0.194, +0.258] | 70.0 | +1.306 | +1.544 [+0.692, +1.862] | 45.0 | -0.541 | -0.235 [-0.562, +0.374] | 25.0 | -0.363 | +1.441 [-0.300, +1.836] | 20.0 |
| 12h | BRK_tap89_first | ALL | short | -0.207 | -0.222 [-0.337, +0.095] | 60.0 | -0.844 | -1.115 [-1.833, +0.689] | 65.0 | -0.343 | -0.252 [-0.833, +0.498] | 40.0 | -0.848 | -1.228 [-2.428, +0.995] | 65.0 |
| 12h | BRK_tap89_first | EXP_ALIGNED* | both | -0.079 | -0.207 [-0.283, +0.356] | 60.0 | -0.221 | +0.144 [-0.647, +1.379] | 45.0 | -0.539 | -0.482 [-0.797, -0.335] | 35.0 | -1.930 | -2.276 [-3.492, -1.495] | 60.0 |
| 12h | BRK_tap89_first | EXP_ALIGNED* | long | +0.097 | +0.117 [-0.063, +0.393] | 45.0 | +0.502 | +0.786 [+0.024, +2.146] | 40.0 | -0.554 | -0.497 [-0.546, +0.706] | 25.0 | -0.544 | -1.017 [-2.000, -0.403] | 70.0 |
| 12h | BRK_tap89_first | EXP_ALIGNED* | short | -0.289 | -0.341 [-0.499, +0.130] | 65.0 | -1.976 | -1.746 [-2.963, -0.235] | 40.0 | -0.348 | -0.531 [-1.051, +0.051] | 55.0 | -3.021 | -3.008 [-4.489, -1.942] | 45.0 |
| 12h | BRK_tap89_first | EXP_COUNTER | both | -0.182 | -0.091 [-0.235, +0.273] | 30.0 | +1.896 | +0.701 [+0.288, +1.705] | 80.0 | -0.189 | +0.172 [-0.255, +0.357] | 35.0 | +2.980 | +2.517 [+1.928, +4.094] | 60.0 |
| 12h | BRK_tap89_first | EXP_COUNTER | long | +0.267 | -0.156 [-0.698, +0.254] | 75.0 | +2.326 | +1.862 [+0.599, +2.649] | 70.0 | -0.359 | +0.220 [-0.265, +0.680] | 20.0 | +4.097 | +3.667 [+2.056, +6.203] | 60.0 |
| 12h | BRK_tap89_first | EXP_COUNTER | short | -0.479 | +0.023 [-0.271, +0.458] | 25.0 | +1.065 | +0.146 [-0.877, +0.835] | 75.0 | -0.166 | +0.003 [-0.947, +0.999] | 33.3 | +2.753 | +1.644 [-0.814, +2.644] | 72.2 |
| 12h | BRK_tap89_first | IN_RANGE_COINCIDENT* | both | — | +1.473 [+0.808, +2.853] | — | — | +3.210 [+0.248, +4.486] | — | — | +0.142 [+0.142, +0.142] | — | — | +3.210 [+3.210, +3.210] | — |
| 12h | BRK_tap89_first | IN_RANGE_COINCIDENT* | long | — | +4.232 [+4.232, +4.232] | — | — | -2.714 [-2.714, -2.714] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_first | IN_RANGE_COINCIDENT* | short | — | +0.808 [+0.475, +1.141] | — | — | +4.486 [+3.848, +5.124] | — | — | +0.142 [+0.142, +0.142] | — | — | +3.210 [+3.210, +3.210] | — |
| 12h | BRK_tap89_first | IN_RANGE_MID* | both | +1.328 | +0.708 [-0.171, +1.018] | 90.0 | -0.862 | +0.703 [-0.882, +2.350] | 40.0 | +1.182 | +0.414 [-0.671, +1.033] | 80.0 | +3.233 | +1.022 [-1.430, +3.388] | 70.0 |
| 12h | BRK_tap89_first | IN_RANGE_MID* | long | -0.271 | -0.599 [-0.783, -0.156] | 75.0 | -0.855 | +1.263 [-0.444, +2.525] | 25.0 | -0.768 | -0.420 [-1.340, +1.023] | 42.1 | +0.172 | -1.200 [-3.346, +2.648] | 52.6 |
| 12h | BRK_tap89_first | IN_RANGE_MID* | short | +2.891 | +1.661 [+0.432, +2.098] | 85.0 | -0.845 | -0.668 [-1.438, +1.930] | 42.5 | +1.733 | +0.811 [+0.123, +1.600] | 84.2 | +3.233 | +0.056 [-1.585, +3.555] | 63.2 |
| 12h | BRK_tap89_first | IN_RANGE_OTHER | both | -0.953 | -0.817 [-1.660, +0.329] | 45.0 | -1.481 | -2.092 [-5.503, +1.179] | 65.0 | -3.241 | -1.623 [-2.494, -0.816] | 15.8 | -3.294 | -3.035 [-5.584, +0.644] | 47.4 |
| 12h | BRK_tap89_first | IN_RANGE_OTHER | long | +3.940 | +1.198 [-0.206, +2.648] | 90.0 | -1.481 | +6.083 [+1.506, +9.649] | 20.0 | +4.348 | +0.207 [-0.784, +1.156] | 100.0 | -1.456 | +10.221 [+0.595, +14.989] | 23.1 |
| 12h | BRK_tap89_first | IN_RANGE_OTHER | short | -1.747 | -2.453 [-2.512, -1.549] | 63.2 | -1.193 | -8.991 [-12.001, -5.615] | 84.2 | -4.028 | -2.547 [-4.131, -2.455] | 38.5 | -5.112 | -5.584 [-13.880, -5.584] | 92.3 |
| 12h | BRK_tap89_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | ALL | both | +0.180 | -0.073 [-0.318, +0.215] | 70.0 | -0.211 | +0.279 [-0.265, +0.772] | 35.0 | -0.521 | -0.325 [-0.521, +0.195] | 25.0 | -1.120 | -0.421 [-0.988, +1.193] | 25.0 |
| 12h | BRK_tap89_oneshot | ALL | long | +0.416 | +0.321 [-0.163, +0.477] | 60.0 | +1.546 | +1.963 [+1.092, +2.431] | 35.0 | -0.541 | +0.064 [-0.516, +0.467] | 15.0 | -0.486 | +2.103 [+0.238, +3.979] | 10.0 |
| 12h | BRK_tap89_oneshot | ALL | short | -0.179 | -0.324 [-0.475, -0.082] | 60.0 | -1.233 | -1.848 [-2.888, -0.816] | 65.0 | -0.344 | -0.311 [-0.955, +0.035] | 50.0 | -2.991 | -1.463 [-3.090, +0.286] | 35.0 |
| 12h | BRK_tap89_oneshot | EXP_ALIGNED* | both | -0.060 | -0.226 [-0.330, +0.097] | 60.0 | -0.340 | -0.214 [-0.571, +1.338] | 35.0 | -0.548 | -0.536 [-0.718, -0.514] | 40.0 | -2.461 | -1.918 [-3.000, -0.899] | 40.0 |
| 12h | BRK_tap89_oneshot | EXP_ALIGNED* | long | +0.129 | +0.146 [+0.014, +0.543] | 45.0 | +0.376 | +1.294 [+0.147, +2.235] | 40.0 | -0.557 | -0.516 [-0.544, -0.271] | 21.1 | -1.059 | -0.957 [-1.547, -0.310] | 47.4 |
| 12h | BRK_tap89_oneshot | EXP_ALIGNED* | short | -0.287 | -0.478 [-0.834, -0.260] | 70.0 | -2.870 | -2.914 [-4.463, -0.932] | 50.0 | -0.648 | -0.531 [-0.976, +0.051] | 50.0 | -3.311 | -3.008 [-4.495, -1.942] | 45.0 |
| 12h | BRK_tap89_oneshot | EXP_COUNTER | both | +0.186 | +0.194 [-0.486, +0.481] | 50.0 | +2.275 | +0.709 [+0.310, +1.783] | 75.0 | +0.164 | +0.172 [-0.386, +0.700] | 50.0 | +3.893 | +4.023 [+1.829, +6.126] | 45.0 |
| 12h | BRK_tap89_oneshot | EXP_COUNTER | long | +0.518 | -0.071 [-0.525, +0.564] | 70.0 | +3.104 | +1.451 [+0.373, +3.137] | 70.0 | +0.187 | +0.187 [-0.449, +0.970] | 52.6 | +6.126 | +6.053 [+2.019, +7.041] | 60.5 |
| 12h | BRK_tap89_oneshot | EXP_COUNTER | short | -0.328 | -0.186 [-0.858, +0.256] | 35.0 | +1.068 | +0.224 [-1.002, +1.041] | 75.0 | +0.011 | +0.019 [-0.559, +0.914] | 46.7 | +2.753 | +1.651 [-0.446, +3.451] | 73.3 |
| 12h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | IN_RANGE_MID* | both | +1.328 | +0.899 [+0.342, +1.098] | 80.0 | -1.012 | +1.973 [-0.915, +3.726] | 20.0 | +0.460 | +0.810 [-0.356, +1.311] | 36.8 | +3.367 | +3.623 [-0.114, +4.659] | 47.4 |
| 12h | BRK_tap89_oneshot | IN_RANGE_MID* | long | +0.409 | +0.179 [-0.402, +0.989] | 60.0 | +3.678 | +3.255 [-0.614, +4.036] | 55.0 | -0.768 | +0.985 [-0.885, +1.369] | 26.3 | +0.172 | +4.021 [-1.833, +5.538] | 31.6 |
| 12h | BRK_tap89_oneshot | IN_RANGE_MID* | short | +3.179 | +1.837 [+0.867, +2.899] | 95.0 | -4.980 | +0.652 [-2.775, +2.235] | 25.0 | +1.512 | +0.819 [-0.615, +1.512] | 76.5 | +3.367 | +1.033 [-1.383, +4.035] | 62.5 |
| 12h | BRK_tap89_oneshot | IN_RANGE_OTHER | both | +0.427 | -0.576 [-0.972, +0.736] | 70.0 | -3.546 | -3.974 [-7.031, -0.047] | 52.5 | -2.455 | -1.619 [-2.455, -0.613] | 27.8 | -5.112 | -1.240 [-7.999, +0.585] | 44.4 |
| 12h | BRK_tap89_oneshot | IN_RANGE_OTHER | long | +3.940 | +1.221 [+0.412, +3.048] | 90.0 | -1.481 | +7.177 [+3.632, +9.402] | 15.0 | +4.348 | -0.175 [-0.784, +1.177] | 100.0 | -1.456 | +13.257 [+0.595, +14.989] | 16.7 |
| 12h | BRK_tap89_oneshot | IN_RANGE_OTHER | short | -1.012 | -1.807 [-2.530, -1.145] | 73.7 | -5.105 | -9.631 [-12.126, -5.501] | 78.9 | -3.241 | -2.455 [-2.512, -2.455] | 0.0 | -9.496 | -13.880 [-13.880, -7.999] | 66.7 |
| 12h | BRK_tap89_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap89_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_first | ALL | both | +0.164 | +0.086 [+0.004, +0.195] | 60.0 | -0.416 | -0.357 [-1.053, +0.199] | 45.0 | +0.329 | +0.424 [+0.166, +0.923] | 30.0 | -0.477 | -1.113 [-1.637, +0.078] | 60.0 |
| 12h | BRK_tap127_first | ALL | long | +0.090 | +0.117 [-0.172, +0.373] | 50.0 | +0.422 | -0.217 [-0.807, +1.134] | 65.0 | +0.795 | +0.793 [-0.152, +0.926] | 50.0 | -1.563 | -1.655 [-3.064, +0.188] | 50.0 |
| 12h | BRK_tap127_first | ALL | short | +0.222 | +0.201 [+0.002, +0.357] | 55.0 | -0.552 | -0.632 [-1.768, -0.357] | 50.0 | +0.158 | +0.978 [+0.481, +1.303] | 15.0 | +0.208 | -0.409 [-1.557, +0.304] | 70.0 |
| 12h | BRK_tap127_first | EXP_ALIGNED* | both | -0.051 | +0.012 [-0.198, +0.381] | 50.0 | +0.214 | -0.609 [-1.735, +0.105] | 75.0 | +0.152 | +0.520 [-0.110, +0.704] | 35.0 | -3.218 | -3.597 [-4.013, -2.875] | 65.0 |
| 12h | BRK_tap127_first | EXP_ALIGNED* | long | -0.357 | -0.124 [-0.462, +0.182] | 35.0 | +1.292 | -0.565 [-1.622, +1.118] | 80.0 | -0.014 | -0.115 [-0.852, +0.694] | 50.0 | -3.367 | -3.738 [-3.990, -3.356] | 70.0 |
| 12h | BRK_tap127_first | EXP_ALIGNED* | short | +0.168 | +0.622 [+0.057, +0.928] | 30.0 | -0.241 | -0.450 [-2.437, +0.222] | 65.0 | +0.327 | +0.997 [+0.766, +1.510] | 13.2 | -0.680 | -0.774 [-4.770, +0.566] | 57.9 |
| 12h | BRK_tap127_first | EXP_COUNTER | both | +0.045 | -0.134 [-0.535, +0.191] | 60.0 | +0.219 | -0.461 [-1.134, +0.292] | 75.0 | -0.666 | +0.817 [-0.187, +1.140] | 10.5 | +2.059 | +2.048 [+1.048, +3.424] | 52.6 |
| 12h | BRK_tap127_first | EXP_COUNTER | long | +2.325 | +0.735 [+0.322, +1.218] | 95.0 | +1.128 | +0.612 [-0.350, +0.945] | 75.0 | +2.534 | +1.072 [+0.105, +1.492] | 84.2 | +3.188 | +1.885 [-0.325, +3.822] | 63.2 |
| 12h | BRK_tap127_first | EXP_COUNTER | short | -0.956 | -0.323 [-0.841, +0.065] | 10.0 | -0.166 | -1.752 [-2.240, -0.541] | 85.0 | -1.422 | +0.188 [-0.613, +0.432] | 23.5 | +2.079 | +2.083 [+0.826, +3.917] | 41.2 |
| 12h | BRK_tap127_first | IN_RANGE_COINCIDENT* | both | +1.241 | -0.325 [-1.410, +1.241] | 75.0 | +14.022 | +4.059 [+1.866, +6.769] | 87.5 | +1.241 | +0.712 [-0.452, +1.241] | 75.0 | +14.022 | +9.064 [+4.083, +14.022] | 75.0 |
| 12h | BRK_tap127_first | IN_RANGE_COINCIDENT* | long | +1.241 | +1.241 [-0.833, +1.241] | 60.0 | +14.022 | +4.013 [-1.349, +14.022] | 80.0 | +1.241 | +1.241 [-0.558, +1.241] | 66.7 | +14.022 | +14.022 [+9.017, +14.022] | 66.7 |
| 12h | BRK_tap127_first | IN_RANGE_COINCIDENT* | short | — | -1.094 [-2.922, -0.455] | — | — | +4.106 [+3.522, +4.228] | — | — | +0.184 [+0.184, +0.184] | — | — | +4.106 [+4.106, +4.106] | — |
| 12h | BRK_tap127_first | IN_RANGE_MID* | both | +0.762 | +0.411 [+0.010, +1.046] | 65.0 | -0.818 | +0.532 [-0.185, +2.838] | 20.0 | +0.763 | +0.922 [+0.410, +1.092] | 45.0 | +0.948 | +1.771 [-0.447, +3.959] | 40.0 |
| 12h | BRK_tap127_first | IN_RANGE_MID* | long | -0.225 | +0.086 [-0.625, +0.701] | 40.0 | -0.830 | +0.356 [-1.595, +1.972] | 30.0 | -0.768 | +0.730 [-0.054, +1.162] | 10.0 | +0.172 | +1.029 [-1.853, +5.651] | 35.0 |
| 12h | BRK_tap127_first | IN_RANGE_MID* | short | +1.291 | +1.061 [+0.292, +1.357] | 75.0 | -0.826 | +0.521 [-0.750, +4.260] | 25.0 | +1.298 | +1.071 [+0.905, +1.538] | 65.0 | +0.948 | +3.224 [+0.612, +4.921] | 40.0 |
| 12h | BRK_tap127_first | IN_RANGE_OTHER | both | +0.617 | -0.347 [-1.223, +0.571] | 75.0 | -2.522 | -2.161 [-3.661, -0.368] | 45.0 | +2.963 | -0.796 [-1.110, +0.301] | 100.0 | -1.497 | -4.502 [-6.995, -2.263] | 77.8 |
| 12h | BRK_tap127_first | IN_RANGE_OTHER | long | +0.016 | +0.052 [-1.344, +1.991] | 42.1 | -1.489 | +4.091 [+2.017, +8.094] | 21.1 | +0.975 | -2.838 [-4.264, -0.114] | 75.0 | +1.258 | +8.128 [+5.550, +8.349] | 0.0 |
| 12h | BRK_tap127_first | IN_RANGE_OTHER | short | +1.232 | -0.551 [-1.314, -0.021] | 88.9 | -5.098 | -5.918 [-11.383, -2.803] | 55.6 | +2.984 | -0.726 [-1.038, +1.237] | 100.0 | -6.823 | -8.603 [-13.904, -4.254] | 62.5 |
| 12h | BRK_tap127_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_oneshot | ALL | both | +0.305 | +0.202 [+0.002, +0.365] | 65.0 | +0.213 | -0.172 [-0.570, +0.673] | 60.0 | +0.379 | +1.085 [+0.395, +1.307] | 25.0 | -0.110 | -0.083 [-0.869, +1.185] | 45.0 |
| 12h | BRK_tap127_oneshot | ALL | long | +0.390 | +0.088 [-0.208, +0.383] | 75.0 | +1.340 | +1.161 [+0.266, +1.293] | 85.0 | +0.434 | +0.984 [-0.626, +1.324] | 40.0 | -0.430 | +0.252 [-2.583, +2.933] | 35.0 |
| 12h | BRK_tap127_oneshot | ALL | short | +0.272 | +0.381 [+0.135, +0.571] | 35.0 | -0.666 | -0.520 [-1.753, -0.210] | 45.0 | +0.327 | +1.249 [+1.027, +1.533] | 10.0 | +0.212 | +0.183 [-1.219, +1.773] | 50.0 |
| 12h | BRK_tap127_oneshot | EXP_ALIGNED* | both | -0.003 | +0.161 [-0.085, +0.386] | 35.0 | +0.927 | +0.124 [-0.741, +1.138] | 70.0 | +0.152 | +0.954 [-0.096, +1.543] | 30.0 | -1.870 | -1.567 [-3.533, -0.599] | 40.0 |
| 12h | BRK_tap127_oneshot | EXP_ALIGNED* | long | -0.047 | -0.075 [-0.369, +0.300] | 50.0 | +1.308 | +0.735 [-1.275, +1.297] | 80.0 | -0.014 | +0.054 [-1.176, +1.572] | 45.0 | -3.050 | -3.129 [-3.757, -1.746] | 55.0 |
| 12h | BRK_tap127_oneshot | EXP_ALIGNED* | short | +0.168 | +0.531 [-0.092, +0.856] | 30.0 | -0.241 | -0.560 [-1.685, +1.154] | 60.0 | +0.327 | +1.149 [+0.541, +1.702] | 18.4 | -0.680 | -0.771 [-3.361, +0.878] | 57.9 |
| 12h | BRK_tap127_oneshot | EXP_COUNTER | both | +0.173 | -0.314 [-0.628, +0.088] | 75.0 | +0.227 | -0.367 [-0.823, +0.871] | 60.0 | -0.249 | +0.762 [-0.272, +1.233] | 26.3 | +5.950 | +4.371 [+1.291, +5.659] | 73.7 |
| 12h | BRK_tap127_oneshot | EXP_COUNTER | long | +3.266 | +1.110 [+0.446, +2.366] | 95.0 | +8.004 | +0.953 [+0.444, +2.120] | 95.0 | +3.836 | +1.585 [+0.280, +3.143] | 80.0 | +8.004 | +4.828 [+2.949, +9.401] | 60.0 |
| 12h | BRK_tap127_oneshot | EXP_COUNTER | short | -1.196 | -0.695 [-1.104, -0.059] | 25.0 | -0.892 | -0.858 [-2.156, +1.351] | 50.0 | -1.422 | +0.163 [-0.642, +0.642] | 6.2 | +3.916 | +2.479 [+0.836, +4.982] | 56.2 |
| 12h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | both | +1.241 | -0.963 [-2.041, +0.723] | 83.3 | +14.022 | +4.182 [+3.207, +11.604] | 83.3 | +1.241 | +1.241 [-0.558, +1.241] | 66.7 | +14.022 | +14.022 [+9.017, +14.022] | 66.7 |
| 12h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | long | +1.241 | +0.204 [-1.214, +1.241] | 75.0 | +14.022 | +9.017 [+2.673, +14.022] | 75.0 | +1.241 | +1.241 [-0.558, +1.241] | 66.7 | +14.022 | +14.022 [+9.017, +14.022] | 66.7 |
| 12h | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | short | — | -2.922 [-3.836, -2.008] | — | — | +3.644 [+3.291, +3.998] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_oneshot | IN_RANGE_MID* | both | +1.071 | +0.711 [+0.230, +1.038] | 75.0 | -1.140 | +0.389 [-0.811, +2.887] | 20.0 | +0.763 | +1.068 [+0.564, +1.305] | 35.0 | +1.592 | +2.256 [+0.247, +3.969] | 40.0 |
| 12h | BRK_tap127_oneshot | IN_RANGE_MID* | long | +0.409 | +0.062 [-0.522, +0.993] | 65.0 | -1.375 | +0.805 [-1.447, +2.163] | 30.0 | -0.768 | +0.986 [-0.624, +1.180] | 21.1 | +0.172 | +0.364 [-3.255, +4.010] | 47.4 |
| 12h | BRK_tap127_oneshot | IN_RANGE_MID* | short | +1.289 | +1.065 [+0.980, +1.849] | 70.0 | -0.828 | +0.784 [-1.180, +4.436] | 35.0 | +1.298 | +1.076 [+1.047, +1.885] | 57.9 | +2.157 | +4.058 [+2.205, +6.181] | 26.3 |
| 12h | BRK_tap127_oneshot | IN_RANGE_OTHER | both | +1.219 | -0.746 [-1.348, +1.464] | 73.7 | -1.489 | -0.670 [-3.545, +2.085] | 42.1 | +2.963 | -0.565 [-3.134, +1.241] | 88.2 | -1.497 | -3.511 [-6.823, +3.968] | 64.7 |
| 12h | BRK_tap127_oneshot | IN_RANGE_OTHER | long | +1.485 | +0.965 [-1.560, +2.337] | 72.2 | +1.266 | +5.725 [+3.720, +8.120] | 11.1 | +0.975 | -2.838 [-4.264, -0.114] | 75.0 | +1.258 | +8.128 [+5.550, +8.349] | 0.0 |
| 12h | BRK_tap127_oneshot | IN_RANGE_OTHER | short | +1.232 | -0.957 [-2.289, +1.141] | 72.2 | -5.098 | -5.965 [-9.668, -2.875] | 50.0 | +2.984 | -0.161 [-3.134, +2.488] | 92.3 | -6.823 | -4.515 [-18.986, -3.511] | 38.5 |
| 12h | BRK_tap127_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap127_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_first | ALL | both | +0.147 | +0.273 [+0.141, +0.530] | 30.0 | -0.249 | +0.280 [-0.542, +0.619] | 35.0 | +0.087 | +0.243 [-0.051, +0.500] | 40.0 | -0.223 | -1.152 [-1.731, +0.116] | 65.0 |
| 12h | BRK_tap200_first | ALL | long | +0.183 | +0.435 [+0.135, +1.021] | 25.0 | -1.020 | -1.177 [-1.301, +0.392] | 55.0 | -0.112 | +0.484 [-0.065, +0.715] | 20.0 | -1.550 | -1.677 [-2.163, -0.532] | 60.0 |
| 12h | BRK_tap200_first | ALL | short | +0.137 | +0.088 [-0.009, +0.343] | 55.0 | +0.010 | +0.781 [-0.258, +1.890] | 30.0 | +0.223 | +0.264 [-0.031, +0.817] | 45.0 | +0.071 | +0.012 [-0.959, +0.933] | 50.0 |
| 12h | BRK_tap200_first | EXP_ALIGNED* | both | +0.664 | +0.662 [+0.315, +1.074] | 50.0 | +1.001 | +0.181 [-1.000, +1.144] | 70.0 | +1.304 | +1.350 [+0.657, +1.671] | 45.0 | -1.616 | -2.097 [-2.877, -1.704] | 75.0 |
| 12h | BRK_tap200_first | EXP_ALIGNED* | long | +0.664 | +0.765 [+0.183, +1.069] | 40.0 | +1.131 | +0.208 [-0.571, +0.998] | 80.0 | +0.677 | +0.943 [+0.019, +1.673] | 45.0 | -1.722 | -1.771 [-2.760, -1.642] | 60.0 |
| 12h | BRK_tap200_first | EXP_ALIGNED* | short | +0.506 | +0.561 [+0.135, +1.308] | 50.0 | +0.569 | -0.833 [-2.143, +0.769] | 75.0 | +1.392 | +2.201 [+1.436, +2.815] | 22.2 | -0.049 | -2.166 [-2.735, -0.880] | 88.9 |
| 12h | BRK_tap200_first | EXP_COUNTER | both | -0.553 | -0.357 [-0.535, -0.178] | 20.0 | -1.053 | +0.022 [-0.754, +1.870] | 15.0 | -0.444 | -0.651 [-1.124, -0.299] | 55.0 | +2.751 | +2.032 [+1.281, +4.400] | 55.0 |
| 12h | BRK_tap200_first | EXP_COUNTER | long | -0.104 | -0.852 [-2.265, +1.200] | 65.0 | -0.878 | -0.289 [-1.448, +3.054] | 30.0 | -0.104 | -1.690 [-2.812, -0.081] | 75.0 | +4.099 | +2.533 [+1.100, +4.402] | 59.4 |
| 12h | BRK_tap200_first | EXP_COUNTER | short | -0.666 | -0.321 [-0.499, +0.001] | 15.0 | -1.238 | +0.051 [-1.187, +1.951] | 25.0 | -0.593 | -0.429 [-0.835, -0.145] | 39.5 | -0.034 | +1.809 [-0.615, +3.354] | 42.1 |
| 12h | BRK_tap200_first | IN_RANGE_COINCIDENT* | both | +1.001 | -0.851 [-2.241, +0.566] | 80.0 | +0.805 | -0.407 [-2.697, +6.625] | 60.0 | +1.001 | +0.286 [-0.527, +0.473] | 100.0 | +0.805 | +3.114 [-0.632, +5.455] | 33.3 |
| 12h | BRK_tap200_first | IN_RANGE_COINCIDENT* | long | +1.122 | -0.851 [-2.177, +0.872] | 66.7 | -1.172 | -1.458 [-2.697, -1.370] | 83.3 | +1.001 | -1.341 [-1.341, -1.341] | 100.0 | +0.805 | -4.379 [-4.379, -4.379] | 100.0 |
| 12h | BRK_tap200_first | IN_RANGE_COINCIDENT* | short | -0.371 | -0.720 [-3.886, +0.286] | 60.0 | +3.392 | +3.114 [+2.525, +7.796] | 60.0 | — | +0.473 [+0.379, +0.566] | — | — | +5.455 [+4.285, +6.625] | — |
| 12h | BRK_tap200_first | IN_RANGE_MID* | both | +0.177 | +0.413 [-0.041, +0.744] | 35.0 | -0.833 | +0.848 [-0.512, +2.932] | 25.0 | -0.101 | +0.416 [+0.002, +0.834] | 25.0 | -0.205 | +0.133 [-1.510, +1.308] | 35.0 |
| 12h | BRK_tap200_first | IN_RANGE_MID* | long | -0.385 | -0.002 [-0.279, +0.481] | 25.0 | -3.038 | -1.003 [-2.407, +2.033] | 15.0 | -1.355 | +0.465 [+0.203, +0.794] | 0.0 | -3.035 | -0.276 [-2.968, +0.620] | 23.7 |
| 12h | BRK_tap200_first | IN_RANGE_MID* | short | +1.598 | +0.769 [-0.163, +1.707] | 60.0 | +0.065 | +2.628 [+0.713, +4.071] | 20.0 | +0.196 | +0.333 [-0.108, +1.423] | 31.6 | +0.575 | +0.937 [-2.014, +2.433] | 47.4 |
| 12h | BRK_tap200_first | IN_RANGE_OTHER | both | +0.314 | +0.667 [+0.087, +1.292] | 40.0 | -4.331 | -3.140 [-6.101, -0.140] | 35.0 | +0.610 | -0.306 [-0.949, +0.342] | 75.0 | -4.727 | -5.887 [-10.120, -0.864] | 50.0 |
| 12h | BRK_tap200_first | IN_RANGE_OTHER | long | -0.579 | +1.002 [+0.216, +1.313] | 10.5 | -3.540 | -3.140 [-3.331, -1.166] | 18.4 | +1.875 | -0.579 [-0.579, +0.228] | 93.3 | -4.714 | -7.953 [-7.953, -2.277] | 53.3 |
| 12h | BRK_tap200_first | IN_RANGE_OTHER | short | +1.220 | -0.821 [-2.190, +0.766] | 85.0 | -5.109 | -4.589 [-12.019, +1.073] | 40.0 | -0.189 | -0.311 [-2.190, +0.528] | 52.6 | -4.815 | -6.401 [-13.529, +2.435] | 52.6 |
| 12h | BRK_tap200_first | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_first | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_oneshot | ALL | both | +0.301 | +0.378 [+0.202, +0.693] | 35.0 | -0.754 | +0.283 [-0.890, +0.659] | 30.0 | +0.309 | +0.362 [+0.165, +0.678] | 40.0 | -0.295 | -1.658 [-2.566, -0.874] | 85.0 |
| 12h | BRK_tap200_oneshot | ALL | long | +0.411 | +0.445 [+0.107, +1.070] | 40.0 | -1.176 | -0.871 [-1.240, -0.208] | 45.0 | -0.105 | +0.463 [+0.081, +0.857] | 15.0 | -1.611 | -2.510 [-3.135, -1.647] | 75.0 |
| 12h | BRK_tap200_oneshot | ALL | short | +0.272 | +0.260 [-0.116, +0.778] | 55.0 | -0.223 | +0.490 [-0.429, +2.175] | 25.0 | +0.810 | +0.281 [-0.342, +1.067] | 65.0 | +0.010 | -0.440 [-1.271, +0.278] | 65.0 |
| 12h | BRK_tap200_oneshot | EXP_ALIGNED* | both | +0.580 | +0.660 [+0.295, +1.068] | 40.0 | +0.574 | +0.464 [-0.704, +1.367] | 60.0 | +1.377 | +1.325 [+0.711, +1.678] | 55.0 | -1.667 | -2.386 [-3.739, -1.730] | 80.0 |
| 12h | BRK_tap200_oneshot | EXP_ALIGNED* | long | +0.664 | +0.834 [-0.034, +1.071] | 45.0 | +1.131 | -0.205 [-1.198, +0.584] | 80.0 | +1.146 | +0.938 [+0.616, +1.644] | 52.6 | -2.741 | -3.727 [-3.750, -2.198] | 63.2 |
| 12h | BRK_tap200_oneshot | EXP_ALIGNED* | short | +0.287 | +0.293 [+0.051, +1.418] | 40.0 | +0.549 | -0.041 [-1.355, +2.258] | 60.0 | +1.392 | +2.113 [+1.330, +2.829] | 41.2 | -0.049 | -1.590 [-1.885, -0.626] | 88.2 |
| 12h | BRK_tap200_oneshot | EXP_COUNTER | both | -0.434 | -0.090 [-0.499, +0.980] | 30.0 | -1.053 | -0.135 [-0.819, +2.620] | 25.0 | -0.439 | -0.364 [-2.220, +0.576] | 40.0 | +2.751 | +1.275 [-1.277, +3.416] | 70.0 |
| 12h | BRK_tap200_oneshot | EXP_COUNTER | long | +0.711 | -0.393 [-1.265, +1.468] | 60.0 | +0.263 | +0.889 [-0.595, +2.500] | 40.0 | -0.104 | -1.258 [-3.322, +1.526] | 60.0 | +4.099 | +2.362 [-3.347, +6.480] | 53.3 |
| 12h | BRK_tap200_oneshot | EXP_COUNTER | short | -1.137 | -0.237 [-0.427, +0.128] | 10.0 | -2.718 | +0.130 [-1.748, +1.528] | 15.0 | -0.736 | -0.307 [-0.736, +0.044] | 26.5 | -0.012 | -0.648 [-2.855, +3.335] | 61.8 |
| 12h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | both | +1.001 | -0.851 [-2.241, +0.566] | 80.0 | +0.805 | -0.407 [-2.697, +6.625] | 60.0 | +1.001 | +0.286 [-0.527, +0.473] | 100.0 | +0.805 | +3.114 [-0.632, +5.455] | 33.3 |
| 12h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | long | +1.122 | -0.851 [-2.177, +0.872] | 66.7 | -1.172 | -1.458 [-2.697, -1.370] | 83.3 | +1.001 | -1.341 [-1.341, -1.341] | 100.0 | +0.805 | -4.379 [-4.379, -4.379] | 100.0 |
| 12h | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | short | -0.371 | -0.720 [-3.886, +0.286] | 60.0 | +3.392 | +3.114 [+2.525, +7.796] | 60.0 | — | +0.473 [+0.379, +0.566] | — | — | +5.455 [+4.285, +6.625] | — |
| 12h | BRK_tap200_oneshot | IN_RANGE_MID* | both | +0.313 | +0.421 [-0.072, +0.818] | 35.0 | -1.376 | +1.096 [-0.974, +2.445] | 20.0 | -0.739 | +0.455 [+0.250, +0.935] | 10.0 | -0.252 | +0.117 [-1.512, +2.194] | 50.0 |
| 12h | BRK_tap200_oneshot | IN_RANGE_MID* | long | -0.385 | -0.071 [-0.404, +0.662] | 40.0 | -3.038 | -1.821 [-2.571, +1.342] | 20.0 | -1.355 | +0.468 [-0.102, +0.865] | 0.0 | -3.035 | -1.303 [-3.041, +2.705] | 34.2 |
| 12h | BRK_tap200_oneshot | IN_RANGE_MID* | short | +3.776 | +1.491 [+0.010, +2.736] | 90.0 | -0.083 | +2.779 [-0.198, +4.246] | 25.0 | +0.316 | +0.668 [-0.753, +1.438] | 36.1 | +0.078 | +0.240 [-3.917, +0.961] | 44.4 |
| 12h | BRK_tap200_oneshot | IN_RANGE_OTHER | both | +0.314 | +0.978 [+0.532, +1.473] | 25.0 | -4.331 | -3.143 [-5.211, -1.176] | 30.0 | +0.610 | -0.548 [-0.949, +0.301] | 80.0 | -4.727 | -7.773 [-10.120, -2.080] | 55.0 |
| 12h | BRK_tap200_oneshot | IN_RANGE_OTHER | long | -0.579 | +1.066 [+0.776, +1.874] | 11.1 | -3.540 | -2.201 [-3.271, -1.164] | 19.4 | +1.875 | -0.454 [-0.579, +0.240] | 92.9 | -4.714 | -5.809 [-7.953, -1.936] | 50.0 |
| 12h | BRK_tap200_oneshot | IN_RANGE_OTHER | short | +1.220 | -1.061 [-2.440, +0.958] | 75.0 | -5.109 | -8.335 [-12.285, +0.822] | 50.0 | -0.189 | -0.895 [-2.190, +0.659] | 63.2 | -4.815 | -12.279 [-13.529, -1.747] | 57.9 |
| 12h | BRK_tap200_oneshot | NONE | both | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_tap200_oneshot | NONE | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_first | ALL | both | +0.274 | +0.080 [-0.238, +0.227] | 80.0 | -0.635 | +0.015 [-0.441, +0.644] | 20.0 | +0.089 | +0.057 [-0.160, +0.411] | 55.0 | -1.111 | +0.203 [-0.827, +1.318] | 25.0 |
| 12h | BRK_mem_first | ALL | long | +0.215 | +0.157 [-0.240, +0.360] | 50.0 | +0.004 | +0.633 [-0.128, +1.236] | 30.0 | +0.076 | +0.165 [-0.523, +0.661] | 45.0 | -1.026 | +0.265 [-0.693, +0.715] | 20.0 |
| 12h | BRK_mem_first | ALL | short | +0.543 | -0.094 [-0.540, +0.251] | 90.0 | -1.290 | -0.824 [-1.274, -0.338] | 25.0 | +0.102 | +0.068 [-0.283, +0.188] | 50.0 | -1.098 | -0.620 [-1.366, +0.936] | 40.0 |
| 12h | BRK_mem_first | EXP_ALIGNED* | both | +0.336 | -0.327 [-0.493, -0.042] | 100.0 | -0.393 | -0.401 [-0.899, +0.439] | 50.0 | -0.143 | -0.009 [-0.635, +0.465] | 40.0 | -1.636 | -2.169 [-2.618, -1.034] | 65.0 |
| 12h | BRK_mem_first | EXP_ALIGNED* | long | -0.191 | -0.225 [-0.781, +0.092] | 50.0 | +0.600 | +0.308 [-0.600, +1.157] | 60.0 | -0.183 | +0.790 [-1.278, +1.317] | 40.0 | -1.270 | -0.659 [-2.212, +1.341] | 40.0 |
| 12h | BRK_mem_first | EXP_ALIGNED* | short | +0.844 | -0.418 [-1.120, +0.362] | 85.0 | -1.385 | -2.481 [-3.560, -1.046] | 70.0 | +0.631 | -0.344 [-1.077, +0.362] | 80.0 | -1.887 | -2.340 [-6.341, -0.926] | 60.0 |
| 12h | BRK_mem_first | EXP_COUNTER | both | -0.015 | +0.086 [-0.197, +0.498] | 40.0 | -1.164 | +1.049 [-0.108, +2.960] | 5.0 | +0.262 | -0.087 [-0.897, +0.653] | 65.0 | +4.394 | +2.720 [+0.771, +4.069] | 75.0 |
| 12h | BRK_mem_first | EXP_COUNTER | long | +0.521 | +0.219 [-0.355, +0.904] | 70.0 | -0.074 | +2.448 [+0.461, +3.716] | 20.0 | +0.520 | +0.065 [-0.960, +0.948] | 70.6 | +4.865 | +2.200 [+0.795, +3.947] | 76.5 |
| 12h | BRK_mem_first | EXP_COUNTER | short | -0.388 | +0.175 [-0.433, +0.591] | 30.0 | -1.814 | +0.252 [-1.079, +1.213] | 25.0 | +0.007 | -0.371 [-0.713, +1.140] | 60.0 | +3.926 | +2.615 [-1.590, +4.293] | 73.3 |
| 12h | BRK_mem_first | IN_RANGE_COINCIDENT* | both | -0.417 | +0.634 [-1.270, +1.341] | 33.3 | +2.217 | -0.356 [-2.621, +3.488] | 55.6 | +0.206 | +0.634 [-1.463, +0.634] | 33.3 | +1.176 | +13.122 [-1.697, +13.122] | 33.3 |
| 12h | BRK_mem_first | IN_RANGE_COINCIDENT* | long | +0.206 | +0.763 [+0.634, +1.341] | 14.3 | +1.176 | -0.356 [-2.621, +6.408] | 71.4 | +0.206 | +0.634 [-1.463, +0.634] | 33.3 | +1.176 | +13.122 [-1.697, +13.122] | 33.3 |
| 12h | BRK_mem_first | IN_RANGE_COINCIDENT* | short | -1.009 | -0.877 [-1.270, +0.031] | 50.0 | +3.288 | +3.203 [+1.413, +3.488] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_first | IN_RANGE_MID* | both | +1.474 | -0.299 [-0.878, +0.902] | 90.0 | -1.039 | +0.540 [-0.925, +2.282] | 25.0 | -0.322 | +0.011 [-0.424, +1.396] | 35.0 | -1.075 | -0.091 [-2.334, +2.417] | 35.0 |
| 12h | BRK_mem_first | IN_RANGE_MID* | long | -1.588 | +0.382 [-0.961, +0.791] | 10.0 | -1.140 | +0.405 [-1.170, +4.002] | 25.0 | -2.621 | +0.262 [-1.468, +1.028] | 10.5 | -1.132 | -0.311 [-2.805, +1.082] | 47.4 |
| 12h | BRK_mem_first | IN_RANGE_MID* | short | +1.993 | +0.035 [-1.807, +1.401] | 85.0 | +0.239 | -0.879 [-1.701, +1.769] | 65.0 | +1.983 | +0.316 [-0.132, +1.995] | 72.2 | -1.011 | +1.399 [-0.901, +4.682] | 27.8 |
| 12h | BRK_mem_first | IN_RANGE_OTHER | both | +0.421 | +0.311 [-0.081, +1.075] | 55.0 | -0.868 | -0.335 [-1.235, +1.827] | 30.0 | +0.710 | -0.122 [-0.412, +1.576] | 57.9 | -0.973 | +2.413 [-2.295, +2.912] | 42.1 |
| 12h | BRK_mem_first | IN_RANGE_OTHER | long | +1.558 | +1.007 [-0.104, +1.647] | 70.0 | -0.765 | -0.552 [-1.644, +2.568] | 45.0 | +3.590 | +1.039 [-0.406, +2.566] | 88.2 | -2.008 | +1.424 [-2.866, +5.572] | 35.3 |
| 12h | BRK_mem_first | IN_RANGE_OTHER | short | +0.104 | +0.093 [-0.456, +0.459] | 50.0 | -1.096 | -0.804 [-3.036, +0.363] | 50.0 | -0.121 | +0.011 [-0.512, +0.991] | 50.0 | +0.297 | +1.849 [-1.233, +3.109] | 38.9 |
| 12h | BRK_mem_first | NONE | both | — | +1.934 [+1.934, +1.934] | — | — | +5.287 [+5.287, +5.287] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_first | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_first | NONE | short | — | +1.934 [+1.934, +1.934] | — | — | +5.287 [+5.287, +5.287] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_oneshot | ALL | both | +0.224 | +0.083 [-0.253, +0.224] | 75.0 | -0.538 | -0.157 [-0.461, +0.533] | 25.0 | -0.031 | +0.194 [-0.265, +0.637] | 35.0 | -1.080 | +0.430 [-0.593, +1.082] | 15.0 |
| 12h | BRK_mem_oneshot | ALL | long | +0.265 | +0.225 [-0.137, +0.427] | 50.0 | +0.004 | +0.513 [-0.303, +1.256] | 30.0 | -0.055 | +0.184 [-0.421, +0.621] | 35.0 | -1.166 | +0.507 [-1.440, +1.402] | 30.0 |
| 12h | BRK_mem_oneshot | ALL | short | +0.042 | -0.085 [-0.547, +0.225] | 60.0 | -1.075 | -1.118 [-1.455, -0.404] | 55.0 | -0.007 | -0.068 [-0.655, +0.203] | 50.0 | -1.041 | -0.724 [-1.920, +0.389] | 40.0 |
| 12h | BRK_mem_oneshot | EXP_ALIGNED* | both | +0.264 | -0.250 [-0.666, +0.206] | 90.0 | -0.387 | -0.286 [-0.807, +0.281] | 35.0 | -0.372 | -0.154 [-1.161, +0.342] | 45.0 | -2.202 | -1.616 [-2.566, -0.011] | 40.0 |
| 12h | BRK_mem_oneshot | EXP_ALIGNED* | long | -0.191 | -0.328 [-0.784, +0.185] | 60.0 | +0.090 | +0.521 [+0.014, +1.407] | 25.0 | -0.517 | -0.288 [-1.255, +0.848] | 35.3 | -2.822 | -0.587 [-1.689, +2.657] | 5.9 |
| 12h | BRK_mem_oneshot | EXP_ALIGNED* | short | +0.765 | -0.357 [-1.007, +0.607] | 85.0 | -0.954 | -1.595 [-2.697, -1.075] | 75.0 | +0.487 | -0.561 [-1.104, +0.642] | 70.0 | -1.681 | -2.562 [-7.362, -1.177] | 65.0 |
| 12h | BRK_mem_oneshot | EXP_COUNTER | both | -0.011 | +0.338 [-0.016, +0.563] | 30.0 | -1.124 | +1.389 [-0.303, +2.272] | 10.0 | +0.262 | -0.069 [-0.478, +0.678] | 65.0 | +4.394 | +1.196 [+0.484, +3.404] | 75.0 |
| 12h | BRK_mem_oneshot | EXP_COUNTER | long | +0.536 | +0.657 [+0.091, +1.021] | 45.0 | +0.123 | +2.538 [+1.190, +3.733] | 15.0 | +0.520 | -0.132 [-0.670, +1.057] | 63.2 | +4.865 | +1.228 [-1.129, +2.723] | 84.2 |
| 12h | BRK_mem_oneshot | EXP_COUNTER | short | -0.604 | -0.021 [-0.433, +0.376] | 15.0 | -1.771 | +0.628 [-1.022, +2.203] | 25.0 | +0.007 | -0.286 [-0.693, +1.145] | 68.8 | +3.926 | +0.347 [-6.268, +2.678] | 81.2 |
| 12h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | both | -0.417 | +0.634 [-1.270, +1.052] | 45.5 | +2.217 | -1.708 [-3.409, +3.488] | 63.6 | +0.206 | -0.467 [-2.067, +0.634] | 50.0 | +1.176 | +2.945 [-9.553, +13.122] | 50.0 |
| 12h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | long | +0.206 | +0.634 [-1.219, +1.341] | 33.3 | +1.176 | -2.621 [-4.196, -0.305] | 77.8 | +0.206 | -0.467 [-2.067, +0.634] | 50.0 | +1.176 | +2.945 [-9.553, +13.122] | 50.0 |
| 12h | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | short | -1.009 | -0.877 [-1.270, +0.031] | 50.0 | +3.288 | +3.203 [+1.413, +3.488] | 50.0 | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_oneshot | IN_RANGE_MID* | both | -1.824 | -0.006 [-1.157, +0.675] | 10.0 | -1.148 | -0.401 [-1.070, +0.998] | 25.0 | -2.214 | +0.360 [-0.703, +0.714] | 0.0 | -1.075 | -1.035 [-2.380, +2.445] | 42.1 |
| 12h | BRK_mem_oneshot | IN_RANGE_MID* | long | -2.109 | +0.175 [-1.214, +0.625] | 10.0 | -2.996 | -0.003 [-2.561, +2.326] | 5.0 | -4.232 | -0.549 [-1.470, +1.783] | 5.9 | -3.122 | -2.650 [-3.521, +1.415] | 35.3 |
| 12h | BRK_mem_oneshot | IN_RANGE_MID* | short | -1.837 | -0.616 [-2.023, +0.902] | 27.8 | -1.048 | -1.040 [-2.015, +1.827] | 44.4 | +0.089 | +0.316 [-0.660, +1.546] | 43.8 | +1.130 | -0.634 [-1.418, +2.288] | 62.5 |
| 12h | BRK_mem_oneshot | IN_RANGE_OTHER | both | +0.353 | +0.498 [-0.180, +1.367] | 40.0 | +0.094 | -0.366 [-1.709, +1.462] | 60.0 | +0.113 | +0.702 [-0.504, +1.811] | 38.9 | -0.853 | -0.366 [-2.232, +2.436] | 50.0 |
| 12h | BRK_mem_oneshot | IN_RANGE_OTHER | long | +0.638 | +0.447 [-0.409, +1.094] | 60.0 | +0.636 | +0.597 [-1.350, +3.457] | 50.0 | +2.579 | -0.144 [-0.406, +2.853] | 70.6 | -0.850 | -1.125 [-2.686, +2.875] | 52.9 |
| 12h | BRK_mem_oneshot | IN_RANGE_OTHER | short | -0.131 | +0.583 [-0.464, +1.537] | 40.0 | -0.120 | -1.033 [-3.236, +0.946] | 55.0 | -0.125 | +0.897 [+0.009, +1.719] | 25.0 | -0.114 | +1.194 [-1.734, +2.444] | 37.5 |
| 12h | BRK_mem_oneshot | NONE | both | — | +1.934 [+1.934, +1.934] | — | — | +5.287 [+5.287, +5.287] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_oneshot | NONE | long | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | BRK_mem_oneshot | NONE | short | — | +1.934 [+1.934, +1.934] | — | — | +5.287 [+5.287, +5.287] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | SFP_harden | ALL | both | -0.028 | +0.006 [-0.197, +0.126] | 50.0 | +0.854 | -0.081 [-0.581, +0.865] | 75.0 | +0.088 | +0.036 [-0.334, +0.425] | 55.0 | +0.558 | +0.104 [-0.616, +0.589] | 70.0 |
| 12h | SFP_harden | ALL | long | +0.168 | +0.196 [+0.003, +0.304] | 40.0 | +1.413 | +0.793 [-0.188, +1.865] | 65.0 | +0.259 | +0.304 [-0.237, +0.680] | 50.0 | +1.644 | -0.455 [-1.699, +0.754] | 75.0 |
| 12h | SFP_harden | ALL | short | -0.414 | -0.167 [-0.799, +0.037] | 40.0 | +0.661 | -0.205 [-1.019, +0.447] | 80.0 | -0.029 | -0.281 [-0.824, +0.255] | 60.0 | +0.253 | +0.744 [-0.699, +1.795] | 45.0 |
| 12h | SFP_harden | EXP_ALIGNED* | both | +0.158 | -0.003 [-0.314, +0.188] | 75.0 | +0.561 | +0.025 [-1.533, +0.900] | 60.0 | +0.144 | -0.197 [-1.101, +0.732] | 60.0 | -0.888 | -2.361 [-4.898, -0.218] | 70.0 |
| 12h | SFP_harden | EXP_ALIGNED* | long | +0.276 | +0.164 [-0.144, +0.639] | 55.0 | +2.062 | +1.064 [-1.232, +2.637] | 60.0 | +0.401 | +0.342 [-1.984, +2.644] | 50.0 | +2.451 | -1.103 [-4.589, +0.356] | 95.0 |
| 12h | SFP_harden | EXP_ALIGNED* | short | -0.774 | -0.250 [-0.812, +0.094] | 25.0 | -2.534 | -3.102 [-3.928, -0.526] | 55.0 | +0.045 | -0.855 [-1.699, +0.341] | 72.2 | -2.471 | -2.360 [-4.492, -0.758] | 44.4 |
| 12h | SFP_harden | EXP_COUNTER | both | +0.161 | +0.046 [-0.181, +0.247] | 60.0 | +1.171 | +1.369 [+0.585, +2.089] | 40.0 | +1.201 | +0.237 [-0.038, +0.765] | 95.0 | +1.167 | +2.989 [+1.952, +5.056] | 10.0 |
| 12h | SFP_harden | EXP_COUNTER | long | +0.585 | +0.206 [-0.203, +0.763] | 70.0 | +1.651 | +2.214 [+1.259, +5.662] | 35.0 | +0.976 | +0.651 [-0.064, +0.963] | 75.0 | +4.634 | +5.183 [+2.868, +8.671] | 45.0 |
| 12h | SFP_harden | EXP_COUNTER | short | -0.106 | -0.291 [-0.654, +0.462] | 55.0 | +0.765 | +0.040 [-1.539, +1.121] | 65.0 | +1.272 | +0.159 [-0.595, +1.284] | 72.2 | -0.921 | +1.783 [+1.364, +3.938] | 5.6 |
| 12h | SFP_harden | IN_RANGE_COINCIDENT* | both | -0.252 | -0.187 [-0.930, +2.776] | 50.0 | +0.206 | +1.964 [+0.299, +3.972] | 16.7 | -0.065 | +0.240 [-0.665, +3.503] | 37.5 | +0.953 | +4.322 [+1.639, +6.660] | 25.0 |
| 12h | SFP_harden | IN_RANGE_COINCIDENT* | long | -0.059 | +0.583 [-0.216, +2.186] | 28.6 | -0.907 | -1.754 [-3.376, +1.495] | 57.1 | +0.742 | +0.497 [-1.020, +3.461] | 60.0 | -0.535 | +0.615 [-2.175, +1.980] | 40.0 |
| 12h | SFP_harden | IN_RANGE_COINCIDENT* | short | -0.956 | -0.838 [-2.563, +1.499] | 50.0 | +2.006 | +2.740 [+1.568, +5.591] | 33.3 | -0.687 | +0.165 [-0.665, +1.646] | 25.0 | +6.476 | +8.322 [+7.103, +9.000] | 25.0 |
| 12h | SFP_harden | IN_RANGE_MID* | both | -1.321 | +0.058 [-0.813, +0.358] | 15.0 | -0.740 | -2.975 [-3.586, -0.529] | 75.0 | -1.452 | +0.169 [-0.956, +0.837] | 20.0 | -2.195 | -1.685 [-3.979, +1.780] | 45.0 |
| 12h | SFP_harden | IN_RANGE_MID* | long | -0.904 | -0.015 [-1.117, +0.823] | 30.0 | -2.195 | -2.983 [-4.303, +2.029] | 60.0 | -0.740 | -0.259 [-1.116, +1.131] | 35.0 | -2.827 | -2.871 [-4.962, +1.317] | 55.0 |
| 12h | SFP_harden | IN_RANGE_MID* | short | -1.381 | +0.219 [-1.314, +0.851] | 25.0 | +0.576 | -0.783 [-5.392, +4.684] | 60.0 | -1.555 | +0.332 [-0.777, +1.367] | 20.0 | -0.715 | +2.049 [-4.007, +5.426] | 45.0 |
| 12h | SFP_harden | IN_RANGE_OTHER | both | -0.060 | +0.043 [-0.739, +0.272] | 35.0 | +1.461 | -0.011 [-1.603, +0.958] | 80.0 | +0.029 | +0.101 [-1.363, +1.048] | 45.0 | +1.404 | +0.035 [-1.657, +0.816] | 85.0 |
| 12h | SFP_harden | IN_RANGE_OTHER | long | -0.320 | +0.033 [-0.538, +0.515] | 35.0 | +1.890 | -1.330 [-2.509, +0.412] | 80.0 | -0.155 | +0.141 [-0.893, +1.045] | 45.0 | +1.675 | -1.834 [-3.609, -0.222] | 90.0 |
| 12h | SFP_harden | IN_RANGE_OTHER | short | -0.021 | -0.388 [-1.305, +0.169] | 55.0 | +1.328 | +0.893 [-4.547, +2.633] | 55.0 | +0.224 | +0.219 [-1.193, +1.387] | 52.6 | +1.328 | +1.601 [-1.811, +3.188] | 42.1 |
| 12h | SFP_harden | NONE | both | — | -2.573 [-5.248, +0.103] | — | — | -4.724 [-5.012, -4.436] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | SFP_harden | NONE | long | — | -7.924 [-7.924, -7.924] | — | — | -5.300 [-5.300, -5.300] | — | — | — [—, —] | — | — | — [—, —] | — |
| 12h | SFP_harden | NONE | short | — | +2.778 [+2.778, +2.778] | — | — | -4.148 [-4.148, -4.148] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_first | ALL | both | -0.063 | -0.065 [-0.172, +0.237] | 50.0 | -0.738 | -0.276 [-1.252, +0.849] | 50.0 | -0.248 | -0.448 [-0.761, +0.310] | 55.0 | -1.455 | -1.958 [-3.843, -1.497] | 80.0 |
| 1d | BRK_tap89_first | ALL | long | +0.088 | +0.091 [-0.138, +0.242] | 45.0 | -0.745 | -0.300 [-1.018, +1.344] | 40.0 | -0.697 | -0.962 [-1.221, +0.225] | 60.0 | -1.470 | -2.446 [-3.381, -1.694] | 80.0 |
| 1d | BRK_tap89_first | ALL | short | -0.154 | -0.130 [-0.451, +0.451] | 45.0 | +1.496 | -0.414 [-1.971, +1.855] | 70.0 | -0.148 | +0.601 [-0.051, +1.381] | 20.0 | -1.232 | -1.906 [-3.570, -0.296] | 60.0 |
| 1d | BRK_tap89_first | EXP_ALIGNED* | both | -0.870 | +0.726 [-0.141, +0.807] | 5.0 | -1.709 | -0.672 [-2.324, +0.521] | 40.0 | -1.424 | +0.884 [-0.816, +1.238] | 20.0 | -1.962 | -1.956 [-4.677, -1.463] | 42.5 |
| 1d | BRK_tap89_first | EXP_ALIGNED* | long | -0.933 | +0.842 [-0.056, +0.900] | 10.0 | -1.955 | -3.044 [-4.081, -2.312] | 75.0 | -0.941 | -0.225 [-1.103, +0.997] | 26.3 | -1.962 | -4.267 [-4.797, -1.944] | 63.2 |
| 1d | BRK_tap89_first | EXP_ALIGNED* | short | -0.806 | +0.463 [-0.268, +0.719] | 20.0 | +0.319 | +0.879 [-1.410, +2.915] | 45.0 | -2.749 | +1.119 [-0.632, +1.969] | 2.5 | -2.763 | -1.629 [-5.956, +2.590] | 37.5 |
| 1d | BRK_tap89_first | EXP_COUNTER | both | +0.224 | +0.086 [-0.230, +0.399] | 55.0 | +0.736 | -0.045 [-1.032, +1.967] | 60.0 | -0.232 | -0.784 [-1.140, +0.214] | 65.0 | +1.386 | +1.313 [-3.250, +3.211] | 50.0 |
| 1d | BRK_tap89_first | EXP_COUNTER | long | +0.225 | +0.140 [-0.235, +0.311] | 60.0 | +0.447 | +0.198 [-1.258, +1.919] | 50.0 | -0.677 | -1.054 [-1.366, -0.677] | 75.0 | -1.440 | -2.432 [-5.697, +2.997] | 60.0 |
| 1d | BRK_tap89_first | EXP_COUNTER | short | +0.625 | +0.637 [-1.783, +2.355] | 42.1 | +4.226 | +2.164 [-2.658, +4.226] | 73.7 | +0.625 | +2.193 [+1.415, +2.526] | 23.5 | +4.226 | +4.226 [+1.842, +4.921] | 58.8 |
| 1d | BRK_tap89_first | IN_RANGE_COINCIDENT* | both | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap89_first | IN_RANGE_COINCIDENT* | long | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap89_first | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_first | IN_RANGE_MID* | both | -0.115 | -0.278 [-1.310, +0.132] | 50.0 | -1.177 | -2.218 [-5.363, -1.117] | 70.0 | +0.196 | -0.246 [-1.784, +0.431] | 70.0 | -1.173 | -1.893 [-3.390, +1.587] | 60.0 |
| 1d | BRK_tap89_first | IN_RANGE_MID* | long | -0.424 | -0.667 [-1.701, +0.526] | 57.9 | -1.186 | -0.726 [-1.624, +6.004] | 47.4 | +0.433 | +0.444 [-1.894, +3.565] | 41.2 | +4.066 | +4.943 [+0.323, +7.421] | 41.2 |
| 1d | BRK_tap89_first | IN_RANGE_MID* | short | -0.049 | -0.039 [-0.385, +0.297] | 42.1 | -1.176 | -6.564 [-11.904, -1.912] | 78.9 | -0.042 | -0.039 [-0.556, +0.486] | 38.9 | -1.840 | -9.632 [-14.176, -2.658] | 77.8 |
| 1d | BRK_tap89_first | IN_RANGE_OTHER | both | -0.479 | -0.713 [-1.253, -0.253] | 60.0 | -1.279 | -0.207 [-6.243, +2.579] | 40.0 | -0.125 | -0.358 [-1.023, +0.007] | 55.0 | -1.365 | -2.749 [-7.455, +0.499] | 52.9 |
| 1d | BRK_tap89_first | IN_RANGE_OTHER | long | -0.941 | -1.093 [-1.956, -0.346] | 52.9 | -3.590 | -0.445 [-3.818, +0.475] | 28.1 | -0.941 | -0.832 [-1.698, +0.254] | 43.8 | -3.590 | -1.348 [-3.590, +6.802] | 23.1 |
| 1d | BRK_tap89_first | IN_RANGE_OTHER | short | -0.479 | -0.257 [-0.713, +0.007] | 42.1 | +3.856 | -4.414 [-9.319, +3.861] | 64.7 | -0.125 | -0.123 [-0.476, +0.007] | 47.1 | -1.279 | -9.319 [-9.328, +3.861] | 64.3 |
| 1d | BRK_tap89_first | NONE | both | +0.212 | +0.094 [-0.526, +0.167] | 85.0 | +8.143 | +2.419 [+1.779, +2.938] | 90.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_first | NONE | long | +0.212 | +0.268 [+0.103, +0.320] | 35.0 | +8.143 | +4.962 [+2.202, +5.540] | 85.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_first | NONE | short | — | -2.066 [-2.263, -0.901] | — | — | -4.091 [-11.618, -3.358] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_oneshot | ALL | both | -0.056 | -0.019 [-0.215, +0.237] | 50.0 | -0.771 | -0.753 [-2.033, +0.882] | 45.0 | -0.052 | -0.115 [-0.727, +0.466] | 50.0 | -1.455 | -1.878 [-3.659, +0.509] | 65.0 |
| 1d | BRK_tap89_oneshot | ALL | long | +0.088 | +0.181 [+0.004, +0.301] | 40.0 | -0.770 | -0.209 [-1.331, +1.276] | 50.0 | -0.309 | -0.628 [-1.143, +0.456] | 60.0 | -1.555 | -2.083 [-2.641, -1.613] | 75.0 |
| 1d | BRK_tap89_oneshot | ALL | short | -0.154 | -0.273 [-0.711, +0.024] | 55.0 | -0.432 | +0.049 [-2.552, +2.147] | 45.0 | -0.050 | -0.037 [-0.375, +0.722] | 45.0 | -1.184 | -1.140 [-4.850, +2.196] | 45.0 |
| 1d | BRK_tap89_oneshot | EXP_ALIGNED* | both | -1.139 | +0.603 [-0.249, +0.789] | 5.0 | -2.028 | -1.863 [-2.971, -1.260] | 40.0 | -1.424 | +0.868 [-1.056, +0.981] | 20.0 | -1.962 | -2.644 [-5.203, -1.712] | 55.0 |
| 1d | BRK_tap89_oneshot | EXP_ALIGNED* | long | -0.933 | +0.842 [+0.140, +0.900] | 5.0 | -1.955 | -2.684 [-4.081, -1.948] | 65.0 | -0.941 | +0.027 [-0.933, +0.997] | 21.1 | -1.962 | -3.907 [-4.523, -1.821] | 57.9 |
| 1d | BRK_tap89_oneshot | EXP_ALIGNED* | short | -1.343 | -0.204 [-0.934, +0.629] | 10.0 | -2.099 | +0.107 [-2.078, +1.932] | 25.0 | -2.749 | +0.958 [-2.540, +1.969] | 5.0 | -2.763 | -3.538 [-5.956, +2.819] | 55.0 |
| 1d | BRK_tap89_oneshot | EXP_COUNTER | both | +0.224 | +0.260 [-0.298, +0.328] | 45.0 | +0.445 | +0.158 [-1.582, +1.976] | 52.5 | -0.232 | -0.742 [-1.277, +0.416] | 65.0 | +1.386 | +2.217 [-2.663, +3.045] | 40.0 |
| 1d | BRK_tap89_oneshot | EXP_COUNTER | long | +0.076 | +0.158 [-0.245, +0.312] | 45.0 | -0.145 | +0.594 [-2.316, +1.960] | 45.0 | -0.677 | -1.022 [-1.332, -0.617] | 68.4 | -1.440 | -3.402 [-5.320, +3.013] | 57.9 |
| 1d | BRK_tap89_oneshot | EXP_COUNTER | short | +0.625 | +0.637 [-1.696, +2.201] | 47.1 | +4.226 | +2.164 [-2.133, +4.226] | 70.6 | +0.625 | +1.886 [-0.151, +2.589] | 25.0 | +4.226 | +4.226 [+1.842, +5.824] | 56.2 |
| 1d | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | both | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | long | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap89_oneshot | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_oneshot | IN_RANGE_MID* | both | -0.059 | -0.049 [-0.828, +0.150] | 45.0 | -0.959 | -1.062 [-3.341, +5.708] | 50.0 | +0.432 | -0.026 [-1.262, +0.777] | 70.0 | +1.446 | -0.414 [-1.846, +7.352] | 60.0 |
| 1d | BRK_tap89_oneshot | IN_RANGE_MID* | long | -0.424 | -0.667 [-1.827, +0.922] | 52.6 | -1.186 | +0.331 [-1.622, +6.004] | 42.1 | +0.433 | +0.444 [-2.147, +3.565] | 41.2 | +4.066 | +4.943 [+0.323, +7.421] | 41.2 |
| 1d | BRK_tap89_oneshot | IN_RANGE_MID* | short | -0.042 | -0.037 [-0.075, +0.397] | 37.5 | +2.111 | -2.065 [-9.264, +0.473] | 75.0 | +0.810 | +0.014 [-0.109, +0.954] | 71.4 | -1.176 | -6.180 [-13.127, -1.172] | 64.3 |
| 1d | BRK_tap89_oneshot | IN_RANGE_OTHER | both | -0.125 | -0.476 [-1.088, -0.182] | 73.7 | -1.279 | -1.413 [-7.051, +1.973] | 50.0 | -0.007 | -0.124 [-0.593, +0.141] | 63.2 | -3.560 | -5.839 [-9.319, +2.180] | 60.0 |
| 1d | BRK_tap89_oneshot | IN_RANGE_OTHER | long | +0.085 | -0.544 [-1.475, +0.103] | 75.0 | -5.833 | -0.687 [-4.275, +2.939] | 10.7 | +0.085 | +0.273 [-1.178, +0.539] | 46.7 | -5.833 | -3.590 [-5.575, +6.808] | 11.1 |
| 1d | BRK_tap89_oneshot | IN_RANGE_OTHER | short | -0.244 | -0.248 [-0.712, +0.007] | 50.0 | +1.289 | -9.319 [-9.319, +3.438] | 60.0 | -0.125 | -0.123 [-0.476, +0.007] | 47.1 | -1.279 | -9.319 [-9.328, +3.861] | 64.3 |
| 1d | BRK_tap89_oneshot | NONE | both | +0.321 | +0.096 [-0.428, +0.221] | 80.0 | +4.963 | +1.776 [+0.659, +2.379] | 90.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_oneshot | NONE | long | +0.321 | +0.284 [+0.108, +0.420] | 65.0 | +4.963 | +2.337 [+1.786, +4.992] | 65.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap89_oneshot | NONE | short | — | -2.100 [-2.637, -0.901] | — | — | -4.091 [-11.401, -3.358] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_first | ALL | both | -0.069 | +0.127 [-0.010, +0.376] | 20.0 | -0.043 | +0.588 [-0.126, +0.846] | 35.0 | -0.560 | -0.260 [-0.896, +0.055] | 45.0 | -2.075 | -2.377 [-3.235, -0.013] | 60.0 |
| 1d | BRK_tap127_first | ALL | long | -0.012 | +0.012 [-0.243, +0.424] | 40.0 | -0.119 | +0.628 [-0.046, +0.981] | 20.0 | -0.697 | -0.990 [-1.395, -0.085] | 65.0 | -1.597 | -2.423 [-3.300, -0.252] | 60.0 |
| 1d | BRK_tap127_first | ALL | short | -0.068 | +0.265 [-0.025, +0.840] | 25.0 | +1.387 | +0.220 [-0.476, +1.760] | 70.0 | -0.326 | +0.323 [-0.173, +1.203] | 25.0 | -2.849 | -1.746 [-4.863, +1.546] | 40.0 |
| 1d | BRK_tap127_first | EXP_ALIGNED* | both | -1.280 | +0.018 [-0.664, +0.465] | 15.0 | +0.594 | +0.630 [+0.546, +0.731] | 40.0 | -3.207 | -0.547 [-1.373, +0.640] | 5.0 | -2.231 | -3.611 [-5.379, +0.841] | 55.0 |
| 1d | BRK_tap127_first | EXP_ALIGNED* | long | -2.040 | -2.223 [-2.543, -1.237] | 50.0 | -2.087 | +0.588 [-3.000, +0.648] | 30.0 | -2.371 | -0.773 [-3.114, -0.441] | 36.8 | -2.096 | -2.413 [-5.079, -0.472] | 68.4 |
| 1d | BRK_tap127_first | EXP_ALIGNED* | short | +0.299 | +0.668 [+0.289, +1.306] | 25.0 | +2.446 | +2.434 [+0.272, +2.616] | 65.0 | -4.977 | -0.048 [-2.099, +2.802] | 7.5 | -3.598 | -1.788 [-7.516, +3.035] | 42.5 |
| 1d | BRK_tap127_first | EXP_COUNTER | both | +0.158 | +0.207 [-0.310, +0.860] | 50.0 | -0.044 | +0.137 [-0.385, +1.216] | 35.0 | -0.405 | -0.794 [-1.338, +0.087] | 65.0 | +1.493 | +2.041 [-1.992, +3.045] | 45.0 |
| 1d | BRK_tap127_first | EXP_COUNTER | long | -0.117 | +0.423 [-0.314, +0.619] | 40.0 | -0.123 | +0.058 [-1.844, +1.064] | 45.0 | -0.677 | -0.927 [-1.768, -0.677] | 75.0 | -1.535 | -3.462 [-5.228, +1.883] | 60.0 |
| 1d | BRK_tap127_first | EXP_COUNTER | short | +0.625 | +0.919 [-0.288, +2.455] | 36.8 | +4.535 | +2.190 [-2.871, +4.533] | 76.3 | +0.625 | +2.134 [+0.748, +5.641] | 26.7 | +4.535 | +4.535 [+3.197, +5.806] | 56.7 |
| 1d | BRK_tap127_first | IN_RANGE_COINCIDENT* | both | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap127_first | IN_RANGE_COINCIDENT* | long | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap127_first | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_first | IN_RANGE_MID* | both | -0.133 | -0.246 [-1.139, +0.362] | 55.0 | -3.217 | -3.544 [-6.420, -1.622] | 50.0 | -0.040 | -0.199 [-1.182, +0.343] | 55.0 | -3.207 | -3.544 [-8.628, -2.216] | 55.0 |
| 1d | BRK_tap127_first | IN_RANGE_MID* | long | -0.424 | -0.244 [-1.322, +0.455] | 45.0 | -2.421 | -1.174 [-3.200, +2.617] | 30.0 | +0.437 | +0.433 [-1.203, +3.159] | 55.9 | -1.615 | +2.103 [-1.619, +6.302] | 35.3 |
| 1d | BRK_tap127_first | IN_RANGE_MID* | short | -0.067 | -0.040 [-3.435, +0.115] | 41.7 | -10.161 | -12.127 [-14.176, -8.824] | 55.6 | -0.067 | -0.039 [-3.472, +0.107] | 44.1 | -10.161 | -12.174 [-14.176, -10.161] | 73.5 |
| 1d | BRK_tap127_first | IN_RANGE_OTHER | both | -0.041 | +0.865 [+0.364, +0.959] | 10.5 | +3.678 | -1.186 [-1.432, +1.122] | 94.1 | -0.041 | +0.287 [-0.041, +0.481] | 26.5 | +3.678 | +3.678 [+3.669, +3.678] | 55.6 |
| 1d | BRK_tap127_first | IN_RANGE_OTHER | long | +0.959 | +1.160 [+0.959, +1.448] | 28.1 | -1.432 | -1.432 [-1.432, -1.411] | 37.5 | +0.481 | +0.481 [+0.481, +0.925] | 31.8 | — | +14.972 [+10.892, +15.019] | — |
| 1d | BRK_tap127_first | IN_RANGE_OTHER | short | -1.247 | -0.550 [-0.845, +0.287] | 25.0 | +5.134 | +3.678 [+3.069, +3.678] | 87.5 | -0.550 | -0.550 [-0.550, +0.287] | 36.4 | +3.678 | +3.678 [+2.459, +3.678] | 64.3 |
| 1d | BRK_tap127_first | NONE | both | +0.214 | +0.345 [+0.186, +0.418] | 30.0 | +1.785 | +1.316 [+0.815, +1.785] | 75.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_first | NONE | long | +0.214 | +0.270 [+0.199, +0.405] | 30.0 | +1.785 | +2.306 [+1.322, +3.393] | 45.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_first | NONE | short | — | +0.198 [-0.933, +5.557] | — | — | -1.678 [-2.943, -0.402] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_oneshot | ALL | both | -0.078 | +0.008 [-0.131, +0.324] | 30.0 | +0.042 | +0.364 [-0.259, +0.665] | 35.0 | -0.561 | -0.301 [-1.029, -0.069] | 42.5 | -0.620 | -2.027 [-3.485, +0.720] | 65.0 |
| 1d | BRK_tap127_oneshot | ALL | long | -0.012 | +0.015 [-0.243, +0.255] | 40.0 | -0.119 | +0.550 [-0.015, +0.806] | 20.0 | -0.410 | -1.083 [-1.841, -0.085] | 65.0 | -1.555 | -2.420 [-3.655, -1.418] | 60.0 |
| 1d | BRK_tap127_oneshot | ALL | short | -0.297 | -0.027 [-0.224, +0.904] | 15.0 | +2.596 | +0.691 [-1.135, +1.890] | 95.0 | -0.558 | +0.245 [-0.617, +1.481] | 25.0 | +0.315 | -0.946 [-2.595, +3.181] | 65.0 |
| 1d | BRK_tap127_oneshot | EXP_ALIGNED* | both | -2.033 | -0.245 [-1.281, +0.354] | 20.0 | +0.459 | +0.584 [+0.141, +0.633] | 30.0 | -3.207 | -1.298 [-2.645, -0.252] | 25.0 | -2.231 | -4.934 [-5.627, +0.587] | 70.0 |
| 1d | BRK_tap127_oneshot | EXP_ALIGNED* | long | -2.040 | -2.535 [-2.546, -1.371] | 60.0 | -2.087 | +0.588 [-3.000, +0.645] | 30.0 | -2.371 | -1.033 [-3.268, -0.441] | 38.9 | -2.096 | -3.889 [-5.329, -2.181] | 77.8 |
| 1d | BRK_tap127_oneshot | EXP_ALIGNED* | short | -1.327 | +0.724 [-0.245, +1.266] | 15.0 | +1.385 | +1.433 [+0.014, +2.623] | 45.0 | -4.977 | -1.522 [-3.684, +1.470] | 21.1 | -3.598 | -3.598 [-7.516, +0.263] | 52.6 |
| 1d | BRK_tap127_oneshot | EXP_COUNTER | both | +0.158 | -0.114 [-0.353, +0.693] | 60.0 | -0.044 | +0.137 [-0.758, +0.820] | 40.0 | -0.405 | -0.784 [-1.596, +0.087] | 65.0 | +1.493 | -0.877 [-3.510, +2.484] | 60.0 |
| 1d | BRK_tap127_oneshot | EXP_COUNTER | long | -0.117 | +0.363 [-0.538, +0.616] | 45.0 | -0.123 | +0.010 [-2.222, +0.865] | 45.0 | -0.677 | -1.197 [-1.769, -0.784] | 81.6 | -1.535 | -3.467 [-5.239, +1.750] | 63.2 |
| 1d | BRK_tap127_oneshot | EXP_COUNTER | short | +0.625 | +0.674 [-0.931, +5.211] | 47.1 | +4.535 | +1.704 [-3.194, +4.535] | 73.5 | +0.625 | +4.844 [+0.008, +6.162] | 30.8 | +4.535 | +4.535 [+2.291, +6.692] | 50.0 |
| 1d | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | both | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | long | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap127_oneshot | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_oneshot | IN_RANGE_MID* | both | -0.110 | -0.102 [-0.881, +0.108] | 50.0 | -2.068 | -1.622 [-5.042, +1.291] | 45.0 | +0.433 | -0.026 [-1.085, +0.344] | 77.5 | -1.619 | -1.375 [-3.062, +1.942] | 42.5 |
| 1d | BRK_tap127_oneshot | IN_RANGE_MID* | long | -0.174 | -0.497 [-1.279, +0.399] | 55.0 | -1.629 | -1.174 [-2.273, +2.220] | 30.0 | +0.472 | +0.433 [-1.179, +1.209] | 64.7 | +2.341 | +1.886 [-1.622, +6.302] | 58.8 |
| 1d | BRK_tap127_oneshot | IN_RANGE_MID* | short | -0.033 | -0.040 [-0.080, +0.080] | 54.5 | -2.495 | -9.632 [-10.170, -7.445] | 90.9 | -0.033 | -0.015 [-0.080, +0.118] | 45.5 | -2.495 | -9.980 [-11.172, -7.738] | 90.9 |
| 1d | BRK_tap127_oneshot | IN_RANGE_OTHER | both | -0.041 | +0.959 [+0.448, +0.959] | 17.6 | +3.678 | -1.348 [-1.432, +1.122] | 100.0 | -0.041 | -0.041 [-0.550, +0.481] | 42.3 | +3.678 | +3.678 [+2.456, +3.678] | 62.5 |
| 1d | BRK_tap127_oneshot | IN_RANGE_OTHER | long | +0.959 | +0.959 [+0.959, +1.448] | 31.2 | -1.432 | -1.432 [-1.432, -1.432] | 40.6 | +0.481 | +0.481 [+0.481, +0.481] | 45.5 | — | +14.972 [+6.812, +14.972] | — |
| 1d | BRK_tap127_oneshot | IN_RANGE_OTHER | short | -1.247 | -0.550 [-1.781, -0.550] | 37.5 | +5.134 | +3.678 [+3.069, +3.678] | 87.5 | -0.550 | -0.550 [-1.139, -0.550] | 64.3 | +3.678 | +3.678 [+2.459, +3.678] | 64.3 |
| 1d | BRK_tap127_oneshot | NONE | both | +0.159 | +0.254 [+0.186, +0.401] | 25.0 | +5.225 | +1.316 [+0.816, +2.600] | 95.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_oneshot | NONE | long | +0.159 | +0.265 [+0.146, +0.330] | 27.5 | +5.225 | +2.861 [+1.322, +3.850] | 80.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap127_oneshot | NONE | short | — | +0.198 [-0.933, +5.557] | — | — | -1.678 [-2.943, -0.402] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_first | ALL | both | -0.238 | -0.341 [-0.612, -0.109] | 65.0 | -1.631 | +0.436 [-0.059, +1.526] | 10.0 | -0.625 | -0.822 [-1.039, -0.090] | 60.0 | -4.462 | -0.316 [-3.576, +0.588] | 5.0 |
| 1d | BRK_tap200_first | ALL | long | -0.345 | -0.382 [-0.834, -0.364] | 75.0 | -0.071 | +1.612 [+0.364, +1.802] | 5.0 | -1.113 | -1.064 [-1.123, -0.904] | 30.0 | -4.413 | -0.316 [-3.151, +2.525] | 15.0 |
| 1d | BRK_tap200_first | ALL | short | -0.078 | -0.095 [-0.288, +0.433] | 60.0 | -4.259 | -1.072 [-2.121, +1.112] | 10.0 | +0.088 | +0.457 [-0.177, +1.053] | 35.0 | -7.160 | -2.460 [-7.216, +0.052] | 25.0 |
| 1d | BRK_tap200_first | EXP_ALIGNED* | both | -0.942 | -0.278 [-0.762, +0.035] | 7.5 | -2.057 | +1.405 [-0.294, +3.120] | 15.0 | -1.033 | -0.595 [-0.966, +0.257] | 20.0 | -5.430 | +0.916 [-1.117, +2.680] | 7.5 |
| 1d | BRK_tap200_first | EXP_ALIGNED* | long | -0.937 | -0.681 [-0.942, +0.391] | 42.5 | -2.672 | +7.260 [+1.624, +8.020] | 15.0 | -1.117 | -1.033 [-1.160, -0.937] | 28.9 | -4.764 | +0.958 [+0.135, +3.918] | 7.9 |
| 1d | BRK_tap200_first | EXP_ALIGNED* | short | -0.682 | -0.139 [-0.467, +0.106] | 15.0 | -1.132 | +0.757 [-2.243, +3.007] | 30.0 | +0.651 | +0.852 [+0.017, +1.548] | 50.0 | -8.813 | -0.809 [-3.139, +2.606] | 5.0 |
| 1d | BRK_tap200_first | EXP_COUNTER | both | -0.178 | -0.910 [-1.591, +0.093] | 60.0 | -0.167 | +0.213 [-0.766, +1.600] | 35.0 | -0.119 | -1.116 [-1.906, +0.257] | 60.0 | -4.799 | -1.078 [-4.414, +1.525] | 10.0 |
| 1d | BRK_tap200_first | EXP_COUNTER | long | -1.548 | -1.607 [-1.908, -0.799] | 55.0 | -0.072 | -0.064 [-1.059, +1.182] | 50.0 | -2.173 | -1.913 [-2.433, -1.348] | 40.0 | -4.600 | -4.354 [-4.649, +0.054] | 30.0 |
| 1d | BRK_tap200_first | EXP_COUNTER | short | +2.299 | +1.619 [+0.896, +1.711] | 83.3 | -6.005 | +2.499 [-1.057, +6.007] | 5.6 | +2.299 | +1.745 [+0.896, +2.606] | 62.5 | -6.005 | +5.543 [+0.004, +6.452] | 18.8 |
| 1d | BRK_tap200_first | IN_RANGE_COINCIDENT* | both | — | -3.180 [-3.180, -2.132] | — | — | -2.259 [-2.259, +4.630] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap200_first | IN_RANGE_COINCIDENT* | long | — | -3.180 [-3.180, -2.132] | — | — | -2.259 [-2.259, +4.630] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap200_first | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_first | IN_RANGE_MID* | both | -0.093 | -0.380 [-1.096, -0.007] | 65.0 | -4.403 | -0.957 [-4.770, +3.578] | 30.0 | -0.093 | -0.580 [-1.100, -0.062] | 70.0 | -4.403 | -2.500 [-4.884, +4.201] | 30.0 |
| 1d | BRK_tap200_first | IN_RANGE_MID* | long | -0.165 | -0.380 [-0.869, +0.039] | 65.0 | -1.620 | +3.804 [-1.622, +6.636] | 30.0 | -1.093 | -0.380 [-0.945, +0.209] | 26.3 | -1.620 | +4.798 [+1.508, +9.241] | 11.8 |
| 1d | BRK_tap200_first | IN_RANGE_MID* | short | -0.067 | -0.429 [-3.744, +0.455] | 64.7 | -10.161 | -9.992 [-12.457, -5.869] | 41.2 | -0.067 | -2.035 [-3.757, -0.093] | 80.0 | -10.161 | -10.170 [-13.601, -9.730] | 53.3 |
| 1d | BRK_tap200_first | IN_RANGE_OTHER | both | -3.188 | -1.350 [-5.012, +0.090] | 36.8 | -2.267 | -2.259 [-2.340, -1.127] | 35.3 | -5.129 | -0.297 [-9.962, +0.481] | 38.9 | -2.292 | -2.292 [-2.412, -2.171] | 50.0 |
| 1d | BRK_tap200_first | IN_RANGE_OTHER | long | -1.741 | -0.348 [-1.546, +0.286] | 23.3 | -2.218 | -2.218 [-2.259, -2.171] | 50.0 | -0.297 | +0.481 [-0.102, +0.670] | 13.6 | -2.171 | -2.171 [-2.171, +7.871] | 28.6 |
| 1d | BRK_tap200_first | IN_RANGE_OTHER | short | -9.962 | -9.962 [-9.962, -8.334] | 37.5 | -2.412 | -2.412 [-2.412, -1.749] | 37.5 | -9.962 | -9.962 [-9.962, -9.962] | 50.0 | -2.412 | -2.412 [-2.412, -2.412] | 50.0 |
| 1d | BRK_tap200_first | NONE | both | -0.241 | -0.119 [-0.257, -0.054] | 25.0 | +2.017 | +1.220 [+0.940, +1.788] | 85.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_first | NONE | long | -0.241 | -0.119 [-0.260, +0.109] | 25.0 | +2.017 | +1.789 [+1.030, +1.790] | 80.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_first | NONE | short | — | -0.265 [-0.265, +0.014] | — | — | -1.493 [-1.493, +0.429] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_oneshot | ALL | both | -0.309 | -0.365 [-0.678, -0.192] | 55.0 | -0.183 | +0.506 [-0.478, +1.179] | 30.0 | -0.954 | -0.833 [-1.020, -0.115] | 30.0 | -2.426 | +1.370 [-3.658, +2.480] | 30.0 |
| 1d | BRK_tap200_oneshot | ALL | long | -0.308 | -0.610 [-0.858, -0.354] | 80.0 | -0.068 | +1.197 [+0.347, +1.785] | 15.0 | -1.105 | -1.101 [-1.126, -0.808] | 47.5 | -2.183 | +0.293 [-2.803, +1.667] | 30.0 |
| 1d | BRK_tap200_oneshot | ALL | short | -0.683 | -0.210 [-0.383, -0.026] | 10.0 | -2.251 | -1.507 [-3.346, +1.003] | 30.0 | +1.114 | +0.452 [-0.261, +1.548] | 68.4 | -2.478 | +0.048 [-2.418, +3.127] | 21.1 |
| 1d | BRK_tap200_oneshot | EXP_ALIGNED* | both | -1.165 | -0.935 [-1.092, -0.687] | 17.5 | -2.373 | -0.729 [-3.489, +0.813] | 35.0 | -1.117 | -1.051 [-1.213, -0.929] | 37.5 | -4.764 | +2.598 [-1.528, +4.168] | 12.5 |
| 1d | BRK_tap200_oneshot | EXP_ALIGNED* | long | -1.026 | -0.948 [-1.051, -0.853] | 45.0 | -3.717 | +0.958 [-2.672, +5.162] | 10.0 | -1.117 | -1.033 [-1.160, -0.937] | 28.9 | -4.764 | +0.958 [+0.135, +3.918] | 7.9 |
| 1d | BRK_tap200_oneshot | EXP_ALIGNED* | short | -2.014 | -0.465 [-1.100, -0.111] | 5.0 | -1.132 | -1.539 [-6.510, +1.558] | 55.0 | — | +0.692 [-1.496, +1.522] | — | — | +2.604 [-5.862, +4.090] | — |
| 1d | BRK_tap200_oneshot | EXP_COUNTER | both | -0.011 | -0.537 [-1.300, +0.497] | 55.0 | +1.206 | +1.207 [+0.656, +2.228] | 50.0 | +1.081 | +0.237 [-1.251, +0.865] | 80.0 | +0.309 | +1.169 [-2.148, +5.400] | 45.0 |
| 1d | BRK_tap200_oneshot | EXP_COUNTER | long | -0.178 | -1.406 [-1.725, +0.074] | 70.0 | +1.207 | +1.071 [-0.080, +2.046] | 60.0 | -1.430 | -1.390 [-1.907, -0.861] | 47.5 | +1.955 | -0.093 [-4.783, +1.597] | 77.5 |
| 1d | BRK_tap200_oneshot | EXP_COUNTER | short | +2.876 | +1.711 [+1.489, +1.780] | 82.4 | +0.309 | +5.546 [+2.302, +6.012] | 23.5 | +2.876 | +1.745 [+1.711, +2.606] | 75.0 | +0.309 | +6.012 [+5.544, +6.452] | 18.8 |
| 1d | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | both | — | -3.180 [-3.180, -2.132] | — | — | -2.259 [-2.259, +4.630] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | long | — | -3.180 [-3.180, -2.132] | — | — | -2.259 [-2.259, +4.630] | — | — | -1.083 [-1.083, -1.083] | — | — | +11.519 [+11.519, +11.519] | — |
| 1d | BRK_tap200_oneshot | IN_RANGE_COINCIDENT* | short | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_oneshot | IN_RANGE_MID* | both | -0.102 | -0.476 [-1.024, +0.223] | 60.0 | -2.060 | -1.836 [-4.258, +2.001] | 50.0 | -0.565 | -0.569 [-1.112, -0.013] | 50.0 | -2.060 | -2.498 [-4.401, +2.001] | 60.0 |
| 1d | BRK_tap200_oneshot | IN_RANGE_MID* | long | -0.165 | -0.474 [-1.103, +0.384] | 65.0 | -1.620 | +0.398 [-1.622, +3.536] | 30.0 | -1.093 | -0.369 [-1.121, +0.870] | 42.1 | -1.620 | +1.886 [-1.621, +4.798] | 29.4 |
| 1d | BRK_tap200_oneshot | IN_RANGE_MID* | short | -0.033 | -0.093 [-1.080, -0.050] | 81.8 | -2.495 | -6.952 [-10.170, -4.415] | 81.8 | -0.033 | -0.093 [-1.409, -0.073] | 90.0 | -2.495 | -8.209 [-10.170, -6.425] | 90.0 |
| 1d | BRK_tap200_oneshot | IN_RANGE_OTHER | both | -3.188 | -2.879 [-3.254, -0.287] | 31.2 | -2.267 | -2.259 [-2.320, -0.100] | 28.6 | -5.129 | +0.481 [-9.962, +0.481] | 38.5 | -2.292 | -2.412 [-2.412, +3.372] | 62.5 |
| 1d | BRK_tap200_oneshot | IN_RANGE_OTHER | long | -1.741 | -1.350 [-3.180, +0.481] | 38.5 | -2.218 | -2.259 [-2.259, -1.410] | 70.0 | -0.297 | +0.481 [+0.481, +0.889] | 12.5 | -2.171 | +16.869 [+7.871, +16.869] | 0.0 |
| 1d | BRK_tap200_oneshot | IN_RANGE_OTHER | short | -9.962 | -9.962 [-9.962, -5.077] | 33.3 | -2.412 | -2.412 [-2.412, -0.421] | 33.3 | -9.962 | -9.962 [-9.962, -9.962] | 50.0 | -2.412 | -2.412 [-2.412, -2.412] | 50.0 |
| 1d | BRK_tap200_oneshot | NONE | both | -0.241 | -0.119 [-0.257, -0.054] | 25.0 | +2.017 | +1.220 [+0.940, +1.788] | 85.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_oneshot | NONE | long | -0.241 | -0.119 [-0.260, +0.109] | 25.0 | +2.017 | +1.789 [+1.030, +1.790] | 80.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_tap200_oneshot | NONE | short | — | -0.265 [-0.265, +0.014] | — | — | -1.493 [-1.493, +0.429] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | ALL | both | +0.352 | +0.209 [-0.151, +0.362] | 75.0 | -1.357 | +0.718 [-1.243, +1.591] | 25.0 | +0.396 | +0.060 [-0.199, +0.766] | 70.0 | -3.437 | -1.594 [-3.347, +0.294] | 25.0 |
| 1d | BRK_mem_first | ALL | long | +0.922 | +0.487 [+0.015, +0.592] | 90.0 | -0.143 | +0.835 [-0.040, +1.745] | 25.0 | +0.044 | +0.066 [-0.369, +0.653] | 50.0 | -2.190 | -1.541 [-2.832, -1.009] | 30.0 |
| 1d | BRK_mem_first | ALL | short | +0.345 | -0.080 [-0.268, +0.206] | 80.0 | -3.337 | -0.776 [-2.353, +0.638] | 20.0 | +0.683 | -0.089 [-0.945, +0.887] | 70.0 | -4.315 | -1.529 [-7.151, +1.013] | 40.0 |
| 1d | BRK_mem_first | EXP_ALIGNED* | both | +0.262 | +0.172 [-1.270, +0.788] | 55.0 | -3.339 | -0.767 [-2.592, +1.751] | 10.0 | +0.565 | -0.332 [-0.942, +0.593] | 75.0 | -5.878 | -1.012 [-2.122, +1.730] | 15.0 |
| 1d | BRK_mem_first | EXP_ALIGNED* | long | +1.168 | +0.565 [+0.010, +1.467] | 64.7 | -5.018 | -0.986 [-2.874, +3.146] | 5.9 | +0.420 | +0.520 [-0.317, +1.190] | 46.7 | -6.167 | -2.832 [-4.574, +0.670] | 6.7 |
| 1d | BRK_mem_first | EXP_ALIGNED* | short | +0.205 | -0.139 [-1.432, +0.799] | 60.0 | -3.248 | -0.642 [-3.714, +1.986] | 30.0 | +0.583 | -0.359 [-1.985, +1.166] | 57.9 | -4.757 | +0.570 [-7.187, +3.309] | 31.6 |
| 1d | BRK_mem_first | EXP_COUNTER | both | +0.870 | +0.094 [-0.451, +0.581] | 90.0 | -0.069 | +0.437 [-0.569, +2.489] | 45.0 | +0.353 | +0.021 [-0.671, +1.192] | 60.0 | -2.393 | -0.506 [-3.742, +1.607] | 35.0 |
| 1d | BRK_mem_first | EXP_COUNTER | long | +1.392 | -0.147 [-0.594, +0.513] | 95.0 | +0.451 | +0.075 [-0.758, +1.296] | 55.0 | +0.770 | -0.795 [-1.506, +0.944] | 70.0 | +1.544 | -0.897 [-4.403, -0.021] | 80.0 |
| 1d | BRK_mem_first | EXP_COUNTER | short | +0.353 | +0.359 [-0.652, +1.705] | 41.2 | -6.874 | -0.077 [-4.319, +3.665] | 17.6 | +0.353 | +0.409 [-0.429, +1.814] | 37.5 | -6.874 | +0.853 [-4.806, +3.672] | 18.8 |
| 1d | BRK_mem_first | IN_RANGE_COINCIDENT* | both | — | +0.971 [-1.191, +3.134] | — | — | +1.341 [-1.053, +3.735] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | IN_RANGE_COINCIDENT* | long | — | -3.353 [-3.353, -3.353] | — | — | -3.446 [-3.446, -3.446] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | IN_RANGE_COINCIDENT* | short | — | +5.296 [+5.296, +5.296] | — | — | +6.129 [+6.129, +6.129] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | IN_RANGE_MID* | both | +0.345 | -0.114 [-0.188, +0.547] | 70.0 | -3.437 | -1.378 [-4.098, +1.162] | 30.0 | +0.717 | -0.065 [-0.343, +0.833] | 68.4 | -3.285 | -1.735 [-4.960, +1.916] | 36.8 |
| 1d | BRK_mem_first | IN_RANGE_MID* | long | +0.065 | -0.166 [-0.906, +0.009] | 77.8 | -3.614 | -0.019 [-2.264, +5.758] | 11.1 | +0.295 | -0.128 [-0.337, +0.210] | 81.2 | -2.876 | +2.672 [-1.198, +6.642] | 12.5 |
| 1d | BRK_mem_first | IN_RANGE_MID* | short | +1.402 | +0.345 [-0.141, +0.845] | 94.1 | -3.437 | -5.404 [-12.220, -2.276] | 64.7 | +1.402 | +0.345 [-0.732, +0.842] | 93.3 | -3.437 | -7.893 [-12.220, -3.478] | 71.4 |
| 1d | BRK_mem_first | IN_RANGE_OTHER | both | +0.024 | +0.294 [-0.110, +1.273] | 31.6 | +2.587 | +1.286 [-2.545, +3.197] | 63.2 | +0.179 | +1.459 [+0.160, +3.169] | 27.8 | -2.170 | +0.869 [-6.483, +5.106] | 46.7 |
| 1d | BRK_mem_first | IN_RANGE_OTHER | long | -0.312 | +1.015 [-0.575, +3.049] | 31.2 | +1.350 | +0.458 [-1.872, +4.986] | 56.2 | -0.312 | +2.828 [+1.474, +4.742] | 6.7 | +1.350 | +3.392 [-3.556, +8.026] | 41.7 |
| 1d | BRK_mem_first | IN_RANGE_OTHER | short | +0.362 | +0.075 [-1.609, +0.459] | 75.0 | +2.587 | +1.721 [-2.808, +3.205] | 58.3 | +0.689 | -0.026 [-0.343, +0.327] | 83.3 | -9.638 | -5.846 [-8.190, -0.127] | 16.7 |
| 1d | BRK_mem_first | NONE | both | +0.939 | +0.800 [+0.343, +1.928] | 50.0 | +1.921 | +0.916 [-0.424, +8.368] | 55.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | NONE | long | +2.199 | +1.796 [+0.874, +3.432] | 65.0 | +5.725 | +5.891 [+1.922, +9.501] | 45.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_first | NONE | short | -0.612 | -1.429 [-2.838, -0.527] | 71.4 | -20.985 | -2.442 [-12.406, -0.643] | 21.4 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | ALL | both | +0.400 | +0.104 [-0.109, +0.370] | 75.0 | -1.470 | +0.115 [-0.835, +1.395] | 20.0 | +0.671 | +0.179 [-0.116, +0.696] | 75.0 | -3.961 | -1.528 [-2.918, +0.449] | 10.0 |
| 1d | BRK_mem_oneshot | ALL | long | +0.290 | +0.205 [-0.164, +0.547] | 60.0 | -0.347 | +0.667 [+0.142, +1.622] | 20.0 | -0.187 | +0.249 [-0.365, +0.816] | 35.0 | -2.543 | -1.108 [-2.085, +0.552] | 25.0 |
| 1d | BRK_mem_oneshot | ALL | short | +0.495 | +0.004 [-0.146, +0.373] | 80.0 | -3.601 | -1.226 [-3.062, +1.166] | 25.0 | +1.077 | +0.206 [-0.763, +1.005] | 80.0 | -5.515 | -2.443 [-4.709, +2.438] | 25.0 |
| 1d | BRK_mem_oneshot | EXP_ALIGNED* | both | +0.494 | +0.246 [-0.726, +0.662] | 65.0 | -4.313 | -0.795 [-2.815, +1.312] | 5.0 | +0.963 | -0.348 [-0.675, +0.264] | 83.3 | -7.019 | -1.213 [-3.637, +0.981] | 11.1 |
| 1d | BRK_mem_oneshot | EXP_ALIGNED* | long | +1.168 | +0.481 [-0.642, +1.189] | 64.7 | -5.018 | -0.986 [-3.729, +1.332] | 5.9 | +0.420 | -0.556 [-1.660, +0.912] | 69.2 | -6.167 | -3.787 [-5.070, -0.986] | 15.4 |
| 1d | BRK_mem_oneshot | EXP_ALIGNED* | short | +0.404 | -0.135 [-1.502, +0.745] | 60.0 | -3.615 | -0.696 [-3.368, +1.748] | 25.0 | +1.180 | -0.019 [-2.168, +1.029] | 81.2 | -7.222 | +1.269 [-3.746, +3.438] | 18.8 |
| 1d | BRK_mem_oneshot | EXP_COUNTER | both | +0.318 | +0.008 [-0.330, +0.579] | 70.0 | -0.206 | -0.300 [-1.663, +1.246] | 50.0 | +0.047 | +0.056 [-0.649, +0.802] | 50.0 | -4.316 | -1.846 [-4.331, -0.444] | 27.5 |
| 1d | BRK_mem_oneshot | EXP_COUNTER | long | +0.290 | -0.001 [-0.279, +0.307] | 75.0 | -0.075 | +0.051 [-0.783, +1.299] | 50.0 | -1.723 | -0.233 [-1.506, +1.030] | 22.5 | -0.463 | -1.491 [-5.066, +1.043] | 62.5 |
| 1d | BRK_mem_oneshot | EXP_COUNTER | short | +0.353 | +0.225 [-0.485, +0.912] | 53.3 | -6.874 | -1.872 [-7.010, +3.573] | 26.7 | +0.353 | +0.359 [+0.059, +1.471] | 41.7 | -6.874 | -0.382 [-4.508, +3.640] | 8.3 |
| 1d | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | both | — | -1.222 [-2.288, +2.037] | — | — | -2.087 [-2.767, +2.021] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | long | — | -2.288 [-2.821, -1.755] | — | — | -2.767 [-3.107, -2.427] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | IN_RANGE_COINCIDENT* | short | — | +5.296 [+5.296, +5.296] | — | — | +6.129 [+6.129, +6.129] | — | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | IN_RANGE_MID* | both | +0.692 | -0.140 [-0.347, +1.037] | 65.0 | -3.283 | -2.142 [-5.592, +3.520] | 35.0 | +1.091 | -0.141 [-0.346, +1.041] | 84.2 | -3.079 | -2.002 [-4.499, +3.596] | 36.8 |
| 1d | BRK_mem_oneshot | IN_RANGE_MID* | long | +0.065 | -0.162 [-0.291, +1.084] | 58.8 | -3.614 | +2.632 [-2.627, +6.171] | 11.8 | +0.295 | -0.145 [-0.228, +2.164] | 66.7 | -2.876 | +2.712 [-0.411, +7.113] | 13.3 |
| 1d | BRK_mem_oneshot | IN_RANGE_MID* | short | +1.452 | +0.344 [+0.081, +0.892] | 93.8 | -3.283 | -4.436 [-9.832, -1.755] | 60.0 | +1.452 | +0.345 [-0.732, +0.886] | 93.3 | -3.283 | -6.063 [-12.220, -2.207] | 66.7 |
| 1d | BRK_mem_oneshot | IN_RANGE_OTHER | both | +0.347 | +0.068 [-1.017, +1.222] | 63.2 | +1.637 | +1.286 [-1.605, +3.416] | 57.9 | +0.179 | +1.459 [-0.111, +3.257] | 31.2 | -2.170 | +1.919 [-3.461, +6.620] | 27.3 |
| 1d | BRK_mem_oneshot | IN_RANGE_OTHER | long | -0.312 | -0.186 [-1.805, +2.041] | 46.7 | +1.350 | -0.371 [-3.577, +2.558] | 73.3 | -0.312 | +2.278 [+1.527, +5.612] | 16.7 | +1.350 | +4.272 [+0.285, +7.893] | 33.3 |
| 1d | BRK_mem_oneshot | IN_RANGE_OTHER | short | +0.687 | +0.068 [-0.922, +0.759] | 66.7 | +1.638 | +2.444 [+0.069, +4.183] | 36.4 | +0.689 | -0.111 [-0.111, +0.369] | 77.8 | -9.638 | -6.241 [-8.618, -3.865] | 50.0 |
| 1d | BRK_mem_oneshot | NONE | both | +0.939 | +0.676 [+0.400, +2.106] | 57.9 | +1.921 | +1.426 [-0.208, +6.923] | 52.6 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | NONE | long | +2.199 | +1.625 [+0.812, +4.005] | 57.9 | +5.725 | +4.208 [+1.264, +9.797] | 52.6 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | BRK_mem_oneshot | NONE | short | -0.612 | -1.178 [-2.780, -0.285] | 69.2 | -20.985 | -3.288 [-13.517, -0.198] | 23.1 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | SFP_harden | ALL | both | -0.781 | -0.143 [-0.619, +0.162] | 15.0 | +0.999 | +0.365 [-0.660, +1.395] | 65.0 | -0.783 | -0.120 [-0.606, +0.561] | 25.0 | -0.112 | +1.274 [-2.086, +1.885] | 40.0 |
| 1d | SFP_harden | ALL | long | -0.280 | -0.255 [-0.696, +0.625] | 45.0 | -0.104 | +0.471 [-1.547, +1.544] | 45.0 | -0.504 | -0.708 [-1.484, +0.894] | 55.0 | -3.037 | -1.206 [-3.420, +2.904] | 40.0 |
| 1d | SFP_harden | ALL | short | -1.509 | -0.100 [-0.641, +0.635] | 0.0 | +3.035 | +0.698 [-0.602, +1.908] | 90.0 | -1.397 | -0.284 [-0.806, +0.858] | 20.0 | +3.800 | +1.618 [-0.000, +3.597] | 80.0 |
| 1d | SFP_harden | EXP_ALIGNED* | both | -0.796 | -0.041 [-0.641, +0.294] | 15.0 | -3.923 | -0.149 [-1.264, +1.359] | 5.0 | -0.508 | -0.221 [-1.141, +0.379] | 45.0 | -5.667 | -0.113 [-3.935, +3.641] | 5.0 |
| 1d | SFP_harden | EXP_ALIGNED* | long | -0.508 | -0.168 [-1.285, +1.136] | 44.4 | -5.667 | -3.351 [-4.527, +0.924] | 5.6 | -0.508 | -0.347 [-1.580, +0.266] | 50.0 | -5.667 | -4.230 [-5.036, -1.426] | 0.0 |
| 1d | SFP_harden | EXP_ALIGNED* | short | -0.807 | +0.083 [-0.263, +0.744] | 15.0 | +3.165 | +1.489 [-0.356, +2.645] | 85.0 | — | +0.020 [-1.470, +1.314] | — | — | +4.354 [+0.100, +5.641] | — |
| 1d | SFP_harden | EXP_COUNTER | both | -0.254 | -0.256 [-0.888, +0.112] | 50.0 | +1.471 | -0.623 [-1.770, +1.761] | 70.0 | -0.072 | -0.396 [-1.180, +0.635] | 60.0 | +1.466 | +1.661 [-1.519, +3.164] | 45.0 |
| 1d | SFP_harden | EXP_COUNTER | long | -0.268 | -0.426 [-1.071, +0.176] | 55.0 | +1.006 | -0.909 [-2.653, +1.055] | 75.0 | -0.126 | +0.305 [-1.836, +3.296] | 44.4 | +1.010 | -1.753 [-3.067, +1.611] | 66.7 |
| 1d | SFP_harden | EXP_COUNTER | short | +0.817 | -0.392 [-0.847, +1.855] | 63.2 | +4.554 | +1.745 [-1.282, +3.816] | 78.9 | +0.817 | +0.713 [-0.637, +1.715] | 52.9 | +4.554 | +3.293 [+1.343, +4.442] | 76.5 |
| 1d | SFP_harden | IN_RANGE_COINCIDENT* | both | +3.244 | -0.328 [-0.658, +0.623] | 100.0 | — | -1.547 [-2.270, +0.266] | — | +3.244 | +1.932 [+1.278, +2.587] | 100.0 | — | +5.560 [+5.560, +5.560] | — |
| 1d | SFP_harden | IN_RANGE_COINCIDENT* | long | +3.244 | +1.292 [+0.317, +2.267] | 100.0 | — | -4.293 [-4.293, -4.293] | — | +3.244 | +3.242 [+3.242, +3.242] | 100.0 | — | — [—, —] | — |
| 1d | SFP_harden | IN_RANGE_COINCIDENT* | short | — | -0.328 [-1.052, +0.148] | — | — | -1.498 [-1.547, +2.031] | — | — | +0.623 [+0.623, +0.623] | — | — | +5.560 [+5.560, +5.560] | — |
| 1d | SFP_harden | IN_RANGE_MID* | both | -1.474 | +0.144 [-0.640, +1.427] | 15.0 | +1.246 | +6.023 [-0.296, +11.863] | 26.3 | -1.474 | +0.144 [-0.956, +1.427] | 25.0 | -1.809 | +6.023 [-3.802, +11.863] | 36.8 |
| 1d | SFP_harden | IN_RANGE_MID* | long | -1.223 | +1.360 [-0.322, +2.295] | 10.5 | +1.248 | +8.013 [+4.361, +85.712] | 16.7 | -1.223 | +1.496 [-0.429, +2.325] | 16.7 | +1.316 | +8.047 [+6.023, +108.798] | 23.5 |
| 1d | SFP_harden | IN_RANGE_MID* | short | -1.501 | -0.811 [-4.373, +0.427] | 45.5 | -55.873 | -3.590 [-59.686, +0.228] | 36.4 | -1.501 | -0.811 [-5.960, +0.598] | 45.5 | -55.873 | -3.590 [-85.010, +0.228] | 36.4 |
| 1d | SFP_harden | IN_RANGE_OTHER | both | -1.505 | -0.998 [-2.159, -0.150] | 45.0 | +3.976 | -0.829 [-3.239, +1.009] | 90.0 | -2.277 | -0.422 [-2.055, +2.352] | 25.0 | +3.849 | +0.446 [-3.904, +3.397] | 77.8 |
| 1d | SFP_harden | IN_RANGE_OTHER | long | — | -1.727 [-2.570, -0.506] | — | — | -2.451 [-5.778, -1.113] | — | — | -1.727 [-3.349, +3.425] | — | — | +0.876 [-5.744, +2.964] | — |
| 1d | SFP_harden | IN_RANGE_OTHER | short | -1.505 | -0.107 [-2.229, +1.373] | 31.6 | +3.976 | +2.653 [-2.043, +4.460] | 55.6 | -2.277 | -0.583 [-2.578, +1.896] | 33.3 | +3.849 | -0.699 [-4.014, +3.066] | 76.5 |
| 1d | SFP_harden | NONE | both | -1.041 | +0.176 [-0.880, +0.992] | 25.0 | -1.072 | +1.331 [-2.391, +2.785] | 40.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | SFP_harden | NONE | long | -0.157 | +1.263 [-0.087, +2.927] | 25.0 | +1.572 | +8.684 [+2.865, +10.528] | 20.0 | — | — [—, —] | — | — | — [—, —] | — |
| 1d | SFP_harden | NONE | short | -4.339 | -1.064 [-2.151, +0.485] | 10.0 | -34.137 | -5.133 [-7.966, -1.230] | 5.0 | — | — [—, —] | — | — | — [—, —] | — |

## 8 · Null schedule diagnostics (seed of record; every (asset, lens, scale))

| asset | lens | scale | draws | boxes per draw (= real confirmed ranges) | draws whose lead gap was swapped (< ATR_LEN) | draws whose schedule IS the real one |
|---|---|---|---|---|---|---|
| 1000BONKUSDT | 1d | calibrated | 20 | 7 | 3 | 0 |
| 1000BONKUSDT | 1d | frozen3.0 | 20 | 5 | 0 | 0 |
| 1000BONKUSDT | 1h | calibrated | 20 | 174 | 1 | 0 |
| 1000BONKUSDT | 1h | frozen3.0 | 20 | 90 | 0 | 0 |
| 1000BONKUSDT | 4h | calibrated | 20 | 35 | 3 | 0 |
| 1000BONKUSDT | 4h | frozen3.0 | 20 | 20 | 0 | 0 |
| 1000PEPEUSDT | 1d | calibrated | 20 | 7 | 1 | 0 |
| 1000PEPEUSDT | 1d | frozen3.0 | 20 | 7 | 1 | 0 |
| 1000PEPEUSDT | 1h | calibrated | 20 | 224 | 1 | 0 |
| 1000PEPEUSDT | 1h | frozen3.0 | 20 | 104 | 1 | 0 |
| 1000PEPEUSDT | 4h | calibrated | 20 | 51 | 2 | 0 |
| 1000PEPEUSDT | 4h | frozen3.0 | 20 | 30 | 0 | 0 |
| BNBUSDT | 1d | calibrated | 20 | 23 | 1 | 0 |
| BNBUSDT | 1d | frozen3.0 | 20 | 8 | 0 | 0 |
| BNBUSDT | 1h | calibrated | 20 | 486 | 1 | 0 |
| BNBUSDT | 1h | frozen3.0 | 20 | 220 | 1 | 0 |
| BNBUSDT | 4h | calibrated | 20 | 94 | 1 | 0 |
| BNBUSDT | 4h | frozen3.0 | 20 | 49 | 0 | 0 |
| BTCUSDT | 12h | calibrated | 20 | 34 | 1 | 0 |
| BTCUSDT | 12h | frozen3.0 | 20 | 18 | 0 | 0 |
| BTCUSDT | 1d | calibrated | 20 | 20 | 1 | 0 |
| BTCUSDT | 1d | frozen3.0 | 20 | 11 | 1 | 0 |
| BTCUSDT | 1h | calibrated | 20 | 522 | 3 | 0 |
| BTCUSDT | 1h | frozen3.0 | 20 | 223 | 0 | 0 |
| BTCUSDT | 4h | calibrated | 20 | 111 | 0 | 0 |
| BTCUSDT | 4h | frozen3.0 | 20 | 63 | 1 | 0 |
| DOGEUSDT | 1d | calibrated | 20 | 17 | 2 | 0 |
| DOGEUSDT | 1d | frozen3.0 | 20 | 10 | 0 | 0 |
| DOGEUSDT | 1h | calibrated | 20 | 399 | 2 | 0 |
| DOGEUSDT | 1h | frozen3.0 | 20 | 182 | 0 | 0 |
| DOGEUSDT | 4h | calibrated | 20 | 92 | 3 | 0 |
| DOGEUSDT | 4h | frozen3.0 | 20 | 46 | 0 | 0 |
| ENAUSDT | 1d | calibrated | 20 | 6 | 0 | 0 |
| ENAUSDT | 1d | frozen3.0 | 20 | 1 | 0 | 7 |
| ENAUSDT | 1h | calibrated | 20 | 222 | 6 | 0 |
| ENAUSDT | 1h | frozen3.0 | 20 | 78 | 0 | 0 |
| ENAUSDT | 4h | calibrated | 20 | 28 | 0 | 0 |
| ENAUSDT | 4h | frozen3.0 | 20 | 24 | 0 | 0 |
| ETHUSDT | 12h | calibrated | 20 | 44 | 0 | 0 |
| ETHUSDT | 12h | frozen3.0 | 20 | 15 | 0 | 0 |
| ETHUSDT | 1d | calibrated | 20 | 20 | 4 | 0 |
| ETHUSDT | 1d | frozen3.0 | 20 | 9 | 0 | 0 |
| ETHUSDT | 1h | calibrated | 20 | 441 | 1 | 0 |
| ETHUSDT | 1h | frozen3.0 | 20 | 231 | 1 | 0 |
| ETHUSDT | 4h | calibrated | 20 | 113 | 1 | 0 |
| ETHUSDT | 4h | frozen3.0 | 20 | 63 | 0 | 0 |
| HYPEUSDT | 1d | calibrated | 20 | 4 | 0 | 0 |
| HYPEUSDT | 1d | frozen3.0 | 20 | 2 | 0 | 2 |
| HYPEUSDT | 1h | calibrated | 20 | 82 | 0 | 0 |
| HYPEUSDT | 1h | frozen3.0 | 20 | 40 | 0 | 0 |
| HYPEUSDT | 4h | calibrated | 20 | 22 | 0 | 0 |
| HYPEUSDT | 4h | frozen3.0 | 20 | 15 | 0 | 0 |
| LTCUSDT | 1d | calibrated | 20 | 19 | 1 | 0 |
| LTCUSDT | 1d | frozen3.0 | 20 | 13 | 2 | 0 |
| LTCUSDT | 1h | calibrated | 20 | 465 | 1 | 0 |
| LTCUSDT | 1h | frozen3.0 | 20 | 217 | 0 | 0 |
| LTCUSDT | 4h | calibrated | 20 | 109 | 1 | 0 |
| LTCUSDT | 4h | frozen3.0 | 20 | 64 | 0 | 0 |
| MNTUSDT_BYBIT | 1d | calibrated | 20 | 8 | 3 | 0 |
| MNTUSDT_BYBIT | 1d | frozen3.0 | 20 | 5 | 0 | 0 |
| MNTUSDT_BYBIT | 1h | calibrated | 20 | 162 | 0 | 0 |
| MNTUSDT_BYBIT | 1h | frozen3.0 | 20 | 97 | 0 | 0 |
| MNTUSDT_BYBIT | 4h | calibrated | 20 | 49 | 3 | 0 |
| MNTUSDT_BYBIT | 4h | frozen3.0 | 20 | 31 | 0 | 0 |
| NEARUSDT | 12h | calibrated | 20 | 36 | 1 | 0 |
| NEARUSDT | 12h | frozen3.0 | 20 | 17 | 0 | 0 |
| NEARUSDT | 1d | calibrated | 20 | 16 | 0 | 0 |
| NEARUSDT | 1d | frozen3.0 | 20 | 8 | 5 | 0 |
| NEARUSDT | 1h | calibrated | 20 | 438 | 0 | 0 |
| NEARUSDT | 1h | frozen3.0 | 20 | 211 | 0 | 0 |
| NEARUSDT | 4h | calibrated | 20 | 112 | 2 | 0 |
| NEARUSDT | 4h | frozen3.0 | 20 | 58 | 0 | 0 |
| PUMPUSDT | 1d | calibrated | 20 | 3 | 0 | 0 |
| PUMPUSDT | 1d | frozen3.0 | 20 | 2 | 0 | 3 |
| PUMPUSDT | 1h | calibrated | 20 | 75 | 1 | 0 |
| PUMPUSDT | 1h | frozen3.0 | 20 | 42 | 0 | 0 |
| PUMPUSDT | 4h | calibrated | 20 | 21 | 1 | 0 |
| PUMPUSDT | 4h | frozen3.0 | 20 | 7 | 0 | 0 |
| SOLUSDT | 12h | calibrated | 20 | 32 | 0 | 0 |
| SOLUSDT | 12h | frozen3.0 | 20 | 21 | 0 | 0 |
| SOLUSDT | 1d | calibrated | 20 | 18 | 0 | 0 |
| SOLUSDT | 1d | frozen3.0 | 20 | 12 | 1 | 0 |
| SOLUSDT | 1h | calibrated | 20 | 441 | 2 | 0 |
| SOLUSDT | 1h | frozen3.0 | 20 | 203 | 1 | 0 |
| SOLUSDT | 4h | calibrated | 20 | 88 | 1 | 0 |
| SOLUSDT | 4h | frozen3.0 | 20 | 53 | 0 | 0 |
| SUIUSDT | 1d | calibrated | 20 | 12 | 1 | 0 |
| SUIUSDT | 1d | frozen3.0 | 20 | 3 | 7 | 0 |
| SUIUSDT | 1h | calibrated | 20 | 230 | 2 | 0 |
| SUIUSDT | 1h | frozen3.0 | 20 | 108 | 0 | 0 |
| SUIUSDT | 4h | calibrated | 20 | 52 | 0 | 0 |
| SUIUSDT | 4h | frozen3.0 | 20 | 30 | 0 | 0 |
| UNIUSDT | 1d | calibrated | 20 | 13 | 0 | 0 |
| UNIUSDT | 1d | frozen3.0 | 20 | 9 | 0 | 0 |
| UNIUSDT | 1h | calibrated | 20 | 375 | 1 | 0 |
| UNIUSDT | 1h | frozen3.0 | 20 | 182 | 0 | 0 |
| UNIUSDT | 4h | calibrated | 20 | 93 | 0 | 0 |
| UNIUSDT | 4h | frozen3.0 | 20 | 55 | 0 | 0 |
| XMRUSDT | 1d | calibrated | 20 | 15 | 0 | 0 |
| XMRUSDT | 1d | frozen3.0 | 20 | 3 | 0 | 1 |
| XMRUSDT | 1h | calibrated | 20 | 435 | 3 | 0 |
| XMRUSDT | 1h | frozen3.0 | 20 | 173 | 1 | 0 |
| XMRUSDT | 4h | calibrated | 20 | 97 | 4 | 0 |
| XMRUSDT | 4h | frozen3.0 | 20 | 40 | 0 | 0 |
| ZECUSDT | 12h | calibrated | 20 | 33 | 0 | 0 |
| ZECUSDT | 12h | frozen3.0 | 20 | 21 | 0 | 0 |
| ZECUSDT | 1d | calibrated | 20 | 19 | 0 | 0 |
| ZECUSDT | 1d | frozen3.0 | 20 | 13 | 0 | 0 |
| ZECUSDT | 1h | calibrated | 20 | 411 | 0 | 0 |
| ZECUSDT | 1h | frozen3.0 | 20 | 220 | 0 | 0 |
| ZECUSDT | 4h | calibrated | 20 | 112 | 2 | 0 |
| ZECUSDT | 4h | frozen3.0 | 20 | 61 | 0 | 0 |

## 9 · Scan ledger [R4-10] — every evaluated touch (R4_SCAN) and every death (R4_DEATHS), per panel x lens x scale x band (whole; per asset in the parquets). END per death: hold = its first hold (the BREAKOUT event, rule first); truncated = a touch whose hold window passes the tape ended it; failed-out = every touch in the candidacy window failed; no-touch = no qualifying touch in the window. A truncated touch's known_at lies beyond the pin (era 'beyond_pin').

| panel | lens | scale | band | deaths | end hold (first hold) | end truncated | end failed-out | end no-touch | evaluated touches | touches failed | touches hold | touches truncated |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CLASSIC5 | 1h | calibrated | tap89 | 2251 | 1790 | 0 | 212 | 249 | 2569 | 779 | 1790 | 0 |
| CLASSIC5 | 1h | calibrated | tap127 | 2251 | 1588 | 0 | 200 | 463 | 2226 | 638 | 1588 | 0 |
| CLASSIC5 | 1h | calibrated | tap200 | 2251 | 1296 | 0 | 200 | 755 | 1819 | 523 | 1296 | 0 |
| CLASSIC5 | 1h | calibrated | memory-line | 2251 | 1390 | 0 | 316 | 545 | 2623 | 1233 | 1390 | 0 |
| CLASSIC5 | 1h | frozen3.0 | tap89 | 1087 | 1021 | 0 | 49 | 17 | 1439 | 418 | 1021 | 0 |
| CLASSIC5 | 1h | frozen3.0 | tap127 | 1087 | 971 | 0 | 65 | 51 | 1392 | 421 | 971 | 0 |
| CLASSIC5 | 1h | frozen3.0 | tap200 | 1087 | 879 | 0 | 81 | 127 | 1261 | 382 | 879 | 0 |
| CLASSIC5 | 1h | frozen3.0 | memory-line | 1087 | 752 | 0 | 112 | 223 | 1325 | 573 | 752 | 0 |
| CLASSIC5 | 4h | calibrated | tap89 | 536 | 450 | 0 | 44 | 42 | 612 | 162 | 450 | 0 |
| CLASSIC5 | 4h | calibrated | tap127 | 536 | 403 | 0 | 44 | 89 | 539 | 136 | 403 | 0 |
| CLASSIC5 | 4h | calibrated | tap200 | 536 | 333 | 0 | 41 | 162 | 456 | 123 | 333 | 0 |
| CLASSIC5 | 4h | calibrated | memory-line | 536 | 310 | 0 | 89 | 137 | 597 | 287 | 310 | 0 |
| CLASSIC5 | 4h | frozen3.0 | tap89 | 298 | 281 | 0 | 12 | 5 | 373 | 92 | 281 | 0 |
| CLASSIC5 | 4h | frozen3.0 | tap127 | 298 | 266 | 0 | 14 | 18 | 359 | 93 | 266 | 0 |
| CLASSIC5 | 4h | frozen3.0 | tap200 | 298 | 234 | 0 | 16 | 48 | 332 | 98 | 234 | 0 |
| CLASSIC5 | 4h | frozen3.0 | memory-line | 298 | 196 | 0 | 36 | 66 | 354 | 158 | 196 | 0 |
| CLASSIC5 | 12h | calibrated | tap89 | 179 | 137 | 0 | 14 | 28 | 197 | 60 | 137 | 0 |
| CLASSIC5 | 12h | calibrated | tap127 | 179 | 118 | 0 | 18 | 43 | 165 | 47 | 118 | 0 |
| CLASSIC5 | 12h | calibrated | tap200 | 179 | 99 | 0 | 9 | 71 | 137 | 38 | 99 | 0 |
| CLASSIC5 | 12h | calibrated | memory-line | 179 | 100 | 0 | 28 | 51 | 183 | 83 | 100 | 0 |
| CLASSIC5 | 12h | frozen3.0 | tap89 | 91 | 84 | 0 | 3 | 4 | 119 | 35 | 84 | 0 |
| CLASSIC5 | 12h | frozen3.0 | tap127 | 91 | 79 | 0 | 5 | 7 | 104 | 25 | 79 | 0 |
| CLASSIC5 | 12h | frozen3.0 | tap200 | 91 | 69 | 0 | 7 | 15 | 97 | 28 | 69 | 0 |
| CLASSIC5 | 12h | frozen3.0 | memory-line | 91 | 61 | 0 | 8 | 22 | 108 | 47 | 61 | 0 |
| CLASSIC5 | 1d | calibrated | tap89 | 93 | 71 | 0 | 9 | 13 | 93 | 22 | 71 | 0 |
| CLASSIC5 | 1d | calibrated | tap127 | 93 | 60 | 0 | 11 | 22 | 81 | 21 | 60 | 0 |
| CLASSIC5 | 1d | calibrated | tap200 | 93 | 51 | 0 | 10 | 32 | 81 | 30 | 51 | 0 |
| CLASSIC5 | 1d | calibrated | memory-line | 93 | 56 | 0 | 11 | 26 | 105 | 49 | 56 | 0 |
| CLASSIC5 | 1d | frozen3.0 | tap89 | 53 | 43 | 0 | 5 | 5 | 61 | 18 | 43 | 0 |
| CLASSIC5 | 1d | frozen3.0 | tap127 | 53 | 38 | 0 | 5 | 10 | 54 | 16 | 38 | 0 |
| CLASSIC5 | 1d | frozen3.0 | tap200 | 53 | 35 | 0 | 5 | 13 | 53 | 18 | 35 | 0 |
| CLASSIC5 | 1d | frozen3.0 | memory-line | 53 | 35 | 0 | 2 | 16 | 47 | 12 | 35 | 0 |
| UNSEEN12 | 1h | calibrated | tap89 | 3325 | 2690 | 0 | 232 | 403 | 3652 | 962 | 2690 | 0 |
| UNSEEN12 | 1h | calibrated | tap127 | 3325 | 2393 | 0 | 265 | 667 | 3278 | 885 | 2393 | 0 |
| UNSEEN12 | 1h | calibrated | tap200 | 3325 | 2000 | 0 | 277 | 1048 | 2812 | 812 | 2000 | 0 |
| UNSEEN12 | 1h | calibrated | memory-line | 3325 | 2089 | 0 | 448 | 788 | 3997 | 1908 | 2089 | 0 |
| UNSEEN12 | 1h | frozen3.0 | tap89 | 1532 | 1468 | 0 | 51 | 13 | 2001 | 533 | 1468 | 0 |
| UNSEEN12 | 1h | frozen3.0 | tap127 | 1532 | 1397 | 0 | 79 | 56 | 1985 | 588 | 1397 | 0 |
| UNSEEN12 | 1h | frozen3.0 | tap200 | 1532 | 1283 | 0 | 96 | 153 | 1834 | 551 | 1283 | 0 |
| UNSEEN12 | 1h | frozen3.0 | memory-line | 1532 | 1107 | 0 | 152 | 273 | 2014 | 907 | 1107 | 0 |
| UNSEEN12 | 4h | calibrated | tap89 | 741 | 619 | 0 | 46 | 76 | 831 | 212 | 619 | 0 |
| UNSEEN12 | 4h | calibrated | tap127 | 741 | 535 | 0 | 62 | 144 | 734 | 199 | 535 | 0 |
| UNSEEN12 | 4h | calibrated | tap200 | 741 | 452 | 0 | 57 | 232 | 631 | 179 | 452 | 0 |
| UNSEEN12 | 4h | calibrated | memory-line | 741 | 470 | 0 | 86 | 185 | 833 | 363 | 470 | 0 |
| UNSEEN12 | 4h | frozen3.0 | tap89 | 410 | 378 | 0 | 21 | 11 | 530 | 152 | 378 | 0 |
| UNSEEN12 | 4h | frozen3.0 | tap127 | 410 | 357 | 0 | 24 | 29 | 517 | 160 | 357 | 0 |
| UNSEEN12 | 4h | frozen3.0 | tap200 | 410 | 311 | 0 | 35 | 64 | 470 | 159 | 311 | 0 |
| UNSEEN12 | 4h | frozen3.0 | memory-line | 410 | 277 | 1 | 50 | 82 | 502 | 224 | 277 | 1 |
| UNSEEN12 | 1d | calibrated | tap89 | 133 | 102 | 0 | 9 | 22 | 140 | 38 | 102 | 0 |
| UNSEEN12 | 1d | calibrated | tap127 | 133 | 90 | 1 | 7 | 35 | 131 | 40 | 90 | 1 |
| UNSEEN12 | 1d | calibrated | tap200 | 133 | 70 | 1 | 7 | 55 | 100 | 29 | 70 | 1 |
| UNSEEN12 | 1d | calibrated | memory-line | 133 | 92 | 2 | 9 | 30 | 140 | 46 | 92 | 2 |
| UNSEEN12 | 1d | frozen3.0 | tap89 | 67 | 57 | 0 | 4 | 6 | 84 | 27 | 57 | 0 |
| UNSEEN12 | 1d | frozen3.0 | tap127 | 67 | 55 | 1 | 1 | 10 | 79 | 23 | 55 | 1 |
| UNSEEN12 | 1d | frozen3.0 | tap200 | 67 | 43 | 0 | 2 | 22 | 71 | 28 | 43 | 0 |
| UNSEEN12 | 1d | frozen3.0 | memory-line | 67 | 51 | 2 | 1 | 13 | 76 | 23 | 51 | 2 |

## 10 · Appendix — every asset and both pools · calibrated · cell law record · L+1 cell ALL (whole over asset x lens x event x direction; n / NET / Δcell as in §4; the partitioned cells in R4_GRID.parquet)

| asset | lens | scale | event | law | L+1 cell | dir | n ALL H20 | NET ALL H20 | Δcell ALL H20 | n ALL H100 | NET ALL H100 | Δcell ALL H100 | n tuning H20 | NET tuning H20 | Δcell tuning H20 | n tuning H100 | NET tuning H100 | Δcell tuning H100 | n holdout H20 | NET holdout H20 | Δcell holdout H20 | n holdout H100 | NET holdout H100 | Δcell holdout H100 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| BTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 382 | -0.104 | +0.031 | 380 | +0.062 | +0.196 | 250 | -0.122 | -0.000 | 250 | -0.197 | -0.075 | 132 | +0.001 | +0.162 | 130 | +0.426 | +0.586 |
| BTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 197 | -0.048 | +0.011 | 196 | +0.126 | -0.074 | 130 | -0.100 | -0.050 | 130 | -0.083 | -0.288 | 67 | +0.199 | +0.278 | 66 | +1.124 | +0.932 |
| BTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 185 | -0.265 | -0.055 | 184 | -0.089 | +0.380 | 120 | -0.137 | +0.057 | 120 | -0.345 | +0.102 | 65 | -0.469 | -0.226 | 64 | +0.196 | +0.710 |
| BTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 319 | -0.107 | +0.028 | 317 | -0.145 | -0.010 | 211 | -0.124 | -0.003 | 211 | -0.289 | -0.167 | 108 | +0.003 | +0.164 | 106 | +0.208 | +0.369 |
| BTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 162 | -0.072 | -0.013 | 161 | +0.120 | -0.080 | 108 | -0.091 | -0.042 | 108 | +0.042 | -0.162 | 54 | +0.009 | +0.089 | 53 | +0.875 | +0.682 |
| BTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 157 | -0.238 | -0.028 | 156 | -0.451 | +0.017 | 103 | -0.254 | -0.060 | 103 | -0.679 | -0.231 | 54 | -0.122 | +0.120 | 53 | -0.098 | +0.416 |
| BTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 338 | -0.106 | +0.028 | 338 | +0.098 | +0.232 | 223 | -0.126 | -0.004 | 223 | +0.013 | +0.135 | 115 | +0.104 | +0.265 | 115 | +0.446 | +0.606 |
| BTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 176 | -0.115 | -0.056 | 176 | +0.404 | +0.204 | 117 | -0.121 | -0.071 | 117 | +0.374 | +0.170 | 59 | +0.104 | +0.183 | 59 | +0.869 | +0.676 |
| BTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 162 | -0.064 | +0.146 | 162 | -0.305 | +0.164 | 106 | -0.189 | +0.005 | 106 | -0.432 | +0.016 | 56 | +0.085 | +0.327 | 56 | +0.093 | +0.607 |
| BTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 291 | -0.162 | -0.028 | 291 | -0.000 | +0.134 | 197 | -0.110 | +0.012 | 197 | +0.015 | +0.137 | 94 | -0.316 | -0.155 | 94 | +0.013 | +0.174 |
| BTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 151 | -0.202 | -0.143 | 151 | +0.433 | +0.234 | 104 | -0.112 | -0.063 | 104 | +0.443 | +0.239 | 47 | -0.824 | -0.745 | 47 | +0.446 | +0.253 |
| BTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 140 | -0.064 | +0.146 | 140 | -0.427 | +0.042 | 93 | -0.096 | +0.098 | 93 | -0.658 | -0.210 | 47 | +0.055 | +0.297 | 47 | -0.327 | +0.187 |
| BTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 273 | -0.103 | +0.031 | 273 | -0.058 | +0.077 | 179 | -0.216 | -0.094 | 179 | +0.006 | +0.128 | 94 | +0.054 | +0.215 | 94 | -0.211 | -0.050 |
| BTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 138 | -0.032 | +0.028 | 138 | +0.666 | +0.466 | 90 | -0.139 | -0.090 | 90 | +0.997 | +0.793 | 48 | +0.285 | +0.364 | 48 | -0.343 | -0.535 |
| BTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 135 | -0.150 | +0.060 | 135 | -0.416 | +0.053 | 89 | -0.238 | -0.044 | 89 | -0.619 | -0.171 | 46 | -0.070 | +0.172 | 46 | -0.066 | +0.448 |
| BTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 236 | -0.106 | +0.029 | 236 | -0.069 | +0.066 | 159 | -0.216 | -0.094 | 159 | +0.006 | +0.128 | 77 | -0.053 | +0.108 | 77 | -0.329 | -0.168 |
| BTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 116 | -0.032 | +0.028 | 116 | +0.856 | +0.656 | 77 | -0.026 | +0.024 | 77 | +1.083 | +0.878 | 39 | -0.053 | +0.026 | 39 | -0.592 | -0.785 |
| BTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 120 | -0.253 | -0.043 | 120 | -0.578 | -0.109 | 82 | -0.297 | -0.103 | 82 | -0.777 | -0.329 | 38 | -0.054 | +0.188 | 38 | -0.066 | +0.448 |
| BTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 293 | -0.427 | -0.292 | 293 | -0.497 | -0.363 | 198 | -0.455 | -0.334 | 198 | -0.409 | -0.287 | 95 | -0.383 | -0.222 | 95 | -0.705 | -0.544 |
| BTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 161 | -0.323 | -0.264 | 161 | -0.356 | -0.556 | 109 | -0.297 | -0.248 | 109 | -0.342 | -0.546 | 52 | -0.404 | -0.324 | 52 | -0.352 | -0.545 |
| BTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 132 | -0.529 | -0.319 | 132 | -0.773 | -0.304 | 89 | -0.584 | -0.390 | 89 | -0.664 | -0.216 | 43 | -0.363 | -0.121 | 43 | -1.205 | -0.691 |
| BTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 275 | -0.320 | -0.186 | 275 | -0.569 | -0.434 | 188 | -0.318 | -0.196 | 188 | -0.432 | -0.310 | 87 | -0.344 | -0.183 | 87 | -0.895 | -0.735 |
| BTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 148 | -0.313 | -0.254 | 148 | -0.454 | -0.654 | 104 | -0.264 | -0.214 | 104 | -0.310 | -0.514 | 44 | -0.574 | -0.495 | 44 | -1.544 | -1.736 |
| BTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 127 | -0.344 | -0.134 | 127 | -0.859 | -0.391 | 84 | -0.543 | -0.349 | 84 | -1.300 | -0.852 | 43 | +0.008 | +0.250 | 43 | -0.384 | +0.130 |
| BTCUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 541 | +0.060 | +0.195 | 540 | +0.385 | +0.519 | 343 | +0.131 | +0.253 | 343 | +0.258 | +0.380 | 198 | -0.034 | +0.127 | 197 | +0.637 | +0.797 |
| BTCUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 252 | +0.205 | +0.265 | 252 | +0.897 | +0.697 | 164 | +0.217 | +0.266 | 164 | +0.698 | +0.494 | 88 | +0.156 | +0.235 | 88 | +1.213 | +1.020 |
| BTCUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 289 | -0.089 | +0.121 | 288 | -0.212 | +0.257 | 179 | -0.059 | +0.135 | 179 | -0.285 | +0.163 | 110 | -0.164 | +0.078 | 109 | +0.129 | +0.643 |
| BTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 88 | -0.020 | +0.044 | 87 | -0.162 | -0.098 | 59 | +0.017 | +0.075 | 59 | +0.567 | +0.625 | 29 | -0.522 | -0.444 | 28 | -1.283 | -1.205 |
| BTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 49 | -0.033 | -0.113 | 48 | +0.072 | -0.344 | 34 | +0.143 | +0.061 | 34 | +1.267 | +0.781 | 15 | -1.177 | -1.263 | 14 | -1.285 | -1.523 |
| BTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 39 | -0.007 | +0.202 | 39 | -0.620 | -0.075 | 25 | -0.158 | +0.040 | 25 | -0.608 | -0.006 | 14 | +0.516 | +0.759 | 14 | -1.328 | -0.935 |
| BTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 79 | +0.046 | +0.111 | 78 | +0.347 | +0.412 | 52 | +0.072 | +0.131 | 52 | +0.636 | +0.695 | 27 | -0.196 | -0.118 | 26 | -1.283 | -1.205 |
| BTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 44 | -0.088 | -0.169 | 43 | +0.555 | +0.139 | 30 | +0.141 | +0.059 | 30 | +1.914 | +1.428 | 14 | -1.082 | -1.168 | 13 | -1.024 | -1.262 |
| BTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 35 | +0.346 | +0.555 | 35 | -0.621 | -0.076 | 22 | -0.058 | +0.140 | 22 | -0.080 | +0.522 | 13 | +0.687 | +0.929 | 13 | -2.189 | -1.795 |
| BTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 85 | -0.010 | +0.055 | 83 | -0.130 | -0.066 | 56 | -0.018 | +0.040 | 56 | +0.505 | +0.563 | 29 | +0.635 | +0.713 | 27 | -1.022 | -0.944 |
| BTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 46 | -0.115 | -0.195 | 45 | -0.618 | -1.035 | 31 | -0.024 | -0.106 | 31 | -0.462 | -0.948 | 15 | -0.213 | -0.299 | 14 | -1.225 | -1.463 |
| BTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 39 | +0.126 | +0.335 | 38 | +0.712 | +1.257 | 25 | -0.008 | +0.190 | 25 | +0.563 | +1.165 | 14 | +0.778 | +1.021 | 13 | +2.487 | +2.880 |
| BTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 76 | +0.017 | +0.082 | 74 | +0.204 | +0.268 | 48 | +0.020 | +0.078 | 48 | +0.560 | +0.618 | 28 | +0.214 | +0.292 | 26 | -0.581 | -0.504 |
| BTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 41 | -0.195 | -0.276 | 40 | -0.084 | -0.501 | 27 | +0.052 | -0.030 | 27 | +1.330 | +0.844 | 14 | -0.367 | -0.453 | 13 | -1.023 | -1.261 |
| BTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 35 | +0.123 | +0.333 | 34 | +0.500 | +1.045 | 21 | -0.016 | +0.183 | 21 | +0.441 | +1.043 | 14 | +0.778 | +1.021 | 13 | +2.487 | +2.880 |
| BTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 67 | -0.599 | -0.535 | 66 | -0.154 | -0.090 | 46 | -0.502 | -0.444 | 46 | +0.510 | +0.568 | 21 | -1.130 | -1.052 | 20 | -0.546 | -0.469 |
| BTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 34 | -0.363 | -0.444 | 33 | -0.185 | -0.602 | 22 | +0.168 | +0.086 | 22 | -0.548 | -1.034 | 12 | -0.762 | -0.848 | 11 | -0.216 | -0.454 |
| BTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 33 | -0.687 | -0.478 | 33 | +0.456 | +1.001 | 24 | -0.640 | -0.442 | 24 | +1.129 | +1.731 | 9 | -1.122 | -0.880 | 9 | -0.874 | -0.481 |
| BTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 51 | -0.599 | -0.535 | 50 | +0.033 | +0.097 | 37 | -0.410 | -0.352 | 37 | +0.563 | +0.621 | 14 | -1.158 | -1.080 | 13 | -0.211 | -0.134 |
| BTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 26 | -0.358 | -0.439 | 25 | -0.122 | -0.539 | 19 | +0.734 | +0.652 | 19 | +0.574 | +0.088 | 7 | -1.187 | -1.273 | 6 | -0.191 | -0.429 |
| BTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 25 | -0.872 | -0.663 | 25 | +0.443 | +0.988 | 18 | -0.734 | -0.535 | 18 | +1.122 | +1.724 | 7 | -1.130 | -0.888 | 7 | -0.881 | -0.488 |
| BTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 61 | +0.232 | +0.296 | 61 | +0.330 | +0.394 | 39 | +0.240 | +0.298 | 39 | +0.721 | +0.779 | 22 | +0.385 | +0.463 | 22 | -1.259 | -1.182 |
| BTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 37 | +0.155 | +0.074 | 37 | +0.522 | +0.106 | 24 | +1.266 | +1.184 | 24 | +1.130 | +0.644 | 13 | -0.006 | -0.092 | 13 | -2.526 | -2.764 |
| BTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 24 | +0.474 | +0.683 | 24 | -0.628 | -0.083 | 15 | +0.203 | +0.402 | 15 | -0.552 | +0.050 | 9 | +1.710 | +1.953 | 9 | -0.707 | -0.314 |
| BTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 54 | +0.196 | +0.260 | 54 | +0.078 | +0.143 | 39 | +0.089 | +0.147 | 39 | +0.723 | +0.781 | 15 | +0.625 | +0.703 | 15 | -0.715 | -0.638 |
| BTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 30 | +0.105 | +0.025 | 30 | +0.756 | +0.339 | 22 | +0.354 | +0.272 | 22 | +1.132 | +0.646 | 8 | -0.374 | -0.460 | 8 | +0.048 | -0.190 |
| BTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 24 | +0.476 | +0.686 | 24 | -0.863 | -0.318 | 17 | +0.080 | +0.278 | 17 | -0.548 | +0.054 | 7 | +1.818 | +2.060 | 7 | -1.803 | -1.410 |
| BTCUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 122 | +0.342 | +0.407 | 121 | +0.824 | +0.888 | 73 | +0.450 | +0.508 | 73 | +0.569 | +0.627 | 49 | +0.282 | +0.360 | 48 | +1.232 | +1.310 |
| BTCUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 63 | +0.447 | +0.367 | 62 | +0.583 | +0.166 | 40 | +0.359 | +0.277 | 40 | +0.428 | -0.058 | 23 | +0.450 | +0.364 | 22 | +1.310 | +1.072 |
| BTCUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 59 | +0.294 | +0.504 | 59 | +1.032 | +1.577 | 33 | +1.022 | +1.220 | 33 | +1.042 | +1.644 | 26 | +0.199 | +0.441 | 26 | +1.199 | +1.592 |
| BTCUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | both | 25 | +0.200 | +0.235 | 25 | -2.109 | -2.074 | 17 | +0.488 | +0.520 | 17 | -2.105 | -2.073 | 8 | -0.296 | -0.253 | 8 | -1.769 | -1.727 |
| BTCUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | long | 14 | +0.346 | +0.150 | 14 | -0.399 | -1.379 | 10 | +0.514 | +0.294 | 10 | +2.197 | +1.084 | 4 | -0.468 | -0.579 | 4 | -0.418 | -1.221 |
| BTCUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | short | 11 | -0.244 | +0.022 | 11 | -6.241 | -5.192 | 7 | +0.346 | +0.630 | 7 | -6.239 | -5.062 | 4 | -0.292 | -0.097 | 4 | -5.052 | -4.166 |
| BTCUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 22 | +0.345 | +0.380 | 22 | -2.255 | -2.220 | 15 | +0.535 | +0.567 | 15 | -2.103 | -2.071 | 7 | -0.251 | -0.208 | 7 | -2.998 | -2.957 |
| BTCUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 13 | +0.490 | +0.294 | 13 | -0.521 | -1.501 | 9 | +0.539 | +0.319 | 9 | -1.036 | -2.149 | 4 | -0.468 | -0.579 | 4 | -0.418 | -1.221 |
| BTCUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 9 | -0.241 | +0.025 | 9 | -6.239 | -5.189 | 6 | +1.165 | +1.449 | 6 | -5.605 | -4.428 | 3 | -0.244 | -0.048 | 3 | -7.106 | -6.219 |
| BTCUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | both | 23 | +0.305 | +0.340 | 23 | -4.016 | -3.981 | 16 | +0.295 | +0.327 | 16 | -6.010 | -5.978 | 7 | +2.821 | +2.864 | 7 | -3.374 | -3.333 |
| BTCUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | long | 14 | -0.680 | -0.877 | 14 | +3.023 | +2.043 | 10 | -0.678 | -0.898 | 10 | +3.118 | +2.006 | 4 | +0.580 | +0.470 | 4 | +0.323 | -0.480 |
| BTCUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | short | 9 | +0.478 | +0.744 | 9 | -6.621 | -5.571 | 6 | +0.391 | +0.675 | 6 | -12.218 | -11.041 | 3 | +2.819 | +3.015 | 3 | -4.035 | -3.148 |
| BTCUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 21 | +0.482 | +0.517 | 21 | -4.016 | -3.981 | 14 | +0.399 | +0.431 | 14 | -6.009 | -5.977 | 7 | +2.821 | +2.864 | 7 | -3.374 | -3.333 |
| BTCUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 12 | -0.023 | -0.219 | 12 | +3.023 | +2.043 | 8 | -0.019 | -0.240 | 8 | +3.119 | +2.006 | 4 | +0.580 | +0.470 | 4 | +0.323 | -0.480 |
| BTCUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 9 | +0.478 | +0.744 | 9 | -6.621 | -5.571 | 6 | +0.391 | +0.675 | 6 | -12.218 | -11.041 | 3 | +2.819 | +3.015 | 3 | -4.035 | -3.148 |
| BTCUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | both | 19 | +0.487 | +0.522 | 19 | -3.043 | -3.008 | 12 | +0.789 | +0.821 | 12 | -4.587 | -4.555 | 7 | +0.137 | +0.180 | 7 | +0.807 | +0.848 |
| BTCUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | long | 10 | +0.755 | +0.559 | 10 | -1.108 | -2.088 | 6 | +0.795 | +0.575 | 6 | -0.166 | -1.279 | 4 | +0.441 | +0.331 | 4 | -1.123 | -1.927 |
| BTCUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | short | 9 | +0.137 | +0.403 | 9 | -4.219 | -3.169 | 6 | +0.064 | +0.348 | 6 | -5.902 | -4.725 | 3 | +0.137 | +0.333 | 3 | +7.626 | +8.513 |
| BTCUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 19 | +0.487 | +0.522 | 19 | -3.043 | -3.008 | 12 | +0.789 | +0.821 | 12 | -4.587 | -4.555 | 7 | +0.137 | +0.180 | 7 | +0.807 | +0.848 |
| BTCUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 10 | +0.755 | +0.559 | 10 | -1.108 | -2.088 | 6 | +0.795 | +0.575 | 6 | -0.166 | -1.279 | 4 | +0.441 | +0.331 | 4 | -1.123 | -1.927 |
| BTCUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 9 | +0.137 | +0.403 | 9 | -4.219 | -3.169 | 6 | +0.064 | +0.348 | 6 | -5.902 | -4.725 | 3 | +0.137 | +0.333 | 3 | +7.626 | +8.513 |
| BTCUSDT | 12h | calibrated | BRK_mem_first | record | ALL | both | 15 | -0.007 | +0.028 | 15 | -1.890 | -1.856 | 11 | -0.727 | -0.695 | 11 | -3.809 | -3.777 | 4 | +0.417 | +0.460 | 4 | -1.313 | -1.272 |
| BTCUSDT | 12h | calibrated | BRK_mem_first | record | ALL | long | 9 | -0.727 | -0.923 | 9 | +1.194 | +0.214 | 7 | -0.719 | -0.939 | 7 | +3.322 | +2.209 | 2 | -1.383 | -1.494 | 2 | -7.451 | -8.254 |
| BTCUSDT | 12h | calibrated | BRK_mem_first | record | ALL | short | 6 | +0.479 | +0.745 | 6 | -2.857 | -1.807 | 4 | -1.012 | -0.728 | 4 | -4.026 | -2.849 | 2 | +1.473 | +1.669 | 2 | -1.301 | -0.414 |
| BTCUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 14 | -0.368 | -0.333 | 14 | -2.265 | -2.230 | 11 | -0.727 | -0.695 | 11 | -3.809 | -3.777 | 3 | +0.213 | +0.255 | 3 | -0.730 | -0.688 |
| BTCUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 10 | -0.367 | -0.563 | 10 | +2.254 | +1.274 | 8 | -0.363 | -0.583 | 8 | +3.667 | +2.554 | 2 | -1.383 | -1.494 | 2 | -7.451 | -8.254 |
| BTCUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 4 | -1.011 | -0.745 | 4 | -4.025 | -2.975 | 3 | -2.360 | -2.076 | 3 | -4.235 | -3.058 | 1 | +2.304 | +2.500 | 1 | -0.725 | +0.162 |
| BTCUSDT | 12h | calibrated | SFP_harden | record | ALL | both | 42 | +0.414 | +0.449 | 42 | -0.218 | -0.183 | 18 | +0.194 | +0.226 | 18 | -0.283 | -0.251 | 24 | +0.689 | +0.731 | 24 | -0.070 | -0.029 |
| BTCUSDT | 12h | calibrated | SFP_harden | record | ALL | long | 21 | +0.278 | +0.082 | 21 | +0.589 | -0.391 | 8 | +0.056 | -0.164 | 8 | +1.955 | +0.842 | 13 | +0.739 | +0.629 | 13 | -0.400 | -1.204 |
| BTCUSDT | 12h | calibrated | SFP_harden | record | ALL | short | 21 | +0.915 | +1.182 | 21 | -0.543 | +0.507 | 10 | +1.113 | +1.397 | 10 | -1.092 | +0.085 | 11 | +0.631 | +0.827 | 11 | +0.253 | +1.140 |
| BTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 15 | -0.063 | -0.039 | 15 | -1.279 | -1.255 | 8 | -0.064 | -0.043 | 8 | -1.828 | -1.806 | 7 | +0.625 | +0.653 | 7 | -1.282 | -1.255 |
| BTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 8 | -0.503 | -0.687 | 8 | -1.099 | -2.320 | 5 | -0.072 | -0.322 | 5 | -0.735 | -2.358 | 3 | -0.941 | -0.961 | 3 | -1.470 | -1.125 |
| BTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 7 | +0.629 | +0.861 | 7 | -1.279 | -0.011 | 3 | -0.057 | +0.236 | 3 | -2.920 | -1.254 | 4 | +2.082 | +2.160 | 4 | +1.474 | +1.183 |
| BTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 15 | -0.063 | -0.039 | 15 | -1.279 | -1.255 | 8 | -0.064 | -0.043 | 8 | -1.828 | -1.806 | 7 | +0.625 | +0.653 | 7 | -1.282 | -1.255 |
| BTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | -0.503 | -0.687 | 8 | -1.099 | -2.320 | 5 | -0.072 | -0.322 | 5 | -0.735 | -2.358 | 3 | -0.941 | -0.961 | 3 | -1.470 | -1.125 |
| BTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 7 | +0.629 | +0.861 | 7 | -1.279 | -0.011 | 3 | -0.057 | +0.236 | 3 | -2.920 | -1.254 | 4 | +2.082 | +2.160 | 4 | +1.474 | +1.183 |
| BTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 13 | -0.095 | -0.071 | 13 | -1.432 | -1.408 | 7 | -1.942 | -1.921 | 7 | -1.432 | -1.410 | 6 | +0.259 | +0.287 | 6 | -0.790 | -0.763 |
| BTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 7 | +0.875 | +0.691 | 7 | -1.436 | -2.656 | 5 | +0.879 | +0.629 | 5 | -1.432 | -3.055 | 2 | -2.056 | -2.077 | 2 | -1.899 | -1.554 |
| BTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 6 | -1.018 | -0.786 | 6 | +0.680 | +1.948 | 2 | -3.099 | -2.805 | 2 | -1.133 | +0.532 | 4 | +0.266 | +0.343 | 4 | +0.675 | +0.384 |
| BTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 12 | -0.656 | -0.632 | 12 | -0.696 | -0.672 | 7 | -1.942 | -1.921 | 7 | -1.432 | -1.410 | 5 | +0.622 | +0.650 | 5 | +1.614 | +1.642 |
| BTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | +0.875 | +0.691 | 7 | -1.436 | -2.656 | 5 | +0.879 | +0.629 | 5 | -1.432 | -3.055 | 2 | -2.056 | -2.077 | 2 | -1.899 | -1.554 |
| BTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 5 | -1.942 | -1.710 | 5 | +4.545 | +5.812 | 2 | -3.099 | -2.805 | 2 | -1.133 | +0.532 | 3 | +0.625 | +0.703 | 3 | +4.535 | +4.244 |
| BTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 9 | +0.010 | +0.034 | 9 | -2.682 | -2.659 | 5 | +0.010 | +0.031 | 5 | -0.261 | -0.240 | 4 | -0.007 | +0.021 | 4 | -6.046 | -6.019 |
| BTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 5 | +0.010 | -0.174 | 5 | -0.261 | -1.482 | 4 | +1.983 | +1.733 | 4 | +1.708 | +0.086 | 1 | -1.117 | -1.138 | 1 | -6.096 | -5.751 |
| BTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 4 | -0.012 | +0.220 | 4 | -8.092 | -6.825 | 1 | -2.806 | -2.513 | 1 | -14.218 | -12.552 | 3 | +0.088 | +0.165 | 3 | -5.997 | -6.287 |
| BTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 6 | -0.555 | -0.531 | 6 | -1.473 | -1.450 | 4 | -1.029 | -1.008 | 4 | -1.473 | -1.452 | 2 | +1.172 | +1.200 | 2 | +0.850 | +0.877 |
| BTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 4 | -0.554 | -0.738 | 4 | -1.472 | -2.693 | 3 | +0.010 | -0.241 | 3 | -0.261 | -1.884 | 1 | -1.117 | -1.138 | 1 | -6.096 | -5.751 |
| BTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 2 | +0.327 | +0.559 | 2 | -3.211 | -1.943 | 1 | -2.806 | -2.513 | 1 | -14.218 | -12.552 | 1 | +3.461 | +3.538 | 1 | +7.796 | +7.505 |
| BTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 9 | +0.344 | +0.368 | 8 | -3.827 | -3.804 | 5 | +0.145 | +0.167 | 5 | -1.355 | -1.334 | 4 | +0.346 | +0.374 | 3 | -7.290 | -7.263 |
| BTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 3 | +1.186 | +1.002 | 3 | -1.369 | -2.589 | 2 | +1.676 | +1.426 | 2 | +11.798 | +10.175 | 1 | +1.180 | +1.160 | 1 | -7.308 | -6.962 |
| BTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 6 | -0.054 | +0.178 | 5 | -4.314 | -3.046 | 3 | -0.431 | -0.138 | 3 | -3.337 | -1.672 | 3 | +0.344 | +0.422 | 2 | -8.268 | -8.559 |
| BTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 7 | +0.357 | +0.381 | 6 | -3.828 | -3.805 | 4 | +0.661 | +0.682 | 4 | -2.348 | -2.327 | 3 | +0.347 | +0.375 | 2 | -5.812 | -5.784 |
| BTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 3 | +1.186 | +1.002 | 3 | -1.369 | -2.589 | 2 | +1.676 | +1.426 | 2 | +11.798 | +10.175 | 1 | +1.180 | +1.160 | 1 | -7.308 | -6.962 |
| BTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 4 | -0.054 | +0.178 | 3 | -4.314 | -3.046 | 2 | -0.140 | +0.153 | 2 | -4.839 | -3.174 | 2 | +0.047 | +0.124 | 1 | -4.316 | -4.606 |
| BTCUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 18 | -0.265 | -0.241 | 18 | -0.613 | -0.590 | 7 | -0.251 | -0.229 | 7 | +2.397 | +2.418 | 11 | -0.506 | -0.478 | 11 | -4.753 | -4.725 |
| BTCUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 9 | -0.499 | -0.683 | 9 | -4.745 | -5.966 | 3 | -0.266 | -0.516 | 3 | -2.687 | -4.309 | 6 | -0.642 | -0.663 | 6 | -5.804 | -5.459 |
| BTCUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 9 | +0.013 | +0.245 | 9 | +2.912 | +4.180 | 4 | +0.291 | +0.584 | 4 | +2.654 | +4.319 | 5 | -0.074 | +0.003 | 5 | +3.800 | +3.509 |
| ETHUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 359 | -0.282 | -0.181 | 359 | -0.148 | -0.047 | 249 | -0.138 | -0.042 | 249 | -0.346 | -0.251 | 110 | -0.559 | -0.450 | 110 | +0.002 | +0.111 |
| ETHUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 205 | -0.119 | -0.122 | 205 | +0.513 | +0.115 | 144 | +0.137 | +0.102 | 144 | +0.673 | +0.059 | 61 | -0.549 | -0.499 | 61 | +0.280 | +0.274 |
| ETHUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 154 | -0.361 | -0.156 | 154 | -1.079 | -0.480 | 105 | -0.324 | -0.098 | 105 | -1.101 | -0.296 | 49 | -0.669 | -0.500 | 49 | -0.988 | -0.764 |
| ETHUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 294 | -0.255 | -0.155 | 294 | -0.022 | +0.079 | 204 | -0.089 | +0.006 | 204 | +0.146 | +0.242 | 90 | -0.525 | -0.415 | 90 | -0.773 | -0.663 |
| ETHUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 171 | -0.011 | -0.014 | 171 | +0.720 | +0.322 | 121 | +0.364 | +0.330 | 121 | +0.918 | +0.304 | 50 | -0.542 | -0.492 | 50 | +0.392 | +0.386 |
| ETHUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 123 | -0.336 | -0.132 | 123 | -1.100 | -0.501 | 83 | -0.380 | -0.155 | 83 | -1.041 | -0.237 | 40 | -0.264 | -0.096 | 40 | -1.970 | -1.746 |
| ETHUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 324 | -0.360 | -0.259 | 323 | -0.253 | -0.152 | 224 | -0.126 | -0.030 | 224 | -0.161 | -0.066 | 100 | -0.805 | -0.696 | 99 | -0.619 | -0.510 |
| ETHUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 180 | -0.466 | -0.469 | 179 | +0.629 | +0.231 | 124 | -0.407 | -0.441 | 124 | +0.775 | +0.162 | 56 | -0.740 | -0.690 | 55 | -1.141 | -1.147 |
| ETHUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 144 | -0.122 | +0.083 | 144 | -0.792 | -0.193 | 100 | +0.217 | +0.443 | 100 | -0.849 | -0.045 | 44 | -0.797 | -0.628 | 44 | -0.301 | -0.076 |
| ETHUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 267 | -0.445 | -0.344 | 266 | -0.221 | -0.121 | 188 | -0.353 | -0.257 | 188 | +0.002 | +0.098 | 79 | -0.834 | -0.724 | 78 | -0.965 | -0.856 |
| ETHUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 151 | -0.488 | -0.491 | 150 | +0.266 | -0.132 | 110 | -0.423 | -0.457 | 110 | +0.743 | +0.129 | 41 | -0.842 | -0.792 | 40 | -1.157 | -1.163 |
| ETHUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 116 | -0.385 | -0.180 | 116 | -0.697 | -0.098 | 78 | -0.142 | +0.083 | 78 | -0.695 | +0.110 | 38 | -0.820 | -0.651 | 38 | -0.709 | -0.485 |
| ETHUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 272 | -0.123 | -0.022 | 272 | +0.209 | +0.310 | 181 | +0.022 | +0.118 | 181 | +0.147 | +0.243 | 91 | -0.634 | -0.525 | 91 | +0.230 | +0.340 |
| ETHUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 150 | -0.287 | -0.290 | 150 | +0.520 | +0.122 | 94 | -0.064 | -0.098 | 94 | +0.859 | +0.245 | 56 | -0.677 | -0.628 | 56 | +0.132 | +0.126 |
| ETHUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 122 | +0.096 | +0.301 | 122 | -0.005 | +0.594 | 87 | +0.226 | +0.451 | 87 | -0.099 | +0.706 | 35 | -0.478 | -0.309 | 35 | +0.608 | +0.832 |
| ETHUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 232 | -0.123 | -0.022 | 232 | +0.126 | +0.226 | 156 | -0.043 | +0.052 | 156 | +0.002 | +0.098 | 76 | -0.544 | -0.434 | 76 | +0.259 | +0.368 |
| ETHUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 129 | -0.271 | -0.274 | 129 | +0.295 | -0.103 | 83 | -0.158 | -0.193 | 83 | +0.752 | +0.138 | 46 | -0.471 | -0.421 | 46 | +0.198 | +0.192 |
| ETHUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 103 | +0.065 | +0.269 | 103 | -0.099 | +0.500 | 73 | +0.229 | +0.455 | 73 | -0.206 | +0.598 | 30 | -0.647 | -0.478 | 30 | +0.513 | +0.737 |
| ETHUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 269 | -0.365 | -0.264 | 268 | -0.207 | -0.107 | 188 | -0.317 | -0.221 | 188 | -0.417 | -0.321 | 81 | -0.507 | -0.398 | 80 | +0.259 | +0.368 |
| ETHUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 159 | -0.312 | -0.315 | 158 | +0.518 | +0.120 | 111 | -0.304 | -0.339 | 111 | +0.560 | -0.054 | 48 | -0.273 | -0.223 | 47 | +0.478 | +0.472 |
| ETHUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 110 | -0.535 | -0.330 | 110 | -0.910 | -0.311 | 77 | -0.348 | -0.122 | 77 | -1.123 | -0.318 | 33 | -0.755 | -0.586 | 33 | -0.232 | -0.008 |
| ETHUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 254 | -0.294 | -0.194 | 253 | -0.229 | -0.128 | 178 | -0.216 | -0.120 | 178 | -0.311 | -0.216 | 76 | -0.558 | -0.448 | 75 | -0.107 | +0.002 |
| ETHUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 146 | -0.160 | -0.163 | 145 | +0.546 | +0.148 | 106 | -0.216 | -0.251 | 106 | +0.587 | -0.026 | 40 | +0.030 | +0.079 | 39 | +0.485 | +0.479 |
| ETHUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 108 | -0.442 | -0.238 | 108 | -0.907 | -0.308 | 72 | -0.221 | +0.004 | 72 | -1.040 | -0.236 | 36 | -0.882 | -0.713 | 36 | -0.407 | -0.182 |
| ETHUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 430 | -0.242 | -0.141 | 430 | +0.050 | +0.150 | 287 | -0.341 | -0.245 | 287 | +0.208 | +0.304 | 143 | -0.041 | +0.069 | 143 | -0.356 | -0.247 |
| ETHUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 211 | -0.079 | -0.082 | 211 | +1.007 | +0.609 | 136 | -0.060 | -0.094 | 136 | +1.838 | +1.225 | 75 | -0.304 | -0.254 | 75 | -0.048 | -0.054 |
| ETHUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 219 | -0.363 | -0.159 | 219 | -1.156 | -0.557 | 151 | -0.658 | -0.433 | 151 | -1.330 | -0.526 | 68 | +0.038 | +0.206 | 68 | -0.621 | -0.397 |
| ETHUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 95 | +0.427 | +0.475 | 94 | +0.432 | +0.480 | 63 | +0.094 | +0.140 | 63 | +0.397 | +0.443 | 32 | +0.739 | +0.790 | 31 | +0.466 | +0.518 |
| ETHUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 50 | +0.811 | +0.659 | 50 | -0.289 | -0.629 | 37 | +0.841 | +0.610 | 37 | -0.269 | -1.087 | 13 | +0.727 | +0.717 | 13 | -0.303 | +0.098 |
| ETHUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 45 | +0.094 | +0.343 | 44 | +1.211 | +1.647 | 26 | -0.246 | +0.077 | 26 | +1.028 | +1.938 | 19 | +0.751 | +0.865 | 18 | +1.306 | +1.008 |
| ETHUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 79 | +0.753 | +0.802 | 78 | +0.872 | +0.920 | 52 | +0.457 | +0.502 | 52 | +0.786 | +0.832 | 27 | +1.084 | +1.136 | 26 | +1.055 | +1.106 |
| ETHUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 42 | +0.874 | +0.722 | 42 | +0.556 | +0.216 | 30 | +0.881 | +0.650 | 30 | +0.850 | +0.031 | 12 | +0.999 | +0.989 | 12 | +0.083 | +0.484 |
| ETHUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 37 | +0.517 | +0.765 | 36 | +1.211 | +1.647 | 22 | -0.059 | +0.263 | 22 | +0.663 | +1.573 | 15 | +1.083 | +1.196 | 14 | +1.702 | +1.403 |
| ETHUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 80 | +0.357 | +0.405 | 78 | +0.854 | +0.902 | 51 | +0.301 | +0.347 | 51 | +0.397 | +0.442 | 29 | +0.997 | +1.049 | 27 | +0.909 | +0.960 |
| ETHUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 42 | +0.061 | -0.091 | 41 | -1.353 | -1.693 | 31 | +0.053 | -0.178 | 31 | -0.276 | -1.095 | 11 | +0.070 | +0.060 | 10 | -2.085 | -1.684 |
| ETHUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 38 | +0.947 | +1.195 | 37 | +1.027 | +1.463 | 20 | +0.309 | +0.632 | 20 | +0.654 | +1.564 | 18 | +1.263 | +1.376 | 17 | +1.310 | +1.012 |
| ETHUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 73 | +0.322 | +0.370 | 71 | +0.911 | +0.959 | 47 | +0.301 | +0.347 | 47 | +0.917 | +0.963 | 26 | +0.865 | +0.917 | 24 | +0.854 | +0.905 |
| ETHUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 38 | +0.061 | -0.091 | 37 | -1.353 | -1.693 | 28 | +0.016 | -0.215 | 28 | -0.001 | -0.820 | 10 | +0.404 | +0.393 | 9 | -1.873 | -1.472 |
| ETHUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 35 | +0.917 | +1.166 | 34 | +0.972 | +1.408 | 19 | +0.323 | +0.646 | 19 | +0.917 | +1.827 | 16 | +1.122 | +1.235 | 15 | +1.029 | +0.731 |
| ETHUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 64 | -0.142 | -0.093 | 64 | -0.139 | -0.091 | 44 | -0.171 | -0.125 | 44 | +0.374 | +0.420 | 20 | -0.146 | -0.095 | 20 | -1.225 | -1.174 |
| ETHUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 34 | -0.316 | -0.468 | 34 | -0.217 | -0.557 | 26 | -0.168 | -0.399 | 26 | +0.377 | -0.442 | 8 | -0.322 | -0.332 | 8 | -2.573 | -2.172 |
| ETHUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 30 | +0.206 | +0.455 | 30 | +0.171 | +0.607 | 18 | -0.273 | +0.050 | 18 | +0.065 | +0.975 | 12 | +0.279 | +0.393 | 12 | +0.168 | -0.130 |
| ETHUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 58 | -0.099 | -0.051 | 58 | +0.680 | +0.728 | 41 | +0.048 | +0.093 | 41 | +1.054 | +1.100 | 17 | -0.134 | -0.083 | 17 | -0.564 | -0.513 |
| ETHUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 30 | -0.200 | -0.352 | 30 | +0.904 | +0.564 | 23 | +0.051 | -0.180 | 23 | +1.355 | +0.537 | 7 | -0.252 | -0.262 | 7 | -1.880 | -1.479 |
| ETHUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 28 | +0.206 | +0.455 | 28 | +0.171 | +0.607 | 18 | -0.273 | +0.050 | 18 | +0.065 | +0.975 | 10 | +0.277 | +0.391 | 10 | +0.166 | -0.132 |
| ETHUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 63 | -0.676 | -0.628 | 62 | +0.517 | +0.565 | 47 | -0.365 | -0.319 | 47 | +0.518 | +0.564 | 16 | -0.975 | -0.923 | 15 | +0.858 | +0.910 |
| ETHUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 33 | +0.485 | +0.333 | 33 | +0.437 | +0.097 | 26 | +0.509 | +0.278 | 26 | +0.483 | -0.336 | 7 | -0.676 | -0.687 | 7 | +0.101 | +0.502 |
| ETHUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 30 | -1.338 | -1.090 | 29 | +0.515 | +0.951 | 21 | -1.360 | -1.037 | 21 | +0.514 | +1.425 | 9 | -1.070 | -0.956 | 8 | +1.659 | +1.361 |
| ETHUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 56 | -0.409 | -0.360 | 55 | +0.512 | +0.560 | 41 | -0.449 | -0.403 | 41 | +0.519 | +0.565 | 15 | +0.043 | +0.095 | 14 | +0.243 | +0.294 |
| ETHUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 32 | +0.353 | +0.201 | 32 | +0.379 | +0.039 | 25 | +0.221 | -0.010 | 25 | +0.529 | -0.290 | 7 | +1.213 | +1.203 | 7 | +0.101 | +0.502 |
| ETHUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 24 | -1.193 | -0.945 | 23 | +0.509 | +0.946 | 16 | -1.471 | -1.149 | 16 | +0.518 | +1.429 | 8 | -0.286 | -0.172 | 7 | +0.381 | +0.083 |
| ETHUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 113 | -0.274 | -0.226 | 113 | +0.030 | +0.078 | 77 | -0.141 | -0.096 | 77 | +0.029 | +0.075 | 36 | -0.312 | -0.260 | 36 | -0.046 | +0.005 |
| ETHUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 42 | +0.288 | +0.136 | 42 | -0.088 | -0.428 | 25 | +0.869 | +0.638 | 25 | -0.209 | -1.028 | 17 | -0.376 | -0.387 | 17 | +0.063 | +0.464 |
| ETHUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 71 | -0.458 | -0.210 | 71 | +0.206 | +0.642 | 52 | -0.535 | -0.213 | 52 | +0.285 | +1.195 | 19 | +1.187 | +1.300 | 19 | -0.154 | -0.453 |
| ETHUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | both | 28 | +0.350 | +0.377 | 28 | +3.505 | +3.531 | 19 | +0.522 | +0.547 | 19 | +4.305 | +4.330 | 9 | +0.186 | +0.214 | 9 | +2.089 | +2.116 |
| ETHUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | long | 18 | +0.342 | +0.135 | 18 | +4.856 | +3.254 | 16 | +0.346 | -0.001 | 16 | +4.860 | +2.563 | 2 | -0.015 | +0.022 | 2 | +10.961 | +11.367 |
| ETHUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | short | 10 | +0.844 | +1.104 | 10 | +0.177 | +1.832 | 3 | +3.179 | +3.576 | 3 | +4.281 | +6.627 | 7 | +0.186 | +0.204 | 7 | -3.003 | -3.354 |
| ETHUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 24 | +0.606 | +0.633 | 24 | +2.933 | +2.959 | 15 | +0.707 | +0.732 | 15 | +3.656 | +3.681 | 9 | +0.186 | +0.214 | 9 | +2.089 | +2.116 |
| ETHUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 15 | +0.522 | +0.315 | 15 | +3.653 | +2.052 | 13 | +0.524 | +0.177 | 13 | +3.656 | +1.359 | 2 | -0.015 | +0.022 | 2 | +10.961 | +11.367 |
| ETHUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 9 | +1.508 | +1.768 | 9 | -3.003 | -1.349 | 2 | +5.984 | +6.381 | 2 | -2.509 | -0.162 | 7 | +0.186 | +0.204 | 7 | -3.003 | -3.354 |
| ETHUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | both | 23 | +1.253 | +1.280 | 23 | +3.915 | +3.941 | 15 | +1.342 | +1.367 | 15 | +6.056 | +6.081 | 8 | +1.249 | +1.277 | 8 | +0.563 | +0.591 |
| ETHUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | long | 15 | +1.253 | +1.046 | 15 | +6.056 | +4.454 | 12 | +1.288 | +0.940 | 12 | +7.155 | +4.858 | 3 | +1.246 | +1.283 | 3 | -2.787 | -2.382 |
| ETHUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | short | 8 | +0.762 | +1.022 | 8 | +0.545 | +2.200 | 3 | +1.313 | +1.711 | 3 | -2.849 | -0.502 | 5 | +0.188 | +0.207 | 5 | +3.917 | +3.567 |
| ETHUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 19 | +1.253 | +1.280 | 19 | +3.915 | +3.942 | 13 | +0.788 | +0.813 | 13 | +1.304 | +1.329 | 6 | +1.384 | +1.412 | 6 | +4.357 | +4.384 |
| ETHUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 13 | +1.253 | +1.046 | 13 | +6.056 | +4.454 | 11 | +0.788 | +0.441 | 11 | +6.063 | +3.766 | 2 | +2.085 | +2.122 | 2 | +3.812 | +4.217 |
| ETHUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 6 | +0.855 | +1.115 | 6 | +0.545 | +2.200 | 2 | +1.452 | +1.849 | 2 | -7.175 | -4.828 | 4 | +0.855 | +0.874 | 4 | +4.361 | +4.011 |
| ETHUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | both | 16 | +0.522 | +0.549 | 16 | +2.431 | +2.457 | 10 | +1.033 | +1.058 | 10 | +2.434 | +2.459 | 6 | -0.189 | -0.161 | 6 | -1.783 | -1.755 |
| ETHUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | long | 9 | +1.075 | +0.867 | 9 | +2.223 | +0.621 | 8 | +1.245 | +0.898 | 8 | +2.434 | +0.138 | 1 | -0.579 | -0.541 | 1 | -7.953 | -7.547 |
| ETHUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | short | 7 | -0.082 | +0.178 | 7 | +4.388 | +6.042 | 2 | -0.315 | +0.082 | 2 | +2.756 | +5.103 | 5 | +0.053 | +0.072 | 5 | +4.388 | +4.037 |
| ETHUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 12 | +1.242 | +1.268 | 12 | +0.431 | +0.457 | 9 | +1.076 | +1.101 | 9 | +2.224 | +2.249 | 3 | +1.819 | +1.847 | 3 | -7.960 | -7.932 |
| ETHUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 9 | +1.075 | +0.867 | 9 | +2.223 | +0.621 | 8 | +1.245 | +0.898 | 8 | +2.434 | +0.138 | 1 | -0.579 | -0.541 | 1 | -7.953 | -7.547 |
| ETHUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 3 | +1.819 | +2.079 | 3 | -2.334 | -0.680 | 1 | -0.056 | +0.341 | 1 | -2.300 | +0.047 | 2 | +3.249 | +3.268 | 2 | -1.214 | -1.565 |
| ETHUSDT | 12h | calibrated | BRK_mem_first | record | ALL | both | 22 | +0.538 | +0.565 | 22 | +0.349 | +0.375 | 13 | +1.567 | +1.592 | 13 | +0.600 | +0.625 | 9 | +0.108 | +0.136 | 9 | -2.168 | -2.141 |
| ETHUSDT | 12h | calibrated | BRK_mem_first | record | ALL | long | 13 | +0.646 | +0.439 | 13 | +5.862 | +4.260 | 10 | +1.015 | +0.667 | 10 | +6.082 | +3.785 | 3 | +0.646 | +0.683 | 3 | -3.152 | -2.746 |
| ETHUSDT | 12h | calibrated | BRK_mem_first | record | ALL | short | 9 | +0.108 | +0.368 | 9 | -2.168 | -0.514 | 3 | +1.557 | +1.954 | 3 | -3.125 | -0.778 | 6 | +0.059 | +0.078 | 6 | -0.676 | -1.027 |
| ETHUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 28 | +0.493 | +0.519 | 28 | -0.127 | -0.100 | 15 | +0.551 | +0.576 | 15 | +0.092 | +0.117 | 13 | +0.109 | +0.137 | 13 | -2.167 | -2.140 |
| ETHUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 15 | +0.652 | +0.445 | 15 | +1.944 | +0.342 | 10 | +1.080 | +0.733 | 10 | +6.085 | +3.788 | 5 | +0.653 | +0.690 | 5 | -3.591 | -3.185 |
| ETHUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 13 | +0.009 | +0.269 | 13 | -2.168 | -0.514 | 5 | -1.890 | -1.493 | 5 | -3.117 | -0.771 | 8 | +0.059 | +0.078 | 8 | -0.676 | -1.027 |
| ETHUSDT | 12h | calibrated | SFP_harden | record | ALL | both | 57 | +0.067 | +0.093 | 57 | +0.748 | +0.775 | 37 | -0.023 | +0.002 | 37 | +0.642 | +0.667 | 20 | +0.254 | +0.282 | 20 | +1.628 | +1.656 |
| ETHUSDT | 12h | calibrated | SFP_harden | record | ALL | long | 29 | +0.166 | -0.042 | 29 | +1.980 | +0.378 | 18 | +0.201 | -0.147 | 18 | +1.360 | -0.937 | 11 | +0.022 | +0.059 | 11 | +2.457 | +2.863 |
| ETHUSDT | 12h | calibrated | SFP_harden | record | ALL | short | 28 | -0.038 | +0.222 | 28 | -0.739 | +0.915 | 19 | -0.693 | -0.296 | 19 | -1.719 | +0.628 | 9 | +0.437 | +0.456 | 9 | +0.528 | +0.178 |
| ETHUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 15 | -0.523 | -0.505 | 13 | -4.535 | -4.517 | 8 | +0.166 | +0.183 | 8 | -0.195 | -0.178 | 7 | -0.710 | -0.691 | 5 | -5.839 | -5.820 |
| ETHUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 9 | +0.094 | -0.029 | 8 | -3.351 | -4.906 | 6 | +0.166 | -0.181 | 6 | -0.195 | -2.685 | 3 | -0.685 | -0.508 | 2 | -5.817 | -3.594 |
| ETHUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 6 | -1.023 | -0.863 | 5 | -5.838 | -4.247 | 2 | -0.273 | +0.108 | 2 | -2.906 | -0.381 | 4 | -1.623 | -1.763 | 3 | -5.839 | -8.024 |
| ETHUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 14 | -0.381 | -0.363 | 12 | -3.353 | -3.335 | 8 | +0.166 | +0.183 | 8 | -0.195 | -0.178 | 6 | -0.699 | -0.680 | 4 | -5.253 | -5.234 |
| ETHUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 9 | +0.094 | -0.029 | 8 | -3.351 | -4.906 | 6 | +0.166 | -0.181 | 6 | -0.195 | -2.685 | 3 | -0.685 | -0.508 | 2 | -5.817 | -3.594 |
| ETHUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 5 | -0.708 | -0.548 | 4 | -1.580 | +0.010 | 2 | -0.273 | +0.108 | 2 | -2.906 | -0.381 | 3 | -0.713 | -0.852 | 2 | -0.992 | -3.177 |
| ETHUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 12 | -0.612 | -0.594 | 12 | -3.572 | -3.555 | 7 | +0.100 | +0.118 | 7 | +0.370 | +0.388 | 5 | -1.276 | -1.257 | 5 | -6.969 | -6.950 |
| ETHUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 8 | -0.390 | -0.514 | 8 | -3.570 | -5.125 | 6 | -0.001 | -0.348 | 6 | -1.120 | -3.610 | 2 | -0.977 | -0.799 | 2 | -5.860 | -3.637 |
| ETHUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 4 | -3.553 | -3.393 | 4 | -1.915 | -0.325 | 1 | +3.460 | +3.841 | 1 | +7.441 | +9.966 | 3 | -6.560 | -6.699 | 3 | -7.513 | -9.698 |
| ETHUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 11 | -0.545 | -0.527 | 11 | -2.612 | -2.595 | 7 | +0.100 | +0.118 | 7 | +0.370 | +0.388 | 4 | -0.980 | -0.961 | 4 | -5.863 | -5.845 |
| ETHUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 8 | -0.390 | -0.514 | 8 | -3.570 | -5.125 | 6 | -0.001 | -0.348 | 6 | -1.120 | -3.610 | 2 | -0.977 | -0.799 | 2 | -5.860 | -3.637 |
| ETHUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 3 | -0.550 | -0.391 | 3 | +3.678 | +5.268 | 1 | +3.460 | +3.841 | 1 | +7.441 | +9.966 | 2 | -3.775 | -3.914 | 2 | -1.919 | -4.105 |
| ETHUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 9 | -1.903 | -1.885 | 9 | -4.758 | -4.740 | 5 | -1.723 | -1.705 | 5 | -2.619 | -2.602 | 4 | -2.591 | -2.572 | 4 | -6.297 | -6.279 |
| ETHUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 8 | -1.813 | -1.936 | 8 | -4.586 | -6.140 | 5 | -1.723 | -2.069 | 5 | -2.619 | -5.109 | 3 | -2.430 | -2.253 | 3 | -4.754 | -2.532 |
| ETHUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 1 | -7.447 | -7.288 | 1 | -14.744 | -13.154 | 0 | — | — | 0 | — | — | 1 | -7.447 | -7.587 | 1 | -14.744 | -16.930 |
| ETHUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 6 | -1.499 | -1.481 | 6 | -3.686 | -3.668 | 4 | -0.816 | -0.799 | 4 | -0.424 | -0.406 | 2 | -2.014 | -1.995 | 2 | -6.297 | -6.278 |
| ETHUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 6 | -1.499 | -1.623 | 6 | -3.686 | -5.241 | 4 | -0.816 | -1.162 | 4 | -0.424 | -2.914 | 2 | -2.014 | -1.837 | 2 | -6.297 | -4.074 |
| ETHUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| ETHUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 12 | +0.852 | +0.870 | 11 | -0.466 | -0.448 | 6 | +1.174 | +1.191 | 6 | +1.987 | +2.005 | 6 | +0.584 | +0.603 | 5 | -6.711 | -6.693 |
| ETHUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 8 | +1.172 | +1.049 | 7 | +1.919 | +0.364 | 5 | +1.407 | +1.061 | 5 | +2.052 | -0.438 | 3 | -0.320 | -0.143 | 2 | -2.734 | -0.511 |
| ETHUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 4 | +0.584 | +0.744 | 4 | -7.221 | -5.631 | 1 | -0.516 | -0.135 | 1 | -3.610 | -1.085 | 3 | +0.763 | +0.624 | 3 | -7.731 | -9.916 |
| ETHUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 12 | +0.852 | +0.870 | 11 | -0.466 | -0.448 | 6 | +1.174 | +1.191 | 6 | +1.987 | +2.005 | 6 | +0.584 | +0.603 | 5 | -6.711 | -6.693 |
| ETHUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 8 | +1.172 | +1.049 | 7 | +1.919 | +0.364 | 5 | +1.407 | +1.061 | 5 | +2.052 | -0.438 | 3 | -0.320 | -0.143 | 2 | -2.734 | -0.511 |
| ETHUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 4 | +0.584 | +0.744 | 4 | -7.221 | -5.631 | 1 | -0.516 | -0.135 | 1 | -3.610 | -1.085 | 3 | +0.763 | +0.624 | 3 | -7.731 | -9.916 |
| ETHUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 22 | -0.642 | -0.624 | 20 | -1.057 | -1.039 | 12 | -0.914 | -0.896 | 12 | +1.546 | +1.564 | 10 | -0.124 | -0.105 | 8 | -3.386 | -3.367 |
| ETHUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 12 | +0.236 | +0.112 | 11 | +0.908 | -0.647 | 5 | +1.324 | +0.978 | 5 | +2.785 | +0.295 | 7 | -0.010 | +0.167 | 6 | -4.160 | -1.937 |
| ETHUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 10 | -1.278 | -1.118 | 9 | -3.447 | -1.857 | 7 | -1.878 | -1.497 | 7 | -29.835 | -27.311 | 3 | -0.239 | -0.378 | 2 | +3.980 | +1.794 |
| SOLUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 346 | +0.126 | +0.196 | 345 | +0.165 | +0.236 | 207 | +0.495 | +0.554 | 207 | +0.715 | +0.774 | 139 | -0.221 | -0.130 | 138 | -0.901 | -0.810 |
| SOLUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 178 | +0.136 | +0.223 | 178 | +0.047 | +0.033 | 111 | +0.549 | +0.638 | 111 | +0.854 | +0.800 | 67 | -0.221 | -0.139 | 67 | -1.922 | -1.866 |
| SOLUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 168 | +0.066 | +0.120 | 167 | +0.188 | +0.342 | 96 | +0.409 | +0.439 | 96 | +0.278 | +0.450 | 72 | -0.217 | -0.117 | 71 | +0.171 | +0.297 |
| SOLUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 304 | +0.147 | +0.217 | 303 | +0.430 | +0.501 | 181 | +0.607 | +0.666 | 181 | +0.812 | +0.872 | 123 | -0.221 | -0.130 | 122 | -0.901 | -0.810 |
| SOLUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 163 | +0.249 | +0.336 | 163 | +0.594 | +0.581 | 102 | +0.694 | +0.783 | 102 | +0.891 | +0.838 | 61 | -0.220 | -0.138 | 61 | -1.769 | -1.713 |
| SOLUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 141 | +0.044 | +0.098 | 140 | +0.278 | +0.432 | 79 | +0.446 | +0.476 | 79 | +0.639 | +0.810 | 62 | -0.247 | -0.148 | 61 | +0.120 | +0.246 |
| SOLUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 305 | -0.210 | -0.140 | 305 | -0.260 | -0.189 | 180 | +0.025 | +0.084 | 180 | +0.246 | +0.305 | 125 | -0.338 | -0.247 | 125 | -0.539 | -0.448 |
| SOLUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 157 | -0.148 | -0.061 | 157 | -0.446 | -0.459 | 96 | +0.259 | +0.348 | 96 | +0.793 | +0.740 | 61 | -0.575 | -0.493 | 61 | -1.396 | -1.341 |
| SOLUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 148 | -0.242 | -0.188 | 148 | +0.111 | +0.265 | 84 | -0.313 | -0.284 | 84 | -0.311 | -0.140 | 64 | -0.174 | -0.075 | 64 | +0.380 | +0.506 |
| SOLUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 275 | -0.207 | -0.137 | 275 | -0.262 | -0.192 | 165 | +0.040 | +0.099 | 165 | +0.390 | +0.449 | 110 | -0.396 | -0.305 | 110 | -0.642 | -0.551 |
| SOLUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 142 | -0.134 | -0.047 | 142 | -0.344 | -0.358 | 88 | +0.303 | +0.392 | 88 | +0.844 | +0.791 | 54 | -0.660 | -0.577 | 54 | -1.417 | -1.361 |
| SOLUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 133 | -0.239 | -0.185 | 133 | +0.088 | +0.242 | 77 | -0.305 | -0.276 | 77 | -1.040 | -0.869 | 56 | -0.028 | +0.072 | 56 | +0.305 | +0.431 |
| SOLUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 237 | -0.111 | -0.040 | 237 | -0.451 | -0.381 | 136 | +0.222 | +0.281 | 136 | +0.166 | +0.226 | 101 | -0.452 | -0.361 | 101 | -0.551 | -0.461 |
| SOLUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 118 | -0.161 | -0.074 | 118 | -0.463 | -0.477 | 70 | +0.059 | +0.148 | 70 | +0.599 | +0.546 | 48 | -0.545 | -0.462 | 48 | -0.683 | -0.628 |
| SOLUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 119 | +0.110 | +0.163 | 119 | -0.376 | -0.222 | 66 | +0.689 | +0.719 | 66 | -0.330 | -0.158 | 53 | -0.193 | -0.093 | 53 | -0.393 | -0.267 |
| SOLUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 210 | -0.082 | -0.012 | 210 | -0.482 | -0.412 | 121 | +0.211 | +0.270 | 121 | +0.517 | +0.576 | 89 | -0.453 | -0.362 | 89 | -0.774 | -0.683 |
| SOLUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 101 | -0.345 | -0.259 | 101 | -0.481 | -0.494 | 60 | -0.156 | -0.067 | 60 | +0.599 | +0.546 | 41 | -0.638 | -0.556 | 41 | -0.816 | -0.761 |
| SOLUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 109 | +0.182 | +0.236 | 109 | -0.482 | -0.328 | 61 | +0.751 | +0.781 | 61 | -0.471 | -0.299 | 48 | -0.099 | +0.001 | 48 | -0.585 | -0.460 |
| SOLUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 280 | -0.066 | +0.004 | 280 | -0.311 | -0.241 | 169 | +0.201 | +0.260 | 169 | +0.099 | +0.158 | 111 | -0.348 | -0.257 | 111 | -1.098 | -1.008 |
| SOLUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 141 | -0.063 | +0.024 | 141 | -0.444 | -0.458 | 91 | +0.501 | +0.590 | 91 | +0.293 | +0.240 | 50 | -0.675 | -0.593 | 50 | -2.490 | -2.435 |
| SOLUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 139 | -0.069 | -0.015 | 139 | -0.253 | -0.099 | 78 | -0.362 | -0.333 | 78 | -0.433 | -0.261 | 61 | +0.001 | +0.100 | 61 | -0.100 | +0.026 |
| SOLUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 275 | -0.064 | +0.006 | 275 | -0.310 | -0.239 | 164 | +0.042 | +0.101 | 164 | +0.273 | +0.332 | 111 | -0.217 | -0.126 | 111 | -1.095 | -1.004 |
| SOLUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 145 | +0.162 | +0.249 | 145 | -0.260 | -0.273 | 89 | +0.481 | +0.570 | 89 | +0.397 | +0.344 | 56 | -0.412 | -0.329 | 56 | -1.935 | -1.879 |
| SOLUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 130 | -0.297 | -0.243 | 130 | -0.333 | -0.179 | 75 | -0.405 | -0.375 | 75 | -0.559 | -0.388 | 55 | +0.002 | +0.101 | 55 | -0.315 | -0.189 |
| SOLUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 492 | +0.130 | +0.200 | 491 | +0.332 | +0.402 | 316 | +0.087 | +0.146 | 316 | +0.106 | +0.166 | 176 | +0.214 | +0.305 | 175 | +1.037 | +1.128 |
| SOLUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 257 | +0.064 | +0.151 | 257 | +0.092 | +0.079 | 162 | +0.047 | +0.136 | 162 | -0.221 | -0.274 | 95 | +0.094 | +0.176 | 95 | +1.080 | +1.136 |
| SOLUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 235 | +0.219 | +0.273 | 234 | +0.756 | +0.910 | 154 | +0.116 | +0.145 | 154 | +0.628 | +0.800 | 81 | +0.437 | +0.536 | 80 | +0.809 | +0.935 |
| SOLUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 71 | -0.052 | -0.018 | 70 | +0.466 | +0.500 | 49 | +0.071 | +0.098 | 49 | +0.637 | +0.665 | 22 | -0.365 | -0.322 | 21 | +0.377 | +0.421 |
| SOLUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 33 | -0.052 | -0.042 | 32 | -0.393 | -0.486 | 22 | -0.232 | -0.241 | 22 | -0.911 | -1.156 | 11 | -0.063 | -0.022 | 10 | +0.323 | +0.482 |
| SOLUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 38 | -0.145 | -0.087 | 38 | +1.095 | +1.256 | 27 | +0.241 | +0.306 | 27 | +1.284 | +1.585 | 11 | -1.371 | -1.324 | 11 | +0.378 | +0.306 |
| SOLUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 62 | +0.259 | +0.293 | 61 | +0.635 | +0.669 | 45 | +0.302 | +0.330 | 45 | +1.066 | +1.094 | 17 | -0.062 | -0.018 | 16 | +0.209 | +0.252 |
| SOLUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 31 | +0.067 | +0.078 | 30 | -0.042 | -0.136 | 21 | +0.073 | +0.065 | 21 | -0.671 | -0.916 | 10 | +0.101 | +0.141 | 9 | +0.765 | +0.924 |
| SOLUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 31 | +0.300 | +0.358 | 31 | +1.131 | +1.292 | 24 | +0.309 | +0.373 | 24 | +1.401 | +1.702 | 7 | -1.383 | -1.336 | 7 | -5.075 | -5.147 |
| SOLUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 67 | -0.217 | -0.183 | 66 | -0.172 | -0.138 | 47 | -0.514 | -0.486 | 47 | +0.005 | +0.033 | 20 | +0.776 | +0.820 | 19 | -1.324 | -1.280 |
| SOLUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 34 | -0.444 | -0.433 | 33 | -1.257 | -1.351 | 24 | -0.439 | -0.448 | 24 | -1.205 | -1.450 | 10 | -0.447 | -0.407 | 9 | -1.321 | -1.162 |
| SOLUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 33 | +0.505 | +0.563 | 33 | +0.381 | +0.542 | 23 | -0.513 | -0.449 | 23 | +0.504 | +0.804 | 10 | +1.065 | +1.112 | 10 | -0.709 | -0.781 |
| SOLUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 56 | -0.194 | -0.160 | 55 | +0.000 | +0.034 | 40 | -0.230 | -0.202 | 40 | +0.254 | +0.282 | 16 | +0.368 | +0.412 | 15 | -0.060 | -0.016 |
| SOLUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 32 | -0.257 | -0.246 | 31 | -1.158 | -1.251 | 22 | -0.232 | -0.241 | 22 | -0.719 | -0.965 | 10 | -0.447 | -0.407 | 9 | -1.321 | -1.162 |
| SOLUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 24 | +0.566 | +0.624 | 24 | +0.614 | +0.775 | 18 | +0.001 | +0.065 | 18 | +0.617 | +0.918 | 6 | +1.127 | +1.174 | 6 | +2.669 | +2.597 |
| SOLUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 62 | -0.069 | -0.035 | 61 | -0.291 | -0.257 | 38 | -0.241 | -0.213 | 38 | +0.249 | +0.277 | 24 | +1.031 | +1.075 | 23 | -0.950 | -0.907 |
| SOLUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 34 | -0.066 | -0.055 | 33 | -1.757 | -1.850 | 22 | +0.015 | +0.007 | 22 | -1.758 | -2.003 | 12 | -0.098 | -0.058 | 11 | -1.118 | -0.959 |
| SOLUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 28 | -0.124 | -0.067 | 28 | +0.663 | +0.824 | 16 | -1.208 | -1.144 | 16 | +1.004 | +1.305 | 12 | +1.403 | +1.450 | 12 | -0.284 | -0.356 |
| SOLUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 59 | +0.040 | +0.074 | 58 | -0.199 | -0.165 | 36 | -0.241 | -0.213 | 36 | +0.249 | +0.277 | 23 | +1.105 | +1.148 | 22 | -0.728 | -0.684 |
| SOLUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 34 | -0.066 | -0.055 | 33 | -1.757 | -1.850 | 22 | +0.015 | +0.007 | 22 | -1.758 | -2.003 | 12 | -0.098 | -0.058 | 11 | -1.118 | -0.959 |
| SOLUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 25 | +0.323 | +0.381 | 25 | +1.273 | +1.434 | 14 | -1.208 | -1.144 | 14 | +1.997 | +2.298 | 11 | +1.457 | +1.504 | 11 | -0.064 | -0.136 |
| SOLUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 57 | -0.123 | -0.089 | 57 | +0.869 | +0.903 | 40 | -0.047 | -0.019 | 40 | +0.245 | +0.272 | 17 | -0.529 | -0.485 | 17 | +2.234 | +2.277 |
| SOLUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 24 | +0.565 | +0.575 | 24 | +2.638 | +2.545 | 17 | +1.005 | +0.996 | 17 | +4.095 | +3.850 | 7 | -0.946 | -0.906 | 7 | +0.852 | +1.011 |
| SOLUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 33 | -0.271 | -0.214 | 33 | +0.656 | +0.817 | 23 | -0.463 | -0.398 | 23 | -0.356 | -0.055 | 10 | -0.031 | +0.016 | 10 | +3.362 | +3.290 |
| SOLUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 53 | -0.098 | -0.064 | 53 | -0.170 | -0.136 | 36 | -0.046 | -0.019 | 36 | -0.327 | -0.300 | 17 | -0.529 | -0.485 | 17 | +2.234 | +2.277 |
| SOLUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 25 | +0.426 | +0.436 | 25 | +3.064 | +2.971 | 16 | +1.438 | +1.429 | 16 | +5.101 | +4.855 | 9 | -0.834 | -0.794 | 9 | +0.332 | +0.491 |
| SOLUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 28 | -0.774 | -0.717 | 28 | -0.329 | -0.168 | 20 | -1.127 | -1.063 | 20 | -0.507 | -0.206 | 8 | +0.076 | +0.123 | 8 | +3.362 | +3.290 |
| SOLUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 104 | +0.530 | +0.564 | 103 | +0.724 | +0.758 | 58 | -0.010 | +0.017 | 58 | -1.162 | -1.134 | 46 | +1.073 | +1.116 | 45 | +2.348 | +2.391 |
| SOLUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 63 | +0.266 | +0.277 | 62 | -0.477 | -0.570 | 36 | -0.105 | -0.114 | 36 | -1.703 | -1.948 | 27 | +0.541 | +0.582 | 26 | +2.127 | +2.286 |
| SOLUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 41 | +0.690 | +0.748 | 41 | +1.221 | +1.382 | 22 | +0.270 | +0.334 | 22 | +0.580 | +0.880 | 19 | +2.333 | +2.380 | 19 | +3.848 | +3.776 |
| SOLUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | both | 27 | -1.024 | -1.005 | 27 | +0.517 | +0.535 | 17 | +0.425 | +0.440 | 17 | +0.262 | +0.277 | 10 | -1.326 | -1.302 | 10 | +1.339 | +1.363 |
| SOLUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | long | 16 | +0.386 | +0.356 | 16 | +1.533 | +1.288 | 11 | +1.530 | +1.481 | 11 | +0.519 | -0.115 | 5 | -2.546 | -2.540 | 5 | +1.736 | +1.964 |
| SOLUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | short | 11 | -1.202 | -1.134 | 11 | -2.739 | -2.457 | 6 | -0.542 | -0.462 | 6 | -1.974 | -1.308 | 5 | -1.293 | -1.252 | 5 | -3.588 | -3.769 |
| SOLUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 22 | -0.337 | -0.319 | 22 | +0.389 | +0.407 | 15 | +0.466 | +0.481 | 15 | +0.262 | +0.278 | 7 | -1.293 | -1.270 | 7 | +1.314 | +1.338 |
| SOLUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 12 | +0.977 | +0.947 | 12 | +2.135 | +1.891 | 10 | +1.553 | +1.505 | 10 | +1.733 | +1.099 | 2 | -1.101 | -1.095 | 2 | +5.923 | +6.151 |
| SOLUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 10 | -1.246 | -1.178 | 10 | -3.162 | -2.880 | 5 | -0.060 | +0.019 | 5 | -2.737 | -2.072 | 5 | -1.293 | -1.252 | 5 | -3.588 | -3.769 |
| SOLUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | both | 25 | -0.636 | -0.618 | 25 | -1.023 | -1.005 | 16 | -0.641 | -0.625 | 16 | -1.115 | -1.099 | 9 | -0.644 | -0.621 | 9 | +1.314 | +1.338 |
| SOLUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | long | 14 | -0.361 | -0.392 | 14 | +0.150 | -0.095 | 9 | -0.613 | -0.661 | 9 | -1.021 | -1.656 | 5 | +2.112 | +2.118 | 5 | +1.316 | +1.543 |
| SOLUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | short | 11 | -1.289 | -1.221 | 11 | -1.214 | -0.932 | 7 | -0.669 | -0.589 | 7 | -1.209 | -0.543 | 4 | -1.584 | -1.543 | 4 | +1.422 | +1.241 |
| SOLUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 23 | -0.636 | -0.618 | 23 | +1.044 | +1.062 | 15 | -0.613 | -0.597 | 15 | -1.208 | -1.193 | 8 | -0.970 | -0.946 | 8 | +4.433 | +4.456 |
| SOLUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 12 | -0.361 | -0.392 | 12 | +1.357 | +1.112 | 8 | -0.359 | -0.408 | 8 | +0.091 | -0.543 | 4 | +1.806 | +1.812 | 4 | +4.588 | +4.816 |
| SOLUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 11 | -1.289 | -1.221 | 11 | -1.214 | -0.932 | 7 | -0.669 | -0.589 | 7 | -1.209 | -0.543 | 4 | -1.584 | -1.543 | 4 | +1.422 | +1.241 |
| SOLUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | both | 21 | -0.078 | -0.059 | 21 | +0.517 | +0.535 | 13 | -0.504 | -0.488 | 13 | -1.209 | -1.194 | 8 | +0.624 | +0.648 | 8 | +0.800 | +0.824 |
| SOLUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | long | 14 | -0.771 | -0.801 | 14 | +0.763 | +0.518 | 8 | -1.199 | -1.247 | 8 | -0.346 | -0.980 | 6 | +1.119 | +1.125 | 6 | +1.216 | +1.444 |
| SOLUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | short | 7 | +0.298 | +0.366 | 7 | -1.213 | -0.931 | 5 | +0.300 | +0.380 | 5 | -1.210 | -0.545 | 2 | -0.564 | -0.522 | 2 | -2.258 | -2.439 |
| SOLUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 20 | -0.292 | -0.274 | 20 | -0.348 | -0.329 | 13 | -0.504 | -0.488 | 13 | -1.209 | -1.194 | 7 | -0.084 | -0.060 | 7 | +0.596 | +0.620 |
| SOLUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 13 | -1.037 | -1.068 | 13 | +0.517 | +0.272 | 8 | -1.199 | -1.247 | 8 | -0.346 | -0.980 | 5 | -0.083 | -0.076 | 5 | +1.426 | +1.654 |
| SOLUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 7 | +0.298 | +0.366 | 7 | -1.213 | -0.931 | 5 | +0.300 | +0.380 | 5 | -1.210 | -0.545 | 2 | -0.564 | -0.522 | 2 | -2.258 | -2.439 |
| SOLUSDT | 12h | calibrated | BRK_mem_first | record | ALL | both | 17 | -0.088 | -0.069 | 17 | -1.717 | -1.699 | 10 | -0.262 | -0.246 | 10 | -1.894 | -1.878 | 7 | -0.089 | -0.065 | 7 | -1.378 | -1.355 |
| SOLUSDT | 12h | calibrated | BRK_mem_first | record | ALL | long | 10 | +0.402 | +0.372 | 10 | -0.834 | -1.079 | 6 | -0.603 | -0.652 | 6 | -2.102 | -2.736 | 4 | +0.700 | +0.706 | 4 | +1.309 | +1.537 |
| SOLUSDT | 12h | calibrated | BRK_mem_first | record | ALL | short | 7 | -0.809 | -0.741 | 7 | -2.080 | -1.798 | 4 | +0.988 | +1.067 | 4 | -1.896 | -1.231 | 3 | -1.346 | -1.304 | 3 | -2.418 | -2.599 |
| SOLUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 16 | -0.154 | -0.136 | 16 | -1.542 | -1.524 | 11 | +0.281 | +0.297 | 11 | -0.970 | -0.954 | 5 | -0.596 | -0.572 | 5 | -2.419 | -2.396 |
| SOLUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 9 | +0.532 | +0.502 | 9 | -0.395 | -0.640 | 7 | +0.281 | +0.232 | 7 | -0.395 | -1.029 | 2 | +3.914 | +3.920 | 2 | +3.536 | +3.764 |
| SOLUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 7 | -0.804 | -0.737 | 7 | -1.712 | -1.431 | 4 | +0.540 | +0.620 | 4 | -1.341 | -0.676 | 3 | -1.346 | -1.304 | 3 | -2.418 | -2.599 |
| SOLUSDT | 12h | calibrated | SFP_harden | record | ALL | both | 25 | -0.655 | -0.637 | 25 | +1.370 | +1.389 | 13 | -0.935 | -0.919 | 13 | +1.423 | +1.438 | 12 | -0.194 | -0.170 | 12 | +0.777 | +0.801 |
| SOLUSDT | 12h | calibrated | SFP_harden | record | ALL | long | 11 | +1.053 | +1.022 | 11 | +1.603 | +1.358 | 7 | +1.270 | +1.222 | 7 | +1.605 | +0.970 | 4 | +0.661 | +0.668 | 4 | -2.108 | -1.880 |
| SOLUSDT | 12h | calibrated | SFP_harden | record | ALL | short | 14 | -0.984 | -0.916 | 14 | +1.087 | +1.369 | 6 | -2.851 | -2.771 | 6 | +1.291 | +1.956 | 8 | -0.724 | -0.683 | 8 | +0.777 | +0.596 |
| SOLUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 14 | -0.023 | -0.011 | 13 | -0.785 | -0.773 | 7 | +0.239 | +0.250 | 7 | +2.311 | +2.322 | 7 | -1.926 | -1.910 | 6 | -1.264 | -1.248 |
| SOLUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 8 | -0.019 | -0.012 | 8 | -1.065 | -1.297 | 5 | +0.242 | +0.173 | 5 | +2.314 | +1.062 | 3 | -1.956 | -1.843 | 3 | -1.622 | -0.536 |
| SOLUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 6 | -0.130 | -0.111 | 5 | +0.329 | +0.585 | 2 | -0.740 | -0.649 | 2 | +2.314 | +3.588 | 4 | -0.132 | -0.212 | 3 | +0.328 | -0.725 |
| SOLUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 12 | -0.024 | -0.011 | 11 | -0.786 | -0.774 | 6 | -0.018 | -0.007 | 6 | +0.766 | +0.777 | 6 | -0.131 | -0.115 | 5 | -1.173 | -1.157 |
| SOLUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 7 | +0.239 | +0.245 | 7 | -0.782 | -1.014 | 5 | +0.242 | +0.173 | 5 | +2.314 | +1.062 | 2 | +0.834 | +0.947 | 2 | -3.727 | -2.642 |
| SOLUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 5 | -1.925 | -1.906 | 4 | -0.422 | -0.166 | 1 | -4.168 | -4.077 | 1 | -2.089 | -0.815 | 4 | -0.132 | -0.212 | 3 | +0.328 | -0.725 |
| SOLUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 12 | +0.443 | +0.456 | 12 | -0.641 | -0.629 | 7 | +0.452 | +0.463 | 7 | +2.105 | +2.116 | 5 | +0.431 | +0.448 | 5 | -3.205 | -3.189 |
| SOLUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 8 | +0.444 | +0.450 | 8 | -0.198 | -0.429 | 5 | +0.453 | +0.385 | 5 | +2.107 | +0.856 | 3 | +0.437 | +0.550 | 3 | -3.200 | -2.114 |
| SOLUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 4 | -0.997 | -0.977 | 4 | -0.880 | -0.624 | 2 | -0.740 | -0.649 | 2 | +2.314 | +3.588 | 2 | -0.997 | -1.077 | 2 | -4.912 | -5.965 |
| SOLUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 9 | +0.437 | +0.449 | 9 | +0.334 | +0.346 | 6 | +0.442 | +0.453 | 6 | +1.664 | +1.675 | 3 | +0.431 | +0.448 | 3 | -1.621 | -1.605 |
| SOLUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | +0.452 | +0.458 | 7 | +1.220 | +0.989 | 5 | +0.453 | +0.385 | 5 | +2.107 | +0.856 | 2 | +2.031 | +2.144 | 2 | -2.411 | -1.325 |
| SOLUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 2 | -3.558 | -3.538 | 2 | -0.880 | -0.624 | 1 | -4.168 | -4.077 | 1 | -2.089 | -0.815 | 1 | -2.947 | -3.027 | 1 | +0.328 | -0.725 |
| SOLUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 11 | +0.109 | +0.121 | 11 | -2.050 | -2.037 | 6 | -0.544 | -0.532 | 6 | +4.088 | +4.099 | 5 | +0.649 | +0.665 | 5 | -4.499 | -4.483 |
| SOLUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 7 | -1.100 | -1.094 | 7 | -1.619 | -1.850 | 4 | -0.906 | -0.975 | 4 | +7.168 | +5.916 | 3 | -1.101 | -0.988 | 3 | -4.401 | -3.315 |
| SOLUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 4 | +0.802 | +0.821 | 4 | -5.432 | -5.176 | 2 | -0.111 | -0.020 | 2 | +1.814 | +3.087 | 2 | +0.802 | +0.722 | 2 | -9.482 | -10.535 |
| SOLUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 8 | -1.138 | -1.125 | 8 | -1.835 | -1.822 | 5 | -1.200 | -1.189 | 5 | +2.497 | +2.508 | 3 | -1.101 | -1.085 | 3 | -4.401 | -4.385 |
| SOLUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 7 | -1.100 | -1.094 | 7 | -1.619 | -1.850 | 4 | -0.906 | -0.975 | 4 | +7.168 | +5.916 | 3 | -1.101 | -0.988 | 3 | -4.401 | -3.315 |
| SOLUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 1 | -1.201 | -1.182 | 1 | -2.051 | -1.795 | 1 | -1.201 | -1.110 | 1 | -2.051 | -0.778 | 0 | — | — | 0 | — | — |
| SOLUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 11 | +1.093 | +1.106 | 10 | -2.186 | -2.174 | 5 | -1.425 | -1.413 | 5 | -1.254 | -1.243 | 6 | +1.248 | +1.265 | 5 | -2.796 | -2.780 |
| SOLUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 6 | +0.465 | +0.471 | 6 | -1.414 | -1.646 | 4 | +0.849 | +0.781 | 4 | +0.847 | -0.405 | 2 | +0.463 | +0.576 | 2 | -2.965 | -1.880 |
| SOLUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 5 | +1.406 | +1.425 | 4 | -3.191 | -2.934 | 1 | -8.704 | -8.613 | 1 | -5.194 | -3.920 | 4 | +1.453 | +1.373 | 3 | -2.796 | -3.849 |
| SOLUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 12 | +0.842 | +0.855 | 11 | -1.576 | -1.564 | 7 | -1.131 | -1.120 | 7 | -1.252 | -1.241 | 5 | +1.404 | +1.420 | 4 | -2.582 | -2.566 |
| SOLUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 7 | -0.164 | -0.158 | 7 | -1.575 | -1.806 | 5 | -1.131 | -1.200 | 5 | -1.252 | -2.504 | 2 | +0.463 | +0.576 | 2 | -2.965 | -1.880 |
| SOLUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 5 | +1.406 | +1.425 | 4 | -0.995 | -0.739 | 2 | -4.055 | -3.964 | 2 | -1.798 | -0.524 | 3 | +1.500 | +1.420 | 2 | +0.737 | -0.316 |
| SOLUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 12 | -1.701 | -1.688 | 10 | +3.657 | +3.669 | 5 | -2.005 | -1.994 | 5 | +4.145 | +4.156 | 7 | -1.676 | -1.659 | 5 | +3.171 | +3.188 |
| SOLUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 5 | +1.972 | +1.978 | 5 | +9.432 | +9.200 | 3 | +4.155 | +4.086 | 3 | +51.686 | +50.434 | 2 | +0.149 | +0.262 | 2 | +1.939 | +3.024 |
| SOLUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 7 | -2.012 | -1.992 | 5 | +3.171 | +3.428 | 2 | -3.835 | -3.744 | 2 | -44.153 | -42.879 | 5 | -1.731 | -1.811 | 3 | +3.171 | +2.118 |
| NEARUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 352 | +0.029 | +0.090 | 351 | -0.655 | -0.595 | 212 | +0.111 | +0.165 | 212 | -0.829 | -0.775 | 140 | -0.111 | -0.043 | 139 | -0.065 | +0.003 |
| NEARUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 185 | -0.366 | -0.222 | 184 | -0.142 | +0.048 | 114 | +0.162 | +0.288 | 114 | +0.229 | +0.237 | 71 | -0.897 | -0.721 | 70 | -1.337 | -0.839 |
| NEARUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 167 | +0.294 | +0.270 | 167 | -0.660 | -0.729 | 98 | +0.097 | +0.079 | 98 | -0.948 | -0.848 | 69 | +0.433 | +0.394 | 69 | +0.447 | +0.086 |
| NEARUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 293 | +0.112 | +0.172 | 292 | -0.598 | -0.538 | 173 | +0.310 | +0.364 | 173 | -0.794 | -0.740 | 120 | -0.038 | +0.031 | 119 | -0.066 | +0.003 |
| NEARUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 157 | -0.367 | -0.223 | 156 | -0.143 | +0.047 | 95 | +0.218 | +0.344 | 95 | +0.447 | +0.456 | 62 | -0.818 | -0.642 | 61 | -1.443 | -0.945 |
| NEARUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 136 | +0.455 | +0.431 | 136 | -0.648 | -0.717 | 78 | +0.394 | +0.376 | 78 | -0.948 | -0.848 | 58 | +0.456 | +0.417 | 58 | +0.622 | +0.262 |
| NEARUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 313 | -0.267 | -0.206 | 313 | -0.417 | -0.357 | 193 | -0.241 | -0.187 | 193 | -0.652 | -0.598 | 120 | -0.323 | -0.255 | 120 | -0.322 | -0.253 |
| NEARUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 160 | -0.383 | -0.239 | 160 | -0.706 | -0.517 | 100 | -0.102 | +0.025 | 100 | +0.595 | +0.604 | 60 | -1.235 | -1.059 | 60 | -1.546 | -1.048 |
| NEARUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 153 | -0.211 | -0.235 | 153 | -0.127 | -0.196 | 93 | -0.477 | -0.495 | 93 | -1.012 | -0.912 | 60 | +0.073 | +0.035 | 60 | +1.053 | +0.692 |
| NEARUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 274 | -0.351 | -0.291 | 274 | -0.681 | -0.620 | 168 | -0.320 | -0.266 | 168 | -0.407 | -0.353 | 106 | -0.371 | -0.302 | 106 | -0.904 | -0.835 |
| NEARUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 143 | -0.489 | -0.345 | 143 | -0.888 | -0.699 | 88 | -0.100 | +0.027 | 88 | +0.052 | +0.060 | 55 | -1.160 | -0.985 | 55 | -1.560 | -1.062 |
| NEARUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 131 | -0.268 | -0.292 | 131 | -0.172 | -0.241 | 80 | -0.523 | -0.541 | 80 | -0.920 | -0.820 | 51 | +0.076 | +0.037 | 51 | +0.977 | +0.616 |
| NEARUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 255 | -0.482 | -0.422 | 255 | -0.397 | -0.337 | 162 | -0.357 | -0.303 | 162 | -0.549 | -0.494 | 93 | -0.567 | -0.499 | 93 | +0.209 | +0.277 |
| NEARUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 123 | -0.623 | -0.478 | 123 | -0.890 | -0.701 | 80 | -0.243 | -0.117 | 80 | +0.231 | +0.239 | 43 | -1.913 | -1.738 | 43 | -1.449 | -0.951 |
| NEARUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 132 | -0.217 | -0.241 | 132 | -0.091 | -0.160 | 82 | -0.637 | -0.655 | 82 | -0.781 | -0.681 | 50 | +0.308 | +0.269 | 50 | +1.694 | +1.333 |
| NEARUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 230 | -0.541 | -0.481 | 230 | -0.557 | -0.496 | 143 | -0.481 | -0.427 | 143 | -0.834 | -0.780 | 87 | -0.886 | -0.818 | 87 | +0.209 | +0.277 |
| NEARUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 113 | -0.678 | -0.534 | 113 | -1.044 | -0.854 | 71 | -0.239 | -0.113 | 71 | -0.160 | -0.152 | 42 | -2.027 | -1.851 | 42 | -1.420 | -0.922 |
| NEARUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 117 | -0.368 | -0.392 | 117 | -0.391 | -0.460 | 72 | -0.649 | -0.667 | 72 | -1.166 | -1.066 | 45 | +0.450 | +0.411 | 45 | +1.843 | +1.483 |
| NEARUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 275 | -0.216 | -0.156 | 275 | -0.120 | -0.060 | 170 | -0.363 | -0.309 | 170 | -0.400 | -0.346 | 105 | +0.121 | +0.190 | 105 | +0.118 | +0.187 |
| NEARUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 146 | -0.658 | -0.513 | 146 | -0.436 | -0.247 | 91 | -0.863 | -0.737 | 91 | -0.003 | +0.006 | 55 | -0.399 | -0.224 | 55 | -0.676 | -0.178 |
| NEARUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 129 | +0.345 | +0.321 | 129 | +0.471 | +0.402 | 79 | +0.054 | +0.036 | 79 | -0.598 | -0.498 | 50 | +0.411 | +0.372 | 50 | +1.384 | +1.023 |
| NEARUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 270 | -0.260 | -0.200 | 270 | +0.102 | +0.162 | 168 | -0.443 | -0.389 | 168 | -0.082 | -0.028 | 102 | +0.063 | +0.131 | 102 | +0.679 | +0.748 |
| NEARUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 147 | -0.623 | -0.478 | 147 | -0.526 | -0.337 | 94 | -0.683 | -0.557 | 94 | +0.092 | +0.101 | 53 | -0.517 | -0.341 | 53 | -0.791 | -0.293 |
| NEARUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 123 | +0.318 | +0.294 | 123 | +1.235 | +1.166 | 74 | -0.186 | -0.204 | 74 | -0.287 | -0.187 | 49 | +0.483 | +0.445 | 49 | +2.432 | +2.071 |
| NEARUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 549 | -0.100 | -0.039 | 547 | -0.059 | +0.001 | 329 | +0.344 | +0.398 | 329 | +0.475 | +0.529 | 220 | -0.768 | -0.700 | 218 | -0.936 | -0.867 |
| NEARUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 265 | -0.180 | -0.035 | 265 | -1.487 | -1.298 | 154 | +0.184 | +0.310 | 154 | -0.578 | -0.569 | 111 | -0.806 | -0.630 | 111 | -2.298 | -1.800 |
| NEARUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 284 | -0.007 | -0.031 | 282 | +1.797 | +1.728 | 175 | +0.450 | +0.432 | 175 | +2.034 | +2.134 | 109 | -0.739 | -0.777 | 107 | +1.106 | +0.745 |
| NEARUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 94 | +0.199 | +0.228 | 94 | +0.461 | +0.490 | 54 | +0.305 | +0.331 | 54 | +0.399 | +0.425 | 40 | -0.150 | -0.116 | 40 | +0.630 | +0.663 |
| NEARUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 47 | -0.304 | -0.212 | 47 | +0.493 | +0.806 | 30 | +0.307 | +0.342 | 30 | +0.427 | +0.436 | 17 | -0.356 | -0.138 | 17 | +0.566 | +1.384 |
| NEARUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 47 | +0.527 | +0.492 | 47 | +0.433 | +0.178 | 24 | +0.319 | +0.336 | 24 | +0.141 | +0.183 | 23 | +0.792 | +0.641 | 23 | +0.691 | -0.060 |
| NEARUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 84 | +0.064 | +0.092 | 84 | +0.392 | +0.421 | 48 | +0.206 | +0.231 | 48 | +0.399 | +0.425 | 36 | -0.151 | -0.118 | 36 | +0.401 | +0.435 |
| NEARUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 46 | -0.326 | -0.233 | 46 | +0.534 | +0.847 | 29 | +0.297 | +0.331 | 29 | +0.495 | +0.504 | 17 | -0.356 | -0.138 | 17 | +0.566 | +1.384 |
| NEARUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 38 | +0.314 | +0.279 | 38 | +0.039 | -0.216 | 19 | +0.109 | +0.126 | 19 | -0.154 | -0.111 | 19 | +0.924 | +0.773 | 19 | +0.236 | -0.515 |
| NEARUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 81 | +0.544 | +0.572 | 81 | -0.142 | -0.113 | 47 | +0.833 | +0.859 | 47 | -0.413 | -0.388 | 34 | -0.448 | -0.414 | 34 | +0.485 | +0.519 |
| NEARUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 42 | +0.735 | +0.828 | 42 | +0.550 | +0.862 | 27 | +0.929 | +0.963 | 27 | +0.960 | +0.968 | 15 | -0.669 | -0.451 | 15 | +0.163 | +0.981 |
| NEARUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 39 | +0.302 | +0.268 | 39 | -0.425 | -0.680 | 20 | +0.526 | +0.543 | 20 | -0.772 | -0.729 | 19 | -0.393 | -0.545 | 19 | +1.006 | +0.255 |
| NEARUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 75 | +0.543 | +0.571 | 75 | -0.251 | -0.222 | 44 | +0.827 | +0.853 | 44 | -0.553 | -0.528 | 31 | -0.393 | -0.360 | 31 | +0.732 | +0.765 |
| NEARUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 40 | +0.735 | +0.828 | 40 | +0.550 | +0.862 | 26 | +0.915 | +0.949 | 26 | +0.659 | +0.668 | 14 | -0.298 | -0.080 | 14 | +0.449 | +1.268 |
| NEARUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 35 | +0.301 | +0.266 | 35 | -0.707 | -0.962 | 18 | +0.523 | +0.541 | 18 | -0.868 | -0.825 | 17 | -0.394 | -0.546 | 17 | +1.005 | +0.254 |
| NEARUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 66 | +0.349 | +0.378 | 66 | -0.342 | -0.313 | 37 | +0.112 | +0.138 | 37 | -0.790 | -0.765 | 29 | +0.599 | +0.632 | 29 | +0.988 | +1.022 |
| NEARUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 35 | +0.503 | +0.596 | 35 | -0.782 | -0.470 | 19 | +0.509 | +0.543 | 19 | -0.787 | -0.779 | 16 | +0.481 | +0.700 | 16 | +0.111 | +0.929 |
| NEARUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 31 | +0.305 | +0.270 | 31 | +1.010 | +0.756 | 18 | -0.052 | -0.035 | 18 | -1.079 | -1.037 | 13 | +1.309 | +1.157 | 13 | +1.141 | +0.390 |
| NEARUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 63 | +0.334 | +0.362 | 63 | -0.344 | -0.315 | 37 | +0.112 | +0.138 | 37 | -0.790 | -0.765 | 26 | +0.481 | +0.514 | 26 | +0.862 | +0.895 |
| NEARUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 34 | +0.555 | +0.648 | 34 | -0.787 | -0.475 | 19 | +0.509 | +0.543 | 19 | -0.787 | -0.779 | 15 | +0.602 | +0.821 | 15 | -0.340 | +0.478 |
| NEARUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 29 | +0.106 | +0.071 | 29 | +1.011 | +0.756 | 18 | -0.052 | -0.035 | 18 | -1.079 | -1.037 | 11 | +0.301 | +0.150 | 11 | +1.141 | +0.390 |
| NEARUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 59 | +0.474 | +0.503 | 59 | +0.178 | +0.207 | 31 | +0.477 | +0.502 | 31 | +0.506 | +0.532 | 28 | +0.283 | +0.317 | 28 | +0.048 | +0.082 |
| NEARUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 27 | +0.294 | +0.386 | 27 | +4.585 | +4.897 | 16 | +0.428 | +0.462 | 16 | +4.925 | +4.934 | 11 | -0.292 | -0.074 | 11 | +3.704 | +4.522 |
| NEARUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 32 | +0.636 | +0.602 | 32 | -0.060 | -0.314 | 15 | +0.474 | +0.491 | 15 | +0.178 | +0.220 | 17 | +0.859 | +0.707 | 17 | -0.148 | -0.899 |
| NEARUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 60 | +0.327 | +0.356 | 60 | +1.575 | +1.604 | 30 | +0.330 | +0.356 | 30 | +3.052 | +3.078 | 30 | +0.283 | +0.317 | 30 | +0.796 | +0.829 |
| NEARUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 30 | +0.288 | +0.380 | 30 | +3.125 | +3.437 | 17 | +0.286 | +0.321 | 17 | +1.898 | +1.907 | 13 | +1.706 | +1.924 | 13 | +3.704 | +4.522 |
| NEARUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 30 | +0.404 | +0.369 | 30 | +0.048 | -0.206 | 13 | +0.474 | +0.491 | 13 | +4.206 | +4.249 | 17 | -0.485 | -0.636 | 17 | -1.498 | -2.249 |
| NEARUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 154 | -0.082 | -0.053 | 154 | -0.233 | -0.204 | 95 | -0.023 | +0.003 | 95 | -0.622 | -0.596 | 59 | -0.327 | -0.294 | 59 | +0.039 | +0.073 |
| NEARUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 86 | -0.139 | -0.047 | 86 | +0.218 | +0.531 | 53 | -0.137 | -0.103 | 53 | -0.007 | +0.002 | 33 | +0.115 | +0.333 | 33 | +1.166 | +1.984 |
| NEARUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 68 | -0.013 | -0.048 | 68 | -1.261 | -1.516 | 42 | +0.030 | +0.048 | 42 | -2.623 | -2.580 | 26 | -0.541 | -0.692 | 26 | -0.766 | -1.517 |
| NEARUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | both | 30 | +0.267 | +0.283 | 29 | +0.948 | +0.964 | 16 | +0.503 | +0.517 | 16 | +1.771 | +1.785 | 14 | -0.327 | -0.309 | 13 | -0.194 | -0.176 |
| NEARUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | long | 15 | -0.492 | -0.439 | 15 | -0.200 | +0.193 | 9 | -0.735 | -0.726 | 9 | +2.596 | +2.329 | 6 | -0.012 | +0.165 | 6 | -1.498 | -0.432 |
| NEARUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | short | 15 | +0.446 | +0.424 | 14 | +1.715 | +1.354 | 7 | +1.246 | +1.266 | 7 | +0.944 | +1.240 | 8 | -0.987 | -1.127 | 7 | +2.486 | +1.457 |
| NEARUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 23 | +0.469 | +0.485 | 23 | +0.948 | +0.964 | 12 | +0.614 | +0.628 | 12 | +2.723 | +2.737 | 11 | -0.157 | -0.139 | 11 | -0.397 | -0.378 |
| NEARUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 12 | +0.517 | +0.570 | 12 | +2.727 | +3.119 | 6 | +0.619 | +0.628 | 6 | +3.304 | +3.037 | 6 | -0.012 | +0.165 | 6 | -1.498 | -0.432 |
| NEARUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 11 | +0.445 | +0.424 | 11 | -0.195 | -0.556 | 6 | +0.844 | +0.864 | 6 | -2.071 | -1.776 | 5 | -0.158 | -0.298 | 5 | -0.195 | -1.224 |
| NEARUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | both | 24 | +0.066 | +0.082 | 23 | -0.269 | -0.253 | 11 | +0.048 | +0.063 | 11 | -0.268 | -0.253 | 13 | +0.367 | +0.386 | 12 | -0.076 | -0.057 |
| NEARUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | long | 13 | +0.020 | +0.074 | 13 | -0.392 | +0.001 | 7 | -0.444 | -0.436 | 7 | -0.267 | -0.534 | 6 | +0.244 | +0.421 | 6 | -1.871 | -0.805 |
| NEARUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | short | 11 | +0.365 | +0.343 | 10 | +0.592 | +0.232 | 4 | +0.666 | +0.686 | 4 | -0.971 | -0.676 | 7 | +0.364 | +0.224 | 6 | +1.024 | -0.005 |
| NEARUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 17 | +0.368 | +0.384 | 17 | +0.948 | +0.964 | 7 | +0.087 | +0.101 | 7 | +3.524 | +3.538 | 10 | +0.418 | +0.437 | 10 | -0.438 | -0.420 |
| NEARUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 9 | +0.019 | +0.073 | 9 | +3.695 | +4.088 | 3 | -0.443 | -0.434 | 3 | +7.756 | +7.489 | 6 | +0.244 | +0.421 | 6 | -1.871 | -0.805 |
| NEARUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 8 | +0.805 | +0.784 | 8 | +0.230 | -0.131 | 4 | +0.666 | +0.686 | 4 | -0.971 | -0.676 | 4 | +1.034 | +0.894 | 4 | +0.660 | -0.369 |
| NEARUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | both | 24 | +0.571 | +0.587 | 23 | -0.266 | -0.250 | 13 | +0.676 | +0.690 | 13 | +1.383 | +1.397 | 11 | +0.466 | +0.485 | 10 | -0.446 | -0.427 |
| NEARUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | long | 12 | -0.725 | -0.671 | 12 | -1.370 | -0.977 | 7 | -0.333 | -0.324 | 7 | -1.159 | -1.426 | 5 | -1.756 | -1.579 | 5 | -1.581 | -0.515 |
| NEARUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | short | 12 | +1.104 | +1.082 | 11 | +1.059 | +0.698 | 6 | +0.994 | +1.013 | 6 | +2.820 | +3.116 | 6 | +1.294 | +1.154 | 5 | -0.200 | -1.229 |
| NEARUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 18 | +0.572 | +0.588 | 18 | -0.229 | -0.213 | 11 | +0.676 | +0.690 | 11 | +1.383 | +1.397 | 7 | +0.463 | +0.482 | 7 | -0.271 | -0.252 |
| NEARUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 10 | +0.069 | +0.123 | 10 | -0.711 | -0.318 | 6 | +0.174 | +0.183 | 6 | +0.987 | +0.720 | 4 | -0.643 | -0.466 | 4 | -0.923 | +0.143 |
| NEARUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 8 | +1.668 | +1.646 | 8 | +0.429 | +0.068 | 5 | +1.247 | +1.267 | 5 | +1.378 | +1.674 | 3 | +4.066 | +3.926 | 3 | -0.200 | -1.229 |
| NEARUSDT | 12h | calibrated | BRK_mem_first | record | ALL | both | 21 | +0.722 | +0.738 | 21 | +0.335 | +0.351 | 13 | +0.863 | +0.877 | 13 | +0.337 | +0.351 | 8 | -1.080 | -1.062 | 8 | -0.264 | -0.245 |
| NEARUSDT | 12h | calibrated | BRK_mem_first | record | ALL | long | 13 | +0.673 | +0.726 | 13 | -0.587 | -0.194 | 9 | +0.675 | +0.683 | 9 | -0.585 | -0.852 | 4 | +0.230 | +0.407 | 4 | -0.288 | +0.778 |
| NEARUSDT | 12h | calibrated | BRK_mem_first | record | ALL | short | 8 | +0.789 | +0.768 | 8 | +1.196 | +0.835 | 4 | +1.640 | +1.660 | 4 | +4.272 | +4.568 | 4 | -1.079 | -1.219 | 4 | -0.187 | -1.216 |
| NEARUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 20 | +0.488 | +0.504 | 20 | +0.524 | +0.540 | 12 | +0.793 | +0.807 | 12 | +0.565 | +0.579 | 8 | -1.795 | -1.777 | 8 | -0.188 | -0.169 |
| NEARUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 10 | +0.491 | +0.544 | 10 | -0.394 | -0.001 | 7 | +0.675 | +0.684 | 7 | +0.339 | +0.072 | 3 | -2.621 | -2.444 | 3 | -1.132 | -0.066 |
| NEARUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 10 | +0.175 | +0.154 | 10 | +1.197 | +0.836 | 5 | +0.859 | +0.879 | 5 | +3.042 | +3.337 | 5 | -1.789 | -1.929 | 5 | +0.710 | -0.319 |
| NEARUSDT | 12h | calibrated | SFP_harden | record | ALL | both | 29 | -0.452 | -0.436 | 29 | -0.620 | -0.604 | 15 | -0.423 | -0.408 | 15 | -2.451 | -2.437 | 14 | -0.756 | -0.737 | 14 | +0.926 | +0.945 |
| NEARUSDT | 12h | calibrated | SFP_harden | record | ALL | long | 18 | -0.432 | -0.378 | 18 | -1.430 | -1.037 | 9 | -0.418 | -0.410 | 9 | -2.446 | -2.713 | 9 | -0.452 | -0.275 | 9 | -0.620 | +0.446 |
| NEARUSDT | 12h | calibrated | SFP_harden | record | ALL | short | 11 | -1.545 | -1.567 | 11 | +1.243 | +0.882 | 6 | -0.216 | -0.197 | 6 | -0.970 | -0.675 | 5 | -1.545 | -1.685 | 5 | +1.243 | +0.214 |
| NEARUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 12 | +0.334 | +0.346 | 11 | +1.045 | +1.056 | 9 | +0.456 | +0.466 | 9 | +1.925 | +1.935 | 3 | +0.007 | +0.020 | 2 | -5.378 | -5.366 |
| NEARUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 7 | +0.482 | +0.649 | 6 | +0.755 | +1.627 | 5 | +1.768 | +1.803 | 5 | +1.048 | +1.364 | 2 | -0.695 | -0.233 | 1 | -1.437 | +0.066 |
| NEARUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 5 | +0.007 | -0.138 | 5 | +3.844 | +2.994 | 4 | -0.248 | -0.263 | 4 | +4.164 | +3.867 | 1 | +0.007 | -0.430 | 1 | -9.319 | -10.798 |
| NEARUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 10 | +0.347 | +0.358 | 9 | +0.463 | +0.474 | 7 | +1.740 | +1.750 | 7 | +1.045 | +1.055 | 3 | +0.007 | +0.020 | 2 | -5.378 | -5.366 |
| NEARUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 7 | +0.482 | +0.649 | 6 | +0.755 | +1.627 | 5 | +1.768 | +1.803 | 5 | +1.048 | +1.364 | 2 | -0.695 | -0.233 | 1 | -1.437 | +0.066 |
| NEARUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 3 | +0.002 | -0.142 | 3 | -9.324 | -10.174 | 2 | -3.890 | -3.905 | 2 | -12.572 | -12.869 | 1 | +0.007 | -0.430 | 1 | -9.319 | -10.798 |
| NEARUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 8 | +0.534 | +0.545 | 7 | -0.104 | -0.093 | 6 | +0.701 | +0.711 | 6 | +1.178 | +1.188 | 2 | -0.912 | -0.900 | 1 | -1.533 | -1.521 |
| NEARUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 7 | +0.482 | +0.649 | 6 | -0.263 | +0.609 | 5 | +0.588 | +0.623 | 5 | -0.102 | +0.215 | 2 | -0.912 | -0.451 | 1 | -1.533 | -0.030 |
| NEARUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 1 | +0.811 | +0.666 | 1 | +2.456 | +1.606 | 1 | +0.811 | +0.796 | 1 | +2.456 | +2.159 | 0 | — | — | 0 | — | — |
| NEARUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 8 | +0.534 | +0.545 | 7 | -0.104 | -0.093 | 6 | +0.701 | +0.711 | 6 | +1.178 | +1.188 | 2 | -0.912 | -0.900 | 1 | -1.533 | -1.521 |
| NEARUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | +0.482 | +0.649 | 6 | -0.263 | +0.609 | 5 | +0.588 | +0.623 | 5 | -0.102 | +0.215 | 2 | -0.912 | -0.451 | 1 | -1.533 | -0.030 |
| NEARUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 1 | +0.811 | +0.666 | 1 | +2.456 | +1.606 | 1 | +0.811 | +0.796 | 1 | +2.456 | +2.159 | 0 | — | — | 0 | — | — |
| NEARUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 8 | -0.226 | -0.215 | 8 | -0.055 | -0.044 | 5 | +0.312 | +0.322 | 5 | +2.247 | +2.257 | 3 | -1.909 | -1.896 | 3 | -2.408 | -2.396 |
| NEARUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 7 | -0.159 | +0.008 | 7 | -0.052 | +0.820 | 5 | +0.312 | +0.347 | 5 | +2.247 | +2.564 | 2 | -1.101 | -0.639 | 2 | -3.477 | -1.973 |
| NEARUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 1 | -9.962 | -10.107 | 1 | -2.412 | -3.262 | 0 | — | — | 0 | — | — | 1 | -9.962 | -10.399 | 1 | -2.412 | -3.891 |
| NEARUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 7 | -0.159 | -0.148 | 7 | -0.052 | -0.041 | 5 | +0.312 | +0.322 | 5 | +2.247 | +2.257 | 2 | -5.129 | -5.117 | 2 | -2.292 | -2.279 |
| NEARUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 6 | +0.077 | +0.244 | 6 | +1.098 | +1.969 | 5 | +0.312 | +0.347 | 5 | +2.247 | +2.564 | 1 | -0.297 | +0.165 | 1 | -2.171 | -0.668 |
| NEARUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 1 | -9.962 | -10.107 | 1 | -2.412 | -3.262 | 0 | — | — | 0 | — | — | 1 | -9.962 | -10.399 | 1 | -2.412 | -3.891 |
| NEARUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 9 | +0.308 | +0.319 | 9 | -0.113 | -0.102 | 5 | +0.311 | +0.321 | 5 | -0.053 | -0.043 | 4 | +0.257 | +0.269 | 4 | -1.143 | -1.131 |
| NEARUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 4 | +0.011 | +0.178 | 4 | -0.122 | +0.750 | 3 | +0.312 | +0.347 | 3 | -0.052 | +0.265 | 1 | -0.297 | +0.165 | 1 | -2.171 | -0.668 |
| NEARUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 5 | +0.689 | +0.544 | 5 | -0.115 | -0.964 | 2 | +3.754 | +3.739 | 2 | -8.415 | -8.712 | 3 | +0.689 | +0.252 | 3 | -0.115 | -1.593 |
| NEARUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 9 | +0.308 | +0.319 | 9 | -0.194 | -0.183 | 6 | -0.151 | -0.141 | 6 | -0.122 | -0.112 | 3 | +0.686 | +0.698 | 3 | -2.171 | -2.159 |
| NEARUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 4 | +0.011 | +0.178 | 4 | -0.122 | +0.750 | 3 | +0.312 | +0.347 | 3 | -0.052 | +0.265 | 1 | -0.297 | +0.165 | 1 | -2.171 | -0.668 |
| NEARUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 5 | +0.689 | +0.544 | 5 | -9.638 | -10.487 | 3 | -0.616 | -0.631 | 3 | -14.828 | -15.124 | 2 | +1.151 | +0.714 | 2 | -3.239 | -4.717 |
| NEARUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 12 | -0.630 | -0.619 | 12 | +0.598 | +0.609 | 7 | -0.941 | -0.932 | 7 | +0.182 | +0.192 | 5 | -0.119 | -0.107 | 5 | +1.017 | +1.029 |
| NEARUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 11 | -0.315 | -0.148 | 11 | +1.017 | +1.889 | 6 | -0.627 | -0.592 | 6 | +0.882 | +1.199 | 5 | -0.119 | +0.343 | 5 | +1.017 | +2.520 |
| NEARUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 1 | -7.399 | -7.543 | 1 | -3.849 | -4.699 | 1 | -7.399 | -7.414 | 1 | -3.849 | -4.146 | 0 | — | — | 0 | — | — |
| ZECUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 350 | -0.009 | +0.057 | 349 | -0.358 | -0.292 | 228 | +0.118 | +0.188 | 228 | -0.004 | +0.066 | 122 | -0.329 | -0.269 | 121 | -0.978 | -0.918 |
| ZECUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 189 | -0.102 | -0.110 | 188 | +0.025 | -0.032 | 123 | +0.148 | +0.122 | 123 | +0.251 | +0.379 | 66 | -0.403 | -0.364 | 65 | -0.351 | -0.769 |
| ZECUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 161 | +0.025 | +0.165 | 161 | -0.676 | -0.486 | 105 | +0.046 | +0.212 | 105 | -0.231 | -0.219 | 56 | -0.101 | -0.019 | 56 | -1.468 | -0.930 |
| ZECUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 298 | -0.103 | -0.037 | 297 | -0.438 | -0.372 | 195 | +0.090 | +0.160 | 195 | +0.047 | +0.117 | 103 | -0.419 | -0.359 | 102 | -1.304 | -1.243 |
| ZECUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 163 | -0.154 | -0.162 | 162 | +0.015 | -0.043 | 107 | +0.065 | +0.039 | 107 | +0.251 | +0.379 | 56 | -0.325 | -0.286 | 55 | -0.497 | -0.914 |
| ZECUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 135 | +0.025 | +0.165 | 135 | -0.918 | -0.729 | 88 | +0.267 | +0.433 | 88 | -0.326 | -0.314 | 47 | -0.572 | -0.490 | 47 | -1.910 | -1.372 |
| ZECUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 307 | -0.141 | -0.074 | 306 | -0.645 | -0.579 | 200 | -0.131 | -0.061 | 200 | -0.099 | -0.029 | 107 | -0.196 | -0.135 | 106 | -1.238 | -1.177 |
| ZECUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 165 | +0.067 | +0.059 | 164 | -0.003 | -0.060 | 107 | +0.064 | +0.038 | 107 | +0.033 | +0.161 | 58 | +0.059 | +0.098 | 57 | -0.884 | -1.302 |
| ZECUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 142 | -0.386 | -0.245 | 142 | -0.997 | -0.807 | 93 | -0.394 | -0.229 | 93 | -0.681 | -0.669 | 49 | -0.580 | -0.498 | 49 | -1.685 | -1.146 |
| ZECUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 264 | -0.256 | -0.190 | 263 | -0.620 | -0.554 | 171 | -0.237 | -0.167 | 171 | -0.176 | -0.106 | 93 | -0.293 | -0.233 | 92 | -0.892 | -0.832 |
| ZECUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 144 | -0.024 | -0.032 | 143 | -0.054 | -0.111 | 91 | -0.114 | -0.140 | 91 | -0.045 | +0.083 | 53 | -0.003 | +0.036 | 52 | -0.891 | -1.309 |
| ZECUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 120 | -0.611 | -0.471 | 120 | -0.866 | -0.676 | 80 | -0.563 | -0.398 | 80 | -0.802 | -0.790 | 40 | -0.801 | -0.719 | 40 | -0.939 | -0.401 |
| ZECUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 258 | +0.288 | +0.354 | 258 | +0.214 | +0.280 | 163 | +0.364 | +0.434 | 163 | +0.614 | +0.684 | 95 | -0.270 | -0.210 | 95 | -1.163 | -1.102 |
| ZECUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 145 | +0.319 | +0.310 | 145 | +1.101 | +1.044 | 95 | +0.446 | +0.420 | 95 | +1.418 | +1.545 | 50 | -0.039 | -0.001 | 50 | +0.033 | -0.384 |
| ZECUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 113 | +0.197 | +0.338 | 113 | -0.913 | -0.724 | 68 | +0.312 | +0.477 | 68 | +0.093 | +0.104 | 45 | -0.854 | -0.772 | 45 | -1.451 | -0.912 |
| ZECUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 233 | +0.307 | +0.373 | 233 | +0.108 | +0.174 | 145 | +0.437 | +0.507 | 145 | +0.613 | +0.683 | 88 | -0.223 | -0.162 | 88 | -1.116 | -1.055 |
| ZECUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 133 | +0.356 | +0.347 | 133 | +1.103 | +1.045 | 85 | +0.475 | +0.449 | 85 | +1.616 | +1.744 | 48 | -0.038 | +0.001 | 48 | -0.649 | -1.067 |
| ZECUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 100 | +0.132 | +0.272 | 100 | -0.964 | -0.774 | 60 | +0.294 | +0.460 | 60 | -0.716 | -0.704 | 40 | -0.862 | -0.780 | 40 | -1.180 | -0.641 |
| ZECUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 272 | -0.185 | -0.119 | 272 | -0.627 | -0.561 | 178 | -0.459 | -0.389 | 178 | -0.383 | -0.313 | 94 | +0.241 | +0.302 | 94 | -1.045 | -0.985 |
| ZECUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 152 | +0.084 | +0.076 | 152 | +0.597 | +0.540 | 102 | -0.255 | -0.281 | 102 | +0.641 | +0.769 | 50 | +0.742 | +0.780 | 50 | -0.047 | -0.464 |
| ZECUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 120 | -0.453 | -0.313 | 120 | -1.214 | -1.024 | 76 | -0.632 | -0.466 | 76 | -1.028 | -1.016 | 44 | -0.052 | +0.030 | 44 | -3.859 | -3.321 |
| ZECUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 235 | -0.184 | -0.118 | 235 | -0.446 | -0.380 | 154 | -0.282 | -0.212 | 154 | -0.170 | -0.100 | 81 | +0.107 | +0.168 | 81 | -1.209 | -1.149 |
| ZECUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 124 | +0.204 | +0.196 | 124 | +0.598 | +0.541 | 82 | -0.061 | -0.087 | 82 | +0.735 | +0.863 | 42 | +0.340 | +0.379 | 42 | -0.794 | -1.212 |
| ZECUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 111 | -0.650 | -0.510 | 111 | -0.841 | -0.651 | 72 | -0.634 | -0.468 | 72 | -0.772 | -0.760 | 39 | -0.910 | -0.828 | 39 | -1.738 | -1.200 |
| ZECUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 559 | -0.229 | -0.163 | 559 | -0.604 | -0.537 | 351 | -0.020 | +0.050 | 351 | -0.021 | +0.049 | 208 | -0.547 | -0.486 | 208 | -1.203 | -1.143 |
| ZECUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 272 | -0.147 | -0.156 | 272 | -0.836 | -0.893 | 147 | +0.309 | +0.283 | 147 | -0.065 | +0.063 | 125 | -0.621 | -0.583 | 125 | -1.663 | -2.081 |
| ZECUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 287 | -0.406 | -0.266 | 287 | -0.206 | -0.017 | 204 | -0.428 | -0.262 | 204 | +0.053 | +0.065 | 83 | -0.364 | -0.282 | 83 | -0.806 | -0.267 |
| ZECUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 102 | +0.257 | +0.288 | 101 | +0.178 | +0.210 | 62 | +0.329 | +0.363 | 62 | +0.319 | +0.352 | 40 | +0.197 | +0.227 | 39 | -0.258 | -0.228 |
| ZECUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 51 | +0.000 | -0.006 | 50 | -0.265 | -0.373 | 30 | -0.061 | -0.028 | 30 | -1.284 | -0.758 | 21 | +0.191 | +0.105 | 20 | +1.384 | -0.381 |
| ZECUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 51 | +0.704 | +0.775 | 51 | +0.276 | +0.448 | 32 | +0.933 | +0.966 | 32 | +1.973 | +1.513 | 19 | +0.202 | +0.347 | 19 | -0.628 | +1.197 |
| ZECUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 88 | +0.169 | +0.201 | 87 | -0.261 | -0.229 | 53 | +0.150 | +0.183 | 53 | -0.264 | -0.231 | 35 | +0.190 | +0.220 | 34 | +0.011 | +0.041 |
| ZECUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 45 | +0.003 | -0.004 | 44 | -0.274 | -0.382 | 24 | -0.059 | -0.026 | 24 | -2.071 | -1.544 | 21 | +0.191 | +0.105 | 20 | +1.384 | -0.381 |
| ZECUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 43 | +0.688 | +0.758 | 43 | +0.276 | +0.448 | 29 | +0.686 | +0.719 | 29 | +2.036 | +1.576 | 14 | -0.019 | +0.126 | 14 | -0.845 | +0.979 |
| ZECUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 90 | +0.016 | +0.048 | 90 | +0.289 | +0.321 | 56 | -0.062 | -0.029 | 56 | -0.349 | -0.315 | 34 | +0.362 | +0.392 | 34 | +0.957 | +0.987 |
| ZECUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 48 | +0.020 | +0.013 | 48 | +0.216 | +0.108 | 30 | +0.019 | +0.052 | 30 | -1.619 | -1.093 | 18 | -0.262 | -0.348 | 18 | +1.606 | -0.159 |
| ZECUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 42 | +0.047 | +0.117 | 42 | +0.607 | +0.779 | 26 | -0.316 | -0.283 | 26 | +0.253 | -0.207 | 16 | +0.593 | +0.738 | 16 | +0.832 | +2.657 |
| ZECUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 78 | +0.091 | +0.123 | 78 | +0.368 | +0.399 | 46 | +0.089 | +0.123 | 46 | +0.002 | +0.035 | 32 | +0.043 | +0.073 | 32 | +0.955 | +0.985 |
| ZECUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 43 | +0.153 | +0.146 | 43 | +0.262 | +0.154 | 25 | +0.150 | +0.183 | 25 | -1.513 | -0.987 | 18 | -0.262 | -0.348 | 18 | +1.606 | -0.159 |
| ZECUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 35 | -0.154 | -0.084 | 35 | +0.838 | +1.010 | 21 | -0.156 | -0.123 | 21 | +1.669 | +1.209 | 14 | +0.136 | +0.282 | 14 | +0.532 | +2.357 |
| ZECUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 74 | +0.150 | +0.182 | 74 | -0.233 | -0.201 | 49 | -0.004 | +0.029 | 49 | -1.518 | -1.484 | 25 | +0.376 | +0.405 | 25 | +0.327 | +0.357 |
| ZECUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 41 | +0.371 | +0.364 | 41 | -0.009 | -0.117 | 27 | +0.495 | +0.528 | 27 | -0.498 | +0.028 | 14 | +0.147 | +0.061 | 14 | +0.456 | -1.310 |
| ZECUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 33 | -0.685 | -0.615 | 33 | -0.758 | -0.586 | 22 | -1.068 | -1.035 | 22 | -2.248 | -2.708 | 11 | +0.907 | +1.052 | 11 | -0.008 | +1.817 |
| ZECUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 64 | +0.266 | +0.298 | 64 | -0.172 | -0.141 | 42 | +0.149 | +0.182 | 42 | -1.008 | -0.975 | 22 | +0.365 | +0.395 | 22 | +0.455 | +0.485 |
| ZECUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 36 | +0.456 | +0.449 | 36 | +0.451 | +0.343 | 23 | +0.599 | +0.632 | 23 | -0.247 | +0.279 | 13 | +0.004 | -0.082 | 13 | +0.584 | -1.181 |
| ZECUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 28 | -0.625 | -0.555 | 28 | -1.025 | -0.853 | 19 | -0.902 | -0.869 | 19 | -2.442 | -2.901 | 9 | +1.567 | +1.712 | 9 | -0.008 | +1.817 |
| ZECUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 70 | -0.078 | -0.046 | 70 | +0.450 | +0.482 | 46 | -0.233 | -0.200 | 46 | +0.272 | +0.305 | 24 | +0.618 | +0.647 | 24 | +0.861 | +0.891 |
| ZECUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 32 | +0.798 | +0.791 | 32 | +1.030 | +0.922 | 21 | -0.404 | -0.370 | 21 | -0.620 | -0.094 | 11 | +2.959 | +2.873 | 11 | +6.717 | +4.952 |
| ZECUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 38 | -0.273 | -0.202 | 38 | +0.093 | +0.265 | 25 | -0.001 | +0.032 | 25 | +0.574 | +0.115 | 13 | -1.718 | -1.573 | 13 | -0.117 | +1.708 |
| ZECUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 64 | -0.380 | -0.348 | 64 | +0.093 | +0.125 | 41 | -0.403 | -0.370 | 41 | -0.037 | -0.003 | 23 | -0.183 | -0.153 | 23 | +0.839 | +0.869 |
| ZECUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 27 | +0.110 | +0.103 | 27 | +0.324 | +0.216 | 18 | -0.485 | -0.452 | 18 | -0.942 | -0.416 | 9 | +2.960 | +2.874 | 9 | +6.718 | +4.953 |
| ZECUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 37 | -0.567 | -0.497 | 37 | -0.033 | +0.138 | 23 | -0.360 | -0.326 | 23 | +0.574 | +0.115 | 14 | -0.839 | -0.694 | 14 | -0.613 | +1.211 |
| ZECUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 134 | -0.050 | -0.018 | 134 | +0.027 | +0.059 | 93 | -0.105 | -0.071 | 93 | -0.525 | -0.492 | 41 | +0.186 | +0.216 | 41 | +4.679 | +4.709 |
| ZECUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 61 | +0.267 | +0.260 | 61 | +0.890 | +0.782 | 36 | +0.563 | +0.596 | 36 | +0.108 | +0.634 | 25 | -0.180 | -0.266 | 25 | +5.533 | +3.768 |
| ZECUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 73 | -0.150 | -0.080 | 73 | -0.659 | -0.487 | 57 | -0.367 | -0.333 | 57 | -1.555 | -2.015 | 16 | +0.616 | +0.761 | 16 | +0.485 | +2.310 |
| ZECUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | both | 27 | -0.204 | -0.186 | 27 | -0.848 | -0.830 | 18 | -0.274 | -0.256 | 18 | -0.277 | -0.258 | 9 | +1.745 | +1.762 | 9 | -1.082 | -1.066 |
| ZECUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | long | 16 | -0.182 | -0.325 | 16 | -1.892 | -2.290 | 11 | -0.026 | +0.029 | 11 | -2.517 | -2.213 | 5 | -0.511 | -1.071 | 5 | -1.532 | -3.232 |
| ZECUSDT | 12h | calibrated | BRK_tap89_first | record | ALL | short | 11 | -0.207 | -0.029 | 11 | +0.582 | +1.016 | 7 | -0.724 | -0.742 | 7 | +0.577 | +0.310 | 4 | +1.918 | +2.511 | 4 | +0.230 | +1.965 |
| ZECUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 24 | -0.271 | -0.253 | 24 | -0.966 | -0.948 | 17 | -0.206 | -0.188 | 17 | +0.298 | +0.316 | 7 | -0.483 | -0.467 | 7 | -1.455 | -1.438 |
| ZECUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 14 | -0.180 | -0.323 | 14 | -1.890 | -2.289 | 10 | +0.047 | +0.102 | 10 | -1.680 | -1.376 | 4 | -0.513 | -1.072 | 4 | -1.891 | -3.592 |
| ZECUSDT | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 10 | -0.349 | -0.170 | 10 | +0.924 | +1.359 | 7 | -0.724 | -0.742 | 7 | +0.577 | +0.310 | 3 | +2.090 | +2.683 | 3 | +1.274 | +3.008 |
| ZECUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | both | 23 | -0.052 | -0.034 | 23 | -0.848 | -0.830 | 15 | -0.032 | -0.013 | 15 | -0.527 | -0.509 | 8 | -0.761 | -0.744 | 8 | -1.289 | -1.272 |
| ZECUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | long | 14 | -0.432 | -0.575 | 14 | -1.651 | -2.049 | 10 | -0.180 | -0.125 | 10 | -1.344 | -1.040 | 4 | -0.802 | -1.361 | 4 | -2.238 | -3.938 |
| ZECUSDT | 12h | calibrated | BRK_tap127_first | record | ALL | short | 9 | +0.963 | +1.141 | 9 | +0.233 | +0.667 | 5 | +0.957 | +0.940 | 5 | +0.228 | -0.039 | 4 | +0.250 | +0.843 | 4 | -0.430 | +1.304 |
| ZECUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 21 | -0.029 | -0.011 | 21 | -0.525 | -0.507 | 14 | +0.314 | +0.332 | 14 | -0.146 | -0.127 | 7 | -0.528 | -0.512 | 7 | -1.122 | -1.105 |
| ZECUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 12 | -0.182 | -0.325 | 12 | -1.150 | -1.549 | 9 | -0.024 | +0.031 | 9 | -0.843 | -0.538 | 3 | -0.532 | -1.091 | 3 | -1.460 | -3.160 |
| ZECUSDT | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 9 | +0.963 | +1.141 | 9 | +0.233 | +0.667 | 5 | +0.957 | +0.940 | 5 | +0.228 | -0.039 | 4 | +0.250 | +0.843 | 4 | -0.430 | +1.304 |
| ZECUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | both | 19 | -0.032 | -0.014 | 19 | -0.022 | -0.005 | 11 | -0.033 | -0.014 | 11 | +3.250 | +3.268 | 8 | -0.200 | -0.184 | 8 | -0.737 | -0.721 |
| ZECUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | long | 9 | +0.719 | +0.576 | 9 | -1.457 | -1.855 | 5 | +0.929 | +0.984 | 5 | -0.847 | -0.543 | 4 | -0.303 | -0.863 | 4 | -1.570 | -3.271 |
| ZECUSDT | 12h | calibrated | BRK_tap200_first | record | ALL | short | 10 | -0.557 | -0.378 | 10 | +0.329 | +0.763 | 6 | -0.933 | -0.950 | 6 | +3.321 | +3.054 | 4 | -0.198 | +0.395 | 4 | +0.045 | +1.779 |
| ZECUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 17 | -0.029 | -0.011 | 17 | -0.847 | -0.830 | 10 | -0.199 | -0.180 | 10 | +1.199 | +1.218 | 7 | +0.341 | +0.358 | 7 | -1.456 | -1.439 |
| ZECUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 7 | +0.720 | +0.576 | 7 | -1.679 | -2.078 | 4 | +0.452 | +0.506 | 4 | -2.183 | -1.879 | 3 | +0.720 | +0.160 | 3 | -1.679 | -3.380 |
| ZECUSDT | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 10 | -0.557 | -0.378 | 10 | +0.329 | +0.763 | 6 | -0.933 | -0.950 | 6 | +3.321 | +3.054 | 4 | -0.198 | +0.395 | 4 | +0.045 | +1.779 |
| ZECUSDT | 12h | calibrated | BRK_mem_first | record | ALL | both | 25 | +0.247 | +0.264 | 25 | -0.848 | -0.830 | 16 | +0.035 | +0.053 | 16 | -0.929 | -0.910 | 9 | +0.589 | +0.606 | 9 | -0.847 | -0.830 |
| ZECUSDT | 12h | calibrated | BRK_mem_first | record | ALL | long | 13 | -0.175 | -0.318 | 13 | -0.849 | -1.247 | 8 | -0.542 | -0.487 | 8 | -2.002 | -1.698 | 5 | -0.175 | -0.734 | 5 | -0.849 | -2.549 |
| ZECUSDT | 12h | calibrated | BRK_mem_first | record | ALL | short | 12 | +0.750 | +0.929 | 12 | -0.231 | +0.203 | 8 | +0.398 | +0.380 | 8 | -0.623 | -0.890 | 4 | +1.826 | +2.419 | 4 | -0.078 | +1.656 |
| ZECUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 26 | +0.115 | +0.132 | 26 | -0.448 | -0.430 | 17 | -0.175 | -0.156 | 17 | -0.060 | -0.041 | 9 | +0.589 | +0.606 | 9 | -0.847 | -0.830 |
| ZECUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 14 | -0.174 | -0.317 | 14 | -0.842 | -1.240 | 9 | -0.172 | -0.118 | 9 | -0.833 | -0.529 | 5 | -0.175 | -0.734 | 5 | -0.849 | -2.549 |
| ZECUSDT | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 12 | +0.570 | +0.749 | 12 | +0.702 | +1.136 | 8 | -0.365 | -0.383 | 8 | +1.160 | +0.893 | 4 | +1.826 | +2.419 | 4 | -0.078 | +1.656 |
| ZECUSDT | 12h | calibrated | SFP_harden | record | ALL | both | 44 | -0.089 | -0.071 | 44 | +1.997 | +2.015 | 22 | -1.118 | -1.099 | 22 | +3.192 | +3.211 | 22 | +0.563 | +0.580 | 22 | -1.192 | -1.175 |
| ZECUSDT | 12h | calibrated | SFP_harden | record | ALL | long | 11 | +0.877 | +0.734 | 11 | +3.411 | +3.013 | 5 | -1.030 | -0.976 | 5 | -2.931 | -2.627 | 6 | +1.136 | +0.576 | 6 | +6.076 | +4.375 |
| ZECUSDT | 12h | calibrated | SFP_harden | record | ALL | short | 33 | -0.314 | -0.135 | 33 | +1.354 | +1.788 | 17 | -1.201 | -1.219 | 17 | +3.207 | +2.940 | 16 | +0.092 | +0.685 | 16 | -6.494 | -4.759 |
| ZECUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 15 | -0.161 | -0.148 | 15 | +3.180 | +3.193 | 10 | -0.218 | -0.205 | 10 | +2.759 | +2.772 | 5 | +0.247 | +0.259 | 5 | +4.072 | +4.084 |
| ZECUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 11 | -0.160 | -0.250 | 11 | +2.338 | +2.076 | 7 | -0.212 | -0.007 | 7 | -0.730 | -0.093 | 4 | +0.345 | -0.326 | 4 | +7.795 | +4.300 |
| ZECUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 4 | -0.415 | -0.301 | 4 | +3.625 | +3.912 | 3 | -0.797 | -0.976 | 3 | +4.070 | +3.458 | 1 | -0.033 | +0.662 | 1 | -2.495 | +1.023 |
| ZECUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 13 | -0.160 | -0.148 | 13 | +3.181 | +3.193 | 8 | -0.217 | -0.205 | 8 | +1.225 | +1.238 | 5 | +0.247 | +0.259 | 5 | +4.072 | +4.084 |
| ZECUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 9 | -0.160 | -0.249 | 9 | -0.730 | -0.991 | 5 | -0.211 | -0.006 | 5 | -2.072 | -1.435 | 4 | +0.345 | -0.326 | 4 | +7.795 | +4.300 |
| ZECUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 4 | -0.415 | -0.301 | 4 | +3.625 | +3.912 | 3 | -0.797 | -0.976 | 3 | +4.070 | +3.458 | 1 | -0.033 | +0.662 | 1 | -2.495 | +1.023 |
| ZECUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 15 | -0.160 | -0.148 | 15 | +0.879 | +0.891 | 10 | -0.186 | -0.173 | 10 | +0.423 | +0.436 | 5 | -0.099 | -0.087 | 5 | +6.304 | +6.316 |
| ZECUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 10 | -0.216 | -0.306 | 10 | +0.742 | +0.481 | 6 | -0.216 | -0.011 | 6 | -0.380 | +0.258 | 4 | -0.594 | -1.265 | 4 | +8.909 | +5.414 |
| ZECUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 5 | +0.304 | +0.418 | 5 | +2.752 | +3.038 | 4 | +0.518 | +0.338 | 4 | +3.411 | +2.799 | 1 | -0.033 | +0.662 | 1 | -2.495 | +1.023 |
| ZECUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 14 | -0.186 | -0.174 | 14 | +1.680 | +1.692 | 9 | -0.212 | -0.199 | 9 | -0.033 | -0.020 | 5 | -0.099 | -0.087 | 5 | +6.304 | +6.316 |
| ZECUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 9 | -0.222 | -0.311 | 9 | +0.604 | +0.342 | 5 | -0.221 | -0.016 | 5 | -0.729 | -0.091 | 4 | -0.594 | -1.265 | 4 | +8.909 | +5.414 |
| ZECUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 5 | +0.304 | +0.418 | 5 | +2.752 | +3.038 | 4 | +0.518 | +0.338 | 4 | +3.411 | +2.799 | 1 | -0.033 | +0.662 | 1 | -2.495 | +1.023 |
| ZECUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 14 | -0.191 | -0.178 | 14 | +0.497 | +0.509 | 8 | -0.275 | -0.263 | 8 | -0.099 | -0.086 | 6 | -0.065 | -0.053 | 6 | +7.168 | +7.180 |
| ZECUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 10 | -0.274 | -0.363 | 10 | +3.667 | +3.405 | 6 | -0.273 | -0.068 | 6 | -0.379 | +0.259 | 4 | -0.514 | -1.186 | 4 | +9.773 | +6.278 |
| ZECUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 4 | -0.076 | +0.038 | 4 | -1.332 | -1.046 | 2 | -2.177 | -2.356 | 2 | +1.793 | +1.180 | 2 | +1.144 | +1.839 | 2 | -4.821 | -1.303 |
| ZECUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 14 | -0.191 | -0.178 | 14 | +0.497 | +0.509 | 8 | -0.275 | -0.263 | 8 | -0.099 | -0.086 | 6 | -0.065 | -0.053 | 6 | +7.168 | +7.180 |
| ZECUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 10 | -0.274 | -0.363 | 10 | +3.667 | +3.405 | 6 | -0.273 | -0.068 | 6 | -0.379 | +0.259 | 4 | -0.514 | -1.186 | 4 | +9.773 | +6.278 |
| ZECUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 4 | -0.076 | +0.038 | 4 | -1.332 | -1.046 | 2 | -2.177 | -2.356 | 2 | +1.793 | +1.180 | 2 | +1.144 | +1.839 | 2 | -4.821 | -1.303 |
| ZECUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 15 | +0.269 | +0.281 | 15 | +0.023 | +0.036 | 10 | +0.156 | +0.169 | 10 | +0.832 | +0.845 | 5 | +0.298 | +0.310 | 5 | -2.872 | -2.861 |
| ZECUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 8 | -0.481 | -0.571 | 8 | +0.420 | +0.159 | 5 | -1.260 | -1.055 | 5 | -2.713 | -2.075 | 3 | +0.296 | -0.375 | 3 | +3.553 | +0.058 |
| ZECUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 7 | +0.269 | +0.383 | 7 | +0.023 | +0.310 | 5 | +0.269 | +0.089 | 5 | +1.641 | +1.029 | 2 | +0.084 | +0.779 | 2 | -6.350 | -2.831 |
| ZECUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 13 | +0.044 | +0.056 | 13 | +0.023 | +0.036 | 9 | +0.044 | +0.057 | 9 | +1.641 | +1.654 | 4 | -0.531 | -0.519 | 4 | -3.075 | -3.063 |
| ZECUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 7 | -1.261 | -1.350 | 7 | -2.714 | -2.976 | 5 | -1.260 | -1.055 | 5 | -2.713 | -2.075 | 2 | -1.051 | -1.723 | 2 | +0.999 | -2.496 |
| ZECUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 6 | +0.785 | +0.899 | 6 | +0.832 | +1.119 | 4 | +0.938 | +0.759 | 4 | +1.697 | +1.084 | 2 | +0.084 | +0.779 | 2 | -6.350 | -2.831 |
| ZECUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 13 | -0.935 | -0.923 | 13 | +0.862 | +0.874 | 9 | -0.795 | -0.782 | 9 | +1.641 | +1.654 | 4 | -1.414 | -1.403 | 4 | -1.559 | -1.547 |
| ZECUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 9 | -0.935 | -1.024 | 9 | -0.093 | -0.355 | 6 | -0.502 | -0.297 | 6 | -0.924 | -0.287 | 3 | -0.932 | -1.603 | 3 | -0.090 | -3.585 |
| ZECUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 4 | -2.559 | -2.445 | 4 | +3.944 | +4.231 | 3 | -0.795 | -0.974 | 3 | +4.711 | +4.099 | 1 | -43.637 | -42.942 | 1 | -113.667 | -110.148 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_first | record | ALL | both | 1789 | -0.086 | +0.048 | 1784 | -0.167 | -0.033 | 1146 | +0.010 | +0.132 | 1146 | -0.097 | +0.025 | 643 | -0.289 | -0.128 | 638 | -0.308 | -0.147 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_first | record | ALL | long | 954 | -0.087 | +0.009 | 951 | +0.117 | +0.046 | 622 | +0.098 | +0.171 | 622 | +0.377 | +0.249 | 332 | -0.485 | -0.342 | 329 | -0.400 | -0.363 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_first | record | ALL | short | 835 | -0.105 | +0.068 | 833 | -0.481 | -0.141 | 524 | -0.058 | +0.113 | 524 | -0.615 | -0.243 | 311 | -0.183 | -0.005 | 309 | -0.248 | +0.036 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 1508 | -0.066 | +0.068 | 1503 | -0.172 | -0.037 | 964 | +0.046 | +0.168 | 964 | -0.003 | +0.119 | 544 | -0.296 | -0.135 | 539 | -0.652 | -0.492 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 816 | -0.081 | +0.014 | 813 | +0.196 | +0.125 | 533 | +0.163 | +0.236 | 533 | +0.621 | +0.493 | 283 | -0.513 | -0.369 | 280 | -0.719 | -0.682 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 692 | -0.060 | +0.113 | 690 | -0.629 | -0.290 | 431 | -0.051 | +0.120 | 431 | -0.643 | -0.272 | 261 | -0.125 | +0.053 | 259 | -0.648 | -0.363 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_first | record | ALL | both | 1587 | -0.248 | -0.113 | 1585 | -0.237 | -0.103 | 1020 | -0.175 | -0.053 | 1020 | -0.133 | -0.011 | 567 | -0.342 | -0.181 | 565 | -0.471 | -0.310 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_first | record | ALL | long | 838 | -0.211 | -0.115 | 836 | -0.059 | -0.129 | 544 | -0.114 | -0.040 | 544 | +0.457 | +0.330 | 294 | -0.468 | -0.325 | 292 | -0.982 | -0.945 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_first | record | ALL | short | 749 | -0.277 | -0.104 | 749 | -0.439 | -0.100 | 476 | -0.304 | -0.134 | 476 | -0.729 | -0.357 | 273 | -0.259 | -0.080 | 273 | +0.043 | +0.328 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 1371 | -0.314 | -0.180 | 1369 | -0.303 | -0.169 | 889 | -0.221 | -0.099 | 889 | -0.110 | +0.012 | 482 | -0.491 | -0.330 | 480 | -0.678 | -0.518 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 731 | -0.264 | -0.169 | 729 | -0.144 | -0.215 | 481 | -0.119 | -0.046 | 481 | +0.523 | +0.395 | 250 | -0.687 | -0.544 | 248 | -1.198 | -1.161 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 640 | -0.360 | -0.187 | 640 | -0.564 | -0.224 | 408 | -0.368 | -0.198 | 408 | -0.834 | -0.462 | 232 | -0.319 | -0.141 | 232 | -0.015 | +0.269 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_first | record | ALL | both | 1295 | -0.104 | +0.030 | 1295 | -0.039 | +0.096 | 821 | +0.010 | +0.132 | 821 | +0.043 | +0.165 | 474 | -0.388 | -0.228 | 474 | -0.360 | -0.199 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_first | record | ALL | long | 674 | -0.143 | -0.047 | 674 | +0.157 | +0.086 | 429 | +0.005 | +0.079 | 429 | +0.832 | +0.705 | 245 | -0.545 | -0.401 | 245 | -0.776 | -0.739 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_first | record | ALL | short | 621 | -0.065 | +0.109 | 621 | -0.407 | -0.067 | 392 | +0.014 | +0.185 | 392 | -0.461 | -0.089 | 229 | -0.196 | -0.018 | 229 | +0.105 | +0.390 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 1141 | -0.105 | +0.029 | 1141 | -0.090 | +0.044 | 724 | +0.011 | +0.133 | 724 | -0.045 | +0.077 | 417 | -0.467 | -0.306 | 417 | -0.338 | -0.177 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 592 | -0.112 | -0.017 | 592 | +0.184 | +0.113 | 376 | +0.017 | +0.090 | 376 | +0.861 | +0.733 | 216 | -0.674 | -0.530 | 216 | -0.801 | -0.764 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 549 | -0.102 | +0.071 | 549 | -0.460 | -0.120 | 348 | -0.022 | +0.148 | 348 | -0.679 | -0.307 | 201 | -0.187 | -0.009 | 201 | +0.105 | +0.390 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_first | record | ALL | both | 1389 | -0.314 | -0.179 | 1388 | -0.410 | -0.275 | 903 | -0.355 | -0.233 | 903 | -0.359 | -0.237 | 486 | -0.276 | -0.116 | 485 | -0.526 | -0.365 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_first | record | ALL | long | 759 | -0.328 | -0.232 | 758 | -0.102 | -0.173 | 504 | -0.280 | -0.207 | 504 | +0.217 | +0.090 | 255 | -0.386 | -0.243 | 254 | -0.683 | -0.646 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_first | record | ALL | short | 630 | -0.298 | -0.124 | 630 | -0.734 | -0.394 | 399 | -0.422 | -0.251 | 399 | -0.856 | -0.484 | 231 | -0.144 | +0.035 | 231 | -0.348 | -0.063 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 1309 | -0.289 | -0.154 | 1308 | -0.380 | -0.245 | 852 | -0.304 | -0.183 | 852 | -0.298 | -0.176 | 457 | -0.283 | -0.123 | 456 | -0.528 | -0.367 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 710 | -0.248 | -0.153 | 709 | -0.185 | -0.255 | 475 | -0.218 | -0.145 | 475 | +0.330 | +0.202 | 235 | -0.380 | -0.236 | 234 | -1.011 | -0.974 |
| POOLED:CLASSIC5 | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 599 | -0.320 | -0.146 | 599 | -0.585 | -0.245 | 377 | -0.418 | -0.248 | 377 | -0.845 | -0.473 | 222 | -0.165 | +0.013 | 222 | -0.105 | +0.179 |
| POOLED:CLASSIC5 | 1h | calibrated | SFP_harden | record | ALL | both | 2571 | -0.103 | +0.031 | 2567 | -0.007 | +0.128 | 1626 | +0.013 | +0.135 | 1626 | +0.162 | +0.284 | 945 | -0.309 | -0.148 | 941 | -0.387 | -0.226 |
| POOLED:CLASSIC5 | 1h | calibrated | SFP_harden | record | ALL | long | 1257 | -0.040 | +0.056 | 1257 | -0.164 | -0.235 | 763 | +0.159 | +0.232 | 763 | +0.154 | +0.026 | 494 | -0.408 | -0.265 | 494 | -0.820 | -0.783 |
| POOLED:CLASSIC5 | 1h | calibrated | SFP_harden | record | ALL | short | 1314 | -0.130 | +0.043 | 1310 | +0.152 | +0.492 | 863 | -0.094 | +0.076 | 863 | +0.162 | +0.534 | 451 | -0.228 | -0.050 | 447 | +0.204 | +0.488 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_first | record | ALL | both | 450 | +0.129 | +0.194 | 446 | +0.281 | +0.345 | 287 | +0.103 | +0.161 | 287 | +0.441 | +0.499 | 163 | +0.137 | +0.215 | 159 | -0.069 | +0.009 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_first | record | ALL | long | 230 | +0.025 | +0.008 | 227 | -0.053 | -0.192 | 153 | +0.101 | +0.058 | 153 | -0.154 | -0.338 | 77 | -0.407 | -0.371 | 74 | +0.020 | -0.008 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_first | record | ALL | short | 220 | +0.277 | +0.424 | 219 | +0.431 | +0.699 | 134 | +0.151 | +0.310 | 134 | +1.037 | +1.337 | 86 | +0.393 | +0.514 | 85 | -0.302 | -0.118 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 392 | +0.245 | +0.310 | 388 | +0.398 | +0.462 | 250 | +0.206 | +0.264 | 250 | +0.565 | +0.623 | 142 | +0.334 | +0.412 | 138 | +0.152 | +0.230 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 208 | +0.065 | +0.047 | 205 | +0.269 | +0.130 | 134 | +0.109 | +0.067 | 134 | +0.233 | +0.050 | 74 | -0.281 | -0.245 | 71 | +0.275 | +0.246 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 184 | +0.358 | +0.505 | 183 | +0.449 | +0.717 | 116 | +0.283 | +0.442 | 116 | +1.065 | +1.365 | 68 | +0.705 | +0.825 | 67 | -0.308 | -0.124 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_first | record | ALL | both | 403 | +0.179 | +0.244 | 398 | +0.130 | +0.195 | 257 | +0.117 | +0.175 | 257 | -0.286 | -0.228 | 146 | +0.322 | +0.400 | 141 | +0.277 | +0.355 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_first | record | ALL | long | 212 | +0.016 | -0.001 | 209 | -0.298 | -0.437 | 143 | +0.056 | +0.013 | 143 | -0.314 | -0.498 | 69 | -0.213 | -0.177 | 66 | -0.100 | -0.129 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_first | record | ALL | short | 191 | +0.278 | +0.424 | 189 | +0.447 | +0.715 | 114 | +0.155 | +0.314 | 114 | +0.212 | +0.511 | 77 | +0.667 | +0.787 | 75 | +0.971 | +1.156 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 358 | +0.208 | +0.272 | 353 | +0.289 | +0.353 | 225 | +0.239 | +0.297 | 225 | +0.224 | +0.282 | 133 | +0.037 | +0.115 | 128 | +0.329 | +0.407 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 194 | +0.047 | +0.030 | 191 | +0.126 | -0.013 | 128 | +0.298 | +0.255 | 128 | -0.024 | -0.207 | 66 | -0.185 | -0.149 | 63 | +0.113 | +0.084 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 164 | +0.287 | +0.433 | 162 | +0.451 | +0.718 | 97 | +0.174 | +0.333 | 97 | +0.370 | +0.670 | 67 | +0.644 | +0.765 | 65 | +0.971 | +1.156 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_first | record | ALL | both | 333 | +0.010 | +0.074 | 331 | -0.277 | -0.213 | 214 | -0.233 | -0.175 | 214 | -0.504 | -0.446 | 119 | +0.230 | +0.308 | 117 | -0.108 | -0.030 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_first | record | ALL | long | 178 | +0.017 | -0.001 | 176 | -0.632 | -0.771 | 116 | +0.318 | +0.276 | 116 | -0.808 | -0.992 | 62 | -0.118 | -0.082 | 60 | -0.202 | -0.231 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_first | record | ALL | short | 155 | -0.050 | +0.097 | 155 | -0.039 | +0.229 | 98 | -0.698 | -0.539 | 98 | -0.189 | +0.111 | 57 | +0.781 | +0.902 | 57 | +0.767 | +0.951 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 295 | +0.030 | +0.094 | 293 | -0.136 | -0.072 | 193 | -0.048 | +0.010 | 193 | -0.273 | -0.215 | 102 | +0.179 | +0.257 | 100 | -0.090 | -0.012 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 160 | +0.100 | +0.082 | 158 | -0.296 | -0.435 | 106 | +0.482 | +0.439 | 106 | -0.408 | -0.592 | 54 | -0.116 | -0.080 | 52 | -0.206 | -0.235 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 135 | -0.062 | +0.084 | 135 | +0.430 | +0.698 | 87 | -0.717 | -0.558 | 87 | -0.140 | +0.160 | 48 | +0.774 | +0.894 | 48 | +0.914 | +1.098 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_first | record | ALL | both | 310 | +0.058 | +0.122 | 309 | +0.493 | +0.557 | 203 | +0.200 | +0.258 | 203 | +0.501 | +0.559 | 107 | -0.237 | -0.159 | 106 | +0.777 | +0.854 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_first | record | ALL | long | 153 | +0.439 | +0.421 | 153 | +0.831 | +0.692 | 104 | +0.520 | +0.477 | 104 | +0.739 | +0.555 | 49 | -0.006 | +0.030 | 49 | +0.815 | +0.786 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_first | record | ALL | short | 157 | -0.228 | -0.082 | 156 | +0.082 | +0.350 | 99 | -0.195 | -0.036 | 99 | +0.180 | +0.480 | 58 | -0.346 | -0.226 | 57 | -0.017 | +0.168 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 287 | +0.017 | +0.082 | 286 | +0.350 | +0.415 | 187 | +0.025 | +0.083 | 187 | +0.498 | +0.556 | 100 | -0.107 | -0.029 | 99 | +0.292 | +0.369 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 144 | +0.254 | +0.236 | 144 | +0.756 | +0.617 | 98 | +0.330 | +0.287 | 98 | +0.526 | +0.342 | 46 | +0.171 | +0.207 | 46 | +2.020 | +1.991 |
| POOLED:CLASSIC5 | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 143 | -0.390 | -0.244 | 142 | -0.153 | +0.115 | 89 | -0.388 | -0.229 | 89 | +0.184 | +0.484 | 54 | -0.347 | -0.227 | 53 | -0.708 | -0.524 |
| POOLED:CLASSIC5 | 4h | calibrated | SFP_harden | record | ALL | both | 627 | +0.103 | +0.167 | 625 | +0.228 | +0.292 | 396 | -0.013 | +0.045 | 396 | -0.454 | -0.396 | 231 | +0.282 | +0.360 | 229 | +1.123 | +1.200 |
| POOLED:CLASSIC5 | 4h | calibrated | SFP_harden | record | ALL | long | 315 | +0.240 | +0.222 | 313 | +0.374 | +0.234 | 190 | +0.281 | +0.238 | 190 | -0.586 | -0.769 | 125 | +0.084 | +0.119 | 123 | +2.015 | +1.986 |
| POOLED:CLASSIC5 | 4h | calibrated | SFP_harden | record | ALL | short | 312 | -0.024 | +0.122 | 312 | +0.011 | +0.279 | 206 | -0.163 | -0.004 | 206 | -0.141 | +0.159 | 106 | +0.647 | +0.767 | 106 | +0.633 | +0.817 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_first | record | ALL | both | 137 | -0.052 | -0.017 | 136 | +0.259 | +0.293 | 87 | +0.352 | +0.384 | 87 | +0.565 | +0.597 | 50 | -0.437 | -0.394 | 49 | -0.429 | -0.387 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_first | record | ALL | long | 79 | +0.155 | +0.050 | 79 | +1.306 | +0.710 | 57 | +0.411 | +0.295 | 57 | +2.497 | +1.612 | 22 | -0.541 | -0.619 | 22 | -0.363 | -0.419 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_first | record | ALL | short | 58 | -0.207 | -0.033 | 57 | -0.844 | -0.179 | 30 | +0.200 | +0.379 | 30 | -0.460 | +0.489 | 28 | -0.343 | -0.180 | 27 | -0.848 | -0.709 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_oneshot | record | ALL | both | 115 | +0.180 | +0.215 | 115 | -0.211 | -0.176 | 74 | +0.469 | +0.501 | 74 | +0.749 | +0.781 | 41 | -0.521 | -0.479 | 41 | -1.120 | -1.079 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_oneshot | record | ALL | long | 66 | +0.416 | +0.312 | 66 | +1.546 | +0.950 | 48 | +0.527 | +0.411 | 48 | +2.710 | +1.825 | 18 | -0.541 | -0.619 | 18 | -0.486 | -0.543 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap89_oneshot | record | ALL | short | 49 | -0.179 | -0.005 | 49 | -1.233 | -0.567 | 26 | +0.246 | +0.425 | 26 | -1.207 | -0.258 | 23 | -0.344 | -0.181 | 23 | -2.991 | -2.852 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_first | record | ALL | both | 118 | +0.164 | +0.199 | 117 | -0.416 | -0.382 | 73 | +0.069 | +0.101 | 73 | -0.287 | -0.255 | 45 | +0.329 | +0.372 | 44 | -0.477 | -0.435 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_first | record | ALL | long | 70 | +0.090 | -0.014 | 70 | +0.422 | -0.174 | 48 | -0.009 | -0.124 | 48 | +1.335 | +0.450 | 22 | +0.795 | +0.718 | 22 | -1.563 | -1.620 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_first | record | ALL | short | 48 | +0.222 | +0.397 | 47 | -0.552 | +0.113 | 25 | +0.257 | +0.437 | 25 | -2.849 | -1.900 | 23 | +0.158 | +0.321 | 22 | +0.208 | +0.347 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_oneshot | record | ALL | both | 101 | +0.305 | +0.340 | 101 | +0.213 | +0.247 | 63 | +0.281 | +0.313 | 63 | +0.218 | +0.250 | 38 | +0.379 | +0.422 | 38 | -0.110 | -0.068 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_oneshot | record | ALL | long | 58 | +0.390 | +0.285 | 58 | +1.340 | +0.744 | 39 | +0.377 | +0.262 | 39 | +4.222 | +3.337 | 19 | +0.434 | +0.356 | 19 | -0.430 | -0.486 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap127_oneshot | record | ALL | short | 43 | +0.272 | +0.446 | 43 | -0.666 | -0.000 | 24 | +0.167 | +0.346 | 24 | -2.873 | -1.924 | 19 | +0.327 | +0.490 | 19 | +0.212 | +0.352 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_first | record | ALL | both | 99 | +0.147 | +0.182 | 98 | -0.249 | -0.214 | 59 | +0.286 | +0.318 | 59 | -0.866 | -0.834 | 40 | +0.087 | +0.130 | 39 | -0.223 | -0.182 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_first | record | ALL | long | 54 | +0.183 | +0.079 | 54 | -1.020 | -1.616 | 34 | +0.455 | +0.340 | 34 | -0.175 | -1.061 | 20 | -0.112 | -0.190 | 20 | -1.550 | -1.606 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_first | record | ALL | short | 45 | +0.137 | +0.311 | 44 | +0.010 | +0.676 | 25 | -0.086 | +0.093 | 25 | -1.235 | -0.286 | 20 | +0.223 | +0.386 | 19 | +0.071 | +0.210 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_oneshot | record | ALL | both | 86 | +0.301 | +0.336 | 86 | -0.754 | -0.719 | 55 | +0.286 | +0.318 | 55 | -1.178 | -1.146 | 31 | +0.309 | +0.352 | 31 | -0.295 | -0.253 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_oneshot | record | ALL | long | 49 | +0.411 | +0.306 | 49 | -1.176 | -1.772 | 32 | +0.455 | +0.340 | 32 | -0.175 | -1.061 | 17 | -0.105 | -0.183 | 17 | -1.611 | -1.667 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_tap200_oneshot | record | ALL | short | 37 | +0.272 | +0.447 | 37 | -0.223 | +0.442 | 23 | -0.086 | +0.093 | 23 | -2.100 | -1.151 | 14 | +0.810 | +0.972 | 14 | +0.010 | +0.150 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_first | record | ALL | both | 100 | +0.274 | +0.309 | 100 | -0.635 | -0.600 | 63 | +0.346 | +0.377 | 63 | -0.359 | -0.327 | 37 | +0.089 | +0.132 | 37 | -1.111 | -1.070 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_first | record | ALL | long | 58 | +0.215 | +0.110 | 58 | +0.004 | -0.592 | 40 | +0.239 | +0.124 | 40 | +0.205 | -0.680 | 18 | +0.076 | -0.002 | 18 | -1.026 | -1.083 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_first | record | ALL | short | 42 | +0.543 | +0.717 | 42 | -1.290 | -0.624 | 23 | +0.694 | +0.873 | 23 | -1.823 | -0.874 | 19 | +0.102 | +0.265 | 19 | -1.098 | -0.959 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_oneshot | record | ALL | both | 104 | +0.224 | +0.259 | 104 | -0.538 | -0.503 | 66 | +0.275 | +0.307 | 66 | -0.219 | -0.187 | 38 | -0.031 | +0.012 | 38 | -1.080 | -1.038 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_oneshot | record | ALL | long | 58 | +0.265 | +0.161 | 58 | +0.004 | -0.592 | 41 | +0.288 | +0.173 | 41 | +0.319 | -0.566 | 17 | -0.055 | -0.132 | 17 | -1.166 | -1.223 |
| POOLED:CLASSIC5 | 12h | calibrated | BRK_mem_oneshot | record | ALL | short | 46 | +0.042 | +0.216 | 46 | -1.075 | -0.410 | 25 | +0.219 | +0.398 | 25 | -1.737 | -0.788 | 21 | -0.007 | +0.155 | 21 | -1.041 | -0.902 |
| POOLED:CLASSIC5 | 12h | calibrated | SFP_harden | record | ALL | both | 197 | -0.028 | +0.007 | 197 | +0.854 | +0.889 | 105 | -0.186 | -0.154 | 105 | +1.149 | +1.181 | 92 | +0.088 | +0.131 | 92 | +0.558 | +0.600 |
| POOLED:CLASSIC5 | 12h | calibrated | SFP_harden | record | ALL | long | 90 | +0.168 | +0.064 | 90 | +1.413 | +0.817 | 47 | +0.143 | +0.028 | 47 | +0.745 | -0.140 | 43 | +0.259 | +0.182 | 43 | +1.644 | +1.587 |
| POOLED:CLASSIC5 | 12h | calibrated | SFP_harden | record | ALL | short | 107 | -0.414 | -0.240 | 107 | +0.661 | +1.326 | 58 | -0.738 | -0.559 | 58 | +1.278 | +2.227 | 49 | -0.029 | +0.134 | 49 | +0.253 | +0.393 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_first | record | ALL | both | 71 | -0.063 | -0.039 | 67 | -0.738 | -0.714 | 42 | +0.017 | +0.038 | 42 | +1.843 | +1.864 | 29 | -0.248 | -0.219 | 25 | -1.455 | -1.427 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_first | record | ALL | long | 43 | +0.088 | +0.035 | 41 | -0.745 | -1.217 | 28 | +0.145 | +0.049 | 28 | +0.739 | -0.033 | 15 | -0.697 | -0.656 | 13 | -1.470 | -1.139 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_first | record | ALL | short | 28 | -0.154 | -0.052 | 26 | +1.496 | +2.015 | 14 | -0.428 | -0.290 | 14 | +3.504 | +4.319 | 14 | -0.148 | -0.132 | 12 | -1.232 | -1.509 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 64 | -0.056 | -0.032 | 60 | -0.771 | -0.747 | 37 | -0.059 | -0.037 | 37 | +0.450 | +0.471 | 27 | -0.052 | -0.024 | 23 | -1.455 | -1.427 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 40 | +0.088 | +0.035 | 38 | -0.770 | -1.242 | 26 | +0.145 | +0.049 | 26 | -0.143 | -0.916 | 14 | -0.309 | -0.268 | 12 | -1.555 | -1.224 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 24 | -0.154 | -0.052 | 22 | -0.432 | +0.087 | 11 | -0.800 | -0.662 | 11 | +2.679 | +3.494 | 13 | -0.050 | -0.034 | 11 | -1.184 | -1.460 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_first | record | ALL | both | 60 | -0.069 | -0.045 | 59 | -0.043 | -0.019 | 37 | +0.299 | +0.321 | 37 | +0.364 | +0.385 | 23 | -0.560 | -0.531 | 22 | -2.075 | -2.048 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_first | record | ALL | long | 40 | -0.012 | -0.065 | 39 | -0.119 | -0.591 | 27 | +0.203 | +0.107 | 27 | -0.043 | -0.815 | 13 | -0.697 | -0.657 | 12 | -1.597 | -1.266 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_first | record | ALL | short | 20 | -0.068 | +0.033 | 20 | +1.387 | +1.905 | 10 | +0.516 | +0.655 | 10 | +3.409 | +4.225 | 10 | -0.326 | -0.310 | 10 | -2.849 | -3.126 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 54 | -0.078 | -0.054 | 53 | +0.042 | +0.066 | 35 | +0.203 | +0.224 | 35 | +0.044 | +0.066 | 19 | -0.561 | -0.533 | 18 | -0.620 | -0.593 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 38 | -0.012 | -0.065 | 37 | -0.119 | -0.591 | 26 | +0.148 | +0.052 | 26 | -0.079 | -0.851 | 12 | -0.410 | -0.370 | 11 | -1.555 | -1.224 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 16 | -0.297 | -0.196 | 16 | +2.596 | +3.115 | 9 | +0.302 | +0.440 | 9 | +2.750 | +3.565 | 7 | -0.558 | -0.542 | 7 | +0.315 | +0.038 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_first | record | ALL | both | 51 | -0.238 | -0.215 | 51 | -1.631 | -1.607 | 29 | -0.176 | -0.155 | 29 | -0.049 | -0.028 | 22 | -0.625 | -0.597 | 22 | -4.462 | -4.434 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_first | record | ALL | long | 37 | -0.345 | -0.398 | 37 | -0.071 | -0.543 | 24 | -0.172 | -0.267 | 24 | +0.484 | -0.289 | 13 | -1.113 | -1.072 | 13 | -4.413 | -4.081 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_first | record | ALL | short | 14 | -0.078 | +0.024 | 14 | -4.259 | -3.740 | 5 | -1.222 | -1.083 | 5 | -0.192 | +0.624 | 9 | +0.088 | +0.104 | 9 | -7.160 | -7.437 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 41 | -0.309 | -0.285 | 41 | -0.183 | -0.160 | 26 | -0.209 | -0.187 | 26 | -0.060 | -0.038 | 15 | -0.954 | -0.926 | 15 | -2.426 | -2.398 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 33 | -0.308 | -0.361 | 33 | -0.068 | -0.540 | 22 | -0.175 | -0.271 | 22 | +0.480 | -0.293 | 11 | -1.105 | -1.064 | 11 | -2.183 | -1.851 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 8 | -0.683 | -0.582 | 8 | -2.251 | -1.733 | 4 | -2.014 | -1.875 | 4 | -1.132 | -0.316 | 4 | +1.114 | +1.130 | 4 | -2.478 | -2.754 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_first | record | ALL | both | 56 | +0.352 | +0.376 | 53 | -1.357 | -1.333 | 31 | +0.264 | +0.285 | 31 | +0.464 | +0.486 | 25 | +0.396 | +0.424 | 22 | -3.437 | -3.410 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_first | record | ALL | long | 29 | +0.922 | +0.869 | 28 | -0.143 | -0.615 | 19 | +1.171 | +1.075 | 19 | +1.126 | +0.353 | 10 | +0.044 | +0.085 | 9 | -2.190 | -1.859 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_first | record | ALL | short | 27 | +0.345 | +0.447 | 25 | -3.337 | -2.818 | 12 | -0.196 | -0.058 | 12 | -1.570 | -0.755 | 15 | +0.683 | +0.699 | 13 | -4.315 | -4.592 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 53 | +0.400 | +0.424 | 50 | -1.470 | -1.446 | 32 | +0.222 | +0.244 | 32 | +0.240 | +0.261 | 21 | +0.671 | +0.700 | 18 | -3.961 | -3.933 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 29 | +0.290 | +0.236 | 28 | -0.347 | -0.818 | 20 | +1.049 | +0.954 | 20 | +0.791 | +0.018 | 9 | -0.187 | -0.146 | 8 | -2.543 | -2.212 |
| POOLED:CLASSIC5 | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 24 | +0.495 | +0.596 | 22 | -3.601 | -3.082 | 12 | -0.193 | -0.055 | 12 | -1.656 | -0.841 | 12 | +1.077 | +1.092 | 10 | -5.515 | -5.791 |
| POOLED:CLASSIC5 | 1d | calibrated | SFP_harden | record | ALL | both | 77 | -0.781 | -0.757 | 73 | +0.999 | +1.023 | 40 | -0.789 | -0.768 | 40 | +1.600 | +1.622 | 37 | -0.783 | -0.754 | 33 | -0.112 | -0.084 |
| POOLED:CLASSIC5 | 1d | calibrated | SFP_harden | record | ALL | long | 46 | -0.280 | -0.333 | 45 | -0.104 | -0.576 | 23 | -0.268 | -0.364 | 23 | +1.568 | +0.795 | 23 | -0.504 | -0.463 | 22 | -3.037 | -2.706 |
| POOLED:CLASSIC5 | 1d | calibrated | SFP_harden | record | ALL | short | 31 | -1.509 | -1.408 | 28 | +3.035 | +3.553 | 17 | -1.850 | -1.712 | 17 | +2.393 | +3.208 | 14 | -1.397 | -1.381 | 11 | +3.800 | +3.523 |
| ENAUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 157 | -0.241 | -0.189 | 156 | -0.035 | +0.017 | 8 | +0.031 | +0.077 | 8 | +1.342 | +1.388 | 149 | -0.273 | -0.220 | 148 | -0.035 | +0.018 |
| ENAUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 72 | -0.786 | -0.477 | 71 | -0.953 | +0.009 | 4 | -0.036 | +0.315 | 4 | -0.877 | +1.004 | 68 | -0.827 | -0.522 | 67 | -0.953 | -0.088 |
| ENAUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 85 | +0.026 | -0.178 | 85 | +1.005 | +0.148 | 4 | +0.846 | +0.588 | 4 | +1.342 | -0.447 | 81 | +0.026 | -0.172 | 81 | +1.005 | +0.246 |
| ENAUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 140 | -0.293 | -0.241 | 139 | -0.332 | -0.279 | 7 | +0.252 | +0.299 | 7 | +3.020 | +3.067 | 133 | -0.370 | -0.317 | 132 | -0.629 | -0.576 |
| ENAUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 68 | -0.786 | -0.477 | 67 | -1.058 | -0.096 | 4 | -0.036 | +0.315 | 4 | -0.877 | +1.004 | 64 | -0.827 | -0.523 | 63 | -1.058 | -0.193 |
| ENAUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 72 | -0.006 | -0.210 | 72 | +0.211 | -0.646 | 3 | +1.882 | +1.624 | 3 | +3.020 | +1.231 | 69 | -0.011 | -0.209 | 69 | +0.181 | -0.578 |
| ENAUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 137 | -0.244 | -0.191 | 136 | +0.616 | +0.668 | 7 | -0.903 | -0.856 | 7 | +0.850 | +0.896 | 130 | -0.173 | -0.120 | 129 | +0.555 | +0.608 |
| ENAUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 66 | -0.379 | -0.070 | 65 | -0.328 | +0.634 | 4 | +0.003 | +0.353 | 4 | -3.423 | -1.542 | 62 | -0.378 | -0.074 | 61 | -0.327 | +0.537 |
| ENAUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 71 | -0.045 | -0.250 | 71 | +1.193 | +0.336 | 3 | -1.550 | -1.808 | 3 | +8.716 | +6.926 | 68 | -0.008 | -0.207 | 68 | +1.170 | +0.411 |
| ENAUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 120 | -0.338 | -0.285 | 119 | +0.148 | +0.201 | 7 | -0.903 | -0.856 | 7 | +0.850 | +0.896 | 113 | -0.306 | -0.253 | 112 | +0.104 | +0.157 |
| ENAUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 58 | -0.461 | -0.152 | 57 | -0.796 | +0.166 | 4 | +0.003 | +0.353 | 4 | -3.423 | -1.542 | 54 | -0.460 | -0.156 | 53 | -0.796 | +0.069 |
| ENAUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 62 | -0.187 | -0.391 | 62 | +1.234 | +0.377 | 3 | -1.550 | -1.808 | 3 | +8.716 | +6.926 | 59 | -0.103 | -0.301 | 59 | +1.147 | +0.388 |
| ENAUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 103 | -0.333 | -0.281 | 103 | +0.479 | +0.532 | 4 | -3.459 | -3.413 | 4 | -6.669 | -6.622 | 99 | -0.306 | -0.253 | 99 | +0.511 | +0.565 |
| ENAUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 56 | -0.616 | -0.307 | 56 | -1.235 | -0.273 | 4 | -3.459 | -3.108 | 4 | -6.669 | -4.787 | 52 | -0.535 | -0.231 | 52 | -1.235 | -0.370 |
| ENAUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 47 | +0.627 | +0.423 | 47 | +1.595 | +0.738 | 0 | — | — | 0 | — | — | 47 | +0.627 | +0.429 | 47 | +1.595 | +0.837 |
| ENAUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 92 | -0.340 | -0.288 | 92 | +0.169 | +0.221 | 4 | -3.459 | -3.413 | 4 | -6.669 | -6.622 | 88 | -0.319 | -0.266 | 88 | +0.250 | +0.303 |
| ENAUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 54 | -0.758 | -0.449 | 54 | -1.972 | -1.010 | 4 | -3.459 | -3.108 | 4 | -6.669 | -4.787 | 50 | -0.615 | -0.311 | 50 | -1.971 | -1.107 |
| ENAUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 38 | +0.629 | +0.425 | 38 | +1.560 | +0.703 | 0 | — | — | 0 | — | — | 38 | +0.629 | +0.431 | 38 | +1.560 | +0.802 |
| ENAUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 125 | +0.158 | +0.210 | 124 | +0.373 | +0.425 | 5 | +0.824 | +0.870 | 5 | +3.411 | +3.457 | 120 | +0.134 | +0.187 | 119 | +0.294 | +0.347 |
| ENAUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 59 | +0.396 | +0.705 | 58 | -0.911 | +0.051 | 2 | -2.387 | -2.037 | 2 | -2.167 | -0.286 | 57 | +0.769 | +1.073 | 56 | -0.910 | -0.045 |
| ENAUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 66 | -0.092 | -0.296 | 66 | +0.698 | -0.159 | 3 | +2.698 | +2.440 | 3 | +3.422 | +1.633 | 63 | -0.245 | -0.443 | 63 | +0.592 | -0.167 |
| ENAUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 130 | +0.190 | +0.242 | 129 | +0.323 | +0.375 | 5 | +0.824 | +0.870 | 5 | +3.411 | +3.457 | 125 | +0.161 | +0.214 | 124 | +0.241 | +0.294 |
| ENAUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 65 | -0.150 | +0.159 | 64 | -1.064 | -0.102 | 2 | -2.387 | -2.037 | 2 | -2.167 | -0.286 | 63 | +0.115 | +0.419 | 62 | -1.063 | -0.198 |
| ENAUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 65 | +0.267 | +0.063 | 65 | +0.695 | -0.162 | 3 | +2.698 | +2.440 | 3 | +3.422 | +1.633 | 62 | +0.220 | +0.022 | 62 | +0.393 | -0.366 |
| ENAUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 305 | -0.278 | -0.225 | 304 | -0.449 | -0.396 | 24 | +0.633 | +0.679 | 24 | +1.173 | +1.219 | 281 | -0.390 | -0.337 | 280 | -0.638 | -0.585 |
| ENAUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 165 | -0.488 | -0.179 | 164 | -1.028 | -0.065 | 11 | +0.696 | +1.046 | 11 | +4.953 | +6.834 | 154 | -0.584 | -0.279 | 153 | -1.118 | -0.253 |
| ENAUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 140 | -0.054 | -0.259 | 140 | +0.420 | -0.437 | 13 | -0.002 | -0.260 | 13 | +0.901 | -0.888 | 127 | -0.060 | -0.258 | 127 | +0.349 | -0.409 |
| ENAUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 26 | +0.316 | +0.341 | 25 | +3.015 | +3.040 | 2 | -1.786 | -1.764 | 2 | +3.166 | +3.189 | 24 | +0.612 | +0.638 | 23 | +3.015 | +3.040 |
| ENAUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 9 | -0.443 | -0.021 | 8 | +3.997 | +5.259 | 0 | — | — | 0 | — | — | 9 | -0.443 | -0.039 | 8 | +3.997 | +5.026 |
| ENAUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 17 | +0.957 | +0.586 | 17 | +2.479 | +1.267 | 2 | -1.786 | -2.393 | 2 | +3.166 | +0.341 | 15 | +0.976 | +0.623 | 15 | +1.041 | +0.064 |
| ENAUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 18 | -0.002 | +0.023 | 17 | +3.628 | +3.653 | 1 | -0.840 | -0.817 | 1 | +2.488 | +2.510 | 17 | +0.441 | +0.466 | 16 | +3.763 | +3.789 |
| ENAUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | -0.681 | -0.260 | 7 | +3.631 | +4.893 | 0 | — | — | 0 | — | — | 8 | -0.681 | -0.278 | 7 | +3.631 | +4.660 |
| ENAUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 10 | +1.117 | +0.746 | 10 | +3.188 | +1.976 | 1 | -0.840 | -1.446 | 1 | +2.488 | -0.338 | 9 | +1.259 | +0.907 | 9 | +3.897 | +2.920 |
| ENAUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 24 | -0.927 | -0.902 | 23 | +2.120 | +2.145 | 3 | -1.370 | -1.348 | 3 | +0.224 | +0.247 | 21 | -0.546 | -0.521 | 20 | +2.406 | +2.431 |
| ENAUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 8 | -1.130 | -0.709 | 7 | +0.892 | +2.154 | 1 | -3.727 | -3.075 | 1 | -7.782 | -4.912 | 7 | -1.056 | -0.653 | 6 | +2.819 | +3.848 |
| ENAUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 16 | -0.719 | -1.091 | 16 | +2.406 | +1.194 | 2 | -1.195 | -1.802 | 2 | +2.348 | -0.477 | 14 | -0.475 | -0.827 | 14 | +2.406 | +1.428 |
| ENAUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 20 | -0.474 | -0.449 | 19 | +2.120 | +2.146 | 2 | -2.372 | -2.349 | 2 | -3.779 | -3.757 | 18 | -0.246 | -0.220 | 17 | +2.692 | +2.717 |
| ENAUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | -1.053 | -0.631 | 6 | +1.115 | +2.378 | 1 | -3.727 | -3.075 | 1 | -7.782 | -4.912 | 6 | -0.487 | -0.083 | 5 | +4.751 | +5.780 |
| ENAUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 13 | -0.403 | -0.774 | 13 | +2.120 | +0.908 | 1 | -1.017 | -1.624 | 1 | +0.224 | -2.601 | 12 | -0.246 | -0.598 | 12 | +2.406 | +1.428 |
| ENAUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 23 | -0.120 | -0.095 | 22 | +0.878 | +0.903 | 3 | -2.094 | -2.071 | 3 | +0.224 | +0.247 | 20 | -0.080 | -0.055 | 19 | +1.484 | +1.510 |
| ENAUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 9 | -0.703 | -0.282 | 8 | -0.719 | +0.543 | 1 | -3.727 | -3.075 | 1 | -7.782 | -4.912 | 8 | -0.389 | +0.015 | 7 | +0.221 | +1.250 |
| ENAUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 14 | -0.104 | -0.475 | 14 | +2.462 | +1.250 | 2 | -1.555 | -2.162 | 2 | +0.337 | -2.488 | 12 | -0.022 | -0.374 | 12 | +4.078 | +3.101 |
| ENAUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 19 | -0.089 | -0.064 | 18 | +2.550 | +2.575 | 2 | -2.372 | -2.349 | 2 | -3.779 | -3.757 | 17 | -0.073 | -0.047 | 16 | +3.899 | +3.925 |
| ENAUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 9 | -0.703 | -0.282 | 8 | -0.719 | +0.543 | 1 | -3.727 | -3.075 | 1 | -7.782 | -4.912 | 8 | -0.389 | +0.015 | 7 | +0.221 | +1.250 |
| ENAUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 10 | -0.022 | -0.394 | 10 | +4.904 | +3.692 | 1 | -1.017 | -1.624 | 1 | +0.224 | -2.601 | 9 | +0.044 | -0.309 | 9 | +5.270 | +4.293 |
| ENAUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 18 | -0.977 | -0.952 | 18 | +1.654 | +1.679 | 4 | -2.730 | -2.707 | 4 | -3.766 | -3.743 | 14 | -0.602 | -0.576 | 14 | +2.619 | +2.645 |
| ENAUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 5 | -1.890 | -1.468 | 5 | -1.576 | -0.313 | 1 | -2.958 | -2.306 | 1 | -9.087 | -6.217 | 4 | -1.358 | -0.954 | 4 | -1.393 | -0.364 |
| ENAUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 13 | -0.351 | -0.723 | 13 | +2.741 | +1.529 | 3 | -2.502 | -3.109 | 3 | +0.811 | -2.014 | 10 | -0.100 | -0.453 | 10 | +2.960 | +1.982 |
| ENAUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 14 | -1.329 | -1.303 | 14 | +0.766 | +0.791 | 3 | -2.958 | -2.935 | 3 | -8.343 | -8.320 | 11 | -0.825 | -0.799 | 11 | +2.741 | +2.766 |
| ENAUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 5 | -1.890 | -1.468 | 5 | -1.576 | -0.313 | 1 | -2.958 | -2.306 | 1 | -9.087 | -6.217 | 4 | -1.358 | -0.954 | 4 | -1.393 | -0.364 |
| ENAUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 9 | -1.130 | -1.502 | 9 | +3.178 | +1.966 | 2 | -3.306 | -3.913 | 2 | -1.069 | -3.895 | 7 | +0.151 | -0.201 | 7 | +3.178 | +2.200 |
| ENAUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 34 | +0.236 | +0.261 | 33 | -0.113 | -0.088 | 3 | -3.058 | -3.035 | 3 | -7.720 | -7.698 | 31 | +0.609 | +0.634 | 30 | +0.653 | +0.679 |
| ENAUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 19 | -0.549 | -0.127 | 18 | -1.349 | -0.087 | 3 | -3.058 | -2.406 | 3 | -7.720 | -4.850 | 16 | -0.103 | +0.301 | 15 | -1.048 | -0.019 |
| ENAUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 15 | +1.551 | +1.179 | 15 | +2.197 | +0.985 | 0 | — | — | 0 | — | — | 15 | +1.551 | +1.198 | 15 | +2.197 | +1.220 |
| ENAUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 5 | -2.133 | -2.124 | 5 | -4.517 | -4.508 | 0 | — | — | 0 | — | — | 5 | -2.133 | -2.124 | 5 | -4.517 | -4.508 |
| ENAUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 2 | -2.910 | -2.456 | 2 | -5.390 | -3.325 | 0 | — | — | 0 | — | — | 2 | -2.910 | -2.539 | 2 | -5.390 | -3.591 |
| ENAUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 3 | -0.419 | -0.855 | 3 | +3.562 | +1.515 | 0 | — | — | 0 | — | — | 3 | -0.419 | -0.771 | 3 | +3.562 | +1.781 |
| ENAUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 5 | -2.133 | -2.124 | 5 | -4.517 | -4.508 | 0 | — | — | 0 | — | — | 5 | -2.133 | -2.124 | 5 | -4.517 | -4.508 |
| ENAUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 2 | -2.910 | -2.456 | 2 | -5.390 | -3.325 | 0 | — | — | 0 | — | — | 2 | -2.910 | -2.539 | 2 | -5.390 | -3.591 |
| ENAUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 3 | -0.419 | -0.855 | 3 | +3.562 | +1.515 | 0 | — | — | 0 | — | — | 3 | -0.419 | -0.771 | 3 | +3.562 | +1.781 |
| ENAUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 4 | -2.649 | -2.640 | 4 | -5.389 | -5.380 | 0 | — | — | 0 | — | — | 4 | -2.649 | -2.640 | 4 | -5.389 | -5.380 |
| ENAUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 2 | -2.910 | -2.456 | 2 | -5.390 | -3.325 | 0 | — | — | 0 | — | — | 2 | -2.910 | -2.539 | 2 | -5.390 | -3.591 |
| ENAUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 2 | -1.386 | -1.823 | 2 | -4.330 | -6.377 | 0 | — | — | 0 | — | — | 2 | -1.386 | -1.738 | 2 | -4.330 | -6.110 |
| ENAUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 3 | -2.822 | -2.813 | 3 | -6.265 | -6.256 | 0 | — | — | 0 | — | — | 3 | -2.822 | -2.812 | 3 | -6.265 | -6.256 |
| ENAUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 2 | -2.910 | -2.456 | 2 | -5.390 | -3.325 | 0 | — | — | 0 | — | — | 2 | -2.910 | -2.539 | 2 | -5.390 | -3.591 |
| ENAUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 1 | -2.477 | -2.914 | 1 | -10.873 | -12.919 | 0 | — | — | 0 | — | — | 1 | -2.477 | -2.829 | 1 | -10.873 | -12.653 |
| ENAUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 3 | +2.209 | +2.218 | 3 | +2.447 | +2.455 | 0 | — | — | 0 | — | — | 3 | +2.209 | +2.219 | 3 | +2.447 | +2.456 |
| ENAUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 1 | +4.725 | +5.180 | 1 | -4.408 | -2.344 | 0 | — | — | 0 | — | — | 1 | +4.725 | +5.096 | 1 | -4.408 | -2.610 |
| ENAUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 2 | -1.590 | -2.027 | 2 | +3.597 | +1.550 | 0 | — | — | 0 | — | — | 2 | -1.590 | -1.943 | 2 | +3.597 | +1.816 |
| ENAUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 3 | +2.209 | +2.218 | 3 | +2.447 | +2.455 | 0 | — | — | 0 | — | — | 3 | +2.209 | +2.219 | 3 | +2.447 | +2.456 |
| ENAUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 1 | +4.725 | +5.180 | 1 | -4.408 | -2.344 | 0 | — | — | 0 | — | — | 1 | +4.725 | +5.096 | 1 | -4.408 | -2.610 |
| ENAUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 2 | -1.590 | -2.027 | 2 | +3.597 | +1.550 | 0 | — | — | 0 | — | — | 2 | -1.590 | -1.943 | 2 | +3.597 | +1.816 |
| ENAUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 2 | +1.027 | +1.036 | 2 | +3.230 | +3.239 | 0 | — | — | 0 | — | — | 2 | +1.027 | +1.036 | 2 | +3.230 | +3.239 |
| ENAUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 1 | -0.324 | +0.131 | 1 | -0.798 | +1.267 | 0 | — | — | 0 | — | — | 1 | -0.324 | +0.047 | 1 | -0.798 | +1.001 |
| ENAUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 1 | +2.378 | +1.942 | 1 | +7.259 | +5.212 | 0 | — | — | 0 | — | — | 1 | +2.378 | +2.026 | 1 | +7.259 | +5.478 |
| ENAUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 3 | -0.328 | -0.319 | 3 | +2.226 | +2.234 | 0 | — | — | 0 | — | — | 3 | -0.328 | -0.318 | 3 | +2.226 | +2.235 |
| ENAUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 1 | -0.324 | +0.131 | 1 | -0.798 | +1.267 | 0 | — | — | 0 | — | — | 1 | -0.324 | +0.047 | 1 | -0.798 | +1.001 |
| ENAUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 2 | -2.571 | -3.008 | 2 | +4.742 | +2.695 | 0 | — | — | 0 | — | — | 2 | -2.571 | -2.923 | 2 | +4.742 | +2.962 |
| ENAUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 6 | -0.435 | -0.426 | 6 | +5.507 | +5.515 | 0 | — | — | 0 | — | — | 6 | -0.435 | -0.425 | 6 | +5.507 | +5.516 |
| ENAUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 4 | -0.435 | +0.020 | 4 | +7.799 | +9.864 | 0 | — | — | 0 | — | — | 4 | -0.435 | -0.064 | 4 | +7.799 | +9.598 |
| ENAUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 2 | -0.163 | -0.600 | 2 | -13.972 | -16.019 | 0 | — | — | 0 | — | — | 2 | -0.163 | -0.515 | 2 | -13.972 | -15.753 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 64 | -0.002 | +0.045 | 64 | +1.004 | +1.051 | 0 | — | — | 0 | — | — | 64 | -0.002 | +0.045 | 64 | +1.004 | +1.051 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 33 | -0.117 | -0.020 | 33 | +0.251 | +0.560 | 0 | — | — | 0 | — | — | 33 | -0.117 | -0.020 | 33 | +0.251 | +0.560 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 31 | +0.196 | +0.193 | 31 | +1.531 | +1.317 | 0 | — | — | 0 | — | — | 31 | +0.196 | +0.193 | 31 | +1.531 | +1.317 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 52 | +0.227 | +0.274 | 52 | +1.381 | +1.428 | 0 | — | — | 0 | — | — | 52 | +0.227 | +0.274 | 52 | +1.381 | +1.428 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 28 | -0.087 | +0.011 | 28 | +0.580 | +0.888 | 0 | — | — | 0 | — | — | 28 | -0.087 | +0.011 | 28 | +0.580 | +0.888 |
| PUMPUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 24 | +0.336 | +0.332 | 24 | +2.335 | +2.121 | 0 | — | — | 0 | — | — | 24 | +0.336 | +0.332 | 24 | +2.335 | +2.121 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 52 | +0.370 | +0.417 | 52 | +0.490 | +0.537 | 0 | — | — | 0 | — | — | 52 | +0.370 | +0.417 | 52 | +0.490 | +0.537 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 28 | +0.483 | +0.580 | 28 | +0.457 | +0.766 | 0 | — | — | 0 | — | — | 28 | +0.483 | +0.580 | 28 | +0.457 | +0.766 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 24 | +0.298 | +0.295 | 24 | +0.794 | +0.580 | 0 | — | — | 0 | — | — | 24 | +0.298 | +0.295 | 24 | +0.794 | +0.580 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 44 | +0.370 | +0.417 | 44 | +0.767 | +0.815 | 0 | — | — | 0 | — | — | 44 | +0.370 | +0.417 | 44 | +0.767 | +0.815 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 24 | +0.483 | +0.580 | 24 | +0.457 | +0.766 | 0 | — | — | 0 | — | — | 24 | +0.483 | +0.580 | 24 | +0.457 | +0.766 |
| PUMPUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 20 | +0.298 | +0.295 | 20 | +1.383 | +1.169 | 0 | — | — | 0 | — | — | 20 | +0.298 | +0.295 | 20 | +1.383 | +1.169 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 48 | +0.227 | +0.274 | 48 | -0.407 | -0.360 | 0 | — | — | 0 | — | — | 48 | +0.227 | +0.274 | 48 | -0.407 | -0.360 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 27 | -0.498 | -0.401 | 27 | -0.823 | -0.515 | 0 | — | — | 0 | — | — | 27 | -0.498 | -0.401 | 27 | -0.823 | -0.515 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 21 | +0.978 | +0.975 | 21 | -0.084 | -0.298 | 0 | — | — | 0 | — | — | 21 | +0.978 | +0.975 | 21 | -0.084 | -0.298 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 43 | +0.040 | +0.087 | 43 | -0.648 | -0.600 | 0 | — | — | 0 | — | — | 43 | +0.040 | +0.087 | 43 | -0.648 | -0.600 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 25 | -0.569 | -0.472 | 25 | -1.723 | -1.415 | 0 | — | — | 0 | — | — | 25 | -0.569 | -0.472 | 25 | -1.723 | -1.415 |
| PUMPUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 18 | +1.010 | +1.007 | 18 | -0.337 | -0.551 | 0 | — | — | 0 | — | — | 18 | +1.010 | +1.007 | 18 | -0.337 | -0.551 |
| PUMPUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 54 | +0.082 | +0.129 | 54 | -0.816 | -0.769 | 0 | — | — | 0 | — | — | 54 | +0.082 | +0.129 | 54 | -0.816 | -0.769 |
| PUMPUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 25 | -0.148 | -0.051 | 25 | -1.517 | -1.209 | 0 | — | — | 0 | — | — | 25 | -0.148 | -0.051 | 25 | -1.517 | -1.209 |
| PUMPUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 29 | +0.170 | +0.166 | 29 | -0.017 | -0.232 | 0 | — | — | 0 | — | — | 29 | +0.170 | +0.166 | 29 | -0.017 | -0.232 |
| PUMPUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 40 | +0.030 | +0.077 | 40 | -1.344 | -1.296 | 0 | — | — | 0 | — | — | 40 | +0.030 | +0.077 | 40 | -1.344 | -1.296 |
| PUMPUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 19 | -0.253 | -0.156 | 19 | -2.799 | -2.491 | 0 | — | — | 0 | — | — | 19 | -0.253 | -0.156 | 19 | -2.799 | -2.491 |
| PUMPUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 21 | +0.164 | +0.161 | 21 | +1.421 | +1.207 | 0 | — | — | 0 | — | — | 21 | +0.164 | +0.161 | 21 | +1.421 | +1.207 |
| PUMPUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 109 | +0.109 | +0.156 | 105 | +0.003 | +0.051 | 0 | — | — | 0 | — | — | 109 | +0.109 | +0.156 | 105 | +0.003 | +0.051 |
| PUMPUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 51 | -0.279 | -0.182 | 50 | -0.872 | -0.564 | 0 | — | — | 0 | — | — | 51 | -0.279 | -0.182 | 50 | -0.872 | -0.564 |
| PUMPUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 58 | +0.716 | +0.713 | 55 | +0.604 | +0.390 | 0 | — | — | 0 | — | — | 58 | +0.716 | +0.713 | 55 | +0.604 | +0.390 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 19 | -1.116 | -1.093 | 18 | -2.198 | -2.175 | 0 | — | — | 0 | — | — | 19 | -1.116 | -1.093 | 18 | -2.198 | -2.175 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 9 | -1.112 | -0.979 | 9 | -3.515 | -2.792 | 0 | — | — | 0 | — | — | 9 | -1.112 | -0.979 | 9 | -3.515 | -2.792 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 10 | -1.202 | -1.289 | 9 | -1.658 | -2.335 | 0 | — | — | 0 | — | — | 10 | -1.202 | -1.289 | 9 | -1.658 | -2.335 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 15 | -1.085 | -1.063 | 14 | -1.875 | -1.852 | 0 | — | — | 0 | — | — | 15 | -1.085 | -1.063 | 14 | -1.875 | -1.852 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 7 | -1.112 | -0.979 | 7 | -2.208 | -1.484 | 0 | — | — | 0 | — | — | 7 | -1.112 | -0.979 | 7 | -2.208 | -1.484 |
| PUMPUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 8 | -0.404 | -0.491 | 7 | -1.306 | -1.983 | 0 | — | — | 0 | — | — | 8 | -0.404 | -0.491 | 7 | -1.306 | -1.983 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 16 | -1.599 | -1.576 | 15 | -2.649 | -2.626 | 0 | — | — | 0 | — | — | 16 | -1.599 | -1.576 | 15 | -2.649 | -2.626 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 8 | -1.949 | -1.816 | 8 | -4.180 | -3.456 | 0 | — | — | 0 | — | — | 8 | -1.949 | -1.816 | 8 | -4.180 | -3.456 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 8 | -1.234 | -1.321 | 7 | -2.502 | -3.180 | 0 | — | — | 0 | — | — | 8 | -1.234 | -1.321 | 7 | -2.502 | -3.180 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 14 | -1.600 | -1.577 | 13 | -2.651 | -2.628 | 0 | — | — | 0 | — | — | 14 | -1.600 | -1.577 | 13 | -2.651 | -2.628 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | -2.193 | -2.060 | 7 | -3.527 | -2.804 | 0 | — | — | 0 | — | — | 7 | -2.193 | -2.060 | 7 | -3.527 | -2.804 |
| PUMPUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 7 | -1.094 | -1.181 | 6 | -1.236 | -1.914 | 0 | — | — | 0 | — | — | 7 | -1.094 | -1.181 | 6 | -1.236 | -1.914 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 14 | -1.229 | -1.206 | 12 | -2.490 | -2.467 | 0 | — | — | 0 | — | — | 14 | -1.229 | -1.206 | 12 | -2.490 | -2.467 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 7 | -1.457 | -1.324 | 6 | -2.509 | -1.786 | 0 | — | — | 0 | — | — | 7 | -1.457 | -1.324 | 6 | -2.509 | -1.786 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 7 | -1.090 | -1.177 | 6 | -0.957 | -1.635 | 0 | — | — | 0 | — | — | 7 | -1.090 | -1.177 | 6 | -0.957 | -1.635 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 13 | -1.085 | -1.062 | 11 | -2.764 | -2.741 | 0 | — | — | 0 | — | — | 13 | -1.085 | -1.062 | 11 | -2.764 | -2.741 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 6 | -0.841 | -0.708 | 5 | -2.805 | -2.082 | 0 | — | — | 0 | — | — | 6 | -0.841 | -0.708 | 5 | -2.805 | -2.082 |
| PUMPUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 7 | -1.090 | -1.177 | 6 | -0.957 | -1.635 | 0 | — | — | 0 | — | — | 7 | -1.090 | -1.177 | 6 | -0.957 | -1.635 |
| PUMPUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 16 | -1.281 | -1.258 | 15 | -1.681 | -1.659 | 0 | — | — | 0 | — | — | 16 | -1.281 | -1.258 | 15 | -1.681 | -1.659 |
| PUMPUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 8 | -1.718 | -1.585 | 8 | -1.942 | -1.218 | 0 | — | — | 0 | — | — | 8 | -1.718 | -1.585 | 8 | -1.942 | -1.218 |
| PUMPUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 8 | -0.872 | -0.959 | 7 | -1.647 | -2.324 | 0 | — | — | 0 | — | — | 8 | -0.872 | -0.959 | 7 | -1.647 | -2.324 |
| PUMPUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 15 | -1.004 | -0.981 | 14 | -1.536 | -1.513 | 0 | — | — | 0 | — | — | 15 | -1.004 | -0.981 | 14 | -1.536 | -1.513 |
| PUMPUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 8 | -1.718 | -1.585 | 8 | -1.942 | -1.218 | 0 | — | — | 0 | — | — | 8 | -1.718 | -1.585 | 8 | -1.942 | -1.218 |
| PUMPUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 7 | +0.007 | -0.080 | 6 | -0.049 | -0.726 | 0 | — | — | 0 | — | — | 7 | +0.007 | -0.080 | 6 | -0.049 | -0.726 |
| PUMPUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 17 | -0.197 | -0.174 | 17 | -1.360 | -1.337 | 0 | — | — | 0 | — | — | 17 | -0.197 | -0.174 | 17 | -1.360 | -1.337 |
| PUMPUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 5 | +0.806 | +0.939 | 5 | +0.063 | +0.787 | 0 | — | — | 0 | — | — | 5 | +0.806 | +0.939 | 5 | +0.063 | +0.787 |
| PUMPUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 12 | -1.277 | -1.364 | 12 | -1.860 | -2.538 | 0 | — | — | 0 | — | — | 12 | -1.277 | -1.364 | 12 | -1.860 | -2.538 |
| PUMPUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 1 | +1.654 | +1.663 | 1 | +3.171 | +3.180 | 0 | — | — | 0 | — | — | 1 | +1.654 | +1.663 | 1 | +3.171 | +3.180 |
| PUMPUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 1 | +1.654 | +1.456 | 1 | +3.171 | +1.663 | 0 | — | — | 0 | — | — | 1 | +1.654 | +1.456 | 1 | +3.171 | +1.663 |
| PUMPUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 1 | +1.654 | +1.663 | 1 | +3.171 | +3.180 | 0 | — | — | 0 | — | — | 1 | +1.654 | +1.663 | 1 | +3.171 | +3.180 |
| PUMPUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 1 | +1.654 | +1.456 | 1 | +3.171 | +1.663 | 0 | — | — | 0 | — | — | 1 | +1.654 | +1.456 | 1 | +3.171 | +1.663 |
| PUMPUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 1 | +2.286 | +2.295 | 1 | +1.905 | +1.914 | 0 | — | — | 0 | — | — | 1 | +2.286 | +2.295 | 1 | +1.905 | +1.914 |
| PUMPUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 1 | +2.286 | +2.088 | 1 | +1.905 | +0.398 | 0 | — | — | 0 | — | — | 1 | +2.286 | +2.088 | 1 | +1.905 | +0.398 |
| PUMPUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 1 | +2.286 | +2.295 | 1 | +1.905 | +1.914 | 0 | — | — | 0 | — | — | 1 | +2.286 | +2.295 | 1 | +1.905 | +1.914 |
| PUMPUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 1 | +2.286 | +2.088 | 1 | +1.905 | +0.398 | 0 | — | — | 0 | — | — | 1 | +2.286 | +2.088 | 1 | +1.905 | +0.398 |
| PUMPUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 1 | -5.842 | -5.833 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -5.842 | -5.833 | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 1 | -5.842 | -6.040 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -5.842 | -6.040 | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 1 | -5.842 | -5.833 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -5.842 | -5.833 | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 1 | -5.842 | -6.040 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -5.842 | -6.040 | 0 | — | — |
| PUMPUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 2 | +1.615 | +1.624 | 2 | +1.354 | +1.363 | 0 | — | — | 0 | — | — | 2 | +1.615 | +1.624 | 2 | +1.354 | +1.363 |
| PUMPUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 1 | +0.773 | +0.989 | 1 | -0.832 | +0.693 | 0 | — | — | 0 | — | — | 1 | +0.773 | +0.989 | 1 | -0.832 | +0.693 |
| PUMPUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 1 | +2.456 | +2.259 | 1 | +3.540 | +2.033 | 0 | — | — | 0 | — | — | 1 | +2.456 | +2.259 | 1 | +3.540 | +2.033 |
| PUMPUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 2 | +1.615 | +1.624 | 2 | +1.354 | +1.363 | 0 | — | — | 0 | — | — | 2 | +1.615 | +1.624 | 2 | +1.354 | +1.363 |
| PUMPUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 1 | +0.773 | +0.989 | 1 | -0.832 | +0.693 | 0 | — | — | 0 | — | — | 1 | +0.773 | +0.989 | 1 | -0.832 | +0.693 |
| PUMPUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 1 | +2.456 | +2.259 | 1 | +3.540 | +2.033 | 0 | — | — | 0 | — | — | 1 | +2.456 | +2.259 | 1 | +3.540 | +2.033 |
| PUMPUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 4 | +0.986 | +0.995 | 3 | -1.420 | -1.412 | 0 | — | — | 0 | — | — | 4 | +0.986 | +0.995 | 3 | -1.420 | -1.412 |
| PUMPUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 4 | +0.986 | +1.202 | 3 | -1.420 | +0.104 | 0 | — | — | 0 | — | — | 4 | +0.986 | +1.202 | 3 | -1.420 | +0.104 |
| PUMPUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 71 | -0.172 | -0.104 | 70 | -0.302 | -0.234 | 0 | — | — | 0 | — | — | 71 | -0.172 | -0.104 | 70 | -0.302 | -0.234 |
| HYPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 39 | +0.147 | +0.210 | 38 | -0.967 | -1.259 | 0 | — | — | 0 | — | — | 39 | +0.147 | +0.210 | 38 | -0.967 | -1.259 |
| HYPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 32 | -0.634 | -0.560 | 32 | +0.034 | +0.463 | 0 | — | — | 0 | — | — | 32 | -0.634 | -0.560 | 32 | +0.034 | +0.463 |
| HYPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 60 | -0.384 | -0.315 | 59 | -0.298 | -0.229 | 0 | — | — | 0 | — | — | 60 | -0.384 | -0.315 | 59 | -0.298 | -0.229 |
| HYPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 29 | +0.041 | +0.104 | 28 | -0.965 | -1.258 | 0 | — | — | 0 | — | — | 29 | +0.041 | +0.104 | 28 | -0.965 | -1.258 |
| HYPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 31 | -0.748 | -0.675 | 31 | +0.367 | +0.796 | 0 | — | — | 0 | — | — | 31 | -0.748 | -0.675 | 31 | +0.367 | +0.796 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 65 | +0.290 | +0.359 | 64 | -0.515 | -0.446 | 0 | — | — | 0 | — | — | 65 | +0.290 | +0.359 | 64 | -0.515 | -0.446 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 34 | -0.082 | -0.018 | 33 | -0.400 | -0.693 | 0 | — | — | 0 | — | — | 34 | -0.082 | -0.018 | 33 | -0.400 | -0.693 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 31 | +0.438 | +0.512 | 31 | -0.626 | -0.196 | 0 | — | — | 0 | — | — | 31 | +0.438 | +0.512 | 31 | -0.626 | -0.196 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 60 | -0.066 | +0.002 | 59 | -0.400 | -0.332 | 0 | — | — | 0 | — | — | 60 | -0.066 | +0.002 | 59 | -0.400 | -0.332 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 32 | -0.227 | -0.164 | 31 | -0.400 | -0.693 | 0 | — | — | 0 | — | — | 32 | -0.227 | -0.164 | 31 | -0.400 | -0.693 |
| HYPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 28 | +0.364 | +0.438 | 28 | -0.486 | -0.057 | 0 | — | — | 0 | — | — | 28 | +0.364 | +0.438 | 28 | -0.486 | -0.057 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 60 | +0.205 | +0.274 | 60 | -0.546 | -0.478 | 0 | — | — | 0 | — | — | 60 | +0.205 | +0.274 | 60 | -0.546 | -0.478 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 33 | +0.536 | +0.599 | 33 | -0.048 | -0.341 | 0 | — | — | 0 | — | — | 33 | +0.536 | +0.599 | 33 | -0.048 | -0.341 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 27 | -0.204 | -0.130 | 27 | -0.715 | -0.286 | 0 | — | — | 0 | — | — | 27 | -0.204 | -0.130 | 27 | -0.715 | -0.286 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 54 | +0.205 | +0.274 | 54 | -0.531 | -0.462 | 0 | — | — | 0 | — | — | 54 | +0.205 | +0.274 | 54 | -0.531 | -0.462 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 30 | +0.658 | +0.721 | 30 | +0.035 | -0.258 | 0 | — | — | 0 | — | — | 30 | +0.658 | +0.721 | 30 | +0.035 | -0.258 |
| HYPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 24 | -0.476 | -0.402 | 24 | -0.827 | -0.398 | 0 | — | — | 0 | — | — | 24 | -0.476 | -0.402 | 24 | -0.827 | -0.398 |
| HYPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 58 | -0.048 | +0.021 | 58 | -1.273 | -1.205 | 0 | — | — | 0 | — | — | 58 | -0.048 | +0.021 | 58 | -1.273 | -1.205 |
| HYPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 30 | +0.049 | +0.112 | 30 | -0.707 | -0.999 | 0 | — | — | 0 | — | — | 30 | +0.049 | +0.112 | 30 | -0.707 | -0.999 |
| HYPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 28 | -0.075 | -0.001 | 28 | -1.515 | -1.086 | 0 | — | — | 0 | — | — | 28 | -0.075 | -0.001 | 28 | -1.515 | -1.086 |
| HYPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 53 | -0.048 | +0.020 | 53 | -0.864 | -0.795 | 0 | — | — | 0 | — | — | 53 | -0.048 | +0.020 | 53 | -0.864 | -0.795 |
| HYPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 28 | -0.197 | -0.134 | 28 | -0.317 | -0.609 | 0 | — | — | 0 | — | — | 28 | -0.197 | -0.134 | 28 | -0.317 | -0.609 |
| HYPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 25 | -0.048 | +0.026 | 25 | -1.298 | -0.869 | 0 | — | — | 0 | — | — | 25 | -0.048 | +0.026 | 25 | -1.298 | -0.869 |
| HYPEUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 124 | -0.045 | +0.023 | 122 | -0.764 | -0.696 | 0 | — | — | 0 | — | — | 124 | -0.045 | +0.023 | 122 | -0.764 | -0.696 |
| HYPEUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 59 | -0.394 | -0.331 | 59 | -1.033 | -1.326 | 0 | — | — | 0 | — | — | 59 | -0.394 | -0.331 | 59 | -1.033 | -1.326 |
| HYPEUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 65 | +0.222 | +0.296 | 63 | -0.525 | -0.095 | 0 | — | — | 0 | — | — | 65 | +0.222 | +0.296 | 63 | -0.525 | -0.095 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 18 | -0.066 | -0.032 | 17 | -3.197 | -3.164 | 0 | — | — | 0 | — | — | 18 | -0.066 | -0.032 | 17 | -3.197 | -3.164 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 10 | -0.063 | -0.145 | 9 | -0.793 | -1.508 | 0 | — | — | 0 | — | — | 10 | -0.063 | -0.145 | 9 | -0.793 | -1.508 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 8 | -1.064 | -0.915 | 8 | -5.039 | -4.258 | 0 | — | — | 0 | — | — | 8 | -1.064 | -0.915 | 8 | -5.039 | -4.258 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 16 | -0.671 | -0.637 | 15 | -3.197 | -3.164 | 0 | — | — | 0 | — | — | 16 | -0.671 | -0.637 | 15 | -3.197 | -3.164 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | -0.665 | -0.747 | 7 | -0.788 | -1.502 | 0 | — | — | 0 | — | — | 8 | -0.665 | -0.747 | 7 | -0.788 | -1.502 |
| HYPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 8 | -1.064 | -0.915 | 8 | -5.039 | -4.258 | 0 | — | — | 0 | — | — | 8 | -1.064 | -0.915 | 8 | -5.039 | -4.258 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 16 | +0.005 | +0.038 | 15 | -2.534 | -2.501 | 0 | — | — | 0 | — | — | 16 | +0.005 | +0.038 | 15 | -2.534 | -2.501 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 9 | -0.131 | -0.213 | 8 | -0.013 | -0.728 | 0 | — | — | 0 | — | — | 9 | -0.131 | -0.213 | 8 | -0.013 | -0.728 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 7 | +0.214 | +0.363 | 7 | -8.201 | -7.420 | 0 | — | — | 0 | — | — | 7 | +0.214 | +0.363 | 7 | -8.201 | -7.420 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 14 | +0.007 | +0.040 | 13 | -2.342 | -2.309 | 0 | — | — | 0 | — | — | 14 | +0.007 | +0.040 | 13 | -2.342 | -2.309 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 8 | -0.080 | -0.162 | 7 | +1.146 | +0.431 | 0 | — | — | 0 | — | — | 8 | -0.080 | -0.162 | 7 | +1.146 | +0.431 |
| HYPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 6 | +0.129 | +0.277 | 6 | -5.918 | -5.137 | 0 | — | — | 0 | — | — | 6 | +0.129 | +0.277 | 6 | -5.918 | -5.137 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 13 | -0.074 | -0.041 | 12 | -2.099 | -2.066 | 0 | — | — | 0 | — | — | 13 | -0.074 | -0.041 | 12 | -2.099 | -2.066 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 8 | +0.473 | +0.391 | 7 | +0.635 | -0.080 | 0 | — | — | 0 | — | — | 8 | +0.473 | +0.391 | 7 | +0.635 | -0.080 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 5 | -2.265 | -2.116 | 5 | -8.359 | -7.578 | 0 | — | — | 0 | — | — | 5 | -2.265 | -2.116 | 5 | -8.359 | -7.578 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 12 | +0.281 | +0.315 | 11 | -1.853 | -1.820 | 0 | — | — | 0 | — | — | 12 | +0.281 | +0.315 | 11 | -1.853 | -1.820 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 7 | +1.016 | +0.935 | 6 | +0.680 | -0.034 | 0 | — | — | 0 | — | — | 7 | +1.016 | +0.935 | 6 | +0.680 | -0.034 |
| HYPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 5 | -2.265 | -2.116 | 5 | -8.359 | -7.578 | 0 | — | — | 0 | — | — | 5 | -2.265 | -2.116 | 5 | -8.359 | -7.578 |
| HYPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 16 | -1.055 | -1.022 | 15 | -1.528 | -1.495 | 0 | — | — | 0 | — | — | 16 | -1.055 | -1.022 | 15 | -1.528 | -1.495 |
| HYPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 10 | -1.052 | -1.134 | 9 | -0.547 | -1.262 | 0 | — | — | 0 | — | — | 10 | -1.052 | -1.134 | 9 | -0.547 | -1.262 |
| HYPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 6 | -1.319 | -1.170 | 6 | -6.747 | -5.967 | 0 | — | — | 0 | — | — | 6 | -1.319 | -1.170 | 6 | -6.747 | -5.967 |
| HYPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 14 | -1.123 | -1.090 | 13 | -0.551 | -0.518 | 0 | — | — | 0 | — | — | 14 | -1.123 | -1.090 | 13 | -0.551 | -0.518 |
| HYPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 8 | -1.118 | -1.200 | 7 | +0.056 | -0.659 | 0 | — | — | 0 | — | — | 8 | -1.118 | -1.200 | 7 | +0.056 | -0.659 |
| HYPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 6 | -1.319 | -1.170 | 6 | -6.747 | -5.967 | 0 | — | — | 0 | — | — | 6 | -1.319 | -1.170 | 6 | -6.747 | -5.967 |
| HYPEUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 33 | -0.097 | -0.063 | 31 | -0.192 | -0.159 | 0 | — | — | 0 | — | — | 33 | -0.097 | -0.063 | 31 | -0.192 | -0.159 |
| HYPEUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 18 | -0.003 | -0.085 | 16 | +1.304 | +0.589 | 0 | — | — | 0 | — | — | 18 | -0.003 | -0.085 | 16 | +1.304 | +0.589 |
| HYPEUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 15 | -0.763 | -0.615 | 15 | -2.642 | -1.861 | 0 | — | — | 0 | — | — | 15 | -0.763 | -0.615 | 15 | -2.642 | -1.861 |
| HYPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 3 | -1.504 | -1.491 | 2 | -7.999 | -7.986 | 0 | — | — | 0 | — | — | 3 | -1.504 | -1.491 | 2 | -7.999 | -7.986 |
| HYPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 2 | -2.366 | -2.570 | 1 | -6.003 | -9.544 | 0 | — | — | 0 | — | — | 2 | -2.366 | -2.570 | 1 | -6.003 | -9.544 |
| HYPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 1 | +0.131 | +0.362 | 1 | -9.995 | -6.428 | 0 | — | — | 0 | — | — | 1 | +0.131 | +0.362 | 1 | -9.995 | -6.428 |
| HYPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 1 | -1.507 | -1.494 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -1.507 | -1.494 | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 1 | -1.507 | -1.711 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | -1.507 | -1.711 | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 3 | +1.432 | +1.446 | 2 | -2.599 | -2.586 | 0 | — | — | 0 | — | — | 3 | +1.432 | +1.446 | 2 | -2.599 | -2.586 |
| HYPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 2 | +1.539 | +1.335 | 1 | -3.312 | -6.853 | 0 | — | — | 0 | — | — | 2 | +1.539 | +1.335 | 1 | -3.312 | -6.853 |
| HYPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 1 | +1.432 | +1.663 | 1 | -1.885 | +1.682 | 0 | — | — | 0 | — | — | 1 | +1.432 | +1.663 | 1 | -1.885 | +1.682 |
| HYPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 1 | +6.114 | +6.128 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | +6.114 | +6.128 | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 1 | +6.114 | +5.911 | 0 | — | — | 0 | — | — | 0 | — | — | 1 | +6.114 | +5.911 | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 1 | +0.225 | +0.239 | 1 | -4.019 | -4.006 | 0 | — | — | 0 | — | — | 1 | +0.225 | +0.239 | 1 | -4.019 | -4.006 |
| HYPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 1 | +0.225 | +0.456 | 1 | -4.019 | -0.452 | 0 | — | — | 0 | — | — | 1 | +0.225 | +0.456 | 1 | -4.019 | -0.452 |
| HYPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 1 | +0.225 | +0.239 | 1 | -4.019 | -4.006 | 0 | — | — | 0 | — | — | 1 | +0.225 | +0.239 | 1 | -4.019 | -4.006 |
| HYPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 1 | +0.225 | +0.456 | 1 | -4.019 | -0.452 | 0 | — | — | 0 | — | — | 1 | +0.225 | +0.456 | 1 | -4.019 | -0.452 |
| HYPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 1 | -3.738 | -3.724 | 1 | -9.429 | -9.416 | 0 | — | — | 0 | — | — | 1 | -3.738 | -3.724 | 1 | -9.429 | -9.416 |
| HYPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 1 | -3.738 | -3.507 | 1 | -9.429 | -5.861 | 0 | — | — | 0 | — | — | 1 | -3.738 | -3.507 | 1 | -9.429 | -5.861 |
| HYPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 1 | -3.738 | -3.724 | 1 | -9.429 | -9.416 | 0 | — | — | 0 | — | — | 1 | -3.738 | -3.724 | 1 | -9.429 | -9.416 |
| HYPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| HYPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 1 | -3.738 | -3.507 | 1 | -9.429 | -5.861 | 0 | — | — | 0 | — | — | 1 | -3.738 | -3.507 | 1 | -9.429 | -5.861 |
| HYPEUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 3 | -1.806 | -1.793 | 3 | -1.437 | -1.424 | 0 | — | — | 0 | — | — | 3 | -1.806 | -1.793 | 3 | -1.437 | -1.424 |
| HYPEUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 3 | -1.806 | -2.010 | 3 | -1.437 | -4.978 | 0 | — | — | 0 | — | — | 3 | -1.806 | -2.010 | 3 | -1.437 | -4.978 |
| HYPEUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 133 | -0.226 | -0.127 | 132 | +0.067 | +0.166 | 38 | +0.390 | +0.490 | 38 | +1.563 | +1.664 | 95 | -0.281 | -0.184 | 94 | -0.523 | -0.425 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 65 | +0.002 | +0.151 | 64 | -0.225 | +0.193 | 20 | -0.669 | -0.455 | 20 | +0.205 | +0.112 | 45 | +0.103 | +0.230 | 44 | -0.688 | -0.073 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 68 | -0.260 | -0.211 | 68 | +0.066 | -0.154 | 18 | +1.020 | +1.007 | 18 | +1.720 | +2.015 | 50 | -0.716 | -0.647 | 50 | -0.327 | -0.746 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 106 | -0.215 | -0.117 | 105 | +0.090 | +0.189 | 31 | +0.235 | +0.336 | 31 | +1.652 | +1.752 | 75 | -0.269 | -0.171 | 74 | -0.325 | -0.227 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 51 | -0.085 | +0.063 | 50 | -0.800 | -0.381 | 17 | -0.958 | -0.743 | 17 | +0.091 | -0.002 | 34 | +0.062 | +0.189 | 33 | -1.106 | -0.491 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 55 | -0.233 | -0.184 | 55 | +1.285 | +1.064 | 14 | +1.106 | +1.094 | 14 | +2.462 | +2.757 | 41 | -0.609 | -0.540 | 41 | -0.122 | -0.541 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 119 | -0.380 | -0.282 | 119 | -0.258 | -0.159 | 33 | +0.453 | +0.554 | 33 | -1.321 | -1.220 | 86 | -0.665 | -0.567 | 86 | -0.011 | +0.087 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 61 | -0.288 | -0.140 | 61 | +0.160 | +0.579 | 20 | -0.246 | -0.031 | 20 | -0.790 | -0.883 | 41 | -0.380 | -0.253 | 41 | +0.180 | +0.795 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 58 | -0.444 | -0.394 | 58 | -0.497 | -0.718 | 13 | +1.157 | +1.144 | 13 | -2.412 | -2.117 | 45 | -0.720 | -0.651 | 45 | -0.360 | -0.779 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 96 | -0.436 | -0.338 | 96 | -0.237 | -0.138 | 25 | +0.756 | +0.857 | 25 | -2.408 | -2.307 | 71 | -0.715 | -0.617 | 71 | +0.090 | +0.188 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 46 | -0.839 | -0.691 | 46 | +0.184 | +0.603 | 13 | -1.654 | -1.440 | 13 | -3.410 | -3.503 | 33 | -0.366 | -0.239 | 33 | +0.254 | +0.869 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 50 | -0.358 | -0.309 | 50 | -0.500 | -0.720 | 12 | +1.216 | +1.203 | 12 | -1.392 | -1.098 | 38 | -0.742 | -0.673 | 38 | -0.493 | -0.912 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 103 | -0.817 | -0.718 | 103 | -0.029 | +0.070 | 26 | -0.282 | -0.182 | 26 | +0.722 | +0.823 | 77 | -0.921 | -0.823 | 77 | -0.259 | -0.161 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 54 | -0.950 | -0.802 | 54 | -0.136 | +0.282 | 18 | -0.277 | -0.063 | 18 | +2.645 | +2.552 | 36 | -1.172 | -1.045 | 36 | -0.839 | -0.224 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 49 | -0.710 | -0.661 | 49 | +0.463 | +0.242 | 8 | -0.229 | -0.242 | 8 | -2.928 | -2.634 | 41 | -0.713 | -0.644 | 41 | +0.742 | +0.323 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 88 | -0.845 | -0.747 | 88 | +0.215 | +0.314 | 23 | -0.485 | -0.384 | 23 | +1.109 | +1.209 | 65 | -0.878 | -0.781 | 65 | -0.033 | +0.065 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 44 | -1.004 | -0.856 | 44 | +0.221 | +0.640 | 15 | -0.479 | -0.265 | 15 | +5.914 | +5.821 | 29 | -1.079 | -0.952 | 29 | -0.264 | +0.351 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 44 | -0.341 | -0.292 | 44 | +0.101 | -0.120 | 8 | -0.229 | -0.242 | 8 | -2.928 | -2.634 | 36 | -0.345 | -0.276 | 36 | +1.059 | +0.640 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_first | record | ALL | both | 92 | +0.109 | +0.208 | 92 | -0.474 | -0.376 | 23 | +0.981 | +1.082 | 23 | +0.480 | +0.580 | 69 | -0.372 | -0.274 | 69 | -0.648 | -0.550 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_first | record | ALL | long | 51 | +0.029 | +0.177 | 51 | -0.242 | +0.176 | 13 | +0.493 | +0.708 | 13 | +0.495 | +0.402 | 38 | -0.408 | -0.281 | 38 | -0.807 | -0.192 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_first | record | ALL | short | 41 | +0.104 | +0.154 | 41 | -0.487 | -0.708 | 10 | +1.003 | +0.990 | 10 | +0.546 | +0.841 | 31 | -0.390 | -0.321 | 31 | -0.499 | -0.918 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 80 | -0.017 | +0.081 | 80 | +0.376 | +0.475 | 22 | +1.131 | +1.232 | 22 | +2.485 | +2.586 | 58 | -0.616 | -0.518 | 58 | -0.146 | -0.048 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 45 | -0.629 | -0.481 | 45 | -0.677 | -0.259 | 12 | +0.373 | +0.587 | 12 | +0.130 | +0.037 | 33 | -1.103 | -0.976 | 33 | -0.943 | -0.328 |
| MNTUSDT_BYBIT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 35 | +0.199 | +0.248 | 35 | +2.033 | +1.812 | 10 | +1.611 | +1.598 | 10 | +3.455 | +3.749 | 25 | -0.391 | -0.322 | 25 | +1.391 | +0.972 |
| MNTUSDT_BYBIT | 1h | calibrated | SFP_harden | record | ALL | both | 158 | +0.055 | +0.153 | 155 | -1.067 | -0.968 | 43 | -1.633 | -1.532 | 43 | -3.472 | -3.371 | 115 | +0.237 | +0.335 | 112 | -0.042 | +0.056 |
| MNTUSDT_BYBIT | 1h | calibrated | SFP_harden | record | ALL | long | 85 | -0.221 | -0.073 | 85 | -1.571 | -1.153 | 29 | -1.633 | -1.419 | 29 | -3.025 | -3.118 | 56 | -0.048 | +0.079 | 56 | -1.203 | -0.588 |
| MNTUSDT_BYBIT | 1h | calibrated | SFP_harden | record | ALL | short | 73 | +0.410 | +0.460 | 70 | -0.039 | -0.259 | 14 | -1.511 | -1.524 | 14 | -7.394 | -7.099 | 59 | +0.830 | +0.899 | 56 | +1.571 | +1.152 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 38 | +1.043 | +1.090 | 37 | +3.394 | +3.441 | 10 | -0.393 | -0.345 | 10 | +2.030 | +2.078 | 28 | +1.416 | +1.463 | 27 | +3.394 | +3.441 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 22 | +0.492 | +0.672 | 21 | +4.387 | +4.993 | 7 | +0.289 | +0.315 | 7 | +4.387 | +3.190 | 15 | +0.702 | +0.946 | 14 | +4.445 | +5.520 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 16 | +1.750 | +1.664 | 16 | -0.078 | -0.590 | 3 | -4.817 | -4.747 | 3 | -3.902 | -2.610 | 13 | +1.869 | +1.718 | 13 | +2.671 | +1.688 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 32 | +0.730 | +0.777 | 31 | +0.485 | +0.532 | 8 | -0.390 | -0.342 | 8 | -1.043 | -0.995 | 24 | +1.066 | +1.112 | 23 | +3.396 | +3.443 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 19 | +0.695 | +0.875 | 18 | +4.032 | +4.639 | 5 | +0.290 | +0.315 | 5 | +3.579 | +2.382 | 14 | +1.034 | +1.278 | 13 | +5.210 | +6.285 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 13 | +0.751 | +0.665 | 13 | -2.906 | -3.419 | 3 | -4.817 | -4.747 | 3 | -3.902 | -2.610 | 10 | +1.920 | +1.768 | 10 | -1.771 | -2.753 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 30 | -1.085 | -1.039 | 29 | -0.788 | -0.741 | 8 | -0.909 | -0.862 | 8 | -0.636 | -0.589 | 22 | -1.189 | -1.143 | 21 | -0.796 | -0.750 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 18 | -1.082 | -0.902 | 17 | -1.135 | -0.528 | 5 | -0.746 | -0.721 | 5 | +3.578 | +2.382 | 13 | -1.273 | -1.029 | 12 | -1.576 | -0.500 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 12 | -0.887 | -0.973 | 12 | +0.241 | -0.272 | 3 | -3.503 | -3.433 | 3 | -2.891 | -1.598 | 9 | +1.594 | +1.442 | 9 | +3.592 | +2.609 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 26 | -0.977 | -0.930 | 25 | -0.787 | -0.740 | 8 | -0.909 | -0.862 | 8 | -0.636 | -0.589 | 18 | -0.991 | -0.944 | 17 | -0.796 | -0.750 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 16 | -0.974 | -0.794 | 15 | +2.680 | +3.287 | 5 | -0.746 | -0.721 | 5 | +3.578 | +2.382 | 11 | -1.092 | -0.848 | 10 | +0.772 | +1.848 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 10 | -0.887 | -0.973 | 10 | -1.855 | -2.368 | 3 | -3.503 | -3.433 | 3 | -2.891 | -1.598 | 7 | +1.858 | +1.706 | 7 | -0.803 | -1.786 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 22 | -1.136 | -1.090 | 21 | +1.299 | +1.345 | 6 | -1.634 | -1.586 | 6 | +2.730 | +2.778 | 16 | -0.816 | -0.770 | 15 | +0.171 | +0.218 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 15 | -1.055 | -0.875 | 14 | +0.343 | +0.949 | 4 | -1.634 | -1.609 | 4 | +4.654 | +3.457 | 11 | -0.572 | -0.327 | 10 | -1.702 | -0.626 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 7 | -3.225 | -3.311 | 7 | +1.297 | +0.784 | 2 | -6.158 | -6.088 | 2 | -7.632 | -6.340 | 5 | -3.231 | -3.382 | 5 | +3.326 | +2.343 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 20 | -1.136 | -1.090 | 19 | +1.299 | +1.345 | 5 | -1.507 | -1.459 | 5 | +1.305 | +1.353 | 15 | -1.061 | -1.014 | 14 | +0.732 | +0.778 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 13 | -1.055 | -0.875 | 12 | +0.344 | +0.950 | 3 | -1.507 | -1.482 | 3 | +5.153 | +3.956 | 10 | -0.816 | -0.572 | 9 | -0.619 | +0.456 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 7 | -3.225 | -3.311 | 7 | +1.297 | +0.784 | 2 | -6.158 | -6.088 | 2 | -7.632 | -6.340 | 5 | -3.231 | -3.382 | 5 | +3.326 | +2.343 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_first | record | ALL | both | 30 | -0.193 | -0.147 | 30 | +2.066 | +2.112 | 10 | -0.352 | -0.304 | 10 | -1.370 | -1.322 | 20 | -0.137 | -0.091 | 20 | +2.638 | +2.684 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_first | record | ALL | long | 17 | +0.768 | +0.948 | 17 | +4.165 | +4.771 | 6 | +0.298 | +0.323 | 6 | +2.075 | +0.878 | 11 | +0.767 | +1.011 | 11 | +4.442 | +5.517 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_first | record | ALL | short | 13 | -0.259 | -0.345 | 13 | -3.079 | -3.592 | 4 | -1.573 | -1.503 | 4 | -9.691 | -8.399 | 9 | -0.195 | -0.347 | 9 | +1.821 | +0.839 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 33 | -0.192 | -0.145 | 33 | +2.970 | +3.016 | 11 | -0.449 | -0.401 | 11 | -0.020 | +0.027 | 22 | -0.135 | -0.089 | 22 | +3.672 | +3.718 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 18 | +0.908 | +1.088 | 18 | +4.308 | +4.915 | 7 | -0.447 | -0.421 | 7 | +4.171 | +2.974 | 11 | +1.330 | +1.574 | 11 | +4.443 | +5.518 |
| MNTUSDT_BYBIT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 15 | -0.813 | -0.899 | 15 | +1.824 | +1.312 | 4 | -1.573 | -1.503 | 4 | -9.691 | -8.399 | 11 | -0.813 | -0.964 | 11 | +2.313 | +1.331 |
| MNTUSDT_BYBIT | 4h | calibrated | SFP_harden | record | ALL | both | 49 | -0.030 | +0.017 | 49 | +2.014 | +2.061 | 8 | -1.234 | -1.187 | 8 | -3.225 | -3.177 | 41 | +0.141 | +0.187 | 41 | +2.073 | +2.119 |
| MNTUSDT_BYBIT | 4h | calibrated | SFP_harden | record | ALL | long | 27 | +0.140 | +0.319 | 27 | +2.141 | +2.748 | 2 | +1.659 | +1.685 | 2 | +5.535 | +4.338 | 25 | +0.140 | +0.384 | 25 | +2.141 | +3.217 |
| MNTUSDT_BYBIT | 4h | calibrated | SFP_harden | record | ALL | short | 22 | -1.226 | -1.312 | 22 | +1.611 | +1.099 | 6 | -1.747 | -1.677 | 6 | -4.812 | -3.520 | 16 | +0.078 | -0.073 | 16 | +1.832 | +0.850 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 7 | +2.652 | +2.669 | 6 | +2.628 | +2.644 | 2 | +4.995 | +5.012 | 2 | +5.779 | +5.797 | 5 | +0.248 | +0.265 | 4 | +0.963 | +0.979 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 4 | +2.415 | +2.535 | 4 | -1.911 | -0.424 | 2 | +4.995 | +4.038 | 2 | +5.779 | -0.163 | 2 | -0.874 | -0.597 | 2 | -4.020 | -1.608 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 3 | +2.651 | +2.565 | 2 | +5.902 | +4.448 | 0 | — | — | 0 | — | — | 3 | +2.651 | +2.406 | 2 | +5.902 | +3.522 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 5 | +4.577 | +4.593 | 5 | -0.248 | -0.232 | 2 | +4.995 | +5.012 | 2 | +5.779 | +5.797 | 3 | +0.251 | +0.268 | 3 | -3.577 | -3.561 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 4 | +2.415 | +2.535 | 4 | -1.911 | -0.424 | 2 | +4.995 | +4.038 | 2 | +5.779 | -0.163 | 2 | -0.874 | -0.597 | 2 | -4.020 | -1.608 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 1 | +5.579 | +5.493 | 1 | +5.504 | +4.049 | 0 | — | — | 0 | — | — | 1 | +5.579 | +5.334 | 1 | +5.504 | +3.123 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 5 | -0.932 | -0.916 | 4 | -3.732 | -3.716 | 1 | -0.394 | -0.376 | 1 | -4.683 | -4.665 | 4 | -1.128 | -1.112 | 3 | -3.576 | -3.560 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 3 | -0.932 | -0.813 | 3 | -3.888 | -2.401 | 1 | -0.394 | -1.350 | 1 | -4.683 | -10.625 | 2 | -1.466 | -1.188 | 2 | -3.729 | -1.317 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 2 | +2.127 | +2.041 | 1 | +5.504 | +4.049 | 0 | — | — | 0 | — | — | 2 | +2.127 | +1.882 | 1 | +5.504 | +3.123 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 5 | -0.932 | -0.916 | 4 | -3.732 | -3.716 | 1 | -0.394 | -0.376 | 1 | -4.683 | -4.665 | 4 | -1.128 | -1.112 | 3 | -3.576 | -3.560 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 3 | -0.932 | -0.813 | 3 | -3.888 | -2.401 | 1 | -0.394 | -1.350 | 1 | -4.683 | -10.625 | 2 | -1.466 | -1.188 | 2 | -3.729 | -1.317 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 2 | +2.127 | +2.041 | 1 | +5.504 | +4.049 | 0 | — | — | 0 | — | — | 2 | +2.127 | +1.882 | 1 | +5.504 | +3.123 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 4 | -2.280 | -2.263 | 4 | -3.230 | -3.213 | 1 | -2.560 | -2.542 | 1 | -6.617 | -6.600 | 3 | -2.001 | -1.985 | 3 | -2.879 | -2.863 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 3 | -2.551 | -2.432 | 3 | -3.573 | -2.085 | 1 | -2.560 | -3.517 | 1 | -6.617 | -12.559 | 2 | -2.323 | -2.046 | 2 | -3.225 | -0.812 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 1 | +3.879 | +3.793 | 1 | +4.730 | +3.276 | 0 | — | — | 0 | — | — | 1 | +3.879 | +3.634 | 1 | +4.730 | +2.349 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 3 | -2.551 | -2.534 | 3 | -3.573 | -3.556 | 1 | -2.560 | -2.542 | 1 | -6.617 | -6.600 | 2 | -2.323 | -2.307 | 2 | -3.225 | -3.209 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 3 | -2.551 | -2.432 | 3 | -3.573 | -2.085 | 1 | -2.560 | -3.517 | 1 | -6.617 | -12.559 | 2 | -2.323 | -2.046 | 2 | -3.225 | -0.812 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_first | record | ALL | both | 5 | -1.400 | -1.384 | 5 | -2.408 | -2.392 | 1 | +3.999 | +4.016 | 1 | -1.606 | -1.588 | 4 | -1.904 | -1.888 | 4 | -2.412 | -2.396 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_first | record | ALL | long | 3 | -1.398 | -1.278 | 3 | -2.405 | -0.918 | 1 | +3.999 | +3.042 | 1 | -1.606 | -7.547 | 2 | -1.901 | -1.624 | 2 | -2.409 | +0.004 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_first | record | ALL | short | 2 | -1.986 | -2.072 | 2 | -1.289 | -2.743 | 0 | — | — | 0 | — | — | 2 | -1.986 | -2.231 | 2 | -1.289 | -3.670 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 5 | -1.400 | -1.384 | 5 | -2.408 | -2.392 | 1 | +3.999 | +4.016 | 1 | -1.606 | -1.588 | 4 | -1.904 | -1.888 | 4 | -2.412 | -2.396 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 3 | -1.398 | -1.278 | 3 | -2.405 | -0.918 | 1 | +3.999 | +3.042 | 1 | -1.606 | -7.547 | 2 | -1.901 | -1.624 | 2 | -2.409 | +0.004 |
| MNTUSDT_BYBIT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 2 | -1.986 | -2.072 | 2 | -1.289 | -2.743 | 0 | — | — | 0 | — | — | 2 | -1.986 | -2.231 | 2 | -1.289 | -3.670 |
| MNTUSDT_BYBIT | 1d | calibrated | SFP_harden | record | ALL | both | 6 | -1.073 | -1.056 | 6 | +2.939 | +2.956 | 0 | — | — | 0 | — | — | 6 | -1.073 | -1.057 | 6 | +2.939 | +2.955 |
| MNTUSDT_BYBIT | 1d | calibrated | SFP_harden | record | ALL | long | 6 | -1.073 | -0.954 | 6 | +2.939 | +4.426 | 0 | — | — | 0 | — | — | 6 | -1.073 | -0.796 | 6 | +2.939 | +5.352 |
| MNTUSDT_BYBIT | 1d | calibrated | SFP_harden | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| SUIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 198 | +0.148 | +0.214 | 197 | +0.066 | +0.132 | 69 | +0.122 | +0.184 | 69 | -1.164 | -1.101 | 129 | +0.163 | +0.231 | 128 | +0.243 | +0.311 |
| SUIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 88 | -0.044 | +0.179 | 87 | -0.880 | -0.236 | 34 | -0.060 | +0.188 | 34 | -1.877 | -1.086 | 54 | -0.016 | +0.195 | 53 | -0.081 | +0.490 |
| SUIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 110 | +0.192 | +0.101 | 110 | +0.465 | -0.047 | 35 | +0.181 | +0.059 | 35 | +0.593 | -0.072 | 75 | +0.203 | +0.127 | 75 | +0.317 | -0.118 |
| SUIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 164 | +0.077 | +0.144 | 163 | +0.156 | +0.222 | 60 | -0.019 | +0.044 | 60 | -0.516 | -0.453 | 104 | +0.149 | +0.217 | 103 | +0.232 | +0.300 |
| SUIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 75 | -0.052 | +0.171 | 74 | -0.690 | -0.045 | 30 | -0.162 | +0.086 | 30 | -2.042 | -1.251 | 45 | +0.036 | +0.247 | 44 | +0.217 | +0.788 |
| SUIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 89 | +0.160 | +0.069 | 89 | +0.336 | -0.176 | 30 | +0.146 | +0.024 | 30 | +2.503 | +1.838 | 59 | +0.162 | +0.087 | 59 | +0.227 | -0.207 |
| SUIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 170 | -0.107 | -0.041 | 169 | -0.366 | -0.300 | 60 | -0.169 | -0.106 | 60 | -0.998 | -0.935 | 110 | -0.108 | -0.040 | 109 | -0.239 | -0.171 |
| SUIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 76 | -1.012 | -0.789 | 75 | -1.029 | -0.384 | 32 | -0.840 | -0.592 | 32 | -1.858 | -1.067 | 44 | -1.099 | -0.887 | 43 | -0.508 | +0.062 |
| SUIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 94 | +0.310 | +0.219 | 94 | +0.482 | -0.030 | 28 | +0.966 | +0.844 | 28 | +1.774 | +1.109 | 66 | +0.005 | -0.070 | 66 | +0.045 | -0.390 |
| SUIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 148 | -0.116 | -0.050 | 147 | -0.427 | -0.361 | 53 | -0.257 | -0.194 | 53 | -0.965 | -0.902 | 95 | -0.113 | -0.045 | 94 | -0.397 | -0.329 |
| SUIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 69 | -1.052 | -0.829 | 68 | -1.309 | -0.664 | 29 | -1.050 | -0.802 | 29 | -2.130 | -1.339 | 40 | -1.098 | -0.887 | 39 | -0.605 | -0.035 |
| SUIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 79 | +0.159 | +0.068 | 79 | +0.371 | -0.141 | 24 | +0.872 | +0.750 | 24 | +2.034 | +1.369 | 55 | -0.032 | -0.107 | 55 | -0.145 | -0.580 |
| SUIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 140 | -0.047 | +0.020 | 140 | -0.324 | -0.257 | 51 | -0.486 | -0.423 | 51 | +1.048 | +1.111 | 89 | +0.119 | +0.187 | 89 | -0.433 | -0.365 |
| SUIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 61 | -0.639 | -0.416 | 61 | -1.106 | -0.461 | 27 | -0.480 | -0.232 | 27 | -0.430 | +0.361 | 34 | -0.840 | -0.628 | 34 | -1.236 | -0.666 |
| SUIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 79 | +0.478 | +0.387 | 79 | +0.616 | +0.104 | 24 | -0.396 | -0.519 | 24 | +1.445 | +0.780 | 55 | +0.598 | +0.522 | 55 | +0.445 | +0.010 |
| SUIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 112 | +0.016 | +0.082 | 112 | +0.014 | +0.081 | 42 | +0.063 | +0.126 | 42 | +1.900 | +1.963 | 70 | +0.013 | +0.081 | 70 | -0.446 | -0.378 |
| SUIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 55 | -0.639 | -0.416 | 55 | -1.105 | -0.460 | 26 | -0.272 | -0.024 | 26 | +0.395 | +1.186 | 29 | -0.861 | -0.650 | 29 | -1.304 | -0.733 |
| SUIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 57 | +0.591 | +0.500 | 57 | +1.393 | +0.881 | 16 | +0.534 | +0.412 | 16 | +3.371 | +2.706 | 41 | +0.594 | +0.519 | 41 | +0.615 | +0.180 |
| SUIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 150 | +0.007 | +0.073 | 150 | -0.408 | -0.341 | 53 | +0.082 | +0.145 | 53 | -0.866 | -0.803 | 97 | -0.007 | +0.061 | 97 | -0.373 | -0.305 |
| SUIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 70 | -0.517 | -0.293 | 70 | -1.854 | -1.210 | 30 | -0.898 | -0.650 | 30 | -1.848 | -1.057 | 40 | -0.016 | +0.196 | 40 | -1.782 | -1.211 |
| SUIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 80 | +0.305 | +0.213 | 80 | +0.500 | -0.012 | 23 | +0.525 | +0.402 | 23 | -0.062 | -0.727 | 57 | +0.091 | +0.016 | 57 | +0.548 | +0.113 |
| SUIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 134 | +0.007 | +0.073 | 134 | -0.407 | -0.341 | 54 | +0.107 | +0.170 | 54 | -1.356 | -1.293 | 80 | -0.015 | +0.052 | 80 | +0.103 | +0.171 |
| SUIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 65 | -0.373 | -0.150 | 65 | -2.124 | -1.480 | 30 | -0.389 | -0.141 | 30 | -2.198 | -1.407 | 35 | -0.208 | +0.003 | 35 | -2.127 | -1.556 |
| SUIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 69 | +0.478 | +0.387 | 69 | +1.207 | +0.694 | 24 | +0.309 | +0.187 | 24 | -0.087 | -0.752 | 45 | +0.481 | +0.405 | 45 | +1.764 | +1.329 |
| SUIUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 245 | +0.229 | +0.295 | 245 | +0.175 | +0.241 | 108 | -0.003 | +0.060 | 108 | -0.035 | +0.027 | 137 | +0.349 | +0.417 | 137 | +0.533 | +0.601 |
| SUIUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 129 | +0.268 | +0.491 | 129 | +0.059 | +0.704 | 57 | +0.282 | +0.530 | 57 | -1.033 | -0.242 | 72 | +0.265 | +0.477 | 72 | +0.337 | +0.907 |
| SUIUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 116 | +0.084 | -0.007 | 116 | +0.752 | +0.239 | 51 | -0.275 | -0.398 | 51 | +0.459 | -0.207 | 65 | +0.685 | +0.609 | 65 | +0.981 | +0.547 |
| SUIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 47 | -0.031 | -0.000 | 47 | +1.436 | +1.467 | 18 | -0.373 | -0.344 | 18 | +2.043 | +2.072 | 29 | +0.357 | +0.389 | 29 | +1.436 | +1.468 |
| SUIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 25 | -0.499 | -0.241 | 25 | +0.422 | +1.232 | 9 | -0.715 | -0.397 | 9 | +2.945 | +3.994 | 16 | -0.427 | -0.207 | 16 | -0.285 | +0.351 |
| SUIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 22 | +0.173 | -0.023 | 22 | +2.032 | +1.283 | 9 | -0.035 | -0.296 | 9 | +1.137 | +0.145 | 13 | +0.565 | +0.409 | 13 | +2.558 | +1.987 |
| SUIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 42 | -0.150 | -0.119 | 42 | +1.289 | +1.320 | 18 | -0.373 | -0.344 | 18 | +2.043 | +2.072 | 24 | +0.148 | +0.180 | 24 | +1.177 | +1.209 |
| SUIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 24 | -0.426 | -0.168 | 24 | +0.930 | +1.740 | 9 | -0.715 | -0.397 | 9 | +2.945 | +3.994 | 15 | -0.354 | -0.134 | 15 | +0.421 | +1.057 |
| SUIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 18 | -0.020 | -0.216 | 18 | +1.849 | +1.101 | 9 | -0.035 | -0.296 | 9 | +1.137 | +0.145 | 9 | +0.566 | +0.410 | 9 | +2.560 | +1.988 |
| SUIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 41 | -0.243 | -0.212 | 41 | +1.435 | +1.466 | 16 | -0.448 | -0.420 | 16 | +3.029 | +3.058 | 25 | -0.087 | -0.055 | 25 | +0.417 | +0.449 |
| SUIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 22 | -0.390 | -0.132 | 22 | -0.102 | +0.708 | 8 | -0.445 | -0.127 | 8 | +2.886 | +3.935 | 14 | -0.392 | -0.171 | 14 | -0.776 | -0.140 |
| SUIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 19 | -0.098 | -0.294 | 19 | +2.374 | +1.626 | 8 | -0.583 | -0.843 | 8 | +3.021 | +2.029 | 11 | +1.323 | +1.167 | 11 | +1.839 | +1.267 |
| SUIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 37 | -0.289 | -0.258 | 37 | +1.141 | +1.172 | 16 | -0.448 | -0.420 | 16 | +3.029 | +3.058 | 21 | -0.290 | -0.257 | 21 | -0.628 | -0.596 |
| SUIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 22 | -0.390 | -0.132 | 22 | -0.102 | +0.708 | 8 | -0.445 | -0.127 | 8 | +2.886 | +3.935 | 14 | -0.392 | -0.171 | 14 | -0.776 | -0.140 |
| SUIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 15 | -0.247 | -0.442 | 15 | +2.376 | +1.627 | 8 | -0.583 | -0.843 | 8 | +3.021 | +2.029 | 7 | +1.326 | +1.170 | 7 | +1.660 | +1.089 |
| SUIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 31 | +1.041 | +1.072 | 31 | +0.233 | +0.264 | 11 | +0.599 | +0.628 | 11 | +2.460 | +2.489 | 20 | +1.485 | +1.517 | 20 | +0.080 | +0.113 |
| SUIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 17 | +0.599 | +0.857 | 17 | -0.063 | +0.747 | 8 | -0.331 | -0.013 | 8 | +0.403 | +1.452 | 9 | +1.784 | +2.004 | 9 | -0.065 | +0.571 |
| SUIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 14 | +1.332 | +1.136 | 14 | +0.741 | -0.007 | 3 | +1.901 | +1.640 | 3 | +4.132 | +3.140 | 11 | +1.036 | +0.880 | 11 | +0.228 | -0.343 |
| SUIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 25 | +0.682 | +0.713 | 25 | -0.067 | -0.036 | 11 | +0.599 | +0.628 | 11 | +2.460 | +2.489 | 14 | +1.165 | +1.197 | 14 | -0.596 | -0.564 |
| SUIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 15 | +0.299 | +0.556 | 15 | -0.776 | +0.035 | 8 | -0.331 | -0.013 | 8 | +0.403 | +1.452 | 7 | +1.344 | +1.565 | 7 | -0.779 | -0.143 |
| SUIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 10 | +1.306 | +1.111 | 10 | +0.200 | -0.549 | 3 | +1.901 | +1.640 | 3 | +4.132 | +3.140 | 7 | +0.984 | +0.828 | 7 | -0.415 | -0.986 |
| SUIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 33 | -0.260 | -0.229 | 32 | +0.239 | +0.269 | 12 | -0.179 | -0.150 | 12 | +2.845 | +2.874 | 21 | -0.260 | -0.228 | 20 | -0.787 | -0.755 |
| SUIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 18 | -0.915 | -0.658 | 17 | -2.007 | -1.197 | 7 | -0.553 | -0.235 | 7 | +1.561 | +2.610 | 11 | -0.970 | -0.749 | 10 | -2.975 | -2.339 |
| SUIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 15 | +2.451 | +2.256 | 15 | +4.677 | +3.928 | 5 | -0.015 | -0.276 | 5 | +5.483 | +4.491 | 10 | +3.184 | +3.029 | 10 | +3.486 | +2.914 |
| SUIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 26 | -0.175 | -0.144 | 25 | +1.557 | +1.588 | 9 | -0.560 | -0.532 | 9 | +1.554 | +1.583 | 17 | +0.794 | +0.826 | 16 | +1.474 | +1.506 |
| SUIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 15 | -0.585 | -0.327 | 14 | -1.684 | -0.874 | 6 | -0.716 | -0.397 | 6 | -0.509 | +0.540 | 9 | -0.585 | -0.365 | 8 | -1.684 | -1.048 |
| SUIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 11 | +1.556 | +1.361 | 11 | +5.481 | +4.733 | 3 | -0.353 | -0.614 | 3 | +5.476 | +4.484 | 8 | +3.066 | +2.910 | 8 | +3.986 | +3.414 |
| SUIUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 71 | -0.576 | -0.545 | 68 | -0.802 | -0.771 | 20 | -0.593 | -0.564 | 20 | -2.673 | -2.644 | 51 | -0.577 | -0.545 | 48 | +0.750 | +0.783 |
| SUIUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 50 | -0.279 | -0.021 | 48 | +0.644 | +1.454 | 13 | -0.499 | -0.181 | 13 | -3.150 | -2.101 | 37 | -0.212 | +0.008 | 35 | +0.811 | +1.447 |
| SUIUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 21 | -2.679 | -2.875 | 20 | -1.996 | -2.744 | 7 | -2.910 | -3.170 | 7 | -2.238 | -3.230 | 14 | -2.161 | -2.317 | 13 | -1.354 | -1.925 |
| SUIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 7 | -1.608 | -1.596 | 6 | -1.424 | -1.412 | 2 | +0.495 | +0.506 | 2 | -19.715 | -19.704 | 5 | -1.608 | -1.596 | 4 | +3.811 | +3.823 |
| SUIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 4 | -0.753 | -0.434 | 4 | -1.421 | +0.284 | 1 | +2.862 | +3.295 | 1 | -3.466 | -2.109 | 3 | -1.604 | -1.334 | 3 | +0.624 | +2.655 |
| SUIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 3 | -1.872 | -2.167 | 2 | -14.483 | -16.165 | 1 | -1.872 | -2.283 | 1 | -35.963 | -37.298 | 2 | +0.262 | +0.016 | 1 | +6.997 | +4.991 |
| SUIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 6 | -0.755 | -0.743 | 6 | -1.424 | -1.412 | 2 | +0.495 | +0.506 | 2 | -19.715 | -19.704 | 4 | -0.755 | -0.743 | 4 | +3.811 | +3.823 |
| SUIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 4 | -0.753 | -0.434 | 4 | -1.421 | +0.284 | 1 | +2.862 | +3.295 | 1 | -3.466 | -2.109 | 3 | -1.604 | -1.334 | 3 | +0.624 | +2.655 |
| SUIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 2 | +0.725 | +0.429 | 2 | -14.483 | -16.165 | 1 | -1.872 | -2.283 | 1 | -35.963 | -37.298 | 1 | +3.321 | +3.076 | 1 | +6.997 | +4.991 |
| SUIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 7 | +1.944 | +1.956 | 6 | -1.735 | -1.724 | 3 | +2.335 | +2.346 | 3 | -3.466 | -3.455 | 4 | +1.909 | +1.922 | 3 | -0.003 | +0.009 |
| SUIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 3 | +2.861 | +3.180 | 3 | -0.002 | +1.703 | 1 | +2.862 | +3.295 | 1 | -3.466 | -2.109 | 2 | +3.768 | +4.038 | 2 | +19.862 | +21.892 |
| SUIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 4 | +1.910 | +1.615 | 3 | -23.381 | -25.063 | 2 | +0.961 | +0.550 | 2 | -9.625 | -10.961 | 2 | +1.908 | +1.662 | 1 | -29.975 | -31.982 |
| SUIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 6 | +1.911 | +1.922 | 5 | -3.467 | -3.456 | 3 | +2.335 | +2.346 | 3 | -3.466 | -3.455 | 3 | +1.877 | +1.889 | 2 | -14.989 | -14.977 |
| SUIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 2 | +0.324 | +0.643 | 2 | -1.734 | -0.029 | 1 | +2.862 | +3.295 | 1 | -3.466 | -2.109 | 1 | -2.213 | -1.944 | 1 | -0.002 | +2.028 |
| SUIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 4 | +1.910 | +1.615 | 3 | -23.381 | -25.063 | 2 | +0.961 | +0.550 | 2 | -9.625 | -10.961 | 2 | +1.908 | +1.662 | 1 | -29.975 | -31.982 |
| SUIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 4 | +0.757 | +0.769 | 4 | +2.018 | +2.029 | 3 | +1.396 | +1.407 | 3 | +2.694 | +2.705 | 1 | -0.517 | -0.505 | 1 | +1.343 | +1.354 |
| SUIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 2 | +3.149 | +3.468 | 2 | +2.513 | +4.218 | 1 | +6.816 | +7.250 | 1 | +3.683 | +5.041 | 1 | -0.517 | -0.248 | 1 | +1.343 | +3.373 |
| SUIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 2 | +0.756 | +0.461 | 2 | -6.722 | -8.404 | 2 | +0.756 | +0.345 | 2 | -6.722 | -8.058 | 0 | — | — | 0 | — | — |
| SUIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 4 | +0.757 | +0.769 | 4 | +2.018 | +2.029 | 3 | +1.396 | +1.407 | 3 | +2.694 | +2.705 | 1 | -0.517 | -0.505 | 1 | +1.343 | +1.354 |
| SUIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 2 | +3.149 | +3.468 | 2 | +2.513 | +4.218 | 1 | +6.816 | +7.250 | 1 | +3.683 | +5.041 | 1 | -0.517 | -0.248 | 1 | +1.343 | +3.373 |
| SUIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 2 | +0.756 | +0.461 | 2 | -6.722 | -8.404 | 2 | +0.756 | +0.345 | 2 | -6.722 | -8.058 | 0 | — | — | 0 | — | — |
| SUIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 9 | +0.824 | +0.836 | 8 | +2.216 | +2.227 | 4 | +0.424 | +0.435 | 4 | -0.932 | -0.921 | 5 | +0.824 | +0.836 | 4 | +3.471 | +3.483 |
| SUIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 4 | +0.784 | +1.103 | 4 | +2.216 | +3.921 | 1 | +4.952 | +5.386 | 1 | +2.321 | +3.679 | 3 | +0.742 | +1.012 | 3 | +2.112 | +4.142 |
| SUIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 5 | +1.016 | +0.720 | 4 | -0.056 | -1.738 | 3 | -0.170 | -0.582 | 3 | -4.185 | -5.521 | 2 | +1.371 | +1.125 | 1 | +4.830 | +2.823 |
| SUIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 9 | +1.016 | +1.028 | 8 | +2.863 | +2.875 | 3 | +1.017 | +1.029 | 3 | +2.321 | +2.332 | 6 | +1.030 | +1.042 | 5 | +3.406 | +3.418 |
| SUIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 4 | +0.784 | +1.103 | 4 | +2.216 | +3.921 | 1 | +4.952 | +5.386 | 1 | +2.321 | +3.679 | 3 | +0.742 | +1.012 | 3 | +2.112 | +4.142 |
| SUIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 5 | +1.239 | +0.943 | 4 | +3.739 | +2.057 | 2 | +0.424 | +0.013 | 2 | -0.055 | -1.390 | 3 | +1.504 | +1.258 | 2 | +4.117 | +2.110 |
| SUIUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 6 | -0.762 | -0.750 | 6 | -14.927 | -14.916 | 5 | -0.413 | -0.402 | 5 | -14.944 | -14.932 | 1 | -1.109 | -1.097 | 1 | -4.582 | -4.570 |
| SUIUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 1 | -1.109 | -0.790 | 1 | -4.582 | -2.877 | 0 | — | — | 0 | — | — | 1 | -1.109 | -0.839 | 1 | -4.582 | -2.551 |
| SUIUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 5 | -0.413 | -0.708 | 5 | -14.944 | -16.626 | 5 | -0.413 | -0.824 | 5 | -14.944 | -16.279 | 0 | — | — | 0 | — | — |
| LTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 385 | -0.064 | +0.024 | 384 | +0.054 | +0.142 | 249 | -0.001 | +0.080 | 249 | -0.028 | +0.054 | 136 | -0.368 | -0.263 | 135 | +0.226 | +0.331 |
| LTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 209 | -0.028 | -0.063 | 208 | -0.129 | -0.163 | 140 | +0.110 | +0.049 | 140 | -0.141 | -0.229 | 69 | -0.360 | -0.341 | 68 | -0.050 | +0.021 |
| LTCUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 176 | -0.238 | -0.027 | 176 | +0.419 | +0.629 | 109 | -0.059 | +0.165 | 109 | +0.130 | +0.380 | 67 | -0.557 | -0.367 | 67 | +0.991 | +1.131 |
| LTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 340 | -0.084 | +0.004 | 339 | -0.143 | -0.055 | 219 | -0.033 | +0.049 | 219 | -0.223 | -0.141 | 121 | -0.353 | -0.248 | 120 | +0.197 | +0.303 |
| LTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 189 | -0.061 | -0.095 | 188 | -0.234 | -0.268 | 124 | +0.031 | -0.030 | 124 | -0.223 | -0.310 | 65 | -0.330 | -0.311 | 64 | -0.244 | -0.174 |
| LTCUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 151 | -0.268 | -0.057 | 151 | +0.124 | +0.335 | 95 | -0.209 | +0.015 | 95 | -0.125 | +0.125 | 56 | -0.590 | -0.400 | 56 | +0.902 | +1.041 |
| LTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 335 | -0.204 | -0.116 | 334 | +0.320 | +0.408 | 212 | +0.054 | +0.136 | 212 | +0.230 | +0.312 | 123 | -0.622 | -0.517 | 122 | +0.354 | +0.459 |
| LTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 189 | -0.015 | -0.050 | 188 | +0.034 | +0.000 | 124 | +0.474 | +0.413 | 124 | +0.168 | +0.081 | 65 | -0.881 | -0.861 | 64 | -0.481 | -0.410 |
| LTCUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 146 | -0.331 | -0.120 | 146 | +0.629 | +0.839 | 88 | -0.324 | -0.100 | 88 | +0.568 | +0.819 | 58 | -0.364 | -0.173 | 58 | +0.806 | +0.946 |
| LTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 304 | -0.072 | +0.016 | 303 | +0.388 | +0.476 | 195 | +0.083 | +0.165 | 195 | +0.296 | +0.378 | 109 | -0.602 | -0.497 | 108 | +0.372 | +0.477 |
| LTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 176 | +0.051 | +0.017 | 175 | +0.151 | +0.117 | 115 | +0.531 | +0.469 | 115 | +0.173 | +0.086 | 61 | -0.625 | -0.605 | 60 | -0.550 | -0.480 |
| LTCUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 128 | -0.294 | -0.083 | 128 | +0.697 | +0.907 | 80 | -0.301 | -0.076 | 80 | +0.637 | +0.887 | 48 | -0.266 | -0.076 | 48 | +1.006 | +1.145 |
| LTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 285 | -0.104 | -0.016 | 285 | +0.460 | +0.548 | 179 | -0.058 | +0.024 | 179 | +0.313 | +0.395 | 106 | -0.143 | -0.038 | 106 | +0.953 | +1.058 |
| LTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 159 | -0.065 | -0.100 | 159 | +0.319 | +0.285 | 101 | +0.081 | +0.020 | 101 | +0.315 | +0.228 | 58 | -0.287 | -0.267 | 58 | +0.311 | +0.382 |
| LTCUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 126 | -0.131 | +0.080 | 126 | +0.750 | +0.960 | 78 | -0.199 | +0.026 | 78 | +0.287 | +0.537 | 48 | -0.088 | +0.102 | 48 | +1.359 | +1.499 |
| LTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 257 | -0.122 | -0.034 | 257 | +0.588 | +0.677 | 163 | -0.126 | -0.045 | 163 | +0.362 | +0.444 | 94 | -0.131 | -0.026 | 94 | +1.194 | +1.299 |
| LTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 146 | -0.092 | -0.126 | 146 | +0.313 | +0.279 | 92 | +0.095 | +0.034 | 92 | +0.386 | +0.299 | 54 | -0.339 | -0.319 | 54 | +0.073 | +0.143 |
| LTCUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 111 | -0.150 | +0.061 | 111 | +1.265 | +1.475 | 71 | -0.214 | +0.011 | 71 | +0.352 | +0.602 | 40 | -0.068 | +0.123 | 40 | +1.730 | +1.870 |
| LTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 293 | -0.129 | -0.041 | 292 | -0.526 | -0.438 | 190 | -0.022 | +0.060 | 190 | -0.193 | -0.111 | 103 | -0.327 | -0.222 | 102 | -1.003 | -0.898 |
| LTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 165 | +0.043 | +0.008 | 164 | -0.475 | -0.509 | 107 | +0.057 | -0.004 | 107 | -0.159 | -0.247 | 58 | -0.071 | -0.051 | 57 | -1.810 | -1.740 |
| LTCUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 128 | -0.280 | -0.069 | 128 | -0.591 | -0.380 | 83 | -0.248 | -0.023 | 83 | -0.601 | -0.351 | 45 | -0.321 | -0.131 | 45 | -0.583 | -0.444 |
| LTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 289 | +0.072 | +0.160 | 288 | -0.200 | -0.111 | 187 | +0.116 | +0.197 | 187 | -0.204 | -0.122 | 102 | -0.039 | +0.066 | 101 | -0.137 | -0.032 |
| LTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 161 | +0.205 | +0.171 | 160 | -0.232 | -0.266 | 102 | +0.089 | +0.028 | 102 | -0.188 | -0.275 | 59 | +0.473 | +0.492 | 58 | -1.007 | -0.937 |
| LTCUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 128 | -0.125 | +0.086 | 128 | +0.339 | +0.549 | 85 | +0.357 | +0.582 | 85 | -0.306 | -0.055 | 43 | -0.321 | -0.131 | 43 | +0.777 | +0.917 |
| LTCUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 616 | +0.209 | +0.297 | 614 | +0.651 | +0.739 | 374 | +0.269 | +0.351 | 374 | +0.618 | +0.699 | 242 | +0.038 | +0.143 | 240 | +0.646 | +0.751 |
| LTCUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 311 | +0.219 | +0.185 | 310 | +0.458 | +0.424 | 189 | +0.304 | +0.243 | 189 | +0.490 | +0.403 | 122 | -0.060 | -0.041 | 121 | +0.348 | +0.419 |
| LTCUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 305 | +0.197 | +0.408 | 304 | +0.938 | +1.149 | 185 | +0.222 | +0.447 | 185 | +0.953 | +1.203 | 120 | +0.091 | +0.281 | 119 | +0.821 | +0.961 |
| LTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 93 | +0.004 | +0.046 | 93 | +0.473 | +0.515 | 61 | -0.023 | +0.016 | 61 | +0.722 | +0.761 | 32 | +0.020 | +0.071 | 32 | -0.157 | -0.106 |
| LTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 55 | +0.008 | -0.023 | 55 | +0.983 | +0.877 | 38 | +0.077 | +0.008 | 38 | +0.704 | +0.509 | 17 | -0.303 | -0.248 | 17 | +3.056 | +3.170 |
| LTCUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 38 | -0.078 | +0.037 | 38 | -0.760 | -0.571 | 23 | -0.430 | -0.284 | 23 | +0.896 | +1.168 | 15 | +0.243 | +0.291 | 15 | -1.333 | -1.345 |
| LTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 75 | -0.027 | +0.015 | 75 | +0.435 | +0.477 | 49 | -0.201 | -0.162 | 49 | +0.724 | +0.762 | 26 | +0.018 | +0.069 | 26 | -0.894 | -0.843 |
| LTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 45 | +0.008 | -0.023 | 45 | +0.983 | +0.877 | 31 | +0.124 | +0.056 | 31 | +0.724 | +0.530 | 14 | -0.158 | -0.103 | 14 | +3.545 | +3.659 |
| LTCUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 30 | -0.255 | -0.140 | 30 | -1.060 | -0.871 | 18 | -0.504 | -0.358 | 18 | +0.058 | +0.330 | 12 | +0.147 | +0.195 | 12 | -1.764 | -1.775 |
| LTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 80 | +0.079 | +0.121 | 80 | +0.423 | +0.465 | 51 | +0.283 | +0.322 | 51 | +0.418 | +0.457 | 29 | -0.345 | -0.293 | 29 | +0.419 | +0.470 |
| LTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 51 | +0.121 | +0.091 | 51 | +0.983 | +0.877 | 35 | +0.299 | +0.231 | 35 | +0.986 | +0.791 | 16 | -0.417 | -0.362 | 16 | +0.485 | +0.599 |
| LTCUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 29 | -0.183 | -0.068 | 29 | -0.400 | -0.211 | 16 | -0.038 | +0.108 | 16 | -1.539 | -1.267 | 13 | -0.295 | -0.248 | 13 | +0.420 | +0.408 |
| LTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 70 | +0.080 | +0.122 | 70 | +0.293 | +0.335 | 46 | +0.172 | +0.211 | 46 | +0.298 | +0.337 | 24 | -0.178 | -0.127 | 24 | -0.098 | -0.047 |
| LTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 47 | +0.121 | +0.091 | 47 | +0.983 | +0.877 | 33 | +0.286 | +0.217 | 33 | +0.986 | +0.791 | 14 | -0.177 | -0.122 | 14 | +0.487 | +0.602 |
| LTCUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 23 | -0.184 | -0.069 | 23 | -1.454 | -1.265 | 13 | -0.173 | -0.027 | 13 | -1.632 | -1.359 | 10 | -0.157 | -0.110 | 10 | -0.100 | -0.112 |
| LTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 74 | +0.284 | +0.326 | 74 | -1.017 | -0.975 | 50 | -0.024 | +0.015 | 50 | -1.125 | -1.086 | 24 | +0.446 | +0.497 | 24 | -0.619 | -0.568 |
| LTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 48 | +0.218 | +0.188 | 48 | +0.454 | +0.349 | 35 | +0.284 | +0.215 | 35 | +1.206 | +1.011 | 13 | +0.137 | +0.192 | 13 | -1.112 | -0.997 |
| LTCUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 26 | +0.375 | +0.490 | 26 | -2.584 | -2.395 | 15 | -0.544 | -0.399 | 15 | -2.742 | -2.470 | 11 | +0.448 | +0.496 | 11 | +0.427 | +0.415 |
| LTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 65 | +0.277 | +0.319 | 65 | -0.934 | -0.892 | 43 | -0.166 | -0.127 | 43 | -0.929 | -0.890 | 22 | +0.446 | +0.497 | 22 | -0.619 | -0.568 |
| LTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 45 | +0.159 | +0.128 | 45 | +0.680 | +0.574 | 32 | +0.222 | +0.154 | 32 | +1.313 | +1.118 | 13 | +0.137 | +0.192 | 13 | -1.112 | -0.997 |
| LTCUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 20 | +0.375 | +0.490 | 20 | -2.984 | -2.794 | 11 | -0.544 | -0.399 | 11 | -3.281 | -3.009 | 9 | +0.448 | +0.496 | 9 | +0.427 | +0.415 |
| LTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 76 | +0.030 | +0.072 | 76 | -0.508 | -0.466 | 51 | -0.006 | +0.033 | 51 | -0.469 | -0.430 | 25 | +0.103 | +0.154 | 25 | -0.545 | -0.494 |
| LTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 42 | +0.444 | +0.413 | 42 | +0.811 | +0.706 | 31 | +0.351 | +0.283 | 31 | -0.171 | -0.366 | 11 | +0.724 | +0.779 | 11 | +2.716 | +2.831 |
| LTCUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 34 | -0.407 | -0.292 | 34 | -2.319 | -2.130 | 20 | -0.958 | -0.812 | 20 | -2.565 | -2.292 | 14 | -0.294 | -0.246 | 14 | -1.420 | -1.432 |
| LTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 72 | -0.091 | -0.049 | 72 | -0.503 | -0.462 | 50 | -0.464 | -0.425 | 50 | -0.578 | -0.539 | 22 | +0.350 | +0.401 | 22 | -0.040 | +0.011 |
| LTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 41 | +0.351 | +0.320 | 41 | +0.276 | +0.171 | 31 | +0.044 | -0.024 | 31 | -0.169 | -0.364 | 10 | +0.738 | +0.793 | 10 | +4.668 | +4.782 |
| LTCUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 31 | -0.361 | -0.246 | 31 | -2.107 | -1.918 | 19 | -1.037 | -0.891 | 19 | -2.527 | -2.255 | 12 | -0.237 | -0.190 | 12 | -0.672 | -0.684 |
| LTCUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 122 | +0.282 | +0.324 | 122 | +1.472 | +1.514 | 78 | +0.056 | +0.094 | 78 | +1.781 | +1.820 | 44 | +1.248 | +1.299 | 44 | +0.887 | +0.938 |
| LTCUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 58 | +0.161 | +0.130 | 58 | +0.469 | +0.364 | 38 | +0.084 | +0.016 | 38 | +1.019 | +0.824 | 20 | +0.532 | +0.587 | 20 | -0.399 | -0.285 |
| LTCUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 64 | +0.784 | +0.899 | 64 | +2.111 | +2.300 | 40 | +0.039 | +0.184 | 40 | +1.879 | +2.151 | 24 | +1.583 | +1.631 | 24 | +3.056 | +3.044 |
| LTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 19 | +0.911 | +0.927 | 17 | -1.536 | -1.520 | 11 | +0.913 | +0.928 | 11 | -0.040 | -0.025 | 8 | +0.901 | +0.920 | 6 | -3.751 | -3.733 |
| LTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 10 | +1.099 | +1.051 | 9 | -2.091 | -1.633 | 7 | +1.285 | +1.222 | 7 | -1.534 | -1.534 | 3 | -0.382 | -0.396 | 2 | -3.746 | -1.958 |
| LTCUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 9 | +0.651 | +0.730 | 8 | -0.687 | -1.114 | 4 | -0.698 | -0.605 | 4 | +1.354 | +1.384 | 5 | +1.152 | +1.204 | 4 | -3.381 | -5.134 |
| LTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 16 | +0.781 | +0.797 | 14 | -1.815 | -1.799 | 9 | +0.912 | +0.927 | 9 | -1.536 | -1.521 | 7 | +0.650 | +0.669 | 5 | -2.097 | -2.079 |
| LTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | +1.099 | +1.051 | 7 | -3.107 | -2.649 | 5 | +1.285 | +1.222 | 5 | -3.107 | -3.107 | 3 | -0.382 | -0.396 | 2 | -3.746 | -1.958 |
| LTCUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 8 | +0.445 | +0.525 | 7 | -0.044 | -0.471 | 4 | -0.698 | -0.605 | 4 | +1.354 | +1.384 | 4 | +0.897 | +0.949 | 3 | -1.334 | -3.086 |
| LTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 17 | +0.569 | +0.585 | 16 | -0.658 | -0.642 | 10 | +0.742 | +0.757 | 10 | +1.693 | +1.708 | 7 | -0.383 | -0.364 | 6 | -3.124 | -3.106 |
| LTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 9 | +0.914 | +0.866 | 8 | -0.452 | +0.006 | 6 | +1.032 | +0.969 | 6 | +1.924 | +1.924 | 3 | -0.383 | -0.397 | 2 | -3.119 | -1.331 |
| LTCUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 8 | -0.003 | +0.077 | 8 | -0.662 | -1.088 | 4 | -0.390 | -0.298 | 4 | +1.382 | +1.412 | 4 | +0.290 | +0.342 | 4 | -3.621 | -5.373 |
| LTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 13 | +0.568 | +0.584 | 12 | -1.432 | -1.416 | 7 | +0.570 | +0.585 | 7 | +0.012 | +0.027 | 6 | +0.384 | +0.403 | 5 | -2.097 | -2.079 |
| LTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 6 | +0.268 | +0.220 | 5 | -2.091 | -1.633 | 3 | +0.914 | +0.851 | 3 | -1.534 | -1.534 | 3 | -0.383 | -0.397 | 2 | -3.119 | -1.331 |
| LTCUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 7 | +0.566 | +0.646 | 7 | +0.008 | -0.418 | 4 | -0.390 | -0.298 | 4 | +1.382 | +1.412 | 3 | +1.152 | +1.204 | 3 | -1.334 | -3.086 |
| LTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 13 | +0.048 | +0.064 | 13 | -0.479 | -0.464 | 8 | +0.335 | +0.350 | 8 | +0.170 | +0.185 | 5 | +0.048 | +0.067 | 5 | -4.151 | -4.133 |
| LTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 7 | +0.822 | +0.774 | 7 | -0.475 | -0.017 | 5 | +0.822 | +0.759 | 5 | -0.053 | -0.053 | 2 | +0.239 | +0.225 | 2 | -2.311 | -0.523 |
| LTCUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 6 | -0.262 | -0.182 | 6 | -2.381 | -2.808 | 3 | -1.638 | -1.545 | 3 | +1.147 | +1.177 | 3 | +0.048 | +0.100 | 3 | -5.908 | -7.660 |
| LTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 10 | -0.050 | -0.034 | 10 | -1.007 | -0.991 | 6 | -0.893 | -0.878 | 6 | -0.795 | -0.780 | 4 | +0.297 | +0.316 | 4 | -2.314 | -2.296 |
| LTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 5 | -0.148 | -0.196 | 5 | -1.534 | -1.075 | 3 | -0.148 | -0.211 | 3 | -1.534 | -1.534 | 2 | +0.239 | +0.225 | 2 | -2.311 | -0.523 |
| LTCUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 5 | +0.048 | +0.128 | 5 | +1.147 | +0.720 | 3 | -1.638 | -1.545 | 3 | +1.147 | +1.177 | 2 | +0.295 | +0.346 | 2 | -5.039 | -6.791 |
| LTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 13 | +0.136 | +0.152 | 13 | +1.434 | +1.450 | 9 | -0.778 | -0.763 | 9 | +1.832 | +1.847 | 4 | +2.015 | +2.034 | 4 | -0.205 | -0.187 |
| LTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 8 | -0.476 | -0.524 | 8 | +1.089 | +1.547 | 6 | -0.476 | -0.539 | 6 | +1.298 | +1.297 | 2 | +0.899 | +0.885 | 2 | -1.010 | +0.779 |
| LTCUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 5 | +0.734 | +0.813 | 5 | +3.298 | +2.871 | 3 | -0.778 | -0.685 | 3 | +3.299 | +3.329 | 2 | +2.015 | +2.066 | 2 | +2.497 | +0.745 |
| LTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 9 | -0.373 | -0.357 | 9 | +1.413 | +1.429 | 6 | -0.731 | -0.716 | 6 | +0.931 | +0.946 | 3 | +2.554 | +2.573 | 3 | +1.413 | +1.431 |
| LTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 5 | -1.089 | -1.137 | 5 | -3.180 | -2.722 | 3 | -1.089 | -1.152 | 3 | -3.180 | -3.180 | 2 | +0.899 | +0.885 | 2 | -1.010 | +0.779 |
| LTCUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 4 | +0.178 | +0.258 | 4 | +2.363 | +1.936 | 3 | -0.378 | -0.285 | 3 | +1.429 | +1.459 | 1 | +2.554 | +2.606 | 1 | +6.817 | +5.064 |
| LTCUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 11 | -0.333 | -0.317 | 11 | -2.606 | -2.590 | 9 | +0.093 | +0.108 | 9 | +0.238 | +0.253 | 2 | -8.005 | -7.986 | 2 | -14.234 | -14.216 |
| LTCUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 4 | +0.193 | +0.146 | 4 | -3.159 | -2.701 | 4 | +0.193 | +0.130 | 4 | -3.159 | -3.159 | 0 | — | — | 0 | — | — |
| LTCUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 7 | -0.572 | -0.492 | 7 | +0.233 | -0.193 | 5 | -0.333 | -0.240 | 5 | +0.556 | +0.586 | 2 | -8.005 | -7.953 | 2 | -14.234 | -15.986 |
| XMRUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 333 | -0.128 | -0.041 | 333 | -0.219 | -0.132 | 224 | -0.112 | -0.027 | 224 | -0.198 | -0.113 | 109 | -0.134 | -0.045 | 109 | -0.379 | -0.290 |
| XMRUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 183 | +0.016 | -0.103 | 183 | +0.032 | -0.515 | 118 | +0.149 | +0.006 | 118 | +0.069 | -0.419 | 65 | -0.327 | -0.405 | 65 | -0.182 | -0.810 |
| XMRUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 150 | -0.259 | +0.034 | 150 | -0.853 | -0.133 | 106 | -0.343 | -0.029 | 106 | -1.102 | -0.443 | 44 | -0.125 | +0.132 | 44 | -0.799 | +0.009 |
| XMRUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 295 | -0.122 | -0.035 | 295 | -0.518 | -0.431 | 198 | +0.009 | +0.094 | 198 | -0.309 | -0.223 | 97 | -0.273 | -0.183 | 97 | -0.796 | -0.706 |
| XMRUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 165 | +0.017 | -0.102 | 165 | -0.145 | -0.691 | 106 | +0.150 | +0.006 | 106 | -0.012 | -0.500 | 59 | -0.327 | -0.406 | 59 | -0.301 | -0.929 |
| XMRUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 130 | -0.288 | +0.005 | 130 | -0.855 | -0.135 | 92 | -0.322 | -0.008 | 92 | -0.737 | -0.079 | 38 | -0.253 | +0.004 | 38 | -0.931 | -0.123 |
| XMRUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 295 | -0.134 | -0.047 | 295 | -0.237 | -0.150 | 203 | -0.218 | -0.133 | 203 | -0.123 | -0.038 | 92 | -0.056 | +0.033 | 92 | -0.535 | -0.446 |
| XMRUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 158 | +0.062 | -0.058 | 158 | +0.629 | +0.083 | 104 | +0.139 | -0.004 | 104 | +0.632 | +0.143 | 54 | -0.294 | -0.373 | 54 | +0.548 | -0.080 |
| XMRUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 137 | -0.639 | -0.346 | 137 | -1.005 | -0.285 | 99 | -0.761 | -0.447 | 99 | -1.312 | -0.654 | 38 | +0.296 | +0.553 | 38 | -0.896 | -0.088 |
| XMRUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 262 | -0.107 | -0.020 | 262 | -0.497 | -0.410 | 178 | -0.115 | -0.030 | 178 | -0.151 | -0.066 | 84 | -0.054 | +0.035 | 84 | -0.764 | -0.675 |
| XMRUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 141 | +0.016 | -0.104 | 141 | +0.216 | -0.330 | 91 | +0.096 | -0.047 | 91 | +0.569 | +0.081 | 50 | -0.437 | -0.515 | 50 | -0.333 | -0.962 |
| XMRUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 121 | -0.303 | -0.011 | 121 | -1.112 | -0.393 | 87 | -0.731 | -0.417 | 87 | -1.480 | -0.822 | 34 | +0.456 | +0.713 | 34 | -0.896 | -0.088 |
| XMRUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 257 | +0.026 | +0.113 | 257 | +0.303 | +0.390 | 175 | +0.059 | +0.145 | 175 | +0.647 | +0.732 | 82 | -0.135 | -0.046 | 82 | -0.623 | -0.534 |
| XMRUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 132 | -0.050 | -0.169 | 132 | +0.672 | +0.126 | 86 | +0.053 | -0.090 | 86 | +1.083 | +0.595 | 46 | -0.373 | -0.452 | 46 | +0.138 | -0.491 |
| XMRUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 125 | +0.052 | +0.345 | 125 | -0.571 | +0.149 | 89 | +0.084 | +0.397 | 89 | -0.116 | +0.543 | 36 | -0.120 | +0.137 | 36 | -0.740 | +0.067 |
| XMRUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 224 | +0.072 | +0.159 | 224 | +0.389 | +0.476 | 152 | +0.188 | +0.273 | 152 | +0.875 | +0.960 | 72 | -0.130 | -0.041 | 72 | -0.726 | -0.636 |
| XMRUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 116 | -0.081 | -0.200 | 116 | +0.757 | +0.211 | 75 | +0.059 | -0.084 | 75 | +1.325 | +0.837 | 41 | -0.450 | -0.528 | 41 | -0.501 | -1.130 |
| XMRUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 108 | +0.257 | +0.550 | 108 | -0.435 | +0.285 | 77 | +0.248 | +0.562 | 77 | +0.139 | +0.798 | 31 | +0.379 | +0.636 | 31 | -0.750 | +0.058 |
| XMRUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 281 | -0.174 | -0.087 | 281 | -0.486 | -0.399 | 193 | -0.139 | -0.054 | 193 | -0.487 | -0.401 | 88 | -0.314 | -0.225 | 88 | -0.479 | -0.389 |
| XMRUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 165 | -0.015 | -0.134 | 165 | +0.286 | -0.260 | 114 | +0.050 | -0.094 | 114 | +0.610 | +0.122 | 51 | -0.229 | -0.307 | 51 | -0.530 | -1.159 |
| XMRUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 116 | -0.335 | -0.042 | 116 | -1.477 | -0.757 | 79 | -0.287 | +0.027 | 79 | -1.888 | -1.230 | 37 | -0.572 | -0.315 | 37 | -0.371 | +0.437 |
| XMRUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 243 | -0.174 | -0.087 | 243 | -0.931 | -0.844 | 163 | -0.109 | -0.024 | 163 | -0.977 | -0.892 | 80 | -0.467 | -0.378 | 80 | -0.845 | -0.756 |
| XMRUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 135 | +0.036 | -0.083 | 135 | -0.010 | -0.557 | 93 | +0.224 | +0.080 | 93 | +0.559 | +0.071 | 42 | -0.252 | -0.330 | 42 | -1.139 | -1.768 |
| XMRUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 108 | -0.457 | -0.164 | 108 | -1.728 | -1.008 | 70 | -0.402 | -0.089 | 70 | -2.176 | -1.518 | 38 | -0.840 | -0.584 | 38 | -0.631 | +0.176 |
| XMRUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 760 | +0.052 | +0.139 | 759 | -0.158 | -0.071 | 501 | +0.002 | +0.087 | 501 | -0.375 | -0.290 | 259 | +0.096 | +0.185 | 258 | +0.349 | +0.439 |
| XMRUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 318 | +0.252 | +0.133 | 318 | +0.753 | +0.206 | 208 | +0.308 | +0.165 | 208 | +0.768 | +0.280 | 110 | +0.218 | +0.140 | 110 | +0.690 | +0.061 |
| XMRUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 442 | -0.074 | +0.219 | 441 | -0.757 | -0.037 | 293 | -0.150 | +0.164 | 293 | -0.939 | -0.281 | 149 | +0.049 | +0.306 | 148 | -0.060 | +0.748 |
| XMRUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 79 | +0.060 | +0.103 | 78 | -0.037 | +0.006 | 62 | +0.124 | +0.165 | 62 | +0.638 | +0.679 | 17 | -0.251 | -0.206 | 16 | -0.858 | -0.813 |
| XMRUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 48 | +0.983 | +0.753 | 47 | +0.848 | +0.097 | 40 | +0.984 | +0.767 | 40 | +1.011 | +0.503 | 8 | +0.677 | +0.415 | 7 | +0.628 | -0.421 |
| XMRUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 31 | -0.675 | -0.359 | 31 | -1.043 | -0.207 | 22 | -0.706 | -0.407 | 22 | +0.277 | +0.868 | 9 | -0.504 | -0.152 | 9 | -1.195 | -0.056 |
| XMRUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 71 | +0.068 | +0.110 | 70 | -0.128 | -0.086 | 56 | +0.193 | +0.235 | 56 | -0.035 | +0.006 | 15 | -0.251 | -0.206 | 14 | -0.937 | -0.891 |
| XMRUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 43 | +1.069 | +0.839 | 42 | +0.312 | -0.439 | 35 | +1.069 | +0.853 | 35 | -0.005 | -0.513 | 8 | +0.677 | +0.415 | 7 | +0.628 | -0.421 |
| XMRUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 28 | -0.651 | -0.335 | 28 | -1.277 | -0.441 | 21 | -0.675 | -0.376 | 21 | -0.067 | +0.524 | 7 | -0.507 | -0.155 | 7 | -1.695 | -0.556 |
| XMRUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 68 | +0.067 | +0.110 | 67 | +0.648 | +0.690 | 52 | +0.662 | +0.703 | 52 | +0.910 | +0.952 | 16 | -0.288 | -0.243 | 15 | -0.252 | -0.207 |
| XMRUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 40 | +0.898 | +0.668 | 39 | +0.649 | -0.102 | 32 | +0.987 | +0.771 | 32 | +0.910 | +0.402 | 8 | -0.074 | -0.337 | 7 | +0.621 | -0.428 |
| XMRUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 28 | -0.283 | +0.032 | 28 | +0.428 | +1.264 | 20 | -0.184 | +0.115 | 20 | +1.160 | +1.751 | 8 | -0.574 | -0.222 | 8 | -0.951 | +0.188 |
| XMRUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 60 | -0.050 | -0.007 | 59 | +0.314 | +0.357 | 46 | +0.253 | +0.294 | 46 | +0.481 | +0.523 | 14 | -0.288 | -0.243 | 13 | -0.252 | -0.207 |
| XMRUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 37 | +0.897 | +0.666 | 36 | +0.471 | -0.279 | 30 | +0.988 | +0.772 | 30 | +0.484 | -0.025 | 7 | -0.258 | -0.521 | 6 | -1.040 | -2.089 |
| XMRUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 23 | -0.329 | -0.014 | 23 | +0.206 | +1.042 | 16 | -0.656 | -0.357 | 16 | +0.425 | +1.016 | 7 | -0.311 | +0.041 | 7 | -0.240 | +0.899 |
| XMRUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 53 | +0.241 | +0.283 | 53 | +0.711 | +0.753 | 39 | +0.220 | +0.261 | 39 | +0.826 | +0.867 | 14 | +0.279 | +0.324 | 14 | -0.117 | -0.072 |
| XMRUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 29 | +0.350 | +0.119 | 29 | +0.313 | -0.437 | 23 | +0.362 | +0.145 | 23 | +0.827 | +0.319 | 6 | +0.045 | -0.217 | 6 | -1.787 | -2.836 |
| XMRUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 24 | +0.149 | +0.464 | 24 | +0.713 | +1.549 | 16 | +0.001 | +0.300 | 16 | +1.026 | +1.617 | 8 | +0.282 | +0.634 | 8 | -0.114 | +1.025 |
| XMRUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 46 | +0.271 | +0.313 | 46 | +0.682 | +0.725 | 33 | +0.221 | +0.263 | 33 | +0.827 | +0.869 | 13 | +0.318 | +0.363 | 13 | +0.019 | +0.064 |
| XMRUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 26 | +0.286 | +0.056 | 26 | +0.265 | -0.486 | 20 | +0.559 | +0.343 | 20 | +0.571 | +0.063 | 6 | +0.045 | -0.217 | 6 | -1.787 | -2.836 |
| XMRUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 20 | +0.189 | +0.504 | 20 | +0.714 | +1.550 | 13 | +0.059 | +0.358 | 13 | +1.282 | +1.873 | 7 | +0.318 | +0.670 | 7 | +0.019 | +1.158 |
| XMRUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 59 | +0.395 | +0.438 | 59 | +0.003 | +0.045 | 44 | +0.405 | +0.446 | 44 | -0.005 | +0.036 | 15 | +0.383 | +0.428 | 15 | +0.064 | +0.109 |
| XMRUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 37 | +0.447 | +0.216 | 37 | +0.813 | +0.062 | 29 | +0.653 | +0.436 | 29 | +0.381 | -0.127 | 8 | +0.270 | +0.008 | 8 | +2.428 | +1.379 |
| XMRUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 22 | -0.061 | +0.254 | 22 | -0.798 | +0.038 | 15 | -0.154 | +0.145 | 15 | -1.843 | -1.252 | 7 | +0.520 | +0.872 | 7 | -0.735 | +0.405 |
| XMRUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 61 | +0.416 | +0.458 | 61 | +0.380 | +0.422 | 46 | +0.483 | +0.524 | 46 | +0.191 | +0.232 | 15 | +0.159 | +0.204 | 15 | +1.173 | +1.218 |
| XMRUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 39 | +0.652 | +0.422 | 39 | +0.482 | -0.269 | 29 | +0.931 | +0.715 | 29 | +0.004 | -0.505 | 10 | +0.272 | +0.010 | 10 | +1.585 | +0.536 |
| XMRUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 22 | -0.304 | +0.012 | 22 | -0.676 | +0.160 | 17 | -0.213 | +0.085 | 17 | +0.727 | +1.318 | 5 | -0.435 | -0.083 | 5 | -0.740 | +0.400 |
| XMRUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 135 | +0.281 | +0.324 | 134 | -0.040 | +0.003 | 96 | +0.042 | +0.083 | 96 | -0.964 | -0.923 | 39 | +0.712 | +0.756 | 38 | +1.068 | +1.114 |
| XMRUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 45 | +0.573 | +0.343 | 45 | +0.772 | +0.022 | 33 | +0.527 | +0.311 | 33 | +0.582 | +0.074 | 12 | +1.179 | +0.916 | 12 | +1.586 | +0.537 |
| XMRUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 90 | +0.056 | +0.371 | 89 | -0.830 | +0.006 | 63 | -0.099 | +0.199 | 63 | -1.662 | -1.072 | 27 | +0.483 | +0.835 | 26 | +0.285 | +1.424 |
| XMRUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 13 | +0.313 | +0.330 | 13 | -0.942 | -0.925 | 8 | +0.189 | +0.205 | 8 | +1.464 | +1.480 | 5 | +0.678 | +0.697 | 5 | -1.376 | -1.357 |
| XMRUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 8 | +0.497 | +0.131 | 8 | -0.164 | -1.260 | 5 | +0.314 | +0.104 | 5 | +10.321 | +9.378 | 3 | +0.680 | +0.151 | 3 | -0.942 | -2.255 |
| XMRUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 5 | -0.082 | +0.319 | 5 | -0.952 | +0.178 | 3 | -0.080 | +0.163 | 3 | -0.771 | +0.204 | 2 | -0.073 | +0.494 | 2 | -9.752 | -8.402 |
| XMRUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 10 | +0.497 | +0.515 | 10 | -0.856 | -0.839 | 7 | +0.314 | +0.331 | 7 | -0.771 | -0.754 | 3 | +0.680 | +0.699 | 3 | -0.942 | -0.923 |
| XMRUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | +0.497 | +0.131 | 8 | -0.164 | -1.260 | 5 | +0.314 | +0.104 | 5 | +10.321 | +9.378 | 3 | +0.680 | +0.151 | 3 | -0.942 | -2.255 |
| XMRUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 2 | +0.733 | +1.133 | 2 | -0.859 | +0.271 | 2 | +0.733 | +0.976 | 2 | -0.859 | +0.117 | 0 | — | — | 0 | — | — |
| XMRUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 11 | +0.063 | +0.081 | 11 | -0.468 | -0.451 | 7 | +0.064 | +0.081 | 7 | -0.467 | -0.451 | 4 | -0.228 | -0.209 | 4 | -0.372 | -0.354 |
| XMRUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 7 | +0.063 | -0.303 | 7 | +0.200 | -0.896 | 4 | +1.082 | +0.872 | 4 | +3.825 | +2.882 | 3 | -1.134 | -1.663 | 3 | +0.200 | -1.113 |
| XMRUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 4 | +0.342 | +0.743 | 4 | -0.718 | +0.412 | 3 | -0.286 | -0.043 | 3 | -0.467 | +0.509 | 1 | +0.969 | +1.536 | 1 | -6.711 | -5.361 |
| XMRUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 10 | -0.111 | -0.094 | 10 | -0.134 | -0.117 | 7 | +0.064 | +0.081 | 7 | -0.467 | -0.451 | 3 | -1.134 | -1.115 | 3 | +0.200 | +0.218 |
| XMRUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | +0.063 | -0.303 | 7 | +0.200 | -0.896 | 4 | +1.082 | +0.872 | 4 | +3.825 | +2.882 | 3 | -1.134 | -1.663 | 3 | +0.200 | -1.113 |
| XMRUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 3 | -0.286 | +0.115 | 3 | -0.467 | +0.663 | 3 | -0.286 | -0.043 | 3 | -0.467 | +0.509 | 0 | — | — | 0 | — | — |
| XMRUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 9 | -0.288 | -0.271 | 9 | -0.505 | -0.488 | 6 | -0.111 | -0.095 | 6 | -0.717 | -0.700 | 3 | -0.489 | -0.471 | 3 | -0.507 | -0.488 |
| XMRUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 4 | -0.256 | -0.623 | 4 | +2.800 | +1.704 | 3 | +0.064 | -0.146 | 3 | -2.473 | -3.415 | 1 | -0.580 | -1.109 | 1 | +8.069 | +6.756 |
| XMRUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 5 | -0.289 | +0.111 | 5 | -0.507 | +0.624 | 3 | -0.287 | -0.044 | 3 | -0.468 | +0.508 | 2 | -0.161 | +0.406 | 2 | -4.372 | -3.022 |
| XMRUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 9 | -0.288 | -0.271 | 9 | -0.505 | -0.488 | 6 | -0.111 | -0.095 | 6 | -0.717 | -0.700 | 3 | -0.489 | -0.471 | 3 | -0.507 | -0.488 |
| XMRUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 4 | -0.256 | -0.623 | 4 | +2.800 | +1.704 | 3 | +0.064 | -0.146 | 3 | -2.473 | -3.415 | 1 | -0.580 | -1.109 | 1 | +8.069 | +6.756 |
| XMRUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 5 | -0.289 | +0.111 | 5 | -0.507 | +0.624 | 3 | -0.287 | -0.044 | 3 | -0.468 | +0.508 | 2 | -0.161 | +0.406 | 2 | -4.372 | -3.022 |
| XMRUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 13 | +0.603 | +0.620 | 13 | -0.853 | -0.836 | 8 | +0.544 | +0.560 | 8 | -0.176 | -0.159 | 5 | +0.599 | +0.618 | 5 | -0.857 | -0.838 |
| XMRUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 9 | +0.452 | +0.086 | 9 | +0.009 | -1.086 | 6 | +0.159 | -0.051 | 6 | +6.053 | +5.110 | 3 | +0.604 | +0.075 | 3 | -0.852 | -2.165 |
| XMRUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 4 | +1.644 | +2.045 | 4 | -3.520 | -2.390 | 2 | +1.750 | +1.993 | 2 | -3.515 | -2.539 | 2 | +0.375 | +0.942 | 2 | -5.981 | -4.631 |
| XMRUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 11 | +0.603 | +0.620 | 11 | -0.328 | -0.311 | 7 | +0.452 | +0.469 | 7 | +1.212 | +1.228 | 4 | +0.773 | +0.792 | 4 | -0.592 | -0.573 |
| XMRUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 9 | +0.452 | +0.086 | 9 | +0.009 | -1.086 | 6 | +0.159 | -0.051 | 6 | +6.053 | +5.110 | 3 | +0.604 | +0.075 | 3 | -0.852 | -2.165 |
| XMRUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 2 | +1.644 | +2.045 | 2 | -0.950 | +0.180 | 1 | +0.635 | +0.878 | 1 | -1.564 | -0.588 | 1 | +2.652 | +3.219 | 1 | -0.337 | +1.014 |
| XMRUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 25 | -2.330 | -2.312 | 24 | +1.906 | +1.923 | 16 | -1.322 | -1.305 | 16 | +1.907 | +1.923 | 9 | -2.445 | -2.426 | 8 | +2.923 | +2.941 |
| XMRUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 11 | -1.086 | -1.452 | 11 | +2.618 | +1.523 | 8 | +0.100 | -0.110 | 8 | +1.909 | +0.967 | 3 | -1.685 | -2.214 | 3 | +6.033 | +4.720 |
| XMRUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 14 | -2.531 | -2.130 | 13 | +0.599 | +1.729 | 8 | -2.530 | -2.287 | 8 | -3.176 | -2.200 | 6 | -4.356 | -3.790 | 5 | +0.598 | +1.948 |
| BNBUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 378 | -0.032 | +0.082 | 378 | +0.069 | +0.183 | 236 | +0.102 | +0.202 | 236 | +0.213 | +0.312 | 142 | -0.233 | -0.086 | 142 | -0.330 | -0.183 |
| BNBUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 209 | +0.140 | +0.131 | 209 | +0.781 | +0.455 | 128 | +0.452 | +0.432 | 128 | +0.759 | +0.452 | 81 | -0.288 | -0.269 | 81 | +0.751 | +0.379 |
| BNBUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 169 | -0.270 | -0.034 | 169 | -0.225 | +0.329 | 108 | -0.349 | -0.131 | 108 | +0.037 | +0.543 | 61 | -0.150 | +0.123 | 61 | -1.101 | -0.436 |
| BNBUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 328 | +0.002 | +0.115 | 328 | +0.106 | +0.219 | 204 | +0.153 | +0.253 | 204 | +0.262 | +0.361 | 124 | -0.232 | -0.085 | 124 | -0.278 | -0.132 |
| BNBUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 182 | +0.231 | +0.222 | 182 | +0.880 | +0.554 | 111 | +0.488 | +0.469 | 111 | +0.993 | +0.686 | 71 | -0.286 | -0.266 | 71 | +0.758 | +0.387 |
| BNBUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 146 | -0.166 | +0.069 | 146 | -0.203 | +0.350 | 93 | -0.211 | +0.007 | 93 | +0.064 | +0.571 | 53 | -0.069 | +0.204 | 53 | -1.022 | -0.358 |
| BNBUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 340 | -0.116 | -0.003 | 340 | -0.163 | -0.049 | 213 | -0.027 | +0.073 | 213 | -0.161 | -0.062 | 127 | -0.208 | -0.062 | 127 | -0.176 | -0.030 |
| BNBUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 185 | +0.120 | +0.112 | 185 | +0.332 | +0.005 | 113 | +0.196 | +0.176 | 113 | +0.177 | -0.131 | 72 | -0.162 | -0.142 | 72 | +0.595 | +0.224 |
| BNBUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 155 | -0.271 | -0.036 | 155 | -0.443 | +0.110 | 100 | -0.307 | -0.089 | 100 | -0.316 | +0.190 | 55 | -0.249 | +0.024 | 55 | -0.827 | -0.163 |
| BNBUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 303 | -0.072 | +0.041 | 303 | -0.196 | -0.082 | 187 | +0.019 | +0.119 | 187 | -0.225 | -0.126 | 116 | -0.191 | -0.045 | 116 | -0.149 | -0.002 |
| BNBUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 159 | +0.120 | +0.112 | 159 | +0.332 | +0.006 | 94 | +0.190 | +0.171 | 94 | +0.016 | -0.291 | 65 | -0.118 | -0.098 | 65 | +1.258 | +0.886 |
| BNBUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 144 | -0.240 | -0.005 | 144 | -0.460 | +0.093 | 93 | -0.248 | -0.030 | 93 | -0.417 | +0.090 | 51 | -0.198 | +0.074 | 51 | -1.472 | -0.808 |
| BNBUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 286 | +0.063 | +0.176 | 285 | -0.118 | -0.005 | 176 | +0.178 | +0.277 | 176 | -0.026 | +0.073 | 110 | -0.234 | -0.088 | 109 | -0.377 | -0.230 |
| BNBUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 156 | +0.095 | +0.086 | 155 | +0.288 | -0.038 | 91 | -0.029 | -0.049 | 91 | +0.149 | -0.158 | 65 | +0.096 | +0.116 | 64 | +0.745 | +0.374 |
| BNBUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 130 | +0.062 | +0.298 | 130 | -0.674 | -0.121 | 85 | +0.248 | +0.466 | 85 | -0.145 | +0.361 | 45 | -0.356 | -0.083 | 45 | -2.332 | -1.668 |
| BNBUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 247 | +0.145 | +0.258 | 246 | -0.173 | -0.059 | 151 | +0.247 | +0.346 | 151 | -0.208 | -0.109 | 96 | -0.084 | +0.062 | 95 | +0.017 | +0.163 |
| BNBUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 131 | +0.146 | +0.137 | 130 | +0.340 | +0.013 | 75 | +0.161 | +0.142 | 75 | -0.316 | -0.623 | 56 | +0.124 | +0.144 | 55 | +1.249 | +0.878 |
| BNBUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 116 | +0.135 | +0.370 | 116 | -0.818 | -0.265 | 76 | +0.255 | +0.473 | 76 | -0.192 | +0.314 | 40 | -0.255 | +0.018 | 40 | -2.416 | -1.752 |
| BNBUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 300 | -0.350 | -0.237 | 299 | -0.212 | -0.099 | 188 | -0.080 | +0.019 | 188 | -0.068 | +0.031 | 112 | -0.797 | -0.651 | 111 | -0.428 | -0.282 |
| BNBUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 175 | +0.050 | +0.042 | 174 | +0.286 | -0.040 | 107 | +0.110 | +0.091 | 107 | +0.386 | +0.078 | 68 | -0.365 | -0.345 | 67 | +0.176 | -0.195 |
| BNBUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 125 | -0.720 | -0.484 | 125 | -0.889 | -0.335 | 81 | -0.529 | -0.310 | 81 | -0.794 | -0.288 | 44 | -1.150 | -0.878 | 44 | -1.346 | -0.682 |
| BNBUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 268 | -0.244 | -0.130 | 267 | -0.207 | -0.094 | 167 | -0.066 | +0.033 | 167 | +0.131 | +0.231 | 101 | -0.739 | -0.592 | 100 | -0.778 | -0.632 |
| BNBUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 155 | -0.057 | -0.065 | 154 | +0.329 | +0.002 | 97 | +0.007 | -0.012 | 97 | +0.295 | -0.012 | 58 | -0.389 | -0.370 | 57 | +0.423 | +0.051 |
| BNBUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 113 | -0.672 | -0.436 | 113 | -0.925 | -0.372 | 70 | -0.433 | -0.215 | 70 | -0.122 | +0.384 | 43 | -1.110 | -0.838 | 43 | -1.512 | -0.848 |
| BNBUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 619 | +0.099 | +0.213 | 617 | +0.138 | +0.252 | 387 | +0.268 | +0.368 | 387 | +0.348 | +0.447 | 232 | -0.205 | -0.058 | 230 | +0.009 | +0.155 |
| BNBUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 321 | +0.160 | +0.152 | 321 | +0.177 | -0.149 | 194 | +0.462 | +0.443 | 194 | +0.418 | +0.111 | 127 | -0.154 | -0.134 | 127 | +0.013 | -0.359 |
| BNBUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 298 | -0.019 | +0.216 | 296 | +0.132 | +0.685 | 193 | +0.186 | +0.405 | 193 | +0.332 | +0.838 | 105 | -0.287 | -0.014 | 103 | -0.011 | +0.654 |
| BNBUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 78 | +0.218 | +0.273 | 77 | -0.197 | -0.143 | 54 | +0.185 | +0.232 | 54 | -0.268 | -0.220 | 24 | +0.274 | +0.344 | 23 | -0.012 | +0.058 |
| BNBUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 45 | +0.453 | +0.301 | 44 | +0.187 | -0.586 | 32 | +0.453 | +0.312 | 32 | +0.057 | -0.620 | 13 | +0.732 | +0.556 | 12 | +1.153 | +0.213 |
| BNBUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 33 | -0.140 | +0.121 | 33 | -0.858 | +0.023 | 22 | -0.372 | -0.136 | 22 | -1.019 | -0.247 | 11 | -0.077 | +0.240 | 11 | -0.278 | +0.801 |
| BNBUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 65 | -0.020 | +0.035 | 64 | -0.311 | -0.257 | 43 | -0.055 | -0.008 | 43 | -0.736 | -0.688 | 22 | +0.274 | +0.344 | 21 | -0.012 | +0.058 |
| BNBUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 36 | +0.412 | +0.260 | 35 | -0.190 | -0.963 | 25 | +0.383 | +0.242 | 25 | -0.344 | -1.021 | 11 | +0.732 | +0.556 | 10 | +1.151 | +0.211 |
| BNBUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 29 | -0.144 | +0.116 | 29 | -0.862 | +0.019 | 18 | -0.375 | -0.139 | 18 | -1.022 | -0.250 | 11 | -0.077 | +0.240 | 11 | -0.278 | +0.801 |
| BNBUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 71 | +0.394 | +0.448 | 70 | +0.237 | +0.291 | 51 | +0.398 | +0.446 | 51 | +0.621 | +0.668 | 20 | +0.246 | +0.316 | 19 | -0.407 | -0.338 |
| BNBUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 42 | +0.190 | +0.037 | 41 | +0.559 | -0.214 | 31 | +0.311 | +0.170 | 31 | +0.560 | -0.117 | 11 | -0.004 | -0.180 | 10 | +0.414 | -0.525 |
| BNBUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 29 | +0.537 | +0.798 | 29 | -0.043 | +0.838 | 20 | +0.974 | +1.210 | 20 | +0.722 | +1.493 | 9 | +0.496 | +0.813 | 9 | -0.595 | +0.485 |
| BNBUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 61 | +0.507 | +0.562 | 60 | +0.471 | +0.525 | 44 | +0.603 | +0.650 | 44 | +0.606 | +0.654 | 17 | +0.501 | +0.571 | 16 | -0.168 | -0.098 |
| BNBUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 35 | +0.404 | +0.251 | 34 | +0.950 | +0.177 | 26 | +0.175 | +0.034 | 26 | +0.840 | +0.163 | 9 | +0.922 | +0.746 | 8 | +1.834 | +0.894 |
| BNBUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 26 | +0.520 | +0.781 | 26 | -0.494 | +0.387 | 18 | +0.974 | +1.210 | 18 | +0.305 | +1.077 | 8 | +0.148 | +0.464 | 8 | -0.755 | +0.324 |
| BNBUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 62 | +0.912 | +0.967 | 62 | +1.225 | +1.279 | 45 | +0.882 | +0.929 | 45 | +1.848 | +1.895 | 17 | +1.049 | +1.119 | 17 | +0.145 | +0.215 |
| BNBUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 33 | +0.957 | +0.804 | 33 | +0.393 | -0.380 | 25 | +0.884 | +0.743 | 25 | +1.850 | +1.174 | 8 | +1.213 | +1.037 | 8 | -0.210 | -1.150 |
| BNBUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 29 | +0.761 | +1.022 | 29 | +1.705 | +2.586 | 20 | +0.891 | +1.127 | 20 | +1.721 | +2.493 | 9 | -0.520 | -0.204 | 9 | +1.696 | +2.776 |
| BNBUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 51 | +1.024 | +1.079 | 51 | +1.127 | +1.181 | 35 | +1.024 | +1.072 | 35 | +1.845 | +1.893 | 16 | +1.084 | +1.154 | 16 | +0.101 | +0.171 |
| BNBUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 26 | +1.086 | +0.933 | 26 | +0.320 | -0.453 | 18 | +1.001 | +0.860 | 18 | +2.852 | +2.175 | 8 | +1.213 | +1.037 | 8 | -0.210 | -1.150 |
| BNBUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 25 | +1.012 | +1.273 | 25 | +1.313 | +2.194 | 17 | +1.017 | +1.253 | 17 | +1.126 | +1.898 | 8 | +0.084 | +0.400 | 8 | +1.498 | +2.578 |
| BNBUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 58 | -0.328 | -0.274 | 58 | -0.056 | -0.002 | 43 | -0.338 | -0.290 | 43 | +0.360 | +0.407 | 15 | -0.292 | -0.222 | 15 | -0.713 | -0.643 |
| BNBUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 35 | -0.077 | -0.230 | 35 | +0.362 | -0.411 | 27 | -0.312 | -0.453 | 27 | +1.005 | +0.329 | 8 | +0.720 | +0.544 | 8 | -1.637 | -2.577 |
| BNBUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 23 | -0.370 | -0.109 | 23 | -0.677 | +0.204 | 16 | -0.585 | -0.349 | 16 | -0.654 | +0.118 | 7 | -0.361 | -0.045 | 7 | -0.712 | +0.367 |
| BNBUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 50 | -0.036 | +0.019 | 50 | -0.056 | -0.002 | 36 | -0.093 | -0.046 | 36 | +0.065 | +0.112 | 14 | +0.850 | +0.920 | 14 | -0.228 | -0.158 |
| BNBUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 28 | +0.506 | +0.354 | 28 | +0.083 | -0.690 | 20 | -0.195 | -0.335 | 20 | +0.727 | +0.051 | 8 | +0.869 | +0.692 | 8 | -0.222 | -1.162 |
| BNBUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 22 | -0.238 | +0.023 | 22 | -0.656 | +0.225 | 16 | -0.049 | +0.187 | 16 | -0.649 | +0.123 | 6 | -0.376 | -0.059 | 6 | +0.594 | +1.674 |
| BNBUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 124 | -0.238 | -0.184 | 124 | -0.036 | +0.018 | 82 | -0.607 | -0.560 | 82 | -0.565 | -0.518 | 42 | +0.645 | +0.715 | 42 | +1.466 | +1.536 |
| BNBUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 52 | +1.178 | +1.026 | 52 | +0.478 | -0.295 | 32 | -0.196 | -0.337 | 32 | +0.304 | -0.373 | 20 | +1.481 | +1.304 | 20 | +1.835 | +0.895 |
| BNBUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 72 | -0.555 | -0.294 | 72 | -0.654 | +0.227 | 50 | -0.707 | -0.471 | 50 | -1.025 | -0.253 | 22 | -0.371 | -0.055 | 22 | +1.281 | +2.360 |
| BNBUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 15 | -0.041 | -0.020 | 14 | +0.212 | +0.233 | 8 | -0.182 | -0.164 | 8 | +1.648 | +1.667 | 7 | -0.044 | -0.018 | 6 | -0.213 | -0.188 |
| BNBUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 8 | -0.367 | -0.660 | 8 | +1.649 | +0.455 | 5 | -0.392 | -0.654 | 5 | +2.916 | +1.227 | 3 | -0.180 | -0.578 | 3 | -2.436 | -2.986 |
| BNBUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 7 | +1.394 | +1.728 | 6 | -0.061 | +1.174 | 3 | +1.398 | +1.697 | 3 | -0.162 | +1.564 | 4 | +1.337 | +1.787 | 3 | +0.041 | +0.641 |
| BNBUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 14 | -0.112 | -0.091 | 13 | +0.380 | +0.400 | 8 | -0.182 | -0.164 | 8 | +1.648 | +1.667 | 6 | -0.120 | -0.094 | 5 | -0.471 | -0.446 |
| BNBUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | -0.367 | -0.660 | 8 | +1.649 | +0.455 | 5 | -0.392 | -0.654 | 5 | +2.916 | +1.227 | 3 | -0.180 | -0.578 | 3 | -2.436 | -2.986 |
| BNBUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 6 | +0.886 | +1.220 | 5 | -0.166 | +1.069 | 3 | +1.398 | +1.697 | 3 | -0.162 | +1.564 | 3 | +0.363 | +0.813 | 2 | +1.092 | +1.692 |
| BNBUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 14 | -0.264 | -0.243 | 13 | +0.046 | +0.066 | 7 | -0.340 | -0.321 | 7 | +2.510 | +2.528 | 7 | -0.191 | -0.165 | 6 | -1.291 | -1.266 |
| BNBUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 7 | -0.340 | -0.632 | 7 | +3.336 | +2.141 | 4 | +0.667 | +0.405 | 4 | +3.462 | +1.773 | 3 | -1.021 | -1.419 | 3 | -0.580 | -1.130 |
| BNBUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 7 | +0.591 | +0.925 | 6 | -0.977 | +0.258 | 3 | -1.007 | -0.708 | 3 | +1.050 | +2.776 | 4 | +1.443 | +1.893 | 3 | -2.002 | -1.402 |
| BNBUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 13 | -0.345 | -0.324 | 12 | +0.240 | +0.260 | 7 | -0.340 | -0.321 | 7 | +2.510 | +2.528 | 6 | -0.609 | -0.583 | 5 | -2.007 | -1.982 |
| BNBUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 7 | -0.340 | -0.632 | 7 | +3.336 | +2.141 | 4 | +0.667 | +0.405 | 4 | +3.462 | +1.773 | 3 | -1.021 | -1.419 | 3 | -0.580 | -1.130 |
| BNBUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 6 | -0.210 | +0.124 | 5 | -1.998 | -0.763 | 3 | -1.007 | -0.708 | 3 | +1.050 | +2.776 | 3 | +0.575 | +1.025 | 2 | -2.297 | -1.697 |
| BNBUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 9 | +0.819 | +0.840 | 9 | +3.080 | +3.100 | 5 | +1.674 | +1.692 | 5 | +3.144 | +3.162 | 4 | +0.318 | +0.344 | 4 | -2.052 | -2.027 |
| BNBUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 4 | +0.324 | +0.031 | 4 | +3.461 | +2.267 | 2 | +0.643 | +0.380 | 2 | +3.464 | +1.775 | 2 | +0.313 | -0.085 | 2 | +5.891 | +5.341 |
| BNBUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 5 | +1.887 | +2.221 | 5 | -1.318 | -0.082 | 3 | +2.725 | +3.024 | 3 | +3.080 | +4.805 | 2 | -0.116 | +0.334 | 2 | -2.052 | -1.452 |
| BNBUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 8 | +1.243 | +1.263 | 8 | +3.108 | +3.128 | 4 | +2.199 | +2.218 | 4 | +3.238 | +3.256 | 4 | +0.318 | +0.344 | 4 | -2.052 | -2.027 |
| BNBUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 4 | +0.324 | +0.031 | 4 | +3.461 | +2.267 | 2 | +0.643 | +0.380 | 2 | +3.464 | +1.775 | 2 | +0.313 | -0.085 | 2 | +5.891 | +5.341 |
| BNBUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 4 | +2.305 | +2.639 | 4 | +0.880 | +2.115 | 2 | +2.983 | +3.283 | 2 | +3.107 | +4.833 | 2 | -0.116 | +0.334 | 2 | -2.052 | -1.452 |
| BNBUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 14 | +0.004 | +0.025 | 14 | -0.515 | -0.495 | 9 | +0.140 | +0.158 | 9 | +2.889 | +2.908 | 5 | -0.134 | -0.108 | 5 | -0.745 | -0.720 |
| BNBUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 10 | +0.494 | +0.201 | 10 | +3.308 | +2.114 | 7 | +0.849 | +0.586 | 7 | +3.728 | +2.039 | 3 | -0.134 | -0.532 | 3 | -0.299 | -0.849 |
| BNBUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 4 | -1.926 | -1.592 | 4 | -3.135 | -1.900 | 2 | -3.208 | -2.908 | 2 | -3.132 | -1.406 | 2 | +0.286 | +0.736 | 2 | -4.186 | -3.586 |
| BNBUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 15 | +0.139 | +0.160 | 15 | -0.736 | -0.716 | 11 | +0.140 | +0.158 | 11 | -0.810 | -0.792 | 4 | +1.508 | +1.534 | 4 | -0.520 | -0.495 |
| BNBUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 10 | +0.494 | +0.201 | 10 | +3.308 | +2.114 | 7 | +0.849 | +0.586 | 7 | +3.728 | +2.039 | 3 | -0.134 | -0.532 | 3 | -0.299 | -0.849 |
| BNBUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 5 | -0.100 | +0.234 | 5 | -0.959 | +0.276 | 4 | -0.686 | -0.387 | 4 | -2.170 | -0.444 | 1 | +3.150 | +3.600 | 1 | -0.741 | -0.141 |
| BNBUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 18 | -0.345 | -0.324 | 18 | -2.094 | -2.074 | 9 | +0.942 | +0.960 | 9 | +0.216 | +0.235 | 9 | -0.480 | -0.454 | 9 | -2.293 | -2.268 |
| BNBUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 7 | -0.332 | -0.624 | 7 | -1.899 | -3.093 | 2 | +0.886 | +0.624 | 2 | +7.541 | +5.852 | 5 | -0.335 | -0.733 | 5 | -1.902 | -2.452 |
| BNBUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 11 | -0.357 | -0.023 | 11 | -2.290 | -1.054 | 7 | +0.942 | +1.241 | 7 | +0.216 | +1.942 | 4 | -1.465 | -1.015 | 4 | -4.046 | -3.446 |
| UNIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 319 | -0.098 | -0.029 | 318 | -0.514 | -0.446 | 199 | +0.237 | +0.301 | 199 | +0.190 | +0.255 | 120 | -0.252 | -0.179 | 119 | -1.205 | -1.131 |
| UNIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 171 | -0.188 | -0.069 | 170 | -0.965 | -0.741 | 110 | +0.178 | +0.278 | 110 | -0.569 | -0.422 | 61 | -0.889 | -0.739 | 60 | -1.780 | -1.449 |
| UNIUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 148 | +0.163 | +0.181 | 148 | +0.442 | +0.354 | 89 | +0.249 | +0.279 | 89 | +0.612 | +0.594 | 59 | +0.139 | +0.136 | 59 | -0.517 | -0.701 |
| UNIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 265 | -0.006 | +0.062 | 264 | +0.260 | +0.328 | 168 | +0.294 | +0.359 | 168 | +0.610 | +0.675 | 97 | -0.207 | -0.134 | 96 | -0.785 | -0.711 |
| UNIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 145 | -0.186 | -0.067 | 144 | -0.894 | -0.669 | 92 | +0.097 | +0.197 | 92 | +0.181 | +0.329 | 53 | -0.889 | -0.739 | 52 | -1.910 | -1.578 |
| UNIUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 120 | +0.310 | +0.327 | 120 | +0.706 | +0.619 | 76 | +0.695 | +0.725 | 76 | +0.660 | +0.642 | 44 | +0.207 | +0.204 | 44 | +1.157 | +0.973 |
| UNIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 295 | -0.168 | -0.100 | 295 | -0.522 | -0.454 | 189 | -0.193 | -0.128 | 189 | -0.389 | -0.324 | 106 | -0.003 | +0.071 | 106 | -0.801 | -0.727 |
| UNIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 166 | -0.166 | -0.047 | 166 | -0.868 | -0.644 | 109 | -0.180 | -0.080 | 109 | -0.850 | -0.702 | 57 | -0.002 | +0.148 | 57 | -0.892 | -0.561 |
| UNIUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 129 | -0.169 | -0.151 | 129 | +0.036 | -0.052 | 80 | -0.199 | -0.169 | 80 | -0.104 | -0.122 | 49 | -0.003 | -0.006 | 49 | +0.239 | +0.055 |
| UNIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 254 | -0.001 | +0.067 | 254 | -0.408 | -0.340 | 162 | -0.065 | +0.000 | 162 | -0.104 | -0.039 | 92 | -0.003 | +0.071 | 92 | -0.731 | -0.657 |
| UNIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 143 | -0.002 | +0.117 | 143 | -0.825 | -0.601 | 93 | -0.108 | -0.008 | 93 | -0.034 | +0.114 | 50 | -0.005 | +0.145 | 50 | -1.071 | -0.739 |
| UNIUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 111 | -0.001 | +0.017 | 111 | +0.064 | -0.024 | 69 | -0.023 | +0.006 | 69 | -0.390 | -0.408 | 42 | -0.003 | -0.006 | 42 | +0.379 | +0.195 |
| UNIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 244 | -0.236 | -0.168 | 244 | -0.823 | -0.755 | 153 | -0.442 | -0.378 | 153 | -0.814 | -0.749 | 91 | -0.004 | +0.070 | 91 | -0.837 | -0.764 |
| UNIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 135 | -0.417 | -0.299 | 135 | -0.856 | -0.631 | 88 | -0.522 | -0.422 | 88 | -0.585 | -0.437 | 47 | -0.108 | +0.042 | 47 | -1.234 | -0.902 |
| UNIUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 109 | -0.073 | -0.056 | 109 | -0.742 | -0.829 | 65 | -0.256 | -0.226 | 65 | -1.094 | -1.113 | 44 | +0.080 | +0.077 | 44 | +0.213 | +0.029 |
| UNIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 205 | -0.113 | -0.045 | 205 | -0.742 | -0.674 | 126 | -0.334 | -0.269 | 126 | -0.606 | -0.542 | 79 | -0.002 | +0.072 | 79 | -0.868 | -0.794 |
| UNIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 115 | -0.313 | -0.194 | 115 | -0.828 | -0.603 | 72 | -0.374 | -0.274 | 72 | -0.438 | -0.291 | 43 | -0.127 | +0.023 | 43 | -1.525 | -1.193 |
| UNIUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 90 | +0.027 | +0.045 | 90 | -0.608 | -0.695 | 54 | -0.312 | -0.282 | 54 | -0.983 | -1.001 | 36 | +0.144 | +0.141 | 36 | +0.312 | +0.128 |
| UNIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 245 | +0.266 | +0.334 | 244 | -0.642 | -0.574 | 157 | +0.281 | +0.346 | 157 | -0.826 | -0.761 | 88 | +0.025 | +0.098 | 87 | -0.578 | -0.504 |
| UNIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 135 | +0.260 | +0.379 | 134 | -0.994 | -0.769 | 91 | +0.281 | +0.381 | 91 | -1.094 | -0.947 | 44 | -0.149 | +0.001 | 43 | -0.579 | -0.247 |
| UNIUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 110 | +0.354 | +0.372 | 110 | +0.284 | +0.197 | 66 | +0.358 | +0.388 | 66 | +0.743 | +0.725 | 44 | +0.344 | +0.341 | 44 | -0.518 | -0.702 |
| UNIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 215 | +0.264 | +0.332 | 215 | -0.433 | -0.365 | 139 | +0.282 | +0.347 | 139 | -0.480 | -0.416 | 76 | +0.025 | +0.099 | 76 | -0.437 | -0.363 |
| UNIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 115 | +0.158 | +0.276 | 115 | -0.832 | -0.608 | 79 | +0.275 | +0.375 | 79 | -1.204 | -1.056 | 36 | -0.364 | -0.214 | 36 | -0.515 | -0.183 |
| UNIUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 100 | +0.411 | +0.429 | 100 | +0.224 | +0.137 | 60 | +0.452 | +0.481 | 60 | +0.743 | +0.725 | 40 | +0.344 | +0.341 | 40 | -0.202 | -0.387 |
| UNIUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 477 | +0.109 | +0.177 | 477 | -0.497 | -0.429 | 300 | +0.227 | +0.292 | 300 | -0.608 | -0.543 | 177 | -0.064 | +0.009 | 177 | -0.203 | -0.129 |
| UNIUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 232 | +0.156 | +0.275 | 232 | -0.264 | -0.039 | 136 | +0.349 | +0.448 | 136 | -0.299 | -0.151 | 96 | -0.194 | -0.044 | 96 | -0.059 | +0.273 |
| UNIUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 245 | +0.024 | +0.042 | 245 | -0.872 | -0.960 | 164 | +0.023 | +0.053 | 164 | -0.871 | -0.889 | 81 | +0.019 | +0.016 | 81 | -0.705 | -0.889 |
| UNIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 83 | -0.151 | -0.118 | 82 | +0.853 | +0.886 | 51 | +0.115 | +0.146 | 51 | +0.862 | +0.893 | 32 | -0.202 | -0.166 | 31 | -0.547 | -0.511 |
| UNIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 43 | -0.081 | -0.007 | 42 | +0.833 | +1.183 | 27 | +0.292 | +0.316 | 27 | +2.303 | +2.661 | 16 | -0.347 | -0.201 | 15 | -0.612 | -0.282 |
| UNIUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 40 | -0.278 | -0.286 | 40 | +0.902 | +0.617 | 24 | -0.693 | -0.654 | 24 | +0.678 | +0.382 | 16 | -0.063 | -0.139 | 16 | +2.541 | +2.282 |
| UNIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 72 | -0.155 | -0.122 | 71 | +0.858 | +0.891 | 46 | +0.015 | +0.046 | 46 | +0.855 | +0.886 | 26 | -0.199 | -0.164 | 25 | +1.264 | +1.299 |
| UNIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 38 | -0.113 | -0.040 | 37 | +0.812 | +1.163 | 24 | +0.251 | +0.274 | 24 | +1.578 | +1.936 | 14 | -0.345 | -0.199 | 13 | -0.611 | -0.280 |
| UNIUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 34 | -0.278 | -0.287 | 34 | +0.980 | +0.695 | 22 | -0.693 | -0.655 | 22 | +0.649 | +0.353 | 12 | -0.064 | -0.139 | 12 | +2.894 | +2.634 |
| UNIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 72 | +0.181 | +0.214 | 72 | +1.245 | +1.278 | 43 | +0.289 | +0.320 | 43 | +1.225 | +1.256 | 29 | -0.117 | -0.081 | 29 | +1.265 | +1.301 |
| UNIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 38 | -0.035 | +0.039 | 38 | +1.400 | +1.751 | 24 | +0.886 | +0.910 | 24 | +2.090 | +2.448 | 14 | -0.651 | -0.505 | 14 | +1.164 | +1.494 |
| UNIUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 34 | +0.408 | +0.400 | 34 | +0.875 | +0.590 | 19 | +0.088 | +0.127 | 19 | +0.439 | +0.143 | 15 | +1.176 | +1.101 | 15 | +1.562 | +1.302 |
| UNIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 62 | +0.692 | +0.725 | 62 | +1.512 | +1.545 | 36 | +0.847 | +0.878 | 36 | +1.361 | +1.392 | 26 | +0.295 | +0.330 | 26 | +1.546 | +1.582 |
| UNIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 33 | +0.290 | +0.364 | 33 | +1.722 | +2.073 | 20 | +1.014 | +1.037 | 20 | +2.837 | +3.195 | 13 | -0.232 | -0.086 | 13 | +1.269 | +1.599 |
| UNIUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 29 | +0.822 | +0.814 | 29 | +1.215 | +0.930 | 16 | +0.177 | +0.216 | 16 | -0.823 | -1.119 | 13 | +1.462 | +1.387 | 13 | +3.543 | +3.283 |
| UNIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 58 | -0.256 | -0.223 | 58 | -0.452 | -0.419 | 36 | +0.314 | +0.345 | 36 | +0.629 | +0.660 | 22 | -0.787 | -0.752 | 22 | -1.620 | -1.584 |
| UNIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 37 | +0.153 | +0.227 | 37 | +0.698 | +1.049 | 22 | +1.556 | +1.579 | 22 | +1.561 | +1.919 | 15 | -0.970 | -0.824 | 15 | +0.624 | +0.954 |
| UNIUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 21 | -0.593 | -0.602 | 21 | -1.659 | -1.944 | 14 | -0.541 | -0.502 | 14 | -0.102 | -0.398 | 7 | -0.593 | -0.668 | 7 | -2.715 | -2.974 |
| UNIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 50 | -0.256 | -0.223 | 50 | -0.504 | -0.471 | 31 | +0.585 | +0.616 | 31 | +0.446 | +0.477 | 19 | -0.970 | -0.935 | 19 | -1.580 | -1.544 |
| UNIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 32 | +0.369 | +0.443 | 32 | +0.661 | +1.012 | 19 | +1.352 | +1.376 | 19 | +0.817 | +1.175 | 13 | -0.970 | -0.824 | 13 | +0.624 | +0.954 |
| UNIUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 18 | -0.672 | -0.680 | 18 | -1.793 | -2.078 | 12 | -0.543 | -0.504 | 12 | -0.743 | -1.039 | 6 | -0.789 | -0.865 | 6 | -2.186 | -2.446 |
| UNIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 56 | -0.287 | -0.254 | 56 | +0.588 | +0.620 | 35 | -0.229 | -0.198 | 35 | +0.632 | +0.663 | 21 | -0.462 | -0.427 | 21 | +0.583 | +0.619 |
| UNIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 34 | +0.028 | +0.102 | 34 | +0.757 | +1.108 | 22 | +0.069 | +0.092 | 22 | +1.307 | +1.665 | 12 | -0.102 | +0.044 | 12 | +0.587 | +0.917 |
| UNIUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 22 | -0.552 | -0.560 | 22 | -0.082 | -0.367 | 13 | -0.393 | -0.354 | 13 | +0.027 | -0.269 | 9 | -0.711 | -0.786 | 9 | -0.191 | -0.450 |
| UNIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 54 | -0.336 | -0.303 | 54 | +0.611 | +0.644 | 34 | -0.331 | -0.299 | 34 | +0.121 | +0.152 | 20 | -0.378 | -0.343 | 20 | +2.023 | +2.058 |
| UNIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 29 | -0.229 | -0.156 | 29 | +0.883 | +1.234 | 20 | +0.056 | +0.079 | 20 | +0.759 | +1.117 | 9 | -0.461 | -0.315 | 9 | +1.020 | +1.350 |
| UNIUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 25 | -0.393 | -0.401 | 25 | +0.027 | -0.258 | 14 | -0.613 | -0.574 | 14 | -1.251 | -1.547 | 11 | -0.295 | -0.370 | 11 | +3.145 | +2.885 |
| UNIUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 119 | +0.017 | +0.050 | 119 | +1.806 | +1.839 | 66 | +0.203 | +0.234 | 66 | +1.644 | +1.675 | 53 | -0.021 | +0.014 | 53 | +2.594 | +2.630 |
| UNIUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 56 | -0.067 | +0.007 | 56 | -0.989 | -0.639 | 20 | +0.503 | +0.526 | 20 | -1.774 | -1.416 | 36 | -0.251 | -0.105 | 36 | -0.339 | -0.009 |
| UNIUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 63 | +0.224 | +0.216 | 63 | +2.167 | +1.882 | 46 | -0.064 | -0.025 | 46 | +1.887 | +1.591 | 17 | +1.339 | +1.263 | 17 | +3.878 | +3.618 |
| UNIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 10 | -0.504 | -0.492 | 9 | -0.835 | -0.822 | 8 | -0.135 | -0.123 | 8 | -0.915 | -0.903 | 2 | -2.681 | -2.668 | 1 | -0.030 | -0.017 |
| UNIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 6 | -0.135 | +0.004 | 6 | -1.487 | -0.599 | 5 | +0.089 | +0.253 | 5 | -2.140 | -1.310 | 1 | -4.061 | -4.001 | 1 | -0.030 | +1.149 |
| UNIUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 4 | -2.418 | -2.532 | 3 | +1.418 | +0.554 | 3 | -3.535 | -3.676 | 3 | +1.418 | +0.611 | 1 | -1.301 | -1.334 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 7 | -1.301 | -1.288 | 6 | +0.698 | +0.710 | 5 | -0.647 | -0.636 | 5 | +1.422 | +1.433 | 2 | -2.681 | -2.668 | 1 | -0.030 | -0.017 |
| UNIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 3 | -0.647 | -0.509 | 3 | -0.022 | +0.867 | 2 | +0.335 | +0.498 | 2 | -0.828 | +0.003 | 1 | -4.061 | -4.001 | 1 | -0.030 | +1.149 |
| UNIUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 4 | -2.418 | -2.532 | 3 | +1.418 | +0.554 | 3 | -3.535 | -3.676 | 3 | +1.418 | +0.611 | 1 | -1.301 | -1.334 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 8 | -1.238 | -1.226 | 6 | +0.295 | +0.307 | 6 | -1.238 | -1.226 | 6 | +0.295 | +0.306 | 2 | +1.777 | +1.790 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 5 | +0.410 | +0.549 | 4 | -1.485 | -0.596 | 4 | -0.311 | -0.147 | 4 | -1.485 | -0.654 | 1 | +5.777 | +5.837 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 3 | -2.268 | -2.382 | 2 | +1.127 | +0.263 | 2 | -2.901 | -3.042 | 2 | +1.127 | +0.320 | 1 | -2.222 | -2.256 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 5 | -2.221 | -2.209 | 4 | +1.129 | +1.141 | 4 | -1.853 | -1.841 | 4 | +1.129 | +1.141 | 1 | -2.222 | -2.209 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 2 | -0.504 | -0.365 | 2 | -0.456 | +0.432 | 2 | -0.504 | -0.340 | 2 | -0.456 | +0.374 | 0 | — | — | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 3 | -2.268 | -2.382 | 2 | +1.127 | +0.263 | 2 | -2.901 | -3.042 | 2 | +1.127 | +0.320 | 1 | -2.222 | -2.256 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 8 | +0.910 | +0.923 | 6 | +1.941 | +1.953 | 6 | +0.419 | +0.430 | 6 | +1.941 | +1.953 | 2 | +2.229 | +2.242 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 5 | +0.425 | +0.564 | 4 | -0.822 | +0.067 | 4 | +0.420 | +0.583 | 4 | -0.822 | +0.009 | 1 | +1.394 | +1.454 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 3 | +1.641 | +1.527 | 2 | +3.521 | +2.657 | 2 | +0.226 | +0.085 | 2 | +3.521 | +2.714 | 1 | +3.063 | +3.030 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 7 | +1.395 | +1.408 | 5 | +2.805 | +2.817 | 5 | +0.429 | +0.441 | 5 | +2.805 | +2.816 | 2 | +2.229 | +2.242 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 4 | +0.913 | +1.052 | 3 | +1.084 | +1.972 | 3 | +0.431 | +0.595 | 3 | +1.084 | +1.914 | 1 | +1.394 | +1.454 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 3 | +1.641 | +1.527 | 2 | +3.521 | +2.657 | 2 | +0.226 | +0.085 | 2 | +3.521 | +2.714 | 1 | +3.063 | +3.030 | 0 | — | — |
| UNIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 11 | +0.634 | +0.646 | 9 | +0.362 | +0.374 | 7 | +1.158 | +1.169 | 7 | -0.251 | -0.239 | 4 | -0.153 | -0.140 | 2 | +1.728 | +1.741 |
| UNIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 6 | +0.896 | +1.034 | 5 | -0.250 | +0.639 | 4 | +0.590 | +0.754 | 4 | -1.240 | -0.410 | 2 | +1.777 | +1.837 | 1 | +2.168 | +3.347 |
| UNIUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 5 | -0.935 | -1.049 | 4 | +2.329 | +1.464 | 3 | +1.963 | +1.822 | 3 | +3.369 | +2.562 | 2 | -2.039 | -2.073 | 1 | +1.288 | +0.134 |
| UNIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 8 | +0.957 | +0.969 | 7 | +1.288 | +1.300 | 5 | +1.279 | +1.291 | 5 | +0.363 | +0.374 | 3 | +0.630 | +0.644 | 2 | +1.728 | +1.741 |
| UNIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 5 | +0.636 | +0.775 | 4 | -0.934 | -0.045 | 3 | +0.022 | +0.186 | 3 | -2.231 | -1.400 | 2 | +1.777 | +1.837 | 1 | +2.168 | +3.347 |
| UNIUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 3 | +1.963 | +1.849 | 3 | +3.370 | +2.506 | 2 | +2.051 | +1.910 | 2 | +3.988 | +3.180 | 1 | -0.934 | -0.967 | 1 | +1.288 | +0.134 |
| UNIUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 13 | -0.173 | -0.161 | 12 | +3.332 | +3.344 | 8 | +0.380 | +0.391 | 8 | +2.086 | +2.098 | 5 | -0.900 | -0.887 | 4 | +5.030 | +5.042 |
| UNIUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 6 | -0.537 | -0.398 | 6 | +0.489 | +1.378 | 4 | +1.745 | +1.909 | 4 | +3.877 | +4.708 | 2 | -2.396 | -2.336 | 2 | +0.489 | +1.669 |
| UNIUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 7 | +0.863 | +0.749 | 6 | +3.331 | +2.467 | 4 | -0.463 | -0.604 | 4 | +2.086 | +1.279 | 3 | +0.867 | +0.833 | 2 | +5.984 | +4.830 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 182 | -0.168 | -0.107 | 182 | +0.026 | +0.086 | 59 | +0.271 | +0.321 | 59 | -0.545 | -0.494 | 123 | -0.388 | -0.323 | 123 | +0.140 | +0.206 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 89 | -0.622 | -0.426 | 89 | -0.844 | -0.138 | 28 | -0.616 | -0.425 | 28 | -1.188 | -0.363 | 61 | -0.616 | -0.416 | 61 | -0.708 | -0.069 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 93 | +0.227 | +0.151 | 93 | +0.663 | +0.077 | 31 | +0.510 | +0.420 | 31 | -0.216 | -0.940 | 62 | -0.111 | -0.181 | 62 | +1.063 | +0.555 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 157 | -0.077 | -0.017 | 157 | -0.153 | -0.093 | 54 | +0.189 | +0.239 | 54 | -0.378 | -0.328 | 103 | -0.111 | -0.046 | 103 | +0.135 | +0.200 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 78 | -0.622 | -0.426 | 78 | -0.882 | -0.176 | 27 | -0.619 | -0.428 | 27 | -0.917 | -0.092 | 51 | -0.623 | -0.423 | 51 | -0.846 | -0.207 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 79 | +0.392 | +0.317 | 79 | +0.663 | +0.077 | 27 | +0.398 | +0.308 | 27 | -0.217 | -0.941 | 52 | +0.414 | +0.344 | 52 | +1.063 | +0.555 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 162 | -0.194 | -0.134 | 161 | +0.137 | +0.197 | 54 | +0.264 | +0.314 | 54 | +0.070 | +0.120 | 108 | -0.344 | -0.279 | 107 | +0.256 | +0.321 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 81 | -0.033 | +0.163 | 80 | -0.556 | +0.150 | 27 | +0.321 | +0.511 | 27 | -0.917 | -0.092 | 54 | -0.170 | +0.030 | 53 | -0.417 | +0.222 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 81 | -0.275 | -0.351 | 81 | +1.049 | +0.463 | 27 | +0.116 | +0.026 | 27 | +0.322 | -0.402 | 54 | -0.400 | -0.470 | 54 | +1.866 | +1.357 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 144 | -0.093 | -0.032 | 143 | +0.137 | +0.197 | 50 | +0.292 | +0.343 | 50 | +0.234 | +0.285 | 94 | -0.364 | -0.299 | 93 | +0.133 | +0.198 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 71 | +0.199 | +0.395 | 70 | -0.555 | +0.152 | 26 | +0.357 | +0.547 | 26 | -0.551 | +0.274 | 45 | -0.138 | +0.062 | 44 | -0.562 | +0.076 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 73 | -0.190 | -0.266 | 73 | +0.883 | +0.297 | 24 | +0.190 | +0.100 | 24 | +0.499 | -0.225 | 49 | -0.382 | -0.452 | 49 | +1.656 | +1.148 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 131 | -0.259 | -0.199 | 131 | -0.414 | -0.353 | 43 | +0.824 | +0.875 | 43 | -0.922 | -0.872 | 88 | -0.445 | -0.380 | 88 | -0.335 | -0.270 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 73 | -0.458 | -0.262 | 73 | -1.049 | -0.342 | 23 | +1.042 | +1.233 | 23 | -0.915 | -0.090 | 50 | -0.857 | -0.657 | 50 | -1.184 | -0.545 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 58 | +0.629 | +0.553 | 58 | +0.810 | +0.224 | 20 | +0.765 | +0.676 | 20 | -0.469 | -1.193 | 38 | +0.577 | +0.507 | 38 | +1.384 | +0.876 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 117 | -0.017 | +0.043 | 117 | -0.322 | -0.262 | 41 | +0.780 | +0.830 | 41 | -0.923 | -0.873 | 76 | -0.320 | -0.255 | 76 | +0.260 | +0.325 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 66 | -0.397 | -0.201 | 66 | -0.917 | -0.210 | 23 | +1.042 | +1.233 | 23 | -0.915 | -0.090 | 43 | -0.634 | -0.435 | 43 | -0.629 | +0.010 |
| 1000PEPEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 51 | +0.625 | +0.549 | 51 | +0.856 | +0.269 | 18 | +0.601 | +0.511 | 18 | -0.470 | -1.194 | 33 | +0.617 | +0.547 | 33 | +1.416 | +0.908 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 133 | -0.195 | -0.134 | 132 | -0.692 | -0.632 | 48 | +0.086 | +0.136 | 48 | +0.571 | +0.621 | 85 | -0.385 | -0.320 | 84 | -0.781 | -0.716 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 66 | -0.149 | +0.047 | 65 | -1.028 | -0.322 | 25 | +0.488 | +0.678 | 25 | -0.202 | +0.623 | 41 | -0.492 | -0.292 | 40 | -1.430 | -0.791 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 67 | -0.235 | -0.311 | 67 | +0.053 | -0.533 | 23 | -0.001 | -0.091 | 23 | +1.238 | +0.513 | 44 | -0.242 | -0.312 | 44 | -0.674 | -1.182 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 123 | -0.081 | -0.021 | 122 | -0.776 | -0.715 | 42 | +0.617 | +0.667 | 42 | +0.335 | +0.385 | 81 | -0.236 | -0.171 | 80 | -1.272 | -1.206 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 62 | -0.083 | +0.114 | 61 | -1.182 | -0.475 | 24 | +0.551 | +0.741 | 24 | -0.217 | +0.607 | 38 | -0.291 | -0.091 | 37 | -1.705 | -1.067 |
| 1000PEPEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 61 | -0.011 | -0.087 | 61 | -0.659 | -1.245 | 18 | +0.931 | +0.841 | 18 | +1.084 | +0.360 | 43 | -0.235 | -0.305 | 43 | -0.705 | -1.213 |
| 1000PEPEUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 315 | +0.213 | +0.273 | 315 | -0.413 | -0.353 | 87 | +0.324 | +0.374 | 87 | -0.041 | +0.009 | 228 | +0.180 | +0.245 | 228 | -0.459 | -0.394 |
| 1000PEPEUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 170 | +0.050 | +0.247 | 170 | -0.636 | +0.070 | 51 | +0.267 | +0.457 | 51 | -0.400 | +0.424 | 119 | -0.014 | +0.186 | 119 | -0.700 | -0.062 |
| 1000PEPEUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 145 | +0.307 | +0.231 | 145 | -0.059 | -0.645 | 36 | +0.417 | +0.327 | 36 | +0.564 | -0.160 | 109 | +0.303 | +0.233 | 109 | -0.198 | -0.706 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 43 | +0.562 | +0.590 | 42 | +0.647 | +0.675 | 16 | -0.093 | -0.070 | 16 | +0.918 | +0.941 | 27 | +0.589 | +0.621 | 26 | +0.448 | +0.479 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 22 | +0.673 | +0.978 | 22 | -0.518 | +0.534 | 9 | +1.902 | +2.179 | 9 | +2.092 | +2.970 | 13 | +0.596 | +0.919 | 13 | -0.835 | +0.337 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 21 | -0.441 | -0.689 | 20 | +2.215 | +1.220 | 7 | -1.312 | -1.544 | 7 | +0.617 | -0.216 | 14 | +0.468 | +0.207 | 13 | +2.852 | +1.742 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 34 | +0.417 | +0.445 | 33 | -0.000 | +0.028 | 14 | -0.093 | -0.070 | 14 | +0.611 | +0.634 | 20 | +0.577 | +0.608 | 19 | -0.355 | -0.324 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 19 | +0.597 | +0.902 | 19 | -0.720 | +0.332 | 8 | +1.412 | +1.689 | 8 | +1.046 | +1.925 | 11 | +0.566 | +0.888 | 11 | -0.931 | +0.242 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 15 | -0.440 | -0.688 | 14 | +2.589 | +1.594 | 6 | -1.719 | -1.951 | 6 | -2.900 | -3.733 | 9 | +1.032 | +0.771 | 8 | +2.888 | +1.777 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 32 | +0.335 | +0.363 | 31 | -0.031 | -0.002 | 10 | +0.367 | +0.390 | 10 | -0.239 | -0.216 | 22 | +0.306 | +0.337 | 21 | -0.033 | -0.002 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 17 | +0.647 | +0.951 | 17 | -1.189 | -0.137 | 6 | +1.276 | +1.554 | 6 | -0.995 | -0.116 | 11 | +0.596 | +0.919 | 11 | -1.189 | -0.016 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 15 | -0.698 | -0.946 | 14 | +1.155 | +0.160 | 4 | -0.580 | -0.812 | 4 | +0.387 | -0.446 | 11 | -0.702 | -0.963 | 10 | +1.810 | +0.699 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 29 | +0.594 | +0.622 | 28 | -0.258 | -0.230 | 9 | +0.083 | +0.106 | 9 | -0.481 | -0.458 | 20 | +0.643 | +0.674 | 19 | -0.031 | -0.000 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 15 | +0.647 | +0.951 | 15 | -1.376 | -0.324 | 5 | +0.647 | +0.924 | 5 | -1.995 | -1.117 | 10 | +0.647 | +0.970 | 10 | -1.282 | -0.109 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 14 | -0.312 | -0.560 | 13 | +1.247 | +0.251 | 4 | -0.580 | -0.812 | 4 | +0.387 | -0.446 | 10 | +0.124 | -0.137 | 9 | +2.558 | +1.447 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 31 | +0.540 | +0.568 | 29 | -0.838 | -0.809 | 13 | +0.704 | +0.727 | 13 | +0.141 | +0.164 | 18 | +0.108 | +0.139 | 16 | -1.376 | -1.345 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 17 | +0.542 | +0.847 | 16 | -1.370 | -0.318 | 8 | +0.936 | +1.214 | 8 | +1.242 | +2.121 | 9 | +0.121 | +0.444 | 8 | -1.658 | -0.485 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 14 | +0.350 | +0.102 | 13 | +2.561 | +1.565 | 5 | +0.703 | +0.471 | 5 | +0.140 | -0.692 | 9 | +0.100 | -0.161 | 8 | +3.670 | +2.560 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 29 | +0.498 | +0.526 | 27 | -0.836 | -0.808 | 12 | +0.676 | +0.699 | 12 | +1.313 | +1.336 | 17 | +0.102 | +0.133 | 15 | -1.381 | -1.351 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 17 | +0.542 | +0.847 | 16 | -1.370 | -0.318 | 8 | +0.936 | +1.214 | 8 | +1.242 | +2.121 | 9 | +0.121 | +0.444 | 8 | -1.658 | -0.485 |
| 1000PEPEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 12 | +0.096 | -0.152 | 11 | +2.562 | +1.567 | 4 | -0.040 | -0.271 | 4 | +1.589 | +0.756 | 8 | +0.095 | -0.166 | 7 | +2.561 | +1.450 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 26 | +0.841 | +0.869 | 25 | +0.849 | +0.877 | 11 | +0.054 | +0.077 | 11 | -1.015 | -0.992 | 15 | +0.888 | +0.919 | 14 | +2.306 | +2.337 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 11 | +0.109 | +0.414 | 11 | -1.181 | -0.129 | 5 | +1.176 | +1.454 | 5 | +6.133 | +7.011 | 6 | -0.138 | +0.185 | 6 | -2.828 | -1.656 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 15 | +1.352 | +1.104 | 14 | +1.407 | +0.412 | 6 | -0.652 | -0.884 | 6 | -4.073 | -4.905 | 9 | +1.651 | +1.390 | 8 | +4.759 | +3.648 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 28 | -0.020 | +0.009 | 27 | -0.625 | -0.597 | 12 | -0.530 | -0.507 | 12 | -1.095 | -1.072 | 16 | +0.075 | +0.106 | 15 | +0.500 | +0.531 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 15 | -0.986 | -0.681 | 15 | -2.774 | -1.723 | 6 | +0.549 | +0.827 | 6 | +2.479 | +3.358 | 9 | -1.390 | -1.067 | 9 | -2.882 | -1.709 |
| 1000PEPEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 13 | +0.788 | +0.540 | 12 | +1.410 | +0.415 | 6 | -1.566 | -1.798 | 6 | -3.474 | -4.307 | 7 | +1.654 | +1.393 | 6 | +4.786 | +3.675 |
| 1000PEPEUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 72 | +0.838 | +0.867 | 72 | +0.463 | +0.491 | 29 | +0.844 | +0.867 | 29 | -0.938 | -0.915 | 43 | +0.823 | +0.854 | 43 | +1.088 | +1.119 |
| 1000PEPEUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 44 | +0.757 | +1.062 | 44 | -1.439 | -0.387 | 20 | +1.460 | +1.738 | 20 | -1.074 | -0.195 | 24 | +0.437 | +0.760 | 24 | -2.445 | -1.273 |
| 1000PEPEUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 28 | +0.902 | +0.654 | 28 | +2.340 | +1.345 | 9 | +0.182 | -0.050 | 9 | +2.217 | +1.384 | 19 | +1.066 | +0.805 | 19 | +2.470 | +1.359 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 6 | -0.315 | -0.305 | 5 | -0.098 | -0.088 | 3 | +0.098 | +0.107 | 3 | -0.097 | -0.089 | 3 | -0.729 | -0.718 | 2 | +0.124 | +0.134 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 2 | +0.624 | +1.106 | 2 | +3.033 | +3.929 | 2 | +0.624 | +0.990 | 2 | +3.033 | +1.463 | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 4 | -0.317 | -0.779 | 3 | -2.266 | -3.143 | 1 | +0.098 | -0.251 | 1 | -26.834 | -25.247 | 3 | -0.729 | -1.295 | 2 | +0.124 | -1.838 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 4 | -1.231 | -1.220 | 3 | -0.098 | -0.088 | 2 | +0.624 | +0.633 | 2 | +3.033 | +3.041 | 2 | -2.816 | -2.805 | 1 | -2.269 | -2.258 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 2 | +0.624 | +1.106 | 2 | +3.033 | +3.929 | 2 | +0.624 | +0.990 | 2 | +3.033 | +1.463 | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 2 | -2.816 | -3.278 | 1 | -2.269 | -3.145 | 0 | — | — | 0 | — | — | 2 | -2.816 | -3.382 | 1 | -2.269 | -4.230 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 5 | +2.603 | +2.613 | 5 | +1.549 | +1.559 | 2 | +0.665 | +0.674 | 2 | -22.076 | -22.068 | 3 | +2.742 | +2.753 | 3 | +1.549 | +1.560 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 2 | +2.677 | +3.159 | 2 | +3.465 | +4.360 | 1 | +2.608 | +2.974 | 1 | +5.377 | +3.807 | 1 | +2.745 | +3.334 | 1 | +1.552 | +3.535 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 3 | +0.123 | -0.339 | 3 | +0.887 | +0.011 | 1 | -1.278 | -1.627 | 1 | -49.530 | -47.943 | 2 | +2.538 | +1.972 | 2 | +2.456 | +0.495 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 2 | +2.677 | +2.687 | 2 | +3.465 | +3.474 | 1 | +2.608 | +2.617 | 1 | +5.377 | +5.386 | 1 | +2.745 | +2.756 | 1 | +1.552 | +1.563 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 2 | +2.677 | +3.159 | 2 | +3.465 | +4.360 | 1 | +2.608 | +2.974 | 1 | +5.377 | +3.807 | 1 | +2.745 | +3.334 | 1 | +1.552 | +3.535 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 3 | +0.126 | +0.136 | 3 | +0.890 | +0.900 | 1 | +0.098 | +0.107 | 1 | -26.834 | -26.825 | 2 | +1.050 | +1.061 | 2 | +0.936 | +0.947 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 1 | +1.976 | +2.458 | 1 | +0.986 | +1.882 | 0 | — | — | 0 | — | — | 1 | +1.976 | +2.564 | 1 | +0.986 | +2.968 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 2 | +0.111 | -0.351 | 2 | -12.973 | -13.850 | 1 | +0.098 | -0.251 | 1 | -26.834 | -25.247 | 1 | +0.123 | -0.443 | 1 | +0.887 | -1.074 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 1 | +1.976 | +1.986 | 1 | +0.986 | +0.996 | 0 | — | — | 0 | — | — | 1 | +1.976 | +1.987 | 1 | +0.986 | +0.996 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 1 | +1.976 | +2.458 | 1 | +0.986 | +1.882 | 0 | — | — | 0 | — | — | 1 | +1.976 | +2.564 | 1 | +0.986 | +2.968 |
| 1000PEPEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 5 | +0.477 | +0.487 | 4 | -2.129 | -2.119 | 2 | -10.986 | -10.978 | 2 | -57.732 | -57.723 | 3 | +1.230 | +1.241 | 2 | -0.002 | +0.009 |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 1 | -1.093 | -0.611 | 1 | -2.289 | -1.393 | 1 | -1.093 | -0.727 | 1 | -2.289 | -3.859 | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 4 | +0.853 | +0.391 | 3 | -1.967 | -2.844 | 1 | -20.879 | -21.228 | 1 | -113.174 | -111.587 | 3 | +1.230 | +0.663 | 2 | -0.002 | -1.963 |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 3 | +0.480 | +0.490 | 2 | -2.127 | -2.117 | 1 | -1.093 | -1.084 | 1 | -2.289 | -2.280 | 2 | +1.038 | +1.049 | 1 | -1.964 | -1.954 |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 1 | -1.093 | -0.611 | 1 | -2.289 | -1.393 | 1 | -1.093 | -0.727 | 1 | -2.289 | -3.859 | 0 | — | — | 0 | — | — |
| 1000PEPEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 2 | +1.038 | +0.576 | 1 | -1.964 | -2.841 | 0 | — | — | 0 | — | — | 2 | +1.038 | +0.471 | 1 | -1.964 | -3.926 |
| 1000PEPEUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 4 | -1.367 | -1.357 | 4 | +0.213 | +0.223 | 1 | -2.993 | -2.984 | 1 | +0.924 | +0.933 | 3 | -0.751 | -0.740 | 3 | -0.498 | -0.488 |
| 1000PEPEUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 3 | -0.751 | -0.269 | 3 | -0.498 | +0.397 | 0 | — | — | 0 | — | — | 3 | -0.751 | -0.163 | 3 | -0.498 | +1.484 |
| 1000PEPEUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 1 | -2.993 | -3.455 | 1 | +0.924 | +0.048 | 1 | -2.993 | -3.341 | 1 | +0.924 | +2.511 | 0 | — | — | 0 | — | — |
| DOGEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 324 | -0.125 | -0.044 | 324 | -0.566 | -0.486 | 196 | -0.041 | +0.036 | 196 | -0.427 | -0.350 | 128 | -0.336 | -0.251 | 128 | -0.864 | -0.779 |
| DOGEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 152 | -0.169 | -0.040 | 152 | -0.915 | -0.520 | 92 | -0.035 | +0.083 | 92 | -0.581 | -0.277 | 60 | -0.888 | -0.737 | 60 | -2.060 | -1.453 |
| DOGEUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 172 | -0.033 | -0.001 | 172 | -0.051 | -0.286 | 104 | -0.027 | +0.010 | 104 | -0.257 | -0.406 | 68 | +0.010 | +0.028 | 68 | +0.771 | +0.332 |
| DOGEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 293 | -0.155 | -0.075 | 293 | -0.606 | -0.526 | 175 | -0.043 | +0.034 | 175 | -0.468 | -0.391 | 118 | -0.380 | -0.295 | 118 | -0.916 | -0.832 |
| DOGEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 143 | -0.171 | -0.042 | 143 | -0.877 | -0.482 | 87 | -0.029 | +0.088 | 87 | -0.543 | -0.239 | 56 | -0.888 | -0.737 | 56 | -2.039 | -1.431 |
| DOGEUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 150 | -0.115 | -0.084 | 150 | -0.392 | -0.627 | 88 | -0.132 | -0.096 | 88 | -0.470 | -0.620 | 62 | +0.008 | +0.026 | 62 | +0.618 | +0.179 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 292 | -0.159 | -0.079 | 291 | -0.312 | -0.232 | 173 | -0.102 | -0.025 | 173 | -0.146 | -0.069 | 119 | -0.196 | -0.112 | 118 | -0.774 | -0.689 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 137 | -0.141 | -0.012 | 136 | -0.888 | -0.493 | 81 | +0.014 | +0.132 | 81 | -0.548 | -0.244 | 56 | -0.944 | -0.793 | 55 | -1.277 | -0.669 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 155 | -0.165 | -0.133 | 155 | +0.014 | -0.220 | 92 | -0.331 | -0.294 | 92 | -0.022 | -0.171 | 63 | +0.190 | +0.207 | 63 | +0.612 | +0.172 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 259 | -0.180 | -0.099 | 258 | -0.318 | -0.237 | 156 | -0.107 | -0.030 | 156 | -0.237 | -0.160 | 103 | -0.421 | -0.337 | 102 | -0.773 | -0.688 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 126 | -0.153 | -0.024 | 125 | -0.730 | -0.334 | 77 | +0.015 | +0.132 | 77 | -0.203 | +0.101 | 49 | -1.031 | -0.880 | 48 | -1.355 | -0.747 |
| DOGEUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 133 | -0.205 | -0.173 | 133 | -0.160 | -0.394 | 79 | -0.385 | -0.348 | 79 | -0.277 | -0.427 | 54 | -0.146 | -0.128 | 54 | +0.310 | -0.129 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 243 | +0.072 | +0.152 | 243 | +0.190 | +0.271 | 149 | -0.054 | +0.023 | 149 | +0.196 | +0.273 | 94 | +0.327 | +0.411 | 94 | +0.151 | +0.236 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 123 | +0.012 | +0.141 | 123 | -0.462 | -0.067 | 73 | -0.046 | +0.071 | 73 | -0.364 | -0.060 | 50 | +0.207 | +0.358 | 50 | -0.818 | -0.210 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 120 | +0.214 | +0.246 | 120 | +0.698 | +0.464 | 76 | -0.036 | +0.001 | 76 | +0.577 | +0.428 | 44 | +0.417 | +0.434 | 44 | +0.960 | +0.521 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 219 | +0.094 | +0.174 | 219 | +0.192 | +0.272 | 132 | -0.044 | +0.033 | 132 | +0.149 | +0.226 | 87 | +0.336 | +0.420 | 87 | +0.191 | +0.276 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 116 | +0.081 | +0.210 | 116 | -0.424 | -0.029 | 70 | -0.036 | +0.082 | 70 | -0.253 | +0.051 | 46 | +0.329 | +0.480 | 46 | -0.614 | -0.006 |
| DOGEUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 103 | +0.248 | +0.280 | 103 | +0.646 | +0.411 | 62 | -0.040 | -0.003 | 62 | +0.554 | +0.405 | 41 | +0.500 | +0.517 | 41 | +0.984 | +0.545 |
| DOGEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 260 | -0.331 | -0.251 | 260 | -0.545 | -0.465 | 167 | -0.128 | -0.051 | 167 | -0.377 | -0.300 | 93 | -0.931 | -0.847 | 93 | -1.402 | -1.317 |
| DOGEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 132 | -0.210 | -0.081 | 132 | -0.419 | -0.024 | 88 | +0.101 | +0.219 | 88 | +0.112 | +0.416 | 44 | -0.833 | -0.682 | 44 | -1.459 | -0.851 |
| DOGEUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 128 | -0.435 | -0.403 | 128 | -0.604 | -0.839 | 79 | -0.260 | -0.224 | 79 | -0.611 | -0.760 | 49 | -1.046 | -1.029 | 49 | -0.554 | -0.993 |
| DOGEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 241 | -0.414 | -0.334 | 241 | -0.606 | -0.526 | 148 | -0.192 | -0.115 | 148 | -0.247 | -0.170 | 93 | -0.929 | -0.845 | 93 | -1.504 | -1.420 |
| DOGEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 123 | -0.146 | -0.017 | 123 | -0.543 | -0.148 | 79 | +0.218 | +0.335 | 79 | +0.093 | +0.397 | 44 | -0.831 | -0.680 | 44 | -1.850 | -1.242 |
| DOGEUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 118 | -0.610 | -0.578 | 118 | -0.669 | -0.904 | 69 | -0.424 | -0.387 | 69 | -0.715 | -0.865 | 49 | -1.046 | -1.029 | 49 | -0.440 | -0.879 |
| DOGEUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 450 | -0.032 | +0.048 | 449 | +0.258 | +0.338 | 278 | -0.029 | +0.048 | 278 | -0.144 | -0.067 | 172 | -0.051 | +0.033 | 171 | +0.640 | +0.724 |
| DOGEUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 237 | -0.112 | +0.016 | 237 | -0.312 | +0.083 | 145 | -0.081 | +0.036 | 145 | -0.482 | -0.178 | 92 | -0.423 | -0.272 | 92 | -0.036 | +0.571 |
| DOGEUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 213 | +0.115 | +0.147 | 212 | +0.888 | +0.653 | 133 | -0.004 | +0.033 | 133 | +0.280 | +0.131 | 80 | +0.273 | +0.290 | 79 | +1.748 | +1.309 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 73 | +0.224 | +0.261 | 73 | +0.514 | +0.551 | 42 | +0.204 | +0.240 | 42 | +0.084 | +0.120 | 31 | +0.349 | +0.389 | 31 | +0.679 | +0.719 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 40 | +0.403 | +0.588 | 40 | -0.565 | +0.198 | 22 | +0.564 | +0.704 | 22 | -0.451 | +0.064 | 18 | +0.161 | +0.417 | 18 | -0.808 | +0.415 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 33 | +0.192 | +0.082 | 33 | +1.379 | +0.691 | 20 | -0.153 | -0.221 | 20 | +0.758 | +0.315 | 13 | +0.666 | +0.490 | 13 | +2.544 | +1.401 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 67 | +0.223 | +0.261 | 67 | +0.497 | +0.534 | 39 | +0.182 | +0.218 | 39 | +0.231 | +0.267 | 28 | +0.439 | +0.480 | 28 | +0.587 | +0.627 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 39 | +0.456 | +0.641 | 39 | -0.470 | +0.293 | 21 | +0.667 | +0.807 | 21 | -0.437 | +0.078 | 18 | +0.161 | +0.417 | 18 | -0.808 | +0.415 |
| DOGEUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 28 | -0.155 | -0.265 | 28 | +1.246 | +0.557 | 18 | -0.456 | -0.524 | 18 | +0.756 | +0.313 | 10 | +0.672 | +0.496 | 10 | +3.183 | +2.041 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 67 | +0.452 | +0.490 | 67 | +0.511 | +0.549 | 37 | +0.457 | +0.493 | 37 | +0.318 | +0.354 | 30 | +0.356 | +0.396 | 30 | +1.068 | +1.108 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 37 | +0.149 | +0.334 | 37 | -0.141 | +0.623 | 20 | +0.816 | +0.956 | 20 | +0.387 | +0.902 | 17 | -0.319 | -0.063 | 17 | -0.957 | +0.265 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 30 | +0.678 | +0.568 | 30 | +2.232 | +1.544 | 17 | -0.512 | -0.580 | 17 | +0.313 | -0.130 | 13 | +2.231 | +2.055 | 13 | +4.763 | +3.621 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 57 | +0.614 | +0.651 | 57 | +1.022 | +1.060 | 32 | +0.538 | +0.574 | 32 | +0.984 | +1.020 | 25 | +1.542 | +1.582 | 25 | +1.019 | +1.059 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 31 | +0.459 | +0.644 | 31 | +0.254 | +1.018 | 17 | +0.824 | +0.965 | 17 | +1.454 | +1.969 | 14 | -0.294 | -0.038 | 14 | -2.695 | -1.473 |
| DOGEUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 26 | +0.863 | +0.753 | 26 | +2.232 | +1.544 | 15 | -0.614 | -0.682 | 15 | +0.313 | -0.130 | 11 | +2.571 | +2.395 | 11 | +5.712 | +4.570 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 55 | +0.160 | +0.197 | 54 | -0.384 | -0.346 | 34 | +0.355 | +0.391 | 34 | -0.108 | -0.072 | 21 | -0.132 | -0.092 | 20 | -1.542 | -1.503 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 33 | +0.162 | +0.347 | 32 | +0.180 | +0.943 | 18 | +0.374 | +0.514 | 18 | +0.786 | +1.301 | 15 | -0.132 | +0.124 | 14 | -2.458 | -1.236 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 22 | +0.016 | -0.094 | 22 | -0.770 | -1.458 | 16 | +0.016 | -0.052 | 16 | -0.913 | -1.356 | 6 | +0.278 | +0.102 | 6 | +1.724 | +0.582 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 49 | +0.160 | +0.197 | 48 | -0.110 | -0.073 | 31 | +0.284 | +0.320 | 31 | -0.076 | -0.040 | 18 | -0.081 | -0.041 | 17 | -2.746 | -2.706 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 31 | +0.165 | +0.350 | 30 | +0.559 | +1.323 | 17 | +0.461 | +0.601 | 17 | +0.954 | +1.469 | 14 | -0.224 | +0.032 | 13 | -2.743 | -1.521 |
| DOGEUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 18 | +0.016 | -0.094 | 18 | -0.914 | -1.602 | 14 | -0.452 | -0.520 | 14 | -0.914 | -1.357 | 4 | +1.947 | +1.771 | 4 | -4.811 | -5.953 |
| DOGEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 60 | -0.216 | -0.178 | 60 | +0.270 | +0.308 | 34 | -0.010 | +0.026 | 34 | +1.057 | +1.093 | 26 | -0.330 | -0.289 | 26 | -0.809 | -0.769 |
| DOGEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 31 | -0.207 | -0.022 | 31 | +1.445 | +2.208 | 16 | +0.403 | +0.543 | 16 | +1.746 | +2.261 | 15 | -0.923 | -0.667 | 15 | -0.728 | +0.494 |
| DOGEUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 29 | -0.256 | -0.365 | 29 | -0.395 | -1.083 | 18 | -0.489 | -0.557 | 18 | +0.077 | -0.366 | 11 | -0.086 | -0.262 | 11 | -0.890 | -2.032 |
| DOGEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 57 | -0.207 | -0.169 | 57 | -0.392 | -0.354 | 32 | -0.010 | +0.026 | 32 | +1.598 | +1.634 | 25 | -0.250 | -0.210 | 25 | -2.339 | -2.299 |
| DOGEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 30 | -0.193 | -0.008 | 30 | +0.958 | +1.721 | 15 | +1.109 | +1.249 | 15 | +2.190 | +2.705 | 15 | -0.921 | -0.664 | 15 | -2.339 | -1.116 |
| DOGEUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 27 | -0.254 | -0.364 | 27 | -0.603 | -1.291 | 17 | -0.524 | -0.592 | 17 | -0.396 | -0.839 | 10 | -0.037 | -0.213 | 10 | -2.781 | -3.923 |
| DOGEUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 103 | -0.004 | +0.034 | 103 | +0.319 | +0.357 | 63 | +0.436 | +0.472 | 63 | +0.321 | +0.357 | 40 | -0.451 | -0.411 | 40 | -0.029 | +0.011 |
| DOGEUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 58 | -0.016 | +0.169 | 58 | -0.442 | +0.322 | 31 | +0.433 | +0.574 | 31 | +0.153 | +0.668 | 27 | -0.360 | -0.103 | 27 | -1.628 | -0.405 |
| DOGEUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 45 | +0.199 | +0.089 | 45 | +0.638 | -0.050 | 32 | +0.393 | +0.325 | 32 | +0.527 | +0.084 | 13 | -0.553 | -0.729 | 13 | +2.241 | +1.099 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 12 | +0.630 | +0.644 | 12 | +1.075 | +1.088 | 8 | +0.501 | +0.514 | 8 | +1.077 | +1.090 | 4 | +1.394 | +1.408 | 4 | -0.089 | -0.075 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 7 | +0.013 | +0.303 | 7 | +0.112 | +1.153 | 5 | +0.014 | +0.187 | 5 | +0.113 | +0.809 | 2 | -1.348 | -0.861 | 2 | -0.411 | +1.691 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 5 | +1.707 | +1.443 | 5 | +2.038 | +1.023 | 3 | +1.109 | +0.963 | 3 | +2.041 | +1.372 | 2 | +2.922 | +2.464 | 2 | +0.301 | -1.774 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 11 | +0.273 | +0.287 | 11 | +0.109 | +0.122 | 8 | +0.501 | +0.514 | 8 | +1.077 | +1.090 | 3 | +0.271 | +0.286 | 3 | -3.559 | -3.545 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 7 | +0.013 | +0.303 | 7 | +0.112 | +1.153 | 5 | +0.014 | +0.187 | 5 | +0.113 | +0.809 | 2 | -1.348 | -0.861 | 2 | -0.411 | +1.691 |
| DOGEUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 4 | +1.408 | +1.145 | 4 | +1.042 | +0.027 | 3 | +1.109 | +0.963 | 3 | +2.041 | +1.372 | 1 | +2.516 | +2.058 | 1 | -3.560 | -5.635 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 10 | +1.049 | +1.062 | 10 | +0.187 | +0.200 | 7 | +0.993 | +1.006 | 7 | +0.269 | +0.282 | 3 | +1.453 | +1.467 | 3 | -0.120 | -0.106 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 5 | +0.014 | +0.305 | 5 | -0.112 | +0.929 | 4 | +0.504 | +0.677 | 4 | -0.255 | +0.441 | 1 | -1.774 | -1.288 | 1 | -0.118 | +1.984 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 5 | +1.453 | +1.189 | 5 | +0.345 | -0.670 | 3 | +1.109 | +0.963 | 3 | +0.348 | -0.322 | 2 | +1.979 | +1.521 | 2 | +2.826 | +0.751 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 10 | +1.049 | +1.062 | 10 | +0.187 | +0.200 | 7 | +0.993 | +1.006 | 7 | +0.269 | +0.282 | 3 | +1.453 | +1.467 | 3 | -0.120 | -0.106 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 5 | +0.014 | +0.305 | 5 | -0.112 | +0.929 | 4 | +0.504 | +0.677 | 4 | -0.255 | +0.441 | 1 | -1.774 | -1.288 | 1 | -0.118 | +1.984 |
| DOGEUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 5 | +1.453 | +1.189 | 5 | +0.345 | -0.670 | 3 | +1.109 | +0.963 | 3 | +0.348 | -0.322 | 2 | +1.979 | +1.521 | 2 | +2.826 | +0.751 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 10 | +0.319 | +0.332 | 9 | -0.834 | -0.821 | 5 | +0.241 | +0.254 | 5 | -0.834 | -0.821 | 5 | +0.394 | +0.408 | 4 | -0.938 | -0.924 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 4 | -0.541 | -0.251 | 4 | -0.936 | +0.105 | 2 | +0.618 | +0.791 | 2 | -1.665 | -0.970 | 2 | -2.012 | -1.525 | 2 | -0.938 | +1.164 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 6 | +0.750 | +0.487 | 5 | -0.835 | -1.850 | 3 | -1.245 | -1.392 | 3 | -0.835 | -1.505 | 3 | +1.386 | +0.928 | 2 | -1.988 | -4.063 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 8 | +0.319 | +0.332 | 7 | -0.830 | -0.817 | 4 | +0.615 | +0.628 | 4 | -0.363 | -0.350 | 4 | -0.465 | -0.451 | 3 | -0.828 | -0.815 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 4 | -0.541 | -0.251 | 4 | -0.936 | +0.105 | 2 | +0.618 | +0.791 | 2 | -1.665 | -0.970 | 2 | -2.012 | -1.525 | 2 | -0.938 | +1.164 |
| DOGEUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 4 | +0.750 | +0.486 | 3 | +0.740 | -0.275 | 2 | -0.071 | -0.218 | 2 | +0.600 | -0.069 | 2 | +0.892 | +0.434 | 1 | +0.743 | -1.332 |
| DOGEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 11 | +0.889 | +0.902 | 10 | +0.749 | +0.762 | 5 | +0.893 | +0.906 | 5 | +1.285 | +1.298 | 6 | +0.911 | +0.925 | 5 | -0.373 | -0.360 |
| DOGEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 4 | +0.060 | +0.350 | 4 | +1.192 | +2.233 | 2 | -0.178 | -0.005 | 2 | +2.891 | +3.586 | 2 | +5.962 | +6.449 | 2 | +0.373 | +2.475 |
| DOGEUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 7 | +0.888 | +0.625 | 6 | +0.749 | -0.266 | 3 | +0.893 | +0.747 | 3 | +1.285 | +0.616 | 4 | +0.910 | +0.452 | 3 | -0.373 | -2.448 |
| DOGEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 11 | +0.889 | +0.903 | 10 | +1.347 | +1.361 | 6 | +0.142 | +0.155 | 6 | +0.754 | +0.767 | 5 | +1.877 | +1.891 | 4 | +3.399 | +3.413 |
| DOGEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 5 | +1.127 | +1.417 | 5 | +2.423 | +3.465 | 3 | -0.610 | -0.437 | 3 | -0.033 | +0.663 | 2 | +7.406 | +7.892 | 2 | +3.518 | +5.620 |
| DOGEUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 6 | +0.599 | +0.336 | 5 | +1.281 | +0.266 | 3 | +0.893 | +0.747 | 3 | +1.285 | +0.616 | 3 | +0.310 | -0.148 | 2 | +1.999 | -0.075 |
| DOGEUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 17 | +0.100 | +0.114 | 17 | -0.092 | -0.079 | 11 | +0.100 | +0.113 | 11 | -1.001 | -0.988 | 6 | -0.283 | -0.269 | 6 | +5.525 | +5.539 |
| DOGEUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 11 | +0.101 | +0.391 | 11 | -0.092 | +0.950 | 9 | +0.533 | +0.705 | 9 | -0.092 | +0.603 | 2 | -1.091 | -0.604 | 2 | +11.000 | +13.102 |
| DOGEUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 6 | -2.850 | -3.113 | 6 | -10.105 | -11.119 | 2 | -7.984 | -8.131 | 2 | -323.404 | -324.074 | 4 | +0.908 | +0.450 | 4 | +5.523 | +3.448 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | both | 143 | +0.115 | +0.171 | 142 | -0.639 | -0.583 | 36 | +0.911 | +0.952 | 36 | -1.482 | -1.441 | 107 | -0.119 | -0.060 | 106 | -0.295 | -0.235 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | long | 58 | +0.246 | +0.479 | 57 | -1.634 | -0.583 | 17 | +0.496 | +0.646 | 17 | -1.732 | -1.340 | 41 | +0.185 | +0.443 | 40 | -1.519 | -0.321 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_first | record | ALL | short | 85 | -0.103 | -0.226 | 85 | +0.561 | -0.379 | 19 | +1.377 | +1.309 | 19 | -1.226 | -1.537 | 66 | -0.170 | -0.310 | 66 | +0.563 | -0.516 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 125 | +0.079 | +0.134 | 124 | -1.029 | -0.974 | 31 | +0.790 | +0.831 | 31 | -1.738 | -1.698 | 94 | -0.119 | -0.060 | 93 | -0.320 | -0.260 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 53 | +0.256 | +0.489 | 52 | -1.516 | -0.465 | 15 | +1.028 | +1.178 | 15 | -1.741 | -1.349 | 38 | +0.211 | +0.470 | 37 | -1.398 | -0.201 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 72 | -0.164 | -0.287 | 72 | -0.586 | -1.527 | 16 | +0.351 | +0.283 | 16 | -2.230 | -2.541 | 56 | -0.218 | -0.357 | 56 | +0.117 | -0.961 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | both | 128 | +0.285 | +0.340 | 128 | -0.279 | -0.224 | 32 | +0.783 | +0.823 | 32 | -1.107 | -1.067 | 96 | +0.106 | +0.166 | 96 | -0.204 | -0.144 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | long | 54 | -0.167 | +0.066 | 54 | -1.190 | -0.139 | 17 | +1.237 | +1.386 | 17 | -0.937 | -0.545 | 37 | -0.254 | +0.004 | 37 | -1.641 | -0.444 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_first | record | ALL | short | 74 | +0.462 | +0.339 | 74 | +0.977 | +0.037 | 15 | +0.767 | +0.699 | 15 | -1.744 | -2.055 | 59 | +0.405 | +0.265 | 59 | +1.184 | +0.106 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 109 | +0.406 | +0.461 | 109 | -0.293 | -0.238 | 31 | +0.798 | +0.839 | 31 | -0.941 | -0.900 | 78 | +0.305 | +0.365 | 78 | -0.284 | -0.225 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 50 | +0.178 | +0.412 | 50 | -1.190 | -0.139 | 17 | +1.237 | +1.386 | 17 | -0.937 | -0.545 | 33 | -0.165 | +0.093 | 33 | -1.641 | -0.444 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 59 | +0.783 | +0.659 | 59 | +0.830 | -0.111 | 14 | +0.781 | +0.713 | 14 | -0.451 | -0.762 | 45 | +1.042 | +0.902 | 45 | +0.884 | -0.194 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | both | 98 | -0.308 | -0.253 | 98 | -0.498 | -0.443 | 20 | -0.079 | -0.038 | 20 | -0.952 | -0.912 | 78 | -0.368 | -0.308 | 78 | -0.218 | -0.159 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | long | 44 | -0.709 | -0.475 | 44 | -2.190 | -1.139 | 10 | +0.623 | +0.772 | 10 | -0.472 | -0.080 | 34 | -0.959 | -0.700 | 34 | -2.435 | -1.238 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_first | record | ALL | short | 54 | +0.624 | +0.501 | 54 | +1.195 | +0.255 | 10 | -0.497 | -0.565 | 10 | -1.705 | -2.016 | 44 | +0.843 | +0.703 | 44 | +1.451 | +0.373 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 81 | -0.132 | -0.077 | 81 | -0.683 | -0.628 | 17 | +0.033 | +0.074 | 17 | -1.268 | -1.228 | 64 | -0.204 | -0.145 | 64 | -0.661 | -0.602 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 36 | -0.628 | -0.395 | 36 | -2.431 | -1.380 | 8 | +0.623 | +0.772 | 8 | -0.472 | -0.080 | 28 | -0.782 | -0.523 | 28 | -2.983 | -1.786 |
| 1000BONKUSDT | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 45 | +0.626 | +0.502 | 45 | +1.567 | +0.627 | 9 | -0.196 | -0.264 | 9 | -2.774 | -3.085 | 36 | +0.844 | +0.705 | 36 | +1.861 | +0.783 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_first | record | ALL | both | 95 | -0.314 | -0.259 | 95 | -0.045 | +0.010 | 21 | -0.362 | -0.321 | 21 | -0.033 | +0.008 | 74 | -0.313 | -0.254 | 74 | -0.430 | -0.370 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_first | record | ALL | long | 43 | -0.092 | +0.141 | 43 | -1.626 | -0.575 | 9 | +0.160 | +0.309 | 9 | -2.797 | -2.405 | 34 | -0.190 | +0.068 | 34 | -1.488 | -0.291 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_first | record | ALL | short | 52 | -0.400 | -0.523 | 52 | +0.127 | -0.814 | 12 | -1.069 | -1.137 | 12 | -0.004 | -0.314 | 40 | -0.352 | -0.491 | 40 | +0.260 | -0.818 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 85 | -0.251 | -0.196 | 85 | +0.007 | +0.062 | 24 | -0.547 | -0.507 | 24 | -2.218 | -2.177 | 61 | -0.216 | -0.157 | 61 | +0.290 | +0.350 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 39 | -0.161 | +0.073 | 39 | -0.946 | +0.105 | 11 | -0.243 | -0.094 | 11 | -2.795 | -2.403 | 28 | -0.129 | +0.129 | 28 | -0.459 | +0.738 |
| 1000BONKUSDT | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 46 | -0.341 | -0.464 | 46 | +0.147 | -0.793 | 13 | -0.847 | -0.915 | 13 | -1.636 | -1.947 | 33 | -0.344 | -0.483 | 33 | +0.600 | -0.478 |
| 1000BONKUSDT | 1h | calibrated | SFP_harden | record | ALL | both | 208 | +0.062 | +0.117 | 208 | +0.006 | +0.061 | 40 | -0.369 | -0.328 | 40 | +0.463 | +0.504 | 168 | +0.098 | +0.157 | 168 | -0.208 | -0.148 |
| 1000BONKUSDT | 1h | calibrated | SFP_harden | record | ALL | long | 97 | -0.805 | -0.571 | 97 | -1.178 | -0.127 | 18 | -1.167 | -1.018 | 18 | -0.233 | +0.159 | 79 | -0.807 | -0.549 | 79 | -1.506 | -0.309 |
| 1000BONKUSDT | 1h | calibrated | SFP_harden | record | ALL | short | 111 | +0.477 | +0.354 | 111 | +0.789 | -0.151 | 22 | +0.536 | +0.468 | 22 | +2.149 | +1.838 | 89 | +0.473 | +0.334 | 89 | +0.771 | -0.308 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | both | 22 | +0.255 | +0.281 | 22 | -1.037 | -1.011 | 4 | -1.086 | -1.067 | 4 | -0.915 | -0.895 | 18 | +0.450 | +0.479 | 18 | -1.040 | -1.012 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | long | 11 | -0.789 | -0.395 | 11 | -2.356 | -0.807 | 3 | -1.461 | -1.210 | 3 | -2.350 | -2.725 | 8 | -0.305 | +0.132 | 8 | -2.644 | -0.594 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_first | record | ALL | short | 11 | +0.576 | +0.234 | 11 | +3.862 | +2.365 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 10 | +0.811 | +0.431 | 10 | +4.227 | +2.233 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 17 | +0.174 | +0.200 | 17 | +0.514 | +0.540 | 4 | -1.086 | -1.067 | 4 | -0.915 | -0.895 | 13 | +0.180 | +0.209 | 13 | +3.862 | +3.890 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 8 | -1.190 | -0.796 | 8 | -3.363 | -1.815 | 3 | -1.461 | -1.210 | 3 | -2.350 | -2.725 | 5 | -1.184 | -0.747 | 5 | -5.852 | -3.802 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 9 | +0.576 | +0.234 | 9 | +4.593 | +3.097 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 8 | +0.811 | +0.431 | 8 | +4.891 | +2.897 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | both | 18 | -0.501 | -0.475 | 18 | -0.966 | -0.940 | 4 | -0.534 | -0.514 | 4 | +0.185 | +0.204 | 14 | +0.134 | +0.162 | 14 | -1.290 | -1.262 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | long | 11 | -0.363 | +0.031 | 11 | -1.904 | -0.356 | 3 | -0.359 | -0.108 | 3 | -0.782 | -1.156 | 8 | -0.380 | +0.057 | 8 | -2.544 | -0.493 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_first | record | ALL | short | 7 | -0.643 | -0.985 | 7 | +5.568 | +4.072 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 6 | +0.572 | +0.192 | 6 | +5.984 | +3.990 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 15 | -0.364 | -0.338 | 15 | -1.142 | -1.116 | 4 | -0.534 | -0.514 | 4 | +0.185 | +0.204 | 11 | +0.909 | +0.937 | 11 | -1.432 | -1.404 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 10 | +0.275 | +0.669 | 10 | -2.303 | -0.755 | 3 | -0.359 | -0.108 | 3 | -0.782 | -1.156 | 7 | +0.911 | +1.348 | 7 | -3.180 | -1.129 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 5 | -0.643 | -0.985 | 5 | +1.634 | +0.138 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 4 | +0.639 | +0.259 | 4 | +4.017 | +2.023 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | both | 16 | +0.719 | +0.745 | 16 | +1.061 | +1.087 | 4 | +0.167 | +0.187 | 4 | +1.068 | +1.087 | 12 | +0.991 | +1.019 | 12 | +1.491 | +1.519 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | long | 9 | -0.151 | +0.243 | 9 | -0.142 | +1.406 | 3 | +0.713 | +0.964 | 3 | +0.984 | +0.610 | 6 | -1.436 | -0.999 | 6 | -2.376 | -0.326 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_first | record | ALL | short | 7 | +2.066 | +1.724 | 7 | +3.108 | +1.612 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 6 | +2.129 | +1.748 | 6 | +3.123 | +1.129 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 9 | +0.731 | +0.757 | 9 | +0.977 | +1.003 | 3 | -0.378 | -0.359 | 3 | +1.152 | +1.171 | 6 | +0.991 | +1.019 | 6 | -2.374 | -2.346 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 6 | +0.290 | +0.684 | 6 | -2.374 | -0.825 | 2 | +1.565 | +1.816 | 2 | +1.671 | +1.297 | 4 | +0.289 | +0.727 | 4 | -4.364 | -2.314 |
| 1000BONKUSDT | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 3 | +1.256 | +0.914 | 3 | +3.109 | +1.613 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 2 | +3.154 | +2.774 | 2 | +5.497 | +3.503 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_first | record | ALL | both | 21 | -0.555 | -0.529 | 20 | +0.853 | +0.879 | 2 | -0.775 | -0.756 | 2 | +0.864 | +0.883 | 19 | +1.046 | +1.075 | 18 | +1.463 | +1.491 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_first | record | ALL | long | 8 | -1.356 | -0.962 | 8 | -1.349 | +0.200 | 1 | -0.843 | -0.591 | 1 | +0.576 | +0.202 | 7 | -1.534 | -1.097 | 7 | -1.437 | +0.614 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_first | record | ALL | short | 13 | +1.365 | +1.023 | 12 | +4.447 | +2.950 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 12 | +1.934 | +1.554 | 11 | +5.535 | +3.542 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 16 | -0.636 | -0.610 | 15 | +0.568 | +0.593 | 2 | -0.775 | -0.756 | 2 | +0.864 | +0.883 | 14 | +0.249 | +0.277 | 13 | +0.352 | +0.380 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 7 | -1.178 | -0.784 | 7 | -1.261 | +0.288 | 1 | -0.843 | -0.591 | 1 | +0.576 | +0.202 | 6 | -1.356 | -0.919 | 6 | -1.349 | +0.702 |
| 1000BONKUSDT | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 9 | +1.366 | +1.024 | 8 | +2.970 | +1.474 | 1 | -0.708 | -0.921 | 1 | +1.152 | +1.565 | 8 | +1.935 | +1.554 | 7 | +3.358 | +1.364 |
| 1000BONKUSDT | 4h | calibrated | SFP_harden | record | ALL | both | 50 | +0.560 | +0.586 | 50 | +0.011 | +0.037 | 10 | +2.593 | +2.612 | 10 | +0.930 | +0.949 | 40 | +0.454 | +0.482 | 40 | -0.356 | -0.327 |
| 1000BONKUSDT | 4h | calibrated | SFP_harden | record | ALL | long | 36 | +0.562 | +0.956 | 36 | -0.296 | +1.252 | 9 | +2.654 | +2.905 | 9 | +1.340 | +0.966 | 27 | +0.480 | +0.917 | 27 | -1.541 | +0.509 |
| 1000BONKUSDT | 4h | calibrated | SFP_harden | record | ALL | short | 14 | +1.167 | +0.825 | 14 | +5.685 | +4.189 | 1 | +2.530 | +2.317 | 1 | -2.031 | -1.618 | 13 | +0.387 | +0.007 | 13 | +6.060 | +4.066 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | both | 3 | -0.425 | -0.416 | 3 | -1.659 | -1.650 | 1 | -0.575 | -0.568 | 1 | -1.659 | -1.652 | 2 | +0.947 | +0.957 | 2 | +0.732 | +0.742 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | long | 2 | -0.499 | +0.139 | 2 | -2.493 | -0.815 | 1 | -0.575 | -0.968 | 1 | -1.659 | -2.690 | 1 | -0.423 | +0.429 | 1 | -3.328 | -0.318 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_first | record | ALL | short | 1 | +2.317 | +1.698 | 1 | +4.792 | +3.132 | 0 | — | — | 0 | — | — | 1 | +2.317 | +1.485 | 1 | +4.792 | +1.801 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 2 | +0.947 | +0.957 | 2 | +0.732 | +0.741 | 0 | — | — | 0 | — | — | 2 | +0.947 | +0.957 | 2 | +0.732 | +0.742 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 1 | -0.423 | +0.216 | 1 | -3.328 | -1.650 | 0 | — | — | 0 | — | — | 1 | -0.423 | +0.429 | 1 | -3.328 | -0.318 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 1 | +2.317 | +1.698 | 1 | +4.792 | +3.132 | 0 | — | — | 0 | — | — | 1 | +2.317 | +1.485 | 1 | +4.792 | +1.801 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | both | 3 | -0.424 | -0.415 | 3 | -1.284 | -1.275 | 1 | -0.550 | -0.543 | 1 | -1.284 | -1.278 | 2 | +1.116 | +1.126 | 2 | +0.889 | +0.898 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | long | 2 | -0.486 | +0.152 | 2 | -2.306 | -0.628 | 1 | -0.550 | -0.942 | 1 | -1.284 | -2.316 | 1 | -0.423 | +0.429 | 1 | -3.328 | -0.318 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_first | record | ALL | short | 1 | +2.654 | +2.035 | 1 | +5.105 | +3.445 | 0 | — | — | 0 | — | — | 1 | +2.654 | +1.822 | 1 | +5.105 | +2.114 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 2 | +1.116 | +1.125 | 2 | +0.889 | +0.898 | 0 | — | — | 0 | — | — | 2 | +1.116 | +1.126 | 2 | +0.889 | +0.898 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 1 | -0.423 | +0.216 | 1 | -3.328 | -1.650 | 0 | — | — | 0 | — | — | 1 | -0.423 | +0.429 | 1 | -3.328 | -0.318 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 1 | +2.654 | +2.035 | 1 | +5.105 | +3.445 | 0 | — | — | 0 | — | — | 1 | +2.654 | +1.822 | 1 | +5.105 | +2.114 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | both | 2 | +0.203 | +0.212 | 2 | -1.311 | -1.302 | 1 | +0.990 | +0.996 | 1 | +0.809 | +0.816 | 1 | -0.583 | -0.573 | 1 | -3.432 | -3.422 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | long | 2 | +0.203 | +0.841 | 2 | -1.311 | +0.367 | 1 | +0.990 | +0.597 | 1 | +0.809 | -0.222 | 1 | -0.583 | +0.269 | 1 | -3.432 | -0.421 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_first | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 2 | +0.203 | +0.212 | 2 | -1.311 | -1.302 | 1 | +0.990 | +0.996 | 1 | +0.809 | +0.816 | 1 | -0.583 | -0.573 | 1 | -3.432 | -3.422 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 2 | +0.203 | +0.841 | 2 | -1.311 | +0.367 | 1 | +0.990 | +0.597 | 1 | +0.809 | -0.222 | 1 | -0.583 | +0.269 | 1 | -3.432 | -0.421 |
| 1000BONKUSDT | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — | 0 | — | — |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_first | record | ALL | both | 3 | -0.550 | -0.540 | 3 | -1.836 | -1.827 | 1 | -0.548 | -0.541 | 1 | -1.834 | -1.827 | 2 | -0.481 | -0.472 | 2 | -3.000 | -2.991 |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_first | record | ALL | long | 2 | -1.237 | -0.599 | 2 | -3.873 | -2.195 | 1 | -0.548 | -0.940 | 1 | -1.834 | -2.865 | 1 | -1.926 | -1.074 | 1 | -5.912 | -2.902 |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_first | record | ALL | short | 1 | +0.963 | +0.344 | 1 | -0.089 | -1.749 | 0 | — | — | 0 | — | — | 1 | +0.963 | +0.131 | 1 | -0.089 | -3.080 |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 3 | -0.550 | -0.540 | 3 | -1.836 | -1.827 | 1 | -0.548 | -0.541 | 1 | -1.834 | -1.827 | 2 | +1.215 | +1.225 | 2 | +0.418 | +0.428 |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 2 | -1.237 | -0.599 | 2 | -3.873 | -2.195 | 1 | -0.548 | -0.940 | 1 | -1.834 | -2.865 | 1 | -1.926 | -1.074 | 1 | -5.912 | -2.902 |
| 1000BONKUSDT | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 1 | +4.356 | +3.737 | 1 | +6.749 | +5.089 | 0 | — | — | 0 | — | — | 1 | +4.356 | +3.524 | 1 | +6.749 | +3.758 |
| 1000BONKUSDT | 1d | calibrated | SFP_harden | record | ALL | both | 7 | -0.963 | -0.954 | 7 | +1.270 | +1.279 | 1 | +3.667 | +3.674 | 1 | +4.928 | +4.935 | 6 | -1.423 | -1.414 | 6 | +1.108 | +1.117 |
| 1000BONKUSDT | 1d | calibrated | SFP_harden | record | ALL | long | 6 | -1.423 | -0.785 | 6 | +1.108 | +2.786 | 0 | — | — | 0 | — | — | 6 | -1.423 | -0.571 | 6 | +1.108 | +4.118 |
| 1000BONKUSDT | 1d | calibrated | SFP_harden | record | ALL | short | 1 | +3.667 | +3.047 | 1 | +4.928 | +3.268 | 1 | +3.667 | +4.073 | 1 | +4.928 | +5.973 | 0 | — | — | 0 | — | — |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_first | record | ALL | both | 2687 | -0.120 | -0.007 | 2680 | -0.156 | -0.042 | 1314 | +0.003 | +0.104 | 1314 | -0.121 | -0.020 | 1373 | -0.282 | -0.136 | 1366 | -0.211 | -0.065 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_first | record | ALL | long | 1368 | -0.115 | -0.006 | 1361 | -0.344 | -0.149 | 691 | +0.089 | +0.136 | 691 | -0.161 | -0.127 | 677 | -0.385 | -0.194 | 670 | -0.653 | -0.270 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_first | record | ALL | short | 1319 | -0.126 | -0.007 | 1319 | +0.097 | +0.129 | 623 | -0.073 | +0.081 | 623 | -0.002 | +0.166 | 696 | -0.169 | -0.068 | 696 | +0.208 | +0.117 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | both | 2325 | -0.115 | -0.001 | 2318 | -0.183 | -0.070 | 1147 | +0.009 | +0.110 | 1147 | -0.156 | -0.055 | 1178 | -0.282 | -0.136 | 1171 | -0.236 | -0.090 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | long | 1206 | -0.112 | -0.003 | 1199 | -0.423 | -0.228 | 613 | +0.096 | +0.144 | 613 | -0.232 | -0.199 | 593 | -0.379 | -0.188 | 586 | -0.676 | -0.292 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap89_oneshot | record | ALL | short | 1119 | -0.114 | +0.004 | 1119 | +0.108 | +0.139 | 534 | -0.056 | +0.098 | 534 | +0.040 | +0.208 | 585 | -0.169 | -0.068 | 585 | +0.163 | +0.072 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_first | record | ALL | both | 2390 | -0.155 | -0.042 | 2384 | -0.182 | -0.068 | 1176 | -0.083 | +0.017 | 1176 | -0.167 | -0.066 | 1214 | -0.217 | -0.071 | 1208 | -0.225 | -0.079 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_first | record | ALL | long | 1235 | -0.080 | +0.029 | 1229 | -0.300 | -0.105 | 631 | +0.084 | +0.132 | 631 | -0.077 | -0.044 | 604 | -0.338 | -0.147 | 598 | -0.545 | -0.162 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_first | record | ALL | short | 1155 | -0.210 | -0.092 | 1155 | -0.044 | -0.012 | 545 | -0.285 | -0.131 | 545 | -0.183 | -0.015 | 610 | -0.124 | -0.023 | 610 | +0.172 | +0.081 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | both | 2103 | -0.123 | -0.009 | 2097 | -0.192 | -0.079 | 1044 | -0.034 | +0.067 | 1044 | -0.172 | -0.071 | 1059 | -0.216 | -0.070 | 1053 | -0.272 | -0.125 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | long | 1095 | -0.071 | +0.038 | 1089 | -0.300 | -0.105 | 559 | +0.145 | +0.193 | 559 | -0.038 | -0.004 | 536 | -0.366 | -0.175 | 530 | -0.590 | -0.206 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap127_oneshot | record | ALL | short | 1008 | -0.162 | -0.044 | 1008 | -0.127 | -0.095 | 485 | -0.227 | -0.073 | 485 | -0.297 | -0.130 | 523 | -0.118 | -0.017 | 523 | +0.126 | +0.035 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_first | record | ALL | both | 1998 | -0.106 | +0.008 | 1997 | -0.079 | +0.035 | 976 | -0.061 | +0.040 | 976 | +0.084 | +0.185 | 1022 | -0.189 | -0.042 | 1021 | -0.271 | -0.125 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_first | record | ALL | long | 1053 | -0.250 | -0.141 | 1052 | -0.337 | -0.142 | 521 | -0.070 | -0.023 | 521 | +0.162 | +0.196 | 532 | -0.480 | -0.289 | 531 | -0.767 | -0.383 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_first | record | ALL | short | 945 | +0.058 | +0.176 | 945 | +0.161 | +0.193 | 455 | +0.005 | +0.159 | 455 | -0.134 | +0.034 | 490 | +0.060 | +0.161 | 490 | +0.345 | +0.254 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | both | 1739 | -0.070 | +0.044 | 1738 | -0.034 | +0.080 | 851 | +0.015 | +0.116 | 851 | +0.083 | +0.184 | 888 | -0.166 | -0.020 | 887 | -0.204 | -0.057 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | long | 934 | -0.184 | -0.075 | 933 | -0.344 | -0.149 | 460 | -0.030 | +0.018 | 460 | +0.172 | +0.206 | 474 | -0.460 | -0.269 | 473 | -0.736 | -0.352 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_tap200_oneshot | record | ALL | short | 805 | +0.155 | +0.273 | 805 | +0.239 | +0.271 | 391 | +0.066 | +0.219 | 391 | -0.050 | +0.118 | 414 | +0.167 | +0.269 | 414 | +0.571 | +0.481 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_first | record | ALL | both | 2086 | -0.186 | -0.072 | 2081 | -0.498 | -0.385 | 1045 | -0.042 | +0.059 | 1045 | -0.317 | -0.216 | 1041 | -0.327 | -0.181 | 1036 | -0.683 | -0.536 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_first | record | ALL | long | 1116 | -0.062 | +0.047 | 1111 | -0.521 | -0.326 | 586 | +0.063 | +0.110 | 586 | -0.176 | -0.143 | 530 | -0.272 | -0.081 | 525 | -1.041 | -0.657 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_first | record | ALL | short | 970 | -0.281 | -0.163 | 970 | -0.469 | -0.437 | 459 | -0.226 | -0.072 | 459 | -0.618 | -0.450 | 511 | -0.353 | -0.252 | 511 | -0.435 | -0.526 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_oneshot | record | ALL | both | 1901 | -0.147 | -0.034 | 1897 | -0.461 | -0.347 | 951 | -0.012 | +0.088 | 951 | -0.274 | -0.173 | 950 | -0.336 | -0.189 | 946 | -0.687 | -0.541 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_oneshot | record | ALL | long | 1012 | -0.069 | +0.040 | 1008 | -0.550 | -0.355 | 529 | +0.115 | +0.163 | 529 | -0.191 | -0.157 | 483 | -0.336 | -0.145 | 479 | -1.141 | -0.757 |
| POOLED:UNSEEN12 | 1h | calibrated | BRK_mem_oneshot | record | ALL | short | 889 | -0.258 | -0.140 | 889 | -0.353 | -0.321 | 422 | -0.177 | -0.024 | 422 | -0.612 | -0.444 | 467 | -0.333 | -0.232 | 467 | -0.092 | -0.183 |
| POOLED:UNSEEN12 | 1h | calibrated | SFP_harden | record | ALL | both | 4386 | +0.025 | +0.139 | 4370 | -0.060 | +0.054 | 2142 | +0.118 | +0.219 | 2142 | -0.082 | +0.018 | 2244 | -0.051 | +0.095 | 2228 | -0.062 | +0.084 |
| POOLED:UNSEEN12 | 1h | calibrated | SFP_harden | record | ALL | long | 2175 | -0.027 | +0.082 | 2172 | -0.220 | -0.025 | 1038 | +0.217 | +0.265 | 1038 | +0.064 | +0.098 | 1137 | -0.242 | -0.051 | 1134 | -0.461 | -0.077 |
| POOLED:UNSEEN12 | 1h | calibrated | SFP_harden | record | ALL | short | 2211 | +0.068 | +0.186 | 2198 | +0.086 | +0.118 | 1104 | -0.019 | +0.135 | 1104 | -0.260 | -0.092 | 1107 | +0.069 | +0.170 | 1094 | +0.297 | +0.207 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_first | record | ALL | both | 619 | +0.052 | +0.106 | 611 | +0.457 | +0.511 | 320 | +0.038 | +0.086 | 320 | +0.633 | +0.681 | 299 | +0.048 | +0.118 | 291 | +0.061 | +0.131 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_first | record | ALL | long | 339 | +0.200 | +0.278 | 333 | -0.016 | +0.222 | 187 | +0.431 | +0.437 | 187 | +0.623 | +0.656 | 152 | -0.146 | +0.022 | 146 | -0.712 | -0.222 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_first | record | ALL | short | 280 | -0.082 | -0.052 | 278 | +0.617 | +0.486 | 133 | -0.636 | -0.547 | 133 | +0.642 | +0.705 | 147 | +0.291 | +0.263 | 145 | +0.496 | +0.146 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | both | 524 | -0.006 | +0.048 | 516 | +0.308 | +0.362 | 278 | -0.016 | +0.032 | 278 | +0.501 | +0.549 | 246 | +0.003 | +0.072 | 238 | -0.145 | -0.075 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | long | 294 | +0.198 | +0.276 | 288 | -0.193 | +0.045 | 161 | +0.383 | +0.390 | 161 | +0.497 | +0.530 | 133 | -0.185 | -0.017 | 127 | -0.703 | -0.213 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap89_oneshot | record | ALL | short | 230 | -0.207 | -0.177 | 228 | +0.669 | +0.538 | 117 | -0.639 | -0.550 | 117 | +0.639 | +0.702 | 113 | +0.232 | +0.204 | 111 | +0.820 | +0.470 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_first | record | ALL | both | 535 | -0.109 | -0.055 | 528 | +0.536 | +0.590 | 275 | +0.117 | +0.165 | 275 | +0.797 | +0.845 | 260 | -0.291 | -0.221 | 253 | -0.022 | +0.048 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_first | record | ALL | long | 301 | -0.037 | +0.041 | 296 | +0.206 | +0.445 | 165 | +0.431 | +0.437 | 165 | +0.838 | +0.871 | 136 | -0.417 | -0.249 | 131 | -0.969 | -0.479 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_first | record | ALL | short | 234 | -0.157 | -0.127 | 232 | +0.943 | +0.812 | 110 | -0.187 | -0.098 | 110 | +0.722 | +0.785 | 124 | -0.049 | -0.078 | 122 | +1.066 | +0.716 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | both | 465 | -0.043 | +0.011 | 458 | +0.513 | +0.568 | 243 | +0.101 | +0.148 | 243 | +0.677 | +0.725 | 222 | -0.181 | -0.111 | 215 | +0.061 | +0.131 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | long | 268 | +0.009 | +0.088 | 263 | +0.393 | +0.632 | 148 | +0.518 | +0.525 | 148 | +0.990 | +1.023 | 120 | -0.290 | -0.122 | 115 | -0.901 | -0.411 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap127_oneshot | record | ALL | short | 197 | -0.167 | -0.137 | 195 | +0.695 | +0.565 | 95 | -0.242 | -0.153 | 95 | +0.409 | +0.471 | 102 | +0.313 | +0.285 | 100 | +1.066 | +0.716 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_first | record | ALL | both | 452 | +0.194 | +0.248 | 444 | +0.209 | +0.263 | 241 | +0.292 | +0.339 | 241 | +0.676 | +0.724 | 211 | +0.085 | +0.155 | 203 | -0.275 | -0.205 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_first | record | ALL | long | 262 | +0.240 | +0.318 | 256 | +0.165 | +0.403 | 147 | +0.521 | +0.527 | 147 | +0.947 | +0.979 | 115 | -0.100 | +0.068 | 109 | -1.317 | -0.827 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_first | record | ALL | short | 190 | +0.127 | +0.157 | 188 | +0.421 | +0.290 | 94 | -0.102 | -0.013 | 94 | +0.208 | +0.271 | 96 | +0.362 | +0.334 | 94 | +0.666 | +0.315 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | both | 388 | +0.149 | +0.203 | 380 | +0.183 | +0.237 | 206 | +0.301 | +0.349 | 206 | +0.666 | +0.713 | 182 | +0.034 | +0.104 | 174 | -0.511 | -0.442 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | long | 233 | +0.214 | +0.292 | 227 | +0.162 | +0.400 | 128 | +0.581 | +0.588 | 128 | +0.954 | +0.986 | 105 | -0.095 | +0.073 | 99 | -1.317 | -0.827 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_tap200_oneshot | record | ALL | short | 155 | +0.039 | +0.069 | 153 | +0.207 | +0.077 | 78 | -0.115 | -0.026 | 78 | +0.176 | +0.239 | 77 | +0.291 | +0.263 | 75 | +0.421 | +0.071 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_first | record | ALL | both | 469 | -0.190 | -0.136 | 464 | -0.021 | +0.033 | 246 | -0.100 | -0.052 | 246 | +0.105 | +0.153 | 223 | -0.224 | -0.154 | 218 | -0.296 | -0.226 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_first | record | ALL | long | 256 | -0.089 | -0.010 | 254 | +0.122 | +0.360 | 145 | +0.349 | +0.356 | 145 | +0.807 | +0.839 | 111 | -0.486 | -0.318 | 109 | -0.746 | -0.256 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_first | record | ALL | short | 213 | -0.225 | -0.195 | 210 | -0.067 | -0.197 | 101 | -0.404 | -0.315 | 101 | -0.633 | -0.570 | 112 | +0.004 | -0.024 | 109 | +0.623 | +0.273 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_oneshot | record | ALL | both | 440 | -0.206 | -0.152 | 435 | +0.036 | +0.090 | 235 | -0.244 | -0.197 | 235 | -0.023 | +0.025 | 205 | -0.197 | -0.127 | 200 | +0.457 | +0.527 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_oneshot | record | ALL | long | 243 | -0.092 | -0.013 | 241 | +0.195 | +0.434 | 136 | +0.332 | +0.338 | 136 | +0.512 | +0.545 | 107 | -0.409 | -0.242 | 105 | -0.407 | +0.083 |
| POOLED:UNSEEN12 | 4h | calibrated | BRK_mem_oneshot | record | ALL | short | 197 | -0.268 | -0.238 | 194 | -0.035 | -0.166 | 99 | -0.469 | -0.380 | 99 | -0.672 | -0.609 | 98 | -0.010 | -0.038 | 95 | +1.869 | +1.518 |
| POOLED:UNSEEN12 | 4h | calibrated | SFP_harden | record | ALL | both | 929 | +0.094 | +0.149 | 922 | +0.333 | +0.387 | 455 | -0.005 | +0.043 | 455 | -0.098 | -0.050 | 474 | +0.162 | +0.232 | 467 | +0.918 | +0.988 |
| POOLED:UNSEEN12 | 4h | calibrated | SFP_harden | record | ALL | long | 468 | +0.208 | +0.287 | 463 | +0.042 | +0.281 | 201 | +0.394 | +0.401 | 201 | -0.090 | -0.057 | 267 | +0.118 | +0.286 | 262 | +0.046 | +0.536 |
| POOLED:UNSEEN12 | 4h | calibrated | SFP_harden | record | ALL | short | 461 | -0.027 | +0.003 | 459 | +0.802 | +0.671 | 254 | -0.210 | -0.121 | 254 | -0.098 | -0.035 | 207 | +0.243 | +0.215 | 205 | +1.557 | +1.206 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_first | record | ALL | both | 101 | +0.081 | +0.102 | 93 | -0.254 | -0.233 | 51 | +0.089 | +0.108 | 51 | -0.040 | -0.021 | 50 | -0.115 | -0.089 | 42 | -1.359 | -1.334 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_first | record | ALL | long | 55 | -0.037 | +0.044 | 53 | -0.945 | -0.515 | 33 | +0.311 | +0.306 | 33 | -0.105 | -0.276 | 22 | -1.268 | -1.100 | 20 | -2.891 | -1.698 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_first | record | ALL | short | 46 | +0.514 | +0.475 | 40 | +0.038 | -0.352 | 18 | +0.031 | +0.072 | 18 | -0.002 | +0.207 | 28 | +1.047 | +0.930 | 22 | +1.273 | +0.129 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | both | 82 | +0.029 | +0.050 | 76 | -0.135 | -0.115 | 43 | +0.308 | +0.327 | 43 | +0.041 | +0.059 | 39 | -0.390 | -0.364 | 33 | -1.336 | -1.311 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | long | 48 | -0.108 | -0.027 | 46 | -0.789 | -0.359 | 27 | +0.914 | +0.910 | 27 | +0.106 | -0.066 | 21 | -1.024 | -0.856 | 19 | -2.440 | -1.247 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap89_oneshot | record | ALL | short | 34 | +0.513 | +0.473 | 30 | +0.723 | +0.333 | 16 | +0.109 | +0.150 | 16 | -0.002 | +0.207 | 18 | +0.881 | +0.765 | 14 | +2.905 | +1.762 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_first | record | ALL | both | 88 | +0.030 | +0.050 | 81 | -0.123 | -0.103 | 44 | +0.034 | +0.053 | 44 | +0.304 | +0.322 | 44 | -0.043 | -0.017 | 37 | -1.338 | -1.313 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_first | record | ALL | long | 47 | -0.178 | -0.096 | 44 | -0.599 | -0.169 | 26 | +0.417 | +0.412 | 26 | -0.072 | -0.244 | 21 | -1.021 | -0.853 | 18 | -1.531 | -0.338 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_first | record | ALL | short | 41 | +0.591 | +0.551 | 37 | +0.257 | -0.132 | 18 | -0.713 | -0.671 | 18 | +0.587 | +0.796 | 23 | +1.415 | +1.299 | 19 | -1.335 | -2.478 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | both | 71 | -0.182 | -0.161 | 65 | -0.123 | -0.102 | 37 | +0.061 | +0.079 | 37 | +0.345 | +0.364 | 34 | -0.420 | -0.394 | 28 | -1.674 | -1.649 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | long | 38 | -0.282 | -0.201 | 36 | -0.788 | -0.358 | 20 | +0.670 | +0.665 | 20 | -0.263 | -0.435 | 18 | -1.085 | -0.917 | 16 | -1.531 | -0.338 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap127_oneshot | record | ALL | short | 33 | +0.590 | +0.550 | 29 | +0.341 | -0.048 | 17 | -0.418 | -0.377 | 17 | +0.832 | +1.041 | 16 | +1.477 | +1.361 | 12 | -1.675 | -2.818 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_first | record | ALL | both | 67 | +0.218 | +0.239 | 63 | -0.479 | -0.459 | 36 | +0.319 | +0.338 | 36 | +0.248 | +0.266 | 31 | +0.114 | +0.140 | 27 | -1.053 | -1.028 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_first | record | ALL | long | 33 | +0.238 | +0.319 | 32 | -0.655 | -0.225 | 19 | +0.422 | +0.417 | 19 | +0.102 | -0.069 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_first | record | ALL | short | 34 | +0.139 | +0.099 | 31 | -0.475 | -0.865 | 17 | +0.087 | +0.128 | 17 | +1.147 | +1.355 | 17 | +0.218 | +0.101 | 14 | -0.914 | -2.058 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | both | 57 | +0.219 | +0.239 | 53 | -0.475 | -0.454 | 30 | +0.328 | +0.346 | 30 | +0.936 | +0.955 | 27 | +0.048 | +0.074 | 23 | -1.053 | -1.028 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | long | 30 | +0.149 | +0.231 | 29 | -0.834 | -0.404 | 16 | +0.328 | +0.323 | 16 | +0.023 | -0.149 | 14 | -0.561 | -0.393 | 13 | -1.058 | +0.135 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_tap200_oneshot | record | ALL | short | 27 | +0.218 | +0.178 | 24 | +0.939 | +0.550 | 14 | +0.605 | +0.646 | 14 | +2.359 | +2.568 | 13 | +0.217 | +0.101 | 10 | -0.915 | -2.058 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_first | record | ALL | both | 89 | +0.601 | +0.622 | 84 | -0.176 | -0.155 | 46 | +0.137 | +0.156 | 46 | +0.560 | +0.579 | 43 | +0.731 | +0.757 | 38 | -0.563 | -0.538 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_first | record | ALL | long | 49 | +0.138 | +0.219 | 48 | -0.147 | +0.283 | 29 | +0.138 | +0.133 | 29 | +0.763 | +0.591 | 20 | +0.230 | +0.399 | 19 | -0.850 | +0.343 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_first | record | ALL | short | 40 | +0.807 | +0.767 | 36 | -0.215 | -0.605 | 17 | -0.173 | -0.132 | 17 | +0.216 | +0.425 | 23 | +1.227 | +1.110 | 19 | -0.337 | -1.480 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_oneshot | record | ALL | both | 80 | +0.616 | +0.637 | 76 | +0.229 | +0.249 | 41 | +0.136 | +0.154 | 41 | +0.357 | +0.376 | 39 | +0.757 | +0.783 | 35 | +0.004 | +0.029 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_oneshot | record | ALL | long | 46 | +0.137 | +0.218 | 45 | -0.291 | +0.139 | 26 | +0.076 | +0.071 | 26 | +0.159 | -0.013 | 20 | +0.609 | +0.777 | 19 | -0.814 | +0.379 |
| POOLED:UNSEEN12 | 1d | calibrated | BRK_mem_oneshot | record | ALL | short | 34 | +0.946 | +0.907 | 31 | +1.276 | +0.887 | 15 | +0.630 | +0.672 | 15 | +0.424 | +0.632 | 19 | +1.590 | +1.474 | 16 | +1.743 | +0.600 |
| POOLED:UNSEEN12 | 1d | calibrated | SFP_harden | record | ALL | both | 120 | -0.526 | -0.505 | 117 | +0.216 | +0.236 | 60 | +0.064 | +0.082 | 60 | +0.224 | +0.243 | 60 | -1.113 | -1.087 | 57 | +0.212 | +0.237 |
| POOLED:UNSEEN12 | 1d | calibrated | SFP_harden | record | ALL | long | 66 | -0.381 | -0.300 | 65 | +0.930 | +1.360 | 27 | +0.287 | +0.282 | 27 | -0.002 | -0.174 | 39 | -0.915 | -0.747 | 38 | +1.089 | +2.282 |
| POOLED:UNSEEN12 | 1d | calibrated | SFP_harden | record | ALL | short | 54 | -1.039 | -1.078 | 52 | +0.198 | -0.191 | 33 | -0.421 | -0.380 | 33 | +0.232 | +0.441 | 21 | -2.023 | -2.140 | 19 | -2.293 | -3.437 |
