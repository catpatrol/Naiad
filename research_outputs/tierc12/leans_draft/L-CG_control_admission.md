## L-C · CONTROL

This section reads Stage C of the contract (:48-50) and the fixture the contract names for it (F-CTRL, :114). It
fixes what "card v6" is by object; the two rides Stage C makes on ONE tape (the scored window, by look-back to
TC11's pin; and the extended corridor to TC12's pin); the 9/12 book; what Stage C files; what "cross-process
anchored" means; the leg of record of F-CTRL and its sibling legs; the two laws under which Σ net_r is stated and
the file that supplies each; the comparator (and the NaN hazard it repairs); the as-of-dependent columns and how
they are bounded rather than hidden; the forward strip; and the campaign frames handed to the V5 stamps. It owns no
registered row. It conforms to ORCHESTRATOR_RULINGS O-1..O-32; it files no objection.

**Abbreviations (both sections of this file).** `M` = `/Users/luis/Naiad`. `T12` = `research_outputs/tierc12`.
`T11` = `research_outputs/tierc11`. `XR` = `research_outputs/tierc12/x_rec` (byte copies of TC11-X, held in the main
tree; every read through `E.x_rec`, which asserts the file's sha against its row of `XR/X_REC_MANIFEST.json`; the
manifest's own sha is read through `tierc12_progress.certified`, L-0.4 — never from a record named by hand).
"contract :n" = line n of `exchange/queue/2026-10-08_TC12_APOLLO.md` (prefix sha `861d6050…a7bd`). "Record" = a
file `T12/progress/<record id>.json`. `E` = the TC12 env shim `scripts/tierc12_env.py` (L-D.25). The lineage
modules are named by the referee's own aliases, which no hunk renames (L-D.26): `E.TP` = `tierc10_panel`, `E.TB` =
`tierc2_baseline`, `E.T9` = `tierc9`, `E.T8` = `tierc8`, `E.LAB` = `tierc7_lab_regime`, `E.T5` / `E.T6` / `E.T7` =
`tierc5` / `tierc6` / `tierc7`, `E.R7` = `tierc7_rules`, `E.R6` = `tierc6_rules`, `E.R2` = `tierc2_rules`.
`PIN` = `E.PIN_MS` = TC12's pin. `W` = `E.TC11_PIN_MS` = TC11's pin, THE SCORE EDGE (`E.TC11_PIN_ISO` its ISO
form; both read from `T11/data/AS_OF_PIN.json` keys `as_of_last_closed_4h_close_ms`, `as_of_last_closed_4h`);
`E.TC10_PIN_MS` = that record's `tc10_pin_close_ms`. `ERA_CUT` = `E.ERA_CUT_MS`. `MS_4H` = `E.TP.MS_4H`.
`E.CLASSIC5` = the five home assets in the lineage's order (the referee's `tuple(TP.CLASSIC5)`, the lineage's
`UNIVERSE` object); `E.PANEL17` = the seventeen. A campaign's INSTANT is its `entry_close_ms = entry_ms + MS_4H`,
the close of its 4h entry bar; its era is `E.era_of(entry_close_ms)`.
**Convention.** A value written "(on file: v)" is orientation for the reader; the constant the build uses is the
named object, read at run time. A sha written `abcd…wxyz` is abbreviated; the build reads the full value from the
record named beside it.
**Tags.** [verified here] = opened and checked by this drafter on 2026-10-08, or in the revision pass recorded
below, read-only.
**Drafting record.** Read as text or inspected structurally: the contract; the rulings; DISCLOSURES; scout maps U3
and U5 in full; the sibling drafts L-0, L-D, L-V, L-X; `scripts/tierc9.py`, `tierc7_lab_regime.py`,
`tierc10_panel.py`, `tierc11_books.py`, `tierc11_stage_g.py`, `tierc11_forward_ledger.py`, `tierc11_score.py`,
`engine/indicators.py`; `XR/scripts/tc11x_books.py`, `tc11x_era.py`; TC11's `books/`, `stage_g/`, `regbooks/`,
`registrations/`, `scores/` records and X's `forward/BOOK_SPECS.json`, `era/X4_stamps.parquet` (schemas, keys,
shas). No module of the estate was imported or executed. No outcome of any TC12 book was computed. While verifying
citations this drafter read FILED outcome records of TC11 and X — `T11/stage_g/STAGE_G.md` (gate rows, the crossed
tables), `T11/books/BOOKS.md`, `T11/scores/S0_VERDICTS.md` (the P-AGE-1 and P-WIN-1 rows and their Tier-E rows) and
`XR/tierc11x/era/X4.md:8-46` (the E-2 rows, the breadth row and its twins among them). No reading below was chosen
between rivals by any of those numbers; where two readings are equally faithful the choice is argued by mechanism
and precedent in the reading itself.
**Revision record (2026-10-09).** Revised once under ORCHESTRATOR_DISPOSITIONS OD-0..OD-19 and the cross-section
canon of the LEANS review (`T12/review/CROSS_SECTION_CANON.md`). Opened while revising, as text, schema or key
listing only: the contract, the rulings, DISCLOSURES, the review records; `scripts/tierc11_env.py:719-752`,
`:868-870`; `scripts/tierc11_books.py:150-221`; `scripts/tierc9.py:93-130`, `:1286-1328`; the `UNIVERSE`, `TIDE_*`,
`PROVISIONAL_MIN_N` lines of `scripts/tierc2_rules.py` … `tierc7_rules.py`; `XR/scripts/tc11x_books.py:176-211`,
`:584-612`; `XR/scripts/tc11x_era.py:164`, `:227`; the column names (no row) of `T11/stage_g/g_campaign_gates`,
`g_grid_books`, `g_gate_rows` and `XR/tierc11x/era/X4_stamps`; the texts and payload shas of TC11's P-AGE-1 and
P-WIN-1 registrations; `T11/registrations/REGISTRY_PIN.json`; the key lists of TC11's two build manifests and of
X's `BOOK_SPECS.json`, with the `roles` block of the first and the `priority` block of the second printed whole
(the second holds, beside its counts, the filed ΣR of TC11's nearer-stop priority book — a TC11 number already on
file and used for nothing here); `T11/stage_g/STAGE_G.md:187-189` and `:197` (the pre-seen row the label cites,
with the filed figures printed on that line — the look D-4 already records); the whole-file shas of the files
this section pins. No parquet row was opened, no outcome of any TC12 book was computed, and no edit was chosen
between rivals by any number.

---------------------------------------------------------------------------------------------------------------
### A · The card and the rides

**L-C.1 CARD v6 BY OBJECT** — "card v6 re-ridden" (contract :48)
READING:
- The card ridden is the object `E.TP.CONTROL_CARD` (`T8.Card(name="v6-control")`, every knob at its class default)
  with the roles object `E.T9.V6_ROLES`. No TC12 source constructs a card or a roles object, calls
  `dataclasses.replace` on one, or passes a knob as a keyword.
- "Card v6" as a CLAIM is the dict `E.TP.ride_spec(E.TP.CONTROL_CARD, E.T9.V6_ROLES)` = `{card_class, card_fields,
  roles_class, roles_fields}` (every dataclass field but the free `name`, as `repr`). Before any ride the builder
  asserts it equal, key for key and string for string, to (i) `E.TP.CONTROL_RIDE` and (ii) the FILED dict
  `XR/tierc11x/forward/BOOK_SPECS.json` → `books.v6.ride_spec` (file sha on record `72a1f523…cac3`; on file:
  `card_class` "tierc8.Card", 29 `card_fields`, `roles_class` "tierc9.Roles", 6 `roles_fields`). HALT `CARD-MOVED`
  on any difference. The count of fields is `len()` of the filed dict; no field name or value is typed in TC12 code.
- WHERE THE 29 FIELDS ARE FILED: at run time, X's record above. Its origin is TC10's registration
  `research_outputs/tierc10/registrations/P-TRG-2.json` key `book_spec.arms[0].ride.card_fields` (sha
  `1e9982d1…85af`), equal to X's dict on all 29 keys [verified here]. That TC10 file is not on the shim's
  `TC10_ALLOW` (L-D.25: eight records, no ninth without a dated amendment) and is NOT read at run time.
- `E.TP.is_control_book(card, roles, E.CLASSIC5)` must be True: the control is the one book `E.TP.run_cell_n` rides
  without registration paperwork, and Stage C rides nothing else through that door.
- The ride path's code is frozen by L-D.29 (every lineage module re-hashed at each shim import; X's
  `path_modules`). The taker fee is the module object `tierc2_rules.FEE_BPS_SIDE` inside `tierc7._account_chain`
  (a constant of the ride, not a file read); TC12's fee file is held equal to it by the shim (L-D.26 P4). The
  control pays no maker fee.
- Every book manifest Stage C writes carries, per book, `ride_spec` (the dict above) and `roles_name`, so L-0.30's
  F-NOT legs (ENTRY-CROSS, TRAIL-OFFSET, ADDS) can read them.
SOURCE: `scripts/tierc10_panel.py:816` (`CONTROL_CARD`), `:874-882` (`ride_spec`, `CONTROL_RIDE`), `:1083-1092`
(`is_control_book`); `scripts/tierc9.py:93-119` (`Roles`, `V6_ROLES`); `XR/tierc11x/forward/BOOK_SPECS.json`
[verified here: 29 + 6 fields]; `research_outputs/tierc10/registrations/P-TRG-2.json` [verified here: equal];
`scripts/tierc11_env.py:140-158` (`TC10_ALLOW`); scout U3 §1.1.
RIVALS: retype the fields in TC12 code — contract :8. Read P-TRG-2.json at run time — a ninth TC10 read on an
operator-pending record for a dict X already files. `tierc6_rules.CARD_V6` as "the card" — it is the parent class's
object; leg F-CTRL-A holds the two rides equal instead.
FAILS-IF: **F-CTRL-CARD** (`scripts/tierc12_books_fixtures.py`) FAILS IF the live `ride_spec` differs from X's filed
dict or from `CONTROL_RIDE`, a book manifest's `ride_spec` differs from it on a card field, or (AST) a non-fixture
TC12 source constructs or `replace`s a card or roles object. Planted mutations: one `card_fields` value changed in a
COPY of the filed dict → `CARD-MOVED`; a shadow builder handing `run_cell_n` a card with one knob moved and no
registration → the door's own HALT (counted as the catch); `dataclasses.replace(E.T9.V6_ROLES, …)` planted in a copy
of the builder → the AST leg RED.

**L-C.2 TWO RIDES ON ONE TAPE: THE SCORED WINDOW BY LOOK-BACK, AND THE EXTENDED CORRIDOR** — "card v6 re-ridden on
the extended corridor; F-CTRL reproduces TC11's filed v6 book trade-by-trade … on TC11's corridor" (contract :48-49)
READING: one process binds one substrate, the TC12 snapshot (O-5, L-D.28). Both rides run in that process on the
same frames; the difference is the index bound.
- **Windows.** `(lo12, hi12, meta12) = E.TP.corridor_n(E.CLASSIC5)`; HALT unless `hi12 + 1 == E.PIN_MS`.
  `(lo11, hi11, meta11) = E.TP.corridor_n(E.CLASSIC5, pin_close_iso=E.TC11_PIN_ISO)`; HALT unless
  `hi11 + 1 == E.TC11_PIN_MS` and `lo11 == lo12`. `corridor_n` admits a pin only if it is a 4h close and looks back.
- **`V6_SCORED`** = `E.TP.run_cell_n(E.TP.CONTROL_CARD, E.T9.V6_ROLES, E.CLASSIC5, lo11, hi11)` — THE SCORED-WINDOW
  BOOK (O-9): the campaigns with `entry_close_ms ≤ W`, ridden with `hi11` = the last 4h bar closing `≤ W`. Every
  campaign's ride ends at bar `hi11`; a campaign still open there is marked at that bar's close with `exit_reason
  = "corridor_end"` (the lineage's default exit), so `exit_close_ms ≤ W` on every row. This is the base of every
  gate of Stages G and R (O-21) and the book F-CTRL holds to TC11's filed one.
- **`V6_EXT`** = the same call with `(lo12, hi12)`, `hi12` = the last 4h bar closing `≤ PIN` — the book "re-ridden
  on the extended corridor".
- **THE FORWARD STRIP of a book** = its extended-ride campaigns with `W < entry_close_ms ≤ PIN` (L-C.10).
- **Identity between the two (the prefix identity of the two rides).** For every `V6_EXT` campaign with
  `entry_close_ms ≤ W` whose `V6_SCORED` twin is not `corridor_end`, the two Trade objects are equal at full float
  on every `E.TP.CTRL_COLS` field and on `exit_reason` (the ride is causal and bounded; F-CTRL-EXT asserts it
  in-process, L-C.9). A campaign OPEN at `W` is compared on its entry, stop and R only (L-C.9's continuation law).
- **Every consumer re-rides.** A stage that needs the v6 book calls `tierc12_books.v6_scored()` /
  `v6_ext()` in its own process (each HALTs unless `E.TP._book_sha` of the scored book equals TC11's certified
  value, L-C.6). No stage reads a `books/*.parquet` back as a ride input: the tables are written at the lineage's
  rounding and are referees and prints, never inputs (TC11's precision law, `T11/books/BOOKS.md:7`).
- **The rejection log.** `run_cell_n` discards the armings. Where they are needed (the arming counts below; the
  slot-arbitration count of L-G.17) the builder calls `E.T9.replay9(s, CONTROL_CARD, V6_ROLES, lo, hi)` per asset in
  `E.CLASSIC5` order and HALTs unless `E.TP._book_sha` of those trades equals the `run_cell_n` book's (TC11's
  `v6_replay` law, mirrored).
SOURCE: `scripts/tierc10_panel.py:650-733` (`corridor_n`; "a pin may only look back" :690-699), `:1095-1189`
(`run_cell_n`; the window check :1173-1179); `scripts/tierc9.py:334-452` (`replay9`), `:266` (`corridor_end`);
`scripts/tierc11_stage_g.py:285-299` (`v6_replay`); `T11/books/BOOKS.md:27-28` (F-912-ANCHOR: a book ridden to an
earlier pin on a longer tape reproduced bit for bit); L-D.28; O-5, O-9, O-21; scout U3 R2, H2, H9.
RIVALS: (a) the scored book = `V6_EXT` filtered on entry close — not taken: a campaign open at TC11's pin would
carry an exit read past the score edge (O-9). (b) a second process bound to `tc11_20260925` — not taken: L-D.28.
(c) read TC11's filed parquet as the base — not taken: "the certified books are the referees, never inputs" (X's
law), and a 6-dp table cannot reproduce the full-float book sha.
FAILS-IF: F-CTRL (L-C.6), F-CTRL-A and F-CTRL-EXT (L-C.12). Planted mutations: the look-back bound dropped (the
scored book ridden to `hi12`) → `CAMP-ASOF` in F-CTRL-CAMP (a window open at TC11's pin carries another
`window_end_i`) and, where the strip holds an entry, `CTRL-KEY`; the corridor pinned by day count instead of by bar →
`corridor_n`'s own HALT.

**L-C.3 THE 9/12 BOOK AND ITS OPEN SOL CAMPAIGN AT TC11's PIN** — "every funnel instant of every book (base v6,
9/12, …)" (contract :44); "all four books (base · 9/12 · OLD-gated · combined-gated)" (contract :109)
READING:
- **Roles.** `R912 = E.T9.SWEEP_CELLS[-1]`, PROVEN without constructing anything: `type(R912) is E.T9.Roles`,
  `R912.name` equals `XR/tierc11x/forward/BOOK_SPECS.json` → `books.trg912.roles_name`, and
  `E.TP.ride_spec(E.TP.CONTROL_CARD, R912)` equals that record's `books.trg912.ride_spec`; and its `roles_fields`
  equal `T11/books/build_manifest.json` → `roles.trg912` on every period key. HALT `912-ROLES` otherwise. The two
  trigger periods are also held equal to the contract's `9/12` by the pin door: pin `book.trg912_periods` (:44, two
  capture groups), asserted equal to `(R912.trg_f, R912.trg_s)`.
- **Ride.** Not the control, so not through `run_cell_n`: `E.T9.replay9(s, E.TP.CONTROL_CARD, R912, lo, hi)` per
  asset in `E.CLASSIC5` order, after the window check `run_cell_n` would apply (`hi` a 4h close no later than the
  corridor end). `T912_SCORED` on `(lo11, hi11)`; `T912_EXT` on `(lo12, hi12)`.
- **Anchor at TC11's pin (F-CTRL-912).** `E.TP._book_sha(T912_SCORED)` equals `T11/books/build_manifest.json` →
  `book_sha.trg912` (on file: `2c32fd60…e030`) and `len` equals `n.trg912` (on file: 199); its journal equals TC11's
  filed `books/trg912_journal.parquet` under L-C.8's comparator, and its campaigns table equals
  `books/trg912_campaigns.parquet` on every column class of L-C.9.
- **The open campaign.** TC11's filed 9/12 book holds exactly one `corridor_end` row (on file: SOLUSDT, entry bar
  open 2026-09-24T16:00Z, `T11/books/BOOKS.md:71`). In `T912_SCORED` it is reproduced AS FILED — marked at the close
  of bar `hi11`, `open_at_asof` True. In `T912_EXT` it is a CONTINUATION (L-C.9): entry, stop and R exact, its exit
  whatever the extended tape gives. Its entry close is `≤ E.TC11_PIN_MS`, so it is NOT a strip entry; it is printed
  in the strip print under class `continuation` (L-C.10).
- The 9/12 book is scored by nothing in TC12. It exists as a stamp target (V5), a ledger book (L-L) and an anchor.
SOURCE: `scripts/tierc9.py:93-130` (`Roles` with `trg_f`, `trg_s`; `SWEEP_CELLS`) [read here];
`scripts/tierc11_books.py:270-303` (`r912`, `trg912_book`, `_check_window`); `T11/books/build_manifest.json` keys
`book_sha`, `n`, `roles` [verified here]; `T11/books/trg912_campaigns.parquet` (one `open_at_asof` row) [verified
here]; contract :44, :109; L-0.17 (the pin `book.trg912_periods`); L-0.30 (ENTRY-CROSS).
RIVALS: prove the cell by `dataclasses.replace(V6_ROLES, trg_f=…, trg_s=…)` as TC11 did — not taken: L-0.30's
ENTRY-CROSS leg forbids a TC12 source building a roles object with a period, and X's filed dict supplies the claim.
FAILS-IF: **F-CTRL-912** FAILS IF the roles proof fails, the pin `book.trg912_periods` differs from `(R912.trg_f,
R912.trg_s)`, the look-back 9/12 book's sha or n differs from TC11's manifest, a journal cell differs, or the open
row is not reproduced as `corridor_end` with TC11's mark. Planted mutations: `SWEEP_CELLS[-2]` taken in a shadow
builder → `912-ROLES` (its trigger periods also differ from the pin's); the SOL row's mark taken from the extended
ride → `CTRL-DIFF` on its exit columns.

**L-C.4 WHAT STAGE C FILES** — "the extension printed separately (the forward strip, never scored)" (contract :50)
READING: record `TC12-C`, builder `scripts/tierc12_books.py` (a DECISION module on `VA_BLIND_T`, L-0.22), directory
`T12/books/` — the one writer of that directory (L-0.9). Every parquet goes through L-0.13's `put` (declared key,
lineage rounding, nine stamps, collar per L-0.16 — none of these tables is registered). The lineage's skip-empty
law stands: an empty frame is not written and is listed under the manifest's `skipped_empty` (L-0.13).

| file | key | rows | stamped with |
|---|---|---|---|
| `v6_journal.parquet`, `trg912_journal.parquet` | `[asset, entry_ms]` | `E.TP.journal_frame(book)` of the SCORED-window book | the score edge (`meta11`) |
| `v6_campaigns.parquet`, `trg912_campaigns.parquet` | `[symbol, entry_ms]` | TC11's campaign columns (below), SCORED-window book, as-of `hi11` | the score edge |
| `v6_ext_journal.parquet`, `trg912_ext_journal.parquet` | `[asset, entry_ms]` | the EXTENDED-ride book | the pin (`meta12`) |
| `v6_ext_campaigns.parquet`, `trg912_ext_campaigns.parquet` | `[symbol, entry_ms]` | the campaign columns, as-of `hi12`, plus `segment`, `entered_after_tc11_pin`, `open_at_tc11_pin` | the pin |
| `strip.parquet` | `[book, symbol, entry_ms]` | L-C.10 | the pin |
| `ctrl_prefix.parquet` | `[book, symbol, entry_ms]` | L-C.9: one row per FILED campaign, its class and every moved cell | the pin |
| `arming_log.parquet` | `[book, window, symbol, arm_ms, direction]` | one row per ARMING of each ride, window ∈ {`scored`, `extended`}: `arm_i`, `tide_ok`, `d_ok`, `trigger_ms` (null if none), the window end as known, `reject` (`entered`, `tide`, `d`, `no_trigger`, `position_open`); no price, no R | the pin |
| `arming_counts.parquet` | `[book, window, symbol, reject]` | the counts of the log by `reject` | the pin |
| `build_manifest.json`, `READ_SET.json`, `BOOKS.md`, `FIXTURES_BOOKS.txt` | — | L-0.13's manifest and its open log (every snapshot, TC10, TC11, X and TC12 record path the builder process read); the stage document; the transcript | — |

The keys above are the declared keys L-L.25 types the ferry classes from; this section assigns no class.

- **Campaign columns.** The tuple `CAMPAIGN_COLUMNS` and the map `NULL_IFF`, read by `ast.literal_eval` from the TEXT
  of `scripts/tierc11_books.py` (`:193-221`; its sha asserted against TC11's PROGRESS, stage TC11-BOOKS), built by
  `tierc12_books.campaign_rows(book, roles, lo, hi, pool, name)` — THE ONE campaign-row function of the tier
  (L-0.14: no second implementation of one law): the mirror of TC11's `campaign_rows` (`:417-504`) and its seams
  (`:347-415`) `entry_streak`, `trailing_edges`, `band_of`, `lag_band`, `known_window_end`, `exit_event`,
  `latch_bar` — each mirrored function naming its source lines, each held equal to TC11's FILED table by
  F-CTRL-CAMP. Its columns carry `lag`, `r_over_atr`, the latch and exit-event stamps, and are a superset of X's
  fifteen `BOOK_COLS` (`XR/scripts/tc11x_era.py:227`) and eleven `TIDE_COLS` (`XR/scripts/tc11x_books.py:208-211`)
  [verified here by comparing the three tuples]; L-L reads `lag` and the eleven tide columns from it, and no port
  of X's own `campaign_rows` exists. The numbers those seams hold as literals in TC11 are READ in TC12: the lag
  bands `LAG_BANDS` and the band codes by `ast.literal_eval` from the same text (`:157-158`), asserted consistent
  with L-G.5's cut and L-G.3's codes; the absolute cut and the far-stop cut are L-G.8's and L-G.16's objects,
  asserted equal to the text's `ABS_TIDE_CUT` and `R_OVER_ATR_CUT` (`:155-156`) read the same way; `MS_4H` by object.
  `window_end_i` is the end AS KNOWN at the ride's as-of (`known_window_end`: an open window carries `hi_i + 1`,
  never a later bar).
- **The module's API** — X's names and signatures where X's twin `XR/scripts/tc11x_books.py` has them, so the
  gates, the range stage and the ledger call one set and no helper exists twice: `corridor(pin_close_iso=None)`,
  `r912()`, `v6_book(lo, hi)`, `trg912_book(lo, hi)`, `book_sha(book)`, `v6_scored()`, `v6_ext()`, `v6_replay(lo,
  hi)` (the book with its armings), `tide_pool(lo, hi)` (= `E.T9._trailing_pool(lo, hi)`), `entry_streak(t)`,
  `trailing_edges(t, pool)`, `band_of(run, edges)`, `known_window_end(end_i, hi_i)`, `campaign_rows(book, roles,
  lo, hi, pool, name)` (above), `abs_tide_cut()`, `lag_cut()`, `ratr_cut()`, `written_journal(book)`, and the
  three exact comparators `cell_delta`, `exact_frame_diff`, `nan_cells` (L-C.8). Beside them, as module
  attributes read from text and never typed: `CAMPAIGN_COLUMNS`, `NULL_IFF`, `LAG_BANDS`, `BAND_CODES` (TC11's
  text, above) and `TIDE_COLS` (`ast.literal_eval` from `XR/scripts/tc11x_books.py:208-211`, asserted a subset of
  `CAMPAIGN_COLUMNS`).
  - **`replay_h(sym, lo_ms, hi_ms, *, refuse=None)`** is THE ONE v6 re-ride with a refusal hook (L-G.18):
    `refuse(ctx) -> bool`, `ctx` carrying TC11's keys `sym`, `arm`, `ti`, `d`, `stp`, `atr`, `r_over_atr`. The hook
    is an opaque callable: `tierc12_books` imports nothing for it. L-R's direction predicate and L-L's `(band,
    lag)` predicate are adapters written in their own modules; `tierc12_forward.reride_gated` calls `replay_h` and
    holds no replay loop of its own.
  - **`base_regbook_frame()`** returns the frame of the `base` arm — the one function every `base` arm of the tier
    (P-ADM-1, P-BRD-1, P-DIR-1) is built from. It writes nothing: the owning stage hands the frame to
    `tierc12_regbook.write_arm` (L-X.24), whose only writer is L-0.13's `put_regbook` (full float).
- **`segment`** = `scored_window` iff `entry_close_ms ≤ W`, else `strip` (`W < entry_close_ms ≤ PIN`);
  `entered_after_tc11_pin` is its boolean; `open_at_tc11_pin` is True iff the campaign's SCORED-window twin is
  `corridor_end`. The era column is `E.era_of(entry_close_ms)` (`tuning` iff `entry_close_ms ≤ ERA_CUT`).
- **Precision.** Every flag, band and era is computed from the Trade objects at full float BEFORE the write
  rounding; the filed flag is the value of record; nothing downstream re-derives a flag from a rounded column.
- **`BOOKS.md`** prints: both instants and the bar count between them (`T12/data/AS_OF_PIN.json` key
  `bars_4h_past_tc11_pin`); the anchors of L-C.12 with their shas; the scored-window books' descriptive tables
  (TC11's layout, labelled CONTROL / DESCRIPTIVE, collared); the Σ laws of L-C.7; the prefix table; the strip print.
- **Inheritance, printed, not re-held.** TC11's own anchors against TC10 (its F-CTRL (b) against
  `research_outputs/tierc10/panel/control_journal.parquet`, F-912-ANCHOR, F-AGE-ANCHOR; transcript
  `T11/books/FIXTURES_BOOKS.txt`, sha `336a2163…5c10`) are cited with their shas as the chain TC10 → TC11 → TC12. TC12
  re-reads no TC10 record for them.
SOURCE: `scripts/tierc11_books.py:193-221`, `:347-415`, `:417-504` [read here]; `scripts/tierc5.py:1058` /
`tierc10_panel.py:85` (`journal_frame`); `XR/scripts/tc11x_books.py:208-211`, `:584-586` (`TIDE_COLS`,
`tide_pool(lo, hi)`), `XR/scripts/tc11x_era.py:227` (`BOOK_COLS`) [read here, as text];
`scripts/tierc11_stage_g.py:449-566` (`replay_g`, the hook's `ctx` keys); L-0.9, L-0.13, L-0.14, L-0.16, L-0.22;
L-X.24; `T11/books/BOOKS.md:7-9`; scout U3 §1.5, R5, R16.
RIVALS: one book table with a segment column and no look-back ride — not taken (L-C.2 rival (a)). Re-hold TC11's
TC10 anchors on the TC12 tape — not taken: three more reads of operator-pending TC10 records to re-prove what a
certified transcript proves; the chain is printed. A port of X's `campaign_rows` beside this one, or a replay loop
of its own in the ledger or the range stage — not taken: one law, one implementation.
FAILS-IF: per directory, L-0's helper legs F-KEY [books], F-DET [books], F-COLLAR [books]; **F-CTRL-CAMP**
(L-C.12). Planted mutations: a required column nulled in a copy; a scored-window table stamped with the pin (F-KEY
stamp-truth); a `to_parquet` bypass in a shadow builder (F-WARRANTY: the only writers are L-0.13's two); `put`
handed a root under `regbooks/` in a shadow builder (F-WARRANTY).

---------------------------------------------------------------------------------------------------------------
### B · F-CTRL

**L-C.5 "CROSS-PROCESS ANCHORED" — WHAT THE ANCHOR IS** — "F-CTRL reproduces TC11's filed v6 book … cross-process
anchored" (contract :48-49); "F-CTRL 0.000e+00 cross-process" (contract :114)
READING: the anchor is a RECORD FILED BY ANOTHER PROCESS IN ANOTHER BUILD, read sha-first, never regenerated:
- **The referee of record** is TC11's filed v6 journal `M/research_outputs/tierc11/books/v6_journal.parquet`, written
  by TC11's stage TC11-BOOKS on snapshot `tc11_20260925`. It is git-ignored and exists only in the main working
  tree, so it is read by ABSOLUTE main-tree path through `E.tc11_record("books/v6_journal.parquet")`, which asserts
  the file's sha256 equal to the sha `T11/PROGRESS.json` certifies under `stages[TC11-BOOKS].artifact_shas` (on
  file: `deb70b09…2a5c`; PROGRESS itself accepted at its R0 sha, or at the value `T12/close/TC11_STAMP_MAP.json`
  names for it once that map reads `applied: true` — L-0.24, L-D.27) BEFORE a byte is parsed. A sha mismatch is
  `CTRL-SHA` and nothing is compared.
- **The second filed object** is the full-float book sha `T11/books/build_manifest.json` → `book_sha.v6` (a tracked
  file; on file: `f3c68f54…9132`, with `n.v6` 200), read through `E.tc11_record` the same way.
- **A second process already agrees on these bytes** and is printed beside as a witness, deciding nothing:
  `XR/tierc11x/books/v6_x_journal.parquet`, written by TC11-X in another tree, hashes to the same file sha as TC11's
  journal [verified here]. TC12 is the third build to reproduce the book and the first to do so on another snapshot.
- **The substrate half** of the anchor is L-D's: F-D-PREFIX (L-D.12) and F-ENV-ASOF (L-D.31) prove the TC12 tape cut
  at TC11's pin bit-identical to the TC11 snapshot. F-CTRL does not run unless both are GREEN in `progress/TC12-D`
  and `progress/TC12-ENV`.
- **What is NOT the anchor.** Two TC12 subprocesses compared with each other are F-DET (L-0.20) — self-comparison
  across processes, banned as a referee by L-0.14. A TC12 process bound to the TC11 snapshot does not exist (L-D.28).
SOURCE: O-3, O-21; L-D.27 (`tc11_record`), L-D.28; `T11/PROGRESS.json` stage TC11-BOOKS [verified here: nine
artifact shas, all re-hash equal]; `XR/tierc11x/books/BOOKS_X.md:29-31`; X's sha-first law
`XR/tierc11x/LEANS_X.md:128 ff.` (LX-0.3); scout U3 §1.7, C2, C3, R4, H6.
RIVALS: (a) a TC12 anchor process on `tc11_20260925` — not taken: L-D.28. (b) subprocess twins as "cross-process" —
not taken: both sides would be TC12's own code on TC12's own tape. (c) X's journal as the referee — not taken: X is
unmerged and its file equals TC11's; TC11's is the contract's "filed v6 book".
FAILS-IF: F-CTRL clause 0 (L-C.6): a referee whose sha is not the certified one must stop the leg. Planted mutation:
one byte flipped in a scratch copy of the referee handed to the comparator → `CTRL-SHA`.

**L-C.6 F-CTRL — THE LEG OF RECORD** — "F-CTRL reproduces TC11's filed v6 book trade-by-trade to 0.000e+00 on TC11's
corridor" (contract :48-49)
READING: held BEFORE any Stage C file is written (a RED anchor writes nothing). Live side: `V6_SCORED` (L-C.2).
0. **SHA (sha-first).** Each referee — the filed journal and `T11/books/build_manifest.json` — is read through
   `E.tc11_record` and its sha256 equals the certified one (L-C.5) before a byte is parsed; otherwise `CTRL-SHA`
   and no later clause runs.
1. **BOOK-SHA (full float).** `E.TP._book_sha(V6_SCORED)` — sha256 of the sorted `[symbol, lane, entry_ms,
   repr(float(net_r))]` rows of the Trade objects — equals `T11/books/build_manifest.json` → `book_sha.v6`, and
   `len(V6_SCORED)` equals `n.v6`. This is the demand for "book sha `f3c68f54…`": the expected value is READ from
   that key, never typed. Because it hashes `repr` of the full float, no write rounding can hide a drift in `net_r`.
2. **KEY.** The live journal's key set `(asset, entry_ms)` equals the filed journal's in both directions; a key on
   one side only is `CTRL-KEY`.
3. **TRADE BY TRADE.** The live journal AS WRITTEN — `E.TP.journal_frame(V6_SCORED)` passed through the lineage's
   write rounding (`E.TB._round_floats`, its decimals read from the function's signature) — against the filed
   journal: for every key and every column of `E.TP.CTRL_COLS`, `cell_delta == 0.0` under L-C.8's exact law, and
   `exit_reason` equal. `worst` = the largest `cell_delta` over all cells; the leg passes iff `worst == 0.0`, and the
   transcript prints it with the lineage's format (`worst=0.000e+00`), the token the contract quotes at :49.
4. **WHOLE.** Every column the live `journal_frame` shares with the filed journal (the frame's own columns; the
   stamp and collar columns are not in the frame) is equal as a column: `E.TB._content_sha` of the two frames
   restricted to the shared columns and sorted on the key by mergesort. The count of shared columns is printed and
   must equal the live frame's column count (no column silently outside the comparison).
5. **NaN census.** The count of NaN cells in the `CTRL_COLS` of each frame is printed; a non-zero count on either
   side is `CTRL-NAN`.
6. **STAMPS.** The nine `E.TP.AS_OF_COLUMNS` of the written scored-window journal are compared with the filed
   journal's and printed column by column. Every one must be equal (the look-back as-of IS TC11's pin) EXCEPT
   `as_of_substrate`, which must differ: the filed value is TC11's snapshot name, the live one Stage D's. Any other
   difference, or an equal `as_of_substrate`, is `CTRL-STAMP`. This is why the filed table's CONTENT sha cannot be
   reproduced and is not demanded.
7. **Σ.** L-C.7's two laws.
- The leg is held in the builder (it gates the build) and re-held by `F-CTRL` in the suite from the FILED TC12
  table against the same referee (the suite never trusts the builder's own print).
SOURCE: `scripts/tierc10_panel.py:1988-1995` (`_book_sha`), `:2707-2724` (`CTRL_COLS`, `ctrl_diff`, the `.3e` print);
`scripts/tierc2_baseline.py:155-188`; `XR/scripts/tc11x_books.py:912-966` (`ctrl_c_findings`: SHA, KEY, DIFF, WHOLE);
`T11/books/v6_journal.parquet` [verified here: 200 rows; 44 frame columns + 9 stamps; `as_of_substrate`
"tc11_20260925"]; scout U3 §1.5-§1.7, H13, H15, H18.
RIVALS: (a) the comparison at the written rounding alone — not taken as sufficient: clause 1 is the full-float
identity beside it. (b) demand the filed parquet's content sha or file bytes — not taken: `as_of_substrate` names
another snapshot and parquet bytes depend on the writer build (U3 H18). (c) a tolerance — banned (L-D's common law:
"a tolerance standing in for an identity").
FAILS-IF: **F-CTRL** FAILS IF any of clauses 0-7 fails. Planted mutations, each inside production or on a copy and
each caught by its NAMED detector: the referee's byte flip of L-C.5 → `CTRL-SHA`; one campaign's structural stop
moved by one tick of its asset (`E.ticks()`) inside
a shadow ride → `CTRL-DIFF` and `BOOK-SHA`; one `net_r` moved by one ulp on a Trade object → `BOOK-SHA` RED while
clause 3 stays GREEN (the transcript says so: the full-float clause is the stricter); one filed campaign dropped
from a copy of the referee → `CTRL-KEY`; a NaN planted in the last numeric `CTRL_COL` of one live row → `CTRL-DIFF`
with `worst = inf` and `CTRL-NAN` (and the transcript prints that `E.TP.ctrl_diff` alone returned ok — L-C.8); a
shared column removed from the comparison set → the WHOLE clause's coverage count RED; `as_of_last_closed_4h` of the
written table set to the pin → `CTRL-STAMP`.

**L-C.7 Σ net_r — TWO LAWS, TWO FILES** — "(Σ net_r 40.807566 at its pin)" (contract :49)
READING: three values of the filed v6 book's Σ net_r are on disk under two laws [verified here]. Both laws are
asserted, each under its own name, each against the file that supplies it; neither is typed.
- **LAW S6 — the sum of the filed 6-dp column.** THIS IS THE CONTRACT'S NUMBER. It is supplied by
  `T11/scores/BASE_IDENT.json` key path `v6.sum_net_r_6dp` (file sha on record `29f795dc…5581`, certified by TC11's
  PROGRESS stage TC11-SCORE; written by TC11's scorer as `float(v6["net_r"].sum())` over
  `books/v6_campaigns.parquet`; on file: 40.807566). TC12 computes S6 EXACTLY: `Σ Decimal(repr(x))` over the `net_r`
  column of the scored-window journal as written (each written value is its shortest decimal, so the sum is exact
  and order-free). Asserted equal as `Decimal`, three ways: the live column's sum == the filed journal's column sum
  == `Decimal(repr(BASE_IDENT value))`; and that value == the contract's token, parsed from :49 by the pin door
  (pin `ctrl.sum_net_r`, regex `Σ net_r (\d+\.\d+) at its pin`). At run time the number is READ from
  BASE_IDENT.json; the contract's token is the second object.
- **LAW SF — the rounding of the full-float sum.** `E.TB.r6(sum(float(t.net_r) for t in V6_SCORED))` in
  `run_cell_n`'s book order — TC11's own expression — equals `T11/books/build_manifest.json` → `net_r_sum.v6` (on
  file: 40.807565). Beside it, the exactly-rounded sum `math.fsum(float(t.net_r) for t in V6_SCORED)` equals, as
  `float.hex`, `T11/regbooks/P-AGE-1/base.json` → `sum_net_r` (on file: 40.80756457414756).
- The two laws differ in the last printed digit on this book. Every TC12 print of the v6 Σ names its law: "ΣR
  (6-dp column sum)" or "ΣR (r6 of the full-float sum)". The 9/12 twins are asserted the same way against
  `net_r_sum.trg912` (law SF) and the filed 9/12 journal's column sum (law S6).
SOURCE: `T11/scores/BASE_IDENT.json:48` [verified here]; `scripts/tierc11_score.py:1263`;
`scripts/tierc11_books.py:1059`; `scripts/tierc2_baseline.py:145-147` (`r6`); `T11/regbooks/P-AGE-1/base.json`
[verified here]; decimal sums of both filed tables' `net_r` columns [verified here: 40.807566]; scout U3 §1.6, C1.
RIVALS: assert only the contract's number — hides that TC11's manifest, PROGRESS and STAGE_G print the other.
Assert only the manifest's — fails the contract's sentence. A pandas float sum for S6 — order- and
method-dependent; the decimal sum is exact.
FAILS-IF: F-CTRL clause 7 FAILS IF either law's equality fails or the contract token differs from BASE_IDENT's
value. Planted mutations: one written `net_r` moved by one unit of the last rounded decimal in a copy → `SUM-6DP`;
the two referees swapped (S6 compared with the manifest's value) → `SUM-LAW` RED — proving the laws are
distinguishable on this book; the contract token re-typed in a shadow builder instead of read → F-TYPED.

**L-C.8 THE COMPARATOR: EXACT, NaN-AWARE (X's REPAIR XFB-V1)** — "to 0.000e+00" (contract :49)
READING: `E.TP.ctrl_diff` takes `max()` over per-column `np.max(np.abs(Δ))`. A column holding a NaN has a NaN
maximum, and Python's `max` DROPS a NaN that follows a finite value (`max(0.0, nan)` is `0.0`): a NaN column can
pass as zero. TC12 therefore runs, beside `ctrl_diff` and as the deciding comparator, three functions PORTED from
X's source (AST-identical, each naming its lines; L-D's port law):
- `cell_delta(x, y)`: `0.0` iff `x == y`; else `|x − y|`, or `inf` when that is not finite. A NaN on either side
  differs (two NaNs differ too). The result is never NaN, so no `max` can drop it and no `> 0` test can miss it.
- `exact_frame_diff(got, want, cols)` on two frames aligned row for row: per column the count of cells not exactly
  equal, and the worst `cell_delta`.
- `nan_cells(df, cols)`: the explicit NaN census.
"Differs by > 0" is read per cell as NOT EXACTLY EQUAL. `ctrl_diff` is still called and its result printed; a
disagreement between it and the exact comparator is itself printed (it is the hazard, made visible).
SOURCE: `scripts/tierc10_panel.py:2712-2724`; `XR/scripts/tc11x_books.py:759-792` (`cell_delta`,
`exact_frame_diff`, `nan_cells`), `:794-799` (the repair's statement) [read here, as text]; scout U3 H17.
RIVALS: `ctrl_diff` alone (TC10, TC11) — the hazard. `np.nanmax` — treats a NaN as absent, the opposite of the law.
FAILS-IF: **F-CTRL-PORT** FAILS IF a ported function is not AST-identical to X's at the manifest sha. F-CTRL's NaN
plant (L-C.6) is the production proof: with the exact comparator removed in a shadow builder, the planted NaN must
pass `ctrl_diff` (printed) and the fixture must go RED on `CTRL-NAN`.

**L-C.9 THE PREFIX / CONTINUATION LEG ON THE EXTENSION; THE AS-OF-DEPENDENT COLUMNS** — "card v6 re-ridden on the
extended corridor" (contract :48)
READING: F-CTRL-EXT holds the EXTENDED rides to TC11's filed tables as a prefix. Referees: `books/v6_journal`,
`v6_campaigns`, `trg912_journal`, `trg912_campaigns` (each sha-first, L-C.5).
- **Column classes.** Every column of a filed campaigns table is in exactly ONE class; the class map is typed in
  the FIXTURE (a second object) and compared with the builder's:
  - KEY: `symbol`, `entry_ms`;
  - STABLE: TC11's `ROW_FIELDS` — "the as-of-STABLE campaign fields" — read by `ast.literal_eval` from the text of
    `scripts/tierc11_forward_ledger.py:94-106` (the text's sha asserted against TC11's PROGRESS, stage
    TC11-T-RELAY, before it is parsed);
  - AS-OF-DEPENDENT: TC11's `AS_OF_DEPENDENT`, read the same way from `:107-108` (on file: `window_end_i`,
    `window_end_close_ms`, `window_open_at_asof`, `open_at_asof`, `continuation`, `entered_after_tc10_pin`);
  - STAMP: the nine as-of columns (L-C.6 clause 6);
  - any filed column in none of these is `COLUMN-COVERAGE` and the leg is RED.
- **In the leg of record nothing is excluded.** At the look-back as-of the dependent columns are reproduced too:
  F-CTRL-CAMP demands the scored-window campaigns tables equal TC11's filed ones on KEY, STABLE and
  AS-OF-DEPENDENT alike (the windows open at TC11's pin carry the same `hi11_i + 1`).
- **On the extended ride**, per filed campaign, one of two classes, filed in `ctrl_prefix.parquet`:
  - `closed` (filed `exit_reason` is not `corridor_end`): present live; every STABLE column and every journal
    `CTRL_COL` EXACTLY equal (L-C.8); `exit_reason` equal; `open_at_asof` False; `continuation` and
    `entered_after_tc10_pin` equal. No funding-explained drift of `net_r` is admitted (TC10's `ctrl_prefix`
    allowance is NOT carried: L-D.12 proves the funding prefix bit-identical). The three window columns are equal
    EXCEPT on a row whose FILED `window_open_at_asof` is True, where the live values must satisfy the one-sided law
    `window_end_i(live) ≥ window_end_i(filed)` and, when the live window has closed, `window_end_close_ms >
    E.TC11_PIN_MS`. Every such moved cell is listed (key, column, filed → live); the number of rows with a moved
    window cell must not exceed the number of filed rows with `window_open_at_asof` True (on file: 3 in v6); a
    window cell moved on any other row is `EXT-ASOF-ROW`.
  - `continuation` (filed `corridor_end`; on file: none in v6, one in 9/12): `entry_px`, `stop_px`, `r_dist`
    EXACT; the live exit bar opens at or after `E.TC11_PIN_MS` (the filed ride reached the close of its last bar
    with no exit, so the live one cannot exit inside the filed window); live `n_advances` and
    `mfe_r` `≥` the filed (a NaN is not `≥`): the filed ride is a prefix of the live one (X's CTRL-B-CONTINUATION).
    `open_at_asof` may move from True to False on such a row AND ON NO OTHER; its exit columns and `net_r` are the
    only STABLE-class cells allowed to differ, and each is listed (filed → live).
- **Live-only campaigns** must all have `entry_close_ms > E.TC11_PIN_MS`; one at or before it is `EXT-EARLY` (drift
  inside the filed window). They are the strip entries.
- The same identities are held in-process at full float between the Trade objects of `V6_SCORED` and `V6_EXT`
  (L-C.2) — the comparison no rounding can blur.
SOURCE: `scripts/tierc11_forward_ledger.py:94-108` [read here; sha `e33a75fa…adfa`];
`scripts/tierc11_books.py:396-401` (`known_window_end`), `:437-474`; `XR/scripts/tc11x_books.py:837-909`
(`ctrl_b_findings`); `scripts/tierc10_panel.py:2737-2823` (`ctrl_prefix`, its funding-drift clause);
`T11/books/v6_campaigns.parquet` [verified here: `open_at_asof` 0, `window_open_at_asof` 3, `continuation` 1,
`entered_after_tc10_pin` 0]; scout U3 H13, H14, H16.
RIVALS: (a) drop the dependent columns from every comparison — hides a moved `open_at_asof` or a window that moved
on a closed row. (b) `E.TP.ctrl_prefix` as written — admits a funding-explained `net_r` drift and carries the NaN
hazard. (c) compare content shas of whole tables — cannot hold (stamps).
FAILS-IF: **F-CTRL-EXT** FAILS IF a filed campaign is absent live, a `closed` row differs on a STABLE column or a
`CTRL_COL`, a window cell moves on a row whose filed window was closed or violates the one-sided law, a
`continuation` row breaks its law, a live-only campaign entered at or before TC11's pin, or a filed column is in no
class. Planted mutations: a closed campaign's `exit_ms` moved in a copy of the live table → `EXT-CLOSED`; a
`window_end_i` changed on a filed-closed-window row → `EXT-ASOF-ROW`; a live-only row planted with an entry close at
TC11's pin → `EXT-EARLY`; a continuation with its stop moved → `EXT-CONT`; a MUTANT CLASS MAP that moves `exit_ms`
into AS-OF-DEPENDENT (so a real difference would be excused) → `COLUMN-COVERAGE` against the fixture-typed map.

**L-C.10 THE FORWARD STRIP** — "the extension printed separately (the forward strip, never scored)" (contract
:49-50); O-9
READING:
- **Membership.** A campaign of an extended-ride book is a STRIP ENTRY iff `W < entry_close_ms ≤ PIN` — its entry
  bar's CLOSE is after TC11's pin (`entry_close_ms = entry_ms + MS_4H`; `≤ PIN` holds by the corridor). Membership
  is by ENTRY close, never by exit, arm or bar open. The strip is taken from the SECOND ride (`hi12`, the last bar
  closing `≤ PIN`), never from the scored-window ride.
- **For every ridden arm (O-9, OD-14).** The strip law is one law for every book and every arm of the tier. This
  stage files the strips of the two books it rides (v6, 9/12) in `books/strip.parquet`; the strip of every regbook
  arm is filed by the stage that owns the regbook, in `regbooks/<ID>/strip.parquet` under the column `arm`
  (L-X.24; for the gates, L-G.18).
- **Two printed classes**, both in `strip.parquet`, column `strip_class`: `strip_entry` (above), and `continuation`
  — a campaign with `entry_close_ms ≤ W` that its SCORED-window book marks `corridor_end`; printed with both exits
  (the scored mark and the extended-ride exit) and counted in NO strip n.
- **What is printed** (`strip.parquet` and `BOOKS.md`): per book the count `n_strip_entries`, `n_open_at_pin`
  (strip entries that are `corridor_end` at TC12's pin) and `n_continuations`; then one row per campaign: `book`,
  `symbol`, `direction`, `arm_open_ms`, `entry_ms`, `entry_close_ms`, `exit_ms`, `exit_reason`, `open_at_pin`,
  `bars_held`, `entry_px`, `stop_px`, `r_dist`, `net_r` (the row's own), `lag`, `r_over_atr`, the tide facts at entry
  (L-G.2-L-G.4), `entered_after_tc10_pin`. Stage G adds the refusal flags as stamps in its own strip table (L-G.19).
- **What is never produced** over strip rows, by Stage C or any other stage: a ΣR, a mean, a hit rate, an interval,
  a p, a verdict word, a pooled figure with the scored window, or a row of any registered arm. A count is the only
  aggregate. Per-row `net_r` is diary-keeping (X's LX-X5.5) and is printed.
- **Two boundaries, both printed.** The strip's boundary is TC11's pin (this stage, O-9). The forward ledger's
  opening is TC10's pin (contract :109; L-L). `entered_after_tc10_pin` on every row lets a reader reconcile them:
  the ledger admits the strip entries plus the campaigns entered between the two pins (on file: none in v6, the SOL
  campaign in 9/12, `T11/books/BOOKS.md:70-71`).
- The strip tables are stamped with the PIN (L-0.13: every table that reads past `W` is) and collared.
SOURCE: O-9; contract :49-50, :109-110; L-X.14 (`strip` leaf: `n` per arm and one pointer, no statistic), L-X.24;
`XR/tierc11x/LEANS_X.md:2082-2085` (LX-X5.5); scout U3 C8, C9, R6, R7.
RIVALS: boundary at TC10's pin — not taken: O-9; the campaigns between the pins are TC11's scored water. Print
strip aggregates "for information" — not taken: an aggregate over unspent water is a look.
FAILS-IF: **F-CTRL-STRIP** FAILS IF a `strip_entry` row has an entry close at or before TC11's pin or a
scored-window row one after it; a `continuation` is counted in a strip n; or any Stage C table or document carries
an aggregate statistic over strip rows (the fixture scans the stage's tables for a row whose population is strip
rows and that holds a `mean`, `sum`, `win` or interval column, and `BOOKS.md`'s strip section for any number not
traceable to a row or a count). Planted mutations: membership taken by the bar OPEN in a shadow builder (a campaign
entered on the bar closing at TC11's pin changes side — constructed on a synthetic frame if the book holds none) →
`STRIP-EDGE`; a `sum_net_r` column planted in a copy of a strip table → `STRIP-STAT`.

**L-C.11 THE CAMPAIGN FRAMES HANDED TO THE V5 STAMPS** — "every funnel instant of every book (base v6, 9/12, the
gated books, every arm below) carries the VA vector" (contract :44-45)
READING: Stage C stamps nothing itself, imports nothing of the value area and opens no path under `T12/va/`
(`tierc12_books` is on `VA_BLIND_T`). No book builder stamps its own book (O-29, O-31).
- **The frames.** Stage C files the two frames the instant law needs — `books/v6_ext_campaigns.parquet` and
  `books/trg912_ext_campaigns.parquet` — each holding `symbol`, the key column `entry_ms` and, as int64 ms (null =
  did not happen), `arm_close_ms`, `entry_close_ms`, `latch_1r_open_ms`, `harvest_close_ms`, `exit_event_ms`,
  beside `exit_event_stamp`, `exit_reason` and `open_at_asof`. All are members of `CAMPAIGN_COLUMNS` (L-C.4), their
  nullability held by `NULL_IFF` in F-KEY [books].
- **Their kind**, declared here in L-V.19's form (the `.c` row of its table), one per book: `book` = `v6` /
  `trg912`; `lens` 4h; `key` `[entry_ms]`; `start_col` = `arm_close_ms` (TC11's `KINDS["v6transform"]`: the run of
  bar closes starts at the ARM close); `end_col` = `exit_event_ms`; `bar_close_lens` 4h; events `arm` and `entry`
  (stamp `close`); `plus_1r` (`latch_1r_open_ms`, `open_of_bar`, with its post-event stamp); `harvest`
  (`harvest_close_ms`, `close`); `bell` and `exit` (from `exit_event_ms`, told apart by `exit_reason`, stamped by
  `exit_event_stamp` — an intrabar exit is `open_of_bar` with its post-event stamp); `as_of_pin` for a row whose
  `open_at_asof` is True (never `exit`).
- **Who stamps.** The child record `TC12-V.stamps.c` (L-V.19; `depends_on` `TC12-V`, `TC12-C`) runs the reader
  over those two frames and files `T12/va/stamps/VA_STAMPS_v6.parquet` and `VA_STAMPS_trg912.parquet`, key `[book,
  symbol, entry_ms, instant_kind, instant_ms]`, pinned in that child's record.
- **THE v6 INSTANTS ARE STAMPED ONCE:** every gated book and every v6-derived arm is a key subset of that table
  (L-G.18), never re-stamped. Only entered campaigns have instants; rejected armings are logged and counted
  (`arming_log.parquet`, `arming_counts.parquet`), not stamped.
SOURCE: contract :44-46; O-29, O-31; L-V.19, L-V.20; `scripts/tierc11_books.py:193-221` (the named columns are in
`CAMPAIGN_COLUMNS`) [read here]; `scripts/tierc11_stage_r.py:213-216` (`KINDS`), `:258` [read here];
`T11/stage_r/NEST_v6.parquet`, `NEST_trg912.parquet` (L-V's F-NEST-KEYS referees).
RIVALS: stamp inside the control builder, or under a child of TC12-C — not taken: the builder would import the
value-area reader, and the stamps are Stage V tables filed under Stage V's own children (O-29, O-31).
FAILS-IF: L-V's F-NEST-KEYS and F-NEST-ASOF [v6], [trg912], hosted at `TC12-V.stamps.c` (suite
`scripts/tierc12_va_stamps_fixtures.py --stage=TC12-V.stamps.c`). Here: F-CLOSURE's `VA-BLIND` leg (L-0.22) on
`tierc12_books.py`, proven by AST and from `books/READ_SET.json` — planted mutation: an import of the stamps
reader in a copy of the builder → `VA-BLIND` RED.

**L-C.12 THE STAGE C FIXTURE ROLL** — "F-CTRL 0.000e+00 cross-process" (contract :114)
READING: suite `scripts/tierc12_books_fixtures.py`, record `TC12-C`, transcript `T12/books/FIXTURES_BOOKS.txt`
(L-0.19's hosting map); L-0.14's dialect (BREAK leg first; a plant counts only when a finding names its detector;
one `prove` call and one transcript block per row below). The contract's name F-CTRL maps to every block whose id
starts `F-CTRL` — the one PREFIX name of L-0.19's map; every other contract name matches its FID exactly. Every
leg runs on the v6 control, which has no precondition: none is ever `CLOSED-NO-BOOK`. A leg that cannot run is
`NOT RUN` (L-0.14), never PASS.

| block | FAILS IF | planted mutation that must turn it RED |
|---|---|---|
| **F-CTRL** (the leg of record) | L-C.6 clauses 0-7 | L-C.5's; L-C.6's; L-C.7's |
| F-CTRL-A (in-process) | `E.TP.run_cell_n(control)` differs from `E.T6.run_cell(E.R6.CARD_V6, lo, hi)` on any `CTRL_COL` at full float (Trade objects; L-C.8), in count or in an exit reason, on EITHER window; or `(lo12, hi12) != E.TP.control_window()` | a one-tick stop perturbation inside the shadow ride → `CTRL-A-DIFF`; the control ridden over a window one bar short → `CTRL-A-WINDOW` |
| F-CTRL-CARD | L-C.1 | L-C.1's |
| F-CTRL-PORT | L-C.8 | one token changed in a copy of a ported comparator |
| F-CTRL-CAMP | a scored-window campaigns table differs from TC11's filed one on any KEY, STABLE or AS-OF-DEPENDENT column at the written rounding, or in key set (v6 and 9/12) | the look-back bound dropped → `CAMP-ASOF`; the tide band taken on whole-corridor edges → `CAMP-TIDE`; the era taken by the bar open → `CAMP-ERA` |
| F-CTRL-912 | L-C.3 | L-C.3's |
| F-CTRL-EXT | L-C.9 | L-C.9's |
| F-CTRL-STRIP | L-C.10 | L-C.10's |
| F-KEY [books] · F-DET [books] · F-COLLAR [books] (L-0's helper legs) | L-0.21, L-0.20, L-0.16 | theirs |

SOURCE: `T11/LEANS.md:158-167` (L-1.7); `XR/tierc11x/LEANS_X.md:2306` (X's F-CTRL row);
`scripts/tierc6.py:558`, `scripts/tierc6_rules.py:220`; `scripts/tierc10_panel.py:2727-2735` (`control_window`).
RIVALS: none.
FAILS-IF: n/a (this reading is the roll).

UNVERIFIED (each decided at build, each a HALT or a printed count, none an input to a reading): that the look-back
ride on the TC12 tape reproduces `f3c68f54…` (it is F-CTRL itself; the precedent is F-912-ANCHOR); how many strip
entries either book holds; whether the three v6 windows open at TC11's pin have closed by TC12's.

---------------------------------------------------------------------------------------------------------------
---------------------------------------------------------------------------------------------------------------
## L-G · ADMISSION FAMILY

This section reads Stage G of the contract (:52-62) and its two fixtures (F-GATE, F-BRD, :117-118). It fixes the
tide age and its bands; "trailing q75, the cut of record"; the window age and its cut; the combined refusal and its
shadows; the per-asset per-bar tide-band series that breadth needs and that no file holds; breadth at the entry bar
and its cut in integers; the two fixtures; and the Tier-E tables — the breadth grid, the breadth-17 twin, the
crossed table in both forms, and the far-stop priority as slot arbitration. It owns two registered rows, P-ADM-1 and
P-BRD-1, whose REGISTRATION SPEC blocks close the section. It conforms to ORCHESTRATOR_RULINGS O-1..O-32 and files
no objection. Abbreviations, conventions, the drafting record and the revision record are those at the head of
L-C.

Record `TC12-G`, builder `scripts/tierc12_stage_g.py`; the tide series is built earlier, by
`scripts/tierc12_tide.py` under the child record `TC12-C.tide` (L-G.10). Both are DECISION modules on `VA_BLIND_T`
(L-0.22): neither imports the stamps reader nor opens a path under `T12/va/`, and the two registered rows read no
value-area column. `TC12-G` is in L-0.10's parallel set: it may start once every record through `TC12-V.stamps.c`
in the resume order, and its own `depends_on` — `TC12-C`, `TC12-C.tide`, `TC12-V.stamps.c`,
`TC12-ENV.score-build` (the regbook interface `scripts/tierc12_regbook.py` is filed there) — are
COMPLETE-VERIFIED.

---------------------------------------------------------------------------------------------------------------
### A · The family and its base

**L-G.1 GATES ARE POST-FILTERS OF ONE FILED BASE** — "ADMISSION FAMILY (m=2, bar 0.05; both two-sample vs v6 —
they remove trades)" (contract :52); "refuse a trigger" (contract :53)
READING:
- The base of both rows is ONE book: `V6_SCORED` (L-C.2), held to TC11's filed v6 by F-CTRL and, on the regbook
  interface, by L-X.25's F-BASE-IDENT. A gate REMOVES campaigns from it and adds none: `scored = [t for t in base if
  key(t) not in refused]`, `key(t) = (symbol, entry_ms)` — the SAME Trade objects in the base's order (TC11's
  `apply_gate`, mirrored). No entry is admitted into a slot a refusal frees.
- "Refuse a trigger" is read at the CAMPAIGN: in v6 the entry bar is the trigger bar (`entry_i = ti`, `entry_px =
  close[ti]`), every trigger that enters is one campaign, and the refusal is judged with facts known at that bar's
  close. The trigger-level evaluation inside the replay (a refused trigger not occupying the slot) is the RE-RIDE,
  a Tier-E disclosure (L-G.18), never the scored arm (O-21).
- The scored window is the base's (`entry_close_ms ≤ W`). The strip (`W < entry_close_ms ≤ PIN`, from the extended
  ride) is filed FOR EVERY ARM of both regbooks — `base`, `scored` and every Tier-E arm — in each regbook's
  `strip.parquet` under the column `arm` (L-G.18; O-9, OD-14), printed with the gates' flags and scored by
  nothing: a count and a pointer are its only aggregates (L-C.10).
- Family, m and bar are L-X.1's parse of :52 and :9; this section types none of them.
SOURCE: O-21; `T11/LEANS.md:141-150` (L-1.5); `scripts/tierc11_stage_g.py:302-303`, `:408-411` (`key_of`,
`apply_gate`); `scripts/tierc9.py:388-404`; L-X.5, L-X.25; scout U5 §2 item 1, R-G4.
RIVALS: refuse inside the replay as the scored arm — not taken: O-21; it can admit a campaign the base never took,
and the pre-seen cell (L-G.7) is a post-filter.
FAILS-IF: L-X's GATE-POSTFILTER (a scored key absent from the base, or a kept row differing from its base row) and
F-GATE (L-G.9). Planted mutation: a campaign admitted by a shadow in-replay gate added to a copy of the scored arm.

---------------------------------------------------------------------------------------------------------------
### B · The combined refusal (P-ADM-1)

**L-G.2 TIDE AGE** — "the tide age at the entry bar" (contract :53)
READING:
- The TIDE of an asset is the two-state sign of (EMA_fast − EMA_slow) of its 4h close: `+1` when
  `e_fast[j] > e_slow[j]`, `−1` otherwise, defined from the asset's own warm bar `WARM = E.LAB.TIDE_WARM_BARS` on
  (below it: state 0, run −1). The periods are the lineage objects `E.R7.TIDE_FAST`, `E.R7.TIDE_SLOW`; the EMA is
  `engine.indicators.ema` (seeded at the series start, hence the warm floor).
- The TIDE AGE at bar j is `run[j]`: the number of consecutive bars ending at j on which the state has not
  changed; THE FLIP BAR COUNTS AS BAR 1. Unit: 4h bars. `start[j]` is the index where the current streak began;
  `start[j] == WARM` marks the one LEFT-CENSORED streak per asset (already running at the warm floor): its run is
  a lower bound of its age.
- It is READ AT THE CAMPAIGN'S ENTRY BAR: `(state, run, start) = E.LAB.tide_streak(symbol)`; `age = run[entry_i]`;
  `left_censored = (start[entry_i] == WARM)`. The decision instant is that bar's close, `entry_close_ms`.
- Every v6 campaign enters at a bar index `≥ WARM` (the ride's floor), so `age ≥ 1` on every campaign; `age ≤ 0`
  at an entry is HALT `ADM-UNWARM`.
SOURCE: `scripts/tierc7_lab_regime.py:179`, `:306-349` [read here]; `scripts/tierc11_books.py:363-368`
(`entry_streak`); `T11/LEANS.md:357-361` (L-G.1); `engine/indicators.py:17-28`; `scripts/tierc2_rules.py:113-114`;
`XR/tierc11x/forward/BOOK_SPECS.json` `books.gated-v6-oldtide.gate.lineage_functions`; scout U5 §1.1, R-G1.
RIVALS: the arm-bar three-state age `E.T9.tide_streak_age` (`scripts/tierc9.py:537-560`) — another quantity; not the
filed pin; printed as a disclosure column only. Counting from bar 0 — the lineage's own "what would make this
wrong". The flip bar as 0.
FAILS-IF: F-GATE's DEF plants (L-G.9): the arm-bar age substituted → `DEF-AGE`; the run read at `entry_i − 1` →
`DEF-BAR`.

**L-G.3 THE BANDS B1..B4** — "is in the OLD band" (contract :53-54); "YOUNG or EARLY" (contract :58)
READING:
- Edges are three quantiles of the pooled streak distribution, at the fractions `E.LAB.STREAK_BAND_QUANTILES` (the
  lineage's tuple; the contract's "q75" is the pin `adm.old_quantile`, parsed from :54 by the pin door, regex
  `trailing q(\d+)`, and asserted equal to the LAST fraction times `PCT_PER_UNIT`).
- `band_index = int(numpy.digitize(float(run), edges))` (right = False) — `E.LAB._streak_band` — an integer from 0
  to `len(edges)`; with `e = edges`: index 0 ⇔ `run < e[0]`; index k ⇔ `e[k−1] ≤ run < e[k]`; the top index ⇔
  `run ≥ e[−1]`.
- Labels and codes come from `E.LAB.STREAK_LABELS` (on file: "B1 YOUNG tide", "B2 EARLY tide", "B3 MATURE tide",
  "B4 OLD tide"): the code is the label's first token.
- **OLD** = the band whose label contains the contract's word "OLD"; asserted to be the TOP index (`len(edges)`).
  So OLD ⇔ `run ≥` the last edge — the comparator is `≥`: a run EQUAL to the edge is OLD.
- **YOUNG-or-EARLY** = the bands whose labels contain the contract's words "YOUNG" or "EARLY"; asserted to be the
  contiguous set of indices from 0 up to some `k_ye`. So YOUNG-or-EARLY ⇔ `run < edges[k_ye]` (on file: the
  middle edge, the trailing median).
- A band is `None` when `run ≤ 0` or when the edges are undefined (L-G.4).
SOURCE: `scripts/tierc7_lab_regime.py:181`, `:446-447`, `:456-459` [read here]; `scripts/tierc11_books.py:378-386`
(`band_of`); `T11/stage_g/FIXTURES_STAGE_G.txt` F-EDGE ("run == q75 is OLD"); scout U5 §1.2.
RIVALS: OLD strict (`run >` the edge) — TC11's own EDGE-OLD plant. Band codes typed (`"B4"`), or the OLD index typed
(TC11's `AGE_OLD_BAND = 3`) — contract :8; both are derived from the lineage's labels.
FAILS-IF: **F-EDGE-G** (Stage G suite; typed boundary cases, production against the fixture's commission) FAILS IF
any comparator is not the typed one at its boundary: `run == q_top` is OLD and `run == q_top − 1` is not (on
integer-valued synthetic edges); `run == edges[k_ye]` is NOT young-or-early and one bar less is. Planted mutations:
OLD made strict → `EDGE-OLD`; young-or-early made inclusive → `EDGE-YE`.

**L-G.4 "TRAILING q75, THE CUT OF RECORD"** — "(trailing q75, the cut of record)" (contract :54)
READING: "trailing" is an EXPANDING prefix of a bar pool, not a rolling window and not the whole corridor.
- **The pool** `POOL = E.T9._trailing_pool(pool_lo_ms, PIN − 1)` (the lineage's object; it is what
  `tierc12_books.tide_pool(pool_lo_ms, PIN − 1)` returns): for each asset of `E.R7.UNIVERSE` (the five home
  assets), every 4h bar with OPEN in `[pool_lo_ms, PIN − 1]` and `run > 0` — BAR-POOLED: each warm panel bar is
  one vote — values `sk_v`, bar-open times `sk_t`, merged by a stable sort on time.
- **`pool_lo_ms` is READ**, never typed and never re-derived as the definition: `XR/tierc11x/forward/BOOK_SPECS.json`
  top-level key `pool_lo_ms` (on file: 1567958400000 = 2019-09-08T16:00:00Z), asserted equal to that record's
  `books.gated-v6-oldtide.gate.pool_lo_ms`, to `lo12` and to `lo11` (L-C.2: the corridor's panel start). HALT
  `POOL-LO-MOVED` if any of the four differs: a moved lower bound re-bands past entries.
- **The edges at an entry bar** with open `e = open_ms[entry_i]`:
  `edges = E.T9._trailing_edges(POOL, e)["streak_bar"]` = `numpy.quantile(sk_v[:i2],
  E.LAB.STREAK_BAND_QUANTILES)` with `i2 = searchsorted(sk_t, e, side="right")` (numpy's default linear
  interpolation) — every pooled bar whose OPEN is `≤ e`, the entry bar itself and the other assets' bars of the same
  open INCLUDED. Those bars have all closed at the decision instant `e + MS_4H`, so the prefix is causal.
- **The floor.** `edges` is `None` while the prefix holds fewer than `E.R7.PROVISIONAL_MIN_N` bars (on file: 30;
  asserted equal to X's spec `min_pool_bars`).
- **THE CUT OF RECORD:** a campaign is OLD iff `band_index(run, edges)` is the top index (L-G.3) ⇔ `run ≥` the
  trailing q75 edge at its entry bar.
- **An unbanded campaign HALTs** (`ADM-UNBANDED`): if `edges is None` at the entry bar of any campaign of the base
  or of the strip — or at a candidate bar the re-ride hook judges (L-G.18) — the stage stops and files nothing.
  It is NOT treated as "not refused". Reason: TC11's filed
  record states no campaign is unbanded on its corridor (`T11/stage_g/STAGE_G.md:122`), the pool only grows after
  it, and the frozen forward spec this refusal continues says `none_band: "HALT"`; an unbanded entry therefore means
  the pool or a floor moved — a defect, not a market fact.
- **Prefix stability.** Extending the tape appends bars at the END of the pool and cannot move an edge at an
  earlier entry. It is asserted, not assumed: for every campaign of the base, `(tide_streak_entry,
  tide_left_censored, q25, q50, q75 at the written rounding, tide_band)` equal TC11's filed
  `T11/stage_g/g_campaign_gates.parquet` row (leg ANCHOR of F-GATE, L-G.9).
SOURCE: `scripts/tierc9.py:1290-1328` [read here]; `scripts/tierc11_books.py:358-375`;
`XR/tierc11x/forward/BOOK_SPECS.json` keys `pool_lo_ms`, `pool_lo_source`, `books.gated-v6-oldtide.gate`
(`band_quantiles`, `min_pool_bars`, `none_band`) [verified here]; `XR/tierc11x/LEANS_X.md:2025-2033` (LX-X5.1: the
band is refresh-stable only if the pool's lower bound stays fixed); `scripts/tierc11_stage_g.py:321-323` (the silent
rival: `old_refused` returns False when the edges are `None`); `T11/stage_g/STAGE_G.md:122`; scout U5 §1.3, §2 item
2, R-G2, H3.
RIVALS: (a) a rolling window — no filed length; not the pin. (b) whole-corridor edges (`E.LAB.cuts`) — look-ahead;
never used. (c) a strict prefix (`open < e`) or a prefix to the entry close (admits bars opening at the decision
instant) — TC11's DEF-EDGE sabotages. (d) per-asset or episode-pooled edges — "NOT USED" in the lineage. (e)
unbanded → not refused (Stage G's code) — not taken: of the two filed treatments it is the one that lets a moved
floor pass silently; HALT is the frozen forward spec's.
FAILS-IF: F-GATE (L-G.9) — plants `DEF-EDGE` (whole-corridor edges; the one-bar-ahead prefix; the strict prefix),
`POOL-LO` (the pool's lower bound moved one bar in a shadow builder: the build must HALT `POOL-LO-MOVED`),
`UNBANDED` (a shadow `_trailing_edges` returning `None` at one entry: the build must HALT, and a mutant that maps it
to "not refused" must be caught by the fixture's own count of unbanded entries).

**L-G.5 WINDOW AGE AND THE 16** — "the window age (entry_i − arm_i) ≥ 16 bars" (contract :54)
READING:
- `lag = entry_i − arm_i`, both indices on the asset's own 4h tape: the count of 4h bars from the bar whose close
  ARMED the window (the window-pair cross) to the bar whose close TRIGGERED the entry. `lag = 0` when both happen on
  one bar. Unit: 4h bars. Asserted on every campaign: `open_ms[entry_i] − open_ms[arm_i] == lag · MS_4H` (a gap
  would break the equality; HALT `LAG-GAP`).
- A campaign is STALE iff `lag ≥ LAG_CUT` (inclusive).
- **`LAG_CUT` is READ BY OBJECT** from TC11's filed registration P-WIN-1: `T11/registrations/REGISTRATIONS.json`
  (pinned by TC11's chain head and the payload sha of the registration read; read through `E.tc11_record`), the
  registration whose `registration` is "P-WIN-1" (exactly one): its `text_of_record` matched by `lag ≥ (\d+) bars`
  (exactly one match) and its `operative_spec.scored_arm` matched by `entry_i - arm_i >= (\d+)` (exactly one
  match). HALT `LAG-CUT` unless both give one integer (on file: 16). That integer is asserted equal to the
  contract's — the pin `adm.lag_cut`, parsed from :54 by the pin door (regex `≥ (\d+) bars`). At run time the
  number is the filed text's; the contract's token is the second object.
- **The registry pin (one law for L-G.5, L-G.8 and L-G.16).** No whole-file sha of TC11's registry is a TC12 pin:
  TC12's own close act moves that file's sha (L-0.24). Before any registration is read, the build asserts (i)
  the chain head — `T11/registrations/REGISTRY_PIN.json` key `head` equals the file's own `head` and the head
  recomputed from the registrations' payload shas by the file's own `law` (the chain's `line_sha256` over `{seq,
  registration, sha256, prev}`); and (ii) for each registration it reads (P-WIN-1 here and in L-G.16, P-AGE-1 in
  L-G.8) that the registration's `sha256` equals the payload sha recomputed from its body by the same `law`. HALT
  `REG-PIN` otherwise. The head and the two payload shas are the pins the two spec blocks carry; the stamp of
  L-0.24 moves one leaf outside every payload and the chain, so none of the three moves.
- The filed text is the cut's only provenance (`T11/LEANS.md:373`: "The 16 cut has no on-disk provenance"); this
  reading adds none.
SOURCE: `T11/registrations/REGISTRATIONS.json` P-WIN-1 `text_of_record` (" P-WIN-1 [50%] window-age gate: refuse
triggers with arm→trigger lag ≥ 16 bars vs v6; …") and `operative_spec.scored_arm`, the keys `head`, `law` and each
registration's `sha256` [verified here]; `T11/registrations/REGISTRY_PIN.json` key `head` [verified here: equal to
the registry's own `head`]; L-0.24 (what the stamp moves: the leaf `contract.sha256`, outside every payload and
the chain); `scripts/tierc11_stage_g.py:331-336`; `XR/scripts/tc11x_books.py:347-362` (`abs_tide_cut`, the
read-by-object precedent); `XR/tierc11x/forward/BOOK_SPECS.json` → `books.gated-v6-oldtide.gate.p_age_1_payload_sha256`
(X pins the same registration by its payload sha) [verified here]; `scripts/tierc9.py:168-232`; scout U5 §1.6, §2
item 3, R-G3.
RIVALS: type 16 — contract :8. Lag in hours or in window-relative units — the contract's parenthesis is
`entry_i − arm_i`. `>` instead of `≥` — TC11's EDGE-WIN plant. Pin the registry by its whole-file sha — not taken:
the tc11-stamp close act moves it (L-0.24), and TC12's builders and fixtures must re-pass after the operator's
keystrokes.
FAILS-IF: F-GATE and F-EDGE-G: `lag == LAG_CUT − 1` kept and `lag == LAG_CUT` refused. Planted mutations: the cut
raised by one in a shadow builder → `EDGE-WIN` (and, on the book, REFUSED-SET RED iff a campaign sits exactly at the
cut; otherwise the boundary case is the proof); a second, disagreeing number planted in a copy of the registration
text → `LAG-CUT` HALT; one character of P-WIN-1's body changed in a scratch copy of the registry → `REG-PIN` HALT
(F-GATE leg BOUND); the leaf `contract.sha256` changed in a scratch copy (the stamp's own move) → NO finding, and
the transcript says so.

**L-G.6 THE COMBINED REFUSAL** — "refuse a trigger when the tide age at the entry bar is in the OLD band … OR the
window age (entry_i − arm_i) ≥ 16 bars" (contract :53-54)
READING: with `A` = the base campaigns that are OLD (L-G.4) and `S` = the base campaigns that are STALE (L-G.5),
- the refused set is the UNION `R_ADM = A ∪ S` (the contract's "OR" is inclusive: a campaign both OLD and stale is
  refused once);
- the scored arm is `base − R_ADM` (L-G.1), keyed `(symbol, entry_ms)`;
- every flag (`old_refused`, `stale_refused`, `adm_refused = old_refused or stale_refused`) is computed from the
  Trade object and the lineage arrays at full precision, and filed per campaign in `stage_g/g_campaign_gates.parquet`
  (L-G.19); the filed flags are the values of record.
- The same rule, the same pool and the same cuts define the forward ledger's fourth book (L-G.7).
SOURCE: contract :53-54; L-G.1-L-G.5; `T11/stage_g/STAGE_G.md:187-198` (TC11's gate-book table: "v6 minus the union of
the refused sets of the gates on").
RIVALS: intersection (refuse only when BOTH) — not the contract's word. Sequential (apply stale to the OLD-gated
book's re-ride) — a re-ride (L-G.1).
FAILS-IF: F-GATE (L-G.9). Planted mutations: the union replaced by the intersection → `REFUSED-SET`; the un-gated
book (below).

**L-G.7 `pre_seen`, AND "CONFIRMATION = THE LEDGER's FOURTH BOOK"** — "Label pre_seen (TC11 crossed table cell 110
@ +0.515) — verdict disclosed as in-sample; confirmation = the ledger's fourth book (below)" (contract :54-56)
READING:
- **The citation, by file and cell.** The contract's "cell 110 @ +0.515" is the row whose `cell` is
  `age:on|win:on|ratr:off` of TC11's GATE-BOOK table `T11/stage_g/g_grid_books.parquet` (file sha on record
  `b2c786e0…b51b`, certified by TC11's PROGRESS stage TC11-G): its `n` (on file: 110) and its `mean_net_r` (on file:
  +0.514611 — the mean net R per campaign of the gated BOOK; not a difference from v6, not an interval). The same row
  is printed at `T11/stage_g/STAGE_G.md:197` (sha on record `440509bc…0187`) as `age:on¦win:on¦ratr:off`. "110" is
  both the gate pattern (age on, window on, far-stop off) and the kept count. The pin door parses :55 (pin
  `adm.preseen_cell`, two capture groups: regex `cell (\d+) @ \+(\d+\.\d+)`) and the build asserts the first group
  equal to that row's `n` and the second equal to its `mean_net_r` rounded to the token's own number of decimals.
- **What the label says.** P-ADM-1's scored arm IS that book: the same base, the same two refusals, a post-filter.
  Its kept count and mean were printed before this contract was drafted. The row is an IN-SAMPLE RE-SCORE; its new
  information is the interval of the difference from v6 and the beside-prints, nothing else (DISCLOSURES D-4: both
  halves also have filed verdicts). The label key is `pre_seen`, its tag `none`, its label
  `IN-SAMPLE RE-SCORE, NOT CONFIRMATORY` — P-ADM-1's label ALONE among the five rows (O-30: only here is the kept
  book's mean on file) — and the cell is the template L-X.13 fixes for this registration id:
  `<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)`,
  `<clause>` = the label's text up to its first top-level `;`.
- **Two facts that bound what the word can mean, carried in the label's text.** (i) The point estimate of the
  row's own statistic is fixed by filed numbers before scoring: the kept book's mean on file minus the v6 mean on
  file. (ii) This family's bar (q ÷ m with the m of :52) is looser than the bar under which both halves were
  scored on these same campaigns in TC11 (q over TC11's family count, `T11/registrations/REGISTRY_PIN.json` key
  `family_m`). A SUPPORTED here adds an interval to a seen effect and no evidence beyond TC11's.
- **The anchor.** The scored arm must REPRODUCE the cited cell: its key set equals the base keys whose
  `age_old_refused` and `win_refused` are both False in TC11's filed `g_campaign_gates.parquet`; its n equals the
  cell's `n`; its refused count equals the cell's `n_refused` (L-G.9 leg ANCHOR). A scored arm that does not
  reproduce it HALTs the row — the label would otherwise cite a book the row is not.
- **Confirmation.** Nothing in TC12 confirms P-ADM-1. "Confirmation" is defined as the forward ledger's FOURTH
  BOOK, `gated-v6-combined`: v6 with this refusal, frozen by its own spec `T12/forward/BOOK_SPEC_COMBINED.json`
  (filed at `TC12-REG.ledger-spec`, after the registry; L-L; O-24), appended on bars after the ledger's opening,
  unscored until its own n reaches the ledger's floor (contract :110). Its rows of record are those the fourth
  spec's `n_law` fixes (L-L.17): every row appended at TC12's pin entered before the book was frozen, is flagged
  on the row, and is NOT a row of record for confirmation.
- **The gate text of that spec** is the ONE element of this registration's `operative_spec.arms` list that begins
  `` `scored` `` followed by a space (regex `` ^`scored`\s ``; L-L HALTs `FWD-GATE-TEXT` unless exactly one), carried
  verbatim and filed there as `gate.text_of_record` with `gate.text_sha256` beside this registration's payload
  sha. That element therefore holds the WHOLE construction of the scored arm (L-X.18's field grammar): the refusal
  `tide_band == OLD or lag ≥ LAG_CUT`, the pool law and `pool_lo_ms` of L-G.4, the HALT on an unbanded entry, and
  "POST-FILTER; no entry admitted into a freed slot". L-L's fixture holds the two texts equal. The verdict text of
  P-ADM-1 carries the sentence "confirmation, if any, is the forward ledger's fourth book; nothing in this tier
  confirms this row".
SOURCE: contract :15-16, :52, :54-56, :108-110; O-13, O-23, O-24, O-30; `T11/stage_g/g_grid_books.parquet`
[verified here: 8 rows; the cell's `n` 110, `n_refused` 90]; `T11/stage_g/STAGE_G.md:187-198`;
`T11/registrations/REGISTRY_PIN.json` keys `family_m`, `family_bar` [verified here: the bar D-4 quotes as 1/90];
`T12/DISCLOSURES.md` D-4; L-0.27; L-X.13, L-X.18; L-L.2, L-L.3, L-L.17; scout U5 §1.7, §2 item 4.
RIVALS: read "+0.515" as an effect size — it is the book's mean (the partition table holds no such cell). Cite the
partition table — the cell is in the gate-book table. Treat a SUPPORTED word as confirming — forbidden by the label.
Read the gate text from a key `operative_spec.scored_arm` — TC11's key; a TC12 registration has none (L-X.19).
FAILS-IF: `F-GATE [ANCHOR · P-ADM-1]` (L-G.9); L-X's F-REG `[TEMPLATE]` leg (the template by registration id).
Planted mutations: the far-stop gate switched on in a shadow builder (the scored arm becomes another cell) →
`ANCHOR-CELL`; P-ADM-1's template rewritten to the `selection_hazard` form in a copy of the plan → L-X's
`TEMPLATE` RED; a second `arms` element beginning `` `scored` `` planted in a copy of the plan → L-L's
`FWD-GATE-TEXT` HALT.

**L-G.8 THE THREE SHADOWS** — "Shadows printed: OLD alone · stale alone · the absolute-206 cut." (contract :56)
READING: three Tier-E arms of P-ADM-1's regbook — and a fourth for the rival reading below — each a post-filter of
the same base, each collared, none carrying a verdict word (L-0.30's RE-FAMILY leg; D-4). With `base`, `scored`
and `strip` they are the arms of record of `regbooks/P-ADM-1/` (L-X.24), each written through
`tierc12_regbook.write_arm`:

| arm | refused set | TC11's filed arm it must equal |
|---|---|---|
| `tierE__shadow_old_alone` | `A` (L-G.4) | `T11/regbooks/P-AGE-1/scored` |
| `tierE__shadow_stale_alone` | `S` (L-G.5) | `T11/regbooks/P-WIN-1/scored` |
| `tierE__shadow_abs206` | campaigns with `run > ABS_CUT` at the entry bar (strict) | `T11/regbooks/P-AGE-1/tierE__shadow_abs206` |
| `tierE__shadow_abs206_or_stale` | campaigns with `run > ABS_CUT` at the entry bar, or in `S` | none (the rival reading, below) |

- **"Held byte-equal"** = the canonical CSV of the sixteen required columns (L-X.24's `book_sha256` law, TC11's
  SC-13) is byte-identical: the arm's `book_sha256` equals the `book_sha256` in the filed arm's sidecar (`scored.json`
  / `tierE__shadow_abs206.json`, each read through `E.tc11_record`; on file: `d008fa50…22d8`, `fd3f407a…bbfe`,
  `2c1e47ee…d169`), AND the sixteen columns equal the filed parquet's row for row under L-C.8's exact law. Parquet
  FILE bytes are not demanded (stamps name another substrate; TC12's arms carry four more fee columns).
- **`ABS_CUT` is READ BY OBJECT** (X's `abs_tide_cut` law, mirrored): from TC11's P-AGE-1 registration (the
  registry pinned by TC11's chain head and P-AGE-1's payload sha, L-G.5; read through `E.tc11_record`), its
  `text_of_record` matched by `refuse age > (\d+) bars` and its `operative_spec.tier_e_arms` entry matched by
  `^SHADOW absolute: refuse streak > (\d+) bars`; HALT unless both give one integer (on file: 206); asserted equal
  to the contract's token — the pin `adm.abs_cut` (:56, regex `absolute-(\d+) cut`).
- **"The absolute-206 cut" is read as TC11's filed arm**: the absolute cut ALONE. It carries TC11's caveat verbatim
  — the full text of that same `tier_e_arms` entry, read by object and never re-typed (the number is the
  whole-corridor median edge of the pooled streak, not the OLD edge, and it reads the corridor ahead) — in the
  arm's sidecar `description` and wherever the arm is printed. The whole-corridor edges of the TC12 corridor
  (`E.LAB.cuts(lo12, hi12)`, used for nothing else) are printed beside the caveat so a moved median is visible.
- **The rival reading is printed, not chosen:** `tierE__shadow_abs206_or_stale` = base minus (`run > ABS_CUT` ∪ `S`)
  — the combined refusal with the absolute cut in the OLD clause's place. It has no filed twin and is anchored only
  through its flags. It carries the same caveat as the filed arm, verbatim, and the sentence "the OLD clause of
  this arm reads the corridor ahead; only its stale clause is causal".
- **TC11's filed words beside, never re-worded.** Under the two halves the report quotes TC11's own verdict cells
  by JSON path (`T11/scores/SCORES.json` → `rows[registration=P-AGE-1].verdict_cell`,
  `rows[registration=P-WIN-1].verdict_cell`) with TC11's own bar.
- **The TC12 recomputation of each shadow at TC12's seed is the scorer's beside leaf `arm__<slug>`** (L-X.14) —
  `arm__shadow_old_alone`, `arm__shadow_stale_alone`, `arm__shadow_abs206`, `arm__shadow_abs206_or_stale`: the
  two-sample ruler of the arm against this registration's `base` at the seed of record, clusters = the sidecar's
  `panel`; it files `n`, `n_base`, `n_clusters`, `point`, `lo`, `hi`, `n_draws_finite` and `would_read_ci_only`
  and NO p, no bar, no sensitivity seed, no slice, no LOAO and no word — whatever its interval reads at this
  family's bar. Stage G computes no interval of its own.
SOURCE: `T11/regbooks/P-AGE-1/scored.json`, `tierE__shadow_abs206.json`, `T11/regbooks/P-WIN-1/scored.json`,
`T11/regbooks/P-AGE-1/base.json` (the four `book_sha256` values) [verified here]; `T11/registrations/REGISTRATIONS.json`
P-AGE-1 [verified here]; `XR/scripts/tc11x_books.py:347-362`; `scripts/tierc11_stage_g.py:176-178` (`ABS_LABEL`),
`:683-704` (`canonical_csv`, `book_sha256`); `T11/books/BOOKS.md:89`; D-4; L-0.24, L-0.30; L-X.14 (`arm__<slug>`),
L-X.24; scout U5 §1.4, §1.13, §2 items 5 and 7, R-G7.
RIVALS: the absolute shadow as the combined-with-206 book only — would have no filed anchor and is not what TC11's
contract named "the absolute definition"; printed as the fourth arm. The cut recomputed as the extended corridor's
whole-corridor median — a new look-ahead number; printed beside as a disclosure only. A p or a second seed on a
shadow's leaf — not taken: it would read as a test (L-X.14).
FAILS-IF: `F-GATE [ANCHOR · P-ADM-1]` FAILS IF one of the three filed-twin shadows' `book_sha256` differs from its
filed sidecar's, a row differs, the fourth arm's key set is not `base` minus its two flags' union, either abs206
arm's sidecar lacks the caveat (the fourth also its added sentence), or a shadow leaf carries a verdict word.
Planted mutations: the absolute cut made inclusive → `EDGE-ABS` and the `shadow_abs206` sha RED; one refused
campaign re-admitted in a copy of a shadow → its sha RED; the caveat cleared in a copy of the fourth arm's sidecar
→ `ANCHOR-CAVEAT`; `"SUPPORTED"` written into a shadow leaf → L-0's F-COLLAR / F-NOT (RE-FAMILY).

**L-G.9 F-GATE** — "F-GATE (refused set == the text; un-gated book must FAIL)" (contract :117-118)
READING: one fixture, run once per REGISTERED gate of this stage; ONE transcript block per leg and gate, with the
id `F-GATE [<LEG> · P-ADM-1]` or `F-GATE [<LEG> · P-BRD-1]` (L-0.14's block grammar; both instances are REQUIRED
qualifiers of the contract name in L-0.19's roll). P-ADM-1's legs: SET, POSTFILTER, ANCHOR, BOUND, SUBSET.
P-BRD-1's legs: SET, POSTFILTER, BOUND, OVERLAP (L-G.13), SUBSET (SUBSET is L-G.18's, for both). Suite
`scripts/tierc12_stage_g_fixtures.py`, record `TC12-G`, transcript `T12/stage_g/FIXTURES_STAGE_G.txt`. Both gates
are post-filters of the v6 base and carry no precondition: no leg is ever `CLOSED-NO-BOOK`.
- **Leg SET — the refused set recomputed FROM THE TEXT, sharing no code with the builder, and compared.** For
  P-ADM-1 the fixture parses the two cuts itself from the contract prefix (:54: the quantile of "trailing q…",
  the lag cut) and derives, for every base campaign, from the raw 4h tapes read by explicit path under
  `E.SNAPSHOT` and cut at the campaign's entry close: its own EMA loops (the recurrence `prev + alpha·(v − prev)`,
  `alpha = 2/(length + 1)`, seeded at the first value), the state from the warm bar, the run by its own loop, the
  pooled five-asset prefix (`pool_lo_ms ≤ open ≤` the entry open, `run > 0`), the top-quantile edge by its own
  order-statistic interpolation, `OLD* = run ≥ edge`, `lag* = (entry_ms − arm_ms) / MS_4H`, `stale* = lag* ≥
  cut`. `R* = {OLD* or stale*}`. For P-BRD-1 the fixture parses the fraction itself from :58 and `R*` = the base
  campaigns with `y5* · den < num · N`, `y5*` from F-BRD's independent derivation on every entry bar (L-G.14 leg
  ALL). The leg FAILS unless `keys(base) − keys(scored) == R*` and `keys(scored) == keys(base) − R*`, exactly,
  both directions; the counts `n_base`, `n_refused`, `n_scored` are printed.
- **Leg POSTFILTER.** Every scored row equals its base row on every regbook column (exact, L-C.8); no scored key is
  absent from the base.
- **Leg ANCHOR (cross-process, P-ADM-1 only).** On every base key: the builder's facts equal TC11's filed
  `g_campaign_gates.parquet` on `tide_streak_entry`, `tide_left_censored`, `tide_band`, `lag`, the three edges and
  `r_over_atr` at the written rounding, and on TC11's flags `age_old_refused`, `win_refused`,
  `age_abs206_refused`, `ratr_refused` under the typed column map of L-G.19; the scored arm reproduces the
  pre-seen cell (L-G.7); the three filed-twin shadows reproduce TC11's filed arms and the fourth holds its flag
  identity and caveat (L-G.8).
- **Leg BOUND.** The cuts the builder used equal the objects of L-G.3, L-G.5, L-G.8 and L-G.12 (read again by the
  fixture's own regexes from the filed texts and the contract prefix), and the registry pin of L-G.5 holds
  (`REG-PIN`).
- **THE UN-GATED BOOK MUST FAIL** (the contract's plant, on both instances): production's `apply_gate`
  monkeypatched to return the base unchanged → leg SET must go RED naming `REFUSED-SET` ("the book refuses
  nothing; the text refuses k").
SOURCE: contract :117-118; L-0.14; `scripts/tierc11_stage_g_fixtures.py` (F-GATE, F-DEF, F-EDGE as TC11 ran them;
transcript `T11/stage_g/FIXTURES_STAGE_G.txt`, sha `30389af6…79ae`); `engine/indicators.py:17-28`; scout U5 §5.
RIVALS: compare the scored arm with the builder's own flags — self-comparison (banned). Hold only the anchor — it
proves equality with TC11, not with the TEXT.
FAILS-IF: **F-GATE** FAILS IF any leg's condition fails. Planted mutations, inside production, one at a time, each
caught by its named detector: the un-gated book → `REFUSED-SET`; the union replaced by the intersection →
`REFUSED-SET`; the arm-bar age for the entry-bar age → `DEF-AGE`; whole-corridor edges → `DEF-EDGE`; the
one-bar-ahead prefix → `DEF-EDGE`; OLD taken at the middle edge → `DEF-BAND`; the lag cut raised by one →
`EDGE-WIN`; a refused campaign re-admitted → `REFUSED-SET`; a kept campaign dropped → `REFUSED-SET`; a kept row's
`net_r` altered → `POSTFILTER`; the far-stop gate also applied → `ANCHOR-CELL`; a cut (or, for P-BRD-1, the
fraction's numerator) replaced by another value in a shadow builder → leg BOUND RED (`BOUND-CUT`). The plants of
the legs defined elsewhere are stated with them: OVERLAP in L-G.13, SUBSET in L-G.18, the registry pin in L-G.5,
the shadows and their caveat in L-G.8.

---------------------------------------------------------------------------------------------------------------
### C · Breadth (P-BRD-1)

**L-G.10 THE PER-ASSET PER-BAR TIDE-BAND SERIES — BUILT, BECAUSE NO FILE HOLDS IT** — "breadth = share of the five
home assets whose tide band is YOUNG or EARLY" (contract :57-58); "breadth-17 twin" (contract :59); "REGIME COLUMNS:
… breadth · 4h tide age" (contract :102-103)
READING: every filed tide record is per campaign or distributional (scout U5 §1.11); breadth needs every asset's
band at arbitrary bars.
- **The record.** Child `TC12-C.tide` of L-0.10's `SUBSTAGES_T`: BLOCKING; `depends_on` `TC12-ENV`; gated BEFORE
  its parent `TC12-C` in the resume order, with its own commit (`tierc12(TC12-C.tide): …`), its own fixture
  record and its own transcript; required by `TC12-G`, `TC12-S` and `TC12-L`. It needs only the snapshot, the pin
  and the lineage objects of `E` — no book: the builder and its suite import neither `tierc12_books` nor
  `tierc12_stage_g` and read no file under `T12/books/`. Builder `scripts/tierc12_tide.py` (the one writer of
  `T12/tide/`): `tide_bars_4h.parquet`, `breadth_4h.parquet`, `build_manifest.json`, `READ_SET.json`, `TIDE.md`,
  `FIXTURES_TIDE.txt`.
- **Assets.** The seventeen stems of Stage D's manifest in panel order (`E.PANEL17`): the five home assets and
  the twelve. Tapes: `E.load_asof_at(stem, "4h", PIN)` (L-D.28).
- **Grid.** `G` = the 4h opens from `pool_lo_ms` to `E.PIN_MS − MS_4H` in steps of `MS_4H` (generated by
  arithmetic). Every tape's opens must lie on `G` and be gap-free from its first bar to the last grid bar; HALT
  `TIDE-GRID` otherwise.
- **The production law is PURE** (explicit arrays in, arrays out — so the as-of fixture can hand it cut tapes; a
  symbol-keyed memo cannot take one): `tide_series(close, fast, slow, warm)` → `(state, run, start)`, a mirror of X's
  `tide_law` (`XR/scripts/tc11x_era.py:416-437`), with `fast`, `slow`, `warm` = the lineage objects of L-G.2.
- **Edges per grid bar** `g` with open `t`: `numpy.quantile` at `E.LAB.STREAK_BAND_QUANTILES` over the pooled HOME
  prefix — every home-asset bar with `pool_lo_ms ≤ open ≤ t` and `run > 0` — or undefined while that prefix holds
  fewer than `E.R7.PROVISIONAL_MIN_N` bars. One edge triple per grid bar, the SAME for all seventeen assets: the
  banding law of P-ADM-1 (L-G.4), not a per-asset and not a 17-pool law.
- **Per asset-bar** (`tide_bars_4h.parquet`, key `[asset, open_ms]`): `panel`, `i` (own bar index), `close_ms`,
  `state`, `run`, `start_i`, `warm` (`run > 0`), `left_censored` (`start_i == warm floor`), `edge_q25`, `edge_q50`,
  `edge_q75`, `edge_pool_n`, `edges_defined`, `band` (L-G.3's code, null when not warm or edges undefined),
  `ye_face` (banded and YOUNG-or-EARLY), `ye_det` (`ye_face` and not `left_censored`), `undetermined` (`ye_face` and
  `left_censored`), `in_strip` (`close_ms > E.TC11_PIN_MS`).
- **Per grid bar** (`breadth_4h.parquet`, key `[open_ms]`): `close_ms`, the edges, and for the home five and for the
  seventeen: `n_listed`, `n_warm`, `n_undetermined`, `y_det`, `y_face`, `n_eff = n_warm − n_undetermined`, the
  member lists (string columns; no column of this table is named `asset` or `symbol`); and the refusal flags of
  L-G.12 and L-G.15.
- **Held to the lineage, bar for bar (leg ORACLE).** On every home-asset bar, `(state, run, start)` equal
  `E.LAB.tide_streak(sym)`'s arrays exactly; at every grid bar with defined edges, the triple equals
  `E.T9._trailing_edges(POOL, t)["streak_bar"]` exactly (POOL of L-G.4, taken from the lineage object). P-ADM-1
  reads the LINEAGE objects at the entry bar (TC11's law); P-BRD-1 reads THIS series; the oracle leg makes them one
  banding. A difference HALTs.
- **Precision.** Edges, bands and flags are computed at full float; the filed integer and boolean columns are the
  values of record; no consumer re-derives a band from a rounded edge. Every written edge must round-trip
  (`round(edge, nd) == edge`): quantiles of integer runs at the lineage's quartile fractions are exact at the write
  rounding, and the leg says so by assertion rather than by argument.
- Stamps: the pin (the series reads past `W`); `as_of_panel` the seventeen. Collared (Tier-E): the series is data
  for gates and regime columns.
SOURCE: `XR/scripts/tc11x_era.py:416-437` (`tide_law`), `:517-560` (`derive`: the pool with times), `:831-900`
(`bar_cells`: the per-bar RUN / CEN / EDG construction and its grid HALTs) [read here, as text];
`XR/tierc11x/LEANS_X.md:1872-1877` (why X's production is pure and the lineage an equality oracle);
`scripts/tierc7_lab_regime.py:306-349`; `scripts/tierc9.py:1290-1328`; `XR/tierc11x/era/X4_stamps.parquet`
(columns `symbol`, `entry_ms` and the breadth and edge columns of L-G.15) [verified here: names only]; L-0.10
(`SUBSTAGES_T`, the resume order); L-0.14 (the fixture stream; the leg states); scout U5 §1.11, §2 item 15, H2,
H4.
RIVALS: (a) the lineage's memoised functions as production — cannot be handed a cut tape, so the as-of leg could
never reach them (L-0.14). (b) per-asset own-history edges or 17-pool edges for the other assets — X4's twins; a
second banding law inside one family. (c) build it inside Stage G — Stage S (which may run beside G) needs it.
FAILS-IF: **F-TIDE-SERIES** — suite `scripts/tierc12_tide_fixtures.py`, record `TC12-C.tide`, transcript
`T12/tide/FIXTURES_TIDE.txt`, one block per leg (`F-TIDE-SERIES [ORACLE]`, `[ASOF]`, `[GRID]`, `[ROUND]`, `[X]`);
the same suite hosts L-0's helper legs F-KEY [tide], F-DET [tide], F-COLLAR [tide]. It FAILS IF
(ORACLE) any home-asset bar differs from the lineage's arrays or any defined edge triple from `_trailing_edges`;
(ASOF, production against production) the series row at a sampled bar `t`, computed by `tide_series` and the edge
builder from tapes freshly cut at `t`'s close (`E.load_asof_at(stem, "4h", close_ms)` for the asset and for the
five home assets — fresh arrays, never a symbol-keyed memo), differs from the filed row on any column;
(GRID) a tape is off the grid; (ROUND) an edge does not round-trip; (X) on the keys of X's own filed rows —
`(symbol, entry_ms)` of `XR/tierc11x/era/X4_stamps.parquet`, TC11's campaigns, so the leg needs no TC12 book — the
seventeen-asset counts or the edges differ from X's filed stamps (L-G.15).
The ASOF sample is frozen here, per asset of the seventeen: three rule-chosen bars — the asset's first warm bar,
its first bar with defined edges, the last grid bar (coincident choices collapse to one) — plus a seeded draw,
without replacement, of `n = 9` further grid bars of the asset, three in each of tuning / holdout / strip
(`E.era_of(close_ms)`; strip = `in_strip`); a class holding fewer than three bars of an asset contributes all it
has and the transcript prints the shortfall.
Stream: `numpy.random.default_rng([SEED, crc32("tide|F-TIDE-SERIES [ASOF]")])` (L-0.14), drawn asset by asset in
panel order. `n` and the per-class three are fixture-typed literals — the fixture's commission; X filed no count
for a per-bar as-of leg — and are printed in the transcript header.
Planted mutations inside `tide_series` or the edge builder: the run counted from bar 0 → ORACLE; the flip bar
counted as 0 → ORACLE; whole-corridor edges → ASOF; the edge prefix taken to the bar's CLOSE (`open ≤ t + MS_4H`)
→ ASOF and ORACLE; a per-asset pool → ORACLE; one tape with a bar removed → `TIDE-GRID` HALT; an edge perturbed
below the write rounding in a shadow builder → ROUND; one member moved between the warm and the undetermined
count of a seventeen-asset row → X.
UNVERIFIED: that the pure law reproduces `E.LAB.tide_streak` on EVERY bar of the TC12 tapes (X measured it at the 200
entry bars of TC11's tape); leg ORACLE decides it at build and HALTs on a difference.

**L-G.11 BREADTH AT THE ENTRY BAR** — "at the entry bar, breadth = share of the five home assets whose tide band is
YOUNG or EARLY" (contract :57-58)
READING: for a campaign with entry bar open `e` and decision instant `τ = e + MS_4H`:
- **The join is by TIME (O-14, L-0.28).** For each home asset `a` (the campaign's OWN asset included — it is one of
  "the five home assets"): `k_a = asof_index(close_ms_a, τ)` — the last bar of `a` closed at or before `τ`. `k_a =
  −1`: the asset has no closed bar (NOT LISTED). Otherwise `close_ms_a[k_a] == τ` is ASSERTED (the bar read opens at
  `e`); a listed asset whose last closed bar is earlier is HALT `BRD-MISALIGNED` — never a stale read, never an
  index join (the five tapes have different lengths).
- **The edge** is the campaign's own: the trailing triple at open `e` (L-G.4), the same for all five. YOUNG-or-EARLY
  is `run < edges[k_ye]` (L-G.3).
- **Each member is in exactly one class:**

  | class | condition | counts as young |
  |---|---|---|
  | NOT LISTED | `k_a = −1` | no |
  | UNWARM | `run_a[k_a] ≤ 0` (its bar index is below the warm floor) | no |
  | NOT YOUNG | warm and `run ≥ edges[k_ye]` (a left-censored streak here is determined: its age is at least its run) | no |
  | DETERMINED YOUNG | warm, `run < edges[k_ye]`, not left-censored | YES |
  | UNDETERMINED | warm, `run < edges[k_ye]`, left-censored (its age is only bounded below) | no |

  The warm test comes FIRST: an unwarm bar's run is −1 and would pass a naive `run < edge`.
- **`y5`** = the number of DETERMINED YOUNG members, an integer from 0 to `N = len(E.CLASSIC5)`. **The denominator
  is FIXED at `N`**: breadth `= y5 / N`. A missing, unwarm or undetermined asset is in the denominator and not in
  the numerator.
- **Why this reading, of three equally literal ones** (chosen by mechanism and precedent, not by outcome; D-1):
  the contract's fraction is "of the five", so the denominator is five; and the gate's claim is
  that youth is PRESENT in the panel, which an asset with no tide yet, or with a tide of unknown age, does not
  evidence. The rivals are (i) FACE VALUE — an undetermined member counted young because its run is below the edge;
  (ii) the EFFECTIVE DENOMINATOR — X4's law, `y / n_eff` with the gate silent below a floor. The reading taken
  refuses on missing information: its refused set contains each rival's (y can only be lower, and it is never
  silent). It therefore cannot admit a campaign on an age nobody observed, and no early-corridor campaign passes by
  default. Precedents: X4's UNDETERMINED class ("the streak's eventual length is never read",
  `XR/tierc11x/LEANS_X.md:1894-1899`) and the lineage's undefined-counts-AGAINST law
  (`scripts/tierc10_panel.py:1241-1242`). What already-seen figures say about the choice is disclosed two bullets
  below.
- **Who it touches.** Only entries made before all five home tides are warm and determined — the early corridor
  (the per-asset warm floors are printed in `tide/TIDE.md`; the count of such campaigns is printed by the build,
  never typed). Every row prints `n_listed5`, `n_warm5`, `n_undetermined5`, `y5`, `y5_face`, `n_eff5` and the member
  lists, so the three readings can be told apart campaign by campaign.
- **Disclosed, so a reader can judge the choice.** Scout U5 (R-G9, tagged scout-derived) printed the summed outcome
  of the early-coverage campaigns, and X's filed breadth-10 table prints an early-coverage cohort's mean
  (`XR/tierc11x/era/X4.md:1026`); this drafter has seen both, and both are positive. The reading of record can only
  refuse MORE of that cohort than either rival, so the seen figures do not argue FOR it — if anything against. Which
  of those campaigns it actually refuses, and what that does to the row, was not computed. The choice rests on the
  mechanism above; the look is recorded so a reader can see it could not have been used to help the row.
- An entry bar with undefined edges cannot occur in a book (L-G.4's HALT). In the per-bar series such a bar has
  `y = 0` and `edges_defined` False.
SOURCE: contract :57-58; O-14; L-0.28 (`asof_index`); `XR/scripts/tc11x_era.py:684-730` (`_stamp_one`'s member loop:
the alignment HALT, warm at the instant, the censoring rule) [read here, as text]; `XR/tierc11x/LEANS_X.md:1883-1906`
(LX-X4.6); `scripts/tierc7_lab_regime.py:313-318`; `T12/DISCLOSURES.md` D-1; scout U3 C14, R13; scout U5 §2 item 8,
R-G8, R-G9, R-G10, H12.
RIVALS: face value; the effective denominator (both printed as twins, L-G.13); leave-own-out as the reading of
record — the contract says "the five home assets" (printed as a twin); banding each asset on its own history —
L-G.10 rival (b).
FAILS-IF: F-BRD (L-G.14).

**L-G.12 "REFUSE WHEN BREADTH < 2/5" — IN INTEGERS** — "refuse when breadth < 2/5 ["breadth"]" (contract :58)
READING:
- The pin door parses the fraction from :58 — the pin `brd.cut`, two capture groups (regex `breadth <
  (\d+)/(\d+)`; `also` :135, `"breadth" \(<(\d+)/(\d+) refused\)`) — as two integers `(num, den)`. The veto token
  `breadth` is the `veto` field of that pin's row in `pins/PIN_REGISTER.json` (L-0.17, L-0.23).
- `den` must equal `N = len(E.CLASSIC5)` (the contract's own denominator is "the five"); HALT `BRD-DEN` otherwise.
- **A campaign is refused iff `y5 · den < num · N`** — integer arithmetic, no division, no float. With `den == N`
  this is `y5 < num`: refused at the counts below `num`, kept at `num` and above. A campaign AT the cut (`y5 ==
  num`) is kept.
- Refused set `R_BRD` = the base campaigns so refused; scored arm = `base − R_BRD` (L-G.1). Flag `brd_refused` in
  `g_campaign_gates.parquet`.
SOURCE: contract :58, :135; L-0.17 (`fractions`; the `also` law), L-0.23; `XR/scripts/tc11x_era.py:405-407`
(`third_share`: thirds decided in integers because values sit exactly on the cut).
RIVALS: `y5 / N < 0.4` in float — 0.4 is not representable; the comparison at the cut would be decided by rounding.
`≤` — refuses the cut itself.
FAILS-IF: F-EDGE-G: `y5 == num − 1` refused, `y5 == num` kept, for the parsed pair. Planted mutations: the
comparator made inclusive → `EDGE-BRD`; the float form → the AST leg of F-TYPED (a numeric string or literal) and
`EDGE-BRD` on the boundary case; the pin bent at its door (`num + 1`) → L-0's F-TYPED-FLOW must see the refused set
move (the numerator collides with the structural set, L-0.17's stated limit).

**L-G.13 P-BRD-1's LABEL, ITS DISCLOSURE, ITS OVERLAPS AND ITS TWINS** — "Label: direction informed by X4's
composition term (selection hazard)." (contract :58-59)
READING:
- **Label.** Key `selection_hazard`, tag `direction-informed` (lower case — O-30's bytes), label
  `NOT CONFIRMATORY`; the cell is the template L-X.13 fixes for this registration id:
  `<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)`.
  It has no clause slot and it is not P-ADM-1's label: the five-asset breadth was never scored on these campaigns
  before (O-30). Its text names what informed the direction, by file: TC11-X's X4 tables on these same 200
  campaigns — table E-2's composition
  term for the breadth block (`XR/tierc11x/era/X4_tables.parquet`, table `E-2`, block `breadth`, reading `calendar`;
  printed at `XR/tierc11x/era/X4.md:28`) and table E-1's breadth thirds (`X4.md:576 ff.`) — and states three facts a
  reader needs: X4's breadth is over the SEVENTEEN with an effective denominator, not this row's five; X4's own
  sentence for breadth reads UNRESOLVED (`X4.md:16`); and X4 itself prints that breadth is near-collinear with the
  campaign's own tide age (`X4.md:1581`).
- **Disclosure D-1** is carried in the row's `disclosures[]` and printed directly under its cell (L-X.13): a scout
  computed a split of X's seventeen-asset breadth at the contract's cut before these readings were frozen.
- **The key overlap, printed directly under the cell, below D-1 (counts only, no outcome).** D-1 records that the
  OUTCOME of a near-identical gate — the seventeen-asset breadth at this cut — was seen. How much of this row's
  refused set IS that seen cohort is printed where the label is read: the cell COUNTS (`n` alone) of
  `stage_g/g_brd17.parquet` (`brd17` ∈ {`refused`, `kept`, `undefined`} × `brd5` ∈ {`refused`, `kept`}; L-G.15),
  carried into the row's `disclosures[]` with the table's path and sha. No ΣR, no mean, no interval is printed
  there. L-X's F-S0-FIVE is RED when the line is absent. If the refused set is mostly the seen cohort, a reader
  can see that "direction-informed" understates the look.
- **Overlaps, printed on the gate row** (`stage_g/g_gate_rows.parquet`, the row `P-BRD-1`), each as n, ΣR and mean:
  refused ∧ OLD; refused ∧ not OLD; refused ∧ STALE; refused ∧ not STALE; refused ∧ `R_ADM`; refused − `R_ADM` (what
  breadth refuses that the combined refusal does not). Without them the row cannot be told from a second scoring
  of the OLD refusal.
- **Twins**, each a Tier-E arm of P-BRD-1's regbook (post-filters of the same base, collared, no word):
  `tierE__brd_face` (refuse iff `y5_face · den < num · N`); `tierE__brd_neff` (X4's law on the five: defined iff
  edges are defined and `n_eff5 ≥` X's floor, refuse iff `y5 · den < num · n_eff5`; where undefined the campaign is
  KEPT and flagged); `tierE__brd_loo` (the home assets other than the campaign's own: refuse iff `y_loo · den <
  num · (N − 1)`, the denominator fixed at `N − 1`, the same member classes); `tierE__brd17` (L-G.15). With `base`,
  `scored` and `strip` they are the arms of record of `regbooks/P-BRD-1/` (L-X.24), each written through
  `tierc12_regbook.write_arm`. Each twin is ruled by the scorer's beside leaf `arm__<slug>` (L-X.14) —
  `arm__brd_face`, `arm__brd_neff`, `arm__brd_loo`, `arm__brd17`: the two-sample ruler of the arm against this
  registration's `base` at the seed of record; `n`, `n_base`, `n_clusters`, `point`, `lo`, `hi`,
  `n_draws_finite`, `would_read_ci_only`; no p, no bar, no sensitivity seed, no slice, no LOAO, no word. The leaf
  `arm__brd17` carries the note "outcome of this split seen at R0 (D-1)".
SOURCE: contract :58-59; O-23, O-30; OD-16; D-1; L-X.13, L-X.14; `XR/tierc11x/era/X4.md:16`, `:28`, `:576`,
`:1581` [read here: located and checked as citations]; `XR/tierc11x/LEANS_X.md:1900-1906`, `:1959 ff.`
(LX-X4.11); scout U5 §1.10, §2 item 9, R-G11, H9, H10.
RIVALS: the RE-SCORE template of P-ADM-1 — not taken: O-30 (the five-asset breadth was never scored on these
campaigns; the hazard is the direction, and D-1 with the key overlap states the look that did happen). No overlap
prints — H10. The key overlap with its ΣR beside — not taken under the cell: an outcome printed beside a label
reads as a second result; the Tier-E table `G-BRD17` holds it.
FAILS-IF: L-X's F-REG `[TEMPLATE]` leg (its plants: a template rewritten to another registration's form, or the
tag written in capitals, in a copy of the plan → RED);
**`F-GATE [OVERLAP · P-BRD-1]`**: the overlap counts of the gate row and the cell counts of `g_brd17`,
re-derived by the fixture from the filed flags, must equal the filed ones; `n(refused ∧ OLD) + n(refused ∧ not
OLD) == n_refused`; and the `brd5 = refused` cells of `g_brd17` sum to `n_refused`. Planted mutations: one
campaign moved between two overlap cells in a copy of the gate row; one campaign moved between two `g_brd17` cells
in a copy of that table.

**L-G.14 F-BRD** — "F-BRD (breadth recomputed independently on 3 bars)" (contract :118)
READING: suite `scripts/tierc12_stage_g_fixtures.py`, record `TC12-G`; four blocks, `F-BRD [THREE]`, `F-BRD [ALL]`,
`F-BRD [JOIN]`, `F-BRD [ORDER]`. The fixture's own derivation shares no code with `tierc12_tide.py` or
`tierc12_stage_g.py`: the five raw 4h tapes read by explicit path under `E.SNAPSHOT` and cut at `τ`; EMAs by the
fixture's own loops (L-G.9's recurrence); state from the warm bar; run and streak start by its own loop; the
pooled prefix; the three edges by its own order-statistic interpolation; the member classes of L-G.11; `y5`; the
integer test of L-G.12.
- **Leg THREE (the contract's three bars), chosen by a rule frozen HERE, before any book exists** (L-0.14's
  hand-sample law: categories first). Population: the entry bars of the base campaigns, in ascending `(symbol,
  entry_ms)` order.
  K1 = the first campaign whose entry bar has `n_warm5 < N` (not all five home tides warm).
  K2 = the first campaign, not K1, with `n_undetermined5 ≥ 1` (a left-censored member below the edge).
  K3 = the first campaign, not K1 or K2, with `n_warm5 == N`, `n_undetermined5 == 0` and `brd_refused` True.
  The short-population law is L-0.14's, not this section's: a category with no member prints `NONE-EXISTS
  <category>`, asserts from the population that its count is zero, and its slot is taken by the next unchosen
  campaign in the same key order, printed `FILL`; were the population to hold fewer rows than the contract's
  count (:118, "3 bars") all of them would be verified under `ONLY <n> EXIST (contract count 3)`. The leg is
  GREEN in every such case and is never RED or VOID on the size or composition of the population — only on a
  mismatch between the fixture's derivation and production. For each chosen bar the transcript prints, per
  member: its bar's open, run, state, censored flag, class; then the three edges, `y5`, the decision — the
  fixture's values and production's, which must be equal.
- **Leg ALL (cardinality; L-0.14 bans one example where cardinality is possible).** The same derivation on the entry
  bar of EVERY base campaign and every strip entry: `y5`, `n_warm5`, `n_undetermined5` and `brd_refused` equal the
  filed columns.
- **Leg JOIN.** For every campaign, the row of `breadth_4h` it was joined to has `open_ms == entry_ms`; its own
  member's `(run, band)` in the series equals P-ADM-1's facts for that campaign (L-G.4); and the base's key set
  equals the key set of X's filed stamps on which F-TIDE-SERIES leg X ran (L-G.10, L-G.15), so that anchor is an
  anchor of THIS book.
- **Leg ORDER.** On every grid bar: `y5_det ≤ y5_face`, `y5_det ≤ y17_det`, `n_warm5 ≤ n_warm17`, `n_warm5 ≤
  n_listed5 ≤ N`.
SOURCE: contract :118; L-0.14; `XR/tierc11x/LEANS_X.md:2311` (F-ERA: sabotages planted INSIDE the production
function; plants (g), (h)); scout U5 §5 ("incl. one 2020 bar with < 5 warm home assets and one with a censored
member").
RIVALS: three bars chosen by eye — not a rule. Three bars by seed alone — a seeded draw is not bound to include an
early-coverage bar or a censored member, the two rules the reading turns on; the categories bind them in.
FAILS-IF: **F-BRD** FAILS IF any member class, edge, `y5` or decision differs on a chosen bar, on any bar of leg
ALL, or a leg JOIN / ORDER identity fails. Planted mutations inside production, one at a time: each member read at
the bar OPENING at `τ` (one bar ahead) → `BRD-ASOF`; the edge prefix taken as `open ≤ τ` → `BRD-ASOF`; an index
join (each member read at the campaign's own bar index) → `BRD-JOIN`; an unwarm member counted (the warm test
removed) → K1 `BRD-WARM`; the denominator taken as `n_warm5` → K1 `BRD-DEN`; an undetermined member counted → K2
`BRD-CENS`; the own asset left out → `BRD-OWN`; whole-corridor edges → `BRD-EDGE`; the cut made inclusive →
`EDGE-BRD`. On copies of filed tables: a determined-young count written above its face count on one row of
`breadth_4h` → leg ORDER RED (`BRD-ORDER`); one campaign's joined `open_ms` shifted by one bar → leg JOIN RED
(`BRD-JOIN`).

---------------------------------------------------------------------------------------------------------------
### D · The Tier-E tables of Stage G

Every table below is collared (L-0.16), carries `promotable` False and no verdict word, and is DESCRIPTIVE: it
prints `n`, `sum_net_r` (the exactly-rounded sum), `mean_net_r`, `win_pct` (`PCT_PER_UNIT · #(net_r > 0) / n`) and
`nan_reason`, and NO interval (`would_read_ci_only` = "no interval"). Population: the base (scored window) only; no
strip row enters a cell. An empty cell is a row with `n = 0`, NaN statistics and a `nan_reason` (L-0.15). Nothing
found in them is registered or promoted (O-13).

**L-G.15 THE BREADTH GRID, WHOLE; THE BREADTH-17 TWIN** — "Tier-E: the whole breadth {0..5} × own-band grid;
breadth-17 twin." (contract :59)
READING:
- **The grid `G-BRD`** (`stage_g/g_brd_grid.parquet`, key `[cell]`): axes `y5` = the levels `0 … N`, generated
  from `N` (the contract's "{0..5}" is the pin `grid.brd_levels`, :59, parsed by the pin door and asserted equal
  to `(0, N)`) × `own` = the campaign's own band code (L-G.3; the lineage's codes — no unbanded level exists,
  L-G.4). Declared count `(N + 1) · len(codes)`, computed, and equal to the fixture's typed cell list. It
  partitions the base: Σ n == `n.v6`. Cell id `y5:<level>¦own:<code>`. No cell is declared impossible; an empty
  one is printed.
- **The breadth-17 twin** is X4's breadth of record (LX-X4.6), mirrored and transplanted at the contract's cut:
  members = the seventeen; the same edge, the same member classes; UNDETERMINED members leave numerator AND
  denominator; `n_eff17 = n_warm17 − n_undetermined17`; DEFINED iff edges are defined and `n_eff17 ≥ BREADTH_FLOOR`
  (X's constant, read by `ast` from `XR/scripts/tc11x_era.py:164`); refuse iff defined and `y17 · den < num ·
  n_eff17` (integers); an undefined campaign is KEPT and flagged. It is filed as the arm `tierE__brd17` and as the
  table `G-BRD17` (`g_brd17.parquet`, key `[cell]`, cell id `brd17:<refused|kept|undefined>¦brd5:<refused|kept>`):
  `brd17` ∈ {`refused`, `kept`, `undefined`} × `brd5` ∈ {`refused`, `kept`} — the product of the two axes, printed
  whole — the agreement of the twin with the row of record. Its cell COUNTS alone are the key overlap printed
  under P-BRD-1's cell (L-G.13).
- **Anchor (cross-process).** On every key of X's filed `XR/tierc11x/era/X4_stamps.parquet` (`symbol`,
  `entry_ms` — TC11's campaigns, which F-BRD leg JOIN holds equal to the base's keys) the twin's `n_listed17`,
  `n_warm17`, `n_undetermined17`, `n_eff17`, `y17`, the three edges (at the written rounding), `edge_pool_n` and
  the own band equal that file's columns `breadth_n_listed`, `breadth_n_warm`, `breadth_n_undetermined`,
  `breadth_n_eff`, `breadth_young`, `edge_q25` / `edge_q50` / `edge_q75`, `edge_pool_n`, `own_band`. The leg is
  F-TIDE-SERIES `[X]`, run at `TC12-C.tide` on the per-bar series (L-G.10).
- The twin is on a panel chosen ex post (X's own disclosure, carried) and its denominator drifts through the
  corridor; it gates nothing.
SOURCE: contract :59; L-0.15; `XR/tierc11x/LEANS_X.md:1883-1906`; `XR/scripts/tc11x_era.py:164`, `:594-597`,
`:684-760`; `XR/tierc11x/era/X4_stamps.parquet` [verified here: 200 rows; the named columns exist]; D-1; scout U5
§1.10, §2 item 10.
RIVALS: breadth-17 with the denominator fixed at seventeen — most of the twelve are unlisted for most of the
corridor; the twin would refuse nearly everything early and measure listing dates. A grid of breadth SHARES for the
five — the contract prints counts `{0..5}`.
FAILS-IF: L-0's **F-GRID [G-BRD]** (the fixture-typed cell list; Σ n == the base count) and **F-GRID [G-BRD17]**;
`F-TIDE-SERIES [X]` (the anchor); L-0's F-PINS on `grid.brd_levels`. Planted mutations: a dropped cell; an `n =
0` row removed; one campaign moved to no cell; the twin's undetermined members left in the denominator → leg X
RED against X's `breadth_n_eff`.

**L-G.16 THE CROSSED TABLE 2 × 2 × 2 × 2** — "Tier-E: the crossed table 2×2×2×2 (OLD · stale · far stop · low
breadth)" (contract :60)
READING: four bits per base campaign, each a filed flag of `g_campaign_gates.parquet`:

| bit | flag | definition |
|---|---|---|
| OLD | `old_refused` | L-G.4 |
| stale | `stale_refused` | L-G.5 |
| far stop | `farstop` | `r_over_atr > RATR_CUT` (strict), `r_over_atr = r_dist / atr_at_entry` of the Trade object |
| low breadth | `brd_refused` | L-G.12 |

- **`RATR_CUT` is READ BY OBJECT**: the TC12 contract names "far stop" and no number. The cut is TC11's, read from
  P-WIN-1's filed `operative_spec.tier_e_arms` entry (the registry pinned by TC11's chain head and P-WIN-1's
  payload sha, L-G.5; read through `E.tc11_record`) by `r_over_atr > (\d+\.\d+) admission` (exactly one match; on
  file: 2.2), parsed as a `Fraction` and compared as one; its meaning (structural-stop distance over ATR14 of the 4h
  entry bar, railed `≥` one ATR) is TC11's L-G.3.
- **Form (a) — THE PARTITION** `G-X16P` (`g_grid_partition.parquet`, key `[cell]`): the base split by the four
  flags; its cells = the product of four two-level axes, computed (the contract's "2×2×2×2" is the pin
  `grid.x16_shape`, :60, parsed by the pin door and asserted equal to the four axes' cardinalities); Σ n == the
  base count. Cell id `old:<0|1>¦stale:<0|1>¦far:<0|1>¦brd:<0|1>`.
- **Form (b) — THE GATE BOOKS** `G-X16B` (`g_grid_books.parquet`, key `[cell]`): for each on/off setting of four
  gates (`age`, `win`, `ratr`, `brd`), the book = base minus the UNION of the refused sets of the gates ON; one
  row per setting (the same product), each with `n_refused` and `sum_net_r_refused` beside. Cell id
  `age:<off|on>¦win:<off|on>¦ratr:<off|on>¦brd:<off|on>`. The
  `ratr` axis is a HYPOTHETICAL refusal — the contract says far stop is "never a refusal"; the axis is printed
  because this is the filed form the pre-seen cell lives in, and every `ratr:on` row carries the caveat
  "hypothetical: the contract forbids refusing far stops". The row `age:on¦win:on¦ratr:off¦brd:off` is P-ADM-1's
  scored arm and `age:off¦win:off¦ratr:off¦brd:on` is P-BRD-1's, by key.
- **Anchors to TC11's filed 2 × 2 × 2.** The eight rows of form (b) with `brd:off` equal TC11's
  `T11/stage_g/g_grid_books.parquet` rows (`|` in TC11's ids read as `¦`) on `n`, `n_refused`, `mean_net_r`,
  `sum_net_r`, `win_pct`, `sum_net_r_refused` at the written rounding; the partition collapsed over the breadth bit
  (recomputed on the three-flag cells, not summed from rounded cells) equals `g_grid_partition.parquet`'s eight
  rows the same way.
SOURCE: contract :60-62; `T11/stage_g/STAGE_G.md:172-198`; `T11/stage_g/g_grid_books.parquet`,
`g_grid_partition.parquet` [verified here: 8 + 8 rows]; `T11/registrations/REGISTRATIONS.json` P-WIN-1
`operative_spec.tier_e_arms` [verified here]; `scripts/tierc11_stage_g.py:343-348`, `:220` (`GRID_FLAGS`), `:784-792`
(`stats`); `T11/LEANS.md:376-384`; scout U3 C5, R9; scout U5 R-G12.
RIVALS: one form only — TC11 filed both and the pre-seen cell is a gate BOOK while "crossed" names a partition.
Form (b) without the `ratr` axis (eight books) — would not be 2 × 2 × 2 × 2 and would drop the rows that anchor to
TC11's table.
FAILS-IF: L-0's **F-GRID [G-X16P]** and **F-GRID [G-X16B]** (the fixture-typed cell lists; the partition's Σ n);
L-0's F-PINS on `grid.x16_shape`; **F-XGRID-ANCHOR** FAILS IF a `brd:off` row or a collapsed partition row differs
from TC11's filed row. Planted mutations: the far-stop flag made inclusive → `EDGE-RATR` and a `ratr:on` anchor
row RED; a campaign in two partition cells; a gate-book row computed with the intersection.

**L-G.17 FAR-STOP PRIORITY AS SLOT ARBITRATION** — "far-stop PRIORITY simulated as slot arbitration (when two
armings compete for an asset, prefer the farther structural stop; never a refusal — refusing forfeited +21.69R)"
(contract :60-62)
READING:
- **When two armings compete for an asset.** In card v6 an asset holds one position; the replay sorts candidates by
  trigger bar and the first in that order takes the slot. A later candidate whose trigger bar `ti` satisfies `ti ≤
  open_until` is marked `Arming.reject == "position_open"`. That mark IS the competition: an ARBITRATION EVENT is
  one `position_open` rejection of the v6 ride, paired with the campaign holding the slot (the one campaign of that
  asset with `entry_i ≤ ti ≤ exit_i`; TC11's `blocker_of`, mirrored). Two classes, by the pair's bars: (T) SAME BAR
  — `ti == entry_i` of the blocker (both candidates triggered on one bar and the sort decided); (H) HELD SLOT — `ti
  > entry_i` (the blocker was already in).
- **The count is printed FIRST.** `n_events`, split (T) / (H), per book window (scored window; strip), read from the
  v6 ride's rejection log (L-C.2), with the event list (asset, both arm stamps, the trigger bar, each side's
  `r_over_atr` at its own trigger bar, which is farther). On the scored window `n_events` must equal TC11's filed
  `T11/stage_g/build_manifest.json` → `priority.n_position_open_v6` (on file: 0); a difference HALTs (the ride
  would not be TC11's).
- **What the contract's rule does to an event.** Class (T) is fully stated by the contract: of the two candidates,
  the one with the larger `r_over_atr` enters (a tie keeps the lineage's order); nothing is refused. It is
  simulated by the mirror loop of L-G.18 with ONE change — candidates of one asset sharing a trigger bar are ordered
  by descending `r_over_atr` at that bar before the lineage's order — and by nothing else. (Class (T) is defined for
  totality: TC11's filed source states that v6's windows of one asset are disjoint in time — a window ends at the
  counter cross that arms the next, `scripts/tierc11_stage_g.py:70-72` — so a same-bar pair needs two windows open
  at once; the count is printed either way.) Class (H) is NOT stated: preferring the challenger would need a rule
  for the incumbent (an exit the contract does not name), and preferring the incumbent is what v6 already does. For
  class (H) this reading simulates NOTHING: each event is listed with both stops, the mark `preferred_by_text`
  (which side is farther) and `simulated` False.
- **Consequence, stated plainly.** Where `n_events = 0` the simulated book IS the v6 book — an identity, printed as
  one line: "0 arbitration events; far-stop priority as slot arbitration is the v6 book (`TP._book_sha` equal)" —
  and no second set of numbers is printed. On TC11's corridor that is the filed fact
  (`T11/stage_g/STAGE_G.md:205`). No rule is invented to make the twin differ: this is the default O-32 lets
  stand ("an event count and an identity statement … nothing simulated beyond the same-bar ordering rule"), and
  the question goes to the operator (OPEN TO OPERATOR 1).
- **Beside, as cites only:** the forfeit the contract quotes — TC11's gate row for the far-stop REFUSAL
  (`T11/stage_g/g_grid_books.parquet`, cell `age:off|win:off|ratr:on`, columns `n_refused`, `sum_net_r_refused`;
  `STAGE_G.md:62`, `:192`; on file: 53 campaigns, +21.692115 R; the contract's "+21.69R") — and the fact that
  TC11's filed "priority" book (`T11/regbooks/P-WIN-1/tierE__ratr_priority`) preferred the NEARER stop by an
  in-window substitution: the opposite direction and a different mechanism, not this twin's ancestor.
- Table `stage_g/g_arbitration.parquet`, key `[window, symbol, trigger_ms, arm_ms]`, `window` ∈ {`scored`,
  `strip`}, with a placeholder row when empty (TC11's `g_rivals` form). It is an event listing, not a per-trade
  row file: its class in L-L.25 is typed by type (a placeholder row makes a row-derived class unstable).
SOURCE: O-32; `scripts/tierc9.py:388-393` (the slot rule); `scripts/tierc11_stage_g.py:569-606` (`blocker_of`,
`rival_rows`); `T11/stage_g/build_manifest.json` `priority` [verified here: both counts 0];
`T11/stage_g/STAGE_G.md:62`, `:192`, `:200-205`, `:679-685`; `T11/stage_g/FIXTURES_STAGE_G.txt` F-EDGE (the forced
hold: the slot code binds when made to); contract :132 ("no entry-cross research"); scout U3 §1.9, C4, R8; scout U5
§1.8, §2 item 12, R-G13.
RIVALS: (a) an in-window rule that passes a near-stop trigger and waits for a farther one — a pass is a refusal,
the wait needs a later cross: a new entry rule, which contract :132 excludes. (b) a cross-asset cap with the
farther stop preferred — no cap exists on any file. (c) evict the incumbent at the challenger's trigger close — an
exit rule the contract does not state.
FAILS-IF: **F-ARB** FAILS IF the scored-window event count differs from TC11's manifest key; an event in the
rejection log is absent from the table; a table with zero events prints any statistic other than the identity
line; or, under a FORCED HOLD (every campaign's exit delayed by a fixture-typed number of bars inside a shadow ride,
TC11's F-EDGE device), the builder's event count differs from the fixture's own held replay — the proof that a
zero count is a fact of the tape and not a blind detector. Planted mutations: the detector reading `reject ==
"no_trigger"` → the forced-hold leg RED (`ARB-COUNT`); a class (H) event simulated by eviction in a shadow builder →
`ARB-INVENTED`; the identity line printed with a non-zero count → `ARB-IDENTITY`.

**L-G.18 THE GATED BOOKS: STAMPED ONCE, SUBSET BY KEY; THE RE-RIDE DISCLOSURE** — "every funnel instant of every
book (base v6, 9/12, the gated books, every arm below)" (contract :44)
READING:
- **The gated books** of this stage are post-filters of ONE base: OLD-gated (= `tierE__shadow_old_alone`; the
  ledger's third book), combined-gated (= P-ADM-1 `scored`; the fourth), breadth-gated (= P-BRD-1 `scored`), and
  every shadow and twin arm.
- **The strip, for every arm (O-9, OD-14).** On the extended ride the same flags define each book's strip. Each
  regbook's `strip.parquet` holds, under the column `arm`, the extended ride's campaigns with `W < entry_close_ms
  ≤ PIN` that each OTHER arm of that regbook keeps — `base` = all of them, `scored` and every Tier-E arm = those
  its own rule keeps — keyed `(arm, symbol, entry_close_ms)`, with the sidecar's `n_by_arm {arm: n}`. No statistic
  is computed over strip rows anywhere: a count per arm and a pointer are the only aggregates (L-C.10, L-X.14).
- **Stamped once.** The V5 stamps of the v6 instants are filed once, by L-V's reader under `TC12-V.stamps.c`
  (`T12/va/stamps/VA_STAMPS_v6.parquet`, L-C.11). Stage G files `stage_g/g_book_keys.parquet`, key `[book, symbol,
  entry_ms]` — one row per (gated book, kept campaign of the extended ride), with `segment`. "The stamps of gated
  book B" are BY DEFINITION the rows of `VA_STAMPS_v6` whose `(symbol, entry_ms)` is in B's keys — a key join made
  by whoever prints them, never a second table. The subset law is held HERE: `keys(B) ⊆` the key set of
  `books/v6_ext_campaigns.parquet` (the frame the reader stamped) for every B, asserted by the builder on its own
  extended ride and by F-GATE leg SUBSET on the two filed tables. That the stamp table covers every key of that
  frame is L-V's (F-NEST-KEYS and F-NEST-ASOF [v6] at `TC12-V.stamps.c`), so coverage of every gated book follows.
  Nothing is re-stamped; neither the builder nor its suite imports the reader or opens a path under `T12/va/`.
- **The re-ride, a disclosure of counts and diff rows — never an arm (O-21).** For each registered gate, each
  shadow and each twin, the builder also evaluates the refusal on every candidate at its own trigger bar inside
  `tierc12_books.replay_h(sym, lo_ms, hi_ms, *, refuse=None)` (L-C.4) — a mirror of `replay9`'s loop (the
  lineage's own `_ride_leg9`, `_account_chain`, `struct_stop_4h` and `Trade`) with one added statement: when
  `refuse(ctx)` is True the trigger does not take the slot (`ctx` carries TC11's keys: `sym`, `arm`, `ti`, `d`,
  `stp`, `atr`, `r_over_atr`). It returns the trades and a per-window log. With no hook it must reproduce the v6
  book (`TP._book_sha` equal). Filed as COUNTS on the gate row: `rival_count_rejection_log` (the `position_open`
  rejections whose blocking campaign the gate refuses), `reride_n`, `reride_admitted_not_in_v6`,
  `reride_v6_not_taken`, `n_reride_differs`; and the differing campaigns, if any, row by row in
  `stage_g/g_reride_diff.parquet`, key `[gate, window, symbol, entry_ms]`, `window` ∈ {`scored`, `strip`}, with a
  placeholder row per (gate, window) when none. On the scored window these follow from the arbitration count (no
  blocked candidate, no freed slot); on the strip they are re-counted. No re-ride book is an arm; no re-ride row
  gets an interval, a scorer leaf or a V5 stamp. (The same form holds for P-DIR-1's gate, L-R.5: one form for the
  three gates.)
- **`ride_spec` on every mirrored ride.** `stage_g/build_manifest.json` carries, per mirrored ride (the no-hook
  mirror, each hooked re-ride, and the same-bar ordering ride of L-G.17), `ride_spec` (the control card and roles,
  by object — `E.TP.ride_spec(E.TP.CONTROL_CARD, E.T9.V6_ROLES)`) and `roles_name`, so L-0.30's TRAIL-OFFSET, ADDS
  and ENTRY-CROSS legs have an object to read.
SOURCE: L-V.19 (a gated book is a key SUBSET of `v6`: it files a key table and is asserted `⊆`, never
re-stamped); O-9, O-21, O-29; OD-14; `scripts/tierc11_stage_g.py:449-566` (`replay_g`, `refuse_hook`) [read here:
the hook's `ctx` keys]; `T11/stage_g/g_gate_rows.parquet` (TC11's gate-row columns `rival_count_rejection_log`,
`reride_n`, `reride_admitted_not_in_v6`, `reride_v6_not_taken`) [verified here: names only];
`T11/stage_g/STAGE_G.md:54`, `:204`; `XR/tierc11x/LEANS_X.md:2059-2064` (`n_reride_differs`); L-X.24 (the strip's
form); L-0.30; scout U3 R10, R11; scout U5 H16.
RIVALS: a stamp table per gated book — the same rows written several times, each a chance to differ. The re-ride as
the scored arm — L-G.1. The re-ride shipped as a Tier-E arm with an interval — not taken: O-21 calls it a
disclosure, TC11 and X filed counts, and an arm would add a look to every gate. A strip for the registered arms
only — not taken: O-9 names every book and every arm.
FAILS-IF: **`F-GATE [SUBSET · P-ADM-1]`** and **`F-GATE [SUBSET · P-BRD-1]`** FAIL IF a key of a gated book of
that regbook in `g_book_keys` is not a key of `books/v6_ext_campaigns.parquet`; a `strip.parquet` row of an arm
has `entry_close_ms ≤ W`, or is not one of that arm's `g_book_keys` rows with `segment == strip` (for `base`: one
of the `segment == strip` rows of `books/v6_ext_campaigns.parquet`), or `n_by_arm` differs from the fixture's own
count; the no-hook mirror's book sha differs from the v6 book's; a gate-row re-ride
count differs from the fixture's recount of the mirror's log; or a mirrored ride's manifest entry lacks
`ride_spec`. Planted mutations: a key added to a copy of a gated book → SUBSET RED; a scored-window campaign
planted in a copy of `strip.parquet` → `STRIP-EDGE`; the mirror's slot test dropped (it would enter while a
position is open) → the identity leg RED under the forced hold of L-G.17; one `ride_spec` entry removed from a
copy of the manifest → `RIDE-SPEC`.

**L-G.19 WHAT STAGE G FILES; THE FIXTURE ROLL** — "FIXTURES (each states its failure condition)" (contract :114)
READING: record `TC12-G`; `scripts/tierc12_stage_g.py` is the one writer of the three directories below.

**`T12/stage_g/`** — every parquet through L-0.13's `put` (6 dp, nine stamps, collar; none is registered; an
empty frame is skipped and listed, hence the placeholder rows of the two event listings):

| file | declared key | rows |
|---|---|---|
| `g_campaign_gates.parquet` | `[symbol, entry_ms]` | every campaign of the EXTENDED ride with `segment`; the facts of L-G.2-L-G.5, `r_over_atr`, the breadth counts and member lists of L-G.11, every flag of this section (below), both grid cell ids |
| `g_strip_gates.parquet` | `[symbol, entry_ms]` | the strip entries (`W < entry_close_ms ≤ PIN`) with every flag; rows and counts only (L-C.10) |
| `g_book_keys.parquet` | `[book, symbol, entry_ms]` | L-G.18: one row per (gated book, kept campaign of the extended ride), with `segment`; `book` = `<registration id>__<arm>` for `scored` and every `tierE__` arm of the two regbooks |
| `g_gate_rows.parquet` | `[gate]` | one row per registered gate, shadow and twin: TC11's gate-row columns WITHOUT its two re-ride outcome columns (`reride_sum_net_r`, `reride_mean_net_r` are not carried: a re-ride is counts and diff rows, L-G.18), plus `n_reride_differs`, the overlaps of L-G.13, and on P-ADM-1's row the stale-only increment — refused by STALE and not OLD — as n, ΣR and mean, so a higher mean is never printed without its ΣR |
| `g_brd_grid.parquet`, `g_brd17.parquet`, `g_grid_partition.parquet`, `g_grid_books.parquet` | `[cell]` | L-G.15, L-G.16; no column named `asset` or `symbol` |
| `g_arbitration.parquet` | `[window, symbol, trigger_ms, arm_ms]` | L-G.17; a placeholder row when empty |
| `g_reride_diff.parquet` | `[gate, window, symbol, entry_ms]` | L-G.18; a placeholder row per (gate, window) when none |
| `build_manifest.json`, `READ_SET.json`, `STAGE_G.md`, `FIXTURES_STAGE_G.txt` | — | L-0.13's manifest (with `ride_spec` per mirrored ride and `column_notes`) and its open log; the stage document, every grid whole; the transcript |

- **The flag columns of `g_campaign_gates`** and their anchors in TC11's filed table — the map `ANCHOR_COLS_T`,
  typed in the fixture and compared with the builder's: `old_refused` ↔ TC11's `age_old_refused`; `stale_refused`
  ↔ `win_refused`; `age_abs206_refused` ↔ `age_abs206_refused`; `farstop` ↔ `ratr_refused`; the three edges ↔
  `tide_edge_q25` / `_q50` / `_q75`. New in TC12, with no filed twin: `adm_refused`, `abs206_or_stale_refused`,
  `brd_refused`, `brd_face_refused`, `brd_neff_refused` and `brd_neff_defined`, `brd_loo_refused`, `brd17_refused`
  and `brd17_defined`. Each refused set of L-G.6, L-G.8, L-G.12, L-G.13 and L-G.15 is exactly one of these columns.
- **A column note.** `age_abs206_refused` and `abs206_or_stale_refused` carry the note "whole-corridor cut —
  look-ahead on the scored window", filed in the manifest's `column_notes` (TC11's manifest key) and printed in
  `STAGE_G.md` wherever either column or either abs206 arm is printed.
- **Stamps (L-0.13).** A table whose rows all lie in the scored window is stamped with the score edge: the four
  grids, and in the two regbooks every arm but `strip`. Every table that reads past `W` is stamped with the pin:
  `g_campaign_gates`, `g_strip_gates`, `g_book_keys`, `g_gate_rows` (it carries the strip's re-ride counts),
  `g_arbitration`, `g_reride_diff`, and each regbook's `strip`. F-KEY's stamp-truth clause holds both ways
  (plant: a grid stamped with the pin in a copy).
- **The ferry classes** of these tables are typed in L-L.25 from the declared keys above; this section assigns
  none.

**`T12/regbooks/P-ADM-1/`, `T12/regbooks/P-BRD-1/`** — L-X.24's layout: `STATUS.json` (`status` "BUILT",
`preconditions` empty), `build_manifest.json`, and per arm `<arm>.parquet` + `<arm>.json`. The arms of record,
exactly: P-ADM-1 — `base`, `scored`, `strip`, `tierE__shadow_old_alone`, `tierE__shadow_stale_alone`,
`tierE__shadow_abs206`, `tierE__shadow_abs206_or_stale`; P-BRD-1 — `base`, `scored`, `strip`, `tierE__brd_face`,
`tierE__brd_neff`, `tierE__brd_loo`, `tierE__brd17`. Every named arm is written even when it holds no row (the
interface's empty-arm form). Regbook arms are written at FULL FLOAT by `tierc12_regbook.write_arm` (L-0.13's
`put_regbook`: no rounding, key asserted unique, the collar on `strip` and `tierE__` arms only) — the canonical
sha of the `base` arm and of the three filed-twin shadows could not otherwise equal TC11's. Stage G writes no
validator, no canonical-CSV function and no `.to_parquet` of its own: `validate_book`, `book_sha256` and the fee
identities are `tierc12_regbook`'s, filed at `TC12-ENV.score-build`. Every sidecar: `ruler` `two_sample`,
`era_scope` `full`, `panel` = the five home stems, `lens` `4h`, `toll` `taker`, `fill_rule` null; every row's
`lane` is `card`; rows carry L-X.24's twenty columns (on these all-taker arms the four fee columns satisfy its
taker identities exactly, and `funding_r` is the card's own D12-capped funding, as TC11 filed it).

**The roll.** Suite `scripts/tierc12_stage_g_fixtures.py`, record `TC12-G`, transcript
`T12/stage_g/FIXTURES_STAGE_G.txt`; one block per leg (L-0.14). The tide suite is a separate record (L-G.10).

| blocks | FAILS IF | plants |
|---|---|---|
| **F-GATE [`<LEG>` · P-ADM-1]**: SET, POSTFILTER, ANCHOR, BOUND, SUBSET · **F-GATE [`<LEG>` · P-BRD-1]**: SET, POSTFILTER, BOUND, OVERLAP, SUBSET | L-G.9, L-G.13, L-G.18 | L-G.9's; L-G.5's; L-G.8's; L-G.13's; L-G.18's |
| **F-BRD [THREE]**, **[ALL]**, **[JOIN]**, **[ORDER]** | L-G.14 | L-G.14's |
| F-EDGE-G [OLD], [YE], [WIN], [ABS], [BRD], [RATR] | a comparator is not the fixture-typed one at its boundary (L-G.3, L-G.5, L-G.8, L-G.12, L-G.16) | one per comparator: `EDGE-OLD`, `EDGE-YE`, `EDGE-WIN`, `EDGE-ABS`, `EDGE-BRD`, `EDGE-RATR` |
| F-XGRID-ANCHOR | L-G.16 | L-G.16's |
| F-ARB | L-G.17 | L-G.17's |
| F-GRID [G-BRD], [G-BRD17], [G-X16P], [G-X16B] (L-0's helper leg) | L-0.15 | L-0.15's |
| F-TYPED-FLOW (L-0's) on the pins `adm.old_quantile`, `adm.lag_cut`, `adm.abs_cut`, `brd.cut`, and on the read-by-object cuts `LAG_CUT`, `ABS_CUT`, `RATR_CUT`, `pool_lo_ms`, the band quantiles | a bent pin or cut neither moves a refused set, flag or cell nor HALTs the build at the assertion that holds it | each bent at its door, one at a time |
| F-KEY · F-DET · F-COLLAR [stage_g], [regbooks/P-ADM-1], [regbooks/P-BRD-1] (L-0's helper legs) | L-0.21, L-0.20, L-0.16 | theirs |
| F-REGBOOK [P-ADM-1], [P-BRD-1] · F-BASE-IDENT [P-ADM-1], [P-BRD-1] (L-X's helper legs, functions of `tierc12_score_fixtures.py` run here on the two directories) | L-X.24, L-X.25 | theirs |
| F-VA-PINS [e · P-ADM-1], [e · P-BRD-1] (L-V's helper leg, an AST scan of the builder) | the builder reads a value-area column that is not on its registration's declared list — declared for both rows: none, so any such read, a `1w_` column included, is RED | a `4h_state` read planted in a copy of the builder |

SOURCE: `T11/stage_g/` (the file set this mirrors; certified by TC11's PROGRESS stage TC11-G);
`T11/stage_g/g_campaign_gates.parquet`, `g_gate_rows.parquet` (column names) [verified here: names only];
`T11/books/build_manifest.json` (keys `column_notes`, `skipped_empty`) [verified here];
`scripts/tierc11_stage_g.py:180-189` (`REQUIRED`, `SIDECAR_KEYS`), `:1168-1193` (`write_regbook`: full float);
L-0.9, L-0.13, L-0.19; L-X.24, L-X.25; L-L.25; OD-5, OD-14.
RIVALS: none on the roll. A regbook writer or a validator of Stage G's own — not taken: one writer and one
interface for every book stage (OD-5).
FAILS-IF: n/a for the roll (each block's condition and plants are in its own reading). For the files: the helper
legs above; planted mutations — `put` handed a root under `regbooks/` in a shadow builder → F-WARRANTY RED; a
regbook arm written through the rounding writer in a shadow builder → `F-BASE-IDENT [P-ADM-1]` RED (the canonical
sha moves); a named arm absent from a copy of a regbook directory → `F-REGBOOK` RED; the column note cleared in a
copy of the manifest → `F-GATE [ANCHOR · P-ADM-1]` (`ANCHOR-CAVEAT`).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · P-ADM-1

- **id:** P-ADM-1
- **family:** ADMISSION (the family name parsed from the header line, contract :52: "STAGE G · ADMISSION FAMILY
  (m=2, bar 0.05; both two-sample vs v6 — they remove trades):")
- **family_m:** 2 (parsed from contract :52; two registrations stand under the header, :53 and :57)
- **family_bar:** 0.05 (parsed from contract :52; asserted equal, as fractions, to q ÷ m with q = 0.10 parsed from
  contract :9: "bar = 0.10 ÷ m per family")
- **prior:** 50 (contract :53: "P-ADM-1 [50%]")
- **mechanism:** A card-v6 entry is a trend-continuation entry: it buys a pullback inside an established 4h tide.
  Two clocks say independently that such an entry is LATE. The tide clock: the tide it rides has already run long
  measured against every tide run the home panel has shown up to that bar (its age at the entry bar is in the top
  trailing quartile, the OLD band). The window clock: the pullback window that armed the entry has stood open for
  many bars before the trigger came (the arm-to-entry lag is at or above the filed cut). An entry late on either
  clock joins a move with less of its course ahead of it and with the same structural stop behind it. The claim is
  that refusing every entry that is late on at least one clock leaves a book whose per-campaign expectancy exceeds
  the whole book's. The mechanism is declared here and in the contract (:53-54) before this row's interval exists;
  the book's kept count and mean were already printed by TC11, which is what the label says.
- **population:** assets: the five home assets `tierc2_rules.UNIVERSE` (BTC, ETH, SOL, NEAR, ZEC USDT perpetuals,
  contract :18). Lens: 4h. Scored window (O-9): campaigns of card v6 whose ENTRY bar closes at or before TC11's pin,
  read from `research_outputs/tierc11/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms`. Era: the full
  corridor inside that window (the text names no era); the tuning and holdout slices by the entry bar's close are
  Tier-E. The forward strip (entry close after TC11's pin, through TC12's pin) is ridden and printed for every arm
  and is scored by nothing.
- **arms:**
  - `base` — the filed v6 book on the scored window: `tierc10_panel.run_cell_n(CONTROL_CARD, tierc9.V6_ROLES,
    UNIVERSE, lo, hi)` with `(lo, hi) = tierc10_panel.corridor_n(UNIVERSE, pin_close_iso=<TC11's pin>)`, on the TC12
    snapshot (L-C.2). The build HALTs unless its `TP._book_sha` equals `research_outputs/tierc11/books/build_manifest.json`
    key `book_sha.v6`, its n equals that file's `n.v6`, and its regbook `book_sha256` equals
    `research_outputs/tierc11/scores/BASE_IDENT.json` key `book_sha256["P-AGE-1"]`.
  - `scored` (the treated arm) — `base` minus the refused set, a POST-FILTER: the same Trade objects in the base's
    order, keyed (symbol, entry_ms), and no entry admitted into a slot a refusal frees (no re-ride). A base
    campaign is refused iff (i) its tide band at the ENTRY bar is OLD — the two-state tide run
    `tierc7_lab_regime.tide_streak(symbol)[1][entry_i]` (EMA periods `tierc7_rules.TIDE_FAST` and
    `tierc7_rules.TIDE_SLOW`; the flip bar counts as bar 1) is `>=` the top edge of
    `tierc9._trailing_edges(pool, open_ms[entry_i])["streak_bar"]`, the quantiles
    `tierc7_lab_regime.STREAK_BAND_QUANTILES` of the home-panel bar pool `tierc9._trailing_pool(pool_lo_ms, pin − 1)`
    (`pin` = the as-of pin of the ride; the edge at an entry does not depend on it) restricted to bars with open
    `<=` the entry bar's open, defined once that prefix holds `tierc7_rules.PROVISIONAL_MIN_N` bars, `pool_lo_ms`
    read from `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json` key `pool_lo_ms` — OR (ii) its
    window age `entry_i − arm_i` (4h bars) is `>=` the cut read from the text of record of TC11's registration
    P-WIN-1 (`research_outputs/tierc11/registrations/REGISTRATIONS.json`) and asserted equal to the contract's
    (:54). The OR is inclusive: a campaign both OLD and stale is refused once. An entry bar whose trailing edges
    are undefined HALTs — it is never 'not refused'.
  - An entry bar with undefined edges HALTs the build (it is never 'not refused').
  - The scored arm must reproduce TC11's filed cell `age:on|win:on|ratr:off` of
    `research_outputs/tierc11/stage_g/g_grid_books.parquet` (its `n` and `n_refused`, and the key set implied by
    `g_campaign_gates.parquet`); otherwise the build HALTs.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm`; rows
    and counts only.
  - `tierE__shadow_old_alone` — Tier-E: `base` minus the campaigns refused by clause (i) alone.
  - `tierE__shadow_stale_alone` — Tier-E: `base` minus the campaigns refused by clause (ii) alone.
  - `tierE__shadow_abs206` — Tier-E: `base` minus the campaigns whose entry-bar tide run is strictly above the
    absolute cut read from the text of record of TC11's registration P-AGE-1 and asserted equal to the contract's
    (:56); a whole-corridor cut, look-ahead on the scored window.
  - `tierE__shadow_abs206_or_stale` — Tier-E: `base` minus the campaigns above that absolute cut OR refused by
    clause (ii); the OLD clause of this arm reads the corridor ahead; only its stale clause is causal.
  - inputs pinned: HALT-grade pins, not closures (a failed pin prints no number and no word, spends no test and
    blocks CLOSE). `research_outputs/tierc11/books/build_manifest.json` (sha256
    `04f129b7731f700a3cf5eea0775e0a05792e7abd2ec458585feb4768a196bd24`);
    `research_outputs/tierc11/scores/BASE_IDENT.json` (`29f795dcae5c3994f8cc09d742c7480e989f09afe72113b95e2e8859a8ca5581`);
    `research_outputs/tierc11/stage_g/g_grid_books.parquet` (`b2c786e0e7204e1be49c31c0ed7eae7e61365e61ae608dd0efcbe0f4e3b7b51b`);
    `research_outputs/tierc11/stage_g/g_campaign_gates.parquet` (`c5a5f486df5709c0386e8733c9cc2490b1a15e6416b6f5adf45efcae608674d6`)
    — each also the sha TC11's `PROGRESS.json` certifies for it, asserted on every read;
    `research_outputs/tierc11/registrations/REGISTRATIONS.json` by TC11's chain head
    `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9`
    (`research_outputs/tierc11/registrations/REGISTRY_PIN.json` key `head`, recomputed from the payloads) and the
    payload shas of the two registrations read, P-WIN-1
    `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084` and P-AGE-1
    `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879` — never by that file's whole sha, which
    TC12's own close act moves; `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json`
    (`72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`, the sha of its row in
    `research_outputs/tierc12/x_rec/X_REC_MANIFEST.json`); and Stage D's pin, manifest and fee schedule by the shas
    `research_outputs/tierc12/progress/TC12-D.json` certifies.
  - VA columns read (declared for F-VA-PINS (e)): none.
- **statistic:** `mean(net_r of the scored arm) − mean(net_r of the base arm)` — kept versus all, per campaign, in R
  net of the taker toll and funding (the TC-series toll of record).
- **comparison:** two-sample vs v6 (contract :52). The bootstrap of record (O-22; L-X.3, L-X.5, L-X.6): whole-asset
  clusters; `tierc5.cluster_boot_diff(kept values, kept assets, base values, base assets, seed, n_boot)` — one asset
  draw per replicate indexes both arms; N_BOOT draws; the interval is `tierc5._ci_from`'s 5th and 95th percentiles;
  `p = (#draws <= 0 + 1) / (N_BOOT + 1)` as a fraction; the seed of record is the contract's (:4), passed explicitly;
  the sensitivity seed `tierc5.SEED` printed beside.
- **preconditions:** none — the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the
  draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm
  the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints
  'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Printed
  beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices,
  LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block
  twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored.
  Tier-E arms carry no verdict word. For this row q = 0.10 (contract :9), m = 2 and the bar = 0.05 (contract :52),
  N_BOOT = 4000 (`research_outputs/tierc11/scores/SCORES.json` key `n_boot`), the seed of record 20261008 (contract
  :4) and the sensitivity seed 20260816 (the same file's `seed_sens`). The verdict words this row can print are
  exactly two: SUPPORTED (all of (a), (b), (c)) and NOT SUPPORTED (any other outcome of a built row, with the
  qualifier PANEL INCOMPLETE or EMPTY BOOK when (c) fails, TWO-SAMPLE-PREMISE when the gate refuses nothing,
  REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, "CI wholly below zero"
  when the 95th percentile is below zero); CLOSED BY PRECONDITION is unreachable (no precondition); HALT and
  ABSENT are scorer statuses, not verdicts. The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before
  any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the
  number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷
  N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test
  is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). The contract
  pre-names no kill for this row. The row prints
  '<verdict> — IN-SAMPLE RE-SCORE, NOT CONFIRMATORY (pre_seen: <clause>)'.
- **labels:**
  - `pre_seen` — tag: none; label: IN-SAMPLE RE-SCORE, NOT CONFIRMATORY; text: "TC11's crossed gate-book table
    printed this exact book before the contract was drafted — research_outputs/tierc11/stage_g/STAGE_G.md:197, row
    age:on¦win:on¦ratr:off (g_grid_books.parquet cell age:on|win:on|ratr:off), kept n 110 at mean net R +0.5146,
    the contract's 'cell 110 @ +0.515'; the same 200 campaigns, the same two refusals, a post-filter; both halves
    have filed verdicts of their own (P-AGE-1, P-WIN-1; DISCLOSURES D-4); the new information is the interval of
    the difference from v6; the point estimate of this row's statistic is fixed by filed numbers before scoring
    (the kept book's mean on file minus the v6 mean on file); the bar of this family (q ÷ 2) is looser than the bar
    under which both halves were scored on these campaigns in TC11 (q ÷ 9); a SUPPORTED here adds an interval to a
    seen effect and no evidence beyond TC11's; confirmation, if any, is the forward ledger's fourth book — nothing
    in this tier confirms this row"; items: external_context `research_outputs/tierc11/stage_g/STAGE_G.md` lines
    187-198 (sha256 `440509bc8c00bc32b48f745a8f76ca1b6c6d6ddb08f708432790ec164e2d0187`); disclosures: D-4.
- **disclosed_beside:**
  - L-X.14's common beside leaves — `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip` — each Tier-E, no verdict word. On this all-taker row the taker twin is
    the record's own book. The `strip` leaf prints n per arm and one pointer, no statistic.
  - `tierE__shadow_old_alone` — base minus the OLD campaigns; Tier-E, no verdict word; must equal TC11's filed
    `regbooks/P-AGE-1/scored` by `book_sha256`; TC11's own filed verdict cell quoted beside by JSON path with
    TC11's bar; ruled by the beside leaf `arm__shadow_old_alone` (the interval of the arm against `base` at the
    seed of record; `would_read_ci_only`; no p, no bar, no second seed, no slice, no LOAO).
  - `tierE__shadow_stale_alone` — base minus the stale campaigns; Tier-E, no verdict word; must equal TC11's filed
    `regbooks/P-WIN-1/scored` by `book_sha256`; TC11's own filed verdict cell quoted beside by JSON path with
    TC11's bar; ruled by the beside leaf `arm__shadow_stale_alone`, in the same form.
  - `tierE__shadow_abs206` — base minus the campaigns whose entry-bar run is above the absolute cut read from
    P-AGE-1's text of record; Tier-E, no verdict word; must equal TC11's filed `regbooks/P-AGE-1/tierE__shadow_abs206`
    by `book_sha256`; carries TC11's look-ahead caveat; ruled by the beside leaf `arm__shadow_abs206`, in the same
    form.
  - `tierE__shadow_abs206_or_stale` — the rival reading of 'the absolute-206 cut': base minus (above the absolute
    cut OR stale); Tier-E, no verdict word; carries TC11's look-ahead caveat; no filed twin; ruled by the beside
    leaf `arm__shadow_abs206_or_stale`, in the same form.
  - the refusal spread of the row — `refused_n`, `refused_assets`, `p_draw_identically_zero`,
    `n_draws_exact_zero` — count-only, filed before any outcome is read.
  - the refused cohort and the stale-only increment (refused by stale and not OLD): n, ΣR, mean on the gate row;
    Tier-E, no verdict word.
  - the re-ride disclosure — counts on the gate row (`rival_count_rejection_log`, `reride_n`,
    `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`) and the differing campaigns in
    `research_outputs/tierc12/stage_g/g_reride_diff.parquet`; never an arm, no interval; Tier-E, no verdict word.
  - the crossed table 2×2×2×2 (contract :60) in both forms, partition and gate books, and the slot-arbitration
    event count; Tier-E, no verdict word.
  - the five-cluster size footnote, in the verdict text and as the last line under the row.
  - the forward ledger's fourth book `gated-v6-combined` — its spec
    `research_outputs/tierc12/forward/BOOK_SPEC_COMBINED.json` (sha filed at TC12-REG.ledger-spec); every row
    appended at TC12's pin entered before the book was frozen (flagged on the row) and none is a row of record for
    confirmation; `n` appended at TC12's pin, UNSCORED until its own n ≥ n_min; Tier-E, no verdict word; it is the
    contract's 'confirmation' (:55-56) and none of it is scored here.
- **failure_conditions:** F-CTRL (the base is TC11's filed book, trade by trade; RED if any CTRL column differs or
  the book sha is not the filed one — plant: a one-tick stop move). F-BASE-IDENT [P-ADM-1] (RED if the base arm's
  canonical sha is not TC11's, or the scored arm holds a foreign key or an altered kept row — plant: one base
  `net_r` moved by one ulp). F-GATE [SET · P-ADM-1], [POSTFILTER · P-ADM-1], [ANCHOR · P-ADM-1],
  [BOUND · P-ADM-1], [SUBSET · P-ADM-1] (RED if the refused set is not the text's, the scored arm is not a
  post-filter, the pre-seen cell or a shadow is not reproduced, a cut or the registry pin is not the filed object,
  or a gated key or strip row is not the extended book's — plants: the un-gated book, the intersection, the
  arm-bar age, whole-corridor edges, the one-bar-ahead prefix, the lag cut raised by one, a registration body
  altered in a copy of the registry, a key added to a copy of a gated book). F-EDGE-G (RED if a comparator is
  wrong at its boundary — plants: OLD strict, the lag cut strict, the absolute cut inclusive). F-TYPED-FLOW (RED
  if a bent cut moves nothing — plant: each cut bent at its door). F-REGBOOK [P-ADM-1] (RED if an arm breaks the
  regbook interface or the directory's arms are not exactly the named ones — plants: a duplicate key or a row
  past the score edge planted in a copy of the scored arm). F-VA-PINS [e · P-ADM-1] (RED if the builder reads a
  value-area column — plant: a state column read in a copy of the builder). F-KEY and F-DET on `stage_g/` and
  `regbooks/P-ADM-1/` (RED on an undeclared table, a duplicate or null key, a missing stamp, or a rebuild that is
  not hash-identical — plants: a duplicated key row; a table rebuilt in another row order). F-GRID on the two
  crossed grids (RED if the written cells are not the typed list or the partition does not sum to the base —
  plant: a dropped cell). F-BOOT (RED if the persisted draws are not the fixture's own loop, or an arm emptied on
  one asset reads anything but NOT SUPPORTED with PANEL INCOMPLETE — plant: clause (c) removed). F-VERDICT (RED
  if a typed case maps to another word, a gate whose refusals sit on too few assets and lacks its qualifier among
  them — plant: the row scored at another family's bar). F-SCORE-ANCHOR (RED if the mirrored rulers do not
  reproduce TC11's filed leaves on TC11's filed arms at TC11's seed — plant: the base arm replaced by the refused
  cohort).

### REGISTRATION SPEC · P-BRD-1

- **id:** P-BRD-1
- **family:** ADMISSION (the family name parsed from the header line, contract :52: "STAGE G · ADMISSION FAMILY
  (m=2, bar 0.05; both two-sample vs v6 — they remove trades):")
- **family_m:** 2 (parsed from contract :52; two registrations stand under the header, :53 and :57)
- **family_bar:** 0.05 (parsed from contract :52; asserted equal, as fractions, to q ÷ m with q = 0.10 parsed from
  contract :9: "bar = 0.10 ÷ m per family")
- **prior:** 40 (contract :57: "P-BRD-1 [40%]")
- **mechanism:** Breadth asks whether trend regimes are NEW across the home panel at the moment of an entry. When at
  least two of the five home assets are in the first half of a tide run (YOUNG or EARLY by the trailing median of
  all tide runs seen so far), fresh tides are present in the panel and a card-v6 continuation entry rides a regime
  the market is still establishing. When fewer than two are, the panel's tides are mature, old, unformed or of
  unknown age, and a continuation entry is late or isolated. The claim is that refusing entries taken when
  panel-wide youth is absent leaves a book whose per-campaign expectancy exceeds the whole book's. The quantity is
  near-collinear with the campaign's own tide age by construction (the own asset is one of the five and the assets
  co-move), which is why the overlap with the OLD refusal is printed beside the row.
- **population:** assets: the five home assets `tierc2_rules.UNIVERSE` (contract :18), which are both the traded
  panel and the breadth panel. Lens: 4h. Scored window (O-9): campaigns of card v6 whose ENTRY bar closes at or
  before TC11's pin, read from `research_outputs/tierc11/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms`.
  Era: the full corridor inside that window (the text names no era); the tuning and holdout slices are Tier-E. The
  forward strip (entry close after TC11's pin, through TC12's pin) is ridden and printed for every arm and is
  scored by nothing.
- **arms:**
  - `base` — the filed v6 book on the scored window: `tierc10_panel.run_cell_n(CONTROL_CARD, tierc9.V6_ROLES,
    UNIVERSE, lo, hi)` with `(lo, hi) = tierc10_panel.corridor_n(UNIVERSE, pin_close_iso=<TC11's pin>)`, on the TC12
    snapshot (L-C.2) — the one base of the family (O-21), the same book as P-ADM-1's. The build HALTs unless its
    `TP._book_sha` equals `research_outputs/tierc11/books/build_manifest.json` key `book_sha.v6`, its n equals that
    file's `n.v6`, and its regbook `book_sha256` equals `research_outputs/tierc11/scores/BASE_IDENT.json` key
    `book_sha256["P-AGE-1"]`.
  - `scored` (the treated arm) — `base` minus the refused set, a POST-FILTER: the same Trade objects in the base's
    order, keyed (symbol, entry_ms), and no entry admitted into a slot a refusal frees (no re-ride). For a campaign
    with entry bar open `e` and decision instant `e + 4h`: each of the five home assets (the campaign's own
    included) is read at its bar closing at that instant (as-of join by time; a listed asset with no bar closing
    there HALTs); a member is DETERMINED YOUNG iff its tide is warm at that bar, its two-state tide run
    (`tierc7_lab_regime.tide_streak`; EMA periods `tierc7_rules.TIDE_FAST` and `tierc7_rules.TIDE_SLOW`; the flip
    bar counts as bar 1) is strictly below the YOUNG-or-EARLY edge — the edge that closes the bands labelled YOUNG
    and EARLY in `tierc7_lab_regime.STREAK_LABELS`, taken from `tierc9._trailing_edges(pool, e)["streak_bar"]`, the
    same home-panel bar pool, prefix (bars with open `<=` `e`), floor and `pool_lo_ms` as P-ADM-1's banding — and
    its streak is not the left-censored first one; `y5` = the number of determined-young members; the denominator
    is fixed at `N`, the number of home assets (a member not listed, not warm or of undetermined age is in the
    denominator and is not young). The campaign is refused iff `y5 · den < num · N` in integers, with `num/den` the
    contract's fraction (:58, "2/5") and `den` required to equal `N`; a campaign exactly at the cut is kept. An
    entry bar whose trailing edges are undefined HALTs — it is never 'not refused'.
  - An entry bar with undefined edges HALTs the build.
  - `strip` — the extended ride's campaigns with entry close after TC11's pin, per arm under the column `arm`; rows
    and counts only.
  - `tierE__brd_face` — Tier-E: the same rule with a left-censored member below the edge counted young.
  - `tierE__brd_neff` — Tier-E: the effective-denominator rule on the five (X4's law): undetermined members leave
    numerator and denominator; defined iff the edges are defined and the effective count is at least X's breadth
    floor (read from `research_outputs/tierc12/x_rec/scripts/tc11x_era.py`); refused iff defined and `y5 · den <
    num · n_eff5`; an undefined campaign is kept and flagged.
  - `tierE__brd_loo` — Tier-E: the same member classes on the home assets other than the campaign's own, the
    denominator fixed at `N − 1`.
  - `tierE__brd17` — Tier-E: X4's seventeen-asset breadth of record at the contract's cut (effective denominator,
    X's floor; an undefined campaign kept and flagged); the outcome of this split was seen at R0 (DISCLOSURES
    D-1).
  - inputs pinned: HALT-grade pins, not closures (a failed pin prints no number and no word, spends no test and
    blocks CLOSE). `research_outputs/tierc11/books/build_manifest.json` (sha256
    `04f129b7731f700a3cf5eea0775e0a05792e7abd2ec458585feb4768a196bd24`) and
    `research_outputs/tierc11/scores/BASE_IDENT.json` (`29f795dcae5c3994f8cc09d742c7480e989f09afe72113b95e2e8859a8ca5581`)
    — each also the sha TC11's `PROGRESS.json` certifies for it, asserted on every read;
    `research_outputs/tierc12/x_rec/tierc11x/forward/BOOK_SPECS.json`
    (`72a1f52359c66084d22f8bc99b0cd35e7edd89db2751f4859f559c8b1f51cac3`),
    `research_outputs/tierc12/x_rec/tierc11x/era/X4_stamps.parquet` and
    `research_outputs/tierc12/x_rec/scripts/tc11x_era.py` by the shas of their rows in
    `research_outputs/tierc12/x_rec/X_REC_MANIFEST.json`; the tide series
    `research_outputs/tierc12/tide/tide_bars_4h.parquet` and `breadth_4h.parquet` by the shas
    `research_outputs/tierc12/progress/TC12-C.tide.json` certifies; and Stage D's pin, manifest and fee schedule by
    the shas `research_outputs/tierc12/progress/TC12-D.json` certifies. The scored arm reads no cut from TC11's
    registry; the stale flag of the overlaps and the stale and far-stop bits of the crossed table printed beside
    it do (P-WIN-1), and the stage's one builder reads P-AGE-1 for the other row's shadows; so
    `research_outputs/tierc11/registrations/REGISTRATIONS.json` is pinned here too, by TC11's chain head
    `6772568b31fcfb2d56eb8c80b66dedee4fb5082673369e872972df8f475ec8f9`
    (`research_outputs/tierc11/registrations/REGISTRY_PIN.json` key `head`, recomputed from the payloads) and the
    payload shas of P-WIN-1 `d19a42a329be3bfeea73c3c628bf515f5d0fa2fb8facd3fcac795b0186525084` and P-AGE-1
    `e01a89ea7e6fda864f7002a450abd1a4e92424c44d1a9626f6641814e7d35879` — never by that file's whole sha, which
    TC12's own close act moves.
  - VA columns read (declared for F-VA-PINS (e)): none.
- **statistic:** `mean(net_r of the scored arm) − mean(net_r of the base arm)` — kept versus all, per campaign, in R
  net of the taker toll and funding.
- **comparison:** two-sample vs v6 (contract :52). The bootstrap of record (O-22; L-X.3, L-X.5, L-X.6): whole-asset
  clusters; `tierc5.cluster_boot_diff` on one asset draw per replicate; N_BOOT draws; the interval is
  `tierc5._ci_from`'s 5th and 95th percentiles; `p = (#draws <= 0 + 1) / (N_BOOT + 1)` as a fraction; the seed of
  record is the contract's (:4), passed explicitly; the sensitivity seed `tierc5.SEED` printed beside.
- **preconditions:** none — the row has no precondition and cannot read CLOSED BY PRECONDITION
- **verdict_rule:** verdict_of_record = SUPPORTED iff (a) the cluster-90% CI lower bound (the 5th percentile of the
  draws) > 0 AND (b) one-sided p <= q ÷ m, exact, AND (c) every declared asset holds at least one row in every arm
  the ruler reads; else NOT SUPPORTED. m is fixed in every case; a registration closed by its precondition prints
  'CLOSED BY PRECONDITION (…) — no number · no test spent', spends no test and never loosens the bar. Printed
  beside, deciding nothing: the sensitivity seed, the haircut and all-taker twins, the tuning and holdout slices,
  LOAO, both single-trade shares, the literal-bar column, the exact enumeration with SEED-FRAGILE, the month-block
  twin with TIME-CLUSTER FRAGILE, the drop-OPEN twin with VERDICT RESTS ON OPEN MARKS, the forward strip unscored.
  Tier-E arms carry no verdict word. For this row q = 0.10 (contract :9), m = 2 and the bar = 0.05 (contract :52),
  N_BOOT = 4000 (`research_outputs/tierc11/scores/SCORES.json` key `n_boot`), the seed of record 20261008 (contract
  :4) and the sensitivity seed 20260816 (the same file's `seed_sens`). The verdict words this row can print are
  exactly two: SUPPORTED (all of (a), (b), (c)) and NOT SUPPORTED (any other outcome of a built row, with the
  qualifier PANEL INCOMPLETE or EMPTY BOOK when (c) fails, TWO-SAMPLE-PREMISE when the gate refuses nothing,
  REFUSALS ON a/N ASSETS when the refusals sit on too few assets for the ruler to clear, "CI wholly below zero"
  when the 95th percentile is below zero); CLOSED BY PRECONDITION is unreachable (no precondition); HALT and
  ABSENT are scorer statuses, not verdicts. The REFUSALS ON a/N ASSETS qualifier is decided on counts alone, before
  any outcome is read: with a = the number of declared assets holding at least one refused campaign and N the
  number declared, the exact probability that a draw holds no refusing asset and is identically zero is ((N − a) ÷
  N) to the power N; when that is at or above the bar the ruler cannot clear, the word is NOT SUPPORTED, the test
  is spent, and the cell is never cited as evidence against the gate (a = 0 is TWO-SAMPLE-PREMISE). The contract
  pre-names no kill for this row. DISCLOSURES D-1 and the key overlap of the refused set with the seventeen-asset
  twin (counts only) are printed directly under the cell. The row prints
  '<verdict> — NOT CONFIRMATORY (selection_hazard: direction-informed)'.
- **labels:**
  - `selection_hazard` — tag: direction-informed; label: NOT CONFIRMATORY; text: "direction informed by TC11-X's
    X4 breadth tables on these same 200 campaigns — the E-2 composition term of the breadth block and the E-1
    breadth thirds (research_outputs/tierc12/x_rec/tierc11x/era/X4.md:28 and :576 ff.; X4_tables.parquet tables
    E-2 and E-1, block breadth); X4's breadth is a seventeen-asset share with an effective denominator, not this
    row's five-asset count; X4's own sentence for breadth reads UNRESOLVED (X4.md:16); X4 prints that breadth is
    near-collinear with the campaign's own tide age (X4.md:1581); a scout computed a split of that seventeen-asset
    breadth at this cut before the readings were frozen (DISCLOSURES D-1)"; items: external_context
    `research_outputs/tierc12/x_rec/tierc11x/era/X4.md` lines 16 and 28 (sha256
    `aac2be88b8d71f46c232a1976cd5d06dd5ded91b3356976050a48344e9557be8`); disclosures: D-1, printed directly under
    the cell, and under it the cell counts of `research_outputs/tierc12/stage_g/g_brd17.parquet` (the key overlap
    of this row's refused set with the cohort whose outcome D-1 records as seen; counts only, no outcome).
- **disclosed_beside:**
  - L-X.14's common beside leaves — `seed_sens`, `haircut`, `haircut_sens`, `taker_twin`, `taker_twin_haircut`,
    `tuning_slice`, `holdout_slice`, `loao`, `loao_sens`, `concentration`, `share_x`, `literal_bar`, `exact`,
    `month_block`, `drop_open`, `strip` — each Tier-E, no verdict word. On this all-taker row the taker twin is
    the record's own book. The `strip` leaf prints n per arm and one pointer, no statistic.
  - `tierE__brd_face` — the face-value twin (a left-censored member below the edge counted young); Tier-E, no
    verdict word; ruled by the beside leaf `arm__brd_face` (the interval of the arm against `base` at the seed of
    record; `would_read_ci_only`; no p, no bar, no second seed, no slice, no LOAO).
  - `tierE__brd_neff` — the effective-denominator twin on the five (X4's law; undefined campaigns kept and
    flagged); Tier-E, no verdict word; ruled by the beside leaf `arm__brd_neff`, in the same form.
  - `tierE__brd_loo` — the leave-own-out twin (the home assets other than the campaign's own, the denominator
    fixed at their number, `N − 1`); Tier-E, no verdict word; ruled by the beside leaf `arm__brd_loo`, in the same
    form.
  - `tierE__brd17` — the breadth-17 twin (X4's seventeen-asset breadth of record at the contract's cut); Tier-E, no
    verdict word; its counts held equal to X's filed stamps; ruled by the beside leaf `arm__brd17`, in the same
    form, which carries the note 'outcome of this split seen at R0 (D-1)'.
  - the refusal spread of the row — `refused_n`, `refused_assets`, `p_draw_identically_zero`,
    `n_draws_exact_zero` — count-only, filed before any outcome is read.
  - the overlaps of the refused set with OLD, with stale and with the combined refusal: n, ΣR, mean on the gate
    row; Tier-E, no verdict word.
  - the whole breadth {0..5} × own-band grid (contract :59) and the breadth-17 agreement table, each printed
    whole; Tier-E, no verdict word.
  - the crossed table 2×2×2×2 (contract :60) in both forms, partition and gate books; Tier-E, no verdict word.
  - the re-ride disclosure — counts on the gate row (`rival_count_rejection_log`, `reride_n`,
    `reride_admitted_not_in_v6`, `reride_v6_not_taken`, `n_reride_differs`) and the differing campaigns in
    `research_outputs/tierc12/stage_g/g_reride_diff.parquet`; never an arm, no interval; Tier-E, no verdict word.
  - the five-cluster size footnote, in the verdict text and as the last line under the row.
- **failure_conditions:** F-CTRL (the base is TC11's filed book, trade by trade; RED if any CTRL column differs or
  the book sha is not the filed one — plant: a one-tick stop move). F-BASE-IDENT [P-BRD-1] (RED if the base arm's
  canonical sha is not TC11's, or the scored arm holds a foreign key or an altered kept row — plant: one base
  `net_r` moved by one ulp). F-TIDE-SERIES [ORACLE], [ASOF], [GRID], [ROUND], [X] (RED if the per-bar series
  differs from the lineage's arrays, from a fresh cut-tape rebuild, or from X's filed seventeen-asset stamps, a
  tape is off the grid, or an edge does not round-trip — plants: whole-corridor edges, the one-bar-ahead prefix,
  the run counted from bar 0, a tape with a bar removed). F-BRD [THREE], [ALL], [JOIN], [ORDER] (RED if breadth
  recomputed independently differs on the three rule-chosen bars or on any entry bar, or a join or ordering
  identity fails — plants: members read one bar ahead, an index join, an unwarm member counted, the denominator
  taken as the warm count, an undetermined member counted, the own asset left out). F-GATE [SET · P-BRD-1],
  [POSTFILTER · P-BRD-1], [BOUND · P-BRD-1], [OVERLAP · P-BRD-1], [SUBSET · P-BRD-1] (RED if the
  refused set is not `y5 · den < num · N`, the scored arm is not a post-filter, the fraction used is not the
  contract's, an overlap count or a breadth-17 agreement count does not re-derive, or a gated key or strip row is
  not the extended book's — plants: the un-gated book, one campaign moved between two overlap cells, a key added
  to a copy of a gated book). F-EDGE-G (RED if the cut is inclusive — plant: `<=`). F-TYPED-FLOW (RED if the bent
  fraction moves nothing — plant: the numerator bent at the pin door). F-GRID on the breadth grid and the
  breadth-17 table (RED if the written cells are not the typed list or the grid does not sum to the base — plant:
  a dropped cell). F-REGBOOK [P-BRD-1] (RED if an arm breaks the regbook interface or the directory's arms are not
  exactly the named ones — plants: a duplicate key or a row past the score edge planted in a copy of the scored
  arm). F-VA-PINS [e · P-BRD-1] (RED if the builder reads a value-area column — plant: a state column read in a
  copy of the builder). F-KEY and F-DET on `tide/`, `stage_g/` and `regbooks/P-BRD-1/` (RED on an undeclared
  table, a duplicate or null key, a missing stamp, or a rebuild that is not hash-identical — plants: a duplicated
  key row; a table rebuilt in another row order). F-BOOT (RED if the persisted draws are not the fixture's own
  loop, or an arm emptied on one asset reads anything but NOT SUPPORTED with PANEL INCOMPLETE — plant: clause (c)
  removed). F-VERDICT (RED if a typed case maps to another word, a gate whose refusals sit on too few assets and
  lacks its qualifier among them — plant: the row scored at another family's bar). F-SCORE-ANCHOR (RED if the
  mirrored rulers do not reproduce TC11's filed leaves on TC11's filed arms at TC11's seed — plant: the base arm
  replaced by the refused cohort).

### OPEN TO OPERATOR

Each item states the default the build takes if the operator is silent; each is harvested into the report's §9.

1. **Far-stop priority as slot arbitration is an identity on TC11's corridor.** Two armings never compete for an
   asset there (TC11's filed count is zero), so "prefer the farther structural stop" changes no trade and the twin
   is the v6 book. A twin that differs needs a rule the contract does not state: what happens to an incumbent
   position when a farther-stopped arming triggers; or a wait for a farther-stopped later cross; or a cross-asset
   cap. DEFAULT if silent (the default O-32 lets stand): the event count is printed first, the identity is stated
   in one line, same-bar events (if any) are simulated by the ordering rule alone, held-slot events (if the strip
   holds any) are listed and not simulated, TC11's filed forfeit and its nearer-stop "priority" book are cited
   beside, and nothing else is built (L-G.17).
2. **"The absolute-206 cut" shadow.** It can mean the absolute cut alone (TC11's filed arm) or the combined refusal
   with the absolute cut in the OLD clause's place. DEFAULT if silent: the filed arm is the shadow of record (it
   has a filed twin to equal); the other is printed as a fourth arm; both carry TC11's look-ahead caveat (L-G.8).
3. **Breadth before all five home tides are warm and determined.** The contract fixes the cut (veto "breadth") and
   is silent on unlisted, unwarm and left-censored assets. DEFAULT if silent: the denominator stays five and such
   an asset is not young — the reading that refuses on missing information — with the face-value and
   effective-denominator readings printed as twins (L-G.11). The operator may name another reading; after the
   freeze that is an amendment and the row is marked as L-0.23 provides.
4. **The far-stop axis in the gate-book form of the crossed table.** The contract says far stop is "never a
   refusal"; the gate-book form of a 2 × 2 × 2 × 2 table necessarily prints books that refuse far stops. DEFAULT
   if silent: printed as HYPOTHETICAL rows with that caveat, because they are the rows that anchor to TC11's filed
   table; the partition form carries no refusal at all (L-G.16). The operator may strike the `ratr:on` rows.
5. **Two forward boundaries.** Stage C's strip starts after TC11's pin (O-9); the ledger opens at TC10's pin
   (contract :109). DEFAULT if silent: both printed with the column that reconciles them; nothing between the pins
   is scored again (L-C.10).

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

Only what the canon of the review settles is assumed here; nothing below is left "to assembly".

- **L-0 (laws, process).**
  - Records. `TC12-C` (this section's), its child `TC12-C.tide` (this section's; blocking; `depends_on`
    `TC12-ENV`; gated before `TC12-C`) and `TC12-V.stamps.c` (L-V's; `depends_on` `TC12-V`, `TC12-C`) are entries of
    L-0.10's `SUBSTAGES_T` and resume order; `TC12-G` is in its parallel set with `depends_on` `TC12-C`,
    `TC12-C.tide`, `TC12-V.stamps.c`, `TC12-ENV.score-build`. One writer script per parquet directory, one
    manifest and one `READ_SET.json` per directory, one transcript per fixture record (L-0.9).
  - None of `books/*`, `tide/*`, `stage_g/*` is on `REGISTERED_TABLES_T`; all are collared. The registered tables
    this section contributes are the `base` and `scored` arms of the two regbooks (L-X.14).
  - The two writers (settled: L-0.13). Every table of `books/`, `tide/` and `stage_g/` goes through `put` (6 dp;
    an empty frame skipped and listed); every regbook arm through `tierc12_regbook.write_arm`, whose only writer
    is L-0.13's `put_regbook` (full float; a zero-row arm IS written).
  - The wall (settled: L-0.22). `tierc12_va_stamps.py` is the data-only reader and not a door; neither
    `tierc12_books.py` nor `tierc12_stage_g.py` imports it. `tierc12_books`, `tierc12_tide` and `tierc12_stage_g`
    are on `VA_BLIND_T`: none imports the reader nor opens a path under `T12/va/`, proven by AST and from each
    directory's `READ_SET.json`.
  - The pin names this section reads through the pin door (L-0.17), and no other: `ctrl.sum_net_r` (:49);
    `adm.old_quantile` and `adm.lag_cut` (:54); `adm.preseen_cell` (:55, two groups); `adm.abs_cut` (:56);
    `brd.cut` (:58, two groups; also :135; its register row carries the veto token `breadth`);
    `grid.brd_levels` (:59); `grid.x16_shape` (:60); `book.trg912_periods` (:44, two groups). The forfeit figure
    (:62) is a quoted history figure (`CONTRACT_TOKENS_UNPINNED`), printed with its filed source. The count "3
    bars" (:118) is a hand-sample count. The zero print `0.000e+00` (:49, :114) is not a pin of this section:
    F-CTRL passes iff `worst == 0.0` and prints it in the lineage's own format (L-C.6).
  - L-0.15's cell-id separator `¦` is used; TC11's filed parquet ids use `|` (its documents print `¦`), and the
    anchors map one to the other.
  - L-0.14's fixture law is used as written: one `prove` call and one block per leg; block ids `<FID> [<leg> ·
    <instance>]`; the stream `default_rng([SEED, crc32("<suite tag>|<block id>")])`; the one hand-sample law
    (NONE-EXISTS, FILL, `ONLY <n> EXIST`) for F-BRD's three bars; `NOT RUN` never PASS. L-0.19's map hosts the
    F-CTRL family at `TC12-C`, F-TIDE-SERIES at `TC12-C.tide`, and F-GATE, F-BRD and Stage G's other blocks at
    `TC12-G`; `F-CTRL` is the one prefix name.
  - L-0.30's ENTRY-CROSS leg: the 9/12 roles are taken as `SWEEP_CELLS[-1]` and proven against X's filed dict
    without constructing a roles object (L-C.3). Its TRAIL-OFFSET, ADDS and ENTRY-CROSS legs read `ride_spec` and
    `roles_name` from this section's manifests, per ride and per mirrored ride (L-C.1, L-G.18).
- **L-D (substrate, env).** `E` exposes the lineage modules under the referee's aliases named in the abbreviations
  (`E.LAB`, `E.R7`, `E.R6`, `E.R2`, `E.T5`…`E.T9`, `E.TP`, `E.TB`), and the objects `E.CLASSIC5`, `E.PANEL17`
  (re-rooted to TC12's manifest), `E.PIN_MS`, `E.TC11_PIN_MS`, `E.TC11_PIN_ISO`, `E.TC10_PIN_MS`, `E.ERA_CUT_MS`,
  `E.SNAPSHOT`, `E.era_of`, `E.load_asof_at(stem, iv, cut_ms)` (any instant `≤` the pin; fresh arrays),
  `E.ticks()`, `E.fees()` with `taker_bps_side`, `slippage_bps_side`, `slippage_tier` per stem (the regbook's
  haircut column is TC11's expression `net_r − fee_r · slippage_bps_side / taker_bps_side`, ported AST-identical
  with the taker read from `E.fees()`, so the base arm's sixteen columns are bit-equal to TC11's), `E.tc11_record`
  (which accepts TC11's PROGRESS at its R0 sha or at the stamped value, L-0.24), `E.x_rec` and `E.read_set()`.
  F-D-PREFIX and
  F-ENV-ASOF are GREEN before `TC12-C.tide` and `TC12-C`. `TC11_ALLOW_FILE` rows this section needs, all on L-D's
  assembled list: `PROGRESS.json`; `data/AS_OF_PIN.json`; `books/v6_journal.parquet`, `v6_campaigns.parquet`,
  `trg912_journal.parquet`, `trg912_campaigns.parquet`, `build_manifest.json`; `scores/BASE_IDENT.json`,
  `scores/SCORES.json`; `registrations/REGISTRATIONS.json`, `registrations/REGISTRY_PIN.json`;
  `stage_g/g_campaign_gates.parquet`, `g_grid_books.parquet`, `g_grid_partition.parquet`, `build_manifest.json`,
  `STAGE_G.md`; `regbooks/P-AGE-1/{base,scored,tierE__shadow_abs206}` and `regbooks/P-WIN-1/scored` (parquet +
  sidecar). `x_rec` rows: `tierc11x/forward/BOOK_SPECS.json`, `tierc11x/era/X4_stamps.parquet`,
  `tierc11x/era/X4.md`, `scripts/tc11x_books.py`, `scripts/tc11x_era.py`. The two TC11 scripts read as TEXT
  (`scripts/tierc11_books.py`, `tierc11_forward_ledger.py`) are not under a read-never class.
  `research_outputs/tierc10/registrations/P-TRG-2.json` is NOT read (L-C.1). In-scope snapshot reads: the 4h tapes
  of the seventeen and the funding tapes of the five.
- **L-V (value area).** The reader is run by L-V under `TC12-V.stamps.c` over `books/v6_ext_campaigns.parquet` and
  `books/trg912_ext_campaigns.parquet` with the kinds L-C.11 declares (L-V.19's `.c` row) and files
  `T12/va/stamps/VA_STAMPS_v6.parquet` and `VA_STAMPS_trg912.parquet`; F-NEST-KEYS and F-NEST-ASOF [v6], [trg912]
  there hold the stamp tables to those frames and to TC11's nest tables. The gated-subset law for
  `stage_g/g_book_keys.parquet` is held by this section's F-GATE leg SUBSET (the key table does not exist when
  F-NEST-KEYS runs). This section's two registered rows read no value-area column; each spec declares "none" for
  F-VA-PINS [e].
- **L-X (statistics, registrations, close).** The two spec blocks above follow L-X.18's fifteen-field markup and
  its field grammar (the leading token of the checked fields; `preconditions: none — …`; one `arms` element
  beginning `` `scored` ``; `inputs pinned:` and `VA columns read …` sub-bullets; one `labels` sub-bullet per key)
  and carry L-X's common verdict sentence verbatim, followed by the one template L-X.13 fixes for the registration
  id. The scorer derives the common beside leaves, the refusal spread, the size footnote and one `arm__<slug>`
  leaf per `tierE__` arm (L-X.14); this section ships only arms that are other BOOKS (shadows, twins) and computes
  no interval. `external_context` slices are cut from `T11/stage_g/STAGE_G.md` and `XR/tierc11x/era/X4.md` by
  L-X.17's law. The regbook interface — `tierc12_regbook.write_arm`, `write_status`, `write_manifest`,
  `validate_book`, the canonical sha — is L-X.24's, filed at `TC12-ENV.score-build`; the frames carry its twenty
  columns, and on these all-taker arms the four fee columns satisfy its taker identities exactly. F-REGBOOK and
  F-BASE-IDENT real-book instances are helper legs Stage G's suite runs on its two directories.
- **L-R (range-state).** P-DIR-1's base is the same `V6_SCORED` book, built by the same function
  (`tierc12_books.base_regbook_frame()`) and written through the same writer, so the three `base` arms hash to one
  value. The re-ride hook is `tierc12_books.replay_h(…, refuse=<ctx predicate>)` (L-C.4, L-G.18); L-R's predicate
  is an adapter in its own module. The rejection log with reasons is `books/arming_log.parquet`. P-DIR-1's
  re-ride is filed in the same form as this section's (counts and a diff table, no arm). The direction gate is not
  a bit of this section's crossed table.
- **L-S (scalper).** Its regime columns "breadth" and "4h tide age" are read from `T12/tide/breadth_4h.parquet` and
  `tide_bars_4h.parquet` by as-of (close `≤` the instant; L-0.28), as filed; it re-derives no band. The tables are
  keyed on the bar OPEN (`[open_ms]`, `[asset, open_ms]`) and carry `close_ms`; they are `TC12-C.tide`'s, a record
  `TC12-S` depends on, so they exist before `TC12-S` starts.
- **L-L (ledger, era, ferry).** The fourth book's gate text is the ONE element of P-ADM-1's `operative_spec.arms`
  that begins `` `scored` `` (L-G.7; L-L.2's selector) — not a key `operative_spec.scored_arm`, which only TC11's
  payloads carry. P-ADM-1's `disclosed_beside` carries L-L's fourth-book clause; L-L's offered precondition is
  withdrawn (the spec is filed after the registry). The third book is `tierE__shadow_old_alone`'s rule. The
  ledger's admission boundary is TC10's pin; the reconciliation column is `entered_after_tc10_pin`. L-L reads `lag`
  and the eleven tide columns from L-C.4's `campaign_rows`, and its `reride_gated` calls `tierc12_books.replay_h`.
  The ferry classes of `books/*`, `tide/*`, `stage_g/*` and the two regbooks are typed in L-L.25 from the keys
  this section declares (L-C.4, L-G.10, L-G.19).

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None against a ruling. O-7, O-9, O-13, O-14, O-21, O-22 and O-23 were checked against the files this section cites
and none was found wrong on a fact. Section H of the rulings (O-25..O-32) is conformed to: O-29 (the file-only
wall), O-30 (the label bytes), O-31 (the record ids) and O-32 (the far-stop default) are the four that bear on
these two sections.

Two facts recorded so no reader takes them for objections: (i) the unit brief describes the pre-seen cell as a cell
of "TC11's crossed table"; TC11 filed TWO crossed tables and the cell is in the gate-book table, not the partition
(L-G.7). (ii) Scout U5 argues for the fixed-denominator breadth reading from the summed outcome of the campaigns it
affects; that argument is NOT used here (D-1 forbids it). L-G.11 takes the same reading on mechanism and precedent
alone.
