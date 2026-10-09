## L-V · THE VALUE AREA, MODULE-IZED

This section governs Stage V of the contract (lines 25-46) and the six fixtures the contract names for it
(F-VA-ASOF, F-VA-RAW, F-VA-MIRROR, F-STATE, F-TRAV, F-NEST-ASOF; lines 114-121). It fixes: the module
`analytics/value_area.py` and its public API, the one door that calls it and the data-only reader every other
stage uses; the profile law; the lookback per lens (and what the 1w lens gets, for which TC11-X pins nothing); the
causal convention in index terms; the V2 state machine as a transition table, its event records and its equality
target against X's filed events; the per-instant columns; the feasibility mirror; the traverse table that is the
time stop of every range trade; the V5 stamps and the boundary coincidence; the twelve new assets; the volume
null; the outputs and the compute plan. Every range trade of Stages R and S stands on these readings. L-V owns no
registered row.

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

**Notation.** ℓ = a lens. For one asset and lens: bars `t = 0..n−1` with `open_ms[t]`, `o,h,l,c,v`;
`close_ms[t] = open_ms[t] + step_ℓ`. `L_ℓ` = the lookback in bars. `VA(t) = (VAL[t], POC[t], VAH[t])` = the
profile over bars `t−L_ℓ+1 .. t`. `ATR[t]` = ATR_ℓ at bar t. "Top" = the VAH side = ABOVE; "bottom" = the VAL side
= BELOW; `s = +1` top, `−1` bottom. `N` = closes to accept, `M` = the one-close margin in ATR, `K` = the
swing-failure return window, `F` = the coincidence fraction (sources in L-V.4). ERA_CUT = `1719791999000`
(`x_rec/tierc11x/pins/PINS_X.json` key `era_cut_ms`; O-9). X_PIN = TC11's pin `1790294400000`
(`research_outputs/tierc11/data/AS_OF_PIN.json` key `as_of_last_closed_4h_close_ms`; `PINS_X.json` key
`as_of_close_ms`).

---------------------------------------------------------------------------------------------------------------
#### A · Source, module, profile, lookback

**L-V.1 SOURCE OF RECORD** — "Source of record = TC11-X's filed implementation (research_outputs/tierc11x/va/,
scripts, shas printed)" (contract :27-28)

READING: The source of record is X's filed X3 implementation, read as BYTES from the R0 copies (O-4), each read
asserted against `x_rec/X_REC_MANIFEST.json` (path + sha256) before use:

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
`analytics/value_area.py`, loading/pins/tables into `scripts/tierc12_va.py`. Each mirrored function names its X
original in its docstring:

| TC12 function | mirrors |
|---|---|
| `value_area.va_series` (+ private `_va_core`, `_bin_right`) | `tc11x_va.py` `va_series` :439-450, `va_windows` :423-436, `va_core` :343-420, `_bin_right` :326-340 |
| `value_area.va_machine` | `tc11x_va.py` `va_episodes` :544-646, `EpLaw` :520-527, `ref_arrays` :535-541 |
| `value_area.va_columns` | `tc11x_va.py` `va_view` :1208-1218; regime age from `regime_units` :968-977 / `adapter_walk` :955 |
| `value_area.va_traverse`, `traverse_pin` | `tc11x_ranges.py` `b_traverses` :787-810, `t_pin` :819-832 |
| `value_area.va_coincidence` | `scripts/tierc11_nest.py` `within` / `coin_flags` :1016-1051 (main tree; read as text) |
| `value_area.null_volume` | `tc11x_va.py` `null_volume` :1130-1169, variant `tr_tercile_lblock` |
| `tierc12_va.load_volume` | `tc11x_va.py` `load_volume` :303-322 |

Equality with X is held by fixtures on X's FILED records, never by shared code: F-VA-RAW (c) (series), F-STATE-X
(events), F-VA-NULL (draws).

SOURCE: contract :27-28; O-4, O-15; shas re-hashed while drafting (`shasum -a 256`); `x_rec/X_REC_MANIFEST.json`
(sha `cf66cb81…3e88`).

RIVALS: (a) import `tc11x_va` from x_rec — not taken: line 101 of that file imports `tc11x_env`, whose guards HALT
off X's snapshot and whose hook arms on import (O-4). (b) a byte copy with the sha in its filename, imported — not
taken: X's own vendor precedent (`tierc11x/vendor/tierc11_env@086d66da.py`) is a referee that is never imported.
(c) rebuild from `analytics.profile` alone and ignore X — not taken: it loses the equality anchor the contract
orders ("X's semantics asserted equal").

FAILS-IF: F-VA-RAW (b), (c) and F-STATE-X (x1)-(x6); mutation: a one-ulp edge nudge inside `_va_core` (X's own
plant).

**L-V.2 THE MODULE, THE DOOR, THE READER AND THE PUBLIC API** — "analytics/value_area.py; decision modules import
NOTHING from it — import-closure extends to it" (contract :25-26)

READING: Three objects and one direction of flow: tapes → the module (inside the door) → FILED tables → everyone
else.
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
- **The door `scripts/tierc12_va.py`** — the ONE member this section contributes to the typed door list. It imports
  the TC12 env FIRST and `analytics.value_area` and `analytics.profile` after it; takes every frame through the
  env's `load_asof` / `load_asof_at`; reads X's records through the env's sha-first `x_rec` and TC11's through
  `tc11_record`; computes ATR; builds and FILES every Stage V table. It decides nothing and trades nothing: no table
  it files carries `net_r`, `gross_r`, `fee_r`, `funding_r`, `entry_px`, `stop_px` or `exit_reason`.
- **The reader `scripts/tierc12_va_stamps.py`** — DATA-ONLY and NOT a door: it imports neither the module nor the
  door. It opens Stage V's filed, manifest-pinned tables and offers `bars(lens)`, `events()`, `regimes()`,
  `instants_of(frame, kind)` (L-V.19), `stamp(instants)` (L-V.20, an as-of join through
  `tierc12_asof.asof_index`) and `licence(lens, toll, era)` (L-V.17). Every other TC12 module — books, gates, range
  and scalper builders, the scorer — receives value-area facts through the reader or by reading the filed tables:
  as DATA, never by a call into the module or the door.

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
    # per bar: pct, edge_dist_atr, near_side, d_vah_atr, d_val_atr, poc_dist_atr, va_age, accept_age (L-V.16)
va_traverse(*, high, low, val, vah, regimes) -> dict           # "legs": per-leg rows (L-V.18)
traverse_pin(*, values) -> dict                # n, lower_hinge, median, upper_hinge, T = ceil(median), integer law
va_coincidence(*, vah_l, val_l, atr_l, vah_u, val_u, frac) -> dict   # L-V.21
null_volume(*, volume, true_range, lookback, rng) -> tuple[ndarray, dict]   # L-V.23; rng is built by the door
```

The as-of index is not in the module: it is `tierc12_asof.asof_index` (section L-0), one implementation for every
cross-lens join in TC12.

SOURCE: contract :25-26; O-15; the sibling readings L-0.17 (no typed number; the structural set; "its functions take
every parameter as a required keyword argument with no default"), L-0.22 (doors, decision modules, "value-area
state enters decision code only as DATA", the analytics wall: imports `numpy` and `__future__` only) and L-0.28
(`asof_index`); L-D (the shim forbids the name `value_area` in its process until a V-stage module imports it after
the shim; `load_asof`, `load_asof_at`, `x_rec`, `tc11_record`); `tests/test_analytics.py:118-161` (F-AN-3: no line
matching `^\s*(from|import)\s+engine\b` in the RAW source, docstrings included; F-AN-4: no `read_parquet`,
`requests`, `urllib`, `os.environ`, `socket` token and no `open(` call); `analytics/rangefinder_census.py:132-133`
("the ATR itself is handed in"); scout U2 §1.12, U3 §1.2.

RIVALS: (a) register the module in `_MODULES` — not taken: it moves `analytics_sha()` for every consumer and X's
F-PROFILE-PIN. (b) a law object built with `dataclasses`, or defaults on law parameters — not taken: the wall admits
`numpy` and `__future__` only, and a default is a typed constant. (c) range and scalper builders call the door for
arrays — not taken: a decision module that imports the door reaches the module transitively, which the contract
forbids. (d) a second door for the stamps — not taken: the vector at an instant is a join of filed rows (L-V.20) and
needs no module call.

FAILS-IF: owned by L-0 — F-WALL (the module's imports and I/O), F-TYPED (literals, defaults), F-CLOSURE (the door's
two conditions; a fresh interpreter importing the reader holds no `analytics.value_area`). Owned here — F-VA-RAW (b)
(two block sizes give byte-equal series). Mutations: a copy of the reader importing the door → F-CLOSURE RED; a
`net_r` column added to a copy of a door table → F-CLOSURE RED; a block size that changes a level → F-VA-RAW (b) RED.

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
cited; `tc11x_va.py:343-450`; `x_rec/tierc11x/LEANS_X.md` LX-X3.2..X3.4 (:1608-1647); O-15. The door imports
`analytics.profile` only after the three pins hold (file sha, `analytics_sha()`, `ANALYTICS_VERSION`), each read
from `x_rec/tierc11x/va/build_manifest.json` → `pins.profile.pins` (X's F-PROFILE-PIN law, `tc11x_va.py:118-149`).

RIVALS: 100 rows (the function default) — X's twin, not carried. Bin edges as levels — X's twin, filed, unused.
ATR-scaled or tick rows — rejected by X (LEANS_X :1640). `windowed_profile` (day windows by bar OPEN, finer
substrate, `profile.py:175-225`) — a different object. A finer-substrate build of the coarse lenses (X's
house-substrate twin) — not carried.

FAILS-IF: F-VA-RAW (a), (b); mutations: the volume column shifted one bar; every interior edge nudged one ulp.

**L-V.4 THE LOOKBACK PER LENS AND THE LAW CONSTANTS** — "Lookback per lens = X's pin, read from its records and
FROZEN here as bars, decoupled from the pivot detector ["va-lookback"]" (contract :28-29)

READING: For ℓ ∈ {1h, 4h, 12h, 1d}: `L_ℓ = int(PINS_X["L"]["by_lens"][ℓ]["L_of_record"])`, read from
`x_rec/tierc11x/pins/PINS_X.json` (values on file at drafting: 71 / 66 / 53 / 35). Stage V writes them ONCE to
`research_outputs/tierc12/va/VA_PINS.json` (`by_lens.<ℓ>.L_bars`, with the source path, key and sha) BEFORE any
series is built; every later read is from `VA_PINS.json` by object, asserted equal to `PINS_X.json`. "Frozen as
bars, decoupled": no pivot-machine run ever re-derives L in TC12; L is an integer bar count and nothing else.
The label X filed travels on every VA row (`l_label`): "a tuning-window L is in-sample for tuning-era VA bars (the
L-R.2 label)" (`PINS_X.json` → `L.by_lens.<ℓ>.label`). X's twins (whole-tape, frozen-3.0, per-asset L) are not
carried. Every other constant of this section, with the source the DOOR reads at run time, what it is asserted equal
to, and — for the pin register's flow leg — what must move when the pin is bent at its door:

| constant | read at run time from | asserted equal to | value on file | witness when bent |
|---|---|---|---|---|
| `L_ℓ` | `PINS_X.json` `L.by_lens.<ℓ>.L_of_record` (X's record) | `va/build_manifest.json` `pins.L.<ℓ>.record`; the `L` column of X's `va_series_<ℓ>` | 71 / 66 / 53 / 35 | `VA(t)` of a seeded window |
| N (closes to accept) | contract :35, through the contract pin door | the AST literal `PINS["BREAK_CONFIRM_N"]` of `analytics/rangefinder_census.py` (:141; file sha `19c5507f…b37d`); X's `pins.laws.break_confirm_n` | 8 | the bar of F-STATE's A1 |
| M (one-close margin, ATR) | contract :35, pin door | `PINS["BREAK_MARGIN"]` (:144); `pins.laws.break_margin` | 1.5 | F-STATE's A2 and A3 |
| K (return window) | contract :36, pin door, with :135 `"sfp-k" (3)` as its second citation | a member of `pins.laws.sfp_k_twins` | 3 | F-STATE's N1 |
| F (coincidence, ATR) | contract :45, pin door, with :135 `"nest" (0.25 ATR)` as its second citation | `pins.laws.coincidence_atr`; the AST literal `COIN_FRAC` of `scripts/tierc11_nest.py` (:108) | 0.25 | the nest flags of a seeded bar set |
| bins, value_area | `analytics.profile.PROFILE_ROWS`, `.VALUE_AREA` (lineage objects, read by the door) | `pins.profile.bins`, `pins.profile.value_area`; contract :29 "70%" (the pin door asserts it) | 120, 0.70 | `VA(t)` of a seeded window |
| ATR length | the lineage object `ATR_LEN` (`scripts/tierc2_rules.py:121`) through the env | the AST literal `ATR_LEN` of `analytics/rangefinder_census.py` (:132) | 14 | `ATR[t]` |
| floor n | the lineage object `PROVISIONAL_MIN_N` (`scripts/tierc5_rules.py:232`) through the env | `pins.laws.floor_n` | 30 | the traverse HALT |
| null draws | X's `pins.laws.k_draws` | the AST literal `K_DEFAULT` of `scripts/tierc10_null.py` (:109) | 20 | the draw count |
| X's record return window (mirror legs only) | X's `pins.laws.dev_return_bars` | `PINS["DEV_RETURN_BARS"]` (:140) | 7 | F-STATE-X (x1) |
| percent factor | `PCT_PER_UNIT` of `scripts/tierc12_units.py`, handed to the module | — | 100 | — |

A veto of "va-lookback", "sfp-k" or "nest" changes the first source's value, demotes Stage V and every range row,
and rebuilds them; nothing else changes.

SOURCE: contract :28-29, :35-36, :45, :135; O-15; `PINS_X.json` keys as cited (`L.law`: "one L per lens — the
CLASSIC5 pooled, dead-weighted mean of DIED confirmed-range lives (die_i − confirm_i) on the tuning-era head at
each asset's pick of record, L = floor(x + 0.5)"); `tc11x_ranges.py` `lookback` :1355-1362; three concordant
sources of L verified while drafting (`PINS_X.json`, `va/build_manifest.json` `pins.L.<ℓ>.record`, X3.md :31-34);
`va/build_manifest.json` `pins.laws` and `pins.profile` read while drafting; the sibling reading L-0.17 (the pin
doors, the register, the flow leg).

RIVALS: type 71/66/53/35 — forbidden. Re-derive L by running the pivot machine — contradicts "decoupled". Carry
X's L twins — three more value areas per lens with no contract phrase behind them. Read N and M from the range
machine by import — puts `analytics.rangefinder_census` in the door's process for two numbers the contract states.

FAILS-IF: F-VA-PINS (a), (b), (d); L-0's F-TYPED and F-TYPED-FLOW on the door and the module (each pin above bent at
its door must move its witness). Mutations: a typed lookback in a copy of the door → F-TYPED RED; one L moved by one
in a copy of `PINS_X.json` → F-VA-PINS (a) RED; `pins.laws.break_margin` changed in a copy of X's manifest → (b) RED.

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

The reading of record is therefore the labelled fallback: **`L_1w := L_1d`, the 1d pin's bar count, read from
`PINS_X["L"]["by_lens"]["1d"]["L_of_record"]`**, written to `VA_PINS.json` as `by_lens.1w` with
`label = "BORROWED: the 1d pin's bar count; X pinned no 1w lookback; not X's law at 1w"` and `source_lens = "1d"`.
The 1w value area is built on the derived weekly tape (L-V.7), runs the same machine, and is a STAMP-ONLY, Tier-E
column block (O-11): no trade, no feasibility row, no licence, no traverse row, no registered construction reads a
`1w_` column (F-VA-PINS (e) proves it). Printed beside in `STAGE_V.md`, as the mechanism disclosure: the five
filed 1w per-asset mean lives at TC11's picks (`SCALE_GRID.parquet`, whole-tape, 1 dp) — every one of them is
shorter than the borrowed count.

Why the borrow and not NA: (i) the contract orders a 1w block twice (:44-45, and the lens above 1d at :76-79);
(ii) TC11's L-R.2 is the filed precedent for this very lens — where the law of record cannot be fitted for lack
of tuning bars it applies a LABELLED fallback and carries the label on every row
(`research_outputs/tierc11/LEANS.md:179-181`), it does not print NA; (iii) the borrowed quantity is a filed X pin
in the law's own unit (bars of the lens), tuning-fit, so it carries no holdout information; (iv) neither reading
can move a verdict — no registered row reads 1w — so the cannot-flatter test does not separate them.

SOURCE: files and keys as cited; O-11, O-15; contract :14, :44-45, :76-79, :137; scout U2 §1.2, R2.

RIVALS: (a) 1w columns NA with the reason — the stricter reading of :28; not taken for (i)-(ii); it is the
operator's one-word alternative (OPEN TO OPERATOR 1). (b) X's law computed afresh at 1w — needs a pivot run
("decoupled" forbids), whole-tape picks, under-floor n. (c) a calendar equivalent of the 1d pin (five weekly bars)
— a profile of five uniform slabs; X's own note that coarse-bar profiles approach "a sum of boxcars" (LEANS_X
:1629-1631). (d) the mean of the five filed 1-dp per-asset means — an executor-invented statistic on whole-tape
fits.

FAILS-IF: F-VA-PINS (a) (`VA_PINS.by_lens.1w.L_bars == by_lens.1d.L_bars`, label present on every 1w row) and (e);
mutation: a copy of a registered arm's spec that reads `1w_state` must turn (e) RED.

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

FAILS-IF: F-VA-RAW (d) (TPO rows == a per-window searchsorted count, a zero-volume flat bar included by
construction of a planted window) and (c) (== X's filed `tpo_*` at the 6-dp write law); mutations: the TPO row
index taken with `side="left"`; zero-volume bars dropped from the TPO count.

**L-V.7 SUBSTRATE PER LENS AND ATR_L** — "volume-at-price" (contract :30); "ATR_L" (:35, :38, :45)

READING: A lens's profile reads that lens's own bars and no other interval's.

| asset set | lens | tape and volume source (snapshot `tc12_20261008`, L-D) |
|---|---|---|
| five home | 1h, 4h, 12h | native `klines/{sym}_{ℓ}.parquet` |
| five home | 1d | Stage D's derived `klines/{sym}_1d.parquet` (4h volume summed per complete UTC day) |
| five home | 1w | Stage D's derived `klines/{sym}_1w.parquet` (seven complete derived days, Monday-anchored UTC) |
| twelve new | 1h, 4h | native |
| twelve new | 1d | Stage D's derived 1d |

Every frame is taken through the env's `load_asof(stem, lens)` (bars closing ≤ the corridor pin) or
`load_asof_at(stem, lens, close_ms)` (a cut tape: the X_PIN tape of the equality legs, the prefixes of the as-of
legs); columns `open_time:int64, open, high, low, close, volume:float64`. One frame supplies both the prices and
the volume of a cell, and the door still asserts X's alignment law before any profile — the frame's `open_time`
strictly increasing and equal, row for row, to the tape it hands the machine — else HALT (`tc11x_va.py:303-322`).
A zero-volume bar is one bar in every count of this section: the lookback, the N closes, the K closes, the
traverse. ATR_ℓ = `engine.indicators.atr(h, l, c, ATR_LEN)` on the lens's
WHOLE tape from its first bar (`engine/indicators.py:31-54`: Wilder RMA, alpha = 1/len, seeded with
`TR[0] = high[0] − low[0]`), computed in the door and handed into the module. It is prefix-invariant; a tail-loaded
tape re-warms it and is refused. `ATR[t]` includes bar t's own true range. A non-finite or non-positive `ATR[t]` at
any `t ≥ L_ℓ` HALTs the cell. **5m is not a VA lens**: no profile is built on 5m bars anywhere in TC12.

SOURCE: O-8, O-15; LEANS_X LX-X3.2 (:1619-1627); `engine/indicators.py` (sha `91805c04…c113`); TC11 LEANS L-R.1
(:172-175); `scripts/tierc11_data.py:1523-1531` (the weekly derivation); 17 `*_1w.parquet` and 17 `*_1d.parquet`
files exist in `tc11_20260925/klines/`, and the BTCUSDT and NEARUSDT files of both lenses carry a `volume` column
(inspected; the other fifteen stems are checked at build by the alignment HALT).

RIVALS: `analytics.volatility.atr` (SMA-seeded, NaN warm-up) — moves every 1.5-ATR acceptance. 1d/1w volume summed
from 1h — disagrees with native 4h/12h on X's six incident days. A 5m profile for the scalper — the contract makes
5m a clock, "never a signal source" (:89).

FAILS-IF: F-VA-ASOF (b) (row alignment); mutation: the volume column misaligned by one row in the door's loader.

**L-V.8 CAUSALITY, IN INDEX TERMS** — "CAUSAL: the VA stamped at bar t uses volume from bars ≤ t only" (contract
:30-31)

READING: Six rules; each is a fixture leg.
1. `VA(t)` reads bars `t−L_ℓ+1 .. t` of the lens's own tape — indices ≤ t. It is known at `close_ms[t]` and is IN
   FORCE from that instant until `close_ms[t+1]`.
2. Bar t's close, high and low are JUDGED against `VA(t−1)`, never against the self-inclusive `VA(t)` (O-16 (a)).
   Every state, event, %-of-value, distance and touch in this section uses that frame. The first judged bar is
   `t = L_ℓ`.
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

FAILS-IF: F-VA-ASOF (a), (c); F-NEST-ASOF (a), (b); mutations: the window shifted one bar forward
(`t−L+2 .. t+1`); judged columns computed from `VA(t)`; the as-of index of the lens above shifted by +1.

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

FAILS-IF: F-STATE (b) rows "edge equality", (c) STRUCT (`E ==` the edge of `VA(t0−1)` exactly on every probe);
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

FAILS-IF: F-STATE (a) A1-A3, (b), (e); mutations: `accept_n − 1`; the margin clause removed; the margin read
with `ATR[t−1]` (caught on the targeted bar of leg (e)).

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

FAILS-IF: F-STATE (a) S1-S3, N1, (b), (c); mutations: `ret_k + 1` (N1 becomes a swing failure); `ret_k − 1` (S2
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

FAILS-IF: F-STATE (a) N2, (b) rows "decay", "blocked re-probe", "opposite probe", "flip"; mutation: decay evaluated
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
close lies outside the rolling `VA(t−1)` (`n_inside_outside_rolling_va`); the next idle bar re-judges it;
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

FAILS-IF: F-STATE (b) (every row of this table on a synthetic tape generated from N, M, K), (c) (identities),
(d) (prefix); mutations: listed under L-V.10..12.

**L-V.14 THE EVENT RECORDS** — "PROBING … ACCEPTED … SWING FAILURE … decays" (contract :34-37)

READING: One row per event in `va/va_events.parquet`, key `[lens, asset, kind, side, i, t0]`,
`kind ∈ {probe, acceptance, swing_failure, lapse, decay}`. Fields, exact:

| field | meaning |
|---|---|
| `lens`, `asset`, `kind`, `side` | side `top` (VAH) / `bottom` (VAL); for `decay`: the side whose acceptance stood (`both` if both) |
| `t0`, `t0_close_ms` | the probe's first close beyond (bar index of the lens tape; its close). `decay`: the bar of the acceptance being decayed |
| `i`, `known_close_ms`, `era`, `in_strip` | the bar whose close prints the event (`probe`: `i = t0`); its close; tuning iff `known_close_ms ≤ ERA_CUT`, else holdout (the estate's close-based era law); `in_strip` iff `known_close_ms > X_PIN` |
| `bars_out` | `i − t0` |
| `closes` | closes beyond E so far (X's counter: 1 at `t0`) |
| `by` | `n_closes` / `margin` for an acceptance, else empty |
| `E` | the frozen edge = that edge of `VA(t0−1)` |
| `extreme` | `max(h[t0..i])` (top) / `min(l[t0..i])` (bottom), inclusive |
| `close_i`, `atr_i`, `excess_atr` | `c[i]`, `ATR[i]`, `s·(c[i] − E)/ATR[i]` |
| `sgn` | swing_failure, lapse: −1 top / +1 bottom (toward value); probe, acceptance: +1 top / −1 bottom; decay 0 |
| `val_f`, `poc_f`, `vah_f` | the FROZEN profile `VA(t0−1)` — the profile whose edge was probed |
| `val_n`, `poc_n`, `vah_n` | the profile in force after the event bar, `VA(i)` |
| `ret_inside_frozen`, `ret_inside_rolling` | swing_failure / lapse only: `val_f ≤ c[i] ≤ vah_f`; `VAL[i−1] ≤ c[i] ≤ VAH[i−1]` |
| `from_state`, `state_after` | the state when the probe opened; the state after bar i |
| `rid`, `r0` | the value regime alive at `t0` (−1 if none) |
| `episode`, `end_kind`, `end_i` | probe rows: ordinal per (asset, lens); how it ended (`swing_failure`, `lapse`, `acceptance`, `open` at the tape end); the resolving bar (−1 open) |

Regimes are filed in `va/va_regimes.parquet` (`asset, lens, rid, r0, r0_close_ms, start_kind ∈ {first_valid,
decay}, die_i, die_close_ms, end_side, end_by, n_bars`). A value regime runs from the first valid bar or a decay
bar to the next acceptance; its geometry excludes the acceptance bar. Identities held per cell:
`probe == swing_failure + lapse + acceptance + open_at_end`; `regimes == 1 + decay` on a tape with at least one
valid bar (each decay starts exactly one regime); every acceptance has `by` non-empty; every row is known at its
own bar (`known_close_ms == close_ms[i]`). Which profile sets a trade's POC and far edge (`*_f` or `*_n`) is the
trading section's reading (INTERFACE).

SOURCE: `tc11x_va.py:569-583` (`close_ep`), :630-646, :1243-1264 (`ev_rows_va`); X's `events_va.parquet` schema
(54 columns, read here); AM-X11 (4), (5).

RIVALS: file only swing failures and acceptances (X's `sfp`/`accept` rows) — the lapse and the decay are V2
outcomes a reader must be able to count. Carry only the frozen profile — the in-force one is one column join away
and the trading section must choose between them in the open.

FAILS-IF: F-STATE (c) (the identities; `extreme` and `E` recomputed from the raw tape for every event);
mutation: a dropped lapse row; a swing failure stamped at `t0`.

**L-V.15 EQUALITY WITH X, AND THE DATED AMENDMENT** — "X's semantics asserted equal on the 4h holdout sample,
amendments dated if they differ" (contract :32-33)

READING: Write a law as the triple `(accept_n, margin_atr, ret_k)`. The contract's V2 is `(N, M, K)`. X's machine
OF RECORD is `(N, none, 7)`; X never ran V2. X filed two one-field twins: `die_parity` = `(N, M, 7)` and `k3` = `(N, none, K)`.
Because only an ACCEPTANCE changes an armed flag or a regime (`tc11x_va.py:575-582`) and `ret_k` only chooses the
label at :610, **V2's event stream is X's `die_parity` stream with every return of `bars_out > K` relabelled from
sfp to lapse**; acceptances, edges, extremes and bars are identical.

The equality target (F-STATE-X), computed by the module at FULL FLOAT from the tapes cut at X_PIN
(`load_asof_at(stem, lens, X_PIN)`) and compared with X's filed rows:
- **Rows.** `x_rec/tierc11x/va/events_va.parquet`, `lens == "4h"`, `variant == "die_parity"`,
  `cls ∈ {"sfp", "accept"}`, five home assets.
- **Era by join.** X's twin `accept` rows carry an EMPTY `era` and a null `known_close_ms` (verified: 1,605 of
  1,605 at 4h). The era is taken by joining `(asset, i)` to `va_series_4h.parquet` `(asset, i)` → `close_ms`;
  holdout iff `ERA_CUT < close_ms ≤ X_PIN`. Filtering X's `era` column directly is forbidden (it drops every
  acceptance).
- **Mapping.** X `accept` ↔ V2 `acceptance`; X `sfp` with `bars_out ≤ K` ↔ V2 `swing_failure`; X `sfp` with
  `bars_out > K` ↔ V2 `lapse`.
- **Comparison.** Set equality on `(asset, side, t0, end_i)` and, per matched row, exact equality of the integers
  and strings `(by, closes, bars_out)` and equality of `E`, `extreme`, `E_end` AT THE 6-dp WRITE LAW: the
  fresh value passed through the estate's own write function (`tierc2_baseline._round_floats`, :162-167, the
  function X's writer used) must equal the filed value exactly — no tolerance.
- **The 6-dp hazard.** X's writer rounds levels to 6 dp, and a state re-derived from FILED levels flips at exact
  edges (scout U2 H7: ZECUSDT 4h `i = 8337`, close 30.17 against a filed VAH of 30.170000 with the filed flag
  False). The fixture never derives a state or an event from filed levels: events come from the fresh full-float
  series; the series is compared with X's filed series at the write law (F-VA-RAW (c)); the fresh full-float flag
  `VAL[i−1] ≤ c[i] ≤ VAH[i−1]` is compared with X's filed `close_in_va_prev` on every bar; and the count of bars
  where the flag re-derived from the filed 6-dp levels would differ is printed as a disclosure.
- **Scope.** The contract's leg is the 4h holdout. The same comparison is binding on 4h tuning and on 1h, 12h, 1d
  (both eras), and three mirror legs prove the mirrored machine IS X's before V2 is trusted: `(N, none, 7)` against
  X's `record` rows, `(N, M, 7)` against `die_parity`, `(N, none, K)` against `k3`; and the machine at
  `(N, none, 7)` on the TPO series against X's `tpo` rows. The value 7 is read from
  `va/build_manifest.json` → `pins.laws.dev_return_bars` and is used by these legs only.
- **Counters.** On each of X's 20 cells the V2 counters `probe`, `acceptance`, `acceptance by margin`, `decay`,
  `blocked_reprobe`, `regimes`, `rearm_blocked_by_pending`, `open_at_end` equal `va/build_manifest.json` →
  `event_counts["<asset>|<lens>"]["die_parity"]` keys `breach`, `accept`, `accept_by_margin`, `rearm_closes`,
  `blocked_disarmed`, `regimes`, `rearm_blocked_by_pending`, `open_at_end`; and `swing_failure + lapse == sfp`.
- **Expectations, not inputs** (scout U2 R10, structural): on the 4h holdout, 555 acceptances (432 by margin, 123
  by count) and 725 closes back inside = 602 swing failures + 123 lapses. The fixture reads its counts from the
  files and prints them beside these.

**The dated amendment (filed at the LEANS freeze, O-16 (c)); text of record:**
"AM-V2 · <freeze date UTC> · TC12's value-area machine is the contract's V2 and differs from TC11-X's machine of
record in two fields. (1) Acceptance: X's record accepts on the 8th consecutive close strictly beyond the frozen
edge only; V2 also accepts on one close at or beyond 1.5·ATR_L of the same bar beyond the edge, the probe's first
bar included — X's `die_parity` twin. (2) The swing-failure return window: X's record is t − t0 ≤ 7; V2 is
t − t0 ≤ 3 — X's `k3` twin. V2 therefore has an outcome X's record cannot reach, the LAPSE (a return on closes
4..7), which is neither a swing failure nor an acceptance and feeds no trade. X never ran the two fields together;
V2 equals X's filed `die_parity` stream with returns of bars_out > 3 relabelled lapse, held by F-STATE-X on the 4h
holdout and on every other lens and era. Everything else is X's law unchanged: each close judged against VA(t−1);
the edge frozen at the probe's first close; decay on the first idle close inside the rolling VA(t−1); one
resolution per bar. New in TC12 with no X counterpart: the per-bar state column, the signed edge distance, the POC
distance, the VA age column, the value-area traverse, the lens-ladder coincidence, the 1w block on a borrowed
lookback. **The feasibility words that license the range trades (F-VA-MIRROR) were earned on X's record machine,
not on V2**; they are read, not re-earned (DISCLOSURES D-2)."

SOURCE: O-16; `tc11x_va.py:520-532, 569-583, 610`; `events_va.parquet` and `va_series_4h.parquet` schemas and the
blank-era fact (inspected while drafting); scout U2 §1.6, R10, H7, H8.

RIVALS: assert equality against X's `record` rows — fails by construction (different law). Recompute X's twin by
running `tc11x_va` — forbidden. Compare floats at a 1e-6 tolerance — looser than the write law and unnecessary if
the mirror is exact. Derive the era from X's `era` column — drops every acceptance.

FAILS-IF: F-STATE-X (x1)-(x6); mutations: the relabel threshold moved to `K + 1`; the era taken from X's `era`
column (the acceptance count must collapse to 0 and the leg turn RED); `margin_atr` read with `ATR[t−1]`.

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
L-V.13 (i). Bars `t < L_ℓ`: `state = UNDEFINED`, every other column NULL.

SOURCE: `tc11x_va.py` `va_view` :1208-1218 (`pct = 100.0 * (c - rl) / (rh - rl)`, `dist = minimum(abs(rh - c),
abs(c - rl)) / tape.atr`), `adapter_walk` :955 (`ir_age = t − r0`); TC11 LEANS L-R.5 (:226-229): "%-of-range
(unclamped); signed distance to the nearest boundary in ATR_L: positive inside the box, negative beyond it, with
near_side beside"; `tierc10_census.py:843-849` (`near_top = … d_top <= d_bot  # tie -> top`); scout U2 R14.

RIVALS: `pct` clipped to [0, 100] — hides how far beyond value a close is. Distance signed by edge (positive above
VAH, negative below VAL) — conflates inside with outside; the two raw distances carry it. Age of the profile window
(always L) — not a regime age. Columns against `VA(t)` — self-inclusive (L-V.8 rule 2).

FAILS-IF: F-VA-ASOF (c) (every column recomputed by the fixture's own arithmetic from the raw tape and the house
profile of `t−L .. t−1`); mutations: columns computed from `VA(t)`; `pct` clipped; the sign of `edge_dist_atr`
flipped.

---------------------------------------------------------------------------------------------------------------
#### C · Mirror, traverse

**L-V.17 F-VA-MIRROR** — "reproduce X's feasibility verdicts from X's records — 4h taker PASS · 1d taker PASS ·
1h maker PASS · 12h FAIL · 1h taker FAIL — HALT if the mirror disagrees on any word (the Q-R3 law licenses exactly
{VA-4h taker, VA-1d taker, VA-1h maker}; nothing else may trade a range)" (contract :39-41)

READING: The mirror READS; it recomputes nothing under V2 (O-17).
1. **File.** `x_rec/tierc11x/va/feasibility.parquet`; its sha256 is asserted equal to `X_REC_MANIFEST.json` and to
   `progress/X3.json` `artifact_shas` (`ea8573b3…b6f0`) before the read.
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
   and carries no Tier-E collar. Its PASS / FAIL tokens are X's filed words, QUOTED, each with X's row key and the
   parquet's sha; TC12 computes none of them. Keys: `x_file {path, sha256}`; `words` — the five in the contract's
   order, each `{lens, toll, word, x_row {asset, era, scale_kind, lens, toll}, would_read, verdict_pass,
   of_record_for_detector, toll_bps, edge_net_h20}`; `licence` — keyed `"<lens>|<toll>"` for the three licensed
   pairs, each with `by_era` ∈ {`ALL`, `tuning`, `holdout`} → `{would_read, verdict_pass, edge_net_h20, toll_bps,
   x_row}`; `beside` — the 12h maker `va_regime` row (FAIL), its `va_lblock` twin (PASS) and the 1h `lens_word`
   sentence; `licence_set`. So each range trade reads the row of its own scoring era, and the report prints beside
   it the rows that do not pass (O-17: 1d taker FAILS on ALL and on tuning).
8. **The selector a registered row's precondition cites:** path `research_outputs/tierc12/va/VA_MIRROR.json`; sha
   from `progress/TC12-V.json` → `artifact_shas`; key `licence["<lens>|<toll>"].by_era["<era>"].would_read` —
   `"4h|taker"` at the era P-SFP-VA-1 is scored on; `"1h|maker"` at `holdout` for P-SCALP-3; `"1d|taker"` for the
   Tier-E 1d cell. Which word closes a row by precondition is that registration's own rule.
9. **The licence set** is the PASS words among the five = {(4h, taker), (1d, taker), (1h, maker)}, asserted equal
   to the set parsed from :41. The reader's guard `licence(lens, toll, era)` returns the selected row and HALTs for
   any pair outside the set. It governs a book's TRADE OF RECORD. A cost twin the contract itself orders (the 4h
   maker twin :75, the scalper's all-taker twin :102) inherits its parent's licence and prints the mirror word of
   its own (lens, toll) beside.
10. **Printed beside the "1h maker PASS" word**, in `STAGE_V.md` and in the report: the row's `toll_bps` (the
   round trip X assumed) and Stage D's `maker_pin.differs_from_x_assumption` flag (O-19).

SOURCE: O-17; `feasibility.parquet` rows and `va_lens_verdicts` read while drafting (the five `would_read` values
are PASS, PASS, PASS, FAIL, FAIL; `toll_bps` 10.0 taker, 4.0 maker); `tc11x_va.py:1727-1756`; DISCLOSURES D-2;
scout U2 §1.8.

RIVALS: recompute the verdicts under V2 regimes and call that the mirror — a different object (scout U2 H4).
Compare `lens_word` — empty on the maker row. Read "12h FAIL" as both tolls — the contract names one word; the
maker row is printed beside. Read the ALL-era rows — X's rows of record are holdout.

FAILS-IF: F-VA-MIRROR (a)-(d); mutations on COPIES of the parquet: the 4h taker `would_read` flipped; the 1h maker
row's `era` changed (0 rows); the mirror pointed at `lens_word`; a `licence("12h", "taker", "holdout")` request
must HALT.

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
  failure followed by a travel to the far edge is the very trade the stop times); the count of legs containing a
  PROBING bar is printed.
- **Unit and statistic.** `b1` in bars of the lens. Per lens ℓ ∈ {1h, 4h, 12h, 1d}:
  `T_ℓ = traverse_pin(b1 of the legs whose COMPLETION bar closes ≤ ERA_CUT, pooled over the five home assets)` =
  `ceil(median)`, by X's integer law (odd n: the middle value; even n: `(s[m−1] + s[m] + 1) // 2`).
- **Era (O-18).** Tuning legs only. A leg that starts in the tuning era and completes after ERA_CUT is not a
  tuning leg.
- **Freeze.** `va/TRAVERSE.json` (`by_lens.<ℓ>`: `T_of_record`, `n_legs`, `lower_hinge`, `median`, `upper_hinge`
  — the hinges are the medians of the lower and upper halves of the sorted legs, the middle value left out when n
  is odd, so that no quantile level is typed — per-asset medians, the label "T tuning-fit (in-sample for
  tuning-era trades)") and the per-leg table
  `va/traverse_legs.parquet` (`asset, lens, rid, leg_seq, from_side, start_i, end_i, start_close_ms,
  end_close_ms, b1, b2, n_probe_bars, both_touch_end, era_of_end`) are written ONCE by stage TC12-V, before any
  range book exists; `progress/TC12-V.json` pins both shas. **`va/TRAVERSE.json` is the traverse pin record**: its
  rows `traverse.<ℓ>` (source `by_lens.<ℓ>.T_of_record`) and `traverse.1h.in_5m_bars` enter the pin register as
  FITTED pins, and a consumer reads them only through the fitted-pin door, which HALTs unless the file's sha is
  the pinned one.
- **Floor.** `n_legs ≥` the floor (L-V.4) at 1h and 4h (the lenses with a registered consumer), else HALT
  `TRAVERSE-UNDER-FLOOR` and file an amendment. Under the floor at 12h or 1d: filed with `provisional: true`.
- **Printed beside, Tier-E, no pin:** the same statistic on the whole scored window (completion close ≤ X_PIN)
  and on the holdout slice; the `b2` distribution (hinges and median); X's pivot T (`PINS_X.json`
  `T.by_lens.<ℓ>.T_of_record`, which exists for 1h and 4h only) as the continuity column. The forward strip is
  never pooled (O-9).
- **12h and 1w.** The 12h row is computed and labelled "no consumer: 12h is closed for range trading". No 1w row
  (O-11).
- **The scalper's clock.** `T_5m = T_1h × (LENS_MS["1h"] // LENS_MS["5m"])`, the factor read by object from the
  env's `LENS_MS` (L-D); filed as `by_lens.1h.T_in_5m_bars`. Which bar the count starts from and where the trade
  exits are the scalper section's reading.
- **"Read, never typed."** Every range trade row carries `T`, and its book's manifest carries
  `time_stop_source = {path, key, sha256, value}`. The flow witness of the pin: bent by one bar at its door, the
  bar of a time-stop exit moves by one bar.

SOURCE: contract :42-43, :72, :100; O-18; `tc11x_ranges.py` `b_traverses` :787-810 ("a traverse completes at the
first bar touching the side OPPOSITE the current one (a both-touch bar completes it) — B1 = t − start, B2 = t −
the last touch of the departure side before t; then the side flips and start = t. The leg open at `end` … is
dropped"), `t_pin` :819-832; LEANS_X LX-X2.7 (:1226-1260), including the refusal of (D) "the harden-anchored time
to the far boundary … an outcome of the X2 event class"; scout U2 §1.10, R17; U6 R-17, R-18.

RIVALS: (a) touch by CLOSE — a close at or beyond an edge is a probe; the trades' targets and the scalper's entry
are resting orders that fill on the bar's range. (b) X's `TOUCH_EPS` tolerance (0.60 ATR) — a pivot-machine pin
with no value-area meaning. (c) `b2`, the pure transit — X filed it as a distribution only; `b1` is the filed
traverse X rode as a twin book. (d) time from a swing failure to the far edge — refused: an outcome of the traded
event class. (e) the whole corridor — leaks the holdout into the scalper's own time stop. (f) state INSIDE on every
bar of the leg — voids every leg that follows a failed probe. (g) the T-th 1h close after the fill instead of a 5m
count — depends on where in the hour the fill lands.

FAILS-IF: F-TRAV (a)-(e); mutations: a typed integer time stop in a copy of a consumer; a holdout leg planted in a
copy of the leg table; the touch test read against `VA(t)`; `T_5m` computed with a typed 12.

---------------------------------------------------------------------------------------------------------------
#### D · Stamps (V5)

**L-V.19 THE FUNNEL INSTANTS** — "every funnel instant of every book (base v6, 9/12, the gated books, every arm
below)" (contract :44)

READING: TC11's instant law, mirrored as `instants_of(frame, kind)` in the reader from
`tierc11_stage_r.instants_of` (`scripts/tierc11_stage_r.py:1267 ff.`; `KINDS` :213-216; `NEST_KEY` :258) — the
TC11 module is a runner that reaches the range layer and is never imported. Per campaign of a book: **every close
of the campaign's own lens from its start (the ARM close; the ENTRY close for a book without arming) through its
exit stamp of record, plus its named events**: `arm`, `entry`, `plus_1r` (intrabar: the OPEN of its bar) with its
close-stamped twin `plus_1r_post_event`, `harvest` (v6's band harvest: a close event), `bell`, `exit` (a stop or
target: the OPEN of its bar; a close event: its close) with `exit_post_event`, and `as_of_pin` for a campaign open
at the corridor pin (never `exit`). A range trade's first-target fill is an intrabar event declared by its owner
under the same OPEN-of-its-bar law, with a post-event twin. An event the campaign's own record says happened but
no source stamps HALTs the reader. Each book's owner declares its kind (lens, start) and any extra `ev_<name>_ms`
events through the regbook-schema frame (INTERFACE). Rejected armings (tide / d / no_trigger / position_open) are
not rows: TC11's law stamps entered campaigns.
**Who files what.** Stage V files no per-book table — no book exists when it runs. Each book stage calls the
reader's `stamp(instants_of(frame, kind))` on its own frame and files `VA_STAMPS_<book>.parquet` in its own stage
directory, key `[book, symbol, entry_ms, instant_kind, instant_ms]`, recorded in its own progress record. A gated
book is a key SUBSET of v6's instants: asserted `⊆`, never re-stamped.

SOURCE: TC11 LEANS L-R.5 (:218-223); `research_outputs/tierc11/stage_r/NEST_v6.parquet` (sha `de27be17…cb11`: 9,693
keys per scale_kind; kinds arm 200, bar_close 8,632, entry 200, plus_1r 103, plus_1r_post_event 103, harvest 55,
bell 4, exit 200, exit_post_event 196 — read while drafting) and `NEST_trg912.parquet` (sha `7c5ffe23…3ef9`);
scout U3 §1.10, R12; the sibling stage order (TC12-V precedes every book stage).

RIVALS: the whole arming funnel including rejected armings — no filed row law, no named consumer (OPEN TO OPERATOR
2). Entry instants only — the contract says "every funnel instant". A stamp at every lens bar of the corridor —
that is the per-bar table `va_bars_<ℓ>`, which exists anyway. A stamping door run after each book — a module call
where a join of filed rows suffices.

FAILS-IF: F-NEST-KEYS: on campaigns entered at or before X_PIN and instants ≤ X_PIN, the TC12 v6 key set
`(symbol, entry_ms, instant_kind, instant_ms)` equals `NEST_v6.parquet`'s at one scale_kind, and the 9/12 key set
equals `NEST_trg912.parquet`'s after dropping `as_of_pin` rows from TC11's side (a campaign open at TC11's pin
continues in TC12); mutation: one filed key dropped; a `plus_1r` stamped at its bar's close.

**L-V.20 THE VECTOR AT AN INSTANT** — "carries the VA vector at 1h, 4h, 12h, 1d, 1w" (contract :44-45)

READING: For an instant τ and lens ℓ, `k = asof_index(close_ms_ℓ, τ)` (L-V.8 rule 4). The block of lens ℓ is **row
k of the filed table `va_bars_<ℓ>.parquet`, whole and as filed** — TC11's law ("read at the last CLOSED bar of L at
or before the instant") made a pure join of data. `k = −1` → every column NULL and `state = UNDEFINED`. The block
(columns prefixed `<ℓ>_`):

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
`view["pct"][ks]`; `atr_L` = `tape.atr[ks]`), `nest_at` :1158-1183; TC11 LEANS L-R.5 (:224-232); O-14, O-16 (a);
the sibling readings L-0.22 ("columns of the Stage V tables, filed, manifest-pinned and as-of-joined") and L-0.28;
scout U2 R15, U6 §1.10.

RIVALS: the instant's own price against `VA(k)` as the vector of record — at an instant that IS a lens close it
measures the close against a profile containing it, and state and `pct` stop being coherent; it is the live
formula, by name, for the one consumer that needs it. The instant's price against `VA(k−1)` — a stale profile for
an order that rests after τ. Interpolating a forming higher-lens bar — a look-ahead. A module call per instant — a
decision module would have to import the module.

FAILS-IF: F-NEST-ASOF (a)-(c); mutations: listed there.

**L-V.21 BOUNDARY COINCIDENCE** — "BOUNDARY COINCIDENCE (an edge of L within 0.25 ATR_L of an edge of L+1)
["nest"]" (contract :45-46)

READING: The ladder is `1h → 4h → 12h → 1d → 1w` (TC11's `LADDER`, `scripts/tierc11_nest.py:101`); L+1 of 1w is
none. The door computes the coincidence PER BAR of the lower lens and files it in `va_bars_<ℓ>` — these columns are
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
gap in the lower tape breaks it, the block's seven fields are set NULL with the reason and the instant is counted
(`n_nest_gap_instants`, printed; never a stale flag).
`va_coincidence` is also what the door uses when a table needs an EVENT's frozen edge tested against the lens
above; whether a trading table asks for that, and with which level, is that table's reading.

SOURCE: `scripts/tierc11_nest.py` `within` / `coin_flags` :1016-1051 ("a LIVE boundary of L within frac x ATR_L
of EITHER live boundary of L+1 (all four pairings, inclusive)"), `COIN_FRAC` :108; TC11 LEANS L-R.5 (:233-235);
contract :45-46, :135; X's same-lens VA-vs-pivot coincidence (`tc11x_va.py:1069-1070`) is a different object; the
sibling stage table (Stage V files "the nest table").

RIVALS: ATR of L+1 — the contract says ATR_L. Same-side pairs only (VAH–VAH, VAL–VAL) — TC11's law is all four.
Judging profiles `VA(k−1)` — coincidence is a relation between two levels standing at τ, not a judgement of a
close. The POC as an "edge" — not an edge. Recomputing the flags per instant in each consumer — one law written in
several places; the door computes it once and files it. `analytics.nesting.va_nesting` — window-scale overlap
fractions, another object.

FAILS-IF: F-NEST-ASOF (a), (c) (flags recomputed by the fixture from the two raw windows); mutations: the
threshold taken in `ATR_U`; strict `<`; the L+1 profile taken at `up_k + 1`.

**L-V.22 THE TWELVE NEW ASSETS** — "Twelve new assets: 1h/4h/1d, Tier-E" (contract :46)

READING: For each of the twelve (the env's `UNSEEN12`, L-D), the series, the TPO twin, the machine and the
per-bar columns are built at 1h, 4h and 1d with the SAME `L_ℓ` as the home assets, each row labelled
`l_label = "CLASSIC5-fitted L (pooled tuning head); not fitted on this asset"`, and every row collared Tier-E
(`tier = "TIER-E"`, `selection_not_a_result = "a SELECTION, not a result"`, `gates = "nothing"`). Their 12h and 1w
blocks are NULL, and their rows carry `panel = "UNSEEN12"`. Coincidence follows TC11 without re-linking the
ladder: `1h` against `4h` is defined; the `4h` block's fields (its L+1 is 12h) and the `1d` block's fields (its L+1
is 1w) are NULL. A tape shorter than `L_ℓ + 1`
bars is UNDEFINED throughout and listed. The feasibility words, the licence and the traverse are CLASSIC5
quantities: no twelve-asset row enters the traverse pool, the mirror or any registered construction; they appear
only in views the contract marks Tier-E (":84 the full-corridor and 17-asset views Tier-E").

SOURCE: contract :18-20, :46, :84; O-8; TC11 LEANS L-R.5 (:237), `tierc11_nest.py` `nest_at` docstring ("For the
twelve, the 12h and 1w columns (and the 4h / 1d coincidence, whose L+1 is NA) are NA"); scout U2 R23.

RIVALS: a per-asset L for the twelve — needs a pivot run and X's per-asset twin scatters by a factor of two
(LEANS_X :1599-1600). Re-linking 4h → 1d for the twelve — not TC11's law. Pooling the twelve into the traverse —
changes the time stop of the registered rows.

FAILS-IF: F-VA-PINS (f): every twelve-asset row carries the collar and the label; its 12h/1w blocks are NULL; no
twelve-asset leg is in `traverse_legs.parquet`; mutation: a twelve-asset leg appended to a copy of the leg table.

---------------------------------------------------------------------------------------------------------------
#### E · Null, outputs, compute

**L-V.23 THE VOLUME NULL** — "null gaps+order (R10)" (contract :79), as it bears on the value area

READING: The value area's null OF RECORD in the estate is X's `tr_tercile_lblock`: a true-range-tercile-stratified
L-block volume PERMUTATION with random phase; prices untouched. `value_area.null_volume(volume=, true_range=,
lookback=, rng=)` mirrors it exactly: draw the phase `φ = rng.integers(0, lookback)`; blocks
`[0, φ), [φ, φ + lookback), …`; inside each block rank the bars by true range with a stable sort, stratum
`= len(TR_STRATA)·rank // m` for a block of m bars; permute the volumes inside each non-empty stratum with
`rng.permutation`, blocks then strata in order. `true_range` is `engine.indicators.true_range(h, l, c)`, computed
by the door and handed in. The door builds the stream `default_rng([SEED + draw, crc32("<asset>|<lens>|va")])`
with `SEED` = TC12's seed (contract :4) and runs the null draw count of L-V.4.
**Where it is used, and how it crosses the door:** only for Stage R's Tier-E two-trades table on the value area at
4h and 1d (contract :76-79). A draw needs the module (series → machine on the permuted volume), so the DOOR runs
the draws and files their events — `va/va_null_events.parquet`, the L-V.14 schema plus `draw`, `phase`,
`perm_sha`, for lenses 4h and 1d × the five home assets — and the table's owner computes its statistic per draw
from those filed events, outside the door. The percentile is mid-rank and is "a DESCRIPTION of where the real
value sits among the draws, never a p-value". Nowhere else: no registered verdict, no licence, no traverse, no
stamp. Whether that table also carries a gaps+order analog on value regimes is the range section's reading; this
generator is the VA null of record and is named as such on every row that uses it.

SOURCE: `tc11x_va.py` `null_rng` :1125-1127, `null_volume` :1130-1169 (`terc[order] = (3 * np.arange(m)) // m`,
:1161), `NULL_OF_RECORD` :236; LEANS_X LX-X3.13 (:1793-1809); AP-11 item 11; X's filed draws
`x_rec/tierc11x/null/null_va.parquet` (`rng`, `draw_info` = `"phase=<φ> shift=-1 perm_sha=<sha256 of the int64
index permutation>"`, read while drafting); scout U2 R18, H16.

RIVALS: re-use X's seed for TC12's draws — reproduces X's percentiles on a longer tape that X never saw; TC12's
seed is the contract's. The per-window permutation — rejected by X (it jitters the VA tenfold). gaps+order
relabelled onto a volume permutation — two different questions (`tc11x_va.py:195-197`). The table's owner running
the draws itself — it would have to import the module.

FAILS-IF: F-VA-NULL: with X's seed (`PINS_X.json` key `seed`) on the tape cut at X_PIN, the mirrored generator
reproduces the filed `phase` and `perm_sha` of every `tr_tercile_lblock` draw of the 20 cells; mutation: the draw
seed shifted by one (X's own plant).

**L-V.24 OUTPUTS, PRECISION AND THE COMPUTE PLAN** — "Stage V pins and the traverse table · the VA stack whole"
(contract :128)

READING: Stage `TC12-V` runs before any book exists and writes under `research_outputs/tierc12/va/`:

| file | key | content |
|---|---|---|
| `VA_PINS.json` | — | L-V.4, L-V.5 |
| `va_bars_<ℓ>.parquet`, ℓ ∈ {1h, 4h, 12h, 1d, 1w} | `[asset, open_ms]` | per bar: `panel`, `i`, `close_ms`, `era`, `in_strip`, `L`, `l_label`, `close`, `atr`, `volume`; the in-force profile `val, poc, vah`, the edges twin, `window_lo, window_hi`; the judging profile `val_j, poc_j, vah_j`; the TPO twin; the machine arrays; the L-V.16 columns; the nest columns of L-V.21 |
| `va_events.parquet`, `va_regimes.parquet` | L-V.14 | events and regimes of every cell |
| `va_null_events.parquet` | events key + `draw` | L-V.23 |
| `traverse_legs.parquet`, `TRAVERSE.json` | L-V.18 | the legs; the traverse pin record |
| `VA_MIRROR.json` | — | L-V.17; a registered record |
| `va_stack.parquet` | `[asset, lens, era]`; era ∈ {tuning (close ≤ ERA_CUT), holdout (ERA_CUT < close ≤ X_PIN), ALL (close ≤ X_PIN), strip (close > X_PIN, never pooled, O-9)} | THE VA STACK, whole: bars; bars per state; every event counter of L-V.13-14; regimes; the median value-area width in ATR; the TPO medians and counters of L-V.6; the share of bars with each nest flag; the counted cases of L-V.13 |
| `STAGE_V.md`, `build_manifest.json`, `FIXTURES_STAGE_V.txt` | — | the report page, the manifest (with `x_sources`), the transcript |

Every parquet goes through the estate's table law (section L-0): declared total key, floats rounded to 6 dp at
write, the nine as-of stamps, the collar on every table that is not registered — which is every parquet here.
What the build report quotes: its feasibility-mirror block from `VA_MIRROR.json`; its "Stage V pins and the
traverse table" from `VA_PINS.json` and `TRAVERSE.json`; its "VA stack whole" from `va_stack.parquet`, every cell.
**Precision.** Inside the door everything is computed at full float and rounded at write only. Outside the door
THE FILED VALUE IS THE VALUE OF RECORD: a consumer reads `state`, the flags, the events and the columns as filed and
never re-derives a state, an event or an inside/outside flag from filed levels (scout U2 H7); a consumer that
needs a LEVEL — an order at an edge, a target at the POC, a stop beyond `extreme` — uses the filed 6-dp value AS
the level. The door and the consumers therefore agree on every state by construction, and a level differs from
its full-float value by at most half a unit of the sixth decimal place.
**Compute.** 61 cells: 5 home assets × 5 lenses + 12 × 3. Per cell: two series passes (volume, TPO), one machine
pass per series, the columns, the traverse, the nest columns. One `spawn` worker per cell, each arming the TC12 env
before any I/O; at most 6 workers while the 1-minute load is below 10, else 2 (O-5); results merged in fixed
(lens, panel-order) key order before any write. X's build of record did 20 cells — each with all of X's series
twins, event variants and nulls at 20 draws — in 6m07s on 4 workers (`x_rec/tierc11x/progress/X3.json` →
`compute.build_of_record`: `workers 4`, `cells 20`, `wall "6m07s"`); Stage V's work per cell is a small fraction
of that, so the full build is a matter of minutes. A stamp is one `searchsorted` per (asset, lens) over a book's
instants. The scalper's 5m clock reads the 1h and 4h tables by as-of; **nothing is profiled at 5m**. The null runs
only for the ten cells its one consumer needs. Worker count and load go to `progress/` only, never into an
artifact.

SOURCE: O-1, O-5, O-6; `tierc2_baseline.py:155-188` (the table law); TC11 BOOKS precision law (scout U3 §1.5:
"flags are computed at full precision BEFORE rounding"); `progress/X3.json` `compute`; scout U2 H7; contract
:126-128 (the report's blocks); the sibling readings L-0.15 (grids whole), L-0.16 (the collar; registered tables).

RIVALS: consumers re-derive states from 6-dp levels — flips exact-edge cases (H7). A full-float sidecar or an
accessor into the door — a second copy of record, or a decision module importing the door. A 5m value area — not
in the contract.

FAILS-IF: F-STATE (f) ROUND-TRAP: on a synthetic tape whose close exceeds the full-float VAH but equals its 6-dp
rounding, the filed `state` must be PROBING_ABOVE (the door's full-float judgement) and the reader's stamp must
return that filed state; mutation: a reader copy that recomputes `state` from `close`, `val_j`, `vah_j` reads
INSIDE and must turn the leg RED. F-DET, F-KEY, F-GRID (on `va_stack`), F-COLLAR per directory are L-0's.

---------------------------------------------------------------------------------------------------------------
#### F · The fixture roll of this section

Common law (section L-0; X's LX-F.1): every leg prints `FAILS IF`; the BREAK plants run first, one at a time,
inside production or on a copy, and each must be caught by its NAMED detector — a plant not caught makes the
fixture VOID and RED; truncated-tape legs build fresh arrays (no memo); as-of legs hold L, N, M, K, F and T at
their filed values and say they do not test them. Fixture RNG: `default_rng([SEED, crc32(<tag>)])`, `SEED` =
contract :4. Suite `scripts/tierc12_va_fixtures.py`, transcript `va/FIXTURES_STAGE_V.txt`.

**F-VA-RAW** (contract :115-116)
- (a) THREE WINDOWS (the contract's count): one per lens 1h, 4h, 1d, eras alternating tuning / holdout / tuning,
  asset and bar drawn from the stream tagged `"va|F-VA-RAW"` (X's form, `tc11x_va_fixtures.py:310-323`).
  Production's (POC, VAL, VAH) == `analytics.profile.volume_profile` on the RAW snapshot slice read by explicit
  path == the fixture's own pure-Python loop, exactly; production's histogram == the house's bit for bit and
  within X's 1e-12 relative of the loop's (`tc11x_va_fixtures.py:348`).
- (b) EQ: the module == the house function on the whole BTCUSDT 1h tape and on a seeded sample of every cell (X's
  sample size, `sample_ts` default `k`, `tc11x_va_fixtures.py:397`); and two different `block` sizes give
  byte-equal series.
- (c) SERIES ANCHOR: on bars closing ≤ X_PIN of X's 20 cells, the module's values passed through the estate's
  write function == X's filed `poc, val, vah, val_edge, vah_edge, tpo_poc, tpo_val, tpo_vah` on every row, and the
  constant `L` column agrees.
- (d) TPO rows == a per-window `searchsorted` count, on seeded windows and on one constructed window holding a
  zero-volume flat bar (it must add one count to one row, and nothing to the volume histogram).
- FAILS IF: any level, histogram or filed value differs. PLANTS: the volume column shifted by one bar inside the
  door's loader — must FAIL on EACH of the three windows (the contract's plant) → (a); every interior edge nudged
  one ulp inside the core → (b); a block size made to truncate the last block → (b); the lookback of one lens moved
  by one bar in a copy of `VA_PINS.json` → (c); the TPO row index taken `side="left"` → (d); zero-volume bars
  dropped from the TPO count → (d).

**F-VA-ASOF** (contract :114-115)
- (a) PREFIX: on seeded cuts over the cells (X's 100, FIXTURES_X3.txt F-VA-ASOF), `VA(t)` from a FRESH tape cut
  after bar t (`load_asof_at`) == the full tape's `VA(t)`, exactly.
- (b) ALIGNMENT: the frame's `open_time` strictly increases and equals the tape's `open_ms` row for row, and
  production's (open, volume) pairs == the raw file's, on every cell.
- (c) JUDGING FRAME: every L-V.16 column and every probe's E recomputed by the fixture from the house profile of
  bars `t−L .. t−1`; exact.
- (d) MACHINE PREFIX: events with `known_at ≤ k` and states of bars ≤ k from a fresh prefix == the full tape's.
- FAILS IF: a prefix value differs; a row is misaligned; a column or an E differs from the `VA(t−1)` derivation.
  PLANTS: the window shifted one bar forward, `t−L+2 .. t+1` — "profile including bar t+1 must FAIL" (the
  contract's plant) → (a); the volume misaligned by one row → (b); the columns computed from `VA(t)` → (c); an
  acceptance stamped one bar early → (d).

**F-STATE** (contract :116-117: "3 acceptances + 3 swing failures hand-verified against V2")
- (a) SIX EVENTS chosen by a rule frozen HERE, before any V2 event exists: lens 4h, assets in the panel order of
  record (`tierc2_rules.UNIVERSE`), events by ascending `i`, holdout era first (tuning if the class has no holdout
  member; a class with no member at all makes the leg VOID and RED). A1 = the first acceptance `by n_closes`;
  A2 = the first `by margin` with `bars_out ≥ 1`; A3 = the first `by margin` with `bars_out == 0`; S1 = the first
  swing failure with `bars_out == 1`; S2 = the first with `bars_out == K`; S3 = the first on the side opposite
  S1's. Two boundary NON-events ride beside: N1 = the first lapse with `bars_out == K + 1`; N2 = the first decay
  after A1. "Hand-verified" = the fixture's own derivation sharing no code with the module — `VA(t0−1)` from the
  house function on the raw slice, ATR by its own Wilder loop, each clause written out per bar (close, E,
  `s·(c − E)/ATR`, count) and printed in the transcript — equal to production's tuple
  `(kind, side, t0, i, by, E, extreme)`.
- (b) TRANSITION TABLE: a synthetic tape GENERATED from (N, M, K) drives every row of L-V.13, including a close
  exactly at an edge, a return exactly at E, the N-th close, the margin on the open bar, returns at K and K + 1,
  decay, a blocked re-probe, an opposite probe under a standing acceptance, both sides disarmed, warm-up, and a
  zero-volume bar inside a probe (it counts as one close).
- (c) IDENTITIES: L-V.14's on every cell; `E ==` the edge of `VA(t0−1)` and `extreme ==` the raw max/min over
  `[t0, i]` on every event; the counted cases of L-V.13 printed.
- (d) = F-VA-ASOF (d). (e) ATR BAR: the first pending bar where `M·ATR[t]` and `M·ATR[t−1]` decide differently is
  found by rule and production must follow `ATR[t]`. (f) ROUND-TRAP (L-V.24).
- FAILS IF: any of the eight tuples, any table row, any identity differs, or the reader returns a state other than
  the filed one. PLANTS: `accept_n − 1` → A1; the margin clause removed → A2, A3; `ret_k + 1` → N1; `ret_k − 1` →
  S2; decay judged on pending bars → (b); E from `VA(t0)` → (c); the extreme without the return bar → (c); a dropped
  lapse row → (c); the margin read with `ATR[t−1]` → (e); a reader copy recomputing `state` from filed levels → (f).

**F-STATE-X** (contract :32-33: "X's semantics asserted equal on the 4h holdout sample") — L-V.15's legs, each
on X's 20 cells cut at X_PIN:
- (x1) `(N, none, 7)` == X's `record` rows. (x2) `(N, M, 7)` == X's `die_parity` rows. (x3) `(N, none, K)` == X's
  `k3` rows. (x4) V2 == `die_parity` with the relabel — **THE CONTRACT'S LEG on the 4h holdout**, binding on every
  lens and era. (x5) the TPO series at `(N, none, 7)` == X's `tpo` rows. (x6) the counters == the tracked
  manifest's `event_counts`, and the fresh full-float inside-flag == X's filed `close_in_va_prev` on every bar.
- FAILS IF: any key set, integer or string field, 6-dp float or counter differs. PLANTS: one-ulp edge nudge in
  the core → (x1); the margin read with `ATR[t−1]` → (x2); `ret_k + 1` handed to the k3 leg → (x3); the relabel
  threshold at `K + 1` → (x4); the era read from X's `era` column → (x4) (the acceptances collapse to 0); the TPO
  row index taken `side="left"` → (x5); one counter moved by one in a copy of the manifest → (x6).

**F-VA-MIRROR** (contract :116: "HALT on disagreement") — L-V.17's legs:
- (a) the five words by exact string equality on `would_read`. (b) the tracked manifest's `va_lens_verdicts`.
  (c) each word re-derived from its row's printed columns. (d) the licence set and the reader's guard.
- FAILS IF: any word, flag or re-derivation disagrees — and then Stage V HALTs and writes no `VA_MIRROR.json`.
  PLANTS, each on a COPY of X's record: the 4h taker `would_read` flipped → (a); the 1h maker row's `era` moved
  (zero rows) → (a); the mirror pointed at `lens_word` → (a); `va_lens_verdicts["1h"].maker_twin` changed → (b);
  `n_ranges` set under the floor on a PASS row → (c); a `licence("12h", "taker", "holdout")` request → (d).

**F-TRAV** (contract :117: "typed constant → FAIL")
- (a) AST "typed constant", the site-targeted leg beside L-0's general scan: in every non-fixture
  `scripts/tierc12_*.py` and in `analytics/value_area.py`, an integer literal passed as, or assigned to, a
  time-stop or traverse name FAILS; the factor of `T_5m` must be the `LENS_MS` quotient. (b) `T_ℓ` re-derived from
  `traverse_legs.parquet` == `TRAVERSE.json`. (c) every pooled leg's completion close ≤ ERA_CUT and its asset is a
  home asset. (d) the leg table rebuilt on FRESH tapes cut at ERA_CUT == the filed tuning legs row for row.
  (e) every range trade row's `T` == `TRAVERSE.json` (or `T_in_5m_bars`), and its manifest's `time_stop_source`
  sha is the pinned one.
- FAILS IF: any of the five. PLANTS: `time_stop = <an integer>` typed in a copy of a consumer → (a); a typed 12 as
  the 5m factor → (a); `T_of_record` moved by one in a copy of `TRAVERSE.json` → (b); a holdout leg planted in a
  copy of the leg table → (c), (d); the touch test read against `VA(t)` → (d); one trade row's `T` changed in a
  copy of a range book → (e).

**F-NEST-ASOF** (contract :46, :121: "a leaked future profile must FAIL")
- (a) PREFIX: for seeded funnel instants and the boundary set of (b), every lens tape of the asset is cut at τ
  (`load_asof_at`; the 1d and 1w tapes re-derived from the cut 4h by Stage D's law, complete days and weeks only),
  the DOOR rebuilds its per-bar rows on those tapes, and the reader's stamp at τ from those rows must equal the
  production stamp at τ from the filed tables, on every column of every block.
- (b) BOUNDARY: for each rung, τ exactly at an L+1 close (that bar IS read) and τ one lower-lens step before it
  (the previous bar is read).
- (c) INDEPENDENT: the block's levels and the seven coincidence fields recomputed by the fixture from the two raw
  windows with the house function; the gap guard exercised on a constructed lower tape with one bar removed (the
  seven fields must be NULL at the instants it hides, and counted).
- FAILS IF: any column differs, a boundary instant reads the wrong bar, or a hidden L+1 close yields a non-NULL
  flag. PLANTS: P1 inside the door, the as-of of the lens above shifted by +1 when `up_k` is computed — **a profile
  built through the unclosed higher-lens bar** — → (a), (b); P2 inside the door, a 1d (1w) bar synthesised from
  the 4h bars of the current incomplete day (week) and appended before the series is built → (a); P3 the judged
  columns from `VA(k)` → (c); P4 a reader copy that joins row `k + 1` → (a), (b); P5 the threshold in `ATR_U` →
  (c); P6 a reader copy without the gap guard → (c).

**F-NEST-KEYS** — L-V.19's anchor. FAILS IF: on campaigns entered at or before X_PIN and instants ≤ X_PIN, the v6
or 9/12 key set built by the reader's `instants_of` differs from TC11's filed nest tables (9/12 after dropping
TC11's `as_of_pin` rows), or a gated book's keys are not a subset of v6's. PLANTS: one filed key dropped from a
copy; a `plus_1r` stamped at its bar's close; a key added to a copy of a gated book.

**F-VA-NULL** — L-V.23's mirror proof. FAILS IF: with X's seed on the tape cut at X_PIN, the `phase` or the
`perm_sha` of any `tr_tercile_lblock` draw of X's 20 cells differs from the filed `draw_info`. PLANT: the draw
seed shifted by one inside the door's stream builder.

**F-VA-PINS**
- (a) lookbacks: `VA_PINS.json` == `PINS_X.json` == `va/build_manifest.json` `pins.L.<ℓ>.record` == the `L`
  column of X's `va_series_<ℓ>`; 1w == the 1d value, labelled BORROWED.
- (b) every row of L-V.4's table: the first source == each cross source.
- (c) FLOW, Stage V's share of L-0's flow leg: each pin of L-V.4's table bent at its door, inside production, must
  move its witness on a seeded sample; a pin whose bend moves nothing is `PIN-NOT-READ`.
- (d) the `L` column of every Stage V table == `VA_PINS.json`.
- (e) no registered construction, gate, licence or traverse reads a `1w_` column (the registration specs'
  declared VA reads, and an AST scan of the builders).
- (f) L-V.22's: the collar and the label on every twelve-asset row; NULL 12h and 1w blocks; no twelve-asset leg
  in the traverse pool.
- FAILS IF: any of the six. PLANTS: one L moved by one in a copy of `PINS_X.json` → (a); `pins.laws.break_margin`
  changed in a copy of X's manifest → (b); a door copy that ignores the handed K and uses its own copy of it → (c);
  the `L` column changed in a copy of a table → (d); a copy of a registered arm's spec that reads `1w_state` →
  (e); a twelve-asset leg appended to a copy of the leg table → (f).

Owned by section L-0 and run on this stage's files: F-WALL and F-TYPED on `analytics/value_area.py`; F-CLOSURE on
the door (its two conditions) and on the reader (a fresh interpreter importing it holds no
`analytics.value_area`); F-DET, F-KEY, F-COLLAR per directory; F-GRID on `va_stack.parquet`.

---------------------------------------------------------------------------------------------------------------
#### G · Unverified at drafting — checked at build, each a HALT or a printed count

- UNVERIFIED: prefix identity of the TC12 snapshot to TC11's (Stage D's fixture). Every equality leg against X
  assumes it.
- UNVERIFIED: that no degenerate window (zero total volume, or `hi <= lo`) occurs after warm-up on the 1w tapes
  and on the twelve's tapes. X's manifest proves it for its 20 cells only (`volume_sources.<cell>` keys
  `zero_or_negative_volume`, `nonfinite_volume`). Counted per cell; HALT per L-V.3.
- UNVERIFIED: that every twelve-asset tape holds at least `L_ℓ + 1` bars at each of its lenses. Short tapes are
  listed and UNDEFINED.
- UNVERIFIED: that the traverse pool clears the floor at 1h and 4h. HALT `TRAVERSE-UNDER-FLOOR` otherwise.
- UNVERIFIED: that each F-STATE (a) class has a member on the 4h tapes. A missing class makes the leg VOID.
- UNVERIFIED: that the correct-until-stable TPO row index reproduces X's filed `tpo_*` series (X's code stops after
  a fixed number of passes). F-VA-RAW (c), (d) decide it; a difference HALTs for an amendment.
- UNVERIFIED: bit-exactness under the interpreter of the build. It rests on numpy's `linspace`, first-max
  `argmax` and summation order; F-VA-RAW (b) and (c) are the guard, and the manifest records the numpy, pandas
  and pyarrow versions.
- UNVERIFIED: that the tapes are nested and gap-free at every lens close a funnel instant reads. The reader's gap
  guard counts the exceptions (L-V.21).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPECS

None. L-V owns no registered row. The five rows (P-ADM-1, P-BRD-1, P-DIR-1, P-SFP-VA-1, P-SCALP-3) belong to
L-G, L-R and L-S; what each reads from this section is listed under INTERFACE ASSUMPTIONS.

---------------------------------------------------------------------------------------------------------------
### OPEN TO OPERATOR

1. **The 1w lookback.** X pinned none and X's law cannot be applied at 1w from filed records (L-V.5). DEFAULT if
   silent: `L_1w` = the 1d pin's bar count, labelled BORROWED, stamp-only, Tier-E, read by no registered
   construction. Alternatives only the operator can order: "1w NA" (the 1w block and the 1d rung's coincidence
   become NULL with the reason; the lens-above conditioning of the 1d trades in Stage R's Tier-E table becomes an
   NA cell), or a commissioned fresh computation of X's law at 1w (a pivot run on whole-tape picks, under the
   floor, in-sample everywhere).
2. **Rejected armings.** "Every funnel instant" is read as TC11's law: entered campaigns from arm to exit.
   DEFAULT if silent: armings rejected before entry carry no stamp. Stamping them is a contract amendment.

---------------------------------------------------------------------------------------------------------------
### INTERFACE ASSUMPTIONS

**What L-V hands the other sections (their open asks, answered here):**
- To L-0: the typed door list gains exactly ONE member from this section, `scripts/tierc12_va.py`.
  `scripts/tierc12_va_stamps.py` is NOT a door: it is data-only and imports neither the module nor the door.
  `analytics/value_area.py` is numpy-only, keyword-only, default-free, structural literals only (L-V.2). The
  mirror's licence record `va/VA_MIRROR.json` IS a registered record (collar-exempt; L-V.17). The traverse pin
  record is `va/TRAVERSE.json` (L-V.18). The per-member bar-close columns of the V5 vector are
  `<ℓ>_bar_close_ms` for ℓ ∈ {1h, 4h, 12h, 1d, 1w} (L-V.20). "The nest table" Stage V files is the nest columns of
  `va_bars_<ℓ>` (L-V.21); the per-book stamp tables are filed by each book stage. The contract pin map rows this
  section needs: `va.accept_n` (:35), `va.accept_margin_atr` (:35), `va.sfp_k` (:36, also :135), `va.nest_frac`
  (:45, also :135), `va.value_area_pct` (:29, held equal to the lineage object), `va.mirror_words` (:39-40) and
  `va.licence_set` (:41). AM-V2 (L-V.15) is filed in the amendments file at freeze.
- To L-D: this section's X records, read through the sha-first reader, are the rows of L-V.1's table plus
  `tierc11x/null/build_manifest.json`; its TC11 records, read through the allow-listed reader, are
  `stage_r/NEST_v6.parquet`, `stage_r/NEST_trg912.parquet`, `ranges/SCALE_GRID.parquet` and
  `ranges/SCALE_PICKS.json`. Every frame is taken through `load_asof` / `load_asof_at`. The door imports the env
  first and the module after it. The zero-volume law is honoured as L-V.6 and L-V.7 state, with the counts
  printed. `maker_pin.differs_from_x_assumption` is printed beside the "1h maker PASS" word (L-V.17 item 10).
- To L-X: a range row's precondition item cites `va/VA_MIRROR.json` by the selector of L-V.17 item 8; the report's
  mirror, pins-and-traverse and VA-stack blocks quote the files named in L-V.24; the dated V2-versus-X amendment is
  the text of record in L-V.15.

**What L-V assumes of them:**
- **L-D (substrate + env):** the snapshot `tc12_20261008` with PREFIX IDENTITY to `tc11_20260925` proven before
  Stage V; the frames of L-V.7 including derived 1d and 1w WITH volume for all seventeen stems' applicable lenses;
  `load_asof`, `load_asof_at`, the sha-first X reader, the allow-listed TC11 reader; the corridor pin and TC11's
  pin by object; `LENS_MS`; the home and twelve panels in their order of record; `ATR_LEN` and
  `PROVISIONAL_MIN_N` as lineage objects; the era function (tuning iff close ≤ ERA_CUT); the Stage D derivation
  law callable on a cut 4h tape (F-NEST-ASOF (a)).
- **L-0 (laws/process):** the fixture common law and harness; the table law (6 dp, keys, as-of stamps, collar,
  registered list); F-WALL, F-TYPED, F-TYPED-FLOW, F-CLOSURE, F-DET, F-KEY, F-GRID, F-COLLAR; the contract pin
  door, the fitted-pin door and the pin register; `tierc12_asof.asof_index`; `PCT_PER_UNIT`; the stage order
  (TC12-V complete before any book stage; the traverse frozen before any range book).
- **L-C (control):** the v6 and 9/12 books on the extended corridor with campaign frames in the regbook schema
  and the event stamps the instant law needs (arm close, entry close, +1R open stamp, harvest close, exit event
  stamp); their `VA_STAMPS_<book>` tables filed through the reader; the count of rejected armings by reason.
- **L-G (admission):** each gated book as a key subset of v6. L-G's two registered rows read no VA column.
- **L-R (range-state):** reads `4h_state` (and `1d_state`) from the stamps for P-DIR-1 and the chop table, and
  `pct` as bar k's judged column; consumes `va_events` swing_failure rows for P-SFP-VA-1 and decides in its own
  readings (i) whether an entry requires `ret_inside_frozen` / `ret_inside_rolling`, (ii) which filed profile
  (`*_f` or `*_n`) sets POC and far edge, (iii) the invalidation event (an `acceptance` row on the faded side),
  (iv) the breakout-retest scan on V2 acceptances, computed outside the door from the filed acceptance rows and
  the tape (X's `scan_retests` / `retest_verdict`, `tc11x_va.py:674-728`), (v) the lens-above conditioning cells,
  (vi) the statistic it computes per null draw from `va_null_events`, and whether a gaps+order analog rides
  beside. It calls the reader's `licence` before any range book and reads T through the fitted-pin door.
- **L-S (scalper):** as-of joins the 1h and 4h tables onto 5m closes and applies the live formulas of L-V.20 on
  the filed columns; decides the order geometry (the in-force `val` / `poc` / `vah` / `atr` at the trigger), what
  it does when the trigger instant is a lens close, the anchor bar of `T_in_5m_bars`, and cancellation on an
  `acceptance` event; declares its instants frame (trigger, fill, T1, exit, and the MISS orders' instants).
- **L-X (statistics + registrations):** each registration spec lists the VA columns and files it reads
  (F-VA-PINS (e) scans that list); the labels of O-23 and the "T tuning-fit" and "tuning-window L" labels are
  carried on the rows that read T and L.
- **L-L (ledger + era + ferry):** the ferry class of the Stage V row files (`va_bars_*`, `va_events`, the
  per-book stamp tables).

---------------------------------------------------------------------------------------------------------------
### OBJECTIONS

None on the facts. One gap, read under L-V.5 rather than objected to: O-15's key path
`L.by_lens.<lens>.L_of_record` has no `1w` entry (`PINS_X.json` carries four lenses), while O-11 names a 1w
value-area stamp column.
