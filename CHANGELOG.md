# CHANGELOG

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
