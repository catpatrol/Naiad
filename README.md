# Project Naiad — Phase 1: Engine + Instrumentation

Cat Patrol's Naiad Agent: an autonomous **paper-trading** research agent
built on the Secret Sauce Cascade v11.0.2 system. This repository holds
**one** deterministic Python engine used identically for backtesting
(replay) and forward paper collection — no live trading, no exchange keys,
no secrets, anywhere.

**Governing documents:** `Naiad_Phase0_Charter.md` (ratified) and
`Naiad_Phase1_Build_Prompt.md`. On any conflict, the charter wins.

> Any number computed from the spent window (BTC 2025-10-06 → 2026-07-07) is
> a plumbing check, never evidence.

---

## One-time setup (Windows)

You need Python 3.11 or newer. In a terminal, from this folder:

```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

*What this does:* creates a private Python environment and installs the five
pinned libraries. *What you should see:* a final line like
`Successfully installed pandas-2.2.3 ...` with no red errors. (On
Mac/Linux: `source .venv/bin/activate` instead of the second line.)

Every command below assumes the environment is active (your prompt shows
`(.venv)`).

## The commands

### 1. Download market data — `scripts/backfill.py`

```
python scripts/backfill.py --symbols BTCUSDT --intervals 5m,1h,4h,12h --end 2026-07-08 --funding
```

*What this does:* downloads Binance USDT-M candles (bulk archives first, then
the live API for recent days) plus funding history into a **local cache
outside this folder** — raw candles are never committed to git. It then
scans for gaps and duplicates. *What you should see:* one line per month
like `BTCUSDT 5m 2026-03: monthly zip, 8928 bars`, ending with
`-> N bars, 0 duplicates, 0 gap(s)` and a coverage report path. A few gaps
can be normal (exchange maintenance); duplicates are never normal.

`--all` does the whole 10-asset basket, every interval, from each asset's
first candle (a large download; hours).

**No-shrink invariant (engine 1.0.2).** A kline or funding cache file can
never lose rows through the save path: every write merges the rows already on
disk back in (new rows win at identical timestamps) and lands atomically via a
temp file + `os.replace`, so no caller — `parity_pack`, `tick`, even
`census.py --repair` — and no interrupted run can truncate or corrupt a cache.
The deliberate consequence is that **there is no deletion primitive**: to
genuinely remove rows you delete the file and re-extend it with
`python scripts/census.py --extend` (which refills from the exchange listing).
Two residuals are accepted by design: two writers racing on the same file may
drop the *other* one's freshly fetched rows (refetchable — never a shrink
below what was on disk), and a file that is deleted and then recreated through
an ordinary engine path restarts at the replay warm-up anchor rather than the
full listing (the census `coverage_ok` check against `data_starts.csv` is the
detector for that case).

### 2. Pin the first-candle table — `scripts/first_candles.py`

```
python scripts/first_candles.py
```

*What this does:* asks Binance for every symbol's first available futures
candle in each interval, applies the hard LIT floor (LITUSDT history before
2025-12-01 belonged to a different token and is refused by the loader
itself), writes `data_starts.csv`, and refreshes the table at the bottom of
this README. *What you should see:* one line per symbol/interval and
`-> data_starts.csv`. The LIT rows must say `<- LIT floor applied`.

### 3. Replay a cell — `scripts/replay.py`

```
python scripts/replay.py --config naiad_v0 --cell BTCUSDT_swing --start 2026-05-01 --end 2026-07-07
```

*What this does:* runs the deterministic engine for one cell (asset ×
mandate) over one window and writes the journal to `journal/` (local only —
real journals live on the `data` branch). Warm-up is enforced: it refuses to
run without ≥2000 exec bars and ≥200 governor bars of history before the
window. *What you should see:* a JSON summary ending in `journal_sha256`,
`tranches`, `final_equity`. Run the same command twice: the
`journal_sha256` must be **identical** — that is fixture F1 live.

The summary numbers are read back from the files on disk after writing:
`rows` = total line count of the run's monthly journal files, and
`journal_sha256` = SHA-256 over the byte concatenation of those files in
chronological (filename) order — anyone can recompute it from the packet
alone (e.g. `cat 2026-05.jsonl 2026-06.jsonl 2026-07.jsonl | sha256sum`).

Cells: `{SYMBOL}_{swing|intraday|position}`, e.g. `ETHUSDT_intraday`.
Configs: `naiad_v0` (paper line) or `v11_faithful` (signals only, parity).

### 4. Run the test suite — fixtures F1–F8

```
python -m pytest fixtures/
```

*What this does:* runs the numbered fixture suite from the build prompt —
determinism, no-lookahead, stop ratchet, risk rails, gate integrity, parity
pack validation, warm-up, journal completeness. *What you should see:* a
green line like `24 passed in ...`. Any `FAILED` line means the build is
broken — stop and report it.

### 5. Build the session packet — `scripts/packet.py`

```
python scripts/packet.py
```

*What this does:* zips journals, reports, configs and a one-page manifest
into `research_outputs/packets/`. *What you should see:*
`packet -> research_outputs/packets/naiad_packet_....zip`. Attach that one
file to the reviewer session.

---

## Deliverable artifacts in this repo

- `research_outputs/parity/` — **D5 parity pack**: `crosses_4h.csv`,
  `crosses_12h.csv` (every confirmed BTC governor cross 2025-10-06 →
  2026-07-07: timestamp, direction, tier) and `case_windows.md` (the six
  case-window event sequences, formatted for bar-by-bar TradingView
  comparison). **All timestamps are UTC** — set your TradingView chart
  timezone to UTC before comparing.
- `research_outputs/dryrun/` + `research_outputs/dryrun_autopsy.md` — **D7
  dry-run autopsy**: the BTC swing-cell plumbing replay (2026-05-01 →
  2026-07-07, spent window) and a report answering every question in
  `fixtures/autopsy_questions.md` from the journal alone.
- `data_starts.csv` — **D2** first-candle table (also at the bottom of this
  README).
- `fixtures/autopsy_questions.md` — the 26 autopsy questions the journal
  schema is derived from.

## Costs (confirmed at Phase 1, charter §5)

Binance USDT-M VIP0 fees confirmed 2026-07-09 from the official fee page:
**taker 0.05%/side** (the charter's 5 bps stands; maker is 0.02% but the
engine books every fill as taker, conservatively). Slippage per side: tier A
(BTC, ETH) 2 bps · tier B (SOL, NEAR, ZEC, JTO, TAO) 5 bps · tier C (HYPE,
FARTCOIN, LIT) 10 bps. Funding: actual historical rates in replay, live
rates in paper.

## Phase 1.5: turning the collector on

**Do NOT do this until the reviewer confirms the Phase 1 verdict criteria
(build prompt §11).** When they do:

1. Create the orphan data branch (one time, from this folder):
   `git checkout --orphan data && git rm -rf . && git commit --allow-empty -m "data branch" && git push origin data && git checkout phase-1`
   *What you should see:* a `data` branch on GitHub with a single empty
   commit.
2. Open `.github/workflows/collector.yml` and remove the leading `# ` from
   exactly these two lines, then commit and push:

   ```yaml
   # schedule:
   #   - cron: "7 * * * *"      # hourly at :07 UTC
   ```

3. *What the first successful run looks like:* on GitHub → Actions →
   "collector", a green run (~5–20 min). On the `data` branch: a new commit
   named `tick: 2026-...` containing `journal/{cell}/{YYYY-MM}.jsonl` files
   and `state/{cell}.json`. Cells whose history is still too short (young
   listings on the 12h mandate) report "warm-up floor not met — skipped";
   that is normal and self-heals as history accrues.
4. Each cell's paper epoch is stamped on its first tick (the UTC month
   start) into `state/{cell}.json` and never moves — every later tick
   recomputes the same journal deterministically and extends it.

You can also test the collector once without enabling the schedule: GitHub →
Actions → collector → "Run workflow" (that button works while the schedule
stays off).

## Repository layout

```
engine/     frozen fixture-gated core (signals, trading, shadows, journal, data)
configs/    named frozen variants: v11_faithful.yaml, naiad_v0.yaml
fixtures/   pytest suite F1–F8 + autopsy_questions.md
research/   empty in Phase 1 (Phase 2's playground)
scripts/    backfill · first_candles · replay · tick · packet
journal/    local replay output (gitignored; real journals -> data branch)
LEDGER.md   data-spend ledger (reviewer-maintained)
```

## Data starts (D2)

<!-- data-starts:begin -->
| Symbol | First valid candle (UTC) | Notes |
|---|---|---|
| BTCUSDT | 2019-09-08 12:00 | per-interval starts differ — see data_starts.csv |
| ETHUSDT | 2019-11-27 00:00 | per-interval starts differ — see data_starts.csv |
| SOLUSDT | 2020-09-14 00:00 | per-interval starts differ — see data_starts.csv |
| NEARUSDT | 2020-10-15 00:00 | per-interval starts differ — see data_starts.csv |
| ZECUSDT | 2020-02-05 00:00 | per-interval starts differ — see data_starts.csv |
| JTOUSDT | 2023-12-08 00:00 | per-interval starts differ — see data_starts.csv |
| TAOUSDT | 2024-04-11 12:00 | per-interval starts differ — see data_starts.csv |
| HYPEUSDT | 2025-05-30 00:00 | per-interval starts differ — see data_starts.csv |
| FARTCOINUSDT | 2024-12-20 12:00 | per-interval starts differ — see data_starts.csv |
| LITUSDT | 2025-12-23 12:00 | per-interval starts differ — see data_starts.csv |
<!-- data-starts:end -->
