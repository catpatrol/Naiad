# SPOT_CHECK — v12 Study, Phase V1 (deliverable D5)

**Escalation rule (read first):** compare every row against TradingView. If
ANY price value (O/H/L/C) mismatches on an asset, that asset fails: tell the
builder, which must regenerate a 10-row escalation sheet for that asset
(`python scripts/spot_check.py --escalate SYMBOL`) and investigate before the
phase can pass. Tiny volume differences can occur; prices must match.

How to check a row: open the TradingView symbol given in the row (Binance
USDT-M perpetual, the `.P` symbol), set the row's timeframe, scroll/jump to
the exact UTC open time, hover the candle, compare open/high/low/close/volume.
Make sure your TradingView chart timezone is set to UTC.

No row in this sheet is a lockbox candle (2024-07-01 → 2025-10-05): printing
lockbox OHLCV would violate the seal. Everything before the lockbox is
exploration-classic (VR-1) — pre-2022 candles included; there is no pre-2022
restriction in the v12 Study. Rows 31–33 sample that deep 2020–2021 era so it
gets operator eyes too.

| # | Symbol | TF | Open (UTC) | Open | High | Low | Close | Volume | Era | Pass? |
|--:|---|---|---|---|---|---|---|---|---|---|
| 1 | BTCUSDT | 12h | 2023-12-12 00:00:00 | 41271.1 | 42125.0 | 41202.1 | 41606.7 | 145701.603 | exploration-classic |  |
| 2 | BTCUSDT | 5m | 2026-03-19 00:00:00 | 71202.9 | 71258.9 | 71134.1 | 71224.8 | 651.031 | spent |  |
| 3 | BTCUSDT | 4h | 2023-09-17 08:00:00 | 26482.6 | 26614.3 | 26480.3 | 26553.9 | 18581.011 | exploration-classic |  |
| 4 | ETHUSDT | 4h | 2024-04-30 20:00:00 | 2927.61 | 3027.91 | 2926.44 | 3012.58 | 487374.746 | exploration-classic |  |
| 5 | ETHUSDT | 15m | 2026-02-25 08:30:00 | 1895.34 | 1906.77 | 1895.34 | 1904.88 | 87440.694 | regime-contaminated |  |
| 6 | ETHUSDT | 1h | 2023-12-16 20:00:00 | 2236.04 | 2242.6 | 2233.35 | 2238.79 | 43700.861 | exploration-classic |  |
| 7 | SOLUSDT | 12h | 2023-11-13 12:00:00 | 57.069 | 59.959 | 51.554 | 51.662 | 43052003.0 | exploration-classic |  |
| 8 | SOLUSDT | 1m | 2025-10-29 07:26:00 | 195.87 | 195.87 | 195.79 | 195.81 | 3955.63 | regime-contaminated |  |
| 9 | SOLUSDT | 1h | 2023-07-11 22:00:00 | 21.913 | 22.047 | 21.882 | 22.005 | 1163351.0 | exploration-classic |  |
| 10 | NEARUSDT | 4h | 2022-07-10 00:00:00 | 3.792 | 3.826 | 3.642 | 3.675 | 11447815.0 | exploration-classic |  |
| 11 | NEARUSDT | 5m | 2026-01-28 16:05:00 | 1.462 | 1.463 | 1.458 | 1.461 | 147702.0 | regime-contaminated |  |
| 12 | NEARUSDT | 12h | 2022-10-10 12:00:00 | 3.467 | 3.482 | 3.199 | 3.215 | 29282318.0 | exploration-classic |  |
| 13 | ZECUSDT | 1h | 2023-07-17 09:00:00 | 31.89 | 31.97 | 31.15 | 31.3 | 74649.835 | exploration-classic |  |
| 14 | ZECUSDT | 15m | 2026-02-17 20:30:00 | 285.77 | 287.63 | 284.28 | 287.02 | 7789.847 | regime-contaminated |  |
| 15 | ZECUSDT | 12h | 2023-11-20 00:00:00 | 29.25 | 29.6 | 28.88 | 29.27 | 139915.204 | exploration-classic |  |
| 16 | JTOUSDT | 4h | 2024-03-14 12:00:00 | 3.0333 | 3.0475 | 2.89 | 2.9249 | 13015870.0 | exploration-classic |  |
| 17 | JTOUSDT | 5m | 2026-06-15 10:50:00 | 0.6227 | 0.6293 | 0.6212 | 0.6252 | 424404.0 | regime-contaminated |  |
| 18 | JTOUSDT | 1h | 2024-06-22 13:00:00 | 2.4432 | 2.4476 | 2.4247 | 2.4333 | 478521.0 | exploration-classic |  |
| 19 | TAOUSDT | 4h | 2024-05-18 20:00:00 | 384.89 | 384.94 | 379.58 | 382.27 | 2816.857 | exploration-classic |  |
| 20 | TAOUSDT | 15m | 2026-05-17 11:45:00 | 272.67 | 274.08 | 272.37 | 273.62 | 4680.487 | regime-contaminated |  |
| 21 | TAOUSDT | 12h | 2024-06-22 12:00:00 | 282.57 | 285.33 | 276.38 | 278.87 | 25862.095 | exploration-classic |  |
| 22 | HYPEUSDT | 4h | 2026-04-05 04:00:00 | 35.921 | 35.968 | 35.439 | 35.64 | 963548.71 | regime-contaminated |  |
| 23 | HYPEUSDT | 1h | 2026-01-29 06:00:00 | 31.954 | 33.248 | 31.905 | 32.854 | 1855259.89 | regime-contaminated |  |
| 24 | HYPEUSDT | 15m | 2026-05-16 21:00:00 | 41.874 | 41.955 | 41.68 | 41.739 | 106836.6 | regime-contaminated |  |
| 25 | FARTCOINUSDT | 4h | 2026-05-10 16:00:00 | 0.259 | 0.2689 | 0.2559 | 0.2663 | 48531636.7 | regime-contaminated |  |
| 26 | FARTCOINUSDT | 1h | 2025-12-10 17:00:00 | 0.3616 | 0.3679 | 0.361 | 0.3639 | 16291016.2 | regime-contaminated |  |
| 27 | FARTCOINUSDT | 5m | 2026-04-06 06:35:00 | 0.1703 | 0.1705 | 0.1702 | 0.1703 | 162672.3 | regime-contaminated |  |
| 28 | LITUSDT | 4h | 2025-12-25 12:00:00 | 3.504 | 3.507 | 3.376 | 3.462 | 4628598.4 | regime-contaminated |  |
| 29 | LITUSDT | 1h | 2026-01-25 14:00:00 | 1.741 | 1.742 | 1.691 | 1.706 | 1345797.6 | regime-contaminated |  |
| 30 | LITUSDT | 15m | 2026-03-06 07:15:00 | 1.187 | 1.191 | 1.184 | 1.191 | 66004.1 | regime-contaminated |  |
| 31 | BTCUSDT | 12h | 2020-01-01 00:00:00 | 7189.43 | 7239.74 | 7170.15 | 7192.65 | 27830.403 | exploration-classic |  |
| 32 | ETHUSDT | 12h | 2020-06-01 00:00:00 | 231.55 | 242.52 | 230.61 | 236.07 | 876889.327 | exploration-classic |  |
| 33 | ZECUSDT | 12h | 2021-01-01 00:00:00 | 63.97 | 67.02 | 63.23 | 66.33 | 129534.469 | exploration-classic |  |

## Navigation lines

1. open BINANCE:BTCUSDT.P, 12h, scroll to 2023-12-12 00:00 UTC
2. open BINANCE:BTCUSDT.P, 5m, scroll to 2026-03-19 00:00 UTC
3. open BINANCE:BTCUSDT.P, 4h, scroll to 2023-09-17 08:00 UTC
4. open BINANCE:ETHUSDT.P, 4h, scroll to 2024-04-30 20:00 UTC
5. open BINANCE:ETHUSDT.P, 15m, scroll to 2026-02-25 08:30 UTC
6. open BINANCE:ETHUSDT.P, 1h, scroll to 2023-12-16 20:00 UTC
7. open BINANCE:SOLUSDT.P, 12h, scroll to 2023-11-13 12:00 UTC
8. open BINANCE:SOLUSDT.P, 1m, scroll to 2025-10-29 07:26 UTC
9. open BINANCE:SOLUSDT.P, 1h, scroll to 2023-07-11 22:00 UTC
10. open BINANCE:NEARUSDT.P, 4h, scroll to 2022-07-10 00:00 UTC
11. open BINANCE:NEARUSDT.P, 5m, scroll to 2026-01-28 16:05 UTC
12. open BINANCE:NEARUSDT.P, 12h, scroll to 2022-10-10 12:00 UTC
13. open BINANCE:ZECUSDT.P, 1h, scroll to 2023-07-17 09:00 UTC
14. open BINANCE:ZECUSDT.P, 15m, scroll to 2026-02-17 20:30 UTC
15. open BINANCE:ZECUSDT.P, 12h, scroll to 2023-11-20 00:00 UTC
16. open BINANCE:JTOUSDT.P, 4h, scroll to 2024-03-14 12:00 UTC
17. open BINANCE:JTOUSDT.P, 5m, scroll to 2026-06-15 10:50 UTC
18. open BINANCE:JTOUSDT.P, 1h, scroll to 2024-06-22 13:00 UTC
19. open BINANCE:TAOUSDT.P, 4h, scroll to 2024-05-18 20:00 UTC
20. open BINANCE:TAOUSDT.P, 15m, scroll to 2026-05-17 11:45 UTC
21. open BINANCE:TAOUSDT.P, 12h, scroll to 2024-06-22 12:00 UTC
22. open BINANCE:HYPEUSDT.P, 4h, scroll to 2026-04-05 04:00 UTC
23. open BINANCE:HYPEUSDT.P, 1h, scroll to 2026-01-29 06:00 UTC
24. open BINANCE:HYPEUSDT.P, 15m, scroll to 2026-05-16 21:00 UTC
25. open BINANCE:FARTCOINUSDT.P, 4h, scroll to 2026-05-10 16:00 UTC
26. open BINANCE:FARTCOINUSDT.P, 1h, scroll to 2025-12-10 17:00 UTC
27. open BINANCE:FARTCOINUSDT.P, 5m, scroll to 2026-04-06 06:35 UTC
28. open BINANCE:LITUSDT.P, 4h, scroll to 2025-12-25 12:00 UTC
29. open BINANCE:LITUSDT.P, 1h, scroll to 2026-01-25 14:00 UTC
30. open BINANCE:LITUSDT.P, 15m, scroll to 2026-03-06 07:15 UTC
31. open BINANCE:BTCUSDT.P, 12h, scroll to 2020-01-01 00:00 UTC
32. open BINANCE:ETHUSDT.P, 12h, scroll to 2020-06-01 00:00 UTC
33. open BINANCE:ZECUSDT.P, 12h, scroll to 2021-01-01 00:00 UTC

33 rows: the 30-row base (3 per asset) plus 3 deep pre-2022 exploration-classic
rows (BTC/ETH/ZEC, rows 31–33). No lockbox candles.
