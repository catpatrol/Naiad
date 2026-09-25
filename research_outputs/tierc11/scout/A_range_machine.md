# TC11 SCOUT · SUBSYSTEM A · THE RANGE MACHINE

Scout map for the TIER-C11 executor. Contract: `exchange/queue/2026-09-24_TC11_APOLLO.md` (103 lines, read in full).
Read-only survey, 2026-09-24, branch `v12-v1-census`. Every `file:line` below was read this session. Nothing
here is a result. The only code run was scratch smoke tests (output kept under the scratchpad, nothing filed)
that proved the call recipe in section 9 works on 1h, 12h, 1w and 15m tapes.

---------------------------------------------------------------------------------------------------------------

## 0 · THE FILES AND THEIR ROLES (shas measured now)

| file | lines | sha256 (now) | role |
|---|---:|---|---|
| `analytics/rangefinder_census.py` | 955 | `19c5507ff2d39b68…b7b37d` | **"the twin" TC11 R1 names.** It is a pure-numpy port of the machine: no IO, no engine import, and ATR is passed IN. O(n) bookkeeping, so it can do 5m full history. It is byte-equal to the engine by F-RF-EQ. It is NOT in `analytics._MODULES` (by design). |
| `engine/rangefinder.py` | 960 | `bbae464fdc8e0e01…4dab84d4` | The frozen machine of record. It is O(n²) and cannot do 5m history, and it computes its own ATR. The only reason to use it is an oracle in fixtures (`E.run_machine(df, pins)`). |
| `scripts/rangefinder_core.py` | 940 | `d2160521…9031` | A byte copy of the engine for the Oracle lane (OR-1/OR-2), kept equal by F-RF-1c/d/e. **Not a TC11 dependency.** |
| `scripts/rangefinder_twin.py` | 595 | `168d6229…206b` | The original calibration twin: KEY-A/B/C, `TARGETS_Q` at :112-117 (`Q3_conf_per_100 = (0.75, 0.375, 1.0)`) and `calibrate_v2` at :543. Its loaders are 4h/1d only. |
| `analytics/nesting.py` | 197 | `022e468b…66db` | **Value-area** nesting across 7d/30d/90d/365d windows (market profile). It is not range nesting (section 6). |
| `scripts/tierc10_census.py` | 4346 | `0e6cb635…a6ba75fb1a` | CENSUS-R: the tape loader, the calibrator, the **as-of layer**, event classes, outcomes, and [Q-R3]/[Q-R4]. |
| `scripts/tierc10_census_fixtures.py` | 3227 | — | F-RNG-ASOF (with sabotage), F-RNG-ASOF-SEAL, F-GRID, F-C10-TOLL, F-CEN-*, F-DET, F-C10-ACC/HT. |
| `scripts/tierc10_stamps.py` | 1349 | — | Stage A: stamps campaign instants with the 4h as-of view. This holds the "five-row table" R5 extends. |
| `scripts/tierc10_brk.py` | — | — | `macro_signals()` at :2332 is **the firewall adapter pattern** a range-conditioned decision must copy. |

The census `code_sha()` (tierc10_census.py:393) is sha256 of `tierc10_census.py` bytes plus port bytes. Now it is
**`5c63aadd6ee509f2…12b8`**, which equals the R34 build's code_sha. The 102 census cell receipts
(`census/cells/*/cell.json`) and `build_manifest.json:code_sha` carry **`629d2863…cb82`**. See GAP G10.

---------------------------------------------------------------------------------------------------------------

## 1 · THE API: RUN THE RANGE MACHINE ON A BAR FRAME

### 1.1 The port (analytics/rangefinder_census.py)

```python
RC.run_machine(d, atr, pins: dict) -> dict                # :258
RC.run_v2(d, atr, pins_v2: dict, mem_cap=None, with_micro=True, retests=True) -> dict   # :915
RC.macro_pins(scale_mult, pins=None) -> dict               # :215  scales ONLY LEG_MIN and REV_MIN
RC.flips_and_leash(macro, d, atr, pins_v2, mem_cap=None, retests=True) -> list[dict]    # :702
RC.machine_known_at(m) -> list[int]                        # :879  pivot -> its SEAL, others -> own bar
RC.leash_known_at(leash, hold_bars) -> list[int]           # :890  flip/failed/truncated -> i + HOLD
RC.span_at(r, events, i, _index=None) -> (bot, top)        # :641  reads 2-dp prices (containment only)
RC.containment(micro, macro)                               # :659  micro only; TC10 never ran micro
```

- **`d`** (:223 `_tape`) is anything indexable by `"o","h","l","c"` and optionally `"ts"`, or the tuple
  `(o,h,l,c[,ts])`. Position is the bar index. `ts` must be a sortable STRING per bar.
- **`atr`** must be finite on every bar. It HALTs on NaN (:244). It must be
  `engine.indicators.atr(h,l,c,14)`: Wilder RMA seeded at TR[0] (engine/indicators.py:31-54). The ATR of a prefix
  equals the prefix of the full ATR, so `tape.head(t)` is legal. A tail re-warms the ATR and is illegal.
- **The census call** (tierc10_census.py:648) is
  `C.run_scale(tape, scale) = RC.run_v2(tape.d, tape.atr, dict(RC.PINS_V2, SCALE_MULT=scale), with_micro=False, retests=False)`.
  It runs the macro scale only with a lean leash.

**`run_v2` returns:** `macro`, `micro`(None), `kept`(None), `suppressed`(None), `micro_kept_events`(None), `leash`,
`flips` (leash rows with event=="flip"), `state` (final), `macro_count_feb_aug` (a BTC literal, ignore) and
`status_line`.

**`run_machine` (macro) returns:** `events` (sorted by `i`), `pivots` [(bar, px, +1 high/−1 low)], `ranges`
[Range], `coverage_pct`, `n_bars`, `n_pivots`, `n_confirmed`, `n_potential_unresolved`,
`mean_confirmed_lifetime` (dead only), `n_lifetime_censored`, `n_pending_open`, `final_state`
(NEUTRAL|BULL_EXP|BEAR_EXP) and `status_line`. Two keys are ADDITIVE: **`seals`**, the bar each pivot became
knowable, aligned with `pivots` and never −1; and **`covered`**, a bool mask per bar.

**`Range` fields** (:185-212, dataclass): `rid, top, bottom, top0, bottom0, seed_i, confirm_i, die_i, state`
(POTENTIAL|CONFIRMED|DEAD|INVALIDATED|SUPERSEDED)`, confirm_side, dev_top_ext, dev_bot_ext, n_deviations,
mem_top_frozen_i, mem_bot_frozen_i, pending, born_at, backdated_from, n_inception_zones, p0_bar, p1_bar`. The
`.mid` property is (top+bottom)/2.
**`Range.top/.bottom/.n_deviations` are END-OF-RUN values. Reading them at bar t is THE leaked-redraw
sabotage.** Take as-of boundaries from `asof_view` (1.2).

### 1.2 Range records: events and their stamps

The machine events are `{"i", "ts", "event", …}`. Every float keyword is rounded to 2 dp, so **never read a
price from an event**. Read prices from the tape or from the view.

| contract term | machine event (kind, fields) | known at | file:line |
|---|---|---|---|
| pivot | `pivot` {px, side high/low, knowable_at} | its **SEAL** (`m["seals"]`); `knowable_at` can read −1 | :303-330, :587-592 |
| seed | `seed` {rid, top, bottom, p0_bar, p1_bar, inception_zones}. Body extremes of the pivot bars (BOUNDARY_MODE body) | i | :408 |
| **confirm ts** | `confirm` {rid, boundary, top, bottom, mid} and `backdate` {born_at, backdated_from} | i (= `r.confirm_i`) | :437-445 |
| inception deviation | `inception-deviation` {rid, side, extreme, boundary}. Spring-birth; it never moves a boundary | i (confirm) | :446-451 |
| breach | `breach-open` {rid, side, px, boundary} | i | :469-479 |
| **deviation confirmed = swing failure** | `harden` {rid, side, bars_outside, extreme}. A close back inside within DEV_RETURN_BARS=7 of breach-open. **Bottom harden is a spring, top harden is an upthrust.** | i | :494-515 |
| **redraw ts** | `redraw` {rid, side, frm, to, mid} on the SAME bar as the harden. The boundary goes to the episode's **wick** extreme (REDRAW_BASIS wick) | i | :516-518 |
| late return | `breach-lapse` {rid, side, bars_outside}. No redraw. Unreachable at these pins | i | :520 |
| **macro death** | `breakout-die` {rid, side top/bottom, by n_closes/margin, closes, px}. Latches BULL_EXP (top) or BEAR_EXP (bottom) | i (= `r.die_i`) | :524-538 |
| memory-line touch (v1) | `memory-touch` {rid, side, px}. The first ONE-SIDED touch of a dead range's top/bottom after death | i | :542-560 |
| memory-line lifecycle | leash: `line-expired` {reason cap/ttl}, `memory-retest` {verdict}, **`flip`** {polarity support/resistance, glyph, parent_death, retest} | flip / failed / truncated at **i + FLIP_HOLD_BARS (6)** | :702-869, :890-912 |

**Macro state:** the port does not emit per-bar state. `asof_view` replays it. **Deviations per side:**
`asof_view.dev_top/dev_bot` count the hardens so far. **Memory line:** a line is the DEAD range's final
top/bottom, born at `die_i`, capped at 6 live per side (`MEM_CAP_PER_SIDE`), with ttl 400 bars.
**Flip:** the first OPPOSITE-side two-sided touch of a line that has no close through by
1.0×ATR over bars i..i+6. A **top** line flipping becomes **support** (+1). A flip is ONE evaluation per line.

### 1.3 The as-of layer (scripts/tierc10_census.py): the per-bar arrays

`C.asof_view(tape, macro, leash) -> dict` (:745-891). Element t is what a reader at the CLOSE of bar t knows.
It RAISES if the replay does not land on the machine's own end-state or coverage mask. It needs `macro["covered"]`,
so it works with the port only. It requires REDRAW_BASIS wick and MULTI_ACTIVE 0.

| key | meaning (all arrays have length n) |
|---|---|
| `rid` (int64, −1) / `in_range` (bool) | a CONFIRMED macro range is alive: `confirm_i <= t < die_i` |
| `state` (int8) | 0 NEUTRAL, +1 BULL_EXP, −1 BEAR_EXP. The latch is replayed from confirm, breakout-die and the first SEALED pivot. **0 also means "nothing known yet". Disambiguate with `in_range`** (tierc10_stamps.macro_state_of :684 collapses it to NONE/NEUTRAL/BULL_EXP/BEAR_EXP). |
| `top` / `bot` (float, NaN out of range) | **as-of** boundaries: top0/bottom0 from confirm, moved by each harden FROM the harden bar to `max(h[open_i..i])` / `min(l[…])` at full precision |
| `pct` | `100*(c-bot)/(top-bot)`, **unclamped** (<0 or >100 on breach bars) |
| `dist_atr` / `near_side` (+1 top / −1 bottom, tie goes to top) | `min(|top-c|,|c-bot|)/atr[t]`. **Unsigned** |
| `top_age` / `bot_age` / `bnd_age` / `range_age` | bars since that side's as-of value last changed (confirm or harden). `bnd_age` = the nearest side's. `range_age = t - confirm_i`. −1 out of range |
| `dev_top` / `dev_bot` | hardens on that side so far (0 out of range) |
| `inc_top` / `inc_bot` | 1 if the defining wick lay beyond the body at confirm |
| `covered` | equals the machine's coverage mask (asserted) |
| `flip_pol` (+1/−1/0), `flip_age`, `flip_rid` | the last flip KNOWN (touch+6 ≤ t). **This survives dead ranges.** |
| `_by_rid`, `_leash_frame` | private |

- `C.ASOF_ARRAYS` (:937) is the 20 keys F-RNG-ASOF compares.
- `C.asof_index(tape, instant_ms) -> ndarray` (:894) gives the last bar whose close ≤ instant, or −1.
  `closes = t0 + tape.step`.
- `C.stamps_at(tape, view, idx) -> dict` (:906) returns the keys `rf_lens, rf_bar_close_ms, rf_state,
  rf_in_range, rf_pct_of_range, rf_dist_boundary_atr, rf_nearest_side, rf_boundary_age, rf_range_age,
  rf_dev_top, rf_dev_bot, rf_inception_top, rf_inception_bot, rf_last_flip, rf_last_flip_age`. Geometry is
  None when not in range; the flip fields survive.
- `C.known_frame(m)` (:715) returns a DataFrame [pos, i, known_at, event, rid, side].
- `C.leash_frame(leash, hold)` (:734) returns a DataFrame [pos, i, known_at, event, rid, side, verdict].
- `C._step_fill(n, cps, fill, dtype)` (:699) is the step-function builder every array uses.

### 1.4 Event classes and outcomes

- `C.census_events(tape, macro, leash, view, bands=RETEST_BANDS, retest=None) -> (evf, hold_tally)` (:1267).
  - `evf` columns: **[cls, i, known_at, rid, side, sgn]**.
  - `cls` ∈ `C.CLASSES` (:149): `breach, harden, DIE, memory-touch-v1, memory-touch-2s, flip-hold,
    retest-hold-ribbon89_127, retest-hold-ribbon127_200, retest-hold-tap89, retest-hold-tap127, retest-hold-tap200`.
  - Signs (`SIGN_LAW` :199): breach and DIE use the side direction (top +1). **harden uses −side (a spring is
    +1 long, an upthrust −1 short).** Memory touches use the parent-death direction. flip-hold uses polarity.
    Retest-hold uses the DIE direction.
  - Anchors (`ANCHOR_LAW` :210): `known_at`. flip-hold is touch+6. Retest-hold is touch+hold_bars.
- `C.retest_holds(tape, dies, lo, hi, margin_atr, hold_bars, ttl_bars)` (:983) is the band retest detector. It is
  **ONE-SHOT**: the first touch from the die side gets the only evaluation, and there are no rows for
  never-retested DIEs. It returns [rid, side, die_i, touch_i, known_at, verdict hold/failed/truncated].
  `C.band_of("tap89"|"ribbon89_127"…)` (:969) gives EMAs of close, NaN until `period` bars.
- `C.outcome_ledger(tape, evf, view, bps)` (:1352) adds **known_close_ms, bad_atr, toll_atr_evt,
  cens_H20, term_H20, mfe_H20, mae_H20, cens_H100, term_H100, mfe_H100, mae_H100, era, state_at, in_range_at,
  pct_at, dist_atr_at, flip_pol_at**. `term = sgn*(c[k+H]-c[k])/atr[k]` from the close of `known_at`, H in
  bars of the lens. A horizon past the end is CENSORED, never shortened.
  `toll_atr_evt = bps/1e4 * c[k]/atr[k]`.
- `C.spring_overlap(tape, macro, view, look=20)` (:1501) gives spring (bottom) and upthrust (top) kinship between
  hardens and the house 20-bar sweep-reclaim shape.

---------------------------------------------------------------------------------------------------------------

## 2 · THE MACRO SCALE AND THE SELF-CALIBRATION (tierc10_census.py)

- `FROZEN_SCALE = RC.PINS_V2["SCALE_MULT"] = 3.0` (:126).
- `SCALE_GRID = (1.5, 1.75, …, 4.0)`: 11 cells, step 0.25 (:127, the Pine minval/step).
- `DENSITY_TARGET_PER_100 = 0.75` (:129, held equal to twin `TARGETS_Q["Q3_conf_per_100"][0]`,
  rangefinder_twin.py:115).
- `SCALE_KINDS = ("frozen3.0", "calibrated")` (:132).
- `density_per_100(m) = 100*n_confirmed/n_bars` (:654). The whole tape counts, with confirmed ranges only.
- **`pick_scale(dens)`** (:658) picks the grid cell nearest the target. Ties go toward 3.0, then to the lower scale.
  It uses no bisection because density is not monotone.
- **`calibrate(tape) -> (pick, grid_df)`** (:666-695) runs `RC.run_machine(tape.d, tape.atr, RC.macro_pins(s))`
  for all 11 scales on the **WHOLE tape**, so the pick is **in-sample by construction**.
  - grid_df columns: `asset, lens, scale_mult, n_bars, n_confirmed, density_per_100, abs_err_to_target,
    coverage_pct, mean_confirmed_lifetime, density_quantum_per_100, is_frozen_pin, chosen, pick_at_grid_edge,
    target_bracketed, target_per_100, tie_break, calibrated_in_sample`.
- `macro_pins(s)` multiplies only LEG_MIN (0.5) and REV_MIN (1.75) by s. Every other pin is shared.
- **LEAN L2** (:297-301) says: *"every registered lane and every Stage-A stamp uses the FROZEN 3.0 …
  CENSUS-R prints the self-calibrated SCALE tables WITH the frozen-3.0 tables beside."*
  `IN_SAMPLE["calibrated"]` (:1596) adds: *"no registered lane and no Stage-A stamp may read it"*.

**TC10 picks** (`census/scale_grid.parquet`, `chosen==True`):

| asset | 5m | 4h | 1d |
|---|---|---|---|
| BTC | 1.75 | 2.00 | 2.25 |
| ETH | 1.75 | 2.00 | 2.00 |
| SOL | 1.75 | 2.00 | 2.50 |
| NEAR | 1.75 | 2.00 | 2.00 |
| ZEC | 1.75 | 2.00 | 2.50 |

UNSEEN12: 5m 1.75–2.0, 4h 1.5–2.25, 1d 1.5–2.5. There are two edge clamps, XMR 1d 1.5 and XMR 4h 1.5. The 1d
clamp is not bracketed (density 0.62). At frozen 3.0 the density is about 0.36–0.55 per 100, roughly half the
target.

**Scratch smoke test** (BTC, TC10 snapshot, nothing filed; these are facts about the grid, not a result):

| lens | bars | confirmed ranges at 3.0 | pick |
|---|---:|---:|---:|
| 1h | 61,679 | 223 | 2.0 |
| 12h | 5,140 | 18 | 1.75 |
| 1w | 367 | 2 | 2.5 (density quantum 0.27/100) |
| 15m | 246,713 | 917 | 2.0 (2.1 s per scale) |

---------------------------------------------------------------------------------------------------------------

## 3 · THE PINS, AND WHAT "pins = TC10 sha" CAN MEAN

**The port literals** (rangefinder_census.py:132-160):

| pin | value | where |
|---|---|---|
| `ATR_LEN` | 14 (the ZigZag warm floor; ATR comes in from outside) | :132 |
| `PINS` | `LEG_MIN 0.5 · REV_MIN 1.75 · TOUCH_EPS 0.60 · DEV_RETURN_BARS 7 · BREAK_CONFIRM_N 8 · BREAK_MARGIN 1.5 · BOUNDARY_MODE "body" · REDRAW_BASIS "wick" · MULTI_ACTIVE 0` (the key order is the export order) | :136-148 |
| `PINS_V2` | `SCALE_MULT 3.0 · FLIP_HOLD_MARGIN 1.0 · FLIP_HOLD_BARS 6 · MEM_TTL_BARS 400` | :154-160 |
| `MEM_CAP_PER_SIDE` | 6 | :152 |
| `V2_WINDOW_BARS` | 1700 (the Oracle's; the census runs FULL history) | :150 |
| `STEP0_SHA256` | pine `4bed1e01…`, twin `7646b576…` (at STEP 0), engine `bbae464f…` | :162-169 |
| `EVENT_SHAS_OF_RECORD` | the five BTC 4h event-log shas | :173-179 |

Note that BREAK_CONFIRM_N=8 is nearly dead: 82–87% of deaths come through the 1.5 ATR margin (digest §A).

**Census-level pins** (`C._pins_block()` :1721, filed in every `cell.json`):
- `SCALE_GRID`, `DENSITY_TARGET_PER_100`
- `HORIZONS ((H20,20),(H100,100))` :123 and `SPRING_LOOK 20` :133
- `ERA_BOUNDARY_MS 1719791999000` (2024-06-30T23:59:59Z) :164, `ERAS (ALL, tuning, holdout)`
- **`RETEST_PINS`** (:290, resolved from `census/TUNING_RESULT.json`): `margin_atr 1.0, hold_bars 3, ttl_bars 400`,
  scored_band `ribbon127_200`, grid_sha `2135ca66…`. **This single 5m-tuned pair is applied to every lens.**
- 1d separate tuning (`TUNING_RESULT_1d.json`): `ribbon89_127, margin 0.25, hold 6, ttl 400`, n 44.

**Gate thresholds** (:2153-2183):
- `HEIGHT_CAPTURE_FRAC 2/3`, `HEIGHT_RATIO_MIN 3.0`, `INFEASIBLE_MAX_SHARE 0.10`
- `HEIGHT_MIN_N_RANGES = EDGE_MIN_N_RANGES = EDGE_MIN_N_BARS = PROVISIONAL_MIN_N = 30`
- `EDGE_NEAR_FRAC 0.2`, `AGE_BUCKETS ((0,5),(5,10),(10,20),(20,40),(40,80),(80,inf))`
- `STALE_RUN_N 6`, `TIME_BEYOND_T = PINS["DEV_RETURN_BARS"] = 7`
- `HEIGHT_GATE_LAW_SHA` and `ACCEPTANCE_LAW_SHA` (digest: `907649b8…`) are hashed from the law dicts

**Where "the TC10 sha" is recorded:**
- `research_outputs/tierc10/STEP0_RECORD.json` → `sources`: port `19c5507f…` (48,328 B), engine `bbae464f…`
  (49,981 B), pine `4bed1e01…`, twin now `168d6229…` (at STEP 0 `7646b576…`; the difference is loader-only).
  `pins_of_record` holds the 12 pins with `pins_key_order`, and `pins_reconciled` reads "PINS-OK 12/12".
- `research_outputs/tierc10/REGISTRY_PIN.json` carries **no range pins**. It pins the six registrations only
  (registry head `7621a857…`, m=6).
- `research_outputs/tierc10/PROGRESS.json` gives the STEP 0 stage one-liner, "PINS-OK 12/12 … TOUCH_EPS 0.60 /
  DEV_RETURN_BARS 7 / BREAK_CONFIRM_N 8 / SCALE_MULT 3.0 / ATR_LEN 14". CENSUS-R stage artifact shas include
  `census/build_manifest.json 54959c7b…` and `R34_MANIFEST.json 2663d923…`.
- `census/build_manifest.json` has `port_sha256 19c5507f…` and `code_sha 629d2863…`. Its `r34.code_sha` is
  `5c63aadd…`.

**Recommended reading of "pins = TC10 sha":** HALT unless all of these hold:
1. `sha256(analytics/rangefinder_census.py) == 19c5507f…` and `sha256(engine/rangefinder.py) == bbae464f…`,
   both equal to STEP0_RECORD.json `sources.*.sha256_expected`.
2. `RC.PINS | RC.PINS_V2 | {ATR_LEN}` equals `STEP0_RECORD.pins_of_record`, key order included.
3. If any retest class is used, `C.RETEST_PINS["grid_sha"] == 2135ca66…`.

Print all three with `C._pins_block()`. See ambiguity A1.

---------------------------------------------------------------------------------------------------------------

## 4 · AS-OF CAUSALITY: HOW TC10 GUARANTEES IT (F-RNG-ASOF)

The mechanism (tierc10_census.py):
1. Every array is a `_step_fill` of change points stamped at the bar where the fact becomes known: confirm at
   `confirm_i`, harden/redraw at the harden bar `i`, death at `die_i`, flip at `touch+6`, state from the first
   SEALED pivot.
2. Boundaries are rebuilt from raw bars (`h[a_open:i+1].max()`), never from `Range.top` or from events.
3. `known_frame` / `leash_frame` give each event a `known_at`.
4. The replay is asserted equal to the machine's end state (:822-824, :852-853).
5. `asof_index` reads only CLOSED coarse bars (:894-900).
6. Stage-A `stamps_at` raises if `bar_close_ms > instant_close_ms` (tierc10_stamps.py:735-742).

**The fixture** (tierc10_census_fixtures.py):
- `ASOF_TAPES` :224-225: BTC 4h/1d, ETH 4h/1d, SOL 5m[:60000]; `ASOF_SCALES (3.0, 2.0)`.
- `_cuts()` :287-302 draws 14 seeded random cuts plus 5 each aimed at harden, harden+1, confirm, confirm+1,
  inside a flip hold, and at seals.
- `asof_corpus()` :327-394 checks, for each cut t, that each of the 20 `ASOF_ARRAYS` on `tape.head(t)` equals the
  full array `[:t]`. It also compares the class events with `known_at <= t-1`, the known_at-filtered
  macro and leash log shas, and the state, bounds, n_deviations and coverage at t−1 against the
  **machine's own** prefix run (`_oracle` :305, which uses the engine on 1d).
- **The leaked-redraw sabotage** (`_law_views` :241-285, leg 1 at :251-258) copies the view and overwrites
  `top/bot[confirm_i:die_i]` with the END-OF-RUN `r.top/r.bottom`, then re-derives pct and dist_atr. The
  same leaky reader is applied to the full run and to every prefix, so it turns RED only through prefix
  instability.
- The other plants are flip-at-stamp (anchor at i, not i+6), backdated-edge (alive from `backdated_from`) and
  naive-known-at (a pivot at its wick).
- `asof_break()` :397 passes only if EVERY tape×scale catches the plant. `asof_real()` :419 must show 0 mismatches.
  The filed result is 440 cuts, 10 runs, 0 mismatches.
- The harness is `RFX = tierc10_rf_fixtures`: `say` :129, `prove(fixture, title, fails_if, break_leg, real_leg)`
  :144, `plants(rows)` :167, `sha` :182. The leg registry is at tierc10_census_fixtures.py ~:3060.
- **The pivot `knowable_at = -1` quirk:** `known_frame` raises if known_at < i (:724-727). F-RNG-ASOF-SEAL proves
  seals on NEAR 4h, UNI 4h and SOL 5m.
- **Era safety for detectors** (F-BRK-ERA, tierc10_brk_fixtures.py:2865): DIEs on the full tape equal DIEs on the
  era-cut tape.

**For F-NEST-ASOF:** cut ALL lenses at one instant T, with `tape_L.head(asof_index(tape_L, T)+1)`. Recompute
every lens view and the nest vector. Require equality with the full vectors at instants ≤ T. Plant the leak by
building a nest from `Range.top/.bottom`. **Caveat:** TC10 proved prefix-stability at a FIXED scale. The
calibrated pick is not prefix-stable (it is fit on the whole tape). See A2 and G12.

---------------------------------------------------------------------------------------------------------------

## 5 · WHAT CENSUS-R COMPUTED

**Commission:** PANEL17 = CLASSIC5 (BTC ETH SOL NEAR ZEC) + UNSEEN12 (ENA PUMP HYPE MNT_BYBIT SUI LTC XMR BNB UNI
1000PEPE DOGE 1000BONK), × lenses {5m, 4h, 1d} × {frozen3.0, calibrated} × eras {ALL, tuning, holdout} ×
{H20, H100}.
- Pools: POOLED:ALL, POOLED:CLASSIC5, POOLED:UNSEEN12.
- AS_OF is 2026-09-21T16:00Z (`research_outputs/tierc10/data/AS_OF_PIN.json`), on snapshot
  `~/.cache/naiad/snapshots/tc10_20260921`.
- The toll is 10 bps round trip on all 17 assets (`data/fee_schedule.json:round_trip_bps_used`,
  `taker_bps_side_used` 5). The haircut twin tiers are A 2 / B 5 / C 10 bps per side slippage.
- The NULL (`scripts/tierc10_null.py`, random-boundary boxes) ran frozen3.0 only on 5m/4h/1d, K=20, with the
  variants gaps-only and gaps+order (gaps+order is of record per R10).

**Tables** in `research_outputs/tierc10/census/`. Every table also carries the collar columns
(`tier, gates, m_looks_this_table, m_note, in_sample`) and the as-of columns (`as_of_last_closed_4h,
as_of_panel_start, as_of_span_days, warranty, as_of_lens, as_of_last_closed_bar, as_of_panel, as_of_n_assets,
as_of_substrate`).

| table | rows | key | payload columns (collar and as-of omitted) |
|---|---:|---|---|
| `outcome_grid.parquet` | 7,920 | asset, lens, cls, scale_kind, era, horizon | horizon_bars, horizon_unit, era_law, scale_mult, pins_status, retest_pins, printable, pooled, n_events, n, n_censored, n_bad_atr, toll_atr_all, median_term, mean_term, q25_term, q75_term, hit_rate, hit_rate_net, median_mfe, median_mae, toll_atr, binding_over_n_assets, toll_pooling, net, nan_reason, provisional, toll_bps, toll_bps_source, sign_law, anchor_law |
| `coverage.parquet` | 102 | asset, lens, scale_kind | scale_mult, n_bars, coverage_pct, n_confirmed, density_per_100, mean_confirmed_lifetime, n_lifetime_censored, n_died, n_pivots, n_flips, bars_in_live_range_pct, final_state, gap_count, missing_bars_total, coverage_law, lifetime_law |
| `scale_grid.parquet` | 561 | asset, lens, scale_mult | see section 2 |
| `height_toll.parquet` | 360 | asset, lens, scale_kind, era | n_ranges, height_atr_median, toll_atr_median, ratio_median, ratio_mean, ratio_final_median, share_ratio_lt_1, share_ratio_lt_min, ratio_min_pinned, infeasible_max_share, capture_frac, min_n_ranges_pinned, provisional, provisional_law, gate_law, gate_law_sha, ratio_d1..d9, gate_height_pass, gate_height_fail_reason, toll_bps, toll_bps_source, toll_basis, toll_atr_binding, ratio_median_under_binding_toll |
| `edge_fade.parquet` | 55,440 | asset, lens, scale_kind, era, entry_decile, age_bucket, horizon | direction, is_near_boundary, age_bars_lo, age_bars_hi, margin (cell / MARGIN_BY_DEC / MARGIN_BY_AGE / MARGIN_NEAR), n, n_ranges, median_term, hit_rate_net, toll_atr, net, near_frac, age_law. **entry_decile −1 means all deciles on the near edge; age_bucket "ALL".** The gate's own statistic is `(−1, "ALL", H20)`. |
| `height_toll_verdict.parquet` | **360** | lens, scale_kind, asset, era | era_law, era_boundary_ms, era_window, era_judged_law, n_ranges, ratio_median, ratio_d1, ratio_d5, ratio_d9, share_ratio_lt_1, height_atr_median, toll_atr_median, gate_height_pass, edge_n, edge_n_ranges, edge_median_term_h20, edge_toll_atr, edge_net_h20, edge_hit_rate_net, gate_edge_fade_pass, gate_edge_fade_fail_reason, gate_height_fail_reason, min_n_ranges_pinned, edge_min_n_ranges_pinned, edge_min_n_bars_pinned, provisional, provisional_reason, **verdict_pass**, verdict_law, min_n_law, gate_law_sha, ledger_line, gates_what, reason |
| `acceptance_head_to_head.parquet` | 3,600 | asset, lens, scale_kind, variant, era, horizon | definition, n_episodes, n_declared, declare_rate, n_never_declared, n_declared_died, n_declared_survived, precision_died, lead_bars_median, lead_bars_p10, lead_bars_p90, n_lead_compared, n_die_by_margin, n_die_by_n_closes, n_outcome, median_term, hit_rate_net, toll_atr, net, provisional, provisional_law, toll_basis, acceptance_law_sha, time_beyond_T, time_beyond_T_source, promoted, engine_default_after |
| `hold_tally.parquet` | 612 | asset, lens, scale_kind, anchor | band, pins_status, n_candidates, n_evaluated, n_hold, n_failed, n_truncated, n_not_evaluated, margin_atr, hold_bars, ttl_bars, scale_mult |
| `spring_overlap.parquet` | 204 | asset, lens, scale_kind, side | shape, look_bars, n_hardens, n_law_reclaim, n_hardens_also_sweep_look, n_house_shapes, n_house_shapes_inside_episode, scale_mult |
| `cells/<SYM>__<lens>/events.parquet` | per cell | asset, lens, scale_kind, cls, rid, side, i | the `outcome_ledger` columns (1.4) plus scale_mult and pins_status |

The manifests are `build_manifest.json`, `R34_MANIFEST.json` (with `replay_by_cell`) and the digest
`CENSUS_R_DIGEST.md` (1,896 lines). The 5m holdout retest-hold rows are **collared** (`printable()` :190).

**[Q-R3] functions** (all pure, keyed off a Tape and a macro run):
- `_r34_walk(tape, macro, pins)` :2334 re-walks each confirmed range's breach lifecycle at full precision
  (proved equal to breakout-die). It returns `episodes`, `ranges` [rid, confirm_i, die_i, close_ms, height_px
  (top0−bottom0), height_px_final, close_at_confirm, atr_at_confirm, life_bars] and in-range arrays `ir_t, ir_pct
  (0..1), ir_age, ir_rid`.
- `height_rows(walk, tape, asset, lens, kind, bps)` :2636 computes `ratio = height_atr / toll_atr` at the confirm
  bar. It is scale-free because the ATR cancels.
- `height_grid(hl, asset, lens)` :2659.
- `edge_arrays(tape, walk, bps, aid)` :2710 considers every in-range bar and fades toward the far boundary.
  `sgn = +1 if pct<0.5`, `dec = min(int(pct*10), 9)`. Bars outside or at exact mid are excluded and counted.
- `edge_gate(A, pooled, era)` :2863 passes iff near-20% H20 `net = median(term) − toll > 0`, `edge_n ≥ 30` and
  `edge_n_ranges ≥ 30` within the era.
- `verdict_rows(hg, eg, lens)` :2899 computes `verdict_pass = gate_height_pass AND gate_edge_fade_pass`.
- Reader: `height_vs_toll_verdict(lens, root, asset="POOLED:ALL", scale_kind="frozen3.0", era="ALL",
  allow_provisional=False)` :3005. It HALTs when the table is missing, the era is absent, the law sha has moved,
  or the row is provisional.
- Builder: `build_r34(root, assets, lenses, kinds, label)` :3116. It reads the calibrated scale and bps from
  `cells/*/cell.json`.
- A scratch smoke test ran `_r34_walk → height_rows/grid → edge_arrays → edge_gate → verdict_rows` and
  `acceptance_rows` on an **ETH 1h** Tape11. The replay equalled breakout-die (231/231).

**Acceptance [Q-R4]:** 5 rules ( 2-close, 3-close, 6-outside-close-stale-run, time-beyond (T=7), RangeFinder-DIE
(8-close OR 1.5 ATR)) on one breach-episode denominator. Nothing is promoted. The data's default per lens at ALL
H20: 5m stale-run (every rule NET-negative), 4h RangeFinder-DIE (+0.0459), 1d time-beyond (+0.7492).

**Results per lens: the [Q-R3] verdict (height AND edge-fade), single assets, PASS out of 17:**

| lens | frozen3.0 ALL / tuning / holdout | calibrated ALL / tuning / holdout |
|---|---|---|
| 5m | **0 / 2 / 0** | **0 / 1 / 0** (height 17/17 PASS; the edge leg fails) |
| 4h | 3 / 4 / **0** | 5 / 1 / 6 |
| 1d | **0 / 0 / 0** (17/17 provisional, <30 ranges per asset) | 0 / 0 / 0 |

**Pooled verdict rows** (edge NET H20 in ATR):
- 5m: FAIL on every pool, era and scale (POOLED:ALL frozen ALL −0.364, holdout −0.573).
- 4h: FAIL everywhere except **frozen CLASSIC5 holdout PASS (+0.0062)**. POOLED:ALL frozen is −0.135 on ALL and
  −0.130 on holdout.
- 1d: PASS only on the **tuning** era (all pools, both scales) and on frozen CLASSIC5 ALL (+0.044). **Holdout
  FAILs on every pool** (CLASSIC5 frozen −0.436, provisional).
- Totals: era ALL 9, tuning 13, holdout 7 PASS out of 120 each.
- The height leg never binds. Median height/toll is 24 (5m), 184 (4h) and 437 (1d) because REV_MIN×SCALE pins the
  height at about 6.5 ATR (frozen). **The edge-fade leg is the binding constraint.**
- CLASSIC5 single-asset 4h passes: ZEC frozen ALL (+0.145) and tuning (+0.139); ETH calibrated holdout (+0.084).
  SOL calibrated holdout is +0.545 but provisional (29 ranges).
- "5m FAILS 0/17" in PROGRESS is the **holdout** figure carried on P-BRK-S1's row.

**R5's base, "the five-row table":** `research_outputs/tierc10/stamps/control_entry_by_state.parquet`, built by
`tierc10_stamps.entry_state_crosstab` (:1093). The v6 control has 200 campaigns on CLASSIC5, stamped on the 4h
lens at frozen 3.0.

| state at entry | n | expectancy R | win % |
|---|---:|---:|---:|
| BEAR_EXP | 40 | −0.016 | 37.5 |
| BULL_EXP | 66 | +0.220 | 28.8 |
| NEUTRAL (in-range) | 94 | +0.297 | 37.2 |
| NONE | 0 | — | — |
| ALL | 200 | +0.209 | 34.5 |

The median pct at NEUTRAL entries is 40.5. The stamped book is `control_v6_stamped.parquet`: 5,745 instants with
`rf4h_*` columns (macro_state, in_range, range_id, pct_of_range, dist_boundary_atr, nearest_side, boundary_age,
range_age, dev_top, dev_bot, inception_top, inception_bot, last_flip, last_flip_age, state_latch, bar_open_ms,
bar_close_ms, bar_lag, bar_lag_ms), keyed [asset, instant_ms, instant_kind]. **No 12h stamps exist.**

---------------------------------------------------------------------------------------------------------------

## 6 · WHAT analytics/nesting.py PROVIDES

It works on **value areas** (VAL/VAH), not ranges.
- `ADJACENT_PAIRS (("7d","30d"),("30d","90d"),("90d","365d"))` :37.
- `va_nesting(short_val, short_vah, long_val, long_vah)` :47 returns `{state ∈ nested_inside | nested_outside |
  overlapping | disjoint_above | disjoint_below, overlap_frac (÷ shorter), consensus_band, gap_band,
  facing_edges, short_va, long_va}`.
- `price_location(price, nest)` :105, `nesting_levels(pair, nest)` :132 and `describe_nesting(pair, nest)` :164
  (prose).
- It has no lens ladder, no as-of, no ATR, no boundary coincidence and no range state.
- **It is in `analytics._MODULES`** (analytics/__init__.py:118-120) and is imported by `scripts/brief2.py`.
  Editing it moves `analytics_sha()` and triggers the I-F version bump plus INTERFACE sync. **Do not extend it.**
- At most, `va_nesting`'s interval-geometry states could label an L box against an L+1 box. Nothing else is
  reusable for R3.

---------------------------------------------------------------------------------------------------------------

## 7 · GAPS: WHAT THE EXISTING CODE CANNOT DO TODAY

- **G1. Lens set.** `tierc10_census.LENSES=("5m","4h","1d")`, `LENS_MS`, `LENS_SOURCE` and `TS_FMT` are hard-coded
  (:117-121).
  - `load_tape` HALTs on other lenses (:585-586).
  - `Tape.step` reads `LENS_MS` (:545), and `stamp()` reads `LENS_MS[lens]` (:1566) and KeyErrors.
  - `tierc10_stamps.LENS_MS = dict(C.LENS_MS)` (:118) and `asof_layer` (:668) use `C.load_tape`.
  - **15m, 1h, 12h and 1w need a TC11 loader.** The Tape subclass in section 9 is verified runnable.
    `asof_index`, `outcome_ledger`, `_r34_walk`, `acceptance_rows` and `edge_arrays` all read `tape.step`, so the
    subclass suffices. `stamp()` does not, so write your own warranty stamper.
- **G2. 15m data.** 15m files are **out of Stage D's scope**: `STAGE_D_MANIFEST.json:out_of_scope_snapshot_files`
  has no gap census, no as-of attestation and no prefix proof. 15m is absent for MNT, PUMP and SUI, which R1 does
  not require. 1h and 12h are native and in scope. 1w is **derived** from native 4h (seven complete days,
  MONDAY-anchored, `scripts/tierc10_data.py:973 derive_1w`, `MONDAY_EPOCH_OFFSET_MS = 4*DAY_MS` :198). The last
  closed 1w bar closes 2026-09-21T00:00Z. `STAGE_D_MANIFEST.as_of_last_closed_bar_per_lens` has
  5m/1h/4h/12h/1d/1w and no 15m.
- **G3. Nesting vector.** No code exists: no multi-lens as-of join, and no L→L+1 ladder
  (1h→4h→12h→1d→1w).
- **G4. Boundary coincidence** (0.25 ATR_L) has no code. **Signed distance** also has none: `dist_atr` is unsigned
  and `near_side` is separate.
- **G5. No 12h (or 1h/1d/1w) Stage-A stamps.** R5 needs the 4h and 12h state at entry. The only stamped book is
  `rf4h_*`.
- **G6. No maker toll object.** There is only taker at 5 bps/side (`tierc2_rules.FEE_BPS_SIDE` :122, `FEE_BPS_ROUND_TRIP`
  10), plus fee_schedule `round_trip_bps_used` 10 and the haircut twin. The one precedent is
  `scripts/v3_recompute.py:965`, "maker entries 2 bps/side, taker stops 5 bps/side". Every toll function takes
  `bps` as an argument, so a maker lens-level twin only needs a bps. The scalper's mixed per-trade toll (maker
  entry and target, taker stop) needs new accounting.
- **G7. No retest-hold pins for 1h, 4h or 12h.** `C.RETEST_PINS` is the 5m tuning (margin 1.0, hold 3, ttl 400)
  and is applied to every lens. 1d has its own tuning (ribbon89_127 / 0.25 / 6). P-BRK-4H's "89 tap" on 4h has no
  tuned or ruled pin.
- **G8. "First retest that HOLDS".** Both detectors are one-shot: `retest_holds` :983 and the leash's one flip
  evaluation per line. A failed first touch ends candidacy. A "scan for the first holding retest" detector does
  not exist.
- **G9. Substrate and as-of pin.**
  - `import tierc10_census` calls `assert_substrate()` at import (:72-96), which HALTs unless
    `NAIAD_CACHE_DIR == ~/.cache/naiad/snapshots/tc10_20260921`.
  - `load_tape` and `as_of_close_ms` read TC10's `AS_OF_PIN.json` (2026-09-21T16:00Z). `toll_bps_for` reads TC10's
    fee_schedule.
  - A TC11 corridor at "latest closed 4h bar" cannot use the loader. Either set the env to the TC10 snapshot for
    the import and load new-corridor bars by explicit path, or vendor the pure functions with an F-EQ fixture.
- **G10. Stale cell receipts.** `cell_is_current` (:1688) compares `code_sha` (now `5c63aadd…`) to the receipts'
  `629d2863…`. `run_cell` would recompute and `merge()` HALTs "code sha moved". **Never point a TC11 run at
  `research_outputs/tierc10/census`.** Use a tierc11 root. The filed tables are fine to READ.
- **G11. The sample floor at coarse lenses.** The floor is 30 confirmed ranges within the era. At 1w each asset
  has about 2–5 ranges in total, and at 12h about 18–40. The 1d single-asset rows were 17/17 provisional in TC10.
  So per-asset R2 at 12h/1d/1w FAILs or goes provisional by construction, and only pools can clear it.
- **G12. Calibrated scale and causality.** `calibrate()` fits on the whole tape, holdout included. LEAN L2 forbade
  registered lanes and stamps from reading it. TC11 R1 mandates the calibrated scale. Prefix-stability (F-NEST-ASOF)
  holds only for a fixed scale.
- **G13. Firewall.** `tierc10_stamps.FORBIDDEN_IN_DECISION = ("tierc10_stamps","tierc10_census","rangefinder")`
  (:253), with DECISION_MODULES at :257, F-STAMP-CLOSURE and F-BR-14. The range-conditioned TC11 decisions
  (P-BRK-4H, P-SCALP-2, P-ADD-*, P-TP-RNG) must take range facts as plain-number ARGUMENTS through a
  function-local-import adapter. The template is `tierc10_brk.macro_signals` (:2332). Note that its `flips`
  carry the touch bar `i`, so the caller must add HOLD.
- **G14. No filed tolls for new lenses.** `C.get_toll` (:1895) reads only the filed 5m/4h/1d grid and HALTs
  otherwise. For 15m/1h/12h/1w, compute `toll_atr = bps/1e4 * c/atr` (`_toll_at` :2504).
- **G15. Null for new lenses.** `tierc10_null.py` covers 5m/4h/1d at frozen3.0 only. R4's "null (gaps+order)" at
  1h/12h needs new cells.

---------------------------------------------------------------------------------------------------------------

## 8 · AMBIGUITIES IN THE TC11 CONTRACT (quoted)

- **A1. "pins = TC10 sha".** Which sha? Candidates: the four STEP 0 sources (port `19c5507f`, engine `bbae464f`,
  pine `4bed1e01`, twin `168d6229`), the census code_sha (`629d2863` cells vs `5c63aadd` now), or the RETEST grid
  sha `2135ca66`. REGISTRY_PIN.json holds none of them. The section 3 reading is proposed.
- **A2. "Macro scale self-calibrated per asset per lens to 0.75 confirmed ranges/100 bars".** This conflicts with
  TC10 LEAN L2 (frozen 3.0 for every registered lane and stamp; the calibrated scale is in-sample). Which scale
  feeds R3/R4/R5, P-BRK-4H, the scalp, the adds and P-TP-RNG? Should calibration use the tuning era only (the
  R1-tuning precedent `era_cut` :1033) or the whole tape?
- **A3. "PASS/FAIL printed per lens".** TC10 filed 120 rows per era (asset × pool × scale). Which row decides a
  lens (POOLED:ALL? CLASSIC5? holdout? calibrated?), and does a per-asset count play any part?
- **A4. "a FAIL closes that lens … in this and every later tier unless the toll model changes".** Do TC10's
  existing FAILs already close 5m (all pools and eras), 4h (pooled, except CLASSIC5 frozen holdout +0.006) and 1d
  (holdout)? Is R2 re-run on the TC11 corridor or read from TC10?
- **A5. "signed distance to nearest boundary (ATR of L)".** No sign convention is given (inside +/outside −? toward
  the top +?).
- **A6. "BOUNDARY COINCIDENCE (a boundary of L within 0.25 ATR_L of a boundary of L+1)".** Open points:
  - Does it count only a live CONFIRMED L+1 range, or also L+1 memory lines of a dead range?
  - Is it any of the 4 pairings or same-side only?
  - Is ATR_L taken at L's as-of bar?
  - For L=1w, L+1 is undefined, but 1w is in R3's lens set.
- **A7. "L+1 in-range mid" vs "L+1 in-range at its own boundary (coincidence)".** "Mid" is not defined (a pct band?
  "not coincident"?). "Expansion aligned" = not in range and state == trade direction? The latch can be months
  stale.
- **A8. "first retest that HOLDS".** Is it the one-shot first touch (TC10 law), or scan until a touch holds? (G8)
- **A9. "SWING-FAILURE = deviation confirmed at a CONFIRMED boundary (spring/upthrust)".** Is it the machine
  `harden` event (known at the back-inside close, ≤7 bars), or the house 20-bar sweep-reclaim spring? Are
  inception deviations at confirm included?
- **A10. "%-of-range decile" (R5).** `pct` is unclamped (<0 or >100 on breach bars while the range is alive), and
  BULL_EXP/BEAR_EXP/NONE rows have no pct. How should they be binned? (`edge_arrays` uses `min(int(pct*10),9)`
  on in-box bars only.)
- **A11. "Corridor: full water, latest closed 4h bar, one as-of pin".** Is it a new snapshot and pin (G9), or the
  TC10 pin of 2026-09-21T16:00Z?
- **A12. Scalper "price in the lower (upper) third" of the 1h range.** Is it `pct < 33.3` on the as-of box, and
  are deviation zones included? The "1h boundary breach" invalidation is a breach-open close (known at i) or a
  wick through.
- **A13. "the edge-fade leg".** Is it TC10's statistic (near 20% of range, H20, net > 0, with a 30-range floor
  within the era), or a new definition?

---------------------------------------------------------------------------------------------------------------

## 9 · HOW TO CALL THIS FROM A NEW tierc11 SCRIPT

This was verified in scratch on the TC10 snapshot for BTC 1h/12h/1w/15m and ETH 1h. It assumes the TC10 snapshot
(G9).

```python
import os, sys
from pathlib import Path
import numpy as np, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "scripts"))
import tierc10_census as C          # HALTS unless NAIAD_CACHE_DIR == ~/.cache/naiad/snapshots/tc10_20260921
from analytics import rangefinder_census as RC
from engine import indicators as ind
from engine.data import cache_dir

LENS_MS11 = {"5m": 300_000, "15m": 900_000, "1h": 3_600_000, "4h": 14_400_000,
             "12h": 43_200_000, "1d": 86_400_000, "1w": 604_800_000}
LADDER = {"1h": "4h", "4h": "12h", "12h": "1d", "1d": "1w", "1w": None}   # L -> L+1

class Tape11(C.Tape):                       # same fields; only the bar length changes
    @property
    def step(self): return LENS_MS11[self.lens]

def load11(sym, lens, close_ms=None):
    """Closed bars <= AS_OF, full history, engine ATR on the WHOLE tape (never a tail).
    1d/1w files in the snapshot are Stage-D DERIVED from native 4h (1w Monday-anchored)."""
    close_ms = C.as_of_close_ms(sym)[0] if close_ms is None else close_ms
    f = (pd.read_parquet(cache_dir() / "klines" / f"{sym}_{lens}.parquet")
           .sort_values("open_time", kind="mergesort").reset_index(drop=True))
    f = f[f["open_time"] + LENS_MS11[lens] <= close_ms].reset_index(drop=True)
    t0 = f["open_time"].to_numpy(np.int64)
    assert (np.diff(t0) > 0).all()                       # load_tape's own HALT law (:615-619)
    o, h, l, c = (f[k].to_numpy(float) for k in ("open", "high", "low", "close"))
    ts = pd.to_datetime(t0, unit="ms", utc=True).strftime("%Y-%m-%dT%H:%M").tolist()
    return Tape11(sym, lens, o, h, l, c, t0, ts, ind.atr(h, l, c, RC.ATR_LEN),
                  {"asset": sym, "lens": lens, "n_bars": len(t0), "as_of_close_ms": close_ms})

tape = load11("BTCUSDT", "1h")
pick, sgrid = C.calibrate(tape)                 # whole 11-cell grid; in-sample (A2/G12)
v2   = C.run_scale(tape, pick)                  # or C.FROZEN_SCALE (3.0)
view = C.asof_view(tape, v2["macro"], v2["leash"])
evf, tally = C.census_events(tape, v2["macro"], v2["leash"], view)   # RETEST_PINS = 5m-tuned (G7)
bps, _ = C.toll_bps_for("BTCUSDT")
led  = C.outcome_ledger(tape, evf, view, bps)   # term/mfe/mae H20/H100 from known_at close

# [Q-R3] per lens (R2): walk -> height + edge -> verdict
w  = C._r34_walk(tape, v2["macro"], RC.macro_pins(pick))
hg = C.height_grid(C.height_rows(w, tape, "BTCUSDT", "1h", "calibrated", bps), "BTCUSDT", "1h")
A  = C.edge_arrays(tape, w, bps, aid=0)          # pool: C._edge_cat([A_asset...]), pooled=True
eg = {("BTCUSDT", "calibrated", e): C.edge_gate(A, False, e) for e in C.ERAS}
verdict = C.verdict_rows(hg, eg, "1h")          # verdict_pass per era

# NEST (R3) at campaign instants: instants = bar-CLOSE ms of the instant on its own lane lens
def lens_vec(tape, view, instant_close_ms):
    k = C.asof_index(tape, instant_close_ms)            # last CLOSED bar of this lens; -1 = none
    ok = k >= 0; ks = np.where(ok, k, 0)
    g = lambda a, fill: np.where(ok, a[ks], fill)
    inr = g(view["in_range"], False)
    return {"k": k, "in_range": inr, "state": g(view["state"], 0),
            "pct": np.where(inr, view["pct"][ks], np.nan),
            "dist_atr": np.where(inr, view["dist_atr"][ks], np.nan),    # UNSIGNED (A5)
            "near_side": g(view["near_side"], 0), "bnd_age": np.where(inr, view["bnd_age"][ks], -1),
            "dev_top": np.where(inr, view["dev_top"][ks], -1), "dev_bot": np.where(inr, view["dev_bot"][ks], -1),
            "flip_pol": g(view["flip_pol"], 0), "flip_age": g(view["flip_age"], -1),
            "top": np.where(inr, view["top"][ks], np.nan), "bot": np.where(inr, view["bot"][ks], np.nan),
            "atr": np.where(ok, tape.atr[ks], np.nan)}

def coincident(vL, vU, frac=0.25):                     # A6: live boxes only, any of 4 pairings
    thr = frac * vL["atr"]
    pairs = [(vL["top"], vU["top"]), (vL["top"], vU["bot"]), (vL["bot"], vU["top"]), (vL["bot"], vU["bot"])]
    with np.errstate(invalid="ignore"):
        return np.any([np.abs(a - b) <= thr for a, b in pairs], axis=0)   # NaN -> False
```

**Rules the executor must keep:**
1. Never read `Range.top/.bottom/.n_deviations`, and never read an event price, at bar t. Use `view`.
2. Anchor outcomes at `known_at`: flip at touch+6, retest at touch+hold, pivot at its seal.
3. Coarse lenses are read through `asof_index` only, which gives closed bars. A forming 4h/12h/1d/1w bar is never
   read.
4. Write to a tierc11 root, never to `research_outputs/tierc10/census`.
5. The v6 decision closure must not import any of this. Hand plain numbers in (G13).
6. To build F-NEST-ASOF, copy the pattern at tierc10_census_fixtures.py:241-433 (`_law_views` plus
   `asof_corpus`), cutting every lens at one instant.
