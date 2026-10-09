## L-R · THE RANGE-STATE FAMILY

This section governs Stage R of the contract (lines 64-80) and the two fixtures the contract names for it (F-DIR,
F-SFP; :118-119). It fixes: the direction gate P-DIR-1 — its population, the as-of instant of the 4h value-area state,
the refusal predicate, its post-filter arms, its Tier-E chop tables; the swing failure as a range trade P-SFP-VA-1 —
event, entry, stop, the two targets, the degenerate geometries, the minimum-reward skip, the time stop, the
invalidation exit, the bar walk, the R-multiple with split targets, the scored window, the licence precondition and its
Tier-E cells and twins; the Tier-E two-trades tables on the value area at 4h and 1d with their lens-above partition,
base rate and null; and the Tier-E 1d value-area edge as a take-profit venue. It owns two registered rows of the
RANGE-STATE family (contract :64): P-DIR-1 and P-SFP-VA-1. It conforms to ORCHESTRATOR_RULINGS O-1..O-24 as written;
one objection is filed at the end (O-11, the scope of "captured-only").

**Drafting record.** Read while drafting, all read-only: the contract (sha256 `861d6050…a7bd`); ORCHESTRATOR_RULINGS
(`c280a972…f509`); DISCLOSURES; scout maps U6 (`8315e351…bc4e`) and U2 (`50109e8b…3aef`); the sibling drafts L-0
(`2c6e9ba5…2a73`), L-D (`9ed43441…79af`), L-V (`5d653d6f…ee1a`) and L-X (`6d1b5055…c263`) as they stood; TC11's
`LEANS.md`, `LEANS_AMENDMENTS.md` (AM-7) and `registrations/REGISTRATIONS.json` (`648834bf…f1ee`); X's `LEANS_X.md` and
`REGISTRATION_PLAN.md` under `x_rec/`; as TEXT, never imported: `x_rec/scripts/tc11x_sfp.py` (`79ba35f4…0f95`),
`x_rec/scripts/tc11x_va.py` (`3f6a43cb…a422`), `scripts/tierc9.py`, `tierc10_brk.py`, `tierc10_null.py`,
`tierc10_census.py`, `tierc5_rules.py`, `tierc7.py`, `tierc11_stage_r.py`, `tierc11_stage_r4.py`, `tierc11_stage_g.py`,
`tierc11_stage_h.py`, `tierc11_ride.py`, `tierc11_nest.py`. Inspections were structural (schemas, key counts, lane and
exit-reason value sets, row counts per variant, sha256). Filed numbers the drafter printed while verifying a fact, none
of them an outcome of a TC12 rule and none used to choose a reading: TC11's R5 alignment rows (the two figures the
contract itself quotes at :67); the row counts of X's filed twin books and event variants; and the sidecar of TC11's
filed P-TP-RNG scored arm (n, Σ net_r and exit-reason counts of the 12h pivot venue), opened to confirm that TC11's
take-profit ride is 4h-granular. No R, mean, hit rate or count of any TC12 book was computed. Counts quoted from filed
records are EXPECTATIONS a fixture reads at run time, never inputs.

**Notation.** Paths are relative to `/Users/luis/Naiad`; `T12` = `research_outputs/tierc12`; `MR` =
`research_outputs/tierc11`; `XR` = `T12/x_rec`. `E` = the TC12 env shim (L-D); `E.BK` = `tierc10_brk`, `E.T9` =
`tierc9`, `E.T7` = `tierc7`, `E.T5` = `tierc5`, `E.TP` = `tierc10_panel`, `E.LN` = `tierc10_lanes` (lineage modules the
shim imports as-is, L-D.29). W = the score edge `E.TC11_PIN_MS` (O-9); PIN = `E.PIN_MS`. For one asset and lens ℓ: bars
`t` with `open_ms[t]`, `o, h, l, c`, `close_ms[t] = open_ms[t] + step_ℓ`; `ATR_ℓ[t]`; `VA(t)` as L-V defines it. `d` =
trade direction, +1 long, −1 short. "The reader" = `scripts/tierc12_va_stamps.py` (L-V.2: data-only, not a door).
"Round6" = the estate's write function `tierc2_baseline._round_floats`. A value written "(on file: v)" is orientation
for the reader; the constant the build uses is the named object, read at run time (L-R.32 lists every one).

---------------------------------------------------------------------------------------------------------------
#### A · P-DIR-1 — the direction gate

**L-R.1 "ANCHOR ENTRY" — THE POPULATION** — "refuse an anchor entry" (contract :65)

READING: An anchor entry is the entry of a campaign of the base book — card v6 as O-21 fixes it: ONE book, bit-equal
on the sixteen regbook columns to TC11's filed v6 (the `base` arm; L-X.25's F-BASE-IDENT against
`MR/scores/BASE_IDENT.json["book_sha256"]`). Every campaign of that book is evaluated by the gate; there is no narrower
population. Three facts make "anchor entry" the whole base: (i) every row of the filed book carries `lane == "card"`
(200 of 200 in `MR/books/v6_campaigns.parquet` and in `MR/books/v6_journal.parquet`) [verified here]; no lane value
"anchor" exists on disk; (ii) the card lane is the lane whose stop is anchored on a confirmed pivot — the ride enters
through `RC.struct_stop_4h` and records the pivot as `Trade.anchor` (`scripts/tierc9.py:397-413`; journal column
`anchor`), which is what the lineage's word "anchor" names for an entry; (iii) a v6 campaign has exactly one entry:
`replay9` HALTs on any lane but "card" and on any add (`tierc9.py:341-346`), and `n_adds == 0` on 200 of 200 journal
rows [verified here]. The gate builder asserts `set(base.lane) == {"card"}` and HALTs `DIR-POPULATION` otherwise.

SOURCE: contract :65; O-21; `scripts/tierc9.py:341-346, :386-414`; `scripts/tierc3_rules.py:237` (`struct_stop_4h`);
`MR/books/v6_campaigns.parquet`, `MR/books/v6_journal.parquet` (certified by `MR/PROGRESS.json` stage TC11-BOOKS);
scout U7 item 9 and R20 (the same finding, independently).

RIVALS: (a) only campaigns whose pivot anchor binds the stop (not rail-bound) — no contract phrase behind it; a second
filter the gate text does not carry. (b) a separate "anchor lane" book — none exists. (c) entries of the 9/12 book too
— the contract says "two-sample vs v6".

FAILS-IF: F-DIR (a): the refused ∪ kept key set must equal the base's key set; mutation: a base row with
`lane = "spring"` planted in a copy must HALT `DIR-POPULATION`.

**L-R.2 THE AS-OF OF THE 4h VALUE-AREA STATE** — "when the 4h VA state is ACCEPTED" (contract :65-66)

READING: The state is read at τ = the campaign's `entry_close_ms` — the CLOSE of its entry bar — as the 4h block of
the reader's stamp at τ (L-V.20): `k = asof_index(close_ms_4h, τ)` (O-14: a bar is visible iff its close ≤ τ), and
`state = 4h_state` = the machine's state AFTER bar k (L-V.13). The entry bar is itself a bar of the same 4h tape, so
`4h_bar_close_ms == τ` and the block is the entry bar's own row; the builder asserts that equality on every campaign
and HALTs `DIR-ASOF` on any difference. So the answer to the contract's open point is: **the state after the entry
bar's close**, in which that close (`c[k]` = the campaign's `entry_px`) has been judged against `VA(k−1)` — or against
the frozen edge of a pending probe — with `ATR_4h[k]`. Nothing later than the close of bar k is read: `VA(k)` itself
judges nothing at k (L-V.8 rule 2).
Why this instant: v6's entry decision is taken at that close and with that bar's own close-time quantities —
`entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])` and the stop from `RC.struct_stop_4h(…, ti, entry_px, d,
atr_sig, …)` (`tierc9.py:394-399`), `entry_ms = open_ms[ti]` (:412). The gate therefore reads no fact the card does
not already hold when it enters. It is the estate's stamp law for an entry: "Close events (arm, entry, harvest, bell,
add, exit at a close) are stamped at their close" (`MR/LEANS.md:221`), and R5 — the table this gate's direction comes
from — read its state at `instant_kind == "entry"` with instant `entry_close_ms`
(`scripts/tierc11_stage_r.py:1319, :1480-1487`).
The value read is the FILED `state` string (L-V.24); the gate never re-derives a state from filed levels.

SOURCE: O-14; L-V.8, L-V.13, L-V.20, L-V.24; `tierc9.py:394-399, :412`; `MR/LEANS.md:219-224` (L-R.5);
`tierc11_stage_r.py:1319, :1480-1487`; L-0.28 (`tierc12_asof.asof_index`).

RIVALS: the state at the last 4h close STRICTLY BEFORE the entry bar's close (row k−1) — the engine's exec-open law
(`engine/htf.py:15-25`), right for an order placed DURING bar k, wrong for a decision taken AT its close; O-14 rules
`≤`. Not taken, and not printed as a book: its effect is disclosed as COUNTS only (L-R.5). The state at the next bar —
a future leak; it is F-DIR's plant.

FAILS-IF: F-DIR (c) and (e); mutations: the predicate fed row k+1; fed row k−1.

**L-R.3 "ACCEPTED OUTSIDE VALUE AGAINST THE TRADE'S DIRECTION" — THE PREDICATE** — "ACCEPTED outside value AGAINST
the trade's direction (accepted below for a long; above for a short)" (contract :66)

READING: With `d` the campaign's `direction` and `s` the string of L-R.2:

    refuse(campaign)  ⇔  (d == +1 AND s == "ACCEPTED_BELOW")  OR  (d == −1 AND s == "ACCEPTED_ABOVE")

`s` is a member of `STATE_NAMES` (L-V.2) compared by exact string equality. Every other case is KEPT: INSIDE;
PROBING_ABOVE and PROBING_BELOW in either direction (a probe is "not yet accepted", contract :34); ACCEPTED on the
trade's own side (above for a long, below for a short); UNDEFINED. "Outside value" is what the ACCEPTED state means
(contract :35) and is not a second condition: the gate applies no position test of its own. Where both sides stand
disarmed the state column reports one side by L-V.13's position rule and the gate follows the column. Each refused row
files `4h_state`, `4h_pct`, `4h_edge_dist_atr`, `4h_accept_age`, `4h_armed_top`, `4h_armed_bottom`,
`4h_bar_close_ms`. Printed counts, deciding nothing: refused by direction; refused with both sides disarmed; refused
whose entry close lies inside the rolling `VA(k−1)` (`0 ≤ 4h_pct ≤ 100`); kept under PROBING against the direction;
UNDEFINED at entry (expected zero: v6's warm floor, `Roles.floor_bars`, is never below the estate's `WARMUP_BARS`,
which exceeds the 4h lookback; the count is printed and such a campaign is kept, not refused).

SOURCE: contract :34-35, :65-66; L-V.13 (the state column; `acc_side`); L-V.16; `scripts/tierc9.py:111-116`
(`floor_bars`).

RIVALS: also refuse PROBING against the direction — the contract says ACCEPTED. Also require the entry close outside
the rolling VA — a second condition with no phrase behind it (its count is printed). Refuse on the 1d state as well —
not in the row's text; the 1d state appears only in the chop table.

FAILS-IF: F-DIR (a), (b), (e); mutations: the sides swapped (refusing acceptance WITH the trade); PROBING treated as
ACCEPTED.

**L-R.4 THE GATE IS A POST-FILTER; THE ARMS; THE STRIP** — "(two-sample vs v6)" (contract :65); O-21, O-9

READING: `regbooks/P-DIR-1/` holds, in L-X.24's interface:
- `base` — the v6 book on the scored window (L-C's control), every row with `entry_close_ms ≤ W`; one canonical
  `book_sha256` equal to TC11's filed value (F-BASE-IDENT).
- `scored` — `base` minus the refused campaigns, by key `(symbol, entry_ms)`; every kept row identical to its base row
  on the sixteen columns (L-X.25 GATE-POSTFILTER). No campaign is re-ridden for the row of record: a refused entry
  does not free its slot (TC11 L-1.5, `MR/LEANS.md:147-148`).
- `strip` — the v6 campaigns of L-C's strip book (`W < entry_close_ms ≤ PIN`) passed through the same predicate at
  their own entry close; n and a pointer only, no statistic (O-9; L-X.14).
The statistic is kept-versus-all (L-X.5). The gate builder is a DECISION module (L-0.22 `NEVER_RUNNER_T`): it reads
value-area state only as filed columns through the reader's `stamp` at the base campaigns' entry instants, and asserts
those blocks equal the `entry` rows of the v6 stamp table (L-V.19) on every column.

SOURCE: O-21, O-9; L-X.5, L-X.24, L-X.25; `MR/LEANS.md:141-150` (L-1.5); L-0.22; L-V.19.

RIVALS: re-ride the gated book as the row of record — a gate removes trades (contract :52); the re-ride is Tier-E
(L-R.5). Score to PIN — O-9.

FAILS-IF: F-BASE-IDENT (L-X); F-DIR (a), (d); mutations: one refused campaign restored to a copy of `scored`; one kept
row's `net_r` moved by one ulp; the un-gated book offered as `scored`.

**L-R.5 THE RE-RIDE TWIN AND THE COUNTED RIVALS** — O-21 "a re-ride twin is Tier-E disclosure"

READING:
- `tierE__reride` — v6 replayed with the predicate evaluated on every CANDIDATE at its own trigger bar's close, a
  refused trigger not occupying the slot: `replay9`'s candidate loop (`T9.card_candidates9`, the same order, one
  position per asset, `ti <= open_until` → `position_open`) with one added site, the refusal — TC11's `replay_g` law
  (`scripts/tierc11_stage_g.py:449-457`). The predicate is L-R.3's, fed the filed `va_bars_4h` row whose `close_ms`
  equals the candidate bar's close. The ride is `T9._ride_leg9`, the booking `T7._account_chain`. With a predicate
  that refuses nothing the twin must equal `base` at 0.000e+00 (canonical sha). Printed: n; `n_admitted_not_in_v6`;
  `n_v6_not_taken`; the first-order rival count from v6's rejection log (`position_open` rejections whose blocking
  campaign the gate refuses); the scorer's CI-only reading of the arm (two-sample vs `base`, collared, no verdict
  word).
- The as-of rival of L-R.2 (row k−1) and the position rival of L-R.3 are disclosed as COUNTS and key lists only —
  `n_refused_prior_bar`, `n_refused_both_readings`, `n_only_of_record`, `n_only_prior_bar` — with no mean, sum or
  interval: a rival reading is not given an outcome to be compared by.

SOURCE: O-21; `tierc11_stage_g.py:449-457, :546-566`; `tierc9.py:386-399`; `MR/LEANS.md:143, :147-148`.

RIVALS: no re-ride at all — O-21 names it. A re-ride book for each rival reading — outcome tables for readings the
row does not take.

FAILS-IF: F-DIR (f): the twin under a refuse-nothing predicate must reproduce `base`; mutation: a hook that marks a
refused trigger `position_open` (the slot stays held) must be caught by the leg's planted pair of adjacent triggers.

**L-R.6 THE LABEL** — "Label: direction informed by TC11 R5 (+0.49 with / −0.49 against, pivot states)" (contract :67)

READING: P-DIR-1 carries `selection_hazard`, tag `DIRECTION-INFORMED` (O-23; L-X.13's shorter template). The two
figures the contract quotes are the cells `calibrated|4h|alignment|EXP_ALIGNED` and `calibrated|4h|alignment|
EXP_COUNTER` of `MR/stage_r/R5_CHOP_DIRECTION.parquet` (sha256
`a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`; rendered at
`MR/stage_r/R5_CHOP.md:120-121`): mean net R on file +0.491349 over 47 campaigns and
−0.493933 over 12, on this same v6 book and corridor, by PIVOT state. The label's `items` cite that file, the two
cells and their `n`. What is new in P-DIR-1 is the detector (the value area's ACCEPTED state, not the pivot machine's
expansion) and the interval; the direction of the refusal was chosen with R5 in view. By schema, no filed TC11 or X
parquet carries both a book-outcome column and a value-area column [verified here: a name scan of every parquet under
`MR/` and `XR/tierc11x/`], so the value-area state has not been tabulated against v6 outcomes on file; the label says
so in those words and claims no more.

SOURCE: contract :67; O-23; L-X.13; the parquet and md as cited [read here]; scout U6 §1.11.

RIVALS: `pre_seen` — the value-area gate's own cohort was never printed; the harsher label would assert a look that
did not happen, and O-23 rules the key.

FAILS-IF: F-REG (TEMPLATE leg, L-X); F-DIR (g): the two quoted cells re-read from the pinned parquet must equal the
label's `items` at the file's precision; mutation: one digit changed in a copy of the label text.

**L-R.7 F-DIR** — "F-DIR (3 refusals hand-verified)" (contract :118-119)

READING: suite `scripts/tierc12_stage_r_fixtures.py`, transcript `T12/stage_r/FIXTURES_STAGE_R.txt`.
- (a) SET. The refused key set equals the fixture's own evaluation of L-R.3 from `va/va_bars_4h.parquet` opened by
  explicit path with the fixture's own linear-scan as-of (last close ≤ τ); kept ∪ refused = the base keys, kept ∩
  refused = ∅; every kept row equals its base row on the sixteen columns; the refused set equals the key set of the
  4h `ACCEPTED_AGAINST` cell of L-R.9's table.
- (b) HAND — three refusals and two kept witnesses, chosen by a rule frozen HERE, before any gated book exists, in
  ascending `(symbol, entry_ms)` order (L-0.14): **D1** the first refused long; **D2** the first refused short;
  **D3** the first other refused campaign whose deciding acceptance is printed at the entry bar itself (the
  acceptance event's `i == k`) — the as-of boundary case — and, if that class is empty (printed NONE-EXISTS with its
  count asserted zero), the first other refused campaign. **N1** the first KEPT campaign whose state is PROBING
  against its direction; **N2** the first KEPT campaign whose state at row k−1 is ACCEPTED against its direction and
  at row k is not (a decay on the entry bar). "Hand-verified" = the fixture's own derivation, sharing no code with
  the module, the door, the reader or the gate: from the raw 4h tape by explicit path, `VA(t−1)` by
  `analytics.profile.volume_profile` on the raw slice, ATR by its own Wilder loop, the V2 clauses written out per
  bar from the start of the value regime that the deciding probe opened in, through the acceptance, through every
  bar to the entry bar (each bar's decay test printed) — yielding the state after the entry bar, compared with the
  filed state and with the gate's decision.
- (c) AS-OF. For every base campaign, the 4h state from the DOOR re-run on the 4h tape cut at τ
  (`E.load_asof_at(stem, "4h", τ)`) equals the filed state the gate read; `4h_bar_close_ms == entry_close_ms`.
- (d) UN-GATED. The un-gated book offered as `scored` must FAIL (a) whenever the refused set is non-empty; if the
  predicate refuses nothing the leg prints `REFUSES-NOTHING` and the scorer's TWO-SAMPLE-PREMISE flag stands (L-X.7).
- (e) TRUTH TABLE. On a synthetic stamp table and synthetic campaigns typed by the fixture — every (direction ×
  state) pair, an acceptance printed on the entry bar, a decay on the entry bar, both sides disarmed — the PRODUCTION
  predicate function returns the fixture's typed answers.
- (f) L-R.5's identity leg. (g) L-R.6's label leg.
- FAILS IF: any set, row, state, hand derivation or typed answer differs. PLANTS, each inside the production
  predicate or on a copy, each caught by its named leg: the state read at row k+1 → (c), (e); at row k−1 → (e), and
  (b) on D3 / N2 where they exist; the sides swapped → (a), (b), (e); PROBING counted as ACCEPTED → (e), and (b) on
  N1; the un-gated book → (d); a refused campaign restored → (a); a state re-derived from filed levels instead of
  read (L-V.24's round trap) → (e) on a typed exact-edge case.

SOURCE: contract :118-119; L-0.14 (the selection law, production against production); L-V.24; X's F-SFP selection
rule (`XR/tierc11x/LEANS_X.md:2309`: "chosen by a frozen rule, never after a look").

RIVALS: three refusals drawn at random — categories exist, so L-0.14 orders the first of each. The reader's stamp as
the hand referee — self-comparison.

FAILS-IF: as stated in the reading.

**L-R.8 THE FULL VA CHOP TABLE** — "Tier-E: the full VA chop table — v6 by 4h and 1d VA state × %-of-value decile at
entry" (contract :67-68)

READING: `T12/stage_r/VA_CHOP.parquet`, a GRID (L-0.15), the value-area form of TC11's R5 (`MR/LEANS.md:284-289`).
- **Population**: the base v6 campaigns of the scored window; strip campaigns are listed apart with their states and
  no statistic.
- **Instant**: τ = `entry_close_ms` (L-R.2), for both lenses; the 1d block is the last 1d bar closed at or before τ.
- **AXES**, declared in this order: `lens` ∈ (`4h`, `1d`) × `state` ∈ `STATE_NAMES` (six, L-V.2) × `band` (the
  %-of-value bands below). The cell count is the product of the three cardinalities, computed; the grid partitions
  the population once per lens (Σ n over a lens's cells == the base's row count).
- **The %-of-value read**: the block's filed `pct` — bar k's own judged column (the lens's last close against
  `VA(k−1)`, L-V.16, L-V.20). At 4h that close IS the entry price. At 1d it is the last closed 1d bar's close,
  `1d_stale_ms` old.
- **Bands** — FIXED, never quantiles of any outcome or of the sample. With `PCT` = `PCT_PER_UNIT` and `n_b` = the
  band count the contract's word "decile" names (pin `chop.n_bands`, L-R.32), `w = PCT / n_b`:
  `pct` null → `na`; `pct < 0` → `<0` (the close is below value); `pct > PCT` → `>100` (above value); otherwise band
  index `min(floor(pct / w), n_b − 1)`, i.e. `[0,w)`, `[w,2w)`, …, the top band CLOSED at `PCT`. The labels are
  generated from `w` and `PCT` (on file: `[0,10)` … `[80,90)`, `[90,100]`). The closed top is the one departure from
  R5's `bucket_of` (`tierc11_stage_r.py:1601-1614`, where `p >= 100` opened `>=100`): L-V.9's INSIDE is the CLOSED
  interval, so a close exactly at VAH is inside value and belongs to the top decile; `<0` and `>100` are then
  exactly "outside value by position". Band levels in order: `<0`, the `n_b` deciles, `>100`, `na`.
- **Cells that cannot hold a row** stay as rows with `n = 0` and `nan_reason = "absent by construction: …"`
  (UNDEFINED with any band but `na`).
- **Columns per cell** — R5's `_stats` / `_cell` law (`tierc11_stage_r.py:1470-1477, :1535-1544`): `n`, `n_long`,
  `n_short`, `mean_net_r`, `p_win` (share with `net_r > 0`), `sum_net_r`, `nan_reason`; the same four for the holdout
  slice and for the tuning slice (era by the entry bar's close). No interval: a descriptive table
  (`would_read_ci_only = "no interval"`, L-0.16, L-0.28). `l_label` carried (the lookback is tuning-fit).
- **Beside**: `VA_CHOP_ROWS.parquet`, one row per campaign (key `(symbol, entry_ms)`): direction, `net_r`, era, both
  lenses' `state`, `pct`, `band`, `alignment` (L-R.9), `bar_close_ms`, `stale_ms`, and the live twin `1d_px_pct` =
  the entry price against the 1d profile in force (L-V.20's live formula); `VA_CHOP_MARGINS.parquet` (per lens: by
  state; by band); the count of campaigns whose `pct` sits exactly on a band edge, per lens (R5's SR-16 disclosure).

SOURCE: contract :67-68; `MR/LEANS.md:284-289` (L-R.7); `tierc11_stage_r.py:168-171, :1470-1477, :1535-1544,
:1601-1636`; L-V.9, L-V.16, L-V.20; L-0.15, L-0.16.

RIVALS: quantile bands fitted on the sample (or on outcomes) — the contract says "decile" of %-of-value, and a fitted
cut is a degree of freedom. R5's half-open top (`>=100`) — moves a close exactly at VAH out of value against L-V.9.
The live entry price against the in-force 1d profile as the 1d read — state and band would stop being coherent
(L-V.20); printed per campaign instead. A 12h or 1w block — the contract names 4h and 1d.

FAILS-IF: F-GRID (`VA_CHOP`: declared cells, partition per lens, n = 0 rows present); F-CHOP: every cell's `n`,
`mean_net_r`, `sum_net_r` recomputed by the fixture from `VA_CHOP_ROWS` and the base arm; a planted campaign with
`pct` exactly `PCT` must land in the top decile; mutations: bands taken as sample quantiles; the top band half-open;
one `n = 0` row dropped.

**L-R.9 WITH-VS-AGAINST ACCEPTANCE** — "with-vs-against acceptance" (contract :68); "§0 … the VA chop table
(with-vs-against)" (:127)

READING: `T12/stage_r/VA_CHOP_ALIGNMENT.parquet`, a GRID: `lens` ∈ (`4h`, `1d`) × `alignment` ∈ (`ACCEPTED_WITH`,
`ACCEPTED_AGAINST`, `PROBING_WITH`, `PROBING_AGAINST`, `INSIDE`, `UNDEFINED`), same population, instant and columns
as L-R.8. WITH = the state's side is the trade's direction: ACCEPTED_ABOVE / PROBING_ABOVE for a long, ACCEPTED_BELOW
/ PROBING_BELOW for a short; AGAINST = the other side (the value-area form of `align_of`,
`tierc11_stage_r.py:1650-1661`). It partitions the population per lens. The 4h `ACCEPTED_AGAINST` cell IS P-DIR-1's
refused cohort: its key set is asserted equal to the refused set. This table, whole, is what the report's §0.2
quotes (L-X.28), collared, with TC11's two R5 cells printed beside as the pivot-state anchor (quoted from the pinned
parquet, L-R.6).

SOURCE: contract :68, :127; `tierc11_stage_r.py:175, :1650-1661, :1687-1717`; L-X.28.

RIVALS: R5's direction-adjusted %-of-range thirds — not asked for the value area; it would add cells with no phrase
behind them.

FAILS-IF: F-GRID (`VA_CHOP_ALIGNMENT`); F-DIR (a) (the refused set == the 4h AGAINST cell); mutation: a refused key
moved to `INSIDE` in a copy of the rows table.

---------------------------------------------------------------------------------------------------------------
#### B · P-SFP-VA-1 — the swing failure as a range trade, 4h

The trade's machinery is X2's (`XR/scripts/tc11x_sfp.py`), MIRRORED into `scripts/tierc12_rangewalk.py` (pure: numpy
only; the bar step, the walk, the per-fraction fee) and held equal to X's FILED trades by F-SFP-MIRROR (L-R.25); no
`tc11x_*` module is imported (O-4). `lf` = `E.BK.frame_l(stem, "4h")` — the lens frame of `D.load_asof`, the same
tape L-V's door reads (`scripts/tierc10_brk.py:920-954`; its `atr` is `ind.atr(h, l, c, ATR_LEN)`).

**L-R.10 THE EVENT** — "a SWING FAILURE (V2) at VAH or VAL" (contract :70); "both directions; five home assets"
(:69-70)

READING: One event = one row of `T12/va/va_events.parquet` (L-V.14) with `lens == "4h"`, `kind == "swing_failure"`,
`asset` in the home panel (`E.CLASSIC5`) — V2's machine as L-V.9-L-V.13 fix it (the contract's K at :36, the frozen
edge, each close judged against `VA(t−1)`). Both sides trade: `side == "top"` (a failure at VAH) and `side ==
"bottom"` (at VAL). The event is known at `known_close_ms`, the close of its return bar `i`. Fields read: `side`,
`t0`, `i`, `bars_out`, `E`, `extreme`, `sgn`, `val_f`, `poc_f`, `vah_f`, `close_i`, `atr_i`, `known_close_ms`, `era`,
`in_strip`, `ret_inside_frozen`, `ret_inside_rolling`, `from_state`. No further filter: neither return flag is
required and no `from_state` is excluded — an event whose close lies outside the frozen value area fails the
geometry law of L-R.14 by itself (a target is then behind the entry), and adding a flag test would be a second,
unwritten condition. Counts by flag and by `from_state` are printed. A LAPSE (`bars_out > K`) and an acceptance
feed no trade. The builder asserts, per event, `lf.open_ms[i] + lf.step_ms == known_close_ms`, `Round6(lf.c[i]) ==
close_i` and `Round6(lf.atr[i]) == atr_i`, else HALT `SFP-FRAME`.

SOURCE: contract :36, :69-70; L-V.9, L-V.11, L-V.14, L-V.24; O-16.

RIVALS: X's record event (return within 7) — the contract's V2 replaces it. The wick-only swing failure (X's twin) —
not a V2 event. Require `ret_inside_frozen` — see above. A warm-up floor beyond the machine's own (`t0 − 1 ≥ L − 1`)
— no phrase behind it.

FAILS-IF: F-SFP (b) (every traded or refused row maps to exactly one V2 swing-failure row, and every such row inside
the window is accounted for: traded, one-position, geometry, rr-min); mutation: lapse rows admitted as events.

**L-R.11 ENTRY AND DIRECTION** — "enter at the close back inside, toward the POC" (contract :70)

READING: `entry_i = i`; `entry_px = e = lf.c[i]`, a taker market fill at the return bar's close; `entry_ms =
lf.open_ms[i]`, `entry_close_ms = known_close_ms` (the lineage's key convention); the path starts at bar `i + 1`.
Direction `d = sgn` of the event: a failure at VAH is SHORT (−1), at VAL LONG (+1) — the fade of the failed edge,
toward value. "Toward the POC" is a property the geometry must have, not a second way to set the sign: if the POC is
not beyond the entry in direction `d` the trade is REFUSED (L-R.14), never reversed.

SOURCE: contract :70; L-V.11 ("its sign points toward value (top → −1, bottom → +1)"); `XR/tierc11x/LEANS_X.md:1133-
1137` (LX-X2.2); `tc11x_sfp.py:490`.

RIVALS: `d = sign(POC − entry)` — turns a close that overshot the POC into a trade AWAY from the failed edge, a
different trade; X refuses those (LX-X2.6). Entry at the next bar's open — the contract says "at the close".

FAILS-IF: F-SFP (a), (b); mutation: the direction taken as `sign(poc_f − e)`.

**L-R.12 THE PROFILE OF THE TRADE; TARGET 1; TARGET 2** — "TARGET 1 = POC (half off); TARGET 2 = far edge − 0.25
ATR_4h (remainder)" (contract :71-72)

READING: The profile of the trade is the one whose edge was probed: `VA(t0−1)`, FROZEN — the event row's `val_f`,
`poc_f`, `vah_f` (L-V.14). All three levels are the filed values (L-V.24) and never move after entry.
- `T1 = poc_f`. Half the position rests there as a limit. "Half" is `Q` = the card's harvest fraction
  (`E.TP.CONTROL_CARD.harvest_frac`), the object `BK.account_l` books with; the contract's word "half" (:71) is
  asserted equal to it by the pin door (L-R.32).
- `far` = `val_f` for a short, `vah_f` for a long. `T2 = far − d·a·A`, with `a` = the contract's "0.25" (:72, pin
  `sfp.t2_offset_atr`) and `A = lf.atr[i]` — ATR_4h of the return bar, known at the entry close. The offset is toward
  the inside of value. The remainder (the other fraction, or the whole position if T1 has not filled) rests at T2.
- Printed per event: `t1_r = d·(T1 − e)/R`, `t2_r = d·(T2 − e)/R`, `r_atr = R/A`, with their distributions.

SOURCE: contract :71-72; L-V.14 (`*_f` = "the FROZEN profile VA(t0−1) — the profile whose edge was probed"); X's
precedent `LEANS_X.md:1158-1184` (LX-X2.4: T1 on the range "the deviation swept", frozen at entry) and :1186-1196
(LX-X2.5); `tc11x_sfp.py:122, :497-502`; scout U2 R20.

RIVALS: the profile in force at entry, `VA(i)` (`*_n`) — its window contains the probe's own bars, so the excursion
being faded has already moved its POC and edges; not taken. Disclosed as a COUNT: events whose disposition (admitted
/ geometry / rr-min) differs under `VA(i)`. The judging profile `VA(i−1)` — neither the probed profile nor the one
in force. Targets re-read each bar — a level set from a bar's own profile or ATR can know that bar's range
(`LEANS_X.md:1194-1196`).

FAILS-IF: F-SFP (a), (b) (`T1 == poc_f`; `T2 == far − d·a·A` on every row); F-SFP-ASOF; mutations: T1 from `poc_n`;
T2 with `ATR[i+1]`; the offset applied outward (`far + d·a·A`).

**L-R.13 THE STOP** — "stop beyond the deviation extreme, railed ≥ 1.0 ATR_4h" (contract :71)

READING: `st = E.BK.brk_stop(d, ext, t0, e, A, rail_atr=RAIL)` — the estate's function, which is
`tierc5_rules.spring_stop` unchanged:

    long :  stop = min(ext − B·A, e − RAIL·A)        short:  stop = max(ext + B·A, e + RAIL·A)
    R = |e − stop| = max(d·(e − ext) + B·A, RAIL·A)   rail_binding ⇔ RAIL·A > d·(e − ext) + B·A

- `ext` = the event's `extreme`: `max(h[t0..i])` for a failure at VAH, `min(l[t0..i])` at VAL — over the probe's
  bars INCLUDING the return bar's own wick (L-V.11).
- `B` = `STOP_BUF_ATR`, the card's one word for "beyond" (lineage object; on file 0.5). The contract states no
  number for "beyond"; none is typed.
- `RAIL` = the contract's "1.0" (:71, pin `sfp.rail_atr`), handed in explicitly and asserted equal to the lineage
  rail `MIN_STOP_ATR`.
- `A = lf.atr[i]`, the ATR of the return bar (X's `tp.atr[b]`).
- `st is None` (ATR not finite or not positive) → the event is refused (`stop_none`).
- The stop and `R` are fixed for the trade's life (L-R.18). `pivot_stop_px`, `rail_binding` are filed per row.

SOURCE: contract :71; `scripts/tierc10_brk.py:1366-1385` (`brk_stop`: "`STOP_BUF_ATR` is the card's one definition
of the word 'beyond'"), :510; `scripts/tierc5_rules.py:481-502` (`spring_stop`), :115-116; `scripts/tierc2_rules.py:
103-104, :127`; `scripts/tierc3_rules.py:148`; `LEANS_X.md:1140-1156` (LX-X2.3); `tc11x_sfp.py:491-496`.

RIVALS: the extreme without the return bar — L-V.11 and X include it. ATR of `t0` — the stop is set at the entry
close. A new stop function — the contract's own words are the card's ("beyond", "railed").

FAILS-IF: F-SFP (a), (b) (`ext ==` the raw extreme over `[t0, i]`; `R ≥ RAIL·A` on every row); F-TYPED-FLOW
(`sfp.rail_atr` bent at its door must move `r_dist` of a rail-bound row); mutations: the rail dropped; `ext` over
`[t0, i−1]`.

**L-R.14 DEGENERATE GEOMETRY** — "toward the POC" (contract :70); X2's refusal of record

READING: An event is REFUSED and counted, before the reward test, if any holds — X's law (`geometry`,
`tc11x_sfp.py:503-513`), in X's order of reasons:
1. `stop_none` (L-R.13);
2. `d·(T1 − e) ≤ thr` — the POC is at, behind, or within the fee band of the entry (`t1_within_10bps`);
3. `d·(T2 − e) ≤ thr` (`t2_within_10bps`);
4. `d·(T2 − T1) ≤ 0` — T2 is not beyond T1 (`targets_inverted`: the POC lies within `a·A` of the far edge).
`thr = (G / BPS_PER_UNIT)·e` with `G` = the lineage object `FEE_BPS_ROUND_TRIP` (the round-trip taker fee; on file
10.0), asserted equal to X's `REFUSAL_BPS` (`tc11x_sfp.py:123`, read as an AST literal). It is the SAME threshold on
every row and every twin, never the row's own toll, so every cost twin shares one admitted set. The row files the
first reason and `reasons_all`. The reason slugs are X's, kept for comparability with `XR/tierc11x/sfp/
X2_refusals.parquet`.

SOURCE: `LEANS_X.md:1198-1224` (LX-X2.6: "the FIXED literal 10 bps of entry on every row"); `tc11x_sfp.py:123,
:503-513`; `scripts/tierc2_rules.py:123`; `scripts/tierc11_ride.py:208` (the same quantity as `TP_GUARD_BPS`).

RIVALS: T1-collapse (the whole position rides to T2 when the POC is behind the entry; X's twin) — not carried as a
book; the count of refusals it would admit is printed. Only "rr-min" — lets a "half off at the entry" trade through.

FAILS-IF: F-SFP (b) (every refused row meets a clause; every admitted row meets none); mutations: a planted event
with the POC behind the entry admitted; the threshold taken from the row's toll.

**L-R.15 "rr-min" AND THE UNFILTERED TWIN** — "Minimum reward at T2 ≥ 1.5 × stop distance or the trade is skipped
["rr-min"]; the unfiltered twin printed" (contract :73-74)

READING: After the geometry law, with `R` the stop distance AFTER the rail (L-R.13) and everything measured from the
entry price: `rr = d·(T2 − e) / R`. The event is SKIPPED and counted (`rr_min`) iff `rr < RR`; it trades iff `rr ≥
RR`. `RR` = the contract's "1.5" (:73; second citation :135-136 `"rr-min" (1.5 at T2)`; pin `rr_min`, veto
"rr-min"). A skipped event does not occupy the asset's slot.
Order of tests per event, in bar order per asset: (1) one position (L-R.18) → (2) geometry (L-R.14) → (3) rr-min →
(4) the walk. The first test that fails names the row's disposition.
**The unfiltered twin** `tierE__unfiltered` is the same book without step (3), RE-WALKED with its own one-position
sequence (X's law for ridden twins, `tc11x_sfp.py:167-168`): a trade the record skipped can hold the slot and block
a trade the record took, so the twin is a different trade set, not a superset. Printed with it: rows in both books;
rows only in the twin (skipped by the record); record rows the twin displaced.

SOURCE: contract :73-74, :135-136; `tc11x_sfp.py:167-168, :892-945` (the order: one position, then geometry);
L-0.23 (the veto).

RIVALS: `R` before the rail (the pivot distance) — the contract says "stop distance", and the stop is the railed
one. The reward measured from T1, or as the fraction-weighted blend — the contract says "at T2". The twin as a
filter of the record's rows — it would hide the slot effect.

FAILS-IF: F-SFP (b) (`rr ≥ RR` on every record row; every `rr_min` row has `rr < RR`); F-TYPED-FLOW (`rr_min` bent
moves the disposition of the event nearest the cut); mutations: `R` taken as the pivot distance on a rail-bound
event; the test applied to T1.

**L-R.16 THE TIME STOP** — "TIME STOP = the 4h traverse (V4)" (contract :72)

READING: `T` = the fitted pin `traverse.4h` — `T12/va/TRAVERSE.json` `by_lens.4h.T_of_record` — read through the
fitted-pin door (L-V.18, O-18), an integer number of 4h bars fitted on the tuning era and frozen before any range
book exists. The position still open at the CLOSE of bar `tend = entry_i + T` exits there: `exit_px = lf.c[tend]`,
`exit_reason = "time_stop"`, a taker leg. Every trade row files `T` and `time_stop_i`; the book's manifest files
`time_stop_source = {path, key, sha256, value}`. The row carries the label "T tuning-fit (in-sample for tuning-era
trades)".

SOURCE: contract :42-43, :72; O-18; L-V.18; `LEANS_X.md:1238-1239` (LX-X2.7: "exits the position still open at the
CLOSE of bar `entry_i + T`"); `scripts/tierc7.py:209-211` (the lineage's shadow clock); `tc11x_sfp.py:657, :738-740`.

RIVALS: the clock started at `t0` — the trade starts at the entry. Exit at the open of `tend + 1` — X's and the
lineage's clock exits at the close. A typed integer — F-TRAV.

FAILS-IF: F-TRAV (a), (e) (L-V); F-SFP (a) T-TIME, (b) (`exit_i == entry_i + T` on every time-stop row);
F-TYPED-FLOW (`traverse.4h` bent by one bar moves the exit bar of a time-stop trade); mutation: the exit at the
close of `entry_i + T + 1`.

**L-R.17 INVALIDATION** — "INVALIDATION = acceptance beyond the faded edge" (contract :72-73)

READING: The faded edge is the side the swing failure failed at (VAH for a short, VAL for a long). The trade is
invalidated when the LENS becomes ACCEPTED beyond that side: the first `acceptance` row of `va_events` for the same
asset and lens with `side ==` the event's side and `entry_i < i_acc ≤ tend`. If the position is still open at the
close of bar `i_acc`, it exits there: `exit_px = lf.c[i_acc]`, `exit_reason = "invalidation"`, a taker leg. It exits
whatever is still open (the whole position, or the remainder after T1).
- It is a CLOSE event. Within bar `i_acc` the intrabar law of L-R.19 runs first: an open at or beyond the stop, the
  stop by range, T1, T2. Acceptance can print in a single bar (the one-close clause of contract :35, on the probe's
  first bar too), so on that bar the stop is tested BEFORE the invalidation: a bar whose range reaches the stop is a
  stop at the stop price, and the acceptance printed at its close does not act. Counted: `n_invalidation`;
  `n_acceptance_on_a_stop_bar`.
- On a close that is both the acceptance and the time stop the reason is `invalidation` (the price is the same).
- An acceptance on the OPPOSITE side (in the trade's favour) is not an exit.
- Decay, a lapse, a re-probe that fails and a re-roll of the value area are not exits.

SOURCE: contract :35, :72-73; L-V.10, L-V.14 (acceptance rows; `i`, `side`); `LEANS_X.md:1292-1305` (close events
after the intrabar order); TC11 L-S.2 (`MR/LEANS.md:458-460`: invalidation exits "at that 1h close … taker"; "STOP →
TARGET → invalidation at the close").

RIVALS: a trade-local acceptance — N closes beyond, or one close M·ATR beyond, the trade's own frozen `E`, counted
by the builder — not taken: it is a second state machine outside the module, on an edge the lens may have re-rolled;
the contract names the V2 state. Invalidation before the intrabar stop — a close event cannot precede the bar's
range. Exit at the next open — the acceptance is known at its close.

FAILS-IF: F-SFP (b) (every `invalidation` row has an acceptance row on the faded side at `exit_i`; no record row
holds an acceptance on the faded side at a bar `j` with `entry_i < j < exit_i`; and none at `j == exit_i` unless the
exit is `invalidation` or an intrabar exit of that bar) and (g) (a synthetic one-bar acceptance whose range touches
the stop must book a stop); mutations: the invalidation ignored; the invalidation taken before the stop on the
synthetic bar; the opposite side's acceptance treated as an exit.

**L-R.18 NO TRAIL, NO TIDE, ONE POSITION PER ASSET** — "NO trail; NO tide requirement" (contract :73)

READING: The stop is the entry stop from entry to exit: no trail, no move to breakeven after T1, no re-anchoring.
The builder reads no tide, ribbon or EMA array and applies no tide filter. One position per asset, in this book's
own sequence (independent of v6 and of every twin): a swing failure at bar `b` is SKIPPED and counted
(`one_position`) iff `entry_i < b ≤ exit_i` of the trade open on that asset — X's `blocks`, the lineage's `ti <=
open_until` — so an event on the exit bar's close is skipped, after an intrabar exit as after a close exit. The
skipped count is split by same or opposite side. Each row files `stop_px_at_exit` (asserted equal to `stop_px`) and
`n_entry_fills` (asserted 1): the two columns L-0.30's F-NOT reads.

SOURCE: contract :73; `tc11x_sfp.py:870-874` (`blocks`); `tierc9.py:391-393`; `LEANS_X.md:1262-1290` (LX-X2.8,
LX-X2.9); L-0.30 (TRAIL-OFFSET and ADDS).

RIVALS: re-entry at the close of an intrabar exit — X counts it as a rival; counted here too
(`rival_reentry_at_intrabar_exit_close`). An opposite-side event reverses the position — not in the text.

FAILS-IF: F-SFP (c): no two trades of an asset overlap under the law and the skipped count equals the events inside
open trades; mutations: an overlapping trade planted; an event planted on an exit bar admitted.

**L-R.19 THE BAR WALK — SAME-BAR ORDER AND FILLS** — "TARGET 1 … (half off); TARGET 2 … (remainder)" (contract
:71-72)

READING: X2's `bar_step`, record law (touch fills, no symmetric-gap twin), on the 4h bars `j = entry_i + 1 …
min(tend, hi)`, `hi` = the window's last bar (L-R.21). With `fav`, `adv` = the bar's favourable and adverse extreme:
0. **THE OPEN decides first.** `d·(o[j] − stop) ≤ 0` → the whole open position exits at the STOP price (the v6 law:
   a stop fills at the stop, through a gap too). Otherwise a resting T1 with `d·(o[j] − T1) ≥ 0` fills at `o[j]`,
   and a resting T2 with `d·(o[j] − T2) ≥ 0` exits the remainder at `o[j]`.
1. **STOP, adverse-first.** `d·(adv − stop) ≤ 0` → the whole open position exits at the stop. A bar that touches
   the stop and a target, neither decided at the open, is a stop (`both_touch`, counted).
2. **T1**, if still resting: `d·(fav − T1) ≥ 0` → the T1 fraction fills at `max(T1, o[j])` long / `min(T1, o[j])`
   short.
3. **T2**: `d·(fav − T2) ≥ 0` → the remainder exits at `max(T2, o[j])` / `min(T2, o[j])`, on the same bar if reached.
4. **Close events**, in this order: INVALIDATION (L-R.17), then the TIME STOP (L-R.16).
A trade with no exit by `hi` and `tend > hi` is marked at `lf.c[hi]`, `corridor_end`, listed OPEN (L-R.21). A
zero-volume lens bar fills no resting target (L-D.16's no-trade rule, adopted); stops and close events act on it as
on any bar; the count is printed (on file: none at 4h or 1d for the home assets). The record reads NO 5m bar: a 4h
bar's internal order is decided by the law above, and `both_touch_bars`, `gap_stop`, `gap_t1`, `gap_t2` are filed
per row so a reader sees how many trades rest on it.

SOURCE: `tc11x_sfp.py:558-601` (`_hit`, `_fill`, `bar_step`), :649-752 (`walk`); `LEANS_X.md:1292-1315` (LX-X2.10);
`scripts/tierc7.py:186-192`; TC11 L-H.1 (`MR/LEANS.md:505`: the limit fill law); L-D.16.

RIVALS: targets before the stop on an ambiguous bar — flatters. Fill at the level on a gap open (X's symmetric-gap
twin) — not carried; the gap counts are printed. 5m-child sequencing of ambiguous bars (X's twin) — not carried: it
would make the record's stage a 5m reader for a twin the contract does not name.

FAILS-IF: F-SFP (a), (g) (a synthetic bar set typed by the fixture: gap through the stop; gap through T1 and T2;
stop and target in one bar; T1 and T2 in one bar; acceptance and time stop on one close); F-SFP-MIRROR; mutations:
target-before-stop on a both-touch bar; a stop filled at the open on a gap; T1 credited on a stop bar.

**L-R.20 THE R-MULTIPLE WITH SPLIT TARGETS; FEES; FUNDING; THE COST TWINS** — "(half off) … (remainder)" (contract
:71-72); "taker and charter tiers unchanged" (:23)

READING: `acc = E.BK.account_l(lf, E.TP.CONTROL_CARD, d, R, leg)` with `leg = {entry_i, exit_i, exit_px, entry_px:
e, harvest}`; `harvest = None` if T1 never filled, else the 3-tuple `(t1_i, t1_px, d·(t1_px − e)/R)`. With `q =
card.harvest_frac`, `b = FEE_BPS_SIDE / 10 000` (the function's own lines, `tierc10_brk.py:1270-1326`):
- T1 filled: `g = q·d·(t1_px − e) + (1 − q)·d·(exit_px − e)`; `fee = b·q·(e + t1_px) + b·(1 − q)·(e + exit_px)`;
  funding of the T1 fraction to the T1 bar and of the remainder to the exit bar; the fractions book the leg (`n1 +
  n2 == net`, asserted inside the function).
- T1 not filled: `g = d·(exit_px − e)`; `fee = b·(e + exit_px)`.
- `gross_r = g/R`, `fee_r = fee/R`, `net_r = gross_r − fee_r − funding_r`.
- **Funding** is the interval sum on the 4h frame: every stamp with `open_ms[entry_i] < stamp ≤ open_ms[bar]`,
  priced at the close of the last 4h bar closed at or before it, accumulated in ascending order (`funding_interval`,
  :1223-1267). A settlement at the entry-close instant is paid; one at a close-exit instant is not. The D12 ceiling
  (`card.funding_ceiling_r`) is taken once, on a cost only. Stamps strictly inside the entry bar are counted
  (`n_stamps_inside_entry_bar`; expected zero on 4h).
- **Toll of record: taker on every leg** — entry, T1, T2, stop, time stop, invalidation, the mark — the TC-series
  toll. Sidecar `toll = "taker"`; `fee_taker_r = fee_all_taker_r = fee_r`, `fee_maker_r = 0`, `taker_twin_net_r =
  net_r` (L-X.24).
- **Charter twin (TC11 AM-7)**: `haircut_net_r = net_r − fee_r × (slip_bps_side / taker_bps_side)`, the two rates
  per stem from `E.fees()`; funding stays in.
- The lens frame, the card and `account_l` are called, never copied; production code holds no tolerance literal
  (the equality of the per-fraction booking with `account_l` is a fixture leg).

SOURCE: `tierc10_brk.py:1223-1326`; `LEANS_X.md:1317-1353` (LX-X2.11); `MR/LEANS_AMENDMENTS.md:86-96` (AM-7);
`tc11x_sfp.py:766-803`; L-X.24.

RIVALS: `T7._account_chain` — 4h-only by construction but bound to the v6 frame memo; `account_l` is the lens
function X rode. Slippage in the toll of record — Q3 stays open (L-0.29); the twin is printed beside.

FAILS-IF: F-SFP (f): `net_r == gross_r − fee_r − funding_r`; the fixture's own per-fraction booking at all-taker
bps equals `account_l` within X's filed tolerance (`LEANS_X.md:1340`); the haircut law; the four fee columns'
identities; mutations: maker bps left on one leg of the taker book; the T1 fraction funded to the exit bar.

**L-R.21 THE SCORED WINDOW, THE STRIP, ERA** — "(vs zero; full corridor; …)" (contract :69); O-9

READING:
- **Scored window.** The book of record holds the trades whose entry bar closes at or before W. It is ridden with
  `hi = hi_W`, the 4h bar closing at W: the walk, the one-position sequence and the marks are those of the tape cut
  at W. A trade not exited by `hi_W` (`tend > hi_W`) is marked at `lf.c[hi_W]` with `exit_reason = "corridor_end"`,
  stays in the scored book and is listed OPEN (`n_open_at_w` per asset) — X's LX-X2.17, the lineage mark. An
  unfilled T1 stays unfilled; a filled T1 keeps its fill.
- **Era.** "Full corridor" = every era inside the scored window (sidecar `era_scope = "full"`). Era of a trade =
  `E.era_of(entry_close_ms)`. The tuning and holdout slices are the scorer's Tier-E leaves (L-X.14).
- **Strip.** A second ride with `hi = hi_PIN` over every event to PIN. Its rows with `W < entry_close_ms ≤ PIN` are
  the `strip` arm (n and a pointer; no statistic). Its rows with `entry_close_ms ≤ W` must equal the scored book
  row for row, except the OPEN-at-W trades, whose true continuation is listed (`continued_past_w`).
- Stamped: the scored arm with the score edge, the strip with the pin (L-0.13).

SOURCE: contract :69; O-9; L-X.24 (the scored-window laws on `scored` and `strip`); `LEANS_X.md:1550-1577`
(LX-X2.17); `tc11x_sfp.py:743-747`.

RIVALS: refuse an event whose `tend` passes W — selects on the corridor's end, which no trader has at the entry
(X's rejected rival). Score the strip — O-9. Holdout of record — the contract says "full corridor".

FAILS-IF: F-SFP (d): the scored arm equals the full ride's rows with `entry_close_ms ≤ W` (OPEN-at-W rows compared
on entry, stop, R, targets and T1 fill); (b) OPEN leg: every OPEN row has `exit_i == hi_W` and `entry_i + T >
hi_W`; mutations: a trade with `entry_i + T ≤ hi_W` marked OPEN; a strip row placed in `scored`.

**L-R.22 THE PRECONDITION — THE LICENCE** — "the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h
maker}; nothing else may trade a range" (contract :40-41); O-17

READING: Evaluated BEFORE any arm is built, from `T12/va/VA_MIRROR.json` (L-V.17; sha certified by
`T12/progress/TC12-V.json`), which quotes X's `XR/tierc11x/va/feasibility.parquet` (sha256
`ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`). Two items, both required:
1. the licence row of the row's OWN scoring era (O-17): P-SFP-VA-1 is scored on the full corridor, so the era row
   is `ALL` — selector `licence["4h|taker"].by_era["ALL"].would_read`, required `"PASS"`;
2. the pair is in the licence set: selector `licence_set` contains `"4h|taker"` — the contract's word of record
   (:39, the holdout row). Stage V HALTs on a mirror disagreement, so this item cannot fail on a tier that reached
   Stage R; it is listed so the scorer re-evaluates it from the record.
If either is not met the stage writes `regbooks/P-SFP-VA-1/STATUS.json` with `status = "CLOSED_BY_PRECONDITION"`,
the item, the value found and `arms = []`, builds nothing, and the row reads `CLOSED BY PRECONDITION
(research_outputs/tierc12/va/VA_MIRROR.json#<selector> reads <found>; required <required>) — no number · no test
spent` (L-X.10), `<required>` being `PASS` for item 1 and `contains 4h|taker` for item 2. The row prints beside its cell, from the same record, the three era words of the pair (`ALL`, `tuning`,
`holdout`; on file all three read PASS for 4h taker) and the sentence of O-16 (d): the licence was earned on X's
record machine, the outer fifth of value and an H20 exit, not on V2 or on this trade (DISCLOSURES D-2).

SOURCE: contract :39-41; O-17, O-16 (d); L-V.17 items 7-9; L-X.10; `MR/regbooks/P-SCALP-2/STATUS.json` (the filed
form); scout U2 §1.8 (the pooled grid).

RIVALS: the holdout row alone — O-17 rules the row of the scoring era. Recompute the licence under V2 — a different
object (L-V.17). Build the book of a closed row and print it collared (X's departure) — O-22 rules STATUS only.

FAILS-IF: F-FAM (PLANTED leg, L-X); F-SFP (h): on a COPY of `VA_MIRROR.json` whose `ALL` word is flipped, the
builder must write STATUS only and no arm; mutation: a builder that reads the `holdout` word for item 1.

**L-R.23 LABELS AND DISCLOSURES** — O-23; "§0 VERDICTS FIRST: the five rows with their labels" (contract :126-127)

READING: P-SFP-VA-1 carries `pre_seen` (O-23) and L-X.13's RE-SCORE template. `pre_seen.text`, whose part before
its first `;` is the cell's clause: "TC11-X's X3 printed value-area swing-failure outcomes at 4h on these five assets
for every bar at or before 2026-09-25T00:00Z before this row was drafted, and this trade form (stop, split targets,
time stop, invalidation, minimum reward) was never scored; X's standing ledger line marks any later value-area
registration pre_seen on those bars; the K = 3 and one-close-acceptance variants are among the printed tables".
`items`: `XR/tierc11x/va/two_trades.parquet` (sha256
`a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0`), detector `va`, trade `swing_failure`, variants
`k3` and `die_parity`, lens `4h`; `XR/tierc11x/va/X3.md`;
`XR/tierc11x/LEANS_X.md:1816-1818, :2468-2470`. Disclosures carried in the row's `disclosures[]`, printed under the
cell: D-2 (what the licence was earned on) and D-3; "T tuning-fit (in-sample for tuning-era trades)"; the lookback's
`l_label`; the count of trades OPEN at W.

SOURCE: O-23; DISCLOSURES D-2, D-3; L-X.13; the files as cited [schemas and variant sets read here].

RIVALS: `selection_hazard` only — X's standing line, which O-23 enacts, names `pre_seen`.

FAILS-IF: F-REG (TEMPLATE leg, L-X); mutation: the template rewritten to the `selection_hazard` form.

**L-R.24 TIER-E BESIDE THE ROW** — "Tier-E beside: the holdout slice · the 1d cell · the 1d-direction-guarded twin
(refuse when 1d is accepted against) · the maker twin" (contract :74-75)

READING: Each is a collared arm under `regbooks/P-SFP-VA-1/` (or a scorer-derived leaf); none carries a verdict
word; each ridden book has its own one-position sequence and its own OPEN list.
- **The holdout slice** — the scorer's `holdout_slice` leaf on `scored` (era by the entry close), printed beside
  the verdict with the fixed sentence "causal for the tuning-fit T and lookback only; the class was pre_seen; the
  era of record is the full corridor".
- **The 1d cell** `tierE__cell_1d` — the whole law of L-R.10-L-R.21 with the lens swapped: events = V2 swing
  failures of lens `1d`; `lf = E.BK.frame_l(stem, "1d")` (the Stage D derived tape, asserted row-identical to
  `va_bars_1d`); ATR_1d; `T` = `traverse.1d` (its `provisional` flag carried, L-V.18); the same `a`, `RAIL`, `RR`,
  `G`; funding by the interval sum on 1d. Its licence pair is `1d|taker`; the cell is built on the full corridor
  like its parent and its sidecar carries the pair's three era words from `VA_MIRROR.json` as
  `licence_would_read_by_era` (on file: holdout PASS; ALL and tuning FAIL). Where the `ALL` word is not PASS the
  cell's description reads "ERA NOT LICENSED on the full corridor — printed as a disclosure; the licensed era is
  the holdout", and its holdout slice is printed first.
- **The 1d-direction-guarded twin** `tierE__guard_1d` — the 4h book with one added refusal, placed after the
  one-position test and before geometry: refuse the event when the 1d state at τ = the entry close (the last 1d bar
  closed ≤ τ, O-14) is ACCEPTED against the trade (`ACCEPTED_BELOW` for a long, `ACCEPTED_ABOVE` for a short). A
  refused event does not hold the slot; the book is re-walked.
- **The maker twin**, two arms, sidecar `toll = "maker_entry_targets__taker_stop"`. MAKER legs = entry, T1, T2 at
  `E.fees()[stem]["maker_bps_side"]`; TAKER legs = stop, time stop, invalidation, the mark at `taker_bps_side`; no
  slippage on a maker leg. Fees are booked per fraction (X's `fee_per_fraction`): T1 filled → `[q·(m·e + m·t1_px) +
  (1 − q)·(m·e + x·exit_px)]/R`, else `(m·e + x·exit_px)/R`, `m` the maker rate, `x` the maker rate iff the exit is
  T2 else the taker rate; gross and funding are `account_l`'s. The four fee columns follow L-X.24; `haircut_net_r =
  net_r − fee_taker_r × (slip / taker)` (AM-7's maker clause); `taker_twin_net_r` = the same path at all-taker.
  - `tierE__maker_conditioned` (named first): the limit rests at `P = e` from the entry close and books only if
    the FIRST 5m child of bar `entry_i + 1` (the 5m bar whose open equals that bar's open) trades strictly through
    it — `low < P` for a long, `high > P` for a short — and is not a zero-volume bar; otherwise a MISS (`miss`,
    `miss_nochild`, or `fill_unresolved` when the bar lies past `hi`), counted, never a trade. On the fill child
    the stop is tested adverse-first and no target is credited (`fillchild_target_withheld`, counted); the rest of
    that 4h bar is walked child by child (STOP → T1 → T2) if its 5m children reproduce its high, low and close
    within `E.LN.REPR_TOL`, else targets rest from the next bar and the stop is judged on the parent; maker targets
    fill only on trade-through (strict); the time-stop clock stays at `entry_i`; funding runs from `entry_i + 1`.
    X's LX-1.1 (ii) law, unchanged.
  - `tierE__maker_assumed`: the record's own path, re-booked at maker fees.
- **The unfiltered twin** `tierE__unfiltered` (L-R.15).
- The scorer's common leaves (L-X.14): `haircut` (the charter twin), `taker_twin` (IDENTICAL on the record),
  tuning slice, LOAO, both single-trade shares, the month-block and drop-OPEN twins, the strip.
TC12-R is a 5m reader for ONE purpose, declared here for `FIVE_MIN_READERS_T` (L-0.30): the fill child and
fill-bar walk of `tierE__maker_conditioned` (the 5m children of 4h bars, home assets). No 5m bar originates a signal
and the record reads none.

SOURCE: contract :74-75; `LEANS_X.md:565-612` (LX-1.1 (i)-(iii)), :1386-1396 (LX-X2.13, a collared cell on a lens
with a failing word); `tc11x_sfp.py:148, :664-712, :756-803`; `MR/LEANS.md:85-93` (L-1.2); AM-7; L-D.16; O-17, O-19.

RIVALS: one maker row — the contract's "maker twin" has two filed readings in X; both are printed, the conditioned
one first. The scalper's through-by-one-tick rule for this twin — that pin (contract :93-94, "fill") is written
for a limit AT an edge on the 5m clock; this twin keeps the law its filed precedent used, and the difference is
listed for the reviser (INTERFACE). The 1d cell on the holdout only — its parent names the full corridor; the era
words are printed beside instead.

FAILS-IF: F-SFP-MIRROR (the maker booking and the conditioned walk against X's filed twins); F-SFP (i): the
guarded twin's refused events all carry a 1d state accepted against, read at their entry close; mutations: maker
bps on the stop leg; a target credited on the fill child; the guard read at the 1d bar still forming.

**L-R.25 F-SFP AND THE MIRROR FIXTURES** — "F-SFP (3 trades hand-walked incl. a POC fill and a time-stop exit)"
(contract :119)

READING:
- **F-SFP (a) HAND-WALK.** Three trades of the book of record chosen by a rule frozen HERE, in ascending `(symbol,
  entry_ms)` order: **T-POC** the first trade with a T1 fill (the POC fill); **T-TIME** the first OTHER trade whose
  exit is the time stop; **T-STOP** the first other trade whose exit is the stop. An empty category prints
  NONE-EXISTS and asserts the book's count of it is zero (and is carried to the report as a finding, since the
  contract names the POC fill and the time-stop exit). Walked beside, by the same rule, as extra witnesses: the
  first invalidation exit; the first T2 exit; the first geometry refusal; the first rr-min skip; the first
  one-position skip. Each walk is the fixture's own, from the raw 4h tape by explicit path, sharing no code with
  the builder, the reader, the door or the module: `VA(t0−1)` by `analytics.profile.volume_profile` on the raw
  slice (its POC, VAL, VAH passed through Round6 must equal the filed `*_f`); the probe's closes against the edge;
  the return within K; the extreme; ATR by its own Wilder loop; stop, R, T1, T2, the refusal clauses, `rr`; the bar
  walk OPEN → STOP → T1 → T2 → INVALIDATION → TIME STOP; fees and funding re-booked by its own arithmetic.
  FAILS IF any price, bar, fill, reason or `net_r` differs beyond the fixture-typed tolerance X's F-SFP used.
- **(b) IDENTITIES** on every row (L-R.10-L-R.21, as each reading's FAILS-IF states). **(c)** one position
  (L-R.18). **(d)** the W identity (L-R.21). **(f)** fees and net (L-R.20). **(g)** the synthetic bar set
  (L-R.17, L-R.19). **(h)** the closed row (L-R.22). **(i)** the guarded twin (L-R.24).
- **F-SFP-ASOF** — for a seeded sample of events per asset (both eras, both sides): the DOOR re-run on the 4h tape
  cut at the event's `known_close_ms` reproduces the event row, and the builder on that cut reproduces `(e, stop,
  R, T1, T2, disposition, rr)` exactly; `T` is held at its filed value and the leg says it does not test the fit.
- **F-SFP-MIRROR** — the mirrored walk and booking against X's FILED trades, before either is pointed at a V2
  event: for every row of `XR/tierc11x/sfp/X2_trades_4h.parquet` (sha256
  `552e7582d7559c032438f89c402e3070a3011559c1b334babd4c942f23b1bbef`) and `X2_trades_1h.parquet`
  (`4e3b5f4f7eb01db468b4203c4b64362f54fe388419290b5c58a68d9a54427eac`), on the tape cut at X's pin: geometry
  re-derived at full float from the filed integers (`breach_i`, `entry_i`, `d`) and the filed box (`top_pre`,
  `bot_pre`) under X's own T1 (the box mid) → `stop_px`, `r_dist`, `T1`, `T2` equal at the 6-dp write law; the
  mirrored walk with the row's `T` → `harvest_i`, `harvest_px`, `exit_i`, `exit_px`, `exit_reason`, `bars_held`,
  the gap flags and `both_touch_bars` equal; the mirrored booking at X's rates (taker from `E.fees()`; maker =
  `maker_pin.x_assumed_bps_side` of TC12's fee file) → `gross_r`, `taker_fee_r`, `funding_r`, `taker_net_r`,
  `maker_fee_r`, `maker_net_r`, `haircut_net_r` equal at the write law; and the `maker_conditioned` rows of
  `X2_twins.parquet` (`f2abf81de9202eef907857355799536012992d114b87a3fbd00a44ac4ae28c25`) reproduced from the 5m
  children (key set, misses, fills). The mirror adds nothing X's walk lacks except the invalidation close event,
  which is switched off in this leg.
- PLANTS: T1 from `poc_n` → (a), (b); the rail dropped → (a) on a rail-bound witness, (b); `ext` without the
  return bar → (b); target-before-stop → (g), F-SFP-MIRROR; the time stop one bar late → (a) T-TIME, (b),
  F-SFP-MIRROR; the invalidation ignored → (b); `R` before the rail in `rr` → (b); an overlapping trade → (c); a
  trade wrongly marked OPEN → (b); maker bps on a taker leg → (f), F-SFP-MIRROR; `T2` from `ATR[i+1]` →
  F-SFP-ASOF; a typed time stop → F-TRAV (a).

SOURCE: contract :119; `LEANS_X.md:2309` (X's F-SFP and its frozen selection rule), :2319 (F-SFP-ASOF), :2337
(F-FEE-EQ); L-0.14; the X files as cited [schemas read here; row counts on file 588 and 2,408].

RIVALS: hand-walk trades picked after the book is seen — the rule is frozen first. Trust the mirror without X's
filed rows — O-4 orders mirror AND equality.

FAILS-IF: as stated in the reading.

---------------------------------------------------------------------------------------------------------------
#### C · The Tier-E tables of Stage R

Every table of this part is collared (L-0.16), descriptive (`would_read_ci_only = "no interval"`), carries no
verdict word, registers nothing and promotes nothing (O-13). Population: the five home assets; events known at or
before W; the strip is a count beside.

**L-R.26 THE TWO TRADES ON THE VALUE AREA — THE EVENTS** — "the two trades per lens on the VA at 4h and 1d — the
breakout-retest (ACCEPTED → first retest of the accepted edge that holds, FLIP_HOLD pins reused) and the swing
failure" (contract :76-78)

READING: Lenses L ∈ (`4h`, `1d`).
- **The swing failure**: V2's `swing_failure` rows of lens L (L-R.10's event, here as an outcome anchor, not a
  ride). Anchor bar = the return bar `i`; sign toward value; edge = the frozen `E`.
- **The breakout-retest**: X's first-HOLD scan (`scan_retests`, `retest_verdict`, `touch_mask`; `tc11x_va.py:
  674-728`), mirrored into `scripts/tierc12_stage_r_tables.py` and run OUTSIDE the door on the filed `acceptance`
  rows and the tape. Anchors = the V2 acceptances of lens L in bar order, each with its level `E` (the frozen
  accepted edge). For an acceptance at bar `a` on side `top` (accepted above VAH): a qualifying touch at `j` is
  `l[j] ≤ E` with `c[j−1] > E` (mirrored for `bottom`: `h[j] ≥ E` with `c[j−1] < E`), taken in bar order over `(a,
  min(a + TTL, next acceptance of EITHER side − 1, n − 1)]`. Verdict at a touch: `truncated` if `j + HOLD ≥ n`;
  `failed` iff some close in `j … j + HOLD` is through the level by MORE than `MARGIN·ATR_L[k]` (`c[k] < E −
  MARGIN·ATR_L[k]` for `top`); else `hold`. The first `hold` is the event, known at bar `j + HOLD`; a `truncated`
  verdict ends the scan; every evaluated touch is a row. Sign: with the acceptance (`top` → long).
  `MARGIN`, `HOLD`, `TTL` are the FLIP_HOLD pins read BY OBJECT: `E.BK.FLIP_HOLD_MARGIN`, `E.BK.FLIP_HOLD_BARS`,
  `E.BK.MEM_TTL_BARS` (`tierc10_brk.py:145-149`, themselves read out of the AST of `engine/rangefinder.py`
  `PINS_V2`, never by importing the range machine), asserted equal to `XR/tierc11x/va/build_manifest.json` →
  `pins.laws.flip_hold_margin`, `.flip_hold_bars`, `.mem_ttl_bars`. `n` = the bars closing at or before W.
- Files: `stage_r/TWO_TRADES_EVENTS.parquet` (key `[lens, asset, trade, side, anchor_i, i]`).

SOURCE: contract :76-78; `tc11x_va.py:174-176, :674-728, :756-764`; `LEANS_X.md:1693-1706` (LX-X3.9);
`tierc10_brk.py:139-149`; L-V interface item (iv); the manifest keys [read here].

RIVALS: the band retest pins (hold 3, `C.RETEST_PINS`) — the contract says FLIP_HOLD. The retest of the LIVE edge
(X's twin) — the contract says "the accepted edge". One-shot first touch — TC10's rule, X's twin.

FAILS-IF: F-RETEST-MIRROR: (r1) fed X's filed RECORD acceptances (`events_va.parquet`, `variant == "record"`,
`cls == "accept"`) on the tape cut at X's pin, the mirrored scan reproduces X's filed `retest-touch` and
`retest-hold` rows of that variant (anchor, touch bar, verdict, `known_at`, level at the write law) at 4h and 1d;
(r2) fed V2's acceptances it reproduces X's filed `die_parity` `retest-hold` rows; every HOLD has `known_at ==
touch + HOLD`; mutations: an off-by-one window start; the hold window read as `touch … touch + HOLD − 1`; the band
pins substituted.

**L-R.27 THE LENS ABOVE AND THE PARTITION** — "conditioned on the lens above {accepted aligned · inside mid ·
inside at its own edge (coincidence)}" (contract :78-79)

READING: The lens above is TC11's ladder (`scripts/tierc11_nest.py:101`): above `4h` is `12h`; above `1d` is `1w`.
The state of the lens above U is read at the event's known-at close τ as U's block of the reader's stamp (the last
U bar closed ≤ τ, O-14). Every event falls in exactly one cell of a WHOLE partition; the contract's three cells are
starred, the rest are printed too (TC11's L-R.6 form):

| cell | condition (d = the trade's sign; first match in this order) |
|---|---|
| `NA` | no conditioning lens (see below) |
| `UNDEFINED` | U's state is UNDEFINED, or no U bar has closed |
| ★ `ACCEPTED_ALIGNED` | U ACCEPTED_ABOVE and d = +1, or U ACCEPTED_BELOW and d = −1 |
| `ACCEPTED_COUNTER` | U ACCEPTED on the other side |
| `PROBING` | U PROBING_ABOVE or PROBING_BELOW |
| ★ `INSIDE_COINCIDENT` | U INSIDE and the event's edge of L within `F·ATR_L` of either in-force edge of U: `abs(E − U_vah) ≤ F·ATR_L[k]` or `abs(E − U_val) ≤ F·ATR_L[k]` (inclusive) |
| ★ `INSIDE_MID` | U INSIDE, not coincident, and U's filed `pct` within `MID_BAND` (inclusive) |
| `INSIDE_OTHER` | U INSIDE, neither |

- `E` = the event's frozen edge of L (the probed edge of a swing failure; the accepted edge of a retest); `k` =
  the event's known-at bar of L; `U_vah`, `U_val` = U's profile IN FORCE at τ (the block's `vah`, `val`).
  `F` = the contract's coincidence fraction (:45, L-V.4's pin). `MID_BAND` = TC11's "in-range mid" band, read as an
  AST literal from the text of `scripts/tierc11_nest.py:109` (on file `(25.0, 75.0)`); the contract states no
  number for "mid" and none is typed. The comparison is arithmetic on filed columns in the table's builder; no
  module call.
- **L = 1d.** Its lens above is 1w, which O-11 makes "a captured-only stamp column" and which L-0.25 reads as "no
  conditioning axis". Drafted under the ruling as written: every 1d event is in cell `NA` ("no conditioning lens:
  1w is captured-only [O-11]") and the other seven 1d cells are rows with `n = 0`, `nan_reason = "absent by
  construction: O-11"`. The 1d two-trades are thereby printed unconditioned. The objection and the alternative are
  at the end of this section.
- **L = 4h.** U = 12h. The 12h lens is closed for range TRADING (contract :40) and is read here only as a state.

SOURCE: contract :45, :78-79; `tierc11_nest.py:101, :108-109, :1466-1483` (`CELLS`, `STARRED`, `_cells`), :1487-1535
(`l1_cell`: the event's boundary of L against either live boundary of L+1, ATR of L); `MR/LEANS.md:260-270`; L-V.20,
L-V.21; O-11, O-14; L-0.25.

RIVALS: only the three named cells — a reader could not see what share of events they hold. Coincidence by L's
per-bar nest flag — that flag tests L's LIVE edges; the event's edge is the frozen `E` (TC11's "event's boundary"
law). Mid by a typed band — no file would supply it.

FAILS-IF: F-GRID (the partition: Σ n over the cells == the events); F-TWO (a): every event's cell recomputed by the
fixture from the filed U block read by its own as-of; mutations: U read at the bar still forming; the coincidence
threshold in `ATR_U`; a 1w column read by a copy of the builder (must also turn L-0's F-NOT leg 1W RED).

**L-R.28 OUTCOMES, THE TOLL, THE BASE RATE** — "H20/H100 net of the lens's toll; base rate" (contract :79)

READING: X's outcome road and statistics (`C.outcome_ledger`, `tc11x_va.stats_rows`), mirrored and held equal to
X's filed tables.
- **Term**: from the CLOSE of the known-at bar `k`: `term_H = sgn·(c[k+H] − c[k]) / ATR_L[k]`, H in bars of L;
  CENSORED, never shortened, when `k + H` passes the last bar closing at or before W; MFE and MAE beside. The
  horizons are read from `XR/tierc11x/va/build_manifest.json` → `pins.laws.horizons` (on file H20 = 20, H100 =
  100), asserted equal to the AST literal `HORIZONS` of `scripts/tierc10_census.py:123`.
- **The lens's toll** = the toll of the lens's licence: taker at 4h and at 1d (contract :41) — the round-trip
  taker rate `E.fees()[stem]["taker_round_trip_bps"]`, in the anchor's own ATR: `toll_atr_evt = (bps /
  BPS_PER_UNIT)·c[k] / ATR_L[k]`. A pooled row's toll is the BINDING maximum of its members' tolls (the census
  law X kept).
- **Statistics per cell**: `n_events`, `n` (uncensored, good ATR), `n_censored`, `median_term`, `mean_term`, the
  quartiles, `hit_rate`, `hit_rate_net`, `median_mfe`, `median_mae`, `toll_atr`, and `net = round(median_term, ND)
  − round(toll_atr, ND)` with `ND` = `pins.laws.round_nd`; `provisional` when `n` is under the floor (L-V.4).
- **Grid** `stage_r/TWO_TRADES_VA.parquet`: `lens` × `trade` (`swing_failure`, `breakout_retest`) × `direction`
  (`long`, `short`) × `era` (`ALL`, `tuning`, `holdout`; by the anchor's close) × `panel` (the five home assets and
  `POOLED:CLASSIC5`) × `cell` (L-R.27's eight) × `horizon`; the unconditioned table
  `TWO_TRADES_VA_UNCOND.parquet` drops the `cell` axis.
- **Base rate** `stage_r/TWO_TRADES_BASE.parquet`: the same statistics anchored at EVERY closed bar `k` of L, for
  each direction, censored the same way, net of the same toll — (i) unconditional and (ii) within each cell of the
  same partition read at `close_k`, coincidence there = L's own nest flag at `k` (`coin_vah OR coin_val`, L-V.21).
  Each event row prints the base row of its own cell and `net − base_net`.
- X's filed rows of the nearest laws (`va|swing_failure|k3`, `|die_parity`, `va|breakout_retest|die_parity` of
  `two_trades.parquet`) are printed beside as the continuity columns, quoted by key.

SOURCE: contract :41, :79; `scripts/tierc10_census.py:123, :136, :1352-1394`; `tc11x_va.py:842-924`; `LEANS_X.md:
1756-1777` (LX-X3.11); `MR/LEANS.md:271-278` (the base rate within each L+1 cell); the manifest keys [read here].

RIVALS: the row's own trade toll (maker) — the licence at 4h and 1d is taker. A pooled median toll — re-derives
different nets from X's (scout U2 H17). Terms that read strip bars — O-9: the window ends at W.

FAILS-IF: F-TWO-MIRROR: on X's filed `events_va.parquet` rows of variants `die_parity` (`sfp`, `retest-hold`) at
4h and 1d, the mirrored ledger reproduces the filed `term_H20`, `term_H100`, `cens_*`, `toll_atr_evt`; and the
mirrored statistics on those rows reproduce X's filed `two_trades.parquet` rows for `va|swing_failure|die_parity`,
`va|breakout_retest|die_parity` and `base|every_bar|record` (every statistic at the write law); F-GRID; mutations:
a one-row drop; the horizon shortened at the tape's end instead of censored; the pooled toll taken as a median.

**L-R.29 THE NULL** — "null gaps+order (R10)" (contract :79)

READING: R10's null is defined on boxes — it permutes the GAPS and the ORDER of the (life, height) pairs of the
real confirmed ranges and replays the trades on static boxes (`scripts/tierc10_null.py:239-340, :356`). X's null of
record for the value area is another object, `tr_tercile_lblock` (`tc11x_va.py:236`). The reading: **build
gaps+order on VALUE REGIMES, because the schedule law transfers; print X's VA null beside, each named; HALT rather
than relabel.**
- **Why it transfers.** A V2 value regime has what the schedule permutes: a start, a life, a height and gaps —
  and X's own feasibility adapter is the filed precedent for treating it as a range (`confirm = r0`, `die` = the
  acceptance bar, height = `VAH(r0−1) − VAL(r0−1)`, `atr[r0]`; `LEANS_X.md:1720-1740`).
- **The real box set**, per (asset, L), from `va/va_regimes.parquet` and `va_bars_<L>` on the bars closing ≤ W
  (`n` of them): one box per regime, in bar order — `real_confirm_i = r0`; `life = die_i − r0`, or `n − r0` for
  the regime alive at the end (censored); `height_atr = (vah_j[r0] − val_j[r0]) / atr[r0]` (the judging profile of
  bar `r0`); the `m + 1` gaps around them. Preconditions, each a HALT `NULL-GAPS-ORDER-UNBUILDABLE` (the three of
  `real_box_set`): lives overlap; a regime other than the last is alive; `atr[r0]` not positive; and lives + gaps
  must tile `n`.
- **The schedule** — a mirror of `schedule(real, rng, keep_order=False)`: `perm = rng.permutation(m + 1)` of the
  gaps, `u = rng.random(m)`, `order = rng.permutation(m)` of the pairs, in that draw order; the lead-gap law with
  the value area's own warm floor: if the first gap is shorter than `L_bars` (the lens's lookback, `VA_PINS.json`)
  it is swapped with the first later gap that is not — "no real range confirms inside it, so no null box is born
  inside it either" (the source's reason, its floor being the pivot detector's). RNG = a mirror of `draw_rng`:
  `default_rng([SEED + draw, crc32("<asset>|<lens>|va_regime")])`, SEED the contract's (:4). K = L-V.4's null draw
  count.
- **The box**: `(bot, top) = box_bounds`: `height = height_atr·atr[a]`, `bot = c[a] − u·height`, `top = bot +
  height`, `a` the box's new first bar — static for its life.
- **The machine on a box** — a mirror of `static_box_machine` with V2's three constants in place of the pivot's
  (`DEV_RETURN_BARS` → K, `BREAK_CONFIRM_N` → N, `BREAK_MARGIN` → M): a close beyond an edge opens a breach; back
  at or inside within K is a swing failure, later a lapse; N closes beyond or one close `M·ATR` beyond (the open
  bar included) is the acceptance, which ends the box. The null's swing failures are those events; its
  breakout-retests are L-R.26's scan on the box's dead edge.
- **Conditioning**: each null event is placed in L-R.27's cell by the REAL state of the lens above at its known-at
  close (TC11's law: "events conditioned on the REAL L+1 state").
- **Statistics per draw and cell**: `n`, `median_term`, `net`, `hit_rate_net` (X's `NULL_STATS`); the real value's
  percentile by the filed mid-rank law (`100 × (#null < real + 0.5 × #null == real) / valid draws`, values at `ND`
  decimals) — "a DESCRIPTION of where the real value sits among the draws, never a p-value". Per draw: event
  counts and the share of bars inside a box.
- **Beside, named as such**: X's VA null of record, from the door's filed `va/va_null_events.parquet` (L-V.23):
  the same statistics per draw, retests scanned by L-R.26 on the null acceptances, conditioned the same way.
  Every null row carries `null_variant` ∈ (`gaps+order@va_regime`, `tr_tercile_lblock`), the flag
  `x_va_null_of_record`, and X's sentence that the two nulls answer different questions (`tc11x_va.py:195-197`).
- Files: `stage_r/TWO_TRADES_NULL.parquet` (per real cell and variant), `TWO_TRADES_NULL_DRAWS.parquet`,
  `NULL_BOXES_VA.parquet`.
No module of the range machine is imported (L-0.22, L-0.30): the two sources are read as text and mirrored.

SOURCE: contract :79; `tierc10_null.py:109, :120, :224, :239-340, :356-440`; `tierc11_stage_r4.py:112-114, :143,
:713-754, :1058-1065`; `tc11x_va.py:195-197, :236-237`; `LEANS_X.md:1720-1740, :1793-1809`; L-V.23; scout U6 C5,
R-29.

RIVALS: X's VA null alone, labelled "gaps+order" — a relabel: forbidden. X's VA null alone, named — leaves the
contract's named null unbuilt although its law transfers. The pivot detector's warm floor (`ATR_LEN`) as the
lead-gap floor — the value area's first regime cannot start before its lookback. X's seed — TC12's is the
contract's.

FAILS-IF: F-NULL-MIRROR: (a) SCHEDULE — fed the real PIVOT box set of the ten cells (five home assets × 4h, 1d;
`XR/tierc11x/pins/life_ranges.parquet`, `scale_kind == "calibrated"`: `confirm_i`, `die_i`; heights from the
filed boxes by `src_rid`), TC11's seed and K (`MR/stage_r4/build_manifest.json` keys `seed`, `k_draws`), the
pivot's lead-gap floor (the lineage object `ATR_LEN`) and the tape cut at X's pin, the mirrored schedule reproduces
every row of `MR/stage_r4/R4_NULL_BOXES.parquet` on `(draw, box, src_rid, confirm_i, life, censored,
lead_gap_swapped, identity_perm)` exactly and `u` at the write law; (b) MACHINE — on a seeded draw of value-regime
boxes, the mirrored static machine's events up to each box's first acceptance equal `value_area.va_machine`'s on
arrays held constant at the box's edges (a fixture may import the module; no builder does); (c) the filed machine
columns of TC11's boxes (`fate`, `die_i`, `die_side`, `n_harden`) under the pivot's three constants (X's
`pins.laws.dev_return_bars`, `.break_confirm_n`, `.break_margin`), every difference listed and admitted only on a
bar whose close lies within the 6-dp rounding band of the filed height, any other difference RED; (d) two runs
byte-equal. Mutations: the draw seed shifted by one; `order` drawn before `u`; `keep_order=True`; a box built from
`VA(r0)`. [Structural check made while drafting: on all ten cells the `(rid, life)` pairs of the died ranges in
`life_ranges.parquet` equal the `(src_rid, life)` pairs of draw 0 of the filed boxes.]

**L-R.30 THE 1d VALUE-AREA EDGE AS A TAKE-PROFIT VENUE** — "The 1d VA edge as a continuation take-profit venue (v6
remainder at 0.25 ATR_1d of the 1d edge when 1d is INSIDE) — paired, Tier-E only" (contract :79-80)

READING: TC11's P-TP-RNG law, unchanged, with the venue swapped. The law of record, quoted
(`MR/registrations/REGISTRATIONS.json`, registration P-TP-RNG, payload sha256
`ad12a44cd8aeb27cc9a1ab0c4225725462f597a6d1dfc621ddf1e06a484de808`, `operative_spec.scored_arm`): "v6 campaigns; at
each 4h bar, with the 12h as-of state at the bar's OPEN IN_RANGE, a resting limit for the remainder (the position
still open: 1.0, or 0.5 after the v6 harvest) at the 12h far boundary -/+ 0.25 ATR_12h, live only when the prior 4h
close is on the near side AND the level is beyond entry in the trade's favour by > 10 bps; fill at max(level, open)
for a long, min(level, open) for a short; EXPANSION/NONE -> no TP; order STOP -> TP -> BELL -> HARVEST -> TRAIL; v6
harvest kept [L-H.1]".
The swap, term by term, for a v6 campaign at 4h bar `j` after entry:
- as-of at the bar's OPEN: `k = asof_index(close_ms_1d, open_ms_4h[j])`; "12h IN_RANGE" → `1d_state == "INSIDE"`
  at `k`; any other state → no order, the trail runs;
- level: long `1d_vah − a·ATR_1d[k]`, short `1d_val + a·ATR_1d[k]`, on the 1d profile IN FORCE at `k` (the
  block's `vah`, `val`, `atr`); `a` = the contract's "0.25" (:80, pin `tp1d.approach_atr`), asserted equal to the
  AST literal `APPROACH_ATR` of `scripts/tierc11_stage_h.py:133`;
- live iff `d·(level − c[j−1]) > 0` (the prior 4h close on the near side) AND `d·(level − entry_px) > (G /
  BPS_PER_UNIT)·entry_px` (`G` as L-R.14; TC11's `TP_GUARD_BPS`);
- fill iff `h[j] ≥ level` (long) at `max(level, o[j])`, `l[j] ≤ level` (short) at `min(level, o[j])`; the
  remainder exits there, `exit_reason = "tp"`;
- order within the bar: STOP (adverse-first; a TP on a stop bar is counted `fill_blocked_by_stop`) → TP → BELL →
  HARVEST → TRAIL; v6's harvest kept.
**The ride**: every base campaign re-ridden independently from its own entry bar, entry price, stop and R (the SET
is kept: no entry is admitted into a freed slot — TC11 L-1.5), by `T9._ride_leg9`'s body with ONE added site, the
TP test between the stop test and the bell (`scripts/tierc9.py:296-310`); booked by `T7._account_chain`.
**"Paired"**: the key set is the base's; per campaign `delta_r = net_r(venue) − net_r(v6)`; the identity law holds
— a campaign on which the TP never fills carries v6's `net_r`, exit bar and exit reason at 0.000e+00. Printed:
`stage_r/TP1D_CAMPAIGNS.parquet` (per campaign), `TP1D_BARS.parquet` (per ridden bar: `k`, state, level, the three
live clauses, fill), `TP1D_SUMMARY.parquet` (by era and asset: n, n filled, Σ and mean of both books, Σ and mean
`delta_r`, withheld and blocked counts, and the D15 tail ratio `E.T5.d15`, the wall-exit risk P-TP-RNG names). No
interval and no verdict word: the table is attached to no registered row and is descriptive (L-0.28).

SOURCE: contract :79-80; the registration as quoted [read here; file sha256 `648834bf…f1ee`]; `MR/LEANS.md:498-515`
(L-H.1); `scripts/tierc11_stage_h.py:133, :265-293`; `scripts/tierc11_ride.py:204, :208, :613-633, :680-686`;
`scripts/tierc9.py:268-331`; L-V.8 rule 5, L-V.20.

RIVALS: the judging profile `VA(k−1)` for the level — an order rests on the profile in force. The post-harvest
runner only (TC11's twin) — the quoted law's remainder is "the position still open". A CI through the scorer — the
scorer rules arms of registered rows; listed under INTERFACE for the reviser. Importing `tierc11_ride` — O-3.

FAILS-IF: F-TP-MIRROR: (a) IDENT — with every level absent the ride reproduces the `base` arm at 0.000e+00
(canonical sha); (b) ANCHOR — fed TC11's FILED 12h levels (`MR/stage_h/tp_bars.parquet`, `scale_kind ==
"calibrated"`, `level` by `(symbol, entry_ms, bar_open_ms)`) on TC11's corridor, the ride reproduces TC11's filed
P-TP-RNG scored arm: canonical `book_sha256` == `MR/regbooks/P-TP-RNG/scored.json["book_sha256"]`; a bar the ride
asks for that the filed table lacks is RED; (c) AS-OF — the level at bar `j` from 1d tapes cut at `open_ms[j]`
equals the filed one; (d) the identity law on every unfilled campaign. Mutations: the 1d bar still forming read at
`open_j`; TP before STOP; the guard dropped; a freed slot re-admitted.

---------------------------------------------------------------------------------------------------------------
#### D · Build, pins, fixtures

**L-R.31 MODULES, STAGE ORDER, OUTPUTS, STAMPS** — "commit + PROGRESS.json per stage" (contract :5-6)

READING:
- **Modules** (O-1): `scripts/tierc12_rangewalk.py` (pure: the mirrored bar step, walk, fee per fraction);
  `tierc12_stage_r_dir.py` (P-DIR-1's regbook; the chop tables); `tierc12_stage_r_sfp.py` (P-SFP-VA-1's regbook
  and twins); `tierc12_stage_r_tables.py` (the two-trades tables, the nulls); `tierc12_stage_r_tp1d.py` (the
  take-profit venue); `tierc12_stage_r_fixtures.py`. **None is a door and none is a runner**: each reads value-area
  facts only as filed Stage V tables through the reader (L-V.2) and is a DECISION module in L-0.22's strong form —
  neither `analytics.value_area` nor the door is in its import closure. Levels are the filed values (L-V.24).
- **Sub-stages** (L-0.10's dotted children), each with its progress record, after TC12-V and TC12-C are
  COMPLETE-VERIFIED: `TC12-R.dir` → `TC12-R.sfp` → `TC12-R.tables`. Inside `TC12-R.sfp` the order is: the licence
  items (L-R.22) → F-SFP-MIRROR on X's filed trades → the event disposition table → the book of record → the
  twins. No bootstrap is run in Stage R (L-0.10 T5).
- **Outputs.** `T12/regbooks/P-DIR-1/` (`STATUS.json`; `base`, `scored`, `strip`, `tierE__reride`);
  `T12/regbooks/P-SFP-VA-1/` (`STATUS.json`; `scored`, `strip`, `tierE__unfiltered`, `tierE__cell_1d`,
  `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__maker_assumed`); `T12/stage_r/` (the tables of L-R.8,
  L-R.9, L-R.26-L-R.30; `SFP_EVENTS.parquet`, key `[lens, book, asset, entry_ms]`, one row per V2 swing failure
  with its disposition and geometry; `STAGE_R.md`; `build_manifest.json`; `FIXTURES_STAGE_R.txt`). Every regbook
  row carries L-X.24's twenty columns; P-SFP-VA-1's rows add `side`, `t0_i`, `bars_out`, `edge_px` (= `E`),
  `ext`, `atr`, `pivot_stop_px`, `rail_binding`, `T1`, `T2`, `far`, `val_f`, `poc_f`, `vah_f`, `t1_r`, `t2_r`,
  `r_atr`, `rr`, `T`, `time_stop_i`, `t1_i`, `t1_px`, `exit_i`, `exit_px`, `exit_event_ms`, `open_at_w`,
  `bars_held`, the gap flags, `both_touch_bars`, `n1`, `n2`, `funding_r_uncapped`, `funding_ceiling_bound`,
  `stop_px_at_exit`, `n_entry_fills`, `from_state`, both return flags, `l_label`, `t_label`; `lane = "sfp-va-4h"`
  (`"sfp-va-1d"` on the 1d cell).
- **Stamps (V5).** P-DIR-1's kept book is a key subset of v6's instants (asserted, never re-stamped). Each RIDDEN
  range book declares its instants frame to the reader (L-V.19) — kind `{lens, start: "entry"}`; events `entry`
  (its close), `ev_t1_ms` (intrabar: the OPEN of its bar, with a post-event twin), `exit` (stop or T2: the OPEN of
  its bar, with `exit_post_event`; time stop, invalidation: its close), `as_of_pin` for a trade OPEN at the
  window's end — and files `stage_r/VA_STAMPS_<book>.parquet`. A derived twin (`maker_assumed`) shares its
  parent's instants.
- **Registry stamp**: every STATUS, sidecar and manifest carries `registry_head` and `registrations_sha256`
  (L-X.21).

SOURCE: O-1, O-6; L-0.10, L-0.13, L-0.22; L-V.2, L-V.19, L-V.24; L-X.21, L-X.24.

RIVALS: a runner holding the door's accessors — L-V's reader is data-only and its tables carry everything these
builders read. One module for the stage — the gate builder must stay provably separate from the range builders
(`NEVER_RUNNER_T`).

FAILS-IF: F-CLOSURE, F-NOT (L-0); F-KEY, F-DET, F-COLLAR per directory; mutation: `import tierc12_va` planted in a
copy of the gate builder must turn F-CLOSURE RED.

**L-R.32 THE PINS THIS SECTION CONSUMES** — "no number typed that a file can supply" (contract :8)

READING: Every constant of this section, the source read at run time, what it is asserted equal to, and its flow
witness (L-0.17). Rows marked ★ are contributed to L-0's contract pin map.

| pin | read at run time from | asserted equal to | on file | witness when bent |
|---|---|---|---|---|
| ★ `sfp.rail_atr` | contract :71 `railed ≥ … ATR_4h`, pin door | the lineage rail `MIN_STOP_ATR` (`E.BK.MIN_STOP_ATR`, `tierc10_brk.py:510`; defined `tierc3_rules.py:148`) | 1.0 | `r_dist` of a rail-bound row |
| ★ `sfp.t2_offset_atr` | contract :72 `− … ATR_4h (remainder)`, pin door | AST literal `T2_ATR_OFF`, `XR/scripts/tc11x_sfp.py:122` | 0.25 | `T2` of a seeded row |
| ★ `sfp.t1_fraction` | `E.TP.CONTROL_CARD.harvest_frac` (inside `account_l`) | contract :71 "half" (word map), pin door | 0.5 | `n1` of a T1-filled row |
| ★ `rr_min` (veto "rr-min"; shared with L-S) | contract :73, second citation :135-136, pin door | — | 1.5 | the disposition of the event nearest the cut |
| ★ `chop.n_bands` | contract :68 "decile" (word map), pin door | the `range` argument of the `DECILES` generator, read by AST from `tierc11_stage_r.py:168` | 10 | the band of a seeded campaign |
| ★ `tp1d.approach_atr` | contract :80 `… ATR_1d`, pin door | AST literal `APPROACH_ATR`, `tierc11_stage_h.py:133` | 0.25 | the level of a seeded bar |
| "beyond" `B` | `tierc5_rules.STOP_BUF_ATR` (inside `spring_stop`) | — | 0.5 | `stop_px` of a pivot-bound row |
| fee band `G` | `tierc2_rules.FEE_BPS_ROUND_TRIP` | AST literal `REFUSAL_BPS`, `tc11x_sfp.py:123` | 10.0 | a planted event at the band's edge |
| taker, maker, slippage rates | `E.fees()[stem]` (TC12's fee file, L-D) | L-D's F-TOLL | — | `fee_r` |
| `T` (4h, 1d) | fitted-pin door, `va/TRAVERSE.json by_lens.<ℓ>.T_of_record` | F-TRAV (b) | fitted | a time-stop exit bar |
| K, N, M, F, null draws, floor, lookbacks | L-V.4's doors | L-V.4 | — | L-V.4 |
| FLIP_HOLD margin, bars, TTL | `E.BK.FLIP_HOLD_MARGIN`, `.FLIP_HOLD_BARS`, `.MEM_TTL_BARS` | X's `pins.laws` | 1.0, 6, 400 | the hold bar of a seeded retest |
| horizons, `ND` | X's `pins.laws.horizons`, `.round_nd` | AST literals, `tierc10_census.py:123, :136` | 20, 100; 8 | a term's anchor+H bar |
| `MID_BAND` | AST literal, `scripts/tierc11_nest.py:109` | — | (25.0, 75.0) | the cell of a seeded event |
| REPR tolerance | `E.LN.REPR_TOL` | — | 1e-9 | a planted child mismatch |
| W, PIN, era cut, seed, home panel | L-D's objects | L-D | — | — |

SOURCE: contract lines as cited; L-0.17, L-0.23; the objects and literals at the lines cited [read here].

RIVALS: typing any of them — forbidden. Reading the rail or "half" from the contract alone — the function that
applies them is the lineage's; the table says which object each run reads and the pin door holds the other equal.

FAILS-IF: F-TYPED (L-0) on every L-R module; F-TYPED-FLOW: each row's bend must move its witness, a bend that
moves nothing is `PIN-NOT-READ`; mutation: a pin replaced by a typed literal of equal value in a shadow copy of
its consumer.

**L-R.33 THE FIXTURE ROLL OF THIS SECTION** — "FIXTURES (each states its failure condition)" (contract :114)

READING: one suite, `scripts/tierc12_stage_r_fixtures.py`; L-0.14's harness and leg law (BREAK first; a plant
caught only by its named detector).

| fixture | FAILS IF | planted mutation that must turn it RED |
|---|---|---|
| **F-DIR** (contract) | L-R.7 (a)-(g) | L-R.7's list |
| **F-SFP** (contract) | L-R.25 (a)-(i), and the identities named in L-R.10-L-R.24 | L-R.25's list |
| F-SFP-ASOF | a cut-tape event or geometry differs from the full-tape one | `T2` from `ATR[i+1]`; `ext` reading bar `i + 1` |
| F-SFP-MIRROR | the mirrored walk or booking differs from X's filed X2 rows | target-before-stop; the time stop one bar late; maker bps on a taker leg |
| F-CHOP | a cell of L-R.8 / L-R.9 does not re-derive from the rows table | quantile bands; a half-open top band; a refused key moved |
| F-RETEST-MIRROR | L-R.26 (r1), (r2) | an off-by-one window; the hold window one bar short; the band pins |
| F-TWO, F-TWO-MIRROR | L-R.27's cells or L-R.28's ledger and statistics differ | U read at a forming bar; a one-row drop; a shortened horizon |
| F-NULL-MIRROR | L-R.29 (a)-(d) | the seed shifted; the draw order changed; `keep_order=True` |
| F-TP-MIRROR | L-R.30 (a)-(d) | a forming 1d bar read; TP before STOP; the guard dropped |
| F-GRID (per grid) | a declared cell missing, extra or duplicated; a partition sum off | a dropped `n = 0` row |
| F-TYPED-FLOW | a pin of L-R.32 bent at its door moves nothing | a typed literal of equal value |
| F-KEY · F-DET · F-COLLAR (per directory) | L-0.21, L-0.20, L-0.16 | L-0's plants |

SOURCE: contract :114-124; L-0.14, L-0.19.

RIVALS: none.

FAILS-IF: n/a (this reading is the roll).

---------------------------------------------------------------------------------------------------------------
#### E · Unverified at drafting — checked at build, each a HALT or a printed count

- UNVERIFIED: that each hand-walk category of F-DIR (b) and F-SFP (a) has a member. An empty one prints
  NONE-EXISTS and asserts the count zero; an empty T-POC or T-TIME is carried to the report as a finding.
- UNVERIFIED: that `E.BK.frame_l(stem, "1d")` under the TC12 shim is row-identical to `va_bars_1d`. Asserted;
  HALT `SFP-FRAME`.
- UNVERIFIED: that the V2 value regimes satisfy the three preconditions of the gaps+order box set on all ten
  cells. HALT `NULL-GAPS-ORDER-UNBUILDABLE`, and then an amendment — never a relabel of X's null.
- UNVERIFIED: that `MR/stage_h/tp_bars.parquet` holds a row for every bar the mirrored ride reaches on TC11's
  corridor. F-TP-MIRROR (b) is RED on a missing bar.
- UNVERIFIED: that F-SFP-MIRROR's geometry re-derivation from X's filed box columns reproduces X's filed stops and
  targets at the write law on every row (it rests on the box edges being tape prices). A difference HALTs for an
  amendment before any V2 book is built.
- UNVERIFIED: that X's `die_parity` rows carry outcome columns on every `sfp` and `retest-hold` row at 4h and 1d
  (on file: all but four). F-TWO-MIRROR compares the rows that carry them and prints the count.
- UNVERIFIED: the count of v6 campaigns the gate refuses, and whether every home asset keeps at least one campaign
  (L-X.7's panel clause decides the word if not).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · P-DIR-1

- **id:** P-DIR-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1; two registrations stand under that header (:65, :69).
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :65).
- **mechanism:** A v6 trend entry taken while the 4h lens stands ACCEPTED outside value on the side opposite to the trade is an entry against a price the market has already accepted away from value in the other direction: the entry bar's 12/26 trigger fires inside a move the value-area machine reads as established against it. The gate removes those entries and nothing else. It is a statement about the STATE of value at the entry close (acceptance needs eight consecutive closes beyond the edge or one close a large multiple of ATR beyond it), not about distance, tide or range position; it is independently failable from P-SFP-VA-1, which trades a different event on a different book.
- **population:** the five home assets (contract :18); lens 4h; the base book = card v6 as TC11 filed it, every campaign (L-R.1); era of record the full corridor (no era is named; TC11 L-1.3); scored window per O-9: campaigns whose entry bar closes at or before TC11's pin, read by object from `research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`; campaigns entered in the forward strip are printed beside, unscored.
- **arms:** two arms and no re-ride (O-21; L-R.4).
  - `base` — the v6 book on the scored window, bit-equal on the sixteen regbook columns to TC11's filed v6 (canonical `book_sha256` == `research_outputs/tierc11/scores/BASE_IDENT.json["book_sha256"]["P-AGE-1"]`).
  - `scored` (the treated arm) — `base` minus every campaign with `refuse == True`, where `refuse ⇔ (direction == +1 AND state == "ACCEPTED_BELOW") OR (direction == −1 AND state == "ACCEPTED_ABOVE")` and `state` is the filed 4h state after the entry bar's close: row `k = asof_index(4h closes, entry_close_ms)` of `research_outputs/tierc12/va/va_bars_4h.parquet`, with `close_ms[k] == entry_close_ms` asserted (L-R.2, L-R.3). Kept rows are identical to their base rows.
  - VA columns read (declared for F-VA-PINS (e)): `4h_state`, `4h_bar_close_ms`; printed only: `4h_pct`, `4h_edge_dist_atr`, `4h_accept_age`, `4h_armed_top`, `4h_armed_bottom`. No `1w_` column.
- **statistic:** `mean(net_r of the kept book) − mean(net_r of the whole v6 base)` (kept versus all, never kept versus refused).
- **comparison:** two-sample vs v6 (contract :65). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot_diff` with one asset pick per draw indexing both arms; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:** none. The gate trades no range and no licence word governs it; no closing condition exists and the word CLOSED BY PRECONDITION cannot occur on this row. Inputs pinned by sha, not preconditions: `research_outputs/tierc12/va/va_bars_4h.parquet` (certified by `progress/TC12-V.json`), the `base` arm (certified by `progress/TC12-C.json`).
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m = 0.10 ÷ 2 = 0.05, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. Asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. The exhaustive words of this row: SUPPORTED (a, b and c hold); NOT SUPPORTED (any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, TWO-SAMPLE-PREMISE when the gate refuses nothing, 'CI wholly below zero' when hi < 0); CLOSED BY PRECONDITION is unreachable (no precondition). The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the refused cohort's n, mean and ΣR with ΣR of both books, and, iff mean(refused) > 0, 'on per-campaign expectancy only; the gate forfeits +X R total'. Tier-E arms carry no verdict word. This registration carries selection_hazard only and prints '<verdict> — NOT CONFIRMATORY (selection_hazard: DIRECTION-INFORMED)'.
- **labels:** `selection_hazard`, per O-23.
  - tag: DIRECTION-INFORMED.
  - label: NOT CONFIRMATORY.
  - text: "the direction of this gate (refuse an entry taken against an acceptance) was informed by TC11's R5 alignment table on this same v6 book and corridor, by pivot state: expansion aligned +0.491349 mean net R over 47 campaigns against expansion counter −0.493933 over 12; the value-area state itself was not tabulated against v6 outcomes in any filed table; new here are the detector and the interval".
  - items: `research_outputs/tierc11/stage_r/R5_CHOP_DIRECTION.parquet` (sha256 `a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`), cells `calibrated|4h|alignment|EXP_ALIGNED` and `calibrated|4h|alignment|EXP_COUNTER`; `research_outputs/tierc11/stage_r/R5_CHOP.md:120-121`; contract :67.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves (sensitivity seed, haircut, taker twin, tuning and holdout slices, LOAO, both shares, literal bar, exact enumeration, month-block, drop-OPEN, strip).
  - `tierE__reride` — the re-ride twin with the refusal inside the replay (L-R.5), with its admitted-not-in-v6 and not-taken counts and the rejection-log rival count.
  - The with-vs-against acceptance table `stage_r/VA_CHOP_ALIGNMENT.parquet` (L-R.9), whose 4h ACCEPTED_AGAINST cell is the refused cohort; printed in the report's §0.2.
  - The full VA chop table `stage_r/VA_CHOP.parquet` — v6 by 4h and 1d state × fixed %-of-value band (L-R.8).
  - Counts only, no outcome: the campaigns the prior-bar as-of reading would refuse instead; refusals with both sides disarmed; refusals whose entry close lies inside the rolling value area.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-DIR (a) set equality and post-filter identity; (b) three refusals and two kept witnesses hand-verified by the frozen key-order rule; (c) the as-of on cut tapes; (d) the un-gated book must FAIL; (e) the synthetic truth table; (f) the re-ride identity; (g) the label's quoted cells.
  - F-BASE-IDENT, F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0).
  - F-CHOP and F-GRID on the two chop tables; F-CLOSURE with the gate builder in `NEVER_RUNNER_T`; F-VA-PINS (e).

### REGISTRATION SPEC · P-SFP-VA-1

- **id:** P-SFP-VA-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1.
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :69).
- **mechanism:** A probe beyond a value-area edge that closes back inside within three closes is a failed auction at that edge: the market tested prices outside value and did not accept them. Inside an unaccepted value area the next reference prices are the point of control and then the opposite edge, so the failure is faded toward them with a stop beyond the extreme the probe reached, a time stop at the lens's own edge-to-edge traverse, and an exit if the lens does accept beyond the faded edge after all. The trade needs no trend and no tide; it stands on the range being respected, which is what the value-area feasibility licence at 4h (taker) asserts. It is independently failable from P-DIR-1.
- **population:** the five home assets (contract :69-70), both directions pooled; lens 4h; every V2 swing failure at VAH or VAL (L-R.10); era of record the full corridor (contract :69) inside the scored window per O-9: trades whose entry bar closes at or before TC11's pin, read by object; a trade open at that instant is marked there (`corridor_end`) and listed OPEN; the forward strip is ridden and printed beside, unscored.
- **arms:** one arm, `scored`; no base (vs zero). Per swing-failure row of `research_outputs/tierc12/va/va_events.parquet` (lens 4h), in bar order per asset: (1) one position per asset — an event at bar b is skipped iff `entry_i < b ≤ exit_i` of the open trade; (2) geometry; (3) rr-min; (4) the walk.
  - Entry: `entry_px = e` = the close of the return bar, taker; direction = the event's sign (failure at VAH short, at VAL long).
  - Stop: `tierc10_brk.brk_stop` (= `tierc5_rules.spring_stop`) on `ext` = the probe's extreme including the return bar: long `min(ext − B·A, e − RAIL·A)`, short mirrored; `B` = `STOP_BUF_ATR`, `RAIL` = the contract's 1.0 (:71), `A` = ATR_4h of the return bar; `R = |e − stop|`, fixed for life.
  - Targets, frozen at entry on the profile whose edge was probed, VA(t0−1): `T1` = its POC (`poc_f`), the card's harvest fraction ("half") off; `T2` = its far edge − d·0.25·A (contract :72), the remainder.
  - Refused (geometry) iff `d·(T1 − e)` or `d·(T2 − e)` is at or under the round-trip taker fee of the entry price, or `d·(T2 − T1) ≤ 0`, or the stop is undefined. Skipped (rr-min) iff `d·(T2 − e) / R < 1.5` (contract :73).
  - Walk on 4h bars from the bar after entry: the open decides first; then the stop, adverse-first, at the stop price; then T1 at max(T1, open) (min for a short); then T2 likewise, same bar if reached; then at the close the invalidation — the first V2 acceptance on the faded side — then the time stop at the close of bar `entry_i + T`, T the fitted 4h traverse read by object (`va/TRAVERSE.json by_lens.4h.T_of_record`). No trail, no stop move, no tide read.
  - Booking: `tierc10_brk.account_l` on the 4h lens frame with T1 as the harvest slice; taker on every leg; interval-sum funding with the D12 ceiling once; `net_r = gross_r − fee_r − funding_r` in units of R.
  - VA columns read (declared for F-VA-PINS (e)): from `va_events` — `kind`, `side`, `t0`, `i`, `E`, `extreme`, `sgn`, `val_f`, `poc_f`, `vah_f`, `close_i`, `atr_i`, `known_close_ms`; from `va/TRAVERSE.json` — `by_lens.4h.T_of_record`; from `va/VA_MIRROR.json` — the licence selectors. No `1w_` column.
- **statistic:** `mean(net_r of the scored book)`.
- **comparison:** vs zero (contract :69). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot`; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:** two items, evaluated before any arm is built, both from the record `research_outputs/tierc12/va/VA_MIRROR.json` (certified_by `research_outputs/tierc12/progress/TC12-V.json` → `artifact_shas`), which quotes `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha256 `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`).
  - selector `licence["4h|taker"].by_era["ALL"].would_read`, required `"PASS"` — the licence row of the row's own scoring era (O-17).
  - selector `licence_set`, required to contain `"4h|taker"` — the contract's word of record (:39-41).
  - If either is not met: STATUS only, no arm, and the cell reads 'CLOSED BY PRECONDITION (research_outputs/tierc12/va/VA_MIRROR.json#<selector> reads <found>; required <required>) — no number · no test spent'.
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m = 0.10 ÷ 2 = 0.05, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. Asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. The exhaustive words of this row: CLOSED BY PRECONDITION (a precondition item is not met; checked first; no ruler is called); SUPPORTED (the preconditions are met and a, b and c hold); NOT SUPPORTED (the preconditions are met and any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, 'CI wholly below zero' when hi < 0). The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the licence words of the three eras. Tier-E arms carry no verdict word. This registration carries pre_seen and prints '<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)'.
- **labels:** `pre_seen`, per O-23.
  - tag: none.
  - label: IN-SAMPLE RE-SCORE, NOT CONFIRMATORY.
  - text: "TC11-X's X3 printed value-area swing-failure outcomes at 4h on these five assets for every bar at or before 2026-09-25T00:00Z before this row was drafted, and this trade form (stop, split targets, time stop, invalidation, minimum reward) was never scored; X's standing ledger line marks any later value-area registration pre_seen on those bars; the K = 3 and one-close-acceptance variants are among the printed tables".
  - items: `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha256 `a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0`; detector `va`, trade `swing_failure`, variants `k3` and `die_parity`, lens `4h`); `research_outputs/tierc12/x_rec/tierc11x/va/X3.md`; `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md:1816-1818, :2468-2470`; `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves; on this all-taker arm the taker twin reads IDENTICAL TO THE RECORD; the haircut leaf is the charter twin (TC11 AM-7).
  - The holdout slice (contract :74), with the sentence "causal for the tuning-fit T and lookback only; the class was pre_seen; the era of record is the full corridor".
  - `tierE__unfiltered` — the book without the rr-min skip, re-walked with its own one-position sequence (contract :74).
  - `tierE__cell_1d` — the same law on the 1d lens (contract :74), with the three era words of the `1d|taker` licence printed as `licence_would_read_by_era`.
  - `tierE__guard_1d` — the 4h book refusing an event when the 1d state at the entry close is accepted against the trade (contract :75).
  - `tierE__maker_conditioned` and `tierE__maker_assumed` — the maker twin (contract :75): maker bps on entry, T1 and T2, taker on the stop, the time stop, the invalidation and the mark; the conditioned arm books only if the first 5m bar after the entry close trades strictly through the entry price.
  - `stage_r/SFP_EVENTS.parquet` — every swing failure with its disposition (traded, one position, geometry reason, rr-min) and geometry; counts only for the rivals not carried as books (T1-collapse, the entry-time profile, re-entry at an intrabar exit close).
  - Disclosures on the row: D-2 and D-3; "T tuning-fit"; the lookback label; `n_open_at_w`.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-SFP (a) three trades hand-walked by the frozen key-order rule — the first POC fill, the first other time-stop exit, the first other stop; (b) the row identities; (c) one position; (d) the scored-window identity; (f) fees and net; (g) the synthetic same-bar set; (h) the closed row on a planted licence; (i) the guarded twin.
  - F-SFP-ASOF; F-SFP-MIRROR against X's filed X2 trades; F-TRAV (a), (e) (L-V); F-TYPED-FLOW on `sfp.rail_atr`, `sfp.t2_offset_atr`, `sfp.t1_fraction`, `rr_min`, `traverse.4h`.
  - F-FAM (PLANTED), F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0); F-VA-PINS (e); F-NOT (no trail, no add, the edge is a VA edge, no 5m signal).

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **The lens above 1d.** The contract conditions the 1d two-trades "on the lens above" (:78-79); that lens is 1w,
   which O-11 holds captured-only. DEFAULT if silent: the 1d two-trades are printed UNCONDITIONED (every 1d event
   in cell `NA`); the 1w state is neither read nor partitioned on. Only the operator can order the 1w block (on
   its borrowed lookback, L-V.5) read as a Tier-E conditioning axis.
2. **What "null gaps+order (R10)" means on a value area.** R10 is a pivot-box null. DEFAULT if silent: the
   gaps+order schedule is run on value regimes (L-R.29) and X's value-area null of record is printed beside, each
   row naming its null; if the box set cannot be built the stage HALTs for an amendment. The operator may instead
   rule that X's null alone answers the clause.
3. **"Anchor entry".** DEFAULT if silent: every campaign of the v6 base (L-R.1). If a narrower population was
   meant, only the operator can name it; no narrower one exists on disk.
4. **The 1d cell's era.** The `1d|taker` licence passes on the holdout and fails on the full corridor and on
   tuning (O-17). DEFAULT if silent: the 1d cell is built on the full corridor like its parent row, labelled ERA
   NOT LICENSED there, with its holdout slice printed first. The operator may order it holdout-only.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

- **L-0 (laws, process).** The pin map takes the ★ rows of L-R.32 (`rr_min` shared with L-S, veto "rr-min").
  `FIVE_MIN_READERS_T` gains TC12-R for the ONE read L-R.24 declares (the maker-conditioned twin's fill child and
  fill-bar walk). The five L-R modules are DECISION modules; none is added to `RUNNERS_T`, and
  `tierc12_stage_r_dir.py` is in `NEVER_RUNNER_T`. **Two differences for the reviser:** (i) L-0.22 lists
  `scripts/tierc12_va_stamps.py` as a door and expects range builders to be runners using accessors; L-V.2 makes
  it a data-only reader that is not a door. This section is drafted on L-V's (the owner's) definition, which is
  also the stricter closure; L-0.22's objection to a file-only consumer (the rounding trap) is answered by L-V.24
  (the filed value IS the level of record). (ii) L-0.25 (iii) forbids the 1w block as a conditioning axis while
  L-V.5 expects the 1d two-trades to be conditioned on it; this section follows L-0.25 and O-11 (OPEN 1,
  OBJECTION). The mirrors of `tierc10_null.schedule` / `static_box_machine` and of the census outcome road are
  read from source TEXT; no range-machine module is imported, so L-0.30's PIVOT-RANGE leg needs no exception.
- **L-D (substrate, env).** `E.BK` (`frame_l` for 4h and 1d with funding, `account_l`, `funding_interval`,
  `brk_stop`, `MIN_STOP_ATR`, the three FLIP_HOLD pins), `E.T9` (`_ride_leg9`, `card_candidates9`, `replay9`'s
  loop), `E.T7._account_chain`, `E.T5.d15`, `E.TP.CONTROL_CARD`, `E.LN.REPR_TOL`, `E.fees()` (taker, taker round
  trip, maker, slippage per stem), `E.era_of`, `E.TC11_PIN_MS`, `E.PIN_MS`, `E.CLASSIC5`, `E.load_asof` (5m of the
  home assets) and `E.load_asof_at`. `TC11_ALLOW_FILE` rows this section needs: `stage_r/R5_CHOP_DIRECTION.parquet`,
  `stage_r/R5_CHOP.md`, `stage_r4/R4_NULL_BOXES.parquet`, `stage_r4/build_manifest.json`, `stage_h/tp_bars.parquet`,
  `regbooks/P-TP-RNG/scored.parquet`, `regbooks/P-TP-RNG/scored.json`, `registrations/REGISTRATIONS.json`,
  `scores/BASE_IDENT.json` (each certified in `MR/PROGRESS.json`) [verified here]. `x_rec` rows:
  `tierc11x/sfp/X2_trades_4h.parquet`, `X2_trades_1h.parquet`, `X2_twins.parquet`, `tierc11x/va/events_va.parquet`,
  `va/two_trades.parquet`, `va/build_manifest.json`, `va/feasibility.parquet`, `pins/life_ranges.parquet`,
  `scripts/tc11x_sfp.py`, `scripts/tc11x_va.py`. The fee file's `maker_pin.x_assumed_bps_side` (L-D.19) is what
  F-SFP-MIRROR books X's maker rows at. AST-literal reads of frozen SCRIPT text (`scripts/tierc11_nest.py`,
  `tierc11_stage_h.py`, `tierc11_stage_r.py`, `tierc10_null.py`, `tierc10_census.py`) are permitted reads under the
  hook; assumed so, since L-D.27's read-never classes do not list `scripts/`.
- **L-V (value area).** `va_bars_<ℓ>` with `state`, `pct`, the judging and in-force profiles, `atr`, `close_ms`,
  the nest flags; `va_events` with the L-V.14 fields, including `acceptance` rows carrying `side`, `i`, `E`;
  `va_regimes`; `va_null_events` for 4h and 1d with `acceptance` and `swing_failure` rows carrying `E`, `i`,
  `side`, `draw`; `TRAVERSE.json` with a 1d row and its `provisional` flag; `VA_MIRROR.json` with
  `licence[…].by_era` for `4h|taker` and `1d|taker` and `licence_set`; the reader's `stamp`, `events`, `regimes`,
  `bars`, `licence`. L-V's open asks, answered here: (i) no return flag is required (L-R.10); (ii) the frozen
  profile `*_f` sets POC and far edge (L-R.12); (iii) invalidation = the first acceptance row on the faded side
  (L-R.17); (iv) the retest scan is L-R.26; (v) the cells are L-R.27; (vi) the per-draw statistic and the
  gaps+order analog are L-R.29.
- **L-X (statistics, registrations, close).** In the two REGISTRATION SPEC blocks the five checked fields (`id`,
  `family`, `family_m`, `family_bar`, `prior`) carry the bare value first and, after a dash, the contract line it
  is parsed from (no family number is typed); assumed: the filer's carry law (L-X.18) checks the leading token. If
  it compares the whole bullet, the text after the dash is dropped at assembly and nothing else changes. The
  regbook interface (L-X.24) accepts the extra columns of L-R.31; the scorer derives the common leaves and rules
  each `tierE__` arm CI-only; the two templates of L-X.13 stand; §0.2 quotes `VA_CHOP_ALIGNMENT`; `exit_reason =
  "corridor_end"` marks a position open at W. Assumed: the scorer takes no arm that belongs to no registered row, so
  L-R.30's
  take-profit table is descriptive and prints no interval; if L-X adds a paired leaf for an unattached table the
  reviser rules it before freeze.
- **L-C (control).** The `base` arm bit-equal to TC11's v6; the strip book; v6's rejection log with reasons; the
  v6 stamp table whose `entry` rows L-R.4 asserts against; per campaign `entry_i`, `entry_px`, `stop_px`,
  `r_dist` for L-R.30's independent re-rides.
- **L-G (admission).** A v6 replay with a refusal hook `refuse(sym, ti, d) → bool` for the re-ride twins. If L-G
  files none, L-R.5 is the specification this section builds (a mirror of `tierc11_stage_g.replay_g`).
- **L-S (scalper).** `rr_min` is one pin for both sections. The SFP maker twin keeps X's fill law (strict
  trade-through of the first 5m bar, no tick) while L-S's fill of record is through-by-one-tick; if the reviser
  wants one fill law for every maker row in the tier, L-S's is the stricter and replaces L-R.24's by one sentence.
  `scripts/tierc12_rangewalk.py` is offered to L-S for the stop / T1 / T2 bar step; if L-S writes its own, F-SCALP
  holds it.
- **L-L (ledger, era, ferry).** Ferry classes: the regbook arms and `SFP_EVENTS`, `VA_CHOP_ROWS`,
  `TP1D_CAMPAIGNS` are per-trade or per-campaign row files; `TP1D_BARS`, the null draw tables and the stamp tables
  are pointed to; the grids are printed whole in the report.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

**OBJECTION O-11 — the scope of "captured-only" leaves a contract clause with no object at 1d.**
- *The fact.* The contract orders "the two trades per lens on the VA at 4h and 1d … conditioned on the lens above
  {accepted aligned · inside mid · inside at its own edge (coincidence)}" (:76-79). The estate's ladder puts 1w
  above 1d (`scripts/tierc11_nest.py:101`: `"1d": "1w"`), and V5 orders a 1w member of the value-area vector
  (:44-45). O-11 rules "The 1w VA is a captured-only stamp column (V5), Tier-E", which the sibling draft L-0.25
  (iii) reads as "read by no gate, no permission, no direction guard, no conditioning axis" and enforces by F-NOT
  (leg 1W). Read that way, the contract's conditioning clause cannot be built for the 1d trades. The sibling draft
  L-V.5 reads the same ruling the other way (its OPEN item 1 treats the 1d conditioning on 1w as the default).
- *Why it matters.* The 1d rows of the contract's own table lose the three cells the contract names; and two
  foundation sections disagree on what O-11 permits.
- *The reading proposed.* O-11 reads: "No 1w range cell exists — no trade, no order, no feasibility row, no
  licence, no gate, no permission. The 1w state MAY be read as the lens-above conditioning axis of the Tier-E 1d
  two-trades table (contract :76-79), labelled BORROWED-LOOKBACK on every row, and by nothing else." Under it,
  L-R.27's 1d rows take the same eight-cell partition with U = 1w, F-NOT's 1W leg exempts that one table by name,
  and nothing registered changes.
- *Drafted under the ruling as written.* L-R.27 puts every 1d event in cell `NA`; no L-R module reads a `1w_`
  column; the default is OPEN TO OPERATOR item 1.
