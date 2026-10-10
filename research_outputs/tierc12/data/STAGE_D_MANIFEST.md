# TIER-C12 · STAGE TC12-D — THE SUBSTRATE TOP-UP (STAGE_D_MANIFEST)

- **AS_OF** 2026-10-08T20:00:00Z (close ms 1791489600000) · seed 20261008 · snapshot `/Users/luis/.cache/naiad/snapshots/tc12_20261008` · complete **True**
- Clone: 176 files, all equal to TC11's record: True · prefix attestation all_ok True (124 files) · seal all_ok True · venue table / probe / TC11 manifest agree: True
- Panel: 17 admitted — BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT ENAUSDT PUMPUSDT HYPEUSDT MNTUSDT_BYBIT SUIUSDT LTCUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT
- Mirror: see data/MIRROR_ATTEST.json — a provenance record outside the determinism set; the mirror's status is not carried here

## The "maker-bps" pin

- `PIN ["maker-bps"] BINANCE_USDTM 2.0 bps/side (4.0 round trip) · ON FILE — NOT RE-CONFIRMED · https://www.binance.com/en/fee/futureFee · retrieved — · body sha —`
- `PIN ["maker-bps"] BYBIT_V5_LINEAR 2.0 bps/side (4.0 round trip) · ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file · https://www.bybit.com/en/help-center/article/Trading-Fee-Structure · retrieved — · body sha —`
- `X assumed 2.0 bps/side (4.0 round trip); differs: BINANCE_USDTM: False, BYBIT_V5_LINEAR: False`

| venue | status | url | retrieval attempted | retrieved | body sha256 |
|---|---|---|---|---|---|
| BINANCE_USDTM | UNRETRIEVABLE (http_202) | https://www.binance.com/en/fee/futureFee | 2026-10-09 | — | — |
| BYBIT_V5_LINEAR | UNRETRIEVABLE (http_403) | https://www.bybit.com/en/help-center/article/Trading-Fee-Structure | 2026-10-09 | — | — |

## Last closed bar per lens at the pin

| lens | open | close |
|---|---|---|
| 5m | 2026-10-08T19:55:00Z | 2026-10-08T20:00:00Z |
| 15m | 2026-10-08T19:45:00Z | 2026-10-08T20:00:00Z |
| 1h | 2026-10-08T19:00:00Z | 2026-10-08T20:00:00Z |
| 4h | 2026-10-08T16:00:00Z | 2026-10-08T20:00:00Z |
| 12h | 2026-10-08T00:00:00Z | 2026-10-08T12:00:00Z |
| 1d | 2026-10-07T00:00:00Z | 2026-10-08T00:00:00Z |
| 1w | 2026-09-28T00:00:00Z | 2026-10-05T00:00:00Z |

## Rows added by TC12 per lens (every file whole)

| lens | files | rows added | per stem |
|---|---|---|---|
| 5m | 17 | 67728 | BTCUSDT:3984 ETHUSDT:3984 SOLUSDT:3984 NEARUSDT:3984 ZECUSDT:3984 ENAUSDT:3984 PUMPUSDT:3984 HYPEUSDT:3984 MNTUSDT_BYBIT:3984 SUIUSDT:3984 LTCUSDT:3984 XMRUSDT:3984 BNBUSDT:3984 UNIUSDT:3984 1000PEPEUSDT:3984 DOGEUSDT:3984 1000BONKUSDT:3984 |
| 15m | 5 | 6640 | BTCUSDT:1328 ETHUSDT:1328 SOLUSDT:1328 NEARUSDT:1328 ZECUSDT:1328 |
| 1h | 17 | 5644 | BTCUSDT:332 ETHUSDT:332 SOLUSDT:332 NEARUSDT:332 ZECUSDT:332 ENAUSDT:332 PUMPUSDT:332 HYPEUSDT:332 MNTUSDT_BYBIT:332 SUIUSDT:332 LTCUSDT:332 XMRUSDT:332 BNBUSDT:332 UNIUSDT:332 1000PEPEUSDT:332 DOGEUSDT:332 1000BONKUSDT:332 |
| 4h | 17 | 1411 | BTCUSDT:83 ETHUSDT:83 SOLUSDT:83 NEARUSDT:83 ZECUSDT:83 ENAUSDT:83 PUMPUSDT:83 HYPEUSDT:83 MNTUSDT_BYBIT:83 SUIUSDT:83 LTCUSDT:83 XMRUSDT:83 BNBUSDT:83 UNIUSDT:83 1000PEPEUSDT:83 DOGEUSDT:83 1000BONKUSDT:83 |
| 12h | 17 | 459 | BTCUSDT:27 ETHUSDT:27 SOLUSDT:27 NEARUSDT:27 ZECUSDT:27 ENAUSDT:27 PUMPUSDT:27 HYPEUSDT:27 MNTUSDT_BYBIT:27 SUIUSDT:27 LTCUSDT:27 XMRUSDT:27 BNBUSDT:27 UNIUSDT:27 1000PEPEUSDT:27 DOGEUSDT:27 1000BONKUSDT:27 |
| 1d | 17 | 221 | BTCUSDT:13 ETHUSDT:13 SOLUSDT:13 NEARUSDT:13 ZECUSDT:13 ENAUSDT:13 PUMPUSDT:13 HYPEUSDT:13 MNTUSDT_BYBIT:13 SUIUSDT:13 LTCUSDT:13 XMRUSDT:13 BNBUSDT:13 UNIUSDT:13 1000PEPEUSDT:13 DOGEUSDT:13 1000BONKUSDT:13 |
| 1w | 17 | 34 | BTCUSDT:2 ETHUSDT:2 SOLUSDT:2 NEARUSDT:2 ZECUSDT:2 ENAUSDT:2 PUMPUSDT:2 HYPEUSDT:2 MNTUSDT_BYBIT:2 SUIUSDT:2 LTCUSDT:2 XMRUSDT:2 BNBUSDT:2 UNIUSDT:2 1000PEPEUSDT:2 DOGEUSDT:2 1000BONKUSDT:2 |
| funding | 17 | 865 | BTCUSDT:41 ETHUSDT:41 SOLUSDT:41 NEARUSDT:41 ZECUSDT:41 ENAUSDT:83 PUMPUSDT:83 HYPEUSDT:83 MNTUSDT_BYBIT:41 SUIUSDT:41 LTCUSDT:41 XMRUSDT:41 BNBUSDT:41 UNIUSDT:41 1000PEPEUSDT:41 DOGEUSDT:41 1000BONKUSDT:83 |

## Files

| path | rows | first open | last open | gaps | complete | sha256 |
|---|---|---|---|---|---|---|
| klines/BTCUSDT_5m.parquet | 745081 | 2019-09-08T17:55:00Z | 2026-10-08T19:55:00Z | 0 | True | `045bf6cf45d15924…` |
| klines/BTCUSDT_15m.parquet | 248361 | 2019-09-08T17:45:00Z | 2026-10-08T19:45:00Z | 0 | True | `ee52dac31f16c651…` |
| klines/BTCUSDT_1h.parquet | 62091 | 2019-09-08T17:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `a9e7af42ac4c3b66…` |
| klines/BTCUSDT_4h.parquet | 15523 | 2019-09-08T16:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `b22a2057e19f5da1…` |
| klines/BTCUSDT_12h.parquet | 5174 | 2019-09-08T12:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `c100b4de5dd4c970…` |
| klines/BTCUSDT_1d.parquet | 2586 | 2019-09-09T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `a31a34c032509ef5…` |
| klines/BTCUSDT_1w.parquet | 369 | 2019-09-09T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `a4ff9ee297b07093…` |
| funding/BTCUSDT.parquet | 7757 | 2019-09-10T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `48de999daae78c9c…` |
| klines/ETHUSDT_5m.parquet | 722163 | 2019-11-27T07:45:00Z | 2026-10-08T19:55:00Z | 0 | True | `5d48a50541e27b68…` |
| klines/ETHUSDT_15m.parquet | 240721 | 2019-11-27T07:45:00Z | 2026-10-08T19:45:00Z | 0 | True | `ba8e6540ff041ef2…` |
| klines/ETHUSDT_1h.parquet | 60181 | 2019-11-27T07:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `0ee0488dcd1c93df…` |
| klines/ETHUSDT_4h.parquet | 15046 | 2019-11-27T04:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `1486f6b8fa9adcfe…` |
| klines/ETHUSDT_12h.parquet | 5015 | 2019-11-27T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `7591d60929462e1e…` |
| klines/ETHUSDT_1d.parquet | 2506 | 2019-11-28T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `edf22fc8b8413ee9…` |
| klines/ETHUSDT_1w.parquet | 357 | 2019-12-02T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `f7752db56adf9b0b…` |
| funding/ETHUSDT.parquet | 7523 | 2019-11-27T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `ad1f94f0a2d42295…` |
| klines/SOLUSDT_5m.parquet | 638076 | 2020-09-14T07:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `3519babec50234c5…` |
| klines/SOLUSDT_15m.parquet | 212692 | 2020-09-14T07:00:00Z | 2026-10-08T19:45:00Z | 0 | True | `da0bb6c994385d70…` |
| klines/SOLUSDT_1h.parquet | 53173 | 2020-09-14T07:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `40105a51c27cbb3a…` |
| klines/SOLUSDT_4h.parquet | 13294 | 2020-09-14T04:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `597f91f54c362960…` |
| klines/SOLUSDT_12h.parquet | 4431 | 2020-09-14T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `dafe64d7ac541ae7…` |
| klines/SOLUSDT_1d.parquet | 2214 | 2020-09-15T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `ef22899076dbd659…` |
| klines/SOLUSDT_1w.parquet | 315 | 2020-09-21T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `38a6667ee0d1ddb8…` |
| funding/SOLUSDT.parquet | 6722 | 2020-09-14T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `e0ef738ee49d1efa…` |
| klines/NEARUSDT_5m.parquet | 629136 | 2020-10-15T08:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `0798a6ed44581dcf…` |
| klines/NEARUSDT_15m.parquet | 209712 | 2020-10-15T08:00:00Z | 2026-10-08T19:45:00Z | 0 | True | `c8ef91b0cf5900bc…` |
| klines/NEARUSDT_1h.parquet | 52428 | 2020-10-15T08:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `87f7b417728a2557…` |
| klines/NEARUSDT_4h.parquet | 13107 | 2020-10-15T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `aacdfe91183e004c…` |
| klines/NEARUSDT_12h.parquet | 4369 | 2020-10-15T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `35f7ee5ae8ec2aa0…` |
| klines/NEARUSDT_1d.parquet | 2183 | 2020-10-16T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `b38404d79d12cd0b…` |
| klines/NEARUSDT_1w.parquet | 311 | 2020-10-19T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `e9752678292ae2f9…` |
| funding/NEARUSDT.parquet | 6554 | 2020-10-15T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `ff72209a547a64c5…` |
| klines/ZECUSDT_5m.parquet | 702000 | 2020-02-05T08:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `e170dfef538d6964…` |
| klines/ZECUSDT_15m.parquet | 234000 | 2020-02-05T08:00:00Z | 2026-10-08T19:45:00Z | 0 | True | `ebd1bf5d1fd624d1…` |
| klines/ZECUSDT_1h.parquet | 58500 | 2020-02-05T08:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `2d810bb621546f2c…` |
| klines/ZECUSDT_4h.parquet | 14625 | 2020-02-05T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `0bfa930b527c0b38…` |
| klines/ZECUSDT_12h.parquet | 4875 | 2020-02-05T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `41009b9c7c5dc5f4…` |
| klines/ZECUSDT_1d.parquet | 2436 | 2020-02-06T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `9fc8925c075ccfd7…` |
| klines/ZECUSDT_1w.parquet | 347 | 2020-02-10T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `68dce507c0b186cd…` |
| funding/ZECUSDT.parquet | 7313 | 2020-02-05T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `8b1b5ac99efda2c4…` |
| klines/ENAUSDT_5m.parquet | 264762 | 2024-04-02T12:30:00Z | 2026-10-08T19:55:00Z | 0 | True | `79ac7d4f77d3e581…` |
| klines/ENAUSDT_1h.parquet | 22064 | 2024-04-02T12:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `5c5063e6122308d8…` |
| klines/ENAUSDT_4h.parquet | 5516 | 2024-04-02T12:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `1faa9df1fba7a9fe…` |
| klines/ENAUSDT_12h.parquet | 1838 | 2024-04-02T12:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `af26f23cf38d64b5…` |
| klines/ENAUSDT_1d.parquet | 918 | 2024-04-03T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `b7bc6d888a1a25ae…` |
| klines/ENAUSDT_1w.parquet | 130 | 2024-04-08T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `7472c2427948640b…` |
| funding/ENAUSDT.parquet | 5515 | 2024-04-02T16:00:00Z | 2026-10-08T20:00:00Z | — | True | `d1ffc6883ae5d2ca…` |
| klines/PUMPUSDT_5m.parquet | 131190 | 2025-07-10T07:30:00Z | 2026-10-08T19:55:00Z | 0 | True | `750c3a1b98040205…` |
| klines/PUMPUSDT_1h.parquet | 10933 | 2025-07-10T07:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `3999cdd4bff650d1…` |
| klines/PUMPUSDT_4h.parquet | 2734 | 2025-07-10T04:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `b5c2cd4c5433e452…` |
| klines/PUMPUSDT_12h.parquet | 911 | 2025-07-10T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `ef13bcd3d290b47b…` |
| klines/PUMPUSDT_1d.parquet | 454 | 2025-07-11T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `a45699e4b24b74f0…` |
| klines/PUMPUSDT_1w.parquet | 64 | 2025-07-14T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `ba6c0cfd5bd242ee…` |
| funding/PUMPUSDT.parquet | 2733 | 2025-07-10T08:00:00Z | 2026-10-08T20:00:00Z | — | True | `46fdea7f4555a5f7…` |
| klines/HYPEUSDT_5m.parquet | 142962 | 2025-05-30T10:30:00Z | 2026-10-08T19:55:00Z | 0 | True | `121e920a5d17bcd6…` |
| klines/HYPEUSDT_1h.parquet | 11914 | 2025-05-30T10:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `3b242abd674548ae…` |
| klines/HYPEUSDT_4h.parquet | 2979 | 2025-05-30T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `5190dad15682170f…` |
| klines/HYPEUSDT_12h.parquet | 993 | 2025-05-30T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `7c6f5212aaf37643…` |
| klines/HYPEUSDT_1d.parquet | 495 | 2025-05-31T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `6e1b7424c51239fa…` |
| klines/HYPEUSDT_1w.parquet | 70 | 2025-06-02T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `3b153bbd3d628fe0…` |
| funding/HYPEUSDT.parquet | 2978 | 2025-05-30T12:00:00Z | 2026-10-08T20:00:00Z | — | True | `51eb825256b36e2e…` |
| klines/MNTUSDT_BYBIT_5m.parquet | 317537 | 2023-10-02T06:35:00Z | 2026-10-08T19:55:00Z | 0 | True | `72b039039b5f869e…` |
| klines/MNTUSDT_BYBIT_1h.parquet | 26462 | 2023-10-02T06:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `84f58f1653832327…` |
| klines/MNTUSDT_BYBIT_4h.parquet | 6616 | 2023-10-02T04:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `1cda01e4953bdb87…` |
| klines/MNTUSDT_BYBIT_12h.parquet | 2205 | 2023-10-02T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `cb98bc1d45028bde…` |
| klines/MNTUSDT_BYBIT_1d.parquet | 1101 | 2023-10-03T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `26997f236b1f1efc…` |
| klines/MNTUSDT_BYBIT_1w.parquet | 156 | 2023-10-09T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `af6e7dbf02333429…` |
| funding/MNTUSDT_BYBIT.parquet | 3309 | 2023-10-02T00:00:00Z | 2026-10-08T16:00:00Z | — | True | `a9a02ad58a3cd0de…` |
| klines/SUIUSDT_5m.parquet | 361200 | 2023-05-03T16:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `f832c2af0e466a42…` |
| klines/SUIUSDT_1h.parquet | 30100 | 2023-05-03T16:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `adac39a4605b5be2…` |
| klines/SUIUSDT_4h.parquet | 7525 | 2023-05-03T16:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `01d1de2c8a633d6e…` |
| klines/SUIUSDT_12h.parquet | 2508 | 2023-05-03T12:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `b93a4d61475a3021…` |
| klines/SUIUSDT_1d.parquet | 1253 | 2023-05-04T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `17b55d6d433eccb4…` |
| klines/SUIUSDT_1w.parquet | 178 | 2023-05-08T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `39a97c1506afac7b…` |
| funding/SUIUSDT.parquet | 3763 | 2023-05-03T16:00:00Z | 2026-10-08T16:00:00Z | — | True | `f3323e09aa7d55af…` |
| klines/LTCUSDT_5m.parquet | 709775 | 2020-01-09T08:05:00Z | 2026-10-08T19:55:00Z | 0 | True | `d7770242070fe069…` |
| klines/LTCUSDT_1h.parquet | 59148 | 2020-01-09T08:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `4b00410e1811297e…` |
| klines/LTCUSDT_4h.parquet | 14787 | 2020-01-09T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `c9c748ebe9e9924e…` |
| klines/LTCUSDT_12h.parquet | 4929 | 2020-01-09T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `1809fdc7fa4581f7…` |
| klines/LTCUSDT_1d.parquet | 2463 | 2020-01-10T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `03c154d34dbddbb4…` |
| klines/LTCUSDT_1w.parquet | 351 | 2020-01-13T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `435146aad8a8a80a…` |
| funding/LTCUSDT.parquet | 7394 | 2020-01-09T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `ebfeb660dedb9d3a…` |
| klines/XMRUSDT_5m.parquet | 702576 | 2020-02-03T08:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `229194aa3a2d5164…` |
| klines/XMRUSDT_1h.parquet | 58548 | 2020-02-03T08:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `1b2f6410f9b73810…` |
| klines/XMRUSDT_4h.parquet | 14637 | 2020-02-03T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `77f5e1582a070c0b…` |
| klines/XMRUSDT_12h.parquet | 4879 | 2020-02-03T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `91db678d52b55df8…` |
| klines/XMRUSDT_1d.parquet | 2438 | 2020-02-04T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `d5c1ae12f28e4435…` |
| klines/XMRUSDT_1w.parquet | 347 | 2020-02-10T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `1b911a5796b79551…` |
| funding/XMRUSDT.parquet | 7322 | 2020-02-02T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `0cc8111efa4eb44e…` |
| klines/BNBUSDT_5m.parquet | 700560 | 2020-02-10T08:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `48fc184dd83381cc…` |
| klines/BNBUSDT_1h.parquet | 58380 | 2020-02-10T08:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `2c3102dd064d71ce…` |
| klines/BNBUSDT_4h.parquet | 14595 | 2020-02-10T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `92a23f9a2293c3bd…` |
| klines/BNBUSDT_12h.parquet | 4865 | 2020-02-10T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `7ee5e83b7dc4f40a…` |
| klines/BNBUSDT_1d.parquet | 2431 | 2020-02-11T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `6c2f18d1fe32c04e…` |
| klines/BNBUSDT_1w.parquet | 346 | 2020-02-17T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `c9b71051323339f6…` |
| funding/BNBUSDT.parquet | 7298 | 2020-02-10T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `9f610b40cd9cb85f…` |
| klines/UNIUSDT_5m.parquet | 636924 | 2020-09-18T07:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `4ae21d7095d956cc…` |
| klines/UNIUSDT_1h.parquet | 53077 | 2020-09-18T07:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `e511eb36cfb768f7…` |
| klines/UNIUSDT_4h.parquet | 13270 | 2020-09-18T04:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `5ae91b4d1da079c7…` |
| klines/UNIUSDT_12h.parquet | 4423 | 2020-09-18T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `6eb3c2c290673a67…` |
| klines/UNIUSDT_1d.parquet | 2210 | 2020-09-19T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `538e1c221cf4f610…` |
| klines/UNIUSDT_1w.parquet | 315 | 2020-09-21T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `fd299527db3f53ed…` |
| funding/UNIUSDT.parquet | 6638 | 2020-09-17T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `81d7047d9e90866b…` |
| klines/1000PEPEUSDT_5m.parquet | 360618 | 2023-05-05T16:30:00Z | 2026-10-08T19:55:00Z | 0 | True | `a7475ad55cbf4d87…` |
| klines/1000PEPEUSDT_1h.parquet | 30052 | 2023-05-05T16:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `d83b965f15e77690…` |
| klines/1000PEPEUSDT_4h.parquet | 7513 | 2023-05-05T16:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `ab6acb37c73c1529…` |
| klines/1000PEPEUSDT_12h.parquet | 2504 | 2023-05-05T12:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `cdb4490e9552fc66…` |
| klines/1000PEPEUSDT_1d.parquet | 1251 | 2023-05-06T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `039e921bf45ba1d5…` |
| klines/1000PEPEUSDT_1w.parquet | 178 | 2023-05-08T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `0f0879c2c1583518…` |
| funding/1000PEPEUSDT.parquet | 3757 | 2023-05-05T16:00:00Z | 2026-10-08T16:00:00Z | — | True | `bc7f75b244532751…` |
| klines/DOGEUSDT_5m.parquet | 657060 | 2020-07-10T09:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `69656d1b4f3f7df5…` |
| klines/DOGEUSDT_1h.parquet | 54755 | 2020-07-10T09:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `227d1d51f9a700c0…` |
| klines/DOGEUSDT_4h.parquet | 13689 | 2020-07-10T08:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `cb241bc1f44b7748…` |
| klines/DOGEUSDT_12h.parquet | 4563 | 2020-07-10T00:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `d7a1f0d5a9a08e35…` |
| klines/DOGEUSDT_1d.parquet | 2280 | 2020-07-11T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `609f0644bcc63678…` |
| klines/DOGEUSDT_1w.parquet | 325 | 2020-07-13T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `45c979f34c090204…` |
| funding/DOGEUSDT.parquet | 6845 | 2020-07-10T08:00:00Z | 2026-10-08T16:00:00Z | — | True | `1e2f8da8b6847531…` |
| klines/1000BONKUSDT_5m.parquet | 302760 | 2023-11-22T14:00:00Z | 2026-10-08T19:55:00Z | 0 | True | `5ec06fa8c77d02d7…` |
| klines/1000BONKUSDT_1h.parquet | 25230 | 2023-11-22T14:00:00Z | 2026-10-08T19:00:00Z | 0 | True | `563d4f81870a0f37…` |
| klines/1000BONKUSDT_4h.parquet | 6308 | 2023-11-22T12:00:00Z | 2026-10-08T16:00:00Z | 0 | True | `6ad95d730488eb2e…` |
| klines/1000BONKUSDT_12h.parquet | 2102 | 2023-11-22T12:00:00Z | 2026-10-08T00:00:00Z | 0 | True | `c7c7cef818f1a9fb…` |
| klines/1000BONKUSDT_1d.parquet | 1050 | 2023-11-23T00:00:00Z | 2026-10-07T00:00:00Z | 0 | True | `f57b3c4b4f31ddd3…` |
| klines/1000BONKUSDT_1w.parquet | 149 | 2023-11-27T00:00:00Z | 2026-09-28T00:00:00Z | 0 | True | `70f0fbf950dbd4dd…` |
| funding/1000BONKUSDT.parquet | 6307 | 2023-11-22T16:00:00Z | 2026-10-08T20:00:00Z | — | True | `6afbfe7fda26a5fc…` |

## 15m vs three 5m bars — a DISCLOSURE, not a failure

| stem | compared | price mismatch | volume-only | no 5m triple | of which TC12-new bars |
|---|---|---|---|---|---|
| BTCUSDT | 248360 | 10 | 3 | 1 | 0 price, 0 volume |
| ETHUSDT | 240721 | 11 | 5 | 0 | 0 price, 0 volume |
| SOLUSDT | 212692 | 5 | 3 | 0 | 0 price, 0 volume |
| NEARUSDT | 209712 | 8 | 3 | 0 | 0 price, 0 volume |
| ZECUSDT | 234000 | 14 | 3 | 0 | 0 price, 0 volume |

## The seam bar vs REST — 73 bars in 73 native files, all equal: True · the last inherited funding print of 17 tapes, all equal: True · inherited rows past TC11's as-of: 0


## Fees

| stem | venue | taker bps/side | round trip | maker bps/side | maker kind | slippage tier |
|---|---|---|---|---|---|---|
| BTCUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | A 2.0 |
| ETHUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | A 2.0 |
| SOLUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| NEARUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| ZECUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| ENAUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | C 10.0 |
| PUMPUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | C 10.0 |
| HYPEUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | C 10.0 |
| MNTUSDT_BYBIT | BYBIT_V5_LINEAR | 5.0 | 10.0 | 2.0 | ASSUMPTION — NOT RE-CONFIRMED; no Bybit figure is on file | C 10.0 |
| SUIUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| LTCUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| XMRUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| BNBUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| UNIUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| 1000PEPEUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | C 10.0 |
| DOGEUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | B 5.0 |
| 1000BONKUSDT | BINANCE_USDTM | 5.0 | 10.0 | 2.0 | ON FILE — NOT RE-CONFIRMED | C 10.0 |

## The tick of record (TC12's capture) beside TC11's

| stem | price_tick (TC12) | price_tick (TC11) | equal as Decimal | qty_step | min notional | status |
|---|---|---|---|---|---|---|
| BTCUSDT | 0.10 | 0.10 | True | 0.001 | 50 | TRADING |
| ETHUSDT | 0.01 | 0.01 | True | 0.001 | 20 | TRADING |
| SOLUSDT | 0.0100 | 0.0100 | True | 0.01 | 5 | TRADING |
| NEARUSDT | 0.0010 | 0.0010 | True | 1 | 5 | TRADING |
| ZECUSDT | 0.01 | 0.01 | True | 0.001 | 5 | TRADING |
| ENAUSDT | 0.0000100 | 0.0000100 | True | 1 | 5 | TRADING |
| PUMPUSDT | 0.0000010 | 0.0000010 | True | 1 | 5 | TRADING |
| HYPEUSDT | 0.00100 | 0.00100 | True | 0.01 | 5 | TRADING |
| MNTUSDT_BYBIT | 0.00010 | 0.00010 | True | 0.1 | 5 | Trading |
| SUIUSDT | 0.000100 | 0.000100 | True | 0.1 | 5 | TRADING |
| LTCUSDT | 0.01 | 0.01 | True | 0.001 | 20 | TRADING |
| XMRUSDT | 0.01 | 0.01 | True | 0.001 | 5 | TRADING |
| BNBUSDT | 0.010 | 0.010 | True | 0.01 | 5 | TRADING |
| UNIUSDT | 0.0010 | 0.0010 | True | 1 | 5 | TRADING |
| 1000PEPEUSDT | 0.0000001 | 0.0000001 | True | 1 | 5 | TRADING |
| DOGEUSDT | 0.000010 | 0.000010 | True | 1 | 5 | TRADING |
| 1000BONKUSDT | 0.0000010 | 0.0000010 | True | 1 | 5 | TRADING |

Ticks moved vs TC11's capture: none.

## On-grid shares of the tape on the recorded tick (exact; n_on_grid/n per price field)

| stem | lens | segment | open | high | low | close | last off-grid open (any field) |
|---|---|---|---|---|---|---|---|
| BTCUSDT | 5m | tuning | 293180/506088 | 333581/506088 | 333507/506088 | 293482/506088 | 2022-04-30T14:45:00Z |
| BTCUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| BTCUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| BTCUSDT | 1h | tuning | 24298/42174 | 29654/42174 | 29887/42174 | 24371/42174 | 2022-04-11T17:00:00Z |
| BTCUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| BTCUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| ETHUSDT | 5m | tuning | 483170/483170 | 483170/483170 | 483170/483170 | 483170/483170 | — |
| ETHUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| ETHUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| ETHUSDT | 1h | tuning | 40264/40264 | 40264/40264 | 40264/40264 | 40264/40264 | — |
| ETHUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| ETHUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| SOLUSDT | 5m | tuning | 122174/399083 | 137175/399083 | 139617/399083 | 123368/399083 | 2024-06-30T23:50:00Z |
| SOLUSDT | 5m | holdout_to_tc11_pin | 208280/235009 | 209711/235009 | 209860/235009 | 208210/235009 | 2026-08-29T18:00:00Z |
| SOLUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| SOLUSDT | 1h | tuning | 10215/33256 | 12235/33256 | 12747/33256 | 10300/33256 | 2024-06-30T22:00:00Z |
| SOLUSDT | 1h | holdout_to_tc11_pin | 17361/19585 | 17562/19585 | 17598/19585 | 17341/19585 | 2025-11-13T07:00:00Z |
| SOLUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| NEARUSDT | 5m | tuning | 271501/390143 | 275226/390143 | 277529/390143 | 271852/390143 | 2022-02-22T04:25:00Z |
| NEARUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| NEARUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| NEARUSDT | 1h | tuning | 22633/32511 | 23180/32511 | 23507/32511 | 22635/32511 | 2022-01-20T22:00:00Z |
| NEARUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| NEARUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| ZECUSDT | 5m | tuning | 463007/463007 | 463007/463007 | 463007/463007 | 463007/463007 | — |
| ZECUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| ZECUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| ZECUSDT | 1h | tuning | 38583/38583 | 38583/38583 | 38583/38583 | 38583/38583 | — |
| ZECUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| ZECUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| ENAUSDT | 5m | tuning | 25769/25769 | 25769/25769 | 25769/25769 | 25769/25769 | — |
| ENAUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| ENAUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| ENAUSDT | 1h | tuning | 2147/2147 | 2147/2147 | 2147/2147 | 2147/2147 | — |
| ENAUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| ENAUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| PUMPUSDT | 5m | tuning | 0/0 | 0/0 | 0/0 | 0/0 | — |
| PUMPUSDT | 5m | holdout_to_tc11_pin | 127206/127206 | 127206/127206 | 127206/127206 | 127206/127206 | — |
| PUMPUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| PUMPUSDT | 1h | tuning | 0/0 | 0/0 | 0/0 | 0/0 | — |
| PUMPUSDT | 1h | holdout_to_tc11_pin | 10601/10601 | 10601/10601 | 10601/10601 | 10601/10601 | — |
| PUMPUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| HYPEUSDT | 5m | tuning | 0/0 | 0/0 | 0/0 | 0/0 | — |
| HYPEUSDT | 5m | holdout_to_tc11_pin | 138978/138978 | 138978/138978 | 138978/138978 | 138978/138978 | — |
| HYPEUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| HYPEUSDT | 1h | tuning | 0/0 | 0/0 | 0/0 | 0/0 | — |
| HYPEUSDT | 1h | holdout_to_tc11_pin | 11582/11582 | 11582/11582 | 11582/11582 | 11582/11582 | — |
| HYPEUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| MNTUSDT_BYBIT | 5m | tuning | 58837/78544 | 59338/78544 | 59148/78544 | 58838/78544 | 2024-01-10T22:20:00Z |
| MNTUSDT_BYBIT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| MNTUSDT_BYBIT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| MNTUSDT_BYBIT | 1h | tuning | 4867/6545 | 4993/6545 | 4986/6545 | 4868/6545 | 2024-01-10T21:00:00Z |
| MNTUSDT_BYBIT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| MNTUSDT_BYBIT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| SUIUSDT | 5m | tuning | 122207/122207 | 122207/122207 | 122207/122207 | 122207/122207 | — |
| SUIUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| SUIUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| SUIUSDT | 1h | tuning | 10183/10183 | 10183/10183 | 10183/10183 | 10183/10183 | — |
| SUIUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| SUIUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| LTCUSDT | 5m | tuning | 470782/470782 | 470782/470782 | 470782/470782 | 470782/470782 | — |
| LTCUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| LTCUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| LTCUSDT | 1h | tuning | 39231/39231 | 39231/39231 | 39231/39231 | 39231/39231 | — |
| LTCUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| LTCUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| XMRUSDT | 5m | tuning | 463583/463583 | 463583/463583 | 463583/463583 | 463583/463583 | — |
| XMRUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| XMRUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| XMRUSDT | 1h | tuning | 38631/38631 | 38631/38631 | 38631/38631 | 38631/38631 | — |
| XMRUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| XMRUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| BNBUSDT | 5m | tuning | 345619/461567 | 354503/461567 | 355769/461567 | 345984/461567 | 2024-03-17T22:35:00Z |
| BNBUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| BNBUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| BNBUSDT | 1h | tuning | 28875/38463 | 30034/38463 | 30171/38463 | 28840/38463 | 2021-05-18T12:00:00Z |
| BNBUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| BNBUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| UNIUSDT | 5m | tuning | 338766/397931 | 342928/397931 | 343813/397931 | 338833/397931 | 2021-11-24T06:35:00Z |
| UNIUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| UNIUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| UNIUSDT | 1h | tuning | 28220/33160 | 28737/33160 | 28873/33160 | 28227/33160 | 2021-09-23T09:00:00Z |
| UNIUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| UNIUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| 1000PEPEUSDT | 5m | tuning | 121625/121625 | 121625/121625 | 121625/121625 | 121625/121625 | — |
| 1000PEPEUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| 1000PEPEUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| 1000PEPEUSDT | 1h | tuning | 10135/10135 | 10135/10135 | 10135/10135 | 10135/10135 | — |
| 1000PEPEUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| 1000PEPEUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| DOGEUSDT | 5m | tuning | 339916/418067 | 343037/418067 | 343872/418067 | 340185/418067 | 2021-07-28T00:10:00Z |
| DOGEUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| DOGEUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| DOGEUSDT | 1h | tuning | 28357/34838 | 28709/34838 | 28809/34838 | 28342/34838 | 2021-05-14T17:00:00Z |
| DOGEUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| DOGEUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |
| 1000BONKUSDT | 5m | tuning | 63767/63767 | 63767/63767 | 63767/63767 | 63767/63767 | — |
| 1000BONKUSDT | 5m | holdout_to_tc11_pin | 235009/235009 | 235009/235009 | 235009/235009 | 235009/235009 | — |
| 1000BONKUSDT | 5m | strip | 3984/3984 | 3984/3984 | 3984/3984 | 3984/3984 | — |
| 1000BONKUSDT | 1h | tuning | 5313/5313 | 5313/5313 | 5313/5313 | 5313/5313 | — |
| 1000BONKUSDT | 1h | holdout_to_tc11_pin | 19585/19585 | 19585/19585 | 19585/19585 | 19585/19585 | — |
| 1000BONKUSDT | 1h | strip | 332/332 | 332/332 | 332/332 | 332/332 | — |

## Observed granularity per calendar month (5m) — 1014 stem-months; coarser than the recorded tick: 24

- NOT HELD on 24 stem-month(s) — listed under coarser_months [O-27]

| stem | month | observed granularity | recorded tick |
|---|---|---|---|
| ENAUSDT | 2024-04 | 0.00100 | 0.0000100 |
| ENAUSDT | 2024-05 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-06 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-07 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-08 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-09 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-10 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-11 | 0.00010 | 0.0000100 |
| ENAUSDT | 2024-12 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-01 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-02 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-03 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-04 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-05 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-06 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-07 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-08 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-09 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-10 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-11 | 0.00010 | 0.0000100 |
| ENAUSDT | 2025-12 | 0.00010 | 0.0000100 |
| ENAUSDT | 2026-01 | 0.00010 | 0.0000100 |
| ENAUSDT | 2026-02 | 0.00010 | 0.0000100 |
| ENAUSDT | 2026-03 | 0.00010 | 0.0000100 |

## Zero-volume flat bars per native file, by segment (kept, counted, never filled)

| stem \| lens | tuning | holdout_to_tc11_pin | strip | total | zero-volume bars (total) |
|---|---|---|---|---|---|
| BTCUSDT|5m | 81 | 5 | 0 | 86 | 86 |
| BTCUSDT|15m | 21 | 0 | 0 | 21 | 21 |
| BTCUSDT|1h | 3 | 0 | 0 | 3 | 3 |
| BTCUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| BTCUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| ETHUSDT|5m | 67 | 5 | 0 | 72 | 72 |
| ETHUSDT|15m | 16 | 0 | 0 | 16 | 16 |
| ETHUSDT|1h | 1 | 0 | 0 | 1 | 1 |
| ETHUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| ETHUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| SOLUSDT|5m | 26 | 5 | 0 | 31 | 31 |
| SOLUSDT|15m | 6 | 0 | 0 | 6 | 6 |
| SOLUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| SOLUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| SOLUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| NEARUSDT|5m | 29 | 5 | 0 | 34 | 34 |
| NEARUSDT|15m | 6 | 0 | 0 | 6 | 6 |
| NEARUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| NEARUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| NEARUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| ZECUSDT|5m | 65 | 5 | 0 | 70 | 70 |
| ZECUSDT|15m | 7 | 0 | 0 | 7 | 7 |
| ZECUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| ZECUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| ZECUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| ENAUSDT|5m | 0 | 21 | 0 | 21 | 21 |
| ENAUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| ENAUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| ENAUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| PUMPUSDT|5m | 0 | 3 | 0 | 3 | 3 |
| PUMPUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| PUMPUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| PUMPUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| HYPEUSDT|5m | 0 | 3 | 0 | 3 | 3 |
| HYPEUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| HYPEUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| HYPEUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| MNTUSDT_BYBIT|5m | 140 | 3 | 0 | 143 | 143 |
| MNTUSDT_BYBIT|1h | 0 | 0 | 0 | 0 | 0 |
| MNTUSDT_BYBIT|4h | 0 | 0 | 0 | 0 | 0 |
| MNTUSDT_BYBIT|12h | 0 | 0 | 0 | 0 | 0 |
| SUIUSDT|5m | 3 | 5 | 0 | 8 | 8 |
| SUIUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| SUIUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| SUIUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| LTCUSDT|5m | 28 | 5 | 0 | 33 | 33 |
| LTCUSDT|1h | 0 | 0 | 0 | 0 | 0 |
| LTCUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| LTCUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| XMRUSDT|5m | 49 | 21 | 0 | 70 | 70 |
| XMRUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| XMRUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| XMRUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| BNBUSDT|5m | 26 | 21 | 0 | 47 | 47 |
| BNBUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| BNBUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| BNBUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| UNIUSDT|5m | 26 | 21 | 0 | 47 | 47 |
| UNIUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| UNIUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| UNIUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| 1000PEPEUSDT|5m | 3 | 21 | 0 | 24 | 24 |
| 1000PEPEUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| 1000PEPEUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| 1000PEPEUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| DOGEUSDT|5m | 28 | 21 | 0 | 49 | 49 |
| DOGEUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| DOGEUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| DOGEUSDT|12h | 0 | 0 | 0 | 0 | 0 |
| 1000BONKUSDT|5m | 0 | 21 | 0 | 21 | 21 |
| 1000BONKUSDT|1h | 0 | 1 | 0 | 1 | 1 |
| 1000BONKUSDT|4h | 0 | 0 | 0 | 0 | 0 |
| 1000BONKUSDT|12h | 0 | 0 | 0 | 0 | 0 |

## Leans

- [LEAN-HEPHAESTUS] L-D.1 (research_outputs/tierc12/LEANS.md) THE PIN: AS_OF = 2026-10-08T20:00:00Z (close ms 1791489600000), the latest 4h bar closed when STEP Q was committed (2026-10-08T22:52:13Z); DERIVED from the filed STEP Q record, never typed, held equal to the value O-7 prints; proven closed on both venue clocks; write-once; every later read is by object.
- [LEAN-HEPHAESTUS] L-D.3 SNAPSHOT: tc12_20261008 is an APFS clone (cp -cpR) of tc11_20260925; every cloned file is re-hashed against TC11's STAGE_D_MANIFEST before the first write (CLONE_ATTEST.json); it is extended over REST only. The live cache is never read or written and the TC10 and TC11 snapshots are never written.
- [LEAN-HEPHAESTUS] L-D.4 SCOPE: TC11's scope of record BY OBJECT (O-26): 17 stems x native {5m,1h,4h,12h} + CLASSIC5 x 15m + 17 x derived {1d,1w} + 17 funding tapes. A SUPERSET of the contract's list: the contract's 'twelve new assets 1h/4h/1d only' binds which lenses Stage V stamps, not which tapes the snapshot carries.
- [LEAN-HEPHAESTUS] L-D.6 ZERO OVERLAP: every tape is extended from ITS OWN edge + one step (engine.data._save_cache keeps the NEW row at an identical open_time, so an overlapping start would let REST overwrite an inherited bar). Gaps are counted and listed, never filled. The seam bar of every native file and the last inherited funding print of every tape are compared with the venue read-only (EDGE_AUDIT.json); a difference is disclosed, never repaired.
- [LEAN-HEPHAESTUS] L-D.7 FORMING BAR: the fetch target is a function of the pin alone; every reply is filtered to [lo, hi] before any save; each venue's clock is read and must be past the pin before its first kline request; every file ends exactly at its lens's last bar closing <= the pin.
- [LEAN-HEPHAESTUS] L-D.8 / TC10 L1 CARRIED: 1d = exactly six complete native-4h bars per UTC day; 1w = seven complete derived days, MONDAY-anchored UTC, complete weeks only; the source is native 4h, never 1h/5m aggregates, never a native 1d/1w fetch. A derived bar is a declared aggregate of venue bars that all exist — not a synthetic bar.
- [LEAN-HEPHAESTUS] L-D.9 / TC10 D-b, D-g CARRIED: funding is kept through AS_OF close + the jitter and a print belongs to the hour its stamp FLOORS to; the funding prefix is cut on the floor hour, never on the raw stamp.
- [LEAN-HEPHAESTUS] L-D.10 VENUE OF RECORD: TC10's Stage D table, TC10's VENUE_PROBE.json and TC11's manifest venues[] must agree row for row, 17 of 17; the venue of a tape is decided once and never re-probed. MNT's whole tape (klines and funding) is Bybit v5 linear, stem MNTUSDT_BYBIT, never spliced; PUMPFUN = PUMPUSDT.
- [LEAN-HEPHAESTUS] L-D.13 / L-D.16 FLAT BARS: a zero-volume flat bar is a bar the VENUE published during an outage — kept, counted, attributed to the venue from a sealed capture (FLAT_BAR_ATTEST.json), never removed, filled or altered. The claim is 'Naiad inserted no bar', not 'the venue published no flat bar'.
- [LEAN-HEPHAESTUS] L-D.17-21 FEES: taker 5.0 bps/side, 10.0 round trip (tierc2_rules) — the toll of record of the TC-series, unchanged; the charter slippage tiers unchanged; maker_bps_side per VENUE is the venue's published entry-tier USDT-margined rate when its page is retrieved and parsed from saved bytes, else the figure on file (README) flagged NOT RE-CONFIRMED, applied to Bybit as an ASSUMPTION. No figure enters by keyboard.
- [LEAN-HEPHAESTUS] L-D.22-23 TICK: the tick of record is the price_tick STRING of this stage's own CONTRACT_SPECS.json capture — a point-in-time venue spec taken at the fetch run, applied over the whole corridor (O-20); TICK_GRID_AUDIT.json prints the on-grid shares and the observed granularity per calendar month and LISTS every month where the tape is coarser than the recorded tick (O-27).
- [LEAN-HEPHAESTUS] L-D.24 MIRROR: a sha-verified plain copy of the sealed snapshot to the LaCie by --mirror, filed under the non-blocking child record TC12-D.mirror; its status lives in MIRROR_ATTEST.json, never in this manifest.

## Standing disclosures

- The R0 scout's three unauthenticated GETs (scout map U4, section 1.16: Binance /fapi/v1/time, one BTCUSDT 4h kline, one Bybit MNTUSDT 4h kline) are NOT the venue proof of the pin: they are in no FETCH_LOG and nothing they returned was saved. The proof is AS_OF_PIN.json's.
- Before this module first ran, the executor resolved the three hostnames it would use (fapi.binance.com, api.bybit.com, data.binance.vision) by DNS only — a name lookup, no HTTP request to any venue; nothing was returned by a venue and nothing was saved.
- At TC11's pin every one of the 17 funding tapes holds exactly one print of that hour (16 Binance tapes stamped a few ms past the pin instant, MNT stamped exactly at it); it is INHERITED, kept by the floor-hour law, and belongs to the bar that OPENS at TC11's pin — the first bar of the forward strip.
- The 15m tapes of the nine non-CLASSIC5 stems that hold one, the 1m tapes, the out-of-panel stems' tapes and the root MANIFEST.json stay in the snapshot untouched and out of scope (listed by sha under out_of_scope_snapshot_files); several end in 2026-08 or at TC10's edge.
- No TC12 stage reads 15m; the five CLASSIC5 15m tapes are extended only so that no in-scope file ends short of the pin.
- The snapshot root's MANIFEST.json (11589 B, sha256 c73fec06e38f2ef9…) is carried byte-for-byte from the TC11 snapshot; TC11's manifest pins it by sha (CLONE_ATTEST compares it with that record). It is a cache manifest written by another estate (self-described created_utc 2026-08-12T02:42:31Z, mode 'estate', 73 files) and it is STALE: of the other 175 files of the TC12 snapshot it describes 0 at their current bytes (3 of the files it lists are not in the snapshot), and 0 of the 124 files TC12 extended. No TC12 loader reads it; it is listed under out_of_scope_snapshot_files and read only to describe it here.

## Operator rulings needed

- CARRIED FROM TC10, STILL OPEN: F-D-1 (which of the venue's two publications, REST or the BULK ARCHIVE, is the record on incident bars). TC12, like TC10 and TC11, fetched REST only; its rows past each TC11 edge are REST by construction. TC12 runs no such leg and re-cuts nothing.
- CARRIED FROM TC10, STILL OPEN: PUMPFUN -> PUMPUSDT [LEAN D-d] and MNT -> Bybit v5 linear [LEAN D-c] await the operator's nod (default: as TC10's table).
- CARRIED FROM TC10, STILL OPEN: whether charter slippage joins the toll of record (default: a twin only — the contract says the tiers are unchanged).
- THE LaCie MIRROR [L-D.24; the resume paste's "mirror"]: default destination /Volumes/LaCie/Naiad/snapshots/tc12_20261008/ (+ /Volumes/LaCie/Naiad/provenance/tc12_20261008/), a sha-verified plain copy by `tierc12_data.py --mirror` when the drive is reachable; its status is in data/MIRROR_ATTEST.json and progress/TC12-D.mirror.json, never here. The TC10 and TC11 snapshots stay UNMIRRORED and are LISTED for ATHENA: ~/.cache/naiad/snapshots/tc10_20260921, ~/.cache/naiad/snapshots/tc11_20260925.
- THE "maker-bps" PIN (veto by name, contract :137): per venue, the published base rate when the page is retrieved and parsed; otherwise the figure on file (README.md) flagged NOT RE-CONFIRMED, applied to Bybit as an ASSUMPTION. A figure given by the operator replaces it and is recorded as his.
