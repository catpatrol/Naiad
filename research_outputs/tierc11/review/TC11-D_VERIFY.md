# TC11-D independent verification (2026-09-25)

**TC11-D independent verification: the data is correct. There are 3 medium and 5 low defects, all in fixture coverage or record-keeping. None changes any number the builder reported.**

## (1) Fixture re-run
I ran `/Users/luis/Naiad/scripts/tierc11_data_fixtures.py` with `NAIAD_CACHE_DIR` set to the tc11 snapshot.
- **Tally:** 9 GREEN, 0 RED. Break legs RED 9/9, real legs GREEN 9/9. Exit 0.
- **Transcript:** `FIXTURES_DATA.txt` came out byte-identical (sha d179770f… unchanged, no `_rerun.txt` written).
- **F-DET twins:** both rebuilt copies are byte-identical to the filed manifest (106cc1f7…), md (ce7248ef…) and fee schedule (ee15621d…).
- Every file in `research_outputs/tierc11/data/` still has the sha in the builder's report.

## (2) My own checks (no module imports)
- **Random draw:** seed 20260925 picked LTCUSDT, ZECUSDT and BNBUSDT. I also checked MNTUSDT_BYBIT, PUMPUSDT and BTCUSDT (Bybit, 960-bar 5m, 4h funding, BTC 15m). That is 42 files across every lens plus funding.
- **Per-file results:**
  - The last open equals the lens's last bar closing at or before 2026-09-25T00:00Z. The 1w file ends at the week of 09-14.
  - No gaps, duplicates, off-grid stamps or rows past the pin.
  - The first new row is exactly one step after the TC10 edge.
  - The first N rows match the TC10 snapshot file bit for bit on every column, with identical dtypes.
  - Each TC10 source file's sha equals TC10's manifest.
  - OHLC values are coherent and finite.
  - Funding ends on the 00:00Z print, with nothing past the pin plus 60 s.
- **Full sweep of all 124 in-scope files:** no faults. Rows added match the builder's table exactly: 5m 954/960 (16,236), 15m 318 (1,590), 1h 80, 4h 20, 12h 7, 1d 4, 1w 0, funding 10/20 (210).
- **Records:**
  - All 124 PRE_STATE file shas equal TC10's manifest.
  - The TC11 seal verifies, and all 124 manifest row shas match the files on disk.
  - The fetch log has 291 lines: 200 HTTP requests, all status 200, maximum Binance weight 539. It has no zero-bar chunks. The 5m fetch started at 16:30Z for the 14 Binance stems and 16:00Z for PUMP and MNT.

## (3) Sabotage legs: defects
1. **MEDIUM — the F-DET break leg is tautological** (`tierc11_data_fixtures.py:654,656-657`).
   - The plant compares an edited copy with the original using `==` inside the lambda. It can only stay GREEN if the text it edits is missing, and it never runs the real leg's comparison (`:666-673`).
   - Fix: move `:666-673` into `det_findings(outs, filed) -> list[str]` and call it from `det_real`. In `det_break`, feed it four cases that must each come back non-empty: one twin altered, both twins equal but different from the filed file, one twin exiting 1, one twin missing a file.
2. **MEDIUM — the write-time barrier has no break leg.** `_assert_bound()` (`tierc11_data.py:435-441`) is what stops `_save_cache`, `backfill_funding` and `_save_funding` from writing to the live cache. F-D11-GUARD (`fixtures:206-235`) only breaks the import-time `guard_substrate`.
   - Fix: add a plant that temporarily sets `os.environ["NAIAD_CACHE_DIR"]` to a temp directory, requires `D._assert_bound()` to HALT, and restores the variable in `finally`.
   - Never point it at the live cache: `engine/data.py:47` runs `mkdir` on whatever path the variable names.
3. **MEDIUM — the live-cache half of F-D11-UNTOUCHED cannot fail for the build.**
   - Its baseline is taken when the fixture starts (`fixtures:787`), so it only covers the fixture run. The fixtures never write the live cache anyway.
   - It stats only `MANIFEST.json`, which `_save_cache` and `_save_funding` never touch; they replace `klines/*.parquet` and `funding/*.parquet`.
   - This contradicts the fixture's own ban on "a check whose claim is not the design's claim" (`fixtures:36-37`), and it goes RED for no TC11 reason if the oracle lane rewrites that file during a run.
   - Fix: change the wording at `fixtures:33-35,765-768,728-731` to "across this fixture run only". Rest the build's no-touch claim on the guard plus `_assert_bound`, which needs defect 2's break leg.
   - Also: `live_cache_touched: False` (`tierc11_data.py:2103`) is typed in, not measured. Relabel it "by construction (guard + _assert_bound)".
4. **LOW — the "not a 4h close" plant is caught by the wrong check** (`fixtures:386,391`).
   - The contract-value check (`tierc11_data.py:639-640`) fires before the modulus check (`:641-642`); the transcript shows "close 1790294700000 != the contract's pin". Deleting the modulus check would leave the fixture GREEN.
   - The real leg's own checks at `fixtures:402-408` (the pin ms and ISO string, the venue-kline arithmetic, the seal sha) are never broken.
   - Fix: plant under `mutated(D, "PIN_CLOSE_MS", c+300_000)` with the open adjusted to match. Move `:402-408` into `pin_record_findings(pin, seal)` and plant a kline row whose closeTime (k[6]) is off by one, plus a wrong seal sha.
5. **LOW — `plants()` never checks which detector fired** (`fixtures:132-151`). Any non-empty result counts as caught. For example, "a bar appended past the pin" is caught by the last-open check, so the past-pin check at `:490-491` is never proven. Fix: give each plant an expected substring and count it caught only when a finding contains it.
6. **LOW — the funding half of F-D11-EDGE has no break leg.** The real leg checks funding (`fixtures:524-530`) and the fixture text claims it (`:26-27,757-758`), but `edge_break` (`:495-506`) plants only BTCUSDT_4h. Fix: add `funding_edge_findings(root, rel)` using `D.funding_coverage(stem, PIN_MS, root)`, which already accepts a root, and plant a temp copy missing the 00:00Z print.
7. **LOW — fixture scope comes from module constants.** The header (`fixtures:75`) says fixtures use their own typed objects, never the module's. Yet F-D11-EDGE loops over `D.scope_paths()` (`:513,531`) and F-D11-DERIVE over `D.PANEL17` (`:613`). The typed 124 in PREFIX guards the count, not which files are in it. Fix: type the 17 stems and the lens map in the fixture and assert that `D.scope_paths()` equals them.
8. **LOW — the fetch-time "latest closed 4h" is never saved.**
   - It is only printed to stdout (`tierc11_data.py:2436-2438`). `LOG_LINES` (`:338-344`) is never written, and the fetch log's clock row (line 3) has no serverTime.
   - L-0.1 says "the latest close at fetch time is printed beside it". The only saved value is the one from the pin run.
   - Fix: in `run_all`, call `_fetch_log(OUT, {"kind":"clock","venue_server_time_ms":srv,"latest_closed_4h_close_ms":latest})` before the seal.

The remaining legs (GUARD, PORT, CLONE, PREFIX, EDGE's kline half, DERIVE, and UNTOUCHED's TC10 half) break the thing they test and would catch their fault. None compares an object with itself. PORT has 57 entries: 48 identical to their TC10 source and 9 marked as changed, and every "ported from" comment maps to one of them.

## (4) Compatibility with the TC10 readers: no gaps
- **`tierc10_census.py`** reads `AS_OF_PIN.as_of_last_closed_4h_close_ms` (1790294400000, a 4h multiple), `panels.{CLASSIC5, UNSEEN_admitted_stems, PANEL17_stems}` (identical to TC10), and `fee_schedule.assets[].{stem, round_trip_bps_used}` (10.0 for all 17).
- **`tierc10_panel.py`** reads `complete` (True) and `admission.rows[].{asset, stem, admitted, venue}` (identical to TC10).
- **Other TC10 modules:**
  - `tierc10_brk.py:3805-3811` reads `taker_bps_side_used`, which is 5.0.
  - `tierc10_score.py:855,1214` reads `venues[].{stem, asset}`, identical to TC10.
- **Key sets:**
  - Every TC10 key at every level is present in TC11: AS_OF_PIN 11 of 11; manifest top level 32 of 32; file rows native 34/34, derived 35/35, funding 27/27; fee schedule top level 8/8, per asset 18/18; CONTRACT_SPECS, seal and PRE_STATE all complete.
  - No value types changed.
  - Every TC10 fee-row value is unchanged except the refreshed `funding_*` keys.
- No TC10 consumer loops over `files[]`, so the extra 15m rows are safe.
- **Note for the later re-root step, not a TC11-D defect:** `tierc10_census.py:520` hard-codes the source label `research_outputs/tierc10/data/fee_schedule.json`. Once `C.STAGE_D` points at TC11, the toll value is correct but its label names TC10's file.

## (5) Protected paths are untouched
- **Git:** the only modified tracked TC10 path is `research_outputs/tierc10/close/FIXTURES_CLOSE_ledger_append_root.txt`. Its mtime is 2026-09-23T11:36:51-03:00, before the build, and it was already modified when this session started.
- **Timestamps:** nothing under `research_outputs/tierc10/`, `scripts/tierc10_*`, `exchange/status/LEDGER*` or the TC10 snapshot (files or directories) changed after 2026-09-24T20:00-03.
- **TC10 snapshot:**
  - It has 176 files; 175 are pinned by TC10's manifest, the other is `MANIFEST.json`.
  - 12 randomly chosen files, plus the 42 source files from my asset checks, re-hash to TC10's manifest.
  - TC10's own seal verifies: its three records and the sealed fetch-log prefix.
- **TC11 snapshot:** 107 files changed, exactly 17 × {5m, 1h, 4h, 12h, 1d}, plus 5 × 15m, plus 17 funding. All 17 1w files are untouched.
- **Live cache:** I did not read it, per the hard rule. The only evidence is the fixture's stat check, which covers only the fixture run (defect 3).

Scratch scripts (read-only): `/private/tmp/claude-501/-Users-luis-Naiad/fa1cb7a0-1726-4409-8f61-bc58ab09398a/scratchpad/indep_check.py` and `schema_check.py`.
