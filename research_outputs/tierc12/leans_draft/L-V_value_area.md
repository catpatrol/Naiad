## L-V · THE VALUE AREA, MODULE-IZED

This section governs Stage V of the contract (lines 25-46) and the six fixtures the contract names for it
(F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-NEST-ASOF; lines 114-121). It fixes: the module
`analytics/value_area.py` and its public API, the two doors that call it and the data-only reader every other
stage uses; the profile law; the lookback per lens (and what the 1w lens gets, for which TC11-X pins nothing); the
causal convention in index terms; the V2 state machine as a transition table, its event records and its equality
target against X's filed events; the per-instant columns; the feasibility mirror; the traverse table that is the
time stop of every range trade; the V5 stamps and the boundary coincidence; the twelve new assets; the volume
null and the Tier-E tables the second door builds; the outputs, the sub-stages and the compute plan. Every range
trade of Stages R and S stands on these readings. L-V owns no registered row. The section conforms to
ORCHESTRATOR_RULINGS O-1..O-32 and to the review dispositions OD-0..OD-19.

**Drafting record.** Read while drafting, all read-only: the contract (sha256 `861d6050…a7bd`), ORCHESTRATOR
RULINGS O-1..O-24 (`c280a972…f509`), DISCLOSURES (`bd6987a2…1958`), scout maps U2 (`50109e8b…3aef`), U3
(`6b95ca28…4148`), U6 (`8315e351…bc4e`); the sibling drafts L-0, L-D and L-X as they stood while this section was
written (their names for shared helpers are used here; where they move, the owning section's name governs); X's
sources and records under `research_outputs/tierc12/x_rec/` (never the X worktree); `analytics/profile.py`,
`engine/indicators.py`, `scripts/tierc10_census.py`, `scripts/tierc11_nest.py`, `scripts/tierc11_stage_r.py` as
text. Inspections were structural: schemas, key
counts, pins, filed verdict words, filed event counts by variant. No outcome of any TC12 book was computed.
While searching for a filed 1w range-life table the drafter also printed TC11's filed 1w pivot verdict row
(`research_outputs/tierc11/stage_r/R2_LENS_VERDICTS.json`, "FAIL (provisional, n<30)"); no reading here uses it.
Counts quoted from X's records or the scout maps are EXPECTATIONS the fixtures read at run time, never inputs.
Revised 2026-10-09 under the LEANS review (`review/LEANS_REVIEW_2026-10-09.json`), the orchestrator's dispositions
(`review/ORCHESTRATOR_DISPOSITIONS.md`, OD-0..OD-19), the reconciler's canon (`review/CROSS_SECTION_CANON.md`) and
section H of the rulings (O-25..O-32). Read while revising, read-only and structural: the X manifest's rows for
the records of L-V.1 (every sha of that table re-read from its row), the schemas of `feasibility.parquet`,
`events_va.parquet` and `va_series_4h.parquet`, the row count per (lens, toll, era) key of the pooled `va_regime`
feasibility rows (one each), and the sample counts of X's and TC11's fixtures as text. No verdict column and no
outcome of any book was read or computed in the revision.

**Notation.** ℓ = a lens. For one asset and lens: bars `t = 0..n−1` with `open_ms[t]`, `o,h,l,c,v`;
`close_ms[t] = open_ms[t] + step_ℓ`. `L_ℓ` = the lookback in bars. `VA(t) = (VAL[t], POC[t], VAH[t])` = the
profile over bars `t−L_ℓ+1 .. t`. `ATR[t]` = ATR_ℓ at bar t. "Top" = the VAH side = ABOVE; "bottom" = the VAL side
= BELOW; `s = +1` top, `−1` bottom. `N` = closes to accept, `M` = the one-close margin in ATR, `K` = the
swing-failure return window, `F` = the coincidence fraction (sources in L-V.4). `E` = the env shim
`scripts/tierc12_env.py` (L-D). ERA_CUT = `E.ERA_CUT_MS` (on file `1719791999000`:
`x_rec/tierc11x/pins/PINS_X.json` key `era_cut_ms`; O-9). `W` = the score edge `E.TC11_PIN_MS` = TC11's pin, which
is also X's (on file `1790294400000`: `research_outputs/tierc11/data/AS_OF_PIN.json` key
`as_of_last_closed_4h_close_ms`; `PINS_X.json` key `as_of_close_ms`). `PIN` = the corridor pin `E.PIN_MS`. `T12` =
`research_outputs/tierc12`. DOOR 1 = `scripts/tierc12_va.py`; DOOR 2 = `scripts/tierc12_va_trades.py`; "the
reader" = `scripts/tierc12_va_stamps.py` (L-V.2). `certified` = `tierc12_progress.certified(rel_path)`, the one
sha-first lookup of a recorded artifact (L-0.4). A fixture leg is cited by its block id, `F-<NAME> [<leg>]`
(L-0.14); a leg is one transcript block.

---------------------------------------------------------------------------------------------------------------
#### A · Source, module, profile, lookback

**L-V.1 SOURCE OF RECORD** — "Source of record = TC11-X's filed implementation (research_outputs/tierc11x/va/,
scripts, shas printed)" (contract :27-28)

READING: The source of record is X's filed X3 implementation, read as BYTES from the R0 copies (O-4) through the
env's sha-first `E.x_rec(rel)`, each read asserted against its row of `x_rec/X_REC_MANIFEST.json` (path + sha256)
before use. The sha column below is each row's value on file at drafting; the build reads the sha from the
manifest row and types none:

| object | path under `research_outputs/tierc12/x_rec/` | sha256 |
|---|---|---|
| implementation | `scripts/tc11x_va.py` | `3f6a43cbbf7fd71cb374bd9e2b2fd16b1cd9bd52b24437a35fb76b9c171ca422` |
| its fixtures | `scripts/tc11x_va_fixtures.py` | `dd941ed23971a8ce590443378fbf7870cb631d86b0ea63028521f224299eee3c` |
| the L reader, the traverse law | `scripts/tc11x_ranges.py` | `26e829d8990b462fc6f22829a9974a5a291fee462dadf58e1160d749dd127d8d` |
| the pins | `tierc11x/pins/PINS_X.json` | `85e1eeea2d04ffe834b93caf76aae55b1f427ae7935b12a7ecae9d814be7498f` |
| X3 manifest (tracked) | `tierc11x/va/build_manifest.json` | `769ac0915ee35b8783d99e0d39870f9e164871b81b94b6bb3533204fa28f078b` |
| X3 stage record (tracked) | `tierc11x/progress/X3.json` | `92b6c49dbc63f737ee421bb0ea53636720f1fd8275d21a0c3d621e1cfd617555` |
| series (untracked at X's tip) | `tierc11x/va/va_series_{1h,4h,12h,1d}.parquet` | `860b8954…af7e` · `d5881508…891c` · `c2ce9a8f…0359` · `1fc7bc75…e1a7` |
| events (untracked) | `tierc11x/va/events_va.parquet` | `2c35b15162a1dfa96fa09074688650dd313fd9245836ccb301cfa2eb3aa35848` |
| feasibility (untracked) | `tierc11x/va/feasibility.parquet` | `ea8573b3240bb1112521c55f0a52ee2ed7156c598b7665685d0b86eefbecb6f0` |
| VA null (untracked) | `tierc11x/null/null_va.parquet` | `a4de5b89868961d207e5ae2515aaaa0678d5b40f976fc2c703a00ea5e3124074` |

"Shas printed" = these rows are written to `va/build_manifest.json` key `x_sources` and to `va/STAGE_V.md`; the
untracked parquets are additionally held equal to `progress/X3.json` → `artifact_shas[<path>].sha256`.
No `tc11x_*` module is imported or executed. X's functions are MIRRORED: pure numerics into
`analytics/value_area.py`, loading, pins and tables into the two door scripts (L-V.2). Each mirrored function
names its X original in its docstring:

| TC12 function | mirrors |
|---|---|
| `value_area.va_series` (+ private `_va_core`, `_bin_right`) | `tc11x_va.py` `va_series` :439-450, `va_windows` :423-436, `va_core` :343-420, `_bin_right` :326-340 |
| `value_area.va_machine` | `tc11x_va.py` `va_episodes` :544-646, `EpLaw` :520-527, `ref_arrays` :535-541 |
| `value_area.va_columns` | `tc11x_va.py` `va_view` :1208-1218; regime age from `regime_units` :968-977 / `adapter_walk` :955 |
| `value_area.va_traverse`, `traverse_pin` | `tc11x_ranges.py` `b_traverses` :787-810, `t_pin` :819-832 |
| `value_area.va_coincidence` | `scripts/tierc11_nest.py` `within` / `coin_flags` :1016-1051 (main tree; read as text) |
| `value_area.null_volume` | `tc11x_va.py` `null_volume` :1130-1169, variant `tr_tercile_lblock` |
| `tierc12_va.load_volume` | `tc11x_va.py` `load_volume` :303-322 |

DOOR 2's mirrors — X's retest scan and outcome statistics, and the gaps+order schedule — are named where they are
defined (L-R.26, L-R.28, L-R.29). Equality with X is held by fixtures on X's FILED records, never by shared code:
F-VA-RAW [c] (series), F-STATE-X (events), F-VA-NULL [a] (draws).

SOURCE: contract :27-28; O-4, O-15, O-25; shas re-hashed while drafting (`shasum -a 256`) and re-read from the
manifest's rows while revising; `x_rec/X_REC_MANIFEST.json` (its sha read through `tierc12_progress.certified`).

RIVALS: (a) import `tc11x_va` from x_rec — not taken: line 101 of that file imports `tc11x_env`, whose guards HALT
off X's snapshot and whose hook arms on import (O-4). (b) a byte copy with the sha in its filename, imported — not
taken: X's own vendor precedent (`tierc11x/vendor/tierc11_env@086d66da.py`) is a referee that is never imported.
(c) rebuild from `analytics.profile` alone and ignore X — not taken: it loses the equality anchor the contract
orders ("X's semantics asserted equal").

FAILS-IF: F-VA-RAW [b], [c] and F-STATE-X [x1]-[x6]; mutation: a one-ulp edge nudge inside `_va_core` (X's own
plant).

**L-V.2 THE MODULE, THE TWO DOORS, THE READER AND THE PUBLIC API** — "analytics/value_area.py; decision modules
import NOTHING from it — import-closure extends to it" (contract :25-26)

READING: The wall is FILE-ONLY (O-29). Four objects and one direction of flow: tapes → the module (inside a
door) → FILED tables → everyone else.
- **The module `analytics/value_area.py`** is pure. It imports `numpy` and `__future__` and nothing else; it
  performs no I/O; it computes no ATR (ATR is handed in as an array, O-15). Every function takes every parameter as
  a REQUIRED KEYWORD argument with no default, and the source holds structural literals only (the integers 0, 1, 2
  and the floats 0.0, 1.0 — the typed-number law of section L-0). Five consequences, stated so the builder has no
  choice to make: a state's code is its index in `STATE_NAMES`; the percent factor is handed in (`pct_per_unit`);
  the null's stratum count is the length of the named tuple `TR_STRATA = ("low", "mid", "high")`; windows are
  processed in blocks of a size handed in (`block`), which changes speed and never a result; the TPO row index is
  corrected until it is stable, with no pass count. The module is not added to `analytics._MODULES`
  (`analytics/__init__.py:118-120`), to `analytics/__init__` or to `analytics/INTERFACE.md`, so
  `analytics.analytics_sha()` stays at the value pinned in `x_rec/tierc11x/va/build_manifest.json` →
  `pins.profile.pins.analytics_sha` (the `analytics/rangefinder_census.py` precedent: in the package, outside the
  hashed recipe).
- **The doors — `DOORS_T = ("tierc12_va", "tierc12_va_trades")`, exactly two (OD-2), typed in the closure
  fixture.** They are the only non-fixture `scripts/tierc12_*.py` modules that import `analytics.value_area` or
  `analytics.profile`; each is EARNED (its source imports `analytics.value_area`); each imports `tierc12_env`
  first and the module after it. A door writes Stage V tables and collared Tier-E tables only: DOOR 1 under
  `T12/va/`, DOOR 2 under `T12/va/trades/`. A door never writes under `regbooks/`, files no order, gate or score,
  files no table holding a column of `TRADE_COLS_T = (net_r, gross_r, fee_r, funding_r, entry_px, stop_px,
  exit_reason)`, and is imported by no module other than `tierc12_va_fixtures.py`.
  - **DOOR 1 `scripts/tierc12_va.py`** (record `TC12-V`): series, TPO twin, ATR, the V2 machine's states and
    events, regimes, the per-bar columns, the nest columns, the traverse legs and pin, `VA_PINS.json`, the mirror
    record, `va_stack`. It takes every frame through `E.D.load_asof(stem, lens)` (the bars closing at or before
    the corridor pin), reads X's records through `E.x_rec(rel)` and TC11's through `E.tc11_record(rel)`, and
    computes ATR.
  - **DOOR 2 `scripts/tierc12_va_trades.py`** (record `TC12-V.trades`): the only place the V2 machine is run on
    permuted volume or on scheduled boxes — (a) the volume null of L-V.23; (b) the gaps+order@va_regime schedule
    and its box events (L-R.29), by `value_area.va_machine` on arrays held constant at each box's edges; (c) the
    Tier-E two-trades tables of L-R.26-L-R.29 (the retest scan, the outcome ledger, the base rate, the lens-above
    partition, the per-draw statistics). It reads Stage V's filed tables through the reader (sha-asserted) and the
    tapes through `E`. **L-R keeps the DEFINITIONS** (L-R.26..L-R.29); this section carries the builder, the files
    and the record (here, L-V.23, L-V.24).
- **The reader `scripts/tierc12_va_stamps.py` is NOT a door.** It is a DECISION module: data-only; it imports
  `tierc12_env`, `tierc12_asof`, `tierc12_tables`, the stdlib-only `tierc12_progress` (for `certified`), pandas
  and numpy; never `analytics.value_area`, `analytics.profile` or a door; it recomputes nothing and contains no
  comparison of a price with a level. Before the first read of any Stage V file in a process it asserts the
  file's sha256 equals `certified(path).sha256`, HALT `STAGE-V-SHA` otherwise. `root=` (an explicit directory
  holding tables and a `build_manifest.json`) may be passed by `_fixtures` modules and by DOOR-side twins only
  (AST); the sha is then asserted against that manifest. Its API, complete:

  | function | returns |
  |---|---|
  | `bars(lens, *, asof_close_ms=None, root=None)` | `va_bars_<lens>` sorted `[asset, close_ms]`; with `asof_close_ms`, the rows with `close_ms ≤` it |
  | `events(*, lens=None, kind=None, asof_close_ms=None, root=None)` | `va_events` rows; with `asof_close_ms`, the rows with `known_close_ms ≤` it |
  | `regimes(*, asof_close_ms, lens=None, root=None)` | `va_regimes` rows with `r0_close_ms ≤ asof_close_ms`; for a regime alive at that instant `die_i`, `die_close_ms`, `end_side`, `end_by`, `n_bars` are null and `alive_at_asof` is True. `asof_close_ms` is REQUIRED: no unbounded form exists |
  | `instants_of(frame, kind)` | `[book, symbol] + kind.key + [instant_kind, instant_ms]` (L-V.19) |
  | `stamp(instants, *, root=None)` | the instants joined, per lens, to row `k = asof_index(close_ms_ℓ, instant_ms)` of `va_bars_<ℓ>`, as filed, with `stale_ms` and the gap guard of L-V.21 (L-V.20) |
  | `licence(lens, toll, era)` | the `VA_MIRROR.json` leaf `licence["<lens>|<toll>"].by_era[<era>]`; HALT for a pair outside `licence_set`; each call is appended to the process's `licence_reads`, written into the directory's `READ_SET.json` (L-V.17 item 9) |
  | `traverse(name)` | `(value, source)`: `name ∈ {"traverse.1h", "traverse.4h", "traverse.12h", "traverse.1d", "traverse.1h.in_5m_bars"}`; `value` = the int at `TRAVERSE.json by_lens.<lens>.T_of_record` (or `by_lens.1h.T_in_5m_bars`); `source = {path, key, sha256, value}` for the book manifest's `time_stop_source`. **This is "the fitted-pin door"** (L-V.18) |
  | CLI `--file-stamps --stage=TC12-V.stamps.<c|r|s>` | files the instant stamps of one stamps child (L-V.19) |

- **Every other `scripts/tierc12_*.py` is a DECISION module, with no exemption** — the P-SFP-VA-1, P-SCALP-3 and
  take-profit builders, the books, the gates and the scorer included. Where it may receive value-area facts at all
  (the members of L-0.22's `VA_BLIND_T` receive none), it receives them only as FILED DATA through the reader,
  never by a call into the module or a door, and it carries no copy of the V2 machine, of a profile, or of an
  acceptance / swing-failure / lapse test. A consumer may compare a price with a filed LEVEL; it never re-derives
  a lens STATE or EVENT.
- **Where the code is filed.** `analytics/value_area.py`, the two doors, the reader and the two suites
  (`scripts/tierc12_va_fixtures.py`, `scripts/tierc12_va_stamps_fixtures.py`) are artifacts of the record
  `TC12-V`; the children of L-V.24 run that code and file tables, records and transcripts, never a changed
  script. The reason is the wall's own proof: the closure suite runs at ORDER-stage gates (L-0.9), so both doors
  and the reader must stand before it at the `TC12-V` gate — DOOR 2 before it has run once — and no child gate
  would see a script filed later. `tierc12_va_fixtures.py` is the only `_fixtures` module that may import the
  module or a door (`VA_MODULE_FIXTURES_T`, L-0.22); the stamps suite imports neither.

The module's public API, complete:

```
STATE_NAMES = ("UNDEFINED", "INSIDE", "PROBING_ABOVE", "PROBING_BELOW", "ACCEPTED_ABOVE", "ACCEPTED_BELOW")
TR_STRATA   = ("low", "mid", "high")

va_series(*, high, low, volume, lookback, bins, value_area, mode, block) -> dict[str, ndarray]
    # mode "volume" | "tpo".  float64 arrays of length n: poc, val, vah, val_edge, vah_edge, window_lo, window_hi
va_machine(*, close, high, low, atr, val, vah, accept_n, margin_atr, ret_k) -> dict
    # margin_atr None disables the one-close clause — the mirror legs of F-STATE-X only
    # per-bar arrays (length n): state int8, armed_top bool, armed_bottom bool, probe_side int8 (0 none, +1, -1),
    #   probe_t0 int64 (-1), probe_edge float64 (NaN), regime_r0 int64 (-1), last_accept_i int64 (-1)
    # "events": list of dicts (L-V.14) · "regimes": list of {rid, r0, die_i, start_kind} · "counters": dict
va_columns(*, close, atr, val, vah, poc, machine, pct_per_unit) -> dict[str, ndarray]
    # per bar: pct, edge_dist_atr, near_side, d_vah_atr, d_val_atr, poc_dist_atr, va_age, accept_age (L-V.16),
    #   inside_frozen_only bool (L-V.13 (i))
va_traverse(*, high, low, val, vah, regimes, state) -> dict    # "legs": per-leg rows (L-V.18); state counts n_probe_bars
traverse_pin(*, values) -> dict                # n, lower_hinge, median, upper_hinge, T = ceil(median), integer law
va_coincidence(*, vah_l, val_l, atr_l, vah_u, val_u, frac) -> dict   # L-V.21
null_volume(*, volume, true_range, lookback, rng) -> tuple[ndarray, dict]   # L-V.23; rng is built by DOOR 2
```

The as-of index is not in the module: it is `tierc12_asof.asof_index` (section L-0), one implementation for every
cross-lens join in TC12.

SOURCE: contract :25-26, :124; O-15, O-29, O-31; OD-2, OD-7; the sibling readings L-0.17 (no typed number; the
structural set; "its functions take every parameter as a required keyword argument with no default"), L-0.22 (the
class law: `DOORS_T`, decision modules with no exemption, `VA_BLIND_T`, `VA_MODULE_FIXTURES_T`, the exit check,
the analytics wall: the module imports `numpy` and `__future__` only), L-0.4 (`tierc12_progress.certified`: the
last record that names a path governs it) and L-0.28 (`asof_index`); L-D.26 (hunk 7: the shim's VA-wall exit
check; hunk 10: `load_asof_at`, `x_rec`, `tc11_record`); `tests/test_analytics.py:118-161` (F-AN-3: no line
matching `^\s*(from|import)\s+engine\b` in the RAW source, docstrings included; F-AN-4: no `read_parquet`,
`requests`, `urllib`, `os.environ`, `socket` token and no `open(` call); `analytics/rangefinder_census.py:132-133`
("the ATR itself is handed in"); scout U2 §1.12, U3 §1.2.

RIVALS: (a) register the module in `_MODULES` — not taken: it moves `analytics_sha()` for every consumer and X's
F-PROFILE-PIN. (b) a law object built with `dataclasses`, or defaults on law parameters — not taken: the wall admits
`numpy` and `__future__` only, and a default is a typed constant. (c) a range or scalper builder importing a door
for arrays — forbidden: O-29 (a module that imports a door reaches the module transitively). (d) a second door for
the stamps — not taken: the vector at an instant is a join of filed rows (L-V.20) and needs no module call. (e) the
two-trades tables in a decision module with a mirrored box machine — not taken: OD-2. (f) a door spawned in a
cut-tape mode by a later stage's suite — not taken: OD-2 (no suite outside Stage V imports or spawns a door; the
later suites cut the FILED tables and lean on F-VA-ASOF [d]).

FAILS-IF: owned by L-0 — F-WALL (the module's imports and I/O), F-TYPED (literals, defaults), F-CLOSURE [i], [i-b],
[ii], [iii] (each door EARNED and typed; a fresh interpreter importing the reader or any other decision module
holds no `analytics.value_area`, no `analytics.profile` and no door; the exit check finds neither in any process
whose entry script is not a door or `tierc12_va_fixtures.py`). Owned here — F-VA-RAW [b] (two block sizes give
byte-equal series) and F-NEST-ASOF plant P7 (the reader's sha law). Mutations: a copy of the reader importing a
door → F-CLOSURE RED; a door copy without its `analytics.value_area` import → UNEARNED; a third module importing
`analytics.value_area` that is not typed in `DOORS_T` → RED; a DOOR 2 copy writing under `regbooks/` → RED; a
`net_r` column added to a copy of a door table → RED; a block size that changes a level → F-VA-RAW [b] RED; one
cell changed in a copy of a filed table under an unchanged manifest → the reader HALTs `STAGE-V-SHA`.

**L-V.3 THE PROFILE LAW** — "Value area = the contiguous band around the POC holding 70% of volume-at-price over
the trailing lookback" (contract :29-30)

READING: VA(t) is the house recipe `analytics.profile.volume_profile(high, low, volume, bins, value_area)`
(`analytics/profile.py:113-172`) applied to the slice `t−L_ℓ+1 .. t` of the lens's OWN tape, computed by the
mirrored vectorised path and held BIT-EXACT to the house function. Clause by clause:

- **Bins.** `bins = analytics.profile.PROFILE_ROWS` (`profile.py:21`; value on file 120), read by object and
  asserted equal to `x_rec/tierc11x/va/build_manifest.json` → `pins.profile.bins`. Range-relative:
  `edges = linspace(min low, max high, bins + 1)` of the window (`profile.py:126, 132`); reproduced as
  `arange(bins + 1)·((hi − lo)/bins) + lo` with the last edge set to `hi` (`tc11x_va.py:355-362`).
- **Spread.** Each bar's volume is spread uniformly over its `[low, high]`: per bin, the bin's overlap with the
  bar's range ÷ the sum of overlaps (`profile.py:145-148`). A doji (`high == low`) puts all its volume in bin
  `min(int((a − lo)/(hi − lo)·bins), bins − 1)` (`profile.py:142-144`). Accumulation is bar by bar in window order.
- **Skipped bars.** A bar with a non-finite high, low or volume, or with `volume <= 0`, contributes nothing
  (`profile.py:137-140`). It still occupies one of the L slots: the window is a bar COUNT.
- **POC.** `argmax(hist)` — the FIRST maximum, so a tie goes to the LOWEST price bin (`profile.py:154`).
- **The 70% band.** `value_area = analytics.profile.VALUE_AREA` (`profile.py:22`; value on file 0.70), by object,
  asserted equal to the contract's "70%" (:29) and to `pins.profile.value_area`. Start at the POC bin; while the
  accumulated volume `< value_area × total` and a side remains, compare the next bin up with the next bin down
  (`−1.0` at a boundary); `up >= down` → extend UP, else DOWN (`profile.py:155-166`): one bin per step, **an
  expansion tie goes UP**, the band is contiguous by construction.
- **Levels are bin CENTRES.** POC, VAH, VAL = `(edges[i] + edges[i+1])/2` of the POC bin, the top included bin and
  the bottom included bin (`profile.py:133, 168-170`). The outer bin EDGES (`val_edge`, `vah_edge`, half a bin
  wider each side; `tc11x_va.py:415-416`) are filed beside and used by nothing.
- **Degenerate windows.** `hi <= lo` → POC = `lo`, VAL = VAH = NaN (`profile.py:127-130`). Zero total volume in the
  window → POC = VAL = VAH = NaN (`profile.py:150-152`). A NaN profile makes the bars it would judge UNDEFINED
  (L-V.13); the build counts such windows per cell and HALTs if one occurs after warm-up on a home-asset tape of a
  licensed lens (1h, 4h, 1d).
- **Warm-up.** `VA(t) = NaN` for `t < L_ℓ − 1`; the first profile is `VA(L_ℓ − 1)` (`tc11x_va.py:439-450`).
- **Gaps.** A missing bar is never filled; L counts bars, so a gap stretches the window in clock time
  (`tierc10_census.py:580-582`). Gap counts per tape are printed.
- **Single-bin band.** If the POC bin alone holds ≥ 70%, `VAL == VAH == POC`; the machine still runs (closed
  interval), `pct` is NaN (L-V.16), and the count is printed.

SOURCE: `analytics/profile.py` (sha `1c0a7519ddd4c37963163e1dc302788d142c74f741a82d8022742595a8eb3e18`) lines as
cited; `tc11x_va.py:343-450`; `x_rec/tierc11x/LEANS_X.md` LX-X3.2..X3.4 (:1608-1647); O-15. Each door imports
`analytics.profile` only after the three pins hold (file sha, `analytics_sha()`, `ANALYTICS_VERSION`), each read
from `x_rec/tierc11x/va/build_manifest.json` → `pins.profile.pins` (X's F-PROFILE-PIN law, `tc11x_va.py:118-149`).

RIVALS: 100 rows (the function default) — X's twin, not carried. Bin edges as levels — X's twin, filed, unused.
ATR-scaled or tick rows — rejected by X (LEANS_X :1640). `windowed_profile` (day windows by bar OPEN, finer
substrate, `profile.py:175-225`) — a different object. A finer-substrate build of the coarse lenses (X's
house-substrate twin) — not carried.

FAILS-IF: F-VA-RAW [a], [b]; mutations: the volume column shifted one bar; every interior edge nudged one ulp.

**L-V.4 THE LOOKBACK PER LENS AND THE LAW CONSTANTS** — "Lookback per lens = X's pin, read from its records and
FROZEN here as bars, decoupled from the pivot detector ["va-lookback"]" (contract :28-29)

READING: For ℓ ∈ {1h, 4h, 12h, 1d}: `L_ℓ = int(PINS_X["L"]["by_lens"][ℓ]["L_of_record"])`, read from
`x_rec/tierc11x/pins/PINS_X.json` (values on file at drafting: 71 / 66 / 53 / 35 — an orientation, never an input).
DOOR 1 writes them ONCE to `T12/va/VA_PINS.json` (`by_lens.<ℓ>` = `{L_bars, source {path, key, sha256}, label,
source_lens}`) BEFORE any series is built; every later read is from `VA_PINS.json` by object, asserted equal to
`PINS_X.json`. "Frozen as bars, decoupled": no pivot-machine run ever re-derives L in TC12; L is an integer bar
count and nothing else. The label X filed travels on every VA row (`l_label`): "a tuning-window L is in-sample for
tuning-era VA bars (the L-R.2 label)" (`PINS_X.json` → `L.by_lens.<ℓ>.label`). X's twins (whole-tape, frozen-3.0,
per-asset L) are not carried.
**The pin register rows** (names of record, L-0.17): the lookbacks are `va.lookback.<lens>` for ℓ ∈ {1h, 4h, 12h,
1d, 1w}, kind `x_record`, door = X's record, value in `VA_PINS.json by_lens.<lens>.L_bars`, each carrying
`veto: "va-lookback"` (the 1w row with `source_lens: 1d`, L-V.5). Every other constant of this section, with its
register row, the source a DOOR reads at run time, what it is asserted equal to, and — for the register's flow leg
— what must move when the pin is bent at its door (the value column is the value on file at drafting):

| constant | register row · kind | read at run time from | asserted equal to | value on file | witness when bent |
|---|---|---|---|---|---|
| `L_ℓ` | `va.lookback.<ℓ>` · x_record · veto `va-lookback` | `PINS_X.json` `L.by_lens.<ℓ>.L_of_record` (X's record) | `va/build_manifest.json` `pins.L.<ℓ>.record`; the `L` column of X's `va_series_<ℓ>` | 71 / 66 / 53 / 35 | `VA(t)` on the sampled windows of F-VA-PINS [c] |
| N (closes to accept) | `va.accept_n` · contract | contract :35, through the contract pin door | the AST literal `PINS["BREAK_CONFIRM_N"]` of `analytics/rangefinder_census.py` (:141; file sha `19c5507f…b37d`); X's `pins.laws.break_confirm_n` | 8 | the bar of F-STATE's A1 |
| M (one-close margin, ATR) | `va.accept_margin_atr` · contract | contract :35, pin door | `PINS["BREAK_MARGIN"]` (:144); `pins.laws.break_margin` | 1.5 | F-STATE's A2 and A3 |
| K (return window) | `va.sfp_k` · contract · veto `sfp-k` | contract :36, pin door, with :135 `"sfp-k" (3)` as its second citation | a member of `pins.laws.sfp_k_twins` | 3 | F-STATE's N1 |
| F (coincidence, ATR) | `va.nest_frac` · contract · veto `nest` | contract :45, pin door, with :135 `"nest" (0.25 ATR)` as its second citation | `pins.laws.coincidence_atr`; the AST literal `COIN_FRAC` of `scripts/tierc11_nest.py` (:108) | 0.25 | the nest flags on the sampled bars of F-VA-PINS [c] |
| value_area | `va.value_area_pct` · contract | `analytics.profile.VALUE_AREA` (the lineage object a door reads) | contract :29 "70%" (the pin door asserts the two equal); `pins.profile.value_area` | 0.70 | `VA(t)` on the sampled windows |
| bins | lineage | `analytics.profile.PROFILE_ROWS` (a lineage object, read by a door) | `pins.profile.bins` | 120 | `VA(t)` on the sampled windows |
| ATR length | lineage | `E.R2.ATR_LEN` (`scripts/tierc2_rules.py:121`) | the AST literal `ATR_LEN` of `analytics/rangefinder_census.py` (:132) | 14 | `ATR[t]` on the sampled bars |
| floor n | lineage | `E.R5.PROVISIONAL_MIN_N` (`scripts/tierc5_rules.py:232`) | `pins.laws.floor_n` | 30 | the traverse HALT |
| null draws (DOOR 2) | x_record | X's `pins.laws.k_draws` | the AST literal `K_DEFAULT` of `scripts/tierc10_null.py` (:109) | 20 | the number of draws filed per cell (F-VA-NULL [c]) |
| X's record return window (mirror legs only) | x_record | X's `pins.laws.dev_return_bars` | `PINS["DEV_RETURN_BARS"]` (:140) | 7 | F-STATE-X [x1] |
| percent factor | units | `PCT_PER_UNIT` of `scripts/tierc12_units.py`, handed to the module | — | 100 | — |

This section's other register rows are `va.mirror_words` (:39-40) and `va.licence_set` (:41), both contract pins
of L-V.17, and the fitted pins `traverse.<lens>` and `traverse.1h.in_5m_bars` of L-V.18. A veto of "va-lookback",
"sfp-k" or "nest" changes the first source's value by a dated amendment naming the operator's quote (L-0.23),
demotes Stage V and every range row, and rebuilds them; nothing else changes.

SOURCE: contract :28-29, :35-36, :45, :135; O-15; `PINS_X.json` keys as cited (`L.law`: "one L per lens — the
CLASSIC5 pooled, dead-weighted mean of DIED confirmed-range lives (die_i − confirm_i) on the tuning-era head at
each asset's pick of record, L = floor(x + 0.5)"); `tc11x_ranges.py` `lookback` :1355-1362; three concordant
sources of L verified while drafting (`PINS_X.json`, `va/build_manifest.json` `pins.L.<ℓ>.record`, X3.md :31-34);
`va/build_manifest.json` `pins.laws` and `pins.profile` read while drafting; the sibling readings L-0.17 (the pin
map, the register with its `kind`, `consumers`, `witness` and `veto` fields, the flow leg) and L-0.23 (the veto
map); L-D.26 (the shim's lineage aliases `E.R2`, `E.R5`).

RIVALS: type 71/66/53/35 — forbidden. Re-derive L by running the pivot machine — contradicts "decoupled". Carry
X's L twins — three more value areas per lens with no contract phrase behind them. Read N and M from the range
machine by import — puts `analytics.rangefinder_census` in a door's process for two numbers the contract states.

FAILS-IF: F-VA-PINS [a], [b], [c], [d]; L-0's F-TYPED on the doors and the module, and F-VETO on the register rows
above. Mutations: a typed lookback in a copy of DOOR 1 → F-TYPED RED; one L moved by one in a copy of
`PINS_X.json` → F-VA-PINS [a] RED; `pins.laws.break_margin` changed in a copy of X's manifest → [b] RED; a door
copy that ignores the handed K and uses its own copy of it → [c] `PIN-NOT-READ`.

**L-V.5 THE 1w LOOKBACK** — "the VA vector at 1h, 4h, 12h, 1d, 1w" (contract :44-45); "Lookback per lens = X's
pin" (:28); "Q4 accept 1w FAIL (provisional) as closing 1w for range trading ["1w"]" (:14)

READING: X pins no 1w lookback (`PINS_X.json` → `L.by_lens` has exactly the keys 12h, 1d, 1h, 4h;
`tc11x_ranges.py:356` `L_LENSES = ("1h", "4h", "12h", "1d")`). X's lookback LAW cannot be applied at 1w from any
filed record, for four facts verified while drafting:
1. No per-range life table covers 1w: `x_rec/tierc11x/pins/life_ranges.parquet` holds lenses 1h/4h/12h/1d only;
   TC11's `stage_r4/R4_DEATHS.parquet`, `R4_NULL_BOXES.parquet`, `R4_EVENTS.parquet` hold 1h/4h/12h/1d only; TC10's
   `census/coverage.parquet` holds 5m/4h/1d only.
2. The only filed 1w range facts are `research_outputs/tierc11/ranges/SCALE_GRID.parquet` (sha `9072aeab…6919`):
   per-asset `mean_confirmed_lifetime` rounded to 1 dp with NO died-range count. X's law is a pooled DEAD-WEIGHTED
   mean (`tc11x_ranges.py` `l_pin` :835-846); X itself ruled the grid insufficient for it (`PINS_X.json` →
   `decision.L.grid_has_died_count: false`, `landing_class: "ABSENT"`).
3. X's law runs on the TUNING-ERA head at a tuning pick. At 1w no tuning pick exists: all five 1w cells are
   `pick_window = "whole-tape (fallback)"`, `tuning_pick` null, labelled IN-SAMPLE (`ranges/SCALE_PICKS.json`
   `fallback_cells`; the 55 1w grid rows all carry `window == "whole"`).
4. The tuning era holds 7 confirmed 1w ranges over the five assets at those picks (`stage_r/R1_LENSES.parquet`,
   `n_confirmed_tuning` 3/1/1/1/1), under the floor of 30.

The reading of record, settled by O-28, is the labelled fallback: **`L_1w := L_1d`, the 1d pin's bar count, read
from `PINS_X["L"]["by_lens"]["1d"]["L_of_record"]`**, written to `VA_PINS.json` as `by_lens.1w` with
`label = "BORROWED: the 1d pin's bar count; X pinned no 1w lookback; not X's law at 1w"` and `source_lens = "1d"`.
The 1w value area is built on the derived weekly tape (L-V.7), runs the same machine, and is a Tier-E column
block read in exactly two places (O-28): the V5 stamp columns and the lens-above axis of the 1d two-trades tables.
- **The two reads, exactly.** (R1) the `1w_*` block the reader files in `va/stamps/VA_STAMPS_<book>.parquet`
  (L-V.19, L-V.20); (R2) the lens-above conditioning axis of the 1d rows of the two-trades tables (L-R.27), built
  by DOOR 2 from the reader's stamp at the event's known-at close τ — row `k = asof_index(close_ms_1w, τ)` of
  `va_bars_1w`: the last COMPLETE Monday-anchored derived week whose close ≤ τ (a week still forming is never
  read; on a Monday 00:00Z close the week closing at τ IS read, O-14). DOOR 2 reads these five columns and no
  other: `1w_state`, `1w_val`, `1w_vah`, `1w_pct`, `1w_bar_close_ms`; every 1d row of the tables that carry the
  lens-above cell carries `u_lookback_label = "BORROWED: the 1d pin's bar count; X pins no 1w lookback"` (4h rows:
  the empty string).
- **Read by nothing else.** No gate, no permission, no direction guard, no licence, no time stop, no order and no
  registered construction reads a `1w_` column. No 1w range cell, trade, traverse row or feasibility row exists.
  The typed pair of readers is L-0.25's `ONEW_READERS_T` = ((`scripts/tierc12_va_stamps.py`,
  `va/stamps/VA_STAMPS_*.parquet`), (`scripts/tierc12_va_trades.py`, `va/trades/TWO_TRADES_*.parquet`)); F-NOT's
  leg 1W (L-0.30) and F-VA-PINS [e] prove it.
Printed beside in `STAGE_V.md`, as the mechanism disclosure: the five filed 1w per-asset mean lives at TC11's
picks (`SCALE_GRID.parquet`, whole-tape, 1 dp, read through `E.tc11_record`) — every one of them is shorter than
the borrowed count.

Why the borrow and not NA: (i) the contract orders a 1w block twice (:44-45, and the lens above 1d at :76-79,
which has no other object at 1d); (ii) TC11's L-R.2 is the filed precedent for this very lens — where the law of
record cannot be fitted for lack of tuning bars it applies a LABELLED fallback and carries the label on every row
(`research_outputs/tierc11/LEANS.md:179-181`), it does not print NA; (iii) the borrowed quantity is a filed X pin
in the law's own unit (bars of the lens), tuning-fit, so it carries no holdout information; (iv) neither reading
can move a verdict — no registered row reads 1w — so the cannot-flatter test does not separate them.

SOURCE: files and keys as cited; O-11 as amended by O-28, O-14, O-15; OD-3; contract :14, :44-45, :76-79, :137;
the sibling readings L-0.25 (the two reads; `ONEW_READERS_T`) and L-R.27 (the partition); scout U2 §1.2, R2.

RIVALS: (a) 1w columns NA with the reason — the stricter reading of :28; not taken: O-28. (b) X's law computed
afresh at 1w — needs a pivot run ("decoupled" forbids), whole-tape picks, under-floor n. (c) a calendar equivalent
of the 1d pin (five weekly bars) — a profile of five uniform slabs; X's own note that coarse-bar profiles approach
"a sum of boxcars" (LEANS_X :1629-1631). (d) the mean of the five filed 1-dp per-asset means — an
executor-invented statistic on whole-tape fits. (e) the 1w block read by the stamps alone, the 1d two-trades
printed unconditioned — not taken: O-28.

FAILS-IF: F-VA-PINS [a] (`VA_PINS.by_lens.1w.L_bars == by_lens.1d.L_bars`, label present on every 1w row) and
[e]; mutation: a copy of a registered arm's spec that reads `1w_state` must turn [e] RED.

**L-V.6 THE TIME-AT-PRICE TWIN** — "time-at-price twin printed" (contract :30)

READING: The twin is X's TPO count: each lens bar adds +1 to every row its `[low, high]` touches (row index =
`searchsorted(edges, price, "right") − 1`, clipped to `[0, bins − 1]`), with the same rows, the same POC and
expansion ties and the same centres (`tc11x_va.py:326-340, 370-377`; `va_series(..., mode="tpo")`). Volume is not
consulted in this mode, so **a zero-volume bar counts in the twin**: a zero-volume FLAT bar adds +1 to the one row
its price sits in (it spent its time at one price), while the volume profile gives the same bar zero weight
(`analytics/profile.py:139`) and still lets its high and low enter the window's range (:126). The twin is built for
every (asset, lens) cell and filed as `tpo_poc`, `tpo_val`, `tpo_vah` in `va/va_bars_<ℓ>.parquet`. "Printed" =
`va/STAGE_V.md` and `va/va_stack.parquet` carry, per cell: the median of `|VAH − tpo_VAH|/ATR`,
`|VAL − tpo_VAL|/ATR`, `|POC − tpo_POC|/ATR`; the V2 machine's event counters on the TPO series beside the
record's; and the zero-volume bar count of the tape with the largest count found inside any one lookback window.
The twin feeds no state column of record, no stamp, no traverse, no book, no licence.

SOURCE: LEANS_X LX-X3.5 (:1649-1653); `tc11x_va.py:370-378` (TPO mode tests finiteness only; the volume mode tests
`vk > 0`); the substrate section's zero-volume law (L-D.16: such bars are kept, counted and never skipped; its
orientation counts for the five home assets: 1h BTC 3, ETH 1; 4h, 12h, 1d, 1w none).

RIVALS: unit volume spread uniformly (X's null control) — a different object. Dropping zero-volume bars from the
twin — a bar spent time at a price whether or not it traded; and no consumer may skip such a bar. The twin stamped
at every funnel instant — doubles the vector for no named consumer.

FAILS-IF: F-VA-RAW [d] (TPO rows == a per-window searchsorted count, a zero-volume flat bar included by
construction of a planted window) and [c] (the FILED `tpo_*` columns == X's filed `tpo_*`, row for row);
mutations: the TPO row index taken with `side="left"`; zero-volume bars dropped from the TPO count.

**L-V.7 SUBSTRATE PER LENS AND ATR_L** — "volume-at-price" (contract :30); "ATR_L" (:35, :38, :45)

READING: A lens's profile reads that lens's own bars and no other interval's.

| asset set | lens | tape and volume source (snapshot `tc12_20261008`, L-D) |
|---|---|---|
| five home | 1h, 4h, 12h | native `klines/{sym}_{ℓ}.parquet` |
| five home | 1d | Stage D's derived `klines/{sym}_1d.parquet` (4h volume summed per complete UTC day) |
| five home | 1w | Stage D's derived `klines/{sym}_1w.parquet` (seven complete derived days, Monday-anchored UTC) |
| twelve new | 1h, 4h | native |
| twelve new | 1d | Stage D's derived 1d |

Every frame is taken through `E.D.load_asof(stem, lens)` (bars closing ≤ the corridor pin) or
`E.load_asof_at(stem, lens, cut_ms)` (a cut tape: the W tape of the equality legs and of DOOR 2, the prefixes of
the as-of legs; any integer instant ≤ `PIN` is admitted, and an off-grid instant such as ERA_CUT cuts each lens at
its last bar closed at or before it — L-D.28); columns `open_time:int64, open, high, low, close,
volume:float64`. One frame supplies both the prices and the volume of a cell, and a door still asserts X's
alignment law before any profile — the frame's `open_time` strictly increasing and equal, row for row, to the tape
it hands the machine — else HALT (`tc11x_va.py:303-322`). A zero-volume bar is one bar in every count of this
section: the lookback, the N closes, the K closes, the traverse. ATR_ℓ = `engine.indicators.atr(h, l, c,
ATR_LEN)`, `ATR_LEN` = `E.R2.ATR_LEN`, on the lens's WHOLE tape from its first bar (`engine/indicators.py:31-54`:
Wilder RMA, alpha = 1/len, seeded with `TR[0] = high[0] − low[0]`), computed in a door at full float and handed
into the module; the ATR DOOR 2 hands to the machine is computed from its own tape by the same call, never taken
from the 6-dp filed `atr` (L-V.23). It is prefix-invariant; a tail-loaded tape re-warms it and is refused.
`ATR[t]` includes bar t's own true range. A non-finite or non-positive `ATR[t]` at any `t ≥ L_ℓ` HALTs the cell.
**5m is not a VA lens**: no profile is built on 5m bars anywhere in TC12.

SOURCE: O-8, O-15; LEANS_X LX-X3.2 (:1619-1627); `engine/indicators.py` (sha `91805c04…c113`); TC11 LEANS L-R.1
(:172-175); `scripts/tierc11_data.py:1523-1531` (the weekly derivation); 17 `*_1w.parquet` and 17 `*_1d.parquet`
files exist in `tc11_20260925/klines/`, and the BTCUSDT and NEARUSDT files of both lenses carry a `volume` column
(inspected; the other fifteen stems are checked at build by the alignment HALT).

RIVALS: `analytics.volatility.atr` (SMA-seeded, NaN warm-up) — moves every 1.5-ATR acceptance. 1d/1w volume summed
from 1h — disagrees with native 4h/12h on X's six incident days. A 5m profile for the scalper — the contract makes
5m a clock, "never a signal source" (:89).

FAILS-IF: F-VA-ASOF [b] (row alignment) and [e] (`atr[t]` of every filed row == the fixture's own Wilder loop);
mutations: the volume column misaligned by one row in DOOR 1's loader; ATR taken at `t+1`.

**L-V.8 CAUSALITY, IN INDEX TERMS** — "CAUSAL: the VA stamped at bar t uses volume from bars ≤ t only" (contract
:30-31)

READING: Six rules; each is a fixture leg.
1. `VA(t)` reads bars `t−L_ℓ+1 .. t` of the lens's own tape — indices ≤ t. It is known at `close_ms[t]` and is IN
   FORCE from that instant until `close_ms[t+1]`.
2. An IDLE bar's close, and every bar's high and low, are judged against `VA(t−1)`. A close while a probe is
   pending is judged against that probe's FROZEN edge, the edge of `VA(t0−1)` (L-V.9) — X's convention, which
   O-16 (a) names. Never the self-inclusive `VA(t)`. The per-bar columns of L-V.16 (%-of-value, the edge and POC
   distances) and the traverse touches of L-V.18 are measured against `VA(t−1)` on every bar, pending or not;
   every state and event follows from the two judgements above. The first judged bar is `t = L_ℓ`.
3. `ATR[t]` is the denominator and the margin unit for bar t's close; it is known at `close_ms[t]`. No rule reads
   `ATR[t+1]`.
4. A stamp at an instant τ for lens ℓ reads bar `k = asof_index(close_ms, τ)` = the last bar with
   `close_ms[k] ≤ τ` (`searchsorted(close_ms, τ, side="right") − 1`; O-14; the one implementation is
   `tierc12_asof.asof_index`, a mirror of `tierc10_census.py:894-900`). A lens bar closing exactly at τ IS read; a
   bar still forming at τ never is.
5. A level that rests during bar `t+1` (an order, a target) may use `VA(t)` and `ATR[t]` and nothing later.
6. L, N, M, K, F and the traverse T are fixed before any book exists. L and T are tuning-fit: in-sample for
   tuning-era bars, labelled on every row that reads them.

SOURCE: `tc11x_va.py:28-29, 424-425, 535-541`; LEANS_X LX-X3.6 (:1655-1668); O-14, O-16; scout U2 §1.5, U6 §1.10.

RIVALS: judging against `VA(t)` (X's `self_inclusive` twin) — "a breakout bar drags VAH to its own close"
(`tc11x_va.py:70-71`). The engine's exec-OPEN law (`engine/htf.py:15-25`: HTF close ≤ exec OPEN) for stamps — it
hides the lens bar that closes exactly at a decision close; it coincides with rule 4 when the instant is written
as the close of the last finished bar.

FAILS-IF: F-VA-ASOF [a], [c], [d], [e]; F-NEST-ASOF [a], [b]; mutations: the window shifted one bar forward
(`t−L+2 .. t+1`, clipped at the tape end); judged columns computed from `VA(t)`; the in-force block shifted one
row forward in the table assembly; ATR taken at `t+1`; the as-of index of the lens above shifted by +1 (NULL
where it passes the tape end).

---------------------------------------------------------------------------------------------------------------
#### B · The state machine (V2)

**L-V.9 THE JUDGING FRAME AND THE FROZEN EDGE** — "at each close of lens L — INSIDE: close within [VAL, VAH] ·
PROBING above/below: close beyond an edge, not yet accepted" (contract :33-34)

READING: One pass in bar order; one resolution per bar (a bar that resolves a probe does nothing else).
- **Idle bar** (no probe pending) with a valid `VA(t−1)`: INSIDE iff `VAL[t−1] ≤ c[t] ≤ VAH[t−1]` — a CLOSED
  interval; a close exactly at an edge is inside. Beyond = strictly outside: `c[t] > VAH[t−1]` (top) or
  `c[t] < VAL[t−1]` (bottom).
- **A probe opens** on an idle close beyond an ARMED side: `t0 = t`; **the edge is FROZEN** at
  `E = VAH[t0−1]` (top) / `VAL[t0−1]` (bottom) — the profile that judged the first close beyond. Every later close
  of the probe is judged against E, not against the re-rolled VA: beyond iff `s·(c[t] − E) > 0` (strict); "back
  inside" iff `s·(c[t] − E) ≤ 0` (a close AT E is back inside). The test is one-sided: the opposite edge is not
  consulted while a probe is pending.
- **While a probe is pending** `VA(t−1)` is not consulted at all, valid or not; the probe's `extreme` is
  updated with bar t's high (top) / low (bottom) BEFORE the close is judged, so it includes the resolving bar.

SOURCE: `tc11x_va.py:585-635` (`lo_ <= cl[t] <= hi_` :618; `E0 = hi_ if side == "top" else lo_` :630; `beyond =
cl[t] > ref` :599 / `< ref` :602; extreme first :598, :601); LEANS_X LX-X3.6 (:1655-1668): "The edge is FROZEN at
an episode's first close outside … This is the pivot machine's law: the boundary does not move while a breach is
pending"; "judged against a moving VA, 27-37% of SFPs are 'drift-backs', where value moved to price rather than
price returning to value"; O-16 (a).

RIVALS: the edge re-rolled each bar (X's `moving_edge` twin) — turns value drifting to price into a "swing
failure". "Back inside" tested two-sided against the current `[VAL, VAH]` — a different event; the two two-sided
tests are filed as FLAGS on each event (L-V.14) so a consumer can require them, and the event of record stays X's.
An open interval for INSIDE — X's is closed.

FAILS-IF: F-STATE [b] rows "edge equality", [c] STRUCT (`E ==` the edge of `VA(t0−1)` exactly on every probe);
mutation: E taken from `VA(t0)`.

**L-V.10 ACCEPTANCE** — "ACCEPTED above/below: 8 consecutive closes beyond the edge OR one close ≥ 1.5 ATR_L
beyond" (contract :35)

READING: A pending probe is ACCEPTED at bar t iff `s·(c[t] − E) > 0` and either
- (count) `t − t0 + 1 ≥ N` — the N-th consecutive close beyond E, counting the probe's first close `t0` as the
  first; it lands at `t0 + N − 1`; `by = "n_closes"`; or
- (margin) `s·(c[t] − E) ≥ M·ATR[t]` — **the ATR of the SAME bar t**, inclusive `≥`; `by = "margin"`.

The count clause is tested first: on the N-th close `by = "n_closes"` even when the margin also holds. The margin
clause applies on the probe's FIRST bar too: a close at or beyond `E + s·M·ATR[t0]` opens and accepts in one bar
(`bars_out = 0`, `closes = 1`). Acceptance is known at `close_ms[t]`. It DISARMS its side and ends the value
regime alive at t.

SOURCE: `tc11x_va.py:603-608`: `if pend["closes"] >= ACCEPT_N: close_ep(t, "accept", "n_closes", ref)` /
`elif law.die_parity and abs(cl[t] - ref) >= BREAK_MARGIN * al[t]: close_ep(t, "accept", "margin", ref)`; and
:634-635 on the open bar: `if law.die_parity and abs(cl[t] - E0) >= BREAK_MARGIN * al[t]` (`al` = `atr.tolist()`,
:559). AM-X11 item (9) (`x_rec/tierc11x/LEANS_X_AMENDMENTS.md:242-268`) and AP-11 item 9
(`AMENDMENTS_PROPOSED.md:558-641`): "DIE parity … accepts on a close >= BREAK_MARGIN·ATR beyond E (the census's
`>=`), the open bar included". Contract :35; O-16.

RIVALS: `ATR[t−1]` as the margin unit — not X's law; the bar's own ATR is known at its close (L-V.8 rule 3).
Counting from `t0 + 1` (acceptance at `t0 + N`) — not X's (`closes` starts at 1 on `t0`, :631). Margin clause not
on the open bar — AM-X11 (9) rules it in. Strict `>` at the margin — the census's `>=`.

FAILS-IF: F-STATE [a] A1-A3, [b], [e]; mutations: `accept_n − 1`; the margin clause removed; the margin read
with `ATR[t−1]` (caught on the targeted bar of leg [e]).

**L-V.11 SWING FAILURE AND LAPSE** — "a probe that closes back inside within K=3 closes = SWING FAILURE at that
edge ["sfp-k"]" (contract :36)

READING: A pending probe that closes back inside (`s·(c[t] − E) ≤ 0`) at bar t resolves as
- **SWING FAILURE** iff `t − t0 ≤ K`: at most K closes beyond E (`t0 .. t0+K−1`) and the close back on the next;
- **LAPSE** iff `t − t0 > K` — reachable for `t − t0 ∈ {K+1, …, N−1}` (closes 4..7 at the filed values): neither a
  swing failure nor an acceptance. A lapse emits an event row, feeds no trade, changes no armed flag and does not
  end the regime.

Either way the machine returns to the state it left when the probe opened (L-V.13). The swing failure is known at
the back-inside close `close_ms[t]`; its side is the probed edge (top = VAH, bottom = VAL); its sign points toward
value (top → −1, bottom → +1); its **deviation extreme** = `max(h[t0..t])` (top) / `min(l[t0..t])` (bottom),
inclusive of both `t0` and the return bar t.

SOURCE: `tc11x_va.py:609-610`: `close_ep(t, "sfp" if t - pend["t0"] <= law.ret_k else "lapse", "", ref)`; X's `k3`
twin `EpLaw(ret_k=3)` (:532; `SFP_K_TWINS = (1, 3)` :187); LEANS_X LX-X3.8 (:1682-1691); the pivot machine's
`bars_out <= dev_ret` (`analytics/rangefinder_census.py`, the breach-return block); contract :36; O-16.

RIVALS: `t − t0 ≤ K − 1` (counting `t0` as the first of three) — not X's literal and no filed stream. A return on
closes 4..7 called a swing failure — that is X's record (K = 7), which the contract replaces. A lapse treated as an
acceptance — neither clause of :35 holds.

FAILS-IF: F-STATE [a] S1-S3, N1, [b], [c]; mutations: `ret_k + 1` (N1 becomes a swing failure); `ret_k − 1` (S2
becomes a lapse); the extreme computed without the return bar.

**L-V.12 DECAY, RE-PROBE, OPPOSITE PROBE, SIMULTANEITY** — "ACCEPTED decays to INSIDE when the re-rolled VA
contains the close (the profile re-forms)" (contract :37)

READING:
- **Decay.** With a side disarmed and no probe pending, the first IDLE close with `VAL[t−1] ≤ c[t] ≤ VAH[t−1]`
  re-arms BOTH sides, starts a new value regime at `r0 = t` and returns the state to INSIDE. "The re-rolled VA" is
  `VA(t−1)`, the rolling profile judging that close — not the frozen E and not the self-inclusive `VA(t)`.
- **Re-probe while ACCEPTED.** An idle close beyond a DISARMED side opens nothing; the state stays ACCEPTED on that
  side; the bar is counted (`blocked_reprobe`).
- **Opposite probe while ACCEPTED.** An idle close beyond the ARMED side opens a probe there (PROBING on that
  side); the standing acceptance stays. If the probe fails or lapses the state returns to the standing ACCEPTED; if
  it is accepted both sides are disarmed and the state is ACCEPTED on the newly accepted side.
- **A probe that flips straight to the other side.** A pending top probe whose next close is below `VAL[t−1]` is
  "back inside" by the one-sided test: it resolves (swing failure or lapse by K) and opens NOTHING on that bar. If
  the following idle close is still below the then-judging VAL, a bottom probe opens with `t0` = that bar.
- **Decay is judged on idle bars only.** A close inside `VA(t−1)` while a probe is pending (possible only when the
  VA has drifted past the frozen E) does not decay; such bars are counted (`rearm_blocked_by_pending`).
- **Simultaneous both-edge events cannot occur**: every transition is decided by ONE close, which lies on one side
  of one edge; wicks decide nothing in the machine.

SOURCE: `tc11x_va.py:618-625` (idle inside → `armed["top"] = armed["bottom"] = True`, `rearm_closes`, a new
regime); :627-629 (`blocked_disarmed`); :595-596 (`rearm_blocked_by_pending`); :611 (`continue` after the pending
branch). LEANS_X LX-X3.7 (:1674): "Re-arm: that side stays disarmed until a close inside the live VA(t−1)".
AM-X11 (1): "The re-arm is judged on idle bars, and the pending-bar rival is counted (15 bars against 20,225
episodes)". O-16.

RIVALS: decay on any close inside the live VA, pending or not — X's counted rival; it changes which later closes
open probes, so the event stream stops equalling X's. Decay tested against `VA(t)` — self-inclusive. Re-arming only
the accepted side — X re-arms both.

FAILS-IF: F-STATE [a] N2, [b] rows "decay", "blocked re-probe", "opposite probe", "flip"; mutation: decay evaluated
on pending bars.

**L-V.13 THE TRANSITION TABLE AND THE STATE COLUMN** — "THE STATE MACHINE (explicit; the module must implement
it …)" (contract :32-37)

READING: Memory after each bar: `armed_top`, `armed_bottom` (start True); the pending probe `(side, t0, E, closes,
extreme)` or none; the live regime start `r0` or none; `acc_side` (the side the ACCEPTED state reports). `closes`
= `t − t0 + 1` on a beyond bar.

| state before bar t | condition at the close of t | event(s) at t | state after bar t |
|---|---|---|---|
| UNDEFINED | `t < L_ℓ`, or no probe pending and `VA(t−1)` invalid | — | UNDEFINED |
| UNDEFINED (first valid bar) | as the INSIDE rows; the first value regime starts here (`r0 = t`) | as INSIDE | as INSIDE |
| INSIDE | `VAL[t−1] ≤ c ≤ VAH[t−1]` | — | INSIDE |
| INSIDE | `c > VAH[t−1]`, `c − E < M·ATR[t]` (`E = VAH[t−1]`, `t0 = t`) | probe | PROBING_ABOVE |
| INSIDE | `c > VAH[t−1]`, `c − E ≥ M·ATR[t]` | probe, acceptance (margin, `bars_out` 0) | ACCEPTED_ABOVE |
| INSIDE | `c < VAL[t−1]` | mirror of the two rows above | PROBING_BELOW / ACCEPTED_BELOW |
| PROBING_ABOVE | `c > E` and `t − t0 + 1 ≥ N` | acceptance (n_closes) | ACCEPTED_ABOVE |
| PROBING_ABOVE | `c > E`, count `< N`, `c − E ≥ M·ATR[t]` | acceptance (margin) | ACCEPTED_ABOVE |
| PROBING_ABOVE | `c > E`, neither clause | — | PROBING_ABOVE |
| PROBING_ABOVE | `c ≤ E`, `t − t0 ≤ K` | swing_failure (top) | the state the probe opened from: INSIDE, or ACCEPTED_BELOW if the bottom stands disarmed |
| PROBING_ABOVE | `c ≤ E`, `t − t0 > K` | lapse (top) | same destination as the row above |
| PROBING_BELOW | mirror of the five rows above (`c < E` beyond; `c ≥ E` back inside) | mirror | mirror |
| ACCEPTED_ABOVE | `VAL[t−1] ≤ c ≤ VAH[t−1]` | decay | INSIDE (both sides re-armed, `r0 = t`) |
| ACCEPTED_ABOVE | `c > VAH[t−1]` | — (`blocked_reprobe`) | ACCEPTED_ABOVE |
| ACCEPTED_ABOVE | `c < VAL[t−1]`, bottom armed | probe (+ acceptance by margin) | PROBING_BELOW (or ACCEPTED_BELOW) |
| ACCEPTED_ABOVE | `c < VAL[t−1]`, bottom disarmed too | — (`blocked_reprobe`) | ACCEPTED_BELOW |
| ACCEPTED_BELOW | mirror of the four rows above | mirror | mirror |

**The state column** is a pure function of the memory after bar t: UNDEFINED per the first row; else PROBING on
the pending side if a probe is pending; else INSIDE if both sides are armed; else ACCEPTED on `acc_side`, where
`acc_side` is set to the accepted side at an acceptance, to the side of the close on a blocked idle bar, and
cleared at decay. Three consequences are stated and COUNTED per cell in `STAGE_V.md`, never hidden:
(i) on a bar that resolves a probe by swing failure or lapse the state is INSIDE by the frozen edge even when the
close lies outside the rolling `VA(t−1)` (`n_inside_outside_rolling_va`); the next idle bar re-judges it. This
departs from the contract's letter ("INSIDE: close within [VAL, VAH]", :34), is declared in AM-1 (L-V.15), and is
FILED PER BAR as the boolean `inside_frozen_only` of `va_bars_<ℓ>` — true iff the bar resolved a probe and
`state == "INSIDE"` by the frozen edge while `close` lies outside `[val_j, vah_j]` — so a consumer that reads
INSIDE (the scalper's permission) can count and print how often it reads it on such a bar;
(ii) a failed probe opened under a standing acceptance returns to ACCEPTED (`n_return_to_standing`);
(iii) bars with both sides disarmed (`n_both_disarmed_bars`). `armed_top` and `armed_bottom` are filed beside the
state so no consumer has to infer them.

SOURCE: contract :32-37; `tc11x_va.py:544-646` whole; O-16; scout U2 R9. The state column has no X counterpart
(X files events and the boolean `close_in_va_prev`): it is new, and is derived from X's memory variables without
feeding back into them, so the event stream is unchanged by it.

RIVALS: state = position of the close in the rolling VA only (INSIDE iff inside `VA(t−1)`) — loses PROBING vs
ACCEPTED, which the contract's gates read. State after an acceptance = "latest acceptance" when both sides are
disarmed — reports ACCEPTED_BELOW with price above value; the position rule is used instead. A seventh state for
"standing acceptance, probe pending" — the two flags carry it.

FAILS-IF: F-STATE [b] (every row of this table on a synthetic tape generated from N, M, K; the tape includes a
resolution bar whose close lies outside the rolling `VA(t−1)`, on which `inside_frozen_only` must be true), [c]
(identities; `n_inside_outside_rolling_va ==` the count of `inside_frozen_only` rows per cell), [d] (prefix);
mutations: listed under L-V.10..12; `inside_frozen_only` computed against the in-force profile `VA(t)`.

**L-V.14 THE EVENT RECORDS** — "PROBING … ACCEPTED … SWING FAILURE … decays" (contract :34-37)

READING: One row per event in `va/va_events.parquet`, key `[lens, asset, kind, side, i, t0]`,
`kind ∈ {probe, acceptance, swing_failure, lapse, decay}`, each row KNOWN AT `known_close_ms`. Fields, exact:

| field | meaning |
|---|---|
| `lens`, `asset`, `kind`, `side` | side `top` (VAH) / `bottom` (VAL); for `decay`: the side whose acceptance stood (`both` if both) |
| `t0`, `t0_close_ms` | the probe's first close beyond (bar index of the lens tape; its close). `decay`: the bar of the acceptance being decayed |
| `i`, `known_close_ms`, `era`, `in_strip` | the bar whose close prints the event (`probe`: `i = t0`); its close; `era = E.era_of(known_close_ms)`: tuning iff `known_close_ms ≤ ERA_CUT`, else holdout (the estate's close-based era law); `in_strip` iff `known_close_ms > W` |
| `bars_out` | `i − t0` |
| `closes` | closes beyond E so far (X's counter: 1 at `t0`) |
| `by` | `n_closes` / `margin` for an acceptance, else empty |
| `E` | the frozen edge = that edge of `VA(t0−1)` |
| `extreme` | the DEVIATION EXTREME: `max(h[t0..i])` (top) / `min(l[t0..i])` (bottom), inclusive of the return bar |
| `close_i`, `atr_i`, `excess_atr` | `c[i]`, `ATR[i]`, `s·(c[i] − E)/ATR[i]` |
| `sgn` | swing_failure, lapse: −1 top / +1 bottom (toward value); probe, acceptance: +1 top / −1 bottom; decay 0 |
| `val_f`, `poc_f`, `vah_f` | the FROZEN profile `VA(t0−1)` — the profile whose edge was probed |
| `val_n`, `poc_n`, `vah_n` | the profile in force after the event bar, `VA(i)` |
| `ret_inside_frozen`, `ret_inside_rolling` | swing_failure / lapse only: `val_f ≤ c[i] ≤ vah_f`; `VAL[i−1] ≤ c[i] ≤ VAH[i−1]` |
| `from_state`, `state_after` | the state when the probe opened; the state after bar i |
| `rid`, `r0` | the value regime alive at `t0` (−1 if none) |
| `episode` | the probe's ordinal per (asset, lens), assigned at `t0` and carried on the probe row and on its resolving row; −1 on a decay row |

Dtypes: `lens`, `asset`, `kind`, `side`, `era`, `by`, `from_state`, `state_after` str; `t0`, `t0_close_ms`, `i`,
`known_close_ms`, `bars_out`, `closes`, `rid`, `r0`, `episode` int64; `in_strip` bool; `sgn` int8; the two return
flags nullable boolean; the levels and ratios float64.
**No field of an event row depends on a bar after `i`.** How a probe ended is read from its resolving row
(`swing_failure` / `lapse` / `acceptance`), joined on `(lens, asset, side, t0)`; a probe with no resolving row is
pending. X's episode fields `end_i` and `end_kind` are therefore not carried onto a probe row: they are later
facts, and a probe row is known at its own bar.

Regimes are filed in `va/va_regimes.parquet`, key `[lens, asset, rid]`: `r0, r0_close_ms, start_kind ∈
{first_valid, decay}, die_i, die_close_ms, end_side, end_by, n_bars`. A value regime runs from the first valid bar
or a decay bar to the next acceptance; its geometry excludes the acceptance bar.
**`va_regimes` is a SUMMARY table, not an as-of table.** A consumer bounded at an instant B treats a regime with
`die_close_ms > B` or null as alive at B and reads none of its `die_*`, `end_*`, `n_bars`; the reader offers
`regimes(asof_close_ms=B)` and no unbounded form (L-V.2).
Identities held per cell: `probe == swing_failure + lapse + acceptance + pending_at_end`, where `pending_at_end`
is the number of probes with no resolving row (at most one per cell); `regimes == 1 + decay` on a tape with at
least one valid bar (each decay starts exactly one regime); every acceptance has `by` non-empty; every row is
known at its own bar (`known_close_ms == close_ms[i]`). Which profile sets a trade's POC and far edge (`*_f` or
`*_n`) is the trading section's reading (L-R.12).

SOURCE: `tc11x_va.py:569-583` (`close_ep`), :630-646 (X writes an episode's end onto it when it resolves, or at
the tape end, :636-640 — a later fact than the probe's own bar), :1243-1264 (`ev_rows_va`); X's
`events_va.parquet` schema (54 columns, read here); AM-X11 (4), (5); O-29 (the tables are read as filed data, so
a filed row must hold nothing a consumer bounded at its instant could not know).

RIVALS: file only swing failures and acceptances (X's `sfp`/`accept` rows) — the lapse and the decay are V2
outcomes a reader must be able to count. Carry only the frozen profile — the in-force one is one column join away
and the trading section must choose between them in the open.

FAILS-IF: F-STATE [c] (the identities; `extreme` and `E` recomputed from the raw tape for every event) and
F-VA-ASOF [d] (every event row known at or before a cut equals the row rebuilt on the tape cut there, on every
column); mutations: a dropped lapse row; a swing failure stamped at `t0`; the resolving bar written onto a probe
row (must turn F-VA-ASOF [d] RED at the rule-based cut one bar before a swing failure); the filed `va_regimes`
read without its bound, so that the later facts of a regime alive at the cut leak (must turn F-VA-ASOF [d] RED).

**L-V.15 EQUALITY WITH X, AND THE DATED AMENDMENT** — "X's semantics asserted equal on the 4h holdout sample,
amendments dated if they differ" (contract :32-33)

READING: Write a law as the triple `(accept_n, margin_atr, ret_k)`. The contract's V2 is `(N, M, K)`. X's machine
OF RECORD is `(N, none, 7)`; X never ran V2. X filed two one-field twins: `die_parity` = `(N, M, 7)` and `k3` = `(N, none, K)`.
Because only an ACCEPTANCE changes an armed flag or a regime (`tc11x_va.py:575-582`) and `ret_k` only chooses the
label at :610, **V2's event stream is X's `die_parity` stream with every return of `bars_out > K` relabelled from
sfp to lapse**; acceptances, edges, extremes and bars are identical.

The equality target (F-STATE-X), computed by the module at FULL FLOAT from the tapes cut at W
(`E.load_asof_at(stem, lens, W)`) and compared with X's filed rows:
- **Rows.** `x_rec/tierc11x/va/events_va.parquet`, `lens == "4h"`, `variant == "die_parity"`,
  `cls ∈ {"sfp", "accept"}`, five home assets.
- **Era by join.** X's twin `accept` rows carry an EMPTY `era` and a null `known_close_ms` (verified: 1,605 of
  1,605 at 4h). The era is taken by joining `(asset, i)` to `va_series_4h.parquet` `(asset, i)` → `close_ms`;
  holdout iff `ERA_CUT < close_ms ≤ W`. Filtering X's `era` column directly is forbidden (it drops every
  acceptance).
- **Mapping.** X `accept` ↔ V2 `acceptance`; X `sfp` with `bars_out ≤ K` ↔ V2 `swing_failure`; X `sfp` with
  `bars_out > K` ↔ V2 `lapse`.
- **Comparison.** Set equality of V2's resolving rows on `(asset, side, t0, i)` with X's rows on `(asset, side,
  t0, end_i)` (X's `end_i` is the resolving bar, which is V2's `i`) and, per matched row, exact equality of the
  integers and strings `(by, closes, bars_out)` and equality of `E` and `extreme` with X's `E` and `extreme` —
  and of `E` with X's `E_end`, the edge at the resolving bar, which under the frozen-edge law is `E` itself
  (`tc11x_va.py:572, :588-589`) — AT THE 6-dp WRITE LAW: the fresh value passed through the estate's own write
  function (`tierc2_baseline._round_floats`, :162-167, the function X's writer used) must equal the filed value
  exactly — no tolerance.
- **The 6-dp hazard.** X's writer rounds levels to 6 dp, and a state re-derived from FILED levels flips at exact
  edges (scout U2 H7: ZECUSDT 4h `i = 8337`, close 30.17 against a filed VAH of 30.170000 with the filed flag
  False). The fixture never derives a state or an event from filed levels: events come from the fresh full-float
  series; the FILED series is compared with X's filed series row for row (F-VA-RAW [c]); the fresh full-float flag
  `VAL[i−1] ≤ c[i] ≤ VAH[i−1]` is compared with X's filed `close_in_va_prev` on every bar; and the count of bars
  where the flag re-derived from the filed 6-dp levels would differ is printed as a disclosure.
- **Scope.** The contract's leg is the 4h holdout. The same comparison is binding on 4h tuning and on 1h, 12h, 1d
  (both eras), and three mirror legs prove the mirrored machine IS X's before V2 is trusted: `(N, none, 7)` against
  X's `record` rows, `(N, M, 7)` against `die_parity`, `(N, none, K)` against `k3`; and the machine at
  `(N, none, 7)` on the TPO series against X's `tpo` rows. The value 7 is read from
  `va/build_manifest.json` → `pins.laws.dev_return_bars` and is used by these legs only.
- **Counters.** On each of X's 20 cells the V2 counters `probe`, `acceptance`, `acceptance by margin`, `decay`,
  `blocked_reprobe`, `regimes`, `rearm_blocked_by_pending`, `pending_at_end` equal `va/build_manifest.json` →
  `event_counts["<asset>|<lens>"]["die_parity"]` keys `breach`, `accept`, `accept_by_margin`, `rearm_closes`,
  `blocked_disarmed`, `regimes`, `rearm_blocked_by_pending`, `open_at_end`; and `swing_failure + lapse == sfp`.
- **Expectations, not inputs** (scout U2 R10, structural): on the 4h holdout, 555 acceptances (432 by margin, 123
  by count) and 725 closes back inside = 602 swing failures + 123 lapses. The fixture reads its counts from the
  files and prints them beside these.

**The dated amendment — AM-1 (nickname AM-V2).** It is the contract's own order ("amendments dated if they
differ", :33; O-16 (c)): no AP precedes it. The orchestrator files it in `T12/LEANS_AMENDMENTS.md` at the
TC12-LEANS freeze under the heading
`## AM-1 · <freeze date UTC> (~HH:MMZ) · L-V.9..L-V.15 · contract :32-33 (no AP) · AM-V2`
and in L-0.5's body form. Text of record (the constants it speaks — 8, 1.5 and 3 — are the contract's at :35-36;
7 is X's `pins.laws.dev_return_bars`):
"TC12's value-area machine is the contract's V2 and differs from TC11-X's machine of record in two fields. (1)
Acceptance: X's record accepts on the 8th consecutive close strictly beyond the frozen edge only; V2 also accepts
on one close at or beyond 1.5·ATR_L of the same bar beyond the edge, the probe's first bar included — X's
`die_parity` twin. (2) The swing-failure return window: X's record is t − t0 ≤ 7; V2 is t − t0 ≤ 3 — X's `k3`
twin. V2 therefore has an outcome X's record cannot reach, the LAPSE (a return on closes 4..7), which is neither a
swing failure nor an acceptance and feeds no trade. X never ran the two fields together; V2 equals X's filed
`die_parity` stream with returns of bars_out > 3 relabelled lapse, held by F-STATE-X on the 4h holdout and on
every other lens and era. Everything else is X's law unchanged: each idle close judged against VA(t−1); the edge
frozen at the probe's first close and every pending close judged against it; decay on the first idle close inside
the rolling VA(t−1); one resolution per bar. Declared against the contract's letter: (i) a close while a probe is
pending is judged against that probe's frozen edge, not against the rolling VA(t−1); (ii) on a bar that resolves a
probe the state is INSIDE by the frozen edge even where the close lies outside the rolling VA(t−1), counted per
cell and filed per bar as `inside_frozen_only`. New in TC12 with no X counterpart: the per-bar state column, the
signed edge distance, the POC distance, the VA age column, the value-area traverse, the lens-ladder coincidence,
the 1w block on a borrowed lookback. **The feasibility words that license the range trades (F-VA-MIRROR) were
earned on X's record machine, not on V2**; they are read, not re-earned (DISCLOSURES D-2)."

SOURCE: O-16; contract :32-37; L-0.5 (the amendment sources and the heading grammar: AM-1 is source (iv), the
contract's own order); `tc11x_va.py:520-532, 569-583, 610`; `events_va.parquet` and `va_series_4h.parquet`
schemas and the blank-era fact (inspected while drafting); scout U2 §1.6, R10, H7, H8.

RIVALS: assert equality against X's `record` rows — fails by construction (different law). Recompute X's twin by
running `tc11x_va` — forbidden. Compare floats at a 1e-6 tolerance — looser than the write law and unnecessary if
the mirror is exact. Derive the era from X's `era` column — drops every acceptance.

FAILS-IF: F-STATE-X [x1]-[x6]; mutations: the relabel threshold moved to `K + 1`; the era taken from X's `era`
column (the acceptance count must collapse to 0 and the leg turn RED); `margin_atr` read with `ATR[t−1]`. The
amendment's presence and heading are held by L-0's F-FROZEN-TEXT and by the registry's `amendments` pin (L-X.19).

**L-V.16 THE COLUMNS** — "Columns at every instant: state · %-of-value · signed edge distance (ATR_L) · VA age ·
POC distance" (contract :38)

READING: Computed at every close of lens ℓ, for bar `t ≥ L_ℓ`, against the JUDGING profile `VA(t−1)` =
`(VAL_j, POC_j, VAH_j)` with `ATR[t]`; filed per bar in `va/va_bars_<ℓ>.parquet`; read at any other instant by the
as-of rule of L-V.20.

| column | formula | notes |
|---|---|---|
| `state` | L-V.13 | the name from `STATE_NAMES` |
| `pct` (%-of-value) | `PCT·(c[t] − VAL_j)/(VAH_j − VAL_j)`, `PCT` = the percent factor of L-V.4 | UNCLIPPED: below value it is negative, above value it exceeds `PCT`; NaN when `VAH_j == VAL_j` or the profile is invalid |
| `edge_dist_atr` (signed edge distance) | `σ·min(abs(VAH_j − c[t]), abs(c[t] − VAL_j))/ATR[t]`, with `σ = +1` if `VAL_j ≤ c[t] ≤ VAH_j` else `−1` | distance to the NEARER edge; POSITIVE inside value (zero at an edge), NEGATIVE beyond it |
| `near_side` | `+1` if `abs(VAH_j − c[t]) ≤ abs(c[t] − VAL_j)` else `−1` | which edge is nearer; a tie goes to VAH |
| `d_vah_atr`, `d_val_atr` | `(c[t] − VAH_j)/ATR[t]`, `(c[t] − VAL_j)/ATR[t]` | the two raw signed distances, no convention |
| `poc_dist_atr` (POC distance) | `(c[t] − POC_j)/ATR[t]` | signed: positive above the POC |
| `va_age` | `t − r0` while a value regime is alive after bar t (both sides armed: INSIDE, or a probe opened from INSIDE) | bars since the regime began: `r0` = the first valid bar (`L_ℓ`) or the decay bar; 0 on those bars; NULL when no regime is alive |
| `accept_age` | `t − last_accept_i` when no regime is alive | NULL otherwise |

`pct` and `state` are coherent on idle bars: INSIDE ⇔ `0 ≤ pct ≤ PCT`, except the counted resolution bars of
L-V.13 (i), which carry `inside_frozen_only`. Bars `t < L_ℓ`: `state = UNDEFINED`, every other column NULL.
Dtypes as filed: `state` str; `near_side` int8; `va_age`, `accept_age` nullable Int64; the rest float64.

SOURCE: `tc11x_va.py` `va_view` :1208-1218 (`pct = 100.0 * (c - rl) / (rh - rl)`, `dist = minimum(abs(rh - c),
abs(c - rl)) / tape.atr`), `adapter_walk` :955 (`ir_age = t − r0`); TC11 LEANS L-R.5 (:226-229): "%-of-range
(unclamped); signed distance to the nearest boundary in ATR_L: positive inside the box, negative beyond it, with
near_side beside"; `tierc10_census.py:843-849` (`near_top = … d_top <= d_bot  # tie -> top`); scout U2 R14.

RIVALS: `pct` clipped to [0, 100] — hides how far beyond value a close is. Distance signed by edge (positive above
VAH, negative below VAL) — conflates inside with outside; the two raw distances carry it. Age of the profile window
(always L) — not a regime age. Columns against `VA(t)` — self-inclusive (L-V.8 rule 2).

FAILS-IF: F-VA-ASOF [c] (every column recomputed by the fixture's own arithmetic from the raw tape and the house
profile of `t−L .. t−1`) and [e] (the judging block of row t is the in-force block of row t−1, exactly);
mutations: columns computed from `VA(t)`; `pct` clipped; the sign of `edge_dist_atr` flipped.

---------------------------------------------------------------------------------------------------------------
#### C · Mirror, traverse

**L-V.17 F-VA-MIRROR** — "reproduce X's feasibility verdicts from X's records — 4h taker PASS · 1d taker PASS ·
1h maker PASS · 12h FAIL · 1h taker FAIL — HALT if the mirror disagrees on any word (the Q-R3 law licenses exactly
{VA-4h taker, VA-1d taker, VA-1h maker}; nothing else may trade a range)" (contract :39-41)

READING: The mirror READS; it recomputes nothing under V2 (O-17).
1. **File.** `x_rec/tierc11x/va/feasibility.parquet`, opened through `E.x_rec`; its sha256 is asserted equal to
   its `X_REC_MANIFEST.json` row and to `progress/X3.json` `artifact_shas` (on file `ea8573b3…b6f0`) before the
   read.
2. **The five words** are parsed from contract :39-40 as `(lens, toll, word)`: (4h, taker, PASS), (1d, taker,
   PASS), (1h, maker, PASS), (12h, taker, FAIL), (1h, taker, FAIL). "12h FAIL" names no toll: it is read as the
   TAKER row, the row X flags `of_record_for_detector`.
3. **Row filter**, per word: `asset == "POOLED:CLASSIC5"` AND `era == "holdout"` AND `scale_kind == "va_regime"`
   AND `lens == <lens>` AND `toll == <toll>`. Exactly one row, else HALT.
4. **Column and comparison.** The token is the row's `would_read` string; it must equal the contract's word by
   exact string equality (`==`, case-sensitive, untrimmed). `"FAIL (provisional, n<30)"` is not `"FAIL"`.
   `lens_word` is NOT the column: it is empty on every maker row and, on the 1h taker row, is the sentence "FAIL —
   maker twin PASSES (the reopening path; needs a toll-model change the operator rules)".
5. **Cross-checks, each a HALT.** (a) `verdict_pass == (word == "PASS")`. (b) The tracked manifest
   `va/build_manifest.json` → `va_lens_verdicts`: `["4h"].word == "PASS"`; `["1d"].word == "PASS"`;
   `["12h"].word == "FAIL"`; `["1h"].word` equals the sentence above exactly and its first whitespace-delimited
   token is `"FAIL"`; `["1h"].maker_twin == "PASS"`. (c) `of_record_for_detector` is True on the four taker rows and
   False on the 1h maker row — the mirror says in the record that "1h maker PASS" is X's maker TWIN, made a licence
   by the operator's "maker" ruling (contract :2-3). (d) Each word re-derives from its row's printed columns by the
   Q-R3 law, in the form of X's fixture `my_word` (`tc11x_va_fixtures.py:927-936`): height leg `n_ranges ≥` the
   row's `min_n_ranges_pinned` AND `ratio_median ≥ HEIGHT_RATIO_MIN` AND `share_ratio_lt_1 ≤ INFEASIBLE_MAX_SHARE`;
   edge leg `edge_n ≥ edge_min_n_bars_pinned` AND `edge_n_ranges ≥ edge_min_n_ranges_pinned` AND
   `edge_net_h20 > 0`; PASS iff both. The two ratio constants are read as AST literals from
   `scripts/tierc10_census.py` (:2155-2156).
6. **HALT.** Any disagreement stops Stage V: `va/VA_MIRROR.json` is not written, and no range builder can start
   (the reader's `licence` HALTs without it).
7. **The licence record** `va/VA_MIRROR.json` is a REGISTERED record: it joins the typed list of registered tables
   and carries no Tier-E collar. **TC12 computes no number in this file**: every value is X's, QUOTED from the row
   its `x_row` key names, with the parquet's sha. Keys, complete:
   - `x_file {path, sha256}`;
   - `words` — the five in the contract's order, each `{lens, toll, word, x_row, would_read, verdict_pass,
     of_record_for_detector, toll_bps, edge_net_h20}`, `x_row` = `{asset, era, scale_kind, lens, toll}`;
   - `licence["<lens>|<toll>"].by_era[<ALL|tuning|holdout>]` for the three licensed pairs = `{would_read,
     verdict_pass, edge_net_h20, toll_bps, x_row, n_ranges, ratio_median, share_ratio_lt_1, edge_n, edge_n_ranges,
     edge_median_term_h20, edge_toll_atr}` — the row of that era, so each range trade reads the row of its own
     scoring era and the report prints beside it the rows that do not pass (O-17: 1d taker FAILS on ALL and on
     tuning);
   - `licence_set` — a list of `"<lens>|<toll>"` (item 9);
   - `beside` — the 12h maker rows (the `va_regime` row and its `va_lblock` twin, each quoted with its `x_row`),
     the 1h `lens_word` sentence, and `twin_words` = `{"4h|maker": {would_read, toll_bps, edge_net_h20, x_row}}`
     quoted from X's holdout row: the words of pairs that license nothing and are printed beside a row or a twin.
   There is no `at_maker_pin` block and no figure at Stage D's maker rate in this file: the edge leg re-expressed
   at the pinned rate is the scorer's collared beside leaf `licence_at_maker_pin` on P-SCALP-3, computed from the
   columns this record quotes for the `1h|maker` holdout row; it decides nothing (O-19, OD-12; L-S.27, L-X.14).
8. **The selector a registered row's precondition cites:** `{record: research_outputs/tierc12/va/VA_MIRROR.json,
   certified_by: progress/TC12-V.json artifact_shas, selector:
   licence["<lens>|<toll>"].by_era["<era>"].would_read, required: "PASS"}` — `"4h|taker"` at `ALL` for P-SFP-VA-1
   (with a second item on `licence_set` containing `"4h|taker"`); `"1h|maker"` at `holdout` for P-SCALP-3, its ONE
   precondition (OD-12); `"1d|taker"` for the Tier-E 1d cell, as a pointer and a boolean in that arm's sidecar,
   never a closing item. Which word closes a row by precondition is that registration's own rule (L-R.22, L-S.27).
9. **The licence set** is the PASS words among the five = {(4h, taker), (1d, taker), (1h, maker)}, asserted equal
   to the set parsed from :41. The reader's guard `licence(lens, toll, era)` returns the selected leaf and HALTs
   for any pair outside the set; each call is appended to the calling process's `licence_reads`, which L-0.13's
   manifest helper writes into that builder's directory `READ_SET.json`. The guard governs a book's TRADE OF
   RECORD. That every range book's pair is inside the set, and that each range builder read its own pair, is
   proven on the BOOKS by F-NOT's leg LICENCE (L-0.30), not only where a builder chooses to ask. A cost twin the
   contract itself orders inherits its parent's licence and prints the mirror word of its own (lens, toll) beside:
   the 4h maker twins of P-SFP-VA-1 (:75) print `beside.twin_words["4h|maker"]`; the scalper's all-taker twin
   column (:102) prints the fifth of the `words` (1h taker). Those twins and the twelve's rows (:84) are the
   members of L-0.30's `ORDERED_TWINS_T`.
10. **Printed beside the "1h maker PASS" word**, in `STAGE_V.md` and in the report: the row's `toll_bps` (the
   round trip X assumed) and Stage D's `maker_pin.differs_from_x_assumption` flag (O-19).

SOURCE: O-17, O-19, O-29; OD-12; `feasibility.parquet` rows and `va_lens_verdicts` read while drafting (the five
`would_read` values are PASS, PASS, PASS, FAIL, FAIL; `toll_bps` 10.0 taker, 4.0 maker); the parquet's schema
re-read while revising (it holds every column item 7 quotes, and one pooled `va_regime` row per (lens, toll, era),
the 4h maker rows included); `tc11x_va.py:1727-1756`; DISCLOSURES D-2; the sibling readings L-0.30 (F-NOT leg
LICENCE; `ORDERED_TWINS_T`), L-0.13 (`READ_SET.json`), L-X.10 (the precondition item's form); scout U2 §1.8.

RIVALS: recompute the verdicts under V2 regimes and call that the mirror — a different object (scout U2 H4).
Compare `lens_word` — empty on the maker row. Read "12h FAIL" as both tolls — the contract names one word; the
maker row is printed beside. Read the ALL-era rows — X's rows of record are holdout. A block of the licence
re-derived at Stage D's maker rate inside this record, or a second closing precondition on it — not taken: OD-12,
O-17 (the mirror reads, never recomputes).

FAILS-IF: F-VA-MIRROR [a]-[d]; mutations on COPIES of the parquet: the 4h taker `would_read` flipped; the 1h maker
row's `era` changed (0 rows); the mirror pointed at `lens_word`; a `licence("12h", "taker", "holdout")` request
must HALT; a number written into a copy of `VA_MIRROR.json` that no X row holds must turn [c] RED.

**L-V.18 THE TRAVERSE TABLE** — "per lens, the median bars for price to travel edge-to-edge while INSIDE (the
time stop of record for every range trade; read, never typed; F-TRAV greps for typed constants → FAIL)" (contract
:42-43)

READING: No value-area traverse exists on disk (X's T is a pivot confirm traverse, 1h and 4h only). It is defined
here as the value-area analog of X's in-range traverse (B1): **from the first touch of one edge to the first
subsequent touch of the OPPOSITE edge, inside one value regime — with no intervening acceptance.**
- **Regimes** are V2's (L-V.14). Bars scanned per regime: `t = r0 .. die_i − 1` (alive: to the last bar).
- **Touch**, by the bar's range against the judging profile, inclusive, no epsilon: top touch iff
  `h[t] ≥ VAH[t−1]`; bottom touch iff `l[t] ≤ VAL[t−1]`.
- **Chain.** No side yet: a bar touching EXACTLY one edge starts the chain (`side` = that edge,
  `start = last = t`); a bar touching both before the chain starts is skipped and counted. Side set: if the bar
  touches the opposite edge the leg completes at t with `b1 = t − start` and `b2 = t − last` (a both-touch bar
  completes it); then `side` flips and `start = last = t`. Else if it touches the current side, `last = t`.
- **Open legs** (regime end by acceptance, or tape end) are dropped and counted.
- **"While INSIDE"** = within a value regime. Bars of a probe that fails or lapses are inside the leg (a swing
  failure followed by a travel to the far edge is the very trade the stop times). Each leg files `n_probe_bars` =
  the number of its bars `start_i .. end_i` whose state after the close is PROBING_ABOVE or PROBING_BELOW.
  **T of record uses the regime reading; the contract's phrase read strictly — the same statistic over the tuning
  legs with `n_probe_bars == 0` (every bar of the leg INSIDE after its close) — is a printed twin per lens and
  enters no book** (OD-15).
- **Unit and statistic.** `b1` in bars of the lens. Per lens ℓ ∈ {1h, 4h, 12h, 1d}:
  `T_ℓ = traverse_pin(b1 of the legs whose COMPLETION bar closes ≤ ERA_CUT, pooled over the five home assets)` =
  `ceil(median)`, by X's integer law (odd n: the middle value; even n: `(s[m−1] + s[m] + 1) // 2`).
- **Era (O-18).** Tuning legs only. A leg that starts in the tuning era and completes after ERA_CUT is not a
  tuning leg.
- **Freeze.** DOOR 1 writes, ONCE, at stage `TC12-V`, before any range book exists, and `progress/TC12-V.json`
  pins both shas:
  - `va/TRAVERSE.json`, **the traverse pin record** — `by_lens.<ℓ>` for ℓ ∈ {1h, 4h, 12h, 1d} = `{T_of_record,
    n_legs, lower_hinge, median, upper_hinge, per_asset_median, label, provisional}` (the hinges are the medians of
    the lower and upper halves of the sorted legs, the middle value left out when n is odd, so that no quantile
    level is typed; `label` = "T tuning-fit (in-sample for tuning-era trades)"); `by_lens.1h.T_in_5m_bars`;
    `twins.strict_inside.<ℓ>` = `{T_strict_inside, n_legs_strict, lower_hinge, median, upper_hinge}`;
    `twins.scored_window.<ℓ>` and `twins.holdout.<ℓ>` = `{T, n_legs, lower_hinge, median, upper_hinge}`;
    `x_pivot_T.<ℓ>` (X's pivot T, quoted; null at 12h and 1d, where X pinned none);
  - `va/traverse_legs.parquet`, key `[lens, asset, rid, leg_seq]`: `from_side, start_i, end_i, start_close_ms,
    end_close_ms, b1, b2, n_probe_bars, both_touch_end, era_of_end`.
  The register rows `traverse.<ℓ>` (source `by_lens.<ℓ>.T_of_record`) and `traverse.1h.in_5m_bars` are FITTED
  pins, and a consumer reads them only through the reader's `traverse(name)` (L-V.2), which HALTs unless the
  file's sha is the certified one.
- **Floor.** `n_legs ≥` the floor (L-V.4) at 1h and 4h (the lenses with a registered consumer), else HALT
  `TRAVERSE-UNDER-FLOOR` and file an amendment. Under the floor at 12h or 1d: filed with `provisional: true`.
- **Printed beside, Tier-E, no pin** (in `STAGE_V.md` beside `T_of_record`, and under `twins` in
  `TRAVERSE.json`): the strict-INSIDE twin above (`T_strict_inside`, `n_legs_strict`, the hinges, per lens); the
  same statistic on the whole scored window (completion close ≤ W) and on the holdout slice (ERA_CUT < completion
  close ≤ W); X's pivot T (`PINS_X.json` `T.by_lens.<ℓ>.T_of_record`, which exists for 1h and 4h only) as the
  continuity column `x_pivot_T`. `STAGE_V.md` also prints the `b2` distribution (hinges and median) from
  `traverse_legs.parquet`. The forward strip is never pooled (O-9).
- **12h and 1w.** The 12h row is computed and labelled "no consumer: 12h is closed for range trading". No 1w row
  (O-28: no 1w traverse row exists).
- **The scalper's clock.** `T_5m = T_1h × (E.LENS_MS["1h"] // E.LENS_MS["5m"])`, the factor read by object from
  the env's `LENS_MS` (L-D); filed as `by_lens.1h.T_in_5m_bars`. Which bar the count starts from and where the
  trade exits are the scalper section's reading (L-S.20).
- **"Read, never typed."** Every range trade row carries `T`, and its book's manifest carries
  `time_stop_source = {path, key, sha256, value}`, the `source` the reader's `traverse` returns. The flow witness
  of the pin: bent by one bar at its door, the bar of a time-stop exit moves by one bar.

SOURCE: contract :42-43, :72, :100; O-18, O-28; OD-15; `tc11x_ranges.py` `b_traverses` :787-810 ("a traverse
completes at the first bar touching the side OPPOSITE the current one (a both-touch bar completes it) — B1 = t −
start, B2 = t − the last touch of the departure side before t; then the side flips and start = t. The leg open at
`end` … is dropped"), `t_pin` :819-832; LEANS_X LX-X2.7 (:1226-1260), including the refusal of (D) "the
harden-anchored time to the far boundary … an outcome of the X2 event class"; scout U2 §1.10, R17; U6 R-17, R-18.

RIVALS: (a) touch by CLOSE — a close at or beyond an edge is a probe; the trades' targets and the scalper's entry
are resting orders that fill on the bar's range. (b) X's `TOUCH_EPS` tolerance (0.60 ATR) — a pivot-machine pin
with no value-area meaning. (c) `b2`, the pure transit — X filed it as a distribution only; `b1` is the filed
traverse X rode as a twin book. (d) time from a swing failure to the far edge — refused: an outcome of the traded
event class. (e) the whole corridor — leaks the holdout into the scalper's own time stop. (f) state INSIDE on every
bar of the leg as the T of record — voids every leg that follows a failed probe, the very case the stop times;
not taken as the record (OD-15) and printed as the twin `strict_inside`. (g) the T-th 1h close after the fill
instead of a 5m count — depends on where in the hour the fill lands.

FAILS-IF: F-TRAV [b], [c], [d] at Stage V; its helper legs [a · <module>] and [e · <book>] in every consuming
suite. Mutations: a typed integer time stop in a copy of a consumer; a holdout leg planted in a copy of the leg
table; the touch test read against `VA(t)`; `T_5m` computed with a typed 12; `T_strict_inside` moved by one in a
copy of `TRAVERSE.json`; a `traverse()` read of a `TRAVERSE.json` copy whose sha is not the certified one.

---------------------------------------------------------------------------------------------------------------
#### D · Stamps (V5)

**L-V.19 THE FUNNEL INSTANTS** — "every funnel instant of every book (base v6, 9/12, the gated books, every arm
below)" (contract :44)

READING: TC11's instant law, mirrored as `instants_of(frame, kind)` in the reader from
`tierc11_stage_r.instants_of` (`scripts/tierc11_stage_r.py:1267 ff.`; `KINDS` :213-216; `NEST_KEY` :258) — the
TC11 module reaches the range layer and is never imported. Per campaign (or order) of a book: **every close of the
book's bar-close lens from its start (the ARM close; the ENTRY close for a book without arming; the trigger close
for an order) through its terminal stamp of record, plus its named events**: `arm`, `entry`, `plus_1r` (intrabar:
the OPEN of its bar) with its close-stamped twin `plus_1r_post_event`, `harvest` (v6's band harvest: a close
event), `bell`, `exit` (a stop or target: the OPEN of its bar; a close event: its close) with `exit_post_event`,
and `as_of_pin` for a row open at the corridor pin (never `exit`). An event the row's own record says happened but
no column stamps HALTs the reader. Rejected armings (tide / d / no_trigger / position_open) are not rows: TC11's
law stamps entered campaigns.

**Who files (OD-7, O-29, O-31).** The instant stamps are Stage V tables. No book builder stamps its own book.
After a book stage files its frames, the READER is run as `scripts/tierc12_va_stamps.py --file-stamps
--stage=TC12-V.stamps.<c|r|s>`; it writes `T12/va/stamps/VA_STAMPS_<book>.parquet` through `put` (L-0.13), merges
its entries into `T12/va/stamps/build_manifest.json` (HALT `STAMPS-MOVED` if an entry it would write exists with
another sha), and its record `progress/TC12-V.stamps.<x>.json` pins each table `{bytes, sha256}` and names in
`depends_on` the records whose frames it read. Every frame is opened after its sha is asserted through
`certified()`. A consumer asserts a stamp table's sha through `certified()` before use.

**`instants_of(frame, kind)`.** `kind` is a dict filed in the manifest per table: `{book, lens, key: [frame
columns after symbol], start_col, end_col, bar_close_lens (default = lens), events: [{name, col, stamp ∈
{"close", "open_of_bar"}, post_event: bool}]}`. The frame holds `symbol`, the key columns and every named column
as int64 ms (null = did not happen). Instants per frame row: every close of `bar_close_lens` from `start_col`
through `end_col` (`instant_kind = "bar_close"`), plus each event (`open_of_bar` events are stamped at the OPEN of
their bar and, if `post_event`, again at its close as `<name>_post_event`), plus `as_of_pin` for a row open at the
corridor pin (never `exit`). Five rules complete the dict; the reader infers nothing else:
1. **Bar closes.** The closes are the `close_ms` of the filed `va_bars_<bar_close_lens>` rows of the row's
   symbol with `start ≤ close_ms ≤ end`; the reader opens no kline file. `start` is the value of `start_col`;
   `end` is the row's terminal stamp, the value of `end_col`. A kind whose `start_col` is null files no
   `bar_close` instant (`tp1d`).
2. **Open rows.** A row is OPEN at the corridor pin iff its terminal stamp is null or its frame flags it
   (`open_at_asof` true, where the frame carries that column; `exit_reason == "corridor_end"`, the tier's one word
   for a position marked at the end of its ride). An open row runs its bar closes through `PIN` and is stamped
   `as_of_pin` at `PIN`; no `exit`, `exit_post_event`, `expiry` or `cancel` instant is filed for it, whatever its
   mark columns hold.
3. **The post-event twin.** An `open_of_bar` event's column already holds the OPEN of its bar; its twin is filed
   at that bar's close, `col + E.LENS_MS[lens]` — no tape is read and nothing is recomputed.
4. **A stamp that differs by row.** An event that is intrabar on some rows and a close event on others (an exit)
   is listed ONCE PER STAMP with the same `col`; the row's own stamp is read from a COMPANION column of the frame
   that the kind names, holding the stamp's word per row: `open_of_bar` (the lineage writes `intrabar_open`,
   `scripts/tierc11_books.py:47-50`, read as the same word) or `close`. Any other value, or a missing companion,
   HALTs. The owner of a frame, who simulated the exit, writes the companion; the reader derives no stamp from an
   exit reason.
5. **`bell`.** On the lineage's frames a row whose `exit_reason` begins `bell` is stamped `bell` at its
   `exit_event_ms` (a close event) and also `exit` there — TC11's law (`scripts/tierc11_stage_r.py:1377-1378`).

**Table key** = `[book, symbol] + kind.key + [instant_kind, instant_ms]`. Columns: those, then per lens ℓ ∈ (1h,
4h, 12h, 1d, 1w) the block of L-V.20 prefixed `<ℓ>_`, and `nest_gap_reason` (str: empty, or the lenses whose nest
fields the gap guard of L-V.21 set NULL at this instant, in ladder order, joined by `|`).

**The books and their kinds** (typed in the reader by child; each row's kind is filed in the manifest):

| child | `<book>` | frame | lens · key · start_col · bar_close_lens | events |
|---|---|---|---|---|
| `.c` | `v6`, `trg912` | `books/v6_ext_campaigns.parquet`, `books/trg912_ext_campaigns.parquet` | 4h · `[entry_ms]` · `arm_close_ms` · 4h | `arm`, `entry` (close); `plus_1r` (`latch_1r_open_ms`, open_of_bar, post); `harvest` (`harvest_close_ms`, close); `bell` and `exit` from `exit_event_ms` by `exit_reason` and `exit_event_stamp` (an intrabar exit: open_of_bar, post); `as_of_pin` from `open_at_asof` |
| `.r` | `P-SFP-VA-1__<arm>` for each RIDDEN arm (`scored`, `tierE__unfiltered`, `tierE__guard_1d`, `tierE__maker_conditioned`, `tierE__x_geometry`, `tierE__x_gaplaw`; the frame is that arm's ride to PIN, so the `strip` rows are covered) | the arm's trade frame | 4h · `[entry_ms]` · `entry_close_ms` · 4h | `entry` (close); `ev_t1` (`ev_t1_ms`, open_of_bar, post); `exit` (stop or T2: open_of_bar, post; time stop, invalidation: close); `as_of_pin` |
| `.r` | `P-SFP-VA-1__tierE__cell_1d` | its trade frame | 1d · as above · 1d | as above |
| `.r` | `tp1d` | `stage_r/tables/TP1D_CAMPAIGNS.parquet`, rows with `exit_reason == "tp"` | 4h · `[entry_ms]` | `ev_tp` (`ev_tp_ms`, open_of_bar, post) ONLY — every other instant of a venue campaign is a v6 instant |
| `.s` | `P-SCALP-3__<arm>` for `scored`, `ladder__touch`, `ladder__deep`, `tierE__panel17`, `tierE__rr_unfiltered`, `tierE__live_edge` (the frame is that arm's ORDER ledger to PIN, misses included) | `stage_s/S_orders_<book>.parquet` | 5m · `[known_at_ms]` · `known_at_ms` · **1h** | `arm` (`known_at_ms`, close); `entry` (the fill: open_of_bar, post); `ev_t1` (post); `exit` (stop or target: open_of_bar, post; a close event: close); `expiry`, `cancel` (close) |

What the table's cells leave unnamed, as the frames' owners declare it (L-C.11, L-R.31, L-S.30) and as the reader
types it — a frame that lacks a named column HALTs the child:

| child · book | frame of record | `end_col` (terminal stamp) | companion stamp of `exit` |
|---|---|---|---|
| `.c` · `v6`, `trg912` | the two campaign frames | `exit_event_ms` (the exit's event stamp) | `exit_event_stamp` |
| `.r` · the P-SFP-VA-1 arms, the 1d cell | the traded rows of `stage_r/sfp/SFP_EVENTS.parquet` with `book == <arm>` | `exit_close_ms` (the close of the exit bar) | `exit_event_stamp` |
| `.r` · `tp1d` | `stage_r/tables/TP1D_CAMPAIGNS.parquet`, `exit_reason == "tp"` | none: no `bar_close`, the one event `ev_tp` | none |
| `.s` · the P-SCALP-3 arms | `stage_s/S_orders_<book>.parquet` | `resolution_close_ms` (the close at which the order's life ended: the exit close of a trade, the expiry or cancel close of a miss; null while open or unresolved at PIN) | `ev_exit_stamp` |

Event columns of a frame are named `ev_<name>_ms` (or the lineage's own names on the v6 frames): the scalper's
order frame carries `ev_entry_ms`, `ev_t1_ms`, `ev_exit_ms`, `ev_expiry_ms`, `ev_cancel_ms` — the OPEN of the bar
for an intrabar event, the close for a close event — and no column named `event_ms`. A derived arm whose instants
are another's is NOT re-stamped: `tierE__maker_assumed` ≡ `P-SFP-VA-1__scored`; `tierE__full_corridor` ≡
`P-SCALP-3__scored`. A gated book (every post-filter of v6) is a key SUBSET of `v6`: it files a key table
`[book, symbol, entry_ms]` (`stage_g/g_book_keys.parquet`; `stage_r/dir/dir_book_keys.parquet` for P-DIR-1's
kept book) and is asserted `⊆`, never re-stamped. A re-ride is a disclosure of counts and diff rows (L-R.5,
L-G.18), never an arm: no stamp table exists for one.
**A closed row; an empty book.** A book whose registration reads CLOSED_BY_PRECONDITION has no arm, no frame and
no stamp table; the child's record is still filed (it certifies the tables that do exist — `tp1d` at `.r`; none
at `.s` if P-SCALP-3 is closed), and the stamps suite's block for each absent book prints `CLOSED-NO-BOOK
<registration id>` (L-0.14). A book whose frame holds no row files no table either (L-0.13's skip-empty law: it is
listed under the manifest's `skipped_empty`), and its block asserts from the frame that it has no instant.
**The shared directory.** `T12/va/stamps/` is written at three records: it is the one member of L-0.9's
`SHARED_DIRS_T`; its `build_manifest.json` is cumulative and re-recorded by each stamps child; its read log is
`READ_SET_<record id>.json`; the helper legs F-KEY, F-DET and F-COLLAR on it are scoped to the tables the records
up to `--stage` name.

SOURCE: TC11 LEANS L-R.5 (:218-223); `research_outputs/tierc11/stage_r/NEST_v6.parquet` (sha `de27be17…cb11`: 9,693
keys per scale_kind; kinds arm 200, bar_close 8,632, entry 200, plus_1r 103, plus_1r_post_event 103, harvest 55,
bell 4, exit 200, exit_post_event 196 — read while drafting) and `NEST_trg912.parquet` (sha `7c5ffe23…3ef9`),
both read through `E.tc11_record`; `scripts/tierc11_stage_r.py:199-201` (`INTRABAR_STAMP`,
`CLOSE_EXIT_PREFIXES`), :1267-1380 (`instants_of`: bar closes from the start through the exit stamp; `as_of_pin`
for a campaign open at the pin; the bell law) and `scripts/tierc11_books.py:47-50` (`exit_event_stamp`) [read
here, as text]; O-29, O-31; OD-7; the sibling readings L-0.10 (the sub-stage table: the three stamps children and
their `depends_on`), L-0.9 (`SHARED_DIRS_T`), L-C.11, L-R.31 and L-S.30 (the frames); scout U3 §1.10, R12.

RIVALS: the whole arming funnel including rejected armings — no filed row law, no named consumer (OPEN TO OPERATOR
2). Entry instants only — the contract says "every funnel instant". A stamp at every lens bar of the corridor —
that is the per-bar table `va_bars_<ℓ>`, which exists anyway. A stamping DOOR run after each book — a module call
where a join of filed rows suffices; the reader, a decision module, does it. Each book stage stamping its own book
into its own directory and record — not taken: O-29 and OD-7 make the instant stamps Stage V tables pinned in
Stage V's records, so that a consumer has one record to assert against. One record
`TC12-V.stamps` for every book — not taken: OD-7 (the books are filed by three stages; three children, each
naming what it read). A `bar_close` at every 5m close of an open order — twelve identical rows per hour; the
vector cannot change between two 1h closes (`bar_close_lens`). A stamp table for a re-ride — no re-ride arm
exists.

FAILS-IF: in the stamps suite (`scripts/tierc12_va_stamps_fixtures.py --stage=<child>`, which imports no door) —
F-NEST-KEYS (child `.c` only): on campaigns entered at or before W and instants ≤ W, the TC12 v6 key set
`(symbol, entry_ms, instant_kind, instant_ms)` equals `NEST_v6.parquet`'s at one scale_kind, and the 9/12 key set
equals `NEST_trg912.parquet`'s after dropping `as_of_pin` rows from TC11's side (a campaign open at TC11's pin
continues in TC12); the gated-subset law for the key tables then on file; and F-NEST-ASOF [<book>] for every table
of the child. Mutations: one filed key dropped; a `plus_1r` stamped at its bar's close; a key added to a copy of a
gated key table; a close-event exit given a post-event twin (the companion stamp ignored); a `bar_close` filed
after the row's terminal stamp; an entry of the shared manifest overwritten with another sha → `STAMPS-MOVED`.

**L-V.20 THE VECTOR AT AN INSTANT** — "carries the VA vector at 1h, 4h, 12h, 1d, 1w" (contract :44-45)

READING: For an instant τ and lens ℓ, `k = asof_index(close_ms_ℓ, τ)` (L-V.8 rule 4). The block of lens ℓ is **the
columns below of row k of the filed table `va_bars_<ℓ>.parquet`, as filed** — TC11's law ("read at the last CLOSED
bar of L at or before the instant") made a pure join of data. `k = −1` → every column NULL and `state =
UNDEFINED`. The block (columns prefixed `<ℓ>_`; the complete list — no other column of the row is carried):

| columns | value |
|---|---|
| `k`, `bar_close_ms`, `stale_ms` | k; `close_ms[k]` — **the member's own bar-close column: `1h_bar_close_ms`, `4h_bar_close_ms`, `12h_bar_close_ms`, `1d_bar_close_ms`, `1w_bar_close_ms`**; `τ − close_ms[k]` (computed by the reader) |
| `state`, `armed_top`, `armed_bottom` | the machine after bar k |
| `pct`, `edge_dist_atr`, `near_side`, `d_vah_atr`, `d_val_atr`, `poc_dist_atr`, `va_age`, `accept_age` | bar k's columns (L-V.16): **the price compared is the lens's own last close `c_ℓ[k]`, judged against `VA(k−1)`, in units of `ATR_ℓ[k]`** |
| `close`, `atr` | `c_ℓ[k]`, `ATR_ℓ[k]` |
| `val_j`, `poc_j`, `vah_j` | the judging profile `VA(k−1)` |
| `val`, `poc`, `vah` | **the profile IN FORCE at τ, `VA(k)`** — the levels any order placed at or after τ and before the next lens close rests on |
| `probe_side`, `probe_t0_close_ms`, `probe_edge` | the pending probe, if the state is PROBING |
| the nest columns of L-V.21 | bar k's own |
| `L`, `l_label` | the lookback and its label |

No instant price enters the vector of record, and the reader contains no comparison of a price with a level: it
joins. **The live formulas** — the one law for a consumer that holds a price `p(τ)` which is not a close of lens ℓ
(the scalper's 5m close against the 1h and 4h value areas) — are computed by that consumer on the block's filed
columns: `px_pct = PCT·(p − val)/(vah − val)`; `px_d_vah_atr = (p − vah)/atr`; `px_d_val_atr = (p − val)/atr`;
`px_poc_atr = (p − poc)/atr` — the price against the IN-FORCE profile `VA(k)` and `ATR[k]`. When
`τ == bar_close_ms` the price is the lens close itself and lies inside the window of the profile it is measured
against; what a consumer does at such instants is its own reading.

Consequences stated for the reader: at a lens coarser than the instant's clock the judged columns are those of the
last lens close and are stale by up to one lens bar (a week at 1w); `stale_ms` says by how much. The filed value is
the value of record for every consumer (L-V.24).

SOURCE: `scripts/tierc11_nest.py` `_lens_arrays` :1079-1107 (`k = C.asof_index(tape, inst)`; `pct` =
`view["pct"][ks]`; `atr_L` = `tape.atr[ks]`), `nest_at` :1158-1183; TC11 LEANS L-R.5 (:224-232); O-14, O-16 (a),
O-29 ("a consumer compares a price with a filed LEVEL … but never re-derives a lens STATE or EVENT"); the sibling
readings L-0.22 and L-0.28; scout U2 R15, U6 §1.10.

RIVALS: the instant's own price against `VA(k)` as the vector of record — at an instant that IS a lens close it
measures the close against a profile containing it, and state and `pct` stop being coherent; it is the live
formula, by name, for the one consumer that needs it. The instant's price against `VA(k−1)` — a stale profile for
an order that rests after τ. Interpolating a forming higher-lens bar — a look-ahead. A module call per instant —
forbidden: O-29.

FAILS-IF: F-NEST-ASOF [a]-[c] at Stage V and F-NEST-ASOF [<book>] in the stamps suite; mutations: listed there.

**L-V.21 BOUNDARY COINCIDENCE** — "BOUNDARY COINCIDENCE (an edge of L within 0.25 ATR_L of an edge of L+1)
["nest"]" (contract :45-46)

READING: The ladder is `1h → 4h → 12h → 1d → 1w` (TC11's `LADDER`, `scripts/tierc11_nest.py:101`); L+1 of 1w is
none. DOOR 1 computes the coincidence PER BAR of the lower lens and files it in `va_bars_<ℓ>` — these columns are
the nest table of Stage V. For bar t of lens ℓ with L+1 lens U: `up_k[t] = asof_index(close_ms_U, close_ms_ℓ[t])`
(the last U bar closed at or before bar t's close), and on the IN-FORCE profiles `VA_ℓ(t)` and `VA_U(up_k[t])`
with `ATR_ℓ[t]` — the ATR of the LOWER lens at its own bar:

- `up_k`, `up_bar_close_ms` — the L+1 bar read;
- four pair flags, inclusive: `coin_vah_vah = abs(VAH_ℓ − VAH_U) ≤ F·ATR_ℓ`; `coin_vah_val = abs(VAH_ℓ − VAL_U) ≤
  F·ATR_ℓ`; `coin_val_vah`; `coin_val_val`;
- two side flags: `coin_vah = coin_vah_vah OR coin_vah_val`; `coin_val = coin_val_vah OR coin_val_val` (TC11's
  rule: a boundary of L against EITHER boundary of L+1, all four pairings);
- `coin_min_atr` = the smallest of the four distances ÷ `ATR_ℓ`.

The seven coincidence fields are NULL (not False) when either profile is invalid or the lens has no L+1. The state
of either lens does not enter the flags; state is its own column. For the five home assets every rung exists (1d
against the borrowed 1w block, L-V.5); the 1w block's fields are NULL.
**At an instant τ** the block carries bar k's nest columns (L-V.20). They are the coincidence standing at τ
whenever no L+1 bar has closed in `(close_ms_ℓ[k], τ]` — always, on nested gap-free tapes, because every L+1
close is a lower-lens close. The reader checks it per instant, `asof_index(close_ms_U, τ) == up_k[k]`; where a
gap in the lower tape breaks it, the block's seven fields are set NULL, the lens is named in the row's
`nest_gap_reason` (L-V.19) and the instant is counted (`n_nest_gap_instants`, printed; never a stale flag).
`va_coincidence` is also what DOOR 2 calls for the event-edge test of the lens-above partition (L-R.27): the
event's frozen edge handed in as both lower edges, against the in-force edges of the lens above, with the level
and the unit that reading defines.

SOURCE: `scripts/tierc11_nest.py` `within` / `coin_flags` :1016-1051 ("a LIVE boundary of L within frac x ATR_L
of EITHER live boundary of L+1 (all four pairings, inclusive)"), `COIN_FRAC` :108; TC11 LEANS L-R.5 (:233-235);
contract :45-46, :135; X's same-lens VA-vs-pivot coincidence (`tc11x_va.py:1069-1070`) is a different object; the
sibling stage table (Stage V files "the nest table").

RIVALS: ATR of L+1 — the contract says ATR_L. Same-side pairs only (VAH–VAH, VAL–VAL) — TC11's law is all four.
Judging profiles `VA(k−1)` — coincidence is a relation between two levels standing at τ, not a judgement of a
close. The POC as an "edge" — not an edge. Recomputing the flags per instant in each consumer — one law written in
several places; DOOR 1 computes it once and files it. `analytics.nesting.va_nesting` — window-scale overlap
fractions, another object.

FAILS-IF: F-NEST-ASOF [a], [c] (flags recomputed by the fixture from the two raw windows); mutations: the
threshold taken in `ATR_U`; strict `<`; the L+1 profile taken at `up_k + 1` (NULL where it passes the tape end).

**L-V.22 THE TWELVE NEW ASSETS** — "Twelve new assets: 1h/4h/1d, Tier-E" (contract :46)

READING: For each of the twelve (the env's `UNSEEN12`, L-D), the series, the TPO twin, the machine and the
per-bar columns are built at 1h, 4h and 1d with the SAME `L_ℓ` as the home assets, each row labelled
`l_label = "CLASSIC5-fitted L (pooled tuning head); not fitted on this asset"`, and every row collared Tier-E
(`tier = "TIER-E"`, `selection_not_a_result = "a SELECTION, not a result"`, `gates = "nothing"`). Their 12h and 1w
blocks are NULL, and their rows carry `panel = "UNSEEN12"`. Coincidence follows TC11 without re-linking the
ladder: `1h` against `4h` is defined; the `4h` block's fields (its L+1 is 12h) and the `1d` block's fields (its L+1
is 1w) are NULL. A tape shorter than `L_ℓ + 1` bars is UNDEFINED throughout and listed. The feasibility words,
the licence and the traverse are CLASSIC5 quantities: no twelve-asset row enters the traverse pool, the mirror,
DOOR 2's tables or any registered construction; they appear only in views the contract marks Tier-E (":84 the
full-corridor and 17-asset views Tier-E").

SOURCE: contract :18-20, :46, :84; O-8; TC11 LEANS L-R.5 (:237), `tierc11_nest.py` `nest_at` docstring ("For the
twelve, the 12h and 1w columns (and the 4h / 1d coincidence, whose L+1 is NA) are NA"); scout U2 R23.

RIVALS: a per-asset L for the twelve — needs a pivot run and X's per-asset twin scatters by a factor of two
(LEANS_X :1599-1600). Re-linking 4h → 1d for the twelve — not TC11's law. Pooling the twelve into the traverse —
changes the time stop of the registered rows.

FAILS-IF: F-VA-PINS [f]: every twelve-asset row carries the collar and the label; its 12h/1w blocks are NULL; no
twelve-asset leg is in `traverse_legs.parquet`; mutation: a twelve-asset leg appended to a copy of the leg table.

---------------------------------------------------------------------------------------------------------------
#### E · Null, outputs, compute

**L-V.23 THE VOLUME NULL, AND WHAT ELSE DOOR 2 BUILDS** — no contract line — X's value-area null of record, built
because L-R.29 prints it beside the contract's gaps+order null ("null gaps+order (R10)", contract :79, is
L-R.29's phrase)

READING: The value area's null OF RECORD in the estate is X's `tr_tercile_lblock`: a true-range-tercile-stratified
L-block volume PERMUTATION with random phase; prices untouched. `value_area.null_volume(volume=, true_range=,
lookback=, rng=)` mirrors it exactly: draw the phase `φ = rng.integers(0, lookback)`; blocks
`[0, φ), [φ, φ + lookback), …`; inside each block rank the bars by true range with a stable sort, stratum
`= len(TR_STRATA)·rank // m` for a block of m bars; permute the volumes inside each non-empty stratum with
`rng.permutation`, blocks then strata in order. `true_range` is `engine.indicators.true_range(h, l, c)`, computed
by DOOR 2 and handed in. DOOR 2 builds the stream `default_rng([SEED + draw, crc32("<asset>|<lens>|va")])` with
`SEED` = TC12's seed (contract :4; `E.SEED`) and `draw` running over the null draw count of L-V.4.
**Who runs it: DOOR 2, record `TC12-V.trades` (OD-2).** A draw needs the module (series → machine on the permuted
volume), and `scripts/tierc12_va_trades.py` is the only place the V2 machine is run on permuted volume. Per cell —
lens ∈ {4h, 1d} × the five home assets — and per draw: the tape is the W tape (`E.load_asof_at(stem, lens, W)`),
the window of the tables the null serves, so that no strip bar enters a draw (O-9); prices are untouched;
`va_series` is rebuilt on the permuted volume with the cell's pinned `L`, bins and value-area share; the ATR is
DOOR 2's own full-float `engine.indicators.atr` on that tape (L-V.7); `va_machine` runs at (N, M, K). The events
are filed in `va/trades/va_null_events.parquet`: the L-V.14 schema plus `draw`, `phase`, `perm_sha`.
**What else DOOR 2 builds, by L-R's definitions** (the laws are L-R.26..L-R.29; this section carries the builder
and the files):
- **The gaps+order@va_regime schedule and its box events** (L-R.29). The real box set is read through
  `regimes(asof_close_ms=W)` and `bars(lens, asof_close_ms=W)`: the regimes are cut at W — regimes with
  `r0_close_ms ≤ W` are kept; a kept regime whose `die_close_ms > W` or is null is the alive one (`life = n −
  r0`, censored) and its `die_*`, `end_*`, `n_bars` are not read; regimes with `r0_close_ms > W` are dropped. The
  schedule is the mirror L-R.29 defines; the machine on a box is `value_area.va_machine` with (N, M, K) on arrays
  held constant at each box's edges — the one V2 machine; no mirror of the pivot's box machine is written
  anywhere. Files: `va/trades/NULL_BOXES_VA.parquet`, key `[lens, asset, draw, box]`: `src_rid`, `confirm_i`,
  `life`, `censored`, `bot`, `top`, `u`, `lead_gap_swapped`, `identity_perm`; and
  `va/trades/va_null_go_events.parquet`: the L-V.14 schema plus `draw`, `box`.
- **The Tier-E two-trades tables** (L-R.26-L-R.29): `TWO_TRADES_EVENTS.parquet` (key `[lens, asset, trade, side,
  anchor_i, i]`), `TWO_TRADES_VA.parquet`, `TWO_TRADES_VA_UNCOND.parquet`, `TWO_TRADES_BASE.parquet`,
  `TWO_TRADES_NULL.parquet`, `TWO_TRADES_NULL_DRAWS.parquet`, all under `va/trades/`; every row carries `l_label`,
  and the rows of the tables that carry the lens-above cell carry `u_lookback_label` (L-V.5). The stage document
  of record `va/trades/TWO_TRADES.md` prints every grid of the family whole; the build report points to it.
DOOR 2 reads the filed Stage V tables through the reader (each sha asserted through `certified()`), the tapes
through `E`, and — for the 1d events' lens above — the five `1w_` columns of L-V.5 and no other. No table it files
holds a `TRADE_COLS_T` column, a gate, an order or a score; every one is collared Tier-E. The percentile those
tables print is mid-rank and is "a DESCRIPTION of where the real value sits among the draws, never a p-value".
Nowhere else is a null used: no registered verdict, no licence, no traverse, no stamp. Every null row names its
generator (L-R.29's `null_variant`); the volume null is the VA null of record and is named as such on every row
that uses it.

SOURCE: `tc11x_va.py` `null_rng` :1125-1127, `null_volume` :1130-1169 (`terc[order] = (3 * np.arange(m)) // m`,
:1161), `NULL_OF_RECORD` :236; LEANS_X LX-X3.13 (:1793-1809); AP-11 item 11; X's filed draws
`x_rec/tierc11x/null/null_va.parquet` (`rng`, `draw_info` = `"phase=<φ> shift=-1 perm_sha=<sha256 of the int64
index permutation>"`, read while drafting); `scripts/tierc10_null.py:239` (`real_box_set`), :286 (`draw_rng`),
:293 (`schedule`), :335 (`box_bounds`), :356 (`static_box_machine`) [read here, as text; never imported]; O-9,
O-29; OD-2; the sibling readings L-R.26..L-R.29 (the definitions) and L-0.22 (a door's obligations); scout U2
R18, H16.

RIVALS: re-use X's seed for TC12's draws — reproduces X's percentiles on a longer tape that X never saw; TC12's
seed is the contract's. The per-window permutation — rejected by X (it jitters the VA tenfold). gaps+order
relabelled onto a volume permutation — two different questions (`tc11x_va.py:195-197`). A decision module running
the draws or the box machine (a mirror of the pivot's static machine in a Stage R builder) — forbidden:
O-29, OD-2 (a second V2 machine outside the wall). The draws on the tape to the corridor pin — pools strip bars
into a table whose window ends at W (O-9). DOOR 2's machine fed the 6-dp filed ATR — a margin acceptance could
flip at an exact edge; the call chain is DOOR 1's, at full float.

FAILS-IF: F-VA-NULL, hosted at `TC12-V.trades`: [a MIRROR] with X's seed (`PINS_X.json` key `seed`) on the tape cut
at W, the mirrored generator reproduces the filed `phase` and `perm_sha` of every `tr_tercile_lblock` draw of X's
20 cells; [b IDENTITY] handed the identity permutation, DOOR 2's series-and-machine pass on the W tape reproduces
the filed `va_events` rows known at or before W of the ten cells (`events(asof_close_ms=W)`) at the write law, and
no row of `va_null_events`, `va_null_go_events` or `NULL_BOXES_VA` lies past W; [c FLOW] the null draw count bent
at its door moves the number of draws filed per cell. Mutations: the draw seed shifted by one (X's own plant) →
[a]; the volume column shifted one bar in DOOR 2's loader → [b]; the tape cut at the corridor pin → [b]; a typed
draw count in a copy of DOOR 2 → [c] `PIN-NOT-READ`. The fixtures of the tables DOOR 2 builds by L-R's
definitions (F-RETEST-MIRROR, F-TWO, F-TWO-MIRROR, F-NULL-MIRROR [a], [c], [d], with the `NULL-STRIP` plant) are
defined in L-R.26..L-R.29 and hosted in the same invocation.

**L-V.24 OUTPUTS, PRECISION AND THE COMPUTE PLAN** — "Stage V pins and the traverse table · the VA stack whole"
(contract :128)

READING: Stage `TC12-V` runs before any book exists. It files one parent record and four dotted children, every
one BLOCKING (L-0.10's sub-stage table):

| record | `depends_on` | what runs | what it files |
|---|---|---|---|
| `TC12-V` | — (its place in the resume order) | DOOR 1; `tierc12_va_fixtures.py --stage=TC12-V` | `T12/va/` (items 1-7 below) and the code of L-V.2 |
| `TC12-V.trades` | `TC12-V` | DOOR 2; `tierc12_va_fixtures.py --stage=TC12-V.trades` | `T12/va/trades/**` (item 8) |
| `TC12-V.stamps.c` | `TC12-V`, `TC12-C` | the reader's `--file-stamps`; `tierc12_va_stamps_fixtures.py --stage=TC12-V.stamps.c` | `va/stamps/VA_STAMPS_{v6,trg912}.parquet` (item 9) |
| `TC12-V.stamps.r` | `TC12-R.sfp`, `TC12-R.tables` | likewise, `--stage=TC12-V.stamps.r` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage R's books |
| `TC12-V.stamps.s` | `TC12-S` | likewise, `--stage=TC12-V.stamps.s` | `va/stamps/VA_STAMPS_<book>.parquet` for Stage S's books |

One commit per record. The children `.stamps.r` and `.stamps.s` close after Stages R and S by design: a later
stage that needs Stage V starts on the RECORD `TC12-V` and on the children that precede it in the resume order,
never on the completion of the whole stage (L-0.10). The stage `TC12-V` is COMPLETE-VERIFIED iff the parent and
all four children are.

**The filed inventory — everything a consumer reads under the file-only wall.** Every file below is pinned
`{bytes, sha256}` in the record named and asserted through `certified()` before any use. Parquet: 6 dp at write,
the nine as-of stamps, the collar (no parquet here is registered; the one registered record is `VA_MIRROR.json`).
1. **`va/VA_PINS.json`** (DOOR 1 · `TC12-V`) — `by_lens.<ℓ>` for ℓ ∈ {1h, 4h, 12h, 1d, 1w}: `{L_bars, source
   {path, key, sha256}, label, source_lens}`; `laws` {`accept_n`, `margin_atr`, `ret_k`, `nest_frac`, `bins`,
   `value_area`, `atr_len`, `floor_n`, `null_draws`, each with its source}. Read by both doors and the pin
   register.
2. **`va/va_bars_<ℓ>.parquet`**, ℓ ∈ {1h, 4h, 12h, 1d, 1w} (DOOR 1 · `TC12-V`) — key `[asset, open_ms]`; one row
   per bar, KNOWN AT `close_ms`:

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

   Read through the reader (`bars`, `stamp`) by L-R (P-DIR-1: `state`, `close_ms`; printed `pct`,
   `edge_dist_atr`, `accept_age`, `armed_*`; the chop tables; the 1d venue: `state`, `val`, `vah`, `atr`), by L-S
   (1h: `close_ms`, `state`, `val`, `poc`, `vah`, `atr`, `va_age`, and the count of `inside_frozen_only`; 4h:
   `close_ms`, `state`), by DOOR 2 and by the stamps.
3. **`va/va_events.parquet`** (DOOR 1 · `TC12-V`) — key `[lens, asset, kind, side, i, t0]`; one row per event,
   KNOWN AT `known_close_ms`; no field depends on a bar after `i`; the fields of L-V.14, which hold no
   `end_kind` and no `end_i`. Read by L-R (swing-failure rows; acceptance rows for invalidation and its `E`), by
   L-S (1h acceptance rows: `lens`, `kind`, `side`, `known_close_ms`, `by`, `bars_out`, `E`) and by DOOR 2.
4. **`va/va_regimes.parquet`** (DOOR 1 · `TC12-V`) — key `[lens, asset, rid]`: `r0`, `r0_close_ms`,
   `start_kind`, `die_i`, `die_close_ms`, `end_side`, `end_by`, `n_bars`. A SUMMARY table, not an as-of table
   (L-V.14); read only as `regimes(asof_close_ms=B)`.
5. **`va/traverse_legs.parquet`** (key `[lens, asset, rid, leg_seq]`) and **`va/TRAVERSE.json`**, the traverse
   pin record (DOOR 1 · `TC12-V`), with the keys of L-V.18. Read only through the reader's `traverse(name)`.
6. **`va/VA_MIRROR.json`** (DOOR 1 · `TC12-V`; a REGISTERED record, no collar), with the keys of L-V.17 item 7.
   Read by the reader's `licence`, by the scorer's precondition evaluator and by the report.
7. **`va/va_stack.parquet`** (key `[asset, lens, era]`), `va/STAGE_V.md`, `va/build_manifest.json` (with
   `x_sources`), `va/READ_SET.json`, `va/FIXTURES_STAGE_V.txt` (DOOR 1 · `TC12-V`). `va_stack` is THE VA STACK,
   whole — `era` ∈ {tuning (`close_ms ≤ ERA_CUT`), holdout (`ERA_CUT < close_ms ≤ W`), ALL (`close_ms ≤ W`),
   strip (`W < close_ms ≤ PIN`, never pooled, O-9)} — per cell: bars; bars per state; every event counter of
   L-V.13-14; regimes; the median value-area width in ATR; the TPO medians and counters of L-V.6; the share of
   bars with each nest flag; the counted cases of L-V.13.
8. **`va/trades/`** (DOOR 2 · `TC12-V.trades`): `va_null_events.parquet`, `NULL_BOXES_VA.parquet`,
   `va_null_go_events.parquet`, `TWO_TRADES_EVENTS.parquet`, `TWO_TRADES_VA.parquet`,
   `TWO_TRADES_VA_UNCOND.parquet`, `TWO_TRADES_BASE.parquet`, `TWO_TRADES_NULL.parquet`,
   `TWO_TRADES_NULL_DRAWS.parquet` (keys and columns: L-V.23 and L-R.26..L-R.29); `TWO_TRADES.md` (the stage
   document of record: every grid whole), `build_manifest.json`, `READ_SET.json`, `FIXTURES_VA_TRADES.txt`. Read
   by the report (pointers) and by nobody else.
9. **`va/stamps/VA_STAMPS_<book>.parquet`** (the reader · `TC12-V.stamps.c/.r/.s`; L-V.19), with the cumulative
   `va/stamps/build_manifest.json`, `READ_SET_<record id>.json` and one transcript per child. The block of lens
   ℓ, prefixed `<ℓ>_`: `k`, `bar_close_ms`, `stale_ms`, `state`, `armed_top`, `armed_bottom`, `pct`,
   `edge_dist_atr`, `near_side`, `d_vah_atr`, `d_val_atr`, `poc_dist_atr`, `va_age`, `accept_age`, `close`,
   `atr`, `val_j`, `poc_j`, `vah_j`, `val`, `poc`, `vah`, `probe_side`, `probe_t0_close_ms`, `probe_edge`, the
   nest columns, `L`, `l_label`. Read by L-R.4 (the `entry` rows of `v6`), L-L.16 (the `entry` rows of `v6` and
   `trg912`) and the report.

**The table law.** Every parquet is written through L-0.13's `put` — the 6-dp table writer: declared total key,
floats rounded at write, the nine as-of stamps, the collar on every table that is not on `REGISTERED_TABLES_T`,
which is every parquet here; an empty frame is not written and is listed under the manifest's `skipped_empty`.
DOOR 1's tables and the stamp tables read past W and are stamped with the corridor pin; a table of DOOR 2 whose
rows end at W is stamped with the score edge, and one that also counts the strip with the pin (L-0.13's rule).
Neither door, nor the reader, calls `.to_parquet` or writes under `regbooks/`.
**What the build report quotes** (L-X.28): its feasibility-mirror block from `VA_MIRROR.json`; its "Stage V pins
and the traverse table" from `VA_PINS.json` and `TRAVERSE.json`, the strict-INSIDE twin included; its "VA stack
whole" from `va_stack.parquet`, every cell, and nothing else. The two-trades grids are printed whole in
`va/trades/TWO_TRADES.md`, and the report carries one pointer row per grid (path, sha, cell count).
**Precision.** Inside a door everything is computed at full float and rounded at write only. Outside the doors
THE FILED VALUE IS THE VALUE OF RECORD: a consumer reads `state`, the flags, the events and the columns as filed and
never re-derives a state, an event or an inside/outside flag from filed levels (scout U2 H7); a consumer that
needs a LEVEL — an order at an edge, a target at the POC, a stop beyond `extreme` — uses the filed 6-dp value AS
the level. The doors and the consumers therefore agree on every state by construction, and a level differs from
its full-float value by at most half a unit of the sixth decimal place.
**Compute.** DOOR 1 — 61 cells: 5 home assets × 5 lenses + 12 × 3. Per cell: two series passes (volume, TPO), one
machine pass per series, the columns, the traverse, the nest columns. One `spawn` worker per cell, each arming the
TC12 env before any I/O; at most 6 workers while the 1-minute load is below 10, else 2 (O-5); results merged in
fixed (lens, panel-order) key order before any write, each worker returning its read set with its result. X's
build of record did 20 cells — each with all of X's series twins, event variants and nulls at 20 draws — in 6m07s
on 4 workers (`x_rec/tierc11x/progress/X3.json` → `compute.build_of_record`: `workers 4`, `cells 20`,
`wall "6m07s"`); DOOR 1's work per cell is a small fraction of that, so the full build is a matter of minutes.
DOOR 2 — the ten cells its tables need (five home assets × 4h, 1d): per cell and draw, one volume series pass and
one machine pass for the volume null, one machine pass on constant arrays per scheduled box for gaps+order, then
the scans and statistics of L-R.26..L-R.29; one `spawn` worker per cell under the same cap. The stamps children —
one process each, no pool: a stamp is one `searchsorted` per (asset, lens) over a book's instants. Stage V's
suite — its cut-tape legs (F-VA-ASOF [d], F-NEST-ASOF [a]) rebuild one asset's lenses per cut, under the same cap,
one fixture subprocess at a time. The scalper's 5m clock reads the 1h and 4h tables by as-of; **nothing is
profiled at 5m**. Worker count and load go to `progress/` only, never into an artifact.

SOURCE: O-1, O-5, O-6, O-9, O-29, O-31; OD-2, OD-7, OD-18; `tierc2_baseline.py:155-188` (the table law); TC11
BOOKS precision law (scout U3 §1.5: "flags are computed at full precision BEFORE rounding"); `progress/X3.json`
`compute`; scout U2 H7; contract :126-128 (the report's blocks); the sibling readings L-0.10 (the sub-stage
table, the resume order, parent and child records), L-0.9 (one manifest and one writer per directory;
`SHARED_DIRS_T`), L-0.13 (`put`; `READ_SET.json`), L-0.15 (grids whole; a grid printed whole in its stage
document may be pointed to), L-0.16 (the collar; registered tables) and L-X.28 (the report's whole-versus-pointed
map).

RIVALS: consumers re-derive states from 6-dp levels — flips exact-edge cases (H7). A full-float sidecar, or a
decision module asking a door for arrays — a second copy of record, or a module importing a door: forbidden
(O-29). A 5m value area — not in the contract. One subdirectory of stamps per child — not taken: OD-7's path is
`va/stamps/VA_STAMPS_<book>.parquet`, so the directory is shared and its manifest cumulative. The stamp tables
recorded by the parent `TC12-V` — impossible: no book exists when it closes.

FAILS-IF: F-STATE [f ROUND-TRAP]: on a synthetic tape whose close exceeds the full-float VAH but equals its 6-dp
rounding, the filed `state` must be PROBING_ABOVE (DOOR 1's full-float judgement) and the reader's stamp must
return that filed state; mutation: a reader copy that recomputes `state` from `close`, `val_j`, `vah_j` reads
INSIDE and must turn the leg RED. F-DET, F-KEY and F-COLLAR per directory (`va`, `va/trades`, and — scoped per
child — `va/stamps`) and F-GRID on `va_stack` and on the `TWO_TRADES_*` family are L-0's helper legs, run by this
section's suites; L-0's F-RESUME holds the five records and their `depends_on`.

---------------------------------------------------------------------------------------------------------------
#### F · The fixture roll of this section

**Common law** (L-0.14; X's LX-F.1). A leg is one `prove` call and one transcript block, with the block id
`F-<NAME> [<leg>]` or `F-<NAME> [<leg> · <instance>]`; every leg prints `FAILS IF`; the BREAK plants run first,
one at a time, inside production or on a copy, and each must be caught by its NAMED detector — a plant not caught
makes the fixture VOID and RED; truncated-tape legs build fresh arrays (no memo); as-of legs hold L, N, M, K, F and
T at their filed values and say they do not test them. A leg that cannot run is NOT RUN, never PASS. No leg makes
a network call.
**Fixture randomness.** Every stream is `numpy.random.default_rng([SEED, crc32("<suite tag>|<block id>")])`,
`SEED` = the tier seed (contract :4; `E.SEED`), `<suite tag>` = `va` for `tierc12_va_fixtures.py` and `va_stamps`
for `tierc12_va_stamps_fixtures.py`. Each seeded leg states its count below — where X or TC11 filed a count for
the leg it mirrors, that count, read from the named source — and prints it in its transcript header.
**Hand samples** follow L-0.14's one law: categories first; a category with no member prints `NONE-EXISTS
<category>`, asserts from the population that its count is zero, and its slot is FILLED by the next unchosen row
in key order; a short population is verified whole and printed `ONLY <n> EXIST (contract count <k>)`; no
hand-sample leg is RED or VOID on the size or composition of a population — only a mismatch between the fixture's
derivation and production is RED.
**Reads.** A Stage V suite reads the tables of its own record through the reader with `root=` (the record does
not exist yet; the sha is asserted against the directory's manifest); every other read of a Stage V table, in any
suite of any stage, goes through `certified()`.
**Hosting** — one transcript per record; a suite serving several records takes `--stage=<record id>`:

| invocation | record | transcript | hosts |
|---|---|---|---|
| `tierc12_va_fixtures.py --stage=TC12-V` | `TC12-V` | `va/FIXTURES_STAGE_V.txt` | F-VA-RAW, F-VA-ASOF, F-STATE, F-STATE-X, F-VA-MIRROR, F-TRAV [b], [c], [d], F-TRAV [a · <own module>], F-VA-PINS [a]-[d], [f], F-NEST-ASOF [a], [b], [c] (seeded instants), F-KEY / F-DET / F-COLLAR [va], F-GRID [va_stack] |
| `tierc12_va_fixtures.py --stage=TC12-V.trades` | `TC12-V.trades` | `va/trades/FIXTURES_VA_TRADES.txt` | F-VA-NULL, F-RETEST-MIRROR, F-TWO, F-TWO-MIRROR, F-NULL-MIRROR [a], [c], [d], F-GRID [TWO_TRADES_*], F-KEY / F-DET / F-COLLAR [va/trades] |
| `tierc12_va_stamps_fixtures.py --stage=TC12-V.stamps.<c|r|s>` | that child | `va/stamps/FIXTURES_STAMPS_TC12-V.stamps.<c|r|s>.txt` | F-NEST-KEYS (`.c` only), F-NEST-ASOF [<book>], scoped F-KEY / F-DET / F-COLLAR [va/stamps] |

F-RETEST-MIRROR, F-TWO, F-TWO-MIRROR and F-NULL-MIRROR are DEFINED in L-R.26..L-R.29 and hosted here, because
only this suite may import a door. Stage V's transcripts never enumerate a later stage's modules or tables.
**Helper legs** (in `tierc12_fx.py`, like F-KEY): F-TRAV [a · <module>], F-TRAV [e · <book>] and F-VA-PINS
[e · <registration>]. Stage V runs F-TRAV [a] on its own files only (`analytics/value_area.py`, the two doors, the
reader). Each consuming stage's suite runs one instance per builder, per range book and per registration — at
TC12-G: F-VA-PINS [e · P-ADM-1], [e · P-BRD-1]; at TC12-R.dir: F-VA-PINS [e · P-DIR-1]; at TC12-R.sfp: F-TRAV
[a · tierc12_stage_r_sfp], [a · tierc12_rangewalk], [e · <each ridden arm>], F-VA-PINS [e · P-SFP-VA-1]; at
TC12-S: F-TRAV [a · tierc12_scalp], [e · <each arm>], F-VA-PINS [e · P-SCALP-3] — and F-TYPED-TOTAL at TC12-FIX
fails if a range book has no GREEN F-TRAV [e · …] instance. A real-book leg whose registration reads
CLOSED_BY_PRECONDITION prints `CLOSED-NO-BOOK <registration id>` and asserts the STATUS record (L-0.14).

**F-VA-RAW** (contract :115-116) — at `TC12-V`
- `[a THREE-WINDOWS]` (the contract's count, :115): one per lens 1h, 4h, 1d, eras alternating tuning / holdout /
  tuning, asset and bar drawn from the leg's stream (X's form, `tc11x_va_fixtures.py:310-323`). Production's
  (POC, VAL, VAH) == `analytics.profile.volume_profile` on the RAW snapshot slice read by explicit path == the
  fixture's own pure-Python loop, exactly; production's histogram == the house's bit for bit and within X's 1e-12
  relative of the loop's (`tc11x_va_fixtures.py:348`).
- `[b EQ]`: the module == the house function on the whole BTCUSDT 1h tape and on a seeded sample of every one of
  the 61 cells — n per cell = X's `sample_ts` default `k` (`x_rec/scripts/tc11x_va_fixtures.py:397`, read by
  `ast`; on file 200), every window where the tape holds fewer; and two different `block` sizes give byte-equal
  series.
- `[c SERIES-ANCHOR]` compares the FILED rows: `val, poc, vah, val_edge, vah_edge, tpo_*` of `va_bars_<ℓ>` at
  every row closing ≤ `W` of X's 20 cells == X's filed `va_series_<ℓ>` row `i` (joined on `(asset, i)`, `open_ms`
  and `close_ms` equal), and the constant `L` column agrees.
- `[d TPO]`: TPO rows == a per-window `searchsorted` count, on seeded windows — n = the count X handed its own
  TPO leg (`x_rec/scripts/tc11x_va_fixtures.py:424`, read by `ast`; on file 60, ETHUSDT 4h, as X ran it) — and on
  one constructed window holding a zero-volume flat bar (it must add one count to one row, and nothing to the
  volume histogram).
- FAILS IF: any level, histogram or filed value differs. PLANTS: the volume column shifted by one bar inside
  DOOR 1's loader — must FAIL on EACH of the three windows (the contract's plant) → [a]; every interior edge
  nudged one ulp inside the core → [b]; a block size made to truncate the last block → [b]; the lookback of one
  lens moved by one bar in a copy of `VA_PINS.json` → [c]; the in-force block filed one row late in a copy of a
  table → [c]; the TPO row index taken `side="left"` → [d]; zero-volume bars dropped from the TPO count → [d].

**F-VA-ASOF** (contract :114-115) — at `TC12-V`. Stage V's suite owns PREFIX IDENTITY for the whole tier (OD-2): a
filed row at bar k equals a door rebuild on tapes cut at `close_k`. No suite outside Stage V imports or spawns a
door; every later as-of leg cuts the FILED tables through the reader (`bars(lens, asof_close_ms=c)`,
`events(asof_close_ms=c)`, `regimes(asof_close_ms=c)`) and the tapes through `E.load_asof_at`, re-runs its own
production function, and prints the fixed line `leans on F-VA-ASOF [d]: a filed row at bar k equals a door rebuild
on tapes cut at close_k`.
- `[a PREFIX]`: on seeded cuts — n per cell = X's `asof_cuts` default `k`
  (`x_rec/scripts/tc11x_va_fixtures.py:491`, read by `ast`; on file 5, which on X's 20 cells is its filed "100
  seeded cuts", `x_rec/tierc11x/va/FIXTURES_X3.txt:44`), over all 61 cells — `VA(t)` from a FRESH tape cut after
  bar t (`E.load_asof_at(stem, lens, close_ms[t])`) == the full tape's `VA(t)`, exactly.
- `[b ALIGNMENT]`: the frame's `open_time` strictly increases and equals the tape's `open_ms` row for row, and
  production's (open, volume) pairs == the raw file's, on every cell.
- `[c JUDGING-FRAME]`: every L-V.16 column and every probe's E recomputed by the fixture from the house profile
  of bars `t−L .. t−1`; exact.
- `[d FILED-ROW PREFIX]`: for every cut `c` in `CUTS_V` = the seeded cuts of [a] ∪ {for the first acceptance and
  the first swing failure of each (cell, era): the closes of bars `i − 1` and `i`} ∪ {`ERA_CUT`} ∪ {`W`}: DOOR 1's
  tables rebuilt on tapes cut at `c` (fresh arrays, `E.load_asof_at(stem, lens, c)`; 1d and 1w re-derived from the
  cut 4h by Stage D's law — L-D.8's, written out in the fixture's own loop) equal the FILED tables restricted to
  `c` — every column of every `va_bars_<ℓ>` row with `close_ms ≤ c`, every `va_events` row with
  `known_close_ms ≤ c`, and `regimes(asof_close_ms=c)` — at the write law. Scope of a rebuild: for a cut drawn for a cell, that cell's ASSET with every lens it carries (the nest
  columns read the lens above); for `ERA_CUT` and `W`, every asset. "Every column" is every declared column — the
  nine as-of stamps and the collar name the build, not the bar, and are not compared. Both regime tables are read
  through the bounded form, which nulls the later facts of a regime alive at `c`.
- `[e IDENTITY]` on every row of every `va_bars_<ℓ>`: `(val_j, poc_j, vah_j)[t] == (val, poc, vah)[t−1]` exactly,
  and `atr[t] ==` Round6 of the fixture's own Wilder loop at `t`.
- FAILS IF: a prefix value differs; a row is misaligned; a column or an E differs from the `VA(t−1)` derivation; a
  filed row differs from its cut-tape rebuild; the judging block is not the previous row's in-force block.
  PLANTS: the window shifted one bar forward, `t−L+2 .. t+1`, clipped at the tape end (X's form,
  `tc11x_va_fixtures.py:530-532, :550`) — "profile including bar t+1 must FAIL" (the contract's plant) → [a]; the
  volume misaligned by one row → [b]; the columns computed from `VA(t)` → [c]; an acceptance stamped one bar
  early → [d] (met by construction at the rule-based cut `i − 1`); the resolving bar written onto a probe row →
  [d]; the filed `va_regimes` read without its bound → [d]; the in-force block shifted one row forward in a copy
  of the door's table assembly → [e]; ATR taken at `t+1` → [e].

**F-STATE** (contract :116-117: "3 acceptances + 3 swing failures hand-verified against V2") — at `TC12-V`
- `[a SIX-EVENTS]`: chosen by a rule frozen HERE, before any V2 event exists: lens 4h, assets in the panel order
  of record (`E.CLASSIC5`, which is the lineage's `tierc2_rules.UNIVERSE` object: `scripts/tierc10_panel.py:197`),
  events by ascending `i`, holdout era first (tuning if the class has no holdout member). A1 = the first
  acceptance `by n_closes`; A2 = the first `by margin` with `bars_out ≥ 1`; A3 = the first `by margin` with
  `bars_out == 0`; S1 = the first swing failure with `bars_out == 1`; S2 = the first with
  `bars_out == K`; S3 = the first on the side opposite S1's. Two boundary NON-events ride beside: N1 = the first
  lapse with `bars_out == K + 1`; N2 = the first decay after A1. A class with no member prints `NONE-EXISTS
  <class>`, asserts from `va_events` that its count is zero, and its slot is FILLED by the next unchosen event of
  its kind in the same order (an acceptance for an A slot, a swing failure for an S slot); the synthetic table of
  [b] covers every class, so no transition goes unproven. "Hand-verified" = the fixture's own derivation sharing
  no code with the module — `VA(t0−1)` from the house function on the raw slice, ATR by its own Wilder loop, each
  clause written out per bar (close, E, `s·(c − E)/ATR`, count) and printed in the transcript — equal to
  production's tuple `(kind, side, t0, i, by, E, extreme)`.
- `[b TRANSITION-TABLE]`: a synthetic tape GENERATED from (N, M, K) drives every row of L-V.13, including a close
  exactly at an edge, a return exactly at E, the N-th close, the margin on the open bar, returns at K and K + 1,
  decay, a blocked re-probe, an opposite probe under a standing acceptance, both sides disarmed, warm-up, a
  resolution bar whose close lies outside the rolling `VA(t−1)` (`inside_frozen_only` true), and a zero-volume
  bar inside a probe (it counts as one close).
- `[c IDENTITIES]`: L-V.14's on every cell; `E ==` the edge of `VA(t0−1)` and `extreme ==` the raw max/min over
  `[t0, i]` on every event; every resolving row joins exactly one probe row on `(lens, asset, side, t0)`; the
  counted cases of L-V.13 printed, `n_inside_outside_rolling_va ==` the count of `inside_frozen_only` rows.
- `[d PREFIX]`: the machine half of F-VA-ASOF [d] — the state columns and the event rows of the same rebuilds —
  printed under this name; no second run.
- `[e ATR-BAR]`: the first pending bar where `M·ATR[t]` and `M·ATR[t−1]` decide differently is found by rule and
  production must follow `ATR[t]`.
- `[f ROUND-TRAP]` (L-V.24).
- FAILS IF: any of the eight tuples, any table row, any identity differs, or the reader returns a state other than
  the filed one. PLANTS: `accept_n − 1` → A1; the margin clause removed → A2, A3; `ret_k + 1` → N1; `ret_k − 1` →
  S2 (each of these four is caught on its named event where the class exists and on the synthetic table of [b]
  always); decay judged on pending bars → [b]; `inside_frozen_only` computed against `VA(t)` → [b]; E from
  `VA(t0)` → [c]; the extreme without the return bar → [c]; a dropped lapse row → [c]; an acceptance stamped one
  bar early → [d]; the margin read with `ATR[t−1]` → [e]; a reader copy recomputing `state` from filed levels →
  [f].

**F-STATE-X** (contract :32-33: "X's semantics asserted equal on the 4h holdout sample") — at `TC12-V`; L-V.15's
legs, each on X's 20 cells cut at W (`E.load_asof_at(stem, lens, W)`):
- `[x1]` `(N, none, 7)` == X's `record` rows. `[x2]` `(N, M, 7)` == X's `die_parity` rows. `[x3]` `(N, none, K)`
  == X's `k3` rows. `[x4]` V2 == `die_parity` with the relabel — **THE CONTRACT'S LEG on the 4h holdout**, binding
  on every lens and era. `[x5]` the TPO series at `(N, none, 7)` == X's `tpo` rows. `[x6]` the counters == the
  tracked manifest's `event_counts`, and the fresh full-float inside-flag == X's filed `close_in_va_prev` on every
  bar.
- FAILS IF: any key set, integer or string field, 6-dp float or counter differs. PLANTS: one-ulp edge nudge in
  the core → [x1]; the margin read with `ATR[t−1]` → [x2]; `ret_k + 1` handed to the k3 leg → [x3]; the relabel
  threshold at `K + 1` → [x4]; the era read from X's `era` column → [x4] (the acceptances collapse to 0); the TPO
  row index taken `side="left"` → [x5]; one counter moved by one in a copy of the manifest → [x6].

**F-VA-MIRROR** (contract :116: "HALT on disagreement") — at `TC12-V`; L-V.17's legs:
- `[a WORDS]` the five words by exact string equality on `would_read`. `[b MANIFEST]` the tracked manifest's
  `va_lens_verdicts`. `[c QUOTED]` each word re-derived from its row's printed columns, and every leaf of
  `VA_MIRROR.json` equal to the cell of the X row its `x_row` names (the record holds no number TC12 computed).
  `[d LICENCE]` the licence set and the reader's guard; every `licence` call appended to `licence_reads`.
- FAILS IF: any word, flag, quoted leaf or re-derivation disagrees — and then Stage V HALTs and writes no
  `VA_MIRROR.json`. PLANTS, each on a COPY of X's record or of the mirror: the 4h taker `would_read` flipped →
  [a]; the 1h maker row's `era` moved (zero rows) → [a]; the mirror pointed at `lens_word` → [a];
  `va_lens_verdicts["1h"].maker_twin` changed → [b]; `n_ranges` set under the floor on a PASS row → [c]; a figure
  no X row holds written into a copy of the mirror → [c]; a `licence("12h", "taker", "holdout")` request → [d]; a
  reader copy whose `licence` does not log its read → [d].

**F-TRAV** (contract :117: "typed constant → FAIL")
- `[a · <module>]` (a helper leg): the AST "typed constant" scan, the site-targeted leg beside L-0's general
  scan — in the named module an integer literal passed as, or assigned to, a time-stop or traverse name FAILS,
  and the factor of `T_5m` must be the `LENS_MS` quotient. Stage V runs it on its own files; every consuming suite
  on its builders.
- `[b REDERIVE]` at `TC12-V`: `T_ℓ` and the strict-INSIDE twin `T_strict_inside`, each with its `n_legs` and
  hinges, re-derived from `traverse_legs.parquet` == `TRAVERSE.json`.
- `[c POOL]` at `TC12-V`: every pooled leg's completion close ≤ ERA_CUT and its asset is a home asset.
- `[d CUT]` at `TC12-V`: the leg table rebuilt on FRESH tapes cut at ERA_CUT (`E.load_asof_at(stem, lens,
  ERA_CUT)`, an off-grid instant: each lens is cut at its last bar closed at or before it) == the filed tuning
  legs, row for row.
- `[e · <book>]` (a helper leg, real-book): every trade row's `T` of that range book == the value the reader's
  `traverse(name)` returns, and its manifest's `time_stop_source` equals the returned `source` with the certified
  sha.
- FAILS IF: any of the five. PLANTS: `time_stop = <an integer>` typed in a copy of a consumer → [a]; a typed 12
  as the 5m factor → [a]; `T_of_record` moved by one in a copy of `TRAVERSE.json` → [b]; `T_strict_inside` moved
  by one in a copy → [b]; a holdout leg planted in a copy of the leg table → [c], [d]; the touch test read against
  `VA(t)` → [d]; one trade row's `T` changed in a copy of a range book → [e].

**F-NEST-ASOF** (contract :46, :121: "a leaked future profile must FAIL")
- `[a PREFIX]` at `TC12-V`, on instants that need no book: per home asset, a tier-seeded draw of 5m-grid instants
  in each of tuning / holdout / strip, of 4h bar closes and of 4h bar opens, plus the boundary set of [b]. Count:
  n per home asset = TC11's count for its own nest as-of leg, `ASOF_MIN_CUTS`
  (`scripts/tierc11_nest_fixtures.py:934`, read by `ast`; on file 40), split equally over those five classes. For
  each instant τ every lens tape of the asset is cut at τ (`E.load_asof_at(stem, lens, τ)`; the 1d and 1w tapes
  re-derived from the cut 4h by Stage D's law, L-D.8's, complete days and weeks only), DOOR 1 rebuilds its
  per-bar rows on those tapes into a scratch root, and the reader's stamp at τ from those rows (`root=` the
  scratch) must equal the production stamp at τ from the filed tables, on every column of every block.
- `[b BOUNDARY]` at `TC12-V`: for each rung, τ exactly at an L+1 close (that bar IS read) and τ one lower-lens
  step before it (the previous bar is read).
- `[c INDEPENDENT]` at `TC12-V`: the block's levels and the seven coincidence fields recomputed by the fixture
  from the two raw windows with the house function; the gap guard exercised on a constructed lower tape with one
  bar removed (the seven fields must be NULL at the instants it hides, `nest_gap_reason` must name the lens, and
  the instants are counted).
- `[<book>]` in the stamps suite, one block per stamp table of the child (real-book): the reader's stamp at every
  instant of the book == the fixture's own linear-scan as-of join of the filed `va_bars` rows, plus the boundary
  legs on the book's own instants; it prints `leans on F-VA-ASOF [d]: a filed row at bar k equals a door rebuild
  on tapes cut at close_k`. The stamps suite imports no door.
- FAILS IF: any column differs, a boundary instant reads the wrong bar, or a hidden L+1 close yields a non-NULL
  flag. PLANTS: P1 inside DOOR 1, the as-of of the lens above shifted to `up_k + 1`, NULL where it passes the tape
  end — **a profile built through the unclosed higher-lens bar** — → [a], [b]; P2 inside DOOR 1, a 1d (1w) bar
  synthesised from the 4h bars of the current incomplete day (week) and filed with `close_ms` = the instant τ (a
  forming bar published as closed) → [a]; P3 the judged columns from `VA(k)` → [c]; P4 a reader copy that joins
  row `k + 1` → [a], [b], [<book>]; P5 the threshold in `ATR_U` → [c]; P6 a reader copy without the gap guard →
  [c]; P7 one cell changed in a copy of a filed table under an unchanged manifest, and a manifest copy whose sha
  entry is bent → the reader HALTs `STAGE-V-SHA` before any join.

**F-NEST-KEYS** — L-V.19's anchor; in the stamps suite at `TC12-V.stamps.c` only. FAILS IF: on campaigns entered
at or before W and instants ≤ W, the v6 or 9/12 key set built by the reader's `instants_of` differs from TC11's
filed nest tables (9/12 after dropping TC11's `as_of_pin` rows), or — the gated-subset law for the key tables
then on file — a key table's keys are not a subset of `v6`'s. No gated key table exists yet when `.c` is gated;
on the real key tables the subset law is asserted where they are filed (L-G.18's F-GATE leg; L-R.31 for
`dir_book_keys`), and this fixture keeps it failable on a constructed key table. PLANTS: one filed key dropped
from a copy; a `plus_1r` stamped at its bar's close; a key added to a copy of a gated key table.

**F-VA-NULL** — L-V.23's legs; at `TC12-V.trades`.
- `[a MIRROR]`: with X's seed (`PINS_X.json` key `seed`, read inside the stream builder typed in L-0.2's
  `X_SEED_MIRROR_T`) on the tape cut at W, the `phase` and the `perm_sha` of every `tr_tercile_lblock` draw of
  X's 20 cells == the filed `draw_info`.
- `[b IDENTITY]`: handed the identity permutation, DOOR 2's series-and-machine pass on the W tape == the filed
  `va_events` rows known at or before W of its ten cells (`events(asof_close_ms=W)`), at the write law; and no row
  of `va_null_events`, `va_null_go_events` or `NULL_BOXES_VA` lies past W.
- `[c FLOW]`: the null draw count bent at its door moves the number of draws filed per cell.
- FAILS IF: a draw's phase or permutation differs from X's; DOOR 2's unpermuted pass differs from DOOR 1's filed
  events; a null row lies in the strip; the draw count is not read from its pin. PLANTS: the draw seed shifted by
  one inside DOOR 2's stream builder → [a]; the volume column shifted one bar in DOOR 2's loader → [b]; the tape
  cut at the corridor pin → [b]; a typed draw count in a copy of DOOR 2 → [c] `PIN-NOT-READ`.
The flow legs of the pins L-R.32 registers with DOOR 2 as their consumer are L-0's F-TYPED-FLOW blocks, hosted in
this invocation (L-0.17: each consuming stage's suite).

**F-VA-PINS**
- `[a LOOKBACKS]` at `TC12-V`: `VA_PINS.json` == `PINS_X.json` == `va/build_manifest.json` `pins.L.<ℓ>.record`
  == the `L` column of X's `va_series_<ℓ>`; 1w == the 1d value, labelled BORROWED.
- `[b CROSS]` at `TC12-V`: every row of L-V.4's table: the first source == each cross source.
- `[c FLOW]` at `TC12-V`, Stage V's share of L-0's flow leg: each pin of L-V.4's table that DOOR 1 consumes, bent
  at its door, inside production, must move its witness; a pin whose bend moves nothing is `PIN-NOT-READ`. The
  profile, ATR and nest witnesses are evaluated on the sampled windows of F-VA-RAW [b] (the same count and
  source), and "moves" means at least one sampled value differs; the machine witnesses are the named events of
  F-STATE [a] and the rows of its synthetic table; the floor's witness is the traverse HALT.
- `[d L-COLUMN]` at `TC12-V`: the `L` column of every Stage V table == `VA_PINS.json`.
- `[e · <registration>]` (a helper leg, run by the suite of the stage that builds the registration): no
  registered construction, gate, licence or traverse reads a `1w_` column — proven on the registration spec's
  declared VA reads (its `VA columns read (declared for F-VA-PINS (e)):` sub-bullet) and by an AST scan of its
  builder.
- `[f TWELVE]` at `TC12-V`: L-V.22's — the collar and the label on every twelve-asset row; NULL 12h and 1w
  blocks; no twelve-asset leg in the traverse pool.
- FAILS IF: any of the six. PLANTS: one L moved by one in a copy of `PINS_X.json` → [a]; `pins.laws.break_margin`
  changed in a copy of X's manifest → [b]; a door copy that ignores the handed K and uses its own copy of it →
  [c]; the `L` column changed in a copy of a table → [d]; a copy of a registered arm's spec that reads `1w_state`
  → [e]; a twelve-asset leg appended to a copy of the leg table → [f].

Owned by section L-0 and run on this section's files: F-WALL and F-TYPED on `analytics/value_area.py`; F-CLOSURE
[i], [i-b], [ii], [iii] and F-HOOK-ESCAPE on the two doors (each EARNED, each typed in `DOORS_T`) and on the reader
(a fresh interpreter importing it holds no `analytics.value_area`, no `analytics.profile` and no door); F-NOT's
legs 1W and LICENCE on what L-V.5 and L-V.17 file; F-DET, F-KEY, F-COLLAR per directory; F-GRID on
`va_stack.parquet` and on the `TWO_TRADES_*` grids.

---------------------------------------------------------------------------------------------------------------
#### G · Unverified at drafting — checked at build, each a HALT or a printed count

- UNVERIFIED: prefix identity of the TC12 snapshot to TC11's (Stage D's fixture). Every equality leg against X
  assumes it.
- UNVERIFIED: that no degenerate window (zero total volume, or `hi <= lo`) occurs after warm-up on the 1w tapes
  and on the twelve's tapes. X's manifest proves it for its 20 cells only (`volume_sources.<cell>` keys
  `zero_or_negative_volume`, `nonfinite_volume`). Counted per cell and the bars are UNDEFINED; no HALT on 1w or
  twelve-asset tapes (L-V.3's HALT covers home 1h, 4h, 1d only).
- UNVERIFIED: that every twelve-asset tape holds at least `L_ℓ + 1` bars at each of its lenses. Short tapes are
  listed and UNDEFINED.
- UNVERIFIED: that the traverse pool clears the floor at 1h and 4h. HALT `TRAVERSE-UNDER-FLOOR` otherwise.
- UNVERIFIED: that each F-STATE [a] class has a member on the 4h tapes. A missing class prints `NONE-EXISTS`, its
  slot is FILLED (L-0.14), and the synthetic table of [b] covers the class; the leg is not RED on it.
- UNVERIFIED: that the correct-until-stable TPO row index reproduces X's filed `tpo_*` series (X's code stops after
  a fixed number of passes). F-VA-RAW [c], [d] decide it; a difference HALTs for an amendment.
- UNVERIFIED: bit-exactness under the interpreter of the build. It rests on numpy's `linspace`, first-max
  `argmax` and summation order; F-VA-RAW [b] and [c] are the guard, and the manifest records the numpy, pandas
  and pyarrow versions.
- UNVERIFIED: that the tapes are nested and gap-free at every lens close a funnel instant reads. The reader's gap
  guard counts the exceptions (L-V.21).
- UNVERIFIED: the wall time of the cut-tape legs (F-VA-ASOF [d] over `CUTS_V`, F-NEST-ASOF [a]): each cut
  rebuilds one asset's lenses. Their counts are fixed above and are not reduced at build; the measured wall time
  goes to the fixture record.
- UNVERIFIED: that every frame handed to the stamps children carries the columns L-V.19 names for its kind (the
  companion stamp column of a row-dependent event among them). The reader HALTs on a missing column or on a value
  outside the two stamps; it never guesses.

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · (none owned by L-V)

L-V owns no registered row and files no registration. The five rows (P-ADM-1, P-BRD-1, P-DIR-1, P-SFP-VA-1,
P-SCALP-3) belong to L-G, L-R and L-S. What a registration takes from this section, stated here so that each
spec block can carry it without a reference back:
- **The precondition selectors** (L-V.17 item 8): P-SFP-VA-1 — `{record:
  research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector:
  licence["4h|taker"].by_era["ALL"].would_read, required: "PASS"}` and `{record:
  research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector:
  licence_set, required: contains "4h|taker"}`; P-SCALP-3 — the one item `{record:
  research_outputs/tierc12/va/VA_MIRROR.json, certified_by: progress/TC12-V.json artifact_shas, selector:
  licence["1h|maker"].by_era["holdout"].would_read, required: "PASS"}`. P-ADM-1, P-BRD-1 and P-DIR-1 have none.
- **The declared VA reads** each spec lists for F-VA-PINS [e · <registration>]: column names of L-V.24's items 2
  and 3, read through the reader; none may be a `1w_` column.
- **The time stop** of the two range rows: the reader's `traverse("traverse.4h")` and
  `traverse("traverse.1h.in_5m_bars")`, tuning-fit, the regime reading (L-V.18).

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **The 1w lookback.** X pinned none and X's law cannot be applied at 1w from filed records (L-V.5). DEFAULT if
   silent: `L_1w` = the 1d pin's bar count, labelled BORROWED, read in exactly two places, both Tier-E (O-28): the
   V5 stamp columns and the lens-above axis of the 1d two-trades tables; read by no registered construction. The
   "1w NA" alternative is closed: O-28 settles the lookback, and O-28 is itself listed for the operator in the
   report's §9. What remains the operator's is the veto "va-lookback" (:135), which names every
   `va.lookback.<lens>` row, the borrowed 1w row included; a veto re-pins the row by a dated amendment carrying
   the operator's quote and rebuilds Stage V and everything downstream of it.
2. **Rejected armings.** "Every funnel instant" is read as TC11's law: entered campaigns from arm to exit.
   DEFAULT if silent: armings rejected before entry carry no stamp. Stamping them is a contract amendment.
3. **The traverse's population.** T of record pools every tuning leg inside a value regime, legs that contain a
   failed or lapsed probe included; the contract's "while INSIDE" (:42) read strictly would pool only the legs on
   which every bar closed INSIDE. DEFAULT if silent: the regime reading is the time stop of P-SFP-VA-1 and
   P-SCALP-3 (OD-15), and the strict reading is printed beside it per lens (`twins.strict_inside`) and enters no
   book. Making the strict figure the time stop is the operator's order, by a dated amendment before any range
   book is built.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

**What L-V hands the other sections:**
- To L-0: the typed door list is exactly two members, `DOORS_T = ("tierc12_va", "tierc12_va_trades")`;
  `scripts/tierc12_va_stamps.py` is the data-only reader, a decision module; `tierc12_va_fixtures.py` is the one
  member of `VA_MODULE_FIXTURES_T`; the Tier-E two-trades tables are DOOR 2's and hold no `TRADE_COLS_T` column.
  `analytics/value_area.py` is numpy-only, keyword-only, default-free, structural literals only (L-V.2). This
  section's two modules are the whole of `ONEW_READERS_T` (L-V.5). The mirror's licence record
  `va/VA_MIRROR.json` IS a registered record (collar-exempt; L-V.17), and its `licence_set` is what F-NOT's leg
  LICENCE reads. The traverse pin record is `va/TRAVERSE.json`, and the fitted-pin door is the reader's
  `traverse(name)` (L-V.18). The per-member bar-close columns of the V5 vector are `<ℓ>_bar_close_ms` for ℓ ∈
  {1h, 4h, 12h, 1d, 1w} (L-V.20). "The nest table" Stage V files is the nest columns of `va_bars_<ℓ>` (L-V.21);
  the per-book stamp tables are Stage V tables filed by the reader under `TC12-V.stamps.c/.r/.s` (L-V.19). The
  records are `TC12-V` and its four children with the `depends_on` of L-V.24; all of this section's code is an
  artifact of `TC12-V`. The register rows this section needs: `va.accept_n` (:35), `va.accept_margin_atr` (:35),
  `va.sfp_k` (:36, also :135), `va.nest_frac` (:45, also :135), `va.value_area_pct` (:29, held equal to the
  lineage object), `va.mirror_words` (:39-40), `va.licence_set` (:41), `va.lookback.<lens>` for the five lenses
  (kind `x_record`; `veto: "va-lookback"`; the 1w row with `source_lens: 1d`), and the fitted rows
  `traverse.<lens>` and `traverse.1h.in_5m_bars`. AM-1 (nickname AM-V2), the text of record in L-V.15, is filed by
  the orchestrator in `LEANS_AMENDMENTS.md` at the freeze.
- To L-D: this section's X records, read through `E.x_rec`, are the rows of L-V.1's table plus
  `tierc11x/null/build_manifest.json`; its TC11 records, read through `E.tc11_record` and all on
  `TC11_ALLOW_FILE`, are `stage_r/NEST_v6.parquet`, `stage_r/NEST_trg912.parquet`, `ranges/SCALE_GRID.parquet` and
  `ranges/SCALE_PICKS.json`. It reads, as TEXT by `ast` and never by import, `scripts/tierc11_nest.py`,
  `scripts/tierc11_nest_fixtures.py`, `scripts/tierc10_null.py`, `scripts/tierc10_census.py` and
  `analytics/rangefinder_census.py` (ordinary repo reads under L-D.27). Every frame is taken through
  `E.D.load_asof` / `E.load_asof_at`. Each door imports the env first and `analytics.value_area` after it, and no
  other non-fixture module imports it. The zero-volume law is honoured as L-V.6 and L-V.7 state, with the counts
  printed. `maker_pin.differs_from_x_assumption` is printed beside the "1h maker PASS" word (L-V.17 item 10).
- To L-X: a range row's precondition item cites `va/VA_MIRROR.json` by the selector of L-V.17 item 8 (the items
  are written out under REGISTRATION SPEC above); the scorer's `licence_at_maker_pin` leaf reads the columns
  L-V.17 item 7 quotes for the `1h|maker` holdout row; the report's mirror, pins-and-traverse and VA-stack blocks
  quote the files named in L-V.24 and its pointer rows name `va/trades/TWO_TRADES.md`; the dated V2-versus-X
  amendment is AM-1, the text of record in L-V.15.
- To L-R: everything L-R reads is in L-V.24's items 2-6 and 8. DOOR 2 builds the tables L-R.26..L-R.29 define, and
  hosts their fixtures at `TC12-V.trades`; `scripts/tierc12_stage_r_tables.py` does not exist. The stamps child
  `.r` stamps the ridden P-SFP-VA-1 arms and the take-profit venue's `tp` exits from the frames L-R files.
- To L-S: the ask to accept the scalper's kind (key `[known_at_ms]`, `bar_close` at 1h closes, the expiry and
  cancel instants) is answered by L-V.19's table; no block at the pinned maker rate is filed in `VA_MIRROR.json`
  (OD-12), only the quoted columns.
- To L-L: the ferry classes of the Stage V files are typed in L-L.25 from the keys declared here.

**What L-V assumes of them:**
- **L-D (substrate + env):** the snapshot `tc12_20261008` with PREFIX IDENTITY to `tc11_20260925` proven before
  Stage V; the frames of L-V.7 including derived 1d and 1w WITH volume for all seventeen stems' applicable lenses;
  `E.D.load_asof(stem, iv)` and `E.load_asof_at(stem, iv, cut_ms)`, the second admitting any integer instant ≤
  `PIN` (L-D.28); `E.x_rec`, `E.tc11_record`; `E.PIN_MS`, `E.TC11_PIN_MS`, `E.ERA_CUT_MS`, `E.SEED`, `E.LENS_MS`,
  `E.CLASSIC5`, `E.UNSEEN12`, `E.era_of`; the lineage aliases `E.R2` (`ATR_LEN`) and `E.R5`
  (`PROVISIONAL_MIN_N`); the VA-wall exit check in the shim (L-D.26 hunk 7), which lets `analytics.value_area`
  stand in a process only when its entry script is a door or `tierc12_va_fixtures.py`; the derivation law of
  L-D.8 as stated (the cut-tape legs re-derive 1d and 1w by it in the fixture's own loop).
- **L-0 (laws/process):** the fixture common law and harness (L-0.14: block ids, NOT RUN, the stream law, the one
  hand-sample law, `CLOSED-NO-BOOK`); the table law and `put` (L-0.13: 6 dp, keys, as-of stamps, collar,
  registered list, `READ_SET.json`); `tierc12_progress.certified` (L-0.4); the sub-stage law of L-0.10 with this
  section's four children, and `va/stamps` as the one shared directory of L-0.9; F-WALL, F-TYPED, F-TYPED-FLOW,
  F-CLOSURE, F-HOOK-ESCAPE, F-NOT (legs 1W and LICENCE), F-DET, F-KEY, F-GRID, F-COLLAR, with the helper legs in
  `tierc12_fx.py`; the contract pin door and the pin register with its `veto` field; `tierc12_asof.asof_index`;
  `PCT_PER_UNIT`; F-SEED's `X_SEED_MIRROR_T` holding the F-VA-NULL stream builder.
- **L-C (control):** the v6 and 9/12 books on the extended corridor as `books/v6_ext_campaigns.parquet` and
  `books/trg912_ext_campaigns.parquet`, carrying `symbol`, `entry_ms`, `arm_close_ms`, `entry_close_ms`,
  `latch_1r_open_ms`, `harvest_close_ms`, `exit_event_ms`, `exit_event_stamp`, `exit_reason`, `open_at_asof`
  (L-C.11); the count of rejected armings by reason. Stage C stamps nothing itself.
- **L-G (admission):** each gated book as a key subset of `v6`, filed as `stage_g/g_book_keys.parquet`, with the
  subset law asserted in its own suite. L-G's two registered rows read no VA column.
- **L-R (range-state):** reads `va_bars_4h` (and `va_bars_1d`) through `bars` for P-DIR-1 and the chop tables,
  with `pct` as bar k's judged column, and the `entry` rows of `VA_STAMPS_v6` for its entry-row assertion;
  consumes `va_events` swing_failure rows for P-SFP-VA-1 and decides in its own readings which filed profile
  (`*_f` or `*_n`) sets POC and far edge, the invalidation event (an `acceptance` row on the faded side) and
  whether an entry requires a return flag; defines, for DOOR 2 to build, the retest scan, the outcome ledger, the
  base rate, the lens-above partition, the gaps+order schedule and the per-draw statistics (L-R.26..L-R.29); its
  builders call `licence("4h", "taker", "ALL")` (and the 1d pair for the 1d cell) before any book and read T
  through `traverse("traverse.4h")` / `traverse("traverse.1d")`; it files the trade frames of the ridden arms,
  `stage_r/dir/dir_book_keys.parquet` and `stage_r/tables/TP1D_CAMPAIGNS.parquet` with the columns L-V.19 names.
- **L-S (scalper):** as-of joins the 1h and 4h tables onto 5m closes through `bars` and applies the live formulas
  of L-V.20 on the filed columns; decides the order geometry (the in-force `val` / `poc` / `vah` / `atr` at the
  trigger), what it does when the trigger instant is a lens close, the anchor bar of `T_in_5m_bars`, and
  cancellation on an `acceptance` event; calls `licence("1h", "maker", "holdout")` and
  `traverse("traverse.1h.in_5m_bars")`; files `stage_s/S_orders_<book>.parquet` keyed `[book, symbol,
  known_at_ms]` with the event columns L-V.19 names.
- **L-X (statistics + registrations):** each registration spec lists the VA columns it reads in its `arms` field
  (F-VA-PINS [e] scans that list); the labels of O-30 and the "T tuning-fit" and "tuning-window L" labels are
  carried on the rows that read T and L; the registry's `amendments` pin holds AM-1 at filing.
- **L-L (ledger + era + ferry):** the ferry classes of L-L.25 for `va/**`; L-L.16 reads the `entry` rows of
  `VA_STAMPS_v6` and `VA_STAMPS_trg912` through `certified()`.

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None on the facts. The 1w gap is settled by O-28 (O-15's key path `L.by_lens.<lens>.L_of_record` has no `1w`
entry; the 1w block stands on the 1d pin's bar count, labelled BORROWED, L-V.5).

ANNOTATION of O-16 (a) — not an objection: the ruling's sentence "every close at bar t is judged against VA(t−1)"
is read as L-V.8 rule 2 states it: an IDLE bar's close, and every bar's high and low, are judged against VA(t−1).
A close while a probe is pending is judged against that probe's FROZEN edge, the edge of VA(t0−1) (L-V.9) — X's
convention, which O-16 (a) names. Never the self-inclusive VA(t). The departure from the contract's letter is
declared in AM-1 (L-V.15).
