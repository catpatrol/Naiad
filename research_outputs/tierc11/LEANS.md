# TIER-C11 · EXECUTOR READINGS (LEANS) — frozen before any TC11 book is computed

Contract of record: `exchange/queue/2026-09-24_TC11_APOLLO.md`
sha256 `bb38e016a8f3e55ca3bcc09fec53ba6b8dc40accb60d054f8163d033a898f835` (STEP Q, commit b9ed953).
Executor: HEPHAESTUS. Seed 20260924. Drafted 2026-09-25 (UTC) after the Understand phase
(`research_outputs/tierc11/scout/A..H_*.md`). Revised the same day after a five-lens adversarial review
(51 findings, disposition in §10). Frozen BEFORE any TC11 range or trade book was computed. The TC11 snapshot
build ran in parallel with the review and touches no reading here except §0.

The operator's standing word is "conscientious range design — never ask again". So every ambiguity is resolved
here as a named executor reading. Each reading quotes the contract phrase it reads, says what it chose and why,
and names the rival reading. Every rival that is cheap to compute is printed beside the reading of record as a
Tier-E twin ("a SELECTION, not a result").
- A reading may be challenged at CLOSE. It is never re-chosen after a number is seen.
- If a reading must change mid-build, the change is filed here as a dated AMENDMENT with its reason, and every
  downstream artifact is redone.

---------------------------------------------------------------------------------------------------------------
## 0 · Substrate, corridor, code reuse

**L-0.1 CORRIDOR** — "Corridor: full water, latest closed 4h bar, one as-of pin."
- The pin is the latest 4h bar closed when the contract was filed and committed (commit 00:09Z): **as_of_close_ms
  1790294400000 = 2026-09-25T00:00:00Z** (bar open 2026-09-24T20:00Z).
- The pin is proven closed by the venue's own closeTime and written once. Every stage reads it, and the latest
  close at fetch time is printed beside it.
- "Full water" means each asset's whole history, as in TC5, with the 316-bar warm-up.

**L-0.2 SNAPSHOT** — a new frozen snapshot `~/.cache/naiad/snapshots/tc11_20260925`.
- It is an APFS clone of `tc10_20260921`, re-hashed against TC10's STAGE_D_MANIFEST first.
- It is extended over REST from each file's edge + step to the pin: 17 × {5m, 1h, 4h, 12h}; CLASSIC5 15m; funding.
  1d and 1w are re-derived from native 4h.
- The live cache is never read and never written. The TC10 snapshot is never written.

**L-0.3 CODE REUSE — TWO SHIMS, A CLOSED RE-ROOT LIST, AN AUDIT HOOK.** TC11 re-uses TC10's code rather than
forking it.
- **`scripts/tierc11_env.py` (range-free).** It imports `tierc2_baseline` first under the TC11 snapshot, so the
  loaders bind to TC11. It then imports tierc10_data, tierc10_panel, tierc10_brk and tierc10_lanes, plus the
  tierc2..9 lineage, with `NAIAD_CACHE_DIR` pointed at the TC10 path **only for the duration of each import
  statement**. It never imports tierc10_census, tierc10_stamps, tierc10_null or analytics.rangefinder_census.
- **`scripts/tierc11_nest.py` (the only TC11 module that reaches the range machine).** It imports tierc11_env,
  then tierc10_census, tierc10_stamps and tierc10_null under a second import window. Every runner that calls
  `BK.macro_signals`, `BK.grid_toll_atr` or an LN census path imports it first.
- **The closed re-root list** is assigned after the imports, each item printed as a lean:
  - `D.SNAPSHOT`, `D.OUT`, and `D.STEP_MS['15m'] = 900_000` in place;
  - `C.SNAPSHOT`, `C.OUT`, `C.STAGE_D`, `C.NULL_ROOT`, `C.SEED`;
  - `C.LENSES / LENS_MS / LENS_SOURCE / TS_FMT` extended **in place** for 15m, 1h, 12h, 1w;
  - `stamps.SNAPSHOT / OUT / LENS_MS`;
  - `TP.OUT / OUT_RERUN / AS_OF_PIN / STAGE_D_MANIFEST / SEED`;
  - `BK.SEED / OUT / OUT_RERUN / LENS_MS / TUNING_RESULT_FOR / HEIGHT_VS_TOLL_PATH / HEIGHT_VS_TOLL_VERDICT_PATH /
    REGISTRY_PIN_PATH / REGISTRATION_TEXTS_PATH`;
  - `LN.SEED / OUT / REGISTRY_PIN_PATH / REGISTRATION_TEXTS_PATH`.
- **Defaults bound at def time are NOT re-rooted.** Every TC11 call passes `seed=20260924` and `n_boot=4000`
  explicitly. None relies on a `family_m` default, and TC11 never calls a TP registry door (L-1.4).
- **The post-shim assertion HALTs unless** all of these hold:
  - `D.load_pin()`, `TP.stage_d_pin()` and `C.as_of_close_ms(s)[0]` for every s all equal 1790294400000;
  - `D.kline_path('BTCUSDT', '4h')` resolves under tc11_20260925;
  - `C.RETEST_PINS == {margin_atr 1.0, hold_bars 3, ttl_bars 400, grid_sha 2135ca66…}`.
  TC10 records are read by absolute main-tree path, so the assertion holds in review worktrees too.
- **The audit hook** (`sys.addaudithook`), installed last, raises on:
  - any open of a path under the TC10 snapshot or the live cache;
  - any write under `research_outputs/tierc10/`, `scripts/tierc10_*` or `exchange/status/LEDGER*`.
  Reads of an explicit allow-list of TC10 records (control journal, P-TRG-2 scored json, TUNING_RESULT,
  STEP0_RECORD, the five-row table, the P_AGE_1 table) are permitted and logged.
- F-SUBSTRATE proves the hook: a planted TC10-snapshot read and a planted tierc10 write must each FAIL.

**L-0.4 NAMES**
- Scripts are `scripts/tierc11_*.py`, outputs `research_outputs/tierc11/`, and commit subjects start `tierc11(`.
- PROGRESS stages are prefixed `TC11-`: D, R, W, G, T, S, A, H, REG, SCORE, FIX, CLOSE.
- `research_outputs/tierc11/PROGRESS.json` is a separate ledger. TC10's PROGRESS is never touched.

**L-0.5 GIT**
- `.gitignore` gains lines only at its end: `research_outputs/tierc11/**/*.parquet` and
  `research_outputs/tierc11/**/_det_*/`.
- Documents of record (md/json/txt) are committed; parquet shas live in PROGRESS and the manifests.
- Only tierc11 paths are staged.

---------------------------------------------------------------------------------------------------------------
## 1 · Tolls, eras, rulers, verdicts

**L-1.1 TOLL OF RECORD (taker)** — 5.0 bps per side, 10.0 bps round trip (`tierc2_rules.py:122-123`). This is
deducted in `net_r` together with funding, as in every TC-series book.
- **Haircut twin** on every trade row: charter slippage of A 2 / B 5 / C 10 bps per side on top.
- TC10's operator question Q2 (whether slippage joins the toll of record) stays open.

**L-1.2 MAKER TWIN** — "maker toll (limit fill at the 5m close, entry and target only)".
- Maker fee is 2.0 bps per side (`README.md:150`, "maker is 0.02%"; precedent `scripts/v3_recompute.py:957-966`),
  an ASSUMPTION. MNT is the same, also marked as an assumption.
- Maker legs carry zero slippage. Stop and invalidation legs stay taker.
- **Two maker rows:**
  - "fill assumed" — the contract's twin, filled at the named price;
  - "fill conditioned" — the entry books only if the next 5m bar trades strictly through the limit (low < P for
    a long, high > P for a short). Otherwise there is no trade, and the misses are counted.
- In R2 the maker twin of the toll is 4.0 bps round trip.

**L-1.3 ERAS** — one law everywhere in TC11: **era = the entry (or event-anchor) bar's CLOSE**. Tuning closes
≤ 2024-06-30T23:59:59Z (1719791999000); holdout is after.
- `TP.in_era` and `BK.require_era` (which read the open) are not used for TC11 era gating. A bar straddling the
  cut is printed as a count.
- A registration naming no era is scored on the **full corridor** (TC10 precedent: P-TRG-2). Its tuning and
  holdout slices are printed beside as Tier-E.
- P-SCALP-2 names the holdout era, so it is scored there.

**L-1.4 SCORER AND VERDICT**
- TC11 does not route through TP's registry doors (`register`, `require_registered`, `require_arm`, `score`,
  `external_book`, `finish_family`). They need TC10's text format, and TP's `verdict` column is CI-only.
  `TP.REG_DIR` and `TP.FAMILY_M` are left untouched.
- **`scripts/tierc11_score.py`** verifies `REGISTRATIONS.json` before scoring: the contract sha, each text slice,
  each payload sha, and the chain head pinned in a tracked file. It then computes, with seed 20260924,
  n_boot 4000, `_ci_from`, and the sensitivity seed 20260816 beside:
  - **vs zero** = `T5.cluster_boot(net_r)`;
  - **two-sample** = `T5.cluster_boot_diff(book, base)`;
  - **paired** = `T5.cluster_boot` of per-campaign deltas keyed (symbol, entry_ms). A paired row HALTs
    ("paired premise failed", no verdict) unless the two key sets are identical and n equals len(base).
- The cluster-90% interval is the 5th–95th percentile. p = (#draws ≤ 0 + 1)/(B + 1), one-sided upward.
- **verdict_of_record = SUPPORTED iff (a) CI lo > 0 AND (b) p ≤ 0.10/9 = 0.011111**, else NOT SUPPORTED.
  - Clause (b) implies (a) under the percentile bootstrap, so the deciding bound (the 1.111th percentile) is
    printed.
  - LOAO (bar 3/5; 9/17 for a 17-asset view) is printed beside and decides nothing.
  - The verdict at the sensitivity seed is printed beside.
- A CI wholly below zero is described as such ("NOT SUPPORTED — CI wholly below zero"). It is not a separate
  verdict.
- **m = 9 in every case.** A registration closed by its own precondition (P-SCALP-2) or condition (P-WARN-1)
  prints that reason in the verdict cell, spends no test, and never loosens the bar. This is conservative:
  P(condition ∧ p ≤ bar) ≤ bar.
- **Honesty labels.** A registration carrying `pre_seen` or `selection_hazard` prints its §0 cell as
  "<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (<hazard>)". The family bar applies unchanged, and the row is
  never cited as confirmation.
- **Tier-E rows carry no verdict word.** Their CI-only reading is printed as `would_read_ci_only`, alongside the
  collar columns `tier = 'TIER-E'`, `selection_not_a_result = 'a SELECTION, not a result'` and
  `gates = 'nothing'`. This applies to every non-registered table and every R2 row except the lens verdict of
  record.
- **Rulers:**

  | ruler | registrations |
  |---|---|
  | paired vs v6 | P-WARN-1, P-ADD-BRK, P-ADD-SFP, P-TP-RNG |
  | two-sample vs v6 | P-AGE-1, P-WIN-1 |
  | two-sample vs the v6 (12/26-triggered) base | P-RELAY-1 |
  | vs zero | P-BRK-4H, P-SCALP-2 |

**L-1.5 PAIRED = THE v6 CAMPAIGN SET, TRANSFORMED; GATES = POST-FILTERS**
- Exit rules and adds transform each v6 campaign: same arm, entry, stop and R. When an early exit frees the
  one-position-per-asset slot, no new entry is admitted. The re-ride rival is printed as a disclosure count.
- **Identity law.** Every campaign on which a paired rule never acts carries v6's `net_r`, `exit_ms` and
  `exit_reason` exactly (0.000e+00), asserted over the whole book before scoring. For adds, the v6 leg is
  identical and Δ = the tranches' net R.
- A gate is a **post-filter**: gated = v6 minus the refused campaigns (F-GATE). The re-ride rival is printed as a
  disclosure count.
- **Gate rows print** the refused cohort's n, mean and ΣR, plus ΣR of both books. If mean(refused) > 0, the §0
  cell appends "on per-campaign expectancy only; the gate forfeits +X R total".

**L-1.6 THE BOOKS**
- **Base v6** = `TP.CONTROL_CARD` + `T9.V6_ROLES` via `TP.run_cell_n` on CLASSIC5 over the TC11 corridor.
- **9/12** = `T9.replay9(s, TP.CONTROL_CARD, T9.SWEEP_CELLS[-1], lo, hi)` per CLASSIC5 asset. It is anchored
  cross-process: `TP._book_sha` over the TC10 window (hi = 2026-09-21T16:00Z) must equal the full-arm
  `book_sha256` b2276fa4… in `research_outputs/tierc10/registrations/P-TRG-2.scored.json`.

**L-1.7 F-CTRL**
- (a) `run_cell_n(control)` vs `tierc6.run_cell(CARD_V6)` on the TC11 corridor: exactly 0.000e+00 on the 12
  CTRL_COLS, with identical exit reasons and count.
- (b) Cross-process: `TP.journal_frame(live)` vs the filed `research_outputs/tierc10/panel/control_journal.parquet`
  (200 rows, sha fcbf5db0…), on the 12 CTRL_COLS at the file's 6 dp.
  - Every campaign the filed journal closed must match exactly.
  - The ETH `corridor_end` row (entered 2026-09-18T08:00Z) is a continuation: entry, stop and r_dist must match,
    and its exit may differ.
  - Entries after 2026-09-21T16:00Z are listed as new.
- Sabotage: a one-tick stop perturbation must turn (a) RED, and a dropped filed campaign must turn (b) RED.

---------------------------------------------------------------------------------------------------------------
## 2 · Stage R — ranges

**L-R.1 LENSES** — R1 runs {5m, 15m, 1h, 4h, 12h, 1d, 1w} × CLASSIC5, and {1h, 4h, 1d} × the twelve (Tier-E).
- 1d and 1w are derived from native 4h (1w Monday-anchored).
- ATR is `engine.indicators.atr(h, l, c, 14)` on the lens's whole tape. It is recursive, so the value at bar k
  uses only bars up to k.

**L-R.2 SCALE** — "Macro scale self-calibrated per asset per lens to 0.75 confirmed ranges/100 bars".
- **Of record: the calibrated scale**, which supersedes TC10's L2 frozen 3.0 for TC11.
- **The calibration window is the tuning era** (`C.calibrate(tape.head(C.era_cut(tape)))`: the 11-cell grid
  1.5..4.0, the density nearest 0.75/100, ties toward 3.0 then lower). Where the tuning era holds fewer than 400
  bars of that lens, the pick falls back to the whole tape and is labelled IN-SAMPLE everywhere.
- `calibrate`'s `calibrated_in_sample` column is overwritten with the true flag: the tuning pick is in-sample for
  tuning and out-of-sample for holdout.
- **SCALE-IN-SAMPLE.** Every calibrated-scale range read at an instant ≤ the era cut is structurally in-sample.
  The look-ahead is outcome-free, but it is look-ahead.
  - The §0 rows of P-BRK-4H, P-ADD-BRK, P-ADD-SFP and P-TP-RNG say so. Each prints beside its verdict the
    holdout-slice statistic (the only slice with a causal scale) and the frozen-3.0 twin (fully causal).
  - Pick stability is printed per CLASSIC5 asset × {1h, 4h, 12h}: the pick fit on the first half of the tuning
    era vs the whole tuning era. A change is flagged on every row that consumes that lens.
- Printed per asset × lens: the tuning pick, the whole-tape pick, the frozen 3.0, the whole density grid, and
  the 12 pins in key order.

**L-R.3 PINS** — "pins = TC10 sha".
- The port `analytics/rangefinder_census.py` must hash to STEP0_RECORD's `19c5507f…`, and
  `engine/rangefinder.py` to `bbae464f…`.
- The 12 pins must equal `pins_of_record` in key order, and the retest grid sha must be `2135ca66…`.
- Any mismatch is a HALT. The pins block is printed.

**L-R.4 R2 FEASIBILITY** — "PASS/FAIL printed per lens [Q-R3 law]".
- **TC10's [Q-R3] gate unchanged**, including its floor law (a leg under its floor FAILS):
  - the height leg: n_ranges ≥ 30, median(height ÷ toll) ≥ 3.0, share(ratio < 1) ≤ 0.10;
  - AND the edge-fade leg: fade from the outer 20% toward the far boundary, edge_n_ranges ≥ 30 and edge_n ≥ 30,
    median H20 term − toll > 0, within one era.
- **Lens verdict of record = the CLASSIC5 pooled row, HOLDOUT era, calibrated scale, taker toll.**
- **Two words: PASS; FAIL.** An under-floor FAIL prints "FAIL (provisional, n<30)". Any FAIL closes that lens
  for range trading per the contract; provisional FAILs are listed in findings-not-fixed for the operator.
- A taker FAIL with a maker-twin PASS reads "FAIL — maker twin PASSES (the reopening path; needs a toll-model
  change the operator rules)".
- **Disclosure.** TC10's per-era Q-R3 verdicts for 5m, 4h and 1d were seen before this era was chosen (4h
  CLASSIC5 pooled passes only on the holdout, +0.0062 ATR; 1d passes ALL and tuning and fails the holdout). 1h,
  12h and 1w were never measured. The holdout is of record because the scale is tuning-calibrated.
- Every other row is Tier-E, with its word printed as `would_read`: each asset, the ALL and tuning eras, the
  frozen scale, and the charter and maker tolls.
- **F-FEAS** re-derives every lens verdict from its printed columns:
  - height: n_ranges, ratio_median, share_ratio_lt_1, toll;
  - edge: edge_n, edge_n_ranges, edge_median_term_h20, edge_toll_atr.

**L-R.5 NEST VECTOR** — "at every instant of every campaign of every card".
- **Instants:** every bar close of the campaign's own lens from its arm (or its entry, for books without arming)
  through its exit, plus the named events.
  - Close events (arm, entry, harvest, bell, add, exit at a close) are stamped at their close.
  - **Intrabar events (+1R, a stop, a TP fill) are stamped as of the OPEN of their bar**, or at the close of the
    1h child that resolves them. A close-stamped twin is labelled "post-event".
- **Per L in {1h, 4h, 12h, 1d, 1w}, read at the last CLOSED bar of L at or before the instant:**
  - state ∈ {NONE, IN_RANGE, BULL_EXP, BEAR_EXP};
  - %-of-range (unclamped);
  - **signed distance** to the nearest boundary in ATR_L: positive inside the box, negative beyond it, with
    `near_side` beside;
  - boundary age;
  - deviations per side;
  - last flip (polarity, age);
  - coincidence.
- **Coincidence** (per side of L): a LIVE boundary of L within 0.25 × ATR_L of either LIVE boundary of L+1.
  - A twin also admits L+1's live memory lines.
  - The ladder is 1h→4h→12h→1d→1w; 1w's coincidence is NA ("no lens above").
- Out of range, the geometry columns are NaN, while state, flip and deviations carry.
- For the twelve, the 12h and 1w columns are NA.
- **F-NEST-ASOF** holds each (asset, lens) scale at its filed pick. The pick is a pin, never re-fitted on a
  prefix, and the fixture says it does not test the pick.
  - Prefix tapes keep their lens step (`C.LENS_MS` extended in place).
  - The leaked-redraw sabotage (reading `Range.top/.bottom` at t) must FAIL.

**L-R.6 R4 THE TWO TRADES**
- **(a) BREAKOUT = macro death → the first retest that HOLDS.** This is a new scan function.
  - Qualifying touches are those of `C.retest_holds`: the bar meets the band AND the prior close sits beyond it
    on the die side.
  - Touches are taken in bar order within the candidacy window `min(die + 400, next_die − 1, end)`. Each gets
    retest_holds' own test, including a touch inside another touch's pending window. The first "hold" is the
    event, known at touch + hold. A "truncated" verdict ends the scan. Every evaluated touch is a row.
  - Bands tap-89 / tap-127 / tap-200 (EMA of close on L's lens) with the census `RETEST_PINS` (1.0 ATR / 3 bars /
    ttl 400).
  - **The memory-line follows the same law.** The opposite-side touches of the dead range's unexpired memory line
    are scanned in the candidacy window. The first touch with no close through by 1.0 ATR over touch..touch+6 is
    the event, known at touch + 6.
  - **Twins:** TC10's one-shot rule, for the bands and for the engine's memory flip.
  - **F-EQ-SCAN:** the first evaluated row per DIE equals `C.retest_holds` / `BK.band_hold_candidates` exactly on
    every CLASSIC5 lens.
- **(b) SWING-FAILURE** = the machine's `harden` event (a close back inside within 7 bars). Hardens occur only
  on confirmed ranges. A bottom harden is a spring (long), a top harden an upthrust (short).
- **L+1 conditioning** (L+1 as-of at the event's known_at), a whole partition with the contract's three named
  cells marked ★:
  - ★ expansion aligned (BULL_EXP for a long, BEAR_EXP for a short);
  - expansion counter;
  - ★ in-range at its own boundary (coincidence);
  - ★ in-range mid (L+1 pct in [25, 75] and not coincident);
  - in-range other;
  - NONE.
  - **The event's boundary of L** for coincidence: BREAKOUT = the broken side's as-of boundary at die_i − 1;
    SWING-FAILURE = the deviated side's as-of boundary at harden_i − 1 (pre-redraw), with the post-redraw value
    as a Tier-E twin. `Range.top/.bottom` are never read.
- **Outcomes:** `term = sgn·(c[k+H] − c[k])/ATR_L[k]` from the known_at close, H20 and H100 in bars of L,
  censored rather than shortened. Per direction.
  - Statistics are `C.grid_rows`': n, median_term, mean_term, hit_rate, hit_rate_net, toll_atr, and
    NET = median_term − toll_atr.
- **Base rate** — the same statistics anchored at EVERY closed bar k of L for that asset × era, per direction,
  censored the same way, net of the same toll. It is computed (i) unconditionally and (ii) within each L+1 cell of
  the same partition (read from L+1's as-of at close_k; coincidence = the nest flag for L at k). Each event row
  prints beside the base row of its own L+1 cell, with event NET − cell-base NET.
- **Null** = the gaps+order null of record (ruling R10), rebuilt for TC11. It uses the TC11 tuning-era pick
  passed in and the same scan (never `tierc10_null.scale_for` or `compute_cell`), K = 20 draws, with events
  conditioned on the REAL L+1 state at their known_at. It is a description, never a p-value.
- Lenses L ∈ {1h, 4h, 12h, 1d} × CLASSIC5 (per asset and pooled). The twelve are Tier-E at 1h/4h/1d.

**L-R.7 R5 THE CHOP TABLE** — v6 outcomes by 4h state × %-of-range decile, and by 12h state × %-of-range
decile, at entry.
- Deciles: [0,10) … [90,100), plus "<0", "≥100" and not-in-range by state.
- Columns: n, E[net R], P(win), ΣR.
- TC10's five-row table (`control_entry_by_state.parquet`, 4h, frozen 3.0) is reproduced beside it as the anchor.
- Printed first in §0. Tier-E.

---------------------------------------------------------------------------------------------------------------
## 3 · Stage W — early warnings

**L-W.0 THE 1H WALK LAW**
- A 4h bar may be walked on 1h only if its four native 1h children exist on the grid and reproduce the parent's
  high, low and close to REPR_TOL (1e-9 relative, the `LN.be_sequence` law).
- On any other bar, the parent decides STOP and the +1R latch exactly as v6 does. 1h-only events on that bar
  (warn cross, add trigger, relay entry) are taken at the parent's close.
- The bar is counted in a per-book mismatch column.
- **F-WALK-IDENT:** with every rule disabled, the 1h-walk ride reproduces v6 at 0.000e+00 on the 12 CTRL_COLS.

**L-W.1 VISIBILITY** — "only 1h bars CLOSED before the 4h bar closes".
- A 1h bar is visible at a 4h decision instant iff its close ≤ the 4h close.
- F-WARN-ASOF's sabotage reads a 1h bar with close > the 4h close, and it must FAIL.

**L-W.2 EVENTS** — 1h EMA-of-close crosses 9/12, 12/26 and 12/89 (engine EMA), each known at the 1h close
where the fast line changes side. With/against is relative to the campaign direction.

**L-W.3 WINDOWS AND +1R ON THE 1H PATH**
- **+1R latch** = the first 1h child after the entry close whose high (long) or low (short) reaches entry ± R.
  On a mismatched bar, the parent decides it (L-W.0).
- **The 1h-resolved exit.**
  - A stop exit (initial or trailed) happens at the first 1h child of the 4h exit bar whose low ≤ the stop in
    force (high ≥ for a short). It HALTs if no child touches the stop, unless the bar is a mismatch bar.
  - A bell or corridor_end exit happens at its 4h close.
- **IN-TRADE events** are those with 1h close > the entry close and strictly before the 1h-resolved exit. A cross
  on the stop child does not count.
- **PRE-ENTRY events** are those with arm close < cross close ≤ entry close. They feed only the W2 pre-entry
  tables, never a post-entry cohort, never the P-WARN-1 condition.
- **Before +1R** = an in-trade cross with 1h index < the latch index (with no latch: any in-trade cross).
- **After +1R** = an in-trade cross with 1h index ≥ the latch index. The touch is intrabar, and the cross is
  known only at the close.

**L-W.4 W2 COMPARISON GROUPS** — each cohort is compared with its **at-risk set**, with the complement within
that set printed beside.
- "Before +1R" and pre-entry cohorts are compared with the whole v6 book.
- "After +1R" cohorts are compared with the campaigns that reached +1R.
- "9/12 re-cross after entry" is compared with campaigns still open 1h after entry.
- Every post-entry cohort also prints its forward leg, E[final net R − R marked at the event's 1h close], i.e.
  hold vs exit at the event.
- **P-WARN-1 condition** (on the full-corridor v6 book the rule is scored on):
  - Cohort = campaigns with an **in-trade counter 12/89 cross before the +1R latch**.
  - Δ = mean(cohort) − mean(whole book), by `T5.cluster_boot_diff`, seed 20260924. MET iff the cluster-90% hi
    < 0.
  - The condition block is the only Tier-E place a CI is printed.
  - Fixture: the condition-cohort keys == the keys whose rule-book exit_reason is the warn exit, plus the keys
    whose first qualifying cross fell on a mismatch bar (listed).
- **Pre-entry tables:** for each event class (counter-12/89, counter-12/26, with-trend 9/12, with-trend 12/26)
  in (arm close, entry close]: n, P(win) and E[net R] vs the whole book, complement beside. Whole, Tier-E.

**L-W.5 THE WARN RULE** — "exit at the 1h counter-12/89 close while pre-+1R".
- Walk each v6 campaign's 1h children (L-W.0). On each child, in order:
  1. STOP (adverse-first);
  2. the +1R latch;
  3. at the child's close, if pre-+1R and a counter 12/89 cross closed: exit at that 1h close.
- At each 4h close, v6's BELL, HARVEST and TRAIL apply unchanged.
- The set is kept, so the ruler is paired, under the identity law (L-1.5).
- If the condition is NOT MET, the rule book is printed only as a collared Tier-E row with no verdict word.

**L-W.6 RELAY EVIDENCE** — for every v6 window: the first 1h with-trend 12/26 cross with arm close < close <
the 4h trigger close. Printed: the share of windows where it precedes the trigger, and the lead in 1h and 4h bars
(distribution, whole).

---------------------------------------------------------------------------------------------------------------
## 4 · Stage G — admission gates

**L-G.1 TIDE AGE** = TC10's P-AGE-1 function: `tierc7_lab_regime.tide_streak`, the run length of
sign(e89 − e316) on 4h counted from warm-up bar 316, **read at the campaign's entry bar**.
- **Trailing-quantile (of record):** quartile edges of that streak over CLASSIC5 4h bars pooled with open ≤ the
  entry bar (`tierc9._trailing_edges`, ≥ 30 bars). **OLD = streak ≥ the trailing 75th-percentile edge (B4).**
  P-AGE-1 refuses OLD.
- **Absolute (shadow):** refuse streak > 206, exactly as written. The shadow row prints that 206 is the
  whole-corridor median edge, not the OLD edge, and that it reads the corridor ahead.
- **Disclosure:** `tierc9.tide_streak_age` (arm bar, three-state tide) is the other "tide age" on disk.
- **F-DEF** computes both definitions. It must FAIL if the absolute cut is swapped for the trailing one, or the
  arm-bar function for the entry-bar one.
- **pre_seen:** the scored cohort IS TC10's `P_AGE_1_TIDE_YOUTH` B4 (the same function, edges and 200 campaigns,
  anchored by F-CTRL(b)). The point was known before filing: gated n 141, +0.4567 vs +0.2087, Δ ≈ +0.2480 R. New
  information is the interval and the campaigns entered after 2026-09-21T16:00Z (listed).

**L-G.2 WINDOW AGE** — lag = entry_i − arm_i (4h bars). P-WIN-1 refuses lag ≥ 16; the shadow cut refuses 7–15.
- **selection_hazard:** the direction was informed by TC6V L-LAG deciles on the same corridor (lag-0 +0.4149;
  56-bar decile −0.5796). P-LAG-1 on the same question was NOT MET (Δ +0.0616 [−0.7819, +0.9566]). The 16 cut has
  no on-disk provenance, and v6 lag 7–15 holds 4/200, so ≥16 ≈ ≥7.

**L-G.3 TIER-E STRUCTURE DISTANCE** — `r_over_atr = r_dist / ATR14_4h(entry)`.
- Admission: refuse > 2.2.
- **Priority:** within one window, when the window's first 12/26 trigger has r_over_atr > 2.2, pass it and take
  that window's next same-direction 12/26 trigger with r_over_atr ≤ 2.2 (before the window closes, asset flat).
  This is its own Tier-E book, with a count of substituted entries.
- The same-close cross-asset collision count is kept as a disclosure; it cannot bind under one position per
  asset.
- The three gates are crossed 2 × 2 × 2, n and E[net R] per cell, whole.

---------------------------------------------------------------------------------------------------------------
## 5 · Stage T — triggers and lanes

**L-T.1 P-BRK-4H**
- 4h macro death (calibrated 4h scale) → the **first retest that HOLDS** on **tap-89** (EMA-89 of 4h close,
  1.0 ATR / 3 bars; L-R.6).
- Entry at the touch + hold close.
- Stop: `BK.brk_stop`, beyond the retest extreme (touch..entry), offset 0.5 ATR(4h), railed so R ≥ 1.0 ATR(4h).
- Tide aligned at the entry bar's close.
- `BK.ride_leg_l(ribbon=None)` (pure v6, no 12/25 bell). One position per asset.
- Vs zero, CLASSIC5, full corridor.
- **Tier-E:** the 17-asset view; the memory-line first-that-holds lane (engine one-shot flip as its twin); the
  frozen-3.0 twin; the one-shot first-touch twin; tuning and holdout slices.
- **selection_hazard:** the best of 7,920 TC10 census cells (4h retest-hold-tap89, CLASSIC5 NET H20 +0.681 ALL
  n 236 / +0.706 holdout n 88; UNSEEN12 +0.064 / +0.272). Every era and asset was seen. The scored event
  (first-HOLD scan, tuning-calibrated scale) differs from the one-shot, frozen-3.0 row that was selected.

**L-T.2 P-RELAY-1** — "4h window open+armed; ENTRY on the 1h 9/12 with-trend close inside it".
- **ARMED** is the estate's posture word (`scripts/posture_engine.py:243-252`): the window is open, no counter
  12/89 and no 89/316-against since, and no in-window 12/26 trigger yet.
- **Entry:** the first 1h close strictly after the v6 arm close AND strictly before the earliest of:
  - (i) that window's v6 4h 12/26 trigger close;
  - (ii) the window-close instant (the counter 4h 12/89);
  - (iii) a 4h 89/316 cross against the window.

  On that 1h bar, EMA9 crosses EMA12 in the trade direction. A 1h close at the 4h trigger instant is not a relay.
  There is one relay per window and one position per asset.
- **Misses:** windows whose 4h trigger closes first (every lag-0 window included), or that close unrelayed.
  They go in the **miss column** with what v6 did in them.
- **Stop:** `struct_stop_4h`, with pivots confirmed and ATR(4h) as of the last CLOSED 4h bar at the entry
  instant, railed at 1.0 ATR(4h). R is on 4h.
- **The ride:**
  - The entry 4h bar J's post-entry 1h children are walked for STOP and the +1R latch (L-W.0).
  - Then J's own close runs v6's close slot:
    - BELL on w_dn[J] or b_dn[J] (mirrored for a short) exits at close[J];
    - HARVEST, armed per close[J−1], with the touch judged on post-entry children only;
    - TRAIL, armed iff the latch fired.
  - The 4h ride continues from J+1, with the stop, reached_1r, trail_armed, h_armed, mfe, mae and mae_to_1r
    carried. This is a new ride with an injectable initial state.
- **F-RELAY-RIDE:** a relay whose entry equals a 4h close reproduces `_ride_leg9` at 0.000e+00 on CTRL_COLS.
- Two-sample vs the v6 book. The rival reading (relays allowed after the trigger) is a Tier-E "late-relay" twin.

**L-T.3 F-RELAY** — on EVERY relay, relay close < that window's v6 4h trigger close (when the window triggered).
A planted post-trigger relay must FAIL, and 3 relays are hand-walked.

**L-T.6 FORWARD LEDGER**
- It opens at **2026-09-21T16:00:00Z** (TC10's pin), after which both frozen books are unseen.
- `--refresh` re-rides each frozen book over the whole tape (bar 0 to the refresh pin), on the F-CTRL code path.
  It admits only campaigns whose entry close is > the opening.
- A campaign is appended **exactly once, when closed** (exit_reason ≠ corridor_end). One open at the refresh pin
  is listed OPEN, not appended, and not counted. A refresh whose re-ride changes any appended row HALTs.
- n is per book; each book stays unscored until its own n ≥ 30.
- `research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` is hash-chained.
- Every v6 row carries the P-AGE-1 trailing band and the P-WIN-1 lag as stamp columns, so both gates build an
  out-of-sample record.

---------------------------------------------------------------------------------------------------------------
## 6 · Stage S — the scalper

**L-S.1 PRECONDITION** — Stage S runs only if the R2 lens verdict of record at 1h is PASS. Otherwise it prints
"CLOSED BY R2 (1h: <verdict>)" and stops. P-SCALP-2's §0 row reads that verdict, with no number and no slot spent.
- The rival (gating on the tuning-era R2) was rejected; see §10.

**L-S.2 FORM** (only if 1h PASSES)
- **Live range:** a CONFIRMED 1h macro range (calibrated 1h scale) in range as of the last closed 1h bar at or
  before the 5m close, **and that 1h bar's close lies inside the as-of box** (no open breach). Crosses during a
  pending breach are refused and counted.
- **Lower third:** 0 ≤ pct < 33.33 at the 5m close against the as-of box (upper third: 66.67 < pct ≤ 100).
- **Entry:** a 5m EMA12/EMA89 cross up (down) closes; enter at that 5m close.
- **Target:** far boundary − 0.25 × ATR_1h (+ for shorts), with the box and ATR frozen at entry. The entry is
  refused (and counted) if (target − entry)·d ≤ 10 bps·entry.
- **Stop:** beyond the nearest confirmed 5m (5,5) pivot within 200 bars (`struct_stop_4h` on 5m arrays),
  offset 0.5 ATR_5m, railed so R ≥ 1.0 ATR_5m.
- **Invalidation:** the first 1h CLOSE beyond the entry-side boundary known after entry. Exit at that 1h close
  (the coincident 5m close), taker.
- **Within a 5m bar:** STOP → TARGET → invalidation at the close.
- No trail, no tide, one position per asset.
- **Twins:** taker (record); maker "fill assumed"; maker "fill conditioned" (L-1.2).
- **Printed per row:** the distribution of (target − entry)/(entry − stop).
- **Regime gate printed:**
  - 5m ATR tercile: trailing 2,000-bar quantiles over a window ending at the entry bar inclusive;
  - 1h boundary-age tercile: trailing quantiles over that asset's 1h in-range bars with close ≤ the entry
    instant, ≥ 30 bars, otherwise unbanded.

---------------------------------------------------------------------------------------------------------------
## 7 · Stage A — adds

**L-A.1 COMMON**
- These apply to v6 campaigns (4h). There are at most 2 adds, each a 0.5-unit tranche, entered at the 1h close
  of the triggering event.
- The event must be IN-TRADE (L-W.3) and **after the +1R latch** (an event on the latch child counts as after).
- Adds are booked by `tierc7._account_chain`:
  - `Add.i` = the 4h bar containing the add's 1h close, so funding runs from the next 4h open;
  - size 0.5;
  - each add exits at the campaign's final exit price and is never harvested.
- The D12 funding ceiling applies once to the campaign's total funding including tranches. The campaign's net R
  is `_account_chain`'s net_r, with add_r printed beside.
- The v6 leg is identical by the identity law, so Δ = the tranches' contribution.
- **Printed per add book:** adds with (add_px − entry_px)·d < 0 (below entry), and adds after the harvest fired
  or inside its 4h bar. Tier-E twins refusing each class are printed beside. The scored arm is unchanged.

**L-A.2 P-ADD-BRK** — a 1h macro range death (calibrated 1h scale) whose breakout side is the trade's direction
(top for a long), known at its 1h close.

**L-A.3 P-ADD-SFP** — "a swing-failure CONFIRMS at the trend-side boundary of the 1h range (the deviation back
into range in the trade's favour)".
- The parenthesis governs: for a long, a **spring at the 1h range's bottom** (a harden, known at its 1h close);
  for a short, an upthrust at the top.
- "Trend-side boundary" is read as the boundary the trend defends (support in an uptrend).

---------------------------------------------------------------------------------------------------------------
## 8 · Stage H — take-profit

**L-H.1 P-TP-RNG** — v6's harvest law (50% at the opposing 89/316 band) is kept.
- **At each 4h bar j after entry,** read the 12h as-of state at j's OPEN (the last 12h bar closed ≤ open_j). If
  it is IN_RANGE, the level is top − 0.25 × ATR_12h for a long (bot + 0.25 × ATR_12h for a short).
- **A resting limit for the remainder is live during bar j iff all of:**
  - (i) the prior 4h close is on the near side of the level;
  - (ii) the level is beyond the entry in the trade's favour by more than the round-trip taker fee:
    (level − entry_px)·d > 10 bps·entry_px.
- **Fill:** if h[j] ≥ level, at max(level, o[j]) for a long; if l[j] ≤ level, at min(level, o[j]) for a short.
- If the prior close is already beyond the level, no order rests (re-arm on a close back inside).
- EXPANSION or NONE means no TP, and the trail runs.
- **"The remainder" — reading of record:** the position still open when the TP fills (1.0 if the band harvest
  has not fired, 0.5 after). The contract makes the harvest a kept law, not a precondition.
- **Rival (Tier-E twin "tp-post-harvest"):** the TP rests only after the v6 harvest has fired, for the 0.5
  runner.
- **Also printed:** the unguarded twin (without (ii)), and counts of the orders the guard withheld.
- **Same-bar order:** STOP (adverse-first) → TP → at the close BELL → HARVEST → TRAIL.
- Paired vs v6. The row prints the D15 tail ratio (`T5.d15`) and names the wall-exit lesson (P-WALL-1, Δ −0.0331,
  tail 0.9329) as the risk.

---------------------------------------------------------------------------------------------------------------
## 9 · Fixtures and close

**L-F.1 F-DET** = TC10 variant (i): two subprocess builds with PYTHONHASHSEED "1" and "20260924", byte-equal on
the file set, the bytes and the parquet content shas.

**L-F.2 IMPORT-CLOSURE**
- The v6 decision closure (tierc2_rules … tierc9) stays range-blind.
- The DECISION set = every tierc11 module except `tierc11_nest` and the runners. It must not import
  tierc10_census, tierc10_stamps, tierc10_null, analytics.rangefinder_census or engine.rangefinder, and must not
  read `Range.top/.bottom`.
- An AST scan plus a fresh-interpreter scan, using a substring match so that rangefinder_* is caught, must FAIL
  on a planted import.

**L-F.3 WORKTREE ATTESTATION** is a real check.
- Each adversarial review runs in a detached worktree at the commit under review.
- The attestation records the path, HEAD (which must equal the reviewed sha), and `git status --porcelain`
  before and after (which must be empty). It FAILS on a mismatch or any modification.
- TC10 records are read by absolute main-tree path.

**L-F.4 CLOSE ORDER** — TC10's `close_acts.sh` is still the operator's to run.
- TC11 stages its ledger append at `research_outputs/tierc11/LEDGER_APOLLO_APPEND.md` and prepares
  `research_outputs/tierc11/close/close_acts.sh`.
- That script refuses to run until TC10's report exists in exchange/reports and TC10's block is in LEDGER_APOLLO,
  so the ledger keeps tier order.
- **No push without the operator's word.** "STATE push" = state the push result plainly.

---------------------------------------------------------------------------------------------------------------
## 10 · Review disposition (2026-09-25; five lenses, 51 findings)

The raw findings are filed at `research_outputs/tierc11/review/LEANS_REVIEW_2026-09-25.json`.

**ACCEPTED, merged above:**

| findings | where |
|---|---|
| fidelity 0, causality 0, statistics 4, trading 2 | L-W.3, the in-trade window |
| fidelity 1, 2, 10; trading 1 | L-H.1 |
| fidelity 3, statistics 11 | L-R.4, two words plus the disclosure |
| fidelity 4, buildability 5 | L-R.6, the scan and the memory line |
| fidelity 5 | L-W.4, pre-entry tables |
| fidelity 6, trading 3, 5 | L-S.2 |
| fidelity 7, buildability 10 | F-FEAS |
| fidelity 8, statistics 6 | the base rate |
| fidelity 9 | REGS contexts |
| causality 1, buildability 0, trading 0, 4 | L-T.2 |
| causality 2 | SCALE-IN-SAMPLE |
| causality 4 | L-T.6 |
| causality 5 | intrabar stamps |
| causality 6 | regime terciles |
| causality 7 | maker fill-conditioned |
| statistics 0, 1 | pre_seen / selection_hazard labels |
| statistics 2, 3; buildability 3 | L-1.4, the own scorer and collars |
| statistics 5 | at-risk sets |
| statistics 8, 10 | the paired premise and the identity law |
| statistics 9 | gate ΣR |
| buildability 1, 2 | L-0.3 |
| buildability 4 | L-W.0 |
| buildability 6 | F-NEST-ASOF pin |
| buildability 7 | adds via `_account_chain` |
| buildability 8 | journal_frame 6 dp; absolute TC10 paths; RETEST_PINS assert |
| buildability 9 | era by close |
| buildability 11 | the event boundary for coincidence |
| trading 6 | add disclosures |
| trading 7 | the priority book |

**REJECTED — causality 3** (gate P-SCALP-2 on the TUNING-era R2 instead of the holdout lens verdict).
- The claim was that gating on the holdout edge-fade and then scoring on the holdout inflates the
  false-positive rate. It does not, unconditionally: under the null, P(gate passes ∧ p ≤ bar) ≤ P(p ≤ bar) ≤ bar,
  so a precondition can only remove chances to reject.
- Moving the gate to the tuning era would also give the 1h lens two verdicts, one opening Stage S and another
  governing closure.
- One lens verdict of record (holdout) governs both. The §0 row prints the tuning-era R2 word beside it as
  Tier-E, so a reader can see if they disagree.
