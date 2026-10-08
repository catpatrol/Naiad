# U6 · RANGE-TRADE AND SCALPER MACHINERY (TC12 STAGES R AND S) — SCOUT MAP

Scout: read-only. Contract read: `scratchpad/tc12/2026-10-08_TC12_APOLLO.md`, sha256
`861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` (137 lines; identical sha to
`/Users/luis/Naiad/exchange/queue/2026-10-08_TC12_APOLLO.md`, filed at main `28e006b`).
Trees: MAIN `/Users/luis/Naiad` (branch `v12-v1-census`; HEAD was `a399b47` when I started and `28e006b`
"tierc12(STEP Q)" when I finished — the orchestrator committed meanwhile). X `/Users/luis/Naiad/.claude/worktrees/tierc11x`
(branch `tierc11x`, HEAD `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11` == `research_outputs/tierc11x/close/CERTIFIED_TIP`).
Abbreviations: `M/` = main tree, `X/` = X worktree, `XR/` = `X/research_outputs/tierc11x`, `MR/` = `M/research_outputs/tierc11`.
Every number below was read from the cited file in this session. Nothing here is an outcome of a TC12 rule: I computed
no P-SFP-VA-1 / P-SCALP-3 statistic. Two small price-grid inspections (§1.9) are unconditional bar facts.

---------------------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.0 Where the code lives (the single most load-bearing structural fact)
- MAIN holds `scripts/tierc11_*.py` and NO `tc11x_*.py` (0 files). X holds `scripts/tc11x_*.py` (33 files) and only the
  three TC11-D scripts of `tierc11_*` (merge-base `e97ad73`, "tierc11(TC11-D): the corridor"). X is not merged.
  `M/research_outputs/` has no `tierc11x/` and no `tierc12/`.
- Therefore a TC12 module built in MAIN can `import tierc11_ride` etc. but CANNOT import `tc11x_sfp`, `tc11x_va`,
  `tc11x_ranges`, `tc11x_pct` without reaching into the certified X worktree. X's own precedent for this situation is
  VENDOR-BY-COPY with the sha in the filename: `XR/vendor/tierc11_env@086d66da.py` (+ `README.md`).
- Lineage files are byte-identical in both trees (shasum compared): `scripts/tierc10_brk.py`, `tierc10_null.py`,
  `tierc10_census.py`, `tierc10_lanes.py`, `tierc5_rules.py`, `engine/indicators.py`, `engine/rangefinder.py`,
  `analytics/rangefinder_census.py`.

### 1.1 How a multi-timeframe ride is simulated today — three engines, three clocks
| engine | file:lines | clock walked | what it is |
|---|---|---|---|
| `ride11` (+ `relay11`) | `M/scripts/tierc11_ride.py:493-736`, `:800-919` | **4h parent bars; 1h children only to RESOLVE** | card v6 (trail/bell/harvest) with hooks walk/warn/tp. This is "the 1h-walk ride". |
| `tc11x_sfp.walk` / `bar_step` | `X/scripts/tc11x_sfp.py:649-752`, `:571-601` | **the trade's own lens bar (1h book, 4h cell)**; 5m children only on the maker fill bar and in one twin | X2's SFP range trade: stop / T1 half / T2 / time stop. |
| `BK.ride_leg_l` | `M/scripts/tierc10_brk.py:1093-1209` | **any lens frame, incl. 5m** (`LENSES = ("5m","4h","1d")` :138; lane `brk-s1` → 5m :156) | v6 management transcribed onto a lens (TC10 P-BRK-S1). NOT a target/stop range trade. |

**No existing ride walks a target/stop/time-stop range trade wholly on the 5m clock.** The only 5m walks are (i)
`BK.ride_leg_l` on a 5m frame (v6 management), (ii) X2's fill-bar walk on the 5m children of ONE lens bar
(`tc11x_sfp.py:669-712`), (iii) X2's `child_walk` twin on ambiguous bars (`:626-646`), (iv) `LN.be_sequence`
(`M/scripts/tierc10_lanes.py:296`). P-SCALP-2's 5m ride was never written (§1.3).

**(a) `tierc11_ride.ride11` — the 1h-walk ride** (`M/scripts/tierc11_ride.py`, sha256 `65eb880f…915d`)
- Signature: `ride11(sym, card, roles, d, ti, entry_px, stop0, r_dist, hi_i, *, walk=None, warn=None, tp=None,
  state=None, j0=None, exit_order=EXIT_ORDER, child_order=CHILD_ORDER, ctx=None) -> dict` (:493-495).
- Bar-walk order per 4h bar j (docstring :28-31, code :548-726): top of bar = +1R latch, trail arming, harvest touch;
  intrabar `EXIT_ORDER = ("stop", "warn", "tp", "bell")` (:204), adverse-first; then the close slot BELL → HARVEST → TRAIL.
  `winner = next(x for x in exit_order if hits[x])` (:640).
- Intrabar ambiguity (stop and target in one bar): **STOP wins**; a TP fill on a stop bar is counted
  `fill_blocked_by_stop` (:642-648). Stop fills AT the stop (`exit_px = stop`, :643).
- 1h children: `walk_of(sym)` (:329-352) marks a 4h bar WALKABLE iff 4 native 1h children on the grid reproduce the parent's
  high/low/close to `REPR_TOL = 1e-9` relative (`LN.REPR_TOL`, `M/scripts/tierc10_lanes.py:276`; `_same_px` :279-281);
  `child_mismatch` :308-326. Per child `CHILD_ORDER = ("stop", "latch", "warn")` (:205, `walk_children` :355-399).
  A mismatch bar is decided by the parent and counted (`n_walk_mismatch`). "The walk resolves WHEN, never WHAT" (:61-63).
- TP hook (L-H.1; :613-633): `TPLevels(level_long, level_short, mode, guard_bps)` (:426-432), per 4h bar; live iff level
  finite, prior 4h close on the NEAR side, and `(level − entry)·d > TP_GUARD_BPS/1e4·entry` with
  `TP_GUARD_BPS = 2.0 * RC.FEE_BPS_SIDE` (:208). **Fill model = TOUCH**: `h[j] >= lvl` fills at `max(lvl, o[j])` (:630-632).
- Partial exits: only the v6 band harvest (`harv`, booked at `card.harvest_frac`); no T1/T2.
- Time stops: **refused** — `scope(card)` HALTs unless `card.time_stop_bars is None` (:239). The lineage clock exists in
  `M/scripts/tierc7.py:209-211` (`(j − ti) >= card.time_stop_bars → c[j], "time_stop"`).
- Invalidation exits: none in `ride11` (bell is the only close-event exit).
- 1h EMA crosses: `cross_1h(h1, fast, slow)` = `ind.crossover/crossunder(ind.ema(h1.c, fast), ind.ema(h1.c, slow))` (:415-418);
  `warn_of(walk, fast=12, slow=89)` (:421-423). No warm floor applied there.
- Fixtures: `MR/ride/FIXTURES_RIDE.txt` (sha `578d6399…3e91`) "9 GREEN, 0 RED": F-WALK-IDENT, F-RELAY-RIDE, F-EXIT1H,
  F-MISMATCH-1H, F-WARN-BOOK, F-ORDER, F-ADD-ACCT, F-CLOSURE-RIDE, F-DET.

**(b) X2's range-trade walk** (`X/scripts/tc11x_sfp.py`, sha256 `79ba35f4…0f95`) — the template for P-SFP-VA-1
- `bar_step(d, o, hh, ll, stop, t1, t2, strict, gap_sym) -> (t1_px | None, (exit_px, reason) | None, info)` (:571-601).
  Order: **0 the OPEN decides first** (open at/beyond the stop → whole position at the stop; open at/beyond a target → that
  target fills at the open) → **1 STOP adverse-first, fills AT the stop** → **2 T1 (half) at `max(T1, o)`** → **3 T2 (remainder),
  same bar if reached**. A bar touching the stop and a target with neither decided at the open is a stop; counted
  `both_touch` (:592-595). Reading: `XR/LEANS_X.md:1292-1315` (LX-X2.10).
- `_hit(d, px, level, strict)` (:558-560): record `strict=False` = TOUCH (≥); maker-conditioned `strict=True` = THROUGH (>).
  `_fill` (:563-568): `max(level, open)` long / `min` short (TC11 L-H.1's law); symmetric-gap twin fills at the level.
- `walk(ctx, g, ev, law, T, cnt) -> dict` (:649-752): from bar `entry_i + 1`; **time stop at the CLOSE of bar `entry_i + T`**
  (`tend = ti + int(T)` :657; `if j == tend: exit_ = (j, c[j], "time_stop")` :738-740); corridor end marks OPEN at `c[hi]`
  (:743-747). No stop move after T1 (breakeven is a twin, :714). Range death is not an exit (twin `death_exit`, :734-737).
- Half off: `Q = float(CARD.harvest_frac)` (:126) with `CARD = TP.CONTROL_CARD` (:125); `HARVEST_FRACTION` value 0.5 at
  `M/scripts/tierc4_rules.py:163-164`.
- One position per asset: `blocks(cur, b) = cur["entry_i"] < b <= cur["exit_i"]` (:870-874; LX-X2.9, `LEANS_X.md:1273-1290`).
- Geometry (`geometry` :483-522): entry `e = c[bar]`; `ext` = episode extreme `min(l[breach_i..bar])` long / `max(h[…])`
  short (:491-494); `st = BK.brk_stop(d, ext, a, e, atr)` (:496); `T1 = mid_pre` (as-of view at bar − 1); `T2 = far − d ·
  T2_ATR_OFF · atr` with `T2_ATR_OFF = 0.25` (:122); refusal iff T1 or T2 within `REFUSAL_BPS = 10.0` bps of entry (:123, :503-513),
  targets inverted, or no stop.
- Stop of record: `BK.brk_stop(direction, retest_extreme, touch_i, entry_px, atr_sig, rail_atr=MIN_STOP_ATR)`
  (`M/scripts/tierc10_brk.py:1366-1385`) → `RC.spring_stop` (`M/scripts/tierc5_rules.py:481-502`):
  long `stop = min(ext − STOP_BUF_ATR·ATR, entry − rail·ATR)`, short mirrored; `r_dist = |entry − stop|`;
  `rail_binding = rail_dist > pivot_dist`. `STOP_BUF_ATR = 0.5` (`M/scripts/tierc2_rules.py:103-104`),
  `MIN_STOP_ATR = 1.0` (`M/scripts/tierc3_rules.py:98-99`).
- Twin set built (`TWINS` :173-175): maker_assumed, maker_conditioned, maker_within_hour, haircut, drop_open,
  post_redraw_t1, t1_collapse, live_far_t2, breakeven_after_t1, range_death_exit, b1_traverse, frozen3_0,
  frozen3_0_trailing_t, wick_only, symmetric_gap, child5m_sequencing, reversal, kin_uncovered.

### 1.2 Per-trade schema of X2 and how R is computed with split targets
Files: `XR/sfp/X2_trades_1h.parquet` (sha `4e3b5f4f…7eac`, 2,408 rows × 96 cols, key `["asset","entry_ms"]`),
`XR/sfp/X2_trades_4h.parquet` (sha `552e7582…3bef`, 588 × 91), `XR/sfp/X2_twins.parquet` (sha `f2abf81d…8c25`, 49,898 × 90,
key `["lens","book","asset","entry_ms"]`), `XR/sfp/X2_refusals.parquet` (sha `81b7fa6c…534d`, 6,103 × 30),
`XR/sfp/X2_grid.parquet` (sha `4e75539e…d7e8`, 56 cells), `XR/sfp/build_manifest.json` (sha `6f786d84…3835`).
Trade columns (dtype), `X2_trades_1h`:
`lens book asset(object) entry_ms entry_i entry_close_ms(int64) entry_close_iso entry_close_month era direction(object)
d(int64) side(object) rid breach_i bars_out(int64) event_kind scale_kind(object) scale_mult(float64) pick_window(object)
pick_stability_changed(boolean) entry_px ext atr stop_px pivot_stop_px r_dist(float64) rail_binding(bool) T1(float64)
t1_collapsed(bool) T2 far top_pre bot_pre top_post bot_post t1_r t2_r r_atr tenbps_r(float64) T time_stop_i(int64)
harvest_i(Int64) harvest_px(float64) exit_i exit_bar_open_ms(int64) exit_px(float64) exit_reason(object) open_at_pin(bool)
bars_held fund_entry_i(int64) gap_stop gap_t1 gap_t2(bool) both_touch_bars child_seq_bars(int64) fill_repr_ok(boolean)
fillchild_target_withheld(bool) gross_r taker_fee_r funding_r funding_r_uncapped(float64) funding_ceiling_bound(bool)
n1 n2 taker_net_r maker_fee_r maker_net_r stop_leg_slip_haircut_net_r haircut_net_r slip_bps_side(float64) slip_tier(object)
fee_r net_r harvest_r(float64) funding_stamps(int64) kin_covered(bool)` + collar (`tier selection_not_a_result gates
would_read_ci_only m_looks_this_table m_note registered_as pointer scale_in_sample r2_mirror_1h r2_label`) + nine as-of stamps
(`as_of_last_closed_4h as_of_panel_start as_of_span_days warranty as_of_lens as_of_last_closed_bar as_of_panel as_of_n_assets
as_of_substrate`). `X2_trades_4h` lacks `kin_covered registered_as pointer scale_in_sample r2_mirror_1h r2_label`, adds `lens_label`.
Filed facts (parquet): 1h record n 2,408, Σ net_r −307.86011, mean −0.127849, exits {time_stop 1160, stop 1021, T2 227},
T = 13; 4h record n 588, Σ −9.726132, mean −0.016541, exits {time_stop 297, stop 244, T2 47}, T = 13.
Maker twins (X2_grid): `1h|maker_assumed` n 2408 mean −0.110379; `1h|maker_conditioned` n 2321 mean −0.115177 (miss 93);
`4h|maker_assumed` n 588 mean −0.007745; `4h|maker_conditioned` n 547 mean −0.011297 (miss 44); `4h|haircut` mean −0.034021.

R with split targets = `BK.account_l(lf, card, d, r_dist, leg) -> dict` (`M/scripts/tierc10_brk.py:1270-1326`):
- `leg = {"entry_i","exit_i","exit_px","entry_px","harvest": None | (hj, hpx, unit_r)}` — a two-target trade maps to ONE leg
  with `harvest = (T1_i, T1_px, (T1_px − e)·d/R)` and exit = T2 / stop / time stop (`tc11x_sfp.py:771-773`; LX-X2.11
  `LEANS_X.md:1317-1353`).
- harvested: `g1 = q·(hpx − e)·d`, `fe1 = bps·q·(e + hpx)`, `g2 = (1−q)·(xpx − e)·d`, `fe2 = bps·(1−q)·(e + xpx)`;
  `n1 = (g1 − fe1 − u1)/R`, `n2 = (g2 − fe2 − u2)/R`, asserted `n1 + n2 == net` to 1e-9 (:1301-1317).
  Not harvested: `g = (xpx − e)·d`, `fe = bps·(e + xpx)`. `bps = FEE_BPS_SIDE/10_000` — ONE rate, the taker 5.0
  (`M/scripts/tierc2_rules.py:87-88`, :122). `net_r = gross_r − fee_r − funding_r` (:1322-1326).
- Returns `gross_r, fee_r, funding_r, funding_r_uncapped, funding_ceiling_bound, net_r, n1, n2, add_r,
  harvest_ride_would_have_r, funding_census`.

### 1.3 P-SCALP-2 — design, precondition text, why CLOSED BY R2, and what was never written
- Registration: `MR/registrations/REGISTRATIONS.json` (sha `648834bf…f1ee`) seq 6, payload sha
  `c4e7ea0064bf0355804f311b8a2c91af1178de0ac9e705a417a1cc09b90bd250`, `text_sha256 e55707eb…5b9c`, prior 30, family m 9,
  bar 0.011111, seed 20260924. Registry pin `MR/registrations/REGISTRY_PIN.json` (sha `ea77921a…748f`), head `6772568b…c8f9`.
- `text_of_record`: " P-SCALP-2 [30%] vs zero, five assets, holdout era, taker; the maker twin and the 17-asset view Tier-E."
- `operative_spec.precondition` (verbatim): "R2 lens verdict of record at 1h (CLASSIC5 pooled, holdout, calibrated, taker) ==
  PASS; otherwise CLOSED BY R2, not scored, no slot spent [L-S.1]".
- L-S.1 frozen text (`MR/LEANS.md:444-446`; typed again at `M/scripts/tierc11_stage_s.py:268-270`): "Stage S runs only if the
  R2 lens verdict of record at 1h is PASS. Otherwise it prints "CLOSED BY R2 (1h: <verdict>)" and stops. P-SCALP-2's §0 row
  reads that verdict, with no number and no slot spent."
- `operative_spec.scored_arm` (verbatim): "live CONFIRMED 1h range (calibrated 1h scale) whose last closed 1h bar closed inside
  the as-of box; 5m close in its lower (upper) third; 5m EMA12/EMA89 cross up (down) -> entry at the 5m close; target far
  boundary -/+ 0.25 ATR_1h (frozen at entry; entry refused if the target is not beyond entry by > 10 bps); stop beyond the 5m
  (5,5) pivot, offset 0.5 ATR_5m, railed 1.0 ATR_5m; invalidation exit at the first 1h close beyond the entry-side boundary;
  within a 5m bar STOP -> TARGET -> invalidation; no trail; no tide; taker toll [L-S.2]". L-S.2 full form `MR/LEANS.md:448-467`.
- Why closed: `MR/stage_r/R2_LENS_VERDICTS.json` (sha `82cc3ec6…3087`) `lenses["1h"]`: verdict "FAIL", n_ranges 816,
  ratio_median 46.2355442, edge_n 12044, edge_n_ranges 771, `edge_median_term_h20` 0.0, `edge_toll_atr` 0.16760525,
  `edge_net_h20` −0.16760525, `toll_bps_rt` 10.0, `maker_twin` "FAIL", `charter_twin` "FAIL". The edge-fade leg fails
  (`edge_net_h20 > 0` required). All seven pivot lenses FAIL (1w "FAIL (provisional, n<30)").
- Status record: `MR/regbooks/P-SCALP-2/STATUS.json` (sha `5457ea6a…3eda`): `status "CLOSED_BY_PRECONDITION"`,
  `reason "CLOSED BY R2 (1h: FAIL)"`, `arms []`, `reopening_path "none — the maker twin of the record row reads FAIL too…"`,
  `verdict_cell_reads "CLOSED BY R2 (1h: FAIL) — no number, no slot spent (m = 9 unchanged, the bar 0.10/9 not loosened)"`.
- **Stage S built a GATE, never a scalper.** `M/scripts/tierc11_stage_s.py` (sha `149e4023…22b8`, 1,137 lines) docstring
  :60 "NO scalper book, NO twin, NO regime gate, NO Tier-E arm is built [L-S.1]"; :81 "L-S.2 the form — NOT BUILT"; on a PASS
  it "HALTs GATE-OPEN and writes NOTHING" (:61-68). Fixtures `MR/stage_s/FIXTURES_STAGE_S.txt` (sha `ef38f7e8…4717`)
  "4 GREEN, 0 RED": F-SCALP-GATE (64 plants), F-GRID, F-KEY, F-DET.
- **Consequently NOT on disk anywhere: a 5m EMA12/EMA89 trigger, a 5m (5,5) pivot stop, a resting-limit entry away from the
  close, a tick-based fill rule, a MISS/would-have table, a 5m range-trade walk.** All are new code for TC12.

### 1.4 The R2 verdict plumbing — how "CLOSED BY R2 / precondition" is produced so that it spends no test
1. Stage R computes R2 rows; the lens verdict of record = POOLED:CLASSIC5 · holdout · calibrated · taker
   (`M/scripts/tierc11_stage_r.py:147` `RECORD`; `lens_verdicts` :865-898 → `R2_LENS_VERDICTS.json`).
   Law: `legs_of` :502-513 (height: `n_ranges >= C.HEIGHT_MIN_N_RANGES`, `ratio_median >= C.HEIGHT_RATIO_MIN`,
   `share_lt1 <= C.INFEASIBLE_MAX_SHARE`; edge: `edge_n >= C.EDGE_MIN_N_BARS`, `edge_n_ranges >= C.EDGE_MIN_N_RANGES`,
   `net > 0`); constants `M/scripts/tierc10_census.py:2155-2167` (3.0, 0.10, 30, 30, 30). `word_of` :516-520;
   `record_verdict(word_taker, word_maker)` :523-528 → "PASS" | REOPEN sentence | taker word.
2. Stage S re-derives the word from the JSON's printed columns by the law TYPED there (`LAW` dict
   `tierc11_stage_s.py:198-200`; `legs_of` :352-385; `record_verdict` :388-395; `gate_opens(verdict) = verdict == "PASS"`
   :398-400), cross-checks JSON ↔ parquet ↔ Stage R manifest (`cross_check` :503), then writes
   `regbooks/<REG>/STATUS.json` with `status = STATUS_CLOSED = "CLOSED_BY_PRECONDITION"` (:224) and NO arm (`SS-7`).
3. The scorer (`M/scripts/tierc11_score.py`, sha `81d99d63…5d68`): `STATUS_WORDS = ("BUILT","CLOSED_BY_PRECONDITION",
   "CONDITION_NOT_MET")` (:245); `precondition_record(r2, rid, status)` (:1536-1557) HALTs the row if STATUS disagrees with the
   R2 word; closed rows get `verdict_cell = "CLOSED BY PRECONDITION (…) — report-only · no number · no slot spent"`
   (:1813-1818); `tests_spent = sum(r["spent_test"])` and the law line "m = 9 in every case; bar = 0.10/9 fixed … a
   registration closed by its own precondition or condition spends no test and never loosens the bar" (:2086-2092).
4. X mirrors it: `XR/registrations/SCORED_X.json` (sha `dd9b6e2d…04ae`) row P-SFP-RNG-1: `cell_text "CLOSED BY R2 (1h: FAIL)"`,
   `number_free true`, `test_spent false`, `verdict_of_record null`, `tests_spent {"EXIT": 2, "SFP-RANGE": 0}`,
   `m_law "m is declared and never loosened; a registration closed by its precondition prints its reason, spends no test, and
   leaves m and the bar unchanged (LX-1.2)"`; the precondition is taken from a LANDING RECORD named by path + sha
   (`XR/land/TC11_LANDING_2026-09-25T11-47-02Z.json`, sha `7cb7f869…2cef`), never recomputed at score time. The CLOSED book's
   CI-only reading is still printed in a collared Tier-E block (`tier_e[0]`).

### 1.5 The VA licence TC12's Stage R/S stand on (X3 record; cited for the precondition only)
`XR/va/feasibility.parquet` (sha `ea8573b3…b6f0`, 432 × 75). Rows with `of_record_for_detector == True`
(scale_kind `va_regime`, asset POOLED:CLASSIC5, era holdout, toll taker):
| lens | edge_net_h20 | verdict_pass | lens_word |
|---|---|---|---|
| 4h | 0.093365 | True | PASS |
| 1d | 0.042952 | True | PASS |
| 1h | −0.058994 | False | "FAIL — maker twin PASSES (the reopening path; needs a toll-model change the operator rules)" |
| 12h | −0.029472 | False | FAIL |
Maker rows (toll_bps 4.0), `va_regime`: 1h edge_net +0.038001 PASS; 4h +0.139728 PASS; 1d +0.059306 PASS; 12h −0.003302 FAIL.
NOTE the unit split: at 12h the `va_lblock` maker row reads PASS (+0.004120) while `va_regime` maker reads FAIL.
Tolls there are read from `research_outputs/tierc11/data/fee_schedule.json[<stem>].maker_round_trip_bps / .round_trip_bps_used`.

### 1.6 Tolls, the maker twin, AM-7 (the haircut twin law) and charter slippage — formulae and fee keys
- Fee file of record: `MR/data/fee_schedule.json` (sha `6febe170…968b`; TC10's `M/research_outputs/tierc10/data/fee_schedule.json`
  sha `3a18b84e…e5cc` has NO maker keys). **There is no `M/data/fee_schedule.json`** (see §2).
- Raw per-asset keys (17 rows, `assets[]`): `taker_bps_side_used` 5.0, `round_trip_bps_used` 10.0, **`maker_bps_per_side` 2.0**,
  `maker_round_trip_bps` 4.0, `maker_slippage_bps_side` 0.0, `charter_slippage_bps_per_side` (A 2.0 BTC ETH · B 5.0 SOL NEAR ZEC
  LTC BNB DOGE UNI SUI XMR · C 10.0 ENA PUMP HYPE MNT PEPE BONK), `charter_slippage_tier`, `haircut_twin_bps_side`,
  `maker_kind "ASSUMPTION — Binance USDT-M VIP0 maker per README; the engine books every fill as taker; this is a TWIN, never
  the toll of record [L-1.2]"`, `venue` (`BINANCE_USDTM`; `BYBIT_V5_LINEAR` for MNT). Top-level `maker_source`: README.md:150
  + `scripts/v3_recompute.py:965`; read by regex, never typed (`M/scripts/tierc11_data.py:274-290` `read_maker_bps_side`).
- Reader: `E.fees() -> {stem: {...}}` (`M/scripts/tierc11_env.py:1025-1044`; X twin `X/scripts/tc11x_env.py:1277-1296`) with
  NORMALISED keys `taker_bps_side, taker_round_trip_bps, maker_bps_side, maker_round_trip_bps, maker_kind,
  maker_slippage_bps_side, slippage_bps_side, slippage_tier`. So the contract's key name `maker_bps_side` exists only as the
  reader's key; on disk it is `maker_bps_per_side`, per ASSET not per venue.
- R2 tolls: `toll_bps(stem, toll)` (`tierc11_stage_r.py:481-492`): taker `taker_round_trip_bps`; maker
  `2·maker_bps_side + 2·maker_slippage_bps_side`; charter `2·(taker_bps_side + slippage_bps_side)`.
- **Maker twin per fill** (L-1.2 `MR/LEANS.md:85-93`; LX-1.1 `XR/LEANS_X.md:544-612`; code `tc11x_sfp.py:756-803`):
  `fee_per_fraction(e, R, harvest_px, exit_px, b_e, b_t1, b_x)` = harvested `[Q·(b_e·e + b_t1·p_T1) + (1−Q)·(b_e·e + b_x·p_x)]/R`,
  else `(b_e·e + b_x·p_x)/R`, `b = bps/10_000`. In `book_trade`: `tk = taker_bps_side/1e4`, `mk = maker_bps_side/1e4`;
  `b_x = tk if exit_reason in TAKER_EXITS else mk` with `TAKER_EXITS = ("stop","time_stop","corridor_end","range_death",
  "reversed")` (:148); `maker_fee = fee_per_fraction(e, R, hpx, xpx, mk, mk, b_x)`; `maker_net = gross_r − maker_fee − funding_r`.
  Maker legs = entry, T1, T2; zero slippage on every leg of the maker row.
- **AM-7** (`MR/LEANS_AMENDMENTS.md:86-96`): `haircut_net_r = net_r − fee_r × (slip_bps_side / taker_bps_side)`; `fee_r` = the
  ride's own taker fee over EVERY fill; slip = the stem's charter tier; funding stays in. "A maker leg (scalper twins) carries
  zero slippage (L-1.2), so the maker twins apply the law to their taker legs only." Code: `haircut = acc["net_r"] −
  acc["fee_r"] * (slip / fz["taker_bps_side"])` (`tc11x_sfp.py:782`), asserted equal (1e-12 R) to the per-fraction form at
  `taker + slip` bps (:783-788). Maker-row variant: `stop_leg_slip_haircut_net_r = maker_net − taker_leg_fee × (slip/taker)`
  with `taker_leg_fee = (0 if exit is maker else ((1−Q) if harvested else 1)·tk·xpx/R)` (:781, :798).
- F-FEE-EQ law: the per-fraction booking at all-taker bps equals `account_l` to 1e-12 R (:789-792; bit-equality is unattainable,
  `LEANS_X.md:1340-1344`).
- The haircut function has NO single home in TC11: `haircut()` is re-typed in `tierc11_stage_h.py:467`, `tierc11_stage_g.py:611`,
  `tierc11_stage_w.py:1539`, `tierc11_stage_t_brk.py:444`, `tierc11_stage_t_relay.py:371`, `tierc11_forward_ledger.py:190`.

### 1.7 Limit-order / fill models already written (touch vs through)
| where | rule | price |
|---|---|---|
| `tierc11_ride.py:630-632` (TP) | TOUCH `h >= lvl` | `max(lvl, open)` |
| `tc11x_sfp.py:558-601` record | TOUCH (`_hit` non-strict) | `max(level, open)` |
| `tc11x_sfp.py:681-685` maker_conditioned ENTRY | THROUGH, strict, **the FIRST 5m child of the next lens bar only**: `fl < e` long / `fh > e` short; absent child → `miss_nochild` | the limit `P = c[harden_i]` |
| `tc11x_sfp.py:677-680` maker_within_hour ENTRY | THROUGH at ANY 5m child of the next lens bar | same |
| `tc11x_sfp.py:664`, `:692-705` maker_conditioned TARGETS | THROUGH, strict (`h > T`) — "A touch that does not trade through is not a fill" (`LEANS_X.md:598-599`) | level |
Fill-bar law (LX-1.1 (ii), `LEANS_X.md:590-597`; code :686-712): on the fill child the STOP is tested adverse-first; **targets
are never credited on the fill child** (counted `fillchild_target_withheld`); the rest of the fill bar is walked child by child
STOP → T1 → T2; if the children fail REPR, targets are denied on that bar. Funding of a conditioned fill is booked from the
fill bar (`fund_i = j1`, :676). Misses are refusal rows (`reason` "miss" / "miss_nochild" / "fill_unresolved_at_pin"), never trades.
**No rule anywhere uses a tick size; no order rests at a price away from the trigger close; no validity window longer than
one lens bar; no would-have table for misses.**

### 1.8 Funding journaling per trade
`BK.funding_interval(lf, entry_ms, exit_ms, d, qty)` (`tierc10_brk.py:1223-1267`): every stamp with
`entry_ms < funding_hour_ms <= exit_ms`, priced at the close of the last lens bar closed at or before it
(`funding_price_idx` :1213-1220, `searchsorted(open + step, stamp, "right") − 1`); `amt += rate · close · d · qty`, accumulated
one stamp at a time in ascending order (the order is load-bearing: vectorised sum drifts 1.665e-16, :1250-1255); returns
`amount, n_stamps, n_priced, n_unpriced, n_on_bar_open`. In `account_l`: `t_entry = lf.open_ms[entry_i]`, exits at
`lf.open_ms[exit_i]` (:1286-1293) — so a settlement at the entry-CLOSE instant is paid, one at a close-exit instant is not
(`LEANS_X.md:1325-1326`); harvested fraction funded to the harvest bar, remainder to the exit bar. D12 ceiling:
`cap = card.funding_ceiling_r` = 1.0 (`M/scripts/tierc5_rules.py:160-161`), binds only on a COST (:1319-1321). Funding source:
`D.load_funding_asof(sym)` grouped by `funding_hour_ms` (:908-917). `LensFrame` (:850-899) carries
`sym lens open_ms o h l c atr step_ms fund_hour_ms fund_rate uid`; `frame_l(sym, lens, with_funding=True)` (:920-954) is
lens-generic and accepts `"5m"`.

### 1.9 TICK SIZE — it IS on disk
- `MR/data/CONTRACT_SPECS.json` (sha `74d9d47b…6b7e`; captured `2026-09-25T00:57:48Z`, endpoint
  `https://fapi.binance.com/fapi/v1/exchangeInfo`, `binance_response_sha256 78a2bcf6…af13`; Bybit `…/v5/market/instruments-info`).
  Per asset: `assets[].price_tick` (string) = `venue_object.filters[PRICE_FILTER].tickSize`, plus `price_precision`, `qty_step`,
  `min_qty`, `min_notional_usdt`. TC10's `M/research_outputs/tierc10/data/CONTRACT_SPECS.json` (sha `275b218d…76d4`,
  captured 2026-09-22T13:11:55Z) carries the same values for CLASSIC5.
- CLASSIC5 `price_tick`: **BTCUSDT "0.10" · ETHUSDT "0.01" · SOLUSDT "0.0100" · NEARUSDT "0.0010" · ZECUSDT "0.01"**
  (the twelve: ENA 0.0000100, PUMP 0.0000010, HYPE 0.00100, MNT(Bybit) 0.00010, SUI 0.000100, LTC 0.01, XMR 0.01, BNB 0.010,
  UNI 0.0010, 1000PEPE 0.0000001, DOGE 0.000010, 1000BONK 0.0000010).
- Capture code: `M/scripts/tierc11_data.py:1040` / `:1060` (write-once, sealed: `SEALED_FILES` :1427).
  Existing reader precedent: `price_tick(stem)` in `M/scripts/tierc11_books_fixtures.py:340-346` (used for one-tick sabotage).
- **The snapshot tick is NOT the historical tick** (unconditional inspection of
  `~/.cache/naiad/snapshots/tc11_20260925/klines/<S>_5m.parquet`, columns `open_time open high low close volume`):
  share of 5m lows on the snapshot tick grid — BTC ALL 0.767128 / tuning 0.65899 / **holdout 1.0** (last off-grid bar
  2022-04-30); ETH 1.0 / 1.0 / 1.0; **SOL ALL 0.551146 / tuning 0.349845 / holdout 0.892987** (off-grid share by quarter:
  2024Q3 0.9992, 2024Q4 0.1636, 2025Q1 0.0088, then ≤ 0.0001 with isolated prints at 0.001 precision as late as
  2026-08-29T18:00Z); NEAR 0.819861 / 0.711352 / **1.0** (last 2022-02-22); ZEC 1.0 / 1.0 / 1.0. Holdout 5m bars per asset 235,009.
- Scale of one tick: holdout median 5m range ÷ tick = BTC 1142, ETH 551, SOL 37, ZEC 34, **NEAR 10**. Holdout ATR_1h in ticks
  (p1 / p5 / p50): BTC 1835.6 / 2389.0 / 5150.2; ETH 757.9 / 1059.4 / 2443.5; SOL 35.3 / 51.3 / 161.1; ZEC 28.2 / 34.7 / 105.4;
  **NEAR 10.1 / 13.2 / 39.1**. Share of holdout 1h bars with `0.05·ATR_1h < 1 tick`: BTC 0.0000, ETH 0.0000, SOL 0.0004,
  ZEC 0.0017, **NEAR 0.1825**; with `0.25·ATR_1h < 1 tick`: 0 on all five.

### 1.10 ATR_L per lens and the as-of alignment
- ATR everywhere = `engine.indicators.atr(h, l, c, 14)` on the lens's WHOLE tape: `atr = rma(true_range, length)`
  (`M/engine/indicators.py:53-54`); `rma` = Wilder, `alpha = 1/len`, seeded at the first finite value (:31-42);
  `true_range` (:45-50) with `tr[0] = h[0] − l[0]`. Length `ATR_LEN = 14` (`M/scripts/tierc2_rules.py:81-82`, :121;
  `M/analytics/rangefinder_census.py:132`). Recursive ⇒ the value at bar k uses bars ≤ k only (L-R.1 `MR/LEANS.md:172-175`).
  X asserts it: `load_x` HALTs unless `tape.atr == IND.atr(h, l, c, RC.ATR_LEN)` (`X/scripts/tc11x_ranges.py:584-604`);
  `BK.frame_l` builds `atr=ind.atr(h, l, c, ATR_LEN)` (`tierc10_brk.py:951`). 1d and 1w are derived from native 4h (L-R.1).
- EMA = `ind.ema(values, length)`: recursive, `alpha = 2/(length + 1)`, **seeded at the series start with the first finite value
  — no SMA seed, never NaN** (`indicators.py:17-28`); crossover `a > b now AND a <= b on the prior bar`, NaN compares False
  (:66-71), crossunder mirrored (:74-78). Warm-up law of the lineage: "an EMA of period p is READABLE from bar p and not
  before" (`tierc10_brk.py:1050-1078`, `warm_components`: `entry_i >= max(periods)`); `cross_1h` applies no floor.
- TWO as-of laws exist and they differ by one bar at a boundary:
  1. **Instant = a CLOSE** — `C.asof_index(tape, instant_ms) = searchsorted(t0 + step, instant, side="right") − 1`
     (`M/scripts/tierc10_census.py:894-900`): the last lens bar whose close ≤ the instant; a 1h bar closing EXACTLY at a 5m close
     IS visible; a bar still forming is never read. Used by the nest (`_lens_arrays`, `M/scripts/tierc11_nest.py:1079-1107`;
     `nest_at` :1158-1183, L-R.5 `MR/LEANS.md:218-241`).
  2. **Instant = the exec bar's OPEN** — `engine.htf.map_htf_to_exec` (`M/engine/htf.py:15-25`) and
     `BK.visible_htf_idx(exec_open_ms, htf_open_ms, htf_step_ms)` (`tierc10_brk.py:1727-1746`): HTF close ≤ exec OPEN; "a 4h bar
     that closes exactly AT the entry instant is NOT read" (`tide_4h_for_exec` docstring :1761-1773). Also the TP hook:
     `asof_12h_index(close12_ms, open4_ms)` at the 4h bar's OPEN (`M/scripts/tierc11_stage_h.py:265-270`, `levels_from_facts` :273-293).
  For a decision taken AT a 5m close t, law 1 with instant = t shows the 1h/4h/1d bar that closed at or before t; for an order
  RESTING DURING 5m bar j, law 2 with instant = open_j (= close of j − 1) gives the same HTF bar. They agree iff the exec
  instant is expressed as the close of the last finished 5m bar.
- Nest vector schema (`NEST_FIELDS`, `tierc11_nest.py:1006-1013`), per lens prefix `L_`: `k(Int64) bar_close_ms(Int64)
  state(object) in_range(boolean) pct(float) dist_signed_atr(float) near_side(Int8) bnd_age(Int64) dev_top dev_bot(Int64)
  flip_pol(Int8) flip_age(Int64) top bot atr_L(float) coin_top coin_bot coin_top_mem coin_bot_mem(boolean)`; coincidence
  `COIN_FRAC = 0.25` inclusive (`:108`, `within` :1016-1026, `coin_flags` :1029-1051); ladder `1h→4h→12h→1d→1w` (:101).

### 1.11 R5 — the pivot-state table, printed (source of the contract's "+0.49 with / −0.49 against")
`MR/stage_r/R5_CHOP_DIRECTION.parquet` (sha `a73b4894…46f1`; rendered `MR/stage_r/R5_CHOP.md:120-121`, sha `601b932a…4f16`);
code `r5_direction` (`tierc11_stage_r.py:1687-1717`), `align_of` (:1650-1661). Split `alignment`, v6 book (n 200, Σ 40.807566):
| cell | n | n_long | n_short | mean_net_r | p_win | sum_net_r | n_holdout |
|---|---|---|---|---|---|---|---|
| calibrated\|4h\|EXP_ALIGNED | 47 | 24 | 23 | **0.491349** | 0.382979 | 23.093382 | 17 |
| calibrated\|4h\|EXP_COUNTER | 12 | 4 | 8 | **−0.493933** | 0.250000 | −5.927196 | 7 |
| calibrated\|4h\|IN_RANGE | 141 | 69 | 72 | 0.167669 | 0.340426 | 23.641380 | 53 |
| calibrated\|4h\|__ALL__ | 200 | 97 | 103 | 0.204038 | 0.345000 | 40.807566 | 77 |
| frozen3.0\|4h\|EXP_ALIGNED | 92 | 55 | 37 | 0.237982 | 0.336957 | 21.894334 | 27 |
| frozen3.0\|4h\|EXP_COUNTER | 14 | 3 | 11 | −0.573981 | 0.214286 | −8.035731 | 5 |
| frozen3.0\|4h\|IN_RANGE | 94 | 39 | 55 | 0.286691 | 0.372340 | 26.948963 | 45 |
| calibrated\|12h\|EXP_ALIGNED | 87 | 53 | 34 | 0.292468 | 0.379310 | 25.444684 | 27 |
| calibrated\|12h\|EXP_COUNTER | 10 | 5 | 5 | 0.103576 | 0.300000 | 1.035763 | 1 |
| calibrated\|12h\|IN_RANGE | 103 | 39 | 64 | 0.139098 | 0.320388 | 14.327119 | 49 |
| frozen3.0\|12h\|EXP_ALIGNED | 108 | 62 | 46 | 0.192825 | 0.305556 | 20.825145 | 35 |
| frozen3.0\|12h\|EXP_COUNTER | 18 | 4 | 14 | 0.438518 | 0.555556 | 7.893315 | 6 |
The `R5_CHOP.md:120-121` rows also print holdout: EXP_ALIGNED holdout mean 1.3416 (n 17); EXP_COUNTER holdout −0.3683 (n 7).
Split `pct_dir_adj` (calibrated 4h): [0,33.33) n 1 mean −1.044801; [33.33,66.67) n 55 mean 0.353702; [66.67,100) n 81 mean
0.056045; ≥100 n 4 mean 0.173220. R5 by decile: `MR/stage_r/R5_CHOP.parquet` (sha `1403a773…2b04`, `r5_chop` :1617-1636,
`bucket_of` :1601-1614, `R5_LENSES = ("4h","12h")` :169). Schema of both: `cell scale_kind lens [split] bucket [n_long n_short]
n mean_net_r p_win sum_net_r nan_reason n_scale_in_sample n_stability_changed n_holdout mean_net_r_holdout p_win_holdout
sum_net_r_holdout nan_reason_holdout lenses_read pick_window stability_changed_members [split_law] tier
selection_not_a_result gates as_of_last_closed_4h as_of_substrate`. Cell statistic law `_stats` :1470-1477, `_cell` :1535-1544.
The sign of the R5 effect holds at 4h on both scales and REVERSES at 12h frozen-3.0 (EXP_COUNTER +0.438518).

### 1.12 R10 — the "gaps+order" null of record
- Home: `M/scripts/tierc10_null.py` (sha `c9f19e70…95db`). `K_DEFAULT = 20` (:109); `SCHEDULE_VARIANTS = {"gaps+order": False,
  "gaps-only": True}` (:120) → `schedule(real, rng, keep_order=False)` (:293-332): permutes the m+1 GAPS and the ORDER of the
  (life, height) pairs of the REAL confirmed pivot ranges (`real_box_set` :239-272), each pair kept whole, one `u ~ U[0,1)` per box;
  lead-gap swap if `g[0] < RC.ATR_LEN`. RNG `draw_rng(seed, draw, asset, lens, scale_kind) =
  default_rng([seed + draw, crc32("asset|lens|scale_kind")])` (:286-290). Box edges `box_bounds` (:335-340); machine
  `static_box_machine` (:356); `null_view` (:478).
- TC11 rebuild: `M/scripts/tierc11_stage_r4.py` (sha `bd6364d1…eb67`): `K_DRAWS = 20` typed (:112), `SCHEDULE_VARIANT =
  "gaps+order"` (:114), `NULL_SEEDS = (SEED, SEED_SENS)` (:113), `null_draw` (:713-754) = `NL.draw_rng` → `NL.schedule(…,
  keep_order=False)` → `NL.static_box_machine` → `RC.flips_and_leash(…, retests=False)` → TC11's scan with the REAL L+1.
  Output `MR/stage_r4/R4_NULL.parquet` (sha `1cdafba4…9f84`). X reads K by object: `K_DRAWS = int(NL.K_DEFAULT)`
  (`tc11x_va.py:180`, `tc11x_sfp.py:130`), `null_pivot_cell` (`tc11x_va.py:1509-1570`).
- How a percentile is read: `PCTILE_LAW = "mid-rank: 100 x (#null < real + 0.5 x #null == real) / valid draws"`
  (`tierc10_null.py:224`; code :628-630; TC11 `_pctile` `tierc11_stage_r4.py:1058-1065`; X `_pctile` `tc11x_va.py:1847-1852`).
  "A DESCRIPTION of where the real value sits among the K draws, never a p-value; K = 20 resolves it to 5 points at best"
  (`tierc11_stage_r4.py:146-148`). Statistics percentiled: `NULL_STATS = ("median_term","net","hit_rate_net")` (:143).
- The null is defined on PIVOT BOXES (lives, gaps, heights of confirmed ranges). For the value area X filed a DIFFERENT null of
  record: `NULL_OF_RECORD = {"va": "tr_tercile_lblock", "pivot": "gaps+order"}` (`tc11x_va.py:236`; LX-X3.13
  `XR/LEANS_X.md:1793-1809`: a true-range-tercile-stratified L-block volume permutation, K = 20, RNG
  `[20260925 + draw, crc32("asset|lens|va")]`, `null_rng` :1125-1127).

### 1.13 FLIP_HOLD pins (names, values, file)
- Source of record: `M/engine/rangefinder.py` (sha `bbae464f…84d4`) `PINS_V2` :573-589: `"SCALE_MULT": 3.0` (:586),
  **`"FLIP_HOLD_MARGIN": 1.0`** (:587), **`"FLIP_HOLD_BARS": 6`** (:588), `"MEM_TTL_BARS": 400` (:589). Port copy
  `M/analytics/rangefinder_census.py:154-159` (sha `19c5507f…b37d`). Law: a flip is decided by bars i..i+FLIP_HOLD_BARS and
  is KNOWN at i + HOLD (`rangefinder_census.py:717`).
- Readers: `tierc10_brk.py:145-149` (`D.pin_literal(…, "PINS_V2", "FLIP_HOLD_MARGIN")` — read out of the AST, never imported, to
  keep the v6 path range-free); `tc11x_va.py:174-176` (`HOLD_MARGIN`, `HOLD_BARS`, `TTL` from `RC.PINS_V2`).
- Do not confuse with the BAND retest pins `C.RETEST_PINS` = margin 1.0 / **hold 3** / ttl 400 (`RETEST_OF_RECORD`,
  `tierc11_nest.py:238`, grid sha `2135ca66…e7b3`; `tc11x_ranges.py:361`), which P-BRK-4H used.
- X's VA breakout-retest of record already uses FLIP_HOLD: `scan_retests(h, l, c, atr, anchors, "va", HOLD_MARGIN, HOLD_BARS,
  TTL)` (`tc11x_va.py:1180`); verdict law `retest_verdict` (:674-687): `j + hold >= n` → truncated; FAILED iff a close in
  j..j+hold is through the level by margin·ATR; else HOLD; known at j + hold.
- Other range pins TC12's V2 text echoes: `BREAK_CONFIRM_N = 8` (`rangefinder_census.py:141`), `BREAK_MARGIN = 1.5` (:144),
  `DEV_RETURN_BARS = 7` (X `DEV_RETURN`, `tc11x_va.py:171`).

### 1.14 Time-stop pins on disk (pivot traverse; NOT a value-area traverse)
`XR/pins/PINS_X.json` (sha `85e1eeea…498f`), read via `R.time_stop(lens, twin="A")` (`tc11x_ranges.py:1349-1352`):
`T.by_lens["1h"].T_of_record = 13` (twins B1 13, frozen3.0 33); `T.by_lens["4h"].T_of_record = 13` (twins B1 16, frozen3.0 30).
Definition (A) = the machine's confirm traverse `confirm_i − p1_bar`, `ceil(median)` over pooled CLASSIC5 confirmed ranges of
the tuning-era head (`t_pin` :819-832; LX-X2.7 `LEANS_X.md:1226-1260`); (B1) = in-range traverse from a touch to the first
opposite touch (`b_traverses` :787-810, touch law `RC.PINS["TOUCH_EPS"]`). **T exists only for 1h and 4h** (`T_LENSES`, :355).
Per-range table `XR/pins/traverse_ranges.parquet` (sha `d0700bd6…4fd3`). Lookbacks `L_of_record`: 1h 71, 4h 66, 12h 53, 1d 35
(`R.lookback`, :1355-1362); none for 1w. F-TRAVERSE precedent: an AST leg FAILS on any integer literal passed as the time stop
(`XR/sfp/FIXTURES_X2.txt`, sha `2c51abe2…bf0d`, "12 GREEN, 0 RED").

### 1.15 X's VA episode machine vs the contract's V2 (cited because P-SFP-VA-1 / P-SCALP-3 trade its events)
`va_episodes(c, h, l, atr, VAL, VAH, law=EpLaw()) -> {"episodes","regimes","counters"}` (`tc11x_va.py:544-646`), record law
`EpLaw(ref="prev", frozen=True, ret_k=DEV_RETURN, die_parity=False, rearm=True)` (:520-527):
- each close is judged against VA(t−1) (`ref_arrays` :535-541); a close beyond an ARMED side opens an episode with the edge
  FROZEN at t0 (`E`); while pending, beyond → `closes += 1`, **acceptance at `closes >= ACCEPT_N` (8)** only;
  at-or-inside → `"sfp" if t − t0 <= ret_k else "lapse"` with **ret_k = 7** of record; the episode carries
  `side, t0, E, closes, extreme (max h / min l over t0..end), end_i, end_kind, by, bars_out, E_end, sgn_sfp, sgn_accept`.
- twins: `"die_parity"` (acceptance ALSO by one close ≥ `BREAK_MARGIN` 1.5·ATR beyond), `"k1"`, `"k3"` (ret_k 1, 3),
  `"moving_edge"`, `"self_inclusive"`, `"no_rearm"` (`EP_LAWS` :530-532) — **each twin changes ONE field**.
- "L+1 conditioning is not built" (`LPLUS1_NOTE`, :206). Two-trades outcomes there are H20/H100 terms per direction
  (`XR/va/two_trades.parquet`, sha `a03ef134…91b0`, 11,520 × 58; `HORIZONS = (("H20",20),("H100",100))`,
  `tierc10_census.py:123`), not rides.

### 1.16 P-TP-RNG and P-BRK-4H (the two other registrations named in the unit)
- P-TP-RNG: seq 9, payload sha `ad12a44c…e808`, prior 35, paired vs card-v6; scored arm = "at each 4h bar, with the 12h as-of
  state at the bar's OPEN IN_RANGE, a resting limit for the remainder … at the 12h far boundary -/+ 0.25 ATR_12h, live only when
  the prior 4h close is on the near side AND the level is beyond entry in the trade's favour by > 10 bps; fill at max(level,
  open) for a long …; order STOP -> TP -> BELL -> HARVEST -> TRAIL; v6 harvest kept [L-H.1]"; named risk "the wall-exit lesson:
  P-WALL-1 (TC6) delta -0.0331, tail ratio 0.9329". Engine: `tierc11_ride.ride11(tp=TPLevels)`; levels:
  `tierc11_stage_h.levels_from_facts(open4_ms, facts)` (`:273-293`, sha of file `780897bf…d159`).
- P-BRK-4H: seq 4, payload sha `120939d9…1655`, prior 45, vs zero; "4h macro death … -> the FIRST retest that HOLDS on tap-89 …
  census RETEST_PINS margin 1.0 ATR, hold 3 bars, ttl 400 … stop BK.brk_stop beyond the retest extreme, offset 0.5 ATR(4h),
  railed R >= 1.0 ATR(4h); tide aligned at the entry bar's close; v6 management (BK.ride_leg_l, ribbon=None, no 12/25 bell)".
- Verdict rule shared by all nine: SUPPORTED iff cluster-90% CI lower bound > 0 AND one-sided p ≤ bar (T5 primitives:
  `cluster_boot(values, clusters, seed, n_boot)` `M/scripts/tierc5.py:1178-1197`; `_ci_from(draws, point)` :1227-1235 with
  `p_one_sided = (Σ(d <= 0) + 1)/(len + 1)`); LOAO `TP.loao_n(new, base, panel, two_sample, seed, label, n_boot)`
  (`M/scripts/tierc10_panel.py:1234-1255`); era `E.era_of(close_ms)` — tuning iff close ≤ `ERA_CUT_MS` 1719791999000
  (2024-06-30T23:59:59Z) (`tierc11_env.py:1047-1055`; `PINS_X.json` `era_cut_ms`).
- Regime-column helper: `tc11x_pct.trailing_counts(arr, i, window=WINDOW, floor=FLOOR) -> (lt, eq, n) | None`,
  `trailing_pct(...)` midrank `100·(2·lt + eq)/(2n)` (`X/scripts/tc11x_pct.py:48-49, 71, 106`, sha `49809c07…4bb7`;
  WINDOW 2000, FLOOR 300; a third decided in integers `3(2lt + eq) < 2n / < 4n`).

### 1.17 Shas of the records and code TC12 would pin for this unit
| path | sha256 |
|---|---|
| `M/scripts/tierc11_ride.py` | `65eb880f2b127a26cc07a6bf40e6ca6556dac37aa62bdfef45e3b045aa26915d` |
| `M/scripts/tierc11_stage_r.py` | `b0d2d23bddb62e2648b57697ff53089b83e6096a12e3ad9ff4ed92d74b8ad4fe` |
| `M/scripts/tierc11_stage_r4.py` | `bd6364d16ab120d85200c52527684a229c2cc12852fd09a4579ab14a3be9eb67` |
| `M/scripts/tierc11_stage_s.py` | `149e4023b5668bf2a8f6a8424e3291a9c1a021fd1378b851c29ccd50d6db22b8` |
| `M/scripts/tierc11_nest.py` | `16e325022523064e67eede439998e9ee4cacfeb0df8171202a85b46125827429` |
| `M/scripts/tierc11_stage_h.py` | `780897bffd0a6c0d011ffdb54f881e456aaeb30d15a35519cdd05a630dadd159` |
| `M/scripts/tierc11_score.py` | `81d99d63f9367268780fe9ec37a0c6af058b03670a83aaff010a93090eab5d68` |
| `M/scripts/tierc11_env.py` | `1526093b25161927337ced6112a310075b1a57c825f08705814e48619398f798` |
| `M/scripts/tierc10_brk.py` | `9c26561c7ad405101496217b145ab78a20e4ee805a5ddfd117dceaa0a7177ae6` |
| `M/scripts/tierc10_null.py` | `c9f19e701996c4048f0037f621b60746f887978571711dbfa6bbd97ba8f995db` |
| `M/scripts/tierc10_census.py` | `0e6cb635436acc2dd75fb0757506bd6122975453ca45a3c311fa4a3d67d7a6ef` |
| `M/scripts/tierc10_lanes.py` | `c9142f1123356ad57687bca6f9877b2d1dd5f04071bac19e41e5bd806daa28a4` |
| `M/scripts/tierc5.py` / `tierc5_rules.py` / `tierc7.py` | `ad912b38…5a6f` / `c27a5ecb…1515` / `6abeaf6e…1452` |
| `M/engine/indicators.py` / `engine/htf.py` | `91805c04130c3701e16f933b4c4ac258109f8636d9cd8a0ae44787d86f13c113` / `52722f1f5540ae4658d12d28bd40af233d774679506334b91edc5fb08cffcfba` |
| `M/engine/rangefinder.py` / `analytics/rangefinder_census.py` | `bbae464f…84d4` / `19c5507f…b37d` |
| `X/scripts/tc11x_sfp.py` | `79ba35f417a5d6d9f59c574f60376945e55722559495ba69a162a917bcd40f95` |
| `X/scripts/tc11x_ranges.py` | `26e829d8990b462fc6f22829a9974a5a291fee462dadf58e1160d749dd127d8d` |
| `X/scripts/tc11x_exit.py` | `2b7b404ff60357f1dc524a9fbb24b28d2695dbaf814e4809102c0c2895358945` |
| `X/scripts/tc11x_va.py` | `3f6a43cbbf7fd71cb374bd9e2b2fd16b1cd9bd52b24437a35fb76b9c171ca422` |
| `X/scripts/tc11x_pct.py` | `49809c070ed00223a345edc51b5d83355f229a6b1372495038ff42aeba204bb7` |
| `X/scripts/tc11x_env.py` / `tc11x_data.py` | `db74225e…6928` / `c73ca805…68d6` |
| `MR/data/fee_schedule.json` | `6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b` |
| `MR/data/CONTRACT_SPECS.json` | `74d9d47b7177955237339eb417100581230efbaf13f2701677436df1c74a6b7e` |
| `MR/registrations/REGISTRATIONS.json` / `REGISTRY_PIN.json` | `648834bf…f1ee` / `ea77921a…748f` |
| `MR/regbooks/P-SCALP-2/STATUS.json` | `5457ea6aeac139a832b3312051fdfef88f409402d0c096678c02cc332c473eda` |
| `MR/stage_r/R2_LENS_VERDICTS.json` / `R2_FEASIBILITY.parquet` / `build_manifest.json` | `82cc3ec6…3087` / `009a30de…04e4` / `087c8556…74d8` |
| `MR/stage_r/R5_CHOP_DIRECTION.parquet` / `R5_CHOP.parquet` / `R5_FIVE_ROW.parquet` | `a73b4894…46f1` / `1403a773…2b04` / `228ef18b…2fe3` |
| `MR/stage_s/S_GATE.json` / `S_R2_1H.parquet` / `build_manifest.json` | `4846bf2a…18c8` / `1ca126e7…7976` / `ece63e68…9fc9` |
| `MR/stage_r4/R4_NULL.parquet` / `R4_GRID.parquet` / `build_manifest.json` | `1cdafba4…9f84` / `1ff9e837…0cc3` / `c822a592…ea75` |
| `MR/LEANS.md` / `LEANS_AMENDMENTS.md` / `ranges/SCALE_PICKS.json` | `655e1605…294f` / `85f57ce7…0c07` / `cb5319c9…454f` |
| `XR/LEANS_X.md` / `LEANS_X_AMENDMENTS.md` | `74a989ee…8623` / `af845b95…d059` |
| `XR/pins/PINS_X.json` / `traverse_ranges.parquet` | `85e1eeea2d04ffe834b93caf76aae55b1f427ae7935b12a7ecae9d814be7498f` / `d0700bd6…4fd3` |
| `XR/sfp/X2_trades_1h.parquet` / `X2_trades_4h.parquet` | `4e3b5f4f7eb01db468b4203c4b64362f54fe388419290b5c58a68d9a54427eac` / `552e7582d7559c032438f89c402e3070a3011559c1b334babd4c942f23b1bbef` |
| `XR/sfp/X2_twins.parquet` / `X2_refusals.parquet` / `X2_grid.parquet` / `build_manifest.json` | `f2abf81d…8c25` / `81b7fa6c…534d` / `4e75539e…d7e8` / `6f786d84…3835` |
| `XR/census/height_toll_verdict.parquet` / `height_toll.parquet` | `5302fb35…a6cf` / `c1a36c6e…79a8` |
| `XR/exit/X1_cells.parquet` / `X1_registered.parquet` / `build_manifest.json` | `19507647…3d8c` / `06049937…b936` / `6f57e78e…3bc6` |
| `XR/va/feasibility.parquet` / `two_trades.parquet` / `build_manifest.json` | `ea8573b3…b6f0` / `a03ef134…91b0` / `769ac091…078b` |
| `XR/registrations/SCORED_X.json` / `REGISTRATIONS_X.json` | `dd9b6e2d…04ae` / `6b0eb52d…b0a4` |
(Full 64-hex values for the abbreviated rows are reproducible with `shasum -a 256 <path>`; the abbreviations are first-8…last-4.)

`tc11x_exit.py` (X1) is the trail-offset family on v6's 4h ride (`ride_x` = `T9._ride_leg9` verbatim with one changed site);
it carries nothing a range trade or scalper needs, and TC12 forbids "trail-offset tuning".

---------------------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

C1. **"`data/fee_schedule.json` must carry maker_bps_side per venue; if absent, add it from the venue's published USDT-M perps
schedule, cite URL + date"** (contract :21-23). Disk: no `M/data/fee_schedule.json`. The fee records are
`research_outputs/tierc11/data/fee_schedule.json` (and tierc10's). The key on disk is `maker_bps_per_side` (per ASSET),
exposed as `maker_bps_side` only by `E.fees()`. It is PRESENT = 2.0, but its provenance is README.md:150 + `v3_recompute.py:965`,
labelled "ASSUMPTION" — not a venue URL + date; and Bybit's (MNT) is declared "not in the repo".

C2. **"FILL OF RECORD … THROUGH the limit by ≥ 1 tick (low < limit − tick for a long)"** (:93-94). Disk: (a) the tick exists
(`CONTRACT_SPECS.json assets[].price_tick`) but as ONE snapshot at 2026-09-25; the tape shows other tick regimes inside the
scored era for SOL (holdout on-grid share 0.892987) and isolated off-grid prints to 2026-08-29. (b) The two halves of the
sentence disagree on a tick grid: "by ≥ 1 tick" is `low <= limit − tick`; the parenthesis is strict `<`. (c) The limit "AT the
edge" is a profile-bin float, not a tick-grid price. (d) No tick-based fill exists in code.

C3. **"Twins printed: TOUCH (low ≤ limit) · DEEP (through by 0.05 ATR_1h)"** and **F-SCALP "fill rule ordering TOUCH ≥ TICK ≥
DEEP by n filled — an inverted order must FAIL"** (:94-95, :120-121). Disk: `0.05·ATR_1h < 1 tick` on 18.25% of NEAR's holdout
1h bars (0.17% ZEC, 0.04% SOL). There DEEP as written is LOOSER than TICK, so TICK ⊇ DEEP is not a set inclusion and the
count ordering is not guaranteed by construction.

C4. **"TIME STOP = the 4h traverse (V4)" / "the 1h traverse (V4)"; V4 = "the median bars for price to travel edge-to-edge
while INSIDE"** (:42-43, :72, :100). Disk: the only traverse pins are PIVOT traverses (`PINS_X.json` T: 1h 13, 4h 13; B1 13/16),
defined on confirmed pivot ranges, for 1h and 4h only. No value-area edge-to-edge traverse exists; none for 1d. V4 is a new table.
The contract also does not say how a 1h-bar count becomes a clock on the 5m walk.

C5. **"null gaps+order (R10)"** for the two trades "on the VA at 4h and 1d" (:76-79). Disk: gaps+order permutes confirmed PIVOT
ranges' lives and gaps; X's null of record for the value area is `tr_tercile_lblock` (`tc11x_va.py:236`), and X states the two
"answer different questions" (`LEANS_X.md:1807-1808`). A gaps+order null needs a box set with lives/gaps/heights; the VA analogue
would be X's "value regimes" (`regimes` from `va_episodes`), which no filed code feeds to `NL.schedule`.

C6. **"the breakout-retest (ACCEPTED → first retest of the accepted edge that holds, FLIP_HOLD pins reused)"** (:77-78). Disk:
consistent — X's VA record already uses `FLIP_HOLD_MARGIN 1.0 / FLIP_HOLD_BARS 6 / MEM_TTL_BARS 400`. But "ACCEPTED" there is
X's record acceptance (8 closes only), not the contract's V2 acceptance (8 closes OR 1.5 ATR).

C7. **"conditioned on the lens above {accepted aligned · inside mid · inside at its own edge (coincidence)}"** (:78-79). Disk:
X built no L+1 conditioning for the VA (`LPLUS1_NOTE`). TC11's partition is on PIVOT states (`N.CELLS`, `tierc11_nest.py:1466-1467`:
EXP_ALIGNED, EXP_COUNTER, IN_RANGE_COINCIDENT, IN_RANGE_MID, IN_RANGE_OTHER, NONE, NA; `STARRED` :1468 = the first, third and
fourth; mid = pct ∈ [25, 75] inclusive, `MID_BAND` :109).
The contract names three cells; the estate's precedent prints a WHOLE partition with the named cells starred.

C8. **V2 "ACCEPTED … 8 consecutive closes beyond the edge OR one close ≥ 1.5 ATR_L beyond · a probe that closes back inside
within K=3 closes = SWING FAILURE"; "X's semantics asserted equal on the 4h holdout sample"** (:35-36, :32-33). Disk: X's RECORD
is 8 closes only and ret_k = 7; the contract's machine = X's `die_parity` twin AND X's `k3` twin AT ONCE, a combination X never
ran (each `EP_LAWS` twin changes one field). The equality assertion against X's record will fail by construction; against which
X variant it is asserted is unstated. Also unstated: whether a close is judged against VA(t−1) (X's record) or VA(t)
(X's `self_inclusive` twin); and whether the edge is frozen at the probe's first close (X) or live.

C9. **"stop beyond the deviation extreme, railed ≥ 1.0 ATR_4h"** (:71) and **"STOP: beyond the deviation extreme if the trigger
was a swing failure, else 0.5 ATR_1h beyond the edge; railed ≥ 1.0 ATR_1h"** (:97-98). Disk: "beyond" has one filed meaning,
`STOP_BUF_ATR = 0.5` ATR (`spring_stop`). For the scalper's cross trigger the entry IS the edge, so "0.5 ATR_1h beyond the edge"
gives R = 0.5 ATR < the 1.0 rail: **the rail always binds and R ≡ 1.0·ATR_1h**; the 0.5 clause is arithmetically dead.

C10. **"TARGET 1 = POC (half off)"** (:71, :99). Disk: X2's T1 is the pre-redraw box MID, and X2 refuses a trade whose T1 is
within 10 bps of entry or behind it (`geometry`). A POC can sit anywhere in the value area, including on the entry side of the
entry price (P-SFP-VA-1 enters at a CLOSE back inside, which can be beyond the POC) or beyond T2 (POC within 0.25 ATR of the far
edge → targets inverted). The contract has "rr-min" at T2 only; nothing for a degenerate T1.

C11. **"INVALIDATION = acceptance beyond the faded edge"** (:72-73) / **"invalidation on acceptance beyond the edge regardless
of stop"** (:98). Disk: X2's range-death exit is a TWIN, not the record, and no code exits on a VA acceptance. Exit price/instant
unstated (the filed analogues exit at the close that prints the event, taker: `range_death` in `TAKER_EXITS`; L-S.2 "Exit at that
1h close (the coincident 5m close), taker").

C12. **"COSTS OF RECORD: maker bps per side on entry and targets; taker on the stop"** (:101). Disk/contract silent on the TIME
STOP and INVALIDATION legs; X's filed law makes them taker (`TAKER_EXITS`). P-SFP-VA-1's entry is "at the close back inside"
(a market act) yet its "maker twin" is asked for (:75) — X2's two maker readings ("fill assumed" at the close price vs "fill
conditioned" on the next 5m child) both exist; which is "the maker twin" is unstated.

C13. **"TWINS on every row: all-taker (the TC-series toll) · charter slippage"** (:102). Disk: two charter forms exist for a
maker book — `haircut_net_r` (AM-7 on the all-taker book: slippage on EVERY fill) and `stop_leg_slip_haircut_net_r` (AM-7 on the
maker book's taker legs only, since "a maker leg carries zero slippage").

C14. **"ENTRY: a limit order AT the edge, valid 12 five-minute bars from the trigger close"** with **TRIGGER "a 5m EMA12/EMA89
cross … while price is within 0.25 ATR_1h of the edge"** (:89-92). Disk: no resting-order model. "Within 0.25 ATR_1h" is
two-sided as written: a trigger close BEYOND the edge (below VAL for a long) makes a buy limit at VAL MARKETABLE — it cannot be
a maker fill, yet the through-tick test would pass on the very next bar.

C15. **"MISS COLUMN first-class: every unfilled order counted and its would-have outcome printed at both targets"** (:95-96).
Disk: misses are refusal rows with no outcome. "Would-have" has no filed definition (enter where? at the limit as if TOUCH-filled,
or at the trigger close as a taker?).

C16. **"P-SCALP-3 … (vs zero; HOLDOUT era ["era"])"** (:83) vs **Stage C "the extension printed separately (the forward strip,
never scored)"** (:48-50). Disk: holdout = close > 1719791999000 with no upper end other than the corridor pin; TC11/X's pin is
2026-09-25T00:00Z and X's 1h-maker licence was measured on that corridor. Whether the scalper's scored holdout runs to TC11's pin
or TC12's is unstated. Also unstated: which instant carries the era (trigger close vs fill bar).

C17. **"REGIME COLUMNS: 1h ATR tercile (trailing)"** (:102-103). Disk: one filed trailing-percentile law
(`tc11x_pct`, window 2000, floor 300, integer thirds) and L-S.2's "trailing 2,000-bar quantiles … ending at the entry bar
inclusive"; fine, but it lives only in X.

C18. **"Label: direction informed by TC11 R5 (+0.49 with / −0.49 against, pivot states)"** (:67). Disk: exact —
+0.491349 (n 47) / −0.493933 (n 12), calibrated scale, 4h, v6 book. Note n = 12 on the "against" side, and the frozen-3.0
4h twin reads +0.237982 / −0.573981.

C19. **P-DIR-1 "Tier-E: the full VA chop table — v6 by 4h and 1d VA state × %-of-value decile at entry"** (:67-68). Disk: R5's
lenses are 4h and 12h (`R5_LENSES`), pivot states; deciles `[0,10)…[90,100)` + `<0`, `>=100`, not-in-range by state. Reusable law,
different state alphabet (INSIDE / PROBING ± / ACCEPTED ±).

C20. **"The 1d VA edge as a continuation take-profit venue (v6 remainder at 0.25 ATR_1d of the 1d edge when 1d is INSIDE) —
paired"** (:79-80). Disk: P-TP-RNG's machinery is exactly this shape at 12h pivot boxes; its law has three extra clauses the
contract line omits (near-side rule, the 10 bps entry-side guard, as-of at the 4h bar's OPEN).

C21. **F-SFP "3 trades hand-walked incl. a POC fill and a time-stop exit"**, **F-SCALP "3 scalps hand-walked end-to-end + 3
MISSES verified"** (:119-120). Disk precedent (X F-SFP): the three trades are "chosen by a frozen rule, never after a look"
(first T1 fill, first other stop, first other time stop, key order). The contract does not state the selection rule.

C22. **Stage S "five home assets; both directions"** and no word on concurrency. Disk: X's one-position law covers open TRADES
only; a pending (unfilled) limit order is a new state with no filed law (does it block a later trigger? does a new trigger
replace it?).

---------------------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans; each must be frozen before any book is built)

**R-1 · TICK OF RECORD.** Q: which tick? Options: (a) `price_tick` from TC11's `CONTRACT_SPECS.json`; (b) `price_tick` from a
CONTRACT_SPECS re-captured by TC12's Stage D at TC12's pin; (c) an empirical per-era tick inferred from the tape.
**Recommend (b)**, falling back to (a) only if Stage D does not re-capture, read by key, never typed, with the on-grid share per
asset × era printed beside every fill table and the SOL regime disclosed. Why: a filed venue record, and for CLASSIC5 the snapshot
tick is ≥ every historical tick seen on the tape (BTC, SOL, NEAR coarsened over time), so it is the STRICTER fill test — it cannot
flatter. (c) introduces an inference rule nobody ratified.

**R-2 · THE THROUGH-TICK INEQUALITY AND ARITHMETIC.** Options: (a) `low <= limit − tick` ("by ≥ 1 tick"); (b) strict
`low < limit − tick` (the contract's parenthesis). **Recommend (b)**, evaluated in exact arithmetic (Decimal from the
`price_tick` string, or integer ticks), not float subtraction. Why: the parenthesis is the operative formula, and it is the
stricter one. Mirror for targets: `high > T + tick` long.

**R-3 · THE LIMIT PRICE.** Options: (a) the raw edge float; (b) the edge rounded to the tick grid AWAY from the market
(long: floor to grid; short: ceil); (c) rounded toward the market. **Recommend (b)** for the order price and the booked fill
price, the raw edge printed beside. Why: a real order sits on the grid; rounding away is the harder fill; (c) flatters.

**R-4 · DEEP TWIN.** Options: (a) through by `0.05·ATR_1h` as written; (b) through by `max(0.05·ATR_1h, 1 tick)`.
**Recommend (b)** and state TOUCH ⊇ TICK ⊇ DEEP as a per-order SET inclusion the fixture asserts. Why: under (a) NEAR inverts
on 18.25% of holdout hours and F-SCALP's ordering leg can go RED for an arithmetic reason, not a model one.

**R-5 · MARKETABLE-AT-TRIGGER ORDERS.** Q: a cross trigger whose 5m close is beyond the edge. Options: (a) place the order
anyway; (b) no order — counted `refused_marketable_at_trigger`; (c) the trigger requires the close on the value side
(`0 <= (close − VAL)·d` and within 0.25 ATR_1h). **Recommend (c)≡(b) with the count printed.** Why: a marketable limit is a
taker fill; booking it at maker bps under a "through" test that passes instantly is the one way the fill model can flatter.

**R-6 · ORDER GEOMETRY FROZEN AT THE TRIGGER.** Options: (a) edge, POC, far edge, ATR_1h frozen at the trigger close (as-of the
last 1h bar closed at or before it); (b) re-read at each 1h close during validity and after the fill. **Recommend (a)**; the
live-edge reading as a Tier-E twin (X precedent: frozen E of record, `live_edge` / `live_far_t2` twins).

**R-7 · VALIDITY WINDOW AND CANCELLATION.** Options for "12 five-minute bars from the trigger close": (a) bars t+1 … t+12
inclusive; (b) t … t+11. **Recommend (a)** (the trigger bar has closed; it cannot fill). Cancellation "on acceptance beyond the
edge": judged at each 1h close inside the window by the V2 machine; a fill and a cancelling 1h close on the same 5m bar →
the fill stands only if it is decided before the close (it is: the fill is intrabar, the acceptance is a close event), and the
invalidation exit then fires at that same close. Print the count.

**R-8 · THE AS-OF JOIN OF 1h/4h/1d ONTO A 5m BAR.** Options: (a) `C.asof_index` with instant = the 5m bar's CLOSE for decisions
taken at that close (permission, setup, trigger), and instant = the 5m bar's OPEN for anything that must rest DURING the bar
(a live level, a cancellation already known); (b) `engine.htf` law everywhere (HTF close ≤ 5m OPEN). **Recommend (a)**, stated
as one function with the instant named, and F-NEST-ASOF planted on the boundary case (a 1h bar closing exactly at the 5m close:
visible to a decision AT that close, not to an order resting during that bar). Why: it reuses the filed TC11 nest law and the
filed TP-hook law, each where it was proven; (b) throws away the hour-close bar the contract's "at the last 1h close" names.

**R-9 · 5m EMA12/EMA89.** Options: (a) `ind.ema` on the FULL 5m tape (seeded at the first bar), `ind.crossover/crossunder`,
readable only from bar index ≥ 89 (the lineage warm floor); (b) a windowed/SMA-seeded EMA. **Recommend (a)** — the engine's own
function, the same pair TC11's warn used at 1h (`warn_of(…, 12, 89)`); the floor asserted (it cannot bind in the holdout: the 5m
tapes start 2019-09 … 2020-10). The cross must close ON the trigger bar; a cross earlier in the hour is not a trigger.

**R-10 · THE 5m SWING-FAILURE TRIGGER AND ITS EXTREME.** Q: "a 5m close back inside the 1h value after a 5m close beyond the
edge" — how long may the excursion be, and what is the deviation extreme? Options: (a) the first 5m close inside after a run of
≥ 1 CONSECUTIVE 5m closes beyond the (frozen-at-run-start) 1h edge, extreme = min low / max high over the run INCLUDING the
return bar; no extra K, because the PERMISSION (1h INSIDE at the last 1h close) already bounds a run to one hour; (b) reuse
"sfp-k" = 3 on the 5m clock. **Recommend (a)**. Why: no new typed constant; the K=3 veto names the lens-L machine, not the 5m
timing rule; "the 5m is never a signal source" argues against importing a 5m state machine.

**R-11 · STOP ARITHMETIC.** Options: (a) `BK.brk_stop(d, ext, i, entry_px, ATR_L)` unchanged (0.5·ATR beyond the extreme,
railed 1.0·ATR) — for the scalper's cross trigger pass `ext = edge` and print that the rail binds on every such row
(R ≡ 1.0·ATR_1h); (b) a new stop function. **Recommend (a)**. ATR_L = the lens ATR at the event bar (P-SFP-VA-1: `atr_4h[t]` of
the return bar; P-SCALP-3: ATR_1h of the last 1h bar closed at or before the trigger close). `entry_px` for R = the limit price.

**R-12 · DEGENERATE TARGETS.** Options: (a) adopt X2's refusal law verbatim (T1 or T2 within the FIXED 10 bps of entry, or
T2 not beyond T1 → refused and counted) then apply "rr-min"; (b) T1-collapse (whole position rides to T2 when the POC is behind
or at the entry); (c) apply only "rr-min". **Recommend (a) of record with (b) as the printed twin** — both are filed X laws;
(c) lets a "half off at entry" trade through.

**R-13 · "rr-min".** `(T2 − entry)·d >= 1.5 × r_dist`, evaluated at the trigger/entry with frozen geometry, AFTER the rail.
Options for the scalper: entry = the limit price (recommended) vs the trigger close. For "the unfiltered twin printed": the
same book without the rr-min skip, Tier-E, and both books keep their own one-position sequence (X precedent: RIDDEN twins
re-walk with their own sequence) — say which. **Recommend: re-walked, own sequence, labelled.**

**R-14 · SAME-BAR ORDER ON THE WALK.** **Recommend X2's `bar_step` law verbatim** (OPEN decides → STOP adverse-first at the stop
→ T1 → T2 same bar → close events), with close events ordered INVALIDATION → TIME STOP (label only; same price), on the lens bar
for P-SFP-VA-1 (4h) and on the 5m bar for P-SCALP-3. Twin: X2's `child5m_sequencing` for P-SFP-VA-1's ambiguous 4h bars.
For the scalper the record walk is already the finest clock on disk; nothing sequences inside a 5m bar (state it).

**R-15 · FILL-BAR LAW (scalper).** **Recommend X's fill-child law**: on the fill bar the stop is tested adverse-first, no target
is credited; funding booked from the fill bar (`fund_entry_i = fill_i`); targets rest from fill_i + 1.

**R-16 · TARGET FILL RULE.** T1 "same fill rule" is explicit; T2 is silent. Options: (a) T2 through-tick too; (b) T2 touch.
**Recommend (a)**. Gap law for a through-filled target: fill AT the level (no gap improvement — X's `symmetric_gap` choice),
since a resting maker order filled through a gap still books its own price; the `max(level, open)` form printed as a twin.

**R-17 · TIME STOP ON THE 5m CLOCK.** Options: (a) exit at the close of 5m bar `fill_i + 12·T_1h` (T_1h = V4's 1h value);
(b) at the T-th 1h close after the fill; (c) clock from the trigger bar. **Recommend (a)**: a pure 5m clock anchored at the fill,
no hour-alignment dependence; `12` is `LENS_MS["1h"] // LENS_MS["5m"]` read by object, never typed. P-SFP-VA-1: the close of
4h bar `entry_i + T_4h` (X2's law).

**R-18 · V4 SOURCE.** The traverse must be computed on the VALUE AREA (new), on which window? Options: (a) tuning-era head only,
pooled CLASSIC5, `ceil(median)` (X's `t_pin` law, causal for the holdout); (b) whole corridor; (c) trailing per trade.
**Recommend (a) of record, (c) as the fully causal twin** (X precedent: `frozen3_0_trailing_t`), and X's pivot T (13 / 13) printed
beside as the continuity column. (b) leaks the holdout into the scalper's own time stop.

**R-19 · COST LEGS.** **Recommend X's `TAKER_EXITS`**: entry, T1, T2 maker (`maker_bps_side`); stop, time stop, invalidation,
corridor-end mark taker (`taker_bps_side`); zero slippage on the maker book; booked per fraction (`fee_per_fraction`), with
F-TOLL = the per-fraction booking at all-taker bps == `account_l` to 1e-12 R.

**R-20 · THE TWO TWINS' NAMES.** "all-taker" = `account_l`'s `net_r` on the SAME fills (same path, taker bps on every leg).
"charter slippage": options (a) AM-7 on the all-taker book (`haircut_net_r`: slippage on every fill); (b) AM-7 on the maker
book's taker legs only (`stop_leg_slip_haircut_net_r`). **Recommend printing both, with (a) named "charter" on the row** — it is
the harsher, and it is the form every TC-series row already carries.

**R-21 · "THE MAKER TWIN" OF P-SFP-VA-1.** Options: (a) fill assumed at the entry close (maker bps on entry/T1/T2);
(b) fill conditioned on the next 5m child trading strictly through the close (X's `maker_conditioned`), misses counted.
**Recommend both printed, (b) named first** (X ruled (b) the honest one: 90.3-95.3% of 5m bars trade through the prior close,
`LEANS_X.md:568-571`).

**R-22 · MISS / WOULD-HAVE.** Options: (a) a taker entry at the TRIGGER close with the same stop and targets, walked by the
same law, printing reached-T1 / reached-T2 / stopped / time-stopped and all-taker net R; (b) an entry at the limit as if
TOUCH-filled. **Recommend (a)**, with misses split into touched-not-through and never-touched (the latter cannot be given (b) at
all). Why: it is the only counterfactual executable at decision time, and it is what "the edge ran away without us" means.
Label the block Tier-E, never netted into the book.

**R-23 · ONE POSITION / ONE ORDER PER ASSET.** **Recommend**: X's `blocks` law for open trades (`entry_i < b <= exit_i`), plus
one resting order per asset — a trigger while an order rests is refused and counted (no replace, no stacking); a trigger on the
bar an order expires may place a new one. Rival counted: replace-with-newest.

**R-24 · ERA INSTANT AND CORRIDOR END.** Options: era by (a) the TRIGGER close (the decision instant); (b) the fill bar's close.
**Recommend (a)** (`E.era_of`; an order triggered in tuning is never a holdout trade). Corridor: options (i) holdout through
TC12's pin; (ii) through TC11's pin with the top-up strip printed apart. **Recommend (i) of record with the two slices printed
beside** — the strip after 2026-09-25T00:00Z is the only part X's licence never saw. An order or trade open at the pin: X's
LX-X2.17 (marked at `c[hi]`, listed OPEN; drop-OPEN twin; an unfilled order at the pin = `fill_unresolved_at_pin`, not a miss).

**R-25 · OUTER THIRD.** `%-of-value` of the trigger 5m close against the frozen 1h VA: long iff `pct <= 33`, short iff
`pct >= 67` (the contract's literals). Options for `pct < 0` / `> 100` (close beyond the edge): moot under R-5(c) for the cross
trigger; for the SFP trigger the close is inside by definition. **Recommend: require `0 <= pct <= 33` (long), mirror short**,
on-the-cut counts printed (R5's SR-16 disclosure precedent).

**R-26 · PERMISSION CLOCK.** "1h state INSIDE (no probe/acceptance at the last 1h close)" and "4h state NOT accepted against":
both read as-of the trigger close (R-8), and **re-checked? no** — once at the trigger. Options: also re-check at the fill.
**Recommend trigger-only**, with "permission lost before the fill" counted (cancellation already covers acceptance).

**R-27 · P-SFP-VA-1's EVENT.** Which machine emits the swing failure: the contract's V2 (K=3, acceptance 8 OR 1.5 ATR) — yes;
but V2's reference (VA(t−1) vs VA(t)) and edge (frozen vs live) must be frozen first (C8). **Recommend X's record on both
(`ref="prev"`, `frozen=True`)**, i.e. V2 := `EpLaw(ret_k=3, die_parity=True)`, a dated amendment naming the two fields that differ
from X's record, and the F-STATE equality asserted against X's episode function RUN with those two fields (not against X's
filed record table). Entry = the return bar's close; `ext` = the episode `extreme`; faded edge = the frozen `E`;
T1 = POC(t−1) or POC(t)? → the same reference as the edge (**recommend the VA the episode was judged against**).

**R-28 · INVALIDATION EXIT.** **Recommend**: at the lens close that prints ACCEPTANCE on the faded side for a NEW probe of the
same edge after entry (P-SFP-VA-1: a 4h close; P-SCALP-3: a 1h close = the coincident 5m close), taker, after the intrabar
STOP/targets of that bar.

**R-29 · THE NULL FOR THE VA TWO TRADES.** Options: (a) gaps+order on VA VALUE REGIMES (regime lives and gaps permuted through
`NL.schedule`, the VA-shaped static box replaying the two trades) — literally R10, new plumbing; (b) X's VA null of record
`tr_tercile_lblock` labelled as such; (c) both. **Recommend (c): (a) built because the contract names it, (b) beside because it
is the filed VA null**, K = `NL.K_DEFAULT` by object, `NL.PCTILE_LAW`, RNG `NL.draw_rng(SEED_TC12, draw, asset, lens, tag)`.
If (a) cannot be built without inventing a box definition, HALT for an amendment rather than relabel (b) as "gaps+order".

**R-30 · L+1 CONDITIONING CELLS.** **Recommend the whole partition with the three named cells starred** (TC11 L-R.6 precedent),
on VA states: ACCEPTED aligned ★ / ACCEPTED counter / INSIDE at own edge (coincidence, 0.25·ATR_L inclusive) ★ / INSIDE mid
(pct ∈ [25, 75], not coincident) ★ / INSIDE other / PROBING / no VA.

**R-31 · 1d TP VENUE.** **Recommend P-TP-RNG's law unchanged** with the 1d VA in place of the 12h box: as-of the 4h bar's OPEN,
level = far VA edge ∓ 0.25·ATR_1d, near-side rule, 10 bps guard, fill `max(level, open)`, order STOP → TP → BELL → HARVEST →
TRAIL, paired vs v6 with the identity law; D15 tail ratio on the row (the wall-exit risk).

**R-32 · PRECONDITION RECORD FOR F-FAM.** Q: what could close P-SFP-VA-1 / P-SCALP-3 "by precondition"? **Recommend**: each
registration names its licence row in X's `va/feasibility.parquet` (4h taker; 1h maker) by path + sha; the row is re-derived from
its printed columns by the Q-R3 law (Stage S's `legs_of` pattern); STATUS = BUILT iff PASS else CLOSED_BY_PRECONDITION with no arm;
the scorer cross-checks STATUS against the record. F-FAM's "spends no test" leg is then proven on a PLANTED failing licence row,
since the real rows pass or F-VA-MIRROR HALTs.

**R-33 · FIXTURE TRADE SELECTION.** **Recommend X's frozen rule**: in (asset, entry) key order — the first T1/POC fill, the first
other stop, the first other time stop; scalper: the first of each fill class + the first three misses (one touched-not-through
if any). Declared before any book exists.

---------------------------------------------------------------------------------------------------------------
## 4 · HAZARDS

H1. **Importing X code from the X worktree.** Putting `X/scripts` on `sys.path` would (i) write `__pycache__` into the certified
tree unless `-B`/`PYTHONDONTWRITEBYTECODE=1` is set in EVERY process incl. fork-pool workers and fixture subprocesses,
(ii) arm X's audit hook and re-root TC10 modules a second time (X's `tc11x_env` and TC11's `tierc11_env` each rebind `C.LENSES`,
`C.toll_bps_for`, fee paths — `tierc11_nest.py:139-186`, `tc11x_ranges.py:381-460`), (iii) make TC12's import closure span two
trees. The X tip must not gain a file: `git -C X status` shows only `?? research_outputs/tierc11x/close/CERTIFIED_TIP`.

H2. **Module-level memos keyed without the corridor.** `tierc11_ride._H1/_WALKS` (:279-280), `BK._FRAMES/_ROLES/_FRACTALS/_ANCHORS`
(`tierc10_brk.py:902-905`), `tc11x_sfp._CTX/_FIVE`, `E._FEES`, `R._PINS`. A process that loads TC11's corridor and then TC12's
extended one (F-CTRL does exactly that) can be served the first tape. One corridor per process, or the pin in the key.

H3. **`ctx_of` HALTs unless the last bar closes at the pin** (`tc11x_sfp.py:407-409`) and `load_x` HALTs unless the tape's pin is
TC11's (`tc11x_ranges.py:595-600`). Vendored code carries TC11's `PIN_MS`; on TC12's corridor these guards fire (good) or, if
loosened carelessly, pass a mixed-pin tape.

H4. **Look-ahead at the 5m↔HTF seam.** (i) A 1h VA/ATR stamped at the 1h bar that CONTAINS the 5m bar (off-by-one in the as-of
index: `side="left"`, or comparing against the 5m OPEN for a decision at the CLOSE and vice versa). (ii) `ATR_L[j]` contains
`TR[j]` — a level set from the ATR or the VA AT a fill bar knows that bar's range (X's rejected live-T2 draft,
`LEANS_X.md:1194-1196`). (iii) The self-inclusive VA(t) used to judge close[t] (X's twin, not its record). (iv) V4 fitted on the
whole corridor then used as the holdout time stop. (v) An hourly permission read at a 1h close LATER than the trigger. (vi) A
REPR/walkability test that reads later children of the same parent to decide an earlier act (TC11 AM-5 discloses this for
L-W.0; 16 corridor bars).

H5. **Tick arithmetic.** `limit − tick` in binary float with ticks like 0.10 / 0.01 / 0.001 mis-decides exact-boundary lows;
on-grid lows are the common case (holdout on-grid share 1.0 for BTC/ETH/NEAR/ZEC). Use Decimal/integer ticks. And the snapshot
tick is not the historical tick (SOL inside the scored era; isolated off-grid prints through 2026-08-29).

H6. **Marketable limits booked as maker** (C14 / R-5), and **targets credited on the fill bar** (X's withheld count exists for
this reason: `fillchild_target_withheld` 19 on the 1h conditioned book).

H7. **DEEP looser than TICK on NEAR** (C3 / R-4): F-SCALP's ordering leg could go RED, or — worse — the PRE-NAMED KILL
("CLOSED FOR GOOD if it fails under DEEP too") would be read on a twin that is not uniformly deeper.

H8. **Fee keys.** The contract's `maker_bps_side` is the READER's key; the file's is `maker_bps_per_side`. If Stage D adds a new
`data/fee_schedule.json` with a differently named or per-venue key, `E.fees()` (which reads `OUT/"data"/"fee_schedule.json"` under
`research_outputs/tierc11/`) keeps serving TC11's 2.0 silently. F-TOLL must assert the value consumed == the value in the file
TC12 pins, by path + sha. A changed maker rate also moves the 1h licence (`va/feasibility` maker rows were struck at 4.0 bps
round trip): if "maker-bps" lands ≠ 2.0, F-VA-MIRROR's "1h maker PASS" is a statement about a different toll.

H9. **`account_l` has ONE fee rate and reads `card.harvest_frac` / `card.funding_ceiling_r`** from the card object passed. A card
other than `TP.CONTROL_CARD` silently changes the half and the cap. Funding accumulation order is load-bearing for bit-identity
(1.665e-16). Float association: the per-fraction maker booking is NOT bit-equal to `account_l` (tolerance 1e-12 R is the filed
law; do not "fix" it to exact).

H10. **Determinism.** Sort keys before any write; the null's RNG must stay `default_rng([seed + draw, crc32(...)])` (never
`hash()`); EMAs/ATRs on the FULL tape (a windowed tape reseeds them); `pd.read_parquet` on path strings only (AM-2: pyarrow
native readers escape the audit hook); no clock field in any artifact; fork-pool row order fixed before writes.

H11. **Frozen records.** TC12 reads but must never rewrite: `MR/**` (registry head `6772568b…`, LEANS sha pinned inside
REGISTRATIONS.json), `M/research_outputs/tierc10/**`, `XR/**`. `MR/regbooks/P-SCALP-2/` must keep holding STATUS.json ONLY
(Stage S's STRAY-BOOK HALT) — P-SCALP-3's book belongs under `research_outputs/tierc12/`, and P-SCALP-2 is NOT reopened by it
(TC12 "no re-family of TC11"; the TC11 1h PIVOT maker twin read FAIL — the licence is X's VA row, a different detector).

H12. **Operator's pending close acts.** `M/research_outputs/tierc10/close/close_acts.sh`, `MR/close/close_acts.sh`,
`XR/close/close_acts.sh` are unrun; `git -C M status` shows ` M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`
and ` M exchange/status/daily/DAILY_2026-10-08.md` uncommitted. TC12 staging must add only tierc12 paths (TC11's L-0.5 law) and
must not `git add -A`, stash, or touch `exchange/status/LEDGER_*`, `exchange/reports/` of prior tiers.

H13. **Selection contact.** I printed R5 (already disclosed by the contract) and X2's filed grid means (all filed, Tier-E).
`XR/va/two_trades.parquet` holds the filed VA swing-failure H20/H100 terms per lens × era × direction (e.g. the 4h and 1d
record cells) — the executor will meet them when mirroring; P-SFP-VA-1's label should say the class was seen there.
I computed nothing on the scalper's trigger population.

H14. **One-position sequencing changes the trade SET across twins.** X's ridden twins each re-walk with their own sequence, so
"the same trade under another fill rule" is not a paired comparison (1h record 2,408 vs conditioned 2,321 vs t1_collapse 2,439).
The TOUCH ⊇ TICK ⊇ DEEP inclusion must be asserted on ORDERS (per trigger), before one-position sequencing, or it will not hold.

H15. **`ride11` cannot carry a time stop** (`scope` HALTs) and its TP is TOUCH at `max(level, open)`; using it for the 1d TP venue
is right, using it for any range trade is wrong.

---------------------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import unchanged from MAIN (through the TC12 env shim, as TC11 did):**
- `BK.frame_l(sym, lens)` / `LensFrame` (5m, 1h, 4h frames + funding), `BK.account_l`, `BK.funding_interval`,
  `BK.brk_stop`, `BK.FLIP_HOLD_MARGIN / FLIP_HOLD_BARS / MEM_TTL_BARS` (AST-read pins) — `scripts/tierc10_brk.py`.
- `ind.ema / atr / crossover / crossunder` — `engine/indicators.py`. `C.asof_index` — `scripts/tierc10_census.py:894`.
- `NL.K_DEFAULT, draw_rng, schedule, static_box_machine, null_view, PCTILE_LAW, real_box_set` — `scripts/tierc10_null.py`.
- `T5.cluster_boot, cluster_boot_diff, _ci_from` (`scripts/tierc5.py`), `TP.loao_n`, `TP.make_put / stamp_n / check_keys /
  check_det / grid_whole` (`scripts/tierc10_panel.py`), `E.fees()`, `E.era_of()` (re-pointed at TC12's fee file and pin).
- `tierc11_ride.ride11(tp=TPLevels)`, `transform_book`, `identity_findings` + `tierc11_stage_h.levels_from_facts /
  asof_12h_index` pattern — ONLY for the Tier-E 1d-VA take-profit venue (paired vs v6).
- `tierc11_stage_r`: `bucket_of`, `align_of`, `r5_chop`, `r5_direction`, `r5_direction_partition`, `_stats`, `_cell`,
  `entry_frame` — MIRROR for the VA chop table (new state alphabet, lenses 4h and 1d); R5's filed table read by path + sha for the
  label. `tierc11_stage_s`: `legs_of`, `record_verdict`, `gate_opens`, `cross_check`, `status_record` and
  `tierc11_score.precondition_record` — MIRROR for the licence gate + STATUS plumbing (R-32).
- `tierc11_books_fixtures.price_tick` — mirror as a production reader (R-1).

**Vendor by copy from X (sha in the filename, README, never imported from the worktree) — or mirror with a parity fixture:**
- `tc11x_sfp.py`: `bar_step`, `_hit`, `_fill`, `walk` (minus harden/redraw specifics), `fee_per_fraction`, `book_trade`,
  `blocks`, `ride` (event → one position → trades skeleton), `trade_row` schema, `refusal_row`, `derived`, `ci_of`,
  `children`, `repr_ok`, the `Law` dataclass + twin table. Parity fixture: the vendored walk re-rides X2's filed
  `X2_trades_4h.parquet` (588 rows) / `X2_trades_1h.parquet` (2,408) from X's own event list to 0 mismatches — the same check
  X-REVIEW ran — which proves the copy before it is pointed at VA events.
- `tc11x_pct.py` (pure; 124 lines) — vendor whole for the ATR-tercile regime column.
- `tc11x_va.va_episodes / EpLaw / scan_retests / retest_verdict` — the VA scout's unit; U6 consumes `episodes[]`
  (`side, t0, E, extreme, end_i, end_kind`) and the retest holds.
- `tc11x_ranges.t_pin` (ceil-median integer law) for V4; `time_stop_of`'s trailing-T table pattern for the causal twin.

**Newly written (nothing on disk to reuse):**
1. The resting-limit ORDER model: order record (trigger_i, side, limit, expiry_i, tick, status), validity window,
   cancellation on acceptance, the three fill rules TOUCH / TICK / DEEP evaluated per ORDER on the 5m tape, exact tick arithmetic.
2. The 5m range-trade walk for P-SCALP-3 (bar_step on 5m bars, fill-bar law, 5m time-stop clock, invalidation at the
   coincident 5m close) and its account on `BK.frame_l(sym, "5m")`.
3. The 5m trigger: EMA12/EMA89 cross + proximity; the 5m close-back-inside run and its extreme.
4. The 5m ← {1h, 4h} as-of stamper for VA state / %-of-value / ATR_1h / POC / edges (one function, the instant named).
5. The MISS table with would-have outcomes at both targets; the fill-sensitivity block that is part of the verdict text.
6. Maker-of-record booking where the MAKER row is `net_r` (X had it as a twin) + the all-taker and charter twins on every row;
   one home for the AM-7 haircut function.
7. V4 traverse table on the value area (+ F-TRAV's AST leg, mirroring F-TRAVERSE).
8. VA-state L+1 conditioning cells; the VA chop table; the gaps+order null on value regimes (R-29).
9. P-SFP-VA-1's geometry (POC T1, far edge − 0.25·ATR T2, rr-min, invalidation) on VA episodes; the 1d cell, the
   1d-direction-guarded twin, the holdout slice.
10. F-SCALP / F-SFP / F-TOLL / F-FAM fixtures, each with its stated failure condition and plants.
