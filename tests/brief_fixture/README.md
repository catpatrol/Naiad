# brief_fixture — the frozen day behind F-B3

Harness for the Daily Brief fixtures (contract §6, Amendment 1 A1.7). Frozen
klines + funding + **canned Tier-2**, so determinism covers the whole artifact
rather than just the parts that avoid the network.

## What is committed, and what is not

| Path | Committed | Why |
|---|---|---|
| `fixture.json` | yes | frozen `as_of` timestamp, asset list, span table |
| `tier2_canned.json` | yes | canned Tier-2 responses (A1.7) |
| `fixture_manifest.json` | yes | sha256 + rows + bytes for every frozen slice |
| `README.md` | yes | this file |
| `data_cache/**.parquet` | **no — FENCED** | raw candles are never committed |
| `out/**` | no | regenerable render of the frozen day |

**The substrate is fenced, not committed.** Charter §10 / build prompt §2
invariant 9 forbid committing raw candles, and `.gitignore` enforces it with a
`data_cache/` rule whose comment explicitly guards "any override that points
inside" the repo — which is exactly what this fixture is. Contract §6 F-B3 asks
for a *committed* kline snapshot; that instruction collides with the charter, the
charter wins, and the operator ratified fencing on 2026-07-27.

The trade is recorded honestly: A1.8's standing "reproduce from a clean checkout"
becomes **reproduce after one command**. `fixture_manifest.json` pins every byte,
so a rebuild is *verifiable* rather than merely plausible — the same contract the
33 MB CENSUS-1b substrate already runs under.

## Rebuilding

From the repo root, with the data estate present in the local cache:

```
.venv/Scripts/python.exe scripts/daily_brief.py --build-fixture 2026-07-20
```

Then run the suite:

```
.venv/Scripts/python.exe scripts/daily_brief.py --fixtures-only
```

The loader verifies every slice against `fixture_manifest.json` before use.
Missing slices print the rebuild command; a slice whose bytes differ is a **hard
failure**, never a silent substitution.

A clean clone on a machine with no estate must first backfill the cache
(`engine/data.py` loaders, or `scripts/census.py --extend`) before the rebuild
can run. That is the same property the CENSUS-1b fence carries.

## Why these spans

Windows are trimmed to keep the rebuild cheap: 1m for 25 days (the prior-day/5d
/20d volume-profile composites), 5m and 15m for 200 days, 1h for 400 days (so the
365d rolling VWAP and the 1y ATR percentile have real history), 4h/12h for 200
days, funding in full. A fixture run therefore carries *less indicator warm-up*
than a live run — which is fine, because F-B3 tests determinism, not agreement
with a live day.

`SOLUSDT` is not optional: F-B4 needs its 2h/4h/8h funding-cadence switches to
prove the per-record integration never assumes 8h × 3/day.
