# TIER-C11 SCOUT · SUBSYSTEM B — THE CAMPAIGN ENGINE (v6 card, 9/12 card, lanes)

Scout: read-only map for HEPHAESTUS. Contract of record: `exchange/queue/2026-09-24_TC11_APOLLO.md` (103 lines, read in full).
Branch `v12-v1-census`. Line numbers are from the tree as of 2026-09-24. Counts marked **[measured]** were computed by this
scout on snapshot `tc10_20260921` (as-of 2026-09-21T16:00Z, corridor 2019-09-08T16:00Z → 2026-09-21T16:00Z) with read-only
probes. They are descriptive counts of the filed control, not results.

Run preamble (every TC10 module assumes it; `tierc2_baseline` binds cache paths AT IMPORT):
```
export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
~/venvs/naiad/bin/python scripts/<tc11 script>.py
```

---------------------------------------------------------------------------------------------------------------------
## 0 · THE IMPORT LINEAGE (what calls what)

```
tierc10_panel (TP)  ── run_cell_n ──> tierc9.replay9 (T9) ──> tierc9._ride_leg9 ──> tierc8.matched_step (trail)
                                                          └──> tierc7._account_chain (fees/funding/ceiling)
tierc10_lanes (LN)  ── run_lane  ──> LN.replay10 ──> LN._ride_leg10 (= _ride_leg9 + BE-floor branch)
tierc10_brk  (BK)   ── brk_campaigns ──> BK.ride_leg_l (lens-generic _ride_leg9) ──> BK.account_l (interval-sum funding)
frames:   T9.frame = T7.frame = T6.frame = tierc5.frame (tierc5.py:116)  — 4h only, memo on BARE SYMBOL
rules:    tierc7_rules (RC) re-exports tierc6_rules → tierc5_rules → tierc4_rules → tierc3_rules → tierc2_rules
engine:   engine.indicators.{ema, atr, crossover, crossunder} · engine.s1._pivots (s1.py:100) · engine.htf.map_htf_to_exec (htf.py:15)
```
`import tierc10_lanes` / `tierc10_brk` also imports `tierc10_data`, whose `assert_substrate()` (tierc10_data.py:94-117) HALTs at
import unless `NAIAD_CACHE_DIR` is EXACTLY `~/.cache/naiad/snapshots/tc10_20260921`. `tierc10_panel.substrate()` (panel:161)
only refuses the live cache.

---------------------------------------------------------------------------------------------------------------------
## 1 · THE BASE v6 CARD, END TO END

Object of record: `TP.CONTROL_CARD = tierc8.Card(name="v6-control")` (panel:816) ridden with `T9.V6_ROLES = Roles()` (tierc9.py:119).
Full field dump of CONTROL_CARD **[measured]**:
```
grid='card' entry_rail_atr=1.0 lane='card' limit_ae_mult=None trail=True trail_l=2 trail_r=2 trail_extra_buf_atr=0.0
trail_arm_after_r=1.0 harvest='band' harvest_fixed_r=2.0 harvest_min_unit_r=-inf time_stop_bars=None funding_ceiling_r=1.0
adds_max=0 add_size=1.0 seal_open=True trail_min_advance_atr=0.05 harvest_frac=0.5 wall_exit_atr=None wall_tf='12h'
hybrid_anchor=False weave=False reentry=False ae_abort_r=None weave_k=6 stop_grid_offset_atr=0.0 anchor_kind='pivot' anchor_offset=0.5
```
`Roles()` (tierc9.py:93-117): `tide_f=89 tide_s=316 win_f=12 win_s=89 trg_f=12 trg_s=26`; `floor_bars = max(316, max(periods)) = 316`.

Constants (all by object) **[measured]**: TIDE 89/316 (tierc2_rules.py:65-66) · WINDOW 12/89 · TRIGGER 12/26 · D_DISPLACEMENT 0.75
(tierc2_rules.py:71) · ATR_LEN 14 Wilder RMA (`ind.atr`, indicators.py:53) · FEE_BPS_SIDE 5.0 (tierc2_rules.py:85) · PIVOT (5,5)
(tierc2_rules.py:94-99) · PIVOT_LOOKBACK_4H 200 (tierc3_rules.py:87) · STOP_BUF_ATR 0.5 · MIN_STOP_ATR 1.0 (tierc3_rules.py:98) ·
RATCHET (2,2) · HARVEST_FRACTION 0.5 · FUNDING_CEILING_R 1.0 · WARMUP_BARS 316 · PROVISIONAL_MIN_N 30 · ADDS_MAX 2 (tierc5_rules).
Lens: **everything is 4h**. EMAs are `engine.indicators.ema` seeded at series start (never NaN), which is why the 316-bar floor exists.

### 1.1 Arm / window (tierc9.armings9, tierc9.py:168-204)
- ARM = 4h `crossover(win_f, win_s)` (12/89) for long, `crossunder` for short, at bar `arm_i` with `lo_i <= arm_i <= hi_i`
  (`lo_i = max(corridor lo index, roles.floor_bars)`, replay9 tierc9.py:383).
- WINDOW runs from `arm_i` to `window_end_i` = index of the FIRST counter 12/89 cross after `arm_i` (EXCLUSIVE); `n` if none.
- TIDE gate evaluated ONLY at `arm_i` (tierc9.py:187-192): long iff `ema89[i] > ema316[i] AND close[i] > ema316[i]`; short mirror.
  Never re-checked at the trigger.
- D gate at `arm_i` (tierc9.py:193-196): `disp = |close - ema89(win_s)| / ATR14`, `d_ok = disp >= 0.75`.
- Record: `RC.Arming` (tierc2_rules.py:232-251): symbol, direction, arm_i, arm_ms, window_end_i, tide_ok, disp, d_ok, trigger_i,
  trigger_ms, entered, reject, strip_d_ok (+ in_window, entry_scored set by card_candidates9).
  `reject` ∈ {"tide", "d", "no_trigger", "position_open", "entered", ""} ("" on degenerate-ATR / no_struct_anchor paths).

### 1.2 Trigger (tierc9.card_candidates9, tierc9.py:207-231)
Gate order tide → d → trigger. Trigger = FIRST `crossover(trg_f, trg_s)` (12/26) in `[arm_i, min(window_end_i, hi_i+1))`
(tierc9.py:223-229) — the ARM BAR ITSELF IS ELIGIBLE (lag 0). **[measured v6 CLASSIC5]** 52/200 campaigns trigger on the arm bar.

### 1.3 Entry, one position per asset (replay9, tierc9.py:334-452)
Candidates sorted `(ti, -d, kind)`; `open_until = exit_i` of the open campaign; a candidate with `ti <= open_until` is refused
(`reject="position_open"`). Entry price = `close[ti]` (the trigger bar's close). Needs finite ATR>0.

### 1.4 Stop and R (tierc3_rules.struct_stop_4h, tierc3_rules.py:237-305; pivots tierc3_rules.py:205)
- Pivots: `engine.s1._pivots` strict (5,5) on 4h high/low; `conf = pivot_bar + 5` = bar at which it is knowable.
- Long: eligible lows with `conf <= ti`, `ti - conf <= 200`, `low < entry`; anchor = the HIGHEST such low (nearest below).
  `pivot_stop = anchor - 0.5*ATR[ti]`; `rail_stop = entry - entry_rail_atr(1.0)*ATR[ti]`; `stop = min(pivot_stop, rail_stop)`
  (the FARTHER one). Short mirrored with max.
- No eligible pivot → `None` → no trade (`no_struct_anchor`). The rail never invents a stop.
- **R = r_dist = |entry - stop|** in price units, fixed for the campaign's life (never re-denominated). `Stop` record (tierc3_rules.py:223)
  carries anchor, anchor_bar, pivot_stop_px, pivot_dist, rail_dist, r_dist, rail_binding, n_eligible.
- **[measured]** r_dist/ATR: min 1.0, median 1.62, max 7.47; rail-bound (==1.0 ATR) 49/200; `> 2.2 ATR` 53/200.

### 1.5 The ride (tierc9._ride_leg9, tierc9.py:236-331) — per 4h bar j = ti+1 .. hi_i, in this order
1. `fav/adverse` = high/low (long) of bar j; `ufav=(fav-entry)*d/R`. `mae=min(mae,uadv)` (tape, includes exit bar).
2. **+1R latch** (tierc9.py:274-277): `if not reached_1r: mae_to_1r=min(..); if ufav>=1.0: reached_1r=True` — taken at the TOP of
   bar j, BEFORE the stop test (the +1R bar's own adverse extreme counts as "before +1R").
3. **Trail arm** (278): `trail_armed` latches when `ufav >= card.trail_arm_after_r (1.0)`.
4. **Harvest touch computed** (281-293): armed once `close[j-1]` is strictly on the trade's side of the band's near edge
   (`RC.harvest_outside`, tierc4_rules.py:427); edge = `max(ema89,ema316)` long / `min` short (`RC.harvest_edge`, tierc4_rules.py:415);
   touch = intrabar `low_j <= edge` (long) / `high_j >= edge` (short) (`harvest_touched`, :445); `ufill >= harvest_min_unit_r (-inf)`;
   only if not yet harvested (max 1 per campaign).
5. **STOP** (296-301): `low_j <= stop` (long) → exit AT `stop`, reason `"stop"`. Adverse-first. Same-bar touch → `blocked="stop"`.
6. MFE update (held law: only on bars that survive the stop).
7. **BELL** (303-311): long: `crossunder(12,89)[j]` → `"bell_12_89"`, else `crossunder(89,316)[j]` → `"bell_89_316"`; short mirror;
   exit at `close[j]`. Same-bar touch → `blocked="bell"`.
8. **HARVEST record** (312-314): `harv=(j, close[j], unit_move_r)` — 50% (`harvest_frac`) off at bar j CLOSE. This is the
   contract's "de-risk at the opposing 89/316 band (law)": a pullback into the tide band's near edge.
9. **TRAIL** (315-323): if `trail and trail_armed`: `T8.matched_step(fr, j, d, stop, close_j, atr_j, s, "pivot", 0.5, open_ms,
   min_advance_atr=0.05)` (tierc8.py:192-252). Fires only on bars where a (2,2) fractal CONFIRMS at j (pivot bar j-2, low for long).
   `cand = pivot - 0.5*ATR_j`, `rail = close_j - 1.0*ATR_j`, `admitted = min(cand, rail)`; must be `> stop` and move `>= 0.05 ATR`.
   New stop governs bar j+1 onward. Fractals: `T9.fractals(sym,2,2)` → `tierc5_rules.build_fractals` (tierc5_rules.py:341).
10. End of loop without exit → `exit_i=hi_i, exit_px=close[hi_i], exit_reason="corridor_end"`.

Exit reasons in v6: `stop` (initial or trailed; `ratchet_exit` flags trailed), `bell_12_89`, `bell_89_316`, `corridor_end`.
**[measured]** v6 CLASSIC5: 200 campaigns; stop 195 · bell_12_89 4 · corridor_end 1 (ETH entry 2026-09-18T08:00Z, open at as-of);
harvested 55; reached_1r 103.

### 1.6 Accounting (tierc7._account_chain, tierc7.py:350-465) — see §6.

---------------------------------------------------------------------------------------------------------------------
## 2 · THE CAMPAIGN RECORD, AND THE PER-BAR PATH

### 2.1 `RC.Trade` = `tierc5_rules.Trade` (tierc5_rules.py:566-626), fields as replay9 fills them (tierc9.py:408-446)
```
symbol lane direction arm_i arm_ms entry_i entry_ms entry_px stop_px r_dist anchor anchor_bar_ms anchor_was_sealed
atr_at_entry disp_at_arming exit_i exit_ms exit_px exit_reason bars_held scored
advances(list[Advance]) final_stop_px stop_advanced_atr ratchet_exit
harvested harvest_i harvest_ms harvest_px harvest_unit_move_r harvest_blocked_by harvest_ride_would_have_r
adds(list[Add]) add_r spring limit_px limit_filled limit_fill_i
mfe_r mae_to_1r_r reached_1r gross_r fee_r funding_r funding_r_uncapped funding_ceiling_bound
net_r net_r_harvest_half net_r_runner_half net_r_bellonly
+ setattr extras (replay9): mae_r, n_opportunities, roles_name
+ setattr extras (replay10, lanes.py:973-988): card_name, be_on, be_reached, be_bar, be_order, be_why, be_exit,
  n_be_tie, n_be_mismatch, be_bound_at_exit, stop_path
+ setattr extras (brk_campaigns, brk.py:2117-2129): lens, inactive_components, n_inactive_components, anchor_kind, touch_i,
  die_i, rid, funding_census, entry_close_ms, exit_close_ms
```
`Advance` (tierc4_rules.py:324): conf_i conf_ms pivot_val pivot_bar pivot_bar_ms atr close cand_px rail_px new_stop prev_stop
rail_binding dist_from_close_over_atr. `Add` (tierc5_rules.py:554): i ms px size retrace_i retrace_ms.

### 2.2 `journal_frame(book)` (tierc5.py:1058; = TP.journal_frame) columns
```
asset lane entry_ms entry_ts direction arm_ms arm_ts entry_px stop_px anchor anchor_bar_ts
anchor_was_sealed_under_the_old_lockbox r_dist atr_at_entry r_over_atr n_advances final_stop_px stop_advanced_atr
ratchet_exit harvested harvest_ts harvest_unit_move_r harvest_blocked_by net_r_harvest_half net_r_runner_half
harvest_ride_would_have_r n_adds add_r spring_sweep_ts spring_bars_to_reclaim mfe_r mae_to_1r_r reached_1r
exit_ms exit_ts exit_px exit_reason bars_held gross_r fee_r funding_r funding_r_uncapped funding_ceiling_bound net_r
```
All floats `r6` (6 dp). Filed journals add the as-of stamp columns (`TP.stamp_n`, panel:2528): as_of_last_closed_4h,
as_of_panel_start, as_of_span_days, warranty, as_of_lens, as_of_last_closed_bar, as_of_panel, as_of_n_assets, as_of_substrate.

### 2.3 `tierc9.features9(book, card, lo_ms, hi_ms, roles)` (tierc9.py:592-662) — the autopsy row, adds:
`lag_arm_to_entry_bars` (= entry_i - arm_i), `tide_streak_age_bars`, `tide_streak_left_censored`, `r_over_atr`,
`mae_held_r mae_tape_r gap_through_r mfe_held_r mfe_tape_r` (excursions9, :467), `bars_to_1r`, `peak_vs_kept_pct`,
`net_r_entry_only`, `management_delta_r` (entry_only_r, :503), wall stamps (tierc6 l_wallq join), `mae_decile mfe_decile lag_decile`.

### 2.4 Per-bar path — NOT stored; reconstruct
- No MFE/MAE timeline, no bar-by-bar state is kept by replay9. `mfe_r`, `mae_r`, `mae_to_1r_r` are scalars.
- `LN.replay10` (and only it) attaches `t.stop_path` (lanes.py:667,685): list; `stop_path[0]=stop0`, then one entry appended at the END
  of every bar that did not exit. **Stop in force during bar j = `stop_path[j - (entry_i+1)]`.**
- Reconstruction recipe (deterministic, matches the ride): `f = T9.frame(sym)["f"]`; for `j in range(t.entry_i+1, t.exit_i+1)`:
  `fav = f.h[j] if d==1 else f.l[j]`, `ufav=(fav-entry)*d/r_dist` (same for adverse); +1R bar = first j with ufav>=1.0 (matches
  `tierc10_stamps._plus_1r_bar`, stamps.py:405, which HALTs if it disagrees with `t.reached_1r`); trail changes at
  `adv.conf_i` (effective from conf_i+1); harvest at `t.harvest_i`. Event-level timeline already exists:
  `tierc10_stamps.campaign_instants(t, f)` (stamps.py:530) emits entry/anchor_bar/plus_1r/harvest/advance/pivot_bar/bell/exit rows.

---------------------------------------------------------------------------------------------------------------------
## 3 · F-CTRL "v6 0.000e+00 cross-process anchored" (how TC10 computed it)

Code: `scripts/tierc10_panel_fixtures.py` f_ctrl_a (:187), _referees (:229), f_ctrl_b (:245); helpers in panel
`CTRL_COLS` (:2707), `ctrl_diff` (:2712), `control_window` (:2727), `ctrl_prefix` (:2737). Transcript:
`research_outputs/tierc10/panel/FIXTURES_PANEL.txt` lines 7-37 (both PASS).

**F-CTRL/a (in-process, exact zero):** `(lo,hi,_) = TP.corridor_n(CLASSIC5)` must equal `TP.control_window()` (= `tierc5.corridor()`
clamped to Stage D pin). `got = TP.run_cell_n(CONTROL_CARD, V6_ROLES, CLASSIC5, lo, hi)` vs `want = tierc6.run_cell(tierc6_rules.CARD_V6,
lo, hi)`. `ctrl_diff(journal_frame(got), journal_frame(want))`: sorted on (asset, entry_ms), equal count, **max abs diff == 0.0** over
CTRL_COLS = `entry_ms exit_ms entry_px exit_px stop_px r_dist net_r gross_r fee_r funding_r mfe_r n_advances`, and identical
exit_reason sequence. Result: n=200, worst 0.000e+00, net +41.7433 R. Break legs: +1e-9 on one net_r, one relabelled exit, one dropped row.

**F-CTRL/b (cross-process, prefix-robust):** referees = FILED parquets written by other processes:
`research_outputs/tierc6/trade_journal.parquet` (196 rows; edge = max exit_ms) and
`research_outputs/tierc9/trade_journal_control.parquet` (196 rows, `as_of_last_closed_4h`=2026-08-22T00:00Z; edge = that − 4h =
2026-08-21T20:00Z). `ctrl_prefix(live, filed, edge_open_ms, label)` asserts: (1) every filed (asset, entry_ms) present live;
(2) entry_px/stop_px/r_dist EXACT on shared rows; (3) every filed campaign NOT `corridor_end` closed live on the same exit_ms,
exit_px, exit_reason; (4) gross_r/fee_r/mfe_r exact on those, and any net_r drift equals −Δfunding_r at 6 dp (funding topped up by
Stage D: 1 ZEC campaign moved 0.0 → 0.014324); (5) every live-only campaign entered AFTER the referee's edge (4 live-only).
**Campaigns open at a referee's as-of** = its `corridor_end` rows: excluded from the close comparison (only such a row may move),
still checked on entry_px/stop_px/r_dist. The forward strip (`tierc10_close_forward_strip.py:10-16`) names them CONTINUATION
(`entry_ms < asof <= exit_ms`), "reported as a continuation, never a diff".

**For TC11:** the natural third referee is `research_outputs/tierc10/panel/control_journal.parquet`
(sha256 `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c`, 200 rows, as_of 2026-09-21T16:00Z, ONE corridor_end:
ETHUSDT entry 2026-09-18T08:00Z = the continuation). `_referees()` does NOT read it today — add it (edge = as_of − 4h).
Note tierc6/tierc9 dirs are gitignored (a fresh worktree lacks the referees; FIXTURES_PANEL.txt:355 says so).

---------------------------------------------------------------------------------------------------------------------
## 4 · THE 9/12 CARD (P-TRG-2)

- Definition: `card = TP.CONTROL_CARD`, `roles = T9.SWEEP_CELLS[-1] = Roles(name="trigger-9/12", trg_f=9, trg_s=12)`
  (tierc9.py:122-130). Only the TRIGGER role moves; window stays 12/89, tide/harvest/bell stay 89/316 & 12/89 (role de-aliasing,
  tierc9.py:136-165). Ride spec differs from `TP.CONTROL_RIDE` in exactly `roles_fields.trg_f '12'→'9'`, `trg_s '26'→'12'`.
- Filed: `research_outputs/tierc10/registrations/P-TRG-2.json` (4 arms, all CLASSIC5, runner run_cell_n: full two_sample [scored],
  full vs_zero, tuning-era, holdout-era). `.scored.json` binds book sha256 `b2276fa4…` (full, n=198), tuning `62284c33…` (n=132),
  holdout `b1fd4188…` (n=66). Rows: `research_outputs/tierc10/scores/P-TRG-2.rows.json` (SUPPORTED: Δ +0.258 R, CI [0.109,0.384]).
- **No filed 9/12 JOURNAL parquet exists** (only the book sha). `_book_sha` (panel:1988) = sha256 of sorted
  `[symbol, lane, entry_ms, repr(net_r)]` — re-ride and compare the sha to anchor it.
- **[measured]** 9/12 on CLASSIC5: 198 campaigns; arm→trigger lag median 22 bars, ≥16 bars: 116, lag 0: 43. (v6: median 3,
  ≥16: 63, 7–15: 4, lag 0: 52.)
- Ride through `run_cell_n` only on CLASSIC5 with `reg_id="P-TRG-2"` + filed text (REGISTRATION_TEXTS.json) + head
  (REGISTRY_PIN.json). No PANEL17 arm is filed → a 17-asset 9/12 view must use `T9.replay9` directly or a new filing.

---------------------------------------------------------------------------------------------------------------------
## 5 · LANES AND EXTENSION POINTS

### 5.1 tierc10_lanes.py (LN)
- `Card(T8.Card)` (lanes.py:200-213) adds ONE knob `be_floor_after_r: float|None = None`. `CARD_TC10_CONTROL`, `CARD_BE1`
  (1.0), `CARD_SPR2` (lane="spring"). `LANES = ("card","spring","union")`.
- `replay10(sym, card, roles, lo_ms, hi_ms, springs=None)` (lanes.py:838-1019): same candidate loop as replay9; card lane via
  `T9.card_candidates9`; spring lane via an INJECTED signal list (`SpringSignal`, lanes.py:714; shape-checked against raw tape by
  `check_signals`, :730); stop = `struct_stop_4h` (card) or `RC.spring_stop` (tierc5_rules.py:481). **TOTALITY guard
  (lanes.py:861-866): the card's field set must be EXACTLY T8.Card's + NEW_KNOBS** — a TC11 Card subclass with new fields HALTs
  here. Also HALTs on adds_max≠0, weave, reentry, ae_abort, time_stop, non-pivot anchor, harvest≠"band".
- `_ride_leg10` (lanes.py:482-685): `_ride_leg9` + BE-floor branch in the STOP slot; the latch bar is SEQUENCED on its 48 native
  5m children (`children_5m`, :262; `be_sequence`, :296; `be_latch_decision` :401; `be_latch_fill` :439; `apply_floor` :284).
  **This is the only existing sub-4h-bar ordering mechanism in the engine** — the template for 1h exits / relay entries.
- `run_lane(card, roles, panel, lo_ms, hi_ms, lane=None, springs_by_sym=None, reg_id, text, arm, lanes, head_of_record, reg_root)`
  (lanes.py:1065-1145): control rides unfiled (`is_control_ride`, :1027 → plain list); anything else walks
  `TP.require_arm` (panel:1834) and returns `TP.external_book(...)` (panel:1900). Refuses non-canonical registry roots with the real replay.
- F-LANES-OFF (lanes_fixtures.py:421-492): `run_lane(CARD_TC10_CONTROL, V6_ROLES, CLASSIC5, lo, hi)` vs `run_cell_n` control:
  every shared journal column 0.000e+00 — the pattern TC11's own replay must repeat.

### 5.2 tierc10_brk.py (BK) — the lens-generic machinery (most reusable for TC11)
- `LensFrame` (brk:851), `frame_l(sym, lens, with_funding=True)` (brk:920; lens ∈ 5m 1h 4h 12h 1d 1w via `D.load_asof`, as-of clean,
  memo keyed (sym, lens) + per-instance uid). `roles_l(lf, roles, ribbon=None)` (:957) → six role EMAs + crosses (w_up/w_dn/t_up/
  t_dn/b_up/b_dn). `fractals_l` (:996), `anchor_series_l` (:1005).
- `ride_leg_l(lf, card, roles, d, ti, entry_px, stop0, r_dist, hi_i, ribbon=None, active=COMPONENTS)` (:1093-1210): `_ride_leg9`
  transcribed onto any lens; cold components (EMA period > entry_i) are inactive and named. `ribbon=(12,25)` adds the BRK 12/25
  bell (tested last) — **pass `ribbon=None` for pure v6 management**.
- `account_l(lf, card, d, r_dist, leg)` (:1270-1326): same fee law; funding by INTERVAL SUM (`funding_interval`, :1223: stamps with
  `entry_ms < hour <= exit_bar_open_ms`, priced at last closed lens bar). Single-leg only (no adds).
- `brk_campaigns(lf, legs, card, roles, lane, lo_i, hi_i, ribbon=None, active, era, account=True)` (:2045-2131): one position per
  (asset, lane), returns `RC.Trade`s. **F-BRK-RIDE-4H** (brk_fixtures.py:383ff) proves feeding the control's 4h entries+stops through
  this core reproduces v6 exactly (all but the 5 arming fields).
- `Leg` (:2025): direction entry_i stop_px r_dist anchor anchor_bar rail_binding n_eligible touch_i die_i rid anchor_kind note.
- `legs_from_candidates(lf, cands, lane, permit=None, rail_atr=1.0)` (:2134): candidate → `brk_stop` (:1366, = spring_stop geometry on
  the retest extreme: farther of `extreme ∓ 0.5 ATR` and `entry ∓ 1.0 ATR`), `permit(entry_i, d)->{"ok":..}` refusals counted.
- Anchors: `Candidate` (:1390; direction anchor die_i touch_i known_i extreme rid verdict note), `candidacy_window` (:1411; end =
  min(die+400, next_die−1, n−1)), `r1_band(name)` (:1429; "tap-89", "tap-127", "tap-200", "ribbon-89/127", "ribbon-127/200"),
  `band_hold_candidates(h,l,c,atr,dies,lo,hi,margin_atr,hold_bars,ttl_bars)` (:1475; known_at = touch + hold_bars),
  `memory_flip_candidates(h,l,dies,flips,n,hold_bars=6,ttl=400)` (:1541). Frozen pins read from engine/rangefinder.py AST:
  FLIP_HOLD_MARGIN 1.0, FLIP_HOLD_BARS 6, SCALE_MULT 3.0, MEM_TTL 400 (brk:145-151).
- `macro_signals(sym, lens, scale_mult=3.0)` (:2332): the ONLY range doorway (function-local `import tierc10_census`) →
  `{"dies":[(die_i,rid,side)], "flips":[{"i","polarity","rid"}]}`. Census lenses: **5m, 4h, 1d only** (tierc10_census.py:117-119).
- HTF causality: `visible_htf_idx(exec_open_ms, htf_open_ms, htf_step_ms)` (:1727; HTF bar visible iff its close <= exec bar OPEN),
  `tide_state(e_fast,e_slow,c)` (:1749; +1/0/−1 three-state), `tide_4h_for_exec(exec_open_ms, f4, roles)` (:1761).
- Runners `run_lane_s1` (:2201; 5m, band-hold, 4h-tide permit, 12/25 bell, holdout era) and `run_lane_i1` (:2271; 1d) are the
  templates for P-BRK-4H and the scalper.

### 5.3 Extension points for TC11 (what exists vs what must be written)
| need | hook today | status |
|---|---|---|
| alternative 4h trigger (other periods) | `Roles(trg_f, trg_s)` + `run_cell_n` / `replay9` | EXISTS |
| alternative trigger on another lens inside the 4h window (relay) | none; candidates are 4h indices, ride starts at `ti+1` 4h | **GAP** |
| admission gate (refuse a trigger) | no hook in replay9/10 candidate loop (tierc9.py:390-400, lanes.py:940-956) | **GAP** — copy replay10 → replay11 with a `refuse(arm, ti, d)` slot after `position_open`, before the stop; or post-filter the v6 book (see ambiguity A5) |
| adds (tranches) | accounting EXISTS: `_account_chain` books `leg["adds"]` (tierc7.py:433-441: add exits at leg exit_px, fees both sides, funding from add bar, R = campaign R, `add_r`); `RC.Add(i,ms,px,size,…)`; precedent ride slot in tierc5._ride (tierc5.py:302-311, after harvest, before trail, fills at bar close) | ride **GAP**: _ride_leg9/10 return `adds: []`, replay9/10 HALT on `adds_max`, Trade gets `adds=[]`, `add_r=None` |
| take-profit order | none in v6 path; precedent `harvest="fixed_r"` resting target filled AT the level in tierc5._ride (tierc5.py:263-265, 298-301) | **GAP** |
| 1h exit rule pre-+1R | none; only sub-bar mechanism is the BE 5m walk | **GAP** |
| new lens lanes (4h BRK, 5m scalp) | BK.frame_l / band_hold_candidates / brk_stop / brk_campaigns / account_l | MOSTLY EXISTS (scalp needs a target/stop-only ride) |

---------------------------------------------------------------------------------------------------------------------
## 6 · TOLL, FEES, FUNDING, NET R

- **Fee law** (tierc7._account_chain, tierc7.py:365-398): `bps = FEE_BPS_SIDE/1e4 = 0.0005` (taker 5 bps/side, flat, EVERY asset).
  No harvest: `gross = (xpx−e)·d`, `fee = bps·(e + xpx)`. Harvest: q=0.5 slice `(hpx−e)·d`, fee `bps·q·(e+hpx)`; runner `(1−q)`.
- **Funding** (lineage 4h path, tierc7.py:369-374): `Σ_{j=ti+1..xi} rate(open_ms[j])·close[j−1]·d·qty` — rates keyed to the 4h bar
  OPEN hour (`tierc2_baseline.load_funding`, :216, hour-floored). Stamps between 4h opens are DROPPED (SOL has 98 2-hour-spaced
  stamps; 4h-interval assets ENA/PUMP/HYPE/BONK align). BK.account_l uses the interval sum (all stamps) — identical on 4h CLASSIC5.
- **Ceiling**: funding COST capped at `funding_ceiling_r = 1.0` R, credits never capped.
- **net_r = gross_r − fee_r − funding_r_eff**, all ÷ r_dist. `net_r_harvest_half + net_r_runner_half == net_r` asserted 1e-9.
- **Tiered slippage is NOT in net_r.** It exists only as the HAIRCUT TWIN, an ADDED column:
  `tierc10_data.haircut_twin_net_r(asset, gross_r, entry_px, exit_px, risk_px)` (tierc10_data.py:1408-1441):
  `cost_px = ((5 + slip)/1e4)·(entry+exit)`, `net_r_twin = gross_r − cost_px/r_dist` — **fee + slippage, NO funding, single leg
  (ignores the harvest split)**. Tiers parsed from `CONTRACT_SLIPPAGE_CLAUSE` (:217): A {BTC ETH} 2 bps · B {SOL NEAR ZEC LTC BNB
  DOGE UNI SUI XMR} 5 · C {ENA PUMPFUN HYPE MNT PEPE BONK} 10 (per side). Keyed by CONTRACT name; `haircut_twin_for_stem(stem,…)`
  (:1444) maps stems via the Stage D manifest. Book-level wrapper: `tierc10_score.haircut_twin_block(book, base)` (score.py:1204;
  also prints `twin − funding_r` companion).
- **Census "toll"** (a third notion): `toll_atr = (round_trip_bps_used/1e4)·close/ATR` with `round_trip_bps_used = 10` for all 17
  (tierc10_census.py:510; data/fee_schedule.json) — flat, no tier. BRK prints it beside net_r (`stamp_toll`, brk:2385;
  `TOLL_ACCOUNTING` brk:453 "PRINT, NOT A DEDUCTION").
- **Maker fee: not defined anywhere** (charter :112 names taker 0.05% only).

---------------------------------------------------------------------------------------------------------------------
## 7 · FIELDS: WINDOW AGE, TIDE AGE, r_dist, ERAS

- **Arm→trigger lag (window age)**: `t.entry_i − t.arm_i` in 4h bars (features9 `lag_arm_to_entry_bars`, tierc9.py:627). From a
  journal: `(entry_ms − arm_ms)//MS_4H` (safe: CLASSIC5 4h grids are gapless in-corridor, but prefer indices).
  **[measured v6]** lag ≥16: **63/200**; 7–15: **4/200**; 0: 52.
- **Tide age — TWO definitions exist and disagree:**
  (a) `tierc9.tide_streak_age(t, roles)` (tierc9.py:537-560): 3-state tide (tide_f>tide_s AND close>tide_s) run length ending AT
      THE ARM BAR, flip bar = 1, counted down to `floor_bars` (left-censored flag). **[measured]** >206: 57/200, median 97.
  (b) `tierc7_lab_regime.tide_streak(sym)` (tierc7_lab_regime.py:306-350): 2-state `sign(e89−e316)` run length at the ENTRY bar,
      counted from `TIDE_WARM_BARS = 316`. **This is TC10's P-AGE-1 definition** (tierc10_close_p_age_1_tide_youth.py; report
      research_outputs/tierc10/close/P_AGE_1_TIDE_YOUTH.md). **[measured]** >206: 120/200, median 249.
  Trailing-quantile banding: `tierc9.tc7g_tables(lo,hi)` (:1331) via `_trailing_pool` (:1290, **hard-wired to RC.UNIVERSE =
  CLASSIC5**, bar-pooled `run>0` bars in [lo,hi]) and `_trailing_edges(pool, at_ms)` (:1318; quantiles
  `STREAK_BAND_QUANTILES=(0.25,0.5,0.75)` of the prefix `open_ms <= entry`, needs ≥30 bars); band = `np.digitize(run, edges)`
  (`_streak_band`, lab:456) → 0 B1 YOUNG · 1 B2 EARLY · 2 B3 MATURE · **3 B4 OLD (run ≥ trailing q75)**. TC10 B4 OLD = 59/200.
  Whole-corridor bar-pooled quartiles = **[88, 206, 396]** — so the contract's "206" is the MEDIAN (B2/B3 edge), not the OLD edge.
- **r_dist / structure distance**: `t.r_dist` (price); `r_over_atr = r_dist/atr_at_entry` (journal column). ">2.2 ATR" = `r_over_atr > 2.2`.
- **Eras** (panel:746-816): `ERA_CUT_ISO = "2024-06-30T23:59:59Z"`, `ERA_CUT_MS = 1719791999000`. `era_window`: tuning = (None,
  1719791999000] · holdout = [1719791999001, None) · full. Membership by `entry_ms` (`in_era`). `corridor_era(panel, era)` ride
  windows **[measured]**: tuning 2019-09-08T16:00Z → last bar closing 2024-06-30T20:00Z; holdout from bar opening
  2024-07-01T00:00Z → 2026-09-21T16:00Z. Consequences: (i) the 4h bar opening 2024-06-30T20:00Z is in NO era window;
  (ii) a tuning-era ride truncates open campaigns with `corridor_end` at the tuning edge; (iii) a holdout ride never sees armings
  before 2024-07-01 (armings9 filters `arm_i >= lo_i`). P-TRG-2 tuning 132 + holdout 66 = full 198 on this corridor.

---------------------------------------------------------------------------------------------------------------------
## 8 · THE ASSETS

- **Five home assets** `TP.CLASSIC5 = RC.UNIVERSE = ("BTCUSDT","ETHUSDT","SOLUSDT","NEARUSDT","ZECUSDT")` (panel:197-199, HALTs if moved).
- **Seventeen** `TP.panel17()` (panel:458; measured from bars, cross-checked vs `research_outputs/tierc10/data/STAGE_D_MANIFEST.json`):
  CLASSIC5 + `ENAUSDT PUMPUSDT HYPEUSDT MNTUSDT_BYBIT SUIUSDT LTCUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT`
  (contract names ENA PUMPFUN HYPE MNT SUI LTC XMR BNB UNI PEPE DOGE BONK; MNT is Bybit v5 linear, all others Binance USDT-M;
  all 12 admitted; admission rule `n_4h >= 316+400`). PANEL17 corridor = same edges as CLASSIC5; per-asset floor = own bar 316.
- Never-touched (per TC10 F-D-5): only PUMPFUN, MNT, SUI.

---------------------------------------------------------------------------------------------------------------------
## 9 · HOW TO CALL THIS FROM A NEW tierc11 SCRIPT

```python
import sys; from pathlib import Path
ROOT = Path("/Users/luis/Naiad"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import numpy as np, pandas as pd
import tierc10_panel as TP, tierc9 as T9, tierc8 as T8, tierc7 as T7, tierc7_rules as RC
import tierc6 as T6, tierc6_rules as V6
import tierc10_brk as BK                       # imports tierc10_data → snapshot must be tc10_20260921

lo, hi, meta = TP.corridor_n(TP.CLASSIC5)      # clamps to research_outputs/tierc10/data/AS_OF_PIN.json
base = TP.run_cell_n(TP.CONTROL_CARD, T9.V6_ROLES, TP.CLASSIC5, lo, hi)   # unfiled control: allowed
j6 = TP.journal_frame(base)

# F-CTRL/a
ok, worst, why = TP.ctrl_diff(j6, TP.journal_frame(T6.run_cell(V6.CARD_V6, lo, hi)))
# F-CTRL/b (add the TC10 filed control as a referee; its ETH corridor_end row is the continuation)
ref = pd.read_parquet(ROOT / "research_outputs/tierc10/panel/control_journal.parquet")
edge = TP._iso_ms(str(ref["as_of_last_closed_4h"].iloc[0])) - TP.MS_4H
ok_b, lines = TP.ctrl_prefix(j6, ref, edge, "FILED tierc10/control_journal")

# 9/12 (Tier-E / 17 assets: the replay is ungated by design; run_cell_n is the gate)
R912 = T9.SWEEP_CELLS[-1]                      # Roles(trigger-9/12, trg_f=9, trg_s=12)
b912 = [t for s in TP.CLASSIC5 for t in T9.replay9(s, TP.CONTROL_CARD, R912, lo, hi)[1]]

# per-campaign bar path + fields
for t in base:
    f = T9.frame(t.symbol)["f"]; d, R = t.direction, t.r_dist
    ufav = [((f.h[j] if d == 1 else f.l[j]) - t.entry_px) * d / R for j in range(t.entry_i + 1, t.exit_i + 1)]
    lag = t.entry_i - t.arm_i; r_atr = t.r_dist / t.atr_at_entry
    age_arm, cens = T9.tide_streak_age(t, T9.V6_ROLES)            # definition (a)
    import tierc7_lab_regime as LR; age_entry = int(LR.tide_streak(t.symbol)[1][t.entry_i])   # definition (b)

# 1h events stamped on a 4h campaign, causal (1h bars CLOSED by the 4h bar's close)
lf1, f4 = BK.frame_l(t.symbol, "1h"), BK.frame_l(t.symbol, "4h")
from engine import indicators as ind
e9, e12, e26, e89 = (ind.ema(lf1.c, p) for p in (9, 12, 26, 89))
x_912_up = ind.crossover(e9, e12); x_1289_dn = ind.crossunder(e12, e89)
k_last = np.searchsorted(lf1.close_ms, f4.close_ms, side="right") - 1   # last 1h bar closed at/before each 4h close
# (use side="left" for STRICTLY-before; see ambiguity A2)

# 4h lane on v6 management (P-BRK-4H template)
sig = BK.macro_signals(sym, "4h")                                      # dies/flips at SCALE 3.0 (census import is lazy)
lo_b, hi_b = BK.r1_band("tap-89")(f4.c)
cands, tally = BK.band_hold_candidates(f4.h, f4.l, f4.c, f4.atr, sig["dies"], lo_b, hi_b, margin_atr=?, hold_bars=?)  # pins: A6
tide = BK.tide_state(*(lambda r: (r["tide_f"], r["tide_s"]))(BK.roles_l(f4, T9.V6_ROLES)), f4.c)
legs, refused = BK.legs_from_candidates(f4, cands, "brk-4h", permit=lambda i, d: {"ok": tide[i] == d})
lo_i, hi_i = BK.idx_range(f4.open_ms, lo, hi)
trades = BK.brk_campaigns(f4, legs, TP.CONTROL_CARD, T9.V6_ROLES, "brk-4h", lo_i, hi_i, ribbon=None, era="full")

# rulers
ci = TP._ci_from(TP.cluster_boot([t.net_r for t in trades], [t.symbol for t in trades], seed=TP.SEED), point)  # 90% CI
d15 = TP.d15(cell_book, base)       # paired_delta_expectancy_r, tail_exit_ratio, max_single_trade_delta_share
```

---------------------------------------------------------------------------------------------------------------------
## 10 · GAPS — what the code CANNOT do today for TC11

G1 **Adds** (P-ADD-BRK / P-ADD-SFP): no ride path appends `RC.Add`; replay9 and replay10 HALT on `adds_max`; Trade gets
   `adds=[]`/`add_r=None`. Accounting is ready (`_account_chain` books `leg["adds"]` at `size·add.size`, exits with the campaign's
   exit price, R = campaign R). The TRIGGER events (1h range DIES in trade direction; 1h SFP confirm at the trend-side boundary) need
   a 1h range census, which `tierc10_census` does not support (lenses 5m/4h/1d). `BK.account_l` has no add support.
G2 **Take-profit at the next-higher lens boundary** (P-TP-RNG): no TP exit in _ride_leg9/_ride_leg10/ride_leg_l; no 12h range
   census (needed "12h boundary for a 4h campaign", "when that lens is IN-RANGE"); only precedent is tierc5's `harvest="fixed_r"`
   resting target (fills AT level), which the v6 paths refuse (`harvest != "band"` HALT).
G3 **1h exit while pre-+1R** (P-WARN-1): the ride is 4h-granular; an exit at a 1h close inside a 4h bar needs a children walk
   (template: `LN.children_5m`/`be_sequence`, lanes.py:262-398) to order the 1h close against the stop and the +1R print.
G4 **Relay entry** (P-RELAY-1): candidates and rides start at 4h closes (`ti` is a 4h index; loop from `ti+1`). A 1h-close entry
   needs: the partial remainder of its 4h bar walked on 1h children for the stop, `struct_stop_4h` evaluated at the last CLOSED 4h
   bar with ATR(4h) of that bar, then the 4h ride. The "miss column" needs the per-window arming list (`card_candidates9` arms).
G5 **Admission gates**: no refusal hook; a new replay (replay11) with an F-LANES-OFF-style 0.000e+00 control is needed, because
   replay10's TOTALITY guard rejects any new Card field.
G6 **Registration plumbing for m = 9**: `run_cell_n` (panel:1137) and `score()` (panel:2215) call `require_registered` WITHOUT
   `family_m`, so the default `FAMILY_M = 6` (bound at def time) is enforced → a TC11 filing with family_m=9 HALTs at both doors.
   `REG_DIR` is hard-coded to `research_outputs/tierc10/registrations`, and both `run_cell_n` and `run_lane` refuse any other root
   while the real replay is loaded. `finish_family(rows, family_m=9)` and `require_arm(..., family_m=9)` do accept it.
G7 **Corridor / as-of**: `corridor_n` clamps to `research_outputs/tierc10/data/AS_OF_PIN.json` (2026-09-21T16:00Z);
   `tierc10_data`/`tierc10_stamps`/close scripts HALT unless the snapshot is exactly tc10_20260921. A "latest closed 4h bar" corridor
   and the FORWARD LEDGER ("re-ridden on new bars only") both need a new snapshot + pin that no module can read today.
G8 **Scalper ride**: no target-or-stop-only ride (v6 management = trail+harvest+bells); no maker fee rate exists anywhere; no 1h
   range census for the target; 5m structural pivot stop can reuse `RC.build_pivots_4h(h5,l5)` + `struct_stop_4h(…, lookback=200)`
   on 5m arrays (generic in the arrays, named 4h).
G9 **15m lens** (R1): `D.load_asof(stem, "15m")` → KeyError (STEP_MS has 5m 1h 4h 12h 1d 1w); 15m parquet files exist for most
   stems but not MNT/PUMP/SUI and were not Stage-D fetched.
G10 **No filed 9/12 journal**: only book shas in `registrations/P-TRG-2.scored.json`; the forward ledger's "frozen 9/12" must be
   re-ridden and anchored by `_book_sha`.
G11 **Tiered toll in net R**: neither net_r nor the census toll carries the tier slippage; only the haircut twin does (and it omits
   funding and the harvest split).
G12 `_trailing_pool` (tide-age trailing quantiles) is hard-wired to CLASSIC5; a 17-asset tide-age gate needs a re-pointed pool.

---------------------------------------------------------------------------------------------------------------------
## 11 · AMBIGUITIES IN THE TC11 CONTRACT (quoted)

A1 F-DEF / P-AGE-1 — "both tide-age definitions computed and printed; a swapped definition must FAIL" and "the absolute definition
   (refuse age > 206 bars)". The estate has two AGE MEASURES (arm-bar 3-state vs entry-bar sign(e89−e316); 57 vs 120 of 200 exceed
   206) AND two CUT RULES (trailing q75 = OLD band vs absolute 206). 206 is the whole-corridor bar-pooled MEDIAN (B2/B3 edge), not
   the OLD edge (396): "absolute >206" refuses MATURE+OLD, the trailing rule refuses OLD only. TC10's P-AGE-1 used measure (b).
A2 F-WARN-ASOF — "only 1h bars CLOSED before the 4h bar closes": the 4th 1h child closes AT the 4h close. Strict "before" excludes it.
A3 P-WARN-1 — "exit at the 1h counter-12/89 close while pre-+1R": is "pre-+1R" the 4h intrabar latch (ride law) or the 1h path up to
   that 1h close? On a 4h bar holding both, the answer depends on 1h order.
A4 P-RELAY-1 — "4h window open+armed; ENTRY on the 1h 9/12 with-trend close inside it": (i) earliest legal 1h close = the arm bar's
   close (the arming is unknowable earlier); (ii) one relay per window or re-entry after exit; (iii) does the relay also require the
   1h close to precede the 4h 12/26 trigger (F-RELAY says "1h close precedes the 4h trigger bar"); (iv) "R on 4h": ATR/pivots of
   the last CLOSED 4h bar.
A5 F-GATE — "each gate removes only the trades its text names": a refusal INSIDE the replay frees the asset's slot and can ADMIT
   campaigns v6 refused as `position_open`; a post-filter of the v6 book removes exactly the named trades. Two different books.
A6 P-BRK-4H — "first HOLD retest on the 89 tap": no tuned 4h hold pins exist (TUNING_RESULT for 5m and 1d only); FLIP_HOLD
   (1.0 ATR / 6 bars) is the frozen default the memory-line uses. "tide aligned": at the entry bar (its own close) or last bar
   before it.
A7 P-TP-RNG — "take-profit of the remainder at the approach (0.25 ATR)": ATR of which lens (12h?); remainder = post-harvest half,
   or the whole unit if not yet harvested; fill as resting limit at the level vs at close; TP vs stop vs bell ordering in one bar;
   "when that lens is IN-RANGE" evaluated at entry or bar by bar.
A8 "net of L's toll" (R4), "E[net R]", "taker toll (record) AND maker toll" — three toll notions exist (flat 10 bps fee in net_r;
   tiered haircut twin; census toll_atr, printed not deducted). Which one is "the toll" for each table is unstated.
A9 "Corridor: full water, latest closed 4h bar, one as-of pin" vs the frozen tc10_20260921 snapshot the scout rules mandate (G7).
A10 Eras on a new corridor: era rides via `corridor_era` truncate tuning campaigns at the cut and drop pre-cut armings from
   holdout; slicing a full-corridor book by `entry_ms` gives a different book. Which one P-SCALP-2 ("holdout era") means matters.
