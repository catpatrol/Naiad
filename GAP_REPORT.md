# GAP_REPORT — v12 Study, Phase V1 (deliverable D4)

Policy: `listing_edge` (gap begins within 24h of the contract's first candle) — expected, accepted. `download_hole` — must be re-fetched (`scripts/census.py --repair`); a hole surviving two independent re-fetch attempts escalates to `exchange_side` — documented, accepted. Phase verdict requires zero unresolved `download_hole` entries.

## Candle gaps

- **BTCUSDT 1m** — missing 1 bar(s), 2019-09-08 19:00:00 → 2019-09-08 19:00:00 — `listing_edge`

## Funding gaps

- **JTOUSDT funding** — missing 1 record(s) on the 4h grid, 2026-06-24 04:00:00 → 2026-06-24 04:00:00 — `exchange_side`
- **TAOUSDT funding** — missing 1 record(s) on the 4h grid, 2026-06-24 04:00:00 → 2026-06-24 04:00:00 — `exchange_side`
- **HYPEUSDT funding** — missing 1 record(s) on the 4h grid, 2026-06-24 04:00:00 → 2026-06-24 04:00:00 — `exchange_side`
- **FARTCOINUSDT funding** — missing 1 record(s) on the 4h grid, 2026-06-24 04:00:00 → 2026-06-24 04:00:00 — `exchange_side`
- **LITUSDT funding** — missing 1 record(s) on the 4h grid, 2026-06-24 04:00:00 → 2026-06-24 04:00:00 — `exchange_side`

## Timestamp-discipline anomalies

(none)
