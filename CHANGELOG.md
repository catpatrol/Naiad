# CHANGELOG

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
