# TIER-C10 · CLOSE §3 · STAGE D MANIFEST — incl. the F-D-4 / F-D-5 tables

**AS OF** `2026-09-21T16:00:00Z` (last closed 4h bar: open `2026-09-21T12:00:00Z`) · seed 20260921 · ONE corridor: `research_outputs/tierc10/data/AS_OF_PIN.json` == `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` == `research_outputs/tierc10/PROGRESS.json` as_of_of_record `2026-09-21T16:00:00Z`

> these files are described AS OF the pinned last closed 4h bar named here and of no other; bars stamped after it are counted, never read [TC6V-a, carried by TIER-C10]

**REPORT-ONLY · Tier-E.** This section DESCRIBES the data of record. It scores nothing, runs no card, consults no registration's verdict, and reads bars only through `tierc10_data.load_asof` (funding through `load_funding_asof`) — never `tierc2_baseline.load_klines`, whose whole-file read would pass the pin on the 14 kline files that hold rows stamped after it. Every table below is labelled so.

Contract of record `exchange/queue/2026-09-22_TC10_RESUME_APOLLO.md` (sha256 `8a0bf279bcab0f27`, == PROGRESS.json contract_of_record), line 135: “· Stage D manifest incl. the F-D-4 / F-D-5 tables”

Generator `scripts/tierc10_close_close_stage_d.py` · transcript `research_outputs/tierc10/close/FIXTURES_CLOSE_stage_d.txt` · spliced source `research_outputs/tierc10/data/STAGE_D_MANIFEST.md` (sha256 `e7252a64a67b77b6`)

## S3 · STATUS — F-D-1 is RED; D-CORE stays PARTIAL on it

*REPORT-ONLY · Tier-E · status carried from filed transcripts and the ledger; this CLOSE build reaches no venue.*

| item | source | reads |
|---|---|---|
| D-CORE ledger status | `research_outputs/tierc10/PROGRESS.json` stages[D-CORE].status | **PARTIAL** (15 artifacts) |
| F-D-1, filed ONLINE run | `research_outputs/tierc10/data/FIXTURES_STAGE_D.txt`:77 | `[FAIL]` — 3 bar(s) differ: XMRUSDT 4h 2025-01-14T12:00:00Z, XMRUSDT 1h 2024-10-28T20:00:00Z, XMRUSDT 5m 2024-10-28T20:00:00Z; FIXTURE SUMMARY failed = ["F-D-1"] |
| F-D-1, filed OFFLINE run | `research_outputs/tierc10/data/FIXTURES_STAGE_D_OFFLINE.txt`:9 | `[NOT RUN]` (listed in not_run) |
| F-D-1, this CLOSE build | `scripts/tierc10_close_close_stage_d.py` | NOT RUN — no venue reach |

F-D-1 STATUS: **RED** (derived from the filed ONLINE transcript) · **NOT RUN** in this CLOSE build

OPERATOR QUESTION: F-D-1 IS RED and stays RED: the venue's REST API and its BULK ARCHIVE publish different bars on incident stamps and the panel is publication-heterogeneous on them (see venue_publications_disagree). RULING NEEDED: which publication is the record. Ruling ARCHIVE makes the REST-carrying files the odd ones out; ruling REST the ARCHIVE-carrying ones. The archive is no clean alternative: it lacks whole days, publishes nothing before 2020, and its monthly and daily zips disagree with each other on BTC incident bars. No bar is rewritten either way without the operator's word.

Ruling on the record (`research_outputs/tierc10/OPERATOR_RULINGS.md`, verbatim): “Which Binance publication is the record.” — “The USDT pair, either on Binance or Bybit”. It names the pair and permits the venue; it does not choose between the venue's REST API and its BULK ARCHIVE.

Still blocked (`research_outputs/tierc10/OPERATOR_RULINGS.md`:141–144, lines joined): **F-D-1 / R5.** "The USDT pair, either on Binance or Bybit" names the pair and permits the venue, but the actual disagreement is the venue's **REST API vs its BULK ARCHIVE**, which publish different bars on incident stamps. F-D-1 stays RED and is **printed RED**; F-D-1b carries. No bar is rewritten either way without the narrower word: **REST or ARCHIVE?**

## S3 · D-CORE artifacts — 15 re-hashed against PROGRESS.json

*REPORT-ONLY · Tier-E · every artifact the D-CORE ledger record names, re-hashed from disk (sha256 and bytes).*

| artifact | bytes | sha256[:16] | re-hash |
|---|---:|---|---|
| `research_outputs/tierc10/data/ARCHIVE_FORMS_PROBE.json` | 12074 | `c29ae6c9aa8ee366` | MATCH |
| `research_outputs/tierc10/data/ARCHIVE_VS_SNAPSHOT_AUDIT.json` | 96438 | `ee4d7086494f51e9` | MATCH |
| `research_outputs/tierc10/data/AS_OF_PIN.json` | 604 | `0a78ae6993cc5fb9` | MATCH |
| `research_outputs/tierc10/data/CONTRACT_SPECS.json` | 57157 | `275b218d04a18a4a` | MATCH |
| `research_outputs/tierc10/data/DATA_SPEND_AUDIT.json` | 249025 | `24cd11f1a882de52` | MATCH |
| `research_outputs/tierc10/data/FETCH_LOG.jsonl` | 18716 | `46783239d5b4af5d` | MATCH |
| `research_outputs/tierc10/data/FIXTURES_STAGE_D.txt` | 62244 | `fd302025991fe5d5` | MATCH |
| `research_outputs/tierc10/data/FIXTURES_STAGE_D_OFFLINE.txt` | 42546 | `8295ce69725c0a8a` | MATCH |
| `research_outputs/tierc10/data/PRE_STATE.json` | 16918 | `9d069d57fba3f163` | MATCH |
| `research_outputs/tierc10/data/REST_VS_SNAPSHOT_AUDIT.json` | 37474 | `45c91ee8559c01a1` | MATCH |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` | 405715 | `de2e8663bbf101df` | MATCH |
| `research_outputs/tierc10/data/STAGE_D_MANIFEST.md` | 65336 | `e7252a64a67b77b6` | MATCH |
| `research_outputs/tierc10/data/VENUE_PROBE.json` | 10787 | `849810473cb8a1c7` | MATCH |
| `research_outputs/tierc10/data/WRITE_ONCE_SEAL.json` | 2049 | `75f7b1aa0836a30d` | MATCH |
| `research_outputs/tierc10/data/fee_schedule.json` | 23925 | `3a18b84e0211110b` | MATCH |

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## Venue of record» (section), bytes [420, 3639), sha256 `643ca8fd36e4ec94` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=venue mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[420,3639) sha256=643ca8fd36e4ec9422074ac2e9d002b71a39145adaeb6984627992ffd2f4fdb0 -->
## Venue of record

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

REJECTED for PUMPFUN: `PUMPBTCUSDT` — baseAsset PUMPBTC != PUMP: a different asset

### The contract's venue premises, held against the probe

- **XMR** — contract: "alternate venue only where Binance lacks history — 'XMR post-delisting'" → STALE — XMRUSDT is a TRADING Binance USDT-M PERPETUAL (listed 2020-02-03T08:00:00Z); the WHOLE tape is Binance, no alternate venue is used and no splice question arises.
- **HYPE** — contract: "alternate venue 'if absent' from Binance" → NOT TRIGGERED — HYPEUSDT is a TRADING Binance USDT-M contract; default venue, whole tape.
- **MNT** — contract: "alternate venue 'if absent' from Binance" → TRIGGERED — absent from Binance USDT-M; the WHOLE tape is BYBIT_V5_LINEAR (stem MNTUSDT_BYBIT), one venue, never spliced.

<!-- S3-SPLICE END id=venue -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## Admission — >= TIDE_SLOW (316) + MEM_TTL_BARS (400) = 716 closed 4h bars» (section), bytes [3639, 5011), sha256 `a022765c5ca2f85e` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=admission mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[3639,5011) sha256=a022765c5ca2f85ec8e320e9a229c95b900fc611c479975fde86bb7db7684720 -->
## Admission — >= TIDE_SLOW (316) + MEM_TTL_BARS (400) = 716 closed 4h bars

| asset | stem | closed 4h | margin | 1d | 1w | admitted |
|---|---|---:|---:|---:|---:|---|
| BTC | BTCUSDT | 15420 | +14704 | 2569 | 367 | ADMITTED |
| ETH | ETHUSDT | 14943 | +14227 | 2489 | 355 | ADMITTED |
| SOL | SOLUSDT | 13191 | +12475 | 2197 | 313 | ADMITTED |
| NEAR | NEARUSDT | 13004 | +12288 | 2166 | 309 | ADMITTED |
| ZEC | ZECUSDT | 14522 | +13806 | 2419 | 345 | ADMITTED |
| ENA | ENAUSDT | 5413 | +4697 | 901 | 128 | ADMITTED |
| PUMPFUN | PUMPUSDT | 2631 | +1915 | 437 | 62 | ADMITTED |
| HYPE | HYPEUSDT | 2876 | +2160 | 478 | 68 | ADMITTED |
| MNT | MNTUSDT_BYBIT | 6513 | +5797 | 1084 | 154 | ADMITTED |
| SUI | SUIUSDT | 7422 | +6706 | 1236 | 176 | ADMITTED |
| LTC | LTCUSDT | 14684 | +13968 | 2446 | 349 | ADMITTED |
| XMR | XMRUSDT | 14534 | +13818 | 2421 | 345 | ADMITTED |
| BNB | BNBUSDT | 14492 | +13776 | 2414 | 344 | ADMITTED |
| UNI | UNIUSDT | 13167 | +12451 | 2193 | 313 | ADMITTED |
| PEPE | 1000PEPEUSDT | 7410 | +6694 | 1234 | 176 | ADMITTED |
| DOGE | DOGEUSDT | 13586 | +12870 | 2263 | 323 | ADMITTED |
| BONK | 1000BONKUSDT | 6205 | +5489 | 1033 | 147 | ADMITTED |

EXCLUDED: none.

PANEL (17): BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT ENAUSDT PUMPUSDT HYPEUSDT MNTUSDT_BYBIT SUIUSDT LTCUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT

<!-- S3-SPLICE END id=admission -->

## S3 · Per asset × lens — STAGE_D_MANIFEST.json files[], whole (119 = 102 kline cells + 17 funding files)

*REPORT-ONLY · Tier-E · printed from `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` files[]. RE-MEASURED = the bars re-read through `tierc10_data.load_asof` (funding: `load_funding_asof`) and their count, first / last open and gaps compared to the filed row, the file re-hashed against its filed sha256. Rows past the pin are COUNTED from the manifest, never read.*

<!-- S3-TABLE BEGIN id=cells -->
| asset | stem | lens | bars as-of | first open | last as-of open | past the pin | gaps (missing) | sha256[:16] | re-measured |
|---|---|---|---:|---|---|---:|---|---|---|
| BTC | BTCUSDT | 5m | 740137 | 2019-09-08T17:55:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `74319e9782cc883b` | OK |
| BTC | BTCUSDT | 1h | 61679 | 2019-09-08T17:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `7a3b86f82f384d09` | OK |
| BTC | BTCUSDT | 4h | 15420 | 2019-09-08T16:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `280607719edd49fd` | OK |
| BTC | BTCUSDT | 12h | 5140 | 2019-09-08T12:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `cd61f763c88f29db` | OK |
| BTC | BTCUSDT | 1d | 2569 | 2019-09-09T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `7c2d90c049aba05a` | OK |
| BTC | BTCUSDT | 1w | 367 | 2019-09-09T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `5844aa75b0253f7b` | OK |
| BTC | BTCUSDT | funding | 7706 | 2019-09-10T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `3ba1f31d10944dd6` | OK |
| ETH | ETHUSDT | 5m | 717219 | 2019-11-27T07:45:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `61c0f0427ccbf35c` | OK |
| ETH | ETHUSDT | 1h | 59769 | 2019-11-27T07:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `fb70f93edf04c30c` | OK |
| ETH | ETHUSDT | 4h | 14943 | 2019-11-27T04:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `c8c14416e498c501` | OK |
| ETH | ETHUSDT | 12h | 4981 | 2019-11-27T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `b5ab0c06c8ca9a26` | OK |
| ETH | ETHUSDT | 1d | 2489 | 2019-11-28T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `2c5abd5ff3691373` | OK |
| ETH | ETHUSDT | 1w | 355 | 2019-12-02T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `6da90fe87b32349c` | OK |
| ETH | ETHUSDT | funding | 7472 | 2019-11-27T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `33c9a22780f36987` | OK |
| SOL | SOLUSDT | 5m | 633132 | 2020-09-14T07:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `0dfda5c7154a03c2` | OK |
| SOL | SOLUSDT | 1h | 52761 | 2020-09-14T07:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `b534bc7eedda7640` | OK |
| SOL | SOLUSDT | 4h | 13191 | 2020-09-14T04:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `33609269233da8f7` | OK |
| SOL | SOLUSDT | 12h | 4397 | 2020-09-14T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `f363e729e781d634` | OK |
| SOL | SOLUSDT | 1d | 2197 | 2020-09-15T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `26f0d20d94f6cebd` | OK |
| SOL | SOLUSDT | 1w | 313 | 2020-09-21T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `f4279094e89aa171` | OK |
| SOL | SOLUSDT | funding | 6671 | 2020-09-14T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `1192f92711d8e0d0` | OK |
| NEAR | NEARUSDT | 5m | 624192 | 2020-10-15T08:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `89682896240f3b7a` | OK |
| NEAR | NEARUSDT | 1h | 52016 | 2020-10-15T08:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `65ada840cd899b35` | OK |
| NEAR | NEARUSDT | 4h | 13004 | 2020-10-15T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `a978d31eb4c949c2` | OK |
| NEAR | NEARUSDT | 12h | 4335 | 2020-10-15T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `850e0406ac79f140` | OK |
| NEAR | NEARUSDT | 1d | 2166 | 2020-10-16T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `8125ba76bb529dfc` | OK |
| NEAR | NEARUSDT | 1w | 309 | 2020-10-19T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `f3ee8ab250bf5b83` | OK |
| NEAR | NEARUSDT | funding | 6503 | 2020-10-15T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `580eb953ba839ce2` | OK |
| ZEC | ZECUSDT | 5m | 697056 | 2020-02-05T08:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `b5363ee6e9585c4d` | OK |
| ZEC | ZECUSDT | 1h | 58088 | 2020-02-05T08:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `9e9b22f917d08c95` | OK |
| ZEC | ZECUSDT | 4h | 14522 | 2020-02-05T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `8d9459e839b9b3da` | OK |
| ZEC | ZECUSDT | 12h | 4841 | 2020-02-05T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `9183c110b31ec214` | OK |
| ZEC | ZECUSDT | 1d | 2419 | 2020-02-06T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `26b67d8072b9fa41` | OK |
| ZEC | ZECUSDT | 1w | 345 | 2020-02-10T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `1c330c55f2625588` | OK |
| ZEC | ZECUSDT | funding | 7262 | 2020-02-05T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `2586f8ec7dda0d44` | OK |
| ENA | ENAUSDT | 5m | 259818 | 2024-04-02T12:30:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `316128479ba330f4` | OK |
| ENA | ENAUSDT | 1h | 21652 | 2024-04-02T12:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `5860d840872b647c` | OK |
| ENA | ENAUSDT | 4h | 5413 | 2024-04-02T12:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `6b9f33bc6af04402` | OK |
| ENA | ENAUSDT | 12h | 1804 | 2024-04-02T12:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `2071332a4c1c6b75` | OK |
| ENA | ENAUSDT | 1d | 901 | 2024-04-03T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `9e81363b553ffcb4` | OK |
| ENA | ENAUSDT | 1w | 128 | 2024-04-08T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `cc9ffe145c6bf48f` | OK |
| ENA | ENAUSDT | funding | 5412 | 2024-04-02T16:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `951e99858f98a1f6` | OK |
| PUMPFUN | PUMPUSDT | 5m | 126246 | 2025-07-10T07:30:00Z | 2026-09-21T15:55:00Z | 0 | 0 (0) | `41d5600e6403247e` | OK |
| PUMPFUN | PUMPUSDT | 1h | 10521 | 2025-07-10T07:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `b48653c974286802` | OK |
| PUMPFUN | PUMPUSDT | 4h | 2631 | 2025-07-10T04:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `1b66edfac0835b80` | OK |
| PUMPFUN | PUMPUSDT | 12h | 877 | 2025-07-10T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `82015cc4d1297027` | OK |
| PUMPFUN | PUMPUSDT | 1d | 437 | 2025-07-11T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `53cd5ca5b79dd54f` | OK |
| PUMPFUN | PUMPUSDT | 1w | 62 | 2025-07-14T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `afa2ee1b1ac4b38e` | OK |
| PUMPFUN | PUMPUSDT | funding | 2630 | 2025-07-10T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `a44738bdb23b23ad` | OK |
| HYPE | HYPEUSDT | 5m | 138018 | 2025-05-30T10:30:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `21da81858fc9b876` | OK |
| HYPE | HYPEUSDT | 1h | 11502 | 2025-05-30T10:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `f1de5d31011bf648` | OK |
| HYPE | HYPEUSDT | 4h | 2876 | 2025-05-30T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `5f8085646ef983bf` | OK |
| HYPE | HYPEUSDT | 12h | 959 | 2025-05-30T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `76c1d5c1426befb4` | OK |
| HYPE | HYPEUSDT | 1d | 478 | 2025-05-31T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `0f5bbe4ccd7d8baa` | OK |
| HYPE | HYPEUSDT | 1w | 68 | 2025-06-02T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `5d52c97c2ea8d700` | OK |
| HYPE | HYPEUSDT | funding | 2875 | 2025-05-30T12:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `98551fd7b530990a` | OK |
| MNT | MNTUSDT_BYBIT | 5m | 312593 | 2023-10-02T06:35:00Z | 2026-09-21T15:55:00Z | 0 | 0 (0) | `4dde955a65086b0a` | OK |
| MNT | MNTUSDT_BYBIT | 1h | 26050 | 2023-10-02T06:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `f78d3b3877922083` | OK |
| MNT | MNTUSDT_BYBIT | 4h | 6513 | 2023-10-02T04:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `ad5265cdb2f5d8f4` | OK |
| MNT | MNTUSDT_BYBIT | 12h | 2171 | 2023-10-02T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `1c8da890f8eaeaf6` | OK |
| MNT | MNTUSDT_BYBIT | 1d | 1084 | 2023-10-03T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `13c5b96c9ed5d80a` | OK |
| MNT | MNTUSDT_BYBIT | 1w | 154 | 2023-10-09T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `a04c5eb57cbdfeb9` | OK |
| MNT | MNTUSDT_BYBIT | funding | 3258 | 2023-10-02T00:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `725824db985dfecb` | OK |
| SUI | SUIUSDT | 5m | 356256 | 2023-05-03T16:00:00Z | 2026-09-21T15:55:00Z | 0 | 0 (0) | `d8206c0d367fa2cb` | OK |
| SUI | SUIUSDT | 1h | 29688 | 2023-05-03T16:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `2259d859dbffe995` | OK |
| SUI | SUIUSDT | 4h | 7422 | 2023-05-03T16:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `ad7f9b5172fe5d69` | OK |
| SUI | SUIUSDT | 12h | 2474 | 2023-05-03T12:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `4b9d0e94ee477c38` | OK |
| SUI | SUIUSDT | 1d | 1236 | 2023-05-04T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `b265039e664ab597` | OK |
| SUI | SUIUSDT | 1w | 176 | 2023-05-08T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `45a2a78abb344242` | OK |
| SUI | SUIUSDT | funding | 3712 | 2023-05-03T16:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `24458a3de211dcae` | OK |
| LTC | LTCUSDT | 5m | 704831 | 2020-01-09T08:05:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `4fb0cd41cfab9253` | OK |
| LTC | LTCUSDT | 1h | 58736 | 2020-01-09T08:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `a37a40fddfe164f4` | OK |
| LTC | LTCUSDT | 4h | 14684 | 2020-01-09T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `f556133b7feaa219` | OK |
| LTC | LTCUSDT | 12h | 4895 | 2020-01-09T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `ce8e49c3d618e7b1` | OK |
| LTC | LTCUSDT | 1d | 2446 | 2020-01-10T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `7a1e025e7ed54f67` | OK |
| LTC | LTCUSDT | 1w | 349 | 2020-01-13T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `f99c92df34c84801` | OK |
| LTC | LTCUSDT | funding | 7343 | 2020-01-09T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `68b874931b1c7a78` | OK |
| XMR | XMRUSDT | 5m | 697632 | 2020-02-03T08:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `0272fffa5c90aaf6` | OK |
| XMR | XMRUSDT | 1h | 58136 | 2020-02-03T08:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `323ceae118c9d704` | OK |
| XMR | XMRUSDT | 4h | 14534 | 2020-02-03T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `9f40d3a0f416f742` | OK |
| XMR | XMRUSDT | 12h | 4845 | 2020-02-03T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `577ce9a055c2437d` | OK |
| XMR | XMRUSDT | 1d | 2421 | 2020-02-04T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `68b7def5da34cb63` | OK |
| XMR | XMRUSDT | 1w | 345 | 2020-02-10T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `043d6eeaa2cd1e23` | OK |
| XMR | XMRUSDT | funding | 7271 | 2020-02-02T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `4f5a64150cee2cd4` | OK |
| BNB | BNBUSDT | 5m | 695616 | 2020-02-10T08:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `d4c94612b91b3c7f` | OK |
| BNB | BNBUSDT | 1h | 57968 | 2020-02-10T08:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `f899d7b3ef6e0ad1` | OK |
| BNB | BNBUSDT | 4h | 14492 | 2020-02-10T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `0ed961d6fa60164a` | OK |
| BNB | BNBUSDT | 12h | 4831 | 2020-02-10T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `6cfd6e9a11349ce5` | OK |
| BNB | BNBUSDT | 1d | 2414 | 2020-02-11T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `5682ce1458f8e8d3` | OK |
| BNB | BNBUSDT | 1w | 344 | 2020-02-17T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `65abb4a833f44ae7` | OK |
| BNB | BNBUSDT | funding | 7247 | 2020-02-10T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `4b8c0176749a526a` | OK |
| UNI | UNIUSDT | 5m | 631980 | 2020-09-18T07:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `3b3684ac9bc688f7` | OK |
| UNI | UNIUSDT | 1h | 52665 | 2020-09-18T07:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `bb33097872d15246` | OK |
| UNI | UNIUSDT | 4h | 13167 | 2020-09-18T04:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `ea4c3c81b71b587c` | OK |
| UNI | UNIUSDT | 12h | 4389 | 2020-09-18T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `aa46bdec70eab63c` | OK |
| UNI | UNIUSDT | 1d | 2193 | 2020-09-19T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `8b5e4f50084f32e9` | OK |
| UNI | UNIUSDT | 1w | 313 | 2020-09-21T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `67f885b934cd9fb4` | OK |
| UNI | UNIUSDT | funding | 6587 | 2020-09-17T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `a84577a184adf232` | OK |
| PEPE | 1000PEPEUSDT | 5m | 355674 | 2023-05-05T16:30:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `822ce1fc9832f004` | OK |
| PEPE | 1000PEPEUSDT | 1h | 29640 | 2023-05-05T16:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `999fd89b04e6b33f` | OK |
| PEPE | 1000PEPEUSDT | 4h | 7410 | 2023-05-05T16:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `10fa162424ccffd6` | OK |
| PEPE | 1000PEPEUSDT | 12h | 2470 | 2023-05-05T12:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `4cbc06d806d1f7e5` | OK |
| PEPE | 1000PEPEUSDT | 1d | 1234 | 2023-05-06T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `aaadd5d267f35b04` | OK |
| PEPE | 1000PEPEUSDT | 1w | 176 | 2023-05-08T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `af42afc572adc568` | OK |
| PEPE | 1000PEPEUSDT | funding | 3706 | 2023-05-05T16:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `ecb902462089afb5` | OK |
| DOGE | DOGEUSDT | 5m | 652116 | 2020-07-10T09:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `67f9d282df57efb4` | OK |
| DOGE | DOGEUSDT | 1h | 54343 | 2020-07-10T09:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `fa5858dfa10eb340` | OK |
| DOGE | DOGEUSDT | 4h | 13586 | 2020-07-10T08:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `2dfd29c6f8809483` | OK |
| DOGE | DOGEUSDT | 12h | 4529 | 2020-07-10T00:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `b7df033d6e1f2749` | OK |
| DOGE | DOGEUSDT | 1d | 2263 | 2020-07-11T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `bfb08cac13c47a72` | OK |
| DOGE | DOGEUSDT | 1w | 323 | 2020-07-13T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `c27d0bcea865748d` | OK |
| DOGE | DOGEUSDT | funding | 6794 | 2020-07-10T08:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `fe51a47364b107a8` | OK |
| BONK | 1000BONKUSDT | 5m | 297816 | 2023-11-22T14:00:00Z | 2026-09-21T15:55:00Z | 6 | 0 (0) | `1d738a5cd662bb08` | OK |
| BONK | 1000BONKUSDT | 1h | 24818 | 2023-11-22T14:00:00Z | 2026-09-21T15:00:00Z | 0 | 0 (0) | `6bc3e0f7946cda33` | OK |
| BONK | 1000BONKUSDT | 4h | 6205 | 2023-11-22T12:00:00Z | 2026-09-21T12:00:00Z | 0 | 0 (0) | `f8494679f8f9c439` | OK |
| BONK | 1000BONKUSDT | 12h | 2068 | 2023-11-22T12:00:00Z | 2026-09-21T00:00:00Z | 0 | 0 (0) | `2f47ad221cfaf1fa` | OK |
| BONK | 1000BONKUSDT | 1d | 1033 | 2023-11-23T00:00:00Z | 2026-09-20T00:00:00Z | 0 | 0 (0) | `3c7035f50fabb59b` | OK |
| BONK | 1000BONKUSDT | 1w | 147 | 2023-11-27T00:00:00Z | 2026-09-14T00:00:00Z | 0 | 0 (0) | `5fcbd0afa58560ff` | OK |
| BONK | 1000BONKUSDT | funding | 6204 | 2023-11-22T16:00:00Z | 2026-09-21T16:00:00Z | 0 | — (coverage OK) | `750ff559aadf9418` | OK |
<!-- S3-TABLE END id=cells -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## Contract multipliers — printed and normalized» (section), bytes [23913, 28350), sha256 `a9f76ef813ea9504` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=multipliers mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[23913,28350) sha256=a9f76ef813ea95044aac27316e6d0bc4b1a69cb024712950c87119e29854de47 -->
## Contract multipliers — printed and normalized

the venue publishes NO ['multiplier', 'contractSize', 'contract_size', 'quantity_multiplier', 'contractMultiplier', 'multiplierSize'] field for any of these contracts — the multiplier lives in the baseAsset NAME and is read from it [LEAN D-l]. Symbols whose multiplier is not 1: ['1000PEPEUSDT', '1000BONKUSDT']. EVERY PRICE ON 1000PEPEUSDT IS QUOTED PER 1000 TOKENS AND EVERY PRICE ON 1000BONKUSDT IS QUOTED PER 1000 TOKENS.

Capture: `research_outputs/tierc10/data/CONTRACT_SPECS.json` sha256 `275b218d04a18a4a9383b1b16c5f18a1c1bd644875c8849a8a8c590113ed76d4` (exchangeInfo response sha256 `25d7de1b288f58e3541788c53eeb1ed91ffdf152860213218df1b54771b83725`). NOT carried here, and not by name either: no run-time clock key enters a deterministic artifact (F-DET scans these files for the key names themselves). The capture's own stamp lives in CONTRACT_SPECS.json — a PROVENANCE file, which holds clocks by design and is never in the determinism set. This row pins that file's BYTES by sha256 instead, and F-D-MULT re-hashes it every run.

| asset | symbol | venue | baseAsset | multiplier (tokens / contract unit) | tokens a quoted price covers | tick | qty step | min qty | min notional | multiplier fields the venue publishes |
|---|---|---|---|---:|---|---|---|---|---|---|
| BTC | BTCUSDT | BINANCE_USDTM | BTC | 1 | 1 | 0.10 | 0.001 | 0.001 | 50 | NONE |
| ETH | ETHUSDT | BINANCE_USDTM | ETH | 1 | 1 | 0.01 | 0.001 | 0.001 | 20 | NONE |
| SOL | SOLUSDT | BINANCE_USDTM | SOL | 1 | 1 | 0.0100 | 0.01 | 0.01 | 5 | NONE |
| NEAR | NEARUSDT | BINANCE_USDTM | NEAR | 1 | 1 | 0.0010 | 1 | 1 | 5 | NONE |
| ZEC | ZECUSDT | BINANCE_USDTM | ZEC | 1 | 1 | 0.01 | 0.001 | 0.001 | 5 | NONE |
| ENA | ENAUSDT | BINANCE_USDTM | ENA | 1 | 1 | 0.0000100 | 1 | 1 | 5 | NONE |
| PUMPFUN | PUMPUSDT | BINANCE_USDTM | PUMP | 1 | 1 | 0.0000010 | 1 | 1 | 5 | NONE |
| HYPE | HYPEUSDT | BINANCE_USDTM | HYPE | 1 | 1 | 0.00100 | 0.01 | 0.01 | 5 | NONE |
| MNT | MNTUSDT | BYBIT_V5_LINEAR | MNT | 1 | 1 | 0.00010 | 0.1 | 0.1 | 5 | NONE |
| SUI | SUIUSDT | BINANCE_USDTM | SUI | 1 | 1 | 0.000100 | 0.1 | 0.1 | 5 | NONE |
| LTC | LTCUSDT | BINANCE_USDTM | LTC | 1 | 1 | 0.01 | 0.001 | 0.001 | 20 | NONE |
| XMR | XMRUSDT | BINANCE_USDTM | XMR | 1 | 1 | 0.01 | 0.001 | 0.001 | 5 | NONE |
| BNB | BNBUSDT | BINANCE_USDTM | BNB | 1 | 1 | 0.010 | 0.01 | 0.01 | 5 | NONE |
| UNI | UNIUSDT | BINANCE_USDTM | UNI | 1 | 1 | 0.0010 | 1 | 1 | 5 | NONE |
| PEPE | 1000PEPEUSDT | BINANCE_USDTM | 1000PEPE | 1000 | 1000 | 0.0000001 | 1 | 1 | 5 | NONE |
| DOGE | DOGEUSDT | BINANCE_USDTM | DOGE | 1 | 1 | 0.000010 | 1 | 1 | 5 | NONE |
| BONK | 1000BONKUSDT | BINANCE_USDTM | 1000BONK | 1000 | 1000 | 0.0000010 | 1 | 1 | 5 | NONE |

### Normalization

NORMALIZED PRICE = venue price / multiplier (USDT per ONE token); NORMALIZED QUANTITY = venue quantity x multiplier (tokens). For 1000PEPEUSDT and 1000BONKUSDT the multiplier is 1000, i.e. EVERY PRICE THE VENUE QUOTES ON THOSE TWO TAPES IS PER 1000 TOKENS; for the other fifteen it is 1 and normalization is the identity. THE NORMALIZATION IS A PURE SCALING OF THE PRICE SERIES BY A CONSTANT, AND THEREFORE CANNOT MOVE ANY RATIO-VALUED STATISTIC: for a constant k > 0, R = (exit - entry) / (entry - stop) has k in numerator and denominator and is unchanged; an ATR-normalized height (high - low) / ATR is a price over a price and is unchanged; a log return ln(p_t / p_{t-1}) is unchanged; the notional price x quantity is unchanged because the quantity scales by 1/k. What DOES move is anything quoted in absolute price units — a tick size, a MIN_NOTIONAL, a per-unit fee in USDT — and those are filed per symbol here, unnormalized, as the venue states them. NAIAD DOES NOT REWRITE THE TAPE: the parquet holds the venue's own numbers; normalization is a READING, applied by whoever needs per-token units, and F-D-MULT proves on the real 1000PEPEUSDT and 1000BONKUSDT tapes that applying it leaves every ratio-valued statistic identical.

Per symbol, the reading:

- **1000PEPEUSDT** — EVERY PRICE ON 1000PEPEUSDT IS QUOTED PER 1000 TOKENS. normalized price = venue price / 1000 (USDT per one PEPE); normalized quantity = venue quantity x 1000 (PEPE tokens).
- **1000BONKUSDT** — EVERY PRICE ON 1000BONKUSDT IS QUOTED PER 1000 TOKENS. normalized price = venue price / 1000 (USDT per one BONK); normalized quantity = venue quantity x 1000 (BONK tokens).


<!-- S3-SPLICE END id=multipliers -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## The two-token trap — F-D-4 (the LIT precedent)» (section), bytes [28350, 33573), sha256 `56e9d1e98291defa` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=fd4 mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[28350,33573) sha256=56e9d1e98291defaa26e7610a1e3b24c51627bf7d81dc6c4f60436704ccc8250 -->
## The two-token trap — F-D-4 (the LIT precedent)

FAILS IF any symbol's history predates its intended listing unfloored. The floor of a lens is the open of the grid bar that CONTAINS the listing instant; a bar opening before it is prior-asset history and is a HALT-grade finding.

Listing source: the VENUE's own onboardDate / launchTime, captured write-once in VENUE_PROBE.json before the first bar was fetched.

engine/cells.py LIT_FLOOR_MS (2025-12-23T00:00Z) — LITUSDT carried Litentry before the Lighter perpetual listing and the loader asserts a hard floor for it. THE LIVE RISK ON THIS PANEL IS PUMPFUN: the venue probe recorded a REJECTED PUMPBTCUSDT (baseAsset PUMPBTC != PUMP, 'a different asset') and PUMPFUN is mapped to PUMPUSDT by [LEAN D-d]. The rejection is carried here so the two tokens can never be confused.

| asset | symbol | intended base | probe baseAsset | listing | first 4h bar | tape predates the listing INSTANT | tape predates the HARD FLOOR | hard-floored, every lens | floor bar rebuilt from its 5m children | floor seam |
|---|---|---|---|---|---|---|---|---|---|---|
| BTC | BTCUSDT | BTC | BTC | 2019-09-08T17:55:00Z | 2019-09-08T16:00:00Z | True | False | True | True (25 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| ETH | ETHUSDT | ETH | ETH | 2019-11-27T07:45:00Z | 2019-11-27T04:00:00Z | True | False | True | True (3 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| SOL | SOLUSDT | SOL | SOL | 2020-09-14T07:00:00Z | 2020-09-14T04:00:00Z | True | False | True | True (12 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| NEAR | NEARUSDT | NEAR | NEAR | 2020-10-15T08:00:00Z | 2020-10-15T08:00:00Z | False | False | True | True (48 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| ZEC | ZECUSDT | ZEC | ZEC | 2020-02-05T08:00:00Z | 2020-02-05T08:00:00Z | False | False | True | True (48 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| ENA | ENAUSDT | ENA | ENA | 2024-04-02T12:30:00Z | 2024-04-02T12:00:00Z | True | False | True | True (42 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| PUMPFUN | PUMPUSDT | PUMP | PUMP | 2025-07-10T07:30:00Z | 2025-07-10T04:00:00Z | True | False | True | True (6 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| HYPE | HYPEUSDT | HYPE | HYPE | 2025-05-30T10:30:00Z | 2025-05-30T08:00:00Z | True | False | True | True (18 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| MNT | MNTUSDT | MNT | MNT | 2023-10-02T05:40:55Z | 2023-10-02T04:00:00Z | True | False | True | True (17 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| SUI | SUIUSDT | SUI | SUI | 2023-05-03T00:00:00Z | 2023-05-03T16:00:00Z | False | False | True | True (48 children, the tape's FIRST bar — the venue serves NO bar at the floor (the tape begins after the listing instant)) | NO seam (no bar before the floor) |
| LTC | LTCUSDT | LTC | LTC | 2020-01-09T08:05:00Z | 2020-01-09T08:00:00Z | True | False | True | True (47 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| XMR | XMRUSDT | XMR | XMR | 2020-02-03T08:00:00Z | 2020-02-03T08:00:00Z | False | False | True | True (48 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| BNB | BNBUSDT | BNB | BNB | 2020-02-10T08:00:00Z | 2020-02-10T08:00:00Z | False | False | True | True (48 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| UNI | UNIUSDT | UNI | UNI | 2020-09-18T07:00:00Z | 2020-09-18T04:00:00Z | True | False | True | True (12 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| PEPE | 1000PEPEUSDT | 1000PEPE | 1000PEPE | 2023-05-05T00:00:00Z | 2023-05-05T16:00:00Z | False | False | True | True (42 children, the tape's FIRST bar — the venue serves NO bar at the floor (the tape begins after the listing instant)) | NO seam (no bar before the floor) |
| DOGE | DOGEUSDT | DOGE | DOGE | 2020-07-10T09:00:00Z | 2020-07-10T08:00:00Z | True | False | True | True (36 children, the bar AT the listing floor) | NO seam (no bar before the floor) |
| BONK | 1000BONKUSDT | 1000BONK | 1000BONK | 2023-11-22T14:00:00Z | 2023-11-22T12:00:00Z | True | False | True | True (24 children, the bar AT the listing floor) | NO seam (no bar before the floor) |

102 (asset, lens) cells over ['5m', '1h', '4h', '12h', '1d', '1w']: the INTENDED asset is confirmed against the venue's own baseAsset on **17 / 17** (no mismatch); bars before a floor: **NONE**; floor bars rebuilt exactly from their own 5m children: **17 / 17**; floor seams that EXIST at all: **0** (a seam can only exist where the tape holds a bar BEFORE the floor — none does, so the continuity limit binds on nothing and that arm of F-D-4 is proven by its BREAK leg alone [LEAN D-i]); discontinuous floor seams: **none**.

Whole-tape 4h seam census (context for the limit 1.0): 179996 adjacent seams over the panel, largest real |ln(open/close)| = 0.1551.

REJECTED and carried: **PUMPFUN** `PUMPBTCUSDT` — baseAsset PUMPBTC != PUMP: a different asset


<!-- S3-SPLICE END id=fd4 -->

## S3 · F-D-4 tally

*REPORT-ONLY · Tier-E · read from `research_outputs/tierc10/data/STAGE_D_MANIFEST.json` two_token_trap; the re-measure re-reads every kline cell through `load_asof` and counts bars opening before that cell's filed floor_open.*

F-D-4 TALLY: cells checked **102** (17 assets × 6 lenses) · bars before a floor **0** · intended asset confirmed **17 / 17** · hard-floored every lens **True** · floor bars rebuilt from 5m **17** · floor seams that exist **0** · discontinuous floor seams **0**

F-D-4 RE-MEASURED: cells **102** · bars before a floor **0**

Rejections carried: PUMPFUN `PUMPBTCUSDT` — baseAsset PUMPBTC != PUMP: a different asset

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## Data-spend audit — F-D-5 {never-touched / display-only / scored}» (section), bytes [33573, 42917), sha256 `95beb5ca747fa7ba` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=fd5 mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[33573,42917) sha256=95beb5ca747fa7ba5f57d8e828d7825aa411a5c36f99d5ed7f39e00ae66dbf2b -->
## Data-spend audit — F-D-5 {never-touched / display-only / scored}

grep the contract's corpus WHOLE and classify every admitted asset {never-touched / display-only / scored} with the evidence line that justifies the class. HARD DEPENDENCY of P-GEN-1, whose text must promise 'LOAO printed twice (all admitted · never-touched only)' — without the never-touched list that clause cannot be honoured.

Corpus: 65 files, whole, no sampling. Excluded: ['_reviewer_box', 'docs/history', 'research_outputs/tierc10', 'research_outputs/tierc10_run2', '.git'] — _reviewer_box/ and docs/history/ hold multi-megabyte single-line JSON (the GREP HAZARD; every kept line is also cut at 240 chars); research_outputs/tierc10*/ is THIS BUILD's own output and would make the audit self-referential and unreproducible.

'root_book' is every root-level .md and .json — the estate's result books, its builder contracts and its change logs together. A HIT THERE IS NOT PROOF OF SCORING (HYPE is named 53 times there and is display-only): the class of an asset is decided by the registers below, not by a hit count. The one-directional rule F-D-5 asserts is the conservative one — a NEVER-TOUCHED asset must have ZERO root_book hits. That is stricter than the definition, so it can be too strict, never too lenient: it cannot pass an asset a scored result rode.

Definitions of record: **never-touched** = the asset has never appeared in any scored result in this estate · **display-only** = it appeared in a chart / brief / census print but never in a scored book · **scored** = a registered or TC-series result rode it

Registers READ as literals (never imported):

- `tc_series_scored_universe` — scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']
- `oracle_display_roster` — scripts/oracle_daily.py REGISTER['ROSTER']['value'] = ['BTCUSDT', 'ETHUSDT', 'ENAUSDT', 'SOLUSDT', 'USELESSUSDT', 'NEARUSDT', '1000PEPEUSDT', 'LITUSDT', 'FARTCOINUSDT', 'HYPEUSDT', 'XPLUSDT', 'ZECUSDT', 'UNIUSDT', 'LTCUSDT', 'BNBUSDT', 'XMRUSDT', 'DOGEUSDT', '1000BONKUSDT']
- `frozen_study_basket` — engine/cells.py SYMBOLS (charter §4) = ['BTCUSDT', 'ETHUSDT', 'FARTCOINUSDT', 'HYPEUSDT', 'JTOUSDT', 'LITUSDT', 'NEARUSDT', 'SOLUSDT', 'TAOUSDT', 'ZECUSDT']

| asset | stem | class | in TC-series scored universe | in Oracle display roster | in frozen study basket | grep hits | evidence |
|---|---|---|---|---|---|---:|---|
| BTC | BTCUSDT | **scored** | True | True | True | 242 | BTCUSDT is in the TC-series SCORED UNIVERSE (scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']); every registered TC-series result rides it |
| ETH | ETHUSDT | **scored** | True | True | True | 156 | ETHUSDT is in the TC-series SCORED UNIVERSE (scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']); every registered TC-series result rides it |
| SOL | SOLUSDT | **scored** | True | True | True | 134 | SOLUSDT is in the TC-series SCORED UNIVERSE (scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']); every registered TC-series result rides it |
| NEAR | NEARUSDT | **scored** | True | True | True | 129 | NEARUSDT is in the TC-series SCORED UNIVERSE (scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']); every registered TC-series result rides it |
| ZEC | ZECUSDT | **scored** | True | True | True | 191 | ZECUSDT is in the TC-series SCORED UNIVERSE (scripts/tierc2_rules.py REGISTER['UNIVERSE']['value'] = ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT']); every registered TC-series result rides it |
| ENA | ENAUSDT | **display-only** | False | True | False | 6 | ENAUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| PUMPFUN | PUMPUSDT | **never-touched** | False | False | False | 9 | PUMPUSDT is in NO estate register: not the TC-series scored universe, not the Oracle's display ROSTER, not the frozen study basket; and no line of the 65-file corpus places it in a scored book |
| HYPE | HYPEUSDT | **display-only** | False | True | True | 65 | HYPEUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) and the FROZEN STUDY BASKET (engine/cells.py SYMBOLS, tier C) — looked at, never scored |
| MNT | MNTUSDT_BYBIT | **never-touched** | False | False | False | 7 | MNTUSDT_BYBIT is in NO estate register: not the TC-series scored universe, not the Oracle's display ROSTER, not the frozen study basket; and no line of the 65-file corpus places it in a scored book |
| SUI | SUIUSDT | **never-touched** | False | False | False | 0 | SUIUSDT is in NO estate register: not the TC-series scored universe, not the Oracle's display ROSTER, not the frozen study basket; and no line of the 65-file corpus places it in a scored book |
| LTC | LTCUSDT | **display-only** | False | True | False | 6 | LTCUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| XMR | XMRUSDT | **display-only** | False | True | False | 9 | XMRUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| BNB | BNBUSDT | **display-only** | False | True | False | 7 | BNBUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| UNI | UNIUSDT | **display-only** | False | True | False | 6 | UNIUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| PEPE | 1000PEPEUSDT | **display-only** | False | True | False | 4 | 1000PEPEUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| DOGE | DOGEUSDT | **display-only** | False | True | False | 6 | DOGEUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |
| BONK | 1000BONKUSDT | **display-only** | False | True | False | 4 | 1000BONKUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) — looked at, never scored |

COUNTS: {'scored': 5, 'display-only': 9, 'never-touched': 3}. **NEVER-TOUCHED: ['PUMPFUN', 'MNT', 'SUI']** — this is the list P-GEN-1's 'LOAO printed twice (all admitted · never-touched only)' clause needs, and without it that clause cannot be honoured.

The evidence lines that decide the two the contract says must be READ, not assumed:

- **PUMPFUN** -> `never-touched`. PUMPUSDT is in NO estate register: not the TC-series scored universe, not the Oracle's display ROSTER, not the frozen study basket; and no line of the 65-file corpus places it in a scored book
    - `exchange/status/LEDGER_ARGUS.md:545` [ledger] NPC PUMPFUN MNT ZCAT, none has a Binance perpetual. JTO and TAO leave the roster (not in the
    - `research_outputs/oracle/roster_probe_2026-09-21.json:5` [probe_ledger] "PUMPFUNUSDT",
    - `research_outputs/oracle/roster_probe_2026-09-21.json:33` [probe_ledger] "dropped": "PUMPFUNUSDT",
- **HYPE** -> `display-only`. HYPEUSDT is NOT in the TC-series scored universe, and IS in the Oracle's display ROSTER (scripts/oracle_daily.py REGISTER['ROSTER']['value'], 18 symbols) and the FROZEN STUDY BASKET (engine/cells.py SYMBOLS, tier C) — looked at, never scored
    - `CHANGELOG.md:426` [root_book] per 4h-grid symbol (JTO/TAO/HYPE/FARTCOIN/LIT), two REST re-fetch attempts
    - `CHANGELOG.md:430` [root_book] prompt assumed — BTC/ETH/NEAR/ZEC 8h; JTO/TAO/HYPE/FARTCOIN/LIT 4h; SOL
    - `LEDGER.md:113` [ledger] - Gaps: 1 listing_edge (BTC 1m, 2019-09-08 19:00) + 5 exchange_side (funding, all at 2026-06-24 04:00, refetched 2x) + 0 download_hole. External anchors: HYPE listing confirmed to the minute and LIT floor to the day vs Binance announcements
    - `LEDGER.md:217` [ledger] (g) RC-0: all 10 assets (7 scored + HYPE, FARTCOIN, LIT) carry {1m,5m,15m,1h,4h,12h}; 30m and 1d are ABSENT for every asset; 15m present for every asset. Both absent TFs are locally resamplable (30m from 15m/1m, 1d from 1h/1m) — feasibility
    - `Naiad_Phase0_Charter.md:96` [charter] | HYPE | young (~2024-12→) | Forward-mostly evidence |
    - `Naiad_Phase0_Charter.md:114` [charter] - **Slippage** per side (confirmed at ratification): tier A (BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE, FARTCOIN, LIT) 10 bps.
    - `research_outputs/oracle/roster_probe_2026-09-21.json:204` [probe_ledger] "HYPEUSDT",
    - `research_outputs/oracle/roster_probe_2026-09-21.json:229` [probe_ledger] "HYPEUSDT",


<!-- S3-SPLICE END id=fd5 -->

## S3 · F-D-5 tally

*REPORT-ONLY · Tier-E · read from `research_outputs/tierc10/data/DATA_SPEND_AUDIT.json` counts / classes.*

F-D-5 COUNTS: never-touched **3** · display-only **9** · scored **5** · assets **17**

| class | count | assets |
|---|---:|---|
| never-touched | 3 | PUMPFUN MNT SUI |
| display-only | 9 | ENA HYPE LTC XMR BNB UNI PEPE DOGE BONK |
| scored | 5 | BTC ETH SOL NEAR ZEC |

NEVER-TOUCHED (P-GEN-1's second LOAO panel): **PUMPFUN MNT SUI**

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## The tiered costs haircut twin [VETO "tiers"]» (section), bytes [42917, 45866), sha256 `9b5cb26fa47d9f9e` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=haircut mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[42917,45866) sha256=9b5cb26fa47d9f9e33f1454f799166828651563f7309bde5aa436cbfcbee85c9 -->
## The tiered costs haircut twin [VETO "tiers"]

every row gets the charter model as a HAIRCUT TWIN BESIDE the TC-series toll. The 5-asset control's TC-series accounting stays UNTOUCHED — round_trip_bps_used is the same object it always was, on every one of the 17 rows; the twin is an ADDED column and nothing reads it unless it asks for it [VETO 'tiers'].

Contract clause, parsed (never typed): `every row gets the charter model as a HAIRCUT TWIN beside the TC-series toll — slippage/side tier A {BTC ETH} 2 bps · tier B {SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR} 5 · tier C {ENA PUMPFUN HYPE MNT PEPE BONK} 10`

Charter source of the model: Naiad_Phase0_Charter.md:114 — - **Slippage** per side (confirmed at ratification): tier A (BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE, FARTCOIN, LIT) 10 bps.

the charter's own tiers name the ratification basket (BTC ETH | SOL NEAR ZEC JTO TAO | HYPE FARTCOIN LIT); the TIER-C10 contract clause EXTENDS the same model to the seventeen, and it is the contract clause — not the charter line — that this table is parsed from

| tier | bps per side | assets |
|---|---:|---|
| A | 2.0 | BTC ETH |
| B | 5.0 | SOL NEAR ZEC LTC BNB DOGE UNI SUI XMR |
| C | 10.0 | ENA PUMPFUN HYPE MNT PEPE BONK |

COVERAGE: 2 + 9 + 6 = 17 assets, admitted 17; every admitted asset assigned: **True**; tiered but not admitted: none.

Cost law: `cost_px = ((FEE_BPS_SIDE + slippage_bps_side) / 10_000) * (entry_px + exit_px); cost_r = cost_px / risk_px; net_r_twin = gross_r - cost_r (tierc10_data.haircut_twin_net_r / haircut_twin_for_stem — importable, so Stage B never re-derives a tier)`

THE TC-SERIES TOLL IS UNTOUCHED ON EVERY ROW: **True** (round_trip_bps_used == FEE_BPS_ROUND_TRIP for all 17; the twin is an ADDED column).

| asset | stem | tier | slippage bps/side | fee bps/side | charter bps/side | charter round trip bps | TC-series round trip bps (UNTOUCHED) |
|---|---|---|---:|---:|---:|---:|---:|
| BTC | BTCUSDT | A | 2.0 | 5.0 | 7.0 | 14.0 | 10.0 |
| ETH | ETHUSDT | A | 2.0 | 5.0 | 7.0 | 14.0 | 10.0 |
| SOL | SOLUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| NEAR | NEARUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| ZEC | ZECUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| ENA | ENAUSDT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |
| PUMPFUN | PUMPUSDT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |
| HYPE | HYPEUSDT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |
| MNT | MNTUSDT_BYBIT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |
| SUI | SUIUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| LTC | LTCUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| XMR | XMRUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| BNB | BNBUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| UNI | UNIUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| PEPE | 1000PEPEUSDT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |
| DOGE | DOGEUSDT | B | 5.0 | 5.0 | 10.0 | 20.0 | 10.0 |
| BONK | 1000BONKUSDT | C | 10.0 | 5.0 | 15.0 | 30.0 | 10.0 |


<!-- S3-SPLICE END id=haircut -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## As-of hazards for downstream loaders» (section), bytes [53082, 54263), sha256 `8931a2da1f0947d8` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=asof mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[53082,54263) sha256=8931a2da1f0947d88553b6960af04ff15a2d597fa0476f4a78ded272fffb4dde -->
## As-of hazards for downstream loaders

- Klines: these rows PRE-DATE TC10 and are never deleted [LEAN D-e]; tierc10_data.load_asof cuts them, but tierc2_baseline.load_klines reads the WHOLE file — a TC10 lane that loads one of these files through it without an as-of cut reads past the pin. Files: `klines/BTCUSDT_5m.parquet` +6, `klines/ETHUSDT_5m.parquet` +6, `klines/SOLUSDT_5m.parquet` +6, `klines/NEARUSDT_5m.parquet` +6, `klines/ZECUSDT_5m.parquet` +6, `klines/ENAUSDT_5m.parquet` +6, `klines/HYPEUSDT_5m.parquet` +6, `klines/LTCUSDT_5m.parquet` +6, `klines/XMRUSDT_5m.parquet` +6, `klines/BNBUSDT_5m.parquet` +6, `klines/UNIUSDT_5m.parquet` +6, `klines/1000PEPEUSDT_5m.parquet` +6, `klines/DOGEUSDT_5m.parquet` +6, `klines/1000BONKUSDT_5m.parquet` +6.
- Funding: [LEAN D-g] a print belongs to the hour its stamp FLOORS to; load_funding_asof returns funding_hour_ms and cuts on it; an interval-sum funding law must sum on funding_hour_ms, never on the raw stamp. Floor hour == nearest hour on every file: **True**; largest stamp offset past its hour over the panel: 47 ms; files holding a print stamped a few ms after the AS_OF close (it is the AS_OF hour's print): 16.

<!-- S3-SPLICE END id=asof -->

*REPORT-ONLY · Tier-E · the publications-disagree SUMMARY is the section's lead and its per-lens table; the whole-history audit tables stay in `research_outputs/tierc10/data/STAGE_D_MANIFEST.md` and `research_outputs/tierc10/data/REST_VS_SNAPSHOT_AUDIT.json` / `research_outputs/tierc10/data/ARCHIVE_VS_SNAPSHOT_AUDIT.json`.*

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## The venue's two publications disagree (archive vs REST) — and the panel is heterogeneous» (lead), bytes [46367, 48236), sha256 `b5ec2b784aa8a7de` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=pubs_lead mode=lead src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[46367,48236) sha256=b5ec2b784aa8a7ded375cea531810f31117d5e1d1b392d7730a2599f7a9c6ba4 -->
## The venue's two publications disagree (archive vs REST) — and the panel is heterogeneous

the venue publishes every native bar TWICE — its REST API and its BULK ARCHIVE — and the two DIFFER on a small set of incident stamps. The panel is PUBLICATION-HETEROGENEOUS there, MEASURED per file over the whole history, both ways. At 4h (the lens 1d/1w derive from): identical to REST and differing from the archive: ['BTCUSDT', 'ETHUSDT', 'SOLUSDT', 'NEARUSDT', 'ZECUSDT', 'SUIUSDT', 'LTCUSDT']; identical to the ARCHIVE and differing from REST: ['ENAUSDT', 'XMRUSDT', 'BNBUSDT', 'UNIUSDT', '1000PEPEUSDT', 'DOGEUSDT', '1000BONKUSDT']; identical to both: ['PUMPUSDT', 'HYPEUSDT']; differing from both: none; unaudited: none. Assets whose OWN lenses carry different publications (a lens TC10 fetched whole is REST even where the asset's older lenses carry the archive): ['1000BONKUSDT', '1000PEPEUSDT', 'BNBUSDT', 'DOGEUSDT', 'ENAUSDT', 'UNIUSDT', 'XMRUSDT']. The ARCHIVE is also INCOMPLETE as a publication: at 4h it LACKS 120 bars that the snapshot holds (whole days), and publishes nothing at all for 947 more (not compared, named per file in the census). And 'the ARCHIVE' is itself TWO forms: the census reads its MONTHLY zips (as the estate's backfill does); on the incident days probed the monthly and the DAILY zip of the same day disagree with EACH OTHER on 22 bars, assets ['BTCUSDT'] (archive_forms; NOT probed off the incident days). No cached bar was changed — a prefix is never rewritten. Which publication is the record is the operator's ruling: ruling ARCHIVE makes the REST-carrying files the odd ones out, ruling REST the ARCHIVE-carrying ones. CORRECTION: the first filing of this manifest said 'pre-existing files carry the ARCHIVE's bar' — that was INFERRED from how the files were assembled, not measured, and it is WRONG for the classics.

<!-- S3-SPLICE END id=pubs_lead -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «### Which publication each native file carries (MEASURED, per lens)» (section), bytes [48236, 49241), sha256 `b5970597f2138ade` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=pubs_carries mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[48236,49241) sha256=b5970597f2138adeb2c8b332cbf8beed8292da44be19a881aad9b16beabc9d96 -->
### Which publication each native file carries (MEASURED, per lens)

| lens | identical to REST (differs from archive) | identical to ARCHIVE (differs from REST) | identical to both | differs from both | unaudited | single publication |
|---|---|---|---|---|---|---|
| 5m | BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT SUIUSDT LTCUSDT | ENAUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT | PUMPUSDT HYPEUSDT | — | — | MNTUSDT_BYBIT |
| 1h | BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT SUIUSDT LTCUSDT | ENAUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT | PUMPUSDT HYPEUSDT | — | — | MNTUSDT_BYBIT |
| 4h | BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT SUIUSDT LTCUSDT | ENAUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT | PUMPUSDT HYPEUSDT | — | — | MNTUSDT_BYBIT |
| 12h | BTCUSDT ETHUSDT SOLUSDT NEARUSDT ZECUSDT ENAUSDT SUIUSDT LTCUSDT XMRUSDT BNBUSDT UNIUSDT 1000PEPEUSDT DOGEUSDT 1000BONKUSDT | — | PUMPUSDT HYPEUSDT | — | — | MNTUSDT_BYBIT |

<!-- S3-SPLICE END id=pubs_carries -->

*REPORT-ONLY · Tier-E · spliced BYTE-EXACT from `research_outputs/tierc10/data/STAGE_D_MANIFEST.md`, heading span «## Operator rulings needed at CLOSE» (section), bytes [56795, 58268), sha256 `36f7a770248e09af` — not re-worded, not re-computed.*

<!-- S3-SPLICE BEGIN id=rulings mode=section src=research_outputs/tierc10/data/STAGE_D_MANIFEST.md bytes=[56795,58268) sha256=36f7a770248e09af1c7799d2927772bab654398029d98a7d55b25d369aa6e87f -->
## Operator rulings needed at CLOSE

1. F-D-1 IS RED and stays RED: the venue's REST API and its BULK ARCHIVE publish different bars on incident stamps and the panel is publication-heterogeneous on them (see venue_publications_disagree). RULING NEEDED: which publication is the record. Ruling ARCHIVE makes the REST-carrying files the odd ones out; ruling REST the ARCHIVE-carrying ones. The archive is no clean alternative: it lacks whole days, publishes nothing before 2020, and its monthly and daily zips disagree with each other on BTC incident bars. No bar is rewritten either way without the operator's word.
2. PUMPFUN -> PUMPUSDT [LEAN D-d]: a printed lean, not a ruling. The roster probe recorded the near-match and explicitly did NOT map it; TC10 maps it because baseAsset PUMP is a TRADING perpetual and PUMPBTCUSDT is rejected by name. Needs the operator's nod at CLOSE.
3. MNT -> Bybit v5 linear, whole tape, stem MNTUSDT_BYBIT [LEAN D-c]: a printed lean, not a ruling (no Binance USDT-M contract exists). The fee charged to it is the estate's flat Binance-era taker figure — an ASSUMPTION; Bybit's own base taker rate is widely quoted higher [UNVERIFIED]. Needs the operator's nod at CLOSE, or a named exclusion.
4. LaCie mirror [LEAN L5]: not done. Every file TC10 fetched exists only in the snapshot on this laptop; the mirror command PUSHES and its default destination would create an empty vault. Needs the operator's destination and consent at CLOSE.

<!-- S3-SPLICE END id=rulings -->

## S3 · Beside the rulings needed — what the operator already said

*REPORT-ONLY · Tier-E · verbatim from `research_outputs/tierc10/OPERATOR_RULINGS.md`, printed beside item 4 above; no inference is drawn from it here.*

- R6 “The LaCie destination and consent to push, which I'll ask for again at close.” — “Permission to push granted”. No destination is named in that text.

