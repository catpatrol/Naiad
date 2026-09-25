# SCOUT E: breakout lane, Stage A stamps, 5m (map for the TC11 executor)

Scope: `scripts/tierc10_brk.py` (4199 lines), `scripts/tierc10_brk_fixtures.py` (5865), `scripts/tierc10_stamps.py` (1349), `scripts/tierc10_lanes.py` (spring / P-SPR-2), `scripts/tierc10_census.py` (the as-of layer, grid, toll and feasibility gate), `analytics/rangefinder_census.py` (the port), `engine/rangefinder.py` (the pins), and the artifacts under `research_outputs/tierc10/{brk,stamps,lanes,scores,census}`.
Read-only scout, 2026-09-24. Line numbers are for HEAD `b9ed953` on branch `v12-v1-census`. Every number below was read from a file or a parquet in this session.

---

## 0. Environment facts that constrain every TC11 script

- **Substrate guards.** `tierc10_census.py:72-107`, `tierc10_stamps.py:72-97` and `tierc10_panel.substrate()` (`tierc10_panel.py:161`) each HALT unless `NAIAD_CACHE_DIR` resolves to exactly `~/.cache/naiad/snapshots/tc10_20260921`. The variable must be exported **before python starts**, because `tierc2_baseline` binds `KLINES` at import.
  - **Gap:** a TC11 corridor with a newer as-of pin ("full water, latest closed 4h bar, one as-of pin") cannot use these modules unchanged. Their guards name the TC10 snapshot literally.
- **The as-of pin.** `research_outputs/tierc10/data/AS_OF_PIN.json`:
  - `as_of_last_closed_4h` = `2026-09-21T16:00:00Z`
  - `as_of_last_closed_4h_close_ms` = `1790006400000`
  - Readers: `tierc10_data.load_pin()` (`:520`) and `tierc10_brk.as_of_of_record()` (`:491`).
- **Lenses Stage D knows.** `tierc10_data.STEP_MS` (`:204`):
  - native `("5m","1h","4h","12h")`, derived `("1d","1w")` from native 4h.
  - 1w is Monday-anchored (`GRID_ANCHOR_MS`, `MONDAY_EPOCH_OFFSET_MS`).
  - **There is no `15m`.** `D.load_asof(sym, "15m")` raises a `KeyError` on `STEP_MS[iv]`.
  - The snapshot does hold `klines/*_15m.parquet` for 20 symbols (none for MNT, PUMP or SUI). These files run past the as-of: BTC 15m ends at open 16:15. They are not in the Stage D manifest, so no F-D-1 audit covers them. **This is a gap for R1's 15m lens.**
- **Lenses the census knows.** `tierc10_census.LENSES = ("5m","4h","1d")` (`:117`), with `LENS_MS` (`:118`) and `LENS_SOURCE` (`:119`, 1d derived from 4h).
  - `load_tape` HALTs on any other lens (`:586`).
  - `Tape.step` reads `C.LENS_MS[self.lens]` (`:544`).
  - So the census as-of layer, the grid, the toll and the feasibility tables exist **only for 5m, 4h and 1d**. 1h, 12h, 1w and 15m are absent everywhere (see §9).
- **Snapshot sizes (BTC).**

  | lens | bars |
  |---|---:|
  | 5m | 740,143 |
  | 15m | 246,715 |
  | 1h | 61,679 |
  | 12h | 5,140 |
  | 1w | 367 |

  Coverage runs from 2019-09-08 to the 2026-09-21 as-of.
- **The port.** `analytics/rangefinder_census.py`, sha256 `19c5507ff2d39b68aa119ff701aef58a2d219fa287c34cdf7302ebf2bbb7b37d`. This equals `census/build_manifest.json .port_sha256`, the "TC10 sha" that R1 pins. `engine/rangefinder.py` sha256 is `bbae464f…84d4`.

---

## 1. The range machine: pins and the events the BRK lane consumes

`engine/rangefinder.py` holds the pins. The census reads them through the port (`analytics/rangefinder_census.PINS` / `PINS_V2`).

`PINS` (`:136-160`):

| pin | value |
|---|---|
| LEG_MIN | 0.5 |
| REV_MIN | 1.75 |
| TOUCH_EPS | 0.60 |
| DEV_RETURN_BARS | 7 |
| BREAK_CONFIRM_N | 8 |
| BREAK_MARGIN | 1.5 |
| BOUNDARY_MODE | "body" |
| REDRAW_BASIS | wick (the census requires wick, `asof_view` `:772`) |

`PINS_V2` (`:573-590`):

| pin | value |
|---|---|
| SCALE_MULT | 3.0 |
| FLIP_HOLD_MARGIN | 1.0 |
| FLIP_HOLD_BARS | 6 |
| MEM_TTL_BARS | 400 |

`MEM_CAP_PER_SIDE` = 6 (`:571`).

The macro machine runs with LEG_MIN and REV_MIN multiplied by SCALE_MULT (`:780-781`). BREAK_MARGIN is **not** scaled.

**Event laws** (`engine/rangefinder.py:395-470`, identical in the port):
- **breach-open:** the first close beyond a CONFIRMED range's top or bottom.
- **harden** (deviation-confirm = spring/upthrust): a body close back inside within `bars_out <= DEV_RETURN_BARS (7)` of the breach-open. It increments `n_deviations` and redraws that side to the wick extreme of the episode. Events: `harden` + `redraw`.
- **breakout-die** (macro DEATH, used by the BRK lane): while a breach is pending, the range dies when **either**
  - `closes >= BREAK_CONFIRM_N (8)` consecutive closes beyond the boundary (the count starts at the breach-open close and resets on an inside close), **or**
  - `|close - boundary| >= BREAK_MARGIN (1.5) * ATR` on the far side.

  The event carries `side` in {top, bottom} and `by` in {n_closes, margin}. The state latch becomes BULL_EXP after a top death and BEAR_EXP after a bottom death.
- **memory line:** each boundary of a DEAD confirmed range. The leash is `analytics/rangefinder_census.flips_and_leash` (`:702-877`):
  - TTL is 400 bars from death; at most 6 live lines per side (the oldest expires).
  - A **flip** is the **first opposite-side touch** (`l<=px<=h` with the prior close on the far side). It gets ONE evaluation: held iff for `j in i..i+6` no close goes through `px -/+ 1.0*ATR[j]`.
  - A failed evaluation CONSUMES the candidacy.
  - A dead top that holds flips to `support` (+1); a dead bottom flips to `resistance` (-1).
  - A flip is stamped at touch bar `i` and KNOWN at `i+6` (`leash_known_at`, `:890`).
  - The docstring at `engine/rangefinder.py:550-560` files the rival reading "first-retest-THAT-HOLDS" as the operator's arbitration exhibit, **not enacted**.

**Adapter into BRK.** `tierc10_brk.macro_signals(sym, lens, scale_mult=FROZEN_SCALE)` (`:2332`) is the only range doorway, with a function-local import of `tierc10_census`. It returns:

```
{'dies': [(die_i, rid, side)], 'flips': [{'i','polarity','rid'}], 'scale_mult', 'lens', 'sym', 'n_bars'}
```

The indices are in the **`C.load_tape(sym, lens)` index space**. It works only for 5m, 4h and 1d.

---

## 2. Q1. The breakout-retest lane in code

**Lane constants** (`tierc10_brk.py`):
- `LANE_S1="brk-s1"`, `LANE_I1="brk-i1"` (`:154-155`)
- `LANE_LENS={s1:"5m", i1:"1d"}`
- `ANCHOR_BAND="band"`, `ANCHOR_MEMORY="memory-line"` (`:157-158`)
- `LANE_ANCHOR={s1: band, i1: memory}`, with the other anchor printed as Tier-E (`:163-164`)
- `LANE_ERA={s1:"holdout", i1:"full"}` (`:196`)
- `RIBBON_FAST, RIBBON_SLOW = 12, 25`; `LIFECYCLE_K=3` (`:200-201`)
- `R1_BANDS=("ribbon-89/127","ribbon-127/200","tap-89","tap-127","tap-200")` (`:206`)
- `FLIP_HOLD_MARGIN=1.0`, `FLIP_HOLD_BARS=6`, `FROZEN_SCALE=3.0`, read from the AST of `engine/rangefinder.py` via `D.pin_literal` (`:145-151`). `MEM_TTL_BARS=400` (`:149`).

**Bands: which moving averages, on which lens.** `r1_band(name)` (`:1429`) builds EMAs of **CLOSE** on the **lane's own lens bars**:
- The EMA is `engine.indicators.ema`: recursive, alpha = 2/(p+1), seeded at `c[0]`.
- A **tap** is a single EMA line (lo == hi), NaN for `idx < p`.
- A **ribbon** is `[min, max](EMA p1, EMA p2)`, NaN for `idx < max(p1, p2)`.
- There are no SMAs anywhere.
- The census twin is `tierc10_census.band_of(name)` (`:969`), which is proven bit-equal.
- Spelling translators: `band_key()` (`:242`) and `census_band()` (`:263`). For example, `ribbon-127/200` and `ribbon127_200` are the same band.

**The candidacy window.** `candidacy_window(dies, n, ttl_bars=400)` (`:1411`):

```
end = min(die_i + ttl, next_die_i - 1, n - 1)
```

The window is `(die_i, end]`.

**How a HOLD is decided (band anchor).** `band_hold_candidates(h, l, c, atr, dies, lo, hi, margin_atr, hold_bars, ttl_bars=400, anchor_label="band") -> (cands, tally)` (`:1475-1538`) is a transcription of `tierc10_census.retest_holds` (`:983`). There is ONE evaluation per DIE:
1. The touch bar `j` is the FIRST bar in the window where `l[j] <= hi[j] and h[j] >= lo[j]` **and** the prior close was beyond the band on the die side. For a top-DIE that means `c[j-1] > hi[j-1]`; for a bottom-DIE, `c[j-1] < lo[j-1]`.
2. `hold` iff for `k in j..j+hold_bars` no close is through the far edge:
   - top-DIE: `c[k] < lo[k] - margin_atr*ATR[k]`
   - bottom-DIE: mirrored
   - a NaN band inside the window counts as a failure.
3. If `j + hold_bars >= n`, the verdict is `truncated` (never a hold).
4. `known_i = j + hold_bars`. The entry is at the close of `known_i`.
5. Direction: +1 for a top DIE, -1 for a bottom DIE.
6. `extreme` = `min(l[j..known])` for a long, `max(h[j..known])` for a short.

`Candidate` dataclass (`:1390`): `direction, anchor, die_i, touch_i, known_i, extreme, rid, verdict, note`.

`tally` keys: `n_dies, n_evaluated, n_hold, n_failed, n_truncated, rows[{rid, side, die_i, touch_i, known_at, verdict}]`.

**Memory anchor.** `memory_flip_candidates(h, l, dies, flips, n, hold_bars=6, ttl_bars=400, same_range_only=False)` (`:1541`) takes the first leash `flip` whose `i` lies in the DIE's candidacy window.
- `known = i + 6`.
- Direction comes from the flip's polarity. A mismatch with the DIE side is counted in `n_polarity_vs_die_mismatch`.
- `extreme` is taken over `[i, known]`.
- FINDINGS mismatch 1: the census window is applied on top of the leash's own TTL/cap.

**Tuned pins** (read at run time; never typed): `tuned_pins(lens)` (`:1653`) reads `TUNING_RESULT_FOR` (`:283`).

| lens | file | band | margin_atr | hold_bars | ttl | n | floor | objective | median_term | toll_atr |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 5m | `census/TUNING_RESULT.json` | `ribbon127_200` | 1.0 | 3 | 400 | 15568 | 200 | **−0.36348607** | 0.04712987 | 0.41061594 |
| 1d | `census/TUNING_RESULT_1d.json` | `ribbon89_127` | 0.25 | 6 | 400 | 44 | 30 | +0.73652813 | — | — |

- 5m: all 45 cells are negative. The chosen cell is the least negative.
- The grid was 5 bands × margin {0.25, 0.5, 1.0} × hold {3, 6, 12}.
- **No 4h, 1h or 12h tuning exists.** The census's own 4h and 1d `retest-hold-*` rows used the 5m pins (margin 1.0, hold 3, ttl 400) via `resolve_retest_pins()` (`tierc10_census.py:272`). The provisional fallback is the flip pins, 1.0 / 6 / 400 (`RETEST_DEFAULT`, `:230`).

**Stop.** `brk_stop(direction, retest_extreme, touch_i, entry_px, atr_sig, rail_atr=1.0)` (`:1366`) wraps `tierc5_rules.spring_stop` (`tierc5_rules.py:481`). For a long:

```
stop = min(extreme - STOP_BUF_ATR*ATR, entry - rail_atr*ATR)
```

(mirrored for a short) with `STOP_BUF_ATR = 0.5` (`tierc2_rules` REGISTER) and `MIN_STOP_ATR = 1.0` (`tierc3_rules:148`).
- **"Railed 1.0 ATR" means R ≥ 1.0 ATR of the lens.** It is a floor, taking the farther of the two stops.
- ATR = `ind.atr` = Wilder RMA(14) of the true range, seeded at TR[0].
- It returns a `Stop` (`tierc3_rules.py:223`) with fields `stop_px, anchor, anchor_bar, pivot_stop_px, pivot_dist, rail_dist, r_dist, rail_binding, n_eligible`.

**Tide ("tide aligned").**
- `tide_state(e_fast, e_slow, c)` (`:1749`): +1 iff `e89 > e316 and c > e316`; -1 on the mirror; otherwise 0 (stand down).
- `tide_4h_for_exec(exec_open_ms, f4, roles=V6_ROLES) -> (state, idx)` (`:1761`) uses `engine.htf.map_htf_to_exec`, under which an HTF bar is visible iff `htf_close <= exec bar OPEN`.
- `s1_permission(entry_i, d, tide_exec)` (`:1897`) returns `{'ok': tide == d, ...}`.
- **Hazard for 4h P-BRK-4H:** feeding a 4h exec frame to `tide_4h_for_exec` reads the **previous** 4h bar (bar `i` closes after bar `i`'s open). On a same-lens frame, use `tide_state(roles_l(lf, V6)['tide_f'], ['tide_s'], lf.c)[entry_i]` instead (B7: permissions are read at the entry bar, from closed bars).

**Management ("v6 management lens-scaled").** `ride_leg_l(lf, card, roles, d, ti, entry_px, stop0, r_dist, hi_i, ribbon=None, active=COMPONENTS)` (`:1093`) is `tierc9._ride_leg9` on the lens.
- Within-bar order: STOP → BELL → HARVEST → TRAIL, adverse first.
- The stop fills AT the stop.
- Bells: counter 12/89 (window) or counter 89/316 (tide). When `ribbon=(12,25)` is passed, the counter 12/25 bell is also tested, last.
- Harvest: 50% at the armed 89/316 band edge.
- Trail: the (2,2) fractal ratchet, armed after +1R (`trail_arm_after_r=1.0`).
- Cold EMAs are INACTIVE, decided at the entry bar (B1).
- Returns: `own_r, entry_i, entry_px, stop0, exit_i, exit_px, exit_reason, advances, harvest, blocked, mfe, mae, final_stop, n_opportunities, mae_to_1r, reached_1r, warm, inactive, n_inactive`.
- **There is no take-profit or target branch** (gap for Stage S and P-TP-RNG).

**Accounting.** `account_l(lf, card, d, r_dist, leg)` (`:1270`) computes:

```
net_r = gross_r - fee_r - funding_r_eff
```

- Fee: `FEE_BPS_SIDE=5.0` × (entry + exit).
- Funding: the interval sum `entry_ms < funding_hour_ms <= exit_ms` (`funding_interval`, `:1223`), capped at the card's 1R ceiling.
- **The toll is not deducted** (`TOLL_ACCOUNTING`, `:453`).

**Core replay.** `brk_campaigns(lf, legs, card, roles, lane, lo_i, hi_i, ribbon=None, active=COMPONENTS, era=None, account=True) -> [RC.Trade]` (`:2045`).
- One position per (asset, lane). A leg whose `entry_i <= open_until` is skipped.
- `require_era` runs only if `era` is not None.
- Trades carry the extra attributes `lens, touch_i, die_i, rid, anchor_kind, inactive_components, entry_close_ms, exit_close_ms, funding_census, mae_r`.

**Candidates → legs.** `legs_from_candidates(lf, cands, lane, permit=None, rail_atr=1.0) -> (legs, refused{permission, no_atr, no_stop, out_of_tape})` (`:2134`). `Leg` dataclass: `:2025`.

**Runners.**
- `run_lane_s1(panel, reg_id, text, arm, signals, tuned=None, …)` (`:2201`)
- `run_lane_i1(…)` (`:2271`)
- Both are **hard-wired** to lens 5m/1d, lane strings `brk-s1`/`brk-i1`, and `TP.require_arm` + `require_lane_era`. `LANE_ERA` knows only those two lanes, so `require_lane_era` HALTs on anything else (`:1973`).
- **A TC11 4h lane cannot reuse the runners.** It must compose the lower-level pieces (snippet in §10) and file its own arm via `TP.arm_spec` / `TP.require_arm` / `TP.external_book`.

**F-C10-HOLD, "hand-verified" as a fixture** (`tierc10_brk_fixtures.py`):
- `hold_harness(lens, tape, rows, margin_atr, hold_bars)` (`:718`) re-walks every DIE window with a plain Python loop. It uses the law as written (`end = min(die+ttl, next_die-1, n-1)`), not `B.candidacy_window`. It compares verdict **and** touch bar with `B.band_hold_candidates`.
- Synthetic half, `f_c10_hold_harness` (`:836`): planted tapes (`hold_tape`, `:308`). Three holds per lens {5m, 4h, 1d} plus one planted failure (`fail_at=23`) that must come back `failed`.
- Real half: `REAL_HOLD_CASES = (BTC 5m, ETH 4h, BTC 1d)` (`:795`), on the tuning-era head of each tape only. It requires 3 holds that agree, at least one real `failed` retest, and agreement on every DIE.
- Sabotage: `band_hold_candidates` is monkeypatched to relabel every retest as a HOLD, and the fixture must go RED.
- Filed half, `f_c10_hold_filed` (`:1777`):
  - `FILED_HOLD_RULE` (`:962`) blind-names the first hold per asset inside each filed arm's era window.
  - Hand EMA (`_hand_ema`, `:1047`) and ATR (`_hand_atr`, `:1057`) are plain loops.
  - Hand pins are typed from the filed text (`HAND_PINS`, `:980`; `HAND_RAIL`; `HAND_STOP_BUF = 0.5`).
  - `_same_bars` (`:1232`) proves `C.load_tape` bars equal `B.frame_l` bars before any index is shared.
- Book half, `f_c10_hold_book` (`:2073`): the first three campaigns of each filed book are walked by hand.
- Transcript: `research_outputs/tierc10/brk/FIXTURES_BRK.txt`, 20/20 PASS.
- **This is the template for F-SCALP, F-RELAY and F-ADD.**

---

## 3. Q2. The registrations: exact definitions and results

Texts: `research_outputs/tierc10/REGISTRATION_TEXTS.json` (keys `P-GEN-1, P-SPR-2, P-BE-1, P-TRG-2, P-BRK-I1, P-BRK-S1`); a readable copy is in `REGISTRATION_TEXTS.md`.
Scores: `research_outputs/tierc10/scores/SCORE_*.txt`, `*.rows.json`, `FAMILY.json`.
Verdict table: `research_outputs/tierc10/BUILD_DRAFT.md:62-69`.

**P-BRK-S1 [30%] "SCALPER".** Text at `REGISTRATION_TEXTS.md:1408+`.
- Panel CLASSIC5; **era holdout** (entry after `2024-06-30T23:59:59Z` = `1719791999000`).
- 5m macro DIE at frozen scale 3.0, then the first HOLD retest of the tuned band (ribbon127_200, margin 1.0, hold 3, ttl 400).
- Entry at the close of the hold-confirm bar.
- Stop beyond the retest extreme (0.5 ATR buffer), railed to 1.0 ATR(5m).
- 4h tide aligned (e89/e316) as of the last closed 4h bar at the 5m bar's OPEN.
- v6 management plus the 12/25 bell. No target.
- Cost: fee 5 bps/side + funding. The toll is a PRINT only.
- **Result:** n 1836, **−0.211069 R** [−0.298366, −0.144105], LOAO 0/5 above (5/5 below), p 1.0 → **NOT SUPPORTED, CI wholly below zero**.
- Tier-E: 17-asset view n 6016 at −0.170156 [−0.205, −0.137]; memory-line anchor n 1300 at −0.198889 [−0.335, −0.073].
- Haircut twin: −0.372757.
- Per-asset 5m toll (ATR): BTC 0.46555286 · ETH 0.35253641 · SOL 0.24410209 · NEAR 0.20944241 · ZEC 0.23793258. Median `toll_pct_of_1r` is 17.76%.
- The builder's recommendation (`close/BUILDERS_REPORT_HEPHAESTUS_2026-09-23_TC10-STAGE-B-CLOSE.md:238`) was **"Drop the 5m scalper."**

**P-BRK-I1 [35%] "INVESTOR".**
- 1d macro DIE, then the first memory-line flip-hold (1.0 ATR / 6 bars). Entry at the close of `flip.i + 6`.
- Stop beyond the retest extreme, railed 1.0 ATR(1d).
- Permission: the weekly 12>25 posture on the last closed Monday week (`weekly_posture`, `:1857`) **and** the daily 12/25 lifecycle DIRECTION (`ribbon_lifecycle`, `:1781`: `s = (e12 - e25)/ATR14`; EXPANDING iff the sign is unchanged over `s[t-3..t]` and `|s_t| > |s_{t-3}|`). Combined in `i1_permission` (`:1874`).
- Full era, CLASSIC5.
- **Result:** n 7, +0.718270 [−0.602912, +1.452261], LOAO 1/5, p 0.2697 → NOT SUPPORTED. One ETH trade (+6.13 R) exceeds the book's net.

**P-SPR-2 [45%] (the spring/upthrust code).**
- Signal: macro **harden** at frozen scale 3.0 / DEV_RETURN_BARS 7. A bottom harden is a LONG spring; a top harden is a SHORT upthrust.
- Code path: `tierc10_lanes.harden_episodes(events)` (`:1155`), then `springs_from_episodes(h, l, c, open_ms, episodes, top_asof, bot_asof, …)` (`:1195`), wrapped by `spring_signals_from_census(sym, lens="4h", scale_mult=3.0)` (`:1231`, lazy census import), then `signals_on_frame(f, springs)` (`:1257`, re-indexes by ms and HALTs on disagreement).
- `SpringSignal` (`:714`) extends `RC.Spring` with `known_at, rid, side, source`.
- `sweep_i` is the breach-open. `sweep_extreme` is the raw extreme over `[breach, harden]`. `swept_level` is the **as-of boundary at the breach bar**. Entry is the **harden bar's close**.
- Stop: `RC.spring_stop(sp, entry, atr, card.entry_rail_atr=1.0)`.
- **No tide gate.** The old P-SPR-1 (`tierc5_rules.spring_signals`, `:401`: a 96-bar extreme sweep plus a reclaim within 3 bars, tide required) is superseded.
- v6 management through `tierc10_lanes._ride_leg10` (`:482`) inside `replay10` (`:838`), with `Card(lane="spring")` = `CARD_SPR2` (`:218`). Spec: `LANE_SPEC["P-SPR-2"]` (`:1840`).
- 4h, CLASSIC5, full era, vs zero.
- **Result:** n 261, −0.005930 [−0.174617, +0.165338], LOAO 0/5 → NOT SUPPORTED.
- Tier-E by era: tuning n 165 at −0.149; holdout n 96 at +0.240 [−0.050, +0.474]. The holdout is **not** out of sample for the RangeFinder pins, which were calibrated on BTC in 2025-26.

**P-GEN-1 [45%].**
- Card v6, all pins frozen, on UNSEEN12, full era, vs zero.
- **Result:** n 286, +0.099777 [−0.154991, +0.315921], LOAO 0/12 → NOT SUPPORTED.
- BNB alone contributes +33.47 R, which is 117% of the net. The never-touched three (PUMP, MNT, SUI) give n 47 at −0.232839.

**Existing swing-failure (SFP) code for R4(b) and P-ADD-SFP.** The harden episode is the only deviation-confirm event.
- As-of arrays come from `C.asof_view`: `dev_top`/`dev_bot` count hardens so far; `top`/`bot` move at the harden bar.
- The event table is per-cell `research_outputs/tierc10/census/cells/{SYM}__{lens}/events.parquet`:
  - `cls ∈ {breach, harden, DIE, flip-hold, memory-touch-v1, memory-touch-2s, retest-hold-{ribbon89_127, ribbon127_200, tap89, tap127, tap200}}`
  - columns `i, known_at, rid, side, sgn, known_close_ms, toll_atr_evt, term/mfe/mae_{H20,H100}, cens_*, era, state_at, in_range_at, pct_at, dist_atr_at, flip_pol_at, scale_kind, scale_mult`
  - lenses 5m, 4h and 1d only; both scale kinds.

---

## 4. Q3. Stage A stamps (the base for R3 and R5)

**What they are.** They are per-**instant** range-state stamps, not per-campaign. Every funnel instant of a ridden book is stamped with the as-of RangeFinder view at the close of the instant's own bar. The stamps are captured and never consulted (`tierc10_stamps.py:1-60`).

`INSTANT_KINDS` (`:131`): `arming, window_open, window_close, reject, trigger, entry, anchor_bar, plus_1r, harvest, advance, pivot_bar, bell, exit`.

**Schema.** `STAMP_DEFS` (`:166-233`), filed as `stamps/stamp_defs.parquet`. `STAMP_FIELDS`:

| field | meaning |
|---|---|
| `macro_state` | NONE / NEUTRAL / BULL_EXP / BEAR_EXP |
| `in_range` | a confirmed range is alive |
| `range_id` | the live range's `rid` |
| `pct_of_range` | `100*(c-bot)/(top-bot)`, unclamped, on the as-of box |
| `dist_boundary_atr` | **unsigned** `min(\|top-c\|, \|c-bot\|)/ATR14` |
| `nearest_side` | which boundary; a tie reads top |
| `boundary_age` | bars since the nearest side's as-of value last changed |
| `range_age` | bars since the confirm bar |
| `dev_top`, `dev_bot` | hardens so far per side |
| `inception_top`, `inception_bot` | defining wick beyond the body boundary |
| `last_flip` | support / resistance (known = touch + 6) |
| `last_flip_age` | bars since that flip became known |
| `state_latch` | raw latch name, for audit |
| `bar_open_ms`, `bar_close_ms`, `bar_lag`, `bar_lag_ms` | the as-of warranty |

- `GEOMETRY_FIELDS` (`:240`) are nulled when no range is alive. `LEASH_FIELDS` (`last_flip`, `last_flip_age`) survive a dead range.
- Joined columns are prefixed `rf{lens}_` (`prefix()`, `:774`).

**Where the arrays come from.** `tierc10_census.asof_view(tape, macro, leash) -> dict` (`:745-891`). Element t is what a reader at the close of bar t knows. `ASOF_ARRAYS` (`:937`):

```
rid, in_range, state(0/±1), top, bot, pct, dist_atr, near_side(±1/0),
top_age, bot_age, bnd_age, range_age, dev_top, dev_bot, inc_top, inc_bot,
covered, flip_pol(+1 support/-1 resistance/0), flip_age, flip_rid
```

It also carries `_by_rid` and `_leash_frame`.

Related functions:
- `C.asof_index(tape, instant_ms)` (`:894`) returns the last bar whose CLOSE is ≤ the instant (a same-instant close IS read).
- `C.stamps_at(tape, view, idx)` (`:906`) returns the `rf_*` dict.
- `STATE_NAME = {0: "NEUTRAL", 1: "BULL_EXP", -1: "BEAR_EXP"}`.

**Public door.** `tierc10_stamps.stamp_book(book_or_journal, panel, lens="4h", arms=None, lo_ms=None, hi_ms=None) -> {instants, trades, coverage, nulls, stamp_tables, defs, leans, meta}` (`:881`).
- It always stamps on the 4h lens of record, plus the lane's lens if different.
- It is a pure m:1 left join on `[asset, instant_ms, instant_kind]` (`join_stamps`, `:778`).
- `asof_layer(asset, lens)` (`:668`) memoises `(C.load_tape, C.asof_view)` at `FROZEN_SCALE` only.
- The lens set is `C.LENS_MS`, i.e. **5m, 4h and 1d only. There is no 12h, 1h or 1w.**

**R5's "five-row table".** `entry_state_crosstab(out)` (`:1093`), filed as `stamps/control_entry_by_state.parquet`: v6 CLASSIC5 entries by 4h macro state.

| macro_state | n | expectancy_r | notes |
|---|---:|---:|---|
| BEAR_EXP | 40 | −0.016 | |
| BULL_EXP | 66 | +0.220 | |
| NEUTRAL (in range) | 94 | +0.297 | median pct 40.5 |
| NONE | 0 | — | |
| __ALL__ | 200 | +0.209 | |

Other Stage A artifacts:
- `stamps/control_v6_stamped.parquet` (5745 × 45: funnel columns + `rf4h_*` + as-of warranty columns)
- `control_v6_units.parquet` (1132 × 30)
- `funnel_tally.parquet`, `stamp_coverage.parquet`, `stamp_nulls.parquet`, `stamp_defs.parquet`, `leans.parquet`
- `build_manifest.json`, `FIXTURES_STAMPS.txt`

**For R3 and R5, what exists and what is missing:**
- Exists: the 4h lens stamp (`pct_of_range` for the decile, `macro_state`, `in_range`, `boundary_age`, `dev_*`, `last_flip`).
- Missing:
  - any 12h, 1h or 1w stamp (census lens gap);
  - a signed distance;
  - boundary COINCIDENCE;
  - a lens-stacked vector.
- Existing as-of proof to reuse:
  - F-RNG-ASOF (`tierc10_census_fixtures.py:222-300`): prefix-stability with 4 leaky readers, `LAWS = ("honest", "leaked-redraw", "flip-at-stamp", "backdated-edge", "naive-known-at")`. **`leaked-redraw` is exactly the sabotage F-NEST-ASOF needs.**
  - F-STAMP-ASOF (`tierc10_stamps_fixtures.py:238 _asof_findings`).

---

## 5. Q4. The 5m height-vs-toll "FAIL 0/17"

- Computed by `tierc10_census.build_r34` (`:3116`), using `height_rows` (`:2636`), `height_grid` (`:2659`), `edge_arrays` (`:2710`), `edge_gate` (`:2863`) and `verdict_rows` (`:2899`). The law is `HEIGHT_GATE_LAW` (`:2186`), sha `6b53434f…`.
- **Height leg.** Per CONFIRMED range at its confirm bar:
  - `height_atr = (top0-bottom0)/atr[confirm]`
  - `toll_atr = (bps/1e4)*close[confirm]/atr[confirm]`
  - `ratio = height/toll` (ATR-free)
  - PASS iff `n_ranges >= 30` **and** `median(ratio) >= 3.0` (= 2/κ, κ = 2/3) **and** `share(ratio<1) <= 0.10`.
- **Edge-fade leg.** Every in-range bar close inside the confirmed range is faded toward the far boundary (`sgn = +1` if `pct<0.5`).
  - Near edge = the outer 20% (`EDGE_NEAR_FRAC = 0.2`, deciles 0-1 and 8-9).
  - `term_H20 = sgn*(c[k+20]-c[k])/atr[k]`, censored.
  - PASS iff `median(term) - toll_atr > 0` within the row's era, with `edge_n_ranges >= 30` and `edge_n >= 30`.
  - Note: `walk['ir_pct']` here is a **fraction 0..1**; `asof_view['pct']` is 0..100.
- **Verdict:** `verdict_pass = gate_height_pass AND gate_edge_fade_pass`.
- **Tables:**
  - `census/height_toll.parquet` (360 × 50, key asset, lens, scale_kind, era)
  - `census/height_toll_verdict.parquet` (360 × 52, same key; columns include `gate_height_pass, edge_net_h20, gate_edge_fade_pass, provisional, verdict_pass, verdict_law, reason, gate_law_sha`)
- **What "0/17" is.** At 5m, **every single asset PASSES the height leg** (ratio_median 13-38) and **FAILS the edge-fade leg**. So `verdict_pass` is 0 of 17 on era ALL and 0 of 17 on holdout, for both scale kinds. The tuning era is 2/17 frozen (1000PEPE, ENA) and 1/17 calibrated.
- Pooled CLASSIC5, frozen3.0:

  | lens | era | n_ranges | ratio_median | toll_atr_median | edge_net_H20 | verdict |
  |---|---|---:|---:|---:|---:|---|
  | 5m | ALL | 13025 | 23.26 | 0.2927 | −0.374 | FAIL |
  | 5m | holdout | 4584 | 20.67 | 0.3277 | **−0.588** | FAIL |
  | 4h | ALL | 298 | 169.5 | 0.039 | −0.226 | FAIL |
  | 4h | holdout | 102 | — | — | +0.006 | **PASS** |
  | 1d | ALL | 53 | — | — | — | PASS |
  | 1d | holdout | 18 | — | — | — | FAIL (provisional) |

- **Where the toll comes from (F-C10-TOLL).**
  - `bps = toll_bps_for(stem)` (`tierc10_census.py:510`) reads `research_outputs/tierc10/data/fee_schedule.json[assets][stem].round_trip_bps_used`. That is **10.0 bps for all 17 assets**: kind "ASSUMPTION — the estate's flat FEE_BPS_SIDE object, NOT a venue schedule", `taker_bps_side_used: 5.0`.
  - Per event: `toll_atr_evt = (bps/1e4)*c[k]/atr[k]`, from `outcome_ledger` (`:1352`).
  - Grid rows: `toll_atr_all` (median over all anchors) or `toll_atr` (per horizon; the pooled row takes the BINDING max).
  - Grid file: `census/outcome_grid.parquet` (7920 × 51, `GRID_KEY = [asset, lens, cls, scale_kind, era, horizon]`).
  - Reader: `C.get_toll(asset, lens, cls, scale_kind="frozen3.0", horizon=None, grid_path=None, era="ALL")` (`:1895`). It HALTs on a missing, duplicated or NaN row.
  - BRK wrappers: `B.grid_toll_atr` (`:2371`), `B.toll_class(anchor, band)` (`:1329`; for example `retest-hold-ribbon127_200` or `flip-hold`), `B.stamp_toll(trades, lens, anchor, band)` (`:2385`), and `B.toll_pct_of_1r(toll_atr, r_dist, atr_at_entry) = toll_atr/(r_dist/atr)*100` (`:1351`).
  - Note: `stamp_toll` reads **era ALL** even for the holdout lane.
  - The F-C10-TOLL fixture (`tierc10_brk_fixtures.py:3139-3330`):
    - runs an AST scan for numeric literals in toll positions (`tierc10_census_fixtures.toll_literals`);
    - reads a real row;
    - checks that a misspelled class HALTs.
  - Haircut twin: `fee_schedule.json` `haircut_twin_slippage_bps_side` is 2 (BTC, ETH), 5 (tier B) or 10 (tier C). Formula: `tierc10_data.haircut_twin_net_r`.

---

## 6. Q5. The stop and tide mechanics, restated for reuse

- **Stop beyond the retest extreme, railed 1.0 ATR:** `B.brk_stop` → `tierc5_rules.spring_stop` (§2). The extreme is taken over `[touch_i, known_i]` on the raw tape.
- **Structural-pivot stop** (for a "5m structural pivot"): `tierc3_rules.struct_stop_4h(pv, cur_i, entry_px, direction, atr_sig, lookback=200, min_stop_atr=1.0, forbidden=None)` (`:237`).
  - `pv` comes from `RC.build_pivots_4h(high, low)`: confirmed (5,5) pivots, `low_conf/low_val/low_bar/high_*`.
  - It picks the nearest confirmed pivot beyond entry within 200 bars of **its own lens**, offsets it by `0.5*ATR`, and rails it to ≥ 1.0 ATR.
  - The code is array-generic, so it runs on 5m arrays. Returns None when there is no anchor.
- **The (2,2) fractal** (the trail clock): `B.fractals_l(lf, 2, 2)` → `RC.build_fractals`.
- **Tide aligned:** `tide_state` on e89/e316 of the lens's closes. The cross-lens version is `tide_4h_for_exec` (exec OPEN law).
- **Two visibility laws coexist.** Pick one per stage and say which:
  - `engine.htf.map_htf_to_exec` / `B.visible_htf_idx` (`:1727`): an HTF bar is visible iff `htf_close <= exec OPEN`. Used by S1's tide and I1's weekly posture.
  - `C.asof_index`: `htf_close <= instant CLOSE` (a same-instant close IS read). Used by the Stage A stamps.
  - W1's "only 1h bars CLOSED before the 4h bar closes" and the scalper's 1h-view-at-5m-close sit exactly on this difference.

---

## 7. Q6. Existing scalper code and results

`grep -ril scalp scripts analytics engine` finds only `tierc10_brk.py`, `tierc10_brk_fixtures.py` and `tierc10_close_ledger_append_root.py`. **The only "scalper" in code is P-BRK-S1** (5m breakout-retest; §3: −0.211 R, n 1836, CI below zero). **There is no 5m 12/89-cross scalper and no range-target scalper anywhere.**

The pre-tierc heir is **TC-5** (`LEDGER.md:403-445`; `scripts/tc5_runner.py`, `configs/tc5_*.json`, `tc5_results.json`, `TC5_RESULTS.md`):
- engine v1.0.10 cells, gov 1h / exec 5m / align 1h, CLASSIC5, exploration-classic window to 2024-06-30.
- mfe/toll ratio 1.79 (versus 0.65 at 1m).
- **net 1× −1180.32**, 2328 campaigns, 3/5 cells halted.
- "5m floor permanent".
- It is a different architecture (engine cells, not the tierc ride).

The ingredients the TC11 scalper needs, and whether they exist:
- **5m 12/89 cross:** `B.roles_l(B.frame_l(sym, "5m"), T9.V6_ROLES)` gives `w_up`/`w_dn`. `win_f=12, win_s=89` (`tierc9.py:101-102`); `ind.crossover(a, b) = (a>b) & (a_prev<=b_prev)`. The EMA has no NaN warm-up; floor at 316 bars (`T9.V6_ROLES.floor_bars`).
- **1h confirmed range / third / far boundary / 1h ATR / boundary age:** `C.asof_view` on a **1h tape, which the census cannot load today** (see the snippet workaround in §10).
- **5m ATR tercile:** trivial from `lf.atr`. No existing code.
- **Target / take-profit exit:** **none**; a new ride is needed.
- **Maker fee:** **none on file.** The only precedent is `scripts/v3_recompute.py:954-990` (R10: "maker entries 2 bps/side, taker stops 5 bps/side", an OPTIMISTIC ceiling that assumes every maker order fills).

---

## 8. Artifacts index

| path | what |
|---|---|
| `research_outputs/tierc10/brk/BRK_MECHANICS.json` | mechanics card |
| `research_outputs/tierc10/brk/BRK_READY.{json,txt}` | sealed rows per filed arm |
| `research_outputs/tierc10/brk/BRK_READY_BOOKS.json` (2.6 MB) | entry geometry of books |
| `research_outputs/tierc10/brk/FIXTURES_BRK.txt` | 20/20 PASS |
| `research_outputs/tierc10/brk/build_manifest.json` | manifest |
| `research_outputs/tierc10/scores/P-BRK-S1.rows.json` (sha `994bcaa6…`) | scored rows |
| `research_outputs/tierc10/scores/P-BRK-I1.rows.json`, `P-SPR-2.rows.json`, `P-GEN-1.rows.json` | scored rows |
| `research_outputs/tierc10/scores/SCORE_*.txt`, `FAMILY.json`, `DRYRUN.json` | score transcripts |
| `research_outputs/tierc10/lanes/` | P-BE-1 only (`BE_LATCH_CENSUS.json`, `FIXTURES_LANES.txt`, manifest) |
| `research_outputs/tierc10/stamps/*` | §4 |
| `research_outputs/tierc10/census/TUNING_RESULT{,_1d}.json`, `TUNING_GRID{,_1d}.{md,parquet}` | R1 tuning |
| `research_outputs/tierc10/census/outcome_grid.parquet` | the toll grid |
| `research_outputs/tierc10/census/height_toll{,_verdict}.parquet`, `edge_fade.parquet` | feasibility |
| `research_outputs/tierc10/census/scale_grid.parquet` | calibrated SCALE picks |
| `research_outputs/tierc10/census/hold_tally.parquet` | 612 × 30 |
| `research_outputs/tierc10/census/cells/{SYM}__{5m,4h,1d}/events.parquet` | event tapes |

Calibrated SCALE picks for CLASSIC5 (`scale_grid.parquet`, `chosen`):
- 5m: 1.75 for all five assets.
- 4h: 2.00 for all five assets.
- 1d: 2.00-2.50.
- The frozen 3.0 gives about **0.36-0.55 confirmed ranges per 100 bars**, not 0.75.

---

## 9. GAPS: what the TC11 contract asks for that the code cannot do today

1. **R1 lens set {5m, 15m, 1h, 4h, 12h, 1d, 1w}.** Census `LENSES`, `LENS_MS`, `LENS_SOURCE`, `TS_FMT` and `load_tape` cover only 5m, 4h and 1d.
   - 1h and 12h are Stage D native, so `D.load_asof` works.
   - 1w is Stage D derived (Monday).
   - 15m is not a Stage D lens at all: `STEP_MS` has no key, and the snapshot files are un-audited and run past the as-of.
   - A tierc11 tape loader is needed (for example a `C.Tape` subclass overriding `step`; `asof_view` itself reads only `n, h, l, c, atr`).
   - `B.macro_signals` and the `stamps.asof_layer` go through `C.load_tape` and HALT on 1h, 12h or 1w.
2. **R2 feasibility** is filed only for 5m, 4h and 1d, on the frozen and calibrated scales. The 1h verdict that gates Stage S does not exist, and `build_r34` needs the lens extension.
   - **No maker-toll object exists.** Every toll is the flat 10 bps round trip (5 taker/side).
3. **R3 nesting vector.** These do not exist:
   - per-lens as-of views for 1h, 12h and 1w;
   - a **signed** distance (`dist_atr` is unsigned; the side is in `near_side`);
   - **boundary coincidence** (0.25 ATR_L against L+1);
   - per-campaign timeline stamping beyond the funnel instants.

   `stamp_book` stamps 4h plus one lane lens only.
4. **R4 grid for L ∈ {1h, 4h, 12h, 1d}.**
   - BRK detection works on 4h and 1d via `macro_signals` (1h and 12h are blocked, see 1).
   - "Conditioned on L+1" does not exist.
   - Hold pins exist only for 5m (tuned) and 1d (tuned); 4h rows used the 5m pins.
   - The **null (gaps+order)** is in `scripts/tierc10_null.py` (other scout) and only for the filed lenses.
5. **P-BRK-4H.** There is no 4h BRK lane, lane string or LANE_ERA entry. The `run_lane_s1`/`run_lane_i1` runners cannot be reused (hard-wired lens and lane plus `require_lane_era`), so the lane must be composed from primitives and filed. A same-lens tide helper is needed (see the hazard in §2).
6. **Stage S scalper.** There is no:
   - target/take-profit exit in any ride (`ride_leg_l` and `_ride_leg10` exit only on STOP/BELL/HARVEST/TRAIL/corridor_end);
   - "no trail" range-trade ride;
   - 1h-boundary-breach invalidation;
   - maker fill model (limit at the 5m close, entry and target only) or maker bps;
   - 5m-ATR-tercile / 1h-boundary-age regime gate.
7. **R5 12h state.** There is no 12h stamp (census lens gap). The 4h `pct_of_range` decile exists.
8. **P-ADD-SFP / P-ADD-BRK.** `ride_leg_l` returns `adds: []`. There are no add mechanics in the BRK or TC10 rides (the TC10 lanes HALT on adds). A 1h harden/DIE event tape is needed (blocked by 1).
9. **F-C10-TOLL analogue for 1h and 4h (lane) tolls.** `get_toll` covers only filed lenses. A 1h toll must be filed to a grid first, or the law ("read from the grid table, never typed") breaks.
10. **Substrate.** Every TC10 module is welded to the `tc10_20260921` snapshot and `AS_OF_PIN.json` of 2026-09-21T16:00Z. A new as-of pin means new guards.

---

## 10. AMBIGUITIES (the contract's phrase, then what the code does)

- **R4(a) and P-BRK-4H: "first retest that HOLDS".** The code (census `retest_holds`, `B.band_hold_candidates`, the leash flip) gives ONE evaluation to the FIRST qualifying touch. If that retest fails, the DIE yields no candidate. The literal phrase names the rival reading, "first-retest-THAT-HOLDS", which `engine/rangefinder.py:550-560` filed as "not enacted". **Decide which is meant.**
- **P-BRK-4H: "first HOLD retest on the 89 tap".** The margin and hold pins are unstated. The options on file are 1.0 / 3 / 400 (the 5m tuning, which the census's 4h rows used) and the frozen flip pins 1.0 / 6 / 400. There is no 4h tuning.
- **P-BRK-4H: "v6 management".** It is unclear whether to include the BRK 12/25 ribbon bell (`ribbon=(12,25)`, TC10 R4) or to use pure v6 (`ribbon=None`, which is bit-identical to the card on 4h).
- **R1: "Macro scale self-calibrated per asset per lens to 0.75 confirmed ranges/100 bars".** TC10 lean L2 bars the calibrated scale from registered lanes and stamps as "in-sample by construction". It is unstated whether R3, R4, the scalper and P-BRK-4H ride calibrated or frozen 3.0. The CLASSIC5 picks are 5m 1.75 and 4h 2.00, very different from 3.0.
- **Stage S: "price in the lower (upper) third".** Third of the as-of box (`top`/`bot`) or of the span including deviation zones (`shi`/`slo`)? It is measured at the 5m close against a 1h view: **the 1h bar closing at that same instant: read or not?** (the two visibility laws in §6).
- **Stage S: "TARGET = the 1h range's far boundary minus 0.25 ATR_1h".** ATR_1h at which bar? Fixed at entry, or does the target move when the 1h range redraws after a harden?
- **Stage S: "invalidation also on a 1h boundary breach".** Breach-open (one 1h close beyond), harden, or DIE? Exit at which price and bar?
- **Stage S: "STOP = beyond the 5m structural pivot".** (5,5) pivot via `struct_stop_4h` with a 200-bar lookback (16.7 h at 5m), or a (2,2) fractal? And "beyond" = 0.5 ATR_5m?
- **Stage S: "maker toll (limit fill at the 5m close, entry and target only)".** No maker bps is on file (the v3 precedent is 2 bps/side). A fill always, or only on trade-through? The contract also says "R2 FAIL closes the lens … (maker twin below is the only reopening path)" while Stage S "stops" if R2 fails at 1h. Does R2 compute a maker-twin verdict itself?
- **Stage S: "P-SCALP-2 … holdout era".** The era cut is `TP.ERA_CUT_ISO = 2024-06-30T23:59:59Z`, on entry OPEN ms. The form tunes nothing, so it is unclear why the holdout is used rather than full.
- **R3: "signed distance to nearest boundary".** Signed by inside/outside, or by side (top +, bottom −)?
- **R3: "BOUNDARY COINCIDENCE (a boundary of L within 0.25 ATR_L of a boundary of L+1)".** Live boundaries only, or also memory lines? For 1w, "L+1" is undefined.
- **W1: "only 1h bars CLOSED before the 4h bar closes".** Strictly before, or at or before? (Four 1h bars close exactly at the 4h close.)
- **P-ADD-SFP: "at the trend-side boundary of the 1h range (the deviation back into range in the trade's favour)".** For a long, the "trend side" reads as the TOP, but a deviation back into range in a long's favour is a BOTTOM spring. The two halves conflict.
- **"NET OF … toll" carried forward.** TC10 never deducted the grid toll from `net_r` (`TOLL_ACCOUNTING`; open operator question Q2). For "H20/H100 net of L's toll" (a census-style event outcome) the census convention is `net = median(term) - toll_atr`. For trade books, `net_r` = fee + funding only.

---

## 11. How to call this from a new tierc11 script

```python
# shell:  export NAIAD_CACHE_DIR=/Users/luis/.cache/naiad/snapshots/tc10_20260921 PYTHONDONTWRITEBYTECODE=1
#         ~/venvs/naiad/bin/python scripts/tierc11_xxx.py
import sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path("/Users/luis/Naiad"); sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import tierc10_panel as TP          # substrate guard lives here (TP.substrate())
import tierc10_data as D            # D.load_asof(sym, lens), D.STEP_MS, D.load_pin()
import tierc10_brk as B             # frame/ride/stop/hold primitives
import tierc10_census as C          # asserts the snapshot AT IMPORT; as-of layer + grid
import tierc9 as T9                 # T9.V6_ROLES (tide 89/316, window 12/89, trigger 12/26)
import tierc7_rules as RC           # RC.build_pivots_4h, RC.struct_stop_4h, RC.spring_stop
from engine import indicators as ind

SYM = "BTCUSDT"

# ── (A) 4h breakout-retest on the 89 tap (P-BRK-4H shape), frozen scale ──
lf  = B.frame_l(SYM, "4h")                            # LensFrame: open_ms,o,h,l,c,atr,step_ms,fund_*
tp4 = C.load_tape(SYM, "4h")
assert np.array_equal(tp4.t0, lf.open_ms)             # indices are shared ONLY if bars are equal
sig = B.macro_signals(SYM, "4h")                      # {'dies':[(die_i,rid,'top'|'bottom')],'flips':[...]}
lo, hi = B.r1_band("tap-89")(lf.c)
MARGIN, HOLD = 1.0, 3   # <- AMBIGUOUS: the contract does not pin these (see §10)
cands, tally = B.band_hold_candidates(lf.h, lf.l, lf.c, lf.atr, sig["dies"], lo, hi,
                                      MARGIN, HOLD, B.MEM_TTL_BARS)
mem, mtally = B.memory_flip_candidates(lf.h, lf.l, sig["dies"], sig["flips"], lf.n)  # printed beside
ra   = B.roles_l(lf, T9.V6_ROLES)
tide = B.tide_state(ra["tide_f"], ra["tide_s"], lf.c)  # SAME-lens tide, read at entry bar
legs, refused = B.legs_from_candidates(lf, cands, "brk-4h",
                                       permit=lambda i, d: {"ok": int(tide[i]) == d})
lo_ms, hi_ms, meta = TP.corridor_era(TP.CLASSIC5, "full")
lo_i, hi_i = B.idx_range(lf.open_ms, lo_ms, hi_ms)
trades = B.brk_campaigns(lf, legs, TP.CONTROL_CARD, T9.V6_ROLES, "brk-4h", lo_i, hi_i,
                         ribbon=None, era=None)        # ribbon=(12,25) is the TC10 BRK bell
# registered path: g = TP.require_arm(reg_id, text, arm, panel, lanes=("brk-4h",)) FIRST,
# then book = TP.external_book(trades, g, lo_ms, hi_ms); TP.score(...) later.

# ── (B) an as-of range view on a lens the census does not know (1h/12h/1w) ──
class TapeL(C.Tape):
    @property
    def step(self):                                   # C.Tape.step reads C.LENS_MS -> KeyError on 1h
        return int(D.STEP_MS[self.lens])

def tape_l(sym, lens):
    k = D.load_asof(sym, lens)                        # closed bars <= AS_OF only
    t0 = k["open_time"].to_numpy(np.int64)
    o, h, l, c = (k[x].to_numpy(float) for x in ("open", "high", "low", "close"))
    ts = pd.to_datetime(t0, unit="ms", utc=True).strftime("%Y-%m-%dT%H:%M").tolist()
    # replicate load_tape's guards: monotone stamps, finite OHLC, gaps COUNTED
    return TapeL(sym, lens, o, h, l, c, t0, ts, ind.atr(h, l, c, 14), {"lens": lens})

t1  = tape_l(SYM, "1h")
m1  = C.run_scale(t1, C.FROZEN_SCALE)                 # or C.calibrate(t1)[0] — AMBIGUOUS (§10)
v1  = C.asof_view(t1, m1["macro"], m1["leash"])       # arrays: in_range, top, bot, pct(0..100), bnd_age, ...
dies_1h = [(e["i"], e["rid"], e["side"]) for e in m1["macro"]["events"] if e["event"] == "breakout-die"]

# ── (C) 5m 12/89 cross at the 1h as-of view ──
f5  = B.frame_l(SYM, "5m")
r5  = B.roles_l(f5, T9.V6_ROLES)                      # r5["w_up"], r5["w_dn"] = 5m 12/89 crosses
k1  = C.asof_index(t1, f5.close_ms)                   # 1h bar CLOSED <= 5m close (CLOSE law)
# k1 = B.visible_htf_idx(f5.open_ms, t1.t0, D.STEP_MS["1h"])  # the OPEN law (S1's tide) — pick one
ok  = k1 >= 0
live = np.zeros(f5.n, bool); live[ok] = v1["in_range"][k1[ok]]
pct  = np.full(f5.n, np.nan); pct[ok] = v1["pct"][k1[ok]]
long_sig = r5["w_up"] & live & (pct < 100 / 3)
# stop: pv5 = RC.build_pivots_4h(f5.h, f5.l); RC.struct_stop_4h(pv5, i, f5.c[i], +1, f5.atr[i], min_stop_atr=1.0)
# target: v1["top"][k1[i]] - 0.25 * t1.atr[k1[i]]   (a NEW ride is needed: no target exit exists)
# toll (bps): C.toll_bps_for(SYM) -> (10.0, source); toll_atr = bps/1e4 * close / atr  (file to a grid first)

# ── (D) stamping a ridden book (4h + one lane lens, 5m/4h/1d only) ──
import tierc10_stamps as S
out = S.stamp_book(trades, TP.CLASSIC5, lens="4h")    # out["instants"] carries rf4h_* columns
```

Notes for the snippet:
- `B.frame_l` memoises on `(sym, lens, with_funding)`.
- Frames reach back to the first bar. Windowing happens only through `lo_i` and `hi_i`.
- `brk_campaigns` requires `legs` with `r_dist > 0` and a finite ATR.
- Every real-book path must go through `TP.require_arm` before the first bar (LAW 4).
