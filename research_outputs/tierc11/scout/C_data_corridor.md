# TC11 SCOUT C: data and the corridor

Scout: subsystem C (data, snapshot, as-of pin, toll, funding). Read-only. Nothing was fetched and no git state was touched.
Contract read in full: `exchange/queue/2026-09-24_TC11_APOLLO.md` (103 lines, STEP Q commit b9ed953, 2026-09-25T00:09:43Z).
Source shas at scout time: `scripts/tierc10_data.py` 2cbf9bb6…, `engine/data.py` ddee4020…, `engine/rangefinder.py` bbae464f…, `analytics/rangefinder_census.py` 19c5507f…, `scripts/tierc2_rules.py` 1739b400….

---

## 0. The most load-bearing facts

1. **You cannot import `tierc10_data` (or any module that imports it) under a TC11 snapshot.** `scripts/tierc10_data.py:94-117` `assert_substrate()` runs at import and HALTs unless `NAIAD_CACHE_DIR` resolves to exactly `~/.cache/naiad/snapshots/tc10_20260921`. The same hard-coded guard is in `tierc10_census.py:68-96`, `tierc10_stamps.py:68-95`, `tierc10_null.py` (through census), `tierc10_close_*`, and in `tierc10_brk.py`, `tierc10_lanes.py` and `tierc10_score.py`, which get it by importing `tierc10_data`. TC10 has **no CLI flag for a different snapshot or pin**: `--out` moves the artifacts only, and `kline_path`/`load_asof` always read `SNAPSHOT`.
2. **The TC10 snapshot is intact and frozen.** 175 of 175 parquet files re-hash equal to `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` (119 in scope, 56 `out_of_scope_snapshot_files`), and no file on disk is missing from the manifest. Do **not** extend it in place: every sha pinned by TC10 would move.
3. **TC11 pin:** `as_of_close_ms = 1790294400000` (2026-09-25T00:00:00Z) and `as_of_open_ms = 1790280000000` (2026-09-24T20:00Z). That is exactly 80 h, or 20 4h bars, past the TC10 pin at 1790006400000 (2026-09-21T16:00Z). It was the latest closed 4h bar when STEP Q was filed.
4. **15m exists for the five home assets**, and for 9 more stems, running to 2026-09-21T16:15Z. It is **out of TC10's scope**: not in PRE_STATE, not scanned, not audited, and listed only by sha in `out_of_scope_snapshot_files`. **1w exists for all 17** (derived from 4h).
5. **The toll is 10 bps round trip, one taker figure** (`tierc2_rules.FEE_BPS_SIDE` = 5.0, ×2). The census turns it into ATR of the lens per event. **No maker fee exists in any code register.** The only estate sources are `README.md:150` ("maker is 0.02%") and the V3 R10 precedent (`V3_Recompute_R1_R10_Builder_Contract.md:155-159`, `scripts/v3_recompute.py:957-966`).
6. **The extension cost is tiny.** About 90 REST calls give 5m +954 or +960 per asset, 15m +318 (home five), 1h +80, 4h +20, 12h +7, derived 1d +4, 1w +0, and funding +10 prints (8h assets) or +20 (4h assets). That is under 1 minute and roughly 900 of Binance's 2400 weight/min. TC10's whole fetch took 11 min 5 s, most of it three full-history 5m tapes.

---

## 1. Modules and import hazards

| Name | Module | Notes |
|---|---|---|
| `ED` | `engine/data.py` (`from engine import data as ED`, as at `tierc10_data.py:126`) | `cache_dir()` (`engine/data.py:39-48`) reads `NAIAD_CACHE_DIR` **on every call** and **`mkdir`s it** (`:47`). A typo'd env var silently creates an empty cache. Guard that `klines/` exists, as TC10 does at `tierc10_data.py:112`. |
| `TB` | `scripts/tierc2_baseline.py` | `KLINES = cache_dir()/"klines"` and `FUNDING = cache_dir()/"funding"` are **bound at import** (`:205-206`). Export the env var **before python starts**. `tierc10_panel.substrate()` (`tierc10_panel.py:161-193`) proves the binding. |
| `TP` | `scripts/tierc10_panel.py` | Has **no** hard-coded snapshot; it refuses only the live cache and a binding mismatch. **But** `AS_OF_PIN = OUT/"data"/"AS_OF_PIN.json"` (`:240`, with OUT = `research_outputs/tierc10`), and `stage_d_pin()` (`:634-647`) **caps every corridor at the TC10 pin** (`corridor_n` `:685-689`). Under a TC11 snapshot you must repoint `TP.AS_OF_PIN` at the TC11 pin. Otherwise the corridor silently ends at 2026-09-21T16:00Z, and the `pin_close_iso` argument can only look back. |
| `R2` | `scripts/tierc2_rules.py` | `UNIVERSE` (`:56-60`, `:111`), `TIDE_SLOW` = 316 (`:67`), `FEE_BPS_SIDE` = 5.0 (`:87-92`, `:122`), `FEE_BPS_ROUND_TRIP` = 10.0 (`:123`). Pure, and safe to import. |
| `engine.cells` | `engine/cells.py` | `INTERVAL_MS` (`:9-16`) **includes `"15m": 900_000`**, so `ED._fetch_rest_klines(sym,"15m",…)` works. `SLIPPAGE_TIER_BPS` = {A:2, B:5, C:10} (`:24`). |
| `analytics/rangefinder_census.py` | the twin | No substrate guard; imports only numpy and stdlib. Safe under a TC11 env. |

**Gitignore hazard (for the read-only worktrees):** `.gitignore:263` `research_outputs/tierc10/**`. Every Stage D artifact (`AS_OF_PIN.json`, `STAGE_D_MANIFEST.json`, `FETCH_LOG.jsonl`, `PRE_STATE.json`, `fee_schedule.json`, `CONTRACT_SPECS.json`) and every census parquet is **untracked**. Only 59 force-added files are tracked. A fresh worktree has **none** of them, so read TC10 records by absolute path from the main tree. `research_outputs/tierc11/**` is currently **not** ignored: TC11 data artifacts will be tracked unless a rule is added.

---

## 2. How TC10 pinned the as-of and sealed provenance

### 2a. The pin: `pin_as_of(out) -> dict` (`tierc10_data.py:472-517`)
- It is write-once. If `out/AS_OF_PIN.json` exists, it is re-read and nothing is re-pinned (`:479-484`).
- It reads **the venue clock**: `GET fapi /fapi/v1/time` → `serverTime` (`:485`).
- `open_ms = (server_ms // MS_4H) * MS_4H - MS_4H`, the last **closed** 4h bar (`:487`).
- It proves the bar is closed with the venue's own closeTime: `GET /fapi/v1/klines BTCUSDT 4h startTime=endTime=open_ms limit=1`. It HALTs if the bar is absent or if `closeTime >= serverTime` (`:488-497`).
- It writes through `_dump_once` (`:448-454`, which HALTs if the file exists; atomic tmp + `os.replace` in `_dump` `:440-445`).
- Reader: `load_pin(out=None)` (`:520-524`), which HALTs if the file is missing.

Filed TC10 pin (`research_outputs/tierc10/data/AS_OF_PIN.json`, sha 0a78ae69…, 604 bytes):
```
as_of_last_closed_4h_open_ms 1789992000000   as_of_last_closed_4h_open  2026-09-21T12:00:00Z
as_of_last_closed_4h_close_ms 1790006400000  as_of_last_closed_4h       2026-09-21T16:00:00Z
venue_server_time_ms 1790015178724  venue_close_time_of_pinned_bar_ms 1790006399999
local_clock_skew_ms -54  pinned_wall_clock_utc 2026-09-21T18:26:18Z  seed 20260921  law "..."
```
The as-of cut used everywhere is `open_time + STEP_MS[iv] <= as_of_close_ms` (`load_asof` `:2786-2794`). Funding is cut on `funding_hour_ms <= as_of_close_ms` (`load_funding_asof` `:2810-2825`).

### 2b. Provenance chain
| Artifact | Writer | Law |
|---|---|---|
| `VENUE_PROBE.json` | `probe_venues(out,pin)` `:549-637` | Write-once. KEEP rule: PERPETUAL, TRADING, quote USDT, and baseAsset equal to the expected base. Bybit only when Binance has no symbol at all. |
| `PRE_STATE.json` | `write_pre_state(assets,pin,out)` `:817-852` | Write-once. Per pre-existing in-scope file: `file_sha256, rows, first_ms, last_ms, content_sha` (`frame_sha` `:428-437`: raw LE column bytes, so it does not move with the parquet writer). Scope = `NATIVE_IVS` only (5m,1h,4h,12h) + funding. **It never listed 15m, 1d or 1w.** TC10 has 54 entries. |
| `FETCH_LOG.jsonl` | `_fetch_log(out,row)` `:683-686` | Append-only. Row keys: `wall_clock_utc, kind(klines/funding/contract_specs), stem, iv, venue, from, to, bars` (funding rows carry `old_edge, new_edge`). |
| `verify_prefixes(pre, root=None)` | `:855-875` | For each pre-existing file, the rows with `t <= old last_ms` read back from the current file must hash to the old `content_sha`. This is the no-rewrite proof. |
| `WRITE_ONCE_SEAL.json` | `seal_provenance(out)` `:888-926` (CLI `--seal`) | Pins the sha and bytes of `AS_OF_PIN.json, VENUE_PROBE.json, PRE_STATE.json` (`SEALED_FILES` `:880`) and the fetch log's **line prefix**: `sealed_lines` 96, `sha256_of_sealed_lines` 5f453b97…. The disclosure notes that VENUE_PROBE and PRE_STATE were re-stamped once after the fetch [LEAN D-h, `:329-337`]. Checked by `verify_seal(out,root)` `:929-952`. |
| `CONTRACT_SPECS.json` | `capture_contract_specs(out,pin)` `:1210-1313` (CLI `--contract-specs`) | Write-once, but **not in the seal**. The manifest's `contract_multipliers.artifact_sha256` pins it instead. |
| `STAGE_D_MANIFEST.json/.md`, `fee_schedule.json`, `DATA_SPEND_AUDIT.json` | `run()` `:2829-2937` | Re-writable (`_dump`). The manifest has `files[]` rows (keys below), `panels`, `admission`, `venues`, `as_of_hazards`, `out_of_scope_snapshot_files`, `prefix_attestation`, `write_once`, `tiered_costs_haircut_twin`, and more. |

Manifest `files[]` row keys (klines): `path, stem, asset, venue, kind, as_of_lens, native, present, rows, rows_as_of, rows_after_as_of, first_open(_ms), last_open(_ms), as_of_last_closed_bar_open/close, complete_to_as_of, gap_count, gaps, missing_bars_total, duplicates, backward, off_grid, non_finite, ohlc_incoherent, venue_zero_volume_bars, venue_flat_bars, venue_zero_volume_flat_bars, sha256, bytes, listing, source, publication{carries, differs_from_rest_bars, differs_from_archive_bars, rest_basis, archive_lacks_bars}`. The scan comes from `scan_klines(df, iv, as_of_close_ms)` `:1013-1043` and `scan_funding(df, as_of_close_ms)` `:1046-1074`.

---

## 3. The snapshot: `~/.cache/naiad/snapshots/tc10_20260921`

Layout: `MANIFEST.json` (12K; the estate backup manifest from 2026-08-12 on Windows, 73 files; inert) · `klines/{STEM}_{iv}.parquet` (154 files) · `funding/{STEM}.parquet` (21 files).
**Sizes (du):** total **817M**: klines 816M, funding 1.5M. By interval: `*_1m` **461M** (10 files, out of scope, end 2026-08-15) · `*_5m` 231M · `*_15m` 84M · `{1h,4h,12h,1d,1w}` 40M. **The 17 panel stems × {5m,15m,1h,4h,12h,1d,1w} = 317M.** The volume is APFS (`/System/Volumes/Data`), with 1.7 TiB free.

**Parquet schemas (every file checked):**
- klines: `open_time:int64` (ms UTC, bar OPEN), `open, high, low, close, volume: double`. No close_time and no index. Sorted ascending after `ED._save_cache`. `ED.KLINE_COLS` (`engine/data.py:36`).
- funding: `funding_time:int64` (raw venue stamp in ms, 0-47 ms past the hour), `funding_rate: double`. `ED.FUNDING_COLS` (`engine/data.py:189`).

**Inventory for the 17 panel stems.** The table gives first open and rows per interval. The last open is the same across the panel unless noted: **5m 2026-09-21T16:25Z** (6 rows after the TC10 as-of; PUMP/SUI/MNT end **15:55Z**, 0 after) · **15m 16:15Z** (2 after) · **1h 15:00Z** · **4h 12:00Z** · **12h 2026-09-21T00:00Z** · **1d 2026-09-20** · **1w 2026-09-14** (Monday-anchored). Gaps = 0 on every panel file (native and derived).

| stem | 5m rows / first | 15m | 1h | 4h | 12h | 1d | 1w |
|---|---|---|---|---|---|---|---|
| BTCUSDT | 740,143 / 2019-09-08T17:55 | 246,715 / 2019-09-08T17:45 | 61,679 | 15,420 / 2019-09-08T16:00 | 5,140 | 2,569 | 367 |
| ETHUSDT | 717,225 / 2019-11-27T07:45 | 239,075 | 59,769 | 14,943 | 4,981 | 2,489 | 355 |
| SOLUSDT | 633,138 / 2020-09-14T07:00 | 211,046 | 52,761 | 13,191 | 4,397 | 2,197 | 313 |
| NEARUSDT | 624,198 / 2020-10-15T08:00 | 208,066 | 52,016 | 13,004 | 4,335 | 2,166 | 309 |
| ZECUSDT | 697,062 / 2020-02-05T08:00 | 232,354 | 58,088 | 14,522 | 4,841 | 2,419 | 345 |
| ENAUSDT | 259,824 / 2024-04-02T12:30 | 86,608 | 21,652 | 5,413 | 1,804 | 901 | 128 |
| PUMPUSDT | 126,246 / 2025-07-10T07:30 | **absent** | 10,521 | 2,631 | 877 | 437 | 62 |
| HYPEUSDT | 138,024 / 2025-05-30T10:30 | 46,008 | 11,502 | 2,876 | 959 | 478 | 68 |
| MNTUSDT_BYBIT | 312,593 / 2023-10-02T06:35 | **absent** | 26,050 | 6,513 | 2,171 | 1,084 | 154 |
| SUIUSDT | 356,256 / 2023-05-03T16:00 | **absent** | 29,688 | 7,422 | 2,474 | 1,236 | 176 |
| LTCUSDT | 704,837 | 234,946 | 58,736 | 14,684 | 4,895 | 2,446 | 349 |
| XMRUSDT | 697,638 | 232,546 | 58,136 | 14,534 | 4,845 | 2,421 | 345 |
| BNBUSDT | 695,622 | 231,874 | 57,968 | 14,492 | 4,831 | 2,414 | 344 |
| UNIUSDT | 631,986 | 210,662 | 52,665 | 13,167 | 4,389 | 2,193 | 313 |
| 1000PEPEUSDT | 355,680 | 118,560 | 29,640 | 7,410 | 2,470 | 1,234 | 176 |
| DOGEUSDT | 652,122 | 217,374 | 54,343 | 13,586 | 4,529 | 2,263 | 323 |
| 1000BONKUSDT | 297,822 | 99,274 | 24,818 | 6,205 | 2,068 | 1,033 | 147 |

Non-panel files, out of scope: FARTCOIN, JTO, TAO, LIT (some stale at 2026-08-15 or 2026-09-19), USELESS, XPL; `*_1m` for BTC, ETH, SOL, NEAR, ZEC, HYPE, FARTCOIN, JTO, TAO, LIT.

**15m provenance (measured here).** The files carry mtime 2026-09-21T16:31Z, before the TC10 pin at 18:26Z; they were copied in from the live cache. I compared them with 3×5m aggregates over the home five, bars closed at or before the TC10 as-of:

| | BTC | ETH | SOL | NEAR | ZEC |
|---|---|---|---|---|---|
| price mismatches | 10 | 11 | 5 | 8 | 14 |
| volume-only mismatches | 3 | 5 | 3 | 3 | 3 |
| total compared | 246,712 | 239,073 | 211,044 | 208,064 | 232,352 |

BTC also has one 15m bar with no complete 5m triple. These are the venue's incident-bar disagreements between intervals, not corruption. TC10's derivation law never aggregates across native intervals (`STAGE_D_MANIFEST.derivation`).

---

## 4. Native vs derived intervals

- `NATIVE_IVS = ("5m","1h","4h","12h")` `tierc10_data.py:202`, fetched venue-native.
- `DERIVED_IVS = ("1d","1w")` `:203`, derived **from native 4h only** [LEAN L1].
- `STEP_MS` `:204-205` = {5m 300000, 1h 3600000, 4h 14400000, 12h 43200000, 1d 86400000, 1w 604800000}. **It has no `"15m"`**, so `target_last_open("15m",…)`, `_assert_grid`, `scan_klines` and `load_asof` KeyError on 15m.
- `GRID_ANCHOR_MS = {"1w": MONDAY_EPOCH_OFFSET_MS}` `:206`, with `MONDAY_EPOCH_OFFSET_MS = 4*DAY_MS` `:198` (1970-01-05 was a Monday).
- `target_last_open(iv, as_of_close_ms) = ((close - step - anchor)//step)*step + anchor` `:465-468`.
- `derive_1d(f4h) -> (df, dropped)` `:956-970`: a day exists only if all **6** 4h bars exist; the frame is grouped on `open_time // DAY_MS`.
- `derive_1w(d1) -> (df, dropped)` `:973-986`: a week exists only if all **7** complete days exist, Monday-anchored.
- `derive_lenses(stem,pin)` `:998-1009`: cuts 4h to closed bars at or before the as-of, derives both lenses, then `_write_if_changed` (`:989-995`) rewrites the whole derived file only when its `frame_sha` changed.
- The census has its own copy of the law: `LENS_SOURCE = {"5m":"5m","4h":"4h","1d":"4h"}` `tierc10_census.py:119`, `load_tape` `:574-640` (it HALTs if its 1d differs from Stage D's file). **Census `LENSES = ("5m","4h","1d")` `:117`; no 15m, 1h, 12h or 1w lens exists in the TC10 census.**
- BRK: `LENS_MS = dict(D.STEP_MS)` `tierc10_brk.py:137`, with no 15m.

**What TC11 needs against what exists (at the TC10 pin):**

| lens | home five | twelve new | TC10 census R2 measured? |
|---|---|---|---|
| 5m | present | present (all 12) | yes |
| 15m | present but out of scope and unaudited | only 9 of 12 (no PUMP, MNT, SUI); not needed | **no** |
| 1h | present | present | **no** |
| 4h | present | present | yes |
| 12h | present | present | **no** |
| 1d | derived | derived | yes |
| 1w | derived, **309-367 bars** | derived, 62-349 bars | **no** |

At the TC11 pin, 1d gains 4 days (09-21..09-24). 1w gains **0**: the week of 2026-09-21 is incomplete at 2026-09-25T00:00Z (a Friday).

---

## 5. Asset lists

- **CLASSIC5 (the "five home assets")** = `tuple(R2.UNIVERSE)` = (BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT). Sources: `tierc10_data.py:260`, `tierc2_rules.py:56-60`, and `tierc10_panel.py` `CLASSIC5 = RC.UNIVERSE` (asserted equal).
- **UNSEEN12** (`tierc10_data.py:262-269`), as (contract name, symbol, baseAsset): ENA/ENAUSDT · PUMPFUN/**PUMPUSDT** (PUMPBTCUSDT rejected by name, LEAN D-d) · HYPE/HYPEUSDT · **MNT/MNTUSDT → stem `MNTUSDT_BYBIT`** · SUI · LTC · XMR · BNB · UNI · PEPE/**1000PEPEUSDT** · DOGE · BONK/**1000BONKUSDT**. The panel module has an equivalent list at `tierc10_panel.py:218-231`.
- **PANEL17** = `STAGE_D_MANIFEST.panels.PANEL17_stems` (the 5 above plus ENAUSDT, PUMPUSDT, HYPEUSDT, MNTUSDT_BYBIT, SUIUSDT, LTCUSDT, XMRUSDT, BNBUSDT, UNIUSDT, 1000PEPEUSDT, DOGEUSDT, 1000BONKUSDT). Reader: `panel(out)` `:2779-2783`. All 17 were admitted under the rule of at least `ADMISSION_MIN_4H = TIDE_SLOW + MEM_TTL_BARS = 316 + 400 = 716` closed 4h bars (`:209-210`; MEM_TTL read by AST from `engine/rangefinder.py:589` PINS_V2). The tightest is PUMP at 2,631.
- **The MNT exception:** `ALT_VENUE_ASSETS = ("MNT",)` `:270`, `BYBIT_STEM_SUFFIX="_BYBIT"` `:271`. The whole tape (klines and funding) is Bybit v5 linear (`BYBIT_BASE` `:273`, `BYBIT_IV = {"5m":"5","1h":"60","4h":"240","12h":"720"}` `:274`, **no 15m**, `BYBIT_PAGE=1000`, `BYBIT_FUNDING_PAGE=200`). It is never spliced. The fee is the estate's flat Binance figure, marked as an ASSUMPTION. Operator nod pending (`OPERATOR_RULINGS` in the manifest). Operator ruling R5, "The USDT pair, either on Binance or Bybit", covers it.
- **Contract multipliers** (`CONTRACT_SPECS.json`): 1000PEPEUSDT and 1000BONKUSDT are ×1000 and every price is per 1000 tokens; the other 15 are ×1. Ratios in ATR or R are invariant (`NORMALIZATION_LAW` `:1191-1207`). `multiplier_of(stem)` `:1321`.
- **Data-spend classes** (`DATA_SPEND_AUDIT.json`): scored = BTC ETH SOL NEAR ZEC · display-only = ENA HYPE LTC XMR BNB UNI PEPE DOGE BONK · **never-touched = PUMPFUN MNT SUI**.

---

## 6. The TOLL model

| Item | Value | Source |
|---|---|---|
| Taker fee per side | **5.0 bps** | `tierc2_rules.py:87-92,122` ← `configs/naiad_v0.yaml:58 fee_bps_side: 5.0` ← charter `Naiad_Phase0_Charter.md:112` |
| TC-series round trip (the accounting figure of record) | **10.0 bps** | `tierc2_rules.py:123` `FEE_BPS_ROUND_TRIP`. Filed per asset as `fee_schedule.json[].round_trip_bps_used` (all 17 = 10.0) |
| Fee law | `fee_px = (FEE_BPS_SIDE/1e4)*(entry_px+exit_px)`; `fee_r = fee_px / r_dist` | `tierc2_baseline.py:333-339`, `tierc10_brk.account_l` `:1270-1325` |
| Charter slippage per side | tier A {BTC ETH} 2 · tier B {SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR} 5 · tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10 bps | Charter line `Naiad_Phase0_Charter.md:114` (ratification basket). Extended to 17 by the TC10 clause `tierc10_data.py:217-220`, parsed by `parse_slippage_clause` `:226-243`. `engine/cells.py:24` |
| Charter "haircut twin" round trip | A **14**, B **20**, C **30** bps (= 2×(5+slip)) | `charter_round_trip_bps(asset)` `:1391`; `haircut_twin_net_r(asset, gross_r, entry_px, exit_px, risk_px) -> dict` `:1408-1441` (returns `net_r_twin` and carries `tc_series_round_trip_bps_used` untouched); `haircut_twin_for_stem` `:1444` |
| **Maker fee** | **2 bps/side (0.02%, Binance VIP0)**, **documentation only** | `README.md:150` ("maker is 0.02% but the engine books every fill as taker"); V3 R10 "maker entries 2 bps/side, taker stops 5 bps/side … entry slippage removed", `V3_Recompute_R1_R10_Builder_Contract.md:155-159`, `scripts/v3_recompute.py:957-966`, `recompute.json:265-268`. **No register, config or `tierc*` constant.** Bybit maker for MNT: not in repo. |
| Toll in lens units (census) | `toll_atr_evt = (bps/10_000) * close[k] / ATR14_lens[k]` per event, and the median per row. **The same bps on every lens; the ATR makes it lens-specific.** | `tierc10_census.py:1373` (outcome), `height_rows` `:2636-2656` (`toll_atr = (bps/1e4)*close_at_confirm/atr_at_confirm`; `ratio = height_atr/toll_atr`; the ATR cancels). `toll_bps_for(stem)` `:510-521` reads `fee_schedule.json` |
| R2 gate constants [Q-R3] | `HEIGHT_CAPTURE_FRAC=2/3`, `HEIGHT_RATIO_MIN=3.0`, `INFEASIBLE_MAX_SHARE=0.10`, `HEIGHT_MIN_N_RANGES = EDGE_MIN_N_RANGES = EDGE_MIN_N_BARS = PROVISIONAL_MIN_N = 30`, `EDGE_NEAR_FRAC=0.2`; verdict = height gate AND edge-fade H20 net > 0, judged **within an era** | `tierc10_census.py:2153-2168`, `HEIGHT_GATE_LAW` `:2186-2254` (sha-pinned `:2255`), reader `height_vs_toll_verdict(lens, root, asset, scale_kind, era, allow_provisional)` `:3005` |
| Eras | tuning ≤ 2024-06-30T23:59:59Z (1719791999000); holdout after that | `tierc10_census.py:164-169`; `tierc10_panel.py` `ERA_CUT_ISO` |
| Funding ceiling | the card's `funding_ceiling_r` (D12, 1R) on the campaign total, only when funding is a cost | `tierc10_brk.account_l` `:1318-1321` |

TC10 reference numbers (frozen3.0, era ALL): 5m pooled CLASSIC5 toll median 0.293 ATR, height 6.48 ATR, ratio 23.3 (the height gate passes; the edge-fade leg fails) · 4h toll 0.039 ATR, ratio 169 · 1d toll 0.017 ATR, ratio 414. In TC10 the **edge-fade leg** is what fails. Filed at `research_outputs/tierc10/census/height_toll_verdict.parquet` (5m, 4h, 1d only).

---

## 7. Building the TC11 snapshot at as_of_close_ms 1790294400000, without touching the live cache

**Where TC10 stands:** its CLI (`main` `:2940-2979`: `--offline --out --audit-rest --audit-archive --probe-archive-forms --audit-stems --audit-merge --seal --contract-specs`) **cannot target another snapshot or pin.** The functions below are the ones to reuse by **copying them into `scripts/tierc11_data.py`**, because importing them HALTs.

Pure, and safe to copy verbatim: `frame_sha` `:428`, `file_sha256` `:420`, `_dump`/`_dump_once` `:440/448`, `target_last_open` `:465`, `_retry` `:656`, `binance_brake` `:670`, `_edge` `:689`, `_assert_grid` `:696`, `bybit_klines` `:703`, `bybit_funding` `:727`, `derive_1d`/`derive_1w` `:956/973`, `_write_if_changed` `:989`, `scan_klines` `:1013`, `scan_funding` `:1046`, `with_funding_hour` `:2797`. `extend_klines` `:754`, `extend_funding` `:797`, `write_pre_state` `:817`, `verify_prefixes` `:855` and `seal_provenance`/`verify_seal` `:888/929` also carry over once `SNAPSHOT`/`OUT` point at TC11 and `"15m"` is in `STEP_MS`. Suggested: an AST-equality fixture per copied function against `tierc10_data.py`, following the rangefinder_core equivalence precedent.

**Steps:**
```bash
SRC=~/.cache/naiad/snapshots/tc10_20260921
DST=~/.cache/naiad/snapshots/tc11_20260925          # name is a lean
cp -cpR "$SRC" "$DST"          # APFS clonefile: instant, no extra bytes until a file is replaced
# optional: rm "$DST"/klines/*_1m.parquet (461M, out of scope in TC10 and in TC11)
export NAIAD_CACHE_DIR=$DST PYTHONDONTWRITEBYTECODE=1   # BEFORE python starts (TB binds at import)
~/venvs/naiad/bin/python scripts/tierc11_data.py        # the new module
```
Then, inside `tierc11_data.py`:
1. **Guard** (a copy of `assert_substrate`). The env var must resolve to DST, not to `LIVE_CACHE`, and **not to `TC10 SNAPSHOT`**; `klines/` must exist.
2. **Chain of custody:** re-hash every DST file against TC10 `STAGE_D_MANIFEST.json` (`files[].sha256` + `out_of_scope_snapshot_files[].sha256`). Today that is 175/175.
3. **Pin** (write-once, `research_outputs/tierc11/data/AS_OF_PIN.json`, seed 20260924). Same keys as TC10; `open_ms = 1790280000000`, `close_ms = 1790294400000`. Venue-proven: `/fapi/v1/klines BTCUSDT 4h` at that open, `closeTime (…4399999) < serverTime`. Print the "latest closed at run start" beside it (see Ambiguity A1).
4. **PRE_STATE** (write-once) over **every** in-scope file: 17 × {5m,1h,4h,12h,1d,1w}, CLASSIC5 × 15m, and 17 funding files, 124 in all. Carry each file's TC10 manifest sha beside `file_sha256`.
5. **Venue:** re-read TC10 `VENUE_PROBE.json` by sha (the venue of record was decided once). Optionally re-probe only to assert that all 17 are still TRADING.
6. **Extend** with REST only (as TC10 did). For a Binance stem, `ED._fetch_rest_klines(sym, iv, edge+step, target_last_open(iv, 1790294400000))`. For MNT, `bybit_klines("MNTUSDT", iv, …)`. Filter to [lo, hi], run `_assert_grid`, then `ED._save_cache(stem, iv, df[KLINE_COLS])`. That call merges, does not shrink, uses tmp + `os.replace`, and **new rows win at an identical open_time**, which is why you must start at `edge + step`. Log each chunk to `FETCH_LOG.jsonl`.

   | lens | new bars per asset | first new open → target last open |
   |---|---|---|
   | 5m | 954 (14 Binance) / 960 (PUMP, SUI, MNT) | 16:30Z or 16:00Z 09-21 → 23:55Z 09-24 |
   | 15m (home five) | 318 | 16:30Z 09-21 → 23:45Z 09-24 |
   | 1h | 80 | 16:00Z 09-21 → 23:00Z 09-24 |
   | 4h | 20 | 16:00Z 09-21 → 20:00Z 09-24 |
   | 12h | 7 | 12:00Z 09-21 → 12:00Z 09-24 |

   Each is one REST page (limit 1500, weight 10). About 73 kline calls in all.
7. **Funding:** Binance `ED.backfill_funding(sym, start_ms, pin_close + 60_000, log=None)` resumes from the file max + 1. Bybit `bybit_funding("MNTUSDT", old+1, end)` then `ED._save_funding(stem, df)`. `FUNDING_JITTER_MS = 60_000` `:208`, [LEAN D-b].
8. **Derive** 1d/1w from the extended 4h (`derive_1d`/`derive_1w`/`_write_if_changed`).
9. **Scan, attest and file:** `verify_prefixes(PRE_STATE)` must be all OK (this is the no-rewrite proof, and it covers the derived and 15m files too). Then scan every file, file the manifest and fee schedule (with the maker row, see Gap G4), and `--seal`.

**TC10 timing (FETCH_LOG, 96 sealed lines):** 2026-09-21T18:26:22Z → 18:37:27Z, **11 min 05 s**.

| kind | wall time | bars | assets |
|---|---|---|---|
| 4h | 11 s | 16,566 | 3 full-history |
| 12h | 34 s | 35,797 | 17 |
| 1h | 44 s | 66,259 | 3 full |
| funding | 72 s | n/a | 17 |
| 5m | **504 s** | 795,095 | 3 full: PUMP, MNT, SUI |

Throughput: Binance 5m about 2,240 bars/s (SUI 356,256 in 159 s, 15,000-bar chunks every ~6.5 s). Bybit 5m about 1,090 bars/s (MNT 312,593 in 287 s). `contract_specs` was one extra line on 2026-09-22T13:11:55Z. The 14 other assets' 5m and 15m were **pre-existing** (copied in from the live cache).

**Rate limits in code:** `WEIGHT_SOFT_CAP = 1200` of Binance's 2400/min (`:279`, braked through the `x-mbx-used-weight-1m` header from a `/fapi/v1/ping`) · `CHUNK_BARS = 15_000` (`:278`) · `RETRIES = 6` with 20 s×attempt backoff (`_retry`) · `ED._get` 4 retries at 1.5 s×attempt, 60 s timeout, and treats 404 as a return (`engine/data.py:63-74`) · a 0.15 s sleep per Binance page (`:127`) and 0.12 s per Bybit page · Bybit sleeps 2 s when `X-Bapi-Limit-Status < 20`.

**REST or bulk archive:** TC10 fetched **REST only**. The bulk archive (`ED.BULK_BASE = data.binance.vision/data/futures/um`, `_fetch_bulk_zip` `engine/data.py:96-104`, `backfill_klines` `:231-302`) was used only by the estate's older live-cache assembly and by the read-only audits. The two publications disagree on incident bars, and the classics were **measured** to carry REST (F-D-1 is designed RED). The operator's R5 does not choose between them. Recommended for TC11: REST, for continuity with TC10's REST tails. The archive's daily zips also lag, and the monthly zip does not exist for the running month.

**The live cache:** never set `NAIAD_CACHE_DIR` to it and never copy from it (a separate lane writes it; `scripts/oracle_roster_backfill.py:75` refuses a scoped env). Everything above writes only DST and `research_outputs/tierc11/data/`.

---

## 8. Funding

- Files: `funding/{stem}.parquet` for all 17, through 2026-09-21T16:00Z (the print stamped a few ms past 16:00 belongs to the AS_OF hour, [LEAN D-g] `:319-328`).
- Rows: BTC 7,706 · ETH 7,472 · SOL 6,671 · NEAR 6,503 · ZEC 7,262 · MNT 3,258 · PUMP 2,630 · HYPE 2,875 · SUI 3,712.
- Cadence, observed (`fee_schedule.json`): 8h for most assets. 4h for ENA, PUMP, HYPE, BONK. SOL's histogram is {2h: 98, 4h: 3, 8h: 6,569}. MNT is 8h (Bybit `fundingInterval` 480).
- Venue endpoints: Binance `/fapi/v1/fundingRate` at 1000 per page (`ED.backfill_funding` `engine/data.py:349-382`). Bybit `/v5/market/funding/history` at 200 per page, paged backward (`bybit_funding` `:727-751`).
- As-of reader: `load_funding_asof(stem)` `:2810-2825` returns `funding_time, funding_rate, funding_hour_ms`, cut at `funding_hour_ms <= as_of_close_ms`. It HALTs on a missing or empty file (unlike `tierc2_baseline.load_funding`, which returns `{}` `:216-233`). `with_funding_hour` `:2797` HALTs if a stamp sits more than 60 s past its hour.
- Accounting law: the interval sum over `entry_ms < funding_hour_ms <= exit_ms`, priced at the close of the last lens bar closed at or before the stamp. `amount = Σ rate*close*d*qty`, accumulated in ascending order (for exact F-CTRL parity). See `tierc10_brk.funding_interval` `:1223-1268`, `_funding_arrays` `:908-917`, and the ceiling in `account_l`. The lineage v6 uses a per-bar-open lookup (`tierc2_baseline.py:336-339`).
- The coverage check is `funding_coverage(stem, as_of_close_ms, root)` `:1077-1095`: the last stamp must be no older than the kline edge minus one observed interval.

---

## 9. Calling this from a new tierc11 script

```python
# run:  export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1
#       ~/venvs/naiad/bin/python scripts/tierc11_<x>.py
import os, sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "scripts")]
import tierc11_data as D11        # its import-time guard runs FIRST (the TC10 pattern, TC11 paths)
# NEVER: import tierc10_data / tierc10_census / tierc10_stamps / tierc10_brk / tierc10_lanes / tierc10_score (HALT)
import tierc10_panel as TP        # ok under TC11 env, BUT repoint its pin before any corridor call:
TP.AS_OF_PIN = D11.OUT / "AS_OF_PIN.json"      # else corridor_n caps at the TC10 pin (tierc10_panel.py:685)
import tierc2_rules as R2         # FEE_BPS_SIDE 5.0, FEE_BPS_ROUND_TRIP 10.0, UNIVERSE, TIDE_SLOW 316

CLOSE = D11.load_pin()["as_of_last_closed_4h_close_ms"]      # 1790294400000
for stem in R2.UNIVERSE:
    for iv in ("5m", "15m", "1h", "4h", "12h", "1d", "1w"):
        k = D11.load_asof(stem, iv)     # cols open_time,open,high,low,close,volume; open_time+STEP_MS[iv] <= CLOSE
    fu = D11.load_funding_asof(stem)    # + funding_hour_ms; cut funding_hour_ms <= CLOSE
# twin (no guard, safe):  from analytics import rangefinder_census as RC
# toll in lens ATR:       toll_atr = (R2.FEE_BPS_ROUND_TRIP / 1e4) * close / atr_lens
# charter twin:           D11.haircut_twin_net_r(asset_name, gross_r, entry_px, exit_px, risk_px)  (copied from tierc10_data:1408)
```
Minimum `tierc11_data.py` constants: `SNAPSHOT`, `TC10_SNAPSHOT` (a forbidden target), `LIVE_CACHE`, `OUT = research_outputs/tierc11/data`, `SEED = 20260924`, `STEP_MS` = TC10's plus `"15m": 900_000`, `GRID_ANCHOR_MS = {"1w": 4*86_400_000}`, `KLINE_COLS`/`FUNDING_COLS` from `ED`, and `MAKER_BPS_SIDE` with a named source (Gap G4).

---

## 10. GAPS: what the existing code cannot do today

- **G1** No TC10 data, census, stamps or brk module runs on any snapshot but `tc10_20260921` (import-time HALT). TC11 needs its own data module and its own guard.
- **G2** `tierc10_data.STEP_MS` has no 15m (`:204`). `tierc10_census.LENSES/LENS_MS` covers only 5m, 4h and 1d (`:117-118`). `tierc10_brk.LENS_MS` has no 15m. **R1 over {5m,15m,1h,4h,12h,1d,1w} and R2 at 15m, 1h, 12h and 1w have no loader or census path.** STAGE S depends on "R2 must PASS at 1h", and **1h was never measured**.
- **G3** 15m is out of TC10's scope. It has no PRE_STATE row, no scan, no REST or archive audit and no publication label. TC11 must bring it into its own PRE_STATE and scans (and ideally an F-D-1-style venue sample). Bybit `BYBIT_IV` also has no 15m (irrelevant unless MNT 15m is wanted).
- **G4** **No maker fee object exists.** The maker twin (STAGE S, and the R2 "reopening path") needs a new register row: 2.0 bps per side per `README.md:150`, plus a law for which legs are maker (contract: "entry and target only"; stop = taker 5 + tier slippage). The V3 R10 precedent also drops slippage on the maker leg. Bybit's maker rate for MNT is unknown.
- **G5** `tierc10_panel.stage_d_pin()` is hard-wired to the TC10 pin file, so a TC11 corridor needs `TP.AS_OF_PIN` repointed (or a wrapper). `pin_close_iso` can only move the pin backward.
- **G6** TC10 data artifacts are gitignored and untracked (`.gitignore:263`), so a read-only worktree cannot see `AS_OF_PIN`, `STAGE_D_MANIFEST` or the census parquet files.
- **G7** Sample floors make some R2 verdicts FAIL structurally. 1w has about 309-367 bars per home asset; at the 0.75 per 100-bar density that is about 2-3 ranges per asset and about 13 pooled, below `HEIGHT_MIN_N_RANGES = 30`. TC10's 1d pooled CLASSIC5 holdout was already PROVISIONAL. 12h holdout is thin as well.
- **G8** No fill model for "limit fill at the 5m close". The data layer has OHLC only, so whether a maker order at the close fills (for example, the next bar trading through it) is undefined in code.

---

## 11. AMBIGUITIES (the contract's phrases)

- **A1** "Corridor: full water, latest closed 4h bar, one as-of pin." "Latest closed" is relative to run start. 1790294400000 was the latest when STEP Q was filed (00:09:43Z on 09-25), but a build started after 04:00Z would auto-pin 1790308800000. Lean: pin the given value, prove it closed, and print the run-start latest beside it. "Full water" is established by TC5 (`exchange/reports/BUILD_2026-08-16_TIERC5_FULLWATER.md`): whole history from bar 0, with the 316-bar EMA warm-up floor.
- **A2** "R2 … PASS/FAIL printed per lens; a FAIL closes that lens … in this and every later tier." Per asset, or POOLED:CLASSIC5? Which era (TC10 showed verdicts **reverse** between ALL and holdout)? Which scale kind (R1 says "self-calibrated", but TC10's pin of record is frozen3.0)? And does a FAIL caused only by the sample floor (G7) close a lens permanently?
- **A3** "only 1h bars CLOSED before the 4h bar closes" (F-WARN-ASOF) and "1h close precedes the 4h trigger bar" (F-RELAY). The last 1h bar of a 4h window closes at **the same millisecond** as the 4h bar (T+4h). Is "before" `<` or `<=`? This decides whether the 4th 1h bar of the window is visible.
- **A4** "twelve new assets: 1h/4h/1d only, Tier-E" (R1) against R3's nest vector "for each lens L in {1h,4h,12h,1d,1w} … every campaign of every card", with 17-asset Tier-E views in P-BRK-4H and P-SCALP-2. Do the twelve need 12h and 1w ranges for nest stamping? The data exists for all 17; only the run is in question.
- **A5** "maker toll (limit fill at the 5m close, entry and target only)". Is the fill assumed or tested (G8)? Is the maker rate 2 bps (Binance VIP0 per README) for every asset, including Bybit MNT? And is slippage zero on maker legs (the V3 R10 precedent)?
- **A6** "net of L's toll" (R4). Is it the TC-series 10 bps in ATR_L, as in TC10's census, or the charter twin (14, 20 or 30 bps)? TC10 printed the twin beside and never in place of the TC-series figure [VETO "tiers"]. The contract does not name the twin.
- **A7** "the 17-asset view" and "seventeen Tier-E" do not say whether MNT (Bybit, flat Binance taker assumed) and PUMPFUN→PUMPUSDT, both leans awaiting the operator's nod, are included.
