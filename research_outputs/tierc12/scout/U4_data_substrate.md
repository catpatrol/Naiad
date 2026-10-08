# U4 · THE SUBSTRATE (TC12 STAGE D) — scout map

Scouted 2026-10-08T22:40Z–23:20Z, read-only. Contract read verbatim:
`…/scratchpad/tc12/2026-10-08_TC12_APOLLO.md` sha256 `861d6050e80e66995e4f9db2855aaf274d63285249c2549e5a0813582095a7bd`
(same bytes already filed at `/Users/luis/Naiad/exchange/queue/2026-10-08_TC12_APOLLO.md`, STEP Q commit `28e006b`,
committer time 2026-10-08T22:52:13Z = unix 1791499933).

Abbreviations: **M** = `/Users/luis/Naiad` (branch `v12-v1-census`, HEAD `28e006b`, 15 commits ahead of origin),
**X** = `/Users/luis/Naiad/.claude/worktrees/tierc11x` (tip `7b24f835…`), **D11** = `M/scripts/tierc11_data.py`,
**D10** = `M/scripts/tierc10_data.py`, **ED** = `M/engine/data.py`, **FX10** = `M/scripts/tierc10_data_fixtures.py`.
Every number below was read from the cited file or measured from the cited parquet in this session.
Network used: 3 of 3 permitted GETs (§1.16). Nothing was written except this file.

---

## 1 · FACTS

### 1.1 The three caches — layout and what lives where

| root | klines files | funding files | intervals present | bytes on disk (`du`) | last write |
|---|---:|---:|---|---|---|
| LIVE `~/.cache/naiad/data_cache` | 104 | 10 | 1m 5m 15m 1h 4h 12h — **no 1d, no 1w** | 798M | 5m/15m/1h/4h: 2026-09-23T17:47–17:50Z · 12h, 1m, funding: 2026-08-15T16:0xZ |
| TC10 `~/.cache/naiad/snapshots/tc10_20260921` | 154 | 21 | 1m 5m 15m 1h 4h 12h 1d 1w | 817M | 2026-09-21T18:37Z |
| TC11 `~/.cache/naiad/snapshots/tc11_20260925` | 154 | 21 | 1m 5m 15m 1h 4h 12h 1d 1w | 818M | 2026-09-25T00:59Z |

- Layout in all three: `<root>/klines/<STEM>_<iv>.parquet`, `<root>/funding/<STEM>.parquet`, `<root>/MANIFEST.json`
  (path builders `D11:448-454`; `ED:51-60`).
- Root `MANIFEST.json` is byte-identical in all three (sha256 `c73fec06e38f2ef9…`, 11589 B): a STALE estate-backup
  manifest (`mode: estate`, `created_utc 2026-08-12T02:42:31Z`, `file_count 73`). No TC loader reads it
  (`D11:2034-2072` describes it as stale).
- **Timeframes per stem (measured by directory listing):**
  - LIVE: BTC ETH SOL NEAR ZEC HYPE FARTCOIN JTO LIT TAO have 1m 5m 15m 1h 4h 12h; BONK PEPE BNB DOGE ENA LTC PUMP UNI
    USELESS XMR XPL have 5m 15m 1h 4h only. **No SUIUSDT, no MNTUSDT_BYBIT at all.** Funding only for
    BTC ETH FARTCOIN HYPE JTO LIT NEAR SOL TAO ZEC.
  - TC10 / TC11 snapshots: all 17 panel stems have 5m 1h 4h 12h 1d 1w; 15m exists for 14 stems (not MNT, PUMP, SUI);
    1m for BTC ETH SOL NEAR ZEC HYPE (+FARTCOIN JTO LIT TAO, out of panel). 21 funding tapes (17 panel + 4 out of panel).
- TC11 snapshot size by class (`M/research_outputs/tierc11/data/STAGE_D_MANIFEST.json`, `files[].bytes`):
  in-scope 124 files = 290,921,304 B (5m 216.9 MB · 15m 35.5 · 1h 25.7 · 4h 7.2 · 12h 2.6 · 1d 1.4 · 1w 0.3 · funding 1.4);
  out-of-scope 52 files = 566,077,090 B, of which the 1m tapes are 482,993,958 B. Five home assets in-scope: 142,999,983 B.
- **Integrity now (re-hashed this session):** TC10 snapshot 175/175 files equal `tierc10/data/STAGE_D_MANIFEST.json`
  (119 in-scope + 56 out-of-scope; `MANIFEST.json` unpinned there); TC11 snapshot 176/176 equal
  `tierc11/data/STAGE_D_MANIFEST.json` (124 + 52). No mismatch, no stray file.

### 1.2 Five home assets — first / last bar per file

**TC11 snapshot (the substrate TC12 extends) — from `tierc11/data/STAGE_D_MANIFEST.json files[]`, re-hashed equal:**

| path | rows | first | last | bytes | sha256 |
|---|---:|---|---|---:|---|
| klines/BTCUSDT_5m.parquet | 741097 | 2019-09-08T17:55:00Z | 2026-09-24T23:55:00Z | 23728395 | 3abf94e4f4a73119b4fd86acf51e47c249368d8f7ed192cc6731aaa3980e568b |
| klines/BTCUSDT_15m.parquet | 247033 | 2019-09-08T17:45:00Z | 2026-09-24T23:45:00Z | 9199731 | 01ebcb00a763e2223838fe1d610d51f7ef4723e0a3e8d7726489037d32ea3f00 |
| klines/BTCUSDT_1h.parquet | 61759 | 2019-09-08T17:00:00Z | 2026-09-24T23:00:00Z | 2646971 | 76ad1c804260a5b57ec663a7550194d21f2e5e7090d574dd183778aa404b3289 |
| klines/BTCUSDT_4h.parquet | 15440 | 2019-09-08T16:00:00Z | 2026-09-24T20:00:00Z | 655618 | 281c3ac3195e5bb8de6b211573f77919bb2af2a342f71162426085f54bf37bfb |
| klines/BTCUSDT_12h.parquet | 5147 | 2019-09-08T12:00:00Z | 2026-09-24T12:00:00Z | 222709 | f2894ed4102a729e332abd205a84b4ba53ea51ff7b475873bfc9c7d8da987e40 |
| klines/BTCUSDT_1d.parquet | 2573 | 2019-09-09T00:00:00Z | 2026-09-24T00:00:00Z | 113547 | 334342841fb5322d02f3eea734dd1823a07cc5236186d3d287cb14e5e24fdd59 |
| klines/BTCUSDT_1w.parquet | 367 | 2019-09-09T00:00:00Z | 2026-09-14T00:00:00Z | 19809 | 5844aa75b0253f7be3b71d544c8bea28d3d73273ef289b2c7e7f186565fe2e1c |
| funding/BTCUSDT.parquet | 7716 | 2019-09-10T08:00:00Z | 2026-09-25T00:00:00Z | 112007 | a3d21e1f1a78930b9ca27132d4973f4f4cd4d3ab0639d33d949f25ad8722a77b |
| klines/ETHUSDT_5m.parquet | 718179 | 2019-11-27T07:45:00Z | 2026-09-24T23:55:00Z | 21685930 | 51b8c64fadee80ad6a31dcd857e8f3fbb7da81b17ca70eb31205c63aa26395bf |
| klines/ETHUSDT_15m.parquet | 239393 | 2019-11-27T07:45:00Z | 2026-09-24T23:45:00Z | 8381323 | 1b6fcff8cb98e83b109811c9327fa3e2ead3a761d3306be3179140f743939ba1 |
| klines/ETHUSDT_1h.parquet | 59849 | 2019-11-27T07:00:00Z | 2026-09-24T23:00:00Z | 2410267 | d447f0ef5784ed610d7f32ca632a3a27ffaca42dd3f08a08c9528982b6abe3c7 |
| klines/ETHUSDT_4h.parquet | 14963 | 2019-11-27T04:00:00Z | 2026-09-24T20:00:00Z | 614983 | e78895774de7d30ae06528060d97896a846975e26e1ceb7bdc6245ef70993fab |
| klines/ETHUSDT_12h.parquet | 4988 | 2019-11-27T00:00:00Z | 2026-09-24T12:00:00Z | 211113 | d67e030dacfdc7d1518757f583f8c8176a16c924e949183ac1b7fa48be484d20 |
| klines/ETHUSDT_1d.parquet | 2493 | 2019-11-28T00:00:00Z | 2026-09-24T00:00:00Z | 107691 | cc79c384a03d25f26ed21e155a5c744a0b2a8ae9233b64de95152bcf9f0dfb4f |
| klines/ETHUSDT_1w.parquet | 355 | 2019-12-02T00:00:00Z | 2026-09-14T00:00:00Z | 18777 | 6da90fe87b32349cda942bf8f58619e778cf3883e07c76182a6419e1bab1fcba |
| funding/ETHUSDT.parquet | 7482 | 2019-11-27T08:00:00Z | 2026-09-25T00:00:00Z | 109487 | 31120f82bd515bf664acedacfa86cb0867d309686c2db508f4977edf981767ed |
| klines/SOLUSDT_5m.parquet | 634092 | 2020-09-14T07:00:00Z | 2026-09-24T23:55:00Z | 17315434 | 434908bb2c5e40f627df3f7ddcedff94f154d918ace09ce099e1f40c9b0e1d86 |
| klines/SOLUSDT_15m.parquet | 211364 | 2020-09-14T07:00:00Z | 2026-09-24T23:45:00Z | 6437999 | 91e98de739305c405720fe4b4857071ead0fbc095c49011858f40b035c60cd7f |
| klines/SOLUSDT_1h.parquet | 52841 | 2020-09-14T07:00:00Z | 2026-09-24T23:00:00Z | 1945962 | 1629d318a6e7424a9a68b600f9ffc3ddb2ec5d2a0b83becc64150c2daaac9a75 |
| klines/SOLUSDT_4h.parquet | 13211 | 2020-09-14T04:00:00Z | 2026-09-24T20:00:00Z | 526181 | 6dfc049478f6e5fb8752c6211ebbda3b0c222afd95933d13b12b4d63e541d021 |
| klines/SOLUSDT_12h.parquet | 4404 | 2020-09-14T00:00:00Z | 2026-09-24T12:00:00Z | 185908 | 4cf86641273e67e15ba7963ee515f8c22075687e55aa84ae5692e269e2a2c3fc |
| klines/SOLUSDT_1d.parquet | 2201 | 2020-09-15T00:00:00Z | 2026-09-24T00:00:00Z | 96463 | bdcae2970043e3e95a9c43314e23105f62f28d23dbc76b7be2037ec2b7b5547b |
| klines/SOLUSDT_1w.parquet | 313 | 2020-09-21T00:00:00Z | 2026-09-14T00:00:00Z | 17829 | f4279094e89aa171b202da85cfbee77fb9a989eb1c4e085eca95429ce6e24a8f |
| funding/SOLUSDT.parquet | 6681 | 2020-09-14T08:00:00Z | 2026-09-25T00:00:00Z | 99168 | 63f3b205c1a88345c9c72bd4d9694b6349b069ce0ebbff93badebb9eabc37f8d |
| klines/NEARUSDT_5m.parquet | 625152 | 2020-10-15T08:00:00Z | 2026-09-24T23:55:00Z | 14398884 | 7d8e1ee901fe1c14c2bb661847ed7d2100aa791fa0898ece4f8c11d3f23f9c4d |
| klines/NEARUSDT_15m.parquet | 208384 | 2020-10-15T08:00:00Z | 2026-09-24T23:45:00Z | 5504927 | 6311c68998ae45169a444cebd2654e8191dbe5219919af1b204d209dea69aadf |
| klines/NEARUSDT_1h.parquet | 52096 | 2020-10-15T08:00:00Z | 2026-09-24T23:00:00Z | 1581789 | 5a8ddf6790886b4be75774d46a46014441b7114221e182c600ce77a0ab9de427 |
| klines/NEARUSDT_4h.parquet | 13024 | 2020-10-15T08:00:00Z | 2026-09-24T20:00:00Z | 437527 | e3fdd23041ffcdd3a55a8c24c9473389051d2c95d20a8c2d1fcb136144d04098 |
| klines/NEARUSDT_12h.parquet | 4342 | 2020-10-15T00:00:00Z | 2026-09-24T12:00:00Z | 168075 | 11165a4d35a40c8da0521892157b5af62ba44408c5361468f9d168bafebcd8ed |
| klines/NEARUSDT_1d.parquet | 2170 | 2020-10-16T00:00:00Z | 2026-09-24T00:00:00Z | 89784 | 617a9921e5c43e8feef13b3aa0e7ac678f48f8835158a1f36328197cb7e9adbd |
| klines/NEARUSDT_1w.parquet | 309 | 2020-10-19T00:00:00Z | 2026-09-14T00:00:00Z | 18175 | f3ee8ab250bf5b833dec8b5423d308850e69dfd1aacb72754c511cb8239a5ddc |
| funding/NEARUSDT.parquet | 6513 | 2020-10-15T08:00:00Z | 2026-09-25T00:00:00Z | 89390 | 593ac29381ca6c6432d3ce59f3134de000c7a1a428286a832835733b09adad50 |
| klines/ZECUSDT_5m.parquet | 698016 | 2020-02-05T08:00:00Z | 2026-09-24T23:55:00Z | 15197087 | 1d74958e1a7abcf9bb5b515c281a3a17b70033df7532f9e8a0a92278bf2d6c0a |
| klines/ZECUSDT_15m.parquet | 232672 | 2020-02-05T08:00:00Z | 2026-09-24T23:45:00Z | 5989421 | b02207c86e48ad614171432af1c86791cf0a860a1a5f72d07d3b914515213faa |
| klines/ZECUSDT_1h.parquet | 58168 | 2020-02-05T08:00:00Z | 2026-09-24T23:00:00Z | 1768699 | 8254440f1a068cae34971b9a58c7ff237838c62b7fcb8144fa5fb3b4d090de11 |
| klines/ZECUSDT_4h.parquet | 14542 | 2020-02-05T08:00:00Z | 2026-09-24T20:00:00Z | 500562 | 1e054d71061f18be429907a0331eb43eb1aa26fa511ca01af581f428b8844935 |
| klines/ZECUSDT_12h.parquet | 4848 | 2020-02-05T00:00:00Z | 2026-09-24T12:00:00Z | 183423 | d0e3bf8f9c974873ce6f41b4eb2493ff637567b1dcfea674badad9fbe7d3bbd0 |
| klines/ZECUSDT_1d.parquet | 2423 | 2020-02-06T00:00:00Z | 2026-09-24T00:00:00Z | 98159 | 323284e90c60706d93c9ab298418db1dc78c1129506e6dcbef209859f2932615 |
| klines/ZECUSDT_1w.parquet | 345 | 2020-02-10T00:00:00Z | 2026-09-14T00:00:00Z | 17867 | 1c330c55f26255885a32e2219dffbcb5c64f73a9209d51363a41e0db9b969196 |
| funding/ZECUSDT.parquet | 7272 | 2020-02-05T08:00:00Z | 2026-09-25T00:00:00Z | 92912 | 19a0080a11c5b3194a7be1a01e61f0f5ae244fc26be9a0e848dfcbeb7c6fa700 |

All 35 home kline rows: `gap_count 0`, `duplicates 0`, `rows_after_as_of 0`, native lenses `publication.carries = REST`
(15m `UNAUDITED`; 1d/1w derived). Venue zero-volume flat bars kept and counted (`venue_zero_volume_flat_bars`): 5m — BTC 86,
ETH 72, SOL 31, NEAR 34, ZEC 70; 1h — BTC 3, ETH 1; 15m — BTC 21, ETH 16, SOL 6, NEAR 6, ZEC 7; 4h/12h/1d/1w — 0.

**TC10 snapshot (frozen) — measured:** every home 5m ends 2026-09-21T16:25Z (6 rows past TC10's pin), 15m 16:15Z, 1h 15:00Z,
4h 12:00Z, 12h 2026-09-21T00:00Z, 1d 2026-09-20, 1w 2026-09-14, funding 2026-09-21T16:00Z; same first bars as TC11's.

**LIVE cache — measured (read of `open_time`/`funding_time` only; not a substrate):** home 5m end 2026-09-23T17:40Z
(ZEC 17:45Z), 15m 17:30Z, 1h 16:00Z, 4h 12:00Z; **12h ends 2026-08-15T00:00Z; funding ends 2026-08-15T16:00Z**; 1m ends
2026-08-15T16:03–16:04Z; 1d and 1w ABSENT. It is 15 days stale and behind the TC11 snapshot on every lens.

### 1.3 Schemas (pyarrow `read_schema`, identical in LIVE / TC10 / TC11, Binance and Bybit stems alike)

- klines: `open_time int64` (UTC ms, bar OPEN), `open double`, `high double`, `low double`, `close double`, `volume double`
  (= venue field index 5: BASE-asset volume in contract units; for `1000PEPEUSDT`/`1000BONKUSDT` units of 1000 tokens).
  `ED.KLINE_COLS` `ED:36`.
- funding: `funding_time int64` (UTC ms, raw venue stamp, jitters 0–47 ms past the hour), `funding_rate double`.
  `ED.FUNDING_COLS` `ED:189`.
- `load_funding_asof` adds `funding_hour_ms int64` (`D11:2499-2528`).
- No close-time, no trade count, no taker-buy volume, no quote volume is stored (`ED:117-118` keeps columns 0–5 only).

### 1.4 How the as-of is pinned at "the latest CLOSED 4h bar" — the two filed procedures

**TC10 (`D10:472-517`, `pin_as_of`)** — read off the VENUE clock at the first run:
`server_ms = GET /fapi/v1/time`; `open_ms = (server_ms // 4h)*4h − 4h`; `GET /fapi/v1/klines BTCUSDT 4h startTime=endTime=open_ms limit=1`;
HALT unless the row's `closeTime < server_ms`; `_dump_once` → `AS_OF_PIN.json` (write-once; a resumed run re-reads).
Filed: `M/research_outputs/tierc10/data/AS_OF_PIN.json` sha256 `0a78ae6993cc5fb9a9ddb09b1804ca76cfe6f401602a1c31f71eb0aed924e98a`:
`as_of_last_closed_4h 2026-09-21T16:00:00Z`, `…_close_ms 1790006400000`, `venue_close_time_of_pinned_bar_ms 1790006399999`,
`pinned_wall_clock_utc 2026-09-21T18:26:18Z`, `seed 20260921`.

**TC11 (`D11:719-793`, `pin_as_of`; reading L-0.1 `M/research_outputs/tierc11/LEANS.md:21-26`)** — pinned BY VALUE:
`PIN_CLOSE_MS = 1_790_294_400_000` typed at `D11:178` = "the latest 4h bar closed when STEP Q was filed" (STEP Q commit
`b9ed953` at 2026-09-25T00:09:43Z); proven closed by the venue (`closeTime == PIN−1 ms` and `< serverTime`, `D11:744-750`);
the run-time latest closed 4h filed beside it (`latest_closed_4h_at_pin_run*` keys) and as a `kind='clock'` FETCH_LOG row
(`record_fetch_clock`, `D11:804-823`); `pin_findings` (`D11:678-710`) re-checks a filed pin (4h modulus, open = close − 4h,
ISO = ms, venue kline row is that bar, seed, TC10's key set present).
Filed: `M/research_outputs/tierc11/data/AS_OF_PIN.json` sha256 `4f609ccfdf2bc61af2e9e2818ff3cd27aea3f88f7637bd73163b3947c977e4bd`
(1768 B): `as_of_last_closed_4h 2026-09-25T00:00:00Z`, `…_close_ms 1790294400000`, `…_open_ms 1790280000000`,
`bars_4h_past_tc10_pin 20`, `tc10_pin 2026-09-21T16:00:00Z`, `tc10_pin_close_ms 1790006400000`,
`pin_equals_latest_closed_at_pin_run true`, `venue_server_time_ms 1790297866708`, `seed 20260924`.
X's own pin record: `X/research_outputs/tierc11x/data/AS_OF_PIN.json` sha256 `c7b99c5865c7a2cfc3cb9ce0d71839115a0c3b8a4e397a69a42461084b91363e`
(same pin 1790294400000, read from TC11's PROGRESS; `latest_closed_4h_at_x_run 2026-09-25T04:00:00Z`).

**Per-lens "last closed bar at the pin"** — one formula, `target_last_open(iv, as_of_close_ms)` `D11:458-461`:
`((close − step − anchor)//step)*step + anchor`, anchor = Monday (`4*DAY_MS`) for 1w, else 0.
**As-of read law:** `load_asof(stem, iv, out=None)` `D11:2487-2495` keeps rows with `open_time + STEP_MS[iv] <= pin`;
funding kept through `pin + 60 s` (`FUNDING_JITTER_MS = 60_000`, `D11:241`, LEAN D-b) and cut on `funding_hour_ms <= pin`.

**TC12 candidate pins (arithmetic with the formula above; venue-proven for A, §1.16):**

| candidate | close_ms | 4h bars past TC11 / TC10 pin | new rows per stem vs TC11 edge: 5m · 15m · 1h · 4h · 12h · 1d · 1w | last closed 12h / 1d / 1w open |
|---|---|---|---|---|
| A · latest closed at STEP Q (22:52:13Z) | 1791489600000 = 2026-10-08T20:00:00Z | 83 / 103 | 3984 · 1328 · 332 · 83 · 27 · 13 · 2 | 10-08T00:00 / 10-07 / 09-28 |
| B · next close | 1791504000000 = 2026-10-09T00:00:00Z | 84 / 104 | 4032 · 1344 · 336 · 84 · 28 · 14 · 2 | 10-08T12:00 / 10-08 / 09-28 |
| C | 1791518400000 = 2026-10-09T04:00:00Z | 85 / 105 | 4080 · 1360 · 340 · 85 · 28 · 14 · 2 | 10-08T12:00 / 10-08 / 09-28 |

Funding prints to add (A): 41 per 8h-cadence tape, 83 per 4h-cadence tape (ENA PUMP HYPE BONK).

### 1.5 How a snapshot is cut — the exact TC11 procedure and code path (`D11`, run order `run_all` `D11:2584-2608`)

Run: `export NAIAD_CACHE_DIR=$HOME/.cache/naiad/snapshots/tc11_20260925 PYTHONDONTWRITEBYTECODE=1; ~/venvs/naiad/bin/python scripts/tierc11_data.py --all` (`D11:59-61`).

0. **Guard at import** `guard_substrate(env)` `D11:87-125`: HALT unless `NAIAD_CACHE_DIR` is set, absolute AS GIVEN (no `~`),
   not the live cache, not the TC10 snapshot, exactly the TC11 snapshot, with `klines/`. Runs before `engine.data` is imported.
   `_assert_bound()` `D11:486-492` re-checks `ED.cache_dir()` before every snapshot write.
1. **`--clone`** `clone_snapshot` `D11:548-602`: `cp -cpR <tc10 snapshot> <tc11 snapshot>` (APFS clonefile) only when the target
   does not exist; re-hash EVERY cloned file against TC10's `STAGE_D_MANIFEST.json` (`files[]` + `out_of_scope_snapshot_files[]`),
   any mismatch HALTs → `CLONE_ATTEST.json` (write-once). The only subcommand that runs without the guard.
2. **`--pin`** (§1.4) → `AS_OF_PIN.json` (write-once) + clock row.
3. **`--fetch`** `run_fetch` `D11:1386-1422`: `capture_contract_specs` (`D11:1009-1114`, ONE `/fapi/v1/exchangeInfo` + one Bybit
   `instruments-info`; HALT if any symbol not TRADING; write-once `CONTRACT_SPECS.json`) → `write_pre_state` (`D11:1161-1205`,
   write-once ledger of every in-scope file's sha/rows/edges/content-sha BEFORE the first fetch) → `audit_inherited_rows`
   (`D11:1219-1281`, read-only `EDGE_AUDIT.json`) → `extend_klines` in the order 4h, 12h, 1h, then funding, then 15m, 5m.
   `extend_klines` (`D11:1311-1354`): cursor = file edge + one step (HALT if not past the PRE_STATE edge — `_save_cache` keeps the
   NEW row at an identical `open_time`), target = `target_last_open(iv, pin)`, chunks of `CHUNK_BARS = 15_000` (`D11:310`),
   `_assert_grid` (HALT on an off-grid venue stamp), `ED._save_cache` (merge, no-shrink, tmp + `os.replace`), one `kind='klines'`
   row of `FETCH_LOG.jsonl` per chunk, `binance_brake()` between chunks.
4. **`--derive`** `run_derive` `D11:1564-1572`: 1d and 1w re-derived from the extended native 4h (§1.7), `_write_if_changed`.
5. **`--seal`** `seal_provenance` `D11:1438-1473`: `WRITE_ONCE_SEAL.json` over `SEALED_FILES` (`D11:1427`:
   AS_OF_PIN, CLONE_ATTEST, CONTRACT_SPECS, EDGE_AUDIT, PRE_STATE) + the fetch log's sealed line prefix.
6. **`--manifest`** `write_manifest` `D11:2450-2466` (no network, no snapshot write): `STAGE_D_MANIFEST.json/.md` +
   `fee_schedule.json`; `verify_prefixes` (`D11:1285-1305`) proves no pre-existing row moved; F-DET runs this twice.

Exit codes: 0 complete · 2 fetch incomplete (re-run resumes from each edge) · 1 HALT (`D11:62`).
TC11's whole networked run: FETCH_LOG first row 2026-09-25T00:57:46Z, last 00:59:46Z; 291 rows = 200 `http` + 73 `klines`
+ 17 `funding` + 1 `contract_specs`; all 200 HTTP rows status 200; max `x-mbx-used-weight-1m` 539
(`M/research_outputs/tierc11/data/FETCH_LOG.jsonl`, sha256 `bf34b4cd9f0f562f91358403a9d91b1d5ea3ed65057da92a781df98385e18ec7`).

**The live cache is a separate lane's and is not a substrate.** It is written by the ORACLE top-up
(`M/scripts/oracle_topup.py:1-44`, step `scope-topup` of `oracle_wrapper.py --job ondemand`, on demand since the schedule was
suspended 2026-09-21); scope `M/research_outputs/oracle/topup_scope.json` = 19 symbols × {5m, 15m, 1h, 4h} = 76 pairs
(no 12h, no funding, no SUI, no MNT); it fetches through `ED.backfill_klines` (`ED:231-302`: monthly archive zips, then daily
zips, then REST). Last run 2026-09-23 (`topup_log.jsonl`, 133 lines). launchd agents loaded now: `com.naiad.daily`,
`com.naiad.estate`, `com.naiad.workflow` only (the oracle plists exist but are not loaded). TC10 and TC11 both declare the live
cache "READ-NEVER, WRITE-NEVER" in code (`D10:58-60,106-108`; `D11:107`, `D11:339-340`); TC11's manifest carries
`live_cache_touched: false` with its basis (`D11:314-318`). **TC12 must fetch into a fresh snapshot; it may not read the live cache.**

### 1.6 Fetch mechanics

| venue | endpoint (public, unauthenticated) | paging | code |
|---|---|---|---|
| Binance USDT-M | `GET https://fapi.binance.com/fapi/v1/klines` `symbol, interval, startTime, endTime, limit=1500` | forward; next cursor = last `open_time` + step; 0.15 s sleep per page | `ED._fetch_rest_klines` `ED:107-130` |
| Binance | `GET /fapi/v1/fundingRate` `symbol, startTime, endTime, limit=1000` | forward; cursor = last `fundingTime` + 1 (resumes at file max + 1) | `ED.backfill_funding` `ED:349-382` |
| Binance | `GET /fapi/v1/time` · `/fapi/v1/ping` (reads `x-mbx-used-weight-1m`; waits out the minute at ≥ `WEIGHT_SOFT_CAP = 1200`) · `/fapi/v1/exchangeInfo` | — | `D11:739`, `binance_brake` `D11:888-898`, `D11:1023` |
| Bybit v5 linear (MNT only) | `GET https://api.bybit.com/v5/market/kline` `category=linear, symbol, interval ∈ {"5","60","240","720"}, start, end, limit=1000` | one window = one page (venue answers newest-first); 0.12 s sleep | `bybit_klines` `D11:925-946`, `BYBIT_IV` `D11:306` |
| Bybit | `GET /v5/market/funding/history` `limit=200` | BACKWARD from `endTime` | `bybit_funding` `D11:950-974` |
| Bybit | `GET /v5/market/instruments-info` | — | `D11:1048` |

- Retries: `ED._get` 4 attempts, 60 s timeout, returns on 200 **or 404** (`ED:63-74`); `_retry` 6 attempts with 20 s × attempt
  (`D11:873-884`); `_bybit_get` 6 attempts (`D11:851-869`). Every HTTP request is a `kind='http'` row via `CallLog` (`D11:613-666`).
- **REST only.** TC10 and TC11 fetched over REST exclusively. The BULK ARCHIVE (`ED.BULK_BASE = https://data.binance.vision/data/futures/um`,
  `ED:33`, `_fetch_bulk_zip` `ED:96-104`) is used only by the live-cache lane and by TC10's read-only audits (`D10:2559-2676`).
- `ED._fetch_rest_klines` indexes `INTERVAL_MS[interval]`; `M/engine/cells.py:9-16` defines only 1m 5m 15m 1h 4h 12h —
  **a native 1d or 1w fetch through the estate fetcher raises KeyError**; 1d/1w have never been fetched native.

### 1.7 Native vs derived · what "no synthetic bars" (F-D-2) means on disk

- `NATIVE_IVS = ("5m","1h","4h","12h")` `D11:230`; `FIFTEEN = "15m"` CLASSIC5 only `D11:231`; `DERIVED_IVS = ("1d","1w")` `D11:232`.
  **12h is fetched native** (Binance `12h`, Bybit `720`). **1d and 1w are DERIVED from native 4h, never fetched**
  (TC10 LEAN L1 `D10:283-285`, carried `D11:341-343`; manifest key `derivation`: "1d/1w derived from NATIVE 4h only [LEAN L1];
  never fetched native, never aggregated from 1h/5m (the venue's own intervals disagree on incident bars)").
- `derive_1d(f4h)` `D11:1505-1519`: a UTC day exists ONLY with all six 4h bars (`groupby(open_time // DAY_MS)`, open first,
  high max, low min, close last, volume sum); incomplete days dropped and counted.
  `derive_1w(d1)` `D11:1523-1536`: seven complete derived days, MONDAY-anchored (`MONDAY_EPOCH_OFFSET_MS = 4*DAY_MS`).
- **F-D-2 as defined in the only suite that carries it** (`FX10:491-620`, header "F-D-2 · NO SYNTHETIC BARS (Naiad inserted none)"):
  1. grid leg `_grid_faults` — every `open_time` of all 17 × `ALL_IVS = NATIVE_IVS + DERIVED_IVS` on its lens grid, no duplicate/backward;
  2. flat-bar recount `_flat0` (o=h=l=c and volume 0) must equal the manifest's `venue_zero_volume_flat_bars` per file;
  3. token leg — none of `BANNED_TOKENS = ("ffill","bfill","fillna","interpolate","reindex","resample","asfreq",".pad(")`
     (`FX10:492`) in the code (comments/docstrings stripped) of `FETCH_PATH_SOURCES = (engine/data.py, scripts/tierc10_data.py)` (`FX10:493`);
  4. attribution leg (online only) — sampled 5m flat bars re-asked of the venue (REST, or its archive for archive-assembled rows).
  The claim in its own words (`FX10:616-620`): "THE CLAIM IS 'Naiad inserted no bar', NOT 'the venue published no flat bar'".
  **Derived 1d/1w are not "synthetic" under this definition**; they are proven separately by F-D-L1 (`FX10:623-704`, an
  independent plain-loop rebuild) and, in TC11, F-D11-DERIVE.
  Checked this session: none of the eight banned tokens occurs in `engine/data.py`, `tierc10_data.py` or `tierc11_data.py`.
- TC11's own suite (`M/scripts/tierc11_data_fixtures.py`) has **no leg named F-D-2 or F-D-3**: its 14 legs are F-D11-GUARD,
  -BOUND, -PORT, -SCOPE, -CLONE, -PIN, -CLOCK, -PREFIX, -EDGE, -DERIVE, F-DET, -OUT, -FETCHPATH, -UNTOUCHED
  (header `:11-98`); funding coverage is checked inside F-D11-EDGE (`:1888` calls `D.funding_coverage`); there is no
  banned-token scan and no flat-bar recount leg there.

### 1.8 F-D-3 funding coverage as defined

- Pure function `funding_coverage(stem, as_of_close_ms, root=None) -> dict` `D11:1654-1672` (VERBATIM port of `D10:1077-1095`):
  `ok` is False if the file is absent, has no row at or before AS_OF + 60 s, or
  `last_ms + 60_000 < as_of_close_ms − ivl*1h`, where `ivl = interval_hours_observed_tail or …_modal or 8`
  (tail = median spacing of the last 10 prints, `scan_funding` `D11:1622-1650`).
- Fixture `FX10:707-814`: for every panel stem — coverage ok AND `tierc2_baseline.load_funding(stem)` non-empty (that loader
  returns `{}` silently on a missing file, `M/scripts/tierc2_baseline.py:216-233`) AND the funding-hour law
  (`_hour_faults`: floor hour == nearest hour for every print, loader column `funding_hour_ms` is that hour, nothing past the
  AS_OF hour comes out). HALT-grade.
- Observed cadence at the TC11 pin (manifest `files[kind=funding]`): 8h for BTC ETH SOL NEAR ZEC MNT SUI LTC XMR BNB UNI PEPE DOGE;
  4h for ENA PUMP HYPE BONK; SOL histogram `{2: 98, 4: 3, 8: 6579}`; every tape `coverage.ok true`, last print 2026-09-25T00:00:00Z;
  16 of 17 tapes hold one print stamped a few ms AFTER the pin close (it is the pin hour's print; kept by the +60 s rule);
  largest stamp offset past its hour 47 ms.
- Funding-from-the-kline-venue: Binance tapes from `/fapi/v1/fundingRate`, MNT from Bybit `funding/history`
  (`extend_funding` `D11:1359-1383`).

### 1.9 "Never spliced" and the Stage D table

- Operational definition = F-D-VENUE `FX10:927-993`: every file's venue equals its asset's venue of record; no FETCH_LOG row
  for a stem from another venue; an alternate-venue tape carries the venue IN its stem (`BYBIT_STEM_SUFFIX = "_BYBIT"`,
  `D11:303`) and no default-named twin file coexists. The venue of record is decided ONCE: `VENUE_PROBE.json` is write-once
  (`D10:549-637`), sealed, and TC11 re-read it read-only (`load_probe` `D11:834-841`, LEAN D11-c `D11:360-363`).
- **THE STAGE D TABLE — venue of record for all 17**, verbatim from `M/research_outputs/tierc10/close/S3_STAGE_D.md:59-77`
  (sha256 `eca4257650d82c301f5627476f324cb55ff3b084a3122ef3a8b645010c81711c`; spliced byte-exact from
  `tierc10/data/STAGE_D_MANIFEST.md`; underlying record `tierc10/data/VENUE_PROBE.json`
  sha256 `849810473cb8a1c7e23a4a85879141ab14a3618a4542465fb4b389f65278bc34`):

| asset | venue | symbol | file stem | status | listing | why |
|---|---|---|---|---|---|---|
| BTC | BINANCE_USDTM | BTCUSDT | BTCUSDT | TRADING | 2019-09-08T17:55:00Z | Binance USDT-M perpetual (the estate's venue of record) |
| ETH | BINANCE_USDTM | ETHUSDT | ETHUSDT | TRADING | 2019-11-27T07:45:00Z | Binance USDT-M perpetual (the estate's venue of record) |
| SOL | BINANCE_USDTM | SOLUSDT | SOLUSDT | TRADING | 2020-09-14T07:00:00Z | Binance USDT-M perpetual (the estate's venue of record) |
| NEAR | BINANCE_USDTM | NEARUSDT | NEARUSDT | TRADING | 2020-10-15T08:00:00Z | Binance USDT-M perpetual (the estate's venue of record) |
| ZEC | BINANCE_USDTM | ZECUSDT | ZECUSDT | TRADING | 2020-02-05T08:00:00Z | Binance USDT-M perpetual (the estate's venue of record) |
| ENA | BINANCE_USDTM | ENAUSDT | ENAUSDT | TRADING | 2024-04-02T12:30:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| PUMPFUN | BINANCE_USDTM | PUMPUSDT | PUMPUSDT | TRADING | 2025-07-10T07:30:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| HYPE | BINANCE_USDTM | HYPEUSDT | HYPEUSDT | TRADING | 2025-05-30T10:30:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| MNT | BYBIT_V5_LINEAR | MNTUSDT | MNTUSDT_BYBIT | Trading | 2023-10-02T05:40:55Z | ABSENT from Binance USDT-M exchangeInfo; the ENTIRE tape is Bybit v5 linear — one venue, never spliced |
| SUI | BINANCE_USDTM | SUIUSDT | SUIUSDT | TRADING | 2023-05-03T00:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| LTC | BINANCE_USDTM | LTCUSDT | LTCUSDT | TRADING | 2020-01-09T08:05:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| XMR | BINANCE_USDTM | XMRUSDT | XMRUSDT | TRADING | 2020-02-03T08:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| BNB | BINANCE_USDTM | BNBUSDT | BNBUSDT | TRADING | 2020-02-10T08:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| UNI | BINANCE_USDTM | UNIUSDT | UNIUSDT | TRADING | 2020-09-18T07:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| PEPE | BINANCE_USDTM | 1000PEPEUSDT | 1000PEPEUSDT | TRADING | 2023-05-05T00:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| DOGE | BINANCE_USDTM | DOGEUSDT | DOGEUSDT | TRADING | 2020-07-10T09:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |
| BONK | BINANCE_USDTM | 1000BONKUSDT | 1000BONKUSDT | TRADING | 2023-11-22T14:00:00Z | Binance USDT-M perpetual, TRADING (default venue) |

  `REJECTED for PUMPFUN: PUMPBTCUSDT — baseAsset PUMPBTC != PUMP: a different asset` (`S3_STAGE_D.md:79`).
- **The five home assets (CLASSIC5 = `tierc2_rules.UNIVERSE`, asserted `D11:293-295`):** BTCUSDT, ETHUSDT, SOLUSDT, NEARUSDT, ZECUSDT.
- **The twelve new (UNSEEN12 `D10:262-269`; stems in commission order `D11:299-301`):** ENA→ENAUSDT, PUMPFUN→PUMPUSDT,
  HYPE→HYPEUSDT, MNT→MNTUSDT_BYBIT, SUI→SUIUSDT, LTC→LTCUSDT, XMR→XMRUSDT, BNB→BNBUSDT, UNI→UNIUSDT, PEPE→1000PEPEUSDT,
  DOGE→DOGEUSDT, BONK→1000BONKUSDT. All 17 ADMITTED (≥ 316 + 400 = 716 closed 4h bars; `S3_STAGE_D.md:92-116`).
- Still-open TC10 nods carried by TC11's manifest `operator_rulings_needed`: PUMPFUN→PUMPUSDT [D-d] and MNT→Bybit [D-c].
- Multipliers: `1000PEPEUSDT` and `1000BONKUSDT` quote per 1000 tokens (`S3_STAGE_D.md:253,275`); the rest 1.

### 1.10 F-D-1 (REST vs ARCHIVE) — still open

- F-D-1 is filed RED ("3 bar(s) differ: XMRUSDT 4h 2025-01-14T12:00:00Z, XMRUSDT 1h 2024-10-28T20:00:00Z, XMRUSDT 5m
  2024-10-28T20:00:00Z", `S3_STAGE_D.md:20`) and "stays RED until the operator rules" (`D10:393-398`). The operator's R5
  ("The USDT pair, either on Binance or Bybit") names the pair, not the publication (`S3_STAGE_D.md:28-30`).
- Measured publication per native file (`S3_STAGE_D.md:487-492`): at 5m/1h/4h — REST: BTC ETH SOL NEAR ZEC SUI LTC;
  ARCHIVE: ENA XMR BNB UNI 1000PEPE DOGE 1000BONK; both: PUMP HYPE; single publication: MNT (Bybit). At 12h all Binance stems
  are REST (PUMP/HYPE both). **All five home assets carry REST on every native lens.** Rows TC11 added are REST by construction
  (`D11:2172-2174`); TC11's `operator_rulings_needed[0]` carries F-D-1 as "STILL OPEN".
- The TC12 contract names F-D-2 and F-D-3 only; it does not name F-D-1 and does not rule it.

### 1.11 The fee schedule — printed whole

File: `M/research_outputs/tierc11/data/fee_schedule.json` — 38,721 B, sha256 `6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b`
(certified in TC11 PROGRESS stage TC11-D; extracted by X to `X/research_outputs/tierc11x/data/tc11_rec/data/fee_schedule.json`).
Writer: `fee_schedule(assets, funding, pin)` `D11:1895-1973`. Printed losslessly: the 15 top-level keys verbatim, then the
17 asset rows as 11 keys that are identical on every row + 15 keys that vary (checked programmatically: 26 row keys, same key
set on all 17 rows).

**Top level (verbatim values):**
- `as_of_last_closed_4h`: "2026-09-25T00:00:00Z" · `as_of_last_closed_4h_open`: "2026-09-24T20:00:00Z" · `seed`: 20260924 · `tier`: "TIER-C11"
- `warranty`: "these files are described AS OF the pinned last closed 4h bar named here and of no other; bars stamped after it are counted, never read [TC6V-a, carried by TIER-C11]"
- `fee_law`: "fee = (FEE_BPS_SIDE / 10_000) * (entry_px + exit_px) (scripts/tierc2_baseline.py)"
- `haircut_twin_law`: "ADDED, never a replacement: haircut_twin_* keys carry the charter model (per-side taker fee + the charter's per-side slippage tier) beside round_trip_bps_used, which stays the TC-series accounting figure on every row [VETO 'tiers']. twin cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * (entry_px + exit_px); net_r_twin = gross_r - cost_px / risk_px (tierc10_data.haircut_twin_net_r)"
- `haircut_twin_clause`: "every row gets the charter model as a HAIRCUT TWIN beside the TC-series toll — slippage/side tier A {BTC ETH} 2 bps · tier B {SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR} 5 · tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10"
- `haircut_twin_tiers` == `charter_slippage_tiers`: `{"A": {"assets": ["BTC","ETH"], "bps_per_side": 2.0}, "B": {"assets": ["SOL","NEAR","ZEC","LTC","BNB","DOGE","UNI","SUI","XMR"], "bps_per_side": 5.0}, "C": {"assets": ["ENA","PUMPFUN","HYPE","MNT","PEPE","BONK"], "bps_per_side": 10.0}}`
- `charter_slippage_source`: ["Naiad_Phase0_Charter.md:114", "scripts/tierc10_data.py:217-220 (CONTRACT_SLIPPAGE_CLAUSE, read by AST)"]
- `maker_bps_per_side`: 2.0
- `maker_law`: "MAKER TWIN [L-1.2] — an ADDED column, never the toll of record: maker fee 2.0 bps per side (4.0 bps round trip) on the maker legs, ENTRY and TARGET only, with ZERO slippage on a maker leg; stop and invalidation legs stay TAKER at 5.0 bps per side, the toll of record's side rate, with no slippage in this twin (the charter slippage tier belongs to the haircut twin only [L-1.1]). A maker leg is ASSUMED filled at the named price (the contract's wording); the fill-risk column is the consuming stage's. MNT (Bybit) carries the same figure, an ASSUMPTION: Bybit's maker rate is not in the repo."
- `maker_source`: ["README.md:150 — \"**taker 0.05%/side** (the charter's 5 bps stands; maker is 0.02% but the\"", "scripts/v3_recompute.py:965 — the V3 R10 precedent ('maker entries 2 bps/side, taker stops 5 bps/side')"]
- `assets`: 17 rows, below.

**Row keys identical on all 17 rows:**
- `taker_bps_side_used`: 5.0 · `round_trip_bps_used`: 10.0 · `kind`: "ASSUMPTION — the estate's flat FEE_BPS_SIDE object, NOT a venue schedule"
- `source`: ["scripts/tierc2_rules.py:122", "scripts/tierc2_rules.py:123", "configs/naiad_v0.yaml:58"]
- `maker_bps_per_side`: 2.0 · `maker_round_trip_bps`: 4.0 · `maker_slippage_bps_side`: 0.0 · `maker_source`: (same two strings as top level)
- `haircut_twin_kind`: "CHARTER MODEL — an ADDED column beside the TC-series toll; round_trip_bps_used above is untouched and stays the accounting figure of record [VETO 'tiers']"
- `haircut_twin_source`: (the `haircut_twin_clause` string) · `charter_slippage_source`: (same two strings as top level)

**Row keys that vary** (`haircut_twin_tier` == `charter_slippage_tier`; `haircut_twin_slippage_bps_side` == `charter_slippage_bps_per_side`;
`haircut_twin_bps_side` = 5.0 + slippage; `haircut_twin_round_trip_bps` = 2 × that; funding modal == tail on every row):

| asset | stem | symbol | venue | tier | slippage bps/side | haircut bps/side | haircut round trip | funding interval h (modal = tail) | funding_spacing_hours_histogram |
|---|---|---|---|---|---:|---:|---:|---:|---|
| BTC | BTCUSDT | BTCUSDT | BINANCE_USDTM | A | 2.0 | 7.0 | 14.0 | 8 | {"8": 7715} |
| ETH | ETHUSDT | ETHUSDT | BINANCE_USDTM | A | 2.0 | 7.0 | 14.0 | 8 | {"8": 7481} |
| SOL | SOLUSDT | SOLUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"2": 98, "4": 3, "8": 6579} |
| NEAR | NEARUSDT | NEARUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 6512} |
| ZEC | ZECUSDT | ZECUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 7271} |
| ENA | ENAUSDT | ENAUSDT | BINANCE_USDTM | C | 10.0 | 15.0 | 30.0 | 4 | {"4": 5430, "8": 1} |
| PUMPFUN | PUMPUSDT | PUMPUSDT | BINANCE_USDTM | C | 10.0 | 15.0 | 30.0 | 4 | {"4": 2648, "8": 1} |
| HYPE | HYPEUSDT | HYPEUSDT | BINANCE_USDTM | C | 10.0 | 15.0 | 30.0 | 4 | {"4": 2893, "8": 1} |
| MNT | MNTUSDT_BYBIT | MNTUSDT | BYBIT_V5_LINEAR | C | 10.0 | 15.0 | 30.0 | 8 | {"8": 3267} |
| SUI | SUIUSDT | SUIUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 3721} |
| LTC | LTCUSDT | LTCUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 7352} |
| XMR | XMRUSDT | XMRUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 7280} |
| BNB | BNBUSDT | BNBUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 7256} |
| UNI | UNIUSDT | UNIUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 6596} |
| PEPE | 1000PEPEUSDT | 1000PEPEUSDT | BINANCE_USDTM | C | 10.0 | 15.0 | 30.0 | 8 | {"8": 3715} |
| DOGE | DOGEUSDT | DOGEUSDT | BINANCE_USDTM | B | 5.0 | 10.0 | 20.0 | 8 | {"8": 6803} |
| BONK | 1000BONKUSDT | 1000BONKUSDT | BINANCE_USDTM | C | 10.0 | 15.0 | 30.0 | 4 | {"4": 6222, "8": 1} |

- `maker_kind` — 16 Binance rows: "ASSUMPTION — Binance USDT-M VIP0 maker per README; the engine books every fill as taker; this is a TWIN, never the toll of record [L-1.2]";
  MNT row: "ASSUMPTION — Bybit's maker rate is not in the repo; the Binance VIP0 figure is applied to MNT unchanged [L-1.2]".
- `venue_note` — 16 Binance rows: "Binance USDT-M per-account commissionRate is a signed endpoint; not fetched";
  MNT row: "Bybit's published base taker rate for linear perpetuals is NOT fetched here (signed endpoint) and is widely quoted ABOVE 5.0 bps [UNVERIFIED, general knowledge]; the estate figure is applied unchanged and that is the assumption of record".

**Where each fee number comes from (all read, none typed):**
- taker 5.0 = `tierc2_rules.FEE_BPS_SIDE` (`M/scripts/tierc2_rules.py:122`, REGISTER row `:87`); round trip `:123`; mirror `M/configs/naiad_v0.yaml:58`.
- maker 2.0 = `read_maker_bps_side()` `D11:280-290`: regex `maker is (\d+(?:\.\d+)?)%` over `M/README.md` → line 150; ×100 → bps.
  The surrounding sentence, `M/README.md:149-151`: "Binance USDT-M VIP0 fees confirmed 2026-07-09 from the official fee page:
  **taker 0.05%/side** (the charter's 5 bps stands; maker is 0.02% but the engine books every fill as taker, conservatively)."
- slippage tiers = parsed from `CONTRACT_SLIPPAGE_CLAUSE` (`D10:217-220`, read by AST `D11:246`); charter line `M/Naiad_Phase0_Charter.md:114`.
- **No fee-page URL exists anywhere on disk.** Searched: `README.md`, `LEDGER.md`, `CHANGELOG.md`, `Naiad_Phase0_Charter.md`,
  `Naiad_Phase1_Build_Prompt.md`, `configs/`, `engine/*.py`, `D10`, `D11`, both `STAGE_D_MANIFEST.json`, both `fee_schedule.json`,
  `VENUE_PROBE.json`. The only URLs in the TC10/TC11 data records are `https://fapi.binance.com/fapi/v1/exchangeInfo`,
  the klines endpoint and Bybit `instruments-info`. The charter (`:112`) says the builder "confirms the current Binance
  USDT-M schedule at Phase 1 and records it in `LEDGER.md`"; `LEDGER.md` holds no such line.
- The in-memory fee table already uses the contract's key name: `tierc11_env.fees()` (`M/scripts/tierc11_env.py:1025-1045`,
  file sha256 `1526093b25161927337ced6112a310075b1a57c825f08705814e48619398f798`) returns per stem
  `{asset, venue, taker_bps_side, taker_round_trip_bps, maker_bps_side, maker_round_trip_bps, maker_kind, maker_slippage_bps_side,
  slippage_bps_side, slippage_tier}`, mapping JSON `maker_bps_per_side` → `maker_bps_side`. X's `tc11x_env.py:1278-1290` does the same.
- TC10's `fee_schedule.json` (sha256 `3a18b84e0211110b69eb09661b7e9a39db08f41c69ebdc4cc8ca8eb54a07e5cc`, 23,925 B) has no maker
  and no `charter_slippage_*` keys; TC11 added exactly: top `charter_slippage_source, charter_slippage_tiers, maker_bps_per_side,
  maker_law, maker_source, seed, tier`; row `charter_slippage_bps_per_side, charter_slippage_source, charter_slippage_tier,
  maker_bps_per_side, maker_kind, maker_round_trip_bps, maker_slippage_bps_side, maker_source`.

### 1.12 Tick size — where it is recorded, and what the tape says about it

- Recorded in `CONTRACT_SPECS.json`, `assets[].price_tick` (a string from Binance `PRICE_FILTER.tickSize` / Bybit `priceFilter.tickSize`,
  `D11:1040,1060`). Two captures, identical for all 17:
  `M/research_outputs/tierc11/data/CONTRACT_SPECS.json` sha256 `74d9d47b7177955237339eb417100581230efbaf13f2701677436df1c74a6b7e`
  (captured 2026-09-25T00:57:48Z, certified in TC11 PROGRESS, extracted by X to `tc11_rec/`), and
  `M/research_outputs/tierc10/data/CONTRACT_SPECS.json` sha256 `275b218d04a18a4a9383b1b16c5f18a1c1bd644875c8849a8a8c590113ed76d4`
  (captured 2026-09-22T13:11:55Z, gitignored). The manifest repeats it under `contract_multipliers.rows[].price_tick`.
  Existing reader: `price_tick(stem) -> float` in `M/scripts/tierc11_books_fixtures.py:340-346` (a fixture helper, not a library function).

| asset | stem | price_tick | qty_step | min_notional | tick ÷ last close at TC11 pin (bps, measured) |
|---|---|---|---|---|---:|
| BTC | BTCUSDT | 0.10 | 0.001 | 50 | 0.0119 |
| ETH | ETHUSDT | 0.01 | 0.001 | 20 | 0.0372 |
| SOL | SOLUSDT | 0.0100 | 0.01 | 5 | 0.8548 |
| NEAR | NEARUSDT | 0.0010 | 1 | 5 | 2.1786 |
| ZEC | ZECUSDT | 0.01 | 0.001 | 5 | 0.0647 |
| ENA | ENAUSDT | 0.0000100 | 1 | 5 | — |
| PUMPFUN | PUMPUSDT | 0.0000010 | 1 | 5 | — |
| HYPE | HYPEUSDT | 0.00100 | 0.01 | 5 | — |
| MNT | MNTUSDT_BYBIT | 0.00010 | 0.1 | 5 | — |
| SUI | SUIUSDT | 0.000100 | 0.1 | 5 | — |
| LTC | LTCUSDT | 0.01 | 0.001 | 20 | — |
| XMR | XMRUSDT | 0.01 | 0.001 | 5 | — |
| BNB | BNBUSDT | 0.010 | 0.01 | 5 | — |
| UNI | UNIUSDT | 0.0010 | 1 | 5 | — |
| PEPE | 1000PEPEUSDT | 0.0000001 (per 1000 tokens) | 1 | 5 | — |
| DOGE | DOGEUSDT | 0.000010 | 1 | 5 | — |
| BONK | 1000BONKUSDT | 0.0000010 (per 1000 tokens) | 1 | 5 | — |

- **The recorded tick is a point-in-time spec; the tape shows it was finer in the past** (measured: share of 5m `low` values
  of the TC11 snapshot that are NOT a multiple of the recorded tick):
  - BTCUSDT: off-grid through 2022-02-15 (2019: 23,756/32,905 · 2020: 70,110/105,408 · 2021: 69,694/105,120), on-grid from 2022-02-16.
  - NEARUSDT: off-grid through 2022-01-20, on-grid from 2022-01-21.
  - **SOLUSDT: off-grid through 2024-10-16** (2024-07: 7,309/8,928 … 2024-09: 7,072/8,640; 2024-10: 3,324/8,928), on-grid from
    2024-10-17 with a few stragglers (last 2025-10-10T03:55Z); smallest low increment observed after 2024-06-30 is 0.001.
    In the holdout era (after 1719791999000, `LEANS.md` L-1.3) **25,148 of 235,008** SOL 5m lows are off the recorded 0.01 grid.
  - ETHUSDT, ZECUSDT: 0 off-grid bars in the whole tape.
  In every observed case the recorded tick is COARSER than (or equal to) the tick then in force.
- No historical tick-size table exists anywhere on disk.

### 1.13 The LaCie and ATHENA's residency rules

- Rule of record, **Data residency v2 (operator ruling 2026-08-15)**: `M/exchange/status/CONVENTIONS.md:204-228`
  (sha256 `42b2cdd6ae4fa5cd85548c133862ac25ddad9c7dd3910b63555a5b628f8a226e`) and
  `M/exchange/reports/NOTE_ATHENA_2026-08-15_ALL-LANES_MAC-ERA-STATUS copy.txt` §1–§2, which "supersedes every prior geography note".
  - `/Volumes/LaCie` is "**backup only.** Bulk mirror plus the `naiad-backups` vault … Reads never touch it in normal work."
  - `~/.cache/naiad/data_cache` is "the data estate. NOT in the repo, never synced. `$NAIAD_CACHE_DIR` overrides."
  - "`drive_wait` gates backup WRITES, not substrate reads" — `M/scripts/drive_wait.py:203` `wait_for_drive(root, attempts=None, delay=None) -> DriveWaitResult`,
    states PRESENT / WOKE / UNREACHABLE (`:108-110`); halt only on UNREACHABLE, never a silent fallback
    (the 2026-08-11 note, amendment 2026-08-12: "A single failed lookup measures that lookup, not absence").
  - "`--estate` and `--workflow` write to `/Volumes/LaCie/naiad-backups`" (`CONVENTIONS.md:831`); default "is CORRECT … Pass no
    `--dest` unless you mean to override it" (`:835-837`).
  - Pointer discipline (2026-08-11 note §1.4): data never enters `exchange/`; path + sha256 pointer only.
- The 2026-08-11 notes (`NOTE_ATHENA_to_ARGUS_2026-08-11_DATA-RESIDENCY.md`, `NOTE_ATHENA_to_APOLLO_2026-08-11_data-residency.md`)
  are the Windows-era v1 ("ALL bulk data lives on `D:/Naiad`, mirroring repo paths"; every D: path carries a reachability gate).
  They are still the newest NOTE of their lane pairs (`BUILDERS_REPORT_HEPHAESTUS_2026-08-18_BOX-CLEANUP-MAILBOX.md:216-217`).
  No document under `M/exchange/` states a residency RULE newer than v2 (searched every `.md`/`.txt` modified after 2026-08-16
  for "residency"/"LaCie"): the later hits only cite the vault path `/Volumes/LaCie/naiad-backups`
  (`exchange/status/CADENCE.md:53`, `exchange/status/RETENTION.md:10,23`) and the aged-archive path
  `/Volumes/LaCie/Naiad/research_outputs/_archive` (`RETENTION.md:46`). `CONVENTIONS.md` was last written 2026-08-22.
- **No rule names a cache snapshot.** The words "snapshot"/"snapshots/" do not occur in the residency rules.
- `/Volumes/LaCie` is mounted now: `exfat`, `/dev/disk6s2`, 3.6 TiB, 1.2 TiB free. Top level: `$RECYCLE.BIN`, `Clau-MEM`,
  `Claude - Resources`, `MacPRO`, `Music`, `Naiad`, `Photos Library.photoslibrary`, `Repo Clone`, `Seagate`, `Trading`, `images`, `naiad-backups`.
  - `/Volumes/LaCie/Naiad/`: `CENSUS2A_CONTRACT_v0.3_RESOLVED_2026-08-12.md`, `research_outputs/` → `_archive census census2a census2b mc1 seq8 seq8_run2`.
  - `/Volumes/LaCie/naiad-backups/`: `naiad_estate_2026-09-27.zip` (633,529,440 B), `naiad_estate_2026-10-04.zip` (633,529,438 B),
    `naiad_workflow_2026-09-27.zip`, `naiad_workflow_2026-10-04.zip`, each with a `.sha256` sidecar — the LIVE weekly vault.
  - `/Volumes/LaCie/Repo Clone/`: `Naiad/`, `naiad-backups/` (older generations, 2026-07-28 … 2026-08-15).
  - **No `tc10`/`tc11`/`snapshots`/`data_cache` path exists on the LaCie** (searched to depth 3 under `Naiad`, `naiad-backups`, `Repo Clone`).
- The weekly estate archive (`M/scripts/backup_estate.py` `run_estate` `:1450-1500`) zips `engine.data.cache_dir()` — the LIVE cache by
  default — to `<dest>/naiad_estate_<local date>.zip`. It does not cover the snapshots.
- Status of the mirror for the two filed tiers: NOT DONE. TC11 manifest key `mirror`: "LaCie mirror NOT done [TC10 LEAN L5 carried] —
  every file TC11 fetched exists ONLY in the TC11 snapshot on this laptop". Operator text on record:
  `M/research_outputs/tierc10/OPERATOR_RULINGS.md:36` ("6- The LaCie destination and consent to push, which I'll ask for again at close.")
  and `:64-66` (R6: permission granted; destination unnamed).

### 1.14 Records TC12 will pin (path · sha256 · note)

| record | sha256 | note |
|---|---|---|
| `M/research_outputs/tierc11/data/STAGE_D_MANIFEST.json` | 0d8da58739bddcbf8c5243ef05bda67151a7b4d3957e10af28a8506c8d0ec712 | the clone reference: 124 `files[]` + 52 `out_of_scope_snapshot_files[]`; tracked; certified TC11-D |
| `M/research_outputs/tierc11/data/STAGE_D_MANIFEST.md` | 1f8e711391594bad6e7f5951c9437f8cbdf7ca18283022cf34d603fe3c636f24 | |
| `M/research_outputs/tierc11/data/AS_OF_PIN.json` | 4f609ccfdf2bc61af2e9e2818ff3cd27aea3f88f7637bd73163b3947c977e4bd | carries `tc10_pin_close_ms` too |
| `M/research_outputs/tierc11/data/fee_schedule.json` | 6febe170d423b0ef37dca9fe95a7316e4259ef5a77e576cafa6781d581c1968b | §1.11 |
| `M/research_outputs/tierc11/data/CONTRACT_SPECS.json` | 74d9d47b7177955237339eb417100581230efbaf13f2701677436df1c74a6b7e | ticks |
| `M/research_outputs/tierc11/data/PRE_STATE.json` | 29361958c3f94bc7d6ff97f27542fc7e5c0cb61db1fab7e6945c8ec7beae37d0 | |
| `M/research_outputs/tierc11/data/CLONE_ATTEST.json` | 3cbd6ff3bf819031057511427ca282588654588834f6828201ca1401d47cb441 | |
| `M/research_outputs/tierc11/data/EDGE_AUDIT.json` | c1fe3206fb099b01616a932746f6f65127dbef88861064aa49d6f56ba0816f39 | |
| `M/research_outputs/tierc11/data/WRITE_ONCE_SEAL.json` | 055dab8cc11c3bd5b848ea0ee2a1a1a04049233d448a98234c9e9ac2ec9aeaeb | |
| `M/research_outputs/tierc11/data/FETCH_LOG.jsonl` | bf34b4cd9f0f562f91358403a9d91b1d5ea3ed65057da92a781df98385e18ec7 | 291 lines, all sealed |
| `M/research_outputs/tierc11/PROGRESS.json` | dbcc08cf60a9dbb5827c65f3728857fcab12df50aeefee7667ba3dbfc205c4fe | certifies all 18 TC11-D artifacts (all MATCH on disk now) |
| `M/research_outputs/tierc10/data/VENUE_PROBE.json` | 849810473cb8a1c7e23a4a85879141ab14a3618a4542465fb4b389f65278bc34 | venue of record; **gitignored** (`M/.gitignore:263`) |
| `M/research_outputs/tierc10/data/AS_OF_PIN.json` | 0a78ae6993cc5fb9a9ddb09b1804ca76cfe6f401602a1c31f71eb0aed924e98a | gitignored |
| `M/research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | de2e8663bbf101dfb46ad9f77a4969ca73648e78373646c0d17b81b9f9a87421 | gitignored; source of the carried blocks |
| `M/research_outputs/tierc10/data/fee_schedule.json` | 3a18b84e0211110b69eb09661b7e9a39db08f41c69ebdc4cc8ca8eb54a07e5cc | gitignored |
| `M/research_outputs/tierc10/data/CONTRACT_SPECS.json` | 275b218d04a18a4a9383b1b16c5f18a1c1bd644875c8849a8a8c590113ed76d4 | gitignored |
| `M/research_outputs/tierc10/close/S3_STAGE_D.md` | eca4257650d82c301f5627476f324cb55ff3b084a3122ef3a8b645010c81711c | "the Stage D table" |
| `M/scripts/tierc11_data.py` | b2fe090f4a6cefe451c7f59cf6a60c4e27dbc69e637b7116340737d6cc6d8dcc | port source |
| `M/scripts/tierc10_data.py` | 2cbf9bb6bcfea3ec6184d5502ba5c530f5c0089d95288ab848a745ad5b3015fc | == `TC10_SRC_SHA256` typed at `D11:144` |
| `M/scripts/tierc10_data_fixtures.py` | 3807d905daf333ba8c7e421360bdc66fbab4268f0cea78b053cf55ab47d71587 | the only F-D-2 / F-D-3 code |
| `M/scripts/tierc11_data_fixtures.py` | 0e621e04583f42c56c3aa73827a594c593fc103d884f071c5c3cfca05dc5a8e0 | |
| `M/engine/data.py` | ddee40202f197765b7c65a1595f32b6d07543fbee517e104bf3610b828edc88f | the fetchers |
| `M/scripts/tierc2_rules.py` | 1739b4006b6a01296bb0b9f6bd8b6c22e546b09d5fa3b47b175545156b12fc2a | UNIVERSE, FEE_BPS_SIDE, TIDE_SLOW |
| `X/scripts/tc11x_data.py` | c73ca805509e504f1f7c5284de8375d389a59c88e71c766384ba44b8fd68b4d6 | no fetch; verify-only |
| `X/research_outputs/tierc11x/data/SUBSTRATE_VERIFY.json` | f0b450da903632e253fec4ba7031320c5989dd0508dbc4002ea3434629e5d453 | 42/42 read-set files matched |
| `X/research_outputs/tierc11x/data/AS_OF_PIN.json` | c7b99c5865c7a2cfc3cb9ce0d71839115a0c3b8a4e397a69a42461084b91363e | |

TC11's STAGE_D_MANIFEST schema TC12 must reproduce — top-level keys: `admission, as_of_hazards, as_of_last_closed_4h,
as_of_last_closed_4h_close_ms, as_of_last_closed_4h_open, as_of_last_closed_bar_per_lens, carried_from_tc10, clone_attestation,
complete, content_sha_law, contract, contract_multipliers, contract_premise_checks, data_spend, derivation, fifteen_minute_audit,
files, gap_policy, inherited_edge_audit, leans, live_cache_touched, live_cache_touched_basis, mirror, operator_rulings_needed,
out_of_scope_snapshot_files, panels, prefix_attestation, seed, snapshot_root, stage, standing_disclosures, tc10_record,
tc11_extension, tier, tiered_costs_haircut_twin, two_token_trap, venue_publications_disagree, venue_rejections, venues, warranty,
write_once`. Native kline row keys: `as_of_last_closed_bar_close, as_of_last_closed_bar_open, as_of_lens, asset, backward, bytes,
complete_to_as_of, content_sha, duplicates, first_open, first_open_ms, gap_count, gaps, kind, last_bar_close_equals_lens_last_closed_at_pin,
last_open, last_open_ms, lens_last_closed_bar_at_pin, listing, missing_bars_total, native, non_finite, off_grid, ohlc_incoherent,
path, pre_state, present, publication, rows, rows_after_as_of, rows_as_of, sha256, source, stem, tc10_manifest_sha256,
tc11_rows_added, venue, venue_flat_bars, venue_zero_volume_bars, venue_zero_volume_flat_bars`; derived rows add
`derivation_content_sha, derived_file_equals_derivation, derived_from, publication_inherited_from`; funding rows carry
`coverage, spacing_hours_histogram, interval_hours_observed_modal/tail, ms_past_hour_max/min, prints_stamped_after_as_of_close_within_jitter, …`.
`content_sha` = `frame_sha(df, cols)` `D11:416-425` (raw little-endian column bytes; independent of the parquet writer).

### 1.15 Signatures TC12 can port or must mirror (none can be IMPORTED under a TC12 snapshot — see hazard H1)

From `D11` (line · signature):
- `:87 guard_substrate(env: str | None) -> Path` · `:486 _assert_bound() -> None`
- `:187 pin_literal(path, table, key)` · `:207 source_literal(path, name) -> (value, first_line, last_line)`
- `:407 file_sha256(path) -> str` · `:416 frame_sha(df, cols) -> str` · `:429 _dump(obj, path)` · `:438 _dump_once(obj, path)`
- `:448 kline_path(stem, iv, root=None) -> Path` · `:453 funding_path(stem, root=None) -> Path`
- `:458 target_last_open(iv, as_of_close_ms) -> int` · `:464 lenses_of(stem) -> tuple` · `:471 scope_paths() -> list[str]` (124)
- `:499 tc10_expected_shas() -> dict` · `:509 tree_files(root)` · `:520 clone_findings(root, exp, ref_root) -> (faults, rows)` · `:548 clone_snapshot(out) -> dict`
- `:613 class CallLog(out, phase)` · `:678 pin_findings(pin, tc10_keys=None) -> list[str]` · `:719 pin_as_of(out) -> dict` ·
  `:796 venue_latest_closed(out) -> (server_ms, latest_close_ms)` · `:804 record_fetch_clock(out, pin=None)` · `:827 load_pin(out=None) -> dict`
- `:834 load_probe() -> dict` · `:844 panel_assets() -> list[dict]`
- `:851 _bybit_get(path, params)` · `:873 _retry(fn, what)` · `:888 binance_brake() -> int` · `:902 _fetch_log(out, row)` ·
  `:909 _edge(path, col) -> int | None` · `:917 _assert_grid(df, iv, what)` · `:925 bybit_klines(symbol, iv, start_ms, end_ms)` ·
  `:950 bybit_funding(symbol, start_ms, end_ms)`
- `:1009 capture_contract_specs(out, pin) -> dict` · `:1118 load_contract_specs(out=None)` · `:1124 contract_multiplier_table(out=None)`
- `:1161 write_pre_state(pin, out) -> dict` · `:1219 audit_inherited_rows(pin, pre, out)` · `:1285 verify_prefixes(pre, root=None) -> list[dict]`
- `:1311 extend_klines(a, iv, pin, out, pre) -> dict` · `:1359 extend_funding(a, pin, first_kline_ms, out) -> dict` · `:1386 run_fetch(pin, out)`
- `:1438 seal_provenance(out) -> dict` · `:1477 verify_seal(out=None, root=None) -> list[str]`
- `:1505 derive_1d(f4h) -> (df, dropped)` · `:1523 derive_1w(d1) -> (df, dropped)` · `:1550 derive_lenses(stem, pin)` · `:1575 derive_in_memory(stem, close_ms, root=None)`
- `:1588 scan_klines(df, iv, as_of_close_ms) -> dict` · `:1622 scan_funding(df, as_of_close_ms) -> dict` · `:1654 funding_coverage(stem, as_of_close_ms, root=None) -> dict`
- `:1744 tier_of(asset)` · `:1755 slippage_bps_side(asset)` · `:1761 charter_bps_side(asset)` · `:1788 haircut_twin_net_r(asset, gross_r, entry_px, exit_px, risk_px) -> dict`
- `:1895 fee_schedule(assets, funding, pin) -> dict` · `:2075 build_manifest(pin, pre) -> dict` · `:2450 write_manifest(dst) -> dict`
- downstream API: `:2471 load_manifest(out=None)` · `:2479 panel(out=None) -> {'CLASSIC5','UNSEEN','PANEL17'}` ·
  `:2487 load_asof(stem, iv, out=None) -> DataFrame` · `:2499 with_funding_hour(d, what="funding")` · `:2513 load_funding_asof(stem, out=None)`
- `PORTS` `D11:2532-2555` lists every port and whether it is VERBATIM (AST-identical to `D10`, proven by F-D11-PORT) or CHANGED.

From `ED`: `cache_dir()` `:39`, `_get(url, params=None, retries=4)` `:63`, `_fetch_rest_klines(symbol, interval, start_ms, end_ms)` `:107`,
`_save_cache(symbol, interval, df)` `:160`, `_save_funding(symbol, df)` `:202`, `backfill_funding(symbol, start_ms, end_ms, log=print)` `:349`.

From `X/scripts/tc11x_data.py` (verify-only pattern): `READ_SET` `:131-143`, `read_set(E)` `:1567`,
`verify_read_set(rows, manifest, snap_root) -> (rows, findings)` `:1590`, `substrate_verify_body(E, reads_doc)` `:1617`,
`write_once(p, body) -> 'WRITTEN'|'VERIFIED'` `:226`, `record_reads(stage, entries, out=None)` `:256`.

### 1.16 Reachability from this machine (the three permitted GETs, 2026-10-08T22:55:44–46Z)

1. `GET https://fapi.binance.com/fapi/v1/time` → HTTP 200, 0.48 s, `{"serverTime":1791500145154}` (2026-10-08T22:55:45Z).
2. `GET https://fapi.binance.com/fapi/v1/klines?symbol=BTCUSDT&interval=4h&startTime=1791475200000&endTime=1791475200000&limit=1`
   → HTTP 200, 0.41 s, one row: open_time 1791475200000 (2026-10-08T16:00Z), `closeTime 1791489599999` < serverTime →
   **the 4h bar closing 2026-10-08T20:00:00Z (1791489600000) is CLOSED by the venue's own record.**
3. `GET https://api.bybit.com/v5/market/kline?category=linear&symbol=MNTUSDT&interval=240&limit=1` → HTTP 200, 0.50 s, `retCode 0`,
   one row stamped 1791489600000 (the FORMING 20:00Z bar — Bybit returns the forming bar newest-first).
Both venues of record are reachable, unauthenticated, from this machine. Nothing was saved.

---

## 2 · CONTRACT-vs-DISK

1. **"{BTC ETH SOL NEAR ZEC}USDT.P"** — disk stems and venue symbols are `BTCUSDT … ZECUSDT` (no `.P`; `.P` is a charting-site
   suffix). Venue of record BINANCE_USDTM for all five (§1.9).
2. **"klines {5m,1h,4h,12h,1d,1w}"** — disk: 5m/1h/4h/12h are venue-native; **1d and 1w are not venue bars at all**: they are
   derived from native 4h (TC10 LEAN L1) and have never been fetched; the estate fetcher cannot fetch them (`engine/cells.py:9-16`).
   X's `READ_SET` reads "Stage D's derived 1d" (`X/scripts/tc11x_data.py:140-141`) and declares no 1w file.
3. **"F-D-2 no synthetic bars"** — the phrase is TC10's contract's (`M/exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md:56`); the
   filed definition is "Naiad inserted no bar" (grid + flat-bar recount + banned-token scan + venue attribution), which
   explicitly BANS the token `resample` in the fetch path yet admits groupby-derived 1d/1w, proven by a separate fixture (F-D-L1).
   The code exists only in `FX10`, which imports `tierc10_data` and HALTs off the TC10 snapshot. TC11 carried no leg by that name.
4. **"F-D-3 funding coverage per asset"** — defined (§1.8); also only in `FX10`. "per asset" on disk = per panel stem (17).
5. **"+ funding through the latest CLOSED 4h bar"** — disk law: funding is kept through pin close **+ 60 s** and attributed by
   floor-hour; 16 of 17 tapes hold a print stamped a few ms AFTER the pin close that belongs to the pin hour.
6. **"the latest CLOSED 4h bar (= the corridor pin, printed)"** — two different filed procedures (§1.4): TC10 = venue clock at
   first fetch run; TC11 = by value at STEP Q, typed, venue-proven. They can differ by one or more bars (table in §1.4).
7. **"the twelve new assets 1h/4h/1d only"** — disk: the TC11 snapshot holds 5m, 12h, 1w (and 15m for 9 of them) for the twelve
   as well, all ending at TC11's pin; TC11's scope was 17 × {5m,1h,4h,12h} + derived 1d/1w + CLASSIC5 15m + 17 funding = 124 files.
   The contract's sentence names no funding for the twelve, while "F-D-3 funding coverage per asset" and the 17-asset Tier-E
   views (STAGE S "the full-corridor and 17-asset views Tier-E"; "funding journaled") presume it; a 17-asset scalper view on
   "the 5m clock" presumes 5m for the twelve, which the same contract's Stage D excludes.
8. **"venue of record per TC10's Stage D table (never spliced)"** — carries exactly (§1.9). The table's underlying records are
   gitignored (`M/.gitignore:263` `research_outputs/tierc10/**`): they exist only in the main tree's working copy, not in any worktree.
9. **"sha manifest"** — carries: TC10/TC11 `STAGE_D_MANIFEST.json` schema (§1.14).
10. **"LaCie mirror per ATHENA's residency rules"** — the rules (§1.13) cover bulk repo data and estate/phase archives; they do
    not mention cache snapshots; the mirror was explicitly NOT done for TC10 or TC11; the destination was never named by the
    operator. Two disk statements disagree on the vault path:
    - `M/research_outputs/tierc10/OPERATOR_RULINGS.md:64-66` (executor operationalisation): "the real vault is
      `/Volumes/LaCie/Repo Clone/naiad-backups` and the default destination would create an empty vault, so the mirror must be
      invoked with an explicit `--dest`."
    - `M/exchange/status/CONVENTIONS.md:835-837`: "The default is `/Volumes/LaCie/naiad-backups` and is CORRECT … Pass no `--dest`
      unless you mean to override it"; `M/scripts/routine_jobs.json` `backup_dest`: "/Volumes/LaCie/naiad-backups".
    - Disk today: `/Volumes/LaCie/naiad-backups` holds the current generations (2026-09-27, 2026-10-04);
      `/Volumes/LaCie/Repo Clone/naiad-backups` holds the old ones (≤ 2026-08-15). The TC10 lean is stale against the disk.
    Also: the only "mirror command" (`backup_estate.py --estate`) names its output `naiad_estate_<date>.zip` regardless of which
    cache it zipped, and that script publishes the bus; LaCie is exFAT (no clonefile).
11. **"`data/fee_schedule.json` must carry maker_bps_side per venue"** — disk: no key named `maker_bps_side` in the JSON; the
    rate lives under `maker_bps_per_side` (top-level scalar 2.0 and on each of 17 ASSET rows), marked `ASSUMPTION`, with no
    per-VENUE block. The in-memory table `tierc11_env.fees()` does expose `maker_bps_side` per stem. So the key the contract
    names is present in code and absent in the file.
12. **"if absent, add it from the venue's published USDT-M perps schedule, cite URL + date in the manifest"** — disk: no URL
    anywhere; the only provenance is `README.md:149-150` ("confirmed 2026-07-09 from the official fee page … maker is 0.02%"),
    a Binance VIP0 figure applied unchanged to MNT (Bybit) with the note "Bybit's maker rate is not in the repo". The
    per-account fee endpoints are signed (`venue_note`); the repo holds no key. Bybit's product is "v5 linear", not "USDT-M".
13. **"print it as a pin ['maker-bps']"** — on disk the maker rate is a TWIN "never the toll of record" (`maker_law`, `maker_kind`);
    the 2026-10-08 ruling makes it the toll of record for scalper mode. The `maker_law` text of TC11's file contradicts the new status.
14. **"taker and charter tiers unchanged"** — carries: `taker_bps_side_used 5.0`, `round_trip_bps_used 10.0`, tiers A 2 / B 5 / C 10.
    TC10's Q2 (does slippage join the toll of record) is still open (`tierc11/BUILD_DRAFT.md:5990`).
15. **"a later 5m bar trades THROUGH the limit by ≥ 1 tick"** (STAGE S, substrate side) — a tick is recorded (§1.12) but only as a
    2026-09 point-in-time spec; for SOL the tick in force during the first 3.5 months of the holdout era was finer (0.001 vs 0.01).
    5m tapes hold venue zero-volume flat bars (BTC 86, ETH 72, SOL 31, NEAR 34, ZEC 70 over the whole tape).
16. **"re-ridden on the bars since 2026-09-21T16:00Z"** (STAGE L) — that instant is TC10's pin; it is on disk as
    `tierc10/data/AS_OF_PIN.json:as_of_last_closed_4h_close_ms = 1790006400000` (gitignored) and, tracked, as
    `tierc11/data/AS_OF_PIN.json:tc10_pin_close_ms`.
17. **"STAGE D · SUBSTRATE TOP-UP"** vs TC11's own filed limit: "the foundation is pinned to the TC11 snapshot and pin; a refresh
    on bars after 2026-09-25T00:00Z needs the foundation re-rooted on a new snapshot + pin record"
    (`tierc11/close/S5_FINDINGS_NOT_FIXED.md:447`). 35 `tierc11_*.py` files name `tc11_20260925` and 21 type `1790294400000`;
    31 `tc11x_*.py` files name a snapshot. A top-up is a new snapshot plus a re-root, not an in-place extension.

---

## 3 · READINGS NEEDED (candidate leans, to freeze before building)

**R1 · THE PIN.** Which bar is "the latest CLOSED 4h bar"?
(a) TC11's reading L-0.1: the latest 4h bar closed when STEP Q was filed → **1791489600000 = 2026-10-08T20:00:00Z** (STEP Q `28e006b`
at 22:52:13Z), pinned by value, venue-proven, write-once; the latest close at fetch time printed and filed beside it.
(b) TC10's reading: the latest closed 4h by the venue clock at the first fetch run (2026-10-09T00:00Z or later).
**Recommend (a).** It reuses the most recent filed reading, is fixed before any byte is fetched, cannot be chosen after a look,
and is already proven closed (§1.16). Cost: one to a few fewer forward bars and the 2026-10-08 daily bar is not yet closed.
The value should enter the code from the frozen LEANS and be cross-checked by a fixture against the STEP Q commit time.

**R2 · SNAPSHOT.** Read the live cache, extend tc11 in place, or cut a new snapshot?
**Recommend:** a new snapshot `~/.cache/naiad/snapshots/tc12_20261008` (name = pin date, as tc10_20260921/tc11_20260925), an APFS
clone (`cp -cpR`) of `tc11_20260925`, every file re-hashed against TC11's `STAGE_D_MANIFEST.json` (0d8da587…) before the first
write, extended over REST only. Live cache: never read, never written. TC10 and TC11 snapshots: never written.

**R3 · FETCH SCOPE.** Contract list (5 home × {5m,1h,4h,12h} + 5 funding; 12 × {1h,4h}; derived 1d for 17, 1w for 5) or TC11's
full scope (17 × {5m,1h,4h,12h} + 17 funding + derived 1d/1w for 17 + CLASSIC5 15m = 124 files)?
**Recommend the superset = TC11's 124-file scope**, disclosed as a superset (TC11 lean D11-a precedent). One uniform edge per
lens; `complete_to_as_of` stays strict on every in-scope file; the 17-asset Tier-E views and F-D-3 "per asset" have their 5m and
funding; the port stays near-verbatim. Extra cost ≈ 12 × (3984 + 27) kline rows + 12 funding tails + 5 × 1328 15m rows.
The contract's "1h/4h/1d only" then binds the twelve's LENSES IN STAGE V, not the fetch. (Strict alternative: fetch only the
contract's list and list every other snapshot file as out-of-scope, unchanged, by sha.)

**R4 · 1d AND 1w.** Fetch native or keep derived?
**Recommend derived from native 4h** (TC10 LEAN L1, carried by TC11 and read by X): 1d = six complete 4h bars of one UTC day,
1w = seven complete derived days, Monday-anchored. X's 1d verdicts (which F-VA-MIRROR must reproduce word for word) were
measured on these derived bars; a native 1d would differ on incident bars; and the estate fetcher cannot fetch 1d/1w.

**R5 · F-D-2 DEFINITION.** **Recommend TC10's filed definition, ported whole** (§1.7: grid, flat-bar recount vs manifest, banned-token
scan over the TC12 fetch-path sources, venue attribution of sampled flat bars), plus the derived-lens rebuild (F-D-L1 /
F-D11-DERIVE) as the proof that 1d/1w are derivations, not insertions. The leg must state the claim in TC10's words.

**R6 · F-D-3 DEFINITION AND PANEL.** **Recommend `funding_coverage` verbatim + the funding-hour law, over all 17 stems** (not only
the five), with `load_funding_asof` as the reader (HALT on absent/empty).

**R7 · REST vs ARCHIVE (F-D-1).** **Recommend REST only**, as TC10 and TC11; the new rows are REST by construction; F-D-1 is
carried as TC10's open operator question, not re-opened, not re-cut, not silently dropped — printed in the manifest's
`operator_rulings_needed`. (The archive has no monthly zip for the running month and its daily zips lag.)

**R8 · "maker_bps_side per venue" — IS IT ABSENT?** (a) present (alias `maker_bps_per_side`); (b) absent in the contract's sense.
**Recommend (b):** TC12's own `research_outputs/tierc12/data/fee_schedule.json` gains a top-level per-venue block
`maker_bps_side: {BINANCE_USDTM: …, BYBIT_V5_LINEAR: …}` with `source_url`, `retrieved_utc`, `tier` and `kind`, and each asset row
gains `maker_bps_side` read from its venue's entry; every TC11 key stays byte-for-byte in meaning (`maker_bps_per_side` kept, so
`fees()`-style readers still work). TC11's file is never edited.

**R9 · THE MAKER NUMBER AND ITS SOURCE.** The published schedule is a web page, not an API (§2.12).
**Recommend:** the executor retrieves each venue's public fee page once, records URL + retrieval date + the base (non-VIP,
no-discount, no-rebate, no-promotion) USDT-margined perpetual maker rate, and files that. Non-flattering rule: where a page
shows several maker rates, take the HIGHEST an unprivileged account pays. If a page cannot be retrieved or parsed, the pin
falls back to the README-recorded 2.0 bps (README.md:150, confirmed 2026-07-09) flagged `NOT RE-CONFIRMED` with the attempted
URL and date — never a remembered number. If the published Binance base rate is not 2.0, the published figure is the pin and
the difference from TC11's twin is printed (X's "1h maker PASS" was measured at 4.0 bps round trip).
Candidate URLs — from the scout's general knowledge, NOT read from any file, to be confirmed by the executor:
Binance `https://www.binance.com/en/fee/futureFee`; Bybit `https://www.bybit.com/en/help-center/article/Trading-Fee-Structure`.

**R10 · BYBIT MAKER FOR MNT.** (a) Bybit's published base rate; (b) carry Binance's figure as TC11 did (ASSUMPTION).
**Recommend (a) when retrievable, else the larger of the two figures on file, marked ASSUMPTION.** MNT is not a home asset, so
this touches Tier-E views only.

**R11 · THE TICK OF RECORD.** (a) `price_tick` from TC12's own `CONTRACT_SPECS.json` capture at its pin, applied over the whole
corridor; (b) TC11's capture; (c) a tick inferred from the tape per era.
**Recommend (a)**, with the TC11 capture diffed beside it and the measured history of §1.12 disclosed. The recorded tick is
coarser than or equal to the historical tick in every measured case, so "through by ≥ 1 recorded tick" is at least as strict
as the historical rule: it cannot flatter the fill count. (Related, for the stage that owns it: a limit "AT the edge" must be
snapped to the tick grid, and the non-flattering direction is away from price — down for a long at VAL, up for a short at VAH.)

**R12 · LaCie MIRROR — FORM AND DESTINATION.** (a) a plain directory mirror under `/Volumes/LaCie/Naiad/…`; (b) an estate-style zip in
`/Volumes/LaCie/naiad-backups` via `backup_estate.py`; (c) leave it to the operator at CLOSE as TC10/TC11 did.
**Recommend (a):** copy the TC12 snapshot to `/Volumes/LaCie/Naiad/snapshots/tc12_20261008/` behind `wait_for_drive('/Volumes/LaCie')`
(mirror step HALTs on UNREACHABLE; the build's reads never depend on the drive), then re-hash every file FROM the destination
against TC12's manifest and file `MIRROR_ATTEST.json` (path + sha pointers only; nothing data-class on the bus). Not (b): the
script would name a snapshot archive `naiad_estate_<date>.zip` beside the real live-cache generations and it publishes.
The destination is a new path the operator never named — it must be printed as a lean and may need the operator's keystroke.

**R13 · MIRROR SCOPE.** TC12 snapshot only, or also the still-unmirrored tc10 and tc11 snapshots?
**Recommend:** TC12's whole snapshot is the contract's act; mirroring tc10_20260921 and tc11_20260925 in the same act (each
verified against its own filed manifest; ≈ 0.86 GB each on exFAT) closes the open TC10/TC11 item and protects the bytes
F-CTRL and F-VA-MIRROR stand on, but it is a widening — the orchestrator's call.

**R14 · THE 15m TAPES.** Extend CLASSIC5 15m (TC11 scope) or leave them at TC11's edge as out-of-scope?
**Recommend extend** (falls out of R3; keeps `scope_paths()` and the scope fixture's typed 124 unchanged). No TC12 stage reads 15m.

**R15 · TC11-CORRIDOR READS ON THE TC12 SNAPSHOT.** F-CTRL and F-VA-MIRROR run on TC11's corridor. Read through (a) a process bound
to the frozen tc11 snapshot, or (b) the TC12 snapshot cut at TC11's pin?
**Recommend (a) for the anchor process and (b) only through `load_asof`-style cuts** — never a whole-file reader — with F-PREFIX
proving the two are the same rows (substrate side of "cross-process anchored").

**R16 · WHAT TO CARRY FROM TC10 WITHOUT RE-MEASURING.** `two_token_trap`, `data_spend`, `venue_publications_disagree` were carried
verbatim by TC11 (lean D11-d). **Recommend carry again**, from TC11's manifest (tracked), with the sha chain TC10 → TC11 → TC12 printed.

---

## 4 · HAZARDS

**H1 · Import-time HALTs.** `tierc10_data` HALTs at import unless `NAIAD_CACHE_DIR` is the TC10 snapshot (`D10:94-117`);
`tierc11_data` unless it is the TC11 snapshot (`D11:87-125`). Neither can be imported under a TC12 snapshot, and `FX10`
(the only F-D-2/F-D-3 code) imports `tierc10_data`. Everything must be ported a third time or run cross-process.

**H2 · `NAIAD_CACHE_DIR` must be exported, absolute, before python starts.** `tierc2_baseline` binds `KLINES`/`FUNDING` at import
(`M/scripts/tierc2_baseline.py:205-206`); `engine.data.cache_dir()` uses `Path(env)` with no `~` expansion and **creates the
directory** (`ED:39-48`) — an unset variable silently resolves to the LIVE cache, a relative one to the working directory.

**H3 · Look-ahead through whole-file readers.** `tierc2_baseline.load_klines` reads the whole file with no as-of cut (`:209-213`).
In TC11 that was harmless because every file ended at the pin; on a TC12 snapshot, any TC11-corridor computation (F-CTRL,
F-VA-MIRROR) that reaches a whole-file reader sees 83+ 4h bars past TC11's pin. `load_funding` (`:216-233`) likewise returns
every print, and returns `{}` silently for a missing tape.

**H4 · An early fetch start overwrites history.** `ED._save_cache` keeps the NEW row at an identical `open_time` (`ED:160-186`,
`keep="last"`). A fetch that starts at or before a file's edge would replace inherited bars with today's REST publication —
and for the seven ARCHIVE-carrying stems the two publications differ on incident bars. `extend_klines` HALTs on it; a port must keep that.

**H5 · The forming bar.** Bybit returns the forming bar (§1.16 GET 3); Binance does too when `endTime` ≥ now. Safety rests entirely on
`end = target_last_open(iv, pin)` and the `[lo, hi]` filter (`D11:1340`). `ED._get` returns a 404 response as success (`ED:68`).

**H6 · The live cache can move mid-build.** An on-demand `/oracle` run tops it up (`oracle_topup.py`), through archive-first
`backfill_klines`. It has no 12h/funding past 2026-08-15, no 1d/1w, no SUI/MNT, and mixed publications. Reading it would break
determinism and the venue-of-record law silently.

**H7 · Frozen records.** TC11's `fee_schedule.json`, `STAGE_D_MANIFEST.json`, `AS_OF_PIN.json`, `CONTRACT_SPECS.json` are certified
by sha in TC11's PROGRESS and re-certified by X (`tc11_rec/`, `SUBSTRATE_VERIFY.json`). "Add maker_bps_side" must land in a NEW
TC12 file. `_dump_once`/`write_once` records (pin, pre-state, clone attest, specs, seal) must stay write-once; `_out_guard`
(`D11:2433-2447`) is what keeps `--out` from landing in `research_outputs/tierc10`.

**H8 · TC10's records are gitignored.** `VENUE_PROBE.json`, TC10's pin and manifest exist only in the main working copy
(`.gitignore:263`); a review worktree does not carry them (`_main_tree`, `D11:150-168`, reads them by absolute main-tree path).
A fresh worktree for TC12 inherits that. `research_outputs/tierc12/**` is NOT ignored — any parquet written there would be tracked.

**H9 · The X worktree must not gain a file.** Importing a module from `X/scripts` without `PYTHONDONTWRITEBYTECODE=1`/`-B` writes
`__pycache__` there, and X's modules write records under `X/research_outputs/tierc11x` when run. Read X by sha (blobs at
`7b24f835`), never execute in place. X already shows one untracked file: `research_outputs/tierc11x/close/CERTIFIED_TIP`.

**H10 · Determinism.** Parquet file bytes depend on the writer; `content_sha` (`frame_sha`) is the writer-independent pin, and
F-DET compares it across two hash-seed builds. Wall clocks may live only in provenance files (pin, specs, fetch log, seal),
never in the manifest (`D11:1140-1145`; the X clock-field scan `tc11x_data.py:158-159`). `fee_schedule.json` gaining a
`retrieved_utc` is a clock field in a determinism-set file — it must be a recorded constant read from a provenance record,
not `now()`.

**H11 · The venue's intervals disagree with each other on incident bars** (printed in `FX10:352-356`; TC11's `fifteen_minute_audit`
is "a DISCLOSURE, never a failure"). 5m children do not always rebuild their 1h parent. A scalper that reads 1h state and
trades on 5m, and any raw-volume recomputation across lenses (F-VA-RAW), must compare SAME-interval data only.

**H12 · Venue zero-volume flat bars in the 5m and 1h tapes** (§1.2). They are real published bars (outages). They carry no volume
for a profile and cannot honestly fill a resting order; they must be counted, not filtered silently and not treated as trades.

**H13 · Tick history.** The recorded tick is not the historical tick for BTC (< 2022-02-16), NEAR (< 2022-01-21), SOL (< 2024-10-17,
inside the holdout era). Prices before those dates are off the recorded grid, so any "price is a multiple of tick" assertion
fails there, and a tick inferred from data would differ from the record.

**H14 · 1000-token contracts.** `1000PEPEUSDT`/`1000BONKUSDT` prices and ticks are per 1000 tokens; ratios are invariant, absolute
ticks are not (`S3_STAGE_D.md:279`).

**H15 · The operator's pending close acts.** `tierc10/close/close_acts.sh` and `tierc11/close/close_acts.sh` export
`NAIAD_CACHE_DIR` to their own snapshots, re-run their own fixtures and require a clean index on `v12-v1-census`
(`tierc10/close/close_acts.sh:26,42-47`; `tierc11/close/close_acts.sh:30,48-58`); step 1 of each is `git push origin` of
everything on the branch. Both snapshots must stay byte-identical until they run. The main tree already shows a modified
tracked TC10 file (`research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`) — not this scout's doing.

**H16 · Automation that touches the same places.** `com.naiad.daily` (07:00 local) commits "exchange: auto-publish <date>" on the
main branch every day and stages `exchange/**`; `com.naiad.estate` (Sunday 08:00 local) zips the live cache to the LaCie vault.
Anything left under `exchange/` (e.g. `exchange/rows/tierc12/`) can be swept into the next auto-publish commit.
`backup_estate.py` run by hand also publishes.

**H17 · LaCie.** exFAT: no clonefile, no permissions, case-insensitive; a USB disk that can be asleep or absent — one failed lookup
is not absence (`wait_for_drive`). A mirror "verified" by listing is not verified; re-read from the destination.

**H18 · Disk and clone semantics.** `cp -cpR` is free until a file is replaced; every extended file is rewritten whole
(`os.replace`), so the TC12 snapshot costs ≈ the in-scope bytes (≈ 0.29 GB) of new blocks. The 1m tapes (0.48 GB) ride along
untouched. Local free space 1.6 TiB.

**H19 · Typed-constant debt.** TC11 typed `PIN_CLOSE_MS`, `TC10_PIN_CLOSE_MS`, `TC10_SRC_SHA256`, `CONTRACT_SHA256` (`D11:144,174,178,179`).
Under TC12's "no number typed that a file can supply", TC10's and TC11's pins are in `tierc11/data/AS_OF_PIN.json` and should be read.

---

## 5 · REUSE PLAN

**New file `scripts/tierc12_data.py` — a port of `D11` (b2fe090f…), same subcommands `--clone --pin --fetch --derive --seal --manifest --all`.**
Carry `PORTS`-style provenance comments and an AST-identity fixture against `D11` (F-D11-PORT's pattern).

- VERBATIM (AST-identical to `D11`): `pin_literal, source_literal, parse_slippage_clause, log, iso, file_sha256, frame_sha, _dump,
  _dump_once, target_last_open, split_rel, tree_files, clone_findings, CallLog, _venue_4h_row, _bybit_get, _retry, binance_brake,
  _fetch_log, _edge, _assert_grid, bybit_klines, bybit_funding, base_multiplier, normalize_price, normalize_qty, load_contract_specs,
  verify_prefixes, _lines_sha, verify_seal, derive_1d, derive_1w, _write_if_changed, derive_lenses, run_derive, derive_in_memory,
  scan_klines, scan_funding, funding_coverage, _source_line, tier_of, slippage_bps_side, charter_bps_side, charter_round_trip_bps,
  assert_tiers_cover, haircut_twin_net_r, haircut_twin_for_stem, haircut_twin_table, premise_checks, load_manifest, panel,
  load_asof, with_funding_hour, load_funding_asof, record_fetch_clock, venue_latest_closed, extend_klines, extend_funding, run_fetch`.
- CHANGED, each change named:
  - `SNAPSHOT` → the TC12 snapshot; `guard_substrate` refuses the live cache, the TC10 snapshot **and the TC11 snapshot**;
  - `clone_snapshot` clones `tc11_20260925` and re-hashes against TC11's manifest (`tc10_expected_shas` → a TC11 twin);
  - `pin_as_of`/`pin_findings`: TC12's pin (R1); TC10/TC11 pins READ from `tierc11/data/AS_OF_PIN.json`;
  - `write_pre_state`/`inherited_rows`/`audit_inherited_rows`: previous edge = TC11's (no rows sit past TC11's pin, so the
    inherited-edge audit has nothing to audit — say so rather than drop the record);
  - `capture_contract_specs`: unchanged logic, TC12's capture; it is also the TICK record (R11) and the TRADING proof;
  - `seal_provenance`: TC12's sealed set;
  - `fee_schedule`: + the per-venue `maker_bps_side` block with URL/date/tier, + `maker_bps_side` per row, `maker_law` rewritten
    for the 2026-10-08 ruling (toll of record for scalper mode; twin elsewhere), every TC11 key kept (R8, R9);
  - `build_manifest`: `tc11_extension` → `tc12_extension`; `tc10_record` kept + a `tc11_record` block; `carried_from_tc10` chain
    (R16); `mirror` → the mirror attestation or "NOT done"; `operator_rulings_needed` carried + the maker source + the mirror destination;
  - `OUT` = `research_outputs/tierc12/data`, `SEED = 20261008`, contract path/sha = the TC12 contract (861d6050…).
- Reused by import (unchanged, no HALT of their own): `engine.data` (`_get, _fetch_rest_klines, _save_cache, _save_funding,
  backfill_funding, cache_dir, REST_BASE, KLINE_COLS, FUNDING_COLS`), `engine.cells.INTERVAL_MS`, `tierc2_rules` (`UNIVERSE,
  FEE_BPS_SIDE, FEE_BPS_ROUND_TRIP, TIDE_SLOW`), `scripts/drive_wait.wait_for_drive` (mirror gate).
- Read, never imported: `D10` literals `UNSEEN12`, `CONTRACT_SLIPPAGE_CLAUSE`, `NORMALIZATION_LAW` by AST (as `D11:246,296,982` do);
  `engine/rangefinder.py PINS_V2['MEM_TTL_BARS']` by `pin_literal`; `README.md` maker sentence by regex.

**New file `scripts/tierc12_data_fixtures.py`.**
- From TC11's suite, re-pointed: F-D11-GUARD, -BOUND, -PORT, -SCOPE, -CLONE, -PIN, -PREFIX, -EDGE, -DERIVE, -OUT, -FETCHPATH,
  -UNTOUCHED (now covering BOTH frozen snapshots + the live-cache stat), F-DET (two hash-seed manifest builds, content shas).
- **F-D-2** mirrored from `FX10:491-620` (`BANNED_TOKENS`, `code_only`, `_token_scan`, `_grid_faults`, `_flat0`, `fd2_break`,
  `fd2_real`), with `FETCH_PATH_SOURCES = (engine/data.py, scripts/tierc12_data.py)`; the online attribution leg reported NOT RUN
  (never PASS) when offline.
- **F-D-3** mirrored from `FX10:707-814` (`_fd3`, `_hour_faults`, `fd3_break`, `fd3_real`) over all 17 stems.
- New legs: F-TICK (every tick read from `CONTRACT_SPECS.json`; a typed tick FAILS; TC11-vs-TC12 capture diff printed);
  F-FEE-MAKER (the `maker_bps_side` block present per venue, each with URL + date; rows equal their venue's entry; taker and tiers
  byte-equal to TC11's; a row with no source FAILS) — the substrate half of the contract's F-TOLL;
  F-MIRROR (every mirrored file re-read from the LaCie equals the manifest sha; a flipped byte in a temp copy must FAIL; an
  unreachable drive is NOT RUN, never PASS).

**Vendored / mirrored from X (read by sha at `7b24f835`, never executed in place):** the verify-only pattern of
`tc11x_data.py` — `read_set`, `verify_read_set`, `substrate_verify_body`, `write_once`, `record_reads` — for any TC12 stage that
must prove "every snapshot file I opened is in the verified set" and for reading TC11/X text records sha-first.

**Must be newly written (no precedent on disk):** the per-venue maker block and its source record; the tick reader as a library
function (today only a fixture helper, `tierc11_books_fixtures.py:340-346`); the LaCie directory mirror + `MIRROR_ATTEST.json`;
a `tc11`-reference twin of `tc10_expected_shas`; the pin fixture's cross-check against the STEP Q commit time.

**Expected run (R1 = A, R3 = superset):** ≈ 17 × (3984 + 332 + 83 + 27) + 5 × 1328 ≈ 81,882 kline rows, 17 funding tails
(41 or 83 prints), derived +13 daily and +2 weekly bars per stem; a few hundred public GETs; TC11's equivalent run took two minutes.
