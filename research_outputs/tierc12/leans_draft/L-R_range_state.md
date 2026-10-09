## L-R · THE RANGE-STATE FAMILY

This section governs Stage R of the contract (lines 64-80) and the two fixtures the contract names for it (F-DIR,
F-SFP; :118-119). It fixes: the direction gate P-DIR-1 — its population, the as-of instant of the 4h value-area state,
the refusal predicate, its post-filter arms, its re-ride disclosure, its Tier-E chop tables; the swing failure as a
range trade P-SFP-VA-1 — event, entry, stop, the two targets, the degenerate geometries, the minimum-reward skip, the
time stop, the invalidation exit, the bar walk, the R-multiple with split targets, the scored window, the licence
precondition and its Tier-E cells and twins; the DEFINITIONS of the Tier-E two-trades tables on the value area at 4h
and 1d with their lens-above partition, base rate and null (BUILT by Stage V's second door at the record
`TC12-V.trades`, L-V.2); and the Tier-E 1d value-area edge as a take-profit venue. It owns two registered rows of the
RANGE-STATE family (contract :64): P-DIR-1 and P-SFP-VA-1. It conforms to ORCHESTRATOR_RULINGS O-1..O-32; the one
objection this section filed was accepted (O-28).

**Drafting record.** Read while drafting, all read-only: the contract (sha256 `861d6050…a7bd`); ORCHESTRATOR_RULINGS
(`c280a972…f509`, as it stood before section H); DISCLOSURES; scout maps U6 (`8315e351…bc4e`) and U2
(`50109e8b…3aef`); the sibling drafts L-0 (`2c6e9ba5…2a73`), L-D (`9ed43441…79af`), L-V (`5d653d6f…ee1a`) and L-X
(`6d1b5055…c263`) as they stood; TC11's `LEANS.md`, `LEANS_AMENDMENTS.md` (AM-7) and
`registrations/REGISTRATIONS.json`; X's `LEANS_X.md` and `REGISTRATION_PLAN.md` under `x_rec/`; as TEXT, never
imported: `x_rec/scripts/tc11x_sfp.py` (`79ba35f4…0f95`), `x_rec/scripts/tc11x_va.py` (`3f6a43cb…a422`),
`scripts/tierc9.py`, `tierc10_brk.py`, `tierc10_null.py`, `tierc10_census.py`, `tierc5_rules.py`, `tierc7.py`,
`tierc11_stage_r.py`, `tierc11_stage_r4.py`, `tierc11_stage_g.py`, `tierc11_stage_h.py`, `tierc11_ride.py`,
`tierc11_nest.py`. Inspections were structural (schemas, key counts, lane and exit-reason value sets, row counts per
variant, sha256). Filed numbers the drafter printed while verifying a fact, none of them an outcome of a TC12 rule and
none used to choose a reading: TC11's R5 alignment rows (the two figures the contract itself quotes at :67); the row
counts of X's filed twin books and event variants; and the sidecar of TC11's filed P-TP-RNG scored arm (n, Σ net_r and
exit-reason counts of the 12h pivot venue), opened to confirm that TC11's take-profit ride is 4h-granular. No R, mean,
hit rate or count of any TC12 book was computed. Counts quoted from filed records are EXPECTATIONS a fixture reads at
run time, never inputs.

**Revision record.** Revised once, before the freeze, under the LEANS review of 2026-10-09
(`T12/review/ORCHESTRATOR_DISPOSITIONS.md`, OD-0..OD-19; `T12/review/CROSS_SECTION_CANON.md`). Re-opened while revising,
read-only and as TEXT: the contract; ORCHESTRATOR_RULINGS O-1..O-32; `scripts/tierc10_brk.py:1215-1330`
(`funding_interval`, `account_l`); `x_rec/scripts/tc11x_sfp.py:115-128, :483-520, :558-601, :660-712`;
`x_rec/tierc11x/LEANS_X.md:1292-1316, :1336-1342, :2305-2322`; `scripts/tierc11_stage_r.py:1640-1665`;
`scripts/tierc11_stage_g.py:440-460, :544-568`; `scripts/tierc10_null.py:356-445`; the lineage literals at the lines
L-R.32 cites; and the column names (no value) of `research_outputs/tierc11/stage_r/NEST_v6.parquet` and
`R5_CHOP_DIRECTION.parquet`. No outcome of any book was computed, and no reading was chosen between rivals by which
would score better: each change is decided on contract text, ruling, disposition or mechanism.

**Notation.** Paths are relative to `/Users/luis/Naiad`; `T12` = `research_outputs/tierc12`; `MR` =
`research_outputs/tierc11`; `XR` = `T12/x_rec`. `E` = the TC12 env shim `scripts/tierc12_env.py` (L-D); `E.BK` =
`tierc10_brk`, `E.T9` = `tierc9`, `E.T7` = `tierc7`, `E.T5` = `tierc5`, `E.TP` = `tierc10_panel`, `E.LN` =
`tierc10_lanes`, `E.D` = `tierc10_data`, `E.TB` = `tierc2_baseline`, `E.R2` / `E.R3` / `E.R5` = `tierc2_rules` /
`tierc3_rules` / `tierc5_rules` (lineage modules the shim imports as-is, L-D.29). W = the score edge `E.TC11_PIN_MS`
(O-9); PIN = `E.PIN_MS`; `ERA_CUT` = `E.ERA_CUT_MS`. For one asset and lens ℓ: bars `t` with `open_ms[t]`, `o, h, l,
c`, `close_ms[t] = open_ms[t] + step_ℓ`; `ATR_ℓ[t]`; `VA(t)` as L-V defines it. `d` = trade direction, +1 long, −1
short. "The reader" = `scripts/tierc12_va_stamps.py` (L-V.2: a data-only DECISION module, not a door; it recomputes
nothing and asserts each Stage V file's sha before the first read). "DOOR 1" = `scripts/tierc12_va.py`, "DOOR 2" =
`scripts/tierc12_va_trades.py` (L-V.2: the only two non-fixture modules that import `analytics.value_area`).
`certified(path)` = `tierc12_progress.certified` (L-0.4): the last progress record that names the path, with its sha.
"Round6" = the estate's write function `E.TB._round_floats`. `BPS_PER_UNIT`, `PCT_PER_UNIT` = the two unit constants of
`scripts/tierc12_units.py` (L-0.17). A value written "(on file: v)" is orientation for the reader; the constant the
build uses is the named object, read at run time (L-R.32 lists every one).

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

FAILS-IF: F-DIR [a]: the refused ∪ kept key set must equal the base's key set; mutation: a base row with
`lane = "spring"` planted in a copy must HALT `DIR-POPULATION`.

**L-R.2 THE AS-OF OF THE 4h VALUE-AREA STATE** — "when the 4h VA state is ACCEPTED" (contract :65-66)

READING: The state is read at τ = the campaign's `entry_close_ms` — the CLOSE of its entry bar — from the FILED
per-bar table `T12/va/va_bars_4h.parquet` (L-V.24), opened through the reader's `bars("4h")` (the file's sha asserted
through `certified()` before the first read, L-V.2): `k = tierc12_asof.asof_index(close_ms_4h, τ)` on the campaign's
asset (O-14: a bar is visible iff its close ≤ τ), and the state is row k's `state` — the machine's state AFTER bar k
(L-V.13). The entry bar is itself a bar of the same 4h tape, so `close_ms[k] == τ` and the row is the entry bar's own;
the builder asserts that equality on every campaign and HALTs `DIR-ASOF` on any difference. So the answer to the
contract's open point is: **the state after the entry bar's close**, in which that close (`c[k]` = the campaign's
`entry_px`) has been judged against `VA(k−1)` — or against the frozen edge of a pending probe — with `ATR_4h[k]`.
Nothing later than the close of bar k is read: `VA(k)` itself judges nothing at k (L-V.8 rule 2).
Why this instant: v6's entry decision is taken at that close and with that bar's own close-time quantities —
`entry_px, atr_sig = float(f.c[ti]), float(f.atr[ti])` and the stop from `RC.struct_stop_4h(…, ti, entry_px, d,
atr_sig, …)` (`tierc9.py:394-399`), `entry_ms = open_ms[ti]` (:412). The gate therefore reads no fact the card does
not already hold when it enters. It is the estate's stamp law for an entry: "Close events (arm, entry, harvest, bell,
add, exit at a close) are stamped at their close" (`MR/LEANS.md:221`), and R5 — the table this gate's direction comes
from — read its state at `instant_kind == "entry"` with instant `entry_close_ms`
(`scripts/tierc11_stage_r.py:1319, :1480-1487`).
The value read is the FILED `state` string; the gate never re-derives a state from filed levels (O-29). The gate's
rows file what they read under the stamp block's names (`4h_state`, `4h_bar_close_ms`, …; L-V.20), and the builder
asserts them equal, column by column, to the same `4h_` columns of the `entry` rows of
`T12/va/stamps/VA_STAMPS_v6.parquet` (filed by the reader at `TC12-V.stamps.c`, L-V.19; no column of another lens is
opened): two reads of one filed row that must agree.

SOURCE: O-14, O-29; L-V.2, L-V.8, L-V.13, L-V.19, L-V.20, L-V.24; `tierc9.py:394-399, :412`; `MR/LEANS.md:219-224`
(L-R.5); `tierc11_stage_r.py:1319, :1480-1487`; L-0.28 (`tierc12_asof.asof_index`).

RIVALS: the state at the last 4h close STRICTLY BEFORE the entry bar's close (row k−1) — the engine's exec-open law
(`engine/htf.py:15-25`), right for an order placed DURING bar k, wrong for a decision taken AT its close; O-14 rules
`≤`. Not taken, and not printed as a book: its effect is disclosed as COUNTS only (L-R.5). The state at the next bar —
a future leak; it is F-DIR's plant.

FAILS-IF: F-DIR [c] and [e]; mutations: the predicate fed row k+1; fed row k−1.

**L-R.3 "ACCEPTED OUTSIDE VALUE AGAINST THE TRADE'S DIRECTION" — THE PREDICATE** — "ACCEPTED outside value AGAINST
the trade's direction (accepted below for a long; above for a short)" (contract :66)

READING: With `d` the campaign's `direction` and `s` the string of L-R.2:

    refuse(campaign)  ⇔  (d == +1 AND s == "ACCEPTED_BELOW")  OR  (d == −1 AND s == "ACCEPTED_ABOVE")

`s` is a member of `STATE_NAMES` (L-V.2) compared by exact string equality. Every other case is KEPT: INSIDE;
PROBING_ABOVE and PROBING_BELOW in either direction (a probe is "not yet accepted", contract :34); ACCEPTED on the
trade's own side (above for a long, below for a short); UNDEFINED. "Outside value" is what the ACCEPTED state means
(contract :35) and is not a second condition: the gate applies no position test of its own. Where both sides stand
disarmed the state column reports one side by L-V.13's position rule and the gate follows the column. Every campaign's
row of `VA_CHOP_ROWS.parquet` (L-R.8) files `refused` and the columns the gate read or prints, under the stamp block's
names: `4h_state`, `4h_pct`, `4h_edge_dist_atr`, `4h_accept_age`, `4h_armed_top`, `4h_armed_bottom`,
`4h_bar_close_ms`, `4h_L`, `4h_l_label` (the lookback and its tuning-fit label, L-V.4). Printed counts, deciding
nothing: refused by direction; refused with both sides disarmed; refused whose entry close lies inside the rolling
`VA(k−1)` (`0 ≤ 4h_pct ≤ PCT_PER_UNIT`); kept under PROBING against the direction; UNDEFINED at entry (expected zero:
v6's warm floor, `Roles.floor_bars`, is never below the estate's `WARMUP_BARS`, which exceeds the 4h lookback; the
count is printed and such a campaign is kept, not refused).

SOURCE: contract :34-35, :65-66; L-V.4, L-V.13 (the state column; `acc_side`), L-V.16; `scripts/tierc9.py:111-116`
(`floor_bars`).

RIVALS: also refuse PROBING against the direction — the contract says ACCEPTED. Also require the entry close outside
the rolling VA — a second condition with no phrase behind it (its count is printed). Refuse on the 1d state as well —
not in the row's text; the 1d state appears only in the chop table.

FAILS-IF: F-DIR [a], [b], [e]; mutations: the sides swapped (refusing acceptance WITH the trade); PROBING treated as
ACCEPTED.

**L-R.4 THE GATE IS A POST-FILTER; THE ARMS; THE STRIP** — "(two-sample vs v6)" (contract :65); O-21, O-9

READING: `regbooks/P-DIR-1/` holds exactly three arms (L-X.24's arms of record), each written by
`tierc12_regbook.write_arm` (L-0.13's `put_regbook`: full float, the key asserted unique) with its sidecar, beside
`STATUS.json` (`status = "BUILT"`; the row has no precondition) and `build_manifest.json`:
- `base` — the v6 book on the scored window: the frame `tierc12_books.base_regbook_frame()` returns (L-C.4), every
  row with `entry_close_ms ≤ W`; one canonical `book_sha256` equal to TC11's filed value (F-BASE-IDENT). Sidecar:
  `kind = "base"`, `ruler = "two_sample"`, `era_scope = "full"`, `lens = "4h"`, `toll = "taker"`; `lane = "card"` on
  every row.
- `scored` — `base` minus the refused campaigns, by key `(symbol, entry_ms)`; every kept row identical to its base row
  on the sixteen columns (L-X.25 GATE-POSTFILTER). No campaign is re-ridden for the row of record: a refused entry
  does not free its slot (TC11 L-1.5, `MR/LEANS.md:147-148`).
- `strip` — under the column `arm` (L-X.24; OD-14): the v6 campaigns of L-C's extended ride with `W <
  entry_close_ms ≤ PIN` (L-C.10), `arm == "base"` holding all of them and `arm == "scored"` those the same predicate
  keeps at their own entry close; key `(arm, symbol, entry_close_ms)`; counts and a pointer only, no statistic (O-9;
  L-X.14).
The statistic is kept-versus-all (L-X.5). The gate builder `scripts/tierc12_stage_r_dir.py` is a DECISION module
(L-0.22: no exemption): it imports no door and nothing of `analytics.value_area`, reads value-area facts only as filed
columns through the reader (L-R.2), and asserts the `4h_` block it files equal to the `entry` rows of
`T12/va/stamps/VA_STAMPS_v6.parquet`. Beside the regbook it files, in `stage_r/dir/`:
- `dir_book_keys.parquet`, key `[book, symbol, entry_ms]`, `book == "P-DIR-1__scored"`: one row per kept campaign of
  the extended ride, with its `segment` (L-C.4) — the kept book as a key SUBSET of the `v6` stamp table, asserted ⊆
  and never re-stamped (L-V.19);
- the gate row — the object `gate` of `stage_r/dir/build_manifest.json`, per window of L-C's rides: `n_base`,
  `n_refused`, `n_kept`, `n_refused_long`, `n_refused_short`, `n_assets_with_a_refusal`, and the printed counts of
  L-R.3 — counts only.

SOURCE: O-21, O-9; OD-14; L-X.5, L-X.14, L-X.24, L-X.25; L-C.4, L-C.10; `MR/LEANS.md:141-150` (L-1.5); L-0.13, L-0.22;
L-V.19.

RIVALS: re-ride the gated book as the row of record — a gate removes trades (contract :52); the re-ride is a
disclosure (L-R.5). Score to PIN — O-9. A strip for the kept book only — OD-14: the strip is for every arm.

FAILS-IF: F-BASE-IDENT [P-DIR-1] and F-REGBOOK [P-DIR-1] (L-X's helper legs, run by this stage's suite); F-DIR [a],
[d]; mutations: one refused campaign restored to a copy of `scored`; one kept row's `net_r` moved by one ulp; the
un-gated book offered as `scored`; a key that is not a `v6` key added to a copy of `dir_book_keys`.

**L-R.5 THE RE-RIDE DISCLOSURE AND THE COUNTED RIVALS** — O-21 "a re-ride twin is Tier-E disclosure"

READING:
- **No re-ride arm.** The re-ride is a disclosure of COUNTS and DIFF ROWS — never an arm, never a book with an
  interval, a scorer leaf or a V5 stamp: one form for the three gates of the tier (L-G.18). The stage runs the refusal
  INSIDE the one v6 replay that takes a hook, `tierc12_books.replay_h(sym, lo_ms, hi_ms, *, refuse=None)` (L-C.4,
  L-G.18: a mirror of `replay9`'s candidate loop — the same armings, the same order, one position per asset, `ti <=
  open_until` → `position_open` — with one added site, TC11's `replay_g` law, `scripts/tierc11_stage_g.py:449-457`).
  `refuse(ctx) -> bool`, `ctx` carrying TC11's keys `sym`, `arm`, `ti`, `d`, `stp`, `atr`, `r_over_atr`; when it
  returns True the trigger does not take the slot. This section's hook is an ADAPTER to that signature: L-R.3's
  predicate fed the filed `va_bars_4h` row of `ctx["sym"]` whose `close_ms` equals the close of the candidate bar
  `ctx["ti"]` (HALT `DIR-ASOF` if no such row). With no hook, and under a hook that refuses nothing, the replay must
  reproduce the v6 book (`E.TP._book_sha` equal).
- **What is filed**, per window of L-C's rides (`scored`, `extended`): in `stage_r/dir/build_manifest.json` under
  `reride {…}`, printed in `stage_r/dir/STAGE_R_dir.md` — `rival_count_rejection_log` (the `position_open` rejections
  of v6's arming log whose blocking campaign the gate refuses), `reride_n`, `reride_admitted_not_in_v6`,
  `reride_v6_not_taken`, `n_reride_differs`; and the differing campaigns, row by row, in
  `stage_r/dir/dir_reride_diff.parquet`, key `[gate, window, symbol, entry_ms]` with `gate == "P-DIR-1"`, a
  placeholder row when none; its other columns are `diff_class` ∈ (`admitted_not_in_v6`, `v6_not_taken`, `none`),
  `direction` and the `4h_state` the hook read — no price, no R. The manifest also carries, for this mirrored ride,
  `ride_spec` (the control card and roles, by object) and `roles_name`, the objects L-0.30's TRAIL-OFFSET, ADDS and
  ENTRY-CROSS legs read.
- The as-of rival of L-R.2 (row k−1) and the position rival of L-R.3 are disclosed as COUNTS and key lists only —
  `n_refused_prior_bar`, `n_refused_both_readings`, `n_only_of_record`, `n_only_prior_bar` — with no mean, sum or
  interval: a rival reading is not given an outcome to be compared by.

SOURCE: O-21; L-G.18, L-C.4 (`replay_h`, one implementation); `tierc11_stage_g.py:449-457, :546-566`;
`tierc9.py:386-399`; `MR/LEANS.md:143, :147-148`; `XR/tierc11x/LEANS_X.md:2059-2064` (`n_reride_differs`, the filed
precedent of a count).

RIVALS: no re-ride at all — O-21 names it. A re-ride ARM with an interval — not taken: one form for the three gates,
the filed precedent is a count, and it is the reading with fewer looks. A re-ride book for each rival reading —
outcome tables for readings the row does not take. A second replay loop in this section — L-C.4's `replay_h` is the
one implementation.

FAILS-IF: F-DIR [f]: the replay under a refuse-nothing hook must reproduce the v6 book (`E.TP._book_sha` equal to
L-C's); mutation: a hook that marks a refused trigger `position_open` (the slot stays held) must be caught by the
leg's planted pair of adjacent triggers.

**L-R.6 THE LABEL** — "Label: direction informed by TC11 R5 (+0.49 with / −0.49 against, pivot states)" (contract :67)

READING: P-DIR-1 carries `selection_hazard`, tag `direction-informed` (O-23, O-30), and prints the template L-X.13
fixes for its registration id: `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)`. The two figures
the contract quotes are the cells `calibrated|4h|alignment|EXP_ALIGNED` and `calibrated|4h|alignment|EXP_COUNTER` of
`MR/stage_r/R5_CHOP_DIRECTION.parquet` (sha256
`a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`; rendered at
`MR/stage_r/R5_CHOP.md:120-121`): mean net R on file +0.491349 over 47 campaigns and
−0.493933 over 12, on this same v6 book and corridor, by PIVOT state. The label's `items` cite that file, the two
cells and their `n`. What is new in P-DIR-1 is the detector (the value area's ACCEPTED state, not the pivot machine's
expansion) and the interval; the direction of the refusal was chosen with R5 in view. By schema, no filed TC11 or X
parquet carries both a book-outcome column and a value-area column [verified at drafting: a name scan of every parquet
under `MR/` and `XR/tierc11x/`], so the value-area state has not been tabulated against v6 outcomes on file; the label
says so in those words and claims no more.
**The key overlap, printed directly under the cell — counts only, no outcome.** Whether "direction-informed" is a
sufficient label depends on how much of the refused set IS the cohort whose mean was already printed. The stage
therefore files, in `stage_r/dir/build_manifest.json` under `r5_overlap`, and the report prints under the cell:
`n_refused` and, of those, the number in TC11 R5's `EXP_COUNTER` cell and in its `EXP_ALIGNED` cell
(`n_refused_in_EXP_COUNTER`, `n_refused_in_EXP_ALIGNED`), with the two cells' own sizes (`n_EXP_COUNTER`,
`n_EXP_ALIGNED`). The pivot state at the entry instant is read from `MR/stage_r/NEST_v6.parquet` (through
`E.tc11_record`; rows `scale_kind == "calibrated"`, `instant_kind == "entry"`; columns `symbol`, `entry_ms`,
`direction`, `4h_state` and no other) and classed by a mirror of `align_of` (`scripts/tierc11_stage_r.py:1650-1661`:
`BULL_EXP` for a long or `BEAR_EXP` for a short → `EXP_ALIGNED`, the other expansion → `EXP_COUNTER`). The mirror's
two cell sizes are asserted equal to the `n` of the two filed cells. No mean, sum or interval of either overlap is
computed anywhere.

SOURCE: contract :67; O-23, O-30; L-X.13; the parquet and md as cited [read at drafting]; `tierc11_stage_r.py:1650-1661`
and the column names of `NEST_v6.parquet` [read at revision]; scout U6 §1.11.

RIVALS: `pre_seen` — the value-area gate's own cohort was never printed; the harsher label would assert a look that
did not happen, and O-23 and O-30 rule the key. The label with no overlap count — a reader of §0 could not tell a new
cohort from a re-read one (O-30: a label must be true).

FAILS-IF: F-REG (TEMPLATE leg, L-X; its plant `DIRECTION-INFORMED` in capitals on P-DIR-1 must be RED); F-DIR [g]:
(i) the two quoted cells re-read from the pinned parquet must equal the label's `items` at the file's precision; (ii)
the `r5_overlap` counts recounted by the fixture's own classing of `NEST_v6` and its own join to the refused keys,
and the two cell sizes equal to the filed cells' `n`; F-S0-FIVE (L-X) is RED when the overlap line is absent.
Mutations: one digit changed in a copy of the label text; the two sides of the `align_of` mirror swapped; the overlap
counted on the rows of the other `scale_kind`.

**L-R.7 F-DIR** — "F-DIR (3 refusals hand-verified)" (contract :118-119)

READING: suite `scripts/tierc12_stage_r_fixtures.py --stage=TC12-R.dir`, transcript
`T12/stage_r/dir/FIXTURES_STAGE_R_dir.txt` (one transcript per record, L-0.9); blocks `F-DIR [a]` … `F-DIR [g]`, one
`prove` call each (L-0.14). The suite imports the gate builder and the reader; it imports no door and not
`analytics.value_area` (L-0.22); `analytics.profile` is imported only as the independent referee of the hand
derivation. Leg [e] is SYNTHETIC; the others run on P-DIR-1's own tables — the row has no precondition, so no leg of
F-DIR can read CLOSED-NO-BOOK.
- [a] SET. The refused key set equals the fixture's own evaluation of L-R.3 from `va/va_bars_4h.parquet` opened by
  explicit path with the fixture's own linear-scan as-of (last close ≤ τ); kept ∪ refused = the base keys, kept ∩
  refused = ∅; every kept row equals its base row on the sixteen columns; the refused set equals the key set of the
  4h `ACCEPTED_AGAINST` cell of L-R.9's table; every key of `dir_book_keys` is a key of the `v6` stamp table.
- [b] HAND — three refusals and two kept witnesses, chosen by a rule frozen HERE, before any gated book exists, in
  ascending `(symbol, entry_ms)` order (L-0.14 G, categories first): **D1** the first refused long; **D2** the first
  refused short; **D3** the first other refused campaign whose deciding acceptance is printed at the entry bar itself
  (the acceptance event's `i == k`) — the as-of boundary case. **N1** the first KEPT campaign whose state is PROBING
  against its direction; **N2** the first KEPT campaign whose state at row k−1 is ACCEPTED against its direction and
  at row k is not (a decay on the entry bar). A category with no member prints `NONE-EXISTS <category>`, asserts from
  the population that its count is zero, and its slot is taken by the next unchosen campaign of its population
  (refused for D1-D3, kept for N1-N2) in key order, printed `FILL`. If the refused set holds fewer than three
  campaigns, EVERY refused campaign is hand-verified and the leg prints `ONLY <n> EXIST (contract count 3)` with `n`
  asserted equal to the gate row's `n_refused` (L-0.14 G); `n = 0` prints `EMPTY POPULATION` with the same assertion.
  The leg is GREEN in every such case; the shortfall is printed `FINDING: …` and carried to the report as a
  finding-not-fixed owned by the operator. No size or composition of the refused set makes the leg RED: only a
  mismatch between the fixture's derivation and production does. "Hand-verified" = the fixture's own derivation,
  sharing no code with the module, the doors, the reader or the gate: from the raw 4h tape by explicit path,
  `VA(t−1)` by `analytics.profile.volume_profile` on the raw slice, ATR by its own Wilder loop, the V2 clauses written
  out per bar from the start of the value regime that the deciding probe opened in, through the acceptance, through
  every bar to the entry bar (each bar's decay test printed) — yielding the state after the entry bar, compared with
  the filed state and with the gate's decision.
- [c] AS-OF. For every base campaign, the gate's production predicate fed the FILED `va_bars_4h` cut at τ
  (`bars("4h", asof_close_ms=τ)`) returns the decision of record, and the last row of that cut has `close_ms ==
  entry_close_ms`; leans on F-VA-ASOF [d]. The transcript carries the fixed line `leans on F-VA-ASOF [d]: a filed row
  at bar k equals a door rebuild on tapes cut at close_k`. No leg of this suite re-runs a door.
- [d] UN-GATED. The un-gated book offered as `scored` must FAIL [a] whenever the refused set is non-empty; if the
  predicate refuses nothing the leg prints `REFUSES-NOTHING` and the scorer's TWO-SAMPLE-PREMISE flag stands (L-X.7).
- [e] TRUTH TABLE (synthetic). On a synthetic `va_bars_4h` frame and synthetic campaigns typed by the fixture —
  every (direction × state) pair, an acceptance printed on the entry bar, a decay on the entry bar, both sides
  disarmed — the PRODUCTION predicate function returns the fixture's typed answers.
- [f] L-R.5's identity leg. [g] L-R.6's label and overlap leg.
- FAILS IF: any set, row, state, hand derivation, count or typed answer differs. PLANTS, each inside the production
  predicate or on a copy, each caught by its named leg: the state read at row k+1 → [c], [e]; at row k−1 → [e], and
  [b] on D3 / N2 where they exist; the sides swapped → [a], [b], [e]; PROBING counted as ACCEPTED → [e], and [b] on
  N1; the un-gated book → [d]; a refused campaign restored → [a]; a key outside `v6` in `dir_book_keys` → [a]; a
  state re-derived from filed levels instead of read (L-V.24's round trap) → [e] on a typed exact-edge case.

SOURCE: contract :118-119; L-0.14 (the hand-sample law, the leg law, production against production); L-V.24; X's
F-SFP selection rule (`XR/tierc11x/LEANS_X.md:2309`: "chosen by a frozen rule, never after a look").

RIVALS: three refusals drawn at random — categories exist, so L-0.14 orders the first of each. The reader's stamp as
the hand referee — self-comparison. A door re-run on a cut tape from this suite — forbidden: no suite outside Stage V
imports or spawns a door (O-29, L-0.22); Stage V's F-VA-ASOF [d] owns prefix identity.

FAILS-IF: as stated in the reading.

**L-R.8 THE FULL VA CHOP TABLE** — "Tier-E: the full VA chop table — v6 by 4h and 1d VA state × %-of-value decile at
entry" (contract :67-68)

READING: `T12/stage_r/dir/VA_CHOP.parquet`, a GRID (L-0.15; declared key `[cell]`), the value-area form of TC11's R5
(`MR/LEANS.md:284-289`), built by `tierc12_stage_r_dir.py` and printed WHOLE in the stage document
`stage_r/dir/STAGE_R_dir.md` (the report carries one pointer row for it: path, sha, cell count — L-X.28).
- **Population**: the base v6 campaigns of the scored window; strip campaigns are listed apart with their states and
  no statistic.
- **Instant**: τ = `entry_close_ms` (L-R.2), for both lenses: each lens's row is `k_ℓ = asof_index(close_ms_ℓ, τ)` of
  the filed `va_bars_<ℓ>` through the reader's `bars(ℓ)` — at 4h the entry bar's own row, at 1d the last 1d bar closed
  at or before τ (`1d_stale_ms = τ − close_ms_1d[k]`).
- **AXES**, declared in this order: `lens` ∈ (`4h`, `1d`) × `state` ∈ `STATE_NAMES` (six, L-V.2) × `band` (the
  %-of-value bands below). The cell count is the product of the three cardinalities, computed; the grid partitions
  the population once per lens (Σ n over a lens's cells == the base's row count).
- **The %-of-value read**: the row's filed `pct` — bar k's own judged column (the lens's last close against
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
  (`would_read_ci_only = "no interval"`, L-0.16, L-0.28). Every row carries `l_label` (the lookback is tuning-fit:
  in-sample for tuning-era VA bars).
- **Beside**: `VA_CHOP_ROWS.parquet`, one row per campaign (key `[symbol, entry_ms]`): direction, `net_r`, era,
  `refused`, both lenses' `state`, `pct`, `band`, `alignment` (L-R.9), `bar_close_ms`, `stale_ms`, `L`, `l_label`,
  the 4h columns of L-R.3, and the live twin `1d_px_pct` = the entry price against the 1d profile in force at `k`
  (the row's `val`, `vah`; L-V.20's live formula — a price against filed levels, never a state);
  `VA_CHOP_MARGINS.parquet` (declared key `[cell]`; per lens: by state; by band); the count of campaigns whose `pct`
  sits exactly on a band edge, per lens (R5's SR-16 disclosure).

SOURCE: contract :67-68; `MR/LEANS.md:284-289` (L-R.7); `tierc11_stage_r.py:168-171, :1470-1477, :1535-1544,
:1601-1636`; L-V.9, L-V.16, L-V.20, L-V.24; L-0.15, L-0.16; L-X.28 (the whole-versus-pointed map).

RIVALS: quantile bands fitted on the sample (or on outcomes) — the contract says "decile" of %-of-value, and a fitted
cut is a degree of freedom. R5's half-open top (`>=100`) — moves a close exactly at VAH out of value against L-V.9.
The live entry price against the in-force 1d profile as the 1d read — state and band would stop being coherent
(L-V.20); printed per campaign instead. A 12h or 1w block — the contract names 4h and 1d.

FAILS-IF: F-GRID [VA_CHOP] (declared cells, partition per lens, n = 0 rows present); F-CHOP: every cell's `n`,
`mean_net_r`, `sum_net_r` and every margin recomputed by the fixture from `VA_CHOP_ROWS` and the base arm; a planted
campaign with `pct` exactly `PCT` must land in the top decile; mutations: bands taken as sample quantiles; the top
band half-open; one `n = 0` row dropped.

**L-R.9 WITH-VS-AGAINST ACCEPTANCE** — "with-vs-against acceptance" (contract :68); "§0 … the VA chop table
(with-vs-against)" (:127)

READING: `T12/stage_r/dir/VA_CHOP_ALIGNMENT.parquet`, a GRID (declared key `[cell]`): `lens` ∈ (`4h`, `1d`) ×
`alignment` ∈ (`ACCEPTED_WITH`, `ACCEPTED_AGAINST`, `PROBING_WITH`, `PROBING_AGAINST`, `INSIDE`, `UNDEFINED`), same
population, instant and columns as L-R.8. WITH = the state's side is the trade's direction: ACCEPTED_ABOVE /
PROBING_ABOVE for a long, ACCEPTED_BELOW / PROBING_BELOW for a short; AGAINST = the other side (the value-area form
of `align_of`, `tierc11_stage_r.py:1650-1661`). It partitions the population per lens. The 4h `ACCEPTED_AGAINST` cell
IS P-DIR-1's refused cohort: its key set is asserted equal to the refused set. This table is printed WHOLE in the
report's §0.2 (L-X.28) and in `STAGE_R_dir.md`, collared, with TC11's two R5 cells printed beside as the pivot-state
anchor (quoted from the pinned parquet, L-R.6).

SOURCE: contract :68, :127; `tierc11_stage_r.py:175, :1650-1661, :1687-1717`; L-X.28.

RIVALS: R5's direction-adjusted %-of-range thirds — not asked for the value area; it would add cells with no phrase
behind them.

FAILS-IF: F-GRID [VA_CHOP_ALIGNMENT]; F-DIR [a] (the refused set == the 4h AGAINST cell); mutation: a refused key
moved to `INSIDE` in a copy of the rows table.

---------------------------------------------------------------------------------------------------------------
#### B · P-SFP-VA-1 — the swing failure as a range trade, 4h

The trade's machinery is X2's (`XR/scripts/tc11x_sfp.py`), MIRRORED into `scripts/tierc12_rangewalk.py` (pure: numpy
and the exact tick grid only; it holds `geometry`, `bar_step`, the walk and `fee_per_fraction`, and is the ONE
implementation of each — `scripts/tierc12_scalp.py` imports `fee_per_fraction` from it) and held equal to X's FILED
trades by F-SFP-MIRROR (L-R.25); no `tc11x_*` module is imported (O-4). The mirror carries two declared switches so
that X's own laws stay provable on X's rows while the tier's laws are the record: `geometry(…, law)` (L-R.14) and
`bar_step(…, gap_law)` (L-R.19). `lf` = `E.BK.frame_l(stem, "4h")` — the lens frame of `E.D.load_asof(stem, "4h")`,
the same tape DOOR 1 reads (`scripts/tierc10_brk.py:920-954`; its `atr` is `ind.atr(h, l, c, ATR_LEN)`). The builder
`scripts/tierc12_stage_r_sfp.py` is a DECISION module (L-0.22): every value-area fact it uses is a filed row read
through the reader.

**L-R.10 THE EVENT** — "a SWING FAILURE (V2) at VAH or VAL" (contract :70); "both directions; five home assets"
(:69-70)

READING: One event = one row of `T12/va/va_events.parquet` (L-V.14), read through the reader's `events(lens="4h",
kind="swing_failure")`, with `asset` in the home panel (`E.CLASSIC5`) — V2's machine as L-V.9-L-V.13 fix it (the
contract's K at :36, the frozen edge, each close judged against `VA(t−1)`). Both sides trade: `side == "top"` (a
failure at VAH) and `side == "bottom"` (at VAL). The event is known at `known_close_ms`, the close of its return bar
`i`. Fields read: `lens`, `asset`, `kind`, `side`, `t0`, `i`, `bars_out`, `E`, `extreme`, `sgn`, `val_f`, `poc_f`,
`vah_f`, `close_i`, `atr_i`, `known_close_ms`, `era`, `in_strip`, `ret_inside_frozen`, `ret_inside_rolling`,
`from_state`, and — for one printed count only (L-R.12) — `val_n`, `poc_n`, `vah_n`. No further filter: neither
return flag is required and no `from_state` is excluded — an event whose close lies outside the frozen value area
fails the geometry law of L-R.14 by itself (a target is then not ahead of the entry), and adding a flag test would be
a second, unwritten condition. Counts by flag and by `from_state` are printed. A LAPSE (`bars_out > K`) and an
acceptance feed no trade. The builder asserts, per event, `lf.open_ms[i] + lf.step_ms == known_close_ms`,
`Round6(lf.c[i]) == close_i` and `Round6(lf.atr[i]) == atr_i`, else HALT `SFP-FRAME`; and that no two swing-failure
rows of one (lens, asset) share a return bar `i`, else HALT `SFP-EVENT-KEY` (the event table's key is `[lens, book,
asset, entry_ms]`, L-R.31).

SOURCE: contract :36, :69-70; L-V.9, L-V.11, L-V.14, L-V.24; O-16, O-29.

RIVALS: X's record event (return within 7) — the contract's V2 replaces it. The wick-only swing failure (X's twin) —
not a V2 event. Require `ret_inside_frozen` — see above. A warm-up floor beyond the machine's own (`t0 − 1 ≥ L − 1`)
— no phrase behind it.

FAILS-IF: F-SFP [b] (every traded or refused row maps to exactly one V2 swing-failure row, and every such row inside
the window is accounted for: traded, one-position, geometry, rr-min); mutation: lapse rows admitted as events.

**L-R.11 ENTRY AND DIRECTION** — "enter at the close back inside, toward the POC" (contract :70)

READING: `entry_i = i`; `entry_px = e = lf.c[i]`, a taker market fill at the return bar's close; `entry_ms =
lf.open_ms[i]`, `entry_close_ms = known_close_ms` (the lineage's key convention); the path starts at bar `i + 1`.
Direction `d = sgn` of the event: a failure at VAH is SHORT (−1), at VAL LONG (+1) — the fade of the failed edge,
toward value. "Toward the POC" is a property the geometry must have, not a second way to set the sign: if the POC is
not ahead of the entry in direction `d` the trade is REFUSED (L-R.14, `poc_not_ahead`), never reversed.

SOURCE: contract :70; L-V.11 ("its sign points toward value (top → −1, bottom → +1)"); `XR/tierc11x/LEANS_X.md:1133-
1137` (LX-X2.2); `tc11x_sfp.py:490`.

RIVALS: `d = sign(POC − entry)` — turns a close that overshot the POC into a trade AWAY from the failed edge, a
different trade; X refuses those (LX-X2.6). Entry at the next bar's open — the contract says "at the close".

FAILS-IF: F-SFP [a], [b]; mutation: the direction taken as `sign(poc_f − e)`.

**L-R.12 THE PROFILE OF THE TRADE; TARGET 1; TARGET 2** — "TARGET 1 = POC (half off); TARGET 2 = far edge − 0.25
ATR_4h (remainder)" (contract :71-72)

READING: The profile of the trade is the one whose edge was probed: `VA(t0−1)`, FROZEN — the event row's `val_f`,
`poc_f`, `vah_f` (L-V.14). All three levels are the filed values (L-V.24) and never move after entry.
- `T1 = poc_f`. Half the position exits there. "Half" is `Q` = the card's harvest fraction
  (`E.TP.CONTROL_CARD.harvest_frac`), the object `E.BK.account_l` books with; the contract's word "half" (:71) is
  asserted equal to it by the pin door (pin `sfp.t1_fraction`, L-R.32).
- `far` = `val_f` for a short, `vah_f` for a long. `T2 = far − d·a·A`, with `a` = the contract's "0.25" (:72, pin
  `sfp.t2_offset_atr`) and `A = lf.atr[i]` — ATR_4h of the return bar, known at the entry close. The offset is toward
  the inside of value. The remainder (the other fraction, or the whole position if T1 is void or has not filled)
  exits at T2.
- T1 and T2 are touch-triggered TAKER exits booked at their level (L-R.19, L-R.20): no resting maker order is
  assumed on the record, and no gap improvement is booked.
- Printed per event: `t1_r = d·(T1 − e)/R`, `t2_r = d·(T2 − e)/R`, `r_atr = R/A`, with their distributions.

SOURCE: contract :71-72; OD-9; L-V.14 (`*_f` = "the FROZEN profile VA(t0−1) — the profile whose edge was probed"); X's
precedent `LEANS_X.md:1158-1184` (LX-X2.4: T1 on the range "the deviation swept", frozen at entry) and :1186-1196
(LX-X2.5); `tc11x_sfp.py:122, :497-502`; scout U2 R20.

RIVALS: the profile in force at entry, `VA(i)` (`*_n`) — its window contains the probe's own bars, so the excursion
being faded has already moved its POC and edges; not taken. Disclosed as a COUNT: events whose disposition (admitted
/ geometry / rr-min) differs under `VA(i)`. The judging profile `VA(i−1)` — neither the probed profile nor the one
in force. Targets re-read each bar — a level set from a bar's own profile or ATR can know that bar's range
(`LEANS_X.md:1194-1196`). Targets as resting maker limits on the record — the toll of record is taker on every leg
(L-R.20); the maker reading is the twin (L-R.24).

FAILS-IF: F-SFP [a], [b] (`T1 == poc_f`; `T2 == far − d·a·A` on every row); F-SFP-ASOF; mutations: T1 from `poc_n`;
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

FAILS-IF: F-SFP [a], [b] (`ext ==` the raw extreme over `[t0, i]`; `R ≥ RAIL·A` on every row); F-TYPED-FLOW
[sfp.rail_atr] (bent at its door, it must move `r_dist` of the first rail-bound row); mutations: the rail dropped;
`ext` over `[t0, i−1]`.

**L-R.14 DEGENERATE GEOMETRY — OD-8** — "toward the POC" (contract :70); "or the trade is skipped ["rr-min"]" (:73-74)

READING: One geometry law for both range rows of the tier (OD-8; L-S.11 carries the same law in integer ticks). With
`e` the entry price (here `lf.c[i]`, the return bar's close), `d` the direction, `T1`, `T2` the targets and `R` the
stop distance after the rail:
1. An event is **REFUSED and counted**, after the one-position test and BEFORE the reward test, with the first reason
   that holds: (1) `stop_none` — the stop function returns none (L-R.13); (2) `poc_not_ahead` — `d·(T1 − e) ≤ 0` (the
   contract's "toward the POC" has no object; never reversed); (3) `t2_not_ahead` — `d·(T2 − e) ≤ 0`. These three
   hold in EVERY book, the unfiltered twin included: an order whose target is not ahead is not an order.
2. **Not refusals.** `t1_within_fee_band` := `0 < d·(T1 − e) ≤ (G / BPS_PER_UNIT)·e`, `G = E.R2.FEE_BPS_ROUND_TRIP` —
   the trade is taken as written, the flag is filed and counted, and `fee_band_r = (G / BPS_PER_UNIT)·e / R` is
   printed. `t1_void` := `d·(T2 − T1) ≤ 0` — no T1 order exists and the WHOLE position exits at T2; filed and
   counted. There is no fee band and no inverted-targets refusal: the contract's only skip is "rr-min" (L-R.15).
3. **X's geometry law** (the 10-bps band refusals `t1_within_10bps`, `t2_within_10bps` and `targets_inverted`;
   `XR/scripts/tc11x_sfp.py:503-513`) is kept behind a declared switch — `tierc12_rangewalk.geometry(…, law)`, `law ∈
   {"tc12", "x"}` — whose `"x"` value has exactly two call sites (AST-typed): F-SFP-MIRROR on X's filed rows, and the
   Tier-E arm `tierE__x_geometry` of P-SFP-VA-1 (TC12's law everywhere else; its own one-position sequence; the rows
   that differ from the record listed; L-R.24). Under `"x"` the threshold is `(G / BPS_PER_UNIT)·e`, the same on every
   row, with `G` asserted equal to X's `REFUSAL_BPS` (`tc11x_sfp.py:123`, read as an AST literal).
The row files the first reason and `reasons_all`. The reason slugs of record, in `SFP_EVENTS.disposition`: `stop_none`,
`poc_not_ahead`, `t2_not_ahead`, `rr_min`, the sequencing reason `one_position`, and `traded`.

SOURCE: contract :70, :73-74; OD-8; `LEANS_X.md:1198-1224` (LX-X2.6) and `tc11x_sfp.py:123, :483-513` (X's law, kept
for the mirror and the twin); `scripts/tierc2_rules.py:122-123` (`FEE_BPS_ROUND_TRIP`); L-S.11 (the same law in
ticks); L-0.17 (`BPS_PER_UNIT`).

RIVALS: X's fee-band and inverted-targets refusals — not taken on the record (OD-8: the contract's only skip is
rr-min); printed as `tierE__x_geometry`. T1-collapse on a POC behind the entry (the whole position rides to T2; X's
twin) — not taken: "toward the POC" then has no object, the event is refused and no book is built on it. Reversing
the trade — L-R.11.

FAILS-IF: F-SFP [b] (every refused row meets a clause and carries the first that holds; every admitted row meets
none; every `t1_void` row has no T1 fill; no row of a book other than `tierE__x_geometry` carries a disposition named
for the fee band or for inverted targets) and [g] (the synthetic events: the POC at the entry; the POC behind it; the
POC inside the band; the POC beyond T2; T2 at the entry); F-SFP-MIRROR [SWITCH] (the two typed call sites of `"x"`,
L-R.25); mutations: a planted event with the POC behind the entry admitted; a `t1_void` event refused; a planted event
at the band's edge refused (X's law left on the record).

**L-R.15 "rr-min" AND THE UNFILTERED TWIN** — "Minimum reward at T2 ≥ 1.5 × stop distance or the trade is skipped
["rr-min"]; the unfiltered twin printed" (contract :73-74)

READING: After the geometry law, with `R` the stop distance AFTER the rail (L-R.13) and everything measured from the
entry price: `rr = d·(T2 − e) / R`. The event is SKIPPED and counted (`rr_min`) iff `rr < RR`; it trades iff `rr ≥
RR`. `RR` = the contract's "1.5" (:73; also :100 and :135-136 `"rr-min" (1.5 at T2)`; pin `rr_min` — ONE pin for both
range rows of the tier — veto "rr-min"). A skipped event does not occupy the asset's slot.
Order of tests per event, in bar order per asset: (1) one position (L-R.18) → (2) geometry (L-R.14) → (3) rr-min →
(4) the walk. The first test that fails names the row's disposition (`one_position`; `stop_none`, `poc_not_ahead` or
`t2_not_ahead`; `rr_min`; else `traded`).
**The unfiltered twin** `tierE__unfiltered` is the same book without step (3) and with nothing else changed — the
three geometry refusals stand in it — RE-WALKED with its own one-position sequence (X's law for ridden twins,
`tc11x_sfp.py:167-168`): a trade the record skipped can hold the slot and block a trade the record took, so the twin
is a different trade set, not a superset. Printed with it: rows in both books; rows only in the twin (skipped by the
record); record rows the twin displaced.

SOURCE: contract :73-74, :100, :135-136; OD-8; `tc11x_sfp.py:167-168, :892-945` (the order: one position, then
geometry); L-0.17, L-0.23 (the one pin and its veto).

RIVALS: `R` before the rail (the pivot distance) — the contract says "stop distance", and the stop is the railed
one. The reward measured from T1, or as the fraction-weighted blend — the contract says "at T2". The twin as a
filter of the record's rows — it would hide the slot effect. The twin also dropping the geometry refusals — an order
whose target is not ahead is not an order in any book.

FAILS-IF: F-SFP [b] (`rr ≥ RR` on every record row; every `rr_min` row has `rr < RR`); F-TYPED-FLOW [rr_min] (bent at
its door, the disposition of the event nearest the cut moves); mutations: `R` taken as the pivot distance on a
rail-bound event; the test applied to T1.

**L-R.16 THE TIME STOP** — "TIME STOP = the 4h traverse (V4)" (contract :72)

READING: `T` = the fitted pin `traverse.4h`, read through the reader's `tierc12_va_stamps.traverse("traverse.4h")` —
the fitted-pin door (L-V.2, L-V.18; O-18): it HALTs unless `T12/va/TRAVERSE.json` carries its certified sha, and
returns `(value, source)`, `value` = the integer at `by_lens.4h.T_of_record`, a number of 4h bars fitted on the tuning
era and frozen before any range book exists. T of record uses the regime reading (L-V.18); the contract's phrase read
strictly (every bar of the leg INSIDE) is a twin printed per lens in Stage V and enters no book (OD-15). The position
still open at the CLOSE of bar `tend = entry_i + T` exits there: `exit_px = lf.c[tend]`, `exit_reason = "time_stop"`,
a taker leg. Every trade row files `T`, `time_stop_i` and `t_label` = "T tuning-fit (regime reading; the strict-INSIDE
twin is printed in Stage V)"; the book's manifest files `time_stop_source = {path, key, sha256, value}` exactly as the
door returned it. The row's disclosure line adds "in-sample for tuning-era trades" (L-R.23).

SOURCE: contract :42-43, :72; O-18; OD-15; L-V.2, L-V.18; `LEANS_X.md:1238-1239` (LX-X2.7: "exits the position still
open at the CLOSE of bar `entry_i + T`"); `scripts/tierc7.py:209-211` (the lineage's shadow clock); `tc11x_sfp.py:657,
:738-740`.

RIVALS: the clock started at `t0` — the trade starts at the entry. Exit at the open of `tend + 1` — X's and the
lineage's clock exits at the close. A typed integer — F-TRAV. The strict-INSIDE traverse as T of record — OD-15: it is
printed, not booked. A second reader of `TRAVERSE.json` in the builder — the reader's `traverse` is the one door.

FAILS-IF: F-TRAV [a · tierc12_stage_r_sfp] and [a · tierc12_rangewalk] (no integer literal reaches a time-stop or
traverse name) and F-TRAV [e · <book>] for every ridden arm (every row's `T` == the door's value) — L-V's helper legs,
run by this stage's suite; F-SFP [a] T-TIME, [b] (`exit_i == entry_i + T` on every time-stop row); F-TYPED-FLOW
[traverse.4h] (bent by one bar at the door, the exit bar of the witness time-stop trade moves); mutation: the exit at
the close of `entry_i + T + 1`.

**L-R.17 INVALIDATION** — "INVALIDATION = acceptance beyond the faded edge" (contract :72-73)

READING: The faded edge is the side the swing failure failed at (VAH for a short, VAL for a long). The trade is
invalidated when the LENS becomes ACCEPTED beyond that side: the first `acceptance` row of the filed `va_events`
(read through the reader's `events(lens="4h", kind="acceptance")`) for the same asset and lens with `side ==` the
event's side and `entry_i < i_acc ≤ tend`. If the position is still open at the close of bar `i_acc`, it exits there:
`exit_px = lf.c[i_acc]`, `exit_reason = "invalidation"`, a taker leg. It exits whatever is still open (the whole
position, or the remainder after T1).
- It is a CLOSE event. Within bar `i_acc` the intrabar law of L-R.19 runs first: the stop at the open, the stop by
  range, T1, T2. Acceptance can print in a single bar (the one-close clause of contract :35, on the probe's first bar
  too), so on that bar the stop is tested BEFORE the invalidation: a bar that opens at or beyond the stop, or whose
  range reaches it, is a stop (L-R.19 steps 1-2), and the acceptance printed at its close does not act. Counted:
  `n_invalidation`; `n_acceptance_on_a_stop_bar`.
- On a close that is both the acceptance and the time stop the reason is `invalidation` (the price is the same).
- An acceptance on the OPPOSITE side (in the trade's favour) is not an exit.
- Decay, a lapse, a re-probe that fails and a re-roll of the value area are not exits.
- **Which edge was accepted through.** The acceptance is the LENS's, on an edge that may have re-rolled since the
  entry, while the trade's edge is frozen. Each invalidation row files `inval_event_E` (the acceptance row's frozen
  edge `E`) and `inval_edge_moved = (inval_event_E != edge_px)`, `edge_px` being the swing failure's own `E`, both
  filed values; printed: `n_invalidation` by `inval_edge_moved` and by the sign of `d·(exit_px − e)`. The reading
  itself is forced by O-29 (no trade-local acceptance test); the two columns let a reader tell "the faded edge was
  accepted through" from "value moved and the lens accepted beyond a new edge".

SOURCE: contract :35, :72-73; O-29; L-V.10, L-V.14 (acceptance rows; `i`, `side`, `E`); `LEANS_X.md:1292-1305` (close
events after the intrabar order); TC11 L-S.2 (`MR/LEANS.md:458-460`: invalidation exits "at that 1h close … taker";
"STOP → TARGET → invalidation at the close").

RIVALS: a trade-local acceptance — N closes beyond, or one close M·ATR beyond, the trade's own frozen `E`, counted
by the builder — not taken: it is a second state machine outside the module, forbidden by O-29; the contract names
the V2 state. Invalidation before the intrabar stop — a close event cannot precede the bar's range. Exit at the next
open — the acceptance is known at its close.

FAILS-IF: F-SFP [b] (every `invalidation` row has an acceptance row on the faded side at `exit_i` and carries its `E`
as `inval_event_E`; no record row holds an acceptance on the faded side at a bar `j` with `entry_i < j < exit_i`; and
none at `j == exit_i` unless the exit is `invalidation` or an intrabar exit of that bar) and [g] (a synthetic one-bar
acceptance whose range touches the stop must book a stop); mutations: the invalidation ignored; the invalidation
taken before the stop on the synthetic bar; the opposite side's acceptance treated as an exit; `inval_event_E` filled
from the trade's own edge.

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

FAILS-IF: F-SFP [c]: no two trades of an asset overlap under the law and the skipped count equals the events inside
open trades; mutations: an overlapping trade planted; an event planted on an exit bar admitted.

**L-R.19 THE BAR WALK — SAME-BAR ORDER AND FILLS** — "TARGET 1 … (half off); TARGET 2 … (remainder)" (contract
:71-72)

READING: The tier's one walk law (OD-9), on the 4h bars `j = entry_i + 1 … min(tend, hi)`, `hi` = the window's last
bar (L-R.21). Each bar is stepped once on what is still open, in this order (`S` the stop, `adv` / `fav` the bar's
adverse / favourable extreme):

| step | test | act |
|---|---|---|
| 1 · STOP at the open | `d·(o[j] − S) ≤ 0` | exit ALL at `o[j]` (the worse price); reason `stop`; `gap_stop = True` |
| 2 · STOP, adverse-first | `d·(adv − S) ≤ 0` | exit ALL at `S`; reason `stop`; `both_touch` counted if a target test holds on this bar; `stop_bar_open_through_target` counted if the bar opened at or beyond a resting target |
| 3 · T1 (resting, not void; never on a zero-volume bar) | P-SFP-VA-1: `d·(fav − T1) ≥ 0`; P-SCALP-3: the book's fill rule at `n_T1` | the T1 fraction exits at the LEVEL (`T1`; `px(n_T1)`); `gap_t1 = True` iff the bar opened at or beyond the level — no gap improvement is booked |
| 4 · T2 (never on a zero-volume bar) | likewise at T2 | the rest exits at the LEVEL, on the same bar as T1 if reached; `gap_t2` |
| 5 · close events | INVALIDATION, then TIME STOP, then CORRIDOR END | exit the rest at `c[j]` |

- There is NO open-decides-first step for a target; the stop is tested before any target on every bar.
- On P-SFP-VA-1 the targets are touch-triggered TAKER exits booked at their level; on P-SCALP-3 they are resting
  MAKER limits booked at their grid price (L-S.18). One law for both range rows.
- No T1 order exists on a `t1_void` trade (L-R.14): step 3 does not run and step 4 exits the whole position.
- The close events of this row: INVALIDATION (L-R.17), then the TIME STOP (L-R.16), then the CORRIDOR END — a trade
  with no exit by `hi` and `tend > hi` is marked at `lf.c[hi]`, `corridor_end`, listed OPEN (L-R.21).
- A zero-volume lens bar fills no target (L-D.16's no-trade rule, adopted); stops and close events act on it as on
  any bar; the count is printed (on file: none at 4h or 1d for the home assets).
- The record reads NO 5m bar: a 4h bar's internal order is decided by the law above, and `both_touch_bars`,
  `gap_stop`, `gap_t1`, `gap_t2`, `stop_bar_open_through_target` are filed per row so a reader sees how many trades
  rest on it.
- **X's record law** (the open decides first for stop and targets; a stop books the stop price through a gap; a
  target books `max(level, open)` long / `min` short; `tc11x_sfp.py:571-601`) is kept behind a declared switch —
  `tierc12_rangewalk.bar_step(…, gap_law)`, `gap_law ∈ {"tc12", "x_record"}` — whose `"x_record"` value has exactly
  two call sites (AST-typed): F-SFP-MIRROR against X's filed X2 rows, and the Tier-E arm `tierE__x_gaplaw` of
  P-SFP-VA-1 (its own one-position sequence; L-R.24).

SOURCE: OD-9; `tc11x_sfp.py:558-601` (`_hit`, `_fill`, `bar_step`), :649-752 (`walk`); `LEANS_X.md:1292-1315`
(LX-X2.10; :1308-1310, X on its own record law: it "favours the trader on both sides (targets collect the gap; the
stop ignores it)"); `scripts/tierc7.py:186-192`; L-S.18; L-D.16.

RIVALS: X's record law — not taken on the record (it favours the trader on both sides,
`x_rec/tierc11x/LEANS_X.md:1308-1310`); printed as `tierE__x_gaplaw`. Targets before the stop on an ambiguous bar —
flatters. An open-decides-first step for a target (X's symmetric-gap twin) — not taken: OD-9 tests the stop before
any target on every bar, the same law as the scalper's. 5m-child sequencing of ambiguous bars (X's twin) — not
carried: it would make the record's stage a 5m reader for a twin the contract does not name.

FAILS-IF: F-SFP [a], [g] (a synthetic bar set typed by the fixture: a gap through the stop, booked at the open; a gap
through T1 and through T2, each booked at its level; stop and target in one bar; a bar that opens beyond a target
and reaches the stop; T1 and T2 in one bar; acceptance and time stop on one close; a void T1; a zero-volume bar
touching a target); F-SFP-MIRROR (X's law, by the switch, on X's rows); mutations: a gap stop booked at the stop
price; a target credited at `max(level, open)`; target-before-stop on a both-touch bar; T1 credited on a stop bar.

**L-R.20 THE R-MULTIPLE WITH SPLIT TARGETS; FEES; FUNDING; THE COST TWINS** — "(half off) … (remainder)" (contract
:71-72); "taker and charter tiers unchanged" (:23)

READING: `acc = E.BK.account_l(lf, E.TP.CONTROL_CARD, d, R, leg)` with `leg = {entry_i, exit_i, exit_px, entry_px:
e, harvest}`; `harvest = None` if T1 never filled or is void, else the 3-tuple `(t1_i, t1_px, d·(t1_px − e)/R)` with
`t1_px = T1`, the level. With `q = card.harvest_frac`, `b = FEE_BPS_SIDE / 10 000` (the function's own lines,
`tierc10_brk.py:1270-1326`):
- T1 filled: `g = q·d·(t1_px − e) + (1 − q)·d·(exit_px − e)`; `fee = b·q·(e + t1_px) + b·(1 − q)·(e + exit_px)`;
  funding of the T1 fraction to the T1 bar and of the remainder to the exit bar; the fractions book the leg (asserted
  inside the function).
- T1 not filled: `g = d·(exit_px − e)`; `fee = b·(e + exit_px)`.
- `gross_r = acc["gross_r"]` (= g/R), `fee_r = acc["fee_r"]` (= fee/R).
- **Funding is NOT capped (OD-10).** `funding_r = acc["funding_r_uncapped"]`; `net_r = gross_r − fee_r − funding_r`;
  `taker_twin_net_r = gross_r − fee_all_taker_r − funding_r` (so L-X.24's identity `taker_twin_net_r == net_r + fee_r
  − fee_all_taker_r` holds exactly). The D12 ceiling (`card.funding_ceiling_r`, which `account_l` applies to its own
  `funding_r` and `net_r`) is a v6-card accounting rule and is not a rule of this trade. What the lineage's own
  booking would have been is filed beside: `tc_series_net_r = acc["net_r"]` and `funding_ceiling_bound =
  acc["funding_ceiling_bound"]`. "Taker twin == TC-series" is therefore held as: `|taker_twin_net_r −
  tc_series_net_r| ≤ HAIRCUT_TOL` on every row with `funding_ceiling_bound == False`, and `taker_twin_net_r <
  tc_series_net_r` on the others; the bound count per arm is printed. The same three assignments hold on the book of
  record, on the 1d cell and on every twin. `funding_r_uncapped` stays a filed column, asserted equal to `funding_r`
  on every row of a range arm.
- **The interval sum** is the lens frame's: every stamp with `open_ms[entry_i] < stamp ≤ open_ms[bar]`, priced at
  the close of the last lens bar closed at or before it, accumulated in ascending order (`funding_interval`,
  :1223-1267). A settlement at the entry-close instant is paid; one at a close-exit instant is not. Stamps strictly
  inside the entry bar are counted (`n_stamps_inside_entry_bar`) and asserted zero on 4h (HALT `SFP-FUND-INBAR`
  otherwise).
- **Toll of record: taker on every leg** — entry, T1, T2, stop, time stop, invalidation, the mark — the TC-series
  toll. Sidecar `toll = "taker"`; `fee_taker_r = fee_all_taker_r = fee_r`, `fee_maker_r = 0`, `taker_twin_net_r =
  net_r` (L-X.24).
- **Charter twin (TC11 AM-7)**: `haircut_net_r = net_r − fee_r × (slippage_bps_side / taker_bps_side)`, the two rates
  per stem from `E.fees()`; funding stays in.
- The lens frame, the card and `account_l` are called, never copied; production code holds no tolerance literal
  (`HAIRCUT_TOL` is the scorer's, read by `ast` with its node sha pinned, L-X.24; the equality of the per-fraction
  booking with `account_l` is a fixture leg).

SOURCE: OD-10; `tierc10_brk.py:1223-1326` (`account_l` returns `funding_r_uncapped` and `funding_ceiling_bound`,
:1322-1324 [re-read at revision]); `scripts/tierc5_rules.py:160-165` (the ceiling: "An ACCOUNTING rule, not a decision
rule"); `LEANS_X.md:1317-1353` (LX-X2.11); `MR/LEANS_AMENDMENTS.md:86-96` (AM-7); `tc11x_sfp.py:766-803`; L-X.24.

RIVALS: the capped figure as the net of record — a one-sided cap written for multi-week v6 campaigns removes a real
cost and never a credit; the contract gives this trade no ceiling. `T7._account_chain` — 4h-only by construction but
bound to the v6 frame memo; `account_l` is the lens function X rode. Slippage in the toll of record — Q3 stays open
(L-0.29); the twin is printed beside.

FAILS-IF: F-SFP [f]: `net_r == gross_r − fee_r − funding_r` with `funding_r == acc["funding_r_uncapped"]`; the
two-case identity of `taker_twin_net_r` against `tc_series_net_r` (within `HAIRCUT_TOL` where the ceiling is not
bound, strictly below where it is); the fixture's own per-fraction booking at all-taker bps equals `account_l` within
X's filed tolerance (`LEANS_X.md:1340`); the haircut law; the fee columns' identities; `n_stamps_inside_entry_bar ==
0` on every 4h row; mutations: maker bps left on one leg of the taker book; the T1 fraction funded to the exit bar;
`funding_r` taken from `acc["funding_r"]` (the capped figure) on a planted bound row.

**L-R.21 THE SCORED WINDOW, THE STRIP, ERA** — "(vs zero; full corridor; …)" (contract :69); O-9

READING:
- **Scored window.** The book of record holds the trades whose entry bar closes at or before W (`entry_close_ms ≤
  W`). It is ridden with `hi = hi_W`, the last 4h bar closing `≤ W`: the walk, the one-position sequence and the marks
  are those of the tape cut at W. A trade not exited by `hi_W` (`tend > hi_W`) is marked at `lf.c[hi_W]` with
  `exit_reason = "corridor_end"` (so `exit_close_ms ≤ W` on every row), stays in the scored book and is listed OPEN
  (`n_open_at_w` per asset) — X's LX-X2.17, the lineage mark. An unfilled T1 stays unfilled; a filled T1 keeps its
  fill.
- **Era.** "Full corridor" = every era inside the scored window (sidecar `era_scope = "full"`). Era of a trade =
  `E.era_of(entry_close_ms)`: `tuning` iff `entry_close_ms ≤ ERA_CUT`, else `holdout`. The tuning and holdout slices
  are the scorer's Tier-E leaves (L-X.14).
- **Strip — for every ridden arm (OD-14).** A second ride with `hi = hi_PIN`, the last bar closing `≤ PIN`, over
  every event to PIN, for EVERY ridden arm of this regbook: `scored`, `tierE__unfiltered`, `tierE__cell_1d` (on its
  own 1d clock), `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__x_geometry`, `tierE__x_gaplaw`
  (`tierE__maker_assumed` is the same walk as `scored` and shares its parent's rows). Each ride's rows with `W <
  entry_close_ms ≤ PIN` go to ONE file, `regbooks/P-SFP-VA-1/strip.parquet`, under the column `arm` (key `(arm,
  symbol, entry_close_ms)`; its sidecar carries `n_by_arm`, with `tierE__maker_assumed` listed `same_rows_as:
  "scored"`): ridden, printed beside, never scored, never pooled — a count and a pointer are the only aggregates.
- **Prefix identity of the two rides**, per ridden arm: every row of the ride to PIN resolved at or before W equals
  its scored-window row on every column; an OPEN-at-W row is compared on entry, stop, R, T1 and T2 levels, and on its
  T1 fill (`t1_i`, `t1_px`) iff the fill happened at or before `hi_W` — else the scored row's T1 must be unfilled. The
  true continuation of an OPEN-at-W trade is listed on its row of `SFP_EVENTS` (`continued_past_w = True`, with the
  ride-to-PIN exit bar, reason and price and `continued_net_r`): printed beside, in no arm, in no statistic.
- Stamped: the scored-window arms with the score edge; the strip, `SFP_EVENTS` and every table that reads past W with
  the pin (L-0.13).

SOURCE: contract :69; O-9; OD-14; L-X.24 (the scored-window laws on `scored` and `strip`); `LEANS_X.md:1550-1577`
(LX-X2.17); `tc11x_sfp.py:743-747`.

RIVALS: refuse an event whose `tend` passes W — selects on the corridor's end, which no trader has at the entry
(X's rejected rival). Score the strip — O-9. Holdout of record — the contract says "full corridor". A strip for the
book of record only — OD-14: O-9 names every arm.

FAILS-IF: F-SFP [d], per ridden arm: the scored-window arm equals the full ride's rows with `entry_close_ms ≤ W`,
OPEN-at-W rows compared on entry, stop, R, T1 and T2 levels; and on `t1_i`, `t1_px` iff the full ride's `t1_i ≤
hi_W`, else the scored row's T1 must be unfilled; every `strip` row of the arm has `W < entry_close_ms ≤ PIN`; [b]
OPEN leg: every OPEN row has `exit_i == hi_W` and `entry_i + T > hi_W`. Plants and mutations: a scored OPEN row
carrying a T1 fill at a bar after `hi_W` → RED; a trade with `entry_i + T ≤ hi_W` marked OPEN; a strip row placed in
`scored`; one ridden arm's rows missing from `strip.parquet`.

**L-R.22 THE PRECONDITION — THE LICENCE** — "the Q-R3 law licenses exactly {VA-4h taker, VA-1d taker, VA-1h
maker}; nothing else may trade a range" (contract :40-41); O-17

READING: Evaluated BEFORE any arm is built, from `T12/va/VA_MIRROR.json` (L-V.17; its sha asserted through
`certified()`, record `TC12-V`), which quotes X's `XR/tierc11x/va/feasibility.parquet` (sha256
`ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`) and computes nothing. The builder reads it only
through the reader's `licence("4h", "taker", "ALL")`, which HALTs for a pair outside `licence_set` and logs the read
(the log is filed as `licence_reads` in `stage_r/sfp/READ_SET.json`; L-0.30's LICENCE leg reads it). Two items, both
required:
1. the licence row of the row's OWN scoring era (O-17): P-SFP-VA-1 is scored on the full corridor, so the era row
   is `ALL` — selector `licence["4h|taker"].by_era["ALL"].would_read`, required `"PASS"`;
2. the pair is in the licence set: selector `licence_set`, required to contain `"4h|taker"` — the contract's word of
   record (:39, the holdout row). Stage V HALTs on a mirror disagreement and the reader HALTs on a pair outside the
   set, so this item cannot fail on a tier that reached Stage R; it is listed so the scorer re-evaluates it from the
   record.
If either is not met the stage writes `regbooks/P-SFP-VA-1/STATUS.json` (through `tierc12_regbook.write_status`) with
`status = "CLOSED_BY_PRECONDITION"`, `arms = []` and, per item, `{record, certified_by, selector, required, found,
met}`; it builds no arm, no event table and no twin; and the row reads `CLOSED BY PRECONDITION
(research_outputs/tierc12/va/VA_MIRROR.json#<selector> reads <found>; required <required>) — no number · no test
spent` (L-X.10), `<required>` being `PASS` for item 1 and `contains 4h|taker` for item 2. In that case the sub-stage
still files `scripts/tierc12_rangewalk.py` with F-SFP-MIRROR and the synthetic legs GREEN (Stage S imports it), and
every real-book leg prints `CLOSED-NO-BOOK P-SFP-VA-1` (L-R.25). The report prints beside the cell, from the same
record, the three era words of the pair (`ALL`, `tuning`, `holdout`; on file all three read PASS for 4h taker) and the
sentence of O-16 (d): the licence was earned on X's record machine, the outer fifth of value and an H20 exit, not on
V2 or on this trade (DISCLOSURES D-2). No arm's collared sidecar carries a licence word.

SOURCE: contract :39-41; O-17, O-16 (d), O-29; L-V.2 (`licence`), L-V.17 items 7-9; L-X.10, L-X.24 (STATUS);
`MR/regbooks/P-SCALP-2/STATUS.json` (the filed form); scout U2 §1.8 (the pooled grid).

RIVALS: the holdout row alone — O-17 rules the row of the scoring era. Recompute the licence under V2 — a different
object (L-V.17). Build the book of a closed row and print it collared (X's departure) — O-22 rules STATUS only. The
builder opening `VA_MIRROR.json` itself — the reader's `licence` is the one door and the one log.

FAILS-IF: F-FAM [PLANTED] (L-X); F-SFP [h] (synthetic): the PRODUCTION precondition function, fed a copy of the filed
licence leaf whose `would_read` is flipped, under the fixture's `--root`, must write STATUS only and no arm; F-NOT
LICENCE (L-0.30: `stage_r/sfp/READ_SET.json` holds a `licence_reads` entry for the pair); mutation: a builder that
reads the `holdout` leaf for item 1.

**L-R.23 LABELS AND DISCLOSURES** — O-23, O-30; "§0 VERDICTS FIRST: the five rows with their labels" (contract
:126-127)

READING: P-SFP-VA-1 carries `pre_seen` with the tag KIN-SEEN (O-30) and prints L-X.13's KIN-SEEN template; its
`pre_seen.text` below is printed under the cell with D-2 and D-3 and is not a clause of the cell. The cell is
`<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)`: this
trade form was never scored, so the row is not a re-score. `pre_seen.text`: "TC11-X's X3 printed value-area
swing-failure outcomes at 4h on these five assets for every bar at or before 2026-09-25T00:00Z before this row was
drafted, and this trade form (stop, split targets, time stop, invalidation, minimum reward) was never scored; X's
standing ledger line marks any later value-area registration pre_seen on those bars; the K = 3 and
one-close-acceptance variants are among the printed tables". `items`: `XR/tierc11x/va/two_trades.parquet` (sha256
`a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0`), detector `va`, trade `swing_failure`, variants
`k3` and `die_parity`, lens `4h`; `XR/tierc11x/va/X3.md`;
`XR/tierc11x/LEANS_X.md:1816-1818, :2468-2470`. Disclosures carried in the row's `disclosures[]`, printed under the
cell: the label's text; D-2 (what the licence was earned on) and D-3; "T tuning-fit (regime reading; the strict-INSIDE
twin is printed in Stage V); in-sample for tuning-era trades"; the lookback's `l_label`; the count of trades OPEN at
W; the count of rows on which the D12 ceiling would have bound (L-R.20).

SOURCE: O-23, O-30; DISCLOSURES D-2, D-3; L-X.13; the files as cited [schemas and variant sets read at drafting].

RIVALS: `selection_hazard` only — X's standing line, which O-23 enacts, names `pre_seen`. The RE-SCORE template on
this row — not taken: O-30 (the trade form was never scored; a label must be true).

FAILS-IF: F-REG (TEMPLATE leg, L-X); mutation: the template rewritten to the RE-SCORE form.

**L-R.24 TIER-E BESIDE THE ROW** — "Tier-E beside: the holdout slice · the 1d cell · the 1d-direction-guarded twin
(refuse when 1d is accepted against) · the maker twin" (contract :74-75)

READING: Each is a collared arm under `regbooks/P-SFP-VA-1/` (or a scorer-derived leaf); none carries a verdict
word; each ridden book has its own one-position sequence, its own OPEN list and its own strip rows (L-R.21); every
arm inherits the geometry law of L-R.14, the walk law of L-R.19 and the uncapped funding of L-R.20 unless its own
bullet says otherwise. The arms of record of this regbook are exactly: `scored`, `strip`, `tierE__unfiltered`,
`tierE__cell_1d`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__maker_assumed`, `tierE__x_geometry`,
`tierE__x_gaplaw` (L-X.24); an arm with no row is written EMPTY. Each Tier-E arm's interval is the scorer's ONE leaf
`arm__<slug>` (L-X.14: the row's ruler on that arm at the seed of record; no p, no bar, no sensitivity seed, no
slice, no LOAO, no word).
- **The holdout slice** — the scorer's `holdout_slice` leaf on `scored` (era by the entry close), printed beside
  the verdict with the fixed sentence "causal for the tuning-fit T and lookback only; the class was pre_seen; the
  era of record is the full corridor".
- **The 1d cell** `tierE__cell_1d` — the whole law of L-R.10-L-R.21 with the lens swapped: events = V2 swing
  failures of lens `1d`; `lf = E.BK.frame_l(stem, "1d")` (the Stage D derived tape, asserted row-identical to the
  filed `va_bars_1d` on `open_ms`, close and ATR at Round6); ATR_1d; `T` = the reader's `traverse("traverse.1d")`
  (its `provisional` flag carried, L-V.18); the same `a`, `RAIL`, `RR`, `G`; rows carry `lane = "sfp-va-1d"`. Its
  licence pair is `1d|taker`: the builder calls `licence("1d", "taker", era)` for the three eras before the cell is
  built. The cell is built on the full corridor like its parent; its collared sidecar carries `licence_pointers =
  {era: "research_outputs/tierc12/va/VA_MIRROR.json#licence[1d|taker].by_era[<era>]"}` and the booleans
  `licence_ok_by_era` — never the words: the words themselves are printed only in §0 beside the row. Where
  `licence_ok_by_era["ALL"]` is false the cell's description reads "ERA NOT LICENSED on the full corridor — printed
  as a disclosure; the licensed era is the holdout", and its holdout slice is printed first. On 1d the interval sum
  is shifted by the entry bar: it charges the entry day's in-bar prints and omits the exit day's on a close exit.
  `n_stamps_inside_entry_bar` and `n_stamps_inside_exit_bar` are filed per row and their totals printed in the
  cell's description with that sentence; the booking stays `account_l`'s so the cell remains comparable with the
  estate's 1d lanes.
- **The 1d-direction-guarded twin** `tierE__guard_1d` — the 4h book with one added refusal, placed after the
  one-position test and before geometry (disposition `guard_1d`): refuse the event when the 1d state at τ = the
  entry close — row `asof_index(close_ms_1d, τ)` of the filed `va_bars_1d`, the last 1d bar closed ≤ τ (O-14) — is
  ACCEPTED against the trade (`ACCEPTED_BELOW` for a long, `ACCEPTED_ABOVE` for a short). A refused event does not
  hold the slot; the book is re-walked.
- **The maker twin**, two arms, sidecar `toll = "maker_entry_targets__taker_stop"`; both are on L-0.30's
  `ORDERED_TWINS_T` (the contract orders them at :75 although `4h|maker` is outside the licence set), and the report
  prints `VA_MIRROR.json beside.twin_words["4h|maker"]` beside them (the sidecars carry the pointer, never the word).
  MAKER legs = entry, T1, T2 at `E.fees()[stem]["maker_bps_side"]`; TAKER legs = stop, time stop, invalidation, the
  mark at `taker_bps_side`; no slippage on a maker leg. Fees are booked per fraction
  (`tierc12_rangewalk.fee_per_fraction`, the mirror of X's): T1 filled → `[q·(m·e + m·t1_px) + (1 − q)·(m·e +
  x·exit_px)]/R`, else `(m·e + x·exit_px)/R`, `m` the maker rate, `x` the maker rate iff the exit is T2 else the
  taker rate; gross and funding are `account_l`'s (funding uncapped). The fee columns follow L-X.24; `haircut_net_r
  = net_r − fee_taker_r × (slippage_bps_side / taker_bps_side)` (AM-7's maker clause); `taker_twin_net_r` = the same
  path at all-taker; `taker_twin_haircut_net_r = taker_twin_net_r − fee_all_taker_r × (slippage_bps_side /
  taker_bps_side)` (required on these two arms, L-X.24).
  - `tierE__maker_conditioned` (named first; sidecar `fill_rule = "tick"`). Every maker leg of the tier fills by the
    fill of record (OD-11). With `grid = TickGrid(E.ticks()[stem])` (L-D.23) and `n_tick` = the pin
    `scalp.fill_ticks`, the conditioned entry at `P = e` books iff, on the FIRST 5m child of bar `entry_i + 1` (the
    5m bar whose open equals that bar's open), `grid.dec(low) < grid.dec(P) − n_tick·grid.T` (long) /
    `grid.dec(high) > grid.dec(P) + n_tick·grid.T` (short), evaluated exactly in the grid's trapping decimal context;
    its maker targets fill likewise against their levels; a zero-volume child fills nothing. Otherwise the event is a
    MISS (`miss`, `miss_nochild`, or `fill_unresolved` when the bar lies past `hi`), counted, never a trade. On the
    fill child the stop is tested (L-R.19 steps 1-2) and no target is credited (`fillchild_target_withheld`,
    counted); the rest of that 4h bar is walked child by child by L-R.19's step if its 5m children reproduce its
    high, low and close within `E.LN.REPR_TOL`, else targets rest from the next bar and the stop is judged on the
    parent; a maker target is booked at its level; the time-stop clock stays at `entry_i`; funding runs from
    `entry_i + 1`. X's law (`low < P`, no tick) runs only inside F-SFP-MIRROR's leg against `X2_twins.parquet` book
    `maker_conditioned`, and the number of fills X's law would add is printed (`x_law_extra_fills`): the count of
    this twin's `miss` rows whose first child traded strictly through `P` — a count, with no book, walk or outcome
    behind it.
  - `tierE__maker_assumed` (sidecar `fill_rule = "touch"`): the record's own path — the same walk and the same rows
    as `scored`, its targets filled on the record's touch — re-booked at maker fees.
- **The unfiltered twin** `tierE__unfiltered` (L-R.15).
- **X's geometry law as a twin** `tierE__x_geometry` — the 4h book with `geometry(…, law = "x")` in place of the
  tier's (L-R.14 point 3): X's three refusals in X's order after `stop_none`, no fee-band flag and no void T1;
  everything else is the record's (V2 events, rr-min, the tier's walk law, the invalidation, the booking). Its own
  one-position sequence; printed with it, the rows that differ from the record: in both books, only in the record,
  only in the twin.
- **X's record gap law as a twin** `tierE__x_gaplaw` — the 4h book with `bar_step(…, gap_law = "x_record")`
  (L-R.19): the open decides first for stop and targets, a stop books the stop price, a target books `max(level,
  open)` long / `min` short; everything else is the record's. Its own one-position sequence; the rows that differ
  from the record are listed the same way.
- The scorer's common leaves (L-X.14): `seed_sens`, `haircut` (the charter twin), `haircut_sens`, `taker_twin`
  (IDENTICAL on the record), `taker_twin_haircut`, `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`,
  `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`, `strip` (`n` per arm and one
  pointer).
TC12-R is a 5m reader for ONE purpose, declared here for `FIVE_MIN_READERS_T` (L-0.30): the fill child and
fill-bar walk of `tierE__maker_conditioned` (the 5m children of 4h bars, home assets, through `E.D.load_asof(stem,
"5m")`). That one read is visible in `stage_r/sfp/READ_SET.json` and no other 5m path is. No 5m bar originates a
signal and the record reads none.

SOURCE: contract :74-75, :93-94; OD-8, OD-9, OD-10, OD-11, OD-14; `LEANS_X.md:565-612` (LX-1.1 (i)-(iii)), :1386-1396
(LX-X2.13, a collared cell on a lens with a failing word); `tc11x_sfp.py:148, :664-712, :756-803`;
`MR/LEANS.md:85-93` (L-1.2); AM-7; L-D.16, L-D.23; L-V.2, L-V.17; L-X.14, L-X.24; O-17, O-19.

RIVALS: one maker row — the contract's "maker twin" has two filed readings in X; both are printed, the conditioned
one first. X's tick-less strict trade-through for the conditioned twin — not taken: one fill law for every maker leg
in the tier (OD-11); X's law is held on X's rows by the mirror and its extra fills are counted. The 1d cell on the
holdout only — its parent names the full corridor; the pointers to the era words are carried instead. The licence
words on the cell's sidecar — a collared file carries no verdict word.

FAILS-IF: F-SFP-MIRROR (the maker booking and the conditioned walk against X's filed twins, under X's laws); F-SFP
[i]: the guarded twin's refused events all carry a 1d state accepted against, read at their entry close; F-SFP [b]
on every arm (each arm's own identities; `fill_rule` and `toll` of each sidecar; every conditioned fill satisfies the
tick test in exact decimal and every `miss` fails it); F-NOT LICENCE and F-NOT 5M (L-0.30); mutations: maker bps on
the stop leg; a target credited on the fill child; the guard read at the 1d bar still forming; the conditioned entry
filled on a child that only touches `P`; a licence word written into the 1d cell's sidecar (F-COLLAR RED).

**L-R.25 F-SFP AND THE MIRROR FIXTURES** — "F-SFP (3 trades hand-walked incl. a POC fill and a time-stop exit)"
(contract :119)

READING: suite `scripts/tierc12_stage_r_fixtures.py --stage=TC12-R.sfp`, transcript
`T12/stage_r/sfp/FIXTURES_STAGE_R_sfp.txt`; blocks `F-SFP [a]` … `F-SFP [i]` (the letter e is not used), `F-SFP-ASOF`,
`F-SFP-MIRROR [<leg>]`. The suite imports the builder, `tierc12_rangewalk` and the reader; it imports no door and
not `analytics.value_area`. **SYNTHETIC legs** (they need no P-SFP-VA-1 book and always run): [g], [h] and
F-SFP-MIRROR. **REAL-BOOK legs**: [a], [b], [c], [d], [f], [i], F-SFP-ASOF and F-TRAV [e · <book>]; when the row is
closed by precondition each of them prints `CLOSED-NO-BOOK P-SFP-VA-1` and asserts from files that
`regbooks/P-SFP-VA-1/STATUS.json` says `CLOSED_BY_PRECONDITION` and lists no arm (L-0.14 C).
- **F-SFP [a] HAND-WALK.** Three trades of the book of record chosen by a rule frozen HERE, in ascending `(symbol,
  entry_ms)` order, categories first (L-0.14 G): **T-POC** the first trade with a T1 fill (the POC fill); **T-TIME**
  the first OTHER trade whose exit is the time stop; **T-STOP** the first other trade whose exit is the stop. A
  category with no member prints `NONE-EXISTS <category>`, asserts from the book that its count is zero, and its slot
  is taken by the next unchosen trade in key order, printed `FILL`; an empty CONTRACT-NAMED category (the POC fill,
  the time-stop exit) is also printed `FINDING: …` and carried to the report as a finding-not-fixed owned by the
  operator. If the book holds `n < 3` trades, ALL are walked and the leg prints `ONLY <n> EXIST (contract count 3)`
  with `n` asserted equal to the book's row count; `n = 0` prints `EMPTY POPULATION` with the same assertion. The leg
  is GREEN in every such case: no size or composition of the book makes it RED. Walked beside, by the same rule, as
  extra witnesses: the first invalidation exit; the first T2 exit; the first gap stop; the first void-T1 trade; the
  first geometry refusal of each reason; the first rr-min skip; the first one-position skip. Each walk is the
  fixture's own, from the raw 4h tape by explicit path, sharing no code with the builder, the reader, the doors or
  the module: `VA(t0−1)` by `analytics.profile.volume_profile` on the raw slice (its POC, VAL, VAH passed through
  Round6 must equal the filed `*_f`); the probe's closes against the edge; the return within K; the extreme; ATR by
  its own Wilder loop; stop, R, T1, T2, the refusal clauses, `rr`; the bar walk STOP AT OPEN → STOP → T1 → T2 →
  INVALIDATION → TIME STOP; fees and funding (uncapped) re-booked by its own arithmetic. FAILS IF any price, bar,
  fill, reason or `net_r` differs beyond the fixture-typed tolerance X's F-SFP used.
- **[b] IDENTITIES** on every row of every arm (L-R.10-L-R.24, as each reading's FAILS-IF states). **[c]** one
  position (L-R.18). **[d]** the prefix identity of the two rides and the strip, per ridden arm (L-R.21). **[f]**
  fees, funding and net (L-R.20). **[g]** the synthetic event and bar sets (L-R.14, L-R.17, L-R.19), fed to the
  production `geometry` and `bar_step` with the fixture's typed answers. **[h]** the closed row (L-R.22). **[i]**
  the guarded twin (L-R.24).
- **F-SFP-ASOF** — for a seeded sample of events per asset (both eras, both sides; `n = 20` per asset, the count X
  filed for the mirrored leg, `XR/tierc11x/LEANS_X.md:2319`, a fixture-typed literal printed in the transcript header;
  an asset holding fewer contributes all it holds, the count printed; stream `default_rng([SEED,
  crc32("stage_r|F-SFP-ASOF")])`, L-0.14 F): the builder run on the 4h tape cut at the event's `known_close_ms`
  (`E.load_asof_at(stem, "4h", ·)`, fresh arrays) and on `events(asof_close_ms=·)` / `bars(…, asof_close_ms=·)`
  reproduces `(e, stop, R, T1, T2, disposition, rr)` exactly; `T` held at its filed value (the leg says it does not
  test the fit); leans on F-VA-ASOF [d], and the transcript carries the fixed line `leans on F-VA-ASOF [d]: a filed
  row at bar k equals a door rebuild on tapes cut at close_k`. No leg of this suite re-runs a door.
- **F-SFP-MIRROR** — the mirrored step with `gap_law = "x_record"`, `geometry` law `"x"` and the invalidation
  switched off, against X's filed rows, on X's events alone:
  - [GEOMETRY] for every row of `XR/tierc11x/sfp/X2_trades_4h.parquet` (sha256
    `552e7582d7559c032438f89c402e3070a3011559c1b334babd4c942f23b1bbef`) and `X2_trades_1h.parquet`
    (`4e3b5f4f7eb01db468b4203c4b64362f54fe388419290b5c58a68d9a54427eac`), on the tape cut at X's pin: geometry
    re-derived at full float from the filed integers (`breach_i`, `entry_i`, `d`) and the filed box (`top_pre`,
    `bot_pre`) under X's own T1 (the box mid) → `stop_px`, `r_dist`, `T1`, `T2` equal at the 6-dp write law;
  - [WALK] the mirrored walk with the row's `T` → `harvest_i`, `harvest_px`, `exit_i`, `exit_px`, `exit_reason`,
    `bars_held`, the gap flags and `both_touch_bars` equal;
  - [BOOKING] the mirrored booking at X's rates (taker from `E.fees()`; maker = `maker_pin.x_assumed_bps_side` of
    TC12's fee file) → `gross_r`, `taker_fee_r`, `taker_net_r`, `maker_fee_r`, `maker_net_r`, `haircut_net_r` equal
    at the write law, and X's filed `funding_r` equal to `acc["funding_r"]` — the CAPPED figure, as X booked it;
  - [MAKER] the `maker_conditioned` rows of `X2_twins.parquet`
    (`f2abf81de9202eef907857355799536012992d114b87a3fbd00a44ac4ae28c25`) reproduced from the 5m children under X's
    fill law (`low < P`, strict, no tick): key set, misses, fills;
  - [SWITCH] an AST scan of every `scripts/tierc12_*.py`: the value `"x"` reaches `geometry`'s `law`, and
    `"x_record"` reaches `bar_step`'s `gap_law`, at exactly the two typed call sites each (this leg; the builder's
    `tierE__x_geometry` / `tierE__x_gaplaw` arm), and X's tick-less maker fill is called from this leg alone.
  FAILS IF any compared value differs, or a switch has another call site. The mirror adds nothing X's walk lacks
  except the invalidation close event, which is switched off in these legs.
- PLANTS: T1 from `poc_n` → [a], [b]; the rail dropped → [a] on a rail-bound witness, [b]; `ext` without the
  return bar → [b]; target-before-stop → [g], F-SFP-MIRROR [WALK]; a gap stop booked at the stop price under the
  tier's law → [g]; a target credited at `max(level, open)` under the tier's law → [g]; the tier's gap law run on
  X's rows → F-SFP-MIRROR [WALK]; the time stop one bar late → [a] T-TIME, [b], F-SFP-MIRROR [WALK]; the
  invalidation ignored → [b]; `R` before the rail in `rr` → [b]; an overlapping trade → [c]; a trade wrongly marked
  OPEN → [b]; maker bps on a taker leg → [f], F-SFP-MIRROR [BOOKING]; the capped funding booked on the record → [f];
  `T2` from `ATR[i+1]` → F-SFP-ASOF; an acceptance with `known_close_ms` after the cut used → F-SFP-ASOF; the
  mirror's T2 offset applied outward → F-SFP-MIRROR [GEOMETRY]; a target credited on the fill child of a conditioned
  row → F-SFP-MIRROR [MAKER]; a third call site of `"x"` in a copy of the builder → F-SFP-MIRROR [SWITCH]; the 1d
  bar still forming read by the guard → [i]; a flipped licence leaf that still builds an arm → [h]; a STATUS copy
  reading `BUILT` on a closed row → detector `CLOSED-STATUS`; a typed time stop → F-TRAV [a · tierc12_stage_r_sfp].

SOURCE: contract :119; OD-8, OD-9, OD-10, OD-11; `LEANS_X.md:2309` (X's F-SFP and its frozen selection rule), :2319
(F-SFP-ASOF, "a seeded sample of ≥ 20 hardens per asset"), :1340 (F-FEE-EQ); L-0.14 (the leg law, the hand-sample
law, the fixture stream); the X files as cited [schemas read at drafting; row counts on file 588 and 2,408].

RIVALS: hand-walk trades picked after the book is seen — the rule is frozen first. Trust the mirror without X's
filed rows — O-4 orders mirror AND equality. Hold the tier's own gap and geometry laws against X's rows — they are
different laws by ruling; the tier's are held by [a] and [g], X's by the mirror. A door re-run on the cut tape from
this suite — forbidden (O-29); Stage V's F-VA-ASOF [d] owns prefix identity.

FAILS-IF: as stated in the reading.

---------------------------------------------------------------------------------------------------------------
#### C · The Tier-E tables of Stage R

Every table of this part is collared (L-0.16), descriptive (`would_read_ci_only = "no interval"`), carries no
verdict word, registers nothing and promotes nothing (O-13). Population: the five home assets; events known at or
before W; the strip is a count beside.
**Who builds what (O-29).** The two-trades tables of L-R.26-L-R.29 need the V2 machine run on scheduled boxes and on
permuted volume, so they are BUILT by DOOR 2, `scripts/tierc12_va_trades.py`, at the record `TC12-V.trades`, and filed
under `T12/va/trades/`: L-V carries the builder, the files and the record (L-V.2, L-V.23, L-V.24); this section keeps
their DEFINITIONS — events, partition, outcome law, base rate, null, statistics — and the definitions of their
fixtures, which are HOSTED in `scripts/tierc12_va_fixtures.py --stage=TC12-V.trades` (transcript
`va/trades/FIXTURES_VA_TRADES.txt`). No module of this section builds or re-derives them, and no table of DOOR 2
holds a trade column (`net_r`, `gross_r`, `fee_r`, `funding_r`, `entry_px`, `stop_px`, `exit_reason`). The
take-profit venue of L-R.30 is this section's own build (`scripts/tierc12_stage_r_tp1d.py`, record `TC12-R.tables`).

**L-R.26 THE TWO TRADES ON THE VALUE AREA — THE EVENTS** — "the two trades per lens on the VA at 4h and 1d — the
breakout-retest (ACCEPTED → first retest of the accepted edge that holds, FLIP_HOLD pins reused) and the swing
failure" (contract :76-78)

READING: Lenses L ∈ (`4h`, `1d`).
- **The swing failure**: V2's `swing_failure` rows of lens L in the filed `va_events` (L-R.10's event, here as an
  outcome anchor, not a ride). Anchor bar = the return bar `i`; sign toward value; edge = the frozen `E`.
- **The breakout-retest**: X's first-HOLD scan (`scan_retests`, `retest_verdict`, `touch_mask`; `tc11x_va.py:
  674-728`), mirrored in and built by DOOR 2, `scripts/tierc12_va_trades.py` (L-V.2), on the filed `acceptance` rows
  (through the reader, sha-asserted) and the tape (through `E`). Anchors = the V2 acceptances of lens L in bar order,
  each with its level `E` (the frozen accepted edge). For an acceptance at bar `a` on side `top` (accepted above
  VAH): a qualifying touch at `j` is `l[j] ≤ E` with `c[j−1] > E` (mirrored for `bottom`: `h[j] ≥ E` with `c[j−1] <
  E`), taken in bar order over `(a, min(a + TTL, next acceptance of EITHER side − 1, n − 1)]`. Verdict at a touch:
  `truncated` if `j + HOLD ≥ n`; `failed` iff some close in `j … j + HOLD` is through the level by MORE than
  `MARGIN·ATR_L[k]` (`c[k] < E − MARGIN·ATR_L[k]` for `top`); else `hold`. The first `hold` is the event, known at bar
  `j + HOLD`; a `truncated` verdict ends the scan; every evaluated touch is a row. Sign: with the acceptance (`top` →
  long). `MARGIN`, `HOLD`, `TTL` are the FLIP_HOLD pins read BY OBJECT: `E.BK.FLIP_HOLD_MARGIN`,
  `E.BK.FLIP_HOLD_BARS`, `E.BK.MEM_TTL_BARS` (`tierc10_brk.py:145-149`, themselves read out of the AST of
  `engine/rangefinder.py` `PINS_V2`, never by importing the range machine), asserted equal to
  `XR/tierc11x/va/build_manifest.json` → `pins.laws.flip_hold_margin`, `.flip_hold_bars`, `.mem_ttl_bars`. `n` = the
  bars closing at or before W.
- File: `T12/va/trades/TWO_TRADES_EVENTS.parquet`, key `[lens, asset, trade, side, anchor_i, i]` — one row per swing
  failure (`anchor_i == i`, the return bar) and per evaluated retest touch (`anchor_i` = the acceptance bar, `i` =
  the touch bar), with `verdict` (`hold` / `failed` / `truncated`; empty on a swing failure), `known_i`,
  `known_close_ms`, `E`, `sgn`, `era`, the lens-above cell `u_cell` and `u_lookback_label` (L-R.27), the outcome
  columns of L-R.28 on event rows, and `l_label`.

SOURCE: contract :76-78; O-29; `tc11x_va.py:174-176, :674-728, :756-764`; `LEANS_X.md:1693-1706` (LX-X3.9);
`tierc10_brk.py:139-149`; L-V.2 (DOOR 2), L-V.24; the manifest keys [read at drafting].

RIVALS: the band retest pins (hold 3, `C.RETEST_PINS`) — the contract says FLIP_HOLD. The retest of the LIVE edge
(X's twin) — the contract says "the accepted edge". One-shot first touch — TC10's rule, X's twin. The scan in a
module of this section — the tables are DOOR 2's, whole (O-29).

FAILS-IF: F-RETEST-MIRROR (hosted at `TC12-V.trades`): [r1] fed X's filed RECORD acceptances (`events_va.parquet`,
`variant == "record"`, `cls == "accept"`) on the tape cut at X's pin, the mirrored scan reproduces X's filed
`retest-touch` and `retest-hold` rows of that variant (anchor, touch bar, verdict, `known_at`, level at the write law)
at 4h and 1d; [r2] fed V2's acceptances it reproduces X's filed `die_parity` `retest-hold` rows; every HOLD has
`known_at == touch + HOLD`; mutations: an off-by-one window start; the hold window read as `touch … touch + HOLD −
1`; the band pins substituted.

**L-R.27 THE LENS ABOVE AND THE PARTITION** — "conditioned on the lens above {accepted aligned · inside mid ·
inside at its own edge (coincidence)}" (contract :78-79)

READING: The lens above is TC11's ladder (`scripts/tierc11_nest.py:101`): above `4h` is `12h`; above `1d` is `1w`.
The state of the lens above U is read at the event's known-at close τ as U's block of the reader's stamp at τ (the
last U bar closed ≤ τ, O-14). Every event falls in exactly one cell of a WHOLE partition, filed as `u_cell`; the
contract's three cells are starred, the rest are printed too (TC11's L-R.6 form):

| `u_cell` | condition (d = the trade's sign; first match in this order) |
|---|---|
| `NA` | no conditioning lens — empty by construction at both lenses (O-28) |
| `UNDEFINED` | U's state is UNDEFINED, or no U bar has closed |
| ★ `ACCEPTED_ALIGNED` | U ACCEPTED_ABOVE and d = +1, or U ACCEPTED_BELOW and d = −1 |
| `ACCEPTED_COUNTER` | U ACCEPTED on the other side |
| `PROBING` | U PROBING_ABOVE or PROBING_BELOW |
| ★ `INSIDE_COINCIDENT` | U INSIDE and the event's edge of L within `F·ATR_L` of either in-force edge of U: `abs(E − U_vah) ≤ F·ATR_L[k]` or `abs(E − U_val) ≤ F·ATR_L[k]` (inclusive) |
| ★ `INSIDE_MID` | U INSIDE, not coincident, and U's filed `pct` within `MID_BAND` (inclusive) |
| `INSIDE_OTHER` | U INSIDE, neither |

- `E` = the event's frozen edge of L (the probed edge of a swing failure; the accepted edge of a retest); `k` =
  the event's known-at bar of L; `U_vah`, `U_val` = U's profile IN FORCE at τ (the block's `vah`, `val`).
  `F` = the contract's coincidence fraction (:45; pin `va.nest_frac`, L-V.4). `MID_BAND` = TC11's "in-range mid"
  band, read as an AST literal from the text of `scripts/tierc11_nest.py:109` (on file `(25.0, 75.0)`); the contract
  states no number for "mid" and none is typed. The comparison is arithmetic on filed columns, made in DOOR 2; no
  state or event of U is re-derived.
- **L = 4h.** U = 12h: the `12h_` block of the stamp (`12h_state`, `12h_val`, `12h_vah`, `12h_pct`,
  `12h_bar_close_ms`). The 12h lens is closed for range TRADING (contract :40) and is read here only as a state.
- **L = 1d.** The 1w value area is built on the 1d pin's bar count (L-V.5; `VA_PINS.json by_lens.1w`, `source_lens =
  "1d"`, label `BORROWED: the 1d pin's bar count; X pinned no 1w lookback; not X's law at 1w`). For a 1d event with
  known-at close τ: `U = 1w`; U's block is the reader's stamp at τ — row `k = asof_index(close_ms_1w, τ)` of
  `va_bars_1w`: the last COMPLETE Monday-anchored derived week whose close ≤ τ (a week still forming is never read;
  on a Monday 00:00Z close the week closing at τ IS read, O-14). Columns read, and no other: `1w_state`, `1w_val`,
  `1w_vah`, `1w_pct`, `1w_bar_close_ms`. The eight-cell partition of L-R.27 applies unchanged, the coincidence unit
  being `F·ATR_1d[k_event]`; `UNDEFINED` holds a 1d event whose U state is UNDEFINED or for which no 1w bar has
  closed; `NA` has no member at either lens and is printed as a row with `n = 0`, `nan_reason = "absent by
  construction: every lens of the table has a lens above (O-28)"`. L-R.28's base rate (ii) at 1d reads 1d's own nest
  flag against 1w at `close_k`.
- **The label.** Every 1d row of `TWO_TRADES_EVENTS`, `TWO_TRADES_VA`, `TWO_TRADES_BASE`, `TWO_TRADES_NULL` and
  `TWO_TRADES_NULL_DRAWS` (the tables that carry the lens-above cell) carries `u_lookback_label = "BORROWED: the 1d
  pin's bar count; X pins no 1w lookback"` (4h rows: the empty string).
- **The two reads of 1w (O-28).** The 1w block is read in EXACTLY TWO places, both Tier-E: the V5 stamp columns, and
  this lens-above conditioning axis of the 1d rows of the two-trades tables. It is read by no gate, no permission, no
  direction guard, no licence, no time stop, no order and no registered construction. No 1w range cell, trade,
  traverse row or feasibility row exists. The five columns are read by DOOR 2 alone (L-0.25's `ONEW_READERS_T`); no
  module of this section reads a `1w_` column, and neither registration spec below declares one.

SOURCE: contract :45, :78-79; O-14, O-28; `tierc11_nest.py:101, :108-109, :1466-1483` (`CELLS`, `STARRED`, `_cells`),
:1487-1535 (`l1_cell`: the event's boundary of L against either live boundary of L+1, ATR of L); `MR/LEANS.md:260-270`;
L-V.5, L-V.20, L-V.21; L-0.25.

RIVALS: only the three named cells — a reader could not see what share of events they hold. Coincidence by L's
per-bar nest flag — that flag tests L's LIVE edges; the event's edge is the frozen `E` (TC11's "event's boundary"
law). Mid by a typed band — no file would supply it. Every 1d event in `NA`, the 1d trades printed unconditioned —
not taken: O-28 gives the contract's clause its object at 1d. A 1w lookback of its own — X pins none; the bar count
is the 1d pin's and every row says so.

FAILS-IF: F-GRID [TWO_TRADES_VA] (the partition: Σ n over the cells == the events); F-TWO [a] (hosted at
`TC12-V.trades`): every event's `u_cell` recomputed by the fixture from the filed U block read by its own linear-scan
as-of, `u_lookback_label` equal to the string above on every 1d row and empty on every 4h row; F-NOT leg 1W (L-0.25).
Mutations and plants: U read at the bar still forming; the 1w bar still forming at τ read → RED; the coincidence
threshold in `ATR_U`; a 1w column read by a copy of the P-SFP-VA-1 builder (must also turn F-NOT leg 1W RED).

**L-R.28 OUTCOMES, THE TOLL, THE BASE RATE** — "H20/H100 net of the lens's toll; base rate" (contract :79)

READING: X's outcome road and statistics (`C.outcome_ledger`, `tc11x_va.stats_rows`), mirrored in DOOR 2 and held
equal to X's filed tables.
- **Term**: from the CLOSE of the known-at bar `k`: `term_H = sgn·(c[k+H] − c[k]) / ATR_L[k]`, H in bars of L;
  CENSORED, never shortened, when `k + H` passes the last bar closing at or before W; MFE and MAE beside. The
  horizons are read from `XR/tierc11x/va/build_manifest.json` → `pins.laws.horizons` (on file H20 = 20, H100 =
  100), asserted equal to the AST literal `HORIZONS` of `scripts/tierc10_census.py:123`, and also held equal to the
  contract's `H20/H100` (:79) by the pin door (pin `two_trades.horizons`).
- **The lens's toll** = the toll of the lens's licence: taker at 4h and at 1d (contract :41) — the round-trip
  taker rate `E.fees()[stem]["taker_round_trip_bps"]`, in the anchor's own ATR: `toll_atr_evt = (bps /
  BPS_PER_UNIT)·c[k] / ATR_L[k]`. A pooled row's toll is the BINDING maximum of its members' tolls (the census
  law X kept).
- **Statistics per cell**: `n_events`, `n` (uncensored, good ATR), `n_censored`, `median_term`, `mean_term`, the
  quartiles, `hit_rate`, `hit_rate_net`, `median_mfe`, `median_mae`, `toll_atr`, and `net = round(median_term, ND)
  − round(toll_atr, ND)` with `ND` = `pins.laws.round_nd`; `provisional` when `n` is under the floor (L-V.4).
- **Grid** `va/trades/TWO_TRADES_VA.parquet` (a GRID, declared key `[cell]`): `lens` × `trade` (`swing_failure`,
  `breakout_retest`) × `direction` (`long`, `short`) × `era` (`ALL`, `tuning`, `holdout`; by the anchor's close) ×
  `panel` (the five home stems and `POOLED` — the five pooled; X's key for the same panel is `POOLED:CLASSIC5`) ×
  `u_cell` (L-R.27's eight) × `horizon`; the unconditioned table `TWO_TRADES_VA_UNCOND.parquet` drops the `u_cell`
  axis. The asset axis is named `panel`, never `asset` or `symbol` (L-L.25).
- **Base rate** `va/trades/TWO_TRADES_BASE.parquet` (declared key `[cell]`): the same statistics anchored at EVERY
  closed bar `k` of L, for each direction, censored the same way, net of the same toll — (i) unconditional and (ii)
  within each cell of the same partition read at `close_k`: U's block by the same stamp at `close_k`, coincidence
  there = L's own nest flag at `k` (`coin_vah OR coin_val`, L-V.21; at 1d that flag is 1d's own, against 1w). Each
  event row prints the base row of its own cell and `net − base_net`.
- X's filed rows of the nearest laws (`va|swing_failure|k3`, `|die_parity`, `va|breakout_retest|die_parity` of
  `two_trades.parquet`) are printed beside as the continuity columns, quoted by key.
- Every row of every table of this family carries `l_label` (the lookback is tuning-fit) and, on 1d rows,
  `u_lookback_label` (L-R.27); no traverse is read here, so no row carries a `t_label`.
- Printed WHOLE in the stage document of record `va/trades/TWO_TRADES.md` (every grid of the family); the report
  carries one pointer row per grid — path, sha, cell count (L-X.28).

SOURCE: contract :41, :79; `scripts/tierc10_census.py:123, :136, :1352-1394`; `tc11x_va.py:842-924`; `LEANS_X.md:
1756-1777` (LX-X3.11); `MR/LEANS.md:271-278` (the base rate within each L+1 cell); L-0.17 (the pin
`two_trades.horizons`); L-V.24; the manifest keys [read at drafting].

RIVALS: the row's own trade toll (maker) — the licence at 4h and 1d is taker. A pooled median toll — re-derives
different nets from X's (scout U2 H17). Terms that read strip bars — O-9: the window ends at W.

FAILS-IF (hosted at `TC12-V.trades`): F-TWO-MIRROR: on X's filed `events_va.parquet` rows of variants `die_parity`
(`sfp`, `retest-hold`) at 4h and 1d, the mirrored ledger reproduces the filed `term_H20`, `term_H100`, `cens_*`,
`toll_atr_evt`; and the mirrored statistics on those rows reproduce X's filed `two_trades.parquet` rows for
`va|swing_failure|die_parity`, `va|breakout_retest|die_parity` and `base|every_bar|record` (every statistic at the
write law); F-TWO [b]: the base-rate cell of every bar recomputed by the fixture from the filed blocks and nest
flags; F-GRID [TWO_TRADES_VA], [TWO_TRADES_VA_UNCOND], [TWO_TRADES_BASE]; mutations: a one-row drop, the horizon
shortened at the tape's end instead of censored, the pooled toll taken as a median → F-TWO-MIRROR; the base-rate
cell taken with the nest flag of bar `k + 1`, or with U read at the bar still forming → F-TWO [b]; a dropped `n = 0`
row → F-GRID.

**L-R.29 THE NULL** — "null gaps+order (R10)" (contract :79)

READING: R10's null is defined on boxes — it permutes the GAPS and the ORDER of the (life, height) pairs of the
real confirmed ranges and replays the trades on static boxes (`scripts/tierc10_null.py:239-340, :356`). X's null of
record for the value area is another object, `tr_tercile_lblock` (`tc11x_va.py:236`). The reading: **build
gaps+order on VALUE REGIMES, because the schedule law transfers; print X's VA null beside, each named; HALT rather
than relabel.** Both nulls are run by DOOR 2 — the only place the V2 machine is run on scheduled boxes or on permuted
volume (L-V.2, L-V.23).
- **Why it transfers.** A V2 value regime has what the schedule permutes: a start, a life, a height and gaps —
  and X's own feasibility adapter is the filed precedent for treating it as a range (`confirm = r0`, `die` = the
  acceptance bar, height = `VAH(r0−1) − VAL(r0−1)`, `atr[r0]`; `LEANS_X.md:1720-1740`).
- **The real box set**, per (asset, L), from the filed regimes — read through `regimes(asof_close_ms=W)`, the only
  form the reader offers — and `va_bars_<L>` on the bars closing ≤ W (`n` of them). The box set is cut at W: regimes
  with `r0_close_ms ≤ W` are kept; a kept regime whose `die_close_ms > W` or is null is the alive one (`life = n −
  r0`, censored) and its `die_*`, `end_*`, `n_bars` are not read; regimes with `r0_close_ms > W` are dropped. One box
  per kept regime, in bar order — `real_confirm_i = r0`; `life = die_i − r0` for a regime dead at or before W;
  `height_atr = (vah_j[r0] − val_j[r0]) / atr[r0]` (the judging profile of bar `r0`); the `m + 1` gaps around them.
  Preconditions, each a HALT `NULL-GAPS-ORDER-UNBUILDABLE` (the three of `real_box_set`): lives overlap; a regime
  other than the last is alive; `atr[r0]` not positive; and lives + gaps must tile `n`.
- **The schedule** — a mirror of `schedule(real, rng, keep_order=False)`: `perm = rng.permutation(m + 1)` of the
  gaps, `u = rng.random(m)`, `order = rng.permutation(m)` of the pairs, in that draw order; the lead-gap law with
  the value area's own warm floor: if the first gap is shorter than `L_bars` (the lens's lookback, `VA_PINS.json`)
  it is swapped with the first later gap that is not — "no real range confirms inside it, so no null box is born
  inside it either" (the source's reason, its floor being the pivot detector's). RNG = a mirror of `draw_rng`:
  `default_rng([SEED + draw, crc32("<asset>|<lens>|va_regime")])`, SEED the contract's (:4). K = L-V.4's null draw
  count.
- **The box**: `(bot, top) = box_bounds`: `height = height_atr·atr[a]`, `bot = c[a] − u·height`, `top = bot +
  height`, `a` the box's new first bar — static for its life.
- **The machine on a box** — `value_area.va_machine` with (N, M, K) on arrays held constant at each box's edges, run
  by DOOR 2 — the one V2 machine; no mirror of `static_box_machine` is written. The null's swing failures are that
  machine's `swing_failure` events inside the box; its first acceptance ends the box; its breakout-retests are
  L-R.26's scan on the box's dead edge.
- **Conditioning**: each null event is placed in L-R.27's `u_cell` by the REAL state of the lens above at its
  known-at close (TC11's law: "events conditioned on the REAL L+1 state") — for a 1d null event the borrowed 1w
  block, read at the last complete week and labelled exactly as L-R.27 fixes.
- **Statistics per draw and cell**: `n`, `median_term`, `net`, `hit_rate_net` (X's `NULL_STATS`); the real value's
  percentile by the filed mid-rank law (`100 × (#null < real + 0.5 × #null == real) / valid draws`, values at `ND`
  decimals) — "a DESCRIPTION of where the real value sits among the draws, never a p-value". Per draw: event
  counts and the share of bars inside a box.
- **Beside, named as such**: X's VA null of record — the volume null of L-V.23, DOOR 2's filed
  `va/trades/va_null_events.parquet`: the same statistics per draw, retests scanned by L-R.26 on the null
  acceptances, conditioned the same way. Every null row carries `null_variant` ∈ (`gaps+order@va_regime`,
  `tr_tercile_lblock`), the flag `x_va_null_of_record`, and X's sentence that the two nulls answer different
  questions (`tc11x_va.py:195-197`).
- Files, all under `T12/va/trades/` (L-V.24): `NULL_BOXES_VA.parquet` (key `[lens, asset, draw, box]`: `src_rid`,
  `confirm_i`, `life`, `censored`, `bot`, `top`, `u`, `lead_gap_swapped`, `identity_perm`), `va_null_go_events.parquet`
  (the L-V.14 schema plus `draw`, `box`: the gaps+order box events), `va_null_events.parquet` (the volume null),
  `TWO_TRADES_NULL.parquet` (declared key `[cell]`; per real cell and variant), `TWO_TRADES_NULL_DRAWS.parquet` (a
  draw table).
No module of the range machine is imported (L-0.22, L-0.30): `tierc10_null.schedule` and the census outcome road are
read as TEXT and mirrored; the box machine is not mirrored at all.

SOURCE: contract :79; O-29; `tierc10_null.py:109, :120, :224, :239-340, :356-440`; `tierc11_stage_r4.py:112-114, :143,
:713-754, :1058-1065`; `tc11x_va.py:195-197, :236-237`; `LEANS_X.md:1720-1740, :1793-1809`; L-V.2, L-V.14, L-V.23,
L-V.24; scout U6 C5, R-29.

RIVALS: X's VA null alone, labelled "gaps+order" — a relabel: forbidden. X's VA null alone, named — leaves the
contract's named null unbuilt although its law transfers. The pivot detector's warm floor (`ATR_LEN`) as the
lead-gap floor — the value area's first regime cannot start before its lookback. X's seed — TC12's is the
contract's. A mirrored box machine in a decision module — a second V2 machine outside the wall: forbidden (O-29).

FAILS-IF: F-NULL-MIRROR (hosted at `TC12-V.trades`; the letter b is not used — no mirrored machine exists to compare):
[a] SCHEDULE — fed the real PIVOT box set of the ten cells (five home assets × 4h, 1d;
`XR/tierc11x/pins/life_ranges.parquet`, `scale_kind == "calibrated"`: `confirm_i`, `die_i`; heights from the filed
boxes by `src_rid`), TC11's seed and K (`MR/stage_r4/build_manifest.json` keys `seed`, `k_draws`), the pivot's
lead-gap floor (the lineage object `ATR_LEN`) and the tape cut at X's pin, the mirrored schedule reproduces every row
of `MR/stage_r4/R4_NULL_BOXES.parquet` on `(draw, box, src_rid, confirm_i, life, censored, lead_gap_swapped,
identity_perm)` exactly and `u` at the write law; and on the filed `NULL_BOXES_VA`, every box's `life` and `(top −
bot) / atr[confirm_i]` equal the life and `height_atr` of its source regime (`src_rid`), recomputed by the fixture
from the filed regimes cut at W and the judging profile of bar `r0`; [c] MACHINE — `value_area.va_machine` run at the
pivot's three constants (X's `pins.laws.break_confirm_n`, `.break_margin`, `.dev_return_bars`) on arrays held
constant at the edges of TC11's filed boxes reproduces their filed machine columns (`fate`, `die_i`, `die_side`,
`n_harden`), every difference listed and admitted only on a bar whose close lies within the 6-dp rounding band of
the filed height, any other difference RED; [d] two runs byte-equal. Plant: a strip-dying regime's filed `die_i`
used in the box set → `NULL-STRIP` RED, caught by [a]'s clause on the value-regime boxes. Mutations: the draw seed
shifted by one, `order` drawn before `u`, `keep_order=True` → [a]; a box height taken from `VA(r0)` → [a] (the
value-regime clause); the return count and the confirm count of the machine swapped → [c]; a draw seeded from the
clock → [d].
[Structural check made while drafting: on all ten cells the `(rid, life)` pairs of the died ranges in
`life_ranges.parquet` equal the `(src_rid, life)` pairs of draw 0 of the filed boxes.]

**L-R.30 THE 1d VALUE-AREA EDGE AS A TAKE-PROFIT VENUE** — "The 1d VA edge as a continuation take-profit venue (v6
remainder at 0.25 ATR_1d of the 1d edge when 1d is INSIDE) — paired, Tier-E only" (contract :79-80)

READING: TC11's P-TP-RNG law, unchanged, with the venue swapped; built by `scripts/tierc12_stage_r_tp1d.py` (a
DECISION module) at the record `TC12-R.tables`, filed under `T12/stage_r/tables/`. The law of record, quoted
(`MR/registrations/REGISTRATIONS.json`, registration P-TP-RNG, payload sha256
`ad12a44cd8aeb27cc9a1ab0c4225725462f597a6d1dfc621ddf1e06a484de808`, `operative_spec.scored_arm`; the registry is pinned
by TC11's chain head and this payload sha, never by a whole-file sha — L-0.24): "v6 campaigns; at
each 4h bar, with the 12h as-of state at the bar's OPEN IN_RANGE, a resting limit for the remainder (the position
still open: 1.0, or 0.5 after the v6 harvest) at the 12h far boundary -/+ 0.25 ATR_12h, live only when the prior 4h
close is on the near side AND the level is beyond entry in the trade's favour by > 10 bps; fill at max(level, open)
for a long, min(level, open) for a short; EXPANSION/NONE -> no TP; order STOP -> TP -> BELL -> HARVEST -> TRAIL; v6
harvest kept [L-H.1]".
The swap, term by term, for a v6 campaign at 4h bar `j` after entry:
- as-of at the bar's OPEN: `k = asof_index(close_ms_1d, open_ms_4h[j])` on the filed `va_bars_1d` (through the
  reader's `bars("1d")`); "12h IN_RANGE" → row k's `state == "INSIDE"`; any other state → no order, the trail runs;
- level: long `vah − a·atr`, short `val + a·atr`, on row k — the 1d profile IN FORCE at `k` and `ATR_1d[k]`; `a` =
  the contract's "0.25" (:80, pin `tp1d.approach_atr`), asserted equal to the AST literal `APPROACH_ATR` of
  `scripts/tierc11_stage_h.py:133`;
- live iff `d·(level − c[j−1]) > 0` (the prior 4h close on the near side) AND `d·(level − entry_px) > (G /
  BPS_PER_UNIT)·entry_px` (`G = E.R2.FEE_BPS_ROUND_TRIP`; TC11's `TP_GUARD_BPS`) — the venue's own filed guard,
  unchanged;
- fill iff `h[j] ≥ level` (long) at `max(level, o[j])`, `l[j] ≤ level` (short) at `min(level, o[j])`; the
  remainder exits there, `exit_reason = "tp"`;
- order within the bar: STOP (adverse-first; a TP on a stop bar is counted `fill_blocked_by_stop`) → TP → BELL →
  HARVEST → TRAIL; v6's harvest kept.
**The ride**: every base campaign re-ridden independently from its own entry bar, entry price, stop and R (the SET
is kept: no entry is admitted into a freed slot — TC11 L-1.5), by `T9._ride_leg9`'s body with ONE added site, the
TP test between the stop test and the bell (`scripts/tierc9.py:296-310`); booked by `T7._account_chain`. The stage
manifest carries, for this mirrored ride, `ride_spec` (the control card and roles, by object) and `roles_name`, the
objects L-0.30's TRAIL-OFFSET, ADDS and ENTRY-CROSS legs read.
**"Paired"**: the key set is the base's; per campaign `delta_r = net_r(venue) − net_r(v6)`; the identity law holds
— a campaign on which the TP never fills carries v6's `net_r`, exit bar and exit reason at 0.000e+00.
**Filed**:
- `TP1D_CAMPAIGNS.parquet` (key `[symbol, entry_ms]`; per campaign): both books' `net_r`, `delta_r`, the venue's
  exit columns, `ev_tp_ms` (the OPEN of the 4h bar the TP filled in, null when it never did — the one instant
  `TC12-V.stamps.r` stamps for this venue, L-R.31), and — because the venue's only added act is a fill that collects
  gaps while the stop it is paired against ignores them — `gap_tp`, `tp_px_level` (the level) and
  `delta_r_level_fill` = the same ride with the TP booked at the level;
- `TP1D_BARS.parquet` (key `[symbol, entry_ms, bar_open_ms]`; per ridden bar): `k`, state, level, the three live
  clauses, fill;
- `TP1D_SUMMARY.parquet` (key `[era, asset]`; one row per era and home asset): n, n filled, Σ and mean of both books,
  Σ and mean `delta_r`, Σ and mean `delta_r_level_fill`, `n_gap_tp`, withheld and blocked counts, and the D15 tail
  ratio `E.T5.d15`, the wall-exit risk P-TP-RNG names. It prints both deltas side by side; the pooled totals are
  printed in `STAGE_R_tables.md`.
The `max(level, open)` form stays the table's first column because F-TP-MIRROR [b] anchors it to TC11's filed arm.
Every row of the three tables carries `l_label` (the 1d lookback is tuning-fit); no traverse is read. No interval,
no verdict word and no scorer leaf: the table is attached to no registered row and is descriptive (L-0.28, L-X.14).
VA columns read by this builder, declared: from `va_bars_1d` — `asset`, `close_ms`, `state`, `val`, `vah`, `atr`,
`L`, `l_label`. No `1w_` column.

SOURCE: contract :79-80; the registration as quoted [payload read at drafting]; `MR/LEANS.md:498-515` (L-H.1);
`scripts/tierc11_stage_h.py:133, :265-293`; `scripts/tierc11_ride.py:204, :208, :613-633, :680-686`;
`scripts/tierc9.py:268-331`; L-V.8 rule 5, L-V.19, L-V.20, L-V.24; L-0.24.

RIVALS: the judging profile `VA(k−1)` for the level — an order rests on the profile in force. The post-harvest
remainder only (TC11's twin) — the quoted law's remainder is "the position still open". A CI through the scorer — the
scorer rules arms of registered rows only (L-X.14). The level fill as the first column — the anchor to TC11's filed
arm needs TC11's fill law; the level fill is printed beside. Importing `tierc11_ride` — O-3.

FAILS-IF: F-TP-MIRROR (suite `scripts/tierc12_stage_r_fixtures.py --stage=TC12-R.tables`, transcript
`T12/stage_r/tables/FIXTURES_STAGE_R_tables.txt`): [a] IDENT — with every level absent the ride reproduces L-C's v6
book (`E.TP._book_sha` equal) and the `base` arm's rows at 0.000e+00; [b] ANCHOR — fed TC11's FILED 12h levels
(`MR/stage_h/tp_bars.parquet`, `scale_kind == "calibrated"`, `level` by `(symbol, entry_ms, bar_open_ms)`) on TC11's
corridor, the ride reproduces TC11's filed P-TP-RNG scored arm: canonical `book_sha256` (`tierc12_regbook.book_sha256`,
L-X.24) == `MR/regbooks/P-TP-RNG/scored.json["book_sha256"]`; a bar the ride asks for that the filed table lacks is
RED; [c] AS-OF — for every ridden bar, the level at bar `j` from `bars("1d", asof_close_ms=open_ms[j])` equals the
level of record; leans on F-VA-ASOF [d]; [d] the identity law on every unfilled campaign; [e] LEVEL-FILL —
`delta_r_level_fill == delta_r` on every campaign with `gap_tp == False`, and `tp_px_level` == the level of record of
the fill bar. Mutations: the 1d bar still forming read at `open_j` → [c]; TP before STOP, or the guard dropped → [b];
a freed slot re-admitted → [a], [d]; the level-fill column booked at `max(level, open)` → [e].

---------------------------------------------------------------------------------------------------------------
#### D · Build, pins, fixtures

**L-R.31 MODULES, STAGE ORDER, OUTPUTS, STAMPS** — "commit + PROGRESS.json per stage" (contract :5-6)

READING:
- **Modules** (O-1): `scripts/tierc12_rangewalk.py` (pure: `geometry`, `bar_step`, the walk and `fee_per_fraction`,
  with the declared switches of L-R.14 and L-R.19; imported by `tierc12_stage_r_sfp.py` and by `tierc12_scalp.py`);
  `tierc12_stage_r_dir.py` (P-DIR-1's regbook; the chop tables; the re-ride disclosure); `tierc12_stage_r_sfp.py`
  (P-SFP-VA-1's regbook, its twins, the event table); `tierc12_stage_r_tp1d.py` (the take-profit venue). **None is a
  door; each is a decision module with no exemption** (L-0.22): each reads value-area facts only as filed Stage V
  tables through the reader (L-V.2), and neither `analytics.value_area`, `analytics.profile` nor a door is in its
  import closure, or in `sys.modules` when its process exits. Levels are the filed values (L-V.24). The suite is
  `tierc12_stage_r_fixtures.py`: it imports no door and not `analytics.value_area`, and imports `analytics.profile`
  only as the referee of a hand derivation (L-0.22). The two-trades tables are not built here (Part C).
- **Sub-stages** (L-0.10's `SUBSTAGES_T`): three dotted children and the parent record, each with its own commit,
  each directory written by ONE builder and holding its own `build_manifest.json`, `READ_SET.json`, stage document and
  transcript:

  | record | `depends_on` | builder → directories | stage document · transcript |
  |---|---|---|---|
  | `TC12-R.dir` | `TC12-V`, `TC12-C`, `TC12-V.stamps.c`, `TC12-ENV.score-build` | `tierc12_stage_r_dir.py` → `regbooks/P-DIR-1/`, `stage_r/dir/` | `stage_r/dir/STAGE_R_dir.md` · `stage_r/dir/FIXTURES_STAGE_R_dir.txt` |
  | `TC12-R.sfp` | `TC12-V`, `TC12-ENV.score-build` | `tierc12_stage_r_sfp.py` (with `scripts/tierc12_rangewalk.py`, filed here) → `regbooks/P-SFP-VA-1/`, `stage_r/sfp/` | `stage_r/sfp/STAGE_R_sfp.md` · `stage_r/sfp/FIXTURES_STAGE_R_sfp.txt` |
  | `TC12-R.tables` | `TC12-V`, `TC12-C` | `tierc12_stage_r_tp1d.py` → `stage_r/tables/` | `stage_r/tables/STAGE_R_tables.md` · `stage_r/tables/FIXTURES_STAGE_R_tables.txt` |
  | `TC12-R` (the parent) | its three children | — | `stage_r/STAGE_R.md`, an index of three pointers; the L-0 suites run at its gate |

  The records are gated and committed in the order `TC12-R.dir` → `TC12-R.sfp` → `TC12-R.tables` → `TC12-R`; each
  child may START once every record through `TC12-V.stamps.c` and every record of its own `depends_on` is
  COMPLETE-VERIFIED (L-0.10's parallel set). The stage `TC12-R` is COMPLETE-VERIFIED iff the parent record and its
  three children are. Stage S starts only after `TC12-R.sfp` (it imports `tierc12_rangewalk.fee_per_fraction`), and
  the reader stamps this stage's books at `TC12-V.stamps.r` after `TC12-R.sfp` and `TC12-R.tables`.
  Inside `TC12-R.sfp` the builder's order is: the licence items (L-R.22) → the event disposition table → the book of
  record → the twins → the rides to PIN (the strip). The record is COMPLETE-VERIFIED only with F-SFP-MIRROR GREEN:
  the suite runs it as the first blocks of its transcript, on X's filed trades alone, and a RED mirror leaves the
  record PARTIAL and quarantines its regbook (L-0.4) — a book walked by an unproven mirror is never certified. No
  bootstrap is run in Stage R (L-0.10 T5).
  Compute: one process per sub-stage, no worker pool; fixture subprocesses run one at a time (O-5).
- **Outputs.**
  - `T12/regbooks/P-DIR-1/`: `STATUS.json`, `build_manifest.json`, and the arms `base`, `scored`, `strip` (L-R.4).
  - `T12/regbooks/P-SFP-VA-1/`: `STATUS.json`, `build_manifest.json`, and the arms `scored`, `strip`,
    `tierE__unfiltered`, `tierE__cell_1d`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__maker_assumed`,
    `tierE__x_geometry`, `tierE__x_gaplaw` (L-R.24). STATUS lists exactly the arms on disk (`[]` when the row is
    closed); every arm a spec names is written even when empty; each arm is `<arm>.parquet` + `<arm>.json`, written
    by `tierc12_regbook.write_arm` and no other writer. The sidecars, in L-X.24's keys:

    | arm | `kind` | `ruler` | `era_scope` | `lens` | `toll` | `fill_rule` |
    |---|---|---|---|---|---|---|
    | P-DIR-1 `base` / `scored` | `base` / `scored` | `two_sample` | `full` | `4h` | `taker` | null |
    | P-SFP-VA-1 `scored` | `scored` | `vs_zero` | `full` | `4h` | `taker` | null |
    | `tierE__unfiltered`, `tierE__guard_1d`, `tierE__x_geometry`, `tierE__x_gaplaw` | `tierE` | `vs_zero` | `full` | `4h` | `taker` | null |
    | `tierE__cell_1d` (adds `licence_pointers`, `licence_ok_by_era`) | `tierE` | `vs_zero` | `full` | `1d` | `taker` | null |
    | `tierE__maker_conditioned` | `tierE` | `vs_zero` | `full` | `4h` | `maker_entry_targets__taker_stop` | `tick` |
    | `tierE__maker_assumed` | `tierE` | `vs_zero` | `full` | `4h` | `maker_entry_targets__taker_stop` | `touch` |
    | `strip` (both regbooks; adds `n_by_arm`, `same_rows_as`) | `strip` | the scored arm's | the scored arm's | the scored arm's | the scored arm's | null |

  - `T12/stage_r/dir/`: `VA_CHOP.parquet`, `VA_CHOP_ALIGNMENT.parquet`, `VA_CHOP_MARGINS.parquet` (key `[cell]`);
    `VA_CHOP_ROWS.parquet` (key `[symbol, entry_ms]`); `dir_book_keys.parquet` (key `[book, symbol, entry_ms]`);
    `dir_reride_diff.parquet` (key `[gate, window, symbol, entry_ms]`); `STAGE_R_dir.md`; `build_manifest.json` (with
    `gate`, `reride`, `r5_overlap`, `ride_spec`, `roles_name`); `READ_SET.json`; the transcript.
  - `T12/stage_r/sfp/`: `SFP_EVENTS.parquet`, key `[lens, book, asset, entry_ms]` — one row per V2 swing failure per
    ridden book (`book` = the arm's name; `lens` = `4h`, or `1d` for `tierE__cell_1d`), from that book's ride to PIN:
    its `disposition` and `reasons_all`; its geometry (`e`, `stop_px`, `R`, `T1`, `T2`, `far`, `ext`, `atr`, `rr`,
    `t1_r`, `t2_r`, `r_atr`, `rail_binding`, `t1_void`, `t1_within_fee_band`, `fee_band_r`); the event's `side`, `E`,
    `from_state`, both return flags, `era`, `in_strip`; `symbol` (= `asset`, on every row: the column the stamp frame
    is read by); and, for a traded event, the instants of its ride — `entry_close_ms`, `exit_close_ms`,
    `ev_entry_ms`, `ev_t1_ms`, `ev_exit_ms`, `exit_event_stamp` (`open_of_bar` for a stop or T2; `close` for a time
    stop, an invalidation or the corridor end), `exit_reason`, `exit_px`, `open_at_asof`, `open_at_w`,
    `continued_past_w`, `continued_net_r` (L-R.21) — null on an event that did not trade. It carries no `net_r` of
    any arm. It is the frame the V5 stamps are taken from (below) and the ferry's per-event file. Also
    `STAGE_R_sfp.md`; `build_manifest.json` (with `time_stop_source` per lens); `READ_SET.json` (with
    `licence_reads`); the transcript.
  - `T12/stage_r/tables/`: the three `TP1D_*` tables (L-R.30); `STAGE_R_tables.md`; `build_manifest.json` (with
    `ride_spec`, `roles_name`); `READ_SET.json`; the transcript.
  - `T12/stage_r/STAGE_R.md` (the parent's index).
  Every regbook row carries L-X.24's twenty columns, in its order and dtypes; on the range arms (lanes `sfp-va-4h`,
  `sfp-va-1d`) also `funding_ceiling_bound` and `tc_series_net_r`; on the two maker twins also
  `taker_twin_haircut_net_r`; on `strip` also `arm`. P-SFP-VA-1's rows add `side`, `t0_i`, `bars_out`, `edge_px`
  (= `E`), `ext`, `atr`, `pivot_stop_px`, `rail_binding`, `T1`, `T2`, `far`, `val_f`, `poc_f`, `vah_f`, `t1_r`,
  `t2_r`, `r_atr`, `rr`, `T`, `time_stop_i`, `t1_i`, `t1_px`, `exit_i`, `exit_px`, `exit_event_ms`, `open_at_w`,
  `bars_held`, the gap flags, `both_touch_bars`, `stop_bar_open_through_target`, `n1`, `n2`, `funding_r_uncapped`,
  `t1_void`, `t1_within_fee_band`, `fee_band_r`, `inval_event_E`, `inval_edge_moved`, `n_stamps_inside_entry_bar`
  (and `n_stamps_inside_exit_bar` on the 1d cell), `stop_px_at_exit`, `n_entry_fills`, `from_state`, both return
  flags, `l_label`, `t_label`; `lane = "sfp-va-4h"` (`"sfp-va-1d"` on the 1d cell). P-DIR-1's rows carry `lane =
  "card"`.
- **Stamps (V5).** P-DIR-1's kept book files `stage_r/dir/dir_book_keys.parquet` (a key subset of `v6`, asserted,
  never re-stamped). The ridden range books and the take-profit venue's `tp` exits are stamped by `TC12-V.stamps.r`
  per L-V.19's table; this section files the frames and declares the kinds there listed. The frames: for
  `P-SFP-VA-1__<arm>`, arm ∈ (`scored`, `tierE__unfiltered`, `tierE__guard_1d`, `tierE__maker_conditioned`,
  `tierE__x_geometry`, `tierE__x_gaplaw`) — the `traded` rows of `SFP_EVENTS` with `book == <arm>`: lens 4h, key
  `[entry_ms]`, start `entry_close_ms`, end `exit_close_ms`; events `entry` (its close), `ev_t1` (`ev_t1_ms`, the OPEN
  of its bar, with a post-event twin), `exit` (`ev_exit_ms`, by `exit_event_stamp`: a stop or T2 at the OPEN of its
  bar with a post-event twin; a time stop or an invalidation at its close) and `as_of_pin` from `open_at_asof`. For
  `P-SFP-VA-1__tierE__cell_1d` — the same on lens 1d. For `tp1d` — the rows of
  `stage_r/tables/TP1D_CAMPAIGNS.parquet` with `exit_reason == "tp"`: the one event `ev_tp` (`ev_tp_ms`, the OPEN of
  its bar, with a post-event twin) and no other instant. `tierE__maker_assumed` shares `P-SFP-VA-1__scored`'s
  instants and is not stamped again. No builder of this section stamps a book, and no re-ride row is stamped.
- **Registry stamp**: every STATUS, sidecar and manifest carries `registry_head` and `registrations_sha256`
  (L-X.21).

SOURCE: O-1, O-5, O-6, O-29, O-31; L-0.4, L-0.9, L-0.10, L-0.13, L-0.22; L-V.2, L-V.19, L-V.24; L-X.21, L-X.24; L-L.25
(the ferry's typed list, by declared key).

RIVALS: a builder importing a door — forbidden: O-29. One module for the stage — the gate builder must stay provably
separate from the range builders, and one writer owns each directory (L-0.9). One transcript for the three
sub-stages — each record's transcript sha would move when the next sub-stage ran. A builder stamping its own book —
the stamps are Stage V tables, filed by the reader.

FAILS-IF: F-CLOSURE, F-NOT (L-0); F-KEY, F-DET, F-COLLAR per directory (`[stage_r/dir]`, `[regbooks/P-DIR-1]`,
`[stage_r/sfp]`, `[regbooks/P-SFP-VA-1]`, `[stage_r/tables]`); F-REGBOOK [P-DIR-1], [P-SFP-VA-1]; mutations: `import
tierc12_va` planted in a copy of the gate builder must turn F-CLOSURE RED; a door imported inside a function body of
a copy of the SFP builder and reached at run time must force exit 70 at the shim's exit check (L-0.22).

**L-R.32 THE PINS THIS SECTION CONSUMES** — "no number typed that a file can supply" (contract :8)

READING: Every constant of this section, the source read at run time, what it is asserted equal to, and its flow
witness (L-0.17). Rows marked ★ are rows of L-0's contract pin map, under the names L-0.17 fixes. The flow sample of
each pin is ONE row (`n = 1`), chosen by rule and not by a seed: the FIRST row, in key order, on which the pin binds;
where the book holds none (or its row is closed by precondition), the production function is fed the fixture's typed
synthetic event for that pin. Each bend prints `[FLOW] <pin> @ <door>: <witness> moved` (L-0.17).

| pin | read at run time from | asserted equal to | on file | consumer · witness when bent |
|---|---|---|---|---|
| ★ `sfp.rail_atr` | contract :71 `railed ≥ … ATR_4h`, pin door | the lineage rail `MIN_STOP_ATR` (`E.BK.MIN_STOP_ATR`, `tierc10_brk.py:510`; defined `tierc3_rules.py:148`) | 1.0 | `TC12-R.sfp` · `r_dist` of the first rail-bound row |
| ★ `sfp.t2_offset_atr` | contract :72 `− … ATR_4h (remainder)`, pin door | AST literal `T2_ATR_OFF`, `XR/scripts/tc11x_sfp.py:122` | 0.25 | `TC12-R.sfp` · `T2` of the first row |
| ★ `sfp.t1_fraction` | `E.TP.CONTROL_CARD.harvest_frac` (inside `account_l`) | contract :71 "half" (word map), pin door | 0.5 | `TC12-R.sfp` · `n1` of the first T1-filled row |
| ★ `rr_min` (veto "rr-min"; ONE pin for both range rows) | contract :73, also :100 and :135-136, pin door | — | 1.5 | `TC12-R.sfp`, `TC12-S` · the disposition of the event nearest the cut |
| ★ `chop.n_bands` | contract :68 "decile" (word map), pin door | the `range` argument of the `DECILES` generator, read by AST from `tierc11_stage_r.py:168` | 10 | `TC12-R.dir` · the band of the first campaign in a band the bend moves |
| ★ `tp1d.approach_atr` | contract :80 `… ATR_1d`, pin door | AST literal `APPROACH_ATR`, `tierc11_stage_h.py:133` | 0.25 | `TC12-R.tables` · the level of the first ridden bar with an order |
| ★ `two_trades.horizons` | X's `pins.laws.horizons` (`XR/tierc11x/va/build_manifest.json`) | contract :79 `H20/H100` (two groups), pin door; AST literal `HORIZONS`, `tierc10_census.py:123` | 20, 100 | `TC12-V.trades` (DOOR 2) · a term's anchor+H bar |
| ★ `scalp.fill_ticks` (veto "fill") | contract :94, also :136, pin door | — | 1 | `TC12-S`, and `TC12-R.sfp` for the maker-conditioned twin (L-R.24) · the fill of the first conditioned event whose child is through by less than the bent count |
| K, N, M, F, the lookbacks (L-V's rows `va.sfp_k`, `va.accept_n`, `va.accept_margin_atr`, `va.nest_frac`, `va.lookback.<lens>`), the null draw count, the floor | L-V.4's doors | L-V.4 | — | L-V.4 |
| `traverse.4h`, `traverse.1d` (fitted) | the reader's `traverse("traverse.4h")`, `traverse("traverse.1d")` — `va/TRAVERSE.json by_lens.<ℓ>.T_of_record` | F-TRAV [b] (L-V) | fitted | `TC12-R.sfp` · a time-stop exit bar |
| "beyond" `B` | `E.R5.STOP_BUF_ATR` (inside `spring_stop`; `tierc5_rules.py:115`) | — | 0.5 | `TC12-R.sfp` · `stop_px` of the first pivot-bound row |
| fee band `G` | `E.R2.FEE_BPS_ROUND_TRIP` (`tierc2_rules.py:123`) | AST literal `REFUSAL_BPS`, `tc11x_sfp.py:123` | 10.0 | the flag `t1_within_fee_band` and the arm `tierE__x_geometry`; witness: the flag of a planted event at the band's edge |
| `BPS_PER_UNIT`, `PCT_PER_UNIT` | `scripts/tierc12_units.py` (L-0.17) | L-0.17's `UNITS_T` | — | L-0.17 |
| taker, maker, slippage rates | `E.fees()[stem]` (TC12's fee file, L-D) | L-D's F-TOLL | — | `fee_r` |
| the tick | `E.ticks()[stem]` through `TickGrid` (L-D.23) | L-D's F-TICK | — | the conditioned twin's fill test |
| FLIP_HOLD margin, bars, TTL | `E.BK.FLIP_HOLD_MARGIN`, `.FLIP_HOLD_BARS`, `.MEM_TTL_BARS` | X's `pins.laws` | 1.0, 6, 400 | `TC12-V.trades` · the hold bar of the first retest |
| `ND` | X's `pins.laws.round_nd` | AST literal `ROUND_ND`, `tierc10_census.py:136` | 8 | `TC12-V.trades` · a `net` at the rounding edge |
| `MID_BAND` | AST literal, `scripts/tierc11_nest.py:109` | — | (25.0, 75.0) | `TC12-V.trades` · the `u_cell` of the first event at the band's edge |
| REPR tolerance | `E.LN.REPR_TOL` | — | 1e-9 | `TC12-R.sfp` · a planted child mismatch |
| W, PIN, era cut, seed, home panel | `E.TC11_PIN_MS`, `E.PIN_MS`, `E.ERA_CUT_MS`, `E.SEED`, `E.CLASSIC5` | L-D | — | — |

SOURCE: contract lines as cited; L-0.17, L-0.23 (the names, the register, the veto rows); the objects and literals at
the lines cited [read at drafting; the lines re-opened at revision].

RIVALS: typing any of them — forbidden. Reading the rail or "half" from the contract alone — the function that
applies them is the lineage's; the table says which object each run reads and the pin door holds the other equal.
A second name for the reward pin on the scalper's side — one pin, `rr_min`, one veto.

FAILS-IF: F-TYPED (L-0) on every L-R module; F-TYPED-FLOW [<pin>], one block per pin in the suite of each record that
consumes it (L-0.17): the pin bent at its door must move its witness, a bend that moves nothing is `PIN-NOT-READ`;
mutation: a pin replaced by a typed literal of equal value in a shadow copy of its consumer.

**L-R.33 THE FIXTURE ROLL OF THIS SECTION** — "FIXTURES (each states its failure condition)" (contract :114)

READING: one suite, `scripts/tierc12_stage_r_fixtures.py`, run as three invocations — `--stage=TC12-R.dir`,
`--stage=TC12-R.sfp`, `--stage=TC12-R.tables` — each filing its own transcript in its own directory (never a leg
filter); L-0.14's harness and leg law (one `prove` call and one block per leg; BREAK first; a plant caught only by
its named detector; PASS, FAIL and NOT RUN the three leg states; every stream `default_rng([SEED,
crc32("stage_r|<block id>")])`). The four two-trades fixtures are DEFINED in L-R.26-L-R.29 and HOSTED by L-V's suite
at `TC12-V.trades`.

| fixture | hosted at | FAILS IF | planted mutation that must turn it RED |
|---|---|---|---|
| **F-DIR** (contract) `[a]`-`[g]` | `TC12-R.dir` | L-R.7 [a]-[g] ([e] synthetic; the rest on P-DIR-1, which has no precondition) | L-R.7's list |
| F-CHOP | `TC12-R.dir` | a cell or margin of L-R.8 / L-R.9 does not re-derive from the rows table | quantile bands; a half-open top band; a refused key moved |
| F-GRID `[VA_CHOP]`, `[VA_CHOP_ALIGNMENT]` | `TC12-R.dir` | a declared cell missing, extra or duplicated; a partition sum off | a dropped `n = 0` row |
| F-REGBOOK · F-BASE-IDENT `[P-DIR-1]`; F-VA-PINS `[e · P-DIR-1]` | `TC12-R.dir` | L-X.24, L-X.25; the builder's VA reads differ from the spec's declared list | L-X's plants; an undeclared VA column read in a copy of the builder |
| **F-SFP** (contract) `[a]`-`[i]` | `TC12-R.sfp` | L-R.25 [a]-[i], and the identities named in L-R.10-L-R.24 (synthetic [g], [h]; real-book [a], [b], [c], [d], [f], [i]) | L-R.25's list |
| F-SFP-ASOF | `TC12-R.sfp` | the builder on a cut tape and cut filed tables differs from the filed row of a sampled event | `T2` from `ATR[i+1]`; an acceptance known after the cut used |
| F-SFP-MIRROR `[GEOMETRY]`, `[WALK]`, `[BOOKING]`, `[MAKER]`, `[SWITCH]` | `TC12-R.sfp` | the mirrored geometry, walk or booking under X's laws differs from X's filed X2 rows; a switch has a call site beyond the typed two | target-before-stop; the time stop one bar late; maker bps on a taker leg; the tier's gap law run on X's rows; a third call site |
| F-TRAV `[a · tierc12_stage_r_sfp]`, `[a · tierc12_rangewalk]`, `[e · <each ridden arm>]` | `TC12-R.sfp` | an integer literal reaches a time-stop or traverse name; a row's `T` differs from the door's value | a typed time stop; a row's `T` moved by one bar |
| F-REGBOOK `[P-SFP-VA-1]`; F-VA-PINS `[e · P-SFP-VA-1]` | `TC12-R.sfp` | L-X.24; the builder's VA reads differ from the spec's declared list | L-X's plants; a `1w_` column read in a copy of the builder |
| F-TP-MIRROR `[a]`-`[e]` | `TC12-R.tables` | L-R.30 [a]-[e] | a forming 1d bar read; TP before STOP; the guard dropped |
| F-TYPED-FLOW `[<pin>]` | the record that consumes the pin (L-R.32) | a pin bent at its door moves nothing | a typed literal of equal value |
| F-KEY · F-DET · F-COLLAR `[<directory>]` | each record, per directory | L-0.21, L-0.20, L-0.16 | L-0's plants |
| F-RETEST-MIRROR `[r1]`, `[r2]` | `TC12-V.trades` (L-V's suite) | L-R.26 [r1], [r2] | an off-by-one window; the hold window one bar short; the band pins |
| F-TWO `[a]`, `[b]`, F-TWO-MIRROR | `TC12-V.trades` | L-R.27's cells and label, or L-R.28's ledger, statistics and base-rate cells differ | U read at a forming bar; the forming 1w bar read; a one-row drop; a shortened horizon |
| F-NULL-MIRROR `[a]`, `[c]`, `[d]` | `TC12-V.trades` | L-R.29 [a], [c], [d]; `NULL-STRIP` | the seed shifted; the draw order changed; `keep_order=True`; a strip-dying regime's `die_i` used |
| F-GRID `[TWO_TRADES_*]` | `TC12-V.trades` | a declared cell missing, extra or duplicated; a partition sum off | a dropped `n = 0` row |

When P-SFP-VA-1 reads CLOSED_BY_PRECONDITION, its synthetic legs run unchanged and each real-book leg (F-SFP [a],
[b], [c], [d], [f], [i], F-SFP-ASOF, F-TRAV [e · …], F-REGBOOK [P-SFP-VA-1] and the directory legs on the closed
regbook) prints `CLOSED-NO-BOOK P-SFP-VA-1` and asserts the STATUS record — a PASS, never NOT RUN (L-0.14 C).

SOURCE: contract :114-124; L-0.14, L-0.19 (the hosting map and the name → block map).

RIVALS: one transcript for the stage — L-R.31. The two-trades fixtures in this suite — they would have to import a
door or the module, which no suite outside Stage V's may.

FAILS-IF: n/a (this reading is the roll).

---------------------------------------------------------------------------------------------------------------
#### E · Unverified at drafting — checked at build, each a HALT or a printed count

- UNVERIFIED: that each hand-walk category of F-DIR [b] and F-SFP [a] has a member, and that each population holds
  the contract's count. A category with no member prints `NONE-EXISTS` and its slot is FILLED; a short population is
  verified whole and printed `ONLY <n> EXIST (contract count 3)`; an empty T-POC or T-TIME is printed `FINDING: …`
  and carried to the report as a finding-not-fixed owned by the operator. None of these makes a leg RED (L-0.14 G).
- UNVERIFIED: that `E.BK.frame_l(stem, "1d")` under the TC12 shim is row-identical to `va_bars_1d`. Asserted;
  HALT `SFP-FRAME`.
- UNVERIFIED: that the V2 value regimes, cut at W, satisfy the three preconditions of the gaps+order box set on all
  ten cells. HALT `NULL-GAPS-ORDER-UNBUILDABLE` in DOOR 2, and then an amendment — never a relabel of X's null.
- UNVERIFIED: that `value_area.va_machine`, run at the pivot's three constants on constant-edge arrays, reproduces
  the filed machine columns of TC11's boxes outside the rounding band. F-NULL-MIRROR [c] lists every difference and
  is RED on one outside the band.
- UNVERIFIED: that `MR/stage_h/tp_bars.parquet` holds a row for every bar the mirrored ride reaches on TC11's
  corridor. F-TP-MIRROR [b] is RED on a missing bar.
- UNVERIFIED: that F-SFP-MIRROR's geometry re-derivation from X's filed box columns reproduces X's filed stops and
  targets at the write law on every row (it rests on the box edges being tape prices). A difference is RED at the
  `TC12-R.sfp` gate: the record stays PARTIAL, its regbook is quarantined and an amendment is proposed before any
  book walked by the mirror is certified.
- UNVERIFIED: that X's `die_parity` rows carry outcome columns on every `sfp` and `retest-hold` row at 4h and 1d
  (on file: all but four). F-TWO-MIRROR compares the rows that carry them and prints the count.
- UNVERIFIED: the count of v6 campaigns the gate refuses, and on how many home assets (L-X.7's REFUSAL SPREAD and
  panel clause decide the word and its qualifier).
- UNVERIFIED: how many refused campaigns sit in TC11 R5's two expansion cells (`r5_overlap`, L-R.6). A count, printed
  under the cell whatever it is.
- UNVERIFIED: that no two V2 swing failures of one (lens, asset) share a return bar. Asserted; HALT `SFP-EVENT-KEY`.
- UNVERIFIED: how many trades the D12 ceiling would have bound on (`funding_ceiling_bound`), and how many fills X's
  tick-less law would add to the conditioned twin (`x_law_extra_fills`). Counts, printed per arm.

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · P-DIR-1

- **id:** P-DIR-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1; two registrations stand under that header (:65, :69).
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :65).
- **mechanism:** A v6 trend entry taken while the 4h lens stands ACCEPTED outside value on the side opposite to the trade is an entry against a price the market has already accepted away from value in the other direction: the entry bar's 12/26 trigger fires inside a move the value-area machine reads as established against it. The gate removes those entries and nothing else. It is a statement about the STATE of value at the entry close (acceptance needs eight consecutive closes beyond the edge or one close a large multiple of ATR beyond it), not about distance, tide or range position; it is independently failable from P-SFP-VA-1, which trades a different event on a different book.
- **population:** the five home assets (contract :18); lens 4h; the base book = card v6 as TC11 filed it, every campaign (L-R.1); era of record the full corridor (no era is named; TC11 L-1.3); scored window per O-9: campaigns whose entry bar closes at or before TC11's pin, read by object from `research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`; campaigns entered in the forward strip are printed beside, unscored.
- **arms:**
  - `base` — the v6 book on the scored window, bit-equal on the sixteen regbook columns to TC11's filed v6 (canonical `book_sha256` == `research_outputs/tierc11/scores/BASE_IDENT.json["book_sha256"]["P-AGE-1"]`).
  - `scored` — the treated arm; two arms and no re-ride (O-21; L-R.4, L-R.5): `base` minus every campaign with `refuse == True`, where `refuse ⇔ (direction == +1 AND state == "ACCEPTED_BELOW") OR (direction == −1 AND state == "ACCEPTED_ABOVE")` and `state` is the filed 4h state after the entry bar's close: row `k = asof_index(4h closes, entry_close_ms)` of `research_outputs/tierc12/va/va_bars_4h.parquet`, with `close_ms[k] == entry_close_ms` asserted (L-R.2, L-R.3). Every other state — INSIDE, PROBING on either side, ACCEPTED on the trade's own side, UNDEFINED — is kept. Kept rows are identical to their base rows; no campaign is re-ridden.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm` (`base`: all of them; `scored`: those the same predicate keeps at their own entry close); rows and counts only.
  - inputs pinned: `research_outputs/tierc12/va/va_bars_4h.parquet` (certified by `progress/TC12-V.json`); the `base` arm (`regbooks/P-DIR-1/base.parquet`, certified by `progress/TC12-R.dir.json`; its book identity held to TC11's by F-BASE-IDENT); `research_outputs/tierc12/va/stamps/VA_STAMPS_v6.parquet` (certified by `progress/TC12-V.stamps.c.json`; the entry-row equality); `research_outputs/tierc11/stage_r/R5_CHOP_DIRECTION.parquet` (sha256 `a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`) and `research_outputs/tierc11/stage_r/NEST_v6.parquet` (each certified by TC11's progress record). These are HALT-grade pins, not closures: a pin that does not verify stops the build and prints no word.
  - VA columns read (declared for F-VA-PINS (e)): by the gate, from `research_outputs/tierc12/va/va_bars_4h.parquet` — `asset`, `close_ms`, `state`; printed only — `pct`, `edge_dist_atr`, `accept_age`, `armed_top`, `armed_bottom`, `L`, `l_label`; by the Tier-E chop tables of the same builder, deciding nothing, from `va_bars_4h.parquet` and `va_bars_1d.parquet` — `asset`, `close_ms`, `state`, `pct`, `val`, `vah`, `L`, `l_label`; from `va/stamps/VA_STAMPS_v6.parquet` — the `4h_` block of the `entry` rows, for the equality assertion only. No `1w_` column.
- **statistic:** `mean(net_r of the kept book) − mean(net_r of the whole v6 base)` (kept versus all, never kept versus refused).
- **comparison:** two-sample vs v6 (contract :65). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot_diff` with one asset pick per draw indexing both arms; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:** none — the gate trades no range and no licence word governs it; the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m = 0.10 ÷ 2 = 0.05, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. Asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. The exhaustive words of this row: SUPPORTED (a, b and c hold); NOT SUPPORTED (any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, TWO-SAMPLE-PREMISE when the gate refuses nothing, REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, 'CI wholly below zero' when hi < 0); CLOSED BY PRECONDITION is unreachable (no precondition). The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷ N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). A cell scored again after a dated refile, or on a regbook rebuilt after its first build, carries the scorer's refile or rebuild qualifier with the superseded line printed under it; neither changes the rule of the word. The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the five-cluster size footnote; the refusal spread; directly under the cell, the key overlap of the refused set with TC11 R5's two expansion cells, counts only; the refused cohort's n, mean and ΣR with ΣR of both books, and, iff mean(refused) > 0, 'on per-campaign expectancy only; the gate forfeits +X R total'. Tier-E arms carry no verdict word. This registration carries selection_hazard only and prints '<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)'.
- **labels:**
  - `selection_hazard` — tag: direction-informed; label: NOT CONFIRMATORY; text: "the direction of this gate (refuse an entry taken against an acceptance) was informed by TC11's R5 alignment table on this same v6 book and corridor, by pivot state: expansion aligned +0.491349 mean net R over 47 campaigns against expansion counter −0.493933 over 12; the value-area state itself was not tabulated against v6 outcomes in any filed table; new here are the detector and the interval"; items: `research_outputs/tierc11/stage_r/R5_CHOP_DIRECTION.parquet` (sha256 `a73b4894998e326a7264619ddd012f37bdf8c193fd512b90b082792c524846f1`), cells `calibrated|4h|alignment|EXP_ALIGNED` and `calibrated|4h|alignment|EXP_COUNTER`; `research_outputs/tierc11/stage_r/R5_CHOP.md:120-121`; contract :67.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves: `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`, `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`, `strip` (`n` per arm and one pointer).
  - Directly under the cell, counts only, no outcome: `n_refused` and, of those, the number in TC11 R5's `EXP_COUNTER` cell and in its `EXP_ALIGNED` cell (`research_outputs/tierc12/stage_r/dir/build_manifest.json` → `r5_overlap`; the pivot state at the entry instant from `research_outputs/tierc11/stage_r/NEST_v6.parquet`, calibrated 4h; L-R.6).
  - The refusal spread, counts only: `refused_n`, `refused_assets`, `p_draw_identically_zero`, `n_draws_exact_zero`.
  - The 4h lookback is tuning-fit (`l_label`: in-sample for tuning-era VA bars); the holdout slice is printed beside for that reason.
  - The re-ride disclosure counts and `stage_r/dir/dir_reride_diff.parquet` (L-R.5): `rival_count_rejection_log`, `reride_n`, `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`; no arm, no interval.
  - The with-vs-against acceptance table `research_outputs/tierc12/stage_r/dir/VA_CHOP_ALIGNMENT.parquet` (L-R.9), whose 4h ACCEPTED_AGAINST cell is the refused cohort; printed whole in the report's §0.2.
  - The full VA chop table `research_outputs/tierc12/stage_r/dir/VA_CHOP.parquet` — v6 by 4h and 1d state × fixed %-of-value band (L-R.8); printed whole in `stage_r/dir/STAGE_R_dir.md`.
  - Counts only, no outcome: the campaigns the prior-bar as-of reading would refuse instead; refusals with both sides disarmed; refusals whose entry close lies inside the rolling value area.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-DIR [a] set equality, post-filter identity and the key-subset law (plant: a refused campaign restored); [b] three refusals and two kept witnesses hand-verified by the frozen key-order rule, every refusal when fewer than three exist (plant: the sides swapped); [c] the as-of on the filed 4h table cut at the entry close (plant: the state read one row late); [d] the un-gated book must FAIL; [e] the synthetic truth table (plant: PROBING counted as ACCEPTED); [f] the re-ride identity (plant: a refused trigger that holds the slot); [g] the label's quoted cells and the overlap counts (plant: one digit changed).
  - F-BASE-IDENT, F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0).
  - F-CHOP and F-GRID on the two chop tables; F-CLOSURE with the gate builder in the decision set; F-VA-PINS (e); F-NOT leg 1W (no `1w_` column read by this builder).

### REGISTRATION SPEC · P-SFP-VA-1

- **id:** P-SFP-VA-1
- **family:** RANGE-STATE — the family name of the contract's STAGE R header (:64).
- **family_m:** 2 — parsed from contract :64 ("m=2") by L-X.1.
- **family_bar:** 0.05 — parsed from contract :64 ("bar 0.05"); asserted equal to q ÷ m with q = 0.10 parsed from :9.
- **prior:** 45 — parsed from the text slice ("[45%]", contract :69).
- **mechanism:** A probe beyond a value-area edge that closes back inside within three closes is a failed auction at that edge: the market tested prices outside value and did not accept them. Inside an unaccepted value area the next reference prices are the point of control and then the opposite edge, so the failure is faded toward them with a stop beyond the extreme the probe reached, a time stop at the lens's own edge-to-edge traverse, and an exit if the lens does accept beyond the faded edge after all. The trade needs no trend and no tide; it stands on the range being respected, which is what the value-area feasibility licence at 4h (taker) asserts. It is independently failable from P-DIR-1.
- **population:** the five home assets (contract :69-70), both directions pooled; lens 4h; every V2 swing failure at VAH or VAL (L-R.10); era of record the full corridor (contract :69) inside the scored window per O-9: trades whose entry bar closes at or before TC11's pin, read by object from `research_outputs/tierc11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`; a trade open at that instant is marked there (`corridor_end`) and listed OPEN; the forward strip is ridden and printed beside, unscored.
- **arms:**
  - `scored` — the one arm the ruler reads; no base (vs zero). Per swing-failure row of `research_outputs/tierc12/va/va_events.parquet` (lens 4h, kind `swing_failure`, the five home assets), in bar order per asset, four tests in this order, the first that fails naming the row's disposition: (1) one position per asset — an event at bar b is skipped iff `entry_i < b ≤ exit_i` of the trade open on that asset; (2) geometry; (3) rr-min; (4) the walk. ENTRY: `entry_px = e` = the close of the return bar, taker; direction = the event's sign (a failure at VAH short, at VAL long). STOP: `tierc10_brk.brk_stop` (= `tierc5_rules.spring_stop`) on `ext` = the probe's extreme including the return bar: long `min(ext − B·A, e − RAIL·A)`, short mirrored; `B` = `STOP_BUF_ATR`, `RAIL` = the contract's 1.0 (:71), `A` = ATR_4h of the return bar; `R = |e − stop|`, fixed for life. TARGETS, frozen at entry on the profile whose edge was probed, VA(t0−1): `T1` = its POC (`poc_f`), the card's harvest fraction ("half") off; `T2` = its far edge − d·0.25·A (contract :72), the remainder; both are touch-triggered taker exits booked at their level. GEOMETRY: Refused (geometry) iff the stop is undefined, or `d·(T1 − e) ≤ 0` (the POC is not ahead of the entry), or `d·(T2 − e) ≤ 0`. Not a refusal: `d·(T2 − T1) ≤ 0` voids T1 and the whole position exits at T2. Skipped (rr-min) iff `d·(T2 − e) / R < 1.5` (contract :73). A T1 within the round-trip taker fee of the entry price is traded as written and flagged. WALK on 4h bars from the bar after entry: a bar opening at or beyond the stop exits at the open; else the stop, adverse-first, at the stop price; then T1 at T1; then T2 at T2, same bar if reached; a target books its level with no gap improvement; then at the close the invalidation — the first V2 acceptance row of the 4h lens on the faded side — then the time stop at the close of bar `entry_i + T`, T the fitted 4h traverse read by object (`research_outputs/tierc12/va/TRAVERSE.json by_lens.4h.T_of_record`); a position still open at the last 4h bar closing at or before TC11's pin is marked at that close (`corridor_end`). No trail, no stop move, no tide read, no 5m bar. BOOKING: `tierc10_brk.account_l` on the 4h lens frame with T1 as the harvest slice; taker on every leg; interval-sum funding, uncapped (the D12 ceiling is a v6-card rule and is not a rule of this trade); `net_r = gross_r − fee_r − funding_r` in units of R.
  - `strip` — each ridden arm's own ride past TC11's pin: its trades with entry close after TC11's pin and at or before TC12's pin, per arm under the column `arm`; rows and counts only.
  - `tierE__unfiltered` — the scored construction without the rr-min skip and with nothing else changed (the three geometry refusals stand), re-walked with its own one-position sequence (contract :74).
  - `tierE__cell_1d` — the scored construction on the 1d lens (contract :74): V2 swing failures of lens 1d, ATR_1d, the fitted 1d traverse (`research_outputs/tierc12/va/TRAVERSE.json by_lens.1d.T_of_record`), the same constants; its sidecar carries pointers to the three era rows of the `1d|taker` licence and booleans, never the words.
  - `tierE__guard_1d` — the scored construction with one added refusal after the one-position test: the event is refused when the filed 1d state at the last 1d bar closed at or before the entry close is accepted against the trade (contract :75); re-walked.
  - `tierE__maker_conditioned` — the maker twin, fill-conditioned (contract :75): maker bps on entry, T1 and T2, taker on the stop, the time stop, the invalidation and the mark; the conditioned arm books only if the first 5m bar after the entry close trades through the entry price by the fill of record (one tick, exact); its maker targets fill by the same rule; otherwise a MISS, counted, never a trade.
  - `tierE__maker_assumed` — the scored arm's own walk and rows, re-booked at maker bps on entry, T1 and T2.
  - `tierE__x_geometry` — the scored construction under TC11-X's geometry law in place of this row's: an event is refused when T1 or T2 lies within the round-trip taker fee of the entry price or when T2 is not beyond T1, and no T1 is void; re-walked.
  - `tierE__x_gaplaw` — the scored construction under TC11-X's record gap law in place of this row's: the open decides first for stop and targets, a stop books the stop price through a gap, a target books the better of its level and the open; re-walked.
  - inputs pinned: `research_outputs/tierc12/va/va_events.parquet`, `research_outputs/tierc12/va/va_bars_1d.parquet`, `research_outputs/tierc12/va/TRAVERSE.json` and `research_outputs/tierc12/va/VA_MIRROR.json` (each certified by `progress/TC12-V.json`); `scripts/tierc12_rangewalk.py` (certified by `progress/TC12-R.sfp.json`, with F-SFP-MIRROR GREEN against TC11-X's filed `research_outputs/tierc12/x_rec/tierc11x/sfp/X2_trades_4h.parquet`, `X2_trades_1h.parquet` and `X2_twins.parquet`). These are HALT-grade pins, not closures: a pin that does not verify stops the build and prints no word.
  - VA columns read (declared for F-VA-PINS (e)): by the scored arm — from `va_events.parquet`, swing-failure rows: `lens`, `asset`, `kind`, `side`, `t0`, `i`, `bars_out`, `E`, `extreme`, `sgn`, `val_f`, `poc_f`, `vah_f`, `close_i`, `atr_i`, `known_close_ms`, `era`, `in_strip`, `ret_inside_frozen`, `ret_inside_rolling`, `from_state`, and for one printed count `val_n`, `poc_n`, `vah_n`; acceptance rows (the invalidation): `lens`, `asset`, `kind`, `side`, `i`, `E`, `known_close_ms`; from `va/TRAVERSE.json`, through the reader's `traverse` — `by_lens.4h.T_of_record`; from `va/VA_MIRROR.json`, through the reader's `licence` — the leaf `licence["4h|taker"].by_era["ALL"]`. By the Tier-E arms of the same builder — from `va_bars_1d.parquet`: `asset`, `open_ms`, `close_ms`, `close`, `atr`, `state`; the same event fields on lens 1d; `by_lens.1d.T_of_record`; the leaves `licence["1d|taker"].by_era` for `ALL`, `tuning` and `holdout`. No `1w_` column.
- **statistic:** `mean(net_r of the scored book)`.
- **comparison:** vs zero (contract :69). Bootstrap of record per O-22: whole-asset clusters; `N_BOOT` draws (on file 4000, `research_outputs/tierc11/scores/SCORES.json["n_boot"]`); `tierc5.cluster_boot`; the interval is `tierc5._ci_from`'s 5th / 95th percentile; `p = (#draws ≤ 0 + 1) / (N_BOOT + 1)` as a Fraction; seed 20261008 (contract :4) passed explicitly, the sensitivity seed (on file 20260816) printed beside.
- **preconditions:**
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector: licence["4h|taker"].by_era["ALL"].would_read, required: "PASS"} — the licence row of the row's own scoring era (O-17); the record quotes `research_outputs/tierc12/x_rec/tierc11x/va/feasibility.parquet` (sha256 `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0`) and computes nothing.
  - {record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector: licence_set, required: contains "4h|taker"} — the contract's word of record (:39-41).
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the draws) > 0 AND (b) one-sided p <= q ÷ m = 0.10 ÷ 2 = 0.05, exact, AND (c) every declared asset holds at least one row in every arm the ruler reads; else NOT SUPPORTED. Asset-cluster bootstrap by scripts/tierc12_score.py, T5 primitives, N_BOOT 4000, seed 20261008, sensitivity seed 20260816 beside. m is fixed in every case; a registration closed by its precondition prints 'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. The exhaustive words of this row: CLOSED BY PRECONDITION (a precondition item is not met; checked first, before any arm is built; no ruler is called; STATUS only, no arm; the cell reads 'CLOSED BY PRECONDITION (research_outputs/tierc12/va/VA_MIRROR.json#<selector> reads <found>; required <required>) — no number · no test spent'); SUPPORTED (the preconditions are met and a, b and c hold); NOT SUPPORTED (the preconditions are met and any of a, b, c fails; with the qualifier PANEL INCOMPLETE or EMPTY BOOK when c fails, 'CI wholly below zero' when hi < 0). A cell scored again after a dated refile, or on a regbook rebuilt after its first build, carries the scorer's refile or rebuild qualifier with the superseded line printed under it; neither changes the rule of the word. The contract pre-names no kill for this row. Printed beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices, LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored; the five-cluster size footnote; the licence words of the three eras; under the cell, the label's text with DISCLOSURES D-2 and D-3. Tier-E arms carry no verdict word. This registration carries pre_seen (KIN-SEEN) and prints '<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)'.
- **labels:**
  - `pre_seen` — tag: KIN-SEEN; label: NOT CONFIRMATORY; text: "TC11-X's X3 printed value-area swing-failure outcomes at 4h on these five assets for every bar at or before 2026-09-25T00:00Z before this row was drafted, and this trade form (stop, split targets, time stop, invalidation, minimum reward) was never scored; X's standing ledger line marks any later value-area registration pre_seen on those bars; the K = 3 and one-close-acceptance variants are among the printed tables"; items: `research_outputs/tierc12/x_rec/tierc11x/va/two_trades.parquet` (sha256 `a03ef1343cc93c9bc093c4f34960978daac51ca24d5160480546d40bf76f91b0`; detector `va`, trade `swing_failure`, variants `k3` and `die_parity`, lens `4h`); `research_outputs/tierc12/x_rec/tierc11x/va/X3.md`; `research_outputs/tierc12/x_rec/tierc11x/LEANS_X.md:1816-1818, :2468-2470`; `research_outputs/tierc12/DISCLOSURES.md` D-2, D-3.
- **disclosed_beside:** each Tier-E, no verdict word.
  - L-X.14's common leaves: `seed_sens`, `haircut` (the charter twin, TC11 AM-7), `haircut_sens`, `taker_twin` (on this all-taker arm it reads IDENTICAL TO THE RECORD), `taker_twin_haircut`, `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`, `strip` (`n` per ridden arm and one pointer); and one leaf `arm__<slug>` per Tier-E arm below — the row's ruler on that arm at the seed of record, an interval and no p, no bar, no word.
  - The holdout slice (contract :74), with the sentence "causal for the tuning-fit T and lookback only; the class was pre_seen; the era of record is the full corridor".
  - `tierE__unfiltered` — the book without the rr-min skip, re-walked with its own one-position sequence (contract :74).
  - `tierE__cell_1d` — the same law on the 1d lens (contract :74); the three era words of the `1d|taker` licence are printed in §0 beside the row, the arm's sidecar carrying pointers and booleans only; where the full-corridor word is not PASS the cell is labelled ERA NOT LICENSED there and its holdout slice is printed first.
  - `tierE__guard_1d` — the 4h book refusing an event when the 1d state at the entry close is accepted against the trade (contract :75).
  - `tierE__maker_conditioned` and `tierE__maker_assumed` — the maker twin (contract :75): maker bps on entry, T1 and T2, taker on the stop, the time stop, the invalidation and the mark; the conditioned arm books only if the first 5m bar after the entry close trades through the entry price by the fill of record (one tick, exact); the number of fills TC11-X's tick-less law would add is printed as a count; the feasibility word of the `4h|maker` pair is printed beside both.
  - `tierE__x_geometry` — the book under TC11-X's geometry law (its fee-band and inverted-targets refusals), re-walked, with the rows that differ from the record listed.
  - `tierE__x_gaplaw` — the book under TC11-X's record gap law (a stop at the stop price through a gap; a target at the better of its level and the open), re-walked, with the rows that differ from the record listed.
  - `research_outputs/tierc12/stage_r/sfp/SFP_EVENTS.parquet` — every swing failure of every ridden book with its disposition (`traded`, `one_position`, `stop_none`, `poc_not_ahead`, `t2_not_ahead`, `rr_min`) and geometry, the flags `t1_void` and `t1_within_fee_band`, and the continuation of each trade open at TC11's pin; counts only for the rivals not carried as books (the entry-time profile; re-entry at an intrabar exit close).
  - Disclosures on the row: the label's text; D-2 and D-3; "T tuning-fit (regime reading; the strict-INSIDE twin is printed in Stage V); in-sample for tuning-era trades"; the lookback label; `n_open_at_w`; the count of rows on which the card's funding ceiling would have bound, with the lineage's booking `tc_series_net_r` filed beside `net_r`; invalidation exits split by whether the accepted edge had moved from the faded one.
- **failure_conditions:** each a fixture leg with its planted mutation.
  - F-SFP [a] three trades hand-walked by the frozen key-order rule — the first POC fill, the first other time-stop exit, the first other stop; every trade when fewer than three exist (plant: T1 from the entry-time profile); [b] the row identities on every arm (plant: the invalidation ignored); [c] one position (plant: an overlapping trade); [d] the scored-window identity of the two rides and the strip, per ridden arm (plant: a T1 fill after TC11's pin on a scored OPEN row); [f] fees, uncapped funding and net (plant: the capped funding booked); [g] the synthetic geometry and same-bar sets (plants: a gap stop booked at the stop price; a target credited above its level; a void T1 refused); [h] the closed row on a planted licence leaf; [i] the guarded twin (plant: the 1d bar still forming read).
  - F-SFP-ASOF on cut tapes and cut filed tables; F-SFP-MIRROR against TC11-X's filed X2 trades under TC11-X's own laws, with the typed call sites of the two switches; F-TRAV (a), (e) (L-V); F-TYPED-FLOW on `sfp.rail_atr`, `sfp.t2_offset_atr`, `sfp.t1_fraction`, `rr_min`, `traverse.4h`.
  - F-FAM (PLANTED), F-REGBOOK, F-KEY, F-BOOT, F-VERDICT, F-SCORE-ANCHOR, F-GRID, F-DET (L-X, L-0); F-VA-PINS (e); F-CLOSURE with the builder in the decision set; F-NOT (no trail, no add, the edge is a VA edge, no 5m signal, no `1w_` column, the licence leg).

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **The lens above 1d.** (settled by O-28: the 1d two-trades are conditioned on the borrowed 1w block; O-28 is
   listed for the operator in the report's §9.)
2. **What "null gaps+order (R10)" means on a value area.** R10 is a pivot-box null. DEFAULT if silent: the
   gaps+order schedule is run on value regimes (L-R.29) and X's value-area null of record is printed beside, each
   row naming its null; if the box set cannot be built its builder HALTs (`NULL-GAPS-ORDER-UNBUILDABLE`) for an
   amendment. The operator may instead rule that X's null alone answers the clause.
3. **"Anchor entry".** DEFAULT if silent: every campaign of the v6 base (L-R.1). If a narrower population was
   meant, only the operator can name it; no narrower one exists on disk.
4. **The 1d cell's era.** The `1d|taker` licence passes on the holdout and fails on the full corridor and on
   tuning (O-17). DEFAULT if silent: the 1d cell is built on the full corridor like its parent row, labelled ERA
   NOT LICENSED there, with its holdout slice printed first. The operator may order it holdout-only.
5. **Three silences of the contract on P-SFP-VA-1, answered on the pessimistic side.** The contract does not say
   what happens when the POC is at or near the entry or beyond T2, when a bar opens through the stop or a target, or
   whether the card's funding ceiling applies to a range trade. DEFAULT if silent: an event is refused only when a
   target is not ahead of the entry, a T1 inside the fee band is traded and flagged, a T1 at or beyond T2 is void
   (L-R.14); a stop gapped through fills at the open and a target at its level (L-R.19); funding is booked uncapped
   (L-R.20). Each rival is printed beside and decides nothing — `tierE__x_geometry`, `tierE__x_gaplaw`, and
   `tc_series_net_r` with the count of rows the ceiling would have bound. Only the operator can order TC11-X's laws
   or the card's ceiling onto the record.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

- **L-0 (laws, process).** The contract pin map and the pin register take the ★ rows of L-R.32 under L-0.17's
  names: `rr_min` is ONE pin for both range rows (veto "rr-min"); `two_trades.horizons`; `scalp.fill_ticks` gains
  the consumer `TC12-R.sfp`. `FIVE_MIN_READERS_T` holds the directory `stage_r/sfp/` for the ONE read L-R.24 declares
  (the maker-conditioned twin's fill child and fill-bar walk). The four L-R modules are all decision modules (L-0.22: no
  exemption); none is on `VA_BLIND_T` (each imports the reader), none is in `ONEW_READERS_T` (none reads a `1w_`
  column), none holds a subprocess site. The sub-stage law, the record keys, one writer per directory and one
  transcript per record are L-0.9's and L-0.10's; the leg law, the block ids, the leg states, the hand-sample law
  and the fixture stream are L-0.14's; F-TYPED-FLOW is run per pin by the suite of the record that consumes it
  (L-0.17); `tierc12_progress.certified` is the one sha-first helper. The mirrors of `tierc10_null.schedule` and of
  the census outcome road (both in DOOR 2) are read from source TEXT; no range-machine module is imported, and this
  section references no attribute of `E.BK` or `E.LN` whose body lazily imports the range census, so L-0.30's
  PIVOT-RANGE leg needs no exception.
- **L-D (substrate, env).** `E.BK` (`frame_l` for 4h and 1d with funding, `account_l`, `funding_interval`,
  `brk_stop`, `MIN_STOP_ATR`, the three FLIP_HOLD pins), `E.T9._ride_leg9`, `E.T7._account_chain`, `E.T5.d15`,
  `E.TP.CONTROL_CARD`, `E.TP._book_sha`, `E.LN.REPR_TOL`, `E.R2.FEE_BPS_ROUND_TRIP`, `E.R5.STOP_BUF_ATR`,
  `E.TB._round_floats`, `E.fees()` (`taker_bps_side`, `taker_round_trip_bps`, `maker_bps_side`,
  `slippage_bps_side` per stem), `E.ticks()` with `TickGrid` (L-D.23: `dec`, `T`), `E.era_of`, `E.TC11_PIN_MS`,
  `E.PIN_MS`, `E.ERA_CUT_MS`, `E.SEED`, `E.CLASSIC5`, `E.D.load_asof(stem, lens)` (5m of the home assets),
  `E.load_asof_at(stem, iv, cut_ms)` (any instant at or before the pin), `E.tc11_record(rel)`, `E.x_rec(rel)`.
  `TC11_ALLOW_FILE` rows this section reads, all on the assembled list: `stage_r/R5_CHOP_DIRECTION.parquet`,
  `stage_r/R5_CHOP.md`, `stage_r/NEST_v6.parquet`, `stage_h/tp_bars.parquet`, `regbooks/P-TP-RNG/scored.parquet`,
  `regbooks/P-TP-RNG/scored.json`, `registrations/REGISTRATIONS.json`, `scores/BASE_IDENT.json`,
  `data/AS_OF_PIN.json` (and, for the fixtures L-V hosts at `TC12-V.trades`, `stage_r4/R4_NULL_BOXES.parquet`,
  `stage_r4/build_manifest.json`). `x_rec` rows: `tierc11x/sfp/X2_trades_4h.parquet`, `X2_trades_1h.parquet`,
  `X2_twins.parquet`, `tierc11x/va/events_va.parquet`, `va/two_trades.parquet`, `va/build_manifest.json`,
  `va/feasibility.parquet`, `pins/life_ranges.parquet`, `scripts/tc11x_sfp.py`, `scripts/tc11x_va.py`. The fee
  file's `maker_pin.x_assumed_bps_side` (L-D.19) is what F-SFP-MIRROR books X's maker rows at. AST-literal reads of
  frozen SCRIPT text (`scripts/tierc11_nest.py`, `tierc11_stage_h.py`, `tierc11_stage_r.py`, `tierc10_null.py`,
  `tierc10_census.py`) are permitted reads under the hook (L-D.27 names no read-never class on `scripts/`); none of
  those scripts is among the files TC12's own close acts move (L-0.24).
- **L-V (value area).** What Stage V files and this section reads, by L-V.24's inventory: `va_bars_<ℓ>` (key
  `[asset, open_ms]`; the columns `asset`, `open_ms`, `close_ms`, `close`, `atr`, `state`, `pct`, `edge_dist_atr`,
  `accept_age`, `armed_top`, `armed_bottom`, `val`, `poc`, `vah`, `val_j`, `vah_j`, `L`, `l_label`, the nest flags);
  `va_events` (key `[lens, asset, kind, side, i, t0]`; the L-V.14 fields, with no field that depends on a bar after
  `i`); `va_regimes` (a summary table, read only through `regimes(asof_close_ms=·)`); `TRAVERSE.json` (through
  `traverse(name)`; a 1d row with its `provisional` flag); `VA_MIRROR.json` (through `licence(lens, toll, era)`;
  `licence_set`; `beside.twin_words["4h|maker"]`); `va/stamps/VA_STAMPS_v6.parquet` (record `TC12-V.stamps.c`).
  DOOR 2 builds the `va/trades/` tables to the definitions of L-R.26-L-R.29 and L-V's suite hosts their fixtures at
  `TC12-V.trades`; the reader stamps this stage's books at `TC12-V.stamps.r` from the frames L-R.31 names. L-V's
  open asks, answered here: (i) no return flag is required (L-R.10); (ii) the frozen profile `*_f` sets POC and far
  edge (L-R.12); (iii) invalidation = the first acceptance row on the faded side (L-R.17); (iv) the retest scan is
  L-R.26; (v) the cells are L-R.27; (vi) the per-draw statistic and the gaps+order analog are L-R.29.
- **L-X (statistics, registrations, close).** The two REGISTRATION SPEC blocks are written to L-X.18's field
  grammar: the five checked fields carry the bare value first and, after a space, the contract line it is parsed
  from (no family number is typed); `preconditions` is `none — …` or brace items; `arms` holds exactly one sub-bullet
  beginning `` `scored` ``, with `inputs pinned:` and `VA columns read …` sub-bullets; `labels` holds one sub-bullet
  per key. The regbook interface is `scripts/tierc12_regbook.py` (L-X.24: `write_arm`, `write_status`,
  `write_manifest`, `validate_book`, `book_sha256`), its arms of record, twenty columns, conditional columns and
  empty-arm form; it accepts the extra columns of L-R.31. The scorer derives the common leaves and writes one
  `arm__<slug>` leaf per `tierE__` arm; the three templates of L-X.13 (by registration id) stand; the REFUSAL SPREAD
  (L-X.7) and the key-overlap line (L-X.13) are printed on P-DIR-1; §0.2 prints `VA_CHOP_ALIGNMENT` whole;
  `exit_reason = "corridor_end"` marks a position open at W; no scorer leaf exists for the take-profit venue
  (attached to no registered row) or for a re-ride.
- **L-C (control).** `tierc12_books`: `base_regbook_frame()` (the frame the `base` arm is written from);
  `v6_ext()` and `books/v6_ext_campaigns.parquet` with `segment` (the strip campaigns); `replay_h` and v6's arming
  log with its `reject` reasons; per campaign `entry_i`, `entry_px`, `stop_px`, `r_dist` for L-R.30's independent
  re-rides; the frames of the `v6` stamp table whose `entry` rows L-R.2 asserts against.
- **L-G (admission).** The hook is `tierc12_books.replay_h(…, refuse=<ctx predicate>)`; the re-ride is a
  disclosure of counts and diff rows on all three gates (L-G.18), with no arm.
- **L-S (scalper).** `rr_min` is one pin for both sections. One geometry law (OD-8), one gap law (OD-9), uncapped
  funding (OD-10) and one fill law for every maker row in the tier (OD-11). `tierc12_rangewalk.fee_per_fraction` is
  the one function; `scripts/tierc12_scalp.py` imports it, so Stage S starts after `TC12-R.sfp`.
- **L-L (ledger, era, ferry).** The ferry classes of this section's tables are typed in L-L.25 from the keys
  declared in L-R.31: the regbook arms, `SFP_EVENTS`, `VA_CHOP_ROWS`, `dir_book_keys` and `TP1D_CAMPAIGNS` are
  per-trade row files, `TP1D_SUMMARY` per-asset; `TP1D_BARS`, `dir_reride_diff` and the grids are pointed to; the
  grids are printed whole in their stage documents.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

OBJECTION O-11 — accepted as O-28.
