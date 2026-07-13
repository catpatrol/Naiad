# CHANGELOG

## engine 1.0.5 — wake-time campaign-death net (2026-07-13, G-4)

Second latent trading-layer defect surfaced by deep history during V3
anchor-run pre-flight (first observed: BTCUSDT_swing bar 52115, 2020-03-07
16:50Z). The signals arming block re-arms on every exec bar of the
cross-visibility window (Pine-literal, parity-signed — §4.1 "literal,
including re-arming"), so a counter-window V campaign is silently overwritten
one bar after birth: dir flips, campaign id increments, the dying side's stop
clears, and NO X / REGIME / V event is journaled. The trading layer's flatten
triggers were all event-based — the position was stranded (short, no stop,
campaign long) and the step-1 stop-guarantee fired as a TRUE positive.

- **Design ruling of record (operator, 2026-07-13, charter §3 trading
  semantics):** a campaign killed by silent re-arm overwrite exits at the
  NEXT open via the wake-time campaign-death net, exit_reason
  `campaign_died` — uniform with the three event-based death modes (one bar
  of exposure, same fill model). The signal layer is untouched.
- **Alternative logged, not lost:** an entry-filter interpretation
  (V-into-standing-cross never opens a tranche) is REGISTERED as a v12
  named-variant seed — "V-entry-filter" — joining the register alongside
  zoneMemory-5, provisional-Z1-only, and zone-gated CONFIRM adds; to be
  tested against this baseline in a chartered VR-2 slot.
- **Fix (`engine/trading.py`):** new step 0 before the stop-guarantee:
  `if open_tranches and pending_flatten is None and sig.dir[i-1] !=
  open_tranches[0].dir: pending_flatten = "campaign_died"`. Fires ONLY when
  no event-queued flatten exists; failure_x / opposite_cross / v_reversal
  reasons untouched. `campaign_died` is a new value in the existing
  free-form exit_reason journal field — no schema change.
- **Fixture (`fixtures/test_g4_campaign_death_net.py`):** silent re-arm
  scenario (short tranche, dir flips +1 next bar with no event) — raises
  GateViolation on 1.0.4, flattens at the next open with
  exit_reason=campaign_died on 1.0.5. The stop-guarantee floor is
  unweakened: test_orphan_still_hard_fails (G-3 file) still passes — NaN
  stop + no queued flatten + NO direction mismatch remains a hard failure.
- **Scope per ruling:** G-4 only. G-1 and J-1 move to 1.0.6 (post-anchor-run
  touch); no loading or journal-schema paths touched. G-2 unchanged.
- **Parity:** the net provably cannot fire on any signed window — the state
  it detects implied a 1.0.3 GateViolation, and those windows ran clean.
  Pinned-stamp regeneration (1.0.5 code, "1.0.3" stamp) re-verified SHA256
  byte-identity with the signed parity journal (4c734317…ce92de).
- **Version:** ENGINE_VERSION 1.0.4 -> 1.0.5.

## engine 1.0.4 — stop-guarantee death-transition exemption (2026-07-13, G-3)

The step-1 stop-guarantee assert (trading.py) fired spuriously on the one-bar
campaign-death transition: the signals layer clears the dying side's ratchet
ON the death bar (opposite governor cross / X failure / V-reversal), the real
book flattens at the NEXT open (wake step 3a), and the assert ran first and
read the now-NaN ratchet. Latent since 1.0.0 — the parity/spent window never
had a tranche still open when a death arrived; deep history hits it almost
immediately (first observed: BTCUSDT_swing bar 31418, 2019-12-26 20:05Z,
during V3 anchor-run pre-flight; operator-ratified G-3 ruling of 2026-07-13).

- **Fix (`engine/trading.py`, one line):** step-1 guard `if open_tranches:` ->
  `if open_tranches and pending_flatten is None:`. Exempts ONLY the wake whose
  open already carries a queued flatten fill. A NaN stop with NO queued
  flatten remains a hard GateViolation for all death modes — the guarantee is
  narrowed by exactly one bar, not weakened.
- **Fixture (`fixtures/test_g3_death_transition.py`):** the exact sequence
  (open tranche + opposite cross next bar) must flatten at that bar's open
  and must not raise — FAILS on 1.0.3, PASSES on 1.0.4; plus the bound test:
  an orphaned NaN-stop position with no queued flatten still raises.
- **Scope per ruling:** G-3 only. G-1 (code-level lockbox guard on the replay
  path) and J-1 (REJECT stage dataclass default) DEFERRED to 1.0.5 — no
  loading or journal-schema paths touched. G-2 (LIT Litentry cache bars)
  deferred to post-run estate remediation.
- **Parity:** signed parity journal regenerated under the 1.0.4 code with the
  1.0.3 version stamp pinned -> SHA256 byte-identical to the signed value
  (4c734317…ce92de) — the fix changes no strategy behavior. (A verbatim 1.0.4
  rerun re-stamps engine_version and run_id on every row by design, so the
  raw SHA necessarily differs; the pinned-stamp run is the behavior proof.)
- **Version:** ENGINE_VERSION 1.0.3 -> 1.0.4.

## engine 1.0.3 — input-parity conformance (2026-07-12, branch engine-1.0.3-input-parity)

Root cause of the 2026-06-23 parity break (and the May 23/27 divergences): the
engine hardcoded `zone_memory = 5` for 5m exec (cells.py) while the deployed Pine
runs `zoneMemory = 3` (input default, operator-verified on the deployed and v11.3
charts). Bands, EMAs, and signal logic are line-identical to the Pine; the single
constant forked `hadPrimeEp`/`activeZone` state. Parity target is the deployed
chart; the engine conforms — never the reverse.

- **Fix:** `Cell.zone_memory` -> 3 for all mandates (was 5 for 5m). No signal-logic
  change; only the constant differed.
- **Input-parity fixtures (`fixtures/test_i_input_parity.py` + `pine_defaults_manifest.yaml`):**
  every live signal constant (both configs) and `zone_memory` (all mandates)
  asserted against defaults extracted from the .pine; behavioral pins at
  zone_memory=3 — NO PRIME (May 23 16:20), NO grade-C (May 27 12:45), NO CONFIRMs
  (Jun 23 17:00/17:45/20:45). Drift can no longer recur silently.
- **Journal:** mem=5 parity journal ARCHIVED (`research_outputs/parity/journal_mem5_archive/`)
  as the "zoneMemory-5" v12 named-variant seed (18 extra entries, 2 regrades, 4,360
  stop-divergent bars over 9 months). Parity journal REGENERATED at mem=3 (new
  run_id via the version bump); diff vs the validated shadow-at-3 = ZERO.
- **Version:** ENGINE_VERSION 1.0.2 -> 1.0.3.

## engine 1.0.2 — cache no-shrink invariant (2026-07-10, branch engine-1.0.2-noshrink)

Data-side twin of the stop ratchet: a kline or funding cache file can no
longer lose rows through the save path. Closes v12 V1 census open item #3
(the truncating writer). Infrastructure only — no signal, trading, shadow,
or config behavior changed; both consumers (Naiad paper line, v12 Study)
inherit the fix.

- **Incident (2026-07-10):** `parity_pack.py --backfill` stamped the 494-day
  parity window [2025-03-01, 2026-07-08) over the full-history BTCUSDT 5m and
  1h caches. Root cause: three combining defects in `engine/data.py` —
  `exists()`-masked silent-empty load, conditional history merge, and a
  non-atomic whole-file save. Estate already repaired by the census; no cache
  file needed data changes.
- **Fix (`engine/data.py`, klines and funding):**
  - `_load_cache` / `_load_funding` — only `FileNotFoundError` yields an empty
    frame; any other read failure (corrupt file, transient stat/sharing error)
    raises and aborts the run. Silent-empty abolished on both the load path
    and the merge-read inside the save path.
  - `_save_cache` / `_save_funding` — merge rows already durably on disk back
    in regardless of the caller's assembled frame (new rows win at identical
    `open_time`/`funding_time`, `keep="last"` preserved), then land the file
    atomically via a same-directory pid-suffixed temp + `os.replace`. An
    interrupted run cannot truncate or corrupt the destination.
  - `backfill_funding` / `load_funding` routed through the loud-load and
    merge-in-save funding helpers — structural twins of the kline path.
- **No deletion primitive (by design):** the save path can no longer shrink a
  file, for every caller including `census.py --repair`. Genuine row removal
  is out-of-band: delete the file, re-extend via `census.py --extend`.
  Accepted residuals: a concurrent last-writer may drop the *other* writer's
  freshly fetched rows (refetchable, never a shrink below disk); a file
  deleted and recreated via an engine path restarts at the warm-up anchor, not
  the listing (`coverage_ok` vs `data_starts.csv` is the detector).
- **Cost:** one extra parquet read per save — up to a few hundred MB of
  transient memory for full-history 1m majors (~3.6M rows), negligible against
  the accompanying network fetch.
- **Fixtures N1–N5** (`fixtures/test_n_noshrink.py`), synthetic and hermetic
  via `NAIAD_CACHE_DIR`: merge-preserve, loud load, atomic abort, first save,
  funding mirror. Suite 35 → 40 green; existing fixtures untouched.
- `engine_version` 1.0.1 → 1.0.2. The operator owns the merge.

## v12 Study V1 — data census & integrity gate (2026-07-10, branch v12-v1-census)

Engine version unchanged (1.0.1): no signal, trading, shadow, or config
behavior touched — this phase adds data tooling, guards, and fixtures only.

- New `study/` package. `study/loader.py`: the v12 Study's only sanctioned
  candle path — LIT floor 2025-12-23T00:00Z (stricter than the Phase 1 engine
  floor, which stands for Naiad), study right edge 2026-07-07 23:59:59Z,
  lockbox seal (`LockboxViolation` on value reads touching
  2024-07-01 → 2025-10-05 without `integrity_only`), VR-1 partition classes,
  guard-event JSONL in the cache dir. `study/census.py`: deterministic census
  (timestamp-and-bytes only; census.json byte-identical on re-run, retrieval
  dates in a write-once sidecar keyed by content hash).
- Estate completed (D1): BTCUSDT 5m and 1h caches were found truncated to
  2025-03-01 — the committed Phase 1 coverage report shows both backfilled to
  the 2019-09-08 listing, so a later cache write shrank them (open item: find
  and guard that writer). Re-extended from the listing; 60/60 kline and 10/10
  funding series now meet the coverage target.
- Gap census (D4): BTC 1m 1-bar gap on listing day 2019-09-08 —
  `listing_edge`. Five funding records missing at 2026-06-24 04:00 UTC, one
  per 4h-grid symbol (JTO/TAO/HYPE/FARTCOIN/LIT), two REST re-fetch attempts
  each returned nothing — `exchange_side` (same skipped settlement across all
  five). Zero `download_hole` remaining.
- Census finding: funding grids are per-symbol, not uniform 8h as the build
  prompt assumed — BTC/ETH/NEAR/ZEC 8h; JTO/TAO/HYPE/FARTCOIN/LIT 4h; SOL
  shifts 8h→4h→2h→8h across 2022-11-09 → 2022-11-18 (FTX week), documented
  as grid segments in census.json.
- Fixtures F1–F9 (`fixtures/test_v12_census.py`), synthetic and CI-safe;
  suite 26 → 35 green, Phase 1 fixtures untouched.
- Artifacts at repo root: `census.json` (manifest of record for the loader
  guards), `DATA_CENSUS.md`, `GAP_REPORT.md`, `SPOT_CHECK.md` (operator
  sheet, 30 rows, no lockbox candles, exploration rows sampled from 2022-01-01
  onward for TradingView reachability — pre-2022 is exploration-classic per
  VR-1, not sealed). Sidecars in `research_outputs/census/`. Ledger block
  appended byte-for-byte (D6).
  (Correction, reviewer finding 2026-07-11: the original wording called
  pre-2022 a "sealed retro holdout" — wrong for the v12 Study, where pre-2022
  is exploration-classic (VR-1). No pre-2022 restriction exists in the loader
  or study code; census.json has no such partition. SPOT_CHECK.md now carries
  33 rows — the 30-row base plus 3 curated deep pre-2022 rows (BTC/ETH/ZEC);
  the generator's 2022-01-01 window floor is retained only for TradingView
  reachability of mid-timeframe auto rows.)

## engine 1.0.1 — reject subkeys carry the signal family (2026-07-10, pre-collector)

- Trade-reject journal subkeys now include the signal family:
  `trade_{kind}_{family}` with family ∈ {prime, confirm, v} — e.g.
  `trade_ADD_prime` vs `trade_ADD_confirm`. Same-bar rejects of different
  families no longer share a journal key, closing the 1.0.0 caveat where the
  idempotent merge silently dropped one row (reviewer-confirmed lower-bound
  reject counts). Fill-time rejects inherit the family from their pending
  entry.
- New fixture **F8b**: a synthetic same-bar PRIME-add + CONFIRM-add
  multi-reject scenario must persist BOTH rows under distinct subkeys, and
  the summary row count must equal the on-disk line count.
- `engine_version` 1.0.0 → 1.0.1: every `run_id` changes (expected —
  reviewer re-anchors on the fresh packet). No signal, trading, shadow, or
  config behavior changed; journal deltas verified field-by-field to be
  limited to `run_id` values, `engine_version` values, REJECT `tranche_id`
  subkeys, and the one restored row (2026-07-02T20:00 `max_tranches`).
- **Operational rule learned while regenerating:** a key-schema change must
  be regenerated into CLEAN journal files, never merged — the idempotent
  writer replaces rows by key, so rows under retired keys are never
  re-emitted and linger as stale duplicates (observed: 373 stale 1.0.0
  reject rows before the wipe). Applies to any future data-branch
  migration; harmless today because the collector is still off.

## engine 1.0.0 — reviewer ticket D-1..D-3 (2026-07-10, docs + instrumentation)

No version bump: the reviewer's byte-identity constraint pins `run_id`
(= hash of engine_version + args), so a bump would rewrite every row. The
only journal bytes that change are the two HALT rows (D-2, sanctioned).

- **D-1** — replay summary `rows`/`journal_sha256` are now re-read from the
  PERSISTED files after writing, never from the in-memory stream. Documented
  formula (README, packet MANIFEST, `engine/journal.py:files_sha256`):
  sha256 over the byte concatenation of the run's monthly files in
  chronological (filename) order; rows = newline count. New fixture **F1b**
  recomputes both via an independent code path.
  **Root cause of the phantom 1503rd row:** at 2026-07-02T20:00 a PRIME add
  (rejected `max_tranches`) and a CONFIRM add (rejected `not_positioned`)
  fired on the same bar; both REJECT rows map to the same journal key
  `(cell, REJECT, ts, "trade_ADD")`, so the idempotent merge keeps the
  later one. The summary previously counted the pre-merge stream (1503) and
  salted the hash with filenames — neither matched disk. The key collision
  itself is left as-is under this ticket's byte-identity constraint;
  candidate refinement for the next engine version: make trade-reject
  subkeys carry the signal family (`trade_ADD_prime` vs
  `trade_ADD_confirm`).
- **D-2** — HALT rows no longer put a bare date in `reject_reason`; the
  value is namespaced: `halt_day:2026-06-19` / `halt_week:2026-Wnn`.
  Schema note: `reject_reason` on HALT rows = `halt_<scope>:<calendar key>`.
  Q18 in the dry-run autopsy updated. All other row bytes unchanged.
- **D-3** — the session packet now includes `Naiad_Phase0_Charter.md`,
  `Naiad_Phase1_Build_Prompt.md`, `LEDGER.md`, and per-file sha256 digests
  plus the journal hash formula in MANIFEST.txt.

## engine 1.0.0 — Phase 1 initial build (2026-07-09, branch phase-1)

- Literal Python port of SS Cascade v11.0.2 (`engine/signals.py`): governor
  arming tiers, zones/tags/episodes, PRIME/CONFIRM/C/V/TPW/CLUSTER/X, grades
  A+/A/B/C/V, sniper leg + `retr`, ratcheting stop; confirmed-HTF visibility
  mapping replicating Pine's `expr[1] + lookahead_on` idiom exactly.
- naiad_v0 trading layer (`engine/trading.py`): per-cell $10k paper book,
  1R = 0.5% equity, charter §3.4 sizing table, per-cell −2R/day −4R/week
  halts, fees 5 bps/side, tiered slippage, historical funding accrual,
  next-bar-open fills, stops-as-orders, in-path gate assertions.
- Shadow lines (`engine/shadows.py`): entry variant, structure ladders,
  stop anchors, sizing counterfactuals, candidate exits X-A..X-D, funnel log.
- Idempotent canonical journal (`engine/journal.py`), deterministic run ids.
- Data layer (`engine/data.py`): bulk zips + REST top-up, integrity checks,
  first-candle detection, LIT hard floor asserted in the loader.
- Scripts: backfill / first_candles / replay / tick (fixed-epoch re-replay) /
  packet; dormant hourly collector workflow (schedule commented out).
- Fixture suite F1–F8 (`fixtures/`), CI workflow.
- Config divergence flagged: `v_births_provisional` — Pine v11.0.2 clears
  campCounter on V; charter §3.2 says V births a provisional campaign.
  v11_faithful follows the Pine, naiad_v0 follows the charter.
- Fix found by fixture F8 during the dry-run autopsy: Binance funding
  timestamps jitter a few ms past the hour, so exact-match lookup accrued
  zero funding; funding times now floor to the hour (engine/trading.py).
- Fix found during the smoke replay: the paper book traded through the
  warm-up period; run_trading now starts flat at the window start.
