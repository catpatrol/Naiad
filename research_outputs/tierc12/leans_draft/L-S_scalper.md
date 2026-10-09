## L-S · SCALPER FAMILY — P-SCALP-3, THE 1h VALUE-AREA RANGE TRADE, MAKER, ON THE 5m CLOCK

This section governs Stage S of the contract (lines 82-106) and the two fixtures the contract names for it: F-SCALP
(:119-121) and the BOOK half of F-TOLL (:121). It conforms to ORCHESTRATOR_RULINGS O-1..O-32. Nothing like this
walk exists on disk — no 5m EMA trigger, no order resting at a price away from a close, no tick-based fill, no
validity window longer than one lens bar, no MISS table, no target / stop / time-stop walk on the 5m clock (scout
U6 §1.1, §1.3, §1.7). The readings below are therefore the specification of a NEW simulator, clause by clause: the
row a 5m close may read; PERMISSION, SETUP and the two TRIGGERS; the order (a limit on the tick grid, geometry
frozen at the trigger, validity, cancellation, one order and one position per asset); the three fill rules in
integer ticks and the three books they make; the walk after the fill (same-bar order, invalidation, time stop); the
costs of record and the twins on every row; the MISS table; the regime columns; the population, the scored window,
the strip and the Tier-E views; the precondition; the pre-named kill as an exhaustive table; the outputs, F-SCALP,
F-TOLL and the compute plan. It owns ONE registered row, P-SCALP-3.

**Drafting record.** Read while drafting, all read-only: the contract (sha256 `861d6050…a7bd`); ORCHESTRATOR RULINGS
as they stood at R0; DISCLOSURES (`bd6987a2…1958`); scout maps U6 (`8315e351…bc4e`), U4 (`f700f842…1342`), U2
(`50109e8b…3aef`); the sibling drafts L-0, L-D, L-V and L-X as they stood (their reading ids are cited; where they
move, the owning section governs). Sources opened as TEXT: `engine/indicators.py`, `scripts/tierc10_brk.py`,
`tierc5_rules.py`, `tierc2_rules.py`, `tierc3_rules.py`, `tierc4_rules.py`, `tierc7.py`, `tierc9.py`,
`tierc10_census.py`, `tierc10_panel.py`, `tierc11_ride.py`, `tierc11_score.py`, `tierc11_env.py`; X's
`x_rec/scripts/tc11x_sfp.py` and `tc11x_pct.py`; X's `LEANS_X.md` (LX-1.1, LX-X2.4 … X2.12, LX-X3.14, :2462-2470);
TC11's `LEANS.md` (L-1.1 … L-1.4, L-S.1, L-S.2) and `LEANS_AMENDMENTS.md` (AM-7). Inspections, structural only: the
keys of `PINS_X.json`; the `constants` block of X's `exit/build_manifest.json` and the `laws` and `geometry` blocks
of X's `sfp/build_manifest.json` (the latter holds entry-time geometry quantiles and refusal counts of X2's pivot
book — no net R); the two 1h holdout rows of X's `va/feasibility.parquet` (the licence row and its taker sibling,
both already printed in DISCLOSURES D-2 and scout U2 §1.8); the five home ticks and one fee row of TC11's Stage D
records. No `tc11x_*`, `tierc10_*` or `tierc11_*` module was imported or run. NO outcome of any TC12 book was
computed, and no count of orders, fills or trades. Counts quoted from scout maps are orientation the build
re-reads, never inputs.

**Revision record (2026-10-09, before the freeze, before any book).** Revised once under the LEANS review
(`review/LEANS_REVIEW_2026-10-09.json`), ORCHESTRATOR_DISPOSITIONS OD-0..OD-19, `review/CROSS_SECTION_CANON.md`
(CANON-01..CANON-42) and rulings O-25..O-32. Opened again as TEXT for this pass: `scripts/tierc10_brk.py:851-954`,
`:1223-1326`, `:1366-1385`; `scripts/tierc5_rules.py:160-166`, `:481-502`; `scripts/tierc2_rules.py:115-127`;
`scripts/tierc11_score.py:258-266`; `scripts/tierc11_env.py:716-752`; X's `x_rec/scripts/tc11x_sfp.py:483-513`,
`:756-803`, `x_rec/scripts/tc11x_score.py:316-321`, `x_rec/scripts/tc11x_registrations.py:329-386`,
`x_rec/tierc11x/LEANS_X.md:1292-1316`. Inspections, structural only: the `pins.laws` keys of X's
`va/build_manifest.json`; the keys `vol_window`, `vol_floor` of X's `exit/build_manifest.json`; five keys of the
`laws` block of X's `sfp/build_manifest.json`; six sha rows of `X_REC_MANIFEST.json`; `n_boot` and `seed_sens` of
TC11's `SCORES.json`. No module of the frozen estate was imported or run; no outcome and no count of orders, fills
or trades of any TC12 book was computed; no reading was chosen by which would score better. Where a sibling
section's text and the canon differ, this section is built to the canon.

**Notation.** One asset, one book. `d` = +1 long, −1 short. 5m tape: bars `j` with `open5[j]`, `o,h,l,c,v`,
`close5[j] = open5[j] + STEP5`, `STEP5 = E.LENS_MS["5m"]`. `t` = the trigger bar, `τ = close5[t]` = the decision
instant, filed everywhere as `known_at_ms`. `G` = the frozen geometry of the order: `(VAL, POC, VAH, ATR)` read once
at τ (L-S.3). `EDGE` = the edge of interest (VAL for a long, VAH for a short); `FAR` = the other edge. `TICK` = the
tick of record; `n_X` = a price in integer ticks; `px(n)` = that grid price (`TickGrid`, L-D.23). `L` = the limit
price `px(n_L)` — the entry price `e` of the tier's one geometry law (L-S.11); `S` = the stop; `R = |L − S|`. `V` =
the validity in 5m bars; `T5` = the time stop in 5m bars; `Q` = the fraction sold at T1. `f` = the fill bar; `x` =
the exit bar. `W` = the score edge `E.TC11_PIN_MS` (O-9); `PIN = E.PIN_MS`; `ERA_CUT = E.ERA_CUT_MS`. `hi` = the
last 5m bar a walk may read. `T12` = `research_outputs/tierc12`. A BUY limit rests below the market (a long's
entry, a short's targets); a SELL limit rests above it (a short's entry, a long's targets). Formulas are written
for a long; "mirrored" means `d` flipped, VAL↔VAH, low↔high, floor↔ceil, `≤`↔`≥`. Where the mirror is not
mechanical it is written out.

---------------------------------------------------------------------------------------------------------------
### A · The stage, its inputs, its pins

**L-S.1 WHAT STAGE S BUILDS, AND FROM WHAT** — "STAGE S · SCALPER FAMILY (m=1, bar 0.10) — exists by the "maker"
ruling:" (contract :82); "P-SCALP-3 [30%] THE 1h VALUE-AREA RANGE TRADE, MAKER, ON THE 5m CLOCK" (:83)
READING:
- **Modules.** Builder `scripts/tierc12_scalp.py`; suite `scripts/tierc12_scalp_fixtures.py` (transcript
  `stage_s/FIXTURES_STAGE_S.txt`); records under `T12/stage_s/` and `T12/regbooks/P-SCALP-3/` (one writer script
  for both directories); progress record `progress/TC12-S.json` with `depends_on = [TC12-V, TC12-C.tide,
  TC12-R.sfp, TC12-ENV.score-build]`; commit subject `tierc12(TC12-S): …`. The stage starts only after `TC12-V`,
  `TC12-C.tide`, `TC12-R.sfp` and `TC12-ENV.score-build` are COMPLETE-VERIFIED (L-0.10): Stage V's filed tables;
  L-G's tide tables (L-S.24); `tierc12_rangewalk.fee_per_fraction`, which this builder imports (L-S.21); and
  `tierc12_regbook`, through which every arm is written (L-S.30).
- **The builder is a DECISION module with no exemption (O-29; L-0.22), an event simulator on each asset's 5m
  tape.** It reads value-area facts ONLY AS FILED DATA, through the data-only reader: it imports neither
  `analytics.value_area` nor `analytics.profile` nor a door (`scripts/tierc12_va.py`,
  `scripts/tierc12_va_trades.py`), computes no profile, runs no state machine, re-derives no lens STATE or EVENT,
  and holds none of the names L-0.22 forbids outside the doors (`volume_profile`, `value_area`, `va_series`,
  `va_machine`, `va_columns`, `va_traverse`, `va_coincidence`, `null_volume`). It compares 5m prices with filed
  LEVELS, which O-29 allows by name ("the scalper's 5m close against the 1h edge"). No 5m value area, range, pivot
  or tide exists (contract :89 "the 5m is never a signal source"; L-V.7 "5m is not a VA lens").
- **The production walk is PURE.** Explicit arrays in, rows out, no symbol-keyed memo inside: the stage hands it
  the asset's 5m `LensFrame` (`E.BK.frame_l(stem, "5m")`), the aligned volume array and the filed 1h / 4h rows;
  the as-of legs of F-SCALP (e) hand the SAME function a `E.BK.LensFrame` built on `E.load_asof_at(stem, "5m",
  cut)` and `E.load_funding_asof_at(stem, cut)` (fresh arrays) and the filed tables cut through the reader at the
  same instant (L-S.31). A walk reachable only through a memo could never be handed a cut tape.
- **Read set, per asset** (every path through the env `E`, L-D.25-28, the reader or a named door; it is what
  `stage_s/READ_SET.json` must hold, L-D.27):
  1. the 5m frame `E.BK.frame_l(stem, "5m")` (`open_ms, o, h, l, c`, the funding arrays; built once per process on
     the tape cut at PIN), and the `volume` column of the same file from `E.load_asof_at(stem, "5m", E.PIN_MS)`,
     asserted row-for-row aligned (`open_time == lf.open_ms`) before use — the snapshot files
     `klines/<stem>_5m.parquet` and `funding/<stem>.parquet` of the seventeen stems and no other snapshot file;
  2. Stage V's filed tables through the data-only reader `scripts/tierc12_va_stamps.py` (L-V.2; each file's sha
     asserted through `tierc12_progress.certified` before its first read): `bars("1h")`, `bars("4h")`,
     `events(lens="1h", kind="acceptance")`, `licence("1h", "maker", "holdout")` — the files
     `va/va_bars_1h.parquet`, `va/va_bars_4h.parquet`, `va/va_events.parquet`, `va/VA_MIRROR.json`;
  3. the traverse through the fitted-pin door, `tierc12_va_stamps.traverse("traverse.1h.in_5m_bars")` (and
     `traverse("traverse.1h")` for the header check of L-S.2) — the file `va/TRAVERSE.json` (L-V.18);
  4. `E.fees()[stem]` and `E.ticks()[stem]` (L-D.19, L-D.22); `data/TICK_GRID_AUDIT.json`, printed beside the fill
     tables (L-S.15); the contract pins through `scripts/tierc12_pins.py`;
  5. L-G's tide tables `tide/tide_bars_4h.parquet` and `tide/breadth_4h.parquet`, filed at `TC12-C.tide` (regime
     columns only, L-S.24), each sha asserted through `certified()`;
  6. X's records through `E.x_rec`, for the header checks of L-S.2 and the trailing rank of L-S.24:
     `tierc11x/exit/build_manifest.json`, `tierc11x/sfp/build_manifest.json`, and `scripts/tc11x_pct.py` as text
     (two literals by `ast`).
  The builder opens NO 1h or 4h kline file: `ATR_1h` is the filed column `atr` of `va_bars_1h` (L-V.24: "THE FILED
  VALUE IS THE VALUE OF RECORD"). It opens no table under `va/trades/` or `va/stamps/`.
- **The value-area columns this builder reads — the complete typed list** (declared for L-V's F-VA-PINS (e) and
  L-0's F-NOT, and carried verbatim in the REGISTRATION SPEC): from `va_bars_1h`: `close_ms`, `state`, `val`,
  `poc`, `vah`, `atr`, `va_age`; from `va_bars_4h`: `close_ms`, `state`; from `va_events`: `lens`, `kind`, `side`,
  `known_close_ms`, `by`, `bars_out`, `E` (rows selected by the key column `asset`). Read beside, deciding nothing:
  `inside_frozen_only` of `va_bars_1h` (one printed count, L-S.4) and `l_label` of `va_bars_1h` (the lookback's
  label, carried on every order row and in every arm's sidecar `description`, L-S.29). No 12h, 1d or 1w column.
  The V5 stamps of the scalper's books are not this builder's: L-V's reader files them at `TC12-V.stamps.s`
  (L-S.30) and this builder never opens them.
- **Two rides of every book on one tape** (L-D.28: "A look-back is an INDEX BOUND on that tape"): WALK-W with `hi =
  hi_W` = the last 5m bar with `close5 ≤ W` makes every scored, ladder and Tier-E arm; WALK-PIN with `hi = hi_PIN` =
  the last bar with `close5 ≤ PIN` makes the strip rows of every ridden arm and the order ledgers the stamps read
  (L-S.25, L-S.30). Each ride covers the asset's whole corridor up to its bound in ONE pass (one-order /
  one-position state is carried across the era cut).
- **Order of acts:** (1) the precondition gate (L-S.27): the builder calls `licence("1h", "maker", "holdout")`
  before anything else — if not met, `regbooks/P-SCALP-3/STATUS.json` only and stop; (2) the gates and geometry of
  every candidate (L-S.3 … L-S.12), fill-rule independent; (3) the rides.
SOURCE: contract :82-83, :89; O-29; L-0.10 (the sub-stage table and the start law), L-0.22, L-0.30 (5m SIGNAL
SOURCE; `FIVE_MIN_READERS_T`), L-D.27 (`READ_SET.json`), L-D.28, L-V.2, L-V.24; `scripts/tierc10_brk.py:851-954`
(`LensFrame`, a dataclass of explicit arrays; `frame_l`: lens-generic, accepts "5m" — `LENS_MS = dict(D.STEP_MS)`
:137) [read here]; scout U6 §1.0, §1.1.
RIVALS: a builder importing a door — forbidden: O-29. `ATR_1h` recomputed from the 1h klines at full float — two
values of record for one quantity (L-V.24). X's `tc11x_sfp.walk` vendored — its clock is the trade's own lens bar
and its entry is a close; it cannot rest an order (scout U6 §1.1).
FAILS-IF: L-0's F-CLOSURE (a scalper copy importing `analytics.value_area` inside a function body → its AST leg
RED; a shadow builder with a run-time lazy door import, run as a subprocess → exit 70 at its exit leg) and F-NOT
leg 5M (a third `ema` site → RED; a 5m kline path in a directory's `READ_SET.json` outside `FIVE_MIN_READERS_T` →
RED); here F-SCALP (g) READ-SET: `stage_s/READ_SET.json` holds a path outside the read set — a snapshot path other
than the 5m kline and the funding file of the seventeen stems, a path under `va/` or `tide/` other than the files
of items 2, 3 and 5, an `x-rec` path other than the three of item 6 — or its `licence_reads` is not the one call
`("1h", "maker", "holdout")`; planted mutation: a 1h kline read planted in a shadow builder.

**L-S.2 THE PINS THIS SECTION CONSUMES** — "no number typed that a file can supply" (contract :8)
READING: every constant below is read at run time from the named source; where the contract's value also stands on
file the two are asserted equal by the pin door or by the builder's header check (a HALT). "Value" is orientation.
Pin names are L-0.17's names of record.

| pin | read at run time from | asserted equal to | value | flow witness when bent at its door |
|---|---|---|---|---|
| `scalp.third_long_max`, `scalp.third_short_min` | contract :87 (pin door); `also` :136 `"outer-third" (33/67)`, each by its `group` | — (no file states this pair) | 33, 67 | the SETUP mask |
| `scalp.ema_fast`, `scalp.ema_slow` | contract :89 "EMA12/EMA89" | `E.R2.WINDOW_FAST`, `E.R2.WINDOW_SLOW` (`scripts/tierc2_rules.py:115-116`) | 12, 89 | the cross bars |
| `scalp.trigger_prox_atr` | contract :90 "within 0.25 ATR_1h" | — | 0.25 | the proximity mask |
| `scalp.validity_bars` (V) | contract :92; `also` :136 `"validity" (12 five-minute bars)` | — (NOT the lens ratio; see below) | 12 | the expiry bar of an order |
| `scalp.fill_ticks` (`n_tick`) | contract :94 "by ≥ 1 tick"; `also` :136 `"fill" (through by 1 tick)`; consumers TC12-S and TC12-R (P-SFP-VA-1's maker twin fills by the same rule, OD-11) | — | 1 | the fill bar of an order (collides with the structural set: held by the FLOW leg alone, L-0.17) |
| `scalp.deep_atr` | contract :94-95 "DEEP (through by 0.05 ATR_1h)" | — | 0.05 | `n_D` of an order |
| `scalp.stop_beyond_atr` | the lineage object `E.R2.STOP_BUF_ATR` (`scripts/tierc2_rules.py:127`), read inside `E.BK.brk_stop` | contract :97 "0.5 ATR_1h beyond"; X's `sfp/build_manifest.json` `laws.stop_buf_atr` | 0.5 | the stop of a swing-failure order |
| `scalp.rail_atr` | contract :98 "railed ≥ 1.0 ATR_1h", passed as `rail_atr=` | `E.R3.MIN_STOP_ATR` (`scripts/tierc3_rules.py:148`); X's `laws.rail_atr` | 1.0 | every cross order's stop (collides with the structural set: FLOW leg) |
| `scalp.t1_fraction` (Q) | the lineage object `E.TP.CONTROL_CARD.harvest_frac` (read inside `E.BK.account_l` and handed to the fee function) | contract :99 "half" (pin door `word_map`); `E.R4.HARVEST_FRACTION` (`scripts/tierc4_rules.py:202`); X's `laws.harvest_frac` | 1/2 | `net_r` of a T1-then-stop trade |
| `scalp.t2_offset_atr` | contract :99 "far edge − 0.25 ATR_1h" | X's `laws.t2_atr_off` | 0.25 | `n_T2` of an order |
| `rr_min` | contract :73 (pin door); `also` :100 and :135-136 `"rr-min" (1.5 at T2)` — ONE pin for both range rows, shared with L-R; `scalp.rr_min` is not a name | — | 1.5 | the skipped set |
| `scalp.era` | contract :83 "HOLDOUT era"; `also` :137 `"era" (scalper scored on holdout)` | sidecar `era_scope` | holdout | the scored arm's row set |
| `traverse.1h.in_5m_bars` (`T5`) | `tierc12_va_stamps.traverse("traverse.1h.in_5m_bars")` → `(value, source)`, the fitted-pin door (L-V.2, L-V.18) | the value of `traverse("traverse.1h")` × (`E.LENS_MS["1h"] // E.LENS_MS["5m"]`) | fitted at TC12-V | the bar of a time-stop exit |
| `fee.maker_bps_side.<VENUE>`; the taker and charter rates | `E.fees()[stem]` keys `maker_bps_side`, `taker_bps_side`, `slippage_bps_side` (L-D.19, L-D.21, L-D.26 hunk 4) | taker == `E.R2.FEE_BPS_SIDE` (`scripts/tierc2_rules.py:122`) | per Stage D | `net_r` of every scored row (F-TOLL [book t4]) |
| tick | `E.ticks()[stem]` (a string; L-D.22) | `data/CONTRACT_SPECS.json` `assets[].price_tick` | per asset | the limit of an order |
| the fee band `G` (a flag, never a refusal) | `E.R2.FEE_BPS_ROUND_TRIP` (`scripts/tierc2_rules.py:123`) | — | the lineage's | the flag `t1_within_fee_band` of a constructed order at the band's edge |
| trailing window, floor (regime column) | X's `exit/build_manifest.json` `constants.vol_window`, `constants.vol_floor` through `E.x_rec` (sha asserted against its manifest row) | the AST literals `WINDOW`, `FLOOR` of `x_rec/scripts/tc11x_pct.py` (:48-49) | 2000, 300 | the tercile of a bar |
| R tolerance | `HAIRCUT_TOL`, read by `ast` from `scripts/tierc11_score.py:264`, node sha pinned (L-0.24) | — | 1e-12 | — |
| `PCT_PER_UNIT`, `BPS_PER_UNIT` | `scripts/tierc12_units.py` (L-0.17) | — | 100, 10000 | — |

`scalp.validity_bars` (a contract pin, vetoable as "validity") and the lens ratio `E.LENS_MS["1h"] //
E.LENS_MS["5m"]` (an object, inside `T5`) are two different quantities that share a value today; neither is read
where the other belongs, their equality is a GUARD and never a HALT (L-S.13), and F-SCALP (n) bends each
separately.
SOURCE: contract lines as cited; L-0.17 (the doors, the pin register, the allow-list, "THE LIMIT", the FLOW leg),
L-0.23 (the veto tokens: `outer-third` names the two thirds rows, `rr-min` names `rr_min`, `maker-bps` names every
`fee.maker_bps_side.<VENUE>`); the lineage objects at the lines cited [read here]; X's two manifests (`constants`,
`laws` keys) [read here]; L-V.18; L-D.19, L-D.22; OD-8 (the fee band is a flag).
RIVALS: read 0.5 / 1.0 / half from the contract and pass them into a re-implemented stop — not taken: the estate's
stop function is called as it is and the contract values are asserted equal to what it reads. Type the window and
floor of the trailing rank — forbidden.
FAILS-IF: F-SCALP (n) FLOW: each pin above, bent at its door inside production, must move its witness on the
synthetic tapes of leg (i), which are generated so that every witness exists — else `PIN-NOT-READ`; planted
mutation: a shadow builder holding a literal of equal value in place of `scalp.validity_bars` (the bend moves
nothing → RED). L-0's F-TYPED and F-PINS hold the rest.

---------------------------------------------------------------------------------------------------------------
### B · The decision at a 5m close

**L-S.3 THE ROW A 5m CLOSE READS** — "at the last 1h close" (contract :85); ruling O-14
READING: a decision is taken only AT a 5m close τ. Per asset the builder holds the arrays of `bars("1h")` and
`bars("4h")` sorted by `close_ms` and computes, for every 5m bar,
`k1 = asof_index(close_ms_1h, τ)` and `k4 = asof_index(close_ms_4h, τ)` with the ONE implementation
`tierc12_asof.asof_index` (L-0.28: `searchsorted(closes, τ, side="right") − 1`): the last lens bar whose CLOSE ≤ τ.
A 1h (4h) bar closing exactly at τ IS that row; a bar still forming is never read.
- **Everything the decision uses about the 1h lens is row `k1` of `va_bars_1h`, as filed:** `state` (the machine
  after bar `k1`), and the profile IN FORCE at τ — `val, poc, vah` = `VA(k1)` — with `atr = ATR_1h[k1]` (L-V.20,
  L-V.24). Those four numbers are the order's frozen geometry `G`. From the 4h lens only `state` at row `k4` is
  read.
- **Freshness.** `0 ≤ τ − close_ms_1h[k1] < E.LENS_MS["1h"]` and `0 ≤ τ − close_ms_4h[k4] < E.LENS_MS["4h"]` are
  required (no missing lens bar between the row and τ); otherwise no decision is taken at τ and the bar is counted
  (`stale_1h`, `stale_4h`). `k1 = −1` or `k4 = −1` is UNDEFINED and takes no decision. A bar that takes no decision
  is not a trigger and is no row of the refusal table (L-S.14).
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
FAILS-IF: F-SCALP (e1) BOUNDARY: per home asset, at the first 1h close of the holdout and at the last 1h close at
or before `W` (a rule, no draw), production's as-of must read the row of the bar closing at τ, and one 5m bar
earlier the previous row; and at every order's τ the order row must equal the reader's `stamp()`. Planted
mutations inside production: `side="left"`; the row taken at `k1 + 1` (the forming hour). The filed in-force block
itself (`val, poc, vah, atr` of row t = `VA(t)`, `ATR[t]`) is held at Stage V by L-V's F-VA-ASOF [d FILED-ROW
PREFIX] and [e IDENTITY] and by F-VA-RAW [c]; this section's as-of legs lean on them and re-run no door (L-S.31).

**L-S.4 PERMISSION** — "PERMISSION: 1h state INSIDE (no probe/acceptance at the last 1h close) AND the 4h state NOT
accepted against the planned direction." (contract :85-86)
READING: at τ, for planned direction `d`:
`PERM(d) = (state_1h[k1] == "INSIDE") AND (state_4h[k4] ∉ {"UNDEFINED", AGAINST(d)})`, with
`AGAINST(+1) = "ACCEPTED_BELOW"`, `AGAINST(−1) = "ACCEPTED_ABOVE"` — P-DIR-1's own parenthesis, "accepted below
for a long; above for a short" (contract :66). State names are L-V.2's `STATE_NAMES`; the filed `state` is read,
never re-derived from levels (O-29; L-V.24).
- 1h PROBING or ACCEPTED on EITHER side, or UNDEFINED, denies permission in both directions.
- 4h PROBING (either side), 4h INSIDE and 4h ACCEPTED WITH the direction permit. 4h UNDEFINED denies (it cannot
  occur in the holdout on a home asset; it is counted in the full-corridor and 17-asset views).
- **Evaluated ONCE, at the trigger close.** It is not re-evaluated while the order rests or at the fill. The
  contract names exactly one way a resting order dies before expiry — "cancelled on acceptance beyond the edge"
  (:92-93, L-S.13) — and a permission-lapse cancel would be a second, unnamed one. What the rival would do is
  printed, deciding nothing: per order `perm_1h_at_resolution`, `perm_4h_at_resolution` (PERM re-read at the last
  lens close at or before the open of the fill bar, or of the expiry bar for an unfilled order) and their counts.
- **Counted, deciding nothing:** the orders whose row `k1` carries `inside_frozen_only` — the hour resolved a
  probe and reads INSIDE by the probe's frozen edge while its close lies outside the rolling `[val_j, vah_j]`
  (L-V.13; declared against the contract's letter in the dated amendment AM-1, L-V.15). PERMISSION reads the filed
  `state` there as everywhere; `n_inside_frozen_only` is printed per asset and direction beside the order counts,
  so a reader sees how often a permitted hour closed outside the rolling value.
- PERMISSION is a pure function of (τ, d, the two filed tables): F-NOT's 5M leg (d) recomputes it in a process
  that opens no 5m file.
SOURCE: contract :66, :85-86; O-29; L-V.13 (the state column; its three counted consequences; the per-bar flag
`inside_frozen_only`), L-V.15, L-V.20; L-0.30 leg 5M (d).
RIVALS: "INSIDE" re-derived as `val ≤ c ≤ vah` — loses PROBING versus resolved and flips at 6-dp edges (L-V.24).
4h "not accepted against" read as "4h INSIDE" — stricter than the text. Re-check at the fill — see above.
FAILS-IF: F-SCALP (g) GATES: the fixture's own recomputation of PERM for every order and every refused trigger,
from the two filed tables alone, differs on any row; or `n_inside_frozen_only` does not re-count from the filed
column. Planted mutations: the 4h clause dropped; `AGAINST` swapped between the directions; the 1h state read at
`k1 − 1`.

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
production's trigger bars; (e2) ACT-BOUNDARY PREFIX: on a tape cut at a sampled order's `known_at_ms` the EMA
values and the trigger set at bars ≤ the cut differ from the full tape's. Planted mutations: the EMA computed on a
tape that starts at the era cut (an EMA seeded at the cut); `crossover` without the prior-bar clause; the
proximity taken with the absolute value.

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
rulings O-20, O-27
READING:
- **The edge** is `EDGE` of `G`: the filed 6-dp `val` (long) / `vah` (short) of row `k1` (`edge_px`; F-NOT's
  PIVOT-RANGE leg holds it equal to the in-force `val` / `vah` of `va_bars_1h` row `k1`).
- **The limit sits on the tick grid, snapped AWAY from the market**, by `TickGrid(E.ticks()[stem])` (L-D.23):
  long (a BUY limit) `n_L = floor_ticks(VAL)`; short (a SELL limit) `n_L = ceil_ticks(VAH)`; `L = px(n_L)`. One
  snapping law for every resting limit in this section — the entry, T1 and T2: **a BUY limit is floored to the
  grid, a SELL limit is ceiled**, so no resting order is easier to reach than its raw level. `snap_ticks = |EDGE −
  L| / TICK ∈ [0, 1)`, formed in the grid's decimal context, is filed per order.
- **The ENTRY limit is never marketable against the price that placed it.** By SETUP `d·(c5[t] − EDGE) ≥ 0` and by
  the snap `d·(EDGE − L) ≥ 0`, so `d·(c5[t] − L) ≥ 0`. The builder asserts it in ticks (long: `floor_ticks(c5[t]) ≥
  n_L`; short: `ceil_ticks(c5[t]) ≤ n_L`) and HALTs otherwise. A trigger pattern whose close is beyond the edge is
  not an order (L-S.6's counted class). The claim is the entry's alone: a TARGET is placed when the entry fills
  and can stand at or behind the market at that instant — that case is counted, never credited early (L-S.17).
- **Frozen of record.** `G`, hence `L`, the stop, both targets and `R`, are fixed at τ and never re-read — not at
  the next 1h close, not at the fill, not after it. Nothing set at or after a bar can know that bar (scout U6 H4
  (ii)). The re-rolled-edge reading is the Tier-E twin `tierE__live_edge` (L-S.26).
- The order's size is one unit; nothing is added (L-0.30: no adds).
SOURCE: contract :92; O-20, O-27; L-D.22, L-D.23 ("The module defines NO fill rule, no snapping direction and no
order model: L-S states those"); X's frozen-edge law (LX-X2.4, LX-X2.5: targets "frozen at entry"; the live far
side "as of the bar's OPEN" a twin); scout U6 R-3, R-6, H6.
RIVALS: the raw edge as an off-grid price — no real order. Snapping TOWARD the market — an easier fill at a better
price than the edge: it flatters. A live limit following each re-rolled VA — the twin.
FAILS-IF: F-SCALP (d) TICK-FILL: `n_L` differs from a `Fraction` floor / ceil of the filed edge over the tick
string on any order, or `d·(EDGE − L) < 0`, or an entry limit is marketable against its trigger close; (f) FROZEN:
any level of an order differs from its recomputation from row `k1` alone. Planted mutations: the snap direction
reversed; `L` recomputed from the row of the fill bar.

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
  prints the count of cross orders and the count of `rail_binding`; the dead clause is listed for the operator
  (OPEN TO OPERATOR 7). On a swing-failure trigger `R = max(|L − EXT| + 0.5·ATR, 1.0·ATR)`: never smaller than a
  cross order's.
- `S` is a float level, not snapped to the grid: it is a stop-market trigger, tested by the lineage's comparison
  (L-S.18), and no tick rule in the contract names it.
- **No stop move, ever** (:100 "NO trail"): `S` is constant from τ to the exit; no breakeven after T1. The trade
  row carries `n_stop_moves` (always 0) and `stop_px_at_exit == stop_px` for F-NOT's TRAIL-OFFSET leg.
- `st is None` (a non-finite or non-positive ATR) → no order: the trigger is REFUSED with the reason `stop_none`,
  the first clause of the geometry law (L-S.11).
SOURCE: contract :97-98, :100; `scripts/tierc10_brk.py:1366-1385`; `scripts/tierc5_rules.py:481-502`;
`tierc2_rules.py:127` (0.5), `tierc3_rules.py:148` (1.0) [read here]; X's use (`tc11x_sfp.py:496`); OD-19; scout
U6 C9, R-11.
RIVALS: distances from the raw edge instead of the limit — the entry is the limit; R is measured from where the
position is. The rail dropped on cross triggers so that 0.5 ATR "means something" — contradicts "railed ≥ 1.0";
it is the operator's to order, by name (OPEN TO OPERATOR 7). A stop snapped to the grid — a rule nobody wrote,
with no unflattering direction.
FAILS-IF: F-SCALP (j) STOP: any order's `S`, `R` or `rail_binding` differs from the fixture's own arithmetic on the
filed row and the raw extreme; a cross order with `R ≠ rail·ATR`; a trade whose stop moved. Planted mutations: the
rail removed; a cross order's `ext` set to the trigger bar's low; a breakeven move after T1.

**L-S.11 THE TWO TARGETS, AND THE TIER'S ONE GEOMETRY LAW** — "TARGETS: T1 = POC (half, resting limit, same fill
rule); T2 = far edge − 0.25 ATR_1h (remainder)" (contract :99); disposition OD-8
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 17] exact tick expressions are formed under `decimal.localcontext(grid.ctx)` — `TickGrid.ctx` as L-D.23 names it; an inexact quotient raises and is a HALT.
READING: both targets are resting limits placed when the entry fills, on the grid by L-S.9's snapping law, levels
from `G`:
- **T1:** the POC of the frozen profile. Long (a SELL limit) `n_T1 = ceil_ticks(POC)`; short `n_T1 =
  floor_ticks(POC)`. Size `Q`.
- **T2:** raw level `FAR − d·t2_offset_atr·ATR`, formed EXACTLY in `decimal` from `dec(FAR)`, `dec(ATR)` and the
  pin's fraction and handed to the grid as an exact `Decimal` (L-D.23: `floor_ticks` / `ceil_ticks` take a `float`
  or a `decimal.Decimal`, the latter used exactly as given): long `n_T2 = ceil_ticks(·)`; short `n_T2 =
  floor_ticks(·)`. Size = everything still open (X's law, LX-X2.5: "The remainder (0.5, or the whole position if T1
  has not filled) rests at T2").
- **The geometry law is the tier's one law for both range rows (OD-8; L-R.14 writes it for P-SFP-VA-1), here in
  integer ticks with the entry price `e = L`.** A trigger that has passed the one-order test (L-S.14) is REFUSED
  and counted, BEFORE the reward test, with the first reason that holds:
  (1) `stop_none` — the stop function returns none (L-S.10);
  (2) `poc_not_ahead` iff `d·(n_T1 − n_L) ≤ 0` — the POC is not ahead of the limit; a target AT the entry price is
  no target (the contract's "toward the POC", :70, has no object; the trade is never reversed);
  (3) `t2_not_ahead` iff `d·(n_T2 − n_L) ≤ 0`.
  These three hold in EVERY book, `tierE__rr_unfiltered` included: an order whose target is not ahead is not an
  order.
- **Not refusals.** `t1_void` := `d·(n_T2 − n_T1) ≤ 0` — the POC lies at or beyond T2, price reaches T2 first, no
  T1 order exists and the WHOLE position exits at T2; filed and counted. That is what two resting orders do; it is
  not a filter. `t1_within_fee_band` := `0 < d·(px(n_T1) − L) ≤ (G / BPS_PER_UNIT)·L` with `G =
  E.R2.FEE_BPS_ROUND_TRIP` — the trade is taken as written, the flag is filed and counted, and `fee_band_r = (G /
  BPS_PER_UNIT)·L / R` is printed. There is no fee band and no inverted-targets refusal: X's `t1_within_10bps`,
  `t2_within_10bps` and `targets_inverted` are not carried; the contract's only skip is "rr-min" (L-S.12).
- Filed per order: `t1_px`, `t2_px`, `t1_r = d·(t1_px − L)/R`, `t2_r = d·(t2_px − L)/R`, `r_atr = R/ATR`,
  `t1_void`, `t1_within_fee_band`, `fee_band_r`; the quantiles of the three ratios are printed.
- Both target fills use the book's own fill rule (L-S.15) and book the LIMIT price — no gap improvement (L-S.18).
SOURCE: contract :70, :99, :100; OD-8; L-R.14; L-S.9; L-D.23; LX-X2.5, LX-X2.6 (`x_rec/tierc11x/LEANS_X.md`);
`x_rec/scripts/tc11x_sfp.py:483-513` (X's `geometry`: `thr = REFUSAL_BPS / BPS_UNIT * e` and the reasons
`stop_none`, `t1_within_10bps`, `t2_within_10bps`, `targets_inverted`) [read here]; `scripts/tierc2_rules.py:123`;
scout U6 C10, R-12, R-16.
RIVALS: X's fee-band and inverted-targets refusals — not taken on the record (OD-8: the contract's only skip is
rr-min); L-R prints X's law as `tierE__x_geometry` on P-SFP-VA-1, and this row ships no such arm. A T1 at the
entry price traded as written, half sold at the entry for two maker fees — not taken: OD-8 (one law for both
range rows; the POC must be ahead). T1 kept resting when it lies beyond T2 and credited before T2 on a bar that
reaches both — books a price the position could not have reached with size left. Targets filled at `max(level,
open)` — a resting maker order books its own price.
FAILS-IF: F-SCALP (d): `n_T1`, `n_T2` differ from the `Fraction` arithmetic; (k): an order of record whose POC or
T2 is not ahead of its limit, or a refusal row whose reason is not the first that holds; (i) WALK-TABLE rows "POC
beyond T2" (the whole unit must exit at T2 and no T1 fill may exist) and "POC at the limit" (no order;
`poc_not_ahead`). Planted mutations: the T2 offset taken with `ATR_1h` of the fill hour; the void rule removed; a
constructed trigger with the POC at the limit admitted; a `t1_void` trigger refused.

**L-S.12 "rr-min"** — "Minimum reward at T2 ≥ 1.5 × stop ["rr-min"]." (contract :100)
READING: evaluated at τ, on the grid prices, AFTER the rail and after the geometry law of L-S.11: with `t2_r =
d·(px(n_T2) − L) / R`, the trigger is SKIPPED iff `t2_r < rr_min` (float64, that operand order — the tier's one
comparator for both range rows, OD-8), reason `rr_min`: no order exists, the asset stays free, and the trigger is
a row of the refusal table with its `t2_r`. With the rail, every placed order has T2 at least `rr_min · rail`
ATR_1h from the limit. The book WITHOUT this skip is the Tier-E twin `tierE__rr_unfiltered`, RE-WALKED with its
own order sequence (L-S.26): it drops this test and nothing else — the geometry refusals of L-S.11 stand in it —
so the twin differs from the record by the rr-min test alone on orders that can exist.
SOURCE: contract :73-74 ("or the trade is skipped ["rr-min"]; the unfiltered twin printed"), :100, :135-136; OD-8.
RIVALS: reward measured from the trigger close — the entry is the limit. Tested at the fill — a look at the fill
bar. The twin as a filter-off subset of the same orders — the skipped triggers would have blocked later ones;
X's ridden twins re-walk (`tc11x_sfp.py:167-168`). The twin with the geometry refusals dropped too — it would hold
orders that cannot exist (a sell limit at or below the entry booked as a maker fill), which makes the filter look
better than the test alone warrants.
FAILS-IF: F-SCALP (k) RR: an order of record with `t2_r < rr_min`; a skipped trigger with `t2_r ≥ rr_min`; a
trigger filed under `rr_min` that fails the geometry law first; the unfiltered twin, substituted for the book of
record, must turn the leg RED. Planted mutation: the test taken before the rail.

**L-S.13 VALIDITY AND CANCELLATION** — "valid 12 five-minute bars from the trigger close, cancelled on acceptance
beyond the edge ["validity"]" (contract :92-93)
READING:
- **Validity window:** the `V` bars `t+1 … t+V` BY INDEX on the 5m tape. The trigger bar itself has closed and
  cannot fill. A zero-volume bar is one of the V (L-D.16). If unfilled after bar `t+V` the order EXPIRES at
  `close5[t+V]`. A window that runs past `hi` and is unfilled by `hi` is `unresolved_at_end` — neither a fill nor a
  miss.
- **Cancellation.** "Acceptance beyond the edge" = a V2 `acceptance` event of the 1h lens on the faded side
  (`side == "bottom"` for a long, `"top"` for a short; L-V.14) with `τ < known_close_ms ≤ close5[t+V]`, read from
  the filed `va_events` rows — no acceptance test is re-implemented here (O-29). The order is CANCELLED at that
  close: let `q` be the 5m bar with `close5[q] == known_close_ms`; bars `> q` are not tested; bar `q` itself IS
  tested (an intrabar fill precedes the close), and an order filled on `q` is then invalidated at that same close
  (L-S.19).
- **What can happen inside the window.** IF `V·STEP5 == E.LENS_MS["1h"]` (a guard, never a HALT) THEN, on a
  gap-free tape, exactly one 1h close lies in the window and every cancellation is asserted `by == "margin"`,
  `bars_out == 0`, `E == edge_px`; ELSE no such assertion is made and every cancellation is filed with its `by`,
  `bars_out` and `E`. Why the assertion holds under the guard: with PERM true no probe is pending at `k1`, so the
  only acceptance that can print at the window's one 1h close is by MARGIN on a probe's first bar (L-V.10), judged
  against the edge of `VA(k1)` — the order's own raw edge. In either branch every cancelled order files the
  event's `by`, `bars_out` and `E`; a cancellation the assertion does not cover (the guard false, or a gap on the
  5m or the 1h tape inside the window) is counted apart (`cancel_other`) and listed.
- A lapse of PERMISSION that is not such an acceptance does not cancel (L-S.4).
SOURCE: contract :92-93, :136; O-29; L-V.10, L-V.14; L-D.16; scout U6 R-7.
RIVALS: bars `t … t+V−1` — the trigger bar is closed. A private acceptance test of 1h closes against the order's
limit — a second state machine inside a decision module; the machine is Stage V's. Cancel on any 1h close beyond
the edge (a probe) — the contract says acceptance. The guard written as a HALT — the flow leg's own bend of
`scalp.validity_bars` would trip it, and a vetoed "validity" would be unbuildable.
FAILS-IF: F-SCALP (i) WALK-TABLE rows "fill on bar t+V", "no fill by t+V → expired", "acceptance at the window's
1h close → cancelled", "fill and acceptance on one bar → filled, then invalidated"; (l) the status partition; (n):
with `scalp.validity_bars` bent the build must complete and file every cancellation with its `by`, `bars_out` and
`E`. Planted mutations: the window shifted to `t … t+V−1`; cancellation ignored; a fill accepted on bar `t+V+1`.

**L-S.14 ONE POSITION AND ONE RESTING ORDER PER ASSET; THE ORDER OF TESTS** — "five home assets; both directions"
(contract :84); the contract is silent on concurrency
READING: per (asset, book) at most one order rests and at most one position is open, across both directions.
- At each 5m close `j`, in this order: (1) bar `j` is processed for the live order or position (fill, exit,
  expiry, cancellation); (2) a trigger at `close5[j]` passes the ONE-ORDER TEST iff, after (1), no order is alive
  AND no position was open during any part of bar `j`; (3) a trigger that passes it is put to the geometry law
  (L-S.11) and then to the reward test (L-S.12), and becomes an order iff it passes both.
- **A trigger while an order rests is REFUSED and counted (`refused_order_resting`); the resting order is never
  replaced, re-priced or stacked.** An order alive after `close5[j]` (unfilled, `j < t+V`, not cancelled) refuses.
- **A trigger while a position is open is refused (`refused_position_open`)** by the lineage's law: for a
  position filled on bar `f` and exited on bar `x`, every trigger at a close `j` with `f ≤ j ≤ x` is refused — the
  fill bar's close and the exit bar's close included, after an intrabar exit as after a close exit (`replay9`'s
  `ti <= open_until`; X's `blocks`).
- An order that EXPIRES or is CANCELLED at `close5[j]` is dead at that close and no position existed during bar
  `j`: a trigger there may place a new order (valid from `j+1`).
- **The reason filed is the first that holds, in this order:** `refused_order_resting` / `refused_position_open`,
  then `stop_none`, `poc_not_ahead`, `t2_not_ahead`, then `rr_min`. These six are the reason slugs of record of
  `S_refusals_<book>.reason`. A trigger refused by the geometry law or skipped by "rr-min" leaves the state
  unchanged: the asset stays free. A 5m close that took no decision (L-S.3: stale or undefined rows) is not a
  trigger; it is counted per asset and is no row of the refusal table.
- Every trigger that did not become an order is a row of `S_refusals_<book>` with its reason; the identity
  `n_triggers == n_orders + Σ reasons` is asserted per asset and book. The count of holdout triggers refused by an
  order or position born at or before the era cut is printed (at most one per asset).
SOURCE: `scripts/tierc9.py:389-393` (`if ti <= open_until: reject "position_open"`); `tc11x_sfp.py:870-874`
(`blocks`), LX-X2.9; OD-8 (the refusals come after the one-order test and before the reward test); scout U6 C22,
R-23.
RIVALS: replace-with-newest (counted as `refused_order_resting`, the number of times it would have acted). One
order per direction — two resting orders on one asset. Re-entry at the close of an intrabar exit — X's counted
rival, not the lineage's law.
FAILS-IF: F-SCALP (h) SEQUENCE: two orders or positions of one asset and book overlap in bars; the identity fails;
a refusal row's reason is not the first that held at that close. Planted mutations: replace-with-newest; a trigger
admitted at an exit bar's close.

---------------------------------------------------------------------------------------------------------------
### D · Fills

**L-S.15 THE FILL OF RECORD AND ITS TWO TWINS, IN INTEGER TICKS** — "FILL OF RECORD: a later 5m bar trades THROUGH
the limit by ≥ 1 tick (low < limit − tick for a long) ["fill"]. Twins printed: TOUCH (low ≤ limit) · DEEP (through
by 0.05 ATR_1h)." (contract :93-95); rulings O-20, O-27, O-32
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 17] exact tick expressions are formed under `decimal.localcontext(grid.ctx)` — `TickGrid.ctx` as L-D.23 names it; an inexact quotient raises and is a HALT.
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
- **DEEP's depth (O-32):** `n_D = max(ceil_ticks(deep_atr · ATR_1h[k1]), n_tick)`, the product formed exactly in
  `decimal` and handed to `ceil_ticks` as an exact `Decimal` (L-D.23), frozen at τ. The contract writes "through
  by 0.05 ATR_1h"; on part of the tape that is less than one tick (scout U6 §1.9: on 18.25% of NEAR's holdout
  hours at TC11's capture, 0.17% of ZEC's, 0.04% of SOL's), where DEEP as written would be LOOSER than the record.
  The floor at `n_tick` makes DEEP never shallower than the record, so that **for every order DEEP-filled ⇒
  TICK-filled ⇒ TOUCH-filled, and the fill bars satisfy `fill_i_touch ≤ fill_i_tick ≤ fill_i_deep`** — by
  arithmetic, not by luck. `deep_floor_binding` (the floor was the larger term) is filed per order and its share
  printed per asset (OPEN TO OPERATOR 1).
- **Fill price = the limit, `px(n)`,** under all three rules and for all three resting limits (entry, T1, T2),
  whatever the bar's open. A resting order books its own price; when a bar opens beyond it the maker is filled at
  the limit and is immediately under water — which is the adverse selection the row is testing.
- **The fill bar** of a rule is the first bar of the window (L-S.13) on which the rule's test holds.
- **A bar with `volume == 0` fills no resting limit under any rule** (L-D.16's NO-TRADE default, adopted): no trade
  printed. Stops, invalidation and the time stop are evaluated on it as on any bar. The number of orders whose
  window held such a bar is printed.
- **The tick** is TC12's own capture applied to the whole corridor (O-20, L-D.22). Beside every fill table the
  build prints `data/TICK_GRID_AUDIT.json`'s on-grid shares and any `coarser_than_recorded_tick` month for the
  asset and segment (O-27 bears here: "stricter than history" is claimed only where the tape's observed
  granularity is not coarser than the recorded tick, and "never looser" is carried UNVERIFIED until that prints).
- **One fill rule for every maker leg in the tier (OD-11):** P-SFP-VA-1's conditioned maker twin fills by this
  same through-tick test (L-R.24), which is why `scalp.fill_ticks` names TC12-R among its consumers (L-S.2).
SOURCE: contract :93-95, :136; O-20, O-27, O-32; L-D.16, L-D.22, L-D.23 (the integer comparisons; a `float` or an
exact `Decimal` accepted); X's trade-through law (LX-1.1 (ii): "A touch that does not trade through is not a
fill"); scout U6 C2, C3, R-2, R-4, H5, H7.
RIVALS: `low ≤ limit − tick`; float `l < L − tick` (mis-decides exact-boundary lows, the common case on an on-grid
tape); DEEP as written (inverts the ladder on NEAR, and the kill would read "fails under DEEP too" on a twin that
is not deeper); a per-era tick inferred from the tape (L-D.22).
FAILS-IF: F-SCALP (d) TICK-FILL: production's three tests, on the fixture's enumerated cases (each home tick ×
lows / highs on-grid, one finer decimal place above and below, the exact boundaries `n`, `n ∓ n_tick`,
`n ∓ n_tick ∓ 1`, `n ∓ n_D`), differ from brute-force `Fraction` comparisons; a zero-volume bar fills. Planted
mutations: TICK written as `l ≤ limit − tick`; a float comparison; DEEP without the floor (the inclusion leg (c)
must go RED on a constructed order with `deep_atr·ATR < TICK`); a fill on a zero-volume bar.

**L-S.16 THREE BOOKS, AND THE INCLUSION PER ORDER** — "F-SCALP (… fill rule ordering TOUCH ≥ TICK ≥ DEEP by n filled
— an inverted order must FAIL)" (contract :120-121); "the fill-sensitivity row is part of the verdict text" (:105);
ruling O-32, disposition OD-6
READING:
- **Three books, one simulator.** `scored` (TICK, the book of record), `ladder__touch` and `ladder__deep` (L-X.24's
  arm names) are three walks that differ ONLY in the fill rule, applied to the entry and to both targets ("same
  fill rule", :99). Each walk has ITS OWN one-order / one-position sequence (L-S.14) — the law of X's ridden twins
  — because an order filled under one rule occupies the asset and changes which later triggers become orders.
- **Therefore the ladder is asserted PER ORDER, not on book totals.** Every order row of every book carries all
  three entry tests evaluated on that same order: `fill_i_touch`, `fill_i_tick`, `fill_i_deep` (null if none in
  the window). Asserted on every order of all three ledgers: `fill_i_deep` non-null ⇒ `fill_i_tick` non-null ⇒
  `fill_i_touch` non-null, and `fill_i_touch ≤ fill_i_tick ≤ fill_i_deep` where present.
- **The ladder law (per order, O-32).** Each of the three ladder-class sidecars (`scored`, `ladder__touch`,
  `ladder__deep`) carries `n_orders`, `n_filled_touch`, `n_filled_tick`, `n_filled_deep` — the three entry tests
  evaluated on THAT arm's own order ledger: its WALK-W orders with `ERA_CUT < known_at_ms ≤ W` (the holdout by
  trigger, inside the scored window; a fill counts when its bar closes at or before `W`). `n_orders ≥
  n_filled_touch ≥ n_filled_tick ≥ n_filled_deep` follows from the per-order inclusion and is asserted on every
  one of the three; the scorer HALTs `LADDER-ORDER` otherwise (L-X.24's `LADDER-ORDER` is on these per-ledger
  counts). This is the contract's "TOUCH ≥ TICK ≥ DEEP by n filled", on a common set of orders, where it is a
  theorem.
- **Book totals are printed and are NOT a theorem:** the arm totals `n(ladder__touch)`, `n(scored)`,
  `n(ladder__deep)` are the row counts of three separately sequenced books; a touch-only fill can block triggers
  the record would have traded. They are printed in the fill-sensitivity row beside the per-order counts and are
  not ordered by law; when they are not ordered the row's `disclosures[]` carries `BOOK-N-NOT-MONOTONE` — a
  disclosure, never a HALT and never a qualifier.
- An order's status in a book is by that book's rule: `filled` (at `fill_i`), `expired`, `cancelled`,
  `unresolved_at_end`. A MISS of a book = `expired` or `cancelled` in that book.
- `S_FILL_SENSITIVITY` (a grid, whole, keyed by `cell`): book × `panel` (each home stem and `POOLED`) × trigger era
  × direction → `n_orders, n_filled_touch, n_filled_tick, n_filled_deep, n_expired, n_cancelled, n_unresolved,
  n_deep_floor_binding, n_window_zero_volume`, on the WALK-W ledgers. Counts only. The fill-sensitivity block of
  `STAGE_S.md` prints beside it, per arm of the regbook, `n` and the count of rows with `funding_ceiling_bound`
  (L-S.21).
SOURCE: contract :93-96, :105, :120-121; O-32; OD-6; L-X.9 (the three fill books; "ladder" arms), L-X.24;
`tc11x_sfp.py:167-175` (RIDDEN twins "re-walk their own events with their own one-position sequence"); scout U6
H14 ("… inclusion must be asserted on ORDERS (per trigger), before one-position sequencing, or it will not hold").
RIVALS: (a) the ladder twins as the record's orders re-filled, overlaps allowed — two positions on one asset in a
book that claims one. (b) the same, overlaps refused — neither a faithful book under the rule nor a common order
set. (c) the count ordering asserted on book totals — not guaranteed, so a HALT on it can fire with no defect
(OD-6).
FAILS-IF: F-SCALP (c) LADDER: an order with a deeper fill and no shallower one, or with fill bars out of order;
a sidecar's four counts out of order, or not re-counted from its ledger. Planted mutations — "an inverted order
must FAIL": the TICK and DEEP tests swapped inside production; TOUCH tested with `<`; DEEP's depth computed from
the fill hour's ATR. L-X's F-REGBOOK holds the scorer's side (the TICK and DEEP counts swapped in a sidecar copy →
`LADDER-ORDER`).

**L-S.17 THE FILL BAR** — "a later 5m bar trades THROUGH the limit" (contract :93); X's fill-child law
READING: on the fill bar `f` the entry books at `L`, and then, on that same bar:
- **the stop is tested** (L-S.18 steps 1-2): the path that traded through the limit may have gone on to the stop.
  A stop on the fill bar is a full-unit loss on bar `f` (`stop_on_fill_bar`, counted);
- **no target is credited**: a sell order cannot rest before the buy fills, and the bar does not show the order.
  The bars on which the book's target test holds on `f` are counted (`fillbar_target_withheld`); T1 and T2 rest
  from bar `f+1`;
- **a target can be at or behind the market when it is placed:** `target_marketable_at_placement = d·(c5[f] −
  px(n_T)) ≥ 0`, counted per target (filed as `t1_marketable_at_placement`, `t2_marketable_at_placement`). Such a
  target is still filled only by the book's test on a later bar and only at its level;
- the close events of L-S.18 apply (invalidation at `close5[f]`; the corridor end if `f == hi`); the time stop
  cannot fall on `f`.
The position's clock, its funding and its `entry_ms` / `entry_close_ms` are bar `f`'s (L-S.20, L-S.21, L-S.25).
SOURCE: LX-1.1 (ii) (`x_rec/tierc11x/LEANS_X.md:590-597`: "The STOP is tested on it, adverse-first … Targets are
never credited on the fill child"); `tc11x_sfp.py:686-712`; scout U6 R-15, H6.
RIVALS: targets live on the fill bar — credits a path the bar cannot order. The stop not tested on the fill bar —
hides the worst case of a maker fill. A target that is marketable at placement filled at once at the close of
`f` — a taker act booked at the maker rate, at a price better than its level.
FAILS-IF: F-SCALP (i) WALK-TABLE rows "fill bar reaches T1 → withheld", "fill bar reaches the stop → stopped on
f", "fill bar closes beyond T1 → flagged, filled later at the level"; planted mutations: a T1 fill on `f`; the
stop skipped on `f`.

---------------------------------------------------------------------------------------------------------------
### E · The walk after the fill

**L-S.18 SAME-BAR ORDER ON A 5m BAR — THE TIER'S ONE WALK LAW** — the contract is silent; "taker on the stop"
(:101); "NO trail" (:100); disposition OD-9
READING: one law with P-SFP-VA-1 (OD-9; L-R.19 writes it on the 4h bars). Each 5m bar `j ≥ f` is stepped once, on
what is still open, in this order (`adv` / `fav` = the bar's adverse / favourable extreme: `l[j]` / `h[j]` for a
long, mirrored for a short), with L-S.17's fill-bar rules on `j = f`:

| step | test | act |
|---|---|---|
| 1 · STOP at the open | `d·(o[j] − S) ≤ 0` | exit ALL at `o[j]` (the worse price); reason `stop`; `gap_stop = True` |
| 2 · STOP, adverse-first | `d·(adv − S) ≤ 0` | exit ALL at `S`; reason `stop`; `both_touch` counted if a target test holds on this bar; `stop_bar_open_through_target` counted if the bar opened at or beyond a resting target |
| 3 · T1 (resting, not void; `j > f`; never on a zero-volume bar) | the book's fill rule at `n_T1` on `fav` (L-S.15) | the fraction `Q` exits at the LEVEL `px(n_T1)`; `gap_t1 = True` iff the bar opened at or beyond the level — no gap improvement is booked |
| 4 · T2 (`j > f`; never on a zero-volume bar) | the book's fill rule at `n_T2` on `fav` | the rest exits at the LEVEL `px(n_T2)`, reason `T2`, on the same bar as T1 if reached; `gap_t2` likewise |
| 5 · close events | INVALIDATION (an acceptance close on the faded side, L-S.19), then TIME STOP (`j == f + T5`), then CORRIDOR END (`j == hi`) | exit the rest at `c[j]`; reason `invalidation` / `time_stop` / `corridor_end` (a mark) |

- **Stop first, unconditionally — the pessimistic rule.** There is NO open-decides-first step for a target: the
  stop is tested before any target on every bar, and a bar that reaches the stop and a target is a stop for
  everything still open.
- **The stop's price.** A stop is a taker market exit: when the bar OPENS at or beyond the stop it is filled at
  the open (the worse price), otherwise at the stop. The stop test is the lineage's float comparison
  `d·(price − S) ≤ 0`.
- **The targets' price.** T1 and T2 are resting MAKER limits booked at their grid price; a bar that opens beyond a
  target still books the level, never the open.
- Nothing sequences inside a 5m bar: it is the finest clock in the snapshot's scope (1m tapes are out of scope,
  L-D.27).
- The three close events share a price; their order fixes the LABEL only.
- The step is this builder's own function (its targets are resting limits tested in integer ticks). It imports
  from `tierc12_rangewalk` only `fee_per_fraction` (L-S.21) and never passes L-R's declared switches
  `gap_law="x_record"` or `law="x"`, whose AST-typed call sites are L-R's two.
SOURCE: OD-9; L-R.19; LX-X2.10 (`x_rec/tierc11x/LEANS_X.md:1292-1316`: the record's steps 0-3 and its
symmetric-gap twin; "The record's gap law favours the trader on both sides (targets collect the gap; the stop
ignores it)", :1308-1310) [read here]; `tc11x_sfp.py:571-601` (`bar_step`); `scripts/tierc7.py:186-189` (the
lineage's stop booking); scout U6 R-14.
RIVALS: X's record law (the open decides first for stop and targets; a stop books its own price even when the bar
opens beyond it; a target books `max(level, open)`) — not taken on the record: OD-9; by X's own note it favours
the trader on both sides. L-R prints it as `tierE__x_gaplaw` on P-SFP-VA-1; this row ships no such arm and counts
the bars instead (`gap_stop`, `gap_t1`, `gap_t2`, `stop_bar_open_through_target`). Targets before the stop —
optimistic.
FAILS-IF: F-SCALP (i) WALK-TABLE: a synthetic 5m tape drives every row of this table and the rows of L-S.13 and
L-S.17; production's (exit bar, price, reason, T1 fill, flags) must equal the table's. Planted mutations: T1
tested before the stop on a both-touch bar; a gap stop booked at the stop price; a target credited at `max(level,
open)`; T2 denied on the bar T1 filled.

**L-S.19 INVALIDATION** — "invalidation on acceptance beyond the edge regardless of stop." (contract :98)
READING: while a position is open, a V2 `acceptance` event of the 1h lens on the faded side (`bottom` for a long,
`top` for a short) with `close5[f] ≤ known_close_ms` EXITS everything still open at the close of the 5m bar that
ends at that instant, at that bar's 5m close price, as a TAKER, reason `invalidation` — after the bar's intrabar
steps, and whether or not the stop was touched ("regardless of stop"). The event is read from Stage V's filed
`va_events`; no acceptance test is re-implemented here (O-29). If no 5m bar closes at that instant (a gap) the
exit is the first 5m bar closing after it, counted.
- On a bar where the stop is also reached the stop is booked (L-S.18's step order), so `invalidation` labels only
  the exits the stop did not take: the hour closing beyond the edge N times with the stop untouched, a margin
  acceptance inside a far swing-failure stop, a margin acceptance after the ATR has contracted. Printed:
  `n_invalidation` by the event's `by` and by `trigger_kind`.
- **The lens's edge can have moved.** The trade's edge is frozen at τ (L-S.9) while the lens re-rolls its value
  area at every 1h close, so an acceptance after the first hour can be beyond another price than the one faded —
  for a long, a re-rolled VAL above the entry, which exits in profit under this label. The reading is forced (no
  trade-local acceptance test may exist, O-29), so it is made visible: each invalidation row files
  `inval_event_E` (the event's frozen edge) and `inval_edge_moved = (inval_event_E != edge_px)`; printed:
  `n_invalidation` by `inval_edge_moved` and by the sign of `d·(exit_px − L)`.
- The price of the exit is the 5m tape's close, not the 1h tape's (the venue's intervals can disagree on incident
  bars, scout U4 H11); the number of invalidation bars where the two differ is printed.
SOURCE: contract :72-73, :98; O-29; L-V.10, L-V.14 (the event's `E`); TC11 `LEANS.md:458-459` (L-S.2: "Exit at that
1h close (the coincident 5m close), taker"); X's `TAKER_EXITS` (`tc11x_sfp.py:148`); scout U6 C11, R-28.
RIVALS: the first 1h CLOSE beyond the edge (a probe) — the contract says acceptance. Exit at the next bar's open —
the event is known at the close and the filed precedent exits there. An acceptance test of 1h closes against the
trade's own frozen edge — a second state machine in a decision module (O-29); the count by `inval_edge_moved`
shows what it would have separated.
FAILS-IF: F-SCALP (i) rows "count acceptance with the stop untouched → invalidation at that 5m close",
"acceptance and stop on one bar → stop", "acceptance beyond a re-rolled edge → invalidation, `inval_edge_moved`";
(a) covers a real one if the class exists. Planted mutations: invalidation ignored; the exit booked at the stop.

**L-S.20 THE TIME STOP, NO TRAIL, THE CORRIDOR END** — "TIME STOP = the 1h traverse (V4); NO trail." (contract :100)
READING:
- `T5` = the tuning-fit 1h value-area traverse (O-18, L-V.18) in 5m bars, the factor being the lens ratio by
  object. It is read through the fitted-pin door: `(T5, source) =
  tierc12_va_stamps.traverse("traverse.1h.in_5m_bars")`. Every trade row and every order row carries `T = T5` and
  the row label `t_label` = `T tuning-fit (regime reading; the strict-INSIDE twin is printed in Stage V)`, and each
  directory's manifest carries `time_stop_source = {path, key, sha256, value}` (the door's `source`; L-V's F-TRAV
  [e]).
- T of record uses L-V.18's regime reading; the contract's phrase read strictly (every bar of the leg INSIDE) is a
  twin printed in Stage V and enters no book (OD-15).
- **The clock starts at the FILL bar:** a position still open at `close5[f + T5]` exits there, at that close, as a
  taker, reason `time_stop`. The count is by 5m bar INDEX (a zero-volume bar is one bar).
- **No trail:** the stop never moves (L-S.10); the position never grows; T1 does not move the stop.
- **Corridor end:** a position still open at `hi` is marked at `c[hi]`, reason `corridor_end`, booked as a taker
  exit, flagged `open_at_end`; an unfilled T1 half stays unfilled. In WALK-W this is the scored window's law
  (O-9; L-X.24); the trade's continuation is printed from WALK-PIN (L-S.25).
SOURCE: contract :42-43, :100; O-18; OD-15; L-V.2 (the reader's `traverse`), L-V.18 (rival (g): the T-th 1h close
after the fill "depends on where in the hour the fill lands"); LX-X2.7, LX-X2.17; `scripts/tierc7.py:209-211` (the
shadow clock); scout U6 R-17.
RIVALS: the clock from the trigger bar (X's maker-conditioned twin kept the record's clock so that it differed by
the fill test only; here the limit order IS the record, and the traverse measures travel from a touch of the
edge — the fill). A typed integer — F-TRAV.
FAILS-IF: L-V's helper legs F-TRAV [a · tierc12_scalp] and F-TRAV [e · <each arm>], run by this stage's suite;
F-SCALP (i) row "open at f + T5 → time stop at that close", and (n): `T5` bent by one bar moves the exit bar by
one. Planted mutation: the clock anchored at `t`.

---------------------------------------------------------------------------------------------------------------
### F · Costs

**L-S.21 COSTS OF RECORD** — "COSTS OF RECORD: maker bps per side on entry and targets; taker on the stop; funding
journaled." (contract :101); the "maker" ruling (:2-3); disposition OD-10
READING:
- **Which leg pays what** (`fz = E.fees()[stem]`; `mk = fz["maker_bps_side"] / BPS_PER_UNIT`, `tk =
  fz["taker_bps_side"] / BPS_PER_UNIT`): MAKER on the entry, on T1 and on T2; TAKER on every other exit — `stop`,
  `time_stop`, `invalidation`, `corridor_end` (X's `TAKER_EXITS` law). The contract names the stop; the time stop,
  the invalidation and the mark are market exits at a close and are booked at the dearer rate. No slippage on any
  leg of the record.
- **Gross and funding are the estate's function, called as it is:**
  `acc = E.BK.account_l(lf5, E.TP.CONTROL_CARD, d, R, leg)` with `leg = {entry_i: f, entry_px: L, exit_i: x,
  exit_px, harvest: None | (h_i, px(n_T1), d·(px(n_T1) − L)/R)}`. `gross_r = acc["gross_r"]`; **`funding_r =
  acc["funding_r_uncapped"]`** — the interval sum of every funding stamp with `open5[f] < stamp ≤ open5[x]` (the
  T1 fraction to `open5[h_i]`), each priced at the last 5m close at or before it. The D12 ceiling is a v6-card
  accounting rule and is not a rule of this trade (OD-10): the contract says "funding journaled" and gives the
  trade no cap, and a cap can only remove a cost. Filed beside: `funding_ceiling_bound =
  acc["funding_ceiling_bound"]`, `tc_series_net_r = acc["net_r"]` (the lineage's own all-taker booking, D12
  ceiling included; L-S.22) and `funding_stamps`; the bound count per arm is printed in the fill-sensitivity block
  (L-S.16). A stamp at the instant the fill bar opens precedes the fill and is not paid.
- **The fee of record is booked per fraction** by the tier's ONE function, `tierc12_rangewalk.fee_per_fraction`
  (L-R's mirror of X's `fee_per_fraction(e, R_, harvest_px, exit_px, b_e, b_t1, b_x)`, filed at `TC12-R.sfp` and
  imported here; this builder holds no second implementation): with `b_e = b_t1 = mk` and `b_x = mk` if the exit
  reason is `T2`, else `tk`, harvested: `fee_r = [Q·(mk·L + mk·p_T1) + (1 − Q)·(mk·L + b_x·p_x)] / R`; not
  harvested: `fee_r = (mk·L + b_x·p_x) / R`.
  `fee_maker_r` and `fee_taker_r` are its maker-leg and taker-leg parts (`fee_taker_r = 0` on a `T2` exit).
- **`net_r = gross_r − fee_r − funding_r`** — the toll of record, in R of the frozen `R`.
- The row's four TC12 fee columns are L-X.24's: `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`,
  `taker_twin_net_r` (L-S.22).
SOURCE: contract :2-3, :101; O-19; OD-10; `scripts/tierc10_brk.py:1223-1326` (`funding_interval`: "every stamp
with entry_ms < funding_hour_ms <= exit_ms"; `account_l` returns `funding_r` — capped —, `funding_r_uncapped` and
`funding_ceiling_bound`, :1319-1324) [read here]; `scripts/tierc5_rules.py:160-166` (the ceiling: "An ACCOUNTING
rule, not a decision rule … a funding CREDIT is never capped") [read here]; `x_rec/scripts/tc11x_sfp.py:148`,
`:756-803` (`fee_per_fraction`, `book_trade`) [read here]; LX-X2.11; TC11 L-1.2 ("Maker legs carry zero slippage.
Stop and invalidation legs stay taker"); L-X.24; L-R.31 (`tierc12_rangewalk.py`); L-D.17 ("WHICH LEGS pay it is
defined by the registration texts").
RIVALS: maker on the time stop and the invalidation (resting orders "could" be used) — a market exit at a close is
a taker act; the dearer booking cannot flatter. A second funding routine for 5m — `account_l` is lens-generic.
The card's capped funding as the cost of record — a one-sided accounting cap written for multi-week v6 campaigns
(OD-10); it stays visible in `tc_series_net_r`.
FAILS-IF: F-TOLL [book t3]: a leg's rate is not the one this reading assigns, or `fee_maker_r + fee_taker_r ≠
fee_r` within the tolerance, or `funding_r` is not the uncapped interval sum; [book t1]: a bps literal in the
builder's fee path. Planted mutations: maker left on the stop leg; the time stop booked maker; a typed maker
rate; `funding_r` taken from `acc["funding_r"]`.

**L-S.22 THE TWINS ON EVERY ROW** — "TWINS on every row: all-taker (the TC-series toll) · charter slippage."
(contract :102); "F-TOLL (… taker twin == TC-series)" (:121)
READING: every trade row of every arm carries, on the SAME fills and the same path:
- **`fee_all_taker_r = acc["fee_r"]` and `taker_twin_net_r = gross_r − fee_all_taker_r − funding_r`** —
  `BK.account_l`'s own fee booking, which charges `FEE_BPS_SIDE` on every fraction (the TC-series toll law,
  unchanged), with the uncapped funding of L-S.21. The identity `taker_twin_net_r == net_r + fee_r −
  fee_all_taker_r` (L-X.24) therefore holds exactly. Filed beside: `tc_series_net_r = acc["net_r"]`, the lineage's
  own net with the D12 ceiling. "Taker twin == TC-series" (:121) is held as a two-case identity:
  `|taker_twin_net_r − tc_series_net_r| ≤ HAIRCUT_TOL` on every row with `funding_ceiling_bound == False`, and
  `taker_twin_net_r < tc_series_net_r` on the others. The per-fraction form at all-taker rates must equal
  `acc["fee_r"]` within `HAIRCUT_TOL` on every row (X's F-FEE-EQ law; bit-equality is not attainable, the terms
  associate differently).
- **`haircut_net_r = net_r − fee_taker_r × (slip / taker_bps_side)`**, `slip = fz["slippage_bps_side"]` — TC11's
  AM-7 with its maker clause: charter slippage falls on the TAKER legs of the record only (stop, time stop,
  invalidation, mark); "A maker leg … carries zero slippage". This is the column L-X.24's haircut law checks.
- **`taker_twin_haircut_net_r = taker_twin_net_r − fee_all_taker_r × (slip / taker_bps_side)`** — AM-7 on the
  all-taker twin, slippage on EVERY fill: the harshest cost row. It is a required regbook column on every arm of
  this row (their sidecar toll is `maker_entry_targets__taker_stop`, L-X.24).
- **No cost twin prices a maker fill's adverse selection — a maker leg carries zero slippage in both. The only
  proxy in this row is the fill ladder (TICK against DEEP), and the verdict text says so beside the twins.**
The scorer rules `taker_twin`, `haircut` and `taker_twin_haircut` as its beside-prints (L-X.14); none of the three
decides a word.
SOURCE: contract :102, :121; OD-10; TC11 `LEANS_AMENDMENTS.md:86-96` (AM-7); LX-X2.11; `tc11x_sfp.py:780-792`;
L-X.14, L-X.24; `scripts/tierc11_score.py:264` [read here].
RIVALS: the charter twin on every fill of the record book — charges slippage on legs that are resting limits.
An all-taker twin re-walked with touch fills — it would be another book; the contract's twin is a toll. The twin
taken whole from `acc["net_r"]` — it would carry the card's funding cap into a row that has none and break
L-X.24's identity wherever the cap binds.
FAILS-IF: F-TOLL [book t2], [book t5]. Planted mutations: the twin computed with a maker entry; slippage applied to
a maker leg; `account_l` handed a card other than the control card (the half, and the ceiling inside
`tc_series_net_r`, would move); the twin booked with the capped funding.

---------------------------------------------------------------------------------------------------------------
### G · Misses, regime columns, population

**L-S.23 THE MISS COLUMN** — "MISS COLUMN first-class: every unfilled order counted and its would-have outcome
printed at both targets." (contract :95-96)
READING:
- **A miss** is an order of the book of record inside the scored window (`known_at_ms ≤ W`) whose WALK-W status
  is `expired` or `cancelled` (L-S.16). Each carries `miss_class`: `touched_not_through` (`fill_i_touch` non-null)
  or `never_touched`. `unresolved_at_end` orders are listed apart and are not misses. Unfilled orders triggered in
  the strip are counted in the strip print and get no would-have (nothing past `W` is summarised, L-S.25).
- **The would-have walk** answers "what did the limit cost us": the same order taken AT THE TRIGGER CLOSE AS A
  TAKER. Entry price `c5[t]` on bar `t`; the frozen stop `S` and the frozen target levels; `R_wh = |c5[t] − S|`;
  walked from bar `t+1` by L-S.18 with the record's target test, bounded at `hi_W`; the time stop at `close5[t +
  T5]`; invalidation by L-S.19; booked ALL-TAKER — gross and fee by `BK.account_l` (entry leg at bar `t`), funding
  uncapped as on every range row (OD-10): `wh_net_r = acc["gross_r"] − acc["fee_r"] − acc["funding_r_uncapped"]`,
  in R of `R_wh`.
- **"At both targets"** = three variants per miss, each on the whole unit unless stated: `T1` (the only target is
  T1), `T2` (the only target is T2), and `split` (the book's own law: `Q` at T1, the rest at T2). Each files
  `wh_exit_reason`, `wh_reached` (the walk ended at its target), `wh_exit_close_ms`, `wh_net_r`, `wh_gross_r`.
- **A would-have target must be ahead of the would-have entry** — the geometry law's own principle (L-S.11). The
  entry here is `c5[t]`, not `L`, and the POC can lie at or behind it. If `d·(px(n_T1) − c5[t]) ≤ 0` (decided
  exactly, by the grid's comparisons), or the order's T1 is void, the `T1` variant does not exist (filed null
  with the reason `wh_t1_not_ahead` or `t1_void`) and `split` is the `T2` walk; if `d·(px(n_T2) − c5[t]) ≤ 0` the
  `T2` and `split` variants do not exist (`wh_t2_not_ahead`). Both classes are counted.
- **Why the trigger close and a taker fill.** It is the only counterfactual executable at decision time. Entry
  "at the limit" assumes a fill at a price the market never gave (and for `never_touched` a price never traded).
  Entry at the expiry close starts after the move the order missed and makes missing look cheap. Of the
  executable readings this is the one that cannot flatter the book: it shows the full run-away at the dearest toll.
- `S_miss` (key `[book, symbol, known_at_ms, variant]`, `variant` ∈ {`T1`, `T2`, `split`}, `book == "scored"`;
  pointed, not inlined) and the grid `S_MISS_GRID` (whole, keyed by `cell`): trigger era × direction ×
  `miss_class` × `variant` → `n, n_reached, mean wh_net_r, sum wh_net_r`. Tier-E, "no interval", no verdict word,
  NEVER netted into any book.
- Printed on the fill-sensitivity grid: `n_orders`, `n_filled` per rule, `n_missed` (L-S.16).
SOURCE: contract :95-96; X's refusal rows for misses (`reason` "miss" / "miss_nochild" / "fill_unresolved_at_pin",
`tc11x_sfp.py:672-685`) — no outcome there; OD-8, OD-10; scout U6 C15, R-22.
RIVALS: as argued. A would-have at maker rates — an unfilled maker order paid no maker fee; the chase is a taker.
A would-have whose target lies behind its own entry, walked anyway — a resting limit that is marketable when
placed, booked as a loss "at target": not an order.
FAILS-IF: F-SCALP (b) MISS-3 and (l) MISS-TABLE: the status partition `n_orders == filled + expired + cancelled +
unresolved` fails; a miss has a TICK fill in its window; a would-have row differs from the fixture's own walk; a
variant exists whose target is not ahead of `c5[t]`. Planted mutations: the would-have entered at the limit; a
filled order listed as a miss; the split walk booked at maker rates.

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
- **`breadth_5`** and **`tide_age_4h`** (with `tide_band_4h`) — L-G's breadth of record and the asset's own 4h
  tide age of record, read AS FILED from the two tables L-G files at `TC12-C.tide` (L-G.10):
  `tide/breadth_4h.parquet` (key `[open_ms]`; the home-five determined-young count of L-G.11) and
  `tide/tide_bars_4h.parquet` (key `[asset, open_ms]`; the asset's own run and band), each at the last 4h bar with
  `close_ms ≤ τ` (`asof_index`). Their definitions are L-G's; this section adds none and re-derives no band. A
  bar that is not warm, or whose edges are undefined, files the column null with L-G's own flag beside it.
- `S_REGIME` (a grid, whole, keyed by `cell`): for the three LEVELLED columns (`atr1h_tercile`; `breadth_5`; the
  tide band) column × level × book → `n_orders, n_filled`; for the two AGES (`va_age_1h`, `tide_age_4h`), which
  have no levels and are given none here, per book `n`, minimum, lower hinge, median, upper hinge, maximum
  (L-V.18's hinge law, so no quantile level is typed). Counts and positions only; no outcome column.
SOURCE: contract :102-103; `x_rec/scripts/tc11x_pct.py:71-106` (sha `49809c07…4bb7`; `WINDOW`, `FLOOR` at :48-49);
X's `exit/build_manifest.json` `constants.vol_window`, `.vol_floor`; LX-X1.7, LX-X4.2, LX-X4.7; TC11
`LEANS.md:464-467` (L-S.2's "trailing 2,000-bar quantiles over a window ending at the entry bar inclusive");
L-V.16; L-G.10, L-G.11; L-0.10 (`TC12-C.tide`); scout U5 §2.15.
RIVALS: an expanding pooled prefix (the tide band's "trailing") — the filed precedent for an ATR tercile in the
scalper is the rolling window. NATR — X's twin. Outcome tables by regime level — a cut of the book the contract
does not order ("columns"). The tide columns recomputed here from the 4h tape — a second banding law outside L-G.
FAILS-IF: F-SCALP (m) REGIME: a stamp differs from the fixture's own loop over the filed series up to `k1` / the
4h as-of bar; a tercile decided on a sample reaching past `k1`. Planted mutations: the window end at `k1 + 1`; the
4h columns joined at the bar containing τ.

**L-S.25 POPULATION, ERA, THE SCORED WINDOW, THE STRIP** — "(vs zero; HOLDOUT era ["era"]; five home assets; both
directions; …)" (contract :83-84); rulings O-9, O-23; disposition OD-14
READING:
- **Panel:** the five home assets (`E.CLASSIC5`, L-D's home panel object), pooled; both directions in one book.
- **A trade's instant is its FILL bar's close** (O-9: "holdout = entry-bar close after `1719791999000`"; L-X.24:
  `entry_close_ms` is "the 5m bar of the fill"): `entry_ms = open5[f]`, `entry_close_ms = close5[f]`, `era =
  E.era_of(entry_close_ms)` — `tuning` iff `entry_close_ms ≤ ERA_CUT`, else `holdout`. **The book of record is the
  rows of the TICK walk with `ERA_CUT < entry_close_ms ≤ W`.**
- **The scored window (O-9).** Every book is ridden with `hi = hi_W`, the last 5m bar closing `≤ W` (WALK-W); a
  position still open there is marked at that bar's close with `exit_reason = "corridor_end"`, so `exit_close_ms ≤
  W` on every row of every scored, ladder and Tier-E arm.
- **An ORDER's era is its trigger close** (`era_trigger = E.era_of(known_at_ms)`): an unfilled order has no entry
  bar. An order triggered at or before the cut and filled after it is a holdout TRADE and a tuning ORDER; at most
  one per asset and book can exist (one resting order), and the count is printed (`era_straddle`).
- **One walk, not one per era.** The scored book is the holdout slice of the full-corridor TICK walk (L-S.1); the
  same walk's every row with `entry_close_ms ≤ W` is the arm `tierE__full_corridor`. The walk is not restarted at
  the cut.
- **The strip (O-9, OD-14) — for every ridden arm.** WALK-PIN is run once per fill rule and once per ridden Tier-E
  arm; `strip.parquet` holds every arm's rows with `W < entry_close_ms ≤ PIN` under the column `arm`; the `strip`
  leaf prints `n` per arm and one pointer, no statistic. The ridden arms are `scored`, `ladder__touch`,
  `ladder__deep`, `tierE__panel17`, `tierE__rr_unfiltered` and `tierE__live_edge`; `tierE__full_corridor` is the
  same walk as `scored` and is not repeated — it appears in the strip sidecar's `n_by_arm` with `same_rows_as =
  "scored"`. Ridden, printed beside, never scored, never pooled: a count and a pointer are the only aggregates
  over strip rows anywhere.
- Trades of the TICK walk open at `W` are continued in `stage_s/open_at_w_continued.parquet` (their WALK-PIN exit
  beside their scored mark). The other walks' open-at-`W` trades are held by the prefix identity below and are
  continued in no table.
- **Prefix identity of the two rides, for every walk:** every WALK-PIN order and trade resolved at or before `W`
  equals its WALK-W row on every column; a trade OPEN at `W` is compared on its entry, stop, R, T1 and T2 levels,
  and on its T1 fill iff that fill happened at or before `hi_W` — else the WALK-W row's T1 must be unfilled; the
  WALK-W rows of the TICK walk marked `corridor_end` are exactly the keys of `open_at_w_continued`.
- **Stamps.** A scored-window table is stamped with the score edge; the strip, the order ledgers and every table
  that reads past `W` with the pin (L-0.13).
- **What is in-sample on these bars** is the label's business (L-S.29): the lookback and the traverse are
  tuning-fit and are out-of-sample on the holdout; the bars themselves are `pre_seen` (O-23, O-30).
SOURCE: contract :83-84, :137; O-9; OD-14; L-X.4, L-X.14, L-X.24; L-D.28; TC11 `LEANS.md:95-102` (L-1.3: "era = the
entry (or event-anchor) bar's CLOSE … P-SCALP-2 names the holdout era, so it is scored there").
RIVALS: era by the trigger close for trades — contradicts O-9 and the scorer's row law. A walk begun fresh at the
cut — discards the position a trader would have carried across it. Scoring to TC12's pin — O-9. A strip for the
record arm only — O-9 names every book and every arm (OD-14).
FAILS-IF: F-SCALP (e3) W≡PIN PREFIX and (o) VIEWS: a WALK-PIN row resolved by `W` differs from WALK-W; a scored row
with `entry_close_ms ≤ ERA_CUT` or `> W`; a strip row at or before `W`; a ridden arm with no strip rows where its
WALK-PIN ledger holds a fill after `W`. Planted mutations inside production: WALK-W reads an acceptance event
after `W`; `hi_W + 1`; the era taken from the trigger close; a WALK-W open row carrying a T1 fill at a bar after
`hi_W`.

**L-S.26 THE TIER-E VIEWS** — "the full-corridor and 17-asset views Tier-E" (contract :84); "the unfiltered twin
printed" (:74)
READING: each is collared (L-0.16), carries no verdict word, is promoted to nothing (:133), and is ruled by the
scorer's one leaf per arm, `arm__<slug>` (L-X.14): the sidecar's ruler (vs zero) at the seed of record on the arm
alone, clusters = the sidecar's `panel`; `n`, `n_clusters`, `point`, `lo`, `hi`, `n_draws_finite`,
`would_read_ci_only`, `seed`, `draws_sha256`. No p, no bar, no sensitivity seed, no slice, no LOAO, no verdict
word. This section computes no interval.
- **`tierE__full_corridor`** — L-S.25; leaf `arm__full_corridor`. On its tuning rows the lookback and the traverse
  are IN-SAMPLE (tuning-fit); the row label says so. The scorer's `tuning_slice` of this registration is computed
  on this arm's tuning rows (the one slice taken on an arm).
- **`tierE__panel17`** — the same TICK walk on all seventeen assets (`E.PANEL17`), holdout by fill, stamped with
  the 17-asset panel; leaf `arm__panel17`. What it honestly is: the snapshot carries 5m, funding and a tick for
  all seventeen (O-8, O-26), and Stage V files 1h and 4h value areas for the twelve (L-V.22), so the simulator
  RUNS; but for the twelve the lookback is the CLASSIC5-fitted pin, the traverse is the CLASSIC5 tuning fit, **no
  feasibility word and no licence exist** (the "1h maker PASS" is a POOLED:CLASSIC5 word), MNT's maker rate is an
  assumption on another venue's schedule, and several tapes begin inside the holdout (the first readable instant
  per asset is printed). Every row carries the column `licence`: `licensed` on the five home assets, `none —
  CLASSIC5 word transplanted` on the twelve (the column holds no mirror word). The five home assets' rows in this
  arm must equal the scored arm's (asserted). The twelve's rows are on L-0.30's `ORDERED_TWINS_T` — the contract
  orders this view (:84) — so F-NOT's LICENCE leg does not read them as an unlicensed trade. Its 5m reads are
  Stage S's own (`FIVE_MIN_READERS_T`).
- **`tierE__rr_unfiltered`** — L-S.12's twin, re-walked; the geometry refusals stand in it. Leaf
  `arm__rr_unfiltered`.
- **`tierE__live_edge`** — the limit follows the re-rolled value area: at the one 1h close inside the window
  (bar `q*`, new row `k1' = asof_index(close_ms_1h, close5[q*])`), an order still unfilled and not cancelled is
  re-priced for bars `> q*` from `VA(k1')` and `ATR_1h[k1']` by L-S.9 … L-S.12 (same direction, same trigger kind
  and extreme; the window is not extended); it is cancelled and counted if the new limit is marketable against
  `c5[q*]` (`reprice_marketable`), is refused by the geometry law or fails "rr-min" (`reprice_<reason>` with
  L-S.14's slug). Once filled, everything is frozen. Leaf `arm__live_edge`.
- **Slices of the book of record, descriptive** (`S_SLICES`, a grid keyed by `cell`, printed whole in
  `STAGE_S.md`; `n`, mean and sum of `net_r`, "no interval"): per `panel` value (each home stem); per direction;
  per `trigger_kind`; `on_1h_close`; `t1_void`. The scorer's own beside-prints (L-X.14) are computed from the arms
  and are not repeated here.
SOURCE: contract :74, :84, :133; O-8, O-26; L-V.22; L-X.14, L-X.24; L-0.15, L-0.16, L-0.30 (leg LICENCE,
`ORDERED_TWINS_T`).
RIVALS: the 17-asset view as NA "because Stage D names 1h/4h/1d for the twelve" — O-8 reads that sentence as binding
Stage V's lenses, not the tapes; the view is printed with its limits named instead. A per-asset lookback for the
twelve — L-V.22's rival. An interval, a p or LOAO computed here on a view — the scorer's leaf is the only ruler,
and it prints no p.
FAILS-IF: F-SCALP (o) VIEWS: a home row of `tierE__panel17` differs from the scored arm; a row's `licence` value is
not the one its asset's panel requires; the holdout slice of `tierE__full_corridor` is not the scored arm; a
Tier-E table lacks the collar (F-COLLAR). Planted mutations: a home row altered in the 17-asset arm; a verdict
column added to a view.

---------------------------------------------------------------------------------------------------------------
### H · Precondition, the kill, the label

**L-S.27 THE PRECONDITION** — "1h maker PASS … (the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h
maker}; nothing else may trade a range)" (contract :39-41); "a registration closed by precondition spends no test"
(:9); "exists by the "maker" ruling" (:82); disposition OD-12
READING: ONE item, evaluated by the builder BEFORE any candidate is computed and again by the scorer (L-X.10).
- **The licence word.** Record `research_outputs/tierc12/va/VA_MIRROR.json`, certified by `progress/TC12-V.json`
  `artifact_shas`; selector `licence["1h|maker"].by_era["holdout"].would_read`; required `"PASS"` (exact string).
  It is X's filed word for POOLED:CLASSIC5 · holdout · `va_regime` · 1h · maker
  (`x_rec/tierc11x/va/feasibility.parquet`, sha `ea8573b3…b6f0`), mirrored by L-V.17 and read through the reader's
  `licence("1h", "maker", "holdout")`, which HALTs for any pair outside the licence set and logs the call in
  `READ_SET.json` `licence_reads`. Nothing else is a precondition of this row (OD-12; O-17: the mirror reads,
  never recomputes).
- **Printed beside, never a precondition (O-19).** The SCORER computes the collared beside leaf
  `licence_at_maker_pin` on P-SCALP-3: `{maker_bps_side (E.fees(), one maker rate over the five home stems
  asserted), round_trip_bps = 2·maker_bps_side, x_toll_bps (the row's quoted toll_bps), differs_from_x_assumption
  (Stage D's maker_pin flag), edge_net_h20_at_pin = round(edge_median_term_h20, ND) − round(edge_toll_atr ×
  round_trip_bps / x_toll_bps, ND)}` from the columns `VA_MIRROR.json` QUOTES for the 1h|maker holdout row
  (L-V.17), `ND` = X's `pins.laws.round_nd`; where the pin equals X's assumption the figure must equal the quoted
  `edge_net_h20`. It carries no word, is labelled "a re-derivation of one leg from printed columns; not a
  licence", and is printed in the verdict text and in §0.3. If `edge_net_h20_at_pin ≤ 0` the cell carries the
  qualifier `LICENCE EDGE ≤ 0 AT THE PINNED MAKER RATE (X assumed <x> bps round trip; pinned <y>)`; the row is
  still built, scored, and spends its test. Closing the row on that figure is the operator's order, by name,
  before Stage D's fee capture (OPEN TO OPERATOR 2). This builder computes nothing of the leaf.
- **Not met** → `regbooks/P-SCALP-3/STATUS.json` (written by `tierc12_regbook.write_status`) with `status =
  "CLOSED_BY_PRECONDITION"`, the item with the value found (`found`, `met = false`), `arms = []`, and NOTHING
  else: no candidate, no order, no book, no MISS table, no Tier-E view, no parquet in either directory (O-22).
  The §0 cell reads `CLOSED BY PRECONDITION (<record>#<selector> reads <found>; required <required>) — no number ·
  no test spent`; m stays as parsed and the bar is not loosened. The stage's fixtures then run their synthetic
  legs and print `CLOSED-NO-BOOK P-SCALP-3` for every real-book leg (L-S.31).
- **Met** → STATUS `"BUILT"` with the same item (`found = "PASS"`, `met = true`) and `arms` = the eight of L-S.30.
- On the records as filed the item is met (F-VA-MIRROR HALTs the tier otherwise); the closed path is proven on a
  planted leaf.
- What the licence is NOT is carried as DISCLOSURES D-2 beside the verdict: it was earned on X's record machine,
  on the outer 20% of value with an H20 exit and BOTH legs at the maker rate, while this trade pays the taker rate
  on every exit that is not a target.
SOURCE: contract :9, :39-41, :82; O-17, O-19, O-22; OD-12; L-V.17 (the `by_era` leaf and the columns it quotes;
the licence set); L-X.10, L-X.14 (`licence_at_maker_pin`), L-X.24 (STATUS); the licence row [read while drafting:
`would_read "PASS"`, `toll_bps 4.0`, `of_record_for_detector False`, `edge_median_term_h20 0.102664`,
`edge_toll_atr 0.064663`, `edge_net_h20 0.038001`]; `pins.laws.round_nd` of X's `va/build_manifest.json` [key
read here]; scout U2 §1.8 (the linear toll law, the break-even round trip); TC11 `LEANS.md:444-446` (L-S.1) and
`regbooks/P-SCALP-2/STATUS.json` (the filed form).
RIVALS: a second, closing item on the re-derived edge leg — not taken: OD-12, O-17 (the mirror reads, never
recomputes). Re-deriving the licence under the V2 machine — O-17 forbids. The ALL-era or tuning row — the row is
scored on the holdout and reads its own era's word (O-17).
FAILS-IF: F-SCALP (p) GATE: with the reader's `licence` returning a planted leaf whose `would_read` is not
`"PASS"`, the builder writes anything but STATUS, or a candidate is computed (a call counter); L-X's F-FAM
[PLANTED] holds the scorer's side. Planted mutations: the gate reading the taker row; the gate reading the ALL
era; a closing second item planted in a copy of the spec → `PRECOND-GRAMMAR` / TEMPLATE mismatch at filing.

**L-S.28 THE PRE-NAMED KILL, EXHAUSTIVELY** — "PRE-NAMED KILL: NOT SUPPORTED if the through-tick book fails the
bar; CLOSED FOR GOOD if it fails under DEEP too; CLOSED if it clears only under TOUCH (the fill-sensitivity row is
part of the verdict text); one-asset dependence read by LOAO 3/5 and the single-trade share." (contract :104-106);
dispositions OD-13, OD-19
READING: the rule of record is L-X.9's, carried without change. For each fill book X ∈ {TOUCH, TICK, DEEP}, at the
seed of record and the SCALPER bar, exactly one of three states holds: `U(X)` = X is not PANEL COMPLETE (L-X.7's
clause (c) fails; its ruler is undefined; an EMPTY BOOK is the limiting case); `C(X)` = PANEL COMPLETE and clauses
(a) ∧ (b) of L-X.8 hold; `F(X)` = PANEL COMPLETE and (a) or (b) fails. `D` = fewer than `above_half_bar(N)`
leave-one-asset-out panels of the TICK book exclude zero from above (L-X.11; "3/5" parsed from :106). **A closure
word needs a MEASURED failure: a book whose ruler is undefined is not a failed book.** The ten cases partition
every outcome:

| TICK | D | DEEP | TOUCH | `verdict_of_record` | qualifier | the contract's clause |
|---|---|---|---|---|---|---|
| C | false | C | any | `SUPPORTED` | — | the positive case |
| C | false | F | any | `SUPPORTED` | `FILL-SENSITIVE (does not clear under DEEP)` | none |
| C | false | U | any | `SUPPORTED` | `FILL-SENSITIVE (DEEP PANEL INCOMPLETE)` | none |
| C | true | any | any | `NOT SUPPORTED` | `LOAO BELOW THE LINE (k/N above; passing when dropped: <assets>; failing when dropped: <assets>)` | "one-asset dependence read by LOAO 3/5" |
| U | any | any | any | `NOT SUPPORTED` | `PANEL INCOMPLETE (…)` / `EMPTY BOOK` and `TICK PANEL INCOMPLETE — closure not ruled` | none (the ruler is undefined) |
| F | any | C | any | `NOT SUPPORTED` | — | "fails the bar" |
| F | any | U | any | `NOT SUPPORTED` | `DEEP PANEL INCOMPLETE — closure not ruled` | "fails the bar"; DEEP not measured |
| F | any | F | C | `NOT SUPPORTED — CLOSED` | `(clears only under TOUCH)` | "clears only under TOUCH" ("fails under DEEP too" also holds: OPEN TO OPERATOR 6) |
| F | any | F | U | `NOT SUPPORTED — CLOSED` | `TOUCH PANEL INCOMPLETE — "for good" not ruled` | "fails under DEEP too"; TOUCH not measured |
| F | any | F | F | `NOT SUPPORTED — CLOSED FOR GOOD` | — | "fails under DEEP too", at every fill model |

- **One test.** m stays as parsed (:82); only the TICK book can produce `SUPPORTED` and only it spends the
  family's test. TOUCH and DEEP are ruled with the same ruler, seed, draws and bar and can only qualify a
  `SUPPORTED` cell or choose among the failure words. The fill-sensitivity row opens with the fixed sentence:
  "TOUCH and DEEP are fill-model twins, not tests: they are ruled at the family bar without a test of their own
  and can only qualify a SUPPORTED cell or choose among the failure words; an interval that excludes zero on
  either is not a result."
- **The unnamed cells.** TICK clears and DEEP fails or is not measured: the row stands, and says in its own cell
  that it does not survive, or was not measured under, a deeper fill. TICK fails and DEEP clears: the row fails
  and nothing is closed — a deeper book that clears is not evidence the idea is dead. TOUCH failing while TICK
  clears is possible because the books are sequenced separately (L-S.16); the word is TICK's and the
  fill-sensitivity row shows the inversion. Any `PANEL INCOMPLETE` book closes nothing beyond what the table says.
- **One-asset dependence** (the clause sits inside the kill; L-X.9 takes the reading that cannot flatter, and
  O-32 lets it stand): where the TICK book clears but LOAO does not reach 3/5, the word is `NOT SUPPORTED` with
  the qualifier `LOAO BELOW THE LINE (…)`, and the verdict text adds the fixed sentence "the contract reads
  one-asset dependence by this line (:106); a panel that fails when an asset is DROPPED leans on that asset, a
  panel that fails while an asset is KEPT is dragged by it". The single-trade share (L-X.12) has no threshold in
  the contract or on file; it is printed and decides nothing.
- **The verdict text** = the cell (word, qualifiers, label per L-S.29) + the fill-sensitivity row (the fixed
  sentence; then per fill rule the book's own `n`, point, interval, `p_num/p_den` and its state C / F / U; then
  the two booleans `fails_under_deep_too = F(TICK) ∧ F(DEEP)` and `clears_only_under_touch = F(TICK) ∧ F(DEEP) ∧
  C(TOUCH)`, which `SCORES.json rows[].fill_ladder` also carries) + the LOAO line `k/N` with its fixed sentence +
  the single-trade share of record + the per-order ladder counts of the TICK ledger and, where the three books'
  own n are not ordered, the line `BOOK-N-NOT-MONOTONE` (L-S.16; L-X.24) + beside the licence word the leaf
  `licence_at_maker_pin` (L-S.27) + beside the cost twins the sentence of L-S.22 on adverse selection.
- **What a closure forbids afterwards** — the standing lines the ledger append carries (L-X.32):
  - `NOT SUPPORTED` (with or without a `PANEL INCOMPLETE` qualifier): nothing is closed. The 1h maker licence
    stands; a later tier may register another 1h value-area range trade, `pre_seen` on these bars.
  - `NOT SUPPORTED — CLOSED`: this trade form — a resting limit at the 1h value edge on the 5m clock — is closed
    under every fill model that requires a trade-through. It is not re-registered on backtest fills; the only
    reopening path is evidence about the fill itself (queue position or live fills), ruled in by the operator.
  - `NOT SUPPORTED — CLOSED FOR GOOD`: scalper mode on the 1h value area at the maker toll is closed in this and
    every later tier; no fill model reopens it (it has a MEASURED failure at every fill model), and the "maker"
    ruling's one use is spent. Only a new operator ruling naming a new mechanism reopens the 1h lens for range
    trading.
  - A `CLOSED BY PRECONDITION` row closes nothing beyond what its failed record already says.
SOURCE: contract :82, :104-106; O-32; OD-13, OD-19; L-X.7, L-X.8, L-X.9 (the table above is its table, row for
row), L-X.11, L-X.12; `x_rec/tierc11x/LEANS_X.md:695-696` (a single strongly negative asset fails every
leave-one-out panel that contains it); TC11's R2 law ("a FAIL closes that lens … unless the toll model changes"),
quoted in `x_rec/tierc11x/REGISTRATION_PLAN.md:206-209`.
RIVALS: L-X.9's rivals (i)-(iii). `CLOSED FOR GOOD` whenever TICK and DEEP fail, whatever TOUCH reads — the
literal order of the contract's two clauses; it is the operator's to name (OPEN TO OPERATOR 6). LOAO as a
qualifier on a `SUPPORTED` word — L-X.9 rival (ii); O-32 lets the stricter reading stand (OPEN TO OPERATOR 4). A
closure word on a book that is not PANEL COMPLETE — a permanent closure resting on a missing row, not on an
interval (OD-13).
FAILS-IF: L-X's F-VERDICT [LADDER], which enumerates every (TICK, D, DEEP, TOUCH) combination over the three
states C / F / U (plants: TOUCH and DEEP swapped; the D column dropped; a closure word produced on a U book); here
F-SCALP (o): the three ladder-class sidecars do not carry `fill_rule` ∈ {tick, touch, deep} one each, or `scored`
is not the TICK book. Planted mutation: the TOUCH book shipped as `scored`.

**L-S.29 THE LABEL** — rulings O-23, O-30; "in-sample labels carried" (contract :130)
READING: P-SCALP-3 carries `pre_seen` with the tag KIN-SEEN (O-30) and prints L-X.13's KIN-SEEN template. The cell
is `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these
bars)`; the template has no clause slot, and the word "re-score" stands nowhere on this row — this trade form was
never scored. The label's `pre_seen.text` (in the REGISTRATION SPEC) is not a clause of the cell: it is filed as
the label's `text` and `items` and printed UNDER the cell, in the row's `disclosures[]`, with D-2 and D-3. It says
what was seen and what was not: X printed the outcome of fading 1h value-area edges at the maker toll on these
same holdout bars — it is the licence row itself — and X3 printed 1h value-area swing-failure outcomes; this
trade form was never scored. Every scored bar is ≤ 2026-09-25T00:00Z (O-9), the instant X's standing ledger line
names. The "T tuning-fit" label rides on every trade and order row (`t_label`, L-S.20) and the lookback's label
(`l_label` of row `k1`, L-V.24) on every order row and in every arm's sidecar `description`; on the holdout book
both the traverse and the lookback are out-of-sample.
SOURCE: O-23, O-30; OD-1; DISCLOSURES D-2, D-3; `x_rec/tierc11x/LEANS_X.md:1811-1818` (LX-X3.14), :2468-2470 (the
standing line); L-X.13.
RIVALS: no label (the contract carries none on this row) — O-23 rules it; the label cannot flatter. The RE-SCORE
template — not taken: O-30 (a label must be true; neither lane's trade form was ever scored).
FAILS-IF: L-X's F-REG [TEMPLATE]; planted mutation: the template rewritten to the RE-SCORE form.

---------------------------------------------------------------------------------------------------------------
### I · Outputs, fixtures, compute

**L-S.30 OUTPUTS** — "the scalper's fill-sensitivity and twins" (contract :128-129); "F-KEY" (:124)
READING:
- **`regbooks/P-SCALP-3/`** (L-X.24's interface; every file written through `scripts/tierc12_regbook.py` —
  `write_status`, `write_arm` (which calls L-0.13's `put_regbook`: full float, the key asserted unique, the collar
  on `strip` and `tierE__*` arms only) and `write_manifest`; this builder holds no parquet writer and no
  validator of its own): `STATUS.json`, `build_manifest.json`, and per arm `<arm>.parquet` + `<arm>.json`. The
  eight arms of record, each written even when it holds no row:

  | arm | kind | what | `era_scope` | `panel` | `fill_rule` |
  |---|---|---|---|---|---|
  | `scored` | scored | the TICK walk, `ERA_CUT < entry_close_ms ≤ W` | holdout | the home five | `tick` |
  | `ladder__touch` | ladder | the TOUCH walk, same window | holdout | the home five | `touch` |
  | `ladder__deep` | ladder | the DEEP walk, same window | holdout | the home five | `deep` |
  | `strip` | strip | every ridden arm's rows with `W < entry_close_ms ≤ PIN`, under `arm` (L-S.25) | holdout | the seventeen | null (a row's rule is its `arm`'s) |
  | `tierE__full_corridor` | tierE | the TICK walk, every era, `entry_close_ms ≤ W` | full | the home five | `tick` |
  | `tierE__panel17` | tierE | the TICK walk on the seventeen, holdout | holdout | the seventeen | `tick` |
  | `tierE__rr_unfiltered` | tierE | the TICK walk without the reward test, holdout | holdout | the home five | `tick` |
  | `tierE__live_edge` | tierE | the TICK walk with the re-priced limit, holdout | holdout | the home five | `tick` |

  Sidecar (L-X.24's keys): `ruler = "vs_zero"`, `lens = "5m"` (the CLOCK — L-X.24's entry-bar law reads it), `toll
  = "maker_entry_targets__taker_stop"`, `fee_schedule {path, sha256}`, `description` (which carries the two
  labels of L-S.29); the three ladder-class sidecars add `n_orders`, `n_filled_touch`, `n_filled_tick`,
  `n_filled_deep` (L-S.16); the `strip` sidecar adds `n_by_arm` and `same_rows_as` (L-S.25); `strip` and
  `tierE__*` sidecars carry the collar keys. The licence pair of every arm is `1h|maker` — the value-area lens of
  the lane `scalp_va_1h` and the maker toll — whatever the sidecar's `lens` says (INTERFACE: L-0).
  Rows: L-X.24's twenty columns at its dtypes (`symbol`, `entry_ms = open5[f]`, `entry_close_ms = close5[f]`,
  `direction`, `entry_px = L`, `stop_px`, `r_dist`, `exit_close_ms = close5[x]`, `exit_reason` ∈ {`stop`, `T2`,
  `time_stop`, `invalidation`, `corridor_end`}, `net_r`, `gross_r`, `fee_r`, `funding_r` (uncapped),
  `haircut_net_r`, `era`, `lane = "scalp_va_1h"`, `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`,
  `taker_twin_net_r`); the three conditional columns this row requires (`taker_twin_haircut_net_r`,
  `funding_ceiling_bound`, `tc_series_net_r`); `arm` on `strip` and only there; and beside them the extra columns
  `known_at_ms`, `era_trigger`, `trigger_kind`, `also_cross`, `on_1h_close`, `edge_px`, `n_limit`, `t1_px`,
  `t2_px`, `t1_void`, `t1_within_fee_band`, `harvest_i`, `harvest_px`, `exit_i`, `exit_px`, `bars_held`, `T`,
  `t_label`, `time_stop_i`, `stop_on_fill_bar`, `gap_stop`, `gap_t1`, `gap_t2`, `both_touch_bars`,
  `stop_bar_open_through_target`, `fillbar_target_withheld`, `t1_marketable_at_placement`,
  `t2_marketable_at_placement`, `inval_event_E`, `inval_edge_moved`, `open_at_end`, `n_entry_fills` (always 1),
  `n_stop_moves` (always 0), `stop_px_at_exit`, `funding_stamps`, the four regime columns and `licence`
  (`licensed` / `none — CLASSIC5 word transplanted`).
- **`stage_s/`** (every parquet written through L-0.13's `put`: collared, keyed, stamped; an empty table is not
  written and is listed under `skipped_empty`; with `build_manifest.json`, `READ_SET.json`, `STAGE_S.md`,
  `FIXTURES_STAGE_S.txt`):

  | table | key | what |
  |---|---|---|
  | `S_orders_<book>` | `[book, symbol, known_at_ms]` | every order of the book's WALK-PIN ledger, misses included (the row is described below) |
  | `S_refusals_<book>` | `[book, symbol, known_at_ms]` | every trigger that did not become an order, with its `reason` (L-S.14's six slugs), its `t2_r` where defined, and `in_scored_window` |
  | `S_miss` | `[book, symbol, known_at_ms, variant]` | L-S.23; `book == "scored"`, `variant` ∈ {`T1`, `T2`, `split`} |
  | `open_at_w_continued` | `[symbol, entry_close_ms]` | L-S.25 |
  | `S_FUNNEL` (grid) | `[cell]` | `panel` × direction × trigger kind × gate → the counts surviving each gate (PERM, SETUP, the trigger, `stop_none`, `poc_not_ahead`, `t2_not_ahead`, `rr_min`), independent of fill rule and of sequence |
  | `S_FILL_SENSITIVITY`, `S_REGIME`, `S_SLICES`, `S_MISS_GRID` (grids) | `[cell]` | L-S.16, L-S.24, L-S.26, L-S.23 |

  `<book>` ∈ {`scored`, `ladder__touch`, `ladder__deep`, `tierE__panel17`, `tierE__rr_unfiltered`,
  `tierE__live_edge`} — the six order ledgers (`tierE__full_corridor` is `scored`'s walk). A grid's asset axis is
  the column `panel` (the stems and, where pooled, `POOLED`), never `asset` or `symbol`. None of the order,
  refusal and miss tables carries a column named `entry_ms`, `entry_open_ms`, `entry_close_ms`, `harden_ms` or
  `event_ms`: the fill is `fill_close_ms`, the three per-rule fill bars are `fill_i_touch`, `fill_i_tick`,
  `fill_i_deep`, and the trigger close is `known_at_ms` everywhere.
- **The order ledger's row** (`S_orders_<book>`): identity and era (`book`, `symbol`, `known_at_ms`,
  `era_trigger`, `in_scored_window = (known_at_ms ≤ W)`, `direction`, `trigger_kind`, `also_cross`,
  `on_1h_close`); the as-of row (`k1_close_ms`, `k4_close_ms`, the two states, `inside_frozen_only`, `l_label`);
  the gates' values; the geometry in prices and ticks (`edge_px`, `n_limit`, `snap_ticks`, `stop_px`, `r_dist`,
  `rail_binding`, the run and its extreme, `t1_px`, `t2_px`, `t1_r`, `t2_r`, `r_atr`, `t1_void`,
  `t1_within_fee_band`, `fee_band_r`, `n_deep`, `deep_floor_binding`); `fill_i_touch`, `fill_i_tick`,
  `fill_i_deep`, `fill_close_ms`; `status` (to PIN) and `status_at_w` (the WALK-W status: equal to `status` for an
  order resolved at or before `W`, `unresolved_at_end` for one alive at `hi_W`, null when `known_at_ms > W`);
  `miss_class`; a cancellation's `cancel_by`, `cancel_bars_out`, `cancel_E`; the permission-at-resolution flags;
  `T`, `t_label`; the regime columns; and the event columns the stamps read — `ev_entry_ms`, `ev_t1_ms`,
  `ev_exit_ms`, `ev_expiry_ms`, `ev_cancel_ms` (int64 ms, null = did not happen; the OPEN of the bar for an
  intrabar event, the close for a close event), `ev_exit_stamp` (`open_of_bar` for a stop or target exit, `close`
  for an invalidation or a time stop — the lineage's `exit_event_stamp` form), `resolution_close_ms` (the close at
  which the order's life ended: the exit close of a trade, the expiry or cancel close of a miss; null while the
  order rests or its position is open at PIN) and `open_at_asof` (true iff that life has not ended at PIN: the
  mark at PIN is no exit event, `ev_exit_ms` stays null and the reader stamps `as_of_pin`). The counts of record
  (the fill-sensitivity grid, the sidecars' four counts, the MISS table) are taken on rows with
  `in_scored_window`, by `status_at_w`.
- **The V5 stamps** (contract :44-45 "every arm below"). The scalper's books are stamped by `TC12-V.stamps.s`
  (L-V.19): key `[book, symbol, known_at_ms, instant_kind, instant_ms]`, `bar_close` at every 1h close between the
  trigger and the order's resolution (`bar_close_lens = "1h"`). No book builder stamps its own book: this section
  files the six frames (`stage_s/S_orders_<book>.parquet`; stamp books `P-SCALP-3__<arm>`) and declares their
  kind — `lens` `5m`; `key` `[known_at_ms]`; `start_col` `known_at_ms`; `end_col` `resolution_close_ms`;
  `bar_close_lens` `1h`; events `arm` (`known_at_ms`, close), `entry` (`ev_entry_ms`, open_of_bar, post), `ev_t1`
  (`ev_t1_ms`, open_of_bar, post), `exit` (`ev_exit_ms`; by `ev_exit_stamp`: open_of_bar with its post twin, or
  close), `expiry` (`ev_expiry_ms`, close), `cancel` (`ev_cancel_ms`, close), and `as_of_pin` from `open_at_asof`
  (never `exit`). `bar_close` is at 1h closes and not
  at every 5m close because no member of the vector can change between two 1h closes (the vector is a join of
  lens rows, L-V.20). `tierE__full_corridor`'s instants are `P-SCALP-3__scored`'s and are not re-stamped. The
  stamp tables are L-V's: filed under `va/stamps/`, proven by its F-NEST-ASOF [<book>] at `TC12-V.stamps.s`, and
  read by nothing in this stage.
- **The report** (L-X.28 §4) prints whole: the verdict text; the three books' sidecars; `S_FILL_SENSITIVITY`,
  `S_MISS_GRID`, `S_REGIME`; the twins' leaves. `S_SLICES` and `S_FUNNEL` are carried by pointer (path, sha, cell
  count) to `STAGE_S.md`, the stage document of record, where they are printed whole; the per-order and per-trade
  tables by pointer (path, sha, rows, key).
- Ferry classes are derived by L-L.24's rule from these declared columns: the arms, `S_orders_*`, `S_refusals_*`,
  `S_miss` and `open_at_w_continued` are PER-TRADE (FERRIED); the stamp tables and the grids are POINTED (L-L.25).
- Scored-window tables are stamped with the score edge; the strip, the order ledgers and every table that reads
  past `W` with the pin (L-0.13); `as_of_lens = "5m"`.
SOURCE: L-X.24, L-X.26, L-X.28; L-0.13 (`put`, `put_regbook`), L-0.15, L-0.16, L-0.21; L-V.19, L-V.20; L-L.24,
L-L.25; L-D.27; OD-5, OD-7, OD-14, OD-18; contract :44-45, :111, :128-129.
RIVALS: a `bar_close` stamp at every 5m close — one identical row per 5m bar of every hour of every open order.
The stamps filed by this stage — not taken: O-29, OD-7 (the instant stamps are Stage V's tables). Order tables
keyed on a private name for the trigger instant — they would class POINTED under the ferry's frozen vocabulary
and the MISS rows would never reach the bus.
FAILS-IF: the stage's instances of F-KEY, F-DET, F-COLLAR on `[stage_s]` and `[regbooks/P-SCALP-3]` and F-GRID
`[S_*]` (L-0.20, L-0.21, L-0.16, L-0.15), L-X's F-REGBOOK `[P-SCALP-3]` on the arms and L-V's F-VA-PINS `[e ·
P-SCALP-3]`; planted mutations as those fixtures define, plus two here: an order row whose `edge_px` is not the
filed `val` / `vah` of its row (F-NOT's PIVOT-RANGE leg must go RED); an order-table copy carrying a column named
`entry_ms` (F-SCALP (o) must go RED).

**L-S.31 F-SCALP** — "F-SCALP (3 scalps hand-walked end-to-end + 3 MISSES verified; fill rule ordering TOUCH ≥ TICK
≥ DEEP by n filled — an inverted order must FAIL)" (contract :119-121)
READING: suite `scripts/tierc12_scalp_fixtures.py`, hosted at TC12-S, transcript `stage_s/FIXTURES_STAGE_S.txt`,
under L-0.14's harness and leg law (BREAK first; each plant caught by its named detector; production against a
fixture-typed second object). It imports no door and not `analytics.value_area` (L-0.22), and it accepts
`--root=DIR`. Each lettered leg is ONE `prove` call and ONE transcript block with the id `F-SCALP [<letter>
<NAME>]` — `F-SCALP [a HAND-3]` … `F-SCALP [p GATE]`. Sample rules are frozen HERE, before any book exists. Key
order = the home panel's order of record, then `known_at_ms` (orders) or `entry_close_ms` (trades) ascending.
Every fixture stream is `numpy.random.default_rng([SEED, crc32("scalp|<block id>")])` (L-0.14); the suite's one
seeded count is leg (e2)'s `N = 10` per home asset — a fixture-typed literal, printed in the transcript header (X
filed no count for this leg: it has no order simulator to mirror).
- **Synthetic legs** (run whatever STATUS says): (d), (i), (p), the constructed-order plants of (c), and (n) on
  the tapes of (i).
- **Real-book legs** (population: the book of P-SCALP-3): (a), (b), (c), (e), (f), (g), (h), (j), (k), (l), (m),
  (o), and the real-tape print of (n). When `regbooks/P-SCALP-3/STATUS.json` reads `CLOSED_BY_PRECONDITION`, each
  prints `CLOSED-NO-BOOK P-SCALP-3` and asserts from files that STATUS says so and lists no arm (BREAK plant: a
  STATUS copy reading `BUILT`, or listing an arm → detector `CLOSED-STATUS`). That is a PASS, and F-ROLL prints
  the fixture `PASS (row closed by precondition: real legs CLOSED-NO-BOOK)`.
- **The hand-sample law of (a) and (b) is L-0.14's:** categories first — the first row of each named category in
  key order. A category with no member prints `NONE-EXISTS <category>`, asserts from the population that its
  count is zero, and its slot is taken by the next unchosen row in key order, printed `FILL`. A population of `n <
  3` rows has ALL `n` verified and prints `ONLY <n> EXIST (contract count 3)` with the count asserted (`EMPTY
  POPULATION` at zero). The leg is GREEN in every such case; a shortfall is printed `FINDING: …` and carried to
  the report as a finding-not-fixed owned by the operator. No leg is RED or VOID on the size or composition of
  the book; only a mismatch between the fixture's derivation and production is RED.

| leg | FAILS IF | planted mutations (each must turn it RED) |
|---|---|---|
| (a) HAND-3 | the three trades chosen by rule from the book of record (the `scored` arm) — H1 the first with a T1 fill and a `T2` exit; H2 the first swing-failure trade exiting `stop` after its fill bar; H3 the first cross trade exiting `time_stop` — re-derived END TO END by code sharing nothing with the builder (the raw 5m slice by explicit path; its own EMA loop from the tape's first bar; the filed 1h and 4h rows as data; `Fraction` tick arithmetic on the tick string; its own bar loop, fee and uncapped funding sums; every step printed) differ from production in any integer, string or price, or in any R figure by more than `HAIRCUT_TOL`. Verified beside by the same rule, where they exist: the first `invalidation`, the first stop on a fill bar, the first `t1_void` | the trigger bar shifted one bar; the limit snapped toward the market; the fill bar taken by TOUCH; T1 credited on the fill bar; maker booked on the stop; funding booked at the capped figure |
| (b) MISS-3 | the three misses chosen by rule from the record's ledger (`S_orders_scored`, holdout by trigger, inside the scored window) — M1 the first `never_touched`; M2 the first `touched_not_through`; M3 the first miss in the direction opposite M1's; beside: the first `cancelled` — are not misses under the fixture's own bar-by-bar TICK test of the whole window, or their class or any of their would-have variants differs from the fixture's own walk | a filled order listed as a miss; the window cut one bar short; the would-have entered at the limit |
| (c) LADDER | L-S.16's per-order inclusion or fill-bar order fails on any order of any of the three ledgers; a sidecar's `n_orders ≥ n_filled_touch ≥ n_filled_tick ≥ n_filled_deep` fails or does not re-count from its ledger | TICK and DEEP swapped inside production ("an inverted order must FAIL"); TOUCH strict; DEEP without its floor, on a constructed order with `deep_atr·ATR < TICK` |
| (d) TICK-FILL | L-S.9, L-S.11, L-S.15: production's snap and fill functions differ from `Fraction` brute force on the enumerated cases (float and exact-`Decimal` inputs); a marketable entry limit exists | TICK as `≤`; float comparison; snap reversed; zero-volume fill |
| (e) ASOF | (e1) BOUNDARY (L-S.3) fails, or an order row ≠ the reader's `stamp()` on its `1h_*` / `4h_*` values. (e2) ACT-BOUNDARY PREFIX. Sample, by a rule frozen here: per home asset, the first 3 orders of each status (filled / expired / cancelled) in each era in key order, plus a tier-seeded draw of N more (N stated here: 10). For each sampled order, three cuts: at its `known_at_ms`; at its resolution close (fill / expiry / cancel); at its exit close. On the 5m tape cut at each instant (`E.load_asof_at`) and the 1h / 4h tables cut at the same instant through the reader, the builder must reproduce: at `known_at_ms`, the order's gates and frozen geometry exactly with status `unresolved_at_end`; at the resolution close, the status and the fill bar; at the exit close, the whole trade row. Leans on F-VA-ASOF [d]. (e3) W≡PIN PREFIX (L-S.25) fails for any walk | `side="left"`; row `k1 + 1`; a fill accepted on `t+V+1`; an acceptance with `known_close_ms` after the cut used; an EMA seeded at the cut; an acceptance event after `W` read by WALK-W |
| (f) FROZEN | any level of any order differs from its recomputation from row `k1`, or changes between τ and the exit | the limit or a target re-read at the fill bar's row; ATR of the fill hour |
| (g) GATES · READ-SET | PERM (no 5m file), SETUP, both triggers, the run and its extreme, recomputed independently, differ; `n_inside_frozen_only` or `S_FUNNEL` does not re-count; `stage_s/READ_SET.json` holds a path outside L-S.1's read set, or a `licence_reads` entry other than the one call | the 4h clause dropped; the lower bound of SETUP removed; `crossover` without its prior-bar clause; the extreme without the return bar; a 1h kline read |
| (h) SEQUENCE | L-S.14's overlap, identity or first-reason law fails | replace-with-newest; admission at an exit bar's close |
| (i) WALK-TABLE | synthetic 5m tapes and synthetic filed-table rows (frames in the filed schemas, built by the fixture from the pins; no door), drive every row of L-S.7's pattern cases, L-S.11's geometry law, L-S.13, L-S.17, L-S.18, L-S.19 and L-S.20; production differs from the table | T1 before the stop; a gap stop booked at the stop price; a target credited at `max(level, open)`; invalidation ignored; the clock from `t`; the void rule removed; a trigger with the POC at the limit admitted |
| (j) STOP | L-S.10: `S`, `R` or `rail_binding` differs from the fixture's arithmetic; a cross order with `R ≠ rail·ATR`; a stop that moved | the rail removed; a stop move |
| (k) RR | L-S.11, L-S.12: an order of record whose POC or T2 is not ahead of its limit, or with `t2_r < rr_min`; a skipped trigger with `t2_r ≥ rr_min`; a refusal whose reason is not the first that holds; the unfiltered twin's law is not the record's minus the reward test alone | the test before the rail; the unfiltered book as record; a `t1_void` trigger refused |
| (l) MISS-TABLE | L-S.23's partition and grid do not re-derive from `S_orders_scored` and `S_miss`; a would-have variant exists whose target is not ahead of its entry | the split walk at maker rates; a miss dropped from the grid |
| (m) REGIME | L-S.24: a stamp differs from the fixture's own loop over the filed series up to `k1` / the 4h as-of bar | the window end at `k1 + 1`; a 4h column at the forming bar |
| (n) FLOW | L-S.2: a pin bent at its door inside production does not move its witness on the tapes of (i) (`PIN-NOT-READ`); the build HALTs when `scalp.validity_bars` is bent (L-S.13's guard). When the row is BUILT the same bends are also run on the tape of the first home asset in panel order and the moved-row counts are printed — a count of zero there is printed, never RED | a literal of equal value in a shadow builder (`PIN-NOT-READ`) |
| (o) VIEWS | L-S.25, L-S.26, L-S.28, L-S.30: the arm identities; the `licence` column; `fill_rule` one each on the three ladder-class sidecars with `scored` the TICK book; a ridden arm's strip rows missing from `strip` or not under its `arm`; an order, refusal or miss table carrying a column of the five forbidden names | a home row altered in the 17-asset arm; TOUCH shipped as `scored`; an order-table copy with a column `entry_ms` |
| (p) GATE | L-S.27: with a planted licence leaf whose word is not `"PASS"` the builder writes anything but STATUS or computes a candidate; the gate's `licence` call is not `("1h", "maker", "holdout")` | the taker row; the ALL era; a closing second item planted in a copy of the spec (caught at filing) |

- **Leg (e2), the details the table leaves out.** The population is the record's ledger inside the scored window
  (`S_orders_scored`, rows with `in_scored_window`, status = `status_at_w`, era = `era_trigger`); a status and era
  class with fewer than 3 orders takes all it has, and the draw takes all the remaining orders where fewer than N
  remain (no leg is RED on a count). An unfilled order has two cuts, not three. The funding tape is cut by
  `E.load_funding_asof_at`; the 1h / 4h rows are `bars(lens, asof_close_ms=cut)` and `events(…,
  asof_close_ms=cut)`; the 5m `LensFrame` is built on fresh arrays (L-S.1), never taken from a symbol-keyed memo.
  The transcript carries the fixed line `leans on F-VA-ASOF [d]: a filed row at bar k equals a door rebuild on
  tapes cut at close_k`. No leg of this suite re-runs a door.
- "Hand-walked" means the fixture's derivation is printed step by step in the transcript, so a reader can follow
  each of the six by eye; it is still a program, and it is the referee.
- **Helper legs the suite also runs** on this stage's files: F-KEY, F-DET, F-COLLAR `[stage_s]` and
  `[regbooks/P-SCALP-3]`, F-GRID `[S_*]`, L-V's F-TRAV `[a · tierc12_scalp]` and `[e · <each arm>]` and F-VA-PINS
  `[e · P-SCALP-3]` (helpers of `tierc12_fx.py`), L-X's F-REGBOOK `[P-SCALP-3]` (a helper of
  `tierc12_score_fixtures.py`), and F-TOLL's book half (L-S.32). It hosts no F-NEST-ASOF: the per-book instances
  are L-V's, at `TC12-V.stamps.s`.
SOURCE: contract :119-121; L-0.14 (the harness; a leg is one `prove` call and one block; the block id grammar; the
leg states; the fixture RNG; the hand-sample law), L-0.19 (CLOSED-NO-BOOK; the roll); OD-2 (cut-tape legs cut the
FILED tables), OD-17; X's F-SFP selection rule (`x_rec/tierc11x/LEANS_X.md:2309`); scout U6 C21, R-33.
RIVALS: samples picked after the book is seen — forbidden by L-0.14. The ladder leg on book totals — L-S.16. A leg
RED because the book came out small — an outcome-dependent stop (OD-17). A prefix leg at one seeded 4h close — it
sees at most the last order before the cut and has almost no power away from it. A cut-tape leg that re-runs the
door — forbidden outside Stage V (OD-2); the filed tables are cut instead.
FAILS-IF: as the table states, leg by leg.

**L-S.32 F-TOLL, THE BOOK HALF** — "F-TOLL (maker bps read, never typed; taker twin == TC-series)" (contract :121)
READING: L-D owns the data half (`F-TOLL [data a]` … `[data g]`, L-D.21) and the reader half (`F-TOLL [reader]`,
L-D.31). The book half, in this stage's suite, is five blocks, `F-TOLL [book t1]` … `F-TOLL [book t5]`: (t1) is
static (synthetic); (t2)-(t5) are real-book legs of P-SCALP-3 and print `CLOSED-NO-BOOK P-SCALP-3` when the row is
closed.

| leg | FAILS IF | planted mutations |
|---|---|---|
| (t1) NEVER TYPED | by AST, the fee path (`tierc12_rangewalk.fee_per_fraction`, this builder's booking function and everything they call) holds a numeric literal outside the structural set, a bps or percent constant, or a rate not read from `E.fees()[stem]` | a typed maker rate; `E.fees()` shadowed by a dict |
| (t2) TAKER TWIN == TC-SERIES | on every row of every arm: `fee_all_taker_r` or `tc_series_net_r` differs from a FRESH `BK.account_l` call on the row's leg by more than `HAIRCUT_TOL`; `taker_twin_net_r ≠ gross_r − fee_all_taker_r − funding_r`; the two-case identity fails (`|taker_twin_net_r − tc_series_net_r| > HAIRCUT_TOL` on a row with `funding_ceiling_bound == False`, or `taker_twin_net_r ≥ tc_series_net_r` on a bound row); the per-fraction form at all-taker rates differs from `acc["fee_r"]` by more than `HAIRCUT_TOL`; `E.fees()[stem]["taker_bps_side"]` is not the lineage's `FEE_BPS_SIDE`; or the bound count printed per arm does not re-count | the twin booked with a maker entry; a card other than the control card; the twin booked with the capped funding |
| (t3) LEGS | a row's maker / taker split is not L-S.21's law re-derived from `exit_reason` and `harvest_i`; `fee_maker_r + fee_taker_r ≠ fee_r`; `net_r ≠ gross_r − fee_r − funding_r`, each within the tolerance; `funding_r` is not the uncapped interval sum; or an arm's sidecar `fee_schedule {path, sha256}` is not what `tierc12_progress.certified` returns for that path | maker on the stop; the time stop booked maker; `funding_r` taken from `acc["funding_r"]` |
| (t4) FLOW | with the maker rate bent at `E.fees()` inside production, `net_r` of any row of the `scored` arm does not move by exactly the maker legs' notional × the bend ÷ R, or `taker_twin_net_r` moves at all | a shadow builder reading TC11's fee file; a cached rate |
| (t5) HAIRCUT | `haircut_net_r` or `taker_twin_haircut_net_r` differs from L-S.22's two laws | slippage on a maker leg; the charter tier of another asset |

SOURCE: contract :121; L-D.21 ("The BOOK half ("taker twin == TC-series") is L-S's"); LX-X2.11 (F-FEE-EQ);
`tc11x_sfp.py:780-792`; L-X.24; OD-10 (the two-case identity).
RIVALS: bit-equality with `account_l` — unattainable (float association); the filed tolerance is the law. "Taker
twin == TC-series" held on every row whatever the cap — it would force the card's funding cap into the twin
(OD-10).
FAILS-IF: as the table states.

**L-S.33 THE COMPUTE PLAN** — ruling O-5; "F-DET hash-identical" (contract :123)
SEAM SETTLEMENTS (`review/SEAM_PASS.json`, 2026-10-09 — part of this reading; each line governs where the text below is silent or differs):
- [seam 1] every flow leg of this section prints L-0.17's fixed line `  [FLOW] <pin> @ <door>: <witness> moved`, which F-TYPED-TOTAL reads at TC12-FIX.
READING:
- **Size (orientation, read at build):** a home 5m tape holds 625,152 to 741,097 bars at TC11's pin (scout U4
  §1.2) plus the top-up; the holdout to TC11's pin is 235,009 bars per asset as the scout counted it (U6 §1.9).
  Seventeen assets in the widest view.
- **Per asset, in one worker:** (1) the 5m frame once (six 8-byte columns over the tape) and the two EMAs
  (`ind.ema` is a Python loop: two passes over the tape); (2) `k1`, `k4` for every 5m bar by two `searchsorted`
  calls and the row gathers; (3) PERM, SETUP and both triggers as boolean masks over the whole tape — O(bars),
  vectorised, FILL-RULE INDEPENDENT; (4) geometry per candidate (exact `decimal` tick arithmetic, a Python step
  per candidate); (5) the rides: each order costs at most `V + T5` bar steps, so a ride is O(candidates × (V +
  T5)) Python steps and can never exceed O(bars) orders. Five walks per home asset share steps 1-4 — TICK, TOUCH,
  DEEP, rr-unfiltered, live-edge — and one, TICK, per asset of the twelve (the 17-asset view); WALK-PIN repeats
  step 5 for EVERY walk (L-S.25), so each walk is ridden twice, to `hi_W` and to `hi_PIN`.
- **No quantity of the plan depends on how many orders exist** — no count was taken while drafting.
- **Process law:** one `spawn` worker per asset, each importing `E` before any I/O; at most 6 workers while the
  1-minute load is below 10, else 2 (O-5); each worker returns its rows and its `E.read_set()` with its result;
  results merged in panel order, then key order, before any write; one 5m tape per process (`BK._FRAMES`, keyed
  with the lens). Worker count and load go to `progress/TC12-S.json` only.
- **F-DET:** the whole stage twice, in fresh subprocesses under the two hash seeds of L-0.20, into `_det_stage_s/`;
  byte-identical parquet, sidecars, manifests, `READ_SET.json` and `STAGE_S.md`. The builder draws no random
  number; the suite's one seeded draw is leg (e2)'s.
- **The stage's 5m reads** are declared for L-0's `FIVE_MIN_READERS_T`: TC12-S reads `klines/<stem>_5m.parquet`
  and `funding/<stem>.parquet` of the seventeen stems and no other snapshot file.
- The stamps child `TC12-V.stamps.s` runs after this stage's record is COMPLETE-VERIFIED and is no part of it.
SOURCE: O-5; L-0.7, L-0.10, L-0.20, L-0.30; L-D.27, L-D.28 ("One tape per process"); `engine/indicators.py:17-28`;
scout U4 §1.2, U6 §1.9.
RIVALS: a bar-by-bar Python loop over every 5m bar — O(bars) interpreter steps per book where masks do it once.
A shared order census walked once for all rules — the books are sequenced separately (L-S.16).
FAILS-IF: F-DET on `stage_s/` and `regbooks/P-SCALP-3/`; planted mutations: a set-iteration line in a merge; a
worker count written into the manifest.

**Unverified at drafting — each checked at build, a HALT or a printed count:**
- UNVERIFIED: that the home 5m and 1h tapes stay gap-free through TC12's pin (Stage D's manifest `gap_count`).
  L-S.3's freshness guard, L-S.7's `run_cut_at_gap` and L-S.13's `cancel_other` count any exception.
- UNVERIFIED: that every hand-sample class of F-SCALP (a), (b) has a member. An empty class prints `NONE-EXISTS`
  and its slot is FILLED; a book with fewer than three trades or three misses prints `ONLY <n> EXIST` and is
  carried as a finding (L-0.14); nothing turns RED on a count.
- UNVERIFIED: that L-G's two tide tables carry the columns L-S.24 reads (the asset's run and band; the home-five
  determined-young count). A column that is absent is filed NULL with the reason and listed as a finding — never
  recomputed here.
- UNVERIFIED: the maker rate (Stage D's capture), hence the figure the scorer prints as `licence_at_maker_pin`,
  and `deep_floor_binding`'s share under TC12's own tick capture.
- UNVERIFIED: O-27's "never looser" (L-S.15), until `TICK_GRID_AUDIT.json` prints.

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · P-SCALP-3

- **id:** P-SCALP-3
- **family:** SCALPER — the family header is contract :82, "STAGE S · SCALPER FAMILY (m=1, bar 0.10) — exists by
  the "maker" ruling:"; text of record :83-106 (slice sha `fa141ec5…2198`, L-X.17).
- **family_m:** 1 — parsed from :82 by L-X.1's `R_FAM` (group 3); never typed.
- **family_bar:** 0.10 — parsed from :82 (`bar 0.10`, group 4) and asserted equal to q ÷ m with q parsed from :9
  ("bar = 0.10 ÷ m per family"); at m = 1 the bar is on record and does not bind (L-X.8).
- **prior:** 30 — parsed from the text slice's `[30%]` (:83).
- **mechanism:** Inside a 1h value area that the 1h machine reports INSIDE, price that reaches the outer third
  near an edge tends to rotate back toward the POC and the far edge — the "edges respected" leg TC11-X licensed for
  the 1h lens at the maker toll and at no other. A limit resting AT the edge is the only entry that pays the maker
  fee, which is the only toll at which the 1h lens may trade a range. The 5m clock supplies timing and nothing
  else: an EMA cross toward value near the edge, or a failed 5m excursion beyond it. The trade is falsified by 1h
  acceptance beyond the faded edge and is bounded in time by the tuning-fit 1h traverse. The hazard is the fill
  itself — a resting limit is filled preferentially when price is going through it — so the row is judged on the
  book whose fills require a trade-through and is closed if it clears only when a touch is taken as a fill.
- **population:** the five home assets (L-D's home panel), pooled, both directions; lens of the clock 5m, lens of
  the value area 1h, permission from 1h and 4h; era HOLDOUT by the fill bar's close, `ERA_CUT < entry_close_ms`,
  with `ERA_CUT` = `research_outputs/tierc12/x_rec/tierc11x/pins/PINS_X.json["era_cut_ms"]`; scored window per
  O-9: `entry_close_ms ≤ W` and `exit_close_ms ≤ W` with `W` = TC11's pin
  (`research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`), a position open at `W` marked
  there as `corridor_end`; the bars in (W, TC12's pin] are the forward strip — ridden for every arm, printed,
  never scored [L-S.25].
- **arms:**
  - `scored` — the THROUGH-TICK book; there is no base arm (the row is ruled vs zero). Decision at a 5m close τ
    on row `k1` of `va_bars_1h` and row `k4` of `va_bars_4h`, the last lens bars with close ≤ τ, read as filed
    [L-S.3]. PERMISSION: 1h `state == INSIDE` and 4h state neither UNDEFINED nor accepted against the direction
    (ACCEPTED_BELOW for a long, ACCEPTED_ABOVE for a short), read once at τ [L-S.4]. SETUP: the 5m close's
    %-of-value against the in-force 1h profile between 0 and 33 inclusive for a long, between 67 and 100 inclusive
    for a short (33 / 67: contract :87; 0 and 100: the edges of value) [L-S.5]. TRIGGER: the engine EMA12 / EMA89
    (:89) of the 5m close crossing in the direction on that bar with the close within 0.25·ATR_1h (:90) of the
    edge on the value side, OR that close back inside value after the previous 5m close beyond the edge; a double
    trigger is a swing failure [L-S.6 … L-S.8]. ORDER: one unit at the edge snapped to the tick grid away from the
    market (a BUY limit floored, a SELL limit ceiled), all geometry frozen at τ; stop by `BK.brk_stop` from the
    limit — 0.5·ATR_1h (:97) beyond the swing failure's deviation extreme (every 5m low / high since the first
    close beyond, the return bar included), else from the limit, railed at 1.0·ATR_1h (:98; so R is exactly
    1.0·ATR_1h on cross orders); T1 = POC and T2 = far edge − 0.25·ATR_1h (:99) on the grid; REFUSED, with the
    first reason that holds, when the stop is undefined (`stop_none`), when T1 is not ahead of the limit
    (`poc_not_ahead`: `d·(n_T1 − n_L) ≤ 0`) or when T2 is not ahead of the limit (`t2_not_ahead`: `d·(n_T2 − n_L) ≤
    0`); T1 void when it lies at or beyond T2, the whole position then exiting at T2; a T1 within the round-trip
    taker fee of the limit is traded as written and flagged; SKIPPED (`rr_min`) iff `d·(T2 − L) / R < 1.5` (:100);
    valid for bars t+1 … t+12 (:92); cancelled at a 1h acceptance on the faded side; one resting order and one
    position per asset, a trigger meanwhile refused, never a replacement [L-S.9 … L-S.14]. FILL: the first valid
    bar with `low < limit − 1 tick` (long; :94) in exact integer ticks, at the limit price; no fill on a
    zero-volume bar [L-S.15]. WALK: on the fill bar the stop is tested and no target credited; then per 5m bar: a
    bar opening at or beyond the stop exits at the open; else the stop, adverse-first, at the stop price; then T1
    (half) at its level; then T2 (the rest) at its level, on the same bar if reached; a target fills by the same
    through-tick rule and books its level with no gap improvement; then at the close the invalidation at a 1h
    acceptance on the faded side, then the time stop at the fill bar + the tuning-fit 1h traverse in 5m bars, then
    the corridor end; no trail, no stop move, no add [L-S.17 … L-S.20]. COST: maker bps on entry, T1, T2; taker on
    stop, time stop, invalidation and mark; interval-sum funding from the fill bar by `BK.account_l`, uncapped (the
    D12 ceiling is a v6-card rule and is not a rule of this trade); `net_r = gross_r − fee_r − funding_r` in R
    [L-S.21].
  - `ladder__touch` — the same simulator with every resting limit filled on a touch (`low ≤ limit` for a long;
    :94), its own order sequence [L-S.15, L-S.16].
  - `ladder__deep` — the same with every resting limit filled only through by `max(0.05·ATR_1h, 1 tick)` (:94-95;
    the floor is ruling O-32's), rounded up to whole ticks and frozen at τ, its own order sequence [L-S.15,
    L-S.16].
  - `tierE__full_corridor` — every row of the `scored` walk with `entry_close_ms ≤ W`, the tuning era included
    [L-S.25].
  - `tierE__panel17` — the `scored` simulator on the seventeen assets of the snapshot, holdout by fill; the five
    home assets' rows equal `scored`'s; the twelve run on the CLASSIC5 lookback and traverse and carry no licence
    (`licence = none — CLASSIC5 word transplanted`) [L-S.26].
  - `tierE__rr_unfiltered` — the `scored` simulator without the reward test and with nothing else removed (the
    three refusals stand), its own order sequence [L-S.12, L-S.26].
  - `tierE__live_edge` — the `scored` simulator in which an order still unfilled and not cancelled at the one 1h
    close inside its window is re-priced for the later bars from the row of that close (limit, stop, targets,
    the refusals and the reward test again; same direction, trigger kind and extreme; the window not extended)
    and is cancelled if the new limit is marketable against that close or the new geometry is refused or
    skipped; everything frozen once filled; its own order sequence [L-S.26].
  - `strip` — for every ridden arm, under the column `arm`, the rows of that arm's second ride with `W <
    entry_close_ms ≤ PIN`; `tierE__full_corridor` shares `scored`'s rows and is not repeated; rows and counts only
    [L-S.25].
  - inputs pinned: Stage V's `va/va_bars_1h.parquet`, `va/va_bars_4h.parquet`, `va/va_events.parquet`,
    `va/VA_MIRROR.json` and `va/TRAVERSE.json`; Stage D's `data/fee_schedule.json`, `data/CONTRACT_SPECS.json` and
    the 5m and funding tapes of its manifest; `tide/tide_bars_4h.parquet` and `tide/breadth_4h.parquet`;
    `scripts/tierc12_rangewalk.py`; `scripts/tierc12_regbook.py` — each held to the sha that the last progress
    record naming it certifies (`tierc12_progress.certified`); X's `tierc11x/exit/build_manifest.json`,
    `tierc11x/sfp/build_manifest.json` and `scripts/tc11x_pct.py` by their `X_REC_MANIFEST.json` rows. A mismatch
    HALTs the stage.
  - VA columns read (declared for F-VA-PINS (e)): from `va_bars_1h`: `close_ms`, `state`, `val`, `poc`, `vah`,
    `atr`, `va_age`; from `va_bars_4h`: `close_ms`, `state`; from `va_events`: `lens`, `kind`, `side`,
    `known_close_ms`, `by`, `bars_out`, `E` (rows selected by the key column `asset`). Read beside, deciding
    nothing: `inside_frozen_only` of `va_bars_1h` (one printed count, L-S.4) and `l_label` of `va_bars_1h` (the
    lookback's label, carried on every order row and in every arm's sidecar `description`, L-S.29). No 12h, 1d or
    1w column.
- **statistic:** mean(`net_r`) of the `scored` book (L-X's common clause).
- **comparison:** vs zero. The bootstrap of record (O-22; L-X.3, L-X.4, L-X.6): whole-asset clusters,
  `tierc5.cluster_boot`, `N_BOOT` draws read from `research_outputs/tierc11/scores/SCORES.json["n_boot"]` (4000 on
  file), the 5th / 95th percentile interval of `tierc5._ci_from`, `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a
  Fraction, seed 20261008 (contract :4) passed explicitly, sensitivity seed 20260816 (`SCORES.json["seed_sens"]`)
  printed beside. The two ladder books are ruled with the same ruler, seed, draws and bar.
- **preconditions:**
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas,
    selector: licence["1h|maker"].by_era["holdout"].would_read, required: "PASS"} — X's filed word for
    POOLED:CLASSIC5 · holdout · va_regime · 1h · maker, mirrored from
    research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet (sha256
    ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0); it is this row's only precondition.
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of
  the draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at
  least one row in every arm the ruler reads; else NOT SUPPORTED. m is
  fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number ·
  no test spent', spends no test and never loosens the bar. Bootstrap of record: asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. At m = 1 the bar does not bind and the bar cell prints
  '0.10 (not binding at m = 1; decided at the 5th percentile, clause (a))'. THE PRE-NAMED KILL (L-X.9's table,
  verbatim in content). For each fill book X ∈ {TOUCH, TICK, DEEP}, at the seed of record and this bar, exactly
  one of three states holds: U(X) = X is not PANEL COMPLETE (clause (c) fails on X; its ruler is undefined; an
  EMPTY BOOK is the limiting case); C(X) = X is PANEL COMPLETE and clauses (a) and (b) hold on X; F(X) = X is
  PANEL COMPLETE and (a) or (b) fails on X. D = fewer than 3 of 5 leave-one-asset-out panels of the TICK book
  exclude zero from above (contract :106; L-X.11). A closure word needs a MEASURED failure: a book whose ruler is
  undefined is not a failed book. The ten cases, exhaustive, written TICK · D · DEEP · TOUCH → word, qualifier:
  (1) C · false · C · any → SUPPORTED; (2) C · false · F · any → SUPPORTED, qualifier FILL-SENSITIVE (does not
  clear under DEEP); (3) C · false · U · any → SUPPORTED, qualifier FILL-SENSITIVE (DEEP PANEL INCOMPLETE); (4) C ·
  true · any · any → NOT SUPPORTED, qualifier LOAO BELOW THE LINE (k/N above; passing when dropped: <assets>;
  failing when dropped: <assets>); (5) U · any · any · any → NOT SUPPORTED, qualifiers PANEL INCOMPLETE (…) or
  EMPTY BOOK, and TICK PANEL INCOMPLETE — closure not ruled; (6) F · any · C · any → NOT SUPPORTED; (7) F · any ·
  U · any → NOT SUPPORTED, qualifier DEEP PANEL INCOMPLETE — closure not ruled; (8) F · any · F · C → NOT
  SUPPORTED — CLOSED, qualifier (clears only under TOUCH); (9) F · any · F · U → NOT SUPPORTED — CLOSED, qualifier
  TOUCH PANEL INCOMPLETE — "for good" not ruled; (10) F · any · F · F → NOT SUPPORTED — CLOSED FOR GOOD. The words
  this row can read are exactly five: SUPPORTED, NOT SUPPORTED, NOT SUPPORTED — CLOSED, NOT SUPPORTED — CLOSED
  FOR GOOD, CLOSED BY PRECONDITION. One test is spent, by the TICK book; TOUCH and DEEP are ruled with the same
  ruler, seed, draws and bar and can never produce SUPPORTED. The verdict text is the cell (word, qualifiers,
  label) followed by the fill-sensitivity row, which opens with the fixed sentence "TOUCH and DEEP are fill-model
  twins, not tests: they are ruled at the family bar without a test of their own and can only qualify a SUPPORTED
  cell or choose among the failure words; an interval that excludes zero on either is not a result." and prints
  per fill rule the book's own n, point, interval, p and its state C / F / U, then the two booleans
  fails_under_deep_too = F(TICK) and F(DEEP), and clears_only_under_touch = F(TICK) and F(DEEP) and C(TOUCH);
  then the LOAO line k/N with the fixed sentence "the contract reads one-asset dependence by this line (:106); a
  panel that fails when an asset is DROPPED leans on that asset, a panel that fails while an asset is KEPT is
  dragged by it"; then the single-trade share of record (no threshold; it decides nothing); then the per-order
  ladder counts of the TICK ledger and, where the three books' own n are not ordered, the line
  BOOK-N-NOT-MONOTONE (the books are sequenced separately; their n are not comparable order for order). Printed
  beside the licence word, deciding nothing: the scorer's collared leaf licence_at_maker_pin — the licence row's
  edge leg re-derived at Stage D's pinned maker rate from the columns VA_MIRROR.json quotes, labelled "a
  re-derivation of one leg from printed columns; not a licence"; if its edge_net_h20_at_pin <= 0 the cell carries
  the qualifier LICENCE EDGE ≤ 0 AT THE PINNED MAKER RATE (X assumed <x> bps round trip; pinned <y>), and the row
  is still built, scored, and spends its test. Printed beside, deciding nothing: the sensitivity seed, the haircut
  and all-taker twins and the all-taker haircut twin — with the sentence "No cost twin prices a maker fill's
  adverse selection — a maker leg carries zero slippage in both. The only proxy in this row is the fill ladder
  (TICK against DEEP)." —, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column,
  the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with
  VERDICT RESTS ON OPEN MARKS, the forward strip unscored. Tier-E arms carry no verdict word. This registration
  carries pre_seen (KIN-SEEN) and prints '<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed
  value-area swing-failure outcomes on these bars)'.
- **labels:**
  - pre_seen — tag: KIN-SEEN; label: NOT CONFIRMATORY; text: "TC11-X printed outcomes of fading 1h value-area
    edges on these same bars — the 1h maker feasibility row this trade is licensed by (outer 20% of value, H20
    exit, both legs at X's assumed maker toll, holdout) and X3's 1h value-area swing-failure table — while this
    trade form (a resting limit at the 1h edge on the 5m clock, through-tick fill, split targets, taker stop) was
    never scored; X's standing ledger line marks any later value-area registration pre_seen for bars ≤
    2026-09-25T00:00Z and every scored bar of this row is at or before that instant; the feasibility word was
    earned on X's record machine, not on V2 (DISCLOSURES D-2, D-3); the lookback and the traverse are tuning-fit
    and out-of-sample on the holdout."; items:
    `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha `ea8573b3…b6f0`; row POOLED:CLASSIC5 ·
    holdout · va_regime · 1h · maker), `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha
    `a03ef134…91b0`; lens 1h, detector va, trade swing_failure), the standing line at :2468-2470 of
    `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md`, and `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:**
  - `ladder__touch`, `ladder__deep` — the contract's fill-sensitivity row: ruled at the family bar without a test
    of their own, part of the verdict text (L-X.9's named exception to the collar), no verdict word of their own.
  - the all-taker twin `taker_twin_net_r` (the TC-series toll, uncapped funding), with `tc_series_net_r` (the
    lineage's own booking, funding ceiling included) and the count of rows the ceiling binds — Tier-E, no verdict
    word.
  - the charter-slippage twin `haircut_net_r` (AM-7, taker legs only) and `taker_twin_haircut_net_r` (AM-7 on
    every fill of the all-taker twin) — Tier-E, no verdict word.
  - `licence_at_maker_pin` (the licence row's edge leg re-derived at the pinned maker rate from printed columns;
    not a licence) — Tier-E, no verdict word.
  - `tierE__full_corridor` (five home assets, every era inside the scored window; lookback and traverse in-sample
    on its tuning rows), by the leaf `arm__full_corridor` — Tier-E, an interval and no p, no verdict word.
  - `tierE__panel17` (seventeen assets; CLASSIC5 pins transplanted; no licence for the twelve), by the leaf
    `arm__panel17` — Tier-E, an interval and no p, no verdict word.
  - `tierE__rr_unfiltered` (the book without the "rr-min" skip, re-walked), by the leaf `arm__rr_unfiltered` —
    Tier-E, an interval and no p, no verdict word.
  - `tierE__live_edge` (the limit re-priced at the 1h close inside its window), by the leaf `arm__live_edge` —
    Tier-E, an interval and no p, no verdict word.
  - the MISS table and grid (every unfilled order of the scored window; the would-have at the trigger close as a
    taker, at T1, at T2 and split) — Tier-E, no interval, no verdict word, never netted into a book.
  - the per-order ladder counts, the funnel, the regime-column occupancy, the descriptive slices (per asset, per
    direction, per trigger kind, triggers on a 1h close, void T1) and the printed counts (rail binding on cross
    orders, T1 within the fee band, gap stops and gap targets, targets marketable at placement, invalidations by
    moved edge, orders on an hour that is INSIDE by the frozen edge only) — Tier-E, no verdict word.
  - `strip` (every ridden arm's fills after TC11's pin through TC12's) — unscored: n per arm and a pointer only.
  - L-X.14's common set (`seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip`) — Tier-E, no verdict word.
- **failure_conditions:** F-SCALP [L-S.31], one block per leg, each FAILS IF: [a HAND-3] a rule-chosen trade
  re-derived end to end by independent code differs from production; [b MISS-3] a rule-chosen miss is not a miss
  under an independent bar-by-bar test, or its class or would-have differs; [c LADDER] the per-order inclusion
  TOUCH ⊇ TICK ⊇ DEEP, the fill-bar order or a ledger's four counts fail — an inverted order must FAIL; [d
  TICK-FILL] the snap or a fill test differs from exact rational arithmetic, or a zero-volume bar fills; [e ASOF]
  a boundary read, an act-boundary prefix on cut tapes and cut filed tables, or the W-versus-PIN prefix differs;
  [f FROZEN] a level of an order changes after the trigger; [g GATES · READ-SET] a gate recomputed independently
  differs, or a path outside the declared read set was opened; [h SEQUENCE] two orders or positions overlap, or a
  refusal's reason is not the first that held; [i WALK-TABLE] production differs from the synthetic walk table;
  [j STOP] a stop, R or rail flag differs, or a stop moved; [k RR] the geometry refusals or the reward test
  differ from their law; [l MISS-TABLE] the MISS partition or grid does not re-derive; [m REGIME] a regime stamp
  reads past its as-of bar; [n FLOW] a pin bent at its door moves nothing; [o VIEWS] an arm identity, a label, a
  fill rule or a strip row is wrong; [p GATE] a failed licence word does not close the row. F-TOLL, book half
  [L-S.32]: [book t1] a fee rate is typed; [book t2] the taker twin is not the TC-series toll (a two-case
  identity on the funding ceiling); [book t3] a leg's rate, the fee split, the net law or the uncapped funding
  fails; [book t4] the maker rate bent at its door does not move net_r exactly; [book t5] a haircut law fails —
  with L-D's F-TOLL [data a..g] and [reader]. L-V's F-TRAV [a · tierc12_scalp] and [e · <each arm>] (a typed
  time stop, or a row's T not the pinned traverse), F-VA-PINS [e · P-SCALP-3] (a 1w column read) and F-NEST-ASOF
  [P-SCALP-3__<arm>] (a leaked future profile in a stamp). L-0's F-NOT legs 5M, TRAIL-OFFSET, ADDS, PIVOT-RANGE,
  1W and LICENCE, F-CLOSURE with this builder in the decision set, F-HOOK-ESCAPE, F-WALL, F-TYPED. The common
  F-REGBOOK [P-SCALP-3], F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET, F-COLLAR. Every leg's planted
  mutations are stated in the reading cited; when this row is closed by precondition the real-book legs print
  CLOSED-NO-BOOK P-SCALP-3.

### OPEN TO OPERATOR

1. **DEEP's floor.** The contract writes DEEP as "through by 0.05 ATR_1h" (:94-95). On part of the tape that is
   under one tick, where DEEP would be looser than the fill of record and "fails under DEEP too" would be read on
   a twin that is not deeper. DEFAULT if silent (O-32): DEEP = through by `max(0.05·ATR_1h, 1 tick)`, rounded up
   to whole ticks, with the share of orders where the floor binds printed per asset (L-S.15). The literal reading
   is the operator's to order; the per-order ladder assertion would then be dropped for the orders it breaks.
2. **A published maker rate at which X's edge leg is not above zero.** DEFAULT if silent: the row is built and
   scored, with the re-derived figure printed beside the word (O-19). Closing the row on it is the operator's
   order, by name, before Stage D's fee capture.
3. **The 17-asset view** needs the twelve's 5m tapes, which Stage D's sentence does not list (:19-20) and which the
   snapshot carries under O-8. DEFAULT if silent: built from those tapes, Tier-E, every row of the twelve labelled
   as carrying no licence (L-S.26). "NA for the twelve" is the alternative.
4. **One-asset dependence.** L-X.9 reads the LOAO clause as part of the kill (a TICK book that clears but fails
   LOAO 3/5 reads NOT SUPPORTED, qualifier `LOAO BELOW THE LINE (…)`); this section carries that rule. DEFAULT if
   silent (O-32): as L-X.9. Reading it as a qualifier on a SUPPORTED word is L-X.9's rival (ii), the operator's to
   name. The single-trade share has no threshold anywhere and decides nothing (L-X, OPEN TO OPERATOR 1).
5. **What CLOSED and CLOSED FOR GOOD forbid.** DEFAULT if silent: the standing lines of L-S.28, carried into the
   ledger append. The operator may word a closure's reach differently before the freeze; after a verdict it is an
   amendment that cannot follow from the outcome.
6. **CLOSED versus CLOSED FOR GOOD when TICK and DEEP fail and TOUCH clears.** Both contract clauses hold there
   (:104-105). DEFAULT if silent: `NOT SUPPORTED — CLOSED` (clears only under TOUCH), so that each clause has a
   live event; the literal-order rival (CLOSED FOR GOOD whenever TICK and DEEP fail) is the operator's to name.
   (The same item is L-X's OPEN TO OPERATOR 7.)
7. **The stop's else-clause never binds.** With the stop measured from the limit at the edge, "0.5 ATR_1h beyond
   the edge" (:97) is always inside the 1.0 ATR_1h rail (:98), so every cross-triggered order has R = 1.0·ATR_1h.
   DEFAULT if silent: the contract as written (the rail governs); the count of cross orders and `rail_binding` is
   printed. A cross stop at 0.5 ATR_1h with no rail is the operator's order.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

- **L-0 (laws / process).** The pin rows of L-S.2 under L-0.17's names of record (`scalp.*`, `rr_min`,
  `traverse.1h.in_5m_bars`, `fee.maker_bps_side.<VENUE>`), the `word_map` for "half" (:99), and the veto tokens by
  `VETO_ROWS_T` ("outer-third" → the two thirds rows; "validity"; "fill"; "rr-min" → `rr_min`; "era";
  "maker-bps"). `tierc12_asof.asof_index`; `tierc12_units`; `tierc12_progress.certified`; the harness, the block
  grammar, the leg states (`CLOSED-NO-BOOK`), the fixture RNG and the hand-sample law (L-0.14, L-0.19); the helper
  legs F-KEY, F-DET, F-COLLAR, F-GRID, F-TRAV [a], [e], F-VA-PINS [e] of `tierc12_fx.py`. The start law of L-0.10
  for TC12-S, with the `depends_on` of L-S.1. `FIVE_MIN_READERS_T` holds TC12-S with the read set of L-S.33. The
  scalper's two `ema` call sites are the two lines of `tierc12_scalp.ema_pair`. F-NOT's columns for this book:
  `edge_px` (against the in-force `val` / `vah` of `va_bars_1h` row `k1`), `n_stop_moves`, `stop_px_at_exit`,
  `n_entry_fills`, and the VA-column list of L-S.1. **Class of the builder:** `scripts/tierc12_scalp.py` is a
  decision module that reads filed columns through the reader (O-29); there is no runner class. **One point for
  F-NOT's LICENCE leg:** this row's licence pair is `1h|maker` — the value-area lens of the lane `scalp_va_1h` and
  the maker toll — while every sidecar's `lens` is `5m` (the clock, which L-X.24's entry-bar law reads); the leg
  must take the pair from the lane and the toll, not from the sidecar's `lens`.
- **L-D (substrate / env).** `E.fees()[stem]` with `maker_bps_side`, `taker_bps_side`, `slippage_bps_side`;
  `E.ticks()`; `E.BK` (`tierc10_brk`: `frame_l` on "5m" with funding, `LensFrame`, `account_l`, `brk_stop`),
  `E.TP.CONTROL_CARD`, `E.R2`, `E.R3`, `E.R4`, `E.LENS_MS`, `E.era_of`, `E.TC11_PIN_MS`, `E.PIN_MS`,
  `E.ERA_CUT_MS`, `E.CLASSIC5`, `E.PANEL17`, `E.load_asof_at` and `E.load_funding_asof_at` (any instant `≤ PIN`
  admitted), `E.x_rec`, `E.read_set()` and the `READ_SET.json` it feeds. `TickGrid` as L-D.23 specifies it:
  `floor_ticks` / `ceil_ticks` take a `float` or an exact `decimal.Decimal` (L-S.11's T2, L-S.15's DEEP depth).
  The NO-TRADE default for zero-volume 5m bars (L-D.16) is adopted unchanged. `x_rec` rows this section reads:
  `tierc11x/exit/build_manifest.json`, `tierc11x/sfp/build_manifest.json`, `scripts/tc11x_pct.py`.
  `TICK_GRID_AUDIT.json` is printed beside the fill tables.
- **L-V (value area).** `va_bars_1h` / `va_bars_4h` for all seventeen assets with the columns of L-S.1 (the
  in-force `val, poc, vah`, `atr`, `state`, `va_age`, `close_ms`, and beside them `inside_frozen_only`,
  `l_label`); `va_events` acceptance rows with `side`, `known_close_ms`, `by`, `bars_out`, `E`; the reader's
  `bars`, `events`, `licence`, `traverse` (and `stamp`, called by this stage's fixture only), each read
  sha-asserted. The licence leaf quotes X's columns for the scorer's `licence_at_maker_pin`; no block is computed
  for this section. The V5 stamps are answered by L-V.19: the scalper's books are stamped at `TC12-V.stamps.s`
  from `stage_s/S_orders_<book>.parquet`, with the kind L-S.30 declares — its `end_col` (`resolution_close_ms`),
  the per-row `ev_exit_stamp` and `open_at_asof` are this section's names for what L-V.19's table leaves unnamed.
  What L-V left
  to this section is decided here: the order geometry (L-S.3, L-S.9), the lens-close instant (L-S.3), the anchor
  of `T_in_5m_bars` (the fill bar, L-S.20), cancellation and invalidation on an `acceptance` event (L-S.13,
  L-S.19).
- **L-X (statistics / registrations / close).** L-X.9's table is carried row for row; the regbook interface (arm
  names, the twenty columns and the conditional three, sidecar keys, STATUS, the fee identities) is built to
  through `scripts/tierc12_regbook.py`, filed at `TC12-ENV.score-build`; the era of a row is its fill bar's close.
  The ladder law is settled: OD-6 — `LADDER-ORDER` is on the four per-ledger counts of the three ladder-class
  sidecars, and the arm totals are printed with `BOOK-N-NOT-MONOTONE` in the row's `disclosures[]`. The scorer
  computes `licence_at_maker_pin`, rules `taker_twin`, `haircut` and `taker_twin_haircut`, and writes one
  `arm__<slug>` leaf per `tierE__` arm of this row's STATUS. The spec block above is written to L-X.18's field
  grammar (bare checked values; one brace item; `arms` sub-bullets; one `labels` sub-bullet; the KIN-SEEN
  template). The `strip` sidecar is written with `fill_rule` null, `era_scope` holdout and `panel` the seventeen
  stems, since it holds rows of several arms.
- **L-G (admission).** The regime columns "breadth" and "4h tide age" are read from `tide/breadth_4h.parquet` and
  `tide/tide_bars_4h.parquet`, which are `TC12-C.tide`'s (blocking; this stage's record depends on it), by as-of
  on `close_ms`, as filed; L-S defines nothing about them and re-derives no band. If a column L-S.24 names is
  absent, the regime column is filed NULL with the reason and listed as a finding — never recomputed here.
- **L-R (range-state).** One geometry law (OD-8) and one gap law (OD-9) for both rows, written in L-R.14 and
  L-R.19 and carried here in integer ticks; `rr_min` is one pin. L-R's `fee_per_fraction` is the one function
  (`tierc12_rangewalk.fee_per_fraction`, filed at `TC12-R.sfp`, taking the per-leg rates of X's signature), which
  is why this stage starts after `TC12-R.sfp`. One fill law for every maker row in the tier (OD-11): L-R's
  conditioned maker twin fills by L-S.15's through-tick test.
- **L-C (control).** Nothing is read from the v6 book. The strip law (O-9) is applied as L-S.25 states.
- **L-L (ledger / era / ferry).** The ferry classes are typed in L-L.25 from the keys L-S.30 declares: the eight
  arms, `S_orders_*`, `S_refusals_*`, `S_miss` and `open_at_w_continued` PER-TRADE (FERRIED); the `stage_s` grids
  POINTED. The stamp tables are L-V's.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None against a ruling. This section conforms to O-1..O-32; O-9, O-14, O-17, O-19, O-20, O-22, O-23 and section H
(O-25..O-32) were checked against the files this section cites and none was found wrong on a fact it rules. Three
notes that are not objections:
- O-27 (the recorded tick is "stricter than history" only where the tape's observed granularity is not coarser
  than it; "never looser" is UNVERIFIED until the audit prints) bears directly on the fill of record; this section
  prints the audit beside every fill table (L-S.15).
- O-9 defines the holdout by the ENTRY bar's close. An unfilled order has no entry bar; orders are era-tagged by
  the trigger close and trades by the fill close, and the at-most-one straddle per asset is counted (L-S.25).
- O-19 orders the maker-rate difference "printed beside" the licence word. L-S.27 prints the re-derived edge leg
  beside the word (O-19, OD-12) as the scorer's leaf `licence_at_maker_pin`; it closes nothing.
