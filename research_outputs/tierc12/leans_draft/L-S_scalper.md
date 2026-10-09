## L-S · SCALPER FAMILY — P-SCALP-3, THE 1h VALUE-AREA RANGE TRADE, MAKER, ON THE 5m CLOCK

This section governs Stage S of the contract (lines 82-106) and the two fixtures the contract names for it: F-SCALP
(:119-121) and the BOOK half of F-TOLL (:121). Nothing like this walk exists on disk — no 5m EMA trigger, no order
resting at a price away from a close, no tick-based fill, no validity window longer than one lens bar, no MISS table,
no target / stop / time-stop walk on the 5m clock (scout U6 §1.1, §1.3, §1.7). The readings below are therefore the
specification of a NEW simulator, clause by clause: the row a 5m close may read; PERMISSION, SETUP and the two
TRIGGERS; the order (a limit on the tick grid, geometry frozen at the trigger, validity, cancellation, one order and
one position per asset); the three fill rules in integer ticks and the three books they make; the walk after the fill
(same-bar order, invalidation, time stop); the costs of record and the twins on every row; the MISS table; the regime
columns; the population, the scored window and the Tier-E views; the precondition; the pre-named kill as an
exhaustive table; the outputs, F-SCALP, F-TOLL and the compute plan. It owns ONE registered row, P-SCALP-3.

**Drafting record.** Read while drafting, all read-only: the contract (sha256 `861d6050…a7bd`); ORCHESTRATOR RULINGS
(`c280a972…f509`); DISCLOSURES (`bd6987a2…1958`); scout maps U6 (`8315e351…bc4e`), U4 (`f700f842…1342`), U2
(`50109e8b…3aef`); the sibling drafts L-0 (`2c6e9ba5…2a73`), L-D (`9ed43441…79af`), L-V (`5d653d6f…ee1a`) and L-X
(`6d1b5055…c263`) as they stood (their reading ids are cited; where they move, the owning section governs). Sources
opened as TEXT: `engine/indicators.py`, `scripts/tierc10_brk.py`, `tierc5_rules.py`, `tierc2_rules.py`,
`tierc3_rules.py`, `tierc4_rules.py`, `tierc7.py`, `tierc9.py`, `tierc10_census.py`, `tierc10_panel.py`,
`tierc11_ride.py`, `tierc11_score.py`, `tierc11_env.py`; X's `x_rec/scripts/tc11x_sfp.py` and `tc11x_pct.py`; X's
`LEANS_X.md` (LX-1.1, LX-X2.4 … X2.12, LX-X3.14, :2462-2470); TC11's `LEANS.md` (L-1.1 … L-1.4, L-S.1, L-S.2) and
`LEANS_AMENDMENTS.md` (AM-7). Inspections, structural only: the keys of `PINS_X.json`; the `constants` block of X's
`exit/build_manifest.json` and the `laws` and `geometry` blocks of X's `sfp/build_manifest.json` (the latter holds
entry-time geometry quantiles and refusal counts of X2's pivot book — no net R); the two 1h holdout rows of X's
`va/feasibility.parquet` (the licence row and its taker sibling, both already printed in DISCLOSURES D-2 and scout U2
§1.8); the five home ticks and one fee row of TC11's Stage D records. No `tc11x_*`, `tierc10_*` or `tierc11_*`
module was imported or run. NO outcome of any TC12 book was computed, and no count of orders, fills or trades.
Counts quoted from scout maps are orientation the build re-reads, never inputs.

**Notation.** One asset, one book. `d` = +1 long, −1 short. 5m tape: bars `j` with `open5[j]`, `o,h,l,c,v`,
`close5[j] = open5[j] + STEP5`, `STEP5 = E.LENS_MS["5m"]`. `t` = the trigger bar, `τ = close5[t]` = the decision
instant. `G` = the frozen geometry of the order: `(VAL, POC, VAH, ATR)` read once at τ (L-S.3). `EDGE` = the edge of
interest (VAL for a long, VAH for a short); `FAR` = the other edge. `TICK` = the tick of record; `n_X` = a price in
integer ticks; `px(n)` = that grid price (`TickGrid`, L-D.23). `L` = the limit price; `S` = the stop; `R = |L − S|`.
`V` = the validity in 5m bars; `T5` = the time stop in 5m bars; `Q` = the fraction sold at T1. `f` = the fill bar;
`x` = the exit bar. `W` = the score edge `E.TC11_PIN_MS` (O-9); `PIN = E.PIN_MS`; `ERA_CUT = E.ERA_CUT_MS`. `hi` =
the last 5m bar a walk may read. A BUY limit rests below the market (a long's entry, a short's targets); a SELL
limit rests above it (a short's entry, a long's targets). Formulas are written for a long; "mirrored" means `d`
flipped, VAL↔VAH, low↔high, floor↔ceil, `≤`↔`≥`. Where the mirror is not mechanical it is written out.

---------------------------------------------------------------------------------------------------------------
### A · The stage, its inputs, its pins

**L-S.1 WHAT STAGE S BUILDS, AND FROM WHAT** — "STAGE S · SCALPER FAMILY (m=1, bar 0.10) — exists by the "maker"
ruling:" (contract :82); "P-SCALP-3 [30%] THE 1h VALUE-AREA RANGE TRADE, MAKER, ON THE 5m CLOCK" (:83)
READING:
- **Modules.** Builder `scripts/tierc12_scalp.py`; suite `scripts/tierc12_scalp_fixtures.py`; records under
  `research_outputs/tierc12/stage_s/` and `research_outputs/tierc12/regbooks/P-SCALP-3/`; progress record
  `progress/TC12-S.json`; commit subject `tierc12(TC12-S): …`. The stage starts only after TC12-V and TC12-C are
  COMPLETE-VERIFIED (L-0.10) and after L-G's per-bar tide and breadth table is filed (L-S.24; INTERFACE).
- **The builder is an event simulator on each asset's 5m tape.** It reads value-area facts ONLY AS FILED DATA
  (L-0.22: "value-area state enters decision code only as DATA"): it imports neither `analytics.value_area` nor the
  door `scripts/tierc12_va.py`, computes no profile, runs no state machine, and holds no name or attribute
  `value_area` / `volume_profile`. No 5m value area, range, pivot or tide exists (contract :89 "the 5m is never a
  signal source"; L-V.7 "5m is not a VA lens").
- **Read set, per asset** (every path through the env `E`, L-D.25-28; anything else opened is a finding):
  1. the 5m frame `E.BK.frame_l(stem, "5m")` (`open_ms, o, h, l, c`, the funding arrays; built once per process on
     the tape cut at PIN), and the `volume` column of the same file from `E.load_asof_at(stem, "5m", E.PIN_MS)`,
     asserted row-for-row aligned (`open_time == lf.open_ms`) before use;
  2. Stage V's filed tables through the data-only reader `scripts/tierc12_va_stamps.py` (L-V.2): `bars("1h")`,
     `bars("4h")`, `events()` (rows `lens == "1h"`, `kind == "acceptance"`), `licence("1h", "maker", "holdout")`;
  3. the traverse through the fitted-pin door: `va/TRAVERSE.json` key `by_lens.1h.T_in_5m_bars` (L-V.18);
  4. `E.fees()[stem]` and `E.ticks()[stem]` (L-D.19, L-D.22); the contract pins through `scripts/tierc12_pins.py`;
  5. L-G's filed per-4h-bar tide and breadth table (regime columns only, L-S.24).
  The builder opens NO 1h or 4h kline file: `ATR_1h` is the filed column `atr` of `va_bars_1h` (L-V.24: "THE FILED
  VALUE IS THE VALUE OF RECORD").
- **The value-area columns the registered construction reads — the complete typed list** (for L-V's F-VA-PINS (e)
  and L-0's F-NOT): from `va_bars_1h`: `close_ms`, `state`, `val`, `poc`, `vah`, `atr`, `va_age`; from `va_bars_4h`:
  `close_ms`, `state`; from `va_events`: `lens`, `kind`, `side`, `known_close_ms`, `by`, `bars_out`, `E`. No 12h, 1d
  or 1w column is read by the registered construction (the 12h / 1d / 1w members reach the scalper only as the
  captured V5 stamps of L-S.30).
- **Two walks on one tape** (L-D.28: "A look-back is an INDEX BOUND on that tape"): WALK-W with `hi = hi_W` = the
  last 5m bar with `close5 ≤ W` makes every scored, ladder and Tier-E arm; WALK-PIN with `hi = hi_PIN` = the last
  bar with `close5 ≤ PIN` makes the strip (L-S.25). Each walk covers the asset's whole corridor up to its bound in
  ONE pass (one-order / one-position state is carried across the era cut).
- **Order of acts:** (1) the precondition gate (L-S.27) — if not met, `regbooks/P-SCALP-3/STATUS.json` only and
  stop; (2) the gates and geometry of every candidate (L-S.3 … L-S.12), fill-rule independent; (3) the walks.
SOURCE: contract :82-83, :89; L-0.10, L-0.22, L-0.30 (5m SIGNAL SOURCE; `FIVE_MIN_READERS_T`), L-D.28, L-V.2,
L-V.24; `scripts/tierc10_brk.py:851-954` (`LensFrame`, `frame_l`: lens-generic, accepts "5m" — `LENS_MS =
dict(D.STEP_MS)` :137); scout U6 §1.0, §1.1.
RIVALS: a RUNNER that asks the door for arrays (L-0.22's other form) — not taken: every fact this trade needs is a
filed column. `ATR_1h` recomputed from the 1h klines at full float — two values of record for one quantity (L-V.24).
X's `tc11x_sfp.walk` vendored — its clock is the trade's own lens bar and its entry is a close; it cannot rest an
order (scout U6 §1.1).
FAILS-IF: L-0's F-CLOSURE (a scalper copy importing `analytics.value_area` or the door → RED) and F-NOT leg 5m (a
third `ema` site → RED; a 5m file opened outside `FIVE_MIN_READERS_T` → RED); here F-SCALP (g) READ-SET: the hook's
open log of a build holds a path outside the read set above; planted mutation: a 1h kline read planted in a shadow
builder.

**L-S.2 THE PINS THIS SECTION CONSUMES** — "no number typed that a file can supply" (contract :8)
READING: every constant below is read at run time from the named source; where the contract's value also stands on
file the two are asserted equal by the pin door or by the builder's header check (a HALT). "Value" is orientation.

| pin | read at run time from | asserted equal to | value | flow witness when bent at its door |
|---|---|---|---|---|
| `scalp.third_long_max`, `scalp.third_short_min` | contract :87 (pin door); `also` :136 `"outer-third" (33/67)` | — (no file states this pair) | 33, 67 | the SETUP mask of a seeded bar set |
| `scalp.ema_fast`, `scalp.ema_slow` | contract :89 "EMA12/EMA89" | `tierc2_rules.WINDOW_FAST`, `WINDOW_SLOW` (:115-116) | 12, 89 | the cross bars of a seeded tape |
| `scalp.trigger_prox_atr` | contract :90 "within 0.25 ATR_1h" | — | 0.25 | the proximity mask |
| `scalp.validity_bars` (V) | contract :92; `also` :136 `"validity" (12 five-minute bars)` | — (NOT the lens ratio; see below) | 12 | the expiry bar of a seeded order |
| `scalp.fill_ticks` (`n_tick`) | contract :94 "by ≥ 1 tick"; `also` :136 `"fill" (through by 1 tick)` | — | 1 | the fill bar of a seeded order (collides with the structural set: held by the FLOW leg alone, L-0.17) |
| `scalp.deep_atr` | contract :94-95 "DEEP (through by 0.05 ATR_1h)" | — | 0.05 | `n_D` of a seeded order |
| `scalp.stop_beyond_atr` | the lineage object `STOP_BUF_ATR` inside `E.BK.brk_stop` (`tierc2_rules.py:127`) | contract :97 "0.5 ATR_1h beyond"; X's `sfp/build_manifest.json` `laws.stop_buf_atr` | 0.5 | the stop of a seeded swing-failure order |
| `scalp.rail_atr` | contract :98 "railed ≥ 1.0 ATR_1h", passed as `rail_atr=` | `tierc3_rules.MIN_STOP_ATR` (:148); X's `laws.rail_atr` | 1.0 | every cross order's stop (collides with the structural set: FLOW leg) |
| `scalp.t1_fraction` (Q) | the lineage object `E.TP.CONTROL_CARD.harvest_frac` (read inside `BK.account_l`) | contract :99 "half" (pin door `word_map`); `tierc4_rules.HARVEST_FRACTION` (:202); X's `laws.harvest_frac` | 1/2 | `net_r` of a seeded T1-then-stop trade |
| `scalp.t2_offset_atr` | contract :99 "far edge − 0.25 ATR_1h" | X's `laws.t2_atr_off` | 0.25 | `n_T2` of a seeded order |
| `scalp.rr_min` | contract :100; `also` :135-136 `"rr-min" (1.5 at T2)` | the same pin L-R reads for :73-74 | 1.5 | the skipped set |
| `scalp.era` | contract :83 "HOLDOUT era"; `also` :137 `"era" (scalper scored on holdout)` | sidecar `era_scope` | holdout | the scored arm's row set |
| `T5` | `va/TRAVERSE.json` `by_lens.1h.T_in_5m_bars`, fitted-pin door (L-V.18) | `T_of_record × (E.LENS_MS["1h"] // E.LENS_MS["5m"])` | fitted at TC12-V | the bar of a time-stop exit |
| maker / taker / charter bps | `E.fees()[stem]` keys `maker_bps_side`, `taker_bps_side`, `slippage_bps_side` (L-D.19, L-D.26 hunk 4) | taker == `tierc2_rules.FEE_BPS_SIDE` (post-shim P4) | per Stage D | `net_r` of a seeded sample (F-TOLL) |
| tick | `E.ticks()[stem]` (a string; L-D.22) | `data/CONTRACT_SPECS.json` `assets[].price_tick` | per asset | the limit of a seeded order |
| trailing window, floor (regime column) | X's `exit/build_manifest.json` `constants.vol_window`, `constants.vol_floor` through `E.x_rec` (sha `6f57e78e…3bc6`) | the AST literals `WINDOW`, `FLOOR` of `x_rec/scripts/tc11x_pct.py` | 2000, 300 | the tercile of a seeded bar |
| R tolerance | `HAIRCUT_TOL`, read by `ast` from `scripts/tierc11_score.py:264` (L-X.24's object) | — | 1e-12 | — |
| `PCT_PER_UNIT`, `BPS_PER_UNIT` | `scripts/tierc12_units.py` (L-0.17) | — | 100, 10000 | — |

`scalp.validity_bars` (a contract pin, vetoable as "validity") and the lens ratio `E.LENS_MS["1h"] //
E.LENS_MS["5m"]` (an object, inside `T5`) are two different quantities that share a value today; neither is read
where the other belongs, and F-SCALP (n) bends each separately.
SOURCE: contract lines as cited; L-0.17 (the doors, the allow-list, "THE LIMIT", the FLOW leg), L-0.23 (the veto
tokens); the lineage objects at the lines cited [read here]; X's two manifests (`constants`, `laws` keys) [read
here]; L-V.18; L-D.19, L-D.22.
RIVALS: read 0.5 / 1.0 / half from the contract and pass them into a re-implemented stop — not taken: the estate's
stop function is called as it is and the contract values are asserted equal to what it reads. Type the window and
floor of the trailing rank — forbidden.
FAILS-IF: F-SCALP (n) FLOW: each pin above, bent at its door inside production, must move its witness on a seeded
sample, else `PIN-NOT-READ`; planted mutation: a shadow builder holding a literal of equal value in place of
`scalp.validity_bars` (the bend moves nothing → RED). L-0's F-TYPED and F-PINS hold the rest.

---------------------------------------------------------------------------------------------------------------
### B · The decision at a 5m close

**L-S.3 THE ROW A 5m CLOSE READS** — "at the last 1h close" (contract :85); ruling O-14
READING: a decision is taken only AT a 5m close τ. Per asset the builder holds the arrays of `bars("1h")` and
`bars("4h")` sorted by `close_ms` and computes, for every 5m bar,
`k1 = asof_index(close_ms_1h, τ)` and `k4 = asof_index(close_ms_4h, τ)` with the ONE implementation
`tierc12_asof.asof_index` (L-0.28: `searchsorted(closes, τ, side="right") − 1`): the last lens bar whose CLOSE ≤ τ.
A 1h (4h) bar closing exactly at τ IS that row; a bar still forming is never read.
- **Everything the decision uses about the 1h lens is row `k1` of `va_bars_1h`, as filed:** `state` (the machine
  after bar `k1`), and the profile IN FORCE at τ — `val, poc, vah` = `VA(k1)` — with `atr = ATR_1h[k1]` (L-V.20).
  Those four numbers are the order's frozen geometry `G`. From the 4h lens only `state` at row `k4` is read.
- **Freshness.** `0 ≤ τ − close_ms_1h[k1] < E.LENS_MS["1h"]` and `0 ≤ τ − close_ms_4h[k4] < E.LENS_MS["4h"]` are
  required (no missing lens bar between the row and τ); otherwise no decision is taken at τ and the bar is counted
  (`stale_1h`, `stale_4h`). `k1 = −1` or `k4 = −1` is UNDEFINED and takes no decision.
- **When τ is itself a 1h close** (one 5m close in `E.LENS_MS["1h"] // E.LENS_MS["5m"]`): the same law — `k1` is
  the hour that has just closed. Its `state` was judged by the machine against `VA(k1 − 1)` (L-V.8 rule 2), while
  the trigger price is measured against `VA(k1)`, whose window contains that hour. Both are known at τ; the order
  then rests on the profile that will judge the NEXT 1h close. Such triggers carry `on_1h_close = True`, their
  count is printed, and the book of record split by that flag is a Tier-E slice (L-S.26).
- The order's row is held equal to the reader's own join: at every order's τ, `stamp()` of L-V.20 must return the
  same `1h_*` and `4h_*` values (F-SCALP (e1)).
SOURCE: O-14; L-0.28; L-V.8 rules 1, 4, 5 ("A level that rests during bar t+1 … may use VA(t) and ATR[t] and
nothing later"), L-V.20 ("The live formulas … the price against the IN-FORCE profile VA(k) and ATR[k]"; "what a
consumer does at such instants is its own reading"); `scripts/tierc10_census.py:894-900`; scout U6 §1.10.
RIVALS: (a) the engine's exec-OPEN law (`engine/htf.py`: lens close ≤ the 5m bar's OPEN) — not taken: it hides the
hour-close bar the contract's "at the last 1h close" names. (b) judging profile `VA(k1 − 1)` for the price at an
hour close and `VA(k1)` for the order — two profiles for one order, and a limit that can be marketable against the
price that triggered it. (c) no trigger on an hour-close bar — an exclusion the contract does not state.
FAILS-IF: F-SCALP (e1) BOUNDARY: a seeded trigger exactly on a 1h close must read the row of the bar closing at τ,
and one 5m bar earlier the previous row; planted mutations inside production: `side="left"`; the row taken at
`k1 + 1` (the forming hour).

**L-S.4 PERMISSION** — "PERMISSION: 1h state INSIDE (no probe/acceptance at the last 1h close) AND the 4h state NOT
accepted against the planned direction." (contract :85-86)
READING: at τ, for planned direction `d`:
`PERM(d) = (state_1h[k1] == "INSIDE") AND (state_4h[k4] ∉ {"UNDEFINED", AGAINST(d)})`, with
`AGAINST(+1) = "ACCEPTED_BELOW"`, `AGAINST(−1) = "ACCEPTED_ABOVE"` — P-DIR-1's own parenthesis, "accepted below
for a long; above for a short" (contract :66). State names are L-V.2's `STATE_NAMES`; the filed `state` is read,
never re-derived from levels (L-V.24).
- 1h PROBING or ACCEPTED on EITHER side, or UNDEFINED, denies permission in both directions.
- 4h PROBING (either side), 4h INSIDE and 4h ACCEPTED WITH the direction permit. 4h UNDEFINED denies (it cannot
  occur in the holdout on a home asset; it is counted in the full-corridor and 17-asset views).
- **Evaluated ONCE, at the trigger close.** It is not re-evaluated while the order rests or at the fill. The
  contract names exactly one way a resting order dies before expiry — "cancelled on acceptance beyond the edge"
  (:92-93, L-S.13) — and a permission-lapse cancel would be a second, unnamed one. What the rival would do is
  printed, deciding nothing: per order `perm_1h_at_resolution`, `perm_4h_at_resolution` (PERM re-read at the last
  lens close at or before the open of the fill bar, or of the expiry bar for an unfilled order) and their counts.
- PERMISSION is a pure function of (τ, d, the two filed tables): F-NOT's 5m leg (d) recomputes it in a process
  that opens no 5m file.
SOURCE: contract :66, :85-86; L-V.13 (the state column; its three counted consequences), L-V.20; L-0.30 leg 5m (d).
RIVALS: "INSIDE" re-derived as `val ≤ c ≤ vah` — loses PROBING versus resolved and flips at 6-dp edges (L-V.24).
4h "not accepted against" read as "4h INSIDE" — stricter than the text. Re-check at the fill — see above.
FAILS-IF: F-SCALP (g) GATES: the fixture's own recomputation of PERM for every order and every refused trigger,
from the two filed tables alone, differs on any row; planted mutations: the 4h clause dropped; `AGAINST` swapped
between the directions; the 1h state read at `k1 − 1`.

**L-S.5 SETUP** — "SETUP: price in the outer third of 1h value (%-of-value ≤ 33 for a long, ≥ 67 for a short)
["outer-third"]; edge of interest VAL (long) / VAH (short)." (contract :87-88)
READING: "price" = the trigger bar's close `c5[t]`. "%-of-value" = L-V.20's live formula against the in-force
profile: `px_pct = PCT_PER_UNIT · (c5[t] − VAL) / (VAH − VAL)`, float64, in that operation order; undefined (no
setup) unless `VAH > VAL` and all three are finite.
- LONG setup iff `0 ≤ px_pct ≤ third_long_max`; `EDGE = VAL`, `FAR = VAH`.
- SHORT setup iff `third_short_min ≤ px_pct ≤ PCT_PER_UNIT`; `EDGE = VAH`, `FAR = VAL`.
- The bounds 0 and `PCT_PER_UNIT` are the reading of "IN the outer third OF 1h value": a close beyond the edge is
  outside value and is not in any third of it. The two inner cuts are inclusive, as the contract writes them
  (`≤ 33`, `≥ 67`). At most one direction can hold at a bar.
- Printed per asset and direction: the counts on each cut exactly (`px_pct == third_long_max`, `== 0`, and the
  mirrors).
SOURCE: contract :87-88, :136; L-V.16 (`pct`, unclipped), L-V.20; TC11 `LEANS.md:452` (L-S.2's lower third,
`0 ≤ pct < 33.33` — the precedent for a floor at the edge; its cut values are NOT these).
RIVALS: no lower bound (`px_pct ≤ 33` alone admits closes below value, where a limit AT the edge is marketable).
The lens's own judged `pct` column (the last 1h close against `VA(k1 − 1)`) — up to an hour stale against a price
the contract takes on the 5m clock. Thirds at 33.33 / 66.67 — the contract types 33 / 67.
FAILS-IF: F-SCALP (g): `px_pct` and the setup flag recomputed in `fractions.Fraction` from the filed row and the raw
5m close differ from production's decision on any candidate (a float / rational disagreement is `FLOAT-BOUNDARY`,
RED); planted mutations: the lower bound removed; `px_pct` computed against `VA(k1 − 1)` (`val_j`, `vah_j`).

**L-S.6 TRIGGER (a): THE 5m EMA CROSS NEAR THE EDGE** — "TRIGGER (5m, timing only — the 5m is never a signal
source): a 5m EMA12/EMA89 cross in the planned direction while price is within 0.25 ATR_1h of the edge" (contract
:89-90)
READING:
- `e_f = ind.ema(c5, ema_fast)`, `e_s = ind.ema(c5, ema_slow)` — the engine's function, on the asset's WHOLE 5m
  tape from its first bar (recursive, `alpha = 2/(len + 1)`, seeded with the first close: no SMA seed, never NaN),
  so a value at bar `j` depends on bars ≤ `j` only and is the same on any longer tape. These are the builder's ONLY
  two `ema` call sites, and no period is a literal (L-0.30).
- `up = ind.crossover(e_f, e_s)`: `e_f[j] > e_s[j]` AND `e_f[j−1] ≤ e_s[j−1]`; `dn = ind.crossunder(e_f, e_s)`:
  `e_f[j] < e_s[j]` AND `e_f[j−1] ≥ e_s[j−1]`. "In the planned direction": `up` for a long, `dn` for a short.
- **Warm-up** (the lineage's law, `tierc10_brk.py:1050-1078`: "an EMA of period p is READABLE from bar p and not
  before"): a cross at tape index `j < ema_slow` is not a trigger. The floor cannot bind in the holdout on a home
  asset; the builder asserts it and prints the first readable instant per asset.
- **The cross must print ON bar t.** A cross at an earlier bar of the hour is not a trigger at t.
- **Proximity:** `0 ≤ d·(c5[t] − EDGE) ≤ trigger_prox_atr · ATR` with `ATR = ATR_1h[k1]`, float64 in that order.
  The lower bound is SETUP's (the close is on the value side of the edge).
- `TRIG_A(d, t) = PERM(d) AND SETUP(d) AND cross(d)[t] AND proximity AND t ≥ ema_slow`.
- **Counted, never ordered:** a cross in the direction of the nearer edge with PERM true whose close is BEYOND
  that edge by at most `trigger_prox_atr · ATR` (`−prox·ATR ≤ d·(c5[t] − EDGE) < 0`) — the contract's "within
  0.25 ATR_1h" read two-sidedly — is `cross_beyond_edge_no_order`: a limit AT the edge would be marketable there
  (L-S.9), so no order exists.
SOURCE: contract :89-90; `engine/indicators.py:17-28` (`ema`), :66-78 (`crossover`, `crossunder`) [read here];
`scripts/tierc11_ride.py:415-423` (`cross_1h`, `warn_of(walk, fast=12, slow=89)` — the same pair, the same
functions, at 1h); `tierc2_rules.py:115-116`; scout U6 R-5, R-9.
RIVALS: an SMA-seeded or windowed EMA — a tail-loaded tape re-seeds it and moves every cross. "A cross within the
last n bars" — a new constant. Two-sided proximity with an order placed — a marketable limit booked at the maker
rate (scout U6 H6). ATR of the 5m tape — the contract says ATR_1h.
FAILS-IF: F-SCALP (g): the fixture's own EMA loop from the tape's first bar and its own cross test differ from
production's trigger bars; (e2) PREFIX: the EMA and trigger set from a fresh tape cut at a seeded 4h close differ
from the full tape's at bars ≤ the cut. Planted mutations: the EMA computed on a tape that starts at the era cut;
`crossover` without the prior-bar clause; the proximity taken with the absolute value.

**L-S.7 TRIGGER (b): THE 5m CLOSE BACK INSIDE** — "OR a 5m close back inside the 1h value after a 5m close beyond
the edge." (contract :90-91)
READING: one profile judges the whole pattern — `G` of bar t (L-S.3) — and the pattern is read on 5m CLOSES only.
- LONG: `TRIG_B(+1, t)` iff `PERM(+1)` AND `SETUP(+1)` (so `VAL ≤ c5[t]`, "back inside", closed interval) AND
  `c5[t−1] < VAL` (the immediately preceding 5m close is beyond the edge, strictly) AND bars `t−1`, `t` are adjacent
  on the 5m grid (`open5[t] − open5[t−1] == STEP5`). SHORT: `c5[t−1] > VAH` and `c5[t] ≤ VAH` with `SETUP(−1)`.
- **How many closes beyond are allowed: any number ≥ 1.** The trigger reads bars `t−1` and `t` only; no K is
  introduced. "sfp-k" (:36, :135) is the lens machine's pin and is not carried to the 5m clock, where the contract
  wants timing and "never a signal source". The run is bounded by the contract's own filters, not by a count: a
  long excursion deepens the deviation extreme, hence the stop (L-S.10), hence fails "rr-min" (L-S.12).
- **The deviation run and its extreme.** `s` = the smallest index such that bars `s … t` are pairwise adjacent
  and `c5[j] < VAL` for every `j ∈ [s, t−1]` (the maximal run of consecutive closes beyond that ends at `t−1`).
  `EXT = min(l5[s … t])` — every low since the first close beyond, THE RETURN BAR INCLUDED (L-V.11's law for the
  lens machine: "inclusive of both t0 and the return bar"). SHORT: `EXT = max(h5[s … t])`.
- Filed per order: `run_start_i`, `n_run = t − s`, `ext_px`, and `run_predates_profile` (the run holds a 5m bar
  whose close ≤ `close_ms_1h[k1]`, i.e. it began before `G` took force — always true when τ is a 1h close).
  Printed: the whole occupancy table of `n_run`, and the count of `run_predates_profile`. A run cut by a missing
  5m bar is counted (`run_cut_at_gap`).
- The 1h lens need not have printed anything: with PERM true the hour is INSIDE. This is the 5m excursion the 1h
  close never showed, used to TIME an order at an edge the 1h value area supplies.
SOURCE: contract :90-91, :36, :89, :135; L-V.9 (closed interval inside; strict beyond), L-V.11; scout U6 R-10;
Stage D's manifest (`gap_count 0` on all home 5m tapes at TC11's pin, scout U4 §1.2).
RIVALS: (a) K = 3 on the 5m clock — imports the lens machine's pin where the contract names none, and turns the 5m
into a state machine. (b) each 5m close judged against the profile in force during its own bar, the edge frozen at
the run's first close (the lens machine's law) — then a run that crosses a 1h close carries two profiles, and the
limit "AT the edge" has two candidate edges. (c) a wick beyond with a close inside on one bar — the contract says
"a 5m close beyond". (d) the extreme without the return bar — the return bar's low can be the lowest.
FAILS-IF: F-SCALP (g): the run start, `n_run` and `EXT` recomputed by a plain backward loop over the raw 5m slice
differ on any swing-failure order; (i) WALK-TABLE rows "return at exactly VAL", "one close beyond", "many closes
beyond", "gap inside the run". Planted mutations: `EXT` taken over `s … t−1`; `c5[t−1] ≤ VAL` in place of `<`; the
run judged against `val_j` (`VA(k1 − 1)`).

**L-S.8 BOTH TRIGGERS ON ONE BAR; "TIMING ONLY"** — "TRIGGER (5m, timing only — the 5m is never a signal source):
… OR …" (contract :89-91); "STOP: beyond the deviation extreme if the trigger was a swing failure, else …" (:97)
READING:
- `TRIG(d, t) = TRIG_A(d, t) OR TRIG_B(d, t)`. At most one order is born at a bar.
- **Precedence.** If both hold, `trigger_kind = "sfp"` and `also_cross = True`: the trigger WAS a swing failure,
  and the stop clause's "else" (:97) applies only when it was not. Otherwise `trigger_kind` ∈ {`"cross"`,
  `"sfp"`} as fired. The count of double triggers is printed.
- **"Timing only"** is held in three ways: (i) PERMISSION and the direction come from the 1h and 4h value areas
  alone (L-S.4, recomputable with no 5m file); (ii) every price level of the order (limit, stop unit, targets)
  comes from `G`, the single 5m-born level being the deviation extreme of a swing failure; (iii) the 5m supplies
  the instant τ, the closes compared with `G`, and the bars that fill and walk the order.
SOURCE: contract :89-91, :97; L-0.30 (5m SIGNAL SOURCE, its legs (a)-(d)).
RIVALS: cross takes precedence — the swing-failure stop is never nearer than the cross stop (L-S.10), so this
would move stops INWARD on double triggers against the text's if / else.
FAILS-IF: F-SCALP (g): a double-trigger order is stamped `cross`, or its stop is not the swing-failure stop;
planted mutation: the precedence reversed.

---------------------------------------------------------------------------------------------------------------
### C · The order

**L-S.9 THE LIMIT: AT THE EDGE, ON THE TICK GRID, FROZEN** — "ENTRY: a limit order AT the edge" (contract :92);
ruling O-20
READING:
- **The edge** is `EDGE` of `G`: the filed 6-dp `val` (long) / `vah` (short) of row `k1` (`edge_px`; F-NOT's
  PIVOT-RANGE leg holds it equal to the filed VA level).
- **The limit sits on the tick grid, snapped AWAY from the market**, by `TickGrid(E.ticks()[stem])` (L-D.23):
  long (a BUY limit) `n_L = floor_ticks(VAL)`; short (a SELL limit) `n_L = ceil_ticks(VAH)`; `L = px(n_L)`. One law
  for every resting limit in this section: **a BUY limit is floored to the grid, a SELL limit is ceiled** — it is
  never marketable against the price that placed it and never easier to reach than the raw level.
  `snap_ticks = |EDGE − L| / TICK ∈ [0, 1)` is filed per order.
- **Never marketable.** By SETUP `d·(c5[t] − EDGE) ≥ 0` and by the snap `d·(EDGE − L) ≥ 0`, so `d·(c5[t] − L) ≥ 0`.
  The builder asserts it in ticks (long: `floor_ticks(c5[t]) ≥ n_L`; short: `ceil_ticks(c5[t]) ≤ n_L`) and HALTs
  otherwise. A trigger pattern whose close is beyond the edge is not an order (L-S.6's counted class).
- **Frozen of record.** `G`, hence `L`, the stop, both targets and `R`, are fixed at τ and never re-read — not at
  the next 1h close, not at the fill, not after it. Nothing set at or after a bar can know that bar (scout U6 H4
  (ii)). The re-rolled-edge reading is the Tier-E twin `tierE__live_edge` (L-S.26).
- The order's size is one unit; nothing is added (L-0.30: no adds).
SOURCE: contract :92; O-20; L-D.22, L-D.23 ("The module defines NO fill rule, no snapping direction and no order
model: L-S states those"); X's frozen-edge law (LX-X2.4, LX-X2.5: targets "frozen at entry"; the live far side "as
of the bar's OPEN" a twin); scout U6 R-3, R-6, H6.
RIVALS: the raw edge as an off-grid price — no real order. Snapping TOWARD the market — an easier fill at a better
price than the edge: it flatters. A live limit following each re-rolled VA — the twin.
FAILS-IF: F-SCALP (d) TICK-FILL: `n_L` differs from a `Fraction` floor / ceil of the filed edge over the tick
string on any order, or `d·(EDGE − L) < 0`; (f) FROZEN: any level of an order differs from its recomputation from
row `k1` alone. Planted mutations: the snap direction reversed; `L` recomputed from the row of the fill bar.

**L-S.10 THE STOP** — "STOP: beyond the deviation extreme if the trigger was a swing failure, else 0.5 ATR_1h
beyond the edge; railed ≥ 1.0 ATR_1h" (contract :97-98)
READING: one call of the estate's stop function, every distance measured from the LIMIT price, `ATR = ATR_1h[k1]`:
`st = E.BK.brk_stop(d, ext, t, L, ATR, rail_atr=rail)` with `ext = EXT` (L-S.7) for `trigger_kind == "sfp"` and
`ext = L` for `"cross"`. It returns `tierc5_rules.spring_stop`'s record:
long `S = min(ext − STOP_BUF_ATR·ATR, L − rail·ATR)`; short `S = max(ext + STOP_BUF_ATR·ATR, L + rail·ATR)`;
`R = |L − S|`; `pivot_stop_px`; `rail_binding = (rail·ATR > |L − pivot_stop|)`.
- "Beyond" is the estate's one definition of the word, `STOP_BUF_ATR` — which is the contract's "0.5 ATR_1h" of the
  else-clause (asserted equal, L-S.2). So the swing-failure stop is 0.5·ATR_1h beyond the deviation extreme.
- **The rail's consequence, stated plainly:** on a CROSS trigger the structural stop is `L ∓ 0.5·ATR`, the rail
  is `L ∓ 1.0·ATR`, the rail always binds, and **R ≡ 1.0·ATR_1h on every cross-triggered order — the contract's
  "0.5 ATR_1h beyond the edge" never sets a stop.** The builder asserts `rail_binding` on every cross order and
  prints the two counts. On a swing-failure trigger `R = max(|L − EXT| + 0.5·ATR, 1.0·ATR)`: never smaller than
  a cross order's.
- `S` is a float level, not snapped to the grid: it is a stop-market trigger, tested by the lineage's comparison
  (L-S.18), and no tick rule in the contract names it.
- **No stop move, ever** (:100 "NO trail"): `S` is constant from τ to the exit; no breakeven after T1. The trade
  row carries `n_stop_moves` (always 0) and `stop_px_at_exit == stop_px` for F-NOT's TRAIL leg.
- `st is None` (a non-finite or non-positive ATR) → no order, counted `no_order_atr`.
SOURCE: contract :97-98, :100; `scripts/tierc10_brk.py:1366-1385`; `scripts/tierc5_rules.py:481-502`;
`tierc2_rules.py:127` (0.5), `tierc3_rules.py:148` (1.0) [read here]; X's use (`tc11x_sfp.py:496`); scout U6 C9,
R-11.
RIVALS: distances from the raw edge instead of the limit — the entry is the limit; R is measured from where the
position is. The rail dropped on cross triggers so that 0.5 ATR "means something" — contradicts "railed ≥ 1.0".
A stop snapped to the grid — a rule nobody wrote, with no unflattering direction.
FAILS-IF: F-SCALP (j) STOP: any order's `S`, `R` or `rail_binding` differs from the fixture's own arithmetic on the
filed row and the raw extreme; a cross order with `R ≠ rail·ATR`; a trade whose stop moved. Planted mutations: the
rail removed; a cross order's `ext` set to the trigger bar's low; a breakeven move after T1.

**L-S.11 THE TWO TARGETS** — "TARGETS: T1 = POC (half, resting limit, same fill rule); T2 = far edge − 0.25 ATR_1h
(remainder)" (contract :99)
READING: both are resting limits placed when the entry fills, on the grid by L-S.9's one law, levels from `G`:
- **T1:** the POC of the frozen profile. Long (a SELL limit) `n_T1 = ceil_ticks(POC)`; short `n_T1 =
  floor_ticks(POC)`. Size `Q`.
- **T2:** raw level `FAR − d·t2_offset_atr·ATR`, formed EXACTLY in `decimal` from `dec(FAR)`, `dec(ATR)` and the
  pin's fraction, then snapped: long `n_T2 = ceil_ticks(·)`; short `n_T2 = floor_ticks(·)`. Size = everything still
  open (X's law, LX-X2.5: "The remainder (0.5, or the whole position if T1 has not filled) rests at T2").
- **A void T1.** If `d·(n_T1 − n_T2) ≥ 0` the POC lies at or beyond T2, price reaches T2 first, and T2 takes the
  whole position: the T1 order never rests (`t1_void = True`, counted). This is what two resting orders do; it is
  not a filter.
- **No other geometry refusal.** `d·(n_T1 − n_L) ≥ 0` always (the POC is inside the band); a T1 at the entry
  price (`t1_at_entry`, counted) is traded as written — half goes off at the entry price and pays two maker fees.
  X's refusal of a target within 10 bps of entry (LX-X2.6) is NOT carried: this contract's only skip is "rr-min"
  (L-S.12), and removing near-zero T1 trades could only raise a mean.
- Filed per order: `t1_px`, `t2_px`, `t1_r = d·(t1_px − L)/R`, `t2_r = d·(t2_px − L)/R`, `r_atr = R/ATR`; their
  quantiles are printed.
- Both target fills use the book's own fill rule (L-S.15) and book the LIMIT price — no gap improvement.
SOURCE: contract :99; L-S.9; LX-X2.5, LX-X2.6 (`x_rec/tierc11x/LEANS_X.md`), `tc11x_sfp.py:483-522`; X's
`symmetric_gap` law ("the targets fill at the level"); scout U6 C10, R-12, R-16.
RIVALS: X's 10-bps refusal — see above. T1 kept resting when it lies beyond T2 and credited before T2 on a bar
that reaches both — books a price the position could not have reached with size left. Targets filled at
`max(level, open)` — a resting maker order books its own price.
FAILS-IF: F-SCALP (d): `n_T1`, `n_T2` differ from the `Fraction` arithmetic; (i) WALK-TABLE row "POC beyond T2":
the whole unit must exit at T2 and no T1 fill may exist. Planted mutations: the T2 offset taken with `ATR_1h` of
the fill hour; the void rule removed.

**L-S.12 "rr-min"** — "Minimum reward at T2 ≥ 1.5 × stop ["rr-min"]." (contract :100)
READING: evaluated at τ, on the grid prices, AFTER the rail: `reward = d·(px(n_T2) − L)`; the order is PLACED iff
`reward ≥ rr_min · R` (float64, that operand order). Otherwise it is `skipped_rr_min`: no order exists, the asset
stays free, and the trigger is a row of the refusal table with `t2_r`. With the rail, every placed order has T2 at
least `rr_min · rail` ATR_1h from the limit. The book WITHOUT this skip is the Tier-E twin `tierE__rr_unfiltered`,
RE-WALKED with its own order sequence (L-S.26).
SOURCE: contract :73-74 ("or the trade is skipped ["rr-min"]; the unfiltered twin printed"), :100, :135-136.
RIVALS: reward measured from the trigger close — the entry is the limit. Tested at the fill — a look at the fill
bar. The twin as a filter-off subset of the same orders — the skipped triggers would have blocked later ones;
X's ridden twins re-walk (`tc11x_sfp.py:167-168`).
FAILS-IF: F-SCALP (k) RR: an order of record with `reward < rr_min · R`; a skipped trigger that satisfies the
rule; the unfiltered twin, substituted for the book of record, must turn the leg RED. Planted mutation: the test
taken before the rail.

**L-S.13 VALIDITY AND CANCELLATION** — "valid 12 five-minute bars from the trigger close, cancelled on acceptance
beyond the edge ["validity"]" (contract :92-93)
READING:
- **Validity window:** the `V` bars `t+1 … t+V` BY INDEX on the 5m tape. The trigger bar itself has closed and
  cannot fill. A zero-volume bar is one of the V (L-D.16). If unfilled after bar `t+V` the order EXPIRES at
  `close5[t+V]`. A window that runs past `hi` and is unfilled by `hi` is `unresolved_at_end` — neither a fill nor a
  miss.
- **Cancellation.** "Acceptance beyond the edge" = a V2 `acceptance` event of the 1h lens on the faded side
  (`side == "bottom"` for a long, `"top"` for a short; L-V.14) with `τ < known_close_ms ≤ close5[t+V]`. The order
  is CANCELLED at that close: let `q` be the 5m bar with `close5[q] == known_close_ms`; bars `> q` are not tested;
  bar `q` itself IS tested (an intrabar fill precedes the close), and an order filled on `q` is then invalidated at
  that same close (L-S.19).
- **What can happen inside the window, as a checked consequence:** with `V·STEP5 == E.LENS_MS["1h"]` (asserted,
  not assumed) exactly one 1h close lies in the window on a gap-free tape; with PERM true no probe is pending at
  `k1`; so the only acceptance that can print there is by MARGIN on a probe's first bar (L-V.10), judged against
  the edge of `VA(k1)` — the order's own raw edge. For every cancellation of an order whose window holds no gap on
  the 5m or the 1h tape the builder asserts `by == "margin"`, `bars_out == 0` and the event's `E == edge_px`; a
  cancellation outside that case is counted apart (`cancel_other`) and listed.
- A lapse of PERMISSION that is not such an acceptance does not cancel (L-S.4).
SOURCE: contract :92-93, :136; L-V.10, L-V.14; L-D.16; scout U6 R-7.
RIVALS: bars `t … t+V−1` — the trigger bar is closed. A private acceptance test of 1h closes against the order's
limit — a second state machine inside a decision module; the machine is Stage V's. Cancel on any 1h close beyond
the edge (a probe) — the contract says acceptance.
FAILS-IF: F-SCALP (i) WALK-TABLE rows "fill on bar t+V", "no fill by t+V → expired", "acceptance at the window's
1h close → cancelled", "fill and acceptance on one bar → filled, then invalidated"; (l) the status partition.
Planted mutations: the window shifted to `t … t+V−1`; cancellation ignored; a fill accepted on bar `t+V+1`.

**L-S.14 ONE POSITION AND ONE RESTING ORDER PER ASSET** — "five home assets; both directions" (contract :84); the
contract is silent on concurrency
READING: per (asset, book) at most one order rests and at most one position is open, across both directions.
- At each 5m close `j`, in this order: (1) bar `j` is processed for the live order or position (fill, exit,
  expiry, cancellation); (2) a trigger at `close5[j]` is ADMITTED iff, after (1), no order is alive AND no position
  was open during any part of bar `j`.
- **A trigger while an order rests is REFUSED and counted (`refused_order_resting`); the resting order is never
  replaced, re-priced or stacked.** An order alive after `close5[j]` (unfilled, `j < t+V`, not cancelled) refuses.
- **A trigger while a position is open is refused (`refused_position_open`)** by the lineage's law: for a
  position filled on bar `f` and exited on bar `x`, every trigger at a close `j` with `f ≤ j ≤ x` is refused — the
  fill bar's close and the exit bar's close included, after an intrabar exit as after a close exit (`replay9`'s
  `ti <= open_until`; X's `blocks`).
- An order that EXPIRES or is CANCELLED at `close5[j]` is dead at that close and no position existed during bar
  `j`: a trigger there may place a new order (valid from `j+1`).
- A trigger skipped by "rr-min", by `no_order_atr` or by staleness leaves the state unchanged.
- Every refused or skipped trigger is a row of `S_refusals_<book>` with its reason; the identity
  `n_triggers == n_orders + Σ reasons` is asserted per asset and book. The count of holdout triggers refused by an
  order or position born at or before the era cut is printed (at most one per asset).
SOURCE: `scripts/tierc9.py:389-393` (`if ti <= open_until: reject "position_open"`); `tc11x_sfp.py:870-874`
(`blocks`), LX-X2.9; scout U6 C22, R-23.
RIVALS: replace-with-newest (counted as `refused_order_resting`, the number of times it would have acted). One
order per direction — two resting orders on one asset. Re-entry at the close of an intrabar exit — X's counted
rival, not the lineage's law.
FAILS-IF: F-SCALP (h) SEQUENCE: two orders or positions of one asset and book overlap in bars; the identity fails;
a refusal row's reason is not the state at that close. Planted mutations: replace-with-newest; a trigger admitted
at an exit bar's close.

---------------------------------------------------------------------------------------------------------------
### D · Fills

**L-S.15 THE FILL OF RECORD AND ITS TWO TWINS, IN INTEGER TICKS** — "FILL OF RECORD: a later 5m bar trades THROUGH
the limit by ≥ 1 tick (low < limit − tick for a long) ["fill"]. Twins printed: TOUCH (low ≤ limit) · DEEP (through
by 0.05 ATR_1h)." (contract :93-95); ruling O-20
READING: a resting limit at grid level `n` is tested on each bar's range with `TickGrid`'s integer comparisons —
never a float subtraction, never a tolerance. Three rules:

| rule | BUY limit at `n` (bar low `l`) | SELL limit at `n` (bar high `h`) | in words |
|---|---|---|---|
| TOUCH | `ceil_ticks(l) ≤ n` | `floor_ticks(h) ≥ n` | `l ≤ limit` / `h ≥ limit` |
| TICK (of record) | `floor_ticks(l) ≤ n − n_tick − 1` | `ceil_ticks(h) ≥ n + n_tick + 1` | `l < limit − n_tick·TICK` / `h > limit + n_tick·TICK` |
| DEEP | `floor_ticks(l) ≤ n − n_D − 1` | `ceil_ticks(h) ≥ n + n_D + 1` | `l < limit − n_D·TICK` / `h > limit + n_D·TICK` |

- **The operative inequality is the contract's parenthesis, strict:** `low < limit − tick`. "By ≥ 1 tick" alone
  would read `low ≤ limit − tick`; the parenthesis is the formula and is the stricter. On an on-grid tape the
  record therefore fills only when a bar trades at least `n_tick + 1` ticks through.
- **DEEP's depth:** `n_D = max(ceil_ticks(deep_atr · ATR_1h[k1]), n_tick)`, the product formed exactly in
  `decimal`, frozen at τ. The contract writes "through by 0.05 ATR_1h"; on part of the tape that is less than one
  tick (scout U6 §1.9: on 18.25% of NEAR's holdout hours at TC11's capture, 0.17% of ZEC's, 0.04% of SOL's), where
  DEEP as written would be LOOSER than the record. The floor at `n_tick` makes DEEP never shallower than the
  record, so that **for every order DEEP-filled ⇒ TICK-filled ⇒ TOUCH-filled, and the fill bars satisfy
  `fill_i_touch ≤ fill_i_tick ≤ fill_i_deep`** — by arithmetic, not by luck. `deep_floor_binding` (the floor was
  the larger term) is filed per order and its share printed per asset (OPEN TO OPERATOR 1).
- **Fill price = the limit, `px(n)`,** under all three rules and for all three resting limits (entry, T1, T2),
  whatever the bar's open. A resting order books its own price; when a bar opens beyond it the maker is filled at
  the limit and is immediately under water — which is the adverse selection the row is testing.
- **The fill bar** of a rule is the first bar of the window (L-S.13) on which the rule's test holds.
- **A bar with `volume == 0` fills no resting limit under any rule** (L-D.16's NO-TRADE default, adopted): no trade
  printed. Stops, invalidation and the time stop are evaluated on it as on any bar. The number of orders whose
  window held such a bar is printed.
- **The tick** is TC12's own capture applied to the whole corridor (O-20, L-D.22). Beside every fill table the
  build prints `data/TICK_GRID_AUDIT.json`'s on-grid shares and any `coarser_than_recorded_tick` month for the
  asset and segment (L-D's OBJECTION O-20 bears here: "stricter than history" is proven only where the tape's
  granularity is not coarser than the recorded tick).
SOURCE: contract :93-95, :136; O-20; L-D.16, L-D.22, L-D.23 (the four integer comparisons); X's trade-through law
(LX-1.1 (ii): "A touch that does not trade through is not a fill"); scout U6 C2, C3, R-2, R-4, H5, H7.
RIVALS: `low ≤ limit − tick`; float `l < L − tick` (mis-decides exact-boundary lows, the common case on an on-grid
tape); DEEP as written (inverts the ladder on NEAR, and the kill would read "fails under DEEP too" on a twin that
is not deeper); a per-era tick inferred from the tape (L-D.22).
FAILS-IF: F-SCALP (d) TICK-FILL: production's three tests, on the fixture's enumerated cases (each home tick ×
lows / highs on-grid, one finer decimal place above and below, the exact boundaries `n`, `n ∓ n_tick`,
`n ∓ n_tick ∓ 1`, `n ∓ n_D`), differ from brute-force `Fraction` comparisons; a zero-volume bar fills. Planted
mutations: TICK written as `l ≤ limit − tick`; a float comparison; DEEP without the floor (the inclusion leg (c)
must go RED on a constructed order with `deep_atr·ATR < TICK`); a fill on a zero-volume bar.

**L-S.16 THREE BOOKS, AND THE INCLUSION PER ORDER** — "F-SCALP (… fill rule ordering TOUCH ≥ TICK ≥ DEEP by n filled
— an inverted order must FAIL)" (contract :120-121); "the fill-sensitivity row is part of the verdict text" (:105)
READING:
- **Three books, one simulator.** `scored` (TICK, the book of record), `ladder__touch` and `ladder__deep` (L-X.24's
  arm names) are three walks that differ ONLY in the fill rule, applied to the entry and to both targets ("same
  fill rule", :99). Each walk has ITS OWN one-order / one-position sequence (L-S.14) — the law of X's ridden twins
  — because an order filled under one rule occupies the asset and changes which later triggers become orders.
- **Therefore the ladder is asserted PER ORDER, not on book totals.** Every order row of every book carries all
  three entry tests evaluated on that same order: `fill_i_touch`, `fill_i_tick`, `fill_i_deep` (null if none in
  the window). Asserted on every order of all three ledgers: `fill_i_deep` non-null ⇒ `fill_i_tick` non-null ⇒
  `fill_i_touch` non-null, and `fill_i_touch ≤ fill_i_tick ≤ fill_i_deep` where present. On each ledger the counts
  `n_filled_touch ≥ n_filled_tick ≥ n_filled_deep` follow and are asserted — this is the contract's "TOUCH ≥ TICK ≥
  DEEP by n filled", on a common set of orders, where it is a theorem.
- **Book totals are printed and are NOT a theorem:** `n(ladder__touch)`, `n(scored)`, `n(ladder__deep)` are the row
  counts of three differently sequenced books; a touch-only fill can block triggers the record would have traded.
  The build prints the three totals beside the per-order counts and flags `BOOK-N-NOT-MONOTONE` if they are not
  ordered. That flag is a disclosure, never a HALT (INTERFACE: L-X.24's `LADDER-ORDER`).
- An order's status in a book is by that book's rule: `filled` (at `fill_i`), `expired`, `cancelled`,
  `unresolved_at_end`. A MISS of a book = `expired` or `cancelled` in that book.
- `S_FILL_SENSITIVITY` (a grid, whole): book × {each asset, POOLED} × trigger era × direction →
  `n_orders, n_filled_touch, n_filled_tick, n_filled_deep, n_expired, n_cancelled, n_unresolved,
  n_deep_floor_binding, n_window_zero_volume`. Counts only.
SOURCE: contract :93-96, :105, :120-121; L-X.9 (the three `C(X)`; "ladder" arms), L-X.24; `tc11x_sfp.py:167-175`
(RIDDEN twins "re-walk their own events with their own one-position sequence"); scout U6 H14 ("… inclusion
must be asserted on ORDERS (per trigger), before one-position sequencing, or it will not hold").
RIVALS: (a) the ladder twins as the record's orders re-filled, overlaps allowed — two positions on one asset in a
book that claims one. (b) the same, overlaps refused — neither a faithful book under the rule nor a common order
set. (c) the count ordering asserted on book totals — not guaranteed, so a HALT on it can fire with no defect.
FAILS-IF: F-SCALP (c) LADDER: an order with a deeper fill and no shallower one, or with fill bars out of order;
a per-ledger count out of order. Planted mutations — "an inverted order must FAIL": the TICK and DEEP tests swapped
inside production; TOUCH tested with `<`; DEEP's depth computed from the fill hour's ATR.

**L-S.17 THE FILL BAR** — "a later 5m bar trades THROUGH the limit" (contract :93); X's fill-child law
READING: on the fill bar `f` the entry books at `L`, and then, on that same bar:
- **the stop is tested** (L-S.18 steps 1-2): the path that traded through the limit may have gone on to the stop.
  A stop on the fill bar is a full-unit loss on bar `f` (`stop_on_fill_bar`, counted);
- **no target is credited**: a sell order cannot rest before the buy fills, and the bar does not show the order.
  The bars on which the book's target test holds on `f` are counted (`fillbar_target_withheld`); T1 and T2 rest
  from bar `f+1`;
- the close events of L-S.18 apply (invalidation at `close5[f]`; the corridor end if `f == hi`); the time stop
  cannot fall on `f`.
The position's clock, its funding and its `entry_ms` / `entry_close_ms` are bar `f`'s (L-S.20, L-S.21, L-S.25).
SOURCE: LX-1.1 (ii) (`x_rec/tierc11x/LEANS_X.md:590-597`: "The STOP is tested on it, adverse-first … Targets are
never credited on the fill child"); `tc11x_sfp.py:686-712`; scout U6 R-15, H6.
RIVALS: targets live on the fill bar — credits a path the bar cannot order. The stop not tested on the fill bar —
hides the worst case of a maker fill.
FAILS-IF: F-SCALP (i) WALK-TABLE rows "fill bar reaches T1 → withheld", "fill bar reaches the stop → stopped on
f"; planted mutations: a T1 fill on `f`; the stop skipped on `f`.

---------------------------------------------------------------------------------------------------------------
### E · The walk after the fill

**L-S.18 SAME-BAR ORDER ON A 5m BAR** — the contract is silent; "taker on the stop" (:101); "NO trail" (:100)
READING: each 5m bar `j ≥ f` is stepped once, on what is still open, in this order (long; short mirrored):

| step | test | act |
|---|---|---|
| 1 · STOP at the open | `o[j] ≤ S` | exit ALL at `o[j]`, reason `stop`, `gap_stop = True` |
| 2 · STOP, adverse-first | `l[j] ≤ S` | exit ALL at `S`, reason `stop`; `both_touch` counted if a target test holds on this bar too |
| 3 · T1 (if resting; `j > f`; `volume > 0`) | the book's SELL test at `n_T1` on `h[j]` | sell `Q` at `px(n_T1)` |
| 4 · T2 (`j > f`; `volume > 0`) | the book's SELL test at `n_T2` on `h[j]` | sell the rest at `px(n_T2)`, reason `T2` — the same bar as T1 if reached |
| 5 · close: INVALIDATION | `close5[j]` is an acceptance close on the faded side (L-S.19) | exit the rest at `c[j]`, reason `invalidation` |
| 6 · close: TIME STOP | `j == f + T5` | exit the rest at `c[j]`, reason `time_stop` |
| 7 · close: CORRIDOR END | `j == hi` | mark the rest at `c[hi]`, reason `corridor_end` |

- **Stop first, unconditionally — the pessimistic rule.** A bar that reaches the stop and a target is a stop for
  everything still open. X's open-decides-first step for a TARGET (LX-X2.10 step 0) is not carried: the bars
  where the open was already through a target on a stop bar are counted (`stop_bar_open_through_target`), so a
  reader sees what the rival would have credited.
- **The stop's price.** A stop is a taker market exit: when the bar OPENS at or beyond the stop it is filled at
  the open (the worse price), otherwise at the stop. The lineage books every stop at the stop even through a gap
  (`tierc7.py:186-189`); X filed the other law as its symmetric-gap twin, noting the record "favours the trader
  on both sides". With targets at their level (L-S.11) and the stop at the worse of stop and open, neither favour
  is in this book. The stop test is the lineage's float comparison `d·(price − S) ≤ 0`.
- Nothing sequences inside a 5m bar: it is the finest clock in the snapshot's scope (1m tapes are out of scope,
  L-D.27).
- Steps 5-7 are close events and share a price; their order fixes the LABEL only.
SOURCE: LX-X2.10 (`x_rec/tierc11x/LEANS_X.md:1292-1315`); `tc11x_sfp.py:571-601` (`bar_step`; its `gap_sym`
branch is the symmetric-gap twin, :553); `scripts/tierc7.py:186-189` [read here]; scout U6 R-14.
RIVALS: X's `bar_step` verbatim (open first for targets; stop at the stop) — both differences from it are in the
direction that cannot flatter, and both are counted. Targets before the stop — optimistic.
FAILS-IF: F-SCALP (i) WALK-TABLE: a synthetic 5m tape drives every row of this table and the rows of L-S.13 and
L-S.17; production's (exit bar, price, reason, T1 fill) must equal the table's. Planted mutations: T1 tested
before the stop; a gap stop booked at the stop; T2 denied on the bar T1 filled.

**L-S.19 INVALIDATION** — "invalidation on acceptance beyond the edge regardless of stop." (contract :98)
READING: while a position is open, a V2 `acceptance` event of the 1h lens on the faded side (`bottom` for a long,
`top` for a short) with `close5[f] ≤ known_close_ms` EXITS everything still open at the close of the 5m bar that
ends at that instant, at that bar's 5m close price, as a TAKER, reason `invalidation` — after the bar's intrabar
steps, and whether or not the stop was touched ("regardless of stop"). The event is read from Stage V's filed
`va_events`; no acceptance test is re-implemented here. If no 5m bar closes at that instant (a gap) the exit is
the first 5m bar closing after it, counted.
- On a bar where the stop is also reached the stop is booked (L-S.18's step order), so `invalidation` labels only
  the exits the stop did not take: the hour closing beyond the edge N times with the stop untouched, a margin
  acceptance inside a far swing-failure stop, a margin acceptance after the ATR has contracted. Printed:
  `n_invalidation` by the event's `by` and by `trigger_kind`.
- The price of the exit is the 5m tape's close, not the 1h tape's (the venue's intervals can disagree on incident
  bars, scout U4 H11); the number of invalidation bars where the two differ is printed.
SOURCE: contract :72-73, :98; L-V.10, L-V.14; TC11 `LEANS.md:458-459` (L-S.2: "Exit at that 1h close (the
coincident 5m close), taker"); X's `TAKER_EXITS` (`tc11x_sfp.py:148`); scout U6 C11, R-28.
RIVALS: the first 1h CLOSE beyond the edge (a probe) — the contract says acceptance. Exit at the next bar's open —
the event is known at the close and the filed precedent exits there.
FAILS-IF: F-SCALP (i) rows "count acceptance with the stop untouched → invalidation at that 5m close",
"acceptance and stop on one bar → stop"; (a) covers a real one if the class exists. Planted mutations:
invalidation ignored; the exit booked at the stop.

**L-S.20 THE TIME STOP, NO TRAIL, THE CORRIDOR END** — "TIME STOP = the 1h traverse (V4); NO trail." (contract :100)
READING:
- `T5 = TRAVERSE.json by_lens.1h.T_in_5m_bars` = the tuning-fit 1h value-area traverse (O-18, L-V.18) in 5m bars,
  the factor being the lens ratio by object. It is read through the fitted-pin door; every trade row carries
  `T = T5` and the book's manifest carries `time_stop_source {path, key, sha256, value}` (L-V's F-TRAV (e)).
- **The clock starts at the FILL bar:** a position still open at `close5[f + T5]` exits there, at that close, as a
  taker, reason `time_stop`. The count is by 5m bar INDEX (a zero-volume bar is one bar).
- **No trail:** the stop never moves (L-S.10); the position never grows; T1 does not move the stop.
- **Corridor end:** a position still open at `hi` is marked at `c[hi]`, reason `corridor_end`, booked as a taker
  exit, flagged `open_at_end`; an unfilled T1 half stays unfilled. In WALK-W this is the scored window's law
  (O-9; L-X.24); the trade's continuation is printed from WALK-PIN (L-S.25).
SOURCE: contract :42-43, :100; O-18; L-V.18 (rival (g): the T-th 1h close after the fill "depends on where in the
hour the fill lands"); LX-X2.7, LX-X2.17; `scripts/tierc7.py:209-211` (the shadow clock); scout U6 R-17.
RIVALS: the clock from the trigger bar (X's maker-conditioned twin kept the record's clock so that it differed by
the fill test only; here the limit order IS the record, and the traverse measures travel from a touch of the
edge — the fill). A typed integer — F-TRAV.
FAILS-IF: L-V's F-TRAV (a), (e) on this builder; F-SCALP (i) row "open at f + T5 → time stop at that close", and
(n): `T5` bent by one bar moves the exit bar by one. Planted mutation: the clock anchored at `t`.

---------------------------------------------------------------------------------------------------------------
### F · Costs

**L-S.21 COSTS OF RECORD** — "COSTS OF RECORD: maker bps per side on entry and targets; taker on the stop; funding
journaled." (contract :101); the "maker" ruling (:2-3)
READING:
- **Which leg pays what** (`fz = E.fees()[stem]`; `mk = fz["maker_bps_side"] / BPS_PER_UNIT`, `tk =
  fz["taker_bps_side"] / BPS_PER_UNIT`): MAKER on the entry, on T1 and on T2; TAKER on every other exit — `stop`,
  `time_stop`, `invalidation`, `corridor_end` (X's `TAKER_EXITS` law). The contract names the stop; the time stop,
  the invalidation and the mark are market exits at a close and are booked at the dearer rate. No slippage on any
  leg of the record.
- **Gross and funding are the estate's function, called as it is:**
  `acc = E.BK.account_l(lf5, E.TP.CONTROL_CARD, d, R, leg)` with `leg = {entry_i: f, entry_px: L, exit_i: x,
  exit_px, harvest: None | (h_i, px(n_T1), d·(px(n_T1) − L)/R)}`. `gross_r = acc["gross_r"]`; `funding_r =
  acc["funding_r"]` — the interval sum of every funding stamp with `open5[f] < stamp ≤ open5[x]` (the T1 fraction
  to `open5[h_i]`), each priced at the last 5m close at or before it, the D12 ceiling taken once on a cost
  (`funding_r_uncapped`, `funding_ceiling_bound`, `funding_stamps` filed; the bound count printed). A stamp at the
  instant the fill bar opens precedes the fill and is not paid.
- **The fee of record is booked per fraction** (X's `fee_per_fraction`, mirrored as
  `tierc12_scalp.fee_per_fraction` with its original named): with `b_x = mk` if the exit reason is `T2`, else `tk`,
  harvested: `fee_r = [Q·(mk·L + mk·p_T1) + (1 − Q)·(mk·L + b_x·p_x)] / R`; not harvested:
  `fee_r = (mk·L + b_x·p_x) / R`.
  `fee_maker_r` and `fee_taker_r` are its maker-leg and taker-leg parts (`fee_taker_r = 0` on a `T2` exit).
- **`net_r = gross_r − fee_r − funding_r`** — the toll of record, in R of the frozen `R`.
- The row's four TC12 fee columns are L-X.24's: `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`,
  `taker_twin_net_r` (L-S.22).
SOURCE: contract :2-3, :101; O-19; `scripts/tierc10_brk.py:1223-1326` (`funding_interval`, `account_l`);
`tc11x_sfp.py:148`, :756-803 (`fee_per_fraction`, `book_trade`); LX-X2.11; TC11 L-1.2 ("Maker legs carry zero
slippage. Stop and invalidation legs stay taker"); L-X.24; L-D.17 ("WHICH LEGS pay it is defined by the
registration texts").
RIVALS: maker on the time stop and the invalidation (resting orders "could" be used) — a market exit at a close is
a taker act; the dearer booking cannot flatter. A second funding routine for 5m — `account_l` is lens-generic.
FAILS-IF: F-TOLL (t3): a leg's rate is not the one this table assigns, or `fee_maker_r + fee_taker_r ≠ fee_r`
within the tolerance; (t1): a bps literal in the builder. Planted mutations: maker left on the stop leg; the time
stop booked maker; a typed maker rate.

**L-S.22 THE TWINS ON EVERY ROW** — "TWINS on every row: all-taker (the TC-series toll) · charter slippage."
(contract :102); "F-TOLL (… taker twin == TC-series)" (:121)
READING: every trade row of every arm carries, on the SAME fills and the same path:
- **`taker_twin_net_r = acc["net_r"]` and `fee_all_taker_r = acc["fee_r"]`** — `BK.account_l`'s own booking, which
  charges `FEE_BPS_SIDE` on every fraction: the TC-series toll law, unchanged. The identity `taker_twin_net_r ==
  net_r + fee_r − fee_all_taker_r` (L-X.24) holds by construction, and the per-fraction form at all-taker rates
  must equal `account_l` within `HAIRCUT_TOL` on every row (X's F-FEE-EQ law; bit-equality is not attainable,
  the terms associate differently).
- **`haircut_net_r = net_r − fee_taker_r × (slip / taker_bps_side)`**, `slip = fz["slippage_bps_side"]` — TC11's
  AM-7 with its maker clause: charter slippage falls on the TAKER legs of the record only (stop, time stop,
  invalidation, mark); "A maker leg … carries zero slippage". This is the column L-X.24's haircut law checks.
- **`taker_twin_haircut_net_r = taker_twin_net_r − fee_all_taker_r × (slip / taker_bps_side)`** — AM-7 on the
  all-taker twin, slippage on EVERY fill: the harshest cost row, printed beside (an extra column).
The scorer rules the first two as its `taker_twin` and `haircut` beside-prints (L-X.14); none of the three decides
a word.
SOURCE: contract :102, :121; TC11 `LEANS_AMENDMENTS.md:86-96` (AM-7); LX-X2.11; `tc11x_sfp.py:780-792`; L-X.14,
L-X.24; `scripts/tierc11_score.py:264`.
RIVALS: the charter twin on every fill of the record book — charges slippage on legs that are resting limits.
An all-taker twin re-walked with touch fills — it would be another book; the contract's twin is a toll.
FAILS-IF: F-TOLL (t2), (t5). Planted mutations: the twin computed with a maker entry; slippage applied to a maker
leg; `account_l` handed a card other than the control card (the half and the ceiling would move).

---------------------------------------------------------------------------------------------------------------
### G · Misses, regime columns, population

**L-S.23 THE MISS COLUMN** — "MISS COLUMN first-class: every unfilled order counted and its would-have outcome
printed at both targets." (contract :95-96)
READING:
- **A miss** is an order of the book of record whose status is `expired` or `cancelled` (L-S.16). Each carries
  `miss_class`: `touched_not_through` (`fill_i_touch` non-null) or `never_touched`. `unresolved_at_end` orders are
  listed apart and are not misses.
- **The would-have walk** answers "what did the limit cost us": the same order taken AT THE TRIGGER CLOSE AS A
  TAKER. Entry price `c5[t]` on bar `t`; the frozen stop `S` and the frozen target levels; `R_wh = |c5[t] − S|`;
  walked from bar `t+1` by L-S.18 with the record's target test; the time stop at `close5[t + T5]`; invalidation
  by L-S.19; booked ALL-TAKER by `BK.account_l` (entry leg at bar `t`), funding included.
- **"At both targets"** = three walks per miss, each on the whole unit unless stated: `T1` (the only target is
  T1), `T2` (the only target is T2), and `split` (the book's own law: `Q` at T1, the rest at T2). Each files
  `wh_exit_reason`, `wh_reached` (the walk ended at its target), `wh_exit_close_ms`, `wh_net_r`, `wh_gross_r`.
  For an order with a void T1 (L-S.11) the `T1` walk does not exist (filed null, reason `t1_void`) and `split` is
  the `T2` walk.
- **Why the trigger close and a taker fill.** It is the only counterfactual executable at decision time. Entry
  "at the limit" assumes a fill at a price the market never gave (and for `never_touched` a price never traded).
  Entry at the expiry close starts after the move the order missed and makes missing look cheap. Of the
  executable readings this is the one that cannot flatter the book: it shows the full run-away at the dearest toll.
- `S_miss` (per miss × target; pointed, not inlined) and the grid `S_MISS_GRID` (whole): trigger era × direction
  × `miss_class` × target → `n, n_reached, mean wh_net_r, sum wh_net_r`. Tier-E, "no interval", no verdict word,
  NEVER netted into any book.
- Printed on the fill-sensitivity grid: `n_orders`, `n_filled` per rule, `n_missed` (L-S.16).
SOURCE: contract :95-96; X's refusal rows for misses (`reason` "miss" / "miss_nochild" / "fill_unresolved_at_pin",
`tc11x_sfp.py:672-685`) — no outcome there; scout U6 C15, R-22.
RIVALS: as argued. A would-have at maker rates — an unfilled maker order paid no maker fee; the chase is a taker.
FAILS-IF: F-SCALP (b) MISS-3 and (l) MISS-TABLE: the status partition `n_orders == filled + expired + cancelled +
unresolved` fails; a miss has a TICK fill in its window; a would-have row differs from the fixture's own walk.
Planted mutations: the would-have entered at the limit; a filled order listed as a miss; the split walk booked at
maker rates.

**L-S.24 REGIME COLUMNS** — "REGIME COLUMNS: 1h ATR tercile (trailing) · VA age · breadth · 4h tide age." (contract
:102-103)
READING: four stamps on every order row and every trade row of every arm, each as of the trigger close τ, Tier-E,
COLUMNS ONLY — no book is cut, gated or re-walked by them, and the only table is an occupancy grid of counts.
- **`atr1h_tercile`** — the trailing midrank of `ATR_1h[k1]` among that asset's last `vol_window` finite
  `ATR_1h` values ending at bar `k1` INCLUSIVE (X's LX-X1.7 / LX-X4.2 law, mirrored from
  `tc11x_pct.trailing_counts`): with `(lt, eq, n)` the counts below, equal and total, decided in integers —
  `T1` iff `3·(2·lt + eq) < 2·n`; `T2` iff `< 4·n`; else `T3`; `unbanded` when fewer than `vol_floor` values exist.
  The raw ATR, the asset's own series. `atr1h_lt`, `atr1h_eq`, `atr1h_n` are filed.
- **`va_age_1h`** — the filed `va_age` of row `k1` (bars since the 1h value regime began, L-V.16); never null on
  an order (PERM requires INSIDE, so a regime is alive).
- **`breadth_5`** and **`tide_age_4h`** (with its band) — L-G's breadth of record and the asset's own 4h tide age
  of record, read from L-G's filed per-4h-bar table at the last 4h bar with close ≤ τ (`asof_index`). Their
  definitions are L-G's; this section adds none.
- `S_REGIME` (a grid, whole): for the three LEVELLED columns (`atr1h_tercile`; `breadth_5`; the tide band) column
  × level × book → `n_orders, n_filled`; for the two AGES (`va_age_1h`, `tide_age_4h`), which have no levels and
  are given none here, per book `n`, minimum, lower hinge, median, upper hinge, maximum (L-V.18's hinge law, so no
  quantile level is typed). Counts and positions only; no outcome column.
SOURCE: contract :102-103; `x_rec/scripts/tc11x_pct.py:71-106` (sha `49809c07…4bb7`); X's
`exit/build_manifest.json` `constants.vol_window`, `.vol_floor`; LX-X1.7, LX-X4.2, LX-X4.7; TC11 `LEANS.md:464-467`
(L-S.2's "trailing 2,000-bar quantiles over a window ending at the entry bar inclusive"); L-V.16; scout U5 §2.15.
RIVALS: an expanding pooled prefix (the tide band's "trailing") — the filed precedent for an ATR tercile in the
scalper is the rolling window. NATR — X's twin. Outcome tables by regime level — a cut of the book the contract
does not order ("columns").
FAILS-IF: F-SCALP (m) REGIME: a stamp differs from the fixture's own loop over the filed series up to `k1` / the
4h as-of bar; a tercile decided on a sample reaching past `k1`. Planted mutations: the window end at `k1 + 1`; the
4h columns joined at the bar containing τ.

**L-S.25 POPULATION, ERA, THE SCORED WINDOW, THE STRIP** — "(vs zero; HOLDOUT era ["era"]; five home assets; both
directions; …)" (contract :83-84); rulings O-9, O-23
READING:
- **Panel:** the five home assets (L-D's home panel object), pooled; both directions in one book.
- **A trade's era is its FILL bar's close** (O-9: "holdout = entry-bar close after `1719791999000`"; L-X.24:
  `entry_close_ms` is "the 5m bar of the fill", `era == era_of(entry_close_ms)`): `entry_ms = open5[f]`,
  `entry_close_ms = close5[f]`. **The book of record is the rows of the TICK walk with `ERA_CUT < entry_close_ms
  ≤ W`.** A position open at `W` is marked there (`corridor_end`).
- **An ORDER's era is its trigger close** (`era_trigger`): an unfilled order has no entry bar. An order triggered
  at or before the cut and filled after it is a holdout TRADE and a tuning ORDER; at most one per asset and book
  can exist (one resting order), and the count is printed (`era_straddle`).
- **One walk, not two.** The scored book is the holdout slice of the full-corridor TICK walk (L-S.1); the same
  walk's every row with `entry_close_ms ≤ W` is the arm `tierE__full_corridor` (L-X.14). The walk is not restarted
  at the cut.
- **The strip:** `regbooks/P-SCALP-3/strip.parquet` = the WALK-PIN rows with `W < entry_close_ms ≤ PIN` (L-X.24);
  ridden, printed beside, never scored, never pooled (O-9). Trades open at `W` are continued in
  `stage_s/open_at_w_continued.parquet` (their WALK-PIN exit beside their scored mark).
- **Prefix identity:** every WALK-PIN order and trade resolved at or before `W` equals its WALK-W row on every
  column; the WALK-W rows marked `corridor_end` are exactly the keys of `open_at_w_continued`.
- **What is in-sample on these bars** is the label's business (L-S.29): the lookback and the traverse are
  tuning-fit and are out-of-sample on the holdout; the bars themselves are `pre_seen` (O-23).
SOURCE: contract :83-84, :137; O-9; L-X.4, L-X.14, L-X.24; L-D.28; TC11 `LEANS.md:95-102` (L-1.3: "era = the entry
(or event-anchor) bar's CLOSE … P-SCALP-2 names the holdout era, so it is scored there").
RIVALS: era by the trigger close for trades — contradicts O-9 and the scorer's row law. A walk begun fresh at the
cut — discards the position a trader would have carried across it. Scoring to TC12's pin — O-9.
FAILS-IF: F-SCALP (e3) W≡PIN PREFIX and (o) VIEWS: a WALK-PIN row resolved by `W` differs from WALK-W; a scored row
with `entry_close_ms ≤ ERA_CUT` or `> W`; a strip row at or before `W`. Planted mutations inside production:
WALK-W reads an acceptance event after `W`; `hi_W + 1`; the era taken from the trigger close.

**L-S.26 THE TIER-E VIEWS** — "the full-corridor and 17-asset views Tier-E" (contract :84); "the unfiltered twin
printed" (:74)
READING: each is collared (L-0.16), carries no verdict word, and is promoted to nothing (:133).
- **`tierE__full_corridor`** — L-S.25. On its tuning rows the lookback and the traverse are IN-SAMPLE (tuning-fit);
  the row label says so.
- **`tierE__panel17`** — the same TICK walk on all seventeen assets, holdout by fill, stamped with the 17-asset
  panel. What it honestly is: the snapshot carries 5m, funding and a tick for all seventeen (O-8), and Stage V files
  1h and 4h value areas for the twelve (L-V.22), so the simulator RUNS; but for the twelve the lookback is the
  CLASSIC5-fitted pin, the traverse is the CLASSIC5 tuning fit, **no feasibility word and no licence exist** (the
  "1h maker PASS" is a POOLED:CLASSIC5 word), MNT's maker rate is an assumption on another venue's schedule, and
  several tapes begin inside the holdout (the first readable instant per asset is printed). Every row of the twelve
  carries `licence = "none — CLASSIC5 word transplanted"`. The five home assets' rows in this arm must equal the
  scored arm's (asserted). Its 5m reads are Stage S's own (`FIVE_MIN_READERS_T`).
- **`tierE__rr_unfiltered`** — L-S.12's twin, re-walked.
- **`tierE__live_edge`** — the limit follows the re-rolled value area: at the one 1h close inside the window
  (bar `q*`, new row `k1' = asof_index(close_ms_1h, close5[q*])`), an order still unfilled is re-priced for bars
  `> q*` from `VA(k1')` and `ATR_1h[k1']` by L-S.9 … L-S.12 (same direction, same trigger kind and extreme; the
  window is not extended); it is cancelled and counted if the new limit is marketable against `c5[q*]` or fails
  "rr-min". Once filled, everything is frozen.
- **Slices of the book of record, descriptive** (`S_SLICES`, a grid, whole; `n`, mean and sum of `net_r`, "no
  interval"): per asset; per direction; per `trigger_kind`; `on_1h_close`; `t1_void`. The scorer's own
  beside-prints (L-X.14) are computed from the arms and are not repeated here.
SOURCE: contract :74, :84, :133; O-8; L-V.22; L-X.14, L-X.24; L-0.15, L-0.16.
RIVALS: the 17-asset view as NA "because Stage D names 1h/4h/1d for the twelve" — O-8 reads that sentence as binding
Stage V's lenses, not the tapes; the view is printed with its limits named instead. A per-asset lookback for the
twelve — L-V.22's rival.
FAILS-IF: F-SCALP (o) VIEWS: a home row of `tierE__panel17` differs from the scored arm; a row of the twelve lacks
its label; the holdout slice of `tierE__full_corridor` is not the scored arm; a Tier-E table lacks the collar
(F-COLLAR). Planted mutations: a home row altered in the 17-asset arm; a verdict column added to a view.

---------------------------------------------------------------------------------------------------------------
### H · Precondition, the kill, the label

**L-S.27 THE PRECONDITION** — "1h maker PASS … (the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h
maker}; nothing else may trade a range)" (contract :39-41); "a registration closed by precondition spends no test"
(:9); "exists by the "maker" ruling" (:82)
READING: two items, evaluated by the builder BEFORE any candidate is computed and again by the scorer (L-X.10).
1. **The licence word.** Record `research_outputs/tierc12/va/VA_MIRROR.json`, certified by
   `progress/TC12-V.json` `artifact_shas`; selector `licence["1h|maker"].by_era["holdout"].would_read`; required
   `"PASS"` (exact string). It is X's filed word for POOLED:CLASSIC5 · holdout · `va_regime` · 1h · maker
   (`x_rec/tierc11x/va/feasibility.parquet`, sha `ea8573b3…b6f0`), mirrored by L-V.17; read through the reader's
   `licence("1h", "maker", "holdout")`, which HALTs for any pair outside the licence set.
2. **The licence at the pinned maker rate.** The word of item 1 was earned at the round trip X assumed (the row's
   `toll_bps`). TC12 books the maker rate Stage D pins (`data/fee_schedule.json`, certified by
   `progress/TC12-D.json`; the venue block of the home assets). The item re-derives the row's edge leg at that
   rate by the census's own linear toll law, from the row's PRINTED columns only:
   `edge_net_at_pin = round(edge_median_term_h20, 8) − round(edge_toll_atr × (2·maker_bps_side / toll_bps), 8)`;
   required `> 0`. Where the pin equals X's assumption the item is item 1 again (asserted identical). Selector:
   `licence["1h|maker"].by_era["holdout"].at_maker_pin.edge_net_h20` of `VA_MIRROR.json` (INTERFACE: L-V files that
   block; until it does, builder and scorer compute it from the two certified records by this formula). The height
   leg's `ratio_median` scales by `toll_bps / (2·maker_bps_side)` and is checked the same way against the census's
   floor `HEIGHT_RATIO_MIN` (read as L-V.17 item 5 (d) reads it: an AST literal of `scripts/tierc10_census.py`
   :2155); `share_ratio_lt_1` cannot be re-derived from printed columns and is carried as read.
- **Not met** → `regbooks/P-SCALP-3/STATUS.json` with `status = "CLOSED_BY_PRECONDITION"`, the item, the value
  found, `arms = []`, and NOTHING else: no candidate, no order, no book, no MISS table, no Tier-E view (O-22).
  The §0 cell reads `CLOSED BY PRECONDITION (<record>#<selector> reads <found>; required <required>) — no number ·
  no test spent`; m stays as parsed and the bar is not loosened.
- On the records as filed item 1 is met (F-VA-MIRROR HALTs the tier otherwise); item 2 is undetermined until
  Stage D's fee capture. Both are proven on planted records.
- What the licence is NOT is carried as DISCLOSURES D-2 beside the verdict: it was earned on X's record machine,
  on the outer 20% of value with an H20 exit and BOTH legs at the maker rate, while this trade pays the taker rate
  on every exit that is not a target.
SOURCE: contract :9, :39-41, :82; O-17, O-19, O-22; L-V.17 items 7-10; L-X.10; the licence row [read here:
`would_read "PASS"`, `toll_bps 4.0`, `of_record_for_detector False`, `edge_median_term_h20 0.102664`,
`edge_toll_atr 0.064663`, `edge_net_h20 0.038001`, `ratio_median 147.976520`]; scout U2 §1.8 (the linear toll law,
the break-even round trip); TC11 `LEANS.md:444-446` (L-S.1) and `regbooks/P-SCALP-2/STATUS.json` (the filed form).
RIVALS: item 1 alone, the pinned rate "printed beside" (O-19's minimum) — then a published maker rate at which the
edge leg FAILS would still trade a lens the Q-R3 law closes "unless the toll model changes"; of the two faithful
readings the one taken cannot flatter. Re-deriving the licence under the V2 machine — O-17 forbids. The ALL-era or
tuning row — the row is scored on the holdout and reads its own era's word (O-17).
FAILS-IF: F-SCALP (p) GATE: with a planted `VA_MIRROR.json` copy whose 1h maker holdout word is not `"PASS"`, or a
planted fee file whose maker rate makes `edge_net_at_pin ≤ 0`, the builder writes anything but STATUS, or a
candidate is computed (a call counter); L-X's F-FAM (PLANTED) holds the scorer's side. Planted mutations: the
gate reading the taker row; the gate reading the ALL era; item 2 evaluated at X's rate instead of the pin.

**L-S.28 THE PRE-NAMED KILL, EXHAUSTIVELY** — "PRE-NAMED KILL: NOT SUPPORTED if the through-tick book fails the
bar; CLOSED FOR GOOD if it fails under DEEP too; CLOSED if it clears only under TOUCH (the fill-sensitivity row is
part of the verdict text); one-asset dependence read by LOAO 3/5 and the single-trade share." (contract :104-106)
READING: the rule of record is L-X.9's, adopted without change. `C(X)` = L-X.8's clauses (a) ∧ (b) ∧ (c) on book
X at the seed of record and the SCALPER bar; `D` = ONE-ASSET DEPENDENT on the TICK book (L-X.11: fewer than
`above_half_bar(N)` leave-one-asset-out panels exclude zero from above; "3/5" parsed from :106). Written over the
three fill books, all eight cells:

| TOUCH clears | TICK clears | DEEP clears | `verdict_of_record` | qualifier | named by the contract? |
|---|---|---|---|---|---|
| yes | yes | yes | `SUPPORTED` if not D · `NOT SUPPORTED` if D | — · `ONE-ASSET DEPENDENT (LOAO k/N)` | the positive case |
| no | yes | yes | as the row above | as above (TOUCH is not consulted when TICK clears; the row prints it) | no |
| yes | yes | no | `SUPPORTED` if not D · `NOT SUPPORTED` if D | `FILL-SENSITIVE (does not clear under DEEP)` · `ONE-ASSET DEPENDENT (LOAO k/N)` | no |
| no | yes | no | as the row above | as above | no |
| yes | no | yes | `NOT SUPPORTED` | — | "fails the bar" |
| no | no | yes | `NOT SUPPORTED` | — | "fails the bar" |
| yes | no | no | `NOT SUPPORTED — CLOSED` | `(clears only under TOUCH)` | "clears only under TOUCH" |
| no | no | no | `NOT SUPPORTED — CLOSED FOR GOOD` | — | "fails under DEEP too" |

- **One test.** m stays as parsed (:82); only the TICK book can produce `SUPPORTED` and only it spends the
  family's test. TOUCH and DEEP are ruled with the same ruler, seed, draws and bar and can only qualify or close.
- **The unnamed cells.** TICK clears and DEEP fails: the row stands, and says in its own cell that it does not
  survive a deeper fill. TICK fails and DEEP clears: the row fails and nothing is closed — a deeper book that
  clears is not evidence the idea is dead. TOUCH fails while TICK clears: possible because the books are
  sequenced separately (L-S.16); the word is TICK's and the fill-sensitivity row shows the inversion.
- **One-asset dependence** (the clause sits inside the kill; L-X.9 takes the reading that cannot flatter): where
  the TICK book clears but LOAO does not reach 3/5, the word is `NOT SUPPORTED · ONE-ASSET DEPENDENT`. Where the
  word is `SUPPORTED`, the verdict text carries the LOAO line `k/N` and the single-trade share of record (L-X.12).
  The share has no threshold in the contract or on file; it is printed and decides nothing.
- **The verdict text** = the cell (word, qualifiers, label) + the fill-sensitivity row (per rule: `n`, point,
  interval, `p_num/p_den`, `C(X)`) + the LOAO line + the single-trade share (L-X.9), followed by the per-order
  ladder counts of L-S.16.
- **What a closure forbids afterwards** — the standing lines the ledger append carries (L-X.32):
  - `NOT SUPPORTED`: nothing is closed. The 1h maker licence stands; a later tier may register another 1h
    value-area range trade, `pre_seen` on these bars.
  - `NOT SUPPORTED — CLOSED`: this trade form — a resting limit at the 1h value edge on the 5m clock — is closed
    under every fill model that requires a trade-through. It is not re-registered on backtest fills; the only
    reopening path is evidence about the fill itself (queue position or live fills), ruled in by the operator.
  - `NOT SUPPORTED — CLOSED FOR GOOD`: scalper mode on the 1h value area at the maker toll is closed in this and
    every later tier; no fill model reopens it (it fails at the most generous one), and the "maker" ruling's one
    use is spent. Only a new operator ruling naming a new mechanism reopens the 1h lens for range trading.
  - A `CLOSED BY PRECONDITION` row closes nothing beyond what its failed record already says.
SOURCE: contract :82, :104-106; L-X.8, L-X.9 (the six-case table, of which the eight rows above are the expansion
over TOUCH), L-X.11, L-X.12; TC11's R2 law ("a FAIL closes that lens … unless the toll model changes"), quoted in
`x_rec/tierc11x/REGISTRATION_PLAN.md:206-209`.
RIVALS: L-X.9's rivals (i)-(iii). LOAO as a qualifier on a `SUPPORTED` word — L-X.9 rival (ii); the brief for this
section allowed it and L-X's stricter reading is the one carried (OPEN TO OPERATOR 4).
FAILS-IF: L-X's F-VERDICT (LADDER leg, all sixteen combinations with D); here F-SCALP (o): the three arms' sidecars
do not carry `fill_rule` ∈ {tick, touch, deep} one each, or `scored` is not the TICK book. Planted mutation: the
TOUCH book shipped as `scored`.

**L-S.29 THE LABEL** — ruling O-23; "in-sample labels carried" (contract :130)
READING: P-SCALP-3 carries `pre_seen` and prints L-X.13's RE-SCORE template. The label's first clause says what
was seen and what was not: X printed the outcome of fading 1h value-area edges at the maker toll on these same
holdout bars — it is the licence row itself — and X3 printed 1h value-area swing-failure outcomes; this trade form
was never scored. Every scored bar is ≤ 2026-09-25T00:00Z (O-9), the instant X's standing ledger line names. The
"T tuning-fit" and "tuning-window L" labels of L-V ride on every row; on the holdout book both are out-of-sample.
The full text is in the REGISTRATION SPEC.
SOURCE: O-23; DISCLOSURES D-2, D-3; `x_rec/tierc11x/LEANS_X.md:1811-1818` (LX-X3.14), :2468-2470 (the standing
line); L-X.13.
RIVALS: no label (the contract carries none on this row) — O-23 rules it; the label cannot flatter.
FAILS-IF: L-X's F-REG (TEMPLATE leg); planted mutation: the template rewritten to the `selection_hazard` form.

---------------------------------------------------------------------------------------------------------------
### I · Outputs, fixtures, compute

**L-S.30 OUTPUTS** — "the scalper's fill-sensitivity and twins" (contract :128-129); "F-KEY" (:124)
READING:
- **`regbooks/P-SCALP-3/`** (L-X.24's interface): `STATUS.json`; arms `scored` (TICK · holdout), `ladder__touch`,
  `ladder__deep` (holdout), `strip`, `tierE__full_corridor`, `tierE__panel17`, `tierE__rr_unfiltered`,
  `tierE__live_edge`, each `<arm>.parquet` + `<arm>.json`. Sidecar: `ruler = "vs_zero"`, `era_scope`, `panel`,
  `lens = "5m"`, `toll = "maker_entry_targets__taker_stop"`, `fill_rule`. Rows: L-X.24's twenty columns
  (`symbol`, `entry_ms = open5[f]`, `entry_close_ms = close5[f]`, `direction`, `entry_px = L`, `stop_px`,
  `r_dist`, `exit_close_ms = close5[x]`, `exit_reason` ∈ {`stop`, `T2`, `time_stop`, `invalidation`,
  `corridor_end`}, `net_r`, `gross_r`, `fee_r`, `funding_r`, `haircut_net_r`, `era`, `lane = "scalp_va_1h"`,
  `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`, `taker_twin_net_r`) and, beside them: `trigger_close_ms`,
  `trigger_kind`, `also_cross`, `on_1h_close`, `edge_px`, `n_limit`, `t1_px`, `t2_px`, `t1_void`, `harvest_i`,
  `harvest_px`, `exit_i`, `exit_px`, `bars_held`, `T`, `time_stop_i`, `stop_on_fill_bar`, `gap_stop`,
  `both_touch_bars`, `fillbar_target_withheld`, `open_at_end`, `n_entry_fills` (always 1), `n_stop_moves`
  (always 0), `stop_px_at_exit`, `funding_r_uncapped`, `funding_ceiling_bound`, `funding_stamps`,
  `taker_twin_haircut_net_r`, the four regime columns, `licence`, the `T` and `L` labels.
- **`stage_s/`** (every parquet collared, keyed, stamped; `build_manifest.json`; `STAGE_S.md`;
  `FIXTURES_STAGE_S.txt`):

  | table | key | what |
  |---|---|---|
  | `S_orders_<book>` | `[book, symbol, trigger_close_ms]` | every order: the as-of row, the gates' values, the geometry in prices and ticks, the three fill bars, cancel / expiry, status, the permission-at-resolution flags, the regime columns |
  | `S_refusals_<book>` | `[book, symbol, trigger_close_ms]` | every trigger that did not become an order, with its reason |
  | `S_FUNNEL` (grid) | asset × direction × trigger kind × gate | counts surviving each gate, fill-rule independent |
  | `S_FILL_SENSITIVITY`, `S_REGIME`, `S_SLICES`, `S_MISS_GRID` (grids) | their axes | L-S.16, L-S.24, L-S.26, L-S.23 |
  | `S_miss` | `[symbol, trigger_close_ms, target]` | L-S.23 |
  | `open_at_w_continued` | `[symbol, entry_close_ms]` | L-S.25 |
  | `VA_STAMPS_scalp` | `[book, symbol, trigger_close_ms, instant_kind, instant_ms]` | the V5 vector (below) |

  Scored-window tables are stamped with the score edge, the strip with the pin (L-0.13); `as_of_lens = "5m"`.
- **The V5 stamps of the scalper's books** (contract :44-45 "every arm below"): through the reader's `stamp`
  (L-V.19, L-V.20). Declared instants per order: `arm` = the trigger close; `entry` = the fill (intrabar: the OPEN
  of its bar, with its close-stamped `entry_post_event` twin); `ev_t1` likewise; `exit` (stop or target: the open
  of its bar; a close event: its close) with `exit_post_event`; `expiry` / `cancel` for a miss; and `bar_close`
  = every 1h CLOSE between the trigger and the order's resolution — not every 5m close: no member of the vector
  can change between two 1h closes (the vector is a join of lens rows, L-V.20), so 5m rows would repeat the stamp
  before them. Captured columns, Tier-E, read by nothing.
- **The report** (L-X.28 §4) quotes: the verdict text; the three books' sidecars; `S_FILL_SENSITIVITY`,
  `S_MISS_GRID`, `S_REGIME`, `S_SLICES`, `S_FUNNEL` whole; the twins' beside-prints; pointers (path, sha, rows,
  key) to the per-order and per-trade tables.
- Every order and trade table is a per-trade or per-asset row file for L-L's ferry (contract :111).
SOURCE: L-X.24, L-X.26, L-X.28; L-0.13, L-0.15, L-0.16, L-0.21; L-V.19, L-V.20; contract :44-45, :111, :128-129.
RIVALS: a `bar_close` stamp at every 5m close (L-V.19's letter) — twelve identical rows per hour per open order.
FAILS-IF: the stage's instances of F-KEY, F-DET, F-COLLAR and F-GRID (L-0.20, L-0.21, L-0.16, L-0.15) on both
directories, and L-X's F-REGBOOK on the arms; planted mutations as those fixtures define, plus one here: an order
row whose `edge_px` is not the filed `val` / `vah` of its row (F-NOT's PIVOT-RANGE leg must go RED).

**L-S.31 F-SCALP** — "F-SCALP (3 scalps hand-walked end-to-end + 3 MISSES verified; fill rule ordering TOUCH ≥ TICK
≥ DEEP by n filled — an inverted order must FAIL)" (contract :119-121)
READING: suite `scripts/tierc12_scalp_fixtures.py`, L-0.14's harness and leg law (BREAK first; each plant caught by
its named detector; production against a fixture-typed second object). Sample rules are frozen HERE, before any
book exists. Key order = the home panel's order of record, then the instant ascending.

| leg | FAILS IF | planted mutations (each must turn it RED) |
|---|---|---|
| (a) HAND-3 | the three trades chosen by rule from the book of record — H1 the first with a T1 fill and a `T2` exit; H2 the first swing-failure trade exiting `stop` after its fill bar; H3 the first cross trade exiting `time_stop` (an empty class prints NONE-EXISTS, asserts its count is zero, and the next unchosen row in key order is walked instead; fewer than three trades in the book is RED) — re-derived END TO END by code sharing nothing with the builder (the raw 5m slice by explicit path; its own EMA loop from the tape's first bar; the filed 1h and 4h rows as data; `Fraction` tick arithmetic on the tick string; its own bar loop, fee and funding sums; every step printed) differ from production in any integer, string or price, or in any R figure by more than `HAIRCUT_TOL`. Verified beside by the same rule, where they exist: the first `invalidation`, the first stop on a fill bar, the first `t1_void` | the trigger bar shifted one bar; the limit snapped toward the market; the fill bar taken by TOUCH; T1 credited on the fill bar; maker booked on the stop |
| (b) MISS-3 | the three misses chosen by rule from the record's orders (holdout by trigger) — M1 the first `never_touched`; M2 the first `touched_not_through`; M3 the first miss in the direction opposite M1's (else the next in key order); beside: the first `cancelled` — are not misses under the fixture's own bar-by-bar TICK test of the whole window, or their class or any of their three would-have walks differs | a filled order listed as a miss; the window cut one bar short; the would-have entered at the limit |
| (c) LADDER | L-S.16's per-order inclusion, fill-bar order or per-ledger counts fail on any of the three ledgers | TICK and DEEP swapped ("an inverted order must FAIL"); TOUCH strict; DEEP without its floor on a constructed order |
| (d) TICK-FILL | L-S.9, L-S.11, L-S.15: production's snap and fill functions differ from `Fraction` brute force on the enumerated cases; a marketable limit exists | TICK as `≤`; float comparison; snap reversed; zero-volume fill |
| (e) ASOF | (e1) BOUNDARY (L-S.3) and the order rows ≠ the reader's `stamp`; (e2) PREFIX: orders with τ ≤ a seeded 4h close, rebuilt from tapes and filed rows cut at that close (fresh arrays, no memo), differ from the full run's; (e3) W≡PIN (L-S.25) | `side="left"`; row `k1 + 1`; an EMA seeded at the cut; an acceptance event read past the bound |
| (f) FROZEN | any level of any order differs from its recomputation from row `k1`, or changes between τ and the exit | the limit or a target re-read at the fill bar's row; ATR of the fill hour |
| (g) GATES · READ-SET | PERM (no 5m file), SETUP, both triggers, the run and its extreme, recomputed independently, differ; `S_FUNNEL` does not re-count; a path outside L-S.1's read set was opened | the 4h clause dropped; the lower bound of SETUP removed; `crossover` without its prior-bar clause; the extreme without the return bar; a 1h kline read |
| (h) SEQUENCE | L-S.14's overlap, identity or reason law fails | replace-with-newest; admission at an exit bar's close |
| (i) WALK-TABLE | synthetic 5m tapes, generated from the pins, drive every row of L-S.7's pattern cases, L-S.13, L-S.17, L-S.18, L-S.19, L-S.20 and L-S.11's void rule; production differs from the table | T1 before the stop; gap stop at the stop; invalidation ignored; the clock from `t`; the void rule removed |
| (j) STOP | L-S.10 | the rail removed; a stop move |
| (k) RR | L-S.12 | the test before the rail; the unfiltered book as record |
| (l) MISS-TABLE | L-S.23's partition and grid do not re-derive from `S_orders_tick` and `S_miss` | the split walk at maker rates; a miss dropped from the grid |
| (m) REGIME | L-S.24 | the window end at `k1 + 1`; a 4h column at the forming bar |
| (n) FLOW | L-S.2: a bent pin does not move its witness | a literal of equal value in a shadow builder (`PIN-NOT-READ`) |
| (o) VIEWS | L-S.25, L-S.26, L-S.28: arm identities, labels, `fill_rule` per arm | a home row altered in the 17-asset arm; TOUCH shipped as `scored` |
| (p) GATE | L-S.27 | the taker row; the ALL era; item 2 at X's rate |

"Hand-walked" means the fixture's derivation is printed step by step in the transcript, so a reader can follow
each of the six by eye; it is still a program, and it is the referee. The suite also runs this stage's instances of
F-KEY, F-DET, F-COLLAR, F-GRID and L-V's F-TRAV (a), (e) on the builder.
SOURCE: contract :119-121; L-0.14 (the harness; the hand-sample law: "the first row of each category in ascending
(asset, instant_ms) order (an empty category prints NONE-EXISTS and asserts the book's count of it is zero)");
X's F-SFP selection rule (`x_rec/tierc11x/LEANS_X.md:2309`); scout U6 C21, R-33.
RIVALS: samples picked after the book is seen — forbidden by L-0.14. The ladder leg on book totals — L-S.16.
FAILS-IF: as the table states, leg by leg.

**L-S.32 F-TOLL, THE BOOK HALF** — "F-TOLL (maker bps read, never typed; taker twin == TC-series)" (contract :121)
READING: L-D owns the data half and the reader half (L-D.21, L-D.31). The book half, in the same suite:

| leg | FAILS IF | planted mutations |
|---|---|---|
| (t1) NEVER TYPED | by AST, the builder's fee path (`fee_per_fraction`, the booking function and everything they call) holds a numeric literal outside the structural set, a bps or percent constant, or a rate not read from `E.fees()[stem]`; or the `fee_schedule` sha in any arm's sidecar is not the one `progress/TC12-D.json` certifies | a typed maker rate; `E.fees()` shadowed by a dict |
| (t2) TAKER TWIN == TC-SERIES | on every row of every arm, `taker_twin_net_r` and `fee_all_taker_r` differ from a FRESH `BK.account_l` call on the row's leg by more than `HAIRCUT_TOL`, or the per-fraction form at all-taker rates differs from it by more than `HAIRCUT_TOL`; or `E.fees()[stem]["taker_bps_side"]` is not the lineage's `FEE_BPS_SIDE` | the twin booked with a maker entry; a card other than the control card |
| (t3) LEGS | a row's maker / taker split is not L-S.21's table re-derived from `exit_reason` and `harvest_i`; `fee_maker_r + fee_taker_r ≠ fee_r`; `net_r ≠ gross_r − fee_r − funding_r`, each within the tolerance | maker on the stop; the time stop booked maker |
| (t4) FLOW | the maker rate bent at `E.fees()` inside production does not move `net_r` of a seeded sample by exactly the maker legs' notional × the bend ÷ R, or moves `taker_twin_net_r` at all | a shadow builder reading TC11's fee file; a cached rate |
| (t5) HAIRCUT | `haircut_net_r` or `taker_twin_haircut_net_r` differs from L-S.22's two laws | slippage on a maker leg; the charter tier of another asset |

SOURCE: contract :121; L-D.21 ("The BOOK half ("taker twin == TC-series") is L-S's"); LX-X2.11 (F-FEE-EQ);
`tc11x_sfp.py:780-792`; L-X.24.
RIVALS: bit-equality with `account_l` — unattainable (float association); the filed tolerance is the law.
FAILS-IF: as the table states.

**L-S.33 THE COMPUTE PLAN** — ruling O-5; "F-DET hash-identical" (contract :123)
READING:
- **Size (orientation, read at build):** a home 5m tape holds 625,152 to 741,097 bars at TC11's pin (scout U4
  §1.2) plus the top-up; the holdout to TC11's pin is 235,009 bars per asset as the scout counted it (U6 §1.9).
  Seventeen assets in the widest view.
- **Per asset, in one worker:** (1) the 5m frame once (six 8-byte columns over the tape) and the two EMAs
  (`ind.ema` is a Python loop: two passes over the tape); (2) `k1`, `k4` for every 5m bar by two `searchsorted`
  calls and the row gathers; (3) PERM, SETUP and both triggers as boolean masks over the whole tape — O(bars),
  vectorised, FILL-RULE INDEPENDENT; (4) geometry per candidate (exact `decimal` tick arithmetic, a Python step
  per candidate); (5) the walks: each order costs at most `V + T5` bar steps, so a walk is O(candidates × (V +
  T5)) Python steps and can never exceed O(bars) orders. Five walks share steps 1-4: TICK, TOUCH, DEEP,
  rr-unfiltered, live-edge; WALK-PIN repeats step 5 for the record rule over the strip.
- **No quantity of the plan depends on how many orders exist** — no count was taken while drafting.
- **Process law:** one `spawn` worker per asset, each importing `E` before any I/O; at most 6 workers while the
  1-minute load is below 10, else 2 (O-5); results merged in panel order, then key order, before any write; one
  5m tape per process (`BK._FRAMES`, keyed with the lens). Worker count and load go to `progress/TC12-S.json` only.
- **F-DET:** the whole stage twice, in fresh subprocesses under the two hash seeds of L-0.20, into `_det_stage_s/`;
  byte-identical parquet, sidecars, manifest and `STAGE_S.md`. Nothing in the stage draws a random number.
- **The stage's 5m reads** are declared for L-0's `FIVE_MIN_READERS_T`: TC12-S reads `klines/<stem>_5m.parquet`
  and `funding/<stem>.parquet` of the seventeen stems and no other snapshot file.
SOURCE: O-5; L-0.7, L-0.20, L-0.30; L-D.28 ("One tape per process"); `engine/indicators.py:17-28`; scout U4 §1.2,
U6 §1.9.
RIVALS: a bar-by-bar Python loop over every 5m bar — O(bars) interpreter steps per book where masks do it once.
A shared order census walked once for all rules — the books are sequenced separately (L-S.16).
FAILS-IF: F-DET on `stage_s/` and `regbooks/P-SCALP-3/`; planted mutations: a set-iteration line in a merge; a
worker count written into the manifest.

**Unverified at drafting — each checked at build, a HALT or a printed count:**
- UNVERIFIED: that the home 5m and 1h tapes stay gap-free through TC12's pin (Stage D's manifest `gap_count`).
  L-S.3's freshness guard, L-S.7's `run_cut_at_gap` and L-S.13's one-close assertion count any exception.
- UNVERIFIED: that every hand-sample class of F-SCALP (a), (b) has a member. An empty class prints NONE-EXISTS;
  fewer than three trades or three misses makes the leg RED and returns to the orchestrator.
- UNVERIFIED: that `TickGrid`'s floor / ceil take an exact `decimal` argument (L-S.11, L-S.15); INTERFACE.
- UNVERIFIED: that L-G files a per-4h-bar tide and breadth table before TC12-S starts (L-S.24); INTERFACE.
- UNVERIFIED: the maker rate (Stage D's capture), hence precondition item 2 and `deep_floor_binding`'s share
  under TC12's own tick capture.

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · P-SCALP-3

- **id:** P-SCALP-3
- **family:** SCALPER — the family header is contract :82, "STAGE S · SCALPER FAMILY (m=1, bar 0.10) — exists by
  the "maker" ruling:"; text of record :83-106 (slice sha `fa141ec5…2198`, L-X.17).
- **family_m:** 1 — parsed from :82 by L-X.1's `R_FAM` (group 3); never typed.
- **family_bar:** 0.10 — parsed from :82 (`bar 0.10`, group 4) and asserted equal to q ÷ m with q parsed from :9
  ("bar = 0.10 ÷ m per family"); at m = 1 the bar is on record and does not bind (L-X.8).
- **prior:** 30% — parsed from the text slice's `[30%]` (:83).
- **mechanism:** Inside a 1h value area that the 1h machine reports INSIDE, price that reaches the outer third
  near an edge tends to rotate back toward the POC and the far edge — the "edges respected" leg TC11-X licensed for
  the 1h lens at the maker toll and at no other. A limit resting AT the edge is the only entry that pays the maker
  fee, which is the only toll at which the 1h lens may trade a range. The 5m clock supplies timing and nothing
  else: an EMA cross toward value near the edge, or a failed 5m excursion beyond it. The trade is falsified by 1h
  acceptance beyond the faded edge and is bounded in time by the tuning-fit 1h traverse. The hazard is the fill
  itself — a resting limit is filled preferentially when price is going through it — so the row is judged on the
  book whose fills require a trade-through and is closed if it clears only when a touch is taken as a fill.
- **population:** the five home assets (L-D's home panel), pooled, both directions; lens of the clock 5m, lens of
  the value area 1h, permission from 1h and 4h; era HOLDOUT by the fill bar's close, `ERA_CUT < entry_close_ms`;
  scored window per O-9: `entry_close_ms ≤ W` and `exit_close_ms ≤ W` with `W` = TC11's pin
  (`research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`), a position open at `W` marked
  there as `corridor_end`; the bars in (W, TC12's pin] are the forward strip — ridden, printed, never scored
  [L-S.25].
- **arms:**
  - base arm: none (vs zero).
  - `scored` — the THROUGH-TICK book. Decision at a 5m close τ on row `k1` of `va_bars_1h` and row `k4` of
    `va_bars_4h`, the last lens bars with close ≤ τ [L-S.3]. PERMISSION: 1h `state == INSIDE` and 4h state neither
    UNDEFINED nor accepted against the direction (ACCEPTED_BELOW for a long, ACCEPTED_ABOVE for a short), read once
    at τ [L-S.4]. SETUP: the 5m close's %-of-value against the in-force 1h profile in [0, 33] for a long, [67, 100]
    for a short [L-S.5]. TRIGGER: the engine EMA12 / EMA89 of the 5m close crossing in the direction on that bar
    with the close within 0.25·ATR_1h of the edge on the value side, OR that close back inside value after the
    previous 5m close beyond the edge; a double trigger is a swing failure [L-S.6 … L-S.8]. ORDER: one unit at the
    edge snapped to the tick grid away from the market (a BUY limit floored, a SELL limit ceiled), all geometry
    frozen at τ; stop by `BK.brk_stop` from the limit — 0.5·ATR_1h beyond the swing failure's deviation extreme
    (every 5m low / high since the first close beyond, the return bar included), else from the limit, railed at
    1.0·ATR_1h (so R is exactly 1.0·ATR_1h on cross orders); T1 = POC and T2 = far edge − 0.25·ATR_1h on the grid,
    T1 void when it lies at or beyond T2; skipped unless the reward at T2 ≥ 1.5 × R; valid for bars t+1 … t+12;
    cancelled at a 1h acceptance on the faded side; one resting order and one position per asset, a trigger
    meanwhile refused, never a replacement [L-S.9 … L-S.14]. FILL: the first valid bar with `low < limit − 1 tick`
    (long) in exact integer ticks, at the limit price; no fill on a zero-volume bar [L-S.15]. WALK: on the fill bar
    the stop is tested and no target credited; then per 5m bar stop at the open, stop, T1 (half), T2 (the rest),
    and at the close invalidation at a 1h acceptance on the faded side, the time stop at the fill bar + the 1h
    traverse in 5m bars, the corridor end; targets fill by the same through-tick rule at their level; a stop fills
    at the stop, or at the open when the bar opens beyond it; no trail, no stop move, no add [L-S.17 … L-S.20].
    COST: maker bps on entry, T1, T2; taker on stop, time stop, invalidation and mark; funding by
    `BK.account_l`'s interval sum from the fill bar; `net_r = gross_r − fee_r − funding_r` in R [L-S.21].
  - `ladder__touch` — the same simulator with every resting limit filled on a touch (`low ≤ limit`), its own
    order sequence [L-S.15, L-S.16].
  - `ladder__deep` — the same with every resting limit filled only through by `max(0.05·ATR_1h, 1 tick)`, rounded
    up to whole ticks, its own order sequence [L-S.15, L-S.16].
- **statistic:** mean(`net_r`) of the `scored` book (L-X's common clause).
- **comparison:** vs zero. The bootstrap of record (O-22; L-X.3, L-X.4, L-X.6): whole-asset clusters,
  `tierc5.cluster_boot`, `N_BOOT` draws read from `research_outputs/tierc11/scores/SCORES.json["n_boot"]` (4000 on
  file), the 5th / 95th percentile interval of `tierc5._ci_from`, `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a
  Fraction, seed 20261008 (contract :4) passed explicitly, sensitivity seed 20260816 (`SCORES.json["seed_sens"]`)
  printed beside. The two ladder books are ruled with the same ruler, seed, draws and bar.
- **preconditions:**
  - {record: `research_outputs/tierc12/va/VA_MIRROR.json`, certified_by: `progress/TC12-V.json` `artifact_shas`,
    selector: `licence["1h|maker"].by_era["holdout"].would_read`, required: `"PASS"`} — X's filed word, mirrored
    from `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha256
    `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`).
  - {record: `research_outputs/tierc12/va/VA_MIRROR.json` with the maker pin of
    `research_outputs/tierc12/data/fee_schedule.json`, certified_by: `progress/TC12-V.json` and
    `progress/TC12-D.json` `artifact_shas`, selector:
    `licence["1h|maker"].by_era["holdout"].at_maker_pin.edge_net_h20`, required: `> 0`} — the licence row's edge
    leg re-derived at TC12's pinned maker round trip by the linear toll law of L-S.27.
  - If either is not met the row is closed by precondition: STATUS only, no arm, no number, cell
    `CLOSED BY PRECONDITION (<record>#<selector> reads <found>; required <required>) — no number · no test spent`,
    m and the bar unchanged.
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of
  the draws) > 0 AND (b) one-sided p <= q ÷ m = 0.10 ÷ 1 = 0.10, exact, AND (c) every declared asset holds at
  least one row in every arm the ruler reads; else NOT SUPPORTED (asset-cluster bootstrap by
  scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008; sensitivity seed 20260816 beside). m is
  fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number ·
  no test spent', spends no test and never loosens the bar. At m = 1 the bar does not bind and the bar cell prints
  '0.10 (not binding at m = 1; decided at the 5th percentile, clause (a))'. THE PRE-NAMED KILL (L-X.9, verbatim in
  content): C(X) = clauses (a), (b), (c) on book X ∈ {TOUCH, TICK, DEEP} at the seed of record and this bar; D =
  ONE-ASSET DEPENDENT on the TICK book (fewer than 3 of 5 leave-one-asset-out panels exclude zero from above,
  L-X.11). One test is spent; TOUCH and DEEP can never produce SUPPORTED. The verdict text is the cell followed by
  the fill-sensitivity row (per fill rule n, point, interval, p, C(X)), the LOAO line k/N and the single-trade
  share of record (no threshold; it decides nothing). Printed beside, deciding nothing: the sensitivity seed, the
  haircut and all-taker twins, the tuning and holdout slices, both single-trade shares, the literal-bar column,
  the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with
  VERDICT RESTS ON OPEN MARKS, the forward strip unscored. Tier-E arms carry no verdict word. This registration
  carries pre_seen and prints '<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)'. The six
  cases of the kill, exhaustive:
  - C(TICK) true · D false · C(DEEP) true · C(TOUCH) any → `SUPPORTED`
  - C(TICK) true · D false · C(DEEP) false · C(TOUCH) any → `SUPPORTED`, qualifier `FILL-SENSITIVE (does not
    clear under DEEP)`
  - C(TICK) true · D true · C(DEEP) any · C(TOUCH) any → `NOT SUPPORTED`, qualifier `ONE-ASSET DEPENDENT (LOAO
    k/N)`
  - C(TICK) false · D any · C(DEEP) true · C(TOUCH) any → `NOT SUPPORTED`
  - C(TICK) false · D any · C(DEEP) false · C(TOUCH) true → `NOT SUPPORTED — CLOSED`, qualifier `(clears only
    under TOUCH)`
  - C(TICK) false · D any · C(DEEP) false · C(TOUCH) false → `NOT SUPPORTED — CLOSED FOR GOOD`
- **labels:**
  - `pre_seen` — tag: none; label: `IN-SAMPLE RE-SCORE, NOT CONFIRMATORY`; text: "TC11-X printed outcomes of
    fading 1h value-area edges on these same bars — the 1h maker feasibility row this trade is licensed by (outer
    20% of value, H20 exit, both legs at X's assumed maker toll, holdout) and X3's 1h value-area swing-failure
    table — while this trade form (a resting limit at the 1h edge on the 5m clock, through-tick fill, split
    targets, taker stop) was never scored; X's standing ledger line marks any later value-area registration
    pre_seen for bars ≤ 2026-09-25T00:00Z and every scored bar of this row is at or before that instant; the
    feasibility word was earned on X's record machine, not on V2 (DISCLOSURES D-2, D-3); the lookback and the
    traverse are tuning-fit and out-of-sample on the holdout."; items:
    `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha `ea8573b3…b6f0`; row POOLED:CLASSIC5 ·
    holdout · va_regime · 1h · maker), `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha
    `a03ef134…91b0`; lens 1h, detector va, trade swing_failure), the standing line at :2468-2470 of
    `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md`, and `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:**
  - `ladder__touch`, `ladder__deep` — the contract's fill-sensitivity row: ruled at the family bar, part of the
    verdict text (L-X.9's named exception to the collar), no verdict word of their own.
  - the all-taker twin `taker_twin_net_r` (the TC-series toll) — Tier-E, no verdict word.
  - the charter-slippage twin `haircut_net_r` (AM-7, taker legs only) and `taker_twin_haircut_net_r` (AM-7 on
    every fill of the all-taker twin) — Tier-E, no verdict word.
  - `tierE__full_corridor` (five home assets, every era inside the scored window; lookback and traverse in-sample
    on its tuning rows) — Tier-E, no verdict word.
  - `tierE__panel17` (seventeen assets; CLASSIC5 pins transplanted; no licence for the twelve) — Tier-E, no
    verdict word.
  - `tierE__rr_unfiltered` (the book without the "rr-min" skip, re-walked) — Tier-E, no verdict word.
  - `tierE__live_edge` (the limit re-priced at the 1h close inside its window) — Tier-E, no verdict word.
  - the MISS table and grid (every unfilled order; the would-have at the trigger close as a taker, at T1, at T2
    and split) — Tier-E, no verdict word, never netted into a book.
  - the per-order ladder counts, the funnel, the regime-column occupancy and the descriptive slices (per asset,
    per direction, per trigger kind, triggers on a 1h close, void T1) — Tier-E, no verdict word.
  - `strip` (fills after TC11's pin through TC12's) — unscored: n and a pointer only.
  - L-X.14's common set (sensitivity seed, LOAO, both single-trade shares, literal bar, exact enumeration,
    month-block twin, drop-OPEN twin, tuning and holdout slices) — Tier-E, no verdict word.
- **failure_conditions:** F-SCALP legs (a) HAND-3, (b) MISS-3, (c) LADDER, (d) TICK-FILL, (e) ASOF, (f) FROZEN,
  (g) GATES · READ-SET, (h) SEQUENCE, (i) WALK-TABLE, (j) STOP, (k) RR, (l) MISS-TABLE, (m) REGIME, (n) FLOW,
  (o) VIEWS, (p) GATE [L-S.31]; F-TOLL book half (t1)-(t5) [L-S.32] with L-D's data and reader halves; L-V's
  F-TRAV (a), (e) and F-VA-PINS (e); L-0's F-NOT (5m SIGNAL SOURCE, TRAIL-OFFSET and ADDS, PIVOT-RANGE, 1W),
  F-CLOSURE, F-TYPED; the common F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET, F-COLLAR
  [L-X]. Each leg states its failure condition and its planted mutations in the reading cited.

### OPEN TO OPERATOR

1. **DEEP's floor.** The contract writes DEEP as "through by 0.05 ATR_1h" (:94-95). On part of the tape that is
   under one tick, where DEEP would be looser than the fill of record and "fails under DEEP too" would be read on
   a twin that is not deeper. DEFAULT if silent: DEEP = through by `max(0.05·ATR_1h, 1 tick)`, rounded up to whole
   ticks, with the share of orders where the floor binds printed per asset (L-S.15). The literal reading is the
   operator's to order; the per-order ladder assertion would then be dropped for the orders it breaks.
2. **A published maker rate at which the licence fails.** DEFAULT if silent: precondition item 2 (L-S.27) — if the
   licence row's edge leg, re-derived at Stage D's pinned maker round trip, is not above zero, P-SCALP-3 is CLOSED
   BY PRECONDITION and spends no test. O-19's minimum (print the difference beside the word and trade anyway) is the
   alternative only the operator can order.
3. **The 17-asset view** needs the twelve's 5m tapes, which Stage D's sentence does not list (:19-20) and which the
   snapshot carries under O-8. DEFAULT if silent: built from those tapes, Tier-E, every row of the twelve labelled
   as carrying no licence (L-S.26). "NA for the twelve" is the alternative.
4. **One-asset dependence.** L-X.9 reads the LOAO clause as part of the kill (a TICK book that clears but fails
   LOAO 3/5 reads NOT SUPPORTED); this section carries that rule. DEFAULT if silent: as L-X.9. Reading it as a
   qualifier on a SUPPORTED word is L-X.9's rival (ii), the operator's to name. The single-trade share has no
   threshold anywhere and decides nothing (L-X, OPEN TO OPERATOR 1).
5. **What CLOSED and CLOSED FOR GOOD forbid.** DEFAULT if silent: the three standing lines of L-S.28, carried into
   the ledger append. The operator may word a closure's reach differently before the freeze; after a verdict it is
   an amendment that cannot follow from the outcome.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

- **L-0 (laws / process).** The pin-map rows of L-S.2 (names, lines, `also` citations, veto tokens "outer-third",
  "validity", "fill", "rr-min", "era"), assembled into `pins/CONTRACT_PIN_MAP.json` at freeze; the `word_map` for
  "half" (:99). `tierc12_asof.asof_index`; `tierc12_units`; the harness and the hand-sample law (L-0.14); F-KEY,
  F-DET, F-COLLAR, F-GRID helper legs. One ordering constraint on L-0.10's parallel clause: TC12-S starts after
  L-G's per-bar tide and breadth table is COMPLETE-VERIFIED (L-S.24), so S is not fully parallel with G.
  `FIVE_MIN_READERS_T` holds TC12-S with the read set of L-S.33. The scalper's
  two `ema` call sites are the two lines of `tierc12_scalp.ema_pair`. F-NOT's columns for this book: `edge_px`
  (against the filed `val` / `vah`), `n_stop_moves`, `stop_px_at_exit`, `n_entry_fills`, and the VA-column list of
  L-S.1. **Class of the builder:** `scripts/tierc12_scalp.py` reads filed columns only. L-0.22 (at drafting) lists
  `tierc12_va_stamps.py` as a DOOR while L-V.2 files it as a data-only reader that is NOT a door; under L-V's text
  the scalper builder is a decision module that reads data, under L-0's it is a RUNNER using the reader's functions
  `bars`, `events`, `stamp`, `licence` (which must then be in `ACCESSORS_T`). Either classification builds; the
  assembly names one.
- **L-D (substrate / env).** `E.fees()[stem]` with `maker_bps_side`, `taker_bps_side`, `slippage_bps_side`;
  `E.ticks()`; `E.BK` (`tierc10_brk`: `frame_l` on "5m" with funding, `account_l`, `brk_stop`), `E.TP.CONTROL_CARD`,
  `E.LENS_MS`, `E.era_of`, `E.TC11_PIN_MS`, `E.PIN_MS`, `E.ERA_CUT_MS`, `E.load_asof_at`, `E.x_rec`; the home and
  17-asset panels by object. `TickGrid` (L-D.23) as specified, PLUS one thing L-D.23 does not state: that
  `floor_ticks` / `ceil_ticks` accept an exact `decimal.Decimal` (L-S.11's T2, L-S.15's DEEP depth). If L-D
  declines, the float `FAR − d·offset·ATR` in that operation order is passed and F-SCALP (d) counts every order
  where the exact rational result lands on another tick (required zero, else HALT for an amendment). The NO-TRADE
  default for zero-volume 5m bars (L-D.16) is adopted unchanged. `x_rec` rows this section reads:
  `tierc11x/exit/build_manifest.json`, `tierc11x/sfp/build_manifest.json`, `scripts/tc11x_pct.py`,
  `scripts/tc11x_sfp.py` (text, for the mirror's provenance). `TICK_GRID_AUDIT.json` is printed beside the fill
  tables.
- **L-V (value area).** `va_bars_1h` / `va_bars_4h` for all seventeen assets with the columns of L-S.1 (the
  in-force `val, poc, vah`, `atr`, `state`, `va_age`, `close_ms`); `va_events` acceptance rows with `side`,
  `known_close_ms`, `by`, `bars_out`, `E`; `TRAVERSE.json by_lens.1h.T_in_5m_bars`; the reader's `licence`. **Two
  additions asked of L-V:** (i) `VA_MIRROR.json` `licence[…].by_era[…]` carries the row's `edge_median_term_h20`,
  `edge_toll_atr`, `ratio_median` and the derived block `at_maker_pin {maker_bps_side, round_trip_bps,
  edge_toll_atr, edge_net_h20, ratio_median}` of L-S.27 (L-V.17 item 7 lists `would_read`, `verdict_pass`,
  `edge_net_h20`, `toll_bps`, `x_row` only); (ii) `instants_of` accepts the scalper's kind with L-S.30's instant
  law (`bar_close` at 1h closes, not at every 5m close). What L-V left to this section is decided here: the order
  geometry (L-S.3, L-S.9), the lens-close instant (L-S.3), the anchor of `T_in_5m_bars` (the fill bar, L-S.20),
  cancellation and invalidation on an `acceptance` event (L-S.13, L-S.19).
- **L-X (statistics / registrations / close).** L-X.9's table is carried verbatim in content; L-X.24's regbook
  interface, arm names, sidecar keys and fee identities are built to; the era of a row is its fill bar's close.
  **One difference for the reviser:** L-X.24's cross-arm law `n(ladder__touch) ≥ n(scored) ≥ n(ladder__deep)`,
  HALT `LADDER-ORDER`, is not a theorem — the three books are sequenced separately (L-S.16). The reading assumed
  here: the HALT is on the PER-ORDER counts each arm's sidecar carries (`n_orders`, `n_filled_touch`,
  `n_filled_tick`, `n_filled_deep`, asserted ordered on each ledger), and the arm totals are printed with the
  `BOOK-N-NOT-MONOTONE` disclosure. The verdict text's fill-sensitivity row still prints each arm's own `n`.
  L-X.10's precondition item is written for one record; item 2 of this row names two certified records until L-V
  files the derived block.
- **L-G (admission).** A filed per-4h-bar table for the seventeen assets carrying the tide age of record, its band
  and the breadth of record, keyed by asset and 4h bar close, COMPLETE-VERIFIED before TC12-S starts (as a dotted
  child of TC12-G if G's books follow later). L-S reads it by as-of for two regime columns and defines nothing
  about it. If L-G files only per-campaign values, the two columns are filed NULL with the reason and listed as a
  finding — never recomputed here.
- **L-R (range-state).** P-SFP-VA-1 shares the "rr-min" pin and three choices on which the two sections either
  agree or state the difference: the stop's price when a bar opens beyond it (here: the open), a T1 that lies at
  or beyond T2 (here: void), and the same-bar order (here: stop first, no open-first step for targets).
  P-SFP-VA-1's "maker twin" is L-R's; this section's fee mirror `fee_per_fraction` is the one function both may
  call.
- **L-C (control).** Nothing is read from the v6 book. The strip law (O-9) is applied as L-S.25 states.
- **L-L (ledger / era / ferry).** The ferry classes of `S_orders_*`, `S_refusals_*`, `S_miss`, the eight arms and
  `VA_STAMPS_scalp` (per-trade row files, CSV, 2 MB cap, held and listed past WARN).

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None against a ruling. O-9, O-14, O-17, O-19, O-20, O-22 and O-23 were checked against the files this section
cites and none was found wrong on a fact it rules. Three notes that are not objections:
- L-D's OBJECTION O-20 (the recorded tick is proven "stricter than history" only where the tape's granularity is
  not coarser than it) bears directly on the fill of record; this section builds under O-20 as written and prints
  the audit beside every fill table (L-S.15).
- O-9 defines the holdout by the ENTRY bar's close. An unfilled order has no entry bar; orders are era-tagged by
  the trigger close and trades by the fill close, and the at-most-one straddle per asset is counted (L-S.25).
- O-19 orders the maker-rate difference "printed beside" the licence word. L-S.27 item 2 does that and also makes
  the re-derived edge leg a precondition; the ruling does not forbid it, and it is listed for the operator (OPEN TO
  OPERATOR 2).
