## L-D · SUBSTRATE TOP-UP AND THE ENVIRONMENT

This section governs contract lines 18-23 (Stage D: the pin, the snapshot, the fetch, venue of record, the sha
manifest, the LaCie mirror, F-D-2, F-D-3, the fee schedule and its maker pin) and the environment every later stage
runs under: the vendored shim `scripts/tierc12_env.py`, its write-protection, its by-object pins, the as-of cuts that
give TC11-corridor reads on the TC12 snapshot, the tick of record, and the lineage modules that are imported as-is.
It owns NO registered row. It conforms to ORCHESTRATOR_RULINGS O-1..O-32; two objections were filed from this
section and both were accepted (O-26, O-27; see OBJECTIONS). Nothing here computes or reads any outcome of any book.

**Abbreviations in SOURCE lines.** M = `/Users/luis/Naiad` (branch `v12-v1-census`).
- T12 = `M/research_outputs/tierc12`; a bare `data/…`, `env/…`, `vendor/…`, `progress/…` or `pins/…` path below is
  under it.
- CON = the contract `M/exchange/queue/2026-10-08_TC12_APOLLO.md` (sha256 `861d6050…a7bd`), cited `:line`.
- OR = `M/research_outputs/tierc12/ORCHESTRATOR_RULINGS.md`.
- D11 = `M/scripts/tierc11_data.py` (`b2fe090f…8dcc`) · D10 = `M/scripts/tierc10_data.py` (`2cbf9bb6…15fc`).
- FX10 = `M/scripts/tierc10_data_fixtures.py` (`3807d905…1587`) · FX11 = `M/scripts/tierc11_data_fixtures.py`
  (`0e621e04…a5e0`).
- ED = `M/engine/data.py` (`ddee4020…c88f`) · ENV11 = `M/scripts/tierc11_env.py` (`1526093b…f798`).
- MR = `M/research_outputs/tierc11` · XR = `M/research_outputs/tierc12/x_rec` (the byte copies of TC11-X).
- XD = `XR/scripts/tc11x_data.py` (`c73ca805…b4d6`) · XF = `XR/scripts/tc11x_env_fixtures.py` (`b1bea520…bcfc`).
- U3 / U4 / U6 = the scout maps under `M/research_outputs/tierc12/scout/`.
- "[verified here]" = opened and checked by this drafter on 2026-10-08; "[scout]" = taken from a scout map and
  re-checked where a reading stands on it. Every sha above was re-hashed here. The shas printed in this block and
  in SOURCE lines are ORIENTATION for a reviewer: code reads each from the record that certifies it (TC11's
  PROGRESS `artifact_shas`, `XR/X_REC_MANIFEST.json`, `progress/STEP_Q.json`), never from this text.

**The register of constants this section uses — every one READ, none typed.** The "value" column is orientation
only and is never typed into code; the build reads the object in the last column.

| constant | value (orientation) | read at run time from |
|---|---|---|
| contract sha256 at STEP Q | `861d6050…a7bd` | `progress/STEP_Q.json` → `artifact_shas[<contract path>].sha256` — PROVENANCE of the filing instant; the pin of record of the contract is L-0.1's prefix sha, and nothing in this section compares the live contract file with this value |
| seed | 20261008 | CON:4 ("Seed 20261008") through L-0's contract-pin door (`scripts/tierc12_pins.py`; filed value in `pins/CONTRACT_PINS.json`) |
| STEP Q commit · its instant | `28e006b` · 2026-10-08T22:52:13Z | `progress/STEP_Q.json` → `commit`, and the ISO instant in `one_line` (regex `committed (\S+Z)`); held equal to git's committer time by F-D-PIN |
| unit identities | 100 bps per percent | L-0's `scripts/tierc12_units.py` objects (`BPS_PER_UNIT / PCT_PER_UNIT`); ms from an instant by `timedelta` division (L-D.1) |
| TC12 pin `PIN` | 1791489600000 = 2026-10-08T20:00:00Z | derived, L-D.1; asserted equal to the 13-digit value printed at OR:56 |
| TC11 pin `TC11_PIN` | 1790294400000 = 2026-09-25T00:00:00Z | `MR/data/AS_OF_PIN.json["as_of_last_closed_4h_close_ms"]` (file sha `4f609ccf…e4bd`) |
| TC10 pin `TC10_PIN` | 1790006400000 = 2026-09-21T16:00:00Z | the same file, key `tc10_pin_close_ms` |
| `MS_4H` and every native step | 14400000 … | `engine.cells.INTERVAL_MS` (`M/engine/cells.py:9-16`) |
| `DAY_MS`, `WEEK_MS`, Monday anchor | 86400000 · 7 d · 4 d | D11:224-226, read by AST (`source_literal`) |
| `FUNDING_JITTER_MS` | 60000 | D11:241, read by AST |
| `CHUNK_BARS`, `WEIGHT_SOFT_CAP`, `RETRIES`, `BYBIT_*` | 15000 · 1200 · 6 · … | D11:303-312, read by AST |
| era cut `ERA_CUT_MS` | 1719791999000 | ENV11:128, read by AST (Stage D) / the vendored shim's own unchanged line (ENV) |
| taker bps per side · round trip | 5.0 · 10.0 | the objects `tierc2_rules.FEE_BPS_SIDE`, `FEE_BPS_ROUND_TRIP` (`M/scripts/tierc2_rules.py:122-123`) |
| maker bps per side ON FILE | 2.0 | `M/README.md:150` by the regex `maker is (\d+(?:\.\d+)?)%` × 100 (D11:275-287) |
| charter slippage tiers | A 2 · B 5 · C 10 | `CONTRACT_SLIPPAGE_CLAUSE` (D10:217-220), read by AST and parsed (D11:246-270) |
| tick per stem | BTC 0.10 … | `M/research_outputs/tierc12/data/CONTRACT_SPECS.json` → `assets[].price_tick` (a string) |
| drive-wait attempts · delay | 6 · 3.0 s | the objects `drive_wait.DEFAULT_ATTEMPTS`, `DEFAULT_DELAY` (`M/scripts/drive_wait.py:105-106`) |
| every certified TC11 sha | — | `MR/PROGRESS.json` → the `artifact_shas[<path>].sha256` of the entry of `stages[]` whose `stage` is the certifying stage (PROGRESS sha read from `progress/TC12-R0.json["frozen_estate_shas_at_r0"]`, or the stamped value `T12/close/TC11_STAMP_MAP.json` names for it when that map reads `applied: true` — L-0.24; the Stage D builder, both fixture suites and the shim all accept PROGRESS under this one rule) |
| every X record sha | — | `XR/X_REC_MANIFEST.json` → `files[].sha256`, row matched on `copy` (manifest sha read through `tierc12_progress.certified`) |
| flat-bar attestation sample, per stem | 2 | FX10:600 (`size=min(2, len(t))` in `fd2_real`), read by AST by the builder; typed by the fixture as its commission (L-D.13) |
| `TickGrid` context limits | — | the stdlib objects `decimal.MAX_PREC`, `decimal.MAX_EMAX`, `decimal.MIN_EMIN` (L-D.23) |

**The quotation law for ported and vendored text.** A literal inside a function proven AST-identical to its filed
source (F-D-PORT), or inside vendored text proven byte-identical to its referee outside the declared hunks (F-VENDOR),
is a QUOTATION of that source, not a typed number. Every NEW number a port or a hunk introduces is read from the
register above.

---------------------------------------------------------------------------------------------------------------
### A · The pin

**L-D.1 THE PIN** — "funding through the latest CLOSED 4h bar (= the corridor pin, printed)" (contract :19)
READING: the corridor pin is the close of the latest 4h bar that was closed when STEP Q was committed (O-7), taken
BY OBJECT and never typed:
- **The instant** is read from the filed STEP Q record `progress/STEP_Q.json` (its sha asserted against the `_record`
  entry `PROGRESS.json` carries for STEP Q): the ISO stamp matched once in its `one_line` by `committed (\S+Z)`,
  parsed with the format `%Y-%m-%dT%H:%M:%SZ` as UTC. Exactly one match or HALT.
  `ct_ms = (instant − datetime.fromtimestamp(0, utc)) // timedelta(milliseconds=1)` — an exact integer, with no
  conversion constant typed. The Stage D builder runs no git; F-D-PIN (a fixture, where a read-only git call is
  allowed) holds that instant equal to the COMMITTER time of the commit the record names, and holds that commit to be
  the one that added the contract file.
- `PIN = (ct_ms // MS_4H) * MS_4H` — the largest multiple of the 4h step that is ≤ the commit instant; a 4h bar closes
  on every such multiple (UTC grid, anchor 0). `PIN_OPEN = PIN − MS_4H`.
- [verified here] `git show -s --format=%ct 28e006b` → 1791499933 = 2026-10-08T22:52:13Z (author time identical), the
  instant STEP_Q.json prints → `PIN` 1791489600000 = 2026-10-08T20:00:00Z, bar open 16:00:00Z. The build asserts `PIN`
  equals the 13-digit value printed in O-7's paragraph (OR:56, parsed from that file — a second object) and that
  `(PIN − TC11_PIN) // MS_4H` equals the bar count that paragraph prints (83).
- **Per-lens last closed bar at the pin** is one formula, ported VERBATIM (D11:458-461):
  `target_last_open(iv, PIN) = ((PIN − step − anchor) // step) * step + anchor`, anchor = the Monday offset for 1w,
  else 0. Orientation: 5m 19:55Z · 15m 19:45Z · 1h 19:00Z · 4h 16:00Z · 12h 2026-10-08T00:00Z · 1d 2026-10-07 · 1w
  2026-09-28 (closes 2026-10-05T00:00Z). The 2026-10-08 daily bar and the week of 2026-10-05 are NOT closed at the pin
  and exist in no file.
- **The write-once record** `M/research_outputs/tierc12/data/AS_OF_PIN.json`, written once by the `--pin` subcommand
  of `scripts/tierc12_data.py` through `_dump_once` (D11:438-444; a second write HALTs; a resumed run re-reads and
  re-checks). It carries
  EVERY key of TC11's pin record (25 keys, the set read from `MR/data/AS_OF_PIN.json` at run time — so
  `tierc10_panel.stage_d_pin` (`M/scripts/tierc10_panel.py:634-647`) and `tierc10_data.load_pin` consume it unchanged)
  with TC12's values, plus: `tc11_pin_close_ms`, `tc11_pin`, `bars_4h_past_tc11_pin`, `step_q` {`commit`, `instant`,
  `record_path`, `record_sha256`, `contract_path`, `contract_sha256`}, `pin_derivation` (the formula above as text),
  `bybit_server_time_ms`, `bybit_kline_of_pinned_bar`, `bybit_pin_bar_closed`. `seed` = the contract's seed.
  It is a PROVENANCE record (it holds clocks) and is never in the determinism set (L-D.11).
- **Every later read is by object:** Stage D reads this file; the shim reads it (L-D.26 hunk 3); no `scripts/tierc12_*`
  source holds the pin, TC11's pin or TC10's pin as a NEW literal, as an int or as an ISO string. "The STEP Q
  instant" that other sections cite (L-L's `entered_before_contract_filed`) is this reading's `ct_ms`, filed as
  `step_q.instant` and held equal to `progress/STEP_Q.json` and to git by F-D-PIN.
SOURCE: O-7 (OR:55-59); TC11 L-0.1 (`MR/LEANS.md:21-26`); D11:178 (the typed precedent this reading replaces),
D11:719-793 `pin_as_of`, D11:678-710 `pin_findings`; `progress/STEP_Q.json`; git commit
`28e006bc5def421bd65e3835a95a2905c4e21b93` [verified here].
RIVALS: (a) the venue clock at the first fetch run (TC10's `pin_as_of`, D10:472-517) — not taken: O-7; it moves with
the hour the executor chooses to run. (b) the pin typed as a literal (D11:178) — not taken: CON:8. (c) author time
instead of committer time — equal here; committer time is of record because it is when the filing entered the branch.
(d) the next close (2026-10-09T00:00Z), which would add the 2026-10-08 daily bar — not taken: O-7; it is chosen after
STEP Q. (e) a git call inside the Stage D builder — not taken: the filed STEP Q record supplies the instant, and L-0
allows that builder one out-of-process site (the clone).
FAILS-IF: F-D-PIN (L-D.15; six blocks `F-D-PIN [a]` … `[f]`). Planted mutations: a copy of the module with a typed
pin one bar later (must be RED at "pin != derivation from STEP Q"); a STEP_Q.json copy whose instant is moved by four
hours (RED at "instant != git committer time"); a pin off the 4h modulus; a pin record rewritten after the seal.

**L-D.2 THE VENUE PROOF AND THE LATEST-AT-FETCH BAR** — "the latest CLOSED 4h bar" (contract :19)
READING: "closed" is proven against EACH venue of record's own clock at `--pin`, inside a `CallLog` block (every HTTP
request one `kind='http'` row of `data/FETCH_LOG.jsonl`):
- **Binance** (venue of record of 16 stems; witness symbol = `CLASSIC5[0]`, read from `tierc2_rules.UNIVERSE`):
  `S_b = GET /fapi/v1/time → serverTime`; `GET /fapi/v1/klines symbol=<witness> interval=4h startTime=endTime=PIN_OPEN
  limit=1`. HALT unless the row's open == `PIN_OPEN`, its `closeTime == PIN − 1` and `closeTime < S_b`. This is D11's
  law (D11:737-750) with the pin by object.
- **Bybit** (MNT's venue): one call, `GET /v5/market/kline` with `category=linear`, `symbol` = MNT's symbol from the
  venue table, `interval=BYBIT_IV["4h"]`, `start=end=PIN_OPEN`, `limit=1`. HALT unless exactly one row is returned
  with start == `PIN_OPEN`, and `PIN < S_y`, where `S_y` is the venue's clock in the v5 response ENVELOPE (the
  top-level `time` field, milliseconds). Bybit rows carry no closeTime: closure is start + step ≤ PIN < the venue
  clock. UNVERIFIED: that the envelope carries `time` in milliseconds — the build HALTs if the field is absent or
  is not an integer with as many digits as Binance's `serverTime` read in the same run (a unit check with no typed
  constant).
- **The latest closed 4h at the pin run** `L = (S_b // MS_4H) * MS_4H` is read off the same clock, its own kline is
  fetched and proven closed, and it is PRINTED beside the pin and FILED (`latest_closed_4h_at_pin_run*`,
  `pin_equals_latest_closed_at_pin_run`). Any run after 2026-10-09T00:00Z prints `False` there; that is a fact, not
  a fault.
- `record_fetch_clock` (D11:804-823, ported with a Bybit row added) files one `kind='clock'` row per venue AFTER the
  pin and BEFORE the first fetch and the seal, on every networked subcommand.
- The R0 scout's three unauthenticated GETs (U4 §1.16) are NOT the proof: they are in no FETCH_LOG and nothing they
  returned was saved. The manifest carries that sentence under `standing_disclosures`.
SOURCE: D11:669-675, :719-793, :796-823; U4 §1.16 (Bybit answers the FORMING bar newest-first); O-7.
RIVALS: Binance's clock alone (TC11) — not taken: MNT's tape is fetched from a venue whose clock TC11 never read.
FAILS-IF: `F-D-PIN [d]`: FAILS IF the filed Binance closeTime ≠ pin − 1 or is not before the filed venue clock, or
the filed Bybit clock is not past the pin. Planted mutations (offline, on stubbed venue answers handed to a copy of
the proof function): a row whose closeTime ≥ serverTime ("still forming") and a Bybit clock ≤ PIN must each HALT.

---------------------------------------------------------------------------------------------------------------
### B · The snapshot and the fetch

**L-D.3 THE SNAPSHOT AND ITS GUARD** — "STAGE D · SUBSTRATE TOP-UP" (contract :18)
READING: the substrate of record is a NEW frozen snapshot `~/.cache/naiad/snapshots/tc12_<pin UTC date yyyymmdd>` =
`tc12_20261008` (O-8); the build asserts the suffix equals the pin's UTC date. A top-up is a new snapshot plus a
re-root, never an in-place extension.
- **Clone** (`--clone`, the one subcommand that runs without the guard): `cp -cpR <tc11_20260925> <tc12_20261008>`
  (APFS clonefile) ONLY when the target does not exist. Then EVERY file of the clone (the whole tree walk, hidden
  files included) is re-hashed against TC11's filed manifest `MR/data/STAGE_D_MANIFEST.json` — `files[].sha256` (124)
  and `out_of_scope_snapshot_files[].sha256` (52) — BEFORE any extension; the manifest's own sha is asserted equal to
  the one TC11's PROGRESS certifies (`0d8da587…c712`); the clone's file set must equal the source tree's file set.
  Any mismatch HALTs, leaves the clone for inspection and files nothing. Result: write-once
  `data/CLONE_ATTEST.json` (D11:548-602 with the reference changed from TC10's manifest to TC11's). A target that
  exists without a filed attestation, or an attestation without its target, HALTs.
  [verified here: the TC11 snapshot holds 176 files, 818 MB, and the manifest hashes to the certified sha; scout U4
  §1.1 re-hashed all 176 files equal to that manifest.]
- **Guard** `guard_substrate(env)`, at import of `scripts/tierc12_data.py`, before `engine.data` is imported: HALT
  unless `NAIAD_CACHE_DIR` is set; is absolute AS GIVEN (no `~`, no relative path — `engine.data.cache_dir()` binds
  `Path(env)` unexpanded and `mkdir`s it, ED:39-48); does not name the live cache, the TC10 snapshot or the TC11
  snapshot (tested on the string, then resolved); resolves to exactly the TC12 snapshot; and that directory holds
  `klines/`. `_assert_bound()` (D11:486-492) re-checks `ED.cache_dir()` before EVERY snapshot write.
- **What is never read or written.** The live cache `~/.cache/naiad/data_cache`: never read, never written (by
  construction — guard + bound; the manifest carries `live_cache_touched: false` with that basis, D11:314-318). The
  TC10 and TC11 snapshots: never written. The TC11 snapshot is READ only by `--clone` (as source) and by the Stage D
  fixtures F-D-CLONE, F-D-PREFIX and F-D-UNTOUCHED (explicit absolute paths, plain processes, never through a bound
  loader); the TC10 snapshot only by F-D-UNTOUCHED's re-hash. Under the armed shim both are read-never (L-D.27).
- `scripts/tierc12_data.py` NEVER imports the shim (it arms the hook and re-roots the lineage) and no
  `tierc10_data` / `tierc11_data` module (each HALTs at import off its own snapshot, D10:94-117, D11:87-125).
SOURCE: O-8 (OR:61-66), O-3, O-5; TC11 L-0.2 (`MR/LEANS.md:28-32`); D11:82-125, :486-492, :499-602.
RIVALS: extend `tc11_20260925` in place — not taken: O-3, it destroys the substrate TC11's and X's pending close acts
re-verify. Read the live cache — not taken: O-8; it is 15 days stale, has no 12h/funding past 2026-08-15, no 1d/1w,
no SUI/MNT, mixed publications (U4 §1.2, §1.5). A fresh full-history REST fetch — not taken: it would replace the
ARCHIVE-carrying history of seven stems with today's REST publication, moving the prefix F-CTRL stands on (U4 §1.10).
FAILS-IF: F-D-GUARD (each bad `NAIAD_CACHE_DIR` must HALT before `engine.data` loads; mutation: a copy of the guard
with its final equality test removed ACCEPTS the planted TC11 path and must be caught by the fixture's own check);
F-D-CLONE (mutation: one flipped byte in a temp copy of a cloned file → "sha != reference"); F-D-BOUND.

**L-D.4 FETCH SCOPE** — "five home assets {BTC ETH SOL NEAR ZEC}USDT.P klines {5m,1h,4h,12h,1d,1w} + funding … the
twelve new assets 1h/4h/1d only" (contract :18-20)
READING: the fetch scope is TC11's scope of record BY OBJECT (O-26), ported — `scope_paths()` (D11:471-477) — and
is asserted equal, as a set of relative paths, to `MR/data/STAGE_D_MANIFEST.json files[].path` (124 paths, read by
key; no count is typed): 17 stems × native {5m, 1h, 4h, 12h} (68 files, fetched) + CLASSIC5 × 15m (5, fetched) +
17 × derived {1d, 1w} (34, never fetched, L-D.8) + 17 funding tapes (fetched).
- It is a SUPERSET of the contract's list, disclosed as one (TC11 lean D11-a, D11:351-353). The contract's "twelve new
  assets 1h/4h/1d only" binds which LENSES Stage V stamps for the twelve (O-8), not which tapes the snapshot carries.
  The superset keeps one uniform edge per lens, keeps `complete_to_as_of` STRICT on every in-scope file (D11-f,
  D11:371-373), gives F-D-3 its "per asset" tapes and the 17-asset Tier-E views their 5m and funding.
- `{…}USDT.P` is a charting suffix: the stems and venue symbols of record are `BTCUSDT … ZECUSDT` (L-D.10).
- The 52 out-of-scope files of the clone (15m of non-CLASSIC5 stems × 15, 1m × 10, the out-of-panel stems' 5m/1h/4h/
  12h × 22, 4 out-of-panel funding tapes, the root `MANIFEST.json`) ride along UNTOUCHED, are listed by sha under
  `out_of_scope_snapshot_files`, must still hash to TC11's manifest after the build, and are unreadable under the
  armed shim (L-D.27 — several end in 2026-08 or at TC10's edge).
- No TC12 stage reads 15m; the five 15m tapes are extended only so that no in-scope file ends short of the pin.
SOURCE: O-26 (OR:184-186), O-8 (OR:61-66); D11:230-233, :464-477; `MR/data/STAGE_D_MANIFEST.json` [verified here:
124 `files[]` = 107 klines (73 native, 34 derived) + 17 funding; 52 out-of-scope; every `rows_after_as_of` 0; every
`gap_count` 0]; U4 §2.7, R3, R14.
RIVALS: the contract's literal list (5 × {5m,1h,4h,12h} + 5 funding; 12 × {1h,4h}) with every other tape left at
TC11's edge as out-of-scope — not taken: O-8, O-26; it leaves in-scope-looking tapes of the twelve 13 days stale and
F-D-3 "per asset" without the twelve's funding. The scope without the five 15m tapes (O-8's parenthesis read
literally) — not taken: O-26 (the parenthesis omitted them; the scope is TC11's 124 paths). Native 1d/1w fetched —
not taken, L-D.8.
FAILS-IF: F-D-SCOPE — FAILS IF `scope_paths()`, `PRE_STATE.json` files, or the manifest's `files[].path` differ as a
set from TC11's manifest `files[].path`. Mutations: a path dropped; a 15m path added for a non-CLASSIC5 stem.

**L-D.5 THE RUN ORDER OF `scripts/tierc12_data.py`** — "sha manifest" (contract :20)
READING: the module is a PORT of D11 (L-D.11's port law). Subcommands `--clone`, `--pin`, `--fetch`, `--derive`,
`--seal`, `--manifest`, `--mirror`, `--all`; exactly one per invocation. All records land in
`M/research_outputs/tierc12/data/`. Run lines (a `$HOME`-expanded absolute path, never `~`):

    export NAIAD_CACHE_DIR="$HOME/.cache/naiad/snapshots/tc12_20261008" PYTHONDONTWRITEBYTECODE=1
    ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/tierc12_data.py --all


| step | act | record | law |
|---:|---|---|---|
| 0 | import: `guard_substrate` | — | L-D.3 |
| 1 | `--clone` (alone, no guard): clone, re-hash vs TC11's manifest | `CLONE_ATTEST.json` (write-once) | L-D.3 |
| 2 | `--pin`: derive the pin, prove it closed on both venue clocks, file the latest-at-run bar | `AS_OF_PIN.json` (write-once) + `kind='clock'` rows | L-D.1, L-D.2 |
| 3a | `--fetch`: contract specs, ONE reach per venue; HALT if any symbol of record is not TRADING / perpetual | `CONTRACT_SPECS.json` (write-once) | L-D.22 |
| 3b | pre-state ledger of all 124 in-scope files BEFORE the first fetch: file sha, rows, edges, content sha, TC11's manifest sha it must equal | `PRE_STATE.json` (write-once) | L-D.6 |
| 3c | the seam audit, read-only | `EDGE_AUDIT.json` (write-once) | L-D.6 |
| 3d | the fee-source capture, one request per venue (no parsing) | `FEE_SOURCE.json` (write-once) + the response bodies | L-D.18 |
| 3e | extension, in D11's order: 4h, 12h, 1h; funding; 15m (CLASSIC5); 5m | `FETCH_LOG.jsonl` rows `klines` / `funding` / `http` | L-D.6, L-D.7 |
| 3f | the flat-bar attestation capture, only once 3e is complete for every in-scope native file: the seeded 5m sample and every zero-volume flat bar among the rows TC12 added, each re-asked of the venue; nothing it fetches is saved to a tape or under the snapshot | `FLAT_BAR_ATTEST.json` (write-once) + `http` rows, phase `flat_attest` | L-D.13 |
| 4 | `--derive`: 1d and 1w re-derived from the extended native 4h | the 34 derived files | L-D.8 |
| 5 | `--seal`: pin the provenance records' bytes and the fetch log's line prefix, once | `WRITE_ONCE_SEAL.json` (write-once) | L-D.11 |
| 6 | `--manifest`: no network, no snapshot write, no clock; the fee extraction runs here (it HALTs while a captured venue has no grammar of record) | `STAGE_D_MANIFEST.json`, `.md`, `fee_schedule.json`, `TICK_GRID_AUDIT.json` | L-D.11, L-D.18, L-D.19, L-D.22 |
| 7 | `scripts/tierc12_data_fixtures.py` — offline: no leg of it makes a network call (L-0.14 D) | `FIXTURES_DATA.txt`; `progress/TC12-D.json` | L-D.15 |
| 8 | `--mirror`, then `scripts/tierc12_data_fixtures.py --stage=TC12-D.mirror` (the non-blocking child record `TC12-D.mirror`; nothing waits on it) | `MIRROR_ATTEST.json`; the PROVENANCE transcript `FIXTURES_MIRROR.txt`; `progress/TC12-D.mirror.json` | L-D.24 |

`--all` = steps 2 → clock row → 3a-3f → 4 → 5 → 6 (D11's `run_all`, D11:2584-2608: it SEALS BEFORE it describes).
Exit codes are D11's: 0 complete · 2 fetch incomplete (a re-run resumes from each file's edge; write-once records are
re-read, never rewritten; the 3f record is not filed while a venue it must ask cannot be reached) · 1 HALT. `--all`
exits 1 if `prefix_attestation.all_ok` is False. On its first run `--all` stops at step 6 with exit 1 for any venue
whose fee page was captured with HTTP 200, until that venue's grammar amendment is ruled (L-D.18); steps 1-5 are then
complete and are not repeated — `--manifest` alone is re-run.
SOURCE: D11:59-62, :1386-1422, :2584-2647; U4 §1.5.
RIVALS: describe before sealing (TC10's first order) — not taken: D11-g (D11:374-377), the manifest's `write_once`
block must verify a FILED seal.
FAILS-IF: F-D-FETCHPATH (offline, on a temp snapshot the module is bound to, against stub venues): FAILS IF a HALT
of the fetch path does not fire, a `--fetch` resume over the filed snapshot asks or saves anything, the flat-bar
capture runs before the extension is complete, or the fetch path replayed from clone-time bytes does not reproduce
the filed content. Mutations: a copy of `run_fetch` that fetches before `write_pre_state`; a copy that captures the
flat bars before the 5m extension.

**L-D.6 THE EXTENSION RULE — ZERO OVERLAP; HISTORY CANNOT BE OVERWRITTEN** — "SUBSTRATE TOP-UP" (contract :18)
READING: every tape is extended over REST ONLY, forward, from ITS OWN edge, and the first stamp asked for is one step
PAST that edge.
- **Klines**, per in-scope native (stem, iv): `edge = max(open_time)` of the file; `cursor = edge + STEP_MS[iv]`;
  `tgt = target_last_open(iv, PIN)`. HALT if the file is absent, is not in `PRE_STATE.json`, or `cursor ≤
  PRE_STATE.files[rel].last_ms` ("an early start would overwrite"). Chunks of `CHUNK_BARS`: fetch `[lo, hi]` with
  `hi ≤ tgt`; keep rows with `lo ≤ open_time ≤ hi`; `_assert_grid` (an off-grid venue stamp HALTs); `_assert_bound`;
  `ED._save_cache` (merge, no-shrink, same-directory temp + `os.replace`); one `kind='klines'` log row;
  `binance_brake()`. This is D11's `extend_klines` with its logic unchanged (D11:1311-1354; a TEXT-ONLY port under
  L-D.11), the pre-state reference being TC11's edge.
- **Why zero overlap and not a one-bar overlap:** `ED._save_cache` keeps the NEW row at an identical `open_time`
  (`drop_duplicates("open_time", keep="last")`, ED:179-182). With `cursor = edge + step` no fetched stamp can equal a
  stored one, so the merge can only append. An overlapping start would let today's REST publication replace an
  inherited bar — and on seven stems the inherited history is ARCHIVE-assembled and differs from REST on incident bars
  (U4 §1.10).
- **Funding**: `end = PIN + FUNDING_JITTER_MS`. Binance tapes through `ED.backfill_funding(symbol, first_4h_open −
  DAY_MS, end)`, whose cursor is the file's `max(funding_time) + 1` (ED:352-356) — strictly new prints. MNT through
  `bybit_funding(symbol, old_edge + 1, end)` (paged backward from `end`, D11:950-974) then `ED._save_funding`. A tape
  whose edge already floors to the pin's hour is skipped ("nothing can be due"). An absent tape HALTs. This is D11's
  `extend_funding` with its logic unchanged (D11:1359-1383; TEXT-ONLY).
- **Row accounting, asserted per native kline file:** `tc12_rows_added` equals `(tgt − PRE_STATE.last_ms) //
  STEP_MS[iv]` minus the bars missing in the new stretch. Gaps are COUNTED and LISTED per file and NEVER filled
  (TC11's `gap_policy`, carried), and any gap leaves the manifest's `complete` False (L-D.11). Orientation, from the
  two pins by the formula: + 3984 (5m) · 1328 (15m) · 332 (1h) · 83 (4h) · 27 (12h) rows per stem; derived + 13 (1d)
  · 2 (1w); funding + 41 prints (8h tapes) or + 83 (4h tapes).
- **No 404 feeds a file.** `ED._get` returns a 404 as success (ED:68). Before `--derive`, the run's `kind='http'` rows
  of the phases that feed a file (`fetch`) are asserted to hold no status 404; every other non-200 row there is a
  retried transient, counted and printed. The phases `fee_source` (L-D.18) and `flat_attest` (L-D.13) feed no file:
  a 404 there is a recorded answer.
- **REST only.** No file is ever fed from the bulk archive. (The flat-bar attestation capture of L-D.13 READS the
  archive to attribute inherited bars and saves nothing.) F-D-1 (which of the venue's two publications is the
  record on incident bars) stays TC10's open operator question, carried in `operator_rulings_needed`, not re-opened,
  not re-cut; rows TC12 adds are REST by construction and the manifest says so per file (`publication`).
- **The seam audit** (`EDGE_AUDIT.json`, write-once, READ-ONLY). TC11's audit compared the inherited rows past TC10's
  as-of; in the TC12 clone that population is EMPTY (every TC11 manifest row has `rows_after_as_of` 0 [verified
  here]) and the record says so rather than being dropped. TC12's audit compares THE SEAM BAR — the last inherited row
  of each of the 73 native in-scope kline files — with the venue's REST bar of the same stamp, exact float equality on
  O, H, L, C, V, and the last inherited funding print of each of the 17 tapes with the venue's print of that hour (rate
  equality). Nothing fetched there is saved to any file. A difference is a DISCLOSURE (`inherited_edge_audit` in the
  manifest), never a repair and never a HALT: a prefix is never rewritten.
SOURCE: D11 lean D11-b (D11:354-359); D11:1161-1205 (`write_pre_state`), :1219-1281 (`audit_inherited_rows`),
:1285-1305 (`verify_prefixes`), :1311-1383; ED:160-186, :202-217, :349-382; U4 hazard H4.
RIVALS: overlap by one bar and assert equality before saving — not taken: one wrong branch overwrites; the read-only
seam audit gives the same evidence with no write path. The bulk archive for the new stretch — not taken: no monthly
zip exists for the running month; TC10 and TC11 fetched REST only.
FAILS-IF: F-D-FETCHPATH, detector "early start" — FAILS IF an extension can start at or behind a file's `PRE_STATE`
edge. Planted mutations: a copy of `extend_klines` whose cursor is `edge` (one-bar overlap) must HALT at "is not
past the PRE_STATE edge"; and a mutant with that HALT removed, run on a TEMP snapshot against a stub venue that
returns a different bar at the edge stamp, must be caught by the prefix comparator of F-D-PREFIX [i] ("old-prefix
content sha moved").

**L-D.7 THE FORMING-BAR GUARD** — "the latest CLOSED 4h bar" (contract :19)
READING: no bar that is not closed at the pin can reach a file. Four clauses, all required:
- **G1** the fetch target is a function of the PIN alone — `tgt = target_last_open(iv, PIN)` — never the venue's
  "latest", never a wall clock. Every request carries `endTime` / `end` = `hi ≤ tgt`.
- **G2** the reply is filtered to `[lo, hi]` BEFORE any save (D11:1340). Bybit answers newest-first and returns the
  FORMING bar when a window reaches it (U4 §1.16, GET 3); Binance does when `endTime ≥ now`.
- **G3** before the first kline request to a venue in a run, that venue's clock is read and must be past the PIN
  (L-D.2's `S_b`, `S_y`); so every bar whose `open_time + step ≤ PIN` is closed on the clock of the venue that serves
  it.
- **G4** after the fetch, on every in-scope kline file: `max(open_time) + STEP_MS[iv] ≤ PIN` (`rows_after_as_of == 0`)
  and the file ends EXACTLY at `target_last_open(iv, PIN)`; on every funding tape no print is stamped past
  `PIN + FUNDING_JITTER_MS`.
SOURCE: D11:925-946 (`bybit_klines`: one window = one page), :1311-1354; U4 hazard H5; U4 §1.16.
RIVALS: trust the venue's `end` parameter alone — not taken: it is a venue behaviour, not a law of this code.
FAILS-IF: F-D-FORMING — offline, a stub Bybit page and a stub Binance page each containing one bar with `open_time =
tgt + step`: FAILS IF any row past `tgt` is saved to the TEMP snapshot, or a stub venue clock ≤ PIN does not HALT.
Mutation: a copy of `extend_klines` with the `[lo, hi]` filter deleted → the stub's forming bar is saved → RED at "a
row past the pin was saved". F-D-EDGE holds G4 on the filed snapshot.

**L-D.8 1d AND 1w ARE DERIVED FROM NATIVE 4h; A DERIVED BAR IS NOT A SYNTHETIC BAR** — "klines {5m,1h,4h,12h,1d,1w}"
(contract :18) and "F-D-2 no synthetic bars" (contract :21)
READING:
- **1d** = exactly the SIX native 4h bars of one UTC day (`groupby(open_time // DAY_MS)`: open first, high max, low
  min, close last, volume sum); a day with fewer than six bars does not exist and is counted. **1w** = SEVEN such
  complete derived days, Monday-anchored UTC, complete weeks only. Source = native 4h closed at the pin, never 1h or
  5m aggregates (the venue's own intervals disagree on incident bars), never a native 1d/1w fetch. `derive_1d`,
  `derive_1w`, `derive_lenses`, `derive_in_memory`, `_write_if_changed` are VERBATIM ports (D11:1505-1583). After the
  extension both are re-derived WHOLE from the extended 4h tape.
- **"Synthetic" is TC10's filed definition, in its own words: "THE CLAIM IS 'Naiad inserted no bar', NOT 'the venue
  published no flat bar'"** (FX10:616-617). A synthetic bar is a bar Naiad PUT INTO A TAPE that the tape's source does
  not contain: a filled gap, a carried-forward bar, an interpolated or resampled bar, a manufactured bar before the
  first venue bar. A derived 1d/1w bar is none of these: it is a declared AGGREGATE of venue bars that all exist,
  re-derivable bit for bit, existing only when every child exists, labelled in the manifest on every row
  (`native: false`, `derived_from`, `derivation_content_sha`, `derived_file_equals_derivation`,
  `publication_inherited_from`). It is proven by its OWN fixture (F-D-DERIVE: an independent plain-loop rebuild), not
  by F-D-2's attribution leg — there is no venue bar to attribute it to.
- This is what X's 1d feasibility words were measured on (X's read set names "Stage D's derived 1d"), so F-VA-MIRROR's
  "1d taker PASS" is a statement about these bars.
SOURCE: TC10 LEAN L1 (D10:283-285); D11:232, :341-343, :1505-1583; FX10:491-620 (F-D-2), :623-704 (F-D-L1); FX11:71-74
(F-D11-DERIVE); `MR/data/STAGE_D_MANIFEST.json["derivation"]`; `M/engine/cells.py:9-16` (the estate fetcher has no 1d
or 1w interval).
RIVALS: fetch native 1d/1w — not taken: never done in the estate, it differs from the 4h tape on incident bars, the
fetcher cannot do it, and it would move X's 1d verdicts off the tape they were earned on. Call derived bars synthetic
and exempt them by name — not taken: the filed definition already excludes them by what it claims.
FAILS-IF: F-D-DERIVE (L-D.15); F-D-2's grid and flat-recount legs also run over the derived files.

**L-D.9 FUNDING "THROUGH THE LATEST CLOSED 4h BAR" AND THE PRINT AT THE PIN INSTANT** — "+ funding through the latest
CLOSED 4h bar" (contract :18-19)
READING:
- A funding print belongs to the hour its stamp FLOORS to: `funding_hour_ms = (funding_time // MS_1H) * MS_1H` (LEAN
  D-g). The venue's stamps sit 0 to a few tens of ms PAST the hour. Funding is FETCHED through `PIN +
  FUNDING_JITTER_MS` and READ as-of by `funding_hour_ms ≤ PIN` (`load_funding_asof`, VERBATIM D11:2513-2528;
  `with_funding_hour` HALTs on a stamp more than `FUNDING_JITTER_MS` past its hour).
- **At TC12's pin.** At the cadences TC11's manifest observed (4h: ENA, PUMP, HYPE, BONK; 8h: the other thirteen),
  2026-10-08T20:00Z is a funding hour of the 4h-cadence tapes only. Each such tape gains ONE print of the pin hour,
  stamped at or after the pin close, kept by the + jitter rule and counted
  (`prints_stamped_after_as_of_close_within_jitter`). It belongs to the bar that OPENS at the pin — the first bar past
  the corridor — so no corridor campaign pays it. The 8h tapes end at the 16:00Z print. The cadence of every tape is
  re-OBSERVED on the extended tape and printed; nothing is assumed from this sentence.
- **At TC11's pin — the one print that sits AT the pin instant.** [verified here, on the TC11 snapshot] every one of
  the 17 tapes holds exactly ONE print of the hour 2026-09-25T00:00Z: 16 Binance tapes stamped `TC11_PIN + 2 ms`, MNT
  (Bybit) stamped exactly `TC11_PIN`. TC11's manifest lists the 16 under `as_of_hazards`, key
  `funding_files_with_a_print_stamped_after_the_as_of_close`. Three consequences, each a rule:
  1. **In the prefix.** The funding prefix is cut on the FLOOR HOUR (`funding_hour_ms ≤ TC11_PIN`), never on the raw
     stamp. A raw cut `funding_time ≤ TC11_PIN` would drop the at-pin print from 16 tapes and keep it in one; the
     floor-hour cut keeps all 17, which is exactly the whole TC11 file (L-D.12).
  2. **In a look-back read.** `load_funding_asof_at(stem, TC11_PIN)` (L-D.28) returns that print, as TC11's own loader
     did.
  3. **In a ride.** The lineage charges a print to the bar whose OPEN is its hour (`M/scripts/tierc7.py:370-376`). The
     bar opening at TC11's pin did not exist on TC11's tape and DOES exist on TC12's: it is the first bar of the
     forward strip. A look-back ride with `hi = TC11_PIN − 1` ends at the bar opening `TC11_PIN − MS_4H` and never
     reads the print; a ride on the extended corridor charges it to the strip. That is the substrate fact L-C's F-CTRL
     stands on.
- `tierc2_baseline.load_funding` (whole file, no as-of cut, `{}` on a missing file) stays the lineage's reader; every
  tape ends within `PIN + FUNDING_JITTER_MS` by G4, and F-D-3 makes the silent `{}` unreachable.
SOURCE: D11:241, :344, :350, :1359-1383, :1622-1672, :2499-2528; U4 §1.8; U3 hazard H16; TC11 snapshot funding files
[verified here].
RIVALS: cut on the raw stamp — not taken (consequence 1). Attribute a print to the bar that CLOSES at its hour — not
taken: it is not the lineage's law and would move every filed `funding_r`.
FAILS-IF: `F-D-PREFIX [iv]` (L-D.12) — FAILS IF a funding prefix does not hold exactly one row of TC11's pin hour,
bit-identical to the last row of TC11's file (plant: the raw-stamp cut applied to a tape copy, which drops the
at-pin print); F-D-3 (L-D.14) — FAILS IF a print's floor hour is not its nearest hour or a print of an hour after
the pin is returned (plants there: a print stamped before its hour; one 30 min past it).

**L-D.10 VENUE OF RECORD; "NEVER SPLICED"** — "venue of record per TC10's Stage D table (never spliced)" (contract :20)
READING:
- **The object read at run time** is TC10's write-once venue probe `M/research_outputs/tierc10/data/VENUE_PROBE.json`
  (keys `classic5[]` + `unseen12[]`; fields `asset`, `venue`, `symbol`, `stem`), by ABSOLUTE main-tree path (it is
  gitignored, `M/.gitignore:263`), read-only. Its sha is asserted equal to the sha two TRACKED TC11 records carry for
  it — `MR/data/CONTRACT_SPECS.json`, key path `venue_of_record.sha256`, and `MR/data/STAGE_D_MANIFEST.json`, key path
  `tc10_record.venue_probe.sha256` (both `84981047…bc34` [verified here]).
- **"TC10's Stage D table"** is the table `M/research_outputs/tierc10/close/S3_STAGE_D.md:59-77` (17 rows at :61-77;
  the section is a byte-exact splice of TC10's manifest, :56). The build parses its (asset, venue, symbol, file stem)
  columns and requires THREE objects to agree row for row, 17 of 17: the table, the probe, and TC11's manifest
  `venues[]`. Any disagreement HALTs. The stems must be the commission's seventeen in the commission's order
  (`load_probe`, D11:834-841).
- The venue of a tape is decided ONCE (TC10) and is never re-probed. All five home assets are `BINANCE_USDTM`; 16 of
  17 stems are; MNT is `BYBIT_V5_LINEAR`, stem `MNTUSDT_BYBIT`. `PUMPFUN → PUMPUSDT` and `MNT → Bybit` remain TC10's
  open operator nods, carried in `operator_rulings_needed`.
- **"Never spliced" = every tape is ONE venue from its first row to its last.** Operationally (TC10's F-D-VENUE,
  FX10:927-993, ported): (i) every in-scope file's `venue` in the manifest equals its asset's venue of record; (ii)
  no `klines` / `funding` row of TC12's `FETCH_LOG.jsonl` names a venue other than the stem's, and every HTTP request
  of a file-feeding phase for a stem went to that venue's REST host (the attestation phase `flat_attest` of L-D.13
  feeds no file and asks the stem's own venue only: its REST host and, for an inherited Binance row, that venue's
  bulk-archive host); (iii) an alternate-venue tape carries the venue IN its stem
  (`BYBIT_STEM_SUFFIX`, D11:303, read by AST) and no default-named twin (`klines/MNTUSDT_<iv>.parquet`,
  `funding/MNTUSDT.parquet`) exists in the snapshot. The inherited prefix's venue purity is TC10's and TC11's
  certified result and is carried by the prefix identity (L-D.12).
SOURCE: D11 lean D11-c (D11:360-363), :834-846; `S3_STAGE_D.md` sha `eca42576…711c`; U4 §1.9.
RIVALS: TC11's manifest `venues[]` alone (tracked, convenient) — not taken as the object: the contract names TC10's
table; it is held equal instead. A fresh probe of `exchangeInfo` — not taken: a venue decided once is not re-decided;
`CONTRACT_SPECS` only proves the symbols are still TRADING.
FAILS-IF: F-D-VENUE — FAILS IF the table, the probe and TC11's manifest `venues[]` disagree on any row, or one of
(i)-(iii) above is false for any in-scope file. Mutations: a default-named twin `MNTUSDT_4h.parquet` in a COPY of
the snapshot listing; a `FETCH_LOG` row for a stem from the other venue in a COPY; one flipped `venue` in a COPY of
the probe (must be RED at "table / probe / manifest disagree").

**L-D.11 THE SHA MANIFEST, THE TWO RECORD CLASSES AND THE PORT LAW** — "sha manifest" (contract :20)
READING:
- **`data/STAGE_D_MANIFEST.json` (+ `.md`)** reproduces TC11's manifest schema KEY FOR KEY (41 top-level keys; the
  native / derived / funding row key sets), with these renames only: `tc11_extension → tc12_extension`; per-row
  `tc11_rows_added → tc12_rows_added` and `tc10_manifest_sha256 → tc11_manifest_sha256`; `tc10_record` kept and a
  `tc11_record` block added (manifest, pin, fee schedule, contract specs: path + sha); `carried_from_tc10 →
  carried_from_tc11` naming the three blocks carried VERBATIM from TC11's manifest (`two_token_trap`, `data_spend`,
  `venue_publications_disagree` — measured by TC10, not re-measured; the sha chain TC10 → TC11 → TC12 printed). New
  keys: `pins` (L-D.21), `tick_of_record` (L-D.22), `fee_sources` (L-D.20), `zero_volume_bars` (L-D.16). `mirror` is
  the constant sentence "see data/MIRROR_ATTEST.json — a provenance record outside the determinism set; the mirror's
  status is not carried here" (the manifest is never rewritten after the mirror). `tierc10_panel.resolve_unseen12` and
  `tierc10_data.panel` read `admission`, `venues` and `panels`, so those keep TC10's shape exactly.
- **Two shas per snapshot file:** `sha256` of the file bytes, and `content_sha = frame_sha(rows sorted by stamp)` —
  the raw little-endian column bytes (int64 for a `*_time` column, float64 otherwise), independent of the parquet
  writer (D11:416-425, VERBATIM). Identity claims are made on `content_sha`; file-byte equality only where a file was
  never rewritten.
- **THE DETERMINISM SET** = {`STAGE_D_MANIFEST.json`, `STAGE_D_MANIFEST.md`, `fee_schedule.json`,
  `TICK_GRID_AUDIT.json`}: written only by `--manifest`, from the snapshot, the sealed records, the saved fee-source
  bodies and the tracked `FEE_GRAMMAR.json`, with no network and no clock call; byte-identical across two subprocess
  builds under `PYTHONHASHSEED` 1 and the contract seed (F-D-DET). They are rebuilt, never write-once.
- **THE PROVENANCE SET** (clocks allowed; write-once through `_dump_once`; never in the determinism set) =
  {`AS_OF_PIN.json`, `CLONE_ATTEST.json`, `CONTRACT_SPECS.json`, `PRE_STATE.json`, `EDGE_AUDIT.json`,
  `FEE_SOURCE.json`, `FLAT_BAR_ATTEST.json`} — these seven are `SEALED_FILES` (TC11's five, D11:1427, plus the fee
  capture and the flat-bar attestation capture of L-D.13) — plus `WRITE_ONCE_SEAL.json` itself, `FETCH_LOG.jsonl`
  (append-only; its sealed LINE PREFIX is pinned), and, written after the seal under the child record
  `TC12-D.mirror`, `MIRROR_ATTEST.json` and (when a WOKE row exists) `DRIVE_WAKE_LOG_TC12.md` (L-D.24).
- **`complete`** is TC11's expression, ported unchanged (D11:2359-2372): every in-scope file present; every kline
  file ending exactly at its lens's last bar closing ≤ the pin with `gap_count`, `duplicates`, `off_grid`, `backward`
  and `rows_after_as_of` all 0; every funding tape's coverage `ok`; every derived file equal to its derivation; the
  prefix attestation `all_ok`; the seal `all_ok`; the clone attestation `all_equal`; the contract-multiplier table
  present; the carried two-token block intact — AND, new, the three-way venue agreement of L-D.10. A gap in any
  in-scope kline file therefore BLOCKS Stage D (exit 2): it is listed, never filled, and waits for the operator.
- **The port law.** `tierc12_data.py` carries a `PORTS` table (name → label and reason) and a provenance comment on
  every ported def naming D11's lines and sha. Three labels: VERBATIM = AST-identical to D11's function; TEXT-ONLY =
  AST-identical once every string constant is blanked (messages and docstrings name TC12; no logic moves);
  CHANGED = logic differs, the difference named. TEXT-ONLY: `extend_klines`, `extend_funding`,
  `capture_contract_specs`, `load_pin`. CHANGED, each named: `guard_substrate` (refuses the TC11 snapshot too),
  `clone_snapshot` / the expected-sha reader (TC11's manifest is the reference), `pin_as_of` / `pin_findings` (the pin
  by object; the Bybit proof), `load_probe` (three-way agreement), `write_pre_state` (TC11 shas per row),
  `audit_inherited_rows` (the seam bar), `record_fetch_clock` (a Bybit row), `run_fetch` (the fee capture; the
  flat-bar attestation capture; the no-404 assertion), `seal_provenance` (seven sealed files), `fee_schedule`
  (L-D.19), `build_manifest` (the renames above). Everything else D11 defines is VERBATIM. NEW:
  `capture_fee_sources`, `extract_fee`, `pct_to_bps`, `tick_grid_audit`, `is_zero_volume_flat`,
  `capture_flat_bar_attest` with its venue readers (the logic of FX10:137-262 — one bar by stamp from REST, one
  from the bulk archive, the field-equal comparison — re-issued through `ED._get` inside a `CallLog` block, so
  every request is a logged row and no retry count, pause or timeout is typed), `mirror_snapshot`,
  `load_asof_at(stem, iv, cut_ms)`, `load_funding_asof_at(stem, cut_ms)` (the cut law of L-D.28, for the Stage D
  fixtures, which cannot import the shim). Module-level constants that D11 holds as literals are READ from D11's
  source by AST (the register above).
- `tierc12_data.py` holds exactly ONE out-of-process call, a literal argv: `cp -cpR <src> <dst>` in
  `clone_snapshot` — the site `tierc12_data.clone_snapshot` of L-0.22's typed `SUBPROC_SITE_T`. It runs no git.
- Numeric literals: the module is scanned under L-0's typed-number law. A VERBATIM or TEXT-ONLY port's literals are
  the referee's (the quotation law); every CHANGED or NEW function holds structural literals only.
SOURCE: D11:1427, :1438-1500, :2075-2466, :2532-2555; U4 §1.14 (the key sets), hazard H10; FX11:140 (TC11's
`DET_FILES`), :166 (`CLOCK_FIELD`).
RIVALS: a new, smaller manifest schema — not taken: the re-rooted lineage readers and every reviewer's diff against
TC11 need the same keys.
FAILS-IF: F-D-MANIFEST — FAILS IF a top-level or row key set differs from TC11's under the rename table, a filed sha
does not re-hash, or the `.md` disagrees with the `.json` (mutations, on copies: a key dropped from the manifest; a
row's sha altered; one figure changed in the `.md`). F-D-PORT — L-D.15 (mutations: one token changed in a copy of
a VERBATIM port → "not AST-identical"; a comparison operator flipped in a copy of a TEXT-ONLY port → "differs outside
string constants"; a provenance comment naming the wrong sha). F-D-SEAL — FAILS IF one of the seven sealed records,
or a sealed line of the fetch log, is not the bytes the seal pinned (mutations: a sealed record rewritten in a temp
copy → "bytes moved since the seal"; a fetch-log sealed line changed). F-D-DET — L-D.15.

---------------------------------------------------------------------------------------------------------------
### C · The Stage D fixtures

**Common law of every leg in this section** (L-0.14's fixture law; TC11's form, FX11:4-11, carried):
- A LEG is one `prove` call and one transcript block; its block id is `<FID>` or `<FID> [<qualifier>]` (L-0.14 A,
  B). A fixture this section gives numbered or lettered legs files one block per leg (`F-D-2 [1]` … `[4]`,
  `F-D-PREFIX [i]` … `[iv]`, `F-D-PIN [a]` … `[f]`, `F-TOLL [data a]` … `[data g]`, `F-TICK [a]` … `[d]`); every
  other fixture named here is one block.
- Inside a leg the BREAK half runs first and must go RED, or the leg is VOID and counts RED; a plant counts as
  caught only when a finding NAMES the detector it was planted for; every plant is made on a COPY (a dict, a frame,
  a source text, a temp directory) — no real artifact moves.
- A leg that cannot run prints NOT RUN (L-0.14 C): the third leg state, written by the harness wrapper
  `not_run(fid, title, reason)` outside `prove`, never counted as PASS, counted in the tally and in the fixture
  record's `legs_not_run`. A NOT RUN block of a contract-named fixture (F-D-2, F-D-3, F-TOLL) is RED at TC12-FIX.
- No leg makes a network call, and no drive-dependent leg is part of a transcript of record (L-0.14 D): the venue
  is asked by the BUILDER, once, and its answers are sealed (L-D.13); F-MIRROR, the one drive-dependent leg, files
  the one PROVENANCE transcript (L-D.24).
- Fixture randomness (L-0.14 F): every stream is `numpy.random.default_rng([SEED, crc32("<suite tag>|<block id>")])`
  with `SEED` the contract seed through the pin door and suite tag `data` or `env`; each seeded leg's count is
  stated in its reading as a fixture-typed literal and printed in the transcript header.
- Both suites accept `--root=DIR` (L-0.14 H: the transcript, every twin and every temp copy go under DIR).
  Transcripts open with `as_of_last_closed_4h: <pin ISO>` (L-0.14 I; read from `data/AS_OF_PIN.json` — every record
  this section files sits at or after TC12-D) and carry no clock, no temp path and no absolute tree path.
- Banned: self-comparison; one example where cardinality was possible; a tolerance standing in for an identity.
- SCOPE (L-0.11's scope law): a leg that scans "the non-fixture `scripts/tierc12_*.py`" scans the sources named in
  `artifact_shas` of the records before its own in the resume order, plus its own record's modules, which the suite
  types (`scripts/tierc12_data.py` and `scripts/tierc12_tick.py` at TC12-D) — never a later stage's modules, so a
  transcript of record does not move when a later stage adds a module.

**L-D.12 F-D-PREFIX — PREFIX IDENTITY** — the ruling O-8: "every row with close ≤ TC11's pin is bit-identical to the
TC11 snapshot" (OR:65-66); contract :48-49 stands on it
READING: for every one of the 124 in-scope files, the rows of the TC12 file with CLOSE ≤ TC11's pin are bit-identical
to the TC11 snapshot's file.
- **"Close ≤ TC11's pin", per kind.** Kline row of lens iv: `open_time + STEP_MS[iv] ≤ TC11_PIN`. Funding row:
  `(funding_time // MS_1H) * MS_1H ≤ TC11_PIN` — the FLOOR HOUR, never the raw stamp (L-D.9).
- **"Bit-identical"** = the same number of rows, the same stamps, and the same raw little-endian column bytes:
  `frame_sha(prefix sorted by stamp, cols)` equal. Parquet FILE bytes are not compared for extended files (the writer
  rewrote them); they are compared for files that were not rewritten.
- **Four legs, all required** (blocks `F-D-PREFIX [i]` … `F-D-PREFIX [iv]`).
  (i) `verify_prefixes(PRE_STATE)` (VERBATIM D11:1285-1305): for each file, the rows at or before its OLD last stamp,
  read back from the CURRENT file, hash to the OLD `content_sha`; `all_ok` over 124.
  (ii) THE BYTE REFEREE, independent of PRE_STATE: for each file, `frame_sha` of the TC12 prefix (cut as defined
  above) == `frame_sha` of the WHOLE TC11 snapshot file read by explicit absolute path == TC11's manifest
  `files[path].content_sha`; row counts == `files[path].rows`; and the TC11 file's `sha256` == TC11's manifest
  `sha256`. (The whole TC11 file IS the prefix: TC11's manifest has `rows_after_as_of` 0 on every row.)
  (iii) every out-of-scope file's `sha256` == TC11's manifest `out_of_scope_snapshot_files[].sha256`; the file set
  of the TC12 snapshot == the union of TC11's manifest `files[].path` and `out_of_scope_snapshot_files[].path` (no
  stray file, none missing).
  (iv) THE AT-PIN PRINT: in each of the 17 funding prefixes there is exactly one row whose floor hour == `TC11_PIN`,
  bit-identical (stamp and rate) to the last row of the TC11 file; the number of tapes where that stamp is > `TC11_PIN`
  equals the length of TC11's manifest hazard list (read by key); and the first row AFTER the prefix has a floor hour
  > `TC11_PIN`.
- The derived 1d/1w files are in scope of all four legs: they are re-derived whole, so their prefix is identical
  exactly when the 4h prefix is.
SOURCE: O-8; D11:1161-1205, :1285-1305; FX11:63-64 (F-D11-PREFIX), :49-52 (F-D11-CLONE reads the previous snapshot
read-only — the precedent for leg (ii)); `MR/data/STAGE_D_MANIFEST.json`; U3 hazard H16.
RIVALS: PRE_STATE alone (leg (i)) — not taken as sufficient: PRE_STATE is written by the module under test; leg (ii)
is the second object. A raw-stamp funding cut — not taken (L-D.9).
FAILS-IF: FAILS IF any of (i)-(iv) is false for any file. Mutations, each on a temp copy of one file: a one-ulp change
of one historical `close` → RED at (ii) "content sha"; a row inserted behind the old edge → RED at (i) and (ii)
"prefix rows"; a bar manufactured BEFORE the tape's first bar (FX10's fourth F-D-2 plant: it sits in the inherited
prefix, which F-D-2's offline leg 4 cannot ask the venue about) → RED at (ii) "prefix rows"; the at-pin funding
print dropped (the raw-stamp cut applied) → RED at (iv) "at-pin print missing"; one byte flipped in an out-of-scope
file → RED at (iii).

**L-D.13 F-D-2 — NO SYNTHETIC BARS** — "F-D-2 no synthetic bars" (contract :21, :114)
READING: TC10's F-D-2 is ported (FX10:491-620) — its legs 1-3 whole, its venue-attribution leg re-formed as an
OFFLINE leg against a capture the builder seals — with its claim in its own words: "Naiad inserted no bar", not "the
venue published no flat bar". Population: every in-scope kline file (17 × {5m, 1h, 4h, 12h, 1d, 1w} as in FX10's
`ALL_IVS`, plus CLASSIC5 × 15m — 107 files, the count read from the scope object). Four legs, one block each
(`F-D-2 [1]` … `F-D-2 [4]`):
1. **Grid** (`_grid_faults`, independent of `scan_klines`): every `open_time` on its lens grid (anchor 0; Monday for
   1w), no duplicate, none backward.
2. **Flat-bar recount** (`_flat0`: o == h == l == c AND volume == 0): the recount of every file equals the manifest's
   `venue_zero_volume_flat_bars` for that file.
3. **Token scan**: none of FX10's `BANNED_TOKENS` (`ffill`, `bfill`, `fillna`, `interpolate`, `reindex`, `resample`,
   `asfreq`, `.pad(` — read from FX10:492 by AST) occurs in the CODE (comments and docstrings stripped by an AST
   round-trip, string literals kept) of the fetch-path sources `engine/data.py` and `scripts/tierc12_data.py`.
4. **Venue attribution — OFFLINE, against a sealed capture.** The venue's answers are captured ONCE, by the builder
   inside `--fetch` (step 3f of L-D.5: `capture_flat_bar_attest`, a `CallLog` block, phase `flat_attest`), as the
   write-once, sealed provenance record `data/FLAT_BAR_ATTEST.json`, listed in `SEALED_FILES`. Two populations:
   - (a) THE SEEDED 5m SAMPLE (FX10's, FX10:584-601). Stems in panel order; for each stem whose extended 5m tape
     holds at least one zero-volume flat bar, `rng.choice(stamps, size=min(n, len(stamps)), replace=False)` over
     that stem's flat-bar stamps in ascending order, all on ONE stream
     `numpy.random.default_rng([seed, crc32("data|F-D-2 [4]")])` (L-0.14 F; `seed` = the contract seed through
     the pin door). `n` = two per stem — FX10's count (FX10:600): the builder READS that literal from FX10's
     source by AST (the first argument of `min` in the `size=` keyword of the `rng.choice` call of `fd2_real`);
     the fixture TYPES it as its commission and prints it in its header.
   - (b) EVERY zero-volume flat bar among the rows TC12 ADDED (a stamp past the file's `PRE_STATE` edge), on every
     native lens of every in-scope file — cardinality, not a sample.
   Per bar the record holds: `stem`, `lens`, `open_ms`, the population(s) it belongs to, the tape's row, the
   venue's REST row at that stamp (its five O, H, L, C, V strings; null when the venue serves none), for a bar of
   the INHERITED prefix on a Binance stem also the bulk archive's row (the daily zip, then the monthly zip when
   the daily one is not field-equal; stamps normalised by the engine's own `ED._normalize_ms`), `publication` ∈
   {`both`, `rest`, `rest-only`, `archive-only`, `neither`} (FX10's `venue_published`, FX10:241-262), and the line
   range of its `kind='http'` rows in `FETCH_LOG.jsonl` (lines the seal's prefix pins). A TC12-added row is REST
   by construction and gets no archive fallback. The capture RECORDS and decides nothing: a bar the venue does
   not publish field-equal is filed as `neither` and is the fixture's RED, not the builder's HALT; a venue that
   cannot be reached leaves the record unfiled and `--fetch` incomplete (exit 2). It saves nothing to any tape
   and nothing under the snapshot.
   **The fixture leg** re-derives population (a) by its own seeded draw on the snapshot (its own `_flat0`, its own
   stream of the same expression) and population (b) by its own recount of the rows past each `PRE_STATE` edge;
   requires the record to hold exactly those bars; requires each bar of the snapshot to equal its sealed venue row
   field for field (`float(venue string) == ` the tape's float64 on O, H, L, C, V — the REST row, or for
   `archive-only` the archive row); and re-verifies the record's bytes against the seal. `archive-only` bars are
   LISTED in the transcript (REST serves a traded bar there now); they are not failures.
Derived 1d/1w are covered by legs 1-2 here and PROVEN by F-D-DERIVE (L-D.8), not by leg 4.
SOURCE: FX10:491-620 (F-D-2), :137-262 (the venue readers and `venue_published`) [verified here]; ED:62-74 (`_get`),
:77-80 (`_normalize_ms`); D11:613-666 (`CallLog`: every request one logged row), :1427 (`SEALED_FILES`); U4 §1.7
(TC11's own suite carries no leg by this name; none of the eight tokens occurs in `engine/data.py`, D10 or D11).
RIVALS: "no flat bar exists" — not taken: the venue publishes zero-volume flat bars during outages (L-D.16); deleting
or filling them would itself be the synthetic act. Dropping leg 4 because the fetch is REST-only — not taken: the
inherited prefix holds archive-assembled rows. An ONLINE leg 4 inside the transcript of record (FX10's form) — not
taken: the transcript must re-pass byte-identical on four runs, one of them inside a reviewer's worktree, and a
fixture that needs the venue cannot (L-0.14 D). A separate online transcript — not taken: the sealed capture gives
the venue's answer one filed, re-readable form, and no fixture leg touches the network.
FAILS-IF: FAILS IF [1] any `open_time` is off its lens grid, duplicated or backward; [2] a flat-bar recount differs
from the manifest; [3] a banned token appears in the fetch-path code; [4] a bar of population (a) or (b) is absent
from the sealed record, the record holds a bar outside the two populations, a bar is not field-equal to its sealed
venue row, a bar's `publication` is `neither`, or the record moved since the seal. Planted mutations, on copies:
an off-grid bar inserted into a 1h frame → RED at [1]; a carried-forward flat bar (the previous close four times,
volume 0) written over a real bar of a tape copy → the recount moves → RED at [2] "recount != manifest";
`def _planted(df): return df.ffill()` appended to a copy of `tierc12_data.py` → RED at [3]; the same carried-forward
flat bar written over a real bar among the TC12-ADDED rows of a tape copy → RED at [4] "absent from the sealed
record"; one field of one sealed venue row altered in a COPY of the record → RED at [4] "field differs"; one
sampled bar's entry removed from a COPY of the record → RED at [4] "absent". FX10's fourth plant — a bar
manufactured before the venue's first bar — is planted in F-D-PREFIX [ii] (L-D.12): it sits in the inherited
prefix, where the referee is TC11's file.

**L-D.14 F-D-3 — FUNDING COVERAGE PER ASSET** — "F-D-3 funding coverage per asset" (contract :21, :114)
READING: TC10's F-D-3 is ported whole (FX10:707-814). "Per asset" = per panel stem, all 17 (the five home assets and
the twelve). For each stem, at the TC12 pin:
- `funding_coverage(stem, PIN)` (VERBATIM D11:1654-1672) is `ok`: the tape exists, has a row at or before `PIN +
  FUNDING_JITTER_MS`, and `last_ms + FUNDING_JITTER_MS ≥ PIN − ivl × MS_1H`, where `ivl` is the OBSERVED interval
  (the median spacing of the last ten prints, else the modal spacing). The function's last-resort fallback constant
  is never consumed: the fixture asserts both observed intervals are non-null on all 17 tapes.
- `tierc2_baseline.load_funding(stem)` is NON-EMPTY (that loader returns `{}` silently on a missing file).
- THE FUNDING-HOUR LAW on every print returned by `load_funding_asof`: floor hour == nearest hour (no stamp sits
  before its hour), the loader's `funding_hour_ms` IS that hour, and no print of an hour after the pin comes out.
HALT-grade: a RED F-D-3 blocks every later stage (no book may ride funding-free).
The observed cadence per tape (interval tail and modal, the spacing histogram WHOLE) is printed in the manifest and
in `fee_schedule.json` rows.
SOURCE: FX10:707-814 [verified here]; D11:1622-1672; U4 §1.8.
RIVALS: the five home assets only — not taken: the contract says "per asset", the 17-asset Tier-E views journal
funding, and the superset fetch (L-D.4) carries the tapes.
FAILS-IF: FAILS IF any panel stem's funding file is absent or empty, its last stamp is older than the pin minus one
observed interval, `load_funding` returns `{}`, any print's floor hour differs from its nearest hour, the loader's
`funding_hour_ms` is missing or wrong, or a print of an hour after the pin is returned. Mutations (FX10's five, on
copies): a print stamped 10 ms BEFORE its hour; a print 30 min past its hour (the loader must HALT); a tape absent;
a tape's tail cut by four prints; `load_funding_asof` on a missing file (must HALT).

**L-D.15 THE STAGE D FIXTURE ROLL** — "FIXTURES (each states its failure condition)" (contract :114)
READING: one suite, two invocations, one transcript each (L-0.9: one transcript per fixture record, never a leg
filter):

| invocation | record | transcript | hosts |
|---|---|---|---|
| `scripts/tierc12_data_fixtures.py` | `TC12-D` | `data/FIXTURES_DATA.txt` | F-D-2, F-D-3, every F-D-* leg below, `F-TOLL [data a]` … `[data g]`, F-TICK |
| `scripts/tierc12_data_fixtures.py --stage=TC12-D.mirror` | `TC12-D.mirror` | `data/FIXTURES_MIRROR.txt` (PROVENANCE) | F-MIRROR (L-D.24) |

The suite HALTs unless `NAIAD_CACHE_DIR` is the TC12 snapshot, never imports the shim (at the TC12-D gate it does
not exist, and its post-shim would HALT on an uncertified Stage D), and makes no network call. Legs of
`data/FIXTURES_DATA.txt` not defined in their own reading above:

| leg | FAILS IF | planted mutation that must turn it RED |
|---|---|---|
| F-D-GUARD | the guard accepts an unset variable, a `~` or relative spelling, the live cache or a directory inside it, the TC10 or the TC11 snapshot, a foreign directory, or the TC12 path without `klines/`; or importing the module in a fresh interpreter under any of those does not HALT before `engine.data` loads | each bad value (one per detector); a guard copy with its final equality test removed (it accepts the TC11 path) |
| F-D-BOUND | a call that writes the snapshot does not sit behind `_assert_bound()` on every path, or a file-writing call sits outside the typed write owners | `NAIAD_CACHE_DIR` moved to a temp dir mid-process; a barrier removed in a source copy; a raw `to_parquet` appended |
| F-D-PORT | a port labelled VERBATIM is not AST-identical to its function in D11 at the sha TC11's PROGRESS certifies for that file (stage TC11-D; orientation `b2fe090f…`); a port labelled TEXT-ONLY differs from it once string constants are blanked; a provenance comment names the wrong lines or sha; or the port set read off the comments is not `PORTS` | one token changed in a copy of a VERBATIM port; a comparison flipped in a copy of a TEXT-ONLY port; a wrong sha in a comment |
| F-D-CLONE | any cloned file's sha differs from TC11's manifest, the clone's file set differs from the source's, or `CLONE_ATTEST.json` is not write-once | a flipped byte in a temp copy; a stray file added to a temp tree |
| F-D-PIN | (a) the filed pin ≠ the derivation from the instant in `progress/STEP_Q.json`, or that instant ≠ the committer time of the commit the record names (the fixture's read-only `git show -s --format=%ct`), or that commit is not the one that added the contract file (`git log --diff-filter=A`); (b) the pin ≠ the value printed in O-7's paragraph (OR:56); (c) it is not a 4h close, open ≠ close − 4h, or the ISO strings disagree; (d) the Binance closeTime ≠ pin − 1 or is not before the venue clock, or the Bybit clock is not past the pin (on the FILED record; L-D.2); (e) a non-fixture `scripts/tierc12_*.py` in this suite's scope (the common law's SCOPE: the sources recorded up to TC12-D) holds the pin, TC11's pin or TC10's pin as a new int literal or ISO string (AST + text scan); (f) the record moved since the seal or a rewrite gets through. Six blocks, `F-D-PIN [a]` … `[f]` | one plant per block: (a) a module copy with a typed pin one bar later, and a `STEP_Q.json` copy whose instant is moved by four hours; (b) a rulings copy whose printed value is one bar off; (c) a pin record copy off the 4h modulus; (d) L-D.2's two stubbed venue answers; (e) the pin as an int and as an ISO string typed into copies of a scoped source; (f) a pin record copy rewritten after the seal |
| F-D-EDGE | a kline file does not end exactly at its lens's last bar closing ≤ the pin, has a duplicate, an off-grid stamp or a row past the pin; a funding tape stops short of the pin's hour, repeats a print or holds a print past pin + jitter; the manifest mis-describes a file (sha, rows, flags, content sha); or a status 404 sits among the fetch phase's HTTP rows | a row past the pin appended to a temp copy; a tape truncated by one bar; a manifest row with a moved sha; a 404 row planted in a COPY of the log |
| F-D-DERIVE | 1d / 1w recomputed from native 4h by a plain loop sharing no code with `derive_1d` / `derive_1w` differ by one bit from the derived files (stamps and O, H, L, C exact; volume exact, the loop stating the COMPENSATED sum explicitly — pandas' groupby sum is Kahan-compensated, FX11:1973-1984), or the manifest's content shas of a derived file and of its derivation are not the loop's; a week does not open on a Monday | a 1d that keeps a five-bar day; weeks anchored on the epoch (Thursday); a naive left-to-right volume sum (differs in the last bit) |
| F-D-OUT | `--out` admits `research_outputs/tierc10/data` or `research_outputs/tierc11/data`, a symlink or `..` traversal to either, or the stage directory's parent; or a write of `write_manifest` does not sit behind `_out_guard()` | each bad `--out`; the guard call removed in a source copy |
| F-D-UNTOUCHED | after the build the TC11 snapshot does not re-hash, file for file, to TC11's manifest (in-scope and out-of-scope lists) or the TC10 snapshot to TC10's manifest (`M/research_outputs/tierc10/data/STAGE_D_MANIFEST.json`, by absolute main-tree path); or the live cache's `MANIFEST.json` stat (size, mtime, inode — stat only, never opened) moved across this fixture run | one byte flipped in a temp copy of an old-snapshot file must be found by the re-hash comparator |
| F-D-DET | two subprocess `--manifest` builds (hash seeds 1 and the contract seed) differ from each other or from the filed bytes in any determinism-set file, hold a different file set, exit non-zero, carry a clock-named key (the regex of FX11:166, ported), or differ in any parquet content sha; OR the call graph of `write_manifest` holds a `time.` / `datetime.` call (AST) | a hash-order-dependent emission; a `fee_schedule()` copy that stamps `datetime.now()`'s date (identical bytes on the same day — only the AST leg sees it) |

Legs of the same transcript defined in their own readings: F-D-SCOPE (L-D.4), F-D-FETCHPATH (L-D.5, L-D.6),
F-D-FORMING (L-D.7), F-D-VENUE (L-D.10), F-D-MANIFEST / F-D-SEAL (L-D.11), `F-D-PREFIX [i]` … `[iv]` (L-D.12),
`F-D-2 [1]` … `[4]` (L-D.13), F-D-3 (L-D.14), `F-TOLL [data a]` … `[data g]` (L-D.21), `F-TICK [a]` … `[d]`
(L-D.23). F-MIRROR is NOT a leg of this transcript: it is filed by the second invocation, after `--mirror`, so
`data/FIXTURES_DATA.txt` never changes when the mirror is made.
What the two source scans of this transcript do not reach: `F-D-PIN [e]` and `F-TICK [b]` scan the sources on file
at TC12-D. A pin or a tick typed into a LATER module as a number is held at that module's own gate by L-0.17's
F-TYPED (neither is a structural literal), and in the shim by F-VENDOR and F-REROOT's typed-`PIN_MS` mutant
(L-D.31); the string forms and the float-compare form are scanned here only.
SOURCE: L-0.9, L-0.11, L-0.14 (the hosting and scope laws); FX11:11-98 (TC11's roll); FX10 (F-D-2, F-D-3, F-D-VENUE,
its fee fixture, F-D-SEAL, F-D-L1).
RIVALS: none.
FAILS-IF: n/a (this reading is the roll).

**L-D.16 THE VENUE'S ZERO-VOLUME FLAT BARS** — "F-D-2 no synthetic bars" (contract :21); "the 5m is never a signal
source" (contract :89) and "a later 5m bar trades THROUGH the limit" (contract :93)
READING: a zero-volume flat bar (o == h == l == c and volume == 0) is a bar the VENUE published during an outage.
- **Substrate law (this section's):** such bars are KEPT, COUNTED per file (`venue_zero_volume_flat_bars`,
  `venue_zero_volume_bars`, `venue_flat_bars` — `scan_klines`, VERBATIM D11:1588-1618), attributed to the venue
  (F-D-2 leg 4), and never removed, filled or altered. No loader drops them: `E.D.load_asof`, `E.load_asof_at` and
  the lineage readers return them like any bar. The predicate of record is one function,
  `is_zero_volume_flat(o, h, l, c, v)`, in `scripts/tierc12_data.py`, the same expression F-D-2 recounts with.
  The manifest block `zero_volume_bars` prints the counts for all 17 stems × native lens, split by segment (tuning /
  holdout to TC11's pin / strip). Orientation from TC11's manifest [verified here]: 5m whole-tape — BTC 86, ETH 72,
  SOL 31, NEAR 34, ZEC 70; 1h — BTC 3, ETH 1; 4h, 12h, 1d, 1w — 0 for the five.
- **One invariant binds every consumer:** a zero-volume bar COUNTS AS ONE BAR in every bar count — a lookback of L
  bars, "8 consecutive closes", "K=3 closes", "12 five-minute bars", every traverse and time stop. No consumer skips
  such a bar to reach further back or to wait longer.
- **Handed to L-V (the profile), with the fact it must build on:** the profile source already gives such a bar ZERO
  weight in volume-at-price — `analytics/profile.py:139` (`if v[i] <= 0: continue`) — while its high and low still
  enter the window's range (`:126`), hence the bin grid. L-V states the time-at-price twin's treatment (the bar spent
  time at one price) and prints the count of zero-volume bars inside each lookback it uses.
- **Handed to the range simulators (L-S, L-R), and adopted by both:** a bar with volume == 0 is a NO-TRADE bar — no
  resting order and no target is filled on it (under TOUCH, TICK or DEEP, whatever its price); stops, invalidation
  and the time stop are evaluated on it as on any bar; the count of orders whose validity window contained such a
  bar is printed (L-S.15; the walk law of L-R.19 and L-S.18; L-R.24's conditioned maker entry, where a zero-volume
  child fills nothing). Reason: no trade printed on the venue, so no order can have been hit; the rule only removes
  fills, so it cannot flatter.
SOURCE: D11:1588-1618; FX10:529-531, :604-620; `analytics/profile.py:113-172` [verified here]; TC11's manifest
`MR/data/STAGE_D_MANIFEST.json`, row key `venue_zero_volume_flat_bars`; U4 hazard H12.
RIVALS: drop them at load — not taken: a silent filter changes every bar count and is the mirror image of a fill.
Treat a flat bar at a price through the limit as a fill — not taken: zero volume traded.
FAILS-IF: `F-D-2 [2]` — FAILS IF a file's recount of zero-volume flat bars is not the manifest's count (plant: a
carried-forward flat bar in a tape copy; L-D.13); F-ENV-ASOF — FAILS IF a cut frame loses a row of the tape (plant:
a cut-function copy that drops zero-volume bars; L-D.31). For the consumers, the legs L-V, L-S and L-R define.

---------------------------------------------------------------------------------------------------------------
### D · Fees — the "maker-bps" pin

**L-D.17 "IF ABSENT" — IT IS ABSENT; WHERE THE FILE LIVES** — "FEES: `data/fee_schedule.json` must carry
maker_bps_side per venue; if absent, add it" (contract :21-22)
READING:
- "`data/fee_schedule.json`" is the tier's own data directory: `M/research_outputs/tierc12/data/fee_schedule.json`
  (O-19), written by `--manifest`. TC11's file `MR/data/fee_schedule.json` (sha `6febe170…968b`) is never edited.
- The condition "if absent" FIRES. [verified here] no fee file on disk has a key `maker_bps_side`; TC11's file carries
  `maker_bps_per_side` 2.0 as a top-level scalar and on each of 17 ASSET rows, with no per-VENUE block, `maker_kind`
  "ASSUMPTION — …", `maker_source` = `README.md:150` + `scripts/v3_recompute.py:965`, and no URL and no date anywhere.
  The contract's key name exists only as a key of the in-memory reader `tierc11_env.fees()` (ENV11:1037). So the maker
  rate is ADDED from the venues' published schedules under L-D.18.
- The 2026-10-08 ruling (CON:2-3) makes the maker rate the toll of record for scalper mode; TC11's `maker_law` text
  ("an ADDED column, never the toll of record") is not carried. TC12's `maker_law` states only the DATA law: the rate
  per venue, its source and kind, zero maker slippage carried from TC11's rows, and that WHICH LEGS pay it is defined
  by the registration texts (CON:101; L-S).
SOURCE: O-19 (OR:132-138); `MR/data/fee_schedule.json` [verified here: 15 top-level keys, 26 row keys]; D11:1881-1973;
ENV11:1025-1044; U4 §1.11, §2.11-2.13; U6 §1.6, C1.
RIVALS: "present under the alias `maker_bps_per_side`" — not taken: it would leave the scalper's toll of record an
unsourced assumption, and O-19 orders the retrieval. Edit TC11's file — not taken: O-3, O-19.
FAILS-IF: `F-TOLL [data a]` … `[data g]` (L-D.21): the file's maker figure must be the extractor's or the README
regex's, never a typed one (plants there).

**L-D.18 THE PUBLISHED BASE RATE AND THE RETRIEVAL PROTOCOL** — "add it from the venue's published USDT-M perps
schedule, cite URL + date in the manifest" (contract :22-23)
READING:
- **"Published base rate"**, per venue = the MAKER fee, in percent of notional per fill, that the venue's own public
  fee schedule lists for USDT-margined perpetual futures at its ENTRY tier — the tier an account holds with no
  volume, balance or token-holding qualification — WITHOUT any token-payment discount, referral kickback,
  market-maker or liquidity-provider programme, zero-fee promotion or pair-specific special rate. The page's percent
  is parsed exactly (`fractions.Fraction` on the captured text) and converted by the one function `pct_to_bps`:
  `bps = percent × BPS_PER_UNIT / PCT_PER_UNIT`, the two unit objects of L-0's `scripts/tierc12_units.py` (D11:286 did
  the same conversion with a typed 100). Where the entry tier still lists more than one qualifying figure, the HIGHEST
  is taken (the reading that cannot flatter). A zero or negative figure is a rebate or a promotion and is never a base
  rate.
- **Which pages.** One public, unauthenticated page per venue, on the venue's own domain (`binance.com`,
  `bybit.com`):
  `BINANCE_USDTM` → `https://www.binance.com/en/fee/futureFee`;
  `BYBIT_V5_LINEAR` → `https://www.bybit.com/en/help-center/article/Trading-Fee-Structure`.
  UNVERIFIED: neither URL is on file anywhere in the estate (U4 §1.11 searched README, LEDGER, the charter, configs,
  the engine, D10, D11, both manifests, both fee files, the venue probe); both come from the scout's general knowledge
  and neither page's format has been read. The per-account fee endpoints are signed and the repo holds no key; they
  are not used.
  The two URLs are frozen with these readings; a correction is a dated amendment under L-0.5 (a build fact: the
  page moved or the URL is wrong), ruled BEFORE `--fetch` first runs. After the capture no URL is substituted.
- **Act 1 — CAPTURE** (`capture_fee_sources`, inside `--fetch`, a `CallLog` block, phase `fee_source`; network): one
  request per venue through `ED._get` (its transport retries included, each an `http` log row) with the library's
  default headers — no forged browser identity. The response body is saved byte for byte to
  `~/.cache/naiad/provenance/tc12_20261008/fee_source/<VENUE>.body` (outside the repo, and outside the snapshot whose
  file set is manifest-pinned). The write-once, sealed record `data/FEE_SOURCE.json` holds per venue: `url`,
  `final_url`, `http_status`, `error`, `body_path`, `body_sha256`, `body_bytes`, `retrieved_wall_clock_utc`,
  `retrieved_utc_date` (the date part of that stamp — the text before its `T`). It holds NO parsed figure. A failed
  capture is a filed status — never a HALT and never an "incomplete" exit.
- **Act 2 — EXTRACTION** (inside `--manifest`; no network, no clock): the grammar of record is applied to the saved
  body, whose sha is first re-verified against `FEE_SOURCE.json`. The grammar is DATA, the tracked record
  `data/FEE_GRAMMAR.json` — per venue: the pattern that locates the entry tier's label, the patterns that locate its
  USDT-margined maker and taker figures, the body sha it was written against, and the `AM-<n>` id that ruled it.
  UNVERIFIED: the page grammar itself. It is fixed by one amendment per venue, proposed as `AP-n` and ruled as
  `AM-<n>` (nickname `AM-D-FEE-<VENUE>`), source (v) of L-0.5's amendments law — TRANSCRIPTION against pinned
  bytes: the Stage D builder proposes it from the saved body bytes after the capture and before the first
  `--manifest`; it names the body sha; its heading is L-0.5's (`## AM-<n> · <date> (~HH:MMZ) · L-D.18 · ruling on
  AP-<m> · AM-D-FEE-<VENUE>`). The amendment may change patterns only; it cannot change the definition above, the
  URL, or the acceptance rule below. A fee page is not an outcome of any book: the amendment is transcription
  against pinned bytes, reviewable by re-running the extractor on them. For a venue whose capture returned HTTP
  200, `--manifest` HALTs while no grammar of record exists for it or while the grammar's body sha is not the
  captured body's. Where the saved body holds no qualifying figure (a page rendered by script, a challenge page),
  the amendment files a NULL grammar with the reason (`no_entry_tier_label` or `no_rate_in_body`) and the search it
  ran over the bytes; the fixture's second extractor must then also find no qualifying figure, or the stage is RED.
- **Acceptance.** `maker_kind = "PUBLISHED"` only if ALL hold: HTTP 200; `final_url`'s host is under the venue's own
  domain; the body contains the entry tier's label; the grammar yields at least one maker figure satisfying the
  definition and, after the highest-of rule, exactly one value; that value is > 0. Otherwise the venue is
  UNRETRIEVABLE with a reason from the closed set {`transport`, `http_<status>`, `off_domain_redirect`,
  `no_entry_tier_label`, `no_rate_in_body`, `ambiguous`}. F-TOLL's independent second extractor (`F-TOLL [data f]`,
  L-D.21) must agree with a PUBLISHED figure or the stage is not complete.
- **What is recorded if unretrievable** (O-19): the venue's `maker_bps_side` is the figure ON FILE —
  `read_maker_bps_side()` over `README.md` (D11:280-287; the sentence at `README.md:149-151`: "Binance USDT-M VIP0
  fees confirmed 2026-07-09 from the official fee page … maker is 0.02%") — with `maker_kind = "ON FILE — NOT
  RE-CONFIRMED"`, the attempted URL, the attempt's date, the HTTP status or error, and the reason. For
  `BYBIT_V5_LINEAR` the same on-file figure is applied and marked "ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is
  on file" (TC11's L-1.2 treatment of MNT, carried). MNT is not a home asset: its figure reaches Tier-E views only.
- **No figure ever enters by keyboard.** A maker rate reaches `fee_schedule.json` only (a) parsed by code from saved
  bytes whose sha is filed, or (b) read from README by the regex. If the executor can see a figure on a rendered page
  that the code cannot extract, that observation goes to `T12/DISCLOSURES_BUILD.md` as a dated `B-n` entry (the
  running record after the registry freeze, L-0.5 — `DISCLOSURES.md` is byte-frozen by then) and the pin stays (b);
  the operator's veto `"maker-bps"` (CON:137) is the only door for a hand-given figure.
- **Taker.** The same body's entry-tier TAKER figure is extracted under the same acceptance and filed as
  `taker_published_bps_side` — DISCLOSURE ONLY. No reader consumes it: the taker of record stays the estate's object
  (CON:23 "taker … unchanged").
SOURCE: O-19; D11:274-290; `M/README.md:149-151`; `M/Naiad_Phase0_Charter.md:112`; U4 R9, R10, §2.12.
RIVALS: (a) take 2.0 from README as "the published rate" — not taken: it is a 2026-07-09 transcription with no URL;
O-19 makes it the FALLBACK and flags it. (b) Bybit carries Binance's figure silently — not taken: flagged ASSUMPTION.
(c) the lowest listed figure, or a discounted one — not taken: flatters. (d) a hand-read figure typed into the file —
not taken: CON:8.
FAILS-IF: `F-TOLL [data d]`, `[data e]`, `[data f]` (L-D.21): the figure of record is not the extractor's on the
sealed bytes, a cited URL or date is not the sealed record's, or the independent second extractor disagrees (plants
there: a nudged venue figure; a date one day off; a grammar bent to capture the neighbouring figure).

**L-D.19 `fee_schedule.json` — THE SCHEMA** — "`data/fee_schedule.json` must carry maker_bps_side per venue … taker
and charter tiers unchanged" (contract :21-23)
READING: written by `fee_schedule()` inside `--manifest`; `json.dumps(indent=2, sort_keys=True)`; in the determinism
set. `fee_schedule()` holds NO numeric literal (the law of TC10's fee fixture, FX10:1357-1364).

Top level:
| key | value |
|---|---|
| `tier`, `stage`, `seed` | "TIER-C12", "TC12-D", the contract seed |
| `as_of_last_closed_4h`, `as_of_last_closed_4h_open`, `warranty` | from `AS_OF_PIN.json`; TC11's warranty sentence with the tier tag |
| `fee_law`, `haircut_twin_law`, `haircut_twin_clause`, `haircut_twin_tiers`, `charter_slippage_tiers`, `charter_slippage_source` | EQUAL to TC11's file, key for key (asserted) |
| `venues` | one block per distinct venue of the Stage D table (below) |
| `maker_pin` | {`name`: "maker-bps", `values`: {venue: bps}, `kinds`: {venue: kind}, `x_assumed_bps_side`: the `maker_bps_per_side` of the rows of `XR/tierc11x/data/tc11_rec/data/fee_schedule.json` (the file X's feasibility read; one value over its rows, asserted; the file's sha asserted against its `X_REC_MANIFEST.json` row and the manifest's against `tierc12_progress.certified`), `differs_from_x_assumption`: {venue: bool} = (`values[venue]` ≠ `x_assumed_bps_side`, the two filed floats compared exactly, no tolerance)} |
| `maker_law` | the data law of L-D.17 |
| `tc11_fee_schedule` | {`path`, `sha256` (read from TC11's PROGRESS), `keys_compared_top`, `keys_compared_row`, `all_equal`: true} |
| `keys_removed_vs_tc11` | {"maker_bps_per_side (top level)": "a scalar cannot carry two venues", "maker_source (top level)": "replaced by the per-venue block"} |
| `assets` | 17 rows (below) |

Each `venues[<VENUE>]` block:
| key | value |
|---|---|
| `stems` | the stems of record on this venue, panel order |
| `maker_bps_side` | THE PIN for this venue (float; L-D.18) |
| `maker_round_trip_bps` | twice the above, computed |
| `maker_slippage_bps_side` | TC11's row key of that name, uniform over the venue's rows (asserted), carried |
| `maker_kind` | "PUBLISHED" or "ON FILE — NOT RE-CONFIRMED" (Bybit fallback: "ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file") |
| `maker_basis` | the definition applied and the entry-tier label found, or the unretrievable reason |
| `maker_source_url` | the URL captured (or attempted) |
| `maker_retrieved_utc_date` | "YYYY-MM-DD" when PUBLISHED, else null |
| `maker_retrieval_attempted_utc_date` | "YYYY-MM-DD" of the capture attempt, always |
| `maker_source_record` | {`path`: "research_outputs/tierc12/data/FEE_SOURCE.json", `sha256`} |
| `maker_source_body_sha256` | the saved body's sha, or null |
| `maker_grammar` | {`record`: "research_outputs/tierc12/data/FEE_GRAMMAR.json", `sha256`, `amendment`: the `AM-<n>` id that ruled the grammar (L-D.18)} when a grammar was applied, else null |
| `maker_on_file_bps_side`, `maker_on_file_source` | the README figure and "README.md:<line> — <the sentence>" |
| `maker_equals_on_file` | bool |
| `taker_bps_side`, `taker_round_trip_bps` | the objects `tierc2_rules.FEE_BPS_SIDE`, `FEE_BPS_ROUND_TRIP` — the toll of record, NOT a venue schedule |
| `taker_kind` | TC11's row `kind` sentence |
| `taker_published_bps_side`, `taker_published_note` | the page's entry-tier taker or null; "DISCLOSURE ONLY — no reader consumes it" |

Each of the 17 `assets[]` rows keeps ALL 26 of TC11's row keys and adds ONE, `maker_bps_side`:
- EQUAL to TC11's row, asserted (19 keys): `asset`, `venue`, `symbol`, `stem`, `taker_bps_side_used`,
  `round_trip_bps_used`, `kind`, `source`, `haircut_twin_tier`, `haircut_twin_slippage_bps_side`,
  `haircut_twin_bps_side`, `haircut_twin_round_trip_bps`, `haircut_twin_kind`, `haircut_twin_source`,
  `charter_slippage_tier`, `charter_slippage_bps_per_side`, `charter_slippage_source`, `maker_slippage_bps_side`,
  `venue_note`.
- RE-MEASURED on the extended tape (3): `funding_interval_hours_observed_tail`, `…_modal`,
  `funding_spacing_hours_histogram`.
- FROM THE VENUE BLOCK (4 + 1): `maker_bps_side` == `maker_bps_per_side` (the TC11 key, kept as an alias so a
  TC11-style reader stays correct per stem) == `venues[row.venue].maker_bps_side`; `maker_round_trip_bps`;
  `maker_kind`; `maker_source` (the URL, the `FEE_SOURCE.json` pointer with sha, the README line).
SOURCE: O-19; D11:1895-1973; `MR/data/fee_schedule.json` [verified here]; FX10:1356-1408; U4 §1.11, R8.
RIVALS: keep the top-level scalar `maker_bps_per_side` — not taken: with two venues it is ambiguous and no code reads
it (`fees()` reads rows, ENV11:1031-1043). Rename the row key and drop the alias — not taken: a reader of the old key
would fail instead of reading the right number.
FAILS-IF: `F-TOLL [data a]`, `[data b]`, `[data c]`, `[data g]` (L-D.21: a numeric literal in the writer; a taker
figure off the estate's object; a carried key off TC11's file; a row off its venue block — one plant each there);
F-D-DET (L-D.15).

**L-D.20 THE RETRIEVAL DATE AND THE DETERMINISM SET** — "cite URL + date in the manifest" (contract :23)
READING: the contract wants a date in the manifest; a determinism-set file must not hold a clock. Both hold:
- The retrieval INSTANT (wall clock to the second, HTTP timing, the log rows) lives ONLY in the provenance set:
  `FEE_SOURCE.json` (write-once, sealed) and `FETCH_LOG.jsonl`.
- `--manifest` COPIES two strings out of that sealed record into the determinism set — `maker_source_url` and the
  calendar date `retrieved_utc_date` — into `STAGE_D_MANIFEST.json["fee_sources"][<VENUE>]` (with `record` {path,
  sha256}, `body_sha256`, `status`) and into the venue blocks of `fee_schedule.json`. They are recorded DATA read from
  a file whose bytes are sealed; `--manifest` makes no clock call. Re-running it any day reproduces the same bytes.
- Key names are chosen outside the ported clock-key pattern (FX11:166); the determinism proof is F-D-DET's two-seed
  identity PLUS its AST leg (no `time.` / `datetime.` call in `write_manifest`'s call graph) PLUS the equality leg
  below — a same-day `now()` stamp would pass a byte comparison, so the byte comparison alone is not the proof.
- The same law covers `CONTRACT_SPECS.json`'s capture stamp (D11:1140-1145, carried): the manifest pins that file's
  BYTES by sha and never carries its clock.
SOURCE: U4 hazard H10; D11:1124-1155, :2450-2466; FX11:140, :166; XD:158-159 (X's wider clock-key pattern, adopted:
`elapsed`, `wall_clock`, `perf_counter`, `_at_run`, `run_started`, load and worker counts).
RIVALS: cite only the record's path + sha in the manifest and keep the date out entirely — not taken: the contract
says "cite URL + date in the manifest". Stamp the date of the `--manifest` run — not taken: that is a clock.
FAILS-IF: `F-TOLL [data e]`: FAILS IF a date or URL in the manifest or the fee file differs from
`FEE_SOURCE.json`'s, or `FEE_SOURCE.json` moved since the seal. Mutation: a manifest copy whose date is one day off.

**L-D.21 "PRINT IT AS A PIN"; F-TOLL's DATA HALF** — "print it as a pin ["maker-bps"]" (contract :23); "F-TOLL (maker
bps read, never typed; taker twin == TC-series)" (contract :121)
READING:
- **The pin line**, one per run, in the Stage D log, in `STAGE_D_MANIFEST.json["pins"]["maker-bps"]`, in the
  manifest `.md`, and in the shim's lean block (every number read from `fee_schedule.json`):
  `PIN ["maker-bps"] <VENUE> <bps> bps/side (<round trip> round trip) · <kind> · <url> · retrieved <date or "—"> ·
  body sha <8 hex or "—">`, once per venue, then `X assumed <x> bps/side (<2x> round trip); differs: <venue: bool>`.
  The `differs` flags are what L-V prints beside the "1h maker PASS" word in `STAGE_V.md` (L-V.17) and what the
  scorer's beside leaf `licence_at_maker_pin` carries on P-SCALP-3 (L-X.14) — O-19: that word was earned at X's
  figure. Both read `maker_pin` from the file at the sha `tierc12_progress.certified` returns for it.
- **The pin in L-0's pin register** (`pins/PIN_REGISTER.json`, L-0.17): one row per venue of the Stage D table,
  named `fee.maker_bps_side.<VENUE>` — kind `stage_d`; source {path `research_outputs/tierc12/data/fee_schedule.json`,
  key `venues[<VENUE>].maker_bps_side`}; door `E.fees()`; veto `maker-bps` (CON:137 — the token names every such
  row, L-0.23). The row is filed at TC12-REG with its source and no value: the value exists from TC12-D, in the
  file. The venue names of the rows are the two of TC10's Stage D table (L-D.10), read there, not typed here.
- **F-TOLL, data half** — seven blocks `F-TOLL [data a]` … `F-TOLL [data g]` in `data/FIXTURES_DATA.txt`. Every
  BREAK half runs on copies, or on the fixture's own constructed page and grammar, so it runs whether or not any
  venue was retrieved; where no venue is PUBLISHED the REAL halves of (d) and (f) assert exactly that from
  `FEE_SOURCE.json` (status and reason) and print it. FAILS IF:
  (a) `fee_schedule()`, `extract_fee()`, `pct_to_bps()` or `capture_fee_sources()` holds ANY numeric literal (AST;
  the law of TC10's fee fixture, stricter here than L-0's structural allow-list: not even 0, 1 or 2);
  (b) any taker figure in the file ≠ the objects `tierc2_rules.FEE_BPS_SIDE` / `FEE_BPS_ROUND_TRIP`, or a row's
  `source` line does not hold the fee object;
  (c) any of the 6 top-level or 19 row keys listed EQUAL in L-D.19 differs from TC11's file (sha asserted against
  TC11's PROGRESS) — "taker and charter tiers unchanged";
  (d) a venue's `maker_bps_side` is neither the value the extractor of record returns on the saved body under
  `FEE_GRAMMAR.json` (when PUBLISHED) nor the README regex value (when ON FILE); the saved body's sha is not
  `FEE_SOURCE.json`'s; or a PUBLISHED venue lacks a URL, a date or a body sha. If `FEE_SOURCE.json` records a body
  (a non-null `body_sha256`) and the body file is absent, the block is NOT RUN (L-0.14 C) — never PASS, and RED
  at TC12-FIX, F-TOLL being a contract-named fixture;
  (e) the URL / date equality of L-D.20;
  (f) the fixture's own second extractor — written independently of the grammar of record (a structural parse of the
  body, not the grammar's patterns), run on the same bytes under the same definition — disagrees with a PUBLISHED
  figure;
  (g) a row's `maker_bps_side` ≠ its `maker_bps_per_side` ≠ its venue block's figure, or the venue blocks do not
  cover exactly the venues of the Stage D table.
  Planted mutations, one per block: a typed `2.0` in a copy of `fee_schedule()` → RED at (a); a row taker of 4.0 in
  a copy → (b); a charter tier moved in a copy → (c); a venue figure nudged in a copy → (d); a manifest copy whose
  retrieval date is one day off → (e); a grammar copy whose maker pattern is bent to capture the neighbouring
  (taker) figure, run through the production extractor on the same bytes → the figure of record moves and the
  second extractor disagrees → (f); a row whose maker differs from its venue block → (g).
- **F-TOLL, reader half** — the block `F-TOLL [reader]` in `env/FIXTURES_ENV.txt` (L-D.31): the value a stage
  CONSUMES — the key `maker_bps_side` of `E.fees()[stem]` — equals the value in the file TC12 pins by path + sha; a
  mutant shim that reads TC11's fee file must be RED. The BOOK half ("taker twin == TC-series") is L-S's:
  `F-TOLL [book t1]` … `[book t5]` (L-S.32). The contract's F-TOLL is PASS only if every block of all three
  qualifiers (`data`, `reader`, `book`) is (L-0.19).
SOURCE: CON:23, :121, :137; O-19; L-0.17, L-0.19, L-0.23; FX10:1356-1408; U6 hazard H8.
RIVALS: print the pin only in the close report — not taken: a pin is printed where it is set and where it is read.
FAILS-IF: as stated in the reading.

---------------------------------------------------------------------------------------------------------------
### E · The tick

**L-D.22 THE TICK OF RECORD AND THE GRID AUDIT** — "trades THROUGH the limit by ≥ 1 tick" (contract :93-94); rulings
O-20, O-27
READING:
- **The tick of record** per stem is the STRING `price_tick` of TC12's OWN capture `data/CONTRACT_SPECS.json`
  (`assets[].price_tick` = Binance `PRICE_FILTER.tickSize` / Bybit `priceFilter.tickSize`), captured ONCE at `--fetch`
  by `capture_contract_specs` (D11:1009-1114; write-once, sealed), applied over the WHOLE corridor (O-20). It is a
  point-in-time venue spec taken at the fetch run, hours after the pin; the record says so.
- **Capture diff, printed:** the manifest block `tick_of_record` holds, per stem, TC12's and TC11's `price_tick`,
  `qty_step`, `min_notional_usdt` and `status` (TC11's from `MR/data/CONTRACT_SPECS.json`, its sha asserted against
  the one TC11's PROGRESS certifies — orientation `74d9d47b…6b7e`), and `equal_as_decimal` (compared as `Decimal`,
  so "0.10" equals "0.1"). A moved tick is printed in the manifest and entered by the executor, at the TC12-D gate,
  in `T12/DISCLOSURES_BUILD.md` (a dated `B-n` entry; the manifest build itself writes nothing there); TC12's
  capture stays of record.
- **On-grid shares, printed** — `data/TICK_GRID_AUDIT.json` (determinism set) and a table in the manifest `.md`. For
  every stem × lens ∈ {5m, 1h} × segment × field ∈ {open, high, low, close}: `n`, `n_on_grid`, the share as the exact
  fraction "n_on_grid/n" and as a float rounded by the lineage's table law, and the last off-grid bar's open.
  Segments by the bar's CLOSE: tuning
  (≤ `ERA_CUT_MS`) · holdout to TC11's pin (`ERA_CUT_MS` < close ≤ `TC11_PIN`) · strip (`TC11_PIN` < close ≤ `PIN`).
  Computed EXACTLY: `TickGrid.on_grid` (L-D.23) on the unique values of each column, weighted by their counts.
- **Observed granularity per calendar month** (5m, the four price fields pooled): the coarsest decimal grid that
  contains every unique price of the month (the gcd of the prices in integer units of the finest decimal place
  present), printed per asset per month beside the recorded tick with the flag `coarser_than_recorded_tick`, and
  every flagged month LISTED. This is the measurement O-27 orders: "stricter than history" is claimed only where
  it is measured — the one-recorded-tick rule is stricter than or equal to history wherever the tape's observed
  granularity is ≤ the recorded tick. An era whose tick was FINER shows as off-grid shares; an era whose tick was
  COARSER than today's leaves every price on today's grid and shows only in this column.
- What is on file already [scout, U4 §1.12 and U6 §1.9, on the TC11 snapshot]: BTC 5m lows are off the recorded 0.10
  grid through 2022-02-15, NEAR through 2022-01-20, SOL through 2024-10-16 — inside the holdout era, 25,148 of 235,008
  SOL 5m lows off the recorded 0.01 grid; ETH and ZEC have no off-grid bar. In every measured case the recorded tick
  is coarser than or equal to the tick then in force. UNVERIFIED (O-27): "never looser" — that no month had a tick
  COARSER than the recorded one. It is carried UNVERIFIED until the monthly-granularity column prints at build; any
  flagged month is listed in the manifest, entered in `T12/DISCLOSURES_BUILD.md`, and printed beside L-S's fill
  tables (L-S.15).
- Readers: `E.ticks() → {stem: price_tick string}` (L-D.26 hunk 10). No tick is typed anywhere.
SOURCE: O-20 (OR:140-142), O-27 (OR:188-191); D11:1040, :1060; `MR/data/CONTRACT_SPECS.json` [verified here: 17
ticks, all strings]; `M/scripts/tierc11_books_fixtures.py:340-346` (the only existing reader, a fixture helper
returning a float).
RIVALS: TC11's capture — not taken: O-20. A per-era tick inferred from the tape — not taken: an inference rule nobody
ratified; the audit PRINTS what such a rule would have seen instead. "Never looser" asserted without the monthly
column — not taken: O-27.
FAILS-IF: `F-TICK [c]` (the tick the audit and the manifest used is not the sealed capture's string; plant: a
`price_tick` altered in a COPY of the specs) and `F-TICK [d]` (the on-grid shares differ from the fixture's own
`Fraction` recount; plant: a seeded cell's `n_on_grid` altered in a COPY of the audit) — L-D.23. The reader identity
`E.ticks()` == the capture's strings is F-REROOT's (L-D.31): no shim exists when the Stage D suite runs.

**L-D.23 `TickGrid` — EXACT INTEGER-TICK ARITHMETIC** — "by ≥ 1 tick (low < limit − tick for a long)" (contract :94);
ruling O-20 "Tick arithmetic is exact (integer ticks), never float compare"
READING: `scripts/tierc12_tick.py`, a PURE module (stdlib `decimal` only; no numpy, no I/O, no engine import). One
class, constructed from the venue's tick STRING: `TickGrid(tick: str)`; HALT unless the tick is finite and > 0.
Its interface, complete: attributes `T` (a `Decimal`, `Decimal(tick)`) and `ctx` (the grid's trapping
`decimal.Context`, below); `dec(x)`; methods `floor_ticks(x)`, `ceil_ticks(x)`, `on_grid(x)`, `px(n)`; and the four
comparisons against a grid level, `lt(x, n)`, `le(x, n)`, `gt(x, n)`, `ge(x, n)`.
- **What an `x` may be.** Every `x` is a `float` (converted by `dec`: `Decimal(repr(float(x)))` — the shortest
  decimal that round-trips the float64, which for every tape price is the venue's own printed decimal) or a
  `decimal.Decimal` (used exactly as given; no float round-trip). It must be finite and > 0. Any other type HALTs
  (an `int`, a `str`, a `numpy.float32`; a `numpy.float64` IS a `float`). `dec(x)` returns that `Decimal`.
- `q, r = divmod(dec(x), T)` — exact: `q` an integer, `0 ≤ r < T`. `floor_ticks(x) = q`; `ceil_ticks(x) = q + (1 if
  r ≠ 0 else 0)`; `on_grid(x) = (r == 0)`.
- `px(n) = float(n × T)` with the round trip asserted (`dec(px(n)) == n × T`).
- **The four comparisons against a grid level `n × T`, each an INTEGER comparison, exact for off-grid `x` too:**
  `lt`: `x <  n·T ⟺ floor_ticks(x) ≤ n − 1` · `le`: `x ≤ n·T ⟺ ceil_ticks(x) ≤ n` · `gt`: `x > n·T ⟺
  ceil_ticks(x) ≥ n + 1` · `ge`: `x ≥ n·T ⟺ floor_ticks(x) ≥ n`.
- **The trapping context.** All arithmetic stays inside ONE local `decimal.Context`, `ctx`, which TRAPS `Inexact`
  and `Rounded` (and `FloatOperation`, so a `Decimal` is never silently mixed with a float): an operation that
  cannot be exact HALTs instead of rounding. Its precision and exponent limits are not typed numbers: they are the
  stdlib objects `decimal.MAX_PREC`, `decimal.MAX_EMAX` and `decimal.MIN_EMIN`, so that a `Decimal` argument of any
  length is divided exactly — under the default 28-digit context the same `divmod` signals `Inexact` on an
  argument longer than the precision [verified here on a 37-digit argument], which would HALT exactly the inputs
  this class must accept. The class performs only `+`, `−`, `×`, `divmod` and comparisons. A decimal signal
  surfaces as a HALT (`SystemExit`), never as a rounded value.
- **A consumer's own exact expression** — the scalper's T2 and DEEP depth (L-S.11, L-S.15), the conditioned maker
  entry `grid.dec(low) < grid.dec(P) − n_tick·grid.T` (L-R.24) — is formed under `decimal.localcontext(grid.ctx)`
  and under no other context, and its `Decimal` result is handed to `floor_ticks` / `ceil_ticks` / a comparison as
  is. Under `ctx` a quotient is admissible only where it is exact (a contract fraction such as the pin door's
  `Fraction` enters as `Decimal(numerator) / Decimal(denominator)`, exact for every terminating decimal); a
  quotient that is not exact raises at this precision and is a HALT, never a rounding.
- No float subtraction, no float comparison, no tolerance.
- The module defines NO fill rule, no snapping direction and no order model: L-S and L-R state those in terms of
  `floor_ticks` / `ceil_ticks`, the four comparisons and `ctx`.
SOURCE: O-20; Python's `decimal` documentation (the exact-arithmetic recipe: `prec=MAX_PREC`, `Emax=MAX_EMAX`,
`Emin=MIN_EMIN` with `Inexact` trapped); U6 R-2, hazard H5 (`limit − tick` in binary float mis-decides
exact-boundary lows, and on-grid lows are the common case).
RIVALS: `low < limit − tick` in float — not taken: O-20. Round-to-nearest-tick then compare — not taken: it moves
off-grid historical prices onto the grid before judging them. Float inputs only, a `Decimal` passed through `float`
— not taken: L-S forms T2 and the DEEP depth exactly, and a float round-trip of an exact product can land on the
neighbouring tick. The default context with the two traps — not taken: it HALTs on the long exact products.
FAILS-IF: F-TICK, four blocks in `data/FIXTURES_DATA.txt`. FAILS IF:
[a] `floor_ticks`, `ceil_ticks`, `on_grid` or any of the four comparisons disagrees with a brute-force `Fraction`
evaluation on the fixture's own enumerated grid of cases — every stem's tick × levels on-grid, one finer decimal
place above and below, and exact boundaries — each case handed in as a `float` AND as a `decimal.Decimal`, plus
`Decimal` inputs carrying more significant digits than a float64 round-trips; or an `x` of another type, a
non-finite or a non-positive `x` is accepted;
[b] a non-fixture `scripts/tierc12_*.py` in this suite's scope (the common law's SCOPE: the sources recorded up to
TC12-D) holds a tick as a literal (AST: a numeric or string literal equal as `Decimal` to any captured tick in an
assignment or comparison naming `tick`) or compares a price to `x − tick` / `x + tick` in float (AST: a `BinOp` with
a name containing `tick` under a `Compare`);
[c] the tick per stem that `TICK_GRID_AUDIT.json` and the manifest's `tick_of_record` used is not, as a string, the
sealed capture's `assets[].price_tick`; a panel stem lacks one; or the capture moved since the seal;
[d] the on-grid shares recomputed by the fixture's own `Fraction` code for three (stem, lens, segment, field)
cells — three is this leg's fixture-typed count, drawn without replacement from the key-sorted cells on the stream
`default_rng([SEED, crc32("data|F-TICK [d]")])` — differ from `TICK_GRID_AUDIT.json`.
Planted mutations: a `TickGrid` copy whose `lt` is `x < n*float(T)` in float → RED at [a] on a boundary case; a
copy whose `dec` passes a `Decimal` through `float` → RED at [a] on a long-`Decimal` case; a typed `0.01` assigned
to `tick` in a copy of a scoped source → RED at [b]; a `price_tick` altered in a COPY of the specs → RED at [c]; the
`n_on_grid` of one of the three seeded cells altered by one in a COPY of the audit → RED at [d].
How a CONSUMER's tick use is held, since [b] cannot reach a module filed later: a typed numeric tick by L-0.17's
F-TYPED at that module's gate; the read by the consumer's flow leg on `E.ticks()` (L-S.2); the arithmetic by the
consumer's own enumerated boundary cases (L-S.15's F-SCALP TICK-FILL leg).

---------------------------------------------------------------------------------------------------------------
### F · The LaCie mirror

**L-D.24 THE LaCie MIRROR** — "LaCie mirror per ATHENA's residency rules" (contract :20-21)
READING:
- **The rules of record** (Data residency v2, operator ruling 2026-08-15, `M/exchange/status/CONVENTIONS.md:204-228`):
  `/Volumes/LaCie` is "backup only … Reads never touch it in normal work" (:211); "`drive_wait` gates backup WRITES,
  not substrate reads" (:226); archives are "BORN LOCAL … and mirrored to the LaCie in the same act" (:222). No rule
  names a cache snapshot, and neither earlier snapshot was ever mirrored (TC11's manifest `mirror`: "NOT done").
- **Form:** a plain directory mirror — a byte copy of every file of the TC12 snapshot (the manifest's in-scope and
  out-of-scope paths) plus the fee-source bodies — not an estate zip. `backup_estate.py --estate` is not used: it
  would file a snapshot under the live cache's archive name beside the real weekly generations, and that script
  publishes the bus.
- **Destination (default; see OPEN TO OPERATOR):** `/Volumes/LaCie/Naiad/snapshots/tc12_20261008/` and, beside it,
  `/Volumes/LaCie/Naiad/provenance/tc12_20261008/`. A NEW directory under the LaCie's existing bulk-mirror root; the
  `naiad-backups` vault is not touched.
- **The record.** `--mirror` files under its own progress record `TC12-D.mirror` — a dotted child of TC12-D (O-31)
  that the filed merger sorts under its parent (`M/scripts/tierc12_progress.py:29-32`), `depends_on: ["TC12-D"]`,
  and THE ONLY NON-BLOCKING child of the tier (L-0.10's `SUBSTAGES_T`): it is in no position of the resume order,
  may be gated at any time after TC12-D, never moves the resume point, may stay PARTIAL through CLOSE, and is then
  harvested as a finding. Its artifacts: `data/MIRROR_ATTEST.json` and, when a WOKE row exists,
  `data/DRIVE_WAKE_LOG_TC12.md`. Its fixture record is F-MIRROR, run by `scripts/tierc12_data_fixtures.py
  --stage=TC12-D.mirror`, with its own transcript `data/FIXTURES_MIRROR.txt` — the tier's one PROVENANCE transcript
  (L-0.14 D): recorded by sha with `provenance: true`, excluded from the sweep's byte-identity roll and listed there
  by name, because it depends on a mounted drive.
- **Procedure** (`--mirror`: a plain process, never under the shim; it requires TC12-D COMPLETE-VERIFIED):
  1. `drive_wait.WAKE_LOG` is REBOUND to `research_outputs/tierc12/data/DRIVE_WAKE_LOG_TC12.md` before the call (the
     module attribute exists for that, `M/scripts/drive_wait.py:114-115`): its default is under `exchange/status/`,
     where nothing is written before CLOSE (O-1).
  2. `r = wait_for_drive("/Volumes/LaCie")` — the MOUNT POINT, never a path inside it (`drive_wait.py:82-85`), with
     the module's own attempts and delay. PRESENT or WOKE → continue (a WOKE row lands in the rebound log).
     UNREACHABLE → step 7.
  3. Destination check: it must not exist, or must be an earlier TC12 mirror named by a filed `MIRROR_ATTEST.json`
     (then only missing or mismatching files are re-copied). Anything else HALTs. Nothing on the LaCie is ever
     deleted or overwritten outside that directory.
  4. Copy every file in sorted relative-path order to `<dest>/<rel>.part`, `fsync`, `os.replace` to `<dest>/<rel>`
     (exFAT: no clonefile, case-insensitive — the copy first asserts no two relative paths collide under casefold).
  5. VERIFY BY RE-READING FROM THE DESTINATION: the sha256 of every destination file equals `STAGE_D_MANIFEST.json`'s
     sha for it (`files[].sha256` + `out_of_scope_snapshot_files[].sha256`; the bodies against `FEE_SOURCE.json`), and
     the destination's file set equals the manifest's. A listing is not a verification. Stated limit: a read served
     from the OS cache cannot be told from a read off the platter; F-MIRROR re-hashes again on any later run.
  6. A copy of `STAGE_D_MANIFEST.json` and a `SHA256SUMS` text are placed in the destination so the mirror describes
     itself; `data/MIRROR_ATTEST.json` is filed (provenance; write-once per completed mirror): destination, volume
     filesystem, `drive_wait` state and attempts, files, bytes, per-file equality, the manifest sha.
  7. **If the drive is asleep, unmounted or absent** (UNREACHABLE after the full budget): the mirror step exits
     "MIRROR NOT RUN — /Volumes/LaCie UNREACHABLE after <elapsed> s"; nothing is written to the drive;
     `progress/TC12-D.mirror.json` is PARTIAL with that blocker; F-MIRROR's block is written by `not_run` (NOT RUN,
     never PASS) in `data/FIXTURES_MIRROR.txt`. NO other stage waits on it (O-32): the substrate is local and every
     read is local. `--mirror` is re-runnable at any time (the record and its provenance transcript are then
     re-filed); CLOSE prints its status, and a mirror still not done at CLOSE is a finding-not-fixed and an operator
     item — never a silent fallback to another destination.
- **Scope:** the TC12 snapshot and its fee-source bodies only. The TC10 and TC11 snapshots stay unmirrored and are
  listed as such (see OPEN TO OPERATOR). The mirror COPIES; no snapshot is moved (the shim's import windows need the
  TC10 snapshot's directory to exist, L-D.25).
- Pointer discipline: no data-class file enters `exchange/`; the bus gets a path + sha pointer at CLOSE at most.
SOURCE: `CONVENTIONS.md` sha `42b2cdd6…a226e`, :204-228, :831-837; `M/scripts/drive_wait.py` :20-25, :82-85,
:105-115, :203-250 [verified here: WOKE appends to `WAKE_LOG`; the file `exchange/status/DRIVE_WAKE_LOG.md` does not
exist today]; `M/research_outputs/tierc10/OPERATOR_RULINGS.md:36, :64-66`; U4 §1.13, §2.10, R12, R13;
`/Volumes/LaCie` mounted, exFAT, 1.2 TiB free [verified here].
RIVALS: (a) an estate-style zip in the vault — not taken (above). (b) defer the mirror to the operator at CLOSE as
TC10 and TC11 did — not taken as the default: the ratified contract orders the mirror inside Stage D, and a plain
copy pushes nothing and publishes nothing (it is not among the acts O-12 reserves); it remains the operator's to
veto or relocate. (c) call `wait_for_drive` with its default log — not taken: it writes under `exchange/` on WOKE.
FAILS-IF: F-MIRROR (one block; `--stage=TC12-D.mirror`; `data/FIXTURES_MIRROR.txt`, PROVENANCE) — FAILS IF any
mirrored file re-read from the LaCie differs from the manifest's sha, the file sets differ, or `MIRROR_ATTEST.json`
mis-states either; NOT RUN (never PASS) when the drive is unreachable. It is not a contract-named fixture and is in
no transcript of record: its NOT RUN leaves `TC12-D.mirror` PARTIAL and is a finding at CLOSE, not a RED of the
sweep. Mutation: one byte flipped in a TEMP copy of the mirror tree → RED at "sha != manifest"; one file removed
from the temp copy → RED at "file set".

---------------------------------------------------------------------------------------------------------------
### G · The environment shim

**L-D.25 `scripts/tierc12_env.py` — VENDORED FROM TC11's SHIM BY DECLARED HUNKS; F-VENDOR** — "one corridor" (contract
:5); rulings O-3, O-4, O-5
READING: every TC12 stage after Stage D runs under ONE shim, `scripts/tierc12_env.py`, which is TC11's
`scripts/tierc11_env.py` at the sha TC11's PROGRESS certifies (stage TC11-ENV, `1526093b…f798`, 1,381 lines), changed
ONLY by the declared hunks of L-D.26 and nothing else.
- **The referee** is a committed byte copy, `M/research_outputs/tierc12/vendor/tierc11_env@1526093b.py`, with
  `vendor/README.md`, filed as the first act of TC12-ENV under the record `TC12-ENV.vendor` (O-31), after TC12-D is
  COMPLETE-VERIFIED and before any hunk is applied; it has its own commit `tierc12(TC12-ENV.vendor): …`, which
  precedes the TC12-ENV gate; its fixture record is F-VENDOR `[referee]` (the three-sha equality, the tag, the hunks
  apply and revert on the referee text), run by `tierc12_env_fixtures.py --stage=TC12-ENV.vendor` without importing
  the shim → `env/FIXTURES_ENV_VENDOR.txt`. The same record files `scripts/tierc12_vendor.py` (the hunk table,
  below) and `env/LINEAGE_PINS.json` (L-D.29); it is a blocking child, `depends_on: ["TC12-D"]`. Three shas must be
  equal: the copy's; the one `MR/PROGRESS.json` certifies for `scripts/tierc11_env.py` under stage TC11-ENV (read by
  key from `artifact_shas`); and the live `M/scripts/tierc11_env.py`'s (a difference there is a moved TC11 byte — a
  finding against O-3). The eight-hex tag in the file name is a label asserted to prefix that sha. The referee is
  never imported.
- **The hunks are DATA**, in `scripts/tierc12_vendor.py` (a plain module; it never imports the shim): a table
  `ENV_HUNKS` of `(hunk number, what, old, new)` entries and `HUNK_NAMES` for hunks 1-10. `build_env_text(referee)`
  applies them in order; each `old` must occur EXACTLY ONCE in the referee and in the text it is applied to; every
  declared hunk number is used and no other; the built text must REVERT to the referee. `scripts/tierc12_env.py` is
  that built text, written once and byte-verified; it is never hand-edited.
- **F-VENDOR** (in `scripts/tierc12_env_fixtures.py`), two blocks at two records:
  - `F-VENDOR [referee]` — at `TC12-ENV.vendor`, no shim import, no shim file needed. FAILS IF: the three shas are
    not equal; the tag does not prefix the sha; `build_env_text(referee)` breaks one of its own laws (an `old` that
    does not occur exactly once, a hunk number outside 1-10, a declared number unused); or the text it builds, with
    the hunks reverted in reverse order, is not the referee byte for byte. Planted mutations: a one-byte edit of a
    COPY of the referee → "sha != certified"; a hunk-table copy whose `old` occurs twice in the referee → RED; an
    eleventh hunk number in a hunk-table copy → RED.
  - `F-VENDOR` — at `TC12-ENV`, on the built shim. FAILS IF: the referee does not hash to the certified sha; the
    built shim with the hunks reverted in reverse order (each `new` exactly once at its step) is not the referee
    BYTE FOR BYTE; a hunk number outside 1-10 is present or a declared one is unused; a hunk-9 (text-only) entry
    changes a character outside a string-literal token (tokenize: STRING / FSTRING_MIDDLE) or changes the module's
    AST with every string constant blanked; the referee is untracked or differs from its blob at HEAD (a
    fixture-side read-only git call; the vendor commit precedes this gate, so the blob exists when the leg first
    runs); or the module imported as `tierc12_env` is not that built file. Planted mutations (X's seven,
    XF:371-411): a one-byte undeclared edit in a copy of the shim; an undeclared edit INSIDE a declared hunk's
    span; a CODE edit declared text-only; a COMMENT edit declared text-only; a `str` literal turned `bytes`
    declared text-only (tokenize-clean — the AST leg must see it); an eleventh hunk number; a one-byte edit of a
    copy of the referee.
- **What the referee keeps doing, unchanged** (no hunk touches it): the import order — `tierc2_baseline` FIRST under
  the bound snapshot, then each lineage module inside an env WINDOW that points `NAIAD_CACHE_DIR` at the TC10 snapshot
  for the duration of that one import statement (TC10's `assert_substrate` demands the directory exist, D10:94-117;
  no data under it is opened — a window that touches it HALTs, ENV11:630-650); the closed re-root list `REROOT_PLAN`
  (25 rows; every PATH target derives from `OUT` or `SNAPSHOT` and every seed target from `SEED`, so hunks 1-2 move
  the targets without editing a row; only the rows' provenance strings change, under hunk 9); the canonical
  path judging (realpath, device + inode, NFC + casefold, firmlink and `/.nofollow` aliases); the audit hook armed
  LAST; exit code 70 on any BLOCKED attempt, forced by the referee's exit report (ENV11:1129-1151); `TC10_ALLOW` and
  `tc10_record` (the referee's eight records, unchanged — a closed list, each read logged ALLOW; no ninth without a
  dated amendment); `SEED_SENS`, `N_BOOT`, `ERA_CUT_MS`, `LENS_MS`, `era_of` (tuning iff the close ≤ `ERA_CUT_MS`,
  else holdout; ENV11:1047-1055), `CLASSIC5`, `UNSEEN12`, `PANEL17` (ENV11:868-870), `static_imports`,
  `hook_escapes`, `opened_paths`, `import_audit`.
- **The hook's stated limit stands** (ENV11:74-84): it sees Python-level opens only — not pyarrow's native readers
  and writers, not `to_parquet(partition_cols=…)`, not subprocesses or ctypes. `hook_escapes` is the AST ban; TC12
  code reads and writes parquet through pandas on a path STRING only.
SOURCE: X's LX-0.4 (`XR/tierc11x/LEANS_X.md:251-342`); XD:608-633 (hunks as data), :1421-1551 (`build_env_text`,
`revert_env_text`, `text_only_findings`, `vendor_findings`); XF:365-439 (F-VENDOR); `XR/tierc11x/vendor/README.md`;
ENV11 [verified here, sha `1526093b…`]; U3 §1.14, R1.
RIVALS: (a) import `tierc11_env` — not taken: its guard HALTs off the TC11 snapshot (ENV11:206-208), its pin is typed
(:122), its `OUT` is TC11's, and no `tierc11_*` module is ever imported or run (O-3). (b) X's vendored shim as the
referee — not taken: X is unmerged (O-4) and its referee `086d66da…` predates TC11's AM-1 wording. (c) the live
`scripts/tierc11_env.py` as the referee — not taken: X's law is a COMMITTED referee, which survives any later TC11
edit and exists in a detached review worktree; the live file is held equal to it instead. (d) a fresh shim — not
taken: it would discard a reviewed hook and re-open TC11's 51 review findings.
FAILS-IF: F-VENDOR, as stated.

**L-D.26 THE TEN HUNKS** — ruling O-7 "every later read is by object"; O-19 "TC12's env reads TC12's file"
READING: the complete list. "code" = changes the AST; "text" = string literals only (F-VENDOR's hunk-9 law applies to
hunk 9; every other hunk is reviewed as code). No identifier of the referee is reused with a new meaning.

| # | name | what changes | class |
|---:|---|---|---|
| 1 | IDENTITY | the docstring header names TIER-C12, the contract of record by path (no sha is typed into the shim: the contract's pin is L-0.1's prefix pin, read from `progress/STEP_Q.json` where it is needed) and these readings; the run / import lines; the literal line `SEED = …` (ENV11:125) is replaced by a READ of the contract seed from L-0's filed pin record `OUT/pins/CONTRACT_PINS.json` (a literal inside a declared hunk is scanned like any other, so none is typed; F-REROOT asserts the value equals the pin door's). `SEED_SENS`, `N_BOOT` unchanged (the referee's lines) | code + text |
| 2 | ROOTS AND GUARD | `SNAPSHOT` → `…/snapshots/tc12_20261008`; `OUT` → `ROOT/research_outputs/tierc12`; NEW names `TC11_SNAPSHOT_OLD`, `TC11_OUT = MAIN_TREE/research_outputs/tierc11`, `X_REC = MAIN_TREE / "research_outputs" / "tierc12" / "x_rec"` (`x_rec/**` is git-ignored and exists only in the main tree, so a detached review worktree reads it there — as TC11's records are read), `X_WORKTREE = MAIN_TREE/.claude/worktrees/tierc11x`, `NAIAD_CACHE_ROOT = HOME/.cache/naiad`; the identifiers that held the BOUND snapshot (`_R_TC11_SNAP`, `_C_TC11_SNAP`) are renamed `_R_SNAP`, `_C_SNAP` at every occurrence (after the build neither old name occurs in the file). `guard_substrate`: HALT also on a value that is not absolute AS GIVEN (D11:102-105 — the referee expands `~` at :200 while `engine.data` does not) and on the TC11 snapshot; a new first clause HALTs unless `sys.dont_write_bytecode` is true (O-5) | code |
| 3 | PINS BY OBJECT | the literal lines `PIN_MS = …` / `PIN_ISO = …` (ENV11:122-123) are replaced by a read of `OUT/data/AS_OF_PIN.json` (`as_of_last_closed_4h_close_ms`, `as_of_last_closed_4h`); HALT "run scripts/tierc12_data.py --pin first" if absent. NEW `TC11_PIN_MS`, `TC11_PIN_ISO` read from `TC11_OUT/data/AS_OF_PIN.json` (sha asserted against TC11's PROGRESS). `TC10_PIN_MS` stays the referee's line and gains an assertion against that record's `tc10_pin_close_ms` | code |
| 4 | RE-ROOTS, `fees()`, POST-SHIM | `fees()` reads `OUT/data/fee_schedule.json` (TC12's, by hunk 2) and takes `maker_bps_side` from the row key of that name, asserting it equals the row's `maker_bps_per_side` and `venues[row.venue].maker_bps_side`; per stem it returns exactly `{asset, venue, taker_bps_side, taker_round_trip_bps, maker_bps_side, maker_round_trip_bps, maker_kind, maker_slippage_bps_side, slippage_bps_side, slippage_tier, maker_source_url}` — the referee's ten keys (ENV11:1033-1043) plus `maker_source_url`. The hunk imports L-0's stdlib-only process tool `tierc12_progress` for `certified` (the sha-first helper P3 and P6 call). The post-shim gains the clauses P1-P9 below. The `_U12` re-root's source sentence and `IMPORT_AUDIT`'s env label name the bound snapshot | code + text |
| 5 | PROTECTION (writes) | L-D.27's write-never classes | code |
| 6 | READ JUDGES | L-D.27's read-never classes; `TC11_ALLOW_FILE` (hunk-6 DATA, the list of L-D.27 — a FILE list only: no listing of a TC11 directory is allowed); the `x_rec` manifest judge, on `X_REC`; the snapshot in-scope judge; the verified-read refusal (L-D.27: an open of a `tc11-allow` or `x-rec` path that its read function has not verified in this process is BLOCKED); a record of every READ open by class, for `read_set()`. `classify` gains the classes `tc11-snapshot` (the OLD one), `tc12-snapshot` (the bound one; the referee's string "tc11-snapshot" for the bound snapshot is retired), `tc12-snapshot-out-of-scope`, `tc11-allow`, `tc11-unlisted`, `x-rec`, `x-rec-unlisted`, `x-worktree`, `x-merged`, and `tc12-record` (a path under `research_outputs/tierc12/`, outside `x_rec/` and outside any `_det_*` segment — judged for the read set only, never refused) | code |
| 7 | FORBIDDEN NAMES, THE RANGE DOOR AND THE VA-WALL EXIT CHECK | `FORBIDDEN_MODULE_SUBSTRINGS` gains `"value_area"` (CON:25-26: decision modules import nothing from it; the shim itself is value-area-free, and the post-shim's forbidden-name clause — ENV11:1015-1017, P7 below — HALTs a process that loaded the module BEFORE the shim); `NEST_MODULE` = the empty string: no caller's name can equal it, so `tc10_import` of a range module HALTs for EVERY caller — the door is CLOSED, with no exception (L-0.30 PIVOT-RANGE: no TC12 module — no door either — imports the range machine; CON:132 "no pivot-range trades"). The hunk also registers the VA-wall exit check of L-0.22 (i-b): typed tuples `VA_WALL_DOORS`, `VA_WALL_FIXTURES`; `BLOCKED:va-wall`; exit 70 — specified below the table | code |
| 8 | ESTATE-MODULE EXEMPTION AND THE BINDING SCAN | `_estate_modules` exempts names starting `tierc12_` (in place of `tierc11_`): they hold the guard constants that name the old snapshots in order to refuse them. `tc10_bindings` also flags any module global naming `tc11_20260925` or `research_outputs/tierc11` (kinds `tc11-snapshot`, `tierc11-out`); an undeclared one HALTs | code |
| 9 | TEXT-ONLY | the TC11 → TC12 wording of audit, lean-block and HALT message STRINGS (the lean block's hand-off paragraph now says the range door is closed for every caller); nothing outside string literals (comments stay the referee's; the header says "where the text names TC11 as the shim's own user, read TC12") | text |
| 10 | API | NEW functions `ticks()`, `load_asof_at(stem, iv, cut_ms)`, `load_funding_asof_at(stem, cut_ms)`, `tc11_record(rel)`, `x_rec(rel)`, `lineage_shas()`, `verified_reads()`, `read_set()`; `__all__` gains them and `PIN_ISO`, `TC10_PIN_MS`, `TC11_PIN_MS`, `TC11_PIN_ISO`, `TC11_OUT`, `X_REC`, `X_WORKTREE`, `TC11_ALLOW_FILE`, `VA_WALL_DOORS`, `VA_WALL_FIXTURES`. No name for listing TC11 directories exists (no stage lists one) | code |

**The API every section uses (the names are exact; an attribute not on this list is not promised).**
- MODULE ALIASES — the referee's, which no hunk renames (ENV11:719-752): `E.TB` tierc2_baseline · `E.D` tierc10_data
  · `E.TP` tierc10_panel · `E.BK` tierc10_brk · `E.LN` tierc10_lanes · `E.T9` tierc9 · `E.T8` tierc8 · `E.T7` tierc7 ·
  `E.R7` tierc7_rules · `E.LAB` tierc7_lab_regime · `E.T6` tierc6 · `E.R6` tierc6_rules · `E.T5` tierc5 · `E.R5`
  tierc5_rules · `E.R4` tierc4_rules · `E.R3` tierc3_rules · `E.R2` tierc2_rules. `E.LR` and `E.RC` do not exist.
- OBJECTS: `E.PIN_MS`, `E.PIN_ISO`, `E.TC11_PIN_MS`, `E.TC11_PIN_ISO`, `E.TC10_PIN_MS`, `E.ERA_CUT_MS`, `E.SEED`,
  `E.SEED_SENS`, `E.N_BOOT`, `E.LENS_MS`, `E.CLASSIC5`, `E.UNSEEN12`, `E.PANEL17`, `E.OUT`, `E.SNAPSHOT`,
  `E.MAIN_TREE`, `E.TC11_OUT`, `E.X_REC`, `E.X_WORKTREE`, `E.TC11_ALLOW_FILE`.
- FUNCTIONS: `E.era_of(close_ms)`; `E.fees()` (hunk 4's eleven keys per stem); `E.ticks() -> {stem: price_tick
  string}` (from `OUT/data/CONTRACT_SPECS.json`); `E.D.load_asof(stem, iv)` (the lineage's reader: bars closing ≤
  the pin — there is no `E.load_asof`); `E.load_asof_at(stem, iv, cut_ms)` and `E.load_funding_asof_at(stem,
  cut_ms)` (L-D.28); `E.tc11_record(rel)`, `E.tc10_record(rel)`, `E.x_rec(rel)` (L-D.27); `E.lineage_shas() ->
  {repo-relative path: sha256}` of the lineage modules loaded in this process, as P6 re-hashed them;
  `E.verified_reads() -> sorted repo-relative paths` that `tc11_record` / `x_rec` verified in this process;
  `E.read_set()` (L-D.27); the referee's `E.hook_escapes`, `E.opened_paths`, `E.import_audit`, `E.classify`.

**The VA-wall exit check (hunk 7; L-0.22 leg (i-b) owns the law, this hunk is its code).** The shim holds two typed
tuples — `VA_WALL_DOORS = ("tierc12_va", "tierc12_va_trades")` and `VA_WALL_FIXTURES = ("tierc12_va_fixtures",)`,
the same members as L-0.22's `DOORS_T` and `VA_MODULE_FIXTURES_T` — and registers an exit check in every process
that imports it. At exit, with `stem` = the stem of `sys.modules["__main__"].__file__` (a spawn worker inherits its
parent's; a process with no such file has the empty stem), the check logs `BLOCKED:va-wall <name>` and the process
is forced to exit 70 if either holds:
  (W1) `stem ∉ VA_WALL_DOORS ∪ VA_WALL_FIXTURES` and `sys.modules` holds `analytics.value_area` or a
  `VA_WALL_DOORS` name;
  (W2) `stem ∉ VA_WALL_DOORS`, `stem` does not end `_fixtures`, and `sys.modules` holds `analytics.profile`.
(W2 exempts the two doors by name: a door is the one non-fixture module that calls the house profile — L-0.22: "no
non-fixture module but a door may" — and the value-area module itself imports nothing of the repo, so a door
process always holds `analytics.profile`. A profile clause without that exemption would refuse Stage V itself.)
Mechanics: the check is registered with `atexit` AFTER the referee's `_exit_report` (ENV11:1151), so it runs
BEFORE it; it appends one `BLOCKED:va-wall` row per offending module to the audit log, and the referee's own report
prints the rows and forces the exit — one forced-exit path, not two. The same predicate is evaluated whenever
`E.read_set()` is called, and a violation there raises `AuditHalt` after logging the same row: a pool does not
read a worker's exit code, and every worker hands its read set back with its result (L-0.13), so a worker that
loaded a door fails its task where its parent sees it. Nothing here imports, names as an identifier, or computes
anything of the value area: the three module names are string constants.

**The post-shim clauses (hunk 4), each a HALT, all evaluated BEFORE the hook is armed:**
- P1 `PIN_MS == D.load_pin() == TP.stage_d_pin()` (the referee's clause, now by object); a value equal to
  `TC11_PIN_MS` or `TC10_PIN_MS` is reported as "the TC11 pin LEAKED" / "the TC10 pin LEAKED".
- P2 `TC10_PIN_MS < TC11_PIN_MS < PIN_MS`; each a multiple of the 4h step; `TC10_PIN_MS` equals TC11's record key.
- P3 `progress/TC12-D.json` exists with status COMPLETE-VERIFIED, and `data/AS_OF_PIN.json`, `STAGE_D_MANIFEST.json`,
  `fee_schedule.json`, `CONTRACT_SPECS.json` each hash to the `{bytes, sha256}` that
  `tierc12_progress.certified(<path>)` returns, the record it names being `TC12-D` (the sha-first law applied to
  TC12's own substrate records: no stage runs on an unverified Stage D; no sha is taken from a record by name).
- P4 fees: every taker == `R2.FEE_BPS_SIDE` (the referee's clause); one row per `PANEL17` stem; each row's maker
  equals its venue block.
- P5 ticks: one per `PANEL17` stem, each a finite `Decimal` > 0.
- P6 lineage pins (L-D.29): `env/LINEAGE_PINS.json` hashes to what `certified()` returns for it (record
  `TC12-ENV.vendor`); the one X record read here (`BOOK_SPECS.json`) is a verified read — the `x_rec` manifest's own
  sha against `certified()`, then the file's sha against its manifest row.
- P7 `sys.modules` holds no module named `tierc11_*` or `tc11x_*`, none whose name contains a forbidden substring
  (the referee's four and `value_area`), and no module or `sys.path` entry under `X_WORKTREE`.
- P8 every `KLINES` / `FUNDING` binding of every estate module lies under the bound snapshot (the referee's clause);
  `TP.substrate()` names it.
- P9 no undeclared module global names the TC10 or TC11 snapshot, the live cache, `research_outputs/tierc10` or
  `research_outputs/tierc11` (the referee's scan, widened by hunk 8).
SOURCE: ENV11:115-134, :192-215, :284-357, :395-431, :639-641, :681-711, :714-752, :769-797, :868-870, :898-946,
:952-1019, :1025-1055, :1062-1108, :1129-1151, :1161-1163, :1369-1377 [verified here]; X's nine hunks (XD:616-628)
as the form; O-29 (the exit clause), O-31; `M/scripts/tierc12_progress.py` (the process tool that gains `certified`
at the TC12-REG commit, L-0.4).
RIVALS: fewer hunks by leaving the referee's identifiers with their old names — not taken: an identifier that says
`TC11` while holding the TC12 snapshot is a standing misreading. A typed `PIN_MS` hunk (X's and TC11's way) — not
taken: O-7, CON:8. `X_REC` under the running tree's `OUT` — not taken: a detached review worktree holds the manifest
and none of the copies. A range-door exception for one TC12 module — not taken: no TC12 module imports the range
machine. An import-time refusal of the value-area module in place of the exit check — not taken: the two door
scripts and their fixture import it lawfully after the shim, and O-29 states the clause at exit.
FAILS-IF: F-VENDOR (the hunks are the whole diff: any undeclared byte is RED — L-D.25's plants); F-REROOT (hunks
1-4; its mutant shims); F-SUBSTRATE (hunks 5-6; one plant per class); F-CLOSURE-ENV (hunk 7: the forbidden names,
the closed door, the exit check and its two tuples; its plants); F-ENV-ASOF and `F-TOLL [reader]` (hunks 4 and
10) — all L-D.31. L-0.22's leg (i-b) proves the exit check on the stage builders.

**L-D.27 PROTECTION — WHAT AN ARMED TC12 PROCESS CANNOT READ OR WRITE** — ruling O-3 "TC12's env shim write-protects
all of them"; O-4; O-1
READING: once `tierc12_env` has finished importing, the audit hook refuses (AuditHalt, forced exit 70, logged
BLOCKED) each of the following. Paths are judged canonically, in the main tree AND in the tree the shim runs from.

READ-NEVER (any open, listing or mutation):
| class | root | why |
|---|---|---|
| `live-cache` | `~/.cache/naiad/data_cache` | referee; O-8 |
| `tc10-snapshot` | `~/.cache/naiad/snapshots/tc10_20260921` | referee |
| `tc11-snapshot` | `~/.cache/naiad/snapshots/tc11_20260925` | NEW — one process, one substrate (O-5); TC11-corridor reads come from the bound snapshot by look-back (L-D.28) |
| `tc12-snapshot-out-of-scope` | any FILE under the bound snapshot that is not one of the 124 in-scope paths (the set read at import from `STAGE_D_MANIFEST.json files[].path`) | NEW — the 52 ride-along files are stale (1m ends 2026-08-15; nine 15m tapes end at TC10's edge) |
| `x-worktree` | `MAIN_TREE/.claude/worktrees/tierc11x` | NEW — O-4: X is read ONLY from `x_rec` |
| `x-merged` | `<tree>/research_outputs/tierc11x`, `<tree>/scripts/tc11x_*` (absent today; present if X merges mid-build) | NEW — O-4 |
| `tc10-unlisted` | under `research_outputs/tierc10`, not on `TC10_ALLOW` | referee |
| `tc11-unlisted` | under `research_outputs/tierc11`, not on `TC11_ALLOW_FILE` — a FILE that is not on the list, and any LISTING of a directory there | NEW — the sha-first read law |
| `x-rec-unlisted` | under `X_REC` (the main tree's `research_outputs/tierc12/x_rec`), not a `copy` path of `X_REC_MANIFEST.json` (nor the manifest itself); any listing of a directory there | NEW — O-4 |
| `tc11-unverified`, `x-rec-unverified` | an open of a `tc11-allow` / `x-rec` path whose sha the path's read function (`E.tc11_record` / `E.x_rec`) has not yet asserted in THIS process | NEW — O-4 "each read asserted"; it makes the sha-first law a refusal instead of a convention |

WRITE-NEVER (any write-mode open, rename, remove, mkdir, chmod, utime, link, copy-into):
| class | root | matching |
|---|---|---|
| referee's | `research_outputs/tierc10`, `research_outputs/tierc10_run2`; `scripts/tierc10_*`; `exchange/status/LEDGER*`; `LEDGER.md`; `.gitignore` | as in the referee |
| `tierc11-write` | `<tree>/research_outputs/tierc11` | separator-aware DIRS class — NEVER the raw-prefix class (`research_outputs/tierc11` is a string prefix of `research_outputs/tierc11x`; X's lesson, `LEANS_X.md:302-303`) |
| `tierc11-script-write`, `tc11x-script-write` | `<tree>/scripts/tierc11_*`, `<tree>/scripts/tc11x_*` | raw-prefix class |
| `x-rec-write` | `X_REC` (the main tree's `x_rec/`, where the copies are), and the same directory of a detached tree (it holds only the tracked manifest) | DIRS |
| `stage-d-write` | `<tree>/research_outputs/tierc12/data` | DIRS — Stage D's records are write-never for every later stage (Stage D's own builder never imports the shim) |
| `vendor-write` | `<tree>/research_outputs/tierc12/vendor` | DIRS |
| `exchange-write` | `<tree>/exchange` (the whole bus: the two earlier TC contracts (TC10 RESUME, TC11), TC12's own, the ledgers, `exchange/rows`) | DIRS — O-1: nothing is written under `exchange/` before CLOSE, and the close acts are the operator's (O-12); the ferry is staged off-bus (O-24) |
| `cache-write` | `~/.cache/naiad` (both old snapshots, the live cache, the BOUND snapshot, the provenance directory) | DIRS — the bound snapshot is read-only once Stage D is certified |
| `mirror-write` | `/Volumes/LaCie` | DIRS — only `--mirror`, a plain process, writes there |

ALLOWED READS that are LOGGED (class ALLOW) and sha-verified by their read function — the function asserts the sha
with its own open, and only then does the hook let any other open of that path through (`tc11-unverified` /
`x-rec-unverified` above):
- **TC11 records** — `E.tc11_record(rel)` returns the absolute MAIN-tree path only for a `rel` on `TC11_ALLOW_FILE`,
  after asserting the file's sha equals the one `MR/PROGRESS.json` certifies. `MR/PROGRESS.json` itself is accepted
  at its R0 sha (`progress/TC12-R0.json["frozen_estate_shas_at_r0"]`) OR at the value
  `T12/close/TC11_STAMP_MAP.json` names for it when that map reads `applied: true` (L-0.24: TC12's own close act
  re-pins that file, and no TC12 pin is a whole-file sha of a file TC12's close acts move).
  `TC11_ALLOW_FILE` is hunk-6 DATA — the union of every section's rows, complete (`rel` under
  `research_outputs/tierc11/`; each of them is certified in `MR/PROGRESS.json` [verified here: 42 of 42, the
  PROGRESS row apart]): `PROGRESS.json`, `LEANS.md`, `data/{AS_OF_PIN.json, fee_schedule.json,
  STAGE_D_MANIFEST.json, CONTRACT_SPECS.json}`, `books/{v6_journal, v6_campaigns, trg912_journal,
  trg912_campaigns}.parquet`, `books/build_manifest.json`, `scores/{BASE_IDENT.json, SCORES.json}`,
  `registrations/{REGISTRATIONS.json, REGISTRY_PIN.json}`, `stage_g/{g_campaign_gates, g_grid_books,
  g_grid_partition}.parquet`, `stage_g/{build_manifest.json, STAGE_G.md}`, `stage_r/{NEST_v6, NEST_trg912,
  R5_CHOP_DIRECTION}.parquet`, `stage_r/R5_CHOP.md`, `ranges/{SCALE_GRID.parquet, SCALE_PICKS.json}`,
  `stage_r4/{R4_NULL_BOXES.parquet, build_manifest.json}`, `stage_h/tp_bars.parquet`,
  `forward/{FORWARD_LEDGER.jsonl, FORWARD_LEDGER.md}`, `regbooks/P-AGE-1/{base, scored,
  tierE__shadow_abs206}.{parquet, json}`, `regbooks/P-WIN-1/scored.{parquet, json}`,
  `regbooks/P-TP-RNG/scored.{parquet, json}`, `regbooks/P-BRK-4H/scored.{parquet, json}`. A row is added only by a
  dated amendment (it is a hunk). The rows this section itself reads are `PROGRESS.json` and the four under `data/`.
- **X records** — `E.x_rec(rel)` returns the absolute MAIN-tree path after asserting the file's sha equals its
  `X_REC_MANIFEST.json` row (O-4), the manifest's own sha having first been asserted against
  `tierc12_progress.certified("research_outputs/tierc12/x_rec/X_REC_MANIFEST.json")` — the LAST record that names
  the manifest, never `TC12-R0` by name (O-25 added a row after R0). The classes `x-rec`, `x-rec-unlisted` and
  `x-rec-write` are judged on that root, `X_REC`.
- **TC10 records** — `E.tc10_record(rel)`: the referee's function and its eight records, unchanged.
- **The read set.** `E.verified_reads()` lists what the two read functions verified. `E.read_set() -> {class:
  sorted paths}` returns every READ open since the hook was armed whose class is one of `tc12-snapshot`,
  `tc10-allow`, `tc11-allow`, `x-rec`, or `tc12-record` (a path under `T12/` outside any `_det_*` segment); paths
  are repo-relative, or snapshot-relative for the snapshot. L-0.13's manifest helper writes it, united over the
  builder process and its spawn workers, beside every `build_manifest.json` as `<dir>/READ_SET.json`. That file —
  not an in-memory log, which no other process can see — is what the fixtures read: each stage's fixture asserts
  from that directory's `READ_SET.json` that every path under the bound snapshot is in the stage's declared read
  set, that every `tc11-allow` path is a row of `TC11_ALLOW_FILE`, and that every `x-rec` path is a `copy` path of
  the manifest; that each of the last two was sha-verified before it was read is what the refusal above enforces
  and F-SUBSTRATE proves.
NOT refused by the hook (stated): reads of the repo outside the classes above — in particular the TEXT of a
frozen-estate script (`scripts/tierc10_*.py`, `scripts/tierc11_*.py`: write-never, not read-never; reading one by
`ast` is an ordinary repo read, importing or running one is what P7 and L-0.22 forbid), `.git/` objects, and
`exchange/` (write-never only); writes elsewhere in the repo outside the write-never classes (TC12's own outputs
under `research_outputs/tierc12/` are written freely); I/O the hook cannot see (L-D.25).
SOURCE: ENV11:284-357, :395-431, :1062-1108, :1161-1176; O-1, O-3, O-4, O-5, O-12, O-24, O-25; X's hunks 4-5
(`LEANS_X.md:299-314`); `MR/PROGRESS.json` (`stages[].artifact_shas`) and `progress/TC12-R0.json`
(`frozen_estate_shas_at_r0`) [verified here]; U3 hazards H4, H5; U4 §1.1 (what the out-of-scope tapes hold).
RIVALS: a WHITELIST (writes allowed only under `research_outputs/tierc12` and temp directories) — not taken: a
library's cache write would HALT a ride for no substrate reason; the referee's blacklist form is the reviewed one.
Leave `exchange/` writable — not taken: O-1 is then a convention, and the 07:00 routine publishes whatever is there.
Leave the TC11 snapshot readable for an anchor process — not taken, L-D.28. A fixture that checks "verified before
read" from the hook's in-memory log — not taken: a fixture is another process and a builder's workers are others
still; the refusal needs no log. A listing allowance on TC11 directories — not taken: no stage lists one.
FAILS-IF: F-SUBSTRATE (L-D.31): one plant per class above, each in a subprocess, each of which must be refused naming
ITS class and end in exit 70 — among them a raw `open` of an allow-listed TC11 record, and of a manifest-listed X
record, made WITHOUT its read function (`tc11-unverified`, `x-rec-unverified`), and a listing of a TC11 directory.

**L-D.28 TC11-CORRIDOR READS: THE LOOK-BACK PIN ON THE TC12 SNAPSHOT; NO TC11-BOUND PROCESS** — "F-CTRL reproduces
TC11's filed v6 book … on TC11's corridor … cross-process anchored" (contract :48-49); ruling O-5
READING: every TC12 process binds exactly ONE substrate, the TC12 snapshot. Anything that must be computed "on TC11's
corridor" is computed on the TC12 tape with a LOOK-BACK, and anchored against a record FILED by TC11's or X's own
process. No TC12 process binds the TC11 snapshot; no "anchor process on the tc11 snapshot" is built.
- **Lineage rides** (the control and every book that goes through `T9.replay9`): `TP.corridor_n` called with
  `pin_close_iso=E.TC11_PIN_ISO` returns `(lo, hi)` with `hi + 1 == TC11_PIN_MS` — the function admits a pin only if
  it is a 4h close and LOOKS BACK ("a pin may only look back", `M/scripts/tierc10_panel.py:690-699`). The frames are
  the whole TC12 4h tape; EMAs and ATR are causal recursions, so their values at bars ≤ the look-back pin do not
  depend on later bars; the ride is bounded by `hi`.
- **Precedent — F-912-ANCHOR:** TC11 rode the 9/12 book and v6 over TC10's window on the LONGER TC11 tape with
  `corridor("2026-09-21T16:00:00Z")` and reproduced TC10's filed book shas bit for bit (`MR/books/BOOKS.md:27-28`:
  `b2276fa4…` n 198; `2bd244bf…` n 200). A book ridden to an earlier pin on a longer tape is the same book.
- **Frames for everything that is not a lineage ride** (the value area, ATR per lens, the 5m walk, every as-of
  fixture leg of every section): `E.load_asof_at(stem, iv, cut_ms)` = the rows of the bound file with `open_time +
  STEP_MS[iv] ≤ cut_ms`, ascending, read through pandas on a path string into FRESH arrays (never a symbol-keyed
  memo); HALT unless `cut_ms` is an int `≤ PIN_MS`, and on a missing file. **Any instant is admitted** — there is
  no 4h-modulus clause: an off-grid instant such as `ERA_CUT_MS` cuts each lens at its last bar closed at or before
  it (the 1h bars closing 21:00, 22:00 and 23:00Z of the last tuning day are tuning bars, and a cut at the last 4h
  close would lose them). `E.load_funding_asof_at(stem, cut_ms)` likewise = the prints with floor hour `≤ cut_ms`,
  with `funding_hour_ms`. `load_asof_at(·, ·, PIN_MS)` is asserted frame-identical to `E.D.load_asof(·, ·)`, the
  lineage's reader at the pin (there is no `E.load_asof`). The Stage D module's two functions of the same names
  (L-D.11) are the same cut law for the Stage D fixtures, which cannot import the shim; the two texts are held to
  ONE referee — TC11's manifest `content_sha` per file — by F-D-PREFIX [ii] and by F-ENV-ASOF.
- **Why the look-back cut IS TC11's tape:** F-D-PREFIX (L-D.12) proves the TC12 file cut at TC11's pin bit-identical
  to the TC11 snapshot's file, and F-ENV-ASOF (L-D.31) re-proves through the shim's own cut function that
  `frame_sha(load_asof_at(stem, iv, TC11_PIN_MS))` equals TC11's manifest `content_sha` for all 124 files. That is
  the substrate half of "cross-process anchored"; the book half is L-C's (the referee is TC11's FILED journal, by
  sha — a record written by another process in another build).
- **One tape per process.** Every memoised frame (`T5._FRAMES`, `BK._FRAMES`, the role and tide memos — keyed on the
  bare symbol) is the TC12 tape cut at the TC12 pin. A look-back is an INDEX BOUND on that tape or an un-memoised
  `load_asof_at` frame handed to a pure function; it is never a second frame stored under a memo key.
- **The hazard this closes** (U4 H3): `tierc2_baseline.load_klines` reads a whole file with no as-of cut. On TC11's
  snapshot every file ended at the pin; on TC12's, a TC11-corridor computation that used a whole-file frame WITHOUT a
  bound would read 83 4h bars past TC11's pin. Every TC11-corridor quantity therefore states its bound (`hi`, or
  `cut_ms`), and each consuming section's as-of fixture plants the unbounded read.
SOURCE: `M/scripts/tierc10_panel.py:650-733` [verified here]; `MR/books/BOOKS.md:24-30` [verified here]; TC11 L-1.6,
L-1.7 (`MR/LEANS.md:152-167`); D11:2487-2528; U3 §1.3, §1.7, R2, hazards H2, H9; U4 R15, H3; U6 hazard H2.
RIVALS: (a) a TC12 anchor process bound to `tc11_20260925` (a second guard value, or a second shim) — not taken: it
adds a degree of freedom to every number ("which snapshot was this from"); every TC11-corridor referee TC12 needs
already exists as a filed record ridden on that snapshot by TC11 or X, which is a stronger anchor than a TC12 re-run;
and by F-D-PREFIX such a process could only reproduce the look-back. (b) whole-file frames with no bound, trusting
causality of the indicators — not taken: `armings9` scans the whole tape for a window's end (U3 H9); the bound is
what keeps the book causal.
FAILS-IF: F-ENV-ASOF (L-D.31): FAILS IF the cut at TC11's pin is not TC11's file by content sha and row count, the
cut at the pin is not the lineage's frame, an off-grid cut does not end at the last bar closed at or before it, or
a cut past the pin is accepted. Planted mutations there: a cut-function copy cutting on `open_time ≤ cut_ms` (one
bar too many); one cutting funding on the raw stamp; one that drops zero-volume bars; one that floors `cut_ms` to
the 4h grid. The book-level proof is L-C's F-CTRL.

**L-D.29 THE LINEAGE MODULES — IMPORTED AS-IS, RE-HASHED BEFORE ANY RIDE** — "F-CTRL … to 0.000e+00" (contract :48-49)
READING: TC12 edits and forks NO lineage module. The shim imports them unchanged through the referee's import section
(no hunk touches it), under the referee's aliases (L-D.26): `tierc2_baseline` (TB), `tierc10_data` (D),
`tierc10_panel` (TP), `tierc10_brk` (BK), `tierc10_lanes` (LN), `tierc9` (T9), `tierc8` (T8), `tierc7` (T7),
`tierc7_rules` (R7), `tierc7_lab_regime` (LAB), `tierc6` (T6), `tierc6_rules` (R6), `tierc5` (T5), `tierc5_rules`
(R5), `tierc4_rules` (R4), `tierc3_rules` (R3), `tierc2_rules` (R2) — and, through them, `tierc3_baseline`,
`tierc4_baseline`, `engine.*` and the `analytics` package with its `structure`, `vwap`, `volatility` and `momentum`
submodules (never `analytics.profile` [verified here: no lineage or engine module imports it], and never
`analytics.value_area`). (Importing the `tierc10_*` LIBRARY modules through the shim's windows is TC11's and X's
precedent; what O-3 forbids is RUNNING a TC10/TC11/X suite, scorer or builder.)
- **The referee of the ride path is X's filed record** `XR/tierc11x/forward/BOOK_SPECS.json["path_modules"]` (its sha
  asserted against its `X_REC_MANIFEST.json` row, the manifest's against `tierc12_progress.certified`; orientation
  `72a1f523…cac3`): 21 keys. The 18 that are main-tree files —
  `engine/indicators.py`, `engine/s1.py`, `scripts/forward_log.py`, `scripts/tierc10_data.py`, `tierc10_panel.py`,
  `tierc2_baseline.py`, `tierc2_rules.py`, `tierc3_rules.py`, `tierc4_rules.py`, `tierc5.py`, `tierc5_rules.py`,
  `tierc6.py`, `tierc6_rules.py`, `tierc7.py`, `tierc7_lab_regime.py`, `tierc7_rules.py`, `tierc8.py`, `tierc9.py` —
  must each hash, in the main tree NOW, to X's value. [verified here: 18 of 18 equal.] The 3 that are X's own
  (`scripts/tc11x_books.py`, `tc11x_env.py`, `tc11x_forward.py`) are never imported; they are asserted equal to their
  `x_rec/scripts/` copies.
- **Modules the shim loads that X's record does not pin** (`tierc10_brk`, `tierc10_lanes`, `tierc3_baseline`,
  `tierc4_baseline`, the `engine` and `analytics` modules, and everything else in the static closure) are pinned by
  TC12's own write-once record `research_outputs/tierc12/env/LINEAGE_PINS.json`: {`walk_roots` (the 17 names above,
  read by AST from the REFEREE's import section — the shim is not built when the record is written, and no hunk
  touches that section, so the built shim's roots are the same and F-LINEAGE holds them equal), `modules` {relative
  path: sha256} for the STATIC repo import closure of those roots (Import / ImportFrom anywhere, function bodies
  included, constant-string dynamic imports — the walk of `M/scripts/tierc11_closure_fixtures.py:449-471`,
  mirrored, NOT stopping at the TC10 layer: pinning is a superset law), `x_path_modules` {record path, sha,
  `n_main_tree_keys`, `all_equal`}, `step_q_commit`}. It is written by `scripts/tierc12_vendor.py --pin-lineage`,
  a plain process that only hashes files, inside the record `TC12-ENV.vendor` (L-D.25), which pins its bytes.
  This pinning walk does not stop at the TC10 layer; it is a different walk from F-CLOSURE's, which discloses the
  TC10 layer and does not walk it (L-0.22 (ii)). The two never disagree about a module: this one HASHES every
  module the lineage can load — the range machine's files included, which the function-local imports of
  `tierc10_brk` and `tierc10_lanes` reach statically and which no TC12 process ever loads (P7; hunk 7's closed
  door) — while F-CLOSURE's judges what a decision module may IMPORT and takes this record's `modules` as the
  name, path and sha of the TC10 layer it discloses.
- **Before any ride** — post-shim clause P6, at EVERY import of the shim, in every process and every worker: each
  estate module loaded in the process (the referee's `_estate_modules()`: files under this tree, TC12's own
  `tierc12_*` scripts apart — those are pinned by their stage records) is re-hashed; it must be a key of
  `LINEAGE_PINS.json["modules"]` with an equal sha (a loaded module absent from the static closure HALTs: the walk
  missed it), and each of X's 18 must equal X's value. An absent `LINEAGE_PINS.json`, or one whose bytes are not
  those `certified()` returns, HALTs ("run scripts/tierc12_vendor.py --pin-lineage"). A drifted lineage module
  HALTs the build; it is never re-pinned silently.
- Defaults bound at def time are never relied on: every call passes `seed` and `n_boot` explicitly (O-22; ENV11:86-92).
SOURCE: `XR/tierc11x/forward/BOOK_SPECS.json` [verified here: 21 keys; hashes compared]; ENV11:714-752, :898-912;
U3 §1.2, §1.12, R15; `M/scripts/tierc11_closure_fixtures.py:449-471`; `M/scripts/tierc10_brk.py:2357`, `:2380` and
`M/scripts/tierc10_lanes.py:1246` (the function-local range imports); `M/scripts/tierc2_baseline.py:79-82`,
`M/analytics/__init__.py` (the package imports no submodule) [verified here].
RIVALS: vendor copies of the lineage into `tierc12_*` files — not taken: a fork is a new book; F-CTRL's 0.000e+00 is a
statement about THESE modules. Pin only X's 18 — not taken: the shim loads modules X's ride path does not name. Stop
the pinning walk at the TC10 layer, as the closure walk does — not taken: a drifted file of that layer is a moved
estate byte whether or not anything imports it.
FAILS-IF: F-LINEAGE (L-D.31): FAILS IF one of X's 18 differs in the main tree, the pins are absent, rewritten or
differ from a file now or from its blob at the STEP Q commit, a module a fresh shim import loads is absent from the
pins, or the shim imports with a drifted module. Planted mutations there: a one-byte-edited copy of a lineage
module first on a temp `sys.path` (the import must HALT at P6); a pins copy with one sha altered.

**L-D.30 ONE PROCESS, ONE SUBSTRATE — THE RUN LINE AND THE STAGE ORDER** — ruling O-5; contract :5-6 "resume law …
commit + PROGRESS.json per stage"
READING:
- **Run lines of every shim-armed process:**

      export NAIAD_CACHE_DIR="$HOME/.cache/naiad/snapshots/tc12_20261008" PYTHONDONTWRITEBYTECODE=1
      ~/venvs/naiad/bin/python -B /Users/luis/Naiad/scripts/<module>.py

  The variable is exported BEFORE python starts (`tierc2_baseline` binds `KLINES` / `FUNDING` at import,
  `M/scripts/tierc2_baseline.py:205-206`); unset, `cache_dir()` would bind the LIVE cache; a `~` or relative value
  would make it `mkdir` a stray directory (ED:39-48) — hunk 2's guard HALTs on all three before any engine import.
- Every child process (fixture subprocesses, `multiprocessing` spawn workers) re-arms the hook by importing the shim
  FIRST and inherits both variables. A worker hands `E.read_set()` back with its result (L-0.13's manifest helper
  unites the sets); that call also evaluates the VA-wall predicate (L-D.26), because a pool does not read a
  worker's exit code.
- **Order of this section's records** (O-6, O-31; the positions are L-0.10's resume order):
  `TC12-D` (L-D.5 steps 1-7) → `TC12-ENV.vendor` (referee and `scripts/tierc12_vendor.py` committed; three-sha
  equality; `--pin-lineage`) → `TC12-ENV` (the shim built from referee + hunks; `env/LEAN_BLOCK.txt`;
  `env/SUBSTRATE_VERIFY.json` — all 124 in-scope snapshot files re-hashed against the manifest;
  `env/FIXTURES_ENV.txt`). One commit per record: `tierc12(TC12-D): …`, `tierc12(TC12-ENV.vendor): …`,
  `tierc12(TC12-ENV): …`. `TC12-D.mirror` hangs off TC12-D, is in no position of the order and blocks nothing
  (L-D.24). TC12-ENV has several producers (this section; L-0's tables, as-of and attestation tools), so its
  parent record is written by the orchestrator's gate step from the artifact maps the producers return (L-0.10);
  this section's map is `scripts/tierc12_env.py`, `env/LEAN_BLOCK.txt`, `env/SUBSTRATE_VERIFY.json` and
  `env/FIXTURES_ENV.txt`. The shim cannot be imported before TC12-D is COMPLETE-VERIFIED and the lineage pins are
  filed (P3 and P6 HALT); no later record starts before the TC12-ENV record is COMPLETE-VERIFIED (L-0.10's start
  law).
- **Which record files which script of this section:** `TC12-D` — `scripts/tierc12_data.py`,
  `scripts/tierc12_tick.py`, `scripts/tierc12_data_fixtures.py` (both of its invocations are in the one file);
  `TC12-ENV.vendor` — `scripts/tierc12_vendor.py` and `scripts/tierc12_env_fixtures.py` (written whole before the
  vendor gate, because its first invocation runs there; if its bytes change before the TC12-ENV gate it is
  re-recorded there under L-0.4's last-record law); `TC12-ENV` — `scripts/tierc12_env.py`.
- **Untracked artifacts of these stages** (pinned by sha in their progress record, O-2): the snapshot itself
  (described by the manifest), the fee-source bodies. Everything else this section writes is a document of record and
  is tracked.
SOURCE: O-2, O-5, O-6, O-31 (OR:216-218: "The env shim is vendored and proven inside TC12-ENV, after TC12-D"); L-0.10
(the sub-stage law); ED:39-48; ENV11:86-97; `LEANS_X.md:86-97` (X's order at X-D: referee, extraction, pin, then the
shim).
RIVALS: build the shim before Stage D — impossible: its pin is read from Stage D's record. File the referee at the
registration stage — not taken: O-31.
FAILS-IF: F-D-GUARD (the data module: each bad `NAIAD_CACHE_DIR` must HALT before `engine.data` loads; L-D.15);
F-SUBSTRATE's guard plants and F-REROOT (the shim: an unset, relative or foreign value, or a process with bytecode
writing on, must HALT at import; L-D.31); L-0's F-RESUME holds the order of the records.

**L-D.31 THE ENV FIXTURE ROLL** — "import-closure · worktree attestation" (contract :124); "F-DET hash-identical"
(contract :123)
READING: one suite, two invocations, one transcript each:

| invocation | record | transcript | hosts |
|---|---|---|---|
| `scripts/tierc12_env_fixtures.py --stage=TC12-ENV.vendor` | `TC12-ENV.vendor` | `env/FIXTURES_ENV_VENDOR.txt` | `F-VENDOR [referee]` (L-D.25) — no shim import; its header pin is read from `data/AS_OF_PIN.json` |
| `scripts/tierc12_env_fixtures.py` | `TC12-ENV` | `env/FIXTURES_ENV.txt` | F-VENDOR, F-SUBSTRATE, F-REROOT, F-ENV-ASOF, F-LINEAGE, `F-TOLL [reader]`, F-CLOSURE-ENV, F-ENV-DET |

Audit hooks cannot be removed, so every hook plant and every mutated copy of the shim runs in a SUBPROCESS; mutated
copies live in a temp directory placed first on `sys.path`; write plants aim at directories that do not exist; read
plants at files that do not exist or, for the old snapshots, at a path whose open is refused before any byte is
read. The legs of `env/FIXTURES_ENV.txt`:

| leg (one block each) | FAILS IF | planted mutation / plant that must be caught |
|---|---|---|
| F-VENDOR | L-D.25, the second block | L-D.25's seven |
| F-SUBSTRATE | any plant is not refused by the hook naming its own class and ending in exit 70; the guard of hunk 2 accepts a bad `NAIAD_CACHE_DIR` or a process with bytecode writing on; OR a representative run (one home asset's 4h frame through TB, the v6 control over the look-back corridor, one `tc11_record`, one `x_rec`), watched by THIS file's own recording hook installed before the shim, opens any path outside {the 124 in-scope snapshot files, the repo minus the protected classes, the allow-listed and verified records, the interpreter, OS directories}; OR `E.read_set()` of that run is not, class for class, what the recording hook saw for the five judged classes; OR `E.classify` over every file under `research_outputs/tierc11` and the main tree's `x_rec` (the files listed by a subprocess that never imports the shim — TC11's form) allows anything that is not a row of `TC11_ALLOW_FILE` or a `copy` path of the manifest | one per class of L-D.27: a read of the TC10 snapshot; of the TC11 snapshot; of the live cache; of a 1m tape in the bound snapshot; of the X worktree; of an unlisted TC11 record; a listing of a TC11 directory; of an `x_rec` path not in the manifest; a raw `open` of an allow-listed TC11 record and of a manifest-listed X record WITHOUT its read function (`tc11-unverified`, `x-rec-unverified`); a write under `research_outputs/tierc10`, `…/tierc11`, `…/tierc12/x_rec`, `…/tierc12/data`, `…/tierc12/vendor`, `scripts/tierc10_*`, `scripts/tierc11_*`, `exchange/` (rows, queue, LEDGER*), the bound snapshot, `/Volumes/LaCie`; each also as a case variant and through the `/System/Volumes/Data` firmlink; an AuditHalt swallowed in a thread (exit must still be 70); each bad guard value (unset, `~`, relative, the live cache, the TC10 or the TC11 snapshot, a foreign directory) and a run without `-B` (each must HALT at import); three shim copies re-pointed at temp trees: `TC11_OUT` holding the true PROGRESS and one allow-listed record with a byte flipped (`tc11_record` must HALT naming the record); `TC11_OUT` holding a PROGRESS copy at a third sha, neither R0's nor a mapped one (it must HALT naming PROGRESS); `X_REC` holding the true manifest and one copy with a byte flipped (`x_rec` must HALT naming the copy) |
| F-REROOT | `E.PIN_MS` ≠ the value in `data/AS_OF_PIN.json` ≠ `E.D.load_pin()` ≠ `E.TP.stage_d_pin()`; `E.TC11_PIN_MS` ≠ TC11's record; any constant of the closed re-root list (TYPED IN THE FIXTURE with its intended target — a second object) resolves anywhere but that target; `E.X_REC` is not the MAIN tree's `research_outputs/tierc12/x_rec`; any module global still names TC10 or TC11 outside the declared set; `E.SEED` ≠ the seed L-0's pin door derives from the contract; `E.TP._U12` is not TC12's manifest; `E.ticks()` is not, stem for stem, the `price_tick` STRINGS of `data/CONTRACT_SPECS.json` at the sha `certified()` returns; a module alias or object of L-D.26's API list is absent, or `E.LR` / `E.RC` exists | mutant shims that skip `D.OUT`, `TP.AS_OF_PIN` or `D.SNAPSHOT` must HALT at the post-shim; a mutant whose pin hunk reads TC11's pin record must HALT "the TC11 pin LEAKED"; a mutant with a typed `PIN_MS` must be RED at F-VENDOR; a mutant whose `ticks()` returns floats, and one that reads TC11's `CONTRACT_SPECS.json`; a mutant whose `X_REC` is `OUT/x_rec`, run from a scratch tree that holds the manifest alone (it must fail on a missing copy) |
| F-ENV-ASOF | `load_asof_at(s, iv, PIN_MS)` is not frame-identical to `E.D.load_asof(s, iv)` for every in-scope kline; `frame_sha(load_asof_at(s, iv, TC11_PIN_MS))` or its row count ≠ TC11's manifest `content_sha` / `rows` for any in-scope kline file, or the funding analogue for any funding tape; for `cut_ms` in {`ERA_CUT_MS`, a seeded 1h close off the 4h grid, a seeded 5m close} (one seeded 1h close and one seeded 5m close per stem — this leg's fixture-typed count — drawn from the stem's own tape on this leg's stream, the common law's form with suite tag `env` and block id `F-ENV-ASOF`; each cut applied to every in-scope lens of the stem): the frame's last close ≤ `cut_ms` < the next bar's close, or the frame is not a row-prefix of `E.D.load_asof(stem, iv)`; a `cut_ms` past the pin is accepted | a cut-function copy cutting on `open_time ≤ cut_ms` (one bar too many); one cutting funding on the raw stamp (drops the at-pin print on 16 tapes); one that drops zero-volume bars; one that floors `cut_ms` to the 4h grid (it loses the 1h bars after the last 4h close before `ERA_CUT_MS`) |
| F-LINEAGE | any of X's 18 main-tree `path_modules` differs in the main tree; `LINEAGE_PINS.json` is absent, not write-once, not the bytes `certified()` returns, or a row differs from the file now or from the file's git blob at the STEP Q commit (read-only `git show`); its `walk_roots` are not the import section of the built shim; a module loaded by a fresh shim import is absent from the pins; the shim imports with a drifted module | a one-byte-edited copy of a lineage module first on a temp `sys.path` (the import must HALT at P6); a pins copy with one sha altered |
| `F-TOLL [reader]` | `E.fees()` is not, stem for stem, the figures of the file at `research_outputs/tierc12/data/fee_schedule.json` at the sha `certified()` returns for it (record `TC12-D`); its key set per stem is not hunk 4's eleven; a maker figure is consumed from any other key or file | a mutant shim whose `fees()` reads `research_outputs/tierc11/data/fee_schedule.json`; one that returns the top-level scalar |
| F-CLOSURE-ENV | a fresh interpreter importing `tierc12_env` holds a module whose name contains a forbidden substring (the referee's four + `value_area`), `analytics.profile`, or any `tierc11_*` / `tc11x_*` module; the shim's source imports one anywhere (AST, function bodies included) or uses I/O the hook cannot see (`hook_escapes`); the range door opens for ANY caller; `E.VA_WALL_DOORS` / `E.VA_WALL_FIXTURES` are not the two tuples this fixture types (`("tierc12_va", "tierc12_va_trades")`, `("tierc12_va_fixtures",)`); or the exit check of hunk 7 is not registered, does not run before the referee's exit report, or misjudges a stem | a shadow shim importing `analytics.value_area`; a lazy in-function `tierc10_stamps` import; `tc10_import("tierc10_census", allow_range=True)` called from a planted module (it must HALT); a `pq.read_table` call planted in the shim; subprocess scripts in a temp directory that import the shim and then place a module object in `sys.modules` under a judged name (no value-area file is needed, and none exists at this gate): `analytics.value_area` under a plain stem → exit 70 with `BLOCKED:va-wall` (W1); `analytics.profile` under a plain stem → exit 70 (W2); `analytics.profile` under a stem ending `_fixtures` → exit 0; `analytics.value_area` under a `_fixtures` stem that is not `tierc12_va_fixtures` → exit 70; `analytics.value_area` and `analytics.profile` under the stem `tierc12_va` → exit 0 (a door is not refused); the first script against a shim copy whose registration is removed → it exits 0, and the fixture's detector must name the missing check; a shim copy whose W2 lacks the door exemption → the door-stem script exits 70, named as the catch; a `read_set()` call in the first script → `AuditHalt` |
| F-ENV-DET | two subprocess emissions of the lean block + probe (hash seeds 1 and the contract seed) differ by one byte from each other or from the filed `env/LEAN_BLOCK.txt` | a hash-order-dependent emission; the comparator on a one-byte-bent copy |

The WORKTREE ATTESTATION (the X worktree at its certified tip with exactly its one untracked file; the frozen-estate
shas of `progress/TC12-R0.json` unmoved) is L-0's; this section supplies the hook that makes a write there impossible
in-process and the fixture that proves the refusal. The IMPORT-CLOSURE of the tier (F-CLOSURE, F-HOOK-ESCAPE, F-WALL,
with the exit leg (i-b) on every stage builder) is L-0.22's; F-CLOSURE-ENV is its fourth block id, the shim's own
half: the shim is value-area-free, range-free and escape-free, and the exit check it supplies works.
SOURCE: L-0.14, L-0.19, L-0.22 (the hosting, block and closure laws); `M/scripts/tierc11_env_fixtures.py:1-100`
(TC11's roll and plant law), :563-612 (the listing by a process that never imports the shim); XF:365-439; ENV11.
RIVALS: none.
FAILS-IF: n/a (this reading is the roll; each row states its failure condition and its plants).

---------------------------------------------------------------------------------------------------------------
### REGISTRATION SPEC · (none owned by L-D)

None. Section L-D owns no registered row: Stage D and the environment have no hypothesis, no family and no verdict
word, and nothing in this section enters the write-once registry. The five registered rows (P-ADM-1, P-BRD-1,
P-DIR-1, P-SFP-VA-1, P-SCALP-3) read from this section only: the pin record, the manifest, the fee file, the tick
strings, and the shim. None of these is a PRECONDITION of any row — no row closes on a Stage D record (L-X.18's field
grammar: the only precondition items of the tier select `va/VA_MIRROR.json`). Where a spec lists the Stage D records
it stands on, it lists them under `inputs pinned:` in its `arms`, by certifying record (`progress/TC12-D.json`
`artifact_shas[<path>]`) — never by a sha value: the registry is filed before Stage D exists.

### OPEN TO OPERATOR

Each item is the operator's alone; the build takes the stated default if he is silent.

1. **The LaCie destination.** No residency rule names a place for a cache snapshot and the operator has never named
   one (`research_outputs/tierc10/OPERATOR_RULINGS.md:36, :64-66`). DEFAULT (O-32 lists it for him): a new
   directory `/Volumes/LaCie/Naiad/snapshots/tc12_20261008/` (+ `/Volumes/LaCie/Naiad/provenance/tc12_20261008/`),
   written by `--mirror` as a sha-verified plain copy when the drive is reachable; NOT RUN, blocking nothing, when it
   is not; nothing else on the drive is touched; the vault `naiad-backups` is not used. A different destination, or
   "not until I say", is his word.
2. **Whether the still-unmirrored TC10 and TC11 snapshots are mirrored too.** DEFAULT: no — TC12 mirrors its own
   snapshot only (the contract's act) and lists the two as unmirrored in the manifest's `operator_rulings_needed`.
3. **The "maker-bps" pin** (veto by name, CON:137). DEFAULT: per venue, the published base rate under L-D.18 when
   the page is retrieved and parsed; otherwise the figure on file (README.md:150) flagged NOT RE-CONFIRMED, applied
   to Bybit as an ASSUMPTION. A figure given by the operator replaces it and is recorded as his. (What a published
   rate does to P-SCALP-3's licence word is L-S's operator item, not this one: here the pin only takes its value.)
4. **Carried from TC10, still open:** which Binance publication is the record on incident bars (TC10's own F-D-1
   finding stands as TC10 filed it — TC12 runs no such leg; DEFAULT: REST only, as TC10 and TC11); `PUMPFUN →
   PUMPUSDT` and `MNT → Bybit` (DEFAULT: as TC10's table); whether charter slippage joins the toll of record
   (DEFAULT: a twin only — the contract says the tiers are unchanged).

### INTERFACE ASSUMPTIONS

- **L-0 (laws / process):** the order of the records is L-0.10's resume order (`… TC12-REG · TC12-REG.ledger-spec ·
  TC12-D · TC12-ENV.vendor · TC12-ENV …`); this section's two side records are the dotted children
  `TC12-ENV.vendor` (blocking) and `TC12-D.mirror` (the one non-blocking child), both on L-0.10's sub-stage table,
  each with one commit and one transcript. L-0's and used here as written: the fixture law of L-0.14 (a leg is one
  `prove` call and one block; block ids; NOT RUN as a third state through `not_run`; no network and no
  drive-dependent leg in a transcript of record; the seeded-stream form; `--root`; the header), the name → block
  map of L-0.19 (F-D-2, F-D-3 and F-TOLL by exact FID; F-TOLL needing its `data`, `reader` and `book`
  qualifiers; F-CLOSURE-ENV under `import-closure`), the scope law of L-0.11, F-DET's form, the typed-number law
  with its refereed-text rule and its unit objects (`scripts/tierc12_units.py`), the contract-pin door
  (`scripts/tierc12_pins.py`, the filed `pins/CONTRACT_PINS.json` and its seed pin), the pin register row
  `fee.maker_bps_side.<VENUE>` (kind `stage_d`, veto `maker-bps`), the amendments law of L-0.5 (source (v), the
  `AM-<n>` heading), `T12/DISCLOSURES_BUILD.md`, and the helper `tierc12_progress.certified` (added to the filed
  process tool at the TC12-REG commit; stdlib only, so the shim may import it). The import-closure, hook-escape
  and wall fixtures are L-0.22's: its typed `SUBPROC_SITE_T` holds the ONE site this section declares,
  `tierc12_data.clone_snapshot` (`cp -cpR`), and treats `scripts/tierc12_vendor.py`, `scripts/tierc12_tick.py` and
  `scripts/tierc12_env.py` as subprocess-free; its `DOORS_T` and `VA_MODULE_FIXTURES_T` have the members of the
  shim's `VA_WALL_DOORS` and `VA_WALL_FIXTURES` (hunk 7), whose exit check is the code of its leg (i-b); its leg
  (ii) takes the name, path and sha of the TC10 layer it discloses from `env/LINEAGE_PINS.json`. L-0.13's manifest
  helper writes `<dir>/READ_SET.json` from `E.read_set()`. The worktree attestation is L-0's. The range door is
  CLOSED for every caller (hunk 7): no TC12 module imports the range machine. `forward/BOOK4_FREEZE.json` is added
  to TC12-D's artifact map by the orchestrator's gate step (L-0.5); this section neither writes nor reads it.
- **L-V (value area):** defines how a zero-volume bar enters the time-at-price twin and prints the count per lookback
  (L-D.16); takes every frame through `E.D.load_asof(stem, lens)` / `E.load_asof_at(stem, lens, cut_ms)`, the latter
  at any instant, off-grid ones included; imports `analytics.value_area` only AFTER the shim and only from the two
  door scripts (`scripts/tierc12_va.py`, `scripts/tierc12_va_trades.py`) and their one fixture module (a process
  that loaded it before the shim HALTs at the post-shim; a process that is none of the three and holds it at exit is
  forced to exit 70, hunk 7); prints `maker_pin.differs_from_x_assumption` beside the "1h maker PASS" word, read
  from the fee file at its certified sha. Its TC11 rows are on `TC11_ALLOW_FILE` (L-D.27); its X records are read
  through `E.x_rec`.
- **L-S (scalper):** defines the fill rules, the limit's snapping direction and the order model in terms of
  `TickGrid` (L-D.23), handing an exact `Decimal` formed under `grid.ctx` where it forms one (T2, the DEEP depth);
  adopts the NO-TRADE rule for zero-volume 5m bars (L-D.16); defines which legs pay `maker_bps_side` and which pay
  taker, reading both from `E.fees()`; prints the on-grid shares and any coarser-month flag of
  `TICK_GRID_AUDIT.json` beside its fill tables (O-27); owns F-TOLL's book half, `F-TOLL [book t1]` … `[book t5]`.
- **L-R (range state):** its conditioned maker twin fills by the tier's one fill rule on
  `TickGrid(E.ticks()[stem])`, the expression formed under `grid.ctx` (L-D.23); it reads frozen-estate SCRIPT text
  by `ast` as an ordinary repo read (L-D.27); its one 5m read goes through `E.D.load_asof` / `E.load_asof_at`.
- **L-C (control):** F-CTRL's TC11-corridor leg rides with the look-back pin of L-D.28 and takes TC11's filed journal
  as its referee through `E.tc11_record`; its rows (the books, the manifest of books) are on `TC11_ALLOW_FILE`.
- **L-X (statistics / registrations / close):** O-9's scored-window bound is the object `E.TC11_PIN_MS`; a
  registration that pins a Stage D record does so under `inputs pinned:`, by certifying record, never as a
  precondition and never by a sha value (the registry is filed before Stage D exists); the scorer's beside leaf
  `licence_at_maker_pin` reads the maker rate from `E.fees()` and the `differs` flag from the fee file's
  `maker_pin`; seeds are passed explicitly; CLOSE carries the manifest's `operator_rulings_needed`, the pin line,
  the mirror status (a `TC12-D.mirror` still PARTIAL is a finding-not-fixed) and every line of
  `DISCLOSURES_BUILD.md` into the report. Its TC11 rows are on `TC11_ALLOW_FILE`.
- **L-G, L-R, L-L, L-V, L-C, L-X — one rule for every reader:** a TC11 record is read only through
  `E.tc11_record(rel)` with `rel` on the list of L-D.27 (a new row is a dated amendment to a hunk); an X record
  only through `E.x_rec(rel)`; a raw open of either is refused. No stage reads a snapshot file outside the 124, and
  no stage lists a TC11 or `x_rec` directory.
- **L-L (ledger / era / ferry):** the ledger's opening instant (CON:109) is the object `E.TC10_PIN_MS` (TC11's pin
  record, key `tc10_pin_close_ms`); "the STEP Q instant" of its row flag is L-D.1's; row files are staged off-bus —
  `exchange/**` is write-never under the shim (reads of it, and of `.git/` objects, are ordinary repo reads), and
  the ferry of record is a close act.

### OBJECTIONS

OBJECTION O-8 — accepted as O-26.

OBJECTION O-20 — accepted as O-27.
