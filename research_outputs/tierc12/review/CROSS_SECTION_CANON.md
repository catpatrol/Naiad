# TIER-C12 · CROSS-SECTION CANON (the reconciler's pass on the LEANS review, 2026-10-09)

Inputs read whole: the contract (`exchange/queue/2026-10-08_TC12_APOLLO.md`, cited `:line`), ORCHESTRATOR_RULINGS O-1..O-32,
ORCHESTRATOR_DISPOSITIONS OD-0..OD-19, the 133 findings of `review/LEANS_REVIEW_2026-10-09.json`, the eight section drafts
under `leans_draft/`. No outcome of any book was computed; no `tierc10_*`, `tierc11_*` or `tc11x_*` module was imported or run.
Facts re-opened while reconciling are tagged [checked].

**How a section fixer uses this file.** Read (1) every CANON item whose PER-SECTION EDITS name your section, (2) the entries
of `review/DISPOSITIONS.json` whose `sections_to_edit` name your section, (3) your own draft. Where a canon text and a
finding's fix differ, the canon text is what you write. Where a canon text and your draft differ, the canon text replaces
the draft's. Names, paths, keys, column names, stage ids and strings below are exact: copy them.

**Precedence used wherever two findings disagreed:** contract text → rulings → dispositions → the pessimistic reading. Each
item says which was taken.

**No typed number.** This file types no constant of any book. Where a seeded leg needs a sample count, the OWNING reading
states it as a fixture-typed literal (L-0.14: the fixture's commission), preferring a count X filed for the mirrored leg
and naming that source (CANON-23 F).

**Abbreviations.** `T12` = `research_outputs/tierc12`; `T11` = `research_outputs/tierc11`; `XR` = `T12/x_rec`; `E` = the shim
`scripts/tierc12_env.py`; `W` = `E.TC11_PIN_MS` (the score edge); `PIN` = `E.PIN_MS`; `ERA_CUT` = `E.ERA_CUT_MS`.
"Record" = a file `T12/progress/<record id>.json`. "The reader" = `scripts/tierc12_va_stamps.py`.

**The scripts of record after this pass** (a name not on this list is not built; a name struck here is struck everywhere):

| section | non-fixture modules | fixture suites |
|---|---|---|
| L-0 | `tierc12_progress.py` (filed at R0), `tierc12_fx.py`, `tierc12_units.py`, `tierc12_pins.py`, `tierc12_frozen.py`, `tierc12_tables.py`, `tierc12_asof.py`, `tierc12_worktree_attest.py` | `tierc12_{resume,pins,closure,tables,attest,not,sweep}_fixtures.py` |
| L-D | `tierc12_data.py`, `tierc12_tick.py`, `tierc12_vendor.py`, `tierc12_env.py` | `tierc12_{data,env}_fixtures.py` |
| L-V | `analytics/value_area.py`, `tierc12_va.py` (DOOR 1), `tierc12_va_trades.py` (DOOR 2), `tierc12_va_stamps.py` (the reader) | `tierc12_va_fixtures.py`, `tierc12_va_stamps_fixtures.py` |
| L-C · L-G | `tierc12_books.py` · `tierc12_tide.py`, `tierc12_stage_g.py` | `tierc12_books_fixtures.py` · `tierc12_{tide,stage_g}_fixtures.py` |
| L-R | `tierc12_rangewalk.py`, `tierc12_stage_r_dir.py`, `tierc12_stage_r_sfp.py`, `tierc12_stage_r_tp1d.py` | `tierc12_stage_r_fixtures.py` |
| L-S | `tierc12_scalp.py` | `tierc12_scalp_fixtures.py` |
| L-L | `tierc12_forward_spec.py`, `tierc12_forward.py`, `tierc12_era.py`, `tierc12_pct.py`, `tierc12_ferry.py` | `tierc12_{forward,era,ferry}_fixtures.py` |
| L-X | `tierc12_registrations.py`, `tierc12_regbook.py`, `tierc12_score.py`, `tierc12_close.py`, `tierc12_close_acts_template.py`, `tierc12_tc11_stamp.py` | `tierc12_{registrations,score,close}_fixtures.py` |

STRUCK: `scripts/tierc12_stage_r_tables.py` (its work is DOOR 2's, CANON-02); the stage ids `TC12-REG.vendor`, `TC12-VENDOR`,
`TC12-D-MIRROR`, `TC12-V5`, `TC12-C.stamps`; the lists `RUNNERS_T`, `ACCESSORS_T`, `NEVER_RUNNER_T`; the arm
`tierE__reride` (CANON-22); the env name `TC11_LIST_DIRS`.

---------------------------------------------------------------------------------------------------------------
## CANON-01 · LABELS — three cell templates keyed by registration id
**Settles:** FID-01, STA-01, BLD-07, CMP-04 (i). **Authority:** OD-1, O-30. **Taken:** the disposition's keying (by
registration id) over FID-01's (key, tag), STA-01's `labels.<key>.form` and CMP-04's `kin` flag — none of those three is built.

**CANON TEXT.**

| registration | label key | tag | label | cell template (bytes of record) |
|---|---|---|---|---|
| P-ADM-1 | `pre_seen` | `none` | `IN-SAMPLE RE-SCORE, NOT CONFIRMATORY` | `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)` |
| P-BRD-1 | `selection_hazard` | `direction-informed` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)` · D-1 printed directly under the cell |
| P-DIR-1 | `selection_hazard` | `direction-informed` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)` |
| P-SFP-VA-1 | `pre_seen` | `KIN-SEEN` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)` |
| P-SCALP-3 | `pre_seen` | `KIN-SEEN` | `NOT CONFIRMATORY` | `<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed value-area swing-failure outcomes on these bars)` |

- The dash is U+2014 with one space each side; the dot is U+00B7; `direction-informed` is lower case (O-30's bytes).
- `<clause>` exists on P-ADM-1 ONLY: its `pre_seen.text` up to the first top-level `;`. The KIN-SEEN and selection_hazard
  templates have no slot.
- The owners' long `pre_seen.text` of P-SFP-VA-1 and P-SCALP-3 stays as the label's `text` and `items` and is printed UNDER
  the cell (in the row's `disclosures[]`) with D-2 and D-3 — for P-SCALP-3 including its sentence that the 1h maker licence
  row was measured on these same holdout bars.
- "re-score" (any case) appears in P-ADM-1's template and label alone.
- Detector `TEMPLATE` (filing and scorer): each filed `verdict_rule` carries exactly one substring `prints '<verdict> …'`,
  and that template equals this table's row FOR ITS REGISTRATION ID, byte for byte; HALT otherwise.
- F-REG `[TEMPLATE]` plants: P-ADM-1's template rewritten to the selection_hazard form → RED; P-SFP-VA-1's rewritten to the
  RE-SCORE form → RED; `DIRECTION-INFORMED` in capitals on P-DIR-1 → RED.

**PER-SECTION EDITS.**
- **L-X** — L-X.13: replace the table by the one above; replace the paragraph "Two templates, keyed on the label keys … the
  harsher template is taken because the label cannot flatter" by "Three templates, keyed by registration id (OD-1, O-30).
  RE-SCORE is printed only where the kept book's mean is on file (P-ADM-1). A label must be true."; "Mechanics": the
  TEMPLATE detector compares by registration id; RIVALS: replace the second rival by "the RE-SCORE template on the two
  lanes — not taken: O-30 (neither trade form was ever scored)"; FAILS-IF: the three plants above. The common table under
  "REGISTRATION SPEC · (none owned by L-X)": column "label keys" reads `pre_seen` / `selection_hazard (direction-informed) +
  D-1` / `selection_hazard (direction-informed)` / `pre_seen (KIN-SEEN)` / `pre_seen (KIN-SEEN)`. Common `verdict_rule`
  sentence: "… followed by exactly one `prints '<verdict> …'` template, the one L-X.13 fixes for the registration id."
- **L-G** — L-G.13 "Label": tag `direction-informed`. P-BRD-1 spec: `verdict_rule` last sentence "The row prints '<verdict>
  — NOT CONFIRMATORY (selection_hazard: direction-informed)'."; `labels` tag `direction-informed` (grammar: CANON-36).
  P-ADM-1's template and label are unchanged.
- **L-R** — L-R.6: tag `direction-informed`. L-R.23 first sentence: "P-SFP-VA-1 carries `pre_seen` with the tag KIN-SEEN
  (O-30) and prints L-X.13's KIN-SEEN template; its `pre_seen.text` below is printed under the cell with D-2 and D-3 and is
  not a clause of the cell."; its FAILS-IF mutation: "the template rewritten to the RE-SCORE form". P-DIR-1 spec:
  `verdict_rule` last sentence and `labels` tag in lower case. P-SFP-VA-1 spec: `verdict_rule` last sentence "This
  registration carries pre_seen (KIN-SEEN) and prints '<verdict> — NOT CONFIRMATORY (pre_seen · KIN-SEEN: X3 printed
  value-area swing-failure outcomes on these bars)'."; `labels`: tag `KIN-SEEN`, label `NOT CONFIRMATORY`, text and items
  unchanged. INTERFACE (L-X): "the two templates of L-X.13 stand" → "the three templates of L-X.13 (by registration id)
  stand".
- **L-S** — L-S.29 first sentence: "P-SCALP-3 carries `pre_seen` with the tag KIN-SEEN (O-30) and prints L-X.13's KIN-SEEN
  template."; RIVALS/FAILS-IF mutation: "the template rewritten to the RE-SCORE form". P-SCALP-3 spec: the `verdict_rule`
  sentence and the `labels` bullet as for P-SFP-VA-1.

---------------------------------------------------------------------------------------------------------------
## CANON-02 · THE WALL — two doors, one reader, no exemption
**Settles:** FID-02, BLD-01, CMP-03 (i), CAU-06 (class law), FID-09 (2), BLD-32, BLD-04, BLD-16 (the door of the fitted pin).
**Also cited by the dispositions of:** CAU-09, CMP-30. **Authority:** OD-2, O-29, contract :25-26, :124. **Taken:** OD-2's letter — DOORS_T is exactly two scripts (FID-02, BLD-01
and CMP-03 type one); DOOR 2 builds the Tier-E two-trades tables WHOLE, not only their null event rows (BLD-32's and
FID-09's split between a door and `tierc12_stage_r_tables.py` is not built); no suite outside Stage V spawns a door
(CAU-06's cut-mode subprocess is not built — CANON-03).

**CANON TEXT.**
1. **THE GLOB** = every `scripts/tierc12_*.py` whose stem does not end `_fixtures`.
2. **`DOORS_T = ("tierc12_va", "tierc12_va_trades")`**, typed in the closure fixture. They are the only GLOB members that
   import `analytics.value_area` or `analytics.profile`; each is EARNED (its source imports `analytics.value_area`); each
   imports `tierc12_env` first. A door writes Stage V tables and collared Tier-E tables only: DOOR 1 under `T12/va/`,
   DOOR 2 under `T12/va/trades/`. A door never writes under `regbooks/`, files no order, gate or score, files no table
   holding a column of `TRADE_COLS_T = (net_r, gross_r, fee_r, funding_r, entry_px, stop_px, exit_reason)`, and is imported
   by no module other than `tierc12_va_fixtures.py`.
   - **DOOR 1 `scripts/tierc12_va.py`** (record `TC12-V`): series, TPO twin, ATR, the V2 machine's states and events,
     regimes, the per-bar columns, the nest columns, the traverse legs and pin, `VA_PINS.json`, the mirror record,
     `va_stack`.
   - **DOOR 2 `scripts/tierc12_va_trades.py`** (record `TC12-V.trades`): the only place the V2 machine is run on permuted
     volume or on scheduled boxes — (a) the volume null of L-V.23; (b) the gaps+order@va_regime schedule and its box events
     (L-R.29), by `value_area.va_machine` on arrays held constant at each box's edges; (c) the Tier-E two-trades tables of
     L-R.26-L-R.29 (the retest scan, the outcome ledger, the base rate, the lens-above partition, the per-draw statistics).
     It reads Stage V's filed tables through the reader (sha-asserted) and the tapes through `E`. **L-R keeps the
     DEFINITIONS** (L-R.26..L-R.29); L-V carries the builder, the files and the record (L-V.2, L-V.23, L-V.24).
3. **The reader `scripts/tierc12_va_stamps.py` is NOT a door.** It is a DECISION module: data-only, it imports neither the
   module nor a door and recomputes nothing (API: CANON-12).
4. **Every other GLOB member is a DECISION module, with no exemption** — the P-SFP-VA-1, P-SCALP-3 and take-profit builders
   included. `RUNNERS_T`, `ACCESSORS_T`, `NEVER_RUNNER_T`, conditions (R-i)-(R-iii), "the accessor law" and every runner
   plant are deleted everywhere. No decision module carries a copy of the V2 machine, a profile, or an acceptance /
   swing-failure / lapse test. A consumer may compare a price with a filed LEVEL; it never re-derives a lens STATE or EVENT.
5. **`VA_BLIND_T`** (typed; a member may not import the reader nor open a path under `T12/va/`; proven by AST and from its
   directory's `READ_SET.json`, CANON-28) = `tierc12_books, tierc12_tide, tierc12_stage_g, tierc12_data, tierc12_env,
   tierc12_vendor, tierc12_tables, tierc12_asof, tierc12_pins, tierc12_units, tierc12_tick, tierc12_registrations,
   tierc12_forward_spec, tierc12_era, tierc12_pct`.
6. **`VA_MODULE_FIXTURES_T = ("tierc12_va_fixtures",)`** — the only `_fixtures` module that may import
   `analytics.value_area` or a door. Any `_fixtures` module may import `analytics.profile` (the house function, frozen
   estate) as an independent referee of a hand derivation; no non-fixture module but a door may.
7. **The closure legs** (`F-CLOSURE`, `F-HOOK-ESCAPE`, `F-WALL`):
   - (i) FRESH INTERPRETER, one per decision module: after `import <module>`, `sys.modules` holds no
     `analytics.value_area`, no `analytics.profile`, no `DOORS_T` name, no forbidden name.
   - (i-b) **EXIT.** The shim registers an exit check (L-D.26 hunk 7, code) in every process that imports it. At exit,
     with `stem` = the stem of `sys.modules["__main__"].__file__` (a spawn worker inherits its parent's): if `stem ∉
     DOORS_T ∪ VA_MODULE_FIXTURES_T` and `sys.modules` holds `analytics.value_area` or a `DOORS_T` name — or `stem` does
     not end `_fixtures` and `sys.modules` holds `analytics.profile` — the hook logs `BLOCKED:va-wall <name>` and forces
     exit 70.
   - (ii) AST as drafted, plus the TC10 clause: modules named `tierc10_*` are TC10's layer — DISCLOSED (name, path, sha
     from `T12/env/LINEAGE_PINS.json`) and NOT WALKED for forbidden imports. The function-local range imports they hold
     [checked: `scripts/tierc10_brk.py:2357`, `:2380`, `scripts/tierc10_lanes.py:1246`, each `import tierc10_census as C`]
     are typed `TC10_LAZY_RANGE_T` by (module, enclosing function name), and the fixture FAILS IF the AST's set differs
     from the typed one. Coverage clause: every repo module a fresh interpreter loaded is in the walk or in the disclosed
     TC10 layer.
   - (iii) DATA-ONLY: outside `DOORS_T` no GLOB source holds an `ast.Name` id or `ast.Attribute` attr equal to
     `volume_profile`, `value_area`, `va_series`, `va_machine`, `va_columns`, `va_traverse`, `va_coincidence` or
     `null_volume`.
   - (iv) HOOK-ESCAPE with `SUBPROC_SITE_T` of CANON-29. (v) THE ANALYTICS WALL as drafted.
   - Plants (the runner plants are replaced by): a P-SFP builder copy importing `tierc12_va` → (i) RED; a scalper copy
     importing `analytics.value_area` inside a function body → (ii) RED; a shadow builder with a run-time lazy door import,
     run as a subprocess → exit 70 at (i-b); a `tierc12_books` copy importing the reader → `VA-BLIND` RED; a decision-module
     copy holding the name `va_machine` → (iii) RED; a third module importing `analytics.value_area` that is not typed in
     `DOORS_T` → RED; a door copy without its import → UNEARNED; a DOOR 2 copy writing under `regbooks/` → RED; a door
     table copy with a `net_r` column → RED.
8. **F-NOT, PIVOT-RANGE:** "No TC12 module — no door either — imports the range machine"; FAILS IF a TC12 source references
   an attribute of `E.BK` or `E.LN` whose function body holds one of `TC10_LAZY_RANGE_T`.

**PER-SECTION EDITS.**
- **L-0** — L-0.22: replace the READING's class law (from "value-area state enters decision code only as DATA" through the
  NEVER_RUNNER_T sentences) by points 1-6; replace the five legs by point 7; RIVALS: (b) FILE-ONLY becomes the reading
  ("the round trap is answered by L-V.24: the filed value is the level of record"); the runner form becomes "not taken:
  O-29"; FAILS-IF: point 7's plants. L-0.25 FAILS-IF: strike "or a runner calls an accessor with the 1w lens" (and apply
  CANON-04). L-0.30 PIVOT-RANGE: point 8. INTERFACE: the L-V bullet reads "the two door scripts (`tierc12_va.py`,
  `tierc12_va_trades.py`) are `DOORS_T`; `tierc12_va_stamps.py` is the data-only reader, a decision module; the Tier-E
  two-trades tables are DOOR 2's and hold no `TRADE_COLS_T` column"; strike the accessor law, the `TC12-V5` sentence
  (CANON-10) and "L-R and L-S name which of their modules are RUNNERS … or declare"; the orchestrator bullet: "assembles
  `DOORS_T`, `VA_BLIND_T`, `FIVE_MIN_READERS_T`, `REGISTERED_TABLES_T`, the pin map and the pin register". L-0.11 SOURCE
  unaffected.
- **L-D** — L-D.26 hunk 7: add "and registers the VA-wall exit check of L-0.22 (i-b): typed tuples `VA_WALL_DOORS`,
  `VA_WALL_FIXTURES`; `BLOCKED:va-wall`; exit 70". L-D.29: add "This pinning walk does not stop at the TC10 layer; it is a
  different walk from F-CLOSURE's, which discloses the TC10 layer and does not walk it (L-0.22 (ii))." L-D INTERFACE
  (L-V): "imports `analytics.value_area` only AFTER the shim and only from the two door scripts".
- **L-V** — L-V.2: "The door" becomes two bullets, DOOR 1 and DOOR 2, in the words of point 2; the reader bullet per
  CANON-12 (incl. its sha law); RIVALS (d) "a second door for the stamps — not taken" stays; add "(e) the two-trades
  tables in a decision module with a mirrored box machine — not taken: OD-2". L-V.23: the generator and its draws run in
  DOOR 2; files under `va/trades/` (CANON-11); F-VA-NULL is hosted at `TC12-V.trades` (CANON-24). L-V.24: outputs table
  per CANON-11; compute plan gains DOOR 2's line. INTERFACE "To L-0": "the typed door list is exactly two members".
- **L-R** — L-R.26: "mirrored into `scripts/tierc12_stage_r_tables.py` and run OUTSIDE the door" → "built by DOOR 2,
  `scripts/tierc12_va_trades.py` (L-V.2), on the filed `acceptance` rows and the tape"; files under `T12/va/trades/`.
  L-R.27, L-R.28: the builder is DOOR 2; paths `va/trades/…`. L-R.29: "The machine on a box" bullet → "`value_area.va_machine`
  with (N, M, K) on arrays held constant at each box's edges, run by DOOR 2 — the one V2 machine; no mirror of
  `static_box_machine` is written"; files per CANON-11; last line "No module of the range machine is imported … mirrored"
  keeps the schedule mirror only; F-NULL-MIRROR: leg (b) deleted, legs (a), (c), (d) hosted in `tierc12_va_fixtures.py
  --stage=TC12-V.trades` (leg (c) runs `va_machine` at the pivot's three constants). L-R.31: Modules list = the four of
  the table above ("None is a door; each is a decision module with no exemption"); strike `tierc12_stage_r_tables.py` and
  "none is a runner"; RIVALS: "a builder importing a door — forbidden: O-29"; FAILS-IF mutation stays. L-R.4: "(L-0.22
  `NEVER_RUNNER_T`)" → "(L-0.22: no exemption)". P-DIR-1 spec `failure_conditions`: "F-CLOSURE with the gate builder in
  the decision set". INTERFACE (L-0): delete difference (i); "none is added to `RUNNERS_T`, and `tierc12_stage_r_dir.py`
  is in `NEVER_RUNNER_T`" → "all are decision modules".
- **L-S** — L-S.1 RIVALS: "a RUNNER that asks the door for arrays (L-0.22's other form)" → "a builder importing a door —
  forbidden: O-29". INTERFACE (L-0) "Class of the builder": replace the paragraph by "`scripts/tierc12_scalp.py` is a
  decision module that reads filed columns through the reader (O-29); there is no runner class."
- **L-C** — L-C.4: "(a DECISION module under L-0.22: it imports no door, no runner and nothing of the value area)" → "(a
  DECISION module on `VA_BLIND_T`, L-0.22)". L-C.11 RIVALS: strike "whichever way L-0.22 classes that reader
  (INTERFACE)"; FAILS-IF plant: "an import of the stamps reader in a copy of the builder → `VA-BLIND` RED".
- **L-G** — head note: "Both are DECISION modules on `VA_BLIND_T` (L-0.22)". INTERFACE (L-0) "A second conflict": replace
  by "`tierc12_va_stamps.py` is the data-only reader and not a door (L-0.22); neither `tierc12_books.py` nor
  `tierc12_stage_g.py` imports it."
- **L-L** — L-L.16: "(L-0.22 `NEVER_RUNNER_T`)" → "(L-0.22)". INTERFACE (L-0): "none is a door or a runner" → "none is a
  door". L-L.20: unchanged (`tierc12_era`, `tierc12_pct` are on `VA_BLIND_T`).

---------------------------------------------------------------------------------------------------------------
## CANON-03 · CUT-TAPE LEGS AND PREFIX IDENTITY
**Settles:** CAU-05 (i)-(iii), CAU-06 (the as-of legs), CAU-07, CAU-08 (the cuts), FID-09 (1). **Also cited by the dispositions of:** CAU-04, BLD-12, CMP-03. **Authority:** OD-2 ("no suite
outside Stage V imports or spawns a door … every downstream as-of leg cuts the FILED tables by `known_close_ms ≤ cut`").
**Taken:** the disposition over CAU-06's cut-mode subprocess and over FID-09's child `TC12-V.asof-r` (neither is built).

**CANON TEXT.**
1. **Stage V's suite owns PREFIX IDENTITY** (`tierc12_va_fixtures.py --stage=TC12-V`, F-VA-ASOF):
   - `[a PREFIX]` as drafted, the plant window `t−L+2 .. t+1` CLIPPED at the tape end (X's form).
   - `[d FILED-ROW PREFIX]` (replaces "MACHINE PREFIX"): for every cut `c` in `CUTS_V` = the seeded cuts of [a] ∪ {for the
     first acceptance and the first swing failure of each (cell, era): the closes of bars `i − 1` and `i`} ∪ {`ERA_CUT`} ∪
     {`W`}: DOOR 1's tables rebuilt on tapes cut at `c` (fresh arrays, `E.load_asof_at(stem, lens, c)`; 1d and 1w
     re-derived from the cut 4h by Stage D's law) equal the FILED tables restricted to `c` — every column of every
     `va_bars_<ℓ>` row with `close_ms ≤ c`, every `va_events` row with `known_close_ms ≤ c`, and
     `regimes(asof_close_ms=c)` — at the write law.
   - `[e IDENTITY]` on every row of every `va_bars_<ℓ>`: `(val_j, poc_j, vah_j)[t] == (val, poc, vah)[t−1]` exactly, and
     `atr[t] ==` Round6 of the fixture's own Wilder loop at `t`. Plants: the in-force block shifted one row forward in a
     copy of the door's table assembly; ATR taken at `t+1`.
   - F-VA-RAW `[c]` compares the FILED rows: `val, poc, vah, val_edge, vah_edge, tpo_*` of `va_bars_<ℓ>` at every row
     closing ≤ `W` of X's 20 cells == X's filed `va_series_<ℓ>` row `i`.
   - F-TRAV `[d]`: the leg table rebuilt on fresh tapes cut at `ERA_CUT` == the filed tuning legs, row for row.
2. **Every other suite** proves as-of by cutting FILED data and re-running its own production function:
   - the Stage V tables through the reader: `bars(lens, asof_close_ms=c)`, `events(asof_close_ms=c)`,
     `regimes(asof_close_ms=c)` (CANON-12);
   - the tapes through `E.load_asof_at(stem, iv, c)` (fresh arrays, never a symbol-keyed memo);
   - the consumer's production function on those inputs must reproduce its filed output for every row decided at or
     before `c`;
   - the leg's transcript carries the fixed line `leans on F-VA-ASOF [d]: a filed row at bar k equals a door rebuild on
     tapes cut at close_k`;
   - plants sit inside the consumer's production: a row `k + 1` read; an event with `known_close_ms` after the cut used.
3. **F-NEST-ASOF at TC12-V** runs `[a]`-`[c]` on instants that need no book: per home asset, a tier-seeded draw of 5m-grid
   instants in each of tuning / holdout / strip, of 4h bar closes and of 4h bar opens, plus the boundary set of `[b]`
   (counts stated in L-V). P1 = "`up_k + 1`, NULL where it passes the tape end"; P2 = "a 1d (1w) bar synthesised from the
   4h bars of the current incomplete day (week) and filed with `close_ms` = the instant τ (a forming bar published as
   closed)". The per-book instances are CANON-10's.

**PER-SECTION EDITS.**
- **L-V** — the fixture roll: F-VA-ASOF `[a]`, `[d]`, `[e]`, F-VA-RAW `[c]`, F-NEST-ASOF `[a]` and plants P1, P2 in the
  words above; L-V.8 FAILS-IF follows. F-STATE `(d)` = F-VA-ASOF `[d]`.
- **L-R** — L-R.7 (c): "For every base campaign, the gate's production predicate fed the FILED `va_bars_4h` cut at τ
  (`bars("4h", asof_close_ms=τ)`) returns the decision of record, and the last row of that cut has `close_ms ==
  entry_close_ms`; leans on F-VA-ASOF [d]." Plants in L-R.7: "the state read at row k+1 → (c), (e)" stays. L-R.25
  F-SFP-ASOF: "for a seeded sample of events per asset (both eras, both sides; count stated): the builder run on the 4h
  tape cut at the event's `known_close_ms` and on `events(asof_close_ms=·)` / `bars(…, asof_close_ms=·)` reproduces `(e,
  stop, R, T1, T2, disposition, rr)` exactly; `T` held at its filed value; leans on F-VA-ASOF [d]." L-R.30 (c): "the level
  at bar `j` from `bars("1d", asof_close_ms=open_ms[j])` equals the level of record". No Stage R leg re-runs a door.
- **L-S** — L-S.31 (e2) becomes "ACT-BOUNDARY PREFIX. Sample, by a rule frozen here: per home asset, the first 3 orders of
  each status (filled / expired / cancelled) in each era in key order, plus a tier-seeded draw of N more (N stated here).
  For each sampled order, three cuts: at its `known_at_ms`; at its resolution close (fill / expiry / cancel); at its exit
  close. On the 5m tape cut at each instant (`E.load_asof_at`) and the 1h / 4h tables cut at the same instant through the
  reader, the builder must reproduce: at `known_at_ms`, the order's gates and frozen geometry exactly with status
  `unresolved_at_end`; at the resolution close, the status and the fill bar; at the exit close, the whole trade row. Leans
  on F-VA-ASOF [d]. Plants inside production: row `k1 + 1`; a fill accepted on `t+V+1`; an acceptance with
  `known_close_ms` after the cut used; an EMA seeded at the cut." (e1) and (e3) stay.

---------------------------------------------------------------------------------------------------------------
## CANON-04 · THE 1w LENS — two reads, both Tier-E
**Settles:** FID-05, FID-06, CAU-01, CAU-02, BLD-08, CMP-05, TRD-06, CMP-03 (ii). **Authority:** OD-3, O-28. **Taken:**
OD-3's column name and string (`u_lookback_label`) over `u_label` (BLD-08, CMP-05) and `lens_above_label` (TRD-06); the
eight-cell partition UNCHANGED (OD-3, FID-05, CAU-01) over "NA holds events with no 1w bar closed" (BLD-08, CMP-05, TRD-06):
that case is cell `UNDEFINED`, as the partition already says; the typed module is DOOR 2 (CANON-02), not
`tierc12_stage_r_tables.py`.

**CANON TEXT.**
1. The 1w value area is built on the 1d pin's bar count (L-V.5; `VA_PINS.json by_lens.1w`, `source_lens = "1d"`, label
   `BORROWED: the 1d pin's bar count; X pinned no 1w lookback; not X's law at 1w`).
2. It is read in EXACTLY TWO places, both Tier-E: (R1) the V5 stamp columns (the `1w_*` block the reader files in
   `va/stamps/VA_STAMPS_<book>.parquet`); (R2) the lens-above conditioning axis of the 1d rows of the two-trades tables.
   It is read by no gate, no permission, no direction guard, no licence, no time stop, no order and no registered
   construction. No 1w range cell, trade, traverse row or feasibility row exists.
3. **R2, exactly.** For a 1d event with known-at close τ: `U = 1w`; U's block is the reader's stamp at τ — row `k =
   asof_index(close_ms_1w, τ)` of `va_bars_1w`: the last COMPLETE Monday-anchored derived week whose close ≤ τ (a week
   still forming is never read; on a Monday 00:00Z close the week closing at τ IS read, O-14). Columns read, and no
   other: `1w_state`, `1w_val`, `1w_vah`, `1w_pct`, `1w_bar_close_ms`. The eight-cell partition of L-R.27 applies
   unchanged, the coincidence unit being `F·ATR_1d[k_event]`; `UNDEFINED` holds a 1d event whose U state is UNDEFINED or
   for which no 1w bar has closed; `NA` has no member at either lens and is printed as a row with `n = 0`, `nan_reason =
   "absent by construction: every lens of the table has a lens above (O-28)"`. L-R.28's base rate (ii) at 1d reads 1d's own
   nest flag against 1w at `close_k`.
4. Every 1d row of `TWO_TRADES_EVENTS`, `TWO_TRADES_VA`, `TWO_TRADES_BASE`, `TWO_TRADES_NULL` and
   `TWO_TRADES_NULL_DRAWS` (the tables that carry the lens-above cell) carries `u_lookback_label = "BORROWED: the 1d pin's bar count; X pins no 1w lookback"` (4h
   rows: the empty string).
5. `ONEW_READERS_T` (typed in F-NOT by (module, table)) = ((`scripts/tierc12_va_stamps.py`,
   `va/stamps/VA_STAMPS_*.parquet`), (`scripts/tierc12_va_trades.py`, `va/trades/TWO_TRADES_*.parquet`)).
6. **F-NOT leg 1W** FAILS IF (a) a table holding a `TRADE_COLS_T` column, an order column or an event-outcome column has a
   row whose OWN lens is 1w; (b) a registered row's declared VA columns hold a `1w_` column; (c) any GLOB module outside
   `ONEW_READERS_T` reads a `1w_` column (AST: a string constant matching `^1w_`, or the lens literal `"1w"` handed to
   `bars`, `events`, `regimes`, `licence` or `traverse`; plus each stage's declared VA read list); (d) DOOR 2 reads a
   `1w_` column outside the five named, or writes a 1w-derived value into a table other than the `TWO_TRADES_*` set.
   Plants: a condition on `1w_state` added to a copy of the P-DIR-1 gate → RED; a 1w column read by a copy of the
   P-SFP-VA-1 builder → RED; a sixth 1w column read by a copy of DOOR 2 → RED; a 1w row added to a range-table copy → RED.
   F-TWO `[a]` gains the plant "the 1w bar still forming at τ read → RED".

**PER-SECTION EDITS.**
- **L-0** — L-0.25 (iii): "The 1w block (built on the 1d pin's bar count, labelled BORROWED, O-28) is read in exactly two
  places, both Tier-E: the V5 stamp columns, and the lens-above conditioning axis of the 1d two-trades tables (L-R.27).
  It is read by no gate, no permission, no direction guard, no licence, no time stop, no order and no registered
  construction."; RIVALS: the "for completeness" rival stays for 1w's OWN cells; FAILS-IF: point 6 with `ONEW_READERS_T`.
- **L-R** — L-R.27 "L = 1d" bullet: point 3 and point 4 verbatim; the table row `NA`: "no conditioning lens — empty by
  construction at both lenses (O-28)"; FAILS-IF mutation: "a 1w column read by a copy of the P-SFP-VA-1 builder (must also
  turn F-NOT leg 1W RED)". L-R.28 (ii), L-R.29 "Conditioning": follow point 3. OPEN TO OPERATOR 1: replace its text by
  "(settled by O-28: the 1d two-trades are conditioned on the borrowed 1w block; O-28 is listed for the operator in the
  report's §9.)" — the item keeps its number. OBJECTIONS: replace the O-11 block by the one line "OBJECTION O-11 —
  accepted as O-28." INTERFACE (L-0): delete difference (ii). The two registration specs keep "No `1w_` column".
- **L-V** — L-V.5: "a STAMP-ONLY, Tier-E column block (O-11)" → "a Tier-E column block read in exactly two places (O-28):
  the V5 stamp columns and the lens-above axis of the 1d two-trades tables"; FAILS-IF unchanged. OPEN TO OPERATOR 1: the
  default text reads "…labelled BORROWED, read in exactly two places, both Tier-E (O-28)". F-VA-PINS (e): "no registered
  construction, gate, licence or traverse reads a `1w_` column".

---------------------------------------------------------------------------------------------------------------
## CANON-05 · PINS THAT MOVED — the last-record law, the append-only files
**Settles:** FID-03 (a)-(d), BLD-02, CMP-01 (a)-(d). **Also cited by the dispositions of:** STA-03, BLD-27. **Authority:** OD-4. **Taken:** OD-4's rule for an earlier record
(the blob at the commit that closed it) over FID-03's and BLD-02's `supersedes{}` for TRACKED paths; `supersedes[]` is kept
for UNTRACKED paths only, where no blob exists.

**CANON TEXT.**
1. **L-0.4 clause (1):** "every `artifact_shas` path exists and verifies under THE LAST RECORD THAT NAMES IT (in
   `RESUME_ORDER_T`, CANON-09): the working file re-hashes to that record's `{bytes, sha256}`. An EARLIER record's entry
   for the same path is held to the blob at the commit that closed its own record — `git show <closing commit>:<path>`
   re-hashes to the earlier entry, the closing commit of a record being the last commit in `28e006b^..<--at>` that touched
   `progress/<record>.json` (a fixture-side read-only git call). For a path on the append-only list the earlier bytes must
   also be a byte-prefix of the working file. An UNTRACKED (git-ignored) path may be recorded by a later record only if
   that record's `supersedes[]` carries `{path, old_sha256, reason}` (reason = a ruling, an AM id or a stage law); its
   earlier entry is printed SUPERSEDED and not re-hashed. Anything else is a moved artifact."
2. **One helper for every sha-first reader:** `tierc12_progress.certified(rel_path) -> {record, bytes, sha256}` (stdlib
   only; walks `T12/progress/*.json` in `RESUME_ORDER_T`; returns the LAST record naming the path; HALT if none). It is
   what the shim (P3, the `x_rec` manifest's own sha, TC11's PROGRESS sha), the reader's sha law, the scorer's inputs
   (L-X.23) and the registry filer call. No reading takes a sha "from `progress/TC12-R0.json`" by name.
3. **L-0.5 lists.** BYTE-FROZEN from STEP Q: the contract prefix. APPEND-ONLY UNTIL THE TC12-REG COMMIT, then byte-frozen at
   the shas `REGISTRATIONS.json` `rulings.sha256` and `disclosures.sha256` name: `T12/ORCHESTRATOR_RULINGS.md` and
   `T12/DISCLOSURES.md` (R0's bytes must be a byte-prefix of every later version; only the orchestrator appends: section
   H, the D-5… entries of CANON-40). APPEND-ONLY THROUGHOUT (every committed version a byte-prefix of the next):
   `T12/LEANS_AMENDMENTS.md`, `T12/AMENDMENTS_PROPOSED.md`, `T12/DISCLOSURES_BUILD.md`, `T12/forward/FORWARD_LEDGER.jsonl`,
   `T12/scores/SUPERSEDED.jsonl`, `T12/scores/REFILE_LOG.jsonl`. The other byte-frozen entries stand as drafted.
4. **`T12/DISCLOSURES_BUILD.md`** is the running record AFTER the registry freeze (entries `B-1 …`, dated, never edited):
   every build-time disclosure a reading sends "to DISCLOSURES.md" after TC12-REG (L-D.18's fee-page observation,
   L-D.22's moved tick or coarser month) goes there. The report's §9 prints every line of both files.
5. **The TC12-LEANS record** (written by the orchestrator at the freeze) re-records `ORCHESTRATOR_RULINGS.md` and
   `x_rec/X_REC_MANIFEST.json` at their current shas, with `x_rec {n_files, bytes}` and the note "O-25 (commit 7295ab5): one
   row added, `queue/2026-09-25_TC11X_APOLLO.md`" [checked: rulings 17,970 B sha `27b8b572…`; manifest `n_files` 491 sha
   `58d594a3…`; `progress/TC12-R0.json` last touched by `ac8cb92`].
6. Paths the readings themselves re-record are lawful under point 1 and are named as such: `forward/FORWARD_LEDGER.jsonl`
   (TC12-REG.ledger-spec, then TC12-L; append-only), `ferry/FERRY_MANIFEST.json` (TC12-L, then TC12-CLOSE; tracked),
   `va/stamps/build_manifest.json` (the three stamps children; tracked, CANON-10), `scripts/tierc12_progress.py` (R0, then
   TC12-REG; tracked, CANON-35), `LEANS_AMENDMENTS.md`.

**PER-SECTION EDITS.**
- **L-0** — L-0.4 clause (1) = point 1; FAILS-IF adds the plants "an earlier record's path whose blob at its closing commit
  differs → RED" and "an untracked path re-recorded with no `supersedes` entry → RED". L-0.5: point 3, point 4; strike
  "(R0; its sha is an R0 artifact … never by editing that file)". L-0.6: "`XR/**` against `XR/X_REC_MANIFEST.json` (path
  set, `n_files`, every sha), the manifest's own sha and `n_files` read through `certified()`"; "the two earlier TC
  contracts in main's `exchange/queue/`, and X's contract as the manifest-pinned copy `XR/queue/2026-09-25_TC11X_APOLLO.md`
  (sha `40e0c4b7…3c3d`, O-25)". L-0.9 record keys: add `supersedes` (and the keys of CANON-09). L-0.12 clause (6): "…whose
  own sha is the one `certified()` returns at the reviewed commit". L-0.10 stage table, TC12-LEANS row: add "the record
  re-records the rulings and the X manifest at their current shas (OD-4)".
- **L-D** — register of constants: the row "every X record sha" reads "(manifest sha read through
  `tierc12_progress.certified`)" and the row "every certified TC11 sha" reads "(PROGRESS sha read from
  `progress/TC12-R0.json[\"frozen_estate_shas_at_r0\"]`, or the stamped value under CANON-35)"; strike the orientation
  value `cf66cb81…3e88`. L-D.18, L-D.22: "DISCLOSURES.md" → "`T12/DISCLOSURES_BUILD.md`". L-D.27 X-records bullet: the
  manifest's own sha through `certified()`.
- **L-V** — L-V.1 SOURCE: strike "(sha `cf66cb81…3e88`)"; write "(its sha read through `tierc12_progress.certified`)".
- **L-C** — abbreviations: strike ", sha `cf66cb81…3e88`".
- **L-L** — L-L.5 "The commit law" and L-L.32: one sentence each naming point 6.
- **L-X** — L-X.19: `rulings` and `disclosures` are the freeze pins of point 3; L-X.28 §9: "every line of `DISCLOSURES.md`
  and of `DISCLOSURES_BUILD.md`"; L-X.30 harvest sources: add `DISCLOSURES_BUILD.md`.

---------------------------------------------------------------------------------------------------------------
## CANON-06 · THE TWO TABLE WRITERS
**Settles:** FID-04, BLD-05, CMP-02, BLD-29 (the empty-arm write). **Authority:** OD-5. **Taken:** one signature for the
three the findings give.

**CANON TEXT.** `scripts/tierc12_tables.py` owns exactly two parquet writers; no other non-fixture TC12 source calls
`.to_parquet`, `TB.write_table` or a `TP` registry door.
1. **`put`** — from `make_put(root, meta, lens) -> (put, W, K, SK)`, the 6-dp table writer through `E.TB.write_table`
   (declared key, the nine stamps, the collar unless the table is on `REGISTERED_TABLES_T`); HALT if `root` resolves under
   `regbooks/`. The lineage's skip-empty law stands (an empty frame is not written and is listed under `skipped_empty`).
2. **`put_regbook(reg_dir, arm, df, *, meta, lens, kind) -> {path, content_sha, n}`** — HALT unless `reg_dir` resolves to
   `…/regbooks/<registration id>/` (under `T12`, under a `_det_*` twin root, or under a fixture's `--root`); `kind ∈ {base,
   scored, ladder, strip, tierE}` and agrees with the arm's name; the key `[symbol, entry_close_ms]` (`[arm, symbol,
   entry_close_ms]` when `kind == "strip"`) asserted unique by `E.TB.assert_key`; rows mergesorted on the key; the nine
   stamps by `E.TP.stamp_n`; the collar iff `kind ∈ {strip, tierE}` (asserted equivalent to "the arm is not on
   `REGISTERED_TABLES_T`"); **FULL FLOAT — no `_round_floats`**; a zero-row frame IS written, with the full schema; atomic
   `.tmp` then `os.replace`; `content_sha = E.TB._content_sha` of the full-float frame. It is TC11's `write_regbook` law
   (`scripts/tierc11_stage_g.py:1168-1178`) and the ONE `.to_parquet` call site in non-fixture TC12 code. Its only caller
   is `tierc12_regbook.write_arm` (CANON-07).
3. F-WARRANTY `(d)`: "… calls `.to_parquet` / `write_table` outside the wrapper's two writers". Plants: `put_regbook`
   called with a root under `T12/books/` → RED; `put` called with a root under `regbooks/` → RED; a `df.to_parquet(…)`
   bypass in a shadow builder → RED.
4. Content shas: "of the table as written — regbook arms at full float, every other table at the lineage's rounding".
   Outside `regbooks/` the fixture-typed file set of a directory is the typed set minus the manifest's `skipped_empty`,
   each skipped name asserted empty by the fixture's own count. Manifest key list gains `registrations_sha256`.

**PER-SECTION EDITS.**
- **L-0** — L-0.13 "The wrapper": points 1-2; "No non-fixture TC12 source calls …" → "… outside these two writers";
  "Manifests": add `registrations_sha256`; FAILS-IF (d) and plants = point 3. L-0.20: "floats rounded to the lineage's
  decimals" → point 4's first sentence; add the skip-empty file-set sentence. L-0.21 (3): the content sha clause likewise.
- **L-X** — L-X.24: "Arms are written by `tierc12_regbook.write_arm`, which calls L-0.13's `put_regbook`" (CANON-07).
  L-X.25: cite the same.
- **L-G** — L-G.19: "Regbook arms are written at FULL FLOAT by `tierc12_regbook.write_arm` (L-0.13's `put_regbook`)";
  INTERFACE (L-0): delete "A conflict to settle at assembly … ASSUMED: …" and write "settled: L-0.13's `put_regbook`".
- **L-C** — L-C.4 API: `base_regbook_frame()` returns the frame handed to `write_arm`; no write of its own.
- **L-R**, **L-S**, **L-L** — wherever a regbook arm is written, name `tierc12_regbook.write_arm`; L-L.16 keeps the
  skip-empty law for its side tables.

---------------------------------------------------------------------------------------------------------------
## CANON-07 · THE REGBOOK INTERFACE (what Stages G, R and S write and the scorer reads)
**Settles:** BLD-29, CMP-15 (the interface module), TRD-08 (the fifth fee column), TRD-04 (the two cost columns), BLD-36 (1),
CMP-20 (the strip's form), and reconciles L-X.24 with L-G.19, L-R.31, L-S.30. **Also cited by the dispositions of:** FID-04, FID-07, STA-12, BLD-05, TRD-09, CMP-29. **Authority:** OD-5, OD-6, OD-10, OD-14.

**CANON TEXT.**
1. **Module.** `scripts/tierc12_regbook.py` (L-X's; filed at `TC12-ENV.score-build`, CANON-09) holds the interface every
   book stage and the scorer share: `ARM_RX`, `COLS16`, `COLS20`, `canonical_csv(df, cols)`, `book_sha256(df)`,
   `book_ext_sha256(df)`, `validate_book(reg_dir, arm) -> findings`, the fee identities, `write_arm(reg_dir, arm, df, *,
   meta, lens, sidecar) -> None` (calls `tierc12_tables.put_regbook`, then writes `<arm>.json`), `write_status(reg_dir,
   …)`, `write_manifest(reg_dir, …)`. The scorer imports it; no stage writes a validator of its own.
2. **Layout.** `T12/regbooks/<ID>/` = `STATUS.json`, `build_manifest.json` (declared key per arm, content shas,
   `registry_head`, `registrations_sha256`), and per arm `<arm>.parquet` + `<arm>.json`. Arm names match
   `^(scored|base|ladder__(touch|deep)|strip|tierE__[a-z0-9_]+)$`.
3. **`STATUS.json` keys:** `registration`, `status ∈ {"BUILT", "CLOSED_BY_PRECONDITION"}`, `reason`, `arms` (sorted; every
   arm on disk and no other; `[]` when closed), `registry_head`, `registrations_sha256`, `source_script`,
   `source_script_sha256`, `preconditions` (each item `{record, certified_by, selector, required, found, met}`).
4. **The arms of record** (STATUS lists exactly these when BUILT; an arm with no row is written EMPTY, point 8):

   | registration | arms |
   |---|---|
   | P-ADM-1 | `base`, `scored`, `strip`, `tierE__shadow_old_alone`, `tierE__shadow_stale_alone`, `tierE__shadow_abs206`, `tierE__shadow_abs206_or_stale` |
   | P-BRD-1 | `base`, `scored`, `strip`, `tierE__brd_face`, `tierE__brd_neff`, `tierE__brd_loo`, `tierE__brd17` |
   | P-DIR-1 | `base`, `scored`, `strip` |
   | P-SFP-VA-1 | `scored`, `strip`, `tierE__unfiltered`, `tierE__cell_1d`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__maker_assumed`, `tierE__x_geometry`, `tierE__x_gaplaw` |
   | P-SCALP-3 | `scored` (TICK), `ladder__touch`, `ladder__deep`, `strip`, `tierE__full_corridor`, `tierE__panel17`, `tierE__rr_unfiltered`, `tierE__live_edge` |

5. **Columns, exact dtypes, in this order.** TC11's sixteen: `symbol` str · `entry_ms` int64 · `entry_close_ms` int64 ·
   `direction` int8 · `entry_px`, `stop_px`, `r_dist` float64 · `exit_close_ms` int64 · `exit_reason` str · `net_r`,
   `gross_r`, `fee_r`, `funding_r`, `haircut_net_r` float64 · `era` str · `lane` str. Then TC12's four, float64:
   `fee_taker_r`, `fee_maker_r`, `fee_all_taker_r`, `taker_twin_net_r`. These twenty are required on every arm.
   Conditional columns: `taker_twin_haircut_net_r` float64 — required iff the sidecar's `toll ==
   "maker_entry_targets__taker_stop"`; `funding_ceiling_bound` bool and `tc_series_net_r` float64 — required on every
   range arm (lanes `sfp-va-4h`, `sfp-va-1d`, `scalp_va_1h`; CANON-15); `arm` str — required on `strip` and only there.
   Extra columns are allowed and ignored by the scorer. `lane` values: `card` (v6 and its gates), `sfp-va-4h`,
   `sfp-va-1d`, `scalp_va_1h`.
6. **Row laws** as L-X.24 states them (HALT on `scored`, `base`, `ladder__*`; NOTE on `tierE__*`), with: unique key
   `(symbol, entry_close_ms)` — on `strip`, `(arm, symbol, entry_close_ms)`; the scored window and the strip per CANON-19;
   the fee identities; added identity `|taker_twin_haircut_net_r − (taker_twin_net_r − fee_all_taker_r × slip / taker)| ≤
   HAIRCUT_TOL` where the column is required; on range arms `funding_r` is the UNCAPPED funding and `|taker_twin_net_r −
   tc_series_net_r| ≤ HAIRCUT_TOL` on rows with `funding_ceiling_bound == False` (CANON-15).
7. **Sidecar `<arm>.json` keys:** `registration`, `arm`, `kind ∈ {base, scored, ladder, strip, tierE}`, `ruler ∈
   {two_sample, vs_zero}`, `era_scope ∈ {full, holdout, tuning}`, `panel` [stems], `lens`, `toll ∈ {"taker",
   "maker_entry_targets__taker_stop"}`, `fill_rule` (`tick` / `touch` / `deep` on P-SCALP-3's arms and on the two SFP
   maker twins; else null), `n`, `sum_net_r`, `book_sha256`, `book_ext_sha256`, `registry_head`, `registrations_sha256`,
   `fee_schedule {path, sha256}`, `description`, `source_script`, `source_script_sha256`. Added by kind: P-SCALP-3
   `scored` / `ladder__touch` / `ladder__deep` carry `n_orders`, `n_filled_touch`, `n_filled_tick`, `n_filled_deep`
   (CANON-08); `strip` carries `n_by_arm {arm: n}` and, for an arm that is the same walk as another, `same_rows_as`;
   `tierE` and `strip` sidecars carry the collar keys; `tierE__cell_1d` carries `licence_pointers = {era:
   "research_outputs/tierc12/va/VA_MIRROR.json#licence[1d|taker].by_era[<era>]"}` and booleans `licence_ok_by_era` — never
   the words (the words are printed only in §0 beside the row).
8. **The empty-arm form.** Every arm a spec names is written even when empty: a zero-row parquet with the columns of
   point 5 at their dtypes, the nine stamps and (if collared) the collar; its sidecar with `n = 0`, `sum_net_r = 0.0` and
   the `book_sha256` of the header-only canonical CSV; STATUS `arms` lists it.
9. **The strip (OD-14).** `strip.parquet` holds, under the column `arm`, the rows with `W < entry_close_ms ≤ PIN` of EVERY
   other arm of the regbook (for a post-filter gate: the v6 strip campaigns each arm's rule keeps, `base` = all of them;
   for a ridden book: that arm's own ride to PIN). An arm that is the same walk as another (P-SFP-VA-1
   `tierE__maker_assumed` ≡ `scored`; P-SCALP-3 `tierE__full_corridor` ≡ `scored`) is not repeated: it appears in
   `n_by_arm` with `same_rows_as`. Counts and a pointer only — no statistic over strip rows anywhere.
10. **Two hashes** as drafted: `book_sha256` over the sixteen (TC11's SC-13 law), `book_ext_sha256` over the twenty.
11. **Fixtures.** F-REGBOOK's plant legs and its production side live with the scorer (`tierc12_score_fixtures.py`,
    hosted at `TC12-ENV.score-build`); the real-book instances `F-REGBOOK [<ID>]` and `F-BASE-IDENT [<ID>]` are helper
    legs (functions of `tierc12_score_fixtures.py`) that each book stage's suite runs on its own regbook directory.

**PER-SECTION EDITS.**
- **L-X** — L-X.24: re-head "no contract line — the regbook interface (F-KEY, :124, is L-0.21's)"; Layout, STATUS, columns,
  laws, sidecar, empty-arm form, strip and module per points 1-11; replace the cross-arm law by CANON-08. L-X.23 item 6:
  "the latest record that names the path (parent or dotted child), through `certified()`". L-X.14: `strip` leaf prints `n`
  per arm and one pointer.
- **L-G** — L-G.8, L-G.13, L-G.19: arms exactly as point 4; `strip` per point 9 (L-G.18's "the same flags define each
  book's strip" is its content); P-ADM-1 and P-BRD-1 specs `arms`: the `strip` sub-bullet reads "`strip` — the extended
  ride's campaigns with entry close after TC11's pin, per arm under the column `arm`; rows and counts only."
- **L-R** — L-R.4, L-R.21, L-R.24, L-R.31: arms exactly as point 4 (no `tierE__reride`; add `tierE__x_geometry`,
  `tierE__x_gaplaw`); every ridden arm's strip rows in `strip.parquet` (point 9); `tierE__cell_1d`'s sidecar per point 7;
  the extra columns of L-R.31 keep their names and add `funding_ceiling_bound`, `tc_series_net_r`, `t1_void`,
  `inval_event_E`, `inval_edge_moved`.
- **L-S** — L-S.30: arms as point 4; rows carry the twenty plus `taker_twin_haircut_net_r`, `funding_ceiling_bound`,
  `tc_series_net_r`; the extra column `trigger_close_ms` is named `known_at_ms` (CANON-33); the row column `licence`
  takes the values `licensed` / `none — CLASSIC5 word transplanted`. L-S.25: strip per point 9.
- **L-0** — L-0.16: "each registered row's regbook of record and its base arm, and the arms a registered row's
  `verdict_rule` reads (P-SCALP-3's `ladder__touch`, `ladder__deep`)". L-0.20: regbook directories hold every named arm,
  empty or not.
- **L-L** — L-L.25: the row `regbooks/<ID>/<arm>.parquet` is expanded over point 4's table by object (STATUS `arms`);
  `strip` is per-trade × `arm`.

---------------------------------------------------------------------------------------------------------------
## CANON-08 · THE FILL LADDER IS PER ORDER
**Settles:** FID-10, STA-04, BLD-06, TRD-02, CMP-04 (ii). **Authority:** OD-6, O-32, contract :120-121.

**CANON TEXT.** "**Ladder law on P-SCALP-3 (per order, O-32).** Each of the three ladder-class sidecars (`scored`,
`ladder__touch`, `ladder__deep`) carries `n_orders`, `n_filled_touch`, `n_filled_tick`, `n_filled_deep` — the three entry
tests of L-S.15 evaluated on THAT arm's own order ledger (L-S.16). The scorer HALTs `LADDER-ORDER` unless `n_orders ≥
n_filled_touch ≥ n_filled_tick ≥ n_filled_deep` on every one of the three. The arm totals `n(ladder__touch)`, `n(scored)`,
`n(ladder__deep)` are printed in the fill-sensitivity row and are not ordered by law (three separately sequenced books);
when they are not ordered the row's `disclosures[]` carries `BOOK-N-NOT-MONOTONE` — a disclosure, never a HALT and never a
qualifier." F-REGBOOK plant: the TICK and DEEP counts swapped in a sidecar copy → `LADDER-ORDER`.

**PER-SECTION EDITS.**
- **L-X** — L-X.24: replace "Cross-arm law on P-SCALP-3: `n(ladder__touch) ≥ n(scored) ≥ n(ladder__deep)`, else HALT
  `LADDER-ORDER`" by the text above; add the plant to F-REGBOOK. L-X.9 verdict-text bullet: "… the single-trade share of
  record; then the per-order ladder counts of the TICK ledger and, where the three books' own n are not ordered, the line
  `BOOK-N-NOT-MONOTONE`".
- **L-S** — L-S.16: "(INTERFACE: L-X.24's `LADDER-ORDER`)" → "(L-X.24's `LADDER-ORDER` is on these per-ledger counts)".
  L-S.28 verdict text: unchanged in content, cites L-X.24. P-SCALP-3 spec `verdict_rule`, after "the single-trade share of
  record (no threshold; it decides nothing)": add "then the per-order ladder counts of the TICK ledger and, where the three
  books' own n are not ordered, the line BOOK-N-NOT-MONOTONE (the books are sequenced separately; their n are not
  comparable order for order)". INTERFACE (L-X): delete "One difference for the reviser …" and write "settled: OD-6".

---------------------------------------------------------------------------------------------------------------
## CANON-09 · THE SUB-STAGE LAW (ids, records, gates, resume point, depends_on)
**Settles:** BLD-09, CMP-06, FID-12, BLD-10, CMP-08, FID-11 (the id), CMP-09 (the ids), BLD-11 (a), BLD-39 (4), BLD-37 (the
S-after-R.sfp clause), CMP-15 (the child). **Also cited by the dispositions of:** STA-03, BLD-36, CMP-03. **Authority:** OD-7, O-31, O-6. **Taken:** OD-7's three stamps children under
TC12-V (BLD-10 item (4) and BLD-11 (c) — stamps filed by each book's own sub-stage, `books/stamps/` — are not built; FID-11's
single record `TC12-V.stamps` is not built).

**CANON TEXT (goes into L-0.10; every section conforms).**
1. **Record ids.** `ORDER` in `scripts/tierc12_progress.py` is the stage list of record. A sub-stage is a dotted child
   `<ORDER entry>.<tag>`; its record is `T12/progress/<id>.json` and its `stage` key is the id. No id exists outside `ORDER`
   and the table `SUBSTAGES_T` below without a dated amendment. The merger sorts a child under its parent by its
   longest-prefix rule [checked on every id below].
2. **`SUBSTAGES_T`:**

   | child id | owner | blocking | depends_on | what it files (directory) |
   |---|---|---|---|---|
   | `TC12-REG.ledger-spec` | L-L | yes | `TC12-REG` | `forward/BOOK_SPEC_COMBINED.json`, `forward/FORWARD_LEDGER.jsonl` (five lines), `tierc12_forward_spec.py`, `tierc12_forward_fixtures.py` |
   | `TC12-D.mirror` | L-D | **NO — the only non-blocking child** | `TC12-D` | `data/MIRROR_ATTEST.json` (PARTIAL allowed through CLOSE; harvested as a finding) |
   | `TC12-ENV.vendor` | L-D | yes | `TC12-D` | `vendor/tierc11_env@1526093b.py`, `vendor/README.md`, `scripts/tierc12_vendor.py`, `env/LINEAGE_PINS.json` |
   | `TC12-ENV.score-build` | L-X | yes | `TC12-ENV` | `scripts/tierc12_regbook.py`, `tierc12_score.py`, `tierc12_score_fixtures.py` (the scorer's code and its synthetic and anchor legs; no TC12 book is read) |
   | `TC12-V.trades` | L-V builds, L-R defines | yes | `TC12-V` | `va/trades/**` (DOOR 2) |
   | `TC12-C.tide` | L-G | yes | `TC12-ENV` | `tide/**` |
   | `TC12-V.stamps.c` | L-V | yes | `TC12-V`, `TC12-C` | `va/stamps/VA_STAMPS_{v6,trg912}.parquet` |
   | `TC12-R.dir` | L-R | yes | `TC12-V`, `TC12-C`, `TC12-V.stamps.c`, `TC12-ENV.score-build` | `regbooks/P-DIR-1/**`, `stage_r/dir/**` |
   | `TC12-R.sfp` | L-R | yes | `TC12-V`, `TC12-ENV.score-build` | `scripts/tierc12_rangewalk.py`, `regbooks/P-SFP-VA-1/**`, `stage_r/sfp/**` |
   | `TC12-R.tables` | L-R | yes | `TC12-V`, `TC12-C` | `stage_r/tables/**` (the 1d take-profit venue, L-R.30) |
   | `TC12-V.stamps.r` | L-V | yes | `TC12-R.sfp`, `TC12-R.tables` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage R's books (CANON-10) |
   | `TC12-V.stamps.s` | L-V | yes | `TC12-S` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage S's books |

3. **`RESUME_ORDER_T`** — the order in which records are gated and committed. It is held as data in
   `scripts/tierc12_progress.py` (`RESUME_ORDER`, with `SUBSTAGES`, beside `ORDER`, which stays the stage list of record;
   added at the TC12-REG commit, CANON-30) and typed again in the resume fixture as its second object: `STEP Q` ·
   `TC12-R0` · `TC12-LEANS` · `TC12-REG` · `TC12-REG.ledger-spec` · `TC12-D` · `TC12-ENV.vendor` · `TC12-ENV` ·
   `TC12-ENV.score-build` · `TC12-V` · `TC12-V.trades` · `TC12-C.tide` · `TC12-C` · `TC12-V.stamps.c` · `TC12-G` ·
   `TC12-R.dir` · `TC12-R.sfp` · `TC12-R.tables` · `TC12-R` · `TC12-V.stamps.r` · `TC12-S` · `TC12-V.stamps.s` · `TC12-L` ·
   `TC12-SCORE` · `TC12-FIX` · `TC12-REVIEW` · `TC12-CLOSE`. `TC12-D.mirror` is in no position: it may be gated at any time
   after `TC12-D`.
4. **THE RESUME POINT** = the first entry of `RESUME_ORDER_T` whose record is absent or not COMPLETE-VERIFIED. Derived,
   never typed, never stored. A non-blocking child never moves it.
5. **Start law.** A record may START iff every earlier entry of `RESUME_ORDER_T` is COMPLETE-VERIFIED — EXCEPT the parallel
   set `PARALLEL_T` = {`TC12-G`, `TC12-R.dir`, `TC12-R.sfp`, `TC12-R.tables`, `TC12-R`, `TC12-V.stamps.r`, `TC12-S`,
   `TC12-V.stamps.s`}, each of which may start once every entry through `TC12-V.stamps.c` and every record in its own
   `depends_on` are COMPLETE-VERIFIED (`TC12-G`: `TC12-C`, `TC12-C.tide`, `TC12-V.stamps.c`, `TC12-ENV.score-build`;
   `TC12-S`: `TC12-V`, `TC12-C.tide`, `TC12-R.sfp`, `TC12-ENV.score-build` — it imports `tierc12_rangewalk.fee_per_fraction`,
   filed at `TC12-R.sfp` with F-SFP-MIRROR GREEN). Commits still land in `RESUME_ORDER_T` order. One machine-wide worker
   cap (O-5). Wherever a reading says "after `<STAGE>` is COMPLETE-VERIFIED" as a START condition it means the RECORD
   `<STAGE>.json` and the children that precede the starter in `RESUME_ORDER_T` — never the stage-complete predicate of
   point 6 (TC12-V's stamps children `.r` and `.s` close after Stages R and S by design).
6. **Parent records.** Every `ORDER` stage files a parent record `<STAGE>.json`. Its `artifact_shas` are the files no
   child records: the stage's own artifacts, its index document where it has children (`stage_r/STAGE_R.md` = three
   pointers), and the transcripts of the L-0 suites run at its gate. An `ORDER` STAGE is COMPLETE-VERIFIED iff its parent
   record and every BLOCKING child are. The parent record of a stage with several producers (`TC12-REG`, `TC12-ENV`) is
   written by the orchestrator's gate step from the artifact maps each producer returns.
7. **One commit per record,** subject `tierc12(<record id>): …` (CANON-31). The gate of L-0.9, steps (1)-(6), is run per
   record; the resume suite runs at every record gate from `TC12-REG` on with `--stage=<record id>`; the closure, not and
   sweep suites run at `ORDER`-stage gates. `TC12-ENV.vendor` and `TC12-REG.ledger-spec` therefore have their own commits,
   and F-VENDOR's "tracked and equal to its blob" leg (read at `--at`) runs at the `TC12-ENV` gate, after the vendor
   commit.
8. **Record keys** (L-0.9): `stage`, `parent`, `status`, `as_of`, `blockers`, `depends_on` [record ids], `artifact_shas`,
   `supersedes` [], `fixtures` [{`suite`, `transcript`, `provenance` (bool), `exit_code`, `legs_red`, `legs_not_run`,
   `legs_total`, `transcript_drift`, `transcript_sha_before`, `transcript_sha_after`, `wall_seconds`}], `one_line`,
   `notes`. `suite` is the full argv after the interpreter; `transcript` is its repo-relative path.
9. **Quarantine follows `depends_on`,** transitively: a record whose `depends_on` closure names a quarantined record
   becomes PARTIAL with it. Quarantine directories are `T12/_det_partial_<YYYYMMDD>T<HHMM>Z/` (already git-ignored).
10. **Directory and transcript law** (L-0.9): one writer script per parquet directory; one `build_manifest.json` per
    directory; one transcript per fixture record; a suite serving several records takes `--stage=<record id>` and files a
    transcript of its own per record (paths: CANON-24) — never a leg filter. The one typed exception is `SHARED_DIRS_T =
    ("research_outputs/tierc12/va/stamps",)`: the reader writes it at three records; its `build_manifest.json` is
    cumulative and re-recorded by each stamps child (CANON-05 point 6); the helper legs F-KEY / F-DET / F-COLLAR on a
    shared directory are SCOPED — they evaluate on a scratch VIEW holding the tables that the records up to `--stage` name
    and the manifest restricted to them, and call `TP.check_keys` / `TP.check_det` on that view.
11. **Pre-substrate header.** A suite run at a record before `TC12-D` in `RESUME_ORDER_T` prints `as_of_last_closed_4h:
    (pre-substrate stage)` and `substrate: none`; F-ONE-CORRIDOR exempts exactly those records.
12. **Fixtureless records** stay the typed three (`STEP Q`, `TC12-R0`, `TC12-LEANS`). Every child has a fixture record.

**PER-SECTION EDITS.**
- **L-0** — L-0.3: THE RESUME POINT per point 4. L-0.4: quarantine name and rule per point 9. L-0.9: record keys (point 8),
  the gate per record (point 7), the directory law (point 10). L-0.10: add points 1-6 and 11-12 verbatim, with the table;
  the stage table's rows gain their children (TC12-REG: + `REGISTRATION_PLAN.md`, `registrations/ATTEST_REG.json`, REG_SET
  of CANON-30, then `TC12-REG.ledger-spec`; TC12-LEANS: + `LEANS_AMENDMENTS.md`, `AMENDMENTS_PROPOSED.md`; TC12-ENV:
  `.vendor` first, `.score-build` last; TC12-V: + `.trades`, `.stamps.c/.r/.s`; TC12-C: + `.tide`; TC12-R: `.dir`, `.sfp`,
  `.tables`); replace "Building in parallel is allowed only for TC12-G, TC12-R and TC12-S, after TC12-V and TC12-C" by
  point 5; replace the examples "`TC12-REG.vendor`" by "`TC12-ENV.vendor`"; T2 unchanged; T5: "TC12-SCORE starts only when
  TC12-C, -G, -R, -S, -L and the three stamps children are COMPLETE-VERIFIED". L-0.11: clock files go to
  `T12/sweep/_det_clock/<record id>.json`; the roll is over `RESUME_ORDER_T`. INTERFACE: strike "A conflict to settle at
  assembly … `TC12-REG.vendor`" and write "L-D's children are `TC12-ENV.vendor` and `TC12-D.mirror` (O-31)".
- **L-D** — L-D.24: record `TC12-D.mirror` (non-blocking), transcript `data/FIXTURES_MIRROR.txt`. L-D.25: "filed as the
  first act of TC12-ENV under the record `TC12-ENV.vendor`, after TC12-D is COMPLETE-VERIFIED and before any hunk is
  applied; it has its own commit `tierc12(TC12-ENV.vendor): …`, which precedes the TC12-ENV gate; its fixture record is
  F-VENDOR `[referee]` (the three-sha equality, the tag, the hunks apply and revert on the referee text), run by
  `tierc12_env_fixtures.py --stage=TC12-ENV.vendor` without importing the shim → `env/FIXTURES_ENV_VENDOR.txt`". L-D.30
  order: "`TC12-D` (L-D.5 steps 1-7) → `TC12-ENV.vendor` (referee and `scripts/tierc12_vendor.py` committed; three-sha
  equality; `--pin-lineage`) → `TC12-ENV`". INTERFACE (L-0): the two side records are `TC12-ENV.vendor` and
  `TC12-D.mirror`.
- **L-V** — L-V.24: "Stage `TC12-V` runs before any book exists" stays; add the children `TC12-V.trades` and
  `TC12-V.stamps.c/.r/.s` with their `depends_on`.
- **L-C** — L-C.11: "The sub-stage `TC12-C.stamps` runs L-V's reader … and files `T12/books/VA_STAMPS_*`" → "The child
  `TC12-V.stamps.c` (L-V.19) runs the reader over those two frames and files `T12/va/stamps/VA_STAMPS_v6.parquet` and
  `VA_STAMPS_trg912.parquet`".
- **L-G** — L-G.10: `TC12-C.tide` stands (blocking; required by TC12-G, TC12-S, TC12-L). INTERFACE (L-0): "Sub-stages
  `TC12-C.tide` and `TC12-C.stamps`" → "`TC12-C.tide` (this section's) and `TC12-V.stamps.c` (L-V's)".
- **L-R** — L-R.31 "Sub-stages": `TC12-R.dir` → `TC12-R.sfp` → `TC12-R.tables`, then the parent record `TC12-R`
  (`stage_r/STAGE_R.md`, an index of three pointers); directories `stage_r/dir/`, `stage_r/sfp/`, `stage_r/tables/`, each
  with its own `build_manifest.json` and stage document (`STAGE_R_dir.md`, `STAGE_R_sfp.md`, `STAGE_R_tables.md`); add
  "Compute: one process per sub-stage, no worker pool; fixture subprocesses run one at a time (O-5)." P-DIR-1 spec
  `preconditions` commentary: "the `base` arm (`regbooks/P-DIR-1/base.parquet`, certified by `progress/TC12-R.dir.json`;
  its book identity held to TC11's by F-BASE-IDENT)".
- **L-S** — L-S.1: "The stage starts only after `TC12-V`, `TC12-C.tide`, `TC12-R.sfp` and `TC12-ENV.score-build` are
  COMPLETE-VERIFIED (L-0.10)". INTERFACE (L-G): the table is `TC12-C.tide`'s.
- **L-L** — L-L.3 "When": unchanged (`TC12-REG.ledger-spec`, own commit, before TC12-D). "What this section files": cite
  point 2.
- **L-X** — L-X.23 item 6: records per CANON-07; the scorer's code is filed at `TC12-ENV.score-build`; L-X.21 per
  CANON-30.

---------------------------------------------------------------------------------------------------------------
## CANON-10 · THE V5 STAMPS — Stage V tables, three children, one kind law
**Settles:** FID-11, CMP-09, BLD-17, FID-19, BLD-11 (c), BLD-12 (per-book legs), CAU-05 (iv). **Also cited by the dispositions of:** BLD-10, TRD-13. **Authority:** OD-7, O-29, O-31,
contract :44-46. **Taken:** OD-7's path `va/stamps/VA_STAMPS_<book>.parquet`; BLD-17's `kind` dict over CMP-09's shorter one;
`known_at_ms` as the order instant (CANON-33).

**CANON TEXT.**
1. **Who files.** No book builder stamps its own book. After a book stage files its frames, the READER is run as
   `scripts/tierc12_va_stamps.py --file-stamps --stage=TC12-V.stamps.<c|r|s>`; it writes
   `T12/va/stamps/VA_STAMPS_<book>.parquet` through `put`, merges its entries into `T12/va/stamps/build_manifest.json`
   (HALT `STAMPS-MOVED` if an entry it would write exists with another sha), and its record `progress/TC12-V.stamps.<x>.json`
   pins each table `{bytes, sha256}` and names in `depends_on` the records whose frames it read. A consumer asserts the
   sha through `certified()` before use.
2. **`instants_of(frame, kind)`.** `kind` is a dict filed in the manifest per table: `{book, lens, key: [frame columns
   after symbol], start_col, end_col, bar_close_lens (default = lens), events: [{name, col, stamp ∈ {"close",
   "open_of_bar"}, post_event: bool}]}`. The frame holds `symbol`, the key columns and every named column as int64 ms (null
   = did not happen). Instants per frame row: every close of `bar_close_lens` from `start_col` through `end_col`
   (`instant_kind = "bar_close"`), plus each event (`open_of_bar` events are stamped at the OPEN of their bar and, if
   `post_event`, again at its close as `<name>_post_event`), plus `as_of_pin` for a row open at the corridor pin (never
   `exit`). An event the frame's own record says happened but no column stamps HALTs the reader.
3. **Table key** = `[book, symbol] + kind.key + [instant_kind, instant_ms]`. Columns: those five-plus, then per lens ℓ ∈
   (1h, 4h, 12h, 1d, 1w) the block of L-V.20 prefixed `<ℓ>_` (CANON-11 point 2 lists it), and `nest_gap_reason`.
4. **The books and their kinds:**

   | child | `<book>` | frame | lens · key · start_col · bar_close_lens | events |
   |---|---|---|---|---|
   | `.c` | `v6`, `trg912` | `books/v6_ext_campaigns.parquet`, `books/trg912_ext_campaigns.parquet` | 4h · `[entry_ms]` · `arm_close_ms` · 4h | `arm`, `entry` (close); `plus_1r` (`latch_1r_open_ms`, open_of_bar, post); `harvest` (`harvest_close_ms`, close); `bell` and `exit` from `exit_event_ms` by `exit_reason` and `exit_event_stamp` (an intrabar exit: open_of_bar, post); `as_of_pin` from `open_at_asof` |
   | `.r` | `P-SFP-VA-1__<arm>` for each RIDDEN arm (`scored`, `tierE__unfiltered`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__x_geometry`, `tierE__x_gaplaw`; the frame is that arm's ride to PIN, so the `strip` rows are covered) | the arm's trade frame | 4h · `[entry_ms]` · `entry_close_ms` · 4h | `entry` (close); `ev_t1` (`ev_t1_ms`, open_of_bar, post); `exit` (stop or T2: open_of_bar, post; time stop, invalidation: close); `as_of_pin` |
   | `.r` | `P-SFP-VA-1__tierE__cell_1d` | its trade frame | 1d · as above · 1d | as above |
   | `.r` | `tp1d` | `stage_r/tables/TP1D_CAMPAIGNS.parquet`, rows with `exit_reason == "tp"` | 4h · `[entry_ms]` | `ev_tp` (`ev_tp_ms`, open_of_bar, post) ONLY — every other instant of a venue campaign is a v6 instant |
   | `.s` | `P-SCALP-3__<arm>` for `scored`, `ladder__touch`, `ladder__deep`, `tierE__panel17`, `tierE__rr_unfiltered`, `tierE__live_edge` (the frame is that arm's ORDER ledger to PIN, misses included) | `stage_s/S_orders_<book>.parquet` | 5m · `[known_at_ms]` · `known_at_ms` · **1h** | `arm` (`known_at_ms`, close); `entry` (the fill: open_of_bar, post); `ev_t1` (post); `exit` (stop or target: open_of_bar, post; a close event: close); `expiry`, `cancel` (close) |

   Event columns of a frame are named `ev_<name>_ms` (or the lineage's own names on the v6 frames): the scalper's order
   frame carries `ev_entry_ms`, `ev_t1_ms`, `ev_exit_ms`, `ev_expiry_ms`, `ev_cancel_ms` — the OPEN of the bar for an
   intrabar event, the close for a close event — and no column named `event_ms` (CANON-33).
   A derived arm whose instants are another's is NOT re-stamped: `tierE__maker_assumed` ≡ `P-SFP-VA-1__scored`;
   `tierE__full_corridor` ≡ `P-SCALP-3__scored`. A gated book (every post-filter of v6) is a key SUBSET of `v6`: it files a
   key table `[book, symbol, entry_ms]` (`stage_g/g_book_keys.parquet`; `stage_r/dir/dir_book_keys.parquet` for P-DIR-1's
   kept book) and is asserted `⊆`, never re-stamped.
5. **Fixtures** (`tierc12_va_stamps_fixtures.py --stage=<child>` → `va/stamps/FIXTURES_STAMPS_<child>.txt`; the suite
   imports no door): `F-NEST-KEYS` (child `.c` only: the v6 and 9/12 key sets against TC11's nest tables; the gated-subset
   law for the key tables then on file); `F-NEST-ASOF [<book>]` for every table of the child — the reader's stamp at every
   instant of the book == the fixture's own linear-scan as-of join of the filed `va_bars` rows, plus the boundary legs on
   the book's own instants (leans on F-VA-ASOF [d], CANON-03); F-KEY / F-DET / F-COLLAR scoped (CANON-09 point 10).

**PER-SECTION EDITS.**
- **L-V** — L-V.19 "Who files what": replace by points 1 and 4; define `kind` per point 2; key per point 3; FAILS-IF:
  F-NEST-KEYS per point 5. L-V.20: unchanged in content (the block). The fixture roll: F-NEST-KEYS and the per-book
  F-NEST-ASOF move to the stamps suite. INTERFACE: "the per-book stamp tables are filed by each book stage" → "are Stage V
  tables filed by the reader under `TC12-V.stamps.c/.r/.s`"; the asks of L-S (ii) are answered by point 4.
- **L-C** — L-C.11: frames and kind as the `.c` row; paths `T12/va/stamps/…`; FAILS-IF: "L-V's F-NEST-KEYS and F-NEST-ASOF
  [v6], [trg912], hosted at `TC12-V.stamps.c`".
- **L-G** — L-G.18: `T12/books/VA_STAMPS_v6.parquet` → `T12/va/stamps/VA_STAMPS_v6.parquet`; the subset law unchanged.
- **L-R** — L-R.31 "Stamps (V5)": replace by "P-DIR-1's kept book files `stage_r/dir/dir_book_keys.parquet` (a key subset
  of `v6`, asserted, never re-stamped). The ridden range books and the take-profit venue's `tp` exits are stamped by
  `TC12-V.stamps.r` per L-V.19's table; this section files the frames and declares the kinds there listed." L-R.4:
  the entry-row assertion reads `va/stamps/VA_STAMPS_v6.parquet`. L-R.30: add `ev_tp_ms` to `TP1D_CAMPAIGNS`.
- **L-S** — L-S.30: strike the `VA_STAMPS_scalp` row and the "V5 stamps of the scalper's books" bullet's filing sentence;
  write "The scalper's books are stamped by `TC12-V.stamps.s` (L-V.19): key `[book, symbol, known_at_ms, instant_kind,
  instant_ms]`, `bar_close` at every 1h close between the trigger and the order's resolution (`bar_close_lens = "1h"`)."
  INTERFACE (L-V) addition (ii): "answered by L-V.19".
- **L-L** — L-L.16: `VA_STAMPS_v6` / `VA_STAMPS_trg912` are `T12/va/stamps/…`, "filed by L-V's reader at
  `TC12-V.stamps.c`"; L-L.25's row: key `[book, symbol] + kind.key + [instant_kind, instant_ms]`.
- **L-0** — INTERFACE: strike the `TC12-V5` sentence; L-0.13: the member's own bar-close column is L-V.20's.

---------------------------------------------------------------------------------------------------------------
## CANON-11 · THE STAGE V FILED TABLE INVENTORY (everything a consumer reads under the file-only wall)
**Settles:** BLD-01 (the list), CAU-04, FID-17 (the column), FID-13 (the twin keys), CMP-19 (twin words), STA-02 / BLD-15 (the
quoted licence columns), BLD-32 / FID-09 (the null files), CAU-09. **Also cited by the dispositions of:** CAU-12, CMP-30. **Authority:** O-29, OD-2, OD-12, OD-15.

**CANON TEXT.** Every file below is pinned `{bytes, sha256}` in the record named and asserted through `certified()` before
any use. Parquet: 6 dp at write, nine stamps, collar (none is registered except `VA_MIRROR.json`). "R:" = who reads.

1. **`va/VA_PINS.json`** (DOOR 1 · `TC12-V`) — `by_lens.<ℓ>` for ℓ ∈ {1h, 4h, 12h, 1d, 1w}: `{L_bars, source {path, key,
   sha256}, label, source_lens}`; `laws` {`accept_n`, `margin_atr`, `ret_k`, `nest_frac`, `bins`, `value_area`, `atr_len`,
   `floor_n`, `null_draws`, each with its source}. R: both doors, the pin register.
2. **`va/va_bars_<ℓ>.parquet`**, ℓ ∈ {1h, 4h, 12h, 1d, 1w} (DOOR 1 · `TC12-V`) — key `[asset, open_ms]`; one row per bar,
   KNOWN AT `close_ms`:

   | columns | dtype | meaning |
   |---|---|---|
   | `asset`, `panel` | str | stem; `CLASSIC5` or `UNSEEN12` |
   | `open_ms`, `i`, `close_ms` | int64 | bar open; index on the lens tape; bar close (= the row's known-at) |
   | `era`, `in_strip` | str, bool | tuning iff `close_ms ≤ ERA_CUT` else holdout; `close_ms > W` |
   | `L`, `l_label` | int64, str | lookback and its label |
   | `close`, `atr`, `volume` | float64 | `c[t]`, `ATR_ℓ[t]`, `v[t]` |
   | `val`, `poc`, `vah` | float64 | the profile IN FORCE from `close_ms`: `VA(t)` — the levels an order placed at or after `close_ms` rests on |
   | `val_edge`, `vah_edge`, `window_lo`, `window_hi` | float64 | the edges twin and the window's range (used by nothing) |
   | `val_j`, `poc_j`, `vah_j` | float64 | the JUDGING profile `VA(t−1)` |
   | `tpo_poc`, `tpo_val`, `tpo_vah` | float64 | the time-at-price twin |
   | `state` | str | the machine after bar t, a member of `STATE_NAMES` |
   | `armed_top`, `armed_bottom`, `inside_frozen_only` | bool | the two flags; `inside_frozen_only` = the bar resolved a probe and `state == "INSIDE"` by the frozen edge while `close` lies outside `[val_j, vah_j]` |
   | `probe_side`, `probe_t0`, `probe_t0_close_ms`, `probe_edge` | int8, int64, int64, float64 | the pending probe (0 / −1 / −1 / NaN when none) |
   | `regime_r0`, `last_accept_i` | int64 | −1 when none |
   | `pct`, `edge_dist_atr`, `d_vah_atr`, `d_val_atr`, `poc_dist_atr` | float64 | L-V.16, against the judging profile |
   | `near_side` | int8 | +1 VAH nearer (tie → VAH), −1 VAL |
   | `va_age`, `accept_age` | Int64 (nullable) | L-V.16 |
   | `up_k`, `up_bar_close_ms` | int64 | the L+1 bar read for the nest (−1 when none) |
   | `coin_vah_vah`, `coin_vah_val`, `coin_val_vah`, `coin_val_val`, `coin_vah`, `coin_val` | boolean (nullable) | L-V.21 |
   | `coin_min_atr` | float64 | L-V.21 |

   R: the reader (`bars`, `stamp`); through it L-R (P-DIR-1: `state`, `close_ms`; printed `pct`, `edge_dist_atr`,
   `accept_age`, `armed_*`; the chop tables; the 1d venue: `state`, `val`, `vah`, `atr`), L-S (1h: `close_ms`, `state`,
   `val`, `poc`, `vah`, `atr`, `va_age`; 4h: `close_ms`, `state`), DOOR 2, the stamps.
3. **`va/va_events.parquet`** (DOOR 1 · `TC12-V`) — key `[lens, asset, kind, side, i, t0]`; one row per event, KNOWN AT
   `known_close_ms`; no field depends on a bar after `i`:
   `lens`, `asset`, `kind` ∈ {`probe`, `acceptance`, `swing_failure`, `lapse`, `decay`}, `side` ∈ {`top`, `bottom`, `both`}
   (str); `t0`, `t0_close_ms`, `i`, `known_close_ms`, `bars_out`, `closes`, `rid`, `r0`, `episode` (int64); `era` (str),
   `in_strip` (bool); `by` (str: `n_closes` / `margin` / empty); `E` (the frozen edge = that edge of `VA(t0−1)`),
   `extreme` (the DEVIATION EXTREME: `max(h[t0..i])` top / `min(l[t0..i])` bottom, return bar included), `close_i`,
   `atr_i`, `excess_atr` (float64); `sgn` (int8); `val_f`, `poc_f`, `vah_f` (the FROZEN profile `VA(t0−1)`), `val_n`,
   `poc_n`, `vah_n` (`VA(i)`) (float64); `ret_inside_frozen`, `ret_inside_rolling` (boolean, nullable); `from_state`,
   `state_after` (str). **`end_kind` and `end_i` are struck** (CAU-04): how a probe ended is read from its resolving row
   (`swing_failure` / `lapse` / `acceptance`), joined on `(lens, asset, side, t0)`; a probe with no resolving row is
   pending. R: L-R (swing-failure rows; acceptance rows for invalidation and its `E`), L-S (1h acceptance rows: `lens`,
   `kind`, `side`, `known_close_ms`, `by`, `bars_out`, `E`), DOOR 2.
4. **`va/va_regimes.parquet`** (DOOR 1 · `TC12-V`) — key `[lens, asset, rid]`: `r0`, `r0_close_ms`, `start_kind`, `die_i`,
   `die_close_ms`, `end_side`, `end_by`, `n_bars`. **A SUMMARY table, not an as-of table:** a consumer bounded at an
   instant B treats a regime with `die_close_ms > B` or null as alive at B and reads none of its `die_*`, `end_*`,
   `n_bars`; the reader offers `regimes(asof_close_ms=B)` and no unbounded form.
5. **`va/traverse_legs.parquet`** (key `[lens, asset, rid, leg_seq]`, L-V.18's columns) and **`va/TRAVERSE.json`** (DOOR 1 ·
   `TC12-V`; the traverse pin record) — `by_lens.<ℓ>` for ℓ ∈ {1h, 4h, 12h, 1d}: `{T_of_record, n_legs, lower_hinge,
   median, upper_hinge, per_asset_median, label, provisional}`; `by_lens.1h.T_in_5m_bars`; `twins.strict_inside.<ℓ>`:
   `{T_strict_inside, n_legs_strict, lower_hinge, median, upper_hinge}` (CANON-20); `twins.scored_window.<ℓ>`,
   `twins.holdout.<ℓ>`; `x_pivot_T.<ℓ>`. R: the reader's `traverse(name)` only.
6. **`va/VA_MIRROR.json`** (DOOR 1 · `TC12-V`; a REGISTERED record, no collar) — `x_file {path, sha256}`; `words` (the
   five, each `{lens, toll, word, x_row, would_read, verdict_pass, of_record_for_detector, toll_bps, edge_net_h20}`);
   `licence["<lens>|<toll>"].by_era[<ALL|tuning|holdout>]` = `{would_read, verdict_pass, edge_net_h20, toll_bps, x_row,
   n_ranges, ratio_median, share_ratio_lt_1, edge_n, edge_n_ranges, edge_median_term_h20, edge_toll_atr}` — every value
   QUOTED from X's row [checked: the columns exist in `feasibility.parquet`]; `licence_set` (list of `"<lens>|<toll>"`);
   `beside` {the 12h maker rows, the 1h `lens_word` sentence, `twin_words {"4h|maker": {would_read (X's holdout row),
   toll_bps, edge_net_h20, x_row}}`}. **TC12 computes no number in this file; there is no `at_maker_pin` block**
   (CANON-17). R: the reader's `licence`; the scorer's precondition evaluator; the report.
7. **`va/va_stack.parquet`** (key `[asset, lens, era]`), `va/STAGE_V.md`, `va/build_manifest.json`,
   `va/FIXTURES_STAGE_V.txt` (DOOR 1 · `TC12-V`).
8. **`va/trades/`** (DOOR 2 · `TC12-V.trades`):
   - `va_null_events.parquet` — the L-V.14 schema plus `draw`, `phase`, `perm_sha`; the volume null `tr_tercile_lblock`;
     lenses 4h, 1d × the five home assets;
   - `NULL_BOXES_VA.parquet` — key `[lens, asset, draw, box]`: `src_rid`, `confirm_i`, `life`, `censored`, `bot`, `top`,
     `u`, `lead_gap_swapped`, `identity_perm`; the real box set is cut at W: regimes with `r0_close_ms ≤ W` are kept, a
     kept regime whose `die_close_ms > W` or is null is the alive one (`life = n − r0`, censored), regimes with
     `r0_close_ms > W` are dropped (plant: a strip-dying regime's filed `die_i` used → `NULL-STRIP` RED);
   - `va_null_go_events.parquet` — the L-V.14 schema plus `draw`, `box`: the gaps+order@va_regime box events;
   - `TWO_TRADES_EVENTS.parquet` (key `[lens, asset, trade, side, anchor_i, i]`), `TWO_TRADES_VA.parquet`,
     `TWO_TRADES_VA_UNCOND.parquet`, `TWO_TRADES_BASE.parquet`, `TWO_TRADES_NULL.parquet`,
     `TWO_TRADES_NULL_DRAWS.parquet` (L-R.26-L-R.29's definitions; `u_lookback_label` per CANON-04; every row carries
     `l_label`);
   - `TWO_TRADES.md` (the stage document of record: every grid whole), `build_manifest.json`, `READ_SET.json`,
     `FIXTURES_VA_TRADES.txt`.
   R: the report (pointers); nobody else.
9. **`va/stamps/VA_STAMPS_<book>.parquet`** (the reader · `TC12-V.stamps.c/.r/.s`; CANON-10). The block of lens ℓ, prefixed
   `<ℓ>_`: `k`, `bar_close_ms`, `stale_ms`, `state`, `armed_top`, `armed_bottom`, `pct`, `edge_dist_atr`, `near_side`,
   `d_vah_atr`, `d_val_atr`, `poc_dist_atr`, `va_age`, `accept_age`, `close`, `atr`, `val_j`, `poc_j`, `vah_j`, `val`,
   `poc`, `vah`, `probe_side`, `probe_t0_close_ms`, `probe_edge`, the nest columns, `L`, `l_label`. R: L-R.4 (the `entry`
   rows of `v6`), L-L.16 (the `entry` rows of `v6` and `trg912`), the report.

**PER-SECTION EDITS.**
- **L-V** — L-V.14: strike `end_kind`, `end_i` from the field table (keep `episode`) and add the two sentences of point 3
  and point 4; L-V.24's outputs table = points 1-9 (with `inside_frozen_only`, the struck fields, `va/trades/`,
  `va/stamps/`); L-V.17 item 7: the `by_era` leaf and `beside.twin_words` per point 6; L-V.18 "Freeze": `TRAVERSE.json`
  keys per point 5; L-V.23: files per point 8; L-V.13 (i): the counted case is filed per bar as `inside_frozen_only`.
- **L-R** — L-R.3, L-R.10, L-R.17, L-R.22, L-R.26-L-R.30: every column name above as written; L-R.29: "The real box set"
  bullet gains the cut-at-W sentence of point 8 and reads the regimes through `regimes(asof_close_ms=W)`; files
  `va/trades/…`. INTERFACE (L-V): the list of what L-V files = points 2-6, 8.
- **L-S** — L-S.1 read set item 2 and "the complete typed list": unchanged names (they are point 2's and point 3's);
  L-S.4 prints the count of orders whose row `k1` carries `inside_frozen_only`.
- **L-L** — L-L.25: rows for `va/trades/*` and `va/stamps/*` per CANON-33.
- **L-0** — L-0.22: "Every filed Stage V table is asserted against the sha its record carries (through `certified()`)
  before use."

---------------------------------------------------------------------------------------------------------------
## CANON-12 · THE READER — `scripts/tierc12_va_stamps.py`
**Settles:** BLD-16, BLD-17, BLD-01 (the sha law), CAU-04 (the bounded forms). **Also cited by the dispositions of:** FID-02. **Authority:** OD-2.

**CANON TEXT.** A decision module; imports `tierc12_env`, `tierc12_asof`, `tierc12_tables`, pandas, numpy; never
`analytics.value_area`, `analytics.profile` or a door; recomputes nothing; contains no comparison of a price with a level.
Before the first read of any Stage V file in a process it asserts the file's sha256 equals `certified(path).sha256`, HALT
otherwise. `root=` (an explicit directory holding tables and a `build_manifest.json`) may be passed by `_fixtures` modules
and by DOOR-side twins only (AST); the sha is then asserted against that manifest.

| function | returns |
|---|---|
| `bars(lens, *, asof_close_ms=None, root=None)` | `va_bars_<lens>` sorted `[asset, close_ms]`; with `asof_close_ms`, the rows with `close_ms ≤` it |
| `events(*, lens=None, kind=None, asof_close_ms=None, root=None)` | `va_events` rows; with `asof_close_ms`, the rows with `known_close_ms ≤` it |
| `regimes(*, asof_close_ms, lens=None, root=None)` | `va_regimes` rows with `r0_close_ms ≤ asof_close_ms`; for a regime alive at that instant `die_i`, `die_close_ms`, `end_side`, `end_by`, `n_bars` are null and `alive_at_asof` is True. `asof_close_ms` is REQUIRED: no unbounded form exists |
| `instants_of(frame, kind)` | `[book, symbol] + kind.key + [instant_kind, instant_ms]` (CANON-10 point 2) |
| `stamp(instants, *, root=None)` | the instants joined, per lens, to row `k = asof_index(close_ms_ℓ, instant_ms)` of `va_bars_<ℓ>`, as filed, with `stale_ms` and the gap guard of L-V.21 |
| `licence(lens, toll, era)` | the `VA_MIRROR.json` leaf `licence["<lens>|<toll>"].by_era[<era>]`; HALT for a pair outside `licence_set`; each call is appended to the process's `licence_reads` (written into `READ_SET.json`, CANON-28) |
| `traverse(name)` | `(value, source)`: `name ∈ {"traverse.1h", "traverse.4h", "traverse.12h", "traverse.1d", "traverse.1h.in_5m_bars"}`; `value` = the int at `TRAVERSE.json by_lens.<lens>.T_of_record` (or `by_lens.1h.T_in_5m_bars`); `source = {path, key, sha256, value}` for the book manifest's `time_stop_source`. **This is "the fitted-pin door".** |
| CLI `--file-stamps --stage=TC12-V.stamps.<c|r|s>` | CANON-10 point 1 |

**PER-SECTION EDITS.**
- **L-V** — L-V.2 reader bullet: the paragraph and table above; L-V.18: "a consumer reads them only through the reader's
  `traverse(name)`, which HALTs unless the file's sha is the certified one"; L-V.17 item 9: `licence` logs its reads.
- **L-0** — L-0.17 "Fitted pins": "the traverse (O-18) — the door is `tierc12_va_stamps.traverse`".
- **L-R** — L-R.16: "read through `tierc12_va_stamps.traverse("traverse.4h")`"; L-R.24 (1d cell): `traverse("traverse.1d")`;
  L-R.32 row `T`: door = the reader's `traverse`. INTERFACE (L-D) "`E.load_asof`" → "`E.D.load_asof(stem, lens)`".
- **L-S** — L-S.1 read set item 3 and L-S.20: "`tierc12_va_stamps.traverse("traverse.1h.in_5m_bars")`"; L-S.2 row `T5`.
- **L-L**, **L-G**, **L-C** — no edit (L-L.16 reads `VA_STAMPS_*` through `certified()`).

---------------------------------------------------------------------------------------------------------------
## CANON-13 · ONE GEOMETRY LAW FOR BOTH RANGE ROWS
**Settles:** FID-07, TRD-03, CMP-25 (geometry), TRD-07 (b). **Authority:** OD-8, contract :70, :73-74, :100. **Taken:** OD-8's
comparators and slugs (`≤ 0`; `poc_not_ahead`, `t2_not_ahead`) over TRD-03's strict `< 0` / `poc_behind_entry` /
`t2_not_beyond_entry` and TRD-07's `no_order_t2_not_beyond_entry`. Consequence stated: on P-SCALP-3 a T1 at the entry price
is REFUSED (`poc_not_ahead`), not "traded as written" as L-S.11 drafted.

**CANON TEXT.** With `e` the entry price (P-SFP-VA-1: `lf.c[i]`, the return bar's close; P-SCALP-3: the limit `L = px(n_L)`),
`d` the direction, `T1`, `T2` the targets and `R` the stop distance after the rail (P-SCALP-3 compares in integer ticks:
`n_T1`, `n_T2`, `n_L`):
1. An event (trigger) is **REFUSED and counted**, after the one-position (one-order) test and BEFORE the reward test, with
   the first reason that holds: (1) `stop_none` — the stop function returns none; (2) `poc_not_ahead` — `d·(T1 − e) ≤ 0`
   (the contract's "toward the POC" has no object; never reversed); (3) `t2_not_ahead` — `d·(T2 − e) ≤ 0`. These three
   hold in EVERY book, the unfiltered twins included: an order whose target is not ahead is not an order.
2. **Not refusals:** `t1_within_fee_band` := `0 < d·(T1 − e) ≤ (G / BPS_PER_UNIT)·e`, `G = E.R2.FEE_BPS_ROUND_TRIP` — the
   trade is taken as written, the flag is filed and counted, `fee_band_r = (G / BPS_PER_UNIT)·e / R` printed. `t1_void` :=
   `d·(T2 − T1) ≤ 0` — no T1 order exists and the WHOLE position exits at T2; filed and counted. There is no fee band and
   no inverted-targets refusal.
3. **The one skip** is the contract's: `rr_min` — skipped iff `d·(T2 − e) / R < RR` (pin `rr_min`). The unfiltered twins
   (`tierE__unfiltered`, `tierE__rr_unfiltered`) drop this test and nothing else, re-walked with their own sequence.
4. **Reason slugs of record** (in `SFP_EVENTS.disposition` and `S_refusals_<book>.reason`): `stop_none`, `poc_not_ahead`,
   `t2_not_ahead`, `rr_min`, plus each book's own sequencing reasons (`one_position`; `refused_order_resting`,
   `refused_position_open`). The scalper's `no_order_atr` and `skipped_rr_min` are renamed `stop_none` and `rr_min`.
5. **X's geometry law** (the 10-bps band refusals `t1_within_10bps`, `t2_within_10bps` and `targets_inverted`;
   `x_rec/scripts/tc11x_sfp.py:503-513`) is kept behind a declared switch — `tierc12_rangewalk.geometry(…, law)`, `law ∈
   {"tc12", "x"}` — whose `"x"` value has exactly two call sites (AST-typed): F-SFP-MIRROR on X's filed rows, and the
   Tier-E arm `tierE__x_geometry` of P-SFP-VA-1 (TC12's law everywhere else; its own one-position sequence; the rows that
   differ from the record listed).

**PER-SECTION EDITS.**
- **L-R** — L-R.14: replace the reading by points 1-2 and 5 (title "DEGENERATE GEOMETRY — OD-8"); RIVALS: "X's fee-band and
  inverted-targets refusals — not taken on the record (OD-8: the contract's only skip is rr-min); printed as
  `tierE__x_geometry`"; FAILS-IF mutations: a planted event with the POC behind the entry admitted; a `t1_void` event
  refused. L-R.10: "fails the geometry law of L-R.14 by itself" stays. L-R.11: "REFUSED (L-R.14, `poc_not_ahead`)". L-R.12:
  the remainder "or the whole position if T1 is void or has not filled". L-R.15: order of tests unchanged; slugs per
  point 4. L-R.19: "no T1 order exists on a `t1_void` trade". L-R.24: add `tierE__x_geometry` (point 5). L-R.32: the row
  "fee band `G`" reads "the flag `t1_within_fee_band` and the arm `tierE__x_geometry`; witness: the flag of a planted
  event at the band's edge". P-SFP-VA-1 spec `arms`: "Refused (geometry) iff the stop is undefined, or `d·(T1 − e) ≤ 0`
  (the POC is not ahead of the entry), or `d·(T2 − e) ≤ 0`. Not a refusal: `d·(T2 − T1) ≤ 0` voids T1 and the whole
  position exits at T2. Skipped (rr-min) iff `d·(T2 − e) / R < 1.5` (contract :73)."; `disclosed_beside`: add
  `tierE__x_geometry`; strike "T1-collapse" from the counted rivals.
- **L-S** — L-S.11: replace "No other geometry refusal … could only raise a mean" by "Geometry refusals are OD-8's, in
  ticks: `poc_not_ahead` iff `d·(n_T1 − n_L) ≤ 0`; `t2_not_ahead` iff `d·(n_T2 − n_L) ≤ 0` — in every book,
  `tierE__rr_unfiltered` included; `t1_within_fee_band` is a flag, not a refusal; X's 10-bps refusal is not carried."
  Keep the void-T1 bullet. L-S.10: `no_order_atr` → `stop_none`. L-S.12: `skipped_rr_min` → `rr_min`; the twin "differs
  from the record by the rr-min test alone on orders that can exist". L-S.14: reasons per point 4. L-S.30: `S_refusals`
  reasons per point 4. P-SCALP-3 spec `arms` ORDER sentence: "T1 void when it lies at or beyond T2; refused when T1 or T2
  is not ahead of the limit". INTERFACE (L-R): "one geometry law (OD-8) and one gap law (OD-9) for both rows".

---------------------------------------------------------------------------------------------------------------
## CANON-14 · ONE GAP LAW, ONE SAME-BAR ORDER — the pessimistic one
**Settles:** TRD-01, CMP-25 (gap). **Authority:** OD-9. **Taken:** OD-9 over TRD-01's fix text (X's symmetric law with an
open-decides-first step for targets): no target is decided at the open in either simulator.

**CANON TEXT.** Each bar `j` of a walk (P-SFP-VA-1: 4h bars `j > entry_i`; P-SCALP-3: 5m bars `j ≥ f` with L-S.17's fill-bar
rules) is stepped once on what is still open, in this order (`S` the stop, `adv` / `fav` the bar's adverse / favourable
extreme):

| step | test | act |
|---|---|---|
| 1 · STOP at the open | `d·(o[j] − S) ≤ 0` | exit ALL at `o[j]` (the worse price); reason `stop`; `gap_stop = True` |
| 2 · STOP, adverse-first | `d·(adv − S) ≤ 0` | exit ALL at `S`; reason `stop`; `both_touch` counted if a target test holds on this bar; `stop_bar_open_through_target` counted if the bar opened at or beyond a resting target |
| 3 · T1 (resting, not void; never on a zero-volume bar) | P-SFP-VA-1: `d·(fav − T1) ≥ 0`; P-SCALP-3: the book's fill rule at `n_T1` | the T1 fraction exits at the LEVEL (`T1`; `px(n_T1)`); `gap_t1 = True` iff the bar opened at or beyond the level — no gap improvement is booked |
| 4 · T2 (never on a zero-volume bar) | likewise at T2 | the rest exits at the LEVEL, on the same bar as T1 if reached; `gap_t2` |
| 5 · close events | INVALIDATION, then TIME STOP, then CORRIDOR END | exit the rest at `c[j]` |

- There is NO open-decides-first step for a target; the stop is tested before any target on every bar.
- On P-SFP-VA-1 the targets are touch-triggered TAKER exits booked at their level; on P-SCALP-3 they are resting MAKER
  limits booked at their grid price.
- **X's record law** (the open decides first for stop and targets; a stop books the stop price through a gap; a target
  books `max(level, open)` long / `min` short) is kept behind a declared switch — `tierc12_rangewalk.bar_step(…,
  gap_law)`, `gap_law ∈ {"tc12", "x_record"}` — whose `"x_record"` value has exactly two call sites (AST-typed):
  F-SFP-MIRROR against X's filed X2 rows, and the Tier-E arm `tierE__x_gaplaw` of P-SFP-VA-1 (its own one-position
  sequence).

**PER-SECTION EDITS.**
- **L-R** — L-R.19: replace steps 0-3 by the table (steps 1-4) and step 4 by step 5; first sentence "The tier's one walk
  law (OD-9), on the 4h bars …"; RIVALS: "X's record law — not taken on the record (it favours the trader on both sides,
  `x_rec/tierc11x/LEANS_X.md:1308-1310`); printed as `tierE__x_gaplaw`"; plants: "a gap stop booked at the stop price";
  "a target credited at `max(level, open)`"; "target-before-stop on a both-touch bar". L-R.12: add "T1 and T2 are
  touch-triggered TAKER exits booked at their level." L-R.17: "the intrabar law of L-R.19 runs first: the stop at the
  open, the stop by range, T1, T2". L-R.24: every twin and the 1d cell inherit the law; add `tierE__x_gaplaw`. L-R.25
  F-SFP-MIRROR: "the mirrored step with `gap_law = "x_record"`, `geometry law = "x"` and the invalidation switched off,
  against X's filed rows"; the hand-walk order "STOP AT OPEN → STOP → T1 → T2 → INVALIDATION → TIME STOP". P-SFP-VA-1 spec
  walk sentence: "a bar opening at or beyond the stop exits at the open; else the stop, adverse-first, at the stop price;
  then T1 at T1; then T2 at T2, same bar if reached; a target books its level with no gap improvement; then at the close
  the invalidation … then the time stop …".
- **L-S** — L-S.18: the table is the canon's (its rows 1-7 already agree); add `stop_bar_open_through_target` to the STOP
  row (already counted); strike "X's open-decides-first step for a TARGET (LX-X2.10 step 0) is not carried" as a
  difference from L-R and write "one law with P-SFP-VA-1 (OD-9)". INTERFACE (L-R): strike the three differences.

---------------------------------------------------------------------------------------------------------------
## CANON-15 · FUNDING IS NOT CAPPED ON THE RANGE ROWS
**Settles:** TRD-04. **Also cited by the dispositions of:** CAU-14. **Authority:** OD-10 [checked: `account_l` returns `funding_r_uncapped` and `funding_ceiling_bound`,
`scripts/tierc10_brk.py:1322-1324`].

**CANON TEXT.** On every arm of P-SFP-VA-1 and P-SCALP-3 (and on the scalper's would-have walks): `funding_r =
acc["funding_r_uncapped"]`; `net_r = gross_r − fee_r − funding_r`; `taker_twin_net_r = gross_r − fee_all_taker_r −
funding_r` (so L-X.24's identity `taker_twin_net_r == net_r + fee_r − fee_all_taker_r` holds exactly); filed beside:
`tc_series_net_r = acc["net_r"]` (the lineage's own booking, D12 ceiling included) and `funding_ceiling_bound`. "Taker twin
== TC-series" is held as: `|taker_twin_net_r − tc_series_net_r| ≤ HAIRCUT_TOL` on every row with `funding_ceiling_bound ==
False`, and `taker_twin_net_r < tc_series_net_r` on the others; the bound count per arm is printed. The D12 ceiling stays
what it is on every v6-derived book (control, gates, ledger): a v6-card accounting rule. F-SFP-MIRROR compares X's filed
`funding_r` with `acc["funding_r"]` (capped, as X booked it).

**PER-SECTION EDITS.**
- **L-R** — L-R.20: "Funding" bullet: strike "The D12 ceiling … is taken once, on a cost only" and write the three
  assignments above; the taker identities line gains `tc_series_net_r`; FAILS-IF (f) adds the two-case identity. P-SFP-VA-1
  spec booking sentence: "interval-sum funding, uncapped (the D12 ceiling is a v6-card rule and is not a rule of this
  trade)".
- **L-S** — L-S.21: "`funding_r = acc["funding_r_uncapped"]` … The D12 ceiling is a v6-card accounting rule and is not a
  rule of this trade." L-S.22: `taker_twin_net_r = gross_r − fee_all_taker_r − funding_r`, `tc_series_net_r = acc["net_r"]`
  filed beside. L-S.23: the would-have walks book uncapped funding. L-S.32 (t2): the two-case identity; the bound count
  per arm printed in the fill-sensitivity block.
- **L-X** — L-X.24 "Meaning": "`funding_r` is the journaled funding, positive = paid — capped by the card's D12 rule on
  v6-derived arms, UNCAPPED on range arms (OD-10)"; the two conditional columns of CANON-07.

---------------------------------------------------------------------------------------------------------------
## CANON-16 · ONE FILL RULE FOR MAKER LEGS
**Settles:** TRD-05. **Authority:** OD-11, contract :93-94.

**CANON TEXT.** Every maker leg of the tier fills by the fill of record. P-SFP-VA-1's `tierE__maker_conditioned`: with
`grid = TickGrid(E.ticks()[stem])`, `n_tick` = the pin `scalp.fill_ticks`, the conditioned entry at `P = e` books iff, on
the FIRST 5m child of bar `entry_i + 1`, `grid.dec(low) < grid.dec(P) − n_tick·grid.T` (long) / `grid.dec(high) >
grid.dec(P) + n_tick·grid.T` (short), evaluated exactly in the grid's trapping decimal context; its maker targets fill
likewise against their levels; a zero-volume child fills nothing. X's law (`low < P`, no tick) runs only inside
F-SFP-MIRROR's leg against `X2_twins.parquet` book `maker_conditioned`, and the number of fills X's law would add is
printed (`x_law_extra_fills`). The twin's sidecar carries `fill_rule = "tick"`.

**PER-SECTION EDITS.**
- **L-R** — L-R.24 `tierE__maker_conditioned`: replace "trades strictly through it — `low < P` … maker targets fill only on
  trade-through (strict)" by the text above; RIVALS: strike "this twin keeps the law its filed precedent used, and the
  difference is listed for the reviser"; L-R.32: add the consumer TC12-R to `scalp.fill_ticks`. INTERFACE (L-S): "one
  fill law for every maker row in the tier (OD-11)". P-SFP-VA-1 spec `disclosed_beside`: "the conditioned arm books only
  if the first 5m bar after the entry close trades through the entry price by the fill of record (one tick, exact)".
- **L-S** — L-S.2: `scalp.fill_ticks` consumers = TC12-S and TC12-R.

---------------------------------------------------------------------------------------------------------------
## CANON-17 · P-SCALP-3 HAS ONE PRECONDITION; THE PINNED-RATE LEAF IS PRINTED BESIDE
**Settles:** FID-08, STA-02, CMP-21 (option B), BLD-15. **Authority:** OD-12, O-17, O-19. **Taken:** OD-12 over BLD-15's fix
(keep item 2 as `at_maker_pin.qr3_pass`) and CMP-21's option A — not built.

**CANON TEXT.**
1. P-SCALP-3's `preconditions` field holds ONE item: `{record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by:
   progress/TC12-V.json artifact_shas, selector: licence["1h|maker"].by_era["holdout"].would_read, required: "PASS"}`.
2. **Printed beside the licence word, deciding nothing (O-19).** The SCORER computes the collared beside leaf
   `licence_at_maker_pin` on P-SCALP-3: `{maker_bps_side (E.fees(), one maker rate over the five home stems asserted),
   round_trip_bps = 2·maker_bps_side, x_toll_bps (the row's quoted toll_bps), differs_from_x_assumption (Stage D's
   maker_pin flag), edge_net_h20_at_pin = round(edge_median_term_h20, ND) − round(edge_toll_atr × round_trip_bps /
   x_toll_bps, ND)}` from the columns `VA_MIRROR.json` QUOTES for the 1h|maker holdout row (CANON-11 point 6), `ND` = X's
   `pins.laws.round_nd`; where the pin equals X's assumption the figure must equal the quoted `edge_net_h20`. It carries no
   word, is labelled "a re-derivation of one leg from printed columns; not a licence", and is printed in the verdict text
   and in §0.3. If `edge_net_h20_at_pin ≤ 0` the cell carries the qualifier `LICENCE EDGE ≤ 0 AT THE PINNED MAKER RATE (X
   assumed <x> bps round trip; pinned <y>)`; the row is still built, scored, and spends its test.
3. Closing the row on that figure is the operator's order, by name, before Stage D's fee capture.

**PER-SECTION EDITS.**
- **L-S** — L-S.27: "one item"; delete item 2 and the sentence "item 2 is undetermined until Stage D's fee capture"; add
  point 2 as the paragraph "Printed beside, never a precondition (O-19)"; RIVALS: "a second, closing item on the
  re-derived edge leg — not taken: OD-12, O-17 (the mirror reads, never recomputes)"; FAILS-IF (p): strike the fee-file
  plant and "item 2 evaluated at X's rate"; add "a closing second item planted in a copy of the spec → `PRECOND-GRAMMAR` /
  TEMPLATE mismatch at filing". P-SCALP-3 spec `preconditions`: the one brace item of point 1 (CANON-36 grammar). L-S.31
  (p): "the taker row; the ALL era". OPEN TO OPERATOR 2: "A published maker rate at which X's edge leg is not above zero.
  DEFAULT if silent: the row is built and scored, with the re-derived figure printed beside the word (O-19). Closing the
  row on it is the operator's order, by name, before Stage D's fee capture." INTERFACE (L-V): strike addition (i);
  INTERFACE (L-X): strike "item 2 of this row names two certified records …". OBJECTIONS third note: "L-S.27 prints the
  re-derived edge leg beside the word (O-19, OD-12)". Unverified list: strike "hence precondition item 2".
- **L-X** — L-X.10: "On the records as filed no item fails" stands; L-X.14: add the slug `licence_at_maker_pin` (P-SCALP-3
  only) to the table; L-X.9: add the qualifier of point 2 to the qualifier list.
- **L-V** — L-V.17 item 7: the quoted columns of CANON-11 point 6; no `at_maker_pin` block; item 10 unchanged.

---------------------------------------------------------------------------------------------------------------
## CANON-18 · THE KILL TABLE — a closure word needs a MEASURED failure
**Settles:** FID-14, STA-06, STA-12, STA-13. **Also cited by the dispositions of:** FID-20, STA-14. **Authority:** OD-13, OD-19, contract :104-106.

**CANON TEXT.**
1. For each fill book X ∈ {TOUCH, TICK, DEEP}, at the seed of record and the SCALPER bar: `U(X)` = X is not PANEL COMPLETE
   (its ruler is undefined; an EMPTY BOOK is the limiting case); `C(X)` = PANEL COMPLETE and clauses (a) ∧ (b) hold; `F(X)`
   = PANEL COMPLETE and (a) or (b) fails. Exactly one of the three holds. `D` = fewer than `above_half_bar(N)`
   leave-one-asset-out panels of the TICK book exclude zero from above (L-X.11).
2. **The word:**

   | TICK | D | DEEP | TOUCH | `verdict_of_record` | qualifier |
   |---|---|---|---|---|---|
   | C | false | C | any | `SUPPORTED` | — |
   | C | false | F | any | `SUPPORTED` | `FILL-SENSITIVE (does not clear under DEEP)` |
   | C | false | U | any | `SUPPORTED` | `FILL-SENSITIVE (DEEP PANEL INCOMPLETE)` |
   | C | true | any | any | `NOT SUPPORTED` | `LOAO BELOW THE LINE (k/N above; passing when dropped: <assets>; failing when dropped: <assets>)` |
   | U | any | any | any | `NOT SUPPORTED` | `PANEL INCOMPLETE (…)` / `EMPTY BOOK` and `TICK PANEL INCOMPLETE — closure not ruled` |
   | F | any | C | any | `NOT SUPPORTED` | — |
   | F | any | U | any | `NOT SUPPORTED` | `DEEP PANEL INCOMPLETE — closure not ruled` |
   | F | any | F | C | `NOT SUPPORTED — CLOSED` | `(clears only under TOUCH)` |
   | F | any | F | U | `NOT SUPPORTED — CLOSED` | `TOUCH PANEL INCOMPLETE — "for good" not ruled` |
   | F | any | F | F | `NOT SUPPORTED — CLOSED FOR GOOD` | — |

3. The verdict text and `SCORES.json rows[].fill_ladder` carry two booleans, printed in the fill-sensitivity row:
   `fails_under_deep_too = F(TICK) ∧ F(DEEP)`; `clears_only_under_touch = F(TICK) ∧ F(DEEP) ∧ C(TOUCH)`.
4. The fill-sensitivity row opens with the fixed sentence: "TOUCH and DEEP are fill-model twins, not tests: they are ruled
   at the family bar without a test of their own and can only qualify a SUPPORTED cell or choose among the failure words;
   an interval that excludes zero on either is not a result."
5. The LOAO qualifier's fixed sentence in the verdict text: "the contract reads one-asset dependence by this line (:106);
   a panel that fails when an asset is DROPPED leans on that asset, a panel that fails while an asset is KEPT is dragged
   by it". The rule for `D` and the word are unchanged; the qualifier `ONE-ASSET DEPENDENT (LOAO k/N)` is renamed as in the
   table.
6. **Operator item (OD-19):** "CLOSED versus CLOSED FOR GOOD when TICK and DEEP fail and TOUCH clears. Both contract
   clauses hold there (:104-105). Default if silent: `NOT SUPPORTED — CLOSED` (clears only under TOUCH), so that each
   clause has a live event; the literal-order rival (CLOSED FOR GOOD whenever TICK and DEEP fail) is the operator's to
   name."
7. F-VERDICT `[LADDER]` enumerates every (TICK, D, DEEP, TOUCH) combination over the three states C / F / U; plants: TOUCH
   and DEEP swapped; the D column dropped; a closure word produced on a U book.

**PER-SECTION EDITS.**
- **L-X** — L-X.9: definitions of point 1 after "Let `C(X)` …"; the table of point 2 replaces the six-case table; "Why rows
  five and six split" stays for the F/F/C row; "One test" bullet gains point 4; the verdict-text bullet gains point 3 and
  point 5; qualifier list: replace `ONE-ASSET DEPENDENT` by `LOAO BELOW THE LINE (…)` and add the three PANEL INCOMPLETE
  closure qualifiers; FAILS-IF per point 7. L-X.7: "Clause (c) applies to each fill-ladder book of P-SCALP-3: a book that
  fails it is U(X), which never closes (L-X.9)". OPEN TO OPERATOR: new item 7 = point 6. Common clauses "verdict_rule,
  P-SCALP-3 only": "L-X.9's table verbatim, the definitions of C, F, U and D, …".
- **L-S** — L-S.28: the eight-row TOUCH/TICK/DEEP table is rewritten over C / F / U from point 2 (rows where a book is U
  shown); "CLOSED FOR GOOD … (it fails at the most generous one)" → "(it has a MEASURED failure at every fill model)"; the
  verdict-text bullet gains points 3-5; the qualifier name per point 5. P-SCALP-3 spec `verdict_rule`: the definitions, the
  table's ten cases in place of the six, the two booleans, the two fixed sentences. OPEN TO OPERATOR: add an item mirroring
  point 6 (and CANON-32's else-clause item); item 4 keeps its text with the renamed qualifier.

---------------------------------------------------------------------------------------------------------------
## CANON-19 · ERA, SCORED WINDOW, STRIP — one wording
**Settles:** CMP-20; fixes one wording for L-C.10, L-G.1, L-R.21, L-S.25, L-X.24, L-L.17, L-V.24. **Also cited by the dispositions of:** CAU-10. **Authority:** O-9, OD-14.

**CANON TEXT.**
1. `W = E.TC11_PIN_MS` (`T11/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]`); `PIN = E.PIN_MS`
   (`T12/data/AS_OF_PIN.json`, same key); `ERA_CUT = E.ERA_CUT_MS`. A row's instant is its `entry_close_ms`: the close of
   the lens bar in which the position was entered (v6: the 4h entry bar; P-SFP-VA-1: the return bar; P-SCALP-3: the 5m
   fill bar).
2. **Scored window:** rows with `entry_close_ms ≤ W`. The book is ridden with `hi` = the last bar of its own clock closing
   `≤ W`; a position still open there is marked at that bar's close with `exit_reason = "corridor_end"`
   (`exit_close_ms ≤ W` on every row).
3. **Strip:** rows with `W < entry_close_ms ≤ PIN`, taken from a second ride with `hi` = the last bar closing `≤ PIN`. FOR
   EVERY RIDDEN ARM of every row (OD-14); filed per regbook in `strip.parquet` under the column `arm` (CANON-07 point 9).
   Ridden, printed beside, never scored, never pooled: a count and a pointer are the only aggregates.
4. **Era:** `era = E.era_of(entry_close_ms)` — `tuning` iff `entry_close_ms ≤ ERA_CUT`, else `holdout`. A bar's era is by
   its `close_ms`, an event's by its `known_close_ms`, an unfilled order's by its `known_at_ms` (`era_trigger`).
   P-SCALP-3's scored rows: `ERA_CUT < entry_close_ms ≤ W`. The gates and P-SFP-VA-1: every era, `entry_close_ms ≤ W`.
5. **Stamps:** a scored-window table is stamped with the score edge; a strip table, a Stage V table and every table that
   reads past `W` with the pin (L-0.13).
6. **Prefix identity of the two rides:** every row of the ride to PIN resolved at or before `W` equals its scored-window
   row on every column; an OPEN-at-W row is compared on entry, stop, R, T1 and T2 levels, and on its T1 fill iff the fill
   happened at or before `hi_W` — else the scored row's T1 must be unfilled.

**PER-SECTION EDITS.**
- **L-S** — L-S.25: "WALK-PIN is run once per fill rule and once per ridden Tier-E arm; `strip.parquet` holds every arm's
  rows with `W < entry_close_ms ≤ PIN` under the column `arm`; the `strip` leaf prints `n` per arm and one pointer, no
  statistic." L-S.33: the compute list says so (WALK-PIN repeats step 5 for every walk).
- **L-R** — L-R.21: the strip sentence for `scored`, `tierE__unfiltered`, `tierE__cell_1d`, `tierE__guard_1d`,
  `tierE__maker_conditioned`, `tierE__x_geometry`, `tierE__x_gaplaw` (`tierE__maker_assumed` shares its parent's rows);
  FAILS-IF (d): "… OPEN-at-W rows compared on entry, stop, R, T1 and T2 levels; and on `t1_i`, `t1_px` iff the full
  ride's `t1_i ≤ hi_W`, else the scored row's T1 must be unfilled"; plant: "a scored OPEN row carrying a T1 fill at a bar
  after `hi_W` → RED". L-R.4: P-DIR-1's `strip` per point 3.
- **L-G** — L-G.1, L-G.18, L-G.19: `strip.parquet` per point 3 for `base`, `scored` and every Tier-E arm.
- **L-X** — L-X.24 "the scored window (O-9)": points 2-3; L-X.14 `strip` leaf: `n` per arm.
- **L-C**, **L-L**, **L-V** — where the window, the strip or the era is defined (L-C.2, L-C.10; L-L.17, L-L.19; L-V.14,
  L-V.24), use the comparators of points 2-4; no other change.

---------------------------------------------------------------------------------------------------------------
## CANON-20 · THE TRAVERSE — the regime reading of record, the strict reading printed
**Settles:** FID-13, BLD-16. **Authority:** OD-15, O-18.

**CANON TEXT.** "T of record uses the regime reading (L-V.18); the contract's phrase read strictly — the same statistic
over the tuning legs with `n_probe_bars == 0` (every bar of the leg INSIDE after its close) — is a printed twin per lens
and enters no book." Filed in `TRAVERSE.json` under `twins.strict_inside.<ℓ>`: `T_strict_inside`, `n_legs_strict`,
`lower_hinge`, `median`, `upper_hinge`; printed in `STAGE_V.md` beside `T_of_record`; F-TRAV `[b]` re-derives both from
`traverse_legs.parquet`. Consumers read T through `tierc12_va_stamps.traverse(name)` (CANON-12) and file
`time_stop_source = {path, key, sha256, value}`.

**PER-SECTION EDITS.** **L-V** — L-V.18: add the sentence to the reading and the keys to "Printed beside"; RIVALS (f): "…
printed as the twin `strict_inside`"; F-TRAV [b]. **L-R** — L-R.16 and **L-S** — L-S.20: cite the reader's `traverse`
and, in the row label, "T tuning-fit (regime reading; the strict-INSIDE twin is printed in Stage V)".

---------------------------------------------------------------------------------------------------------------
## CANON-21 · THE SCORER'S LEAVES FOR OWNER-SHIPPED TIER-E ARMS; m_looks
**Settles:** STA-07, CMP-16, BLD-38 (3), TRD-08 (the leaf). **Also cited by the dispositions of:** STA-15. **Authority:** L-0.16, L-0.28, O-13. **Taken:** STA-07's slug
(`arm__<slug>`) and content (no p) over CMP-16's `arm:<name>` with `p_num` / `p_den` — the reading that prints less that
could be mistaken for a test; STA-07's look count (every interval, every LOAO panel) over CMP-16's "counts once".

**CANON TEXT.**
1. For every `tierE__<slug>` arm a STATUS lists, the scorer writes ONE beside leaf `arm__<slug>`: the sidecar's `ruler` at
   the seed of record with `N_BOOT` draws (two_sample: the arm against that registration's `base`; vs_zero: the arm
   alone), clusters = the sidecar's `panel`; filed `n`, `n_base` (two-sample), `n_clusters`, `point`, `lo`, `hi`,
   `n_draws_finite`, `would_read_ci_only`, `seed`, `draws_sha256`. No p, no bar, no sensitivity seed, no slice, no LOAO,
   no verdict word. A `strip` arm gets the `strip` leaf only.
2. The common slugs of L-X.14 are: `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut` (the row's
   ruler on `taker_twin_haircut_net_r`; on an all-taker arm it reads `IDENTICAL TO haircut`), `tuning_slice`,
   `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`, `month_block`, `drop_open`,
   `strip`; P-SCALP-3 adds `licence_at_maker_pin` (CANON-17). P-SCALP-3's `full_corridor` IS `arm__full_corridor`; its
   `tuning_slice` is computed on the tuning rows of `tierE__full_corridor` (the one slice taken on an arm) and its
   `holdout_slice` reads `IDENTICAL TO THE RECORD (era of record)`.
3. **The declared beside set of a row** = the common slugs ∪ {`arm__<slug>` for exactly the Tier-E arms in its STATUS}; an
   arm without a leaf, or a leaf without an arm, is F-GRID RED.
4. `literal_bar` prints `literal_bar_p`, `literal_bar_pctile` (the (100 · bar)-th percentile of the record's draws) and
   `would_read_ci_only`; no boolean. The forbidden-key pattern for collared leaves and tables is
   `verdict|clears|spent_test` (L-X.14 and L-0.16).
5. `m_looks_this_table` = the number of intervals (`lo`, `hi` pairs) in `SCORES.json beside[]`, every LOAO panel counted;
   §1 prints the tier total over all collared tables beside the five tests.
6. No leaf exists for a re-ride (CANON-22) and none for a table attached to no registered row (L-R.30's take-profit
   venue is descriptive).

**PER-SECTION EDITS.**
- **L-X** — L-X.14: add the rows `arm__<slug>`, `taker_twin_haircut`, `licence_at_maker_pin`; points 2-5; L-X.26: "the
  declared beside set" per point 3; `scores/BESIDE.md` (every beside leaf, whole) joins the output list (CANON-32).
  L-X.24: list `taker_twin_haircut_net_r` with its identity (CANON-07). L-0.16's pattern is L-0's edit.
- **L-0** — L-0.16: the forbidden-name pattern `verdict|clears|spent_test`; `m_looks_this_table` "= the count of
  intervals".
- **L-G** — L-G.8: "The TC12 recomputation of each shadow at TC12's seed is the scorer's leaf `arm__shadow_…` (L-X.14):
  `would_read_ci_only`, no p, no word"; L-G.13: the four twins likewise; `arm__brd17` carries the note of CANON-41 (d).
- **L-R** — L-R.24: each Tier-E arm's interval is the scorer's `arm__<slug>` leaf; INTERFACE (L-X): "the scorer derives the
  common leaves and writes one `arm__<slug>` leaf per `tierE__` arm".
- **L-S** — L-S.22: add "No cost twin prices a maker fill's adverse selection — a maker leg carries zero slippage in both.
  The only proxy in this row is the fill ladder (TICK against DEEP), and the verdict text says so beside the twins.";
  "The scorer rules `taker_twin`, `haircut` and `taker_twin_haircut`". L-S.26: `tierE__panel17`, `tierE__rr_unfiltered`,
  `tierE__live_edge`, `tierE__full_corridor` are ruled by their `arm__<slug>` leaves.

---------------------------------------------------------------------------------------------------------------
## CANON-22 · THE RE-RIDE IS A DISCLOSURE OF COUNTS AND DIFF ROWS — never an arm
**Settles:** CMP-31, FID-19 (the re-ride half). **Authority:** O-21 ("a re-ride twin is Tier-E disclosure"); no disposition
rules it, so the tie-break applies: filed precedent (TC11's and X's counts, `n_reride_differs`) and the reading with fewer
looks — L-G.18's form for all three gates. (Listed for the orchestrator.)

**CANON TEXT.**
1. No gate ships a re-ride arm: `tierE__reride` is struck from P-DIR-1. For each registered gate (and each shadow and
   twin) the stage runs the refusal inside `tierc12_books.replay_h(sym, lo_ms, hi_ms, *, refuse=None)` (CANON-38) and
   files COUNTS on its gate row — `rival_count_rejection_log`, `reride_n`, `reride_admitted_not_in_v6`,
   `reride_v6_not_taken`, `n_reride_differs` — and the differing campaigns row by row in a diff table with a placeholder
   row when none: `stage_g/g_reride_diff.parquet` and `stage_r/dir/dir_reride_diff.parquet`, key `[gate, window, symbol,
   entry_ms]`. With no hook the mirror must reproduce the v6 book (`TP._book_sha` equal). No re-ride row gets an interval,
   a scorer leaf or a V5 stamp.
2. P-DIR-1's counts live in `stage_r/dir/build_manifest.json` under `reride {…}` and in `STAGE_R_dir.md`; the as-of rival
   and the position rival of L-R.5 stay counts and key lists.
3. Every stage manifest carries, per mirrored ride, `ride_spec` (the control card and roles, by object) and `roles_name`,
   for L-0.30's TRAIL-OFFSET, ADDS and ENTRY-CROSS legs: L-G.18 (`replay_h`), L-R.5 (the same function) and L-R.30 (the
   take-profit ride).

**PER-SECTION EDITS.**
- **L-R** — L-R.5: retitle "THE RE-RIDE DISCLOSURE AND THE COUNTED RIVALS"; replace the `tierE__reride` bullet by point 1-2
  (the hook is `refuse(ctx)`, fed the filed `va_bars_4h` row whose `close_ms` equals the candidate bar's close); strike
  "the scorer's CI-only reading of the arm"; FAILS-IF (f) stays (the refuse-nothing identity). L-R.31 outputs and the
  P-DIR-1 spec (`arms`: "two arms and no re-ride"; `disclosed_beside`: "the re-ride disclosure counts and
  `stage_r/dir/dir_reride_diff.parquet` (L-R.5)") lose the arm. L-R.30: point 3. INTERFACE (L-G): "the hook is
  `tierc12_books.replay_h(…, refuse=<ctx predicate>)`".
- **L-G** — L-G.18: point 3; `g_reride_diff` key per point 1. L-G.19: declare `[symbol, entry_ms]` for `g_strip_gates` and
  the key above for `g_reride_diff`.
- **L-V** — L-V.19: no stamp table for a re-ride.

---------------------------------------------------------------------------------------------------------------
## CANON-23 · THE FIXTURE LAW — legs, block ids, leg states, the roll, the RNG, the one hand-sample law
**Settles:** BLD-22, CMP-12, STA-16, CMP-13, BLD-28 (the states), CMP-11, BLD-34, CMP-26, BLD-35, BLD-39 (2), CMP-08 (the
header). **Authority:** OD-17, contract :6-7, :114. **Taken:** CMP-26's grammar (exact FID + qualifier) over BLD-34's
per-name prefix table and its ids `F-FAM-PARSE`, `F-TOLL-DATA/-READER/-BOOK` (not built); BLD-22's "never RED or VOID on a
population's size" over CMP-12's VOID carve-out for F-STATE; the print tokens below over the three the findings give.

**CANON TEXT (L-0.14, L-0.19; every section conforms).**
A. **A leg is one `prove` call and one transcript block;** `legs_total` counts blocks. A fixture with lettered legs files
   one block per leg.
B. **Block id** = `<FID>` or `<FID> [<qualifier>]`; `FID` matches `F-[A-Z0-9]+(-[A-Z0-9]+)*`; `<qualifier>` = `<leg>`, or
   `<instance>`, or `<leg> · <instance>`, with `<leg>` = `<letter> <NAME>` or `<NAME>` and `<instance>` a registration
   id, arm, book, directory or grid id; no bracket inside a qualifier. Examples: `F-SCALP [a HAND-3]`, `F-GATE [SET ·
   P-ADM-1]`, `F-KEY [stage_g]`, `F-TRAV [e · P-SFP-VA-1__scored]`, `F-TOLL [data a]`, `F-LEDGER [PREFIX]`,
   `F-NEST-ASOF [v6]`.
C. **Leg states.** PASS and FAIL come from `prove` (a VOID fixture counts FAIL). **NOT RUN** is a third state, written by
   the wrapper `not_run(fid, title, reason)` outside `prove` (it prints the block header and `  [NOT RUN] <fid>:
   <reason>`); it is never PASS. The tally line is `  N GREEN, M RED, K NOT RUN`; the fixture record carries
   `legs_not_run`; a transcript is GREEN iff zero RED and `GREEN + NOT RUN == legs_total` with NOT RUN equal to the
   record's. A NOT RUN block of a contract-named FID is RED at TC12-FIX.
   **CLOSED-NO-BOOK** is a PASS, not a fourth state: a fixture whose population is the book of a registration that reads
   CLOSED_BY_PRECONDITION runs its SYNTHETIC legs unchanged and, for each REAL-BOOK leg, its real leg prints
   `CLOSED-NO-BOOK <registration id>` and asserts from files that `regbooks/<id>/STATUS.json` says
   `CLOSED_BY_PRECONDITION` and lists no arm (BREAK plant: a STATUS copy reading `BUILT`, or listing an arm → detector
   `CLOSED-STATUS`). F-ROLL prints such a fixture `PASS (row closed by precondition: real legs CLOSED-NO-BOOK)`. A data leg
   of F-NOT whose only tables belong to a closed registration is CLOSED-NO-BOOK by the same rule, never `NO TABLE IN
   SCOPE`.
D. **No fixture leg makes a network call, and no drive-dependent leg is part of a transcript of record.** A transcript
   typed PROVENANCE (`data/FIXTURES_MIRROR.txt`, the only one) is recorded by sha with `provenance: true`, is excluded
   from the sweep's byte-identity roll and is listed there by name.
E. **F-ROLL's name → block map** (typed in the sweep suite): the contract name `F-<X>` matches the blocks whose FID is
   EXACTLY `F-<X>` for F-D-2, F-D-3, F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-GATE, F-BRD, F-DIR, F-SFP, F-SCALP,
   F-TOLL, F-NEST-ASOF, F-LEDGER, F-FAM, F-DET, F-GRID, F-KEY; `F-CTRL` matches every FID with the prefix `F-CTRL`;
   `import-closure` matches the FIDs {`F-CLOSURE`, `F-HOOK-ESCAPE`, `F-WALL`, `F-CLOSURE-ENV`}; `worktree attestation`
   matches `F-ATTEST`. (So `F-SFP-ASOF`, `F-SFP-MIRROR`, `F-STATE-X`, `F-NEST-KEYS`, `F-LEDGER-FMT`, `F-FAM-PINS`,
   `F-ATTEST-ORDER` are the readings' additions and are rolled after the contract's.) A contract name is PASS at TC12-FIX
   iff EVERY block of its FID(s) in every transcript of record is PASS and every REQUIRED qualifier is present: F-GATE —
   `P-ADM-1`, `P-BRD-1`; F-TOLL — `data`, `reader`, `book`; F-TRAV — one `[e · <book>]` block per range book (held by
   F-TYPED-TOTAL); F-NEST-ASOF — one block per stamp table.
F. **Fixture randomness.** Every fixture stream is `numpy.random.default_rng([SEED, crc32("<suite tag>|<block id>")])`,
   `<suite tag>` = the suite's stem without `tierc12_` and `_fixtures` (`va`, `stage_r`, `scalp`, `tide`, …). Each seeded
   leg states its count `n` in the OWNING reading as a fixture-typed literal (where X filed a count for the mirrored leg,
   that count, with its source) and prints it in the transcript header. F-SEED: a seed expression resolves iff every leaf
   is the pin-door seed (or `E.SEED`), an integer draw index, or a `crc32` call; a seed read by key from a sha-pinned X
   record is allowed only inside the functions typed `X_SEED_MIRROR_T` (the F-VA-NULL stream builder; `tierc12_era.compute`
   with `seed_source = "x"`).
G. **THE HAND-SAMPLE LAW (one law, every section).** The sample is chosen by a rule frozen in the owning reading before
   any book exists: categories first — the first row of each named category in the reading's stated key order.
   (1) A category with no member prints `NONE-EXISTS <category>`, asserts from the population that its count is zero, and
   its slot is taken by the next unchosen row in key order, printed `FILL`.
   (2) If the population holds `n < k` rows (`k` = the contract's count), ALL `n` are verified, the leg prints `ONLY <n>
   EXIST (contract count <k>)` and asserts the population's count equals `n`; `n = 0` prints `EMPTY POPULATION` with the
   same assertion.
   (3) The leg is GREEN in every such case; a shortfall, or an empty CONTRACT-NAMED category (F-SFP's POC fill or time-stop
   exit), is printed `FINDING: …` and carried to the report as a finding-not-fixed owned by the operator.
   (4) No hand-sample leg is RED or VOID on the size or composition of a population; only a mismatch between the
   fixture's derivation and production is RED.
H. **Every `tierc12_*_fixtures.py` accepts `--root=DIR`** (all writes, transcripts and twins under DIR); the sweep appends
   it to each recorded invocation when it runs inside the reproducibility lens.
I. **Header.** First line `as_of_last_closed_4h: <pin ISO>`; at a record before TC12-D: `as_of_last_closed_4h:
   (pre-substrate stage)` and `substrate: none` (CANON-09 point 11).

**PER-SECTION EDITS.**
- **L-0** — L-0.14: "Every fixture is one `prove` call" → A and B; add C, D, F, G, H, I; "Hand-verified samples" bullet = G
  (the uncategorised-sample sentence becomes F). L-0.9: `legs_not_run`. L-0.11: GREEN per C; the provenance clause of D;
  `--root` per H. L-0.19: E in place of "a typed pattern table (TC11's form …)"; owner line "F-TOLL (L-D data and reader
  halves, L-S book half)"; add the CLOSED-NO-BOOK sentence of C. L-0.30: the CLOSED-NO-BOOK sentence for data legs. L-0.2
  F-SEED: F's resolution rule. L-0.18: "Its parse leg is fixed here" → block `F-FAM-PINS` in the pins suite (the contract's
  F-FAM blocks are L-X's).
- **L-D** — "Common law": "a leg that cannot run prints NOT RUN (L-0.14 C)"; L-D.13 leg 4 becomes OFFLINE (CANON-24 note
  1); L-D.21: blocks `F-TOLL [data a]` … `[data g]`, "also named F-D-FEE" struck; L-D.31: block `F-TOLL [reader]`; F-MIRROR
  leaves `data/FIXTURES_DATA.txt`.
- **L-V** — fixture common law: the RNG per F; F-STATE (a): "a class with no member at all makes the leg VOID and RED" →
  "a class with no member prints NONE-EXISTS and its slot is FILLED (L-0.14 G); the synthetic table of (b) covers every
  class"; unverified list line likewise; counts stated for F-VA-ASOF [a], F-NEST-ASOF [a], F-VA-RAW (b).
- **L-G** — L-G.9: blocks `F-GATE [<LEG> · P-ADM-1]`, `F-GATE [<LEG> · P-BRD-1]`; L-G.14: the FILL clause is L-0.14 G's
  ("this section's addition" struck in INTERFACE); L-G.10 ASOF: count stated.
- **L-R** — L-R.7 (b): add "If the refused set holds fewer than three campaigns, EVERY refused campaign is hand-verified
  and the leg prints `ONLY <n> EXIST (contract count 3)` with `n` asserted equal to the gate row's `n_refused` (L-0.14
  G)"; D3's fallback is the FILL rule. L-R.25 (a): the FILL rule and the FINDING line per G; name the legs: synthetic =
  (g), (h), F-SFP-MIRROR; real-book = (a), (b), (c), (d), (f), (i), F-SFP-ASOF, F-TRAV [e …]; F-SFP-ASOF: count stated.
  §E unverified line: per G.
- **L-S** — L-S.31 (a), (b): "fewer than three trades in the book is RED" → G (2); the unverified line "makes the leg RED
  and returns to the orchestrator" → "prints `ONLY <n> EXIST` and is carried as a finding (L-0.14 G)"; blocks `F-SCALP
  [<letter> <NAME>]`; name the legs: synthetic = (d), (i), (p), the constructed-order plants of (c), and (n) on the tapes
  of (i) when the row is closed; real-book = (a), (b), (c), (e), (f), (g), (h), (j), (k), (l), (m), (o); L-S.32: blocks
  `F-TOLL [book t1]` … `[book t5]`, (t1) synthetic (static), (t2)-(t5) real-book.
- **L-L** — L-L.7: five blocks `F-LEDGER [PREFIX]`, `[CHAIN]`, `[STRUCTURE]`, `[REHASH]`, `[ANCESTORS]` ("one fixture block
  whose id is exactly `F-LEDGER`" → "five blocks whose FID is exactly `F-LEDGER`"); L-L.20 seed per F; `F-GRID (era)` →
  `F-GRID [ERA_tables]`. INTERFACE (L-0): the exact-FID map settles the `F-LEDGER-FMT` note.
- **L-X** — the fixture table: FIDs unchanged; legs become `[<LEG>]` qualifiers; F-FAM blocks `[PARSE]`, `[REAL]`,
  `[PLANTED]`.
- **L-C** — L-C.12: "maps to every block whose id starts `F-CTRL`" stands (the one prefix FID).

---------------------------------------------------------------------------------------------------------------
## CANON-24 · THE FIXTURE HOSTING MAP (suite · record · transcript · what it hosts)
**Settles:** BLD-12, CMP-10, CMP-15, BLD-11 (a)-(b), CMP-09 (b), CMP-13 (the transcripts), BLD-28, BLD-39 (3), CAU-05 (iii)-(iv).
**Also cited by the dispositions of:** FID-09, BLD-32, BLD-34, CMP-08, CMP-26. **Authority:** OD-7, OD-17. **Taken:** BLD-28's sealed capture for F-D-2 leg 4 over CMP-13's `--online` transcript (no
fixture leg touches the network); CMP-10's helper legs in the consuming suites over BLD-12's "closure suite at --stage ≥
TC12-S"; `env/FIXTURES_SCORE_BUILD.txt` instead of CMP-15's `scores/FIXTURES_SCORE_BUILD.txt` (a file under `scores/`
before the regbooks would turn L-0.10 T5 RED).

**CANON TEXT.** One row per invocation; `T12/` is implied in transcript paths.

| invocation | record | transcript | hosts |
|---|---|---|---|
| `tierc12_resume_fixtures.py --stage=<id> --at=<sha>` | every record from TC12-REG | `resume/FIXTURES_RESUME_<id>.txt` | F-CONTRACT, F-RESUME, F-FROZEN-TEXT, F-FROZEN, F-ONE-CORRIDOR, F-OFFBUS, F-COMMIT, F-PROGRESS, F-ORDER |
| `tierc12_pins_fixtures.py` | TC12-REG | `pins/FIXTURES_PINS.txt` | F-PINS, F-VETO, F-FAM-PINS |
| `tierc12_registrations_fixtures.py` | TC12-REG | `registrations/FIXTURES_REG.txt` | F-CONTRACT-PIN, F-REG, F-ATTEST-ORDER [REG] |
| `tierc12_closure_fixtures.py --stage=<S>` | ORDER stages from TC12-REG | `closure/FIXTURES_CLOSURE_<S>.txt` | at TC12-REG: F-TYPED, F-SEED, F-FX-MIRROR, F-FX-FORM, F-CLOSURE [ii], [iii]; from TC12-ENV: also F-CLOSURE [i], [i-b], F-HOOK-ESCAPE, F-WALL |
| `tierc12_forward_fixtures.py --stage=TC12-REG.ledger-spec` | TC12-REG.ledger-spec | `forward/FIXTURES_LEDGER_SPEC.txt` | F-LEDGER (five blocks, on the five-line file; the suite imports the env-free chain module only) |
| `tierc12_data_fixtures.py` | TC12-D | `data/FIXTURES_DATA.txt` | F-D-2, F-D-3, the F-D-* legs, F-TOLL [data a..g], F-TICK |
| `tierc12_data_fixtures.py --stage=TC12-D.mirror` | TC12-D.mirror | `data/FIXTURES_MIRROR.txt` (PROVENANCE) | F-MIRROR |
| `tierc12_env_fixtures.py --stage=TC12-ENV.vendor` | TC12-ENV.vendor | `env/FIXTURES_ENV_VENDOR.txt` | F-VENDOR [referee] (no shim import) |
| `tierc12_env_fixtures.py` | TC12-ENV | `env/FIXTURES_ENV.txt` | F-VENDOR, F-SUBSTRATE, F-REROOT, F-ENV-ASOF, F-LINEAGE, F-TOLL [reader], F-CLOSURE-ENV, F-ENV-DET |
| `tierc12_tables_fixtures.py` | TC12-ENV | `env/FIXTURES_TABLES.txt` | F-WARRANTY, F-ASOF, the helper mirrors of F-COLLAR, F-GRID, F-KEY, F-DET |
| `tierc12_attest_fixtures.py` | TC12-ENV | `closure/FIXTURES_ATTEST.txt` | F-ATTEST |
| `tierc12_not_fixtures.py --stage=<S>` | ORDER stages from TC12-ENV | `closure/FIXTURES_NOT_<S>.txt` | F-NOT (ENTRY-CROSS, TRAIL-OFFSET, ADDS, PIVOT-RANGE, 5M, NEW-ASSETS, SAIL, PROMOTION, RE-FAMILY, 1W, ACTS, POST-HOC, LICENCE) |
| `tierc12_sweep_fixtures.py --stage=<S>` | ORDER stages from TC12-ENV | `sweep/FIXTURES_SWEEP_<S>.txt` | F-SWEEP; at TC12-FIX also F-ROLL, F-TYPED-TOTAL |
| `tierc12_score_fixtures.py --stage=TC12-ENV.score-build` | TC12-ENV.score-build | `env/FIXTURES_SCORE_BUILD.txt` | F-VERDICT, F-BOOT [synthetic], F-BOOT [EMPTY-ARM], F-SCORE-ANCHOR (TC11's filed arms), F-REGBOOK [plants], F-FAM [PLANTED] |
| `tierc12_va_fixtures.py --stage=TC12-V` | TC12-V | `va/FIXTURES_STAGE_V.txt` | F-VA-RAW, F-VA-ASOF, F-STATE, F-STATE-X, F-VA-MIRROR, F-TRAV [b], [c], [d], F-TRAV [a · <own module>], F-VA-PINS [a]-[d], [f], F-NEST-ASOF [a], [b], [c] (seeded instants), F-KEY / F-DET / F-COLLAR [va], F-GRID [va_stack] |
| `tierc12_va_fixtures.py --stage=TC12-V.trades` | TC12-V.trades | `va/trades/FIXTURES_VA_TRADES.txt` | F-VA-NULL, F-RETEST-MIRROR, F-TWO, F-TWO-MIRROR, F-NULL-MIRROR [a], [c], [d], F-GRID [TWO_TRADES_*], F-KEY / F-DET / F-COLLAR [va/trades] |
| `tierc12_tide_fixtures.py` | TC12-C.tide | `tide/FIXTURES_TIDE.txt` | F-TIDE-SERIES, F-KEY / F-DET / F-COLLAR [tide] |
| `tierc12_books_fixtures.py` | TC12-C | `books/FIXTURES_BOOKS.txt` | the F-CTRL family, F-KEY / F-DET / F-COLLAR [books] |
| `tierc12_va_stamps_fixtures.py --stage=TC12-V.stamps.<c|r|s>` | that child | `va/stamps/FIXTURES_STAMPS_TC12-V.stamps.<c|r|s>.txt` | F-NEST-KEYS (`.c` only), F-NEST-ASOF [<book>], scoped F-KEY / F-DET / F-COLLAR [va/stamps] |
| `tierc12_stage_g_fixtures.py` | TC12-G | `stage_g/FIXTURES_STAGE_G.txt` | F-GATE [… · P-ADM-1], F-GATE [… · P-BRD-1], F-BRD, F-EDGE-G, F-XGRID-ANCHOR, F-ARB, F-GRID [G-BRD], [G-BRD17], [G-X16P], [G-X16B], F-TYPED-FLOW, F-KEY / F-DET / F-COLLAR [stage_g], [regbooks/P-ADM-1], [regbooks/P-BRD-1], F-REGBOOK and F-BASE-IDENT [P-ADM-1], [P-BRD-1], F-VA-PINS [e · P-ADM-1], [e · P-BRD-1] |
| `tierc12_stage_r_fixtures.py --stage=TC12-R.dir` | TC12-R.dir | `stage_r/dir/FIXTURES_STAGE_R_dir.txt` | F-DIR, F-CHOP, F-GRID [VA_CHOP], [VA_CHOP_ALIGNMENT], F-REGBOOK and F-BASE-IDENT [P-DIR-1], F-VA-PINS [e · P-DIR-1], F-KEY / F-DET / F-COLLAR [stage_r/dir], [regbooks/P-DIR-1] |
| `… --stage=TC12-R.sfp` | TC12-R.sfp | `stage_r/sfp/FIXTURES_STAGE_R_sfp.txt` | F-SFP, F-SFP-ASOF, F-SFP-MIRROR, F-TRAV [a · tierc12_stage_r_sfp], [a · tierc12_rangewalk], F-TRAV [e · <each ridden arm>], F-REGBOOK [P-SFP-VA-1], F-VA-PINS [e · P-SFP-VA-1], F-TYPED-FLOW, F-KEY / F-DET / F-COLLAR [stage_r/sfp], [regbooks/P-SFP-VA-1] |
| `… --stage=TC12-R.tables` | TC12-R.tables | `stage_r/tables/FIXTURES_STAGE_R_tables.txt` | F-TP-MIRROR, F-KEY / F-DET / F-COLLAR [stage_r/tables] |
| `tierc12_scalp_fixtures.py` | TC12-S | `stage_s/FIXTURES_STAGE_S.txt` | F-SCALP [a]-[p], F-TOLL [book t1..t5], F-TRAV [a · tierc12_scalp], F-TRAV [e · <each arm>], F-REGBOOK [P-SCALP-3], F-VA-PINS [e · P-SCALP-3], F-GRID [S_*], F-KEY / F-DET / F-COLLAR [stage_s], [regbooks/P-SCALP-3] |
| `tierc12_forward_fixtures.py --stage=TC12-L` | TC12-L | `forward/FIXTURES_LEDGER.txt` | F-LEDGER, the F-FWD-* family, F-DET / F-KEY / F-COLLAR [forward], F-PORT |
| `tierc12_era_fixtures.py` | TC12-L | `era/FIXTURES_ERA.txt` | F-ERA-MIRROR, F-ERA, F-ERA-BOOKS, F-INT-THIRDS, F-GRID [ERA_tables], F-DET / F-KEY / F-COLLAR [era], F-PORT |
| `tierc12_ferry_fixtures.py --stage=<TC12-L|TC12-CLOSE>` | that stage | `ferry/FIXTURES_FERRY_<S>.txt` | F-ROWS, F-DET, F-PORT |
| `tierc12_score_fixtures.py --stage=TC12-SCORE` | TC12-SCORE | `scores/FIXTURES_SCORE.txt` | F-FAM [PARSE], F-FAM [REAL], F-BOOT [real], F-SCORE-INPUTS, F-EXIT, F-DET / F-COLLAR / F-GRID [scores], F-ATTEST-ORDER [ORDER] |
| `tierc12_close_fixtures.py` | TC12-CLOSE | `close/FIXTURES_CLOSE.txt` | F-S0-FIVE, F-FORM, F-NUM, F-WORDS, F-FNF, F-BOXCOST, F-LEDGER-FMT, F-CLOSE-SCRIPT, F-TC11-STAMP, F-ATTEST-ORDER [ORDER] |

**The contract's fixtures (:114-124) — owner, blocks, home, and which legs need a registered book.**

| contract name | owner reading | blocks (FID `[qualifier]`) | hosted at | synthetic legs · REAL-BOOK legs (the registration that can close them) |
|---|---|---|---|---|
| F-CTRL | L-C.6, L-C.12 | the `F-CTRL` family | TC12-C | all on the v6 control (no precondition; never CLOSED-NO-BOOK) |
| F-D-2 · F-D-3 | L-D.13 · L-D.14 | `F-D-2 [1..4]` · `F-D-3` | TC12-D | the snapshot; leg 4 offline against the sealed capture |
| F-VA-ASOF | L-V.8 | `[a]`, `[b]`, `[c]`, `[d]`, `[e]` | TC12-V | tapes and filed Stage V tables |
| F-VA-RAW | L-V.3, L-V.6 | `[a]`-`[d]` | TC12-V | — |
| F-VA-MIRROR | L-V.17 | `[a]`-`[d]` | TC12-V | X's filed record |
| F-STATE | L-V.13 | `[a]`-`[f]` | TC12-V | `[b]` synthetic tape; `[a]` a hand sample of V2 events (CANON-23 G) |
| F-TRAV | L-V.18 | `[b]`, `[c]`, `[d]`; `[a · <module>]`; `[e · <book>]` | TC12-V; TC12-R.sfp; TC12-S | `[e · …]` REAL-BOOK (P-SFP-VA-1, P-SCALP-3) |
| F-GATE | L-G.9 | `[<LEG> · P-ADM-1]`, `[<LEG> · P-BRD-1]` | TC12-G | the v6 base and its gates (no precondition) |
| F-BRD | L-G.14 | `[THREE]`, `[ALL]`, `[JOIN]`, `[ORDER]` | TC12-G | — |
| F-DIR | L-R.7 | `[a]`-`[g]` | TC12-R.dir | `[e]` synthetic; the rest on P-DIR-1 (no precondition) |
| F-SFP | L-R.25 | `[a]`-`[i]` | TC12-R.sfp | synthetic `[g]`, `[h]`; REAL-BOOK `[a]`, `[b]`, `[c]`, `[d]`, `[f]`, `[i]` (P-SFP-VA-1) |
| F-SCALP | L-S.31 | `[a HAND-3]` … `[p GATE]` | TC12-S | synthetic `[d]`, `[i]`, `[p]`, the constructed plants of `[c]`; REAL-BOOK the rest (P-SCALP-3) |
| F-TOLL | L-D.21 · L-D.31 · L-S.32 | `[data a..g]` · `[reader]` · `[book t1..t5]` | TC12-D · TC12-ENV · TC12-S | `[book t1]` static; `[book t2..t5]` REAL-BOOK (P-SCALP-3) |
| F-NEST-ASOF | L-V.20, L-V.21 | `[a]`, `[b]`, `[c]`; `[<book>]` | TC12-V; the stamps children | `[<book>]` REAL-BOOK (the book's registration, where it has one) |
| F-LEDGER | L-L.7 | `[PREFIX]`, `[CHAIN]`, `[STRUCTURE]`, `[REHASH]`, `[ANCESTORS]` | TC12-REG.ledger-spec; TC12-L | the chain |
| F-FAM | L-X.15 | `[PLANTED]`; `[PARSE]`, `[REAL]` | TC12-ENV.score-build; TC12-SCORE | `[PLANTED]` synthetic; `[REAL]` the five rows |
| F-DET · F-GRID · F-KEY | L-0.20 · L-0.15 · L-0.21 | `[<directory>]` / `[<grid>]` | every record that writes parquet | on a closed regbook directory: CLOSED-NO-BOOK |
| import-closure | L-0.22 (and L-D.31) | `F-CLOSURE`, `F-HOOK-ESCAPE`, `F-WALL`, `F-CLOSURE-ENV` | the closure suite; the env suite | — |
| worktree attestation | L-0.12 | `F-ATTEST` | TC12-ENV (the tool); the records at TC12-REVIEW | — |

Notes.
1. **F-D-2 leg 4 is OFFLINE.** The venue answers are captured ONCE, by the builder inside `--fetch`, as the sealed
   provenance record `data/FLAT_BAR_ATTEST.json` (the seeded 5m sample and every zero-volume flat bar among the rows TC12
   added; per bar the venue's row, its publication and the FETCH_LOG row ids), listed in `SEALED_FILES`. The fixture leg
   re-derives the sample by its own seeded draw, recounts the flat bars of the snapshot and requires each to equal its
   sealed venue row field for field; a bar absent from the record is RED.
2. **Helper legs** F-TRAV `[a]`, `[e]`, F-VA-PINS `[e]`, F-KEY, F-DET, F-COLLAR, F-GRID live in `tierc12_fx.py`; F-REGBOOK
   and F-BASE-IDENT real-book helpers are functions of `tierc12_score_fixtures.py`. The owning stage's suite runs one
   instance per builder, book, directory or grid as listed. F-TYPED-TOTAL at TC12-FIX fails if a range book has no GREEN
   `F-TRAV [e · …]` instance or a registered pin has no GREEN flow leg.
3. Stage V's transcript never enumerates a later stage's modules or tables (L-0.11's scope law adds "and any stage suite
   that enumerates modules or tables of later stages").
4. A suite outside `tierc12_va_fixtures.py` imports no door and not `analytics.value_area` (CANON-02 point 6).

**PER-SECTION EDITS.** Each section's "suite / transcript" sentences and fixture rolls are rewritten to its rows of the
table: **L-0** (the suites table; L-0.11 scope sentence; L-0.18), **L-D** (L-D.5 run table: the capture of note 1 inside
`--fetch` and the `--mirror` row's transcript; L-D.11: `FLAT_BAR_ATTEST.json` joins the provenance set and `SEALED_FILES`
— seven; L-D.13 leg 4 = note 1; L-D.15: F-MIRROR leaves the Stage D roll; L-D.24; L-D.31), **L-V** (the fixture roll's
first paragraph; F-TRAV and F-VA-PINS split per note 2; F-VA-NULL at `.trades`), **L-C** (L-C.11, L-C.12), **L-G** (L-G.9,
L-G.10, L-G.19), **L-R** (L-R.7, L-R.25, L-R.33: three invocations; the two-trades fixtures F-RETEST-MIRROR, F-TWO,
F-TWO-MIRROR, F-NULL-MIRROR are DEFINED in L-R.26-L-R.29 and HOSTED at `TC12-V.trades`), **L-S** (L-S.31: "The suite also
runs … L-V's F-TRAV [a], [e] on the builder" per note 2), **L-L** (L-L.7, L-L.18, L-L.23, L-L.33), **L-X** (the "FIXTURES
DEFINED BY THIS SECTION" table gains a hosting column from the rows above; L-X.15 PARSE/REAL at TC12-SCORE, PLANTED at
`TC12-ENV.score-build`; L-X.21 ATTEST-ORDER hosted by the score and close suites).

---------------------------------------------------------------------------------------------------------------
## CANON-25 · THE PIN MAP, THE PIN REGISTER AND THE VETO MAP
**Settles:** BLD-21, CMP-18, CMP-27. **Authority:** contract :8, :135-137; L-0.17, L-0.23. **Taken:** CMP-18's home for the
veto (the register, which covers every door) and per-lens / per-venue rows, with BLD-21's multi-capture schema and typed
`VETO_ROWS_T`; one name per pin where the two findings differ (`brd.cut`).

**CANON TEXT.**
1. **`pins/CONTRACT_PIN_MAP.json`** — one row per contract pin: `{pin, lines [a, b], regex (one or more capture groups),
   type (a tuple of the regex's arity; members ∈ {int, fraction, word, iso, str}), word_map, also [{lines, regex, group
   (optional: the capture group of this citation that must equal the row's value when arities differ)}]}`. No `veto`
   field here. A multi-group row's value is a tuple.
2. **`pins/PIN_REGISTER.json`** — one row per pin of EVERY door: `{pin, kind ∈ {contract, x_record, stage_d, fitted,
   lineage, ruling}, source {path, key or lines}, door, consumers [record ids], witness, veto (a token of :135-137 or
   null)}`. A `ruling` row has no value.
3. **Pin names of record** (sections use these and no other): `seed`; `fam.q`, `fam.<stage letter>`; `ctrl.sum_net_r`
   (:49); `va.accept_n`, `va.accept_margin_atr` (:35); `va.sfp_k` (:36, also :135); `va.nest_frac` (:45, also :135);
   `va.value_area_pct` (:29); `va.mirror_words` (:39-40); `va.licence_set` (:41); `va.lookback.<lens>` (x_record / the 1w
   row `source_lens: 1d`; value in `VA_PINS.json by_lens.<lens>.L_bars`); `adm.old_quantile`, `adm.lag_cut` (:54);
   `adm.preseen_cell` (:55, two groups); `adm.abs_cut` (:56); `brd.cut` (:58, two groups; also :135); `rr_min` (:73; also
   :100 and :135-136 — ONE pin for both range rows; `scalp.rr_min` is not a name); `sfp.rail_atr`, `sfp.t1_fraction`
   (:71); `sfp.t2_offset_atr` (:72); `chop.n_bands` (:68); `tp1d.approach_atr` (:80); `two_trades.horizons` (:79, two
   groups, asserted equal to X's `pins.laws.horizons`); `book.trg912_periods` (:44, two groups, asserted equal to R912's
   `trg_f`, `trg_s`); `grid.x16_shape` (:60, asserted equal to the four axes' cardinalities); `grid.brd_levels` (:59,
   asserted equal to (0, N)); `scalp.third_long_max`, `scalp.third_short_min` (:87; also :136 by `group`);
   `scalp.ema_fast`, `scalp.ema_slow` (:89); `scalp.trigger_prox_atr` (:90); `scalp.validity_bars` (:92; also :136);
   `scalp.fill_ticks` (:94; also :136); `scalp.deep_atr` (:94-95); `scalp.stop_beyond_atr` (:97); `scalp.rail_atr`
   (:98); `scalp.t1_fraction`, `scalp.t2_offset_atr` (:99); `scalp.era` (:83; also :137); `loao.line` (:106, two groups);
   `ledger.opening` (:109); `ledger.n_min` (:110); `ferry.bus_dir` (:111); `ferry.cap_mb` (:112);
   `fee.maker_bps_side.<VENUE>` (stage_d: `data/fee_schedule.json venues[<VENUE>].maker_bps_side`); `traverse.<lens>`,
   `traverse.1h.in_5m_bars` (fitted); `ruling.tc11_stamp`, `ruling.1w` (ruling).
4. **`VETO_ROWS_T`** (typed in F-VETO): `va-lookback` → every `va.lookback.<lens>`; `sfp-k` → `va.sfp_k`; `nest` →
   `va.nest_frac`; `breadth` → `brd.cut`; `rr-min` → `rr_min`; `outer-third` → `scalp.third_long_max`,
   `scalp.third_short_min`; `validity` → `scalp.validity_bars`; `fill` → `scalp.fill_ticks`; `maker-bps` → every
   `fee.maker_bps_side.<VENUE>`; `era` → `scalp.era`; `tc11-stamp` → `ruling.tc11_stamp`; `1w` → `ruling.1w`. F-VETO
   FAILS IF the set of register rows carrying a token differs from `VETO_ROWS_T[token]`, a token of :135-137 has no row,
   a token's parenthesised value (where the line gives one) does not parse equal to its stage-text citation, or an
   amendment that changes a pin names no operator quote.
5. **Effects not stated in the draft:** `era` vetoed without a substitute → the full-corridor book becomes `scored`, the
   holdout its Tier-E slice, the row re-filed by amendment; `1w` vetoed → Q4 is NOT ENACTED: no 1w cell is built either
   way, the report and the append drop the closure sentence and carry the operator's quote.
6. **Totality.** `CONTRACT_TOKENS_UNPINNED.json` classes gain `lens name`, `ruling or section id`, `tier id`.

**PER-SECTION EDITS.**
- **L-0** — L-0.17: the map row schema of point 1, the register schema of point 2; "Each token names exactly one pin" →
  "each token names the register rows of `VETO_ROWS_T`"; totality classes per point 6. L-0.23: "The token is the `veto`
  field of the register rows (L-0.17)"; the list of owners per point 4; point 5; F-VETO per point 4.
- **L-S** — L-S.2: `scalp.rr_min` → `rr_min` ("the one pin, shared with L-R"); the two thirds rows as point 3.
- **L-R** — L-R.32: names as point 3 (`rr_min` stands); add the row `two_trades.horizons`; L-R.28: "the horizons … also
  held equal to the contract's `H20/H100` (:79) by the pin door".
- **L-G** / **L-C** — name their rows as point 3: `ctrl.sum_net_r` (L-C.7), `adm.old_quantile` (L-G.3), `adm.lag_cut`
  (L-G.5), `adm.preseen_cell` (L-G.7), `adm.abs_cut` (L-G.8), `brd.cut` (L-G.12), `grid.brd_levels` (L-G.15),
  `grid.x16_shape` (L-G.16), `book.trg912_periods` (L-C.3: "also held equal to the contract's `9/12` by the pin door");
  INTERFACE (L-0) bullet on the pin map likewise.
- **L-V** — L-V.4: the lookback rows are `va.lookback.<lens>` with `veto: "va-lookback"`; INTERFACE "To L-0": add them to
  the rows this section needs.
- **L-D** — L-D.21: the pin `fee.maker_bps_side.<VENUE>` (register kind `stage_d`, veto `maker-bps`).
- **L-X** — L-X.11: the row `loao.line` (two groups); L-X.28 §9: the twelve tokens with the value in force (CANON-32).
- **L-L** — the four rows of point 3 (`ledger.*`, `ferry.*`).

---------------------------------------------------------------------------------------------------------------
## CANON-26 · THE ENV SHIM — attribute names and API every section uses
**Settles:** BLD-33, CAU-03, BLD-13, BLD-14. **Also cited by the dispositions of:** FID-18, BLD-38. **Authority:** L-D.25-28; the referee [checked: `scripts/tierc11_env.py:719-752`,
`:868-870`, `:1025-1047`].

**CANON TEXT.**
1. **Module aliases** (the referee's, no hunk renames them): `E.TB` tierc2_baseline · `E.D` tierc10_data · `E.TP`
   tierc10_panel · `E.BK` tierc10_brk · `E.LN` tierc10_lanes · `E.T9` · `E.T8` · `E.T7` · `E.R7` tierc7_rules · `E.LAB`
   tierc7_lab_regime · `E.T6` · `E.R6` · `E.T5` · `E.R5` tierc5_rules · `E.R4` · `E.R3` · `E.R2` tierc2_rules. **`E.LR` and
   `E.RC` do not exist:** write `E.LAB` and `E.R7`.
2. **Objects:** `E.PIN_MS`, `E.PIN_ISO`, `E.TC11_PIN_MS`, `E.TC11_PIN_ISO`, `E.TC10_PIN_MS`, `E.ERA_CUT_MS`, `E.SEED`,
   `E.SEED_SENS`, `E.N_BOOT`, `E.LENS_MS`, `E.CLASSIC5`, `E.UNSEEN12`, `E.PANEL17`, `E.OUT`, `E.SNAPSHOT`, `E.MAIN_TREE`,
   `E.TC11_OUT`, `E.X_REC`, `E.X_WORKTREE`, `E.TC11_ALLOW_FILE`. **`X_REC = MAIN_TREE / "research_outputs" / "tierc12" /
   "x_rec"`** (hunk 2): `x_rec/**` is git-ignored and exists only in the main tree, so a detached review worktree reads it
   there. `TC11_LIST_DIRS` is deleted.
3. **Functions:** `E.era_of(close_ms)`; `E.fees() -> {stem: {asset, venue, taker_bps_side, taker_round_trip_bps,
   maker_bps_side, maker_round_trip_bps, maker_kind, maker_slippage_bps_side, slippage_bps_side, slippage_tier,
   maker_source_url}}`; `E.ticks() -> {stem: price_tick string}`; `E.D.load_asof(stem, iv)` (bars closing ≤ the pin — there
   is no `E.load_asof`); **`E.load_asof_at(stem, iv, cut_ms)`** = the rows of the bound file with `open_time + STEP_MS[iv]
   ≤ cut_ms`, ascending; HALT unless `cut_ms` is an int `≤ PIN_MS`, and on a missing file. **Any instant is admitted** —
   there is no 4h-modulus clause: an off-grid instant such as `ERA_CUT_MS` cuts each lens at its last bar closed at or
   before it. `E.load_funding_asof_at(stem, cut_ms)` likewise (floor hour `≤ cut_ms`). `E.tc11_record(rel)` (absolute
   MAIN-tree path for a `rel` on `TC11_ALLOW_FILE`, sha asserted against TC11's PROGRESS, itself accepted at its R0 sha or
   at the stamped value of CANON-35); `E.tc10_record(rel)`; `E.x_rec(rel)` (absolute MAIN-tree path, sha asserted against
   its manifest row; the manifest's own sha through `certified()`); `E.lineage_shas()`; `E.verified_reads()`;
   `E.read_set()` (CANON-28); `E.hook_escapes`, `E.opened_paths`, `E.import_audit`, `E.classify`.
4. **F-ENV-ASOF:** strike "that is not a 4h close or"; its last condition reads "a `cut_ms` past the pin is accepted"; add
   the leg "for `cut_ms` in {`ERA_CUT_MS`, a seeded 1h close off the 4h grid, a seeded 5m close}: the frame's last close ≤
   `cut_ms` < the next bar's close, and the frame is a row-prefix of `E.D.load_asof(stem, iv)`".
5. **`TC11_ALLOW_FILE`** (hunk-6 data) is the union of the sections' rows, assembled now: `PROGRESS.json`, `LEANS.md`,
   `data/{AS_OF_PIN.json, fee_schedule.json, STAGE_D_MANIFEST.json, CONTRACT_SPECS.json}`, `books/{v6_journal,
   v6_campaigns, trg912_journal, trg912_campaigns}.parquet`, `books/build_manifest.json`, `scores/{BASE_IDENT.json,
   SCORES.json}`, `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json}`, `stage_g/{g_campaign_gates,
   g_grid_books, g_grid_partition}.parquet`, `stage_g/{build_manifest.json, STAGE_G.md}`, `stage_r/{NEST_v6,
   NEST_trg912, R5_CHOP_DIRECTION}.parquet`, `stage_r/R5_CHOP.md`, `ranges/{SCALE_GRID.parquet, SCALE_PICKS.json}`,
   `stage_r4/{R4_NULL_BOXES.parquet, build_manifest.json}`, `stage_h/tp_bars.parquet`, `forward/{FORWARD_LEDGER.jsonl,
   FORWARD_LEDGER.md}`, `regbooks/P-AGE-1/{base, scored, tierE__shadow_abs206}.{parquet, json}`,
   `regbooks/P-WIN-1/scored.{parquet, json}`, `regbooks/P-TP-RNG/scored.{parquet, json}`,
   `regbooks/P-BRK-4H/scored.{parquet, json}`.

**PER-SECTION EDITS.**
- **L-D** — L-D.26 hunk 2 (`X_REC`), hunk 7 (CANON-02), hunk 10 (the API of point 3; `TC11_LIST_DIRS` removed from
  `__all__`); L-D.27: `E.x_rec(rel)` "returns the absolute MAIN-tree path after asserting the file's sha equals its
  `X_REC_MANIFEST.json` row"; the classes `x-rec`, `x-rec-unlisted`, `x-rec-write` are judged on that root; the allow
  list of point 5; strike the `TC11_LIST_DIRS` sentence; L-D.28: the `load_asof_at` sentence of point 3; L-D.31
  F-ENV-ASOF per point 4. INTERFACE (L-L): strike "its enumeration of TC11 directories uses `TC11_LIST_DIRS`".
- **L-C** / **L-G** — abbreviations and every use: `E.LR` → `E.LAB`, `E.RC` → `E.R7`; `E.TP.PANEL17` → `E.PANEL17`.
- **L-V** — L-V.2, L-V.7: "the env's `load_asof`" → "`E.D.load_asof(stem, lens)`"; L-V.4: `ATR_LEN` is `E.R2.ATR_LEN`,
  the floor `E.R5.PROVISIONAL_MIN_N`; F-TRAV [d], F-VA-ASOF, F-NEST-ASOF call `E.load_asof_at(stem, lens, cut_ms)` at
  off-grid instants.
- **L-R** — INTERFACE (L-D): "`E.load_asof`" → "`E.D.load_asof`"; lineage objects by the aliases of point 1.
- **L-S** — L-S.2: `tierc2_rules.WINDOW_FAST` etc. are `E.R2.…`, `tierc3_rules.MIN_STOP_ATR` is `E.R3.…`.
- **L-L** — INTERFACE (L-D): the `TC11_LIST_DIRS` sentence is moot (the name is deleted).
- **L-0** — L-0.12 clause (6) and INTERFACE (L-D): the X binding is on the main tree's `XR/`; L-0.17: `RC.ATR_LEN` →
  `E.R2.ATR_LEN`, `RC.WARMUP_BARS` → `E.R2.WARMUP_BARS`.
- **L-X** — INTERFACE (L-D): this section's allow-list rows are in point 5 (the P-BRK-4H and P-AGE-1 arms, `SCORES.json`,
  `BASE_IDENT.json`, `AS_OF_PIN.json`, the two registry files).

---------------------------------------------------------------------------------------------------------------
## CANON-27 · `TickGrid` ACCEPTS A FLOAT OR A DECIMAL
**Settles:** BLD-31, TRD-11, CMP-28. **Authority:** O-20.

**CANON TEXT.** `scripts/tierc12_tick.py`, `TickGrid(tick: str)`; attributes `T` (`Decimal`), `dec(x)`; methods
`floor_ticks(x)`, `ceil_ticks(x)`, `on_grid(x)`, `px(n)`, and the four comparisons against a grid level `lt(x, n)`,
`le(x, n)`, `gt(x, n)`, `ge(x, n)`. Every `x` is a `float` (converted by `dec`: `Decimal(repr(float(x)))`) or a
`decimal.Decimal` (used exactly as given; finite and > 0; no float round-trip); any other type HALTs. All arithmetic
stays inside the trapping context (`Inexact`, `Rounded`). F-TICK `[a]` enumerates Decimal inputs carrying more significant
digits than a float64 round-trips, beside the float ones.

**PER-SECTION EDITS.** **L-D** — L-D.23: the paragraph above (method names included). **L-S** — L-S.11 (T2) and L-S.15 (DEEP's
depth) hand an exact `Decimal` to `ceil_ticks` / `floor_ticks`; INTERFACE (L-D): delete "If L-D declines, the float … (required
zero, else HALT for an amendment)"; unverified list: delete the `TickGrid` line.

---------------------------------------------------------------------------------------------------------------
## CANON-28 · THE OPEN LOG — `READ_SET.json`
**Settles:** BLD-23. **Also cited by the dispositions of:** BLD-01. **Authority:** L-D.27, L-0.30.

**CANON TEXT.** `E.read_set() -> {class: sorted paths}` (hunk 10): every READ open since the hook was armed whose class is
one of `tc12-snapshot`, `tc10-allow`, `tc11-allow`, `x-rec`, or `tc12-record` (a path under `T12/` outside any `_det_*`
segment); paths repo-relative, or snapshot-relative for the snapshot. L-0.13's manifest helper writes, beside every
`build_manifest.json`, `<dir>/READ_SET.json` = the sorted union of `E.read_set()` over the builder process and its spawn
workers (each worker returns its set with its result; merged in key order), plus `licence_reads` (CANON-12). In a
directory of `SHARED_DIRS_T` the file is `READ_SET_<record id>.json`. It is a member of the directory's determinism set
and is re-derived in the F-DET twin. It is THE object these legs read: L-0.30 5m leg (a); F-SCALP (g) READ-SET; L-D.27's
verified-read law; L-L.9's declared snapshot read set; the `VA-BLIND` leg (CANON-02); F-NOT LICENCE (CANON-42).

**PER-SECTION EDITS.** **L-D** — L-D.26 hunk 10 and L-D.27 ("each stage's fixture asserts … from that directory's
`READ_SET.json`"). **L-0** — L-0.13 "Manifests"; L-0.30 5m leg (a): "a 5m kline path appears in a directory's
`READ_SET.json` outside `FIVE_MIN_READERS_T`"; L-0.20: the file is in the determinism set. **L-S** — L-S.1 FAILS-IF /
L-S.31 (g): "`stage_s/READ_SET.json` holds a path outside the read set". **L-L** — L-L.9, L-L.20: "the directory's
`READ_SET.json` must hold no other snapshot path". **L-R** — L-R.24: TC12-R's one 5m read is visible in
`stage_r/sfp/READ_SET.json`. **L-V**, **L-C**, **L-G** — their directories carry the file; no other edit.

---------------------------------------------------------------------------------------------------------------
## CANON-29 · SUBPROCESS SITES, THE CLOSE ACTS, THE STAMP PROOF TREE
**Settles:** BLD-24, FID-15, BLD-25, BLD-26. **Authority:** OD-18, O-12, O-10. **Taken:** OD-18's "template module that holds
only its text" (FID-15) over BLD-24's `ACTS_TEMPLATE` constant inside `tierc12_close.py`; BLD-26's detached linked worktree
for the tc11-stamp proof — O-10 says "scratch clone", read here as "a scratch tree outside both trees", because a clone
cannot run TC11's suites [checked: `scripts/tierc11_env.py:218-230` resolves `MAIN_TREE` to the tree itself unless `.git`
is a `gitdir:` file, and `tc10_record` returns `MAIN_TREE / rel` for untracked TC10 records]. (Listed for the orchestrator.)

**CANON TEXT.**
1. **`SUBPROC_SITE_T`** (typed, closed, one pinned call site each; `hook_escapes` findings are filtered by exactly these):
   `tierc12_data.clone_snapshot` (`cp -cpR`); `tierc12_worktree_attest.git` (subcommands `worktree`, `rev-parse`,
   `status`, `show`); `tierc12_close.git_ro` (read-only verbs `rev-parse`, `log`, `ls-files`, `ls-tree`, `cat-file`,
   `show`, `merge-base`, each with `--no-optional-locks`); `tierc12_tc11_stamp.run` (`git worktree add --detach` /
   `git worktree remove --force` on the scratch proof tree, and the interpreter running TC11's suites with cwd asserted
   inside that tree). Fixture modules may use `subprocess` (read-only git; twins; scratch repositories). No other
   non-fixture module holds a subprocess site.
2. **The acts' text** lives in `scripts/tierc12_close_acts_template.py`: string constants holding the text of
   `close_acts.sh` and nothing else — no call, no subprocess, no import beyond `__future__`; imported only by
   `tierc12_close.py`. F-NOT leg ACTS exempts, by a typed list of one, the string constants of that module (and the
   generated `close/close_acts.sh`); everywhere else in TC12 sources, fixtures included, an argv or shell string whose git
   subcommand is `push` or `merge`, an `import publish_exchange`, or a call named `publish` is RED. Plants: a `git push`
   string in any other TC12 source → RED; a call added to the template module → UNEARNED RED.
3. **Executions of the acts** (L-0.26): "its only executions are `bash -n` and runs of a SCRATCH COPY with every path and
   cwd asserted outside both trees: step 0 (`--check`) against scratch repositories, and steps 1-7 against a sandbox clone
   with a local bare origin, cut before `publish()`. The generated file in the main tree is never executed by the
   executor." The scratch copy is produced by the same generator with two typed substitution points — the step-2 ferry
   planner call and the step-4 stamp call are replaced by stubs that write their expected outputs (a copy list naming one
   planted CSV; a planted `BUILT:` line with no re-pin) — and proves ORDER and the STOP guards only; the real planner is
   proven by F-ROWS `[ACT]` and the real stamp by F-TC11-STAMP.
4. **The tc11-stamp proof tree** (`tierc12_tc11_stamp.py --prove`): a DETACHED LINKED WORKTREE of the main repository at
   `HEAD` under a scratch directory outside both trees (`git worktree add --detach`; removed with `--force` at the end; no
   ref and no main-tree file moves), so that TC11's `_main_tree()` resolves the real main tree and the TC10 allow-list is
   read there read-only, as in TC11's certified lens runs; TC11's ignored parquet and `TC10_STAGED` are staged by the
   attest tool's globs. A `[PRE]` leg first runs TC11's sweep on the UNSTAMPED proof tree and must be GREEN; a RED PRE leg
   is reported `PROOF ENVIRONMENT DEFECT` and is not a tc11-stamp result. The tool never imports `E`.
5. **L-0.16:** the registered marker is allowed in score documents, §0, and §4's verbatim re-quote of P-SCALP-3's
   `verdict_text` (L-X.28).

**PER-SECTION EDITS.**
- **L-0** — L-0.22 leg (iv): point 1. L-0.26: READING sentence = point 3; F-NOT leg ACTS = point 2. L-0.24: "SCRATCH CLONE"
  → "scratch proof tree (a detached linked worktree, L-X.34)"; F-TC11-STAMP gains "(0) PRE: the unstamped sweep is not
  GREEN". L-0.16: point 5.
- **L-X** — L-X.28: the generator's modules are `tierc12_close.py` and `tierc12_close_acts_template.py`. L-X.33: the
  scratch-proof paragraph = point 3 (strike "L-0.26 words the acts' executions more narrowly …"). L-X.34 `--prove` =
  point 4; FAILS-IF gains the PRE leg; UNVERIFIED (ii): "in a detached linked worktree with the staged parquet". L-X.31,
  L-X.29: git facts through `tierc12_close.git_ro`. INTERFACE (L-0): delete "Three differences for the reviser to rule".
- **L-D** — INTERFACE (L-0): the one site this section declares is `tierc12_data.clone_snapshot`.
- **L-L** — L-L.32: "Its only executions of `--of-record` are inside fixtures, against scratch repositories (F-ROWS
  [ACT]); in the acts' sandbox proof the planner call is stubbed (L-X.33)".

---------------------------------------------------------------------------------------------------------------
## CANON-30 · `PRE_REG` AND `REG_SET` — the registration attestation sets
**Settles:** BLD-03, CMP-14. **Authority:** contract :8; L-0.10 T1. **Taken:** BLD-03's exact file list (CMP-14's directory
globs are its superset and are not used).

**CANON TEXT.**
- **`PRE_REG`** = the artifact paths of STEP Q, TC12-R0 and TC12-LEANS; `progress/**`; `PROGRESS.json`; `.gitignore`;
  `scout/**`; `x_rec/**`; `leans_draft/**`; `review/**`; `LEANS.md`, `LEANS_AMENDMENTS.md`, `AMENDMENTS_PROPOSED.md`,
  `ORCHESTRATOR_RULINGS.md`, `DISCLOSURES.md`.
- **`REG_SET`** (fixture-typed; exactly what the TC12-REG commit ADDS) = `REGISTRATION_PLAN.md`;
  `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json, ATTEST_REG.json, FIXTURES_REG.txt}`;
  `pins/{CONTRACT_PIN_MAP.json, CONTRACT_PINS.json, PIN_REGISTER.json, CONTRACT_TOKENS_UNPINNED.json, FIXTURES_PINS.txt}`;
  `frozen/FROZEN_ESTATE.json`; `resume/FIXTURES_RESUME_TC12-REG.txt`; `closure/FIXTURES_CLOSURE_TC12-REG.txt`;
  `progress/TC12-REG.json`; the scripts `tierc12_{fx, units, pins, frozen, registrations}.py` and
  `tierc12_{registrations, pins, resume, closure}_fixtures.py`. The commit also MODIFIES (does not add)
  `scripts/tierc12_progress.py` (CANON-05 point 2, CANON-35 point 4) and `PROGRESS.json`.
- **ATTEST-REG** (at filing): the disk walk under `T12/` holds no file outside `PRE_REG ∪ REG_SET`, no `.parquet` outside
  `x_rec/`, and `scripts/tierc12_*.py == {tierc12_progress.py} ∪ REG_SET`'s scripts. `ATTEST_REG.json` is the sorted
  listing (path, sha) taken after `--file`, of every file then on disk except itself.
- **ATTEST-ORDER** (at TC12-SCORE, at CLOSE and in `close_acts.sh` step 0): the paths first added by `REG` are exactly
  `REG_SET`; every tracked TC12 path outside `PRE_REG ∪ REG_SET` has `first_add` a PROPER descendant of `REG`.
  `TC12-REG.ledger-spec` (`forward/**`, `tierc12_forward_spec.py`, `tierc12_forward_fixtures.py`) is filed AFTER the
  attested instant and is covered by that descendant test.
- The vendored referee is not in `REG_SET` (it is `TC12-ENV.vendor`'s).

**PER-SECTION EDITS.** **L-X** — L-X.21: the four bullets above replace the PRE_REG parenthesis and the ATTEST-ORDER
sentence; L-X.20: "the REG commit adds exactly `REG_SET`" (strike "committed alone with the frozen LEANS, the plan, the
review record and `ATTEST_REG.json`"); L-X.1: the filer calls the pin door, whose files are in `REG_SET`. **L-0** — L-0.10's
TC12-REG row lists `REG_SET` verbatim; the TC12-LEANS row keeps `LEANS.md` and the review record. **L-L** — L-L.3: the
ledger-spec commit is a proper descendant of `REG`.

---------------------------------------------------------------------------------------------------------------
## CANON-31 · THE COMMIT-SUBJECT GRAMMAR
**Settles:** BLD-30, CMP-01 (e). **Authority:** O-1; the filed history [checked: `tierc12(STEP Q)`, `tierc12(R0)` ×2,
`tierc12(LEANS draft)`, `tierc12(LEANS review)`].

**CANON TEXT.** "Subject: `tierc12(<ID>[ <words>]): <sentence>`. `<ID>` is the LONGEST record id of `RESUME_ORDER_T` ∪
{`TC12-D.mirror`} — written with or without its `TC12-` prefix; `STEP Q` is the one two-token id; `CLOSE` also heads the
operator's close-act commits — that is a prefix of the text inside the parentheses and is followed by `)` or a space; any
words after it are free. The filed subjects parse as STEP Q, R0, R0, LEANS, LEANS. A subject never starts `tierc10`,
`tierc11(` or `tc11x(`." F-COMMIT tests the parsed `<ID>`; plant: a subject whose first token is not a record id → RED; a
child commit labelled with its parent's id while it touches the child's record → RED.

**PER-SECTION EDITS.** **L-0** — L-0.9 "Commit": the sentence above replaces "where `<STAGE>` is an `ORDER` entry written
with or without its `TC12-` prefix"; F-COMMIT's "a subject does not name an `ORDER` stage" → "the parsed `<ID>` is not a
record id". **L-D**, **L-L**, **L-S**, **L-X** — every subject they quote (`tierc12(TC12-ENV.vendor): …`,
`tierc12(TC12-REG.ledger-spec): …`, `tierc12(TC12-S): …`, `tierc12(CLOSE): …`) already conforms; no other edit.

---------------------------------------------------------------------------------------------------------------
## CANON-32 · THE REPORT — whole versus pointed, §0.1's columns, §9's lists, the operator items
**Settles:** CMP-17, STA-08 (the columns), FID-14 / STA-12 (b) and FID-20 (the operator items). **Also cited by the dispositions of:** BLD-38. **Authority:** OD-18, OD-19,
contract :7, :126-131.

**CANON TEXT.**
1. **The map, frozen now.** Printed WHOLE IN THE REPORT: §0.2 `VA_CHOP_ALIGNMENT`; §0.3 the mirror; §0.4 `LEDGER-BOOKS`,
   `LEDGER-ROWS`; §1 the families; §2 `VA_PINS`, `TRAVERSE` (with the strict-INSIDE twin); §3 `va_stack` (L-V.24, nothing
   else); §4 `S_FILL_SENSITIVITY`, the twins' leaves, `S_MISS_GRID`, `S_REGIME`; §5 `G-BRD`, `G-BRD17`, `G-X16P`, `G-X16B`.
   Every other grid is printed whole in its STAGE DOCUMENT OF RECORD and the report carries one pointer row per grid
   (path, sha, cell count): `VA_CHOP` → `stage_r/dir/STAGE_R_dir.md`; the `TWO_TRADES_*` family → `va/trades/TWO_TRADES.md`;
   `ERA_tables` → `era/ERA.md`; `S_FUNNEL`, `S_SLICES` → `stage_s/STAGE_S.md`; `SCORES.json beside` → `scores/BESIDE.md`.
   "A report may point to a grid printed whole in its stage document; that is not an abbreviation" (L-0.15). No operator
   choice is made at render; the generator still HALTs above the per-file cap.
2. **§0.1's columns:** `seq | registration | family · m · bar_cell | era · n (n_base) · n_clusters | point | 90% [lo, hi]
   | p_num/p_den | LOAO line | verdict_cell`, then under each row its `disclosures[]`, its `size_footnote` and its
   `superseded[]` lines (CANON-41).
3. **§9 gains three lists:** O-1..O-32, one line each ("each is carried into the build report as a reading"); O-32's
   defaults that stand; the twelve veto tokens with the value in force (from `PIN_REGISTER.json`) and "no veto received"
   or the operator's quote. §9 prints every line of `DISCLOSURES.md` and `DISCLOSURES_BUILD.md`.
4. **Operator items added (OD-19),** each in its owner's OPEN TO OPERATOR list and harvested into §9: (i) the CLOSED /
   CLOSED FOR GOOD choice in the both-clauses cell (CANON-18 point 6; L-X item 7, mirrored in L-S); (ii) "The stop's
   else-clause never binds. With the stop measured from the limit at the edge, '0.5 ATR_1h beyond the edge' (:97) is
   always inside the 1.0 ATR_1h rail (:98), so every cross-triggered order has R = 1.0·ATR_1h. DEFAULT if silent: the
   contract as written (the rail governs); the count of cross orders and `rail_binding` is printed. A cross stop at 0.5
   ATR_1h with no rail is the operator's order." (L-S).

**PER-SECTION EDITS.**
- **L-X** — L-X.28: the "Whole, frozen by KIND" bullet is followed by point 1; §3's row reads "`va_stack`, every cell
  (L-V.24)"; §5's row reads "D · C · G (its four grids whole) · R and L (pointers to their stage documents)"; §0.1 per
  point 2; §9 per point 3; F-S0-FIVE RED when a row lacks its footnote. L-X.26: add `scores/BESIDE.md`. OPEN TO OPERATOR:
  item 6 becomes "(settled: the whole-versus-pointed map is frozen in L-X.28.)"; item 7 = point 4 (i).
- **L-0** — L-0.15 "Printed whole": add the quoted sentence. L-0.10 T4 unchanged.
- **L-S** — L-S.30 "The report": `S_FILL_SENSITIVITY`, `S_MISS_GRID`, `S_REGIME` whole; `S_SLICES`, `S_FUNNEL` by pointer
  to `STAGE_S.md`, where they are printed whole. OPEN TO OPERATOR: add point 4 (i) and (ii).
- **L-R** — L-R.9: `VA_CHOP_ALIGNMENT` whole in §0.2; L-R.8, L-R.28: printed whole in `STAGE_R_dir.md` /
  `va/trades/TWO_TRADES.md`. INTERFACE (L-L): "the grids are printed whole in their stage documents".
- **L-L** — L-L.19, L-L.22: `ERA.md` is the stage document of record; the report points to it.
- **L-V** — L-V.24: "its 'VA stack whole' from `va_stack.parquet`, every cell" stands; the two-trades grids are in
  `va/trades/TWO_TRADES.md`.

---------------------------------------------------------------------------------------------------------------
## CANON-33 · THE FERRY'S TYPED LIST, COMPLETED; THE ORDER-TABLE KEYS
**Settles:** CMP-07, FID-16, BLD-20 (keys). **Authority:** OD-18 ("completed from every section's declared tables at
assembly"), contract :111; X's frozen vocabulary [checked: `x_rec/scripts/tc11x_ferry.py:194-199` — ASSET `asset`,
`symbol`; INSTANT `entry_ms`, `entry_open_ms`, `entry_close_ms`, `harden_ms`, `event_ms`, `known_at_ms`; the 26 axis
words include `arm`, `book`, `variant`, `lens`, `era`, `direction`, `side`, `kind`, `trade`, `cell`, `panel`].
**Taken:** `known_at_ms` (FID-16, CMP-07, CMP-09) over BLD-20's `event_ms`; CMP-07's S_miss key (with `book`).

**CANON TEXT.**
1. **Order tables are built to the vocabulary.** `S_orders_<book>` and `S_refusals_<book>`: key `[book, symbol,
   known_at_ms]`, `known_at_ms` = the trigger close; `S_miss`: key `[book, symbol, known_at_ms, variant]`, `variant ∈
   {T1, T2, split}`, `book == "scored"`. None of the three carries a column named `entry_ms`, `entry_open_ms`,
   `entry_close_ms`, `harden_ms` or `event_ms` (the fill is `fill_close_ms`; the three per-rule fill bars are
   `fill_i_touch`, `fill_i_tick`, `fill_i_deep`). The column `trigger_close_ms` does not exist anywhere: it is
   `known_at_ms`.
2. **Grids are keyed by `cell`.** A grid whose axes include the assets names that axis column `panel` (values: the stems
   and, where pooled, `POOLED`), never `asset` or `symbol` — so it classes POINTED "no ASSET column". (`va/va_stack` is
   the declared exception: key `[asset, lens, era]`, FERRIED per-asset.)
3. **L-L.25's table, completed** (class derived by L-L.24's rule from the declared key; paths relative to `T12/`):

   | file | declared key | class · reason |
   |---|---|---|
   | `books/{v6,trg912}{,_ext}_journal.parquet` | `[asset, entry_ms]` | FERRIED · per-trade |
   | `books/{v6,trg912}{,_ext}_campaigns.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
   | `books/strip.parquet`, `books/ctrl_prefix.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
   | `books/arming_log.parquet`, `books/arming_counts.parquet` | `[book, window, symbol, arm_ms, direction]`, `[book, window, symbol, reject]` | POINTED · rows per identity > 1 |
   | `tide/tide_bars_4h.parquet` | `[asset, open_ms]` | POINTED · rows per identity > 1 |
   | `tide/breadth_4h.parquet` | `[open_ms]` | POINTED · no ASSET column |
   | `stage_g/g_campaign_gates.parquet`, `stage_g/g_strip_gates.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
   | `stage_g/g_book_keys.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
   | `stage_g/{g_gate_rows, g_brd_grid, g_brd17, g_grid_partition, g_grid_books}.parquet` | `[gate]` / `[cell]` | POINTED · no ASSET column |
   | `stage_g/g_arbitration.parquet`, `stage_g/g_reride_diff.parquet`, `stage_r/dir/dir_reride_diff.parquet` | `[window, symbol, trigger_ms, arm_ms]`; `[gate, window, symbol, entry_ms]` | POINTED · by type ("an event listing with a placeholder row; class not row-stable") |
   | `stage_r/dir/VA_CHOP_ROWS.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
   | `stage_r/dir/dir_book_keys.parquet` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
   | `stage_r/dir/{VA_CHOP, VA_CHOP_ALIGNMENT, VA_CHOP_MARGINS}.parquet` | `[cell]` | POINTED · no ASSET column |
   | `stage_r/sfp/SFP_EVENTS.parquet` | `[lens, book, asset, entry_ms]` | FERRIED · per-trade × axes |
   | `stage_r/tables/TP1D_CAMPAIGNS.parquet` | `[symbol, entry_ms]` | FERRIED · per-trade |
   | `stage_r/tables/TP1D_SUMMARY.parquet` | `[era, asset]` | FERRIED · per-asset × era |
   | `stage_r/tables/TP1D_BARS.parquet` | `[symbol, entry_ms, bar_open_ms]` | POINTED · rows per identity > 1 |
   | `stage_s/S_orders_<book>.parquet`, `stage_s/S_refusals_<book>.parquet` | `[book, symbol, known_at_ms]` | FERRIED · per-trade × book |
   | `stage_s/S_miss.parquet` | `[book, symbol, known_at_ms, variant]` | FERRIED · per-trade × axes |
   | `stage_s/open_at_w_continued.parquet` | `[symbol, entry_close_ms]` | FERRIED · per-trade |
   | `stage_s/{S_FUNNEL, S_FILL_SENSITIVITY, S_REGIME, S_SLICES, S_MISS_GRID}.parquet` | `[cell]` | POINTED · no ASSET column |
   | `va/va_bars_<lens>`, `va/va_events`, `va/va_regimes`, `va/traverse_legs` | as CANON-11 | POINTED · rows per identity > 1 |
   | `va/va_stack.parquet` | `[asset, lens, era]` | FERRIED · per-asset × axes |
   | `va/trades/{va_null_events, va_null_go_events, NULL_BOXES_VA, TWO_TRADES_NULL_DRAWS}.parquet` | … + `draw` | POINTED · a draw table |
   | `va/trades/TWO_TRADES_EVENTS.parquet` | `[lens, asset, trade, side, anchor_i, i]` | POINTED · rows per identity > 1 |
   | `va/trades/{TWO_TRADES_VA, TWO_TRADES_VA_UNCOND, TWO_TRADES_BASE, TWO_TRADES_NULL}.parquet` | `[cell]` | POINTED · no ASSET column |
   | `va/stamps/VA_STAMPS_<book>.parquet` | `[book, symbol] + kind.key + [instant_kind, instant_ms]` | POINTED · rows per identity > 1 |
   | `regbooks/<ID>/<arm>.parquet` (CANON-07 point 4, by object) | `(symbol, entry_close_ms)`; `strip`: `(arm, symbol, entry_close_ms)` | FERRIED · per-trade (× `arm` on `strip`) |
   | `forward/ledger_rows`, `forward/ledger_side`, `forward/ledger_listed` | `[book, symbol, entry_ms]` | FERRIED · per-trade × book |
   | `forward/FORWARD_LEDGER.jsonl` | a hash chain | POINTED · by type |
   | `era/ERA_stamps.parquet` | `[symbol, entry_ms]` | FERRIED · per-campaign |
   | `era/ERA_tables.parquet` | `[book, table, block, reading, cell, side]` | POINTED · no ASSET column |
   | `scores/DRAWS.parquet` | `(registration, draw_set, draw_idx)` | POINTED · a draw table |
   | `scores/REFILE_LOG.jsonl`, `scores/SUPERSEDED.jsonl`, `review/*.jsonl` | — | POINTED · no ASSET column |
   | `data/FETCH_LOG.jsonl` | — | EXCLUDED · per-request log |

   The sentence "To be completed at assembly …" is struck: the list is complete, and a tabular file not on it is a HALTED
   ELEMENT as before. Triage adds: a directory whose name starts `_det_partial_` is EXCLUDED (it is a `_det_` segment).

**PER-SECTION EDITS.**
- **L-L** — L-L.25: the table above replaces the draft's table and its closing paragraph; L-L.24 triage: `_partial_` →
  `_det_partial_`; INTERFACE (L-R, L-S): "declared in L-L.25".
- **L-S** — L-S.30: the three keys of point 1; `variant` in place of `target`; the grids per point 2; replace "Every order
  and trade table is a per-trade or per-asset row file for L-L's ferry (contract :111)" by "Ferry classes are derived by
  L-L.24's rule from these declared columns: the arms, `S_orders_*`, `S_refusals_*`, `S_miss` and `open_at_w_continued`
  are PER-TRADE (FERRIED); the stamp tables and the grids are POINTED (L-L.25)."; `τ` is filed as `known_at_ms`
  everywhere (L-S.23, L-S.25's `era_trigger`, L-S.31). INTERFACE (L-L): likewise.
- **L-G** — L-G.19: declare `[symbol, entry_ms]` for `g_strip_gates` and `[gate, window, symbol, entry_ms]` for
  `g_reride_diff`. INTERFACE (L-L): "the ferry classes … are L-L's to assign" → "are typed in L-L.25".
- **L-C** — L-C.4: no key changes; INTERFACE: classes typed in L-L.25.
- **L-R** — L-R.31: directories per CANON-09; INTERFACE (L-L): classes typed in L-L.25.
- **L-V** — INTERFACE (L-L): answered by L-L.25.

---------------------------------------------------------------------------------------------------------------
## CANON-34 · THE AMENDMENTS LAW — sources and form
**Settles:** CMP-23, FID-17 (the AM text), FID-18 (objection residue is CANON-39). **Authority:** contract :33; L-0.5.

**CANON TEXT.**
1. **Sources** (an amendment may never follow from a registered rule's outcome): (i) a build fact — the code cannot do
   what a reading says; (ii) a verifier's finding; (iii) an operator veto by name (L-0.23); (iv) the contract's own order
   — AM-1 is the dated V2-versus-X statement of L-V.15, filed at the TC12-LEANS freeze with no AP; (v) TRANSCRIPTION
   against pinned bytes — a fee-page grammar (L-D.18), proposed by the Stage D builder as `AP-n` and ruled as `AM-n`,
   naming the body sha; it may change patterns only.
2. **Form.** Every heading is `## AM-<integer> · <YYYY-MM-DD> (~HH:MMZ) · <reading ids> · <basis>[ · <nickname>]`, with
   `<basis>` = `ruling on AP-<m>` | `contract :32-33 (no AP)` | `operator veto "<token>"`; ids ascend from 1; the body is
   **Text amended / Amended to / Reason / Redone**. A section's nickname (`AM-V2`, `AM-D-FEE-<VENUE>`) may follow in the
   title and is never an id. `--refile=<id>` accepts `AM-<n>` (a heading) or `FIX-<n>` (a key of
   `progress/TC12-FIX.json`).
3. **AM-1's text** is L-V.15's text of record with this paragraph added: "Declared against the contract's letter: (i) a
   close while a probe is pending is judged against that probe's frozen edge, not against the rolling VA(t−1); (ii) on a
   bar that resolves a probe the state is INSIDE by the frozen edge even where the close lies outside the rolling VA(t−1),
   counted per cell and filed per bar as `inside_frozen_only`."

**PER-SECTION EDITS.** **L-0** — L-0.5: points 1-2 replace "The law is TC11's, verbatim … TC12 adds one source". **L-V** —
L-V.15: "AM-V2 · <freeze date UTC>" → heading `## AM-1 · <date> (~HH:MMZ) · L-V.9..L-V.15 · contract :32-33 (no AP) ·
AM-V2`, text per point 3; INTERFACE: "AM-1 (nickname AM-V2)". **L-D** — L-D.18, L-D.19: "ONE dated amendment per venue
(`AM-D-FEE-<venue>`)" → "one amendment per venue, proposed as `AP-n` and ruled as `AM-<n>` (nickname
`AM-D-FEE-<VENUE>`), source (v)"; `maker_grammar.amendment` holds the `AM-<n>` id. **L-X** — L-X.19: `amendments` "holds
AM-1 at filing"; L-X.27: the id grammar of point 2.

---------------------------------------------------------------------------------------------------------------
## CANON-35 · NO TC12 PIN IS A WHOLE-FILE SHA OF A FILE TC12's OWN CLOSE ACTS MOVE
**Settles:** BLD-27. **Authority:** O-10; contract :13.

**CANON TEXT.** "No TC12 pin is a whole-file sha of a path in L-0.24's sets (a)-(f)."
1. A literal read by AST from one of the set-(c) scripts (`scripts/tierc11_registrations.py`, `tierc11_score.py`,
   `tierc11_score_fixtures.py`, `tierc11_stage_g.py`, `tierc11_stage_t_brk.py`) is pinned by `sha256(ast.dump(node))`,
   recorded per literal in `pins/PIN_REGISTER.json` (kind `lineage`) at TC12-REG — never by the file's sha.
2. `T11/registrations/REGISTRATIONS.json` is pinned by its chain head VALUE (`T11/registrations/REGISTRY_PIN.json["head"]`,
   asserted equal to the head recomputed from the payloads) plus the payload sha of each registration read. The literal
   `648834bf…f1ee` is struck from every reading and spec block.
3. `E.tc11_record` accepts `T11/PROGRESS.json` at its R0 sha OR at the value `T12/close/TC11_STAMP_MAP.json` names for it
   when that map reads `applied: true`; F-FROZEN accepts a census path of sets (a)-(f) at its census sha or at its mapped
   value under the same condition.
4. The merger records `contract_of_record` as `{path, prefix_bytes, prefix_sha256}` read from `progress/STEP_Q.json`
   (`scripts/tierc12_progress.py:54` changes at the TC12-REG commit; the script is re-recorded under CANON-05), so TC12's
   own BUILT stamp moves no byte of `PROGRESS.json`.

**PER-SECTION EDITS.**
- **L-0** — L-0.24: add the quoted sentence and points 1-3; L-0.9: point 4; L-0.1: "The whole-file sha is recorded beside
  the prefix sha and compared by nothing afterwards" stays true; L-0.6 F-FROZEN: point 3; L-0.16: the collar literals read
  from `tierc11_score.py` are pinned per point 1.
- **L-X** — L-X.19: `law` "read by object from `T11/registrations/REGISTRATIONS.json["law"]`, the file pinned by TC11's
  chain head and `law_source` naming path, head and key" (strike "file sha `648834bf…f1ee` asserted"); L-X.24, L-X.27:
  the AST reads from `scripts/tierc11_score.py` are pinned per point 1 ("sha asserted" → "node sha asserted").
- **L-G** — L-G.5, L-G.8, L-G.16: "(sha on record `648834bf…f1ee`, read through `E.tc11_record`)" → "(pinned by TC11's
  chain head and the payload sha of the registration read; read through `E.tc11_record`)"; P-ADM-1 and P-BRD-1 specs: the
  pinned-inputs list (CANON-36) names `T11/registrations/REGISTRATIONS.json` by chain head and the P-AGE-1 / P-WIN-1
  payload shas.
- **L-R** — L-R.30 SOURCE and L-R drafting record: the P-TP-RNG payload sha stands; the file sha is struck.
- **L-S** — L-S.2: `HAIRCUT_TOL` "read by `ast` from `scripts/tierc11_score.py:264`, node sha pinned (L-0.24)".
- **L-D** — L-D.27 / hunk 10: `tc11_record` per point 3; register row "every certified TC11 sha" per CANON-05.
- **L-L** — L-L.2: already conforms ("never TC11's whole-file registrations sha"); cite L-0.24.

---------------------------------------------------------------------------------------------------------------
## CANON-36 · THE SPEC FIELD GRAMMAR; THE GATE-TEXT SELECTOR
**Settles:** BLD-18, BLD-19, CMP-22, BLD-20 (the declared VA reads). **Also cited by the dispositions of:** STA-09, STA-11. **Authority:** L-X.18's carry law; contract :108.

**CANON TEXT (L-X.18 gains a FIELD GRAMMAR; the five blocks are rewritten to it).**
1. **Checked fields** `id`, `family`, `family_m`, `family_bar`, `prior`: the value is the text up to the first space;
   anything after it is citation, kept in the plan and dropped from the body key. `prior` is digits only (`30`, not `30%`).
2. **`preconditions`:** either the bare word `none`, optionally followed by ` — <commentary>` (never evaluated), or
   sub-bullets each of the form `{record: <path>, certified_by: <progress record> <key>, selector: <selector>, required:
   <"string" | contains "string" | true>}` optionally followed by ` — <commentary>`; HALT `PRECOND-GRAMMAR` otherwise.
   The separator is space, U+2014, space. P-ADM-1, P-BRD-1, P-DIR-1: `none — …`. P-SFP-VA-1: two items —
   `{record: research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector:
   licence["4h|taker"].by_era["ALL"].would_read, required: "PASS"}` and `{…, selector: licence_set, required: contains
   "4h|taker"}`. P-SCALP-3: the one item of CANON-17. The "If either is not met …" sub-bullets are struck (the sentence is
   in `verdict_rule`).
3. **`arms`:** sub-bullets. Exactly one begins `` `scored` `` followed by a space (regex `` ^`scored`\s ``) and holds the
   whole construction of the scored arm; the others begin with their arm's name in backticks, or with `inputs pinned:`
   (the HALT-grade input pins that P-ADM-1, P-BRD-1 and P-DIR-1 now list under `preconditions` move here; pins by
   certifying record, chain head or payload sha — CANON-35), or with `VA columns read (declared for F-VA-PINS (e)):`.
   P-SCALP-3's block carries that last sentence with L-S.1's list verbatim, ending "No 12h, 1d or 1w column."; P-ADM-1 and
   P-BRD-1 carry "VA columns read (declared for F-VA-PINS (e)): none."
4. **`labels`:** one sub-bullet per key: `<key> — tag: <TAG|none>; label: <label>; text: "<text>"; items: <items>`; the
   text is the first double-quoted string (quotes inside it are single). Tags and labels: CANON-01.
5. **The fourth book's gate text (L-L.2, L-L.3, F-FWD-SPEC, L-G.7):** "the gate text of record is the ONE element of
   `registrations[P-ADM-1].operative_spec.arms` (a list under L-X.18's carry law) that matches `` ^`scored`\s ``; HALT
   `FWD-GATE-TEXT` unless exactly one; it is filed as `gate.text_of_record` with `gate.text_sha256` beside
   `p_adm_1_payload_sha256`." `operative_spec.scored_arm` is TC11's key and is read only from TC11's P-AGE-1 and P-WIN-1
   payloads.
6. **P-ADM-1's `disclosed_beside` gains** (L-L's clause, as amended by CANON-37): "the forward ledger's fourth book
   `gated-v6-combined` — its spec `research_outputs/tierc12/forward/BOOK_SPEC_COMBINED.json` (sha filed at
   TC12-REG.ledger-spec); every row appended at TC12's pin entered before the book was frozen (flagged on the row) and
   none is a row of record for confirmation; `n` appended at TC12's pin, UNSCORED until its own n ≥ n_min; Tier-E, no
   verdict word; it is the contract's 'confirmation' (:55-56) and none of it is scored here." L-L's offered precondition
   is withdrawn: the spec is filed after the registry and cannot be its precondition.

**PER-SECTION EDITS.**
- **L-X** — L-X.18: add points 1-4 after the carry law; detector `PRECOND-GRAMMAR` joins L-X.22's list; L-X.10: "a list of
  items `{record, certified_by, selector, required}`" in the grammar of point 2; L-X.19: `operative_spec.arms` is a list.
- **L-G** — both spec blocks: checked fields with the bare value first (they already are); `preconditions: none — the row
  has no precondition and cannot read CLOSED BY PRECONDITION`; the pin paragraph moves to an `inputs pinned:` sub-bullet
  of `arms`; `labels` per point 4; P-ADM-1 `disclosed_beside` gains point 6; `arms` sub-bullets "An entry bar with
  undefined edges HALTs …" and "The scored arm must reproduce …" stay as sub-bullets (they do not match the selector).
  L-G.7: "The gate text of that spec is the `scored` element of this spec's `arms` (point 5)". INTERFACE (L-X), (L-L):
  settled as above.
- **L-R** — both spec blocks: `prior: 45` (bare; the citation after a space); P-DIR-1 `preconditions: none — …` with the
  "Inputs pinned by sha" sentence moved under `arms` as `inputs pinned:`; P-SFP-VA-1 `arms` restructured so that one
  sub-bullet begins `` `scored` — `` and holds the whole construction (entry, stop, targets, refusals, walk, booking),
  followed by the Tier-E arms' names and the `VA columns read …` sub-bullet; `preconditions`: the two brace items; `labels`
  per point 4. INTERFACE (L-X): "assumed: the filer's carry law checks the leading token" → "L-X.18's field grammar".
- **L-S** — spec block: `prior: 30`; `arms`: the `base arm: none (vs zero).` sub-bullet becomes commentary inside the
  `` `scored` `` sub-bullet's lead-in or is struck; add the `VA columns read …` sub-bullet; `preconditions`: one brace
  item; `labels` per point 4.
- **L-L** — L-L.2, L-L.3 and F-FWD-SPEC: point 5 in place of "`operative_spec.scored_arm`" for TC12's P-ADM-1; the
  "REGISTRATION SPEC · (none owned by L-L)" note: the first clause is point 6, the second is struck ("withdrawn");
  unverified list: strike "and that L-G's P-ADM-1 payload carries `operative_spec.scored_arm`". INTERFACE (L-G): likewise.

---------------------------------------------------------------------------------------------------------------
## CANON-37 · THE FORWARD SCORE'S ROW SET IS FIXED NOW; THE TWO FREEZE FLAGS
**Settles:** STA-09, CAU-13. **Also cited by the dispositions of:** CMP-22. **Authority:** OD-16, O-32 ("every pre-filing row flagged"), contract :55-56, :110.

**CANON TEXT.**
1. **Three flags, pin-independent, CHAINED on every row** (functions of `entry_close_ms` and frozen instants):
   `in_o9_scored_window` := `OPENING_MS < entry_close_ms ≤ W`; `entered_before_contract_filed` := `entry_close_ms ≤` the
   STEP Q instant (L-D.1's); `entered_before_book_frozen` := `entry_close_ms ≤` the committer time (ms) of the commit that
   first adds line 5 of `forward/FORWARD_LEDGER.jsonl`. The fourth spec's `row_fields_added` is (`p_age_1_refuses`,
   `p_win_1_refuses`, `p_adm_1_refuses`, `in_o9_scored_window`, `entered_before_contract_filed`,
   `entered_before_book_frozen`); the row's field count is X's `row_fields` plus `len(row_fields_added)` (read, not
   typed). `ledger_side.parquet` no longer carries the flags.
2. **The freeze instant** is filed ONCE in the write-once provenance record `forward/BOOK4_FREEZE.json` `{commit,
   committer_time_ms, committer_time_iso, path, line}` — written by the orchestrator immediately after the
   `tierc12(TC12-REG.ledger-spec)` commit (the STEP_Q.json pattern: no builder runs git), recorded by `TC12-D`'s record;
   the TC12-L builder reads it and HALTs if absent; F-FWD-OVERLAP holds it equal to git by a fixture-side read-only call
   (the F-D-PIN pattern). Plant: the freeze flag computed against the STEP Q instant → `FREEZE-FLAG`.
3. **The row set of record for any later score is fixed HERE,** in `BOOK_SPEC_COMBINED.json → n_law`, before a strip bar
   is on disk: rows with `in_o9_scored_window == false` and, for `gated-v6-combined`, `entered_before_book_frozen ==
   false`. The all-rows figure is printed beside under the collar. No later registration chooses.
4. The status line prints `n` (the contract's count, :110) and `n_record` (rows of the set of point 3): "… of which
   <n_record> are rows of record for a forward score".

**PER-SECTION EDITS.**
- **L-L** — L-L.10: `row_fields_added` per point 1 ("46 fields" becomes the computed count); L-L.3: `n_law` per point 3 and
  `row_fields_added`; L-L.14: point 4; L-L.16: strike the two flags from `ledger_side`; L-L.17: the standing-line bullet
  is replaced by point 3, the "BACKDATED" bullet names the two flags of point 1 and point 2's record; L-L.18
  F-FWD-OVERLAP: the flags are row fields; add the `FREEZE-FLAG` plant; `BACKDATE-FLAG` stays for
  `entered_before_contract_filed`; "What this section files": `forward/BOOK4_FREEZE.json`. OPEN TO OPERATOR 2 and 7:
  "a later scorer must exclude the flagged rows or print both scores" → "the rows of record are fixed in `n_law`
  (L-L.17); the all-rows figure is printed beside".
- **L-G** — P-ADM-1 `disclosed_beside`: CANON-36 point 6; L-G.7 "Confirmation": "…its rows of record are those the fourth
  spec's `n_law` fixes".
- **L-0** — L-0.5: `forward/BOOK4_FREEZE.json` is write-once from the record that first names it (`TC12-D`'s: the
  orchestrator's gate step adds the path to that record's artifact map; L-D writes nothing for it).

---------------------------------------------------------------------------------------------------------------
## CANON-38 · SHARED HELPERS — one implementation each
**Settles:** BLD-37. **Authority:** L-0.14 (no second implementation of one law).

**CANON TEXT.**
- `tierc12_books.campaign_rows(book, roles, lo, hi, pool, name)` is L-C.4's — the mirror of
  `scripts/tierc11_books.py:417-504` (its `CAMPAIGN_COLUMNS` carry `lag`, `r_over_atr`, the latch and exit-event stamps and
  are a superset of X's fifteen `BOOK_COLS` and eleven `TIDE_COLS`). L-L reads `lag` and the eleven tide columns from it;
  there is no port of `XB:607`.
- The v6 re-ride with a refusal hook is ONE function: `tierc12_books.replay_h(sym, lo_ms, hi_ms, *, refuse=None)`,
  `refuse(ctx) -> bool`, `ctx` carrying TC11's keys `sym`, `arm`, `ti`, `d`, `stp`, `atr`, `r_over_atr`. L-R's predicate
  and L-L's `(band, lag)` predicate are adapters to that hook; `tierc12_forward.reride_gated(lo, hi, pool, refuse)` calls
  `replay_h` and holds no replay loop of its own.
- `fee_per_fraction` is ONE function, `tierc12_rangewalk.fee_per_fraction` (filed at `TC12-R.sfp`); `tierc12_scalp.py`
  imports it. Hence `TC12-S` depends on `TC12-R.sfp` (CANON-09).
- Already single: `tierc12_asof.asof_index`; the exact comparators `cell_delta`, `exact_frame_diff`, `nan_cells`
  (`tierc12_books`); `tierc12_regbook` (CANON-07); `tierc12_progress.certified` (CANON-05).

**PER-SECTION EDITS.** **L-L** — L-L.9: "`campaign_rows` (port of `XB`:607)" → "L-C.4's `campaign_rows`"; "`reride_gated` … a
CHANGED port of `XF`:495-519" → "adapts the `(band, lag)` predicate to a `ctx` hook and calls `tierc12_books.replay_h`".
**L-C** — L-C.4 API: as above. **L-G** — L-G.18: `replay_h`'s signature as above (already). **L-R** — INTERFACE (L-G): the hook
is `refuse(ctx)`; L-R.31: `tierc12_rangewalk.py` holds `bar_step`, `geometry`, the walk and `fee_per_fraction`, and is
imported by `tierc12_scalp.py`. **L-S** — L-S.21: "mirrored as `tierc12_scalp.fee_per_fraction`" → "imported from
`scripts/tierc12_rangewalk.py`"; INTERFACE (L-R): "this section's fee mirror … is the one function both may call" → "L-R's
`fee_per_fraction` is the one function". **L-0** — L-0.10: the parallel clause of CANON-09 point 5.

---------------------------------------------------------------------------------------------------------------
## CANON-39 · RESIDUE OF RULINGS SINCE ACCEPTED (section H)
**Settles:** FID-18, FID-03 (e), CMP-03 (iii)-(iv), CMP-06 (the objection blocks). **Also cited by the dispositions of:** FID-17, CMP-01. **Authority:** O-25..O-32.

**CANON TEXT / PER-SECTION EDITS.**
- **Every section header:** "conforms to ORCHESTRATOR_RULINGS O-1..O-32" (L-D: strike the list "O-1..O-9, O-14, O-19,
  O-20"; L-X: add the sentence to OBJECTIONS: "Section H (O-25..O-32) is conformed to").
- **L-0** — OBJECTIONS: replace the block by "OBJECTION O-3 / O-4 — accepted as O-25." (delete "Drafted under the ruling as
  written"); header: "one objection was filed and accepted (O-25)". L-0.6: X's contract per CANON-05.
- **L-D** — OBJECTIONS: two lines, "OBJECTION O-8 — accepted as O-26." and "OBJECTION O-20 — accepted as O-27." (delete
  both "Drafted under the ruling as written" alternatives, including "the change is one line (`FIFTEEN` leaves
  `lenses_of`)"); L-D.4 cites O-26 for the 124-path scope; L-D.22 cites O-27 for the UNVERIFIED "never looser"; L-D.27:
  "the three earlier contracts" → "the two earlier TC contracts (TC10 RESUME, TC11)".
- **L-S** — L-S.15: "L-D's OBJECTION O-20 bears here" → "O-27 bears here"; OBJECTIONS first note cites O-27.
- **L-R** — OBJECTIONS: CANON-04. **L-V** — OBJECTIONS: "The 1w gap is settled by O-28." and the annotation of O-16 (a)
  from DISPOSITIONS FID-17; "Drafting record" stays as history.
- **L-C** / **L-G** / **L-L** — headers only.

---------------------------------------------------------------------------------------------------------------
## CANON-40 · THE DISCLOSURES A VERDICT READER NEEDS — D-5 … D-12
**Settles:** CMP-24. **Authority:** OD-18 ("appended to `DISCLOSURES.md` as D-5… by the assembler").

**CANON TEXT.** Before the freeze the assembler appends to `T12/DISCLOSURES.md` the entries D-5..D-12 as the finding gives
them (the drafters' looks at FILED outcomes, by file; the breadth reading against the early-coverage cohort; P-ADM-1's
known point; the pivot-state analogue of P-DIR-1's cohort; the verdict law's clause (c), the m = 1 bar and the
five-cluster size; the scalper's mechanics; the tuning-fit traverse; the pre-filing ledger rows), with two conformances to
this canon: D-10's "a stop fills at the open on a gap" holds for BOTH range rows (CANON-14), and D-12 names the flag
`entered_before_book_frozen` (CANON-37). L-0's digest line on RUNNERS is NOT carried. No section fixer writes these.

**PER-SECTION EDITS.** **L-0** — L-0.10 stage table, TC12-LEANS row: "`T12/DISCLOSURES.md` appended" → "`T12/DISCLOSURES.md`
appended with D-5..D-12 (the drafters' and reviewers' disclosures; OD-18)". **L-X** — L-X.28 §9 prints them (CANON-32).

---------------------------------------------------------------------------------------------------------------
## CANON-41 · STATISTICS RECORDS (OD-16) — superseded verdicts, refusal spread, size footnote, key overlaps
**Settles:** STA-03, STA-05, STA-08, STA-10. **Authority:** OD-16; contract :5 (resume item 3), :8-9.

**CANON TEXT.**
(a) **A refile never drops a verdict.** Before a record is replaced under `--refile=<id>`, every `rows[]` leaf whose
`verdict_of_record`, `n`, `point`, `lo`, `hi` or `p_num` will change is appended whole to `scores/SUPERSEDED.jsonl`
(append-only, tracked) with the refile id and the scorer and regbook shas. The fresh leaf carries `superseded[] = [{id,
verdict_of_record, n, point, lo, hi, p_num, p_den, book_sha256}]`, the qualifier `RE-SCORED AFTER <id>`, and one §0 line
per entry under its cell: `before <id>: <word> · n … · point … · [lo, hi] · p …`. For a regbook rebuilt BEFORE TC12-SCORE
(L-0.10 T7), `superseded[]` also lists every quarantined `regbooks/<ID>/scored.json` sidecar under `T12/_det_partial_*/`
with its `book_sha256`, `n`, `sum_net_r` and AP id (the sidecar's own numbers, no ruler), printed the same way with the
qualifier `REBUILT AFTER FIRST BUILD (AP-n)`. F-S0-FIVE is RED when a row with a REFILE_LOG entry or a quarantined sidecar
lacks its line.
(b) **REFUSAL SPREAD** (count-only, decided before any outcome is read; every two-sample row): `a` = the number of
declared assets holding ≥ 1 refused campaign; `z = Fraction((N − a)**N, N**N)`. Filed: `refused_n`, `refused_assets`,
`p_draw_identically_zero`, `n_draws_exact_zero`. If `z ≥ bar_f` the row carries the qualifier `REFUSALS ON a/N ASSETS —
the ruler cannot clear (P(draw ≡ 0) = z ≥ bar)`; the word is NOT SUPPORTED and the test is spent; the cell is never cited
as evidence against the gate. `a = 0` is TWO-SAMPLE-PREMISE.
(c) **The size footnote** is X's `SIZE_FOOTNOTE`, read by `ast` from `x_rec/scripts/tc11x_score.py`, printed on every one
of the five rows (in `verdict_text` and as the last line under each §0 row) and in §1 beside the three bars. Rows gain
`size_footnote` and `size_measured {ruler, n_clusters, nominal, one_sided_size}`; F-VERDICT `[SIZE]` regenerates the size
deterministically from the tier seed on synthetic exchangeable clusters, separately for the two forms the rows use (vs
zero; kept-versus-all at a fixture-typed refusal share), and each row prints the figure of ITS ruler and cluster count. §1
prints Σ_f m_f·bar_f computed from the parse beside the footnote.
(d) **Key overlaps under the selection_hazard cells** (counts only, no outcome): under P-BRD-1 (below D-1) the six cells
of `stage_g/g_brd17.parquet`; under P-DIR-1 `n_refused` and, of those, the number in TC11 R5's `EXP_COUNTER` and
`EXP_ALIGNED` cells (the pivot state at the entry instant: a mirror of `align_of`, `scripts/tierc11_stage_r.py:1650-1661`,
on `T11/stage_r/NEST_v6.parquet`, calibrated 4h), filed by `tierc12_stage_r_dir.py` in `stage_r/dir/build_manifest.json`
under `r5_overlap`. F-S0-FIVE is RED when either line is absent. The leaf `arm__brd17` carries the note "outcome of this
split seen at R0 (D-1)".

**PER-SECTION EDITS.**
- **L-X** — L-X.27: (a); L-X.26: rows gain `superseded`, `size_footnote`, `size_measured`, and on two-sample rows the four
  keys of (b); `scores/SUPERSEDED.jsonl` joins the outputs; L-X.7: (b) after the TWO-SAMPLE-PREMISE bullet; L-X.9
  qualifier list: the (b) qualifier, `RE-SCORED AFTER <id>`, `REBUILT AFTER FIRST BUILD (AP-n)`; L-X.14: (c) in place of
  "and the size footnote (…)"; L-X.13: (d); L-X.2: the Σ sentence; L-X.28: CANON-32 point 2; F-VERDICT gains the case "a
  synthetic gate refusing on two of five assets must carry the qualifier".
- **L-0** — L-0.10 T7: "… and the scorer prints the superseded sidecar's n and ΣR beside the row (L-X.27)"; L-0.5:
  `scores/SUPERSEDED.jsonl` on the append-only list (CANON-05).
- **L-G** — the two specs' exhaustive-words sentence gains "REFUSALS ON a/N ASSETS when the refusals sit on too few
  assets for the ruler to clear"; L-G.13: names the count of (d) and its source (`g_brd17`).
- **L-R** — P-DIR-1 spec: the same qualifier sentence; L-R.6: names the count of (d) and files `r5_overlap`; §E: "the
  count of v6 campaigns the gate refuses, and on how many home assets (L-X.7's REFUSAL SPREAD and panel clause decide the
  word and its qualifier)".

---------------------------------------------------------------------------------------------------------------
## CANON-42 · F-NOT LEG LICENCE; THE TWIN WORDS
**Settles:** CMP-19. **Authority:** OD-18; contract :40-41.

**CANON TEXT.** F-NOT gains leg LICENCE (the licence set is L-V.17 item 9's): "FAILS IF a regbook arm or stage table
holding a `TRADE_COLS_T` column with a value-area lane (`sfp-va-*`, `scalp_va_*`) has a sidecar `(lens, toll)` whose trade
of record is outside `VA_MIRROR.json licence_set`, unless the arm is on the fixture-typed list `ORDERED_TWINS_T` =
{P-SFP-VA-1 `tierE__maker_conditioned` and `tierE__maker_assumed` (:75); P-SCALP-3's all-taker twin COLUMN (:102);
`tierE__panel17` rows of the twelve (:84)}; or a range builder's directory `READ_SET.json` holds no `licence_reads` entry
for its own pair. Plants: a `lens = 12h` arm copy; a 1h taker arm shipped as `scored`." `VA_MIRROR.json beside.twin_words`
carries `"4h|maker"` (CANON-11 point 6), printed beside the SFP maker twin.

**PER-SECTION EDITS.** **L-0** — L-0.30: the leg, in the list "1W, ACTS, POST-HOC, LICENCE". **L-V** — L-V.17 items 7 and 9.
**L-R** — L-R.24: the maker twin prints `twin_words["4h|maker"]` beside; the SFP builder calls `licence("4h", "taker",
"ALL")` (and `("1d", "taker", …)` for the 1d cell) before any book. **L-S** — L-S.1, L-S.27: the builder calls
`licence("1h", "maker", "holdout")`; L-S.26: the twelve's rows are on `ORDERED_TWINS_T`.

---------------------------------------------------------------------------------------------------------------
## INDEX — which canon items each section must apply

| section | canon items with edits (or an explicit "no edit") for it |
|---|---|
| L-0 | 02, 04, 05, 06, 07, 09, 10, 11, 12, 21, 23, 24, 25, 26, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42 |
| L-D | 02, 05, 09, 23, 24, 25, 26, 27, 28, 29, 31, 34, 35, 39 |
| L-V | 02, 03, 04, 05, 09, 10, 11, 12, 17, 19, 20, 22, 23, 24, 25, 26, 28, 32, 33, 34, 39, 42 |
| L-X | 01, 05, 06, 07, 08, 09, 15, 17, 18, 19, 21, 23, 24, 25, 26, 29, 30, 31, 32, 34, 35, 36, 39, 40, 41 |
| L-C | 02, 05, 06, 09, 10, 12, 19, 23, 24, 25, 26, 28, 33, 38, 39 |
| L-G | 01, 02, 06, 07, 09, 10, 12, 19, 21, 22, 23, 24, 25, 26, 28, 33, 35, 36, 37, 38, 39, 41 |
| L-R | 01, 02, 03, 04, 06, 07, 09, 10, 11, 12, 13, 14, 15, 16, 19, 20, 21, 22, 23, 24, 25, 26, 28, 32, 33, 35, 36, 38, 39, 41, 42 |
| L-S | 01, 02, 03, 06, 07, 08, 09, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 31, 32, 33, 35, 36, 38, 39, 42 |
| L-L | 02, 05, 06, 07, 09, 10, 11, 12, 19, 23, 24, 25, 26, 28, 29, 30, 31, 32, 33, 35, 36, 37, 38, 39 |

## RECONCILER'S DECISIONS THE ORCHESTRATOR MAY REVISIT (each is settled above and built as written unless ruled otherwise)

1. **CANON-02** reads OD-2 to the letter: DOOR 2 (`tierc12_va_trades.py`, `TC12-V.trades`) builds the Tier-E two-trades
   tables whole, `tierc12_stage_r_tables.py` is struck, and the 1w typed pair is (the reader, DOOR 2).
2. **CANON-09 / CANON-10** keep OD-7's path `va/stamps/VA_STAMPS_<book>.parquet` for three children by typing `va/stamps`
   as the one shared directory (cumulative manifest, scoped helper legs); the alternative is one subdirectory per child.
3. **CANON-22** settles CMP-31 (left "to the orchestrator" by the finding) for counts and diff rows on all three gates; no
   `tierE__reride` arm.
4. **CANON-29** takes a detached linked worktree for the tc11-stamp proof where O-10 says "scratch clone" (a clone cannot
   run TC11's suites); O-10 needs a one-line annotation.
5. **CANON-05** follows OD-4's freeze of `DISCLOSURES.md` at the registry commit and therefore opens
   `T12/DISCLOSURES_BUILD.md` for build-time disclosures after it.
6. **CANON-09** adds the record key `transcript` (and `depends_on`, `parent`, `supersedes`, `legs_not_run`,
   `provenance`) to L-0.9's schema, makes `TC12-V.trades` blocking before `TC12-C`, and hosts the scorer's code at
   `TC12-ENV.score-build` with its transcript under `env/` (not `scores/`, which T5 guards).
7. **Acts that are the orchestrator's at the freeze:** the TC12-LEANS record (CANON-05 point 5); AM-1 in
   `LEANS_AMENDMENTS.md` (CANON-34); D-5..D-12 (CANON-40); `forward/BOOK4_FREEZE.json` after the ledger-spec commit
   (CANON-37); the `tierc12_progress.py` change at TC12-REG (CANON-05 point 2, CANON-35 point 4).
8. **Seeded sample counts** (CANON-23 F) are typed by the owning section in this pass, not by the reconciler.
