# TC11-D builder report (2026-09-25)

TC11-D is done: the pipeline exited 0 with `complete=True`, and all 9 fixtures are GREEN (every break leg went RED first; exit 0). Nothing was committed or staged.

**Pin** (`AS_OF_PIN.json`, write-once, has all 11 of TC10's keys plus 14 extra)
- as_of_last_closed_4h is 2026-09-25T00:00:00Z. Open ms is 1790280000000 and close ms is 1790294400000.
- The venue proves it closed: Binance's BTCUSDT 4h closeTime is 1790294399999, earlier than the venue clock 1790297866708 (00:57:46Z). The full kline row is stored in the file.
- The latest closed 4h at run time was the same bar (`pin_equals_latest_closed_at_pin_run` is true). Local clock skew was +127 ms. The pin is 20 4h bars after TC10's pin.

**New bars per lens** (every file ends at its lens's last bar closing at or before the pin; 0 gaps, 0 rows past the pin)

| lens | bars added per file | total |
|---|---|---|
| 5m | 954, or 960 for PUMP/SUI/MNT | 16,236 |
| 15m (CLASSIC5) | 318 | 1,590 |
| 1h | 80 | 1,360 |
| 4h | 20 | 340 |
| 12h | 7 | 119 |
| 1d | 4 | 68 |
| 1w | 0 (the week of 09-21 is incomplete) | 0 |
| funding | 10 (8h payers) or 20 (4h payers) | 210 |

**Fetch**
- The fetch phase took 106.8 s; the whole `--all` run took 122 s.
- 200 HTTP requests (193 Binance, 7 Bybit), all status 200. The highest Binance weight used in a minute was 539 of 2,400.
- Every request is a row in `FETCH_LOG.jsonl`. The log had 291 lines when sealed.

**Manifest:** `STAGE_D_MANIFEST.json` sha256 `106cc1f7222bf8fee9cb8c5a77dbc8651dd9169ff4fcc5f0266095f83c71c158`.
- It has every top-level key and file-row key of TC10's manifest, and the fee schedule, pin and contract specs match TC10's schemas the same way. Where TC11 adds keys, they sit alongside TC10's and replace none.
- `panels`, `admission.rows` (all 17 admitted), `complete`, `venues` and `fee_schedule.round_trip_bps_used` (10.0) are all present. Those are the keys the census and panel modules read.
- `fee_schedule.json` adds `maker_bps_per_side` 2.0, read from the README.md:150 sentence and marked as an assumption, with scripts/v3_recompute.py:965 as precedent. MNT gets the same figure, also marked as an assumption. It also adds the charter slippage tier per asset (A 2 / B 5 / C 10 bps per side), sourced from Naiad_Phase0_Charter.md:114 and tierc10_data.py:217-220.

**Fixtures** (transcript first line `as_of_last_closed_4h: 2026-09-25T00:00:00Z`; a second run produced byte-identical output)
- The seven you asked for all passed: F-D11-CLONE, F-D11-PIN, F-D11-PREFIX, F-D11-EDGE, F-D11-DERIVE, F-DET and F-D11-UNTOUCHED.
- I added F-D11-GUARD (the substrate guard) and F-D11-PORT. F-D11-PORT proves 48 ported functions are identical to their `tierc10_data.py` source and that the 9 changed ones are labelled as changed.

**Deviations and why**
- **PRE_STATE covers 124 files,** not the brief's 90: 1d and 1w are included, following the C map §7, so the no-rewrite proof covers them too.
- **The seal covers five records:** AS_OF_PIN, PRE_STATE, CLONE_ATTEST, CONTRACT_SPECS and EDGE_AUDIT, plus the fetch-log head.
- **`--all` seals before it writes the manifest,** so the manifest can verify the seal. The brief listed manifest before seal.
- **`CONTRACT_SPECS.json` was fetched fresh** in TC10's schema. It doubles as the check that all 17 symbols are still trading.
- **Carried from TC10 rather than re-run:** the venue of record is TC10's `VENUE_PROBE.json`, pinned by sha. The `two_token_trap`, `data_spend` and `venue_publications_disagree` sections are copied verbatim from TC10's manifest, and `carried_from_tc10` records its sha. There is no TC11 `DATA_SPEND_AUDIT.json` or `VENUE_PROBE.json`; the census and panel modules read neither.
- **Stricter completeness check:** 1d and 1w must also end at the pin. TC10 let derived lenses pass automatically.
- **Values read from source:** UNSEEN12, the slippage clause and NORMALIZATION_LAW are read out of `tierc10_data.py` rather than retyped.
- **Live cache check is stat only:** size, modification time and inode of its MANIFEST.json, with no sha, because reading the file is forbidden.
- **Two probes are not in the fetch log:** before writing the module I made two unlogged connectivity checks with curl (the Binance clock plus one BTC 4h kline, and Bybit's clock). The manifest discloses them.

**Findings**
- **No incident bars in the new window:** no flat or zero-volume bars among the 19,645 new kline rows.
- **Inherited rows match the venue:** the 94 rows TC10's as-of left out but TC11's includes (5m 16:00–16:25Z on 14 stems, 15m 16:00 and 16:15Z on CLASSIC5) are all equal to the venue's REST bars. They were compared read-only and not refetched into the files (`EDGE_AUDIT.json`).
- **15m vs the three 5m bars it spans (disclosure only):**
  - Price / volume-only mismatches: BTC 10/3 (plus one 15m bar with no complete set of 5m bars, 2019-09-08T17:45Z), ETH 11/5, SOL 5/3, NEAR 8/3, ZEC 14/3.
  - Total: 48 price and 17 volume-only out of 1,138,845 bars compared. None are in TC11's new bars, and the counts match the C map's earlier measurement.
- **pandas sums group volumes with a compensated (Kahan) method.** A plain left-to-right sum differs in the last bit on 792 BTC days, so F-D11-DERIVE's independent loop uses the compensated sum explicitly.
- **ENA funding** shows one historical 8h gap between prints; it was already in TC10's data. All 17 funding tapes carry the 2026-09-25T00:00Z print.
- **The snapshots:** the TC11 clone (`~/.cache/naiad/snapshots/tc11_20260925`, an APFS clone of `tc10_20260921`) re-hashed 176 of 176 files against TC10's record before any write. After the build, the TC10 snapshot still re-hashes to its manifest and TC10's own seal still verifies.
- **The F-DET twins are covered by `.gitignore`:** `.gitignore:288` already ignores `research_outputs/tierc11/**/_det_*/`.

**Files created** (sha256)
- /Users/luis/Naiad/scripts/tierc11_data.py `a080d78605c18bb11479429a287e82031b08aee131d20773245928932def1538`
- /Users/luis/Naiad/scripts/tierc11_data_fixtures.py `71e75105033f90bb38c7931258cb541276df4dc464b9a9b244bbbbafc67db56c`
- /Users/luis/Naiad/research_outputs/tierc11/data/AS_OF_PIN.json `4f609ccfdf2bc61af2e9e2818ff3cd27aea3f88f7637bd73163b3947c977e4bd`
- /Users/luis/Naiad/research_outputs/tierc11/data/CLONE_ATTEST.json `3cbd6ff3bf819031057511427ca282588654588834f6828201ca1401d47cb441`
- /Users/luis/Naiad/research_outputs/tierc11/data/CONTRACT_SPECS.json `74d9d47b7177955237339eb417100581230efbaf13f2701677436df1c74a6b7e`
- /Users/luis/Naiad/research_outputs/tierc11/data/PRE_STATE.json `29361958c3f94bc7d6ff97f27542fc7e5c0cb61db1fab7e6945c8ec7beae37d0`
- /Users/luis/Naiad/research_outputs/tierc11/data/EDGE_AUDIT.json `c1fe3206fb099b01616a932746f6f65127dbef88861064aa49d6f56ba0816f39`
- /Users/luis/Naiad/research_outputs/tierc11/data/FETCH_LOG.jsonl `bf34b4cd9f0f562f91358403a9d91b1d5ea3ed65057da92a781df98385e18ec7`
- /Users/luis/Naiad/research_outputs/tierc11/data/WRITE_ONCE_SEAL.json `055dab8cc11c3bd5b848ea0ee2a1a1a04049233d448a98234c9e9ac2ec9aeaeb`
- /Users/luis/Naiad/research_outputs/tierc11/data/STAGE_D_MANIFEST.json `106cc1f7222bf8fee9cb8c5a77dbc8651dd9169ff4fcc5f0266095f83c71c158`
- /Users/luis/Naiad/research_outputs/tierc11/data/STAGE_D_MANIFEST.md `ce7248ef310e8599d05b44159bf81213cc30bedf98dc8474ce959fc45b47d850`
- /Users/luis/Naiad/research_outputs/tierc11/data/fee_schedule.json `ee15621de529bf357f093d845ebdf746f1583038a3b17a7cb2c353135a715ad3`
- /Users/luis/Naiad/research_outputs/tierc11/data/FIXTURES_DATA.txt `d179770f32db7158e1d01b7bec802dd6cdebe7094850af16b3a6461318cd3e3d`
- /Users/luis/Naiad/research_outputs/tierc11/data/_det_data/seed_{1,20260924}/: three files in each, byte-identical to the filed manifest, markdown and fee schedule (gitignored).
