# U3 — THE TC11 ENVIRONMENT, THE BOOKS AND THE CONTROL (TC12 STAGE C)

Scout map, read-only. Contract read: `scratchpad/tc12/2026-10-08_TC12_APOLLO.md` sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd` (137 lines, 12,209 B).
Trees: MAIN = `/Users/luis/Naiad` (branch v12-v1-census; HEAD was `a399b47` when this scout began and `28e006b tierc12(STEP Q)` when it ended — another actor committed mid-scout). X = `/Users/luis/Naiad/.claude/worktrees/tierc11x` (HEAD `7b24f835bcbf7430eb0f97b6c39b6b1b233eef11`; `git status --short` = exactly one line `?? research_outputs/tierc11x/close/CERTIFIED_TIP`).
Every number below was read this session; "computed" = a short inline read of the cited file. Nothing was built or run.

---------------------------------------------------------------------------------------------------
## 1 · FACTS

### 1.1 What "card v6" is, and where its parameters live

- **The object ridden**: `TP.CONTROL_CARD = T8.Card(name="v6-control")` (`scripts/tierc10_panel.py:816`) with roles `T9.V6_ROLES = Roles()` (`scripts/tierc9.py:119`). `TP.is_control_book(card, roles, panel)` (`tierc10_panel.py:1083-1092`) is the only book `TP.run_cell_n` rides without registration paperwork.
- **Class chain** (each a frozen dataclass subclass, defaults = v6): `tierc5_rules.Card` (`scripts/tierc5_rules.py:287-320`) → `tierc6_rules.Card` (`:197-217`; `CARD_V6 = Card()` `:220`) → `tierc7_rules.Card` (`:227-246`, six v7 knobs all OFF) → `tierc8.Card` (`scripts/tierc8.py:254-264`, `anchor_kind="pivot"`, `anchor_offset=RC.STOP_BUF_ATR`).
- **The 29 card fields, as FILED** (`research_outputs/tierc10/registrations/P-TRG-2.json` key `book_spec.arms[0].ride.card_fields`; identical dict in X `research_outputs/tierc11x/forward/BOOK_SPECS.json` `books.v6.ride_spec`): add_size 1.0 · adds_max 0 · ae_abort_r None · anchor_kind 'pivot' · anchor_offset 0.5 · entry_rail_atr 1.0 · funding_ceiling_r 1.0 · grid 'card' · harvest 'band' · harvest_fixed_r 2.0 · harvest_frac 0.5 · harvest_min_unit_r -inf · hybrid_anchor False · lane 'card' · limit_ae_mult None · reentry False · seal_open True · stop_grid_offset_atr 0.0 · time_stop_bars None · trail True · trail_arm_after_r 1.0 · trail_extra_buf_atr 0.0 · trail_l 2 · trail_r 2 · trail_min_advance_atr 0.05 · wall_exit_atr None · wall_tf '12h' · weave False · weave_k 6.
- **Roles**: v6 = tide 89/316 · window 12/89 · trigger 12/26; 9/12 = same with trg 9/12 (`research_outputs/tierc11/books/build_manifest.json` key `roles`; `tierc9.py:93-130`). `Roles.floor_bars = max(RC.WARMUP_BARS, max(periods))` = 316 (`tierc9.py:111-116`).
- **Register constants** the ride reads: `scripts/tierc2_rules.py:54-127` (UNIVERSE = BTC ETH SOL NEAR ZEC USDT; TIDE 89/316; WINDOW 12/89; TRIGGER 12/26; D_DISPLACEMENT 0.75; ATR_LEN 14; FEE_BPS_SIDE 5.0; PIVOT_L/R 5/5; STOP_BUF_ATR 0.5) · `tierc3_rules.py:88-108,147-148` (PIVOT_LOOKBACK_4H 200; MIN_STOP_ATR 1.0) · `tierc4_rules.py:116-169` (RATCHET_PIVOT 2/2; HARVEST_FRACTION 0.5; HARVEST_BAND (89,316)) · `tierc5_rules.py:150-213` (SEAL_OPEN True; FUNDING_CEILING_R 1.0; WARMUP_BARS = TIDE_SLOW; PROVISIONAL_MIN_N 30) · `tierc6_rules.py:122-130` (TRAIL_ARM_AFTER_R 1.0; TRAIL_MIN_ADVANCE_ATR 0.05).
- **Fees are a module constant, not a file read**: `bps = RC.FEE_BPS_SIDE / 10_000.0` inside `tierc7._account_chain` (`scripts/tierc7.py:366`); `fe = bps*size*(e + xpx)` (`:415`); funding = Σ over bars j in (entry_i, exit_i] of `rate(open_ms[j]) * close[j-1] * d * qty` (`:370-376`); the D12 ceiling once per campaign (`:454-456`); `net = gross - fee - fund_eff` (`:457`). The fee schedule file is only CHECKED against it (`tierc11_env.py:1010-1014`).

### 1.2 The decision-module import closure, and the fixture that asserts it

Fixture: `scripts/tierc11_closure_fixtures.py` (sha256 `68253ed1a09a70c5…`, certified by TC11 PROGRESS stage TC11-FIX). Transcript of record: `research_outputs/tierc11/closure/FIXTURES_CLOSURE.txt` sha256 `520fbc49bfca22f6a611f46deef474344b091aa6ed654e500aee0a12703c6c9b` (3 GREEN, 0 RED).

- **How it enumerates** — `tierc11_names()` globs `scripts/tierc11_*.py` minus `*_fixtures` (`:246-248`) → 19 modules. DECISION set = all of them except `tierc11_nest` and the TYPED runners `RUNNERS_T` (`:120-121`: stage_a, stage_h, stage_r, stage_r4, stage_t_brk); a module the file does not name DEFAULTS to DECISION (docstring `:9-13`). Each runner's exemption must be EARNED: its source must import `tierc11_nest` (`runner_findings` `:474-484`).
- **DECISION (13)** (FIXTURES_CLOSURE.txt:18; the 19 non-fixture modules at :16): tierc11_books, tierc11_data, tierc11_data_clock_note, tierc11_env, tierc11_forward_ledger, tierc11_registrations, tierc11_ride, tierc11_score, tierc11_stage_g, tierc11_stage_s, tierc11_stage_t_relay, tierc11_stage_w, tierc11_worktree_attest.
- **LINEAGE (54)** = static repo closure by `lineage_walk` (`:449-471`; Import/ImportFrom anywhere incl. function bodies, constant-string `import_module`/`__import__`/`tc10_import`, name-held dynamic imports) (FIXTURES_CLOSURE.txt:33): analytics, analytics.levels, analytics.momentum, analytics.profile, analytics.structure, analytics.volatility, analytics.vwap, census2a_program, census2b_firstlook, census2b_parta, census2b_program, census_build, engine, engine.cells, engine.config, engine.data, engine.htf, engine.indicators, engine.journal, engine.replay, engine.s1, engine.s2, engine.shadows, engine.signals, engine.trading, engine.version, mc1_program, mc2_program, seq8_extract, seq8_views, tierc2_baseline, tierc2_rules, tierc3_baseline, tierc3_rules, tierc4_baseline, tierc4_rules, tierc5, tierc5_rules, tierc5q, tierc6, tierc6_lab_limit, tierc6_lab_misc, tierc6_lab_zec, tierc6_rules, tierc7, tierc7_lab_chain, tierc7_lab_regime, tierc7_lab_stopgrid, tierc7_lab_weave, tierc7_rules, tierc8, tierc8_an1, tierc8_an2, tierc9.
- **`LINEAGE_ENV_T` (15)** = what a fresh `import tierc11_env` actually loads, typed (`:122-124`): tierc2_baseline, tierc2_rules, tierc3_baseline, tierc3_rules, tierc4_baseline, tierc4_rules, tierc5, tierc5_rules, tierc6, tierc6_rules, tierc7, tierc7_lab_regime, tierc7_rules, tierc8, tierc9.
- **TC10 layer, disclosed not walked** (FIXTURES_CLOSURE.txt:36): tierc10_brk and tierc10_lanes (each has a `tierc10_census` import in its source), tierc10_data, tierc10_panel.
- **What it asserts** (`scan_source` `:410-434`, `fresh`/`fresh_findings` `:524-546`): `FORBIDDEN = ("rangefinder","tierc10_census","tierc10_stamps","tierc10_null","tierc11_nest")` (`:118`) is a SUBSTRING test on module names; one fresh interpreter per DECISION module must hold no such name in `sys.modules` and must load the module from `scripts/<name>.py`; the AST walk of every DECISION and LINEAGE source must find no forbidden import, no `sys.modules[...]` reach, no `.top`/`.bottom` read, no undeclared non-constant import site (declared: `tierc11_env.tc10_import`, `:144`), no exec/eval/compile in a DECISION module; the walk must hold `LINEAGE_ENV_T` and every repo module the fresh interpreters loaded.
- **NOTE for V**: the package `analytics` and `analytics.profile` (which already holds `volume_profile(high, low, volume, bins=100, value_area=0.70)`, `analytics/profile.py:113`) are INSIDE the decision lineage today (reached through tierc2_baseline's A-TAPE). `analytics/__init__.py` imports only hashlib and pathlib (`:24-25`) — it loads no submodule; `analytics_sha()` hashes the files named in `_MODULES` (`analytics/__init__.py:118,123-136`).
- Same shim-level rule in the env: `FORBIDDEN_MODULE_SUBSTRINGS` (`tierc11_env.py:133-134`), the RANGE-FREE post-shim clause (`:1015-1017`), `static_imports` (`:1179-1197`), `hook_escapes` (`:1212-1252`).

### 1.3 How the snapshot and the corridor are selected

1. `engine.data.cache_dir()` (`engine/data.py:39-48`): `NAIAD_CACHE_DIR` if set, else `~/.cache/naiad/data_cache` (the LIVE cache); it then `base.mkdir(parents=True, exist_ok=True)`.
2. `tierc2_baseline.KLINES = cache_dir() / "klines"`, `FUNDING = cache_dir() / "funding"` — bound AT IMPORT (`scripts/tierc2_baseline.py:205-206`). `load_klines(sym, tf)` reads `KLINES/{sym}_{tf}.parquet` (`:209-213`); `load_funding(sym)` → `{hour_ms: rate}` (`:216-232`). Exporting the variable after python starts changes nothing.
3. `tierc11_env.guard_substrate(env)` (`scripts/tierc11_env.py:192-211`, called at `:214-215` BEFORE any engine import): HALTs unless `NAIAD_CACHE_DIR` resolves to `SNAPSHOT = ~/.cache/naiad/snapshots/tc11_20260925` (`:117`) with a `klines/` dir; refuses the live cache and `tc10_20260921` by string and by resolve.
4. Imports: `tierc2_baseline` FIRST under the TC11 env (`:718-719`); then tierc10_data, tierc10_panel, tierc10_brk, tierc10_lanes, tierc9, tierc8, tierc7, tierc7_rules, tierc7_lab_regime, tierc6, tierc6_rules, tierc5, tierc5_rules, tierc4_rules, tierc3_rules, tierc2_rules, each inside `_window(label, TC10_SNAPSHOT)` (`:721-752`) — the env var points at `tc10_20260921` for that one import statement because `tierc10_data.assert_substrate()` runs at import and demands it (`scripts/tierc10_data.py:94-117`).
5. Re-roots: `REROOT_PLAN` (`tierc11_env.py:769-797`, 25 rows) + the `TP._U12` re-resolve (`:847-866`). The ones that select the corridor: `D.SNAPSHOT`, `D.OUT → OUT/data`, `TP.AS_OF_PIN → research_outputs/tierc11/data/AS_OF_PIN.json`, `TP.STAGE_D_MANIFEST`.
6. Post-shim assertion (`:952-1019`): `D.load_pin() == TP.stage_d_pin() == PIN_MS` (`PIN_MS = 1_790_294_400_000`, `:122`); every KLINES/FUNDING binding under the TC11 snapshot; no undeclared TC10 binding; panels == TC11's Stage D manifest; fee schedule taker == `R2.FEE_BPS_SIDE`; no range module.
7. Audit hook armed LAST (`sys.addaudithook(_enforce_hook)`, `:1150`): AuditHalt on any open under the TC10 snapshot or the live cache; any write under `research_outputs/tierc10[_run2]/`, `scripts/tierc10_*`, `exchange/status/LEDGER*`, `LEDGER.md`, `.gitignore` (both trees); any read under `research_outputs/tierc10` not on `TC10_ALLOW` (8 records, `:140-158`). Exit code 70 on any BLOCKED attempt (`:183,1129-1147`).
8. The corridor: `TP.corridor_n(panel, pin_close_iso=None, floor_bars=WARMUP_BARS)` (`tierc10_panel.py:650-733`): `lo` = earliest first 4h bar of the panel; `close` = min over assets of (last open + 4h), CLAMPED DOWN to `TP.stage_d_pin()` (reads `TP.AS_OF_PIN` key `as_of_last_closed_4h_close_ms`, `:634-647`); an explicit `pin_close_iso` may only look BACK (`:690-699`); `hi = close - 1`.
9. `tierc11_books.corridor(pin_close_iso=None)` (`scripts/tierc11_books.py:254-262`) wraps it and HALTs unless `hi + 1 == PIN_MS` (or the given pin). `tc10_window()` = `corridor("2026-09-21T16:00:00Z")` (`:265-266`).

Pin record of TC11: `research_outputs/tierc11/data/AS_OF_PIN.json` sha256 `4f609ccfdf2bc61af2e9e2818ff3cd27aea3f88f7637bd73163b3947c977e4bd` — `as_of_last_closed_4h_close_ms 1790294400000` (2026-09-25T00:00:00Z), `tc10_pin_close_ms 1790006400000` (2026-09-21T16:00:00Z), `bars_4h_past_tc10_pin 20`, write-once law in key `law`.

Snapshots on disk (`ls ~/.cache/naiad/snapshots/`): `tc10_20260921`, `tc11_20260925` only. No TC12 snapshot exists yet.

TC11 snapshot, home-asset 4h tapes (computed from `~/.cache/naiad/snapshots/tc11_20260925/klines/*_4h.parquet`; columns `open_time:int64, open, high, low, close, volume: float64`):

| asset | n bars | first open | last open | tide floor (bar 316) |
|---|---:|---|---|---|
| BTCUSDT | 15,440 | 2019-09-08T16:00Z | 2026-09-24T20:00Z | 2019-10-31T08:00Z |
| ETHUSDT | 14,963 | 2019-11-27T04:00Z | 2026-09-24T20:00Z | 2020-01-18T20:00Z |
| ZECUSDT | 14,542 | 2020-02-05T08:00Z | 2026-09-24T20:00Z | 2020-03-29T00:00Z |
| SOLUSDT | 13,211 | 2020-09-14T04:00Z | 2026-09-24T20:00Z | 2020-11-05T20:00Z |
| NEARUSDT | 13,024 | 2020-10-15T08:00Z | 2026-09-24T20:00Z | 2020-12-07T00:00Z |

Every tape is on an unbroken 4h grid, ends exactly at the pin (0 bars after it). Funding files (`funding_time:int64, funding_rate:float64`) each carry ONE print stamped at 2026-09-25T00:00Z (the pin instant itself). The ten input shas in `books/build_manifest.json` key `input_sha` all re-hash equal on disk (verified this session).

### 1.4 How a book is ridden end to end (the funnel)

`TP.run_cell_n(card, roles, panel, lo_ms, hi_ms, reg_id=None, text=None, reg_root=None, arm=None, head_of_record=None) -> Book` (`tierc10_panel.py:1095-1189`): gate (control only rides free) → window check (`hi` must be a 4h close ≤ corridor end, `:1173-1179`) → `frame_n(s)` per asset (substrate · funding · memo safety, `:590-621`) → `T9.replay9(s, card, roles, lo_ms, hi_ms)` per asset in panel order.

`T9.replay9(sym, card, roles, lo_ms, hi_ms) -> (arms, trades)` (`tierc9.py:334-452`):

1. **Frame** `T5.frame(sym)` (`scripts/tierc5.py:116-135`): the WHOLE 4h file, indicators over the full loaded history; `{"k4","f","x","pv4","fund","fractals","addctx"}`; memoised on the BARE SYMBOL.
2. **Bounds** `lo_i, hi_i = T7._idx_range(open_ms, lo_ms, hi_ms)`; `lo_i = max(lo_i, roles.floor_bars)` (`:382-383`).
3. **ARM** — `armings9(sym, roles, lo_i, hi_i)` (`:168-204`): every window cross (12/89) with `lo_i <= i <= hi_i`; `window_end_i` = first counter cross AFTER i scanning the WHOLE tape (`:185-186`, may be a future bar; `n` if none); tide gate AT THE ARM BAR (`tide_f > tide_s and close > tide_s`, mirrored); displacement `|close - win_s| / ATR >= 0.75`.
4. **TRIGGER** — `card_candidates9` (`:207-232`): gate order tide → d → trigger; the trigger is the FIRST 12/26 cross in `[arm_i, min(window_end_i, hi_i + 1))`; rejects `"tide" | "d" | "no_trigger"`.
5. **SLOT** — candidates sorted `(trigger_i, -direction, kind)` (`:388`); `if ti <= open_until: arm.reject = "position_open"; continue` (`:391-393`); one position per asset.
6. **ENTRY** — at the trigger bar's close: `entry_px = close[ti]`, `entry_i = ti`, `entry_ms = open_ms[ti]` (bar OPEN); no ATR → skipped (`:394-396`).
7. **STRUCTURAL STOP** — `RC.struct_stop_4h(pv4, ti, entry_px, d, atr_sig, min_stop_atr=card.entry_rail_atr, forbidden=None)` (`:397-401`; law at `tierc3_rules.py:237-300`): nearest CONFIRMED 4h (5,5) pivot beyond entry within 200 bars (`conf <= cur_i`), offset 0.5 ATR, railed ≥ 1.0 ATR; None → skipped.
8. **RIDE** — `_ride_leg9` (`:236-331`), per bar j in (ti, hi_i]: top of bar +1R latch and trail arming; harvest touch test; STOP (intrabar, `:296-300`) → BELL at the close (`bell_12_89` / `bell_89_316`, `:303-311`) → HARVEST (`:312-314`) → TRAIL `matched_step` on the (2,2) pivot clock (`:315-323`); default exit `corridor_end` at `close[hi_i]` (`:266`).
9. **ACCOUNT** — `T7._account_chain` (§1.1) → `RC.Trade` (`tierc5_rules.py:566-618`; built at `tierc9.py:409-446`).

`Arming` fields: `symbol, direction, arm_i, arm_ms, window_end_i, tide_ok, disp, d_ok, trigger_i, trigger_ms, entered, reject, strip_d_ok` (`tierc2_rules.py:232-250`). The rejection log exists only in memory (returned `arms`); no books/ file carries rejected armings.

**The 9/12 book** is not the control, so it bypasses `run_cell_n`: `tierc11_books.trg912_book(lo, hi)` calls `T9.replay9(s, TP.CONTROL_CARD, r912(), lo, hi)` per CLASSIC5 asset after `_check_window` (`tierc11_books.py:270-303`).

### 1.5 The filed books (research_outputs/tierc11/books/) — files, shas, schemas

All six files are certified in `research_outputs/tierc11/PROGRESS.json` stage `TC11-BOOKS.artifact_shas` and re-hash equal on disk (verified this session). The four parquets are NOT in git (`.gitignore:287` `research_outputs/tierc11/**/*.parquet`).

| file | bytes | sha256 (file bytes) | content sha (`TB._content_sha`, manifest key `sha`) | rows × cols | key |
|---|---:|---|---|---|---|
| v6_journal.parquet | 70,081 | `deb70b099593f0a8096f3437e0a1aa5dfb5d6a9835dc596d161303ee86b42a5c` | `5952563c9d8fdc689c37fe481aba00459762b3b54628b93b1ec6fe4c79414894` | 200 × 53 | asset, entry_ms |
| v6_campaigns.parquet | 75,048 | `aab06934ae92689ef2e0fcc6b857350cf397ddca7a0a57e180960c51669b28e5` | `a5d0c57087c9b9bb95b61341e798b98eb41a8dc135d07c2eb279db8683ca96dd` | 200 × 64 | symbol, entry_ms |
| trg912_journal.parquet | 70,918 | `1ac9e317f0966c9cfb86a3129d1758590bb949db350993463c006bc33ccaca5f` | `42060018fbceee721fa76e271841b0f955b72adaa249ca93541936531d740536` | 199 × 53 | asset, entry_ms |
| trg912_campaigns.parquet | 75,359 | `46ef63c5fe348871f5601ba2c7768008b195b7934e1cb5dc2f0b49c5a39f87c4` | `ff2b62cbebc657cdc57a6e80b9e393a5ed3b41633e499828de00525628f55fae` | 199 × 64 | symbol, entry_ms |
| build_manifest.json | 7,744 | `04f129b7731f700a3cf5eea0775e0a05792e7abd2ec458585feb4768a196bd24` | — | — | — |
| BOOKS.md | 9,889 | `7b4e37d5b8e00208b52c8fa630a32abe7e08a738e6861e9a624cfb01afb05d5d` | — | — | — |
| FIXTURES_BOOKS.txt | 20,970 | `336a2163e9bd8df8fd40d1fdb6949a0251529c0f34a5c025e4ff6b3d31b45c10` | — | 8 GREEN 0 RED | — |

**Book shas** (`TP._book_sha` = sha256 of the sorted `[symbol, lane, entry_ms, repr(float(net_r))]` rows, FULL float; `tierc10_panel.py:1988-1995`; manifest key `book_sha`): v6 `f3c68f544bcda52c909374105dabbdc773c9bffa4b66b2ef7e0f35ac9b369132` (n 200) · trg912 `2c32fd60924336acc7c48852143d47661a5eb83f12c047ac8b041ad90046e030` (n 199).

**Journal schema (53)** = `tierc5.journal_frame` (`tierc5.py:1058-1097`) + 9 as-of stamps: asset:object · lane:object · entry_ms:int64 · entry_ts:object · direction:object ('long'/'short') · arm_ms:int64 · arm_ts:object · entry_px:float64 · stop_px:float64 · anchor:float64 · anchor_bar_ts:object · anchor_was_sealed_under_the_old_lockbox:bool · r_dist:float64 · atr_at_entry:float64 · r_over_atr:float64 · n_advances:int64 · final_stop_px:float64 · stop_advanced_atr:float64 · ratchet_exit:bool · harvested:bool · harvest_ts:object · harvest_unit_move_r:float64 · harvest_blocked_by:object · net_r_harvest_half:float64 · net_r_runner_half:float64 · harvest_ride_would_have_r:float64 · n_adds:int64 · add_r:object · spring_sweep_ts:object · spring_bars_to_reclaim:object · mfe_r:float64 · mae_to_1r_r:float64 · reached_1r:bool · exit_ms:int64 · exit_ts:object · exit_px:float64 · exit_reason:object · bars_held:int64 · gross_r:float64 · fee_r:float64 · funding_r:float64 · funding_r_uncapped:float64 · funding_ceiling_bound:bool · net_r:float64 · as_of_last_closed_4h:object · as_of_panel_start:object · as_of_span_days:float64 · warranty:object · as_of_lens:object · as_of_last_closed_bar:object · as_of_panel:object · as_of_n_assets:int64 · as_of_substrate:object. The journal has NO bar indices.

**Campaign schema (55 + 9 stamps)** = `CAMPAIGN_COLUMNS` (`tierc11_books.py:193-210`), built by `campaign_rows(book, roles, lo, hi, pool, name)` (`:417-504`): symbol:object · entry_ms:int64 · book:object · roles_name:object · lane:object · direction:int64 (±1) · arm_i:int64 · arm_open_ms:int64 · arm_close_ms:int64 · entry_i:int64 · entry_open_ms:int64 · entry_close_ms:int64 · exit_i:int64 · exit_ms:int64 · exit_close_ms:int64 · exit_event_ms:int64 · exit_event_stamp:object · exit_reason:object · open_at_asof:bool · entry_px:float64 · stop_px:float64 · r_dist:float64 · atr_at_entry:float64 · r_over_atr:float64 · r_over_atr_gt_2p2:bool · lag:int64 · lag_band:object · window_end_i:int64 · window_end_close_ms:Int64 · window_open_at_asof:bool · harvested:bool · harvest_i:Int64 · harvest_close_ms:Int64 · reached_1r:bool · latch_1r_i:Int64 · latch_1r_open_ms:Int64 · net_r:float64 · gross_r:float64 · fee_r:float64 · funding_r:float64 · era_of_entry:object · entry_bar_straddles_era_cut:bool · tide_state_entry:int64 · tide_streak_entry:int64 · tide_left_censored:bool · tide_trailing_edge_q25/q50/q75:float64 · tide_band:object (B1..B4) · tide_band_label:object · tide_abs_gt206:bool · tide_streak_age_arm:int64 · tide_streak_age_arm_censored:bool · entered_after_tc10_pin:bool · continuation:bool · + the 9 `TP.AS_OF_COLUMNS` (`tierc10_panel.py:2557-2560`). Null-iff map at `:211-221`.

Stamp laws (BOOKS.md:9): ms fields are bar OPENs, `*_close_ms = open + 4h`; `entry_close_ms` is the decision instant; a STOP exit is stamped at its bar's OPEN (`exit_event_stamp 'intrabar_open'`), a bell/corridor_end at the close; `latch_1r_open_ms` at its bar's OPEN; `window_end_i` is the end AS KNOWN at the as-of (`known_window_end`, `:396-401`: an open window carries `hi_i + 1`).

**Precision law**: every float column is rounded to 6 dp at write (`TB._round_floats` via `TP.make_put` → `TB.write_table`, `tierc2_baseline.py:162-188`); flags are computed at full precision BEFORE rounding; identity checks must read the Trade objects (BOOKS.md:7).

**v6 at TC11's pin** (BOOKS.md:34-87): n 200 · win 34.50 % (69 positive rows, computed) · open at pin 0 · exit reasons stop 196 / bell_12_89 4 (computed) · per asset BTC 39 / ETH 48 / SOL 36 / NEAR 40 / ZEC 37 · tuning 123 (−1.3238) / holdout 77 (+42.1314) · lag bands 0/1-6/7-15/≥16 = 52/81/4/63 · r_over_atr > 2.2: 53 · bands B1 25 / B2 60 / B3 56 / B4 59 · streak > 206: 120 · left-censored 4 · windows still open at the as-of 3 · first entry 2020-01-27T00:00Z, last entry 2026-09-18T08:00Z, last exit bar opens 2026-09-23T12:00Z (computed).
**9/12 at TC11's pin**: n 199 · ΣR +92.3184 · 1 open (SOLUSDT long entered 2026-09-24T16:00Z, `corridor_end`, −0.031452).

### 1.6 The Σ net_r of the filed v6 book — THREE values on disk, two laws

| value | law | where |
|---|---|---|
| `40.80756457414756` | fsum of full-float `Trade.net_r` | `research_outputs/tierc11/regbooks/P-AGE-1/base.json` key `sum_net_r` |
| `40.807565` | `r6(sum(full-float net_r))` | `books/build_manifest.json` key `net_r_sum.v6`; PROGRESS.json TC11-BOOKS `one_line`; FIXTURES_BOOKS.txt:16; STAGE_G.md:66 |
| `40.807566` | sum of the filed 6-dp `net_r` column | `research_outputs/tierc11/scores/BASE_IDENT.json:48` key `v6.sum_net_r_6dp`; computed this session from `v6_journal.parquet` and `v6_campaigns.parquet` (pandas sum, math.fsum and Decimal sum all `40.807566`) |

The contract's `40.807566` is the 6-dp-column sum. The 9/12 twins: `92.31844` (manifest) vs `92.318442` (column sum, computed).

### 1.7 How F-CTRL proves 0.000e+00, and what "cross-process" means on disk

Comparator: `TP.ctrl_diff(got, want) -> (ok, worst, why)` (`tierc10_panel.py:2712-2724`): both journals sorted on (asset, entry_ms); equal count; worst = max |Δ| over the 12 `TP.CTRL_COLS = ("entry_ms","exit_ms","entry_px","exit_px","stop_px","r_dist","net_r","gross_r","fee_r","funding_r","mfe_r","n_advances")` (`:2707-2709`); identical exit_reason lists; `why = "n=… worst=0.000e+00 exit_reasons_identical=True"`.

TC11's legs (LEANS.md L-1.7, `research_outputs/tierc11/LEANS.md:158-167`; code `tierc11_books.py:508-616`; all held BEFORE any file is written, `compute()` `:783-836`):
- **(a) in-process**: `run_cell_n(control)` vs `tierc6.run_cell(CARD_V6, lo, hi)` (`scripts/tierc6.py:558`) on the TC11 corridor → `n=200 worst=0.000e+00`; `(lo, hi) == TP.control_window()` (BOOKS.md:25).
- **(b) cross-process**: `TP.journal_frame(live)` vs the FILED TC10 journal `research_outputs/tierc10/panel/control_journal.parquet` (sha256 `fcbf5db0480416b0a5c7f704987980aea220650cb0764d5dd4095611fae64c1c`, 200 rows, typed referee `tierc11_books.py:168-169`) at its 6 dp: 199 closed campaigns EXACT on the 12 CTRL_COLS + exit_reason; 1 continuation (ETHUSDT entered 2026-09-18T08:00Z: filed `corridor_end` +3.642965 → live stop +2.707180); 0 new (BOOKS.md:26,80).
- **F-912-ANCHOR**: the 9/12 book ridden over the TC10 WINDOW on the TC11 tape (`corridor("2026-09-21T16:00:00Z")`) hashes to `b2276fa487119ef12a8e0434e54f9b77efbfb7ee387b3cb35d2955043c371a8f` n 198 == `research_outputs/tierc10/registrations/P-TRG-2.scored.json` full-arm `book_sha256`; v6 over the same window hashes to that arm's `base_sha256` `2bd244bfa0a1349ee73aa51e61619e3dda1257eafe3f613df4524a4d87909acd` n 200 (BOOKS.md:27-28). This is the look-back-pin precedent: a book ridden to an EARLIER pin on a LONGER tape reproduces bit-for-bit.
- **F-AGE-ANCHOR / prefix**: TC10-window trailing bands reproduce `P_AGE_1_TIDE_YOUTH.parquet` exactly; 200/200 TC10-window campaigns carry the same band in the TC11 table (BOOKS.md:29-30). **F-WINDOW-ASOF** rebuilds at four earlier pins (FIXTURES_BOOKS.txt:41).

X's third leg, the direct precedent for TC12 (X `scripts/tc11x_books.py:794-926`; X `research_outputs/tierc11x/books/BOOKS_X.md:29-31`):
- (a) at FULL FLOAT on the Trade objects, plus book sha == TC11's certified `book_sha.v6`;
- (c) X's journal as written (6 dp) vs TC11's CERTIFIED `books/v6_journal.parquet` (sha read from TC11's PROGRESS at the reading stage, `deb70b099593f0a8…`): "X 200 · TC11 200 · shared 200 · worst 0.000e+00 on the 12 CTRL_COLS · rows differing 0 · all 44 shared columns equal True".
- X's own `books/v6_x_journal.parquet` hashes to `deb70b099593f0a8096f3437e0a1aa5dfb5d6a9835dc596d161303ee86b42a5c` — BYTE-IDENTICAL to TC11's file, written by another process in another tree (computed this session).
- X's repair XFB-V1 (`tc11x_books.py:796-799`): `TP.ctrl_diff`'s Python `max()` over per-column `np.max` can DROP a NaN column that follows a finite one; X adds a NaN-aware exact compare ("a NaN against a number differs; the worst counts it as inf").

### 1.8 The gated books and the crossed table (what they are, where filed)

Builder: `scripts/tierc11_stage_g.py` (sha `17235ed2078ad37a…`, certified TC11-G). Gates are POST-FILTERS [L-1.5]: `apply_gate(book, refused)` = the base book minus exactly the refused keys, the same Trade objects (`:408-411`). Constants: `AGE_OLD_BAND = 3` (B4), `ABS_TIDE_CUT = 206`, `LAG_CUT = 16`, `SHADOW_LAG = (7, 15)`, `RATR_CUT = 2.2`, `TAKER_BPS_SIDE = 5.0` (`:161-166`).

| book | definition | n | Σ net_r (full float) | file | sha256 |
|---|---|---:|---:|---|---|
| base | v6 | 200 | 40.80756457414756 | `regbooks/P-AGE-1/base.parquet` | `dbfe4788610b11cc70ef64be31aac95949b921f086eaeb66b4535fbbad7af4ce` |
| OLD-gated | v6 minus B4 (entry-bar streak ≥ trailing q75) = P-AGE-1 scored | 141 | 63.464130732724186 | `regbooks/P-AGE-1/scored.parquet` | `6440a6e0d14cfbf1c62df19246a066d0f7086a1e64aae3bb0ced8c2b2a624dca` |
| stale-gated | v6 minus lag ≥ 16 = P-WIN-1 scored | 137 | 51.97401862719062 | `regbooks/P-WIN-1/scored.parquet` | `824c5e08ca79511fea96b98d65b74e8e7209f36379d881a2ff02f927db08241c` |
| far-stop refusal | v6 minus r_over_atr > 2.2 | 147 | 19.115450023555383 | `regbooks/P-WIN-1/tierE__ratr_admission.parquet` | (certified in PROGRESS TC11-G) |
| far-stop PRIORITY (TC11's) | within-window substitute, see §1.9 | 165 | 18.392480226910806 | `regbooks/P-WIN-1/tierE__ratr_priority.parquet` | (certified in PROGRESS TC11-G) |
| **combined (OLD ∪ stale)** | v6 minus (B4 or lag ≥ 16) | **110** | 6-dp sum 56.607239 (computed) | **NOT FILED AS A BOOK** — only the row `age:on¦win:on¦ratr:off` of `stage_g/g_grid_books.parquet` (n 110 · mean +0.5146 · Σ +56.6072 · refused 90, Σ −15.7997; STAGE_G.md:197) and derivable from the flags of `stage_g/g_campaign_gates.parquet` | grid `b2c786e0e7204e1be49c31c0ed7eae7e61365e61ae608dd0efcbe0f4e3b7b51b`; gates `c5a5f486df5709c0386e8733c9cc2490b1a15e6416b6f5adf45efcae608674d6` |

Regbook schema: 16 REQUIRED columns `symbol, entry_ms, entry_close_ms, direction, entry_px, stop_px, r_dist, exit_close_ms, exit_reason, net_r, gross_r, fee_r, funding_r, haircut_net_r, era, lane` (`tierc11_stage_g.py:180-182`) + extras (arm_ms, arm_i, entry_i, exit_ms, exit_px, exit_event_ms, exit_event_stamp, atr_at_entry, mfe_r, n_advances, harvested, reached_1r, slip_bps_side, slippage_tier, lag, r_over_atr, tide_streak_entry, tide_edge_q75, tide_band, tide_streak_age_arm, priority_substitute, harvest_close_ms, as-of stamps) — full float, NOT 6-dp. `g_campaign_gates.parquet` (200 × 41) carries every flag: `age_old_refused, age_abs206_refused, win_refused, lag7_15_refused, ratr_refused, grid_cell` plus the facts.

**The slippage twin** is `haircut_net_r = net_r − fee_r × slip_bps_side / 5.0` [AM-7] (`tierc11_stage_g.py:611-615`; `HAIRCUT_LAW` `:195-197`), slip = the stem's charter tier from `E.fees()` (A 2 / B 5 / C 10 bps/side; BTC ETH = A, SOL NEAR ZEC = B; `research_outputs/tierc11/data/fee_schedule.json` sha256 `6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b`). It lives in the regbooks and the ledgers, not in `books/*.parquet`.

**The crossed 2×2×2 of TC11** (STAGE_G.md:172-198): (a) the PARTITION by flags A (OLD) · W (lag ≥ 16) · S (r_over_atr > 2.2): A0W0S0 81 / A0W0S1 29 / A0W1S0 23 / A0W1S1 8 / A1W0S0 21 / A1W0S1 6 / A1W1S0 22 / A1W1S1 10; (b) the eight gate BOOKS. `ratr:on` alone refuses 53 campaigns worth +21.6921 R (STAGE_G.md:62,192) — the contract's "+21.69R".

### 1.9 Slot arbitration as it exists today

- **The only rule**: one position per asset, first trigger wins, `ti <= open_until` → `position_open` (`tierc9.py:388-393`). A window takes its FIRST trigger only (`card_candidates9` `:225-229`); a rejected window is dead.
- **Windows of one asset are disjoint in time**: a window ends at the counter 12/89 cross, which is the next window's arm (`tierc11_stage_g.py:70-73`). Two armings can therefore contend for the slot only through a campaign still open at a later window's trigger.
- **Measured on TC11's corridor** (STAGE_G.md:205, 679-685): "position_open rejections v6 0, priority 0; substitute crosses skipped for 'asset not flat' 0; campaigns exiting AFTER their window's end bar v6 0 … 'asset flat' never binds and the re-ride rival is 0 for every gate". The rival log `g_rivals.parquet` is one placeholder row. 200 candidate windows → 200 entries (`g_priority_windows.parquet`, 200 rows).
- **TC11's PRIORITY book** [L-G.3] — `replay_g(sym, lo_ms, hi_ms, *, refuse=None, priority_cut=None, pool=None) -> (trades, window log)` (`tierc11_stage_g.py:449-534`): a window whose FIRST trigger has r_over_atr > 2.2 is PASSED and the entry becomes the first LATER same-direction 12/26 cross with the asset flat and r_over_atr ≤ 2.2. It prefers the NEARER stop. Outcomes: entered 147 / passed_no_substitute 35 / passed_substituted 18 → n 165, Σ +18.392480 (STAGE_G.md:202-203).
- **Cross-asset same-close collisions** (disclosure; "cannot bind: one position per ASSET, no portfolio cap", STAGE_G.md:643-647): v6 has 10 collision closes involving 21 campaigns, max 3 assets at one close, 0 collisions of mixed r/ATR class.
- `replay_g` with no hook is proven == the v6 book (`TP._book_sha f3c68f54…`, STAGE_G.md:204); it rides with `tierc11_ride.ride11` / `trade11`.

### 1.10 The "funnel instants" that exist as rows

TC11 R3's instant law: `tierc11_stage_r.instants_of(reg, kind, laws=None)` (`scripts/tierc11_stage_r.py:1267-…`), `KINDS = {"v6transform": {"lens":"4h","start":"arm"}, "lane4h": {…"entry"}, "relay": {…"arm"}, "scalp5m": {"lens":"5m","start":"entry"}}` (`:213-216`); key `NEST_KEY = ["scale_kind","symbol","entry_ms","instant_kind","instant_ms"]` (`:258`). "Per campaign, every close of its own lens from its arm (or entry) through its exit stamp of record, plus its named events"; a campaign open at the pin gets `as_of_pin`, never `exit`; an UNSTAMPED recorded event HALTs the door.

Filed: `research_outputs/tierc11/stage_r/NEST_v6.parquet` (sha256 `de27be17325fada7e8033cb295508a8bc4b65eccdcd632f512bb874e6138cb11`, 19,386 × 127) and `NEST_trg912.parquet` (sha256 `7c5ffe231deb10d982b36fbc5068a26941db66c8e8dc8f92746b2eed7b383ef9`, 21,416 rows). Per `scale_kind` (two kinds, identical instant sets):

| instant_kind | v6 | trg912 | stamp law |
|---|---:|---:|---|
| arm | 200 | 199 | close (arm_close_ms) |
| bar_close | 8,632 | 9,626 | close (4h bar), arm close through exit |
| entry | 200 | 199 | close |
| plus_1r | 103 | 112 | intrabar — the OPEN of its 4h bar |
| plus_1r_post_event | 103 | 112 | post-event twin (close) |
| harvest | 55 | 63 | close |
| bell | 4 | 7 | close |
| exit | 200 | 198 | stop: OPEN of its bar (196 of v6); bell: close |
| exit_post_event | 196 | 191 | post-event twin (close) |
| as_of_pin | 0 | 1 | open at the pin |
| **total** | **9,693** | **10,708** | |

The vector is stamped at lenses 1h · 4h · 12h · 1d · 1w (column prefixes of NEST_v6.parquet) — the same five the contract's V5 names. Each lens block carries `<L>_bar_close_ms` (the lens bar actually used). The gated books were stamped as lanes: `stage_r/lanes/NEST_P-AGE-1.parquet`, `NEST_P-WIN-1.parquet` (+ six more registrations).
Only ENTERED campaigns have instants. Armings rejected at tide / d / no_trigger exist nowhere on disk.

### 1.11 Tide age, the trailing q75, and why it is prefix-stable

- Age of record [L-G.1]: `LR.tide_streak(sym) -> (state, run, start)` (`scripts/tierc7_lab_regime.py:306-349`): run length of sign(e89 − e316) on 4h, counted from the warm floor `TIDE_WARM_BARS = 316` (`:179`); read at the ENTRY bar (`tierc11_books.entry_streak`, `:363-368`).
- Pool: `T9._trailing_pool(lo_ms, hi_ms)` (`tierc9.py:1290-1315`): every bar of the five `RC.UNIVERSE` assets with open in `[lo, hi]` and `run > 0`, with times, sorted (mergesort).
- Edges: `T9._trailing_edges(pool, at_ms)["streak_bar"]` (`:1318-1328`): `np.quantile` at `STREAK_BAND_QUANTILES = (0.25, 0.50, 0.75)` (`tierc7_lab_regime.py:181`) over the pooled prefix `open_ms <= at_ms` (INCLUSIVE of the entry bar and of other assets' bars with that open), or None while the prefix holds < `RC.PROVISIONAL_MIN_N` = 30 bars.
- Band: `LR._streak_band(run, edges) = np.digitize(run, edges)` (`:456-459`), 0..3 = `STREAK_LABELS ("B1 YOUNG tide","B2 EARLY tide","B3 MATURE tide","B4 OLD tide")` (`:446-447`); B4 OLD ⇔ run ≥ trailing q75.
- **Dependence**: the edge at an entry bar depends only on (pool lo, the five tapes' bars with open ≤ the entry bar). Extending `hi` appends later bars and cannot move it. X pins the lower bound: `pool_lo_ms 1567958400000` (2019-09-08T16:00:00Z) in X `forward/BOOK_SPECS.json` and X `books/build_manifest.json`, asserted at every refresh (FWD-LO-MOVED).
- Trailing q75 over the v6 book ranges 188.0 … 602.0; the last entries carry q75 396.0 / q50 206.0 (computed from `v6_campaigns.parquet`).
- The WHOLE-corridor edges (`LR.cuts`, `:416-440`) are `[88.0, 206.0, 396.0]` on both the TC10 window and the TC11 corridor (BOOKS.md:89); they are corridor-dependent and used only for the shadow caveat.
- Other age on disk (disclosure only): `T9.tide_streak_age(t, roles)` at the ARM bar, three-state (`tierc9.py:537-560`).
- Era [L-1.3]: `E.era_of(close_ms)` — tuning iff the entry bar's CLOSE ≤ `ERA_CUT_MS = 1_719_791_999_000` (2024-06-30T23:59:59Z) (`tierc11_env.py:128,1047-1055`).

### 1.12 The two forward ledgers

| | TC11's (MAIN tree) | TC11-X's (X worktree, not merged) |
|---|---|---|
| file | `research_outputs/tierc11/forward/FORWARD_LEDGER.jsonl` | `research_outputs/tierc11x/forward/FORWARD_LEDGER.jsonl` |
| sha256 | `e53328add9e71f1c6198f724a131565a2a10ad2ad1600c36a74c6676f7ada288` (3,442 B, 2 lines, tracked) | `4a6da7e89a3cf5f0127f76aca0d2ae12d218ffc06417c6528c70210092cfa4c5` (5,643 B) |
| books | 2: `v6`, `trg912` (`tierc11_forward_ledger.py:83`) | 3: `v6` (X twin), `trg912` (X twin), `gated-v6-oldtide` (of record) (`BOOK_SPECS.json` key `book_order`) |
| chain law | `line_sha256` = sha256 of the canonical line without `line_sha256`; kinds GENESIS / CAMPAIGN / REFRESH | `forward_log.chain_hash(line, prev)`; kinds book_open / refresh / row |
| opening | 2026-09-21T16:00:00Z (`OPENING_MS`, `:80`) | the same, read from TC10's STEP0_RECORD |
| head | `0db889425ef8e3d2075a2a3cf2d1b500c3b0bbc7f7b4d535ffa3dec3575261cb` | last refresh line `61ea177fadcc82ba…` |
| appended rows | 0 / 0 | 0 / 0 / 0 |
| open at the pin | 9/12: SOLUSDT long 2026-09-24T16:00Z | the same |

X frozen spec: `forward/BOOK_SPECS.json` sha256 `72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`; it pins `path_modules` (21 files with sha256: the 17 lineage scripts + engine/indicators.py, engine/s1.py + X's own). All 17 lineage scripts and the three engine files re-hash IDENTICAL in MAIN and X (computed this session).
As-of-STABLE row fields vs `AS_OF_DEPENDENT = ("window_end_i","window_end_close_ms","window_open_at_asof","open_at_asof","continuation","entered_after_tc10_pin")` (`tierc11_forward_ledger.py:94-108`).
TC11's ledger states its own limit: "a refresh on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record" (`FORWARD_LEDGER.md` last line; `tierc11_forward_ledger.py:43-48`).

### 1.13 Determinism conventions

- Seeds: TC11 `SEED = 20260924`, `SEED_SENS = 20260816` (the lineage's `T5.SEED`), `N_BOOT = 4000` (`tierc11_env.py:125-127`); X `SEED = 20260925`. The books draw nothing.
- F-DET: `DET_SEEDS = (1, SEED)`; two SUBPROCESS builds under `PYTHONHASHSEED` 1 and SEED into `<stage out>/_det_<stage>/seed_<s>/`; the break leg plants a hash-order-dependent emission into `hashorder_<s>/` (`tierc11_books_fixtures.py:1284,1323,1339`). Claim: every file byte-identical seed 1 == seed SEED == canonical, every parquet content sha equal (FIXTURES_BOOKS.txt:51).
- `--out-dir=DIR` is guarded: only OUT, a direct child of `OUT/_det_<stage>/`, or a child of a `_det_<stage>/` directory OUTSIDE the repo (`tierc11_books._guard_out`, `:998-1010`).
- Table law: sort on a declared TOTAL key (mergesort), round floats to 6 dp, content sha = sha256 of `df.to_csv(index=False)`, atomic write (`tierc2_baseline.py:155-188`); manifests `json.dumps(indent=2, sort_keys=True)`; reports carry no clock, no temp path; `VOLATILE_META = ("wall_clock_at_run","cache_lag_hours")` are never stamped (`tierc10_panel.py:625`).
- Fixture law: two legs per fixture, the BREAK leg first, RED or the fixture is VOID; a plant counts only if a finding names its intended detector (`tierc11_books_fixtures.py` docstring).
- `.gitignore:287-288`: `research_outputs/tierc11/**/*.parquet` and `research_outputs/tierc11/**/_det_*/` — a TC11-only rule.

### 1.14 The X worktree's vendored env — how X used TC11 code without touching it

- X's tree has NO `scripts/tierc11_env.py`, `tierc11_books.py`, `tierc11_ride.py` (it branched at `e97ad73`; merge-base with MAIN is `e97ad7390c6212273b0e06daf33a463d4106c9d1`); only `tierc11_data.py`, `tierc11_data_fixtures.py`, `tierc11_registrations.py`.
- **Referee**: `research_outputs/tierc11x/vendor/tierc11_env@086d66da.py`, sha256 `086d66da0609043834df59336e107acd8b202a39a697a8f012d6a1845f52d82c` (68,355 B) — "a byte-for-byte copy of TC11's untracked scripts/tierc11_env.py, taken from the main tree … never imported" (`vendor/README.md`).
- **Build**: `scripts/tc11x_env.py` (sha256 `db74225e6fa26bf7e9c2e19f31b6e0c76b379a8de72ef4c0cc9e6b1a2e653928`) = the referee + the declared hunks 1-9, filed AS DATA in `scripts/tc11x_data.py` (`ENV_HUNKS`, `:629-633`; `H(no, what, old, new)` calls `:637-1359`); **F-VENDOR** reverts the hunks and must meet the referee byte for byte (`scripts/tc11x_env_fixtures.py:22,365`).
- Hunks by number: 1 header/SEED · 2 `OUT → tierc11x`, `TC11_REC`, `TC11_LIVE` · 3 re-roots (D.OUT, TP.AS_OF_PIN, STAGE_D_MANIFEST, fees) + the extraction re-hash · 4 write-protection of `research_outputs/tierc11/`, `data/tc11_rec/`, `scripts/tierc11_*` · 5 `TC11_ALLOW` in three classes + the hook's TC11 judge · 6 `NEST_MODULE = "tc11x_ranges"` · 7 `tc11x_*` exempt from the binding scan · 8 messages · 9 the TC10 allow-list.
- **Sha-first read law** [LX-0.3]: TC11 records are read by ABSOLUTE MAIN-tree path, each asserted equal to the sha TC11's PROGRESS certifies at the reading stage; text records are extracted into `research_outputs/tierc11x/data/tc11_rec/`; every read is filed in `data/TC11_READS_<stage>.json`; "TC11's CERTIFIED books are the referees, never inputs" (`tc11x_books.py` docstring).
- X did NOT vendor tierc11_books; it wrote its own twin `scripts/tc11x_books.py` (sha256 `26870ff97317801fdf9c4874e1f41cdac69bacbf9263198e623e19ab19913b2b`) and held it to TC11's files by F-CTRL (c).
- **The referee is no longer TC11's shim of record**: MAIN `scripts/tierc11_env.py` is sha256 `1526093b25161927337ced6112a310075b1a57c825f08705814e48619398f798` (68,545 B; certified TC11-ENV; tracked since `ba66d95`). `diff` of the two files shows five hunks, all AM-1: two records (`census/height_toll_verdict.parquet`, `census/outcome_grid.parquet`) moved from `TC10_AMENDMENT_CANDIDATES` into `TC10_ALLOW` (six → eight, `tierc11_env.py:153-157`) and the matching docstring / comment / lean-block wording. No logic differs.
- Reusable X helper, pure: `scripts/tc11x_pct.py` `trailing_pct(arr, i, window, floor)` (midrank, inclusive of i, None below floor), sha256 `49809c070ed00223a345edc51b5d83355f229a6b1372495038ff42aeba204bb7`.

### 1.15 Signatures TC12 can import (through a shim) or must mirror

```
engine.data.cache_dir() -> Path                                               engine/data.py:39
tierc2_baseline: load_klines(sym, tf) · load_funding(sym) · _idx_range(open_ms, lo_ms, hi_ms)
                 r6(x) · _content_sha(df) · _round_floats(df, nd=6) · write_table(df, name, keys, root)
tierc5.frame(sym) -> dict · tierc5.journal_frame(book) -> DataFrame           tierc5.py:116, 1058
tierc6.run_cell(card, lo_ms, hi_ms, wall_lens=None) -> list                   tierc6.py:558
tierc7._account_chain(sym, card, direction, r_dist, chain) -> dict            tierc7.py:350
tierc7_lab_regime.tide_streak(sym) -> (state, run, start) · _streak_band(run, edges) · cuts(lo, hi)
tierc9.Roles · V6_ROLES · SWEEP_CELLS · role_arrays(sym, roles) · armings9(sym, roles, lo_i, hi_i)
       card_candidates9(sym, roles, lo_i, hi_i) -> (arms, cands) · replay9(sym, card, roles, lo_ms, hi_ms)
       _trailing_pool(lo_ms, hi_ms) -> dict · _trailing_edges(pool, at_ms) -> dict · tide_streak_age(t, roles)
tierc10_panel: substrate() · stage_d_pin() · corridor_n(panel, pin_close_iso=None, floor_bars=316)
       run_cell_n(card, roles, panel, lo_ms, hi_ms, …) -> Book · is_control_book · ride_spec(card, roles)
       _book_sha(book) · CTRL_COLS · ctrl_diff(got, want) · control_window() · ctrl_prefix(live, filed, edge, label)
       make_put(root, meta, lens="4h") -> (put, W, K, SK) · stamp_n · lens_edge(hi_ms, lens) · AS_OF_COLUMNS
       check_keys(root, manifest=None) · check_det(root_a, root_b) · input_sha(panel)
tierc11_env: guard_substrate · tc10_record(rel) · fees() · era_of(close_ms) · static_imports(src) · hook_escapes(src)
tierc11_books: corridor(pin_close_iso=None) · v6_book(lo, hi) · trg912_book(lo, hi) · r912() · book_sha(book)
       tide_pool(lo, hi) · entry_streak(t) · trailing_edges(t, pool) · band_of(run, edges) · lag_band(lag)
       known_window_end(end_i, hi_i) · exit_event(t) · plus_1r_bar(f, t) · campaign_rows(book, roles, lo, hi, pool, name)
       ctrl_a(lo, hi, book=None) · ctrl_b_findings(live, filed, tc10_close_ms) · key_findings(...)
tierc11_ride: ride11(sym, card, roles, d, ti, entry_px, stop0, r_dist, hi_i, *, walk, warn, tp, state, j0, …, ctx)
       trade11(sym, card, roles, d, *, arm_i, arm_ms, disp, entry_i, entry_ms, entry_px, stp, atr_sig, leg, lane, entry_close_ms)
tierc11_stage_g: replay_g(sym, lo_ms, hi_ms, *, refuse=None, priority_cut=None, pool=None) · refuse_hook(gate, pool)
       apply_gate(book, refused) · facts_of(t, pool) · haircut(stem, net_r, fee_r) · canonical_csv(df) · book_sha256(df)
```

---------------------------------------------------------------------------------------------------
## 2 · CONTRACT-vs-DISK

**C1 · "Σ net_r 40.807566 at its pin"** — three values on disk (§1.6). `40.807566` is the sum of the filed 6-dp column (`scores/BASE_IDENT.json:48`), not the number TC11 prints as the book's ΣR (`40.807565` in the books manifest, PROGRESS, STAGE_G.md, FIXTURES_BOOKS.txt). Both are true; they are different laws.

**C2 · "F-CTRL reproduces TC11's filed v6 book trade-by-trade to 0.000e+00 on TC11's corridor … cross-process anchored"** — nothing on disk can do this as written: `tierc11_env.guard_substrate` HALTs on any snapshot but `tc11_20260925` (`tierc11_env.py:206-208`), `PIN_MS` is typed (`:122`), `tierc11_books.corridor()` HALTs unless `hi + 1 == PIN_MS` (`tierc11_books.py:259-261`), and TC11's own ledger says so (`FORWARD_LEDGER.md` LIMIT line). "Cross-process" on disk means a referee FILED by another process: TC11's (b) vs TC10's journal, X's (c) vs TC11's journal.

**C3 · "the filed v6 book"** — the parquets are gitignored (`.gitignore:287`). They exist only in the MAIN working tree; a linked or detached worktree does not carry them. Their byte shas are tracked in `research_outputs/tierc11/PROGRESS.json` (TC11-BOOKS), their content shas in the tracked `books/build_manifest.json`.

**C4 · "far-stop PRIORITY simulated as slot arbitration (when two armings compete for an asset, prefer the farther structural stop …)"** — on the TC11 corridor two armings NEVER compete for an asset: 0 `position_open` rejections, 0 rivals for every gate, 'asset flat' never binds (STAGE_G.md:205, 679-685). The only "priority" book on disk prefers the NEARER stop and is a within-window substitution, not slot arbitration (`replay_g(priority_cut=2.2)`). The +21.69 R is the refused cohort of the far-stop REFUSAL (53 campaigns, +21.6921 R, STAGE_G.md:62). Read as per-asset slot arbitration, the contract's twin is the v6 book itself on TC11's corridor.

**C5 · "the crossed table 2×2×2×2 (OLD · stale · far stop · low breadth)"** — TC11 filed 2×2×2 two ways (partition and gate books). A 16-cell PARTITION needs no arbitration; a 16-cell GATE-BOOK table would need far-stop as a refusal, which the same sentence forbids.

**C6 · "the combined refusal … (TC11 crossed table cell 110 @ +0.515)"** — confirmed: cell `age:on¦win:on¦ratr:off` n 110, mean +0.5146, Σ +56.6072 (STAGE_G.md:197). It is a table row; no combined-gated book file exists in either tree.

**C7 · "all four books (base · 9/12 · OLD-gated · combined-gated) … F-LEDGER (append-only on the three existing books; the fourth re-hashes)"** — the three existing books live in TWO ledgers with two different chain laws, in two trees: TC11's ledger holds base + 9/12; X's unmerged ledger holds the OLD-gated book of record plus its own twins of base and 9/12 (§1.12). Neither file may be written (TC11's is a frozen record whose own foundation is pinned to the TC11 snapshot; X's tree may not gain a file).

**C8 · "the bars since 2026-09-21T16:00Z" (Stage L) vs "TC11's corridor" (Stage C)** — two boundaries. The ledger's opening is TC10's pin; the control's corridor ends at TC11's pin (2026-09-25T00:00Z). Between them v6 has 0 entries (BOOKS.md:70) and one continuation (ETH, entered 2026-09-18T08:00Z, stopped 2026-09-23T12:00Z, +2.707180); 9/12 has one entry (SOL, 2026-09-24T16:00Z, open at TC11's pin).

**C9 · "the forward strip, never scored"** — the contract does not say whether campaigns entered after TC11's pin are excluded from the SCORED books of Stages G / R / S ("full corridor", "HOLDOUT era") or only printed apart.

**C10 · "every funnel instant of every book"** — rows exist only for ENTERED campaigns (§1.10). The pre-entry funnel (armings rejected at tide / d / no_trigger) is in memory only.

**C11 · "`data/fee_schedule.json` must carry maker_bps_side per venue"** — no `data/fee_schedule.json` at the repo root. The records are `research_outputs/tierc10/data/fee_schedule.json` and `research_outputs/tierc11/data/fee_schedule.json`; TC11's already carries a maker figure under the key `maker_bps_per_side` (2.0, per ASSET row and at top level), `maker_kind` = "ASSUMPTION — Binance USDT-M VIP0 maker per README …". `tierc11_env.fees()` reads the keys `taker_bps_side_used, round_trip_bps_used, maker_bps_per_side, maker_round_trip_bps, maker_kind, maker_slippage_bps_side, charter_slippage_bps_per_side, charter_slippage_tier` (`tierc11_env.py:1031-1043`). No key named `maker_bps_side` exists.

**C12 · "decision modules import NOTHING from it — import-closure extends to it"** — the existing fixture cannot be "extended" by a flag: it globs `tierc11_*.py`, types TC11's runners and pins `tc11_20260925`; and `analytics` + `analytics.profile` are already inside the decision lineage (§1.2). `"value_area"` is not in any FORBIDDEN tuple.

**C13 · "the absolute-206 cut"** — 206 is `ABS_TIDE_CUT` (`tierc11_books.py:155`, `tierc11_stage_g.py:158`), defined as the whole-corridor MEDIAN edge and labelled look-ahead; whole-corridor edges are corridor-dependent and may no longer read `[88, 206, 396]` on a longer corridor.

**C14 · "breadth = share of the five home assets whose tide band is YOUNG or EARLY"** — 16 of the 200 v6 entries occur before all five assets have a tide (assets past their floor at the entry bar: 2 → 2 entries, 3 → 12, 4 → 2, 5 → 184; computed from `v6_campaigns.parquet` and the tape floors of §1.3). The band also needs ≥ 30 pooled bars.

**C15 · "stamp TC11 BUILT and re-pin its registry files"** (rulings) — TC11's close is still the operator's: `research_outputs/tierc11/close/close_acts.sh` step 0 requires its SOURCES equal to HEAD and re-runs F-LAR11 "every «cite» against its source as it stands NOW" (`close_acts.sh:8-11,56-66`). TC11 PROGRESS `resume_point` = "TC11-CLOSE (… close_acts.sh ordered after TC10's close)".

---------------------------------------------------------------------------------------------------
## 3 · READINGS NEEDED (candidate leans)

**R1 · The shim for the extended corridor.**
Options: (a) vendor `scripts/tierc11_env.py` at its CERTIFIED sha `1526093b…` into `tierc12_env.py` by declared hunks filed as data, F-VENDOR reverting them to the referee (X's LX-0.4 law); (b) edit tierc11_env in place; (c) a fresh shim.
Recommend (a). Hunks needed: SNAPSHOT name · PIN_MS/PIN_ISO READ from Stage D's write-once pin record (never typed) · SEED 20261008 · OUT → `research_outputs/tierc12` · re-roots (D.OUT, TP.AS_OF_PIN, TP.STAGE_D_MANIFEST, fees()) · write-protection widened to `research_outputs/tierc11/`, `scripts/tierc11_*`, the X worktree root and `tc11_20260925` · a sha-first `TC11_ALLOW` / `X_ALLOW` · FORBIDDEN + `"value_area"`. Referee = MAIN's file at the sha TC11's PROGRESS certifies, not X's older vendor copy.

**R2 · What F-CTRL asserts.**
Options: (i) LOOK-BACK PIN — ride v6 on the TC12 tape with `hi = TC11 pin − 1` (`corridor_n(CLASSIC5, pin_close_iso=<TC11 pin>)`) and demand `TP._book_sha == f3c68f54…` (full float), n 200, and `ctrl_diff` vs the filed `v6_journal.parquet` == 0.000e+00 with every shared as-of-stable column equal; (ii) PREFIX — ride the extended corridor and hold the filed campaigns as a prefix (closed exact; `corridor_end` rows as continuations; live-only rows entered after TC11's pin).
Recommend BOTH, (i) as the leg of record. It is the F-912-ANCHOR precedent, it is bit-exact at full float so no 6-dp rounding can hide a drift, and it also reproduces the 9/12 book including its open SOL row (`2c32fd60…`, n 199). Keep (a) in-process vs `tierc6.run_cell(CARD_V6)` on the extended corridor. Use X's NaN-aware exact compare beside `TP.ctrl_diff`.

**R3 · Which Σ is "40.807566".**
Options: assert the 6-dp-column sum; assert r6 of the full-float sum; both.
Recommend both, each under its own name, each READ: `Σ(6-dp column) == BASE_IDENT.json v6.sum_net_r_6dp` (40.807566, the contract's number) and `r6(fsum(Trade.net_r)) == books/build_manifest.json net_r_sum.v6` (40.807565). Print the full-float sum beside (`regbooks/P-AGE-1/base.json sum_net_r`).

**R4 · "Cross-process anchored".**
Options: (a) the referee is TC11's FILED parquet, read by absolute MAIN path, its sha asserted equal to the sha TC11's PROGRESS certifies at the reading stage (X's law), plus the book sha against the tracked manifest; (b) two TC12 subprocesses compared to each other.
Recommend (a) as the anchor and (b) as F-DET. (b) alone is self-comparison across time, which the fixture law bans.

**R5 · TC10 anchors.**
Options: re-hold F-CTRL(b) vs TC10's journal, F-912-ANCHOR vs P-TRG-2 and F-AGE-ANCHOR vs P_AGE_1 on the TC12 tape; or inherit them through TC11's certified books.
Recommend inherit: TC11's books are the referees, TC10's records are not re-read (a shorter allow-list on closed, operator-pending records). Print the inheritance chain with its shas.

**R6 · The corridor of record for SCORING.**
Options: (a) one corridor = the extended pin for stamps and as-of, but every scored book of TC12 excludes campaigns whose entry close is after TC11's pin (1790294400000); (b) scored books include the extension.
Recommend (a) for every family. It keeps P-ADM-1's pre_seen cell (110 @ +0.5146) exactly reproducible, and it leaves the ledger's first appended rows unspent — a campaign cannot be both in-sample evidence and forward confirmation. This is the reading that cannot flatter. Needs the orchestrator's ruling because it binds Stages G, R and S, not only C.

**R7 · The forward strip's boundary.**
Options: entry close > TC11's pin (Stage C's corridor), or > 2026-09-21T16:00Z (the ledger's opening).
Recommend: Stage C's strip = entry close > TC11's pin; Stage L keeps the opening of record (TC10's pin). Print both; say that for v6 the two memberships are identical (0 entries between the pins) and for 9/12 they differ by the SOL row.

**R8 · Far-stop PRIORITY as slot arbitration.**
Options: (A) per-asset slot: replay9's loop with ONE change — when a trigger finds the slot held (`ti <= open_until`), or two candidates share a trigger bar, the candidate with the larger `r_over_atr` (read at its own trigger bar) takes the slot; nothing is refused; (B) the mirror of TC11's within-window substitute (pass a near-stop first trigger, wait for a far one); (C) cross-asset arbitration under a portfolio cap.
Recommend (A), with the count of arbitration events printed FIRST and the row declared precondition-closed when it is 0 — as it is on TC11's corridor (STAGE_G.md:205), where the book is v6 itself. (B) passes a trigger, which is a refusal the contract forbids, and it waits for a future cross. (C) needs a cap that no file supplies. Flag C4 to APOLLO as a finding, not a fix.

**R9 · The crossed 2×2×2×2.**
Options: 16-cell PARTITION of the v6 book by four flags; 16 gate books.
Recommend the partition, whole (F-GRID 16 cells, n = 0 cells carried with a nan_reason), with the three refusals' eight gate books beside it and the far-stop axis as a FLAG only (`r_over_atr > 2.2`, TC11's `RATR_CUT`, read by object).

**R10 · Gates: post-filter or re-ride.**
Recommend TC11's L-1.5 for every refusal of TC12 (P-ADM-1, P-BRD-1, P-DIR-1 and the shadows): gated = v6 minus exactly the refused keys, row-identical; the re-ride rival printed as a disclosure (`replay_g(refuse=…)`), as TC11 and X both did (X: `n_reride_differs 0 · 0`).

**R11 · "The gated books" of V5 and L.**
Recommend: OLD-gated = P-AGE-1's scored arm verbatim (n 141 at TC11's pin; must equal `regbooks/P-AGE-1/scored.parquet` on its keys) and combined-gated = v6 minus (B4 ∪ lag ≥ 16) (n 110; must equal the flags of `g_campaign_gates.parquet`). Shadows (stale alone 137, absolute-206 80) are tables, not ledger books. Stamp the v6 instant set once; every gated book's stamps are the subset by key (assert the subset).

**R12 · The funnel-instant set.**
Options: TC11's R3 law (entered campaigns; kinds of §1.10) or the whole arming funnel.
Recommend TC11's law, transcribed, and anchored cross-process: on TC11's corridor the key set must equal `NEST_v6.parquet`'s (9,693 keys at one scale_kind) and `NEST_trg912.parquet`'s (10,708). Rejected armings are not rows on disk; adding them is a contract amendment.

**R13 · Breadth's denominator and clock.**
Options: denominator fixed at 5 with an asset that has no band (pre-floor, or < 30 pooled bars) counted as NOT young; or the share among assets that have a band.
Recommend the literal text: /5, a missing band is not YOUNG/EARLY, `n_banded` printed on every row and the available-denominator twin in the Tier-E grid. Other assets are read at the bar with the SAME open_ms as the entry bar (by time, never by index — the five tapes have different lengths).

**R14 · The trailing pool's lower bound.**
Recommend: pin `pool_lo_ms = 1567958400000` READ from X's `forward/BOOK_SPECS.json` (== `TP.corridor_n`'s panel start) and HALT if the TC12 corridor's `lo` differs (X's FWD-LO-MOVED).

**R15 · The ride code is frozen.**
Recommend: before riding, re-hash the lineage path modules and require equality with X's `BOOK_SPECS.json path_modules` (17 lineage scripts + engine/indicators.py + engine/s1.py — identical in both trees today). A drifted module HALTs.

**R16 · Non-control books and `run_cell_n`.**
Recommend: only the control goes through `TP.run_cell_n`. The 9/12, the arbitration twin and every re-ride call `T9.replay9` / a `replay_g`-style loop directly, as `trg912_book` does — `run_cell_n` would demand a registration in TC10's write-protected registry.

**R17 · The absolute-206 shadow.**
Recommend: 206 read by object (TC11's `ABS_TIDE_CUT`), printed with TC11's caveat verbatim, and the whole-corridor edges of the extended corridor printed beside it so a moved median is visible.

---------------------------------------------------------------------------------------------------
## 4 · HAZARDS

**Substrate and isolation**
- H1 · `tierc2_baseline` binds KLINES/FUNDING at import; `cache_dir()` falls back to the LIVE cache when the variable is unset and `mkdir`s whatever path it is given (`engine/data.py:39-48`) — a mistyped snapshot name silently creates an empty directory.
- H2 · Memos keyed on the bare symbol (`T5._FRAMES`, `T9._RA`, `LR._TIDE`, `LR._RV`, `T8._SERIES`) and on `(lo, hi)` (`LR._CUTS`): one process = one substrate. Riding TC11's window and the extended corridor in ONE process on ONE tape is safe (it is how TC11 rode TC10's window); loading two snapshots in one process is not.
- H3 · Every shim import of a `tierc10_*` module needs `~/.cache/naiad/snapshots/tc10_20260921/klines/` to exist (`tierc10_data.py:94-117`). A LaCie mirror or residency move that relocates it breaks the import windows.
- H4 · TC11's hook protects `tierc10` only. It does NOT write-protect `research_outputs/tierc11/`, `scripts/tierc11_*`, or the X worktree — the X worktree sits UNDER the main tree's path and classifies as plain "repo" (`tierc11_env.py:395-416`). A TC12 process could write into X unrefused.
- H5 · The hook cannot see pyarrow-native I/O, `to_parquet(partition_cols=…)`, subprocess, ctypes (`tierc11_env.py:74-84`); `hook_escapes` is the only ban.
- H6 · TC11's referee parquets are untracked: `git clean -x`, a careless checkout or a rebuild of TC11 would destroy or replace the F-CTRL referee. Read them by absolute MAIN path, sha-first.
- H7 · `.gitignore` is write-protected by the hook and its TC11 rule does not cover `research_outputs/tierc12/`. A TC12 rule must be appended by a plain process BEFORE any shim is armed, at the END of the file (TC10 cites `.gitignore:263`, TC11's own text cites `:287`).
- H8 · X baseline to attest before and after: HEAD `7b24f835…`, status exactly `?? research_outputs/tierc11x/close/CERTIFIED_TIP`, no `scripts/__pycache__` in X today (MAIN has one).

**Causality (look-ahead)**
- H9 · `armings9` scans the WHOLE tape for `window_end_i` (`tierc9.py:185-186`); only `known_window_end` and `card_candidates9`'s `min(window_end_i, hi_i + 1)` keep it causal. On a look-back pin the frames hold the later bars.
- H10 · The tide age of record is at the ENTRY bar and banded on the TRAILING inclusive prefix. The rivals are all look-ahead or a different quantity: whole-corridor edges (`LR.cuts`), the absolute 206, the arm-bar age, a one-bar-ahead pool, a strict prefix (F-AGE-ANCHOR's five sabotages).
- H11 · Instants stamped at a bar's OPEN (`plus_1r`, a stop `exit`) may only carry profiles built from lens bars that CLOSED at or before that open; each has a close-stamped post-event twin that must not be confused with it.
- H12 · Breadth across assets must be aligned by timestamp; an index join would read another asset's bar from a different day.

**Reproducing TC11 bar-for-bar**
- H13 · As-of-dependent columns move when the corridor extends: `window_end_i`, `window_end_close_ms`, `window_open_at_asof` (three v6 rows are open windows at TC11's pin: ETHUSDT entered 2026-09-18T08:00Z, SOLUSDT 2026-09-18T00:00Z, ZECUSDT 2026-08-17T04:00Z), `open_at_asof`, `continuation`, `entered_after_tc10_pin`, and all nine as-of stamps (`as_of_substrate` names the snapshot). The filed tables' CONTENT shas therefore cannot be reproduced under a new snapshot name; compare the 12 CTRL_COLS, the as-of-stable ROW_FIELDS and `TP._book_sha`.
- H14 · The 9/12 SOL campaign is `corridor_end` at TC11's pin; on the extension it is a continuation whose exit changes.
- H15 · The files are 6 dp; flags were computed at full float. Re-deriving `r_over_atr > 2.2`, the band or the era from the 6-dp tables can flip a boundary row.
- H16 · Funding: each home file already holds a print at the pin instant, read for the first time on the extended tape. A restated or back-filled funding or kline row on the prefix moves `net_r` (TC10's `ctrl_prefix` lesson, `tierc10_panel.py:2752-2758`). Stage D must prove the prefix bit-identical to `tc11_20260925` (TC11-D proved it against TC10: "prefixes bit-identical to TC10").
- H17 · `TP.ctrl_diff` can drop a NaN column (X's XFB-V1).
- H18 · Parquet BYTE identity depends on the pyarrow/pandas build; the content sha is the estate's law. X happened to reproduce TC11's journal bytes; a library upgrade would not.

**The frozen records and the operator's close acts**
- H19 · `close_acts.sh` of TC11 (`research_outputs/tierc11/close/close_acts.sh`): step 0 needs branch `v12-v1-census`, a CLEAN index, SOURCES equal to HEAD, F-LAR11 green on the sources as they stand; step 1 is `git push origin v12-v1-census` — it will publish every TC12 commit already on that branch. TC12 is being committed on that branch (`28e006b`).
- H20 · Any in-place "tc11-stamp" edit of TC11's PROGRESS, registry or SCORES files changes bytes that TC11's F-LAR11 cites and that X's sha-first reads certified; X's own ferry forecast (AM-X21) depends on TC11's close landing.
- H21 · MAIN's working tree carries an uncommitted change to a TC10 record: `M research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt` (3 insertions, 3 deletions). A TC12 `git add -A` or `git commit -a` would sweep it in.
- H22 · Three `close_acts.sh` are pending (TC10 6,823 B · TC11 9,675 B · X 23,780 B). TC12 must run none and must not write `exchange/status/LEDGER_APOLLO.md` (the hook's `ledger-write` class covers `exchange/status/LEDGER*`).
- H23 · Two ledgers, two chain laws (§1.12): "append-only on the three existing books" cannot mean writing either file.

**Determinism**
- H24 · `corridor_n`'s meta carries `wall_clock_at_run` and `cache_lag_hours`; `time.time()` is called inside it. Never stamp them.
- H25 · A default seed bound at def time is not re-rooted (`tierc11_env.py:90-92`): pass seed and n_boot explicitly at every call.
- H26 · `analytics_sha()` moves if `value_area.py` is added to `analytics._MODULES`; the package's I-F law then demands a version bump (`analytics/__init__.py:12-14,118`).

---------------------------------------------------------------------------------------------------
## 5 · REUSE PLAN

**Import unchanged, through a vendored shim (never edited):** the lineage `tierc2_baseline`, `tierc2..7_rules`, `tierc5`, `tierc6`, `tierc7`, `tierc7_lab_regime`, `tierc8`, `tierc9`, `tierc10_panel` (as `TP`), `tierc10_data` (as `D`), `engine.indicators`, `engine.s1`. Specifically: `TP.corridor_n`, `TP.run_cell_n` (control only), `TP.journal_frame`, `TP._book_sha`, `TP.ctrl_diff`, `TP.control_window`, `TP.make_put`, `TP.stamp_n`, `TP.check_keys`, `TP.check_det`, `TP.input_sha`, `T9.replay9`, `T9.card_candidates9`, `T9.armings9`, `T9._trailing_pool`, `T9._trailing_edges`, `T9.tide_streak_age`, `LR.tide_streak`, `LR._streak_band`, `LR.STREAK_LABELS`, `T6.run_cell`, `T7._account_chain`.

**Vendor by declared hunks (X's F-VENDOR law):** `scripts/tierc11_env.py` @ `1526093b…` → `tierc12_env.py` (R1).

**Mirror as a TC12 twin held to TC11's files (X's `tc11x_books.py` pattern):** `tierc11_books.py` — `corridor`, `v6_book`, `trg912_book`, `r912`, `campaign_rows` and its field seams (`entry_streak`, `trailing_edges`, `band_of`, `lag_band`, `known_window_end`, `exit_event`, `plus_1r_bar`, `latch_bar`), `ctrl_a`, `key_findings`. It cannot be imported: it does `import tierc11_env as E` and types TC11's pin and referees.
Mirror from `tierc11_stage_g.py`: `apply_gate`, `facts_of`, `refuse_hook`, `replay_g` (it needs `ride11`/`trade11`, so `tierc11_ride.py` must be vendored or its two functions mirrored — with both hooks off `ride11` is `_ride_leg9` line for line), `haircut`, `canonical_csv` / `book_sha256` (the regbook interface the scorer reads).
Mirror from `tierc11_stage_r.py`: the instant law (`instants_of`, `KINDS`, `NEST_KEY`) — the module itself is a runner that imports the range layer.
Mirror from `tierc11_closure_fixtures.py`: the whole F-CLOSURE-ALL machinery re-typed for `tierc12_*` (glob, typed runners with earned exemptions, FORBIDDEN + `value_area`, `LINEAGE_ENV_T`, fresh interpreters on the TC12 snapshot).
Reuse from X, read-only reference: `tc11x_books.ctrl_a_findings / ctrl_c_findings` (the NaN-aware compare and the CTRL-C-WHOLE clause), `tc11x_data.ENV_HUNKS` (the hunk-as-data form), `tc11x_pct.trailing_pct`, `forward/BOOK_SPECS.json` (the frozen-spec form and the `path_modules` pin).

**Records TC12 pins (sha-first, by absolute MAIN path unless noted):**
`research_outputs/tierc11/PROGRESS.json` (the source of every certified sha; read once) · `data/AS_OF_PIN.json` `4f609ccf…` · `data/fee_schedule.json` `6febe170…` · `data/STAGE_D_MANIFEST.json` `0d8da587…` · `books/v6_journal.parquet` `deb70b09…` · `books/v6_campaigns.parquet` `aab06934…` · `books/trg912_journal.parquet` `1ac9e317…` · `books/trg912_campaigns.parquet` `46ef63c5…` · `books/build_manifest.json` `04f129b7…` · `scores/BASE_IDENT.json` `29f795dc…` · `regbooks/P-AGE-1/scored.parquet` `6440a6e0…` · `regbooks/P-WIN-1/scored.parquet` `824c5e08…` · `stage_g/g_campaign_gates.parquet` `c5a5f486…` · `stage_g/g_grid_books.parquet` `b2c786e0…` · `stage_g/STAGE_G.md` `440509bc…` · `stage_r/NEST_v6.parquet` `de27be17…` · `stage_r/NEST_trg912.parquet` `7c5ffe23…` · `forward/FORWARD_LEDGER.jsonl` `e53328ad…` · `scripts/tierc11_env.py` `1526093b…`.
X (read-only, by absolute X path): `forward/BOOK_SPECS.json` `72a1f523…` · `forward/FORWARD_LEDGER.jsonl` `4a6da7e8…` · `books/build_manifest.json` `68d4a4a9…`.
All of the MAIN shas above were re-hashed on disk this session and equal the shas certified in TC11's PROGRESS.

**Newly written for Stage C:**
1. `tierc12_env.py` + its hunk table + F-VENDOR / F-SUBSTRATE / F-REROOT fixtures.
2. `tierc12_books.py`: v6 and 9/12 on the extended corridor AND on TC11's window; the three F-CTRL legs (R2), the two Σ laws (R3), the prefix/continuation table, the forward strip printed apart.
3. The combined-gated book as a filed book (it has never existed as a file), the far-stop arbitration twin with its event count, the 16-cell partition.
4. A TC12 closure fixture and a worktree attestation covering MAIN's TC10/TC11 records and the X worktree.
5. A `.gitignore` rule for `research_outputs/tierc12/**/*.parquet` and `_det_*/`, written before any shim arms.
